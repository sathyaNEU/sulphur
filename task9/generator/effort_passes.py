"""task9: generator/effort.json. Each result's golden and band, and the value each pass files, computed end to end by
analysis.py's routes on the cut pack (figures.py runs them; this file lays them out). None reads the prompt. effort.py
grades them and prices the rubric.

  quick      the excursion ticket's view: the classifier's EDGE_RING wafers as the loss, tool commonality for the
             cause, the polish record's own pad counter as the dose and the pad as the part, the whole rise on Rev F
  careful    what a frontier run does unprompted, stopping where the result needs a move beyond it: every file
             cleaned, retests and aliases resolved, each part's counter rebuilt from the maintenance log, the band's
             excess fitted on a hinge in each unit's own disk use with the pad and every rival beside it, the textbook
             replacement interval per unit; it stops at the band's level before April as the baseline, the joint fit's
             retaining-ring share read wafer by wafer, the loss sliced at 2,000 and 2,800 wafers of disk use, and the
             summer's own loss rate as Rev F's
  thorough   the golden
"""
import importlib.util
import json
import os

# id, name, block, depends, independent input, figures key
CHAIN = [
    ("R1", "the ring's loss on wafers sorted 1 April to 31 August, points of mean sort yield", "Component 1", ["R4"],
     "the sort record's zone counts and the band's fallout at a fresh disk", "R1_points"),
    ("R2", "the same loss in good die for each product", "Ask 1", ["R1"], "", "R2_die"),
    ("R3", "each candidate cause's share of the loss", "Ask 2", [], "", "R3_shares"),
    ("R4", "each unit's onset and the slope after it", "Component 2", [], "", "R4_dose"),
    ("R5", "the shares from the 2,000-wafer rule's own exposure, Rev F's extension and the EW-118 retained disks",
     "Component 3", ["R4"], "", "R5_bridge"),
    ("R6", "each unit's count for the disk under Rev G", "Recommendation", ["R4"], "", "R6_counts"),
    ("R7", "the yearly saving against Rev F as it stands", "Ask 3", ["R4", "R6"], "", "R7_saving"),
]
PRECEDENT = {
    "R1": ["L27"],     # the band's level before April taken as the baseline: the dramatic before-and-after over like for like
    "R2": ["L27"],     # the same baseline, product by product
    "R3": ["L19"],     # the joint fit's standard errors with the wafers as independent though the disk lives are the units
    "R5": ["L26"],     # the loss sliced by the disk's usage, a shallower account that passes its own sum check
    "R7": ["N02"],     # the summer's loss rate assumed to run on, though the waiver that drove it has ended
}
PARTLY = {"R1_points": 0.05, "R7_saving": 0.10}
HINTS = [
    ("The edge ring was already costing yield before April, on the high-downforce pair under the 2,000-wafer rule", ["R1", "R2"]),
    ("Each disk wears at its own rate, so read the retaining ring off its six ring-only swaps", ["R3"]),
    ("What the old rule would have cost needs that rule run on each unit's own wafers", ["R5"]),
    ("The summer's loss rate carries the waiver's retained disks, and the waiver has ended", ["R7"]),
    ("The two downforce pairs wear their disks at different rates", ["R4", "R6"]),
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
        if key == "R4_dose":
            e["golden"] = Pz["thorough"]["R4_dose"]
            e["bands"] = B["R4_dose"]
        elif isinstance(S[key], dict):
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

    def answer(loss, counts):
        return {"loss": None if loss is None else round(loss, 2),
                "counts": {u: (None if v is None or v != v else int(round(v, -1))) for u, v in counts.items()}}
    routes = [{"name": "the golden", "answer": answer(S["R1_points"], S["R6_counts"]), "golden": True},
              {"name": "the ticket's view: the classifier's wafers and the pad", "answer": answer(R["R1_labels"], R["R6_pad_lever"])},
              {"name": "careful but hurried: the band before April as the baseline, each unit's own fit",
               "answer": answer(R["R1_q1_baseline"], R["R6_unit"])},
              {"name": "one fit for the fleet", "answer": answer(S["R1_points"], R["R6_fleet"])},
              {"name": "a dose straight from zero", "answer": answer(S["R1_points"], R["R6_linear"])},
              {"name": "the full PM moved to its own best interval", "answer": answer(S["R1_points"], R["R6_full_pm_lever"])},
              {"name": "no fallout taken out of the band", "answer": answer(R["R1_no_rolloff"], S["R6_counts"])},
              {"name": "the yield team's die-map sample read as the fab", "answer": answer(R["R1_diemap_sample"], S["R6_counts"])},
              {"name": "the fab's yield before and after April", "answer": answer(R["R1_before_after"], S["R6_counts"])}]

    def band_label(v, lo, hi):
        return "inside" if lo <= v <= hi else ("below" if v < lo else "above")

    def call(counts):
        out = {}
        for pair, us in sorted(A.pairs.items()):
            u = us[0]
            lo, hi = B["R6_counts"][u]
            vals = [counts[x] for x in us]
            out["%s %s" % (pair, "/".join(us))] = "none" if any(v is None or v != v for v in vals) else \
                "+".join(sorted({band_label(v, lo, hi) for v in vals}))
        return out
    gold_call = call(S["R6_counts"])
    fam = [{"name": "the golden (each downforce pair's fit)", "answer": gold_call}]
    fam += [{"name": k, "answer": call(v)} for k, v in F["rivals"]["R6"].items()]
    pert = [{"input": k, "answer": call(v)} for k, v in F["perturbations"].items()]
    sc = [{"name": k, "answer": call(R[k2])} for k, k2 in (("one fit for the fleet", "R6_fleet"), ("a dose straight from zero", "R6_linear"),
                                                          ("the full PM moved to its own best interval", "R6_full_pm_lever"),
                                                          ("the pad as the part", "R6_pad_lever"))]
    forcing = {"kind": "set", "golden_answer": gold_call,
               "what": "each downforce pair's count for the disk on its own count, read against the pair's band (the golden's "
                       "count less and more 8 per cent): every sound method inside it, every shortcut outside",
               "bands": {u: B["R6_counts"][u] for u in B["R6_counts"]},
               "golden_family": fam, "shortcuts": sc, "perturbations": pert}
    return {"results": results, "hints": hints, "routes": routes, "forcing": forcing}


if __name__ == "__main__":
    import sys
    import figures as FG
    F = FG.compute(sys.argv[1])
    E = build(F)
    json.dump(FG.jsonable(E), open(sys.argv[2], "w"), indent=1, sort_keys=True)
    json.dump(FG.jsonable(dict(F["stated"], **{"bands": F["bands"]})), open(sys.argv[3], "w"), indent=1, sort_keys=True)
