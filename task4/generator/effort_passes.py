"""effort.json, written from results.compute: each result's golden and band, the value the quick, careful-but-hurried
and thorough passes file, each pass computed end to end by its own method on the cut pack; the one-fact hint run
literally; the routes' calls; the forcing block (the golden family, the shortcuts, each fitted input perturbed)."""
import copy
import json

import analysis as A
import docs
import params as P
import results as RS

CYC_PRICED = ("SG", "BRK", "BAV")


def _tab(d, keys):
    return {k: d[k] for k in keys}


def build(G):
    fc, MC, H, Hw, W = G["fc"], G["MC"], G["H"], G["Hw"], G["W"]
    rem = {k: round(fc[k]["total"]) for k in A.PARTS}
    hproj = {k: round(H[k]["proj"]) for k in A.PARTS}
    # the quick pass reads the October report's own 2027 outlook: every part at October's MTBUR, pooled
    qproj = {k: round(v) for k, v in G["qproj"].items()}
    rb = G["rem_band"]
    need = G["need"]
    nb = {k: list(G["need_band"][k]) for k in A.PARTS}
    E = {"results": [], "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    R = E["results"]
    R.append({"id": "R2", "name": "the landing-driven parts' 2027 unscheduled removals", "graded_as": "Component 1",
              "figure": "rem_cyc", "golden": _tab(rem, CYC_PRICED), "depends": [], "independent": "the legs and the changes",
              "bands": {k: [rb[k][0], rb[k][1]] for k in CYC_PRICED},
              "passes": {"quick": _tab(qproj, CYC_PRICED),
                         "careful": {"value": _tab(hproj, CYC_PRICED), "grade": "partly",
                                     "why": "the computed careful pass carries every part per flight hour and misses all three; "
                                            "the stage 4 determinism judge's blind derivation found the landings driver by "
                                            "comparing the bases' rates, so a careful run may too"},
                         "thorough": _tab(rem, CYC_PRICED)},
              "precedent": ["N04", "N01"], "partly_share": 0.5})
    R.append({"id": "R3", "name": "the watch-list serials worth withdrawing", "graded_as": "Component 3",
              "figure": "scrap_set", "golden": G["scrap"], "depends": [], "independent": "the changes and the findings",
              "passes": {"quick": sorted(Hw["face_set"]), "careful": sorted(Hw["cf_set"]), "thorough": G["scrap"]},
              "precedent": ["L03", "L13"]})
    R.append({"id": "R3b", "name": "the removals withdrawing the whole watch list saves", "graded_as": "Ask 3",
              "figure": "saving", "golden": round(G["saving"]), "depends": [], "independent": "the changes and the findings",
              "band": [G["saving_band"][0], G["saving_band"][1]], "partly": [G["saving_band"][0] * 0.85, G["saving_band"][1] * 1.15],
              "passes": {"quick": round(Hw["face"]), "careful": round(Hw["cf_only"]), "thorough": round(G["saving"])},
              "precedent": ["L03", "L14"]})
    R.append({"id": "R4", "name": "the propeller control's 2027 removals and spares", "graded_as": "Component 4",
              "figure": "pec", "golden": {"removals": rem["PEC"], "spares": need["PEC"]}, "depends": [],
              "independent": "the repairers' orders and the stores snapshot",
              "bands": {"removals": [rb["PEC"][0], rb["PEC"][1]], "spares": nb["PEC"]},
              "passes": {"quick": {"removals": qproj["PEC"], "spares": P.POOL["PEC"]},
                         "careful": {"removals": hproj["PEC"], "spares": H["PEC"]["spares"]},
                         "thorough": {"removals": rem["PEC"], "spares": need["PEC"]}},
              "precedent": ["L12", "L11"], "partly_share": 0.5})
    R.append({"id": "R5", "name": "every part number's expected 2027 unscheduled removals", "graded_as": "Ask 1",
              "figure": "rem", "golden": rem, "depends": [], "independent": "the legs, the changes and the programme",
              "bands": {k: [rb[k][0], rb[k][1]] for k in A.PARTS},
              "passes": {"quick": qproj, "careful": hproj, "thorough": rem}, "precedent": ["L12", "L36"], "partly_share": 0.5})
    inh = list(P.IN_HOUSE)
    R.append({"id": "R6", "name": "the in-house lines' spares through the Bodø shop's 2027 queue", "graded_as": "Component 2",
              "figure": "need_inhouse", "golden": _tab(need, inh), "depends": ["R2"], "independent": "",
              "bands": {k: nb[k] for k in inh},
              "passes": {"quick": _tab(P.POOL, inh), "careful": {k: H[k]["spares"] for k in inh}, "thorough": _tab(need, inh)},
              "precedent": ["L15", "L16"], "partly_share": 0.5})
    p10 = {k: int(MC[k]["p10"]) for k in A.PARTS}
    p90 = {k: int(MC[k]["p90"]) for k in A.PARTS}
    gold_rng = {**{k + "_lo": p10[k] for k in A.PARTS}, **{k + "_hi": p90[k] for k in A.PARTS}}
    hr = {**{k + "_lo": int(H[k]["p10"]) for k in A.PARTS}, **{k + "_hi": int(H[k]["p90"]) for k in A.PARTS}}
    # the quick pass's range: Poisson quantiles around the October outlook
    qr = {**{k + "_lo": A._pois_q(qproj[k], 0.10) for k in A.PARTS}, **{k + "_hi": A._pois_q(qproj[k], 0.90) for k in A.PARTS}}
    rbands = {**{k + "_lo": list(G["p10_band"][k]) for k in A.PARTS}, **{k + "_hi": list(G["p90_band"][k]) for k in A.PARTS}}
    R.append({"id": "R7", "name": "the 80 per cent ranges", "graded_as": "Ask 1", "figure": "range", "golden": gold_rng,
              "depends": ["R5"], "independent": "", "bands": rbands,
              "passes": {"quick": qr, "careful": hr, "thorough": gold_rng}, "precedent": ["L35"], "partly_share": 0.5})
    R.append({"id": "R8", "name": "the spares each line needs", "graded_as": "Ask 2", "figure": "need", "golden": dict(need),
              "depends": ["R5", "R6"], "independent": "", "bands": nb,
              "passes": {"quick": dict(P.POOL), "careful": {k: H[k]["spares"] for k in A.PARTS}, "thorough": dict(need)},
              "precedent": ["L11"], "partly_share": 0.5})
    rob = sorted(G["robust"])
    gch = {k: G["calls"][k] for k in rob}
    cch = {k: H[k]["spares"] - P.POOL[k] for k in rob}
    fam_ch = [{k: v[k] for k in rob} for v in G["fam_calls"].values()]
    R.append({"id": "R9", "name": "the lines to buy and to cut, with how many", "graded_as": "Recommendation",
              "figure": "call_units", "golden": gch, "depends": ["R8"], "independent": "",
              "bands": {k: [min([gch[k]] + [c[k] for c in fam_ch]), max([gch[k]] + [c[k] for c in fam_ch])] for k in rob},
              "passes": {"quick": {k: 0 for k in rob}, "careful": cch, "thorough": gch}, "precedent": ["L11"],
              "partly_share": 0.5})
    # the one-fact test: the strongest sentence, executed on the careful pass
    Hd = G["Hd"]
    E["hints"] = [{"sentence": "the starter-generators, brakes and bleed valves wear by landings and engine starts, which the "
                               "2027 programme raises while flight hours fall", "rescues": ["R2"]},
                  {"sentence": "a no-fault-found removal is often the aircraft's fault, not the unit's", "rescues": []},
                  {"sentence": "the Bodø shop's turnaround depends on its load", "rescues": []}]
    E["hint_values"] = {"exposure": {"R2": {k: round(Hd[k]["proj"]) for k in CYC_PRICED},
                                     "R8": {k: Hd[k]["spares"] for k in A.PARTS}}}
    E["routes"] = G["routes"]
    return E


def forcing(G, target):
    """The golden family's calls, the shortcuts' calls, and each fitted input moved by its spread."""
    F, D, fc = G["F"], G["D"], G["fc"]
    robust_keys = sorted(G["robust"])

    def answer(need):
        ch = RS.calls(need)
        out = []
        for k in robust_keys:
            if ch[k] > 0:
                out.append("BUY:%s" % k)
            elif ch[k] < 0:
                out.append("CUT:%s" % k)
        return sorted(out)
    fam = [{"name": n, "answer": answer(v)} for n, v in G["fam_need"].items()]
    sc = [{"name": r["name"], "answer": r["answer"]} for r in G["routes"][1:]]
    pert = []

    def run(name, fc2=None, **kw):
        M = A.simulate(F, fc2 or fc, D, reps=RS.REPS, seed=20271, **kw)
        pert.append({"input": name, "answer": answer({k: M[k]["need"] for k in A.PARTS})})
    def scaled(f, k, m, parts=("cf", "nff")):
        for c in parts:
            f[k]["total"] += (m - 1.0) * f[k][c]
            f[k][c] *= m
    for k in CYC_PRICED:
        f2 = copy.deepcopy(fc)
        scaled(f2, k, 0.8)
        run("%s rate on landings -20%%" % k, f2)
    run("the Bodø shop's calibrated capacity +5%", cap_mult=1.05)
    run("the Bodø shop's calibrated capacity -5%", cap_mult=0.95)
    f2 = copy.deepcopy(fc)
    scaled(f2, "PEC", 1.2)
    run("the propeller control's 2027 rate +20%", f2)
    run("the frost terms +20%", frost_mult=1.2)
    f2 = copy.deepcopy(fc)
    for k in A.PARTS:
        scaled(f2, k, 1.2, ("nff",))
    run("every no-fault-found rate +20%", f2)
    return {"kind": "set", "golden_answer": answer(G["need"]), "golden_family": fam, "shortcuts": sc, "perturbations": pert}


def write(path, E):
    json.dump(E, open(path, "w"), indent=1, default=lambda o: o.item() if hasattr(o, "item") else str(o))
