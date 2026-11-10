"""task15: the analysis. One Panel in, every graded figure out.

The Panel is the conformed record (built from the clean world by checks.py, and again from the shipped pack by
verify.py on its own loaders): programme plots, each trial's season water, the series' published site means with
their season water, the lines' cohorts, the nominations as quoted, and this year's Stage 3 lines.

analyse(panel) is the golden. analyse(panel, **options) runs a rival (another defensible way to do one step);
quick(panel) and careful(panel) are the hurried analyst's passes. None of them reads the prompt.
"""
import math

import numpy as np
import pandas as pd

BENCH = "Byaduk"
STANDARDS = ["Byaduk", "Wando", "Carapook"]       # in the programme's trials and in the series
INDEX_SITES = ["Lake Bolac", "Skipton", "Kerang"]
STANDARD_RY = 103.0                               # the default; a Panel carries the deed's own figure
CAP = 3                                           # nominations a sowing year (the option deed, schedule 2)
PLACES = 2                                        # the lines asked for this year (the request names the number)
LEVEL0 = 4.0                                      # t/ha, where the yield-level covariate is centred


class Panel(object):
    def __init__(self, plots, water, series, series_water, series_cv, cohort, checks, noms, cands, s3_seasons,
                 last_season):
        # trial, site, season, stage, line, rep, blk, col, y (nan if abandoned), L, ab; one order whatever the source
        self.plots = plots.sort_values(["season", "trial", "blk", "col"]).reset_index(drop=True)
        self.water = dict(water)            # programme trial -> season water, mm
        # trial, site, season, line, y, L  (site means as published)
        self.series = series.sort_values(["season", "site", "line"]).reset_index(drop=True)
        self.series_water = dict(series_water)
        self.series_cv = dict(series_cv)    # series trial -> cv of plot yields, per cent
        self.cohort = dict(cohort)          # line -> first Stage 1 season (0 for the check varieties)
        self.checks = list(checks)
        self.noms = sorted(noms, key=lambda n: (n["sow"], n["line"]))   # sow (year), line, index (quoted), s3 (seasons)
        self.cands = sorted(cands)
        self.irrigation = {}                # programme trial -> millimetres watered on (part of its season water)
        self.standard = STANDARD_RY         # the uptake standard, as the deed states it
        self.places = PLACES                # how many lines the request asks to nominate
        self.wi = {}
        self.s3_seasons = dict(s3_seasons)
        self.last = int(last_season)


def xw(mm):
    return (float(mm) - 350.0) / 100.0


# ------------------------------------------------------------------ plots to cells

def plot_model(pl, lodging=True, blocks=True, trend=False, iters=12):
    """Harvested plots: yield = line-in-trial + block - loss per lodging unit (+ a slope along the range).
    Returns the plots with block-adjusted yield, and the loss per lodging unit."""
    d = pl.reset_index(drop=True).copy()
    ok = (d["ab"] == 0).to_numpy()
    y = d["y"].to_numpy(float)
    L = d["L"].to_numpy(float)
    cell = (d["trial"] + "|" + d["line"]).to_numpy()
    blk = (d["trial"] + "|" + d["blk"].astype(str)).to_numpy()
    ci = pd.factorize(cell)[0]
    bi = pd.factorize(blk)[0]
    ti = pd.factorize(d["trial"])[0]
    col = d["col"].to_numpy(float)
    colc = col - pd.Series(col).groupby(ti).transform("mean").to_numpy()
    nb, nc, nt = bi.max() + 1, ci.max() + 1, ti.max() + 1
    gam, beff, slope = 0.0, np.zeros(nb), np.zeros(nt)

    def gmean(v, idx, n):
        s = np.bincount(idx[ok], weights=v[ok], minlength=n)
        c = np.bincount(idx[ok], minlength=n)
        return s / np.maximum(c, 1)

    for _ in range(iters):
        base = y - beff[bi] - slope[ti] * colc + gam * L
        cm = gmean(np.where(ok, base, 0.0), ci, nc)
        if blocks:
            res = y - cm[ci] + gam * L - slope[ti] * colc
            beff = gmean(np.where(ok, res, 0.0), bi, nb)
            tmean = gmean(beff[bi], ti, nt)
            beff = beff - tmean[ti[np.unique(bi, return_index=True)[1]]]
        if trend:
            res = y - cm[ci] + gam * L - beff[bi]
            num = np.bincount(ti[ok], weights=(res * colc)[ok], minlength=nt)
            den = np.bincount(ti[ok], weights=(colc * colc)[ok], minlength=nt)
            slope = num / np.maximum(den, 1e-9)
        if lodging:
            ya = y - beff[bi] - slope[ti] * colc
            ym = gmean(np.where(ok, ya, 0.0), ci, nc)
            lm = gmean(np.where(ok, L, 0.0), ci, nc)
            yt, lt = (ya - ym[ci])[ok], (L - lm[ci])[ok]
            gam = float(-(yt * lt).sum() / max((lt * lt).sum(), 1e-9))
    d["yadj"] = y - beff[bi] - slope[ti] * colc
    return d, gam


def cells(d, gam, water):
    """One row per line per trial: potential yield (lodging loss added back) from the harvested plots, the mean
    lodging of every plot sown, and the harvested-only mean the breeder reads."""
    h = d[d["ab"] == 0].copy()
    h["pot"] = h["yadj"] + gam * h["L"]
    g = h.groupby(["trial", "line"], sort=False)
    a = g.agg(pot=("pot", "mean"), n=("pot", "size"), yh=("yadj", "mean"), yraw=("y", "mean"), Lh=("L", "mean"))
    b = d.groupby(["trial", "line"], sort=False).agg(L=("L", "mean"), nall=("L", "size"), site=("site", "first"),
                                                       season=("season", "first"), stage=("stage", "first"))
    c = b.join(a, how="left").reset_index()
    r = h["pot"] - g["pot"].transform("mean")
    ss = (r * r).groupby(h["trial"]).sum()
    dfree = (h.groupby("trial").size() - h.groupby("trial")["line"].nunique()).clip(lower=1)
    c["s2"] = c["trial"].map(ss / dfree)
    c["x"] = c["trial"].map({t: xw(w) for t, w in water.items()})
    c["n"] = c["n"].fillna(0)
    return c


# ------------------------------------------------------------------ the line effects

def cross_of(line):
    """A line's cross: the part of its cross code before the plant selection (22X238-17 is of cross 22X238)."""
    return str(line).split("-")[0]


def eb_fit(c, cohort, checks, col="pot", slope=True, iters=70, pooled_prior=False, family=True):
    """Every line's yield level and water response relative to the benchmark. Lines are random within their
    cohort (the whole Stage 1 intake, so the lines later dropped set the prior) and, inside it, within their
    cross (sister lines share part of both), the check varieties fixed, trial means free. EM on the cell means
    with the cells' own variances."""
    c = c[c[col].notna() & (c["n"] > 0)]
    tr = pd.factorize(c["trial"])
    ti, tnames = tr[0], list(tr[1])
    lf = pd.factorize(c["line"])
    li, ln = lf[0], list(lf[1])
    nl, nt = len(ln), len(tnames)
    y = c[col].to_numpy(float)
    x = c["x"].to_numpy(float)
    n = c["n"].to_numpy(float)
    s2 = c["s2"].to_numpy(float)
    k = 2 if slope else 1
    Z = np.column_stack([np.ones(len(c)), x])[:, :k]
    xt = np.zeros(nt)
    xt[ti] = x
    Zt = np.column_stack([np.ones(nt), xt])[:, :k]
    is_check = np.array([l in checks for l in ln])
    coh = np.array([0 if pooled_prior and not (l in checks) else cohort.get(l, 0) for l in ln])
    if pooled_prior:
        coh = np.where(is_check, 0, 1)
    cohs = sorted(set(coh[~is_check].tolist()))
    cf = pd.factorize(np.array([("" if is_check[j] else cross_of(l)) for j, l in enumerate(ln)]))
    xi, nx = cf[0], len(cf[1])
    theta = np.zeros((nl, k))
    V = np.zeros((nl, k, k))
    m = {cc: np.zeros(k) for cc in cohs}
    Sig = np.eye(k) * 0.05                      # between sister lines of one cross (or between lines, no family)
    SigC = np.eye(k) * 0.03                     # between crosses
    u = np.zeros((nx, k))
    Vu = np.zeros((nx, k, k))
    sd2 = 0.02
    mu = np.zeros(nt)
    bj = ln.index(BENCH)
    I = np.eye(k)
    for it in range(iters):
        w = 1.0 / (sd2 + s2 / n)
        fit = (Z * theta[li]).sum(1)
        mu = np.bincount(ti, weights=w * (y - fit), minlength=nt) / np.bincount(ti, weights=w, minlength=nt)
        r = y - mu[ti]
        A = np.zeros((nl, k, k))
        bv = np.zeros((nl, k))
        for a_ in range(k):
            bv[:, a_] = np.bincount(li, weights=w * Z[:, a_] * r, minlength=nl)
            for b_ in range(k):
                A[:, a_, b_] = np.bincount(li, weights=w * Z[:, a_] * Z[:, b_], minlength=nl)
        Sinv = np.linalg.inv(Sig)
        prior_m = np.zeros((nl, k))
        for cc in cohs:
            prior_m[coh == cc] = m[cc]
        Pm = A + np.where(is_check[:, None, None], 1e-9 * np.eye(k), Sinv)
        V = np.linalg.inv(Pm)
        if family:
            # each cross's share, from its lines with their own noise and their spread about it taken out
            AV = np.einsum("ijk,ikl->ijl", A, V)
            Wl = A - np.einsum("ijk,ikl->ijl", AV, A)
            rl = np.einsum("ijk,ik->ij", I[None] - AV, bv) - np.einsum("ijk,ik->ij", Wl, prior_m)
            Wl[is_check] = 0.0
            rl[is_check] = 0.0
            prec = np.zeros((nx, k, k)) + np.linalg.inv(SigC)[None]
            rhs_u = np.zeros((nx, k))
            np.add.at(prec, xi, Wl)
            np.add.at(rhs_u, xi, rl)
            Vu = np.linalg.inv(prec)
            u = np.einsum("ijk,ik->ij", Vu, rhs_u)
            prior_l = prior_m + u[xi]
        else:
            prior_l = prior_m
        rhs = bv + np.where(is_check[:, None], 0.0, prior_l @ Sinv.T)
        theta = np.einsum("ijk,ik->ij", V, rhs)
        tb = theta[bj].copy()                    # everything relative to the benchmark
        theta = theta - tb
        mu = mu + Zt @ tb
        V[is_check] = 0.0
        S = np.zeros((k, k))
        SC = np.zeros((k, k))
        cnt = 0
        dev = np.zeros((nl, k))
        for cc in cohs:
            sel = (~is_check) & (coh == cc)
            m[cc] = (theta[sel] - (u[xi[sel]] if family else 0.0)).mean(0)
            dev[sel] = theta[sel] - m[cc] - (u[xi[sel]] if family else 0.0)
            S += dev[sel].T @ dev[sel] + V[sel].sum(0)
            cnt += int(sel.sum())
        Sig = S / max(cnt, 1)
        if family:
            used = np.unique(xi[~is_check])
            SigC = (u[used].T @ u[used] + Vu[used].sum(0)) / max(len(used), 1)
        fit = (Z * theta[li]).sum(1)
        res = y - mu[ti] - fit
        lev = np.einsum("ij,ijk,ik->i", Z, V[li], Z)
        sd2 = max(1e-4, float(np.sum(w * w * (res * res + lev - s2 / n)) / np.sum(w * w)))
    if family:                                   # a line's spread includes what is unsure about its cross's share
        G_ = np.einsum("ijk,kl->ijl", V, Sinv)
        V = V + np.einsum("ijk,ikl,iml->ijm", G_, Vu[xi], G_)
        V[is_check] = 0.0
    th = {l: theta[j] for j, l in enumerate(ln)}
    Vd = {l: V[j] for j, l in enumerate(ln)}
    return dict(theta=th, V=Vd, m=m, Sig=Sig, SigC=SigC, sd2=sd2, mu=dict(zip(tnames, mu)), k=k)


def plain_fit(c, checks, col="pot", slope=True):
    """The plainest sound fit, as a rival to eb_fit: each line on its own trials alone. In every trial the line's
    cell mean less the benchmark's in the same trial; per line, an ordinary least squares line of that difference
    on the trial's season water. No pooling across lines, cohorts or crosses."""
    c = c[c[col].notna() & (c["n"] > 0)]
    b = c[c["line"] == BENCH].set_index("trial")
    d = c[c["line"] != BENCH].copy()
    d["dy"] = d[col] - d["trial"].map(b[col])
    d["v"] = d["s2"] / d["n"] + d["trial"].map(b["s2"] / b["n"])
    k = 2 if slope else 1
    th, V, rss, dof = {}, {}, 0.0, 0
    for l, g in d.groupby("line", sort=False):
        x = g["x"].to_numpy(float)
        y = g["dy"].to_numpy(float)
        if k == 2 and len(g) >= 4 and float(np.ptp(x)) > 0.3:
            X = np.column_stack([np.ones(len(g)), x])
        else:
            X = np.ones((len(g), 1))
        XtX = np.linalg.inv(X.T @ X)
        beta = XtX @ X.T @ y
        res = y - X @ beta
        if len(g) > X.shape[1]:
            rss += float(res @ res)
            dof += len(g) - X.shape[1]
        th[l] = np.array([beta[0], beta[1] if X.shape[1] == 2 else 0.0])[:k]
        Vl = np.zeros((k, k))
        Vl[:X.shape[1], :X.shape[1]] = XtX
        V[l] = Vl
    s2r = rss / max(dof, 1)
    for l in V:
        V[l] = V[l] * s2r
    th[BENCH] = np.zeros(k)
    V[BENCH] = np.zeros((k, k))
    sd2 = max(1e-4, s2r - float(d["v"].mean()))          # what is left once the cells' own sampling error is out
    return dict(theta=th, V=V, m={}, Sig=np.eye(k) * s2r, SigC=np.zeros((k, k)), sd2=sd2, mu={}, k=k)


# ------------------------------------------------------------------ lodging

def pressure(cl, col="L", who="standards"):
    """A trial's lodging pressure: the mean lodging of the three standards grown both by the programme and by
    the series (or, as a rival, the benchmark's alone)."""
    s = cl[cl["line"].isin(STANDARDS if who == "standards" else [BENCH])]
    return s.groupby("trial")[col].mean()


def lodging_fit(c, cohort, checks, pmin=0.5, shrink=True, baseline=False, family=True, press="standards"):
    """Each line's lodging above the dry-trial floor as a multiple of the standards' in the same trial, shrunk
    toward its cross's and its cohort's. The floor is what plots score where nothing lodges (the trials with the
    least pressure)."""
    P = pressure(c, who=press)
    base = 0.0
    if baseline:
        dry = c[c["trial"].map(P) <= P.quantile(0.35)]
        base = float(np.average(dry["L"], weights=dry["nall"]))
    d = c.assign(P=c["trial"].map(P))
    d = d[d["P"] > pmin]
    w = d["nall"].to_numpy(float)
    Lx = d["L"].to_numpy(float) - base
    Px = d["P"].to_numpy(float) - base
    num = pd.Series(Lx * Px * w).groupby(d["line"].to_numpy()).sum()
    den = pd.Series(Px * Px * w).groupby(d["line"].to_numpy()).sum()
    h = num / den
    res = Lx - d["line"].map(h).to_numpy(float) * Px
    s2 = float((res * res * w).sum() / max(1, len(d) - len(h)))
    vh = s2 / den
    out, var = {}, {}
    coh = pd.Series({l: (0 if l in checks else cohort.get(l, 0)) for l in h.index})
    for cc, idx in coh.groupby(coh).groups.items():
        hh, vv = h.loc[idx], vh.loc[idx]
        if cc == 0 or not shrink or len(idx) < 8:
            for l in idx:
                out[l], var[l] = float(hh[l]), float(vv[l])
            continue
        # the spread between lines is read off the lines that saw enough lodging to show their own multiple
        # (six plots' worth at a tenth of pressure); a line that saw less is still pulled, by its own variance
        seen = den.loc[idx] >= 6.0
        if int(seen.sum()) < 8:
            seen = den.loc[idx] >= float(den.loc[idx].median())
        hs, vs = hh[seen], vv[seen]
        mbar = float(np.average(hs, weights=1.0 / vs))
        tau2 = max(1e-4, float(np.average((hs - mbar) ** 2 - vs, weights=1.0 / vs ** 2)))
        if not family:
            for l in idx:
                k = tau2 / (tau2 + vv[l])
                out[l] = float(mbar + k * (hh[l] - mbar))
                var[l] = float(k * vv[l])
            continue
        # the spread between lines splits into a part sister lines share and a part of their own
        cr = pd.Series([cross_of(l) for l in idx], index=idx)
        g = cr.groupby(cr).groups
        num_w = den_w = 0.0
        for _, ls in g.items():
            ls_ = [l for l in ls if bool(seen[l])]
            if len(ls_) > 1:
                x_, v_ = hh.loc[ls_], vv.loc[ls_]
                num_w += float(((x_ - x_.mean()) ** 2).sum() - v_.sum() * (1.0 - 1.0 / len(ls_)))
                den_w += len(ls_) - 1
        tw = min(max(1e-4, num_w / max(den_w, 1.0)), tau2)       # between sister lines
        tc = max(1e-4, tau2 - tw)                               # between crosses
        for _, ls in g.items():
            wl = 1.0 / (tw + vv.loc[ls])
            xbar = float((wl * hh.loc[ls]).sum() / wl.sum())
            vx = 1.0 / float(wl.sum())
            kc = tc / (tc + vx)
            uc = mbar + kc * (xbar - mbar)                       # the cross's own multiple
            vu = kc * vx
            for l in ls:
                k = tw / (tw + vv[l])
                out[l] = float(uc + k * (hh[l] - uc))
                var[l] = float(k * vv[l] + (1.0 - k) ** 2 * vu)
    return out, var, P, base


# ------------------------------------------------------------------ the series side

def series_frame(P, upto=None, covar="water", press="standards"):
    s = P.series if upto is None else P.series[P.series["season"] <= upto]
    s = s.copy()
    s["x"] = s["trial"].map({t: xw(w) for t, w in P.series_water.items()})
    if covar == "level":
        s["x"] = s["trial"].map(s.groupby("trial")["y"].mean()) - LEVEL0
    b = s[s["line"] == BENCH].set_index("trial")
    press = pressure(s, who=press)
    t = pd.DataFrame({"site": b["site"], "season": b["season"], "x": b["x"], "yb": b["y"], "Lb": b["L"],
                      "P": press.reindex(b.index)})
    return s, t


def realised_ry(s, line, seasons=None):
    d = s[s["line"] == line]
    if seasons is not None:
        d = d[d["season"].isin(seasons)]
    b = s[(s["line"] == BENCH) & (s["trial"].isin(d["trial"]))]
    return 100.0 * float(d["y"].mean()) / float(b.set_index("trial")["y"].reindex(d["trial"]).mean())


def realised_lodging(s, line, seasons=None):
    d = s[s["line"] == line]
    if seasons is not None:
        d = d[d["season"].isin(seasons)]
    return 10.0 * float(d["L"].mean())


def lodge_units(h, P, base):
    """A line's expected lodging (tenths of the plot) in a trial whose standards lodge P."""
    return np.minimum(base + h * np.maximum(np.asarray(P, float) - base, 0.0), 10.0)


def expected_ry(th, h, gam, tt, base=0.0, use_slope=True, use_lodge=True):
    """Expected relative yield over a set of series trials (the ratio of the means, as the series reports it)."""
    d = th[0] + (th[1] * tt["x"].to_numpy(float) if (use_slope and len(th) > 1) else 0.0)
    if use_lodge:
        d = d - gam * (lodge_units(h, tt["P"].to_numpy(float), base) - tt["Lb"].to_numpy(float))
    return 100.0 + 100.0 * float(np.sum(d + 0 * tt["yb"].to_numpy(float))) / float(tt["yb"].sum())


def expected_lodging_score(h, tt, base=0.0):
    """Expected lodging over a set of series trials, per cent of the plot."""
    return 10.0 * float(np.mean(lodge_units(h, tt["P"].to_numpy(float), base)))


# ------------------------------------------------------------------ the breeder's index, and the model's reading of it

def index_trials(P, line, seasons):
    c = P._cells
    return c[(c["line"] == line) & (c["stage"] == "S3") & (c["site"].isin(INDEX_SITES)) & (c["season"].isin(seasons))]


def raw_index(P, line, seasons, col="yraw"):
    """The breeder's index: the mean, over the line's Stage 3 trials at the three wetter sites, of its harvested
    trial mean as a percentage of the benchmark's."""
    c = P._cells
    mine = index_trials(P, line, seasons)
    b = c[(c["line"] == BENCH) & (c["trial"].isin(mine["trial"]))].set_index("trial")[col]
    v = 100.0 * mine.set_index("trial")[col] / b.reindex(mine["trial"].to_numpy()).to_numpy()
    return float(v.dropna().mean())


def model_index(P, fit, hl, gam, Ptrial, line, seasons, base=0.0, parts=False, observed=False):
    """The relative yield to be expected of the line at the trials its index was taken from, as the series
    defines a relative yield (the ratio of the means over those trials), with every sown plot's lodging counted.
    With parts, the points its yield potential adds and the points lodging takes, each against the benchmark's."""
    c = P._cells
    mine = index_trials(P, line, seasons)
    b = c[(c["line"] == BENCH) & (c["trial"].isin(mine["trial"]))].set_index("trial")
    th = fit["theta"][line]
    pot = lod = den = 0.0
    for t, x, lobs in zip(mine["trial"], mine["x"], mine["L"]):
        net_b = float(b.loc[t, "pot"]) - gam * float(b.loc[t, "L"])
        lu = float(lobs) if observed else float(lodge_units(hl.get(line, 1.0), float(Ptrial.get(t, 0.0)), base))
        pot += th[0] + (th[1] * x if len(th) > 1 else 0.0)
        lod += gam * (lu - float(b.loc[t, "L"]))
        den += net_b
    if parts:
        return 100.0 * pot / den, 100.0 * lod / den
    return 100.0 + 100.0 * (pot - lod) / den


def series_parts(th, h, gam, tt, base=0.0, observed=None):
    """The same two parts over a set of series trials (the ratio of the means, as the series reports it).
    observed: the line's published lodging at those trials, in place of the fitted one."""
    yb = tt["yb"].to_numpy(float)
    pot = th[0] + (th[1] * tt["x"].to_numpy(float) if len(th) > 1 else 0.0) + 0.0 * yb
    lu = lodge_units(h, tt["P"].to_numpy(float), base) if observed is None else np.asarray(observed, float)
    lod = gam * (lu - tt["Lb"].to_numpy(float))
    return 100.0 * float(np.sum(pot)) / float(yb.sum()), 100.0 * float(np.sum(lod)) / float(yb.sum())


# ------------------------------------------------------------------ the golden, and its rivals through options

def fit_all(P, upto=None, lodging=True, blocks=True, trend=False, slope=True, pooled_prior=False, pmin=0.5,
            shrink_lodging=True, baseline=False, covar="water", family=True, irrigation=True, engine="eb",
            press="standards"):
    pl = P.plots if upto is None else P.plots[P.plots["season"] <= upto]
    d, gam = plot_model(pl, lodging=lodging, blocks=blocks, trend=trend)
    water = P.water if irrigation else {t: v - P.irrigation.get(t, 0.0) for t, v in P.water.items()}
    c = cells(d, gam, water)
    if covar == "level":                     # the trial's own yield level in place of its season water
        c["x"] = c["trial"].map(c[c["n"] > 0].groupby("trial")["yh"].mean()) - LEVEL0
    if engine == "plain":
        fit = plain_fit(c, P.checks, slope=slope)
        shrink_lodging = False
    else:
        fit = eb_fit(c, P.cohort, P.checks, slope=slope, pooled_prior=pooled_prior, family=family)
    hl, hv, Ptrial, base = lodging_fit(c, P.cohort, P.checks, pmin=pmin, shrink=shrink_lodging, baseline=baseline,
                                       family=family, press=press)
    return dict(d=d, gam=gam, cells=c, fit=fit, hl=hl, hv=hv, Ptrial=Ptrial, base=base)


def bench_swing(P, F, tt, s):
    """The benchmark's own season swing in the series: its yield against the other two standards, less what its
    level, water response and lodging say that difference should be, averaged by season."""
    oth = [v for v in STANDARDS if v != BENCH]
    o = s[s["line"].isin(oth)].groupby("trial").agg(y=("y", "mean"), L=("L", "mean"))
    th = np.mean([F["fit"]["theta"][v] for v in oth], axis=0)
    exp = -(th[0] + (th[1] * tt["x"] if len(th) > 1 else 0.0)) + F["gam"] * (o["L"].reindex(tt.index) - tt["Lb"])
    r = (tt["yb"] - o["y"].reindex(tt.index)) - exp
    sw = r.groupby(tt["season"]).mean()
    return sw - sw.mean()


def simulate(P, F, tt, s, lines, n=20000, seed=7, own=None):
    """Realised two-season relative yields for the lines, drawn together: two series seasons taken from its
    history with their trials, water, lodging pressure and the benchmark's swing as they were; each line's level,
    water response and lodging drawn from what the record leaves uncertain; trial noise on top."""
    rng = np.random.default_rng([15, seed])
    sw = bench_swing(P, F, tt, s)
    seasons = sorted(tt["season"].unique())
    by = {y: tt[tt["season"] == y] for y in seasons}
    cv = pd.Series(P.series_cv)
    th = np.array([F["fit"]["theta"][l] for l in lines])
    V = np.array([F["fit"]["V"][l] for l in lines])
    k = th.shape[1]
    h = np.array([F["hl"].get(l, 1.0) for l in lines])
    hv = np.array([F["hv"].get(l, 0.0) for l in lines])
    chol = np.array([np.linalg.cholesky(v + 1e-12 * np.eye(k)) for v in V])
    out = np.zeros((n, len(lines)))
    pick = rng.integers(0, len(seasons), size=(n, 2))
    blocks = {}
    for y in seasons:
        t = by[y]
        e = (cv.reindex(t.index).to_numpy(float) / 100.0 * t["yb"].to_numpy(float)) ** 2 / 3.0
        blocks[y] = (t["x"].to_numpy(float), t["P"].to_numpy(float), t["Lb"].to_numpy(float),
                     t["yb"].to_numpy(float), e, float(sw[y]))
    gam, sd2, base = F["gam"], F["fit"]["sd2"], F["base"]
    for i in range(n):
        num = np.zeros(len(lines))
        den = 0.0
        z = rng.normal(size=(len(lines), k))
        thi = th + np.einsum("ijk,ik->ij", chol, z)
        hi = h + np.sqrt(hv) * rng.normal(size=len(lines))
        for y in (seasons[pick[i, 0]], seasons[pick[i, 1]]):
            x, Pp, Lb, yb, e, swy = blocks[y]
            lu = np.minimum(base + np.maximum(hi, 0.0)[:, None] * np.maximum(Pp[None, :] - base, 0.0), 10.0)
            d = thi[:, [0]] + (thi[:, [1]] * x[None, :] if k > 1 else 0.0) - gam * (lu - Lb[None, :])
            noise = rng.normal(size=d.shape) * np.sqrt(sd2 + e[None, :])
            num += (yb[None, :] - swy + d + noise).sum(1)
            den += yb.sum()
        out[i] = 100.0 * num / den
    return out


def analyse(P, sims=20000, backtest=True, **opt):
    opt = dict(opt)
    S = float(P.standard)
    recent = opt.pop("recent", None)         # a rival: the series' last few seasons only for the forecast
    obs_lodging = opt.pop("obs_lodging", True)    # the bridge's lodging part on the lodging recorded; False: fitted
    covar = opt.get("covar", "water")
    press = opt.get("press", "standards")
    F = fit_all(P, **opt)
    P._cells = F["cells"]
    gam, fit, hl, base = F["gam"], F["fit"], F["hl"], F["base"]
    s, tt = series_frame(P, covar=covar, press=press)
    R = dict(gam=gam, sd2=fit["sd2"], Sig=fit["Sig"].tolist())

    # R1 to R4: the completed nominees and the bridge
    rows = []
    for nm in P.noms:
        l, sow = nm["line"], nm["sow"]
        mine = s[s["line"] == l]
        if mine["season"].nunique() < 2:
            continue
        mine = mine.set_index("trial")
        tj = tt.loc[mine.index]
        A = raw_index(P, l, nm["s3"])
        potB, lodB = model_index(P, fit, hl, gam, F["Ptrial"], l, nm["s3"], base, parts=True, observed=obs_lodging)
        potC, lodC = series_parts(fit["theta"][l], hl.get(l, 1.0), gam, tj, base,
                                  observed=mine["L"].to_numpy(float) if obs_lodging else None)
        D = realised_ry(s, l)
        it = index_trials(P, l, nm["s3"])
        bi = P._cells[(P._cells["line"] == BENCH) & (P._cells["trial"].isin(it["trial"]))].set_index("trial")
        thl = fit["theta"][l]
        adv_i = float(np.mean([thl[0] + (thl[1] * x_ if len(thl) > 1 else 0.0) for x_ in it["x"]]))
        adv_s = float(np.mean(thl[0] + (thl[1] * tj["x"].to_numpy(float) if len(thl) > 1 else 0.0)))
        rows.append(dict(line=l, sow=sow, quoted=nm["index"], A=A, B=100.0 + potB - lodB, C=100.0 + potC - lodC,
                         D=D, water=potB - potC, lodging=lodC - lodB, adv_index=adv_i, adv_series=adv_s,
                         bench_index=float((bi["pot"] - gam * bi["L"]).mean()), bench_series=float(tj["yb"].mean()),
                         lod_index=float((it.set_index("trial")["L"] - bi["L"]).mean()),
                         lod_series=float((mine["L"] - tj["Lb"]).mean()),
                         water_index=float(np.mean(it["x"])) * 100.0 + 350.0,
                         water_series=float(tj["x"].mean()) * 100.0 + 350.0))
    br = pd.DataFrame(rows)
    R["bridge_rows"] = br
    R["n_completed"] = int(len(br))
    R["promised"] = float(br["quoted"].mean())
    R["realised"] = float(br["D"].mean())
    R["shortfall"] = R["promised"] - R["realised"]
    R["own_sites"] = float((br["quoted"] - br["B"]).mean())
    R["series_sites"] = float((br["B"] - br["C"]).mean())
    R["water_part"] = float(br["water"].mean())
    R["lodging_part"] = float(br["lodging"].mean())
    R["left_over"] = float((br["C"] - br["D"]).mean())

    # R5: what the method would have said when each was nominated
    if backtest:
        back = []
        cache = {}
        for nm in P.noms:
            l, sow = nm["line"], nm["sow"]
            if l not in set(br["line"]):
                continue
            y = sow - 1
            if y not in cache:
                Fy = fit_all(P, upto=y, **opt)
                sy, ty = series_frame(P, upto=y, covar=covar, press=press)
                cache[y] = (Fy, ty)
            Fy, ty = cache[y]
            pred = expected_ry(Fy["fit"]["theta"][l], Fy["hl"].get(l, 1.0), Fy["gam"], ty, Fy["base"])
            back.append(dict(line=l, sow=sow, predicted=pred, quoted=nm["index"], realised=realised_ry(s, l)))
        bk = pd.DataFrame(back)
        R["back_rows"] = bk
        R["rmse_method"] = float(np.sqrt(((bk["predicted"] - bk["realised"]) ** 2).mean()))
        R["rmse_index"] = float(np.sqrt(((bk["quoted"] - bk["realised"]) ** 2).mean()))
        R["bias_method"] = float((bk["predicted"] - bk["realised"]).mean())

    # R6, R7: this year's Stage 3 lines over the series as it has run
    tf = tt if not recent else tt[tt["season"] > P.last - int(recent)]
    sim = simulate(P, F, tf, s, P.cands, n=sims) if sims else None
    rows = []
    for j, l in enumerate(P.cands):
        ry = expected_ry(fit["theta"][l], hl.get(l, 1.0), gam, tf, base)
        row = dict(line=l, ry=ry, lodging=expected_lodging_score(hl.get(l, 1.0), tf, base),
                   index=raw_index(P, l, P.s3_seasons[l]), seasons=len(P.s3_seasons[l]))
        if sim is not None:
            row.update(lo=float(np.percentile(sim[:, j], 10)), hi=float(np.percentile(sim[:, j], 90)),
                       p=float((sim[:, j] >= S).mean()))
        rows.append(row)
    cd = pd.DataFrame(rows).sort_values("ry", ascending=False).reset_index(drop=True)
    R["cands"] = cd
    R.update(choose(cd, P.places))
    R["index_picks"] = choose(cd, P.places, col="index")["picks"]
    R["F"] = F
    return R


def choose(cd, places=PLACES, col="ry"):
    """The nominations: the lines with the highest expected relative yield, as many as the request asks for. Also
    the first line left out and how far the last line in stands above it (the cut)."""
    cd = cd.sort_values([col, "line"], ascending=[False, True], kind="mergesort").reset_index(drop=True)
    picks = cd["line"].head(places).tolist()
    nxt = cd["line"].iloc[places] if len(cd) > places else None
    cut = float(cd[col].iloc[places - 1] - cd[col].iloc[places]) if len(cd) > places else float("nan")
    return dict(picks=picks, next=nxt, margin=cut)


# ------------------------------------------------------------------ the hurried passes

def quick(P):
    """Ten minutes: reproduce the shortfall, call it regression to the mean, keep the index's order."""
    F = fit_all(P, lodging=False)
    P._cells = F["cells"]
    s, tt = series_frame(P)
    done = [nm for nm in P.noms if s[s["line"] == nm["line"]]["season"].nunique() >= 2]
    promised = float(np.mean([nm["index"] for nm in done]))
    realised = float(np.mean([realised_ry(s, nm["line"]) for nm in done]))
    c = P._cells
    rows = []
    for l in P.cands:
        mine = c[(c["line"] == l)]
        rows.append(dict(line=l, ry=raw_index(P, l, P.s3_seasons[l]), lodging=10.0 * float(mine["L"].mean())))
    cd = pd.DataFrame(rows).sort_values("ry", ascending=False).reset_index(drop=True)
    ch = choose(cd, P.places)
    return dict(promised=promised, realised=realised, shortfall=promised - realised, own_sites=promised - realised,
                series_sites=0.0, water_part=0.0, lodging_part=0.0, left_over=0.0, rmse_method=None, cands=cd,
                picks=ch["picks"], next=ch["next"], margin=ch["margin"], p_any=None, p_each=None)


def _norm_p(ry, sd, S=STANDARD_RY):
    return float(0.5 * math.erfc(((S - ry) / sd) / math.sqrt(2.0)))


def careful(P, with_lodging=True, covar="level"):
    """An afternoon, careful but hurried, as the run record says a strong run works unprompted: every file
    cleaned, block-adjusted trial means, every line's yield against the benchmark's in the same trial, the visible
    fall of that advantage with the trial's yield level (or its season water) taken as one slope for all lines,
    each line's level shrunk for its own noise, the forecast read at the series' conditions, then checked against
    the past nominees: the mean miss taken off, and the part of the miss that goes with a line's lodging at the
    wetter sites taken off line by line, a prediction interval from the scatter that is left, and the three
    nominees treated as independent. The review's lodging head it gets right (a tenth lodged priced from the plots
    with line and trial taken out, on the lodging recorded). What it does not do: give each line its own response,
    carry a line's lodging to the series' pressure, or let the nominees' results move together."""
    F = fit_all(P, lodging=False)
    P._cells = F["cells"]
    s, tt = series_frame(P)
    c = F["cells"]
    c = c[c["n"] > 0].copy()
    bm = c[c["line"] == BENCH].set_index("trial")["yh"]
    c["yb"] = c["trial"].map(bm)
    c["r"] = c["yh"] - c["yb"]                       # tonnes a hectare over the benchmark in the same trial
    c["m"] = c["trial"].map(c.groupby("trial")["yh"].mean()) if covar == "level" else c["x"]
    lines_ = c[~c["line"].isin(P.checks)]
    smean = s.groupby("trial")["y"].mean() if covar == "level" else s.groupby("trial")["x"].first()
    sbench = s[s["line"] == BENCH].set_index("trial")["y"]
    sbl = s[s["line"] == BENCH].set_index("trial")["L"]
    sseason = s.groupby("trial")["season"].first()

    def fit(upto):
        d = lines_[(lines_["season"] <= upto) & (lines_["stage"].isin(["S2", "S3"]))]
        g_ = d.groupby("line")
        dm, dr = d["m"] - g_["m"].transform("mean"), d["r"] - g_["r"].transform("mean")
        beta = float((dm * dr).sum() / (dm * dm).sum())
        mbar = float(d["m"].mean())
        d = d.assign(adj=d["r"] - beta * (d["m"] - mbar))
        a = d.groupby("line")["adj"].agg(["mean", "count"])
        s2 = float(((d["adj"] - d["line"].map(a["mean"])) ** 2).sum() / max(1, len(d) - len(a)))
        return beta, mbar, a, s2

    def level(a, s2, l, pool):
        pool = [q for q in pool if q in a.index]
        v = s2 / a.loc[pool, "count"]
        m = float(a.loc[pool, "mean"].mean())
        tau2 = max(1e-4, float(a.loc[pool, "mean"].var(ddof=1)) - float(v.mean()))
        return m + tau2 / (tau2 + s2 / a.loc[l, "count"]) * (float(a.loc[l, "mean"]) - m)

    def wet_lodging(l, upto):
        d = c[(c["line"] == l) & (c["site"].isin(INDEX_SITES)) & (c["stage"] == "S3") & (c["season"] <= upto)]
        v = d["L"].mean()
        return 10.0 * (float(v) if v == v else float(c[c["line"] == l]["L"].mean()))

    def pool_of(season):
        return sorted(set(c[(c["stage"] == "S3") & (c["season"] == season) & (~c["line"].isin(P.checks))]["line"]))

    done = [nm for nm in P.noms if s[s["line"] == nm["line"]]["season"].nunique() >= 2]
    fits = {}
    rows = []
    for nm in done:
        y = nm["sow"] - 1
        if y not in fits:
            fits[y] = fit(y)
        beta, mbar, a, s2 = fits[y]
        l = nm["line"]
        lev = level(a, s2, l, pool_of(y))
        it = index_trials(P, l, nm["s3"])
        ms = s[s["line"] == l].set_index("trial")
        mine = ms.index
        past = sseason[sseason <= y].index
        m_h, b_h = float(smean.reindex(past).mean()), float(sbench.reindex(past).mean())
        mt = c.groupby("trial")["m"].first().reindex(it["trial"])
        ybt = bm.reindex(it["trial"])
        rows.append(dict(line=l, sow=nm["sow"], quoted=nm["index"],
                         B=float((100.0 + 100.0 * (lev + beta * (mt.to_numpy() - mbar)) / ybt.to_numpy()).mean()),
                         pred=100.0 + 100.0 * (lev + beta * (m_h - mbar)) / b_h,
                         C=100.0 + 100.0 * (lev + beta * (float(smean.reindex(mine).mean()) - mbar))
                         / float(sbench.reindex(mine).mean()), lod=wet_lodging(l, y),
                         D=realised_ry(s, l), Ls=realised_lodging(s, l),
                         Lx=10.0 * float((ms["L"] - sbl.reindex(mine)).mean())))
    d = pd.DataFrame(rows)
    promised, realised = float(d["quoted"].mean()), float(d["D"].mean())

    def miss_fit(tr, xcol):
        """The miss (forecast less realised) against a lodging figure: its level and what goes with lodging; a
        slope with the wrong sign is dropped, as a careful analyst would drop it."""
        e = (tr["pred"] if xcol == "lod" else tr["C"]).to_numpy(float) - tr["D"].to_numpy(float)
        x = tr[xcol].to_numpy(float)
        cc = 0.0
        if with_lodging and len(tr) >= 9 and float(np.var(x, ddof=1)) > 4.0:
            cc = float(np.cov(x, e)[0, 1] / np.var(x, ddof=1))
        cc = min(max(cc, 0.0), 0.5)             # a wrong-signed or runaway share is not filed
        a0 = float(e.mean() - cc * x.mean())
        res = e - a0 - cc * x
        return a0, cc, float(np.sqrt((res ** 2).sum() / max(1, len(tr) - (2 if cc > 0 else 1))))

    back = []
    for _, row in d.iterrows():
        seen = d[d["sow"] <= row["sow"] - 2]
        p = float(row["pred"])
        if len(seen) >= 6:
            a0, cc, _ = miss_fit(seen, "lod")
            p = p - a0 - cc * float(row["lod"])
        back.append(dict(line=row["line"], sow=int(row["sow"]), predicted=p, realised=float(row["D"])))
    bk = pd.DataFrame(back)
    a0, cc, sd = miss_fit(d, "lod")
    # the review's lodging head: what the plots say a tenth lodged costs, on the lodging each nomination recorded
    gam_c = plot_model(P.plots, lodging=True)[1]
    cell_all = F["cells"]
    lod_rows = []
    for nm in done:
        l = nm["line"]
        it = index_trials(P, l, nm["s3"]).set_index("trial")
        bi = cell_all[(cell_all["line"] == BENCH) & (cell_all["trial"].isin(it.index))].set_index("trial")
        ms = s[s["line"] == l].set_index("trial")
        at_index = float((100.0 * gam_c * (it["L"] - bi["L"].reindex(it.index)) / bi["yh"].reindex(it.index)).mean())
        at_series = 100.0 * gam_c * float((ms["L"] - sbl.reindex(ms.index)).sum()) / float(sbench.reindex(ms.index).sum())
        lod_rows.append(at_series - at_index)
    lodging_part = float(np.mean(lod_rows))
    lb, *_ = np.linalg.lstsq(np.column_stack([np.ones(len(d)), d["lod"]]), d["Ls"].to_numpy(float), rcond=None)
    beta, mbar, a, s2 = fit(P.last)
    m_h, b_h = float(smean.mean()), float(sbench.mean())
    pool = pool_of(P.last)
    out = []
    for l in P.cands:
        lev = level(a, s2, l, pool)
        raw = 100.0 + 100.0 * (lev + beta * (m_h - mbar)) / b_h
        lod = wet_lodging(l, P.last)
        ry = raw - a0 - cc * lod
        out.append(dict(line=l, ry=ry, lodging=float(np.clip(lb[0] + lb[1] * lod, 0.0, 100.0)),
                        lo=ry - 1.2816 * sd, hi=ry + 1.2816 * sd, p=_norm_p(ry, sd, float(P.standard))))
    cd = pd.DataFrame(out).sort_values("ry", ascending=False).reset_index(drop=True)
    ch = choose(cd, P.places)
    pe = cd[cd["line"].isin(ch["picks"])]["p"].tolist()
    own = float((d["quoted"] - d["B"]).mean())
    move = float((d["B"] - d["C"]).mean())          # its one response already carries what lodging does on average
    return dict(promised=promised, realised=realised, shortfall=promised - realised, own_sites=own,
                water_part=move - lodging_part, lodging_part=lodging_part, series_sites=move,
                left_over=float((d["C"] - d["D"]).mean()),
                rmse_method=float(np.sqrt(((bk["predicted"] - bk["realised"]) ** 2).mean())), back_rows=bk, cands=cd,
                picks=ch["picks"], next=ch["next"], margin=ch["margin"], p_each=pe,
                p_any=float(1.0 - np.prod([1.0 - p for p in pe])) if pe else None,
                p_all=float(np.prod(pe)) if pe else None, sd=sd, beta=[a0, cc], slope=beta, loss_per_tenth=gam_c)


def index_route(P):
    """The first story: the shortfall is regression to the mean, so scale the breeder's index by what the past
    nominees realised and keep its order."""
    F = fit_all(P, lodging=False)
    P._cells = F["cells"]
    s, tt = series_frame(P)
    done = [nm for nm in P.noms if s[s["line"] == nm["line"]]["season"].nunique() >= 2]
    x = np.array([nm["index"] for nm in done])
    yv = np.array([realised_ry(s, nm["line"]) for nm in done])
    b = float(np.cov(x, yv)[0, 1] / np.var(x, ddof=1))
    a0 = float(yv.mean() - b * x.mean())
    rows = [dict(line=l, ry=a0 + b * raw_index(P, l, P.s3_seasons[l])) for l in P.cands]
    cd = pd.DataFrame(rows).sort_values("ry", ascending=False).reset_index(drop=True)
    return dict(cands=cd, picks=choose(cd, P.places)["picks"], slope=b)
