"""task8: score linking on integer score scales (Kolen and Brennan's continuized equipercentile method).

A score distribution is (points, probabilities) on consecutive integers. Each is continuized with a uniform kernel
over [k - 0.5, k + 0.5); a score x on scale X is linked to scale Y at the Y value with the same continuized
percentile. Log-linear presmoothing (degree C, the first C moments kept) is optional. Chained linking composes two
links through an anchor; frequency estimation and linear methods are the rivals."""
import numpy as np


def dist(scores, lo, hi, weights=None):
    pts = np.arange(lo, hi + 1)
    s = np.clip(np.asarray(scores, float), lo, hi).round().astype(int)
    w = np.ones(len(s)) if weights is None else np.asarray(weights, float)
    f = np.bincount(s - lo, weights=w, minlength=len(pts)).astype(float)
    return pts, f / f.sum()


def smooth(pts, f, n, degree):
    """Log-linear presmoothing: the fitted frequencies keep the first `degree` moments of the observed ones."""
    if not degree:
        return f
    x = (pts - pts.mean()) / (pts.std() or 1.0)
    X = np.column_stack([x ** k for k in range(degree + 1)])
    y = f * n
    b = np.zeros(degree + 1)
    b[0] = np.log(max(y.mean(), 1e-9))
    for _ in range(200):
        mu = np.exp(np.clip(X @ b, -30, 30))
        g = X.T @ (y - mu)
        H = X.T @ (X * mu[:, None]) + 1e-9 * np.eye(degree + 1)
        step = np.linalg.solve(H, g)
        b += step
        if np.max(np.abs(step)) < 1e-10:
            break
    mu = np.exp(np.clip(X @ b, -30, 30))
    return mu / mu.sum()


def cdf_star(pts, f, t):
    """Continuized cumulative proportion at real t."""
    t = np.atleast_1d(np.asarray(t, float))
    F = np.concatenate([[0.0], np.cumsum(f)])
    lo = pts[0]
    k = np.clip(np.floor(t + 0.5).astype(int) - lo, 0, len(pts) - 1)
    frac = np.clip(t - (pts[k] - 0.5), 0.0, 1.0)
    out = F[k] + f[k] * frac
    out = np.where(t < pts[0] - 0.5, 0.0, out)
    out = np.where(t >= pts[-1] + 0.5, 1.0, out)
    return out


def inv_star(pts, f, p):
    p = np.atleast_1d(np.asarray(p, float))
    F = np.cumsum(f)
    Fm = F - f
    k = np.searchsorted(F, p, side="right")
    k = np.clip(k, 0, len(pts) - 1)
    fk = np.maximum(f[k], 1e-12)
    t = (pts[k] - 0.5) + (p - Fm[k]) / fk
    return np.clip(t, pts[0] - 0.5, pts[-1] + 0.5)


class Equi:
    """The equipercentile link of scale X onto scale Y from two distributions (same population or two)."""

    def __init__(self, dx, dy):
        self.dx, self.dy = dx, dy

    def __call__(self, x):
        return inv_star(*self.dy, cdf_star(*self.dx, x))


class Chain:
    def __init__(self, *links):
        self.links = links

    def __call__(self, x):
        for l in self.links:
            x = l(x)
        return x


class Linear:
    def __init__(self, mx, sx, my, sy):
        self.mx, self.sx, self.my, self.sy = mx, sx, my, sy

    def __call__(self, x):
        return self.my + self.sy / self.sx * (np.asarray(x, float) - self.mx)


def equi(x_scores, y_scores, xr, yr, degree=0, wx=None, wy=None):
    px, fx = dist(x_scores, *xr, wx)
    py, fy = dist(y_scores, *yr, wy)
    fx = smooth(px, fx, len(x_scores), degree)
    fy = smooth(py, fy, len(y_scores), degree)
    return Equi((px, fx), (py, fy))


def linear(x_scores, y_scores):
    x, y = np.asarray(x_scores, float), np.asarray(y_scores, float)
    return Linear(x.mean(), x.std(), y.mean(), y.std())


def freq_estimation(x1, a1, a2, y2, xr, ar, yr, w1=0.5, degree=0):
    """Frequency estimation (post-stratification) in a NEAT design: group 1 took X and anchor A, group 2 took Y and
    A; the conditional distributions of X given A (group 1) and Y given A (group 2) are carried to a synthetic
    population with weight w1 on group 1. Returns the equipercentile link of X onto Y in that population."""
    x1, a1, a2, y2 = (np.asarray(v, float) for v in (x1, a1, a2, y2))
    apts = np.arange(ar[0], ar[1] + 1)
    pa1 = dist(a1, *ar)[1]
    pa2 = dist(a2, *ar)[1]
    xp = np.arange(xr[0], xr[1] + 1)
    yp = np.arange(yr[0], yr[1] + 1)

    def cond(scores, anchors, pts, lo, hi):
        tab = np.zeros((len(apts), len(pts)))
        sa = np.clip(anchors.round().astype(int), *ar) - ar[0]
        ss = np.clip(scores.round().astype(int), lo, hi) - lo
        np.add.at(tab, (sa, ss), 1.0)
        rows = tab.sum(1, keepdims=True)
        # anchor points with no cases borrow their neighbours' conditional distribution
        out = np.where(rows > 0, tab / np.maximum(rows, 1e-12), np.nan)
        for i in range(len(apts)):
            if np.isnan(out[i]).all():
                j = np.argmin(np.where(rows[:, 0] > 0, np.abs(np.arange(len(apts)) - i), 10 ** 9))
                out[i] = out[j]
        return out

    cx = cond(x1, a1, xp, *xr)
    cy = cond(y2, a2, yp, *yr)
    pa = w1 * pa1 + (1 - w1) * pa2
    fx = pa @ cx
    fy = pa @ cy
    fx = smooth(xp, fx, len(x1), degree)
    fy = smooth(yp, fy, len(y2), degree)
    return Equi((xp, fx), (yp, fy))
