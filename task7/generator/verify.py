"""task7 architecture 8: the independent verifier. It reads only the pack under target/, rebuilds every building's normal-weather gas
use season by season the way the utility's benchmarking method sets out, and hands the result to golden.py; checks.py
asserts that the figures it yields are the golden's."""
import csv
import datetime as dt
import math
import os
import sys
from collections import defaultdict

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD  # noqa: E402

HW = {"office": 0.08, "retail": 0.06, "hotel": 0.30, "workshop": 0.05, "care home": 0.25, "restaurant": 0.35}
TYPES = ["office", "retail", "hotel", "workshop", "care home", "restaurant"]


def d_(s):
    return dt.date(*map(int, s.split("-")))


def season_of(d):
    return d.year + 1 if d.month >= 5 else d.year


def rows(path):
    with open(path, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def sheet(path):
    ws = load_workbook(path, read_only=True).active
    it = ws.iter_rows(values_only=True)
    head = next(it)
    return [dict(zip(head, r)) for r in it]


def load(target, pro_rate=True, estimates="as filed", threshold=0.5, outbuildings="kept"):
    """season x building normal-weather use (kWh), and the pilot and 2026 tables, as a golden.Panel"""
    reg = sheet(os.path.join(target, "buildings_register_2026.xlsx"))
    bidx = {r["building_id"]: k for k, r in enumerate(reg)}
    use = [r["use"] for r in reg]
    N = len(reg)
    temps = {d_(r["date"]): float(r["mean_temperature_c"]) for r in rows(os.path.join(target, "weather_haldenau_daily_2013_2026.csv"))}
    dd = rows(os.path.join(target, "degree_days_haldenau.csv"))
    G_LT = sum(float(r["g20_15"]) for r in dd if r["season"] == "1991-2020 mean")
    G = defaultdict(float)
    for r in dd:
        if r["season"] != "1991-2020 mean":
            G[int(r["season"][:4]) + 1] += float(r["g20_15"])
    seasons = sorted(G)
    si = {s: k for k, s in enumerate(seasons)}
    hs = {(r["network_area"], int(r["season"][:4]) + 1): float(r["billing_calorific_value_kwh_per_m3"])
          for r in rows(os.path.join(target, "calorific_values_2013_2026.csv"))}
    mpr = rows(os.path.join(target, "meter_points_2026.csv"))
    mp_b, mp_z, mp_area, dev_factor = {}, {}, {}, {}
    for r in mpr:
        mp_b[r["meter_point"]] = bidx[r["building_id"]]
        mp_z[r["meter_point"]] = float(r["z_number"])
        mp_area[r["meter_point"]] = r["network_area"]
        dev_factor[r["meter_number"]] = int(r["factor"])
    reads = defaultdict(dict)
    with open(os.path.join(target, "gas_meter_reads_2013_2026.csv"), newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            key = (r["read_date"], r["meter_number"], r["read_reason"] in ("meter removed",))
            prev = reads[r["meter_point"]].get(key)
            if r["read_reason"] == "correction" or prev is None or (prev[1] != "correction" and r["read_reason"] != "estimate"):
                if estimates == "dropped" and r["read_reason"] == "estimate":
                    continue
                reads[r["meter_point"]][key] = (int(r["reading"]), r["read_reason"])
    weight_cache = {}

    def day_weight(day, h):
        t = temps[day]
        return h / 365.0 + (1 - h) * (20.0 - t if t < 15.0 else 0.0) / G_LT
    kwh = np.zeros((N, len(seasons)))
    seen = np.zeros((N, len(seasons)), bool)
    tune = np.zeros(N, int)
    visits = [set() for _ in range(N)]
    for mp, rs in reads.items():
        b = mp_b[mp]
        h = HW[use[b]]
        pts = []                       # (date, cumulative m3 at the end of the day)
        cum, last = 0.0, None
        for (ds_, num, removed), (val, why) in sorted(rs.items(), key=lambda x: (x[0][0], not x[0][2])):
            day = d_(ds_)
            if why == "service visit":
                s = season_of(day)
                tune[b] = s if tune[b] == 0 else min(tune[b], s)
                visits[b].add(day)
            if why == "meter fitted":
                last = (num, val)
                if not pts:
                    pts.append((day, 0.0))
                continue
            if last is None:
                last = (num, val)
                pts.append((day, 0.0))
                continue
            if last[0] != num:
                last = (num, val)
                continue
            cum += ((val - last[1]) % 100000) * dev_factor[num]
            last = (num, val)
            pts.append((day, cum))
        # cumulative at each 30 April
        ends = {}
        for k in range(len(pts) - 1):
            a, ca = pts[k]
            b2, cb = pts[k + 1]
            for y in range(a.year, b2.year + 1):
                e = dt.date(y, 4, 30)
                if a <= e <= b2:
                    if e == a:
                        ends[y] = ca
                    elif e == b2:
                        ends[y] = cb
                    elif pro_rate:
                        span = [a + dt.timedelta(days=x) for x in range(1, (b2 - a).days + 1)]
                        wts = [day_weight(x, h) for x in span]
                        upto = sum(w_ for x, w_ in zip(span, wts) if x <= e)
                        ends[y] = ca + (cb - ca) * upto / sum(wts)
                    else:
                        ends[y] = cb if (b2 - e).days < (e - a).days else ca
        for s in seasons:
            if s in ends and s - 1 in ends:
                m3 = ends[s] - ends[s - 1]
                kwh[b, si[s]] += m3 * mp_z[mp] * hs[(mp_area[mp], s)]
                seen[b, si[s]] = True
    hvec = np.array([HW[u] for u in use])
    U = np.full((N, len(seasons)), np.nan)
    for s in seasons:
        k = si[s]
        U[:, k] = np.where(seen[:, k], kwh[:, k] * (hvec + (1 - hvec) * G_LT / G[s]), np.nan)
    P = GD.Panel()
    P.seasons, P.si, P.U = seasons, si, U
    P.typ = np.array([TYPES.index(u) for u in use])
    P.ntype = len(TYPES)
    P.tune_season = tune
    P.visits = [sorted(x) for x in visits]
    onum = sorted({str(r["owner_number"]) for r in reg})
    oidx = {o: k for k, o in enumerate(onum)}
    P.owner = np.array([oidx[str(r["owner_number"])] for r in reg])
    P.owner_no = onum
    P.check_season = GD.campaign_season(P)
    P.bid = [r["building_id"] for r in reg]
    P.area = np.array([float(r["heated_floor_area_m2"]) for r in reg])
    # the use each building had on its 2019 notice, the register's use where it had none
    P.typ_register = P.typ.copy()
    P.notice_area = {}
    for r in rows(os.path.join(target, "benchmarking_notices_2019_2026.csv")):
        b = bidx[r["building_id"]]
        s_ = int(r["season"][:4]) + 1
        P.notice_area[(b, s_)] = float(r["heated_floor_area_m2"])
        if s_ == GD.PILOT:
            P.typ[b] = TYPES.index(r["use"])
    pilot = sheet(os.path.join(target, "pilot_2019_responses_and_draw.xlsx"))
    P.answered = np.zeros(N, bool)
    P.drawn = np.zeros(N, bool)
    P.works = np.zeros(N, bool)
    P.withdrawn = np.zeros(N, bool)
    P.measure = np.array([""] * N, dtype=object)
    P.answers19 = []
    P.firm_names = {}
    for r in pilot:
        P.firm_names[firm_key(r["contractor"])] = str(r["contractor"])
        b = bidx[r["building_id"]]
        drawn = r["draw_8_july_2019"] == "drawn"
        wd = bool(r["withdrawn"])
        works = drawn and bool(r["works_completed"])
        P.answers19.append({"b": b, "measure": r["measure"], "date": d_(str(r["received"])[:10]),
                            "cost": float(r["quoted_cost_eur"]), "grant": float(r["grant_eur"]), "drawn": drawn,
                            "withdrawn": wd, "works": works, "firm": firm_key(r["contractor"]),
                            "owner": oidx[str(r["owner_number"])],
                            "done": d_(str(r["works_completed"])[:10]) if works else None})
        P.answered[b] = True
        P.measure[b] = r["measure"]
        P.drawn[b] = drawn
        P.withdrawn[b] = wd
        P.works[b] = works
    P.offered2019 = np.zeros(N, bool)
    for r in rows(os.path.join(target, "benchmarking_notices_2019_2026.csv")):
        if r["grant_offer"] == "pilot 2019":
            P.offered2019[bidx[r["building_id"]]] = True
    # the 2026 applications received by 12 June; a later application for the same building and measure replaces the
    # earlier one
    P.pipe_raw = []
    for r in sheet(os.path.join(target, "applications_2026.xlsx")):
        P.pipe_raw.append({"no": r["application_no"], "b": bidx[r["building_id"]], "measure": r["measure"],
                           "grant": float(r["grant_eur"]), "ref_kwh": float(r["reference_consumption_kwh"]),
                           "date": d_(str(r["received"])[:10]), "firm": firm_key(r["contractor"]),
                           "cost": float(r["quoted_cost_eur"])})
    latest = {}
    for a in P.pipe_raw:
        key = (a["b"], a["measure"])
        if key not in latest or (a["date"], a["no"]) > (latest[key]["date"], latest[key]["no"]):
            latest[key] = a
    P.pipe = sorted(latest.values(), key=lambda a: a["no"])
    for a in P.pipe:
        a["typ"] = int(P.typ_register[a["b"]])
    P.G, P.G_LT, P.hvec = G, G_LT, hvec
    # each building's 2025 week of electricity, its market locations summed, and its roof per square metre of floor
    cust_b = {r["customer_number"]: k for k, r in enumerate(reg)}
    P.week = {}
    for r in rows(os.path.join(target, "electricity_load_profiles_2025.csv")):
        b = cust_b[r["customer_number"]]
        wk = P.week.setdefault(b, np.zeros((7, 24)))
        wk[WEEKDAYS.index(r["weekday"])] += [float(r["kw_%02d" % h]) for h in range(24)]
    faces = defaultdict(list)
    for r in sheet(os.path.join(target, "solar_cadastre_rooftops_2024.xlsx")):
        faces[(street(r["address"]), str(r["postcode"]))].append(float(r["roof_face_area_m2"]))
    roof = {}
    for key, fs in faces.items():
        if outbuildings == "dropped" and max(fs) >= 100.0:     # a garage or shed beside a main roof left out
            fs = [f for f in fs if f >= 50.0]
        roof[key] = sum(fs)
    P.roof = np.full(N, np.nan)
    for k, r in enumerate(reg):
        a = roof.get((street(r["address"]), str(r["postcode"])))
        if a:
            P.roof[k] = a
    P.empty, P.lived_in = empty_weeks(P, threshold)
    P.roof_ratio = P.roof / P.area
    return P


WEEKDAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def firm_key(name):
    """a contractor as the quotes name it, with or without its legal form (the office types some off the letterhead
    without it)"""
    return str(name).replace(" GmbH & Co. KG", "").replace(" GmbH", "").strip()


def street(a):
    """the register writes Lindenstraße 12, the cadastre Lindenstr. 12"""
    return a.replace("str. ", "straße ").strip()


def empty_weeks(P, threshold=0.5, lived_rule="use", margin=0.08):
    """the share of the week each building stands empty: the hours its load is under the point a share `threshold` of
    the way from its lowest hour to its highest, none where the load never falls below three quarters of its highest
    hour. Every hotel and care home is lived in round the clock, its guests or residents there at night whatever its
    load does (lived_rule "use"); the rivals: "weekend" takes a hotel or care home as lived in only where its weekend
    days (8:00 to 20:00) run more than `margin` above its weekend nights (0:00 to 5:00), "strict" only where every
    weekend day hour runs above every weekend night hour, "none" reads every building off its load alone"""
    e = np.full(len(P.typ_register), np.nan)
    lived = np.zeros(len(P.typ_register), bool)
    for b, kw in P.week.items():
        lo, hi = kw.min(), kw.max()
        e[b] = 1.0 - float((kw > lo + threshold * (hi - lo)).sum()) / 168.0
        if lo >= 0.75 * hi:                  # never falls below three quarters of its peak: in use round the clock
            e[b] = 0.0
        if TYPES[P.typ_register[b]] in ("hotel", "care home") and lived_rule != "none":
            day, night = kw[5:, 8:20], kw[5:, 0:5]
            if (lived_rule == "use" or (lived_rule == "weekend" and day.mean() > (1.0 + margin) * night.mean())
                    or (lived_rule == "strict" and day.min() > night.max())):
                lived[b] = True
                e[b] = 0.0
    return e, lived
