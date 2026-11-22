"""task9 architecture 5: every owed figure computed from target/ alone (load.py, then the core's estimators on the
loaded record), the rivals the cut pack adds to the core's battery, figures.json and effort.json.

    python3 task9/generator/results.py      prints the golden and the bands
"""
import copy
import datetime as dt
import io
import contextlib
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
ORDER = ("labels", "optimisation", "releases", "turnover", "retunes")   # the blocks' order: by band, then points
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
    """The record's mean-square change between its consecutive quarter-end snapshots only (the 2026 pairs)."""
    out = []
    for f in range(C.F):
        v = []
        for a, b in C.SPANS26:
            d = pk.z[f][:, b] - pk.z[f][:, a]
            v.append(np.nanmean(d ** 2))
        out.append(np.mean(v))
    return np.array(out)


def all_weeks_d13(pk):
    return np.array([np.nanmean((pk.z[f][:, 13:] - pk.z[f][:, :-13]) ** 2) for f in range(C.F)])


def single_runs(pk, kind):
    """Retunes' or label revisions' points with each family's instrument runs taken one at a time (the k-th run)."""
    import pandas as pd
    t = os.path.join(TASK, "target")
    preg = pd.read_csv(os.path.join(t, "mrm_instrument_pair_register_2026.csv"))
    ps = pd.read_csv(os.path.join(t, "mrm_instrument_pair_scores_2026.csv"))
    var = (ps["score_a"] - ps["score_b"]).groupby(ps["pair_id"]).agg(lambda x: float(np.var(x.to_numpy())))
    codes = pk.w["codes"]
    per = {}
    for c, g in preg[preg["pair_kind"] == kind].sort_values("refresh_date").groupby("model_family"):
        per[codes.index(c)] = [var[p] for p in g["pair_id"]]
    k = min(len(v) for v in per.values())
    wt = pk.w["merch"] / pk.w["merch"].sum()
    scale = C.H / 4.0 if kind == "retune_shadow" else C.H
    return [math.sqrt(float(sum(wt[f] * per[f][i] for f in range(C.F))) * scale) for i in range(k)]


def cc3_rivals(pk, g):
    """The pinned-views share on calendar 2027's Mondays (4 January to 27 December), and weighted by the book (a
    share of retrains counts each family's weekly retrain once, so the book weighting is not the prompt's)."""
    m = pk.models["loglin"]
    wk = np.arange(C.Y27 + 1, C.Y27 + 53)
    cc = np.array([C.lognormal_cdf(wk - (pk.w["fv_planned"][f] + m["slip"]), m["mu"][f], m["sg"]) * (1 - m["rev"])
                   for f in range(C.F)])
    wt = pk.w["merch"] / pk.w["merch"].sum()
    return {"calendar 2027 weeks": 100.0 * float(cc.mean()),
            "book weighted": 100.0 * float((wt * g["cov"][:, 1:].mean(1)).sum())}


def at_start(pk, start):
    """The record's gap curves, event counts and thirteen-week change rebuilt from other first weeks: where a family's
    settled weeks begin is the analyst's choice, and the curve, the closure and the release count move with it."""
    q = copy.copy(pk)
    s = [int(x) for x in start]
    q.curves = [C.lag_curve(pk.w, pk.z, f, start=s[f])[0] for f in range(C.F)]
    q.t0 = tuple(s)
    q.events = [C.events_in_span(pk.w, f, s[f], C.LAGS) for f in range(C.F)]
    q.curves26 = [C.lag_curve(pk.w, pk.z, f, start=max(s[f], C.Y26))[0] for f in range(C.F)]
    q.d13 = np.array([c[C.H - 1] for c in q.curves])
    q.d1 = np.array([c[0] for c in q.curves])
    return q


def plug_in(pk, model, weeks):
    """Pinned views from the planned week plus the mean slip plus the family's median lag, less the reverted share."""
    w = pk.w
    return np.array([(weeks >= w["fv_planned"][f] + model["slip"] + math.exp(model["mu"][f])) * (1 - model["rev"])
                     for f in range(C.F)], float)


def integrated(pk, model, weeks):
    w = pk.w
    return np.array([C.lognormal_cdf(weeks - (w["fv_planned"][f] + model["slip"]), model["mu"][f], model["sg"]) *
                     (1 - model["rev"]) for f in range(C.F)])


def pair_mean_rms(pk, g):
    """Feature releases read as the mean of the four 2027 pairs' root-mean-square changes (the reading the standard's
    section 3.2 closes): each pair's book-weighted mean square from the roadmap releases that land in it."""
    w = pk.w
    wt = w["merch"] / w["merch"].sum()
    out = []
    for a, b in C.SPANS27:
        ms = 0.0
        for f in range(C.F):
            hit = w["plan_weeks"][w["plan_hits"][:, f]]
            hit = hit[(hit > a) & (hit <= b)]
            ms += wt[f] * pk.inst["rel"][f] * float(np.sum(1 - g["cov"][f, hit - (C.Y27 - 1)]))
        out.append(math.sqrt(ms))
    return float(np.mean(out))


START_RULES = ("the first warm retrain after the last cold one", "thirteen weeks after the last cold retrain, no floor",
               "the last of the three past rollouts' first use", "2026 only")


def forks(pk):
    """The rivals the determinism audit opened, run in the golden's own estimators: where the settled weeks start
    (with each fit), the take-up as a plug-in median lag, calendar 2027's Mondays for the pinned-views share; and,
    refused, own change with 2026's release movement taken from a total measured over other weeks."""
    w = pk.w
    last_use = np.array([max(int(w[n]["eff"][f]) for n in ("runtime", "warm", "amp")) for f in range(C.F)])
    starts = dict(zip(START_RULES, (w["last_cold"] + 1, w["last_cold"] + 13, last_use,
                                    np.maximum(np.array(pk.t0), C.Y26))))
    admitted, mism = {}, {}
    for k, s in starts.items():
        q = at_start(pk, s)
        for fit in ("anch26", "anch20", "anch30", "flat"):
            admitted["settled weeks from %s, fit %s" % (k, fit)] = C.evaluate(q, fit=fit)
        if k != "2026 only":
            q.events = [C.events_in_span(w, f, max(int(s[f]), C.Y26), C.LAGS) for f in range(C.F)]
            mism[k] = C.evaluate(q)["own_share"]
    q = copy.copy(pk)
    q.events = [C.events_in_span(w, f, max(pk.t0[f], C.Y26), C.LAGS) for f in range(C.F)]
    mism["the settled weeks"] = C.evaluate(q)["own_share"]
    wp, wc = np.arange(C.Y27 - 1, 182), np.arange(C.Y27 + 1, C.Y27 + 53)
    cal, refused = {}, {}
    for m in ("loglin", "linear", "groups", "own", "pooled", "norevert"):
        e = C.evaluate(pk, cov=plug_in(pk, pk.models[m], wp))
        c1 = 100.0 * float(integrated(pk, pk.models[m], wc).mean())
        c2 = 100.0 * float(plug_in(pk, pk.models[m], wc).mean())
        if m in ("pooled", "norevert"):
            # one lag for every family is refused by the past rollouts' lags by custom components, and no reverts
            # by the manifests' reverted weeks; the battery's own pooled and no-revert members keep the call
            refused["take-up %s as a plug-in median lag" % m] = {"cc3": e["cc3"], "releases": e["points"]["releases"],
                                                                "own_share": e["own_share"], "call": call_list(e)}
            refused["calendar 2027's Mondays, take-up %s" % m] = {"cc3": c1}
            refused["calendar 2027's Mondays, take-up %s as a plug-in" % m] = {"cc3": c2}
            continue
        admitted["take-up %s as a plug-in median lag" % m] = e
        cal["calendar 2027's Mondays, take-up %s" % m] = c1
        cal["calendar 2027's Mondays, take-up %s as a plug-in" % m] = c2
    return admitted, cal, mism, refused


def run(target=None, quiet=True):
    target = target or os.path.join(TASK, "target")
    pk = L.pack(target)
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        A = C.analyse(pk, None)
    g = A["gold"]
    wt = pk.w["merch"] / pk.w["merch"].sum()
    bw = lambda v: float((wt * np.asarray(v)).sum())

    # the rivals the cut pack adds to the core's battery
    panel116 = np.array([np.sum(~np.isnan(pk.z[f][:, 116])) * 5.0 for f in range(C.F)])
    extra = {"families weighted by the panel at the latest snapshot, times five": C.evaluate(with_weights(pk, panel116)),
             "merchants' own change from the 2026 snapshot pairs only": C.evaluate(with_d13(pk, snapshot_d13(pk)))}
    # ruled out by named data: before each family's settled weeks the manifests show cold restarts and the change
    # calendar's three rollouts, model-side movement the 2026 sources as they stood do not hold
    ruled = {"merchants' own change over every thirteen-week gap from July 2024":
             C.evaluate(with_d13(pk, all_weeks_d13(pk)))}
    pre_gap = np.array([np.nanmean((pk.z[f][:, 13:pk.t0[f]] - pk.z[f][:, :pk.t0[f] - 13]) ** 2) for f in range(C.F)])
    mess = {}
    for m in L.MESS:
        mess[m] = C.evaluate(L.pack(target, mess=(m,)))
    fam = A["fam"] + list(extra.values())
    admitted, cal_cc3, mism, refused_takeup = forks(pk)
    lat = A["lattice"]
    routes = A["routes"]
    cut8 = C.evaluate(pk, S2="cut", cut_lag=8)
    free = A["free"]
    refused_e = list(lat.values()) + list(routes.values()) + list(A["extra"].values()) + [
        cut8, free, C.evaluate(pk, S2="over"), C.evaluate(pk, S2="over2"), C.evaluate(pk, S3="worst"),
        C.evaluate(pk, S3="y2026"), C.evaluate(pk, S1="flat"), C.evaluate(pk, S1="single"),
        C.evaluate(pk, weights="equal")]

    keys = ["points_" + s for s in C.SOURCES] + ["share_" + s for s in C.SOURCES] + ["cc3", "own_share",
                                                                                   "fr_sched", "fr_removed"]
    bands, adm_range = {}, {}
    for k in keys:
        vals = [e[k] for e in fam] + [g[k]] + [e[k] for e in admitted.values()]
        if k == "cc3":
            vals += list(cal_cc3.values())
        lo, hi = min(vals), max(vals)
        adm_range[k] = [lo, hi]
        bands[k] = [lo - 0.25 * (hi - lo), hi + 0.25 * (hi - lo)]
        # an edge stops halfway to the nearest figure a refused route, a lost stump or a ruled-out probe files
        ref = [e[k] for e in refused_e]
        if k == "own_share":
            ref += list(mism.values())
        below, above = [v for v in ref if v < lo - 1e-9], [v for v in ref if v > hi + 1e-9]
        if below:
            bands[k][0] = max(bands[k][0], 0.5 * (max(below) + lo))
        if above:
            bands[k][1] = min(bands[k][1], 0.5 * (min(above) + hi))
    for s, kind in (("retunes", "retune_shadow"), ("labels", "label_freeze")):
        sr = single_runs(pk, kind)
        bands["points_" + s] = [min(bands["points_" + s][0], min(sr)), max(bands["points_" + s][1], max(sr))]
    bands["cc1"], bands["cc2"] = bands["points_turnover"], bands["points_optimisation"]

    reflex = lat["S1+S2+S3"]
    direct = routes["direct"]
    fals = A["fals"]

    # counts and bases for the Step-by-Step
    raw = L.load(target, mess=("no_rekey",))[0]
    import pandas as pd
    reg = pd.read_csv(os.path.join(target, "mrm_instrument_pair_register_2026.csv"))
    nruns = sum(1 for _ in open(os.path.join(target, "training_scheduler_runs_2024_2026.jsonl")))
    m = C.coverage_model(pk.w, "loglin")
    loo = {}
    for name in ("runtime", "warm", "amp"):
        mdl = C.coverage_model(pk.w, "loglin", leave=name)
        r = pk.w[name]
        obs, pred = [], []
        for f in range(C.F):
            d = r["declared"][f]
            span = np.arange(d, d + 39)
            on = (span >= r["eff"][f]) & ~((span >= r["revert"][f, 0]) & (span < r["revert"][f, 1]))
            obs.append(on.mean())
            pred.append(float(np.mean(C.lognormal_cdf(span - d, mdl["mu"][f], mdl["sg"]) * (1 - mdl["rev"]))))
        loo[name] = {"record": float(np.mean(obs)), "model": float(np.mean(pred))}
    past = C.past_adoption(pk.w)
    lags = np.array([r[5] - r[4] for r in past])
    probe = {"thirteen of 52 weeks for every family": C.evaluate(pk, S1="flat")["points"]["turnover"],
             "the rows that entered only": C.evaluate(pk, S1="single")["points"]["turnover"],
             "every family counted once": C.evaluate(pk, weights="equal")["points"]["turnover"],
             "2026's release level carried": C.evaluate(pk, S3="y2026")["points"]["releases"],
             "each family's worst past lag": C.evaluate(pk, S3="worst")["points"]["releases"],
             "line through gaps 8 to 26": cut8["points"]["optimisation"],
             "unanchored fit": free["points"]["optimisation"],
             "unanchored implied replicate": bw(free["A"] * (1 - free["phi"] ** 2)),
             "a whole replicate pair a refit": C.evaluate(pk, S2="over2")["points"]["optimisation"],
             "thirteen refits added up": C.evaluate(pk, S2="over")["points"]["optimisation"],
             "feature releases as the mean of the four pairs' root-mean-square": pair_mean_rms(pk, g),
             "merchants' own change as a share of the record's own movement":
                 100.0 * g["own"] / float((pk.w["merch"] * pk.d13).sum() / pk.w["merch"].sum())}

    rel26 = pk.inst["rel"] * np.array([pk.events[f][C.H - 1, 1] for f in range(C.F)])
    side26 = (reflex["opt13"] + reflex["tur"] + pk.inst["ret"] * C.H / 4.0 + pk.inst["lab"] * C.H + rel26)
    unfloored = bw(pk.d13 - side26)
    reflex_floor = {"families_floored": int(np.sum(pk.d13 - side26 < 0)), "model_side_2026": bw(side26),
                    "own_share_unfloored": 100.0 * unfloored / (unfloored + sum(reflex["agg"].values()))}
    allv = fam + list(admitted.values())
    near = min(((abs(e["points"][s] - l), NAMES[s], e["points"][s], l) for e in allv for s in C.SOURCES
                for l in C.LINES), key=lambda x: x[0])
    d0 = dt.date(2024, 7, 1)
    when = lambda t: "%d %s" % ((d0 + dt.timedelta(weeks=int(t))).day, (d0 + dt.timedelta(weeks=int(t))).strftime("%B %Y"))
    fig = {
        "call": call_list(g),
        "points": {NAMES[s]: g["points"][s] for s in C.SOURCES},
        "share": {NAMES[s]: g["share"][s] for s in C.SOURCES},
        "band_of": call_of(g),
        "bands": {k: v for k, v in bands.items()},
        "cc1": g["cc1"], "cc2": g["cc2"], "cc3": g["cc3"], "own_share": g["own_share"],
        "fr_sched": g["fr_sched"], "fr_removed": g["fr_removed"],
        "fr26": 100.0 * bw(pk.fr26),
        "reflex": {"points": {NAMES[s]: reflex["points"][s] for s in C.SOURCES},
                   "share": {NAMES[s]: reflex["share"][s] for s in C.SOURCES}, "cc3": reflex["cc3"],
                   "own_share": reflex["own_share"], "fr_sched": reflex["fr_sched"], "fr_removed": reflex["fr_removed"],
                   "call": call_list(reflex), **reflex_floor},
        "direct": {"points": {NAMES[s]: direct["points"][s] for s in C.SOURCES}, "cc3": direct["cc3"],
                   "call": call_list(direct)},
        "rigorous": {"points": {NAMES[s]: routes["rigorous"]["points"][s] for s in C.SOURCES},
                     "cc3": routes["rigorous"]["cc3"]},
        "lattice": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES}, "call": call_list(e), "cc3": e["cc3"],
                        "own_share": e["own_share"]} for k, e in lat.items()},
        "routes": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES}, "call": call_list(e)}
                   for k, e in list(routes.items()) + list(A["extra"].items())},
        "over": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES}, "call": call_list(e)}
                 for k, e in A["over"].items()},
        "variants": len(fam), "variants_core": len(A["fam"]), "variants_all": len(fam) + len(admitted),
        "fit_grid": [0.50, 0.985, 0.0025],
        "battery_range": {NAMES[s]: [min(e["points"][s] for e in fam), max(e["points"][s] for e in fam)]
                          for s in C.SOURCES},
        "battery_cc3": [min(e["cc3"] for e in fam), max(e["cc3"] for e in fam)],
        "battery_calls": sorted(set(tuple(call_list(e)) for e in fam)) == [tuple(call_list(g))],
        "extra": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES}, "own_share": e["own_share"],
                      "cc3": e["cc3"], "fr_sched": e["fr_sched"], "fr_removed": e["fr_removed"],
                      "call": call_list(e)} for k, e in extra.items()},
        "cc3_rivals": cc3_rivals(pk, g),
        "forks": {"admitted": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES},
                                   "share": {NAMES[s]: e["share"][s] for s in C.SOURCES}, "own_share": e["own_share"],
                                   "cc3": e["cc3"], "fr_sched": e["fr_sched"], "fr_removed": e["fr_removed"],
                                   "call": call_list(e)} for k, e in admitted.items()},
                  "calendar_cc3": cal_cc3, "own_share_mismatched_weeks": mism, "refused_takeup": refused_takeup,
                  "admitted_range": adm_range,
                  "calls_hold": all(call_list(e) == call_list(g) for e in admitted.values())},
        "nearest_line": {"source": near[1], "points": near[2], "line": near[3], "gap": near[0]},
        "settled_floor": {"week": 66, "date": when(66), "weeks": C.T - 66},
        "assessment_weeks": {"first": when(C.Y27), "last": when(181), "refreshes": int(181 - C.Y27 + 1)},
        "ruled": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES}, "own_share": e["own_share"],
                      "call": call_list(e)} for k, e in ruled.items()},
        "pre_settled": {"d13_before": bw(pre_gap), "d13_settled": bw(pk.d13),
                        "families_higher": int(np.sum(pre_gap > pk.d13)),
                        "ratio_range": [float(np.min(pre_gap / pk.d13)), float(np.max(pre_gap / pk.d13))]},
        "mess": {k: {"points": {NAMES[s]: e["points"][s] for s in C.SOURCES}, "own_share": e["own_share"],
                     "cc3": e["cc3"], "fr_sched": e["fr_sched"], "fr_removed": e["fr_removed"],
                     "share": {NAMES[s]: e["share"][s] for s in C.SOURCES}} for k, e in mess.items()},
        "probe": probe,
        "falsification": {"record": fals["truth"], "golden": fals["golden"], "rivals": fals["rivals"]},
        "loo": loo,
        "base": {
            "panel_merchants": int(pk.w["ms"].sum()), "panel_merchants_unmapped": int(raw["ms"].sum()),
            "score_rows": int(sum(int(np.sum(~np.isnan(Z))) for Z in pk.z)),
            "manifest_lines": nruns, "manifest_runs": len({json.loads(x)["run_id"] for x in
                                                           open(os.path.join(target, "training_scheduler_runs_2024_2026.jsonl"))}),
            "families": C.F,
            "production_runs": C.F * C.T,
            "pairs": len(reg), "pairs_by_kind": {k: int(v) for k, v in reg["pair_kind"].value_counts().items()},
            "long_window_families": int(np.sum(pk.w["window"] == 104)),
            "replicate": bw(pk.inst["rep"]), "bootstrap_raw": bw(pk.inst["boot"]), "bootstrap_net": bw(g["face"]),
            "d13": bw(pk.d13), "d1": bw(pk.d1),
            "phi_fit": [float(min(g["phi"])), float(max(g["phi"]))],
            "turned_share_2027": [float(x) for x in [min(g["tur"] / np.maximum(g["face"], 1e-9)),
                                                    max(g["tur"] / np.maximum(g["face"], 1e-9))]],
            "slip_mean": float(m["slip"]), "revert_share": float(m["rev"]),
            "past_family_rollouts": len(past), "past_lag_median": float(np.median(lags)),
            "past_lag_range": [int(lags.min()), int(lags.max())],
            "lag_median_custom0": float(math.exp(m["mu"][int(np.argmin(pk.w["custom"]))])),
            "lag_median_custom_max": float(math.exp(m["mu"][int(np.argmax(pk.w["custom"]))])),
            "custom_max": int(pk.w["custom"].max()),
            "releases_2026": int(np.sum(pk.w["rel_weeks"] >= C.Y26)), "releases_before": int(np.sum(pk.w["rel_weeks"] < C.Y26)),
            "releases_2027": int(len(pk.w["plan_weeks"])),
            "cov_plan": direct["cc3"], "cov_declared": routes["rigorous"]["cc3"],
        },
    }
    E = effort(fig, g, A, pk, lat, routes, fam, extra, bands)
    fig["rubric"] = rubric(A["spec"])
    import writeup
    fig["stated"] = writeup.stated(fig)
    fig["rubric_stated"] = rubric(stated_spec(A["spec"], fig["stated"]))
    fig["panel_merchants"] = fig["base"]["panel_merchants"]
    fig["weekly_check"] = fig["falsification"]["golden"]
    fig["cap"] = 12
    fig["windows"] = sorted(set(int(x) for x in pk.w["window"]))
    fig["loo_pct"] = {k: [100 * v["record"], 100 * v["model"]] for k, v in fig["loo"].items()}
    fig["lines"] = list(C.LINES)
    return pk, A, fig, E


def stated_spec(spec, S):
    """The core's pricing spec with every figure's band set to the band the answer blocks state."""
    spec = copy.deepcopy(spec)
    key = {"CC1 turnover alone, points": "points_turnover", "CC2 optimisation noise alone, points": "points_optimisation",
           "CC3 share of 2027 retrains on pinned views": "cc3", "pinned views share, on its own ask line": "cc3",
           "merchants' own share of all movement": "own_share", "2027 flip rate as scheduled": "fr_sched",
           "2027 flip rate with the designated sources removed": "fr_removed"}
    for s in C.SOURCES:
        key["%s points, on its line" % s] = "points_" + s
        key["share %s" % s] = "share_" + s
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
        if line.startswith("| ") and "| wrong |" in line or "| right |" in line:
            parts = [p.strip() for p in line.strip("|").split("|")]
            if len(parts) == 3 and parts[2].isdigit():
                got[parts[0]] = int(parts[2])
    return {"verdict": txt.strip().splitlines()[-1], "exit": rc, "routes": got}


def effort(fig, g, A, pk, lat, routes, fam, extra, bands):
    reflex = lat["S1+S2+S3"]
    direct = routes["direct"]
    pts = lambda e, s: e["points"][s]
    tbl = lambda e: {NAMES[s]: round(e["share"][s], 2) for s in C.SOURCES}
    share_bands = {NAMES[s]: bands["share_" + s] for s in C.SOURCES}
    share_bands["merchants' own"] = bands["own_share"]
    sh = lambda e: dict(tbl(e), **{"merchants' own": round(e["own_share"], 2)})
    r9 = lambda e: {"tier changes 2027": round(e["fr_sched"], 2),
                    "with the designated sources removed": round(e["fr_removed"], 2)}
    r9_bands = {"tier changes 2027": bands["fr_sched"], "with the designated sources removed": bands["fr_removed"]}
    r2 = lambda e: {"retunes points": round(e["points"]["retunes"], 3), "retunes share": round(e["share"]["retunes"], 2),
                    "label revisions points": round(e["points"]["labels"], 3),
                    "label revisions share": round(e["share"]["labels"], 2)}
    r2_bands = {"retunes points": bands["points_retunes"], "retunes share": bands["share_retunes"],
                "label revisions points": bands["points_labels"], "label revisions share": bands["share_labels"]}
    r5 = lambda e: {"pinned views share": round(e["cc3"], 2), "feature releases": round(e["points"]["releases"], 3)}
    fals = A["fals"]
    res = [
        {"id": "R1", "name": "the panel on one merchant key and one family scheme", "graded_as": "Step-by-Step",
         "figure": "panel_merchants", "depends": [], "independent": "",
         "golden": fig["base"]["panel_merchants"], "band": [fig["base"]["panel_merchants"]] * 2,
         "passes": {"quick": fig["base"]["panel_merchants_unmapped"], "careful": fig["base"]["panel_merchants"],
                    "thorough": fig["base"]["panel_merchants"]}},
        {"id": "R2", "name": "the retunes and label revisions lines: points and share", "graded_as": "Ask 1",
         "figure": "r2", "depends": ["R1"], "independent": "the retune shadows and freeze pairs",
         "golden": r2(g), "bands": r2_bands, "partly_share": 1.0,
         "passes": {"quick": r2(direct), "careful": r2(reflex), "thorough": r2(g)},
         "precedent": ["L11", "L63"]},
        {"id": "R3", "name": "what training data alone moves a score between snapshots in 2027",
         "graded_as": "Component 1, Ask 1", "figure": "cc1", "depends": ["R1"],
         "independent": "the bootstrap pairs and the manifests' windows and rows",
         "golden": g["cc1"], "band": bands["cc1"],
         "passes": {"quick": pts(direct, "turnover"), "careful": pts(reflex, "turnover"), "thorough": g["cc1"]},
         "precedent": ["L28", "L22", "N21"]},
        {"id": "R4", "name": "what optimisation noise alone moves a score between snapshots",
         "graded_as": "Component 2, Ask 1", "figure": "cc2", "depends": ["R1"],
         "independent": "the change-by-gap curve and the replicate pairs",
         "golden": g["cc2"], "band": bands["cc2"],
         "passes": {"quick": pts(direct, "optimisation"), "careful": pts(reflex, "optimisation"), "thorough": g["cc2"]},
         "precedent": ["L39", "N44", "L28"]},
        {"id": "R5", "name": "the share of 2027's retrains on pinned views and what feature releases move",
         "graded_as": "Component 3, Ask 2, Ask 1", "figure": "r5", "depends": ["R1"],
         "independent": "the manifests' runtime fields for the past rollouts",
         "golden": r5(g), "bands": {"pinned views share": bands["cc3"], "feature releases": bands["points_releases"]},
         "passes": {"quick": r5(direct), "careful": r5(reflex), "thorough": r5(g)},
         "precedent": ["L46", "N03", "N22"]},
        {"id": "R6", "name": "each route's model asked for the weekly score-change variance",
         "graded_as": "Step-by-Step", "figure": "weekly_check", "depends": ["R3", "R4", "R5"],
         "independent": "", "golden": fals["golden"], "band": [fals["truth"] - 1.0, fals["truth"] + 1.0],
         "passes": {"quick": fals["rivals"]["both at face value"], "careful": fals["rivals"]["both at face value"],
                    "thorough": fals["golden"]},
         "precedent": ["L28"]},
        {"id": "R7", "name": "each source's share and merchants' own share", "graded_as": "Ask 1",
         "figure": "r7", "depends": ["R3", "R4", "R5"], "independent": "",
         "golden": sh(g), "bands": share_bands, "partly_share": 0.5,
         "passes": {"quick": sh(direct), "careful": sh(reflex), "thorough": sh(g)},
         "precedent": ["N21", "L46"]},
        {"id": "R8", "name": "each source's band for 2027", "graded_as": "Recommendation",
         "figure": "call", "depends": ["R3", "R4", "R5"], "independent": "",
         "golden": call_list(g),
         "passes": {"quick": call_list(direct), "careful": call_list(reflex), "thorough": call_list(g)},
         "precedent": ["L63", "L11"]},
        {"id": "R9", "name": "the merchants expected to change tier between snapshots in 2027", "graded_as": "Ask 3",
         "figure": "r9", "depends": ["R3", "R4", "R5", "R8"], "independent": "",
         "golden": r9(g), "bands": r9_bands, "partly_share": 1.0,
         "passes": {"quick": r9(direct), "careful": r9(reflex), "thorough": r9(g)},
         "precedent": ["L63", "L11"]},
    ]
    fig["r2"], fig["r5"], fig["r7"], fig["r9"] = r2(g), r5(g), sh(g), r9(g)
    spec = A["spec"]
    hints = [{"sentence": spec["stumps"][k]["said_out_loud"], "rescues": [r]} for k, r in
             (("S1", "R3"), ("S2", "R4"), ("S3", "R5"))]
    single = {"S1": lat["S1"], "S2": lat["S2"], "S3": lat["S3"]}
    alone = {"S1": lat["S2+S3"], "S2": lat["S1+S3"], "S3": lat["S1+S2"]}
    moved = lambda e: [r["id"] for r in res[1:] if _moved(r, e, g, bands)]
    fact = {"golden_answer": call_list(g), "reflex_route": {"answer": call_list(reflex)},
            "judgments": [
                {"id": k, "name": spec["stumps"][k]["said_out_loud"], "kind": "stump",
                 "precedent": spec["stumps"][k]["precedents"],
                 "dropped": {"answer": call_list(single[k]), "results_moved": moved(single[k])},
                 "alone": {"answer": call_list(alone[k]), "results_rescued": [{"S1": "R3", "S2": "R4", "S3": "R5"}[k]]}}
                for k in ("S1", "S2", "S3")] + [
                {"id": "J4", "name": "each instrument's pair variance by family, book weighted", "kind": "reflex",
                 "precedent": ["R20"]},
                {"id": "J5", "name": "retunes and label revisions scaled by their counts between two snapshots",
                 "kind": "reflex", "precedent": ["R20"]},
                {"id": "J6", "name": "merchants' own change as the remainder of the record's thirteen-week movement",
                 "kind": "reflex", "precedent": ["R93"]},
                {"id": "J7", "name": "re-sent refreshes, re-keyed merchants and the two family code schemes resolved",
                 "kind": "reflex", "precedent": ["R01"]}]}
    forcing = {"kind": "set", "golden_answer": call_list(g),
               "golden_family": [{"name": str(v) or "the golden", "answer": call_list(e)}
                                 for v, e in zip(A["variants"], A["fam"])] +
                                [{"name": k, "answer": call_list(e)} for k, e in extra.items()],
               "shortcuts": [{"name": k, "answer": call_list(e)} for k, e in list(lat.items())
                             if k != "golden"] + [{"name": k, "answer": call_list(e)} for k, e in routes.items()],
               "perturbations": _perturb(g)}
    route_list = [{"name": "the golden", "answer": call_list(g), "golden": True}] + \
        [{"name": "stumps lost: " + k, "answer": call_list(e)} for k, e in lat.items()] + \
        [{"name": k, "answer": call_list(e)} for k, e in list(routes.items()) + list(A["extra"].items())]
    return {"results": res, "hints": hints, "factorial": fact, "forcing": forcing, "routes": route_list,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}


def _moved(r, e, g, bands):
    if r["id"] == "R6":     # each single drop fails the check: S1 at 270.43, S2 at 50.92, S3 at the calendar's 1.000
        return True
    if r["id"] == "R8":
        return call_list(e) != call_list(g)
    key = {"R2": ["points_retunes", "share_retunes", "points_labels", "share_labels"],
           "R3": ["points_turnover"], "R4": ["points_optimisation"], "R5": ["cc3", "points_releases"],
           "R7": ["share_" + s for s in C.SOURCES] + ["own_share"],
           "R9": ["fr_sched", "fr_removed"]}[r["id"]]
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
    print(json.dumps({k: fig[k] for k in ("call", "points", "share", "cc3", "own_share", "fr_sched", "fr_removed",
                                          "fr26", "variants", "battery_calls", "battery_range", "extra", "probe",
                                          "falsification", "loo", "base", "rubric")}, indent=1, default=float))
    print(json.dumps(fig["bands"], indent=0, default=float))
    print(json.dumps(fig["mess"], indent=0, default=float))
