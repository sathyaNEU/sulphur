"""task3 architecture 3: the data files of the pack, written the way each office's system writes them.

The consultant's logger export for the September 2026 test (two logger brands, two clocks, absolute pressure), the
on-site barologger, the field notes workbook, the August step test, Harlow Springs' monthly operating report
extract, the Mill Street monitoring well's tape readings, the district's network export and its well register,
and the raw-water quality workbook."""
import calendar
import csv
import datetime as dt
import io
import math

import numpy as np
import openpyxl
from openpyxl.styles import Alignment, Font

import ooxml
import params as P
import world as W

UTC = dt.timezone.utc
EDT = W.EDT
EST = dt.timezone(dt.timedelta(hours=-5))
PSI_FT = 0.43353        # psi per foot of fresh water at about 12 C

# ground and measuring point elevations (ft NAVD88); MP history where a measuring point moved
GROUND = {"TW-1": 757.8, "TW-2": 757.1, "MS-MW": 758.6, "PW-1": 754.2, "PW-2": 754.0, "OW-1": 754.4,
          "OW-2": 755.9, "OW-3": 753.1, "OW-S": 755.3, "CV-07": 758.9, "CV-02": 771.4, "CV-11": 741.6,
          "CV-04": 756.2, "CV-09": 764.8, "CV-13": 803.7, "CV-05": 768.2,
          "DW-17": 761.9, "DW-22": 752.6, "DW-09": 765.3}
STICKUP = {"TW-1": 1.1, "TW-2": 1.3, "MS-MW": 2.42, "PW-1": 1.6, "PW-2": 1.5, "OW-1": 2.31, "OW-2": 2.74,
           "OW-3": 2.18, "OW-S": 2.63, "CV-07": 2.21, "CV-02": 2.95, "CV-11": 1.87, "CV-04": 2.40, "CV-09": 2.66,
           "CV-13": 1.94, "CV-05": 2.37, "DW-17": 1.0, "DW-22": 1.2,
           "DW-09": 0.9}
MS_MW_MP_RAISE = (dt.date(2017, 4, 11), 2.15)      # a casing extension after the flood-proofing of the pad
CV07_MP_RESET = (dt.date(2013, 8, 6), -0.58)       # cut down after a mower strike, MP re-surveyed


def static_elev(w):
    a = P.WELLS[w][0]
    if w in ("CV-04", "CV-09"):
        return 744.0 - 0.0007 * a
    if w == "CV-13":
        return 768.0 - 0.0002 * a
    return 731.4 - 0.00062 * a


def mp_elev(w, day=None):
    e = GROUND[w] + STICKUP[w]
    if w == "MS-MW" and day is not None and day >= MS_MW_MP_RAISE[0]:
        e += MS_MW_MP_RAISE[1]
    if w == "CV-07" and day is not None and day < CV07_MP_RESET[0]:
        e -= CV07_MP_RESET[1]
    return round(e, 2)


def _csv(rows, header):
    buf = io.StringIO()
    wr = csv.writer(buf, lineterminator="\r\n")
    wr.writerow(header)
    wr.writerows(rows)
    return buf.getvalue().encode("utf-8")


# ---------------------------------------------------------------- the September 2026 test

LOGGERS = [  # well, model, serial, clock, sensor depth below MP (ft)
    ("PW-1", "Level TROLL 400", "852214", "local", 96.50),
    ("PW-2", "Level TROLL 400", "852230", "local", 88.00),
    ("OW-1", "Level TROLL 400", "852219", "local", 74.20),
    ("OW-2", "Levelogger 5", "2109347", "utc", 61.03),
    ("OW-3", "Levelogger 5", "2109351", "utc", 63.80),
    ("OW-S", "Levelogger 5", "2109362", "utc", 66.45),
]
OW2_REHANG = (dt.datetime(2026, 9, 12, 14, 20, tzinfo=EDT), 62.40)
OW3_DOWNLOAD = dt.datetime(2026, 9, 12, 14, 5, tzinfo=EDT)


def test_series(truth, rng):
    """Depth to water (ft below MP) minute by minute at each logged well, and the barometer, the truth behind the
    logger file; also the times, the rate steps and the static level each well started from."""
    stamps, tdays, on = W.test_clock()
    baro = W.barometer(tdays, rng)
    steps = W.test_rate_steps()
    i_sep = W.MI[(2026, 9)]
    out = {}
    for w, _, _, _, _ in LOGGERS:
        lvl0 = static_elev(w) + truth["nat"][w][i_sep] - truth["draw"][w][i_sep]
        dd = W.test_drawdown(tdays, w, steps)
        if w == "PW-1":
            q = np.interp(tdays, [s[0] for s in steps], [s[1] for s in steps])
            q = np.where((tdays >= 0) & (tdays < P.TEST_HOURS / 24.0), q, 0.0)
            dd = dd + 3.05e-6 * q * q + 1.1e-3 * q
            dd += np.where(q > 0, rng.normal(0, 0.012, len(tdays)), 0)
        dbaro_ft = (baro - baro[0]) / PSI_FT
        lvl = lvl0 - dd - 0.0058 * (tdays - tdays[0]) - P.BE * dbaro_ft + W.earth_tide(tdays, 0.011)
        lvl += rng.normal(0, 0.0025, len(tdays))
        out[w] = mp_elev(w) - lvl
    return stamps, tdays, on, baro, steps, out


def write_test(paths, truth, rng):
    stamps, tdays, on, baro, steps, dtw = test_series(truth, rng)
    rows = []
    for w, model, sn, clock, depth in LOGGERS:
        for k, s in enumerate(stamps):
            sensor = depth
            if w == "OW-2" and s >= OW2_REHANG[0]:
                sensor = OW2_REHANG[1]
            if w == "OW-2" and OW2_REHANG[0] - dt.timedelta(minutes=7) <= s < OW2_REHANG[0]:
                continue                                        # lifted for the download
            col = sensor - dtw[w][k]
            psi = col * PSI_FT + baro[k] + rng.normal(0, 0.0012)
            temp = 12.6 + 0.02 * math.sin(k / 900.0) + (0.4 if w == "PW-1" and 0 <= tdays[k] < 3 else 0.0)
            when = s.astimezone(UTC) if clock == "utc" else s
            rows.append((w, sn, when.strftime("%Y-%m-%d %H:%M:%S"), "%.4f" % psi, "%.2f" % temp))
            if w == "OW-3" and s == OW3_DOWNLOAD:                # the logger rewrites its last three records
                rows.extend(rows[-4:-1])
    open(paths["transducers"], "wb").write(_csv(rows, ["well_id", "logger_sn", "date_time", "pressure_psi",
                                                       "temperature_c"]))
    brow = []
    for k in range(0, len(stamps), 5):
        brow.append((stamps[k].astimezone(UTC).strftime("%Y-%m-%d %H:%M:%S"), "%.4f" % (baro[k] + rng.normal(0, 4e-4)),
                     "%.2f" % (17.5 + 6 * math.sin(2 * math.pi * (tdays[k] - 0.3)))))
    open(paths["baro"], "wb").write(_csv(brow, ["date_time_utc", "pressure_psi", "temperature_c"]))
    _field_notes(paths["notes"], stamps, tdays, on, steps, dtw, rng)
    return {"rows": len(rows), "steps": steps}


def _field_notes(path, stamps, tdays, on, steps, dtw, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Loggers"
    ws.append(["Well", "Logger", "Serial", "Clock", "Interval", "Sensor depth below MP (ft)", "Set", "Notes"])
    for w, model, sn, clock, depth in LOGGERS:
        clk = "UTC" if clock == "utc" else "Local (EDT)"
        ws.append([w, model, sn, clk, "1 min", depth, "2026-09-08 11:40" if w != "OW-S" else "2026-09-08 12:05",
                   "absolute (non-vented) sensor"])
    ws.append(["OW-2", "Levelogger 5", "2109347", "UTC", "1 min", OW2_REHANG[1], "2026-09-12 14:20",
               "downloaded and re-hung after the cable clip slipped"])
    ws.append(["Site", "Barologger 5", "2109388 (BL-2231)", "UTC", "5 min", None, "2026-09-08 11:30",
               "in the PW-1 well house, above flood level"])
    ws2 = wb.create_sheet("Manual levels")
    ws2.append(["Date", "Time (EDT)", "Well", "Depth to water (ft below MP)", "By", "Remark"])
    times = [dt.datetime(2026, 9, 8, 11, 35), dt.datetime(2026, 9, 12, 14, 12), dt.datetime(2026, 9, 14, 8, 40),
             dt.datetime(2026, 9, 14, 10, 30), dt.datetime(2026, 9, 14, 15, 0), dt.datetime(2026, 9, 15, 9, 15),
             dt.datetime(2026, 9, 16, 9, 5), dt.datetime(2026, 9, 17, 8, 50), dt.datetime(2026, 9, 17, 9, 40),
             dt.datetime(2026, 9, 18, 9, 30), dt.datetime(2026, 9, 20, 11, 50)]
    who = ["M. Munoz", "T. Robinson"]
    for i, tm in enumerate(times):
        for w, _, _, _, _ in LOGGERS:
            if w == "PW-1" and 0 < (tm.replace(tzinfo=EDT) - on).total_seconds() / 86400 < 3:
                continue          # no tape down the pumping well while the pump runs
            k = int(round((tm.replace(tzinfo=EDT) - stamps[0]).total_seconds() / 60))
            val = dtw[w][k] + rng.normal(0, 0.006)
            ws2.append([tm.date().isoformat(), tm.strftime("%H:%M"), w, round(val, 2), who[i % 2],
                        "steel tape" if w != "PW-1" else "e-tape"])
    ws3 = wb.create_sheet("Discharge")
    ws3.append(["Date", "Time (EDT)", "Totalizer (gal)", "Rate (gpm)", "Remark"])
    tot = 4418200.0
    last = 0.0
    q_at = lambda td: next((r for t0, r in reversed(steps) if td >= t0), 0.0)
    for hh in [0, 0.25, 0.5, 1, 2, 3, 4, 6, 8, 10, 12, 16, 20, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 71.9]:
        td = hh / 24.0
        # totalizer integrates the hourly rate
        vol = 0.0
        for (t0, r), (t1, _) in zip(steps[:-1], steps[1:]):
            a, b = max(t0, last), min(t1, td)
            if b > a:
                vol += r * (b - a) * 1440
        tot += vol
        last = td
        tm = on + dt.timedelta(days=td)
        ws3.append([tm.date().isoformat(), tm.strftime("%H:%M"), int(round(tot)), round(q_at(td) + rng.normal(0, 1.5)),
                    "pump on, gate valve set" if hh == 0 else ("valve opened a quarter turn" if hh == 8 else "")])
    ws4 = wb.create_sheet("Events")
    ws4.append(["Date", "Time (EDT)", "Event"])
    for tm, ev in [(dt.datetime(2026, 9, 8, 11, 30), "Loggers set in PW-1, PW-2, OW-1, OW-2, OW-3, OW-S; barologger in well house"),
                   (dt.datetime(2026, 9, 12, 14, 5), "OW-3 downloaded"),
                   (dt.datetime(2026, 9, 12, 14, 13), "OW-2 downloaded, cable clip had slipped; re-hung, see Loggers"),
                   (dt.datetime(2026, 9, 14, 9, 0), "PW-1 pump on; discharge to Hollins Ditch 1,650 ft east of the well field"),
                   (dt.datetime(2026, 9, 14, 17, 0), "Valve adjusted to hold about 1,010 gpm"),
                   (dt.datetime(2026, 9, 16, 6, 0), "Rain overnight, front passing; 0.6 in at the site gauge"),
                   (dt.datetime(2026, 9, 17, 9, 0), "PW-1 pump off; recovery begins"),
                   (dt.datetime(2026, 9, 20, 12, 0), "Loggers pulled; test complete"),
                   (dt.datetime(2026, 9, 20, 12, 10), "Mill Street wells ran on their normal schedule throughout")]:
        ws4.append([tm.date().isoformat(), tm.strftime("%H:%M"), ev])
    for s in wb.worksheets:
        for col in s.columns:
            s.column_dimensions[col[0].column_letter].width = max(10, min(70, max(len(str(c.value or "")) for c in col) + 2))
        for c in s[1]:
            c.font = Font(bold=True)
    wb.properties.creator = "Tillbrook Hydrogeologic"
    wb.properties.lastModifiedBy = "Tillbrook Hydrogeologic"
    wb.save(path)
    ooxml.normalize(path, dt.datetime(2026, 9, 14, 7, 55), dt.datetime(2026, 9, 21, 15, 12), "Tillbrook Hydrogeologic")


def write_step_test(path, rng):
    """The August step test at PW-1: four 100-minute steps, the pumping well alone, local time."""
    t0 = dt.datetime(2026, 8, 27, 8, 0, tzinfo=EDT)
    rates = [(0, 0), (60, 410), (160, 615), (260, 820), (360, 1020), (460, 0)]
    rows = []
    for k in range(0, 640):
        t = k
        q = [r for s, r in rates if t >= s][-1]
        steps = [(s / 1440.0, r) for s, r in rates]
        dd = 0.0
        prev = 0.0
        import aquifer as A
        for (s, r) in steps:
            if t / 1440.0 > s:
                dq = (r - prev) * P.GPM
                dd += dq * float(A.step_response(P.T, P.S, P.B, P.WELLS["PW-1"], (P.WELLS["PW-1"][0], P.WELLS["PW-1"][1] + 0.5),
                                                 [t / 1440.0 - s], P.WIDTH)[0])
            prev = r
        dd += 3.05e-6 * q * q + 1.1e-3 * q
        dtw = 31.42 + dd + rng.normal(0, 0.01)
        rows.append(((t0 + dt.timedelta(minutes=t)).strftime("%m/%d/%Y %H:%M"), "%.2f" % dtw, q if q else ""))
    open(path, "wb").write(_csv(rows, ["Date Time (EDT)", "Depth to water (ft below MP)", "Step rate (gpm)"]))


# ---------------------------------------------------------------- long-term records

def _read_day(y, m, rng, lo=3, hi=13):
    d = int(rng.integers(lo, hi))
    while dt.date(y, m, d).weekday() >= 5:
        d += 1
    return dt.date(y, m, d)


def write_mor(path, truth, rng):
    q1, q2 = truth["q1"], truth["q2"]
    rows = []
    for i, (y, m) in enumerate(W.MONTHS):
        if (y, m) < P.TOWN_START or (y, m) > W.DATA_END:
            continue
        days = calendar.monthrange(y, m)[1]
        for well, q in (("TW-1", q1[i]), ("TW-2", q2[i])):
            if well == "TW-2" and (y, m) < P.TW2_START:
                continue
            gal = q * days * 1440
            hours = gal / (1150.0 if well == "TW-1" else 980.0) / 60.0
            old = (y, m) < (2016, 7)
            name = {"TW-1": "WELL 1", "TW-2": "WELL 2"}[well] if old else well
            meter = ("M-1187" if (y, m) < (2019, 5) else "M-5530") if well == "TW-1" else "M-2204"
            remark = ""
            vol = gal / 1000.0 if old else gal
            if well == "TW-1" and (y, m) == (2019, 5):
                remark = "meter replaced 5/14; month from run hours x 1,150 gpm"
                vol = round(hours * 60 * 1150)
            elif well == "TW-1" and (y, m) == (2018, 3):
                remark = "pump and motor replaced, well out of service"
            elif well == "TW-2" and (y, m) in ((2021, 10), (2021, 11)):
                remark = "screen redevelopment" if (y, m) == (2021, 10) else "back in service 11/29"
            vtxt = ("%.1f" % vol) if old else ("%d" % int(round(vol)))
            rows.append(("%04d-%02d" % (y, m), name, vtxt, "1000 gal" if old else "gal", meter,
                         "%.1f" % hours, remark))
    open(path, "wb").write(_csv(rows, ["report_month", "source", "metered_volume", "units", "meter_id",
                                       "run_hours", "remarks"]))
    return len(rows)


def _level(w, i, truth, rng, noise=0.03):
    return static_elev(w) + truth["nat"][w][i] - truth["draw"][w][i] + rng.normal(0, noise)


def write_msmw(path, truth, rng):
    rows = []
    for i, (y, m) in enumerate(W.MONTHS):
        if (y, m) < (2008, 6) or (y, m) > W.DATA_END:
            continue
        day = _read_day(y, m, rng, 2, 11)
        lvl = _level("MS-MW", i, truth, rng)
        running = (y, m) >= P.TOWN_START and rng.random() < 0.08
        remark = ""
        if running:
            lvl -= 0.8 + 0.5 * rng.random()        # the short-term cone of TW-1 running at the hour of reading
            remark = "TW-1 running"
        elif (y, m) >= P.TOWN_START and rng.random() < 0.5:
            remark = "TW-1 off %d hr" % int(rng.integers(2, 9))
        if (y, m) == (2017, 4):
            remark = (remark + "; " if remark else "") + "read from top of new casing extension (+2.15 ft) from 4/11"
        mp = mp_elev("MS-MW", day)
        hh = "%02d:%02d" % (int(rng.integers(7, 11)), int(rng.integers(0, 60)))
        rows.append((day.strftime("%m/%d/%Y"), hh, "%.2f" % (mp - lvl),
                     "top of casing" if day < MS_MW_MP_RAISE[0] else "top of casing extension",
                     ["WR", "WR", "MA", "J. Ponce"][int(rng.integers(0, 4))], remark))
    open(path, "wb").write(_csv(rows, ["date", "time", "depth_to_water_ft", "measured_from", "by", "remarks"]))
    return len(rows)


NET_START = {"OW-S": (2005, 1), "CV-02": (2005, 1), "CV-04": (2005, 1), "CV-07": (2005, 1), "CV-09": (2005, 1),
             "CV-11": (2005, 1), "CV-13": (2006, 4), "CV-05": (2016, 5)}


def write_network(path, truth, rng):
    rows = []
    for i, (y, m) in enumerate(W.MONTHS):
        if (y, m) > W.DATA_END:
            continue
        for w in P.NETWORK:
            if (y, m) < NET_START[w]:
                continue
            if (y, m) in ((2020, 4), (2020, 5)) or rng.random() < 0.012:
                continue                           # no field run, or the well not reached
            day = _read_day(y, m, rng)
            lvl = _level(w, i, truth, rng)
            mp = mp_elev(w, day)
            method = "steel tape" if (y < 2015 or w in ("CV-13", "CV-05")) else "electric tape"
            qual = ""
            remark = ""
            if w == "CV-07" and (y, m) == (2013, 8):
                remark = "casing cut down after mower strike 8/6; new MP surveyed"
            if rng.random() < 0.01:
                qual = "E"
                remark = "cascading water in casing; reading uncertain"
                lvl += rng.normal(0, 0.4)
            hh = "%02d:%02d" % (int(rng.integers(8, 15)), int(rng.integers(0, 60)))
            rows.append((w, day.isoformat(), hh, "%.2f" % (mp - lvl), method, qual, remark))
            if rng.random() < 0.008:                 # entered twice when the field sheet was keyed
                rows.append(rows[-1])
    open(path, "wb").write(_csv(rows, ["site_id", "date", "time", "dtw_ft_below_mp", "method", "qualifier",
                                       "remarks"]))
    return len(rows)


UNITS = {"BVA": "Corrin Valley buried valley aquifer (sand and gravel under till)",
         "SOW": "surficial outwash above the till",
         "BDR": "Devonian shale bedrock"}
OWNERS = {"DW-17": "private (registered 2019)", "DW-22": "private (registered 2019)",
          "DW-09": "private (registered 2020)", "TW-1": "Harlow Springs Utilities", "TW-2": "Harlow Springs Utilities", "MS-MW": "Harlow Springs Utilities",
          "PW-1": "Harlow Springs Utilities", "PW-2": "Harlow Springs Utilities", "OW-1": "Harlow Springs Utilities",
          "OW-2": "Harlow Springs Utilities", "OW-3": "Harlow Springs Utilities"}
PURPOSE = {"DW-17": "domestic", "DW-22": "domestic and livestock", "DW-09": "domestic", "TW-1": "public supply", "TW-2": "public supply", "PW-1": "public supply (proposed)",
           "PW-2": "public supply (proposed)", "MS-MW": "monitoring", "OW-1": "test observation",
           "OW-2": "test observation", "OW-3": "test observation", "OW-S": "sentinel (WR-4 Table 1)"}
SCREEN = {"TW-1": (96, 136), "TW-2": (94, 134), "MS-MW": (104, 114), "PW-1": (95, 135), "PW-2": (93, 133),
          "OW-1": (108, 118), "OW-2": (102, 112), "OW-3": (105, 115), "OW-S": (100, 110), "CV-07": (98, 108),
          "CV-02": (121, 131), "CV-11": (82, 92), "CV-04": (14, 24), "CV-09": (18, 28), "CV-13": (160, 220),
          "CV-05": (110, 120), "DW-17": (88, 96), "DW-22": (79, 87), "DW-09": (101, 109)}
INSTALLED = {"TW-1": "2008-05-20", "TW-2": "2013-10-02", "MS-MW": "2008-05-29", "PW-1": "2026-06-11",
             "PW-2": "2026-06-30", "OW-1": "2026-07-14", "OW-2": "2026-07-15", "OW-3": "2026-07-16",
             "DW-17": "1997-05-14", "DW-22": "2003-08-29", "DW-09": "1988-10-03", "OW-S": "2004-09-21", "CV-07": "2004-10-05", "CV-02": "2004-08-17", "CV-11": "2004-11-03",
             "CV-04": "2004-10-06", "CV-09": "2004-08-24", "CV-13": "2006-03-15", "CV-05": "2016-04-26"}


def write_register(path):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Wells"
    ws.append(["Well ID", "Owner", "Purpose", "Easting (ft)", "Northing (ft)", "Ground elev (ft)", "MP elev (ft)",
               "Screen top (ft bgs)", "Screen bottom (ft bgs)", "Unit", "Installed", "Status"])
    order = ["OW-S", "CV-02", "CV-04", "CV-05", "CV-07", "CV-09", "CV-11", "CV-13", "TW-1", "TW-2", "MS-MW",
             "PW-1", "PW-2", "OW-1", "OW-2", "OW-3", "DW-09", "DW-17", "DW-22"]
    for w in order:
        x, y = W.xy(P.WELLS[w])
        unit = "SOW" if w in ("CV-04", "CV-09") else ("BDR" if w == "CV-13" else "BVA")
        ws.append([w, OWNERS.get(w, "CVWCD"), PURPOSE.get(w, "network monitoring"), round(x, 1), round(y, 1),
                   GROUND[w], mp_elev(w, dt.date(2026, 10, 1)), SCREEN[w][0], SCREEN[w][1], unit, INSTALLED[w],
                   "active"])
    ws2 = wb.create_sheet("MP history")
    ws2.append(["Well ID", "From", "To", "MP elev (ft)", "Note"])
    ws2.append(["MS-MW", "2008-05-29", "2017-04-10", mp_elev("MS-MW", dt.date(2010, 1, 1)), "top of PVC casing"])
    ws2.append(["MS-MW", "2017-04-11", "", mp_elev("MS-MW", dt.date(2020, 1, 1)), "top of casing extension"])
    ws2.append(["CV-07", "2004-10-05", "2013-08-05", mp_elev("CV-07", dt.date(2010, 1, 1)), "top of steel casing"])
    ws2.append(["CV-07", "2013-08-06", "", mp_elev("CV-07", dt.date(2020, 1, 1)), "casing cut down, resurveyed"])
    ws3 = wb.create_sheet("Units")
    ws3.append(["Code", "Unit"])
    for k, v in UNITS.items():
        ws3.append([k, v])
    ws4 = wb.create_sheet("Datum")
    for line in ["Coordinates: Indiana State Plane East (NAD83), US survey feet.",
                 "Elevations: NAVD88, feet. Ground elevations from the 2019 district LiDAR, MP elevations by level loop.",
                 "Depths below ground surface (bgs) from the drillers' logs."]:
        ws4.append([line])
    for s in wb.worksheets:
        for col in s.columns:
            s.column_dimensions[col[0].column_letter].width = max(9, min(60, max(len(str(c.value or "")) for c in col) + 2))
        for c in s[1]:
            c.font = Font(bold=True)
    wb.properties.creator = "Corrin Valley Water Conservancy District"
    wb.properties.lastModifiedBy = "Corrin Valley Water Conservancy District"
    wb.save(path)
    ooxml.normalize(path, dt.datetime(2019, 3, 4, 13, 20), dt.datetime(2026, 10, 2, 13, 41),
                    "Corrin Valley Water Conservancy District")


def write_water_quality(path, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "PW-1 raw water"
    ws.append(["Sample", "Collected", "Analyte", "Result", "Units", "MDL", "Method", "Lab"])
    analytes = [("Iron", 1.42, "mg/L", 0.02, "EPA 200.7"), ("Manganese", 0.118, "mg/L", 0.002, "EPA 200.8"),
                ("Hardness as CaCO3", 362, "mg/L", 2, "SM 2340B"), ("Nitrate as N", 0.31, "mg/L", 0.05, "EPA 300.0"),
                ("Chloride", 41.8, "mg/L", 0.5, "EPA 300.0"), ("Sulfate", 66.2, "mg/L", 0.5, "EPA 300.0"),
                ("Total dissolved solids", 512, "mg/L", 10, "SM 2540C"), ("Arsenic", 0.0021, "mg/L", 0.0005, "EPA 200.8"),
                ("Ammonia as N", 0.44, "mg/L", 0.05, "SM 4500-NH3"), ("pH (field)", 7.21, "s.u.", None, "field meter")]
    for k, when in enumerate(["2026-09-14 10:15", "2026-09-15 14:30", "2026-09-17 08:40"]):
        for a, v, u, mdl, meth in analytes:
            val = v * math.exp(rng.normal(0, 0.05))
            ws.append(["PW1-%d" % (k + 1), when, a, round(val, 4 if val < 0.01 else 3 if val < 1 else 1), u, mdl,
                       meth, "Heartland Environmental Laboratories"])
    for col in ws.columns:
        ws.column_dimensions[col[0].column_letter].width = max(9, min(40, max(len(str(c.value or "")) for c in col) + 2))
    for c in ws[1]:
        c.font = Font(bold=True)
    wb.properties.creator = "Heartland Environmental Laboratories"
    wb.properties.lastModifiedBy = "Tillbrook Hydrogeologic"
    wb.save(path)
    ooxml.normalize(path, dt.datetime(2026, 10, 1, 16, 2), dt.datetime(2026, 10, 5, 10, 18), "Tillbrook Hydrogeologic")
