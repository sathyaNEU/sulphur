"""Every owed figure, from the cut pack: the golden and its bands (core.py's battery, the step windows and the forcing
perturbations run on the read-back arrays), the three passes of the effort test (the quick pass, the careful but
hurried pass that is the reflex route, the golden), the hints, the factorial and the forcing block. Writes the
figures.json and effort.json the gates read."""
import numpy as np

import analysis as AN
import core as C
import read as R

WINDOWS = (3, 4, 5, 6, 7, 8, 9, 10)       # minutes either side of a command a step can be read over (core.WINDOWS)
NAMES = {"rep_w": "Kettle Ridge VHF repeater", "rep_n": "Halverson carrier fill-in site",
         "fix_t": "Larkin find-and-fix round", "fix_w": "Medora Flats find-and-fix round",
         "recon_in": "Reconnection round within 14 km", "recon_out": "Outlying reconnection round"}
ORDER = ["rep_w", "rep_n", "fix_t", "fix_w", "recon_in", "recon_out"]
KEYS = ORDER + ["c1_fringe_loss", "c2_failed_old", "c3_unwired", "lost_reach", "lost_hw", "lost_unwired", "delivered",
                "plan_kw", "plan_cost_per_kw"]


def battery(target, wd, ex, A, windows=True):
    """The golden family: core's fifteen rebuilds and the 63 other step windows (a minutes before, b after, 3 to 10
    each), every one on the cut pack: 78 rebuilds, as core.py's battery."""
    fam = dict(A["fam"])
    if windows:
        for a_ in WINDOWS:
            for b_ in WINDOWS:
                if (a_, b_) == (5, 5):
                    continue
                w2 = R.steps_for_window(wd, ex, a_, b_)
                fam["step window %d minutes before, %d after" % (a_, b_)] = C.all_figures(w2, C.model(w2), A["ln"])
    return fam


def rnd(x, nd=0):
    return float(round(float(x), nd)) if nd else int(round(float(x)))


def run_all(target, windows=True):
    wd, ex = R.read(target)
    A = AN.run(wd)
    ln, cnt, gold = A["ln"], A["cnt"], A["gold"]
    fam = battery(target, wd, ex, A, windows)
    names = list(fam)
    bands = {}
    for k in KEYS:
        bands[k] = AN.band(float(gold[k]), [float(fam[v][k]) for v in names])
    go = AN.funded(gold, ln)
    for v in names:
        assert AN.funded(fam[v], ln) == go, "a rebuild in the battery files another set: %s" % v
    pert = AN.perturb(wd, A)
    for v, f in pert.items():
        assert AN.funded(f, ln) == go, "a perturbed input files another set: %s" % v
    st = A["study"]
    k = A["gm"]["k"]
    could = C.W_CP * k * wd["n_s"]
    # ---- the figures the answer blocks state ----
    F = {}
    F["funded"] = [NAMES[m] for m in ORDER if m in go]
    F["rejected"] = [NAMES[m] for m in ORDER if m not in go]
    F["proposals"] = {}
    for m in ORDER:
        lo, hi = bands[m]
        F["proposals"][m] = dict(name=NAMES[m], kw=rnd(gold[m]), band=[rnd(lo), rnd(hi)], breakeven=rnd(ln[m]),
                                 breakeven_1=rnd(ln[m], 1), funded=m in go,
                                 premises=cnt.get(m), cost=rnd(ln[m] * C.VALUE),
                                 cost_per_kw=rnd(ln[m] * C.VALUE / gold[m], 1) if gold[m] > 0 else None,
                                 margin=rnd(gold[m] - ln[m]))
    pct = lambda x: int(round(100 * float(x)))
    b1, b2, b3 = bands["c1_fringe_loss"], bands["c2_failed_old"], bands["c3_unwired"]
    F["c1_lost"] = pct(gold["c1_fringe_loss"])
    F["c1_through"] = 100 - F["c1_lost"]
    F["c1_lost_band"] = [pct(b1[0]), pct(b1[1])]
    F["c1_through_band"] = [100 - pct(b1[1]), 100 - pct(b1[0])]
    F["c2_failed"] = pct(gold["c2_failed_old"])
    F["c2_work"] = 100 - F["c2_failed"]
    F["c2_failed_band"] = [pct(b2[0]), pct(b2[1])]
    F["c2_work_band"] = [100 - pct(b2[1]), 100 - pct(b2[0])]
    F["c3_unwired"] = pct(gold["c3_unwired"])
    F["c3_wired"] = 100 - F["c3_unwired"]
    F["c3_unwired_band"] = [pct(b3[0]), pct(b3[1])]
    F["c3_wired_band"] = [100 - pct(b3[1]), 100 - pct(b3[0])]
    F["could_shed"] = rnd(could)
    for kk in ("lost_reach", "lost_hw", "lost_unwired", "delivered"):
        F[kk] = rnd(gold[kk])
        F[kk + "_band"] = [rnd(bands[kk][0]), rnd(bands[kk][1])]
    F["plan_kw"] = rnd(gold["plan_kw"])
    F["plan_kw_band"] = [rnd(bands["plan_kw"][0]), rnd(bands["plan_kw"][1])]
    F["plan_cost_per_kw"] = rnd(gold["plan_cost_per_kw"], 1)
    F["plan_cost_per_kw_band"] = [rnd(bands["plan_cost_per_kw"][0], 1), rnd(bands["plan_cost_per_kw"][1], 1)]
    F["plan_cost"] = rnd(sum(ln[m] for m in go) * C.VALUE)
    F["plan_value"] = rnd(gold["plan_kw"] * C.VALUE)
    # the record behind the figures (the Step-by-Step's counts and fitted terms)
    gm = A["gm"]
    F["counts"] = dict(switches=int(wd["n_s"]), steps=int(len(wd["step"])), events=int(wd["n_events"]),
                       commands=int(wd["disp"].sum()), feeders=int(wd["n_feed"]), groups=16, study_homes=int(len(ex["hid"])),
                       flagged=int(wd["flag"].sum()), old=int((wd["yr"] <= 2015).sum()), fix_t=cnt["fix_t"], fix_w=cnt["fix_w"],
                       recon_in=cnt["recon_in"], recon_out=cnt["recon_out"],
                       fringe=int((wd["now"] > 20).sum()), near=int((wd["now"] <= 8).sum()),
                       variants=len(names))
    F["fit"] = dict(q=[rnd(v, 3) for v in gm["q"]], c_connected=rnd(gm["c"][1], 3), working_kw=rnd(k, 3),
                    study_itt=rnd(st["itt"], 3), study_share=pct(st["share"]), a=[rnd(v, 3) for v in gm["a"]],
                    h=[rnd(v, 3) for v in gm["h"]], index=C.W_CP, value=C.VALUE)
    F["routes"] = {}
    for lab, f in (("reflex", A["reflex"]), ("rigorous", A["rig"]), ("generous", A["gen"]), ("cutoff", A["cut"]["14 km, 2011"])):
        F["routes"][lab] = {m: rnd(f[m]) for m in ORDER}
        F["routes"][lab]["funded"] = [NAMES[m] for m in ORDER if f[m] >= ln[m]]
    F["routes"]["rigorous"]["delivered"] = rnd(A["rig"]["delivered"])
    F["reflex_bridge"] = {kk: rnd(A["reflex"][kk]) for kk in ("lost_reach", "lost_hw", "lost_unwired")}
    F["reflex_bridge"]["total"] = rnd(sum(A["reflex"][kk] for kk in ("lost_reach", "lost_hw", "lost_unwired")))
    F["lattice"] = {}
    for kk, f in A["lat"].items():
        F["lattice"][kk] = {"funded": [NAMES[m] for m in ORDER if f[m] >= ln[m]],
                            **{m: rnd(f[m]) for m in ORDER},
                            "c1_through": 100 - pct(f["c1_fringe_loss"]), "c2_work": 100 - pct(f["c2_failed_old"]),
                            "c3_wired": 100 - pct(f["c3_unwired"])}
    F["over"] = {kk: {"funded": [NAMES[m] for m in ORDER if f[m] >= ln[m]], **{m: rnd(f[m]) for m in ORDER}}
                 for kk, f in A["over"].items()}
    F["fals"] = {kk: rnd(v, 3) for kk, v in A["fals"].items()}
    F["bands_raw"] = {kk: [float(v) for v in b] for kk, b in bands.items()}
    F["golden_raw"] = {kk: float(gold[kk]) for kk in KEYS}
    F["family"] = {v: {kk: float(fam[v][kk]) for kk in KEYS} for v in names}
    F["perturb"] = {v: {kk: float(f[kk]) for kk in ORDER} for v, f in pert.items()}
    F["quick"] = quick(wd, A)
    # the constants the work plan files, as the blocks state them
    F["appraisal"] = dict(fringe_km=20, near_km=8, split_km=int(C.OUT_KM), index=C.W_CP, value_usd_kw_year=int(C.VALUE),
                          demand_rate=22.0, through_year=C.OLD_YEAR)
    # the table results effort.json grades, keyed as figures.json holds them
    F["bridge"] = {"could": F["could_shed"], "delivered": F["delivered"], "lost_reach": F["lost_reach"], "lost_hw": F["lost_hw"],
                   "lost_unwired": F["lost_unwired"]}
    F["proposal_kw"] = {m: F["proposals"][m]["kw"] for m in ORDER}
    F["plan"] = {"plan_kw": F["plan_kw"], "plan_cost_per_kw": F["plan_cost_per_kw"]}
    E = effort(F, A, fam, pert)
    return F, E, wd, ex, A


def quick(wd, A):
    """Ten minutes: last year's planning figure of 1.0 kW a switch and the three records read as they stand."""
    ln, cnt = A["ln"], A["cnt"]
    n = wd["n_s"]
    out = {"rep_w": 0.0, "rep_n": 0.0}
    for m in ("fix_t", "fix_w"):
        out[m] = C.W_CP * cnt[m] * 1.0 * (1 - C.FACE["test_pass"])
    for m in ("recon_in", "recon_out"):
        out[m] = C.W_CP * cnt[m] * 1.0 * C.FACE["test_pass"] * (1 - C.FACE["wo_connected"])
    out["c1_fringe_loss"], out["c2_failed_old"], out["c3_unwired"] = 0.0, 1 - C.FACE["test_pass"], 1 - C.FACE["wo_connected"]
    could = C.W_CP * n * 1.0
    out["could"] = could
    out["lost_reach"] = 0.0
    out["lost_hw"] = could * (1 - C.FACE["test_pass"])
    out["lost_unwired"] = C.W_CP * int(wd["flag"].sum()) * C.FACE["test_pass"] * (1 - C.FACE["wo_connected"])
    out["delivered"] = could - out["lost_hw"] - out["lost_unwired"]
    go = [m for m in ORDER if out[m] >= ln[m]]
    out["plan_kw"] = float(sum(out[m] for m in go))
    out["plan_cost_per_kw"] = 0.0
    out["funded"] = go
    return {kk: (float(v) if not isinstance(v, list) else v) for kk, v in out.items()}


def effort(F, A, fam, pert):
    gold, ln = A["gold"], A["ln"]
    B = F["bands_raw"]
    reflex = A["reflex"]
    Q = F["quick"]
    pct = lambda x: 100 * float(x)

    def tab(f, keys):
        return {kk: round(float(f[kk]), 1) for kk in keys}

    k = A["gm"]["k"]
    could = C.W_CP * k * A["gm"]["th"].size
    bridge_keys = ["lost_reach", "lost_hw", "lost_unwired"]
    res = [
        {"id": "R1", "name": "the share of shed commands that get through at the fringe, against switches within 8 km (per 100)",
         "graded_as": "Component 1", "figure": "c1_through", "depends": [], "independent": "the transmitter register, the outage log and the steps",
         "golden": F["c1_through"], "band": F["c1_through_band"], "precedent": ["N09", "N27", "L38", "L70"],
         "passes": {"quick": 100.0, "careful": round(100 - pct(reflex["c1_fringe_loss"]), 1), "thorough": F["c1_through"]}},
        {"id": "R2", "name": "the share of switches installed through 2015 that still work, at premises with no replaced unit (per 100)",
         "graded_as": "Component 2", "figure": "c2_work", "depends": [], "independent": "the install batches, the study homes and the steps",
         "golden": F["c2_work"], "band": F["c2_work_band"], "precedent": ["L28", "N11", "N46", "N35"],
         "passes": {"quick": round(100 - pct(Q["c2_failed_old"]), 1), "careful": round(100 - pct(reflex["c2_failed_old"]), 1),
                    "thorough": F["c2_work"]}},
        {"id": "R3", "name": "the share of switches still wired in where the air conditioner was replaced since (per 100)",
         "graded_as": "Component 3", "figure": "c3_wired", "depends": [], "independent": "the rebate and permit records and the steps",
         "golden": F["c3_wired"], "band": F["c3_wired_band"], "precedent": ["L26", "L58", "N14", "L56", "N36"],
         "passes": {"quick": round(100 - pct(Q["c3_unwired"]), 1), "careful": round(100 - pct(reflex["c3_unwired"]), 1),
                    "thorough": F["c3_wired"]}},
        {"id": "R4", "name": "the bridge from the kW the switches could take off at peak to the kW they deliver",
         "graded_as": "Ask 2", "figure": "bridge", "depends": ["R1", "R2", "R3"], "independent": "",
         "golden": {"could": F["could_shed"], "delivered": F["delivered"], **{kk: F[kk] for kk in bridge_keys}},
         "bands": {"could": [F["could_shed"] - 1, F["could_shed"] + 1], "delivered": F["delivered_band"],
                   **{kk: F[kk + "_band"] for kk in bridge_keys}},
         "partly_share": 0.4, "precedent": ["L63", "L06"],
         "passes": {"quick": {"could": round(Q["could"], 1), "delivered": round(Q["delivered"], 1), **tab(Q, bridge_keys)},
                    "careful": {"could": round(could, 1), "delivered": F["delivered"], **tab(reflex, bridge_keys)},
                    "thorough": {"could": F["could_shed"], "delivered": F["delivered"], **{kk: F[kk] for kk in bridge_keys}}}},
        {"id": "R5", "name": "the peak kW each proposal adds in 2027", "graded_as": "Ask 1", "figure": "proposal_kw",
         "depends": ["R1", "R2", "R3"], "independent": "",
         "golden": {m: F["proposals"][m]["kw"] for m in ORDER}, "bands": {m: F["proposals"][m]["band"] for m in ORDER},
         "partly_share": 0.5, "precedent": ["L63", "L06"],
         "passes": {"quick": tab(Q, ORDER), "careful": tab(reflex, ORDER), "thorough": {m: F["proposals"][m]["kw"] for m in ORDER}}},
        {"id": "R6", "name": "the funded plan's kW and its cost per kW-year", "graded_as": "Ask 3", "figure": "plan",
         "depends": ["R5"], "independent": "",
         "golden": {"plan_kw": F["plan_kw"], "plan_cost_per_kw": F["plan_cost_per_kw"]},
         "bands": {"plan_kw": F["plan_kw_band"], "plan_cost_per_kw": F["plan_cost_per_kw_band"]},
         "precedent": ["L63"],
         "passes": {"quick": {"plan_kw": Q["plan_kw"], "plan_cost_per_kw": Q["plan_cost_per_kw"]},
                    "careful": {"plan_kw": round(float(reflex["plan_kw"]), 1), "plan_cost_per_kw": round(float(reflex["plan_cost_per_kw"]), 1)},
                    "thorough": {"plan_kw": F["plan_kw"], "plan_cost_per_kw": F["plan_cost_per_kw"]}}},
        {"id": "R7", "name": "the proposals funded", "graded_as": "Recommendation", "figure": "funded", "depends": ["R5", "R6"],
         "independent": "", "golden": F["funded"], "precedent": ["L26", "L63"],
         "passes": {"quick": [NAMES[m] for m in Q["funded"]], "careful": F["routes"]["reflex"]["funded"], "thorough": F["funded"]}},
    ]

    def right(f):
        """The results a route lands (graded the way effort.py grades them) from its figure dict."""
        got = []
        if F["c1_through_band"][0] <= 100 - pct(f["c1_fringe_loss"]) <= F["c1_through_band"][1]:
            got.append("R1")
        if F["c2_work_band"][0] <= 100 - pct(f["c2_failed_old"]) <= F["c2_work_band"][1]:
            got.append("R2")
        if F["c3_wired_band"][0] <= 100 - pct(f["c3_unwired"]) <= F["c3_wired_band"][1]:
            got.append("R3")
        cells = [B[kk][0] <= f[kk] <= B[kk][1] for kk in bridge_keys]
        if all(cells):
            got.append("R4")
        if all(B[m][0] <= f[m] <= B[m][1] for m in ORDER):
            got.append("R5")
        if all(B[kk][0] <= f[kk] <= B[kk][1] for kk in ("plan_kw", "plan_cost_per_kw")):
            got.append("R6")
        if [NAMES[m] for m in ORDER if f[m] >= ln[m]] == F["funded"]:
            got.append("R7")
        return got

    allr = ["R1", "R2", "R3", "R4", "R5", "R6", "R7"]
    careful_right = set(right(reflex))
    stumps = {"S1": ("J1", "reception by reach to an on-air transmitter of the switch's own paging system, not the coverage map",
                     ["N09", "N27", "L38", "L70"]),
              "S2": ("J2", "switches still working by install batch, not the test log's pass rate", ["L28", "N11", "N46", "N35"]),
              "S3": ("J3", "switches still wired where the air conditioner was replaced, not the work orders' finding",
                     ["L26", "L58", "N14", "L56", "N36"])}
    others = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
    judg, hints = [], []
    for s, (jid, nm, prec) in stumps.items():
        dropped = A["lat"][s]
        alone = A["lat"][others[s]]
        judg.append({"id": jid, "name": nm, "kind": "stump", "precedent": prec,
                     "dropped": {"answer": [NAMES[m] for m in ORDER if dropped[m] >= ln[m]],
                                 "results_moved": [r for r in allr if r not in right(dropped)]},
                     "alone": {"answer": [NAMES[m] for m in ORDER if alone[m] >= ln[m]],
                               "results_rescued": [r for r in right(alone) if r not in careful_right]}})
    for jid, nm, prec in (("J4", "the delivered total found by regressing the steps on the switches dispatched", ["R102"]),
                          ("J5", "the study homes' randomised comparison with a placebo and an interval clustered by home", ["R55", "R92"]),
                          ("J6", "feeder membership as operated, from the switching log", ["R38"]),
                          ("J7", "the SCADA, encoder and register hygiene (clocks, retries, held readings, renamed points, re-keyed premises)", ["R01"])):
        judg.append({"id": jid, "name": nm, "kind": "reflex", "precedent": prec})
    s1_alone = A["lat"]["S2+S3"]
    hints.append({"sentence": "a one-way switch far from an on-air transmitter of its own paging system misses most of its pages",
                  "rescues": [r for r in right(s1_alone) if r not in careful_right]})
    for s, sent in (("S2", "a switch that passed its last test is not a switch that works now: the share still shedding falls with the install batch's age"),
                    ("S3", "where the air conditioner was replaced after the switch went in, most switches were left unwired")):
        hints.append({"sentence": sent, "rescues": [r for r in right(A["lat"][others[s]]) if r not in careful_right]})
    fam_rows = [{"name": "the golden", "answer": F["funded"]}] + \
        [{"name": v, "answer": [NAMES[m] for m in ORDER if fam[v][m] >= ln[m]]} for v in fam]
    pert_rows = [{"input": v, "answer": [NAMES[m] for m in ORDER if f[m] >= ln[m]]} for v, f in pert.items()]
    short = [{"name": "%s read at face value" % s, "answer": [NAMES[m] for m in ORDER if A["lat"][s][m] >= ln[m]]} for s in ("S1", "S2", "S3")]
    short += [{"name": "the study homes carried to the fleet", "answer": F["routes"]["rigorous"]["funded"]},
              {"name": "the nearest listed transmitter of either system", "answer": F["routes"]["generous"]["funded"]},
              {"name": "the three records at face value (the reflex route)", "answer": F["routes"]["reflex"]["funded"]},
              {"name": "beyond 14 km lost, through 2011 dead, flagged unwired", "answer": F["routes"]["cutoff"]["funded"]}]
    routes = [{"name": "the golden", "answer": F["funded"], "golden": True},
              {"name": "the careful route (the reflex route)", "answer": F["routes"]["reflex"]["funded"]},
              {"name": "the quick route", "answer": [NAMES[m] for m in Q["funded"]]}] + \
             [{"name": r_["name"], "answer": r_["answer"]} for r_ in short[:3] + short[3:5]]
    return {"results": res, "hints": hints,
            "factorial": {"golden_answer": F["funded"], "reflex_route": {"answer": F["routes"]["reflex"]["funded"]}, "judgments": judg},
            "forcing": {"kind": "set", "golden_answer": F["funded"], "golden_family": fam_rows, "perturbations": pert_rows,
                        "shortcuts": short},
            "routes": routes, "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}
