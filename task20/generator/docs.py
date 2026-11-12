"""task20 architecture 2 documents (second hardening): the company's 10-K excerpts the desk keeps (a Word document exported to PDF by
LibreOffice Writer) and the desk's own card model from the third quarter (an Excel workbook)."""
import datetime as dt

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import world as W

EST = dt.timezone(dt.timedelta(hours=-5))
F_FILING = "bmh_10k_fy2024_excerpts.pdf"
F_MODEL = "larkhill_bmh_card_model_q3fy25.xlsx"


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.2, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10, leading=13.4, spaceBefore=7,
                        spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.9, leading=10.4, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.2, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def money(x):
    return "{:,.1f}".format(x)


def filing(path, regions, fern, contract):
    body, h1, h2, small, cell = _styles()
    yrs = list(regions)
    reg_rows = [["USD million"] + ["Fiscal %s" % y[2:] for y in yrs]]
    for j, r in enumerate(W.REGIONS):
        reg_rows.append([r] + [money(regions[y][j]) for y in yrs])
    reg_rows.append(["Brindle & Moss"] + [money(sum(regions[y])) for y in yrs])
    reg_rows.append(["Fernhollow"] + [money(fern[y]) if fern[y] else "" for y in yrs])
    reg_rows.append(["Contract"] + [money(contract[y]) for y in yrs])
    reg_rows.append(["Total net sales"] + [money(sum(regions[y]) + contract[y] + fern[y]) for y in yrs])
    s = [Paragraph("Brindle & Moss, Inc.: research desk copy", small),
         Paragraph("Brindle & Moss, Inc.: excerpts from the Form 10-K for fiscal 2024", h1),
         Paragraph("Filed 26 March 2025. Page references omitted.", small),
         Spacer(1, 4),
         Paragraph("Fiscal year", h2),
         Paragraph("Our fiscal year ends on the Saturday closest to January 31. Fiscal 2024 was the 52 weeks ended "
                   "February 1, 2025, and fiscal 2025 is the 52 weeks ending January 31, 2026. Fiscal 2023 was the 53 "
                   "weeks ended February 3, 2024; its fourth quarter had 14 weeks.", body),
         Paragraph("Business", h2),
         Paragraph("We sell furniture and home furnishings under the Brindle & Moss brand through our stores, our design "
                   "studios, four outlets and brindlemoss.com. Fernhollow Outfitters, acquired in fiscal 2024, sells "
                   "outdoor furniture through 31 stores and fernhollow.com. B&M Contract furnishes hotels, offices and "
                   "senior living communities.", body),
         Paragraph("Brindle & Moss shop-in-shops in Hollister's department stores and the Brindle Cafe locations are "
                   "operated by licensees under the Brindle & Moss name. Their sales are not our net sales; the license "
                   "royalties are recorded in other income.", body),
         Paragraph("Net sales by brand and region", h2),
         Paragraph("Brindle & Moss net sales by region of the store or, for orders shipped from brindlemoss.com, of the "
                   "delivery address:", body),
         _grid(reg_rows, [130] + [80] * len(yrs), cell),
         Spacer(1, 3),
         Paragraph("Acquisition of Fernhollow Outfitters", h2),
         Paragraph("On June 2, 2024 we acquired Fernhollow Outfitters for USD 286 million, funded with cash and a USD 250 "
                   "million term loan. Its results are included in our consolidated results from the date of "
                   "acquisition.", body),
         Spacer(1, 6),
         Paragraph("Source: Brindle & Moss, Inc., Form 10-K for the fiscal year ended February 1, 2025.", small)]
    O.build(path, s, "Brindle & Moss 10-K excerpts", "Larkhill Partners research", "BMH 10-K FY2024",
            "Larkhill Partners  |  Research  |  Internal", dt.datetime(2025, 3, 27, 8, 40, 12, tzinfo=EST),
            dt.datetime(2025, 3, 27, 9, 2, 47, tzinfo=EST))


def model(path, rows, fit, rmse, q3):
    """the desk's third-quarter model: per-active-card growth fitted to reported growth, with its own back-test"""
    wb = Workbook()
    ws = wb.active
    ws.title = "Index"
    ws.append(["Fiscal quarter", "Per-card spend growth, YoY (%)", "Reported net sales growth, comparable basis (%)"])
    for r in rows:
        ws.append(r)
    f = wb.create_sheet("Fit")
    f.append(["Term", "Value"])
    f.append(["Intercept (pp)", round(100 * fit[0], 2)])
    f.append(["Slope", round(fit[1], 3)])
    f.append(["Back-test RMSE (pp)", round(100 * rmse, 2)])
    b = wb.create_sheet("Q3 FY2025 call")
    b.append(["Item", "Value"])
    for k, v in q3:
        b.append([k, v])
    for sh in (ws, f, b):
        for c in sh[1][:3]:
            c.font = Font(bold=True)
            c.fill = PatternFill("solid", fgColor="E2E8F0")
            c.alignment = Alignment(wrap_text=True, vertical="top")
        sh.freeze_panes = "A2"
        for col in sh.columns:
            wmax = max(len(str(c.value)) if c.value is not None and len(str(c.value)) < 60 else 0 for c in col)
            sh.column_dimensions[col[0].column_letter].width = min(max(12, wmax * 1.05), 48)
    wb.save(path)
