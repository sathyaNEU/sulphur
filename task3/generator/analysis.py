"""task3: the golden analysis, read from the shipped files alone, and every rival route on the same files.

The creek's annual flood series is built storm by storm: each flood in the Coyner River's peak files is matched to
the storm that made it in the Tessel record; the storm's snow line is placed from the valley's storm temperature
with the storm lapse rate (the Tessel and Durrow Ridge pair on storm days) and the rain-snow temperature (the SNOTEL
sites' rain and snow days); rain over each basin is summed over the elevation bands below the snow line with the
orographic gradient the stations show; the river's flood is carried to the creek at the ratio of the two basins'
storm rain depths and the state equation's drainage-area exponent; the creek's flood each water year is the largest
of its storms'. Bulletin 17C then gives the frequency curve.
"""
import csv
import datetime as dt
import os
import re

import numpy as np
from openpyxl import load_workbook
from scipy import stats

import freq as F

FT_PER_KM = 3280.84
T0 = dt.datetime(1950, 10, 1)       # hour 0 of the hourly series (local standard time)
NH = int((dt.datetime(2025, 10, 1) - T0).total_seconds() // 3600)
LCD_FILE = "lcd_tessel_field_hourly_1950-2025.csv"
DESIGN_LIFE = 75
STATE_B = 0.78              # the state equations' drainage-area exponent for the 1 per cent flood (docs.py)
SPANS = None                # filled by docs.RATED at import time of the build


def _num(s):
    s = (s or "").strip()
    return float(s) if s not in ("", "-") else None


def read_rdb(path):
    rows = []
    hdr = None
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.rstrip("\n").split("\t")
            if hdr is None:
                hdr = parts
                continue
            if re.fullmatch(r"\d+s", parts[0] or "") or parts[0].endswith("s") and parts[0][:-1].isdigit():
                continue
            rows.append(dict(zip(hdr, parts)))
    return rows


def river_floods(tgt):
    """Every flood in the river's peak files: (date, discharge), annual peaks and peaks above base together, one row
    per flood (a peak listed in both files counted once)."""
    ann = read_rdb(os.path.join(tgt, "usgs_12183450_coyner_r_annual_peaks.txt"))
    pot = read_rdb(os.path.join(tgt, "usgs_12183450_coyner_r_peaks_above_base.txt"))
    out = {}
    annual = {}
    for r in ann:
        d = dt.date.fromisoformat(r["peak_dt"])
        q = float(r["peak_va"])
        out[d] = q
        wy = d.year + (1 if d.month >= 10 else 0)
        annual[wy] = (d, q)
    for r in pot:
        d = dt.date.fromisoformat(r["peak_dt"])
        out[d] = max(out.get(d, 0.0), float(r["peak_va"]))
    return sorted(out.items()), annual


def read_ghcn(path):
    rows = []
    with open(path) as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def valley_daily(tgt):
    """Tessel's daily precipitation (multi-day totals spread over their days) and mean temperature (deg C), the old
    station to its last day and the new one after, the new one's temperatures carried to the old site's elevation."""
    rows = read_ghcn(os.path.join(tgt, "ghcnd_tessel_daily_1950-2025.csv"))
    by = {}
    for r in rows:
        by.setdefault(r["STATION"], []).append(r)
    old, new = by["USC00458114"], by["USC00458117"]
    last_old = max(dt.date.fromisoformat(r["DATE"]) for r in old)
    seq = [r for r in old] + [r for r in new if dt.date.fromisoformat(r["DATE"]) > last_old]
    P, T, Z = {}, {}, {}
    for r in seq:
        d = dt.date.fromisoformat(r["DATE"])
        p = _num(r["PRCP"])
        md, da = _num(r.get("MDPR")), _num(r.get("DAPR"))
        if md is not None and da:
            n = int(da)
            for k in range(n):
                P[d - dt.timedelta(days=k)] = md / n
        elif p is not None:
            P[d] = p
        tx, tn = _num(r["TMAX"]), _num(r["TMIN"])
        if tx is not None and tn is not None:
            T[d] = ((tx + tn) / 2.0 - 32.0) * 5.0 / 9.0
        Z[d] = round(float(r["ELEVATION"]) / 0.3048, 0)
    return P, T, Z


def ridge_daily(tgt):
    rows = read_ghcn(os.path.join(tgt, "ghcnd_durrow_ridge_daily_1950-2025.csv"))
    P, T = {}, {}
    for r in rows:
        d = dt.date.fromisoformat(r["DATE"])
        p = _num(r["PRCP"])
        if p is not None:
            P[d] = p
        tx, tn = _num(r["TMAX"]), _num(r["TMIN"])
        if tx is not None and tn is not None:
            T[d] = ((tx + tn) / 2.0 - 32.0) * 5.0 / 9.0
    return P, T


def snotel(tgt, name):
    path = os.path.join(tgt, name)
    rows = []
    with open(path) as f:
        lines = [l for l in f if not l.startswith("#")]
    rd = csv.reader(lines)
    hdr = next(rd)
    for r in rd:
        rows.append(dict(zip(hdr, r)))
    out = {}
    for r in rows:
        d = dt.date.fromisoformat(r["Date"])
        out[d] = dict(swe=_num(r[hdr[1]]), prec=_num(r[hdr[2]]), tavg=_num(r[hdr[5]]))
    return out


def storm_lapse(PV, TV, PR, TR, ZV, zr=2710.0, min_p=0.5):
    """The storm lapse rate (deg C per km): the valley-ridge difference of the day-mean temperature on the days both
    stations record 0.5 in or more, over the elevation between them, the median over the record."""
    vals = []
    for d, p in PV.items():
        if p is None or p < min_p or PR.get(d) is None or PR[d] < min_p or d not in TV or d not in TR:
            continue
        vals.append((TV[d] - TR[d]) / ((zr - ZV[d]) / FT_PER_KM))
    return float(np.median(vals)), len(vals)


def rain_snow_temperature(sn):
    """The SNOTEL day-mean temperature at which half a day's precipitation stays as snow: days with 0.4 in or more of
    precipitation; the snow share is the day's SWE gain over its precipitation, clipped to 0..1; a logistic fit."""
    xs, ys = [], []
    days = sorted(sn)
    for i in range(len(days) - 1):
        d, e = days[i], days[i + 1]
        if (e - d).days != 1 or d.month in (6, 7, 8, 9):
            continue
        a, b = sn[d], sn[e]
        if None in (a["prec"], b["prec"], a["swe"], b["swe"], a["tavg"]):
            continue
        dp = b["prec"] - a["prec"]
        if dp < 0.4 or dp > 8:
            continue
        frac = float(np.clip((b["swe"] - a["swe"]) / dp, 0, 1))
        xs.append((a["tavg"] - 32.0) * 5.0 / 9.0)
        ys.append(frac)
    xs, ys = np.array(xs), np.array(ys)
    from scipy.optimize import curve_fit

    def lg(t, t50, k):
        return 1.0 / (1.0 + np.exp((t - t50) / k))
    (t50, k), _ = curve_fit(lg, xs, ys, p0=(1.0, 0.7))
    return float(t50), float(abs(k)), len(xs)


def snotel_lapse(sh, sc, zh=4160.0, zc=5630.0, min_p=0.5):
    """The storm lapse rate from the two SNOTEL sites (same calendar day): days both catch 0.5 in or more."""
    v = []
    for d in sh:
        e = d + dt.timedelta(days=1)
        if d in sc and e in sh and e in sc:
            a, b, c, f = sh[d], sh[e], sc[d], sc[e]
            if None in (a["tavg"], c["tavg"], a["prec"], b["prec"], c["prec"], f["prec"]):
                continue
            if b["prec"] - a["prec"] >= min_p and f["prec"] - c["prec"] >= min_p:
                v.append(((a["tavg"] - c["tavg"]) * 5.0 / 9.0) / ((zc - zh) / FT_PER_KM))
    return float(np.median(v)), len(v)


def orographic(st_list, PV, TV, PR, ZV, lapse, t50, zr=2710.0, warm_margin=1500.0):
    """Precipitation at z relative to 1,000 ft, P(z) = P(1,000 ft) (1 + g (z - 1,000)/1,000): g from the ridge's
    storm totals over the valley's in the storms whose snow line sat at least warm_margin feet above the ridge (both
    gauges catching rain), the median ratio over those storms."""
    ratios = []
    for st in st_list:
        tv = storm_temperature(st, PV, TV)
        if tv is None:
            continue
        zv = ZV[st[0]]
        sl = zv + (tv - t50) / lapse * FT_PER_KM
        if sl < zr + warm_margin:
            continue
        days = [d for d in st] + [st[-1] + dt.timedelta(days=1)]
        if any(PR.get(d) is None for d in days):
            continue
        pv = sum(PV[d] for d in st)
        pr = sum(PR[d] for d in days)
        ratios.append(pr / pv)
    r = float(np.median(ratios))
    zv = 1180.0
    # r = (1 + g (zr - 1000)/1000) / (1 + g (zv - 1000)/1000)
    g = (r - 1.0) / ((zr - 1000.0) / 1000.0 - r * (zv - 1000.0) / 1000.0)
    return float(g), dict(ratio=r, n=len(ratios))


def bands(tgt):
    wb = load_workbook(os.path.join(tgt, "region3_basin_characteristics.xlsx"), data_only=True)
    ws = wb["Elevation bands"]
    head = [str(h or "") for h in next(ws.iter_rows(min_row=3, max_row=3, values_only=True))]
    jr = next(j for j, h in enumerate(head) if h.startswith("Coyner"))
    jc = next(j for j, h in enumerate(head) if h.startswith("Durrow"))
    zc, ar, ac = [], [], []
    for row in ws.iter_rows(min_row=4, values_only=True):
        if not row or row[0] is None:
            continue
        lo, hi = [float(x) for x in str(row[0]).split("-")]
        zc.append((lo + hi) / 2.0)
        ar.append(float(row[jr] or 0))
        ac.append(float(row[jc] or 0))
    g = wb["Gauged basins"]
    areas = {}
    for row in g.iter_rows(min_row=4, values_only=True):
        if row and row[0]:
            areas[str(row[0])] = dict(area=float(row[2]), map=float(row[6]))
    d = wb["Durrow Ck at Ransom Bar Rd"]
    area_c = None
    for row in d.iter_rows(values_only=True):
        if row and row[0] == "Drainage area (sq mi)":
            area_c = float(row[1])
    return np.array(zc), np.array(ar), np.array(ac), areas, area_c


def storms(PV, min_total=1.0):
    """Storms in the valley record: runs of days with 0.10 in or more, holding 1.0 in or more."""
    days = sorted(PV)
    out = []
    cur = []
    for d in days:
        p = PV[d] or 0.0
        if p >= 0.10 and (not cur or (d - cur[-1]).days == 1):
            cur.append(d)
            continue
        if cur and sum(PV[x] for x in cur) >= min_total:
            out.append(list(cur))
        cur = [d] if p >= 0.10 else []
    if cur and sum(PV[x] for x in cur) >= min_total:
        out.append(cur)
    return out


def storm_temperature(st, PV, TV):
    w = [PV[d] for d in st if d in TV]
    t = [TV[d] for d in st if d in TV]
    if not t:
        return None
    return float(np.average(t, weights=w))


def depth(zc, area, total, snowline_t, lapse, t50, k, g, zv=1180.0, ramp="logistic"):
    """Basin-average rain (inches) from a storm: total is the valley's storm total, snowline_t the valley's storm
    temperature; each band rains in the share the SNOTEL fit gives at the band's temperature."""
    tz = snowline_t - lapse * (zc - zv) / FT_PER_KM
    if ramp == "logistic":
        rain = 1.0 - 1.0 / (1.0 + np.exp((tz - t50) / k))
    else:
        rain = (tz > t50).astype(float)
    rel = (1.0 + g * (zc - 1000.0) / 1000.0) / (1.0 + g * (zv - 1000.0) / 1000.0) if g is not None else np.ones(len(zc))
    return float((area * rel * rain).sum() / area.sum() * total)


def match(floods, st_list, PV, TV, max_after=2):
    """Each river flood's storm: the storm whose last wet day is no more than max_after days before the peak and whose
    first is on or before it, cut at the peak day (rain after the peak made no part of it). Floods with no storm
    (snowmelt) are left out of the transfer."""
    out = []
    for d, q in floods:
        best = None
        for st in st_list:
            if st[0] <= d <= st[-1] + dt.timedelta(days=max_after):
                best = st
        if best is not None:
            cut = [x for x in best if x <= d]
            out.append((d, q, cut if cut else best))
    return out


def flood_day(st, d, PV, TV, back=2):
    """The flood's wettest day: the storm day with the most valley precipitation among the peak day and the two days
    before it (the day whose snow line set where the flood's heaviest rain fell)."""
    cand = [x for x in st if 0 <= (d - x).days <= back and x in TV]
    if not cand:
        cand = [x for x in st if x in TV]
    if not cand:
        return None
    return max(cand, key=lambda x: (PV[x], x))


def transfer(matched, PV, TV, ZV, zc, ar, ac, lapse, t50, k, g, b, ramp="logistic", annual_only=None, storm_mean=False,
             fit_out=None):
    series = {}
    for d, q, st in matched:
        wy = d.year + (1 if d.month >= 10 else 0)
        if annual_only is not None and annual_only.get(wy, (None,))[0] != d:
            continue
        core = flood_day(st, d, PV, TV)
        if core is None:
            continue
        tot = sum(PV[x] for x in st)
        tv = TV[core] if not storm_mean else storm_temperature(st, PV, TV)
        zv = ZV[core]
        dr = depth(zc, ar, tot, tv, lapse, t50, k, g, zv=zv, ramp=ramp)
        dc = depth(zc, ac, tot, tv, lapse, t50, k, g, zv=zv, ramp=ramp)
        if dr <= 0.01:
            continue
        v = q * (ac.sum() / ar.sum()) ** b * dc / dr
        series[wy] = max(series.get(wy, 0.0), v)
        if fit_out is not None:
            fit_out.append((q, dr))
    return series


def read_lcd(tgt):
    """The airport's routine hourly reports (FM-15; the specials repeat rain the next routine report carries): hourly
    temperature (deg C) and precipitation (inches, a trace as 0.001) by hour from T0, and the airport's elevation (ft)."""
    T = np.full(NH, np.nan)
    P = np.full(NH, np.nan)
    z = None
    with open(os.path.join(tgt, LCD_FILE)) as f:
        for row in csv.DictReader(f):
            if row["REPORT_TYPE"].strip() != "FM-15":
                continue
            if z is None:
                z = float(row["ELEVATION"]) / 0.3048
            d = dt.datetime.fromisoformat(row["DATE"])
            i = int((d - T0).total_seconds() // 3600)
            if not 0 <= i < NH:
                continue
            t = row["HourlyDryBulbTemperature"].rstrip("s*").strip()
            if t:
                T[i] = (float(t) - 32.0) * 5.0 / 9.0
            p = row["HourlyPrecipitation"].rstrip("s*").strip()
            if p == "T":
                P[i] = 0.001
            elif p:
                P[i] = float(p)
    return T, P, z


def flood_hours(tgt):
    """Every flood in the river's peak files with its peak hour: (date, hour, discharge); an annual peak with no time
    takes the time the peaks-above-base file gives that day, else noon."""
    ann = read_rdb(os.path.join(tgt, "usgs_12183450_coyner_r_annual_peaks.txt"))
    pot = read_rdb(os.path.join(tgt, "usgs_12183450_coyner_r_peaks_above_base.txt"))

    def hour(dd, tm):
        hh, mm = (int(x) for x in tm.split(":")) if tm else (12, 0)
        return int((dt.datetime(dd.year, dd.month, dd.day, hh, mm) - T0).total_seconds() // 3600)
    out = {}
    pot_tm = {}
    for r in pot:
        d = dt.date.fromisoformat(r["peak_dt"])
        pot_tm[d] = r["peak_tm"]
        h = hour(d, r["peak_tm"])
        out[d] = (h, max(out.get(d, (0, 0.0))[1], float(r["peak_va"])))
    annual = {}
    for r in ann:
        d = dt.date.fromisoformat(r["peak_dt"])
        q = float(r["peak_va"])
        tm = r.get("peak_tm") or pot_tm.get(d, "")
        h = hour(d, tm)
        out[d] = (h, max(out.get(d, (0, 0.0))[1], q))
        annual[d.year + (1 if d.month >= 10 else 0)] = (d, q)
    return sorted((d, h, q) for d, (h, q) in out.items()), annual


def lcd_event(i, P, gap=6, thr=0.005, back=36):
    """The rain that fed a peak at hour i: back from the peak to the last wet hour within back hours, then every wet
    hour before it with no dry spell longer than gap hours (missing hours count as dry)."""
    j = min(i, NH - 1)
    lim = j - back
    while j > lim and not (P[j] >= thr):
        j -= 1
    if j <= lim:
        return None
    hrs = []
    dry = 0
    while j >= 0:
        if P[j] >= thr:
            hrs.append(j)
            dry = 0
        else:
            dry += 1
            if dry > gap:
                break
        j -= 1
    return np.array(sorted(hrs))


def event_temperature(h, T, P, how="pw"):
    """The temperature the rain fell at: weighted by each hour's rain (pw), the plain mean of the rain hours (mean), or
    the wettest 24 hours, rain-weighted (core)."""
    h = h[~np.isnan(T[h])]
    if len(h) == 0:
        return None
    if how == "mean":
        return float(T[h].mean())
    if how == "core" and len(h) > 24:
        cs = np.convolve(P[h], np.ones(24), "valid")
        s0 = int(np.argmax(cs))
        h = h[s0:s0 + 24]
    return float(np.average(T[h], weights=P[h]))


def transfer_hourly(fh, T, P, zc, ar, ac, lapse, t50, k, g, b, zv, ramp="logistic", gap=6, how="pw", annual_only=None,
                    fit_out=None, rows_out=None, back=36):
    """The creek's annual series: every river flood fed by rain is carried at the ratio of the rain each basin took
    below the storm's snow line (the snow line from the airport's temperature while the rain fell) and the state
    equation's drainage-area exponent; a flood with no rain in the 36 hours before it (snowmelt) is not carried."""
    series = {}
    for d, i, q in fh:
        wy = d.year + (1 if d.month >= 10 else 0)
        if annual_only is not None and annual_only.get(wy, (None,))[0] != d:
            continue
        h = lcd_event(i, P, gap=gap, back=back)
        if h is None or len(h) < 2:
            continue
        if how == "peak":
            j = min(i, NH - 1)
            while j > 0 and np.isnan(T[j]):
                j -= 1
            tv = float(T[j])
        else:
            tv = event_temperature(h, T, P, how=how)
        if tv is None:
            continue
        tot = float(np.nansum(P[h]))
        dr = depth(zc, ar, tot, tv, lapse, t50, k, g, zv=zv, ramp=ramp)
        dc = depth(zc, ac, tot, tv, lapse, t50, k, g, zv=zv, ramp=ramp)
        if dr <= 0.01:
            continue
        v = q * (ac.sum() / ar.sum()) ** b * dc / dr
        series[wy] = max(series.get(wy, 0.0), v)
        if fit_out is not None:
            fit_out.append((q, dr, tot))
        if rows_out is not None:
            rows_out.append((d, q, tv, tot, dr, dc, v))
    return series


def record_years(rec):
    """Water years in a workbook record span such as "1951-2025"."""
    y0, y1 = (int(x) for x in str(rec).split("-"))
    return y1 - y0 + 1


def short_gauge(tgt):
    """The gauged basin whose record is under 25 years: site, area, elevation bands (aligned with bands()) and its annual
    peaks as (date, hour, discharge)."""
    wb = load_workbook(os.path.join(tgt, "region3_basin_characteristics.xlsx"), data_only=True)
    site = area = name = None
    for row in wb["Gauged basins"].iter_rows(min_row=4, values_only=True):
        if row and row[0] and record_years(row[8]) < 25:
            site, name, area = str(row[0]), str(row[1]), float(row[2])
    ws = wb["Elevation bands"]
    head = [str(h or "") for h in next(ws.iter_rows(min_row=3, max_row=3, values_only=True))]
    js = next(j for j, h in enumerate(head) if h.split(" (")[0].lower().startswith(name.split()[0].lower()))
    bands_s = np.array([float(r[js] or 0) for r in ws.iter_rows(min_row=4, values_only=True) if r and r[0] is not None])
    peaks = []
    for r in read_rdb(os.path.join(tgt, "usgs_%s_annual_peaks.txt" % site)):
        d = dt.date.fromisoformat(r["peak_dt"])
        hh, mm = (int(x) for x in r["peak_tm"].split(":")) if r.get("peak_tm") else (12, 0)
        peaks.append((d, int((dt.datetime(d.year, d.month, d.day, hh, mm) - T0).total_seconds() // 3600), float(r["peak_va"])))
    return site, area, bands_s, peaks


def validate(tgt, fh, T, P, zc, ar, area_r, est, b, zv, PV=None, TV=None):
    """Each construction of the carry run from the river to the short-record foothill gauge, flood by flood: the river's
    flood in the 24 hours before to 36 hours after the gauge's annual peak, carried to the gauge's own bands and area,
    against the peak it recorded. Returns construction -> (median log error, median absolute log error, floods)."""
    site, area_s, bs, peaks = short_gauge(tgt)
    pairs = []
    for d, hs, qs in peaks:
        near = [(q, i, dd) for dd, i, q in fh if hs - 24 <= i <= hs + 36]
        if near:
            q, i, dd = max(near)
            pairs.append((qs, q, i, dd))

    def temp(i, dd, how):
        if how in ("pw", "peak"):
            if how == "peak":
                j = min(i, NH - 1)
                while j > 0 and np.isnan(T[j]):
                    j -= 1
                return float(T[j])
            h = lcd_event(i, P)
            return None if h is None or len(h) < 2 else event_temperature(h, T, P)
        days = [dd - dt.timedelta(days=k) for k in range(3) if (dd - dt.timedelta(days=k)) in TV]
        if how == "daily_peak_day":
            return TV.get(dd)
        w = [PV.get(x) or 0.0 for x in days]
        return float(np.average([TV[x] for x in days], weights=w)) if sum(w) > 0 else None
    cons = {"golden": dict(), "peak_hour": dict(how="peak"), "daily_peak_day": dict(how="daily_peak_day"),
            "daily_storm_mean": dict(how="daily_storm_mean"), "lapse_6.5": dict(lapse=6.5), "freezing_0C": dict(t50=0.0),
            "no_orography": dict(g=None), "textbook": dict(lapse=6.5, t50=0.0, g=None)}
    out = {}
    for name, ov in cons.items():
        e = []
        for qs, q, i, dd in pairs:
            t = temp(i, dd, ov.get("how", "pw"))
            if t is None:
                continue
            L, t50, g = ov.get("lapse", est["lapse"]), ov.get("t50", est["t50"]), ov.get("g", est["g"])
            dr = depth(zc, ar, 1.0, t, L, t50, est["k"], g, zv=zv)
            ds = depth(zc, bs, 1.0, t, L, t50, est["k"], g, zv=zv)
            if dr > 0.01:
                e.append(np.log(q * (area_s / area_r) ** b * ds / dr / qs))
        out[name] = (float(np.median(e)), float(np.median(np.abs(e))), len(e))
    e = [np.log(q * (area_s / area_r) ** b / qs) for qs, q, i, dd in pairs]
    out["drainage_area"] = (float(np.median(e)), float(np.median(np.abs(e))), len(e))
    # the shortcuts a short record invites, carried to the creek: one concurrent ratio on the river's curve, and the
    # short record extended on the river's by MOVE.1
    shortcuts = {"median_ratio": float(np.median([qs / q for qs, q, i, dd in pairs]))}
    return out, pairs, shortcuts, (site, area_s)


def own_fit(pairs, min_q=0.0):
    """How well the river's storm rain over its area below the snow line explains its own flood peaks: the
    correlation of the logarithms over the matched floods."""
    a = np.array([(np.log(q), np.log(dr)) for q, dr in pairs if q >= min_q and dr > 0.05])
    return float(np.corrcoef(a[:, 0], a[:, 1])[0, 1]), len(a)


def curve(series, years=range(1951, 2026), regional=True, low_test=True):
    vals = np.array([series[y] for y in years if y in series])
    par = F.fit(vals, regional=regional, low_test=low_test)
    return par, vals


AEPS = (0.5, 0.1, 0.04, 0.02, 0.01, 0.002)


def station_map(PV, PR, sns, zc, area):
    """A basin's mean annual precipitation (in) from the stations: the water-year means of the two cooperative
    stations and the SNOTEL sites, a straight line against elevation, averaged over the basin's elevation bands."""
    def wy_tot(P, years):
        tot = {}
        for d, p in P.items():
            wy = d.year + (1 if d.month >= 10 else 0)
            if wy in years and p is not None:
                tot[wy] = tot.get(wy, 0.0) + p
        return float(np.mean([tot[y] for y in years if y in tot]))
    years = set(range(1991, 2021))
    z = [1180.0, 2710.0]
    pm = [wy_tot(PV, years), wy_tot(PR, years)]
    for zz, sn in sns:
        tot = [sn[dt.date(y, 9, 30)]["prec"] for y in years if dt.date(y, 9, 30) in sn and sn[dt.date(y, 9, 30)]["prec"] is not None]
        z.append(zz)
        pm.append(float(np.mean(tot)))
    sl, ic = np.polyfit(z, pm, 1)
    return float(((ic + sl * zc) * area).sum() / area.sum()), dict(zip(z, pm))


def creek_series(fh, T, P, zc, ar, ac, est, b0, zv, **kw):
    fo, ro = [], []
    s = transfer_hourly(fh, T, P, zc, ar, ac, kw.get("lapse", est["lapse"]), kw.get("t50", est["t50"]), kw.get("k", est["k"]),
                        kw.get("g", est["g"]), kw.get("b", b0), zv, ramp=kw.get("ramp", "logistic"), gap=kw.get("gap", 6),
                        how=kw.get("how", "pw"), annual_only=kw.get("annual_only"), fit_out=fo, rows_out=ro)
    return s, fo, ro


def curve_of(series, years=range(1951, 2026), regional=True, low_test=True):
    """Bulletin 17C on the creek's series: a water year with no flood fed by rain is known only to lie below the low-flood
    threshold (an expected-moments interval)."""
    vals = np.array([series[y] for y in years if y in series])
    missing = [y for y in years if y not in series]
    return F.fit(vals, regional=regional, low_test=low_test, extra_low=len(missing)), vals, missing


def run(tgt, rated=None, equations=None):
    fh, annual = flood_hours(tgt)
    T, P, zv = read_lcd(tgt)
    PV, TV, ZV = valley_daily(tgt)
    PR, TR = ridge_daily(tgt)
    sh = snotel(tgt, "snotel_1187_hatchet_meadow_daily.csv")
    sc = snotel(tgt, "snotel_1203_corbel_ridge_daily.csv")
    lapse, n_lapse = storm_lapse(PV, TV, PR, TR, ZV)
    th = rain_snow_temperature(sh)
    tc = rain_snow_temperature(sc)
    t50 = (th[0] + tc[0]) / 2.0
    k = (th[1] + tc[1]) / 2.0
    zc, ar, ac, areas, area_c = bands(tgt)
    st_list = storms(PV)
    g, station_means = orographic(st_list, PV, TV, PR, ZV, lapse, t50)
    est = dict(lapse=lapse, t50=t50, k=k, g=g)
    ser, fo, rows = creek_series(fh, T, P, zc, ar, ac, est, STATE_B, zv)
    own_r, own_n = own_fit([(q_, dr_) for q_, dr_, _ in fo])
    area_r, _ = own_fit([(q_, tot_) for q_, _, tot_ in fo])
    par, vals, missing = curve_of(ser)
    q = {a: F.quantile(par, a) for a in AEPS}
    rq = np.array([annual[y][1] for y in range(1951, 2026)])
    rpar = F.fit(rq)
    r0 = F.quantile(rpar, 0.01) * (area_c / areas["12183450"]["area"]) ** STATE_B
    R = dict(lapse=lapse, n_lapse=n_lapse, t50=t50, k=k, t50_sites=(th[0], tc[0]), n_rs=(th[2], tc[2]), g=g, zv=zv,
             station_means=station_means, n_floods=len(fh), n_matched=len(rows), rows=rows, series=ser, missing=missing,
             par=par, q=q, river_par=rpar, river_q={a: F.quantile(rpar, a) for a in AEPS}, r0=r0, annual=annual,
             area_r=areas["12183450"]["area"], area_c=area_c, areas=areas, own_r=own_r, own_n=own_n, total_rain_r=area_r)
    variants = {
        "gap_3": dict(gap=3), "gap_12": dict(gap=12), "gap_24": dict(gap=24), "rain_hour_mean": dict(how="mean"),
        "wettest_24h": dict(how="core"), "sharp": dict(ramp="sharp"), "annual_only": dict(annual_only=annual),
        "b_1.0": dict(b=1.0), "b_0.70": dict(b=0.70), "lapse_snotel": dict(lapse=snotel_lapse(sh, sc)[0]),
        "t50_hatchet": dict(t50=th[0]), "t50_corbel": dict(t50=tc[0]),
        "peak_hour": dict(how="peak"),
        "lapse_6.5": dict(lapse=6.5), "freezing_0C": dict(t50=0.0), "lapse_6.5_0C": dict(lapse=6.5, t50=0.0),
        "no_orography": dict(g=None), "textbook": dict(lapse=6.5, t50=0.0, g=None),
    }
    V = {}
    for name, ov in variants.items():
        s2, fo2, _ = creek_series(fh, T, P, zc, ar, ac, est, STATE_B, zv, **ov)
        p2, _, miss2 = curve_of(s2)
        V[name] = {a: F.quantile(p2, a) for a in AEPS}
        V[name]["series"] = s2
        V[name]["par"] = p2
    for name, kw in (("station_skew", dict(regional=False)), ("no_low_test", dict(low_test=False))):
        p2, _, _ = curve_of(ser, **kw)
        V[name] = {a: F.quantile(p2, a) for a in AEPS}
        V[name]["series"] = ser
        V[name]["par"] = p2
    # the daily-record snow lines the hourly record supersedes: the valley's daily mean on the flood's wettest day, and on
    # the peak day
    floods_d, _ = river_floods(tgt)
    matched = match(floods_d, st_list, PV, TV)
    for name, kw in (("daily_wettest_day", dict()), ("daily_storm_mean", dict(storm_mean=True))):
        s2 = transfer(matched, PV, TV, ZV, zc, ar, ac, lapse, t50, k, g, STATE_B, **kw)
        p2, _, _ = curve_of(s2)
        V[name] = {a: F.quantile(p2, a) for a in AEPS}
        V[name]["series"] = s2
        V[name]["par"] = p2
    R["variants"] = V
    # the temperature at the river's peak hour against the rain's own
    dry, diff = [], []
    for d_, q_, tv_, tot_, dr_, dc_, v_ in rows:
        i_ = next(i for dd, i, qq in fh if dd == d_)
        j_ = min(i_, NH - 1)
        dry.append(not (P[j_] >= 0.005))
        if not np.isnan(T[j_]):
            diff.append(T[j_] - tv_)
    R["peak_hour"] = dict(dry_share=float(np.mean(dry)), median_diff=float(np.median(diff)))
    R["lapse_snotel"], R["n_lapse_snotel"] = snotel_lapse(sh, sc)
    val, vpairs, vshort, (vsite, varea) = validate(tgt, fh, T, P, zc, ar, areas["12183450"]["area"], est, STATE_B, zv, PV, TV)
    R["validation"], R["val_pairs"], R["val_site"], R["val_area"] = val, vpairs, vsite, varea
    # shortcuts: the median concurrent ratio on the river's curve, carried by area to the creek; the short record extended
    # on the river's annual peaks by MOVE.1 and carried by area; the short record's own curve carried by area
    rq_ = {y: annual[y][1] for y in annual}
    ratio = float(np.median([qs / q for qs, q, i, dd in vpairs]))
    R["sc_ratio"] = F.quantile(rpar, 0.01) * ratio * (area_c / varea) ** STATE_B
    sp_ = {d.year + (1 if d.month >= 10 else 0): q for d, i, q in short_gauge(tgt)[3]}
    xs = np.log10([rq_[y] for y in sorted(sp_)]); ys = np.log10([sp_[y] for y in sorted(sp_)])
    b1 = ys.std(ddof=1) / xs.std(ddof=1) * np.sign(np.corrcoef(xs, ys)[0, 1]); a1 = ys.mean() - b1 * xs.mean()
    ext = [10 ** (a1 + b1 * np.log10(rq_[y])) for y in range(1951, 2026) if y not in sp_] + list(sp_.values())
    R["sc_move1"] = F.quantile(F.fit(np.array(ext)), 0.01) * (area_c / varea) ** STATE_B
    R["sc_own"] = F.quantile(F.fit(np.array(list(sp_.values()))), 0.01) * (area_c / varea) ** STATE_B
    R["short_years"] = len(sp_)
    p_creek, st_means = station_map(PV, PR, [(4160.0, sh), (5630.0, sc)], zc, ac)
    R["map_creek"] = p_creek
    R["map_station_means"] = st_means
    if equations:
        e = equations[100]
        R["regional_eq"] = e["a"] * area_c ** e["b"] * p_creek ** e["c"]
    wb = load_workbook(os.path.join(tgt, "region3_basin_characteristics.xlsx"), data_only=True)
    gsh = wb["Gauged basins"]
    pts = []
    for row in gsh.iter_rows(min_row=4, values_only=True):
        if not row or not row[0] or record_years(row[8]) < 25:
            continue
        site = str(row[0])
        fn = "usgs_12183450_coyner_r_annual_peaks.txt" if site == "12183450" else "usgs_%s_annual_peaks.txt" % site
        rr = read_rdb(os.path.join(tgt, fn))
        qq = np.array([float(r["peak_va"]) for r in rr])
        pts.append((float(row[3]), np.log(F.quantile(F.fit(qq), 0.01) / float(row[2]) ** STATE_B)))
    pts = np.array(pts)
    R["regional_unit_flood"] = float(np.mean(np.exp(pts[:, 1])) * area_c ** STATE_B)
    slope, icpt = np.polyfit(pts[:, 0], pts[:, 1], 1)
    zmean_c = float((zc * ac).sum() / ac.sum())
    R["elev_reg"] = float(np.exp(icpt + slope * zmean_c) * area_c ** STATE_B)
    # its 90 per cent prediction interval at the creek's mean elevation, five gauges, three degrees of freedom
    xs, ys = pts[:, 0], pts[:, 1]
    resid = ys - (icpt + slope * xs)
    s = float(np.sqrt((resid ** 2).sum() / (len(xs) - 2)))
    se = s * np.sqrt(1 + 1.0 / len(xs) + (zmean_c - xs.mean()) ** 2 / ((xs - xs.mean()) ** 2).sum())
    tq = stats.t.ppf(0.95, len(xs) - 2)
    R["elev_reg_interval"] = tuple(float(np.exp(icpt + slope * zmean_c + sgn * tq * se) * area_c ** STATE_B) for sgn in (-1, 1))
    R["elev_range"] = (float(xs.min()), float(xs.max()))
    if rated:
        R["rated"] = rated
        R["aep_rated"] = {k_: F.aep_of(par, v) for k_, v in rated.items()}
    return R
