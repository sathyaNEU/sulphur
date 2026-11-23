"""task9 architecture 6: every owed figure computed from target/ alone (load.py, then core.py's estimators on the
loaded record), the rivals the cut pack adds to the core's battery, figures.json and effort.json.

    python3 task9/generator/results.py      prints the golden and the bands
"""
import contextlib
import copy
import io
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402
import load as L  # noqa: E402

TASK = os.path.dirname(HERE)
NAMES = {"optimisation": "optimisation noise", "turnover": "training data", "retunes": "retunes",
         "releases": "feature releases", "labels": "label revisions"}
ORDER = ("labels", "releases", "optimisation", "turnover", "retunes")
BANDS = ("monitor", "a remediation plan", "escalation")


def call_of(e):
    return {NAMES[s]: BANDS[e["band"][s]] for s in C.SOURCES}


def call_list(e):
    return sorted("%s: %s" % (k, v) for k, v in call_of(e).items())


def with_weights(pk, merch):
    q = copy.copy(pk)
    q.w = dict(pk.w, merch=np.asarray(merch, float))
    return q


def with_d13(pk, d13):
    q = copy.copy(pk)
    q.d13 = np.asarray(d13, float)
    return q


def snapshot_d13(pk):
    out = []
    for f in range(C.F):
        v = [np.nanmean((pk.z[f][:, b] - pk.z[f][:, a]) ** 2) for a, b in C.SPANS26]
        out.append(float(np.mean(v)))
    return np.array(out)


def single_runs(pk, kind):
    import pandas as pd
    t = os.path.join(TASK, "target")
    preg = pd.read_csv(os.path.join(t, "mrm_instrument_pair_register_2026.csv"))
    ps = pd.read_csv(os.path.join(t, "mrm_instrument_pair_scores_2026.csv"))
    var = (ps["score_b"] - ps["score_a"]).groupby(ps["pair_id"]).agg(lambda x: float(np.var(x.to_numpy())))
    codes = pk.w["codes"]
    per = {}
    for c, g in preg[preg["pair_kind"] == kind].sort_values("refresh_date").groupby("model_family"):
        per[codes.index(c)] = [var[p] for p in g["pair_id"]]
    k = min(len(v) for v in per.values())
    wt = pk.w["merch"] / pk.w["merch"].sum()
    scale = C.H / 4.0 if kind == "retune_shadow" else C.H
    return [math.sqrt(float(sum(wt[f] * per[f][i] for f in range(C.F))) * scale) for i in range(k)]


def at_start(pk, start):
    q = copy.copy(pk)
    s = [int(x) for x in start]
    q.curves = [C.lag_curve(pk.w, pk.z, f, start=s[f])[0] for f in range(C.F)]
    q.t0 = tuple(s)
    q.events = [C.events_in_span(pk.w, f, s[f], C.LAGS) for f in range(C.F)]
    q.curves26 = [C.lag_curve(pk.w, pk.z, f, start=max(s[f], C.Y26))[0] for f in range(C.F)]
    q.d13 = np.array([c[C.H - 1] for c in q.curves])
    q.d1 = np.array([c[0] for c in q.curves])
    q.dc_gold = q._data_curve(*q.rec["fam_log"])
    return q


def plug_in(pk, model, weeks):
    w = pk.w
    return np.array([(weeks >= w["fv_planned"][f] + model["slip"] + math.exp(model["mu"][f])) * (1.0 - model["rev"])
                     for f in range(C.F)], float)


def recency_kernel_probes(pk):
    """Alternative monotone recency kernels fitted to the 16 2026 bootstrap pairs per family (S2 determinism check)."""
    w, inst = pk.w, pk.inst
    wt = w["merch"] / w["merch"].sum()
    specs = [
        ("exponential", lambda ages, g: g[:, None] ** ages[None, :], np.linspace(0.75, 1.0, 126)),
        ("power-law (a=2)", lambda ages, g: (1.0 + ages[None, :] / g[:, None]) ** (-2.0), np.linspace(2.0, 100.0, 99)),
        ("linear ramp", lambda ages, g: np.maximum(1.0 - ages[None, :] / g[:, None], 1e-4), np.linspace(6.0, 200.0, 98)),
        ("truncated K-week", lambda ages, g: np.where(ages[None, :] < g[:, None], 1.0, 1e-4), np.arange(4, 105, 1, dtype=float)),
        ("uniform (lam=1)", lambda ages, g: np.ones((len(g), len(ages))), np.array([1.0])),
    ]
    out = {}
    for name, fn, grid in specs:
        rmses, tur27 = [], np.zeros(C.F)
        for f in range(C.F):
            W = int(w["window"][f])
            ages = np.arange(W - 1, -1, -1, dtype=float)
            y = np.maximum(inst["boot_v"][f] - inst["rep"][f], 0.5)
            bt = inst["boot_t"][f]
            rows = w["rows"][f]
            wk0 = w["wk0"]
            N_mat = np.array([rows[wk0 + int(t) - W + 1:wk0 + int(t) + 1] for t in bt], float)
            A_mat = fn(ages, grid)
            den = A_mat @ N_mat.T
            bf_all = 2.0 * ((A_mat ** 2) @ N_mat.T) / (den ** 2)
            log_diff = np.log(y)[None, :] - np.log(bf_all)
            log_c = np.mean(log_diff, axis=1)
            sses = np.sum((log_diff - log_c[:, None]) ** 2, axis=1)
            bi = int(np.argmin(sses))
            rmses.append(math.sqrt(float(sses[bi]) / len(bt)))
            c = math.exp(float(log_c[bi]))
            a = A_mat[bi]
            tfs = []
            for t0, t1 in C.SPANS27:
                n0 = rows[wk0 + t0 - W + 1:wk0 + t0 + 1]
                n1 = rows[wk0 + t1 - W + 1:wk0 + t1 + 1]
                p0 = (a * n0) / (a * n0).sum()
                p1 = (a * n1) / (a * n1).sum()
                h = t1 - t0
                tf = float(np.sum((p0[:h] ** 2) / n0[:h]) + np.sum((p1[W - h:] ** 2) / n1[W - h:]) +
                           np.sum(((p1[:W - h] - p0[h:]) ** 2) / n0[h:]))
                tfs.append(tf)
            tur27[f] = c * float(np.mean(tfs))
        out[name] = {"log_rmse": float(np.mean(rmses)), "points": math.sqrt(float(wt @ tur27))}
    return out


START_RULES = ("the first warm retrain after the last cold one",
               "thirteen weeks after the last cold retrain, no floor",
               "the last of the three past rollouts' first use",
               "2026 only")


def forks(pk):
    w = pk.w
    last_use = np.array([max(int(w[n]["eff"][f]) for n in ("runtime", "warm", "amp")) for f in range(C.F)])
    starts = dict(zip(START_RULES, (w["last_cold"] + 1, w["last_cold"] + 13, last_use,
                                    np.maximum(np.array(pk.t0), C.Y26))))
    admitted = {}
    for k, s in starts.items():
        q = at_start(pk, s)
        fits = ("anch25", "anch20") if k == "2026 only" else ("anch25", "anch20", "flat")
        for fit in fits:
            admitted["settled weeks from %s, fit %s" % (k, fit)] = C.evaluate(q, fit=fit)
    wp = np.arange(C.Y27 - 1, 182)
    for m in ("loglin", "linear", "groups", "own"):
        admitted["take-up %s as a plug-in median lag" % m] = C.evaluate(pk, cov=plug_in(pk, pk.models[m], wp))
    return admitted


def run(target=None, quiet=True):
    target = target or os.path.join(TASK, "target")
    pk = L.pack(target)
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        A = C.analyse(pk, None)
    g = A["gold"]
    wt = pk.w["merch"] / pk.w["merch"].sum()
    bw = lambda v: float(wt @ np.asarray(v, float))

    panel116 = np.array([np.sum(~np.isnan(pk.z[f][:, 116])) * 5.0 for f in range(C.F)])
    extra = {
        "families weighted by the panel at the latest snapshot, times five": C.evaluate(with_weights(pk, panel116)),
        "merchants' own change from the 2026 snapshot pairs only": C.evaluate(with_d13(pk, snapshot_d13(pk))),
    }
    mess_pks = {m: L.pack(target, mess=(m,)) for m in L.MESS}
    mess = {m: C.evaluate(mpk) for m, mpk in mess_pks.items()}
    fam = A["fam"] + list(extra.values())
    admitted = forks(pk)
    lat = A["lattice"]
    routes = A["routes"]
    free = A["free"]
    free_nosub = C.evaluate(pk, fit="free25", sub_data=False)

    refused_e = (
        list(lat.values()) + list(routes.values()) + list(A["extra"].values()) +
        list(A["over"].values()) + [
            free_nosub,
            C.evaluate(pk, S1="linear2"),
            C.evaluate(pk, S1="cut8"),
            C.evaluate(pk, S2="raw"),
            C.evaluate(pk, S2="unif_raw"),
            C.evaluate(pk, S2="half_w"),
            C.evaluate(pk, S3="all_same_rho"),
            C.evaluate(pk, cov_mode="plan"),
            C.evaluate(pk, cov_mode="declared"),
            C.evaluate(pk, cov_mode="worst"),
            C.evaluate(pk, weights="equal"),
        ]
    )

    keys = (
        ["points_" + s for s in C.SOURCES]
        + ["tot_q1", "tot_q2", "tot_q3", "tot_q4", "tot_yr", "cc_pin"]
        + ["share_" + s for s in C.SOURCES]
        + ["own_share", "fr_sched", "fr_removed"]
    )
    bands, adm_range = {}, {}
    for k in keys:
        vals = [e[k] for e in fam] + [g[k]] + [e[k] for e in admitted.values()]
        lo, hi = min(vals), max(vals)
        adm_range[k] = [lo, hi]
        bands[k] = [lo - 0.25 * (hi - lo), hi + 0.25 * (hi - lo)]
        ref = [e[k] for e in refused_e]
        below, above = [v for v in ref if v < lo - 1e-9], [v for v in ref if v > hi + 1e-9]
        if below:
            bands[k][0] = max(bands[k][0], 0.5 * (max(below) + lo))
        if above:
            bands[k][1] = min(bands[k][1], 0.5 * (min(above) + hi))
    for s, kind in (("retunes", "retune_shadow"), ("labels", "label_freeze")):
        sr = single_runs(pk, kind)
        bands["points_" + s] = [min(bands["points_" + s][0], min(sr)), max(bands["points_" + s][1], max(sr))]
    bands["cc1"] = bands["points_optimisation"]
    bands["cc2"] = bands["points_turnover"]
    bands["cc3"] = bands["points_releases"]

    reflex = lat["S1+S2+S3"]
    direct = routes["direct"]
    rigorous = routes["rigorous"]
    fals = A["fals"]

    # Clean record counts for Step-by-Step
    import glob as _glob
    import pandas as pd
    raw_ms = int(mess_pks["no_rekey"].w["ms"].sum())
    score_rows = int(sum(np.sum(~np.isnan(Z)) for Z in pk.z))
    raw_score_rows = sum(sum(1 for _ in open(p)) - 1 for p in _glob.glob(os.path.join(target, "gms_monitoring_panel_scores_*.csv")))
    manifest_lines = sum(1 for _ in open(os.path.join(target, "training_scheduler_runs_2024_2026.jsonl")))
    seen_r, prod_r = set(), 0
    for line in open(os.path.join(target, "training_scheduler_runs_2024_2026.jsonl")):
        r = json.loads(line)
        if r["run_id"] not in seen_r:
            seen_r.add(r["run_id"])
            if r["kind"] == "production":
                prod_r += 1
    preg = pd.read_csv(os.path.join(target, "mrm_instrument_pair_register_2026.csv"))
    pairs_by_kind = {k: int(v) for k, v in preg["pair_kind"].value_counts().items()}

    # Leave-one-rollout-out check for pinned views
    loo = {}
    for leave in ("runtime", "warm", "amp"):
        m = C.coverage_model(pk.w, "loglin", leave=leave)
        r = pk.w[leave]
        rec_sh, mod_sh = [], []
        for f in range(C.F):
            p0 = int(r["planned"][f])
            wks = np.arange(p0, p0 + 39)
            a, b = r["revert"][f]
            on = (wks >= r["eff"][f]) & ~((b > a) & (wks >= a) & (wks < b))
            rec_sh.append(float(np.mean(on)))
            mod_sh.append(float(np.mean(C.lognormal_cdf(wks - (p0 + m["slip"]), m["mu"][f], m["sg"]) * (1.0 - m["rev"]))))
        loo[leave] = {"record": float(np.mean(rec_sh)), "model": float(np.mean(mod_sh))}

    # Gap-curve bend & cold-era linearity diagnostics
    ic8 = [float(np.polyfit(np.arange(8, 26), pk.curves[f][7:25], 1)[1]) for f in range(C.F)]
    ic8_book = bw(ic8)
    boot_mean_v = np.array([float(np.mean(v)) for v in pk.inst["boot_v"]])
    boot_net_v = np.maximum(boot_mean_v - pk.inst["rep"], 0.0)
    kernels = recency_kernel_probes(pk)

    # S2 bootstrap log-RMSE comparison (golden exponential vs uniform vs lag-0)
    rmse_rec, rmse_unif, rmse_lag0 = [], [], []
    for f in range(C.F):
        W = int(pk.w["window"][f])
        y = np.maximum(pk.inst["boot_v"][f] - pk.inst["rep"][f], 0.5)
        bt = pk.inst["boot_t"][f]
        bf_r = np.array([C.boot_factor(pk.w["rows"][f], pk.w["wk0"], int(t), W, g["lam"][f]) for t in bt])
        bf_u = np.array([C.boot_factor(pk.w["rows"][f], pk.w["wk0"], int(t), W, 1.0) for t in bt])
        bf_0 = np.array([2.0 / pk.w["rows"][f][pk.w["wk0"] + int(t)] for t in bt])
        for bf, acc in ((bf_r, rmse_rec), (bf_u, rmse_unif), (bf_0, rmse_lag0)):
            c = float(np.mean(np.log(y) - np.log(bf)))
            acc.append(math.sqrt(float(np.mean((np.log(y) - (c + np.log(bf))) ** 2))))

    # Calendar 2027 Mondays pinned share (closed by Standard 2.2 -- recorded as probe only!)
    m_ll = pk.models["loglin"]
    wk_cal = np.arange(C.Y27 + 1, C.Y27 + 53)
    cc_cal = 100.0 * float(np.mean([
        C.lognormal_cdf(wk_cal - (pk.w["fv_planned"][f] + m_ll["slip"]), m_ll["mu"][f], m_ll["sg"]) * (1.0 - m_ll["rev"])
        for f in range(C.F)
    ]))

    fig = {
        "call": call_list(g),
        "band_of": call_of(g),
        "points": {NAMES[s]: g["points"][s] for s in C.SOURCES},
        "agg": {NAMES[s]: g["agg"][s] for s in C.SOURCES},
        "share": {NAMES[s]: g["share"][s] for s in C.SOURCES},
        "tot_q": list(g["tot_q"]),
        "tot_q1": g["tot_q1"], "tot_q2": g["tot_q2"], "tot_q3": g["tot_q3"], "tot_q4": g["tot_q4"],
        "tot_yr": g["tot_yr"],
        "cc1": g["cc1"], "cc2": g["cc2"], "cc3": g["cc3"],
        "cc_pin": g["cc_pin"],
        "own_share": g["own_share"],
        "own_ms": g["own"],
        "fr_sched": g["fr_sched"],
        "fr_removed": g["fr_removed"],
        "fr26": 100.0 * bw(pk.fr26),
        "bands": bands,
        "adm_range": adm_range,
        "variants": len(fam),
        "battery_calls": all(call_list(e) == call_list(g) for e in fam + list(admitted.values())),
        "battery_range": {NAMES[s]: [min(e["points"][s] for e in fam), max(e["points"][s] for e in fam)] for s in C.SOURCES},
        "base": {
            "panel_merchants": int(pk.w["ms"].sum()),
            "panel_merchants_unmapped": int(raw_ms),
            "score_rows": score_rows,
            "raw_score_rows": raw_score_rows,
            "manifest_lines": manifest_lines,
            "manifest_runs": len(seen_r),
            "production_runs": prod_r,
            "pairs": int(len(preg)),
            "pairs_by_kind": pairs_by_kind,
            "book_sep26": int(pk.w["merch"].sum()),
            "replicate": bw(pk.inst["rep"]),
            "bootstrap": bw(boot_mean_v),
            "bootstrap_net": bw(boot_net_v),
            "retune": bw(pk.inst["ret"]),
            "release": bw(pk.inst["rel"]),
            "label": bw(pk.inst["lab"]),
            "phi_fit": [float(g["phi"].min()), float(g["phi"].max())],
            "lam_fit": [float(g["lam"].min()), float(g["lam"].max())],
            "coh_same_mean": float(np.mean(pk.inst["rel_coh_same_pairs"])),
            "coh_same_min": float(np.min(pk.inst["rel_coh_same_pairs"])),
            "coh_same_n": int(len(pk.inst["rel_coh_same_pairs"])),
            "coh_diff_mean": float(np.mean(pk.inst["rel_coh_diff_pairs"])),
            "coh_diff_n": int(len(pk.inst["rel_coh_diff_pairs"])),
            "cov_plan": 100.0 * float(np.mean(C.coverage_weeks(pk.w, "plan", pk.models["loglin"])[:, 1:])),
            "cov_declared": 100.0 * float(np.mean(C.coverage_weeks(pk.w, "declared", pk.models["loglin"])[:, 1:])),
            "cov_cal27": cc_cal,
            "d1": pk.obs_d1,
            "d13": bw(pk.d13),
            "retunes_per_pair": C.H / 4.0,
        },
        "bend": {
            "intercept8_book": ic8_book,
            "intercept8_min": min(ic8),
            "cold_min_weeks": int(pk.w["warm"]["eff"].min()),
            "cold_max_weeks": int(pk.w["warm"]["eff"].max()),
            "cold_curv_mean": float(np.mean(pk.cold_curv)),
            "cold_curv_min": float(min(pk.cold_curv)),
            "cold_curv_max": float(max(pk.cold_curv)),
        },
        "recency_diag": {
            "log_rmse_exp": float(np.mean(rmse_rec)),
            "log_rmse_unif": float(np.mean(rmse_unif)),
            "log_rmse_lag0": float(np.mean(rmse_lag0)),
            "unif_ratio": float(np.mean(rmse_unif) / np.mean(rmse_rec)),
            "lag0_ratio": float(np.mean(rmse_lag0) / np.mean(rmse_rec)),
            "kernels": kernels,
        },
        "falsification": {
            "obs_d1": pk.obs_d1,
            "obs_boot_contrast": pk.obs_boot_contrast,
            "obs_rel_cov": pk.obs_rel_cov,
            "golden_err": g["fals_err"],
            "golden_parts": {"d1": g["pred_d1"], "boot_c": g["pred_bc"], "rel_cov": g["pred_rc"]},
            "rivals": dict(fals["rivals"]),
        },
        "loo": loo,
        "reflex": {"points": {NAMES[s]: reflex["points"][s] for s in C.SOURCES},
                   "tot_q": list(reflex["tot_q"]), "tot_yr": reflex["tot_yr"],
                   "cc_pin": reflex["cc_pin"], "call": call_list(reflex)},
        "direct": {"points": {NAMES[s]: direct["points"][s] for s in C.SOURCES},
                   "tot_q": list(direct["tot_q"]), "tot_yr": direct["tot_yr"],
                   "cc_pin": direct["cc_pin"], "call": call_list(direct)},
        "rigorous": {"points": {NAMES[s]: rigorous["points"][s] for s in C.SOURCES},
                     "tot_q": list(rigorous["tot_q"]), "tot_yr": rigorous["tot_yr"],
                     "cc_pin": rigorous["cc_pin"], "call": call_list(rigorous)},
        "lattice": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES},
                        "tot_q": list(e["tot_q"]), "tot_yr": e["tot_yr"],
                        "cc_pin": e["cc_pin"], "call": call_list(e)} for k, e in lat.items()},
        "over": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES}, "call": call_list(e)}
                 for k, e in A["over"].items()},
        "probe": {
            "linear 13 refits (half pair)": lat["S1"]["points"]["optimisation"],
            "full replicate pair per refit": C.evaluate(pk, S1="linear2")["points"]["optimisation"],
            "single replicate pair (over)": A["over"]["S1"]["points"]["optimisation"],
            "unanchored fit (sub data)": free["points"]["optimisation"],
            "unanchored fit (raw curve)": free_nosub["points"]["optimisation"],
            "unanchored raw implied rep": bw(free_nosub["A"] * (1.0 - free_nosub["phi"] ** 2)),
            "uniform window turnover": lat["S2"]["points"]["turnover"],
            "raw bootstrap face value": direct["points"]["turnover"],
            "net bootstrap face value (over)": A["over"]["S2"]["points"]["turnover"],
            "orthogonal releases (actual lag)": lat["S3"]["points"]["releases"],
            "orthogonal releases (calendar plan)": direct["points"]["releases"],
            "all releases aligned (over)": A["over"]["S3"]["points"]["releases"],
        },
        "extra": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES},
                      "tot_yr": e["tot_yr"], "cc_pin": e["cc_pin"], "call": call_list(e)}
                  for k, e in extra.items()},
        "mess": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES},
                     "tot_q": list(e["tot_q"]), "tot_yr": e["tot_yr"],
                     "cc_pin": e["cc_pin"], "call": call_list(e)} for k, e in mess.items()},
    }
    import writeup as WU
    fig["stated"] = WU.stated(fig)
    fig["rubric"] = rubric(A["spec"])
    fig["rubric_stated"] = rubric(stated_spec(A["spec"], fig["stated"]))
    fig["panel_merchants"] = fig["base"]["panel_merchants"]
    fig["fals_check"] = fig["falsification"]["golden_err"]
    fig["cap"] = 12
    fig["windows"] = sorted(set(int(x) for x in pk.w["window"]))
    fig["loo_pct"] = {k: [100.0 * v["record"], 100.0 * v["model"]] for k, v in fig["loo"].items()}
    fig["lines"] = list(C.LINES)
    E = effort(fig, g, A, pk, lat, routes, fam, extra, bands)
    return pk, A, fig, E


def stated_spec(spec, S):
    spec = copy.deepcopy(spec)
    key = {
        "CC1 optimisation noise alone, points": "points_optimisation",
        "CC2 training data alone, points": "points_turnover",
        "CC3 feature releases alone, points": "points_releases",
        "optimisation points": "points_optimisation",
        "turnover points": "points_turnover",
        "releases points": "points_releases",
        "labels points": "points_labels",
        "retunes points": "points_retunes",
        "Q1 combined model-side RMS": "tot_q1",
        "Q2 combined model-side RMS": "tot_q2",
        "Q3 combined model-side RMS": "tot_q3",
        "Q4 combined model-side RMS": "tot_q4",
        "2027 combined model-side RMS": "tot_yr",
        "pinned views share": "cc_pin",
    }
    for f in spec["figures"]:
        f["band"] = list(S[key[f["id"]]])
    return spec


def rubric(spec):
    import corelib
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        rc = corelib.run(spec)
    txt = out.getvalue()
    got = {}
    for line in txt.splitlines():
        if line.startswith("| ") and ("| wrong |" in line or "| right |" in line):
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) == 3 and parts[2].isdigit():
                got[parts[0]] = int(parts[2])
    return {"verdict": txt.strip().splitlines()[-1], "exit": rc, "routes": got}


def effort(fig, g, A, pk, lat, routes, fam, extra, bands):
    reflex = lat["S1+S2+S3"]
    direct = routes["direct"]
    rigorous = routes["rigorous"]
    pts = lambda e, s: round(float(e["points"][s]), 3)
    r1_gold = {"panel merchants": fig["base"]["panel_merchants"],
               "retunes points": pts(g, "retunes"), "label revisions points": pts(g, "labels")}
    r1_val = lambda e, m_cnt: {"panel merchants": m_cnt,
                               "retunes points": pts(e, "retunes"), "label revisions points": pts(e, "labels")}
    r1_bands = {"panel merchants": [fig["base"]["panel_merchants"]] * 2,
                "retunes points": bands["points_retunes"], "label revisions points": bands["points_labels"]}
    r7 = lambda e: {"Q1": round(e["tot_q1"], 3), "Q2": round(e["tot_q2"], 3)}
    r7_bands = {"Q1": bands["tot_q1"], "Q2": bands["tot_q2"]}
    r8 = lambda e: {"Q3": round(e["tot_q3"], 3), "Q4": round(e["tot_q4"], 3)}
    r8_bands = {"Q3": bands["tot_q3"], "Q4": bands["tot_q4"]}
    fals = A["fals"]
    res = [
        {"id": "R1", "name": "cleaned panel, manifests, instruments and forced baseline sources (retunes and labels)",
         "graded_as": "Ask 1, Step-by-Step", "figure": "r1", "depends": [], "independent": "",
         "golden": r1_gold, "bands": r1_bands, "partly_share": 1.0,
         "passes": {"quick": r1_val(direct, fig["base"]["panel_merchants_unmapped"]),
                    "careful": r1_val(rigorous, fig["base"]["panel_merchants"]),
                    "thorough": r1_gold}},
        {"id": "R2", "name": "what optimisation noise alone moves a score between snapshots (warm-start decay)",
         "graded_as": "Component 1, Ask 1", "figure": "cc1", "depends": ["R1"],
         "independent": "the warm-era change-by-gap curve anchored to replicate pairs, with cold-era linearity",
         "golden": g["cc1"], "band": bands["cc1"],
         "passes": {"quick": pts(direct, "optimisation"), "careful": pts(rigorous, "optimisation"), "thorough": g["cc1"]},
         "precedent": ["L39", "L65", "N34"]},
        {"id": "R3", "name": "what training data alone moves a score between snapshots (recency-weighted turnover)",
         "graded_as": "Component 2, Ask 1", "figure": "cc2", "depends": ["R1"],
         "independent": "2026 weighted bootstrap pairs inverted against warehouse weekly labelled rows",
         "golden": g["cc2"], "band": bands["cc2"],
         "passes": {"quick": pts(direct, "turnover"), "careful": pts(rigorous, "turnover"), "thorough": g["cc2"]},
         "precedent": ["L28", "L22", "N21"]},
        {"id": "R4", "name": "what feature releases alone move a score between snapshots (within-group covariance)",
         "graded_as": "Component 3, Ask 1", "figure": "cc3", "depends": ["R1"],
         "independent": "paired 2026 release_shadow merchant vectors and past rollout manifests",
         "golden": g["cc3"], "band": bands["cc3"],
         "passes": {"quick": pts(direct, "releases"), "careful": pts(rigorous, "releases"), "thorough": g["cc3"]},
         "precedent": ["N44", "L58", "L28"]},
        {"id": "R5", "name": "share of 2027 assessment-year weekly retrains expected on pinned feature views",
         "graded_as": "Ask 3", "figure": "cc_pin", "depends": ["R1"],
         "independent": "past rollout lags from training scheduler manifests against change calendar",
         "golden": g["cc_pin"], "band": bands["cc_pin"],
         "passes": {"quick": direct["cc_pin"], "careful": rigorous["cc_pin"], "thorough": g["cc_pin"]}},
        {"id": "R6", "name": "three-part 2026 internal-record variance discrepancy check",
         "graded_as": "Step-by-Step", "figure": "fals_check", "depends": ["R2", "R3", "R4"],
         "independent": "", "golden": fals["golden"], "band": [0.0, 1.5],
         "passes": {"quick": fals["rivals"]["direct"], "careful": fals["rivals"]["rigorous (Response 1)"],
                    "thorough": fals["golden"]},
         "precedent": ["L28", "N44"]},
        {"id": "R7", "name": "H1 2027 combined model-side movement (Q1 and Q2 snapshot pairs)",
         "graded_as": "Ask 2", "figure": "r7", "depends": ["R1", "R2", "R3", "R4"], "independent": "",
         "golden": r7(g), "bands": r7_bands, "partly_share": 0.9,
         "passes": {"quick": r7(direct), "careful": r7(rigorous), "thorough": r7(g)},
         "precedent": ["L39", "L28", "N44"]},
        {"id": "R8", "name": "H2 2027 combined model-side movement (Q3 and Q4 snapshot pairs)",
         "graded_as": "Ask 2", "figure": "r8", "depends": ["R1", "R2", "R3", "R4"], "independent": "",
         "golden": r8(g), "bands": r8_bands, "partly_share": 0.9,
         "passes": {"quick": r8(direct), "careful": r8(rigorous), "thorough": r8(g)},
         "precedent": ["L39", "L28", "N44"]},
        {"id": "R9", "name": "full-year 2027 combined model-side movement",
         "graded_as": "Ask 2", "figure": "tot_yr", "depends": ["R1", "R2", "R3", "R4"], "independent": "",
         "golden": g["tot_yr"], "band": bands["tot_yr"],
         "passes": {"quick": direct["tot_yr"], "careful": rigorous["tot_yr"], "thorough": g["tot_yr"]},
         "precedent": ["L39", "L28", "N44"]},
        {"id": "R10", "name": "each source's band for 2027", "graded_as": "Recommendation",
         "figure": "call", "depends": ["R1", "R2", "R3", "R4"], "independent": "",
         "golden": call_list(g),
         "passes": {"quick": call_list(direct), "careful": call_list(rigorous), "thorough": call_list(g)},
         "precedent": ["L39", "L28", "N44"]},
    ]
    fig["r1"], fig["r7"], fig["r8"] = r1_gold, r7(g), r8(g)
    spec = A["spec"]
    hints = [{"sentence": spec["stumps"][k]["said_out_loud"], "rescues": [r]}
             for k, r in (("S1", "R2"), ("S2", "R3"), ("S3", "R4"))]
    alone_key = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
    moved = lambda e: [r["id"] for r in res[1:] if _moved(r, e, g, bands)]
    fact = {
        "golden_answer": call_list(g),
        "reflex_route": {"answer": call_list(reflex)},
        "judgments": [
            {"id": k, "name": spec["stumps"][k]["said_out_loud"], "kind": "stump",
             "precedent": spec["stumps"][k]["precedents"],
             "dropped": {"answer": call_list(lat[k]), "results_moved": moved(lat[k])},
             "alone": {"answer": call_list(lat[alone_key[k]]), "results_rescued": [{"S1": "R2", "S2": "R3", "S3": "R4"}[k]]}}
            for k in ("S1", "S2", "S3")
        ] + [
            {"id": "J4", "name": "retunes and label revisions scaled by their snapshot-pair counts", "kind": "reflex",
             "precedent": ["R20"]},
            {"id": "J5", "name": "actual pinned-view adoption lag fitted from the three past platform rollouts", "kind": "reflex",
             "precedent": ["R73"]},
            {"id": "J6", "name": "re-sent refreshes, Tolka Pay re-keying and scheduler family code mapping resolved", "kind": "reflex",
             "precedent": ["R01"]},
        ],
    }
    forcing = {
        "kind": "set", "golden_answer": call_list(g),
        "golden_family": [{"name": str(v) or "the golden", "answer": call_list(e)}
                          for v, e in zip(A["variants"], A["fam"])] +
                         [{"name": k, "answer": call_list(e)} for k, e in extra.items()],
        "shortcuts": [{"name": k, "answer": call_list(e)} for k, e in lat.items()] +
                     [{"name": k, "answer": call_list(e)} for k, e in routes.items()],
        "perturbations": _perturb(g),
    }
    route_list = [{"name": "the golden", "answer": call_list(g), "golden": True}] + \
        [{"name": "stumps lost: " + k, "answer": call_list(e)} for k, e in lat.items()] + \
        [{"name": k, "answer": call_list(e)} for k, e in list(routes.items()) + list(A["extra"].items())]
    return {"results": res, "hints": hints, "factorial": fact, "forcing": forcing, "routes": route_list,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}


def _moved(r, e, g, bands):
    if r["id"] == "R6":
        return True
    if r["id"] == "R10":
        return call_list(e) != call_list(g)
    key = {
        "R2": ["points_optimisation"],
        "R3": ["points_turnover"],
        "R4": ["points_releases"],
        "R5": ["cc_pin"],
        "R7": ["tot_q1", "tot_q2"],
        "R8": ["tot_q3", "tot_q4"],
        "R9": ["tot_yr"],
    }[r["id"]]
    return any(not (bands[k][0] <= e[k] <= bands[k][1]) for k in key)


def _perturb(g):
    out = []
    for s in C.SOURCES:
        for k, lab in ((0.8, "down a fifth"), (1.2, "up a fifth")):
            p = math.sqrt(k * g["agg"][s])
            band = sum(1 for l in C.LINES if p >= l)
            ans = call_of(g)
            ans[NAMES[s]] = BANDS[band]
            out.append({"input": "%s's mean-square movement %s" % (NAMES[s], lab),
                        "answer": sorted("%s: %s" % kv for kv in ans.items())})
    return out


if __name__ == "__main__":
    pk, A, fig, E = run()
    print(json.dumps({k: fig[k] for k in ("call", "points", "tot_q", "tot_yr", "cc_pin",
                                          "variants", "battery_calls", "probe", "falsification",
                                          "bend", "recency_diag", "rubric", "rubric_stated")},
                     indent=1, default=float))
