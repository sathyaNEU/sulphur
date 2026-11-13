"""Every owed figure from the cut pack's read-back, the golden family that sets each band, the named shortcuts, the
three passes and the stump factorial, written as figures.json and effort.json."""
import csv
import os

import numpy as np

import analysis as A
import params as P
import verify as V

GOLD = dict(A.GOLD)
BASE = dict(cop=None, whkw=None, quad=True, win=2, ctrl="class", tctl="class", lamstat="median", lossfit="origin", comp=None,
            lam=1.0, lossk=1.0, room=0.0)
# the judgments a careful run gets wrong in a hurry: the call turns on these
STUMPS = {
    2: ("J2", "each untested feeder's response built from its own makeup, not the trial feeders' average", ["N25", "L15"]),
    3: ("J3", "the response carried through the year hour by hour, thermostatic load giving its energy back", ["N12", "L15"]),
    5: ("J5", "the change in line losses from current squared, not the annual report's 6.1 percent added in proportion", ["N21", "L22"]),
}
# the judgments the files spell out, so a careful run makes them unprompted
FILED = {
    1: ("J1", "the trial read on the volts its regulators actually took off (VO-1 3.1: feeder-head voltage is the pilot regulator's output)", []),
    4: ("J4", "the volts each feeder can give hour by hour from its far-end meters (VO-1 2.3 and 3.1)", []),
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
    "the trial's scale the mean of the trial feeders' ratios, not the median": dict(lamstat="mean"),
    "the loss fit with a no-load term": dict(lossfit="intercept"),
}
PERTURB = [("the trial-calibrated response 4.6 percent higher (twice its sampling error)", dict(lam=1.046)),
           ("the trial-calibrated response 4.6 percent lower (twice its sampling error)", dict(lam=0.954)),
           ("the loss coefficient 20 percent higher", dict(lossk=1.2)), ("the loss coefficient 20 percent lower", dict(lossk=0.8)),
           ("the far-end readings 0.2 V higher", dict(room=0.2)), ("the far-end readings 0.2 V lower", dict(room=-0.2))]


def J(*off):
    return {j: (j not in off) for j in GOLD}


REFLEX_ROUTE = tuple(STUMPS)          # every stump hurried, every filed judgment and reflex right


def run(R, Jset, **kw):
    A.OPT.update(BASE)
    A.OPT.update(kw)
    A.reset()
    parts = [A.parts2(R, f, Jset) for f in range(P.NF)]
    out = {"save": np.array([p["total"] for p in parts]), "cust": np.array([p["cust"] for p in parts]),
           "loss": np.array([p["loss_rise"] for p in parts]), "cvrf": np.array([p["cvrf"] for p in parts])}
    out["vc"] = out["save"] * P.PRICE * P.ANNUITY / np.array(R.cost)
    out["set"] = tuple(int(f) for f in np.where(out["vc"] >= 1)[0])
    out["trial"] = {f: A.trial_effect(R, f, Jset[1]) for f in R.trial}
    out["room"] = np.array([A.headroom(R, f, Jset[4]).mean() for f in range(P.NF)])
    return out


def quick(R):
    """ten minutes: the export summed as it comes (re-sent rows in), the trial as ON days' mean energy over OFF days',
    the trial's 4.8 V on every feeder all year, the customer meters' saving taken as the substation's"""
    raw = np.zeros(P.NF)
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
    out["cvrf"] = np.full(P.NF, eta)
    out["cust"] = np.array([eta * P.TRIAL_DV / P.VNOM * R.ami[f].sum() for f in range(P.NF)])
    out["save"] = out["cust"].copy()
    out["loss"] = np.zeros(P.NF)
    out["vc"] = out["save"] * P.PRICE * P.ANNUITY / np.array(R.cost)
    out["set"] = tuple(int(f) for f in np.where(out["vc"] >= 1)[0])
    return out


def energy_mwh(R):
    return np.array([R.ami[f].sum() for f in range(P.NF)])


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
    C = run(R, J(*REFLEX_ROUTE))
    drops = {j: run(R, J(j)) for j in STUMPS}
    alone = {j: run(R, J(*[k for k in STUMPS if k != j])) for j in STUMPS}
    assigned = run(R, J(1))
    E = energy_mwh(R)
    fam = [G] + list(riv.values())
    nf = range(P.NF)
    bands = {
        "save": {ids[f]: _band([x["save"][f] for x in fam], 0.03, 8.0) for f in nf},
        "cust": {ids[f]: _band([x["cust"][f] for x in fam], 0.03, 8.0) for f in nf},
        "room": {ids[f]: _band([x["room"][f] for x in fam], 0.02, 0.05) for f in nf},
        "loss": {ids[f]: _band([x["loss"][f] for x in fam], 0.10, 3.0) for f in nf},
        "cvrf": {ids[f]: _band([x["cvrf"][f] for x in fam], 0.03, 0.01) for f in nf},
        "trial_mean": _band([tmean(x, R) for x in fam], 0.02, 0.01),
        "energy": {ids[f]: [round(E[f] * 0.995, 0), round(E[f] * 1.005, 0)] for f in nf},
    }
    tot = [float(sum(x["save"][f] for f in G["set"])) for x in fam]
    bands["total"] = [round(min(tot) * 0.97, 0), round(max(tot) * 1.03, 0)]
    fig = {
        "ids": ids, "trial": [ids[f] for f in R.trial], "headmetered": [ids[f] for f in R.headmetered],
        "kind": {ids[f]: R.kind[f] for f in nf}, "cost": {ids[f]: R.cost[f] for f in nf},
        "energy_mwh": {ids[f]: round(float(E[f]), 0) for f in nf},
        "trial_effect": {ids[f]: round(float(G["trial"][f]), 2) for f in R.trial},
        "trial_mean": round(tmean(G, R), 2), "trial_mean_assigned": round(tmean(assigned, R), 2),
        "room_v": {ids[f]: round(float(G["room"][f]), 2) for f in nf},
        "cvrf": {ids[f]: round(float(G["cvrf"][f]), 2) for f in nf},
        "cust_mwh": {ids[f]: round(float(G["cust"][f]), 0) for f in nf},
        "loss_mwh": {ids[f]: round(float(G["loss"][f]), 0) for f in nf},
        "save_mwh": {ids[f]: round(float(G["save"][f]), 0) for f in nf},
        "value_ratio": {ids[f]: round(float(G["vc"][f]), 2) for f in nf},
        "break_even_mwh": {ids[f]: round(R.cost[f] / (P.PRICE * P.ANNUITY), 0) for f in nf},
        "funded": [ids[f] for f in G["set"]],
        "bands": bands,
        "routes": {"the careful route (the reflex route)": [ids[f] for f in C["set"]]},
        "price": P.PRICE, "annuity": P.ANNUITY, "loss_rate_report": P.LOSS_RATE_REPORT, "vnom": P.VNOM,
        "largest_loss_rise_mwh": round(float(max(G["loss"])), 0), "n_loss_rise": int((G["loss"] > 0).sum()),
        "cvrf_lo": round(float(min(G["cvrf"])), 2), "cvrf_hi": round(float(max(G["cvrf"])), 2),
        "total_save_mwh": round(float(sum(G["save"][f] for f in G["set"])), 0),
        "total_cost": round(float(sum(R.cost[f] for f in G["set"])), 0),
    }
    for j, d in drops.items():
        fig["routes"]["%s dropped (%s)" % (STUMPS[j][0], STUMPS[j][1])] = [ids[f] for f in d["set"]]
    eff = effort(R, ids, G, C, drops, alone, riv, fig)
    return fig, eff


def effort(R, ids, G, C, drops, alone, riv, fig):
    b = fig["bands"]
    nf = range(P.NF)

    def tab(vals, nd=2):
        return {ids[f]: round(float(vals[f]), nd) for f in nf}
    Qk = quick(R)
    res = [
        {"id": "R1", "name": "each feeder's 2026 energy at the customer meters (MWh)", "graded_as": "Ask 1", "figure": "energy_mwh",
         "depends": [], "independent": "the customer-meter sums", "golden": fig["energy_mwh"], "bands": b["energy"],
         "passes": {"quick": tab(Qk["raw_mwh"], 0), "careful": fig["energy_mwh"], "thorough": fig["energy_mwh"]}},
        {"id": "R2", "name": "the trial's change in energy per 1 percent of voltage removed, averaged over the trial feeders",
         "graded_as": "Ask 2", "figure": "trial_mean", "depends": [], "independent": "the trial records",
         "golden": fig["trial_mean"], "band": b["trial_mean"],
         "passes": {"quick": round(float(np.mean([Qk["trial"][f] for f in R.trial])), 2),
                    "careful": round(tmean(C, R), 2), "thorough": fig["trial_mean"]}},
        {"id": "R3", "name": "the average reduction in volts each feeder could be held at over the year", "graded_as": "Ask 3",
         "figure": "room_v", "depends": [], "independent": "the far-end meters", "golden": fig["room_v"], "bands": b["room"],
         "passes": {"quick": tab(Qk["room"]), "careful": tab(C["room"]), "thorough": fig["room_v"]}},
        {"id": "R4", "name": "each feeder's yearly change in customer energy per 1 percent of voltage removed", "graded_as": "Component 2",
         "figure": "cvrf", "depends": ["R2"], "independent": "", "golden": fig["cvrf"], "bands": b["cvrf"],
         "precedent": ["N25", "N12", "L15"], "partly_share": 0.75,
         "passes": {"quick": tab(Qk["cvrf"]), "careful": tab(C["cvrf"]), "thorough": fig["cvrf"]}},
        {"id": "R5", "name": "each feeder's yearly energy saving at the customer meters (MWh)", "graded_as": "Ask 4", "figure": "cust_mwh",
         "depends": ["R3", "R4"], "independent": "", "golden": fig["cust_mwh"], "bands": b["cust"], "precedent": ["N25", "N12", "L15"],
         "partly_share": 0.75, "passes": {"quick": tab(Qk["cust"], 0), "careful": tab(C["cust"], 0), "thorough": fig["cust_mwh"]}},
        {"id": "R6", "name": "the rise in each feeder's own line losses (MWh a year)", "graded_as": "Component 3", "figure": "loss_mwh",
         "depends": ["R3", "R5"], "independent": "", "golden": fig["loss_mwh"], "bands": b["loss"], "precedent": ["N21", "L22"],
         "partly_share": 0.75, "passes": {"quick": tab(Qk["loss"], 0), "careful": tab(C["loss"], 0), "thorough": fig["loss_mwh"]}},
        {"id": "R7", "name": "each feeder's yearly energy saving at the substation (MWh)", "graded_as": "Component 1", "figure": "save_mwh",
         "depends": ["R5", "R6"], "independent": "", "golden": fig["save_mwh"], "bands": b["save"], "precedent": ["N25", "N12", "L15"],
         "partly_share": 0.75, "passes": {"quick": tab(Qk["save"], 0), "careful": tab(C["save"], 0), "thorough": fig["save_mwh"]}},
        {"id": "R9", "name": "the 2027 program's total yearly saving at the substation (MWh)", "graded_as": "Ask 5", "figure": "total_save_mwh",
         "depends": ["R7", "R8"], "independent": "", "golden": fig["total_save_mwh"], "band": b["total"], "precedent": ["N25", "L15"],
         "passes": {"quick": round(float(sum(Qk["save"][f] for f in Qk["set"])), 0), "careful": round(float(sum(C["save"][f] for f in C["set"])), 0),
                    "thorough": fig["total_save_mwh"]}},
        {"id": "R8", "name": "the feeders that receive voltage optimization in 2027", "graded_as": "Recommendation", "figure": "funded",
         "depends": ["R7"], "independent": "", "golden": fig["funded"], "precedent": ["N25", "L15"],
         "passes": {"quick": [ids[f] for f in Qk["set"]], "careful": [ids[f] for f in C["set"]], "thorough": fig["funded"]}},
    ]
    byid = {r["id"]: r for r in res}

    def inb(vals, rid):
        bb = byid[rid]["bands"]
        return all(bb[ids[f]][0] <= vals[f] <= bb[ids[f]][1] for f in nf)

    def rescued(out):
        got = []
        lo, hi = byid["R2"]["band"]
        if lo <= tmean(out, R) <= hi:
            got.append("R2")
        for rid, key in (("R3", "room"), ("R4", "cvrf"), ("R5", "cust"), ("R6", "loss"), ("R7", "save")):
            if inb(out[key], rid):
                got.append(rid)
        if out["set"] == G["set"]:
            got.append("R8")
        return got
    careful_right = set(rescued(C))

    def moved(out):
        return [r for r in ("R2", "R3", "R4", "R5", "R6", "R7", "R8") if r not in rescued(out)]
    judg = []
    for j, (jid, name, prec) in STUMPS.items():
        judg.append({"id": jid, "name": name, "kind": "stump", "precedent": prec,
                     "dropped": {"answer": [ids[f] for f in drops[j]["set"]], "results_moved": moved(drops[j])},
                     "alone": {"answer": [ids[f] for f in alone[j]["set"]],
                               "results_rescued": [r for r in rescued(alone[j]) if r not in careful_right]}})
    for j, (jid, name, prec) in FILED.items():
        judg.append({"id": jid, "name": name, "kind": "reflex", "precedent": prec})
    for i, (name, prec) in enumerate(REFLEXES, 6):
        judg.append({"id": "J%d" % i, "name": name, "kind": "reflex", "precedent": prec})
    hints = [{"sentence": STUMPS[j][1], "rescues": [r for r in rescued(alone[j]) if r not in careful_right]} for j in STUMPS]
    pert = [{"input": nm, "answer": [ids[f] for f in run(R, GOLD, **kw)["set"]]} for nm, kw in PERTURB]
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
