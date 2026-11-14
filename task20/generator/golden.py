"""The golden deliverables: the Office of Investments' workbook testing Corrigan Hart's 2027 programs, and the memo
to the Investment Committee."""
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, Mm
from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.marker import DataPoint
from openpyxl.styles import Alignment, Font
import analysis as A

XLSX = "wexmoor_2027_program_test.xlsx"
MEMO = "commitment_program_2027_memo.docx"
QL = lambda q: "Q%d %d" % (q % 4 + 1, A.Q0 + q // 4)


USD = "#,##0.0"
WHOLE = "#,##0"
TIDY = lambda t: t[:1].upper() + t[1:]
NUMW = {1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five", 6: "Six", 7: "Seven", 8: "Eight", 9: "Nine"}
# the other forecasts on the Sensitivity sheet, in the office's own words
SAY = {"the careful route: every investment period to its registered end, the real-asset loans rolled over as they stand":
           "every investment period to its registered end, the real-asset loans rolled over as they stand",
       "the same benchmark rate for every strategy on the careful route":
           "section 8's benchmark rate for every strategy's funds past their periods, the periods to their registered ends and the loans as they stand",
       "the textbook pacing model on the capital accounts": "calls at each strategy's past rate on the commitment not yet called, from the capital accounts",
       "the pacing model recalibrated on the 2022 to 2024 exit drought": "the same rates taken from 2022 to 2024 alone"}


def _fmt(ws, cols, fmt, first=2, last=None):
    for row in ws.iter_rows(min_row=first, max_row=last or ws.max_row):
        for c in row:
            if c.column_letter in cols and isinstance(c.value, (int, float)):
                c.number_format = fmt


def workbook(F, R, path):
    g = R["golden"]; bold = Font(bold=True); L = R["L"]
    wb = Workbook(); ws = wb.active; ws.title = "Summary"
    adopt = F["program"]
    fails = [c for c in sorted(F["programs"]) if not F["programs"][c]["passes"]]
    fail = ", ".join(fails[:-1]) + " and " + fails[-1] if len(fails) > 1 else "".join(fails)
    ws.append(["Program %s is the largest that passes the 2027 liquidity test; %s %s" % (adopt, fail, "fails" if len(fails) == 1 else "fail")])
    ws["A1"].font = Font(bold=True, size=13)
    ws.append(["Position at 31 December 2026; the policy's stress over the eight quarters from 1 January 2027; USD million at Wexmoor's share"])
    ws["A2"].font = Font(italic=True, size=9)
    ws.append([])
    ws.append(["Program the policy lets the Committee adopt", F["program"]])
    ws.append(["Its new commitments (USD m)", F["program_total_usd_m"]]); ws.cell(ws.max_row, 2).number_format = WHOLE
    ws.append([])
    ws.append(["The test before any 2027 commitment", "USD m"])
    for c in ws[ws.max_row]: c.font = bold
    tot = lambda d: round(sum(d.values()), 1)
    calls_tot = round(tot(g["R2"]) + tot(g["R3"]), 1)
    for lbl, v in (("Liquid reserve at the policy's factors", round(F["reserve_usd_m"], 1)), ("Spending distribution", F["spending_24m_usd_m"]),
                   ("Calls on the commitments made by the end of 2026", calls_tot), ("Distributions", tot(g["R4"])),
                   ("Net cash needs", F["net_needs_before_2027_usd_m"]), ("Minimum reserve set for 2027", F["minimum_reserve_usd_m"]),
                   ("Headroom above the minimum before any 2027 commitment", F["headroom_before_2027_usd_m"])):
        ws.append([lbl, v]); ws.cell(ws.max_row, 2).number_format = USD
    ws.cell(ws.max_row, 1).font = bold; ws.cell(ws.max_row, 2).font = bold
    ws.append([])
    ws.append(["Program", "Funds", "New commitments (USD m)", "Their calls over the eight quarters (USD m)", "Headroom left (USD m)", "Passes"])
    hdr_row = ws.max_row
    for c in ws[hdr_row]: c.font = bold
    for pr in L["programs"]:
        p = F["programs"][pr["code"]]
        ws.append([pr["code"], "; ".join(pr["funds"]), p["total_usd_m"], p["calls_usd_m"], p["headroom_usd_m"], "Yes" if p["passes"] else "No"])
        ws.cell(ws.max_row, 3).number_format = WHOLE
        for k in (4, 5): ws.cell(ws.max_row, k).number_format = USD
        ws.cell(ws.max_row, 6).alignment = Alignment(horizontal="center")
    ch = BarChart(); ch.type = "bar"; ch.style = 10
    ch.title = "Program %s is the largest that keeps the minimum reserve" % adopt
    n0 = hdr_row + 1
    ch.add_data(Reference(ws, min_col=5, min_row=hdr_row, max_row=ws.max_row), titles_from_data=True)
    ch.set_categories(Reference(ws, min_col=1, min_row=n0, max_row=ws.max_row))
    ch.x_axis.title = "Program"; ch.y_axis.title = "Headroom left, USD million"; ch.y_axis.numFmt = "#,##0"
    ch.legend = None; ch.height, ch.width = 7.5, 15
    ser = ch.series[0]; ser.graphicalProperties.solidFill = "A6A6A6"; ser.graphicalProperties.line.solidFill = "A6A6A6"
    for i, pr in enumerate(L["programs"]):
        if pr["code"] == adopt:
            pt = DataPoint(idx=i); pt.graphicalProperties.solidFill = "1F6E43"; pt.graphicalProperties.line.solidFill = "1F6E43"
            ser.dPt.append(pt)
    ws.add_chart(ch, "H4")
    ws.column_dimensions["A"].width = 54; ws.column_dimensions["B"].width = 66
    for col, w in zip("CDEF", (16, 22, 16, 9)): ws.column_dimensions[col].width = w
    ws.print_area = "A1:F%d" % ws.max_row
    # by half-year
    h = wb.create_sheet("By half-year")
    h.append(["USD m", *A.HALVES, "Eight quarters"])
    for c in h[1]: c.font = bold
    def line(lbl, d):
        h.append([lbl] + [d[k] for k in A.HALVES] + [round(sum(d.values()), 1)])
    calls = {**g["R2"], **g["R3"]}
    line("Calls on the commitments made by the end of 2026", calls)
    line("   funds that have held a first close", g["closed"])
    line("   funds yet to hold one", g["pending"])
    line("   of which facility balances called", {hh: (F["line_stock_usd_m"] if hh == A.HALVES[0] else 0.0) for hh in A.HALVES})
    line("   of which new investments at the pace of section 8", g["new"])
    line("   of which fees and fund expenses", g["fees"])
    line("   of which buyout, growth and venture funds past their periods, at the benchmark's rate", g["old"])
    line("   of which property and infrastructure loans refinanced short of their balance", g["refi"])
    line("Distributions, the policy's 2008-10 rates", g["R4"])
    _fmt(h, "BCDEF", USD); h.freeze_panes = "B2"
    h.column_dimensions["A"].width = 78
    for col in "BCDEF": h.column_dimensions[col].width = 13
    # the re-ups
    p = wb.create_sheet("Re-ups")
    p.append(["Fund", "Strategy", "Proposed commitment (USD m)", "First close expected", "Calls over the eight quarters if committed (USD m)"])
    for c in p[1]: c.font = bold
    for x in L["plan"]:
        p.append([x["fund"], {v: k for k, v in A.STRATS.items()}[x["st"]], x["C"], QL(x["exp_fc"]), F["re_up_calls_usd_m"][x["fund"]]])
    _fmt(p, "C", WHOLE); _fmt(p, "E", USD); p.freeze_panes = "B2"
    for col, w in zip("ABCDE", (24, 16, 16, 12, 22)): p.column_dimensions[col].width = w
    for c in p[1]: c.alignment = Alignment(wrap_text=True, vertical="top")
    # unfunded
    u = wb.create_sheet("Unfunded")
    u.append(["Strategy", "Commitments not yet called at 31 Dec 2026 (USD m)"])
    for c in u[1]: c.font = bold
    for s_ in A.STRAT_ORDER: u.append([s_, g["R1"][s_]])
    u.append(["Total", F["unfunded_total_usd_m"]])
    for c in u[u.max_row]: c.font = bold
    _fmt(u, "B", USD); u.freeze_panes = "A2"
    u.column_dimensions["A"].width = 18; u.column_dimensions["B"].width = 24
    u["B1"].alignment = Alignment(wrap_text=True, vertical="top")
    # the successor closes
    sc = wb.create_sheet("Successor closes")
    sc.append(["Fund", "Manager", "Investment period ends (register)", "Successor fund", "Successor's first close (manager's date)",
               "Last quarter of new investments"])
    for c in sc[1]: c.font = bold; c.alignment = Alignment(wrap_text=True, vertical="top")
    for e in F["successor_events"]:
        r = L["reg"][e["fid"]]
        ie = r["Investment period ends"]; ie = ie.date() if hasattr(ie, "date") else ie
        k = int(round(e["close"]))
        sc.append([e["fund"], r["Manager"], ie.strftime("%d %B %Y").lstrip("0"), e["successor"], QL(k), QL(k - 1)])
    sc.append([])
    sc.append(["Managers whose past funds' investment periods ended at the successor's first close", "; ".join(F["clause_managers"])])
    sc.append(["Managers whose past funds' periods ran on past the successor's first close", "; ".join(F["no_clause_managers"]) or "none"])
    sc.append(["Effect on the headroom before any 2027 commitment (USD m)", F["successor_effect_usd_m"]])
    sc.cell(sc.max_row, 2).number_format = USD
    for col, w in zip("ABCDEF", (34, 30, 18, 28, 18, 18)): sc.column_dimensions[col].width = w
    sc.freeze_panes = "B2"
    # the asset loans
    al = wb.create_sheet("Asset loans")
    al.append(["Fund", "Asset", "Loan matures", "Loan balance (USD m)", "Asset value 31 Dec 2026 (USD m)", "Asset value at maturity in the stress (USD m)",
               "Lenders' limit then (share of value)", "Short of the balance (USD m)"])
    for c in al[1]: c.font = bold; c.alignment = Alignment(wrap_text=True, vertical="top")
    for x in sorted(F["loans_due"], key=lambda x: (x["due"], x["fund"], x["asset"])):
        al.append([x["fund"], x["asset"], QL(x["due"]), x["D"], x["P26"], x["P"], x["ltv"], x["gap"]])
        for k in (4, 5, 6, 8): al.cell(al.max_row, k).number_format = USD
        al.cell(al.max_row, 7).number_format = "0.0%"
    al.append(["Total", "", "", F["loans_due_balance_usd_m"], "", "", "", F["loans_due_gap_usd_m"]])
    for c in al[al.max_row]: c.font = bold
    for k in (4, 8): al.cell(al.max_row, k).number_format = USD
    lr, vr = F["lender_rule"], F["value_response"]
    al.append([])
    al.append(["Called by the funds within their commitments, by half-year (USD m)"] + [F["refinancing_calls_by_half_usd_m"][h] for h in A.HALVES])
    for k in range(2, 6): al.cell(al.max_row, k).number_format = USD
    al.append(["Lenders' limit fitted on the refinancings since mid-2022 (%d): the lower of a cap and kappa over the rate plus a spread" % lr["n"],
               "cap %.3f" % lr["cap_post"], "kappa %.3f" % lr["kappa"], "spread %.2f" % lr["spread"], "at %.2f%%: %.3f" % (F["stressed_rate_pct"], F["lender_limit_stressed"])])
    al.append(["Refinancings in the activity file since 2013, and those at a lower balance with the fund investing the difference",
               F["refinancings_in_record"], F["refinancings_short_in_record"]])
    al.append(["Asset values on their own valuations (%d quarters): equities a quarter late, the short rate" % vr["n"], "beta %.2f" % vr["beta"], "c %.3f" % vr["c"]])
    al.append([])
    al.append(["Past refinancings the lenders' limit is read from", "Asset", "Quarter", "Loan replaced (USD m)", "New loan (USD m)",
               "Asset value then: valuation the quarter before plus the loan replaced (USD m)", "New loan over value", "Short rate (%)",
               "Fitted limit at that rate", "In the fit (since mid-2022)"])
    for c in al[al.max_row]: c.font = bold; c.alignment = Alignment(wrap_text=True, vertical="top")
    for x in A.refinancing_table(L, R["fit"]):
        al.append([L["reg"][x["fid"]]["Fund"], x["co"], QL(x["q"]), round(x["old"], 2), round(x["new"], 2), round(x["value"], 2), round(x["ltv"], 4),
                   round(x["rate"], 2), round(x["limit"], 4), "yes" if x["fitted"] else "no"])
        for k in (4, 5, 6): al.cell(al.max_row, k).number_format = USD
        for k in (7, 9): al.cell(al.max_row, k).number_format = "0.0%"
    for col, w in zip("ABCDEFGHIJ", (34, 18, 12, 14, 16, 18, 16, 16, 12, 12)): al.column_dimensions[col].width = w
    al.freeze_panes = "B2"; al.auto_filter.ref = "A1:H%d" % (len(F["loans_due"]) + 1)
    # the facility balances
    ls = wb.create_sheet("Facility balances")
    ls.append(["Fund ID", "Fund", "Manager", "Latest audited year-end", "Borrowings on it (USD m)", "Investments since (USD m)",
               "Called for investments since (USD m)", "Invested through the credit facility, not yet called, 31 Dec 2026 (USD m)"])
    for c in ls[1]: c.font = bold; c.alignment = Alignment(wrap_text=True, vertical="top")
    ft = A.facility_table(L, R["per"])
    for fid, v in sorted(R["stock"].items(), key=lambda kv: -kv[1]):
        r = L["reg"][fid]
        if r["Status"] == "liquidated" or v < 0.05: continue
        x = ft[fid]
        ls.append([fid, r["Fund"], r["Manager"], ("FY%d" % (A.Q0 + x["audit"] // 4)) if x["audit"] is not None else "none yet",
                   round(x["borrowings"], 1), round(x["invested_since"], 1), round(x["called_since"], 1), round(v, 1)])
    ls.append(["Total", "", "", "", "", "", "", F["line_stock_usd_m"]])
    for c in ls[ls.max_row]: c.font = bold
    ls.append([])
    ls.append(["Basis (policy section 8): the borrowings on each fund's latest audited balance sheet, plus its investments since and less the "
               "capital called for investments since, at Wexmoor's share and never below nil; no allowance for proceeds reinvested since."])
    ls.append(["Latest audited borrowings, as they stood at each fund's last year-end (USD m)", "", "", "", "", "", "", F["line_stock_audited_usd_m"]])
    _fmt(ls, "EFGH", USD); ls.freeze_panes = "B2"
    for col, w in zip("ABCDEFGH", (11, 30, 28, 14, 14, 14, 16, 24)): ls.column_dimensions[col].width = w
    # the bases section 8 sets
    pb = wb.create_sheet("Policy bases")
    pb.append(["Pace of new investments (section 8): investments, first and follow-on, over the commitment not yet invested, percent a quarter"])
    pb["A1"].font = bold
    years = sorted({a_ for (st, a_) in R["fit"]["pace"]})
    pb.append(["Strategy"] + ["Year %d" % (a_ + 1) for a_ in years] + ["Fund-quarters"])
    for c in pb[pb.max_row]: c.font = bold
    inv_s = {v: k for k, v in A.STRATS.items()}
    for s_ in A.STRAT_ORDER:
        st = A.STRATS[s_]
        pb.append([s_] + [round(100 * R["fit"]["pace"][(st, a_)], 2) if (st, a_) in R["fit"]["pace"] else None for a_ in years]
                  + [sum(n for (s2, a_), n in R["fit"]["pace_n"].items() if s2 == st)])
        for k in range(2, 2 + len(years)): pb.cell(pb.max_row, k).number_format = "0.00"
    pb.append([])
    pb.append(["Benchmark call rate for funds past their investment periods (section 8): contributions of funds with a vintage %d or more years "
               "before, over their value a quarter earlier, percent" % F["benchmark_vintage_years"]])
    pb[pb.max_row][0].font = bold
    pb.append(["Strategy"] + [QL(A.qi(2008, 3) + k) for k in range(8)] + ["Eight quarters"])
    for c in pb[pb.max_row]: c.font = bold
    for st in A.EQUITY:
        pb.append([inv_s[st]] + F["old_fund_rates_pct"][st] + [F["old_fund_rate_8q_pct"][st]])
        for k in range(2, 11): pb.cell(pb.max_row, k).number_format = "0.00"
    pb.append([])
    pb.append(["Buyout, growth and venture funds past their investment periods at 31 December 2026", F["old_funds_31dec"]])
    pb.append(["Their value at 31 December 2026 (USD m)", F["old_funds_value_usd_m"]]); pb.cell(pb.max_row, 2).number_format = USD
    pb.append(["Their calls and those of the funds whose periods end in the stress, eight quarters (USD m)", F["old_fund_calls_total_usd_m"]]); pb.cell(pb.max_row, 2).number_format = USD
    pb.append(["Funds yet to hold a first close, on their managers' dates"] + ["%s %s" % (x["fund"], QL(x["close"])) for x in F["pending_funds"]])
    pb.append([])
    pb.append(["Fee and expenses of a fund yet to close (section 8): the median quarter of the strategy's funds in their investment periods, "
               "percent of commitment a quarter"])
    pb[pb.max_row][0].font = bold
    pb.append(["Strategy", "Management fee", "Fund expenses"])
    for c in pb[pb.max_row]: c.font = bold
    for s_ in A.STRAT_ORDER:
        st = A.STRATS[s_]
        if st in F["fee_rate_pct"]:
            pb.append([s_, F["fee_rate_pct"][st], F["expense_rate_pct"][st]])
            for k in (2, 3): pb.cell(pb.max_row, k).number_format = "0.000"
    pb.append(["Every other fund: the fee and expenses of its latest quarterly statement; a buyout, growth or venture fund past its investment "
               "period calls the benchmark's rate alone. Eight quarters (USD m)", F["fees_total_usd_m"]]); pb.cell(pb.max_row, 2).number_format = USD
    pb.column_dimensions["A"].width = 86
    for col in "BCDEFGHIJK": pb.column_dimensions[col].width = 12
    # sensitivity
    se = wb.create_sheet("Sensitivity")
    se.append(["Method or input", "Program", "Headroom before 2027 (USD m)"])
    for c in se[1]: c.font = bold
    se.append(["This workbook", F["program"], F["headroom_before_2027_usd_m"]])
    for n, v in F["family"].items(): se.append([TIDY(n), v["program"], v["headroom_before_2027_usd_m"]])
    se.append([])
    se.append(["Section 8's bases read another way", "Program", "Headroom before 2027 (USD m)"])
    for c in se[se.max_row]: c.font = bold
    for n, v in F["readings"].items(): se.append([TIDY(n), v["program"], v["headroom_before_2027_usd_m"]])
    se.append([])
    se.append(["Other ways of forecasting the calls", "Program", "Headroom before 2027 (USD m)"])
    for c in se[se.max_row]: c.font = bold
    for n, v in list(F["routes"].items())[1:]: se.append([TIDY(SAY.get(n, n)), v["program"], v["headroom_before_2027_usd_m"]])
    se.append([])
    se.append(["Bootstrap over funds, 5th and 95th percentiles of the headroom (USD m)", "5th", "95th"])
    for c in se[se.max_row]: c.font = bold
    for k, v in F["bootstrap_p5_p95"].items(): se.append([TIDY(k), v[0], v[1]])
    _fmt(se, "BC", USD); se.freeze_panes = "A2"
    for row in se.iter_rows(min_row=2):
        if row[1].value is not None and isinstance(row[1].value, str): row[1].alignment = Alignment(horizontal="center")
    se.column_dimensions["A"].width = 124; se.column_dimensions["B"].width = 10; se.column_dimensions["C"].width = 16
    # notes
    nt = wb.create_sheet("Notes")
    nt.append(["Notes"]); nt["A1"].font = bold
    for t in ("Position at 31 December 2026: capital account statements, custodian records and the commitment register as pulled on 12 March 2027.",
              "The test follows the liquidity policy for private-fund commitments (September 2025): the eight quarters from 1 January 2027 "
              "(section 2), net cash needs as section 3 defines them, the reserve at the section 4 factors, the minimum the Investment "
              "Committee set for 2027 (section 5), the stress of section 6 and distributions at the benchmark's 2008-10 rates (section 7).",
              "Figures are USD million at Wexmoor's share of each fund, to one decimal; proposed commitments are the plan's sizes. "
              "Halves are calendar halves.",
              "Commitments released at a fund's term end are excluded; commitments to funds yet to hold a first close count in full (section 3).",
              "%s funds' fourth-quarter statements had not arrived by 12 March 2027; their 31 December values are the 30 September values "
              "plus the quarter's calls less its distributions in the custodian's records (section 7)." % NUMW.get(F["late_statements"], str(F["late_statements"])),
              "One manager restated its second-quarter 2024 statement; the superseded line is left out.",
              "Section 8 sets the pace of new investments, the dates of first closes still to come, the calls of buyout, growth and venture "
              "funds past their investment periods, how the facility balances are formed and the quarter they count in, and the fees and "
              "expenses; the Policy bases and Facility balances sheets carry them. No investment period is extended in the stress. "
              "When each fund's investment period ends and what the property and infrastructure loans cost at maturity are judged on "
              "the register and the managers' activity reports (sheets Successor closes and Asset loans)."):
        nt.append([t]); nt.cell(nt.max_row, 1).alignment = Alignment(wrap_text=True, vertical="top")
    nt.column_dimensions["A"].width = 120
    wb.save(path)


def _footer(sec):
    par = sec.footer.paragraphs[0]
    par.text = "Wexmoor University Endowment  |  Office of Investments  |  Internal  |  Page "
    for r in par.runs: r.font.size = Pt(8)
    run = par.add_run(); run.font.size = Pt(8)
    fld = OxmlElement("w:fldSimple"); fld.set(qn("w:instr"), "PAGE")
    r_ = OxmlElement("w:r"); t_ = OxmlElement("w:t"); t_.text = "1"; r_.append(t_); fld.append(r_)
    par._p.append(fld)


def memo(F, R, path):
    g = R["golden"]; L = R["L"]
    doc = Document()
    sec = doc.sections[0]; sec.page_width, sec.page_height = Mm(216), Mm(279)
    sec.left_margin = sec.right_margin = Mm(22); sec.top_margin = sec.bottom_margin = Mm(18)
    st = doc.styles["Normal"]; st.font.name = "Calibri"; st.font.size = Pt(10)
    _footer(sec)
    def p(t, bold_lead=None, size=None, after=5):
        par = doc.add_paragraph()
        if bold_lead:
            r0 = par.add_run(bold_lead); r0.bold = True
            if size: r0.font.size = Pt(size)
        run = par.add_run(t)
        if size: run.font.size = Pt(size)
        par.paragraph_format.space_after = Pt(after); return par
    pr = F["programs"]; adopt = F["program"]
    funds = next(x for x in L["programs"] if x["code"] == adopt)["funds"] if adopt != "none" else []
    fails = [c for c in sorted(pr) if not pr[c]["passes"]]
    deferred = [x["fund"] for x in L["plan"] if x["fund"] not in funds]
    doc.add_heading("Program %s is the largest that passes the liquidity test for 2027" % adopt, 1)
    for lead, t in (("To: ", "Investment Committee"), ("From: ", "Caitlin Hill, Director of Private Markets"),
                    ("Copy: ", "Daniel Marshall, Chief Investment Officer"), ("Date: ", "16 March 2027"),
                    ("Subject: ", "Corrigan Hart's 2027 commitment programs against the liquidity policy")):
        p(t, lead, after=10 if lead == "Subject: " else 0)
    big = fails[-1] if fails else adopt
    andl = lambda xs: ", ".join(xs[:-1]) + " and " + xs[-1] if len(xs) > 1 else "".join(xs)
    p("Adopt program %s (%s, USD %.0f million) and defer %s to 2028. Before any 2027 commitment the policy's stress leaves "
      "USD %.1f million above the USD %s million minimum. Program %s's re-ups would call USD %.1f million over the eight quarters "
      "and leave USD %.1f million to spare; program %s's would call USD %.1f million and take the reserve USD %.1f million below the "
      "minimum."
      % (adopt, andl(funds), F["program_total_usd_m"], andl(deferred), F["headroom_before_2027_usd_m"],
         format(int(F["minimum_reserve_usd_m"]), ","), adopt, pr[adopt]["calls_usd_m"], pr[adopt]["headroom_usd_m"],
         big, pr[big]["calls_usd_m"], -pr[big]["headroom_usd_m"]), "Recommendation. ")
    ev = F["successor_events"]
    p("Two things in the evidence decide it, and they pull in opposite directions. First, most of our managers' agreements end "
      "a fund's investment period when the manager's next fund holds its first close; the register shows it at every past "
      "succession for %d managers. %s of our funds have a successor closing inside the eight quarters (%s), so their new "
      "investments stop earlier than the register's period ends say. That takes USD %.1f million off the calls; held to their "
      "registered ends, the headroom would be USD %.1f million and program %s would be the largest to pass."
      % (len(F["clause_managers"]), NUMW.get(len(ev), str(len(ev))), andl([e["fund"] for e in ev]), F["successor_effect_usd_m"],
         F["factorial"]["S1 dropped"]["headroom_before_2027_usd_m"], F["factorial"]["S1 dropped"]["program"]))
    lr = F["lender_rule"]
    p("Second, %d loans on our property and infrastructure funds' assets fall due in 2027 and 2028 (USD %.1f million at our share). "
      "Lenders have refinanced since mid-2022 at the lower of %.0f percent of value and what the asset's income carries at the "
      "rate then, about %.0f percent of value at the stress's rate; on values that fall with the stress they would grant USD %.1f "
      "million less than the balances, and the funds would call USD %.1f million of it from us. Carried as they stand, the loans "
      "would leave USD %.1f million of headroom and program %s would appear to pass."
      % (F["loans_due_count"], F["loans_due_balance_usd_m"], 100 * lr["cap_post"], 100 * F["lender_limit_stressed"], F["loans_due_gap_usd_m"],
         F["refinancing_calls_total_usd_m"], F["factorial"]["S2 dropped"]["headroom_before_2027_usd_m"], F["factorial"]["S2 dropped"]["program"]))
    p("The rest follows section 8 of the policy as written: the capital our managers have invested through their credit facilities "
      "(USD %.1f million) counts in the first quarter, new investments run at each strategy's pace while a fund's investment period "
      "lasts (USD %s million), funds yet to hold a first close call from their managers' dates, and the %d buyout, growth and "
      "venture funds past their investment periods call at the benchmark's rate for 2008 to 2010 (USD %.1f million with those whose "
      "periods end in the stress)."
      % (F["line_stock_usd_m"], format(F["new_investments_total_usd_m"], ",.1f"), F["old_funds_31dec"], F["old_fund_calls_total_usd_m"]))
    t = doc.add_table(rows=1, cols=5); t.style = "Table Grid"
    hdr = t.rows[0].cells; hdr[0].text = "USD million"
    for i, hh in enumerate(A.HALVES): hdr[i + 1].text = hh
    for c in hdr:
        for r in c.paragraphs[0].runs: r.bold = True
    calls = {**g["R2"], **g["R3"]}
    for lbl, d in (("Calls on the commitments made by the end of 2026", calls), ("Distributions at the policy's rates", g["R4"])):
        row = t.add_row().cells; row[0].text = lbl
        for i, hh in enumerate(A.HALVES):
            row[i + 1].text = "%.1f" % d[hh]; row[i + 1].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p("Source: Office of Investments, 2027 program test workbook; the policy's stress on the position at 31 December 2026.", size=8, after=8)
    fam = [v["headroom_before_2027_usd_m"] for v in F["family"].values()]
    p("The commitments not yet called at 31 December total USD %s million. The workbook carries the test, each program, the "
      "successor closes, the loans that fall due, the facility balances fund by fund, the bases section 8 sets and the "
      "sensitivities; the alternative fits on its Sensitivity sheet leave the headroom between USD %.1f and %.1f million and "
      "program %s the largest that passes."
      % (format(F["unfunded_total_usd_m"], ",.1f"), min(fam), max(fam), adopt))
    p("%s funds' fourth-quarter statements had not arrived by 12 March; as section 7 of the policy provides, their 31 December "
      "values are the 30 September values plus the quarter's calls less its distributions in the custodian's records."
      % NUMW.get(F["late_statements"], str(F["late_statements"])), size=8, after=0)
    doc.save(path)
