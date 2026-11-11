"""The golden, computed from the cut pack alone (panel.from_pack), with every rival the fork table licenses run on
the same pack to set each figure's band, and the named shortcuts for the effort passes.

compute(target) returns {"golden": results, "rivals": {...}, "routes": {...}, "bands": {...}, "plan": ...}."""
import json
import os

import numpy as np

import docs
import models
import panel
import params as P
import results
import routes
import world

PREC = {"R1": 1, "R2": 1, "R3": 0.001, "R4": 0.001, "R5": 0.001, "R6": 1, "R7": 1, "R9": 1}
RIVAL_PANELS = {"reading over the first two months": dict(months=2),
                "reading against the month's average": dict(adjust=True)}


def plan_cost(plan):
    spend = docs.plan_spend(plan)
    return ({l: sum(spend[l]) for l in plan}, {l: sum(spend[l]) / sum(plan[l]["starts"]) for l in plan})


def funded(values, cost_per_start):
    return sorted(l for l in values if values[l] / cost_per_start[l] >= P.HURDLE)


def run_route(pn, plan, o):
    R, M = results.all_results(pn, plan, o)
    return R


def resampled(pn, plan, cps, golden_set):
    """The forcing check: whole start months drawn again within each line (boot.py), every model refitted; each
    line's multiple at the 5th and 95th percentile of the draws and the number of draws funding the same lines."""
    import boot
    vals = boot.run(pn, plan, P.BOOT_REPS, seed=P.SEED + 13)
    mult = {l: np.array([v[l] / cps[l] for v in vals]) for l in plan}
    same = sum(1 for v in vals if funded(v, cps) == golden_set)
    return {"reps": len(vals), "same": int(same),
            "lo": {l: float(np.percentile(mult[l], 5)) for l in plan},
            "hi": {l: float(np.percentile(mult[l], 95)) for l in plan}}


def newest_own(pn):
    """What a calibration of each line on its own newest starts would rest on: the full-price cancellations so far
    of the line's starts of the twelve months to the cut, against what the golden's leaving model expects of them."""
    import sim
    M = models.fit_hazard(pn, models.GOLD)
    out = {}
    for (c, t) in P.LINES:
        ci, tj = sim.C_IDX[c], sim.T_IDX[t]
        sel = ((pn["channel"] == ci) & (pn["title"] == tj) & (pn["kind"] == "new") & ~pn["withdrawn"]
               & (pn["start"] > P.CUT - 12) & (pn["stepup"] <= P.CUT - 1) & (pn["last"] >= pn["stepup"]))
        O, E = 0, 0.0
        for i in np.where(sel)[0]:
            a, b = pn["stepup"][i], min(pn["last"][i], P.CUT - 1)
            mm = np.arange(a, b + 1)
            if not np.isnan(pn["proxy"][i]):
                E += float(models.hazard(M, np.full(len(mm), ci), mm - a + 1, np.full(len(mm), pn["proxy"][i]), mm,
                                         np.full(len(mm), tj)).sum())
            O += int((a <= pn["end"][i] <= b) and pn["reason"][i] == "CANCELLED")
        out[(c, t)] = (O, E)
    return out


def compute(target, with_rivals=True, with_routes=True, with_boot=False):
    pn = panel.from_pack(target)
    plan = world.plan_2027()
    spend, cps = plan_cost(plan)
    out = {"plan": plan, "spend": spend, "cps": cps}
    out["golden"] = run_route(pn, plan, models.GOLD)
    out["golden"]["R8"] = funded(out["golden"]["R7"], cps)
    out["golden"]["budget"] = int(sum(spend[l] for l in out["golden"]["R8"]))
    if with_rivals:
        riv = {}
        for nm in routes.RIVALS:
            riv[nm] = run_route(pn, plan, routes.route(nm))
        for nm, kw in RIVAL_PANELS.items():
            riv[nm] = run_route(panel.from_pack(target, **kw), plan, models.GOLD)
        for nm in riv:
            riv[nm]["R8"] = funded(riv[nm]["R7"], cps)
        out["rivals"] = riv
        out["bands"] = bands(out["golden"], riv)
    if with_routes:
        rt = {}
        for nm in ["careful"] + list(routes.SINGLE) + list(routes.PAIRS):
            rt[nm] = run_route(pn, plan, routes.route(nm))
            rt[nm]["R8"] = funded(rt[nm]["R7"], cps)
        out["routes"] = rt
    if with_boot:
        out["boot"] = resampled(pn, plan, cps, out["golden"]["R8"])
    out["newest_own"] = newest_own(pn)
    out["n_households"] = int(len(set(pn["household"])))
    out["n_plan_starts"] = {c: int(sum(sum(s["starts"]) for (cc, t), s in plan.items() if cc == c)) for c in P.PAID}
    out["quick"] = quick(pn, plan, cps, target)
    return out


def quick(pn, plan, cps, target):
    """Ten minutes: the obvious file and the first account that fits."""
    import csv
    import sim
    q = {}
    # R1: every exported row charged for October 2026
    cnt = {t: 0 for t in P.TITLES}
    oct_rows = set()
    with open(os.path.join(target, "price_periods_2023-01_2026-10.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r["valid_to"] == "" or r["valid_to"] >= "2026-10-31") and r["valid_from"] <= "2026-10-31" \
                    and float(r["monthly_price_eur"]) > 0:
                oct_rows.add(r["subscription_id"])
    with open(os.path.join(target, "subscriptions_2023-01_2026-10.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["subscription_id"] in oct_rows:
                cnt[r["title"]] += 1
    q["R1"] = cnt
    net = results.net_matrix(pn)
    # R2 and R7: each start's own subscription, realised
    q["R2"] = {}
    for c in P.CHANNELS:
        sel = np.isin(pn["start"], results.R2_MONTHS) & (pn["kind"] == "new") & ~pn["withdrawn"] & (
            pn["channel"] == sim.C_IDX[c])
        idx = np.where(sel)[0]
        q["R2"][c] = float(np.mean([net[i, pn["start"][i]: pn["start"][i] + 36].sum() for i in idx]))
    q["R7"] = {}
    for (c, t) in plan:
        sel = (pn["start"] <= 9) & (pn["kind"] == "new") & ~pn["withdrawn"] & (pn["channel"] == sim.C_IDX[c]) & (
            pn["title"] == sim.T_IDX[t])
        idx = np.where(sel)[0]
        q["R7"][(c, t)] = float(np.mean([net[i, pn["start"][i]: pn["start"][i] + 36].sum() for i in idx]))
    q["R8"] = funded(q["R7"], cps)
    # R3: each offer's share leaving at the end of the intro, over everything on file
    idx, y = models.su_rows(pn)
    q["R3"] = {code: float(y[pn["offer"][idx] == sim.O_IDX[code]].mean()) for code in sim.OFFER_CODES}
    q["R4"] = {code: 0.0 for code in sim.OFFER_CODES}
    # R5: the starts of three years earlier, as they turned out
    q["R5"] = {}
    for c in P.CHANNELS:
        sel = (pn["start"] <= 9) & (pn["kind"] == "new") & ~pn["withdrawn"] & (pn["channel"] == sim.C_IDX[c])
        idx = np.where(sel)[0]
        q["R5"][c] = float(np.mean(pn["gross"][idx, pn["start"][idx] + results.R5_AT] > 0))
    q["R6"] = {t: 0.0 for t in P.TITLES}
    # R9: each channel's planned starts times the share that stays at the end of the intro, on everything on file
    stay = 1 - y.mean()
    q["R9"] = {c: float(stay * sum(sum(s["starts"]) for (cc, t), s in plan.items() if cc == c)) for c in P.PAID}
    q["budget"] = int(sum(sum(docs.plan_spend(plan)[l]) for l in q["R8"]))
    return q


def bands(g, riv):
    """Each figure's band: the golden and every rival, widened by half the figure's printed unit."""
    out = {}
    for r, u in PREC.items():
        out[r] = {}
        for k, v in g[r].items():
            vals = [v] + [riv[n][r][k] for n in riv]
            out[r][k] = (min(vals) - u / 2, max(vals) + u / 2)
    return out


def rounded(r, v):
    u = PREC[r]
    if u == 1:
        return int(round(v))
    return round(v, 3)


def key(k):
    return "%s-%s" % k if isinstance(k, tuple) else k
