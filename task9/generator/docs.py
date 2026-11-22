"""task9 architecture 5, the organisation's own workbooks and documents: the platform change calendar, the feature
platform's 2027 roadmap, the data planning team's 2027 labelled-row plan, the model stability standard and the
covenant's tier stability schedule. Documents file the WHAT (what a source's movement is, the bands, the shares, the
covenant test, the tiers and the snapshot calendar) and never how anything is estimated."""
import datetime as dt
import os
import sys

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(HERE, "..", "..", ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import postprocess  # noqa: E402
import core as C  # noqa: E402
import pack as P  # noqa: E402

ORG = "Garrane Risk"
IST = dt.timezone(dt.timedelta(hours=1))     # Irish summer time
GMT = dt.timezone.utc
FILES = {"calendar": "platform_change_calendar.xlsx", "roadmap": "feature_platform_roadmap_2027.xlsx",
         "plan": "labelled_row_plan_2027.xlsx", "standard": "gms_model_stability_standard_2026.pdf",
         "covenant": "acquirer_agreement_schedule_c_tier_stability.pdf"}
CHANGES = (("PC-24-031", "runtime", "Training runtime image garrane-train:4.1.0"),
           ("PC-24-047", "warm", "Weekly refits warm-started from the previous model, with the long training window"),
           ("PC-25-012", "amp", "Mixed-precision training (bf16)"))
PINNED = ("PC-26-058", "Pinned feature views for training and scoring")


def _head(ws, row):
    for c in ws[row]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DCE3EC")
        c.alignment = Alignment(wrap_text=True, vertical="top")


def _widths(ws, widths):
    for j, wd in enumerate(widths, 1):
        ws.column_dimensions[chr(64 + j)].width = wd


def calendar(w, target):
    r = np.random.default_rng(C.SEED + 111)
    wb = Workbook()
    ws = wb.active
    ws.title = "Changes"
    ws.append(["change_ref", "change", "model_family", "planned_week", "status", "completed_on"])
    _head(ws, 1)
    for ref, key, label in CHANGES:
        roll = w[key]
        for f in sorted(range(C.F), key=lambda x: P.CODE[x]):
            d = P.monday(roll["declared"][f]) + dt.timedelta(days=int(r.integers(0, 5)))
            ws.append([ref, label, P.CODE[f], P.isow(roll["planned"][f]), "completed", d])
            ws.cell(row=ws.max_row, column=6).number_format = "dd/mm/yyyy"
    for f in sorted(range(C.F), key=lambda x: P.CODE[x]):
        ws.append([PINNED[0], PINNED[1], P.CODE[f], P.isow(w["fv_planned"][f]), "scheduled", None])
    _widths(ws, (11, 62, 13, 13, 11, 13))
    ws.freeze_panes = "A2"
    lg = wb.create_sheet("Legend")
    for row in (["Column", "What it records"],
                ["change_ref", "The platform change's reference in the change board's register"],
                ["change", "What the change is"],
                ["model_family", "The model family the row is for, by its registry code"],
                ["planned_week", "The ISO week the change is planned for the family"],
                ["status", "scheduled, in progress or completed"],
                ["completed_on", "The date the image or option was released to the family's training environment"]):
        lg.append(row)
    _head(lg, 1)
    _widths(lg, (16, 84))
    path = os.path.join(target, FILES["calendar"])
    wb.save(path)
    postprocess.normalize_ooxml(path, "Marie O'Reilly", "Marie O'Reilly", "2024-06-24T09:12:00Z",
                                "2026-11-16T14:37:52Z", excel=True, company=ORG)


def roadmap(w, target):
    r = np.random.default_rng(C.SEED + 112)
    wb = Workbook()
    ws = wb.active
    ws.title = "2027 roadmap"
    ws.append(["release_ref", "target_refresh", "quarter", "feature_groups", "model_families_touched", "owner"])
    plan_groups = P.release_groups(w)[1]
    _head(ws, 1)
    for k, t in enumerate(w["plan_weeks"]):
        d = P.monday(t)
        q = "Q%d" % ((d.month - 1) // 3 + 1)
        g = ";".join(plan_groups[k])
        fams = ";".join(P.CODE[f] for f in range(C.F) if w["plan_hits"][k, f])
        ws.append(["FR-27-%02d" % (k + 1), d, q, g, fams, str(r.choice(["Shauneen Miley", "Cassie Gilbride"]))])
        ws.cell(row=ws.max_row, column=2).number_format = "dd/mm/yyyy"
    _widths(ws, (11, 14, 8, 44, 64, 16))
    ws.freeze_panes = "A2"
    path = os.path.join(target, FILES["roadmap"])
    wb.save(path)
    postprocess.normalize_ooxml(path, "Shauneen Miley", "Cassie Gilbride", "2026-09-07T10:03:00Z",
                                "2026-10-29T16:48:15Z", excel=True, company=ORG)


def plan(w, target):
    rows_int = np.rint(w["rows"]).astype(np.int64)
    fams = sorted(range(C.F), key=lambda x: P.CODE[x])
    wb = Workbook()
    ws = wb.active
    ws.title = "Labelled rows"
    ws.append(["label_week"] + [P.CODE[f] for f in fams])
    _head(ws, 1)
    for t in range(C.T, 183):
        ws.append([P.monday(t)] + [int(rows_int[f, w["wk0"] + t]) for f in fams])
        ws.cell(row=ws.max_row, column=1).number_format = "dd/mm/yyyy"
        for j in range(2, C.F + 2):
            ws.cell(row=ws.max_row, column=j).number_format = "#,##0"
    _widths(ws, [13] + [10] * C.F)
    ws.freeze_panes = "B2"
    bk = wb.create_sheet("Book")
    bk.append(["model_family", "scored_merchants_dec_2027"])
    _head(bk, 1)
    for f in fams:
        bk.append([P.CODE[f], int(round(w["merch"][f] * (1 + w["growth"][f])))])
        bk.cell(row=bk.max_row, column=2).number_format = "#,##0"
    _widths(bk, (14, 26))
    path = os.path.join(target, FILES["plan"])
    wb.save(path)
    postprocess.normalize_ooxml(path, "Tamara O'Rooney", "Tamara O'Rooney", "2026-10-05T08:41:00Z",
                                "2026-11-09T11:26:03Z", excel=True, company=ORG)


# ---------------------------------------------------------------------------------------------- documents
def _styles():
    ss = getSampleStyleSheet()
    body = ParagraphStyle("body", parent=ss["Normal"], fontName="Helvetica", fontSize=9.3, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.8, leading=16.2,
                        spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=10.0, leading=13.4,
                        spaceBefore=7, spaceAfter=3, keepWithNext=1)
    cell = ParagraphStyle("cell", fontName="Helvetica", fontSize=8.4, leading=10.2)
    return body, h1, h2, cell


def _grid(rows, widths, cell):
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=widths, repeatRows=1)
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t


STANDARD = [
    ("1. Scope", [
        "1.1 This standard sets how the model risk committee places each model-side source of movement in the Garrane "
        "Merchant Score for an assessment year, and what each placement requires. It covers every model family in the "
        "model registry. The assessment for a year is made in November of the year before, on the records to the "
        "latest weekly refresh, and each figure in it is given as a committed estimate.",
        "1.2 The model-side sources are:",
        [["Source", "What it is"],
         ["Optimisation noise", "the randomness of training itself: initial weights, the order rows are seen in, the seed"],
         ["Training data", "the labelled rows a family's weekly refit is trained on"],
         ["Retunes", "a change to a family's training configuration made by the retune job"],
         ["Feature releases", "a change to a feature group a family's model reads, released by the feature platform"],
         ["Label revisions", "changes to the labels of rows already in a family's training data (chargebacks, "
                             "disputes and outcomes that arrive late)"]],
        "1.3 A merchant's own change (its business, its customers, its chargebacks as they happen) is not a "
        "model-side source."]),
    ("2. The assessment year", [
        "2.1 The assessment year's feature releases are the feature platform's roadmap for that year as filed with "
        "the committee, and its labelled training rows are the data planning team's plan for that year as filed."]),
    ("3. A source's movement", [
        "3.1 A source's movement is the root-mean-square change in a merchant's score between two consecutive "
        "quarter-end snapshots that the source alone produces, every scored merchant counted once and each model "
        "family weighted by its scored merchants at the latest quarter-end snapshot.",
        "3.2 For an assessment year it is the expected movement over the four snapshot pairs that close in that year, "
        "the snapshots being those of the covenant schedule. It is stated in score points."]),
    ("4. Bands", [
        "4.1 Each source is placed in one band on its movement for the assessment year:",
        [["Band", "Movement", "What it requires"],
         ["Monitor", "under 5.5 points", "quarterly reporting to the committee"],
         ["Remediation plan", "5.5 points or more and under 8 points",
          "a plan to bring the source under 5.5 points, filed with the committee by 31 January"],
         ["Escalation", "8 points or more", "escalation to the board risk committee and a plan filed by 31 January"]]]),
    ("5. Shares", [
        "5.1 A source's share is its mean-square movement as a share of the sum of the model-side sources' "
        "mean-square movements, in per cent.",
        "5.2 Merchants' own change is the mean-square change in a merchant's score over thirteen weekly refreshes in "
        "the record, less the model-side sources' mean-square movements as they stood in the record. It is reported "
        "apart, as a share of all movement (merchants' own change and the model-side sources together)."]),
    ("6. The covenant test", [
        "6.1 With the placements the committee reports the share of merchants expected to change tier between "
        "consecutive quarter-end snapshots in the assessment year, and the same share with the movement of every "
        "source placed in a remediation plan or escalation taken out in full. Tiers, the cap and the panel are those "
        "of the covenant schedule."]),
    ("7. Review", [
        "7.1 The committee reviews this standard each autumn, before the assessment."]),
]

COVENANT = [
    ("C1. Tiers", [
        "C1.1 The Garrane Merchant Score runs from 0 to 1,000; a higher score is a higher risk. Each merchant is placed "
        "in a tier on its score:",
        [["Tier", "Score"], ["1", "under 400"], ["2", "400 or more and under 500"], ["3", "500 or more and under 600"],
         ["4", "600 or more"]],
        "C1.2 Scores and tiers are refreshed every Monday and delivered to the Acquirer the same day."]),
    ("C2. Quarter-end snapshots", [
        "C2.1 The tiers the covenant reads are those of the quarter-end snapshots, every thirteenth weekly refresh, "
        "on these Mondays:",
        [["Year", "Snapshots"],
         ["2025", "22 December"],
         ["2026", "23 March, 22 June, 21 September, 21 December"],
         ["2027", "22 March, 21 June, 20 September, 20 December"]]]),
    ("C3. The stability covenant", [
        "C3.1 Between two consecutive quarter-end snapshots no more than 12 per cent of scored merchants may change "
        "tier, measured on the monitoring panel.",
        "C3.2 Where a year's measured share exceeds the cap, Garrane Risk files a stability plan with the Acquirer "
        "with its expected share for the next year, before 31 January."]),
    ("C4. The monitoring panel", [
        "C4.1 The monitoring panel is one merchant in five of each model family's scored book, drawn at random on 1 "
        "July 2024 and scored in production every week. A panel merchant that leaves its acquirer's book is not "
        "replaced. A share of tier changes between two snapshots counts the panel merchants scored at both."]),
]


def _pdf(target, key, title, head, sections, author, subject, footer, created, modified, widths):
    body, h1, h2, cell = _styles()
    story = [Paragraph(title, h1), _grid(head, [44 * 2.83, 118 * 2.83], cell), Spacer(1, 6)]
    for hd, paras in sections:
        story.append(Paragraph(hd, h2))
        for p in paras:
            if isinstance(p, list):
                story.append(_grid(p, [x * 2.83 for x in widths[len(p[0])]], cell))
            else:
                story.append(Paragraph(p, body))
    O.build(os.path.join(target, FILES[key]), story, title=title, author=author, subject=subject, footer=footer,
            created=created, modified=modified, font="Liberation Sans")


def documents(target):
    _pdf(target, "standard", "Model stability standard for the Garrane Merchant Score",
         [["Document", "Model stability standard, version 2"],
          ["Owner", "Iona Cairns, head of model risk"],
          ["Approved", "Julie-Anne Inglis, chief risk officer, 12 October 2026"],
          ["Replaces", "version 1 of 3 November 2025"]],
         STANDARD, "Iona Cairns", "Model stability standard", "%s, model stability standard, version 2" % ORG,
         dt.datetime(2026, 10, 12, 15, 4, tzinfo=IST), dt.datetime(2026, 10, 12, 15, 4, tzinfo=IST),
         {2: (40, 122), 3: (34, 56, 72)})
    _pdf(target, "covenant", "Schedule C: tier stability",
         [["Agreement", "Acquirer services agreement, Garrane Merchant Score"],
          ["Schedule", "C, tier stability, as amended 19 January 2026"],
          ["For Garrane Risk", "Richard McLeer, director of acquirer partnerships"],
          ["In force", "from the snapshot of 22 December 2025"]],
         COVENANT, "Richard McLeer", "Schedule C, tier stability", "Acquirer services agreement, Schedule C",
         dt.datetime(2026, 9, 2, 10, 47, tzinfo=IST), dt.datetime(2026, 9, 2, 10, 51, tzinfo=IST),
         {2: (30, 132), 3: (34, 56, 72)})


def write_all(w, target):
    calendar(w, target)
    roadmap(w, target)
    plan(w, target)
    documents(target)
