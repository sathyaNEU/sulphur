"""The shipped records, written from the world `world.py` lays out: each road station's tip log, the technicians'
visit book, the present-weather detectors' database, the agency's convective-cell extract and pixel list, the
rainfall normal, the research valley's weighing gauges, and two files the analysis does not use. Each file is
written the way its system writes it; the texture laid on top (re-sent logger blocks, the technicians' tip tests,
maintenance visits) never touches an array the core reads."""
import csv
import datetime as dt
import math
import os
import sqlite3
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402
import world as WL  # noqa: E402

CODE = {d: v[0] for d, v in WL.STATIONS.items()}
FILES = {
    "tips": "tips_%s_2009-2026.csv",
    "visits": "station_visit_book_2009-2026.csv",
    "pw": "present_weather_blocks.sqlite",
    "wx": "present_weather_codes.csv",
    "radar": "radar_cells_p60max_2013-2026.csv",
    "pixels": "radar_pixels.csv",
    "normal": "precipitation_normal_1991-2020_500m.csv",
    "rs_events": "rio_scuro_weighing_gauges_events_2013-2026.csv",
    "rs_gauges": "rio_scuro_weighing_gauges.csv",
    "daily": "ardesa_centro_daily_precipitation_1961-2026.csv",
    "traffic": "sp141_traffic_daily_2019-2026.csv",
}
GAUGE_ID = {"Scuro 1": "RS-W1", "Scuro 2": "RS-W2", "Scuro 3": "RS-W3", "Scuro 4": "RS-W4"}
E64 = np.datetime64(WL.EPOCH, "s")


def iso(t, shift=0):
    """seconds on the loggers' clock as ISO strings (shift in seconds, for UTC)"""
    return np.datetime_as_string(E64 + (np.asarray(t, dtype=np.int64) + shift).astype("timedelta64[s]"), unit="s")


# ------------------------------------------------------------------------------------------------- the texture
def windows(WD, d):
    """every rain event at a station as (start, end) on the loggers' clock"""
    w = [(int(t), int(t) + WL.STORM_LEN) for t in WD["onset"][d]]
    w += [(st, st + 3600 * len(h)) for (_, _, st, h) in WD["spells"][d]]
    return sorted(w)


def texture(WD):
    """Maintenance visits between the monthly reads, the technicians' tip tests, and the blocks a logger sent twice
    after a restart. All of it falls in dry weather or inside long rain, and none of it is in the core's arrays."""
    r = WL.rng(8)
    extra, tests, resent = [], {d: [] for d in WD["W"]}, {}
    remarks = ["funnel cleared of larch needles", "logger battery replaced (11.6 V)", "solar panel cleaned",
               "mast guy wires tightened", "grass cut around the mast", "modem restarted, no data lost",
               "wasps' nest removed from the logger box", "level of the gauge checked, in order",
               "detector lens cleaned", "storage gauge funnel cleared of pollen", "fence repaired after cattle",
               "cable gland replaced on the logger box"]
    for d in WL.ORDER:
        ev = windows(WD, d)
        starts = np.array([a for a, _ in ev])
        for s, y in enumerate(WL.YEARS):
            reg = WD["V"][(d, s)]
            for b, t in enumerate(reg):                      # tip tests on the regular rounds
                if b == 0 or r.random() < 0.3:
                    tests[d].append((t + int(r.integers(240, 720)), 5, ("reg", s, b)))
            for _ in range(int(r.poisson(1.0))):
                for _try in range(200):
                    day = dt.date(y, 5, 10) + dt.timedelta(days=int(r.integers(0, 160)))
                    if not WL.working(day):
                        continue
                    cv = dt.datetime(day.year, day.month, day.day) + dt.timedelta(minutes=int(r.integers(102, 190)) * 5)
                    t = WL.sec(WL.civil_to_logger(cv))
                    i = int(np.searchsorted(starts, t))
                    near = [ev[j] for j in (i - 1, i) if 0 <= j < len(ev)]
                    if any(a - 4 * 3600 < t < z + 4 * 3600 for a, z in near):
                        continue
                    if min(abs(t - v) for v in reg) < 4 * 86400 or any(abs(t - x[1]) < 2 * 86400 for x in extra if x[0] == d):
                        continue
                    tested = r.random() < 0.5
                    extra.append((d, t, cv, "A. Cundari" if (y < 2019 or r.random() < 0.6) else "B. Panatta",
                                  str(r.choice(remarks)), 5 if tested else 0))
                    if tested:
                        tests[d].append((t + int(r.integers(240, 720)), 5, ("extra", len(extra) - 1)))
                    break
        # blocks re-sent after a restart: a run of tips inside a spell of long rain, written twice
        T = WD["tips"][d]
        blocks = []
        sp = [x for x in WD["spells"][d] if len(x[3]) >= 8]
        for k in r.choice(len(sp), int(r.integers(6, 11)), replace=False):
            st, n = sp[k][2], len(sp[k][3])
            i0, i1 = int(np.searchsorted(T, st + 3600)), int(np.searchsorted(T, st + 3600 * (n - 1)))
            run = int(r.integers(14, 70))
            if i1 - i0 > run + 4:
                a = int(r.integers(i0, i1 - run))
                blocks.append((a, a + run))
        resent[d] = sorted(blocks)
    return dict(extra=extra, tests=tests, resent=resent)


def test_tips(tests, r):
    """the seconds at which a technician's manual tips were logged"""
    out = []
    for t, n, _ in tests:
        gaps = r.integers(2, 5, n)
        out.extend(int(t + g) for g in np.cumsum(gaps))
    return np.array(sorted(out), dtype=np.int64)


# --------------------------------------------------------------------------------------------------- the files
def write_tips(target, WD, TX):
    r = WL.rng(10)
    counts = {}
    for d in WL.ORDER:
        b = WL.BUCKET[WD["W"][d]["model"]]
        tt = test_tips(TX["tests"][d], r)
        T = WD["tips"][d]
        assert len(np.intersect1d(T, tt)) == 0
        # the logger's own order: rain tips and test tips by time, a re-sent block straight after its first copy
        pieces, prev = [], 0
        for a, z in TX["resent"][d]:
            pieces += [T[prev:z], T[a:z]]
            prev = z
        pieces.append(T[prev:])
        seq = np.concatenate(pieces)
        if len(tt):
            pos = np.searchsorted(seq, tt)               # test tips fall in dry weather, never inside a re-sent block
            seq = np.insert(seq, pos, tt)
        stamps = iso(seq)
        val = "%.1f" % b
        with open(os.path.join(target, FILES["tips"] % CODE[d]), "w", newline="") as f:
            f.write("tip_time,tip_mm\r\n")
            f.write("".join("%s+01:00,%s\r\n" % (s, val) for s in stamps))
        counts[d] = (len(seq), len(tt), sum(z - a for a, z in TX["resent"][d]))
    return counts


def write_visits(target, WD, TX):
    r, r2 = WL.rng(11), WL.rng(12)
    notes = ["", "", "", "", "", "", "", "oil film renewed", "storage gauge read twice, same value", "spirit level in order",
             "screen door hinge oiled", "logger clock checked against the phone", "snow patches still above the station",
             "road works at the lay-by, parked below", "cows in the enclosure, gate closed again", "data card swapped"]
    tested = {d: {k[1:] for _, _, k in TX["tests"][d] if k[0] == "reg"} for d in WD["W"]}
    rows = []
    for d in WL.ORDER:
        w = WD["W"][d]
        for s in range(C.G_SEASONS):
            for b in range(WL.MONTHS + 1):
                cv, who = WD["civil"][(d, s, b)], WD["who"][(d, s, b)]
                test = "5" if (s, b) in tested[d] else ""
                if b == 0:
                    rows.append((cv, d, who, "", "set empty", test, "season opening: funnel fitted, storage gauge set with oil film"))
                    continue
                read = "%.1f" % float(w["check"][s * WL.MONTHS + b - 1])
                note = "season closing: logger read out, funnel covered" if b == WL.MONTHS else str(r.choice(notes))
                if note.startswith("logger clock checked"):          # a quartz logger drifts a few seconds a month
                    note += ", %d s" % int(r2.choice([0, 1, 1, 2, 2, 3, 4, 6]))
                rows.append((cv, d, who, read, "yes", test, note))
    for (d, _, cv, who, note, n) in TX["extra"]:
        rows.append((cv, d, who, "", "no", str(n) if n else "", note))
    rows.sort(key=lambda x: (x[0], WL.ORDER.index(x[1])))
    with open(os.path.join(target, FILES["visits"]), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["station", "visit_date", "visit_time_local", "technician", "storage_gauge_mm", "storage_emptied",
                     "tip_test_tips", "remarks"])
        for cv, d, who, read, emptied, test, note in rows:
            wr.writerow([CODE[d], cv.strftime("%Y-%m-%d"), cv.strftime("%H:%M"), who, read, emptied, test, note])
    return len(rows)


def write_detector(target, WD):
    path = os.path.join(target, FILES["pw"])
    if os.path.exists(path):
        os.remove(path)
    con = sqlite3.connect(path)
    con.execute("PRAGMA page_size = 4096")
    con.execute("PRAGMA journal_mode = OFF")
    con.execute("CREATE TABLE pw_block (station TEXT NOT NULL, block_start TEXT NOT NULL, block_min INTEGER NOT NULL, "
                "wx TEXT NOT NULL, intensity_mm_h REAL NOT NULL)")
    n = 0
    for d in WL.ORDER:
        t, c, v = WD["detector"][d]
        stamps = iso(t)
        con.executemany("INSERT INTO pw_block VALUES (?, ?, 10, ?, ?)",
                        [(CODE[d], s + "+01:00", str(cc), float(vv)) for s, cc, vv in zip(stamps, c, v)])
        n += len(t)
    con.execute("CREATE INDEX ix_pw_block_station_start ON pw_block (station, block_start)")
    con.commit()
    con.execute("VACUUM")
    con.close()
    with open(os.path.join(target, FILES["wx"]), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["wx", "meaning"])
        for row in (("DZ", "drizzle"), ("-RA", "rain, light"), ("RA", "rain, moderate"), ("+RA", "rain, heavy"),
                    ("GS", "small hail or graupel"), ("RAGS", "rain with small hail or graupel"), ("GR", "hail"),
                    ("+RAGR", "heavy rain with hail"), ("SN", "snow"), ("RASN", "rain and snow"), ("UP", "unidentified")):
            wr.writerow(row)
    return n


def write_radar(target, WD):
    new, old = WL.pixel_ids()
    seqs, n = {}, 0
    with open(os.path.join(target, FILES["radar"]), "w", newline="") as f:
        f.write("cell_id,first_scan_utc,last_scan_utc,pixel,p60_max_mm\r\n")
        for (t0, t1, d, k, rows) in WD["radar"]:
            y = int(str(iso(t0))[:4])
            seqs[y] = seqs.get(y, 0) + 1
            cid = "%d-%04d" % (y, seqs[y])
            a, z = str(iso(t0))[:16].replace("T", " "), str(iso(t1))[:16].replace("T", " ")
            ids = old if y <= 2018 else new
            core_n = 1 + len(WD["W"][d]["pts"])
            for j, (pix, v) in enumerate(sorted(rows[:core_n] + [x for x in rows[core_n:] if x[1] >= 0.05],
                                                key=lambda x: ids[x[0]])):
                f.write("%s,%s,%s,%d,%.2f\r\n" % (cid, a, z, ids[pix], v))
                n += 1
    with open(os.path.join(target, FILES["pixels"]), "w", newline="") as f:
        f.write("pixel,pixel_until_2018,x_centre_etrs89_utm33n_m,y_centre_etrs89_utm33n_m\r\n")
        for pn in range(WL.GRID_N[1] - 1, WL.GRID_N[0] - 1, -1):
            for pe in range(WL.GRID_E[0], WL.GRID_E[1]):
                f.write("%d,%d,%d,%d\r\n" % (new[(pe, pn)], old[(pe, pn)], pe * 1000 + 500, pn * 1000 + 500))
    return n


def write_normal(target, WD):
    cx, cy, field, _ = WD["normal"]
    with open(os.path.join(target, FILES["normal"]), "w", newline="") as f:
        f.write("x_centre_etrs89_utm33n_m,y_centre_etrs89_utm33n_m,precip_1991_2020_mm\r\n")
        for j in range(len(cy) - 1, -1, -1):
            for i in range(len(cx)):
                f.write("%d,%d,%d\r\n" % (cx[i], cy[j], field[j, i]))
    return field.size


def write_research(target, WD):
    with open(os.path.join(target, FILES["rs_events"]), "w", newline="") as f:
        f.write("gauge,event_start_utc,event_end_utc,p60_max_mm\r\n")
        for (t0, t1, s, _, v) in WD["research"]:
            f.write("%s,%s,%s,%.2f\r\n" % (GAUGE_ID[s], str(iso(t0))[:16].replace("T", " "), str(iso(t1))[:16].replace("T", " "), v))
    site = {"Scuro 1": "Ghiaion Bas", "Scuro 2": "Val dei Camosci", "Scuro 3": "Ghiaion Alt", "Scuro 4": "Forca Scura"}
    with open(os.path.join(target, FILES["rs_gauges"]), "w", newline="") as f:
        wr = csv.writer(f)
        wr.writerow(["gauge", "site", "x_etrs89_utm33n_m", "y_etrs89_utm33n_m", "elevation_m", "gauge_type",
                     "resolution_mm", "in_service_from", "in_service_to", "triggering_depth_point_mm_60min"])
        for s in C.RESEARCH:
            e, n = WL.point(s)
            wr.writerow([GAUGE_ID[s], site[s], e, n, WL.SOURCES[s][2], "weighing, 200 cm2 orifice, wind shield", "0.01",
                         "2013-04-%02d" % (16 + list(C.RESEARCH).index(s) // 2), "2026-11-05", "%.1f" % C.RESEARCH[s]["T"]])
    return len(WD["research"])


def write_daily(target, WD):
    """Ardesa Centro's daily manual gauge, read at 08:00: the valley's long rain on its days, showers of its own, and
    the cold season from a monthly climate. Not used by the analysis."""
    r = WL.rng(12)
    wetp = [0.26, 0.25, 0.29, 0.36, 0.42, 0.44, 0.40, 0.38, 0.33, 0.34, 0.36, 0.28]
    mean = [8.8, 8.9, 10.2, 11.4, 11.9, 11.6, 11.2, 12.0, 14.8, 16.2, 16.6, 11.2]
    day0, day1 = dt.date(1961, 1, 1), dt.date(2026, 10, 31)
    nd = (day1 - day0).days + 1
    rain = np.zeros(nd)
    for i in range(nd):
        m = (day0 + dt.timedelta(days=i)).month - 1
        if r.random() < wetp[m]:
            rain[i] = r.gamma(0.78, mean[m] / 0.78)
    kap = C.KAPPA["A"]
    for s, y in enumerate(WL.YEARS):                  # the seasons the road stations cover: the valley's own spells
        a = (dt.date(y, 4, 21) - day0).days
        z = min((dt.date(y, 11, 8) - day0).days, nd)
        rain[a:z] = np.where(r.random(z - a) < 0.2, r.gamma(0.7, 6.0, z - a), 0.0)
        for (ss, _, st, hours) in WD["spells"]["Pradalt"]:
            if ss != s:
                continue
            true = hours / (1.0 - kap * hours)
            f = 0.9 * math.exp(0.2 * r.standard_normal())
            for h, v in enumerate(true):
                t = WL.EPOCH + dt.timedelta(seconds=int(st + 3600 * h) - 8 * 3600 + 86400)
                k = (t.date() - day0).days
                if k < nd:
                    rain[k] += f * v
    gaps = [(dt.date(1976, 5, 7), dt.date(1976, 9, 30)), (dt.date(1993, 11, 2), dt.date(1993, 12, 19)),
            (dt.date(2003, 1, 14), dt.date(2003, 2, 3))]
    n = 0
    with open(os.path.join(target, FILES["daily"]), "w", newline="") as f:
        f.write("date,precip_mm,fresh_snow_cm,qc\r\n")
        for i in range(nd):
            d = day0 + dt.timedelta(days=i)
            if any(a <= d <= z for a, z in gaps):
                f.write("%s,,,M\r\n" % d.isoformat())
                n += 1
                continue
            v = round(float(rain[i]), 1)
            snow, flag = "", ""
            if v > 0 and d.month in (11, 12, 1, 2, 3) and r.random() < (0.55 if d.month in (12, 1, 2) else 0.25):
                snow = "%d" % max(1, int(round(v * r.uniform(0.6, 1.2))))
            if v == 0.0 and r.random() < 0.03:
                flag = "T"
            elif v > 0 and r.random() < 0.012:
                flag = "E"
            f.write("%s,%.1f,%s,%s\r\n" % (d.isoformat(), v, snow, flag))
            n += 1
    return n


def write_traffic(target):
    """Daily counts at the three permanent counting sections of the SP 141. Not used by the analysis."""
    r = WL.rng(13)
    sec = [("S1", "km 2.1 Ponte Ardesa", 3420, 0.074), ("S2", "km 12.8 Pradalt", 2090, 0.061), ("S3", "km 30.4 Costarossa", 870, 0.038)]
    day0, day1 = dt.date(2019, 1, 1), dt.date(2026, 10, 31)
    n = 0
    with open(os.path.join(target, FILES["traffic"]), "w", newline="") as f:
        f.write("date,section,location,vehicles,heavy_vehicles,status\r\n")
        d = day0
        while d <= day1:
            doy = d.timetuple().tm_yday
            season = 1.0 + 0.52 * math.exp(-((doy - 213) / 34.0) ** 2) + 0.16 * math.exp(-((doy - 45) / 22.0) ** 2)
            wk = 1.0 + (0.24 if d.weekday() >= 5 else 0.0) * (1.4 if 150 < doy < 260 else 0.6)
            covid = 0.31 if dt.date(2020, 3, 10) <= d <= dt.date(2020, 5, 3) else (0.72 if dt.date(2020, 5, 4) <= d <= dt.date(2020, 6, 14) else 1.0)
            trend = 1.0 + 0.011 * (d.year - 2019)
            for code, loc, base, heavy in sec:
                closed = code == "S3" and (d.month in (12, 1, 2, 3) or (d.month == 11 and d.day >= 12) or (d.month == 4 and d.day <= 18 + (d.year % 5)))
                if closed:
                    f.write("%s,%s,%s,,,pass closed\r\n" % (d.isoformat(), code, loc))
                elif r.random() < 0.006:
                    f.write("%s,%s,%s,,,counter fault\r\n" % (d.isoformat(), code, loc))
                else:
                    v = int(r.poisson(base * season * wk * covid * trend * math.exp(0.07 * r.standard_normal())))
                    hv = int(r.binomial(v, heavy * (0.45 if d.weekday() >= 5 else 1.12)))
                    f.write("%s,%s,%s,%d,%d,\r\n" % (d.isoformat(), code, loc, v, hv))
                n += 1
            d += dt.timedelta(days=1)
    return n


def build(WD, target):
    TX = texture(WD)
    out = {"tips": write_tips(target, WD, TX), "visits": write_visits(target, WD, TX),
           "detector": write_detector(target, WD), "radar": write_radar(target, WD),
           "normal": write_normal(target, WD), "research": write_research(target, WD),
           "daily": write_daily(target, WD), "traffic": write_traffic(target)}
    return out, TX
