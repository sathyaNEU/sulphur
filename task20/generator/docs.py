"""The documents of target/: the hedging policy (Word), the liquidity standard, NEX Clearing's public margin summary and
the regulation licence extract (PDFs written through the house office writer), and the budget workbook. Documents
describe the business and the rules it set itself; none describes how the desk, the plants, the customers or the
clearing house actually behave."""
import datetime as dt
import os
from zoneinfo import ZoneInfo

from docx import Document
from docx.shared import Pt, Mm
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Spacer, Table

import officepdf as O
import sim as S

OSL = ZoneInfo("Europe/Oslo")
F_POLICY = "hk_hedging_policy_2025.docx"
F_STANDARD = "hk_liquidity_standard_2026.pdf"
F_NEXDOC = "nex_clearing_margin_summary.pdf"
F_LICENCE = "hallingvass_regulation_licence_extract.pdf"
F_BUDGET = "hk_budget_vintages_2016_2026.xlsx"
F_CONTRACTS = "hk_supply_contracts_register.xlsx"


def _st():
    body = ParagraphStyle("body", fontName="Helvetica", fontSize=9.4, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=13, leading=17, spaceAfter=6)
    h2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.2, leading=14, spaceBefore=6, spaceAfter=3)
    small = ParagraphStyle("small", fontName="Helvetica", fontSize=8.0, leading=10.5)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=11)
    return body, h1, h2, small, cell


def policy(path):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)

    def h(t, lvl=1):
        doc.add_heading(t, level=lvl)

    def p(t):
        doc.add_paragraph(t)
    doc.add_heading("Hallingvass Kraft AS: Hedging policy for power sales", 0)
    p("Approved by the board on 11 December 2024, in force from 1 January 2025. Owner: Head of Trading. Replaces the "
      "policy of 2021.")
    h("1. Purpose")
    p("The policy sets how much of each year's expected generation the company sells forward at a fixed price, so that "
      "revenue in the coming years is less exposed to the system price, and who may do so on the company's behalf.")
    h("2. Hedge ratio")
    p("The hedge ratio of a delivery year is the share of that year's budgeted generation that has been sold forward "
      "at a fixed price. Budgeted generation is the figure in the budget approved in October before the delivery year "
      "or, for later years, the latest long-range budget.")
    h("3. Limits")
    p("The hedge ratio of each delivery year must stay between the minimum and the maximum below, read at the time "
      "left until the delivery year starts. Between the points in the table the limits move in a straight line.")
    t = doc.add_table(rows=1, cols=3)
    t.style = "Table Grid"
    hdr = t.rows[0].cells
    hdr[0].text, hdr[1].text, hdr[2].text = "Time to the start of the delivery year", "Minimum", "Maximum"
    for tau, lo, hi in S.P["ladder"]:
        r = t.add_row().cells
        r[0].text = "%d months" % int(round(12 * tau)) if tau > 0 else "Delivery year started"
        r[1].text = "%d per cent" % round(100 * lo)
        r[2].text = "%d per cent" % round(100 * hi)
    p("")
    p("Within the limits the Head of Trading decides the pace and timing of sales. The desk reports the hedge ratio of "
      "each delivery year to the CFO every Monday.")
    h("4. Instruments and counterparties")
    p("Exchange-traded base-load futures on the Nordvik Energy Exchange, cleared at NEX Clearing, are the standard "
      "instrument. Bilateral sales at a fixed price require the CFO's approval. Options and profile products are not "
      "permitted.")
    h("5. Authority")
    p("The Head of Trading and the traders named in the trading mandate may enter trades within the limits. A breach "
      "of a limit is reported to the CFO the same day and corrected within ten business days.")
    h("6. Review")
    p("The policy is reviewed every second year or after any year in which variation margin paid exceeded EUR 100 "
      "million.")
    doc.save(path)


def standard(path):
    body, h1, h2, small, cell = _st()
    s = [Paragraph("Hallingvass Kraft AS", small),
         Paragraph("Liquidity standard: committed margin facility", h1),
         Paragraph("Approved by the board on 9 December 2025. Owner: Treasurer. This standard sets how large the "
                   "committed facility that funds the hedge program's cash needs at NEX Clearing and in the day-ahead "
                   "market must be for each calendar year.", body),
         Paragraph("1. Requirement", h2),
         Paragraph("The facility committed for a calendar year must be at least the stress requirement for that year, "
                   "rounded up to the next EUR 50 million.", body),
         Paragraph("2. Stress requirement", h2),
         Paragraph("The stress requirement is the largest cumulative net cash outflow of the hedge program during the "
                   "year, counted from the year's first business day, in a year whose market prices and inflows repeat "
                   "those of 2022. Treasury builds that year from the company's own records as set out in the annex.",
                   body),
         Paragraph("3. Net cash outflow", h2),
         Paragraph("Net cash outflow is variation margin, delivery settlement and changes in initial margin paid to "
                   "NEX Clearing, plus day-ahead purchases less day-ahead sales, less payments received from supply "
                   "customers, each counted on the day the cash moves. Interest, fees, taxes and operating costs are "
                   "left out.", body),
         Paragraph("4. Review", h2),
         Paragraph("Treasury computes the requirement each December for the coming year and again whenever the hedge "
                   "book, the supply contracts or NEX Clearing's margin practice change materially. The facility "
                   "committed for 2026 is EUR 150 million.", body),
         Spacer(1, 6),
         Paragraph("Annex. Building the stress year", h2),
         Paragraph("(a) Every delivery month's forward price on the risk system's daily curve moves on each business "
                   "day by the percentage the forward for the same calendar month moved on the corresponding day of "
                   "2022 (the same date in 2022, or the latest 2022 business day before it), starting from the curve "
                   "of the last business day of the previous year.", body),
         Paragraph("(b) The system price of each calendar day is the stress curve's forward for the next delivery "
                   "month on that day (the latest business day's curve) times the ratio of the 2022 system price of "
                   "the corresponding date to the 2022 curve's forward for the next delivery month on that date.", body),
         Paragraph("(c) Each week's inflow is the normal inflow for that week times the ratio of the 2022 inflow of "
                   "the same ISO week to its normal.", body),
         Paragraph("(d) Everything else runs as it runs in practice: the trading desk's hedging, the plants' operation "
                   "within the regulation licence, the supply contracts and NEX Clearing's margining.", body),
         Spacer(1, 8),
         Paragraph("Hallingvass Kraft AS, Treasury. Internal.", small)]
    O.build(path, s, "Liquidity standard: committed margin facility", "Jorunn Solberg", "Liquidity standard",
            "Hallingvass Kraft AS  |  Treasury  |  Internal", dt.datetime(2025, 12, 9, 14, 12, 40, tzinfo=OSL),
            dt.datetime(2025, 12, 9, 14, 31, 5, tzinfo=OSL))


def nexdoc(path):
    body, h1, h2, small, cell = _st()
    s = [Paragraph("NEX Clearing", small),
         Paragraph("Margining of Nordic base-load futures: summary for clearing members", h1),
         Paragraph("This summary describes how NEX Clearing margins the base-load futures listed on the Nordvik Energy "
                   "Exchange. The clearing rules and the clearing notices prevail over it.", body),
         Paragraph("Products and cascading", h2),
         Paragraph("Base Year futures cascade at expiry into the four Base Quarter futures of the year, and Base "
                   "Quarter futures cascade into the three Base Month futures of the quarter. A month future's "
                   "delivery period is settled day by day against the system price.", body),
         Paragraph("Variation margin and delivery settlement", h2),
         Paragraph("Open positions are marked to the daily settlement price, and the change is paid or received on "
                   "the same business day. Each delivery day of a position in delivery is settled against that day's "
                   "system price on the next business day, at the position's last settlement price before delivery.",
                   body),
         Paragraph("Initial margin", h2),
         Paragraph("Initial margin is the energy of each open position not yet settled times the margin rate of the "
                   "product class in which the position is held after cascading (Base Month, Base Quarter or Base "
                   "Year). Positions in delivery are margined in the Base Month class on their remaining days. Margin "
                   "rates are set by NEX Clearing's risk function from the observed behaviour of settlement prices and "
                   "are published in clearing notices with the date from which they apply.", body),
         Paragraph("Collateral", h2),
         Paragraph("Margin is called in euro cash. Members may not post securities or bank guarantees against the "
                   "Nordic power margin pool.", body),
         Spacer(1, 8),
         Paragraph("NEX Clearing, Risk. Public.", small)]
    O.build(path, s, "Margining of Nordic base-load futures", "NEX Clearing Risk", "Margin summary",
            "NEX Clearing  |  Public", dt.datetime(2023, 3, 1, 9, 15, 0, tzinfo=OSL),
            dt.datetime(2023, 3, 1, 9, 22, 41, tzinfo=OSL), producer="LibreOffice 7.5")


def licence(path):
    body, h1, h2, small, cell = _st()
    s = [Paragraph("Extract from the regulation licence for the Hallingvass reservoirs", h1),
         Paragraph("Granted by royal decree of 14 June 1974, amended 2 March 2018. Extract made by Hallingvass Kraft AS "
                   "for internal use; the licence in full prevails.", small),
         Paragraph("Section 3. Regulation limits", h2),
         Paragraph("The reservoirs may be regulated between the lowest and highest regulated water levels stated in "
                   "the annex. Together they hold 2,600 GWh of stored energy at the highest regulated level.", body),
         Paragraph("Section 4. Minimum storage", h2),
         Paragraph("Stored energy in the regulated reservoirs shall not be drawn below %d GWh at any time of the " % S.P["res_floor"] +
                   "year, so that the minimum flows in Section 5 can be released through a dry winter.", body),
         Paragraph("Section 5. Minimum flows", h2),
         Paragraph("Below the main dam at least 1.2 cubic metres a second shall be released from 1 May to 30 September "
                   "and 0.6 cubic metres a second for the rest of the year.", body),
         Paragraph("Section 9. Reporting", h2),
         Paragraph("The licensee reports weekly storage and inflow to the regulator and publishes them with the "
                   "normal (median) values for each week.", body)]
    O.build(path, s, "Regulation licence extract", "Hallingvass Kraft AS", "Licence extract",
            "Hallingvass Kraft AS  |  Production", dt.datetime(2018, 3, 20, 10, 5, 0, tzinfo=OSL),
            dt.datetime(2018, 3, 20, 10, 9, 33, tzinfo=OSL), producer="LibreOffice 6.0")


def budget(path, W):
    wb = Workbook()
    ws = wb.active
    ws.title = "Budget vintages"
    ws.append(["Budget approved", "Delivery year", "Budget price (EUR/MWh)", "Budgeted generation (GWh)"])
    for c in ws[1]:
        c.font = Font(bold=True)
    for set_on, y, px, gen in sorted(W.bud, key=lambda x: (x[0], x[1])):
        if set_on.year < 2016:
            continue
        ws.append([set_on if set_on.year >= 2017 else dt.date(2016, 10, 3), y, round(px, 2), round(gen / 1e3)])
    for row in ws.iter_rows(min_row=2, max_col=1):
        for c in row:
            c.number_format = "yyyy-mm-dd"
    ws.column_dimensions["A"].width = 16
    ws.column_dimensions["B"].width = 13
    ws.column_dimensions["C"].width = 22
    ws.column_dimensions["D"].width = 26
    wb.save(path)


def contracts(path):
    wb = Workbook()
    ws = wb.active
    ws.title = "Supply contracts"
    ws.append(["Customer", "Contract", "Start", "End", "Volume", "Price basis", "Invoicing", "Payment terms"])
    for c in ws[1]:
        c.font = Font(bold=True)
    ws.append(["Fjordal Aluminium AS", "FA-2019-01", dt.date(2020, 1, 1), dt.date(2029, 12, 31), "%d MW base load" % S.P["smelter_mw"],
               "EUR %.2f/MWh for the whole term" % S.P["smelter_px"][2025], "Monthly in arrears", "30 days from invoice"])
    ws.append(["Nesbyen Treforedling AS", "NT-2016-03", dt.date(2016, 7, 1), "Evergreen, 12 months' notice",
               "%d MW base load" % S.P["pulp_mw"], "Monthly average system price", "Monthly in arrears", "30 days from invoice"])
    ws.append(["Hallingvass Straum AS", "Group supply", dt.date(2012, 1, 1), "Evergreen",
               "{:,.0f} GWh a year on the retail load profile".format(S.P["affiliate_gwh"]), "Group transfer price", "Monthly in arrears",
               "30 days from invoice"])
    ws.append(["Bygdenett AS", "BN-2018-07", dt.date(2018, 1, 1), dt.date(2028, 12, 31),
               "Grid losses, {:,.0f} GWh a year on the losses profile".format(S.P["grid_gwh"]), "Monthly average system price",
               "Monthly in arrears", "30 days from invoice"])
    for row in ws.iter_rows(min_row=2):
        for c in row[2:4]:
            if isinstance(c.value, dt.date):
                c.number_format = "yyyy-mm-dd"
    for col, wd in zip("ABCDEFGH", (26, 14, 12, 26, 40, 32, 20, 22)):
        ws.column_dimensions[col].width = wd
    prof = wb.create_sheet("Profiles")
    prof.append(["Month", "Retail load (share of year)", "Grid losses (share of year)"])
    for c in prof[1]:
        c.font = Font(bold=True)
    for m in range(12):
        prof.append([m + 1, round(float(S.RETAIL_SHAPE[m] / S.RETAIL_SHAPE.sum()), 5),
                     round(float(S.LOSS_SHAPE[m] / S.LOSS_SHAPE.sum()), 5)])
    wb.save(path)


def write_all(tgt, W):
    contracts(os.path.join(tgt, F_CONTRACTS))
    policy(os.path.join(tgt, F_POLICY))
    standard(os.path.join(tgt, F_STANDARD))
    nexdoc(os.path.join(tgt, F_NEXDOC))
    licence(os.path.join(tgt, F_LICENCE))
    budget(os.path.join(tgt, F_BUDGET), W)
