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
NAMES = {"A": "the full program", "B": "the credit re-up deferred", "C": "the growth and credit re-ups deferred", "D": "the venture re-up only"}


USD = "#,##0.0"
WHOLE = "#,##0"
TIDY = lambda t: t[:1].upper() + t[1:]


def _fmt(ws, cols, fmt, first=2, last=None):
    for row in ws.iter_rows(min_row=first, max_row=last or ws.max_row):
        for c in row:
            if c.column_letter in cols and isinstance(c.value, (int, float)):
                c.number_format = fmt


def workbook(F, R, path):
    g = R["golden"]; bold = Font(bold=True); L = R["L"]
    wb = Workbook(); ws = wb.active; ws.title = "Summary"
    adopt = F["program"]
    others = [c for c in sorted(F["programs"]) if c != adopt]
    fail = ", ".join(others[:-1]) + " and " + others[-1] if len(others) > 1 else "".join(others)
    ws.append(["Program %s passes the 2027 liquidity test; %s fail" % (adopt, fail)])
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
    ch.title = "Only program %s leaves headroom above the minimum" % adopt
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
    line("   of which defensive follow-ons and rescue financings", g["support"])
    line("Distributions, the policy's 2008-10 rates", g["R4"])
    _fmt(h, "BCDEF", USD); h.freeze_panes = "B2"
    h.column_dimensions["A"].width = 52
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
    # the line stock
    ls = wb.create_sheet("Credit-line stock")
    ls.append(["Fund ID", "Fund", "Manager", "Invested on lines, not yet called, 31 Dec 2026 (USD m)", "Basis"])
    for c in ls[1]: c.font = bold
    for fid, v in sorted(R["stock"].items(), key=lambda kv: -kv[1]):
        r = L["reg"][fid]
        if r["Status"] == "liquidated" or v < 0.05: continue
        basis = ("Company-level reports stop after Q4 2024: rolled from that quarter on the covered funds' pace, less the investment "
                 "capital called, re-anchored at each later audit" if r["Manager"] in L["cov"] else
                 "Investments at Wexmoor's share less the investment capital called, less recycled proceeds")
        ls.append([fid, r["Fund"], r["Manager"], round(v, 1), basis])
    ls.append(["Total", "", "", F["line_stock_usd_m"], ""])
    for c in ls[ls.max_row]: c.font = bold
    _fmt(ls, "D", USD); ls.freeze_panes = "B2"
    for col, w in zip("ABCDE", (11, 28, 26, 20, 104)): ls.column_dimensions[col].width = w
    ls["D1"].alignment = Alignment(wrap_text=True, vertical="top")
    ls.auto_filter.ref = "A1:E%d" % (ls.max_row - 1)
    # the support response
    sp = wb.create_sheet("Support response")
    s_ = F["support"]
    sp.append(["Fitted on", "Parameter", "Value"])
    for c in sp[1]: c.font = bold
    for src, lbl, v, fmt in (("Wexmoor's funds, 2013-26", "Defensive follow-ons per quarter, share of the cost of companies held two years or more, per unit of shortfall", s_["sigma"], "0.000"),
                             ("Wexmoor's funds, 2013-26", "Shortfall at which the managers' reserves cap them", s_["cap"], "0%"),
                             ("Wexmoor's funds, 2013-26", "Lag behind the exit index (quarters)", s_["lag"], "0"),
                             ("Benchmark funds past their investment period, 2004-14", "Shortfall past which rescue financings start", s_["th"], "0%"),
                             ("Benchmark funds past their investment period, 2004-14", "Rescue financings per unit of shortfall past it, relative to the first channel", s_["ratio"], "0.00"),
                             ("Benchmark funds past their investment period, 2004-14", "Rescue financings per quarter, per unit of shortfall past it", s_["sigma2"], "0.000")):
        sp.append([src, lbl, v]); sp.cell(sp.max_row, 3).number_format = fmt
    sp.append([])
    sp.append(["Quarter", "Benchmark funds more than six years old with commitment left to call: calls, share of commitment", "Exit shortfall two quarters before"])
    t0 = sp.max_row
    for c in sp[t0]: c.font = bold
    bq = A.bench_old_calls(L)
    for q in sorted(bq):
        if A.qi(2007, 1) <= q <= A.qi(2012, 4):
            sp.append([QL(q), round(bq[q], 5), round(max(0.0, 1.0 - L["E"][q - 2] / 100.0), 3)])
            sp.cell(sp.max_row, 2).number_format = "0.00%"; sp.cell(sp.max_row, 3).number_format = "0.0%"
    sp.column_dimensions["A"].width = 46; sp.column_dimensions["B"].width = 96; sp.column_dimensions["C"].width = 18
    # sensitivity
    se = wb.create_sheet("Sensitivity")
    se.append(["Method or input", "Program", "Headroom before 2027 (USD m)"])
    for c in se[1]: c.font = bold
    se.append(["This workbook", F["program"], F["headroom_before_2027_usd_m"]])
    for n, v in F["family"].items(): se.append([TIDY(n), v["program"], v["headroom_before_2027_usd_m"]])
    se.append([])
    se.append(["Bootstrap over funds, 5th and 95th percentiles of the headroom (USD m)", "5th", "95th"])
    for c in se[se.max_row]: c.font = bold
    for k, v in F["bootstrap_p5_p95"].items(): se.append([TIDY(k), v[0], v[1]])
    _fmt(se, "BC", USD); se.freeze_panes = "A2"
    for row in se.iter_rows(min_row=2):
        if row[1].value is not None and isinstance(row[1].value, str): row[1].alignment = Alignment(horizontal="center")
    se.column_dimensions["A"].width = 84; se.column_dimensions["B"].width = 10; se.column_dimensions["C"].width = 16
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
              "Two funds' fourth-quarter statements had not arrived by 12 March 2027; their 31 December values are the 30 September values "
              "plus the quarter's calls less its distributions in the custodian's records (section 7).",
              "One manager restated its second-quarter 2024 statement; the superseded line is left out.",
              "Six managers' company-level reports stop after the fourth quarter of 2024 while their statements and audits continue (%s); "
              "their funds' line balances are carried as the Credit-line stock sheet sets out." % ", ".join(F["six_managers"])):
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
    doc.add_heading("Only program %s passes the liquidity test for 2027" % adopt, 1)
    for lead, t in (("To: ", "Investment Committee"), ("From: ", "Caitlin Hill, Director of Private Markets"),
                    ("Copy: ", "Daniel Marshall, Chief Investment Officer"), ("Date: ", "16 March 2027"),
                    ("Subject: ", "Corrigan Hart's 2027 commitment programs against the liquidity policy")):
        p(t, lead, after=10 if lead == "Subject: " else 0)
    p("Adopt program %s, %s: %s, USD %.0f million, and defer the other re-ups to 2028. Programs A, B and C "
      "fail the liquidity policy: before any 2027 commitment the stress leaves USD %.1f million above the USD %s million minimum, "
      "and their re-ups would call USD %.1f, %.1f and %.1f million over the eight quarters. Program %s's re-up calls USD %.1f million, "
      "which leaves USD %.1f million to spare."
      % (adopt, NAMES.get(adopt, ""), "; ".join(funds), F["program_total_usd_m"], F["headroom_before_2027_usd_m"],
         format(int(F["minimum_reserve_usd_m"]), ","), pr["A"]["calls_usd_m"], pr["B"]["calls_usd_m"], pr["C"]["calls_usd_m"], adopt,
         pr[adopt]["calls_usd_m"] if adopt in pr else 0.0, pr[adopt]["headroom_usd_m"] if adopt in pr else 0.0), "Recommendation. ")
    s_ = F["support"]
    p("Two things in the evidence decide it. First, the managers' calls on the companies they already hold do not stop rising "
      "where our own record stops. Our funds show defensive follow-ons climbing with the exit market's shortfall up to about %.0f "
      "percent, then flat; the stress takes the shortfall past %.0f percent, further than our record has gone. The benchmark's "
      "funds past their investment period, where new deals cannot move the calls, show what happens there: in 2009 their calls "
      "rose again, about %.1f times as steeply per point of shortfall past %.0f percent, as lenders forced rescue financings. "
      "Carried on our holdings, that puts the defensive and rescue calls at USD %.1f million over the eight quarters, most of it in 2028."
      % (100 * s_["cap"], 100 * s_["th"], s_["ratio"], 100 * s_["th"], F["support_total_usd_m"]))
    p("Second, six managers' company-level files stop after 2024, so their capital invested on credit lines cannot be read off "
      "them. Rolled from the last quarter the files cover, at the pace our other managers kept and less the capital the six called, "
      "and re-anchored at each audit since, it stands at USD %.1f million at 31 December; their last audited balances would put it near "
      "nothing, because those lines were cleaned down at the end of 2025 and rebuilt through 2026 as rates fell. Like the other "
      "managers' USD %.1f million, it is called in the first quarter of the stress."
      % (F["line_stock_six_managers_usd_m"], F["line_stock_usd_m"] - F["line_stock_six_managers_usd_m"]))
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
    p("The commitments not yet called at 31 December total USD %s million. The workbook carries the test, each program, the "
      "line balances fund by fund, the support response and the sensitivities; the alternative fits on its Sensitivity sheet and "
      "a bootstrap over funds all leave program %s as the one that passes." % (format(F["unfunded_total_usd_m"], ",.1f"), adopt))
    p("Two funds' fourth-quarter statements had not arrived by 12 March; as section 7 of the policy provides, their 31 December "
      "values are the 30 September values plus the quarter's calls less its distributions in the custodian's records.", size=8, after=0)
    doc.save(path)
