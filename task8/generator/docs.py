"""task8 architecture 18: the Board's documents, written in Writer and exported (officepdf): the Level 1 Numeracy
specification, the 2022 standard-setting record and the Awards Committee's September 2026 minute; and the chair's
email asking for the recommendation."""
import datetime as dt

from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

import officepdf as O
import params as P

CST = dt.timezone(dt.timedelta(hours=-6))
CDT = dt.timezone(dt.timedelta(hours=-5))
SS = getSampleStyleSheet()
BODY = ParagraphStyle("b", parent=SS["Normal"], fontName="Helvetica", fontSize=9.2, leading=12.4, spaceAfter=5)
H1 = ParagraphStyle("h1", parent=SS["Heading1"], fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=6)
H2 = ParagraphStyle("h2", parent=SS["Heading2"], fontName="Helvetica-Bold", fontSize=10.4, leading=13.5,
                    spaceBefore=6, spaceAfter=3)
SMALL = ParagraphStyle("s", parent=BODY, fontSize=7.8, leading=10, textColor=colors.HexColor("#444444"))
CELL = ParagraphStyle("c", parent=BODY, fontSize=7.6, leading=9.4, spaceAfter=0)
CELLB = ParagraphStyle("cb", parent=CELL, fontName="Helvetica-Bold")

PEOPLE = {"manager": "Yvette Clark", "chair": "Shawn Simpson", "psychometrician": "Andrew Adams"}


def _esc(x):
    return str(x).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def _p(t, st=BODY):
    return Paragraph(_esc(t), st)


def _table(rows, widths):
    data = [[Paragraph(_esc(c), CELLB if i == 0 else CELL) for c in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * mm for w in widths], hAlign="LEFT")
    t.setStyle(TableStyle([("LINEBELOW", (0, 0), (-1, 0), 0.6, colors.HexColor("#333333"))]))
    return t


SPEC_SENTENCES = {
    "pass": ("The pass mark on each Level 1 paper is the mark that a candidate who just meets the Level 1 standard "
             "can be expected to score on that paper, rounded to the nearest whole mark."),
    "band": ("Each item on a Level 1 paper should be one that a candidate who just meets the Level 1 standard "
             "answers correctly with a chance of at least 0.20 and at most 0.90."),
}


def specification(path):
    s = [_p("Level 1 Numeracy: qualification specification", H1),
         _p("%s. Version 2026.1, approved by the Board on 12 March 2026 for papers set from 2027; replaces version "
            "2021.2." % P.ORG, SMALL),
         Spacer(1, 4),
         _p("1. Purpose", H2),
         _p("Level 1 Numeracy recognises that an adult can work with whole numbers, simple fractions and decimals, "
            "money, measures, simple data and number patterns at the level set out in the Board's Level 1 performance "
            "descriptors, in the settings of daily life, training and work. It is offered through registered "
            "community learning centres in Manitoba and Saskatchewan and is recognised by the provinces' adult "
            "learning programmes as the numeracy entry point to Level 2 and to apprenticeship preparation."),
         _p("2. The paper", H2),
         _p("Candidates sit one paper online at a registered learning centre, under the centre's invigilation, on a "
            "day the centre arranges between 1 February and 30 October. The paper has 40 items worth one mark each "
            "and candidates have 75 minutes. Answers are typed: a number, a value with its unit, or a short word or "
            "phrase. On-screen calculators are available for every item. A new paper is set for each calendar "
            "year, and a candidate sits a given year's paper once; a candidate who does not pass may register for "
            "the next year's paper."),
         _p("3. Content", H2),
         _p("From 2027 the paper covers five strands. The 2026 revision adds the patterns and relationships strand "
            "(sequences, rules written in words, simple formulas and proportional reasoning) and reduces money and "
            "measures accordingly."),
         _table([["Strand", "Items from 2027", "Items to 2026"], ["Number", "10", "11"],
                 ["Money and measures", "8", "14"], ["Data", "5", "8"], ["Shape and space", "5", "7"],
                 ["Patterns and relationships", "12", "none"]], [62, 32, 32]),
         _p("Items are set in everyday contexts (money and shopping, the home, travel, the workplace) or in "
            "mathematical contexts."),
         _p("4. The standard and the pass mark", H2),
         _p("4.1 The Level 1 standard is the one the Board's standard-setting panel fixed on the 2022 Level 1 paper "
            "and the Board adopted on 9 May 2022 (record LN1-SS-2022)."),
         _p("4.2 " + SPEC_SENTENCES["pass"] + " A candidate whose mark reaches the pass mark is awarded Level 1 "
            "Numeracy."),
         _p("4.3 The Awards Committee sets each paper's pass mark before the paper opens, on the recommendation of "
            "the assessment manager. A pass mark is not changed once its paper has opened."),
         _p("5. Item quality", H2),
         _p("5.1 " + SPEC_SENTENCES["band"] + " Items outside that range are reported to the Item Review Group, "
            "which decides whether they are kept for later papers; they stay on the paper for which they were set."),
         _p("5.2 Every item is reviewed for bias and accessibility before first use, and its record in the item bank "
            "is reviewed each year after the papers close."),
         _p("6. Access arrangements", H2),
         _p("Centres may give a candidate up to 25 minutes' extra time, a reader for the instructions (not the "
            "items) or a separate room, as recorded on the candidate's registration. No other change to the paper "
            "is made."),
         Spacer(1, 6),
         _p("Document control: version 2026.1; owner, Assessment Manager; next review March 2028.", SMALL)]
    O.build(path, s, "Level 1 Numeracy: qualification specification", P.ORG, "Level 1 Numeracy specification, "
            "version 2026.1", P.ORG + " | LN1 specification 2026.1",
            dt.datetime(2026, 3, 12, 15, 40, tzinfo=CST), dt.datetime(2026, 3, 13, 9, 12, tzinfo=CST))


def standard_record(path):
    rounds = [["Round", "Panellists", "Median of panellists' totals", "Range of totals", "Board's note"],
              ["1 (item ratings, before discussion)", "12", "25.4", "21.9 to 29.6", "item data not yet shown"],
              ["2 (after discussion of the ratings)", "12", "26.0", "23.8 to 28.1", "item facility shown"],
              ["3 (final ratings)", "12", "26.2", "24.6 to 27.5", "adopted, rounded to 26"]]
    s = [_p("Level 1 Numeracy: standard-setting record", H1),
         _p("%s. Record LN1-SS-2022. Panel met 26 and 27 April 2022, Winnipeg; adopted by the Board 9 May 2022." % P.ORG,
            SMALL),
         Spacer(1, 4),
         _p("1. Panel", H2),
         _p("Twelve panellists: seven adult numeracy tutors from community learning centres in both provinces, two "
            "apprenticeship preparation instructors, two of the Board's markers and one employer representative. "
            "Each had taught or assessed Level 1 learners within the last two years. The Board's assessment staff "
            "facilitated and did not rate."),
         _p("2. Method", H2),
         _p("The panel worked from the Level 1 performance descriptors and the 2022 Level 1 paper. Panellists first "
            "agreed a description of a candidate who just meets the Level 1 standard, then rated each of the paper's "
            "40 items: the chance, out of 100, that such a candidate answers it correctly. A panellist's total is the "
            "sum of their ratings over the 40 items, read as the mark such a candidate can be expected to score. "
            "Ratings were made three times; between rounds the panel discussed the items with the widest spread of "
            "ratings and, before the second round, saw each item's facility from the 2022 sittings to date."),
         _table(rounds, [44, 18, 34, 28, 40]),
         _p("3. Outcome", H2),
         _p("The panel recommended, and the Board adopted on 9 May 2022, the Level 1 standard as the performance of a "
            "candidate who just meets the Level 1 descriptors: such a candidate can be expected to score 26 of the 40 "
            "marks on the 2022 Level 1 paper. The 2022 pass mark was set at 26."),
         _p("4. Evaluation", H2),
         _p("All twelve panellists rated the training and the process as clear or very clear; eleven were confident "
            "or very confident in the final recommendation and one was neutral. The facilitators' notes record no "
            "procedural concerns."),
         Spacer(1, 6),
         _p("Facilitated by the Board's assessment staff; record prepared by the Assessment Manager, 20 May 2022.",
            SMALL)]
    O.build(path, s, "Level 1 Numeracy: standard-setting record", P.ORG, "Standard-setting record LN1-SS-2022",
            P.ORG + " | LN1-SS-2022", dt.datetime(2022, 5, 20, 14, 5, tzinfo=CDT),
            dt.datetime(2022, 5, 20, 16, 48, tzinfo=CDT))


def minute(path, l1_2026, l2_2026):
    s = [_p("Awards Committee: minute of the meeting of 17 September 2026", H1),
         _p("%s. Held by video call, 10:00 to 11:35 Central. Unconfirmed: to be confirmed at the next meeting of the "
            "Committee." % P.ORG,
            SMALL),
         Spacer(1, 4),
         _p("Present: %s (chair), %s (Assessment Manager), %s (psychometrician), two centre representatives (Westman, "
            "Regina and South), the Level 2 lead marker. Apologies: the Saskatoon and Central centre representative."
            % (PEOPLE["chair"], PEOPLE["manager"], PEOPLE["psychometrician"])),
         _p("1. 2026 sittings", H2),
         _p("The Assessment Manager reported %d Level 1 and %d Level 2 sittings to 31 August. Both 2026 papers close "
            "on 30 October as usual; the item bank's annual run will follow once marking and appeals are complete."
            % (l1_2026, l2_2026)),
         _p("2. Papers for 2027", H2),
         _p("The Committee approved the 2027 Level 1 and Level 2 papers as assembled by the Item Review Group against "
            "version 2026.1 of the specifications. The 2027 Level 1 paper is the first under the revised strand "
            "structure. Both papers will be loaded to the platform in January 2027 and open on 1 February."),
         _p("3. Pass marks for 2027", H2),
         _p("The pass marks for the 2027 papers will be set at the meeting of 3 December 2026. The Assessment "
            "Manager will bring the recommendation for Level 1 with its working, the item table the Committee "
            "asked for last year and the regional figures the regional coordinators requested."),
         _p("4. Centre matters", H2),
         _p("The computer suite audit of the centres is complete and the report will go to the operations group. "
            "The learner confidence survey closed on 30 June; the Board's research officer will report in the new "
            "year. Two Winnipeg centres merged on 1 July 2025 under the North End code; their earlier records stay "
            "under their own codes."),
         _p("5. Next meeting", H2),
         _p("3 December 2026, 10:00 Central."),
         Spacer(1, 6),
         _p("Minute taken by the Board's committee secretary.", SMALL)]
    O.build(path, s, "Awards Committee minute, 17 September 2026", P.ORG, "Awards Committee minute 2026-09-17",
            P.ORG + " | Awards Committee 2026-09-17", dt.datetime(2026, 9, 21, 11, 20, tzinfo=CDT),
            dt.datetime(2026, 9, 21, 11, 54, tzinfo=CDT))


def email(path):
    body = (
        "Yvette,\n\n"
        "Ahead of 3 December, could you bring the Committee your recommended pass mark for the 2027 Level 1 "
        "Numeracy paper, with your working. The October sittings are all in now and Andrew tells me the bank's "
        "annual run is done.\n\n"
        "Two things the Committee will want beside it. First, the item table we asked for last year: each item on "
        "the paper with how a candidate right at the standard is likely to do on it, and whether it sits inside "
        "the band in section 5 of the specification. Second, the regional coordinators want to know how the "
        "learners who sat the 2026 paper at their centres would be expected to do on the 2027 one, as a mark for "
        "each region, so they can plan tutor time for the new strand.\n\n"
        "The papers go to the platform in January, so whatever we set on the 3rd is what the year runs on.\n\n"
        "Thanks,\n\n"
        "Shawn Simpson\nChair, Awards Committee\n%s\n" % P.ORG)
    hdr = ("Message-ID: <20261109094112.5f2c1e@pacb-adult-credentials.ca>\r\n"
           "Date: Mon, 9 Nov 2026 09:41:12 -0600\r\n"
           "From: Shawn Simpson <s.simpson@pacb-adult-credentials.ca>\r\n"
           "To: Yvette Clark <y.clark@pacb-adult-credentials.ca>\r\n"
           "Cc: Andrew Adams <a.adams@pacb-adult-credentials.ca>\r\n"
           "Subject: 2027 Level 1 pass mark for 3 December\r\n"
           "MIME-Version: 1.0\r\n"
           "Content-Type: text/plain; charset=utf-8\r\n"
           "Content-Transfer-Encoding: 8bit\r\n\r\n")
    open(path, "wb").write((hdr + body.replace("\n", "\r\n")).encode("utf-8"))
