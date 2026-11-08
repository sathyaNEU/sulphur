"""task3: the data files under target/, written from the simulated world as each publishing system writes them.

Gauge daily values and peaks (a USGS-style export), two cooperative observer stations (a GHCN-Daily style CSV), two
SNOTEL sites (the NRCS report generator's CSV), four regional gauges' annual peaks, and the basins' characteristics
workbook. The documents (the county standard, the state's regional equations, the consultant's span ratings) are
written by docs.py.
"""
import datetime as dt
import os

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font

import world as W

PULL = dt.datetime(2026, 10, 14, 9, 41)
# each download carries its own retrieval clock
RETRIEVED = {"daily": dt.datetime(2026, 10, 14, 9, 41), "12183450": dt.datetime(2026, 10, 14, 9, 43),
             "pot": dt.datetime(2026, 10, 14, 10, 6), "12187200": dt.datetime(2026, 10, 14, 9, 44),
             "12181650": dt.datetime(2026, 10, 14, 9, 46), "12189500": dt.datetime(2026, 10, 14, 9, 47),
             "12184900": dt.datetime(2026, 10, 14, 9, 49)}
RIVER = dict(site="12183450", name="COYNER RIVER NEAR TESSEL, WA", lat="48 21 07", lon="121 46 52", datum=1603.4)
REGIONAL = [  # world index, site, name, first water year
    (2, "12187200", "TARROW RIVER NEAR BRANDT, WA", 1956),
    (3, "12181650", "GORHAM CREEK NEAR VESPER, WA", 1963),
    (4, "12189500", "QUILLEN RIVER AT ASHBY FALLS, WA", 1951),
    (5, "12184900", "PINNELL CREEK NEAR COE, WA", 1968),
]
BASE = 2500                     # the river's partial-duration base discharge, cfs
ESTIMATED = (1991, 2004)        # water years whose annual peak the gauge estimated (recorder washed out)
COOP = [
    dict(id="USC00458114", name="TESSEL 2 NE, WA US", lat=48.3586, lon=-121.7342, z=1180.0, obs=17,
         start=dt.date(1950, 10, 1), end=dt.date(1988, 6, 30), off=0.05),
    dict(id="USC00458117", name="TESSEL 3 E, WA US", lat=48.3511, lon=-121.7019, z=1215.0, obs=17,
         start=dt.date(1988, 4, 1), end=dt.date(2025, 9, 30), off=0.0),
]
RIDGE = dict(id="USC00452231", name="DURROW RIDGE, WA US", lat=48.2847, lon=-121.8806, z=2710.0, obs=17,
             start=dt.date(1950, 10, 1), end=dt.date(2025, 9, 30), off=0.0)
LCD = dict(station="72784624151", name="TESSEL FIELD AIRPORT, WA US", lat=48.3489, lon=-121.7208, z=1160.0,
           file="lcd_tessel_field_hourly_1950-2025.csv")
SNOTEL = [
    dict(sid=1187, name="Hatchet Meadow", z=4160.0, lat=48.4402, lon=-121.5318, start=dt.date(1981, 10, 1),
         tstart=dt.date(1987, 10, 1), dstart=dt.date(2001, 10, 1), swe_f=1.08, off=0.0, file="snotel_1187_hatchet_meadow_daily.csv"),
    dict(sid=1203, name="Corbel Ridge", z=5630.0, lat=48.4756, lon=-121.4469, start=dt.date(1983, 10, 1),
         tstart=dt.date(1989, 10, 1), dstart=dt.date(2003, 10, 1), swe_f=0.94, off=0.0, file="snotel_1203_corbel_ridge_daily.csv"),
]


def hour_of(d):
    return int((d - W.T0).total_seconds() // 3600)


def usgs_round(q):
    """USGS daily and peak values: three significant figures (two below ten)."""
    if q <= 0:
        return 0.0
    if q < 10:
        return round(q, 1)
    p = int(np.floor(np.log10(q))) - 2
    return float(round(q / 10 ** p) * 10 ** p)


def fmt_q(q):
    v = usgs_round(q)
    return ("%.1f" % v) if v < 10 else ("%d" % int(v))


def stage(q, datum_shift):
    """Gage height from a rating (feet), the 1985 datum lowered the gage 2.00 ft."""
    return 2.1 + 0.118 * q ** 0.47 + datum_shift


# --------------------------------------------------------------------------------------------- gauge files

def daily_means(W_, k):
    q = W_.flows[k]
    n = len(q) // 24
    return q[:n * 24].reshape(n, 24).mean(axis=1)


def write_daily(W_, rng, path):
    dm = daily_means(W_, 0)
    days = [W.T0.date() + dt.timedelta(days=i) for i in range(len(dm))]
    lines = ["# U.S. Geological Survey, National Water Information System",
             "# Daily statistic: mean; parameter 00060, discharge, cubic feet per second",
             "# Site %s %s" % (RIVER["site"], RIVER["name"]),
             "# Qualification codes: A approved for publication, P provisional, e value estimated,",
             "#   Eqp equipment malfunction (no value), Ice ice affected (no value)",
             "# Retrieved %s" % RETRIEVED["daily"].strftime("%Y-%m-%d %H:%M PDT"),
             "agency_cd,site_no,datetime,discharge_cfs,qualifiers"]
    gaps = [(dt.date(1977, 8, 9), dt.date(1977, 9, 6))]                # recorder failure, no record
    ann = W.annual_peaks(W_, 0)
    pk = {y: (W.T0 + dt.timedelta(hours=int(ann[y][1]))).date() for y in ESTIMATED}
    est = [(pk[y] - dt.timedelta(days=n - 14), pk[y] + dt.timedelta(days=13)) for y, n in zip(ESTIMATED, (56, 71))]  # washouts
    assert all(a <= pk[y] <= b for (a, b), y in zip(est, ESTIMATED))
    assert sum((b - a).days + 1 for a, b in est) == 127
    ice = [d for d in days if d.month in (12, 1, 2) and rng.random() < 0.004]
    ice = set(ice)
    for d, v in zip(days, dm):
        if d < dt.date(1950, 10, 1) or d > dt.date(2025, 9, 30):
            continue
        if any(a <= d <= b for a, b in gaps):
            continue
        q = "A"
        val = fmt_q(v)
        if any(a <= d <= b for a, b in est):
            q = "A:e"
            val = fmt_q(v * float(np.exp(rng.normal(0, 0.06))))
        if d in ice:
            q, val = "A:Ice", ""
        lines.append("USGS,%s,%s,%s,%s" % (RIVER["site"], d.isoformat(), val, q))
    open(path, "w", newline="\n").write("\n".join(lines) + "\n")
    return len(lines) - 7


def storm_peaks_hourly(q, base, min_sep=72):
    """Independent peaks above base from an hourly series: local maxima, merged when closer than min_sep hours
    or when the trough between them stays above two thirds of the smaller peak."""
    idx = np.nonzero((q[1:-1] > q[:-2]) & (q[1:-1] >= q[2:]) & (q[1:-1] >= base))[0] + 1
    peaks = []
    for i in idx:
        if peaks and (i - peaks[-1] < min_sep or q[peaks[-1]:i + 1].min() > 0.667 * min(q[i], q[peaks[-1]])):
            if q[i] > q[peaks[-1]]:
                peaks[-1] = i
            continue
        peaks.append(i)
    return peaks


def peak_tables(W_, k):
    """Annual peaks (water years 1951 to 2025) and peaks above the base for basin k: lists of (hour, q)."""
    q = W_.flows[k]
    ann = W.annual_peaks(W_, k)
    annual = [(ann[y][1], ann[y][0]) for y in range(1951, 2026)]
    pot = [(i, float(q[i])) for i in storm_peaks_hourly(q, BASE) if 1951 <= W.water_year(i) <= 2025]
    have = {W.water_year(i): (i, v) for i, v in annual}
    # every annual peak of BASE or more appears among the peaks above base at its own hour
    for y, (i, v) in have.items():
        if v >= BASE and not any(abs(j - i) <= 6 for j, _ in pot):
            pot.append((i, v))
    pot.sort()
    return annual, pot


def write_peaks(W_, rng, path, k, site, name, first_wy=1951):
    annual, _ = peak_tables(W_, k)
    lines = ["# U.S. Geological Survey, National Water Information System, peak streamflow",
             "# Site %s %s" % (site, name),
             "# peak_cd: 2 discharge is an estimate; 5 discharge affected to an unknown degree by regulation or",
             "#   diversion; 7 discharge is an historic peak; A year of occurrence is unknown or not exact",
             "# gage_ht in feet above the gage datum in use on the date of the peak"]
    lines += ["# Retrieved %s" % RETRIEVED[site].strftime("%Y-%m-%d %H:%M PDT"),
              "agency_cd\tsite_no\tpeak_dt\tpeak_tm\tpeak_va\tpeak_cd\tgage_ht",
              "5s\t15s\t10d\t6s\t8s\t27s\t8s"]
    for i, v in annual:
        d = W.T0 + dt.timedelta(hours=int(i))
        wy = W.water_year(i)
        if wy < first_wy:
            continue
        tm = "" if (k == 0 and wy < 1963) else d.strftime("%H:%M")
        cd = ""
        if k == 0 and wy in ESTIMATED:
            cd = "2"
        shift = 0.0 if (k != 0 or d.date() >= dt.date(1985, 10, 1)) else 2.00
        gh = "%.2f" % stage(v, shift) if (k == 0 or rng.random() > 0.05) else ""
        lines.append("USGS\t%s\t%s\t%s\t%s\t%s\t%s" % (site, d.date().isoformat(), tm, fmt_q(v), cd, gh))
    open(path, "w", newline="\n").write("\n".join(lines) + "\n")


def write_pot(W_, path):
    _, pot = peak_tables(W_, 0)
    lines = ["# U.S. Geological Survey, Washington Water Science Center",
             "# Partial-duration series: peaks above base, %s %s" % (RIVER["site"], RIVER["name"]),
             "# Base discharge %d ft3/s. Peaks are independent instantaneous peaks above the base, from the recorder" % BASE,
             "#   charts (1950 to 1990) and the 15-minute record (1990 on), as published in the annual data reports.",
             "# Times are Pacific Standard Time. Gage heights are above the datum in use on the date of the peak",
             "#   (lowered 2.00 ft on 1 October 1985).",
             "# Retrieved %s" % RETRIEVED["pot"].strftime("%Y-%m-%d %H:%M PDT"),
             "water_year\tpeak_dt\tpeak_tm\tpeak_va\tgage_ht"]
    for i, v in pot:
        d = W.T0 + dt.timedelta(hours=int(i))
        shift = 0.0 if d.date() >= dt.date(1985, 10, 1) else 2.00
        lines.append("%d\t%s\t%s\t%s\t%.2f" % (W.water_year(i), d.date().isoformat(), d.strftime("%H:%M"), fmt_q(v),
                                                 stage(v, shift)))
    open(path, "w", newline="\n").write("\n".join(lines) + "\n")
    return len(pot)


# ------------------------------------------------------------------------------------------ station files

def station_hourly(W_, rng, z, off, snow_catch, rain_catch=0.98, noise_sd=0.5):
    """Hourly precipitation (inches) and temperature (deg C) at a station elevation."""
    w = W_.weather
    p = w["p"] * (1.0 + w["gain"] * (min(z, 5500.0) - 1000.0) / 1000.0 + 0.15 * w["gain"] * max(z - 5500.0, 0.0) / 1000.0)
    t = w["tv"] - w["lapse"] * (z - W.Z_VALLEY) / W.FT_PER_KM + off
    e = np.zeros(len(t))
    shocks = rng.normal(0, noise_sd * np.sqrt(1 - 0.9 ** 2), len(t))
    for i in range(1, len(t)):
        e[i] = 0.9 * e[i - 1] + shocks[i]
    t = t + e
    fr = np.clip((t - W.T_RS + W.T_HALF) / (2 * W.T_HALF), 0, 1)
    catch = rain_catch * fr + snow_catch * (1 - fr)
    return p * catch, t, fr


def obs_days(n_hours, obs_hour):
    """Observation-day index of each hour: the day ending at obs_hour local (the label is the ending date)."""
    hours = np.arange(n_hours)
    return (hours + (24 - obs_hour)) // 24


def c2f(t):
    return t * 9.0 / 5.0 + 32.0


def coop_rows(W_, rng, st, accum_weekends):
    ph, th, fr = station_hourly(W_, rng, st["z"], st["off"], snow_catch=0.92)
    od = obs_days(len(ph), st["obs"])
    nd = od.max() + 1
    pday = np.bincount(od, weights=ph, minlength=nd)
    snow = np.bincount(od, weights=ph * (1 - fr) * 11.0, minlength=nd)
    tmax = np.full(nd, -99.0)
    tmin = np.full(nd, 99.0)
    np.maximum.at(tmax, od, th)
    np.minimum.at(tmin, od, th)
    rows = []
    depth = 0.0
    pending = 0.0
    pend_days = 0
    for i in range(1, nd):
        d = W.T0.date() + dt.timedelta(days=int(i))
        if d < st["start"] or d > st["end"]:
            continue
        pv = pday[i] * float(np.exp(rng.normal(0, 0.07))) if pday[i] > 0.004 else pday[i]
        depth = max(0.0, depth * 0.88 + snow[i] - 0.9 * max(tmax[i], 0.0))
        r = dict(date=d, prcp=pv, snow=snow[i], snwd=depth, tmax=c2f(tmax[i]), tmin=c2f(tmin[i]), mdpr=None, dapr=None,
                 tobs=c2f(th[min(int(i) * 24 + st["obs"], len(th) - 1)]))
        # observer away at weekends in the early decades: Saturday and Sunday blank, Monday the three-day total
        if accum_weekends and d.year < 1979 and d.weekday() in (5, 6) and rng.random() < 0.55:
            pending += pv
            pend_days += 1
            r["prcp"] = None
            r["snow"] = None
            r["tmax"] = None
            r["tmin"] = None
            rows.append(r)
            continue
        if pend_days:
            r["mdpr"] = pending + pv
            r["dapr"] = pend_days + 1
            r["prcp"] = None
            pending, pend_days = 0.0, 0
        if rng.random() < 0.008:
            r["tmax"] = None
        if rng.random() < 0.008:
            r["tmin"] = None
        rows.append(r)
    return rows


def write_coop(W_, rng, path):
    cols = ["STATION", "NAME", "LATITUDE", "LONGITUDE", "ELEVATION", "DATE", "DAPR", "DAPR_ATTRIBUTES", "MDPR",
            "MDPR_ATTRIBUTES", "PRCP", "PRCP_ATTRIBUTES", "SNOW", "SNOW_ATTRIBUTES", "SNWD", "SNWD_ATTRIBUTES", "TMAX",
            "TMAX_ATTRIBUTES", "TMIN", "TMIN_ATTRIBUTES", "TOBS", "TOBS_ATTRIBUTES"]
    out = [",".join('"%s"' % c for c in cols)]
    n = 0
    for st in COOP:
        for r in coop_rows(W_, rng, st, accum_weekends=True):
            out.append(_ghcn_line(st, r))
            n += 1
    open(path, "w", newline="\n").write("\n".join(out) + "\n")
    return n


def _ghcn_line(st, r):
    def num(v, nd):
        return "" if v is None else ("%.*f" % (nd, v))

    def attr(v, obs, trace=False):
        if v is None:
            return ""
        return ",%s,7,%04d" % ("T" if trace else "", obs * 100)
    obs = st["obs"]
    p = r["prcp"]
    trace = p is not None and 0 < p < 0.005
    pv = None if p is None else (0.0 if trace else round(p, 2))
    sn = None if r["snow"] is None else round(r["snow"], 1)
    sd = None if r["snwd"] is None else float(int(round(r["snwd"])))
    tx = None if r["tmax"] is None else float(int(round(r["tmax"])))
    tn = None if r["tmin"] is None else float(int(round(r["tmin"])))
    to = None if r["tobs"] is None else float(int(round(r["tobs"])))
    vals = [st["id"], st["name"], "%.4f" % st["lat"], "%.4f" % st["lon"], "%.1f" % (st["z"] * 0.3048),
            r["date"].isoformat(),
            "" if r["dapr"] is None else "%d" % r["dapr"], attr(r["dapr"], obs),
            num(r["mdpr"], 2), attr(r["mdpr"], obs),
            num(pv, 2), attr(pv, obs, trace),
            num(sn, 1), attr(sn, obs), num(sd, 0) if sd is not None else "", attr(sd, obs),
            num(tx, 0), attr(tx, obs), num(tn, 0), attr(tn, obs), num(to, 0), attr(to, obs)]
    return ",".join('"%s"' % v for v in vals)


def write_ridge(W_, rng, path):
    cols = ["STATION", "NAME", "LATITUDE", "LONGITUDE", "ELEVATION", "DATE", "PRCP", "PRCP_ATTRIBUTES", "SNOW",
            "SNOW_ATTRIBUTES", "SNWD", "SNWD_ATTRIBUTES", "TMAX", "TMAX_ATTRIBUTES", "TMIN", "TMIN_ATTRIBUTES", "TOBS",
            "TOBS_ATTRIBUTES"]
    rows = coop_rows(W_, rng, RIDGE, accum_weekends=False)
    out = [",".join('"%s"' % c for c in cols)]
    missing_winters = {1969, 1984, 2003}
    n = 0
    for r in rows:
        d = r["date"]
        wy = d.year + (1 if d.month >= 10 else 0)
        if wy in missing_winters and d.month in (12, 1, 2):
            continue
        line = _ghcn_line(RIDGE, r).split('","')
        # drop the DAPR and MDPR columns this station never reported
        keep = line[:6] + line[10:]
        out.append('","'.join(keep))
        n += 1
    open(path, "w", newline="\n").write("\n".join(out) + "\n")
    return n


def write_lcd(W_, path):
    """The airport's Local Climatological Data export: a routine report (FM-15) every hour (at 56 minutes past before the
    automated station, 53 after), specials
    (FM-16) in changing weather carrying the rain since the last routine report, whole degrees F, inches of rain."""
    rng = np.random.default_rng(W_.seed + 2000)
    ph, th, fr = station_hourly(W_, rng, LCD["z"], 0.0, snow_catch=0.88, rain_catch=0.98, noise_sd=0.3)
    n = len(ph)
    w = W_.weather
    ar_hour = np.zeros(n, bool)
    for s in w["storms"]:
        if s["ar"]:
            ar_hour[s["start"]:s["start"] + s["dur"]] = True
    wet = ph >= 0.005
    wind = np.where(wet, rng.gamma(4.0, 2.6, n) + np.where(ar_hour, 6.0, 0.0), rng.gamma(1.6, 2.4, n))
    rh = np.where(wet, rng.uniform(90, 100, n), np.clip(rng.normal(78, 12, n), 28, 100))
    i0 = hour_of(dt.datetime(1950, 10, 1))
    i1 = hour_of(dt.datetime(2025, 10, 1))
    miss = rng.random(n)
    sus = rng.random(n)
    spec = rng.random(n)
    minute = rng.integers(5, 50, n)
    cols = ["STATION", "DATE", "LATITUDE", "LONGITUDE", "ELEVATION", "NAME", "REPORT_TYPE", "SOURCE",
            "HourlyDryBulbTemperature", "HourlyPrecipitation", "HourlyPresentWeatherType", "HourlyRelativeHumidity",
            "HourlyWindSpeed"]
    head = '"%s","%%s","%.5f","%.5f","%.1f","%s"' % (LCD["station"], LCD["lat"], LCD["lon"], LCD["z"] * 0.3048, LCD["name"])
    out = [",".join('"%s"' % c for c in cols)]

    def pcp(v):
        if v < 0.0005:
            return "0.00"
        if v < 0.005:
            return "T"
        return "%.2f" % v

    def wx(v, f, humid):
        if v < 0.0005:
            return "BR:1 ||" if humid and v == 0 and rng.random() < 0.15 else ""
        base = "RA" if f >= 0.75 else ("SN" if f <= 0.25 else "RASN")
        if base == "RA" and v < 0.02 and rng.random() < 0.4:
            base = "DZ"
        sign = "-" if v < 0.10 else ("+" if v >= 0.30 else "")
        mist = " BR:1" if humid else ""
        return "%s%s:02%s |%s |%s" % (sign, base, mist, base, base)

    n_rows = 0
    for i in range(i0, i1):
        d = W.T0 + dt.timedelta(hours=int(i))
        early = d.year < 1965
        if miss[i] < (0.022 if early else 0.004):
            continue
        tf = "%d" % int(round(c2f(th[i])))
        if sus[i] < 0.0015:
            tf += "s"
        v = float(ph[i])
        humid = rh[i] > 96
        src = "4" if d.year < 1996 else "7"
        if wet[i] and spec[i] < 0.09:
            part = v * minute[i] / 53.0
            out.append(",".join([head % d.replace(minute=int(minute[i])).strftime("%Y-%m-%dT%H:%M:%S"), '"FM-16"', '"%s"' % src, '"%s"' % tf,
                                 '"%s"' % pcp(part), '"%s"' % wx(part, fr[i], humid), '"%d"' % int(rh[i]), '"%d"' % int(wind[i])]))
            n_rows += 1
        out.append(",".join([head % d.replace(minute=56 if src == "4" else 53).strftime("%Y-%m-%dT%H:%M:%S"), '"FM-15"', '"%s"' % src, '"%s"' % tf,
                             '"%s"' % pcp(v), '"%s"' % wx(v, fr[i], humid), '"%d"' % int(rh[i]), '"%d"' % int(wind[i])]))
        n_rows += 1
    open(path, "w", newline="\n").write("\n".join(out) + "\n")
    return n_rows


def write_snotel(W_, rng, st, path):
    ph, th, fr = station_hourly(W_, rng, st["z"], st["off"], snow_catch=0.84, rain_catch=0.97)
    nd = len(ph) // 24
    pday = ph[:nd * 24].reshape(nd, 24).sum(axis=1)
    tday = th[:nd * 24].reshape(nd, 24)
    # SWE at the site from the band snowpack, interpolated in elevation, scaled by the site's exposure
    zb = W.Z
    j = np.searchsorted(zb, st["z"]) - 1
    wgt = (st["z"] - zb[j]) / (zb[j + 1] - zb[j])
    swe_mm = (1 - wgt) * W_.swe_day[:, j] + wgt * W_.swe_day[:, j + 1]
    lines = ["#------------------------------------------------- WARNING --------------------------------------------",
             "# The data you have obtained from this automated U.S. Department of Agriculture Natural Resources",
             "# Conservation Service database are subject to revision regardless of indicated Quality Assurance level.",
             "#-------------------------------------------------------------------------------------------------------",
             "# Reporting Frequency: Daily; Date Range: %s to 2025-09-30" % st["start"].isoformat(),
             "# Data for the following site(s) are contained in this file:",
             "#   SNOTEL %d: %s, WA  Elevation: %d ft  Lat: %.2f  Lon: %.2f" % (st["sid"], st["name"], st["z"], st["lat"], st["lon"]),
             "# Precipitation Accumulation is the water year total since 1 October; Snow Water Equivalent and",
             "#   Precipitation Accumulation are start-of-day values; air temperatures are for the calendar day.",
             "#",
             "Date,Snow Water Equivalent (in) Start of Day Values,Precipitation Accumulation (in) Start of Day Values,"
             "Air Temperature Maximum (degF),Air Temperature Minimum (degF),Air Temperature Average (degF),"
             "Snow Depth (in) Start of Day Values"]
    acc = 0.0
    swe_noise = 0.0
    n = 0
    for i in range(1, nd):
        d = W.T0.date() + dt.timedelta(days=i)
        if d < st["start"] or d > dt.date(2025, 9, 30):
            if d.month == 10 and d.day == 1:
                acc = 0.0
            continue
        if d.month == 10 and d.day == 1:
            acc = 0.0
        acc_sod = acc
        acc += pday[i]                       # today's catch shows in tomorrow's start-of-day value
        swe_noise = 0.85 * swe_noise + rng.normal(0, 0.06)
        swe_in = max(0.0, swe_mm[i - 1] / 25.4 * st["swe_f"] + (swe_noise if swe_mm[i - 1] > 5 else 0.0))
        t = tday[i]
        tx = c2f(t.max())
        tn = c2f(t.min())
        ta = c2f(t.mean())
        dep = swe_in * 3.4 if d >= st["dstart"] else None
        temps = d >= st["tstart"]
        prec_s = "%.1f" % acc_sod
        swe_s = "%.1f" % swe_in
        if rng.random() < 0.004:              # a pillow or gauge outage day
            swe_s = ""
        if rng.random() < 0.003:
            prec_s = ""
        row = [d.isoformat(), swe_s, prec_s,
               ("%.1f" % tx) if temps else "", ("%.1f" % tn) if temps else "", ("%.1f" % ta) if temps else "",
               ("%d" % round(dep)) if dep is not None else ""]
        lines.append(",".join(row))
        n += 1
    open(path, "w", newline="\n").write("\n".join(lines) + "\n")
    return n


# --------------------------------------------------------------------------------------------- the workbook

def basin_map(W_, b):
    """Mean annual precipitation over a basin (inches) from the world's climate: each band's mean water-year total."""
    w = W_.weather
    tot = np.zeros(W.NB)
    for z_i, z in enumerate(W.Z):
        tot[z_i] = float((w["p"] * (1.0 + w["gain"] * (min(z, 5500.0) - 1000.0) / 1000.0
                                    + 0.15 * w["gain"] * max(z - 5500.0, 0.0) / 1000.0)).sum())
    years = (W.NH / 24.0) / 365.25
    return float((b["bands"] / b["area"] * tot).sum() / years * b.get("pmult", 1.0))


def write_workbook(W_, path, maps):
    wb = Workbook()
    ws = wb.active
    ws.title = "Gauged basins"
    ws["A1"] = "Basin characteristics of stream gauges, Region 3 (state flood study 2019, appendix B)"
    ws["A1"].font = Font(bold=True)
    hdr = ["Station", "Name", "Drainage area (sq mi)", "Mean basin elevation (ft)", "Minimum elevation (ft)",
           "Maximum elevation (ft)", "Mean annual precipitation 1981-2010 (in)", "Forest cover (%)", "Record (water years)",
           "Distance from the Ransom Bar Rd crossing (mi)"]
    ws.append([])
    ws.append(hdr)
    for c in ws[3]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True)
    rows = [(0, RIVER["site"], RIVER["name"], 1951)] + REGIONAL
    forest = {0: 71, 2: 78, 3: 83, 4: 69, 5: 86}
    dist = {0: 6.2, 2: 27.4, 3: 18.9, 4: 41.3, 5: 33.6}
    for k, site, name, first in rows:
        b = W_.basins[k]
        mean_z = float((b["bands"] * W.Z).sum() / b["area"])
        ws.append([site, name.title().replace(", Wa", ", WA"), round(b["area"], 1), int(round(mean_z, -1)), b["zmin"],
                   b["zmax"], round(maps[k], 0), forest[k], "%d-2025" % first, dist[k]])
    for col, wdt in zip("ABCDEFGHIJ", (11, 38, 12, 12, 12, 12, 14, 10, 14, 14)):
        ws.column_dimensions[col].width = wdt
    # the county's delineation of the crossing
    ws2 = wb.create_sheet("Durrow Ck at Ransom Bar Rd")
    b = W_.basins[1]
    mean_z = float((b["bands"] * W.Z).sum() / b["area"])
    info = [("Pelton County Public Works, GIS: basin delineated from the county 10 m DEM, March 2026", None),
            (None, None),
            ("Outlet", "Durrow Creek at the Ransom Bar Road crossing (existing bridge 2209-04)"),
            ("Drainage area (sq mi)", round(b["area"], 1)),
            ("Minimum elevation (ft)", b["zmin"]),
            ("Maximum elevation (ft)", b["zmax"]),
            ("Mean basin elevation (ft)", int(round(mean_z, -1))),
            ("Main channel length (mi)", 17.4),
            ("Main channel slope (ft/mi)", 151.0),
            ("Forest cover (%)", 74),
            ("Developed land (%)", 3.1),
            ("Hydrologic soil group B (%)", 38),
            ("Hydrologic soil group C (%)", 51),
            ("Hydrologic soil group D (%)", 11)]
    for a, v in info:
        ws2.append([a, v])
    ws2["A1"].font = Font(bold=True)
    ws2.column_dimensions["A"].width = 34
    ws2.column_dimensions["B"].width = 58
    # elevation bands: the gauged basins from the state study, the crossing from the county's delineation
    ws3 = wb.create_sheet("Elevation bands")
    ws3["A1"] = "Area by elevation band (500 ft bands, lower edge inclusive)"
    ws3["A1"].font = Font(bold=True)
    ws3.append([])
    short = {"12183450": "Coyner R nr Tessel", "12187200": "Tarrow R nr Brandt", "12181650": "Gorham Ck nr Vesper",
             "12189500": "Quillen R at Ashby Falls", "12184900": "Pinnell Ck nr Coe"}
    cols = [(k, "%s (sq mi)" % short[site], 1.0) for k, site, _, _ in rows] + [(1, "Durrow Ck at Ransom Bar Rd (sq mi)", 1.0)]
    ws3.append(["Band (ft)"] + [h for _, h, _ in cols])
    for c in ws3[3]:
        c.font = Font(bold=True)
        c.alignment = Alignment(wrap_text=True)
    for lo in range(0, 10500, 500):
        m = (W.Z >= lo) & (W.Z < lo + 500)
        vals = []
        for k, _, scale in cols:
            a = float(W_.basins[k]["bands"][m].sum()) * scale
            if scale == 1.0:
                vals.append(round(a, 2) if a > 0.004 else 0)
            else:
                vals.append(int(round(a)) if a > 0.5 else 0)
        if not any(vals):
            continue
        ws3.append(["%d-%d" % (lo, lo + 500)] + vals)
    ws3.column_dimensions["A"].width = 12
    for col in "BCDEFG":
        ws3.column_dimensions[col].width = 15
    ws3.freeze_panes = "B4"
    # the climate stations the state study's precipitation map drew on
    ws4 = wb.create_sheet("Climate stations")
    ws4["A1"] = "Climate stations used for the Region 3 precipitation map (state flood study 2019, appendix C)"
    ws4["A1"].font = Font(bold=True)
    ws4.append([])
    ws4.append(["Station", "Name", "Network", "Latitude", "Longitude", "Elevation (ft)", "Record"])
    for c in ws4[3]:
        c.font = Font(bold=True)
    stations = [(COOP[0]["id"], "Tessel 2 NE", "COOP", COOP[0]["lat"], COOP[0]["lon"], COOP[0]["z"], "1950-1988"),
                (COOP[1]["id"], "Tessel 3 E", "COOP", COOP[1]["lat"], COOP[1]["lon"], COOP[1]["z"], "1988-"),
                (LCD["station"], "Tessel Field Airport", "WBAN", LCD["lat"], LCD["lon"], LCD["z"], "1948-"),
                (RIDGE["id"], "Durrow Ridge", "COOP", RIDGE["lat"], RIDGE["lon"], RIDGE["z"], "1950-"),
                ("USC00450874", "Brandt 4 W", "COOP", 48.5121, -121.9403, 610.0, "1931-"),
                ("USC00458862", "Vesper 1 S", "COOP", 48.2210, -121.5532, 1975.0, "1962-2011"),
                ("SNOTEL 1187", "Hatchet Meadow", "SNOTEL", SNOTEL[0]["lat"], SNOTEL[0]["lon"], SNOTEL[0]["z"], "1981-"),
                ("SNOTEL 1203", "Corbel Ridge", "SNOTEL", SNOTEL[1]["lat"], SNOTEL[1]["lon"], SNOTEL[1]["z"], "1983-"),
                ("SNOTEL 1241", "Ashby Pass", "SNOTEL", 48.6033, -121.3381, 6240.0, "1985-")]
    for row in stations:
        ws4.append(list(row))
    for col, wdt in zip("ABCDEFG", (14, 24, 10, 11, 12, 15, 12)):
        ws4.column_dimensions[col].width = wdt
    wb.save(path)


def write(W_, tgt):
    rng = np.random.default_rng(W_.seed + 1000)
    os.makedirs(tgt, exist_ok=True)
    info = {}
    info["daily_rows"] = write_daily(W_, rng, os.path.join(tgt, "usgs_12183450_coyner_r_daily_discharge.csv"))
    write_peaks(W_, rng, os.path.join(tgt, "usgs_12183450_coyner_r_annual_peaks.txt"), 0, RIVER["site"], RIVER["name"])
    info["pot_rows"] = write_pot(W_, os.path.join(tgt, "usgs_12183450_coyner_r_peaks_above_base.txt"))
    for k, site, name, first in REGIONAL:
        write_peaks(W_, rng, os.path.join(tgt, "usgs_%s_annual_peaks.txt" % site), k, site, name, first_wy=first)
    info["coop_rows"] = write_coop(W_, rng, os.path.join(tgt, "ghcnd_tessel_daily_1950-2025.csv"))
    info["ridge_rows"] = write_ridge(W_, rng, os.path.join(tgt, "ghcnd_durrow_ridge_daily_1950-2025.csv"))
    info["lcd_rows"] = write_lcd(W_, os.path.join(tgt, LCD["file"]))
    for st in SNOTEL:
        info[st["file"]] = write_snotel(W_, rng, st, os.path.join(tgt, st["file"]))
    maps = {k: basin_map(W_, W_.basins[k]) for k in (0, 1, 2, 3, 4, 5)}
    write_workbook(W_, os.path.join(tgt, "region3_basin_characteristics.xlsx"), maps)
    info["maps"] = maps
    return info
