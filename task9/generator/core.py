"""task9 architecture 6 (Level-5 upgrade): Garrane Risk's weekly refreshed merchant scores, what each model-side
source alone moves a score between quarter-end snapshots in 2027, and the combined model-side movement across the
four quarter-end snapshot pairs and the year.

    python3 task9/generator/core.py             runs corelib (CORE PASS level 5, zero waivers)
    python3 task9/generator/core.py --detail    also prints the world, variants, lattice, cold-era check and forcing

Three independent stumps on three axes (zero closed strategies):
  S1 (what)  Optimisation noise: warm-started refits carry decaying randomness (phi_f in [0.65, 0.79]),
             identified from the bend of D_warm(h) anchored to replicate pairs, while strictly linear D_cold(h)
             in the cold-start era rules out mean-reverting merchant own change.
             Hurried/Rigorous: linear 13-refit carry -> Escalation; Over: raw replicate -> Monitor.
  S2 (when)  Training data: 52/104-week training windows apply exponential recency weighting (lambda_f unlisted,
             filed as WHAT in Standard 1.6 and manifest options), identified from seasonal volume swings in
             2026 weighted bootstrap pairs against warehouse weekly labelled rows.
             Hurried/Rigorous: uniform (entering+leaving)/(2N) -> Monitor; Over/Direct: bootstrap face -> Escalation.
  S3 (unit)  Feature releases: sequential releases modifying the same feature group move the same merchants in
             the same direction (positive merchant-level covariance c_f in [0.72, 0.84]), measured from 2026
             semi-annual release_shadow score vectors (27 weeks apart per group, keeping 2026 D_warm linear)
             and carried to 2027's multi-phase sprint roadmap alongside actual pinned-view adoption (supporting).
             Direct/Hurried/Rigorous: orthogonal releases -> Monitor; Over: all releases aligned -> Escalation.
"""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "..", ".agents", "skills", "stumping"))
import corelib  # noqa: E402

SEED = 9605
F = 14
G = 12
FRAC = 0.2
LEAVE = 0.09
T = 126                                                # 1 Jul 2024 to 23 Nov 2026 (weekly Mondays, 0..125)
PRE = 112                                              # warehouse history before 1 Jul 2024
H = 13                                                 # weeks between consecutive quarter-end snapshots
LAGS = 26
Y26 = 78                                               # first Monday of 2026 (29 Dec 2025)
Y27 = 130                                              # first Monday of 2027 pair year (28 Dec 2026)
SPANS26 = ((77, 90), (90, 103), (103, 116))            # 2026 closed quarter-end pairs (Dec 25 -> Sep 26)
SPANS27 = ((129, 142), (142, 155), (155, 168), (168, 181))  # 2027 assessment-year snapshot pairs
CUTS = (400.0, 500.0, 600.0)                           # Schedule C tier boundaries
LINES = (5.5, 8.0)                                     # Standard section 4.1 bands: Monitor / Remediation / Escalation
SOURCES = ("optimisation", "turnover", "retunes", "releases", "labels")


# --------------------------------------------------------------------------------------------- math primitives
def lognormal_cdf(x, mu, sg):
    x = np.asarray(x, float)
    z = (np.log(np.maximum(x, 1e-9)) - mu) / (max(float(sg), 1e-6) * math.sqrt(2.0))
    return np.where(x > 0, 0.5 * (1.0 + np.vectorize(math.erf)(z)), 0.0)


def normal_cdf(x):
    return 0.5 * (1.0 + math.erf(x / math.sqrt(2.0)))


def recency_weights(rows_f, wk0, t, W, lam):
    """Per-week probability weights p and labelled row counts n for a window of W weeks ending at refresh t."""
    i = wk0 + int(t)
    n = rows_f[i - W + 1:i + 1]
    if lam >= 0.999999:
        p = n / n.sum()
    else:
        ages = np.arange(W - 1, -1, -1, dtype=float)
        w_tot = (lam ** ages) * n
        p = w_tot / w_tot.sum()
    return p, n


def boot_factor(rows_f, wk0, t, W, lam):
    """Expected bootstrap pair variance per unit of per-row noise row2 at refresh t: 2 * sum(p_u^2 / n_u)."""
    p, n = recency_weights(rows_f, wk0, t, W, lam)
    return 2.0 * float(np.sum((p ** 2) / n))


def turn_factor(rows_f, wk0, t0, t1, W, lam, simple=False, entered=False):
    """Variance of (weighted window estimator at t1 - weighted window estimator at t0) per unit of row2."""
    p0, n0 = recency_weights(rows_f, wk0, t0, W, lam)
    p1, n1 = recency_weights(rows_f, wk0, t1, W, lam)
    h = int(t1 - t0)
    if h >= W:
        return float(np.sum((p0 ** 2) / n0) + np.sum((p1 ** 2) / n1))
    if entered:
        return float(np.sum((p1[W - h:] ** 2) / n1[W - h:]))
    if simple and lam >= 0.999999:
        n_a, n_b = n0.sum(), n1.sum()
        out_, in_ = n0[:h].sum(), n1[W - h:].sum()
        return float((in_ + out_) / (0.5 * (n_a + n_b)) ** 2)
    v_out = np.sum((p0[:h] ** 2) / n0[:h])
    v_in = np.sum((p1[W - h:] ** 2) / n1[W - h:])
    v_sh = np.sum(((p1[:W - h] - p0[h:]) ** 2) / n0[h:])
    return float(v_out + v_in + v_sh)


# --------------------------------------------------------------------------------------------- the world
def build_world(seed=SEED):
    rng = np.random.default_rng(seed)
    w = {}
    w["merch"] = rng.integers(2000, 21000, F).astype(float)
    w["ms"] = np.rint(FRAC * w["merch"]).astype(int)
    w["custom"] = rng.integers(0, 6, F)
    w["epochs"] = rng.choice([2, 3, 4], F, p=[0.3, 0.4, 0.3])
    # S1: warm-start persistence phi_f in [0.65, 0.79] (sharp early bend h=1..8, decoupled from S2)
    w["phi"] = np.array([{2: 0.78, 3: 0.72, 4: 0.66}[e] for e in w["epochs"]]) + rng.uniform(-0.008, 0.008, F)
    # S2: rolling window lengths (52 or 104 weeks) and exponential recency decay lambda_f
    w["window"] = np.where(rng.random(F) < 0.50, 104, 52)
    w["lam"] = np.where(w["window"] == 104, rng.uniform(0.928, 0.942, F), rng.uniform(0.905, 0.920, F))

    # Weekly labelled rows: family-specific seasonal cycles + multi-week promo/volume waves
    base_rows = w["merch"] * rng.uniform(10, 18, F)
    w["growth"] = rng.uniform(0.03, 0.28, F)
    wk = np.arange(-PRE, 190)
    w["wk0"] = PRE
    phase = rng.uniform(0, 52, F)
    amp1 = rng.uniform(0.45, 0.62, F)
    amp2 = rng.uniform(0.12, 0.22, F)
    rows = np.zeros((F, wk.size))
    for f in range(F):
        seas = np.exp(amp1[f] * np.cos(2.0 * np.pi * (wk - phase[f]) / 52.0) +
                      amp2[f] * np.sin(4.0 * np.pi * (wk - phase[f]) / 52.0))
        ar = np.zeros(wk.size)
        for j in range(1, wk.size):
            ar[j] = 0.80 * ar[j - 1] + rng.normal(0, 0.13)
        rows[f] = base_rows[f] * (1.0 + w["growth"][f]) ** (wk / 52.0) * seas * np.exp(ar + rng.normal(0, 0.04, wk.size))
    w["rows"] = rows

    small = (w["merch"] / w["merch"].mean()) ** -0.28
    jit = lambda s: np.exp(rng.normal(0, s, F))
    w["eta2"] = small * jit(0.14)
    w["cold2"] = 2.2 * w["eta2"]
    w["row2"] = small * jit(0.12)
    w["tau2"] = small * jit(0.20)
    w["lab2"] = jit(0.20)
    w["ret2"] = jit(0.20)
    w["rel2"] = jit(0.18)
    # S3: merchant-level directional coherence across same-group feature releases
    w["rel_coh"] = rng.uniform(0.72, 0.84, F)
    w["use"] = rng.uniform(0.55, 0.85, F)
    w["ret_off"] = rng.integers(0, 4, F)

    def rollout(lo, hi, min_eff=0):
        planned = rng.integers(lo, hi + 1, F)
        declared = planned + rng.integers(0, 4, F)
        lag = np.minimum(np.rint(np.exp(rng.normal(np.log(5 + 4 * w["custom"]), 0.28))), 40).astype(int)
        eff = np.maximum(declared + lag, min_eff)
        rev = np.zeros((F, 2), int)
        for f in range(F):
            if rng.random() < 0.30:
                a = eff[f] + rng.integers(2, 10)
                rev[f] = (a, a + rng.integers(3, 8))
        return {"planned": planned, "declared": declared, "eff": eff, "revert": rev}

    w["runtime"] = rollout(2, 7)
    w["warm"] = rollout(18, 25, min_eff=24)                # >= 24 cold weeks in every family for cold linearity test
    w["amp"] = rollout(34, 42)
    # Pinned feature views scheduled across H1 2027 (staggered waves across Q1 and Q2)
    w["fv_planned"] = rng.integers(131, 145, F)

    # 2024-2026 feature releases: semi-annual refresh per feature group in 2026 (24 releases = 2 per group),
    # spaced 27 weeks apart per group (H1 weeks 79..98, H2 weeks 106..125) so ZERO same-group pairs occur
    # inside lags h=1..26 of the 2026 warm panel, keeping V_rel(h) strictly linear in D_warm(h).
    rel_pre = [t for t in range(Y26) if rng.random() < 0.14]
    g_pre = rng.integers(0, G, len(rel_pre)).tolist()
    h1_wks = sorted(rng.choice(np.arange(Y26 + 1, 99), G, replace=False).tolist())
    h2_wks = [wk_ + 27 for wk_ in h1_wks]
    g_h1 = list(rng.permutation(G))
    g_h2 = list(g_h1)
    w["rel_weeks"] = np.array(rel_pre + h1_wks + h2_wks, int)
    w["rel_group"] = np.array(g_pre + g_h1 + g_h2, int)

    fam_reads = np.zeros((F, G), bool)
    for f in range(F):
        k_read = int(rng.integers(9, 12))
        fam_reads[f, rng.choice(G, k_read, replace=False)] = True
    w["fam_reads"] = fam_reads
    w["rel_hits"] = np.array([fam_reads[:, g] for g in w["rel_group"]], bool)

    # 2027 roadmap: 28 releases (7 per quarter-pair) organized into multi-phase feature-group sprints
    plan_weeks, plan_groups = [], []
    sprint_pairs = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (9, 10, 11)]
    for qi, (a, b) in enumerate(SPANS27):
        wks = np.sort(rng.choice(np.arange(a + 1, b + 1), 7, replace=False))
        g1, g2, g3 = sprint_pairs[qi]
        gs = [g1, g2, g1, g2, g1, g2, g3]
        plan_weeks.extend(wks.tolist())
        plan_groups.extend(gs)
    w["plan_weeks"] = np.array(plan_weeks, int)
    w["plan_group"] = np.array(plan_groups, int)
    w["plan_hits"] = np.array([fam_reads[:, g] for g in w["plan_group"]], bool)

    warm = np.zeros((F, T), bool)
    for f in range(F):
        warm[f, w["warm"]["eff"][f]:] = True
        a, b = w["warm"]["revert"][f]
        if b > a:
            warm[f, a:b] = False
    w["is_warm"] = warm
    w["last_cold"] = np.array([int(np.max(np.where(~warm[f])[0])) for f in range(F)])
    return w, rng


def past_adoption(w):
    """Per-rollout adoption lags and 26-week revert shares from the three completed platform rollouts."""
    rows = []
    for name in ("runtime", "warm", "amp"):
        r = w[name]
        for f in range(F):
            rv = max(0, min(r["revert"][f, 1], r["eff"][f] + 26) - r["revert"][f, 0])
            rows.append((name, f, int(w["custom"][f]), int(r["planned"][f]), int(r["declared"][f]),
                         int(r["eff"][f]), rv / 26.0))
    return rows


def coverage_model(w, kind="loglin", leave=None):
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
        mu = np.log(pred)
    elif kind == "groups":
        mu = np.array([np.mean(np.log(lag[c == x])) if np.any(c == x) else np.mean(np.log(lag)) for x in cf])
        sg = float(np.mean([np.std(np.log(lag[c == x]), ddof=1) for x in np.unique(c) if np.sum(c == x) > 2]))
    elif kind == "own":
        fam = np.array([r[1] for r in rows])
        mu = np.array([np.mean(np.log(lag[fam == f])) for f in range(F)])
        sg = float(np.sqrt(np.mean([np.var(np.log(lag[fam == f]), ddof=1) for f in range(F) if np.sum(fam == f) > 1])))
    else:
        mu = np.full(F, float(np.mean(np.log(lag))))
        sg = float(np.std(np.log(lag), ddof=1))
    return {"mu": mu, "sg": sg, "slip": slip, "rev": rev}


def coverage_weeks(w, mode, model=None, cut=3):
    """Expected pinned-view share by family over assessment-year weeks 129..181 (col 0 = week 129, cols 1..52 = 2027)."""
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
            cov[f] = (wk >= p + model["slip"]) if w["custom"][f] < cut else 0.0
        else:
            cov[f] = lognormal_cdf(wk - (p + model["slip"]), model["mu"][f], model["sg"]) * (1.0 - model["rev"])
    return cov


def true_coverage(w, rng, draws=3000):
    wk = np.arange(Y27 - 1, 182)
    cov = np.zeros((F, wk.size))
    for f in range(F):
        dec = w["fv_planned"][f] + rng.integers(0, 4, draws)
        lag = np.minimum(np.rint(np.exp(rng.normal(np.log(5 + 4 * w["custom"][f]), 0.28, draws))), 40)
        eff = dec + lag
        on = wk[None, :] >= eff[:, None]
        has = rng.random(draws) < 0.30
        a = eff + rng.integers(2, 10, draws)
        b = a + rng.integers(3, 8, draws)
        off = has[:, None] & (wk[None, :] >= a[:, None]) & (wk[None, :] < b[:, None])
        cov[f] = np.mean(on & ~off, axis=0)
    return cov


def release_pair_var(w, rel_v, coh_f, cov, mode="cov", span_idx=None):
    """Per-family expected feature-release MS per quarter-end pair (or one pair span_idx in 0..3).
    Under S3 (mode='cov'): same-group releases inside a snapshot pair carry correlation coh_f; different groups 0.
    Exact expectation over pinning time T_pin:
      E[Var(sum_{k in pair} 1(T_pin > t_k) j_k)]
        = sum_k P_live(t_k) v_f + 2 * sum_{k < l, g_k == g_l} P_live(max(t_k, t_l)) * coh_f * v_f.
    """
    spans = [SPANS27[span_idx]] if span_idx is not None else SPANS27
    out = np.zeros(F)
    for f in range(F):
        tot = 0.0
        for a, b in spans:
            idx = [k for k in range(len(w["plan_weeks"]))
                   if w["plan_hits"][k, f] and a < w["plan_weeks"][k] <= b]
            p_live = [1.0 - float(cov[f, w["plan_weeks"][k] - (Y27 - 1)]) for k in idx]
            var_pair = sum(pl * rel_v[f] for pl in p_live)
            if mode == "cov":
                for i1 in range(len(idx)):
                    for i2 in range(i1 + 1, len(idx)):
                        k1, k2 = idx[i1], idx[i2]
                        if w["plan_group"][k1] == w["plan_group"][k2]:
                            var_pair += 2.0 * min(p_live[i1], p_live[i2]) * coh_f[f] * rel_v[f]
            elif mode == "all_corr":
                for i1 in range(len(idx)):
                    for i2 in range(i1 + 1, len(idx)):
                        var_pair += 2.0 * min(p_live[i1], p_live[i2]) * 1.0 * rel_v[f]
            elif mode == "all_same_rho":
                for i1 in range(len(idx)):
                    for i2 in range(i1 + 1, len(idx)):
                        var_pair += 2.0 * min(p_live[i1], p_live[i2]) * coh_f[f] * rel_v[f]
            elif mode == "indep":
                pass
            tot += var_pair
        out[f] = tot / len(spans)
    return out


def scale_world(w):
    wt = w["merch"] / w["merch"].sum()
    tcov = true_coverage(w, np.random.default_rng(SEED + 1))
    tf = np.array([np.mean([turn_factor(w["rows"][f], w["wk0"], a, b, int(w["window"][f]), float(w["lam"][f]))
                            for a, b in SPANS27]) for f in range(F)])
    rel_unit = release_pair_var(w, np.ones(F), w["rel_coh"], tcov, mode="cov")
    TARGET = {"optimisation": 46.5, "turnover": 46.5, "retunes": 18.5, "releases": 47.0, "labels": 96.0, "merchant": 210.0}
    raw = {
        "optimisation": 2.0 * w["eta2"] / (1.0 - w["phi"] ** 2) * (1.0 - w["phi"] ** H),
        "turnover": w["row2"] * tf,
        "retunes": w["ret2"] * H / 4.0,
        "releases": w["rel2"] * rel_unit,
        "labels": w["lab2"] * H,
        "merchant": w["tau2"] * H,
    }
    key = {"optimisation": ("eta2", "cold2"), "turnover": ("row2",), "retunes": ("ret2",),
           "releases": ("rel2",), "labels": ("lab2",), "merchant": ("tau2",)}
    for s, ks in key.items():
        k = TARGET[s] / float((wt * raw[s]).sum())
        for name in ks:
            w[name] = w[name] * k
    return w


def simulate(w, rng, keep=None):
    """Simulate Garrane Risk's 2024-2026 weekly panel and 2026 instruments. When keep is a dict, retain raw draws."""
    z = [None] * F
    inst = {
        "rep": np.zeros(F), "ret": np.zeros(F), "rel": np.zeros(F), "lab": np.zeros(F),
        "boot_t": [], "boot_v": [], "boot_n": [],
        "rel_coh_same": np.zeros(F), "rel_coh_diff": np.zeros(F),
        "rel_cov_same": np.zeros(F), "rel_cov_diff": np.zeros(F),
        "rel_coh_same_pairs": [], "rel_coh_diff_pairs": [],
    }
    boot_weeks = np.arange(Y26 + 1, T, 3)  # 16 bootstrap pairs per family across 2026
    for f in range(F):
        MS = int(w["ms"][f])
        base = rng.normal(500.0, 100.0, MS)
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
                        keep.setdefault("ret", []).append((f, int(t), j))
        # S3: fixed merchant-level latent sensitivity u_{m,g} to each feature group g
        u_grp = rng.normal(0, 1.0, (MS, G))
        rel = np.zeros((MS, T))
        rel_vecs_26 = []
        c_f = float(w["rel_coh"][f])
        for k, t in enumerate(w["rel_weeks"]):
            if w["rel_hits"][k, f]:
                g = int(w["rel_group"][k])
                j = math.sqrt(w["rel2"][f]) * (math.sqrt(c_f) * u_grp[:, g] + math.sqrt(1.0 - c_f) * rng.normal(0, 1.0, MS))
                rel[:, t:] += j[:, None]
                if t >= Y26:
                    rel_vecs_26.append((g, j))
                    if keep is not None:
                        keep.setdefault("rel", []).append((f, int(k), int(t), j))
        # S2: training data noise -- uniform 26w in cold era, exponential recency lambda_f in warm 52/104w era
        rows = w["rows"][f]
        eps = rng.normal(0, 1.0, (MS, rows.size)) * np.sqrt(w["row2"][f] * rows)[None, :]
        data = np.zeros((MS, T))
        opt = np.zeros((MS, T))
        e = np.zeros(MS)
        W_warm = int(w["window"][f])
        lam_f = float(w["lam"][f])
        ages_w = np.arange(W_warm - 1, -1, -1, dtype=float)
        a_warm = lam_f ** ages_w
        for t in range(T):
            i = w["wk0"] + t
            if t >= w["warm"]["eff"][f]:
                n_win = rows[i - W_warm + 1:i + 1]
                w_tot = a_warm * n_win
                data[:, t] = (eps[:, i - W_warm + 1:i + 1] @ a_warm) / w_tot.sum()
            else:
                n_win = rows[i - 26 + 1:i + 1]
                data[:, t] = eps[:, i - 26 + 1:i + 1].sum(axis=1) / n_win.sum()
            if w["is_warm"][f, t]:
                e = w["phi"][f] * e + rng.normal(0, math.sqrt(w["eta2"][f]), MS)
            else:
                e = rng.normal(0, math.sqrt(w["cold2"][f]), MS)
            opt[:, t] = e
        z[f] = base[:, None] + own + lab + ret + rel + data + opt
        if keep is not None:
            keep.setdefault("lab_path", {})[f] = lab
            keep.setdefault("opt", {})[f] = opt
        left = np.where(rng.random(MS) < 1.0 - (1.0 - LEAVE) ** (T / 52.0), rng.integers(8, T, MS), T)
        z[f][np.arange(T)[None, :] >= left[:, None]] = np.nan
        if keep is not None:
            keep.setdefault("left", {})[f] = left

        # 2026 instruments
        rep_w = np.sort(rng.choice(np.arange(Y26 + 4, T), 6, replace=False))
        rv = []
        for t in rep_w:
            a_ = rng.normal(0, math.sqrt(w["eta2"][f]), MS)
            b_ = rng.normal(0, math.sqrt(w["eta2"][f]), MS)
            rv.append(float(np.var(a_ - b_)))
            if keep is not None:
                keep.setdefault("rep", []).append((f, int(t), a_, b_))
        inst["rep"][f] = float(np.mean(rv))

        bt_list, bv_list, bn_list = [], [], []
        for t in boot_weeks:
            bf = boot_factor(rows, w["wk0"], int(t), W_warm, lam_f)
            sd = math.sqrt(w["eta2"][f] + 0.5 * w["row2"][f] * bf)
            a_ = rng.normal(0, sd, MS)
            b_ = rng.normal(0, sd, MS)
            n_sum = float(rows[w["wk0"] + int(t) - W_warm + 1:w["wk0"] + int(t) + 1].sum())
            bt_list.append(int(t))
            bv_list.append(float(np.var(a_ - b_)))
            bn_list.append(n_sum)
            if keep is not None:
                keep.setdefault("boot", []).append((f, int(t), a_, b_, n_sum))
        inst["boot_t"].append(np.array(bt_list, int))
        inst["boot_v"].append(np.array(bv_list, float))
        inst["boot_n"].append(np.array(bn_list, float))

        inst["ret"][f] = float(np.mean([np.var(j) for j in jumps]))
        inst["rel"][f] = float(np.mean([np.var(j) for _, j in rel_vecs_26]))
        same_c, diff_c, same_cv, diff_cv = [], [], [], []
        for i1 in range(len(rel_vecs_26)):
            g1, v1 = rel_vecs_26[i1]
            for i2 in range(i1 + 1, len(rel_vecs_26)):
                g2, v2 = rel_vecs_26[i2]
                corr = float(np.corrcoef(v1, v2)[0, 1])
                covv = float(np.cov(v1, v2, ddof=0)[0, 1])
                if g1 == g2:
                    same_c.append(corr)
                    same_cv.append(covv)
                else:
                    diff_c.append(corr)
                    diff_cv.append(covv)
        inst["rel_coh_same"][f] = float(np.mean(same_c))
        inst["rel_coh_diff"][f] = float(np.mean(diff_c))
        inst["rel_cov_same"][f] = float(np.mean(same_cv))
        inst["rel_cov_diff"][f] = float(np.mean(diff_cv))
        inst["rel_coh_same_pairs"].extend(same_c)
        inst["rel_coh_diff_pairs"].extend(diff_c)

        lw = np.sort(rng.choice(np.arange(Y26 + 4, T), 8, replace=False))
        inst["lab"][f] = float(np.mean([np.var(np.diff(lab[:, t - 1:t + 1], axis=1)) for t in lw]))
        if keep is not None:
            keep.setdefault("lab", []).extend((f, int(t)) for t in lw)
    return z, inst


# --------------------------------------------------------------------------------------------- estimators on the record
def lag_curve(w, z, f, lags=LAGS, start=None, end=None):
    end = int(w.get("T", T)) if end is None else int(end)
    t0 = max(int(w["last_cold"][f]) + 13, 66) if start is None else int(start)
    return np.array([np.nanmean((z[f][:, t0 + h:end] - z[f][:, t0:end - h]) ** 2) for h in range(1, lags + 1)]), t0


def events_in_span(w, f, t0, lags):
    tt = int(w.get("T", T))
    ret = np.array([(t - w["ret_off"][f]) % 4 == 0 for t in range(tt)], float)
    rel = np.zeros(tt)
    for k, t in enumerate(w["rel_weeks"]):
        if w["rel_hits"][k, f] and t < tt:
            rel[t] += 1.0
    cr, cl = np.cumsum(ret), np.cumsum(rel)
    out = []
    for h in range(1, lags + 1):
        s = np.arange(t0, tt - h)
        out.append((float(np.mean(cr[s + h] - cr[s])), float(np.mean(cl[s + h] - cl[s]))))
    return np.array(out)


def fit_bend(D, rep, lags=25, anchored=True, lo=1, flat=False):
    """D(h) = b*h + A*(1 - phi^h), anchored at A*(1 - phi^2) = rep."""
    h = np.arange(1, len(D) + 1)[lo - 1:lags]
    d = D[lo - 1:lags]
    wgt = np.ones_like(d) if flat else 1.0 / (d ** 2)
    best = None
    for phi in np.arange(0.45, 0.9851, 0.0025):
        g = 1.0 - phi ** h
        if anchored:
            A = rep / (1.0 - phi ** 2)
            b = float(np.sum(wgt * h * (d - A * g)) / np.sum(wgt * h * h))
        else:
            X = np.vstack([h, g]).T * np.sqrt(wgt)[:, None]
            b, A = np.linalg.lstsq(X, d * np.sqrt(wgt), rcond=None)[0]
        sse = float(np.sum(wgt * (d - b * h - A * g) ** 2))
        if A > 0 and (best is None or sse < best[0]):
            best = (sse, phi, A, b)
    return float(best[1]), float(best[2]), float(best[3])


def _bf_grid(w, inst, grid):
    """Vectorized bootstrap variance factors bf_grid[f] of shape (len(grid), n_boot) and net_v[f]."""
    bf_grid, net_v = [], []
    for f in range(F):
        net_v.append(np.maximum(inst["boot_v"][f] - inst["rep"][f], 0.5))
        W = int(w["window"][f])
        bt = inst["boot_t"][f]
        ages = np.arange(W - 1, -1, -1, dtype=float)
        # N_mat: (n_boot, W)
        N_mat = np.array([w["rows"][f][w["wk0"] + int(t) - W + 1:w["wk0"] + int(t) + 1] for t in bt], float)
        # A_mat: (len(grid), W)
        A_mat = grid[:, None] ** ages[None, :]
        # num = sum_u (a_u^2 * n_u) = A_mat^2 @ N_mat.T, den = (A_mat @ N_mat.T)^2
        den = A_mat @ N_mat.T
        num = (A_mat ** 2) @ N_mat.T
        bf_grid.append(2.0 * num / (den ** 2))
    return bf_grid, net_v


def fit_recency(w, inst, mode="family", loss="log", _cache=None):
    """Estimate exponential recency decay lambda_f and per-row noise row2_f from 2026 bootstrap pairs vs warehouse rows."""
    grid = np.linspace(0.75, 1.00, 251)
    bf_grid, net_v = _bf_grid(w, inst, grid) if _cache is None else _cache

    def fit_group(fams):
        best = None
        for gi, lam in enumerate(grid):
            tot_sse = 0.0
            c_map = {}
            for f in fams:
                bf = bf_grid[f][gi]
                y = net_v[f]
                if loss == "log":
                    c = math.exp(float(np.mean(np.log(y) - np.log(bf))))
                    tot_sse += float(np.sum((np.log(y) - np.log(c * bf)) ** 2))
                elif loss == "wls":
                    c = float(np.sum((y * bf) / (y ** 2)) / np.sum((bf ** 2) / (y ** 2)))
                    tot_sse += float(np.sum(((y - c * bf) / y) ** 2))
                else:
                    c = float(np.sum(y * bf) / np.sum(bf ** 2))
                    tot_sse += float(np.sum((y - c * bf) ** 2))
                c_map[f] = c
            if best is None or tot_sse < best[0]:
                best = (tot_sse, float(lam), c_map)
        return best[1], best[2], best[0]

    lam_hat, row2_hat = np.zeros(F), np.zeros(F)
    if mode == "family":
        for f in range(F):
            l, cm, _ = fit_group([f])
            lam_hat[f], row2_hat[f] = l, cm[f]
    elif mode == "window":
        for W in (52, 104):
            fams = [f for f in range(F) if int(w["window"][f]) == W]
            if fams:
                l, cm, _ = fit_group(fams)
                for f in fams:
                    lam_hat[f], row2_hat[f] = l, cm[f]
    else:
        l, cm, _ = fit_group(list(range(F)))
        for f in range(F):
            lam_hat[f], row2_hat[f] = l, cm[f]
    return lam_hat, row2_hat


def fit_recency_all(w, inst):
    grid = np.linspace(0.75, 1.00, 251)
    cache = _bf_grid(w, inst, grid)
    return {
        "fam_log": fit_recency(w, inst, "family", "log", _cache=cache),
        "win_log": fit_recency(w, inst, "window", "log", _cache=cache),
        "pool_log": fit_recency(w, inst, "pooled", "log", _cache=cache),
        "fam_wls": fit_recency(w, inst, "family", "wls", _cache=cache),
        "fam_ols": fit_recency(w, inst, "family", "ols", _cache=cache),
    }


def flip_rate(z, spans):
    out = np.zeros(F)
    for f in range(F):
        rates = []
        for a, b in spans:
            za, zb = z[f][:, a], z[f][:, b]
            ok = ~np.isnan(za) & ~np.isnan(zb)
            ta = np.searchsorted(CUTS, za[ok], side="right")
            tb = np.searchsorted(CUTS, zb[ok], side="right")
            rates.append(float(np.mean(ta != tb)))
        out[f] = float(np.mean(rates))
    return out


class Pack:
    """Everything computed once from the record (simulated world or loaded target/), cached for all estimators."""

    def __init__(self, w, z, inst):
        self.w, self.z, self.inst = w, z, inst
        self.T = int(w.get("T", T))
        self.curves, self.t0 = [], []
        self.cold_curves, self.cold_curv = [], []
        for f in range(F):
            c, t0 = lag_curve(w, z, f, lags=LAGS)
            self.curves.append(c)
            self.t0.append(t0)
            end_c = int(w["warm"]["eff"][f])
            dc, _ = lag_curve(w, z, f, lags=14, start=0, end=end_c)
            self.cold_curves.append(dc)
            hc = np.arange(1, 15)
            p2 = np.polyfit(hc, dc, 2)
            self.cold_curv.append(float(p2[0] * 14.0 ** 2 / dc[-1]))
        self.t0 = tuple(self.t0)
        self.events = [events_in_span(w, f, self.t0[f], LAGS) for f in range(F)]
        self.curves26 = [lag_curve(w, z, f, lags=LAGS, start=max(self.t0[f], Y26))[0] for f in range(F)]
        self.d13 = np.array([c[H - 1] for c in self.curves])
        self.d1 = np.array([c[0] for c in self.curves])
        self.fr26 = flip_rate(z, SPANS26)
        self.p26 = np.array([np.mean([np.nanmean((z[f][:, b] - z[f][:, a]) ** 2) for a, b in SPANS26]) for f in range(F)])
        self.models = {k: coverage_model(w, k) for k in ("loglin", "linear", "groups", "own", "pooled")}
        self.models["norevert"] = dict(self.models["loglin"], rev=0.0)
        self.rec = fit_recency_all(w, inst)
        self.dc_gold = self._data_curve(*self.rec["fam_log"])
        # 2026 internal-record targets for the 3-part native-unit (points^2) falsification check
        wt = w["merch"] / w["merch"].sum()
        self.obs_d1 = float(wt @ self.d1)
        self.boot_low_idx, self.boot_hi_idx = [], []
        bc_f = np.zeros(F)
        for f in range(F):
            bt = inst["boot_t"][f]
            tr8 = np.array([w["rows"][f][w["wk0"] + int(t) - 7:w["wk0"] + int(t) + 1].sum() for t in bt])
            order = np.argsort(tr8)
            mid = len(bt) // 2
            lo_i, hi_i = order[:mid], order[mid:]
            self.boot_low_idx.append(lo_i)
            self.boot_hi_idx.append(hi_i)
            net_v = np.maximum(inst["boot_v"][f] - inst["rep"][f], 0.0)
            bc_f[f] = float(np.mean(net_v[lo_i]) - np.mean(net_v[hi_i]))
        self.obs_boot_contrast = float(wt @ bc_f)
        self.obs_rel_cov = float(wt @ inst["rel_cov_same"])

    def _data_curve(self, lam_vec, row2_vec):
        dc = np.zeros((F, LAGS))
        for f in range(F):
            W = int(self.w["window"][f])
            t0 = self.t0[f]
            for h in range(1, LAGS + 1):
                dc[f, h - 1] = row2_vec[f] * np.mean([
                    turn_factor(self.w["rows"][f], self.w["wk0"], t, t + h, W, lam_vec[f])
                    for t in range(t0, self.T - h)
                ])
        return dc


DEFAULT = dict(S1="gold", S2="gold", S3="gold", fit="anch25", sub_data=True,
               rec_key="fam_log", rel_coh="family", adopt="loglin",
               cov_mode="model", cut=3, weights="current", cov=None)


def evaluate(pk, **opt):
    o = dict(DEFAULT, **opt)
    w, inst = pk.w, pk.inst
    rep = inst["rep"]
    wt = w["merch"] / w["merch"].sum()

    # S2: Training data
    if o["S2"] == "gold":
        lam_h, r2_h = pk.rec[o["rec_key"]]
        tur_q = np.array([[r2_h[f] * turn_factor(w["rows"][f], w["wk0"], a, b, int(w["window"][f]), lam_h[f])
                           for a, b in SPANS27] for f in range(F)])
        tur26 = np.array([r2_h[f] * np.mean([turn_factor(w["rows"][f], w["wk0"], a, b, int(w["window"][f]), lam_h[f])
                                             for a, b in SPANS26]) for f in range(F)])
        tur27 = tur_q.mean(axis=1)
        pred_bc_f = np.zeros(F)
        for f in range(F):
            bt = inst["boot_t"][f]
            W = int(w["window"][f])
            pb = np.array([r2_h[f] * boot_factor(w["rows"][f], w["wk0"], int(t), W, lam_h[f]) for t in bt])
            pred_bc_f[f] = float(np.mean(pb[pk.boot_low_idx[f]]) - np.mean(pb[pk.boot_hi_idx[f]]))
    elif o["S2"] in ("unif", "unif_raw"):
        bv = np.array([np.mean(v) for v in inst["boot_v"]])
        bn = np.array([np.mean(n) for n in inst["boot_n"]])
        face = bv if o["S2"] == "unif_raw" else np.maximum(bv - rep, 0.0)
        r2_h = 0.5 * face * bn
        lam_h = np.ones(F)
        tur_q = np.array([[r2_h[f] * turn_factor(w["rows"][f], w["wk0"], a, b, int(w["window"][f]), 1.0)
                           for a, b in SPANS27] for f in range(F)])
        tur26 = np.array([r2_h[f] * np.mean([turn_factor(w["rows"][f], w["wk0"], a, b, int(w["window"][f]), 1.0)
                                             for a, b in SPANS26]) for f in range(F)])
        tur27 = tur_q.mean(axis=1)
        pred_bc_f = np.zeros(F)
        for f in range(F):
            bt = inst["boot_t"][f]
            W = int(w["window"][f])
            pb = np.array([r2_h[f] * boot_factor(w["rows"][f], w["wk0"], int(t), W, 1.0) for t in bt])
            pred_bc_f[f] = float(np.mean(pb[pk.boot_low_idx[f]]) - np.mean(pb[pk.boot_hi_idx[f]]))
    elif o["S2"] in ("raw", "over", "cutoff_13w"):
        bv = np.array([np.mean(v) for v in inst["boot_v"]])
        bn = np.array([np.mean(n) for n in inst["boot_n"]])
        face = bv if o["S2"] == "raw" else np.maximum(bv - rep, 0.0)
        lam_h, r2_h = np.zeros(F), 0.5 * face * bn
        tur_q = np.repeat(face[:, None], 4, axis=1)
        tur26 = face.copy()
        tur27 = face.copy()
        pred_bc_f = np.zeros(F)
    elif o["S2"] == "half_w":
        bv = np.array([np.mean(v) for v in inst["boot_v"]])
        bn = np.array([np.mean(n) for n in inst["boot_n"]])
        face = np.maximum(bv - rep, 0.0)
        lam_h, r2_h = np.ones(F), 0.5 * face * bn
        tur27 = face * np.minimum(2.0 * H / w["window"], 1.0)
        tur26 = tur27.copy()
        tur_q = np.repeat(tur27[:, None], 4, axis=1)
        pred_bc_f = np.zeros(F)

    # S1: Optimisation noise
    phi_h, A_h, sl_h = np.zeros(F), np.zeros(F), np.zeros(F)
    if o["S1"] == "gold":
        sub = pk.dc_gold if (o["sub_data"] and o["S2"] == "gold") else np.zeros((F, LAGS))
        opt13 = np.zeros(F)
        for f in range(F):
            D = (pk.curves26[f] if o["fit"] == "y2026" else pk.curves[f]) - sub[f]
            kw = {"anch25": dict(lags=25), "anch20": dict(lags=20), "anch18": dict(lags=18),
                  "y2026": dict(lags=25), "flat": dict(lags=25, flat=True),
                  "from2": dict(lags=25, lo=2), "free25": dict(lags=25, anchored=False)}[o["fit"]]
            phi_h[f], A_h[f], sl_h[f] = fit_bend(D, rep[f], **kw)
            opt13[f] = A_h[f] * (1.0 - phi_h[f] ** H)
        pred_d1_f = sl_h + A_h * (1.0 - phi_h) + sub[:, 0]
    elif o["S1"] == "linear":
        opt13 = H * rep / 2.0
        pred_d1_f = pk.d13 / H
    elif o["S1"] == "linear2":
        opt13 = H * rep
        pred_d1_f = pk.d13 / H
    elif o["S1"] == "over":
        opt13 = rep.copy()
        pred_d1_f = rep + (pk.d13 - rep) / H
    elif o["S1"] == "cut8":
        opt13 = np.array([max(float(np.polyfit(np.arange(8, 26), pk.curves[f][7:25], 1)[1]), 0.0) for f in range(F)])
        pred_d1_f = opt13 + (pk.d13 - opt13) / H
    opt_q = np.repeat(opt13[:, None], 4, axis=1)

    # S3: Feature releases + pinned views (supporting)
    m = pk.models[o["adopt"]]
    cov = o["cov"] if o["cov"] is not None else coverage_weeks(w, o["cov_mode"], m, cut=o["cut"])
    coh_vec = inst["rel_coh_same"] if o["rel_coh"] == "family" else np.full(F, float(np.mean(inst["rel_coh_same_pairs"])))
    rel_mode = {"gold": "cov", "indep": "indep", "over": "all_corr", "all_same_rho": "all_same_rho"}[o["S3"]]
    rel_q = np.array([release_pair_var(w, inst["rel"], coh_vec, cov, mode=rel_mode, span_idx=qi) for qi in range(4)]).T
    rel27 = rel_q.mean(axis=1)
    if o["S3"] == "gold":
        pred_rc_f = coh_vec * inst["rel"]
    elif o["S3"] == "indep":
        pred_rc_f = np.zeros(F)
    else:
        pred_rc_f = inst["rel"].copy()

    ret13 = inst["ret"] * H / 4.0
    lab13 = inst["lab"] * H
    ret_q = np.repeat(ret13[:, None], 4, axis=1)
    lab_q = np.repeat(lab13[:, None], 4, axis=1)

    wgt = w["merch"] / w["merch"].sum()
    if o["weights"] == "plan":
        wgt = w["merch"] * (1.0 + w["growth"])
        wgt /= wgt.sum()
    elif o["weights"] == "equal":
        wgt = np.full(F, 1.0 / F)

    comp = {"optimisation": opt13, "turnover": tur27, "retunes": ret13, "releases": rel27, "labels": lab13}
    agg = {s: float(wgt @ v) for s, v in comp.items()}
    points = {s: math.sqrt(agg[s]) for s in SOURCES}
    band = {s: sum(1 for l in LINES if points[s] >= l) for s in SOURCES}
    model_side = sum(agg.values())
    share = {s: 100.0 * agg[s] / model_side for s in SOURCES}

    # Combined model-side RMS per 2027 snapshot pair (Q1..Q4) and full year (Standard section 3.2)
    tot_q_ms = [float(wgt @ (opt_q[:, qi] + tur_q[:, qi] + ret_q[:, qi] + rel_q[:, qi] + lab_q[:, qi])) for qi in range(4)]
    tot_q = [math.sqrt(x) for x in tot_q_ms]
    tot_yr = math.sqrt(float(np.mean(tot_q_ms)))
    cc_pin = 100.0 * float(np.mean(cov[:, 1:]))

    # Supplement (Standard sections 5.2 and 6.1 -- carried in workbook/notes, not graded asks)
    rel26 = inst["rel"] * np.array([pk.events[f][H - 1, 1] for f in range(F)])
    own_f = np.maximum(pk.d13 - (opt13 + tur26 + ret13 + rel26 + lab13), 10.0)
    own_a = float(wgt @ own_f)
    own_share = 100.0 * own_a / (own_a + model_side)
    v26 = pk.d13
    v27 = own_f + opt13 + tur27 + ret13 + rel27 + lab13
    gone = sum(comp[s] for s in SOURCES if band[s] >= 1)
    fr_sched = 100.0 * float(wgt @ (pk.fr26 * np.sqrt(v27 / np.maximum(v26, 1.0))))
    fr_removed = 100.0 * float(wgt @ (pk.fr26 * np.sqrt(np.maximum(v27 - gone, 0.0) / np.maximum(v26, 1.0))))

    # 3-part native-unit (points^2) falsification discrepancy against 2026 internal record
    f1_err = abs(float(wt @ pred_d1_f) - pk.obs_d1)
    f2_err = abs(float(wt @ pred_bc_f) - pk.obs_boot_contrast)
    f3_err = abs(float(wt @ pred_rc_f) - pk.obs_rel_cov)
    fals_err = f1_err + f2_err + f3_err

    out = {
        "points": points, "agg": agg, "share": share, "band": band, "own": own_a, "own_share": own_share,
        "fr_sched": fr_sched, "fr_removed": fr_removed,
        "tot_q": tot_q, "tot_q_ms": tot_q_ms, "tot_yr": tot_yr, "cc_pin": cc_pin,
        "cc1": points["optimisation"], "cc2": points["turnover"], "cc3": points["releases"],
        "phi": phi_h, "A": A_h, "slope": sl_h, "opt13": opt13,
        "lam": lam_h, "row2": r2_h, "tur": tur27, "tur_q": tur_q, "rel_q": rel_q, "rel27": rel27,
        "cov": cov, "coh": coh_vec,
        "fals_err": fals_err, "f_parts": (f1_err, f2_err, f3_err),
        "pred_d1": float(wt @ pred_d1_f), "pred_bc": float(wt @ pred_bc_f), "pred_rc": float(wt @ pred_rc_f),
    }
    for s in SOURCES:
        out["points_" + s] = points[s]
        out["share_" + s] = share[s]
    for qi in range(4):
        out["tot_q%d" % (qi + 1)] = tot_q[qi]
    return out


def world(keep=None):
    w, rng = build_world()
    w = scale_world(w)
    z, inst = simulate(w, rng, keep)
    return w, z, inst


def truth_of(w):
    wt = w["merch"] / w["merch"].sum()
    tcov = true_coverage(w, np.random.default_rng(SEED + 2))
    t_tf = np.array([np.mean([turn_factor(w["rows"][f], w["wk0"], a, b, int(w["window"][f]), float(w["lam"][f]))
                              for a, b in SPANS27]) for f in range(F)])
    tcomp = {
        "optimisation": 2.0 * w["eta2"] / (1.0 - w["phi"] ** 2) * (1.0 - w["phi"] ** H),
        "turnover": w["row2"] * t_tf,
        "retunes": w["ret2"] * H / 4.0,
        "releases": release_pair_var(w, w["rel2"], w["rel_coh"], tcov, mode="cov"),
        "labels": w["lab2"] * H,
    }
    tagg = {s: float(wt @ v) for s, v in tcomp.items()}
    return tcov, tagg


def analyse(pk, truth=None, detail=False):
    w, inst = pk.w, pk.inst
    wt = w["merch"] / w["merch"].sum()
    if truth is None:
        truth = (None, evaluate(pk)["agg"])
    tcov, tagg = truth
    tpoints = {s: math.sqrt(tagg[s]) for s in SOURCES}

    gold = evaluate(pk)
    variants = [
        dict(),
        dict(fit="anch20"),
        dict(fit="anch18"),
        dict(fit="y2026"),
        dict(fit="flat"),
        dict(fit="from2"),
        dict(sub_data=False),
        dict(rec_key="win_log"),
        dict(rec_key="pool_log"),
        dict(rec_key="fam_wls"),
        dict(rec_key="fam_ols"),
        dict(rel_coh="pooled"),
        dict(adopt="linear"),
        dict(adopt="groups"),
        dict(adopt="own"),
        dict(adopt="pooled"),
        dict(adopt="norevert"),
        dict(weights="plan"),
        dict(fit="anch20", rec_key="win_log", rel_coh="pooled", adopt="linear"),
        dict(fit="flat", rec_key="pool_log", adopt="groups", weights="plan"),
        dict(sub_data=False, rec_key="fam_wls", adopt="own"),
        dict(fit="from2", rec_key="fam_ols", rel_coh="pooled", adopt="norevert"),
    ]
    fam = [evaluate(pk, **v) for v in variants]
    free = evaluate(pk, fit="free25")

    hur = {"S1": dict(S1="linear"), "S2": dict(S2="unif"), "S3": dict(S3="indep")}
    lat_eval, lattice = {}, {}
    for key in ("S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"):
        kw = {}
        for st in key.split("+"):
            kw.update(hur[st])
        lat_eval[key] = evaluate(pk, **kw)
        lattice[key] = lat_eval[key]["points"]

    routes = {
        "direct": evaluate(pk, S1="linear", S2="raw", S3="indep", cov_mode="plan"),
        "rigorous": evaluate(pk, S1="linear", S2="unif", S3="indep", adopt="own"),
        "generous": evaluate(pk, S1="linear2", S2="over", S3="over", cov_mode="worst"),
        "calibrated": evaluate(pk, S1="cut8", S2="unif_raw", S3="indep", cov_mode="declared"),
        "hedge": evaluate(pk, S1="linear", S2="unif", S3="indep", cov_mode="plan"),
        "cutoff": evaluate(pk, S1="cut8", S2="cutoff_13w", S3="indep", cov_mode="threshold", cut=3),
    }
    extra = {
        "generous:all same rho": evaluate(pk, S1="linear2", S2="over", S3="all_same_rho", cov_mode="worst"),
        "generous:plan dates with aligned releases": evaluate(pk, S1="linear2", S2="over", S3="over", cov_mode="plan"),
        "calibrated:free gap fit": evaluate(pk, fit="free25", S2="unif", S3="indep", cov_mode="declared"),
        "calibrated:plan dates": evaluate(pk, S1="cut8", S2="unif_raw", S3="indep", cov_mode="plan"),
        "hedge:half window shortcut": evaluate(pk, S1="linear", S2="half_w", S3="indep", cov_mode="plan"),
        "hedge:full replicate pair per refit": evaluate(pk, S1="linear2", S2="unif", S3="indep", cov_mode="own"),
        "cutoff:cut 2": evaluate(pk, S1="cut8", S2="cutoff_13w", S3="indep", cov_mode="threshold", cut=2),
        "cutoff:cut 4": evaluate(pk, S1="cut8", S2="cutoff_13w", S3="indep", cov_mode="threshold", cut=4),
    }
    over = {
        "S1": evaluate(pk, S1="over"),          # raw replicate pair -> Monitor
        "S2": evaluate(pk, S2="over"),          # net bootstrap face value -> Escalation
        "S3": evaluate(pk, S3="over"),          # all releases perfectly aligned -> Escalation
    }

    members = {
        s: {
            "lines": list(LINES), "truth": tpoints[s], "golden": gold["points"][s],
            "family": [v["points"][s] for v in fam],
            "routes": {"direct": routes["direct"]["points"][s], "rigorous": routes["rigorous"]["points"][s]},
        } for s in SOURCES
    }

    def fig(fid, key, block, sentence=None, weight=1.0):
        d = {
            "id": fid, "block": block, "weight": weight, "golden": gold[key],
            "family": [v[key] for v in fam],
            "lattice": {k: lat_eval[k][key] for k in lat_eval},
            "routes": {r: routes[r][key] for r in ("rigorous", "generous", "calibrated", "hedge", "cutoff")},
        }
        if sentence:
            d["sentence"] = sentence
        return d

    figures = [
        {"id": "CC1 optimisation noise alone, points", "block": "component", "member": "optimisation"},
        {"id": "CC2 training data alone, points", "block": "component", "member": "turnover"},
        {"id": "CC3 feature releases alone, points", "block": "component", "member": "releases"},
        fig("optimisation points", "points_optimisation", "ask", sentence="source optimisation"),
        fig("turnover points", "points_turnover", "ask", sentence="source turnover"),
        fig("releases points", "points_releases", "ask", sentence="source releases"),
        fig("labels points", "points_labels", "ask", sentence="forced sources"),
        fig("retunes points", "points_retunes", "ask", sentence="forced sources"),
        fig("Q1 combined model-side RMS", "tot_q1", "ask", sentence="combined q1"),
        fig("Q2 combined model-side RMS", "tot_q2", "ask", sentence="combined q2"),
        fig("Q3 combined model-side RMS", "tot_q3", "ask", sentence="combined q3"),
        fig("Q4 combined model-side RMS", "tot_q4", "ask", sentence="combined q4"),
        fig("2027 combined model-side RMS", "tot_yr", "ask", sentence="combined year"),
        fig("pinned views share", "cc_pin", "ask", sentence="pinned share"),
    ]

    fals = {
        "check": "sum of absolute 2026 internal-record variance discrepancies (points^2): 1-week warm panel "
                 "variance D_warm(1), high-vs-low recent-volume bootstrap net-variance contrast, and same-group "
                 "release-shadow cross-release merchant covariance",
        "observes_target": False,
        "truth": 0.0,
        "golden": gold["fals_err"],
        "rivals": {
            "S1 linear carry": lat_eval["S1"]["fals_err"],
            "S2 uniform window": lat_eval["S2"]["fals_err"],
            "S3 orthogonal releases": lat_eval["S3"]["fals_err"],
            "rigorous (Response 1)": routes["rigorous"]["fals_err"],
            "direct": routes["direct"]["fals_err"],
        },
    }

    spec = {
        "task": "task9", "call": "lines", "members": members,
        "stumps": {
            "S1": {"axis": "what", "opens": "optimisation", "steps_left": 4, "precedents": ["L39", "L65", "N34"],
                   "said_out_loud": "Warm-started refit noise decays from refit to refit rather than accumulating "
                                    "linearly across thirteen weekly refits.",
                   "sides": {"over": over["S1"]["points"]}},
            "S2": {"axis": "when", "opens": "turnover", "steps_left": 4, "precedents": ["L28", "L22", "N21"],
                   "said_out_loud": "The 52-week and 104-week training windows apply exponential recency weighting "
                                    "whose decay rate is identified from seasonal swings in 2026 bootstrap variances.",
                   "sides": {"over": over["S2"]["points"]}},
            "S3": {"axis": "unit", "opens": "releases", "steps_left": 4, "precedents": ["L58", "L28"],
                   "said_out_loud": "Sequential feature releases modifying the same feature group move the same "
                                    "merchants in the same direction, adding positive cross-release covariance.",
                   "sides": {"over": over["S3"]["points"]}},
        },
        "lattice": lattice,
        "falsification": fals,
        "run_routes": dict({r: routes[r]["points"] for r in ("generous", "calibrated", "hedge", "cutoff")},
                           **{k: v["points"] for k, v in extra.items()}),
        "figures": figures,
    }

    if detail:
        np.set_printoptions(precision=3, suppress=True, linewidth=160)
        print("truth points     ", {s: round(tpoints[s], 2) for s in SOURCES})
        print("golden points    ", {s: round(gold["points"][s], 2) for s in SOURCES},
              f"| Q1-Q4={[round(x, 2) for x in gold['tot_q']]} yr={gold['tot_yr']:.2f} pin={gold['cc_pin']:.1f}%")
        print(f"cold-start check  min_len={w['warm']['eff'].min()}, curvature mean={np.mean(pk.cold_curv):+.3f}, "
              f"range=[{min(pk.cold_curv):+.3f}, {max(pk.cold_curv):+.3f}]")
        print(f"S3 2026 corr      same={np.mean(inst['rel_coh_same_pairs']):.3f} (min={min(inst['rel_coh_same_pairs']):.3f}, "
              f"n={len(inst['rel_coh_same_pairs'])}), diff={np.mean(inst['rel_coh_diff_pairs']):.3f}")
        print(f"falsification 26  D1={pk.obs_d1:.2f} (gold {gold['pred_d1']:.2f}), "
              f"boot_c={pk.obs_boot_contrast:.2f} (gold {gold['pred_bc']:.2f}), "
              f"rel_cov={pk.obs_rel_cov:.2f} (gold {gold['pred_rc']:.2f})")
        print(f"unanchored fit    opt={free['points']['optimisation']:.2f}, "
              f"implied rep={float(wt @ (free['A'] * (1 - free['phi'] ** 2))):.2f} vs actual {float(wt @ inst['rep']):.2f}")
        for s_ in SOURCES:
            lo, hi = math.sqrt(0.8 * gold["agg"][s_]), math.sqrt(1.2 * gold["agg"][s_])
            print(f"forcing {s_:13s} -20%={lo:.2f} +20%={hi:.2f} band_held="
                  f"{sum(1 for l in LINES if lo >= l) == gold['band'][s_] == sum(1 for l in LINES if hi >= l)}")

    return {
        "spec": spec, "gold": gold, "fam": fam, "variants": variants, "free": free,
        "lattice": lat_eval, "routes": routes, "extra": extra, "over": over, "fals": fals,
    }


def main():
    detail = "--detail" in sys.argv
    w, z, inst = world()
    pk = Pack(w, z, inst)
    A = analyse(pk, truth_of(w), detail)
    return corelib.run(A["spec"])


if __name__ == "__main__":
    sys.exit(main())
