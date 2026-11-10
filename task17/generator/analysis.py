"""The analysis, on the clean tables only (tables.Pack): the Q3 2026 record (R1), the use of grants and the burst
index (R2), the run-time families under censoring with the 24 to 48 hour validation (R3), the outage record and its
process (R4), the rework after node failures (R5), and the simulation of the partition under the filed scheduling
policy: the backtest on Q3 2026 (R6) and the 2027 cap (R7). Options switch each input to its hurried form for the
routes (passes.py). Nothing here reads the generator's truth."""
import datetime as dt
import math
import multiprocessing as mp
import os
import re

import numpy as np
import pandas as pd
from scipy import optimize, special, stats

import des
import params as P
import sim
import tables as T

N_NODES = P.N_NODES
NORMAL_CHANGE_H = sim.hrs(P.QOS_NORMAL_24_UNTIL)
GRID = np.exp(np.linspace(np.log(0.005), np.log(6000.0), 1400))


def H(y, m=1, d=1):
    return sim.hrs(dt.datetime(y, m, d, tzinfo=P.TZ))


def quarter(y, q):
    return H(y, 3 * (q - 1) + 1), H(y + (q == 4), (3 * q) % 12 + 1)


def limit_at(pk, h):
    lim = pk.limits["normal"][0][1]
    for from_h, l in pk.limits["normal"]:
        if h >= from_h:
            lim = l
    return lim


def limits_vec(pk, hs):
    out = np.full(len(hs), pk.limits["normal"][0][1])
    for from_h, l in pk.limits["normal"]:
        out = np.where(hs >= from_h, l, out)
    return out


# ================================================================ R1: the Q3 2026 record
def assembly(pk, y=2026, q=3):
    a, b = quarter(y, q)
    j = pk.jobs
    m = (j["elig_h"].values >= a) & (j["elig_h"].values < b) & (j["state"].values != "CANCELLED") & ~np.isnan(j["start_h"].values)
    n_jobs = int(m.sum())
    nh = float(j["nh"].values[m].sum())
    deliv = T.delivered(pk, a, b)
    rep = pk.report["quarterly"]
    rep_row = rep[rep["quarter"] == "%d Q%d" % (y, q)].iloc[0]
    # the hurried counts: every row a job (segments and the re-run month), and ids merged across the counter's wrap
    seg = pk.seg
    sm = (seg["start_h"].values >= a) & (seg["start_h"].values < b)
    return {"jobs": n_jobs, "nh": nh, "delivered": deliv, "report_delivered": float(rep_row["delivered_nh"]),
            "report_p90": float(rep_row["p90_wait_h"]), "segments_started": int(sm.sum()),
            "jobs_by_submit": int(((j["submit_h"].values >= a) & (j["submit_h"].values < b) & m).sum())}


# ================================================================ R2: the use of grants, the burst index
def use_by_project_year(pk):
    j = pk.jobs
    rows = []
    for _, g in pk.grants.iterrows():
        a, b = H(int(g["year"])), H(int(g["year"]) + 1)
        m = (j["account"].values == g["project"]) & (j["elig_h"].values >= a) & (j["elig_h"].values < b)
        rows.append({"project": g["project"], "year": int(g["year"]), "category": g["category"],
                     "new": int(g["year"]) == int(g["first_year"]), "granted": float(g["granted"]),
                     "used": float(j["nh"].values[m].sum())})
    return pd.DataFrame(rows)


def use_ratios(pk, years=(2024, 2025), rng=None):
    u = use_by_project_year(pk)
    u = u[u["year"].isin(years)]
    if rng is not None:
        u = u.iloc[rng.integers(0, len(u), size=len(u))]
    r_new = u[u["new"]]["used"].sum() / u[u["new"]]["granted"].sum()
    r_cont = u[~u["new"]]["used"].sum() / u[~u["new"]]["granted"].sum()
    pooled = u["used"].sum() / u["granted"].sum()
    bycat = {}
    for c in sorted(u["category"].unique()):
        for new in (True, False):
            s = u[(u["category"] == c) & (u["new"] == new)]
            bycat[(c, new)] = s["used"].sum() / s["granted"].sum() if s["granted"].sum() > 0 else (r_new if new else r_cont)
    mean_ratio = {"new": u[u["new"]].eval("used/granted").mean(), "cont": u[~u["new"]].eval("used/granted").mean()}
    return {"new": r_new, "cont": r_cont, "pooled": pooled, "bycat": bycat, "mean_ratio": mean_ratio,
            "n_new": int(u["new"].sum()), "n_cont": int((~u["new"]).sum())}


def expected_use(pk, ratios, T=None, how="age"):
    rq = pk.requests
    tot = rq["requested"].sum()
    scale = 1.0 if T is None else T / tot
    if how == "age":
        r = np.where(rq["new"].values, ratios["new"], ratios["cont"])
    elif how == "pooled":
        r = np.full(len(rq), ratios["pooled"])
    elif how == "grant":
        r = np.ones(len(rq))
    elif how == "bycat":
        r = np.array([ratios["bycat"][(c, bool(n))] for c, n in zip(rq["category"], rq["new"])])
    else:
        raise ValueError(how)
    return float((rq["requested"].values * scale * r).sum())


def burst_index(pk, a=None, b=None, clock="utc", population="submitted"):
    a = H(2026, 1, 1) if a is None else a
    b = H(2026, 7, 1) if b is None else b
    j = pk.jobs
    sub = j["submit_h"].values
    if population == "ran":
        sel = ~np.isnan(j["start_h"].values)
    else:
        sel = np.ones(len(j), dtype=bool)
    sub = sub[sel & (sub >= a) & (sub < b)]
    if clock == "local":
        # bins on the local hour: shift each stamp by its offset
        off = np.array([sim.local(h).utcoffset().total_seconds() / 3600.0 for h in np.floor(sub)])
        sub = sub + off
        a_, b_ = a + off.min(), b + off.max()
    n_h = int(math.ceil(b - a))
    cnt = np.bincount(np.clip((sub - a).astype(int), 0, n_h - 1), minlength=n_h)
    how, _ = sim.hour_of_week_local(a + np.arange(n_h) + 0.5)
    if clock == "local":
        how = (np.arange(n_h) + int(round(sim.local(a).weekday() * 24 + sim.local(a).hour))) % 168
    m = np.zeros(168)
    for k in range(168):
        m[k] = cnt[how == k].mean()
    return float(((cnt - m[how]) ** 2).sum() / m[how].sum()), float(cnt.var() / cnt.mean())


# ================================================================ sessions
STEM = re.compile(r"(_(r|fix))?(_\d+)?$")


def stem_of(name):
    return STEM.sub("", name)


def sessions(pk, until_h, gap_h=0.5):
    """jobs grouped into sessions: the same account, user and name stem, submitted within gap_h of each other"""
    j = pk.jobs
    j = j[(j["submit_h"] < until_h)].copy()
    j["stem"] = [stem_of(n) for n in j["name"].values]
    j = j.sort_values(["account", "user", "stem", "submit_h"])
    key = (j["account"] + "|" + j["user"] + "|" + j["stem"]).values
    sub = j["submit_h"].values
    new = np.ones(len(j), dtype=bool)
    new[1:] = (key[1:] != key[:-1]) | ((sub[1:] - sub[:-1]) > gap_h)
    j["session"] = np.cumsum(new)
    return j


def session_records(js, pk, limit_fn):
    """one record per session with its jobs' attributes as arrays (the forward model resamples these)"""
    out = {}
    js = js.sort_values(["session", "submit_h"])
    st = js["state"].values
    elapsed = js["elapsed_h"].values
    wall = js["wall_h"].values
    sub = js["submit_h"].values
    elig = js["elig_h"].values
    lim = limits_vec(pk, sub)
    groups = limit_groups(pk)
    keys = js["account"].values + "|" + js["stem"].values
    maxreq = (js["qos"].values == "normal") & np.array([k in groups for k in keys])
    censored = st == "TIMEOUT"
    ran = ~np.isnan(js["start_h"].values) & np.isin(st, ["COMPLETED", "TIMEOUT", "FAILED", "CANCELLED", "NODE_FAIL"])
    endcode = np.where(st == "FAILED", 2, np.where(st == "CANCELLED", 3, 0))
    how = sim.hour_of_week_local(sub)[0]
    for sid, idx in js.groupby("session").indices.items():
        if not ran[idx].any():
            continue
        k = idx[ran[idx]]
        rec = {"account": js["account"].values[k[0]], "k": len(k), "how": int(how[k[0]]), "stems": js["stem"].values[k],
               "gap": sub[k] - sub[k[0]], "nodes": js["nodes"].values[k].astype(np.int32),
               "qos": js["qos"].values[k], "wall": wall[k], "maxreq": maxreq[k], "elapsed": elapsed[k],
               "censored": censored[k], "endcode": endcode[k].astype(np.int32),
               "chain": bool((elig[k] - sub[k] > 0.01).any()), "nh": float((elapsed[k] * js["nodes"].values[k]).sum()),
               "submit": float(sub[k[0]])}
        out[sid] = rec
    return out


# ================================================================ R3: run-time families
FAMILIES = ["weibull", "lognormal", "loglogistic", "gengamma", "lognormal_mix", "loglogistic_mix", "weibull_mix"]


KINDS = [("train", ("train", "pretrain", "run_lr")), ("finetune", ("ft_", "finetune", "lora", "sft")),
         ("md", ("md_", "gromacs", "namd", "lammps")), ("cfd", ("cfd", "les_", "openfoam", "dns_", "channel"))]


def kind_of(stem):
    s = stem.lower()
    for k, keys in KINDS:
        if any(s.startswith(x) or ("_" + x) in s for x in keys):
            return k
    return "other"


def kind_index(stems):
    names = [k for k, _ in KINDS] + ["other"]
    return np.array([names.index(kind_of(st)) for st in stems])


def limit_groups(pk):
    """(account, stem) groups of normal jobs that requested the limit in force in at least nine jobs of ten"""
    j = pk.jobs[pk.jobs["qos"] == "normal"]
    lim = limits_vec(pk, j["submit_h"].values)
    at_max = np.abs(j["wall_h"].values - lim) < 1e-6
    key = j["account"].values + "|" + np.array([stem_of(n) for n in j["name"].values])
    df = pd.DataFrame({"key": key, "at_max": at_max})
    share = df.groupby("key")["at_max"].mean()
    return set(share[share >= 0.9].index)


def duration_data(pk, until_h, include_requeued=False, elapsed_how="sum", groups=None, strata="kind"):
    j = pk.jobs
    m = (j["qos"].values == "normal") & np.isin(j["state"].values, ["COMPLETED", "TIMEOUT"]) & (j["submit_h"].values < until_h)
    if not include_requeued:
        m &= j["restarts"].values == 0
    d = j[m]
    groups = limit_groups(pk) if groups is None else groups
    keys = d["account"].values + "|" + np.array([stem_of(n) for n in d["name"].values])
    t = d["elapsed_h"].values.copy()
    if elapsed_how == "last" and include_requeued:
        last = pk.seg.groupby(["jobid", "epoch"])["elapsed_h"].last()
        t = np.array([last.get((a, b), x) for a, b, x in zip(d["jobid"], d["epoch"], t)])
    cens = d["state"].values == "TIMEOUT"
    t = np.where(cens, d["wall_h"].values, t)
    t = np.maximum(t, 0.005)
    maxreq = np.array([k in groups for k in keys])
    nodes = d["nodes"].values
    stems = np.array([stem_of(n) for n in d["name"].values])
    cls = class_index(nodes, maxreq, stems, strata)
    return {"t": t, "cens": cens, "cls": cls.astype(int), "nodes": nodes, "maxreq": maxreq, "submit": d["submit_h"].values,
            "wall": d["wall_h"].values, "stems": stems, "strata": strata}


def class_index(nodes, maxreq, stems, strata="kind"):
    """the AFT's strata: by job kind (from the name), node count and whether the group requests the limit"""
    ng = np.searchsorted(np.array([1, 2, 4, 8]), nodes)
    if strata == "nodes":
        return ng * 2 + maxreq.astype(int)
    if strata == "kind":
        return (kind_index(stems) * 4 + ng) * 2 + maxreq.astype(int)
    if strata == "kindonly":
        return kind_index(stems) * 2 + maxreq.astype(int)
    raise ValueError(strata)


def n_classes(strata="kind"):
    return {"nodes": 8, "kind": 40, "kindonly": 10}[strata]


def _logS_logf(family, z, sigma, extra):
    """log survival and log density of log T = mu + sigma eps at standardised z, as functions of z"""
    if family == "weibull":
        logS = -np.exp(z)
        logf = z - np.exp(z)
    elif family == "lognormal":
        logS = stats.norm.logsf(z)
        logf = stats.norm.logpdf(z)
    elif family == "loglogistic":
        logS = -np.logaddexp(0.0, z)
        logf = z - 2.0 * np.logaddexp(0.0, z)
    else:
        raise ValueError(family)
    return logS, logf


def _mix_logS_logf(kernel, z, sigma, extra):
    """two-component mixture on the log scale: eps ~ pi K(0,1) + (1-pi) K(delta, s2)"""
    pi = 1.0 / (1.0 + np.exp(-extra[0]))
    delta, s2 = extra[1], np.exp(extra[2])
    lS1, lf1 = _logS_logf(kernel, z, 1.0, None)
    z2 = (z - delta) / s2
    lS2, lf2 = _logS_logf(kernel, z2, 1.0, None)
    logS = np.logaddexp(np.log(pi) + lS1, np.log(1 - pi) + lS2)
    logf = np.logaddexp(np.log(pi) + lf1, np.log(1 - pi) + lf2 - np.log(s2))
    return logS, logf


def _gg(t, mu, k, c):
    """generalised gamma (Stacy): scale exp(mu), shapes k and c; log survival and log density"""
    x = np.exp(c * (np.log(t) - mu))
    logS = np.log(np.maximum(special.gammaincc(k, x), 1e-300))
    logf = np.log(c) - mu - special.gammaln(k) + (c * k - 1.0) * (np.log(t) - mu) - x
    return logS, logf


def family_logS(family, t, mu, sigma, extra):
    z = (np.log(t) - mu) / sigma
    if family in ("weibull", "lognormal", "loglogistic"):
        return _logS_logf(family, z, sigma, extra)[0]
    if family == "gengamma":
        k, c = np.exp(extra[0]), np.exp(extra[1])
        return _gg(t, mu, k, c)[0]
    kern = family.split("_")[0]
    return _mix_logS_logf(kern, z, sigma, extra)[0]


def family_loglik(family, theta, data, n_cls=8):
    mu_c = theta[:n_cls]
    sigma = np.exp(theta[n_cls])
    extra = theta[n_cls + 1:]
    t, cens, cls = data["t"], data["cens"], data["cls"]
    mu = mu_c[cls]
    if family == "gengamma":
        k, c = np.exp(extra[0]), np.exp(extra[1])
        logS, logf = _gg(t, mu, k, c)
        ll = np.where(cens, logS, logf)
    else:
        z = (np.log(t) - mu) / sigma
        if family in ("weibull", "lognormal", "loglogistic"):
            logS, logf = _logS_logf(family, z, sigma, extra)
        else:
            logS, logf = _mix_logS_logf(family.split("_")[0], z, sigma, extra)
        ll = np.where(cens, logS, logf - np.log(sigma) - np.log(t))
    return float(np.sum(ll))


def n_params(family, n_cls=8):
    if family == "gengamma":
        return n_cls + 3
    if family.endswith("_mix"):
        return n_cls + 4
    return n_cls + 1


def fit_family(family, data, n_cls=None, theta0=None):
    n_cls = n_cls or n_classes(data.get("strata", "kind"))
    """maximum likelihood of the family's AFT model with a shift per class (node count x whether the job requested
    the limit) and a common shape; aggregated over distinct (t, cens, cls) rows for speed"""
    key = pd.DataFrame({"t": np.round(data["t"], 2), "cens": data["cens"], "cls": data["cls"]})
    g = key.groupby(["t", "cens", "cls"]).size().reset_index(name="w")
    agg = {"t": np.maximum(g["t"].values, 0.005), "cens": g["cens"].values, "cls": g["cls"].values}
    w = g["w"].values.astype(float)
    import hashlib, json
    hkey = hashlib.sha256(("%s|%d|" % (family, n_cls)).encode() + np.ascontiguousarray(agg["t"]).tobytes()
                          + np.ascontiguousarray(agg["cens"]).tobytes() + np.ascontiguousarray(agg["cls"]).tobytes()
                          + w.tobytes()).hexdigest()[:24]
    cdir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache")
    os.makedirs(cdir, exist_ok=True)
    cpath = os.path.join(cdir, "fit_%s.json" % hkey)
    if os.path.exists(cpath):
        c = json.load(open(cpath))
        c["theta"] = np.array(c["theta"])
        return c

    def nll(theta):
        mu_c = theta[:n_cls]
        sigma = np.exp(theta[n_cls])
        extra = theta[n_cls + 1:]
        mu = mu_c[agg["cls"]]
        t = agg["t"]
        if family == "gengamma":
            k, c = np.exp(extra[0]), np.exp(extra[1])
            if k > 400 or c > 60:
                return 1e12
            logS, logf = _gg(t, mu, k, c)
            ll = np.where(agg["cens"], logS, logf)
        else:
            z = (np.log(t) - mu) / sigma
            if family in ("weibull", "lognormal", "loglogistic"):
                logS, logf = _logS_logf(family, z, sigma, extra)
            else:
                logS, logf = _mix_logS_logf(family.split("_")[0], z, sigma, extra)
            ll = np.where(agg["cens"], logS, logf - np.log(sigma) - np.log(t))
        v = -float(np.sum(w * ll))
        return v if np.isfinite(v) else 1e12

    if theta0 is None:
        lt = np.log(data["t"])
        mu0 = np.array([np.median(lt[data["cls"] == c]) if (data["cls"] == c).any() else np.median(lt) for c in range(n_cls)])
        # empty classes keep their start value (no data moves them)
        theta0 = np.concatenate([mu0, [np.log(max(lt.std(), 0.3))]])
        if family == "gengamma":
            theta0 = np.concatenate([theta0, [0.0, 0.0]])
        elif family.endswith("_mix"):
            theta0 = np.concatenate([theta0, [0.0, 1.0, 0.0]])
    best = None
    starts = [theta0]
    if family.endswith("_mix"):
        starts.append(np.concatenate([theta0[:n_cls + 1], [1.0, 1.5, -0.3]]))
        starts.append(np.concatenate([theta0[:n_cls + 1], [-0.5, -1.0, 0.3]]))
    if family == "gengamma":
        starts.append(np.concatenate([theta0[:n_cls + 1], [0.7, -0.5]]))
    for s0 in starts:
        r = optimize.minimize(nll, s0, method="L-BFGS-B", options={"maxiter": 2000})
        if best is None or r.fun < best.fun:
            best = r
    ll = -best.fun
    k = n_params(family, n_cls)
    out = {"family": family, "theta": best.x, "loglik": ll, "aic": 2 * k - 2 * ll, "n": len(data["t"]), "n_cls": n_cls}
    json.dump({**out, "theta": [float(x) for x in best.x]}, open(cpath, "w"))
    return out


def surv_grid(fit, cls):
    th = fit["theta"]
    n_cls = fit["n_cls"]
    mu = th[cls]
    return np.exp(family_logS(fit["family"], GRID, mu, np.exp(th[n_cls]), th[n_cls + 1:]))


def tail_moments(fit, cls, L=96.0, c=48.0):
    """E[min(D, L)] and E[(min(D, L) - c)+] for one class"""
    S = surv_grid(fit, cls)
    g = GRID
    m = g <= L
    x = np.concatenate([[0.0], g[m], [L]])
    y = np.concatenate([[1.0], S[m], [np.interp(L, g, S)]])
    e_min = float(np.trapezoid(y, x))
    m2 = (g >= c) & (g <= L)
    x2 = np.concatenate([[c], g[m2], [L]])
    y2 = np.concatenate([[np.interp(c, g, S)], S[m2], [np.interp(L, g, S)]])
    e_tail = float(np.trapezoid(y2, x2))
    return e_min, e_tail


def r3_figures(fit, mix_cls, mix_nodes, L=96.0, c=48.0):
    """the mean run time under the limit L over the class mix (jobs weighted) and the share of work beyond c"""
    tot_j, tot_mean, tot_work, tot_tail = 0.0, 0.0, 0.0, 0.0
    for cls, n_jobs, nodes in zip(*mix_cls):
        e_min, e_tail = tail_moments(fit, cls, L, c)
        tot_j += n_jobs
        tot_mean += n_jobs * e_min
        tot_work += n_jobs * nodes * e_min
        tot_tail += n_jobs * nodes * e_tail
    return tot_mean / tot_j, tot_tail / tot_work


def class_mix(data):
    """jobs per class and the mean nodes per class, over the 2026 record"""
    m = data["submit"] >= H(2026)
    cls = data["cls"][m]
    nodes = data["nodes"][m]
    cs = sorted(set(cls))
    return ([c for c in cs], [int((cls == c).sum()) for c in cs], [float(nodes[cls == c].mean()) for c in cs])


def validate_24_48(pk, family, until_h=None, strata="kind"):
    """fit on the jobs submitted before the limit's change (censored at 24 hours or their own limit); among the
    limit-requesting groups' jobs after the change (limit 48 hours) that ran beyond 24 hours, compare the shape the
    family predicts for the 24 to 48 hour window with what ran: the mean run time within the window and the share
    that reached the 48 hour limit, each as a z-score against the observed value's sampling error"""
    groups = limit_groups(pk)
    d_pre = duration_data(pk, NORMAL_CHANGE_H, groups=groups, strata=strata)
    fit = fit_family(family, d_pre)
    d_all = duration_data(pk, until_h or pk.cut_h, groups=groups, strata=strata)
    post = (d_all["submit"] >= NORMAL_CHANGE_H) & d_all["maxreq"] & (d_all["wall"] >= 47.9)
    cls = d_all["cls"][post]
    t = d_all["t"][post]
    cens = d_all["cens"][post]
    beyond = t > 24.0
    nb = int(beyond.sum())
    obs_mass = float(beyond.mean())
    obs_excess = float((np.minimum(t[beyond], 48.0) - 24.0).mean())
    obs_s48 = float(cens[beyond].mean())
    S24 = np.zeros(len(t)); S48 = np.zeros(len(t)); ex = np.zeros(len(t))
    for c in sorted(set(cls)):
        m = cls == c
        S = surv_grid(fit, int(c))
        s24, s48 = np.interp(24.0, GRID, S), np.interp(48.0, GRID, S)
        gm = (GRID >= 24) & (GRID <= 48)
        x = np.concatenate([[24.0], GRID[gm], [48.0]])
        y = np.concatenate([[s24], S[gm], [s48]])
        S24[m], S48[m], ex[m] = s24, s48, float(np.trapezoid(y, x))
    pred_mass = float(S24.mean())
    pred_excess = float(ex.sum() / S24.sum())
    pred_s48 = float(S48.sum() / S24.sum())
    se_ex = float((np.minimum(t[beyond], 48.0) - 24.0).std() / math.sqrt(max(nb, 1)))
    se_s48 = math.sqrt(max(obs_s48 * (1 - obs_s48), 1e-9) / max(nb, 1))
    se_mass = math.sqrt(max(obs_mass * (1 - obs_mass), 1e-9) / max(len(t), 1))
    return {"family": family, "n": int(len(cls)), "n_beyond": nb,
            "observed": obs_mass, "predicted": pred_mass, "se": se_mass, "z_mass": (pred_mass - obs_mass) / se_mass,
            "excess_obs": obs_excess, "excess_pred": pred_excess, "z_excess": (pred_excess - obs_excess) / se_ex,
            "s48_obs": obs_s48, "s48_pred": pred_s48, "z_s48": (pred_s48 - obs_s48) / se_s48,
            "z": max(abs((pred_excess - obs_excess) / se_ex), abs((pred_s48 - obs_s48) / se_s48)), "fit_pre": fit}


def r3(pk, until_h=None, families=FAMILIES, z_pass=3.0, strata="kind"):
    until_h = until_h or pk.cut_h
    data = duration_data(pk, until_h, strata=strata)
    mix = class_mix(data)
    out = {}
    for fam in families:
        v = validate_24_48(pk, fam, until_h, strata=strata)
        fit = fit_family(fam, data)
        mean96, share48 = r3_figures(fit, mix, None)
        mean48, _ = r3_figures(fit, mix, None, L=48.0)
        out[fam] = {"fit": fit, "validation": {k: v[k] for k in v if k != "fit_pre"},
                    "passes": abs(v["z"]) <= z_pass, "mean96": mean96, "share48": share48, "mean48": mean48,
                    "aic": fit["aic"]}
    # the empirical "no tail" route: the record's durations cut at 48 (2026 jobs, censored ones at their limit)
    m = data["submit"] >= H(2026)
    t48 = np.minimum(data["t"][m], 48.0)
    out["_cut48"] = {"mean96": float(t48.mean()), "share48": 0.0}
    return {"families": out, "mix": mix, "data_n": int(len(data["t"])), "strata": strata}


def choose_family(r3res):
    """the passing family with the best-supported fit (highest likelihood among those that pass the validation)"""
    fams = {k: v for k, v in r3res["families"].items() if not k.startswith("_") and v["passes"]}
    if not fams:
        allf = {k: v for k, v in r3res["families"].items() if not k.startswith("_")}
        return min(allf, key=lambda k: abs(allf[k]["validation"]["z"]))
    return min(fams, key=lambda k: fams[k]["aic"])


# ================================================================ R4: the outage record and its process
KW = {
    "hardware": ["rma", "replac", "swap", "getauscht", "dimm", "psu", "netzteil", "hca", "nvme", "mainboard", "fan",
                 "awaiting", "pending", "ecc"],
    "rack": ["switch", "leaf", "ib ", "pdu", "strom", "tripped", "trip", "sw-r"],
    "admin": ["drain", "reserved"],
    "maint": ["maintenance", "wartung", "pm window"],
    "software": ["xid", "reboot", "hang", "panic", "driver", "nvlink", "nhc", "slurmd", "neustart", "power cycled", "haengt"],
}


def classify_reason(txt):
    s = txt.lower()
    for cls in ("maint", "admin", "rack", "hardware", "software"):
        if any(k in s for k in KW[cls]):
            return cls
    return "unknown"


def intervals(pk, rejoin=True):
    """node outage intervals: rows cut by a scheduler restart (the same node and reason, the end of one row the
    start of the next) rejoined; 'Not responding' rows classed as rack events when three or more nodes of the rack
    went down within ten minutes, as software otherwise"""
    ev = pk.events.copy()
    ev["end_f"] = ev["end_h"].fillna(pk.cut_h)
    ev = ev.sort_values(["node", "start_h"]).reset_index(drop=True)
    if rejoin:
        keep = []
        cur = None
        for r in ev.to_dict("records"):
            if cur is not None and r["node"] == cur["node"] and r["reason"] == cur["reason"] and \
                    abs(r["start_h"] - cur["end_f"]) < 1.0 / 60.0 + 1e-9:
                cur["end_f"] = r["end_f"]
                cur["end_h"] = r["end_h"]
                continue
            if cur is not None:
                keep.append(cur)
            cur = dict(r)
        keep.append(cur)
        ev = pd.DataFrame(keep)
    ev["cls"] = [classify_reason(t) for t in ev["reason"].values]
    ev["rack"] = pk.rack["rack"].values[ev["node"].values]
    # 'Not responding' and other unknown rows: rack events when the rack went down together
    unk = ev["cls"].isin(["unknown", "software"]) & ev["reason"].str.lower().str.contains("not responding")
    starts = ev["start_h"].values
    racks = ev["rack"].values
    cls = ev["cls"].values.copy()
    for i in np.where(unk)[0]:
        same = (racks == racks[i]) & (np.abs(starts - starts[i]) <= 10.0 / 60.0)
        cls[i] = "rack" if same.sum() >= 3 else "software"
    cls[cls == "unknown"] = "software"
    ev["cls"] = cls
    ev["hours"] = ev["end_f"] - ev["start_h"]
    return ev.reset_index(drop=True)


def outage_record(pk, ev, year=2026):
    """node-days lost per quarter outside maintenance windows, the share lost while four or more nodes of a rack
    were down together, and the median repair time by class"""
    un = ev[~ev["cls"].isin(["maint"])]
    out = {"quarters": {}}
    for q in (1, 2, 3, 4):
        a, b = quarter(year, q)
        b = min(b, pk.cut_h)
        if a >= pk.cut_h:
            continue
        s, e = un["start_h"].values, un["end_f"].values
        ov = np.clip(np.minimum(e, b) - np.maximum(s, a), 0.0, None)
        for ms, me in zip(pk.maint["start_h"].values, pk.maint["end_h"].values):
            lo, hi = max(a, ms), min(b, me)
            if hi > lo:
                ov -= np.clip(np.minimum(e, hi) - np.maximum(s, lo), 0.0, None)
        out["quarters"][q] = float(ov.sum() / 24.0)
    # the share in four-or-more-node rack events: lost node-time while the node's rack had >= 4 nodes down
    a, b = H(year), min(H(year + 1), pk.cut_h)
    s, e = un["start_h"].values, un["end_f"].values
    racks = un["rack"].values
    tot, multi = 0.0, 0.0
    for r in sorted(set(racks)):
        m = racks == r
        pts = np.unique(np.concatenate([np.clip(s[m], a, b), np.clip(e[m], a, b), [a, b]]))
        for lo, hi in zip(pts[:-1], pts[1:]):
            if hi <= lo:
                continue
            mid = 0.5 * (lo + hi)
            down = ((s[m] <= mid) & (e[m] > mid)).sum()
            in_m = any(ms <= mid < me for ms, me in zip(pk.maint["start_h"].values, pk.maint["end_h"].values))
            if in_m:
                continue
            tot += down * (hi - lo)
            if down >= 4:
                multi += down * (hi - lo)
    out["share_multi"] = multi / tot if tot else 0.0
    y = un[(un["start_h"] >= H(2024)) & (un["start_h"] < pk.cut_h) & un["end_h"].notna()]
    out["median_software_h"] = float(y[y["cls"] == "software"]["hours"].median())
    out["median_hardware_d"] = float(y[y["cls"] == "hardware"]["hours"].median() / 24.0)
    # rack events: one duration per event (the nodes' longest interval)
    rk = y[y["cls"] == "rack"].copy()
    rk["ev"] = (rk["rack"].astype(str) + "|" + (rk["start_h"] // 0.5).astype(int).astype(str))
    out["median_rack_h"] = float(rk.groupby("ev")["hours"].max().median())
    out["n_rack_events"] = int(rk["ev"].nunique())
    out["counts"] = y["cls"].value_counts().to_dict()
    return out


UPTIME_BINS = np.array([0.0, 48.0, 120.0, 240.0, 360.0, 480.0, 720.0, 960.0, 1e9])


def outage_process(pk, ev, until_h):
    """the fleet's failure process: a software hazard by uptime since the node's last reset (every interval's end
    and every maintenance end is a reset; a node is not at risk while it is down), a hardware rate per node-hour at
    risk, rack events per rack-year by kind, administrative drains, and repair-time pools by class"""
    ev = ev[ev["start_h"] < until_h]
    nodes = pk.rack
    nb = len(UPTIME_BINS) - 1
    sw_events = np.zeros(nb)
    sw_expo = np.zeros(nb)
    hw_n, expo_total = 0, 0.0
    m_end = pk.maint["end_h"].values
    for node in range(len(nodes)):
        t0 = nodes["in_service_h"].values[node]
        if t0 >= until_h:
            continue
        rows = ev[ev["node"] == node].sort_values("start_h")
        starts = rows["start_h"].values
        ends = np.minimum(rows["end_f"].values, until_h)
        cls = rows["cls"].values
        # up-segments: from each reset to the next interval's start (or the horizon); the first segment of the
        # record has an unknown origin (the log opens on 1 January 2024) and is left out
        rec_open = max(t0, H(2024))
        resets = np.concatenate([ends, m_end[(m_end > t0) & (m_end < until_h)]])
        resets = np.unique(resets[(resets < until_h) & (resets >= rec_open)])
        for a in resets:
            # the node is down at a if some interval covers it
            inside = (starts <= a) & (ends > a)
            if inside.any():
                continue
            nxt = starts[starts > a]
            b = min(nxt[0], until_h) if len(nxt) else until_h
            # the next reset before b ends this up-segment without an event
            later = resets[resets > a]
            if len(later) and later[0] < b:
                b_seg, event = later[0], None
            else:
                b_seg = b
                event = cls[np.where(starts > a)[0][0]] if (len(nxt) and nxt[0] < until_h) else None
            u = b_seg - a
            for kb in range(nb):
                sw_expo[kb] += max(0.0, min(u, UPTIME_BINS[kb + 1]) - UPTIME_BINS[kb])
            expo_total += u
            if event == "software":
                k = np.searchsorted(UPTIME_BINS, u, side="right") - 1
                sw_events[min(max(k, 0), nb - 1)] += 1
            elif event == "hardware":
                hw_n += 1
    hazard = sw_events / np.maximum(sw_expo, 1.0)
    rk = ev[ev["cls"] == "rack"].copy()
    rk["ev"] = (rk["rack"].astype(str) + "|" + (rk["start_h"] // 0.5).astype(int).astype(str))
    events = rk.groupby("ev").agg(n=("node", "nunique"), rack=("rack", "first"), start=("start_h", "min"),
                                  hours=("hours", "max")).reset_index()
    rack_years = sum(max(0.0, until_h - nodes["in_service_h"].values[k * P.NODES_PER_RACK]) for k in range(P.RACKS)) / 8760.0
    switch = events[events["n"] >= 6]
    pdu = events[events["n"] < 6]
    sw_rows = ev[(ev["cls"] == "software") & (ev["start_h"] >= H(2024)) & ev["end_h"].notna()]
    office = np.array([(sim.local(h).weekday() < 5) and (7.5 <= sim.local(h).hour + sim.local(h).minute / 60.0 <= 19.0)
                       for h in sw_rows["start_h"].values])
    adm = ev[(ev["cls"] == "admin") & ev["end_h"].notna()]
    return {"sw_hazard": hazard, "sw_events": sw_events, "sw_expo": sw_expo,
            "hw_rate": hw_n / max(expo_total, 1.0), "hw_n": hw_n, "expo": expo_total,
            "switch_rate": len(switch) / rack_years, "pdu_rate": len(pdu) / rack_years, "rack_years": rack_years,
            "n_switch": len(switch), "n_pdu": len(pdu),
            "repair": {"software_office": sw_rows["hours"].values[office], "software_night": sw_rows["hours"].values[~office],
                       "hardware": ev[(ev["cls"] == "hardware") & ev["end_h"].notna()]["hours"].values,
                       "switch": switch["hours"].values, "pdu": pdu["hours"].values, "admin": adm["hours"].values},
            "admin_rate": len(adm) / max(expo_total, 1.0),
            "mean_availability": 1.0 - lost_share(pk, ev, until_h)}


def lost_share(pk, ev, until_h):
    a, b = H(2024), until_h
    un = ev[ev["cls"] != "maint"]
    lost = np.clip(np.minimum(un["end_f"].values, b) - np.maximum(un["start_h"].values, a), 0, None).sum()
    m = pk.maint
    ml = sum(max(0.0, min(me, b) - max(ms, a)) for ms, me in zip(m["start_h"].values, m["end_h"].values))
    nodes_h = sum(max(0.0, b - max(a, h)) for h in pk.rack["in_service_h"].values)
    return (lost + ml * (nodes_h / (b - a))) / nodes_h


# ================================================================ R5: rework after node failures
def rework(pk, year=2026, like="session", until_h=None):
    """node-hours redone after node failures as a share of the year's node-hours: for each requeued job, its total
    elapsed over every segment less the run time of like jobs (the same session's jobs that ran through), by the
    project's checkpointing"""
    until_h = until_h or pk.cut_h
    a, b = H(year), min(H(year + 1), until_h)
    js = sessions(pk, until_h)
    j = js[(js["elig_h"] >= a) & (js["elig_h"] < b)]
    total_nh = float(j["nh"].sum())
    seg = pk.seg
    killed = seg[seg["state"] == "NODE_FAIL"].groupby(["jobid", "epoch"])["elapsed_h"].sum()
    rq = j[(j["restarts"] > 0) & (j["state"] == "COMPLETED")]
    ref_pool = js[(js["restarts"] == 0) & (js["state"] == "COMPLETED")]
    by_session = ref_pool.groupby(["session", "nodes"])["elapsed_h"].median()
    by_stem = ref_pool.groupby(["account", "stem", "nodes"])["elapsed_h"].median()
    rows = []
    for r in rq.to_dict("records"):
        ref = by_session.get((r["session"], r["nodes"]), np.nan)
        if like != "session" or (isinstance(ref, float) and math.isnan(ref)):
            ref = by_stem.get((r["account"], r["stem"], r["nodes"]), np.nan)
        if isinstance(ref, float) and math.isnan(ref):
            continue
        k = killed.get((r["jobid"], r["epoch"]), 0.0)
        excess = r["elapsed_h"] - ref
        rows.append({"account": r["account"], "jobid": r["jobid"], "nodes": r["nodes"], "excess_h": excess,
                     "killed_h": k, "excess_nh": excess * r["nodes"], "killed_nh": k * r["nodes"],
                     "elapsed": r["elapsed_h"], "ref": ref, "restarts": r["restarts"]})
    d = pd.DataFrame(rows)
    covered = d["excess_nh"].sum()
    # requeued jobs without a reference take the covered jobs' redone share of their killed time
    all_rq = j[j["restarts"] > 0]
    killed_all = sum(killed.get((a_, b_), 0.0) * n for a_, b_, n in zip(all_rq["jobid"], all_rq["epoch"], all_rq["nodes"]))
    frac = covered / d["killed_nh"].sum() if d["killed_nh"].sum() > 0 else 0.0
    redone = frac * killed_all
    share = redone / total_nh
    # by project: the redone fraction of killed time, read as the project's checkpointing
    per = d.groupby("account").agg(excess=("excess_nh", "sum"), killed=("killed_nh", "sum"), n=("jobid", "size"))
    per["frac"] = per["excess"] / per["killed"].replace(0, np.nan)
    return {"share": share, "share_covered_only": covered / total_nh, "frac": frac, "n": int(len(d)),
            "n_requeued": int(len(all_rq)), "total_nh": total_nh, "killed_nh": float(killed_all),
            "whole_segment_share": killed_all / total_nh, "per_project": per, "rows": d}


def checkpoint_classes(rw, pk):
    """each project's checkpointing from its requeued jobs: the work redone after a kill is the killed run time
    (no checkpoint), the part since the last full hour (hourly) or since the last six hours (six-hourly); the
    hypothesis with the smallest total residual over the project's requeues wins. Projects with no requeue on
    record draw from the inferred mix of their category (or the whole mix where the category has few)"""
    rows = rw["rows"]
    cls = {}
    for pid, g in rows.groupby("account"):
        if g["killed_h"].sum() <= 0:
            continue
        e = g["killed_h"].values
        x = g["excess_h"].values
        resid = {0.0: np.abs(x - e).sum(), 1.0: np.abs(x - np.mod(e, 1.0)).sum(), 6.0: np.abs(x - np.mod(e, 6.0)).sum()}
        best = min(resid.values())
        tied = [c for c in (6.0, 1.0, 0.0) if resid[c] <= best + 1e-9]
        cls[pid] = tied[0]
    bycat = {}
    for pid, c in cls.items():
        cat = pk.projects.get(pid, {}).get("category", "FOR")
        bycat.setdefault(cat, []).append(c)
    allc = list(cls.values())
    for cat in list(bycat):
        if len(bycat[cat]) < 12:
            bycat[cat] = allc
    bycat["_all"] = allc
    return cls, bycat


# ================================================================ the forward model
class Fits:
    pass


def monday0(year):
    """hours since T0 of the Monday 00:00 local that starts the week holding 1 January"""
    d = dt.date(year, 1, 1)
    d = d - dt.timedelta(days=d.weekday())
    return sim.hrs(dt.datetime(d.year, d.month, d.day, tzinfo=P.TZ))


def weekly_profile(js, pk, year_from, year_to, until_h=None, opt_nosmooth=False):
    """submitted node-hours by week of year (53 weeks from the Monday of 1 January) for (category, first-year or
    continuing): each year's profile normalised on the weeks the record covers, then averaged over the years"""
    until_h = until_h or pk.cut_h
    j = js[(js["submit_h"] >= H(year_from)) & (js["submit_h"] < min(H(year_to + 1), until_h))].copy()
    yrs = np.array([sim.local(h).year for h in j["submit_h"].values])
    m0 = np.array([monday0(y) for y in yrs])
    wk = np.clip(((j["submit_h"].values - m0) / 168.0).astype(int), 0, 52)
    cat = np.array([pk.projects[a]["category"] for a in j["account"].values])
    fy = np.array([pk.projects[a]["first_year"] for a in j["account"].values])
    new = fy == yrs
    nh = (j["elapsed_h"].values * j["nodes"].values)
    prof = {}
    for c in sorted(set(cat)):
        for isnew in (True, False):
            acc = np.zeros(53)
            cnt = np.zeros(53)
            for y in sorted(set(yrs)):
                m = (cat == c) & (new == isnew) & (yrs == y)
                if m.sum() < 20:
                    continue
                w = np.bincount(wk[m], weights=nh[m], minlength=53)
                covered = np.arange(53) < int((min(until_h, H(y + 1)) - monday0(y)) / 168.0)
                if covered.sum() < 8:
                    continue
                w = w / max(w[covered].sum(), 1e-9) * covered.sum()
                acc[covered] += w[covered]
                cnt[covered] += 1
            w = np.where(cnt > 0, acc / np.maximum(cnt, 1), 0.0) + 1e-3
            # the weekly profile smoothed over five weeks (a triangular kernel): week-level sampling noise is
            # not seasonality, and replaying it would make every simulated year lumpier than the record
            if not opt_nosmooth:
                k = np.array([1.0, 2.0, 3.0, 2.0, 1.0]) / 9.0
                pad = np.concatenate([w[-2:], w, w[:2]])
                w = np.convolve(pad, k, mode="valid")
            prof[(c, isnew)] = w / w.sum()
    return prof


def fit_all(pk, until_h, family=None, options=None):
    """every input of the simulation, fitted on the record to until_h"""
    opt = options or {}
    F = Fits()
    F.until_h = until_h
    F.ratios = use_ratios(pk)
    js = sessions(pk, until_h)
    F.sessions_df = js
    F.sess = session_records(js, pk, limit_at)
    # pools: by project, and by (category, new) for projects without a record
    # the pools the forward model resamples: the sessions of the limit regime in force (since 3 May 2026), the
    # regime 2027 continues from; the full record is used for the profiles, the families and the processes
    F.pool_from = NORMAL_CHANGE_H if not opt.get("pool_all") else 0.0
    F.pool_project = {}
    F.pool_cat = {}
    yr = {sid: sim.local(rec["submit"]).year for sid, rec in F.sess.items()}
    for sid, rec in F.sess.items():
        if rec["submit"] < F.pool_from:
            continue
        F.pool_project.setdefault(rec["account"], []).append(sid)
        pr = pk.projects[rec["account"]]
        F.pool_cat.setdefault((pr["category"], pr["first_year"] == yr[sid]), []).append(sid)
    F.profile = weekly_profile(js, pk, 2024, 2026, until_h, opt_nosmooth=bool(opt.get("nosmooth")))
    r3res = r3(pk, until_h)
    F.r3 = r3res
    F.family = family or choose_family(r3res)
    F.fit = r3res["families"][F.family]["fit"]
    F.fit_weibull = r3res["families"]["weibull"]["fit"]
    # within-session dispersion of run times (completed jobs of sessions with two or more)
    disp = []
    for rec in F.sess.values():
        m = (~rec["censored"]) & (rec["endcode"] == 0)
        if m.sum() >= 2:
            e = rec["elapsed"][m]
            disp.append(np.std(np.log(np.maximum(e, 0.01))))
    F.within_sigma = float(np.median(disp)) if disp else 0.05
    ev = intervals(pk)
    F.events = ev
    F.outage = outage_process(pk, ev, until_h)
    F.outage_record = outage_record(pk, ev)
    rw = rework(pk, until_h=until_h)
    F.rework = rw
    F.ckpt, F.ckpt_bycat = checkpoint_classes(rw, pk)
    return F


def family_params_draw(fit, rng, data_n):
    """the family's parameters redrawn from their large-sample spread (a diagonal normal on the shape parameters
    and the class shifts, scaled by the record's size)"""
    th = fit["theta"].copy()
    n_cls = fit["n_cls"]
    k = len(th)
    sd = np.full(k, 1.0 / math.sqrt(max(data_n, 1)) * 3.0)
    sd[:n_cls] = 2.0 / math.sqrt(max(data_n / n_cls, 1))
    return th + rng.normal(0.0, 1.0, size=k) * sd


def conditional_tail(fit, cls, c, rng, size, theta=None):
    """draws of D given D > c under the family for class cls"""
    f = dict(fit)
    if theta is not None:
        f["theta"] = theta
    S = surv_grid(f, cls)
    Sc = float(np.interp(c, GRID, S))
    u = rng.uniform(0.0, Sc, size=size)
    # S is decreasing: invert on the grid
    idx = np.searchsorted(-S, -u)
    idx = np.clip(idx, 1, len(GRID) - 1)
    t = GRID[idx - 1] + (GRID[idx] - GRID[idx - 1]) * (S[idx - 1] - u) / np.maximum(S[idx - 1] - S[idx], 1e-12)
    return np.maximum(t, c + 1e-3)


def demand_year(F, pk, year, T_total, rng, opt):
    """the jobs of one future year: for each project of the round, sessions resampled from its record (or its
    category's first-year pool) until its expected use is reached, placed by the category's weekly profile and the
    session's own hour of week; censored run times extended by the family's tail; walltime habits carried to the
    limit in force"""
    rq = pk.requests if year == 2027 else None
    if year == 2027:
        tot = rq["requested"].sum()
        projects = [(r["project"], r["requested"] * T_total / tot, bool(r["new"]), r["category"]) for r in rq.to_dict("records")]
    else:
        g = pk.grants[pk.grants["year"] == year]
        projects = [(r["project"], r["granted"], int(r["first_year"]) == year, r["category"]) for r in g.to_dict("records")]
    ratios = F.ratios if not opt.get("ratio_draw") else use_ratios(pk, rng=rng)
    y0, y1 = H(year), H(year + 1)
    horizon = y1 + 24.0 * 35
    lim_year = [(h, l) for h, l in pk.limits["normal"]]
    if opt.get("no_tail"):
        lim_year = [(h, min(l, 48.0)) for h, l in lim_year]
    theta = family_params_draw(F.fit, rng, F.r3["data_n"]) if opt.get("param_draw") else None
    fit = F.fit_weibull if opt.get("weibull") else F.fit
    cols = {k: [] for k in ("submit", "nodes", "wall", "dur", "ckpt", "dep", "endstate", "account")}
    n_so_far = 0
    for pid, grant, new, cat in projects:
        if opt.get("realised") is not None and pid in opt["realised"]:
            r = opt["realised"][pid]
        elif opt.get("ratio_how") == "pooled":
            r = ratios["pooled"]
        elif opt.get("ratio_how") == "grant":
            r = 1.0
        else:
            r = ratios["new"] if new else ratios["cont"]
        U = grant * r * opt.get("u_scale", 1.0)
        pool = F.pool_project.get(pid) if (not new and pid in F.pool_project and len(F.pool_project[pid]) >= 3) else None
        if pool is None:
            pool = F.pool_cat.get((cat, True)) or F.pool_cat.get((cat, False))
        if not pool:
            continue
        pool = np.array(pool)
        prof = F.profile.get((cat, new)) if not opt.get("flat_profile") else None
        mean_nh = np.mean([F.sess[s]["nh"] for s in pool]) + 1e-6
        m = int(U / mean_nh * 1.6) + 6
        picks = rng.choice(pool, size=m)
        if prof is not None:
            weeks = rng.choice(53, size=len(picks), p=prof)
        else:
            weeks = rng.integers(0, 52, size=len(picks))
        m0 = monday0(year)
        ck = F.ckpt.get(pid)
        if opt.get("no_rework"):
            ck = 1e-6
        elif ck is None:
            pool_c = F.ckpt_bycat.get(cat) or F.ckpt_bycat.get("_all") or [0.0, 1.0, 6.0]
            ck = float(rng.choice(pool_c))
        cum = 0.0
        for s_i, sid in enumerate(picks):
            if cum >= U:
                break
            rec = F.sess[sid]
            base = m0 + weeks[s_i] * 168.0 + rec["how"] + rng.uniform(0, 1)
            if opt.get("keep_time"):
                base = rec["submit"]
            if opt.get("poisson"):
                subs = base + rng.uniform(-6.0, 6.0, size=rec["k"])
            else:
                subs = base + rec["gap"]
            subs = np.clip(subs, y0, horizon - 1)
            k = rec["k"]
            lim = np.array([limit_at_list(lim_year, h) for h in subs])
            wall = np.where(rec["maxreq"], lim, np.minimum(rec["wall"], lim))
            if opt.get("no_habit"):
                wall = np.minimum(rec["wall"], lim)
            dur = rec["elapsed"].copy()
            cens = rec["censored"]
            if cens.any() and not opt.get("no_tail"):
                cls_nodes = class_index(rec["nodes"][cens], rec["maxreq"][cens], rec["stems"][cens], F.r3.get("strata", "kind"))
                for c in sorted(set(cls_nodes)):
                    mm = cls_nodes == c
                    dur[np.where(cens)[0][mm]] = conditional_tail(fit, int(c), float(rec["wall"][cens][mm].min()), rng,
                                                                  int(mm.sum()), theta)
            dur = np.maximum(dur * np.exp(rng.normal(0.0, 0.3 * F.within_sigma, size=k)), 0.01)
            dep = np.full(k, -1, dtype=np.int64)
            if rec["chain"] and k > 1:
                dep[1:] = np.arange(k - 1) + n_so_far
            cols["submit"].append(subs); cols["nodes"].append(rec["nodes"]); cols["wall"].append(wall)
            cols["dur"].append(dur); cols["ckpt"].append(np.full(k, ck)); cols["dep"].append(dep)
            cols["endstate"].append(rec["endcode"]); cols["account"].append(np.full(k, pid))
            n_so_far += k
            cum += float((rec["nodes"] * np.minimum(dur, wall)).sum())
    J = {k: np.concatenate(v) for k, v in cols.items()}
    order = np.argsort(J["submit"], kind="stable")
    inv = np.empty(len(order), dtype=np.int64)
    inv[order] = np.arange(len(order))
    dep = J["dep"][order]
    dep = np.where(dep >= 0, inv[np.maximum(dep, 0)], -1)
    n = len(order)
    jobs = {"submit": J["submit"][order].astype(float), "nodes": J["nodes"][order].astype(np.int32),
            "wall": J["wall"][order].astype(float), "dur": J["dur"][order].astype(float),
            "ckpt": J["ckpt"][order].astype(float), "dep": dep.astype(np.int32),
            "after": np.full(n, -1, dtype=np.int32), "after_delay": np.zeros(n), "endstate": J["endstate"][order].astype(np.int32),
            "account": J["account"][order]}
    return jobs


def limit_at_list(lims, h):
    lim = lims[0][1]
    for from_h, l in lims:
        if h >= from_h:
            lim = l
    return lim


def outages_year(F, pk, year, rng, opt):
    """the fleet's outages over one future year from the fitted process"""
    O = F.outage
    y0, y1 = H(year), H(year + 1) + 24.0 * 35
    nodes_n = len(pk.rack)
    m = pk.maint
    msel = (m["start_h"].values >= y0 - 24) & (m["start_h"].values < y1)
    ms, me = m["start_h"].values[msel], m["end_h"].values[msel]
    if opt.get("const_avail"):
        return (np.zeros(0, dtype=np.int32), np.zeros(0), np.zeros(0)), (ms, me)
    draw = opt.get("param_draw", False)
    hz = O["sw_hazard"].copy()
    hw = O["hw_rate"]
    sw_rate, pd_rate = O["switch_rate"], O["pdu_rate"]
    rep = {k: np.asarray(v, dtype=float) for k, v in O["repair"].items()}
    if draw:
        hz = rng.gamma(O["sw_events"] + 0.5, 1.0 / np.maximum(O["sw_expo"], 1.0))
        hw = rng.gamma(O["hw_n"] + 0.5, 1.0 / max(O["expo"], 1.0))
        sw_rate = rng.gamma(O["n_switch"] + 0.5, 1.0 / O["rack_years"])
        pd_rate = rng.gamma(O["n_pdu"] + 0.5, 1.0 / O["rack_years"])
        rep = {k: v[rng.integers(0, len(v), size=len(v))] if len(v) else v for k, v in rep.items()}
    if opt.get("independent"):
        # the same expected node-hours lost, as independent single-node events
        extra_rate = (sw_rate * 8 * np.mean(rep["switch"]) + pd_rate * 4 * np.mean(rep["pdu"])) / 8760.0 / 8.0
    out_n, out_s, out_e, out_c = [], [], [], []
    racks = pk.rack["rack"].values
    if not opt.get("independent"):
        for r in sorted(set(racks)):
            members = np.where(racks == r)[0]
            for kind, rate, pool, take in (("switch", sw_rate, rep["switch"], members), ("pdu_a", pd_rate / 2, rep["pdu"], members[:4]),
                                           ("pdu_b", pd_rate / 2, rep["pdu"], members[4:])):
                t = y0
                while True:
                    t += rng.exponential(8760.0 / max(rate, 1e-9))
                    if t > y1:
                        break
                    dur = float(rng.choice(pool)) if len(pool) else 19.0
                    for k in take:
                        out_n.append(k); out_s.append(t); out_e.append(t + dur + rng.uniform(0, 0.4)); out_c.append(2)
    for k in range(nodes_n):
        t = y0
        last = y0 - rng.uniform(0, 200.0)
        while t < y1:
            # next maintenance end resets uptime
            nm = ms[ms > t]
            next_m = nm[0] if len(nm) else 1e18
            u = t - last
            # software failure: piecewise-constant hazard by uptime, inverted exactly
            E = rng.exponential(1.0)
            uu = u
            acc = 0.0
            t_sw = 1e18
            for kb in range(len(hz)):
                lo, hi = UPTIME_BINS[kb], UPTIME_BINS[kb + 1]
                if uu >= hi:
                    continue
                a = max(uu, lo)
                need = (E - acc) / max(hz[kb], 1e-12)
                if a + need < hi:
                    t_sw = last + a + need
                    break
                acc += hz[kb] * (hi - a)
            t_hw = t + rng.exponential(1.0 / max(hw, 1e-12))
            t_ex = t + rng.exponential(1.0 / extra_rate) if opt.get("independent") and extra_rate > 0 else 1e18
            t_next = min(t_sw, t_hw, next_m, t_ex)
            if t_next >= y1:
                break
            if t_next == next_m:
                t = me[ms == next_m][0] + 0.1
                last = t
                continue
            if t_next == t_hw:
                dur = float(rng.choice(rep["hardware"])) if len(rep["hardware"]) else 100.0
                out_c.append(1)
            elif t_next == t_ex:
                dur = float(rng.choice(np.concatenate([rep["switch"], rep["pdu"]]))) if len(rep["switch"]) + len(rep["pdu"]) else 19.0
                out_c.append(2)
            else:
                out_c.append(0)
                l = sim.local(t_next)
                office = l.weekday() < 5 and 7.5 <= l.hour + l.minute / 60.0 <= 19.0
                pool = rep["software_office"] if office else rep["software_night"]
                dur = float(rng.choice(pool)) if len(pool) else 1.0
            out_n.append(k); out_s.append(t_next); out_e.append(t_next + dur)
            t = t_next + dur + 0.05
            last = t
    # administrative drains
    t = y0
    while True:
        t += rng.exponential(1.0 / max(O["admin_rate"] * nodes_n, 1e-9))
        if t > y1:
            break
        out_n.append(int(rng.integers(0, nodes_n))); out_s.append(t)
        out_e.append(t + (float(rng.choice(rep["admin"])) if len(rep["admin"]) else 4.0)); out_c.append(3)
    out_n = np.array(out_n, dtype=np.int32); out_s = np.array(out_s); out_e = np.array(out_e); out_c = np.array(out_c)
    order = np.argsort(out_s, kind="stable")
    return (out_n[order], out_s[order], out_e[order], out_c[order]), (ms, me)


def elig_of(jobs, R):
    """eligibility as the scheduler sets it: a dependent job becomes eligible when its predecessor ends"""
    sub = R["submit"].copy()
    dep = jobs["dep"]
    has = dep >= 0
    pred_end = np.where(has, R["final_end"][np.maximum(dep, 0)], -1.0)
    return np.where(has & (pred_end > sub), pred_end, sub)


def future(F, pk, year, T_total, seed, opt=None, window=None):
    """one simulated future: the window's P90 queue wait over the jobs eligible in it (policy 2.1 and 2.2),
    node-hours and rework"""
    opt = opt or {}
    rng = np.random.default_rng(seed)
    jobs = demand_year(F, pk, year, T_total, rng, opt)
    outages, maint = outages_year(F, pk, year, rng, opt)
    outages = outages[:3]
    n_nodes = len(pk.rack)
    if opt.get("const_avail"):
        n_nodes = int(round(len(pk.rack) * F.outage["mean_availability"]))
    a, b = window or (H(year), H(year + 1))
    R = des.simulate(n_nodes, jobs, outages, maint, b + 24.0 * 35, mode=opt.get("mode", 1), bf_max=P.BF_MAX,
                     hold=P.REQUEUE_HOLD)
    elig = elig_of(jobs, R)
    m = (elig >= a) & (elig < b) & (R["first_start"] >= 0)
    w = R["first_start"][m] - elig[m]
    return {"p90": float(np.percentile(w, 90)), "p50": float(np.percentile(w, 50)), "n": int(m.sum()),
            "nh": float(R["nh"][m].sum()), "rework": float(R["rework"][m].sum()),
            "pending": int(((elig >= a) & (elig < b) & (R["first_start"] < 0)).sum())}


def replay_inputs(pk, a, b, warm=24.0 * 21):
    """the record's own jobs as the simulator's input: every job eligible from a warm-up before the window to its
    end, with its recorded eligibility, nodes, requested limit and run time (a job cut at its limit runs to it)"""
    j = pk.jobs[(pk.jobs["elig_h"] >= a - warm) & (pk.jobs["elig_h"] < b) & pk.jobs["start_h"].notna()]
    j = j.sort_values("elig_h")
    n = len(j)
    st = j["state"].values
    endstate = np.where(st == "FAILED", 2, np.where(st == "CANCELLED", 3, 0)).astype(np.int32)
    # a requeued job's elapsed carries its redone work; the run time replayed is its last run plus what the
    # earlier runs kept, which the record does not show; the final run's elapsed is the closest reading
    last = pk.seg.groupby(["jobid", "epoch"])["elapsed_h"].last()
    dur = np.array([last.get((a_, b_), e) for a_, b_, e in zip(j["jobid"], j["epoch"], j["elapsed_h"])])
    dur = np.where(st == "TIMEOUT", j["wall_h"].values, dur)
    return {"submit": j["elig_h"].values.astype(float), "nodes": j["nodes"].values.astype(np.int32),
            "wall": j["wall_h"].values.astype(float), "dur": np.maximum(dur, 0.01), "ckpt": np.zeros(n),
            "dep": np.full(n, -1, dtype=np.int32), "after": np.full(n, -1, dtype=np.int32), "after_delay": np.zeros(n),
            "endstate": endstate, "account": j["account"].values}


def replay(F, pk, window, seed, opt=None):
    """the backtest: the window's recorded jobs through the simulator with the outage and rework processes fitted
    on the record before the window; the P90 wait over the jobs eligible in the window"""
    opt = opt or {}
    rng = np.random.default_rng(seed)
    a, b = window
    jobs = replay_inputs(pk, a, b)
    if not opt.get("no_rework"):
        ck = np.array([F.ckpt.get(acc, np.nan) for acc in jobs["account"]])
        pool_c = F.ckpt_bycat.get("_all") or [0.0, 1.0, 6.0]
        fill = rng.choice(pool_c, size=len(ck))
        jobs["ckpt"] = np.where(np.isnan(ck), fill, ck)
    else:
        jobs["ckpt"] = np.full(len(jobs["submit"]), 1e-6)
    year = sim.local(a).year
    outages, maint = outages_year(F, pk, year, rng, opt)
    outages = outages[:3]
    n_nodes = len(pk.rack)
    if opt.get("const_avail"):
        n_nodes = int(round(len(pk.rack) * F.outage["mean_availability"]))
    R = des.simulate(n_nodes, jobs, outages, maint, b + 24.0 * 10, mode=opt.get("mode", 1), bf_max=P.BF_MAX,
                     hold=P.REQUEUE_HOLD)
    sub = jobs["submit"]
    m = (sub >= a) & (sub < b) & (R["first_start"] >= 0)
    w = R["first_start"][m] - sub[m]
    return {"p90": float(np.percentile(w, 90)), "p50": float(np.percentile(w, 50)), "n": int(m.sum()),
            "nh": float(R["nh"][m].sum()), "rework": float(R["rework"][m].sum())}


_CTX = {}


def _worker(args):
    key, year, T_total, seed, opt, window = args
    F, pk = _CTX["F"], _CTX["pk"]
    if key == "replay":
        return replay(F, pk, window, seed, opt)
    return future(F, pk, year, T_total, seed, opt, window)


def run_futures(F, pk, year, T_total, n, opt=None, window=None, seed0=0, workers=None, kind="future"):
    """n futures in parallel (fork), deterministic in seed; kind='replay' runs the backtest's trace replay"""
    opt = opt or {}
    _CTX["F"], _CTX["pk"] = F, pk
    args = [("replay" if kind == "replay" else "f", year, T_total, seed0 + i, opt, window) for i in range(n)]
    workers = workers or max(1, min(16, (os.cpu_count() or 4) - 2))
    if workers == 1 or n < 8:
        return [_worker(a) for a in args]
    ctx = mp.get_context("fork")
    with ctx.Pool(workers) as pool:
        return pool.map(_worker, args, chunksize=max(1, n // (workers * 4)))


def p_meets(results, level=4.0):
    return float(np.mean([r["p90"] <= level for r in results]))


def cap_sweep(F, pk, Ts, n, opt=None, seed0=0, workers=None, level=4.0):
    out = {}
    for T_total in Ts:
        res = run_futures(F, pk, 2027, T_total, n, opt, seed0=seed0 + int(T_total), workers=workers)
        out[int(T_total)] = {"p": p_meets(res, level), "p90_mean": float(np.mean([r["p90"] for r in res])),
                             "p90_median": float(np.median([r["p90"] for r in res])), "n": n,
                             "nh_mean": float(np.mean([r["nh"] for r in res])),
                             "rework_mean": float(np.mean([r["rework"] for r in res]))}
    return out


def cap_from_sweep(sw, threshold=0.8, step=10000):
    Ts = sorted(sw)
    ok = [t for t in Ts if sw[t]["p"] >= threshold]
    if not ok:
        return None
    return max(ok)


def find_cap(F, pk, opt=None, n_coarse=200, n_fine=2000, step=10000, lo=300000, hi=1200000, seed0=0, workers=None,
             fine_span=3, level=4.0, max_extend=4):
    """bracket the crossing on a coarse grid, then the steps around it with n_fine futures"""
    opt = opt or {}
    coarse = {}
    a, b = lo, hi
    # bisection on the coarse count
    while b - a > 4 * step:
        mid = int(round((a + b) / 2 / step) * step)
        res = run_futures(F, pk, 2027, mid, n_coarse, opt, seed0=seed0 + mid, workers=workers)
        p = p_meets(res, level)
        coarse[mid] = p
        if p >= 0.8:
            a = mid
        else:
            b = mid
    centre = int(round((a + b) / 2 / step) * step)
    Ts = [centre + k * step for k in range(-fine_span, fine_span + 1)]
    fine = cap_sweep(F, pk, Ts, n_fine, opt, seed0=seed0, workers=workers, level=level)
    # extend while the edges are not settled, by at most max_extend steps each way
    k = 0
    while fine[min(fine)]["p"] < 0.8 and min(fine) > lo and k < max_extend:
        t = min(fine) - step
        fine.update(cap_sweep(F, pk, [t], n_fine, opt, seed0=seed0, workers=workers, level=level))
        k += 1
    k = 0
    while fine[max(fine)]["p"] >= 0.8 and max(fine) < hi and k < max_extend:
        t = max(fine) + step
        fine.update(cap_sweep(F, pk, [t], n_fine, opt, seed0=seed0, workers=workers, level=level))
        k += 1
    return {"coarse": coarse, "fine": fine, "cap": cap_from_sweep(fine)}


def quick_cap(F, pk):
    """the plan's arithmetic: node-hours available at the mean availability over the pooled use ratio"""
    avail = len(pk.rack) * 8760.0 * F.outage["mean_availability"]
    return avail / F.ratios["pooled"]
