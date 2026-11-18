"""The golden deliverables: the tier one workbook (the list on its first sheet, with the chart) and the CSV of each
feature group's cost in each month of the quarter. Every figure comes from figures.json."""
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import core as C
import world as WL

FILES = {"wb": "tessel_tier_one_hardening_2027.xlsx", "csv": "tessel_feature_group_losses_2026q3.csv"}
G = C.GROUPS
MONTHS = [n for n, _, _ in C.Q3_MONTHS]
MONTH_KEY = {"July": "2026-07", "August": "2026-08", "September": "2026-09"}
HEAD = PatternFill("solid", fgColor="D3DEE8")   # a light band: the house writer keeps fills and drops font colours
ON, OFF, MISS = PatternFill("solid", fgColor="D5E7F5"), PatternFill("solid", fgColor="EEF1F3"), PatternFill("solid", fgColor="F6E0C6")
THIN = Side(style="thin", color="B8C0C8")
BOX = Border(top=THIN, bottom=THIN, left=THIN, right=THIN)
WRAP = Alignment(wrap_text=True, vertical="top")
F3, F2, F4 = "0.000", "0.00", "0.0000"
ORDER = ["S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3", "direct", "rigorous"]


def _rng(b, nd=3):
    return "%.*f to %.*f" % (nd, b[0], nd, b[1])


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _name(j):
    return WL.GROUP_NAME[j]


def _cap(s):
    return s[0].upper() + s[1:]


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


def _title(ws, text, sub=None, span=8, sub_height=44):
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
        ws.row_dimensions[2].height = sub_height


def _note(ws, row, text, span, height=30):
    ws.cell(row=row, column=1, value=text).alignment = WRAP
    ws.cell(row=row, column=1).font = Font(size=9)
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    ws.row_dimensions[row].height = height


def _body(ws, r0, r1, n):
    for r in range(r0, r1 + 1):
        for c in range(1, n + 1):
            ws.cell(row=r, column=c).border = BOX


def _middle(ws, r0, r1, n):
    """Rows whose label wraps: every cell centred on the row's height, its other alignment kept."""
    for r in range(r0, r1 + 1):
        for c in range(1, n + 1):
            a = ws.cell(row=r, column=c).alignment
            ws.cell(row=r, column=c).alignment = Alignment(horizontal=a.horizontal, wrap_text=a.wrap_text, vertical="center")


def ranked(f):
    return sorted(G, key=lambda j: -f["cost"][j])


def headline(f):
    on = [j for j in ranked(f) if j in f["list"]]
    off = [j for j in ranked(f) if j not in f["list"]]
    return "Tier one for 2027: %s. %s keep their present tier." % (_list(_name(j) for j in on), _cap(_list(_name(j) for j in off)))


def first_sheet(wb, f):
    ws = wb.active
    ws.title = "Tier one list"
    h = f["hurried"]
    wrong = [j for j in ranked(f) if (j in h["list"]) != (j in f["list"])]
    _title(ws, headline(f),
           "Each feature group's cost of degraded service over the third quarter of 2026, in points of search conversion "
           "(Reliability Charter 2027, sections 3 and 4: 0.05 points or more goes on the list). The ablation tests as "
           "reported, applied to the status record's unhealthy share, would list %s and leave %s off; that reading is "
           "wrong for %s (sheet Routes)." % (
               _list(_name(j) for j in ranked(f) if j in h["list"]),
               _list(_name(j) for j in ranked(f) if j in f["list"] and j not in h["list"]),
               _list(_name(j) for j in wrong)), span=8, sub_height=58)
    head = ["Feature group", "Owning team", "Cost, third quarter 2026 (points of search conversion)", "Range across conventions",
            "Tier for 2027", "Distance from the 0.05 line (points)", "Ablation tests on the status record (points)",
            "That reading's tier", "Tier one line"]
    for c, t in enumerate(head, 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 8, 58)
    rows = ranked(f)
    for i, j in enumerate(rows):
        r = 5 + i
        on = j in f["list"]
        row = [_name(j), WL.TEAMS[j], f["cost"][j], _rng(f["cost_band"][j]), "Tier one" if on else "Present tier",
               f["margin"][j], h["cost"][j], "Tier one" if j in h["list"] else "Present tier", f["line"]]
        for c, v in enumerate(row, 1):
            ws.cell(row=r, column=c, value=v)
        for c in (3, 6, 7):
            ws.cell(row=r, column=c).number_format = F3
        ws.cell(row=r, column=9).number_format = F2
        for c in range(1, 9):
            ws.cell(row=r, column=c).fill = ON if on else OFF
        if (j in h["list"]) != on:
            ws.cell(row=r, column=7).fill = ws.cell(row=r, column=8).fill = MISS
        ws.cell(row=r, column=3).font = Font(bold=True)
        for c in (4, 5, 8):
            ws.cell(row=r, column=c).alignment = Alignment(horizontal="center")
    r = 5 + len(rows)
    for k, (label, v, band, hv) in enumerate((("All feature groups together", f["all"], f["all_band"], h["all"]),
                                              ("Tier one groups together", f["listed_cost"], f["listed_band"], h["listed_cost"]))):
        row = [label, None, v, _rng(band, 2), None, None, hv]
        for c, x in enumerate(row, 1):
            ws.cell(row=r + k, column=c, value=x)
        ws.cell(row=r + k, column=1).font = ws.cell(row=r + k, column=3).font = Font(bold=True)
        ws.cell(row=r + k, column=3).number_format = ws.cell(row=r + k, column=7).number_format = F2
        ws.cell(row=r + k, column=4).alignment = Alignment(horizontal="center")
    _body(ws, 5, r + 1, 8)
    ws.cell(row=4, column=9).font = Font(size=8)
    for rr in range(5, 5 + len(rows)):
        ws.cell(row=rr, column=9).font = Font(size=8)
    r2 = r + 3
    for c, t in enumerate(["All feature groups together, by month"] + MONTHS, 1):
        ws.cell(row=r2, column=c, value=t)
    _hdr(ws, r2, 4, 30)
    ws.cell(row=r2 + 1, column=1, value="Cost over the month's search sessions (points)")
    ws.cell(row=r2 + 2, column=1, value="Range across conventions")
    for c, n in enumerate(MONTHS, 2):
        ws.cell(row=r2 + 1, column=c, value=f["month"][n]).number_format = F2
        ws.cell(row=r2 + 1, column=c).font = Font(bold=True)
        ws.cell(row=r2 + 1, column=c).alignment = Alignment(horizontal="center")
        ws.cell(row=r2 + 2, column=c, value=_rng(f["month_band"][n], 2)).alignment = Alignment(horizontal="center")
    _body(ws, r2 + 1, r2 + 2, 4)
    _note(ws, r2 + 4, "Search conversion fell from %.2f per cent in the second quarter to %.2f in the third. A cost is the "
          "conversion the quarter's sessions would have had with the group in normal service to every service that reads "
          "it, less the conversion as served. The range is the lowest and highest figure across %d sets of estimating "
          "conventions and the readings beside them, with a quarter of its width added at each end; every one gives the "
          "same list (sheet Sensitivity). Costs by group and month are on the next sheet and in %s." % (
              f["conversion"]["q2"], f["conversion"]["q3"], f["variants"], FILES["csv"]), 8, 56)
    _widths(ws, [30, 21, 20, 18, 13, 15, 18, 13, 8])
    ws.freeze_panes = "B5"
    bar = BarChart()
    bar.type, bar.style = "col", 10
    on = [j for j in rows if j in f["list"]]
    bar.title = "%s each cost 0.05 points or more; %s did not" % (_cap(_list(_name(j) for j in on)),
                                                                  _list(_name(j) for j in rows if j not in f["list"]))
    bar.add_data(Reference(ws, min_col=3, min_row=4, max_row=4 + len(rows)), titles_from_data=True)
    bar.add_data(Reference(ws, min_col=7, min_row=4, max_row=4 + len(rows)), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=5, max_row=4 + len(rows)))
    bar.y_axis.title = "Points of search conversion, third quarter 2026"
    bar.y_axis.number_format = "0.00"
    bar.y_axis.majorGridlines = None
    bar.y_axis.scaling.min = 0
    bar.x_axis.tickLblPos = "low"
    bar.x_axis.delete = bar.y_axis.delete = False
    bar.series[0].graphicalProperties.solidFill = "1F6FA8"
    bar.series[1].graphicalProperties.solidFill = "C9CED3"
    for s in bar.series:
        s.graphicalProperties.line.noFill = True
    bar.gapWidth = 60
    line = LineChart()
    line.add_data(Reference(ws, min_col=9, min_row=4, max_row=4 + len(rows)), titles_from_data=True)
    for s in line.series:
        s.graphicalProperties.line.solidFill = "B5471B"
        s.graphicalProperties.line.width = 15875
        s.graphicalProperties.line.dashStyle = "dash"
        s.marker.symbol = "none"
        s.smooth = False
    bar += line
    bar.legend.position = "b"
    bar.height, bar.width = 9.8, 25.5
    ws.add_chart(bar, "A%d" % (r2 + 6))
    ws.print_area = "A1:H%d" % (r2 + 27)
    ws.page_setup.fitToHeight = 1
    return ws


def month_sheet(wb, f):
    ws = wb.create_sheet("Cost by month")
    worst = max(MONTHS, key=lambda n: f["month"][n])
    _title(ws, "%s was the costliest month: %.2f points across the seven groups" % (worst, f["month"][worst]),
           "Each group's cost over each month's search sessions and over the quarter's, in points of search conversion "
           "(Charter 3.4). A group's quarterly figure is its months weighted by their sessions.", span=6)
    for c, t in enumerate(["Feature group"] + MONTHS + ["Third quarter", "Tier for 2027"], 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 6, 30)
    gm = f["group_month"]
    rows = ranked(f)
    for i, j in enumerate(rows):
        ws.cell(row=5 + i, column=1, value=_name(j))
        for c, n in enumerate(MONTHS, 2):
            ws.cell(row=5 + i, column=c, value=gm[j][n]).number_format = F4
        ws.cell(row=5 + i, column=5, value=f["cost"][j]).number_format = F3
        ws.cell(row=5 + i, column=5).font = Font(bold=True)
        ws.cell(row=5 + i, column=6, value="Tier one" if j in f["list"] else "Present tier")
    r = 5 + len(rows)
    ws.cell(row=r, column=1, value="All feature groups together").font = Font(bold=True)
    for c, n in enumerate(MONTHS, 2):
        ws.cell(row=r, column=c, value=f["month"][n]).number_format = F2
    ws.cell(row=r, column=5, value=f["all"]).number_format = F2
    ws.cell(row=r + 1, column=1, value="Tier one groups together").font = Font(bold=True)
    ws.cell(row=r + 1, column=5, value=f["listed_cost"]).number_format = F2
    _body(ws, 5, r + 1, 6)
    _note(ws, r + 3, "Source: search sessions by hour from the edge log; each group's default share and effect as on sheet "
          "Inputs. Months are the mart's business days, 1 July to 30 September 2026.", 6)
    _widths(ws, [30, 12, 12, 12, 14, 14])
    ws.freeze_panes = "B5"


def inputs_sheet(wb, f):
    ws = wb.create_sheet("Inputs")
    fs = f["fresh_share_pct"]
    _title(ws, "Three things the test and status records do not hold decide the list",
           "An ablation test withholds a group where pages are ranked, and %d per cent of app and %d per cent of web result "
           "page views were built at origin in the quarter, the rest served from the page cache (%d and %d per cent before "
           "the cache lifetime changed on 9 June). A value is served for its validity after its source fails. Three groups "
           "are also read by a page component." % (fs["app"]["q3"], fs["web"]["q3"], fs["app"]["before"], fs["web"]["before"]),
           span=13, sub_height=48)
    head = ["Feature group", "Pipeline stage", "Value served for (hours)", "Effect in the ablation tests as reported (points a session)",
            "Full effect a session at the default (points)", "Status record: unhealthy share, third quarter (per cent)",
            "Sessions served the default over normal service (per cent)", "Cost through the ranking model (points)",
            "Page component that reads the group", "Component's loss per eligible session (points)",
            "Eligible share of sessions in its test (per cent)", "Cost through the component (points)", "Cost (points)"]
    for c, t in enumerate(head, 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 13, 84)
    for i, j in enumerate(G):
        r = 5 + i
        ttl = C.G[j]["ttl"]
        row = [_name(j), "rank" if C.G[j]["pre"] else "rerank", int(ttl) if ttl else "request time", f["measured_effect"][j],
               f["full_effect"][j], f["status_unhealthy_pct"][j], f["served_default_pct"][j], f["rank_cost"][j],
               WL.COMPONENT.get(j), f["reader_per_eligible"].get(j), f["reader_eligible_pct"].get(j), f["reader_cost"].get(j),
               f["cost"][j]]
        for c, v in enumerate(row, 1):
            ws.cell(row=r, column=c, value=v)
        for c in (4, 5, 6, 7, 10):
            ws.cell(row=r, column=c).number_format = F2
        for c in (8, 12, 13):
            ws.cell(row=r, column=c).number_format = F3
        ws.cell(row=r, column=13).font = Font(bold=True)
        ws.cell(row=r, column=3).alignment = Alignment(horizontal="right")
        ws.cell(row=r, column=2).alignment = ws.cell(row=r, column=9).alignment = Alignment(horizontal="center")
    _body(ws, 5, 4 + len(G), 13)
    s = f["seller"]
    _note(ws, 6 + len(G), "The full effect is the reported effect of a group's %d completed tests over the share of the held "
          "slice's result page views built at origin on the test's days, by device, net of the default served on those days; "
          "trending clicks' is stated with the range %s points. The default share is each source's state replayed from "
          "the feed gap, batch, lag and scoring logs with the value's validity, weighted by the traffic the source carries; "
          "for the request-time groups it is the status record's share of requests. Seller quality: %.2f per cent of scoring "
          "runs failed in the quarter, %.2f per cent of sessions were served a default score, %.2f per cent would have been "
          "with every failed run scored (sellers with nothing new to score), leaving %.2f per cent (range %s). A component's "
          "cost is its loss per eligible session in its own holdout test, on the sessions its render record counts as "
          "eligible, at the group's default share; the delivery promise badge's is stated with the range %s points." % (
              f["counts"]["tests_per_group"], _rng(f["c1_band"], 2), s["failed_share_q3_pct"], s["total_default_pct"],
              s["usual_default_pct"], f["c2"], _rng(f["c2_band"], 2), _rng(f["c3_band"])), 13, 92)
    _widths(ws, [20, 10, 11, 14, 13, 14, 14, 13, 24, 13, 12, 13, 10])
    ws.freeze_panes = "B5"


def april_sheet(wb, f):
    ws = wb.create_sheet("April check")
    a = f["april"]
    _title(ws, "April's missed price batches: the estimate calls %.3f points, the conversion record shows %.3f" % (a["golden"], a["record"]),
           "On %d nights in April the competitor price batch did not reach serving region fra2. Users are assigned to a "
           "region by hash and each region has its own page cache, so the mart's conversion in ams1 less fra2 over the %d "
           "business days the expired prices touch measures what the group's default cost there. None of it is in the "
           "third quarter; it is used only to check the route." % (a["batches"], a["days"]), span=4, sub_height=58)
    for c, t in enumerate(["Route", "Called for April (points)", "Away from the record (points)"], 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 3, 36)
    rv = a["rivals"]
    rows = [("Conversion record: ams1 less fra2 (standard error %.3f)" % a["record_se"], a["record"], None),
            ("This estimate (range %s)" % _rng(a["band"]), a["golden"], a["off"]),
            ("Ablation effects as reported (not taken over the share built at origin)", rv["S1 lost"]["value"], rv["S1 lost"]["off"]),
            ("Status record's unhealthy hours in place of the hours the prices had expired", rv["S2 lost"]["value"], rv["S2 lost"]["off"]),
            ("Ranking model only (no price match label)", rv["S3 lost"]["value"], rv["S3 lost"]["off"]),
            ("All three of these together", rv["every stump lost"]["value"], rv["every stump lost"]["off"])]
    for i, (name, v, off) in enumerate(rows):
        ws.cell(row=5 + i, column=1, value=name).alignment = WRAP
        ws.cell(row=5 + i, column=2, value=v).number_format = F3
        if off is not None:
            ws.cell(row=5 + i, column=3, value=off).number_format = F3
        ws.row_dimensions[5 + i].height = 30
    ws.cell(row=6, column=1).font = Font(bold=True)
    _body(ws, 5, 4 + len(rows), 3)
    _middle(ws, 5, 4 + len(rows), 3)
    b = f["april_batch_days"]
    _note(ws, 6 + len(rows), "Over the seven batch days alone the record shows %.3f points and the estimate calls %.3f; the "
          "three shortcuts call %.3f, %.3f and %.3f. Source: the conversion mart by serving region and business day; the "
          "batch log's status by region." % (b["record"], b["golden"], b["rivals"]["S1"]["value"], b["rivals"]["S2"]["value"],
                                              b["rivals"]["S3"]["value"]), 4, 44)
    _widths(ws, [62, 16, 16, 4])
    ws.freeze_panes = "A5"


def routes_sheet(wb, f):
    ws = wb.create_sheet("Routes")
    _title(ws, "What each shortcut would file: none gives the estimate's list",
           "Third-quarter cost in points of search conversion. A figure on the other side of the 0.05 line from the "
           "estimate's is shaded.", span=10)
    for c, t in enumerate(["Route"] + [_name(j) for j in G] + ["All together", "Tier one list"], 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 10, 36)
    rows = [("This estimate", f["cost"], f["all"], f["list"])]
    rows += [(_cap(f["routes"][k]["name"]), f["routes"][k]["cost"], f["routes"][k]["all"], f["routes"][k]["list"]) for k in ORDER]
    for i, (name, d, tot, lst) in enumerate(rows):
        ws.cell(row=5 + i, column=1, value=name).alignment = WRAP
        for c, j in enumerate(G, 2):
            cell = ws.cell(row=5 + i, column=c, value=d[j])
            cell.number_format = F3
            if (d[j] >= f["line"]) != (f["cost"][j] >= f["line"]):
                cell.fill = MISS
        ws.cell(row=5 + i, column=9, value=tot).number_format = F2
        ws.cell(row=5 + i, column=10, value=", ".join(lst)).alignment = WRAP
        ws.row_dimensions[5 + i].height = 44
    ws.cell(row=5, column=1).font = Font(bold=True)
    _body(ws, 5, 4 + len(rows), 10)
    _middle(ws, 5, 4 + len(rows), 10)
    _widths(ws, [52, 10, 10, 10, 10, 10, 10, 10, 11, 30])
    ws.freeze_panes = "B5"


def sensitivity_sheet(wb, f):
    ws = wb.create_sheet("Sensitivity")
    nv = f["nearest_variant"]
    _title(ws, "The list holds under every convention: the nearest any comes to the line is %.3f points (%s)" % (
        nv["distance"], _name(nv["group"])),
           "Third-quarter cost in points of search conversion under %d sets of estimating conventions, the readings beside "
           "them, and each fitted input moved by the furthest any convention moves it." % f["variants"], span=9)
    for c, t in enumerate(["Across the conventions"] + [_name(j) for j in G], 1):
        ws.cell(row=4, column=c, value=t)
    _hdr(ws, 4, 8, 36)
    for i, (lab, k) in enumerate((("Lowest", 0), ("Highest", 1))):
        ws.cell(row=5 + i, column=1, value=lab)
        for c, j in enumerate(G, 2):
            ws.cell(row=5 + i, column=c, value=f["variant_range"][j][k]).number_format = F4
    ws.cell(row=7, column=1, value="One spread of the full effect (per cent of itself)")
    ws.cell(row=8, column=1, value="One spread of the default share (per cent of itself)")
    ws.cell(row=9, column=1, value="One spread of the component's cost (per cent of itself)")
    for c, j in enumerate(G, 2):
        for k, key in enumerate(("effect", "served", "reader")):
            ws.cell(row=7 + k, column=c, value=f["spreads_pct"][j][key]).number_format = "0.0"
    _body(ws, 5, 9, 8)
    r0 = 11
    for c, t in enumerate(["Input moved"] + [_name(j) for j in G] + ["List"], 1):
        ws.cell(row=r0, column=c, value=t)
    _hdr(ws, r0, 9, 30)
    for i, p in enumerate(f["perturbations"]):
        ws.cell(row=r0 + 1 + i, column=1, value=_cap(p["input"]))
        for c, j in enumerate(G, 2):
            ws.cell(row=r0 + 1 + i, column=c, value=p["cost"][j]).number_format = F4
        ws.cell(row=r0 + 1 + i, column=9, value="Unchanged" if p["call_holds"] else "Changed").alignment = Alignment(horizontal="center")
    last = r0 + len(f["perturbations"])
    _body(ws, r0 + 1, last, 9)
    r1 = last + 2
    for c, t in enumerate(["Reading beside the conventions"] + [_name(j) for j in G] + ["List"], 1):
        ws.cell(row=r1, column=c, value=t)
    _hdr(ws, r1, 9, 30)
    for i, b in enumerate(f["beside"]):
        ws.cell(row=r1 + 1 + i, column=1, value=_cap(b["name"])).alignment = Alignment(wrap_text=True, vertical="center")
        for c, j in enumerate(G, 2):
            ws.cell(row=r1 + 1 + i, column=c, value=b["cost"][j]).number_format = F4
            ws.cell(row=r1 + 1 + i, column=c).alignment = Alignment(vertical="center")
        ws.cell(row=r1 + 1 + i, column=9, value="Unchanged" if b["call_holds"] else "Changed").alignment = Alignment(
            vertical="center", horizontal="center")
        ws.row_dimensions[r1 + 1 + i].height = 30
    _body(ws, r1 + 1, r1 + len(f["beside"]), 9)
    r2 = r1 + len(f["beside"]) + 2
    for c, t in enumerate(["Effects from a part of each group's tests (not used)"] + [_name(j) for j in G] + ["List"], 1):
        ws.cell(row=r2, column=c, value=t)
    _hdr(ws, r2, 9, 30)
    order = ["the quarter's own tests", "the four tests from June", "the latest test alone"]
    assert sorted(order) == sorted(f["rival_test_subsets"])
    for i, nm in enumerate(order):
        b = f["rival_test_subsets"][nm]
        ws.cell(row=r2 + 1 + i, column=1, value=_cap(nm))
        for c, j in enumerate(G, 2):
            ws.cell(row=r2 + 1 + i, column=c, value=b["cost"][j]).number_format = "0.000"
        ws.cell(row=r2 + 1 + i, column=9, value="Unchanged" if b["call_holds"] else "Changed").alignment = Alignment(
            horizontal="center")
    _body(ws, r2 + 1, r2 + len(f["rival_test_subsets"]), 9)
    ta = f["test_agreement"]["trend"]
    _note(ws, r2 + len(f["rival_test_subsets"]) + 2, "A group's nine tests agree once each is taken over the pages built "
          "without the group (Cochran's Q %.1f on %d degrees of freedom for trend), so a part of them measures the same "
          "effect less precisely: the quarter's three carry %.1f times the standard error of the nine." % (
              ta["q"], ta["df"], ta["se_ratio_quarter"]), 9, 30)
    _note(ws, r2 + len(f["rival_test_subsets"]) + 4, "The conventions: effects by device, by market and device, or pooled; weighted by "
          "sessions or by precision; on every completed test, the first half's or those from April; netted or not for the "
          "default served on a test's own days; the share built at origin by day or averaged over each test; a snapshot "
          "taken as fresh, 7.5 minutes or a full sync interval old when its feed stops; counters back at once, one hour or two "
          "hours after catch-up; sellers weighted by the month's or the quarter's traffic; what normal service leaves at "
          "the default for sellers from the same nights replayed, or the level of the second quarter, June or the first "
          "half; a component's loss by device or pooled; its lost sessions from its eligible sessions at the group's "
          "default share, or from its failed renders over the rate at which it fails with the value present, or over its "
          "rate in the second quarter, June or the first half; and every pair of these that changes two different choices.",
          9, 110)
    _widths(ws, [58, 11, 11, 11, 11, 11, 11, 11, 12])
    ws.freeze_panes = "B5"


def basis_sheet(wb, f):
    ws = wb.create_sheet("Basis")
    ws["A1"] = "Definitions and conventions"
    ws["A1"].font = Font(bold=True, size=12)
    k = f["counts"]
    lines = [
        ("Search conversion", "Orders attributed to search sessions over search sessions, in per cent; a difference is in "
                              "percentage points (Charter 3.1)."),
        ("Cost", "The conversion the quarter's search sessions in the six markets would have had with the group in normal "
                 "service to every service that reads it, less the conversion as served (3.3). Groups together are the sum; "
                 "a month's cost is taken over that month's sessions (3.4)."),
        ("Normal service", "Each source refreshing on its schedule and the services the group is read from answering (3.2). "
                           "A seller with no newly settled orders is in normal service at the default score once its "
                           "last score is five days old."),
        ("Quarter", "1 July to 30 September 2026 by the mart's business days (2.1)."),
        ("Tier one line", "0.05 points or more (4.1)."),
        ("Records", "As extracted on 12 October 2026. Where the monitor loaded an hour twice the later load stands (%s of "
                    "%s status rows are earlier loads); a scoring row written twice is one run (%s of %s rows); the "
                    "aborted run of a test is left out; feed gap times are converted from local time to UTC." % (
                        format(k["status_rows_reloaded"], ","), format(k["status_rows"], ","),
                        format(k["scoring_repeats"], ","), format(k["scoring_rows"], ","))),
        ("Not used", "The ranking model's offline replay, its feature importance table and its release log carry nothing "
                     "on what was served or lost in the quarter."),
        ("Precision", "Group costs to 0.001 point, months and totals to 0.01, each with its range across conventions."),
    ]
    for i, (key, v) in enumerate(lines):
        ws.cell(row=3 + i, column=1, value=key).font = Font(bold=True)
        ws.cell(row=3 + i, column=2, value=v).alignment = WRAP
        ws.row_dimensions[3 + i].height = 46
    _widths(ws, [22, 112])


def write_csv(path, f):
    lines = ["feature_group,month,cost_points"]
    for j in G:
        for n in MONTHS:
            lines.append("%s,%s,%.4f" % (j, MONTH_KEY[n], f["group_month"][j][n]))
    with open(path, "w", newline="") as fh:
        fh.write("\r\n".join(lines) + "\r\n")
    return len(lines) - 1


def build(folder, f):
    os.makedirs(folder, exist_ok=True)
    wb = Workbook()
    first_sheet(wb, f)
    month_sheet(wb, f)
    inputs_sheet(wb, f)
    april_sheet(wb, f)
    sensitivity_sheet(wb, f)
    routes_sheet(wb, f)
    basis_sheet(wb, f)
    wb.save(os.path.join(folder, FILES["wb"]))
    return write_csv(os.path.join(folder, FILES["csv"]), f)
