"""task9: generator/effort.json. Each result's golden and band, and the value each pass files, computed end to end by
analysis.py's routes on the cut pack (figures.py runs them; this file lays them out). None reads the prompt. effort.py
grades them and prices the rubric.

  quick      the excursion ticket's view: the classifier's EDGE_RING wafers as the loss, tool commonality for the
             cause, burn-in above the lots with no ring label as final test's loss, one hinge for the fleet, the
             count on the sort loss alone, the summer's own loss rate as Rev F's
  careful    what a frontier run does unprompted, stopping where the result needs a move beyond it: every file
             cleaned, retests and aliases resolved, each part's counter rebuilt from the maintenance log, the band's
             excess fitted on a hinge in each pair's own disk use with the pad and every rival beside it, final test
             tied to the ring, the textbook replacement interval on the fitted curve; it fits each pair over every
             disk it ran, takes final test's burn-in failures in proportion to the ring's die at sort, sets the count
             on that curve and that proportion, and prices Rev F on the same curve
  thorough   the golden
"""
import importlib.util
import json
import os

# id, name, block, depends, independent input, figures key
CHAIN = [
    ("R1", "the ring's loss at sort on wafers sorted 1 April to 31 August: points of mean sort yield and good die by product",
     "Component 1", [], "the sort record's zone counts and the band's fallout on young disks", "R1_loss"),
    ("R2", "each candidate cause's share of that loss", "Component 2", [], "", "R2_shares"),
    ("R3", "the units final test lost to the ring on lots it finished 1 April to 31 August, by product", "Ask 1", [],
     "the final-test lot summary and each lot's wafers at sort", "R3_ft_units"),
    ("R4", "each unit's onset and climb on the disks it will be fitted with from September", "Component 3", [],
     "the stores receipts' serial ranges and the PM log's fitted serials", "R4_dose"),
    ("R5", "each unit's count for the disk under Rev G, the ring costed at sort and at final test", "Recommendation", ["R3", "R4"],
     "", "REC_counts"),
    ("R6", "the yearly saving of those counts against Rev F as it stands", "Ask 2", ["R4", "R5"], "", "R5_saving"),
]
PRECEDENT = {
    "R3": ["L15"],     # burn-in taken in proportion to the ring's die at sort: the response's shape assumed, never measured
    "R4": ["L12"],     # every disk lot pooled though the lots wear at their own rates: the current disks read off the old ones
    "R5": ["L11"],     # final test's loss estimated and then carried into the count on the sort curve's own shape
    "R6": ["N02"],     # Rev F priced on the disks it ran before, though the disks it will run from September are another lot
}
PARTLY = {"R5_saving": 0.10}
HINTS = [
    ("The disks fitted since May come from a supplier lot that wears faster than the ones before it", ["R4", "R6"]),
    ("Burn-in failures start well before the ring shows at sort, and level off", ["R3"]),
    ("Final test's extra failures come from the outer band's good die on each lot's own wafers", ["R3"]),
    ("A part off the full PM pays its own change each time, so the count has to price both stages of loss", ["R5"]),
    ("Rev F as it stands runs the disks in stores, not the ones it ran", ["R6"]),
]


def _grade_mod():
    here = os.path.dirname(os.path.abspath(__file__))
    spec = importlib.util.spec_from_file_location("effort", os.path.join(here, "..", "..", ".claude", "skills", "stumping", "effort.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def build(F):
    S, B, Pz = F["stated"], F["bands"], F["passes"]
    results = []
    for rid, name, graded_as, depends, independent, key in CHAIN:
        e = {"id": rid, "name": name, "graded_as": graded_as, "figure": key, "depends": depends, "independent": independent}
        if isinstance(S[key], dict):
            e["golden"] = S[key]
            e["bands"] = B[key]
        else:
            e["golden"] = S[key]
            lo, hi = B[key]
            wdt = PARTLY.get(key, 0.1) * abs(S[key])
            e["band"] = [lo, hi]
            e["partly"] = [round(lo - wdt, 3), round(hi + wdt, 3)]
        if rid in PRECEDENT:
            e["precedent"] = PRECEDENT[rid]
        e["passes"] = {p: Pz[p][key] for p in ("quick", "careful", "thorough")}
        results.append(e)
    mod = _grade_mod()
    careful_grade = {r["id"]: mod.grade(r["passes"]["careful"], r)[0] for r in results}
    hints = [{"sentence": s, "rescues": [x for x in rescues if careful_grade[x] != "right"]} for s, rescues in HINTS]
    R = F["routes"]
    A = F["A"]

    def answer(loss, ft, counts):
        return {"loss": None if loss is None else round(loss, 2), "final test": None if ft is None else int(round(sum(ft.values()), -3)),
                "counts": {p: int(round(counts[us[0]], -1)) for p, us in sorted(A.pairs.items())}}
    g = F["gold"]
    routes = [{"name": "the golden", "answer": answer(g["R1_points"], g["R3_units"], g["REC"]), "golden": True},
              {"name": "the ticket's view: the classifier's wafers, the lots with no ring label as final test's base, one fleet fit",
               "answer": answer(R["R1_labels"], R["R3_clean_lot_base"], R["REC_fleet_sort_only"])},
              {"name": "careful but hurried: every disk lot pooled, burn-in in proportion to the ring's die",
               "answer": answer(R["R1_pooled"], R["R3_proportional"], R["REC_pooled_proportional"])},
              {"name": "the current lot found, burn-in in proportion to the ring's die",
               "answer": answer(g["R1_points"], R["R3_proportional"], R["REC_proportional"])},
              {"name": "final test's rise measured, every disk lot pooled", "answer": answer(R["R1_pooled"], g["R3_units"], R["REC_pooled"])},
              {"name": "the current lot found, final test left out of the count", "answer": answer(g["R1_points"], g["R3_units"], R["REC_sort_only"])},
              {"name": "the summer's wafers as the current state", "answer": answer(g["R1_points"], g["R3_units"], R["REC_summer"])},
              {"name": "the earlier lots' curve", "answer": answer(g["R1_points"], g["R3_units"], R["REC_old_lots"])},
              {"name": "a dose straight from zero", "answer": answer(g["R1_points"], g["R3_units"], R["REC_linear"])},
              {"name": "the first quarter's burn-in as final test's base, the fab's yield before and after April",
               "answer": answer(R["R1_before_after"], R["R3_q1_base"], R["REC_pooled_sort_only"])}]

    def band_label(v, lo, hi):
        return "inside" if lo <= v <= hi else ("below" if v < lo else "above")

    def call(counts):
        out = {}
        for pair, us in sorted(A.pairs.items()):
            lo, hi = B["REC_counts"][us[0]]
            vals = [counts[x] for x in us]
            out["%s %s" % (pair, "/".join(us))] = "none" if any(v is None or v != v for v in vals) else \
                "+".join(sorted({band_label(v, lo, hi) for v in vals}))
        return out
    gold_call = call(g["REC"])
    fam = [{"name": "the golden (each downforce pair's fit on the current lot, final test's rise on the disk's wear)", "answer": gold_call}]
    fam += [{"name": k, "answer": call(v)} for k, v in F["rivals"]["REC"].items()]
    pert = [{"input": k, "answer": call(v)} for k, v in F["perturbations"].items()]
    sc = [{"name": k, "answer": call(R[k2])} for k, k2 in (
        ("every disk lot pooled", "REC_pooled"), ("final test in proportion to the ring's die", "REC_proportional"),
        ("final test left out", "REC_sort_only"), ("every lot pooled and final test in proportion", "REC_pooled_proportional"),
        ("the earlier lots' curve", "REC_old_lots"), ("one fit for the fleet, sort only", "REC_fleet_sort_only"),
        ("a dose straight from zero", "REC_linear"))]
    forcing = {"kind": "set", "golden_answer": gold_call,
               "what": "each downforce pair's count for the disk on its own count, read against the pair's band (the golden's "
                       "count less and more 8 per cent): every sound method inside it, every shortcut outside",
               "bands": {u: B["REC_counts"][u] for u in B["REC_counts"]},
               "golden_family": fam, "shortcuts": sc, "perturbations": pert}
    return {"results": results, "hints": hints, "routes": routes, "forcing": forcing}


if __name__ == "__main__":
    import sys
    import figures as FG
    F = FG.compute(sys.argv[1])
    E = build(F)
    json.dump(FG.jsonable(E), open(sys.argv[2], "w"), indent=1, sort_keys=True)
