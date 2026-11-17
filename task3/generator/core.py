#!/usr/bin/env python3
"""task3 architecture 8, the core: triggering storms at seven gully crossings of a mountain road service.

The decision's quantity is the mean number of storms a season in which the rain at a crossing's source area reaches
the crossing's triggering depth in 60 consecutive minutes. No record holds it. Each instrument sees a part of it:

  the governing gauge   an unheated tipping bucket at the road station below the source, tip by tip for 18 seasons
                        (2009 to 2026).
                        It loses water while the bucket tips, more the harder it rains (S1), and on hail days the
                        funnel holds the ice and the bucket tips its melt for an hour or two afterwards (S3).
  the totaliser         a storage gauge beside each bucket, read at the monthly visit: the true depth of the interval.
  the detector          the road station's present-weather detector: when precipitation fell and of what kind, every
                        ten minutes, with an optical intensity good for timing and poor for amounts.
  the radar             60-minute storm maxima on one-kilometre pixels: it sees the source and the gauge in the same
                        storm, as area averages on its own scale (S2).
  the rainfall normal   the mean annual precipitation grid: totals, which is not what a burst is.

This file simulates that world, builds the golden estimator and the hurried one at each of the three judgments, the
direct, the index and the radar routes, a battery of rebuilds of the golden's conventions and the referee slice
(a research valley with weighing gauges at its sources), and hands the lot to corelib. Nothing here reads a prompt.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = 20270213
G_SEASONS = 18            # tip record, warm seasons 2009 to 2026
R_SEASONS = 14            # radar storm maxima, 2013 to 2026
C_SEASONS = 14            # research valley weighing gauges, 2013 to 2026
T_SEASONS = 600           # the world's own long run, for the truth
LINE = 3.0                # triggering storms a season from which a crossing is class 3 (automatic barrier)
LOW_LINE = 1.0            # from which it is class 2 (seasonal patrol and hand gates); under it, class 1 (signs)
M = 300                   # minutes kept per storm
MONTH_P = np.array([0.08, 0.20, 0.30, 0.26, 0.12, 0.04])   # May to October

SIG_Z, SIG_E, CORR_KM = 0.46, 0.34, 5.0      # storm to storm, place to place inside a storm, and its reach
GAMMA, SIG_B, SIG_NU = 0.28, 0.15, 0.07      # what a pixel keeps of the local factor; the radar's storm and pixel error
KAPPA = {"A": 0.0014, "B": 0.0024}           # hours per mm: the bucket's loss per unit of rate
THETA = (55.0, 115.0)                        # the funnel's melt time on a hail day, minutes
PHI = (0.35, 0.70)                           # the share of a hail storm's burst that falls as ice
HAIL_Z = (3.5, 5.0)                          # a cell hails from this strength (mm), and always this much above it

DEPOTS = {
    # name: bucket model, storms a season, median burst (mm), burst length (min), hail share of the larger storms
    "Valfosca":   dict(model="B", mu=58, zmed=6.2, tau=(5, 14),  hail=0.10, wet=60),
    "Pradalt":    dict(model="A", mu=56, zmed=5.6, tau=(6, 20),  hail=0.34),
    "Costarossa": dict(model="A", mu=55, zmed=5.8, tau=(6, 20),  hail=0.86),
    "Malga Sora": dict(model="A", mu=60, zmed=6.4, tau=(6, 20),  hail=0.30),
    "Forcella":   dict(model="B", mu=60, zmed=6.6, tau=(8, 24),  hail=0.30),
    "Rio Scuro":  dict(model="B", mu=58, zmed=6.0, tau=(7, 22),  hail=0.45),    # the research valley
}
# crossing: governing gauge, km from the gauge, burst factor against the gauge, rainfall-normal ratio, and the
# triggering depth the geotechnical survey filed (mm in 60 minutes at the source area)
CROSSINGS = {
    "Rio Gelt":   dict(depot="Valfosca",   km=1.8, f=1.12, map=1.03, depth=17.0),
    "Rio Marden": dict(depot="Pradalt",    km=3.4, f=1.38, map=1.06, depth=19.5),
    "Rio Bianc":  dict(depot="Costarossa", km=2.2, f=1.10, map=1.045, depth=16.0),
    "Rio Ciadin": dict(depot="Malga Sora", km=2.9, f=1.06, map=1.40, depth=13.0),
    "Rio Toval":  dict(depot="Forcella",   km=4.1, f=1.08, map=1.00, depth=12.5),
    "Rio Sass":   dict(depot="Pradalt",    km=2.0, f=0.98, map=0.90, depth=17.0),
    "Rio Larin":  dict(depot="Malga Sora", km=4.6, f=0.94, map=1.02, depth=29.0),
}
RESEARCH = {
    "Scuro 1": dict(depot="Rio Scuro", km=0.4, f=0.90, map=1.38, rate=4.0),
    "Scuro 2": dict(depot="Rio Scuro", km=0.8, f=0.82, map=1.25, rate=4.0),
    "Scuro 3": dict(depot="Rio Scuro", km=1.2, f=0.88, map=1.44, rate=4.0),
    "Scuro 4": dict(depot="Rio Scuro", km=1.7, f=0.78, map=1.22, rate=4.0),
}
ALL = {**CROSSINGS, **RESEARCH}
OPENED = {"S1": "Rio Gelt", "S2": "Rio Marden", "S3": "Rio Bianc"}

COUNT_FLOOR, DEPTH_FLOOR, OWN_FLOOR = 0.04, 0.015, 0.03   # what two honest rebuilds of a count, a depth and a stump's own figure differ by
LOSS_WAYS = ("recip", "lin", "scaled")
POOL_WAYS = ("model", "gauge")
STEP_WAYS = (1, 5)                           # the rate read minute by minute, or on five-minute totals
SITE_WAYS = ("geo", "median", "sums", "trim", "geo3", "gauge3", "pairs", "upper")
CRUDE_SITE = ("slope", "top", "q90")         # one-sided selections and unpaired percentiles, each refuted by a figure
HAIL_WAYS = ("profile", "weighted", "onset", "carried")
CRUDE_HAIL = ("dry", "even", "optical")      # each refuted by a figure the files hold
CRUDE_STEP = (10, 15)                        # the rate read on ten- and fifteen-minute totals: the account refuses both


class Rates(dict):
    """Triggering storms a season by crossing, with `.even`: the depth each source reaches LINE times a season."""


def slide60(a):
    """The largest total over 60 consecutive minutes, storm by storm."""
    cs = np.cumsum(a, axis=1, dtype=np.float64)
    w = np.concatenate([cs[:, 59:60], cs[:, 60:] - cs[:, :-60]], axis=1)
    return w.max(axis=1)


def storms(name, seasons, rng, record=True):
    """One gauge's storms: the true minutes, what the bucket tipped, what the detector saw, the monthly account."""
    d = DEPOTS[name]
    kap = KAPPA[d["model"]]
    n = rng.poisson(d["mu"], seasons)
    N = int(n.sum())
    season = np.repeat(np.arange(seasons), n)
    month = rng.choice(6, N, p=MONTH_P)
    pts = [s for s, c in ALL.items() if c["depot"] == name]
    km = np.array([0.0] + [ALL[s]["km"] for s in pts])
    cov = SIG_E ** 2 * np.exp(-np.abs(km[:, None] - km[None, :]) / CORR_KM)
    side = np.random.default_rng(int(rng.integers(0, 2 ** 31)))     # the sources' own stream: the gauge's storms do not move with the layout
    e = np.concatenate([rng.standard_normal((N, 1)), side.standard_normal((N, len(pts)))], axis=1) @ np.linalg.cholesky(cov).T
    Z = np.exp(rng.normal(math.log(d["zmed"]), SIG_Z, N))
    D = Z * np.exp(e[:, 0])                                   # the burst at the gauge
    tau = rng.integers(d["tau"][0], d["tau"][1] + 1, N)
    idx = np.arange(M)[None, :]
    t = (idx + 0.5) / tau[:, None]
    w = np.where(t < 1.0, t * (1.0 - t) ** 2, 0.0) * np.exp(0.35 * rng.standard_normal((N, M)))
    w /= w.sum(axis=1, keepdims=True)
    burst = D[:, None] * w
    has = rng.random(N) < 0.5
    V = np.minimum(D * rng.uniform(0.1, 0.5, N), 15.0) * has
    L = rng.integers(60, 181, N)
    tw = np.where((idx >= tau[:, None]) & (idx < (tau + L)[:, None]), (tau + L)[:, None] - idx, 0.0)
    trail = V[:, None] * tw / tw.sum(axis=1, keepdims=True)
    true_min = burst + trail
    out = dict(name=name, N=N, season=season, month=month, e=e, pts=pts, x_true=slide60(true_min))
    if not record:
        return out
    hail = rng.random(N) < d["hail"] * np.clip((Z - HAIL_Z[0]) / HAIL_Z[1], 0.0, 1.0)     # ice comes with the stronger cells
    phi = rng.uniform(PHI[0], PHI[1], N) * hail               # the share of the burst that falls as hail
    theta = rng.uniform(THETA[0], THETA[1], N)                # the funnel's melt time, minutes
    cen = (burst * idx).sum(axis=1) / D + 3.0
    lag = np.maximum(idx - cen[:, None], 0.0)
    melt = np.where(idx >= cen[:, None], np.exp(-lag / theta[:, None]) - np.exp(-(lag + 1.0) / theta[:, None]), 0.0)
    melt /= np.maximum(melt.sum(axis=1, keepdims=True), 1e-12)
    inflow = burst * (1.0 - phi[:, None]) + trail + (phi * D)[:, None] * melt
    rec = inflow / (1.0 + kap * 60.0 * inflow)                # the bucket loses in proportion to the rate
    b10 = lambda a: a.reshape(N, M // 10, 10).sum(axis=2)
    rain10, hail10 = b10(burst * (1.0 - phi[:, None]) + trail), b10(burst * phi[:, None])
    opt = rain10 * np.exp(0.30 * rng.standard_normal(N))[:, None] + hail10 * np.exp(0.40 * rng.standard_normal(N))[:, None]
    wet = (rain10 + hail10) > 0.02
    # the monthly account: storms plus the long light rain no storm file holds
    nint = seasons * 6
    fh = np.minimum(rng.gamma(1.5, 1.8, (nint, d.get("wet", 40))), 6.0)   # hourly depths of the long rain, never near a triggering depth
    ivl = season * 6 + month
    check = (np.bincount(ivl, true_min.sum(axis=1), nint) + fh.sum(axis=1)) * (1.0 + 0.006 * rng.standard_normal(nint))
    out.update(model=d["model"], rec=rec.astype(np.float64), hail=hail, opt=opt, wet=wet, hail10=hail10 > 0.02,
               ivl=ivl, nint=nint, front_rec=fh / (1.0 + kap * fh), check=check,
               base=out["x_true"] * np.exp(-e[:, 0]),
               rb=np.exp(SIG_B * rng.standard_normal(N)), rnu=SIG_NU * side.standard_normal((N, len(km))))
    return out


# ---------------------------------------------------------------------------------------------------- estimators
def put_back(r, k, form, per_hour=60.0):
    """A recorded depth per step put back at loss k: the tipping-time form, its first-order form, or the tipping-time
    form with a static calibration factor fitted beside it (k is then the pair (factor, loss))."""
    if form == "lin":
        return r * (1.0 + k * per_hour * r)
    if form == "scaled":
        return k[0] * r / (1.0 - k[1] * per_hour * r)
    return r / (1.0 - k * per_hour * r)


def put_step(rec, k, form="recip", step=1):
    """The tipped minutes put back with the rate read on `step`-minute totals."""
    if step == 1:
        return put_back(rec, k, form)
    n, m = rec.shape
    b = rec.reshape(n, m // step, step).sum(axis=2)
    cb = put_back(b, k, form, 60.0 / step)
    return rec * np.repeat(np.where(b > 0, cb / np.maximum(b, 1e-12), 1.0), step, axis=1)


def account(w, k, form="recip", step=1):
    """The interval totals the tips give once each step is put back at loss k."""
    return np.bincount(w["ivl"], put_step(w["rec"], k, form, step).sum(axis=1), w["nint"]) + \
        put_back(w["front_rec"], k, form, 1.0).sum(axis=1)


def fit_kappa(ws, form="recip", step=1):
    """The bucket's loss per unit of rate, from the account that has to close against the totaliser."""
    lo, hi = 0.0, 0.0075
    if form == "scaled":
        def scale(k):
            acc = [account(w, (1.0, k), form, step) for w in ws]
            return sum(float((w["check"] * a).sum()) for w, a in zip(ws, acc)) / sum(float((a * a).sum()) for a in acc)
        sse = lambda k: sum(float(((w["check"] - account(w, (scale(k), k), form, step)) ** 2).sum()) for w in ws)
    else:
        sse = lambda k: sum(float(((w["check"] - account(w, k, form, step)) ** 2).sum()) for w in ws)
    g = (math.sqrt(5.0) - 1.0) / 2.0
    a, b = hi - g * (hi - lo), lo + g * (hi - lo)
    fa, fb = sse(a), sse(b)
    for _ in range(44):
        if fa < fb:
            hi, b, fb = b, a, fa
            a = hi - g * (hi - lo)
            fa = sse(a)
        else:
            lo, a, fa = a, b, fb
            b = lo + g * (hi - lo)
            fb = sse(b)
    k = 0.5 * (lo + hi)
    return (scale(k), k) if form == "scaled" else k


_KAP = {}


def kappas(W, form="recip", pool="model", step=1):
    if (id(W), form, pool, step) in _KAP:
        return _KAP[(id(W), form, pool, step)]
    out = _KAP.setdefault((id(W), form, pool, step), {})
    for mdl in KAPPA:
        ws = [w for w in W.values() if w["model"] == mdl]
        if pool == "gauge":
            out.update({w["name"]: fit_kappa([w], form, step) for w in ws})
        else:
            k = fit_kappa(ws, form, step)
            out.update({w["name"]: k for w in ws})
    return out


def minutes(w, s1, k=0.0, form="recip", step=1):
    """The tipped minutes put back: by the rate (golden), by one factor that closes the account, or left raw."""
    if s1 == "rate":
        return put_step(w["rec"], k, form, step)
    if s1 == "factor":
        return w["rec"] * float(w["check"].sum() / account(w, 0.0).sum())
    return w["rec"]


def band(golden, family, floor):
    """A figure's band: the battery's range, and never tighter than what two honest rebuilds differ by."""
    lo, hi = min(family + [golden]), max(family + [golden])
    return [min(lo, golden * (1.0 - floor)), max(hi, golden * (1.0 + floor))]


def storm_max(w, c, s3):
    """Each storm's 60-minute maximum at the gauge. On hail storms the bucket has the amount and the detector has
    the timing. 'profile' places the storm's water by the detector's ten-minute profile; 'weighted' first rescales
    the hail intervals' optical intensity so the hail storms' totals close; 'onset' keeps the tips before the first
    hail interval and places the rest; 'dry' and 'even' are the crude rivals (move only the water tipped while the
    detector saw nothing; spread it evenly over the wet intervals); 'tips' takes the tips as rain."""
    x = slide60(c)
    if s3 == "tips":
        return x
    h, N = w["hail"], w["N"]
    if s3 == "optical":                      # the detector's own amounts on hail storms, scaled on the rain storms
        c10 = c.reshape(N, M // 10, 10).sum(axis=2)
        cr = float(c10[~h].sum() / w["opt"][~h].sum())
        return np.where(h, slide60(np.repeat(cr * w["opt"] / 10.0, 10, axis=1)), x)
    if s3 == "carried":                      # one hail-day multiplier, read at the research valley's weighing gauges
        return np.where(h, x * w["carried"], x)
    c10 = c.reshape(N, M // 10, 10).sum(axis=2)
    tot = c10.sum(axis=1, keepdims=True)
    opt = w["opt"]
    if s3 == "weighted":
        dryday = ~h
        cr = float(c10[dryday].sum() / opt[dryday].sum())
        wh = float((c10[h].sum() - cr * (opt[h] * ~w["hail10"][h]).sum()) / (cr * (opt[h] * w["hail10"][h]).sum()))
        opt = opt * np.where(w["hail10"], wh, 1.0)
    if s3 in ("profile", "weighted"):
        b = tot * opt / np.maximum(opt.sum(axis=1, keepdims=True), 1e-12)
    elif s3 == "onset":
        first = np.where(w["hail10"].any(axis=1), w["hail10"].argmax(axis=1), 0)
        pre = np.arange(M // 10)[None, :] < first[:, None]
        rest = opt * ~pre
        b = c10 * pre + (tot - (c10 * pre).sum(axis=1, keepdims=True)) * rest / np.maximum(rest.sum(axis=1, keepdims=True), 1e-12)
    elif s3 == "even":
        b = tot * w["wet"] / np.maximum(w["wet"].sum(axis=1, keepdims=True), 1)
    else:
        dry = ~w["wet"]
        key = opt * w["hail10"]
        b = c10 * ~dry + (c10 * dry).sum(axis=1, keepdims=True) * key / np.maximum(key.sum(axis=1, keepdims=True), 1e-12)
    y = slide60(np.repeat(b / 10.0, 10, axis=1))
    return np.where(h, y, x)


def radar(w, j):
    """The radar's 60-minute storm maximum on the pixel over point j of this gauge's group (0 is the gauge)."""
    f = 1.0 if j == 0 else ALL[w["pts"][j - 1]]["f"]
    return f * w["rb"] * w["base"] * np.exp(GAMMA * w["e"][:, j] + w["rnu"][:, j])


def site_factor(w, s, how="geo"):
    """The source's bursts against the gauge's, from the radar's pixel pairs storm by storm."""
    j = 1 + w["pts"].index(s)
    era = w["season"] >= G_SEASONS - R_SEASONS
    a, b = radar(w, j)[era], radar(w, 0)[era]
    if how == "q90":                         # the two pixels' upper deciles, unpaired
        return float(np.quantile(a, 0.9) / np.quantile(b, 0.9))
    if how == "slope":                       # crude: the source pixel regressed on the gauge's through the origin
        return float((a * b).sum() / (b * b).sum())
    if how == "top":                         # crude: the gauge pixel's largest quarter of storms
        m = b >= np.quantile(b, 0.75)
        return float(a[m].sum() / b[m].sum())
    if how == "upper":                       # the pairs whose joint size is in the upper quarter
        g = np.sqrt(a * b)
        m = g >= np.quantile(g, 0.75)
        return float(np.exp(np.log(a[m] / b[m]).mean()))
    ok = (b >= 3.0) if how == "gauge3" else ((a >= 3.0) & (b >= 3.0)) if how == "geo3" else (a >= 1.0) & (b >= 1.0)
    a, b = a[ok & (a > 0)], b[ok & (a > 0)]
    lr = np.log(a / b)
    if how in ("geo", "geo3", "gauge3", "pairs"):
        return float(np.exp(lr.mean()))
    if how == "median":
        return float(np.exp(np.median(lr)))
    if how == "sums":
        return float(a.sum() / b.sum())
    q = np.sort(lr)
    k = int(0.1 * len(q))
    return float(np.exp(q[k:len(q) - k].mean()))


def build(seed):
    W = {d: storms(d, G_SEASONS, np.random.default_rng([seed, i])) for i, d in enumerate(DEPOTS)}
    # the world's long run sets the truth, and the triggering depths the geotechnical survey filed
    for s, c in ALL.items():
        lr = storms(c["depot"], T_SEASONS, np.random.default_rng(seed + 7 + sorted(ALL).index(s)), record=False)
        q = np.sort(lr["x_true"])[::-1]
        c["T"] = float(c["depth"]) if "depth" in c else round(2.0 * c["f"] * float(q[int(round(c["rate"] * T_SEASONS))])) / 2.0
        c["truth"] = float((lr["x_true"] >= c["T"] / c["f"]).sum()) / T_SEASONS
    return W


def source_max(w, s):
    """What a weighing gauge at source s recorded: the storm's true 60-minute maximum there."""
    j = 1 + w["pts"].index(s)
    return w["x_true"] * ALL[s]["f"] * np.exp(w["e"][:, j] - w["e"][:, 0])


def research_reads(W, kap):
    """What the research valley's weighing gauges say when they are read as a calibration of the bucket: one ratio of
    source to bucket over every storm (the carried transfer), and one hail-day multiplier (hail storms' ratio over
    the rain storms' ratio, on the bucket's rate-corrected maxima)."""
    w = W["Rio Scuro"]
    era = w["season"] >= G_SEASONS - C_SEASONS
    raw, cor = slide60(w["rec"]), slide60(put_back(w["rec"], kap, "recip"))
    src = sum(source_max(w, s) for s in RESEARCH) / len(RESEARCH)
    h, r = era & w["hail"], era & ~w["hail"]
    return float(src[era].sum() / raw[era].sum()), float((src[h].sum() / cor[h].sum()) / (src[r].sum() / cor[r].sum()))


_XS = {}


def station_maxima(W, s1, s3, form, pool, step):
    """Each gauge's storm maxima under one choice of loss and hail handling (kept: the site ways reuse them)."""
    key = (id(W), s1, s3, form, pool, step)
    if key not in _XS:
        kap = kappas(W, form, pool, step) if s1 == "rate" else {d: 0.0 for d in W}
        if s3 == "carried":
            m = research_reads(W, kappas(W)["Rio Scuro"])[1]
            for w in W.values():
                w["carried"] = m
        _XS[key] = ({d: storm_max(w, minutes(w, s1, kap[d], form, step), s3) for d, w in W.items()}, kap)
    return _XS[key]


def transfer(w, s, x, s2):
    """A gauge's storm maxima carried to source s. 'pairs' carries each storm by its own pixel pair where the radar
    saw both, and by the mean factor before the radar's record."""
    c = ALL[s]
    if s2 == "map":
        return c["map"] * x
    if s2 == "one":
        return x
    f = site_factor(w, s, s2)
    if s2 != "pairs":
        return f * x
    j = 1 + w["pts"].index(s)
    a, b = radar(w, j), radar(w, 0)
    ok = (w["season"] >= G_SEASONS - R_SEASONS) & (a >= 1.0) & (b >= 1.0)
    return np.where(ok, x * a / np.maximum(b, 1e-9), x * f)


def at_source(W, s, s1="rate", s2="geo", s3="profile", form="recip", pool="model", step=1):
    """Source s's 60-minute storm maxima, storm by storm, under one choice at each judgment."""
    xs, _ = station_maxima(W, s1, s3, form, pool, step)
    return transfer(W[ALL[s]["depot"]], s, xs[ALL[s]["depot"]], s2)


def estimate(W, s1="rate", s2="geo", s3="profile", form="recip", pool="model", only=None, seasons=None, step=1):
    """Every crossing's triggering storms a season under one choice at each judgment."""
    xs, kap = station_maxima(W, s1, s3, form, pool, step)
    out, even, upper = Rates(), {}, {}
    for s, c in ALL.items():
        if only and s not in only:
            continue
        w = W[c["depot"]]
        est = transfer(w, s, xs[c["depot"]], s2)
        keep = np.ones(w["N"], bool) if seasons is None else w["season"] >= G_SEASONS - seasons
        out[s] = float(((est >= c["T"]) & keep).sum()) / (seasons or G_SEASONS)
        even[s] = at_line(est[keep], seasons or G_SEASONS)
        upper[s] = upper_mean(est[keep], seasons or G_SEASONS)
    out.even, out.upper = even, upper
    return out, kap


def at_line(x, seasons):
    """The 60-minute depth a source reaches LINE times a season: the triggering depth at which it would sit on the line."""
    return float(np.sort(x)[::-1][int(round(LINE * seasons)) - 1])


def upper_mean(x, seasons, per=5):
    """The mean 60-minute depth of a source's `per` largest storms a season."""
    return float(np.sort(x)[::-1][:per * seasons].mean())


def radar_route(W, only=None, seasons=R_SEASONS):
    """The standard radar product: one field bias against the gauges' account-closed maxima, then the source pixel
    counted against the triggering depth."""
    num = den = 0.0
    for d, w in W.items():
        era = w["season"] >= G_SEASONS - R_SEASONS
        num += float(slide60(minutes(w, "factor"))[era].sum())
        den += float(radar(w, 0)[era].sum())
    bias = num / den
    out, even, upper = Rates(), {}, {}
    for s, c in ALL.items():
        if only and s not in only:
            continue
        w = W[c["depot"]]
        era = w["season"] >= G_SEASONS - seasons
        j = 1 + w["pts"].index(s)
        out[s] = float(((bias * radar(w, j) >= c["T"]) & era).sum()) / seasons
        even[s] = at_line(bias * radar(w, j)[era], seasons)
        upper[s] = upper_mean(bias * radar(w, j)[era], seasons)
    out.even, out.upper = even, upper
    return out


def seen(W, s, seasons):
    """The triggering storms a weighing gauge at source s saw in the last `seasons` seasons."""
    w = W[ALL[s]["depot"]]
    return float(((source_max(w, s) >= ALL[s]["T"]) & (w["season"] >= G_SEASONS - seasons)).sum())


def carried_route(W):
    """The research valley read as a calibration: its one ratio of source to bucket carried to every crossing."""
    c = research_reads(W, 0.0)[0]
    return {s: float((c * slide60(W[k["depot"]]["rec"]) >= k["T"]).sum()) / G_SEASONS for s, k in CROSSINGS.items()}


def main(seed=SEED, quiet=False):
    W = build(seed)
    names = sorted(CROSSINGS)
    gold, kap = estimate(W)
    truth = {s: CROSSINGS[s]["truth"] for s in names}

    # the battery: every convention of the golden rebuilt the ways the field does it, crossed
    ways = [(fo, po, st, a, b) for fo in LOSS_WAYS for po in POOL_WAYS for st in STEP_WAYS for a in SITE_WAYS for b in HAIL_WAYS]
    fam = [estimate(W, "rate", a, b, fo, po, step=st)[0] for fo, po, st, a, b in ways]
    FAM = len(fam)

    def route(lost):
        return estimate(W, "factor" if "S1" in lost else "rate", "map" if "S2" in lost else "geo",
                        "tips" if "S3" in lost else "profile")[0]
    keys = [("S1",), ("S2",), ("S3",), ("S1", "S2"), ("S1", "S3"), ("S2", "S3"), ("S1", "S2", "S3")]
    lat_full = {"+".join(k): route(k) for k in keys}
    direct = estimate(W, "raw", "one", "tips")[0]
    index = lat_full["S1+S2+S3"]
    rad = radar_route(W)
    car = carried_route(W)
    crude_fam = {"hail " + b: estimate(W, s3=b)[0] for b in CRUDE_HAIL}
    crude_fam.update({"site " + a: estimate(W, s2=a)[0] for a in CRUDE_SITE})
    crude_fam.update({"loss on %d-minute totals" % st: estimate(W, step=st)[0] for st in CRUDE_STEP})

    members = {s: {"lines": [LOW_LINE, LINE], "truth": truth[s], "golden": gold[s], "family": [v[s] for v in fam],
                   "routes": {"direct": direct[s], "rigorous": rad[s], "index": index[s], "carried": car[s]}} for s in names}
    lattice = {k: {s: v[s] for s in names} for k, v in lat_full.items()}

    # the stumps' own figures
    dB, dH = W["Valfosca"], W["Costarossa"]
    fac = lambda w: float(w["check"].sum() / account(w, 0.0).sum())

    def under_read(k, form="recip", true_rate=100.0):
        """What the bucket fails to record at a true rate, in per cent, under a fitted loss."""
        lo, hi = 0.0, true_rate
        for _ in range(60):                 # the recorded rate whose put-back is the true rate
            mid = 0.5 * (lo + hi)
            lo, hi = (mid, hi) if float(put_back(mid, k, form, 1.0)) < true_rate else (lo, mid)
        return 100.0 * (1.0 - lo / true_rate)
    c1 = {"g": under_read(kap["Valfosca"]), "lost": 100.0 * (1.0 - 1.0 / fac(dB)),
          "fam": [under_read(kappas(W, fo, po, st)["Valfosca"], fo) for fo in LOSS_WAYS for po in POOL_WAYS for st in STEP_WAYS]}
    c2 = {"g": site_factor(W["Pradalt"], "Rio Marden"), "lost": CROSSINGS["Rio Marden"]["map"],
          "fam": [site_factor(W["Pradalt"], "Rio Marden", a) for a in SITE_WAYS]}

    def hail_gap(w, k, s3="profile", form="recip"):
        c = put_back(w["rec"], k, form)
        a, b = storm_max(w, c, "tips")[w["hail"]], storm_max(w, c, s3)[w["hail"]]
        return 100.0 * (1.0 - float(a.sum()) / float(b.sum()))
    c3 = {"g": hail_gap(dH, kap["Costarossa"]), "lost": 0.0,
          "fam": [hail_gap(dH, kappas(W, fo, po)["Costarossa"], b, fo) for fo in LOSS_WAYS for po in POOL_WAYS for b in HAIL_WAYS]}
    _XS.clear()

    def per_key(golden_value, lost_value, sid):
        return {"+".join(k): (lost_value if sid in k else golden_value) for k in keys}
    pad = lambda v: (v * (FAM // len(v) + 1))[:max(FAM, 12)]
    figures = [
        {"id": "C1 the Valfosca bucket's under-read at 100 mm an hour (per cent)", "block": "component",
         "golden": c1["g"], "family": pad(c1["fam"]), "lattice": per_key(c1["g"], c1["lost"], "S1"),
         "routes": {"rigorous": c1["lost"]}},
        {"id": "C2 burst factor, Rio Marden against Pradalt", "block": "component", "golden": c2["g"],
         "family": pad(c2["fam"]), "lattice": per_key(c2["g"], c2["lost"], "S2"), "routes": {"rigorous": 1.0}},
        {"id": "C3 hail storms' 60-minute maximum the tips miss, Costarossa (per cent)", "block": "component",
         "golden": c3["g"], "family": pad(c3["fam"]), "lattice": per_key(c3["g"], c3["lost"], "S3"),
         "routes": {"rigorous": 0.0}},
    ]
    figures += [{"id": s, "block": "ask", "member": s} for s in names]
    figures += [{"id": "depth on the line, " + s, "block": "ask", "golden": gold.even[s],
                 "family": [v.even[s] for v in fam], "lattice": {k: v.even[s] for k, v in lat_full.items()},
                 "routes": {"rigorous": rad.even[s]}} for s in names]
    for f in figures:                       # every band holds the battery and the rebuild floor
        g = members[f["member"]]["golden"] if "member" in f else f["golden"]
        fm = members[f["member"]]["family"] if "member" in f else f["family"]
        f["band"] = band(g, fm, COUNT_FLOOR if "member" in f else DEPTH_FLOOR if f["id"].startswith("depth") else OWN_FLOOR)

    # the referee: the research valley's weighing gauges at four sources
    wr = W["Rio Scuro"]
    era_c = wr["season"] >= G_SEASONS - C_SEASONS
    rdepth = lambda v: float(np.mean([v.even[s] for s in RESEARCH]))
    rtop = lambda v: float(np.mean([v.upper[s] for s in RESEARCH]))
    rcount = lambda v: float(sum(v[s] for s in RESEARCH)) * C_SEASONS
    rv = lambda **kw: estimate(W, only=RESEARCH, seasons=C_SEASONS, **kw)[0]
    rivals = {"bucket put back by one factor": rv(s1="factor"), "source scaled by the rainfall normal": rv(s2="map"),
              "tips taken as rain on hail days": rv(s3="tips"), "the gauge read raw": rv(s1="raw", s2="one", s3="tips"),
              "the radar product": radar_route(W, only=RESEARCH, seasons=C_SEASONS)}
    others = {"hail water moved only from the dry intervals": rv(s3="dry"), "hail water spread evenly": rv(s3="even"),
              "the detector's own amounts on hail storms": rv(s3="optical"), "each storm by its own pixel pair": rv(s2="pairs"),
              "one hail-day multiplier from the valley": rv(s3="carried"), "the rate read on five-minute totals": rv(step=5),
              "the pixels' upper deciles": rv(s2="q90"), "the source pixel regressed on the gauge's": rv(s2="slope")}
    rgold = rv()
    seen_depth = float(np.mean([at_line(source_max(wr, s)[era_c], C_SEASONS) for s in RESEARCH]))
    seen_count = sum(seen(W, s, C_SEASONS) for s in RESEARCH)
    seen_top = float(np.mean([upper_mean(source_max(wr, s)[era_c], C_SEASONS) for s in RESEARCH]))
    ref = {"slice": "the Rio Scuro research valley: weighing gauges at four sources over %d seasons; the mean 60-minute "
                    "depth of each source's five largest storms a season, mean of the four (mm)" % C_SEASONS,
           "covers_target": False, "truth": seen_top, "golden": rtop(rgold),
           "rivals": {k: rtop(v) for k, v in rivals.items()}}

    stumps = {
        "S1": {"axis": "what", "opens": OPENED["S1"], "steps_left": 4, "precedents": ["N21", "L28"],
               "said_out_loud": "The tipping buckets lose water while they tip, more the harder it rains."},
        "S2": {"axis": "who", "opens": OPENED["S2"], "steps_left": 4, "precedents": ["N26", "N01"],
               "said_out_loud": "A source's cloudbursts are not its gauge's, and they do not scale with its yearly rainfall."},
        "S3": {"axis": "when", "opens": OPENED["S3"], "steps_left": 4, "precedents": ["N30", "L26"],
               "said_out_loud": "On hail days the funnel holds the ice and the bucket tips its melt after the storm has gone."},
    }
    spec = {"task": "task3 architecture 8", "call": "lines", "members": members, "stumps": stumps, "lattice": lattice,
            "referee": ref, "figures": figures}

    if quiet:
        return spec
    if "--quiet" not in sys.argv:
        p = lambda label, v: print("%-26s" % label + ", ".join("%s %.2f" % (s.replace("Rio ", ""), v[s]) for s in names))
        print("triggering depths (mm in 60 minutes): " + ", ".join("%s %.1f" % (s, ALL[s]["T"]) for s in ALL))
        print("loss per unit of rate, fitted: " + ", ".join("%s %.5f (%.5f)" % (d, kap[d], KAPPA[DEPOTS[d]["model"]]) for d in DEPOTS))
        for fo in LOSS_WAYS:
            for po in POOL_WAYS:
                print("   %s/%s: " % (fo, po) + ", ".join("%s %s" % (d[:6], ("%.3f x %.5f" % v) if isinstance(v, tuple) else "%.5f" % v) for d, v in kappas(W, fo, po).items()))
        for dim, opts in (("loss", [(fo, po, st, "geo", "profile") for fo in LOSS_WAYS for po in POOL_WAYS for st in STEP_WAYS]),
                          ("site", [("recip", "model", 1, a, "profile") for a in SITE_WAYS]),
                          ("hail", [("recip", "model", 1, "geo", b) for b in HAIL_WAYS])):
            vs = [estimate(W, "rate", a, b, fo, po, step=st)[0] for fo, po, st, a, b in opts]
            print("   spread by %s: " % dim + ", ".join("%s %.2f-%.2f" % (s.replace("Rio ", ""), min(v[s] for v in vs), max(v[s] for v in vs)) for s in names))
        print("account factor: " + ", ".join("%s %.3f" % (d, fac(W[d])) for d in DEPOTS))
        print("burst factors, fitted (world): " + ", ".join("%s %.3f (%.2f)" % (s, site_factor(W[ALL[s]["depot"]], s), ALL[s]["f"]) for s in ALL))
        p("truth", truth)
        p("golden", gold)
        print("%-26s" % "family" + ", ".join("%s %.2f-%.2f" % (s.replace("Rio ", ""), min(v[s] for v in fam), max(v[s] for v in fam)) for s in names))
        for k, v in lat_full.items():
            p(k + " lost", v)
        p("direct", direct)
        p("radar", rad)
        p("carried", car)
        print("research valley read as a calibration: source over bucket %.3f, hail-day multiplier %.3f" % research_reads(W, kap["Rio Scuro"]))
        for b, v in crude_fam.items():
            p(b, v)
        pe = lambda label, v: print("%-26s" % label + ", ".join("%s %.1f" % (s.replace("Rio ", ""), v.even[s]) for s in names))
        pe("depth golden", gold)
        print("%-26s" % "depth family" + ", ".join("%s %.1f-%.1f" % (s.replace("Rio ", ""), min(v.even[s] for v in fam), max(v.even[s] for v in fam)) for s in names))
        for k, v in lat_full.items():
            if "+" not in k:
                pe("depth %s lost" % k, v)
        print("components: C1 %.2f (lost %.2f; family %.2f to %.2f), C2 %.3f (lost %.2f; family %.3f to %.3f), C3 %.1f (family %.1f to %.1f)" % (
            c1["g"], c1["lost"], min(c1["fam"]), max(c1["fam"]), c2["g"], c2["lost"], min(c2["fam"]), max(c2["fam"]),
            c3["g"], min(c3["fam"]), max(c3["fam"])))
        # what refutes each shortcut, from records the pack will hold
        for d in ("Valfosca", "Pradalt"):
            w = W[d]
            x = np.bincount(w["ivl"], (60.0 * w["rec"] ** 2).sum(axis=1), w["nint"])
            rf, rg = w["check"] - fac(w) * account(w, 0.0), w["check"] - account(w, kap[d])
            r = float(np.corrcoef(x, rf)[0, 1])
            print("account, %s: one factor leaves a monthly residual of %.2f mm rms that follows the month's burst rain (r %.2f, t %.1f); the rate fit leaves %.2f mm" % (
                d, float(np.sqrt((rf ** 2).mean())), r, r * math.sqrt((w["nint"] - 2) / (1 - r * r)), float(np.sqrt((rg ** 2).mean()))))
        for mdl in ("B", "A"):               # the account against the rate's time step and the loss's form
            ws = [w for w in W.values() if w["model"] == mdl]
            rms = lambda form, st: float(np.sqrt(np.mean(np.concatenate(
                [w["check"] - account(w, fit_kappa(ws, form, st), form, st) for w in ws]) ** 2)))
            print("account, model %s buckets, monthly residual (mm rms) with the rate read on 1, 5, 10 and 15 minute totals: %s; first-order form on 1 minute %.2f" % (
                mdl, ", ".join("%.2f" % rms("recip", st) for st in (1, 5, 10, 15)), rms("lin", 1)))
        for d in ("Costarossa", "Valfosca"):
            w = W[d]
            c10 = w["rec"].reshape(w["N"], M // 10, 10).sum(axis=2)
            late = lambda m: 100.0 * float((c10[m] * ~w["wet"][m]).sum() / c10[m].sum())
            print("detector, %s: %.0f per cent of the hail storms' tipped water arrives in intervals the detector logs dry, %.1f per cent of the rain storms'; %d hail storms" % (
                d, late(w["hail"]), late(~w["hail"]), int(w["hail"].sum())))
        for d in ("Costarossa", "Rio Scuro"):
            w = W[d]
            lr = np.log(w["opt"].sum(axis=1)[~w["hail"]] / w["rec"].sum(axis=1)[~w["hail"]])
            print("detector, %s: on rain storms its optical storm totals scatter around the tipped totals by a log sd of %.2f (%d storms)" % (d, float(lr.std()), int((~w["hail"]).sum())))
        halves, sides, tops = [], [], []
        for s in names:                      # the crude site ways against their own reverse and their own halves
            w = W[CROSSINGS[s]["depot"]]
            era = w["season"] >= G_SEASONS - R_SEASONS
            a, b = radar(w, 1 + w["pts"].index(s)), radar(w, 0)
            odd, evn = era & (w["season"] % 2 == 1), era & (w["season"] % 2 == 0)
            q = lambda m: float(np.quantile(a[m], 0.9) / np.quantile(b[m], 0.9))
            g = lambda m: float(np.exp(np.log(a[m] / b[m]).mean()))
            halves.append((s, 100.0 * abs(q(odd) / q(evn) - 1.0), 100.0 * abs(g(odd) / g(evn) - 1.0)))
            sides.append((s, float((a[era] * b[era]).sum() / (b[era] ** 2).sum()), float((a[era] ** 2).sum() / (a[era] * b[era]).sum())))
            tb, ta = era & (b >= np.quantile(b[era], 0.75)), era & (a >= np.quantile(a[era], 0.75))
            tops.append((s, float(a[tb].sum() / b[tb].sum()), float(a[ta].sum() / b[ta].sum())))
        print("site, upper deciles unpaired: odd against even seasons differ by " + ", ".join("%s %.1f" % (s.replace("Rio ", ""), x) for s, x, _ in halves) +
              " per cent; the paired mean by " + ", ".join("%.1f" % y for _, _, y in halves))
        print("site, regression through the origin, source on gauge and its reverse: " + ", ".join("%s %.3f and %.3f" % (s.replace("Rio ", ""), x, y) for s, x, y in sides))
        print("site, the largest quarter chosen on the gauge pixel and on the source pixel: " + ", ".join("%s %.3f and %.3f" % (s.replace("Rio ", ""), x, y) for s, x, y in tops))
        era = era_c
        gs = storm_max(wr, minutes(wr, "rate", kap["Rio Scuro"]), "profile")
        print("research valley, source over station (weighing gauges over the station's golden maxima; radar contrast; rainfall normal): " + ", ".join(
            "%s %.2f; %.2f; %.2f" % (s, float(source_max(wr, s)[era].sum() / gs[era].sum()), site_factor(wr, s), RESEARCH[s]["map"]) for s in RESEARCH))
        print("referee (mean of the five largest storms a season, mm; depth reached three times a season, mm; triggering storms seen): "
              "weighing gauges %.2f, %.2f and %.0f; golden %.2f, %.2f and %.0f" % (seen_top, seen_depth, seen_count, rtop(rgold), rdepth(rgold), rcount(rgold)))
        for k, v in {**rivals, **others}.items():
            print("   %-46s %.2f, %.2f and %.0f" % (k, rtop(v), rdepth(v), rcount(v)))
        # forcing: each fitted input moved by a fifth, the classing read again
        cls = lambda v: tuple(int(v[s] >= LOW_LINE) + int(v[s] >= LINE) for s in names)
        cnt = lambda est, s: float((est >= CROSSINGS[s]["T"]).sum()) / G_SEASONS
        dep = lambda s: CROSSINGS[s]["depot"]
        moved = {}
        for fk in (0.8, 1.2):
            xs = {d: storm_max(w, put_back(w["rec"], fk * kap[d], "recip"), "profile") for d, w in W.items()}
            moved["the fitted loss times %.1f" % fk] = {s: cnt(transfer(W[dep(s)], s, xs[dep(s)], "geo"), s) for s in names}
        xs0 = station_maxima(W, "rate", "profile", "recip", "model", 1)[0]
        for pw in (0.8, 1.2):
            moved["each burst factor's distance from one times %.1f" % pw] = {
                s: cnt(site_factor(W[dep(s)], s) ** pw * xs0[dep(s)], s) for s in names}
        for lam in (0.8, 1.2):
            xs = {}
            for d, w in W.items():
                c = put_back(w["rec"], kap[d], "recip")
                a, b = storm_max(w, c, "tips"), storm_max(w, c, "profile")
                xs[d] = a + lam * (b - a)
            moved["the hail storms' put-back times %.1f" % lam] = {s: cnt(transfer(W[dep(s)], s, xs[dep(s)], "geo"), s) for s in names}
        for k, v in moved.items():
            print("forcing, %-46s %s; classing %s" % (k + ":", ", ".join("%s %.2f" % (s.replace("Rio ", ""), v[s]) for s in names),
                                                       "unchanged" if cls(v) == cls(gold) else "MOVED"))
        print("storms on the tip record: " + ", ".join("%s %d (%d with hail or graupel)" % (d, w["N"], int(w["hail"].sum())) for d, w in W.items()))
        print()
    return corelib.run(spec)


if __name__ == "__main__":
    sys.exit(main())
