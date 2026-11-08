"""task3: flood frequency the Bulletin 17C way, for every route the checks and the golden run.

Log-Pearson Type III on the base-10 logarithms of annual peaks: the moments of the logs (the expected moments
algorithm reduces to them on a complete record with no low floods censored), the station skew weighted with the
regional skew by their mean square errors, and the Multiple Grubbs-Beck test for potentially influential low floods
(null distributions of its order statistics simulated once, seeded). When the test flags low floods they are treated
as censored below the threshold and the moments re-estimated by the expected moments algorithm.
"""
import functools

import numpy as np
from scipy import stats

REGIONAL_SKEW = -0.12       # the state's Region 3 regional skew (state equations report, table 4)
REGIONAL_SKEW_MSE = 0.13


def skew_mse(g, n):
    """Mean square error of a station skew (Bulletin 17B/17C approximation, Wallis-Matalas-Slack form)."""
    g = abs(g)
    a = -0.33 + 0.08 * g if g <= 0.90 else -0.52 + 0.30 * g
    b = 0.94 - 0.26 * g if g <= 1.50 else 0.55
    return 10 ** (a - b * np.log10(n / 10.0))


def weighted_skew(gs, n, gr=REGIONAL_SKEW, mse_r=REGIONAL_SKEW_MSE):
    mse_s = skew_mse(gs, n)
    return (mse_r * gs + mse_s * gr) / (mse_r + mse_s)


@functools.lru_cache(maxsize=None)
def _mgbt_null(n, nsim=20000, seed=17):
    """Simulated null distribution of the Grubbs-Beck statistic for each k (the k-th smallest against the moments of
    the observations above it) in normal samples of size n."""
    rng = np.random.default_rng(seed)
    x = np.sort(rng.standard_normal((nsim, n)), axis=1)
    kmax = n // 2
    out = np.zeros((kmax, nsim))
    for k in range(1, kmax + 1):
        rest = x[:, k:]
        out[k - 1] = (x[:, k - 1] - rest.mean(axis=1)) / rest.std(axis=1, ddof=1)
    return np.sort(out, axis=1)


def mgbt(q, alpha_out=0.005, alpha_in=0.10):
    """Number of potentially influential low floods and the threshold (the smallest retained flood)."""
    lx = np.sort(np.log10(np.asarray(q, float)))
    n = len(lx)
    null = _mgbt_null(n)
    kmax = n // 2
    p = np.zeros(kmax)
    for k in range(1, kmax + 1):
        rest = lx[k:]
        w = (lx[k - 1] - rest.mean()) / rest.std(ddof=1)
        p[k - 1] = np.searchsorted(null[k - 1], w) / null.shape[1]
    out = 0
    for k in range(kmax, 0, -1):          # outward from the median
        if p[k - 1] < alpha_out:
            out = k
            break
    inward = 0
    for k in range(1, kmax + 1):          # inward from the smallest, consecutive
        if p[k - 1] < alpha_in:
            inward = k
        else:
            break
    m = max(out, inward)
    return m, (10 ** lx[m] if m else None), p


def _cond_moments(m, s, g, thr):
    """E[X], E[X^2], E[X^3] for X log-Pearson III (logs: mean m, sd s, skew g) given X < thr, by integration."""
    from scipy.integrate import quad
    dist = stats.pearson3(g, loc=m, scale=s)
    lo = dist.ppf(1e-12)
    F = dist.cdf(thr)
    if F <= 1e-15:
        return thr, thr ** 2, thr ** 3
    out = []
    for k in (1, 2, 3):
        v, _ = quad(lambda x: x ** k * dist.pdf(x), lo, thr, limit=200)
        out.append(v / F)
    return tuple(out)


def _ema(lx, nlow, thr, gfix=None):
    """Expected moments on logs with nlow observations known only to lie below thr (log10)."""
    obs = lx[lx >= thr] if nlow else lx
    n = len(lx)
    m, s, g = obs.mean(), obs.std(ddof=1), stats.skew(obs, bias=False)
    if not nlow:
        return m, s, g
    for _ in range(300):
        gg = g if gfix is None else gfix
        e1, e2, e3 = _cond_moments(m, s, gg, thr)
        mn = (obs.sum() + nlow * e1) / n
        S2 = ((obs - mn) ** 2).sum() + nlow * (e2 - 2 * mn * e1 + mn ** 2)
        sn = np.sqrt(S2 / (n - 1))
        S3 = ((obs - mn) ** 3).sum() + nlow * (e3 - 3 * mn * e2 + 3 * mn ** 2 * e1 - mn ** 3)
        gn = n * S3 / ((n - 1) * (n - 2) * sn ** 3)
        done = abs(mn - m) < 1e-10 and abs(sn - s) < 1e-10 and abs(gn - g) < 1e-9
        m, s, g = mn, sn, gn
        if done:
            break
    return m, s, g


def fit(q, regional=True, low_test=True, extra_low=0):
    """Bulletin 17C log-Pearson III parameters (mean, sd, skew used) for an annual series; a dict. extra_low years are
    known only to lie below the low-flood threshold (below the smallest peak when the test flags none)."""
    q = np.asarray(q, float)
    nlow, thr = 0, None
    if low_test:
        nlow, thrq, _ = mgbt(q)
        thr = np.log10(thrq) if nlow else None
    if extra_low:
        if thr is None:
            thr = np.log10(q.min())
        q = np.concatenate([q, np.full(extra_low, 10 ** thr * 0.5)])
        nlow += extra_low
    lx = np.log10(q)
    n = len(lx)
    m, s, gs = _ema(lx, nlow, thr) if nlow else (lx.mean(), lx.std(ddof=1), stats.skew(lx, bias=False))
    g = weighted_skew(gs, n) if regional else gs
    if nlow:
        m, s, _ = _ema(lx, nlow, thr, gfix=g)
    return dict(mean=float(m), sd=float(s), station_skew=float(gs), skew=float(g), n=n, low=nlow,
                low_threshold=(float(10 ** thr) if nlow else None))


def quantile(par, aep):
    return float(10 ** (par["mean"] + stats.pearson3.ppf(1 - aep, par["skew"]) * par["sd"]))


def aep_of(par, q):
    """Annual exceedance probability of flow q under the fitted curve."""
    z = (np.log10(q) - par["mean"]) / par["sd"]
    return float(1 - stats.pearson3.cdf(z, par["skew"]))
