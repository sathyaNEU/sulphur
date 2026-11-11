"""task9: generator/effort.json. Each result's golden and band, and the value each pass files, computed end to end by
analysis.py's routes on the cut pack (figures.py runs them; this file lays them out). None reads the prompt. effort.py
grades them and prices the rubric.

  quick      the quarter's close-out: each family's last-quarter rate per drive in service carried for four quarters,
             the spare order at a quarter of it, the hot vaults' last-quarter rate held for two years
  careful    what a frontier run does unprompted, stopping where the result needs a move beyond it: every file cleaned,
             DC-3's ages rebuilt from the handover, the serials and power-on hours, a censored age curve per family,
             the elevated HX-8 drives modelled with a ramp, the counts' bands from the fitted values; it stops at the
             firmware release as the batch, one curve per family over every vault, and Poisson counts
  thorough   the golden
"""
import importlib.util
import os

import params as P

# id, name, block, depends, independent input, the figures key, its kind
CHAIN = [
    ("R1", "DC-3's replacements over the four quarters", "Component 1", [], "", "dc3", "number"),
    ("R2", "the bad-build batch: its drives in service and their July to September 2026 rate", "Ask 1", [], "",
     "hot_batch", "table"),
    ("R3", "the batch's replacements over the four quarters", "Component 2", ["R2"], "", "hot_count", "number"),
    ("R4", "the surviving OM-6 vaults' replacements over the four quarters", "Ask 2", [], "", "om6", "number"),
    ("R5", "the fleet's replacements in each quarter and the width of the four quarters' 80 per cent interval", "Component 3",
     ["R1", "R3", "R4"], "", "path_range", "table"),
    ("R6", "how often intervals built the same way covered the year to 30 September 2026", "Component 4", [],
     "the record to 30 September 2025 and the four quarters after it", "coverage", "number"),
    ("R7", "the fourth-quarter spare order per family", "Ask 3", ["R5"], "", "spares", "table"),
    ("R8", "the vaults to migrate and the doubling time at which migration stops paying", "Recommendation", ["R2", "R3"], "",
     "rec", "table"),
]
PARTLY = {"dc3": 0.12, "hot_count": 0.15, "om6": 0.10, "coverage": 0.10}
PRECEDENT = {
    "R2": ["L26"],                 # the firmware release, a shallower story that passes its own segment checks
    "R4": ["L14", "L13"],          # survivors of a selection priced on the whole family's curve
    "R6": ["L33", "L11"],          # drive-level draws never checked against vault-to-vault variation
    "R7": ["L14"],                 # the survivors' spares at the family's pooled rate
    "R8": ["L17", "L09"],          # every batch vault migrated on the batch's average share
}
CAREFUL = "careful but hurried"
HINTS = [
    ("The vaults retired at the reviews were the ones failing fastest", "careful, each vault at its own level"),
    ("Only the drives built in 2024 weeks 16 to 30 carry the rising hazard, whatever their firmware",
     "careful, the batch by build week"),
    ("A vault pays for its migration only when its own replacements over 24 months exceed 240",
     "careful, each vault decided on its own replacements"),
]


def _grade_mod():
    spec = importlib.util.spec_from_file_location("effort", os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..",
                                                                         ".claude", "skills", "stumping", "effort.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _in(v, b):
    return v is not None and b[0] <= v <= b[1]


def entry(rid, route, F):
    """A pass's value for one result, as effort.py reads it."""
    key = next(c[5] for c in CHAIN if c[0] == rid)
    if route is None:
        return None
    if key == "rec":
        rec = route.get("rec") or {}
        return {"migrate": sorted(rec.get("migrate") or []), "flip": None if rec.get("flip") is None else round(rec["flip"], 1)}
    if key == "path_range":
        p, b = route.get("path"), route.get("total_band")
        if p is None:
            return None
        out = {q: round(x) for q, x in p.items()}
        if b is not None:
            out["width"] = round(b[1]) - round(b[0])
        return out
    v = route.get(key)
    if v is None:
        return None
    if key == "hot_batch":
        return {"drives": int(v["drives"]), "rate": round(v["rate"], 4)}
    if key == "spares":
        return {f: int(x) for f, x in v.items()}
    if key == "coverage":
        return round(v, 3)
    return round(v)


def build(F):
    S = F["stated"]
    R = F["routes"]
    passes = {"quick": F["quick"], "careful": R[CAREFUL], "thorough": dict(F["gold"], **{k: S[k] for k in S})}
    results = []
    for rid, name, graded_as, depends, independent, key, kind in CHAIN:
        e = {"id": rid, "name": name, "graded_as": graded_as, "figure": key, "depends": depends, "independent": independent}
        e["golden"] = S[key]
        if key == "path_range":
            e["bands"] = dict(F["bands"]["path"], width=F["bands"]["total_width"])
        elif key == "hot_batch":
            e["bands"] = F["bands"]["hot_batch"]
        elif key == "spares":
            e["bands"] = dict(F["bands"]["spares"])
        elif key == "rec":
            e["bands"] = {"flip": F["bands"]["rec_flip"]}
        else:
            lo, hi = F["bands"][key]
            w = PARTLY[key] * abs(S[key])
            e["band"], e["partly"] = [round(lo, 3), round(hi, 3)], [round(lo - w, 3), round(hi + w, 3)]
        if rid in PRECEDENT:
            e["precedent"] = PRECEDENT[rid]
        e["passes"] = {p: entry(rid, v, F) for p, v in passes.items()}
        results.append(e)
    mod = _grade_mod()

    def grade_of(rid, route):
        res = next(r for r in results if r["id"] == rid)
        return mod.grade(entry(rid, route, F), res)[0]

    careful = R[CAREFUL]

    def rescued(route):
        return [c[0] for c in CHAIN if grade_of(c[0], careful) != "right" and grade_of(c[0], route) == "right"]
    hints = [{"sentence": s, "rescues": rescued(R[name])} for s, name in HINTS]

    def answer(v):
        rec = v.get("rec") or {}
        return {"total": None if v.get("total") is None else int(round(v["total"], -1)), "migrate": sorted(rec.get("migrate") or []),
                "flip": None if rec.get("flip") is None else round(rec["flip"])}
    routes = [{"name": "the golden", "answer": answer(dict(F["gold"], rec=S["rec"])), "golden": True},
              {"name": "the quarter's close-out carried", "answer": answer(F["quick"])}]
    for k, v in R.items():
        if k.startswith("careful,"):
            continue
        routes.append({"name": k, "answer": answer(v)})
    fam = [{"name": "the golden (the ramp's shapes averaged)", "answer": sorted(S["rec"]["migrate"])}]
    fam += [{"name": k, "answer": sorted(v["rec"]["migrate"])} for k, v in F["rivals"].items()]
    pert = [{"input": k, "answer": sorted(v["rec"]["migrate"])} for k, v in F["perturbations"].items()]
    sc = [{"name": k, "answer": sorted(R[k]["rec"]["migrate"])} for k in
          ("the firmware release as the batch", "every batch vault on the batch's share", "the hot batch inside its family",
           "the build window a week wider at each end", CAREFUL)]
    sc.append({"name": "the quarter's close-out carried", "answer": sorted(F["quick"]["rec"]["migrate"])})
    forcing = {"kind": "set", "golden_answer": sorted(S["rec"]["migrate"]),
               "what": "the vaults whose own replacements over the 24 months from 1 October 2026 exceed the break-even "
                       "share of their 1,200 drives (migration cost over the handling cost, 240 replacements)",
               "line": F["gold"]["vaults"] and P.COSTS["migrate_vault"] / P.COSTS["failure_handling"],
               "vault_means": {v: round(s["mean"]) for v, s in F["gold"]["vaults"].items()},
               "golden_family": fam, "shortcuts": sc, "perturbations": pert}
    return {"results": results, "hints": hints, "routes": routes, "forcing": forcing}
