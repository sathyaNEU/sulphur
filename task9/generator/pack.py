"""task9 (architecture 3): the pack. Each file is written the way the fab's own system writes it, from the simulated
process in world.py: the yield database the sort floor fills, the MES lot history, each tool's own export in its own
layout and clock, the metrology and inspection systems' sampling, the facilities controller's exception-reported trend,
the bench controller's event log, the lab's results, the engineering paperwork. Mess is what those systems and people
produce; nothing is placed where it decides a result."""
import csv
import datetime as dt
import io
import json
import math
import os
import sqlite3

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import params as P
import postprocess as PP
import world as W

F = {
    "sort": "fab2_yield.sqlite",
    "mes": "mes_lot_history.csv",
    "gen": "lot_genealogy.csv",
    "cm1": "CM1_ild0_polish.csv", "cm2": "CM2_ild0_polish.csv", "cm3": "CM3_ild0_polish.csv", "cm4": "CM4_ild0_polish.csv",
    "dep": "ild0_dep_wafer_log.csv",
    "etch": "ct_etch_fdc_summary.csv",
    "mon": "etch_chamber_monitors.csv",
    "thk": "ild0_thickness_49pt.csv",
    "spc": "spc_ild0_thickness.csv",
    "insp": "inline_defect_scans.csv",
    "wat": "wat_parametric.csv",
    "pm": "equipment_pm_log.xlsx",
    "rcp": "recipe_change_log.csv",
    "sds": "sds_ox1_trend_export.csv",
    "lines": "facility_line_list.xlsx",
    "fac": "facilities_change_log.xlsx",
    "bench": "pgc_bench_controller.jsonl",
    "lab": "lab_bath_metals_2026.xlsx",
    "ecn": "ecn_register_2026.xlsx",
    "prod": "product_data_sheet.xlsx",
    "plan": "vr90_ramp_plan_q1_2027.pdf",
    "cost": "cost_inputs_2027.yaml",
    "notes": "shift_handover_ft2_2026.txt",
    "env": "cleanroom_bay_environment.csv",
    "probe": "probe_card_touchdowns.csv",
    "ovl": "scanner_overlay_lots.csv",
}
DISTRACTORS = [F["env"], F["probe"], F["ovl"]]
BINCHAR = {1: "1", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6", 8: "8", 9: "9", 11: "B"}


PULL_D = None


def cycle_offsets(rng, n, base, cv, p_pause, pause):
    """start offsets (days) of n wafers run one after another on a tool, as its own log stamps them: each cycle varies a
    little and now and then the tool waits (an endpoint retry, a conditioner check, a load port)"""
    out, t = [], 0.0
    for k in range(n):
        out.append(t)
        t += base * max(0.6, 1 + rng.normal(0, cv)) + (rng.uniform(*pause) if rng.random() < p_pause else 0.0)
    return out


def pulled(d):
    """True when an event at d (days) happened before the yield team's pull: the extracts hold nothing later."""
    global PULL_D
    if PULL_D is None:
        PULL_D = W.tday(P.PULL)
    return d < PULL_D


def ts(d, fmt="%Y-%m-%d %H:%M:%S", shift_min=0.0):
    t = W.dtime(d) + dt.timedelta(minutes=shift_min)
    return t.strftime(fmt)


def old_id(lid, d):
    """lot IDs carried a dot after the product prefix until the MES upgrade"""
    return lid[:3] + "." + lid[3:] if W.dtime(d) < P.T_MES_UPGRADE else lid


def utc(d):
    """the local wall time as UTC (Europe/Berlin: +1 in winter, +2 in summer)"""
    from zoneinfo import ZoneInfo
    t = W.dtime(d).replace(tzinfo=ZoneInfo(P.TZ)).astimezone(dt.timezone.utc)
    return t.strftime("%Y-%m-%dT%H:%M:%S.") + "%03dZ" % int((d * 86400 * 1000) % 1000)


def write_csv(path, header, rows, delimiter=",", lineterminator="\r\n"):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh, delimiter=delimiter, lineterminator=lineterminator)
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def save_xlsx(wb, path, creator, last_by, created, modified):
    wb.save(path)
    PP.normalize_ooxml(path, creator, last_by, created, modified, excel=True, company=P.FIRM)


def head(ws, cols, widths=None):
    ws.append(cols)
    for c in ws[1]:
        c.font = Font(bold=True)
    if widths:
        for i, wdt in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wdt


class Pack:
    def __init__(self, fab):
        self.fab = fab
        self.rng = np.random.default_rng(P.SEED + 77)
        self.info = {}
        self.events = []      # what the floor saw happen, for the shift book
        self.trng = np.random.default_rng(P.SEED + 4343)     # the tools' own cycle times in their logs

    # ------------------------------------------------------------------ the yield database
    def sort_db(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 101)
        if os.path.exists(path):
            os.remove(path)
        con = sqlite3.connect(path)
        cur = con.cursor()
        cur.executescript("""
        CREATE TABLE product (product TEXT PRIMARY KEY, die_w_mm REAL, die_h_mm REAL, map_cols INTEGER, map_rows INTEGER,
            col0_x_mm REAL, row0_y_mm REAL, gross_die INTEGER, test_program TEXT);
        CREATE TABLE test_program (program TEXT, revision TEXT, product TEXT, released TEXT, note TEXT);
        CREATE TABLE bin_def (bin INTEGER PRIMARY KEY, bin_name TEXT, test_block TEXT, flow_order INTEGER, good INTEGER);
        CREATE TABLE sort_wafer (wafer_key TEXT, lot_id TEXT, wafer_no INTEGER, product TEXT, program TEXT,
            insertion INTEGER, prober TEXT, probe_card TEXT, start_time TEXT, end_time TEXT, tested INTEGER, good INTEGER,
            PRIMARY KEY (wafer_key, insertion));
        CREATE TABLE sort_bin_count (wafer_key TEXT, insertion INTEGER, bin INTEGER, die INTEGER);
        CREATE TABLE sort_map (wafer_key TEXT, insertion INTEGER, map_text TEXT);
        """)
        for name, g in fab.grids.items():
            if name == "VR90":
                continue
            cur.execute("INSERT INTO product VALUES (?,?,?,?,?,?,?,?,?)",
                        (name, g.w, g.h, g.ncol, g.nrow, round(float(g.colmin_x), 3), round(float(g.rowmin_y), 3), g.n,
                         {"VX40": "VX40-S", "VP12": "VP12-S"}[name]))
        cur.executemany("INSERT INTO test_program VALUES (?,?,?,?,?)", [
            ("VX40-S", "r14", "VX40", "2025-09-29", "production sort, 125 C"),
            ("VX40-S", "r15", "VX40", "2026-02-16", "retention pattern update, test time -3 %"),
            ("VP12-S", "r9", "VP12", "2025-08-11", "production sort, 25 C"),
            ("VP12-S", "r10", "VP12", "2026-05-04", "trim limits tightened per customer PCN 26-07"),
        ])
        cur.executemany("INSERT INTO bin_def VALUES (?,?,?,?,?)", [
            (1, "PASS", "-", 99, 1), (2, "PROBE_CONTACT", "contact check", 0, 0), (3, "CONT_OPEN_HIGH_RC", "continuity", 1, 0),
            (4, "GATE_CONTACT_SHORT", "shorts", 2, 0), (5, "METAL_SHORT_COMB", "shorts", 3, 0), (6, "IDDQ_LEAK", "iddq", 4, 0),
            (8, "FUNC_SCAN_BIST", "functional", 5, 0), (9, "PARAM_SPEED_VT", "parametric", 6, 0),
            (11, "NVM_RETENTION", "retention", 7, 0)])
        # program revision by sort date
        def program_rev(product, d):
            t = W.dtime(d)
            if product == "VX40":
                return "VX40-S"
            return "VP12-S"
        cards = {"PR-1": "PC-VX-07", "PR-2": "PC-VX-11", "PR-3": "PC-VP-04", "PR-4": "PC-VP-09"}
        probers = {"VX40": ["PR-1", "PR-2"], "VP12": ["PR-3", "PR-4"]}
        test_min = {"VX40": 65.0, "VP12": 43.0}          # minutes a wafer on the tester
        # every wafer's draws first, in the record's order: its test time, and whether part of it needs a re-probe
        plan = []
        for w in fab.sorted:
            g = fab.grids[w["product"]]
            rng.integers(0, 2)                           # (the prober is the lot's, chosen below)
            dur = test_min[w["product"]] / 1440.0 * rng.uniform(0.95, 1.08)
            bins1 = None
            if rng.random() < 0.04:
                # a probe-card contact problem on part of the wafer: re-probed after a card clean
                bins1 = w["bins"].copy()
                ang = np.arctan2(g.yc, g.xc)
                a0 = rng.uniform(-np.pi, np.pi)
                sector = (np.abs(((ang - a0 + np.pi) % (2 * np.pi)) - np.pi) < rng.uniform(0.3, 0.9))
                hit = sector & (rng.random(g.n) < 0.85)
                bins1[hit] = 2
                rng.uniform(0.08, 0.35)
            plan.append((w, dur, bins1))
        # each lot goes to the first free prober of its pair and its wafers run one after another; the wafers that
        # need it are re-probed at the end of the lot, after the card clean
        srng = np.random.default_rng(P.SEED + 131)
        free = {p: -1e9 for v in probers.values() for p in v}
        by_lot = {}
        for item in plan:
            by_lot.setdefault(item[0]["lid"], []).append(item)
        sched, lot_prober = {}, {}
        for lid in sorted(by_lot, key=lambda x: (min(it[0]["d"] for it in by_lot[x]), x)):
            items = sorted(by_lot[lid], key=lambda it: it[0]["slot"])
            prod = items[0][0]["product"]
            arrive = min(it[0]["d"] for it in items)
            pr = min(probers[prod], key=lambda p: (max(free[p], arrive), p))
            lot_prober[lid] = pr
            t = max(free[pr], arrive) + srng.uniform(0.004, 0.02)          # load, align and first touchdown
            for w, dur, bins1 in items:
                sched[(lid, w["slot"])] = [(1, t, dur, w["bins"] if bins1 is None else bins1)]
                t += dur + srng.uniform(0.0007, 0.0021)
            redo = [(w, dur) for w, dur, bins1 in items if bins1 is not None]
            if redo:
                t += srng.uniform(0.007, 0.017)                            # card clean
                for w, dur in redo:
                    d2 = dur * srng.uniform(0.97, 1.03)
                    sched[(lid, w["slot"])].append((2, t, d2, w["bins"]))
                    t += d2 + srng.uniform(0.0007, 0.0021)
            free[pr] = t
        n_wafers = n_ins = 0
        for w, dur, bins1 in plan:
            g = fab.grids[w["product"]]
            key = "%s-%02d" % (w["lid"], w["slot"])
            prober = lot_prober[w["lid"]]
            inserts = [x for x in sched[(w["lid"], w["slot"])] if pulled(x[1] + x[2])]
            if not inserts:
                continue
            for ins, d0, du, bins in inserts:
                good = int((bins == 1).sum())
                cur.execute("INSERT INTO sort_wafer VALUES (?,?,?,?,?,?,?,?,?,?,?,?)",
                            (key, w["lid"], w["slot"], w["product"], program_rev(w["product"], d0), ins, prober,
                             cards[prober], ts(d0), ts(d0 + du), g.n, good))
                vals, cnts = np.unique(bins, return_counts=True)
                cur.executemany("INSERT INTO sort_bin_count VALUES (?,?,?,?)",
                                [(key, ins, int(v), int(c)) for v, c in zip(vals, cnts)])
                grid = np.full((g.nrow, g.ncol), ".", dtype="<U1")
                chars = np.array([BINCHAR[int(b)] for b in bins])
                grid[g.row, g.col] = chars
                text = "\n".join("".join(grid[r]) for r in range(g.nrow - 1, -1, -1))
                cur.execute("INSERT INTO sort_map VALUES (?,?,?)", (key, ins, text))
                n_ins += 1
            if len(inserts) == 2:
                self.events.append({"t": W.dtime(inserts[1][1]), "kind": "reprobe", "tool": prober, "card": cards[prober],
                                    "lot": old_id(w["lid"], inserts[1][1]), "slot": w["slot"]})
            n_wafers += 1
        cur.execute("CREATE INDEX ix_sw_lot ON sort_wafer (lot_id)")
        con.commit()
        con.execute("VACUUM")
        con.close()
        self.info["sort_wafers"], self.info["sort_insertions"] = n_wafers, n_ins

    # ------------------------------------------------------------------ MES
    def mes(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 102)
        rows = []
        hold_codes = ["ENG-HOLD", "TOOL-DOWN", "QA-REVIEW", "METRO-OOC", "CUST-HOLD"]
        for L in fab.lots:
            qty = L.n
            steps = list(L.times.items())
            for i, (step, d) in enumerate(steps):
                grp = W.ROUTE[W.STEP_IDX[step]][1]
                tool = L.tools.get(step, "-")
                if grp not in ("WB", "DP", "CM", "ET") and grp != "MES":
                    tool = W.TOOLS[grp][int(rng.integers(0, len(W.TOOLS[grp])))]
                proc = {"WB": 0.045, "DP": 0.09, "CM": 0.11, "ET": 0.10, "MES": 0.0, "PRB": 0.0}.get(grp, 0.06)
                t_in = d
                t_out = d + proc * rng.uniform(0.8, 1.3) if proc else d
                hold, hh = "", ""
                for hs, h in L.hold:
                    if hs == step:
                        hold, hh = hold_codes[int(rng.integers(0, len(hold_codes)))], "%.1f" % h
                q_in = qty
                for s, at in L.scrap.items():
                    if at == step:
                        qty -= 1
                route = P.PRODUCTS.get(L.product, P.PRODUCTS["VR90"])["route"] if not L.tv else "VR90T-R2"
                rows.append([old_id(L.lid, t_in), L.product, route, (i + 1) * 10, step, tool,
                             ts(t_in), ts(t_out) if proc else "", q_in, qty, hold, hh])
                if hold:
                    self.events.append({"t": W.dtime(t_in), "kind": "hold", "lot": old_id(L.lid, t_in), "product": L.product,
                                        "step": step, "code": hold, "hours": float(hh)})
                if L.tv and step == "M1-ETCH":
                    rows.append([old_id(L.lid, t_out + 0.6), L.product, route, (i + 2) * 10, "SHIP-DESIGN-CTR", "-",
                                 ts(t_out + 0.6), "", qty, qty, "", ""])
        # a handful of track-in rows the floor reversed and re-entered (the MES keeps both)
        extra = []
        for r in rows:
            if r[4] in ("POLY-LITHO", "M1-LITHO", "V2-M3") and rng.random() < 0.02:
                rr = list(r)
                rr[11] = ""
                rr[10] = "TRACKIN-REVERSED"
                extra.append(rr)
        rows += extra
        cut = W.dtime(W.tday(P.PULL)).strftime("%Y-%m-%d %H:%M:%S")
        rows = [r for r in rows if r[6] < cut]
        for r in rows:
            if r[7] and r[7] >= cut:
                r[7] = ""
        rows.sort(key=lambda r: (r[6], r[0], r[3]))
        self.info["mes_rows"] = write_csv(path, ["LOT_ID", "PRODUCT", "ROUTE", "STEP_NO", "STEP", "EQP_ID", "TRACK_IN",
                                                 "TRACK_OUT", "QTY_IN", "QTY_OUT", "HOLD_CODE", "HOLD_HRS"], rows)

    def genealogy(self, path):
        rng = np.random.default_rng(P.SEED + 103)
        rows = []
        for L in self.fab.lots:
            if L.tv or rng.random() > 0.06:
                continue
            step = ["POLY-LITHO", "M1-LITHO", "V2-M3", "PAD-ETCH"][int(rng.integers(0, 4))]
            d = L.times[step]
            n = int(rng.integers(2, 7))
            child = L.lid + "A"
            rows.append([ts(d - 0.02), old_id(L.lid, d), old_id(child, d), "SPLIT", n, step, "rework split"])
            rows.append([ts(d + rng.uniform(0.6, 2.0)), old_id(child, d), old_id(L.lid, d), "MERGE", n, step, "rework complete"])
        rows.sort()
        self.info["gen_rows"] = write_csv(path, ["EVENT_TIME", "FROM_LOT", "TO_LOT", "ACTION", "WAFERS", "AT_STEP", "COMMENT"], rows)

    # ------------------------------------------------------------------ the polishers' own exports
    def cmp_exports(self, tgt):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 104)
        by_tool = {t: [] for t in P.CMP_TOOLS}
        for L in fab.lots:
            if "ILD0-CMP" not in L.times:
                continue
            tool = L.tools["ILD0-CMP"]
            pol = P.PRODUCTS["VR90"]["polish_s"] if L.tv else P.PRODUCTS[L.product]["polish_s"]
            recipe = {"VX40": "ILD0-VX", "VP12": "ILD0-VP", "VR90-T": "ILD0-VR"}[L.product]
            rev = 8 if (tool == "CM3" and L.times["ILD0-CMP"] >= W.tday(P.T_CM3_TUNE)) else 7
            offs = cycle_offsets(self.trng, len(L.slots), 0.0035, 0.03, 0.03, (0.002, 0.006))
            for k, slot in enumerate(L.slots):
                if slot in L.scrap and L.scrap[slot] in ("STI-CMP", "POLY-ETCH"):
                    continue
                d = L.times["ILD0-CMP"] + offs[k]
                p1 = pol * rng.normal(1, 0.035)
                by_tool[tool].append(dict(d=d, lid=L.lid, slot=slot, recipe=recipe, rev=rev, head=int(k % 4) + 1,
                                          p1=p1, p2=28.0 * rng.normal(1, 0.03), p3=19.0 * rng.normal(1, 0.03),
                                          epd="OK" if rng.random() > 0.004 else "TIMEOUT"))
        n = 0
        for tool, rows in by_tool.items():
            rows.sort(key=lambda r: r["d"])
            if tool == "CM1":   # its controller clock runs four minutes fast
                out = [[old_id(r["lid"], r["d"]), r["slot"], "%s_R%d" % (r["recipe"], r["rev"]), ts(r["d"], shift_min=4.1),
                        r["head"], "%.1f" % r["p1"], "%.1f" % r["p2"], "%.1f" % r["p3"], r["epd"]] for r in rows]
                n += write_csv(os.path.join(tgt, F["cm1"]), ["LotID", "Slot", "Recipe", "StartTime", "Head", "P1_sec", "P2_sec",
                                                            "P3_sec", "EPD"], out)
            elif tool == "CM3":   # German locale export
                out = [[old_id(r["lid"], r["d"]), "%02d" % r["slot"], r["recipe"], "R%d" % r["rev"],
                        ts(r["d"], "%d.%m.%Y %H:%M:%S"), r["head"], ("%.1f" % r["p1"]).replace(".", ","),
                        ("%.1f" % r["p2"]).replace(".", ","), ("%.1f" % r["p3"]).replace(".", ","), r["epd"]] for r in rows]
                n += write_csv(os.path.join(tgt, F["cm3"]), ["Los", "Scheibe", "Rezept", "Rev", "Startzeit", "Kopf", "P1_s",
                                                            "P2_s", "P3_s", "Endpunkt"], out, delimiter=";")
            else:
                out = [[old_id(r["lid"], r["d"]), "%s-%02d" % (r["lid"], r["slot"]), "%s_R%d" % (r["recipe"], r["rev"]),
                        ts(r["d"]), r["head"], "%.2f" % r["p1"], "%.2f" % r["p2"], "%.2f" % r["p3"],
                        "1" if r["epd"] == "OK" else "0"] for r in rows]
                n += write_csv(os.path.join(tgt, F[tool.lower()]), ["lot_id", "wafer_id", "recipe_name", "start_ts",
                                                                   "carrier_head", "platen1_s", "platen2_s", "platen3_s",
                                                                   "endpoint_ok"], out)
        self.info["cmp_rows"] = n

    def dep_log(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 105)
        rows = []
        for L in fab.lots:
            if "ILD0-DEP" not in L.times:
                continue
            tool = L.tools["ILD0-DEP"]
            d0 = L.times["ILD0-DEP"]
            pairs = cycle_offsets(self.trng, (len(L.slots) + 1) // 2, 0.0042, 0.03, 0.03, (0.002, 0.008))
            for k, slot in enumerate(L.slots):
                if slot in L.scrap and L.scrap[slot] in ("STI-CMP", "POLY-ETCH"):
                    continue
                e = fab.edge_of.get((L.lid, slot))
                ch = e["ch"] if e else tool + ("A" if slot % 2 else "B")
                d = d0 + pairs[k // 2] + (0.0005 * float(self.trng.uniform(0.6, 1.6)) if ch.endswith("B") else 0)
                rows.append([tool, ch[-1], old_id(L.lid, d), slot, "PMD-USG-605", ts(d), "%.1f" % (148.0 * rng.normal(1, 0.01)),
                             "%.0f" % (rng.normal(1180, 6)), 605])
        rows.sort(key=lambda r: (r[5], r[0], r[1]))
        self.info["dep_rows"] = write_csv(path, ["TOOL", "CHAMBER", "LOT", "WAFER", "RECIPE", "START", "DEP_TIME_S",
                                                 "RF_W", "TARGET_NM"], rows)

    def etch_fdc(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 106)
        rows = []
        for ch, lst in fab.etch_wafers.items():
            ds = [r["d"] for r in lst]
            for i, r in enumerate(lst):
                pw = 1650.0 if r["rec"] == "CT-DEEP-07" else 1420.0
                ep = r["rf"] * rng.uniform(0.86, 0.90)
                gap = (ds[i + 1] - ds[i]) if i + 1 < len(ds) else 0.01
                d_log = r["d"] + float(self.trng.uniform(0.0, min(25.0 / 86400.0, 0.4 * max(gap, 0.0))))
                rows.append([ch[:3], ch[3], old_id(r["lid"], r["d"]), r["slot"], r["rec"], ts(d_log), "%.1f" % r["rf"],
                             "%.0f" % (pw * rng.normal(1, 0.004)), "%.2f" % rng.normal(38.0, 0.3), "%.1f" % ep,
                             r["count"], "%.2f" % r["rfh"]])
        rows.sort(key=lambda r: (r[5], r[0], r[1]))
        # a network outage left a gap in the export in early July (the tools buffered nothing)
        lo, hi = W.tday(dt.datetime(2026, 7, 6, 22)), W.tday(dt.datetime(2026, 7, 7, 9))
        rows = [r for r in rows if not (lo <= W.tday(dt.datetime.strptime(r[5], "%Y-%m-%d %H:%M:%S")) < hi)]
        self.info["etch_rows"] = write_csv(path, ["TOOL", "CHAMBER", "LOT_ID", "SLOT", "RECIPE", "WAFER_START", "RF_ON_S",
                                                  "RF_FWD_W", "PRESS_MTORR", "EP_TIME_S", "CH_WAFERS_SINCE_WC",
                                                  "CH_RF_HOURS_SINCE_WC"], rows)

    def monitors(self, path):
        fab = self.fab
        rows = [[m["ch"][:3], m["ch"][3], ts(m["d"]), "PM-BARE-MON", m["adders"], "0.12", m["count"]] for m in fab.monitors
                if W.dtime(m["d"]) >= dt.datetime(2025, 12, 1)]
        rows.sort(key=lambda r: (r[2], r[0], r[1]))
        self.info["mon_rows"] = write_csv(path, ["tool", "chamber", "measured", "monitor_type", "adders", "size_um",
                                                 "wafer_counter"], rows)

    # ------------------------------------------------------------------ metrology and inspection
    SITES = [(0.0, 0.0)] + [(50.0, a) for a in range(0, 360, 45)] + [(100.0, a) for a in range(0, 360, 22)][:16] + \
            [(145.0, a) for a in np.arange(0, 360, 15)]

    def thickness(self, path_raw, path_spc):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 107)
        sites = [(r, (a if isinstance(a, (int, float)) else float(a))) for r, a in self.SITES][:49]
        prof = lambda r: np.clip((r - P.EDGE_R0) / (P.WAFER_R - P.EDGE_EXCL - P.EDGE_R0), 0, 1) ** P.EDGE_POW
        raw, spc = [], []
        for L in fab.lots:
            if "ILD0-CMP" not in L.times:
                continue
            for step, slots in (("ILD0-DEP", (3,)), ("ILD0-CMP", (3, 18))):
                for slot in slots:
                    key = (L.lid, slot)
                    if key not in fab.edge_of:
                        continue
                    e = fab.edge_of[key]
                    d = L.times[step] + 0.05 + rng.uniform(0, 0.08)
                    tool = ("TH-1", "TH-2")[int(rng.integers(0, 2))]
                    wn = rng.normal(0, 3.0)
                    vals = []
                    for i, (r, a) in enumerate(sites):
                        x, y = r * math.cos(math.radians(a)), r * math.sin(math.radians(a))
                        if step == "ILD0-DEP":
                            t = P.ILD_NOM + wn + e["dep"] * prof(r) - 2.0 * (r / 147.0) ** 2 + rng.normal(0, 1.4)
                        else:
                            t = (P.ILD_NOM - P.REMOVE_NOM) + wn + (e["dep"] - e["rem"] + e["noise"]) * prof(r) \
                                + 3.0 * (r / 147.0) ** 2 + rng.normal(0, 1.6)
                        gof = rng.uniform(0.985, 0.999)
                        vals.append(t)
                        raw.append([old_id(L.lid, d), slot, step, tool, ts(d), i + 1, "%.1f" % x, "%.1f" % y, "%.1f" % t,
                                    "%.3f" % gof])
                    five = [vals[0]] + vals[1:9:2]
                    spc.append([old_id(L.lid, d), L.product, step, tool, ts(d), slot, "%.1f" % np.mean(five),
                                "%.1f" % (max(five) - min(five)), {"ILD0-DEP": "605 +/- 18", "ILD0-CMP": "305 +/- 20"}[step]])
        self.info["thk_rows"] = write_csv(path_raw, ["lot", "wafer", "step", "tool", "measured", "site", "x_mm", "y_mm",
                                                     "thk_nm", "gof"], raw)
        self.info["spc_rows"] = write_csv(path_spc, ["LOT", "PRODUCT", "STEP", "TOOL", "MEAS_TIME", "WAFER", "MEAN5_NM",
                                                     "RANGE5_NM", "SPEC"], spc)

    def inspection(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 108)
        rows = []
        ns_of = {(w["lid"], w["slot"]): w["ns"] for w in fab.sorted}
        for L in fab.lots:
            if "ILD0-CMP" not in L.times:
                continue
            for slot in (7, 19):
                key = (L.lid, slot)
                if key not in fab.scr_lam:
                    continue
                ns = ns_of.get(key, int(rng.poisson(fab.scr_lam[key])))
                scr = int(rng.binomial(ns, 0.74))
                prt = int(rng.poisson(9.0))
                res = int(rng.poisson(2.5))
                pit = int(rng.poisson(1.2))
                oth = int(rng.poisson(3.0))
                d = L.times["ILD0-CMP"] + 0.12 + rng.uniform(0, 0.1)
                rows.append([old_id(L.lid, d), slot, "ILD0-CMP", ("KL-2", "KL-3")[int(rng.integers(0, 2))], ts(d),
                             scr + prt + res + pit + oth, scr, prt, res, pit, oth])
            if "CT-ETCH" in L.times:
                slot = 12
                key = (L.lid, slot)
                if key in fab.etch_of:
                    lam = fab.etch_of[key]["lam"]
                    prt = int(rng.poisson(lam * 0.62 + 2.0))
                    d = L.times["CT-ETCH"] + 0.08 + rng.uniform(0, 0.1)
                    rows.append([old_id(L.lid, d), slot, "CT-ETCH", "KL-4", ts(d), prt + int(rng.poisson(4)), 0, prt,
                                 int(rng.poisson(2)), 0, int(rng.poisson(2))])
        rows.sort(key=lambda r: (r[4], r[0]))
        self.info["insp_rows"] = write_csv(path, ["LOT_ID", "WAFER", "LAYER", "INSP_TOOL", "SCAN_TIME", "TOTAL",
                                                  "CLS_SCRATCH", "CLS_PARTICLE", "CLS_RESIDUE", "CLS_PIT", "CLS_OTHER"], rows)

    def wat(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 109)
        prof = lambda r: np.clip((r - P.EDGE_R0) / (P.WAFER_R - P.EDGE_EXCL - P.EDGE_R0), 0, 1) ** P.EDGE_POW
        sites = [(0, 0)] + [(70, a) for a in (0, 90, 180, 270)] + [(135, a) for a in (45, 135, 225, 315)]
        rows = []
        for L in fab.lots:
            if L.tv or "WAT" not in L.times:
                continue
            c = fab.bath_at.get(L.lid, P.C_FRESH)
            for slot in (4, 11, 20):
                key = (L.lid, slot)
                if key not in fab.edge_of or slot in L.scrap:
                    continue
                e = fab.edge_of[key]
                d = L.times["WAT"] + rng.uniform(0, 0.05)
                for i, (r, a) in enumerate(sites):
                    net = e["net"] * prof(r)
                    jg = 10 ** (-9.15 + 0.30 * c + rng.normal(0, 0.07))
                    rc = 41.0 + max(0.0, net - 2.0) * 0.55 + rng.normal(0, 0.9)
                    vtn = 0.412 + rng.normal(0, 0.006)
                    vtp = -0.448 + rng.normal(0, 0.007)
                    rs = 7.85 + rng.normal(0, 0.09)
                    rows.append([L.lid, slot, L.product, ts(d), i + 1, r, a, "%.3e" % jg, "%.2f" % rc, "%.4f" % vtn,
                                 "%.4f" % vtp, "%.3f" % rs])
        cut = W.dtime(W.tday(P.PULL)).strftime("%Y-%m-%d %H:%M:%S")
        rows = [r for r in rows if r[3] < cut]
        self.info["wat_rows"] = write_csv(path, ["lot_id", "wafer", "product", "test_time", "site", "site_r_mm", "site_deg",
                                                 "JG_A_CM2", "RC_CT_OHM", "VTN_V", "VTP_V", "RS_POLY_OHMSQ"], rows)

    # ------------------------------------------------------------------ maintenance and recipes
    def pm_log(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 110)
        rows = []
        tech = lambda: P.TECHS[int(rng.integers(0, len(P.TECHS)))]
        lo = W.tday(dt.datetime(2025, 11, 1))
        for tool in P.CMP_TOOLS:
            for d in fab.pou[tool]:
                if d < lo:
                    continue
                rows.append(["CMP", tool, ts(d + rng.uniform(0, 0.02), "%Y-%m-%d %H:%M"), "POU_FILTER",
                             str(rng.choice(["POU filter changed (Planar 0.5 um)", "POU filter swap 0.5um", "slurry POU filter replaced"])),
                             "", tech()])
            d = lo + rng.uniform(1, 9)
            while d < W.tday(P.SORT_TO):
                rows.append(["CMP", tool, ts(d, "%Y-%m-%d %H:%M"), "PAD_CHANGE", "P1 pad IC1010 + conditioner check", "", tech()])
                d += rng.uniform(9.5, 12.5)
            d = lo + rng.uniform(5, 30)
            while d < W.tday(P.SORT_TO):
                rows.append(["CMP", tool, ts(d, "%Y-%m-%d %H:%M"), "RING_CHANGE", "retaining ring RR-300 head %d" % rng.integers(1, 5), "", tech()])
                d += rng.uniform(30, 45)
        for ch in P.DEP_CHAMBERS:
            d = lo + rng.uniform(1, 12)
            while d < W.tday(P.SORT_TO):
                rows.append(["CVD", ch[:3], ts(d, "%Y-%m-%d %H:%M"), "CHAMBER_CLEAN", "chamber %s NF3 clean + season" % ch[3], "", tech()])
                d += rng.uniform(11, 16)
        d_sh = W.tday(P.T_SHOWERHEAD)
        rows.append(["CVD", "DP2", ts(d_sh, "%Y-%m-%d %H:%M"), "PART_REPLACE",
                     "chamber B showerhead SH-300-B removed (faceplate erosion), SH-300-C installed per ECN-2026-0388; "
                     "season 25 dummy, particle check pass", "", "R. Heuser"])
        for ch, cl in fab.etch_cleans.items():
            for c in cl:
                back = rng.random() < 0.05
                rows.append(["ETCH", ch[:3], ts(c["d"] + (rng.uniform(0.6, 1.2) if back else 0), "%Y-%m-%d %H:%M"), "WET_CLEAN",
                             "chamber %s wet clean, liner and edge ring swap" % ch[3],
                             "" if rng.random() < 0.04 else c["count"], tech()] + (["back-entered"] if back else []))
        for b in P.BENCHES:
            d = lo + rng.uniform(2, 20)
            while d < W.tday(P.SORT_TO):
                rows.append(["WET", b, ts(d, "%Y-%m-%d %H:%M"), "PM_MONTHLY", "recirc pump seal check, T3 heater cal, filter 0.05um", "", tech()])
                d += rng.uniform(26, 33)
        for tool, wins in fab.down.items():
            for a, b2, _ in wins:
                if a < lo:
                    continue
                rows.append([{"WB": "WET", "DP": "CVD", "CM": "CMP", "ET": "ETCH"}[tool[:2] if tool[:2] in ("WB", "DP") else
                             ("CM" if tool.startswith("CM") else "ET")], tool, ts(a, "%Y-%m-%d %H:%M"), "UNSCHED_DOWN",
                             str(rng.choice(["robot handoff fault", "chamber pressure alarm", "wafer slip detected", "door interlock",
                                             "RF match fault", "load port error", "exhaust low alarm"])) + ", up after %.1f h" % ((b2 - a) * 24),
                             "", tech()])
        rows.sort(key=lambda r: (r[2], r[0], r[1]))
        for r in rows:
            self.events.append({"t": dt.datetime.strptime(r[2], "%Y-%m-%d %H:%M"), "kind": "pm", "area": r[0], "tool": r[1],
                                "type": r[3], "desc": r[4]})
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "PM log"
        head(ws, ["area", "equipment", "event_time", "event_type", "description", "counter", "technician", "entry_note"],
             [7, 10, 17, 15, 86, 9, 13, 13])
        for r in rows:
            ws.append(r + [""] * (8 - len(r)))
        save_xlsx(wb, path, P.PEOPLE["maint"], P.PEOPLE["maint"], "2025-12-29T07:41:00Z", "2026-11-05T15:12:44Z")
        self.info["pm_rows"] = len(rows)

    def recipes(self, path):
        rows = [
            ["2026-01-19 10:42", "CM1", "ILD0-VX", "R6", "R7", "endpoint threshold", "0.92", "0.90", "M. Hertrampf", "endpoint margin after pad lot change"],
            ["2026-01-19 10:55", "CM2", "ILD0-VX", "R6", "R7", "endpoint threshold", "0.92", "0.90", "M. Hertrampf", "same change as CM1"],
            ["2026-01-19 11:03", "CM3", "ILD0-VX", "R6", "R7", "endpoint threshold", "0.92", "0.90", "M. Hertrampf", "fleet set"],
            ["2026-01-19 11:10", "CM4", "ILD0-VX", "R6", "R7", "endpoint threshold", "0.92", "0.90", "M. Hertrampf", "as CM1"],
            ["2026-02-23 14:20", "DP1", "PMD-USG-605", "R3", "R4", "dep time", "150.0 s", "148.0 s", "A. Dörr", "rate drift after RF generator swap"],
            ["2026-02-23 14:31", "DP2", "PMD-USG-605", "R3", "R4", "dep time", "150.0 s", "148.0 s", "A. Dörr", "matched to DP1 after rate check"],
            ["2026-02-23 14:38", "DP3", "PMD-USG-605", "R3", "R4", "dep time", "150.0 s", "148.0 s", "A. Dörr", "keep DP fleet on one rev"],
            ["2026-03-30 09:12", "ET2", "CT-STD-11", "R11", "R12", "O2 flash step", "4 s", "5 s", "D. Lindau", "residue on CT bottom, VX40"],
            ["2026-04-14 16:02", "CM2", "ILD0-VP", "R7", "R7.1", "P2 time", "29 s", "28 s", "M. Hertrampf", "throughput"],
            ["2026-05-11 09:05", "CM3", "ILD0-VX", "R7", "R8", "zone 5 pressure", "2.90 psi", "3.15 psi", "M. Hertrampf", "uniformity tune after 49-pt review"],
            ["2026-05-11 09:11", "CM3", "ILD0-VP", "R7", "R8", "zone 5 pressure", "2.90 psi", "3.15 psi", "M. Hertrampf", "uniformity tune after 49-pt review"],
            ["2026-05-11 09:15", "CM3", "ILD0-VR", "R7", "R8", "zone 5 pressure", "2.90 psi", "3.15 psi", "M. Hertrampf", "uniformity tune after 49-pt review"],
            ["2026-06-15 13:40", "ET1", "CT-DEEP-07", "R2", "R3", "C4F8 flow", "18 sccm", "18 sccm", "D. Lindau", "no change, step timing only"],
            ["2026-07-27 08:50", "CM4", "ILD0-VX", "R7", "R7.1", "conditioner sweep", "11 zones", "12 zones", "M. Hertrampf", "pad life"],
            ["2026-09-08 10:30", "DP3", "PMD-USG-605", "R4", "R5", "spacing", "420 mil", "410 mil", "A. Dörr", "uniformity tune, centre-thin"],
            ["2026-10-12 15:05", "ET3", "CT-STD-11", "R12", "R13", "over-etch", "22 %", "24 %", "D. Lindau", "VP12 CT open margin"],
        ]
        self.info["rcp_rows"] = write_csv(path, ["changed_at", "tool", "recipe", "rev_from", "rev_to", "parameter", "old_value",
                                                 "new_value", "engineer", "reason"], rows)

    # ------------------------------------------------------------------ the slurry loop's controller trend
    def sds_trend(self, path):
        """The SDS-OX1 controller's trend export: each tag stored when it moves past its deadband or on the 30-minute
        heartbeat; the flow tag reads L/min until the firmware update, gpm after; outages leave gaps."""
        fab, rng = self.fab, np.random.default_rng(P.SEED + 111)
        L = fab.loop
        t, v, lpc = L["t"], L["v"], L["lpc_tank"]
        area = math.pi * (0.0266 / 2) ** 2
        flow = v * area * 60000.0       # L/min
        vfd = np.where(t < W.tday(P.T_VFD_DOWN), 51.5, 38.0)
        stb = (t >= W.tday(P.T_STANDBY_ON)) & (t < W.tday(P.T_STANDBY_OFF))
        vfd = np.where(stb, 0.0, vfd) + rng.normal(0, 0.05, len(t))
        press = 1.05 + 0.92 * (v / P.V_NOM) ** 2 + rng.normal(0, 0.015, len(t))
        level = 30 + 60 * ((t - L["totes"][np.maximum(np.searchsorted(L["totes"], t, side="right") - 1, 0)]) % 2.6 / 2.6)
        level = 92 - level + rng.normal(0, 0.4, len(t))
        temp = 21.2 + 0.4 * np.sin(2 * np.pi * (t - 0.6)) + rng.normal(0, 0.05, len(t))
        upgrade = W.tday(P.T_SDS_UPGRADE)
        outages = [(W.tday(dt.datetime(2026, 3, 17, 11)), W.tday(dt.datetime(2026, 3, 19, 8))),
                   (W.tday(dt.datetime(2026, 7, 21, 2)), W.tday(dt.datetime(2026, 7, 21, 8, 30)))]
        lo = W.tday(dt.datetime(2025, 12, 1))
        tags = [("FT-101", flow, 2.0), ("PT-102", press, 0.05), ("SC-101", vfd, 0.4), ("LT-103", level, 3.0),
                ("AT-104", lpc, 110.0), ("TT-105", temp, 0.3)]
        rows = []
        for tag, series, db in tags:
            last_v, last_t = None, -1e9
            for i in range(len(t)):
                d = t[i]
                if d < lo or any(a <= d < b for a, b in outages):
                    continue
                val = float(series[i])
                if last_v is None or abs(val - last_v) > db or (d - last_t) >= 60 / 1440.0:
                    last_v, last_t = val, d
                    if tag == "FT-101":
                        if d < upgrade:
                            out, unit = "%.1f" % val, "L/min"
                        else:
                            out, unit = "%.2f" % (val * 0.264172), "gpm"
                    elif tag == "AT-104":
                        out, unit = "%.0f" % val, "cts/mL>0.56um"
                    elif tag == "PT-102":
                        out, unit = "%.3f" % val, "bar"
                    elif tag == "SC-101":
                        out, unit = "%.1f" % max(val, 0.0), "Hz"
                    elif tag == "LT-103":
                        out, unit = "%.1f" % val, "%"
                    else:
                        out, unit = "%.2f" % val, "degC"
                    rows.append([ts(d + rng.uniform(0, 0.0003)), "SDS-OX1", tag, out, unit, "GOOD"])
            if tag == "SC-101":
                rows.append([ts(W.tday(P.T_STANDBY_ON) + 0.0001), "SDS-OX1", "P-02B.RUN", "1", "-", "GOOD"])
                rows.append([ts(W.tday(P.T_STANDBY_OFF) + 0.0001), "SDS-OX1", "P-02B.RUN", "0", "-", "GOOD"])
        rows.sort(key=lambda r: (r[0], r[2]))
        self.info["sds_rows"] = write_csv(path, ["timestamp", "system", "tag", "value", "unit", "quality"], rows)

    def line_list(self, path):
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Line list"
        head(ws, ["system", "line_tag", "from", "to", "serves", "dist_from_tank_outlet_m", "DN", "ID_mm", "material", "note"],
             [10, 14, 16, 16, 12, 22, 5, 7, 10, 40])
        rows = [
            ["SDS-OX1", "OX1-L01", "TK-OX1 outlet", "VMB-OX1-1", "CM2", 64, 25, 26.6, "PFA", "ILD0 oxide slurry, recirculating loop"],
            ["SDS-OX1", "OX1-L02", "VMB-OX1-1", "VMB-OX1-2", "CM4", 148, 25, 26.6, "PFA", ""],
            ["SDS-OX1", "OX1-L03", "VMB-OX1-2", "VMB-OX1-3", "CM1", 231, 25, 26.6, "PFA", "riser to subfab level 2"],
            ["SDS-OX1", "OX1-L04", "VMB-OX1-3", "VMB-OX1-4", "CM3", 318, 25, 26.6, "PFA", ""],
            ["SDS-OX1", "OX1-L05", "VMB-OX1-4", "TK-OX1 return", "-", 402, 25, 26.6, "PFA", "return with back-pressure regulator BPR-106"],
            ["SDS-CE1", "CE1-L01", "TK-CE1 outlet", "VMB-CE1-1", "CC-1", 41, 20, 21.0, "PFA", "STI ceria slurry"],
            ["SDS-CE1", "CE1-L02", "VMB-CE1-1", "VMB-CE1-2", "CC-2", 97, 20, 21.0, "PFA", ""],
            ["SDS-CE1", "CE1-L03", "VMB-CE1-2", "TK-CE1 return", "-", 150, 20, 21.0, "PFA", ""],
            ["SDS-W1", "W1-L01", "TK-W1 outlet", "VMB-W1-1", "CW-1", 52, 20, 21.0, "PFA", "tungsten slurry"],
            ["SDS-W1", "W1-L02", "VMB-W1-1", "VMB-W1-2", "CW-2", 118, 20, 21.0, "PFA", ""],
            ["SDS-W1", "W1-L03", "VMB-W1-2", "TK-W1 return", "-", 171, 20, 21.0, "PFA", ""],
            ["CDS-HF1", "HF1-L01", "CDS-2 cabinet", "WB-1", "WB-1", 36, 15, 16.0, "PFA", "49 % HF to bench dilution unit"],
            ["CDS-HF1", "HF1-L02", "CDS-2 cabinet", "WB-2", "WB-2", 44, 15, 16.0, "PFA", ""],
            ["CDS-HCL", "HCL-L01", "CDS-3 cabinet", "WB-1", "WB-1", 38, 15, 16.0, "PFA", "HCl for SC2"],
            ["CDS-HCL", "HCL-L02", "CDS-3 cabinet", "WB-2", "WB-2", 47, 15, 16.0, "PFA", ""],
        ]
        for r in rows:
            ws.append(r)
        save_xlsx(wb, path, P.PEOPLE["fac"], P.PEOPLE["fac"], "2024-06-03T08:15:00Z", "2026-02-11T13:40:21Z")

    def fac_changes(self, path):
        c, d, n = P.FAC_STAFF["chem"], P.FAC_STAFF["day"], P.FAC_STAFF["night"]
        rows = [
            ["FC-2026-004", "2026-01-13 07:30", "HVAC", "AHU-4 fan belt replacement, bay 4 air change rate verified", d],
            ["FC-2026-007", "2026-01-27 13:40", "CHEM", "bulk H2SO4 distribution filter change, VMB-SA-2", c],
            ["FC-2026-011", "2026-02-02 22:00", "UPW", "UPW polish loop resin bed exchange (TOC trend)", n],
            ["FC-2026-015", "2026-02-19 06:10", "PCW", "process cooling water loop 2 strainer clean", d],
            ["FC-2026-018", "2026-03-03 09:20", "ELEC", "UPS 2 battery string replacement, transfer test ok", d],
            ["FC-2026-021", "2026-03-17 10:55", "SDS", "SDS-OX1 controller PLC replaced after I/O card fault; trend logging restored 19 Mar", c],
            ["FC-2026-024", "2026-04-08 15:05", "SDS", "SDS-CE1 ceria loop filter housing replaced (weep at the bowl seal)", c],
            ["FC-2026-026", "2026-04-21 10:15", "SDS", "SDS-OX1/CE1/W1 controller firmware 4.2 (flow totaliser; flow unit set to gpm)", c],
            ["FC-2026-028", "2026-04-28 08:35", "CHEM", "HF bulk supply pressure regulator replaced, set 2.1 bar", c],
            ["FC-2026-030", "2026-05-06 14:20", "EXH", "acid exhaust balancing bay 3 after new duct take-off", d],
            ["FC-2026-034", "2026-06-02 09:40", "SDS", "EP-114 pump energy programme: SDS-OX1 P-02A VFD setpoint 51.5 Hz -> 38.0 Hz; loop pressure at VMB-OX1-4 verified >= 1.4 bar", c],
            ["FC-2026-035", "2026-06-02 11:15", "SDS", "EP-114: SDS-W1 P-07A VFD setpoint 50 Hz -> 41 Hz", c],
            ["FC-2026-039", "2026-06-16 07:50", "SDS", "SDS-W1 tungsten slurry day tank inspection and clean", c],
            ["FC-2026-041", "2026-06-24 23:00", "N2", "bulk N2 vaporiser 2 defrost cycle retune", n],
            ["FC-2026-044", "2026-07-08 10:30", "PCW", "PCW loop 2 plate heat exchanger cleaned, approach temperature back to 1.8 K", d],
            ["FC-2026-047", "2026-07-21 02:00", "SDS", "SDS-OX1 controller reboot (watchdog); trend gap 02:00-08:30", n],
            ["FC-2026-050", "2026-08-04 13:15", "VAC", "house vacuum pump 3 rebuild", d],
            ["FC-2026-052", "2026-08-10 14:05", "SDS", "SDS-OX1 P-02A VFD fault (overcurrent); standby pump P-02B started (fixed speed) pending VFD repair", d],
            ["FC-2026-058", "2026-08-24 16:30", "SDS", "SDS-OX1 P-02A VFD repaired and returned to service at EP-114 setpoint; P-02B to standby", c],
            ["FC-2026-061", "2026-09-01 08:00", "HVAC", "cleanroom ceiling FFU bank 7 filter changes (12 units)", d],
            ["FC-2026-063", "2026-09-10 11:45", "UPW", "UPW polish loop resistivity analyser recalibrated", d],
            ["FC-2026-066", "2026-09-22 21:30", "CDA", "CDA dryer 1 desiccant change", n],
            ["FC-2026-069", "2026-10-05 05:40", "N2", "bulk N2 purifier B regeneration", n],
            ["FC-2026-072", "2026-10-14 06:45", "PCW", "PCW loop 1 pump seal replacement", d],
            ["FC-2026-078", "2026-10-29 10:00", "UPW", "UPW final filter change (point of distribution)", d],
        ]
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "Change log"
        head(ws, ["change_no", "executed", "system", "description", "by"], [12, 17, 7, 110, 12])
        for r in rows:
            ws.append(r)
        save_xlsx(wb, path, P.PEOPLE["fac"], P.PEOPLE["fac"], "2026-01-05T07:02:00Z", "2026-10-29T10:31:07Z")

    # ------------------------------------------------------------------ the bench controller and the lab
    def bench_log(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 112)
        bg_prefix = ["VQ2", "VL0", "VS3", "VM7", "VK5"]
        lines = []
        lo = W.tday(dt.datetime(2025, 12, 1))
        seq = {b: 880000 + 50000 * i for i, b in enumerate(P.BENCHES)}
        for b in P.BENCHES:
            use_utc = b == "WB-2"
            stamp = (lambda d: utc(d)) if use_utc else (lambda d: ts(d, "%Y-%m-%dT%H:%M:%S"))
            out = []
            for e in fab.bench_events[b]:
                if e["d"] < lo:
                    continue
                seq[b] += 1 + int(rng.poisson(1.4))      # the controller numbers every tank's events; the export keeps T3
                if e["ev"] == "BATCH":
                    lot = e["lot"] if e["lot"] else "%s%05d" % (bg_prefix[int(rng.integers(0, 5))], int(rng.integers(10000, 99999)))
                    rec = {"tool": b, "seq": seq[b], "ts": stamp(e["d"]), "event": "BATCH_START", "tank": "T3",
                           "lot": old_id(lot, e["d"]), "wafers": e["n"], "recipe": "PGC-HFSC2-07"}
                elif e["ev"] == "SPIKE":
                    rec = {"tool": b, "seq": seq[b], "ts": stamp(e["d"]), "event": "CHEM_SPIKE", "tank": "T3",
                           "added_l": 6.0, "chem_lot": "HCL-%d" % (2260 + int(e["d"] // 9))}
                else:
                    rec = {"tool": b, "seq": seq[b], "ts": stamp(e["d"]), "event": "DRAIN_FILL", "tank": "T3",
                           "fill_l": 52.0, "chem_lot": "HCL-%d" % (2260 + int(e["d"] // 9))}
                out.append(rec)
                if rng.random() < 0.0008:
                    seq[b] += 1
                    out.append({"tool": b, "seq": seq[b], "ts": stamp(e["d"] + 0.0002), "event": "CTRL_RESTART",
                                "reason": "watchdog"})
                    self.events.append({"t": W.dtime(e["d"] + 0.0002), "kind": "restart", "tool": b, "after": e["ev"],
                                        "lot": rec.get("lot", "")})
                    for dup in out[-4:-1]:
                        out.append(dict(dup))
                if rng.random() < 0.004:
                    seq[b] += 1
                    out.append({"tool": b, "seq": seq[b], "ts": stamp(e["d"] + 0.001), "event": "ALARM",
                                "code": str(rng.choice(["T3_TEMP_HI", "T3_LEVEL_LO", "RINSE_RES_LO", "EXH_FLOW_LO"])),
                                "cleared": True})
                    self.events.append({"t": W.dtime(e["d"] + 0.001), "kind": "alarm", "tool": b, "code": out[-1]["code"]})
            lines += out
        lines.sort(key=lambda r: (r["tool"], r["seq"]))
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for r in lines:
                fh.write(json.dumps(r, ensure_ascii=False) + "\n")
        self.info["bench_lines"] = len(lines)

    def lab(self, path):
        fab, rng = self.fab, np.random.default_rng(P.SEED + 113)
        rows = []
        n = 0
        d = W.tday(dt.datetime(2026, 1, 5, 6, 20))
        while d < W.tday(dt.datetime(2026, 10, 30)):
            for b in P.BENCHES:
                n += int(rng.integers(3, 19))
                rows.append(self._sample(b, d + rng.uniform(0, 0.01), "routine weekly", n, rng))
            d += 7
        inv = [dt.datetime(2026, 8, 18, 14, 10), dt.datetime(2026, 8, 18, 22, 5), dt.datetime(2026, 8, 19, 3, 40),
               dt.datetime(2026, 8, 25, 11, 30), dt.datetime(2026, 8, 25, 19, 55), dt.datetime(2026, 8, 26, 4, 15),
               dt.datetime(2026, 9, 2, 9, 40), dt.datetime(2026, 9, 2, 16, 20), dt.datetime(2026, 9, 3, 1, 50),
               dt.datetime(2026, 9, 9, 13, 5), dt.datetime(2026, 9, 9, 23, 35), dt.datetime(2026, 9, 16, 8, 0),
               dt.datetime(2026, 9, 16, 17, 45), dt.datetime(2026, 9, 23, 12, 25), dt.datetime(2026, 9, 24, 2, 10)]
        for t in inv:
            for b in P.BENCHES:
                n += int(rng.integers(1, 4))
                rows.append(self._sample(b, W.tday(t) + rng.uniform(0, 0.004), "investigation (YE-26-114)", n, rng))
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = "ICP-MS results"
        head(ws, ["sample_id", "bench", "tank", "sampled", "analysed", "request", "Fe_ppb", "Ni_ppb", "Cu_ppb", "method",
                  "analyst", "comment"], [12, 7, 5, 17, 17, 24, 8, 8, 8, 14, 11, 30])
        for r in rows:
            ws.append(r)
        save_xlsx(wb, path, P.PEOPLE["lab"], P.PEOPLE["lab"], "2026-01-05T09:30:00Z", "2026-10-30T14:02:51Z")
        self.info["lab_rows"] = len(rows)

    def _sample(self, bench, d, request, n, rng):
        c = self.fab.bath_state(bench, d)
        vals = []
        for share in (0.55, 0.25, 0.20):
            x = c * share * rng.normal(1, 0.06) + rng.normal(0, 0.012)
            vals.append("<0.05" if x < 0.05 else round(float(x), 3))
        d_an = d + rng.uniform(0.8, 2.5)
        who = P.LAB_STAFF[W.dtime(d_an).isocalendar()[1] % len(P.LAB_STAFF)]
        return ["LB26-%04d" % n, bench, "T3", ts(d, "%Y-%m-%d %H:%M"), ts(d_an, "%Y-%m-%d %H:%M"),
                request, vals[0], vals[1], vals[2], "ICP-MS, SEMI C35", who, ""]


def write(fab, tgt):
    import docs as D
    pk = Pack(fab)
    p = lambda k: os.path.join(tgt, F[k])
    pk.sort_db(p("sort"))
    pk.mes(p("mes"))
    pk.genealogy(p("gen"))
    pk.cmp_exports(tgt)
    pk.dep_log(p("dep"))
    pk.etch_fdc(p("etch"))
    pk.monitors(p("mon"))
    pk.thickness(p("thk"), p("spc"))
    pk.inspection(p("insp"))
    pk.wat(p("wat"))
    pk.pm_log(p("pm"))
    pk.recipes(p("rcp"))
    pk.sds_trend(p("sds"))
    pk.line_list(p("lines"))
    pk.fac_changes(p("fac"))
    pk.bench_log(p("bench"))
    pk.lab(p("lab"))
    D.ecn_register(p("ecn"))
    D.product_sheet(p("prod"), fab)
    D.ramp_plan(p("plan"))
    D.costs(p("cost"))
    D.shift_notes(p("notes"), fab, pk.events)
    pk.info["env_rows"] = D.environment(p("env"))
    pk.info["probe_rows"] = D.probe_cards(p("probe"))
    pk.info["ovl_rows"] = D.overlay(p("ovl"), fab)
    return pk.info
