"""task3 architecture 4: the clean truth. Parcels in the Sallow Road wellhead protection area and under the county's
network wells, each with its land cover by year, depth to water and travel times; nitrate leached at the land surface,
carried through the unsaturated sand to the water table, then through the aquifer to the wells; the wells' pumping;
the entry point's blend. Everything here is the world; nothing here is what an analyst can see."""
import math

import numpy as np

import params as P

T0, T1, DT = 1940.0, 2041.0, 0.05
TG = np.round(np.arange(T0, T1 + 1e-9, DT), 4)     # the time grid (decimal years)
NT = len(TG)


def idx(t):
    return int(round((t - T0) / DT))


# ---------------------------------------------------------------- weather
def weather(rng):
    """county-wide wet and dry years: a leaching factor and a recharge factor per land-surface year"""
    yrs = np.arange(1940, 2042)
    lf = np.clip(rng.normal(1.0, 0.065, len(yrs)), 0.85, 1.18)
    rf = np.clip(1.0 + 0.8 * (lf - 1.0) + rng.normal(0, 0.03, len(yrs)), 0.82, 1.2)
    for y in range(2027, 2042):          # the forecast years carry no weather
        lf[y - 1940] = rf[y - 1940] = 1.0
    return {int(y): (float(a), float(b)) for y, a, b in zip(yrs, lf, rf)}


# ---------------------------------------------------------------- parcels
def _hist(c0, changes=()):
    """land cover by year 1940..2040 from a starting class and (year, class) changes"""
    h, cur = {}, c0
    ch = dict(changes)
    for y in range(1940, 2041):
        if y in ch:
            cur = ch[y]
        h[y] = cur
    return h


def whpa_parcels(rng):
    out = []

    def plain(zone, n_near, n_far, dtw, mix, tnear=(0.5, 4.2), tfar=(5.5, 11.0)):
        classes = []
        for c, k in mix.items():
            classes += [c] * k
        rng.shuffle(classes)
        for i, c in enumerate(classes):
            far = i >= n_near
            out.append(dict(zone=zone, kind="plain",
                            acres=float(np.round(rng.uniform(14, 34) if far else rng.uniform(26, 80), 1)),
                            dtw=float(np.round(rng.uniform(*dtw), 0)),
                            T=float(np.round(rng.uniform(*(tfar if far else tnear)), 1)),
                            hist=_hist(c), theta=float(rng.normal(P.THETA, P.THETA_SD)),
                            mult=float(math.exp(rng.normal(0, 0.03)))))
    plain("W3", 11, 3, (6, 17), {"FOR": 6, "GRS": 2, "DRY": 2, "IRC": 2, "RES": 2})
    plain("W5", 12, 4, (8, 24), {"FOR": 5, "GRS": 1, "DRY": 3, "IRC": 4, "IRV": 1, "RES": 2})
    plain("W6", 10, 3, (8, 24), {"FOR": 2, "GRS": 1, "DRY": 3, "IRC": 4, "IRV": 2, "RES": 1})
    plain("W7", 9, 3, (9, 25), {"FOR": 2, "GRS": 1, "DRY": 2, "IRC": 4, "IRV": 2, "RES": 1})
    # the Sallow Ridge timber tract, cleared for irrigated vegetables 2016-2020 in ten parcels, and the city's own
    # ridge woodland (two parcels, left in forest)
    ridge = [("W6", 2017, 94, 1.7, 106),
             ("W6", 2018, 84, 2.0, 93),
             ("W6", 2019, 80, 1.5, 111),
             ("W6", 2019, 72, 2.6, 80),
             ("W6", 2020, 71, 1.7, 100),
             ("W7", 2018, 88, 1.5, 125),
             ("W7", 2019, 76, 2.1, 136),
             ("W7", 2020, 68, 2.1, 108),
             ("W7", 2021, 66, 1.4, 144),
             ("W7", 2021, 57, 2.6, 96)]
    for zone, yr, dtw, T, ac in ridge:
        out.append(dict(zone=zone, kind="ridge", acres=float(ac), dtw=float(dtw), T=float(T),
                        hist=_hist("FOR", [(yr, "IRV")]), theta=float(rng.normal(P.THETA, P.THETA_SD * 0.6)),
                        mult=float(math.exp(rng.normal(0, 0.03))), cleared=yr))
    for zone, dtw, T, ac in [("W6", 78, 0.9, 64), ("W5", 71, 1.5, 58)]:
        out.append(dict(zone=zone, kind="ridge_woods", acres=float(ac), dtw=float(dtw), T=float(T),
                        hist=_hist("FOR"), theta=P.THETA, mult=1.0))
    return out


def network_sites(rng):
    """the county's 72 water-table monitoring wells, each on its own parcel"""
    out = []

    def site(c0, changes, dtw, kind):
        out.append(dict(kind=kind, dtw=float(dtw), hist=_hist(c0, changes),
                        theta=float(rng.normal(P.THETA, P.THETA_SD)), mult=float(math.exp(rng.normal(0, 0.10))),
                        age=float(np.round(rng.uniform(0.1, 0.45), 2))))
    steady = {"FOR": 12, "GRS": 5, "DRY": 7, "IRC": 13, "IRV": 10, "RES": 4}
    for c, k in steady.items():
        for _ in range(k):
            site(c, (), np.round(rng.uniform(8, 52), 0), "steady")
    # the matured conversions: pasture, dry cropland or grass put under pivots between 1988 and 2009
    mat_dtw = [11, 14, 17, 19, 22, 25, 28, 31, 34, 38, 43, 49, 57, 68, 82]
    mat_yr = [1993, 1989, 2001, 1996, 2006, 1991, 1999, 2004, 1994, 2008, 1990, 2002, 1997, 1992, 1998]
    froms = ["DRY", "GRS", "DRY", "DRY", "GRS", "DRY", "FOR", "DRY", "GRS", "DRY", "FOR", "DRY", "GRS", "FOR", "FOR"]
    tos = ["IRC", "IRV", "IRC", "IRV", "IRC", "IRC", "IRV", "IRC", "IRC", "IRV", "IRC", "IRV", "IRC", "IRV", "IRC"]
    for d, y, f, t in zip(mat_dtw, mat_yr, froms, tos):
        site(f, [(y, t)], d, "converted")
    # irrigated land enrolled in the conservation reserve
    for d, y, f in [(16, 1991, "IRC"), (29, 1996, "IRV"), (47, 2003, "IRC")]:
        site(f, [(y, "GRS")], d, "retired")
    # the recent clearings on timbered upland
    for d, y in [(90, 2017), (79, 2018), (69, 2020)]:
        site("FOR", [(y, "IRV")], d, "recent")
    order = rng.permutation(len(out))
    return [out[i] for i in order]


# ---------------------------------------------------------------- transport
def surface_series(p, wx):
    """land-surface leachate concentration and recharge on the grid"""
    yrs = np.floor(TG).astype(int)
    conc = np.empty(NT)
    q = np.empty(NT)
    U = np.empty(NT)
    for i, (t, y) in enumerate(zip(TG, yrs)):
        y = int(min(max(y, 1940), 2040))
        c = p["hist"][y]
        lf, rf = wx[y]
        conc[i] = P.leach(c, t) * p["mult"] * lf if c != "FOR" else P.leach(c, t) * lf
        q[i] = P.RECHARGE[c] * rf
        U[i] = P.vadose_years(p["dtw"], c, p["theta"])
    return conc, q, U


def water_table(p, wx):
    """concentration and flux of the water reaching the water table under the parcel, on the grid. The water moves
    down as a piston on the cumulative recharge clock: water leaving the root zone at s reaches the water table when
    the recharge since s has filled the sand's held water above it (theta times the depth to water)."""
    conc, q, _ = surface_series(p, wx)
    Q = np.concatenate([[0.0], np.cumsum(q[:-1] / 12.0 * DT)])     # feet of recharge since T0
    store = p["theta"] * p["dtw"]
    arr = np.interp(Q + store, Q, TG, right=np.inf)
    num = np.zeros(NT)
    den = np.zeros(NT)
    for i in range(NT):
        if not np.isfinite(arr[i]):
            continue
        tt = arr[i] - TG[i]
        sig = max(P.VADOSE_SPREAD * tt, 0.12)
        mu = arr[i]
        lo, hi = idx(max(mu - 4 * sig, T0)), idx(min(mu + 4 * sig, T1))
        if lo > hi:
            continue
        r = TG[lo:hi + 1]
        w = np.exp(-0.5 * ((r - mu) / sig) ** 2) / (sig * math.sqrt(2 * math.pi)) * DT
        num[lo:hi + 1] += w * q[i] * conc[i]
        den[lo:hi + 1] += w * q[i]
    c_wt = np.where(den > 0, num / np.maximum(den, 1e-12), 0.0)
    return c_wt, den


GH_Z, GH_W = np.polynomial.hermite_e.hermegauss(7)
GH_W = GH_W / GH_W.sum()


def to_well(c_wt, fl, T):
    """water from one parcel arriving at the well: the water-table series lagged by the aquifer travel time"""
    num = np.zeros(NT)
    den = np.zeros(NT)
    for z, w in zip(GH_Z, GH_W):
        lag = max(T * (1 + P.SAT_SPREAD * z), 0.05)
        k = int(round(lag / DT))
        num[k:] += w * (fl * c_wt)[:NT - k]
        den[k:] += w * fl[:NT - k]
    return num, den


def build(seed=P.SEED):
    rng = np.random.default_rng(seed)
    wx = weather(rng)
    parcels = whpa_parcels(rng)
    sites = network_sites(rng)
    wells = {}
    for w in P.WELLS:
        num = np.zeros(NT)
        den = np.zeros(NT)
        for p in parcels:
            if p["zone"] != w:
                continue
            c_wt, fl = water_table(p, wx)
            p["c_wt"] = c_wt
            n, d = to_well(c_wt, fl, p["T"])
            num += p["acres"] * n
            den += p["acres"] * d
        wells[w] = num / np.maximum(den, 1e-12)
    for s in sites:
        c_wt, _ = water_table(s, wx)
        k = int(round(s["age"] / DT))
        out = np.empty(NT)
        out[k:] = c_wt[:NT - k]
        out[:k] = c_wt[0]
        s["c"] = out
    return dict(wx=wx, parcels=parcels, sites=sites, wells=wells, rng_state=seed)


def annual(series, y):
    a, b = idx(y), idx(y + 1)
    return float(np.mean(series[a:b]))
