"""task9: the estimators and the five-year simulation, shared by the golden analysis, the checks and the rivals.

A panel row is one company-year at risk: (company, year, fund, sector, rating, age, defaulted, house), age being the
full years since the buyout that began the current ownership (or, for a rival, since the loan began). Default rates
come from a probit on rating and age; dependence from random-effect probits fitted cluster by cluster (Gauss-Hermite
quadrature), each layer conditioned on the one above it; each sector's loading on the shared year from the marginal
likelihood over the year and sector-year factors; the forward years from a Gaussian factor simulation.
"""
import collections

import numpy as np
from scipy.optimize import minimize, minimize_scalar
from scipy.special import log_ndtr, logsumexp
from scipy.stats import norm

GH_X, GH_W = np.polynomial.hermite_e.hermegauss(40)
GH_W = GH_W / GH_W.sum()
MAXAGE = 7
NSECT = 16


def probit(X, y, ridge=None, prior=None, iters=60):
    b = np.zeros(X.shape[1])
    R = np.full(X.shape[1], 1e-6) if ridge is None else ridge
    pr = np.zeros(X.shape[1]) if prior is None else prior
    for _ in range(iters):
        eta = np.clip(X @ b, -7, 7)
        p = np.clip(norm.cdf(eta), 1e-10, 1 - 1e-10)
        phi = np.maximum(norm.pdf(eta), 1e-14)
        w = phi ** 2 / (p * (1 - p))
        z = eta + (y - p) / phi
        XtW = X.T * w
        bn = np.linalg.solve(XtW @ X + np.diag(R), XtW @ z + R * pr)
        if np.max(np.abs(bn - b)) < 1e-9:
            return bn
        b = bn
    return b


def _design(P, cells=None, maxage=MAXAGE):
    n = len(P)
    if cells is None:
        uc, ci = np.array([0]), np.zeros(n, dtype=int)
    else:
        uc, ci = np.unique(cells, return_inverse=True)
    nc = len(uc)
    X = np.zeros((n, nc + 3 + maxage - 1))
    X[np.arange(n), ci] = 1
    for r in (1, 2, 3):
        X[:, nc + r - 1] = (P[:, 4] == r)
    ag = np.clip(P[:, 5], 1, maxage)
    for a in range(2, maxage + 1):
        X[:, nc + 3 + a - 2] = (ag == a)
    return X, nc


def pd_table(P, maxage=MAXAGE):
    """Unconditional one-year default chance by rating and age (ages beyond maxage share the last level)."""
    X, nc = _design(P, None, maxage)
    b = probit(X, P[:, 6].astype(float))
    tab = np.zeros((4, 31))
    for r in range(4):
        for a in range(1, 31):
            x = np.zeros(X.shape[1])
            x[0] = 1
            if r:
                x[nc + r - 1] = 1
            aa = min(a, maxage)
            if aa >= 2:
                x[nc + 3 + aa - 2] = 1
            tab[r, a] = norm.cdf(x @ b)
    loglik = float(np.sum(np.where(P[:, 6] == 1, np.log(norm.cdf(X @ b)), np.log(1 - norm.cdf(X @ b)))))
    return tab, norm.cdf(np.clip(X @ b, -7, 7)), loglik


def cond_pd(P, cells, ridge_fe=0.5, maxage=MAXAGE):
    """Default chance with a fixed effect per cell (a year, or an industry-year), plus rating and age."""
    X, nc = _design(P, cells, maxage)
    R = np.full(X.shape[1], 1e-6)
    R[:nc] = ridge_fe
    pr = np.zeros(X.shape[1])
    pr[:nc] = -2.0
    b = probit(X, P[:, 6].astype(float), R, pr)
    return norm.cdf(np.clip(X @ b, -7, 7))


def cluster_mle(p, d, keys, lo=1e-4, hi=0.95):
    """Latent correlation c inside clusters: d_i ~ Bernoulli(Phi((Phi^-1(p_i) - sqrt(c) u) / sqrt(1 - c))), u shared."""
    groups = collections.defaultdict(list)
    for i, k in enumerate(keys):
        groups[k].append(i)
    # clusters with one member carry no information about c
    idx = [np.array(v) for k, v in sorted(groups.items(), key=lambda kv: str(kv[0])) if len(v) >= 2]
    t = norm.ppf(np.clip(p, 1e-10, 1 - 1e-10))

    def nll(c):
        s, q = np.sqrt(c), np.sqrt(1 - c)
        tot = 0.0
        for g in idx:
            pu = norm.cdf((t[g][:, None] - s * GH_X[None, :]) / q)
            lk = np.where(d[g][:, None] == 1, pu, 1 - pu)
            tot += np.log(max((np.prod(lk, axis=0) * GH_W).sum(), 1e-300))
        return -tot
    r = minimize_scalar(nll, bounds=(lo, hi), method="bounded", options={"xatol": 1e-5})
    return float(r.x), float(-r.fun), float(-nll(lo))


def estimate(P):
    """Every layer the golden reads, and the rivals' layers, from one panel."""
    tab, pu, ll_pd = pd_table(P)
    d = P[:, 6]
    am, ll_m, _ = cluster_mle(pu, d, list(P[:, 1]))
    pY = cond_pd(P, P[:, 1])
    ck, _, _ = cluster_mle(pY, d, list(zip(P[:, 1].tolist(), P[:, 3].tolist())))
    pKY = cond_pd(P, P[:, 1] * 100 + P[:, 3])
    ch, ll_h, ll_h0 = cluster_mle(pKY, d, list(zip(P[:, 1].tolist(), P[:, 7].tolist())))
    cf, ll_f, _ = cluster_mle(pKY, d, list(zip(P[:, 1].tolist(), P[:, 2].tolist())))
    cq, ll_q, _ = cluster_mle(pKY, d, list(P[:, 2].tolist()))
    cqh, ll_qh, _ = cluster_mle(pKY, d, list(P[:, 7].tolist()))
    ak = ck * (1 - am)
    k = 1 - am - ak
    return dict(pdt=tab, am=am, ak=ak, ck=ck, ch=ch, ah=ch * k, cf=cf, af=cf * k, cq=cq, aq=cq * k, cqh=cqh,
                aqh=cqh * k, ll_h=ll_h, ll_h0=ll_h0, ll_f=ll_f, ll_q=ll_q, ll_qh=ll_qh, ll_pd=ll_pd,
                n=int(len(P)), defaults=int(d.sum()))


def per_loan(port, am, ak, aks=None):
    """The economy's and the sector's shares for each loan: am a scalar or one loading per sector, aks (optional) one
    own-factor share per sector in place of the common ak."""
    k = port["k"]
    am_i = np.full(len(k), float(am)) if np.isscalar(am) else np.asarray(am, dtype=float)[k]
    ak_i = np.full(len(k), float(ak)) if aks is None else np.asarray(aks, dtype=float)[k]
    return am_i, ak_i


def simulate(port, pdt, am, ak=0.0, ah=0.0, af=0.0, aq=0.0, lgd=0.37, nsim=1_000_000, years=5, seed=27,
             chunk=100_000, frozen=False, link=None, aks=None):
    """Cumulative portfolio credit loss (share of par) at the end of each forward year, nsim paths.

    port: dict of arrays w (par weights summing to one), r (rating 0-3), a (full years since buyout at the start),
    k (sector 0-15), h (house id), f (fund id). am is the economy's share, one for every loan or one per sector; aks,
    when given, replaces the common sector share ak sector by sector. aq is a persistent fund effect drawn once for
    the five years. link (a, bm, bh): each default recovers a + bm z_year + bh z_house of its exposure, from the same
    year and house shocks that drew the default; without it every default loses lgd."""
    n = len(port["w"])
    uh, hi = np.unique(port["h"], return_inverse=True)
    uf, fi = np.unique(port["f"], return_inverse=True)
    am_i, ak_i = per_loan(port, am, ak, aks)
    resid = np.sqrt(np.maximum(1.0 - am_i - ak_i - ah - af - aq, 1e-12))
    rng = np.random.default_rng(seed)
    out = np.zeros((years, nsim))
    step = 0 if frozen else 1
    thr = np.array([norm.ppf(pdt[port["r"], np.minimum(port["a"] + step * t, pdt.shape[1] - 1)]) for t in range(years)])
    for s0 in range(0, nsim, chunk):
        m = min(chunk, nsim - s0)
        loss = np.zeros(m)
        alive = np.ones((m, n), dtype=bool)
        Q = rng.standard_normal((m, len(uf)))[:, fi] if aq > 0 else 0.0
        for t in range(years):
            zm = rng.standard_normal((m, 1))
            x = (np.sqrt(am_i)[None, :] * zm
                 + np.sqrt(ak_i)[None, :] * rng.standard_normal((m, NSECT))[:, port["k"]]
                 + resid[None, :] * rng.standard_normal((m, n)))
            zh = 0.0
            if ah > 0:
                zh = rng.standard_normal((m, len(uh)))[:, hi]
                x += np.sqrt(ah) * zh
            if af > 0:
                x += np.sqrt(af) * rng.standard_normal((m, len(uf)))[:, fi]
            if aq > 0:
                x += np.sqrt(aq) * Q
            dd = (x < thr[t][None, :]) & alive
            if link is None:
                loss += (dd * port["w"]).sum(axis=1) * lgd
            else:
                a, bm, bh = link
                rec = np.clip(a + bm * zm + bh * zh, 0.0, 1.0)
                loss += (dd * port["w"] * (1.0 - rec)).sum(axis=1)
            alive &= ~dd
            out[t, s0:s0 + m] = loss
    return out


def simulate_count(port, book, pdt, am, ak=0.0, ah=0.0, rec=None, whole=False, nsim=200_000, years=5, seed=27,
                   chunk=25_000):
    """Cumulative portfolio credit loss when each default recovers by how many other companies of its house default in
    the same year (the rival read off the record's co-default counts): counted among the note's own loans (whole False)
    or over the house's whole book, the note's loans with the house's other companies at risk at the end of 2026 in the
    record (whole True). book: arrays r, a, k, h of those other companies; rec maps an array of counts to recoveries."""
    n = len(port["w"])
    cat = lambda f: np.concatenate([port[f], book[f]]) if whole and len(book["h"]) else port[f]
    hh, rr, aa, kk = cat("h"), cat("r"), cat("a"), cat("k")
    N = len(hh)
    uh, hi = np.unique(hh, return_inverse=True)
    onehot = np.zeros((N, len(uh)))
    onehot[np.arange(N), hi] = 1.0
    am_i, ak_i = per_loan(dict(k=kk), am, ak)
    resid = np.sqrt(np.maximum(1.0 - am_i - ak_i - ah, 1e-12))
    rng = np.random.default_rng(seed)
    out = np.zeros((years, nsim))
    thr = np.array([norm.ppf(pdt[rr, np.minimum(aa + t, pdt.shape[1] - 1)]) for t in range(years)])
    for s0 in range(0, nsim, chunk):
        m = min(chunk, nsim - s0)
        loss = np.zeros(m)
        alive = np.ones((m, N), dtype=bool)
        for t in range(years):
            x = (np.sqrt(am_i)[None, :] * rng.standard_normal((m, 1))
                 + np.sqrt(ak_i)[None, :] * rng.standard_normal((m, NSECT))[:, kk]
                 + np.sqrt(ah) * rng.standard_normal((m, len(uh)))[:, hi]
                 + resid[None, :] * rng.standard_normal((m, N)))
            dd = (x < thr[t][None, :]) & alive
            others = (dd.astype(float) @ onehot)[:, hi[:n]] - 1.0
            r = np.clip(rec(others), 0.0, 1.0)
            loss += (dd[:, :n] * port["w"] * (1.0 - r)).sum(axis=1)
            alive &= ~dd
            out[t, s0:s0 + m] = loss
    return out


def summary(cum, sub, targets=(0.01, 0.005, 0.0025), grid=None):
    """Chance of a loss on a note with subordination sub by each year end, the subordination each target chance
    needs over the five years, and the exceedance curve of five-year losses."""
    by_year = [float((cum[t] > sub).mean()) for t in range(cum.shape[0])]
    L = cum[-1]
    need = [float(np.quantile(L, 1 - p)) for p in targets]
    grid = np.round(np.arange(0.0, 0.3001, 0.005), 3) if grid is None else grid
    exc = [float((L > g).mean()) for g in grid]
    el = float(np.mean(np.clip(L - sub, 0, 1 - sub)) / (1 - sub))
    return dict(by_year=by_year, p5=by_year[-1], need=need, grid=[float(g) for g in grid], exceed=exc,
                el_note=el, el_port=float(L.mean()))


def cohort_pdt(P, maxage=MAXAGE, k=200.0):
    """A cohort table of one-year default rates by rating and age, each cell shrunk toward the rating's rate times the
    age's relativity with the weight of k company-years (the rival to the probit)."""
    d = P[:, 6].astype(float)
    ag = np.clip(P[:, 5], 1, maxage)
    base = d.mean()
    rr = np.array([d[P[:, 4] == r].mean() for r in range(4)])
    ar = np.array([d[ag == a].mean() / base if (ag == a).any() else 1.0 for a in range(maxage + 1)])
    tab = np.zeros((4, 31))
    for r in range(4):
        for a in range(1, 31):
            aa = min(a, maxage)
            m = (P[:, 4] == r) & (ag == aa)
            prior = rr[r] * ar[aa]
            tab[r, a] = (d[m].sum() + k * prior) / (m.sum() + k)
    return tab


def _joint(rho, p):
    from scipy.stats import multivariate_normal
    t = norm.ppf(p)
    return float(multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf([t, t]))


def moment_dependence(P):
    """The rival dependence estimator: the economy's share from the excess variance of yearly default rates, the
    sector's and the house's from joint defaults of pairs in the same sector-year across houses and in the same house,
    each inverted through the bivariate normal at the record's mean default rate."""
    from scipy.optimize import brentq
    d = P[:, 6].astype(float)
    pbar = d.mean()
    years = sorted(set(P[:, 1].tolist()))
    rates = np.array([d[P[:, 1] == y].mean() for y in years])
    ns = np.array([(P[:, 1] == y).sum() for y in years])
    ex = rates.var() - np.mean(pbar * (1 - pbar) / ns)
    am = brentq(lambda r: _joint(r, pbar) - pbar * pbar - ex, 1e-4, 0.9)

    def pairs(cols):
        g = collections.defaultdict(lambda: [0, 0])
        for row in P:
            key = tuple(int(row[c]) for c in cols)
            g[key][0] += 1
            g[key][1] += int(row[6])
        n = sum(v[0] * (v[0] - 1) / 2 for v in g.values())
        j = sum(v[1] * (v[1] - 1) / 2 for v in g.values())
        return j, n
    j_ky, n_ky = pairs((1, 3))
    j_hky, n_hky = pairs((1, 3, 7))
    q_cross = (j_ky - j_hky) / (n_ky - n_hky)
    q_house = j_hky / n_hky
    rho_ky = brentq(lambda r: _joint(r, pbar) - q_cross, 1e-4, 0.95)
    rho_hky = brentq(lambda r: _joint(r, pbar) - q_house, 1e-4, 0.98)
    ak = max(rho_ky - am, 0.0)
    ah = max(rho_hky - rho_ky, 0.0)
    return dict(am=am, ak=ak, ah=ah)


# ---------------------------------------------------------------- each sector's loading on the shared year
ZX, ZW = np.polynomial.hermite_e.hermegauss(20)
LZW = np.log(ZW / ZW.sum())
EX, EW = np.polynomial.hermite_e.hermegauss(10)
LEW = np.log(EW / EW.sum())


def _sector_cells(P, pdt):
    """Company-years grouped by year, sector and rating-age threshold, with their counts and defaults."""
    p = pdt[P[:, 4], np.minimum(P[:, 5], pdt.shape[1] - 1)]
    t = np.round(norm.ppf(p), 8)
    cells = collections.defaultdict(lambda: [0, 0])
    for y, k, tt, d in zip(P[:, 1].tolist(), P[:, 3].tolist(), t.tolist(), P[:, 6].tolist()):
        c = cells[(y, k, tt)]
        c[0] += 1
        c[1] += d
    keys = sorted(cells)
    years = sorted(set(k[0] for k in keys))
    yi = {y: i for i, y in enumerate(years)}
    Y = np.array([yi[k[0]] for k in keys])
    S = np.array([k[1] for k in keys])
    return dict(S=S, T=np.array([k[2] for k in keys]), N=np.array([cells[k][0] for k in keys], float),
                D=np.array([cells[k][1] for k in keys], float), cell=Y * NSECT + S, ny=len(years))


def _sector_loglik(l, k, dat):
    """The record's log-likelihood with the year's shock shared by every sector, sector s loading l[s] on it, and a
    sector-year shock of share k, both integrated out (Gauss-Hermite)."""
    sl = np.sqrt(l[dat["S"]])
    q = np.sqrt(np.maximum(1 - l[dat["S"]] - k, 1e-9))
    arg = (dat["T"][:, None, None] - sl[:, None, None] * ZX[None, :, None] - np.sqrt(k) * EX[None, None, :]) / q[:, None, None]
    g = dat["D"][:, None, None] * log_ndtr(arg) + (dat["N"] - dat["D"])[:, None, None] * log_ndtr(-arg)
    acc = np.zeros((dat["ny"] * NSECT, len(ZX), len(EX)))
    np.add.at(acc, dat["cell"], g)
    inner = logsumexp(acc + LEW[None, None, :], axis=2)
    yz = inner.reshape(dat["ny"], NSECT, len(ZX)).sum(axis=1)
    return float(logsumexp(yz + LZW[None, :], axis=1).sum())


def sector_loadings(P, pdt, groups=None):
    """Each sector's loading on the year's shock (groups: sector -> parameter index, None for one loading per sector)
    and the sector-year share, by maximum likelihood. Returns the loadings by sector, the share and the
    log-likelihood."""
    dat = _sector_cells(P, pdt)
    g = np.arange(NSECT) if groups is None else np.asarray(groups)
    ng = int(g.max()) + 1

    def unpack(th):
        return (0.6 / (1 + np.exp(-th[:ng])))[g], 0.3 / (1 + np.exp(-th[ng]))

    def f(th):
        l, k = unpack(th)
        return -_sector_loglik(l, k, dat)
    r = minimize(f, np.full(ng + 1, -1.5), method="L-BFGS-B", options={"maxiter": 400})
    l, k = unpack(r.x)
    return dict(l=l, k=float(k), loglik=float(-r.fun), groups=g.tolist())


def house_share_latent(P, pKY, l, k):
    """The house-year's share of each standing on the latent scale: inside its sector-year a company's correlation
    with its house-year's other companies is ah / (1 - l_s - k), its sector's room once the year and the sector-year
    are known."""
    groups = collections.defaultdict(list)
    for i, key in enumerate(zip(P[:, 1].tolist(), P[:, 7].tolist())):
        groups[key].append(i)
    idx = [np.array(v) for k_, v in sorted(groups.items()) if len(v) >= 2]
    t = norm.ppf(np.clip(pKY, 1e-10, 1 - 1e-10))
    room = 1 - np.asarray(l)[P[:, 3]] - k
    d = P[:, 6]

    def nll(ah):
        tot = 0.0
        for gi in idx:
            c = np.clip(ah / room[gi], 1e-6, 0.999)
            pu = norm.cdf((t[gi][:, None] - np.sqrt(c)[:, None] * GH_X[None, :]) / np.sqrt(1 - c)[:, None])
            lk = np.where(d[gi][:, None] == 1, pu, 1 - pu)
            tot += np.log(max((np.prod(lk, axis=0) * GH_W).sum(), 1e-300))
        return -tot
    r = minimize_scalar(nll, bounds=(1e-3, 0.6), method="bounded", options={"xatol": 1e-5})
    return float(r.x)


def moment_loadings(P):
    """The rival loading estimator, pair moments with nothing integrated: for each two sectors, the share of their
    company pairs at risk in the same year (held by different houses) that both defaulted, inverted through the
    bivariate normal at each sector's own default rate to a latent correlation, and one loading per sector fitted to
    those correlations as the product of the two sectors' square roots (least squares weighted by the pairs)."""
    from scipy.optimize import brentq, least_squares
    d = P[:, 6].astype(np.int64)
    ns, dsum = np.zeros((NSECT, 1 + int(P[:, 1].max()) - int(P[:, 1].min()))), None
    y0 = int(P[:, 1].min())
    n_sy = np.zeros((NSECT, ns.shape[1]))
    d_sy = np.zeros((NSECT, ns.shape[1]))
    np.add.at(n_sy, (P[:, 3], P[:, 1] - y0), 1)
    np.add.at(d_sy, (P[:, 3], P[:, 1] - y0), d)
    N = n_sy @ n_sy.T
    J = d_sy @ d_sy.T
    # same-house pairs across sectors carry the house's year too: take them out
    hy = collections.defaultdict(lambda: np.zeros((NSECT, 2)))
    for row in P:
        c = hy[(int(row[7]), int(row[1]))]
        c[int(row[3]), 0] += 1
        c[int(row[3]), 1] += int(row[6])
    for c in hy.values():
        N -= np.outer(c[:, 0], c[:, 0])
        J -= np.outer(c[:, 1], c[:, 1])
    pr = np.clip(d_sy.sum(axis=1) / n_sy.sum(axis=1), 1e-4, 0.5)
    t = norm.ppf(pr)
    rows, w, rho = [], [], []
    for a in range(NSECT):
        for b in range(a + 1, NSECT):
            if N[a, b] <= 0:
                continue
            q = J[a, b] / N[a, b]
            f = lambda r: _bvn(t[a], t[b], r) - q
            lo_, hi_ = f(-0.5), f(0.95)
            r = brentq(f, -0.5, 0.95) if lo_ < 0 < hi_ else (-0.5 if lo_ >= 0 else 0.95)
            rows.append((a, b))
            w.append(np.sqrt(N[a, b]))
            rho.append(r)
    rows, w, rho = np.array(rows), np.array(w), np.array(rho)
    res = least_squares(lambda x: w * (x[rows[:, 0]] * x[rows[:, 1]] - rho), np.full(NSECT, 0.2),
                        bounds=(0.0, 0.8))
    return np.clip(res.x ** 2, 0.0, 0.6)


def _bvn(a, b, rho):
    from scipy.stats import multivariate_normal
    return float(multivariate_normal(mean=[0, 0], cov=[[1, rho], [rho, 1]]).cdf([a, b]))


def year_posterior(P, pdt, l, k):
    """Each year's shock as its posterior mean given every sector's defaults that year, sector s loading l[s] on it
    and the sector-year shock integrated out (the same likelihood as sector_loadings)."""
    dat = _sector_cells(P, pdt)
    sl = np.sqrt(np.asarray(l)[dat["S"]])
    q = np.sqrt(np.maximum(1 - np.asarray(l)[dat["S"]] - k, 1e-9))
    arg = (dat["T"][:, None, None] - sl[:, None, None] * ZX[None, :, None] - np.sqrt(k) * EX[None, None, :]) / q[:, None, None]
    g = dat["D"][:, None, None] * log_ndtr(arg) + (dat["N"] - dat["D"])[:, None, None] * log_ndtr(-arg)
    acc = np.zeros((dat["ny"] * NSECT, len(ZX), len(EX)))
    np.add.at(acc, dat["cell"], g)
    inner = logsumexp(acc + LEW[None, None, :], axis=2)
    yz = inner.reshape(dat["ny"], NSECT, len(ZX)).sum(axis=1) + LZW[None, :]
    w = np.exp(yz - yz.max(axis=1, keepdims=True))
    post = (w * ZX[None, :]).sum(axis=1) / w.sum(axis=1)
    years = sorted(set(P[:, 1].tolist()))
    return {y: float(v) for y, v in zip(years, post)}


def _bvn_grid(ta, tb, grid):
    """Bivariate normal orthant probabilities P(X < ta, Y < tb) on a grid of correlations, by Gauss-Legendre on
    Plackett's identity d/drho = phi2(ta, tb; rho)."""
    gx, gw = np.polynomial.legendre.leggauss(24)
    base = norm.cdf(ta) * norm.cdf(tb)
    out = []
    for r in grid:
        u = 0.5 * r * (gx + 1)
        w = 0.5 * r * gw
        dens = np.exp(-(ta * ta - 2 * u * ta * tb + tb * tb) / (2 * (1 - u * u))) / (2 * np.pi * np.sqrt(1 - u * u))
        out.append(base + float((w * dens).sum()))
    return np.array(out)


def moment_house_share(P, pdt, l, k):
    """The house-year's share by pair moments: every pair of companies held by one house and at risk in the same year,
    each pair's joint default chance through the bivariate normal at its two companies' own one-year rates (rating and
    years since the buyout) and their correlation without the house (the product of their sectors' square-root loadings
    on the year, plus the sector-year's share for a pair in one sector), the house's share the one number that makes the
    expected joint defaults the record's."""
    from scipy.optimize import brentq
    cls = np.minimum(P[:, 5], MAXAGE) - 1 + MAXAGE * P[:, 4]
    tcls = np.array([norm.ppf(pdt[c // MAXAGE, c % MAXAGE + 1]) for c in range(4 * MAXAGE)])
    sl = np.sqrt(np.asarray(l))
    cnt = collections.Counter()
    joint = 0
    groups = collections.defaultdict(list)
    for row, c in zip(P, cls):
        groups[(int(row[1]), int(row[7]))].append((int(c), int(row[3]), int(row[6])))
    for g in groups.values():
        n = len(g)
        if n < 2:
            continue
        nd = sum(x[2] for x in g)
        joint += nd * (nd - 1) // 2
        for i_ in range(n):
            for j_ in range(i_ + 1, n):
                a, b = g[i_], g[j_]
                base = sl[a[1]] * sl[b[1]] + (k if a[1] == b[1] else 0.0)
                key = (min(a[0], b[0]), max(a[0], b[0]), round(base, 4))
                cnt[key] += 1
    keys = list(cnt)
    ta = np.array([tcls[x[0]] for x in keys])
    tb = np.array([tcls[x[1]] for x in keys])
    bs = np.array([x[2] for x in keys])
    nn = np.array([cnt[x] for x in keys], float)
    gx, gw = np.polynomial.legendre.leggauss(24)

    def expected(ah):
        r = np.clip(bs + ah, 0.0, 0.97)
        base = norm.cdf(ta) * norm.cdf(tb)
        u = 0.5 * r[:, None] * (gx[None, :] + 1)
        w = 0.5 * r[:, None] * gw[None, :]
        dens = np.exp(-(ta[:, None] ** 2 - 2 * u * ta[:, None] * tb[:, None] + tb[:, None] ** 2) / (2 * (1 - u * u))) \
            / (2 * np.pi * np.sqrt(1 - u * u))
        return float((nn * (base + (w * dens).sum(axis=1))).sum())
    f = lambda ah: expected(ah) - joint
    return float(brentq(f, 0.0, 0.9)) if f(0.0) < 0 < f(0.9) else (0.0 if f(0.0) >= 0 else 0.9)
