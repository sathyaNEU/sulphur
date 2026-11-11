"""task9 (architecture 10): the golden deliverables the prompt asks for, a spreadsheet and a one-page note, written from
the figures as stated (F). Nothing is typed: every number below is read from F.

    write_all(F, golden_dir)
"""
import os

import openpyxl
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.shared import Pt, RGBColor
from openpyxl.chart import BarChart, Reference
from openpyxl.chart.label import DataLabelList
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import params as P
import postprocess as PP

BOOK, NOTE = "Brindlemoor_2027_quoting_plan.xlsx", "Brindlemoor_2027_quoting_memo.docx"
AUTHOR = "Credit Trading Strategy"
STAMPS = {BOOK: ("2026-11-10T15:12:40Z", "2026-11-11T20:47:31Z"), NOTE: ("2026-11-11T16:02:00Z", "2026-11-11T21:24:00Z")}
HEAD_FILL = PatternFill("solid", fgColor="E9EEF4")
THIN = Side(style="thin", color="B8BEC6")
TYPE = {"AM": "asset managers", "INS": "insurers", "HF": "hedge funds", "RET": "wealth platforms"}
TYPE_CAP = {"AM": "Asset managers", "INS": "Insurers", "HF": "Hedge funds", "RET": "Wealth platforms"}
BAND = {"IG": "investment grade", "HY": "high yield"}
NUMBER = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten",
          11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen", 15: "fifteen", 16: "sixteen"}


BAND_ADJ = {"IG": "investment-grade", "HY": "high-yield"}


def label(seg, cap=False):
    """A segment as the desk names it: "liquid investment-grade bonds for asset managers"."""
    b, l, t = seg.split("|")
    s = "%s %s bonds for %s" % (l, BAND_ADJ[b], TYPE[t])
    return s[0].upper() + s[1:] if cap else s


def m(v, k=1):
    """USD millions as the committee reads them."""
    return ("USD %." + str(k) + "f million") % (v / 1e6)


def k(v):
    return "USD {:,.0f}".format(round(v / 1e3) * 1e3)


def joined(xs):
    xs = list(xs)
    if not xs:
        return "none"
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _head(ws, row, labels, widths=None):
    for j, t in enumerate(labels, 1):
        c = ws.cell(row=row, column=j, value=t)
        c.font = Font(bold=True, size=10)
        c.fill = HEAD_FILL
        c.alignment = Alignment(wrap_text=True, vertical="top")
        c.border = Border(bottom=THIN)
    if widths:
        for j, w in enumerate(widths, 1):
            ws.column_dimensions[openpyxl.utils.get_column_letter(j)].width = w


def _title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12)
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(size=10, color="52514E")


def _row(ws, r, vals, fmts=None, bold=False):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=j, value=v)
        f = (fmts or {}).get(j)
        if f:
            c.number_format = f
        if bold:
            c.font = Font(bold=True)


def write_workbook(path, F):
    g = F["gold"]
    segs = F["segments"]
    wb = openpyxl.Workbook()
    usd = "#,##0"
    # ---- the plan
    ws = wb.active
    ws.title = "2027 plan"
    _title(ws, "On the draft schedule the desk plans %s for 2027, against %s on the schedule in force" % (
        m(g["proposed"]), m(g["current"])),
           "USD, the plan's P&L per the quoting policy (edge less the move after each trade once complete, less the offload "
           "charge), the record since January 2023 replayed at each schedule and carried at the requests of the twelve "
           "months to October 2026")
    _head(ws, 4, ["", "USD"], [58, 16])
    rows = [("2027 P&L at the current schedule", g["current"]), ("2027 P&L at the draft schedule", g["proposed"]),
            ("Draft schedule, 10th percentile of the year", g["p10"]), ("Draft schedule, 90th percentile of the year", g["p90"]),
            ("2027 P&L at the draft without the changes that lose money", g["adopt"])]
    for i, (a, v) in enumerate(rows):
        _row(ws, 5 + i, [a, round(v, 0)], {2: usd})
    ws.cell(row=11, column=1, value="Changed segments that lose money: " + joined(label(s) for s in g["lose"])).font = Font(size=10)
    notes = ("Notes: lost requests with no matching customer print on the tape ({:.1f} per cent of losses) are taken as lost "
             "at any quote; a win priced level with the cover at the platform's rounding keeps its win; 144A bonds are "
             "carried with their registered successors; cancelled tape reports are dropped and corrected ones used.").format(
                 100 * (1 - F["match_rate"]))
    ws.cell(row=13, column=1, value=notes).font = Font(size=9, color="52514E")
    ws.freeze_panes = "A5"
    # ---- the changed segments
    ws = wb.create_sheet("Changed segments")
    ig_only = all(s.split("|")[0] == "IG" for s in g["lose"])
    _title(ws, "%s of the draft's %s changes lose money%s" % (NUMBER[len(g["lose"])].capitalize(), NUMBER[len(segs)],
                                                              ", all in investment grade" if ig_only and g["lose"] else ""),
           "Costs after the trade in USD per million face, read once the move "
           "is complete; shares of the segment's requests since January 2023")
    _head(ws, 4, ["Segment", "Half-spread now (cents)", "Draft half-spread (cents)", "Share won at the current schedule", "Share won at the draft",
                  "Cost after the current schedule's trades (USD per million)", "Cost after the trades the draft adds (USD per million)",
                  "2027 P&L change (USD)", "Verdict"], [34, 11, 11, 10, 11, 15, 17, 14, 12])
    for i, s in enumerate(segs):
        d = g["bridge"][s]
        _row(ws, 5 + i, [label(s, True), F["h"][s][0], F["h"][s][1], round(F["today_share"][s], 3), round(g["share"][s], 3),
                         round(g["won_cost"][s], 0), round(g["add_cost"][s], 0) if g["add_cost"][s] is not None else None,
                         round(d, 0), "keep today's quote" if d < 0 else "adopt"],
             {4: "0.0%", 5: "0.0%", 6: usd, 7: usd, 8: usd})
    ws.freeze_panes = "B5"
    # ---- the bridge, with its chart
    ws = wb.create_sheet("Bridge")
    _title(ws, "From %s at the current schedule to %s at the draft, by changed segment" % (m(g["current"]), m(g["proposed"])),
           "USD")
    _head(ws, 4, ["Item", "USD"], [44, 16])
    r = 5
    _row(ws, r, ["Current schedule, 2027", round(g["current"], 0)], {2: usd}, bold=True)
    order = sorted(segs, key=lambda s: g["bridge"][s])
    for s in order:
        r += 1
        _row(ws, r, [label(s, True), round(g["bridge"][s], 0)], {2: usd})
    r += 1
    _row(ws, r, ["Draft schedule, 2027", round(g["proposed"], 0)], {2: usd}, bold=True)
    ch = BarChart()
    ch.type = "bar"
    ch.title = "2027 P&L change by changed segment (USD)"
    ch.y_axis.title = None
    ch.add_data(Reference(ws, min_col=2, min_row=6, max_row=5 + len(order)), titles_from_data=False)
    ch.set_categories(Reference(ws, min_col=1, min_row=6, max_row=5 + len(order)))
    ch.legend = None
    ch.height, ch.width = 9.5, 17
    ch.dataLabels = DataLabelList()
    ch.dataLabels.showVal = True
    ws.add_chart(ch, "D4")
    # ---- the range
    ws = wb.create_sheet("Range")
    _title(ws, "Four years in five the draft makes between %s and %s" % (m(g["p10"]), m(g["p90"])), "USD; {:,} simulated years, each of 251 trading days drawn "
           "from the record's own days in runs of {} days, at the plan's request counts".format(P.SIMS, P.BLOCK))
    _head(ws, 4, ["", "USD"], [44, 16])
    for i, (a, v) in enumerate([("10th percentile", g["p10"]), ("Expected", g["proposed"]), ("90th percentile", g["p90"])]):
        _row(ws, 5 + i, [a, round(v, 0)], {2: usd})
    # ---- the shortcuts beside the golden
    ws = wb.create_sheet("Methods compared")
    _title(ws, "What other readings of the record would plan", "USD; each row is one way of reading the requests, the "
           "evaluations and the tape, with what it would tell the committee")
    _head(ws, 4, ["Reading", "Current schedule", "Draft schedule", "Draft, 10th percentile", "Draft, 90th percentile",
                  "Changed segments it says lose money"], [52, 14, 14, 14, 14, 60])
    rr = 5
    _row(ws, rr, ["This workbook", round(g["current"], 0), round(g["proposed"], 0), round(g["p10"], 0), round(g["p90"], 0),
                  joined(label(s) for s in g["lose"])], {2: usd, 3: usd, 4: usd, 5: usd}, bold=True)
    for name, v in F["routes_shown"].items():
        rr += 1
        _row(ws, rr, [name, round(v["current"], 0), round(v["proposed"], 0), round(v["p10"], 0) if v.get("p10") else None,
                      round(v["p90"], 0) if v.get("p90") else None, joined(label(s) for s in v["lose"])],
             {2: usd, 3: usd, 4: usd, 5: usd})
    for row in ws.iter_rows(min_row=5, max_row=rr):
        row[5].alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    PP.normalize_ooxml(path, AUTHOR, AUTHOR, STAMPS[BOOK][0], STAMPS[BOOK][1], excel=True, company=P.FIRM)


def write_note(path, F):
    g = F["gold"]
    lose = g["lose"]
    pays = [s for s in F["segments"] if s not in lose]
    doc = Document()
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10.5)
    for sec in doc.sections:
        sec.left_margin = sec.right_margin = Pt(64)
        sec.top_margin = sec.bottom_margin = Pt(54)
    p = doc.add_paragraph()
    ig_only = all(s.split("|")[0] == "IG" for s in lose)
    r = p.add_run("The 2027 quoting schedule: approve the draft without %s of its %schanges" % (
        NUMBER[len(lose)], "investment-grade " if ig_only and lose else ""))
    r.bold = True
    r.font.size = Pt(13)
    p = doc.add_paragraph()
    r = p.add_run("Credit trading strategy, 11 November 2026")
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x52, 0x51, 0x4E)
    doc.add_paragraph(
        "On the draft schedule the desk should plan %s of P&L for 2027, against %s on the schedule in force; four years in "
        "five it lands between %s and %s. %s of the draft's %s changes lose money: %s. Without %s the plan is %s." % (
            m(g["proposed"]), m(g["current"]), m(g["p10"]), m(g["p90"]), NUMBER[len(lose)].capitalize(),
            NUMBER[len(F["segments"])], joined(label(s) for s in lose), "them" if len(lose) > 1 else "it", m(g["adopt"])))
    doc.add_paragraph(
        "Each schedule is priced on the desk's own requests since January 2023, each request kept as it was except for "
        "the desk's half-spread. Whether a request would have been won at another quote comes from the level the trade "
        "went at: the cover the platform showed on the requests we won, and the winning dealer's print on the public tape "
        "on the requests we lost. What a trade costs after it is done is read on Ashcote's evaluations once they have "
        "caught up, which for thinner bonds is not until the month-end review; the desk's next-day view puts the "
        "schedule in force at %s." % m(F["routes"]["the desk's next-day view"]["current"]))
    ex = F["note_examples"]
    usd = lambda v: "USD {:,.0f}".format(v or 0)
    tail = "".join("; in %s it is %s against %s" % (label(s), usd(g["won_cost"][s]), usd(g["add_cost"][s])) for s in ex[1:])
    doc.add_paragraph(
        "The trades a tighter quote adds are not like the trades we win on today's schedule. Where rivals who read hedge "
        "fund flow price a request tight it was usually benign, so a tighter quote picks up cheaper trades; where Ashcote's "
        "marks are stale, a tighter quote draws the requests that pick it off. In %s the trades we win on today's schedule "
        "cost %s a million and the added trades %s%s." % (label(ex[0]), usd(g["won_cost"][ex[0]]), usd(g["add_cost"][ex[0]]), tail))
    doc.add_paragraph(
        "Recommendation: approve the draft except for its changes for %s, where today's quotes should stay; the other %s "
        "changes each add P&L once their added trades are costed on their own record." % (
            joined(label(s) for s in lose), NUMBER[len(pays)]))
    p = doc.add_paragraph()
    r = p.add_run("The workbook holds the plan, each changed segment's figures, the bridge between the two schedules, the "
                  "range and what other readings of the record would show.")
    r.font.size = Pt(9)
    r.font.color.rgb = RGBColor(0x52, 0x51, 0x4E)
    doc.core_properties.author = AUTHOR
    doc.save(path)
    PP.normalize_docx(path, AUTHOR, AUTHOR, STAMPS[NOTE][0], STAMPS[NOTE][1], revision=6, total_time=74, seed=P.SEED,
                      title="2027 quoting schedule", company=P.FIRM)


def write_all(F, out):
    os.makedirs(out, exist_ok=True)
    write_workbook(os.path.join(out, BOOK), F)
    write_note(os.path.join(out, NOTE), F)
