"""effort.json: the client's effort test computed on the cut pack (python3 effort_passes.py [target]). Each pass is
the author's implementation of a named method, run end to end on the shipped files; nothing reads the prompt.

  quick      the pilot's average consumption on January-like days times each duty's km, against 85 per cent of the
             quoted battery; planning loads as the bridge's mean net weight over everything weighed
  careful    what both architecture 7 platform runs did: every file cleaned, each declaration taken to its weighed
             equivalent, a curved cold form, the loss net of the cold, the square of speed fitted and each duty fed
             its routing-tool speed at the year's actual-to-planned ratio; the pilot's energy carried per km and per
             tonne of departing payload, the trailer each day pulled never read
  thorough   the golden

Each hint is executed literally: the careful pass with that one step done right, its results graded like the
passes; a hint rescues the results it turns from not Right to Right.
"""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A
import golden as GD

r10 = GD.r10


def main(target):
    pk = A.load(target)
    g = A.golden(pk)
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    R = A.routes(pk)
    gp = A.payloads(pk, "shipper")
    L = g["limit"]

    def energies(a):
        return {c: r10(a[c]["kwh"]) for c in sorted(a)}

    def verdicts(a):
        return {c: "yes" if a[c]["go"] else "no" for c in sorted(a)}

    def tru_set(m, inp):
        if not m["o"]["tru"]:
            return []
        k = "epto" if m["o"]["tru"] == "epto" else "reefer"
        return sorted(c for c in pk.short if inp[c][k] == 1.0)

    def build(m, lm, ratio):
        a = A.assess(pk, m, lim=lm)
        inp = g["inputs"]
        cells = {}
        for c in ("V02", "V14"):
            cells["%s combination t" % c] = round(inp[c]["combo"], 1) if m["o"]["tare"] else round(g["pilot_combo"], 1)
        for c in ("V03", "V11"):
            cells["%s load share" % c] = round(inp[c]["phi"], 2) if m["o"]["drops"] == "yes" else 1.0
        return {"R1": round(A.slope_per_100(m), 1), "R2": None, "R3": tru_set(m, inp), "R4": round(ratio, 2),
                "R5": cells, "R6": energies(a), "R7": verdicts(a), "R8": A.chosen(a)}

    gold = build(g["model"], L, A.speed_ratio(pk))
    cm, cl = R["careful but hurried"]
    car = build(cm, cl, A.speed_ratio(pk, how="mean"))
    car["R2"] = figs["loss_pct"]
    gold["R2"] = figs["loss_pct"]
    # quick
    qa, _ = A.rung0(pk)
    quick = {"R1": None, "R2": None, "R3": [], "R4": None, "R5": None, "R6": energies(qa), "R7": verdicts(qa),
             "R8": A.chosen(qa)}

    res = [
        {"id": "R1", "name": "payload term, kWh per t per 100 loaded km", "graded_as": "Component 1",
         "figure": "payload_term", "depends": [], "independent": "", "golden": figs["payload_term"],
         "band": [2.0, 2.4], "partly": [1.8, 2.6]},
        {"id": "R2", "name": "first-year battery loss, per cent", "graded_as": "Component 2", "figure": "loss_pct",
         "depends": [], "independent": "", "golden": figs["loss_pct"], "band": [3.6, 4.0], "partly": [2.8, 4.8]},
        {"id": "R3", "name": "the duties whose fridge unit draws from the battery", "graded_as": "Component 3",
         "figure": "fridge_set", "depends": [], "independent": "", "golden": figs["fridge_set"]},
        {"id": "R4", "name": "actual over planned speed on a -5 C day", "graded_as": "Component 4",
         "figure": "speed_ratio_design", "depends": [], "independent": "", "golden": figs["speed_ratio_design"],
         "band": [0.75, 0.79], "partly": [0.72, 0.82]},
        {"id": "R5", "name": "the combination's weight and the load's share of the loaded run",
         "graded_as": "Component 5", "figure": "combination_and_drops", "depends": [], "independent": "",
         "golden": figs["combination_and_drops"],
         "bands": {k: ([v - 0.3, v + 0.3] if k.endswith("t") else [v - 0.03, v + 0.03])
                   for k, v in figs["combination_and_drops"].items()}},
        {"id": "R6", "name": "the 14 design-day energies", "graded_as": "Ask 1", "figure": "energy",
         "depends": ["R1", "R3", "R4", "R5"], "independent": "", "golden": figs["energy"],
         "bands": {c: [v - 10, v + 10] for c, v in figs["energy"].items()}},
        {"id": "R7", "name": "each duty's verdict", "graded_as": "Ask 2", "figure": "verdict",
         "depends": ["R2", "R6"], "independent": "", "golden": figs["verdict"]},
        {"id": "R8", "name": "the order", "graded_as": "Recommendation", "figure": "call_set",
         "depends": ["R2", "R6"], "independent": "", "golden": figs["call_set"]},
    ]
    for r in res:
        r["passes"] = {"quick": quick[r["id"]], "careful": car[r["id"]], "thorough": gold[r["id"]]}
        if r["id"] == "R8":
            for p in ("quick", "careful"):
                v = r["passes"][p]
                if v != r["golden"]:
                    r["passes"][p] = {"value": v, "grade": "missed",
                                      "why": "the order is graded as the count and the duties; %d is not %d" %
                                             (len(v), len(r["golden"]))}
    # the hints, executed: the careful pass with one step done right
    one = {
        "the duties drive slower than the routing tool plans on a -5 C day than over the year":
            (A.fit(pk, gp, A.H2, vmode="hinge10", **A.HURRIED), A.speed_ratio(pk)),
        "on the ePTO trailers the fridge unit runs from the tractor's battery for as long as the duty is out":
            (A.fit(pk, gp, A.H2, vmode="mean", tare=None, drops="no"), A.speed_ratio(pk, how="mean")),
        "a multi-drop duty's load comes off along the loaded run":
            (A.fit(pk, gp, A.H2, vmode="mean", tare=None, tru=None), A.speed_ratio(pk, how="mean")),
        "a tonne of trailer costs on every leg what a tonne of payload costs on the loaded leg":
            (A.fit(pk, gp, A.H2, vmode="mean", tru=None, drops="no"), A.speed_ratio(pk, how="mean")),
    }
    sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "stumping"))
    import effort as EF
    hints = []
    for sent, (m, ratio) in one.items():
        h = build(m, L, ratio)
        h["R2"] = figs["loss_pct"]
        rescued = []
        for r in res:
            gc = EF.grade(car[r["id"]], r)[0]
            gh = EF.grade(h[r["id"]], r)[0]
            if gh == "right" and gc != "right":
                rescued.append(r["id"])
        hints.append({"sentence": sent, "rescues": rescued, "order": len(h["R8"])})
    routes = []
    for k, (m, lm) in R.items():
        aa = A.assess(pk, m, lim=lm)
        routes.append({"name": k, "answer": A.chosen(aa), "golden": k == "golden"})
    routes.append({"name": "quick (average cold-day consumption)", "answer": A.chosen(qa), "golden": False})
    out = {"results": res, "hints": hints, "routes": routes}
    json.dump(out, open(os.path.join(HERE, "effort.json"), "w"), indent=1, ensure_ascii=False, sort_keys=True)
    print("effort.json: careful order %d, quick order %d; hints rescue %s" %
          (len(car["R8"]), len(quick["R8"]), [len(h["rescues"]) for h in hints]))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
