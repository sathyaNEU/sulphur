"""task3 architecture 4: the data files of the pack, cut from the truth with the mess each system really makes."""
import csv
import datetime as dt
import io
import math

import numpy as np
import openpyxl
from openpyxl.styles import Font

import ooxml
import params as P
import world as W

AS_OF = dt.date(*P.ASOF)


def _csv(path, header, rows):
    buf = io.StringIO()
    w = csv.writer(buf, lineterminator="\r\n")
    w.writerow(header)
    w.writerows(rows)
    open(path, "w", newline="", encoding="utf-8").write(buf.getvalue())
    return len(rows)


def dec(d):
    """decimal year of a date"""
    y0 = dt.date(d.year, 1, 1)
    return d.year + (d - y0).days / (dt.date(d.year + 1, 1, 1) - y0).days


def at(series, d):
    t = dec(d)
    return float(np.interp(t, W.TG, series))


# ---------------------------------------------------------------- identifiers
def assign_ids(truth, rng):
    """assessor parcel numbers (township-section-parcel), network site IDs, and the assessor's re-numbering"""
    used = set()

    def pid(twp):
        while True:
            s = "%02d-%03d-%04d" % (twp, int(rng.integers(1, 37)), int(rng.integers(1, 9800)))
            if s not in used:
                used.add(s)
                return s
    for p in truth["parcels"]:
        p["pid"] = pid(14 if p["zone"] in ("W3", "W5") else 15)
        p["old_pid"] = None
    # the ridge tract was re-numbered when Hartvale Produce bought it from the paper company in 2015
    for p in truth["parcels"]:
        if p["kind"] in ("ridge",):
            p["old_pid"] = pid(15)
    # three plain parcels split by the assessor in 2012: the panel carries the parent number to 2011
    plain = [p for p in truth["parcels"] if p["kind"] == "plain"]
    for k in rng.choice(len(plain), 3, replace=False):
        plain[int(k)]["old_pid"] = pid(14)
    n = list(range(1, 90))
    rng.shuffle(n)
    for s, k in zip(truth["sites"], sorted(n[:len(truth["sites"])])):
        s["sid"] = "TCGW-%03d" % k
        s["pid"] = pid(int(rng.choice([12, 13, 14, 15, 16, 17])))
        s["old_pid"] = None
    # two network wells rebuilt in 2011 under new numbers
    for s in [truth["sites"][7], truth["sites"][40]]:
        s["sid_old"] = s["sid"]
        s["sid"] = s["sid"] + "R"
        s["rebuilt"] = dt.date(2011, 6, int(rng.integers(6, 24)))


# ---------------------------------------------------------------- land cover panel
LOCAL = {"FOR": ["F1", "F2"], "GRS": ["G1", "G2"], "DRY": ["A1", "A2"], "IRC": ["A3"], "IRV": ["A4"],
         "RES": ["U1"], "WAT": ["W"]}
NEWC = {"FOR": [141, 142], "GRS": [176, 37], "DRY": [24, 36], "IRC": [301], "IRV": [304], "RES": [121], "WAT": [111]}
LEGEND = [
    ("F1", "1986-2007", "Forest, deciduous"), ("F2", "1986-2007", "Forest, coniferous and plantation"),
    ("G1", "1986-2007", "Grassland, pasture, idle"), ("G2", "1986-2007", "Conservation reserve grass"),
    ("A1", "1986-2007", "Cropland, not irrigated"), ("A2", "1986-2007", "Hay and alfalfa, not irrigated"),
    ("A3", "1986-2007", "Irrigated cropland, corn and soybean rotation"),
    ("A4", "1986-2007", "Irrigated cropland, vegetable rotation (potato, sweet corn, snap bean)"),
    ("U1", "1986-2007", "Residential and farmstead"), ("W", "1986-2007", "Open water, wetland"),
    ("141", "2008-", "Deciduous forest"), ("142", "2008-", "Evergreen forest and plantation"),
    ("176", "2008-", "Grassland and pasture"), ("37", "2008-", "Other hay and conservation grass"),
    ("24", "2008-", "Cropland, not irrigated"), ("36", "2008-", "Alfalfa, not irrigated"),
    ("301", "2008-", "Irrigated corn and soybean rotation"),
    ("304", "2008-", "Irrigated vegetable rotation (potato, sweet corn, snap bean, field corn)"),
    ("121", "2008-", "Developed, residential and farmstead"), ("111", "2008-", "Open water and wetland"),
]


def land_cover(path, truth, rng):
    rows = []
    allp = [(p, "whpa") for p in truth["parcels"]] + [(s, "network") for s in truth["sites"]]
    variant = {}
    for p, _ in allp:
        for c in P.CLASSES:
            variant[(id(p), c)] = (LOCAL[c][int(rng.integers(len(LOCAL[c])))], NEWC[c][int(rng.integers(len(NEWC[c])))])
    for p, src in allp:
        for y in P.YEARS:
            c = p["hist"][y]
            lo, nw = variant[(id(p), c)]
            code = lo if y < 2008 else str(nw)
            source = "LWCD inventory" if y < 2008 else "LWCD from cropland layer"
            pid = p["pid"]
            parent = ""
            if p.get("old_pid"):
                if p["kind"] == "ridge" and y < 2015:
                    pid = p["old_pid"]
                elif p["kind"] == "plain" and y < 2012:
                    pid = p["old_pid"]
                elif p["kind"] in ("ridge", "plain"):
                    parent = p["old_pid"]
            rows.append([pid, y, code, source, parent])
    order = sorted(range(len(rows)), key=lambda i: (rows[i][0], rows[i][1]))
    rows = [rows[i] for i in order]
    # the 2016 file was exported twice for one township and both copies were kept
    dup = [r for r in rows if r[1] == 2016 and r[0].startswith("15-")]
    rows += dup[: len(dup) // 3]
    rows.sort(key=lambda r: (r[0], r[1]))
    return _csv(path, ["parcel_id", "year", "land_cover_code", "source", "parent_parcel_id"], rows)


# ---------------------------------------------------------------- laboratory helpers
def _lab(d):
    return ("Ravell County Health Department Laboratory", "Nitrate", "mg/L as NO3", 0.5) if d.year < 2004 else \
        ("Pellow Analytical Services", "Nitrate+Nitrite as N", "mg/L", 0.10)


def _report(c_n, d, rng):
    """a laboratory result for a true nitrate-N concentration c_n on date d: (result text, units, qualifier, RL)"""
    lab, analyte, unit, rl = _lab(d)
    val = c_n * (1 + rng.normal(0, 0.03)) + rng.normal(0, 0.03)
    if unit == "mg/L as NO3":
        val *= P.NO3_PER_N
        txt = "%.1f" % val if val >= rl else "<%.1f" % rl
    else:
        txt = "%.2f" % val if val >= rl else "<%.2f" % rl
    return lab, analyte, unit, txt, ("" if not txt.startswith("<") else "U"), rl


def _sample_day(y, m, rng, lo=3, hi=26):
    d = dt.date(y, m, int(rng.integers(lo, hi)))
    while d.weekday() > 4:
        d += dt.timedelta(days=1)
    return d


# ---------------------------------------------------------------- the utility's results
def point_name(w, d):
    return ("WELL %s" % w[1:]) if d < dt.date(2014, 4, 1) else ("HR-W%02d" % int(w[1:]))


def utility_results(path, truth, pump, rng):
    rows = []
    sid = [880000]

    def add(point, d, c, extra=""):
        lab, an, un, txt, q, rl = _report(c, d, rng)
        sid[0] += int(rng.integers(3, 40))
        rows.append(["WX%07d" % sid[0], point, d.isoformat(), lab, an, txt, un, q, ("%g" % rl), extra])
        return rows[-1]
    for w in P.WELLS:
        y0 = max(1988, P.WELL_DRILLED[w])
        for y in range(y0, 2027):
            for m in (2, 5, 8, 11):
                d = _sample_day(y, m, rng)
                if d >= AS_OF or (y == 1996 and w == "W7" and m < 8):
                    continue
                if rng.random() < 0.04:
                    continue
                short = 1 + rng.normal(0, 0.035)
                c = at(truth["wells"][w], d) * short
                r = add(point_name(w, d), d, c)
                if rng.random() < 0.035:      # field duplicate
                    lab, an, un, txt, q, rl = _report(c, d, rng)
                    rows.append([r[0] + "-D", r[1], r[2], lab, an, txt, un, q, ("%g" % rl), "field duplicate"])
                if rng.random() < 0.012:      # laboratory re-run
                    lab, an, un, txt, q, rl = _report(c, d, rng)
                    rows.append([r[0], r[1], r[2], lab, an, txt, un, q, ("%g" % rl), "re-run, QC"])
    # entry point, monthly from 2012
    for y in range(2012, 2027):
        for m in range(1, 13):
            d = _sample_day(y, m, rng, 4, 20)
            if d >= AS_OF:
                continue
            c = pump["blend_at"](d) * (1 + rng.normal(0, 0.02))
            add("EP-01", d, c)
    rows.sort(key=lambda r: (r[2], r[1]))
    return _csv(path, ["sample_id", "sample_point", "collected", "laboratory", "analyte", "result", "units",
                       "qualifier", "reporting_limit", "remarks"], rows)


# ---------------------------------------------------------------- pumping
def pumping(truth, rng):
    """daily pumping by well 2009-01-01 to 2026-10-31 and the blend it makes"""
    days = []
    d = dt.date(2009, 1, 1)
    while d <= dt.date(2026, 10, 31):
        days.append(d)
        d += dt.timedelta(days=1)
    vol = {w: np.zeros(len(days)) for w in P.WELLS}
    drift = {w: 1.0 for w in P.WELLS}
    for i, d in enumerate(days):
        doy = d.timetuple().tm_yday
        season = 1 + 0.28 * math.exp(-((doy - 205) / 38.0) ** 2)
        grow = 1 + 0.006 * (d.year - 2009)
        total = P.FIELD_MGD * 1e6 * 0.93 * season * grow * (1 + rng.normal(0, 0.04))
        if doy == 1:
            for w in P.WELLS:
                drift[w] = float(np.clip(rng.normal(1.0, 0.08), 0.8, 1.2))
        sh = {w: P.HIST_SHARE[w] * drift[w] for w in P.WELLS}
        if d.year == 2013 and 150 < doy < 240:     # Well 3's pump replaced
            sh["W3"] = 0.0
        s = sum(sh.values())
        for w in P.WELLS:
            vol[w][i] = total * sh[w] / s * (1 + rng.normal(0, 0.03))
    dts = np.array([dec(x) for x in days])

    def blend_at(day):
        k = (day - days[0]).days
        if k < 0 or k >= len(days):
            sh = P.HIST_SHARE
            return sum(sh[w] * at(truth["wells"][w], day) for w in P.WELLS)
        num = sum(vol[w][k] * at(truth["wells"][w], day) for w in P.WELLS)
        return num / sum(vol[w][k] for w in P.WELLS)
    return dict(days=days, vol=vol, dts=dts, blend_at=blend_at)


def pumping_csv(path, pump, rng):
    rows = []
    for i, d in enumerate(pump["days"]):
        for w in P.WELLS:
            v = pump["vol"][w][i]
            name = point_name(w, d)
            if d.year == 2013 and w == "W3" and v == 0:
                rows.append([d.isoformat(), name, "0", "gal", "0.0", "OUT OF SERVICE"])
                continue
            hours = min(24.0, v / (P.FIELD_MGD * 1e6 * P.HIST_SHARE[w] * 1.9 / 24.0))
            if rng.random() < 0.002:
                rows.append([d.isoformat(), name, "", "", "", "NO DATA"])
                continue
            if d >= dt.date(2019, 3, 12):
                rows.append([d.isoformat(), name, "%.1f" % (v / 1000.0), "kgal", "%.1f" % hours, ""])
            else:
                rows.append([d.isoformat(), name, "%d" % round(v), "gal", "%.1f" % hours, ""])
    # the export for the week of 6 June 2022 was appended twice
    extra = [r for r in rows if "2022-06-06" <= r[0] <= "2022-06-12"]
    rows += extra
    rows.sort(key=lambda r: (r[0], r[1]))
    return _csv(path, ["date", "well", "volume", "volume_units", "run_hours", "status"], rows)


# ---------------------------------------------------------------- the county network
def network_samples(path, truth, rng):
    rows = []
    for s in truth["sites"]:
        inst = s.setdefault("installed", int(rng.choice([1988, 1989, 1989, 1990, 1990, 1990])))
        for y in range(max(1990, inst), 2027):
            months = (5, 10) if y not in (2009, 2010) else (10,)
            for m in months:
                d = _sample_day(y, m, rng)
                if d >= AS_OF or rng.random() < 0.03:
                    continue
                sid = s["sid"]
                if s.get("sid_old"):
                    if d < s["rebuilt"]:
                        sid = s["sid_old"]
                    elif y == 2011 and m == 5:
                        continue
                c = at(s["c"], d) * (1 + rng.normal(0, 0.045))
                lab, an, un, txt, q, rl = _report(c, d, rng)
                do = max(0.3, rng.normal(8.4, 0.9))
                sc = 90 + 32 * c + rng.normal(0, 25)
                tc = 9.0 + rng.normal(0, 0.5) + (0.6 if m == 10 else 0)
                wl = s["dtw"] + rng.normal(0, 1.2) + (0.8 if m == 10 else -0.4)
                rows.append([sid, d.isoformat(), txt, un, an, lab, q, "%.1f" % do, "%d" % sc, "%.1f" % tc,
                             "%.2f" % wl, str(rng.choice(["CB", "CB", "DS", "LW"]) if y >= 2006 else
                                              rng.choice(["JK", "RT", "RT"]))])
                if rng.random() < 0.02:
                    rows.append(rows[-1][:])
    rows.sort(key=lambda r: (r[0], r[1]))
    return _csv(path, ["site_id", "sample_date", "nitrate_result", "units", "analyte", "laboratory", "qualifier",
                       "dissolved_oxygen_mg_L", "specific_conductance_uS_cm", "temperature_C",
                       "depth_to_water_ft", "sampler"], rows)


def _book(path, sheets, created, modified, company):
    wb = openpyxl.Workbook()
    wb.remove(wb.active)
    for name, header, rows, widths in sheets:
        ws = wb.create_sheet(name)
        ws.append(header)
        for c in ws[1]:
            c.font = Font(bold=True)
        for r in rows:
            ws.append(r)
        for i, wdt in enumerate(widths):
            ws.column_dimensions[openpyxl.utils.get_column_letter(i + 1)].width = wdt
        ws.freeze_panes = "A2"
    wb.properties.creator = company
    wb.properties.lastModifiedBy = company
    wb.save(path)
    ooxml.normalize(path, created, modified, company)


def network_sites(path, truth, rng):
    rows = []
    for s in sorted(truth["sites"], key=lambda s: s["sid"]):
        inst = s["installed"]
        idate = dt.date(inst, int(rng.integers(4, 10)), int(rng.integers(2, 27)))
        top = s["dtw"] - float(rng.uniform(2.0, 4.0))
        note = ""
        status = "active"
        if s.get("sid_old"):
            note = "replaces %s (casing failure), rebuilt %s on the same parcel" % (s["sid_old"], s["rebuilt"].isoformat())
        elev = 1050 + rng.uniform(-30, 90) + s["dtw"] * 0.6
        rows.append([s["sid"], s["pid"], idate.isoformat(), round(elev, 1), round(top + 10.0 + 2.0, 1),
                     round(top, 1), round(top + 10.0, 1), round(s["dtw"], 1), status, note])
    for s in truth["sites"]:
        if s.get("sid_old"):
            rows.append([s["sid_old"], s["pid"], dt.date(s["installed"], 5, 14).isoformat(), "", "", "", "",
                         round(s["dtw"], 1), "abandoned %s" % s["rebuilt"].isoformat(), "replaced by %s" % s["sid"]])
    rows.sort(key=lambda r: r[0])
    created = dt.datetime(2026, 1, 12, 15, 2)
    _book(path, [("Sites", ["site_id", "parcel_id", "installed", "land_surface_elev_ft", "well_depth_ft",
                            "screen_top_ft", "screen_bottom_ft", "mean_depth_to_water_ft", "status", "notes"], rows,
                  [12, 14, 11, 12, 10, 10, 11, 12, 18, 54]),
                 ("Land cover codes", ["code", "years used", "description"], [list(x) for x in LEGEND], [8, 12, 70])],
          created, dt.datetime(2026, 10, 21, 13, 40), "Ravell County Land and Water Conservation Department")
    return len(rows)


def age_survey(path, truth, rng):
    """the 2019 tritium-helium survey: 24 network wells and the four production wells"""
    rows = []
    pick = [s for s in truth["sites"]]
    rng.shuffle(pick)
    lam = math.log(2) / 12.32
    for s in sorted(pick[:24], key=lambda s: s["sid"]):
        age = max(0.1, s["age"] + rng.normal(0, 0.15))
        h3 = 6.1 + rng.normal(0, 0.4)
        he = h3 * (math.exp(lam * age) - 1)
        rows.append([s["sid"], dt.date(2019, 7, int(rng.integers(8, 26))).isoformat(), round(h3, 2), round(he, 2),
                     round(age, 1), "water-table well"])
    for w in P.WELLS:
        ps = [p for p in truth["parcels"] if p["zone"] == w]
        wt = np.array([p["acres"] * P.RECHARGE[p["hist"][2019]] for p in ps])
        T = np.array([p["T"] for p in ps])
        mix = float(np.sum(wt * T) / wt.sum())
        age = mix * 0.82 + rng.normal(0, 0.3)
        h3 = 6.0 + rng.normal(0, 0.4)
        he = h3 * (math.exp(lam * age) - 1)
        rows.append(["Corlinden " + P.WELL_NAMES[w], dt.date(2019, 8, int(rng.integers(5, 20))).isoformat(),
                     round(h3, 2), round(he, 2), round(age, 1), "production well, raw tap, pump running"])
    _book(path, [("Results", ["site", "sampled", "tritium_TU", "tritiogenic_he3_TU", "apparent_age_yr", "notes"], rows,
                  [22, 11, 11, 16, 15, 38]),],
          dt.datetime(2020, 2, 3, 9, 15), dt.datetime(2020, 2, 3, 9, 15), "Ravell County Land and Water Conservation Department")
    return len(rows)


# ---------------------------------------------------------------- distractors
def specific_capacity(path, rng):
    rows = []
    for w in P.WELLS:
        sc0 = {"W3": 41.0, "W5": 63.0, "W6": 58.0, "W7": 70.0}[w]
        for y in range(2008, 2027, 2):
            d = dt.date(y, int(rng.integers(3, 6)), int(rng.integers(2, 27)))
            rate = {"W3": 650, "W5": 900, "W6": 900, "W7": 950}[w] + int(rng.integers(-40, 40))
            sc = sc0 * (1 - 0.012 * (y - 2008)) * (1 + rng.normal(0, 0.04))
            if w == "W3" and y >= 2016:
                sc *= 0.86
            dd = rate / sc
            rows.append([P.WELL_NAMES[w], d.isoformat(), rate, round(dd, 1), round(sc, 1),
                         "after rehabilitation" if (w == "W5" and y == 2018) else ""])
    _book(path, [("Tests", ["well", "test_date", "rate_gpm", "drawdown_ft", "specific_capacity_gpm_ft", "remarks"],
                  rows, [10, 11, 9, 11, 22, 24])],
          dt.datetime(2026, 5, 4, 10, 0), dt.datetime(2026, 5, 4, 10, 0), "Corlinden Water Utility")
    return len(rows)


def fertilizer_sales(path, rng):
    rows = []
    for y in range(1990, 2026):
        base = 9800 * (1 + 0.012 * (y - 1990)) if y < 1998 else 10700 * (1 - 0.035 * min(y - 1998, 7))
        if y >= 2005:
            base = 10700 * (1 - 0.035 * 7) * (1 + 0.004 * (y - 2005))
        for prod, sh in [("Anhydrous ammonia", 0.18), ("Urea", 0.27), ("UAN solutions", 0.31),
                         ("Ammonium sulfate", 0.07), ("Ammonium nitrate", 0.05), ("Other N blends", 0.12)]:
            rows.append([y, prod, round(base * sh * (1 + rng.normal(0, 0.05)), 0), "tons N",
                         "reported to the state" if y >= 1995 else "dealer survey"])
    return _csv(path, ["year", "product", "nitrogen_sold", "units", "basis"], rows)


CLASS_DESC = {"FOR": "forest", "GRS": "grass and pasture", "DRY": "cropland, not irrigated",
              "IRC": "irrigated corn and soybean", "IRV": "irrigated vegetables", "RES": "residential",
              "WAT": "wetland"}


def whpa_attributes(path, truth, rng):
    rows = []
    for p in sorted(truth["parcels"], key=lambda p: (p["zone"], p["pid"])):
        owner = "City of Corlinden" if p["kind"] == "ridge_woods" else ("Hartvale Produce LLC" if p["kind"] == "ridge"
                                                                       else "private")
        rows.append([p["pid"], round(p["acres"], 1), P.WELL_NAMES[p["zone"]], int(round(p["dtw"])),
                     round(p["T"], 1), CLASS_DESC[p["hist"][2018]], owner])
    wb = [[CLASS_DESC[c], P.RECHARGE[c]] for c in P.CLASSES if c != "WAT"]
    _book(path, [("Parcels", ["parcel_id", "acres", "zone", "depth_to_water_ft", "gw_time_of_travel_yr",
                              "land_cover_2018", "owner"], rows, [14, 8, 9, 16, 20, 28, 20]),
                 ("Recharge", ["land_cover", "recharge_in_per_yr"], wb, [30, 18])],
          dt.datetime(2019, 11, 12, 14, 31), dt.datetime(2019, 11, 14, 9, 5), "Fenwright Hydrogeologic")
    return len(rows)
