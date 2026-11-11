"""task19: figures.json (every figure the answer blocks state) and effort.json (each result's golden, band and the value
each pass files), written from the analysis of the cut pack."""
import json
import os

import analysis as AN

# bands: where reasonable methods differ, the range the golden family spans with a margin; set from the rivals run on
# the cut pack (checks.py asserts every rival inside and every shortcut outside)
BAND = {"district_pct": 1.0, "national_pct": 0.6, "coverage_nat": 0.6, "coverage_oth": 2.5, "over_pct": 8.0,
        "elsewhere_pct": 25.0, "k": 0.04, "half_pct": (0.75, 1.45), "on_no_list_pct": 25.0, "p": 0.16,
        "emig_pct": 15.0, "gap_pct_of_national": 0.6}


def jsonable(x):
    import numpy as np
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating,)):
        return float(x)
    return x


def table_bands(gold, pct, floor=0):
    return {k: [v - max(floor, abs(v) * pct / 100.0), v + max(floor, abs(v) * pct / 100.0)] for k, v in gold.items()}


def write(res, gen_out):
    g, c, q = res["golden"], res["careful"], res["quick"]
    dists = list(g["districts"].keys())
    close = g["call"]["too close to call"]
    F = {
        "national_estimate": g["national"],
        "district_estimates": g["districts"],
        "national_interval": g["nat_interval"],
        "national_halfwidth_pct": round(g["nat_half_pct"], 1),
        "district_intervals": g["intervals"],
        "p_line": g["p_line"],
        "call": g["call"],
        "coverage_pct": g["coverage"],
        "linked_pct": g["linked"],
        "recall_pct": g["recall"],
        "raising_factor": g["k"],
        "da_ratio": g["da"],
        "register_counts": g["register"],
        "register_not_correct": g["over"],
        "register_not_correct_parts": g["over_parts"],
        "listed_elsewhere": g["listed_elsewhere"],
        "on_no_list": g["on_no_list"],
        "official_2026": g["official"],
        "official_gap": g["gap"],
        "unrecorded_emigration": g["unrecorded_emigration"],
        "immigration_not_in_accounts": g["imm_not_in_accounts"],
        "official_remainder": g["remainder"],
        "careful_national": c["national"],
        "careful_districts": c["districts"],
        "careful_call": c["call"],
        "careful_halfwidth_pct": round(c["nat_half_pct"], 1),
        "careful_gap": c["gap"],
        "register_national": q["national"],
        "district_names": AN.DNAME,
    }
    F = jsonable(F)
    json.dump(F, open(os.path.join(gen_out, "figures.json"), "w"), indent=1, ensure_ascii=False)

    est_table = dict(g["districts"])
    est_table["national"] = g["national"]
    est_bands = table_bands(g["districts"], BAND["district_pct"])
    est_bands["national"] = [g["national"] * (1 - BAND["national_pct"] / 100), g["national"] * (1 + BAND["national_pct"] / 100)]

    def est_of(s):
        t = dict(s["districts"])
        t["national"] = s["national"]
        return t
    gap_band = BAND["gap_pct_of_national"] / 100 * g["national"]
    r9_gold = {"gap": g["gap"], "unrecorded_emigration": g["unrecorded_emigration"], "remainder": g["remainder"]}
    r9_bands = {"gap": [g["gap"] - gap_band, g["gap"] + gap_band],
                "unrecorded_emigration": [g["unrecorded_emigration"] * (1 - BAND["emig_pct"] / 100),
                                          g["unrecorded_emigration"] * (1 + BAND["emig_pct"] / 100)],
                "remainder": [g["remainder"] - gap_band, g["remainder"] + gap_band]}
    r7_gold = {"call": g["call"]}
    r7_bands = {}
    for d in close:
        r7_gold["p_" + d] = g["p_line"][d]
        r7_bands["p_" + d] = [g["p_line"][d] - BAND["p"], g["p_line"][d] + BAND["p"]]

    def r7_of(s):
        if s.get("call") is None:
            return None
        out = {"call": s["call"]}
        for d in close:
            out["p_" + d] = (s.get("p_line") or {}).get(d, 1.0 if d in s["call"]["qualifies"] else 0.0)
        return out

    def r9_of(s, quick=False):
        if quick:
            return None
        return {"gap": s["gap"], "unrecorded_emigration": s["unrecorded_emigration"], "remainder": s["remainder"]}

    results = [
        {"id": "R1", "name": "share of survey residents on their own district's list", "graded_as": "Component 1",
         "figure": "coverage_pct", "depends": [], "independent": "the survey, the register and the clerical review",
         "golden": g["coverage"],
         "bands": {"nationals": [g["coverage"]["nationals"] - BAND["coverage_nat"], g["coverage"]["nationals"] + BAND["coverage_nat"]],
                   "others": [g["coverage"]["others"] - BAND["coverage_oth"], g["coverage"]["others"] + BAND["coverage_oth"]]},
         "passes": {"quick": q["coverage"], "careful": c["linked"], "thorough": g["coverage"]},
         "precedent": ["L01", "L06"]},
        {"id": "R2", "name": "register entries not correct for their district", "graded_as": "Ask 3",
         "figure": "register_not_correct", "depends": [], "independent": "the follow-up and the register",
         "golden": g["over"], "bands": table_bands(g["over"], BAND["over_pct"], 25), "partly_share": 0.5,
         "passes": {"quick": {d: 0 for d in dists}, "careful": c["over"], "thorough": g["over"]}},
        {"id": "R3", "name": "residents listed in another district", "graded_as": "Ask 3b",
         "figure": "listed_elsewhere", "depends": ["R1"], "independent": "the survey's links by district",
         "golden": g["listed_elsewhere"], "bands": table_bands(g["listed_elsewhere"], BAND["elsewhere_pct"], 40),
         "passes": {"quick": {d: 0 for d in dists}, "careful": c["listed_elsewhere"], "thorough": g["listed_elsewhere"]},
         "precedent": ["L01"]},
        {"id": "R4", "name": "raising factors for men aged 18 to 29 and 30 to 44", "graded_as": "Component 2",
         "figure": "raising_factor", "depends": [], "independent": "births by sex, the life table and the survey",
         "golden": g["k"], "bands": {k: [v - BAND["k"], v + BAND["k"]] for k, v in g["k"].items()},
         "passes": {"quick": q["k"], "careful": c["k"], "thorough": g["k"]}, "precedent": ["L22", "N05"]},
        {"id": "R5", "name": "district estimates and the national total", "graded_as": "Ask 1",
         "figure": "district_estimates", "depends": ["R1", "R2", "R4"], "independent": "",
         "golden": est_table, "bands": est_bands,
         "passes": {"quick": est_of(q), "careful": est_of(c), "thorough": est_table}, "precedent": ["L22", "L01"]},
        {"id": "R6", "name": "national 90 per cent interval half-width", "graded_as": "Component 3",
         "figure": "national_halfwidth_pct", "depends": [], "independent": "the bootstrap of the survey blocks",
         "golden": round(g["nat_half_pct"], 1), "band": list(BAND["half_pct"]), "partly": [0.65, 1.8],
         "passes": {"quick": None, "careful": round(c["nat_half_pct"], 1), "thorough": round(g["nat_half_pct"], 1)},
         "precedent": ["L35", "L31"]},
        {"id": "R7", "name": "the call and each close district's chance", "graded_as": "Recommendation",
         "figure": "call", "depends": ["R5", "R6"], "independent": "",
         "golden": r7_gold, "bands": r7_bands,
         "passes": {"quick": r7_of(q), "careful": r7_of(c), "thorough": r7_gold}, "precedent": ["L35", "L22"]},
        {"id": "R8", "name": "residents on no district's list, by district", "graded_as": "Ask 3c",
         "figure": "on_no_list", "depends": ["R5"], "independent": "",
         "golden": g["on_no_list"], "bands": table_bands(g["on_no_list"], BAND["on_no_list_pct"], 40),
         "passes": {"quick": {d: 0 for d in dists}, "careful": c["on_no_list"], "thorough": g["on_no_list"]},
         "precedent": ["L28"]},
        {"id": "R9", "name": "the rolled-forward estimate bridged to the estimate", "graded_as": "Component 4",
         "figure": "unrecorded_emigration", "depends": [], "independent": "the follow-up, the border record and the accounts",
         "golden": r9_gold, "bands": r9_bands,
         "passes": {"quick": None, "careful": r9_of(c), "thorough": r9_gold}, "precedent": ["L29", "L26"]},
    ]
    # constants the answer blocks state (bands, ages, the circular's paragraphs) and the shortcut sizes they quote
    sc = res["shortcuts"]
    s1 = sc["linked share read as coverage"]
    s4 = sc["independence within age and sex"]
    eff1 = [100.0 * (s1["districts"][d] / g["districts"][d] - 1) for d in dists]
    eff4 = [100.0 * (s4["districts"][d] / g["districts"][d] - 1) for d in dists]
    F["constants"] = {"line": 25000, "interval_pct": 90, "band_district_pct": 1.0, "band_national_pct": 0.6,
                      "band_cov_nat": 0.6, "band_cov_oth": 2.5, "band_over_pct": 8, "band_else_pct": 25,
                      "band_people": 40, "band_k": 0.04, "band_half": [0.75, 1.45], "band_p": 0.16,
                      "band_emig_pct": 15, "band_gap_pct": 0.6, "ages": [18, 29, 30, 44],
                      "circular_paragraphs": ["2.1", "2.2", "2.3", "3.1", "3.2"], "circular": "2026/14",
                      "supplement_pct_of_pool": 1.2}
    F["linked_share_effect_pct"] = [round(min(eff1), 1), round(max(eff1), 1)]
    F["independence_effect_pct"] = [round(min(eff4), 1), round(max(eff4), 1)]
    F["independence_gap"] = g["national"] - s4["national"]
    F["linked_share_gap"] = s1["national"] - g["national"]
    # the R9 figure key carries the whole bridge in figures.json
    F["official_bridge"] = r9_gold
    F["call_and_chances"] = r7_gold
    F["estimates_with_national"] = est_table
    json.dump(F, open(os.path.join(gen_out, "figures.json"), "w"), indent=1, ensure_ascii=False)
    for r in results:
        if r["id"] == "R9":
            r["figure"] = "official_bridge"
        if r["id"] == "R7":
            r["figure"] = "call_and_chances"
        if r["id"] == "R5":
            r["figure"] = "estimates_with_national"
        if r["id"] == "R6":
            r["golden"] = F["national_halfwidth_pct"]
    hints = [
        {"sentence": "the register and the coverage survey miss the same young men; compare the estimate's sex ratios "
                     "with the ones births and survival give", "rescues": ["R4"]},
        {"sentence": "a survey person the matcher could not link may still be on the register; measure what the matcher "
                     "misses on the clerical review", "rescues": ["R1"]},
        {"sentence": "the interval has to carry the errors every district shares, such as the linkage correction and the "
                     "raising factors", "rescues": ["R6"]},
        {"sentence": "the rolled-forward estimate misses the same emigrants the register still lists, so its closeness "
                     "to an estimate is no check", "rescues": ["R9"]},
    ]
    routes = [{"name": "the golden", "answer": g["call"], "golden": True},
              {"name": "careful but hurried: linked share as coverage, independence, survey-only intervals",
               "answer": c["call"]},
              {"name": "the register's own counts", "answer": q["call"]}]
    for name, s in res["shortcuts"].items():
        routes.append({"name": name, "answer": s["call"]})
    forcing = {"kind": "set", "golden_answer": g["call"],
               "golden_family": [{"name": n, "answer": s["call"]} for n, s in res["rivals"].items()],
               "shortcuts": [{"name": n, "answer": s["call"]} for n, s in res["shortcuts"].items()],
               "perturbations": [{"input": n, "answer": {"qualifies": v["qualifies"], "too close to call": v["too close to call"]}}
                                 for n, v in res["perturb"].items()]}
    E = {"results": results, "hints": hints, "routes": routes, "forcing": forcing,
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7},
         "careful_pass": "the matcher's links read as the register's coverage, independence within age and sex, the "
                         "survey blocks resampled alone, the gap to the rolled-forward figure read as emigration",
         "rivals": res["rivals"], "shortcut_figures": res["shortcuts"], "hinted": res["hinted"],
         "perturbation_figures": res["perturb"], "bands": {k: (list(v) if isinstance(v, tuple) else v) for k, v in BAND.items()}}
    E = jsonable(E)
    json.dump(E, open(os.path.join(gen_out, "effort.json"), "w"), indent=1, ensure_ascii=False)
    return F, E
