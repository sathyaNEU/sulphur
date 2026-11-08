"""Flood-frequency fits used by the golden and the checks: log-Pearson III by moments of the base-10 logs with the
station skew (the Bulletin 17C form without a regional skew), and the generalized extreme value by L-moments."""
import numpy as np
from scipy import stats
from scipy.special import gamma as G


def lmoments(x):
    x = np.sort(np.asarray(x, dtype=float)); n = len(x); i = np.arange(1, n + 1)
    b0 = x.mean()
    b1 = np.sum((i - 1) / (n - 1) * x) / n
    b2 = np.sum((i - 1) * (i - 2) / ((n - 1) * (n - 2)) * x) / n
    l1, l2, l3 = b0, 2 * b1 - b0, 6 * b2 - 6 * b1 + b0
    return l1, l2, l3 / l2


def gev_quantile(x, aep):
    l1, l2, t3 = lmoments(x)
    c = 2 / (3 + t3) - np.log(2) / np.log(3)
    k = 7.8590 * c + 2.9554 * c * c
    a = l2 * k / ((1 - 2 ** -k) * G(1 + k))
    xi = l1 - a * (1 - G(1 + k)) / k
    return xi + a / k * (1 - (-np.log(1 - aep)) ** k)


def lp3_quantile(x, aep):
    lx = np.log10(np.asarray(x, dtype=float))
    m, s, g = lx.mean(), lx.std(ddof=1), stats.skew(lx, bias=False)
    return 10 ** (m + s * stats.pearson3.ppf(1 - aep, g))
