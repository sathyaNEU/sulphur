"""task2 architecture 4: everything owed, computed from the cut pack alone.

The golden path: collars on the mine grid; the 1 m assays (detection-limit values at half the limit, the original
assay kept where a screen fire re-assay follows) composited to the 2.5 m flitches; the Stage 5 composites (inside
each flitch's design outline) declustered on 25 m cells; the variogram (downhole and across holes) fitted with a
nugget and two spherical structures; the variance of a 5 m by 5 m by 2.5 m block from the model's average within a
block; the declustered distribution corrected to that variance by the indirect lognormal correction; tonnes from the
weathering zones' densities; the gold in blocks at each cut-off; the tier. The rungs and rivals run through the same
functions with one switch changed, and the kriged block model is built for the rung that reads it."""
import csv
import math
import os
from functools import lru_cache

import numpy as np

FILES = {
    "collars": "MC_drillhole_collars.csv",
    "assays": "MC_drillhole_assays.csv",
    "density": "MC_bulk_density.csv",
    "weathering": "MC_weathering_logs.csv",
    "design": "MC_stage5_design_flitches.csv",
}
MGA_SHIFT = (339250.0, 6601480.0)
TOP_RL = 400.0
FLITCH = 2.5
CUTS = [1.0, 1.5, 2.0, 2.5, 3.0]
CUT = 2.5
TIERS = [("A", 75), ("B", 125), ("C", 200)]
OZ = 31.1035


def _rows(target, key):
    with open(os.path.join(target, FILES[key]), newline="") as f:
        return list(csv.DictReader(f))


@lru_cache(maxsize=None)
def composites(target, reassay="original"):
    """2.5 m flitch composites: (hole, east, north, rl_mid, grade, zone)."""
    col = {}
    for r in _rows(target, "collars"):
        e, n = float(r["east"]), float(r["north"])
        if r["grid"] == "MGA94_51":
            e, n = e - MGA_SHIFT[0], n - MGA_SHIFT[1]
        col[r["hole_id"]] = (e, n, float(r["rl"]))
    zones = {}
    for r in _rows(target, "weathering"):
        zones.setdefault(r["hole_id"], []).append((float(r["depth_from"]), float(r["depth_to"]), r["weathering"]))
    samp = {}
    for r in _rows(target, "assays"):
        v = float(r["au"][1:]) / 2 if r["au"].startswith("<") else float(r["au"])
        key = (r["hole_id"], float(r["depth_from"]), float(r["depth_to"]))
        if key in samp:
            if reassay == "mean":
                samp[key] = (samp[key] + v) / 2
            elif reassay == "reassay":
                samp[key] = v
            continue
        samp[key] = v
    by_hole = {}
    for (h, a, b), v in samp.items():
        by_hole.setdefault(h, []).append((a, b, v))
    out = []
    for h, iv in by_hole.items():
        e, n, rl0 = col[h]
        iv.sort()
        # flitch k spans RL 400 - 2.5k to RL 400 - 2.5(k+1); depth below collar = rl0 - RL
        for k in range(40):
            top, bot = rl0 - (TOP_RL - k * FLITCH), rl0 - (TOP_RL - (k + 1) * FLITCH)
            tot = acc = 0.0
            for a, b, v in iv:
                ov = min(b, bot) - max(a, top)
                if ov > 0:
                    tot += ov
                    acc += ov * v
            if tot >= 0.5 * FLITCH:
                mid = (top + bot) / 2
                zn = next((z for a, b, z in zones.get(h, []) if a <= mid < b), "FR")
                out.append((h, e, n, TOP_RL - (k + 0.5) * FLITCH, acc / tot, zn))
    return out


def design(target):
    return {int(r["flitch"]) - 1: tuple(float(r[c]) for c in ("east_min", "east_max", "north_min", "north_max"))
            for r in _rows(target, "design")}


def densities(target):
    d = {}
    for r in _rows(target, "density"):
        d.setdefault(r["weathering"], []).append(float(r["density_t_m3"]))
    return {k: float(np.mean(v)) for k, v in d.items()}


def stage5(target, reassay="original"):
    des = design(target)
    comps = composites(target, reassay)
    out = []
    for c in comps:
        k = int(round((TOP_RL - c[3]) / FLITCH - 0.5))
        if k in des:
            e0, e1, n0, n1 = des[k]
            if e0 <= c[1] <= e1 and n0 <= c[2] <= n1:
                out.append(c + (k,))
    return out


def decluster(s5, cell=25.0):
    """Cell weights in plan, flitch by flitch: each occupied cell of each flitch carries equal weight."""
    key = [(int(math.floor(c[1] / cell)), int(math.floor(c[2] / cell)), c[6]) for c in s5]
    cnt = {}
    for k in key:
        cnt[k] = cnt.get(k, 0) + 1
    w = np.array([1.0 / cnt[k] for k in key])
    return w / w.mean()


def tonnage(target, s5, w):
    """Stage 5 tonnes: each flitch's outline area times 2.5 m times the declustered mean density of its composites."""
    des = design(target)
    rho = densities(target)
    by = {}
    for c, wi in zip(s5, w):
        by.setdefault(c[6], []).append((wi, rho[c[5]]))
    T = 0.0
    for k, (e0, e1, n0, n1) in des.items():
        v = by.get(k)
        r = sum(a * b for a, b in v) / sum(a for a, _ in v) if v else rho["FR"]
        T += (e1 - e0) * (n1 - n0) * FLITCH * r
    return T, rho


# ---------------------------------------------------------------- the variogram

def experimental(s5, lag_h=12.5, max_h=112.5):
    """lag_h is the class width beyond the first class, which holds the grade control trial's 5 m and 7 m pairs."""
    """Downhole variogram at 2.5 m lags and the across-hole variogram within flitches in lag classes."""
    by_hole = {}
    for c in s5:
        by_hole.setdefault(c[0], {})[c[6]] = c[4]
    dh = []
    for L in range(1, 11):
        sq = [(f[k] - f[k + L]) ** 2 for f in by_hole.values() for k in f if k + L in f]
        dh.append((L * FLITCH, 0.5 * float(np.mean(sq)), len(sq)))
    holes = {c[0]: (c[1], c[2]) for c in s5}
    names = sorted(holes)
    xy = np.array([holes[h] for h in names])
    vals = [by_hole[h] for h in names]
    bins = np.concatenate([[0.0, 8.0], np.arange(lag_h + 2.5, max_h + lag_h, lag_h)])
    acc = np.zeros(len(bins) - 1)
    num = np.zeros(len(bins) - 1)
    dsum = np.zeros(len(bins) - 1)
    for i in range(len(names)):
        dd = np.hypot(xy[:, 0] - xy[i, 0], xy[:, 1] - xy[i, 1])
        for j in np.nonzero((dd > 0.5) & (dd < max_h))[0]:
            if j <= i:
                continue
            common = [k for k in vals[i] if k in vals[j]]
            if not common:
                continue
            b = int(np.searchsorted(bins, dd[j], side="right") - 1)
            if b < 0 or b >= len(acc):
                continue
            acc[b] += sum((vals[i][k] - vals[j][k]) ** 2 for k in common)
            num[b] += len(common)
            dsum[b] += dd[j] * len(common)
    hz = [(dsum[b] / num[b], 0.5 * acc[b] / num[b], int(num[b])) for b in range(len(acc)) if num[b] > 50]
    return dh, hz


def sph(h, a):
    x = np.minimum(np.asarray(h, dtype=float) / a, 1.0)
    return 1.5 * x - 0.5 * x ** 3


def gamma_model(hx, hz, m):
    c0, c1, a1, a2, r = m
    h = np.sqrt(np.asarray(hx) ** 2 + (np.asarray(hz) / r) ** 2)
    return np.where(h > 0, c0, 0.0) + c1 * sph(h, a1) + (1 - c0 - c1) * sph(h, a2)


def fit_variogram(dh, hz, sill, nugget_fixed=None, a1s=(6, 8, 10, 12, 15), a2s=(40, 50, 60, 70, 80, 100),
                  rs=(0.3, 0.4, 0.5, 0.6)):
    """Nugget, two spherical structures and a vertical anisotropy ratio, by least squares weighted by pairs on both
    experimental curves, in units of the sill."""
    hd = np.array([a for a, _, _ in dh])
    gd = np.array([b for _, b, _ in dh]) / sill
    nd = np.array([n for _, _, n in dh], dtype=float)
    hh = np.array([a for a, _, _ in hz])
    gh = np.array([b for _, b, _ in hz]) / sill
    nh = np.array([n for _, _, n in hz], dtype=float)
    best = None
    c0s = [nugget_fixed] if nugget_fixed is not None else np.linspace(0.1, 0.7, 31)
    for c0 in c0s:
        for c1 in np.linspace(0.05, 0.8, 31):
            if c0 + c1 >= 0.97:
                continue
            for a1 in a1s:
                for a2 in a2s:
                    for r in rs:
                        m = (c0, c1, a1, a2, r)
                        e = float(np.sum(nd * (gamma_model(0, hd, m) - gd) ** 2) / nd.sum() +
                                  np.sum(nh * (gamma_model(hh, 0, m) - gh) ** 2) / nh.sum())
                        if best is None or e < best[0]:
                            best = (e, m)
    return best[1]


def gamma_bar(m, disc=(5, 5, 3), size=(5.0, 5.0, 2.5)):
    """The model's average within a block (in units of the sill), the block discretised to disc points."""
    px = (np.arange(disc[0]) + 0.5) / disc[0] * size[0]
    py = (np.arange(disc[1]) + 0.5) / disc[1] * size[1]
    pz = (np.arange(disc[2]) + 0.5) / disc[2] * size[2]
    pts = np.array([(a, b, c) for a in px for b in py for c in pz])
    D = pts[:, None, :] - pts[None, :, :]
    return float(gamma_model(np.hypot(D[..., 0], D[..., 1]), np.abs(D[..., 2]), m).mean())


# ---------------------------------------------------------------- distributions at a support

def correct(g, w, ratio, how="lognormal", target_var=None):
    """The declustered composite distribution carried to a support whose variance is ratio times the composites'
    (target_var replaces the declustered variance the ratio applies to)."""
    m = float(np.sum(w * g) / w.sum())
    v = float(np.sum(w * (g - m) ** 2) / w.sum())
    if target_var is not None:
        b = math.sqrt(math.log(1 + ratio * target_var / m ** 2) / math.log(1 + v / m ** 2))
        out = g ** b
        return out * m / float(np.sum(w * out) / w.sum())
    if how == "affine":
        return m + (g - m) * math.sqrt(ratio)
    # indirect lognormal: g' = a g^b, b from the variances of the logs, a restoring the mean
    b = math.sqrt(math.log(1 + ratio * v / m ** 2) / math.log(1 + v / m ** 2))
    out = g ** b
    return out * m / float(np.sum(w * out) / w.sum())


def grade_tonnage(g, w, rho_c, T, cuts=CUTS):
    """Tonnes, grade and gold above each cut-off: each value stands for its declustered share of Stage 5's tonnes,
    weighted by its own zone's density."""
    tw = w * rho_c
    out = {}
    for c in cuts:
        a = g >= c
        share = float(tw[a].sum() / tw.sum())
        t = share * T
        gr = float((tw[a] * g[a]).sum() / tw[a].sum()) if a.any() else 0.0
        out[c] = {"t": t, "g": gr, "oz": t * gr / OZ}
    return out


def tier(oz):
    ok = [t for t, v in TIERS if oz >= v * 1000]
    return ok[-1] if ok else None


def run(target, cell=25.0, how="lognormal", reassay="original", support=True, decl=True, nugget=None,
        disc=(5, 5, 3), lag=12.5, raw_variance=False):
    s5 = stage5(target, reassay)
    g = np.array([c[4] for c in s5])
    w = decluster(s5, cell) if decl else np.ones(len(s5))
    T, rho = tonnage(target, s5, w)
    rho_c = np.array([rho[c[5]] for c in s5])
    m = float(np.sum(w * g) / w.sum())
    v = float(np.sum(w * (g - m) ** 2) / w.sum())
    dh, hz = experimental(s5, lag)
    model = fit_variogram(dh, hz, float(np.var(g)), nugget)
    gb = gamma_bar(model, disc)
    ratio = 1.0 - gb
    gs = (correct(g, w, ratio, how, float(np.var(g)) if raw_variance else None) if support else g)
    gt = grade_tonnage(gs, w, rho_c, T)
    return {"n": len(s5), "holes": len({c[0] for c in s5}), "mean_raw": float(g.mean()), "mean_decl": m,
            "var_decl": v, "cv_decl": math.sqrt(v) / m, "model": model, "gamma_bar": gb, "ratio": ratio, "T": T,
            "rho": rho, "gt": gt, "oz": gt[CUT]["oz"], "tier": tier(gt[CUT]["oz"]), "dh": dh, "hz": hz}


# ---------------------------------------------------------------- the kriged block model (the rung that reads it)

def krige_blocks(target, model, s5, max_n=24, radius=45.0, reassay="original"):
    """Ordinary kriging of every 5 m by 5 m by 2.5 m block of Stage 5 from the composites inside the design, the
    block discretised to 2 by 2 by 1 points; returns block grades and the flitch of each."""
    des = design(target)
    comps = np.array([(c[1], c[2], c[3], c[4]) for c in s5])
    holes = {}
    for i, c in enumerate(s5):
        holes.setdefault((round(c[1], 2), round(c[2], 2)), []).append(i)
    hxy = np.array(list(holes.keys()))
    hidx = list(holes.values())
    c0, c1, a1, a2, r = model

    def cov(hx, hz):
        return 1.0 - gamma_model(hx, hz, model)
    off = np.array([(-1.25, -1.25), (-1.25, 1.25), (1.25, -1.25), (1.25, 1.25)])
    est, fl = [], []
    for k, (e0, e1, n0, n1) in sorted(des.items()):
        rl = TOP_RL - (k + 0.5) * FLITCH
        es = np.arange(math.floor(e0 / 5) * 5 + 2.5, e1, 5.0)
        ns = np.arange(math.floor(n0 / 5) * 5 + 2.5, n1, 5.0)
        for be in es:
            if be < e0 or be > e1:
                continue
            for bn in ns:
                if bn < n0 or bn > n1:
                    continue
                dd = np.hypot(hxy[:, 0] - be, hxy[:, 1] - bn)
                near = np.nonzero(dd < radius)[0]
                idx = np.concatenate([hidx[j] for j in near]) if len(near) else np.array([], dtype=int)
                if len(idx) < 4:
                    continue
                p = comps[idx]
                dist = np.sqrt((p[:, 0] - be) ** 2 + (p[:, 1] - bn) ** 2 + ((p[:, 2] - rl) / r) ** 2)
                sel = idx[np.argsort(dist)[:max_n]]
                q = comps[sel]
                n = len(sel)
                A = np.ones((n + 1, n + 1))
                A[n, n] = 0.0
                dx = q[:, None, 0] - q[None, :, 0]
                dy = q[:, None, 1] - q[None, :, 1]
                dz = q[:, None, 2] - q[None, :, 2]
                A[:n, :n] = cov(np.hypot(dx, dy), np.abs(dz))
                bvec = np.ones(n + 1)
                bvec[:n] = np.mean([cov(np.hypot(q[:, 0] - (be + o[0]), q[:, 1] - (bn + o[1])), np.abs(q[:, 2] - rl))
                                    for o in off], axis=0)
                lam = np.linalg.solve(A, bvec)[:n]
                est.append(float(lam @ q[:, 3]))
                fl.append(k)
    return np.array(est), np.array(fl)


def kriged_tonnage(target, s5, est, fl, w):
    """The kriged blocks' gold above each cut-off, each flitch's tonnes spread over its blocks."""
    T, rho = tonnage(target, s5, w)
    des = design(target)
    by = {}
    for c, wi in zip(s5, w):
        by.setdefault(c[6], []).append((wi, rho[c[5]]))
    out = {}
    for c in CUTS:
        t = gsum = 0.0
        for k, (e0, e1, n0, n1) in des.items():
            m = fl == k
            if not m.any():
                continue
            v = by.get(k)
            r = sum(a * b for a, b in v) / sum(a for a, _ in v) if v else rho["FR"]
            ft = (e1 - e0) * (n1 - n0) * FLITCH * r
            a = est[m] >= c
            t += ft * a.mean()
            gsum += ft * a.mean() * (est[m][a].mean() if a.any() else 0.0)
        out[c] = {"t": t, "g": gsum / t if t else 0.0, "oz": gsum / OZ}
    return out
