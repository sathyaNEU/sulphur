"""task3: the data files of the pack, written the way each system exports them."""
import csv
import datetime as dt
import os

import numpy as np

import world as W

STATION = "8673718"
STATION_NAME = "Port Tolliver, Brayle River Entrance, GA"
USGS = "02203560"
USGS_NAME = "BRAYLE RIVER NEAR HENSLEY, GA"
LST = np.timedelta64(5, "h")
VERIFIED_THROUGH = np.datetime64("2026-09-30T23:59")  # local standard time; October 2026 is preliminary


def _lst(t):
    return t - LST


def hilo(th6, y, smooth=7):
    """High and low waters of a 6-minute series: extremes of a 42-minute running mean, the raw value taken at the
    6-minute reading nearest that extreme's peak."""
    k = smooth
    ys = np.convolve(y, np.ones(k) / k, mode="same")
    d = np.diff(ys)
    hi = np.where((d[:-1] > 0) & (d[1:] <= 0))[0] + 1
    lo = np.where((d[:-1] < 0) & (d[1:] >= 0))[0] + 1
    out = []
    for idx, is_hi in ((hi, True), (lo, False)):
        keep = []
        for i in idx:
            a, b = max(0, i - 3), min(len(y), i + 4)
            j = a + (np.argmax(y[a:b]) if is_hi else np.argmin(y[a:b]))
            keep.append(j)
        keep = np.array(keep, dtype=int)
        out.append((keep, np.full(len(keep), is_hi)))
    idx = np.concatenate([out[0][0], out[1][0]])
    kind = np.concatenate([out[0][1], out[1][1]])
    o = np.argsort(idx)
    idx, kind = idx[o], kind[o]
    # alternate high and low; where two of a kind follow, keep the more extreme
    keep_i, keep_k = [], []
    for i, kk in zip(idx, kind):
        if keep_k and keep_k[-1] == kk:
            if (kk and y[i] > y[keep_i[-1]]) or ((not kk) and y[i] < y[keep_i[-1]]):
                keep_i[-1] = i
            continue
        keep_i.append(i)
        keep_k.append(kk)
    return np.array(keep_i), np.array(keep_k)


def types(t_lst, h, is_hi):
    """NOAA-style codes: of each local day's two highs the higher is HH, of its two lows the lower is LL."""
    day = t_lst.astype("datetime64[D]")
    code = np.where(is_hi, "H", "L").astype(object)
    for flag in (True, False):
        m = np.where(is_hi == flag)[0]
        dd = day[m]
        brk = np.r_[0, np.where(np.diff(dd.astype(np.int64)) != 0)[0] + 1, len(m)]
        for a, b in zip(brk[:-1], brk[1:]):
            grp = m[a:b]
            if len(grp) >= 2:
                j = grp[np.argmax(h[grp])] if flag else grp[np.argmin(h[grp])]
                code[j] = "HH" if flag else "LL"
            elif len(grp) == 1:
                code[grp[0]] = "HH" if flag else "LL"
    return code


def in_any(t, spans):
    m = np.zeros(len(t), dtype=bool)
    for a, b in spans:
        m |= (t >= np.datetime64(a)) & (t < np.datetime64(b))
    return m


def write_hilo(path, S, which):
    th6, y = S["th6"], S["obs6"] if which == "obs" else S["pred6"]
    idx, is_hi = hilo(th6, y)
    t = _lst(th6[idx])
    h = y[idx]
    if which == "obs":
        ok = (~in_any(th6[idx], W.GAUGE_OUT)) & (t <= VERIFIED_THROUGH) & (t >= np.datetime64("1955-01-01"))
    else:
        ok = (t < np.datetime64("2028-05-01")) & (t >= np.datetime64("1955-01-01"))
    t, h, is_hi = t[ok], h[ok], is_hi[ok]
    code = types(t, h, is_hi)
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        if which == "obs":
            w.writerow(["Date Time", " Water Level", " Type", " I", " L"])
            for tt, hh, cc in zip(t, h, code):
                w.writerow([str(tt.astype("datetime64[m]")).replace("T", " "), " %.3f" % hh, " " + cc, " 0", " 0"])
        else:
            w.writerow(["Date Time", " Prediction", " Type"])
            for tt, hh, cc in zip(t, h, code):
                w.writerow([str(tt.astype("datetime64[m]")).replace("T", " "), " %.3f" % hh, " " + cc])
    return len(t)


def write_hourly(path, S):
    th6 = S["th6"]
    th1 = th6[::10]
    obs1, pred1 = S["obs6"][::10], S["pred6"][::10]
    t = _lst(th1)
    m = (t >= np.datetime64("2000-01-01T00:00")) & (t < np.datetime64("2026-11-01T00:00"))
    out = in_any(th1, W.GAUGE_OUT)
    n = 0
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Date", "Time (LST)", "Predicted (ft)", "Preliminary (ft)", "Verified (ft)"])
        for i in np.where(m)[0]:
            ts = str(t[i].astype("datetime64[m]"))
            d, hm = ts[:10].replace("-", "/"), ts[11:16]
            p = "%.3f" % pred1[i]
            if out[i]:
                w.writerow([d, hm, p, "", ""])
            elif t[i] > VERIFIED_THROUGH:
                w.writerow([d, hm, p, "%.3f" % obs1[i], ""])
            else:
                w.writerow([d, hm, p, "", "%.3f" % obs1[i]])
            n += 1
    return n


def monthly_rows(S):
    th6 = S["th6"]
    t6 = _lst(th6)
    obs6 = S["obs6"]
    idx, is_hi = hilo(th6, obs6)
    th, hh = t6[idx], obs6[idx]
    code = types(th, hh, is_hi)
    out_h = in_any(th6[::10], W.GAUGE_OUT)
    t1 = t6[::10]
    o1 = obs6[::10]
    rows = []
    for m in np.arange(np.datetime64("1955-01"), np.datetime64("2026-10")):
        a, b = m.astype("datetime64[m]"), (m + 1).astype("datetime64[m]")
        sel = (t1 >= a) & (t1 < b)
        good = sel & ~out_h
        frac = good.sum() / max(sel.sum(), 1)
        hs = (th >= a) & (th < b) & ~in_any(th6[idx], W.GAUGE_OUT)
        y, mo = int(str(m)[:4]), int(str(m)[5:7])
        if frac < 0.9:
            rows.append([y, mo] + [""] * 16)
            continue
        hw = hh[hs & is_hi]
        lw = hh[hs & ~is_hi]
        hhw = hh[hs & (code == "HH")]
        llw = hh[hs & (code == "LL")]
        mhhw, mhw, mlw, mllw = hhw.mean(), hw.mean(), lw.mean(), llw.mean()
        msl = o1[good].mean()
        rows.append([y, mo, "%.3f" % o1[good].max(), "%.3f" % mhhw, "%.3f" % mhw, "%.3f" % msl, "%.3f" % ((mhw + mlw) / 2),
                     "%.3f" % mlw, "%.3f" % mllw, "%.3f" % ((mhhw + mllw) / 2), "%.3f" % (mhhw - mllw), "%.3f" % (mhw - mlw),
                     "%.3f" % (mhhw - mhw), "%.3f" % (mlw - mllw), "", "", "%.3f" % o1[good].min(), ""])
    return rows


def write_monthly(path, S):
    rows = monthly_rows(S)
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Year", " Month", " Highest", " MHHW", " MHW", " MSL", " MTL", " MLW", " MLLW", " DTL", " GT", " MN",
                    " DHQ", " DLQ", " HWI", " LWI", " Lowest", " Inf"])
        for r in rows:
            w.writerow([r[0], " %d" % r[1]] + [(" " + str(x)) if x != "" else "" for x in r[2:]])
    return len(rows)


def epoch_datums(S):
    th6, obs6 = S["th6"], S["obs6"]
    t6 = _lst(th6)
    idx, is_hi = hilo(th6, obs6)
    th, hh = t6[idx], obs6[idx]
    code = types(th, hh, is_hi)
    ep = (th >= np.datetime64("1983-01-01")) & (th < np.datetime64("2002-01-01"))
    e1 = (t6[::10] >= np.datetime64("1983-01-01")) & (t6[::10] < np.datetime64("2002-01-01"))
    d = dict(MHHW=hh[ep & (code == "HH")].mean(), MHW=hh[ep & is_hi].mean(), MLW=hh[ep & ~is_hi].mean(),
             MLLW=hh[ep & (code == "LL")].mean(), MSL=obs6[::10][e1].mean())
    d["MTL"] = (d["MHW"] + d["MLW"]) / 2
    d["DTL"] = (d["MHHW"] + d["MLLW"]) / 2
    allok = ~in_any(th6[idx], W.GAUGE_OUT) & (th <= VERIFIED_THROUGH)
    j = np.argmax(np.where(allok & is_hi, hh, -99))
    k = np.argmin(np.where(allok & ~is_hi, hh, 99))
    d["max"] = (hh[j], th[j])
    d["min"] = (hh[k], th[k])
    return d


def write_datums(path, S):
    d = epoch_datums(S)
    stnd = 6.10
    lines = ["Datums for %s, %s" % (STATION, STATION_NAME),
             "Status: Accepted (Apr 17 2003)    Epoch: 1983-2001    Units: Feet    Datum: MLLW",
             "Control station: %s" % STATION, "",
             "Datum      Value    Description"]
    rows = [("MHHW", d["MHHW"], "Mean Higher-High Water"), ("MHW", d["MHW"], "Mean High Water"),
            ("MTL", d["MTL"], "Mean Tide Level"), ("MSL", d["MSL"], "Mean Sea Level"),
            ("DTL", d["DTL"], "Mean Diurnal Tide Level"), ("MLW", d["MLW"], "Mean Low Water"),
            ("MLLW", 0.0, "Mean Lower-Low Water"), ("NAVD88", -W.NAVD88_OF_MLLW, "North American Vertical Datum of 1988"),
            ("STND", -stnd, "Station Datum"), ("GT", d["MHHW"] - 0.0, "Great Diurnal Range"),
            ("MN", d["MHW"] - d["MLW"], "Mean Range of Tide"), ("DHQ", d["MHHW"] - d["MHW"], "Mean Diurnal High Water Inequality"),
            ("DLQ", d["MLW"] - 0.0, "Mean Diurnal Low Water Inequality")]
    for k, v, desc in rows:
        lines.append("%-9s %7.2f    %s" % (k, v, desc))
    lines += ["", "Maximum observed  %.2f ft  %s" % (d["max"][0], str(d["max"][1].astype("datetime64[m]")).replace("T", " ")),
              "Minimum observed  %.2f ft  %s" % (d["min"][0], str(d["min"][1].astype("datetime64[m]")).replace("T", " ")),
              "", "Times are local standard time (LST). Datums are computed from the 1983-2001 National Tidal Datum Epoch.",
              "NAVD88 is referenced to the station's bench marks by differential leveling (2019)."]
    with open(path, "w", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    return d


def write_river(path, S):
    days, Q = S["days"], S["Q"]
    m = (days >= np.datetime64("1985-10-01")) & (days <= np.datetime64("2026-10-31"))
    rng = W.rngs(8)
    est = set()
    for a in (np.datetime64("1998-01-04"), np.datetime64("2011-08-19"), np.datetime64("2019-12-02")):
        for k in range(int(rng.integers(5, 14))):
            est.add(a + np.timedelta64(k, "D"))
    lines = ["# U.S. Geological Survey", "# National Water Information System", "#",
             "# Data provided for site %s" % USGS, "#    TS   parameter     statistic     Description",
             "#  148201       00060     00003     Discharge, cubic feet per second (Mean)", "#",
             "# Data-value qualification codes included in this output:", "#     A  Approved for publication -- Processed and reviewed",
             "#     P  Provisional data subject to revision.", "#     e  Value has been estimated.", "#",
             "agency_cd\tsite_no\tdatetime\t148201_00060_00003\t148201_00060_00003_cd", "5s\t15s\t20d\t14n\t10s"]
    for d_, q in zip(days[m], Q[m]):
        sig = 3 if q < 1000 else (int(np.floor(np.log10(q))) - 2)
        v = int(round(q / 10 ** max(sig, 0)) * 10 ** max(sig, 0)) if q >= 1000 else int(round(q))
        code = "P" if d_ >= np.datetime64("2025-10-01") else "A"
        if d_ in est:
            code += ":e"
        lines.append("USGS\t%s\t%s\t%d\t%s" % (USGS, str(d_), v, code))
    with open(path, "w", newline="\n") as f:
        f.write("\n".join(lines) + "\n")
    return int(m.sum())


def site_series(S, site, t_from, t_to):
    """A low point's 6-minute water level (ft MLLW-equivalent at the gauge datum) between two UT instants."""
    th6 = S["th6"]
    s = W.SITES[site]
    a = np.searchsorted(th6, np.datetime64(t_from)) - 2000
    b = np.searchsorted(th6, np.datetime64(t_to)) + 2000
    lag = int(round(s["lag"] / 6.0))
    H = S["obs6"][a - lag:b - lag]
    M = W.low_frequency(None, S["obs6"][a - 8000:b + 8000])[8000:-8000]
    days = S["days"]
    di = np.searchsorted(days, (th6[a:b] - LST).astype("datetime64[D]"))  # USGS daily means are local days
    Q = S["Q"][np.clip(di, 0, len(days) - 1)]
    return th6[a:b], W.site_level(site, H, M, Q)


def write_logger(path, S, site, serial, title):
    t0, t1, off = W.CAMPAIGNS[site]
    off_td = np.timedelta64(off, "h")
    ut0, ut1 = np.datetime64(t0) - off_td, np.datetime64(t1) - off_td
    th6, lev6 = site_series(S, site, ut0, ut1)
    rng = W.rngs(20 + list(W.SITES).index(site))
    th = np.arange(ut0, ut1, np.timedelta64(15, "m"))
    x6 = (th6 - th6[0]) / np.timedelta64(1, "m")
    lev = np.interp((th - th6[0]) / np.timedelta64(1, "m"), x6, lev6)
    lev = lev + rng.normal(0, 0.025, len(lev))
    nav = lev + W.NAVD88_OF_MLLW
    bed = {"marsh": -1.35, "oyster": -1.10, "river": -4.80}[site]  # sensor elevation, ft NAVD88
    nav = np.maximum(nav, bed + np.abs(rng.normal(0, 0.006, len(nav))))
    doy = (th - th.astype("datetime64[Y]")) / np.timedelta64(1, "D")
    temp = 72 + 14 * np.cos(2 * np.pi * (doy - 215) / 365.25) + rng.normal(0, 0.6, len(th))
    lab = "(LGR S/N: %s, SEN S/N: %s)" % (serial, serial)
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, lineterminator="\n")
        f.write('"Plot Title: %s"\n' % title)
        w.writerow(["#", "Date Time, GMT%+03d:00" % off, "Water Level, ft %s" % lab, "Temp, °F %s" % lab])
        for i, (tt, v, tp) in enumerate(zip(th, nav, temp), start=1):
            local = (tt + off_td).astype("datetime64[s]").astype(dt.datetime)
            w.writerow([i, local.strftime("%m/%d/%y %I:%M:%S %p"), "%.3f" % v, "%.2f" % tp])
    return len(th)


def site_daily_max(S, site, d0, d1):
    """A low point's highest water level each local standard day from d0 to d1 (inclusive start, exclusive end)."""
    ut0 = np.datetime64(d0 + "T00:00") + LST
    ut1 = np.datetime64(d1 + "T00:00") + LST
    th, lev = site_series(S, site, ut0, ut1)
    sel = (th >= ut0) & (th < ut1)
    th, lev = th[sel], lev[sel]
    day = _lst(th).astype("datetime64[D]")
    brk = np.r_[0, np.where(np.diff(day.astype(np.int64)) != 0)[0] + 1, len(day)]
    mx = np.maximum.reduceat(lev, brk[:-1])
    hour_at = np.array([(_lst(th[a + np.argmax(lev[a:b])]) - day[a]) / np.timedelta64(1, "h") for a, b in zip(brk[:-1], brk[1:])])
    return day[brk[:-1]], mx, hour_at


def rainfall(days):
    rng = W.rngs(9)
    doy = (days - days.astype("datetime64[Y]")) / np.timedelta64(1, "D")
    p_wet = 0.27 + 0.10 * np.cos(2 * np.pi * (doy - 200) / 365.25)
    wet = rng.random(len(days)) < p_wet
    amt = rng.gamma(0.75, 0.55 + 0.25 * np.cos(2 * np.pi * (doy - 215) / 365.25), len(days))
    return np.where(wet, np.round(amt, 2), 0.0)


def write_rain(path, days, prcp):
    rng = W.rngs(10)
    doy = (days - days.astype("datetime64[Y]")) / np.timedelta64(1, "D")
    tmax = 77 + 15 * np.cos(2 * np.pi * (doy - 200) / 365.25) + rng.normal(0, 4.5, len(days))
    tmin = tmax - 19 + rng.normal(0, 3, len(days))
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["STATION", "NAME", "DATE", "PRCP", "TMAX", "TMIN"])
        for d_, p, a, b in zip(days, prcp, tmax, tmin):
            pr = "%.2f" % p
            if rng.random() < 0.004:
                pr = ""
            w.writerow(["USW00003817", "PORT TOLLIVER MUNICIPAL AIRPORT, GA US", str(d_), pr, "%d" % round(a), "%d" % round(b)])
    return len(days)


def write_sensor(path, S, prcp_days, prcp):
    """Front Street's ultrasonic street sensor over the travel lane at the low point, every 6 minutes in UT: distance
    to the surface below, and the vendor's water depth over the dry-road baseline set at install."""
    s = W.SITES["front"]
    t0, t1 = np.datetime64(W.SENSOR[0]), np.datetime64(W.SENSOR[1])
    th, lev = site_series(S, "front", t0, t1)
    sel = (th >= t0) & (th < t1) & ~in_any(th, W.SENSOR_OUT)
    th, lev = th[sel], lev[sel]
    rng = W.rngs(30)
    n = len(th)
    depth_ft = np.maximum(lev - s["level"], 0.0)
    # rain ponding over the lane: on days with an inch or more, a few hours of shallow water at a random hour
    day = _lst(th).astype("datetime64[D]")
    pond = np.zeros(n)
    for d_, p in zip(prcp_days, prcp):
        if p >= 1.0:
            m = np.where(day == d_)[0]
            if len(m):
                start = m[0] + int(rng.integers(0, max(1, len(m) - 40)))
                dur = int(rng.integers(10, 40))
                k = np.arange(start, min(n, start + dur))
                pond[k] = np.maximum(pond[k], (0.04 + 0.08 * rng.random()) * np.sin(np.pi * (k - start) / dur))
    hod = (th - th.astype("datetime64[D]")) / np.timedelta64(1, "h")
    drift_mm = 3.0 * np.sin(2 * np.pi * (hod - 20) / 24) + np.cumsum(rng.normal(0, 0.02, n))
    base = 3852.0
    dist = base + drift_mm - (depth_ft + pond) * 304.8 + rng.normal(0, 1.6, n)
    spike = rng.random(n) < 0.012
    dist[spike] = rng.uniform(1650, 3600, spike.sum())
    depth_mm = base - dist
    lane_navd88 = s["level"] + W.NAVD88_OF_MLLW
    wet = depth_mm >= 6.0  # the vendor's detection threshold over the dry-road baseline
    wl = np.where(wet, lane_navd88 + depth_mm / 304.8, np.nan)
    # the battery sags over the weeks before each outage and is replaced after it; the device flags weak echoes and
    # its first reading after a restart
    batt = 3.64 + rng.normal(0, 0.004, n)
    status = np.array(["OK"] * n, dtype=object)
    for a_, b_ in W.SENSOR_OUT:
        a_, b_ = np.datetime64(a_), np.datetime64(b_)
        before = (th < a_) & (th >= a_ - np.timedelta64(21, "D"))
        frac = ((th[before] - (a_ - np.timedelta64(21, "D"))) / np.timedelta64(21, "D")).astype(float)
        batt[before] -= 0.42 * frac ** 2
        status[before & (batt < 3.35)] = "BATTERY_LOW"
        after = np.where(th >= b_)[0]
        if len(after):
            status[after[0]] = "RESTART"
    weak = rng.random(n) < 0.0025
    status[weak & (status == "OK")] = "LOW_SIGNAL"
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["timestamp_utc", "device_id", "distance_mm", "water_level_ft_navd88", "battery_v", "status"])
        for tt, dm, v, bv, st in zip(th, dist, wl, batt, status):
            w.writerow([str(tt.astype("datetime64[s]")) + "Z", "PT-FRONT-01", "%d" % round(dm),
                        "" if np.isnan(v) else "%.3f" % v, "%.2f" % bv, st])
    return n


ADDRESSES = {
    "front": ["Front St & Ferry Ln", "FRONT ST / FERRY LN", "100 block Front St", "Front Street at Ferry Lane", "Ferry Ln at Front"],
    "wharf": ["Wharf St", "WHARF ST AT THE SEAWALL", "Wharf Street near Customs House", "300 Wharf St"],
    "marsh": ["Marsh Rd at Pellam Creek", "MARSH RD", "Marsh Road by the creek bridge", "2200 Marsh Rd"],
    "river": ["River Rd, Hensley Landing", "RIVER RD @ HENSLEY LANDING", "River Road boat ramp", "4100 River Rd"],
    "oyster": ["Oyster Creek Rd", "OYSTER CREEK RD AT CULVERT", "Oyster Creek Road"],
}
OTHER = [("Pothole", "pothole in travel lane"), ("Drainage - Clogged Inlet", "storm drain clogged with leaves"),
         ("Mosquito", "standing water in ditch, mosquitoes"), ("Streetlight", "light out on pole"),
         ("Drainage - Clogged Inlet", "inlet grate blocked"), ("Sidewalk", "sidewalk heaved by roots")]


def write_311(path, S, prcp_days, prcp):
    rng = W.rngs(40)
    weight = {"front": 1.0, "wharf": 0.8, "marsh": 0.55, "river": 0.45, "oyster": 0.3}
    rows = []
    for site in W.SITES:
        days, mx, hr = site_daily_max(S, site, "2023-01-01", "2026-11-01")
        lvl = W.SITES[site]["level"]
        for d_, m, h in zip(days, mx, hr):
            if m >= lvl:
                daytime = 7 <= h <= 19
                if rng.random() < (0.42 if daytime else 0.05) * weight[site]:
                    hh = h + rng.uniform(0.2, 2.5) if daytime else rng.uniform(7, 10)
                    rows.append((d_, hh, site, "Flooding - Street", rng.choice(["water over the road at high tide", "street flooded, tide",
                                 "salt water coming up through drain", "road impassable, flooding", "flooding again"])))
    for d_, p in zip(prcp_days, prcp):
        if p >= 1.2 and d_ >= np.datetime64("2023-01-01"):
            for site in W.SITES:
                if rng.random() < 0.25 * weight[site]:
                    rows.append((d_, rng.uniform(8, 20), site, "Flooding - Street", rng.choice(["heavy rain, street flooded", "ponding after storm",
                                 "drain backed up in the rain"])))
    alld = np.arange(np.datetime64("2023-01-01"), np.datetime64("2026-11-01"))
    for d_ in alld[rng.random(len(alld)) < 0.55]:
        site = rng.choice(list(W.SITES))
        cat, desc = OTHER[int(rng.integers(0, len(OTHER)))]
        rows.append((d_, rng.uniform(7, 21), site, cat, desc))
    rows.sort(key=lambda r: (r[0], r[1]))
    from zoneinfo import ZoneInfo
    ny = ZoneInfo("America/New_York")
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["request_id", "created_date", "category", "address", "description", "status", "closed_date"])
        for i, (d_, hh, site, cat, desc) in enumerate(rows):
            base = dt.datetime.combine(d_.astype(dt.date), dt.time(0, 0)) + dt.timedelta(hours=float(hh))
            local = (base + dt.timedelta(hours=5)).replace(tzinfo=dt.timezone.utc).astimezone(ny)
            closed = local + dt.timedelta(days=float(rng.uniform(0.2, 9)))
            st = "Closed" if closed.date() < dt.date(2026, 11, 1) else "Open"
            addr = ADDRESSES[site][int(rng.integers(0, len(ADDRESSES[site])))]
            w.writerow(["SR-%07d" % (2300000 + i * 7 + int(rng.integers(0, 7))), local.strftime("%m/%d/%Y %I:%M %p"), cat, addr, desc,
                        st, closed.strftime("%m/%d/%Y %I:%M %p") if st == "Closed" else ""])
    return len(rows)


def write_slr(path):
    yrs = [2020, 2030, 2040, 2050, 2060, 2070, 2080, 2090, 2100]
    sc = {"Low": 0.95, "Intermediate-Low": 1.25, "Intermediate": 1.9, "Intermediate-High": 2.9, "High": 3.8}
    with open(path, "w", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(["Site", "Scenario", "Year", "RSL_ft_rel_2000", "Low_CI_ft", "High_CI_ft"])
        for name, end in sc.items():
            for y in yrs:
                x = (y - 2000) / 100.0
                v = 0.012 * (y - 2000) * 0.95 + (end - 1.14) * x ** 2 * 1.0 + 0.0
                v = max(v, 0.0)
                w.writerow([STATION_NAME, name, y, "%.2f" % v, "%.2f" % (v * 0.8), "%.2f" % (v * 1.22)])
    return 5 * len(yrs)
