"""task9: generator/effort.json. Each result's golden and band, and the value each pass files, computed end to end.

The passes are this generator's own implementations of named methods, run on the same record the pack ships (figures.py
runs them; this file only lays them out). None reads the prompt. effort.py grades them and prices the rubric.
"""
# id, name, block, depends, independent input, the figures.json key, its kind
CHAIN = [
    ("R1", "each group's alpha a year since 2017", "Ask 2", [], "the daily record and the market series", "R1_alpha", "table"),
    ("R2", "alpha per dollar given up per doubling", "Component 3", [], "the daily record and the capital history", "R3_fall", "number"),
    ("R3", "the expected 2027 net P&L at the draft", "Component 1", ["R1", "R2"], "", "R4_net", "number"),
    ("R4", "its 80 per cent range", "Ask 1 (range)", ["R3"], "", "R5_range", "table"),
    ("R5", "the increases below the hurdle", "Component 2", ["R1", "R2"], "", "R6_fail", "set"),
    ("R6", "the recommendation: plan and increases dropped", "Recommendation", ["R3", "R5"], "", "REC", "rec"),
]
KEY = {c[0]: c[5] for c in CHAIN}
KIND = {c[0]: c[6] for c in CHAIN}
BANDS = {"R1_alpha": "R1_bands", "R5_range": "R5_bands"}


def in_band(v, b):
    return v is not None and b[0] <= v <= b[1]


def set_grade(flag, F):
    """Right when every failing increase is flagged and no clear pass is: a borderline increase either way."""
    core, either = set(F["R6_fail"]), set(F["R6_either"])
    if flag is None:
        return "missed", "no list filed"
    f = set(flag)
    if core <= f <= core | either:
        return "right", "flags all %d failing increases and no clear pass" % len(core)
    hit = len((f - either) & core) / float(len((f - either) | core) or 1)
    return ("partly" if hit >= 0.5 else "missed"), "%d of the %d failing increases flagged, %d clear passes flagged" % (
        len(f & core), len(core), len(f - core - either))


def grade(rid, v, F):
    key, kind = KEY[rid], KIND[rid]
    if kind == "table":
        gold, bands = F[key], F[BANDS[key]]
        s = sum(1 for k in gold if in_band((v or {}).get(k), bands[k])) / float(len(gold))
        return "right" if s >= 0.999 else ("partly" if s >= 0.5 else "missed")
    if kind == "number":
        b, p = F[key.split("_")[0] + "_band"], F[key.split("_")[0] + "_partly"]
        return "right" if in_band(v, b) else ("partly" if in_band(v, p) else "missed")
    if kind == "set":
        return set_grade(v, F)[0]
    if v is None:
        return "missed"
    a = in_band(v["plan"], F["R4_band"])
    b = set_grade(v["drop"], F)[0]
    return "right" if a and b == "right" else ("partly" if a or b == "right" else "missed")


def wrap(rid, v, F):
    """A pass's entry: the value, with the grade written out where effort.py's own rule cannot read a borderline either way."""
    if KIND[rid] == "set":
        g, why = set_grade(v, F)
        return {"value": v, "grade": g, "why": why}
    if KIND[rid] == "rec":
        g = grade(rid, v, F)
        return {"value": v, "grade": g, "why": "plan %s the band; %s" % ("inside" if v and in_band(v["plan"], F["R4_band"]) else "outside",
                                                                         set_grade(v["drop"] if v else None, F)[1])}
    return v


def passes(F):
    rt = F["routes"]

    def from_route(r, alpha):
        return {"R1": alpha, "R2": F["R3_fall"], "R3": r["mean"], "R4": {"P10": r["p10"], "P90": r["p90"]}, "R5": r["fail"],
                "R6": {"plan": r["mean"], "drop": r["fail"]}}
    quick = {"R1": F["R1_raw"], "R2": F["R3_rivals"]["pooled"], "R3": F["quick"]["mean"], "R4": None, "R5": F["quick"]["fail"],
             "R6": {"plan": F["quick"]["mean"], "drop": F["quick"]["fail"]}}
    careful = from_route(rt["careful but hurried"], F["R1_risk_model"])
    gold = {"R1": F["R1_alpha"], "R2": F["R3_fall"], "R3": F["R4_net"], "R4": F["R5_range"], "R5": F["R6_fail"],
            "R6": {"plan": F["R4_net"], "drop": F["R6_fail"]}}
    hints = [
        ("A passive holding earns its carry as well as its price moves: the Baa spread, the interest differential, the term spread",
         from_route(rt["careful but hurried, carry netted"], F["R1_alpha"])),
        ("A year's markets are not a year of independent days when spreads trend for weeks",
         from_route(rt["careful but hurried, a year's horizon"], F["R1_risk_model"])),
        ("An increase is judged on what the added dollar earns, not on the pod's return at its new size",
         from_route(rt["careful but hurried, the added dollar"], F["R1_risk_model"])),
        ("A pod's record over a few years is part luck, and the draft raised the pods with the luckiest records", careful),
        ("Capital has followed records, so capacity shows only within pods", careful),
    ]
    compounds = [("carry netted, a year's horizon and the added dollar", gold),
                 ("carry netted and the added dollar", from_route(rt["daily resampling"], F["R1_alpha"])),
                 ("carry netted and a year's horizon", from_route(rt["average return at the new size"], F["R1_alpha"]))]
    return quick, careful, gold, hints, compounds


def build(F):
    quick, careful, gold, hints, compounds = passes(F)
    F["REC"] = {"plan": F["R4_net"], "drop": F["R6_fail"]}
    results = []
    for rid, name, graded_as, depends, independent, key, kind in CHAIN:
        e = {"id": rid, "name": name, "graded_as": graded_as, "figure": key, "depends": depends, "independent": independent,
             "golden": F[key]}
        if kind == "table":
            e["bands"] = F[BANDS[key]]
        elif kind == "number":
            e["band"], e["partly"] = F[key.split("_")[0] + "_band"], F[key.split("_")[0] + "_partly"]
        e["passes"] = {"quick": wrap(rid, quick[rid], F), "careful": wrap(rid, careful[rid], F), "thorough": wrap(rid, gold[rid], F)}
        results.append(e)
    ids = [c[0] for c in CHAIN]

    def rescued(new):
        return [r for r in ids if grade(r, careful[r], F) != "right" and grade(r, new[r], F) == "right"]
    rt = F["routes"]
    routes = [{"name": "the golden", "answer": {"plan": F["R4_net"], "drop": F["R6_fail"]}, "golden": True},
              {"name": "priced the way past plans were", "answer": {"plan": F["quick"]["mean"], "drop": F["quick"]["fail"]}}]
    for k in ("careful but hurried", "risk model's factors", "each pod's own record", "capacity across pods", "no drawdown rules",
              "average return at the new size", "daily resampling"):
        routes.append({"name": k, "answer": {"plan": rt[k]["mean"], "drop": rt[k]["fail"]}})
    return {"results": results,
            "hints": [{"sentence": s, "rescues": rescued(p)} for s, p in hints],
            "compounds": [{"moves": s, "rescues": rescued(p)} for s, p in compounds],
            "routes": routes}
