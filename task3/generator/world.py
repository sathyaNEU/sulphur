"""task3: the hydrometeorological world behind the pack, simulated hour by hour from water year 1950 to 2025.

A western Washington Cascade setting: Pacific storms arrive with a snow line (the elevation where the air is at the
rain-snow temperature) and an orographic gain; each 250-ft elevation band rains below the snow line and snows above
it; a degree-hour snowpack with rain-on-snow melt per band; an HBV soil and response routine per basin and band; a
triangular routing of each basin's runoff to its outlet. Every basin sees the same storms and the same band climate;
the basins differ in their elevation bands, their size and their routing. Valley, ridge and SNOTEL stations read the
same weather at their own elevations, with the noise a station adds.
"""
import datetime as dt
import math

import numpy as np

SEED = 3069
T0 = dt.datetime(1949, 10, 1)          # one spin-up water year before the record starts
T1 = dt.datetime(2025, 10, 1)
NH = int((T1 - T0).total_seconds() // 3600)
FT_PER_KM = 3280.84

# elevation bands, 250 ft, centres 375 ... 9,875 ft
Z = np.arange(375.0, 10000.0, 250.0)
NB = len(Z)

T_RS = 1.0          # the rain-snow temperature, deg C: half the precipitation falls as rain
T_HALF = 0.7        # the rain fraction ramps from 0 to 1 over T_RS +/- T_HALF
Z_VALLEY = 1180.0   # Tessel's valley station, the storm temperature reference


def band_areas(area, zmin, zmax, a, b):
    """Area (square miles) by elevation band for a basin spanning zmin..zmax, mass shaped by a beta(a, b)."""
    edges = np.arange(250.0, 10001.0, 250.0)
    from scipy.stats import beta as B
    lo = np.clip((edges[:-1] - zmin) / (zmax - zmin), 0, 1)
    hi = np.clip((edges[1:] - zmin) / (zmax - zmin), 0, 1)
    w = B.cdf(hi, a, b) - B.cdf(lo, a, b)
    return area * w / w.sum()


# The basins: name, area (sq mi), min and max elevation (ft), beta shape, routing base (hours), whether gauged.
BASINS = [
    dict(key="coyner", area=86.4, zmin=1640, zmax=10380, a=1.55, b=1.25, maxbas=13, fc=240.0),
    dict(key="durrow", area=85.3, zmin=610, zmax=4380, a=1.45, b=2.9, maxbas=13, fc=240.0),
    dict(key="tarrow", pmult=0.926, area=142.0, zmin=1880, zmax=10140, a=1.70, b=1.35, maxbas=17, fc=240.0),
    dict(key="gorham", pmult=0.890, area=38.6, zmin=2610, zmax=9190, a=1.45, b=1.30, maxbas=9, fc=240.0),
    dict(key="quillen", pmult=0.929, area=211.5, zmin=1490, zmax=10420, a=1.80, b=1.30, maxbas=20, fc=240.0),
    dict(key="pinnell", pmult=0.888, area=64.2, zmin=2230, zmax=9580, a=1.50, b=1.40, maxbas=12, fc=240.0),
]
# Twelve more gauged basins of the state's Region 3, never shipped: the state's regional equations are fitted on
# them with the four regional gauges and the Coyner River.
_RB = [(24.8, 2650, 8350, 1.6, 1.3), (47.1, 2120, 9100, 1.7, 1.3), (73.9, 1780, 8600, 1.6, 1.4),
       (112.0, 2300, 10300, 1.8, 1.4), (156.0, 1900, 9700, 1.7, 1.3), (233.0, 1660, 10400, 1.9, 1.4),
       (318.0, 1560, 10200, 2.0, 1.5), (29.6, 3200, 8900, 1.5, 1.3), (58.3, 2500, 8900, 1.5, 1.4),
       (88.8, 2060, 9200, 1.5, 1.4), (134.0, 1740, 9400, 1.6, 1.4), (402.0, 1500, 10400, 2.1, 1.5)]
_PM = [1.32, 0.86, 1.18, 0.94, 1.41, 1.05, 0.81, 1.24, 1.12, 0.90, 1.36, 0.98]   # their precipitation, against Tessel's climate
_FC = [205.0, 310.0, 170.0, 265.0, 330.0, 190.0, 280.0, 160.0, 300.0, 220.0, 255.0, 345.0]   # soil storage, mm
_MB = [0.75, 1.30, 0.85, 1.20, 1.00, 0.70, 1.35, 0.90, 1.15, 0.80, 1.25, 1.05]   # routing, against the area rule
REGRESSION = [dict(key="r%02d" % (i + 1), area=a, zmin=z0, zmax=z1, a=aa, b=bb, pmult=_PM[i],
                   maxbas=int(round((7 + 2.2 * a ** 0.35) * _MB[i])), fc=_FC[i]) for i, (a, z0, z1, aa, bb) in enumerate(_RB)]
# a foothill basin of the county with a short record (a crest-stage gauge from water year 2012), never in the state study
SELBY = dict(key="selby", area=62.0, zmin=420, zmax=3900, a=1.40, b=2.6, maxbas=10, fc=240.0)
for _b in BASINS + REGRESSION + [SELBY]:
    _b["bands"] = band_areas(_b["area"], _b["zmin"], _b["zmax"], _b["a"], _b["b"])

# Stations: key, elevation (ft), first water year of record.
STATIONS = {
    "tessel": dict(z=1180.0, first=1950),
    "tessel_new": dict(z=1340.0, first=1988),
    "durrow_ridge": dict(z=2710.0, first=1950),
    "hatchet": dict(z=4160.0, first=1981),
    "corbel": dict(z=5630.0, first=1983),
}


def oro(z, gain):
    """Precipitation at z relative to 1,000 ft: rises by `gain` a thousand feet to 6,000 ft, then slowly."""
    low = 1.0 + gain * (np.minimum(z, 5500.0) - 1000.0) / 1000.0
    return low + 0.15 * gain * np.maximum(z - 5500.0, 0.0) / 1000.0


def seasonal_t(doy):
    """Valley daily mean temperature climatology (deg C), coldest about 10 January."""
    return 10.2 - 7.4 * np.cos(2 * np.pi * (doy - 10.0) / 365.25)


AR_SHARE = {10: 0.22, 11: 0.30, 12: 0.26, 1: 0.24, 2: 0.18, 3: 0.12, 4: 0.06, 5: 0.02}
AR_MEDIAN, AR_SIGMA, AR_SNOWLINE = 3.6, 0.45, 6150.0
ORD_MEDIAN, ORD_SIGMA, ORD_SNOWLINE = 1.45, 0.55, 3700.0


def storm_rate(month):
    return {10: 2.4, 11: 4.6, 12: 4.8, 1: 4.5, 2: 3.6, 3: 3.4, 4: 2.2, 5: 1.1, 6: 0.6, 7: 0.3, 8: 0.4, 9: 1.1}[month]


class World:
    pass


def weather(rng):
    """Hourly reference precipitation (inches an hour at 1,000 ft), valley temperature (deg C), the storm lapse rate
    and orographic gain by hour, and the storm table."""
    hours = np.arange(NH)
    t = np.array([T0 + dt.timedelta(hours=int(h)) for h in range(0, NH, 24)])
    doy_day = np.array([d.timetuple().tm_yday for d in t])
    nday = len(t)
    # synoptic temperature anomaly, daily AR(1)
    anom = np.zeros(nday)
    e = rng.normal(0, 1, nday)
    for i in range(1, nday):
        anom[i] = 0.72 * anom[i - 1] + 1.9 * e[i]
    tmean_day = seasonal_t(doy_day) + anom
    hod = hours % 24
    day_of_hour = hours // 24
    tv = tmean_day[day_of_hour] + 4.3 * np.sin(2 * np.pi * (hod - 9) / 24.0)
    lapse = np.full(NH, 5.8)            # dry-weather lapse, deg C per km
    gain = np.full(NH, 0.13)
    p = np.zeros(NH)
    storms = []
    # showers between storms: light, in the wet season
    month_day = np.array([d.month for d in t])
    wetseason = np.isin(month_day, [10, 11, 12, 1, 2, 3, 4, 5])
    shower = (rng.random(nday) < np.where(wetseason, 0.28, 0.05)) & True
    amt = rng.gamma(1.2, 0.07, nday) * shower
    for i in np.nonzero(shower)[0]:
        h0 = i * 24 + rng.integers(0, 18)
        ln = rng.integers(3, 9)
        p[h0:h0 + ln] += amt[i] / ln
    # storms, a Poisson process with a monthly rate
    # a non-homogeneous Poisson process by thinning: candidate arrivals at the peak monthly rate, each kept with
    # the ratio of its month's rate to the peak
    peak_rate = max(storm_rate(m) for m in range(1, 13)) / (30.4 * 24.0)
    h = 0
    while h < NH - 200:
        h = int(h + max(rng.exponential(1.0 / peak_rate), 54))
        if h >= NH - 200:
            break
        d = T0 + dt.timedelta(hours=int(h))
        if rng.random() > storm_rate(d.month) / (30.4 * 24.0) / peak_rate:
            continue
        season = {10: 700, 11: 300, 12: -150, 1: -200, 2: -100, 3: -150, 4: 150, 5: 600, 6: 1300, 7: 1900, 8: 1900,
                  9: 1300}[d.month]
        ar = rng.random() < AR_SHARE.get(d.month, 0.0)
        z1, z2, z3 = rng.multivariate_normal([0, 0, 0], [[1, 0.15, 0.25], [0.15, 1, 0.0], [0.25, 0.0, 1]])
        if ar:
            # an atmospheric river: subtropical moisture, a high snow line, long and wet
            dur = int(np.clip(np.exp(np.log(40.0) + 0.40 * z3), 18, 120))
            total = float(np.exp(np.log(AR_MEDIAN) + AR_SIGMA * z1))
            sl_mid = float(np.clip(AR_SNOWLINE + 0.4 * season + 850.0 * z2, 4300.0, 8300.0))
        else:
            dur = int(np.clip(np.exp(np.log(26.0) + 0.45 * z3), 8, 96))
            total = float(np.exp(np.log(ORD_MEDIAN) + ORD_SIGMA * z1))
            sl_mid = float(np.clip(ORD_SNOWLINE + season + 1000.0 * z2, 300.0, 7600.0))
        swing = rng.normal(0, 200.0)
        lap = float(np.clip(rng.normal(5.2, 0.22), 4.6, 5.9))
        g = float(0.10 * np.exp(rng.normal(0, 0.22)))
        # hourly envelope: a gamma-shaped pulse with embedded bursts
        x = np.linspace(0.02, 1.0, dur)
        k = rng.uniform(1.6, 3.2)
        env = x ** (k - 1) * np.exp(-x * (k - 1) / rng.uniform(0.3, 0.6))
        env *= np.exp(rng.normal(0, 0.45, dur))
        env /= env.sum()
        ph = total * env
        hh = slice(h, h + dur)
        p[hh] += ph
        # the storm's air mass: it arrives with the rain and lingers a little after it, under a damped diurnal cycle
        pre, post = 10, 14
        a0, a1 = max(h - pre, 0), min(h + dur + post, NH)
        span = a1 - a0
        sl_track = sl_mid + swing * np.linspace(-1, 1, span) + rng.normal(0, 120.0, span)
        t_storm = T_RS + lap * (sl_track - Z_VALLEY) / FT_PER_KM + 1.0 * np.sin(2 * np.pi * ((np.arange(a0, a1) % 24) - 9) / 24.0)
        edge = np.ones(span)
        ramp = 6
        edge[:ramp] = np.linspace(0.2, 1.0, ramp)
        edge[-ramp:] = np.linspace(1.0, 0.2, ramp)
        tv[a0:a1] = edge * t_storm + (1 - edge) * tv[a0:a1]
        lapse[a0:a1] = edge * lap + (1 - edge) * lapse[a0:a1]
        gain[hh] = g
        storms.append(dict(start=h, dur=dur, total=total, snowline=sl_mid, lapse=lap, gain=g, month=d.month, ar=bool(ar)))
        h += dur
    return dict(p=p, tv=tv, lapse=lapse, gain=gain, storms=storms, days=t)


def simulate(seed=SEED, basins=None):
    basins = BASINS + REGRESSION + [SELBY] if basins is None else basins
    rng = np.random.default_rng(seed)
    w = weather(rng)
    p, tv, lapse, gain = w["p"], w["tv"], w["lapse"], w["gain"]
    nbas = len(basins)
    frac = np.array([b["bands"] / b["area"] for b in basins])          # (basins, bands)
    fc = np.array([b["fc"] for b in basins])[:, None]
    pm = np.array([b.get("pmult", 1.0) for b in basins])[:, None]
    BETA, LP, UZL, K0, K1, K2, PERC = 2.3, 0.72, 22.0, 0.11, 0.018, 0.0016, 0.07
    swe = np.zeros(NB)                     # mm, by band (shared)
    liq = np.zeros(NB)
    sm = np.full((nbas, NB), 150.0)
    uz = np.zeros(nbas)
    lz = np.full(nbas, 60.0)
    qgen = np.zeros((nbas, NH))
    swe_day = np.zeros((NH // 24 + 1, NB))
    hod = np.arange(NH) % 24
    doy = np.array([(T0 + dt.timedelta(hours=int(i))).timetuple().tm_yday for i in range(0, NH, 24)])
    ddf_day = 1.4 + 1.3 * (1 + np.sin(2 * np.pi * (doy - 80) / 365.25)) / 2           # mm per deg C per day
    pet_day = np.maximum(0.0, 3.6 * np.sin(2 * np.pi * (doy - 95) / 365.25))         # mm per day
    zkm = (Z - Z_VALLEY) / FT_PER_KM
    for i in range(NH):
        d = i // 24
        t = tv[i] - lapse[i] * zkm
        pb = p[i] * 25.4 * oro(Z, gain[i])                           # mm this hour by band
        fr = np.clip((t - T_RS + T_HALF) / (2 * T_HALF), 0.0, 1.0)
        rain = pb * fr
        snow = pb - rain
        swe += snow
        melt = np.where(t > 0, np.where(rain > 0.2, 0.0126 * rain * t + 0.035 * t, ddf_day[d] / 24.0 * t), 0.0)
        melt = np.minimum(melt, swe)
        swe -= melt
        has = swe > 0
        hold = 0.05 * swe
        liq_in = np.where(has, rain + melt, 0.0)
        liq += liq_in
        out = np.maximum(liq - hold, 0.0)
        liq -= out
        win = np.where(has, out, rain + melt)
        liq = np.where(swe <= 0, 0.0, liq)
        # soil, per basin and band
        wb = win[None, :] * pm
        rch = wb * np.minimum(sm / fc, 1.0) ** BETA
        sm += wb - rch
        sm = np.minimum(sm, fc)
        if 7 <= hod[i] <= 18:
            et = pet_day[d] / 12.0 * np.minimum(sm / (LP * fc), 1.0) * (p[i] < 0.01)
            sm = np.maximum(sm - et, 0.0)
        r = (rch * frac).sum(axis=1)
        uz += r
        perc = np.minimum(PERC, uz)
        uz -= perc
        lz += perc
        q0 = K0 * np.maximum(uz - UZL, 0.0)
        q1 = K1 * uz
        uz -= q0 + q1
        q2 = K2 * lz
        lz -= q2
        qgen[:, i] = q0 + q1 + q2
        if hod[i] == 23:
            swe_day[d] = swe
    flows = np.zeros((nbas, NH))
    for k, b in enumerate(basins):
        m = b["maxbas"]
        tri = np.concatenate([np.arange(1, m // 2 + 2), np.arange(m - m // 2 - 1, 0, -1)]).astype(float)
        tri /= tri.sum()
        q = np.convolve(qgen[k], tri)[:NH]
        flows[k] = q * b["area"] * 25.41                                 # cfs
    W = World()
    W.weather = w
    W.flows = flows
    W.swe_day = swe_day
    W.basins = basins
    W.seed = seed
    return W


def water_year(i_hour):
    d = T0 + dt.timedelta(hours=int(i_hour))
    return d.year + (1 if d.month >= 10 else 0)


def annual_peaks(W, k):
    """Water year -> (instantaneous peak cfs, hour index), water years 1951 to 2025 (1950 is spin-up)."""
    q = W.flows[k]
    out = {}
    wy_start = [int((dt.datetime(y - 1, 10, 1) - T0).total_seconds() // 3600) for y in range(1950, 2027)]
    for j, y in enumerate(range(1950, 2026)):
        a, b = wy_start[j], wy_start[j + 1]
        i = a + int(np.argmax(q[a:b]))
        out[y] = (float(q[i]), i)
    return out
