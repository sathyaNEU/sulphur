"""The three documents in the pack: the merger protocol, the regulator's code of practice for centre-assessed work
and the scope letter of the 2023 review. Each is exported by the house PDF writer. They file what a banked mark, the
standard, a board's distance and the conversion are, and how moderation and standardisation are run; none says how
any estimate is made."""
import datetime as dt
import os
import sys

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
sys.path.insert(0, HERE)
import officepdf as O  # noqa: E402
import core as C  # noqa: E402
import world as WL  # noqa: E402

GMT = dt.timezone.utc
IST = dt.timezone(dt.timedelta(hours=1))
FILES = {"protocol": "protocol_on_banked_marks_2026.pdf",
         "code": "code_of_practice_centre_assessed_work_rev2024.pdf",
         "scope": "oer_review_2023_dunmoyle_scope_letter.pdf"}
JOINING = ", ".join("%s Examining Board" % b for b in C.MEMBERS[:-1]) + " and %s Examining Board" % C.MEMBERS[-1]


def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.6, leading=13.2, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13.0, leading=16.4, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.2, leading=13.6,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.7, leading=10.6)
    return body, h1, h2, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=[w * 2.83 for w in widths], repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


PROTOCOL = [
    ("1. Purpose and scope", [
        "1.1 From the June 2027 awards Carrow Awards makes the awards of the Senior Trades Certificate for candidates "
        "entered with the joining boards: %s." % JOINING,
        "1.2 The workshop portfolio (unit WP1) is assessed by the candidate's centre in the first year of the "
        "three-year course and marked out of 100. The mark is banked with the board and enters the award at the end "
        "of the course.",
        "1.3 This protocol settles how marks banked with a joining board are carried into awards made by Carrow "
        "Awards. It was agreed by the Transition Group on 9 December 2026 and approved by the Office of the "
        "Examinations Regulator on 14 December 2026.",
    ]),
    ("2. Banked marks", [
        "2.1 A banked mark is a workshop portfolio mark awarded by a joining board in the 2025 series or the 2026 "
        "series, as awarded by the board after moderation.",
        "2.2 Marks awarded in earlier series entered awards the joining boards have already made and are outside "
        "this protocol.",
        "2.3 An entry that was withdrawn, or for which the candidate was absent, carries no mark and is outside this "
        "protocol.",
    ]),
    ("3. Carrow's standard", [
        "3.1 Carrow's standard is the standard of the agreed marks of the principal moderator of Carrow Awards for "
        "the workshop portfolio, as applied in Carrow's moderation of the 2026 series.",
    ]),
    ("4. Distance and conversion", [
        "4.1 A joining board's distance from Carrow's standard is the mean, over its candidates with a banked mark, "
        "the 2025 and 2026 series taken together, of the banked mark less the mark the portfolio merits at Carrow's "
        "standard. It is stated in marks: above Carrow's standard where the banked marks are the higher, below where "
        "they are the lower.",
        "4.2 Where a board's distance is 2.0 marks or more above Carrow's standard, its banked marks are converted "
        "down by the distance. Where it is 2.0 marks or more below, they are converted up by the distance. Otherwise "
        "the board's banked marks are carried as banked.",
        "4.3 A conversion applies alike to every banked mark of the board in both series. Converted marks are held to "
        "one decimal place and are rounded only in the award calculation.",
    ]),
    ("5. Reporting", [
        "5.1 The conversion is reported with each joining board's distance for the two series taken together and "
        "for each series, and with the distance of the joining boards as a whole, which is the same mean taken over "
        "every candidate with a banked mark at any joining board.",
        "5.2 The report gives, for every centre of a joining board and each series, the distance of that centre's "
        "banked marks from Carrow's standard.",
    ]),
    ("6. Filing", [
        "6.1 Carrow Awards files the conversion with the Office of the Examinations Regulator by 31 March 2027.",
        "6.2 Each joining board supplies Carrow Awards with its mark sheets, moderation records and standardisation "
        "records for the workshop portfolio for the 2012 to 2026 series, as held in its own systems, by 5 February 2027.",
        "6.3 A centre is told of a conversion of its candidates' banked marks before the June 2027 awards are issued.",
    ]),
]

CODE = [
    ("1. Scope", [
        "1.1 This Code applies to every board approved by the Office to award a qualification with a unit assessed by "
        "the candidate's centre. It is issued under section 23 of the Examinations Regulation Act.",
        "1.2 In this Code a series is the examination series ending in June of the year named.",
    ]),
    ("2. Marking by the centre", [
        "2.1 The centre's instructors mark each candidate's work against the published marking scheme for the unit.",
        "2.2 The centre enters every candidate's mark on the board's mark sheet by the date the board sets. A "
        "candidate who withdrew or was absent is entered without a mark.",
    ]),
    ("3. The moderation sample", [
        "3.1 A board moderates every centre at least once in the rota period shown for it in the Schedule.",
        "3.2 In a centre's rota year the board draws a sample across the range of the centre's marks. For a centre "
        "with 15 candidates or fewer the sample is 10 portfolios, or every portfolio where there are fewer than 10. "
        "For a centre with 16 to 100 candidates it is 15 portfolios. For a centre with more than 100 candidates it is "
        "20 portfolios.",
        "3.3 The centre sends the sampled portfolios to the moderator with the sample record (form CA2), which lists "
        "the sampled candidates and the marks the centre awarded.",
        "3.4 The moderator marks each sampled portfolio against the marking scheme and enters the mark on the form.",
    ]),
    ("4. The outcome", [
        "4.1 The mean difference of a sample is the mean, over the sampled portfolios, of the centre's mark less the "
        "moderator's mark.",
        "4.2 Where the mean difference does not exceed the board's tolerance in either direction, the centre's marks "
        "are confirmed.",
        "4.3 Where the mean difference exceeds the tolerance, the mark of every candidate of the centre in that series "
        "is adjusted by the mean difference rounded to the nearest whole mark.",
        "4.4 The board issues the outcome to the centre together with the moderator's report on the centre's marking.",
        "4.5 A record found to be in error is corrected and reissued. The reissued record replaces the earlier one.",
    ]),
    ("5. Standardisation", [
        "5.1 Each board appoints a principal moderator for the unit.",
        "5.2 Before each series the board holds a standardisation meeting. The scripts for the meeting are 40 portfolios "
        "sampled in the previous series, issued to the board's moderators without marks or annotations.",
        "5.3 Every moderator marks each script before the meeting and returns the marks to the board.",
        "5.4 The principal moderator's agreed mark for each script is confirmed at the meeting. The agreed marks are "
        "the board's standard for the series.",
        "5.5 A moderator applies the standard of the agreed marks in the moderation of that series.",
    ]),
    ("6. Registration of moderators", [
        "6.1 From the 2020 series every moderator holds a registration number issued by the Office. A moderator uses "
        "the same number with every board that appoints them.",
        "6.2 Records of series before 2020 carry the references each board issued to its own moderators.",
    ]),
    ("7. Records", [
        "7.1 A board keeps its mark sheets, sample records, outcomes and standardisation records for fifteen series.",
    ]),
]
SCHEDULE = [("Carrow Awards", 1, 3), ("Ardkeel Examining Board", 3, 3), ("Brannock Examining Board", 3, 5),
            ("Dunmoyle Examining Board", 3, 4), ("Eskerry Examining Board", 2, 4), ("Fennor Examining Board", 3, 6),
            ("Gortavale Examining Board", 2, 4)]

SCOPE = [
    "Dear Mr Kealty,",
    "<b>Review of centre-assessed marking: workshop portfolio (WP1), 2023 series</b>",
    "I write to confirm the scope of the review the Office will carry out this autumn under section 31 of the "
    "Examinations Regulation Act.",
    "The review covers every centre that entered candidates for the workshop portfolio with Dunmoyle Examining Board "
    "in the 2023 series. The Office will draw eight portfolios from each centre's mark sheet, or every portfolio "
    "where a centre entered fewer than eight, and will ask the centres to send them to the Office by 6 October 2023.",
    "The portfolios will be marked by the senior moderators of Carrow Awards, to the standard of the agreed marks of "
    "Carrow's principal moderator for the 2023 series. They will be supplied to the panel without the centre's "
    "marks, the moderator's marks or any annotation.",
    "When the marking is complete the Office will return the review marks to the Board as a data file, with the "
    "centre's mark beside each review mark.",
    "The review does not alter any mark awarded in the 2023 series, and no centre's outcome for that series is "
    "reopened by it.",
    "Please let me have the name of the officer who will act as the Board's contact for the review by 22 September.",
    "Yours sincerely,",
    "%s<br/>Head of Qualifications Review<br/>Office of the Examinations Regulator" % WL.PEOPLE["regulator"],
]


def protocol(target):
    body, h1, h2, cell = _styles()
    title = "Protocol on Banked Marks"
    story = [Paragraph(title, h1),
             Paragraph("Senior Trades Certificate, workshop portfolio (WP1). Transition Group paper TG/26/41, as approved.", body),
             Spacer(1, 4)]
    for head, paras in PROTOCOL:
        story.append(Paragraph(head, h2))
        for p in paras:
            story.append(Paragraph(p, body))
    O.build(os.path.join(target, FILES["protocol"]), story, title=title, author=WL.PEOPLE["secretary"],
            subject="Transfer of banked marks to Carrow Awards", footer="TG/26/41 Protocol on Banked Marks, approved 14 December 2026",
            created=dt.datetime(2026, 12, 15, 10, 22, tzinfo=GMT), modified=dt.datetime(2026, 12, 15, 10, 22, tzinfo=GMT),
            producer="LibreOffice 25.8", font="Liberation Sans")


def code(target):
    body, h1, h2, cell = _styles()
    title = "Code of Practice for Centre-Assessed Work"
    story = [Paragraph(title, h1),
             Paragraph("Office of the Examinations Regulator. First issued September 2018, revised January 2024.", body),
             Spacer(1, 4)]
    for head, paras in CODE:
        story.append(Paragraph(head, h2))
        for p in paras:
            story.append(Paragraph(p, body))
    story.append(Paragraph("Schedule. Rota periods and tolerances, workshop portfolio (WP1)", h2))
    story.append(_grid([["Board", "Rota period (years)", "Tolerance (marks)"]] + [list(r) for r in SCHEDULE], [70, 40, 40], cell))
    O.build(os.path.join(target, FILES["code"]), story, title=title, author="Office of the Examinations Regulator",
            subject="Centre-assessed work", footer="Code of Practice for Centre-Assessed Work, revised January 2024",
            created=dt.datetime(2024, 1, 18, 15, 6, tzinfo=GMT), modified=dt.datetime(2024, 1, 18, 15, 6, tzinfo=GMT),
            producer="LibreOffice 7.6", font="Liberation Sans")


def scope(target):
    body, h1, h2, cell = _styles()
    title = "Review of centre-assessed marking, WP1, 2023 series: scope"
    story = [Paragraph("Office of the Examinations Regulator", h1),
             Paragraph("Qualifications Review Unit, 14 Harcourt Quay, Dublin 2", body),
             Paragraph("12 September 2023<br/>Our reference: OER/QR/23/07", body), Spacer(1, 4),
             Paragraph("Mr Lucas Kealty<br/>Chief Executive<br/>Dunmoyle Examining Board<br/>Dundalk, Co. Louth", body),
             Spacer(1, 6)]
    for p in SCOPE:
        story.append(Paragraph(p, body))
    O.build(os.path.join(target, FILES["scope"]), story, title=title, author=WL.PEOPLE["regulator"],
            subject="OER/QR/23/07", footer="OER/QR/23/07",
            created=dt.datetime(2023, 9, 12, 11, 40, tzinfo=IST), modified=dt.datetime(2023, 9, 12, 11, 40, tzinfo=IST),
            producer="LibreOffice 7.5", font="Liberation Sans")


def write_all(target):
    protocol(target)
    code(target)
    scope(target)


if __name__ == "__main__":
    write_all(sys.argv[1])
