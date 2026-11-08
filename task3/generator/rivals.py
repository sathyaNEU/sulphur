"""task3 architecture 4: every rung of the ladder and every rival of the fork table, run on the cut pack through
solve.py with one switch changed, written to generator/rungs.json for checks.py, ceiling.py and the write-up."""
import json
import math

import numpy as np

import params as P
import solve as S

# the standing family: every defensible construction of the golden
STANDING = [
    ("golden", {}),
    ("no_anchor", {"anchor": False}),
    ("delay_origin", {"delay": "origin"}),
    ("delay_origin_noanchor", {"delay": "origin", "anchor": False}),
    ("arrival_step", {"rule": "step"}),
    ("arrival_step_noanchor", {"rule": "step", "anchor": False}),
    ("no_age", {"age": False}),
    ("smooth0", {"smooth": 0}),
    ("smooth2", {"smooth": 2}),
    ("tail3", {"tail": 3}),
    ("tail8", {"tail": 8}),
    ("nd_zero", {"nd": "zero"}),
    ("nd_full", {"nd": "full"}),
    ("leach_cohort", {"leach_from": "cohort"}),
    ("leach_cohort_noanchor", {"leach_from": "cohort", "anchor": False}),
    ("leachtime_noanchor", {"weight": "leach", "anchor": False}),
]
# the shallow forms of the second judgments (the deep step taken)
SECOND = [
    ("area_weights", {"flux": False}),
    ("area_weights_noanchor", {"flux": False, "anchor": False}),
    ("leachtime_anchored", {"weight": "leach"}),
    ("leach_all_years", {"tail": "all"}),
    ("area_and_all_years", {"flux": False, "tail": "all"}),
    ("history_shares", {"share": P.HIST_SHARE}),
    ("arrival_quarter", {"rule": "quarter"}),
    ("arrival_threequarter", {"rule": "3q"}),
]
# the wrong rungs: the clearing's effect fitted to the wells' 2019-2026 record under a delay that puts it before 2026
RUNGS = [
    ("rung1_gw_travel_time", {"delay": "none"}),
    ("rung1_pooled_cohort_delay", {"delay": "pooled"}),
    ("rung1_single_lag", {"delay": "lag", "lag": None}),
]


def ft(x):
    return int(math.floor(x + 0.5))


def summarise(r):
    hi = max(("W5", "W6", "W7", "W3"), key=lambda w: r["fc"][w][2034])
    return {"cross": r["cross"], "call": r["call"], "ep": {str(y): round(v, 3) for y, v in r["ep"].items()},
            "w2034": {w: round(r["fc"][w][2034], 3) for w in P.WELLS}, "hi_well": hi,
            "hi_2034": round(r["fc"][hi][2034], 3), "a": round(r["fit"]["a"], 4), "b": round(r["fit"]["b"], 5),
            "irv": round(r["curves"]["IRV"]["last"], 3), "irc": round(r["curves"]["IRC"]["last"], 3),
            "resid": {w: round(v, 3) for w, v in r["resid"].items()},
            "rmse": {w: round(v, 3) for w, v in r["rmse"].items()}}


def single_lag(target, D):
    """one lag for every parcel, fitted to the wells' 1998-2018 record (before any clearing could show)"""
    best = None
    for lag in np.arange(2.0, 14.01, 0.5):
        r = S.run(target, D=D, delay="lag", lag=float(lag), anchor=False)
        e = float(np.sqrt(np.mean([(r["obs"][w][y] - r["model"][w][y]) ** 2 for w in P.WELLS
                                   for y in range(1998, 2019) if y in r["obs"][w]])))
        if best is None or e < best[0]:
            best = (e, float(lag))
    return best[1], best[0]


def trend(target, D, kind="linear"):
    """each well's 2015-2026 annual means carried forward on their own trend, blended by the plan"""
    obs = D["well_annual"]
    fc = {}
    for w in P.WELLS:
        xs = np.array([y for y in range(2015, 2027) if y in obs[w]], float)
        ys = np.array([obs[w][int(y)] for y in xs])
        if kind == "sen":
            sl = [(ys[j] - ys[i]) / (xs[j] - xs[i]) for i in range(len(xs)) for j in range(i + 1, len(xs))]
            b = float(np.median(sl))
            a = float(np.median(ys - b * xs))
        else:
            b, a = np.polyfit(xs, ys, 1)
        fc[w] = {y: max(0.0, a + b * y) for y in P.FC_YEARS}
    ep = {y: sum(P.PLAN_SHARE[w] * fc[w][y] for w in P.WELLS) for y in P.FC_YEARS}
    cross = next((y for y in P.FC_YEARS if ep[y] >= P.LIMIT), None)
    hi = max(P.WELLS, key=lambda w: fc[w][2034])
    return {"cross": cross, "call": 2027 if (cross and cross < P.CYCLES[2031]) else 2031,
            "ep": {str(y): round(v, 3) for y, v in ep.items()}, "w2034": {w: round(fc[w][2034], 3) for w in P.WELLS},
            "hi_well": hi, "hi_2034": round(fc[hi][2034], 3)}


def main(target, out):
    D = S.read(target)
    res, full = {}, {}
    for name, o in STANDING + SECOND:
        r = S.run(target, D=D, **o)
        res[name] = summarise(r)
        if name == "golden":
            full["golden"] = r
    lag, lag_rmse = single_lag(target, D)
    for name, o in RUNGS:
        o = dict(o)
        if o.get("lag", 0) is None:
            o["lag"] = lag
        k = S.fit_k(target, D, **o)
        r = S.run(target, D=D, k=k, **o)
        res[name] = summarise(r)
        res[name]["k"] = k
        r1 = S.run(target, D=D, k=1.0, anchor=False, **o)
        res[name]["misfit_2026_k1"] = {w: round(r1["model"][w][2026] - r1["obs"][w][2026], 3) for w in ("W6", "W7")}
        sse = {}
        for kk in (0.0, 1.0):
            rr = S.run(target, D=D, k=kk, anchor=False, **o)
            sse[str(kk)] = round(sum((rr["obs"][w][y] - rr["model"][w][y]) ** 2 for w in ("W6", "W7")
                                     for y in range(2019, 2027)), 3)
        res[name]["sse_2019_2026"] = sse
    res["rung1_single_lag"]["lag"] = lag
    res["rung1_single_lag"]["lag_rmse_1998_2018"] = round(lag_rmse, 3)
    sse = {}
    for kk in (0.0, 1.0):
        rr = S.run(target, D=D, k=kk, anchor=False)
        sse[str(kk)] = round(sum((rr["obs"][w][y] - rr["model"][w][y]) ** 2 for w in ("W6", "W7")
                                 for y in range(2019, 2027)), 3)
    res["golden"]["sse_2019_2026"] = sse
    res["rung0_trend"] = trend(target, D)
    res["rung0_trend_sen"] = trend(target, D, "sen")
    res["rung2_dismissed"] = summarise(S.run(target, D=D, k=0.0))
    res["standing"] = [n for n, _ in STANDING]
    res["second"] = [n for n, _ in SECOND]
    json.dump(res, open(out, "w"), indent=1)
    return res, full
