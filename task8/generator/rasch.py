"""task8: Rasch estimation on a sittings-by-items matrix with NaN where an item was not presented.

jml      joint maximum likelihood, item difficulties and person abilities, the scale fixed by the mean of a set of
         anchor items; an optional person-by-item offset adds to each difficulty (a known shift)
wle      Warm's weighted likelihood abilities with difficulties fixed
mml      marginal maximum likelihood with a normal population (EM on Gauss-Hermite nodes), a rival estimator
fit      infit and outfit mean squares
"""
import numpy as np

CLIP = 6.0


def sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def _prep(X):
    M = ~np.isnan(X)
    Xz = np.where(M, X, 0.0)
    return Xz, M.astype(float)


def jml(X, anchors, anchor_mean, offset=None, iters=400, tol=1e-7, b0=None):
    """Returns dict(theta, b, se, extreme). Persons with a zero or perfect score are left out of the item
    estimation (their abilities come from wle afterwards)."""
    Xz, M = _prep(X)
    n, I = X.shape
    off = np.zeros((n, I)) if offset is None else offset
    raw = (Xz * M).sum(1)
    cnt = M.sum(1)
    extreme = (raw == 0) | (raw == cnt)
    keep = ~extreme
    Xk, Mk, Ok = Xz[keep], M[keep], off[keep]
    has = Mk.sum(0) > 0
    b = np.zeros(I) if b0 is None else np.nan_to_num(b0.copy())
    th = np.zeros(Xk.shape[0])
    anchors = np.asarray(anchors)
    for _ in range(iters):
        p = sig(th[:, None] - b[None, :] - Ok)
        w = p * (1 - p) * Mk
        th_new = np.clip(th + ((Xk - p) * Mk).sum(1) / np.maximum(w.sum(1), 1e-9), -CLIP, CLIP)
        p = sig(th_new[:, None] - b[None, :] - Ok)
        w = p * (1 - p) * Mk
        b_new = np.where(has, np.clip(b - ((Xk - p) * Mk).sum(0) / np.maximum(w.sum(0), 1e-9), -CLIP, CLIP), 0.0)
        shift = b_new[anchors].mean() - anchor_mean
        b_new -= shift
        th_new -= shift
        delta = max(np.abs(b_new - b).max(), np.abs(th_new - th).max())
        b, th = b_new, th_new
        if delta < tol:
            break
    p = sig(th[:, None] - b[None, :] - Ok)
    info = (p * (1 - p) * Mk).sum(0)
    se = np.where(has, 1.0 / np.sqrt(np.maximum(info, 1e-9)), np.nan)
    b = np.where(has, b, np.nan)
    theta = np.full(n, np.nan)
    theta[keep] = th
    return dict(theta=theta, b=b, se=se, extreme=extreme)


def wle(X, b, offset=None, iters=60):
    """Warm's weighted likelihood ability for every row, difficulties b fixed (NaN items ignored)."""
    Xz, M = _prep(X)
    bb = np.nan_to_num(b)
    M = M * (~np.isnan(b))[None, :]
    n, I = X.shape
    off = np.zeros((n, I)) if offset is None else offset
    th = np.zeros(n)
    for _ in range(iters):
        p = sig(th[:, None] - bb[None, :] - off)
        q = p * (1 - p) * M
        info = q.sum(1)
        g = ((Xz - p) * M).sum(1) + (q * (1 - 2 * p)).sum(1) / np.maximum(2 * info, 1e-9)
        th = np.clip(th + g / np.maximum(info, 1e-9), -CLIP, CLIP)
    return th


def fit(X, theta, b, offset=None):
    Xz, M = _prep(X)
    ok = ~np.isnan(theta)
    Xz, M = Xz[ok], M[ok]
    off = 0.0 if offset is None else offset[ok]
    p = sig(theta[ok][:, None] - np.nan_to_num(b)[None, :] - off)
    v = p * (1 - p)
    z2 = (Xz - p) ** 2
    n = M.sum(0)
    outfit = (z2 / np.maximum(v, 1e-9) * M).sum(0) / np.maximum(n, 1)
    infit = (z2 * M).sum(0) / np.maximum((v * M).sum(0), 1e-9)
    return infit, outfit


def mml(X, anchors, anchor_mean, nodes=31, iters=120, tol=1e-6):
    """Rasch marginal maximum likelihood with a normal ability distribution (mean fixed at 0 before the anchor
    shift, variance estimated), EM on Gauss-Hermite nodes. Returns item difficulties on the anchor scale."""
    Xz, M = _prep(X)
    n, I = X.shape
    has = M.sum(0) > 0
    x, w = np.polynomial.hermite_e.hermegauss(nodes)
    w = w / w.sum()
    b = np.zeros(I)
    sd = 1.0
    for _ in range(iters):
        q = sd * x
        logp = np.zeros((n, nodes))
        for k in range(nodes):
            p = sig(q[k] - b)
            lp, lq = np.log(np.maximum(p, 1e-12)), np.log(np.maximum(1 - p, 1e-12))
            logp[:, k] = (Xz * M) @ lp + ((1 - Xz) * M) @ lq
        logp += np.log(w)[None, :]
        mx = logp.max(1, keepdims=True)
        post = np.exp(logp - mx)
        post /= post.sum(1, keepdims=True)
        nk = post.T @ M                     # nodes x items: expected number presented
        rk = post.T @ (Xz * M)              # nodes x items: expected number correct
        b_new = b.copy()
        for _ in range(8):
            p = sig(q[:, None] - b_new[None, :])
            g = (rk - nk * p).sum(0)
            h = (nk * p * (1 - p)).sum(0)
            b_new = np.where(has, b_new - g / np.maximum(h, 1e-9), 0.0)
        var = float((post * (q[None, :] ** 2)).sum(1).mean())
        sd_new = np.sqrt(max(var, 0.05))
        delta = max(np.abs(b_new - b).max(), abs(sd_new - sd))
        b, sd = b_new, sd_new
        if delta < tol:
            break
    shift = b[np.asarray(anchors)].mean() - anchor_mean
    return np.where(has, b - shift, np.nan)


def tcc(b, theta):
    return float(sig(theta - np.asarray(b)).sum())


def solve_tcc(b, target, lo=-8.0, hi=8.0):
    for _ in range(80):
        m = 0.5 * (lo + hi)
        if tcc(b, m) < target:
            lo = m
        else:
            hi = m
    return 0.5 * (lo + hi)
