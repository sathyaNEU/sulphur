"""task8: effort.json, the client's effort test computed on the cut pack. Each pass is the author's implementation of
named methods, run end to end on the shipped files; nothing reads the prompt.

  quick      ten minutes: every exported row's own standardised score below 85, by the academy on the row; no
             conversion, no July adjustment, no gain
  careful    what a frontier run does unprompted: every file cleaned and joined, the policy's valid-sitting rule, the
             other tests put on the Lexis basis through KS2 by the textbook chained equipercentile link, the Brightway
             trial's pairs taken as they stand and the July transition-day sittings taken as entry reading
  thorough   the golden
"""
import json

import params as P
import results as R

HINTS = [
    ("the Brightway academies sat their Lexis trial after their own test, except some tutor groups",
     "careful, the trial's second sitting corrected"),
    ("four Lexis academies tested their intake at the July transition day", "careful, the July sittings brought to September"),
]

# (id, name, figures key, graded as, depends, precedents for a careful-column loss)
SPEC = [
    ("R1", "students with a valid entry sitting by the census, by academy", "valid_by_academy", "Ask 1", [], []),
    ("R2", "the Lexis trial's second-sitting gain", "second_sitting_gain", "Component 1", [], ["L07", "L04"]),
    ("R3", "Lexis score of Brightway results at six points", "brightway_lexis", "Ask 2", ["R2"], ["L28", "L30"]),
    ("R4", "Lexis score of Quill results at six points", "quill_lexis", "Ask 3", [], ["L25", "L10"]),
    ("R5", "the July transition-day level above the start of Year 7", "july_level", "Component 2", [], ["L07", "L04"]),
    ("R6", "Reading Forward students by academy", "programme", "Ask 4", ["R3", "R4", "R5"], ["L07", "L06"]),
    ("R7", "the change from each academy's own-test list, by test", "change_by_test", "Ask 5", ["R6"], ["L07", "L06"]),
    ("R8", "the trust's tutor hours, cost and range", "hours_total", "Recommendation", ["R6"], ["L28", "L31"]),
    ("R9", "tutor hours a week by academy", "hours", "Ask 6", ["R6"], ["L07", "L06"]),
]


def value(rid, r, F=None):
    if rid == "R1":
        return {a: int(v) for a, v in r["R1"].items()}
    if rid == "R2":
        return round(float(r["R2"]), 1)
    if rid == "R3":
        return {str(x): round(float(v), 1) for x, v in r["R3"].items()}
    if rid == "R4":
        return {str(x): round(float(v), 1) for x, v in r["R4"].items()}
    if rid == "R5":
        return round(float(r["R5"]), 1)
    if rid == "R6":
        return {a: int(v) for a, v in r["R6"].items()}
    if rid == "R7":
        return {k: int(v) for k, v in r["R7_test"].items()}
    if rid == "R8":
        return round(float(r["R8_hours"]), 1)
    if rid == "R9":
        return {a: round(float(v), 1) for a, v in r["R9"].items()}


def bands_of(rid, F):
    b = F["bands"]
    if rid == "R1":
        return None
    if rid == "R2":
        return b["R2"]
    if rid == "R3":
        return b["R3"]
    if rid == "R4":
        return b["R4"]
    if rid == "R5":
        return b["R5"]
    if rid == "R6":
        return b["R6"]
    if rid == "R7":
        return b["R7_test"]
    if rid == "R8":
        return b["R8_hours"]
    if rid == "R9":
        return b["R9"]


def build(G, F, path):
    g, rt, q = G["golden"], G["routes"], G["quick"]
    res = []
    for rid, name, fig, graded, dep, prec in SPEC:
        gold = value(rid, g)
        e = {"id": rid, "name": name, "figure": fig, "graded_as": graded, "depends": dep, "independent": "",
             "golden": gold, "passes": {"thorough": gold, "careful": value(rid, rt["careful"])}}
        bnd = bands_of(rid, F)
        if isinstance(gold, dict):
            if bnd:
                e["bands"] = {k: list(v) for k, v in bnd.items()}
            e["partly_share"] = 0.5
        elif bnd:
            e["band"] = list(bnd)
        if prec:
            e["precedent"] = prec
        # the quick pass: own standardised scores on raw rows, no conversion, no adjustment
        if rid == "R1":
            e["passes"]["quick"] = {a: int(v) for a, v in q["R1"].items()}
        elif rid == "R2":
            e["passes"]["quick"] = 0.0
        elif rid in ("R3", "R4"):
            e["passes"]["quick"] = {str(x): float(x) for x in R.POINTS}
        elif rid == "R5":
            e["passes"]["quick"] = 0.0
        elif rid == "R6":
            e["passes"]["quick"] = {a: int(v) for a, v in q["R6"].items()}
        elif rid == "R7":
            e["passes"]["quick"] = {k: 0 for k in g["R7_test"]}
        elif rid == "R8":
            e["passes"]["quick"] = round(float(q["R8_hours"]), 1)
        elif rid == "R9":
            e["passes"]["quick"] = {a: round(float(v), 1) for a, v in q["R9"].items()}
        res.append(e)
    hints = []
    for sentence, route in HINTS:
        r = rt[route]
        rescued = []
        for e in res:
            v_c, v_h = e["passes"]["careful"], value(e["id"], r)
            if ok(e, v_h) and not ok(e, v_c):
                rescued.append(e["id"])
        hints.append({"sentence": sentence, "rescues": rescued})
    hints.sort(key=lambda h: -len(h["rescues"]))
    routes_ = [{"name": "the golden", "answer": g["R6"], "golden": True}]
    for nm in ["careful"] + [n for n in rt if n != "careful"]:
        routes_.append({"name": nm, "answer": rt[nm]["R6"]})
    fam = [{"name": nm, "value": round(r["R8_cost"], 2)} for nm, r in G["rivals"].items()]
    sc = [{"name": nm, "value": round(r["R8_cost"], 2)} for nm, r in rt.items() if nm in (
        "careful", "the trial's pairs as they stand", "the July sittings as entry reading",
        "the other tests' standardised scores read as Lexis scores", "Quill predicted from KS2 by regression")]
    E = {"results": res, "hints": hints, "routes": routes_,
         "forcing": {"kind": "numeric", "line": P.PROVISIONAL_BUDGET, "golden_side": "above",
                     "golden_family": fam, "shortcuts": sc, "perturbations": G.get("perturbations", [])},
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    json.dump(E, open(path, "w"), indent=1, sort_keys=True, ensure_ascii=False)
    return E


def ok(e, v):
    if isinstance(e["golden"], dict):
        b = e.get("bands") or {}
        cells = [(k, gv) for k, gv in e["golden"].items()]
        good = sum(1 for k, gv in cells if (b.get(k) and b[k][0] <= v.get(k, -1e9) <= b[k][1]) or (not b.get(k) and v.get(k) == gv))
        return good == len(cells)
    if "band" in e:
        return e["band"][0] <= v <= e["band"][1]
    return v == e["golden"]
