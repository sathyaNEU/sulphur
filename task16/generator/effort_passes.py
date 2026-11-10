"""generator/effort.json: each result's golden and band, and the value each pass files, computed end to end.

The passes are this generator's own implementations of named methods (results.py), run on the built pack. None reads
the prompt. effort.py grades them and prices the rubric.
"""
import golden as GD
import results as RS

# the results chain of the design note: its ID, the analysis key it grades, where the answer blocks grade it, what it
# depends on, and the figures.json key the blocks state it from
CHAIN = [
    ("R1", "trial", "Ask 3", [], "trial_map384"),
    ("R2", "costs", "Component 1 (Ask 4)", ["R1"], "costs"),
    ("R3", "level", "Component 2 (Ask 5)", ["R1", "R2"], "level_512k"),
    ("R4", "expected", "Component 3 (Ask 1)", ["R2", "R3"], "expected"),
    ("R5", "range", "Ask 2", ["R1", "R4"], "range"),
    ("R6", "call", "Recommendation", ["R4"], "call"),
]
ID_OF = {key: rid for rid, key, _, _, _ in CHAIN}
HINTS = [
    ("give every total the trials ran a level of its own and read each route's cost from the mixes at one total", "every"),
    ("past the expert pool, take the level at each total as its own unknown, read off the vendor trials once each "
     "route's cost is taken out", "levels"),
    ("score every run on the expert-labelled development items and carry it to the benchmark on the scored runs", "yardstick"),
    ("read each route against expert-label runs at the same learning rate", "matched"),
    ("choose the curve on the pilot's largest runs held back", "heldback"),
]


def filed(res, key):
    """A pass's value for one result, rounded the way the answer blocks state it."""
    r = res.get(key)
    if r is None:
        return None
    if key == "trial":
        return GD.r3(r["exp128k_map384k"])
    if key == "costs":
        return {"contractor": GD.r4(r["ctr_per10"]), "map_transfer": GD.r4(r["map_per10"])}
    if key == "level":
        return GD.r3(r)
    if key == "expected":
        return {k: GD.r3(v) for k, v in r.items()}
    if key == "range":
        return {"%s_low" % r["config"]: GD.r3(r["low"]), "%s_high" % r["config"]: GD.r3(r["high"]),
                "half_width": GD.r3(RS.half_width(r))}
    return r["pick"]


def hint_pass(G, kind):
    """The careful pass with one sentence of help taken literally."""
    if kind == "levels":
        return G["hint_levels"]
    if kind == "every":
        return G["hint_every"]
    return G["careful"]          # the careful pass already scores on expert items, matches the rate and holds runs back


def rescued(G, kind):
    """The analysis keys a hint turns from not Right to Right in the careful pass."""
    base = G["careful"]; new = hint_pass(G, kind)
    return [k for k in GD.KEYS if RS.grade(base, k) != "right" and RS.grade(new, k) == "right"]


def build(G, F):
    quick = dict(G["quick"])
    results = []
    for rid, key, graded_as, depends, figure in CHAIN:
        e = {"id": rid, "name": GD.NAMES[key], "graded_as": graded_as, "figure": figure, "depends": depends,
             "independent": "", "golden": F[figure]}
        b = RS.BANDS.get(key)
        if key == "trial":
            e["band"] = list(b["exp128k_map384k"])
        elif key == "costs":
            e["bands"] = {"contractor": list(b["ctr_per10"]), "map_transfer": list(b["map_per10"])}
        elif key == "level":
            e["band"] = list(b)
        elif key == "expected":
            e["bands"] = {x: list(v) for x, v in b.items()}
        elif key == "range":
            e["bands"] = {"B_low": list(b["low"]), "B_high": list(b["high"]), "half_width": list(b["half"])}
        q = filed(quick, key)
        if key == "trial":
            q = GD.r3(G["logged_trial"])
        e["passes"] = {"quick": q, "careful": filed(G["careful"], key), "thorough": filed(G["golden"], key)}
        results.append(e)
    hints = [{"sentence": s, "rescues": [ID_OF[k] for k in rescued(G, kind)]} for s, kind in HINTS]

    def ans(res):
        p = res["call"]["pick"]
        return {"names": p, "expected": GD.r3(res["expected"][p])}
    routes = [
        {"name": "the golden", "answer": ans(G["golden"]), "golden": True},
        {"name": "the logged development loss on the ladder's straight line", "answer": ans(G["quick"])},
        {"name": "one scaling curve through every run, its form chosen on held-back runs", "answer": ans(G["careful"])},
        {"name": "the ladder's straight line carried past the expert pool", "answer": ans(G["line"])},
        {"name": "the two vendor routes read as one", "answer": ans(G["one_vendor"])},
        {"name": "only the runs the benchmark scored", "answer": ans(G["scored_only"])},
    ]
    return {"results": results, "hints": hints, "routes": routes}
