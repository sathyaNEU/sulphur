"""task15: the pack's data files, written the way each system exports them. No file describes another.

Banyena's side: the plot harvest record in two layouts (the old logger's export to its last season, the harvest
system's from the season after), each trial's entry list, the trial and site lists, monthly rain at the sites, the Kerang irrigation log, the
line register and the nomination workbook. The series' side: the published site results and the site seasons.
Beside them the quality laboratory's results, the disease nursery scores and the seed store's inventory.
"""
import csv
import datetime as dt
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font
from openpyxl.utils import get_column_letter

import panel as PN
import world as W

AEDT = dt.timezone(dt.timedelta(hours=11))
AEST = dt.timezone(dt.timedelta(hours=10))
SITE_CODE = {"Walpeup": "WAL", "Hopetoun": "HOP", "Manangatang": "MAN", "Birchip": "BIR", "Horsham": "HOR",
             "Minyip": "MIN", "Kaniva": "KAN", "Lake Bolac": "LBO", "Skipton": "SKI", "Kerang": "KER"}
STAGE_NAME = {"S1": "Stage 1", "S2": "Stage 2", "S3": "Stage 3"}
SOW_DOY = {"LRZ": 128, "MRZ": 138, "HRZ": 152}      # early May in the Mallee to the start of June in the south
HARVEST_DOY = {"LRZ": 312, "MRZ": 326, "HRZ": 349}
PARENTS = ["Tatyoon", "Willaura", "Wickliffe", "Moyston", "Pomonal", "Jeparit", "Beulah", "Lascelles", "Woomelang",
           "Nullawil", "Watchem", "Glenorchy", "Lubeck", "Dooen", "Marnoo", "Callawadda", "Wallup", "Kewell", "Ailsa",
           "Areegra", "Brim", "Galaquil", "Byaduk", "Wando", "Carapook", "Nareen"]
REMARKS = ["wheel track", "edge plot", "thin stand", "ryegrass", "header blockage, restarted", "short plot",
           "bird damage at south end", "mouse damage", "wet patch", "late tillers", "frost tipping"]
BREEDER_OF = {"Byaduk": "Glenelg Plant Breeding", "Wando": "Otway Cereals", "Carapook": "Corangamite Seeds",
              "Nareen": "Banyena Grain Genetics"}


def rng(w, *key):
    return np.random.default_rng([w["seed"], 77, *key])


def date_of(year, doy):
    return dt.date(year, 1, 1) + dt.timedelta(days=int(doy) - 1)


def trial_facts(w):
    """Sowing and harvest dates, plot size: what the trials list holds for each programme trial."""
    out = {}
    zone = {s[0]: s[2] for s in W.PROGRAMME_SITES}
    for code, t in w["trials"].items():
        if t["series"]:
            continue
        r = rng(w, 1, W.hash_name(code))
        z = zone[t["site"]]
        if t["site"] == "Kerang":
            sow, hv = 135, 331
        else:
            sow, hv = SOW_DOY[z], HARVEST_DOY[z]
        sow += int(r.integers(-9, 12))
        hv += int(r.integers(-8, 11)) + {"S1": 4, "S2": 2, "S3": 0}[t["stage"]]
        out[code] = dict(sown=date_of(t["season"], sow), harvest=date_of(t["season"], hv),
                         length=float(r.choice([5.0, 5.5, 5.5, 6.0])),
                         width=1.76 if t["season"] >= W.WIDE_FROM else 1.54,
                         moist=float(r.uniform(9.6, 13.4)))
    return out


def line_label(w, lid, stage):
    """How a line is written on that stage's entry list."""
    ln = w["lines"][lid]
    if ln["kind"] == "check":
        return lid
    if stage == "S3" and ln.get("wi"):
        return ln["wi"]
    return lid


def write_csv(path, header, rows, repeat_header_on=None):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator="\r\n")
        wr.writerow(header)
        last = None
        for row in rows:
            if repeat_header_on is not None:
                key = row[repeat_header_on]
                if last is not None and key != last:
                    wr.writerow(header)
                last = key
            wr.writerow(row)


def plot_files(w, target, facts):
    """The harvest record. A plot's weight is taken off the harvester at field moisture; the system stores the
    yield at 12.5 per cent moisture. A plot weighed twice has two rows in the new system, the later one standing."""
    old, new = [], []
    tr = w["trials"]
    by_trial = {}
    for p in w["plots"]:
        by_trial.setdefault(p[0], []).append(p)
    order = sorted(by_trial, key=lambda c: (tr[c]["season"], facts[c]["harvest"], c))
    n_reweigh = 0
    for code in order:
        t, f = tr[code], facts[code]
        r = rng(w, 2, W.hash_name(code))
        rows = sorted(by_trial[code], key=lambda p: (p[4], p[5] if p[4] % 2 else -p[5]))    # the harvester's serpentine path
        area = round(f["length"] * f["width"], 2)
        day = dt.datetime.combine(f["harvest"], dt.time(9, 0)) + dt.timedelta(minutes=int(r.integers(5, 95)))
        clock = day
        for (c, plot_no, rep, blk, rng_, col, eno, lid, yv, L, ab) in rows:
            clock += dt.timedelta(seconds=float(r.lognormal(math.log(105), 0.35)))
            if clock.hour >= 18 or (clock.hour == 17 and clock.minute > 20):
                nxt = clock.date() + dt.timedelta(days=1)
                clock = dt.datetime.combine(nxt, dt.time(8, 40)) + dt.timedelta(minutes=int(r.integers(0, 70)))
            if clock.hour == 12 and clock.minute < 5 and r.random() < 0.6:
                clock += dt.timedelta(minutes=int(r.integers(25, 50)))
            moist = float(np.clip(f["moist"] + r.normal(0, 0.45), 8.0, 16.5))
            note = ""
            if ab:
                note = str(r.choice(["lodged, header could not pick up", "flat, not harvested", "lodged",
                                     "lodged and tangled, left"]))
            elif r.random() < 0.021:
                note = str(r.choice(REMARKS))
            lod = int(round(L * 10))
            if t["season"] <= W.OLD_LAST:
                if ab:
                    old.append([code, plot_no, rep, blk, rng_, col, eno, "%.1f" % f["length"], "", "", "", lod, "N",
                                clock.strftime("%d/%m/%Y"), note])
                else:
                    kg = yv * (f["length"] * f["width"]) / 10.0 * (100 - 12.5) / (100 - moist)
                    old.append([code, plot_no, rep, blk, rng_, col, eno, "%.1f" % f["length"], "%.2f" % kg,
                                "%.1f" % moist, int(round(yv * 1000)), lod, "Y", clock.strftime("%d/%m/%Y"), note])
            else:
                tz = AEDT
                stamp = clock.replace(tzinfo=tz).isoformat(timespec="seconds")
                if ab:
                    new.append([code, plot_no, rep, blk, rng_, col, eno, "%.2f" % area, "", "", "", lod, "abandoned",
                                "", 1, note])
                    continue
                kg = yv * area / 10.0 * (100 - 12.5) / (100 - moist)
                if r.random() < 0.0068:        # the sample was weighed again; both weighings are kept
                    n_reweigh += 1
                    off = float(r.choice([-1, 1]) * r.uniform(0.012, 0.06))
                    kg0 = kg * (1 + off)
                    y0 = yv * (1 + off)
                    new.append([code, plot_no, rep, blk, rng_, col, eno, "%.2f" % area, "%.2f" % kg0, "%.1f" % moist,
                                "%.3f" % y0, lod, "harvested", stamp, 1, note])
                    stamp2 = (clock + dt.timedelta(minutes=int(r.integers(3, 40)))).replace(tzinfo=tz).isoformat(
                        timespec="seconds")
                    new.append([code, plot_no, rep, blk, rng_, col, eno, "%.2f" % area, "%.2f" % kg, "%.1f" % moist,
                                "%.3f" % yv, lod, "harvested", stamp2, 2, "reweighed"])
                else:
                    new.append([code, plot_no, rep, blk, rng_, col, eno, "%.2f" % area, "%.2f" % kg, "%.1f" % moist,
                                "%.3f" % yv, lod, "harvested", stamp, 1, note])
    write_csv(os.path.join(target, W.FILES["old"]),
              ["Trial", "Plot", "Rep", "Blk", "Range", "Row", "Entry", "PlotLen_m", "GrainWt_kg", "Moist_pct",
               "Yld_kgha_12.5", "Lodging_pct", "Harvested", "HarvDate", "Remarks"], old, repeat_header_on=0)
    write_csv(os.path.join(target, W.FILES["new"]),
              ["trial_code", "plot_no", "replicate", "block", "range", "row", "entry_no", "plot_area_m2", "grain_kg",
               "moisture_pct", "yield_t_ha", "lodging_pct", "plot_status", "harvested_at", "weigh_seq", "note"], new)
    return dict(old_rows=len(old), new_rows=len(new), reweighed=n_reweigh)


def entry_lists(w, target):
    rows = []
    tr = w["trials"]
    for code in sorted((c for c, t in tr.items() if not t["series"]), key=lambda c: (tr[c]["season"], c)):
        t = tr[code]
        for lid, eno in sorted(t["entry_no"].items(), key=lambda kv: kv[1]):
            lab = line_label(w, lid, t["stage"])
            if t["stage"] == "S1" and t["season"] in (W.FIRST + 1, W.FIRST + 3) and "X" in lab:
                lab = lab.replace("X", "x")            # those two seasons' sowing lists were keyed in lower case
            if t["stage"] == "S3" and t["season"] in (W.FIRST + 4, W.FIRST + 7) and lab.startswith("WI"):
                lab = "WI " + lab[2:]                   # and two Stage 3 lists carry the space the seed labels print
            rows.append([code, eno, lab])
    write_csv(os.path.join(target, W.FILES["entries"]), ["trial_code", "entry_no", "line"], rows)
    return len(rows)


def trials_list(w, target, facts):
    tr = w["trials"]
    rows = []
    nplots = {}
    for p in w["plots"]:
        nplots[p[0]] = nplots.get(p[0], 0) + 1
    for code in sorted((c for c, t in tr.items() if not t["series"]), key=lambda c: (tr[c]["season"], c)):
        t, f = tr[code], facts[code]
        n = nplots[code]
        rows.append([code, t["season"], STAGE_NAME[t["stage"]], t["site"], f["sown"].isoformat(),
                     f["harvest"].isoformat(), t["reps"], n, "%.1f" % f["length"], "%.2f" % f["width"]])
    write_csv(os.path.join(target, W.FILES["trials"]),
              ["trial_code", "season", "stage", "site", "sown", "harvest_started", "replicates", "plots",
               "plot_length_m", "plot_width_m"], rows)
    return len(rows)


def rainfall(w, target):
    """Monthly rain at the gauge nearest each trial site, as the bureau's monthly files give it."""
    rows = []
    gap = 0
    for (name, *_r) in W.PROGRAMME_SITES:
        for y in w["years"]:
            e = w["env"][(name, y)]
            r = rng(w, 3, W.hash_name(name), y)
            off = list(e["offseason"])          # January, February, March, November, December
            months = off[:3] + list(e["months"]) + off[3:]
            for m, v in enumerate(months, 1):
                if m in (1, 2, 12) and r.random() < 0.012:
                    rows.append([name, y, m, ""])       # the gauge was out
                    gap += 1
                else:
                    rows.append([name, y, m, "%.1f" % v])
    write_csv(os.path.join(target, W.FILES["rain"]), ["site", "year", "month", "rain_mm"], rows)
    irr = []
    for y in w["years"]:
        e = w["env"][("Kerang", y)]
        r = rng(w, 4, y)
        for doy, mm in e["irrigation"]:
            irr.append([date_of(y, doy).isoformat(), "K3", int(mm), str(r.choice(["channel 7/2", "channel 7/2", "bore"]))])
    write_csv(os.path.join(target, W.FILES["irrigation"]), ["date", "bay", "applied_mm", "supply"], irr)
    return dict(rain_rows=len(rows), rain_gaps=gap, irrigations=len(irr))


def _sheet(ws, header, rows, widths, formats=None):
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True)
        c.alignment = Alignment(vertical="center")
    for row in rows:
        ws.append(row)
    for k, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    ws.freeze_panes = "A2"
    for col, fmt in (formats or {}).items():
        for cell in ws[col][1:]:
            cell.number_format = fmt


def sites_workbook(w, target):
    wb = Workbook()
    ws = wb.active
    ws.title = "Trial sites"
    rows = []
    first = {}
    for code, t in w["trials"].items():
        if not t["series"]:
            first[t["site"]] = min(first.get(t["site"], 9999), t["season"])
    for (name, district, zone, lat, lon, soil, gsr, irr) in W.PROGRAMME_SITES:
        rows.append([name, SITE_CODE[name], district, zone, lat, lon, soil, "yes" if irr else "no", first[name]])
    _sheet(ws, ["Site", "Code", "District", "Rainfall zone", "Latitude", "Longitude", "Soil", "Irrigated",
                "First trial season"], rows, [14, 7, 20, 13, 10, 10, 26, 10, 17], {"E": "0.00", "F": "0.00"})
    path = os.path.join(target, W.FILES["sites"])
    wb.save(path)
    return path


def line_register(w, target):
    """The breeding database's register: a line's cross code, its WI number once it reaches Stage 3, its cross."""
    wb = Workbook()
    ws = wb.active
    ws.title = "Lines"
    last_stage, nom_year = {}, {}
    for (stage, y), ls in w["stage_sets"].items():
        for l in ls:
            if y <= W.LAST and (l not in last_stage or (int(stage[1]), y) > last_stage[l]):
                last_stage[l] = (int(stage[1]), y)
    for sow, ds in w["nominations"].items():
        for d in ds:
            nom_year[d["line"]] = sow
    rows = []
    cross_parents = {}
    for lid in w["order"]:
        ln = w["lines"][lid]
        if ln["kind"] != "line":
            continue
        cross = lid.split("-")[0]
        if cross not in cross_parents:
            r = rng(w, 5, W.hash_name(cross))
            a, b = r.choice(len(PARENTS), size=2, replace=False)
            cross_parents[cross] = "%s / %s" % (PARENTS[a], PARENTS[b])
        stg, yr = last_stage.get(lid, (1, ln["cohort"]))
        if lid in nom_year:
            status = "nominated to HRBS for %d" % nom_year[lid]
        elif yr == W.LAST:
            status = "in trial %d" % yr
        else:
            status = "discarded after %d" % yr
        rows.append([lid, ln["wi"] or "", cross_parents[cross], ln["cohort"], "Stage %d" % stg, yr, status])
    _sheet(ws, ["Cross code", "WI number", "Cross", "First trial season", "Last stage", "Last trial season", "Status"],
           rows, [13, 11, 26, 17, 11, 17, 30])
    ws2 = wb.create_sheet("Check varieties")
    _sheet(ws2, ["Variety", "Breeder", "In programme trials since"],
           [[c, BREEDER_OF[c], W.FIRST] for c in W.CHECKS], [14, 28, 24])
    path = os.path.join(target, W.FILES["register"])
    wb.save(path)
    return path, len(rows)


def nominations_workbook(w, target):
    wb = Workbook()
    ws = wb.active
    ws.title = "HRBS nominations"
    rows = []
    for sow, ds in sorted(w["nominations"].items()):
        r = rng(w, 6, sow)
        day = dt.date(sow, 2, int(r.integers(9, 25)))
        for d in ds:
            vals = [w["rel"].get((d["line"], "%02dS3%s" % (yy % 100, SITE_CODE[s])), float("nan"))
                    for yy in d["s3"] for s in W.INDEX_SITES]
            n_tr = sum(1 for v in vals if v == v)
            rows.append([sow, w["lines"][d["line"]]["wi"], ", ".join(str(y) for y in d["s3"]), n_tr,
                         round(d["index"], 1), day, float(r.choice([12, 12, 15, 18, 20]))])
    _sheet(ws, ["Sowing year", "WI number", "Stage 3 seasons", "Trials in index", "High-rainfall index (% of Byaduk)",
                "Nominated", "Seed sent (kg)"], rows, [12, 11, 16, 14, 30, 12, 14], {"E": "0.0", "F": "d mmm yyyy"})
    path = os.path.join(target, W.FILES["nominations"])
    wb.save(path)
    return path, len(rows)


def series_label(w, lid):
    ln = w["lines"][lid]
    if ln["kind"] == "line":
        return ln["wi"]
    return lid


def series_files(w, target):
    """What the series publishes: every entry's site mean, and a line per site and season."""
    rows = []
    for c in sorted(w["series_cells"], key=lambda c: (c["season"], c["site"], series_label(w, c["line"]))):
        ln = w["lines"][c["line"]]
        breeder = (BREEDER_OF.get(c["line"]) or ln.get("breeder") or "Banyena Grain Genetics")
        rows.append([c["season"], c["site"], series_label(w, c["line"]), breeder, c["plots"], "%.2f" % c["y"],
                     "%.1f" % (c["L"] * 10.0)])
    write_csv(os.path.join(target, W.FILES["results"]),
              ["season", "site", "entry", "breeder", "plots", "grain_yield_t_ha", "lodging_pct"], rows)
    srows = []
    lost = 0
    months = ["July", "August", "September"]
    kept_notes = [
        lambda r: "resown %d June after a seeder blockage" % int(r.integers(9, 24)),
        lambda r: "rep %d waterlogged in %s, kept" % (int(r.integers(1, 4)), months[int(r.integers(0, 3))]),
        lambda r: "harvest held up by rain, %d days" % int(r.integers(3, 12)),
        lambda r: "bird damage along the %s edge" % ["east", "west", "north", "south"][int(r.integers(0, 4))],
        lambda r: "late ryegrass, sprayed out %d September" % int(r.integers(2, 28)),
        lambda r: "sown into a wet seedbed, %d mm in the week before" % int(r.integers(18, 61)),
        lambda r: "lodging scored %d days after the others" % int(r.integers(4, 11)),
        lambda r: "net blotch from %s" % ["August", "September", "October"][int(r.integers(0, 3))],
        lambda r: "scald in %s" % months[int(r.integers(1, 3))],
        lambda r: "frost on %d October, no damage seen" % int(r.integers(2, 21)),
        lambda r: "slugs in rep %d, baited" % int(r.integers(1, 4)),
        lambda r: "mice at sowing, baited",
        lambda r: "header breakdown, finished %d December" % int(r.integers(18, 30)),
        lambda r: "leaf rust from %s" % ["mid September", "late September", "early October", "mid October"][
            int(r.integers(0, 4))]]
    lost_notes = ["waterlogged from %s, not harvested", "hail on %d November, not harvested",
                  "poor establishment after a dry sowing, abandoned in %s", "sheep got in during %s, abandoned"]
    for (name, district, lat, lon, soil, gsr) in W.SERIES_SITES:
        for y in w["years"]:
            code = "HRBS%02d-%s" % (y % 100, name[:3].upper())
            r = rng(w, 7, W.hash_name(code))
            e = w["env"][(name, y)]
            sow = date_of(y, 150 + int(r.integers(-8, 14)))
            if code in w["series_trials"]:
                t = w["series_trials"][code]
                hv = date_of(y, 350 + int(r.integers(-9, 9)))
                note = ""
                if r.random() < 0.11:
                    note = kept_notes[int(r.integers(0, len(kept_notes)))](r)
                srows.append([y, name, district, sow.isoformat(), hv.isoformat(), int(t["rain"]), "%.2f" % t["mean"],
                              "%.1f" % t["cv"], "harvested", note])
            else:
                lost += 1
                note = str(r.choice(lost_notes))
                if "%d" in note:
                    note = note % int(r.integers(3, 27))
                elif "%s" in note:
                    note = note % str(r.choice(["July", "August", "September"]))
                srows.append([y, name, district, sow.isoformat(), "", int(e["W"]), "", "", "abandoned", note])
    srows.sort(key=lambda r_: (r_[0], r_[1]))
    write_csv(os.path.join(target, W.FILES["seasons"]),
              ["season", "site", "district", "sown", "harvested", "apr_oct_rain_mm", "trial_mean_t_ha", "cv_pct",
               "status", "comment"], srows)
    return dict(series_rows=len(rows), site_seasons=len(srows), lost=lost)


def side_files(w, target):
    """The quality laboratory's Stage 3 results, the disease nursery's scores and the seed store's inventory."""
    lines = w["lines"]
    q, dz = [], []
    for y in (W.LAST - 2, W.LAST - 1, W.LAST):
        ents = w["stage_sets"].get(("S3", y), [])
        r = rng(w, 8, y)
        for lid in ents + list(W.CHECKS):
            lab = lines[lid]["wi"] if lines[lid]["kind"] == "line" else lid
            base_p = 10.6 + 6.0 * (0.44 - lines[lid]["s"]) * 0.2 - 2.2 * lines[lid]["g"] + r.normal(0, 0.25)
            for site in ("Horsham", "Birchip", "Lake Bolac", "Kerang"):
                e = w["env"][(site, y)]
                prot = base_p + 0.9 * (1.0 - min(1.6, e["W"] / 350.0)) + r.normal(0, 0.35)
                ret = float(np.clip(88 - 9 * max(0.0, 1.1 - e["W"] / 300.0) + r.normal(0, 4.0), 40, 99))
                scr = float(np.clip(4.5 + 6 * max(0.0, 1.0 - e["W"] / 280.0) + r.normal(0, 1.6), 0.4, 30))
                tw = float(np.clip(66.5 + r.normal(0, 1.4) - 2.5 * max(0.0, 1.0 - e["W"] / 260.0), 55, 74))
                q.append([y, site, lab, "%.1f" % prot, "%.1f" % ret, "%.1f" % scr, "%.1f" % tw])
            rs = np.random.default_rng([w["seed"], 78, W.hash_name(lid)])
            res = rs.integers(2, 9, size=4)
            for nursery, k in (("Horsham", 0), ("Hamilton", 1)):
                dz.append([y, nursery, lab, int(np.clip(res[0] + r.integers(-1, 2), 1, 9)),
                           int(np.clip(res[1] + r.integers(-1, 2), 1, 9)), int(np.clip(res[2] + r.integers(-1, 2), 1, 9)),
                           int(np.clip(res[3] + r.integers(-1, 2), 1, 9))])
    write_csv(os.path.join(target, W.FILES["quality"]),
              ["season", "site", "line", "protein_pct_db", "retention_pct_2.5mm", "screenings_pct_2.2mm",
               "test_weight_kg_hl"], q)
    write_csv(os.path.join(target, W.FILES["disease"]),
              ["season", "nursery", "line", "net_form_net_blotch", "spot_form_net_blotch", "leaf_rust", "scald"], dz)
    wb = Workbook()
    ws = wb.active
    ws.title = "Seed store"
    rows = []
    r = rng(w, 9)
    for lid in w["stage_sets"][("S3", W.LAST)]:
        lab = lines[lid]["wi"]
        rows.append([lab, "SS%02d-%04d" % (W.LAST % 100, int(r.integers(100, 9000))), int(r.integers(38, 160)),
                     float(round(r.uniform(96.0, 99.6), 1)), int(r.integers(88, 100)),
                     str(r.choice(["Shed 2 bay A", "Shed 2 bay B", "Cool room"]))])
    _sheet(ws, ["WI number", "Seed lot", "Clean seed (kg)", "Purity (%)", "Germination (%)", "Held at"], rows,
           [11, 12, 15, 11, 15, 14], {"D": "0.0"})
    path = os.path.join(target, W.FILES["seed"])
    wb.save(path)
    return dict(quality_rows=len(q), disease_rows=len(dz), seed_rows=len(rows)), path


def write_all(w, target):
    facts = trial_facts(w)
    counts = {}
    counts.update(plot_files(w, target, facts))
    counts["entry_rows"] = entry_lists(w, target)
    counts["trials"] = trials_list(w, target, facts)
    counts.update(rainfall(w, target))
    sites_path = sites_workbook(w, target)
    reg_path, counts["register_rows"] = line_register(w, target)
    nom_path, counts["nominations"] = nominations_workbook(w, target)
    counts.update(series_files(w, target))
    side, seed_path = side_files(w, target)
    counts.update(side)
    return facts, counts, dict(sites=sites_path, register=reg_path, nominations=nom_path, seed=seed_path)
