"""task9: generator/effort.json. Each result's golden and band, and the value each pass files, computed end to end.

The passes are this generator's own implementations of named methods (passes.py), run on the same record the pack
ships. None reads the prompt. effort.py grades them and prices the rubric.
"""
import passes as PS

# the results chain of the design note: id, name, where the answer blocks grade it, what it depends on, the input that
# lets it be graded on its own
CHAIN = [
    ("R1", "the 3-month ladder's average settlement per sale", "Ask 2", [], "the index and price histories"),
    ("R2", "the 3-month ladder's worst calendar year", "Component 4 (Ask 2)", [], "the index and price histories"),
    ("R3", "the 12-month ladder's peak collateral", "Ask 4", [], "the index and price histories"),
    ("R4", "the largest 3-month size", "Component 1", ["R2", "R3"], ""),
    ("R5", "the largest 6-month size", "Ask 1", ["R3"], ""),
    ("R6", "the range of the 12-month ladder's average", "Ask 3 (12-month)", [], "the 12-month ladder's settlements, which need no rebuilt strike"),
    ("R7", "the range of the 3-month ladder's average", "Ask 3 (3-month)", ["R1"], ""),
    ("R8", "the open swaps' expected settlement", "Component 2 (Ask 5)", [], "the open swaps and the record's start dates"),
    ("R9", "the open swaps' 80 per cent range", "Ask 5 (range)", [], "the start dates' replay, graded on its own ends"),
    ("R10", "the 2027 plan by ladder with its range", "Component 3 (Ask 6)", ["R1", "R4", "R8"], ""),
    ("R11", "the recommendation", "Recommendation", ["R4", "R10"], ""),
]
BAND = {"R1": ("R1_band", "R1_partly"), "R2": ("R2_band", "R2_partly"), "R3": ("R3_band", "R3_partly"), "R4": ("R4_band", "R4_partly"),
        "R5": ("R5_band", "R5_partly"), "R8": ("R8_band", "R8_partly")}
BANDS = {"R6": "R6_bands", "R7": "R7_bands", "R9": "R9_bands", "R10": "R10_bands", "R11": "R11_bands"}


def same(a, b):
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return abs(a - b) <= 1e-9 * max(1.0, abs(a))
    return str(a).strip().lower() == str(b).strip().lower()


def cells(rid, value, F):
    """For a table result, which cells a pass has inside their bands."""
    gold, bands = F[PS.FIGURE[rid]], F[BANDS[rid]]
    out = {}
    for cell, gv in gold.items():
        pv, b = (value or {}).get(cell), bands.get(cell)
        out[cell] = bool(b[0] <= pv <= b[1]) if (b is not None and isinstance(pv, (int, float))) else bool(pv is not None and same(pv, gv))
    return out


def grade(rid, value, F):
    """right, partly or missed, by the rule effort.py applies (checks.py asserts the two agree on every cell)."""
    if value is None:
        return "missed"
    if rid in BANDS:
        c = cells(rid, value, F)
        share = sum(c.values()) / float(len(c))
        return "right" if share >= 0.999 else ("partly" if share >= 0.5 else "missed")
    band, partly = F[BAND[rid][0]], F[BAND[rid][1]]
    if band[0] <= value <= band[1]:
        return "right"
    return "partly" if partly[0] <= value <= partly[1] else "missed"


def rescued(F, base, new):
    return [rid for rid in PS.IDS if grade(rid, base[rid], F) != "right" and grade(rid, new[rid], F) == "right"]


def build(A, R, F):
    quick, careful, gold = PS.quick(A, R), PS.careful(A, R), PS.golden(F)
    results = []
    for rid, name, graded_as, depends, independent in CHAIN:
        e = {"id": rid, "name": name, "graded_as": graded_as, "figure": PS.FIGURE[rid], "depends": depends,
             "independent": independent, "golden": gold[rid]}
        if rid in BAND:
            e["band"], e["partly"] = F[BAND[rid][0]], F[BAND[rid][1]]
        else:
            e["bands"] = F[BANDS[rid]]
        e["passes"] = {"quick": quick[rid], "careful": careful[rid], "thorough": gold[rid]}
        results.append(e)
    hints = [{"sentence": s, "rescues": rescued(F, careful, p)} for s, p in PS.hint_passes(A, R)]
    compounds = [{"moves": s, "rescues": rescued(F, careful, p)} for s, p in PS.compound_passes(A, R)]
    routes = [{"name": x["route"], "answer": {"size_usd": x["size_usd"], "plan_usd": x["plan_usd"]}} for x in F["routes"]]
    routes[0]["golden"] = True
    return {"results": results, "hints": hints, "compounds": compounds, "routes": routes}
