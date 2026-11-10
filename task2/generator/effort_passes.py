"""task2 architecture 6: effort.json, the three passes of the client's effort test run end to end on the cut pack by
the generator's own implementations of named methods (never a solver; nothing reads the prompt).

  quick     the quality reports and the record: the 2026 share carried into 2027, each university hospital at its own
            late-2026 share, Ballykeel's last quarter's dictations carried, the bridge's whole change put to the releases
  careful   what the platform's runs did on this world's last architecture: every Layer 1 item cleaned and every move
            linked, the releases measured within clinicians, clinicians typed by their start against the compulsory
            date and split by appointment, the 2027 starters given the smaller hospitals' compelled clinicians' rate,
            every clinician starting on the date at their own first months' volume, no hospital effect
  thorough  the golden"""
import json
import math
import os
from collections import defaultdict

import numpy as np

import golden as GD
import world as W


def r1(x, nd=1):
    return round(100 * x, nd)


def results_figs(X):
    """the graded figures a pass files, at the precision the answer blocks state them"""
    B = X["bridge"]
    return {
        "r1_bridge_ends": {"start": r1(B["start"]), "end": r1(B["end"])},
        "r2_bridge_split": {"releases": r1(B["releases"]), "mix": r1(B["mix"])},
        "r3_hospital_effects": {h: round(100 * (math.exp(X["F"]["site"][h]) - 1), 1) for h in W.TEACHING},
        "r4_starters_share": {h: r1(X["U"][h]["h_ent"]) for h in W.TEACHING},
        "r5_bku_q4_dictations": int(round(X["hq"]["BKU"]["vol"], -3)),
        "r6_univ_q4_share": {h: r1(X["hq"][h]["share"]) for h in W.TEACHING},
        "r7_lowest_ceilings": list(X["bands"]),
        "r8_p90_q4": r1(X["p90"]),
        "r9_ceiling": X["ceiling"],
    }


def quick(P, G):
    """the ten-minute pass"""
    acc = defaultdict(list)
    for a in P.audits:
        if W.mi(2026, 10) <= a["t"] <= GD.DEC:
            acc[a["site"]].append(a["wer"] > W.LINE)
    own = {h: float(np.mean(v)) for h, v in acc.items()}
    bku = sum(n for s, ser in P.vol.items() for t, n in ser.items()
              if GD.DEC - 2 <= t <= GD.DEC and P.site_of[(s, t)] == "BKU")
    q4 = np.sort([a["wer"] for a in P.audits if W.mi(2026, 10) <= a["t"] <= GD.DEC])
    steady = GD.route(P, G, "steady")
    B = G["bridge"]
    return {
        "r1_bridge_ends": {"start": r1(B["start"]), "end": r1(B["end"])},
        "r2_bridge_split": {"releases": r1(B["change"]), "mix": 0.0},
        "r3_hospital_effects": None,
        "r4_starters_share": None,
        "r5_bku_q4_dictations": int(round(bku, -3)),
        "r6_univ_q4_share": {h: r1(own[h]) for h in W.TEACHING},
        "r7_lowest_ceilings": [GD.band(x) for x in steady],
        "r8_p90_q4": r1(float(q4[int(0.9 * len(q4))])),
        "r9_ceiling": GD.band(max(steady)),
    }


SPEC = [
    ("R1", "the audited share at the bridge's two ends, from the cleaned audits tied to the quarterly reports",
     "Ask 7", "r1_bridge_ends", [], "", {"start": (0.05,), "end": (0.05,)}),
    ("R2", "the 2023 to 2026 change split into the releases and the mix of dictations", "Component 4", "r2_bridge_split",
     ["R1"], "", None),
    ("R3", "each university hospital's own effect on a clinician's word error, against the six smaller hospitals",
     "Component 1", "r3_hospital_effects", [], "", None),
    ("R4", "the heavy-correction share of each university hospital's 2027 starters", "Component 2",
     "r4_starters_share", ["R3"], "", None),
    ("R5", "Ballykeel University Hospital's fourth-quarter dictations", "Ask 5", "r5_bku_q4_dictations", [],
     "independent: the six past go-lives' volumes and the register's staff in post", None),
    ("R6", "each university hospital's expected fourth-quarter share", "Ask 4", "r6_univ_q4_share",
     ["R3", "R4", "R5"], "", None),
    ("R7", "each 2027 quarter's lowest ceiling", "Ask 3", "r7_lowest_ceilings", ["R6"], "", None),
    ("R8", "the word error rate nine in ten fourth-quarter dictations stay under", "Ask 6", "r8_p90_q4",
     ["R4", "R5"], "", None),
    ("R9", "the ceiling", "Recommendation", "r9_ceiling", ["R7"], "", None),
]


def build(C, F):
    """effort.json from the checks' golden, routes and figures (F is figures.json's content)"""
    P, G = C["P"], C["G"]
    bands = C["bands_stated"]
    gold = {k: F["results"][k] for k in F["results"]}
    careful_X = C["full_routes"]["careful but hurried: the compelled rate, own first months, no hospital effect"]
    passes = {"quick": quick(P, G), "careful": results_figs(careful_X), "thorough": results_figs(G)}
    # the careful pass measures the releases within clinicians (its own bridge, the same as the golden's)
    passes["careful"]["r1_bridge_ends"] = gold["r1_bridge_ends"]
    passes["careful"]["r2_bridge_split"] = gold["r2_bridge_split"]
    passes["careful"]["r3_hospital_effects"] = {"value": None, "grade": "missed",
                                                "why": "no hospital effect estimated: the university hospitals' "
                                                       "dictators read at the smaller hospitals' acoustic level"}
    results = []
    for rid, name, graded_as, key, deps, indep, _ in SPEC:
        r = {"id": rid, "name": name, "graded_as": graded_as, "figure": key, "depends": deps, "independent": indep,
             "golden": gold[key]}
        b = bands.get(key)
        if isinstance(gold[key], dict):
            r["bands"] = {k: list(v) for k, v in b.items()}
        elif isinstance(gold[key], list):
            r["ordered"] = True
        elif b is not None:
            r["band"] = list(b["band"])
            if "partly" in b:
                r["partly"] = list(b["partly"])
        r["passes"] = {p: passes[p][key] for p in ("quick", "careful", "thorough")}
        results.append(r)
    hints = [
        {"sentence": "A university hospital's 2027 starters are most of its staff, so they look like the smaller "
                     "hospitals' whole staffs rather than their compelled clinicians.", "rescues": []},
        {"sentence": "The hospitals' own effects on error show in the clinicians who moved between them.",
         "rescues": ["R3"]},
        {"sentence": "At every go-live the departments switch over one after another for about four months.",
         "rescues": ["R5"]},
    ]
    routes = [{"name": "the golden", "answer": G["ceiling"], "golden": True}]
    for k, (v, c) in C["routes"].items():
        routes.append({"name": k, "answer": c if c is not None else "none"})
    for k, X in C["full_routes"].items():
        routes.append({"name": k, "answer": X["ceiling"] if X["ceiling"] is not None else "none"})
    return {"results": results, "hints": hints, "routes": routes,
            "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}


def write(C, F, gen_dir):
    E = build(C, F)
    with open(os.path.join(gen_dir, "effort.json"), "w", encoding="utf-8") as fh:
        json.dump(E, fh, indent=1, ensure_ascii=False, default=lambda o: o.item() if hasattr(o, "item") else str(o))
    return E
