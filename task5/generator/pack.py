"""The systems' exports and the tables, written from world.py's arrays: Orlava's register events, the area office's
migration tables as released, its vital events table and census workbook, Orlava's census table, Fenmark's 2016
count, the establishment in force, the code table, the municipality list and two files nobody here needs."""
import csv
import datetime as dt
import os

import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

import core as C
import world as WL

FILES = {
    "register": "orlava_register_migration_events_2011_2026.csv",
    "tables": "cmaso_migration_tables_releases_2014_2026.csv",
    "vital": "cmaso_vital_events_foreign_citizens_2011_2023.csv",
    "census": "cmaso_census_rounds_2011_2021_usual_residents.xlsx",
    "c14": "orlava_census_2021_table_C14.xlsx",
    "count16": "fenmark_population_count_2016_by_citizenship.xlsx",
    "estab": "consular_establishment_in_force.xlsx",
    "codes": "state_codes.csv",
    "muni": "orlava_municipalities.csv",
    "pop": "cmaso_population_1_january_2011_2026.csv",
    "traffic": "orlava_passenger_traffic_by_partner_state_2011_2026.csv",
}
HOME, HOSTS, STATES, ROW, PARTNERS = WL.HOME, WL.HOSTS, WL.STATES, WL.ROW, WL.PARTNERS
NY, LAST, Y0 = WL.NY, WL.LAST, WL.Y0
EXTRACT = dt.date(2027, 2, 19)
MAX_LAG = 42
MONTH_W = np.array([1.25, 0.85, 0.9, 0.9, 0.95, 1.0, 1.05, 1.3, 1.5, 1.2, 0.9, 0.7])
REGIONS = ["Osrednja", "Primorska", "Gorska", "Podravska", "Dolenjska", "Zahodna"]


def _days(year):
    d0 = dt.date(year, 1, 1)
    n = (dt.date(year + 1, 1, 1) - d0).days
    days = [d0 + dt.timedelta(k) for k in range(n)]
    w = np.array([MONTH_W[d.month - 1] * (0.35 if d.weekday() >= 5 else 1.0) for d in days])
    return np.array([d.toordinal() for d in days]), w / w.sum()


def register_rows(WD):
    """One row per deregistration abroad or registration from abroad in Orlava's register, 2011 to 2026."""
    rng = np.random.default_rng([C.SEED, 600])
    nm = len(WL.MUNICIPALITIES)
    mw = 1.0 / (np.arange(nm) + 2.0) ** 0.85
    mw[0] *= 3.0
    mw /= mw.sum()
    old = np.zeros(nm, bool)
    old[rng.choice(nm, nm // 3, replace=False)] = True
    cols = {k: [] for k in ("move", "lag", "mun", "etype", "cit", "sex", "birth", "state")}
    pid = {p: k for k, p in enumerate(PARTNERS)}
    others = np.array([pid[p] for p in PARTNERS if p != HOME])
    for t in WL.TABLES:
        own = t in ("B", "D")
        for p in PARTNERS:
            if p == HOME:
                continue
            sp = WD["split"][t, HOME, p]
            for y in range(NY):
                ords, w = _days(Y0 + y)
                for s in range(2):
                    for a in range(len(WL.AGES)):
                        c = int(sp[y, s, a])
                        if not c:
                            continue
                        cols["move"].append(rng.choice(ords, c, p=w))
                        u = rng.random(c)
                        lag = np.where(u < 0.55, rng.integers(0, 4, c), np.where(u < 0.85, rng.integers(4, 15, c),
                                                                                 rng.integers(15, MAX_LAG + 1, c)))
                        cols["lag"].append(lag)
                        cols["mun"].append(rng.choice(nm, c, p=mw))
                        cols["etype"].append(np.full(c, 0 if t in ("B", "C") else 1))
                        cols["cit"].append(np.full(c, pid[HOME] if own else pid[p]))
                        cols["sex"].append(np.full(c, s))
                        age = rng.integers(WL.AGE_LO[a], WL.AGE_HI[a] + 1, c)
                        cols["birth"].append(Y0 + y - age)
                        st = np.full(c, pid[p])
                        if p == ROW and not own:         # a citizen of a state outside the Area comes from or goes anywhere
                            st = np.where(rng.random(c) < 0.8, st, rng.choice(others, c))
                        elif t == "C":                   # a foreign citizen who leaves goes home or leaves the Area
                            st = np.where(rng.random(c) < 0.84, st, pid[ROW])
                        cols["state"].append(st)
    df = pd.DataFrame({k: np.concatenate(v) for k, v in cols.items()})
    df["entered"] = df["move"] + df["lag"]
    assert int(df["entered"].max()) < EXTRACT.toordinal()
    df = df.sort_values(["mun", "entered", "move", "cit", "state", "birth", "sex", "etype"], kind="mergesort").reset_index(drop=True)
    ey = np.array([dt.date.fromordinal(int(o)).year for o in np.unique(df["entered"])])
    ymap = dict(zip(np.unique(df["entered"]), ey))
    df["eyear"] = df["entered"].map(ymap)
    df["seq"] = df.groupby(["mun", "eyear"]).cumcount() + 1
    df["event_no"] = ["%03d/%d/%06d" % (m + 1, y, q) for m, y, q in zip(df["mun"], df["eyear"], df["seq"])]
    iso = {o: dt.date.fromordinal(int(o)).isoformat() for o in np.unique(np.concatenate([df["move"], df["entered"]]))}
    code2 = np.array([WL.CODE2[p] for p in PARTNERS])
    code3 = np.array([WL.CODE3[p] for p in PARTNERS])
    name = np.array(list(PARTNERS))
    st = df["state"].to_numpy()
    blank = old[df["mun"].to_numpy()] & (df["eyear"].to_numpy() < 2016)
    u = rng.random(len(df))
    v = rng.random(len(df))
    text = np.where(v < 0.5, name[st], np.where(v < 0.8, np.char.upper(name[st]), code3[st]))
    out = pd.DataFrame({
        "event_no": df["event_no"],
        "move_date": df["move"].map(iso),
        "entered_on": df["entered"].map(iso),
        "municipality_code": ["M%03d" % (m + 1) for m in df["mun"]],
        "event_type": np.where(df["etype"].to_numpy() == 0, "deregistration_abroad", "registration_from_abroad"),
        "citizenship": code2[df["cit"].to_numpy()],
        "sex": np.where(df["sex"].to_numpy() == 0, "F", "M"),
        "birth_year": df["birth"].to_numpy(),
        "state_code": np.where(blank, "", code2[st]),
        "state_text": np.where(blank | (u < 0.08), text, ""),
    })
    # a municipality's queue sent twice: every event it entered over a few days appears again, unchanged
    ent = df["entered"].to_numpy()
    mun = df["mun"].to_numpy()
    rep = np.zeros(len(df), bool)
    for _ in range(46):
        m = int(rng.choice(nm, p=mw))
        d0 = int(rng.integers(dt.date(2011, 2, 1).toordinal(), dt.date(2026, 12, 1).toordinal()))
        rep |= (mun == m) & (ent >= d0) & (ent < d0 + int(rng.integers(3, 12)))
    out = pd.concat([out, out[rep]]).sort_values(["entered_on", "municipality_code", "event_no"], kind="mergesort")
    return out.reset_index(drop=True), int(rep.sum()), old


def table_rows(WD):
    """The area office's Tables A to D as released each May: a reference year first appears three years on, and a
    state that corrects a table has the whole table for that partner and year published again in a later release."""
    rng = np.random.default_rng([C.SEED, 610])
    rows, revised = [], 0
    for t in WL.TABLES:
        for s in STATES:
            for p in PARTNERS:
                if p == s:
                    continue
                sp = WD["split"][t, s, p]
                for y in range(LAST):
                    first = Y0 + y + 3
                    final = sp[y].astype(int)
                    early = final.copy()
                    again = None
                    if y < LAST - 1 and rng.random() < 0.04:
                        k = int(rng.integers(1, 4))
                        for _ in range(k):
                            i, j = int(rng.integers(0, 2)), int(rng.integers(0, len(WL.AGES)))
                            early[i, j] = max(0, early[i, j] + int(rng.choice([-3, -2, -1, 1, 2, 3])))
                        if not np.array_equal(early, final):
                            again = min(2026, first + int(rng.integers(1, 3)))
                            revised += 1
                    for rel, vals in ((first, early), (again, final)):
                        if rel is None:
                            continue
                        for i, sx in enumerate(WL.SEXES):
                            for j, ag in enumerate(WL.AGES):
                                rows.append(("%d-05" % rel, t, WL.CODE3[s], WL.CODE3[p], Y0 + y, sx, ag, int(vals[i, j])))
    rows.sort(key=lambda r: (r[0], r[1], r[2], r[3], r[4], r[5], WL.AGES.index(r[6])))
    return rows, revised


def _sheet(ws, title, note, header, rows, widths, numfmt="#,##0"):
    ws["A1"] = title
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = note
    ws["A2"].font = Font(italic=True, size=9, color="555555")
    for k, h in enumerate(header):
        c = ws.cell(row=4, column=k + 1, value=h)
        c.font = Font(bold=True)
        c.alignment = Alignment(horizontal="left" if k == 0 else "right", wrap_text=True, vertical="top")
    for r, row in enumerate(rows):
        for k, v in enumerate(row):
            c = ws.cell(row=5 + r, column=k + 1, value=v)
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                c.number_format = numfmt
                c.alignment = Alignment(horizontal="right")
    for k, w in enumerate(widths):
        ws.column_dimensions[chr(65 + k)].width = w
    ws.freeze_panes = "B5"


def write_census(WD, path):
    wb = Workbook()
    wb.remove(wb.active)
    head = ["Reporting state"] + [WL.CODEN[p] for p in PARTNERS] + ["Total"]
    for kind, src in (("T1 citizenship", "census"), ("T2 country of birth", "birthplace")):
        for t, year in ((0, 2011), (10, 2021)):
            rows = []
            for j in STATES:
                vals = []
                for i in PARTNERS:
                    if i == j:
                        v = WD["own"][j, t] if src == "census" else float(np.round(WD["own"][j, t] * 0.985))
                    elif i == ROW:
                        v = WD["other"][j][t] if src == "census" else float(np.round(WD["other"][j][t] * 1.31))
                    else:
                        v = WD[src][i, j, t]
                    vals.append(int(v))
                if src == "birthplace":                  # the same residents by where they were born
                    tot = int(WD["own"][j, t] + sum(WD["census"][i, j, t] for i in STATES if i != j) + WD["other"][j][t])
                    vals[PARTNERS.index(j)] = tot - (sum(vals) - vals[PARTNERS.index(j)])
                rows.append([WL.CODEN[j]] + vals + [sum(vals)])
            ws = wb.create_sheet("%s %d" % (kind, year))
            _sheet(ws, "Table %s. Usual residents on 1 January %d by %s" % (kind[:2], year, kind[3:]),
                   "Census round %d. Persons. Rows: reporting state. Columns: %s. State codes of the Area's numeric "
                   "scheme." % (year, "citizenship" if src == "census" else "country of birth"),
                   head, rows, [16] + [12] * 9 + [13])
    wb.save(path)


def write_c14(WD, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "C-14"
    rows = []
    for i in list(HOSTS) + [ROW]:
        q = WD["c14"][i]
        rows.append([WL.LONG[i] if i != ROW else "Other citizenships", int(q["total"]), int(q["same"]),
                     int(q["elsewhere"]), int(q["abroad"])])
    rows.append(["All foreign citizens"] + [sum(r[k] for r in rows) for k in range(1, 5)])
    _sheet(ws, "Table C-14. Foreign citizens usually resident on 1 January 2021 by citizenship and place of usual "
               "residence on 1 January 2020",
           "Census of Population and Housing 2021, field enumeration, question 14. Persons aged one year or over at "
           "the census.", ["Citizenship", "Usually resident on 1 January 2021", "Same address on 1 January 2020",
                           "Elsewhere in Orlava on 1 January 2020", "Abroad on 1 January 2020"], rows,
           [34, 16, 16, 16, 16])
    for c in ws[5 + len(rows) - 1]:
        c.font = Font(bold=True)
    wb.save(path)


def write_count16(WD, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Citizenship"
    j, t = "Fenmark", 5
    rows = [[WL.LONG[i], int(WD["census"][i, j, t])] for i in STATES if i != j]
    rows.append(["Other citizenships", int(WD["other"][j][t])])
    rows.insert(0, [WL.LONG[j], int(WD["own"][j, 5])])
    rows.append(["All usual residents", sum(r[1] for r in rows)])
    _sheet(ws, "Usual residents of Fenmark on 1 January 2016 by citizenship",
           "Five-yearly population count, enumeration of 1 January 2016. Persons.", ["Citizenship", "Usual residents"],
           rows, [36, 18])
    for c in ws[5 + len(rows) - 1]:
        c.font = Font(bold=True)
    wb.save(path)


def write_estab(WD, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Establishment"
    rows = []
    for h in HOSTS:
        n = int(WD["R"]["host"][h]["n21"])
        rows.append([h, WL.SEAT[h], n, n // 5000 + 1])
    rows.append(["All districts", "", sum(r[2] for r in rows), sum(r[3] for r in rows)])
    _sheet(ws, "Consular establishment in force",
           "Set by the Posting Board on 13 June 2023 on the census counts of 1 January 2021, in force from 1 September "
           "2023 until the establishment for the 2027 to 2029 cycle takes effect.",
           ["District", "Consulate general", "Orlavan citizens usually resident, census of 1 January 2021",
            "Consular officers"], rows, [16, 18, 24, 12])
    for c in ws[5 + len(rows) - 1]:
        c.font = Font(bold=True)
    wb.save(path)


def _csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\r\n")
        w.writerow(header)
        w.writerows(rows)


def build(WD, target):
    counts = {}
    reg, repeats, old = register_rows(WD)
    reg.to_csv(os.path.join(target, FILES["register"]), index=False, lineterminator="\r\n")
    counts["register_rows"], counts["register_repeats"] = len(reg), repeats
    rows, revised = table_rows(WD)
    _csv(os.path.join(target, FILES["tables"]),
         ["release", "table", "reporting_state", "partner", "reference_year", "sex", "age_group", "persons"], rows)
    counts["table_rows"], counts["tables_revised"] = len(rows), revised
    vit = []
    rv = np.random.default_rng([C.SEED, 620])
    for j in STATES:
        for i in PARTNERS:
            if i == j:
                continue
            for y in range(LAST):
                if i == ROW:
                    n = WD["other"][j][0] * (1.0 + 0.012 * y)
                    b, d = int(rv.poisson(n * C.BIRTH)), int(rv.poisson(n * C.DEATH))
                else:
                    b, d = int(WD["births"][i, j][y]), int(WD["deaths"][i, j][y])
                vit.append((WL.CODE3[j], WL.CODE3[i], Y0 + y, b, d))
    _csv(os.path.join(target, FILES["vital"]), ["reporting_state", "citizenship", "reference_year", "live_births", "deaths"], vit)
    write_census(WD, os.path.join(target, FILES["census"]))
    write_c14(WD, os.path.join(target, FILES["c14"]))
    write_count16(WD, os.path.join(target, FILES["count16"]))
    write_estab(WD, os.path.join(target, FILES["estab"]))
    _csv(os.path.join(target, FILES["codes"]), ["area_code", "alpha3", "register_code", "name", "official_name"],
         [(WL.CODEN[p], WL.CODE3[p], WL.CODE2[p], p, WL.LONG[p]) for p in PARTNERS])
    rm = np.random.default_rng([C.SEED, 630])
    _csv(os.path.join(target, FILES["muni"]), ["municipality_code", "municipality", "region", "register_office_opened"],
         [("M%03d" % (k + 1), m, REGIONS[int(rm.integers(0, len(REGIONS)))] if k else REGIONS[0],
           int(rm.integers(1994, 2009))) for k, m in enumerate(WL.MUNICIPALITIES)])
    _csv(os.path.join(target, FILES["pop"]), ["state", "reference_date", "usual_residents"],
         [(WL.CODE3[j], "%d-01-01" % (Y0 + t), int(WD["pop_total"][j][t])) for j in STATES for t in range(16)])
    rt = np.random.default_rng([C.SEED, 640])
    traffic = []
    for h in HOSTS:
        base = {"air": rt.uniform(40, 420), "rail": rt.uniform(15, 260), "coach": rt.uniform(10, 120)}
        for y in range(NY):
            for qn in range(4):
                for mode, b in base.items():
                    season = (0.8, 1.05, 1.35, 0.9)[qn]
                    v = b * (1.0 + 0.025 * y) * season * rt.lognormal(0, 0.05)
                    arr = v * rt.uniform(0.97, 1.03)
                    traffic.append(("%dQ%d" % (Y0 + y, qn + 1), WL.CODE3[h], mode, round(arr, 1), round(v, 1)))
    _csv(os.path.join(target, FILES["traffic"]),
         ["quarter", "partner_state", "mode", "passengers_arriving_thousands", "passengers_departing_thousands"], traffic)
    counts["municipalities_old_software"] = int(old.sum())
    return counts
