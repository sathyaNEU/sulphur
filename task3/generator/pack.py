"""Write task3's evidence pack from the seeded world: the rain gauge's daily record, the creek gauge's annual peaks,
its peaks above base and its daily mean flows, the county's stormwater parcels, the cross sections and the grab
samples. docs.py writes the drainage standard, the culvert alternatives and the 2024 inspection."""
import csv
import datetime as dt
import os

import numpy as np

import common as K
import world as W

RG_OLD, RG_NEW = "TAM-RG-01", "TAM-RG-02"          # the rain gauge before and after its 1987 move
MOVE_START, MOVE_END = dt.date(1987, 4, 15), dt.date(1987, 6, 14)
SITE = "0209417500"                                  # the county's creek gauge number in the state cooperative list
POT_BASE = 50                                       # cfs, the peaks-above-base threshold the gauge reports


def stage_ft(q):
    """Gage height from the rating (the control is the old culvert's apron)."""
    return 1.35 + 0.118 * float(q) ** 0.49


def sig3(q):
    """Peaks are published to three significant figures (two under 100 cfs)."""
    q = float(q)
    if q < 100:
        return int(round(q))
    p = 10 ** (int(np.floor(np.log10(q))) - 2)
    return int(round(q / p) * p)


def write_rain(path, w, r):
    """The rain gauge's daily record as the county's climate office exports it: one row per station-day, the gauge
    moved in 1987 with two months on both sites, observer weekends accumulated into Monday's reading through 1978,
    trace days, and a few missed days."""
    rows = []
    rain = w.rain.copy()
    for i, d in enumerate(w.days):
        v = round(float(rain[i]), 2)
        st = RG_OLD if d < MOVE_END else RG_NEW
        flag = ""
        if v == 0 and r.random() < 0.035:
            flag = "T"
        rows.append([st, d.isoformat(), v, flag])
    # weekend accumulations through 1978: Saturday and Sunday read on Monday
    for i, d in enumerate(w.days):
        if d.year <= 1978 and d.weekday() == 0 and i >= 2 and r.random() < 0.55:
            tot = round(rows[i - 2][2] + rows[i - 1][2] + rows[i][2], 2)
            if rows[i - 2][2] + rows[i - 1][2] > 0:
                rows[i - 2][2], rows[i - 2][3] = None, "A"
                rows[i - 1][2], rows[i - 1][3] = None, "A"
                rows[i][2], rows[i][3] = tot, "A3"
    # missed days, the reading lost (not on storm days)
    for i in r.choice(len(rows), 41, replace=False):
        if rows[i][2] is not None and rows[i][2] < 0.3:
            rows[i][2], rows[i][3] = None, "M"
    # the new site's overlap months: both gauges read
    extra = []
    for i, d in enumerate(w.days):
        if MOVE_START <= d < MOVE_END:
            v = rows[i][2]
            if v is not None:
                v2 = round(max(0.0, v * float(np.exp(r.normal(0, 0.06))) if v > 0 else 0.0), 2)
                extra.append([RG_NEW, d.isoformat(), v2, ""])
    rows += extra
    rows.sort(key=lambda x: (x[1], x[0]))
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["station_id", "date", "precip_in", "mflag"])
        for st, d, v, f in rows:
            wr.writerow([st, d, "" if v is None else "%.2f" % v, f])
    return len(rows)


def write_peaks(path, w, r):
    """The gauge's annual peak flows by water year (October to September), as the county's hydrologic data unit
    publishes them: three significant figures, the gage height, a code where the peak is estimated."""
    n = 0
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["site_no", "water_year", "peak_date", "peak_time", "peak_cfs", "gage_height_ft", "peak_code"])
        for y in range(K.YEAR0, K.YEAR1 + 1):
            e = w.annual[y]
            hh = int(e["hour"]); mm = int((e["hour"] - hh) * 60) // 15 * 15
            code = "E" if e["kind"] == "none" else ("2" if r.random() < 0.05 else "")
            wr.writerow([SITE, y, e["date"].isoformat(), "%02d:%02d" % (hh, mm), sig3(e["peak"]),
                         "%.2f" % stage_ft(e["peak"]), code])
            n += 1
    return n


def write_pot(path, w, r):
    """Every independent peak above the 50 cfs base, as the gauge's peak-above-base listing carries it; the 2009 and
    2010 water years were exported twice when the unit moved databases, and some peaks carry the estimate code."""
    rows = []
    for e in w.events:
        y = W.water_year(e["date"])
        if not (K.YEAR0 <= y <= K.YEAR1) or e["peak"] < POT_BASE:
            continue
        hh = int(e["hour"]); mm = int((e["hour"] - hh) * 60) // 15 * 15
        code = "2" if r.random() < 0.04 else ""
        rows.append([SITE, y, e["date"].isoformat(), "%02d:%02d" % (hh, mm), sig3(e["peak"]),
                     "%.2f" % stage_ft(e["peak"]), code])
    dup = [list(x) for x in rows if x[1] in (2009, 2010)]
    rows += dup
    rows.sort(key=lambda x: (x[2], x[3]))
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["site_no", "water_year", "peak_date", "peak_time", "peak_cfs", "gage_height_ft", "peak_code"])
        wr.writerows(rows)
    return len(rows)


def write_flow(path, w, r):
    """Daily mean discharge as the gauge's data unit exports it: approved through September 2024, provisional after,
    estimated days, ice and equipment-malfunction days without a value."""
    n = 0
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["agency_cd", "site_no", "datetime", "discharge_cfs", "qualifier"])
        for i, d in enumerate(w.days):
            q = float(w.flow[i])
            qual = "A" if d < dt.date(2024, 10, 1) else "P"
            val = "%.3g" % q
            u = r.random()
            if d.month in (1, 2) and u < 0.004:
                val, qual = "", qual + " Ice"
            elif u < 0.002:
                val, qual = "", qual + " Eqp"
            elif u < 0.012:
                qual = qual + " e"
            wr.writerow(["TCO", SITE, d.isoformat(), val, qual])
            n += 1
    return n


def write_parcels(path, w, r):
    """The county stormwater utility's billing parcels with the impervious area each carries and the year it was
    built, every basin in the county; parcels were renumbered at the 2004 reassessment and 37 split parcels are still
    carried under both numbers."""
    from openpyxl import Workbook
    basin_sqft = K.AREA_ACRES * 43560.0
    years = np.arange(1940, K.YEAR1 + 1)
    target = W.imp_frac(np.maximum(years, K.YEAR0)) * basin_sqft
    target[years < K.YEAR0] = np.linspace(0.3, 1.0, (years < K.YEAR0).sum()) * W.imp_frac(K.YEAR0) * basin_sqft
    adds = np.diff(np.concatenate([[0.0], target]))
    uses = [("SFR", 4200, 900), ("SFR", 5200, 1200), ("TH", 3100, 600), ("COM", 38000, 22000), ("INS", 61000, 30000),
            ("MFR", 24000, 9000)]
    rows = []
    pin = 11000
    for y, add in zip(years, adds):
        left = add
        while left > 0:
            if y < 1975:
                use = uses[0] if r.random() < 0.8 else uses[3]
            else:
                use = uses[int(r.choice(6, p=[0.36, 0.22, 0.14, 0.12, 0.04, 0.12]))]
            sq = max(400.0, float(r.normal(use[1], use[2])))
            sq = min(sq, left) if left < 400 else sq
            left -= sq
            pin += int(r.integers(3, 40))
            rows.append({"basin": "OLL", "use": use[0], "imp": int(round(sq)), "year": int(y), "pin": pin})
    # the county's other basins on the same bill
    for b, n in (("FEN", 2600), ("CRK", 1900), ("LTL", 1400)):
        for _ in range(n):
            pin += int(r.integers(3, 40))
            y = int(np.clip(r.normal(1995, 14), 1940, 2025))
            u = uses[int(r.choice(6, p=[0.4, 0.2, 0.14, 0.12, 0.04, 0.1]))]
            rows.append({"basin": b, "use": u[0], "imp": int(max(400, r.normal(u[1], u[2]))), "year": y, "pin": pin})
    order = r.permutation(len(rows))
    rows = [rows[i] for i in order]
    wb = Workbook()
    ws = wb.active
    ws.title = "billing_parcels"
    ws.append(["pin", "prior_pin", "basin_code", "land_use", "impervious_sqft", "impervious_year", "eru"])
    split = set(r.choice(len(rows), 37, replace=False).tolist())
    old_ids = r.permutation(np.arange(10000, 10000 + 3 * len(rows)))[:len(rows)]
    for k, x in enumerate(rows):
        newpin = "%07d" % (x["pin"] + 3000000)
        prior = "T-%05d" % old_ids[k] if x["year"] < 2004 else ""
        ws.append([newpin, prior, x["basin"], x["use"], x["imp"], x["year"], round(x["imp"] / 2800, 1)])
        if k in split and x["year"] < 2004:          # carried under the old number too after the reassessment
            ws.append(["", prior, x["basin"], x["use"], x["imp"], x["year"],
                       round(x["imp"] / 2800, 1)])
    ws2 = wb.create_sheet("basins")
    ws2.append(["basin_code", "basin_name", "drainage_area_sq_mi", "outlet"])
    ws2.append(["OLL", "Ollery Creek", K.AREA_SQMI, "Kinnard Road"])
    ws2.append(["FEN", "Fenner Branch", 6.8, "Hollis Mill Road"])
    ws2.append(["CRK", "Crooked Run", 9.2, "US 15 crossing"])
    ws2.append(["LTL", "Little Ollery Creek", 3.1, "confluence with Ollery Creek below Kinnard Road"])
    import datetime as _dt
    wb.properties.creator = "Tamsett County Stormwater Utility"
    wb.properties.lastModifiedBy = "Tamsett County Stormwater Utility"
    wb.properties.created = _dt.datetime(2026, 1, 6, 8, 12)
    wb.properties.modified = _dt.datetime(2026, 1, 6, 8, 12)
    wb.save(path)
    return len(rows)


def write_survey(path, r):
    """The 2023 cross sections of the Kinnard Road reach, surveyed for the replacement's hydraulic model."""
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["section", "river_station_ft", "point", "offset_ft", "elevation_ft", "description"])
        for k, st in enumerate((310, 180, 60, -45, -160, -290)):
            for j, off in enumerate(np.arange(0, 241, 8)):
                z = 412.0 - 0.0021 * st + (0.0006 * (off - 120) ** 2 if abs(off - 120) > 18 else -5.6 + 0.05 * abs(off - 120))
                wr.writerow(["XS-%d" % (k + 1), st, j + 1, int(off), "%.2f" % (z + r.normal(0, 0.08)),
                             "bank" if abs(off - 120) in (18, 20) else ("channel" if abs(off - 120) < 18 else "overbank")])


def write_quality(path, r):
    """The county's grab samples at Kinnard Road (turbidity, nutrients), 2019 to 2025."""
    with open(path, "w", newline="") as fh:
        wr = csv.writer(fh, lineterminator="\n")
        wr.writerow(["sample_id", "date", "time", "turbidity_ntu", "nitrate_mg_l", "total_p_mg_l", "e_coli_mpn", "notes"])
        d = dt.date(2019, 1, 9)
        k = 1
        while d < dt.date(2025, 12, 20):
            wet = r.random() < 0.18
            wr.writerow(["OLL-%04d" % k, d.isoformat(), "%02d:%02d" % (int(r.integers(8, 15)), int(r.choice([0, 15, 30, 45]))),
                         "%.1f" % (r.gamma(2, 30 if wet else 4)), "%.2f" % r.gamma(3, 0.25), "%.3f" % r.gamma(2, 0.04),
                         int(r.gamma(1.2, 900 if wet else 140)), "storm sample" if wet else ""])
            d += dt.timedelta(days=int(r.integers(12, 20)))
            k += 1


def write_pack(out, w=None):
    import docs as D
    w = w or W.World(K.SEED)
    r = np.random.default_rng(K.SEED + 101)
    p = lambda k: os.path.join(out, K.FILES[k])
    n = {"rain": write_rain(p("rain"), w, r), "peaks": write_peaks(p("peaks"), w, r), "pot": write_pot(p("pot"), w, r),
         "flow": write_flow(p("flow"), w, r), "parcels": write_parcels(p("parcels"), w, r)}
    write_survey(p("survey"), r)
    write_quality(p("quality"), r)
    D.write_docs(out, w)
    return w, n
