"""The two files the prompt asks for, as the subscription analyst hands them to the head of controlling: the 2027
lines workbook (every line's expected 36-month net revenue per start against its planned cost, the lines funded, the
figures behind them, and what the same arithmetic gives on each shortcut) and a one-page note."""
import datetime as dt
import os
import sys

from openpyxl import Workbook
from openpyxl.styles import Alignment, Font, PatternFill
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import Paragraph, Spacer, Table, TableStyle

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import officepdf as O  # noqa: E402
import postprocess  # noqa: E402

import golden as GD  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402

XLSX = "acquisition_lines_2027.xlsx"
PDF = "acquisition_note_2027.pdf"
CET = dt.timezone(dt.timedelta(hours=1))
SHOW = {"careful": "Every shortcut below together",
        "completion on each channel's older starts": "Newest starts completed on each channel's older starts",
        "no full-price term at the intro's end": "End-of-intro exits without the full price they step up to",
        "returns on the customer number only": "Later subscriptions counted on the same customer number only",
        "the 2025 rise read from April, pooled": "The April 2025 rise read from April on, all tenures together"}


def eur(x, d=0):
    s = f"{x:,.{d}f}"
    return s


def pct(x, d=1):
    return ("%." + str(d) + "f%%") % (100 * x)


def workbook(path, G):
    g = G["golden"]
    plan, spend, cps = G["plan"], G["spend"], G["cps"]
    wb = Workbook()
    ws = wb.active
    ws.title = "Lines 2027"
    ws.append(["2027 digital acquisition lines: expected 36-month net revenue per start against planned cost"])
    ws["A1"].font = Font(bold=True, size=12)
    ws.append(["Controlling · per the digital subscription KPI standard v3 (4.1: funded at 3.5 times the planned cost "
               "per start) · records to 31 October 2026"])
    ws.append([])
    head = ["Line", "Channel", "Title", "Offer 2027", "Planned starts", "Planned spend (EUR)",
            "Planned cost per start (EUR)", "Expected 36-month net revenue per start (EUR)", "Multiple of cost",
            "Funded"]
    ws.append(head)
    for c in ws[4]:
        c.font = Font(bold=True)
        c.fill = PatternFill("solid", fgColor="DDE3EA")
        c.alignment = Alignment(wrap_text=True, vertical="top")
    order = sorted(plan, key=lambda l: -g["R7"][l] / cps[l])
    for line in order:
        v = g["R7"][line]
        ws.append([GD.key(line), P.CH_NAME[line[0]], P.TITLE_NAME[line[1]], plan[line]["offer"],
                   sum(plan[line]["starts"]), spend[line], round(cps[line], 2), int(round(v)),
                   round(v / cps[line], 2), "yes" if line in g["R8"] else "no"])
    last = 4 + len(order)
    for r in range(5, last + 1):
        ws.cell(r, 5).number_format = "#,##0"
        ws.cell(r, 6).number_format = "#,##0"
        ws.cell(r, 7).number_format = "#,##0.00"
        ws.cell(r, 8).number_format = "#,##0"
        ws.cell(r, 9).number_format = "0.00"
    ws.append([])
    ws.append(["Budget for the funded lines (EUR)", None, None, None, None, '=SUMIF(J5:J%d,"yes",F5:F%d)' % (last, last)])
    ws.cell(last + 2, 6).number_format = "#,##0"
    ws.cell(last + 2, 1).font = Font(bold=True)
    ws.append(["Plan total (EUR)", None, None, None, None, "=SUM(F5:F%d)" % last])
    ws.cell(last + 3, 6).number_format = "#,##0"
    ws.freeze_panes = "B5"
    widths = [10, 20, 25, 10, 10, 13, 13, 16, 10, 8]
    for i, w in enumerate(widths):
        ws.column_dimensions["ABCDEFGHIJ"[i]].width = w
    w2 = wb.create_sheet("Figures")
    w2.append(["Paying digital subscribers at 31 October 2026"])
    w2["A1"].font = Font(bold=True)
    for t in P.TITLES:
        w2.append([P.TITLE_NAME[t], g["R1"][t]])
    w2.append(["All titles", sum(g["R1"].values())])
    w2.append([])
    w2.append(["The plan's 2027 starts still paying on 31 December 2027, every line run as planned", "Paying",
               "Planned starts"])
    w2.cell(w2.max_row, 1).font = Font(bold=True)
    for c in P.PAID:
        w2.append([P.CH_NAME[c], int(round(g["R9"][c])), G["n_plan_starts"][c]])
    w2.append([])
    w2.append(["Extra cancellations the April 2027 list prices bring by 31 December 2027, subscribers paying at "
               "31 October 2026"])
    w2.cell(w2.max_row, 1).font = Font(bold=True)
    for t in P.TITLES:
        w2.append([P.TITLE_NAME[t], int(round(g["R6"][t]))])
    w2.append([])
    w2.append(["2027 offer", "Share leaving when the introductory price ends, at 2026 list prices",
               "Points added by the April 2027 list prices"])
    for c in w2[w2.max_row]:
        c.font = Font(bold=True)
    for code in g["R3"]:
        w2.append([code, round(100 * g["R3"][code], 1), round(100 * g["R4"][code], 1)])
    w2.append([])
    w2.append(["Channel", "Starts November 2025 to April 2026 still paying three years after starting (per cent)",
               "Starts July to September 2023: net revenue per start over 36 months (EUR)"])
    for c in w2[w2.max_row]:
        c.font = Font(bold=True)
    for ch in P.CHANNELS:
        w2.append([P.CH_NAME[ch], round(100 * g["R5"][ch], 1), int(round(g["R2"][ch]))])
    w2.column_dimensions["A"].width = 34
    w2.column_dimensions["B"].width = 22
    w2.column_dimensions["C"].width = 22
    w3 = wb.create_sheet("Checks")
    w3.append(["What the same arithmetic funds when one step is done another way"])
    w3["A1"].font = Font(bold=True)
    w3.append(["Way of working", "Lines funded", "Added against this workbook", "Dropped"])
    for c in w3[2]:
        c.font = Font(bold=True)
    for nm, label in SHOW.items():
        S = G["routes"][nm]["R8"]
        add = [GD.key(l) for l in S if l not in g["R8"]]
        drop = [GD.key(l) for l in g["R8"] if l not in S]
        w3.append([label, len(S), ", ".join(add) or "-", ", ".join(drop) or "-"])
    w3.append([])
    w3.append(["Other reasonable specifications (reading in bands or linear, two months of reading, titles, the offer "
               "or the price stepped up to in the leaving model, a time trend at the end of the intro, the offers by "
               "discount and length, households linked by payment method or by address alone) fund the same eight "
               "lines."])
    own = G["newest_own"]
    w3.append(["Calibrating each line on its own starts of November 2025 to October 2026 instead of their reading "
               "rests on %d to %d full-price cancellations a line so far (%d in all; the leaving model on their "
               "reading expects %d of them)." % (min(o for o, e in own.values()), max(o for o, e in own.values()),
                                                 sum(o for o, e in own.values()),
                                                 int(round(sum(e for o, e in own.values()))))])
    if "boot" in G:
        B = G["boot"]
        w3.append([])
        w3.append(["Start months drawn again within each line (%d draws, every model refitted): %d draws fund the "
                   "same eight lines" % (B["reps"], B["same"])])
        w3.cell(w3.max_row, 1).font = Font(bold=True)
        w3.append(["Line", "Multiple of cost", "5th percentile of the draws", "95th percentile of the draws"])
        for c in w3[w3.max_row]:
            c.font = Font(bold=True)
        for line in sorted(plan, key=lambda l: -g["R7"][l] / cps[l]):
            w3.append([GD.key(line), round(g["R7"][line] / cps[line], 2), round(B["lo"][line], 2),
                       round(B["hi"][line], 2)])
            for col in (2, 3, 4):
                w3.cell(w3.max_row, col).number_format = "0.00"
    w3.column_dimensions["A"].width = 58
    w3.column_dimensions["C"].width = 44
    w3.column_dimensions["D"].width = 22
    w4 = wb.create_sheet("Notes")
    for line in [
            "As of: records to 31 October 2026 (subscription system and analytics exports of 2 to 4 November 2026).",
            "Definitions as in the digital subscription KPI standard, version 3 (20 January 2026): a start is a "
            "subscription not withdrawn within 14 days; net revenue is net of VAT at 7 per cent, store fees and "
            "refunds; a household's later subscriptions to the same title count towards its start.",
            "2027 starts: each line's starts of November 2025 to October 2026 (their first months' reading and "
            "payment routes), at the plan's offer and monthly numbers, at the April 2027 list prices and no "
            "later change.",
            "Excluded from every count: staff access, gift subscriptions, company licences and test accounts.",
            "Euro figures per start are rounded to whole euros; costs per start to the cent; multiples to two "
            "decimals; shares to one decimal."]:
        w4.append([line])
    w4.column_dimensions["A"].width = 120
    wb.save(path)
    postprocess.normalize_ooxml(path, "Tamara Naser", "Tamara Naser", "2026-11-05T08:02:00Z", "2026-11-06T15:24:00Z",
                                excel=True, company="Medienhaus Brückenhafen GmbH")


def note(path, G):
    g = G["golden"]
    plan, spend, cps = G["plan"], G["spend"], G["cps"]
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Helvetica", fontSize=9.4, leading=12.8, spaceAfter=5)
    h1 = ParagraphStyle("h", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=12.5, leading=16, spaceAfter=3)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.4, textColor=colors.HexColor("#444444"))
    cell = ParagraphStyle("c", fontName="Helvetica", fontSize=8.2, leading=10)
    funded = sorted(g["R8"], key=lambda l: -g["R7"][l] / cps[l])
    names = ", ".join(GD.key(l) for l in funded)
    unf = sorted([l for l in plan if l not in g["R8"]], key=lambda l: -g["R7"][l] / cps[l])
    rows = [["Line", "Offer", "Cost per start", "36-month value", "Multiple"]]
    for l in funded:
        rows.append([GD.key(l), plan[l]["offer"], "%.2f" % cps[l], eur(g["R7"][l]), "%.2f" % (g["R7"][l] / cps[l])])
    t = Table([[Paragraph(str(c), cell) for c in r] for r in rows], colWidths=[60, 50, 70, 75, 55])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#9AA0AB"))]))
    near = [l for l in unf if g["R7"][l] / cps[l] >= 0.8 * P.HURDLE]
    s = [Paragraph("Controlling · To: Rosa-Maria Herrmann, head of controlling · From: Tamara Naser · 6 November 2026",
                   small),
         Paragraph("Fund eight acquisition lines in 2027, for EUR %s" % eur(g["budget"]), h1),
         Paragraph("Fund eight of the plan's 18 lines, %s, for a budget of EUR %s. Each is expected to bring at least "
                   "3.5 times its planned cost per start in net revenue over 36 months; the other ten are not "
                   "funded." % (names, eur(g["budget"])), body),
         t,
         Paragraph("Source: media plan 2027 v2.1 (cost per start); subscription system and analytics exports to 31 "
                   "October 2026 (value).", small), Spacer(1, 6),
         Paragraph("The lines closest to the bar that miss it, %s, run between %.2f and %.2f times their cost. "
                   "All four paid social lines and the cashback partner lines at the Rundschau and the Kreisblatt "
                   "look fundable on their earlier starts' survival, but the starts since late 2025 read far less in "
                   "their first months than earlier ones and leave correspondingly faster once on the full price "
                   "(paid social: %s of the November 2025 to April 2026 starts still paying three years in)." % (
                       ", ".join(GD.key(l) for l in near), min(g["R7"][l] / cps[l] for l in near),
                       max(g["R7"][l] / cps[l] for l in near), pct(g["R5"]["SOC"])), body),
         Paragraph("The April 2027 list prices add %.1f to %.1f points to the share leaving when an introductory "
                   "price ends, as the April 2025 rise did (at today's prices APP-KBO and SOC-KBO would clear the "
                   "bar); the 2025 rise's own cancellations began with the notice "
                   "letters in February and were heaviest among subscribers in their first year, and on today's base "
                   "the April 2027 rise brings about %s extra cancellations by the end of 2027. A household that "
                   "leaves and comes back often does so under a new customer number: counted by household, the "
                   "July to September 2023 starts brought EUR %s per start (paid social) to EUR %s (direct) over 36 "
                   "months." % (100 * min(g["R4"].values()), 100 * max(g["R4"].values()),
                                eur(sum(g["R6"].values())), eur(g["R2"]["SOC"]), eur(g["R2"]["DIR"])), body),
         Paragraph("Paying digital subscribers at 31 October 2026: %s (Rundschau %s, Anzeiger %s, Kreisblatt %s, "
                   "Nachrichten %s). Run in full, the plan's %s starts in 2027 would leave about %s paying at the "
                   "end of the year." % (
                       eur(sum(g["R1"].values())), eur(g["R1"]["BHR"]), eur(g["R1"]["GAZ"]), eur(g["R1"]["KBO"]),
                       eur(g["R1"]["ELN"]), eur(sum(G["n_plan_starts"].values())),
                       eur(sum(int(round(v)) for v in g["R9"].values()))), body),
         Paragraph("The figures assume each line's 2027 starts are like its starts of the twelve months to October "
                   "2026 at the offer in the plan (standard 3.3). Every line keeps its side of the bar under the "
                   "other reasonable specifications in the workbook's Checks sheet%s." % (
                       (", and %d of %d redraws of the start months fund the same eight lines" % (
                           G["boot"]["same"], G["boot"]["reps"])) if "boot" in G else ""), small),
         Paragraph("Starts are counted after the 14-day withdrawal period (standard 2.3); telemarketing's "
                   "withdrawals run well above the other channels'.", small)]
    O.build(path, s, "Fund eight acquisition lines in 2027", "Tamara Naser", "Controlling note",
            "Medienhaus Brückenhafen · Controlling", dt.datetime(2026, 11, 6, 15, 31, tzinfo=CET),
            dt.datetime(2026, 11, 6, 15, 58, tzinfo=CET))


def write(gold_dir, G):
    os.makedirs(gold_dir, exist_ok=True)
    for f in os.listdir(gold_dir):
        os.remove(os.path.join(gold_dir, f))
    workbook(os.path.join(gold_dir, XLSX), G)
    note(os.path.join(gold_dir, PDF), G)
    postprocess.own_mtimes(gold_dir, {})
