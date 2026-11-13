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
    def span(get, pad):
        vals = [get(g)] + [get(o) for o in fam]
        return [round(min(vals) - pad, 1), round(max(vals) + pad, 1)]
    return {"R1": {s: [round(v - 0.5, 1), round(v + 0.5, 1)] for s, v in g["R1"].items()},
            "R4": {h: [round(v - 0.5, 1), round(v + 0.5, 1)] for h, v in g["R4"].items()},
            "R2": {h: span(lambda o, h=h: o["R2"][h], 6.0) for h in H27},
            "R3": {h: span(lambda o, h=h: o["R3"][h], 6.0) for h in H28},
            "R5": span(lambda o: o["R5"], 8.0)}

def inband(b, v):
    if isinstance(b, dict):
        return all(b[k][0] - 1e-9 <= v[k] <= b[k][1] + 1e-9 for k in b)
    return b[0] - 1e-9 <= v <= b[1] + 1e-9

def moved(R, B, o, ids=("R2", "R3", "R5")):
    """the graded results a route files outside their bands, the program included."""
    out = [r for r in ids if not inband(B[r], o[r])]
    return out + (["R6"] if o["R7"] != R["golden"]["R7"] else [])

def rescued(R, B, o, ids=("R2", "R3", "R5", "R7")):
    """the results a route files inside their bands that the careful pass does not."""
    c = R["passes"]["careful"]
    ok = lambda x, r: (x["R7"] == R["golden"]["R7"]) if r == "R7" else inband(B[r], x[r])
    return [("R6" if r == "R7" else r) for r in ids if ok(o, r) and not ok(c, r)]

def at_percentile(vals, progs, pc):
    """the program of the bootstrap draw nearest a percentile of the headroom."""
    v = np.array(vals); t = float(np.percentile(v, pc)); i = int(np.argmin(np.abs(v - t)))
    return progs[i]

def write(R, root):
    g = R["golden"]; fit = R["fit"]; B = bands(R); fac = R["factorial"]
    progs = {p["code"]: p for p in g["programs"]}
    adopt = g["R7"]
    fs = lambda d: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items() if k != "pts"}
    succ = R["successor_events"]
    F = {"program": adopt, "program_total_usd_m": progs[adopt]["total"] if adopt in progs else 0.0,
         "headroom_before_2027_usd_m": g["R5"], "reserve_usd_m": R["reserve"], "spending_24m_usd_m": R["spending24"],
         "minimum_reserve_usd_m": R["cushion"], "net_needs_before_2027_usd_m": round(R["spending24"] + g["need0"], 1),
         "calls_2027_by_half_usd_m": g["R2"], "calls_2028_by_half_usd_m": g["R3"], "distributions_by_half_usd_m": g["R4"],
         "calls_total_usd_m": round(sum(g["R2"].values()) + sum(g["R3"].values()), 1), "distributions_total_usd_m": round(sum(g["R4"].values()), 1),
         "calls_closed_by_half_usd_m": g["closed"], "calls_pending_by_half_usd_m": g["pending"],
         "unfunded_by_strategy_usd_m": g["R1"], "unfunded_total_usd_m": round(sum(g["R1"].values()), 1),
         "programs": {p["code"]: {"total_usd_m": p["total"], "calls_usd_m": p["calls"], "headroom_usd_m": p["headroom"], "passes": p["passes"]} for p in g["programs"]},
         "re_up_calls_usd_m": g["by_fund"],
         # the two judgments that decide the program
         "successor_events": succ, "successor_funds": [e["fund"] for e in succ],
         "successor_effect_usd_m": round(g["R5"] - fac["S1 dropped"]["R5"], 1),
         "clause_managers": sorted(m for m, v in R["clause"].items() if v[0] is True), "no_clause_managers": sorted(m for m, v in R["clause"].items() if v[0] is False),
         "clause_votes": {m: list(v[1]) for m, v in R["clause"].items() if v[1] is not None},
         "loans_due": R["loans_due"], "loans_due_count": len(R["loans_due"]),
         "loans_due_balance_usd_m": round(sum(x["D"] for x in R["loans_due"]), 1), "loans_due_gap_usd_m": round(sum(x["gap"] for x in R["loans_due"]), 1),
         "refinancing_calls_by_half_usd_m": g["refi"], "refinancing_calls_total_usd_m": round(sum(g["refi"].values()), 1),
         "refinancing_effect_usd_m": round(fac["S2 dropped"]["R5"] - g["R5"], 1),
         "lender_rule": fs(fit["lender"]), "value_response": fs(fit["value"]),
         # the reflexes' figures
         "line_stock_usd_m": R["line_stock_total"], "line_stock_six_managers_usd_m": R["line_stock_uncovered"],
         "line_stock_six_managers_audited_usd_m": R["line_stock_uncovered_audited"], "six_managers": R["uncovered"],
         "support_by_half_usd_m": g["support"], "support_total_usd_m": round(sum(g["support"].values()), 1), "support": fs(fit["support"]),
         "slip": {k: round(v, 4) for k, v in fit["slip"].items()}, "extension_rule": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in fit["ext"].items()},
         "pending_funds": R["pending"], "bands": B,
         "careful_route_programs": {p["code"]: {"calls_usd_m": p["calls"], "headroom_usd_m": p["headroom"], "passes": p["passes"]} for p in R["passes"]["careful"]["programs"]},
         "careful_route": {"program": R["passes"]["careful"]["R7"], "headroom_before_2027_usd_m": R["passes"]["careful"]["R5"],
                           "calls_by_half_usd_m": {**R["passes"]["careful"]["R2"], **R["passes"]["careful"]["R3"]}},
         "reflex_drops": {k: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]} for k, o in R["reflex_drops"].items()},
         "own_record_max_shortfall": R["own_record_max_shortfall"], "stress_max_shortfall": R["stress_max_shortfall"],
         "six_managers_live_funds": R["six_live_funds"], "past_first_closes": R["past_first_closes"],
         "routes": {n: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]} for n, o in R["routes"]},
         "partials": {n: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]} for n, o in R["partials"]},
         "family": {n: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]} for n, o in R["family"]},
         "factorial": {k: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"], "calls_by_half_usd_m": {**o["R2"], **o["R3"]}} for k, o in fac.items()},
         "bootstrap_p5_p95": {k: [round(float(np.percentile(v, 5)), 1), round(float(np.percentile(v, 95)), 1)] for k, v in R["boot"].items()},
         "bootstrap_programs": {k: {c: v.count(c) for c in sorted(set(v))} for k, v in R["boot_programs"].items()},
         "years": [2008, 2009, 2010, 2022, 2023, 2024, 2025, 2026, 2027, 2028], "exact_tolerance_usd_m": 0.5}
    json.dump(F, open(os.path.join(root, "figures.json"), "w"), indent=1, sort_keys=True)
    P = R["passes"]
    prec_calls = ["N28", "N03", "N13"]
    spec = [("R1", "commitments not yet called at 31 December 2026, by strategy", "Ask 1", "unfunded_by_strategy_usd_m", [], None, "R1"),
            ("R2", "capital calls in the policy's stress on the commitments made by the end of 2026, each half of 2027", "Component 2", "calls_2027_by_half_usd_m", [], prec_calls, "R2"),
            ("R3", "capital calls in the policy's stress on the commitments made by the end of 2026, each half of 2028", "Component 3", "calls_2028_by_half_usd_m", [], prec_calls, "R3"),
            ("R4", "distributions in the policy's stress, each half of 2027 and 2028", "Ask 2", "distributions_by_half_usd_m", [], None, "R4"),
            ("R5", "the headroom above the minimum reserve before any 2027 commitment", "Ask 3", "headroom_before_2027_usd_m", ["R2", "R3", "R4"], prec_calls, "R5"),
            ("R6", "the program the policy lets the Investment Committee adopt", "Recommendation", "program", ["R2", "R3", "R4"], prec_calls, "R7")]
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
    n_s = len(F["successor_funds"]); n_l = F["loans_due_count"]
    E = {"results": res,
         "hints": [{"sentence": "a fund's investment period ends when its manager's next fund holds its first close, and %d of the endowment's funds have a successor closing in 2027 or 2028" % n_s,
                    "rescues": rescued(R, B, fac["S1 alone"])},
                   {"sentence": "%d of the real-asset funds' property and infrastructure loans fall due in 2027 and 2028, and lenders will refinance them on the stressed rate and values" % n_l,
                    "rescues": rescued(R, B, fac["S2 alone"])}],
         "factorial": {"golden_answer": adopt, "reflex_route": {"answer": P["careful"]["R7"]}, "judgments": [
             {"id": "S1", "name": "the investment periods the successor funds' first closes end: the clause read off each manager's past successions, the close dated on the slip the exit market gives",
              "kind": "stump", "precedent": ["N28", "N03"], "dropped": {"answer": fac["S1 dropped"]["R7"], "results_moved": moved(R, B, fac["S1 dropped"])},
              "alone": {"answer": fac["S1 alone"]["R7"], "results_rescued": rescued(R, B, fac["S1 alone"])}},
             {"id": "S2", "name": "the property and infrastructure loans that fall due in the stress, refinanced at the lenders' limit fitted on the past refinancings, on the values the stress path gives, the gaps called",
              "kind": "stump", "precedent": ["N28", "N13"], "dropped": {"answer": fac["S2 dropped"]["R7"], "results_moved": moved(R, B, fac["S2 dropped"])},
              "alone": {"answer": fac["S2 alone"]["R7"], "results_rescued": rescued(R, B, fac["S2 alone"])}},
             {"id": "J1", "name": "the calls on companies already held past the endowment's own record read off the benchmark's funds past their investment period (policy section 8)", "kind": "reflex", "precedent": ["R51", "R64"]},
             {"id": "J2", "name": "the six managers' line balances estimated to 31 December from the capital accounts and the audits (policy section 8)", "kind": "reflex", "precedent": ["R75", "R63"]},
             {"id": "J3", "name": "the covered managers' capital invested on lines and not yet called, called at the clean-down", "kind": "reflex", "precedent": ["R63"]},
             {"id": "J4", "name": "defensive follow-ons on the held companies' cost, two quarters after the exit index, the plateau fitted", "kind": "reflex", "precedent": ["R64"]},
             {"id": "J5", "name": "pending funds' first closes slipped on the exit market", "kind": "reflex", "precedent": ["R65"]},
             {"id": "J6", "name": "investment periods extended where the register's record shows, new investment at the managers' pace (policy section 8)", "kind": "reflex", "precedent": ["R14", "R51"]},
             {"id": "J7", "name": "statements cleaned; distributions, reserve and spending as the policy sets them", "kind": "reflex", "precedent": ["R01", "R18"]},
             {"id": "J8", "name": "fees, recycling, the fits chosen by fit and back-tested, a bootstrap over funds", "kind": "reflex", "precedent": ["R14", "R36", "R66", "R04"]}]},
         "forcing": {"kind": "set", "golden_answer": adopt,
                     "golden_family": [{"name": "the golden", "answer": adopt}] + [{"name": n, "answer": o["R7"]} for n, o in R["family"]],
                     "shortcuts": [{"name": n, "answer": o["R7"]} for n, o in R["routes"][1:]],
                     "perturbations": [{"input": "%s at the bootstrap's %s" % (k, side), "answer": at_percentile(v, R["boot_programs"][k], pc)}
                                       for k, v in R["boot"].items() for side, pc in (("5th percentile", 5), ("95th percentile", 95))]},
         "routes": [{"name": n, "answer": o["R7"], "golden": i == 0} for i, (n, o) in enumerate(R["routes"])],
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    json.dump(E, open(os.path.join(root, "effort.json"), "w"), indent=1)
    return F, E
