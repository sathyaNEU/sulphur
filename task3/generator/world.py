"""task3: Port Tolliver's harbor, river and tidal low points, simulated.

The harbor gauge's water level is the astronomical tide (real lunar and solar arguments, nodal factors) plus the
station's mean sea level (a secular rise with a slow ocean-dynamic anomaly and a fast monthly one, and a faint river
lift), plus the weather's surge (a background random walk, nor'easters from October to April, tropical systems from
August to October), with the tide delayed under a positive surge so hourly residuals swing through the tide while the
high waters keep the surge. The river's discharge is a seasonal log-normal process. Each low point's water level is
the harbor's, carried by its own physics: Front Street and Wharf Street sit on the harbor; Marsh Road and Oyster Creek
Road are on marsh creeks whose high water rises ever more slowly once the tide tops the marsh platform; River Road
rides on the river's flow. Units: feet above the gauge's MLLW (1983-2001), times UT unless named.
"""
import numpy as np
from scipy.signal import lfilter

import tides as T

SEED = 3070
T0 = np.datetime64("1955-01-01T00:00")
T1 = np.datetime64("2028-05-01T06:00")
LAST_DATA = np.datetime64("2026-11-01T05:00")  # 2026-11-01 00:00 local standard time
NAVD88_OF_MLLW = -3.42  # MLLW lies 3.42 ft below NAVD88 at the gauge

AMP = {"M2": 3.05, "S2": 0.52, "N2": 0.70, "K2": 0.15, "2N2": 0.09, "NU2": 0.14, "MU2": 0.07, "L2": 0.10,
       "T2": 0.03, "K1": 0.36, "O1": 0.27, "P1": 0.12, "Q1": 0.05, "M4": 0.10, "MS4": 0.06, "MN4": 0.04,
       "M6": 0.04, "SA": 0.24, "SSA": 0.07}
PHA = {"M2": 200, "S2": 225, "N2": 180, "K2": 222, "2N2": 160, "NU2": 185, "MU2": 190, "L2": 215, "T2": 225,
       "K1": 110, "O1": 115, "P1": 108, "Q1": 112, "M4": 30, "MS4": 80, "MN4": 10, "M6": 120, "SA": 193, "SSA": 26}

# low points: kind, flooding level (harbor MLLW-equivalent feet at the site), transfer parameters, lag (minutes)
SITES = {
    "front": dict(name="Front Street at Ferry Lane", kind="harbor", level=8.60, lag=8, rim_below=0.33),
    "marsh": dict(name="Marsh Road at Pellam Creek", kind="marsh", level=8.42, lag=25,
                  k1=1.07, k2=0.55, P=7.45, w=0.30),
    "river": dict(name="River Road at Hensley Landing", kind="river", level=8.37, lag=75, r=0.86, a_s=0.30),
    "wharf": dict(name="Wharf Street at Market Lane", kind="harbor", level=8.555, lag=5),
    "oyster": dict(name="Oyster Creek Road", kind="marsh", level=8.45, lag=20, k1=1.03, k2=0.58, P=7.25, w=0.30),
}
CAMPAIGNS = {  # local logger windows (the logger's own fixed offset from UT, hours)
    "marsh": ("2024-09-15T11:00", "2024-11-21T10:00", -4),
    "oyster": ("2025-08-25T10:00", "2025-10-30T15:00", -4),
    "river": ("2025-01-20T12:00", "2025-04-20T09:00", -5),
}
SENSOR = ("2024-05-14T00:00", "2026-11-01T05:00")  # Front Street street sensor, UT
SENSOR_OUT = [("2025-07-19T03:00", "2025-07-22T15:00"), ("2025-09-28T21:00", "2025-10-24T16:00")]
GAUGE_OUT = [("1979-09-03T00:00", "1979-09-11T00:00"), ("1989-09-21T00:00", "1989-09-25T12:00"),
             ("2004-08-29T00:00", "2004-09-02T00:00"), ("2016-10-07T06:00", "2016-10-09T18:00"),
             ("2022-11-14T00:00", "2022-11-15T12:00")]


def rngs(k):
    return np.random.default_rng([SEED, k])


def decyear(t):
    t = t.astype("datetime64[s]")
    y = t.astype("datetime64[Y]").astype(int) + 1970
    a = (y - 1970).astype("datetime64[Y]").astype("datetime64[s]")
    b = (y - 1969).astype("datetime64[Y]").astype("datetime64[s]")
    return y + (t - a) / (b - a)


def msl_monthly(months):
    rng = np.random.default_rng([SEED, 1, 455])
    n = len(months)
    dy = decyear(months.astype("datetime64[D]") + np.timedelta64(14, "D"))
    rate0, acc = 0.0095, 0.00035
    sec = rate0 * (dy - 1992.0) + np.where(dy > 1995, 0.5 * acc * (dy - 1995) ** 2, 0.0)
    phi_s, sd_s, phi_f, sd_f = 0.963, 0.11, 0.45, 0.07
    es = rng.normal(0, sd_s * np.sqrt(1 - phi_s ** 2), n)
    ef = rng.normal(0, sd_f * np.sqrt(1 - phi_f ** 2), n)
    slow = np.zeros(n)
    fast = np.zeros(n)
    slow[0] = rng.normal(0, sd_s)
    fast[0] = rng.normal(0, sd_f)
    for i in range(1, n):
        slow[i] = phi_s * slow[i - 1] + es[i]
        fast[i] = phi_f * fast[i - 1] + ef[i]
    return sec, slow, fast


def river_daily(days):
    rng = rngs(4)
    nd = len(days)
    doy = (days - days.astype("datetime64[Y]")) / np.timedelta64(1, "D")
    yi = days.astype("datetime64[Y]").astype(int) + 1970 - 1955
    yr = rng.normal(0, 0.35, 90)
    ar = lfilter([1.0], [1.0, -0.985], rng.normal(0, 0.55 * np.sqrt(1 - 0.985 ** 2), nd))
    storms = np.zeros(nd)
    for i in np.where(rng.random(nd) < 0.018)[0]:  # rain events: a sharp rise and a two-week recession
        k = np.arange(i, min(nd, i + 40))
        storms[k] += rng.gamma(2.0, 0.25) * np.exp(-(k - i) / 6.0)
    lnQ = np.log(11000.0) + 0.70 * np.cos(2 * np.pi * (doy - 50) / 365.25) + yr[yi] + ar + storms
    return np.exp(lnQ)


def surge_hourly(t):
    rng = rngs(2)
    n = len(t)
    th = (t - t[0]) / np.timedelta64(1, "h")
    doy = (t - t.astype("datetime64[Y]")) / np.timedelta64(1, "D")
    phi = np.exp(-1.0 / 36.0)
    sd = 0.15 + 0.05 * np.cos(2 * np.pi * (doy - 15) / 365.25)
    bg = lfilter([1.0], [1.0, -phi], rng.normal(0, 1, n) * sd * np.sqrt(1 - phi ** 2))
    ev = np.zeros(n)
    for y in range(1955, 2029):
        for _ in range(rng.poisson(6.0)):
            mo = rng.choice([10, 11, 12, 1, 2, 3, 4], p=[0.12, 0.17, 0.17, 0.16, 0.15, 0.14, 0.09])
            yy = y if mo >= 10 else y + 1
            c = (np.datetime64("%04d-%02d-01T00:00" % (yy, mo)) - t[0]) / np.timedelta64(1, "h") + rng.uniform(0, 672)
            dur = rng.uniform(30, 72)
            a = rng.gamma(2.0, 0.33)
            i0, i1 = int(c), int(c + dur) + 1
            if 0 <= i0 and i1 < n:
                ev[i0:i1] += a * np.sin(np.pi * (th[i0:i1] - c) / dur) ** 2
        for _ in range(rng.poisson(0.3)):
            mo = rng.choice([8, 9, 10], p=[0.3, 0.5, 0.2])
            c = (np.datetime64("%04d-%02d-01T00:00" % (y, mo)) - t[0]) / np.timedelta64(1, "h") + rng.uniform(0, 672)
            dur = rng.uniform(18, 30)
            a = rng.gamma(2.0, 0.8)
            i0, i1 = int(c), int(c + dur) + 1
            if 0 <= i0 and i1 < n:
                ev[i0:i1] += a * np.sin(np.pi * (th[i0:i1] - c) / dur) ** 2
    return bg + ev


def running_mean(x, k):
    c = np.convolve(x, np.ones(k) / k, mode="same")
    return c


def simulate():
    """The harbor at 6 minutes, the river by day, and everything the pack writers need."""
    th6 = np.arange(T0, T1, np.timedelta64(6, "m"))
    th1 = th6[::10]
    months = np.arange(np.datetime64("1955-01"), np.datetime64("2028-06"))
    sec, slow, fast = msl_monthly(months)
    days = np.arange(np.datetime64("1955-01-01"), np.datetime64("2028-05-02"))
    Q = river_daily(days)
    # faint river lift at the harbor, by month
    qm = np.array([Q[(days >= m.astype("datetime64[D]")) & (days < (m + 1).astype("datetime64[D]"))].mean() for m in months])
    lift = 0.012 * (qm / 1e4 - 1.1)
    mid = ((months.astype("datetime64[D]") + np.timedelta64(14, "D")).astype("datetime64[h]") - th1[0]) / np.timedelta64(1, "h")
    hrs1 = (th1 - th1[0]) / np.timedelta64(1, "h")
    msl1 = np.interp(hrs1, mid, sec + slow + fast + lift)
    surge1 = surge_hourly(th1)
    hrs6 = (th6 - th6[0]) / np.timedelta64(1, "h")
    msl6 = np.interp(hrs6, hrs1, msl1)
    surge6 = np.interp(hrs6, hrs1, surge1)
    delta = np.clip(0.12 * surge6, -0.25, 0.5)
    pred6 = T.tide(th6, AMP, PHA)
    obs6 = T.tide(th6 - (delta * 3600).astype("timedelta64[s]"), AMP, PHA) + msl6 + surge6
    obs6 = obs6 + rngs(3).normal(0, 0.02, len(th6))
    # datum: MLLW = the mean of daily lower low waters (local standard time) over 1983-2001
    lst = th6 - np.timedelta64(5, "h")
    day = lst.astype("datetime64[D]")
    ep = (day >= np.datetime64("1983-01-01")) & (day < np.datetime64("2002-01-01"))
    d_ep = day[ep]
    o_ep = obs6[ep]
    brk = np.r_[0, np.where(np.diff(d_ep.astype(np.int64)) != 0)[0] + 1, len(d_ep)]
    lows = np.minimum.reduceat(o_ep, brk[:-1])
    mllw_raw = lows.mean()
    msl_raw = o_ep.mean()
    obs6 = obs6 - mllw_raw
    z0 = msl_raw - mllw_raw - msl6[ep].mean()  # predictions sit on the epoch's mean sea level
    pred6 = pred6 + z0 + msl6[ep].mean()
    return dict(th6=th6, obs6=obs6, pred6=pred6, msl6=msl6 - msl6[ep].mean(), surge6=surge6, days=days, Q=Q,
                months=months, z0=z0 + msl6[ep].mean(), lst6=lst)


def low_frequency(th6, obs6, hours=720):
    """The harbor's 30-day running mean level at 6 minutes (what a creek's mean level follows)."""
    k = int(hours * 10)
    return running_mean(obs6, k)


def softplus(x):
    return np.logaddexp(0.0, x)


def site_level(site, H, M, Q):
    """A low point's water level from the harbor's (lagged) level H, the harbor's low-frequency level M and the
    river's flow Q."""
    s = SITES[site]
    if s["kind"] == "harbor":
        return H
    if s["kind"] == "marsh":
        return M + s["k1"] * (H - M) - (s["k1"] - s["k2"]) * s["w"] * softplus((H - s["P"]) / s["w"])
    if s["kind"] == "river":
        setup = s["a_s"] * ((np.maximum(Q, 500.0) / 1e4) ** 0.85 - 0.5 ** 0.85)
        return M + setup + s["r"] * (H - M)
    raise ValueError(site)
