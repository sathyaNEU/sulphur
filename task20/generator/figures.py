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
    exact = lambda v: [v, v]
    return {"R1": {s: [round(v - 0.5, 1), round(v + 0.5, 1)] for s, v in g["R1"].items()},
            "R4": {h: [round(v - 0.5, 1), round(v + 0.5, 1)] for h, v in g["R4"].items()},
            "calls": {h: span(lambda o, h=h: o["calls"][h], 6.0) for h in A.HALVES},
            "R5": span(lambda o: o["R5"], 8.0),
            "succ": {"funds": exact(g["succ"]["funds"]), "calls_taken_off_usd_m": span(lambda o: o["succ"]["calls_taken_off_usd_m"], 8.0)},
            "refi_res": {"loans_due": exact(g["refi_res"]["loans_due"]),
                         "balance_due_usd_m": [round(g["refi_res"]["balance_due_usd_m"] - 0.5, 1), round(g["refi_res"]["balance_due_usd_m"] + 0.5, 1)],
                         "calls_usd_m": span(lambda o: o["refi_res"]["calls_usd_m"], 8.0)}}

def inband(b, v):
    if isinstance(b, dict):
        return all(b[k][0] - 1e-9 <= v[k] <= b[k][1] + 1e-9 for k in b)
    return b[0] - 1e-9 <= v <= b[1] + 1e-9

GRADED = (("R2", "succ"), ("R3", "refi_res"), ("R5", "calls"), ("R6", "R5"))      # chain id, the key evaluate() files it under

def moved(R, B, o):
    """the graded results a route files outside their bands, the program included."""
    out = [rid for rid, k in GRADED if not inband(B[k], o[k])]
    return out + (["R7"] if o["R7"] != R["golden"]["R7"] else [])

def rescued(R, B, o):
    """the results a route files inside their bands that the careful pass does not."""
    c = R["passes"]["careful"]
    out = [rid for rid, k in GRADED if inband(B[k], o[k]) and not inband(B[k], c[k])]
    return out + (["R7"] if o["R7"] == R["golden"]["R7"] and c["R7"] != R["golden"]["R7"] else [])

def at_percentile(vals, progs, pc):
    """the program of the bootstrap draw nearest a percentile of the headroom."""
    v = np.array(vals); t = float(np.percentile(v, pc)); i = int(np.argmin(np.abs(v - t)))
    return progs[i]

def window(g):
    """the golden program's window: the headroom that covers its calls and not the next larger program's."""
    calls = {p["code"]: p["calls"] for p in g["programs"]}
    lo = calls[g["R7"]]; above = [v for v in calls.values() if v > lo]
    return lo, (min(above) if above else float("inf"))

def write(R, root):
    g = R["golden"]; fit = R["fit"]; B = bands(R); fac = R["factorial"]
    progs = {p["code"]: p for p in g["programs"]}
    adopt = g["R7"]
    fs = lambda d: {k: (round(v, 4) if isinstance(v, float) else v) for k, v in d.items() if k != "pts"}
    succ = R["successor_events"]
    lo, hi = window(g)
    brief = lambda o: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"]}
    crate = fit["crate"]
    F = {"program": adopt, "program_total_usd_m": progs[adopt]["total"] if adopt in progs else 0.0,
         "headroom_before_2027_usd_m": g["R5"], "reserve_usd_m": R["reserve"], "spending_24m_usd_m": R["spending24"],
         "minimum_reserve_usd_m": R["cushion"], "net_needs_before_2027_usd_m": round(R["spending24"] + g["need0"], 1),
         "calls_2027_by_half_usd_m": g["R2"], "calls_2028_by_half_usd_m": g["R3"], "calls_by_half_usd_m": g["calls"], "distributions_by_half_usd_m": g["R4"],
         "successor_result": g["succ"], "refinancing_result": g["refi_res"],
         "calls_total_usd_m": round(sum(g["R2"].values()) + sum(g["R3"].values()), 1), "distributions_total_usd_m": round(sum(g["R4"].values()), 1),
         "calls_closed_by_half_usd_m": g["closed"], "calls_pending_by_half_usd_m": g["pending"],
         "unfunded_by_strategy_usd_m": g["R1"], "unfunded_total_usd_m": round(sum(g["R1"].values()), 1),
         "programs": {p["code"]: {"total_usd_m": p["total"], "calls_usd_m": p["calls"], "headroom_usd_m": p["headroom"], "passes": p["passes"]} for p in g["programs"]},
         "re_up_calls_usd_m": g["by_fund"],
         "window_usd_m": [lo, hi], "margin_below_usd_m": round(g["R5"] - lo, 1), "margin_above_usd_m": round(hi - g["R5"], 1),
         # the two judgments that decide the program
         "successor_events": succ, "successor_funds": [e["fund"] for e in succ],
         "successor_effect_usd_m": g["succ"]["calls_taken_off_usd_m"],
         "clause_managers": sorted(m for m, v in R["clause"].items() if v[0] is True), "no_clause_managers": sorted(m for m, v in R["clause"].items() if v[0] is False),
         "clause_votes": {m: list(v[1]) for m, v in R["clause"].items() if v[1] is not None},
         "past_successions": sum(v[1][1] for v in R["clause"].values() if v[1] is not None),
         "loans_due": R["loans_due"], "loans_due_count": len(R["loans_due"]),
         "loans_due_balance_usd_m": g["refi_res"]["balance_due_usd_m"], "loans_due_gap_usd_m": round(sum(x["gap"] for x in R["loans_due"]), 1),
         "refinancing_calls_by_half_usd_m": g["refi"], "refinancing_calls_total_usd_m": g["refi_res"]["calls_usd_m"],
         "refinancing_effect_usd_m": round(fac["S2 dropped"]["R5"] - g["R5"], 1),
         "lender_rule": fs(fit["lender"]), "value_response": fs(fit["value"]),
         "refinancings_in_record": R["refinancings"], "refinancings_short_in_record": R["refinancings_short"],
         "lender_limit_stressed": round(min(fit["lender"]["cap_post"], fit["lender"]["kappa"] / (float(R["mkt"][2][A.W[0]]) + fit["lender"]["spread"])), 3),
         "stressed_rate_pct": round(float(R["mkt"][2][A.W[0]]), 2), "rate_31dec_pct": round(float(R["mkt"][2][A.H_END]), 2),
         # what the policy sets and the rest of the evidence
         "line_stock_usd_m": R["line_stock_total"], "line_stock_audited_usd_m": R["line_stock_audited"],
         "new_investments_by_half_usd_m": g["new"], "new_investments_total_usd_m": round(sum(g["new"].values()), 1),
         "fees_by_half_usd_m": g["fees"], "fees_total_usd_m": round(sum(g["fees"].values()), 1),
         "fees_before_cap_usd_m": round(sum(dict(R["readings"])["no cap at the commitment a fund has left"]["fees"].values()), 1),
         "old_fund_calls_by_half_usd_m": g["old"], "old_fund_calls_total_usd_m": round(sum(g["old"].values()), 1),
         "old_funds_31dec": R["old_funds_31dec"], "old_funds_value_usd_m": R["old_funds_value"], "benchmark_vintage_years": A.OLD_YEARS,
         "old_fund_rate_8q_pct": {st: round(100 * sum(crate.get((st, k), 0.0) for k in range(8)), 2) for st in A.EQUITY},
         "old_fund_rates_pct": {st: [round(100 * crate.get((st, k), 0.0), 3) for k in range(8)] for st in A.EQUITY},
         "pace_pct": {"%s year %d" % (st, a + 1): round(100 * v, 2) for (st, a), v in sorted(fit["pace"].items())},
         "extension_rule": {k: (round(v, 3) if isinstance(v, float) else v) for k, v in fit["ext"].items()},
         "extended_commitments_usd_m": dict(R["family"])["investment periods extended in the stress as the register shows past weak exit markets extended them"]["extended"],
         "fee_rate_pct": {st: round(100 * v, 3) for st, v in sorted(fit["fee"].items())}, "expense_rate_pct": {st: round(100 * v, 3) for st, v in sorted(fit["exp"].items())},
         "pending_funds": R["pending"], "late_statements": R["late_statements"], "bands": B,
         "careful_route_programs": {p["code"]: {"calls_usd_m": p["calls"], "headroom_usd_m": p["headroom"], "passes": p["passes"]} for p in R["passes"]["careful"]["programs"]},
         "careful_route": {"program": R["passes"]["careful"]["R7"], "headroom_before_2027_usd_m": R["passes"]["careful"]["R5"],
                           "calls_by_half_usd_m": {**R["passes"]["careful"]["R2"], **R["passes"]["careful"]["R3"]}},
         "reflex_drops": {k: brief(o) for k, o in R["reflex_drops"].items()},
         "routes": {n: brief(o) for n, o in R["routes"]},
         "readings": {n: brief(o) for n, o in R["readings"]},
         "ruled_out": {n: brief(o) for n, o in R["ruled_out"]},
         "perturbations": {n: brief(o) for n, o in R["perturb"]},
         "partials": {n: brief(o) for n, o in R["partials"]},
         "family": {n: brief(o) for n, o in R["family"]},
         "factorial": {k: {"program": o["R7"], "headroom_before_2027_usd_m": o["R5"], "calls_by_half_usd_m": {**o["R2"], **o["R3"]}} for k, o in fac.items()},
         "bootstrap_p5_p95": {k: [round(float(np.percentile(v, 5)), 1), round(float(np.percentile(v, 95)), 1)] for k, v in R["boot"].items()},
         "bootstrap_programs": {k: {c: v.count(c) for c in sorted(set(v))} for k, v in R["boot_programs"].items()},
         "years": [2008, 2009, 2010, 2020, 2022, 2023, 2024, 2025, 2026, 2027, 2028], "exact_tolerance_usd_m": 0.5}
    json.dump(F, open(os.path.join(root, "figures.json"), "w"), indent=1, sort_keys=True)
    P = R["passes"]
    spec = [("R1", "commitments not yet called at 31 December 2026, by strategy", "Ask 1", "unfunded_by_strategy_usd_m", [], None, "R1", "R1"),
            ("R2", "the successor closes: the funds whose investment periods their managers' next funds' first closes end inside the eight quarters, and the calls that takes off",
             "Component 3", "successor_result", [], ["N28", "N03"], "succ", "succ"),
            ("R3", "the refinancing calls: the property and infrastructure loans that fall due in the eight quarters, their balance and the shortfalls the funds call",
             "Component 2", "refinancing_result", [], ["N28", "N13"], "refi_res", "refi_res"),
            ("R4", "distributions in the policy's stress, each half of 2027 and 2028", "Ask 2", "distributions_by_half_usd_m", [], None, "R4", "R4"),
            ("R5", "capital calls in the policy's stress on the commitments made by the end of 2026, each half of 2027 and 2028", "Ask 3", "calls_by_half_usd_m",
             ["R2", "R3"], ["N28", "N03", "N13"], "calls", "calls"),
            ("R6", "the headroom above the minimum reserve before any 2027 commitment", "Ask 4", "headroom_before_2027_usd_m", ["R4", "R5"], ["N28", "N03", "N13"], "R5", "R5"),
            ("R7", "the program the policy lets the Investment Committee adopt", "Recommendation", "program", ["R6"], ["N28", "N03", "N13"], "R7", None)]
    res = []
    for rid, name, ga, fig, dep, prec, key, bkey in spec:
        r = {"id": rid, "name": name, "graded_as": ga, "figure": fig, "depends": dep, "independent": "", "golden": g[key]}
        if bkey is None:
            pass
        elif isinstance(B[bkey], dict):
            r["bands"] = B[bkey]; r["partly_share"] = 0.5
        else:
            r["band"] = B[bkey]
        if prec: r["precedent"] = prec
        r["passes"] = {p: P[p][key] for p in ("quick", "careful", "thorough")}
        res.append(r)
    n_s = len(F["successor_funds"]); n_l = F["loans_due_count"]
    s1 = "the investment periods the successor funds' first closes end: the clause read off each manager's past successions, each live fund's successor found among the pending funds and the plan, the period cut at its first close"
    s2 = "the property and infrastructure loans that fall due in the stress, refinanced at the lenders' limit fitted on the past refinancings, on the values the stress path gives, the shortfalls called within each fund's commitment"
    E = {"results": res,
         "hints": [{"sentence": "a fund's investment period ends when its manager's next fund holds its first close, and %d of the endowment's funds have a successor closing in 2027 or 2028" % n_s,
                    "rescues": rescued(R, B, fac["S1 alone"])},
                   {"sentence": "%d of the real-asset funds' property and infrastructure loans fall due in 2027 and 2028, and lenders will refinance them on the stressed rate and values" % n_l,
                    "rescues": rescued(R, B, fac["S2 alone"])}],
         "factorial": {"golden_answer": adopt, "reflex_route": {"answer": P["careful"]["R7"]}, "judgments": [
             {"id": "S1", "name": s1, "kind": "stump", "precedent": ["N28", "N03"],
              "dropped": {"answer": fac["S1 dropped"]["R7"], "results_moved": moved(R, B, fac["S1 dropped"])},
              "alone": {"answer": fac["S1 alone"]["R7"], "results_rescued": rescued(R, B, fac["S1 alone"])}},
             {"id": "S2", "name": s2, "kind": "stump", "precedent": ["N28", "N13"],
              "dropped": {"answer": fac["S2 dropped"]["R7"], "results_moved": moved(R, B, fac["S2 dropped"])},
              "alone": {"answer": fac["S2 alone"]["R7"], "results_rescued": rescued(R, B, fac["S2 alone"])}},
             {"id": "J1", "name": "the capital invested through the credit facilities and not yet called, as policy section 8 files it (the latest audited borrowings plus the investments since less the capital called for them since, counted in the first quarter)", "kind": "reflex", "precedent": ["R63", "R18"]},
             {"id": "J2", "name": "buyout, growth and venture funds past their investment periods on the benchmark's rate as policy section 8 files it (the vintage rule, the value basis, the whole rate)", "kind": "reflex", "precedent": ["R18", "R51"]},
             {"id": "J3", "name": "the pace of new investments as policy section 8 files it (first and follow-on investments over the commitment not yet invested, by strategy and year since first close)", "kind": "reflex", "precedent": ["R18", "R14"]},
             {"id": "J4", "name": "first closes still to come on their managers' dates (policy section 8)", "kind": "reflex", "precedent": ["R18"]},
             {"id": "J5", "name": "statements cleaned; distributions, reserve, spending and the cap at the commitment as the policy sets them", "kind": "reflex", "precedent": ["R01", "R18"]},
             {"id": "J6", "name": "fees and expenses as policy section 8 files them (each fund's latest statement; the strategy's median quarter for a fund yet to close)", "kind": "reflex", "precedent": ["R18", "R14"]}]},
         "forcing": {"kind": "set", "golden_answer": adopt,
                     "golden_family": [{"name": "the golden", "answer": adopt}] + [{"name": n, "answer": o["R7"]} for n, o in R["family"]],
                     "shortcuts": [{"name": n, "answer": o["R7"]} for n, o in R["routes"][1:]],
                     "perturbations": [{"input": "%s at the bootstrap's %s" % (k, side), "answer": at_percentile(v, R["boot_programs"][k], pc)}
                                       for k, v in R["boot"].items() for side, pc in (("5th percentile", 5), ("95th percentile", 95))]
                                      + [{"input": n, "answer": o["R7"]} for n, o in R["perturb"]]
                                      + [{"input": n, "answer": o["R7"]} for n, o in R["readings"]]},
         "routes": [{"name": n, "answer": o["R7"], "golden": i == 0} for i, (n, o) in enumerate(R["routes"])],
         "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7}}
    json.dump(E, open(os.path.join(root, "effort.json"), "w"), indent=1)
    return F, E
