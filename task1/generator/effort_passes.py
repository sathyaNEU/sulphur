"""effort.json: the client's effort test computed on the cut pack. Each pass is the author's implementation of named
methods, run end to end on the shipped files; nothing reads the prompt.

  quick      ten minutes: every exported row charged in October counted; each start's own subscription only;
             each offer's share leaving at the end of the intro over everything on file; the starts of three years
             earlier as they turned out; no response to the April 2027 rise; each line's 2023 starts' realised
             36-month revenue as its 2027 value
  careful    what a frontier run does unprompted: every file cleaned; the end-of-intro model by offer, channel and
             title with a term for the jump after April 2025; young starts completed on each channel's older
             starts' survival; the April 2025 rise's excess read from April on and pooled over tenure; later
             subscriptions on the same customer number
  thorough   the golden
"""
import json
import os

import golden as GD
import params as P

HINTS = [
    ("the newest social and partner starts read far less in their first months than earlier ones",
     "careful, reading used"),
    ("the April 2025 rise also raised the share leaving at the end of the introductory price",
     "careful, full price carried"),
    ("households that leave often come back under a new customer number, with the same payment method or address",
     "careful, households linked"),
    ("the April 2025 rise's cancellations began with the notice letters and were heaviest in the first paid year",
     "careful, the 2025 rise read in full"),
]

SPEC = [
    ("R1", "paying digital subscribers at 31 Oct 2026 by title", "paying_oct", "Ask 1", [], 1.0),
    ("R2", "Jul-Sep 2023 starts: 36-month net revenue per start by channel", "value_2023q3", "Component 4", [], 1.0),
    ("R3", "share leaving at the end of the intro, 2027 offers, 2026 prices", "stepup_share", "Ask 3", [], 100.0),
    ("R4", "points the April 2027 prices add at the end of the intro", "stepup_added", "Component 3", [], 100.0),
    ("R5", "Nov 2025-Apr 2026 starts still paying three years in, by channel", "survival_36", "Component 2", [], 100.0),
    ("R6", "extra cancellations from the April 2027 rise by Dec 2027, by title", "rise_extra", "Ask 4", [], 1.0),
    ("R7", "expected 36-month net revenue per start, every 2027 line", "line_value", "Component 1",
     ["R3", "R4", "R5"], 1.0),
    ("R8", "the funded lines and the budget they need", "funded", "Recommendation", ["R7"], None),
    ("R9", "the plan's 2027 starts paying at 31 Dec 2027, by channel", "plan_paying", "Ask 2", [], 1.0),
]


def scaled(r, d, scale):
    if scale is None:
        return d
    out = {}
    for k, v in d.items():
        x = v * scale
        out[GD.key(k)] = round(x, 1) if scale == 100.0 else int(round(x))
    return out


def build(G, path):
    g, rt, q = G["golden"], G["routes"], G["quick"]
    res = []
    for rid, name, fig, graded, dep, scale in SPEC:
        if rid == "R8":
            entry = {"id": rid, "name": name, "figure": fig, "graded_as": graded, "depends": dep, "independent": "",
                     "golden": [GD.key(l) for l in g["R8"]],
                     "passes": {"quick": [GD.key(l) for l in q["R8"]],
                                "careful": [GD.key(l) for l in rt["careful"]["R8"]],
                                "thorough": [GD.key(l) for l in g["R8"]]}}
        else:
            b = G["bands"][rid]
            bands = {GD.key(k): [round(lo * scale, 2), round(hi * scale, 2)] for k, (lo, hi) in b.items()}
            entry = {"id": rid, "name": name, "figure": fig, "graded_as": graded, "depends": dep, "independent": "",
                     "golden": scaled(rid, g[rid], scale), "bands": bands, "partly_share": 0.5,
                     "passes": {"quick": scaled(rid, q[rid], scale), "careful": scaled(rid, rt["careful"][rid], scale),
                                "thorough": scaled(rid, g[rid], scale)}}
        res.append(entry)
    hints = []
    for sentence, route in HINTS:
        r = rt[route]
        rescued = []
        for e in res:
            rid = e["id"]
            if rid == "R8":
                ok_c = sorted(GD.key(l) for l in rt["careful"]["R8"]) == sorted(e["golden"])
                ok_h = sorted(GD.key(l) for l in r["R8"]) == sorted(e["golden"])
            else:
                scale = [s for s in SPEC if s[0] == rid][0][5]
                bands = e["bands"]
                ok_c = all(bands[k][0] <= v <= bands[k][1] for k, v in scaled(rid, rt["careful"][rid], scale).items())
                ok_h = all(bands[k][0] <= v <= bands[k][1] for k, v in scaled(rid, r[rid], scale).items())
            if ok_h and not ok_c:
                rescued.append(rid)
        hints.append({"sentence": sentence, "rescues": rescued})
    hints.sort(key=lambda h: -len(h["rescues"]))
    routes_ = [{"name": "the golden", "answer": [GD.key(l) for l in g["R8"]], "golden": True}]
    for nm in ["careful"] + [n for n in rt if n != "careful"]:
        routes_.append({"name": nm, "answer": [GD.key(l) for l in rt[nm]["R8"]]})
    E = {"results": res, "hints": hints, "routes": routes_,
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    json.dump(E, open(path, "w"), indent=1, sort_keys=True, ensure_ascii=False)
    return E
