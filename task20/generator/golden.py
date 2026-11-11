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
                                       "carried from the quarters reported before it. Reported growth: weekly averages, "
                                       "Fernhollow out unless in both quarters.")
    rc.cell(row=n + 5, column=1, value="For comparison, reported growth regressed on the panel at its own mix")
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
    p.add_run("The panel puts fourth quarter net sales at USD %s million, %.2f%% above last year's USD %s million, with an "
              "80%% range of USD %s to %s million. The street's figure, the mean of %d estimates, is USD %s million "
              "(%.2f%%), USD %.1f million above the top of the range."
              % ("{:,.1f}".format(F["forecast_m"]), F["growth_pct"], "{:,.1f}".format(F["base_net_sales_m"]),
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
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.add_run("Why not the panel's own read. ").bold = True
    p.add_run("On issuers in both years and cards of the same age the panel grew %.2f%%, and reported growth regressed on "
              "it over past quarters gives %.2f%% (USD %s million), a beat. The regression cannot see two things that "
              "moved this quarter. KS-06, a Midwest issuer, left the panel after the week of 26 October, so the cards left "
              "are %.0f%% Southeast and %.0f%% West against the company's %.0f%% and %.0f%%, and those regions grew %.2f%% "
              "and %.2f%% against %.2f%% in the Northeast and %.2f%% in the Midwest; at the company's fiscal 2024 mix the "
              "panel's growth is %.2f%%. And the private-label card, which the panel does not hold, fell from %.1f%% of "
              "net sales a year ago to %.1f%% in the third quarter, a little faster each quarter since the partner "
              "tightened approvals; carried at fiscal 2025's pace it is %.2f%% this quarter, so bank cards pay for %.1f%% "
              "of net sales against %.1f%% a year ago and each dollar the panel sees stands for %.2f%% less net sales "
              "(%.2f points of growth)."
              % (F["pooled_growth_pct"], F["shortcut_pct"]["careful"], "{:,.1f}".format(F["shortcut_m"]["careful"]),
                 pw["Southeast"], pw["West"], cw["Southeast"], cw["West"], rg["Southeast"], rg["West"],
                 rg["Northeast"], rg["Midwest"], F["visible_growth_pct"], F["pl_q4fy24_pct"], F["pl_q3fy25_pct"],
                 F["pl_target_pct"], F["bank_target_pct"], F["bank_q4fy24_pct"], F["drift_less_pct"], F["bridge_pp"][5][1]))

    p = doc.add_paragraph()
    p.add_run("How the range has held. ").bold = True
    e = F["errors_pp"]
    p.add_run("Built the same way at each of the %d quarters from %s to %s, on what was known three weeks before each "
              "release, the estimate missed reported growth by %.2f points (root mean square) and %d of the %d quarters "
              "fell inside their ranges. It ran high in all three quarters of fiscal 2025 (%.2f, %.2f and %.2f points), "
              "so if anything this quarter's figure leans high. The regression on the panel's own mix missed the third "
              "quarter by %.2f points."
              % (F["origins"], _q(F["first_origin"]).lower(), _q(F["last_origin"]).lower(), F["golden_rmse_pp"], F["coverage_in"],
                 F["origins"], e["FY2025 Q1"], e["FY2025 Q2"], e["FY2025 Q3"], F["careful_q3_error_pp"]))

    hi = F["family_high_m"]
    p = doc.add_paragraph()
    p.add_run("What would change it. ").bold = True
    p.add_run("The other reasonable ways to carry the private-label share, the fiscal 2023 regional mix or fiscal 2024's "
              "rolled forward, and the chain calibrated by regression put the top of the range between USD %s and %s "
              "million; none reaches the street. A Midwest or Northeast holiday quarter far stronger than the panel's "
              "cardholders there showed would, and so would a private-label share that stopped falling in November, "
              "which only the release will show."
              % ("{:,.1f}".format(min(hi.values())), "{:,.1f}".format(max(hi.values()))))
    fp = sec.footer.paragraphs[0]
    fp.text = "Larkhill Partners  |  Research  |  Internal"
    for r_ in fp.runs:
        r_.font.size = Pt(8)
        r_.font.color.rgb = RGBColor(0x59, 0x59, 0x59)
    doc.core_properties.author = "Audrey Hanson"
    doc.save(path)
