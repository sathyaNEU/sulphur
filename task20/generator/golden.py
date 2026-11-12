"""task20 architecture 2 golden deliverables (second hardening): the desk's nowcast workbook and the one-page note to the investment
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
    rows = [("Fourth quarter fiscal 2024 net sales (USD m)", F["base_net_sales_m"], "#,##0.0"),
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
    n = len(F["bridge_pp"]) + 3
    b.cell(row=n, column=1, value="Steps applied in the order listed; each worth is the change in year-on-year growth "
                                  "(weekly averages) when the step is added. The panel's steps are at the panel's own "
                                  "regional weights with KS-01 kept; from the regional mix on, at the company's.")
    _widths(b, [58, 22, 24])

    g = wb.create_sheet("Regions")
    _head(g, 1, ["Billing region", "Growth per open card, KS-01 kept (%)", "Growth per open card, KS-01 out (%)",
                 "Panel spend weight, KS-01 out (%)", "Company weight, fiscal 2024 (%)"])
    for i, r in enumerate(REG, 2):
        g.cell(row=i, column=1, value=r)
        g.cell(row=i, column=2, value=F["regional_with_ks01_pct"][r]).number_format = "0.00"
        g.cell(row=i, column=3, value=F["regional_pct"][r]).number_format = "0.00"
        g.cell(row=i, column=4, value=F["panel_weights_pct"][r]).number_format = "0.00"
        g.cell(row=i, column=5, value=F["company_weights_pct"][r]).number_format = "0.00"
    g.cell(row=6, column=1, value="At the panel's weights")
    g.cell(row=6, column=2, value=F["pooled_with_ks01_pct"]).number_format = "0.00"
    g.cell(row=6, column=3, value=F["pooled_growth_pct"]).number_format = "0.00"
    g.cell(row=7, column=1, value="At the company's weights")
    g.cell(row=7, column=2, value=F["visible_with_ks01_pct"]).number_format = "0.00"
    g.cell(row=7, column=3, value=F["visible_growth_pct"]).number_format = "0.00"
    g.cell(row=9, column=1, value="Issuers reporting in every week of both quarters: %s. KS-01 is set aside: its cards "
                                  "took a block of re-issued accounts in October 2025 (sheet Issuers). Company weights "
                                  "from the 10-K's Brindle & Moss net sales by region, fiscal 2024."
                                  % ", ".join(F["issuers_both"]))
    _widths(g, [26, 24, 24, 22, 22])

    iu = wb.create_sheet("Issuers")
    _head(iu, 1, ["Week beginning", "KS-01 Midwest panel cards"])
    cs = A.card_series(R["P"])[("KS-01", "Midwest")]
    sel = cs[(cs.index >= A.pd.Timestamp("2025-08-31")) & (cs.index <= A.pd.Timestamp("2025-11-30"))]
    for i, (wk, v) in enumerate(sel.items(), 2):
        iu.cell(row=i, column=1, value=wk.date().isoformat())
        iu.cell(row=i, column=2, value=int(round(float(v)))).number_format = "#,##0"
    n = len(sel) + 3
    notes = [("KS-01 Midwest cards, 28 September to 26 October 2025 (%)", F["ks01_mw_cards_rise_pct"], "0.00"),
             ("KS-02 Southeast cards, 23 April to 21 May 2023 (%)", F["ks02_se_rise_pct"], "0.00"),
             ("KS-01's book taken out, points of growth at the company's mix",
              dict(F["bridge_pp"])["KS-01's re-issued book taken out"], "0.00")]
    for i, (k, v, fmt) in enumerate(notes, n):
        iu.cell(row=i, column=1, value=k)
        iu.cell(row=i, column=2, value=v).number_format = fmt
    iu.cell(row=n + 4, column=1, value="Card accounts open on an issuer's file move by about one per cent a month; a "
                                       "rise of more than 5 per cent in four weeks is a book of accounts re-issued under "
                                       "the issuer's codes. KS-01's came as KS-06's cards fell and KS-06's feed ended; the "
                                       "accounts are labelled 2025 but spend like long-held cards, and spend per card in "
                                       "KS-01's Midwest rose with them. An issuer with such a book between the two "
                                       "quarters is left out of the comparison (KS-01 here, KS-02 in the record's "
                                       "fiscal 2023 to 2024 quarters).")
    _widths(iu, [62, 26])

    dp = wb.create_sheet("Deposits")
    _head(dp, 1, ["Fiscal quarter end", "Customer deposits (USD m)", "Deposits in weeks of the brand's payments"])
    P = R["P"]
    ks = [k for k in P["keys"][:-1] if k >= "FY2023 Q1"]
    for i, k in enumerate(ks, 2):
        dp.cell(row=i, column=1, value=_q(k))
        dp.cell(row=i, column=2, value=F["deposits_by_q"][k]).number_format = "#,##0.0"
        dp.cell(row=i, column=3, value=F["deposit_weeks"][k]).number_format = "0.00"
    n = len(ks) + 3
    rows = [("Custom-order share of the brand's panel spend, last eight weeks of Q4 fiscal 2024 (%)", F["custom_base_pct"], "0.00"),
            ("Custom-order share, last eight weeks of Q4 fiscal 2025 (%)", F["custom_q4_pct"], "0.00"),
            ("Share of the quarter's panel spend in its last eight weeks, Q4 fiscal 2024 (%)", F["trail_base_pct"], "0.00"),
            ("Share of the quarter's panel spend in its last eight weeks, Q4 fiscal 2025 (%)", F["trail_q4_pct"], "0.00"),
            ("Customer deposits, end of Q4 fiscal 2024 (USD m)", F["deposits_base_m"], "#,##0.0"),
            ("Customer deposits, end of Q3 fiscal 2025 (USD m)", F["deposits_q3_m"], "#,##0.0"),
            ("Customer deposits, end of Q4 fiscal 2025, estimated (USD m)", F["deposits_q4_m"], "#,##0.0"),
            ("Change in deposits in Q4 fiscal 2025 (USD m)", F["deposit_change_m"], "#,##0.0"),
            ("Change in deposits in Q4 fiscal 2024 (USD m)", F["deposit_change_base_m"], "#,##0.0"),
            ("Customer payments, retail, Q4 fiscal 2024 (USD m)", F["payments_base_m"], "#,##0.0"),
            ("Customer payments, retail, Q4 fiscal 2025, estimated (USD m)", F["payments_q4_m"], "#,##0.0"),
            ("Retail net sales, Q4 fiscal 2025, estimated (USD m)", F["retail_q4_m"], "#,##0.0")]
    for i, (k, v, fmt) in enumerate(rows, n):
        dp.cell(row=i, column=1, value=k)
        dp.cell(row=i, column=2, value=v).number_format = fmt
    dp.cell(row=n + len(rows) + 1, column=1,
            value="Customers pay when they order; custom pieces are delivered, and recognised, about eight weeks later "
                  "(deposits run near eight weeks of custom orders at each quarter end). Deposits at the quarter's end: "
                  "last year's, scaled by the brand's payments, the share of them in the last eight weeks (the panel's "
                  "weekly profile) and the custom-order share of those weeks (design studios and the site's custom "
                  "orders, descriptor detail). Retail net sales are payments less the quarter's change in deposits.")
    _widths(dp, [76, 22, 26])

    ct = wb.create_sheet("Contract")
    _head(ct, 1, ["Fiscal quarter", "Contract net sales (USD m)"])
    kw = [k for k in P["keys"][:-1] if k >= "FY2023 Q1"]
    for i, k in enumerate(kw, 2):
        ct.cell(row=i, column=1, value=_q(k))
        ct.cell(row=i, column=2, value=F["contract_by_q"][k]).number_format = "#,##0.0"
    n = len(kw) + 3
    rows = [("Fiscal 2024, from the fourth-quarter release (USD m)", F["contract_fy2024_m"]),
            ("First nine months of fiscal 2024, from the third-quarter release (USD m)", F["contract_9m_fy2024_m"]),
            ("Q4 fiscal 2024, the difference (USD m)", F["contract_base_m"]),
            ("Q4 fiscal 2025, run rate: median of the last eight quarters (USD m)", F["contract_q4_m"])]
    for i, (k, v) in enumerate(rows, n):
        ct.cell(row=i, column=1, value=k)
        ct.cell(row=i, column=2, value=v).number_format = "#,##0.0"
    ct.cell(row=n + 5, column=1, value="Fourth quarters are the fiscal year less the first nine months (the fourth-quarter "
                                       "releases give contract for the year only). Contract is invoiced to hotels, offices "
                                       "and senior living operators and is not on the card panel; retail is estimated "
                                       "from the panel and contract added at its run rate.")
    _widths(ct, [70, 26])

    rc = wb.create_sheet("Record")
    _head(rc, 1, ["Fiscal quarter", "Estimate, growth (%)", "Reported growth (%)", "Error (points)", "Inside the 80% range"])
    G = R["golden"]
    band = A.Z80 * G["rmse"]
    for i, q in enumerate(G["origins"], 2):
        e = G["errs"][q]
        rc.cell(row=i, column=1, value=_q(q))
        rc.cell(row=i, column=2, value=F["estimates_pct"][q]).number_format = "0.00"
        rc.cell(row=i, column=3, value=F["reported_pct"][q]).number_format = "0.00"
        rc.cell(row=i, column=4, value=F["errors_pp"][q]).number_format = "0.00"
        rc.cell(row=i, column=5, value="yes" if abs(e) <= band else "no")
    n = len(G["origins"]) + 3
    rc.cell(row=n, column=1, value="Root mean square error (points)")
    rc.cell(row=n, column=2, value=F["golden_rmse_pp"]).number_format = "0.00"
    rc.cell(row=n + 1, column=1, value="Quarters inside the range")
    rc.cell(row=n + 1, column=2, value="%d of %d" % (F["coverage_in"], F["origins"]))
    rc.cell(row=n + 2, column=1, value="Inside a range built only on the errors before each, from %s"
                                       % _q(F["first_asof_origin"]))
    rc.cell(row=n + 2, column=2, value="%d of %d" % (F["coverage_asof_in"], F["coverage_asof_n"]))
    rc.cell(row=n + 4, column=1, value="Each quarter built as it would have been three weeks before its release: the "
                                       "issuers in every week of both quarters less any with a re-issued book between "
                                       "them, the prior fiscal year's regional weights, deposits estimated from the year "
                                       "before, contract at the median of the eight quarters before. Reported growth: "
                                       "weekly averages, Fernhollow out unless in both quarters.")
    rc.cell(row=n + 6, column=1, value="For comparison: issuers in both quarters on spend per open card at the company's "
                                       "mix, net sales grown with it")
    rc.cell(row=n + 7, column=1, value="Root mean square error (points)")
    rc.cell(row=n + 7, column=2, value=F["shortcut_rmse_pp"]["careful"]).number_format = "0.00"
    rc.cell(row=n + 8, column=1, value="Fiscal 2025 Q3 error (points)")
    rc.cell(row=n + 8, column=2, value=F["careful_q3_error_pp"]).number_format = "0.00"
    rc.cell(row=n + 9, column=1, value="Fourth quarter estimate (USD m)")
    rc.cell(row=n + 9, column=2, value=F["shortcut_m"]["careful"]).number_format = "#,##0.0"
    _widths(rc, [44, 20, 20, 16, 20])

    cp = wb.create_sheet("Completion")
    _head(cp, 1, ["Issuer", "Latest week as first delivered (% of final)", "One week back (%)", "Two weeks back (%)"])
    for i, iss in enumerate(sorted(R["cf_last_week"]), 2):
        cp.cell(row=i, column=1, value=iss)
        for j, lag in enumerate((0, 1, 2), 2):
            cp.cell(row=i, column=j, value=round(100 * R["cf"][(iss, lag)], 1)).number_format = "0.0"
    n = len(R["cf_last_week"]) + 3
    cp.cell(row=n, column=1, value="Medians over the delivery history (27 deliveries, 4 August 2025 to 2 February 2026). "
                                   "Completing the quarter's latest weeks lifts its spend by %.2f%%." % F["completion_pct"])
    cp.cell(row=n + 1, column=1, value="Licensed shop-in-shops and cafes: %.2f%% of the brand id's spend in November to "
                                       "January, taken out by month." % F["excluded_share_pct"])
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
    br = dict(F["bridge_pp"])

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

    rg, rk = F["regional_pct"], F["regional_with_ks01_pct"]
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.add_run("Why the panel reads a beat and the quarter is not one. ").bold = True
    p.add_run("Three things in the panel's %.2f%% are not this quarter's net sales. KS-01's Midwest cards rose %.1f%% in "
              "the four weeks to 26 October as KS-06's fell and its feed ended: a block of KS-06's accounts re-issued as "
              "KS-01 cards, labelled 2025 but spending like long-held cards. With them the Midwest reads %+.2f%%; without "
              "KS-01 it reads %+.2f%%, in line with the region's last two years, and the card-visible growth falls to "
              "%.2f%%. Second, custom orders are paid when placed and recognised on delivery about eight weeks later; "
              "the design studios and the site's custom orders were %.2f%% of the brand's spend in the quarter's last "
              "eight weeks against %.2f%% a year earlier (three studios opened this autumn), so deposits should end the "
              "quarter near USD %s million against USD %s million at the end of October, %.2f points off growth. Third, "
              "last year's quarter held USD %s million of contract sales, the fiscal year's USD %s million less the "
              "first nine months' USD %s million; at this year's run rate of USD %s million, applying the panel's growth "
              "to all of last year's net sales overstates the quarter by %.2f points."
              % (F["visible_with_ks01_pct"], F["ks01_mw_cards_rise_pct"], rk["Midwest"], rg["Midwest"],
                 F["visible_growth_pct"], F["custom_q4_pct"], F["custom_base_pct"], "{:,.1f}".format(F["deposits_q4_m"]),
                 "{:,.1f}".format(F["deposits_q3_m"]), -br["revenue on delivery"], "{:,.1f}".format(F["contract_base_m"]),
                 "{:,.1f}".format(F["contract_fy2024_m"]), "{:,.1f}".format(F["contract_9m_fy2024_m"]),
                 "{:,.1f}".format(F["contract_q4_m"]), -br["contract at its run rate"]))

    p = doc.add_paragraph()
    p.add_run("How the range has held. ").bold = True
    p.add_run("Built the same way at each of the %d quarters from %s to %s, on what was known three weeks before each "
              "release (KS-02's own re-issued book left out of the fiscal 2023 to 2024 comparisons), the estimate missed "
              "reported growth by %.2f points (root mean square) and %d of the %d quarters fell inside their ranges; the "
              "largest miss, %.2f points, was %s, when the contract delivery could not have been foreseen. The panel's "
              "growth taken straight to net sales would have missed by %.2f points and now reads USD %s million."
              % (F["origins"], _q(F["first_origin"]).replace("Fiscal", "fiscal"), _q(F["last_origin"]).replace("Fiscal", "fiscal"), F["golden_rmse_pp"],
                 F["coverage_in"], F["origins"], F["largest_miss_pp"], _q(F["largest_miss_q"]).replace("Fiscal", "fiscal"),
                 F["shortcut_rmse_pp"]["careful"], "{:,.1f}".format(F["shortcut_m"]["careful"])))

    hi = F["family_high_m"]
    p = doc.add_paragraph()
    p.add_run("What would change it. ").bold = True
    p.add_run("The other reasonable choices (spend per card issuer by issuer or on cards of the same age, the fiscal 2023 "
              "or rolled-forward regional mix, a seven- or nine-week deposit window, contract at a four-quarter run rate, "
              "a re-issued book read at 3 or 10 per cent, only KS-01's Midwest cards or newest accounts set aside) put "
              "the top of the range between USD %s and %s million; none "
              "reaches the street. A second large contract delivery in the quarter, or custom orders delivered far "
              "faster than usual, would; neither shows in anything filed so far."
              % ("{:,.1f}".format(min(hi.values())), "{:,.1f}".format(max(hi.values()))))
    fp = sec.footer.paragraphs[0]
    fp.text = "Larkhill Partners  |  Research  |  Internal"
    for r_ in fp.runs:
        r_.font.size = Pt(8)
        r_.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    doc.core_properties.author = "Audrey Hanson"
    doc.save(path)
