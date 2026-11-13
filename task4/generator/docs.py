"""The documents: Wrenfold's keg fleet standard, the Northern Keg Exchange's monthly statements, the keg maker's
quotation and the Maplestead listing agreement. Each office document is a Word document; the PDFs are exported by
LibreOffice Writer through the house writer. Documents describe the business and its terms; none describes a method."""
import datetime as dt
import os
import sys
from collections import defaultdict

from docx import Document
from docx.shared import Pt
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import params as P  # noqa: E402

GMT = dt.timezone(dt.timedelta(hours=0))
BST = dt.timezone(dt.timedelta(hours=1))
MM = 2.835


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=13.0, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.6,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.0, leading=10.4, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=7.8, leading=9.4)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=[w * MM for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


STANDARD = [
    ("1. Scope", [
        "This standard covers the planning of Wrenfold's returnable keg fleet: the 50, 30 and 20 litre stainless "
        "kegs the brewery fills at Brighouse and delivers from its four depots. Casks are planned under the cask "
        "standard (issue 2) and are not covered here."]),
    ("2. Terms", [
        "2.1 The fleet of a size is Wrenfold's own kegs of that size that exist and can still be filled: at Brighouse "
        "(washer yard, cold store, keg repair cage), at a depot or on a depot's lorry, at customers' premises, or "
        "with the Northern Keg Exchange on their way back to Brighouse. A condemned keg, and a keg that will not "
        "come back, is not part of the fleet.",
        "2.2 A keg is lost in the trade when it went out full to a customer and will not come back. The kegs lost in "
        "a period are the net fall in the fleet over the period, other than kegs bought and kegs condemned in it.",
        "2.3 Kegs in circulation are the fleet's kegs other than clean empties standing in the Brighouse washer yard.",
        "2.4 Normal weather is, for each calendar day, the average daily maximum temperature at the Leeds Weather "
        "Centre over 2016 to 2025.",
        "2.5 The season is the 21 weeks from Monday 3 May to Sunday 26 September 2027. A size's busiest week is the "
        "season week, Monday to Sunday, with the most kegs of that size in circulation on average over its seven "
        "days."]),
    ("3. The fleet target", [
        "3.1 The fleet of each size in its busiest week of the season, at normal weather and with every plan the "
        "company has filed for the year, is to cover the kegs of that size in circulation that week and a working "
        "float of clean empties at the washer equal to two days of that size's fills at its average daily rate over "
        "the season (fills run Monday to Saturday).",
        "3.2 The year's keg order is placed with the maker by the third Friday of December and sized so the fleet "
        "meets 3.1. Kegs bought join the fleet when they arrive at Brighouse."]),
    ("4. Records", [
        "4.1 The depot gate counters count kegs through each depot's gate by size: full kegs loaded to the delivery "
        "lorries, and empty kegs unloaded from them.",
        "4.2 The washer log records each shift's kegs presented at the washer and what became of them.",
        "4.3 The keg register lists every keg bought, by serial, with its status.",
        "4.4 The stocktake on 30 November counts every keg on Wrenfold's sites by size and condition.",
        "4.5 Sales representatives count Wrenfold's kegs on site at a sample of customers each quarter.",
        "4.6 Kegs bought since March 2024, and every 20 litre keg, carry an RFID tag read when filled, when delivered "
        "and when presented at the washer."]),
]


def standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph(P.ORG + ", supply chain", small), Paragraph("Keg fleet standard", h1),
         Paragraph("Issue 3, approved by the head of supply chain on 6 October 2026. Replaces issue 2 (January 2024). "
                   "Owner: the keg fleet manager.", small), Spacer(1, 4)]
    for head, paras in STANDARD:
        s.append(Paragraph(head, h2))
        for t in paras:
            s.append(Paragraph(t, body))
    s.append(Paragraph("Revisions", h2))
    s.append(_grid([["Issue", "Date", "Change"],
                    ["1", "March 2021", "first issue"],
                    ["2", "January 2024", "20 litre kegs added"],
                    ["3", "October 2026", "2.4 and 2.5 restated for the 2027 order; 4.6 RFID reads"]],
                   [16, 30, 126], cell))
    O.build(path, s, "Keg fleet standard, issue 3", P.PEOPLE["fleet"], P.ORG + " supply chain",
            "%s. Keg fleet standard, issue 3." % P.ORG,
            dt.datetime(2026, 10, 6, 9, 41, tzinfo=BST), dt.datetime(2026, 10, 6, 10, 3, tzinfo=BST),
            producer="LibreOffice 7.6")


def exchange(path, w):
    body, h1, h2, small, cell = _styles()
    ev = w.ev
    handed = defaultdict(lambda: defaultdict(int))
    for d, pile in ev["exchange_out"]:
        for s, n in pile.items():
            handed[(d.year, d.month)][s] += n
    back = defaultdict(lambda: defaultdict(int))
    for d, kid, s in ev["back_exchange"]:
        back[(d.year, d.month)][s] += 1
    held = defaultdict(lambda: defaultdict(int))
    months = []
    y, m = 2024, 1
    while (y, m) <= (2026, 11):
        months.append((y, m))
        m += 1
        if m == 13:
            y, m = y + 1, 1
    ends = {}
    for (y, m) in months:
        nx = dt.date(y + (m == 12), m % 12 + 1, 1)
        ends[(y, m)] = nx - dt.timedelta(days=1)
    for d, kid, bk in ev["exch_taken"]:
        k = w.kegs[kid]
        arrive = d + dt.timedelta(days=12)
        for ym, e in ends.items():
            if arrive <= e < bk:
                held[ym][k.size] += 1
    s = []
    for i, ym in enumerate(months):
        e = ends[ym]
        part = [Paragraph(P.EXCHANGE + " (members' keg clearing)", small),
                Paragraph("Member statement: %s, %s" % (P.ORG, e.strftime("%B %Y")), h2),
                Paragraph("Member no. NKE-0147. Statement period 1 to %d %s." % (e.day, e.strftime("%B %Y")), small)]
        rows = [["", "50 l", "30 l", "20 l"],
                ["Kegs handed in by the member (other members' kegs)"] + [str(handed[ym][s_]) for s_ in P.SIZES],
                ["Member's own kegs returned to the member"] + [str(back[ym][s_]) for s_ in P.SIZES],
                ["Member's own kegs held at month end, awaiting return"] + [str(held[ym][s_]) for s_ in P.SIZES]]
        part.append(_grid(rows, [92, 26, 26, 26], cell))
        fee = 0.9 * sum(handed[ym].values()) + 1.4 * sum(back[ym].values())
        part.append(Paragraph("Clearing fees for the period: GBP %.2f (handling GBP 0.90 a keg handed in, GBP 1.40 a "
                              "keg returned). Payable 30 days from statement." % fee, small))
        part.append(Spacer(1, 10))
        s.append(KeepTogether(part))
        if i % 3 == 2 and i != len(months) - 1:
            s.append(PageBreak())
    O.build(path, s, "Member statements January 2024 to November 2026", "NKE member services", P.EXCHANGE,
            "%s, statements for member NKE-0147" % P.EXCHANGE,
            dt.datetime(2026, 12, 1, 8, 12, tzinfo=GMT), dt.datetime(2026, 12, 1, 8, 12, tzinfo=GMT),
            producer="LibreOffice 7.6")


def quote(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph(P.MAKER + ", Remscheid", small), Paragraph("Quotation LF-26-1187", h1),
         Paragraph("To: %s, Brighouse, attn. %s. Date: 19 November 2026. Valid to 31 December 2026." %
                   (P.ORG, P.PEOPLE["fleet"]), body),
         Paragraph("Stainless steel DIN kegs, Wrenfold livery embossing, A-type spear, RFID tag fitted and encoded, "
                   "serials continuing the customer's ranges.", body),
         _grid([["Keg", "Unit price (GBP)", "Minimum per order line", "Pallet"],
                ["50 l DIN", "96.40", "200", "8 kegs"], ["30 l DIN", "84.10", "200", "12 kegs"],
                ["20 l slim", "71.80", "100", "18 kegs"]], [40, 34, 44, 30], cell),
         Spacer(1, 6),
         Paragraph("Delivery: orders confirmed by 18 December 2026 are produced in the February slot and delivered to "
                   "Brighouse in the week beginning 26 April 2027. Later orders take the next slot (July 2027).", body),
         Paragraph("Prices ex works, carriage GBP 410 a load of up to 22 pallets. Payment 50 per cent with order, 50 "
                   "per cent on delivery.", body)]
    O.build(path, s, "Quotation LF-26-1187", "Jana Brettschneider", P.MAKER, "%s. Quotation LF-26-1187" % P.MAKER,
            dt.datetime(2026, 11, 19, 14, 5, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            dt.datetime(2026, 11, 19, 14, 22, tzinfo=dt.timezone(dt.timedelta(hours=1))), producer="LibreOffice 7.5")


def agreement(path, plans):
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    doc.add_heading("Listing agreement: %s and %s" % (P.ESTATE, P.ORG), level=1)
    doc.add_paragraph("Heads of terms agreed on 14 October 2026 between %s (the pub company) and %s (the brewer). "
                      "Signed for the brewer by %s, trade sales director." % (P.ESTATE, P.ORG, P.PEOPLE["sales"]))
    items = [
        "Estate: the pub company's %d pubs in West and North Yorkshire listed in the schedule held by the brewer's "
        "trade sales team (the 2027 plan workbook, sheet Maplestead pubs)." % len(plans["estate"]),
        "Range: every pub lists Wrenfold Pils (50 l), Calder Pale, Wrenfold IPA and Heron Lager (30 l) on a "
        "dedicated tap each, replacing the pub company's current supplier's lines.",
        "Start: the first deliveries run in the weeks of 12, 19 and 26 April 2027 by pub, as scheduled.",
        "Delivery: once a week on a fixed day from the nearest Wrenfold depot; orders by 14:00 the day before.",
        "Containers: the pub company's pubs are exempt from keg deposits, as for its other suppliers. Kegs remain "
        "the brewer's property.",
        "Expected volumes: the schedule gives each pub's expected kegs a week by line, taken from the pub company's "
        "own sales of the lines being replaced over the twelve months to September 2026.",
        "Term: three years from the first delivery, with a review after the first summer.",
    ]
    for i, t in enumerate(items):
        doc.add_paragraph("%d. %s" % (i + 1, t))
    doc.add_paragraph("Commercial terms (prices, retrospective discount) are in the separate pricing letter and are "
                      "not repeated here.")
    doc.save(path)
