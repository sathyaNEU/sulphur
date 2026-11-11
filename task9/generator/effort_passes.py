"""task9 (architecture 10): generator/effort.json. Each result's golden and band, and the value each pass files,
computed end to end by analysis.py's routes on the cut pack (figures.py runs them; this file lays them out). None
reads the prompt. effort.py grades them and prices the rubric.

  quick      the desk's month-end summaries: the base year's next-day view carried to 2027, the draft's tightening
             taken as spread given up on the trades the desk already wins
  careful    re-priced on the determinism judge's blind first pass, which recovered rivals' levels from the tape on
             its own: the replay on the tape's levels, each trade's cost read a week on, the trades a tighter quote adds
             costed like the desk's own wins, the year's range from single days (the first pricing, a win model fitted on
             the desk's own quotes, stays among the routes)
  thorough   the golden
"""
# id, name, block, depends, independent input, the figures key, its kind
CHAIN = [
    ("R1", "each changed segment's cost after the trades the current schedule wins, USD a million", "Ask 4", [],
     "the record replayed at the current schedule and the evaluations",
     "won_cost", "table"),
    ("R2", "each changed segment's share of requests won at the draft's quote", "Ask 3", [], "the requests, the covers and the tape",
     "share", "table"),
    ("R3", "the cost after the trades the draft's quote would add, USD a million", "Component 2", ["R2"], "", "add_cost", "table"),
    ("R4", "the 2027 P&L at the current schedule", "Component 3", [], "the record replayed at the current schedule", "current",
     "number"),
    ("R5", "the 2027 P&L at the draft schedule", "Component 1", ["R2", "R3", "R4"], "", "proposed", "number"),
    ("R6", "the draft's 80 per cent range", "Ask 1", ["R5"], "", "range", "table"),
    ("R7", "the difference by changed segment", "Ask 2", ["R2", "R3"], "", "bridge", "table"),
    ("R8", "the changed segments that lose money, and the plan", "Recommendation", ["R7"], "", "rec", "rec"),
]
PARTLY = 0.15          # a P&L figure within 15 per cent of the golden's band is Partly


def set_grade(flag, F):
    core = set(F["gold"]["lose"])
    either = set(F.get("lose_either", []))
    if flag is None:
        return "missed", "no list filed"
    f = set(flag)
    if core - either <= f <= core | either:
        return "right", "names every changed segment that loses money (%d) and none that pays" % len(core)
    a, b = f - either, core - either
    share = len(a & b) / float(len(a | b) or 1)
    return ("partly" if share >= 0.5 else "missed"), "%d of the %d losing segments named, %d paying segments named" % (
        len(f & core), len(core), len(f - core - either))


def _in(v, b):
    return v is not None and b[0] <= v <= b[1]


def entry(rid, route, F):
    """A pass's value for one result, as effort.py reads it."""
    key, kind = next((c[5], c[6]) for c in CHAIN if c[0] == rid)
    if route is None:
        return None
    if kind == "table" and key == "range":
        return None if route.get("p10") is None else {"P10": route["p10"], "P90": route["p90"]}
    if kind == "table":
        return route.get(key)
    if kind == "number":
        return route.get(key)
    if kind == "rec":
        g, why = set_grade(route.get("lose"), F)
        plan_ok = _in(route.get("adopt"), F["bands"]["adopt"])
        grade = "right" if (g == "right" and plan_ok) else ("partly" if (g == "right" or plan_ok) else "missed")
        return {"value": {"plan": route.get("adopt"), "drop": route.get("lose")}, "grade": grade,
                "why": "plan %s the band; %s" % ("inside" if plan_ok else "outside", why)}


def quick_pass(F):
    q = F["quick"]
    return {"won_cost": q["won_cost"], "share": q["share"], "add_cost": q["won_cost"], "current": q["current"],
            "proposed": q["proposed"], "p10": None, "p90": None, "bridge": q["bridge"], "lose": q["lose"], "adopt": q["adopt"]}


CAREFUL = "the tape's levels, a week's marks, today's wins' cost for the added trades"   # re-priced on the judge's first pass
HINTS = [
    ("The level a rival won a request at is on the public tape, a minute after the request", CAREFUL),
    ("Ashcote's evaluations of thinner bonds catch up with the market only at the month-end review",
     "the tape's levels, complete moves, today's wins' cost for the added trades, days one at a time"),
    ("The requests a tighter quote adds are not the requests the desk wins today", "the tape's levels, a week's marks"),
    ("A year of this desk's P&L is not a year of independent days",
     "the tape's levels, a week's marks, today's wins' cost for the added trades, the year in blocks"),
]
COMPOUNDS = [
    ("complete moves and the added trades' own cost", "the golden's figures, days drawn one at a time"),
    ("complete moves and the year in blocks", "the tape's levels, today's wins' cost for the added trades"),
    ("complete moves, the added trades' own cost and the year in blocks", None),
]


def build(F):
    R = F["routes"]
    gold = dict(F["gold"])
    passes = {"quick": quick_pass(F), "careful": R[CAREFUL], "thorough": gold}
    results = []
    for rid, name, graded_as, depends, independent, key, kind in CHAIN:
        e = {"id": rid, "name": name, "graded_as": graded_as, "figure": key, "depends": depends, "independent": independent}
        if kind == "table" and key == "range":
            e["golden"] = {"P10": gold["p10"], "P90": gold["p90"]}
            e["bands"] = {"P10": F["bands"]["p10"], "P90": F["bands"]["p90"]}
        elif kind == "table":
            e["golden"] = gold[key]
            e["bands"] = F["bands"][key]
        elif kind == "number":
            e["golden"] = gold[key]
            b = F["bands"][key]
            w = PARTLY * abs(gold[key])
            e["band"], e["partly"] = b, [b[0] - w, b[1] + w]
        else:
            e["golden"] = {"plan": gold["adopt"], "drop": gold["lose"]}
        e["passes"] = {p: entry(rid, v, F) for p, v in passes.items()}
        results.append(e)
    careful = R[CAREFUL]

    def grade_of(rid, route):
        import importlib.util
        import os
        spec = importlib.util.spec_from_file_location("effort", os.path.join(os.path.dirname(__file__), "..", "..", ".claude",
                                                                             "skills", "stumping", "effort.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        res = next(r for r in results if r["id"] == rid)
        return mod.grade(entry(rid, route, F), res)[0]

    def rescued(route):
        return [c[0] for c in CHAIN if grade_of(c[0], careful) != "right" and grade_of(c[0], route) == "right"]
    hints = [{"sentence": s, "rescues": rescued(R[name])} for s, name in HINTS]
    compounds = [{"moves": s, "rescues": rescued(R[name] if name else gold)} for s, name in COMPOUNDS]
    routes = [{"name": "the golden", "answer": {"plan": round(gold["adopt"], -4), "drop": gold["lose"]}, "golden": True},
              {"name": "the desk's month-end summaries", "answer": {"plan": round(F["quick"]["adopt"], -4), "drop": F["quick"]["lose"]}}]
    for k, v in R.items():
        routes.append({"name": k, "answer": {"plan": round(v["adopt"], -4), "drop": v["lose"]}})
    return {"results": results, "hints": hints, "compounds": compounds, "routes": routes}
