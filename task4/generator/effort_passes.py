"""effort.json: the client's effort test computed on the cut pack (python3 effort_passes.py [target]). Each pass is
the author's implementation of a named method, run end to end on the shipped files; nothing reads the prompt.

  quick      the pilot's average consumption on January-like days times each duty's km, against 85 per cent of the
             quoted battery; planning loads as the bridge's mean net weight over everything weighed
  careful    what the architecture 6 platform run did: every file cleaned, each declaration taken to its weighed
             equivalent, a curved cold form, the loss net of the cold; energy forecast in proportion to distance at
             the pilot's own speeds (no speed term), the transfer to the Varnamo duties' faster runs left untested
  thorough   the golden
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
    gold_a = g["assess"]

    def energies(a):
        return {c: r10(a[c]["kwh"]) for c in sorted(a)}

    def verdicts(a):
        return {c: "yes" if a[c]["go"] else "no" for c in sorted(a)}

    # quick
    qa, _ = A.rung0(pk)
    q_loads = {}
    for c in sorted(pk.short):
        v = [r["net"] for r in pk.wb if r["duty"] == c]
        q_loads[c] = round(float(np.mean(v)) / 1000, 1)
    # careful
    cm, cl = R["careful but hurried"]
    ca = A.assess(pk, cm, lim=cl)
    c_loss = round(100 * A.fade(pk, "age"), 1)

    res = [
        {"id": "R1", "name": "payload term, kWh per t per 100 km", "graded_as": "Component 1",
         "figure": "payload_term", "depends": [], "independent": "",
         "golden": figs["payload_term"], "band": [1.9, 2.1], "partly": [1.6, 2.4],
         "passes": {"quick": None, "careful": figs["payload_term"], "thorough": figs["payload_term"]}},
        {"id": "R2", "name": "first-year battery loss, per cent", "graded_as": "Component 2", "figure": "loss_pct",
         "depends": [], "independent": "",
         "golden": figs["loss_pct"], "band": [3.6, 4.0], "partly": [2.8, 4.8],
         "passes": {"quick": None, "careful": figs["loss_pct"], "thorough": figs["loss_pct"]}},
        {"id": "R3", "name": "the 14 design-day energies", "graded_as": "Ask 1", "figure": "energy",
         "depends": ["R1"], "independent": "",
         "golden": figs["energy"], "bands": {c: [v - 10, v + 10] for c, v in figs["energy"].items()},
         "passes": {"quick": energies(qa), "careful": energies(ca), "thorough": figs["energy"]}},
        {"id": "R4", "name": "each duty's verdict", "graded_as": "Ask 2", "figure": "verdict",
         "depends": ["R2", "R3"], "independent": "", "golden": figs["verdict"],
         "passes": {"quick": verdicts(qa), "careful": verdicts(ca), "thorough": figs["verdict"]}},
        {"id": "R5", "name": "the order", "graded_as": "Recommendation", "figure": "call_set",
         "depends": ["R2", "R3"], "independent": "", "golden": figs["call_set"],
         "passes": {"quick": A.chosen(qa), "careful": A.chosen(ca), "thorough": figs["call_set"]}},
    ]
    # a result's list grade: Partly when half the union is shared; the order is graded exactly
    for r in res:
        if r["id"] == "R5":
            for p in ("quick", "careful"):
                v = r["passes"][p]
                if v != r["golden"]:
                    r["passes"][p] = {"value": v, "grade": "missed",
                                      "why": "the order is graded as the count and the duties; %d is not %d" %
                                             (len(v), len(r["golden"]))}
    routes = []
    for k, (m, lm) in R.items():
        aa = A.assess(pk, m, lim=lm)
        routes.append({"name": k, "answer": A.chosen(aa), "golden": k == "golden"})
    routes.append({"name": "quick (average cold-day consumption)", "answer": A.chosen(qa), "golden": False})
    hints = [
        {"sentence": "the Värnamo duties drive faster than the pilot, and energy per km rises with speed",
         "rescues": []},
        {"sentence": "the routing tool's driving times are optimistic, more so in winter", "rescues": []},
        {"sentence": "the shippers' declared weights scatter around what the trucks carry", "rescues": []},
    ]
    out = {"results": res, "hints": hints, "routes": routes}
    json.dump(out, open(os.path.join(HERE, "effort.json"), "w"), indent=1, ensure_ascii=False, sort_keys=True)
    print("effort.json: careful order %d, quick order %d" % (len(A.chosen(ca)), len(A.chosen(qa))))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
