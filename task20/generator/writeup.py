"""submission.md, every figure from figures.json."""
import analysis as A
import golden as GD

def m(x, d=1):
    return format(x, ",.%df" % d)

def ql(q):
    q = int(round(q)); return "Q%d %d" % (q % 4 + 1, A.Q0 + q // 4)

def word(c):
    return "no program" if c == "none" else "program %s" % c

def andl(xs):
    xs = list(xs)
    return ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else "".join(xs)

def text(F, R):
    g = R["golden"]; b = F["bands"]; L = R["L"]
    rt = F["routes"]; fac = F["factorial"]; pr = F["programs"]; adopt = F["program"]
    H = A.HALVES
    funds = next(x for x in L["programs"] if x["code"] == adopt)["funds"] if adopt != "none" else []
    order = [p["code"] for p in sorted(L["programs"], key=lambda p: -p["total"])]
    bigger = [c for c in order if pr[c]["total_usd_m"] > pr[adopt]["total_usd_m"]]
    deferred = [x["fund"] for x in L["plan"] if x["fund"] not in funds]
    cells = lambda d, bd: "; ".join("%s %s (%s to %s)" % (h, m(d[h]), m(bd[h][0]), m(bd[h][1])) for h in d)
    careful = F["careful_route"]
    s1d, s2d = fac["S1 dropped"], fac["S2 dropped"]
    lr, vr = F["lender_rule"], F["value_response"]
    ev = F["successor_events"]
    first = [e for e in ev if e["close"] < A.qi(2027, 2)]; later = [e for e in ev if e["close"] >= A.qi(2027, 2)]
    sname = lambda e: "%s (successor %s, %s)" % (e["fund"], e["successor"], ql(e["close"]))
    rd = F["readings"]; ro = F["ruled_out"]
    out = []
    out.append("# task20: Wexmoor University's endowment, the 2027 private-fund program\n")
    out.append("## Tags\n")
    out.append("**Domain:** Quantitative Finance, Liquidity, funding & balance-sheet risk (an endowment's private-fund commitment "
               "program under its liquidity policy: capital calls in a stressed exit and credit market).")
    out.append("**Analytical objective:** Forecasting & Predictive Modeling.\n")
    out.append("## Final Recommendation\n")
    out.append("Adopt program %s (%s, USD %s million) and defer %s to 2028: before any 2027 commitment the policy's stress leaves "
               "USD %s million above the USD %s million minimum, enough for program %s's USD %s million of calls but not for "
               "program %s's USD %s million. Not program %s, which the careful reading adopts by holding every investment period "
               "to its registered end and the real-asset loans as they stand (USD %s million of headroom), nor program %s, which "
               "a reading that refinances the loans but misses the successor funds' first closes adopts (USD %s million)."
               % (adopt, andl(funds), m(F["program_total_usd_m"], 0), andl(deferred), m(F["headroom_before_2027_usd_m"]),
                  m(F["minimum_reserve_usd_m"], 0), adopt, m(pr[adopt]["calls_usd_m"]), bigger[-1], m(pr[bigger[-1]]["calls_usd_m"]),
                  careful["program"], m(careful["headroom_before_2027_usd_m"]), s1d["program"], m(s1d["headroom_before_2027_usd_m"])))
    out.append("\n## Supplementary Questions\n")
    out.append("### %s\n" % GD.XLSX)
    out.append("1. Sheet Summary opens on the program the policy lets the Committee adopt, sets out the test before any 2027 "
               "commitment (reserve, spending, calls, distributions, net cash needs, the minimum and the headroom) and each "
               "program's new commitments, calls, headroom left and result, with a chart of the headroom left; sheets By "
               "half-year, Re-ups, Unfunded, Successor closes, Asset loans, Facility balances, Policy bases and Sensitivity "
               "carry the figures below.")
    out.append("2. The program that can be adopted: %s (%s; USD %s million of new commitments); %s %s." % (
        adopt, "; ".join(funds), m(F["program_total_usd_m"], 0), andl(bigger), "fails" if len(bigger) == 1 else "fail"))
    out.append("3. The headroom above the minimum reserve before any 2027 commitment, in USD million: %s (%s to %s)." % (m(F["headroom_before_2027_usd_m"]), m(b["R5"][0]), m(b["R5"][1])))
    out.append("4. Capital calls in the policy's stress on the commitments made by the end of 2026, in USD million (band in brackets): %s." % cells(g["calls"], b["calls"]))
    out.append("5. Distributions in the same stress, in USD million (each within 0.5): %s." % "; ".join("%s %s" % (h, m(g["R4"][h])) for h in H))
    out.append("6. Commitments not yet called at 31 December 2026, by strategy, in USD million (each within 0.5): %s; %s in all."
               % ("; ".join("%s %s" % (k, m(v)) for k, v in g["R1"].items()), m(F["unfunded_total_usd_m"])))
    out.append("\n### %s\n" % GD.MEMO)
    out.append("7. A short memo to the Investment Committee from the Director of Private Markets: the program and why %s %s, the "
               "two things in the evidence that decide it (the investment periods the successor funds' first closes end, and the "
               "property and infrastructure loans that fall due in the stress), a table of the calls and distributions by "
               "half-year, and the commitments not yet called." % (andl(bigger), "fails" if len(bigger) == 1 else "fail"))
    out.append("\n## Critical Components\n")
    out.append("1. The headroom before any 2027 commitment (synthesis): **USD %s million**, against re-up calls of **USD %s million** "
               "for program %s and **USD %s million** for program %s." % (m(F["headroom_before_2027_usd_m"]), m(pr[adopt]["calls_usd_m"]), adopt,
                                                                           m(pr[bigger[-1]]["calls_usd_m"]), bigger[-1]))
    out.append("2. The refinancing calls (modeling): **%d** property and infrastructure loans fall due in 2027 and 2028 (**USD %s million** "
               "at Wexmoor's share); refinanced at the lenders' limit on the stressed rate and values they leave shortfalls the funds "
               "call, **USD %s million** over the eight quarters. Without them the headroom is **USD %s million** and program %s passes."
               % (F["loans_due_count"], m(F["loans_due_balance_usd_m"]), m(F["refinancing_calls_total_usd_m"]),
                  m(s2d["headroom_before_2027_usd_m"]), s2d["program"]))
    out.append("3. The successor closes (investigation): **%d** funds' investment periods end when their managers' next funds hold their "
               "first closes inside the eight quarters (%s), which takes **USD %s million** off their calls. Held to their registered "
               "ends the headroom is **USD %s million** and program %s." % (len(ev), "; ".join(e["fund"] for e in ev), m(F["successor_effect_usd_m"]),
                                                                             m(s1d["headroom_before_2027_usd_m"]), s1d["program"]))
    out.append("\n## Step-by-Step\n")
    out.append("1. Assemble the commitments: the statements less the superseded row, the custodian's fourth-quarter cash for the "
               "late statements, released commitments out, the pending funds in full: USD %s million not yet called." % m(F["unfunded_total_usd_m"]))
    out.append("2. The reserve (USD %s million at the policy's factors), the spending (eight quarters of a quarter of FY2027's "
               "distribution, USD %s million) and the distributions at the policy's 2008-10 rates: %s." % (m(F["reserve_usd_m"]), m(F["spending_24m_usd_m"]), "; ".join("%s %s" % (h, m(g["R4"][h])) for h in H)))
    out.append("3. The capital invested through the funds' credit facilities and not yet called, formed as policy section 8 "
               "sets out (each fund's latest audited borrowings at Wexmoor's share, plus its investments since on the managers' "
               "activity file and less the capital called for investments since, never below nil): USD %s million, counted in the "
               "first quarter. The latest audited borrowings alone show USD %s million; the facilities were drawn again through "
               "2026." % (m(F["line_stock_usd_m"]), m(F["line_stock_audited_usd_m"])))
    out.append("4. What section 8 sets, applied as written. New investments while a fund's investment period runs, the quarter "
               "it ends included: the pace of its strategy and year since first close (first and follow-on investments on the "
               "managers' activity file over the commitment not yet invested, at Wexmoor's share) on its own commitment not yet "
               "invested, USD %s million over the eight quarters. No period is extended in the stress, section 8 making no "
               "allowance for the exit market. Fees and expenses at each fund's latest statement (none on top of the benchmark's "
               "rate for a buyout, growth or venture fund past its period), and at its strategy's median quarter for a fund yet "
               "to close, USD %s million. Funds yet to hold a first close on their managers' dates. Buyout, "
               "growth and venture funds past their investment periods (%d at 31 December, worth USD %s million, and those whose "
               "periods end inside the eight quarters from the quarter after): the 31 December value times the benchmark's call "
               "rate of 2008Q3 to 2010Q2 for funds with a vintage six or more years before the quarter's year (%s, %s and %s "
               "percent of value over the eight quarters for buyout, growth and venture), USD %s million once no fund calls more "
               "than its commitment has left. That cap runs quarter by quarter: each quarter's calls come off the commitment the "
               "fund has left, and within a quarter they are counted in this order until it is used up: the facility balance, fees "
               "and expenses, the benchmark's rate, new investments, and last a maturing loan's shortfall (taking the shortfall "
               "first leaves the headroom where it is). A fund that has used its commitment up calls nothing more, its fees "
               "included, so the fees and expenses above are USD %s million before the cap. A fund whose term ends "
               "inside the eight quarters calls nothing after it."
               % (m(F["new_investments_total_usd_m"]), m(F["fees_total_usd_m"]), F["old_funds_31dec"], m(F["old_funds_value_usd_m"]),
                  m(F["old_fund_rate_8q_pct"]["BO"], 2), m(F["old_fund_rate_8q_pct"]["GE"], 2), m(F["old_fund_rate_8q_pct"]["VC"], 2),
                  m(F["old_fund_calls_total_usd_m"]), m(F["fees_before_cap_usd_m"])))
    nv = F["past_successions"]
    out.append("5. The successor closes: the register records, for every past fund whose successor closed before its agreed "
               "investment period was out, whether the period ended at the successor's first close (%d such successions). %d "
               "managers' funds always stopped there (the clause of their agreements) and %d managers' ran on (%s). For the managers "
               "with the clause, a fund's investment period ends the quarter before its successor's first close, on the manager's "
               "date as section 8 takes it: %s; %s. From then the fund stops investing, and a buyout, growth or venture fund moves "
               "to the benchmark's rate. This is where the hurried forecast goes wrong first: it holds every period to the end the "
               "register records, and calls USD %s million more."
               % (nv, len(F["clause_managers"]), len(F["no_clause_managers"]), ", ".join(F["no_clause_managers"]) or "none",
                  "; ".join(sname(e) for e in first) or "none", "; ".join(sname(e) for e in later) or "none", m(F["successor_effect_usd_m"])))
    out.append("6. The refinancing calls: the activity file's asset-loan records give each property and infrastructure asset's loan "
               "and maturity, and %d past refinancings, %d of them at a lower balance with the fund investing the difference. The "
               "lenders' limit, fitted on the %d refinancings since mid-2022 (the new balance over the asset's value, which is the "
               "fund's valuation of its holding the quarter before plus the loan replaced), is the lower of %s of value and %s over "
               "the rate plus %s points (%s of value at the stressed rate of %s percent). The assets' values (valuation plus loan) "
               "move with equities (an elasticity of %s) and with the short rate (%s per point), both a quarter late, fitted on "
               "the %d quarterly changes in value between two valuations both sixteen quarters or more after the asset's loan "
               "was first drawn (its four-year plan behind it), in quarters the loan did not change; "
               "the lag is the record's own, the same fit with no lag or two quarters late leaving the changes largely "
               "unexplained. So a loan maturing in a quarter is refinanced on the asset's 31 December value moved by equities and "
               "the short rate from 30 September 2026 to the end of the quarter before. Of the loans "
               "alive at 31 December, %d fall due in the eight quarters (USD %s million at Wexmoor's share); at the stressed rate "
               "and values the lenders grant USD %s million less than the balances, and the funds call USD %s million of it within "
               "their commitments (%s). This is the second place the hurried forecast goes wrong: it carries the loans as they stand."
               % (F["refinancings_in_record"], F["refinancings_short_in_record"], lr["n"], m(lr["cap_post"], 3), m(lr["kappa"], 3), m(lr["spread"], 2),
                  m(F["lender_limit_stressed"], 3), m(F["stressed_rate_pct"], 2), m(vr["beta"], 2), m(vr["c"], 3), vr["n"], F["loans_due_count"],
                  m(F["loans_due_balance_usd_m"]), m(F["loans_due_gap_usd_m"]), m(F["refinancing_calls_total_usd_m"]),
                  "; ".join("%s %s" % (h, m(v)) for h, v in F["refinancing_calls_by_half_usd_m"].items())))
    out.append("7. The test: the headroom before any 2027 commitment is USD %s million; each re-up's calls over the eight quarters "
               "(%s) give program A USD %s million, B USD %s million, C USD %s million and D USD %s million; the largest program "
               "that passes is %s, with USD %s million to spare, and program %s falls USD %s million short."
               % (m(F["headroom_before_2027_usd_m"]), "; ".join("%s %s" % (k, m(v)) for k, v in F["re_up_calls_usd_m"].items()),
                  m(pr["A"]["calls_usd_m"]), m(pr["B"]["calls_usd_m"]), m(pr["C"]["calls_usd_m"]), m(pr["D"]["calls_usd_m"]), adopt,
                  m(F["margin_below_usd_m"]), bigger[-1], m(F["margin_above_usd_m"])))
    ta = rt["the textbook pacing model on the capital accounts"]["program"]
    rp = rt["the benchmark's 2008-10 call rates replayed on the commitments not yet called"]["program"]
    rdr = rt["the pacing model recalibrated on the 2022 to 2024 exit drought"]["program"]
    an = rt["the same benchmark rate for every strategy on the careful route"]["program"]
    cur = rt["the loans refinanced at the lenders' terms and the values of 31 December 2026"]["program"]
    vf = rt["the loans refinanced at the stressed rate on the values of 31 December 2026"]["program"]
    out.append("8. The shortcuts land elsewhere: the careful route (periods to their registered ends, loans as they stand) on %s; "
               "the successor closes found but the loans carried on %s; the loans refinanced but the periods held on %s; the loans "
               "refinanced at 31 December's terms on %s, and at the stressed rate on 31 December's values on %s; section 8's "
               "benchmark rate carried over to the property, infrastructure and credit funds on %s; the pacing model on the capital "
               "accounts on %s as it stands and on %s recalibrated on the 2022 to 2024 exit drought; the benchmark's 2008-10 call "
               "rates replayed on the commitments not yet called on %s."
               % (word(careful["program"]), word(fac["S1 alone"]["program"]), word(fac["S2 alone"]["program"]), word(cur), word(vf), word(an),
                  word(ta), word(rdr), word(rp)))
    y0, y1 = F["benchmark_vintage_years"] - 1, F["benchmark_vintage_years"] + 1
    k5 = "section 8's benchmark funds at a vintage %d or more years before the quarter's year" % y0
    k7 = "section 8's benchmark funds at a vintage %d or more years before the quarter's year" % y1
    kc = "the pace over the commitment not yet called"
    kg = "the facility balances as the investments less the capital called for them, the audited borrowings set aside"
    kf = "the funds' own fees and expenses added on top of section 8's benchmark rate"
    fam = F["family"]; fv = [v["headroom_before_2027_usd_m"] for v in fam.values()] + [F["headroom_before_2027_usd_m"]]
    out.append("\nNo other conclusion survives the records. The two judgments pull the headroom in opposite directions, so each "
               "alone lands on a wrong program: the successor closes take calls out and the refinancing shortfalls put more in, "
               "and only both together leave program %s passing and program %s failing. What the policy leaves to the evidence "
               "moves the headroom only between USD %s and %s million across every rival fit (the lenders' limit, the assets' "
               "values on every valuation or on the settled ones, the order a fund's calls meet its commitment, investment periods "
               "extended as past weak exit markets extended them), against USD %s million of room "
               "below and USD %s million above. The bases section 8 files are not close calls either, each reading its sentences "
               "rule out leaving program %s: the benchmark's funds a year younger or older than it says (USD %s or %s million of "
               "headroom), the pace over the commitment not yet called (USD %s million), the facility balances as the investments "
               "less the capital called for them with the audited borrowings set aside (USD %s million), and the funds' own fees "
               "on top of the benchmark's rate (USD %s million)."
               % (adopt, bigger[-1], m(min(fv)), m(max(fv)), m(F["margin_below_usd_m"]), m(F["margin_above_usd_m"]), adopt,
                  m(rd[k5]["headroom_before_2027_usd_m"]), m(rd[k7]["headroom_before_2027_usd_m"]), m(rd[kc]["headroom_before_2027_usd_m"]),
                  m(rd[kg]["headroom_before_2027_usd_m"]), m(rd[kf]["headroom_before_2027_usd_m"])))
    return "\n".join(out) + "\n"
