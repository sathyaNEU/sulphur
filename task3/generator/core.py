#!/usr/bin/env python3
"""task3 architecture 9: the core, proved on the world's own arrays before any pack exists.

The world. A ground handler works the ramp at seven airports of one region. The ramp stands down whenever a
cloud-to-ground stroke falls within 8 km and resumes 15 minutes after the last one, so a season's stand-down is the
length of the union of the 15 minute intervals the strokes open. A station whose expected stand-down in the coming
summer window (1 December 2026 to 31 March 2027) is over 25 hours carries a relief crew. The only record of past
strokes is the national location network's archive, and the network locates a stroke with a chance that rises with
its peak current and with the sensors in range and up that day. Two things a run has to set, each with a default
the network's own process makes false at every station:

  S1  what a season's hours were, given the strokes the network missed. The default is the hours the located
      strokes give (or those hours raised in proportion to the strokes missed, or the missed strokes put back
      around the located ones). Missed strokes shorten a stand-down, split it and erase whole days, the weak ones
      sit at a cell's edges, and the days that left no record are in no file, so hours answer to detection by the
      day's size and shape, never in proportion.
  S3  what a legacy receiver adds to detection. The default is the filed table read at the count of sensors up. A
      legacy receiver adds about a third of a standard sensor, and the days it is in range show it only in how far
      the weak strokes are cut.

One supporting step, next to a closed card and so never the step the call turns on: the bureau's outlook puts the
coming window warm, and the region's storm days answer to the shelf index. Leaving it out (the record's mean
carried forward) moves every figure for the window and leaves the call standing.

Everything a golden constant needs is filed (the timer, the radius, the line, the detection table and its width,
the outlook value) or measured from the located strokes and the sensor log. Arithmetic on arrays: nothing here
reads a prompt.
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

# ------------------------------------------------------------------------------------------------ filed
T_CLEAR = 15.0                     # minutes the ramp stays stood down after the last ground stroke within the radius
LINE = 25.0                        # hours of stand-down in the window above which a station carries a relief crew
X_F = 0.5                          # the bureau's outlook value of the shelf index for the window
SEASONS = np.arange(2002, 2026)    # the season starting 1 December of each year, 2002-03 to 2025-26
INDEX = np.array([+0.6, +1.1, +0.4, +1.3, +0.8, +1.2, +0.9, +0.5,
                  -0.3, +0.2, -0.5, +0.4, -0.1, -0.6, +0.3, +0.0,
                  -0.4, +0.5, -0.2, +0.1, -0.6, +0.3, -0.1, +0.2])    # the bureau's seasonal shelf index
ERA = np.array([0] * 8 + [1] * 8 + [2] * 8)                           # network eras: to 2009-10, to 2017-18, since
NDAY = 121
TABLE_N = np.arange(2, 9)
TABLE_I50 = np.array([26.0, 19.0, 13.0, 9.0, 6.5, 4.8, 3.5])          # kA located half the time, by sensors up
WIDTH = 0.35                                                          # the curve's width in log amplitude

# ------------------------------------------------------------------------------------------------ the world's own
SEED = 3909
KAPPA = 0.30                       # what a legacy receiver adds, in standard sensors
P_OUT = 0.12                       # chance a sensor is down on a day
BETA = 0.45                        # storm days' response to the shelf index, log points per index unit
STRAY = 0.25                       # share of a day's strokes that fall outside its main cell, before or after
PHASE = (0.30, 0.70)               #              # log amplitude at a cell's mature minutes, and its fall to the edge of the cell
GAMMA_SD = 0.06                    # season to season spread of the region's storm days beyond the index
CG_NEG, CG_POS, CG_POS_SHARE = (15.0, 0.70), (22.0, 0.75), 0.10
# name, storm days in a neutral season, median strokes a storm day, standard sensors in range by era, legacy
# receivers in range by era
SITES = [
    ("A", 27.0, 20.0, (1, 6, 7), (4, 1, 0)),
    ("Z", 37.0, 3.0, (2, 3, 3), (0, 0, 0)),
    ("X", 55.0, 1.5, (3, 3, 3), (0, 0, 0)),
    ("V", 41.0, 3.0, (1, 1, 2), (5, 5, 4)),
    ("Y", 18.0, 4.0, (2, 7, 8), (3, 0, 0)),
    ("W", 11.3, 18.0, (1, 3, 3), (3, 0, 0)),
    ("B", 23.5, 5.0, (1, 1, 2), (5, 5, 4)),
]
NAMES = [s[0] for s in SITES]
NS, NT = len(SITES), len(SEASONS)
EDGES = np.array([2, 3, 4, 6, 10, 20, 40])


def i50(L):
    L = np.asarray(L, dtype=float)
    return np.exp(np.interp(L, TABLE_N, np.log(TABLE_I50))
                  + np.where(L < 2, (2 - L) * math.log(TABLE_I50[0] / TABLE_I50[1]), 0.0))


def de(I, L):
    """The filed chance that a stroke of peak current I is located with L sensors up."""
    return 1.0 / (1.0 + np.exp(-(np.log(I) - np.log(i50(L))) / WIDTH))


def day_hours(day, t, ndays):
    """Hours stood down on each day: the union of [t, t + T_CLEAR] over the day's strokes (sorted by day, t)."""
    if len(t) == 0:
        return np.zeros(ndays), np.zeros(ndays, dtype=int)
    gap = np.full(len(t), T_CLEAR)
    same = day[1:] == day[:-1]
    gap[:-1] = np.where(same, np.minimum(t[1:] - t[:-1], T_CLEAR), T_CLEAR)
    return np.bincount(day, weights=gap, minlength=ndays) / 60.0, np.bincount(day, minlength=ndays)


def make_days(rng, K, size_med):
    """K storm days: each day's strokes, their minute of the day, peak current and polarity."""
    N = np.maximum(1, np.ceil(rng.lognormal(math.log(size_med), 1.15, K) - 0.5)).astype(int)
    D = 45.0 * (N / 15.0) ** 0.30 * rng.lognormal(0.0, 0.45, K)
    s0 = rng.uniform(420.0, 1080.0, K)
    d = np.repeat(np.arange(K), N)
    u = rng.beta(1.5, 2.0, len(d))
    stray = rng.random(len(d)) < STRAY
    u = np.where(stray, rng.uniform(-0.6, 1.8, len(d)), u)
    t = s0[d] + D[d] * u
    pos = rng.random(len(d)) < CG_POS_SHARE
    I = np.where(pos, rng.lognormal(math.log(CG_POS[0]), CG_POS[1], len(d)),
                 rng.lognormal(math.log(CG_NEG[0]), CG_NEG[1], len(d)))
    # a cell's strongest strokes come in its mature minutes; the first and the last ones, and the strays, are weak
    I = I * np.exp(PHASE[0] - PHASE[1] * np.minimum(np.abs(u - 0.45) / 0.45, 1.5))
    return N, d, t, I, pos


def build(seed=SEED):
    """The record: every ground stroke within 8 km of a station, whether the network located it, and each
    station-day's sensors in range and up."""
    gam = np.random.default_rng([seed, 99]).gamma(1 / GAMMA_SD ** 2, GAMMA_SD ** 2, NT)
    cols = {k: [] for k in ("day", "t", "I", "pos", "det")}
    cal_std = np.zeros((NS, NT, NDAY), dtype=int)
    cal_leg = np.zeros((NS, NT, NDAY), dtype=int)
    dsite, dseason, dstd, dleg, ddos = [], [], [], [], []
    base = 0
    for si, (name, lam, size, std, leg) in enumerate(SITES):
        rng = np.random.default_rng([seed, si])
        for ti in range(NT):
            e = ERA[ti]
            cal_std[si, ti] = rng.binomial(std[e], 1 - P_OUT, NDAY)
            cal_leg[si, ti] = rng.binomial(leg[e], 1 - P_OUT, NDAY) if leg[e] else 0
            K = min(NDAY, rng.poisson(lam * math.exp(BETA * INDEX[ti]) * gam[ti]))
            which = rng.choice(NDAY, K, replace=False)
            ns, nl = cal_std[si, ti][which], cal_leg[si, ti][which]
            N, d, t, I, pos = make_days(rng, K, size)
            neff = np.maximum(ns + KAPPA * nl, 1.0)[d]
            det = (rng.random(len(d)) < de(I, neff)) & ((ns + nl)[d] >= 2)
            for k, v in zip(("day", "t", "I", "pos", "det"), (d + base, t, I, pos, det)):
                cols[k].append(v)
            dsite += [si] * K
            dseason += [ti] * K
            dstd.append(ns)
            dleg.append(nl)
            ddos.append(which)
            base += K
    W = {k: np.concatenate(v) for k, v in cols.items()}
    o = np.lexsort((W["t"], W["day"]))
    for k in W:
        W[k] = W[k][o]
    W.update(d_site=np.array(dsite), d_season=np.array(dseason), d_std=np.concatenate(dstd),
             d_leg=np.concatenate(dleg), d_dos=np.concatenate(ddos), ndays=base, cal_std=cal_std, cal_leg=cal_leg)
    return W


def expectation(seed=SEED + 1, K=60000):
    """The world's own expectation at each station: hours and ground strokes per storm day."""
    out = {}
    for si, (name, lam, size, std, leg) in enumerate(SITES):
        rng = np.random.default_rng([seed, si])
        N, d, t, I, pos = make_days(rng, K, size)
        o = np.lexsort((t, d))
        H, R = day_hours(d[o], t[o], K)
        out[name] = (H.mean(), N.mean())
    return out


def records(W):
    """What the files hold, and nothing else: the located strokes, each on the station-day it fell (a day is a
    row here only when the network located a stroke on it; a storm day that left none is in no file), that day's
    place in its season, and the sensor log (the standard sensors and legacy receivers up on every station-day)."""
    r = W["det"]
    seen = np.unique(W["day"][r])
    idx = np.full(W["ndays"], -1)
    idx[seen] = np.arange(len(seen))
    d = idx[W["day"][r]]
    return {"day": d, "t": W["t"][r], "I": W["I"][r], "pos": W["pos"][r], "site": W["d_site"][seen][d],
            "season": W["d_season"][seen][d], "ndays": len(seen), "d_site": W["d_site"][seen],
            "d_season": W["d_season"][seen], "d_std": W["d_std"][seen], "d_leg": W["d_leg"][seen],
            "d_dos": W["d_dos"][seen], "cal_std": W["cal_std"], "cal_leg": W["cal_leg"]}


# ------------------------------------------------------------------------------------------------ the golden's parts
GRID = np.linspace(math.log(0.5), math.log(600.0), 400)
DG = GRID[1] - GRID[0]


def npdf(x, m, s):
    return np.exp(-0.5 * ((x - m) / s) ** 2) / (s * 2.5066282746310002)


def curve(L):
    return 1.0 / (1.0 + np.exp(-(GRID - math.log(float(i50(L)))) / WIDTH))


def amp_loglik(x, lev, mu, sg):
    """Log likelihood of located log amplitudes under a lognormal law cut by the filed detection curve."""
    ll = 0.0
    for v in np.unique(lev):
        m = lev == v
        Z = np.sum(npdf(GRID, mu, sg) * curve(v)) * DG
        xx = x[m]
        dd = 1.0 / (1.0 + np.exp(-(xx - math.log(float(i50(v)))) / WIDTH))
        ll += np.sum(np.log(npdf(xx, mu, sg) * dd / Z + 1e-300))
    return ll


def fit_amp_law(R, by_pol=True, min_std=3):
    """The ground strokes' amplitude law, from the days seen by standard sensors only."""
    ok = (R["d_leg"][R["day"]] == 0) & (R["d_std"][R["day"]] >= min_std)
    lev = R["d_std"][R["day"]].astype(float)
    out = {}
    for p in ((False, True) if by_pol else (None,)):
        m = ok if p is None else ok & (R["pos"] == p)
        x, ne = np.log(R["I"][m]), lev[m]
        best = (-1e300, 2.7, 0.7)
        mus, sgs = np.linspace(2.2, 3.6, 15), np.linspace(0.4, 1.1, 15)
        for _ in range(3):
            for mu in mus:
                for sg in sgs:
                    l = amp_loglik(x, ne, mu, sg)
                    if l > best[0]:
                        best = (l, mu, sg)
            dm, ds = (mus[1] - mus[0]), (sgs[1] - sgs[0])
            mus = np.linspace(best[1] - dm, best[1] + dm, 9)
            sgs = np.linspace(max(0.2, best[2] - ds), best[2] + ds, 9)
        out[p] = (best[1], best[2])
    if by_pol:                                  # the share of positive strokes among all ground strokes
        lv, pp = lev[ok], R["pos"][ok]
        wn = wp = 0.0
        for v in np.unique(lv):
            m = lv == v
            wn += np.sum(~pp[m]) / (np.sum(npdf(GRID, *out[False]) * curve(v)) * DG)
            wp += np.sum(pp[m]) / (np.sum(npdf(GRID, *out[True]) * curve(v)) * DG)
        out["share_pos"] = wp / (wp + wn)
    return out


def fit_kappa(R, law, sites=None, step=0.02):
    """What a legacy receiver adds, in standard sensors: the value under which the located amplitudes on the
    days one is in range are cut where the filed curve says."""
    nl = R["d_leg"][R["day"]]
    m = nl >= 1
    if sites is not None:
        m &= np.isin(R["site"], sites)
    x, st, lg, pos = np.log(R["I"][m]), R["d_std"][R["day"]][m], nl[m], R["pos"][m]
    best = (-1e300, 1.0)
    for kap in np.arange(0.0, 1.0 + 1e-9, step):
        ne = np.round(np.maximum(st + kap * lg, 1.0), 1)
        l = 0.0
        for p in ((False, True) if (False in law) else (None,)):
            mm = np.ones(len(x), bool) if p is None else (pos == p)
            l += amp_loglik(x[mm], ne[mm], *law[p])
        if l > best[0]:
            best = (l, kap)
    return float(best[1])


def fit_levels(R, law, kappa, min_strokes=150, step=0.1):
    """The same fit freed of its one number: every pairing of standard sensors and legacy receivers up that holds
    enough located strokes gets its own level, the one under which its amplitudes are cut where the filed curve
    says; a pairing with too few strokes keeps the level the one number gives it."""
    nl, st = R["d_leg"][R["day"]], R["d_std"][R["day"]]
    x, pos = np.log(R["I"]), R["pos"]
    out = {}
    for a, b in sorted(set(zip(st[nl >= 1].tolist(), nl[nl >= 1].tolist()))):
        m = (st == a) & (nl == b)
        if m.sum() < min_strokes:
            continue
        best = (-1e300, max(a + kappa * b, 1.0))
        for L in np.arange(1.0, min(a + b, 8) + 1e-9, step):
            l = 0.0
            for p in ((False, True) if (False in law) else (None,)):
                mm = m if p is None else m & (pos == p)
                l += amp_loglik(x[mm], np.full(mm.sum(), round(L, 1)), *law[p])
            if l > best[0]:
                best = (l, round(float(L), 1))
        out[(a, b)] = best[1]
    return out


def pbar(law, L):
    """Share of ground strokes located at a sensor level, under an amplitude law."""
    c = curve(L)
    if None in law:
        return float(np.sum(npdf(GRID, *law[None]) * c) * DG)
    s = law["share_pos"]
    return float((1 - s) * np.sum(npdf(GRID, *law[False]) * c) * DG + s * np.sum(npdf(GRID, *law[True]) * c) * DG)


def mean_logamp(law, L):
    """Mean log amplitude of the strokes located at a sensor level, under an amplitude law."""
    c = curve(L)
    if None in law:
        f = npdf(GRID, *law[None])
    else:
        s = law["share_pos"]
        f = (1 - s) * npdf(GRID, *law[False]) + s * npdf(GRID, *law[True])
    return float(np.sum(GRID * f * c) / np.sum(f * c))


def cls_of(r, edges):
    return np.searchsorted(edges, r, side="right")


def response(R, lev_day, donor, rng, reps, edges):
    """The timer rule replayed on the best-covered days thinned to each lower sensor level with the filed
    chances: for a day of each true size, the chance of each recorded size (or of leaving no record), and the
    hours a day of each true size carries."""
    nd, nc = R["ndays"], len(edges) + 1
    dn = lev_day[R["day"]]
    k = donor[R["day"]]
    day, t, I, n = R["day"][k], R["t"][k], R["I"][k], dn[k]
    Hd, Rd = day_hours(day, t, nd)
    have = Rd > 0
    cd = cls_of(Rd, edges)
    num, den = np.zeros(nc), np.zeros(nc)       # the donors' own last step, from a second thinning by their chances
    for _ in range(reps):
        kk = rng.random(len(I)) < de(I, n)
        Ht, Rt = day_hours(day[kk], t[kk], nd)
        s = have & (Rt > 0)
        num += np.bincount(cls_of(Rt[s], edges), weights=Hd[s], minlength=nc)
        den += np.bincount(cls_of(Rt[s], edges), weights=Ht[s], minlength=nc)
    top = np.where(den > 0, num / np.maximum(den, 1e-9), 1.0)
    Hfull = Hd * top[cd]
    cnt = np.bincount(cd[have], minlength=nc).astype(float)
    Hbar = np.bincount(cd[have], weights=Hfull[have], minlength=nc) / np.maximum(cnt, 1)
    P = {}
    for L in np.unique(lev_day[~donor]):
        M = np.zeros((nc, nc + 1))
        q = np.minimum(1.0, de(I, np.full(len(I), L)) / de(I, n))
        for _ in range(reps):
            kk = rng.random(len(I)) < q
            Ht, Rt = day_hours(day[kk], t[kk], nd)
            rc = np.where(Rt > 0, cls_of(Rt, edges), nc)
            np.add.at(M, (cd[have], rc[have]), 1.0)
        P[L] = M / np.maximum(M.sum(axis=1, keepdims=True), 1e-9)
    return {"P": P, "Hbar": Hbar, "prior": cnt / cnt.sum(), "top": top}


def unfold(O, P, prior, nc, iters=400, shared=True):
    """True storm days by size at one station, from its recorded days by size at each sensor level."""
    Ls = [L for L in O if O[L].sum() > 0]
    pi = {L: prior.copy() for L in Ls}
    T = {L: O[L].sum() / max(1e-9, float(prior @ P[L][:, :nc].sum(axis=1))) for L in Ls}
    for _ in range(iters):
        tot = np.zeros(nc)
        u = {}
        for L in Ls:
            pred = T[L] * (pi[L] @ P[L][:, :nc])
            ratio = np.where(pred > 0, O[L] / np.maximum(pred, 1e-12), 0.0)
            u[L] = T[L] * pi[L] * (P[L][:, :nc] @ ratio + P[L][:, nc])
            T[L] = u[L].sum()
            tot += u[L]
        for L in Ls:
            pi[L] = (tot / tot.sum()) if shared else (u[L] / max(u[L].sum(), 1e-12))
    return T, pi


def blind_scale(R):
    """One over the share of each station-season's days on which two or more sensors were up."""
    ok = (R["cal_std"] + R["cal_leg"]) >= 2
    return 1.0 / np.maximum(ok.mean(axis=2), 1e-9)


def season_sum(R, v):
    out = np.zeros((NS, NT))
    np.add.at(out, (R["d_site"], R["d_season"]), v)
    return out


def corrected(R, kappa, law, s1=True, donor_n=6, reps=6, seed=11, shared=True, edges=EDGES, iters=400, levmap=None):
    """Season tables at each station: stand-down hours and ground strokes as they occurred."""
    rng = np.random.default_rng(seed)
    nd, nc = R["ndays"], len(edges) + 1
    lev = np.round(np.maximum(R["d_std"] + kappa * R["d_leg"], 1.0), 1)
    if levmap:
        for (a, b), L in levmap.items():
            lev[(R["d_std"] == a) & (R["d_leg"] == b)] = L
    H, C = day_hours(R["day"], R["t"], nd)
    scale = blind_scale(R)
    pb = {L: pbar(law, L) for L in np.unique(lev)}
    St = season_sum(R, C / np.array([pb[L] for L in lev])) * scale
    if not s1:
        return {"H": season_sum(R, H) * scale, "S": St, "lev": lev}
    donor = R["d_std"] >= donor_n               # standard sensors alone give full sight, whatever a legacy adds
    rs = response(R, lev, donor, rng, reps, edges)
    cl = cls_of(C, edges)
    fac = np.where(C > 0, rs["top"][cl], 0.0)
    for si in range(NS):
        ds = (R["d_site"] == si) & (C > 0) & ~donor
        O = {L: np.bincount(cl[ds & (lev == L)], minlength=nc).astype(float) for L in np.unique(lev[ds])}
        if not O:
            continue
        T, pi = unfold(O, rs["P"], rs["prior"], nc, iters=iters, shared=shared)
        for L in T:
            m = ds & (lev == L)
            fac[m] = T[L] * float(pi[L] @ rs["Hbar"]) / max(H[m].sum(), 1e-9)
    return {"H": season_sum(R, H * fac) * scale, "S": St, "lev": lev}


def strong_days(R, thr):
    """Days with a located stroke at or above thr kA, by station and season: strokes that strong are located
    whatever the sensors in range."""
    mx = np.zeros(R["ndays"])
    np.maximum.at(mx, R["day"], R["I"])
    return season_sum(R, (mx >= thr).astype(float)) * blind_scale(R)


def pooled_slope(y, x):
    """One response to the index across the stations, each with its own level (Poisson, by Newton)."""
    b = 0.0
    for _ in range(80):
        e = np.exp(b * x)
        a = y.sum(axis=1) / e.sum()
        mu = np.outer(a, e)
        g = np.sum((y - mu) * x)
        h = np.sum(mu * x * x) - np.sum((mu * x).sum(axis=1) ** 2 / mu.sum(axis=1))
        st = g / h
        b += st
        if abs(st) < 1e-11:
            break
    return float(b), float(1.0 / math.sqrt(h))


def cell_slope(cells):
    """One response across cells that each keep their own level and their own seasons (Poisson, by Newton)."""
    b = 0.0
    for _ in range(80):
        g = h = 0.0
        for y, x in cells:
            e = np.exp(b * x)
            mu = y.sum() / e.sum() * e
            g += np.sum((y - mu) * x)
            h += np.sum(mu * x * x) - np.sum(mu * x) ** 2 / mu.sum()
        st = g / h
        b += st
        if abs(st) < 1e-11:
            break
    return float(b)


def station_slopes(y, x):
    out = []
    for i in range(len(y)):
        out.append(pooled_slope(y[i:i + 1], x))
    return np.array(out)


def state(R, T, thr=60.0, form="pooled", series=None):
    """The region's response to the shelf index, in log points per index unit."""
    x = INDEX[T]
    y = (strong_days(R, thr) if series is None else series)[:, T]
    if form == "pooled":
        return pooled_slope(y, x)[0]
    if form == "groups":                        # warm seasons against the rest, two groups
        w = x >= 0.5
        return float(np.log(y[:, w].sum() / w.sum() / (y[:, ~w].sum() / (~w).sum())) / (x[w].mean() - x[~w].mean()))
    if form == "station_mean":                  # each station's own slope, averaged by its precision
        ss = station_slopes(y, x)
        return float(np.sum(ss[:, 0] / ss[:, 1] ** 2) / np.sum(1 / ss[:, 1] ** 2))
    if form == "line":                          # a straight line: each station's series over its own mean, one slope
        rel, xc = y / y.mean(axis=1, keepdims=True), x - x.mean()
        return float((rel * xc).sum() / (len(rel) * (xc ** 2).sum()))
    raise ValueError(form)


def figures(B, S, beta, line=False):
    """The graded figures. An average season is the mean over the seasons on record; this season is that mean
    carried to the outlook value of the index; the crossing is the season, as a per cent of an average one, at
    which a station's stand-down meets the line (it needs no form for the response, so it is the same figure
    under a straight line and under a constant per cent per index unit, and never leaves the record's range).
    The response is a constant per cent per index unit (the golden), or a straight line in the index (line)."""
    beta = np.broadcast_to(np.asarray(beta, dtype=float), (NS,)).copy()
    if line:
        rel = 1.0 + beta * (X_F - INDEX.mean())
    else:
        rel = np.exp(beta * X_F) / np.exp(np.outer(beta, INDEX)).mean(axis=1)
    cross = 100.0 * LINE / np.maximum(np.asarray(B, dtype=float), 1e-9)
    return {"F": B * rel, "B": np.asarray(B, dtype=float), "S": np.asarray(S, dtype=float), "pct": 100.0 * rel,
            "cross": cross, "beta": beta}


def estimate(R, s1=True, s2=True, s3=True, by_pol=True, kap_sites=None, donor_n=6, thr=60.0, form="pooled",
             seasons=None, reps=6, seed=11, shared=True, law=None, kappa=None, hours_state=False, min_std=3,
             edges=EDGES, iters=400, by_pairing=False, kap_tail=None):
    """The golden estimator and its lattice: each stump made the golden way (True) or the hurried way (False)."""
    T = np.arange(NT) if seasons is None else np.asarray(seasons)
    law = law or fit_amp_law(R, by_pol, min_std)
    if kap_tail is not None and kappa is None:
        kappa = tail_worth(R, law, kap_tail, own_share=True)     # the same parameter from one moment of the amplitudes
    kap = (kappa if kappa is not None else fit_kappa(R, law, kap_sites)) if s3 else 1.0
    tab = corrected(R, kap, law, s1, donor_n, reps, seed, shared, edges, iters,
                    fit_levels(R, law, kap) if (by_pairing and s3) else None)
    beta = state(R, T, thr, form, series=tab["H"] if hours_state else None) if s2 else 0.0
    out = figures(tab["H"].mean(axis=1), tab["S"].mean(axis=1), beta, line=(form == "line"))
    out.update(kappa=kap, tab=tab, law=law, how="replay" if s1 else "none")
    return out


# ------------------------------------------------------------------------------------------------ the other routes
def face_tables(R, cap=1e9):
    """Recorded hours, and strokes weighted by one over the filed chance at the count of sensors up."""
    nd = R["ndays"]
    lev = (R["d_std"] + R["d_leg"]).astype(float)
    H, C = day_hours(R["day"], R["t"], nd)
    w = np.minimum(1.0 / de(R["I"], lev[R["day"]]), cap)
    return H, C, np.bincount(R["day"], weights=w, minlength=nd), lev


def ols(y, X):
    b, *_ = np.linalg.lstsq(X, y, rcond=None)
    return b, y - X @ b


def configs(R):
    """Each station-season's sensors in range (the most seen up on a day of the season), standard and legacy."""
    return R["cal_std"].max(axis=2), R["cal_leg"].max(axis=2)


def route_direct(R):
    """The pack's most direct evidence read raw: the located strokes' own hours, averaged over the record."""
    H, C, Wd, lev = face_tables(R)
    out = figures(season_sum(R, H).mean(axis=1), season_sum(R, C.astype(float)).mean(axis=1), 0.0)
    out.update(kappa=1.0, how="none")
    return out


def config_cells(R, Hs):
    """Each station's seasons under one set of sensors in range, as cells of (season hours, index)."""
    cs, cl = configs(R)
    key = cs * 100 + cl
    cells = []
    for i in range(NS):
        for k in np.unique(key[i]):
            m = key[i] == k
            if m.sum() >= 3 and Hs[i][m].sum() > 0:
                cells.append((Hs[i][m], INDEX[m]))
    return cells, key


def route_rigorous(R):
    """The most rigorous standard design: counts weighted by the filed chances at the sensors up, stand-down hours
    as the located strokes give them, a level for every station under every documented set of sensors in range,
    one response to the season's state fitted within those levels across the stations, the level read on the
    present network."""
    H, C, Wd, lev = face_tables(R)
    sc = blind_scale(R)
    Hs, Ss = season_sum(R, H) * sc, season_sum(R, np.minimum(Wd, 50.0 * C)) * sc
    cells, key = config_cells(R, Hs)
    b = cell_slope(cells)
    mm = np.exp(b * INDEX).mean()
    B, S = np.zeros(NS), np.zeros(NS)
    for i in range(NS):
        now = key[i] == key[i][-1]
        B[i] = Hs[i][now].sum() / np.exp(b * INDEX[now]).sum() * mm
        S[i] = Ss[i][now].sum() / np.exp(b * INDEX[now]).sum() * mm
    out = figures(B, S, b)
    out.update(kappa=1.0, how="none")
    return out


def route_generous(R, law, kappa=1.0, beta=None):
    """Every correction the files suggest at full strength: the amplitude law fitted, each day's strokes and its
    hours raised by one over the share of strokes the filed table locates at the sensors up, the response to the
    season's state fitted on the raised series across the stations. With kappa below 1 a legacy receiver counts
    for that much of a standard sensor; with beta given the season's state is the one handed in."""
    H, C, Wd, lev = face_tables(R)
    if kappa != 1.0:
        lev = np.round(np.maximum(R["d_std"] + kappa * R["d_leg"], 1.0), 1)
    sc = blind_scale(R)
    pb = {L: pbar(law, L) for L in np.unique(lev)}
    f = np.array([1.0 / pb[L] for L in lev])
    Hc, Ss = season_sum(R, H * f) * sc, season_sum(R, C * f) * sc
    b = pooled_slope(Hc, INDEX)[0] if beta is None else beta
    out = figures(Hc.mean(axis=1), Ss.mean(axis=1), b)
    out.update(kappa=kappa, how="prorata", tab_H=Hc)
    return out


def route_imputed(R, law, pad=T_CLEAR, seed=7):
    """The strokes the filed table says were missed, put back: each day's missing count drawn from its located
    count and the share located at the sensors up, their minutes drawn between the day's first and last located
    stroke with the timer's length either side, the timer rule rerun; the response as on the rigorous route."""
    rng = np.random.default_rng(seed)
    H, C, Wd, lev = face_tables(R)
    nd = R["ndays"]
    sc = blind_scale(R)
    pb = {L: pbar(law, L) for L in np.unique(lev)}
    f = np.array([1.0 / pb[L] for L in lev])
    first, last = np.full(nd, np.inf), np.full(nd, -np.inf)
    np.minimum.at(first, R["day"], R["t"])
    np.maximum.at(last, R["day"], R["t"])
    d2 = np.repeat(np.arange(nd), rng.poisson(C * (f - 1.0)))
    t2 = rng.uniform(first[d2] - pad, last[d2] + pad)
    day, t = np.concatenate([R["day"], d2]), np.concatenate([R["t"], t2])
    o = np.lexsort((t, day))
    Hi = day_hours(day[o], t[o], nd)[0]
    Hs, Ss = season_sum(R, Hi) * sc, season_sum(R, C * f) * sc
    b = cell_slope(config_cells(R, season_sum(R, H) * sc)[0])
    out = figures(Hs.mean(axis=1), Ss.mean(axis=1), b)
    out.update(kappa=1.0, how="imputed", tab_H=Hs, day_H=Hi)
    return out


_PB = {}


def pbar_face(n):
    """Share of ground strokes located at a sensor count under the filed table, for a typical amplitude law."""
    if n not in _PB:
        _PB[n] = pbar({None: (math.log(15.0), 0.75)}, float(n))
    return _PB[n]


def route_calibrated(R):
    """End to end on the days a sensor was down: how far recorded hours fall with the filed share of strokes
    located, fitted within each station and network era across its sensor counts, and carried to every station
    by its count."""
    H, C, Wd, lev = face_tables(R)
    sc = blind_scale(R)
    face_cal = R["cal_std"] + R["cal_leg"]
    ys, xs, ws, cells = [], [], [], []
    for i in range(NS):
        for e in range(3):
            T = np.where(ERA == e)[0]
            dm = (R["d_site"] == i) & np.isin(R["d_season"], T)
            for n in np.unique(face_cal[i][T]):
                if n < 2:
                    continue
                ex = (face_cal[i][T] == n).sum()
                h = H[dm & (lev == n)].sum()
                nrec = (dm & (lev == n) & (C > 0)).sum()
                if ex >= 20 and nrec >= 5:
                    ys.append(math.log(h / ex))
                    xs.append(math.log(pbar_face(int(n))))
                    ws.append(nrec)
                    cells.append(i * 3 + e)
    ys, xs, ws, cells = map(np.array, (ys, xs, ws, cells))
    for c in np.unique(cells):
        m = cells == c
        ys[m] -= np.average(ys[m], weights=ws[m])
        xs[m] -= np.average(xs[m], weights=ws[m])
    gamma = float(np.sum(ws * xs * ys) / np.sum(ws * xs * xs))
    f = np.array([pbar_face(int(min(max(l, 2), 8))) ** (-gamma) for l in lev])
    Hs, Ss = season_sum(R, H * f) * sc, season_sum(R, C / np.array([pbar_face(int(min(max(l, 2), 8))) for l in lev])) * sc
    b = pooled_slope(Hs, INDEX)[0]
    out = figures(Hs.mean(axis=1), Ss.mean(axis=1), b)
    out.update(kappa=1.0, how="power", gamma=gamma, tab_H=Hs)
    return out


def route_flat(R, law, kappa=1.0, donor_n=6, reps=6, seed=21, max_located=None, donors=None, beta=None):
    """End to end on the days the full network saw: those days thinned by the filed chances to each lower sensor
    count, the timer rerun, the share of their hours that is left read off count by count, and every station's
    recorded hours divided by the share at its count; strokes raised by the filed share located; the response
    fitted on the corrected hours. With kappa at 1 the sensors are counted as the log lists them. The family a run
    can choose from: max_located keeps only the well-covered days with at most that many located strokes (a run
    matching its calibration days to the thin stations' small storms), donors keeps the well-covered days of one
    station or one era (a boolean per day), and beta hands in a season's state in place of the route's own."""
    rng = np.random.default_rng(seed)
    nd = R["ndays"]
    lev = np.round(np.maximum(R["d_std"] + kappa * R["d_leg"], 1.0), 1)
    H, C = day_hours(R["day"], R["t"], nd)
    sc = blind_scale(R)
    donor = lev >= donor_n
    use = donor.copy()
    if max_located is not None:
        use &= C <= max_located
    if donors is not None:
        use &= donors
    k = use[R["day"]]
    day, t, I, n = R["day"][k], R["t"][k], R["I"][k], lev[R["day"]][k]
    Hd = day_hours(day, t, nd)[0].sum()
    r, fac = {}, np.ones(nd)
    for L in np.unique(lev[~donor]):
        q = np.minimum(1.0, de(I, np.full(len(I), L)) / de(I, n))
        tot = 0.0
        for _ in range(reps):
            kk = rng.random(len(I)) < q
            tot += day_hours(day[kk], t[kk], nd)[0].sum()
        r[float(L)] = tot / reps / Hd
        fac[lev == L] = 1.0 / r[float(L)]
    pb = {L: pbar(law, L) for L in np.unique(lev)}
    Hs = season_sum(R, H * fac) * sc
    Ss = season_sum(R, C / np.array([pb[L] for L in lev])) * sc
    b = pooled_slope(Hs, INDEX)[0] if beta is None else beta
    out = figures(Hs.mean(axis=1), Ss.mean(axis=1), b)
    out.update(kappa=kappa, how="flat", tab_H=Hs, r=r, cut=max_located)
    return out


def route_sizemix(R, law, kappa, beta, donor_n=6, reps=6, seed=23):
    """The calibration matched to each station's recorded size mix: the well-covered days thinned to each sensor
    count, and for the days left in each size class as recorded after thinning, the hours they carried on the full
    network over the hours left; every recorded day is raised by the ratio of its own size class at its own
    count. It is the replay read by recorded size without the days that left no record."""
    rng = np.random.default_rng(seed)
    nd, nc = R["ndays"], len(EDGES) + 1
    lev = np.round(np.maximum(R["d_std"] + kappa * R["d_leg"], 1.0), 1)
    H, C = day_hours(R["day"], R["t"], nd)
    sc = blind_scale(R)
    donor = lev >= donor_n
    k = donor[R["day"]]
    day, t, I, n = R["day"][k], R["t"][k], R["I"][k], lev[R["day"]][k]
    Hd = day_hours(day, t, nd)[0]
    fac = np.ones(nd)
    for L in np.unique(lev[~donor]):
        q = np.minimum(1.0, de(I, np.full(len(I), L)) / de(I, n))
        num, den = np.zeros(nc), np.zeros(nc)
        for _ in range(reps):
            kk = rng.random(len(I)) < q
            Ht, Rt = day_hours(day[kk], t[kk], nd)
            s = Rt > 0
            cl = cls_of(Rt[s], EDGES)
            num += np.bincount(cl, weights=Hd[s], minlength=nc)
            den += np.bincount(cl, weights=Ht[s], minlength=nc)
        ratio = np.where(den > 0, num / np.maximum(den, 1e-9), 1.0)
        m = (lev == L) & ~donor
        fac[m] = ratio[cls_of(C[m], EDGES)]
    pb = {L: pbar(law, L) for L in np.unique(lev)}
    Hs = season_sum(R, H * fac) * sc
    Ss = season_sum(R, C / np.array([pb[L] for L in lev])) * sc
    out = figures(Hs.mean(axis=1), Ss.mean(axis=1), beta)
    out.update(kappa=kappa, how="sizemix", tab_H=Hs)
    return out


def tail_worth(R, law, thr=60.0, step=0.01, own_share=False):
    """The legacy receivers' worth a run reads off the strong strokes: on the days a legacy receiver was in range,
    the located strokes of thr kA and over divided by the fitted law's share above thr stand for the ground strokes,
    and the worth is the one at which the located strokes over the filed share located give the same count. With
    own_share the strong strokes are themselves divided by the share of them the filed table locates at the day's
    level, which is the same fit as the golden's from one moment of the amplitudes."""
    nd = R["ndays"]
    C = np.bincount(R["day"], minlength=nd).astype(float)
    strong = np.bincount(R["day"], weights=(R["I"] >= thr).astype(float), minlength=nd)
    leg = R["d_leg"] > 0
    tail = GRID >= math.log(thr)
    dens = (1 - law["share_pos"]) * npdf(GRID, *law[False]) + law["share_pos"] * npdf(GRID, *law[True])
    p_tail = float(np.sum(dens * tail) * DG)
    best = None
    for w in np.arange(0.0, 1.0 + 1e-9, step):
        lev = np.round(np.maximum(R["d_std"][leg] + w * R["d_leg"][leg], 1.0), 1)
        pb = {L: pbar(law, L) for L in np.unique(lev)}
        tot = float(np.sum(C[leg] / np.array([pb[L] for L in lev])))
        if own_share:
            q = {L: float(np.sum(dens * tail * curve(L)) * DG) / p_tail for L in np.unique(lev)}
            target = float(np.sum(strong[leg] / np.array([q[L] for L in lev]))) / p_tail
        else:
            target = strong[leg].sum() / p_tail
        if best is None or abs(tot - target) < best[0]:
            best = (abs(tot - target), float(w))
    return best[1]


def route_cutoff(R, since=16, warm=0.3):
    """A subset where a model is needed: the seasons on the present network only, and among them the warm ones
    as the window's analogues."""
    H, C, Wd, lev = face_tables(R)
    sc = blind_scale(R)
    Hs, Ss = season_sum(R, H) * sc, season_sum(R, np.minimum(Wd, 50.0 * C)) * sc
    T = np.arange(since, NT)
    an = T[INDEX[T] >= warm]
    B, F = Hs[:, T].mean(axis=1), Hs[:, an].mean(axis=1)
    out = figures(B, Ss[:, T].mean(axis=1), 0.0)
    out["F"], out["pct"] = F, 100.0 * F / np.maximum(B, 1e-9)
    out.update(kappa=1.0, how="none")
    return out


# ------------------------------------------------------------------------------------------------ falsification
def replay_test(R, law, m, levels=(2.0, 3.0), small=6, reps=8, seed=17, edges=EDGES, size=None):
    """The stations' own well-covered days as an experiment. The days six or more standard sensors saw are thinned
    by the filed chances to two and to three sensors, a route's correction is applied to what is left, and the
    result is set against the hours those days carried on the full network. Read on the days of fewer than six
    located strokes, the size the thin stations' days run to, in two folds: whatever a route fits, it fits on the
    days that fall on an even day of their season and is tested on the odd ones, and the other way round. Returns the mean absolute
    log miss over the two counts. With size=(lo, hi) the test days are the well-covered days that carried lo to hi
    located strokes on the full network (the test read by day size); a flat route that calibrates on the days of at
    most m["cut"] located strokes fits on those days of the other fold."""
    rng = np.random.default_rng(seed)
    nd, nc = R["ndays"], len(edges) + 1
    how = m["how"]
    lev = np.round(np.maximum(R["d_std"] + m["kappa"] * R["d_leg"], 1.0), 1)
    donor = R["d_std"] >= 6
    k = donor[R["day"]]
    day, t, I, n = R["day"][k], R["t"][k], R["I"][k], lev[R["day"]][k]
    Hd, Cd = day_hours(day, t, nd)
    pbn = {L: pbar(law, L) for L in np.unique(lev[donor])}
    pb_day = np.array([pbn.get(L, 1.0) for L in lev])
    cd = cls_of(Cd, edges)
    out = []
    for L in levels:
        q = np.minimum(1.0, de(I, np.full(len(I), L)) / de(I, n))
        est, truth = 0.0, 0.0
        for par in (1, 0):
            odd = R["d_dos"] % 2 == par             # the day's place in its season, odd or even
            fit, test = donor & ~odd & (Cd > 0), donor & odd & (Cd > 0) & (Cd < small)
            if size is not None:
                test = donor & odd & (Cd >= size[0]) & (Cd <= size[1])
            fitc = fit & (Cd <= m["cut"]) if m.get("cut") else fit
            truth += Hd[test].sum()
            cnt = np.bincount(cd[fit], minlength=nc).astype(float)
            Hbar = np.bincount(cd[fit], weights=Hd[fit], minlength=nc) / np.maximum(cnt, 1)
            if how == "replay":                 # the response from the other fold alone
                M = np.zeros((nc, nc + 1))
                for _ in range(reps):
                    kk = rng.random(len(I)) < q
                    Rt = day_hours(day[kk], t[kk], nd)[1]
                    rc = np.where(Rt > 0, cls_of(Rt, edges), nc)
                    np.add.at(M, (cd[fit], rc[fit]), 1.0)
                P = {L: M / np.maximum(M.sum(axis=1, keepdims=True), 1e-9)}
            for _ in range(reps):
                kk = rng.random(len(I)) < q
                dk, tk = day[kk], t[kk]
                Ht, Ct = day_hours(dk, tk, nd)
                if how == "none":
                    e = Ht[test].sum()
                elif how == "prorata":
                    e = (Ht[test] * pb_day[test]).sum() / pbar(law, L)
                elif how == "power":
                    e = (Ht[test] * (np.array([pbar_face(int(min(max(x, 2), 8))) for x in lev[test]])
                                     / pbar_face(int(L))) ** m["gamma"]).sum()
                elif how == "flat":
                    e = Ht[test].sum() / (Ht[fitc].sum() / Hd[fitc].sum())
                elif how == "imputed":
                    first, last = np.full(nd, np.inf), np.full(nd, -np.inf)
                    np.minimum.at(first, dk, tk)
                    np.maximum.at(last, dk, tk)
                    add = np.where(test & (Ct > 0), Ct * (pb_day / pbar(law, L) - 1.0), 0.0)
                    d2 = np.repeat(np.arange(nd), rng.poisson(add))
                    t2 = rng.uniform(first[d2] - T_CLEAR, last[d2] + T_CLEAR)
                    dd, tt = np.concatenate([dk, d2]), np.concatenate([tk, t2])
                    o = np.lexsort((tt, dd))
                    e = day_hours(dd[o], tt[o], nd)[0][test].sum()
                else:
                    s_ = test & (Ct > 0)
                    O = {L: np.bincount(cls_of(Ct[s_], edges), minlength=nc).astype(float)}
                    T, pi = unfold(O, P, cnt / cnt.sum(), nc, iters=m.get("iters", 400), shared=m.get("shared", True))
                    e = T[L] * float(pi[L] @ Hbar)
                est += e / reps
        out.append(abs(math.log(est / truth)))
    return float(np.mean(out))


def replay_counts(R, law, kappa, levels=(2.0, 3.0), reps=8, seed=19, cap=50.0):
    """The same experiment for the stroke counts: the well-covered days thinned to two and to three sensors, and
    the count the full network located recovered two ways, as the count left over the share the fitted amplitude
    law puts at that sensor count, and as the strokes left weighted by one over their own filed chance (capped).
    Returns the two ratios to the full network's count, per sensor count."""
    rng = np.random.default_rng(seed)
    lev = np.round(np.maximum(R["d_std"] + kappa * R["d_leg"], 1.0), 1)
    donor = R["d_std"] >= 6
    k = donor[R["day"]]
    I, n = R["I"][k], lev[R["day"]][k]
    pbn = {L: pbar(law, L) for L in np.unique(n)}
    full = float(np.sum([1.0 / pbn[L] for L in n]))        # the donors' own count, raised by their own share
    out = []
    for L in levels:
        q = de(I, np.full(len(I), L)) / de(I, n)
        a = b = 0.0
        for _ in range(reps):
            kk = rng.random(len(I)) < np.minimum(1.0, q)
            a += kk.sum() / pbar(law, L)
            b += np.minimum(1.0 / de(I[kk], np.full(kk.sum(), L)), cap).sum()
        out.append((a / reps / full, b / reps / full))
    return out


def falsify(R, m, law, reps=8, seed=5):
    """Three statistics of the stations' own located strokes and sensor log, each the log of what the record
    shows over what a route's own assumptions predict:
      K1  the replay test: the well-covered days thinned to two and three sensors, the route's correction
          applied, against the hours those days carried on the full network (replay_test), read by the day's
          size on the full network in four classes (SIZES), the largest of the four misses: a correction that
          is right for days of one size and wrong for another fails it, whichever days it was fitted on;
      K2  the amplitude of the strokes located on the days a legacy receiver was in range;
      K3  the response to the index of the strokes of 60 kA and over, which every network in the record locates,
          against the response the route carries to the window and against the response its own corrected
          season hours show (the larger miss), in log points of the window's figure.
    The score is the root mean square of the three misses, in log points. A fourth statistic is printed beside
    them and kept out of the score for its sampling error: recorded stand-down hours on the days a standard
    sensor was down against the days all were up, at the thin stations themselves (K4, without and with legacy
    receivers in range); a few hundred outage days carry a sampling error as large as the routes' differences,
    so it rules on nothing and no route is scored on it.
    No file observes a true stroke count, a true hour or a legacy receiver's worth."""
    rng = np.random.default_rng(seed)
    nd = R["ndays"]
    kap, how = m["kappa"], m["how"]
    H, C = day_hours(R["day"], R["t"], nd)
    cs, cl = configs(R)
    obs = {0: 0.0, 1: 0.0}
    pred = {0: 0.0, 1: 0.0}
    for i in range(NS):
        for e in range(3):
            T = np.where(ERA == e)[0]
            s0, l0 = int(cs[i][T].max()), int(cl[i][T].max())
            if s0 > 3 or s0 < 1 or s0 - 1 + l0 < 2:
                continue
            dm = (R["d_site"] == i) & np.isin(R["d_season"], T) & (R["d_leg"] == l0)
            up, dn = dm & (R["d_std"] == s0), dm & (R["d_std"] == s0 - 1)
            calm = R["cal_leg"][i][T] == l0
            e_up = (calm & (R["cal_std"][i][T] == s0)).sum()
            e_dn = (calm & (R["cal_std"][i][T] == s0 - 1)).sum()
            if not e_up or not e_dn or H[up].sum() <= 0:
                continue
            L_up, L_dn = max(s0 + kap * l0, 1.0), max(s0 - 1 + kap * l0, 1.0)
            k = up[R["day"]]
            day, t, I = R["day"][k], R["t"][k], R["I"][k]
            if how == "none":
                ratio = 1.0
            elif how == "prorata":
                ratio = float(np.mean(de(I, L_dn) / de(I, L_up)))
            elif how == "imputed":
                ratio = m["day_H"][up].sum() / H[up].sum() * H[dn].sum() / max(m["day_H"][dn].sum(), 1e-9)
            elif how == "power":
                ratio = (pbar_face(int(max(s0 - 1 + l0, 2))) / pbar_face(int(min(s0 + l0, 8)))) ** m["gamma"]
            elif how == "flat":
                near = lambda x: m["r"][min(m["r"], key=lambda z: abs(z - x))]
                ratio = near(L_dn) / (near(L_up) if L_up < 6 else 1.0)
            else:
                q = np.minimum(1.0, de(I, np.full(len(I), L_dn)) / de(I, np.full(len(I), L_up)))
                tot = 0.0
                for _ in range(reps):
                    kk = rng.random(len(I)) < q
                    tot += day_hours(day[kk], t[kk], nd)[0].sum()
                ratio = tot / reps / H[up].sum()
            g = 1 if l0 > 0 else 0
            obs[g] += H[dn].sum()
            pred[g] += e_dn * H[up].sum() / e_up * ratio
    k4 = (abs(math.log(obs[0] / pred[0])), abs(math.log(obs[1] / pred[1])))
    k1 = max(replay_test(R, law, m, size=sz) for sz in SIZES)      # read by day size, the largest class miss
    lg = R["d_leg"][R["day"]] >= 1
    lev = np.round(np.maximum(R["d_std"] + kap * R["d_leg"], 1.0), 1)[R["day"]][lg]
    ml = {L: mean_logamp(law, L) for L in np.unique(lev)}
    k2 = abs(float(np.mean(np.log(R["I"][lg]))) - float(np.mean([ml[L] for L in lev])))
    bs = pooled_slope(strong_days(R, 60.0), INDEX)[0]
    k3a = abs(float(np.mean(m["beta"])) - bs) * (X_F - INDEX.mean())
    k3b = abs(pooled_slope(m["tab_H"], INDEX)[0] - bs) * (X_F - INDEX.mean())
    k3 = max(k3a, k3b)
    return {"K1": k1, "K2": k2, "K3": k3, "score": math.sqrt((k1 ** 2 + k2 ** 2 + k3 ** 2) / 3.0),
            "parts": (k4[0], k4[1], k3a, k3b)}


# ------------------------------------------------------------------------------------------------ the core
BATTERY = [
    ("as filed", {}),
    ("one amplitude law for both polarities", {"by_pol": False}),
    ("amplitude law from days with four or more standard sensors", {"min_std": 4}),
    ("amplitude law from days with two or more standard sensors", {"min_std": 2}),
    ("amplitude law from days with six or more standard sensors", {"min_std": 6}),
    ("legacy worth fitted at V alone", {"kap_sites": [3]}),
    ("legacy worth fitted without V", {"kap_sites": [0, 4, 5]}),
    ("a level of its own for every pairing of standard sensors and legacy receivers up", {"by_pairing": True}),
    ("legacy worth from the count of strokes of 60 kA and over, their own share located allowed for", {"kap_tail": 60.0}),
    ("replay donors: seven or more standard sensors", {"donor_n": 7}),
    ("replay seed 12", {"seed": 12}),
    ("replay seed 13", {"seed": 13}),
    ("replay with twelve thinnings a level", {"reps": 12}),
    ("day sizes unfolded level by level", {"shared": False}),
    ("day sizes taken in one step from the well-covered days' own mix", {"shared": False, "iters": 1}),
    ("day sizes taken in three steps", {"iters": 3}),
    ("coarser day-size classes", {"edges": np.array([2, 4, 8, 16, 32])}),
    ("finer day-size classes", {"edges": np.array([2, 3, 4, 5, 7, 10, 15, 25, 50])}),
    ("strong strokes from 50 kA", {"thr": 50.0}),
    ("strong strokes from 75 kA", {"thr": 75.0}),
    ("state as warm seasons against the rest", {"form": "groups"}),
    ("state as the stations' own slopes, precision weighted", {"form": "station_mean"}),
    ("state fitted without the first two seasons", {"seasons": np.arange(2, NT)}),
    ("state fitted without the last two seasons", {"seasons": np.arange(0, NT - 2)}),
    ("state fitted on the corrected hours", {"hours_state": True}),
    ("state as a straight line in the index, on the strong strokes", {"form": "line"}),
    ("state as a straight line in the index, on the corrected hours", {"form": "line", "hours_state": True}),
]
FAMS = ("F", "B", "S", "pct", "cross")
CUTS = (2, 3, 4, 5, 6, 7, 8, 10, 12, 15, 20, 30)                 # the most located strokes a calibration day may carry
TAILS = (40.0, 60.0, 80.0)                             # kA: where a run puts the strong strokes' threshold
SWEEP = (0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 1.0)       # the legacy worth swept on the golden
SIZES = ((1, 2), (3, 5), (6, 19), (20, 10 ** 9))       # located strokes on the full network: the replay test's classes
GROUPS = {"g1": ["A", "X", "B"], "g2": ["Z", "V"], "g3": ["Y", "W"]}


def main():
    W = build()
    R = records(W)
    ex = expectation()
    lam = np.array([s[1] for s in SITES])
    mm = float(np.exp(BETA * INDEX).mean())
    t_h = np.array([ex[n][0] for n in NAMES])
    truth = {"F": lam * t_h * math.exp(BETA * X_F), "B": lam * t_h * mm,
             "S": lam * np.array([ex[n][1] for n in NAMES]) * mm, "pct": np.full(NS, 100 * math.exp(BETA * X_F) / mm)}
    truth["cross"] = 100.0 * LINE / truth["B"]

    law = fit_amp_law(R)
    g = estimate(R, law=law)
    kap = g["kappa"]
    lat = {}
    for key, kw in (("S1", dict(s1=False)), ("S3", dict(s3=False)), ("S1+S3", dict(s1=False, s3=False))):
        lat[key] = estimate(R, law=law, kappa=kap if kw.get("s3", True) else None, **kw)
    fam = [estimate(R, **kw) for _, kw in BATTERY]
    routes = {"direct": route_direct(R), "rigorous": route_rigorous(R), "generous": route_generous(R, law),
              "calibrated": route_flat(R, law, kappa=1.0), "cutoff": route_cutoff(R), "imputed": route_imputed(R, law),
              # two more a run can build: the hours' fall on the outage days as one elasticity, and the calibration on
              # the well-covered days with the legacy receivers' worth fitted (S3 made, S1 half made)
              "outage": route_calibrated(R), "flat": route_flat(R, law, kappa=kap)}
    # the hedge: every signal noticed and kept as a sensitivity, the located strokes' hours and the record's mean central
    routes["hedge"] = estimate(R, law=law, s1=False, s2=False, s3=False)
    # the supporting step left out alone: the golden's corrected record, its mean carried to the window
    routes["mean"] = estimate(R, law=law, kappa=kap, s2=False)

    gb = g["beta"]
    crew = lambda F: "".join(n for n, v in zip(NAMES, F) if v > LINE) or "none"
    # each stump's over-corrected side: the stump alone pushed past its fitted value to the far end a run might
    # set (hours raised in proportion; a legacy receiver worth nothing), everything else the golden's
    over = {"S1": route_generous(R, law, kappa=kap, beta=gb), "S3": estimate(R, law=law, kappa=0.0)}
    # the families a run can choose from, every setting with the season's state made the golden way: the cut on
    # the calibration days' size at the fitted worth and with the legacy receivers as listed, the calibration days
    # of one station or one era, the calibration matched to the recorded size mix, the worth read off the strong
    # strokes
    family = {}
    for k in CUTS:
        family["cutoff:k%d" % k] = route_flat(R, law, kappa=kap, max_located=k, beta=gb)
        family["cutoff:k%d, legacy as listed" % k] = route_flat(R, law, kappa=1.0, max_located=k, beta=gb)
        for n_, sd in ((2, 31), (3, 41)):         # the route's own thinning redrawn: the cut is wrong by more than its draw
            family["cutoff:k%d, thinning draw %d" % (k, n_)] = route_flat(R, law, kappa=kap, max_located=k, beta=gb, seed=sd)
    for si in range(NS):
        if ((R["d_std"] >= 6) & (R["d_site"] == si)).sum() >= 30:
            family["calibrated:donors %s" % NAMES[si]] = route_flat(R, law, kappa=kap, donors=R["d_site"] == si, beta=gb)
    for e, nm in ((1, "2010-11 to 2017-18"), (2, "since 2018-19")):
        family["calibrated:donors %s" % nm] = route_flat(R, law, kappa=kap, donors=ERA[R["d_season"]] == e, beta=gb)
    family["calibrated:size mix"] = route_sizemix(R, law, kap, gb)
    family["calibrated:size mix, legacy as listed"] = route_sizemix(R, law, 1.0, gb)
    tw = {thr: tail_worth(R, law, thr) for thr in TAILS}
    family["generous:tail-worth"] = route_generous(R, law, kappa=tw[60.0], beta=gb)
    tail_g = {thr: estimate(R, law=law, kappa=w) for thr, w in tw.items()}
    tw_own = {thr: tail_worth(R, law, thr, own_share=True) for thr in TAILS}
    tail_own = {thr: estimate(R, law=law, kappa=w) for thr, w in tw_own.items()}
    sweep = {w: estimate(R, law=law, kappa=w) for w in SWEEP}

    # the falsification check, with each stump left out alone and in pairs
    def model(o, tab_H=None):
        return {"kappa": o["kappa"], "how": o["how"], "beta": o["beta"], "gamma": o.get("gamma"), "day_H": o.get("day_H"),
                "r": o.get("r"), "cut": o.get("cut"), "tab_H": o["tab"]["H"] if tab_H is None else tab_H}
    fal = {"golden": falsify(R, model(g), law)}
    for key in lat:
        fal[key] = falsify(R, model(lat[key]), law)
    for nm in ("rigorous", "generous", "calibrated", "imputed", "outage", "flat"):
        o = routes[nm]
        fal[nm] = falsify(R, model(o, o.get("tab_H", season_sum(R, face_tables(R)[0]) * blind_scale(R))), law)
    for nm in ("hedge", "mean"):
        fal[nm] = falsify(R, model(routes[nm]), law)
    for k in CUTS:                                 # the cut-off family at the fitted worth, scored like any rival
        o = family["cutoff:k%d" % k]
        fal["cut k%d" % k] = falsify(R, model(o, o["tab_H"]), law)
    one = estimate(R, law=law, kappa=kap, shared=False, iters=1)
    fal_one = falsify(R, dict(model(one), iters=1, shared=False), law)

    np.set_printoptions(linewidth=200, suppress=True)
    Ht = season_sum(W, day_hours(W["day"], W["t"], W["ndays"])[0]).mean(axis=1)
    print("realised average-season hours ", "  ".join("%6.1f" % v for v in Ht), " | strokes",
          " ".join("%5.0f" % v for v in season_sum(W, np.bincount(W["day"], minlength=W["ndays"]).astype(float)).mean(axis=1)))
    for (nm, kw), f in zip(BATTERY, fam):
        print("  battery %-58s F %s | pct %5.1f | k %.2f" % (nm, " ".join("%5.1f" % v for v in f["F"]), f["pct"][0], f["kappa"]))
    print("located %d of %d ground strokes on %d storm days; legacy worth fitted %.2f (world %.2f); response "
          "fitted %.3f (world %.2f)" % (len(R["t"]), len(W["t"]), W["ndays"], kap, KAPPA, g["beta"][0], BETA))
    # the record's own counts, for the note and the build (nothing here is an estimate)
    site_w = W["d_site"][W["day"]]
    print("storm days %d, %d with a located stroke and %d with none; share of ground strokes located by station %s; located by station %s" % (
        W["ndays"], R["ndays"], W["ndays"] - R["ndays"], " ".join("%.2f" % W["det"][site_w == i].mean() for i in range(NS)),
        " ".join("%d" % W["det"][site_w == i].sum() for i in range(NS))))
    don_ = R["d_std"] >= 6
    leg_ = (R["d_leg"] > 0)[R["day"]]
    print("well-covered storm days (six or more standard sensors up) %d, by station %s; located strokes on days a legacy receiver was up %d; located strokes of 60 kA and over %d" % (
        don_.sum(), " ".join("%d" % (don_ & (R["d_site"] == i)).sum() for i in range(NS)), leg_.sum(), (R["I"] >= 60).sum()))
    for n_ in ("V", "B"):
        i_ = NAMES.index(n_)
        thin_ = ((R["d_site"] == i_) & (R["d_std"] <= 1))[R["day"]]
        print("%s: %d located strokes, %d of them on days with one standard sensor or none up" % (n_, (R["site"] == i_).sum(), thin_.sum()))
    hm = lambda x: "%02d:%02d" % (int(x) // 60, int(x) % 60)
    print("local time of day: every ground stroke between %s and %s, the located ones between %s and %s; %d located strokes fall before 09:30" % (
        hm(W["t"].min()), hm(W["t"].max()), hm(R["t"].min()), hm(R["t"].max()), (R["t"] < 570).sum()))
    print("sensors in the register %d; station-days with fewer than two sensors up by station %s of %d" % (
        sum(max(s_) + max(l_) for _, _, _, s_, l_ in SITES), " ".join("%d" % ((W["cal_std"][i] + W["cal_leg"][i]) < 2).sum() for i in range(NS)), NT * NDAY))
    Hrec = day_hours(R["day"], R["t"], R["ndays"])[0]
    cs_, cl_ = configs(R)
    od = [0.0, 0.0, 0]
    for i in range(NS):
        for e_ in range(3):
            T_ = np.where(ERA == e_)[0]
            s0, l0 = int(cs_[i][T_].max()), int(cl_[i][T_].max())
            if l0 > 0 or s0 > 3 or s0 < 1 or s0 - 1 < 2:
                continue
            dn_ = (R["d_site"] == i) & np.isin(R["d_season"], T_) & (R["d_leg"] == 0) & (R["d_std"] == s0 - 1)
            od[0] += Hrec[dn_].sum(); od[1] += (Hrec[dn_] ** 2).sum(); od[2] += int(dn_.sum())
    print("K4 without legacy receivers rests on %d outage days with a located stroke; the sampling error of their hours is %.2f in log points" % (
        od[2], math.sqrt(od[1]) / od[0]))
    print("an average season read as a season at the index's mean value would put this season at %.1f per cent of it (%.1f as filed)" % (
        100.0 * math.exp(float(g["beta"][0]) * (X_F - INDEX.mean())), g["pct"][0]))
    print("stations          ", "  ".join("%6s" % n for n in NAMES))
    for nm, o in [("truth", truth), ("golden", g), ("S1 lost", lat["S1"]), ("S3 lost", lat["S3"]), ("both lost", lat["S1+S3"]),
                  ("record's mean", routes["mean"])] + [(k, routes[k]) for k in ("direct", "rigorous", "generous", "calibrated", "hedge", "cutoff", "imputed", "outage", "flat")]:
        print("%-12s F    " % nm, "  ".join("%6.1f" % v for v in o["F"]), " | pct", " ".join("%4.0f" % v for v in o["pct"]))
        print("%-12s B    " % "", "  ".join("%6.1f" % v for v in o["B"]), " | S", " ".join("%5.0f" % v for v in o["S"]),
              " | cross", " ".join("%5.0f" % v for v in o["cross"]))
    print("average-season hours against the golden's:  located strokes at face value %s | raised in proportion %s | "
          "missed strokes put back %s | one share of hours kept at each sensor count, legacy fitted %s | legacy receivers "
          "at face value %s | the golden against the world's realised %s" % tuple(
              " ".join("%.2f" % v for v in x) for x in (lat["S1"]["B"] / g["B"], routes["generous"]["B"] / g["B"],
                                                       routes["imputed"]["B"] / g["B"], routes["flat"]["B"] / g["B"],
                                                       lat["S3"]["B"] / g["B"], g["B"] / Ht)))
    print("\nfalsification (log points; K1 the replay test on the well-covered days read by day size, the largest class miss, K2 amplitudes under legacy receivers, "
          "K3 the strong strokes' response against the route's carried and corrected ones; K4, beside the score, hours "
          "on the thin stations' own outage days without and with legacy receivers in range)")
    for k, v in list(fal.items()) + [("one step", fal_one)]:
        print("  %-10s K1 %.3f  K2 %.3f  K3 %.3f  score %.3f  (%.1f times the golden's)   K4 %.3f %.3f" % (
            k, v["K1"], v["K2"], v["K3"], v["score"], v["score"] / fal["golden"]["score"], v["parts"][0], v["parts"][1]))

    print("\neach stump over-corrected alone, everything else the golden's (expected hours, the crews it files)")
    print("  S1 hours raised in proportion, legacy worth fitted  %s | %s" % (
        " ".join("%5.1f" % v for v in over["S1"]["F"]), crew(over["S1"]["F"])))
    print("  S3 a legacy receiver worth nothing                  %s | %s" % (
        " ".join("%5.1f" % v for v in over["S3"]["F"]), crew(over["S3"]["F"])))
    print("the legacy worth swept on the golden (worth, expected hours, the crews it files, V's average-season strokes)")
    for w in SWEEP:
        print("  worth %.2f  %s | %-6s | S_V %4.0f" % (w, " ".join("%5.1f" % v for v in sweep[w]["F"]), crew(sweep[w]["F"]),
                                                       sweep[w]["S"][NAMES.index("V")]))
    print("the worth read off the strong strokes, with the golden's replay (threshold, worth, expected hours, crews, S_V)")
    for thr in TAILS:
        o = tail_g[thr]
        print("  %2.0f kA and over  worth %.2f  %s | %-6s | S_V %4.0f" % (thr, tw[thr], " ".join("%5.1f" % v for v in o["F"]),
                                                                        crew(o["F"]), o["S"][NAMES.index("V")]))
    print("the same with the strong strokes divided by their own filed share located at the day's level")
    for thr in TAILS:
        o = tail_own[thr]
        print("  %2.0f kA and over  worth %.2f  %s | %-6s | S_V %4.0f" % (thr, tw_own[thr], " ".join("%5.1f" % v for v in o["F"]),
                                                                        crew(o["F"]), o["S"][NAMES.index("V")]))
    print("the run routes' further settings (expected hours, the crews each files; the golden files %s)" % crew(g["F"]))
    for k_, o in family.items():
        print("  %-44s %s | %s" % (k_, " ".join("%5.1f" % v for v in o["F"]), crew(o["F"])))
    lands = [k_ for k_, o in family.items() if crew(o["F"]) == crew(g["F"])]
    gside = [v > LINE for v in g["F"]]
    print("the cut-off family at the fitted worth: at each cut, the station furthest on the wrong side of the line (hours past it), least over the three thinning draws")
    close = []
    for k in CUTS:
        worst_k = []
        for lab in ("cutoff:k%d" % k, "cutoff:k%d, thinning draw 2" % k, "cutoff:k%d, thinning draw 3" % k):
            F_ = family[lab]["F"]
            worst_k.append(max((abs(F_[i] - LINE), NAMES[i]) for i in range(NS) if (F_[i] > LINE) != gside[i]) if any(
                (F_[i] > LINE) != gside[i] for i in range(NS)) else (0.0, "-"))
        close.append((min(worst_k), k))
        print("  k %2d  %s by %.1f" % (k, min(worst_k)[1], min(worst_k)[0]))
    print("the cut family's least closure is %.1f hours, at k %d" % (min(close)[0][0], min(close)[1]))
    # the replay test read by day size: what rules on a calibration cut at any size (its own days pass by construction)
    by_size = {}
    print("the replay test by the day's size on the full network (log points, out of fold; one or two strokes, three to five, six to nineteen, twenty or more; the largest)")
    for lab, m_ in [("golden", g), ("one share, every well-covered day", routes["flat"])] + [
            ("cutoff:k%d" % k, family["cutoff:k%d" % k]) for k in CUTS]:
        v = [replay_test(R, law, m_, size=sz) for sz in SIZES]
        by_size[lab] = v
        print("  %-36s %s | %.3f" % (lab, " ".join("%.3f" % x for x in v), max(v)))
    worst_g = max(by_size["golden"])
    least_cut = min((max(v), lab) for lab, v in by_size.items() if lab != "golden")
    print("read by day size the golden's largest miss is %.3f; the least of the one-share routes' largest misses is %.3f (%s), %.1f times it" % (
        worst_g, least_cut[0], least_cut[1], least_cut[0] / worst_g))
    print("settings that file the golden's call: %s" % (", ".join(lands) or "none"))

    rc_ = replay_counts(R, law, kap)
    print("\nground strokes on the well-covered days thinned to two and to three sensors, against those days' own count: "
          "the count left over the fitted law's share %.2f and %.2f; the strokes left weighted by one over their filed "
          "chance, capped at 50, %.2f and %.2f" % (rc_[0][0], rc_[1][0], rc_[0][1], rc_[1][1]))

    # the back-test a run does on the record: fit 2002 to 2017, forecast 2018 to 2025, hours as located
    H, C, Wd, lev = face_tables(R)
    Hs = season_sum(R, H)
    tr, te = np.arange(16), np.arange(16, 24)
    print("\nhold-out on the located hours (fit to 2017-18, forecast the eight seasons since): rmse of the record's "
          "mean, of a regression on the index")
    for i, n in enumerate(NAMES):
        b, _ = ols(np.log(Hs[i][tr] + 0.5), np.column_stack([np.ones(16), INDEX[tr]]))
        e0 = math.sqrt(np.mean((Hs[i][te] - Hs[i][tr].mean()) ** 2))
        e1 = math.sqrt(np.mean((Hs[i][te] - (np.exp(b[0] + b[1] * INDEX[te]) - 0.5)) ** 2))
        bb, _ = ols(np.log(Hs[i] + 0.5), np.column_stack([np.ones(NT), INDEX]))
        print("  %s  mean %.1f  regression %.1f  | slope on the whole record %.2f | era means %s" % (
            n, e0, e1, bb[1], " ".join("%.1f" % Hs[i][ERA == k].mean() for k in range(3))))
    print()

    ix = {n: i for i, n in enumerate(NAMES)}
    members = {}
    for n, i in ix.items():
        members[n] = {"lines": [LINE], "truth": float(truth["F"][i]), "golden": float(g["F"][i]),
                      "family": [float(f["F"][i]) for f in fam],
                      "routes": {"direct": float(routes["direct"]["F"][i]), "rigorous": float(routes["rigorous"]["F"][i]),
                                 "imputed": float(routes["imputed"]["F"][i])}}
    fmap = lambda k: {n: float(routes[k]["F"][i]) for n, i in ix.items()}
    mean_map = fmap("mean")
    lattice = {k: {n: float(v["F"][i]) for n, i in ix.items()} for k, v in lat.items()}
    run_routes = {k: {n: float(routes[k]["F"][i]) for n, i in ix.items()} for k in ("generous", "calibrated", "hedge", "cutoff")}
    run_routes.update({k: {n: float(o["F"][i]) for n, i in ix.items()} for k, o in family.items()})
    side = lambda o: {"over": {n: float(o["F"][i]) for n, i in ix.items()}}

    fkey = {"F_" + n: ("F", n) for n in NAMES}        # each graded figure's table and station, to price any route

    def fig(fid, block, famkey, n, sentence=None):
        i = ix[n]
        fkey[fid] = (famkey, n)
        d = {"id": fid, "block": block, "golden": float(g[famkey][i]), "family": [float(f[famkey][i]) for f in fam],
             "lattice": {k: float(v[famkey][i]) for k, v in lat.items()},
             "routes": {k: float(routes[k][famkey][i]) for k in ("rigorous", "generous", "calibrated", "hedge", "cutoff", "imputed", "mean", "outage", "flat")}}
        if sentence:
            d["sentence"] = sentence
        return d

    figs = [fig("C1 average-season hours at Z", "component", "B", "Z"),
            fig("C2 average-season ground strokes at V", "component", "S", "V")]
    for gname, ms in GROUPS.items():
        for n in ms:
            figs.append({"id": "F_" + n, "block": "ask", "member": n, "sentence": "this season, " + gname})
        for n in ms:
            figs.append(fig("B_" + n, "ask", "B", n, "average season, " + gname))
            figs.append(fig("S_" + n, "ask", "S", n, "average season, " + gname))
    figs.append(fig("pct", "ask", "pct", "A", "crossing, over the line"))
    for n in ("A", "Z", "X", "V"):
        figs.append(fig("cross_" + n, "ask", "cross", n, "crossing, over the line"))
    for n in ("Y", "W", "B"):
        figs.append(fig("cross_" + n, "ask", "cross", n, "crossing, under the line"))

    spec = {
        "task": "task3 architecture 9",
        "call": "lines",
        "members": members,
        "stumps": {
            "S1": {"axis": "what", "opens": "Z",
                   "said_out_loud": "The strokes the network missed shorten stand-downs, split them and erase whole "
                                    "days, so recorded hours do not answer to detection in proportion.",
                   "steps_left": 5, "precedents": ["L56", "N21", "L57"], "sides": side(over["S1"])},
            "S3": {"axis": "against", "opens": "V",
                   "said_out_loud": "A legacy receiver does not add what a standard sensor adds to detection.",
                   "steps_left": 4, "precedents": ["N42", "L58"], "sides": side(over["S3"])},
        },
        "lattice": lattice,
        "falsification": {
            "check": "three statistics of the stations' own located strokes and sensor log (the well-covered days "
                     "thinned to two and three sensors by the filed chances with the route's correction applied, "
                     "against the hours those days carried on the full network, read by the day's size in four "
                     "classes, the largest miss; amplitudes on the days a legacy "
                     "receiver was in range; the strong strokes' response to the index against the response the "
                     "route carries and the response its corrected hours show), each against what the route's own "
                     "assumptions predict; the score is the root mean square of the three log misses",
            "observes_target": False, "truth": 0.0, "golden": fal["golden"]["score"],
            "rivals": {k: v["score"] for k, v in fal.items() if k not in ("golden", "mean")}},
        "run_routes": run_routes,
        "figures": figs,
    }
    rc = corelib.run(spec)
    e = corelib.earnings(spec)
    gcall = corelib._calls(spec, {m: spec["members"][m]["golden"] for m in spec["members"]})
    for k, what in (("imputed", "missed strokes put back, the timer rerun"),
                    ("outage", "one elasticity of hours to the filed share, from the outage days"),
                    ("flat", "one share of hours kept at each sensor count from the well-covered days, legacy worth fitted")):
        print("the %s route (%s) earns %.0f on the rubric; it files %s" % (
            k, what, corelib._run_route_score(spec, e["figs"], k, fmap(k), gcall)[0],
            ", ".join(n for n in NAMES if routes[k]["F"][ix[n]] > LINE) or "no station"))
    # the supporting step is where the response is read (the strong strokes, which every era's network located).
    # Left out alone, with both stumps made, it is the response read on the route's own corrected hours: a variant
    # of the battery. The harsher reading, no state carried at all (the record's mean, the filed outlook ignored),
    # is printed beside it with its room, at the golden's conventions and in the battery's lowest variant.
    basis = estimate(R, law=law, kappa=kap, hours_state=True)
    same_b = all((basis["F"][ix[n]] > LINE) == (g["F"][ix[n]] > LINE) for n in NAMES)
    print("the supporting step left out alone (the response read on the corrected hours in place of the strong strokes): "
          "this season %.1f per cent of an average one against %.1f; it files %s, %s" % (
              basis["pct"][0], g["pct"][0], crew(basis["F"]), "the golden's call" if same_b else "NOT the golden's call"))
    over_ = [n for n in NAMES if g["F"][ix[n]] > LINE]
    same = all((mean_map[n] > LINE) == (g["F"][ix[n]] > LINE) for n in NAMES)
    room = min((mean_map[n] / LINE - 1.0, n) for n in over_)
    worst = min((f["B"][ix[n]] / LINE - 1.0, nm, n) for (nm, _), f in zip(BATTERY, fam) for n in over_)
    print("no state carried at all (the corrected record's mean, the filed outlook ignored) earns %.0f on the rubric; it "
          "files %s, %s, with every figure for the window %.0f per cent low; the nearest station it keeps over the line "
          "is %s, %.1f per cent over; in the battery's lowest variant %s is %.1f per cent %s the line ('%s')" % (
              corelib._run_route_score(spec, e["figs"], "mean", mean_map, gcall)[0], crew([mean_map[n] for n in NAMES]),
              "the golden's call" if same else "NOT the golden's call", 100 - 1e4 / g["pct"][0], room[1], 100 * room[0],
              worst[2], abs(100 * worst[0]), "over" if worst[0] > 0 else "under", worst[1]))
    # every further setting of a run route priced on the rubric, per sentence and per figure: the review reads its
    # strongest run, so the dearest setting is the one that counts
    def price(o, per_fig=False):
        right = all((o["F"][ix[n]] > LINE) == (g["F"][ix[n]] > LINE) for n in NAMES)
        val = lambda f: float(o[fkey[f["id"]][0]][ix[fkey[f["id"]][1]]])
        if not per_fig:
            return corelib._score(e["figs"], right, val)
        sc = corelib.BLOCKS["instruction"] + (corelib.BLOCKS["recommendation"] if right else 0.0)
        for b_ in ("components", "asks"):
            fs = [f for f in e["figs"] if f["block"] == b_]
            sc += corelib.BLOCKS[b_] * sum(1 for f in fs if corelib._earned(f, val(f))) / len(fs)
        return sc
    priced = sorted(((price(o), price(o, True), k) for k, o in family.items()), reverse=True)
    print("the run routes' further settings on the rubric (per sentence, per figure), dearest first:")
    for a_, b_, k in priced[:8]:
        print("  %-44s %3.0f %3.0f" % (k, a_, b_))
    print("the dearest further setting earns %.0f per sentence (%s) and %.0f per figure (%s); %d settings priced" % (
        priced[0][0], priced[0][2], max(p[1] for p in priced), max(priced, key=lambda p: p[1])[2], len(priced)))
    print("the worth read off the strong strokes with the golden's replay (S3 made by a count of strong strokes): "
          + "; ".join("%.0f kA worth %.2f earns %.0f, files %s" % (thr, tw[thr], price(tail_g[thr]), crew(tail_g[thr]["F"])) for thr in TAILS))
    if priced[0][0] > corelib.ONE_LOST_MAX + 1e-9:
        print("FAIL  a further setting of a run route earns over %.0f" % corelib.ONE_LOST_MAX)
        rc = rc or 1
    # one stump lost, priced per figure in place of per sentence (the same blocks, each figure its own criterion)
    def per_figure(key):
        sc = corelib.BLOCKS["instruction"] + (corelib.BLOCKS["recommendation"] if corelib._calls(spec, lattice[key]) == gcall else 0.0)
        for b_ in ("components", "asks"):
            fs = [f for f in e["figs"] if f["block"] == b_]
            sc += corelib.BLOCKS[b_] * sum(1 for f in fs if corelib._earned(f, f["values"][corelib._key(key.split("+"))])) / len(fs)
        return sc
    print("priced per figure in place of per sentence: S1 lost alone earns %.0f, S3 lost alone %.0f, both lost %.0f" % (
        per_figure("S1"), per_figure("S3"), per_figure("S1+S3")))
    if not (same_b and same):
        # a closed lesson may support, never decide: where the response is read may not move the call, and neither
        # may the state left out at the golden's own conventions
        print("FAIL  the supporting step decides        left out alone it moves the call; a closed lesson may never decide")
        rc = rc or 1
    return rc


if __name__ == "__main__":
    sys.exit(main())
