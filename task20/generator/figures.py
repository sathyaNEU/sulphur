"""figures.json (every figure the answer blocks and the goldens state) and effort.json (the effort test, the factorial
and the forcing, run on the cut pack by the generator's own methods)."""
import json
import os
import numpy as np
import analysis as A

BANDS = {
    "R1": {s: 0.5 for s in A.STRAT_ORDER},
    "R2": {"H1 2027": (505.0, 532.0), "H2 2027": (198.0, 226.0), "H1 2028": (205.0, 245.0), "H2 2028": (160.0, 188.0)},
    "R3": {"H1 2027": (0.0, 1.0), "H2 2027": (0.0, 6.0), "H1 2028": (56.0, 72.0), "H2 2028": (78.0, 92.0)},
    "R4": {h: 0.5 for h in A.HALVES},
    "R5": (1022.0, 1100.0), "R6": (-163.0, -85.0), "R7": (175, 350),
}

def band_of(rid, golden):
    b = BANDS[rid]
    if isinstance(b, dict):
        return {k: ([round(golden[k] - v, 1), round(golden[k] + v, 1)] if not isinstance(v, tuple) else list(v)) for k, v in b.items()}
    return list(b)

def inband(rid, value, golden):
    bd = band_of(rid, golden)
    if isinstance(bd, dict):
        return all(bd[k][0] - 1e-9 <= value[k] <= bd[k][1] + 1e-9 for k in bd)
    return bd[0] - 1e-9 <= value <= bd[1] + 1e-9

def cap_label(R, v):
    lo, hi = BANDS["R7"]
    return "USD %dm to %dm" % (lo, hi) if lo <= v <= hi else "USD %dm" % v

def rescued(R, o, ids=("R1", "R2", "R3", "R4", "R5", "R6", "R7")):
    """the results a route files inside their bands that the careful pass does not."""
    g = R["golden"]; c = R["passes"]["careful"]
    return [r for r in ids if inband(r, o[r], g[r]) and not inband(r, c[r], g[r])]

def write(R, root):
    g = R["golden"]; fit = R["fit"]
    F = {"capacity_usd_m": g["R7"], "capacity_unrounded_usd_m": g["B"], "capacity_band_usd_m": list(BANDS["R7"]),
         "net_cash_needs_500_usd_m": g["R5"], "headroom_500_usd_m": g["R6"], "reserve_usd_m": R["reserve"], "spending_24m_usd_m": R["spending24"],
         "minimum_reserve_usd_m": R["cushion"], "calls_closed_funds_by_half_usd_m": g["R2"], "calls_pending_funds_by_half_usd_m": g["R3"],
         "distributions_by_half_usd_m": g["R4"], "unfunded_by_strategy_usd_m": g["R1"],
         "unfunded_total_usd_m": round(sum(g["R1"].values()), 1), "plan_calls_500_by_half_usd_m": g["plan_calls"],
         "calls_per_100_of_budget_usd_m": round(100 * g["c_plan"], 1), "line_stock_usd_m": R["line_stock_total"], "line_stock_by_strategy_usd_m": R["line_stock_by"],
         "defensive_follow_ons_by_half_usd_m": g["support"], "fees_by_half_usd_m": g["fees"], "recycled_by_half_usd_m": g["recycled"],
         "support": {k: round(v, 4) for k, v in fit["support"].items()}, "slip": {k: round(v, 4) for k, v in fit["slip"].items()},
         "deal_market_elasticity": round(fit["eta"], 3), "pending_funds": R["pending"], "plan_slips": R["plan_slips"],
         "bands": {k: band_of(k, g[k]) for k in ("R1", "R2", "R3", "R4", "R5", "R6", "R7")},
         "routes": {n: {"capacity_usd_m": o["R7"], "unrounded": o["B"], "headroom_500_usd_m": o["R6"], "net_cash_needs_500_usd_m": o["R5"]} for n, o in R["routes"]},
         "family": {n: {"capacity_usd_m": o["R7"], "unrounded": o["B"], "net_cash_needs_500_usd_m": o["R5"],
                        "defensive_follow_ons_usd_m": round(sum(o["support"].values()), 1)} for n, o in R["family"]},
         "defensive_follow_ons_range_usd_m": [round(min(sum(o["support"].values()) for o in [g] + [o for n, o in R["family"]]), 1),
                                              round(max(sum(o["support"].values()) for o in [g] + [o for n, o in R["family"]]), 1)],
         "factorial": {k: {"capacity_usd_m": o["R7"], "unrounded": o["B"], "headroom_500_usd_m": o["R6"]} for k, o in R["factorial"].items()},
         "bootstrap_p5_p95": {k: [round(float(np.percentile(v, 5)), 1), round(float(np.percentile(v, 95)), 1)] for k, v in R["boot"].items()},
         "test_500": R["test_at"][500.0], "test_250": R["test_at"][250.0], "shortfall_500_usd_m": round(-R["test_at"][500.0]["headroom"], 1),
         "defensive_follow_ons_total_usd_m": round(sum(g["support"].values()), 1), "fy2027_distribution_usd_m": R["L"]["spend"][2027],
         "stress_short_rate_pct": round(float(R["L"]["R"][A.H_END]) + 2.5, 2), "follow_on_rate_per_10_points_pct": round(10 * fit["support"]["sigma"] / fit["support"]["e_star"], 2),
         "slip_per_10_points_quarters": round(fit["slip"]["b"] * 10 / fit["slip"]["ref"], 2), "pending_calls_total_usd_m": round(sum(g["R3"].values()), 1),
         "pending_calls_on_managers_dates_usd_m": round(sum(R["passes"]["careful"]["R3"].values()), 1), "exact_tolerance_usd_m": 0.5,
         "years": [2023, 2026, 2027, 2028]}
    json.dump(F, open(os.path.join(root, "figures.json"), "w"), indent=1, sort_keys=True)
    # ---------------------------------------------------------------- effort.json
    P = R["passes"]
    spec = [("R1", "commitments not yet called at 31 December 2026, by strategy", "Ask 1", "unfunded_by_strategy_usd_m", [], "", None),
            ("R2", "capital calls on the funds that have held a first close, in each half of 2027 and 2028", "Component 2", "calls_closed_funds_by_half_usd_m", [], "", ["L32", "L10", "L15"]),
            ("R3", "capital calls on the funds yet to hold a first close, in each half of 2027 and 2028", "Component 3", "calls_pending_funds_by_half_usd_m", [], "", ["N22", "N03", "N28"]),
            ("R4", "distributions in each half of 2027 and 2028 under the policy's stress", "Ask 2", "distributions_by_half_usd_m", [], "", None),
            ("R5", "the policy's net cash needs over 2027 and 2028 at a USD 500 million budget", "Ask 3", "net_cash_needs_500_usd_m", ["R2", "R3", "R4"], "", ["L32", "L10", "N22"]),
            ("R6", "the headroom above the minimum reserve at a USD 500 million budget", "Component 1", "headroom_500_usd_m", ["R5"], "", ["L32", "L10", "N22"]),
            ("R7", "the largest 2027 total that passes", "Recommendation", "capacity_usd_m", ["R2", "R3", "R4"], "", ["L32", "L10", "N22"])]
    res = []
    for rid, name, ga, fig, dep, ind, prec in spec:
        r = {"id": rid, "name": name, "graded_as": ga, "figure": fig, "depends": dep, "independent": ind, "golden": g[rid]}
        bd = band_of(rid, g[rid])
        if isinstance(bd, dict):
            r["bands"] = bd; r["partly_share"] = 0.75
        else:
            r["band"] = bd
        if prec: r["precedent"] = prec
        r["passes"] = {p: P[p][rid] for p in ("quick", "careful", "thorough")}
        res.append(r)
    fac = R["factorial"]
    lab = lambda o: o["R7"]                      # the factorial reads the budget the route files, in the policy's steps
    band = lambda o: cap_label(R, o["R7"])       # the forcing reads it against the band
    E = {"results": res,
         "hints": [{"sentence": "the managers had about USD %d million invested on their funds' credit lines at 31 December and not yet called, and the stress's rates make every manager call it in the first quarter" % round(R["line_stock_total"]),
                    "rescues": rescued(R, fac["J1 alone"])},
                   {"sentence": "in a weak exit market the managers put more into the companies they have held two years or more, from two quarters after the exit index falls below normal",
                    "rescues": rescued(R, fac["J2 alone"])},
                   {"sentence": "first closes slip when the exit index sits below normal in the quarter before, by about six quarters for every 100 per cent it falls short",
                    "rescues": rescued(R, fac["J3 alone"])}],
         "factorial": {"golden_answer": lab(g), "reflex_route": {"answer": lab(P["careful"])}, "judgments": [
             {"id": "J1", "name": "the capital invested on subscription lines and not yet called, rebuilt and told apart from recycled proceeds, called at the clean-down",
              "kind": "stump", "precedent": ["L32", "N02"], "dropped": {"answer": lab(fac["J1 dropped"]), "results_moved": [r for r in ("R2", "R5", "R6", "R7") if not inband(r, fac["J1 dropped"][r], g[r])]},
              "alone": {"answer": lab(fac["J1 alone"]), "results_rescued": rescued(R, fac["J1 alone"], ("R2", "R3", "R5", "R6", "R7"))}},
             {"id": "J2", "name": "defensive follow-ons into companies held two years or more, measured apart from new deals, on the stress path",
              "kind": "stump", "precedent": ["L10", "L15"], "dropped": {"answer": lab(fac["J2 dropped"]), "results_moved": [r for r in ("R2", "R5", "R6", "R7") if not inband(r, fac["J2 dropped"][r], g[r])]},
              "alone": {"answer": lab(fac["J2 alone"]), "results_rescued": rescued(R, fac["J2 alone"], ("R2", "R3", "R5", "R6", "R7"))}},
             {"id": "J3", "name": "first closes that slip with the exit market, measured on the register's own closes and carried on the stress path",
              "kind": "stump", "precedent": ["N22", "N03"], "dropped": {"answer": lab(fac["J3 dropped"]), "results_moved": [r for r in ("R3", "R5", "R6", "R7") if not inband(r, fac["J3 dropped"][r], g[r])]},
              "alone": {"answer": lab(fac["J3 alone"]), "results_rescued": rescued(R, fac["J3 alone"], ("R2", "R3", "R5", "R6", "R7"))}},
             {"id": "J4", "name": "statements cleaned: the superseded row, the custodian's fourth-quarter cash for late statements, commitments released at term end", "kind": "reflex", "precedent": ["R01"]},
             {"id": "J5", "name": "distributions at the policy's 2008-10 benchmark rates on each fund's 31 December value", "kind": "reflex", "precedent": ["R18"]},
             {"id": "J6", "name": "new deals from the managers' own pace on the room left, by strategy and year, with the deal market's elasticity", "kind": "reflex", "precedent": ["R14", "R20"]},
             {"id": "J7", "name": "fees on commitments while investing and on the cost held afterwards; recycling read per manager", "kind": "reflex", "precedent": ["R14"]},
             {"id": "J8", "name": "the response's window and level chosen by fit, a bootstrap over funds for the spread", "kind": "reflex", "precedent": ["R36", "R33", "R04"]}]},
         "forcing": {"kind": "set", "golden_answer": band(g),
                     "golden_family": [{"name": "the golden", "answer": band(g)}] + [{"name": n, "answer": band(o)} for n, o in R["family"]],
                     "shortcuts": [{"name": n, "answer": band(o)} for n, o in R["routes"][1:]],
                     "perturbations": [{"input": "%s at the bootstrap's %s" % (k, side), "answer": cap_label(R, int(np.floor(np.percentile(v, pc) / A.GRID + 1e-9) * A.GRID))}
                                       for k, v in R["boot"].items() if k not in ("eta", "sigma", "slip_b") for side, pc in (("5th percentile", 5), ("95th percentile", 95))]},
         "routes": [{"name": n, "answer": lab(o), "golden": i == 0} for i, (n, o) in enumerate(R["routes"])],
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    json.dump(E, open(os.path.join(root, "effort.json"), "w"), indent=1)
    return F, E
