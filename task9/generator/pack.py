"""task9: the pack under target/, written from the simulated fab the way its systems export it.

  wafer_sort_zones.csv              the sort database: every sort record with zone fail and tested counts and bins
  process_history.csv               the MES: lot-level steps and the six chamber-per-wafer steps
  cmp_unit_pm_log.xlsx              the ILD-CMP units' maintenance log
  cmp_wafer_fdc.csv                 the polish record per wafer from the units' fault-detection system
  die_maps.sqlite                   the yield database's die maps for the wafers pulled into the review set
  die_geometry.py                   the yield database's die position helpers
  wafer_map_examples/*.png          maps from the yield review deck
  pm_spec_history.md                the module's maintenance-spec revisions and waiver EW-118
  excursion_ticket_YE-2026-031.txt  the yield excursion ticket
  cost_inputs.yaml                  finance's cost inputs
  dep_chamber_rf_hours.csv, facility_particle_counts.csv, scanner_sc4_edge_focus.csv, slurry_lot_coa.csv
"""
import csv
import datetime as dt
import math
import os
import sqlite3
import zlib

import numpy as np
import openpyxl
from openpyxl.styles import Font

import docs as DC
import params as P
import postprocess as PP
import world as WD

F = {"sort": "wafer_sort_zones.csv", "mes": "process_history.csv", "pm": "cmp_unit_pm_log.xlsx", "fdc": "cmp_wafer_fdc.csv",
     "diemaps": "die_maps.sqlite", "geometry": "die_geometry.py", "examples": "wafer_map_examples", "spec": "pm_spec_history.md",
     "ticket": "excursion_ticket_YE-2026-031.txt", "costs": "cost_inputs.yaml", "rf": "dep_chamber_rf_hours.csv",
     "particles": "facility_particle_counts.csv", "sc4": "scanner_sc4_edge_focus.csv", "slurry": "slurry_lot_coa.csv"}
DISTRACTORS = [F["sc4"], F["slurry"]]
T0 = dt.datetime.combine(P.START, dt.time(0, 0))


def ts(t, fmt="%Y-%m-%d %H:%M:%S"):
    return (T0 + dt.timedelta(days=float(t))).strftime(fmt)


def strip_png(path):
    b = open(path, "rb").read()
    out, i = [b[:8]], 8
    while i < len(b):
        n = int.from_bytes(b[i:i + 4], "big")
        t = b[i + 4:i + 8]
        if t in (b"IHDR", b"PLTE", b"IDAT", b"IEND", b"pHYs"):
            out.append(b[i:i + 12 + n])
        i += 12 + n
    open(path, "wb").write(b"".join(out))


class Pack:
    def __init__(self, fab, seed=P.SEED + 7):
        self.fab = fab
        self.rng = np.random.default_rng(seed)

    def write(self, tgt):
        os.makedirs(tgt, exist_ok=True)
        info = {}
        info["sort_rows"] = self.sort(os.path.join(tgt, F["sort"]))
        info["mes_rows"] = self.mes(os.path.join(tgt, F["mes"]))
        info["pm_rows"] = self.pm_log(os.path.join(tgt, F["pm"]))
        info["fdc_rows"] = self.fdc(os.path.join(tgt, F["fdc"]))
        info["diemap_wafers"], info["diemap_rows"] = self.diemaps(os.path.join(tgt, F["diemaps"]))
        open(os.path.join(tgt, F["geometry"]), "w").write(DC.DIE_GEOMETRY)
        self.examples(os.path.join(tgt, F["examples"]))
        open(os.path.join(tgt, F["spec"]), "w").write(DC.SPEC)
        open(os.path.join(tgt, F["ticket"]), "w").write(DC.TICKET)
        open(os.path.join(tgt, F["costs"]), "w").write(DC.costs_yaml()[0])
        info["rf_rows"] = self.rf_hours(os.path.join(tgt, F["rf"]))
        info["particle_rows"] = self.particles(os.path.join(tgt, F["particles"]))
        info["sc4_rows"] = self.sc4(os.path.join(tgt, F["sc4"]))
        info["slurry_rows"] = self.slurry(os.path.join(tgt, F["slurry"]))
        return info

    # ---- the sort database: every sort record, retests included
    def sort(self, path):
        rng = self.rng
        rows = []
        for w in self.fab.wafers:
            if w["scrapped"] or w["sort_t"] > WD.day(P.PULL) + 0.999:
                continue
            prod = w["product"]
            name = prod if rng.random() < 0.96 else str(rng.choice(P.PRODUCTS[prod]["alias"]))
            n = self.fab.zone_n[prod]
            gross = int(n.sum())
            prog = "%s_%s" % (prod.replace("-", ""), "R7" if w["sort_t"] < WD.day(dt.date(2026, 5, 4)) else "R8")
            tester = "T-%02d" % int(rng.integers(1, 7))
            card = "PC-%s%d" % (prod[-1], int(rng.integers(1, 4)))
            records = []
            if rng.random() < 0.02:
                bad = w["fail"].copy()
                k = int(rng.integers(0, 8))
                bad[k] = min(int(n[k]), int(bad[k] + rng.integers(5, max(6, n[k] // 3))))
                records.append((w["sort_t"] - rng.uniform(0.2, 1.5), bad, "N"))
                records.append((w["sort_t"], w["fail"], "Y"))
            else:
                records.append((w["sort_t"], w["fail"], "N"))
            for t, fail, rt in records:
                band_extra = max(0, int(fail[7]) - int(round(n[7] * (fail[:7].sum() / max(n[:7].sum(), 1)))))
                rand = int(fail.sum()) - band_extra
                b_os = int(round(rand * 0.25)); b_f = int(round(rand * 0.40)); b_i = int(round(rand * 0.20))
                b_p = rand - b_os - b_f - b_i
                b_p += int(round(band_extra * 0.6)); b_i += int(round(band_extra * 0.3)); b_f += band_extra - int(round(band_extra * 0.6)) - int(round(band_extra * 0.3))
                rows.append([w["lot"]["lot_id"], w["wafer_id"], name, ts(t), tester, card, prog, gross, gross - int(fail.sum())]
                            + [int(x) for x in fail] + [int(x) for x in n] + [b_os, b_f, b_i, b_p, w["adc"], rt])
        rows.sort(key=lambda r: (r[3], r[1]))
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["lot_id", "wafer_id", "product", "sort_end_ts", "tester", "probe_card", "test_prog_rev", "gross_die", "good_die"]
                        + ["fail_z%d" % k for k in range(1, 9)] + ["tested_z%d" % k for k in range(1, 9)]
                        + ["bin_open_short", "bin_func", "bin_iddq", "bin_param", "adc_label", "retest"])
            wr.writerows(rows)
        return len(rows)

    # ---- the MES: lot-level tracking at 34 steps, wafer-level at the six chamber steps
    def mes(self, path):
        rng = self.rng
        rows = []
        lot_w = {}
        for w in self.fab.wafers:
            lot_w.setdefault(w["lot"]["lot_id"], []).append(w)
        for lot in self.fab.lots:
            ws = lot_w.get(lot["lot_id"], [])
            if not ws:
                continue
            base = lot["cmp_t"]
            for k, step in enumerate(WD.STEPS):
                t_in = base + (k - WD.CMP_STEP) * 1.15 + rng.uniform(-0.2, 0.2)
                recipe = "%s_%s_%s" % (step.replace("-", ""), lot["product"].replace("-", ""), "V3" if k % 3 else "V2")
                if step in WD.WAFER_STEPS:
                    for w in ws:
                        if step == "ILD-CMP":
                            ti = w["polish_t"]
                            to = ti + 0.0035
                        else:
                            ti = t_in + w["slot"] * 0.004 + rng.uniform(0, 0.02)
                            to = ti + rng.uniform(0.003, 0.01)
                        cham = w["chambers"][step]
                        rows.append([lot["lot_id"], w["wafer_id"], k + 1, step, cham.rsplit("-", 1)[0] if step != "ILD-CMP" else "CMP-ILD",
                                     cham, ts(ti), ts(to), recipe, "N"])
                else:
                    tool = lot["tools"][step]
                    rows.append([lot["lot_id"], "", k + 1, step, tool, "", ts(t_in), ts(t_in + rng.uniform(0.02, 0.15)), recipe, "N"])
                    if "LITHO" in step and rng.random() < 0.02:
                        t2 = t_in + rng.uniform(0.2, 0.5)
                        rows.append([lot["lot_id"], "", k + 1, step, lot["tools"][step], "", ts(t2), ts(t2 + 0.05), recipe, "Y"])
        rows.sort(key=lambda r: (r[6], r[0], r[1]))
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["lot_id", "wafer_id", "step_seq", "step_name", "tool_id", "chamber_id", "track_in_ts", "track_out_ts", "recipe",
                         "rework"])
            wr.writerows(rows)
        return len(rows)

    # ---- the units' maintenance log, with the routine checks around the part changes
    def pm_log(self, path):
        rng = self.rng
        rows = []
        pad_names = ["pad IC1010", "IC1010 pad", "polish pad (IC1010)", "pad IC-1010"]
        disk_names = ["cond disk A165", "conditioner disk A165", "CD A165", "cond. disk A-165"]
        ring_names = ["retaining ring RR-300", "ret ring RR300", "RR-300 retaining ring", "ret. ring RR-300"]
        for e in self.fab.events:
            p = []
            if "pad" in e["parts"]:
                p.append(str(rng.choice(pad_names)))
            if "disk" in e["parts"]:
                p.append("%s s/n %d" % (rng.choice(disk_names), int(rng.integers(7000, 9900))))
            if "ring" in e["parts"]:
                p.append(str(rng.choice(ring_names)))
            text = ", ".join(p)
            if e["cls"] == "FULL_PM":
                text += "; platen and carrier inspected"
                if e["waiver"]:
                    text += "; " + str(rng.choice(["cond disk retained per EW-118 (visual OK)", "disk kept, EW-118, inspection pass",
                                                    "CD retained under EW-118"]))
            elif e["cls"] == "UNSCHED":
                text += " - " + ("chipped segment found at check" if e["why"] == "disk damage" else "groove wear past limit")
            t = e["t"]
            back = rng.random() < 0.05
            counter = "" if (rng.random() < 0.04 and not back) else e["counter"]
            rows.append([e["unit"], ts(t + (rng.uniform(0.7, 1.1) if back else 0), "%Y-%m-%d %H:%M"), e["cls"], text, counter,
                         str(rng.choice(P.TECHS)), e["waiver"], "back-entered" if back else ""])
        base = {u: min(w["platen_count"] for w in self.fab.by_unit[u]) for u in WD.UNITS}
        for u in WD.UNITS:
            ini = P.INITIAL[u]
            t_full = -ini["full"] / 40.0 - rng.uniform(0.2, 0.8)
            rows.append([u, ts(t_full, "%Y-%m-%d %H:%M"), "FULL_PM", "%s, %s s/n %d, %s; platen and carrier inspected" % (
                rng.choice(pad_names), rng.choice(disk_names), int(rng.integers(7000, 9900)), rng.choice(ring_names)),
                base[u] - ini["full"], str(rng.choice(P.TECHS)), "", ""])
            if ini["pad"] < ini["full"]:
                rows.append([u, ts(-ini["pad"] / 40.0 - rng.uniform(0.05, 0.2), "%Y-%m-%d %H:%M"), "PAD_CHANGE", str(rng.choice(pad_names)),
                             base[u] - ini["pad"], str(rng.choice(P.TECHS)), "", ""])
        n_days = WD.day(P.LAST_POLISH) + 1
        for u in WD.UNITS:
            for d0 in range(2, n_days, 7):
                rows.append([u, ts(d0 + rng.uniform(0.3, 0.6), "%Y-%m-%d %H:%M"), "PM_CHECK", str(rng.choice(
                    ["weekly check, no findings", "weekly check: slurry arm aligned", "weekly check, pad glazing within limit",
                     "weekly check ok"])), "", str(rng.choice(P.TECHS)), "", ""])
            for d0 in range(4, n_days, 7):
                rows.append([u, ts(d0 + rng.uniform(0.1, 0.9), "%Y-%m-%d %H:%M"), "SLURRY_FLUSH", "slurry line flush and filter change",
                             "", str(rng.choice(P.TECHS)), "", ""])
            for d0 in range(9, n_days, 14):
                rows.append([u, ts(d0 + rng.uniform(0.1, 0.9), "%Y-%m-%d %H:%M"), "ENDPOINT_CAL", "endpoint sensor calibration", "",
                             str(rng.choice(P.TECHS)), "", ""])
        rows.sort(key=lambda r: (r[1], r[0]))
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "PM log"
        ws.append(["unit_id", "event_ts", "event_class", "parts_text", "wafer_counter_at_event", "tech", "waiver_ref", "entry_note"])
        for c in ws[1]:
            c.font = Font(bold=True)
        for r in rows:
            ws.append(r)
        for col, wdt in zip("ABCDEFGH", (8, 17, 14, 70, 12, 13, 10, 12)):
            ws.column_dimensions[col].width = wdt
        wb.save(path)
        PP.normalize_ooxml(path, P.PEOPLE["maint"], P.PEOPLE["maint"], "2025-12-30T16:12:00Z", "2026-08-31T21:05:44Z", excel=True,
                           company=P.FIRM)
        return len(rows)

    # ---- the polish record per wafer
    def fdc(self, path):
        rng = self.rng
        rows = []
        for w in self.fab.wafers:
            temp = rng.normal(41.5 + 0.004 * w["disk"] ** 0.5, 0.6)
            ep = rng.normal(62 if w["product"] != "P-B" else 71, 2.5)
            df = round(w["downforce"], 2) if rng.random() > 0.01 else ""
            cen, edge = (round(w["rr"][0], 1), round(w["rr"][1], 1)) if w["rr"] else ("", "")
            rows.append([w["wafer_id"], w["unit"], ts(w["polish_t"]), w["platen_count"], w["pad"], df,
                         round(temp, 1) if rng.random() > 0.01 else "", round(ep, 1), cen, edge])
        rows.sort(key=lambda r: (r[2], r[1]))
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["wafer_id", "unit_id", "polish_start_ts", "platen_wafer_count", "pad_life_ctr", "downforce_psi", "platen_temperature_c",
                         "endpoint_s", "rr_center_nm_min", "rr_edge_nm_min"])
            wr.writerows(rows)
        return len(rows)

    # ---- the yield database's die maps for the review set
    def diemaps(self, path):
        rng = self.rng
        if os.path.exists(path):
            os.remove(path)
        con = sqlite3.connect(path)
        con.execute("PRAGMA page_size=4096")
        con.execute("CREATE TABLE die_geometry (product TEXT, die_w_mm REAL, die_h_mm REAL, x_offset_mm REAL, y_offset_mm REAL, "
                    "edge_exclusion_mm REAL, gross_die INTEGER)")
        for prod, p in P.PRODUCTS.items():
            con.execute("INSERT INTO die_geometry VALUES (?,?,?,?,?,?,?)", (prod, p["die_w"], p["die_h"], 0.0, 0.0, P.EDGE_EXCL,
                                                                          int(self.fab.zone_n[prod].sum())))
        con.execute("CREATE TABLE wafer_index (wafer_id TEXT, product TEXT, requested_by TEXT, request_ts TEXT)")
        con.execute("CREATE TABLE die_fail (wafer_id TEXT, die_col INTEGER, die_row INTEGER, bin TEXT)")
        n_w, n_r = 0, 0
        self.map_wafers = []
        reqs = [P.PEOPLE["yield_lead"], "R. Ostrowski", "A. Kaminski"]
        for w in sorted((x for x in self.fab.wafers if x["diemap"]), key=lambda x: x["sort_t"]):
            grid = self.fab.grids[w["product"]]
            zone_idx = {}
            for g in grid:
                zone_idx.setdefault(g[5], []).append(g)
            fails = []
            for z in range(1, 9):
                k = int(w["fail"][z - 1])
                if k <= 0:
                    continue
                pick = rng.choice(len(zone_idx[z]), size=k, replace=False)
                for j in pick:
                    g = zone_idx[z][j]
                    b = str(rng.choice(["param", "iddq", "func"], p=[0.6, 0.3, 0.1])) if (z == 8 and rng.random() < 0.6) else \
                        str(rng.choice(["func", "open_short", "iddq", "param"], p=[0.4, 0.25, 0.2, 0.15]))
                    fails.append((w["wafer_id"], g[0], g[1], b))
            con.execute("INSERT INTO wafer_index VALUES (?,?,?,?)", (w["wafer_id"], w["product"], str(rng.choice(reqs)),
                                                                    ts(w["sort_t"] + rng.uniform(0.2, 4))))
            con.executemany("INSERT INTO die_fail VALUES (?,?,?,?)", fails)
            n_w += 1
            n_r += len(fails)
            self.map_wafers.append((w, fails))
        con.commit()
        con.execute("VACUUM")
        con.close()
        return n_w, n_r

    # ---- maps from the yield review deck
    def examples(self, folder):
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
        os.makedirs(folder, exist_ok=True)
        rng = self.rng
        cands = [mw for mw in self.map_wafers if mw[0]["sort_t"] > WD.day(dt.date(2026, 4, 1))]
        pick = [cands[int(i)] for i in sorted(rng.choice(len(cands), size=12, replace=False))]
        for w, fails in pick:
            grid = self.fab.grids[w["product"]]
            p = P.PRODUCTS[w["product"]]
            failed = {(f[1], f[2]) for f in fails}
            fig, ax = plt.subplots(figsize=(3.2, 3.2), dpi=110)
            for g in grid:
                ax.add_patch(plt.Rectangle((g[2] - p["die_w"] / 2, g[3] - p["die_h"] / 2), p["die_w"], p["die_h"],
                                           facecolor="#c0392b" if (g[0], g[1]) in failed else "#7fb77e", edgecolor="white", lw=0.2))
            ax.add_patch(plt.Circle((0, 0), P.WAFER_R, fill=False, lw=0.8, color="#555555"))
            ax.set_xlim(-152, 152)
            ax.set_ylim(-152, 152)
            ax.set_aspect("equal")
            ax.axis("off")
            ax.set_title("%s  %s" % (w["wafer_id"], w["adc"]), fontsize=7)
            fn = os.path.join(folder, "%s.png" % w["wafer_id"].replace(".", "_"))
            fig.savefig(fn, metadata={"Software": None})
            plt.close(fig)
            strip_png(fn)

    # ---- the deposition chambers' RF hours since their last clean (a counter the fab tracks)
    def rf_hours(self, path):
        rng = self.rng
        rows = []
        n_days = WD.day(P.LAST_POLISH) + 1
        for ch in ["DEP-1", "DEP-2", "DEP-3", "DEP-4"]:
            h = float(rng.uniform(0, 110))
            for d0 in range(n_days):
                h += rng.uniform(14, 19)
                cleaned = h > 120
                if cleaned:
                    h = rng.uniform(0, 6)
                rows.append([ch, (P.START + dt.timedelta(days=d0)).isoformat(), round(h, 1), "Y" if cleaned else ""])
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["chamber_id", "date", "rf_hours_since_clean", "clean_done"])
            wr.writerows(rows)
        return len(rows)

    # ---- hourly particle counts by bay
    def particles(self, path):
        rng = self.rng
        rows = []
        n_h = (WD.day(P.LAST_POLISH) + 1) * 24
        pw0, pw1 = WD.day(P.PARTICLE_WEEK[0]) * 24, (WD.day(P.PARTICLE_WEEK[1]) + 1) * 24
        for bay in ["B1", "B2", "B3", "B4"]:
            base = float(rng.uniform(40, 70))
            for h in range(n_h):
                lam = base * (1 + 0.15 * math.sin(2 * math.pi * (h % 24) / 24)) * (3.2 if pw0 <= h < pw1 else 1.0)
                if rng.random() < 0.003:
                    continue
                rows.append([bay, ts(h / 24.0, "%Y-%m-%d %H:00"), int(rng.poisson(lam)), int(rng.poisson(lam * 0.18))])
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["bay", "hour", "count_0p3um", "count_1p0um"])
            wr.writerows(rows)
        return len(rows)

    def sc4(self, path):
        rng = self.rng
        rows = []
        for lot in self.fab.lots:
            if lot["tools"]["M1-LITHO"] != "SC-4":
                continue
            for field in range(1, 9):
                rows.append([lot["lot_id"], field, round(rng.normal(0, 18), 1), round(rng.normal(0, 22), 1)])
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["lot_id", "edge_field", "focus_offset_nm", "leveling_residual_nm"])
            wr.writerows(rows)
        return len(rows)

    def slurry(self, path):
        rng = self.rng
        rows = []
        d = P.START - dt.timedelta(days=20)
        k = 0
        while d <= P.LAST_POLISH:
            k += 1
            rows.append(["SL%05d" % (31200 + k), d.isoformat(), round(rng.normal(12.0, 0.15), 2), round(rng.normal(145, 6)),
                         round(rng.normal(10.9, 0.08), 2), round(rng.normal(0.9, 0.2), 2)])
            d += dt.timedelta(days=int(rng.integers(5, 9)))
        with open(path, "w", newline="") as fh:
            wr = csv.writer(fh)
            wr.writerow(["slurry_lot", "received", "solids_pct", "mean_particle_nm", "ph", "large_particle_ppm"])
            wr.writerows(rows)
        return len(rows)


def write(fab, tgt):
    pk = Pack(fab)
    return pk.write(tgt), pk
