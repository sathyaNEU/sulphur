"""The documents: Saarnela's labour planning standard (issue 4) and the agency's framework agreement, each a Word
document exported to PDF by LibreOffice Writer through the house writer, and the pilot review, a Word document."""
import datetime as dt
import os
import sys

from docx import Document
from docx.shared import Mm, Pt
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import params as P  # noqa: E402

FI_W = dt.timezone(dt.timedelta(hours=2))
FI_S = dt.timezone(dt.timedelta(hours=3))


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.4, spaceAfter=6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.6, leading=10.4)
    return body, h1, h2, small, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


STANDARD = [
    ("1. Scope", [
        "This standard sets how the Saarnela fulfilment centre plans its pickers for the peak and how the peak plan "
        "put to the operations director is stated. It applies to the pick zones P1, P2 and B1 and to every client "
        "the centre picks for."]),
    ("2. Terms", [
        "2.1 The peak is ISO weeks 46 to 50 of a year.",
        "2.2 Picker hours are the paid hours of pickers working in a pick zone, as the payroll records them against "
        "the zone's cost centre. Absence is not picker hours, and hours booked to the packing cost centre are not "
        "picker hours of any zone.",
        "2.3 Lines are the order lines a zone picks, as the WMS counts them. The time a line takes to pick is the WMS "
        "task time of the pick.",
        "2.4 The WMS releases the web orders it receives on a day for picking at 06:00 on the next working day. The "
        "showrooms' replenishment orders are released and picked on the weekday they are placed."]),
    ("3. Zones and shifts", [
        "3.1 The pick zones are those in the table below.",
        "TABLE",
        "3.2 A small-parts zone never has more pickers on its floor in a shift than its limit.",
        "3.3 The day shift runs 06:00 to 14:30 with eight paid hours and an unpaid half hour, Monday to Saturday in "
        "the peak and Monday to Friday outside it. The evening shift runs 14:30 to 23:00 with eight paid hours, Monday "
        "to Friday. The centre is closed on public holidays.",
        "3.4 A small-parts zone works the evening shift in a peak week when the lines it is expected to pick that week "
        "cannot be picked on that week's day shifts with the zone's limit of pickers on the floor. The day shifts are "
        "then worked at the limit and the evening shifts of the week's working weekdays pick the rest.",
        "3.5 The peak plan states each zone's picker hours for each peak week with a range the planner would put 80 "
        "per cent on. The range covers both how the client's volumes turn out and the zone's time a line."]),
    ("4. Staffing", [
        "4.1 Own pickers are planned on the day shift of every working weekday in their home zone, less the zone's "
        "sickness absence over the same weeks of the last peak.",
        "4.2 Every other picker hour is booked from the agency under the framework agreement, week by week."]),
    ("5. Volumes", [
        "5.1 The plan is made on the lines the centre expects to pick. A client's forecasts are an input to that "
        "expectation."]),
]


def standard(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s, %s fulfilment centre" % (P.ORG, P.SITE), small),
         Paragraph("Labour planning standard", h1),
         Paragraph("Issue 4, approved by the operations director 21 September 2026. Replaces issue 3 (January 2024). "
                   "Owner: the site manager.", small), Spacer(1, 4)]
    for head, paras in STANDARD:
        s.append(Paragraph(head, h2))
        for t in paras:
            if t == "TABLE":
                s.append(_grid([["Zone", "Use", "Aisles", "Limit of pickers on the floor"],
                                ["P1", "small parts", "12 (8 before 8 January 2024)", "24"],
                                ["P2", "small parts", "11 (7 before 8 January 2024)", "22"],
                                ["B1", "bulky, reach trucks", "6", "none set"]], [18 * 2.835, 42 * 2.835, 60 * 2.835, 52 * 2.835], cell))
                s.append(Spacer(1, 6))
                continue
            s.append(Paragraph(t, body))
    s.append(Paragraph("Revisions", h2))
    s.append(_grid([["Issue", "Date", "Change"],
                    ["1", "March 2021", "first issue, at the start of operations for Kotikaari Oy"],
                    ["2", "August 2022", "2.2 the packing cost centre; 4.1 the absence allowance"],
                    ["3", "January 2024", "3.1 the zones after the mezzanine extension; 3.2 the zone limits after the 2023 safety review"],
                    ["4", "September 2026", "2.1 and 2.4 restated; 3.4 revised; 3.5 and 5.1 added"]],
                   [16 * 2.835, 30 * 2.835, 126 * 2.835], cell))
    O.build(path, s, "Labour planning standard, issue 4", P.PEOPLE["site"], "Saarnela fulfilment centre",
            "%s, Saarnela. Labour planning standard, issue 4." % P.ORG,
            dt.datetime(2026, 9, 21, 13, 42, tzinfo=FI_S), dt.datetime(2026, 9, 21, 14, 5, tzinfo=FI_S), producer="LibreOffice 7.6")


def agreement(path):
    body, h1, h2, small, cell = _styles()
    s = [Paragraph("%s and %s" % (P.AGENCY, P.ORG), small),
         Paragraph("Framework agreement for agency pickers, Saarnela fulfilment centre", h1),
         Paragraph("Signed 12 February 2025, in force 1 March 2025 to 28 February 2028.", small), Spacer(1, 4)]
    sec = [
        ("1. Services", ["%s supplies trained warehouse pickers to the Saarnela fulfilment centre of %s for its pick "
                         "zones, on the day and evening shifts the centre runs." % (P.AGENCY, P.ORG)]),
        ("2. Booking", ["2.1 The centre books agency picker hours by week and pick zone, by the Thursday two weeks "
                        "before the week. Bookings for the peak weeks are confirmed by 15 October of the year.",
                        "2.2 A booked shift is eight paid hours. A booking may be cut by up to 10 per cent of the "
                        "week's hours until 72 hours before the shift; later cuts are invoiced.",
                        "2.3 The agency's pickers wear the agency's badge. The badges were re-issued on 1 April 2025 "
                        "with new numbers; the agency keeps the register of old and new numbers."]),
        ("3. Prices", ["3.1 The hourly price is EUR 31.40 on the day shift and EUR 37.05 on the evening shift, Monday "
                       "to Friday; Saturday hours are priced at EUR 39.25. Prices are indexed on 1 March each year to "
                       "the collective agreement for the logistics sector.",
                       "3.2 A picker's first shift at the centre includes a two-hour induction, priced as picker hours."]),
        ("4. Quality", ["4.1 The agency replaces a picker the centre asks it to replace within two working days.",
                        "4.2 Pick accuracy and safety incidents are reviewed by the parties each quarter."]),
        ("5. Contacts", ["For %s: %s, account manager. For %s: %s, site manager." % (
            P.AGENCY, P.PEOPLE["agency"], P.ORG, P.PEOPLE["site"])]),
    ]
    for head, paras in sec:
        s.append(Paragraph(head, h2))
        for t in paras:
            s.append(Paragraph(t, body))
    O.build(path, s, "Framework agreement, agency pickers", P.PEOPLE["agency"], "Saarnela fulfilment centre",
            "%s / %s, framework agreement 2025" % (P.AGENCY, P.ORG),
            dt.datetime(2025, 2, 12, 10, 18, tzinfo=FI_W), dt.datetime(2025, 2, 12, 11, 2, tzinfo=FI_W), producer="LibreOffice 7.6")


def review(path, figs):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    doc.add_heading("Huippu Sport pilot at Saarnela, weeks 37 to 44: review", level=1)
    doc.add_paragraph("%s, continuous improvement, 3 November 2026" % P.PEOPLE["ci"])
    doc.add_heading("Scope", level=2)
    doc.add_paragraph("From 7 September to 1 November 2026 Saarnela picked Huippu Sport's web orders for %d of its "
                      "fastest-moving articles, stocked in P2 aisles 1 to 4. The lines were picked in Huippu tours by "
                      "six trained P2 pickers and packed on two benches; the other articles stayed at the current "
                      "warehouse." % figs["articles"])
    doc.add_heading("Volumes", level=2)
    doc.add_paragraph("%s Huippu Sport lines were picked over the eight weeks, %s a working day on average." % (
        "{:,}".format(figs["lines"]).replace(",", " "), "{:,}".format(figs["per_day"]).replace(",", " ")))
    doc.add_heading("Pick time", level=2)
    doc.add_paragraph("A Huippu Sport line took %s minutes, scanner confirmation to confirmation in the tours. P2's "
                      "other lines took %s minutes a line in the same weeks (the WMS zone report, task time over "
                      "lines)." % (("%.2f" % figs["pilot_t"]).replace(".", ","), ("%.2f" % figs["p2_t"]).replace(".", ",")))
    doc.add_heading("Accuracy and damages", level=2)
    doc.add_paragraph("Pick accuracy was 99.6 per cent against 99.7 for P2 as a whole. Two lines were damaged in "
                      "picking. Size and colour labels on the polybags were checked at every pick, as agreed with "
                      "Huippu Sport's customer service.")
    doc.add_heading("Next", level=2)
    doc.add_paragraph("The slotting run of 30 October 2026 places the whole assortment for the move on 1 March 2027. "
                      "Bench layout for the Huippu Sport packaging to be agreed by January.")
    doc.save(path)
