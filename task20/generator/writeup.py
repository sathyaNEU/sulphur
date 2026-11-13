"""submission.md, every figure from figures.json."""
import analysis as A
import golden as GD

def m(x, d=1):
    return format(x, ",.%df" % d)

def ql(q):
    q = int(round(q)); return "Q%d %d" % (q % 4 + 1, A.Q0 + q // 4)

def half(q):
    q = int(q); return "%s %d" % ("first half of" if q % 4 < 2 else "second half of", A.Q0 + q // 4)

def word(c):
    return "no program" if c == "none" else "program %s" % c

def text(F, R):
    g = R["golden"]; b = F["bands"]; L = R["L"]
    rt = F["routes"]; fac = F["factorial"]; pr = F["programs"]; adopt = F["program"]
    H = A.HALVES
    funds = next(x for x in L["programs"] if x["code"] == adopt)["funds"] if adopt != "none" else []
    order = [p["code"] for p in sorted(L["programs"], key=lambda p: -p["total"])]
    bigger = [c for c in order if pr[c]["total_usd_m"] > pr[adopt]["total_usd_m"]]
    smaller = [c for c in order if pr[c]["total_usd_m"] < pr[adopt]["total_usd_m"]]
    deferred = [x["fund"] for x in L["plan"] if x["fund"] not in funds]
    cells = lambda d, bd: "; ".join("%s %s (%s to %s)" % (h, m(d[h]), m(bd[h][0]), m(bd[h][1])) for h in d)
    careful = F["careful_route"]
    s1d, s2d = fac["S1 dropped"], fac["S2 dropped"]
    lr, vr = F["lender_rule"], F["value_response"]
    ev = F["successor_events"]
    first = [e for e in ev if e["close"] < A.qi(2027, 3)]; later = [e for e in ev if e["close"] >= A.qi(2027, 3)]
    sname = lambda e: "%s (successor %s, %s)" % (e["fund"], e["successor"], ql(e["close"]) if abs(e["close"] - round(e["close"])) < 0.15 else half(e["close"]))
    out = []
    out.append("# task20: Wexmoor University's endowment, the 2027 private-fund program\n")
    out.append("## Tags\n")
    out.append("**Domain:** Quantitative Finance, Liquidity, funding & balance-sheet risk (an endowment's private-fund commitment "
               "program under its liquidity policy: capital calls in a stressed exit and credit market).")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## Final Recommendation\n")
    flist = ", ".join(funds[:-1]) + " and " + funds[-1] if len(funds) > 1 else "".join(funds)
    out.append("Adopt program %s (%s, USD %s million) and defer %s to 2028: before any 2027 commitment the policy's stress leaves "
               "USD %s million above the USD %s million minimum, enough for program %s's USD %s million of calls but not for "
               "program %s's USD %s million. Not program %s, which the careful reading adopts by holding every investment period "
               "to its registered end and the real-asset loans as they stand (USD %s million of headroom), nor program %s, which "
               "a reading that refinances the loans but misses the successor funds' first closes adopts (USD %s million)."
               % (adopt, flist, m(F["program_total_usd_m"], 0), " and ".join(deferred), m(F["headroom_before_2027_usd_m"]),
                  m(F["minimum_reserve_usd_m"], 0), adopt, m(pr[adopt]["calls_usd_m"]), bigger[-1], m(pr[bigger[-1]]["calls_usd_m"]),
                  careful["program"], m(careful["headroom_before_2027_usd_m"]), s1d["program"], m(s1d["headroom_before_2027_usd_m"])))
    out.append("\n## Supplementary Questions\n")
    out.append("### %s\n" % GD.XLSX)
    out.append("1. Sheet Summary opens on the program the policy lets the Committee adopt, sets out the test before any 2027 "
               "commitment (reserve, spending, calls, distributions, net cash needs, the minimum and the headroom) and each "
               "program's new commitments, calls, headroom left and result, with a chart of the headroom left; sheets By "
               "half-year, Re-ups, Unfunded, Successor closes, Asset loans, Credit-line stock, Support response and Sensitivity "
               "carry the figures below.")
    out.append("2. The program that can be adopted: %s (%s; USD %s million of new commitments); %s %s." % (
        adopt, "; ".join(funds), m(F["program_total_usd_m"], 0), " and ".join(bigger), "fails" if len(bigger) == 1 else "fail"))
    out.append("3. The headroom above the minimum reserve before any 2027 commitment, in USD million: %s (%s to %s)." % (m(F["headroom_before_2027_usd_m"]), m(b["R5"][0]), m(b["R5"][1])))
    out.append("4. Capital calls in the policy's stress on the commitments made by the end of 2026, in USD million (band in brackets): %s; %s." % (cells(g["R2"], b["R2"]), cells(g["R3"], b["R3"])))
    out.append("5. Distributions in the same stress, in USD million (each within 0.5): %s." % "; ".join("%s %s" % (h, m(g["R4"][h])) for h in H))
    out.append("6. Commitments not yet called at 31 December 2026, by strategy, in USD million (each within 0.5): %s; %s in all."
               % ("; ".join("%s %s" % (k, m(v)) for k, v in g["R1"].items()), m(F["unfunded_total_usd_m"])))
    out.append("\n### %s\n" % GD.MEMO)
    out.append("7. A short memo to the Investment Committee from the Director of Private Markets: the program and why %s %s, the "
               "two things in the evidence that decide it (the investment periods the successor funds' first closes end, and the "
               "property and infrastructure loans that fall due in the stress), a table of the calls and distributions by "
               "half-year, and the commitments not yet called." % (" and ".join(bigger), "fails" if len(bigger) == 1 else "fail"))
    out.append("\n## Critical Components\n")
    out.append("1. The headroom before any 2027 commitment (synthesis): **USD %s million**, against re-up calls of **USD %s million** "
               "for program %s and **USD %s million** for program %s." % (m(F["headroom_before_2027_usd_m"]), m(pr[adopt]["calls_usd_m"]), adopt,
                                                                           m(pr[bigger[-1]]["calls_usd_m"]), bigger[-1]))
    out.append("2. The refinancing calls (modeling): **%d** property and infrastructure loans fall due in 2027 and 2028 (**USD %s million** "
               "at Wexmoor's share); refinanced at the lenders' limit on the stressed rate and values they leave gaps the funds call, "
               "**USD %s million** over the eight quarters. Without them the headroom is **USD %s million** and program %s passes."
               % (F["loans_due_count"], m(F["loans_due_balance_usd_m"]), m(F["refinancing_calls_total_usd_m"]),
                  m(s2d["headroom_before_2027_usd_m"]), s2d["program"]))
    out.append("3. The successor closes (investigation): **%d** funds' investment periods end when their managers' next funds hold their "
               "first closes inside the eight quarters (%s), which takes **USD %s million** off their calls. Held to their registered "
               "ends the headroom is **USD %s million** and program %s." % (len(ev), "; ".join(e["fund"] for e in ev), m(F["successor_effect_usd_m"]),
                                                                             m(s1d["headroom_before_2027_usd_m"]), s1d["program"]))
    out.append("\n## Step-by-Step\n")
    out.append("1. Assemble the commitments: the statements less the superseded row, the custodian's fourth-quarter cash for the two "
               "late statements, released commitments out, the pending funds in full: USD %s million not yet called." % m(F["unfunded_total_usd_m"]))
    out.append("2. The reserve (USD %s million at the policy's factors), the spending (eight quarters of a quarter of FY2027's "
               "distribution, USD %s million) and the distributions at the policy's 2008-10 rates: %s." % (m(F["reserve_usd_m"]), m(F["spending_24m_usd_m"]), "; ".join("%s %s" % (h, m(g["R4"][h])) for h in H)))
    out.append("3. The capital invested on credit lines and not yet called, called in the first quarter once the stressed rate passes "
               "every manager's limit: USD %s million, of which USD %s million for the six managers whose company-level files stop "
               "after 2024, estimated to 31 December from the capital accounts and the audits as policy section 8 sets out."
               % (m(F["line_stock_usd_m"]), m(F["line_stock_six_managers_usd_m"])))
    s_ = F["support"]
    out.append("4. The calls on companies already held: defensive follow-ons on the endowment's own funds up to a shortfall of %s, "
               "and past the shortfall the endowment's record reaches, rescue financings read off the benchmark's funds past their "
               "investment period from 2008 to 2010 (section 8): USD %s million over the eight quarters."
               % (m(s_["cap"], 2), m(F["support_total_usd_m"])))
    out.append("5. New investment at each strategy's pace on the room left, with no allowance for a slower deal market (section 8); "
               "investment periods extended on the rule the register's agreed and current ends show; pending funds' first closes "
               "slipped on the exit market; fees and recycling at each fund's and manager's own rates; a fund whose term ends inside "
               "the eight quarters calls nothing after it.")
    nv = sum(v[1] for v in F["clause_votes"].values())
    out.append("6. The successor closes: the register records, for every past fund whose successor closed before its agreed "
               "investment period was out, whether the period ended at the successor's first close (%d such successions). %d "
               "managers' funds always stopped there (the clause of their agreements) and %d managers' ran on (%s). For the managers "
               "with the clause, a fund's investment period ends at its successor's first close, dated on the same slip as the "
               "pending funds': %s close in the first quarter of 2027 and %s later in the window. This is where the hurried forecast "
               "goes wrong first: it holds every period to the end the register records, and calls USD %s million more."
               % (nv, len(F["clause_managers"]), len(F["no_clause_managers"]), ", ".join(F["no_clause_managers"]) or "none",
                  "; ".join(sname(e) for e in first) or "none", "; ".join(sname(e) for e in later) or "none", m(F["successor_effect_usd_m"])))
    out.append("7. The refinancing calls: the activity file's asset-loan records give each property and infrastructure asset's loan "
               "and maturity. The lenders' limit, fitted on the %d refinancings since mid-2022, is the lower of %s of value and %s "
               "over the rate plus %s points; the assets' values move with equities a quarter late (an elasticity of %s) and with "
               "the short rate (%s per point), fitted on their own %d quarterly valuations. Of the loans alive at 31 December, %d fall "
               "due in the eight quarters (USD %s "
               "million at Wexmoor's share); at the stressed rate and values the lenders grant USD %s million less than the "
               "balances, and the funds call USD %s million of it within their commitments (%s). This is the second place the hurried "
               "forecast goes wrong: it carries the loans as they stand."
               % (lr["n"], m(lr["cap_post"], 3), m(lr["kappa"], 3), m(lr["spread"], 2), m(vr["beta"], 2), m(vr["c"], 3), vr["n"], F["loans_due_count"],
                  m(F["loans_due_balance_usd_m"]), m(F["loans_due_gap_usd_m"]), m(F["refinancing_calls_total_usd_m"]),
                  "; ".join("%s %s" % (h, m(v)) for h, v in F["refinancing_calls_by_half_usd_m"].items())))
    out.append("8. The test: the headroom before any 2027 commitment is USD %s million; each re-up's calls over the eight quarters "
               "(%s) give program A USD %s million, B USD %s million, C USD %s million and D USD %s million; the largest program "
               "that passes is %s." % (m(F["headroom_before_2027_usd_m"]), "; ".join("%s %s" % (k, m(v)) for k, v in F["re_up_calls_usd_m"].items()),
                                       m(pr["A"]["calls_usd_m"]), m(pr["B"]["calls_usd_m"]), m(pr["C"]["calls_usd_m"]), m(pr["D"]["calls_usd_m"]), adopt))
    ta = rt["the textbook pacing model on the capital accounts"]["program"]
    rp = rt["the benchmark's 2008-10 call rates replayed on the commitments not yet called"]["program"]
    rd = rt["the pacing model recalibrated on the 2022 to 2024 exit drought"]["program"]
    out.append("9. The shortcuts land elsewhere: the careful route (periods to their registered ends, loans as they stand) on %s; "
               "the successor closes found but the loans carried on %s; the loans refinanced but the periods held on %s; the loans "
               "refinanced at 31 December's terms on %s; the pacing model on the capital accounts on %s as it stands and on %s "
               "recalibrated on the 2022 to 2024 exit drought; the benchmark's 2008-10 call rates replayed on the commitments not yet "
               "called on %s." % (word(careful["program"]), word(fac["S1 alone"]["program"]), word(fac["S2 alone"]["program"]),
                                  word(rt["the loans refinanced at the lenders' terms and the values of 31 December 2026"]["program"]), word(ta), word(rd), word(rp)))
    out.append("\nNo other conclusion survives the records. The two judgments pull the headroom in opposite directions, so each "
               "alone lands on a wrong program: the successor closes take calls out and the refinancing gaps put more in, and only "
               "both together leave program %s passing and program %s failing. Every rival fit, slice and cap, the lenders' and the "
               "values' alternative fits, the bootstrap over funds and the world's own replay keep program %s the largest that passes." % (adopt, bigger[-1], adopt))
    return "\n".join(out) + "\n"
