"""Kraanvogel's own documents and finance's workbook: schedule B of the 2027 licence agreement with the publishers'
foundation, the growth planning guideline, the 2027 price list, the agency's quote for the spring 2027 campaign, and
finance's monthly KPI report. The PDFs are Word documents exported by LibreOffice Writer through the house writer;
the workbook passes through the house workbook writer with its owner's stamps."""
import datetime as dt
import os
import sys

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

ORG = "Kraanvogel Luisterboeken B.V."
CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))

FILES = {
    "schB": "SUL_licence_agreement_2027-2029_schedule_B.pdf",
    "guide": "growth_planning_guideline_2026-10.pdf",
    "price": "price_list_2027.pdf",
    "quote": "spring_campaign_2027_quote_Bureau_Grauwe_Gans.pdf",
    "kpi": "kpi_monthly_report_2026-09.xlsx",
}


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.3, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.8, leading=16.2,
                        spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.4,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=7.9, leading=10.4, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


def _doc(path, title, sections, meta, header_rows, author, subject, footer, created, modified, widths=None):
    body, h1, h2, small, cell = _styles()
    story = [Paragraph(title, h1), _grid(header_rows, [44 * 2.83, 118 * 2.83], cell), Spacer(1, 6)]
    for head, paras in sections:
        story.append(Paragraph(head, h2))
        for p in paras:
            if isinstance(p, list):
                n = len(p[0])
                w = widths or {2: [60, 100], 3: [52, 56, 52], 4: [40, 40, 40, 40], 5: [34, 30, 32, 32, 32]}[n]
                story.append(_grid(p, [x * 2.83 for x in w], cell))
            else:
                story.append(Paragraph(p, body))
    if meta:
        story.append(Spacer(1, 8))
        story.append(Paragraph(meta, small))
    O.build(path, story, title=title, author=author, subject=subject, footer=footer, created=created,
            modified=modified, font="Liberation Sans")


SCHEDULE_B = [
    ("B1. Term and what this schedule replaces", [
        "This schedule sets the remuneration Kraanvogel pays the publishers represented by the Stichting "
        "Uitgeverslicenties Luisterboek (SUL) for their audiobooks from 1 January 2027 to 31 December 2029. It "
        "replaces schedule B of the 2024 agreement, under which Kraanvogel paid each month 52 per cent of its net "
        "subscription revenue, divided among the publishers in proportion to the seconds of their titles streamed "
        "in the month."]),
    ("B2. Remuneration from 1 January 2027", [
        "B2.1 For each month Kraanvogel pays each publisher EUR 0.40 for every counted hour of the publisher's "
        "titles in the month.",
        "B2.2 A profile's counted hours of a title in a month are the hours by which the furthest position the "
        "profile has reached in the title, as reported by the app in that month, exceeds the furthest position "
        "reported for that profile and title before the month. Listening again to a part of a title the profile "
        "has already reached adds nothing.",
        "B2.3 A position is counted in the month the app reports it to Kraanvogel.",
        "B2.4 Titles Kraanvogel produces itself and recordings in the public domain are not counted. E-books are "
        "licensed under schedule C."]),
    ("B3. Statements and payment", [
        "B3.1 Kraanvogel sends each publisher a statement of its counted hours and remuneration for each month "
        "by the 15th of the following month and pays within 30 days of the statement.",
        "B3.2 A publisher whose code changes keeps its statements under the new code from the month of the change."]),
    ("B4. Audit", [
        "B4.1 SUL may have Kraanvogel's counting audited once a year by an auditor of its choice, at its own cost "
        "unless the audit finds counted hours understated by more than 2 per cent in any month."]),
]

GUIDELINE = [
    ("1. Scope", [
        "This guideline sets the figures Kraanvogel's growth and finance teams use to plan and judge acquisition "
        "campaigns. It binds growth, finance and the agencies' briefs."]),
    ("3. Planning figures", [
        "3.1 A paying subscription is a consumer account whose monthly charge for the billing month covering the "
        "date was collected. Staff and test accounts are not consumer accounts. A charge returned and not "
        "re-presented, or refunded, is not collected. The paying subscriptions on a plan at a month end are the "
        "accounts paying on the month's last day, on the plan charged.",
        "3.2 A paying subscription-month is a consumer account's calendar month in which its monthly charge was "
        "collected, on the plan charged.",
        "3.3 An account's counted hours in a month are the counted hours (licence agreement, schedule B) of the "
        "profiles that belonged to the account in that month.",
        "3.5 Net revenue is what Kraanvogel keeps of the charges collected: the charge less VAT, less the app "
        "store's fee on a store subscription (Apple 30 per cent of the price net of VAT in a subscription's first "
        "12 paid months and 15 per cent after; Google 15 per cent), less refunds.",
        "3.8 Forecasts use the licence agreement in force in the forecast months, the current price list including "
        "the changes it announces, and the rivals' prices as last scanned, and assume no other change of terms or "
        "prices.",
        "3.9 A subscription's contribution in a period is its net revenue in the period less the remuneration on "
        "its account's counted hours in the period at the licence agreement's rate.",
        "3.10 A January price rise goes ahead on a plan when it raises the 2027 contribution of the subscriptions "
        "paying on that plan at 31 October 2026, followed through 2027, against holding the plan's 2026 price. "
        "A rise's extra cancellations and extra downgrades are those at a subscription's first bill at the new "
        "price beyond what the same months would have brought without the rise, counted among the subscriptions "
        "that reach that bill."]),
]


def write_pdfs(folder):
    _doc(os.path.join(folder, FILES["schB"]),
         "Licence agreement 2027 to 2029: Schedule B, remuneration",
         SCHEDULE_B, "Agreed on 24 September 2026 between Kraanvogel Luisterboeken B.V., Utrecht, and Stichting "
         "Uitgeverslicenties Luisterboek, Amsterdam. Schedules A (licensed titles), C (e-books) and D (data) are "
         "issued separately.",
         [["Parties", "Kraanvogel Luisterboeken B.V.; Stichting Uitgeverslicenties Luisterboek (SUL)"],
          ["In force", "1 January 2027"], ["Reference", "SUL-KRV-2027 / B"]],
         "Kraanvogel Luisterboeken B.V., legal", "Schedule B, remuneration", "SUL-KRV-2027 schedule B",
         dt.datetime(2026, 9, 22, 10, 4, tzinfo=CEST), dt.datetime(2026, 9, 24, 15, 31, tzinfo=CEST))
    _doc(os.path.join(folder, FILES["guide"]),
         "Growth planning guideline, version 3",
         GUIDELINE, "Version 3 replaces version 2 (February 2025): 3.3 and 3.9 take the remuneration of the 2027 "
         "licence agreement; 3.10 sets how a January price rise is judged. Owner: finance controller.",
         [["Owner", "Finance (controller)"], ["Approved", "6 October 2026, management team"],
          ["Applies to", "Acquisition campaigns and price changes from January 2027"]],
         "Kraanvogel Luisterboeken B.V., finance", "Growth planning guideline", "Growth planning guideline v3",
         dt.datetime(2026, 10, 1, 9, 12, tzinfo=CEST), dt.datetime(2026, 10, 6, 16, 48, tzinfo=CEST))
    rows = [["Plan", "Listening", "Profiles", "Per month from 1 January 2027 (NL and BE, VAT included)"]]
    for pl, lis, prof in [("FLEX", "10 hours a month", "1"), ("STD", "30 hours a month", "1"),
                          ("ONB", "unlimited", "up to 2"), ("GEZ", "unlimited", "up to 4")]:
        rows.append([P.PLAN_NAME[pl], lis, prof, "EUR %.2f" % P.PRICE27[pl]])
    _doc(os.path.join(folder, FILES["price"]), "Price list from 1 January 2027",
         [("Subscriptions", [rows, "Prices until 31 December 2026: Flex EUR 9.99, Standaard EUR 14.99, Onbeperkt "
           "EUR 18.99, Gezin EUR 22.99, in the Netherlands and in Flanders. Existing subscriptions move to the new "
           "price at their first billing date in 2027; subscribers are told by e-mail on 1 December 2026. A rise "
           "may still be withdrawn for a plan until 30 November 2026.",
           "Listening hours that are not used do not carry over to the next month. In the app stores the price is "
           "the store's nearest price point."]),
          ("Earlier price changes", [
              "1 January 2025, in Flanders: Standaard from EUR %.2f to EUR %.2f and Onbeperkt from EUR %.2f to EUR %.2f; "
              "in the Netherlands: Flex from EUR %.2f to EUR %.2f and Gezin from EUR %.2f to EUR %.2f. Subscribers were "
              "told by e-mail on 1 December 2024." % (P.PRICE0["STD"], P.PRICE["STD"], P.PRICE0["ONB"], P.PRICE["ONB"],
                                                     P.PRICE0["FLEX"], P.PRICE["FLEX"], P.PRICE0["GEZ"], P.PRICE["GEZ"]),
              "1 January 2026, in the Netherlands: Standaard and Onbeperkt; in Flanders: Flex and Gezin; each to the "
              "price above. Subscribers were told by e-mail on 1 December 2025.",
              "Before 2025 the prices had not changed since 2022."])],
         "", [["Issued", "28 October 2026"], ["Valid from", "1 January 2027"]],
         "Kraanvogel Luisterboeken B.V., commercial", "Price list 2027", "Price list 2027",
         dt.datetime(2026, 10, 27, 14, 20, tzinfo=CET), dt.datetime(2026, 10, 28, 9, 2, tzinfo=CET),
         widths=[44, 38, 24, 56])
    q = [["Lead plan on the landing pages", "Fee per trial start", "Trial"]]
    for pl in P.PLANS:
        q.append([P.PLAN_NAME[pl], "EUR %.2f" % P.FEE27[pl], "30 days free"])
    _doc(os.path.join(folder, FILES["quote"]), "Quote: Kraanvogel spring campaign 2027",
         [("What we quote", ["Paid social, search and podcast placements from 4 January to 28 March 2027, with "
                             "landing pages that lead with one plan. We charge per trial start: an account that "
                             "starts the 30-day trial through the campaign's links. A trial started from an account "
                             "that has held a subscription before is not charged.", q]),
          ("Volume and terms", ["We plan for about 1,800 trial starts over the twelve weeks whichever plan the "
                                "pages lead with. Fees are invoiced monthly on the trial starts Kraanvogel's "
                                "billing system records; this quote is valid until 30 November 2026."])],
         "Bureau Grauwe Gans, Haarlem. Ref. GG-2611-KRV.",
         [["To", "Kraanvogel Luisterboeken B.V., growth"], ["Date", "10 November 2026"]],
         "Bureau Grauwe Gans", "Quote spring campaign 2027", "GG-2611-KRV",
         dt.datetime(2026, 11, 9, 16, 40, tzinfo=CET), dt.datetime(2026, 11, 10, 11, 25, tzinfo=CET))


def write_kpi(path, kpi):
    """Finance's monthly KPI report, January to September 2026."""
    wb = Workbook()
    ws = wb.active
    ws.title = "KPI 2026"
    ws["A1"] = "Kraanvogel Luisterboeken, monthly KPI report 2026 (to September)"
    ws["A1"].font = Font(bold=True, size=12)
    head = ["Month", "Paying Flex", "Paying Standaard", "Paying Onbeperkt", "Paying Gezin", "Paying total",
            "Trial starts", "Net subscription revenue (EUR)", "Publisher remuneration (EUR)"]
    for j, h in enumerate(head, 1):
        c = ws.cell(row=3, column=j, value=h)
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True)
    for i, r in enumerate(kpi, 4):
        for j, v in enumerate(r, 1):
            c = ws.cell(row=i, column=j, value=v)
            if j >= 8:
                c.number_format = "#,##0.00"
    for col, w in zip("ABCDEFGHI", [10, 11, 13, 13, 11, 11, 11, 18, 18]):
        ws.column_dimensions[col].width = w
    ws.cell(row=len(kpi) + 5, column=1, value="Paying: the monthly charge for the billing month covering the "
            "month's last day collected (growth planning guideline 3.1). Remuneration as stated to SUL.")
    wb.save(path)
