"""The golden deliverables: the Office of Investments' workbook for the 2027 budget and the one-page memo to the
Investment Committee."""
import datetime as dt
from zoneinfo import ZoneInfo
from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.styles import Font
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table
import analysis as A
import officepdf as O

NY = ZoneInfo("America/New_York")
XLSX = "wexmoor_2027_commitment_capacity.xlsx"
MEMO = "commitment_budget_2027_memo.pdf"
QL = lambda q: "Q%d %d" % (q % 4 + 1, A.Q0 + q // 4)


def workbook(F, R, path):
    g = R["golden"]; t5, t25 = R["test_at"][500.0], R["test_at"][250.0]
    wb = Workbook(); bold = Font(bold=True)
    ws = wb.active; ws.title = "Summary"
    rows = [("2027 private-fund commitment budget: liquidity test at 31 December 2026", None, None),
            ("", None, None),
            ("Largest budget that passes (USD m, policy steps of 25)", F["capacity_usd_m"], None),
            ("Before rounding to the policy's steps (USD m)", F["capacity_unrounded_usd_m"], None),
            ("Range across the defensible methods (USD m)", "%d to %d" % tuple(F["capacity_band_usd_m"]), None),
            ("", None, None),
            ("The test over 2027 and 2028 (USD m)", "Budget 500", "Budget 250"),
            ("Liquid reserve at 31 December 2026, at the policy's factors", t5["reserve"], t25["reserve"]),
            ("Spending distribution (eight quarters of FY2027's)", t5["spending"], t25["spending"]),
            ("Calls, funds that have held a first close", t5["calls_closed"], t25["calls_closed"]),
            ("Calls, funds yet to hold a first close", t5["calls_pending"], t25["calls_pending"]),
            ("Calls, the 2027 budget's new commitments", t5["calls_budget"], t25["calls_budget"]),
            ("Distributions", t5["distributions"], t25["distributions"]),
            ("Net cash needs", t5["net"], t25["net"]),
            ("Reserve left at 31 December 2028", t5["left"], t25["left"]),
            ("Minimum reserve set for 2027", t5["minimum"], t25["minimum"]),
            ("Headroom above the minimum", t5["headroom"], t25["headroom"]),
            ("Result", "Fails" if t5["headroom"] < 0 else "Passes", "Fails" if t25["headroom"] < 0 else "Passes")]
    for r in rows:
        ws.append(list(r))
    for rr in (1, 7):
        for c in ws[rr]: c.font = bold
    ws.column_dimensions["A"].width = 62; ws.column_dimensions["B"].width = 14; ws.column_dimensions["C"].width = 14
    # calls and distributions by half (the eight quarters' totals as the Summary states them)
    h = wb.create_sheet("By half-year")
    h.append(["USD m", *A.HALVES, "Eight quarters"])
    for c in h[1]: c.font = bold
    def line(lbl, d, total=None):
        h.append([lbl] + [d[k] for k in A.HALVES] + [round(sum(d.values()), 1) if total is None else total])
    line("Calls, funds that have held a first close", g["R2"], t5["calls_closed"])
    stock = {k: (F["line_stock_usd_m"] if k == "H1 2027" else 0.0) for k in A.HALVES}
    new_deals = {k: round(g["R2"][k] - g["support"][k] - g["fees"][k] - stock[k] + g["recycled"][k], 1) for k in A.HALVES}
    line("   of which new deals and planned follow-ons", new_deals)
    line("   of which defensive follow-ons", g["support"])
    line("   of which fees", g["fees"])
    line("   of which investments on credit lines at 31 December, called at the clean-down", stock)
    line("   less proceeds recycled into investments", g["recycled"])
    line("Calls, funds yet to hold a first close", g["R3"], t5["calls_pending"])
    line("Calls, a USD 500m 2027 budget", F["plan_calls_500_by_half_usd_m"], t5["calls_budget"])
    line("Distributions, the policy's 2008-10 rates", g["R4"], t5["distributions"])
    h.column_dimensions["A"].width = 70
    for col in "BCDEF": h.column_dimensions[col].width = 12
    # unfunded
    u = wb.create_sheet("Unfunded")
    u.append(["Strategy", "Commitments not yet called at 31 Dec 2026 (USD m)"])
    for c in u[1]: c.font = bold
    for s in A.STRAT_ORDER: u.append([s, g["R1"][s]])
    u.append(["Total", F["unfunded_total_usd_m"]])
    u.column_dimensions["A"].width = 20; u.column_dimensions["B"].width = 46
    # the line stock by fund
    ls = wb.create_sheet("Credit-line stock")
    ls.append(["Fund ID", "Fund", "Manager", "Strategy", "Invested on lines, not yet called, 31 Dec 2026 (USD m)"])
    for c in ls[1]: c.font = bold
    L = R["L"]
    for fid, v in sorted(R["stock"].items(), key=lambda kv: -kv[1]):
        r = L["reg"][fid]
        if r["Status"] == "liquidated" or v < 0.05: continue
        ls.append([fid, r["Fund"], r["Manager"], r["Strategy"], round(v, 1)])
    ls.append(["Total", "", "", "", F["line_stock_usd_m"]])
    for col, w in zip("ABCDE", (12, 30, 28, 16, 50)): ls.column_dimensions[col].width = w
    # the pending funds
    pf = wb.create_sheet("First closes")
    pf.append(["Fund", "Strategy", "Commitment (USD m)", "First close expected", "Expected slip in the stress (quarters)", "Group"])
    for c in pf[1]: c.font = bold
    for p in F["pending_funds"]:
        pf.append([p["fund"], {v: k for k, v in A.STRATS.items()}[p["st"]], p["C"], QL(p["exp"]), p["slip"], "committed, yet to close"])
    for p in F["plan_slips"]:
        pf.append([p["fund"], {v: k for k, v in A.STRATS.items()}[p["st"]], p["C"], QL(p["exp"]), p["slip"], "2027 plan"])
    for col, w in zip("ABCDEF", (28, 16, 18, 20, 34, 22)): pf.column_dimensions[col].width = w
    # fitted inputs
    fi = wb.create_sheet("Fitted inputs")
    s, sl = F["support"], F["slip"]
    for r in [("Defensive follow-ons: share of the cost of companies held two years or more, per quarter, per unit the index sits below its threshold", s["sigma"]),
              ("   threshold on the exit index (2015 = 100)", round(100 * s["e_star"])), ("   quarters after the index", s["lag"]),
              ("First-close slip: quarters per unit the index sits below its reference in the quarter before", sl["b"]),
              ("   intercept (quarters)", sl["a"]), ("   reference level", sl["ref"]), ("   quarters averaged", sl["win"]),
              ("New-deal pace: elasticity on the exit index", F["deal_market_elasticity"]),
              ("Calls per USD 100m of 2027 budget over the eight quarters (USD m)", F["calls_per_100_of_budget_usd_m"])]:
        fi.append(list(r))
    fi.append([])
    fi.append(["Investment pace on the room left, per quarter", "Year 1", "Year 2", "Year 3", "Year 4", "Year 5", "Year 6", "Year 7"])
    for c in fi[fi.max_row]: c.font = bold
    for sname in A.STRAT_ORDER:
        st = A.STRATS[sname]
        fi.append([sname] + [round(R["dep"].get((st, a), 0.0), 4) if (st, a) in R["dep"] else None for a in range(7)])
    fi.append([])
    fi.append(["Management fee per quarter while investing, share of commitment"] + [None] * 7)
    for c in fi[fi.max_row]: c.font = bold
    for sname in A.STRAT_ORDER:
        fi.append([sname, round(R["fee"][A.STRATS[sname]], 5)])
    fi.column_dimensions["A"].width = 100
    # the sweep and its chart
    sw = wb.create_sheet("Budget sweep")
    sw.append(["2027 budget (USD m)", "Headroom above the minimum reserve (USD m)"])
    for c in sw[1]: c.font = bold
    for b, hd in R["sweep"]: sw.append([b, hd])
    ch = LineChart(); ch.title = "Headroom above the minimum reserve by 2027 budget"; ch.y_axis.title = "USD m"; ch.x_axis.title = "2027 budget (USD m)"
    ch.add_data(Reference(sw, min_col=2, min_row=1, max_row=sw.max_row), titles_from_data=True)
    ch.set_categories(Reference(sw, min_col=1, min_row=2, max_row=sw.max_row)); ch.height, ch.width = 8, 16
    sw.add_chart(ch, "D2")
    sw.column_dimensions["A"].width = 20; sw.column_dimensions["B"].width = 42
    # sensitivity
    se = wb.create_sheet("Sensitivity")
    se.append(["Method or input", "Largest budget that passes (USD m)", "Before rounding"])
    for c in se[1]: c.font = bold
    se.append(["This workbook", F["capacity_usd_m"], F["capacity_unrounded_usd_m"]])
    for n, v in F["family"].items(): se.append([n, v["capacity_usd_m"], v["unrounded"]])
    se.append([])
    se.append(["Bootstrap over funds (40 resamples), 5th and 95th percentiles before rounding", None, None])
    for c in se[se.max_row]: c.font = bold
    for k, v in F["bootstrap_p5_p95"].items():
        if k in ("eta", "sigma", "slip_b"): continue
        se.append([k, v[0], v[1]])
    se.column_dimensions["A"].width = 80; se.column_dimensions["B"].width = 34; se.column_dimensions["C"].width = 16
    wb.save(path)


def memo(F, R, path):
    g = R["golden"]; t5 = R["test_at"][500.0]
    body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.0, leading=12.2, spaceAfter=4.5)
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=12, leading=15, spaceAfter=4)
    small = ParagraphStyle("small", fontName="Helvetica", fontSize=8.0, leading=10.4)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.2, leading=10.4)
    sup = sum(g["support"].values()); pend = sum(g["R3"].values())
    unslipped = sum(R["passes"]["careful"]["R3"].values())
    n_pend = len(F["pending_funds"]); c_pend = sum(p["C"] for p in F["pending_funds"])
    rows = [["USD m", *A.HALVES]]
    rows.append(["Calls, funds that have held a first close"] + ["%.1f" % g["R2"][k] for k in A.HALVES])
    rows.append(["Calls, funds yet to hold a first close"] + ["%.1f" % g["R3"][k] for k in A.HALVES])
    rows.append(["Distributions (policy rates)"] + ["%.1f" % g["R4"][k] for k in A.HALVES])
    t = Table([[Paragraph(c, cell) for c in r] for r in rows], colWidths=[190, 62, 62, 62, 62])
    s = [Paragraph("Wexmoor University Endowment  |  Office of Investments", small),
         Paragraph("2027 private-fund commitment budget", h1),
         Paragraph("To the Investment Committee. From Caitlin Hill, Director of Private Markets; copy Daniel Marshall, Chief "
                   "Investment Officer. 16 March 2027.", small), Spacer(1, 4),
         Paragraph("<b>Recommendation.</b> Approve a 2027 budget of no more than USD %d million, not the USD 500 million in "
                   "Corrigan Hart's draft. At USD 500 million the liquidity policy's test fails: in the policy's stress the "
                   "reserve of USD %s million less net cash needs of USD %s million over 2027 and 2028 leaves USD %s million, "
                   "USD %.1f million below the USD %s million minimum. The largest budget that passes is USD %.1f million "
                   "before the policy's USD 25 million steps; the methods I could defend put it between USD %d and %d million."
                   % (F["capacity_usd_m"], format(t5["reserve"], ",.1f"), format(t5["net"], ",.1f"), format(t5["left"], ",.1f"),
                      -t5["headroom"], format(int(F["minimum_reserve_usd_m"]), ","), F["capacity_unrounded_usd_m"],
                      F["capacity_band_usd_m"][0], F["capacity_band_usd_m"][1]), body),
         Paragraph("<b>What the draft's pacing does not see.</b> Three things in our own records decide the number, and "
                   "missing any one of them puts the budget well outside that range.", body),
         Paragraph("<i>Capital already invested and not yet called.</i> Our managers had USD %.1f million invested on their "
                   "funds' subscription lines at 31 December, rebuilt fund by fund from their portfolio activity, the "
                   "capital we were called for and the borrowings in each fund's audited accounts, after the proceeds they "
                   "recycle. The stress puts short rates at %.2f per cent, past every manager's limit for carrying a line, and "
                   "as in 2022 and 2023 they clean the lines down: it is called in the first quarter."
                   % (F["line_stock_usd_m"], R["L"]["R"][A.H_END] + 2.5), body),
         Paragraph("<i>Defensive follow-ons.</i> When exits run below normal our buyout, growth and venture managers put more "
                   "into companies they have held two years or more, two quarters later, while new deals slow. Fitted on "
                   "2020 and 2022 to 2024, that adds USD %.1f million of calls over the eight quarters on the stress path."
                   % sup, body),
         Paragraph("<i>First closes slip.</i> Our register shows first closes slipping about %.2f quarters for each 10 "
                   "points the exit index sat below 100 in the quarter before. The %s funds still to close (USD %.0f "
                   "million) close in 2028, not in the second half of 2027, and call USD %.1f million in the eight quarters "
                   "rather than USD %.1f million." % (F["slip"]["b"] * 10 / F["slip"]["ref"], {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}.get(n_pend, str(n_pend)), c_pend, pend, unslipped), body),
         Paragraph("<b>Calls and distributions on the commitments made by 31 December 2026.</b>", body), t, Spacer(1, 5),
         Paragraph("Distributions follow the policy's 2008 to 2010 benchmark rates on each fund's 31 December value. "
                   "The commitments not yet called at 31 December total USD %s million. A USD %d million budget leaves USD "
                   "%.1f million above the minimum. The workbook carries the test, the fund-by-fund line stock, the fitted "
                   "inputs and the sensitivities." % (format(F["unfunded_total_usd_m"], ",.1f"), F["capacity_usd_m"],
                                                      R["test_at"][250.0]["headroom"]), body)]
    O.build(path, s, "2027 private-fund commitment budget", "Caitlin Hill", "Commitment budget memo",
            "Wexmoor University Endowment  |  Office of Investments  |  Confidential",
            dt.datetime(2027, 3, 16, 9, 4, 12, tzinfo=NY), dt.datetime(2027, 3, 16, 11, 38, 50, tzinfo=NY), producer="LibreOffice 26.8")
