"""Every owed figure from the cut pack's read-back, the golden family that sets each band, the named shortcuts, the
three passes and the stump factorial, written as figures.json and effort.json."""
import numpy as np

import analysis as A
import params as P
import verify as V

GOLD = dict(A.GOLD)
BASE = dict(cop=12100 / 4350, whkw=3200 / 8.76e6, quad=True, win=2, ctrl="class", tctl="class", comp=None, lam=1.0, lossk=1.0, room=0.0)
STUMPS = {
    1: ("J1", "the trial read on the volts its regulators actually took off, not on the day's assignment", ["N24", "L04"]),
    2: ("J2", "each untested feeder's response built from its own makeup, not the trial feeders' average", ["N25", "L15"]),
    3: ("J3", "the response carried through the year hour by hour, thermostatic load giving its energy back", ["N12", "L15"]),
    4: ("J4", "the volts each feeder can give hour by hour from its far-end meters, not the trial's 4 percent", ["N01", "L17"]),
    5: ("J5", "the change in line losses from current squared, not the annual report's 6.1 percent added in proportion", ["N21", "L22"]),
}
REFLEXES = [
    ("the customer-meter sums cleaned (re-sent rows, estimated intervals, the far-end meters' lowest reading)", []),
    ("daily energy regressed on the trial with weather and day-type terms against comparable untested feeders", []),
    ("energy at the substation, the 115 V floor and the 4.8 V cap, valued at USD 48 and 9.4 (filed in VO-1)", []),
]
RIVALS = {
    "a resistive home at 2.5 times a heat pump home's heating draw": dict(cop=2.5),
    "a resistive home at 3.2 times a heat pump home's heating draw": dict(cop=3.2),
    "the trial's weather terms without squares": dict(quad=False),
    "the trial's control every untested feeder, not the same class": dict(tctl="all"),
}


def J(*off):
    return {j: (j not in off) for j in GOLD}


def run(R, Jset, **kw):
    A.OPT.update(BASE)
    A.OPT.update(kw)
    A.reset()
    out = {}
    out["save"] = np.array([A.saving2(R, f, Jset) for f in range(P.NF)])
    out["vc"] = out["save"] * P.PRICE * P.ANNUITY / np.array(R.cost)
    out["set"] = tuple(int(f) for f in np.where(out["vc"] >= 1)[0])
    out["trial"] = {f: A.trial_effect(R, f, Jset[1]) for f in R.trial}
    out["room"] = np.array([A.headroom(R, f, Jset[4]).mean() for f in range(P.NF)])
    out["loss"] = np.array([loss_change(R, f, Jset) for f in range(P.NF)])
    return out


def loss_change(R, f, Jset):
    """MWh a year by which the feeder's own line losses fall under voltage optimization (negative: they rise)"""
    tot = A.saving2(R, f, Jset)
    j5 = dict(Jset)
    S = R.ami[f] * 4
    if Jset[2] or f in R.trial:
        eta = A.eta_structural(R, f, Jset)
        if not Jset[3]:
            sel = np.zeros(P.NQ, bool)
            for d in R.trial_days:
                sel[d * P.Q:(d + 1) * P.Q] = True
            eta = np.full(P.NQ, float((eta[sel] * S[sel]).sum() / S[sel].sum()))
    else:
        eta = np.full(P.NQ, float(np.mean([A.trial_effect(R, g, Jset[1]) for g in R.trial])))
    dvq = np.repeat(A.headroom(R, f, Jset[4]), 4) / P.VNOM
    cust = float((eta * dvq * S).sum() * 0.25)
    return tot - cust


def quick(R):
    """ten minutes: the export summed as it comes (re-sent rows in), the trial as ON days' mean energy over OFF days',
    the trial's 4.8 V on every feeder all year, the customer meters' saving taken as the substation's"""
    import os
    raw = np.zeros(P.NF)
    import csv
    for r in csv.DictReader(open(os.path.join(R.target, "mdm_feeder_interval_kwh_2026.csv"))):
        raw[R.ids.index(r["feeder_id"])] += float(r["kwh"])
    out = {"raw_mwh": raw / 1000.0}
    tr = {}
    for f in R.trial:
        E = R.ami[f].reshape(P.ND, P.Q).sum(axis=1)[R.trial_days]
        a = R.assign[f][R.trial_days]
        tr[f] = (1 - E[a == 1].mean() / E[a == 0].mean()) / (P.TRIAL_DV / P.VNOM)
    eta = float(np.mean(list(tr.values())))
    out["trial"] = tr
    out["room"] = np.full(P.NF, P.TRIAL_DV)
    out["save"] = np.array([eta * P.TRIAL_DV / P.VNOM * R.ami[f].sum() / 1000.0 for f in range(P.NF)])
    out["loss"] = np.zeros(P.NF)
    out["vc"] = out["save"] * P.PRICE * P.ANNUITY / np.array(R.cost)
    out["set"] = tuple(int(f) for f in np.where(out["vc"] >= 1)[0])
    return out


def energy_mwh(R):
    return np.array([R.ami[f].sum() / 1000.0 for f in range(P.NF)])


def _band(vals, rel, floor):
    lo, hi = min(vals), max(vals)
    w = max(rel * abs(np.mean(vals)), floor)
    return [round(lo - w, 2), round(hi + w, 2)]


def tmean(out, R):
    """the trial's response averaged over the trial feeders, each counted once"""
    return float(np.mean([out["trial"][f] for f in R.trial]))


def run_all(target):
    R = V.read_pack(target)
    ids = R.ids
    G = run(R, GOLD)
    riv = {nm: run(R, GOLD, **kw) for nm, kw in RIVALS.items()}
    C = run(R, J(1, 2, 3, 4, 5))                                    # the reflex route: every stump hurried
    drops = {j: run(R, J(j)) for j in GOLD}
    alone = {j: run(R, J(*[k for k in GOLD if k != j])) for j in GOLD}
    E = energy_mwh(R)
    fam = [G] + list(riv.values())
    bands = {
        "save": {ids[f]: _band([x["save"][f] for x in fam], 0.03, 8.0) for f in range(P.NF)},
        "room": {ids[f]: _band([x["room"][f] for x in fam], 0.02, 0.05) for f in range(P.NF)},
        "loss": {ids[f]: _band([x["loss"][f] for x in fam], 0.10, 3.0) for f in range(P.NF)},
        "trial": {ids[f]: _band([x["trial"][f] for x in fam], 0.04, 0.02) for f in R.trial},
        "trial_mean": _band([tmean(x, R) for x in fam], 0.02, 0.01),
    }
    fig = {
        "ids": ids, "trial": [ids[f] for f in R.trial], "headmetered": [ids[f] for f in R.headmetered],
        "kind": {ids[f]: R.kind[f] for f in range(P.NF)}, "cost": {ids[f]: R.cost[f] for f in range(P.NF)},
        "energy_mwh": {ids[f]: round(float(E[f]), 0) for f in range(P.NF)},
        "trial_effect": {ids[f]: round(float(G["trial"][f]), 2) for f in R.trial},
        "trial_mean": round(tmean(G, R), 2),
        "trial_mean_assigned": round(tmean(drops[1], R), 2),
        "break_even_mwh": {ids[f]: round(R.cost[f] / (P.PRICE * P.ANNUITY), 0) for f in range(P.NF)}, "vnom": P.VNOM,
        "largest_loss_rise_mwh": round(-float(min(G["loss"])), 0),
        "room_v": {ids[f]: round(float(G["room"][f]), 2) for f in range(P.NF)},
        "loss_mwh": {ids[f]: round(float(G["loss"][f]), 0) for f in range(P.NF)},
        "save_mwh": {ids[f]: round(float(G["save"][f]), 0) for f in range(P.NF)},
        "value_ratio": {ids[f]: round(float(G["vc"][f]), 2) for f in range(P.NF)},
        "funded": [ids[f] for f in G["set"]],
        "bands": bands,
        "routes": {"the careful route (the reflex route)": [ids[f] for f in C["set"]]},
        "price": P.PRICE, "annuity": P.ANNUITY, "loss_rate_report": P.LOSS_RATE_REPORT,
        "total_save_mwh": round(float(sum(G["save"][f] for f in G["set"])), 0),
        "total_cost": round(float(sum(R.cost[f] for f in G["set"])), 0),
    }
    for j, d in drops.items():
        fig["routes"]["%s dropped (%s)" % (STUMPS[j][0], STUMPS[j][1])] = [ids[f] for f in d["set"]]
    eff = effort(R, ids, G, C, drops, alone, riv, fig)
    return fig, eff


def effort(R, ids, G, C, drops, alone, riv, fig):
    b = fig["bands"]
    E = energy_mwh(R)

    def tab(vals, key, keys=None):
        keys = keys if keys is not None else range(P.NF)
        return {ids[f]: round(float(vals[f]), 2) for f in keys}
    Qk = quick(R)
    res = [
        {"id": "R1", "name": "each feeder's 2026 energy at the customer meters (MWh)", "graded_as": "Ask 1", "figure": "energy_mwh",
         "depends": [], "independent": "the customer-meter sums", "golden": fig["energy_mwh"],
         "bands": {k: [v - 2, v + 2] for k, v in fig["energy_mwh"].items()},
         "passes": {"quick": {ids[f]: round(float(Qk["raw_mwh"][f]), 0) for f in range(P.NF)}, "careful": fig["energy_mwh"], "thorough": fig["energy_mwh"]}},
        {"id": "R2", "name": "the trial's change in energy per 1 percent of voltage removed, averaged over the trial feeders",
         "graded_as": "Component 2", "figure": "trial_mean", "depends": [], "independent": "the trial records",
         "golden": fig["trial_mean"], "band": b["trial_mean"], "precedent": ["N24", "L04"],
         "passes": {"quick": round(float(np.mean([Qk["trial"][f] for f in R.trial])), 2),
                    "careful": round(tmean(C, R), 2), "thorough": fig["trial_mean"]}},
        {"id": "R3", "name": "the average reduction in volts each feeder could be held at over the year", "graded_as": "Ask 3",
         "figure": "room_v", "depends": [], "independent": "the far-end meters", "golden": fig["room_v"], "bands": b["room"],
         "precedent": ["N01", "L17"], "partly_share": 0.75,
         "passes": {"quick": tab(Qk["room"], "room"), "careful": tab(C["room"], "room"), "thorough": fig["room_v"]}},
        {"id": "R4", "name": "the change in each feeder's own line losses (MWh a year)", "graded_as": "Ask 4", "figure": "loss_mwh",
         "depends": ["R3"], "independent": "", "golden": fig["loss_mwh"], "bands": b["loss"], "precedent": ["N21", "L22"], "partly_share": 0.75,
         "passes": {"quick": tab(Qk["loss"], "loss"), "careful": tab(C["loss"], "loss"), "thorough": fig["loss_mwh"]}},
        {"id": "R5", "name": "each feeder's yearly energy saving at the substation (MWh)", "graded_as": "Component 1", "figure": "save_mwh",
         "depends": ["R2", "R3", "R4"], "independent": "", "golden": fig["save_mwh"], "bands": b["save"], "precedent": ["N25", "N12", "L15"],
         "partly_share": 0.75,
         "passes": {"quick": tab(Qk["save"], "save"), "careful": tab(C["save"], "save"), "thorough": fig["save_mwh"]}},
        {"id": "R6", "name": "the feeders that receive voltage optimization in 2027", "graded_as": "Recommendation", "figure": "funded",
         "depends": ["R5"], "independent": "", "golden": fig["funded"], "precedent": ["N25", "L15"],
         "passes": {"quick": [ids[f] for f in Qk["set"]], "careful": [ids[f] for f in C["set"]], "thorough": fig["funded"]}},
    ]
    byid = {r["id"]: r for r in res}

    def inb(out, key, rid, keys=None):
        r = byid[rid]
        vals = out[key]
        keys = keys if keys is not None else range(P.NF)
        return all(r["bands"][ids[f]][0] <= (vals[f]) <= r["bands"][ids[f]][1] for f in keys)

    def rescued(out):
        got = []
        lo, hi = byid["R2"]["band"]
        if lo <= tmean(out, R) <= hi:
            got.append("R2")
        for rid, key in (("R3", "room"), ("R4", "loss"), ("R5", "save")):
            if inb(out, key, rid):
                got.append(rid)
        if out["set"] == G["set"]:
            got.append("R6")
        return got

    def moved(out):
        return [r for r in ("R2", "R3", "R4", "R5", "R6") if r not in rescued(out)]
    judg = []
    for j, (jid, name, prec) in STUMPS.items():
        judg.append({"id": jid, "name": name, "kind": "stump", "precedent": prec,
                     "dropped": {"answer": [ids[f] for f in drops[j]["set"]], "results_moved": moved(drops[j])},
                     "alone": {"answer": [ids[f] for f in alone[j]["set"]], "results_rescued": rescued(alone[j])}})
    for i, (name, prec) in enumerate(REFLEXES, 6):
        judg.append({"id": "J%d" % i, "name": name, "kind": "reflex", "precedent": prec})
    hints = [{"sentence": STUMPS[j][1], "rescues": rescued(alone[j])} for j in STUMPS]
    pert = []
    for nm, kw in (("the trial-calibrated response 4.6 percent higher (twice its sampling error)", dict(lam=1.046)),
                   ("the trial-calibrated response 4.6 percent lower (twice its sampling error)", dict(lam=0.954)),
                   ("the loss coefficient 20 percent higher", dict(lossk=1.2)), ("the loss coefficient 20 percent lower", dict(lossk=0.8)),
                   ("the far-end readings 0.2 V higher", dict(room=0.2)), ("the far-end readings 0.2 V lower", dict(room=-0.2))):
        pert.append({"input": nm, "answer": [ids[f] for f in run(R, GOLD, **kw)["set"]]})
    fam = [{"name": "the golden", "answer": fig["funded"]}] + [{"name": nm, "answer": [ids[f] for f in r["set"]]} for nm, r in riv.items()]
    shortcuts = [{"name": "%s dropped" % STUMPS[j][0], "answer": [ids[f] for f in drops[j]["set"]]} for j in STUMPS]
    routes = [{"name": "the golden", "answer": fig["funded"], "golden": True},
              {"name": "the careful route (the reflex route)", "answer": [ids[f] for f in C["set"]]}] + \
             [{"name": "%s dropped" % STUMPS[j][0], "answer": [ids[f] for f in drops[j]["set"]]} for j in STUMPS] + \
             [{"name": "the quick route", "answer": [ids[f] for f in Qk["set"]]}]
    return {"results": res, "hints": hints,
            "factorial": {"golden_answer": fig["funded"], "reflex_route": {"answer": [ids[f] for f in C["set"]]}, "judgments": judg},
            "forcing": {"kind": "set", "golden_answer": fig["funded"], "golden_family": fam, "perturbations": pert, "shortcuts": shortcuts},
            "routes": routes, "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
