"""Generator assertions for task20 architecture 4: the processes the golden fits are the world's own, the golden from the
pack tracks the world's 2027-28 under the stress, every rival and perturbation sits inside the band and every shortcut
outside it, the stump factorial holds, and the figures add up across the deliverables."""
import json
import os
import re
import sys

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
    print("%-4s %-74s %s" % ("PASS" if ok else "FAIL", name, detail))
    if not ok:
        fails.append(name)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    R = A.full(TGT)
    g = R["golden"]
    # the processes the golden fits are the world's own
    check("first-close slips: window and reference chosen by fit are the world's", (R["fit"]["slip"]["win"], R["fit"]["slip"]["ref"]) == (1, Wd.P["slip_ref"]),
          str(R["fit"]["slip"]))
    check("first-close slips: the fitted response within 10 per cent of the world's", abs(R["fit"]["slip"]["b"] / Wd.P["slip_k"] - 1) < 0.10, "%.3f" % R["fit"]["slip"]["b"])
    sp = R["fit"]["support"]
    check("defensive follow-ons: lag and threshold chosen by fit are the world's", (sp["lag"], sp["e_star"]) == (2, Wd.P["support_e"]), str(sp))
    check("defensive follow-ons: the fitted rate within 10 per cent of the world's", abs(sp["sigma"] / Wd.P["support"] - 1) < 0.10, "%.4f" % sp["sigma"])
    Wo = PK.build_world(); H = PK.history(Wo)
    reg = R["L"]["reg"]
    tl = sum(H[f]["o"]["line"][Wd.H_END] for f in H if reg[f]["Status"] != "liquidated")
    check("the credit-line stock rebuilt from the pack within 2 per cent of the world's", abs(F["line_stock_usd_m"] / tl - 1) < 0.02,
          "%.1f against %.1f" % (F["line_stock_usd_m"], tl))
    tr = T.truth(0.0)
    hv = lambda v: [float(v[Wd.W[2 * i:2 * i + 2]].sum()) for i in range(4)]
    ti, tp = hv(tr["call_inv"]), hv(tr["call_pend"])
    gi = [g["R2"][h] for h in A.HALVES]; gp = [g["R3"][h] for h in A.HALVES]
    check("calls of the closed funds by half within 6 per cent of the world's under the stress",
          all(abs(a - b) <= 0.06 * b + 1.0 for a, b in zip(gi, ti)), "golden %s world %s" % ([round(x, 1) for x in gi], [round(x, 1) for x in ti]))
    check("calls of the pending funds over the eight quarters within 20 per cent of the world's",
          abs(sum(gp) - sum(tp)) <= 0.20 * sum(tp), "golden %.1f world %.1f" % (sum(gp), sum(tp)))
    # bands
    lo, hi = FG.BANDS["R7"]
    fam = E["forcing"]["golden_family"]; pert = E["forcing"]["perturbations"]
    gold = E["forcing"]["golden_answer"]
    check("every golden-family method lands inside the band", all(x["answer"] == gold for x in fam), ", ".join("%s" % x["answer"] for x in fam))
    check("every perturbation by the bootstrap's spread lands inside the band", all(x["answer"] == gold for x in pert))
    for rid in ("R2", "R3", "R4", "R5", "R6"):
        offs = [n for n, o in R["family"] if not FG.inband(rid, o[rid], g[rid])]
        check("every golden-family method inside %s's bands" % rid, not offs, "; ".join(offs))
    out = [n for n, o in R["routes"][1:] if lo <= o["R7"] <= hi]
    check("every shortcut lands outside the band", not out, ", ".join("%s %s" % (n[:30], o["R7"]) for n, o in R["routes"][1:]))
    fac = R["factorial"]
    check("each stump dropped alone moves the budget outside the band", all(not (lo <= fac[k]["R7"] <= hi) for k in ("J1 dropped", "J2 dropped", "J3 dropped")),
          ", ".join("%s %d" % (k, fac[k]["R7"]) for k in fac))
    check("the three single drops land on three different budgets", len({fac[k]["R7"] for k in ("J1 dropped", "J2 dropped", "J3 dropped")}) == 3)
    check("no stump alone on the careful route reaches the band", all(not (lo <= fac[k]["R7"] <= hi) for k in ("J1 alone", "J2 alone", "J3 alone")))
    check("the drops land on both sides of the band", min(fac[k]["R7"] for k in fac) < lo and max(fac[k]["R7"] for k in fac) > hi)
    # arithmetic across the deliverables
    t5 = R["test_at"][500.0]
    check("calls of the closed funds by half add to the test's figure", abs(sum(g["R2"].values()) - t5["calls_closed"]) < 0.11)
    check("calls of the pending funds by half add to the test's figure", abs(sum(g["R3"].values()) - t5["calls_pending"]) < 0.11)
    check("distributions by half add to the test's figure", abs(sum(g["R4"].values()) - t5["distributions"]) < 0.11)
    check("net cash needs are spending plus calls less distributions",
          abs(t5["spending"] + t5["calls_closed"] + t5["calls_pending"] + t5["calls_budget"] - t5["distributions"] - t5["net"]) < 0.21)
    check("headroom is the reserve less the needs less the minimum", abs(t5["reserve"] - t5["net"] - t5["minimum"] - t5["headroom"]) < 0.01)
    check("the figures file and the test agree", F["net_cash_needs_500_usd_m"] == t5["net"] and F["headroom_500_usd_m"] == t5["headroom"])
    check("the budget sweep crosses zero between the answer and the next step", R["sweep"][F["capacity_usd_m"] // 25][1] >= 0 > R["sweep"][F["capacity_usd_m"] // 25 + 1][1])
    # the policy and the analysis read the same rule
    check("the policy's minimum reserve is the analysis's", DC.CUSHION == A.CUSHION)
    check("the policy's factors are the analysis's", all(DC.FACTORS[k] == v for k, v in A.FACTORS.items()))
    # the semantic forks (DESIGN_NOTE.md, Semantic fork table)
    L = R["L"]
    live = [f for f, r in L["reg"].items() if r["Status"] not in ("liquidated", "pending first close")]
    col = sum(L["st"][f][max(q for q in L["st"][f] if "unfunded_commitment_usd" in L["st"][f][q])]["unfunded_commitment_usd"] for f in live
              if any("unfunded_commitment_usd" in v for v in L["st"][f].values()))
    cash_late = sum(v.get("contributions_investments_usd", 0.0) for f in live for q, v in L["st"][f].items() if v.get("cash_only"))
    paid = sum(float(L["reg"][f]["Commitment (USD m)"]) - sum(v["contributions_investments_usd"] + v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"]
               for v in L["st"][f].values()) for f in live)
    check("SF1 commitment less contributions equals the statements' unfunded once the custodian's cash is in", abs(paid - (col - cash_late)) < 0.05,
          "%.2f against %.2f" % (paid, col - cash_late))
    released = [f for f, r in L["reg"].items() if r["Status"] == "liquidated"]
    check("SF1 every released commitment's final statement shows nothing unfunded", all(
        L["st"][f][max(q for q in L["st"][f] if "unfunded_commitment_usd" in L["st"][f][q])]["unfunded_commitment_usd"] == 0.0 for f in released))
    check("SF2 funds with a first close are every status but pending", {L["reg"][f]["Status"] for f in live} == {"investing", "harvesting"})
    fees = sum(v["contributions_management_fees_usd"] + v["contributions_fund_expenses_usd"] for f in live for v in L["st"][f].values())
    check("SF3 fees and expenses are called as contributions (the unfunded falls by them)", fees > 0 and abs(paid - (col - cash_late)) < 0.05, "%.1f called as fees and expenses" % fees)
    check("SF4 the spending is eight quarters of one quarter of FY2027's distribution", R["spending24"] == 2.0 * L["spend"][2027])
    mv = sum(float(h["Market value 31 Dec 2026 (USD m)"]) for h in L["hold"] if h["Policy liquidity class"])
    check("SF5 the reserve at the policy's factors, not market value", abs(R["reserve"] - A.reserve(L)) < 0.01 and R["reserve"] < mv)
    late = [x for x in R["states"] if not x["pending"] and A.H_END in L["st"].get(x["fid"], {}) and L["st"][x["fid"]][A.H_END].get("cash_only")]
    check("SF6 the late statements' value is 30 September plus the fourth quarter's cash", all(
        abs(x["nav"] - (L["st"][x["fid"]][A.H_END - 1]["ending_nav_usd"] + L["st"][x["fid"]][A.H_END]["contributions_investments_usd"]
                        - L["st"][x["fid"]][A.H_END]["distributions_return_of_capital_usd"])) < 1e-9 for x in late), "%d funds" % len(late))
    check("SF7 the distribution rate is the sum of distributions over the sum of values", all(0.0 <= v < 0.2 for v in R["fit"]["drate"].values()))
    e = R["fit"]["mkt"][0]
    check("SF8 the stress index is 2026Q4's level times 2008's path relative to 2008Q2",
          all(abs(e[A.W[k]] - L["E"][A.H_END] * L["E"][A.qi(2008, 3) + k] / L["E"][A.qi(2008, 2)]) < 1e-9 for k in range(8)))
    check("SF9 the budget is spread in the pacing plan's proportions", abs(sum(p["C"] for p in L["plan"]) - 500.0) < 1e-9)
    check("SF10 the answer is the largest multiple of USD 25 million that passes", F["capacity_usd_m"] % 25 == 0 and F["capacity_usd_m"] <= F["capacity_unrounded_usd_m"] < F["capacity_usd_m"] + 25)
    check("SF11 the headroom is net of the minimum reserve", abs(t5["left"] - t5["minimum"] - t5["headroom"]) < 0.01)
    check("SF12 the halves are calendar halves of 2027 and 2028", A.W[0] == A.qi(2027, 1) and A.W[-1] == A.qi(2028, 4))
    check("SF13 the plan's funds close where expected (same call)", all(p["slip"] < 0.1 for p in R["plan_slips"]))
    check("SF14 recycled proceeds net from calls; the policy's distributions taken as they are", sum(g["recycled"].values()) > 0)
    # the deliverables
    b = open(os.path.join(TASK, "golden", "commitment_budget_2027_memo.pdf"), "rb").read()
    check("the memo is one page", len(re.findall(rb"/Type\s*/Page[^s]", b)) == 1)
    sub = open(os.path.join(TASK, "submission.md")).read()
    check("no em dash in the answer blocks", "—" not in sub)
    src = open(os.path.join(HERE, "analysis.py")).read()
    check("the distractors are never read", all(n not in src for n in (DC.F_PEER, DC.F_CAPPLAN, DC.F_IPS)))
    check("the stated figures appear in the answer blocks", all(("%s" % format(x, ",.1f")) in sub for x in (F["capacity_unrounded_usd_m"], F["net_cash_needs_500_usd_m"])))
    print("\n%d failure%s" % (len(fails), "" if len(fails) == 1 else "s"))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
