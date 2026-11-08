"""task3 architecture 3: everything owed, computed from the cut pack alone.

The golden path: the test's loggers compensated and put on one clock, the barometric response and the background
trend taken out, the Theis fit to the three observation wells (the test's transmissivity and storativity); the Mill
Street wells' monthly pumping from the operating reports; each monitoring well's natural level from the two
confined-aquifer network wells beyond the Mill Street cone (CV-02 and CV-11), the drawdown the Mill Street wells
caused being that natural level less the reading; the leakage factor that makes the bounded leaky aquifer (walls at
the plate's mapped edges) reproduce that drawdown at MS-MW, CV-07 and OW-S from March 2009 to September 2026; and the monthly forecast at OW-S
for 2027 to 2046 under the town's projection and each requested schedule. Every rung and rival of the design note
runs through the same functions with one switch changed."""
import calendar
import csv
import datetime as dt
import math
import os
from functools import lru_cache

import numpy as np
import openpyxl

import aquifer as A

UTC = dt.timezone.utc
EDT = dt.timezone(dt.timedelta(hours=-4))
PSI_FT = 0.43353
GPM = 192.5
LIMIT = 9.0
OPTIONS = [450, 700, 1000, 1250]
FILES = {
    "transducers": "PW-1_constant_rate_2026-09_transducers.csv",
    "baro": "barologger_BL-2231_2026-09.csv",
    "notes": "PW-1_constant_rate_2026-09_field_readings.xlsx",
    "mor": "harlow_springs_MOR_well_production_2009-2026.csv",
    "msmw": "mill_street_MW_water_levels_2008-2026.csv",
    "network": "cvwcd_network_water_levels_2005-2026.csv",
    "register": "cvwcd_well_register.xlsx",
}
# read off Plate 3 and the application: the valley axis bears N 18 E and the mapped edges of the saturated sand and
# gravel run parallel to it 5,000 ft apart; the edge west of TW-1 passes through (409,800, 1,687,555)
PLATE = {"az_deg": 18.0, "width": 5000.0, "west_edge_point": (409800.0, 1687555.0)}
NEW_SEASON = [0.78, 0.76, 0.80, 0.88, 1.02, 1.21, 1.34, 1.31, 1.17, 0.98, 0.88, 0.87]
TOWN_FACTORS = [0.81, 0.80, 0.84, 0.90, 1.03, 1.17, 1.25, 1.23, 1.11, 0.98, 0.95, 0.93]
TOWN_2026 = 548.0
TOWN_GROWTH = 0.012


def months(y0=2005, m0=1, y1=2046, m1=12):
    out, y, m = [], y0, m0
    while (y, m) <= (y1, m1):
        out.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    return out


MONTHS = months()
MI = {ym: i for i, ym in enumerate(MONTHS)}
N = len(MONTHS)
YR = np.array([y for y, _ in MONTHS])


# ---------------------------------------------------------------- reading the pack

def register(target):
    wb = openpyxl.load_workbook(os.path.join(target, FILES["register"]), read_only=True)
    rows = list(wb["Wells"].iter_rows(values_only=True))
    hdr = rows[0]
    reg = {r[0]: dict(zip(hdr, r)) for r in rows[1:] if r[0]}
    mph = [r for r in wb["MP history"].iter_rows(values_only=True)][1:]
    return reg, mph


def valley_frame(reg, width=None):
    """Valley coordinates (a along the axis, c across from the centre line) of every well, from the plate."""
    az = math.radians(PLATE["az_deg"])
    ua = (math.sin(az), math.cos(az))
    uc = (math.cos(az), -math.sin(az))
    wx, wy = PLATE["west_edge_point"]
    # centre line: half a width east-south-east of the west edge
    cx, cy = wx + uc[0] * PLATE["width"] / 2, wy + uc[1] * PLATE["width"] / 2
    out = {}
    for w, r in reg.items():
        dx, dy = r["Easting (ft)"] - cx, r["Northing (ft)"] - cy
        out[w] = (dx * ua[0] + dy * ua[1], dx * uc[0] + dy * uc[1])
    return out


def mp_at(w, day, reg, mph):
    for r in mph:
        if r[0] != w:
            continue
        f = dt.date.fromisoformat(r[1])
        t = dt.date.fromisoformat(r[2]) if r[2] else dt.date(2100, 1, 1)
        if f <= day <= t:
            return float(r[3])
    return float(reg[w]["MP elev (ft)"])


def town_pumping(target):
    q = {"TW-1": np.zeros(N), "TW-2": np.zeros(N)}
    with open(os.path.join(target, FILES["mor"]), newline="") as f:
        for r in csv.DictReader(f):
            y, m = map(int, r["report_month"].split("-"))
            well = {"WELL 1": "TW-1", "WELL 2": "TW-2"}.get(r["source"], r["source"])
            v = float(r["metered_volume"]) * (1000.0 if r["units"] == "1000 gal" else 1.0)
            q[well][MI[(y, m)]] = v / (calendar.monthrange(y, m)[1] * 1440.0)
    return q


def town_projection():
    out = np.zeros(N)
    for i, (y, m) in enumerate(MONTHS):
        if (y, m) >= (2026, 10):
            out[i] = TOWN_2026 * (1 + TOWN_GROWTH) ** (y - 2026) * TOWN_FACTORS[m - 1]
    return out


def levels(target, reg, mph, keep_running=False):
    """Monthly water-level elevation (ft) at MS-MW and each network well; NaN where no usable reading."""
    lv = {}
    with open(os.path.join(target, FILES["msmw"]), newline="") as f:
        s = np.full(N, np.nan)
        for r in csv.DictReader(f):
            if "TW-1 running" in r["remarks"] and not keep_running:
                continue
            day = dt.datetime.strptime(r["date"], "%m/%d/%Y").date()
            s[MI[(day.year, day.month)]] = mp_at("MS-MW", day, reg, mph) - float(r["depth_to_water_ft"])
        lv["MS-MW"] = s
    seen = set()
    with open(os.path.join(target, FILES["network"]), newline="") as f:
        for r in csv.DictReader(f):
            key = (r["site_id"], r["date"])
            if key in seen:
                continue
            seen.add(key)
            if r["qualifier"] == "E":
                continue
            day = dt.date.fromisoformat(r["date"])
            lv.setdefault(r["site_id"], np.full(N, np.nan))[MI[(day.year, day.month)]] = (
                mp_at(r["site_id"], day, reg, mph) - float(r["dtw_ft_below_mp"]))
    return lv


# ---------------------------------------------------------------- the test

def _notes(target):
    wb = openpyxl.load_workbook(os.path.join(target, FILES["notes"]), read_only=True)
    loggers = [r for r in wb["Loggers"].iter_rows(values_only=True)][1:]
    disch = [r for r in wb["Discharge"].iter_rows(values_only=True)][1:]
    return loggers, disch


_TEST = {}


def test_drawdowns(target, baro_correct=True, clock_naive=False, ignore_rehang=False):
    key = (os.path.abspath(target), baro_correct, clock_naive, ignore_rehang)
    if key not in _TEST:
        _TEST[key] = _test_drawdowns(target, baro_correct, clock_naive, ignore_rehang)
    return _TEST[key]


def _test_drawdowns(target, baro_correct=True, clock_naive=False, ignore_rehang=False):
    """Drawdown (ft) at each logged well against days since pump-on, with the test's average rate (gpm)."""
    loggers, disch = _notes(target)
    clock, depth, rehang = {}, {}, {}
    for r in loggers:
        if r[0] == "Site":
            continue
        if r[0] in clock and r[6] != clock.get(r[0] + "_set"):
            rehang[r[0]] = (dt.datetime.strptime(r[6], "%Y-%m-%d %H:%M").replace(tzinfo=EDT), float(r[5]))
            continue
        clock[r[0]] = r[3]
        clock[r[0] + "_set"] = r[6]
        depth[r[0]] = float(r[5])
    bt, bp = [], []
    with open(os.path.join(target, FILES["baro"]), newline="") as f:
        for r in csv.DictReader(f):
            bt.append(dt.datetime.strptime(r["date_time_utc"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=UTC).timestamp())
            bp.append(float(r["pressure_psi"]))
    bt, bp = np.array(bt), np.array(bp)
    on = dt.datetime(2026, 9, 14, 9, 0, tzinfo=EDT).timestamp()
    off = on + 3 * 86400
    data = {}
    with open(os.path.join(target, FILES["transducers"]), newline="") as f:
        rows = list(csv.DictReader(f))
    seen = set()
    for r in rows:
        w = r["well_id"]
        key = (w, r["date_time"])
        if key in seen:
            continue
        seen.add(key)
        tz = UTC if (clock[w] == "UTC" and not clock_naive) else EDT
        t = dt.datetime.strptime(r["date_time"], "%Y-%m-%d %H:%M:%S").replace(tzinfo=tz)
        d = depth[w]
        if w in rehang and t >= rehang[w][0] and not ignore_rehang:
            d = rehang[w][1]
        data.setdefault(w, []).append((t.timestamp(), float(r["pressure_psi"]), d))
    # average rate from the totalizer over the pumping period
    tot = [(dt.datetime.strptime(r[0] + " " + r[1], "%Y-%m-%d %H:%M").replace(tzinfo=EDT).timestamp(), r[2])
           for r in disch]
    q_avg = (tot[-1][1] - tot[0][1]) / ((tot[-1][0] - tot[0][0]) / 60.0)
    out = {}
    for w, v in data.items():
        v.sort()
        t = np.array([a for a, _, _ in v])
        p = np.array([b for _, b, _ in v])
        sd = np.array([c for _, _, c in v])
        baro = np.interp(t, bt, bp)
        dtw = sd - (p - baro) / PSI_FT
        lvl = -dtw
        pre = (t >= on - 5.5 * 86400) & (t < on - 60)
        tt = (t - on) / 86400.0
        # background: linear trend and barometric response fitted on the pre-test days, in first differences of
        # hourly means for the barometric efficiency
        be = 0.0
        if baro_correct:
            hh = np.floor(tt[pre] * 24)
            hl = np.array([lvl[pre][hh == h].mean() for h in np.unique(hh)])
            hb = np.array([baro[pre][hh == h].mean() for h in np.unique(hh)])
            dl, db = np.diff(hl), np.diff(hb) / PSI_FT
            X = np.column_stack([db, np.ones_like(db)])
            be = -np.linalg.lstsq(X, dl, rcond=None)[0][0]
        corr = lvl + be * (baro - baro[pre].mean()) / PSI_FT
        X = np.column_stack([np.ones(pre.sum()), tt[pre]])
        c0, c1 = np.linalg.lstsq(X, corr[pre], rcond=None)[0]
        dd = (c0 + c1 * tt) - corr
        out[w] = {"t": tt, "s": dd, "be": be}
    return out, q_avg


def theis_fit(test, q_avg, wells=("OW-1", "OW-2", "OW-3"), coords=None, t_lo=2 / 1440.0, t_hi=3.0):
    """Least-squares Theis fit of T and S to the pumping-period drawdowns of the observation wells."""
    obs = []
    for w in wells:
        t, s = test[w]["t"], test[w]["s"]
        m = (t >= t_lo) & (t <= t_hi)
        # thin to log-spaced samples so the late minutes do not swamp the fit
        idx = np.unique(np.searchsorted(t[m], np.logspace(np.log10(t_lo), np.log10(t_hi), 160)).clip(0, m.sum() - 1))
        r = coords[w]
        obs.append((r, t[m][idx], s[m][idx]))
    Q = q_avg * GPM

    def sse(lT, lS):
        T, S = math.exp(lT), math.exp(lS)
        e = 0.0
        for r, t, s in obs:
            m = Q / (4 * math.pi * T) * A.well_function(r * r * S / (4 * T * t))
            e += float(np.sum((m - s) ** 2))
        return e
    best = None
    for lT in np.linspace(math.log(3000), math.log(30000), 40):
        for lS in np.linspace(math.log(1e-5), math.log(1e-2), 40):
            e = sse(lT, lS)
            if best is None or e < best[0]:
                best = (e, lT, lS)
    _, lT, lS = best
    step = 0.06
    for _ in range(60):
        moved = False
        for dT, dS in ((step, 0), (-step, 0), (0, step), (0, -step)):
            e = sse(lT + dT, lS + dS)
            if e < best[0]:
                best, lT, lS, moved = (e, lT + dT, lS + dS), lT + dT, lS + dS, True
        if not moved:
            step /= 2
            if step < 1e-4:
                break
    n = sum(len(t) for _, t, _ in obs)
    return math.exp(lT), math.exp(lS), math.sqrt(best[0] / n)


def test_leakage(test, q_avg, frame, T, S, width, reg, wells=("OW-1", "OW-2", "OW-3")):
    """The leakage factor fitted to the test alone (walls at the plate, T and S held): the chain's third link
    skipped, the far field read from three days."""
    obs = []
    for w in wells:
        t, s = test[w]["t"], test[w]["s"]
        m = (t >= 2 / 1440.0) & (t <= 3.0)
        idx = np.unique(np.searchsorted(t[m], np.logspace(np.log10(2 / 1440.0), np.log10(3.0), 120)).clip(0, m.sum() - 1))
        obs.append((frame[w], t[m][idx], s[m][idx]))
    Q = q_avg * GPM
    best = None
    for B in np.geomspace(1000, 200000, 40):
        e = 0.0
        for o, t, s in obs:
            e += float(np.sum((Q * A.step_response(T, S, B, frame["PW-1"], o, t, width) - s) ** 2))
        if best is None or e < best[0]:
            best = (e, B)
    return round(best[1], 0)


# ---------------------------------------------------------------- the far field

def nearest_domestic(reg):
    """The registered domestic well nearest PW-1 and PW-2 (Rule WR-4 4.4)."""
    px = (reg["PW-1"]["Easting (ft)"] + reg["PW-2"]["Easting (ft)"]) / 2
    py = (reg["PW-1"]["Northing (ft)"] + reg["PW-2"]["Northing (ft)"]) / 2
    dom = [w for w, r in reg.items() if str(r["Purpose"]).startswith("domestic")]
    return min(dom, key=lambda w: math.hypot(reg[w]["Easting (ft)"] - px, reg[w]["Northing (ft)"] - py))


CLEAN = ("CV-02", "CV-11")
_FITS = {}
BASE = {"MS-MW": ((2008, 6), (2009, 2)), "default": ((2005, 1), (2008, 12))}


def _win(w):
    a, b = BASE.get(w, BASE["default"])
    return np.array([a <= ym <= b for ym in MONTHS])


def attributable(lv, w, control):
    """Drawdown the Mill Street wells caused at w: its natural level (its own pre-pumping mean moved by the
    control's change from the same months) less the reading. control None: the reading against its own
    pre-pumping mean."""
    win = _win(w)
    base = np.nanmean(lv[w][win])
    if control is None:
        return base - lv[w]
    cs = np.vstack([lv[c] - np.nanmean(lv[c][win]) for c in control])
    cnt = np.sum(~np.isnan(cs), axis=0)
    nat = np.where(cnt > 0, np.nansum(cs, axis=0) / np.maximum(cnt, 1), np.nan)
    return base + nat - lv[w]


FIT = np.array([(2009, 3) <= ym <= (2026, 9) for ym in MONTHS])


@lru_cache(maxsize=None)
def _kern(T, S, B, well, obs, width):
    return A.monthly_kernel(T, S, B, well, obs, width, N)


def model_town(q1, q2, frame, w, T, S, B, width):
    return (A.superpose_monthly(q1, _kern(T, S, B, frame["TW-1"], frame[w], width)) +
            A.superpose_monthly(q2, _kern(T, S, B, frame["TW-2"], frame[w], width)))


def calibrate(q, frame, att, T, S, width, wells=("MS-MW", "CV-07", "OW-S"), trend=False, profile=False):
    """The leakage factor (ft) minimising the squared misfit to the attributable drawdown, March 2009 to September
    2026; trend adds a free intercept and slope per well (the easy route's regional trend)."""
    q1, q2 = q["TW-1"], q["TW-2"]

    def sse(lB):
        B = math.exp(lB)
        e = 0.0
        for w in wells:
            m = model_town(q1, q2, frame, w, T, S, B, width)
            ok = FIT & ~np.isnan(att[w])
            r = att[w][ok] - m[ok]
            if trend:
                X = np.column_stack([np.ones(ok.sum()), np.arange(N)[ok] / 120.0])
                r = r - X @ np.linalg.lstsq(X, r, rcond=None)[0]
            e += float(np.sum(r * r))
        return e
    grid = np.linspace(math.log(600), math.log(60000), 30)
    vals = [sse(g) for g in grid]
    if profile:
        return [(round(math.exp(g)), v) for g, v in zip(grid, vals)]
    k = int(np.argmin(vals))
    lo, hi = grid[max(k - 1, 0)], grid[min(k + 1, len(grid) - 1)]
    for _ in range(24):
        m1, m2 = lo + (hi - lo) / 3, hi - (hi - lo) / 3
        if sse(m1) < sse(m2):
            hi = m2
        else:
            lo = m1
    return round(math.exp((lo + hi) / 2), 0)


def profile(q, frame, att, T, S, width, wells, B0):
    """The misfit over leakage factors from half to twice B0, 61 points."""
    q1, q2 = q["TW-1"], q["TW-2"]
    out = []
    for B in np.geomspace(B0 / 2, B0 * 2, 61):
        B = round(float(B), 0)
        e = 0.0
        for w in wells:
            m = model_town(q1, q2, frame, w, T, S, B, width)
            ok = FIT & ~np.isnan(att[w])
            e += float(np.sum((att[w][ok] - m[ok]) ** 2))
        out.append((B, e))
    return out


def forecast(q, frame, T, S, B, width, rate, seasonal=True, at="OW-S"):
    """Monthly drawdown at OW-S, 2005 to 2046: the Mill Street wells (record, then the projection) and the Reidel
    Road field at the rate."""
    proj = town_projection()
    fut = np.array([ym >= (2026, 10) for ym in MONTHS])
    if not seasonal:
        proj = np.array([TOWN_2026 * (1 + TOWN_GROWTH) ** (y - 2026) if (y, m) >= (2026, 10) else 0.0
                         for y, m in MONTHS])
    q1 = np.where(fut, proj * 0.56, q["TW-1"])
    q2 = np.where(fut, proj * 0.44, q["TW-2"])
    town = model_town(q1, q2, frame, at, T, S, B, width)
    new = np.array([rate * (NEW_SEASON[m - 1] if seasonal else 1.0) if (y, m) >= (2027, 4) else 0.0
                    for y, m in MONTHS])
    field = (A.superpose_monthly(new / 2, _kern(T, S, B, frame["PW-1"], frame[at], width)) +
             A.superpose_monthly(new / 2, _kern(T, S, B, frame["PW-2"], frame[at], width)))
    return town, field


def run(target, control=CLEAN, width="plate", T=None, S=None, trend=False, leaky=True, keep_running=False,
        baro_correct=True, fit_wells=("MS-MW", "CV-07", "OW-S"), fit_test=("OW-1", "OW-2", "OW-3"),
        clock_naive=False, ignore_rehang=False, seasonal=True, test_leaky=False):
    reg, mph = register(target)
    frame = valley_frame(reg)
    wd = PLATE["width"] if width == "plate" else width
    test, q_avg = test_drawdowns(target, baro_correct, clock_naive, ignore_rehang)
    dist = {w: math.hypot(reg[w]["Easting (ft)"] - reg["PW-1"]["Easting (ft)"],
                          reg[w]["Northing (ft)"] - reg["PW-1"]["Northing (ft)"]) for w in ("OW-1", "OW-2", "OW-3", "PW-2", "OW-S")}
    fk = (os.path.abspath(target), baro_correct, tuple(fit_test), clock_naive, ignore_rehang)
    if fk not in _FITS:
        _FITS[fk] = theis_fit(test, q_avg, wells=fit_test, coords=dist)
    Tf, Sf, rms = _FITS[fk]
    T = Tf if T is None else T
    S = Sf if S is None else S
    q = town_pumping(target)
    lv = levels(target, reg, mph, keep_running)
    att = {w: attributable(lv, w, control) for w in ("MS-MW", "OW-S", "CV-07")}
    if test_leaky:
        B = test_leakage(test, q_avg, frame, T, S, wd, reg)
    elif leaky:
        B = calibrate(q, frame, att, T, S, wd, fit_wells, trend)
    else:
        B, wd = None, None
    res = {"T": T, "S": S, "T_fit": Tf, "S_fit": Sf, "rms": rms, "q_avg": q_avg, "B": B, "width": wd,
           "be": {w: test[w]["be"] for w in test}, "dist": dist, "att": att, "lv": lv, "q": q, "frame": frame}
    peaks, series = {}, {}
    for r in OPTIONS:
        town, field = forecast(q, frame, T, S, B, wd, r, seasonal)
        tot = town + field
        series[r] = (town, field)
        peaks[r] = float(tot[YR == 2046].max())
        res.setdefault("peak_term", {})[r] = float(tot[(YR >= 2027) & (YR <= 2046)].max())
        res.setdefault("peak_year", {})[r] = int(YR[(YR >= 2027) & (YR <= 2046)][np.argmax(tot[(YR >= 2027) & (YR <= 2046)])])
    res["peaks"] = peaks
    res["resid"] = {}
    for w in ("MS-MW", "CV-07", "OW-S"):
        mdl = model_town(q["TW-1"], q["TW-2"], frame, w, T, S, B, wd)
        ok = FIT & ~np.isnan(att[w])
        res["resid"][w] = float(np.sqrt(np.mean((att[w][ok] - mdl[ok]) ** 2)))
    res["series"] = series
    ok = [r for r in OPTIONS if peaks[r] <= LIMIT]
    res["call"] = max(ok) if ok else None
    m25 = YR == 2025
    res["msmw_2025"] = float(np.nanmean(att["MS-MW"][m25]))
    res["msmw_2025_model"] = float(model_town(q["TW-1"], q["TW-2"], frame, "MS-MW", T, S, B, wd)[m25].mean())
    if res["call"]:
        tw, fd = forecast(q, frame, T, S, B, wd, res["call"], seasonal, at=nearest_domestic(reg))
        res["dw"] = float((tw + fd)[YR == 2046].max())
        res["dw_id"] = nearest_domestic(reg)
    else:
        res["dw"], res["dw_id"] = None, nearest_domestic(reg)
    town_sel = series[OPTIONS[0]][0]
    res["town_dec2046"] = float(town_sel[MI[(2046, 12)]])
    return res
