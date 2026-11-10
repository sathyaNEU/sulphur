"""effort.json: the client's effort test computed on the cut pack (python3 effort_passes.py [target]). Each pass is the
author's implementation of a named method, run end to end on the shipped files; nothing reads the prompt.

  quick      the last twelve months' ARR growth carried fourteen months forward; the opening book as every exported
             line in force summed (duplicates, credited lines and failed Team invoices kept)
  careful    what a frontier run does unprompted: every file cleaned (the opening book right), the mean realised uplift
             applied to every contract still to reprice, pooled renewal exit and seat rates, the Team plan's last
             three months' rates, each account's trailing true-up rate, the open pipeline at the CRM's stage
             probabilities, accounts drawn independently for the band
  thorough   the golden
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import golden as GD
import params as P
import writeup as WU

r10k, r100k = GD.r10k, GD.r100k


def values(f, figs, months):
    """What a pass files at each result, from one route's figures (the opening book cleaned)."""
    return {"R1": figs["opening"], "R2": r10k(f["price"]), "R3": r10k(f["team_left"]),
            "R4": {"contraction": r10k(f["contraction"]), "churn": r10k(f["churn"])},
            "R5": {"new_bus": r10k(f["new_bus"]), "new_open": r10k(f["new_open"])},
            "R6": r100k(f["p20"]), "R7": {m: r10k(v) for m, v in zip(months, f["path"])}}


def grade(res, v):
    """effort.py's grading of one value against one result: right, partly or missed."""
    if v is None:
        return "missed"
    if "bands" in res:
        cells = [k for k in res["bands"]]
        inside = sum(1 for k in cells if res["bands"][k][0] <= v[k] <= res["bands"][k][1])
        if inside == len(cells):
            return "right"
        return "partly" if inside >= res.get("partly_share", 0.5) * len(cells) else "missed"
    lo, hi = res["band"]
    if lo <= v <= hi:
        return "right"
    if "partly" in res and res["partly"][0] <= v <= res["partly"][1]:
        return "partly"
    return "missed"


def build(F, B, g, R, figs):
    months = figs["path_months"]
    car = R["careful but hurried"]
    quick = R["quick"]
    fam = [g] + [v for v in R.values() if v.get("kind") == "rival"]
    path_bands = {m: figs["band_path"][i] for i, m in enumerate(months)}
    path_g = {m: v for m, v in zip(months, figs["path"])}
    path_c = values(car, figs, months)["R7"]
    # the quick pass draws a straight line at its growth rate from October
    g12 = quick["growth12"]
    path_q = {m: r10k(figs["open_total"] * g12 ** ((i + 1) / 12.0)) for i, m in enumerate(months)}
    res = [
        {"id": "R1", "name": "ARR on the books 31 Oct 2026, Business and Team", "graded_as": "Ask 1",
         "figure": "opening", "depends": [], "independent": "", "golden": figs["opening"],
         "bands": {"business": [figs["open_bus"]] * 2, "team": [figs["open_team"]] * 2}, "partly_share": 0.5,
         "passes": {"quick": {"business": figs["r1_all_lines"], "team": figs["r1_team_all_rows"]},
                    "careful": figs["opening"], "thorough": figs["opening"]}},
        {"id": "R2", "name": "price line of the bridge", "graded_as": "Component 1", "figure": "price",
         "depends": [], "independent": "", "golden": figs["price"], "band": figs["band_price"],
         "partly": [figs["band_price"][0] - 30000, figs["band_price"][1] + 30000],
         "passes": {"quick": None, "careful": r10k(car["price"]), "thorough": figs["price"]}},
        {"id": "R3", "name": "Dec 2027 Team ARR from the October Team accounts", "graded_as": "Ask 3", "figure": "team_left",
         "depends": [], "independent": "", "golden": figs["team_left"], "band": figs["band_team_left"],
         "partly": [figs["band_team_left"][0] - 40000, figs["band_team_left"][1] + 40000],
         "passes": {"quick": None, "careful": r10k(car["team_left"]), "thorough": figs["team_left"]}},
        {"id": "R4", "name": "seat reductions and accounts lost", "graded_as": "Component 2",
         "figure": "renewal_lines", "depends": [], "independent": "", "golden": figs["renewal_lines"],
         "bands": {"contraction": figs["band_contraction"], "churn": figs["band_churn"]}, "partly_share": 0.5,
         "passes": {"quick": None, "careful": {"contraction": r10k(car["contraction"]), "churn": r10k(car["churn"])},
                    "thorough": figs["renewal_lines"]}},
        {"id": "R5", "name": "new Business ARR and the open deals' part", "graded_as": "Ask 4",
         "figure": "new_split", "depends": [], "independent": "", "golden": figs["new_split"],
         "bands": {"new_bus": figs["band_new_bus"], "new_open": figs["band_new_open"]}, "partly_share": 0.5,
         "passes": {"quick": None, "careful": {"new_bus": r10k(car["new_bus"]), "new_open": r10k(car["new_open"])},
                    "thorough": figs["new_split"]}},
        {"id": "R6", "name": "Dec 2027 commitment (80 per cent)", "graded_as": "Recommendation",
         "figure": "commitment", "depends": ["R2", "R3", "R4", "R5"], "independent": "",
         "golden": figs["commitment"], "band": [figs["commitment_lo"], figs["commitment_hi"]],
         "passes": {"quick": figs["quick_commitment"], "careful": r100k(car["p20"]), "thorough": figs["commitment"]}},
        {"id": "R7", "name": "monthly path Nov 2026 to Dec 2027", "graded_as": "Ask 2", "figure": "path_table",
         "depends": ["R1", "R2", "R3", "R4", "R5"], "independent": "", "golden": path_g, "bands": path_bands,
         "partly_share": 0.5,
         "passes": {"quick": path_q, "careful": path_c, "thorough": path_g}},
    ]
    routes = [{"name": "golden", "answer": figs["commitment"], "golden": True},
              {"name": "quick: trailing growth carried forward", "answer": figs["quick_commitment"]},
              {"name": "careful but hurried", "answer": r100k(car["p20"])}]
    for k, v in R.items():
        if v.get("kind") == "hurried":
            routes.append({"name": k, "answer": r100k(v["p20"])})
    hints = []
    for k, v in R.items():
        if v.get("kind") != "hint":
            continue
        now = values(v, figs, months)
        resc = [r["id"] for r in res if grade(r, r["passes"]["careful"]) != "right" and grade(r, now[r["id"]]) == "right"]
        hints.append({"sentence": v["sentence"], "rescues": resc})
    return {"results": res, "hints": hints, "routes": routes}


def write(F, B, g, R, figs):
    out = build(F, B, g, R, figs)
    json.dump(out, open(os.path.join(HERE, "effort.json"), "w"), indent=1, ensure_ascii=False, sort_keys=True)
    return out


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    F, B, g, R = GD.compute(target)
    figs = WU.figures(F, B, g, R)
    write(F, B, g, R, figs)
    print("effort.json written")
