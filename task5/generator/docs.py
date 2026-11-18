"""The three documents in the pack, each exported from a word processor through the house writer: the Minister's
order on the consular establishment, the area's regulation on migration and population statistics (consolidated
text) and the Posting Board's request for the 2027 cycle. They say what a district, a citizen, usual residence and
each table are; none says how any number is arrived at."""
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
import world as WL  # noqa: E402

CET = dt.timezone(dt.timedelta(hours=1))
CEST = dt.timezone(dt.timedelta(hours=2))
FILES = {
    "order": "consular_establishment_order_14_2025.pdf",
    "regulation": "cma_regulation_7_2009_migration_population_statistics_consolidated.pdf",
    "letter": "posting_board_request_2027_cycle.pdf",
}
RATE = 5000


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


ORDER = [
    ("1. Districts", [
        "1.1 A consular district is the territory of one partner state of the Common Movement Area. The districts and "
        "the consulates general that serve them are listed in the Schedule.",
        "1.2 This Order applies to consular officers posted to the consulates general. Honorary consuls and locally "
        "engaged staff are outside it.",
    ]),
    ("2. Establishment", [
        "2.1 The establishment of a district for a posting cycle is one consular officer for every %s Orlavan "
        "citizens, or part of %s, usually resident in the district on 1 January of the first year of the cycle." % (
            format(RATE, ","), format(RATE, ",")),
        "2.2 A person is usually resident in a state where they have lived, or intend to live, for a period of twelve "
        "months or more. An Orlavan citizen is a person registered as a citizen of Orlava. Both terms have the meaning "
        "they have in Regulation 7/2009 of the Common Movement Area.",
        "2.3 The number of citizens usually resident in each district is supplied to the Posting Board by Statistics "
        "Orlava, in whole persons, not later than ten working days before the Board meets.",
        "2.4 The establishment is fixed for each district on its own. No district's establishment is raised or "
        "reduced on account of another's, and the Order sets no smallest or largest establishment.",
    ]),
    ("3. Posting cycle", [
        "3.1 A posting cycle is three calendar years. The first cycle under this Order is 2027 to 2029. The Board "
        "meets in March of the first year of a cycle; for the first cycle it meets on 18 March 2027.",
        "3.2 An establishment fixed by the Board takes effect on 1 September of the first year of the cycle. Until "
        "then the establishment in force continues.",
    ]),
    ("4. Report", [
        "4.1 With the number of citizens for each district, Statistics Orlava reports the number of emigrations of "
        "citizens from the district (Regulation 7/2009, article 2(c)) from the date of the last census of the partner "
        "state to the day before the date in 2.1. The Ministry's Office for Returning Citizens uses this number in "
        "planning its casework.",
        "4.2 The report sets out, for each district, the number of citizens, the establishment that 2.1 gives and "
        "the number in 4.1.",
    ]),
    ("5. Commencement", [
        "5.1 This Order comes into force on 1 October 2025.",
        "5.2 The establishment fixed by the Posting Board on 13 June 2023 continues in force as 3.2 provides.",
    ]),
]


def write_order(target):
    body, h1, h2, cell = _styles()
    title = "Order No. 14 of 2025 on the establishment of consular officers in the districts of the Common Movement Area"
    head = [["Issued by", "The Minister of Foreign Affairs"], ["Date", "23 September 2025"],
            ["Published", "Official Gazette of the Republic of Orlava, No. 71/2025"]]
    story = [Paragraph(title, h1), _grid(head, [36, 130], cell), Spacer(1, 6)]
    for hd, paras in ORDER:
        story.append(Paragraph(hd, h2))
        for p in paras:
            story.append(Paragraph(p, body))
    story.append(Paragraph("Schedule. Consular districts", h2))
    story.append(_grid([["District", "Partner state", "Consulate general"]] +
                       [[h, WL.LONG[h], WL.SEAT[h]] for h in WL.HOSTS], [36, 80, 50], cell))
    O.build(os.path.join(target, FILES["order"]), story, title=title, author="Ministry of Foreign Affairs, Legal Service",
            subject="Consular establishment", footer="Order No. 14 of 2025, Official Gazette No. 71/2025",
            created=dt.datetime(2025, 9, 23, 11, 48, tzinfo=CEST), modified=dt.datetime(2025, 9, 23, 11, 48, tzinfo=CEST),
            producer="LibreOffice 25.2", font="Liberation Sans")


REGULATION = [
    ("Article 1. Subject matter", [
        "1. This Regulation lays down the tables on international migration and on the usually resident population "
        "that each member state of the Common Movement Area transmits to the Common Movement Area Statistical "
        "Office (the Office), and the definitions those tables follow.",
    ]),
    ("Article 2. Definitions", [
        "(a) Usual residence is the place where a person normally spends the daily period of rest. A person is "
        "usually resident in a state where they have lived, or intend to live, for a period of twelve months or more.",
        "(b) Immigration is the act by which a person establishes usual residence in a member state, having been "
        "usually resident in another state.",
        "(c) Emigration is the act by which a person who was usually resident in a member state ceases to be "
        "usually resident there, whatever the state they move to.",
        "(d) Citizenship is the legal bond between a person and a state. In every table a person is classified under "
        "the citizenship registered when they established usual residence in the reporting state, and keeps that "
        "classification for as long as they remain usually resident there. A child born in the reporting state is "
        "classified under the citizenship registered at birth.",
        "(e) The reference year of an immigration or an emigration is the calendar year in which the change of usual "
        "residence took place.",
    ]),
    ("Article 3. Tables", [
        "1. For each reference year each member state transmits:",
        "Table A. Immigration, by citizenship of the person, sex and age group.",
        "Table B. Emigration of the reporting state's own citizens, by state of next usual residence, sex and age group.",
        "Table C. Emigration of foreign citizens, by citizenship of the person, sex and age group.",
        "Table D. Immigration of the reporting state's own citizens, by state of previous usual residence, sex and "
        "age group.",
        "Table E. Live births to, and deaths of, foreign citizens usually resident in the reporting state, by "
        "citizenship.",
        "2. For each census round each member state transmits Table F: usual residents by citizenship (F.1) and by "
        "country of birth (F.2).",
        "3. Age is the age the person reaches during the reference year. The age groups are 0 to 14, 15 to 24, 25 to "
        "34, 35 to 44, 45 to 64 and 65 or over.",
        "4. A citizenship or a state outside the Area is shown under Other (ZZZ in the tables, 990 in Table F).",
    ]),
    ("Article 4. Reference dates", [
        "1. A count of the usually resident population refers to 00:00 on 1 January. A person who establishes usual "
        "residence during a calendar year is first counted on 1 January of the following year.",
        "2. Census rounds are held on 1 January of each year ending in 1. A member state may hold a count in other "
        "years.",
    ]),
    ("Article 5. Sources", [
        "1. Member states compile Tables A to D from their population registers and Table E from civil registration.",
        "2. Table F is compiled from the population census of the member state.",
    ]),
    ("Article 6. Transmission and release", [
        "1. Tables A to E for a reference year are transmitted to the Office within 24 months of the end of that year.",
        "2. The Office publishes the tables it has received in a release each May. A reference year first appears "
        "in the release of the third year after it.",
        "3. A member state may transmit a table again for an earlier reference year. The Office publishes it in its "
        "next release, and for the same table, reporting state, partner and reference year a later release replaces "
        "an earlier one.",
    ]),
    ("Article 7. Codes", [
        "1. Tables A to E identify states by the Area's three-letter codes. Table F identifies them by the Area's "
        "three-digit codes. The Office keeps the list of codes.",
    ]),
    ("Article 8. Entry into force", [
        "1. This Regulation entered into force on 1 January 2010. This consolidated text includes the amendments of "
        "Regulation 3/2016 (Table E) and Regulation 11/2023 (age groups).",
    ]),
]


def write_regulation(target):
    body, h1, h2, cell = _styles()
    title = "Regulation 7/2009 of the Council of the Common Movement Area on statistics of migration and of the usually resident population"
    head = [["Text", "Consolidated text of 1 March 2024"], ["Prepared by", WL.HUB + ", Legal and Standards Unit"],
            ["Status", "For documentation; the texts published in the Area's Journal are authentic"]]
    story = [Paragraph(title, h1), _grid(head, [36, 130], cell), Spacer(1, 6)]
    for hd, paras in REGULATION:
        story.append(Paragraph(hd, h2))
        for p in paras:
            story.append(Paragraph(p, body))
    O.build(os.path.join(target, FILES["regulation"]), story, title=title, author="Constanze Huemer",
            subject="Migration and population statistics", footer="Regulation 7/2009, consolidated text of 1 March 2024",
            created=dt.datetime(2024, 2, 27, 16, 9, tzinfo=CET), modified=dt.datetime(2024, 2, 27, 16, 9, tzinfo=CET),
            producer="LibreOffice 24.2", font="Liberation Serif")


def write_letter(target):
    body, h1, h2, cell = _styles()
    title = "Posting Board: citizens resident in the consular districts for the 2027 to 2029 cycle"
    head = [["To", "%s, Head of Population Statistics, %s" % (WL.PEOPLE["head"], WL.ORG)],
            ["From", "%s, Secretary of the Posting Board, Ministry of Foreign Affairs" % WL.PEOPLE["secretary"]],
            ["Date", "11 January 2027"], ["Reference", "PB/2027/004"]]
    paras = [
        "The Posting Board meets on 18 March 2027 to fix the establishment of consular officers for the 2027 to 2029 "
        "cycle, the first under Order No. 14 of 2025.",
        "Under clause 2.3 of the Order I ask Statistics Orlava to supply, for each of the seven districts, the number "
        "of Orlavan citizens usually resident on 1 January 2027, with the establishment that clause 2.1 gives on it.",
        "Under clause 4.1 the Board also needs the number of citizens who moved away from each district between the "
        "census of 1 January 2021 and 31 December 2026.",
        "The Board would like the report by 4 March 2027. The establishment in force, set in 2023 on the 2021 census "
        "counts, is enclosed for reference.",
        "Yours sincerely,",
        WL.PEOPLE["secretary"],
    ]
    story = [Paragraph(title, h1), _grid(head, [26, 140], cell), Spacer(1, 8)]
    for p in paras:
        story.append(Paragraph(p, body))
    O.build(os.path.join(target, FILES["letter"]), story, title=title, author=WL.PEOPLE["secretary"],
            subject="Consular establishment 2027 to 2029", footer="Ministry of Foreign Affairs, Posting Board, PB/2027/004",
            created=dt.datetime(2027, 1, 11, 10, 26, tzinfo=CET), modified=dt.datetime(2027, 1, 11, 10, 26, tzinfo=CET),
            font="Liberation Sans")


def write_all(target):
    write_order(target)
    write_regulation(target)
    write_letter(target)
