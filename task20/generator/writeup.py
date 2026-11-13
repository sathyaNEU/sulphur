"""submission.md, every figure from figures.json."""
import analysis as A

def m(x, d=1):
    return format(x, ",.%df" % d)

def text(F, R):
    g = R["golden"]; b = F["bands"]; t5, t25 = R["test_at"][500.0], R["test_at"][250.0]
    rt = F["routes"]; fac = F["factorial"]
    careful = rt[[k for k in rt if k.startswith("the careful route")][0]]["capacity_usd_m"]
    ta = rt["the textbook pacing model on the capital accounts"]["capacity_usd_m"]
    ta23 = rt["the pacing model recalibrated on 2022 and 2023"]["capacity_usd_m"]
    bench = rt["the benchmark's 2008-10 call rates replayed on the commitments not yet called"]["capacity_usd_m"]
    audit = rt["the latest audited borrowings carried as the line stock at 31 December 2026"]["capacity_usd_m"]
    H = A.HALVES
    halves = lambda d, bd: "; ".join("%s %s (%s to %s)" % (h, m(d[h]), m(bd[h][0]), m(bd[h][1])) for h in H)
    pend = F["pending_funds"]; slips = sorted({p["slip"] for p in pend})
    sup = sum(F["defensive_follow_ons_by_half_usd_m"].values())
    unsl = sum(R["passes"]["careful"]["R3"].values())
    s, sl = F["support"], F["slip"]
    lo, hi = F["capacity_band_usd_m"]
    out = []
    out.append("# task20: Wexmoor University's endowment, the 2027 private-fund commitment budget\n")
    out.append("## Tags\n")
    out.append("**Domain:** Quantitative Finance, Liquidity, funding & balance-sheet risk (an endowment's private-fund commitment "
               "pacing under its liquidity policy: capital calls, distributions and first closes in a stressed exit market).")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## Final Recommendation\n")
    out.append("Approve a 2027 private-fund budget of no more than USD %d million (USD %s million before the policy's USD 25 million "
               "steps; band USD %d million to USD %d million), not Corrigan Hart's USD 500 million, which fails the liquidity policy "
               "by USD %s million. Not the careful reading that takes the gap between the managers' investments and the capital "
               "called as recycled proceeds, gives every follow-on one pace and closes the pending funds on their managers' dates "
               "(USD %d million), nor the textbook pacing model on the capital accounts (USD %d million)."
               % (F["capacity_usd_m"], m(F["capacity_unrounded_usd_m"]), lo, hi, m(-t5["headroom"]), careful, ta))
    out.append("\n## Supplementary Questions\n")
    out.append("### wexmoor_2027_commitment_capacity.xlsx\n")
    out.append("1. Sheet Summary opens on the largest budget that passes and sets out the policy's test at a USD 500 million and a "
               "USD 250 million budget (reserve, spending, calls by group, distributions, net cash needs, the reserve left, the "
               "minimum and the headroom); sheet By half-year has the calls and distributions by half-year with what makes up the "
               "calls of the funds that have held a first close; sheets Unfunded, Credit-line stock, First closes, Fitted inputs, "
               "Budget sweep (with a chart of the headroom by budget) and Sensitivity carry the figures below.")
    out.append("2. The largest 2027 total that passes, in USD million: %d (USD %s million before the policy's USD 25 million steps; "
               "band %d to %d)." % (F["capacity_usd_m"], m(F["capacity_unrounded_usd_m"]), lo, hi))
    out.append("3. At a USD 500 million budget, in USD million: the policy's net cash needs over 2027 and 2028 %s (%s to %s); the "
               "headroom above the minimum reserve %s (%s to %s), so the budget fails."
               % (m(F["net_cash_needs_500_usd_m"]), m(b["R5"][0], 0), m(b["R5"][1], 0), m(F["headroom_500_usd_m"]), m(b["R6"][0], 0), m(b["R6"][1], 0)))
    out.append("4. Capital calls in the policy's stress on the commitments made by the end of 2026 to funds that have held a first "
               "close, in USD million (band in brackets): %s." % halves(g["R2"], b["R2"]))
    out.append("5. Capital calls in the policy's stress on the commitments made by the end of 2026 to funds yet to hold a first "
               "close, in USD million (band in brackets): %s." % halves(g["R3"], b["R3"]))
    out.append("6. Distributions in the policy's stress on the commitments made by the end of 2026, in USD million (band in "
               "brackets): %s." % halves(g["R4"], b["R4"]))
    out.append("7. Commitments not yet called at 31 December 2026, by strategy, in USD million (each within 0.5): %s; %s in all."
               % ("; ".join("%s %s" % (k, m(v)) for k, v in g["R1"].items()), m(F["unfunded_total_usd_m"])))
    out.append("\n### commitment_budget_2027_memo.pdf\n")
    out.append("8. One page to the Investment Committee from the Director of Private Markets: the recommendation and the test at USD "
               "500 million first, then the three things in the endowment's records that decide the number, a table of the calls "
               "and distributions by half-year, and the commitments not yet called.")
    out.append("\n## Critical Components\n")
    out.append("1. The test at USD 500 million (synthesis): the reserve of **USD %s million** less net cash needs of **USD %s million** "
               "leaves USD %s million, **USD %s million below** the USD %s million minimum; a USD %d million budget leaves **USD %s "
               "million** above it." % (m(t5["reserve"]), m(t5["net"]), m(t5["left"]), m(-t5["headroom"]), m(t5["minimum"], 0),
                                        F["capacity_usd_m"], m(t25["headroom"])))
    out.append("2. The calls of the funds that have held a first close (decomposition and modeling): **USD %s million** in the first "
               "half of 2027, of which **USD %s million** is capital the managers had invested on their funds' subscription lines "
               "at 31 December and call at the clean-down; defensive follow-ons add **USD %s million** over the eight quarters "
               "(USD %s to %s million across the defensible fits)." % (m(g["R2"]["H1 2027"]), m(F["line_stock_usd_m"]), m(sup),
                                                                      m(F["defensive_follow_ons_range_usd_m"][0]), m(F["defensive_follow_ons_range_usd_m"][1])))
    out.append("3. The calls of the funds yet to close (forecasting): **nothing in 2027**, **USD %s million** and **USD %s million** in "
               "the two halves of 2028, the four funds' first closes slipping %s quarters." % (m(g["R3"]["H1 2028"]), m(g["R3"]["H2 2028"]),
                                                                                             " and ".join(m(x, 1) for x in slips)))
    out.append("\n## Step-by-Step\n")
    out.append("1. Assemble the commitments: the capital account statements less the superseded row, the custodian's fourth-quarter "
               "cash for the funds whose statement has not arrived, the commitments released at a fund's term end left out and the "
               "four funds yet to close counted in full: USD %s million not yet called at 31 December 2026." % m(F["unfunded_total_usd_m"]))
    out.append("2. The reserve and the spending: the year-end holdings at the policy's factors, USD %s million; eight quarters of a "
               "quarter of FY2027's approved USD %s million distribution, USD %s million." % (m(F["reserve_usd_m"]), m(R["L"]["spend"][2027]), m(F["spending_24m_usd_m"])))
    out.append("3. Distributions as the policy sets them: each fund's 31 December value (the late statements' 30 September value "
               "plus the fourth quarter's calls less its distributions) times its strategy's 2008Q3 to 2010Q2 benchmark rate, "
               "the benchmark funds' distributions over their previous-quarter value: %s." % "; ".join("%s %s" % (h, m(g["R4"][h])) for h in H))
    out.append("4. The capital invested and not yet called: for each fund, the endowment's share of the investments in the managers' "
               "activity less the investment capital it was called for; at each audited year-end the part not on the fund's credit "
               "facility (borrowings at the endowment's share) is proceeds recycled, carried to the end of 2026 at the manager's own "
               "recycling rate: USD %s million on the lines at 31 December. The 2022 and 2023 calls show each manager cleaning its "
               "lines down once the line's all-in cost passed its own limit; the stress's %s per cent short rate passes every "
               "manager's limit, so the stock is called in the first quarter of 2027. Reading the whole gap as recycled proceeds leaves it out "
               "and gives USD %d million." % (m(F["line_stock_usd_m"]), m(R["L"]["R"][A.H_END] + 2.5, 2), fac["J1 dropped"]["capacity_usd_m"]))
    out.append("5. New deals and planned follow-ons: each strategy's pace on the room left by year since first close, the deal "
               "market's elasticity on the exit index %s; fees on the commitment while investing and on the cost held afterwards; "
               "recycling at each manager's rate." % m(F["deal_market_elasticity"], 2))
    out.append("6. Defensive follow-ons: follow-ons into companies held two years or more, as a share of those companies' cost each "
               "quarter, rise once the exit index two quarters earlier sits below %d (%s per cent of the cost a quarter for each 10 "
               "points below, or about half that on the companies' latest value, which carries the same calls; the threshold and "
               "the lag chosen by fit on 2020 and 2022 to 2024). On the stress path they add USD %s million while new deals slow. One investment pace for every follow-on misses the rise and gives USD %d million."
               % (round(100 * s["e_star"]), m(10 * s["sigma"] / s["e_star"], 2), m(sup), fac["J2 dropped"]["capacity_usd_m"]))
    out.append("7. First closes: on the register's closes, a fund's first close slips %s quarters for each 10 points the exit index "
               "sat below %d in the quarter before (window and reference chosen by fit). On the stress path the three funds due in "
               "the third quarter of 2027 slip %s quarters and the one due in the fourth %s, so the four close in 2028: USD %s million "
               "of calls in the eight quarters, not the USD %s million their managers' dates give. On those dates the budget is USD %d "
               "million." % (m(sl["b"] * 10 / sl["ref"], 2), round(sl["ref"]), m(slips[0], 1), m(slips[-1], 1), m(sum(g["R3"].values())), m(unsl),
                             fac["J3 dropped"]["capacity_usd_m"]))
    out.append("8. The budget: spread across the pacing plan's funds in its proportions, each USD 100 million calls USD %s million over "
               "the eight quarters; at USD 500 million the net cash needs are USD %s million and the headroom USD %s million; the "
               "largest budget that passes is USD %s million, USD %d million in the policy's steps."
               % (m(F["calls_per_100_of_budget_usd_m"]), m(F["net_cash_needs_500_usd_m"]), m(F["headroom_500_usd_m"]),
                  m(F["capacity_unrounded_usd_m"]), F["capacity_usd_m"]))
    out.append("9. The shortcuts land elsewhere: the careful route USD %d million; the pacing model on the capital accounts USD %d "
               "million, recalibrated on 2022 and 2023 USD %d million; the benchmark's 2008-10 call rates replayed USD %d million; "
               "the latest audited borrowings carried as the line stock USD %d million; each of the three judgments alone on the "
               "careful route USD %s, %s and %s million."
               % (careful, ta, ta23, bench, audit, m(fac["J1 alone"]["capacity_usd_m"], 0), m(fac["J2 alone"]["capacity_usd_m"], 0), m(fac["J3 alone"]["capacity_usd_m"], 0)))
    out.append("\nNo other conclusion survives the records. The calls of 2027 and 2028 are the managers' own: capital they have "
               "already invested on credit and will call when the stress makes the credit dear, defensive money into the companies "
               "they cannot sell, and new deals that slow; the pending funds call only once they close, and the register shows "
               "closes slipping when exits are weak. Each of the three moves the budget outside the band on its own, in different "
               "directions, and every rival fit, the bootstrap's spread over funds and the next-best windows keep it between USD %d "
               "and USD %d million, well short of USD 500 million." % (lo, hi))
    return "\n".join(out) + "\n"
