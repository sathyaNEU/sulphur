"""task5 architecture 4: the pack's documents in their issuers' genres.

The Community Transition Fund Act (the Legislature's enrolled act), the data sharing agreement between the
Unemployment Insurance Tax Division and the Labor Market Information section (its schedules list the fields the
extract carries), the Fund administrator's request for the certification, and the Division's notice of 2027
contribution rates. Each is laid out by the house writer's Word stage and saved in Word's own form."""
import datetime as dt
import email.utils

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

import world as W

BODY = ParagraphStyle("body", fontName="Times-Roman", fontSize=11, leading=14.2, spaceAfter=7)
SMALL = ParagraphStyle("small", parent=BODY, fontSize=9.5, leading=12, spaceAfter=4)
HEAD = ParagraphStyle("head", parent=BODY, fontName="Times-Bold", fontSize=11.5, spaceBefore=6, spaceAfter=5)
TITLE = ParagraphStyle("title", parent=BODY, fontName="Times-Bold", fontSize=14, alignment=TA_CENTER, spaceAfter=4)
CENTER = ParagraphStyle("center", parent=BODY, alignment=TA_CENTER, spaceAfter=3)
SANS = ParagraphStyle("sans", fontName="Helvetica", fontSize=9.5, leading=12.4, spaceAfter=6)
SANSB = ParagraphStyle("sansb", parent=SANS, fontName="Helvetica-Bold", fontSize=10, spaceBefore=5, spaceAfter=4)
SANST = ParagraphStyle("sanst", parent=SANS, fontName="Helvetica-Bold", fontSize=13, spaceAfter=2)
CELL = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
CELLB = ParagraphStyle("cellb", parent=CELL, fontName="Helvetica-Bold")

INV = b"D:20000101000000+00'00'"


def _pdfdate(d):
    return ("D:%s-05'00'" % d.strftime("%Y%m%d%H%M%S")).encode()


def _build(path, story, title, author, subject, created, modified, footer=None, company=None):
    """the office's document as its word processor saves it: the story laid out by the house writer's Word stage
    (officepdf) and saved in Word's own form (postprocess.normalize_docx), stamped with its issue and last save"""
    import hashlib
    from zoneinfo import ZoneInfo
    from docx import Document
    from docx.enum.text import WD_BREAK
    from docx.shared import Mm, Pt, RGBColor
    import officepdf as OP
    import postprocess as PP
    OP.FONT = "Times New Roman" if "Act" in title else "Arial"
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    sec.left_margin = sec.right_margin = Mm(25.4)
    sec.top_margin, sec.bottom_margin = Mm(22.9), Mm(22.9)
    normal = doc.styles["Normal"]
    normal.font.name = OP.FONT
    normal.font.size = Pt(10)
    for fl in story:
        if isinstance(fl, Paragraph):
            OP._paragraph(doc, fl)
        elif isinstance(fl, Table):
            OP._table(doc, fl)
        elif isinstance(fl, KeepTogether):
            OP._keep(doc, fl._content)
        elif isinstance(fl, Spacer):
            sp = doc.add_paragraph()
            sp.paragraph_format.space_after = Pt(0)
            sp.paragraph_format.line_spacing = Pt(max(1, fl.height))
        elif isinstance(fl, PageBreak):
            doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)
    if footer:
        fp = sec.footer.paragraphs[0]
        r = fp.add_run(footer.replace("%(page)d", ""))
        r.font.name = OP.FONT
        r.font.size = Pt(8)
        r.font.color.rgb = RGBColor.from_string("444444")
        OP._page_field(fp)
    tz = ZoneInfo("America/New_York")
    utc = lambda d: d.replace(tzinfo=tz).astimezone(dt.timezone.utc)
    cp = doc.core_properties
    cp.title, cp.author, cp.subject, cp.last_modified_by = title, author, subject, author
    cp.created, cp.modified = utc(created).replace(tzinfo=None), utc(modified).replace(tzinfo=None)
    cp.revision = 1
    doc.save(path)
    seed = int(hashlib.blake2b(title.encode(), digest_size=4).hexdigest(), 16)
    PP.normalize_docx(path, author, author, utc(created).strftime("%Y-%m-%dT%H:%M:00Z"),
                      utc(modified).strftime("%Y-%m-%dT%H:%M:00Z"), 3 + seed % 4, 24 + seed % 50, seed, title=title,
                      company=company or author)


def _table(rows, widths, head=True, font=CELL):
    data = [[Paragraph(str(x), CELLB if (head and k == 0) else font) for x in r] for k, r in enumerate(rows)]
    t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("LINEBELOW", (0, 0), (-1, 0), 0.7, colors.black),
          ("TOPPADDING", (0, 0), (-1, -1), 2.2), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2),
          ("LEFTPADDING", (0, 0), (-1, -1), 3), ("RIGHTPADDING", (0, 0), (-1, -1), 3)]
    if head:
        st.append(("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.92, 0.92, 0.92)))
    t.setStyle(TableStyle(st))
    return t


# ------------------------------------------------------------------------------------------------------- the Act
ACT_SECTIONS = [
    ("Section 1. Short title.", ["This act may be cited as the Community Transition Fund Act."]),
    ("Section 2. Definitions.", [
        "In this act:",
        "(a) “Board” means the Community Transition Fund Board established in section 3.",
        "(b) “Commissioner” means the Commissioner of Labor.",
        "(c) “Covered employment,” for a county and a month, means the number of workers in employment covered by "
        "the Unemployment Insurance Law for the payroll period that includes the twelfth day of the month at worksites "
        "located in the county. It is the sum over every employer subject to that Law on any day of the calendar "
        "quarter that contains the month.",
        "(d) “Employer subject to the Unemployment Insurance Law” has the meaning given in section 41-102 of that "
        "Law. An employing unit is subject to the Law from the first day on which it has a worker in covered employment, "
        "whether or not an account has been established for it, and remains subject until the day its account is closed, "
        "inactivated or transferred takes effect.",
        "(e) “Fund year” means the calendar year in which grants under section 6 are made.",
    ]),
    ("Section 3. Fund; Board.", [
        "(a) There is established in the Department of Commerce the Community Transition Fund, consisting of money "
        "appropriated to it and any interest earned on it. Money in the fund does not lapse.",
        "(b) The Community Transition Fund Board consists of the Secretary of Commerce or the Secretary’s designee, "
        "who chairs it; the Commissioner or the Commissioner’s designee, who does not vote on a designation; two "
        "members appointed by the Governor who represent county government; and one member appointed by the Governor "
        "who represents organized labor. The Department of Commerce staffs the Board.",
    ]),
    ("Section 4. Designation.", [
        "For each fund year, the Board shall designate every county whose covered employment for December of the year "
        "before the fund year, as certified under section 5, changed against its covered employment for December of the "
        "year before that by minus 2.0 percent or lower, the change being expressed as a percent and rounded to one "
        "decimal place. A county designated for a fund year is eligible for grants under section 6 in that year. The "
        "first fund year is 2027.",
    ]),
    ("Section 5. Certification.", [
        "(a) Not later than March 1 of each fund year, the Commissioner shall certify to the Board, for each county, the "
        "Department of Labor’s best estimate of covered employment for December of the year before the fund year, made "
        "from the records of the Unemployment Insurance Tax Division as they stand at the close of February 15 of the "
        "fund year; covered employment for December of the year before that, from the same records as they stand at the "
        "same date; and the change between the two.",
        "(b) The certification shall count every employer subject to the Unemployment Insurance Law for the quarter, "
        "whether or not its contribution report for the quarter has been received and whether or not an account has been "
        "established for it when the Commissioner certifies, and shall state for each county how many of the jobs "
        "certified are on reports received and how many are estimated.",
        "(c) With the certification, the Commissioner shall report to the Board how the covered employment certified for "
        "the earlier December differs from the figure the Department has published for it, and why; and what the same "
        "estimate would have given for the earlier December from the Division’s records as they stood at the close of "
        "February 15 of the year before the fund year, beside the figure certified for it.",
        "(d) With the certification, the Commissioner shall deliver to the Board a list of the employers counted for "
        "the fourth calendar quarter of the year before the fund year, showing for each employer and each county in "
        "which it has a worksite the covered employment for December that the certification counts, and whether the "
        "employer’s report for that quarter had been received. The list is confidential under section 41-712 of the "
        "Unemployment Insurance Law and may be used only for the Board’s audit of the certification.",
    ]),
    ("Section 6. Grants.", [
        "(a) From the fund, the Board may make grants to a designated county, or to a nonprofit workforce board or "
        "economic development organization serving it, for training and placement of dislocated workers, for "
        "assistance to small employers in the county, and for planning the county’s economic transition.",
        "(b) The Board shall allocate the amount available for a fund year among the designated counties in proportion "
        "to the covered employment each lost between the two months of December certified for it, except that no "
        "county may receive more than 40 percent of the amount available.",
    ]),
    ("Section 7. Appropriation.", [
        "There is appropriated from the general fund to the Community Transition Fund $24,000,000 for the fiscal year "
        "beginning July 1, 2026.",
    ]),
    ("Section 8. Effective date.", ["This act takes effect July 1, 2026."]),
]


def write_act(path):
    st = [Paragraph("STATE OF FRANKLIN", CENTER), Paragraph("FIFTY-NINTH LEGISLATURE, 2026 REGULAR SESSION", CENTER),
          Spacer(1, 6), Paragraph("ENROLLED SENATE BILL NO. 312", TITLE), Spacer(1, 4),
          Paragraph("AN ACT establishing the Community Transition Fund and its Board; providing for the designation of "
                    "counties that have lost covered employment and for grants to them; and making an appropriation.",
                    CENTER), Spacer(1, 10),
          Paragraph("<i>Be it enacted by the Legislature of the State of Franklin:</i>", BODY), Spacer(1, 4)]
    for head, paras in ACT_SECTIONS:
        block = [Paragraph(head, HEAD)] + [Paragraph(p, BODY) for p in paras]
        st.append(KeepTogether(block))
    st += [Spacer(1, 14), Paragraph("Passed the Senate April 9, 2026. Passed the House of Representatives April 21, 2026.", SMALL),
           Paragraph("Approved by the Governor May 4, 2026. Chapter 147, Laws of 2026.", SMALL)]
    _build(path, st, "Enrolled Senate Bill No. 312 (2026), Community Transition Fund Act", "Franklin Legislature",
           "Community Transition Fund Act, Chapter 147, Laws of 2026", dt.datetime(2026, 4, 27, 15, 18, 0),
           dt.datetime(2026, 5, 6, 9, 41, 12), footer="ESB 312 (2026), page %(page)d")
    return [p for _, ps in ACT_SECTIONS for p in ps]


# ------------------------------------------------------------------------------------------- the data agreement
AGREEMENT = [
    ("1. Parties and purpose", [
        "This memorandum of understanding is between the Unemployment Insurance Tax Division (the Division) and the "
        "Labor Market Information section (the Section) of the Franklin Department of Labor. The Division supplies the "
        "Section with employer account and contribution report data for the Section’s statistical work: the "
        "covered employment and wages program it runs with the U.S. Bureau of Labor Statistics, and the statistics "
        "state law asks the Department to certify."]),
    ("2. Data supplied", [
        "The Division supplies four extracts, refreshed each business night, each carrying everything the Division’s "
        "systems hold through the date of the extract: the quarterly contribution reports, the employer accounts, the "
        "history of changes to account status and the multiple worksite reports. Schedules A to D set out what each "
        "holds, and no extract holds more. The Section does not receive taxpayer correspondence, payments, liens, audit files, or "
        "information about any person other than the employer and its worksites."]),
    ("3. Use and confidentiality", [
        "The data are confidential under section 41-712 of the Unemployment Insurance Law and 20 CFR part 603. The "
        "Section uses them for statistical purposes only, publishes no figure from which an employer’s data can be "
        "identified, and may share employer-level data only where a state law requires it, under the terms of that law."]),
    ("4. Term", ["This memorandum takes effect July 1, 2025 and continues until either party ends it with ninety days’ notice."]),
]
SCHED = {
    "A": ("Schedule A. Quarterly contribution reports",
          "Every report posted to an employer account, including each amended report and any report received more than "
          "once. Each gives the employer’s account number, the year and quarter the report covers, whether it is the "
          "first report received for the quarter (ORIGINAL) or a report that replaces an earlier one for the same quarter "
          "(AMENDED), the number of covered workers who worked during or received pay for the payroll period that includes "
          "the twelfth day of each month of the quarter, the wages paid in the quarter in dollars and the part subject to "
          "contributions, and the date and time the Division’s system received the report. A report received on paper "
          "carries the date it was received, with the time recorded as 00:00:00. A report received from an employing unit "
          "that has no account is held, and is posted with the date and time it was received once the account is "
          "established. The contribution report is the record of an account’s employment for the quarter."),
    "B": ("Schedule B. Employer accounts",
          "Every account, active or inactive, as at the date of the extract: the account number (seven digits, a hyphen "
          "and a check digit); the employer’s legal name and any name it trades under; its ownership (5 private, 3 "
          "local government, 2 state government); the industry code assigned at registration or at the latest review, "
          "which for a code assigned before 2022 may be a NAICS 2017 code; the county of the employer’s principal "
          "place of business in Franklin, or of its only worksite; the first day on which the employer had a worker in "
          "covered employment, from which the account is liable for contributions (month, day, year); the date the "
          "Division established the account (month, day, year); whether the account is active or inactive, and the date "
          "that status took effect; whether the employer reports its employment by worksite on the multiple worksite "
          "report; and, where the account succeeded to another employer’s business, that employer’s account."),
    "C": ("Schedule C. Account status history",
          "Every change to an account’s status since January 1, 2023: the account number; the change (LIABLE, a new "
          "liability for a new employer or a successor; CLOSED, the employer has told the Division it has ceased business; "
          "INACTIVATED, the Division has inactivated the account; TRANSFERRED, the employer’s business has passed to a "
          "successor); the date the change takes effect, which for a new liability is the first day of covered "
          "employment, for a closure or an inactivation the first day for which the employer had no workers in covered "
          "employment and for a transfer the date of transfer; the date the Division entered the change, which for a new "
          "liability is the date the account was established; and the Division’s reason text."),
    "D": ("Schedule D. Multiple worksite reports",
          "Every worksite on each multiple worksite report received: the account number, as digits only; the worksite’s "
          "reporting unit number within the account; the year and quarter; the worksite’s county and city; its "
          "industry code; the worksite’s employment for each month of the quarter; and the date the report was "
          "received (month, day, year). The multiple worksite report distributes the employment on the account’s "
          "contribution report among its worksites."),
}


def write_agreement(path):
    st = [Paragraph("FRANKLIN DEPARTMENT OF LABOR", SANSB),
          Paragraph("Memorandum of Understanding: Unemployment Insurance Tax Division and Labor Market Information", SANST),
          Paragraph("Data sharing for statistical purposes. Agreement LMI-UI-2025-03, effective July 1, 2025.", SANS), Spacer(1, 6)]
    for head, paras in AGREEMENT:
        st.append(Paragraph(head, SANSB))
        st += [Paragraph(p, SANS) for p in paras]
    st += [Spacer(1, 8), _table([["For the Division", "For the Section"],
                                 ["%s, %s" % (W.PEOPLE["ui_chief"][0], W.PEOPLE["ui_chief"][1]), "%s, %s" % (W.PEOPLE["lmi_director"][0], W.PEOPLE["lmi_director"][1])],
                                 ["Signed June 18, 2025", "Signed June 20, 2025"]], [3.2 * inch, 3.2 * inch]), PageBreak()]
    for k in "ABCD":
        title, body = SCHED[k]
        st.append(Paragraph(title, SANSB))
        st.append(Paragraph(body, SANS))
        st.append(Spacer(1, 8))
    _build(path, st, "LMI-UI-2025-03 Data Sharing Agreement", "Labor Market Information",
           "Memorandum of understanding, UI Tax Division and Labor Market Information", dt.datetime(2025, 6, 9, 11, 26, 0),
           dt.datetime(2025, 6, 20, 14, 2, 47), footer="LMI-UI-2025-03  |  page %(page)d",
           company="Franklin Department of Labor")
    texts = [p for _, ps in AGREEMENT for p in ps]
    for k in "ABCD":
        texts += [SCHED[k][1]]
    return texts


# ------------------------------------------------------------------------------------------------ the request
REQUEST_BODY = """Danielle,

The Board meets on Thursday, March 4 to designate counties for the fund's first year. Under section 5 of the Act the Commissioner's certification is due by March 1: each county's covered employment for December 2026 and December 2025 and the change between them, with the employer list under 5(d).

The Board will also want the two things 5(c) asks for in front of it, since this is the first time anyone has had to stand behind December numbers this early: how December 2025 now compares with what the Department published in June, and what you would have told us a year ago.

A chart of the changes against the 2.0 percent line would help the discussion, and a workbook is fine for the figures.

If anything in the timetable is a problem, let me know this month.

Thanks,
Matt

Matthew Cox
Administrator, Community Transition Fund
Franklin Department of Commerce
(612) 498-3317
"""


def write_request(path):
    who, title, addr = W.PEOPLE["fund_admin"]
    to_who, _, to_addr = W.PEOPLE["lmi_director"]
    d = dt.datetime(2027, 1, 12, 10, 14, 22, tzinfo=dt.timezone(dt.timedelta(hours=-5)))
    hdr = [
        "Return-Path: <%s>" % addr,
        "Received: from mail.commerce.franklin.gov (mail.commerce.franklin.gov [10.41.8.22]) by mx1.labor.franklin.gov "
        "with ESMTPS id 4f1c09a7; Tue, 12 Jan 2027 10:14:24 -0500",
        "Message-ID: <CAF7e1b2a90.3c41d@commerce.franklin.gov>",
        "Date: %s" % email.utils.format_datetime(d),
        "From: %s <%s>" % (who, addr),
        "To: %s <%s>" % (to_who, to_addr),
        "Cc: %s <%s>" % (W.PEOPLE["ui_chief"][0], W.PEOPLE["ui_chief"][2]),
        "Subject: CTF 2027 designation: certification due March 1",
        "MIME-Version: 1.0",
        "Content-Type: text/plain; charset=\"utf-8\"",
        "Content-Transfer-Encoding: 7bit",
    ]
    open(path, "w", encoding="utf-8", newline="").write("\r\n".join(hdr) + "\r\n\r\n" + REQUEST_BODY.replace("\n", "\r\n"))
    return [REQUEST_BODY]


# ------------------------------------------------------------------------------------------- the rate notice
def write_rates(path):
    rows = [["Reserve ratio (percent)", "Contribution rate (percent)"]]
    bands = [("13.0 and over", "0.40"), ("11.0 to 12.9", "0.70"), ("9.0 to 10.9", "1.00"), ("7.0 to 8.9", "1.40"),
             ("5.0 to 6.9", "1.90"), ("3.0 to 4.9", "2.50"), ("1.0 to 2.9", "3.20"), ("0.0 to 0.9", "4.00"),
             ("-2.0 to -0.1", "5.10"), ("-4.0 to -2.1", "6.20"), ("under -4.0", "7.40")]
    rows += [list(b) for b in bands]
    st = [Paragraph("FRANKLIN DEPARTMENT OF LABOR, UNEMPLOYMENT INSURANCE TAX DIVISION", SANSB),
          Paragraph("Notice of 2027 Contribution Rates", SANST), Spacer(1, 6),
          Paragraph("Under section 41-305 of the Unemployment Insurance Law, the Division has computed each employer’s "
                    "contribution rate for calendar year 2027 from the employer’s reserve ratio on the computation date, "
                    "June 30, 2026. Rate notices were mailed to employers on November 30, 2026.", SANS),
          Paragraph("Taxable wage base for 2027: the first $15,400 of wages paid to each worker in the year (2026: $14,600).", SANS),
          Paragraph("Rate for a new employer not yet eligible for an experience rate: 2.70 percent, or the average rate of its "
                    "industry sector if higher, for construction 4.10 percent.", SANS),
          Paragraph("Schedule in effect for 2027: Schedule C, the trust fund balance on September 30, 2026 being 1.12 percent "
                    "of total wages paid in the year ended June 30, 2026.", SANS), Spacer(1, 6),
          _table(rows, [2.6 * inch, 2.6 * inch]), Spacer(1, 10),
          Paragraph("An employer may request a review of its rate within thirty days of the date of its notice. Voluntary "
                    "contributions to lower a 2027 rate are accepted until March 31, 2027.", SANS)]
    _build(path, st, "Notice of 2027 Contribution Rates", "UI Tax Division",
           "2027 unemployment insurance contribution rates", dt.datetime(2026, 11, 23, 16, 4, 0),
           dt.datetime(2026, 11, 30, 8, 30, 5), footer="UI Tax Division  |  2027 rates  |  page %(page)d",
           company="Franklin Department of Labor")
