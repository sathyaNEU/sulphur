"""submission.md, every figure from figures.json."""
import analysis as A
import golden as GD

def m(x, d=1):
    return format(x, ",.%df" % d)

def text(F, R):
    g = R["golden"]; b = F["bands"]; L = R["L"]; s_ = F["support"]
    rt = F["routes"]; fac = F["factorial"]; pr = F["programs"]; adopt = F["program"]
    H = A.HALVES
    funds = next(x for x in L["programs"] if x["code"] == adopt)["funds"] if adopt != "none" else []
    cells = lambda d, bd: "; ".join("%s %s (%s to %s)" % (h, m(d[h]), m(bd[h][0]), m(bd[h][1])) for h in d)
    careful = [v for k, v in rt.items() if k.startswith("the careful route")][0]["program"]
    ta = rt["the textbook pacing model on the capital accounts"]["program"]
    sup = F["support_total_usd_m"]
    out = []
    out.append("# task20: Wexmoor University's endowment, the 2027 private-fund program\n")
    out.append("## Tags\n")
    out.append("**Domain:** Quantitative Finance, Liquidity, funding & balance-sheet risk (an endowment's private-fund commitment "
               "program under its liquidity policy: capital calls in a stressed exit market).")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## Final Recommendation\n")
    out.append("Adopt program %s, %s (%s, USD %s million), and defer the other re-ups to 2028: before any 2027 commitment the "
               "policy's stress leaves USD %s million above the USD %s million minimum, enough for %s's USD %s million of calls but not "
               "for program C's USD %s million, B's USD %s million or A's USD %s million. Not the careful reading that holds the "
               "support curve flat past the shortfall the endowment's record reaches and carries the six managers' last audited "
               "borrowings (program %s), nor the textbook pacing model on the capital accounts (program %s)."
               % (adopt, GD.NAMES.get(adopt, ""), "; ".join(funds), m(F["program_total_usd_m"], 0), m(F["headroom_before_2027_usd_m"]),
                  m(F["minimum_reserve_usd_m"], 0), adopt, m(pr[adopt]["calls_usd_m"]), m(pr["C"]["calls_usd_m"]), m(pr["B"]["calls_usd_m"]),
                  m(pr["A"]["calls_usd_m"]), careful, ta))
    out.append("\n## Supplementary Questions\n")
    out.append("### %s\n" % GD.XLSX)
    out.append("1. Sheet Summary opens on the program the policy lets the Committee adopt, sets out the test before any 2027 "
               "commitment (reserve, spending, calls, distributions, net cash needs, the minimum and the headroom) and each "
               "program's new commitments, calls, headroom left and result, with a chart of the headroom left; sheets By "
               "half-year, Re-ups, Unfunded, Credit-line stock, Support response and Sensitivity carry the figures below.")
    out.append("2. The program that can be adopted: %s (%s; USD %s million of new commitments); A, B and C fail." % (adopt, "; ".join(funds), m(F["program_total_usd_m"], 0)))
    out.append("3. The headroom above the minimum reserve before any 2027 commitment, in USD million: %s (%s to %s)." % (m(F["headroom_before_2027_usd_m"]), m(b["R5"][0]), m(b["R5"][1])))
    out.append("4. Capital calls in the policy's stress on the commitments made by the end of 2026, in USD million (band in brackets): %s; %s." % (cells(g["R2"], b["R2"]), cells(g["R3"], b["R3"])))
    out.append("5. Distributions in the same stress, in USD million (band in brackets): %s." % cells(g["R4"], b["R4"]))
    out.append("6. Commitments not yet called at 31 December 2026, by strategy, in USD million (each within 0.5): %s; %s in all."
               % ("; ".join("%s %s" % (k, m(v)) for k, v in g["R1"].items()), m(F["unfunded_total_usd_m"])))
    out.append("\n### %s\n" % GD.MEMO)
    out.append("7. A short memo to the Investment Committee from the Director of Private Markets: the program and why A, B and C "
               "fail, the two things in the evidence that decide it, a table of the calls and distributions by half-year, and the "
               "commitments not yet called.")
    out.append("\n## Critical Components\n")
    out.append("1. The headroom before any 2027 commitment (synthesis): **USD %s million**, against re-up calls of **USD %s million** "
               "for program %s and **USD %s million** for program C." % (m(F["headroom_before_2027_usd_m"]), m(pr[adopt]["calls_usd_m"]), adopt, m(pr["C"]["calls_usd_m"])))
    out.append("2. The 2028 calls (modeling past the record's range): **USD %s million** and **USD %s million** in the two halves, "
               "the defensive follow-ons and rescue financings adding **USD %s million** over the eight quarters." % (m(g["R3"]["H1 2028"]), m(g["R3"]["H2 2028"]), m(sup)))
    out.append("3. The first-half 2027 calls (missingness and measurement): **USD %s million**, of which **USD %s million** is the six "
               "managers' capital on their lines at 31 December, called at the clean-down." % (m(g["R2"]["H1 2027"]), m(F["line_stock_six_managers_usd_m"])))
    out.append("\n## Step-by-Step\n")
    out.append("1. Assemble the commitments: the statements less the superseded row, the custodian's fourth-quarter cash for the two "
               "late statements, released commitments out, the pending funds in full: USD %s million not yet called." % m(F["unfunded_total_usd_m"]))
    out.append("2. The reserve (USD %s million at the policy's factors), the spending (eight quarters of a quarter of FY2027's "
               "distribution, USD %s million) and the distributions at the policy's 2008-10 rates: %s." % (m(F["reserve_usd_m"]), m(F["spending_24m_usd_m"]), "; ".join("%s %s" % (h, m(g["R4"][h])) for h in H)))
    out.append("3. The line stock for the managers whose company-level file runs to 2026: the managers' investments at the endowment's "
               "share less the capital called for them, less recycled proceeds read at the audited year-ends, called in the first quarter "
               "once the stressed rate passes every manager's limit.")
    out.append("4. The six managers whose files stop after 2024 (%s): their stock cannot be read as a gap after the file ends; it is rolled "
               "from the file's last quarter on the pace fitted to the covered funds, less the investment capital the statements show "
               "them calling, and re-anchored at each audited year-end since: USD %s million. Their last audited balances would put it at "
               "USD %s million, because the lines were cleaned down at the end of 2025 and rebuilt through 2026; carried that way the "
               "headroom is USD %s million and program %s." % ("; ".join(F["six_managers"]), m(F["line_stock_six_managers_usd_m"]),
                                                                   m(F["line_stock_six_managers_audited_usd_m"]), m(fac["J2 dropped"]["headroom_before_2027_usd_m"]), fac["J2 dropped"]["program"]))
    out.append("5. The support response: on the endowment's own funds, follow-ons into companies held two years or more rise with the "
               "exit index's shortfall two quarters earlier at %s of their cost a quarter per unit, up to a shortfall of %s where the "
               "fit caps them; the stress goes further than the record. The benchmark's funds past their investment period and with "
               "commitment left to call show a second rise past %s, %s times as steep (their 2009 calls). Held flat at the plateau "
               "the headroom is USD %s million and program %s." % (m(s_["sigma"], 3), m(s_["cap"], 2), m(s_["th"], 2), m(s_["ratio"], 2),
                                                                     m(fac["J1 dropped"]["headroom_before_2027_usd_m"]), fac["J1 dropped"]["program"]))
    out.append("6. New deals at each strategy's pace on the room left with the deal market's elasticity; investment periods extended "
               "on the rule the register's agreed and current period ends show (two years more when the exit index over the two "
               "quarters before the agreed end averages below %s and the fund has invested less than %s of its commitment); pending funds' first closes slipped on the exit "
               "market; fees and recycling at each fund's and manager's own rates; a fund whose term ends inside the eight quarters "
               "calls nothing after it (policy section 3: the part not called is released) and distributes as section 7 sets out."
               % (m(F["extension_rule"]["e_star"], 1), m(F["extension_rule"]["s_star"], 2)))
    out.append("7. The test: the headroom before any 2027 commitment is USD %s million; each re-up's calls over the eight quarters "
               "(%s) give program A USD %s million, B USD %s million, C USD %s million and D USD %s million; the largest program "
               "that passes is %s." % (m(F["headroom_before_2027_usd_m"]), "; ".join("%s %s" % (k, m(v)) for k, v in F["re_up_calls_usd_m"].items()),
                                       m(pr["A"]["calls_usd_m"]), m(pr["B"]["calls_usd_m"]), m(pr["C"]["calls_usd_m"]), m(pr["D"]["calls_usd_m"]), adopt))
    rp = rt["the benchmark's 2008-10 call rates replayed on the commitments not yet called"]["program"]
    rd = rt["the pacing model recalibrated on the 2022 to 2024 exit drought"]["program"]
    word = lambda c: "no program" if c == "none" else "program %s" % c
    out.append("8. The shortcuts land elsewhere: the careful route on %s; the pacing model on the capital accounts on %s, or on %s "
               "recalibrated on the 2022 to 2024 exit drought; the benchmark's 2008-10 call rates, replayed on the commitments not yet "
               "called, on %s; each of the two judgments alone on the careful route on %s and %s."
               % (word(careful), word(ta), word(rd), word(rp), word(fac["J1 alone"]["program"]), word(fac["J2 alone"]["program"])))
    out.append("\nNo other conclusion survives the records. The stress reaches a shortfall the endowment's own funds never saw, and the "
               "funds that did see it show the calls rising again past the plateau; six managers' lines have to be rebuilt from the "
               "complete records once their detailed files stop. Each moves the program on its own, and every rival fit, slice, cap, "
               "bridge and the bootstrap over funds keep program %s the one that passes." % adopt)
    return "\n".join(out) + "\n"
