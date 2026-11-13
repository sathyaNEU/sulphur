"""figures.json (every figure the answer blocks and the goldens state) and effort.json (the effort test, the factorial
and the forcing, run on the cut pack by the generator's own methods)."""
import json
import os
import numpy as np
import analysis as A

H27, H28 = A.HALVES[:2], A.HALVES[2:]

def bands(R):
    """each graded figure's band: the golden family's spread with a margin, never so wide that it takes in a shortcut."""
    g = R["golden"]; fam = [o for n, o in R["family"]]
    def span(get, pad, lo_floor=None):
        vals = [get(g)] + [get(o) for o in fam]
        return [round(min(vals) - pad, 1), round(max(vals) + pad, 1)]
    out = {"R1": {s: [round(v - 0.5, 1), round(v + 0.5, 1)] for s, v in g["R1"].items()},
           "R4": {h: [round(v - 0.5, 1), round(v + 0.5, 1)] for h, v in g["R4"].items()},
           "R2": {h: span(lambda o, h=h: o["R2"][h], 6.0) for h in H27},
           "R3": {h: span(lambda o, h=h: o["R3"][h], 6.0) for h in H28},
           "R5": span(lambda o: o["R5"], 8.0)}
    return out

def inband(b, v):
    if isinstance(b, dict):
        return all(b[k][0] - 1e-9 <= v[k] <= b[k][1] + 1e-9 for k in b)
    return b[0] - 1e-9 <= v <= b[1] + 1e-9

def rescued(R, B, o, ids=("R2", "R3", "R5", "R7")):
    """the results a route files inside their bands that the careful pass does not."""
    c = R["passes"]["careful"]
    ok = lambda x, r: (x["R7"] == R["golden"]["R7"]) if r == "R7" else inband(B[r], x[r])
    return [("R6" if r == "R7" else r) for r in ids if ok(o, r) and not ok(c, r)]

def write(R, root):
    g = R["golden"]; fit = R["fit"]; B = bands(R)
    progs = {p["code"]: p for p in g["programs"]}
    F = {"program": g["R7"], "program_total_usd_m": progs[g["R7"]]["total"] if g["R7"] in progs else 0.0,
         "headroom_before_2027_usd_m": g["R5"], "reserve_usd_m": R["reserve"], "spending_24m_usd_m": R["spending24"],
         "minimum_reserve_usd_m": R["cushion"], "net_needs_before_2027_usd_m": round(R["spending24"] + g["need0"], 1),
         "calls_2027_by_half_usd_m": g["R2"], "calls_2028_by_half_usd_m": g["R3"], "distributions_by_half_usd_m": g["R4"],
         "calls_closed_by_half_usd_m": g["closed"], "calls_pending_by_half_usd_m": g["pending"],
         "unfunded_by_strategy_usd_m": g["R1"], "unfunded_total_usd_m": round(sum(g["R1"].values()), 1),
         "programs": {p["code"]: {"total_usd_m": p["total"], "calls_usd_m": p["calls"], "headroom_usd_m": p["headroom"], "passes": p["passes"]} for p in g["programs"]},
         "re_up_calls_usd_m": g["by_fund"], "line_stock_usd_m": R["line_stock_total"], "line_stock_six_managers_usd_m": R["line_stock_uncovered"], "line_stock_six_managers_audited_usd_m": R["line_stock_uncovered_audited"],
         "six_managers": R["uncovered"], "support_by_half_usd_m": g["support"], "support_total_usd_m": round(sum(g["support"].values()), 1),
         "support": {k: (round(v, 4) if isinstance(v, float) else v) for k, v in fit["support"].items()},
         "slip": {k: round(v, 4) for k, v in fit["slip"].items()}, "extension_rule": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in fit["ext"].items()},
         "deal_market_elasticity": round(fit["eta"], 3) if not isinstance(fit["eta"], dict) else {k: round(v, 3) for k, v in fit["eta"].items()},
         "pending_funds": R["pending"], "bands": B,
         "careful_route_programs": {p["code"]: {"calls_usd_m": p["calls"], "headroom_usd_m": p["headroom"], "passes": p["passes"]} for p in R["passes"]["careful"]["programs"]},
         "reflex_drops": {k: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]} for k, o in R["reflex_drops"].items()},
         "own_record_max_shortfall": R["own_record_max_shortfall"], "stress_max_shortfall": R["stress_max_shortfall"],
         "six_managers_live_funds": R["six_live_funds"], "past_first_closes": R["past_first_closes"],
         "routes": {n: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]} for n, o in R["routes"]},
         "family": {n: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]} for n, o in R["family"]},
         "factorial": {k: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]} for k, o in R["factorial"].items()},
         "bootstrap_p5_p95": {k: [round(float(np.percentile(v, 5)), 1), round(float(np.percentile(v, 95)), 1)] for k, v in R["boot"].items()},
         "years": [2008, 2009, 2010, 2022, 2023, 2024, 2025, 2026, 2027, 2028], "exact_tolerance_usd_m": 0.5}
    json.dump(F, open(os.path.join(root, "figures.json"), "w"), indent=1, sort_keys=True)
    P = R["passes"]
    spec = [("R1", "commitments not yet called at 31 December 2026, by strategy", "Ask 1", "unfunded_by_strategy_usd_m", [], None, "R1"),
            ("R2", "capital calls in the policy's stress on the commitments made by the end of 2026, each half of 2027", "Component 2", "calls_2027_by_half_usd_m", [], ["N13", "L44", "L43"], "R2"),
            ("R3", "capital calls in the policy's stress on the commitments made by the end of 2026, each half of 2028", "Component 3", "calls_2028_by_half_usd_m", [], ["L42", "N34"], "R3"),
            ("R4", "distributions in the policy's stress, each half of 2027 and 2028", "Ask 2", "distributions_by_half_usd_m", [], None, "R4"),
            ("R5", "the headroom above the minimum reserve before any 2027 commitment", "Ask 3", "headroom_before_2027_usd_m", ["R2", "R3", "R4"], ["L42", "N13", "N34"], "R5"),
            ("R6", "the program the policy lets the Investment Committee adopt", "Recommendation", "program", ["R2", "R3", "R4"], ["L42", "N13", "N34"], "R7")]
    res = []
    for rid, name, ga, fig, dep, prec, key in spec:
        r = {"id": rid, "name": name, "graded_as": ga, "figure": fig, "depends": dep, "independent": "", "golden": g[key]}
        if rid == "R6":
            pass
        elif isinstance(B[rid], dict):
            r["bands"] = B[rid]; r["partly_share"] = 0.75
        else:
            r["band"] = B[rid]
        if prec: r["precedent"] = prec
        r["passes"] = {p: P[p][key] for p in ("quick", "careful", "thorough")}
        res.append(r)
    fac = R["factorial"]
    E = {"results": res,
         "hints": [{"sentence": "past a shortfall the endowment's own record never reached, rescue financings keep the managers' calls on held companies rising; the benchmark's funds past their investment period show it in 2009",
                    "rescues": rescued(R, B, fac["J1 alone"])},
                   {"sentence": "six managers' company-level files stop after 2024, and their funds' lines were rebuilt through 2026 as rates fell",
                    "rescues": rescued(R, B, fac["J2 alone"])}],
         "factorial": {"golden_answer": g["R7"], "reflex_route": {"answer": P["careful"]["R7"]}, "judgments": [
             {"id": "J1", "name": "the support curve past the plateau the record shows: rescue financings beyond a shortfall it never reached, read off the benchmark's funds past their investment period",
              "kind": "stump", "precedent": ["L42", "N34"], "dropped": {"answer": fac["J1 dropped"]["R7"], "results_moved": [r for r in ("R3", "R5") if not inband(B[r], fac["J1 dropped"][r])] + ["R6"]},
              "alone": {"answer": fac["J1 alone"]["R7"], "results_rescued": rescued(R, B, fac["J1 alone"])}},
             {"id": "J2", "name": "the six managers whose company-level files stop after 2024: their line stock bridged from the file's end on the fitted pace, re-anchored at the audits",
              "kind": "stump", "precedent": ["N13", "L44"], "dropped": {"answer": fac["J2 dropped"]["R7"], "results_moved": [r for r in ("R2", "R5") if not inband(B[r], fac["J2 dropped"][r])] + ["R6"]},
              "alone": {"answer": fac["J2 alone"]["R7"], "results_rescued": rescued(R, B, fac["J2 alone"])}},
             {"id": "J3", "name": "the covered managers' capital invested on lines and not yet called, called at the clean-down", "kind": "reflex", "precedent": ["R63"]},
             {"id": "J4", "name": "defensive follow-ons on the held companies' cost, two quarters after the exit index, the plateau fitted", "kind": "reflex", "precedent": ["R64"]},
             {"id": "J5", "name": "pending funds' first closes slipped on the exit market", "kind": "reflex", "precedent": ["R65"]},
             {"id": "J6", "name": "investment periods extended where the register's rule says, new deals at the managers' pace with the deal market", "kind": "reflex", "precedent": ["R14", "R20"]},
             {"id": "J7", "name": "statements cleaned; distributions, reserve and spending as the policy sets them", "kind": "reflex", "precedent": ["R01", "R18"]},
             {"id": "J8", "name": "fees, recycling, the fits chosen by fit and back-tested, a bootstrap over funds", "kind": "reflex", "precedent": ["R14", "R36", "R66", "R04"]}]},
         "forcing": {"kind": "set", "golden_answer": g["R7"],
                     "golden_family": [{"name": "the golden", "answer": g["R7"]}] + [{"name": n, "answer": o["R7"]} for n, o in R["family"]],
                     "shortcuts": [{"name": n, "answer": o["R7"]} for n, o in R["routes"][1:]],
                     "perturbations": [{"input": "%s at the bootstrap's %s" % (k, side), "answer": program_at(R, float(np.percentile(v, pc)))}
                                       for k, v in R["boot"].items() for side, pc in (("5th percentile", 5), ("95th percentile", 95))]},
         "routes": [{"name": n, "answer": o["R7"], "golden": i == 0} for i, (n, o) in enumerate(R["routes"])],
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    json.dump(E, open(os.path.join(root, "effort.json"), "w"), indent=1)
    return F, E

def program_at(R, h0):
    """the program the policy adopts at a given headroom before any 2027 commitment, the golden's program calls."""
    passing = [p for p in R["golden"]["programs"] if h0 - p["calls"] >= 0]
    return max(passing, key=lambda p: p["total"])["code"] if passing else "none"
