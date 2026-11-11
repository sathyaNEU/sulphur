"""task8: the pack's documents and workbooks. The trust's Reading Forward policy (version 3) and the three test
publishers' technical summaries are Word documents exported to PDF by LibreOffice Writer through the house writer;
the Brightway results workbook (typed by each academy's staff) passes through the house workbook writer."""
import datetime as dt
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import postprocess  # noqa: E402
import params as P  # noqa: E402

BST = dt.timezone(dt.timedelta(hours=1))
GMT = dt.timezone(dt.timedelta(hours=0))


def styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=4)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.5, leading=14,
                        spaceBefore=8, spaceAfter=4, keepWithNext=1)
    small = ParagraphStyle("small", parent=body, fontSize=8.2, leading=10.8, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, small, cell


def grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


POLICY = [
    ("1. Purpose and scope", [
        "Reading Forward supports Year 7 students whose reading at the start of secondary school is below the level "
        "the Key Stage 3 curriculum assumes. This policy sets who joins the programme in each academy and the tutor "
        "time each academy is given for it. It covers every Year 7 student on roll at an academy of the trust at the "
        "October census (1 October 2026 for the 2026-27 year)."]),
    ("2. Entry reading", [
        "2.1 A student's entry reading is their reading at the start of Year 7, on the Lexis 2019 standardisation (the "
        "Lexis basis), as a whole standardised score.",
        "2.2 It is taken from the student's first valid sitting of an entry reading test after the May 2026 KS2 "
        "tests. A sitting is valid when the test was completed; a Quill session is valid when the student answered "
        "at least 24 questions.",
        "2.3 Each result counts at the whole Lexis score of equal reading at the start of Year 7.",
        "2.4 A student on roll who has no valid sitting by the census is placed from their KS2 reading scaled "
        "score, at the whole Lexis score of equal reading at the start of Year 7. A student with neither is "
        "assessed on arrival and is not in the October numbers."]),
    ("3. Who joins", [
        "A Year 7 student joins Reading Forward when their entry reading is below 85. Places are confirmed to "
        "families by each academy after the October census."]),
    ("4. Tutor time", [
        "Each academy is given 0.4 tutor hours a week for each Reading Forward student, for the 36 teaching weeks of "
        "the year. Tutor time is costed at the trust's reading tutor rate, £27.80 an hour for 2026-27 including "
        "on-costs. The provisional 2026-27 budget, approved with this policy on last October's 848 Reading Forward "
        "students, is £339,500; the trust board approves the final budget at its October meeting on the October "
        "census numbers."]),
    ("5. Review in the year", [
        "Reading Forward students are re-assessed in January and in June. A student leaves the programme at a "
        "re-assessment when their reading reaches 85; the tutor time set in October is not reduced in-year."]),
    ("6. Changes", [
        "Version 3 (July 2026) places every academy's students on the Lexis basis ahead of the trust's move to Lexis "
        "in all academies from September 2027. Year 7 at the Brightway academies also sit Lexis in September 2026, "
        "to put Brightway results on the Lexis basis. Version 2 (September 2024) placed students on their own "
        "academy's test, on a standardised score below 85."]),
]


def policy(path):
    body, h1, h2, small, cell = styles()
    s = [Paragraph("%s · Education" % P.TRUST, small),
         Paragraph("Reading Forward: Year 7 entry reading", h1),
         Paragraph("Trust policy, version 3. Approved by the trust board on 9 July 2026. Owner: Rosemary Collier, "
                   "director of education.", small), Spacer(1, 4)]
    for head, paras in POLICY:
        s.append(Paragraph(head, h2))
        for p in paras:
            s.append(Paragraph(p, body))
    O.build(path, s, "Reading Forward: Year 7 entry reading", "Rosemary Collier", "Trust policy",
            "%s · Reading Forward policy v3" % P.TRUST, dt.datetime(2026, 7, 9, 15, 12, tzinfo=BST),
            dt.datetime(2026, 7, 10, 8, 44, tzinfo=BST), page_of=True, producer="LibreOffice 25.8")


TECH = {
    "LEXIS": ("Lexis Assessment", "Lexis 11-14 Reading: technical summary", [
        ("The test", "Lexis 11-14 is an online test of reading comprehension for students aged 11 to 14. Form A has "
                     "48 questions on six passages (fiction, non-fiction and a poem) and is taken in one sitting of 40 "
                     "minutes, with a further 10 minutes for students with extra time. Questions are marked by the "
                     "platform; results are available to the school the next day."),
        ("Standardisation", "Standard age scores were set in 2019 on 4,212 students in 168 maintained schools and "
                            "academies in England and Wales, sampled by region, school type and attainment, each "
                            "taking the test for the first time between September and November. Scores are "
                            "standardised by age in months, with a mean of 100 and a standard deviation of 15."),
        ("Reporting", "The standard age score runs from 69 to 141; 69 is shown for scores below 70 and 141 for scores "
                      "above 140. A stanine and a reading age are reported alongside."),
        ("Reliability", "Internal consistency (Cronbach's alpha) 0.93 in the standardisation sample; standard error of "
                        "measurement 4.0 standard age score points.")]),
    "QUILL": ("Quill Learning", "Quill Reading: technical summary (UK edition)", [
        ("The assessment", "Quill Reading is an adaptive online reading assessment for Years 3 to 11. Each question is "
                           "chosen from the bank by the student's answers so far; a full session is 24 to 34 "
                           "questions and usually takes 20 to 35 minutes."),
        ("Scales", "The Quill scaled score (0 to 1400) runs across all year groups. The standardised score compares a "
                   "student with others of the same age in months, mean 100 and standard deviation 15, from 69 to "
                   "141."),
        ("Standardisation", "The UK standardised scores were set in a 2024 restandardisation on 6,840 students in "
                            "Years 6 to 9 in 214 schools in England, weighted to the national school population by "
                            "region and free school meals."),
        ("Reliability", "Marginal reliability 0.91; the session report gives each student's standard error.")]),
    "BRIGHTWAY": ("Brightway Education", "Brightway Reading Check: technical summary", [
        ("The test", "The Brightway Reading Check is a paper test of reading for Years 6 to 8: 50 questions in 45 "
                     "minutes, marked by the school with the mark scheme and converted to a standardised score "
                     "with the norm tables in the teacher's guide."),
        ("Standardisation", "The norm tables were set in 2016 on 2,390 pupils in Years 6 to 8 in 61 schools in the "
                            "North of England and the Midlands. Scores are standardised by age in months, with a mean "
                            "of 100 and a standard deviation of 15."),
        ("Reporting", "The norm tables give standardised scores from 70 to 130; scores below the tables are reported "
                      "as &lt;70 and above them as &gt;130."),
        ("Reliability", "KR-20 0.87; standard error of measurement 5.4 points.")]),
}


def technical(path, test):
    body, h1, h2, small, cell = styles()
    org, title, parts = TECH[test]
    s = [Paragraph(org, small), Paragraph(title, h1), Spacer(1, 4)]
    for head, text in parts:
        s.append(Paragraph(head, h2))
        s.append(Paragraph(text, body))
    created = {"LEXIS": dt.datetime(2023, 3, 2, 10, 5, tzinfo=GMT), "QUILL": dt.datetime(2024, 11, 18, 14, 40, tzinfo=GMT),
               "BRIGHTWAY": dt.datetime(2017, 1, 23, 9, 30, tzinfo=GMT)}[test]
    producer = {"LEXIS": "LibreOffice 7.4", "QUILL": "LibreOffice 24.8", "BRIGHTWAY": "LibreOffice 5.2"}[test]
    O.build(path, s, title, org, "Technical summary", org, created, created + dt.timedelta(minutes=37),
            producer=producer)


def brightway_workbook(path, sheets):
    wb = Workbook()
    wb.remove(wb.active)
    for name, rows in sheets.items():
        ws = wb.create_sheet(name.replace(" Academy", "")[:30])
        ws["A1"] = "Brightway Reading Check results, Year 7, September 2026"
        ws["A1"].font = Font(bold=True)
        ws["A2"] = name
        start = 4 if name != "Parkgate Academy" else 5
        if start == 5:
            ws["A3"] = "Marked by the English department; standardised scores from the teacher's guide tables"
        ws.cell(start, 1, "Name")
        ws.cell(start, 2, "Form")
        ws.cell(start, 3, "DOB")
        ws.cell(start, 4, "Raw /50")
        ws.cell(start, 5, "Standardised score")
        ws.cell(start, 6, "Date tested")
        for c in range(1, 7):
            ws.cell(start, c).font = Font(bold=True)
        for k, r in enumerate(rows):
            for c, v in enumerate(r, 1):
                cell = ws.cell(start + 1 + k, c, v)
                if c == 6 and v is not None:
                    cell.number_format = "dd/mm/yyyy"
        ws.column_dimensions["A"].width = 28
        ws.column_dimensions["C"].width = 13
        ws.column_dimensions["E"].width = 18
        ws.column_dimensions["F"].width = 12
    wb.save(path)
    postprocess.normalize_ooxml(path, "Beverley Barnett", "Abbie Lee", "2026-09-04T07:58:00Z", "2026-09-29T15:21:00Z",
                                excel=True, company=P.TRUST)
