"""task20 architecture 2 documents: the company's 10-K and 10-Q excerpts the desk keeps (a Word document exported to
PDF by LibreOffice Writer), the panel vendor's client bulletin (a text file), and the desk's own model from the third
quarter (an Excel workbook)."""
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
F_FILING = "bmh_10k_fy2024_10q_q3_fy2025_excerpts.pdf"
F_NOTES = "kestrel_client_bulletin_bmh_2025-11-10.txt"
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


def filing(path, pl, regions, fern_fy2024, acq_date):
    body, h1, h2, small, cell = _styles()
    yrs = list(regions)
    reg_rows = [["USD million"] + ["Fiscal %s" % y[2:] for y in yrs]]
    for j, r in enumerate(W.REGIONS):
        reg_rows.append([r] + [money(regions[y][j]) for y in yrs])
    reg_rows.append(["Brindle & Moss banner"] + [money(sum(regions[y])) for y in yrs])
    reg_rows.append(["Fernhollow"] + ["" for _ in yrs[:-1]] + [money(fern_fy2024)])
    reg_rows.append(["Total net sales"] + [money(sum(regions[y]) + (fern_fy2024 if y == yrs[-1] else 0)) for y in yrs])
    keys = [k for k in W.QKEYS[:-1]]
    pl_rows = [["Fiscal quarter", "Private-label card share of net sales (%)"]]
    for k in keys:
        pl_rows.append([k.replace("FY", "Fiscal ").replace("Q", " Q"), "%.1f" % pl[k]])
    s = [Paragraph("Brindle & Moss, Inc.: research desk copy", small),
         Paragraph("Brindle & Moss, Inc.: excerpts from the Form 10-K for fiscal 2024 and the Form 10-Q for the third "
                   "quarter of fiscal 2025", h1),
         Paragraph("Compiled from the company's filings of 26 March 2025 (10-K) and 10 December 2025 (10-Q). Page "
                   "references omitted.", small),
         Spacer(1, 4),
         Paragraph("Fiscal year", h2),
         Paragraph("Our fiscal year ends on the Saturday closest to January 31. Fiscal 2025 is the 52 weeks ending "
                   "January 31, 2026, and fiscal 2024 was the 52 weeks ended February 1, 2025. Fiscal 2023 was the 53 "
                   "weeks ended February 3, 2024; its fourth quarter had 14 weeks. Each fiscal quarter otherwise has 13 "
                   "weeks.", body),
         Paragraph("Net sales by region", h2),
         Paragraph("We report the net sales of the Brindle & Moss banner by the region of the store or, for online orders, "
                   "the ship-to address. Fernhollow is reported separately from its acquisition.", body),
         _grid(reg_rows, [130] + [80] * len(yrs), cell),
         Spacer(1, 3),
         Paragraph("Acquisition of Fernhollow Outfitters", h2),
         Paragraph("On %s we acquired Fernhollow Outfitters, a specialty retailer of outdoor furniture with 31 stores and "
                   "an online business. Its results are included in our consolidated results from the date of "
                   "acquisition; it contributed net sales of USD %s million in fiscal 2024. The quarterly contribution is "
                   "reported in each Form 10-Q." % (acq_date.strftime("%B %-d, %Y"), money(fern_fy2024)), body),
         Paragraph("Licensed operations", h2),
         Paragraph("Brindle & Moss shop-in-shops in Hollister's department stores and the Brindle Café locations are "
                   "operated by licensees under the Brindle & Moss name. Their sales are not our net sales; we recognize "
                   "the license royalties in other income.", body),
         Paragraph("Tender", h2),
         Paragraph("In fiscal 2024 approximately 67 per cent of net sales were paid with bank-issued credit and debit "
                   "cards, 21 per cent with the Brindle & Moss private-label credit card, which our card program partner "
                   "issues and services, and 12 per cent with cash, checks, consumer financing and other tenders.", body),
         Paragraph("Private-label credit card (Form 10-Q, third quarter of fiscal 2025)", h2),
         Paragraph("Penetration of the private-label card, the share of net sales paid with it, declined in the first "
                   "three quarters of fiscal 2025 after our card program partner tightened approval standards for new "
                   "accounts at the start of the first quarter. Penetration by quarter:", body),
         _grid(pl_rows, [130, 200], cell),
         Spacer(1, 6),
         Paragraph("Source: Brindle & Moss, Inc., Form 10-K for the fiscal year ended February 1, 2025, and Form 10-Q for the "
                   "quarter ended November 1, 2025.", small)]
    O.build(path, s, "Brindle & Moss filing excerpts", "Larkhill Partners research", "BMH 10-K FY2024 and 10-Q Q3 FY2025",
            "Larkhill Partners  |  Research  |  Internal", dt.datetime(2025, 12, 11, 8, 40, 12, tzinfo=EST),
            dt.datetime(2025, 12, 11, 9, 2, 47, tzinfo=EST))


def release_notes(path, joins, leave):
    lines = [
        "KESTREL SPEND PANEL  -  CLIENT BULLETIN",
        "Merchant coverage file: Brindle & Moss (merchant ids M0412, M0413, M2290)",
        "",
        "DELIVERY",
        "Weekly, on Mondays, for fiscal weeks running Sunday to Saturday. Each delivery restates the full history.",
        "Recent weeks are provisional: issuers post late transactions for up to three weeks after a week ends,",
        "and each delivery restates the trailing weeks. A history of the trailing weeks as first delivered is",
        "supplied with each merchant coverage file.",
        "",
        "COVERAGE",
        "The panel holds the general-purpose credit and debit cards (Visa, Mastercard, American Express,",
        "Discover) of its contributing issuers' cardholders in the United States. Store-branded private-label",
        "cards and prepaid cards are not in the panel.",
        "",
        "WHAT EACH ROW CARRIES",
        "Each row is one fiscal week, one contributing issuer, one billing region of the cardholder (Northeast,",
        "Southeast, Midwest, West), one year in which the card accounts were opened at the issuer and one",
        "merchant id. It gives the settled value in US dollars of the panel's card transactions matched to the",
        "merchant, the number of those transactions, and the panel cards open on the issuer's file that week",
        "for that region and opening year.",
        "",
        "MERCHANT MATCHING",
        "Descriptors are matched to merchants by name. A descriptor carrying the merchant's trade name is",
        "rolled into that merchant's id. Monthly spend by raw descriptor is supplied for each merchant id.",
        "",
        "ISSUER CHANGES",
    ]
    for code, d in joins:
        lines.append("%s  first delivered week beginning %s" % (code, d))
    for code, d in leave:
        lines.append("%s  last delivered week beginning %s; the issuer's data agreement ended" % (code, d))
    lines += ["", "Kestrel Spend Panel, client services. A bulletin is sent with each change to the panel."]
    open(path, "w").write("\n".join(lines) + "\n")


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
    f.append(["Back-test RMSE, rolling origins (pp)", round(100 * rmse, 2)])
    f.append([])
    f.append(["Per-card spend: Kestrel spend per open panel card, merchant ids M0412, M0413 and M2290 (from 2 June 2024) "
              "as delivered, issuers in the panel in both quarters, weekly averages."])
    f.append(["Reported growth: net sales per week, Fernhollow taken out unless in both quarters."])
    f.append(["Fit: least squares, fiscal 2022 Q1 to fiscal 2025 Q2. Back-test: from the seventh quarter, each fitted on "
              "the quarters before it."])
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
