"""Generator assertions for task20 architecture 6: the processes the golden fits are the world's own, the golden from the
pack tracks the world's 2027-28 under the stress and lands on the world's own program, every rival and perturbation
gives the golden program and every shortcut another, the stump factorial holds, and the figures add up across the
deliverables."""
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as DC  # noqa: E402
import figures as FG  # noqa: E402
import pack as PK  # noqa: E402
import truth as T  # noqa: E402
import world as Wd  # noqa: E402

TGT = os.path.join(TASK, "target")
fails = []


def check(name, ok, detail=""):
    print("%-4s %-78s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        fails.append(name)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    R = A.full5(TGT)
    g = R["golden"]; L = R["L"]; P = Wd.P
    # the processes the golden fits are the world's own
    sl = R["fit"]["slip"]
    check("first-close slips: window and reference chosen by fit are the world's", (sl["win"], sl["ref"]) == (1, P["slip_ref"]), str(sl))
    check("first-close slips: the fitted response within 10 per cent of the world's", abs(sl["b"] / P["slip_k"] - 1) < 0.10, "%.3f" % sl["b"])
    sp = R["fit"]["support"]
    check("defensive follow-ons: lag and threshold chosen by fit are the world's", (sp["lag"], sp["e_star"]) == (P["exit_lag"], P["support_e"]), str(sp))
    check("defensive follow-ons: the fitted rate within 10 per cent of the world's", abs(sp["sigma"] / P["support"] - 1) < 0.10, "%.4f" % sp["sigma"])
    check("defensive follow-ons: the cap chosen by fit is the world's reserve cap", abs(sp["cap"] - P["support_cap"]) < 1e-9, "%.2f" % sp["cap"])
    sfs = [max(0.0, 1.0 - R["mkt"][0][q - 2] / 100.0) for q in A.W]
    gr = lambda s: min(s, sp["cap"]) + sp["ratio"] * max(0.0, s - sp["th"]); wr = lambda s: min(s, P["support_cap"]) + P["rescue"] / P["support"] * max(0.0, s - P["rescue_th"])
    check("rescue financings: the two-channel response within 25 per cent of the world's at every shortfall the stress reaches",
          all(abs(gr(s) / wr(s) - 1) < 0.25 for s in sfs if s > 0.05), "threshold %.2f against %.2f, steepness %.2f against %.2f; worst %.3f" % (
              sp["th"], P["rescue_th"], sp["ratio"], P["rescue"] / P["support"], max(abs(gr(s) / wr(s) - 1) for s in sfs if s > 0.05)))
    check("the endowment's own record never reaches the second channel", A.own_record_max_shortfall(L) < sp["th"],
          "%.3f against %.2f" % (A.own_record_max_shortfall(L), sp["th"]))
    check("the stress takes the shortfall past the second channel's threshold",
          max(max(0.0, 1.0 - R["mkt"][0][q - 2] / 100.0) for q in A.W) > sp["th"])
    ex = R["fit"]["ext"]
    check("investment-period extensions: the length is the world's and the rule classes 85 per cent of the agreed ends or more",
          ex["length"] == P["ext_q"] and ex["accuracy"] >= 0.85, str(ex))
    # the line stock against the world's
    Wo = PK.build_world(); H = PK.history(Wo)
    reg = L["reg"]; six = set(L["cov"])
    aud_stock, _ = A.line_stock(L, bridge=True, uncovered="audited")
    tc = sum(H[f]["o"]["line"][Wd.H_END] for f in H if f in reg and reg[f]["Status"] != "liquidated" and reg[f]["Manager"] not in six)
    tu = sum(H[f]["o"]["line"][Wd.H_END] for f in H if f in reg and reg[f]["Status"] != "liquidated" and reg[f]["Manager"] in six)
    gc = F["line_stock_usd_m"] - F["line_stock_six_managers_usd_m"]
    check("the covered managers' line stock within 3 per cent of the world's", abs(gc / tc - 1) < 0.03, "%.1f against %.1f" % (gc, tc))
    check("the six managers' bridged stock within 25 per cent of the world's", abs(F["line_stock_six_managers_usd_m"] / tu - 1) < 0.25,
          "%.1f against %.1f" % (F["line_stock_six_managers_usd_m"], tu))
    check("their last audited borrowings fall well short of the world's stock (under half; the lines rebuilt through 2026)", F["line_stock_six_managers_audited_usd_m"] < 0.50 * tu,
          "%.1f against %.1f" % (F["line_stock_six_managers_audited_usd_m"], tu))
    check("six managers, their company-level rows stopping after 2024Q4", len(six) == 6 and all(
        L["cov"][m] == A.qi(2024, 4) for m in six), ", ".join(sorted(six)))
    # the successor clause and the successor closes against the world's
    Wf = {f["id"]: f for f in Wo["funds"]}
    gp_of = {fid: Wf[fid]["gp"] for fid in reg if fid in Wf}
    mgr_gp = {}
    for fid, g_ in gp_of.items(): mgr_gp[reg[fid]["Manager"]] = g_
    wrong = [m for m, v in R["clause"].items() if v[0] is not None and v[0] != mgr_gp[m]["succ_clause"]]
    check("S1 the clause read off each manager's past successions is its own", not wrong and sum(v[0] is not None for v in R["clause"].values()) >= 15,
          "%d managers read, %s" % (sum(v[0] is not None for v in R["clause"].values()), "; ".join(wrong) or "none wrong"))
    Es, Ss, Rs = Wd.stressed(Wo["E"], Wo["S"], Wo["R"])
    wev = set()
    for fid, r in reg.items():
        f = Wf.get(fid)
        if f is None or r["Status"] not in ("investing", "harvesting") or not f["gp"]["succ_clause"]: continue
        sq = PK.succ_fc(f, Es); ie = A._qd(r["Investment period ends"])
        if sq is not None and ie is not None and sq <= ie and A.W[0] <= sq <= A.W[-1]: wev.add(r["Fund"])
    gev = set(F["successor_funds"])
    unread = [r["Fund"] for fid, r in reg.items() if r["Fund"] in wev and R["clause"].get(r["Manager"], (None,))[0] is None]
    check("S1 the funds whose successors close inside the stress are the world's", gev == wev, "golden %s; world %s" % (sorted(gev), sorted(wev)))
    check("S1 no manager without a past succession has a successor closing inside the stress", not unread, "; ".join(unread) or "none")
    # the asset loans, the lenders and the values against the world's
    lr, vr = R["fit"]["lender"], R["fit"]["value"]
    check("S2 the lenders' cap since mid-2022 within 0.02 of the world's", abs(lr["cap_post"] - P["ltv_post"]) <= 0.02, "%.3f against %.2f" % (lr["cap_post"], P["ltv_post"]))
    r26 = float(L["R"][A.H_END]); rates = [r26, r26 + Wd.P["stress_rate_up"]]
    fl = lambda r: min(lr["cap_post"], lr["kappa"] / (r + lr["spread"])); wl = lambda r: min(P["ltv_post"], P["refi_kappa"] / (r + P["refi_spread"]))
    check("S2 the fitted lenders' limit within 0.02 of the world's at 31 December's rate and at the stressed rate",
          all(abs(fl(r) - wl(r)) <= 0.02 for r in rates), "; ".join("%.2f%%: %.3f against %.3f" % (r, fl(r), wl(r)) for r in rates))
    check("S2 the assets' equity sensitivity within 0.1 of the world's", abs(vr["beta"] - P["beta_p"]) <= 0.1, "%.3f against %.2f" % (vr["beta"], P["beta_p"]))
    check("S2 the assets' rate sensitivity within 0.006 of the world's", abs(vr["c"] - P["cap1"] / P["cap0"]) <= 0.006, "%.3f against %.4f" % (vr["c"], P["cap1"] / P["cap0"]))
    tr, tplan = T.truth()
    wdue = {}
    for fid, x in tr["due"]:
        if fid in reg and reg[fid]["Status"] in ("investing", "harvesting"): wdue.setdefault((fid, x[0]), []).append(x)
    wref = float(tr["refi"][A.W].sum())
    wrh = [float(tr["refi"][Wd.W[2 * i:2 * i + 2]].sum()) for i in range(4)]
    check("S2 the refinancing calls within 20 per cent of the world's under the stress", abs(F["refinancing_calls_total_usd_m"] / wref - 1) < 0.20,
          "golden %.1f world %.1f; by half golden %s world %s" % (F["refinancing_calls_total_usd_m"], wref,
                                                                 [F["refinancing_calls_by_half_usd_m"][h] for h in A.HALVES], [round(x, 1) for x in wrh]))
    # the calls against the world's under the stress, and the world's own program
    hv = lambda v: [float(v[Wd.W[2 * i:2 * i + 2]].sum()) for i in range(4)]
    ti, tp = hv(tr["call_inv"]), hv(tr["call_pend"])
    gi = [g["closed"][h] for h in A.HALVES]; gp = [g["pending"][h] for h in A.HALVES]
    check("calls of the closed funds by half within 8 per cent of the world's under the stress, and within 2 per cent over the eight quarters",
          all(abs(a - b) <= 0.08 * b + 1.0 for a, b in zip(gi, ti)) and abs(sum(gi) / sum(ti) - 1) < 0.02,
          "golden %s world %s" % ([round(x, 1) for x in gi], [round(x, 1) for x in ti]))
    check("calls of the pending funds over the eight quarters within 20 per cent of the world's",
          abs(sum(gp) - sum(tp)) <= 0.20 * sum(tp), "golden %.1f world %.1f" % (sum(gp), sum(tp)))
    check("each re-up's calls within 20 per cent of the world's", all(abs(F["re_up_calls_usd_m"][k] / v - 1) < 0.20 for k, v in tplan.items()),
          "; ".join("%s %.1f/%.1f" % (k.split()[0], F["re_up_calls_usd_m"][k], v) for k, v in tplan.items()))
    h0w = round(F["reserve_usd_m"] - F["spending_24m_usd_m"] - (sum(ti) + sum(tp) - sum(g["R4"].values())) - F["minimum_reserve_usd_m"], 1)
    passing = [pr for pr in L["programs"] if h0w - sum(tplan[f] for f in pr["funds"]) >= 0]
    world_prog = max(passing, key=lambda pr: pr["total"])["code"] if passing else "none"
    check("the world's own calls give the golden's program", world_prog == g["R7"], "world headroom %.1f, program %s" % (h0w, world_prog))
    check("the world's own headroom sits inside the headroom band", F["bands"]["R5"][0] <= h0w <= F["bands"]["R5"][1], "%.1f in %s" % (h0w, F["bands"]["R5"]))
    tr2, tplan2 = T.truth(policy=False)
    h0m = round(F["reserve_usd_m"] - F["spending_24m_usd_m"] - (float((tr2["call_inv"] + tr2["call_pend"])[Wd.W].sum()) - sum(g["R4"].values())) - F["minimum_reserve_usd_m"], 1)
    passing2 = [pr for pr in L["programs"] if h0m - sum(tplan2[f] for f in pr["funds"]) >= 0]
    prog2 = max(passing2, key=lambda pr: pr["total"])["code"] if passing2 else "none"
    check("the world's managers slowing in the weak deal market still give the golden's program", prog2 == g["R7"], "headroom %.1f, program %s" % (h0m, prog2))
    # forcing and bands
    gold = E["forcing"]["golden_answer"]
    fam = E["forcing"]["golden_family"]; pert = E["forcing"]["perturbations"]
    check("every golden-family method gives the golden program", all(x["answer"] == gold for x in fam), ", ".join(x["answer"] for x in fam))
    check("every perturbation by the bootstrap's spread gives the golden program", all(x["answer"] == gold for x in pert))
    check("every shortcut gives another program", all(x["answer"] != gold for x in E["forcing"]["shortcuts"]),
          ", ".join(x["answer"] for x in E["forcing"]["shortcuts"]))
    B = FG.bands(R)
    for rid in ("R2", "R3", "R5"):
        offs = [n for n, o in R["family"] if not FG.inband(B[rid], o[rid])]
        check("every golden-family method inside %s's bands" % rid, not offs, "; ".join(offs))
    car = R["passes"]["careful"]
    check("the careful route lands outside the bands of R2, R3 and R5", not any(FG.inband(B[r], car[r]) for r in ("R2", "R3", "R5")))
    prog_calls = {p["code"]: p["calls"] for p in g["programs"]}
    lo, hi = prog_calls[gold], min(v for k, v in prog_calls.items() if v > prog_calls[gold])
    check("the headroom band sits inside the golden program's window", lo <= B["R5"][0] and B["R5"][1] < hi, "%s inside [%.1f, %.1f)" % (B["R5"], lo, hi))
    check("the bootstrap's 5th to 95th percentiles sit inside the golden program's window",
          all(lo <= v[0] and v[1] < hi for v in F["bootstrap_p5_p95"].values()), str(F["bootstrap_p5_p95"]))
    fac = R["factorial"]
    check("each stump dropped alone moves the program", all(fac[k]["R7"] != gold for k in ("S1 dropped", "S2 dropped")),
          ", ".join("%s %s" % (k, fac[k]["R7"]) for k in fac))
    check("the two single drops land on different programs", fac["S1 dropped"]["R7"] != fac["S2 dropped"]["R7"])
    check("no stump fixed alone on the careful route reaches the golden program", all(fac[k]["R7"] != gold for k in ("S1 alone", "S2 alone")))

    check("the careful route misses the call", car["R7"] != gold, car["R7"])
    # arithmetic across the deliverables
    calls = sum(g["R2"].values()) + sum(g["R3"].values())
    check("calls by half split into closed and pending funds", all(abs(({**g["R2"], **g["R3"]})[h] - g["closed"][h] - g["pending"][h]) < 0.11 for h in A.HALVES))
    check("net cash needs are spending plus calls less distributions",
          abs(F["spending_24m_usd_m"] + calls - sum(g["R4"].values()) - F["net_needs_before_2027_usd_m"]) < 0.21)
    check("headroom is the reserve less the needs less the minimum",
          abs(F["reserve_usd_m"] - F["net_needs_before_2027_usd_m"] - F["minimum_reserve_usd_m"] - F["headroom_before_2027_usd_m"]) < 0.11)
    check("each program's calls are its re-ups' calls", all(abs(F["programs"][pr["code"]]["calls_usd_m"] - sum(F["re_up_calls_usd_m"][f] for f in pr["funds"])) < 0.11
                                                              for pr in L["programs"]))
    check("each program's headroom left is the headroom less its calls", all(
        abs(F["programs"][c]["headroom_usd_m"] - (F["headroom_before_2027_usd_m"] - v["calls_usd_m"])) < 0.11 for c, v in F["programs"].items()))
    check("the adopted program is the largest that passes", F["program"] == max((c for c, v in F["programs"].items() if v["passes"]),
                                                                                     key=lambda c: F["programs"][c]["total_usd_m"]))
    check("the unfunded total is the strategies' sum", abs(sum(F["unfunded_by_strategy_usd_m"].values()) - F["unfunded_total_usd_m"]) < 0.11)
    # the policy and the analysis read the same rule
    check("the policy's minimum reserve is the analysis's", DC.CUSHION == A.CUSHION)
    check("the policy's factors are the analysis's", all(DC.FACTORS[k] == v for k, v in A.FACTORS.items()))
    plan_by = {p["st"]: p["fund"] for p in L["plan"]}
    check("the plan's programs as read are the plan's as written", [(pr["code"], pr["funds"]) for pr in L["programs"]] ==
          [(c, [plan_by[{"BO": "BO", "GE": "GE", "VC": "VC", "RE": "RE", "PC": "PC"}[s]] for s in sts if s in plan_by]) for c, _, sts in DC.PROGRAMS])
    # the semantic forks (DESIGN_NOTE.md, Semantic fork table)
    live = [f for f, r in reg.items() if r["Status"] not in ("liquidated", "pending first close")]
    col = sum(L["st"][f][max(q for q in L["st"][f] if "unfunded_commitment_usd" in L["st"][f][q])]["unfunded_commitment_usd"] for f in live
              if any("unfunded_commitment_usd" in v for v in L["st"][f].values()))
    cash_late = sum(v.get("contributions_investments_usd", 0.0) for f in live for q, v in L["st"][f].items() if v.get("cash_only"))
    paid = sum(float(reg[f]["Commitment (USD m)"]) - sum(v["contributions_investments_usd"] + v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"]
               for v in L["st"][f].values()) for f in live)
    check("SF1 commitment less contributions equals the statements' unfunded once the custodian's cash is in", abs(paid - (col - cash_late)) < 0.05,
          "%.2f against %.2f" % (paid, col - cash_late))
    released = [f for f, r in reg.items() if r["Status"] == "liquidated"]
    check("SF1 every released commitment's final statement shows nothing unfunded", all(
        L["st"][f][max(q for q in L["st"][f] if "unfunded_commitment_usd" in L["st"][f][q])]["unfunded_commitment_usd"] == 0.0 for f in released))
    check("SF2 funds with a first close are every status but pending", {reg[f]["Status"] for f in live} == {"investing", "harvesting"})
    fees = sum(v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"] for f in live for v in L["st"][f].values())
    check("SF3 fees and expenses are called as contributions (the unfunded falls by them)", fees > 0, "%.1f called as fees and expenses" % fees)
    check("SF4 the spending is eight quarters of one quarter of FY2027's distribution", R["spending24"] == 2.0 * L["spend"][2027])
    mv = sum(float(h["Market value 31 Dec 2026 (USD m)"]) for h in L["hold"] if h["Policy liquidity class"])
    check("SF5 the reserve at the policy's factors, not market value", abs(R["reserve"] - A.reserve(L)) < 0.01 and R["reserve"] < mv)
    states = [A.fund_state(L, fid, R["stock"], bridge=True) for fid in reg]
    late = [x for x in states if not x.get("pending") and not x.get("liquidated") and A.H_END in L["st"].get(x["fid"], {})
            and L["st"][x["fid"]][A.H_END].get("cash_only")]
    check("SF6 the late statements' value is 30 September plus the fourth quarter's cash", len(late) > 0 and all(
        abs(x["nav"] - (L["st"][x["fid"]][A.H_END - 1]["ending_nav_usd"] + L["st"][x["fid"]][A.H_END]["contributions_investments_usd"]
                        - L["st"][x["fid"]][A.H_END]["distributions_return_of_capital_usd"])) < 1e-9 for x in late), "%d funds" % len(late))
    check("SF7 the distribution rate is the sum of distributions over the sum of values", all(0.0 <= v < 0.2 for v in R["fit"]["drate"].values()))
    e = R["mkt"][0]
    check("SF8 the stress index is 2026Q4's level times 2008's path relative to 2008Q2",
          all(abs(e[A.W[k]] - L["E"][A.H_END] * L["E"][A.qi(2008, 3) + k] / L["E"][A.qi(2008, 2)]) < 1e-9 for k in range(8)))
    check("SF9 each program is its re-ups at their proposed sizes", all(abs(pr["total"] - sum(p["C"] for p in L["plan"] if p["fund"] in pr["funds"])) < 1e-9
                                                                          for pr in L["programs"]))
    check("SF10 the program adopted is the largest total that passes, and the next larger fails", (lambda s: s[s.index(F["program"]) - 1] if s.index(F["program"]) > 0 else None)(
        sorted(F["programs"], key=lambda c: -F["programs"][c]["total_usd_m"])) is None or not F["programs"][(lambda s: s[s.index(F["program"]) - 1])(
        sorted(F["programs"], key=lambda c: -F["programs"][c]["total_usd_m"]))]["passes"])
    check("SF11 the headroom is net of the minimum reserve", abs(F["reserve_usd_m"] - F["net_needs_before_2027_usd_m"] - F["headroom_before_2027_usd_m"] - F["minimum_reserve_usd_m"]) < 0.11)
    check("SF12 the halves are calendar halves of 2027 and 2028", A.W[0] == A.qi(2027, 1) and A.W[-1] == A.qi(2028, 4))
    slips = [A.expected_slip(R["fit"], R["mkt"][0], p["exp_fc"]) for p in L["plan"]]
    check("SF13 the re-ups close where the plan expects (same call)", all(s < 0.1 for s in slips), ", ".join("%.2f" % s for s in slips))
    check("SF14 recycled proceeds net from calls; the policy's distributions taken as they are", R["fit"]["rho"] and max(R["fit"]["rho"].values()) > 0)
    pend = [f for f, r in reg.items() if r["Status"] == "pending first close"]
    check("SF15 the pending funds count in full among the commitments not yet called", abs(sum(float(reg[f]["Commitment (USD m)"]) for f in pend)
                                                                                            - sum(p["C"] for p in R["pending"])) < 1e-9 and len(pend) == len(R["pending"]))
    check("SF16 the headroom before any 2027 commitment carries no re-up", abs(F["headroom_before_2027_usd_m"] - R["golden"]["R5"]) < 1e-9)
    check("SF17 the calls of the commitments made by the end of 2026 include the pending funds'", sum(g["pending"].values()) > 0)
    ended = [x for x in states if not x.get("pending") and not x.get("liquidated") and x.get("term") is not None and x["term"] in A.W[:-1]]
    sw_ = dict(A.GOLDEN5); fit_, mkt_ = R["fit"], R["mkt"]
    late_calls = 0.0
    for x in ended:
        o_ = A.project2(L, [x], [], 0.0, sw_, fit_, mkt_)
        late_calls += sum(float(o_["call_inv"][q]) for q in A.W if q > x["term"])
    check("SF18 a fund whose term ends inside the stress calls nothing after it", len(ended) > 0 and late_calls == 0.0, "%d funds" % len(ended))
    plan_funds = {p["fund"] for p in L["plan"]}
    check("SF19 the successors' first closes are their managers' whether or not Wexmoor commits (re-ups among them)",
          any(e["successor"] in plan_funds for e in R["successor_events"]) and all(e["successor"] for e in R["successor_events"]),
          "; ".join("%s to %s" % (e["fund"], e["successor"]) for e in R["successor_events"]))
    pol = open(os.path.join(HERE, "docs.py")).read()
    part = {n: o for n, o in R["partials"]}
    check("SF20 values move with the stress outside sections 4 and 7 (policy section 6), the values held at 31 December keep the call",
          "values move with these paths" in pol and part["the assets' values held at 31 December while the lenders' terms move with the stress"]["R7"] == gold)
    j7 = [o for k, o in R["reflex_drops"].items() if k.startswith("J7")][0]
    check("SF21 no allowance for a slower deal market (policy section 8), a fitted deal-market term keeps the call",
          "No allowance is made for managers finding fewer new companies" in pol and j7["R7"] == gold, "%.1f %s" % (j7["R5"], j7["R7"]))
    lf = [o for n, o in R["family"] if n.startswith("the lenders' limit fitted")]
    check("SF22 the lenders' limit on the refinancings since mid-2022 or since 2020, or at the grid's next-best fit (same call)", all(o["R7"] == gold for o in lf))
    six_real = [f for f, r in reg.items() if r["Manager"] in six and A.STRATS[r["Strategy"]] in ("RE", "IN")]
    check("SF23 no property or infrastructure fund sits with the six managers, so every loan's record runs to 2026 (C1)", not six_real and all(
        reg[x["fid"]]["Manager"] not in six for x in F["loans_due"]), "%d loans due, none with the six" % len(F["loans_due"]))
    held = part["the six managers' held companies as their files last show them"]
    check("SF26 the six managers' held companies as their files last show them keep the call", held["R7"] == gold, "%.1f %s" % (held["R5"], held["R7"]))
    unk = [r["Fund"] for fid, r in reg.items() if r["Status"] in ("investing", "harvesting") and R["clause"].get(r["Manager"], (None,))[0] is None
           and (A.successor_close(L, R["fit"], R["mkt"][0], fid, A.GOLDEN5) or [(None, 0)])[0][0] is not None
           and A.W[0] <= A.successor_close(L, R["fit"], R["mkt"][0], fid, A.GOLDEN5)[0][0] <= A.W[-1]]
    check("SF24 no manager without a past succession has a successor closing inside the stress (same call)", not unk, "; ".join(unk) or "none")
    unsl = part["the successor's first close on its manager's date, unslipped, while the pending funds' own calls slip"]
    check("SF25 the successors' closes on their managers' dates, unslipped, keep the call", unsl["R7"] == gold, "%.1f %s" % (unsl["R5"], unsl["R7"]))
    # the deliverables
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("no em dash in the answer blocks", "—" not in sub)
    src = open(os.path.join(HERE, "analysis.py")).read()
    check("the distractors are never read", all(n not in src for n in (DC.F_PEER, DC.F_CAPPLAN, DC.F_IPS)))
    check("the stated figures appear in the answer blocks", all(format(x, ",.1f") in sub for x in (F["headroom_before_2027_usd_m"], F["refinancing_calls_total_usd_m"],
                                                                                                    F["successor_effect_usd_m"], F["line_stock_six_managers_usd_m"])))
    check("the answer blocks name the golden program first", sub.split("## Final Recommendation")[1].strip().startswith("Adopt program %s" % F["program"]))
    print("\n%d failure%s" % (len(fails), "" if len(fails) == 1 else "s"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
