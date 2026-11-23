#!/usr/bin/env python3
"""task9 architecture 5, the core: which sources of score movement carry a risk model's tier instability in 2027.

A risk vendor refreshes merchant risk scores every week across 14 model families and supplies the tiers to
acquirers. The acquirers read the tiers at quarter-end snapshots, and a covenant caps the share of merchants whose
tier changes between two snapshots. 2026 breached it. The stability policy places each model-side source of score
movement in a band on the points it alone moves a merchant's score between two consecutive quarter-end snapshots
(root mean square over the scored book, 2027 as scheduled): under 5.5 monitor, 5.5 to under 8 a remediation plan,
8 or more escalation. No record holds what one source alone moves a score between two snapshots: the production
scores hold every source at once, and each instrument the platform keeps sees one source through its own design.

The sources (members): optimisation noise (replicate pairs), training-window turnover (bootstrap pairs), retunes
(old-against-new configuration scores), feature releases (shadow deltas), label revisions (label-freeze pairs).
Merchants' own change is the remainder and is reported apart.

The three stumps (each opens a different source, each leaves several dependent steps once said):
  S1 (unit)  a bootstrap pair resamples the whole training window, so its spread is the noise of two unrelated
             windows. Two quarter-end models share every week of the window but the 13 that left and the 13 that
             entered. The contribution is the per-row noise times the rows turned over, family by family and span
             by span from the training manifests (windows of 52 and 104 weeks, seasonal and growing volumes).
  S2 (what)  a replicate pair is two fits from one parent, so it shows one week's fresh noise. Since the warm-start
             change each weekly model starts from last week's weights and inherits its deviation, so two models 13
             refreshes apart differ by far more than a replicate pair. The persistence is in no instrument. It is
             in the bend of the production score-change variance across lags, where turnover, retunes, releases,
             label revisions and merchants' own change are straight lines, tied to the replicate variance.
  S3 (when)  pinned feature views are scheduled for every family by February 2027 and stop feature releases moving
             scores. The change calendar marks a rollout complete when the image is available. The run manifests
             of three past rollouts show when each family actually trained on it: weeks to months later by how many
             custom components the family carries, with reverts. 2027 coverage is that lag model carried to the plan.

What forces the call between estimators (a falsification check, no file observes a stump's quantity): each route's
own model of the lag curve is asked for the weekly score-change variance of the warm families in 2026, which the
production record holds. The adoption model is checked on its own records by leaving one past rollout out.

Run:  python3 task9/generator/core.py            the corelib verdict
      python3 task9/generator/core.py --detail   the world, the fitted inputs, every route
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))


def waivers():
    """The author's ruling on corelib's two rubric rows, read from pipeline.json `rulings.rubric_rows` (corelib
    prints it and turns those rows to WARN; no other row can be waived)."""
    import json
    try:
        r = json.load(open(os.path.join(os.path.dirname(HERE), "pipeline.json"), encoding="utf-8"))["rulings"]
        t = r["rubric_rows"]["text"]
    except (OSError, KeyError, ValueError):
        return {}
    return {"one stump lost, the run stays under the bar": t, "the reflex route on the rubric": t}
sys.path.insert(0, os.path.join(HERE, "..", "..", ".claude", "skills", "stumping"))
import corelib  # noqa: E402

SEED = int(os.environ.get("CORE_SEED", 9505))
F = 14                      # model families
FRAC = float(os.environ.get("CORE_FRAC", 0.2))   # the monitoring panel: one merchant in five of every family's book
LEAVE = 0.09                # a panel merchant's yearly chance of leaving the book (it is not replaced)
T = 126                     # record weeks: t = 0 is the week of 1 July 2024, t = 125 the week of 23 November 2026
PRE = 112                   # weeks of training rows held before t = 0
H = 13                      # the covenant's grain: quarter-end snapshot to quarter-end snapshot
LAGS = 30
Y26 = 78                    # first week of 2026
Y27 = 130                   # first week of 2027
SPANS26 = ((77, 90), (90, 103), (103, 116))             # quarter-end snapshot pairs inside the 2026 record
SPANS27 = ((129, 142), (142, 155), (155, 168), (168, 181))   # the four pairs that close in 2027
LINES = (5.5, 8.0)          # the stability policy's bands on the points a source moves a score on its own
SOURCES = ("optimisation", "turnover", "retunes", "releases", "labels")
TARGET = {"optimisation": 44.0, "turnover": 44.0, "retunes": 20.0, "releases": 105.0, "labels": 100.0,
          "merchant": 200.0}   # points squared at 13 weeks, book weighted; releases before pinned views
CUTS = (400.0, 500.0, 600.0)


def lognormal_cdf(x, mu, sg):
    return np.where(x > 0, 0.5 * (1 + np.vectorize(math.erf)((np.log(np.maximum(x, 1e-9)) - mu) / (sg * math.sqrt(2)))), 0.0)


# --------------------------------------------------------------------------------------------------- the world
def build_world(seed=SEED):
    rng = np.random.default_rng(seed)
    w = {}
    w["merch"] = rng.integers(1500, 22000, F).astype(float)
    w["ms"] = np.rint(FRAC * w["merch"]).astype(int)
    w["custom"] = rng.integers(0, 6, F)                         # custom training components a family carries
    w["epochs"] = rng.choice([2, 3, 4], F, p=[0.3, 0.4, 0.3])
    w["phi"] = np.array([{2: 0.90, 3: 0.86, 4: 0.80}[e] for e in w["epochs"]]) + rng.uniform(-0.008, 0.008, F)
    w["window"] = np.where(rng.random(F) < 0.36, 104, 52)       # weeks of rows a warm family trains on
    base_rows = w["merch"] * rng.uniform(9, 16, F)
    growth = rng.uniform(0.02, 0.38, F)
    w["growth"] = growth
    wk = np.arange(-PRE, 190)
    season = 1 + 0.32 * np.cos(2 * np.pi * ((wk + 26) % 52 - 46) / 52.0)
    w["wk0"] = PRE
    w["rows"] = np.array([base_rows[f] * (1 + growth[f]) ** (wk / 52.0) * season *
                          np.exp(rng.normal(0, 0.05, wk.size)) for f in range(F)])
    small = (w["merch"] / w["merch"].mean()) ** -0.30           # small books: noisier models, more volatile merchants
    jit = lambda s: np.exp(rng.normal(0, s, F))
    w["eta2"] = small * jit(0.15)                               # fresh optimisation noise per refit
    w["cold2"] = 2.4 * w["eta2"]                                # a cold start's own run-to-run noise
    w["row2"] = jit(0.12)                                       # per-row sampling noise carried to a score
    w["tau2"] = small * jit(0.22)                               # merchants' own weekly change
    w["lab2"] = jit(0.22)                                       # a week's label revisions
    w["ret2"] = jit(0.22)                                       # one retune
    w["rel2"] = jit(0.22)                                       # one feature release, where it hits
    w["use"] = rng.uniform(0.45, 0.9, F)                        # chance a release touches a family's feature groups
    w["ret_off"] = rng.integers(0, 4, F)

    # three past platform rollouts and the scheduled one: planned, declared and effective weeks per family
    def rollout(lo, hi):
        planned = rng.integers(lo, hi + 1, F)
        declared = planned + rng.integers(0, 4, F)
        lag = np.minimum(np.rint(np.exp(rng.normal(np.log(5 + 4 * w["custom"]), 0.30))), 44).astype(int)
        eff = declared + lag
        rev = np.zeros((F, 2), int)
        for f in range(F):
            if rng.random() < 0.32:
                a = eff[f] + rng.integers(2, 11)
                rev[f] = (a, a + rng.integers(3, 9))
        return {"planned": planned, "declared": declared, "eff": eff, "revert": rev}
    w["runtime"] = rollout(2, 8)
    w["warm"] = rollout(14, 22)
    w["amp"] = rollout(30, 40)
    w["fv_planned"] = rng.integers(131, 139, F)

    # release weeks: the feature platform shipped far more in 2026; the 2027 roadmap plans six a quarter
    rel = [t for t in range(T) if rng.random() < (0.15 if t < Y26 else 0.40)]
    w["rel_weeks"] = np.array(rel)
    w["rel_hits"] = rng.random((len(rel), F)) < w["use"]
    plan = np.concatenate([np.sort(rng.choice(np.arange(a + 1, b + 1), 6, replace=False)) for a, b in SPANS27])
    w["plan_weeks"] = plan
    w["plan_hits"] = rng.random((plan.size, F)) < w["use"]

    # the regime of every weekly retrain
    warm = np.zeros((F, T), bool)
    for f in range(F):
        warm[f, w["warm"]["eff"][f]:] = True
        a, b = w["warm"]["revert"][f]
        if b > a:
            warm[f, a:b] = False
    w["is_warm"] = warm
    w["last_cold"] = np.array([np.max(np.where(~warm[f])[0]) for f in range(F)])
    return w, rng


def win_rows(w, f, t, W):
    """Rows of each week in the window of the retrain at week t (the W weeks ending at t)."""
    i = w["wk0"] + t
    return w["rows"][f, i - W + 1:i + 1]


def turnover_factor(w, f, t0, t1, W, simple=False, entered=False):
    """Variance of the change in a window fit between t0 and t1, per unit of per-row noise."""
    a, b = win_rows(w, f, t0, W), win_rows(w, f, t1, W)
    h = t1 - t0
    n0, n1 = a.sum(), b.sum()
    if h >= W:
        return 1 / n0 + 1 / n1
    out_, in_, common = a[:h].sum(), b[-h:].sum(), a[h:].sum()
    if entered:                       # the rows that entered only
        return in_ / n1 ** 2
    if simple:
        return (in_ + out_) / (0.5 * (n0 + n1)) ** 2
    return common * (1 / n1 - 1 / n0) ** 2 + in_ / n1 ** 2 + out_ / n0 ** 2


def scale_world(w):
    """Set each source's size so the book-weighted 13-week variances sit at TARGET (sizes from the process)."""
    wt = w["merch"] / w["merch"].sum()
    tf = np.array([np.mean([turnover_factor(w, f, a, b, w["window"][f]) for a, b in SPANS27]) for f in range(F)])
    raw = {"optimisation": 2 * w["eta2"] / (1 - w["phi"] ** 2) * (1 - w["phi"] ** H), "turnover": w["row2"] * tf,
           "retunes": w["ret2"] * H / 4.0, "labels": w["lab2"] * H, "merchant": w["tau2"] * H,
           "releases": w["rel2"] * np.array([w["plan_hits"][:, f].sum() / 4.0 for f in range(F)])}
    key = {"optimisation": ("eta2", "cold2"), "turnover": ("row2",), "retunes": ("ret2",), "labels": ("lab2",),
           "merchant": ("tau2",), "releases": ("rel2",)}
    for s, ks in key.items():
        k = TARGET[s] / float((wt * raw[s]).sum())
        for name in ks:
            w[name] = w[name] * k
    return w


def simulate(w, rng, keep=None):
    """Production scores, the instruments' pairs and the quarter-end tiers, merchant by merchant. keep, a dict, is
    given every draw the instruments made (the pack's pair files are written from it); no draw is added or moved."""
    z = [None] * F
    inst = {"rep": np.zeros(F), "boot": np.zeros(F), "boot_last": np.zeros(F), "boot_n": np.zeros(F),
            "boot_n_last": np.zeros(F), "ret": np.zeros(F), "rel": np.zeros(F), "lab": np.zeros(F)}
    for f in range(F):
        MS = int(w["ms"][f])
        base = rng.normal(500, 100, MS)
        own = np.cumsum(rng.normal(0, math.sqrt(w["tau2"][f]), (MS, T)), axis=1)
        lab = np.cumsum(rng.normal(0, math.sqrt(w["lab2"][f]), (MS, T)), axis=1)
        ret = np.zeros((MS, T))
        jumps = []
        for t in range(T):
            if (t - w["ret_off"][f]) % 4 == 0:
                j = rng.normal(0, math.sqrt(w["ret2"][f]), MS)
                ret[:, t:] += j[:, None]
                if t >= Y26:
                    jumps.append(j)
                    if keep is not None:
                        keep.setdefault("ret", []).append((f, t, j))
        rel = np.zeros((MS, T))
        steps = []
        for k, t in enumerate(w["rel_weeks"]):
            if w["rel_hits"][k, f]:
                j = rng.normal(0, math.sqrt(w["rel2"][f]), MS)
                rel[:, t:] += j[:, None]
                if t >= Y26:
                    steps.append(j)
                    if keep is not None:
                        keep.setdefault("rel", []).append((f, k, t, j))
        rows = w["rows"][f]
        eps = rng.normal(0, 1, (MS, rows.size)) * np.sqrt(w["row2"][f] * rows)[None, :]   # n_w times the week's noise
        cum = np.cumsum(eps, axis=1)
        crow = np.cumsum(rows)
        data = np.zeros((MS, T))
        opt = np.zeros((MS, T))
        e = np.zeros(MS)
        for t in range(T):
            W = w["window"][f] if t >= w["warm"]["eff"][f] else 26
            i = w["wk0"] + t
            data[:, t] = (cum[:, i] - cum[:, i - W]) / (crow[i] - crow[i - W])
            if w["is_warm"][f, t]:
                e = w["phi"][f] * e + rng.normal(0, math.sqrt(w["eta2"][f]), MS)
            else:
                e = rng.normal(0, math.sqrt(w["cold2"][f]), MS)
            opt[:, t] = e
        z[f] = base[:, None] + own + lab + ret + rel + data + opt
        if keep is not None:
            keep.setdefault("lab_path", {})[f] = lab
            keep.setdefault("opt", {})[f] = opt
        left = np.where(rng.random(MS) < 1 - (1 - LEAVE) ** (T / 52.0), rng.integers(8, T, MS), T)
        z[f][np.arange(T)[None, :] >= left[:, None]] = np.nan      # a merchant that left is no longer scored
        # the instruments, all run in 2026 on warm families
        rep_w = rng.choice(np.arange(Y26 + 4, T), 6, replace=False)
        rv = []
        for t in rep_w:
            a_ = rng.normal(0, math.sqrt(w["eta2"][f]), MS)
            b_ = rng.normal(0, math.sqrt(w["eta2"][f]), MS)
            rv.append(np.var(a_ - b_))
            if keep is not None:
                keep.setdefault("rep", []).append((f, int(t), a_, b_))
        inst["rep"][f] = np.mean(rv)
        bw = np.sort(rng.choice(np.arange(Y26 + 4, T), 4, replace=False))
        bv, bn = [], []
        for t in bw:
            n = win_rows(w, f, t, w["window"][f]).sum()
            sd = math.sqrt(w["eta2"][f] + w["row2"][f] / n)
            a_ = rng.normal(0, sd, MS)
            b_ = rng.normal(0, sd, MS)
            bv.append(np.var(a_ - b_))
            bn.append(n)
            if keep is not None:
                keep.setdefault("boot", []).append((f, int(t), a_, b_, n))
        inst["boot"][f], inst["boot_n"][f] = np.mean(bv), np.mean(bn)
        inst["boot_last"][f], inst["boot_n_last"][f] = bv[-1], bn[-1]
        inst["ret"][f] = np.mean([np.var(j) for j in jumps])
        inst["rel"][f] = np.mean([np.var(j) for j in steps])
        lw = rng.choice(np.arange(Y26 + 4, T), 8, replace=False)
        inst["lab"][f] = np.mean([np.var(np.diff(lab[:, t - 1:t + 1], axis=1)) for t in lw])
        if keep is not None:
            keep.setdefault("lab", []).extend((f, int(t)) for t in lw)
            keep.setdefault("left", {})[f] = left
    return z, inst


# --------------------------------------------------------------------------------- what the files let one compute
def lag_curve(w, z, f, lags=LAGS, start=None):
    """Mean squared score change at each lag over the family's settled warm weeks."""
    t0 = max(w["last_cold"][f] + 13, 66) if start is None else start
    return np.array([np.nanmean((z[f][:, t0 + h:T] - z[f][:, t0:T - h]) ** 2) for h in range(1, lags + 1)]), t0


def events_in_span(w, f, t0, lags):
    """Mean number of retunes and of releases that hit the family inside a span of each lag, over the same starts."""
    ret = np.array([(t - w["ret_off"][f]) % 4 == 0 for t in range(T)], float)
    rel = np.zeros(T)
    for k, t in enumerate(w["rel_weeks"]):
        if w["rel_hits"][k, f]:
            rel[t] += 1
    cr, cl = np.cumsum(ret), np.cumsum(rel)
    out = []
    for h in range(1, lags + 1):
        s = np.arange(t0, T - h)
        out.append((np.mean(cr[s + h] - cr[s]), np.mean(cl[s + h] - cl[s])))
    return np.array(out)


def fit_bend(D, rep, lags=26, anchored=True, lo=1, flat=False):
    """D(h) = b h + A (1 - phi^h). Anchored: A (1 - phi^2) is the replicate pair variance."""
    h = np.arange(1, len(D) + 1)[lo - 1:lags]
    d = D[lo - 1:lags]
    wgt = np.ones_like(d) if flat else 1.0 / d ** 2
    best = None
    for phi in np.arange(0.50, 0.9851, 0.0025):
        g = 1 - phi ** h
        if anchored:
            A = rep / (1 - phi ** 2)
            b = float(np.sum(wgt * h * (d - A * g)) / np.sum(wgt * h * h))
        else:
            X = np.vstack([h, g]).T * np.sqrt(wgt)[:, None]
            b, A = np.linalg.lstsq(X, d * np.sqrt(wgt), rcond=None)[0]
        sse = float(np.sum(wgt * (d - b * h - A * g) ** 2))
        if A > 0 and (best is None or sse < best[0]):
            best = (sse, phi, A, b)
    return best[1], best[2], best[3]


def past_adoption(w):
    """What the run manifests show for the three past rollouts: lag from the declared week, weeks reverted."""
    rows = []
    for name in ("runtime", "warm", "amp"):
        r = w[name]
        for f in range(F):
            rv = max(0, min(r["revert"][f, 1], r["eff"][f] + 26) - r["revert"][f, 0])
            rows.append((name, f, w["custom"][f], r["planned"][f], r["declared"][f], r["eff"][f], rv / 26.0))
    return rows


def coverage_model(w, kind="loglin", leave=None):
    """Expected share of each 2027 week a family trains on pinned feature views, from the past rollouts' lags."""
    rows = [r for r in past_adoption(w) if r[0] != leave]
    c = np.array([r[2] for r in rows], float)
    lag = np.array([max(r[5] - r[4], 1) for r in rows], float)
    slip = float(np.mean([r[4] - r[3] for r in rows]))
    rev = float(np.mean([r[6] for r in rows]))
    cf = w["custom"].astype(float)
    if kind == "loglin":
        X = np.vstack([np.ones_like(c), c]).T
        beta = np.linalg.lstsq(X, np.log(lag), rcond=None)[0]
        mu = beta[0] + beta[1] * cf
        sg = float(np.std(np.log(lag) - X @ beta, ddof=2))
    elif kind == "linear":
        X = np.vstack([np.ones_like(c), c]).T
        beta = np.linalg.lstsq(X, lag, rcond=None)[0]
        pred = np.maximum(beta[0] + beta[1] * cf, 1.0)
        sg = float(np.std(np.log(lag) - np.log(np.maximum(X @ beta, 1.0)), ddof=2))
        mu = np.log(pred) - 0.5 * sg ** 2 * 0
    elif kind == "groups":
        mu = np.array([np.mean(np.log(lag[c == x])) if np.any(c == x) else np.mean(np.log(lag)) for x in cf])
        sg = float(np.mean([np.std(np.log(lag[c == x]), ddof=1) for x in np.unique(c) if np.sum(c == x) > 2]))
    else:   # each family's own three rollouts
        fam = np.array([r[1] for r in rows])
        mu = np.array([np.mean(np.log(lag[fam == f])) for f in range(F)])
        sg = float(np.sqrt(np.mean([np.var(np.log(lag[fam == f]), ddof=1) for f in range(F) if np.sum(fam == f) > 1])))
    if kind == "pooled":
        mu = np.full(F, float(np.mean(np.log(lag))))
        sg = float(np.std(np.log(lag), ddof=1))
    return {"mu": mu, "sg": sg, "slip": slip, "rev": rev}


def coverage_weeks(w, mode, model=None):
    """cov[f, t - Y27 + 1]: share of week t (129 to 181) a family is on pinned views, by route."""
    wk = np.arange(Y27 - 1, 182)
    cov = np.zeros((F, wk.size))
    for f in range(F):
        p = w["fv_planned"][f]
        if mode == "plan":
            cov[f] = wk >= p
        elif mode == "declared":
            cov[f] = wk >= p + model["slip"]
        elif mode == "none":
            cov[f] = 0.0
        elif mode == "worst":
            worst = max(r[5] - r[4] for r in past_adoption(w) if r[1] == f)
            cov[f] = wk >= p + model["slip"] + worst
        elif mode == "threshold":
            cov[f] = (wk >= p + model["slip"]) if w["custom"][f] < model["cut"] else 0.0
        else:
            cov[f] = lognormal_cdf(wk - (p + model["slip"]), model["mu"][f], model["sg"]) * (1 - model["rev"])
    return cov


def true_coverage(w, rng, draws=4000):
    wk = np.arange(Y27 - 1, 182)
    cov = np.zeros((F, wk.size))
    for f in range(F):
        dec = w["fv_planned"][f] + rng.integers(0, 4, draws)
        lag = np.minimum(np.rint(np.exp(rng.normal(np.log(5 + 4 * w["custom"][f]), 0.30, draws))), 44)
        eff = dec + lag
        on = wk[None, :] >= eff[:, None]
        has = rng.random(draws) < 0.32
        a = eff + rng.integers(2, 11, draws)
        b = a + rng.integers(3, 9, draws)
        off = has[:, None] & (wk[None, :] >= a[:, None]) & (wk[None, :] < b[:, None])
        cov[f] = np.mean(on & ~off, axis=0)
    return cov


def release_exposure(w, cov):
    """Per family: planned 2027 releases that hit it and land on a week it is not on pinned views, per quarter pair."""
    out = np.zeros(F)
    for f in range(F):
        hit = w["plan_weeks"][w["plan_hits"][:, f]]
        out[f] = np.sum(1 - cov[f, hit - (Y27 - 1)]) / len(SPANS27)
    return out


# ------------------------------------------------------------------------------------------ one route, end to end
class Pack:
    """Everything a route may read: the production record, the instruments, the manifests, the calendar."""

    def __init__(self, w, z, inst):
        self.w, self.z, self.inst = w, z, inst
        self.curves, self.t0 = zip(*[lag_curve(w, z, f) for f in range(F)])
        self.events = [events_in_span(w, f, self.t0[f], LAGS) for f in range(F)]
        self.curves26 = [lag_curve(w, z, f, start=max(self.t0[f], Y26))[0] for f in range(F)]
        self.d13 = np.array([c[H - 1] for c in self.curves])
        self.d1 = np.array([c[0] for c in self.curves])
        self.fr26 = self.rescaled_flips(np.ones(F))
        self.models = {k: coverage_model(w, k) for k in ("loglin", "linear", "groups", "own", "pooled")}
        self.models["norevert"] = dict(self.models["loglin"], rev=0.0)

    def normal_flips(self, var):
        """Tier changes under a normal change of the given variance, on the scores of the last quarter-end snapshot."""
        out = np.zeros(F)
        cuts = np.array((-np.inf,) + CUTS + (np.inf,))
        erf = np.vectorize(math.erf)
        for f in range(F):
            z0 = self.z[f][:, 116]
            z0 = z0[~np.isnan(z0)]
            k = np.searchsorted(CUTS, z0, side="right")     # the covenant's tiers: 400 is the second tier
            sd = math.sqrt(max(float(var[f]), 1e-9)) * math.sqrt(2.0)
            stay = 0.5 * (erf((cuts[k + 1] - z0) / sd) - erf((cuts[k] - z0) / sd))
            out[f] = float(np.mean(1.0 - stay))
        return out

    def rescaled_flips(self, k):
        out = np.zeros(F)
        for f in range(F):
            fl = []
            for a, b in ((77, 90), (90, 103), (103, 116)):
                ok = ~np.isnan(self.z[f][:, b])                 # scored at both snapshots
                z0 = self.z[f][ok, a]
                z1 = z0 + k[f] * (self.z[f][ok, b] - z0)
                fl.append(np.mean(np.searchsorted(CUTS, z1, side="right") != np.searchsorted(CUTS, z0, side="right")))
            out[f] = np.mean(fl)
        return out


DEFAULT = {"S1": "gold", "S2": "gold", "S3": "gold", "fit": "anch26", "turn": "general", "boot": "mean",
           "adopt": "loglin", "weights": "current", "closure": "lag13", "frmap": "family"}


def evaluate(pk, **opt):
    """Every source's 13-week variance by family (2026 as recorded, 2027 as scheduled), then the graded figures."""
    o = dict(DEFAULT, **opt)
    w, inst = pk.w, pk.inst
    rep = inst["rep"]
    # optimisation noise
    fit = []
    for f in range(F):
        D = pk.curves26[f] if o["fit"] == "y2026" else pk.curves[f]
        if o["fit"] in ("events", "free_events"):
            D = D - pk.events[f][:, 0] * inst["ret"][f] - pk.events[f][:, 1] * inst["rel"][f]
        kw = {"anch26": dict(lags=26), "free26": dict(lags=26, anchored=False), "anch20": dict(lags=20),
              "anch30": dict(lags=30), "events": dict(lags=26), "pooled": dict(lags=26), "flat": dict(lags=26, flat=True),
              "from2": dict(lags=26, lo=2), "y2026": dict(lags=26), "free30": dict(lags=30, anchored=False),
              "free_events": dict(lags=30, anchored=False)}[o["fit"]]
        fit.append(fit_bend(D, rep[f], **kw))
    phi = np.array([x[0] for x in fit])
    A = np.array([x[1] for x in fit])
    slope = np.array([x[2] for x in fit])
    if o["fit"] == "pooled":
        for e in (2, 3, 4):
            sel = w["epochs"] == e
            phi[sel] = np.mean(phi[sel])
        A = rep / (1 - phi ** 2)
    if o["S2"] == "gold":
        opt13 = A * (1 - phi ** H)
    elif o["S2"] in ("hur", "cal"):   # a replicate pair is two models: its variance at any gap
        opt13 = rep.copy()
    elif o["S2"] == "over":           # thirteen weekly refits, each adding one fresh draw (half a replicate pair)
        opt13 = H * rep / 2.0
    elif o["S2"] == "over2":          # thirteen weekly refits, each adding a whole replicate pair's variance
        opt13 = H * rep
    elif o["S2"] == "cut":            # the intercept of a straight line through the later lags
        opt13 = np.zeros(F)
        for f in range(F):
            h = np.arange(o.get("cut_lag", 8), 27)
            opt13[f] = max(np.polyfit(h, pk.curves[f][h - 1], 1)[1], 0.0)
    # turnover
    bv = inst["boot"] if o["boot"] == "mean" else inst["boot_last"]
    bn = inst["boot_n"] if o["boot"] == "mean" else inst["boot_n_last"]
    face = np.maximum(bv - rep, 0.0)                     # two unrelated windows, the seeds' part taken out
    row2 = face / 2.0 * bn
    simple = o["turn"] == "simple"
    tf26 = np.array([np.mean([turnover_factor(w, f, a, b, w["window"][f], simple) for a, b in SPANS26]) for f in range(F)])
    tf27 = np.array([np.mean([turnover_factor(w, f, a, b, w["window"][f], simple) for a, b in SPANS27]) for f in range(F)])
    if o["turn"] == "recent":         # 2027's spans at the rows the 2026 spans turned over
        tf27 = tf26
    if o["S1"] == "gold" and o["turn"] == "weeks":   # weeks of the window in place of its rows
        tur26 = tur27 = face * H / w["window"]
    elif o["S1"] == "gold":
        tur26, tur27 = row2 * tf26, row2 * tf27
    elif o["S1"] == "raw":            # the bootstrap pairs as they stand, the seeds' part left in
        tur26 = tur27 = bv
    elif o["S1"] == "single":         # the rows that entered, and not the rows that left
        e27 = np.array([np.mean([turnover_factor(w, f, a, b, w["window"][f], entered=True) for a, b in SPANS27]) for f in range(F)])
        tur26 = tur27 = row2 * e27
    elif o["S1"] == "hur":
        tur26 = tur27 = face
    elif o["S1"] == "over":
        tur26 = tur27 = np.zeros(F)
    elif o["S1"] == "square":         # the share of the window turned over, applied to the spread and squared
        tur26 = tur27 = face * (H / w["window"]) ** 2
    elif o["S1"] == "flat":           # one share for every family: 13 weeks of a 52-week window
        tur26 = tur27 = face * (H / 52.0)
    elif o["S1"] == "double":         # the rows that left and the rows that entered each counted against the window
        tur26 = tur27 = face * (2.0 * H / w["window"])
    elif o["S1"] == "regress":        # the slope of the families' 13-week variance on their bootstrap spread
        X = np.vstack([np.ones(F), face]).T
        b = np.linalg.lstsq(X, pk.d13, rcond=None)[0][1]
        tur26 = tur27 = face * float(np.clip(b, 0.0, 1.5))
    ret13 = inst["ret"] * H / 4.0
    lab13 = inst["lab"] * H
    rel26 = inst["rel"] * np.array([pk.events[f][H - 1, 1] for f in range(F)])
    # pinned feature views
    m = pk.models[o["adopt"]]
    mode = {"gold": "model", "hur": "plan", "over": "none", "declared": "declared", "worst": "worst",
            "threshold": "threshold", "y2026": "none"}[o["S3"]]
    if mode == "threshold":
        m = dict(m, cut=o.get("cut_custom", 3))
    cov = coverage_weeks(w, mode, m) if "cov" not in o else o["cov"]
    rel27 = inst["rel"] * release_exposure(w, cov)
    if o["S3"] == "y2026":            # the record's own 2026 level carried into 2027
        rel27 = rel26.copy()
    if o["closure"] == "lag13":
        own = pk.d13 - (opt13 + tur26 + ret13 + lab13 + rel26)
    else:
        own = H * slope - (tur26 + ret13 + lab13 + rel26)
    if o["S2"] == "cal":              # a nugget and a slope through the weekly and the 13-week variance
        nug = np.maximum((H * pk.d1 - pk.d13) / (H - 1.0), 0.0)
        opt13 = nug * rep / (rep + face)
        tur26 = tur27 = nug * face / (rep + face)
        own = pk.d13 - (opt13 + tur26 + ret13 + lab13 + rel26)
    own = np.maximum(own, 0.0)
    wt = w["merch"] / w["merch"].sum()
    if o["weights"] == "plan":        # the book the 2027 plan expects in place of the one scored at the last snapshot
        wt = w["merch"] * (1 + w["growth"])
        wt = wt / wt.sum()
    if o["weights"] == "equal":       # every family counted once (refused by the policy's weighting sentence)
        wt = np.full(F, 1.0 / F)
    comp = {"optimisation": opt13, "turnover": tur27, "retunes": ret13, "releases": rel27, "labels": lab13}
    agg = {s: float((wt * v).sum()) for s, v in comp.items()}
    model_side = sum(agg.values())
    own_a = float((wt * own).sum())
    share = {s: 100.0 * agg[s] / model_side for s in SOURCES}
    points = {s: math.sqrt(agg[s]) for s in SOURCES}
    v26 = opt13 + tur26 + ret13 + rel26 + lab13 + own
    v27 = opt13 + tur27 + ret13 + rel27 + lab13 + own
    band = {s: sum(1 for l in LINES if points[s] >= l) for s in SOURCES}
    gone = sum(comp[s] for s in SOURCES if band[s] >= 1)
    if o["frmap"] == "family":
        fr_s = float((wt * pk.fr26 * np.sqrt(v27 / v26)).sum())
        fr_r = float((wt * pk.fr26 * np.sqrt(np.maximum(v27 - gone, 0) / v26)).sum())
    elif o["frmap"] == "rescale":     # each merchant's 2026 quarter-end changes rescaled, the tiers recounted
        fr_s = float((wt * pk.rescaled_flips(np.sqrt(v27 / v26))).sum())
        fr_r = float((wt * pk.rescaled_flips(np.sqrt(np.maximum(v27 - gone, 0) / v26))).sum())
    elif o["frmap"] == "normal":      # a normal change of the estimated variance on the last snapshot's scores
        fr_s = float((wt * pk.normal_flips(v27)).sum())
        fr_r = float((wt * pk.normal_flips(np.maximum(v27 - gone, 0))).sum())
    else:
        base = float((wt * pk.fr26).sum())
        fr_s = base * math.sqrt(float((wt * v27).sum()) / float((wt * v26).sum()))
        fr_r = base * math.sqrt(max(float((wt * (v27 - gone)).sum()), 0.0) / float((wt * v26).sum()))
    out = {"share_" + s: share[s] for s in SOURCES}
    out.update({"points_" + s: points[s] for s in SOURCES})
    return dict(out, **{"share": share, "points": points, "agg": agg, "own": own_a, "band": band,
            "cc1": math.sqrt(agg["turnover"]), "cc2": math.sqrt(agg["optimisation"]),
            "cc3": 100.0 * float(np.mean(cov[:, 1:])), "own_share": 100.0 * own_a / (own_a + model_side),
            "fr_sched": 100.0 * fr_s, "fr_removed": 100.0 * fr_r, "phi": phi, "A": A, "slope": slope,
            "opt13": opt13, "tur": tur27, "face": face, "row2": row2, "cov": cov})


def weekly_prediction(pk, route):
    """Each route's own model of the lag curve, asked for the weekly score-change variance (book weighted)."""
    w, inst = pk.w, pk.inst
    wt = w["merch"] / w["merch"].sum()
    g = evaluate(pk)
    lin = lambda r: (r["tur"] + inst["ret"] * H / 4.0 + inst["lab"] * H +
                     inst["rel"] * np.array([pk.events[f][H - 1, 1] for f in range(F)]))
    if route == "golden":
        pred = g["slope"] + g["A"] * (1 - g["phi"])
    else:
        r = evaluate(pk, **route)
        own = pk.d13 - r["opt13"] - lin(r)
        if route.get("S1") == "hur" and route.get("S2") != "hur":   # an inherited part, and a constant for turnover
            pred = r["face"] + g["A"] * (1 - g["phi"]) + (pk.d13 - g["opt13"] - r["face"]) / H
        elif route.get("S1") == "hur":                              # two constants and a straight line
            pred = r["face"] + inst["rep"] + (pk.d13 - inst["rep"] - r["face"]) / H
        elif route.get("S2") in ("over", "over2"):                  # every source a straight line
            pred = pk.d13 / H
        else:                                                       # a constant for the seeds and a straight line
            pred = r["opt13"] + (pk.d13 - r["opt13"]) / H
    return float((wt * pred).sum())


def world(keep=None):
    """The world and its record: (w, z, inst), every draw in the order the core makes it."""
    w, rng = build_world()
    w = scale_world(w)
    z, inst = simulate(w, rng, keep)
    return w, z, inst


def truth_of(w):
    """What each source alone moves a score between snapshots in 2027, from the world's own parameters."""
    wt = w["merch"] / w["merch"].sum()
    tcov = true_coverage(w, np.random.default_rng(SEED + 1))
    tf27 = np.array([np.mean([turnover_factor(w, f, a, b, w["window"][f]) for a, b in SPANS27]) for f in range(F)])
    tcomp = {"optimisation": 2 * w["eta2"] / (1 - w["phi"] ** 2) * (1 - w["phi"] ** H), "turnover": w["row2"] * tf27,
             "retunes": w["ret2"] * H / 4.0, "releases": w["rel2"] * release_exposure(w, tcov), "labels": w["lab2"] * H}
    tagg = {s: float((wt * v).sum()) for s, v in tcomp.items()}
    return tcov, tagg


def main():
    detail = "--detail" in sys.argv
    w, z, inst = world()
    pk = Pack(w, z, inst)
    A = analyse(pk, truth_of(w), detail)
    return corelib.run(A["spec"])


def analyse(pk, truth, detail=False):
    """Every route, the battery, the lattice and corelib's spec, on a Pack (the world's or one loaded from files)."""
    w, z, inst = pk.w, pk.z, pk.inst
    wt = w["merch"] / w["merch"].sum()
    if truth is None:                 # a pack loaded from files carries no world: the golden stands in for the truth
        truth = (None, evaluate(pk)["agg"])
    tcov, tagg = truth
    truth = {s: 100.0 * tagg[s] / sum(tagg.values()) for s in SOURCES}

    gold = evaluate(pk)
    variants = [dict(), dict(fit="anch20"), dict(fit="anch30"), dict(fit="events"), dict(fit="pooled"),
                dict(turn="simple"), dict(boot="last"), dict(adopt="linear"), dict(adopt="groups"),
                dict(adopt="own"), dict(weights="plan"), dict(closure="slope"), dict(frmap="pooled"),
                dict(fit="anch20", adopt="linear", turn="simple"), dict(fit="events", adopt="groups", boot="last"),
                dict(fit="anch30", adopt="own", closure="slope"), dict(fit="pooled", weights="plan", turn="simple"),
                dict(fit="flat"), dict(fit="from2"), dict(fit="y2026"), dict(adopt="norevert"),
                dict(fit="y2026", adopt="norevert", weights="plan"), dict(turn="weeks"), dict(turn="recent"),
                dict(frmap="rescale"), dict(adopt="pooled"), dict(turn="weeks", fit="events", frmap="rescale"),
                dict(turn="recent", adopt="pooled", fit="flat"), dict(frmap="rescale", adopt="linear", fit="anch30"),
                dict(frmap="normal"), dict(frmap="normal", fit="events", turn="weeks"),
                dict(S2="cut", cut_lag=12), dict(S2="cut", cut_lag=16),     # the level a line through the long lags starts from
                dict(S2="cut", cut_lag=14, turn="weeks", adopt="groups")]
    fam = [evaluate(pk, **v) for v in variants]
    free = evaluate(pk, fit="free26")      # the unanchored fit, ruled on by the replicate pairs (--detail)
    if detail:
        for k in ("free30", "free_events"):
            e = evaluate(pk, fit=k)
            print("probe %-12s optimisation %.2f points, implied fresh noise %.2f" % (k, e["points"]["optimisation"], float((wt * e["A"] * (1 - e["phi"] ** 2)).sum())))
        for lab, kw in (("S1 thirteen of 52 weeks for every family", dict(S1="flat")), ("S1 rows that entered only", dict(S1="single")),
                        ("S3 2026's release level carried", dict(S3="y2026")), ("S3 each family's worst past lag", dict(S3="worst")),
                        ("S2 intercept from lag 12", dict(S2="cut", cut_lag=12)), ("S2 intercept from lag 16", dict(S2="cut", cut_lag=16)),
                        ("S2 intercept from lag 8", dict(S2="cut")), ("S2 a whole replicate pair a refit", dict(S2="over2")),
                        ("every family counted once", dict(weights="equal"))):
            e = evaluate(pk, **kw)
            print("probe %-42s" % lab, " ".join("%s %.2f" % (s[:5], e["points"][s]) for s in SOURCES), "cc3 %.1f" % e["cc3"])
        g0 = evaluate(pk)
        for sh in (-4, 4, 8):           # the roadmap's releases landing earlier or later than planned
            w2 = dict(w, plan_weeks=np.clip(w["plan_weeks"] + sh, Y27 - 1, 181))
            print("probe releases %+d weeks against the roadmap: %.2f points" % (
                sh, math.sqrt(float((wt * inst["rel"] * release_exposure(w2, g0["cov"])).sum()))))
        print("probe replicate pair by family", np.round(inst["rep"], 2), "bootstrap net of seeds", np.round(g0["face"], 1))
        print("probe windows", w["window"], "custom", w["custom"], "epochs", w["epochs"], "panel", w["ms"], "book", w["merch"].astype(int))
        print("probe pinned views planned weeks", w["fv_planned"], "releases 2026:", int((w["rel_weeks"] >= Y26).sum()), "before:", int((w["rel_weeks"] < Y26).sum()))
        print("probe warm effective weeks", w["warm"]["eff"], "last cold", w["last_cold"], "curve starts", list(pk.t0))
        print("probe turnover factor share of window, 2027 against 2026: %s" % np.round(np.array([np.mean([turnover_factor(w, f, a, b, w["window"][f]) for a, b in SPANS27]) for f in range(F)]) / np.array([np.mean([turnover_factor(w, f, a, b, w["window"][f]) for a, b in SPANS26]) for f in range(F)]), 2))
        for s_ in ("optimisation", "turnover", "releases", "labels", "retunes"):
            lo, hi = math.sqrt(0.8 * g0["agg"][s_]), math.sqrt(1.2 * g0["agg"][s_])
            print("forcing %-13s variance down a fifth %.2f, up a fifth %.2f, band held %s" % (
                s_, lo, hi, sum(1 for l in LINES if lo >= l) == g0["band"][s_] == sum(1 for l in LINES if hi >= l)))

    # the standard's 1.4 files that a warm-started refit carries the randomness of the refits before it, so the
    # replicate pair read as the gap's whole noise (S2="hur") is refused; the hurried S2 adds thirteen refits' fresh
    # draws up in full. Its 1.5 files that no release moves a family on pinned views (S3="over" refused), and the
    # ask is for retrains expected to actually run on pinned views: the take-up is then a supporting step, not a stump.
    hur = {"S1": dict(S1="hur"), "S2": dict(S2="over")}
    lattice, lat_eval = {}, {}
    for key in ("S1", "S2", "S1+S2"):
        o = {}
        for st in key.split("+"):
            o.update(hur[st])
        lat_eval[key] = evaluate(pk, **o)
        lattice[key] = lat_eval[key]["points"]

    routes = {
        "direct": evaluate(pk, S1="raw", S2="over", S3="hur"),
        "rigorous": evaluate(pk, S1="hur", S2="over", S3="declared"),
        "generous": evaluate(pk, S1="square", S2="over", S3="worst"),
        "calibrated": evaluate(pk, S1="hur", S2="cal", S3="declared"),
        "hedge": evaluate(pk, S1="hur", S2="over", S3="hur"),
        "cutoff": evaluate(pk, S1="single", S2="cut", S3="threshold"),
    }
    extra = {"cutoff:lags from 1": evaluate(pk, S1="single", S2="cut", cut_lag=1, S3="threshold"),
             "cutoff:lags from 4": evaluate(pk, S1="single", S2="cut", cut_lag=4, S3="threshold"),
             "cutoff:lags from 12": evaluate(pk, S1="single", S2="cut", cut_lag=12, S3="threshold"),
             "cutoff:lags from 16": evaluate(pk, S1="single", S2="cut", cut_lag=16, S3="threshold"),
             "cutoff:two components": evaluate(pk, S1="single", S2="cut", S3="threshold", cut_custom=2),
             "cutoff:four components": evaluate(pk, S1="single", S2="cut", S3="threshold", cut_custom=4),
             "generous:rows out and rows in doubled": evaluate(pk, S1="double", S2="over", S3="worst"),
             "generous:turnover cancels": evaluate(pk, S1="over", S2="over", S3="worst"),
             "generous:a whole replicate pair a refit": evaluate(pk, S1="square", S2="over2", S3="worst"),
             "calibrated:plan dates": evaluate(pk, S1="hur", S2="cal", S3="hur"),
             "calibrated:the families' variance on their bootstrap spread": evaluate(pk, S1="regress", S2="over", S3="declared"),
             "hedge:2026's releases carried": evaluate(pk, S1="hur", S2="over", S3="y2026"),
             "hedge:a whole replicate pair a refit": evaluate(pk, S1="hur", S2="over2", S3="hur"),
             "hedge:the gap curve fitted free": evaluate(pk, S1="hur", fit="free26", S3="hur")}
    over = {"S1": evaluate(pk, S1="over"), "S2": evaluate(pk, S2="over2"), "S3": evaluate(pk, S3="over")}
    tpoints = {s: math.sqrt(tagg[s]) for s in SOURCES}

    members = {}
    for s in SOURCES:
        members[s] = {"lines": list(LINES), "truth": tpoints[s], "golden": gold["points"][s],
                      "family": [v["points"][s] for v in fam],
                      "routes": {"direct": routes["direct"]["points"][s], "rigorous": routes["rigorous"]["points"][s]}}

    def fig(fid, key, block, sentence=None, weight=1.0):
        d = {"id": fid, "block": block, "weight": weight, "golden": gold[key], "family": [v[key] for v in fam],
             "lattice": {k: lat_eval[k][key] for k in lat_eval},
             "routes": {r: routes[r][key] for r in ("rigorous", "generous", "calibrated", "hedge", "cutoff")}}
        if sentence:
            d["sentence"] = sentence
        return d

    figures = [{"id": "CC1 turnover alone, points", "block": "component", "member": "turnover"},
               {"id": "CC2 optimisation noise alone, points", "block": "component", "member": "optimisation"}]
    # the asks are each source's points and band and the pinned-views share. Each source's share of model-side
    # movement, merchants' own share and the two tier figures left the prompt on the author's ruling after the
    # Holistic Audit v3 (2026-11-22): the audit grades a figure computed from an earlier one on the response's own
    # earlier figure, so all four were earned by both runs whatever their movements (30 of 100 points); they are
    # still computed and checked, and stated in no graded block
    for s in SOURCES:
        figures += [fig("%s points, on its line" % s, "points_" + s, "ask", sentence="source " + s)]
    figures += [fig("pinned views share, on its own ask line", "cc3", "ask", sentence="pinned views")]

    d1_truth = float((wt * pk.d1).sum())
    fals = {"check": "the weekly score-change variance of the settled warm families in 2026, book weighted, which "
                     "the production record holds: each route's own model of how a source's variance grows with "
                     "the gap between two models is asked for it",
            "observes_target": False, "truth": d1_truth, "golden": weekly_prediction(pk, "golden"),
            "rivals": {"replicate variance at any gap": weekly_prediction(pk, dict(S2="hur")),
                       "bootstrap spread at any gap": weekly_prediction(pk, dict(S1="hur")),
                       "both at face value": weekly_prediction(pk, dict(S1="hur", S2="hur")),
                       "thirteen weekly refits added up": weekly_prediction(pk, dict(S2="over"))}}

    spec = {
        "task": "task9", "call": "lines", "members": members,
        "stumps": {
            "S1": {"axis": "unit", "opens": "turnover", "steps_left": 4, "precedents": ["L28", "L22", "N21"],
                   "said_out_loud": "A bootstrap pair resamples the whole training window, while two quarter-end "
                                    "models share every week of it but the thirteen that left and the thirteen that "
                                    "entered.",
                   "sides": {"over": over["S1"]["points"]}},
            "S2": {"axis": "what", "opens": "optimisation", "steps_left": 4, "precedents": ["L68", "N45", "L39"],
                   "said_out_loud": "The randomness a warm-started refit carries decays from refit to refit, so "
                                    "thirteen refits' fresh draws do not add up in full between two snapshots.",
                   "sides": {"over": over["S2"]["points"]}},
        },
        "lattice": lattice,
        "falsification": fals,
        "run_routes": dict({r: routes[r]["points"] for r in ("generous", "calibrated", "hedge", "cutoff")},
                           **{k: v["points"] for k, v in extra.items()}),
        "figures": figures,
        "waivers": waivers(),
    }

    if detail:
        np.set_printoptions(precision=3, suppress=True, linewidth=160)
        pr = lambda e: " ".join("%s %.2f (%.1f%%)" % (s[:5], e["points"][s], e["share"][s]) for s in SOURCES)
        print("truth points      ", {s: round(tpoints[s], 2) for s in SOURCES})
        print("truth variances   ", {s: round(tagg[s], 2) for s in SOURCES}, "own", round(float((wt * w['tau2'] * H).sum()), 1))
        print("golden            ", pr(gold))
        print("golden variances  ", {s: round(gold["agg"][s], 2) for s in SOURCES}, "own", round(gold["own"], 1))
        print("golden cc3 %.1f own share %.1f flip sched %.2f removed %.2f  fr26 %.2f" % (
            gold["cc3"], gold["own_share"], gold["fr_sched"], gold["fr_removed"], 100 * float((wt * pk.fr26).sum())))
        print("true coverage %.1f  plan %.1f  declared %.1f" % (100 * tcov[:, 1:].mean(),
              routes["direct"]["cc3"], routes["rigorous"]["cc3"]))
        print("phi true", w["phi"], "\nphi fit ", gold["phi"])
        print("13-week variance, weekly variance (book):", round(float((wt * pk.d13).sum()), 1), round(float((wt * pk.d1).sum()), 2))
        print("replicate pair %.2f  bootstrap data spread %.2f" % (float((wt * inst["rep"]).sum()), float((wt * gold["face"]).sum())))
        print("unanchored fit    ", pr(free), " implied fresh noise %.2f against the replicate pairs' %.2f" % (
            float((wt * free["A"] * (1 - free["phi"] ** 2)).sum()), float((wt * inst["rep"]).sum())))
        tail = lambda e: "cc3 %.1f own %.1f fr %.2f %.2f" % (e["cc3"], e["own_share"], e["fr_sched"], e["fr_removed"])
        for i, v in enumerate(variants):
            print("variant %-58s" % (str(v) or "{}"), pr(fam[i]), tail(fam[i]))
        for k in sorted(lat_eval):
            print("%-9s" % k, pr(lat_eval[k]), tail(lat_eval[k]))
        for k in list(routes) + list(extra):
            e = routes.get(k) or extra[k]
            print("%-38s" % k, pr(e), tail(e))
        for k, e in over.items():
            print("over %-4s" % k, pr(e))
        for name in ("runtime", "warm", "amp"):
            mdl = coverage_model(w, "loglin", leave=name)
            r = w[name]
            wk = np.arange(0, T)
            obs, pred, plan = [], [], []
            for f in range(F):
                d = r["declared"][f]
                span = np.arange(d, d + 39)
                on = (span >= r["eff"][f]) & ~((span >= r["revert"][f, 0]) & (span < r["revert"][f, 1]))
                obs.append(on.mean())
                pred.append(float(np.mean(lognormal_cdf(span - d, mdl["mu"][f], mdl["sg"]) * (1 - mdl["rev"]))))
            print("leave %-8s out: covered share of the 39 weeks after declared, record %.3f, model %.3f, calendar 1.000" % (
                name, np.mean(obs), np.mean(pred)))
        print("falsification", {k: round(v, 2) for k, v in fals["rivals"].items()}, "golden", round(fals["golden"], 2),
              "record", round(fals["truth"], 2))
    return {"spec": spec, "gold": gold, "variants": variants, "fam": fam, "free": free, "lattice": lat_eval,
            "routes": routes, "extra": extra, "over": over, "fals": fals, "tpoints": tpoints, "truth_share": truth}


if __name__ == "__main__":
    sys.exit(main())
