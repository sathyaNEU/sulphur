"""task7 architecture 8: the pack's data files, written from the world (world.py) the way the utility's and the
council's systems would export them. The meter reads carry the billing system's own mess: periodic reads taken a few
days off 30 April, interim reads, the service team's reads at its visits, meter exchanges, five-digit counters that roll
over, estimates (some later corrected), customer reads corrected after a typo, rows imported twice, meters that count in
tens of cubic metres. None of it decides the call (checks.py)."""
import csv
import datetime as dt
import math
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from openpyxl.utils import get_column_letter

import postprocess as PP
import world as W

SEED = 7401
AREAS = ["HN-1", "HN-2", "HN-3"]
AREA_P = [0.42, 0.36, 0.22]
L_GAS_UNTIL = 2017                       # HN-3 ran on L-gas to 30 April 2017
DISTRICTS = ["Altstadt", "Nordstadt", "Südstadt", "Weststadt", "Oststadt", "Bahnhofsviertel", "Hafen", "Kirchberg",
             "Lindenhof", "Mühlbach", "Rosental", "Sonnenberg", "Steinach", "Talheim", "Unterwiesen", "Waldau",
             "Weinsteige", "Ziegelhütte", "Am Ring", "Auenpark", "Bergheim", "Birkenfeld", "Brühl", "Eichwald",
             "Feldkirch", "Gartenstadt", "Hochfeld", "Hohenrain", "Gewerbegebiet Nord", "Gewerbegebiet Süd",
             "Kreuzäcker", "Langenau", "Marienhöhe", "Neckarvorstadt", "Neuhof", "Oberwiesen", "Rheinau",
             "Schlossberg", "Sandweg", "Uferviertel", "Wiesental", "Wolfsgrube"]
STREET_A = ["Linden", "Ahorn", "Bahnhof", "Schiller", "Goethe", "Kirch", "Markt", "Mühlen", "Garten", "Wald", "Berg",
            "Hafen", "Industrie", "Gewerbe", "Post", "Schul", "Brunnen", "Rosen", "Tannen", "Eichen", "Birken",
            "Wiesen", "Feld", "Mozart", "Kepler", "Uhland", "Hölderlin", "Daimler", "Bosch", "Benz", "Neckar",
            "Rathaus", "Schloss", "Burg", "Kloster", "Stein", "Ziegel", "Hopfen", "Weinberg", "Sonnen", "Mond",
            "Stern", "Kanal", "Brücken", "Werk", "Hütten", "Röntgen", "Siemens", "Zeppelin", "Kant"]
STREET_B = ["straße", "weg", "allee", "ring", "platz", "gasse", "steige"]
TYPE_LABEL = {"office": "office", "retail": "retail", "hotel": "hotel", "workshop": "workshop",
              "care home": "care home", "restaurant": "restaurant"}
OFFICE_TIME = dt.datetime(2026, 6, 22, 9, 12)


def ymd(d):
    return d.strftime("%Y-%m-%d")


def season_label(s):
    return "%d/%02d" % (s - 1, s % 100)


def office(path, company, created, modified):
    """the workbook laid out as the issuing office's Excel saves it (H1)"""
    PP.normalize_ooxml(path, company, company, created, modified, excel=True, company=company)


def write_csv(path, header, rows, newline="\n"):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        wr = csv.writer(fh, lineterminator=newline)
        wr.writerow(header)
        wr.writerows(rows)


class Pack:
    pass


def assemble(w):
    rng = np.random.default_rng(SEED)
    P = Pack()
    P.w = w
    N = w.N
    # building identities
    ids = rng.choice(np.arange(100000, 999999), N, replace=False)
    P.bid = ["HB-%06d" % x for x in ids]
    P.cust = ["%09d" % x for x in rng.choice(np.arange(100000000, 999999999), N, replace=False)]
    P.district = [DISTRICTS[int(d)] for d in w.district]
    onums = rng.choice(np.arange(2000000, 2999999), w.n_owners, replace=False)
    P.owner_no = ["%07d" % x for x in onums]
    streets = {}
    for d in range(len(DISTRICTS)):
        n = 9 + int(rng.integers(0, 8))
        streets[d] = sorted({STREET_A[int(rng.integers(0, len(STREET_A)))] + STREET_B[int(rng.integers(0, len(STREET_B)))]
                             for _ in range(n)})
    P.postcode = {d: "7%04d" % (1100 + 37 * d) for d in range(len(DISTRICTS))}
    P.address = []
    used = set()
    for i in range(N):
        d = int(w.district[i])
        while True:
            a = "%s %d" % (streets[d][int(rng.integers(0, len(streets[d])))], int(rng.integers(1, 160)))
            if (d, a) not in used:
                used.add((d, a))
                break
        P.address.append(a)
    P.built = rng.integers(1900, 2016, N)
    P.area_net = [AREAS[int(rng.choice(3, p=AREA_P))] for _ in range(N)]
    # meter points: most buildings one, some two (main building and annex)
    two = rng.random(N) < 0.08
    P.mps = []                           # per meter point: dict
    P.mp_of = [[] for _ in range(N)]
    for i in range(N):
        shares = [0.65, 0.35] if two[i] else [1.0]
        for sh in shares:
            mp = {"id": "DE004712%012d" % int(rng.integers(10 ** 11, 10 ** 12)), "b": i, "share": sh,
                  "z": round(float(rng.uniform(0.9300, 0.9690)), 4), "area": P.area_net[i]}
            P.mp_of[i].append(len(P.mps))
            P.mps.append(mp)
    # calorific values by network area and season
    P.hs = {}
    for a in AREAS:
        base = {"HN-1": 11.31, "HN-2": 11.24, "HN-3": 11.36}[a]
        for s in W.SEASONS:
            if a == "HN-3" and s <= L_GAS_UNTIL:
                P.hs[(a, s)] = round(10.04 + float(rng.normal(0, 0.03)), 3)
            else:
                P.hs[(a, s)] = round(base + float(rng.normal(0, 0.05)), 3)
    return P


def meter_reads(P):
    """every read of every meter point, May 2013 to April 2026, and the meter devices"""
    w = P.w
    rng = np.random.default_rng(SEED + 1)
    rows = []
    devices = []
    s0 = W.SEASONS[0]
    for j, mp in enumerate(P.mps):
        i = mp["b"]
        first, last = int(w.first[i]), int(w.last[i])
        # daily m3 over the building's connected seasons
        days, m3 = [], []
        for s in range(first, last + 1):
            dk = W.daily_kwh(w, i, s) * mp["share"]
            days += W.season_days(s)
            m3 += list(dk / (mp["z"] * P.hs[(mp["area"], s)]))
        cum = np.cumsum(m3)
        start_day = days[0]
        annual = cum[-1] / max(1, len(days) / 365.25)
        factor = 10 if annual > 30000 else 1
        mp["factor"] = factor

        def at(d):
            """cumulative m3 through the end of day d (a read is the index at the end of its day)"""
            k = (d - start_day).days + 1
            return 0.0 if k <= 0 else float(cum[min(k, len(cum)) - 1])
        # devices: an exchange for about one meter point in ten
        exch = []
        if rng.random() < 0.10:
            k = int(rng.integers(30, len(days) - 30))
            exch.append(days[k])
        dev_start = [start_day] + exch
        dev_end = exch + [days[-1] + dt.timedelta(days=1)]
        dev = []
        for a, b in zip(dev_start, dev_end):
            num = "7GMT%010d" % int(rng.integers(10 ** 9, 10 ** 10))
            offset = float(rng.integers(500, 60000)) if factor == 1 else float(rng.integers(50, 6000)) * 10
            dev.append({"num": num, "from": a, "to": b,
                        "offset": offset if a == start_day else -at(a) + float(rng.integers(0, 40)) * factor})
            fitted = a if a != start_day else start_day - dt.timedelta(days=1)
            if a == start_day and first == s0:
                fitted = dt.date(2009, 1, 1) + dt.timedelta(days=int(rng.integers(0, 1400)))
            removed = b if b in exch else (days[-1] if last < W.SEASONS[-1] else None)
            devices.append({"mp": mp["id"], "num": num, "fitted": fitted, "removed": removed, "factor": factor})

        def reading(dv, d):
            v = (at(d) + dv["offset"]) / factor
            return int(math.floor(v)) % 100000

        def device_on(d):
            for dv in dev:
                if dv["from"] < d + dt.timedelta(days=1) <= dv["to"]:
                    return dv
            return dev[-1]
        out = []
        # the connection read, and the periodic reads at 30 April
        if first > s0:
            out.append((start_day - dt.timedelta(days=1), dev[0], "meter fitted", "utility"))
        for y in range(first, last + 1):
            d = dt.date(y, 4, 30)
            if y == last and last < W.SEASONS[-1]:
                out.append((d, device_on(d), "meter removed", "utility"))
                continue
            dd = d
            u = rng.random()
            if y < last and u < 0.07:
                dd = d + dt.timedelta(days=int(rng.integers(1, 41)))
            elif y < last and u < 0.09:
                dd = d - dt.timedelta(days=int(rng.integers(1, 9)))
            by = "customer" if rng.random() < 0.30 else "utility"
            out.append((dd, device_on(dd), "periodic", by))
        if first == s0:
            out.append((start_day - dt.timedelta(days=1), dev[0], "periodic", "utility"))
        # meter exchanges
        for k, d in enumerate(exch):
            out.append((d, dev[k], "meter removed", "utility"))
            out.append((d, dev[k + 1], "meter fitted", "utility"))
        # interim reads (a tenant change, a bill on request)
        for s in range(first, last + 1):
            if rng.random() < 0.015:
                ds = W.season_days(s)
                d = ds[int(rng.integers(5, len(ds) - 5))]
                out.append((d, device_on(d), "interim", "customer" if rng.random() < 0.5 else "utility"))
        # the service team's read at each of its checks
        for td in w.visits[i]:
            if start_day <= td <= days[-1]:
                out.append((td, device_on(td), "service visit", "utility"))
        for d, dv, why, by in sorted(out, key=lambda x: (x[0], x[2] != "meter removed")):
            if d < start_day - dt.timedelta(days=1):
                continue
            r = reading(dv, d)
            rows.append([mp["id"], dv["num"], ymd(d), r, why, by])
            if why == "periodic" and by == "customer" and rng.random() < 0.006:
                s = str(r).zfill(5)
                k = int(rng.integers(0, 4))
                bad = int(s[:k] + s[k + 1] + s[k] + s[k + 2:])
                if bad != r:
                    rows[-1][3] = bad
                    rows.append([mp["id"], dv["num"], ymd(d), r, "correction", "utility"])
            elif why == "periodic" and rng.random() < 0.02:
                est = int(math.floor(r + (rng.normal(0, 0.06) * annual / factor))) % 100000
                rows[-1][3] = est
                rows[-1][4] = "estimate"
                rows[-1][5] = "estimated"
                rows.append([mp["id"], dv["num"], ymd(d), r, "correction", "utility"])
    # rows imported twice
    dup = rng.random(len(rows)) < 0.004
    rows = rows + [list(r) for r, f in zip(rows, dup) if f]
    order = np.lexsort((np.array([r[2] for r in rows]), np.array([r[0] for r in rows])))
    rows = [rows[k] for k in order]
    return rows, devices


def write_reads(P, target):
    rows, devices = meter_reads(P)
    P.n_reads = len(rows)
    write_csv(os.path.join(target, "gas_meter_reads_2013_2026.csv"),
              ["meter_point", "meter_number", "read_date", "reading", "read_reason", "read_by"], rows)
    P.devices = devices
    mpi = {mp["id"]: mp for mp in P.mps}
    out = []
    for dv in devices:
        mp = mpi[dv["mp"]]
        out.append([dv["mp"], P.bid[mp["b"]], dv["num"], ymd(dv["fitted"]), ymd(dv["removed"]) if dv["removed"] else "",
                    dv["factor"], "%.4f" % mp["z"], mp["area"]])
    out.sort(key=lambda r: (r[1], r[0], r[3]))
    write_csv(os.path.join(target, "meter_points_2026.csv"),
              ["meter_point", "building_id", "meter_number", "fitted", "removed", "factor", "z_number", "network_area"],
              out)


def write_calorific(P, target):
    rows = []
    for a in AREAS:
        for s in W.SEASONS:
            rows.append([a, season_label(s), ymd(dt.date(s - 1, 5, 1)), ymd(dt.date(s, 4, 30)), "%.3f" % P.hs[(a, s)]])
    write_csv(os.path.join(target, "calorific_values_2013_2026.csv"),
              ["network_area", "season", "from", "to", "billing_calorific_value_kwh_per_m3"], rows)


def wb_sheet(wb, title, header, rows, widths, first=False):
    ws = wb.active if first else wb.create_sheet()
    ws.title = title
    ws.append(header)
    for c in ws[1]:
        c.font = Font(bold=True, color="FFFFFF")
        c.fill = PatternFill("solid", fgColor="2F5D50")
        c.alignment = Alignment(vertical="center", wrap_text=True)
    for r in rows:
        ws.append(r)
    for k, wd in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(k)].width = wd
    ws.freeze_panes = "A2"
    return ws


def write_register(P, target):
    w = P.w
    rows = []
    for i in np.argsort(P.bid):
        rows.append([P.bid[i], P.address[i], P.postcode[int(w.district[i])], P.district[i], TYPE_LABEL[W.TYPES[w.typ[i]]],
                     float(w.area[i, -1]), int(P.built[i]), P.cust[i], P.owner_no[int(w.owner[i])]])
    wb = Workbook()
    wb_sheet(wb, "buildings", ["building_id", "address", "postcode", "district", "use", "heated_floor_area_m2",
                               "year_built", "customer_number", "owner_number"], rows, [12, 26, 9, 20, 12, 12, 10, 14, 12],
             first=True)
    path = os.path.join(target, "buildings_register_2026.xlsx")
    wb.save(path)
    office(path, "Stadtwerke Haldenau", "2026-06-15T07:40:00Z", "2026-06-15T07:52:00Z")


def type_medians(w, k):
    out = {}
    live = np.isfinite(w.norm_intensity[:, k])
    for t in range(len(W.TYPES)):
        m = live & (w.typ == t) & (w.first <= W.SEASONS[k] - 1)
        out[t] = float(np.median(w.norm_intensity[m, k]))
    return out


def write_notices(P, target):
    w = P.w
    rows = []
    n = 0
    for s in W.SEASONS[W.SI[W.PILOT]:]:
        k = W.SI[s]
        med = type_medians(w, k)
        nd = dt.date(s, *W.NOTICE_MD)
        for i in sorted(np.where(w.flag[:, k])[0], key=lambda x: P.bid[x]):
            n += 1
            offer = "pilot 2019" if (s == W.PILOT and w.offer[i, k]) else ("round 2026" if (s == W.PIPELINE and w.offer[i, k]) else "")
            rows.append(["N%d-%05d" % (s, n), P.bid[i], season_label(s), ymd(nd), "%.0f" % w.area[i, k],
                         "%.1f" % w.norm_intensity[i, k], "%.1f" % med[w.typ[i]], TYPE_LABEL[W.TYPES[w.typ[i]]], offer])
    P.n_notices = len(rows)
    write_csv(os.path.join(target, "benchmarking_notices_2019_2026.csv"),
              ["notice_id", "building_id", "season", "sent", "heated_floor_area_m2", "normalised_use_kwh_per_m2",
               "median_for_use_kwh_per_m2", "use", "grant_offer"], rows)


def write_pilot(P, target):
    w = P.w
    rng = np.random.default_rng(SEED + 2)
    k = W.SI[W.PILOT]
    idx = sorted(np.where(w.applied[:, k])[0], key=lambda x: (rng.random(), P.bid[x]))
    rows = []
    for n, i in enumerate(idx, 1):
        ans = w.answer_date[W.PILOT][i]
        wd = ""
        done = ""
        if w.withdrawn[i]:
            wd = ymd(W.DRAW_DATE + dt.timedelta(days=int(rng.integers(3, 45))))
        elif w.works[i]:
            done = ymd(w.done_date[i])
        rows.append(["P19-%04d" % n, P.owner_no[int(w.owner[i])], P.bid[i], ymd(ans), w.measure[i],
                     contractor(w, i, W.PILOT), float(w.cost[W.PILOT][i]), float(w.grant[W.PILOT][i]),
                     "drawn" if w.drawn[i] else "not drawn", wd, done])
    wb = Workbook()
    wb_sheet(wb, "responses", ["response_no", "owner_number", "building_id", "received", "measure", "contractor",
                             "quoted_cost_eur", "grant_eur", "draw_8_july_2019", "withdrawn", "works_completed"], rows,
             [11, 12, 12, 11, 20, 30, 14, 11, 16, 11, 14], first=True)
    path = os.path.join(target, "pilot_2019_responses_and_draw.xlsx")
    wb.save(path)
    office(path, "Stadt Haldenau", "2019-07-08T15:05:00Z", "2019-10-07T08:31:00Z")


def contractor(w, i, year):
    """the firm the owner's quote came from"""
    f = w.firm[year][int(i)]
    return W.ROOFERS[f] if (w.measure if year == W.PILOT else w.measure26)[i] == "insulation" else W.HEATING_FIRMS[f]


def write_applications(P, target):
    """the applications the Climate Protection Office passed on, received by 12 June; an owner who revised the quote
    sent the application again, and the later one stands"""
    w = P.w
    rng = np.random.default_rng(SEED + 3)
    k = W.SI[W.PIPELINE]
    entries = []
    for i in np.where(w.received26)[0]:
        i = int(i)
        m = w.measure26[i]
        ref = round(round(float(w.norm_intensity[i, k]), 1) * w.area[i, k])
        rec = w.answer_date[W.PIPELINE][i]
        if i in w.resubmit:
            d2, c1, g1 = w.resubmit[i]
            entries.append((rec, rng.random(), i, m, c1, g1, ref))
            if d2 <= W.RECEIVED_TO:
                entries.append((d2, rng.random(), i, m, float(w.cost[W.PIPELINE][i]), float(w.grant[W.PIPELINE][i]), ref))
        else:
            entries.append((rec, rng.random(), i, m, float(w.cost[W.PIPELINE][i]), float(w.grant[W.PIPELINE][i]), ref))
    entries.sort(key=lambda e: (e[0], e[1], P.bid[e[2]]))
    rows = []
    P.pipe_rows = []
    rv = np.random.default_rng(SEED + 31)
    for n, (rec, _, i, m, c, g, ref) in enumerate(entries, 1):
        firm = contractor(w, i, W.PIPELINE)
        if rv.random() < 0.06:              # typed off the quote's letterhead without the legal form
            firm = firm.replace(" GmbH & Co. KG", "").replace(" GmbH", "")
        rows.append(["A26-%04d" % n, P.bid[i], ymd(rec), m, firm, float(c), float(g), int(ref)])
        P.pipe_rows.append({"no": "A26-%04d" % n, "b": int(i), "measure": m, "grant": float(g), "ref_kwh": float(ref),
                            "date": rec})
    wb = Workbook()
    wb_sheet(wb, "applications", ["application_no", "building_id", "received", "measure", "contractor",
                                  "quoted_cost_eur", "grant_eur", "reference_consumption_kwh"], rows,
             [14, 12, 11, 20, 30, 14, 11, 16], first=True)
    path = os.path.join(target, "applications_2026.xlsx")
    wb.save(path)
    office(path, "Stadt Haldenau", "2026-05-21T08:40:00Z", "2026-06-15T16:22:00Z")


def write_weather(P, target):
    w = P.w
    rows = []
    for s in W.SEASONS:
        for d, t in zip(w.days[s], w.temp[s]):
            rows.append([ymd(d), "%.1f" % t])
    write_csv(os.path.join(target, "weather_haldenau_daily_2013_2026.csv"), ["date", "mean_temperature_c"], rows)
    out = []
    for s in W.SEASONS:
        for m in [5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4]:
            idx = [k for k, d in enumerate(w.days[s]) if d.month == m]
            out.append([season_label(s), "%d-%02d" % (s - 1 if m >= 5 else s, m), "%.0f" % W.g2015(w.temp[s][idx])])
    for m in [5, 6, 7, 8, 9, 10, 11, 12, 1, 2, 3, 4]:
        out.append(["1991-2020 mean", "%02d" % m, "%.0f" % w.G_LT_MONTH[m]])
    write_csv(os.path.join(target, "degree_days_haldenau.csv"), ["season", "month", "g20_15"], out)


WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
PROFILE_SEED = 4242


def profile_buildings(w):
    """the buildings standing through calendar 2025, whose electricity the meter operator profiles (a building that
    has left the gas network still draws electricity)"""
    return [i for i in range(w.N) if w.first[i] <= 2025]


def write_profiles(P, target):
    """Stadtwerke Haldenau Netz's typical weeks for 2025: for every commercial market location, the mean load in each
    hour of each weekday over the year's measured days; a building with an annex or a separately metered part has two
    market locations, and a meter exchanged during the year leaves fewer measured days"""
    w = P.w
    rng = np.random.default_rng(SEED + 5)
    rows = []
    P.malo = {}
    for i in profile_buildings(w):
        kw = W.load_week(w, i, PROFILE_SEED)
        parts = [(1.0, kw)]
        if rng.random() < 0.06:
            sh = float(rng.uniform(0.20, 0.35))
            k2 = np.round(np.clip(kw * sh * (1.0 + 0.04 * rng.normal(0, 1, kw.shape)), 0.1, None), 1)
            parts = [(1.0 - sh, np.round(np.clip(kw - k2, 0.1, None), 1)), (sh, k2)]
        ids = []
        for _, v in parts:
            ml = "5%010d" % int(rng.integers(10 ** 9, 10 ** 10))
            ids.append(ml)
            gap = int(rng.integers(1, 9)) if rng.random() < 0.03 else 0
            for d in range(7):
                rows.append([ml, P.cust[i], 2025, WEEKDAY_NAMES[d], W.WEEKDAYS_2025[d] - gap]
                            + ["%.1f" % x for x in v[d]])
        P.malo[i] = ids
    rows.sort(key=lambda r: (r[0], WEEKDAY_NAMES.index(r[3])))
    P.n_profiles = len(rows)
    write_csv(os.path.join(target, "electricity_load_profiles_2025.csv"),
              ["market_location", "customer_number", "year", "weekday", "days_measured"]
              + ["kw_%02d" % h for h in range(24)], rows)


def cadastre_address(a):
    return a.replace("straße ", "str. ")


def write_cadastre(P, target):
    """the state's solar cadastre (2023 flight), one row per roof face: a flat roof one face, a gable roof two, a hipped
    roof four, and at some addresses a garage or outbuilding beside the main roof"""
    w = P.w
    rng = np.random.default_rng(SEED + 6)
    rows = []
    k = W.SI[2025]
    orient = ["N", "NE", "E", "SE", "S", "SW", "W", "NW"]
    yield_by = {"N": 0, "NE": 560, "E": 820, "SE": 930, "S": 980, "SW": 930, "W": 820, "NW": 560, "flat": 900}
    for i in np.argsort(P.bid):
        if w.first[i] > 2023:
            continue
        total = w.roof_ratio[i] * w.area[i, k]
        faces = []
        if not w.pitched[i]:
            faces.append((total, float(rng.uniform(0, 4)), "flat"))
        else:
            tilt = float(rng.uniform(24, 45))
            o = int(rng.integers(0, 8))
            if rng.random() < 0.65:
                faces += [(total / 2, tilt, orient[o]), (total / 2, tilt, orient[(o + 4) % 8])]
            else:
                big = float(rng.uniform(0.30, 0.38))
                faces += [(total * big, tilt, orient[o]), (total * big, tilt, orient[(o + 4) % 8]),
                          (total * (0.5 - big), tilt, orient[(o + 2) % 8]), (total * (0.5 - big), tilt, orient[(o + 6) % 8])]
        if rng.random() < 0.10:
            faces.append((float(rng.uniform(18, 45)), float(rng.uniform(0, 3)), "flat"))
        for n, (ar, tl, ori) in enumerate(faces, 1):
            ar = round(ar * float(rng.normal(1.0, 0.02)), 1)
            good = ori == "flat" or ori in ("SE", "S", "SW")
            fair = ori in ("E", "W")
            suit = "very good" if good and tl < 40 else ("good" if good or fair else "not suitable")
            kwp = round(ar * (0.62 if ori == "flat" else 0.80) * 0.19, 1) if suit != "not suitable" else 0.0
            rows.append([cadastre_address(P.address[i]), P.postcode[int(w.district[i])], n, ar, round(tl), ori, suit,
                         kwp, int(round(kwp * yield_by[ori]))])
    wb = Workbook()
    wb_sheet(wb, "roof faces", ["address", "postcode", "roof_face", "roof_face_area_m2", "tilt_deg", "orientation",
                                "pv_suitability", "pv_potential_kwp", "pv_yield_kwh_per_year"],
             rows, [26, 9, 9, 16, 8, 11, 14, 15, 18], first=True)
    path = os.path.join(target, "solar_cadastre_rooftops_2024.xlsx")
    wb.save(path)
    office(path, "Landesanstalt für Umwelt Baden-Württemberg", "2024-03-11T09:00:00Z", "2024-03-11T09:00:00Z")
    P.n_roof_faces = len(rows)


def write_distractors(P, target):
    """the billing system's annual electricity consumption for customers on the commercial tariff, 2019 to 2025"""
    w = P.w
    rng = np.random.default_rng(SEED + 4)
    rows = []
    covid = {2020: 0.04, 2021: 0.07}
    for i in np.argsort(P.bid):
        if rng.random() < 0.55 or i not in P.malo:
            continue
        kwh = float(W.load_week(w, int(i), PROFILE_SEED).sum()) * 52.14
        t = W.TYPES[w.typ[i]]
        for y in range(2019, 2026):
            f = 1.0 - (covid.get(y, 0.0) if t in ("office", "restaurant", "hotel") else 0.0) - (0.05 if y >= 2023 else 0.0)
            rows.append([P.cust[i], P.address[i], y, int(round(kwh * f * float(rng.normal(1, 0.04)))), "commercial"])
    write_csv(os.path.join(target, "electricity_customers_annual_2019_2025.csv"),
              ["customer_number", "supply_address", "year", "consumption_kwh", "tariff_group"], rows)


def write_all(w, target):
    P = assemble(w)
    write_reads(P, target)
    write_calorific(P, target)
    write_register(P, target)
    write_notices(P, target)
    write_pilot(P, target)
    write_applications(P, target)
    write_weather(P, target)
    write_profiles(P, target)
    write_cadastre(P, target)
    write_distractors(P, target)
    counts = {"reads": P.n_reads, "notices": P.n_notices, "meter_points": len(P.mps), "applications_2026": len(P.pipe_rows),
              "load_profile_rows": P.n_profiles, "roof_faces": P.n_roof_faces}
    return P, counts
