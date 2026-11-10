"""task2 architecture 5: the pack's documents. Each PDF is a Word document exported by LibreOffice Writer
(officepdf.py); the draft 2027 schedule stays a Word document. They file the WHAT (the metric, the audit, the
deployment dates, the ceilings, the release in force) and say nothing of how 2027 is to be projected or whom a new
dictator resembles."""
import datetime as dt
import os

from docx import Document
from docx.shared import Mm, Pt
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph, Table

import officepdf
import postprocess as PP
import world as W

GMT = dt.timezone.utc
IST = dt.timezone(dt.timedelta(hours=1))
H1 = ParagraphStyle("h1", fontName="Helvetica-Bold", fontSize=14, spaceAfter=6, textColor="#1D3557")
H2 = ParagraphStyle("h2", fontName="Helvetica-Bold", fontSize=10.5, spaceBefore=8, spaceAfter=3, textColor="#1D3557")
BODY = ParagraphStyle("b", fontName="Helvetica", fontSize=9.2, spaceAfter=4)
SMALL = ParagraphStyle("s", fontName="Helvetica", fontSize=8, spaceAfter=2, textColor="#444444")


def P(t, st=BODY):
    return Paragraph(t, st)


def date_of(t):
    y, m = divmod(t, 12)
    return dt.date(W.START[0] + y, m + 1, 1)


def deployment(target):
    rows = [["Hospital", "Site code", "Service available from", "Dictation compulsory from"]]
    avail = {"CLM": dt.date(2021, 9, 6), "RTH": dt.date(2021, 9, 6), "KBR": dt.date(2021, 10, 4),
             "CSL": dt.date(2021, 10, 4), "KNA": dt.date(2021, 11, 1), "DRL": dt.date(2021, 11, 1),
             "SSU": dt.date(2021, 9, 6), "BKU": dt.date(2021, 10, 4)}
    for code, name, _, _, comp, _, _ in W.HOSPITALS:
        rows.append([name, code, avail[code].strftime("%-d %B %Y"), date_of(comp).strftime("%-d %B %Y")])
    s = [P("Shannonside Hospital Group and Larkmoor Speech Limited", SMALL),
         P("Medical dictation services agreement: Schedule 2, Deployment", H1),
         P("Schedule 2 as amended on 1 October 2026 (amendment 4). Replaces Schedule 2 as amended on 3 March 2025.", SMALL),
         P("2.1 Hospitals in scope", H2),
         P("The Service is provided at the hospitals below. From the date the Service is available at a hospital, any "
           "clinician in post there may dictate through it. From the date dictation is compulsory at a hospital, every "
           "clinician in post there dictates clinical correspondence, discharge summaries and reports through the "
           "Service, and so does every clinician who takes up post there later."),
         Table(rows, colWidths=[190, 60, 120, 130]),
         P("2.2 Changes", H2),
         P("Amendment 4 sets the dates on which dictation becomes compulsory at Shannonside University Hospital and "
           "Ballykeel University Hospital. A change to a date in this schedule is agreed in writing by both parties."),
         P("2.3 Data", H2),
         P("The Supplier keeps a record of each clinician's dictations by month and makes it available to the Group on "
           "request; the Group keeps the clinician register.")]
    officepdf.build(os.path.join(target, "services_agreement_schedule2_deployment.pdf"), s,
                    "Schedule 2: Deployment (amendment 4)", "Shannonside Hospital Group, Procurement",
                    "Medical dictation services agreement", "Shannonside Hospital Group | Schedule 2 | Amendment 4",
                    dt.datetime(2026, 9, 24, 15, 10, tzinfo=IST), dt.datetime(2026, 10, 1, 9, 42, tzinfo=IST),
                    producer="LibreOffice 24.2")


def audit_procedure(target):
    s = [P("Larkmoor Speech Limited, Quality Assurance", SMALL),
         P("QA-07 Recognition quality audit", H1),
         P("Version 3, issued 21 November 2022. Owner: Head of Recognition Quality. Applies to every customer from "
           "1 January 2023.", SMALL),
         P("1 Sample", H2),
         P("Each month, at each customer hospital, 2.5 per cent of the month's dictations, rounded to the nearest whole "
           "dictation, are drawn at random from the month's completed dictations at that hospital."),
         P("2 Reference", H2),
         P("A medical transcriptionist types a verbatim reference transcript from the audio. Numbers, units and "
           "punctuation are written as Appendix A sets out, and filled pauses are not transcribed."),
         P("3 Score", H2),
         P("The recognised text is aligned with the reference. Substitutions, deletions and insertions are counted, and "
           "the word error rate is their sum divided by the number of words in the reference."),
         P("4 Second scoring and adjudication", H2),
         P("A second transcriptionist scores about one audit in twenty again. Where the two scores differ, the "
           "adjudication panel's score is recorded as the adjudicated score and replaces the first-pass score."),
         P("5 Unscorable audio", H2),
         P("A dictation whose audio cannot be transcribed is recorded as unscorable and left out of every rate."),
         P("6 Records and reporting", H2),
         P("Each audit is recorded with the dictation, the site, the clinician's staff number and the recognition "
           "release that produced the text. Quality is reported to each customer quarterly."),
         P("Appendix A: normalisation", H2),
         P("Numbers are written as digits; drug doses keep their units; abbreviations are expanded only where the "
           "clinician spoke them in full; punctuation is ignored when counting.")]
    officepdf.build(os.path.join(target, "QA-07_recognition_quality_audit.pdf"), s, "QA-07 Recognition quality audit",
                    "Larkmoor Speech, Quality Assurance", "Recognition quality audit procedure",
                    "Larkmoor Speech | QA-07 v3", dt.datetime(2022, 11, 17, 10, 4, tzinfo=GMT),
                    dt.datetime(2022, 11, 21, 16, 30, tzinfo=GMT), producer="LibreOffice 7.4")


RELNOTES = [
    ("4.0", "14 February 2023", "New acoustic model trained on a further 3,100 hours of clinical audio; a larger "
     "medical vocabulary.", "3.6"),
    ("5.0", "11 June 2024", "Acoustic and language models rebuilt on a new architecture; punctuation by "
     "context; faster first result.", "7.8"),
    ("5.2", "18 March 2025", "Language model adapted to Irish hospital correspondence; drug names updated to the "
     "2025 formulary.", "3.9"),
    ("6.0", "4 November 2025", "Noise-robust front end; better handling of overlapping speech; dose and unit "
     "formatting.", "3.2"),
]


def release_notes(target):
    rows = [["Release", "Released", "Relative reduction in word error rate on the LCB-2 benchmark (%)"]]
    for r, d, _, red in RELNOTES:
        rows.append([r, d, red])
    s = [P("Larkmoor Speech Limited", SMALL), P("Larkmoor Medical Recognition: release notes, 2023 to 2026", H1),
         P("Releases go to every customer on the date shown. Release 3.4 was in service from April 2021.", SMALL)]
    for r, d, note, red in RELNOTES:
        s.append(P("Release %s (%s)" % (r, d), H2))
        s.append(P(note + " Word error rate on Larkmoor's LCB-2 clinical benchmark down %s per cent on the release "
                   "before." % red))
    s += [P("Benchmark summary", H2), Table(rows, colWidths=[60, 110, 300]),
          P("LCB-2 is Larkmoor's held-out benchmark of 41 hours of consented clinical dictation from four countries; "
            "its figures are not a customer's.", SMALL)]
    officepdf.build(os.path.join(target, "recognition_releases_2023_2026.pdf"), s, "Larkmoor Medical Recognition: release notes",
                    "Larkmoor Speech, Product", "Release notes 2023 to 2026", "Larkmoor Speech | Release notes",
                    dt.datetime(2025, 11, 4, 8, 15, tzinfo=GMT), dt.datetime(2025, 11, 4, 12, 2, tzinfo=GMT),
                    producer="LibreOffice 24.2")


def migration_notice(target):
    s = [P("Larkmoor Speech Limited", SMALL), P("Service notice SN-2026-14: moving to the Dublin region", H1),
         P("14 October 2026. To: Irish customers' ICT and procurement leads.", SMALL),
         P("During 2027 Larkmoor moves the service for its Irish customers from its Frankfurt data centre to the new "
           "Dublin region. Each customer moves on a weekend agreed with its ICT team; no dictation is lost and no "
           "downtime is planned outside those weekends."),
         P("Recognition stays on release 6.0 for every Irish customer from 1 January to 31 December 2027, so that the "
           "migration changes one thing at a time. The next recognition release, 7.0, is planned for the first quarter "
           "of 2028, after the migration has finished."),
         P("Customers will receive the migration timetable in November 2026.")]
    officepdf.build(os.path.join(target, "service_notice_SN-2026-14.pdf"), s, "SN-2026-14: moving to the Dublin region",
                    "Larkmoor Speech, Customer Operations", "Service notice", "Larkmoor Speech | SN-2026-14",
                    dt.datetime(2026, 10, 13, 16, 40, tzinfo=IST), dt.datetime(2026, 10, 14, 8, 55, tzinfo=IST),
                    producer="LibreOffice 24.8")


def draft_schedule(target):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(210), Mm(297)
    sec.left_margin = sec.right_margin = Mm(22)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(11)
    paras = [
        ("Shannonside Hospital Group, Procurement", None),
        ("Medical dictation services agreement: draft Schedule 4 (Quality) for 2027", "h"),
        ("Sent to Larkmoor Speech on 14 December 2026. Return with your chosen ceiling by 15 January 2027.", None),
        ("4.1 Definitions", "h2"),
        ("Audited dictation: a dictation drawn for audit under the Supplier's audit procedure QA-07 and scored. Word "
         "error rate: the rate QA-07 records for an audited dictation, the adjudicated score where there is one. Heavy "
         "correction: an audited dictation whose word error rate is above 15 per cent.", None),
        ("4.2 The measure", "h2"),
        ("For each calendar quarter, the heavy correction share is the number of the quarter's audited dictations "
         "needing heavy correction divided by the number of the quarter's audited dictations. Every dictation made "
         "under the Service in the quarter by a clinician of the Group's hospitals is in scope, at every hospital in "
         "Schedule 2, including hospitals where dictation becomes compulsory during the year.", None),
        ("4.3 Ceiling", "h2"),
        ("The Supplier commits to one ceiling for every quarter of 2027. A quarter whose heavy correction share is above "
         "the ceiling earns the Group a service credit of 8 per cent of that quarter's service fee.", None),
        ("Ceiling A: 10 per cent; annual service fee EUR 1,920,000.", "li"),
        ("Ceiling B: 12 per cent; annual service fee EUR 1,845,000.", "li"),
        ("Ceiling C: 14 per cent; annual service fee EUR 1,770,000.", "li"),
        ("Ceiling D: 16 per cent; annual service fee EUR 1,690,000.", "li"),
        ("4.4 Reporting", "h2"),
        ("The Supplier reports each quarter's audited dictations and heavy correction share within 30 days of the "
         "quarter's end, by hospital and for the Group.", None),
        ("Yasmine Ganley, Head of Procurement, Shannonside Hospital Group", None),
    ]
    for t, kind in paras:
        if kind == "h":
            p = doc.add_paragraph()
            r = p.add_run(t)
            r.bold = True
            r.font.size = Pt(14)
        elif kind == "h2":
            p = doc.add_paragraph()
            r = p.add_run(t)
            r.bold = True
        elif kind == "li":
            p = doc.add_paragraph(t)
            p.paragraph_format.left_indent = Mm(8)
        else:
            p = doc.add_paragraph(t)
        p.paragraph_format.space_after = Pt(6)
    cp = doc.core_properties
    cp.title, cp.author, cp.last_modified_by = "Draft Schedule 4 (Quality) 2027", "Yasmine Ganley", "Yasmine Ganley"
    path = os.path.join(target, "draft_schedule4_quality_2027.docx")
    doc.save(path)
    PP.normalize_docx(path, "Yasmine Ganley", "Yasmine Ganley", "2026-12-08T11:20:00Z", "2026-12-14T15:47:00Z", 4, 63,
                      "task2-draft-schedule4", "Draft Schedule 4 (Quality) 2027", "Shannonside Hospital Group")


def write_all(target):
    deployment(target)
    audit_procedure(target)
    release_notes(target)
    migration_notice(target)
    draft_schedule(target)
