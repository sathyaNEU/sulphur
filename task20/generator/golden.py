"""task20 architecture 2 golden deliverables: the desk's nowcast workbook and the one-page note to the investment
committee, every figure taken from figures.json (and the analysis run that wrote it)."""
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import analysis as A

XLSX = "bmh_q4fy25_revenue_nowcast.xlsx"
NOTE = "bmh_q4fy25_nowcast_note.docx"
REG = A.REGIONS
HEAD = PatternFill("solid", fgColor="D9E1F2")
THIN = Side(style="thin", color="A6A6A6")


def _q(k):
    return k.replace("FY", "Fiscal ").replace(" Q", " Q")


def _head(ws, row, cols):
    for j, v in enumerate(cols, 1):
        c = ws.cell(row=row, column=j, value=v)
        c.font = Font(bold=True)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)


def _widths(ws, widths):
    for j, w in enumerate(widths):
        ws.column_dimensions[chr(65 + j)].width = w


def workbook(F, R, path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Call"
    ws["A1"] = "Brindle & Moss (BMH): fourth quarter fiscal 2025 net sales from the Kestrel panel"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Panel delivery of 2 February 2026; results due 26 February 2026"
    rows = [("Fourth quarter fiscal 2024 net sales (USD m)", F["base_net_sales_m"], "0.0"),
            ("Year-on-year growth, fourth quarter fiscal 2025 (%)", F["growth_pct"], "0.00"),
            ("Net sales estimate (USD m)", F["forecast_m"], "#,##0.0"),
            ("80% range, low (USD m)", F["range_low_m"], "#,##0.0"),
            ("80% range, high (USD m)", F["range_high_m"], "#,##0.0"),
            ("Range half-width (points of growth)", F["band_pp"], "0.00"),
            ("Street: mean of %d estimates (USD m)" % F["street_n"], F["street_m"], "#,##0.0"),
            ("Street: median (USD m)", F["street_median_m"], "#,##0.0"),
            ("Street growth implied (%)", F["street_growth_pct"], "0.00"),
            ("Street less top of range (USD m)", F["range_gap_m"], "#,##0.0"),
            ("Call", "Short: the whole range sits below the street", None)]
    _head(ws, 4, ["Item", "Value"])
    for i, (k, v, fmt) in enumerate(rows, 5):
        ws.cell(row=i, column=1, value=k)
        c = ws.cell(row=i, column=2, value=v)
        if fmt:
            c.number_format = fmt
    ws.cell(row=17, column=1, value="Range: estimate plus and minus 1.2816 times the record's root mean square error "
                                    "(sheet Record).")
    _widths(ws, [52, 44])

    b = wb.create_sheet("Bridge")
    _head(b, 1, ["Step", "Worth (points of growth)", "Growth after the step (%)"])
    run = 0.0
    for i, (k, v) in enumerate(F["bridge_pp"], 2):
        run = v if i == 2 else run + v
        b.cell(row=i, column=1, value=k[0].upper() + k[1:])
        b.cell(row=i, column=2, value=v).number_format = "0.00"
        b.cell(row=i, column=3, value=round(run, 2)).number_format = "0.00"
    b.cell(row=9, column=1, value="Steps applied in the order listed; each worth is the change in year-on-year growth "
                                  "(weekly averages) when the step is added.")
    _widths(b, [48, 22, 24])

    g = wb.create_sheet("Regions")
    _head(g, 1, ["Billing region", "Growth, same-age cards (%)", "Panel spend weight (%)", "Company weight, fiscal 2024 (%)",
                 "Contribution at company weight (points)"])
    for i, r in enumerate(REG, 2):
        g.cell(row=i, column=1, value=r)
        g.cell(row=i, column=2, value=F["regional_pct"][r]).number_format = "0.00"
        g.cell(row=i, column=3, value=F["panel_weights_pct"][r]).number_format = "0.00"
        g.cell(row=i, column=4, value=F["company_weights_pct"][r]).number_format = "0.00"
        g.cell(row=i, column=5, value=round(F["regional_pct"][r] * F["company_weights_pct"][r] / 100.0, 2)).number_format = "0.00"
    g.cell(row=6, column=1, value="At the panel's weights")
    g.cell(row=6, column=2, value=F["pooled_growth_pct"]).number_format = "0.00"
    g.cell(row=7, column=1, value="At the company's weights")
    g.cell(row=7, column=2, value=F["visible_growth_pct"]).number_format = "0.00"
    g.cell(row=9, column=1, value="Issuers KS-01 to KS-05 (in the panel in both quarters). Each card-open year is set "
                                  "against the open year one later, on the base quarter's cards. Company weights from the "
                                  "10-K's net sales by region, fiscal 2024.")
    _widths(g, [26, 22, 20, 24, 26])

    t = wb.create_sheet("Tender")
    _head(t, 1, ["Fiscal quarter", "Private-label share of net sales (%)", "Bank-card share (%)"])
    pl = R["P"]["pl"]
    ks = [k for k in R["P"]["keys"] if k >= "FY2024 Q1" and k in pl]
    for i, k in enumerate(ks, 2):
        t.cell(row=i, column=1, value=_q(k))
        t.cell(row=i, column=2, value=pl[k]).number_format = "0.0"
        t.cell(row=i, column=3, value=round(100 * A.bank_share(pl[k]), 1)).number_format = "0.0"
    n = len(ks) + 2
    t.cell(row=n, column=1, value="Fiscal 2025 Q4 (carried)")
    t.cell(row=n, column=2, value=F["pl_target_pct"]).number_format = "0.00"
    t.cell(row=n, column=3, value=round(100 * A.bank_share(F["pl_target_pct"]), 2)).number_format = "0.00"
    t.cell(row=n + 2, column=1, value="Net sales per dollar of bank-card spend, Q4 on Q4 (%)")
    t.cell(row=n + 2, column=2, value=F["drift_pct"]).number_format = "0.00"
    t.cell(row=n + 4, column=1, value="Fourth quarter carried at the pace of fiscal 2025's first three quarters: the third "
                                      "quarter plus a third of its change on the fourth quarter of fiscal 2024. Bank cards: "
                                      "net sales less the private-label card and the 10-K's 12% of other tenders.")
    _widths(t, [44, 30, 20])

    dp = wb.create_sheet("Deposits")
    _head(dp, 1, ["Fiscal quarter end", "Customer deposits (USD m)", "Deposits in weeks of retail payments"])
    P = R["P"]
    ks = [k for k in P["keys"][:-1] if k >= "FY2023 Q1"]
    for i, k in enumerate(ks, 2):
        dp.cell(row=i, column=1, value=_q(k))
        dp.cell(row=i, column=2, value=P["deposits"][k]).number_format = "#,##0.0"
        dp.cell(row=i, column=3, value=F["deposit_weeks"][k]).number_format = "0.00"
    n = len(ks) + 3
    rows = [("Made-to-order share of the banner's panel spend, last eight weeks of Q4 fiscal 2024 (%)", F["mto_share_base_pct"], "0.00"),
            ("Made-to-order share, last eight weeks of Q4 fiscal 2025 (%)", F["mto_share_q4_pct"], "0.00"),
            ("Customer deposits, end of Q4 fiscal 2024 (USD m)", F["deposits_base_m"], "#,##0.0"),
            ("Customer deposits, end of Q3 fiscal 2025 (USD m)", F["deposits_q3_m"], "#,##0.0"),
            ("Customer deposits, end of Q4 fiscal 2025, estimated (USD m)", F["deposits_q4_m"], "#,##0.0"),
            ("Change in deposits in Q4 fiscal 2025 (USD m)", F["deposit_change_m"], "#,##0.0"),
            ("Change in deposits in Q4 fiscal 2024 (USD m)", F["deposit_change_base_m"], "#,##0.0"),
            ("Retail payments, Q4 fiscal 2024 (USD m)", F["payments_base_m"], "#,##0.0"),
            ("Retail payments, Q4 fiscal 2025, estimated (USD m)", F["payments_q4_m"], "#,##0.0"),
            ("Retail net sales, Q4 fiscal 2025, estimated (USD m)", F["retail_q4_m"], "#,##0.0")]
    for i, (k, v, fmt) in enumerate(rows, n):
        dp.cell(row=i, column=1, value=k)
        dp.cell(row=i, column=2, value=v).number_format = fmt
    dp.cell(row=n + len(rows) + 1, column=1,
            value="Deposits at the quarter's end: last year's, scaled by retail payments in the last eight weeks of each "
                  "quarter (the panel's weekly profile) and by the made-to-order share of the banner's spend over the same "
                  "weeks (design studios and the site's custom orders, descriptor detail). Retail net sales are retail "
                  "payments less the quarter's change in deposits.")
    _widths(dp, [70, 22, 26])

    wsh = wb.create_sheet("Wholesale")
    _head(wsh, 1, ["Fiscal quarter", "Wholesale net sales (USD m)"])
    res = P["results"].set_index("fiscal_quarter")
    kw = [k for k in P["keys"][:-1] if k >= "FY2023 Q1"]
    for i, k in enumerate(kw, 2):
        wsh.cell(row=i, column=1, value=_q(k))
        wsh.cell(row=i, column=2, value=float(res.wholesale_net_sales_usd_m[k])).number_format = "#,##0.0"
    n = len(kw) + 3
    wsh.cell(row=n, column=1, value="Q4 fiscal 2025, run rate: median of the last eight quarters (USD m)")
    wsh.cell(row=n, column=2, value=F["wholesale_q4_m"]).number_format = "#,##0.0"
    wsh.cell(row=n + 1, column=1, value="Q4 fiscal 2024, as reported (USD m)")
    wsh.cell(row=n + 1, column=2, value=F["wholesale_base_m"]).number_format = "#,##0.0"
    wsh.cell(row=n + 3, column=1, value="Wholesale is invoiced to commercial customers and never appears in the card panel; "
                                        "retail is estimated from the panel and wholesale added at its run rate.")
    _widths(wsh, [62, 26])

    rc = wb.create_sheet("Record")
    _head(rc, 1, ["Fiscal quarter", "Estimate, growth (%)", "Reported growth (%)", "Error (points)", "Inside the 80% range"])
    G = R["golden"]
    band = A.Z80 * G["rmse"]
    for i, (q, x, y) in enumerate(zip(G["origins"], G["xs"], G["ys"]), 2):
        e = G["errs"][q]
        rc.cell(row=i, column=1, value=_q(q))
        rc.cell(row=i, column=2, value=round(100 * x, 2)).number_format = "0.00"
        rc.cell(row=i, column=3, value=round(100 * y, 2)).number_format = "0.00"
        rc.cell(row=i, column=4, value=F["errors_pp"][q]).number_format = "0.00"
        rc.cell(row=i, column=5, value="yes" if abs(e) <= band else "no")
    n = len(G["origins"]) + 3
    rc.cell(row=n, column=1, value="Root mean square error (points)")
    rc.cell(row=n, column=2, value=F["golden_rmse_pp"]).number_format = "0.00"
    rc.cell(row=n + 1, column=1, value="Quarters inside the range")
    rc.cell(row=n + 1, column=2, value="%d of %d" % (F["coverage_in"], F["origins"]))
    rc.cell(row=n + 3, column=1, value="Each quarter built as it would have been three weeks before its release: issuers "
                                       "in both years, the prior fiscal year's regional weights, the private-label share "
                                       "carried from the quarters reported before it, deposits from last year's, wholesale "
                                       "at the median of the eight quarters before it. Reported growth: weekly averages, "
                                       "Fernhollow out unless in both quarters.")
    rc.cell(row=n + 5, column=1, value="For comparison, net sales taken as what the panel shows (no deposits, no wholesale)")
    rc.cell(row=n + 6, column=1, value="Root mean square error (points)")
    rc.cell(row=n + 6, column=2, value=F["shortcut_rmse_pp"]["careful"]).number_format = "0.00"
    rc.cell(row=n + 7, column=1, value="Fiscal 2025 Q3 error (points)")
    rc.cell(row=n + 7, column=2, value=F["careful_q3_error_pp"]).number_format = "0.00"
    rc.cell(row=n + 8, column=1, value="Fourth quarter estimate (USD m)")
    rc.cell(row=n + 8, column=2, value=F["shortcut_m"]["careful"]).number_format = "#,##0.0"
    _widths(rc, [40, 20, 20, 16, 20])

    cp = wb.create_sheet("Completion")
    _head(cp, 1, ["Issuer", "Latest week as first delivered (% of final)", "One week back (%)", "Two weeks back (%)"])
    for i, iss in enumerate(sorted(R["cf_last_week"]), 2):
        cp.cell(row=i, column=1, value=iss)
        for j, lag in enumerate((0, 1, 2), 2):
            cp.cell(row=i, column=j, value=round(100 * R["cf"][(iss, lag)], 1)).number_format = "0.0"
    cp.cell(row=9, column=1, value="Medians over the delivery history (27 deliveries, 4 August 2025 to 2 February 2026). "
                                   "Completing the quarter's latest weeks lifts its spend by %.2f%%." % F["completion_pct"])
    cp.cell(row=10, column=1, value="Licensed shop-in-shops and cafes: %.2f%% of the brand id's spend in November to January, "
                                    "taken out by month." % F["excluded_share_pct"])
    _widths(cp, [14, 36, 20, 20])
    for sh in wb.worksheets:
        sh.freeze_panes = "A2" if sh.title != "Call" else "A5"
    wb.save(path)


def _cell_text(cell, text, bold=False, size=9, align=None):
    cell.text = ""
    p = cell.paragraphs[0]
    r = p.add_run(text)
    r.bold = bold
    r.font.size = Pt(size)
    if align:
        p.alignment = align


def note(F, R, path):
    doc = Document()
    sec = doc.sections[0]
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin = Cm(1.6)
    sec.bottom_margin = Cm(1.5)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    st.paragraph_format.space_after = Pt(4)
    h = doc.add_paragraph()
    r = h.add_run("Brindle & Moss (BMH): fourth quarter fiscal 2025 net sales")
    r.bold = True
    r.font.size = Pt(13)
    m = doc.add_paragraph()
    m.add_run("To: Robert Campbell   From: Audrey Hanson   6 February 2026").font.size = Pt(9)

    p = doc.add_paragraph()
    p.add_run("Short into the 26 February print. ").bold = True
    p.add_run("The panel puts fourth quarter net sales at USD %s million, %.2f%% %s last year's USD %s million, with an "
              "80%% range of USD %s to %s million. The street's figure, the mean of %d estimates, is USD %s million "
              "(%+.2f%%), USD %.1f million above the top of the range."
              % ("{:,.1f}".format(F["forecast_m"]), abs(F["growth_pct"]), "below" if F["growth_pct"] < 0 else "above",
                 "{:,.1f}".format(F["base_net_sales_m"]),
                 "{:,.1f}".format(F["range_low_m"]), "{:,.1f}".format(F["range_high_m"]), F["street_n"],
                 "{:,.1f}".format(F["street_m"]), F["street_growth_pct"], F["range_gap_m"]))

    tb = doc.add_table(rows=1, cols=3)
    tb.style = "Table Grid"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, v in enumerate(["From the delivered panel to net sales", "Points", "Growth after (%)"]):
        _cell_text(tb.rows[0].cells[j], v, bold=True)
    run = 0.0
    for i, (k, v) in enumerate(F["bridge_pp"]):
        run = v if i == 0 else run + v
        c = tb.add_row().cells
        _cell_text(c[0], k[0].upper() + k[1:])
        _cell_text(c[1], "%+.2f" % v, align=WD_ALIGN_PARAGRAPH.RIGHT)
        _cell_text(c[2], "%.2f" % run, align=WD_ALIGN_PARAGRAPH.RIGHT)
    for row in tb.rows:
        row.cells[0].width = Cm(9.5)
        row.cells[1].width = Cm(2.5)
        row.cells[2].width = Cm(3.0)

    rg, cw, pw = F["regional_pct"], F["company_weights_pct"], F["panel_weights_pct"]
    br = dict(F["bridge_pp"])
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.add_run("Why the panel reads a beat and the quarter is not one. ").bold = True
    p.add_run("Re-weighted to the company's regions and to the bank cards' %.1f%% share of sales (the private-label card, "
              "which the panel does not hold, carried to %.2f%%), the panel says customers paid %.2f%% more than a year "
              "ago, USD %s million against %s. Two things in that figure are not this quarter's net sales. First, the "
              "December custom event: the design studios' and the site's made-to-order orders were %.2f%% of the banner's "
              "spend in the quarter's last eight weeks against %.2f%% a year earlier, and those sofas are delivered, and "
              "recognised, after the quarter. Deposits should end the quarter near USD %s million against %s at the end "
              "of October, which takes %.2f points off growth. Second, last year's quarter carried USD %s million of "
              "wholesale, a hotel contract the panel never sees; at its run rate of USD %s million this year, applying "
              "the panel's growth to all of last year's net sales overstates the quarter by %.2f points."
              % (F["bank_target_pct"], F["pl_target_pct"], F["payments_growth_pct"], "{:,.1f}".format(F["payments_q4_m"]),
                 "{:,.1f}".format(F["payments_base_m"]), F["mto_share_q4_pct"], F["mto_share_base_pct"],
                 "{:,.1f}".format(F["deposits_q4_m"]), "{:,.1f}".format(F["deposits_q3_m"]), -br["revenue on delivery"],
                 "{:,.1f}".format(F["wholesale_base_m"]), "{:,.1f}".format(F["wholesale_q4_m"]),
                 -br["wholesale at its run rate"]))

    p = doc.add_paragraph()
    p.add_run("How the range has held. ").bold = True
    e = F["errors_pp"]
    p.add_run("Built the same way at each of the %d quarters from %s to %s, on what was known three weeks before each "
              "release, the estimate missed reported growth by %.2f points (root mean square) and %d of the %d quarters "
              "fell inside their ranges; the largest miss, %.2f points, was last year's fourth quarter, when the hotel "
              "contract could not have been foreseen. Taking net sales as what the panel shows, with no deposits and no "
              "wholesale, would have missed by %.2f points and now reads USD %s million."
              % (F["origins"], _q(F["first_origin"]).lower(), _q(F["last_origin"]).lower(), F["golden_rmse_pp"],
                 F["coverage_in"], F["origins"], e["FY2024 Q4"], F["shortcut_rmse_pp"]["careful"],
                 "{:,.1f}".format(F["shortcut_m"]["careful"])))

    hi = F["family_high_m"]
    p = doc.add_paragraph()
    p.add_run("What would change it. ").bold = True
    p.add_run("The other reasonable choices (the private-label rules, the fiscal 2023 or rolled-forward regional mix, a "
              "seven- or nine-week deposit window, wholesale at a four-quarter run rate, the chain calibrated by "
              "regression) put the top of the range between USD %s and %s million; none reaches the street. A second "
              "hotel contract in the quarter, or custom orders delivered far faster than usual, would; neither shows in "
              "anything filed so far."
              % ("{:,.1f}".format(min(hi.values())), "{:,.1f}".format(max(hi.values()))))
    fp = sec.footer.paragraphs[0]
    fp.text = "Larkhill Partners  |  Research  |  Internal"
    for r_ in fp.runs:
        r_.font.size = Pt(8)
        r_.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    doc.core_properties.author = "Audrey Hanson"
    doc.save(path)
