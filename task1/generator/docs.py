"""The group's own documents: the controlling department's digital subscription KPI standard (version 3), the 2027
digital price list, the digital marketing team's 2027 acquisition plan and finance's monthly KPI workbook. The two
PDFs are Word documents exported by LibreOffice Writer through the house writer; the workbooks pass through the
house workbook writer with their owners' stamps."""
import datetime as dt
import os
import sys

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402

ORG = "Medienhaus Brückenhafen GmbH"
CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


STANDARD = [
    ("1. Scope", [
        "This standard sets the figures the group reports for the digital subscriptions of its four daily titles "
        "(Brückenhafener Rundschau, Grevenauer Anzeiger, Kreisblatt Ostheide, Elmsbacher Nachrichten) and the figures "
        "on which each year's digital acquisition plan is funded. It binds controlling, digital marketing and the "
        "titles' publishing teams."]),
    ("2. Terms", [
        "2.1 A digital subscription is a consumer subscription to a title's digital edition, taken out in the web shop "
        "or through an app store and billed monthly from its start date. Staff access, gift subscriptions, company "
        "licences and accounts kept for testing are not consumer subscriptions.",
        "2.2 A subscription is paying at a date when the billing period that covers the date is charged at a price "
        "above zero. An introductory price counts; a free introductory month does not. The paying digital subscribers "
        "of a title at a month end are its subscriptions paying on the last day of the month.",
        "2.3 A start is a new digital subscription that is not withdrawn within the 14-day withdrawal period. A start "
        "belongs to the acquisition line that brought it in: the title and the marketing channel recorded at the "
        "start. Paywall subscriptions taken out without a campaign belong to the direct channel.",
        "2.4 Net revenue is what the group keeps from the charges collected: the charge less VAT at 7 per cent, less "
        "the app store's fee on a store subscription (Apple: 30 per cent of the price net of VAT in a subscription's "
        "first 12 paid months and 15 per cent after; Google: 15 per cent), less refunds. A debit that is returned and "
        "never collected is not revenue.",
        "2.5 A household is the reader, or the home, that pays for a subscription.",
        "2.6 The 36-month value of a start is the net revenue from the start's household in the 36 months from the "
        "start date: from the start's own subscription and from any later subscription by the same household to the "
        "same title that is billed in those months."]),
    ("3. Planning figures", [
        "3.1 Planning figures are expected values, estimated from the group's own records; a figure per start is the "
        "average over the starts it covers.",
        "3.2 Forecasts use the list prices of the current price list, including changes it announces, and assume no "
        "other change of list prices.",
        "3.3 In a plan, an acquisition line's starts are taken to be like the line's starts of the twelve months to "
        "the last month closed before the plan, at the offer and in the numbers the plan gives the line.",
        "3.4 The extra cancellations a change of list prices brings by a date are the subscriptions that have ended by "
        "that date and would still be running on it without the change."]),
    ("4. Funding the acquisition plan", [
        "4.1 The digital acquisition plan is funded line by line. A line is funded when the expected 36-month value "
        "of its starts is at least 3.5 times its planned cost per start, the plan's spend on the line divided by its "
        "planned starts.",
        "4.2 The acquisition budget is the planned spend of the funded lines. Lines that are not funded do not run.",
        "4.3 The direct channel carries no planned spend and is not a line of the plan."]),
    ("5. Monthly reporting", [
        "5.1 Controlling reports, for each title and month, the paying digital subscribers at the month end and the "
        "month's net revenue from digital subscriptions."]),
]


def standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s, Controlling" % ORG, small),
         Paragraph("Digital subscription KPI standard", h1),
         Paragraph("Version 3, approved by the management board on 20 January 2026. Replaces version 2 (March 2024). "
                   "Owner: head of controlling, Rosa-Maria Herrmann.", small), Spacer(1, 4)]
    for head, paras in STANDARD:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    s.append(Spacer(1, 6))
    s.append(Paragraph("Changes from version 2: section 4 (line-by-line funding at 3.5 times the planned cost per "
                       "start, replacing the single channel budget); 2.4 (the Apple fee after a subscription's first "
                       "12 paid months).", small))
    O.build(path, s, "Digital subscription KPI standard", "Rosa-Maria Herrmann", "Controlling standard",
            "%s · Controlling · Digital subscription KPI standard v3" % ORG,
            dt.datetime(2026, 1, 20, 9, 14, tzinfo=CET), dt.datetime(2026, 1, 20, 9, 41, tzinfo=CET), page_of=True,
            producer="LibreOffice 25.8")


def price_list(path):
    body, h1, h2, small, cell = _styles()
    rows = [["Title", "until 31 March 2025", "from 1 April 2025", "from 1 April 2027"]]
    for t in P.TITLES:
        a, b, c = P.PRICE[t]
        rows.append([P.TITLE_NAME[t]] + [("%.2f €" % x).replace(".", ",") for x in (a, b, c)])
    s = [Paragraph("%s, Vertrieb Digital" % ORG, small),
         Paragraph("Digital subscription list prices", h1),
         Paragraph("Issued 15 September 2026. Monthly list price of the digital edition (web and app), VAT at 7 per "
                   "cent included.", small), Spacer(1, 6),
         _grid(rows, [62 * 2.83, 33 * 2.83, 33 * 2.83, 33 * 2.83], cell), Spacer(1, 8),
         Paragraph("A change of list price applies to a running subscription from its first billing on or after the "
                   "date of the change. Introductory offers are priced as in the offer catalogue; the price after an "
                   "introductory period is the list price in force at that billing.", body),
         Paragraph("App store prices are set in the stores at the nearest store price point.", small)]
    O.build(path, s, "Digital subscription list prices", "Vertrieb Digital", "Price list",
            "%s · Vertrieb Digital · Price list 2027" % ORG,
            dt.datetime(2026, 9, 15, 11, 2, tzinfo=CEST), dt.datetime(2026, 9, 15, 11, 20, tzinfo=CEST))


MONTHS_DE = ["Jan", "Feb", "Mär", "Apr", "Mai", "Jun", "Jul", "Aug", "Sep", "Okt", "Nov", "Dez"]


def plan_spend(plan):
    """The plan's monthly spend by line: planned starts at the planned cost per start, rounded to whole euros."""
    out = {}
    for line, spec in plan.items():
        out[line] = [int(round(n * P.PLAN_CPA[line])) for n in spec["starts"]]
    return out


def media_plan(path, plan):
    wb = Workbook()
    ws = wb.active
    ws.title = "Plan 2027"
    ws["A1"] = "Digital acquisition plan 2027"
    ws["A1"].font = Font(bold=True, size=13)
    ws["A2"] = "Medienhaus Brückenhafen · Digital Marketing · version 2.1 · 28 October 2026"
    head = (["Line", "Channel", "Title", "Offer", "Offer name"] + ["Starts %s" % m for m in MONTHS_DE]
            + ["Starts 2027", "Spend 2027 (EUR)", "Cost per start (EUR)"])
    ws.append([])
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    spend = plan_spend(plan)
    order = sorted(plan, key=lambda l: (P.TITLES.index(l[1]), P.PAID.index(l[0])))
    for k, line in enumerate(order):
        c, t = line
        spec = plan[line]
        st = spec["starts"]
        sp = spend[line]
        r = 5 + k
        ws.append(["%s-%s" % (c, t), P.CH_NAME[c], P.TITLE_NAME[t], spec["offer"], P.OFFERS[spec["offer"]]["name"]]
                  + st + [sum(st), sum(sp), round(sum(sp) / sum(st), 2)])
        ws.cell(r, 19).number_format = "#,##0"
        ws.cell(r, 20).number_format = "0.00"
    last = 4 + len(order)
    ws.append([])
    ws.append(["Total", None, None, None, None] + [None] * 12 + [sum(sum(plan[l]["starts"]) for l in order),
                                                                    sum(sum(spend[l]) for l in order), None])
    ws.cell(last + 2, 19).number_format = "#,##0"
    ws.append([])
    ws.append(["Starts are counted after the 14-day withdrawal period. Spend is media and partner commission at the "
               "planned cost per start; telemarketing is paid per start by the call centre contract."])
    ws.column_dimensions["A"].width = 11
    ws.column_dimensions["B"].width = 20
    ws.column_dimensions["C"].width = 24
    ws.column_dimensions["E"].width = 24
    # the monthly spend, a second sheet the team keeps for the agencies
    w2 = wb.create_sheet("Spend by month")
    w2.append(["Line"] + ["Spend %s (EUR)" % m for m in MONTHS_DE])
    for line in order:
        w2.append(["%s-%s" % line] + spend[line])
    wb.save(path)


def kpi(path, rows):
    """Finance's monthly KPI workbook, January to September 2026."""
    wb = Workbook()
    ws = wb.active
    ws.title = "KPI Digital 2026"
    ws["A1"] = "Digital subscriptions: monthly KPI 2026"
    ws["A1"].font = Font(bold=True, size=12)
    ws["A2"] = "Controlling · prepared 8 October 2026 · per the digital subscription KPI standard v3"
    ws.append([])
    ws.append(["Month"] + ["Paying subscribers %s" % t for t in P.TITLES] + ["Net revenue %s (EUR)" % t
                                                                          for t in P.TITLES])
    for c in ws[4]:
        c.font = Font(bold=True)
    for r in rows:
        ws.append(r)
    for row in ws.iter_rows(min_row=5, min_col=6, max_col=9):
        for c in row:
            c.number_format = "#,##0.00"
    wb.save(path)
