"""The golden deliverables: the conversion workbook (the call on its first sheet, with the chart) and the CSV of
every centre's banked marks against Carrow's standard. Every figure comes from figures.json or the centre-level
estimates results.py returns."""
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import core as C

FILES = {"wb": "carrow_banked_marks_conversion_2027.xlsx", "csv": "carrow_banked_marks_by_centre_2025_2026.csv"}
MEMBERS = C.MEMBERS
HEAD = PatternFill("solid", fgColor="D3DEE8")  # a light band: the house writer keeps fills and drops font colours
DOWN, UP, KEEP = PatternFill("solid", fgColor="F6E0C6"), PatternFill("solid", fgColor="D5E7F5"), PatternFill("solid", fgColor="EEF1F3")
THIN = Side(style="thin", color="B8C0C8")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
F1, F2 = "0.0;-0.0;0.0", "0.00;-0.00;0.00"


def _rng(b):
    return "%.1f to %.1f" % (b[0], b[1])


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _hdr(ws, row, n, height=44):
    for c in range(1, n + 1):
        cell = ws.cell(row=row, column=c)
        cell.font, cell.fill, cell.border = Font(bold=True, size=10), HEAD, BOX
        cell.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center" if c > 1 else "left")
    ws.row_dimensions[row].height = height


def _widths(ws, widths):
    for i, w in enumerate(widths):
        ws.column_dimensions[chr(65 + i)].width = w
    ws.page_setup.orientation = "landscape"
    ws.page_setup.paperSize = 9
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0


def _title(ws, text, sub=None, span=8):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=13)
    ws["A1"].alignment = WRAP
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=span)
    ws.row_dimensions[1].height = 36
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(size=10)
        ws["A2"].alignment = WRAP
        ws.merge_cells(start_row=2, start_column=1, end_row=2, end_column=span)
        ws.row_dimensions[2].height = 44


def _note(ws, row, text, span, height=30):
    ws.cell(row=row, column=1, value=text).alignment = WRAP
    ws.cell(row=row, column=1).font = Font(size=9)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    ws.row_dimensions[row].height = height


def _body(ws, r0, r1, n):
    for r in range(r0, r1 + 1):
        for c in range(1, n + 1):
            ws.cell(row=r, column=c).border = BOX


def headline(f):
    down = [b for b in MEMBERS if f["side"][b] == "down"]
    up = [b for b in MEMBERS if f["side"][b] == "up"]
    keep = [b for b in MEMBERS if f["side"][b] == "as banked"]
    return ("Convert %s banked marks down (%s marks) and %s up (%s marks); carry %s as banked." % (
        _list(b + "'s" for b in down), _list("%.1f" % f["converted"][b] for b in down),
        _list(b + "'s" for b in up), _list("%.1f" % f["converted"][b] for b in up), _list(b + "'s" for b in keep)))


def first_sheet(wb, f):
    ws = wb.active
    ws.title = "Conversion"
    h = f["hurried"]["distance"]
    wrong = [b for b in MEMBERS if (abs(h[b]) >= f["line"]) != (f["side"][b] != "as banked") or (h[b] > 0) != (f["distance_2dp"][b] > 0)]
    _title(ws, headline(f),
           "Banked workshop portfolio marks of the 2025 and 2026 series against Carrow's standard (Protocol on Banked "
           "Marks, 4.1 and 4.2). The boards' moderation records read as they stand would convert every board except "
           "Ardkeel down; that reading is wrong for %s (sheet Routes)." % _list(wrong), span=9)
    head = ["Board", "Candidates with a banked mark", "Distance from Carrow's standard, 2025 and 2026 together (marks)",
            "Range across conventions", "2025 series", "2026 series", "Protocol 4.2", "Conversion (marks)",
            "Moderation record as it stands (marks)", "Upper tolerance", "Lower tolerance"]
    for c, t in enumerate(head, 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 9, 58)
    for i, b in enumerate(MEMBERS):
        r = 5 + i
        side = f["side"][b]
        conv = 0.0 if side == "as banked" else -f["distance"][b]
        row = [b, sum(f["banked_candidates"][b].values()), f["distance"][b], _rng(f["distance_band"][b]),
               f["by_series"]["2025"][b], f["by_series"]["2026"][b],
               {"down": "Convert down", "up": "Convert up", "as banked": "Carry as banked"}[side], conv, h[b], f["line"], -f["line"]]
        for c, v in enumerate(row, 1):
            ws.cell(row=r, column=c, value=v)
        for c in (3, 5, 6, 8, 10, 11):
            ws.cell(row=r, column=c).number_format = F1
        ws.cell(row=r, column=9).number_format = F2
        ws.cell(row=r, column=2).number_format = "#,##0"
        for c in range(1, 10):
            ws.cell(row=r, column=c).fill = {"down": DOWN, "up": UP, "as banked": KEEP}[side]
        ws.cell(row=r, column=3).font = Font(bold=True)
        ws.cell(row=r, column=4).alignment = Alignment(horizontal="center")
    r = 5 + len(MEMBERS)
    row = ["Joining boards as a whole", f["banked_total"], f["whole"], _rng(f["whole_band"]), None, None, None, None,
           f["hurried"]["whole"]]
    for c, v in enumerate(row, 1):
        ws.cell(row=r, column=c, value=v)
    ws.cell(row=r, column=1).font = ws.cell(row=r, column=3).font = Font(bold=True)
    ws.cell(row=r, column=2).number_format = "#,##0"
    ws.cell(row=r, column=3).number_format = F1
    ws.cell(row=r, column=4).alignment = Alignment(horizontal="center")
    ws.cell(row=r, column=9).number_format = F2
    _body(ws, 5, r, 9)
    for c in (10, 11):
        ws.cell(row=4, column=c).font = Font(size=8)
        for rr in range(5, 5 + len(MEMBERS)):
            ws.cell(row=rr, column=c).font = Font(size=8)
    _note(ws, r + 2, "A positive distance means the banked marks stand above Carrow's standard. The range is the lowest and "
          "highest figure across %d sets of estimating conventions, with a quarter of its width added at each end; "
          "every set gives the same six outcomes (sheet Sensitivity). Distances by centre are in %s." % (
              f["variants"], FILES["csv"]), 9, 42)
    _widths(ws, [27, 13, 21, 15, 10, 10, 16, 12, 17, 9, 9])
    ws.freeze_panes = "B5"
    bar = BarChart()
    bar.type, bar.style = "col", 10
    bar.title = "Ardkeel and Dunmoyle stand 2 marks or more above Carrow's standard, Gortavale 2 or more below"
    bar.add_data(Reference(ws, min_col=3, min_row=4, max_row=4 + len(MEMBERS)), titles_from_data=True)
    bar.add_data(Reference(ws, min_col=9, min_row=4, max_row=4 + len(MEMBERS)), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + len(MEMBERS)))
    bar.y_axis.title = "Marks above (+) or below (-) Carrow's standard"
    bar.y_axis.number_format = "0"
    bar.y_axis.majorGridlines = None
    bar.x_axis.tickLblPos = "low"
    bar.x_axis.delete = bar.y_axis.delete = False
    bar.series[0].graphicalProperties.solidFill = "1F6FA8"
    bar.series[1].graphicalProperties.solidFill = "C9CED3"
    for s in bar.series:
        s.graphicalProperties.line.noFill = True
        s.invertIfNegative = False
    bar.gapWidth = 60
    line = LineChart()
    line.add_data(Reference(ws, min_col=10, max_col=11, min_row=4, max_row=4 + len(MEMBERS)), titles_from_data=True)
    for s in line.series:
        s.graphicalProperties.line.solidFill = "B5471B"
        s.graphicalProperties.line.width = 15875
        s.graphicalProperties.line.dashStyle = "dash"
        s.marker.symbol = "none"
        s.smooth = False
    bar += line
    bar.legend.position = "b"
    bar.height, bar.width = 9.6, 23.5
    ws.add_chart(bar, "A%d" % (r + 5))
    ws.print_area = "A1:I%d" % (r + 26)
    return ws


def share_sheet(wb, f):
    ws = wb.create_sheet("Share recorded")
    _title(ws, "Moderators record %.1f to %.1f per cent of a marking difference, least at %s" % (
        min(f["share_pct"][b] for b in MEMBERS), max(f["share_pct"][b] for b in MEMBERS),
        min(MEMBERS, key=lambda b: f["share_pct"][b])),
           "Each standardisation script is a portfolio sampled the series before. Its centre mark less the team's "
           "consensus mark before the meeting is the difference found without the centre's marks; the centre mark less "
           "the moderator's mark on the sample record is what the same portfolio's moderation recorded. The share is the "
           "slope of the second on the first.", span=6)
    head = ["Board", "Scripts, 2015 to 2026 meetings", "Moderators marking a script (mean)", "Share of the difference recorded (per cent)",
            "Mean recorded difference, 2021 to 2026 samples (marks)", "Sampled centres adjusted, 2021 to 2026 (per cent)"]
    for c, t in enumerate(head, 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 6, 58)
    for i, b in enumerate(C.BOARDS):
        row = [b, f["trial_scripts"][b], f["trial_markers"][b], f["share_pct"][b], f["recorded_mean"][b], f["adjusted_pct"][b]]
        for c, v in enumerate(row, 1):
            ws.cell(row=5 + i, column=c, value=v)
        ws.cell(row=5 + i, column=4).number_format = "0.0"
        ws.cell(row=5 + i, column=5).number_format = F2
    _body(ws, 5, 4 + len(C.BOARDS), 6)
    _note(ws, 6 + len(C.BOARDS), "%s's share is stated with the range %s per cent across the conventions on sheet Sensitivity. "
          "Carrow is shown for comparison; its marks are not converted." % (C.PULL_BOARD, _rng(f["c1_band"])), 6)
    _widths(ws, [16, 16, 17, 20, 22, 20])
    ws.freeze_panes = "B5"


def cycle_sheet(wb, f):
    ws = wb.create_sheet("Years after a sample")
    _title(ws, "Centres mark lower in the years after a sample: %s's by %.1f marks in the first year" % (
        C.CYCLE_BOARD, abs(f["c2"])),
           "Mean centre mark by years since the centre's last sample, each centre against itself and net of the board's "
           "year, from the mark sheets of the last nine series. A centre not sampled in a series is placed at its last "
           "sample, scaled up by the share recorded, plus the level for the years since.", span=5)
    head = ["Board", "Rota (years)", "One year after a sample (marks)", "Two years after a sample (marks)", "Centres"]
    for c, t in enumerate(head, 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 5, 46)
    for i, b in enumerate(C.BOARDS):
        cy = f["cycle"][b]
        row = [b, f["rota_years"][b], cy[0] if cy else None, cy[1] if len(cy) > 1 else None, f["centres"][b]]
        for c, v in enumerate(row, 1):
            ws.cell(row=5 + i, column=c, value=v)
        for c in (3, 4):
            ws.cell(row=5 + i, column=c).number_format = F2
    _body(ws, 5, 4 + len(C.BOARDS), 5)
    _note(ws, 6 + len(C.BOARDS), "%s's first-year level is stated with the range %s marks. Carrow samples every centre every "
          "year, so it has no years between samples." % (C.CYCLE_BOARD, _rng(f["c2_band"])), 5)
    _widths(ws, [16, 12, 20, 20, 11])
    ws.freeze_panes = "B5"


def standards_sheet(wb, f):
    ws = wb.create_sheet("Standards")
    _title(ws, "%s's moderators mark %.1f marks below Carrow's standard; the other boards between %.1f below and %.1f above" % (
        C.LINK_BOARD, abs(f["c3"]), abs(min(f["standard"][b] for b in MEMBERS if b != C.LINK_BOARD)),
        max(f["standard"][b] for b in MEMBERS)),
           "Moderators registered with two boards mark both boards' standardisation scripts. Each person's marks less "
           "each team's consensus, taken as a difference between the two meetings of one series, link the two teams; "
           "each board's agreed marks place its standard against its own consensus; the ten links are fitted together "
           "with Carrow at zero.", span=6)
    head = ["Board", "Second board", "Person-series, 2020 to 2026", "Second board's consensus less the board's (marks)"]
    for c, t in enumerate(head, 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 4, 46)
    for i, l in enumerate(f["links"]):
        for c, v in enumerate([l["a"], l["b"], l["person_years"], l["difference"]], 1):
            ws.cell(row=5 + i, column=c, value=v)
        ws.cell(row=5 + i, column=4).number_format = F2
    last = 4 + len(f["links"])
    _body(ws, 5, last, 4)
    r0 = last + 3
    for c, t in enumerate(["Board", "Consensus less agreed mark (marks)", "Standard against Carrow's (marks)"], 1):
        ws.cell(row=r0, column=c, value=t)
    _hdr(ws, r0, 3, 46)
    for i, b in enumerate(C.BOARDS):
        for c, v in enumerate([b, f["agreed_gap"][b], f["standard"][b]], 1):
            ws.cell(row=r0 + 1 + i, column=c, value=v)
        for c in (2, 3):
            ws.cell(row=r0 + 1 + i, column=c).number_format = F2
    _body(ws, r0 + 1, r0 + len(C.BOARDS), 3)
    _note(ws, r0 + len(C.BOARDS) + 2, "A negative standard means the board's moderators give a portfolio fewer marks than "
          "Carrow's. %s's is stated with the range %s marks." % (C.LINK_BOARD, _rng(f["c3_band"])), 6)
    _widths(ws, [16, 22, 20, 26, 12, 12])
    ws.freeze_panes = "A5"


def check_sheet(wb, f):
    ws = wb.create_sheet("2023 review")
    rf = f["referee"]
    _title(ws, "The estimate reproduces the regulator's 2023 review of %s to %.2f marks; no shortcut comes within %.1f" % (
        rf["board"], rf["off"], min(v["off"] for v in rf["rivals"].values())),
           "The Office's review marked eight portfolios from every %s centre at Carrow's standard in the 2023 series. "
           "It is read here on the %d centres the board did not sample that series, which the moderation record does not "
           "see, and each route is run for 2023 on the same centres." % (rf["board"], rf["unsampled_centres"]), span=4)
    for c, t in enumerate(["Route", "Marks above Carrow's standard", "Away from the review (marks)"], 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 3, 40)
    names = {"S1 lost": "The recorded difference taken as the difference", "S2 lost": "The last sample carried to the "
             "years not sampled", "S3 lost": "The board's own principal taken as the standard",
             "rigorous": "The board's own meeting severity added to the record"}
    rows = [("The review, centres not sampled in 2023", rf["review"], None), ("This estimate", rf["golden"], rf["off"])]
    rows += [(names[k], v["value"], v["off"]) for k, v in rf["rivals"].items()]
    for i, row in enumerate(rows):
        for c, v in enumerate(row, 1):
            ws.cell(row=5 + i, column=c, value=v)
        for c in (2, 3):
            ws.cell(row=5 + i, column=c).number_format = F2
    ws.cell(row=6, column=1).font = Font(bold=True)
    _body(ws, 5, 4 + len(rows), 3)
    _note(ws, 6 + len(rows), "The review covers one board and one series before the banked ones, so it checks the method and "
          "is not %s's answer: read on every centre it gives %.2f marks for the 2023 series." % (rf["board"], rf["raw_all_centres"]), 4)
    _widths(ws, [78, 20, 20, 10])


def sensitivity_sheet(wb, f):
    ws = wb.create_sheet("Sensitivity")
    nv, bs = f["nearest_any"], f["beside"]
    _title(ws, "All %d sets of conventions give the same six outcomes; the nearest any of them comes to the tolerance is %.2f marks (%s)" % (
        f["all_rebuilds"], nv["distance"], nv["board"]),
           "Upper part: each fitted input moved up and down by the furthest any convention moves it, alone and all "
           "three together. Lower part: the lowest and highest distance across the %d crossed conventions and "
           "across the %d run beside them." % (f["variants"], bs["rebuilds"]), span=8)
    head = ["Input moved"] + list(MEMBERS) + ["Outcomes"]
    for c, t in enumerate(head, 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 8, 30)
    for i, p in enumerate(f["perturbations"]):
        ws.cell(row=5 + i, column=1, value=p["input"][0].upper() + p["input"][1:])
        for j, b in enumerate(MEMBERS):
            ws.cell(row=5 + i, column=2 + j, value=p["distance"][b]).number_format = F2
        ws.cell(row=5 + i, column=8, value="Unchanged" if p["call_holds"] else "Changed")
    last = 4 + len(f["perturbations"])
    _body(ws, 5, last, 8)
    r0 = last + 3
    for c, t in enumerate(["Across the conventions"] + list(MEMBERS), 1):
        ws.cell(row=r0, column=c, value=t)
    _hdr(ws, r0, 7, 30)
    for i, (lab, k) in enumerate((("Lowest", 0), ("Highest", 1))):
        ws.cell(row=r0 + 1 + i, column=1, value=lab)
        for j, b in enumerate(MEMBERS):
            ws.cell(row=r0 + 1 + i, column=2 + j, value=f["variant_range"][b][k]).number_format = F2
    for i, (lab, k) in enumerate((("Lowest, recent meetings or all fifteen series", 0),
                                  ("Highest, recent meetings or all fifteen series", 1))):
        ws.cell(row=r0 + 3 + i, column=1, value=lab)
        for j, b in enumerate(MEMBERS):
            ws.cell(row=r0 + 3 + i, column=2 + j, value=bs["range"][b][k]).number_format = F2
    ws.cell(row=r0 + 5, column=1, value="One spread of the share recorded (per cent of itself)")
    ws.cell(row=r0 + 6, column=1, value="One spread of a level after a sample (marks)")
    ws.cell(row=r0 + 7, column=1, value="One spread of the standard (marks)")
    for j, b in enumerate(MEMBERS):
        ws.cell(row=r0 + 5, column=2 + j, value=f["spreads"][b]["share_pct"]).number_format = "0.0"
        ws.cell(row=r0 + 6, column=2 + j, value=f["spreads"][b]["cycle"]).number_format = F2
        ws.cell(row=r0 + 7, column=2 + j, value=f["spreads"][b]["standard"]).number_format = F2
    _body(ws, r0 + 1, r0 + 7, 7)
    _note(ws, r0 + 9, "The conventions: the share fitted with or without an intercept, on the consensus or the agreed marks, "
          "as a ratio of means on the agreed marks, on the last six meetings, year by year, with the consensus' own error allowed for; "
          "levels after a sample on six, nine or twelve series, weighted by candidates or not, or each centre's own "
          "change in mean mark; the last sample or the last two; links weighted by people or not, trimmed, at the "
          "median, on the 2023 to 2026 meetings, one link a board, with or without a marker's own mark in the "
          "consensus; agreed marks at the mean or the median, on all meetings or those the links cover; and every pair "
          "of these that changes two different choices. Beside them: the share fitted on the last five or four "
          "meetings with every form of the links and of the levels; the share as a ratio of means on the agreed "
          "marks on the last six to three meetings; the levels on all fifteen series, alone and with each other "
          "choice. The ranges on the first sheet hold every one.", 8, 96)
    _widths(ws, [46, 11, 11, 11, 11, 11, 11, 12])
    ws.freeze_panes = "B5"


def routes_sheet(wb, f):
    ws = wb.create_sheet("Routes")
    _title(ws, "What each shortcut would file: none gives the six outcomes of the estimate",
           "Marks above Carrow's standard, 2025 and 2026 series together. An outcome that differs from the estimate's is "
           "shaded.", span=8)
    for c, t in enumerate(["Route"] + list(MEMBERS) + ["Joining boards as a whole"], 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 8, 36)
    rows = [("This estimate", f["distance_2dp"], f["whole_2dp"])]
    order = ["S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3", "direct", "rigorous"]
    rows += [(f["routes"][k]["name"][0].upper() + f["routes"][k]["name"][1:], f["routes"][k]["distance"], f["routes"][k]["whole"])
             for k in order]

    def side(v):
        return 1 if v >= f["line"] else (-1 if v <= -f["line"] else 0)
    for i, (name, d, whole) in enumerate(rows):
        ws.cell(row=5 + i, column=1, value=name).alignment = WRAP
        for j, b in enumerate(MEMBERS):
            cell = ws.cell(row=5 + i, column=2 + j, value=d[b])
            cell.number_format = F2
            if side(d[b]) != side(f["distance_2dp"][b]):
                cell.fill = DOWN
        ws.cell(row=5 + i, column=8, value=whole).number_format = F2
        ws.row_dimensions[5 + i].height = 30
    ws.cell(row=5, column=1).font = Font(bold=True)
    _body(ws, 5, 4 + len(rows), 8)
    _widths(ws, [58, 11, 11, 11, 11, 11, 11, 14])
    ws.freeze_panes = "B5"


def notes_sheet(wb, f):
    ws = wb.create_sheet("Notes")
    ws["A1"] = "Definitions and conventions"
    ws["A1"].font = Font(bold=True, size=12)
    lines = [
        ("Banked mark", "A workshop portfolio mark awarded by a joining board in the 2025 or 2026 series, as awarded after "
                        "moderation (Protocol 2.1). Withdrawn and absent entries carry no mark (2.3)."),
        ("Carrow's standard", "The agreed marks of Carrow's principal moderator as applied in its 2026 moderation (Protocol 3.1)."),
        ("Distance", "The mean over candidates of the banked mark less the mark the portfolio merits at Carrow's standard, "
                     "in marks (4.1). Converted at 2.0 marks or more either way, by the distance (4.2)."),
        ("Joining boards as a whole", "The same mean over every candidate with a banked mark at any joining board (5.1)."),
        ("Records", "As supplied by the boards between 25 January and 5 February 2027. Centres are keyed by national roll "
                    "number; a reissued moderation record replaces the earlier one (Code 4.5); %d mark sheet rows %s's "
                    "system loaded twice are counted once." % (sum(f["repeat_rows"].values()), _list(f["repeat_rows"]))),
        ("Sample difference", "Centre's mark less moderator's mark, the mean over the sampled portfolios (Code 4.1). An "
                              "adjustment applied in the series is taken off the centre's level, since the banked mark "
                              "is the mark after it."),
        ("Not used", "Enquiries about results, centre approval visits and entries by trade and age band carry nothing on "
                     "marking standards."),
        ("Precision", "Distances to 0.1 mark, each with its range across conventions."),
    ]
    for i, (k, v) in enumerate(lines):
        ws.cell(row=3 + i, column=1, value=k).font = Font(bold=True)
        ws.cell(row=3 + i, column=2, value=v).alignment = WRAP
        ws.row_dimensions[3 + i].height = 46
    _widths(ws, [26, 110])


def write_csv(path, centre, rolls):
    lines = ["board,roll_no,series,candidates_with_banked_mark,sampled_in_series,distance_from_carrow_standard_marks"]
    for b in MEMBERS:
        for i, roll in enumerate(rolls[b]):
            for y in C.BANKED:
                c = centre[b, y]
                lines.append("%s,%d,%d,%d,%s,%.2f" % (b, roll, y, c["n"][i], "Y" if c["sampled"][i] else "N", c["est"][i] + 0.0))
    with open(path, "w", newline="") as fh:
        fh.write("\r\n".join(lines) + "\r\n")
    return len(lines) - 1


def build(folder, f, centre, rolls):
    os.makedirs(folder, exist_ok=True)
    wb = Workbook()
    first_sheet(wb, f)
    share_sheet(wb, f)
    cycle_sheet(wb, f)
    standards_sheet(wb, f)
    check_sheet(wb, f)
    sensitivity_sheet(wb, f)
    routes_sheet(wb, f)
    notes_sheet(wb, f)
    wb.save(os.path.join(folder, FILES["wb"]))
    return write_csv(os.path.join(folder, FILES["csv"]), centre, rolls)
