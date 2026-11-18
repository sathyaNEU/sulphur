"""The two golden files: the workbook the head of supply chain opens (the cover for each container type on its first
sheet, the working behind it) and the slides for the order meeting. Every number comes from figures.json."""
import datetime as dt
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from openpyxl import Workbook  # noqa: E402
from openpyxl.chart import BarChart, Reference  # noqa: E402
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side  # noqa: E402
from pptx import Presentation  # noqa: E402
from pptx.dml.color import RGBColor  # noqa: E402
from pptx.util import Emu, Pt  # noqa: E402

FILES = {"wb": "wrenfold_container_fleet_2027.xlsx", "deck": "wrenfold_container_order_2027.pptx"}
POOLS = ("K50", "K30", "K20", "FIR", "KIL")
AUTHOR = "Justin Francis"
DATED = "9 December 2026"
HEAD = PatternFill("solid", fgColor="2F3E46")
FILL = {"buy": "CFE0F5", "hire": "FBDCCB", "nothing": "E4E5E2"}
THIN = Side(style="thin", color="B8BEC8")
INK, INK2, RULE, BG = "#0b0b0b", "#52514e", "#c9c8c2", "#fcfcfb"
BLUE, ORANGE, GREY = "#2a78d6", "#eb6834", "#8a8f98"
COVER = {"buy": "Purchase", "hire": "Seasonal hire", "nothing": "No cover"}
COLOR = {"buy": BLUE, "hire": ORANGE, "nothing": GREY}
ROUTES = [("golden", "This review"),
          ("S1", "Stock at customers moved in step with deliveries"),
          ("S2", "Cold store at summer 2026's weeks of cover"),
          ("S3", "Tagged kegs' loss rate used for every type"),
          ("S1+S2+S3", "All three together"),
          ("direct", "Register as the fleet, scaled to the busiest week"),
          ("rigorous", "Tagged kegs' own stock response, store regressed on deliveries, tagged loss rate")]


def k(x):
    return "{:,}".format(int(x))


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _short(names):
    """50 litre kegs and 20 litre kegs read as 50 and 20 litre kegs"""
    kegs = [n for n in names if n.endswith("litre kegs")]
    rest = [n for n in names if not n.endswith("litre kegs")]
    if len(kegs) > 1:
        kegs = [_list([n.split(" ")[0] for n in kegs]) + " litre kegs"]
    return _list(kegs + rest)


def day(iso):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year)


def headline(f, cap=True):
    by = {c: [f["plural"][p] for p in POOLS if f["cover"][p] == c] for c in ("buy", "hire", "nothing")}
    parts = []
    if by["buy"]:
        parts.append("buy %s" % _short(by["buy"]))
    if by["hire"]:
        parts.append("hire %s for the summer" % _short(by["hire"]))
    if by["nothing"]:
        parts.append("leave %s alone" % _short(by["nothing"]))
    s = ", ".join(parts)
    return s[0].upper() + s[1:] if cap else s


def rejected(f):
    r = f["routes"]["S1+S2+S3"]
    moved = [p for p in POOLS if r[p]["cover"] != f["cover"][p]]
    return _list("%s for %s (%s)" % ({"buy": "a purchase", "hire": "a seasonal hire", "nothing": "no cover"}[r[p]["cover"]],
                                     f["plural"][p], k(r[p]["plan"])) for p in moved)


def _hdr(ws, row, n, height=44):
    for c in ws[row][:n]:
        c.font = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = Border(bottom=THIN)
    ws.row_dimensions[row].height = height


def _widths(ws, ws_):
    for col, w in zip("ABCDEFGHIJKLMNOPQRST", ws_):
        ws.column_dimensions[col].width = w


def _title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12, name="Calibri")
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, size=9, color="555555", name="Calibri")


def _note(ws, row, text, span, height=30):
    c = ws.cell(row=row, column=1, value=text)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    c.font = Font(size=9, color="444444", name="Calibri")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=span)
    ws.row_dimensions[row].height = height


def _num(ws, row, cols, fmt="#,##0"):
    for c in cols:
        ws.cell(row=row, column=c).number_format = fmt


def first_sheet(wb, f):
    ws = wb.active
    ws.title = "Cover 2027"
    c = f["counts"]
    _title(ws, "Container fleets for summer 2027: " + headline(f, cap=False),
           "Fleet standard FS-04 issue 3, sections 3 and 4. Annual count of %s. %s, %s." % (day(c["count_dates"][-1]), AUTHOR, DATED))
    ws["A3"] = ("This is not what the usual sizing gives. With the stock at customers moved in step with deliveries, the cold "
                "store held at summer 2026's weeks of cover and the tagged kegs' loss rate used for every type, the same "
                "records give %s. The Routes sheet sets each of those three choices beside this review." % rejected(f))
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:H3")
    ws.row_dimensions[3].height = 46
    ws.append([])
    hdr = ["Container type", "Largest weekly shortfall, planning case (containers)", "Hot case (containers)",
           "Maker's minimum order run (containers)", "Cover", "Week of the planning case's figure (week beginning)",
           "Planning case across the conventions tried, low", "Planning case across the conventions tried, high"]
    ws.append(hdr)
    _hdr(ws, 5, len(hdr), 60)
    for i, p in enumerate(POOLS):
        ws.append([f["names"][p].capitalize(), f["plan"][p], f["hot"][p], f["min_run"][p], COVER[f["cover"][p]],
                   dt.date.fromisoformat(f["plan_week"][p]), f["variant_range"][p][0], f["variant_range"][p][1]])
        row = 6 + i
        _num(ws, row, (2, 3, 4, 7, 8))
        ws.cell(row=row, column=6).number_format = "dd mmm yyyy"
        ws.cell(row=row, column=5).fill = PatternFill("solid", fgColor=FILL[f["cover"][p]])
        ws.cell(row=row, column=5).alignment = Alignment(horizontal="center")
    last = 5 + len(POOLS)
    notes = [
        "Cover is read on the planning case (FS-04 4.1): nil or negative, no cover; above nil and below the maker's minimum "
        "order run, a seasonal hire; the minimum order run or more, a purchase. Minimum order runs from quotation %s. A "
        "negative figure is a surplus (2.3)." % f["stated"]["quotation"],
        "The season is the %d weeks beginning %s to %s (3.1). The planning case takes every week at the Calder Vale normal "
        "(3.2); the hot case is the second highest of the ten summers %d to %d (3.3) and does not change the cover."
        % (c["season_weeks"], day(f["season"][0]), day(f["season"][1]), c["summers"][0], c["summers"][1]),
        "Nobody counts the containers at customers or the ones lost there, so each figure is an estimate: the sheets behind "
        "this one give the stock account, what a cellar holds, the cold store under the 2027 brew plan and the weekly path. "
        "The last two columns are the lowest and highest planning-case figure across %s rebuilds on other reasonable "
        "conventions (sheet Sensitivity); the cover is the same in every one." % k(f["variants"] - 1)]
    for i, t in enumerate(notes):
        _note(ws, last + 2 + i, t, 8, 40)
    _widths(ws, (17, 17, 13, 15, 15, 17, 15, 15))
    ws.freeze_panes = "B6"
    bar = BarChart()
    bar.type = "col"
    bar.title = "Largest weekly shortfall of summer 2027 against the maker's minimum order run"
    bar.y_axis.title = "Containers"
    bar.add_data(Reference(ws, min_col=2, max_col=4, min_row=5, max_row=last), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=6, max_row=last))
    bar.y_axis.number_format = "#,##0"
    bar.y_axis.delete = False
    bar.x_axis.delete = False
    bar.x_axis.tickLblPos = "low"
    for s, col in zip(bar.series, ("2A78D6", "EB6834", "8A8F98")):
        s.graphicalProperties.solidFill = col
        s.graphicalProperties.line.solidFill = col
    bar.gapWidth = 80
    bar.overlap = -10
    bar.height, bar.width = 8.6, 19.5
    bar.legend.position = "b"
    ws.add_chart(bar, "A%d" % (last + 6))
    ws.print_area = "A1:H%d" % (last + 24)
    ws.page_setup.orientation = "landscape"


def path_sheet(wb, f):
    ws = wb.create_sheet("Weekly path")
    _title(ws, "Requirement, fleet and shortfall by week, planning case",
           "FS-04 2.1 to 2.3. Weeks from the count of %s to the end of the season; the fleet is the count's, with no purchase and no hire."
           % day(f["counts"]["count_dates"][-1]))
    ws.append([])
    hdr = ["Container type", "Week beginning", "In the season", "Containers delivered in the week", "At customers",
           "Full in the cold store", "Depots, wash and repair", "Float", "Requirement", "Fleet", "Shortfall"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 46)
    r = 5
    for p in POOLS:
        for x in f["path"][p]:
            ws.append([f["names"][p].capitalize(), dt.date.fromisoformat(x["week"]), "yes" if x["in_season"] else "",
                       x["deliveries"], x["at_customers"], x["store"], x["other"], x["float"], x["requirement"], x["fleet"],
                       x["shortfall"]])
            ws.cell(row=r, column=2).number_format = "dd mmm yyyy"
            _num(ws, r, range(4, 12))
            if x["in_season"] and x["week"] == f["plan_week"][p]:
                for col in range(1, 12):
                    ws.cell(row=r, column=col).font = Font(bold=True)
            r += 1
    ws.auto_filter.ref = "A4:K%d" % (r - 1)
    _widths(ws, (16, 13, 9, 13, 12, 12, 12, 9, 12, 10, 10))
    ws.freeze_panes = "C5"
    ws.print_title_rows = "4:4"


def cellars_sheet(wb, f):
    ws = wb.create_sheet("Cellars")
    _title(ws, "What a cellar holds: a fixed stock for each line and cover for its delivery interval",
           "Reps' cellar counts by line (full, on dispense and empty) against the line's deliveries and its account's delivery interval.")
    ws.append([])
    hdr = ["Container type", "Line counts used", "Held per line whatever it sells", "Held per container sold a week, weekly call",
           "Held per container sold a week, two calls a week", "Type average per container delivered a week",
           "Deliveries a week at the count", "Deliveries in the worst week", "of which the new estate",
           "New estate's cellars at the worst week", "Rise in stock at customers, count to worst week"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 62)
    for i, p in enumerate(POOLS):
        d = f["pool"][p]
        ws.append([f["names"][p].capitalize(), d["audit_counts"], d["fixed_per_line"], d["per_sale_weekly"], d["per_sale_twice"],
                   d["per_sale_pool"], d["level_at_count"], d["deliveries_at_week"], d["estate_at_week"], d["estate_cellars"],
                   d["swing"]])
        row = 5 + i
        _num(ws, row, (2, 7, 8, 9, 10, 11))
        _num(ws, row, (3, 4, 5), "0.00")
        _num(ws, row, (6,), "0.000")
    row = 5 + len(POOLS)
    ws.cell(row=row, column=1, value="All five types").font = Font(bold=True)
    ws.cell(row=row, column=11, value=f["trade_rise"]).font = Font(bold=True)
    _num(ws, row, (11,))
    rf = f["referee"]
    e = f["estate"]
    notes = [
        "The rise is the type average times the change in weekly deliveries of the accounts supplied today, plus the new "
        "estate's cellars (%s outlets under the supply agreement signed 23 October 2026: its lines at the fixed stock, and "
        "its scheduled volume at the weekly-call figure)." % k(e["pubs"]),
        "Deliveries at the count are the fitted season's value for the count's own week. The mean of the four weeks before "
        "the count is one of the conventions on the Sensitivity sheet.",
        "Check on the tagged 20 litre kegs, the one type whose stock at customers can be counted: from the count of "
        "December 2025 to the busiest three weeks of summer 2026 (around the week of %s) the tags show %s more kegs at "
        "customers (%s to %s). The line relation gives %s for the same weeks; stock moved in step with deliveries would "
        "have been %s." % (day(rf["week"]), k(rf["seen"]), k(rf["start"]), k(rf["top"]), k(rf["golden"]), k(rf["proportional"]))]
    for i, t in enumerate(notes):
        _note(ws, row + 2 + i, t, 11, 34)
    _widths(ws, (16, 10, 12, 13, 13, 13, 12, 12, 11, 13, 14))
    ws.freeze_panes = "B5"


def account_sheet(wb, f):
    ws = wb.create_sheet("Stock account")
    _title(ws, "The register never loses a container: what went missing at customers comes from the counts",
           "Register (bought and not condemned) less the annual count on Wrenfold's sites, by count.")
    ws.append([])
    hdr = ["Container type", "Count", "On the register", "Counted on site", "Off site", "Delivered in the year to the count",
           "Rise in off site over the year", "Change in stock at customers over the year", "Lost at customers in the year",
           "Lost, per cent of deliveries", "Condemned at the wash in the year"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 58)
    r = 5
    for p in POOLS:
        d = f["pool"][p]
        dates = sorted(f["account"][p])
        for j, iso in enumerate(dates):
            a = f["account"][p][iso]
            row = [f["names"][p].capitalize(), dt.date.fromisoformat(iso), a["register"], a["on_site"], a["off_site"]]
            if j == len(dates) - 1:
                row += [f["deliveries"][p]["last_year"], d["off_site_gain"], d["trade_change"],
                        f["year_loss_by_pool"][p], d["loss_pct"] / 100.0, d["condemned_last_year"]]
            ws.append(row)
            ws.cell(row=r, column=2).number_format = "dd mmm yyyy"
            _num(ws, r, (3, 4, 5, 6, 7, 8, 9, 11))
            _num(ws, r, (10,), "0.00%")
            r += 1
    t = f["tags"]
    notes = [
        "Lost at customers in the year is the rise in off site less the change in the stock customers hold (the Cellars "
        "relation on the change in deliveries between the two counts). Over the four types without tags it comes to %s "
        "containers." % k(f["year_loss"]),
        "The 20 litre kegs carry tags, so their loss is read from the recovery agent's cases: %s kegs not traced of %s "
        "delivered in the 52 weeks to %s (the latest whose cases have all closed), %s per cent. That rate applied to the "
        "other four types would put their year's loss at %s." % (
            k(t["not_traced"]), k(t["delivered"]), day(t["window"][1]), "%.2f" % t["loss_pct"],
            k(f["route_components"]["S3"]["C3"])),
        "Containers condemned at the wash leave the register and are taken forward at last year's rate per delivery."]
    for i, x in enumerate(notes):
        _note(ws, r + 1 + i, x, 11, 34)
    _widths(ws, (16, 12, 12, 11, 10, 13, 12, 14, 13, 11, 13))
    ws.freeze_panes = "C5"


def store_sheet(wb, f):
    ws = wb.create_sheet("Cold store")
    _title(ws, "The cold store holds each beer a racking run at a time, and the 2027 plan changes the runs and the range",
           "Monday position against the racking log, December 2024 to November 2026; brew plan 2027 issue 1.")
    ws.append([])
    hdr = ["Container type", "Cover beside the runs (weeks of deliveries)", "Beers racked in 2026", "Half a run per beer, 2026",
           "Beers on sale in the worst week of 2027", "Half a run per beer, 2027 plan", "Deliveries in the worst week",
           "Full in the cold store, worst week", "Same week on summer 2026's weeks of cover"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 62)
    for i, p in enumerate(POOLS):
        d = f["pool"][p]
        ws.append([f["names"][p].capitalize(), d["store_cover_weeks"], d["beers_2026"], d["half_runs_2026"], d["beers_at_week"],
                   f["half_runs_at_week"][p], d["deliveries_at_week"], d["store"], f["store_cover_route"][p]])
        _num(ws, 5 + i, (3, 4, 5, 6, 7, 8, 9))
        _num(ws, 5 + i, (2,), "0.00")
    row = 5 + len(POOLS)
    ws.cell(row=row, column=1, value="All five types").font = Font(bold=True)
    ws.cell(row=row, column=8, value=f["store_2027"]).font = Font(bold=True)
    ws.cell(row=row, column=9, value=f["route_components"]["S2"]["C2"])
    _num(ws, row, (8, 9))
    _note(ws, row + 2, "A beer racked a run at a time sits, on average, at half a run above its cover, so the store's stock "
                       "follows the runs and the number of beers on sale as well as the deliveries. The last column carries "
                       "each type's weeks of cover in the same weeks of 2026 to 2027's deliveries (for each type's own "
                       "worst week on that reading).", 9, 34)
    r = row + 5
    hdr2 = ["Container type", "Product", "Racking run in 2026 (median filled)", "Racking run in the 2027 plan, worst week",
            "On sale in the worst week"]
    for j, h in enumerate(hdr2):
        ws.cell(row=r, column=1 + j, value=h)
    _hdr(ws, r, len(hdr2), 46)
    r += 1
    for p in POOLS:
        skus = sorted({b["sku"] for b in f["beers"][p]} | set(f["runs_2026"][p]))
        for s in skus:
            now = [b for b in f["beers"][p] if b["sku"] == s and b["on_sale_at_week"]]
            ws.append([f["names"][p].capitalize(), s, f["runs_2026"][p].get(s), now[0]["run"] if now else None,
                       "yes" if now else "no"])
            _num(ws, r, (3, 4))
            r += 1
    _widths(ws, (16, 14, 14, 14, 14, 13, 12, 13, 14))
    ws.freeze_panes = "B5"


def summers_sheet(wb, f):
    ws = wb.create_sheet("Ten summers")
    yrs = sorted(f["summers"]["K50"])
    _title(ws, "Hot case: the season run on each recorded summer, second highest of the ten",
           "FS-04 3.3. Each summer's 21 season weeks in order from its own first Monday of May; other weeks at the normal.")
    ws.append([])
    hdr = ["Container type"] + yrs + ["Hot case", "Summer it comes from", "Planning case"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 34)
    for i, p in enumerate(POOLS):
        ws.append([f["names"][p].capitalize()] + [f["summers"][p][y] for y in yrs] + [f["hot"][p], f["hot_year"][p], f["plan"][p]])
        _num(ws, 5 + i, list(range(2, 12)) + [12, 14])
        j = yrs.index(str(f["hot_year"][p]))
        ws.cell(row=5 + i, column=2 + j).font = Font(bold=True)
    _widths(ws, (16,) + (9,) * 10 + (10, 12, 11))
    ws.freeze_panes = "B5"


def routes_sheet(wb, f):
    ws = wb.create_sheet("Routes")
    _title(ws, "What each shortcut would have ordered",
           "Largest weekly shortfall, planning case, with the cover it implies. One choice changed at a time, then all three.")
    ws.append([])
    hdr = ["How the fleets are sized"]
    for p in POOLS:
        hdr += [f["names"][p].capitalize(), "Cover"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 34)
    for i, (key, label) in enumerate(ROUTES):
        row = [label]
        for p in POOLS:
            row += [f["routes"][key][p]["plan"], COVER[f["routes"][key][p]["cover"]]]
        ws.append(row)
        for j, p in enumerate(POOLS):
            _num(ws, 5 + i, (2 + 2 * j,))
            if f["routes"][key][p]["cover"] != f["cover"][p]:
                ws.cell(row=5 + i, column=3 + 2 * j).fill = PatternFill("solid", fgColor="F6D5D2")
        if key == "golden":
            for col in range(1, len(hdr) + 1):
                ws.cell(row=5 + i, column=col).font = Font(bold=True)
    r = 5 + len(ROUTES) + 1
    rc = f["route_components"]
    _note(ws, r, "Shaded covers differ from this review's. Stock at customers moved in step with deliveries puts the rise to the "
                 "worst week at %s containers over the five types against %s; summer 2026's weeks of cover put the cold "
                 "store at %s against %s; the tagged kegs' loss rate puts the year's loss on the other four types at %s "
                 "against %s." % (k(rc["S1"]["C1"]), k(f["trade_rise"]), k(rc["S2"]["C2"]), k(f["store_2027"]),
                                  k(rc["S3"]["C3"]), k(f["year_loss"])), 11, 40)
    _widths(ws, (54, 12, 13, 12, 13, 12, 13, 12, 13, 12, 13))
    ws.freeze_panes = "B5"


def sensitivity_sheet(wb, f):
    ws = wb.create_sheet("Sensitivity")
    n1 = f["singles"]
    _title(ws, "The cover is the same on every reasonable convention",
           "Largest weekly shortfall, planning case, rebuilt with each convention changed alone and with every two together.")
    ws.append([])
    hdr = ["Convention"] + [f["names"][p].capitalize() for p in POOLS] + ["Cover unchanged"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 30)
    r = 5
    for i, name in enumerate(f["variant_names"][:1 + n1]):
        ws.append([("As used" if i == 0 else name[0].upper() + name[1:])] + [f["variant_plan"][p][i] for p in POOLS] + ["yes"])
        _num(ws, r, range(2, 7))
        r += 1
    for label, j in (("lowest", 0), ("highest", 1)):
        ws.append(["Any two of these together (%s rebuilds), %s" % (k(f["variants"] - 1 - n1), label)] +
                  [f["variant_range"][p][j] for p in POOLS] + ["yes" if f["family_calls_all_golden"] else "no"])
        _num(ws, r, range(2, 7))
        for col in range(1, 8):
            ws.cell(row=r, column=col).font = Font(bold=True)
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Readings not used").font = Font(bold=True)
    r += 1
    for name, v in f["refused"].items():
        ws.cell(row=r, column=1, value=name[0].upper() + name[1:])
        for j, p in enumerate(POOLS):
            ws.cell(row=r, column=2 + j, value=v[p])
        ws.cell(row=r, column=7, value="yes" if all(f["refused_cover"][name][p] == f["cover"][p] for p in POOLS) else "no")
        _num(ws, r, range(2, 7))
        r += 1
    r += 1
    ws.cell(row=r, column=1, value="Fitted inputs moved").font = Font(bold=True)
    r += 1
    for x in f["perturbations"]:
        ws.cell(row=r, column=1, value=x["input"][0].upper() + x["input"][1:])
        for j, p in enumerate(POOLS):
            ws.cell(row=r, column=2 + j, value=x["plan"][p])
        ws.cell(row=r, column=7, value="yes" if x["call_holds"] else "no")
        _num(ws, r, range(2, 7))
        r += 1
    lv, ts = f["levels"]["K50"], f["tests"]["K50"]
    _note(ws, r + 1, "Deliveries at a count are read on the fitted season for the count's own week. Trailing means beyond four "
                     "weeks are not used: for 50 litre kegs the eight weeks before the count average %s a week and the thirteen "
                     "weeks %s, against %s in the count's week (%s and %s per cent above), because the season is falling into "
                     "the count. A single slope in temperature is not used: against it the bend's F statistic for 50 litre kegs "
                     "is %s on 2 and %d degrees of freedom. The trend is not dropped for every type: its t statistic is %s for 20 "
                     "litre kegs, %s for firkins and %s for kilderkins. The store's split is not fitted on 52 Mondays alone: "
                     "the fixed part's standard error is then %s to %s containers. Condemned containers leave the fleet "
                     "(FS-04 2.2)." % (
                         k(lv["eight_weeks"]), k(lv["thirteen_weeks"]), k(lv["fit"]), lv["eight_over_fit_pct"],
                         lv["thirteen_over_fit_pct"], ts["bend_F"], ts["df"], f["tests"]["K20"]["trend_t"],
                         f["tests"]["FIR"]["trend_t"], f["tests"]["KIL"]["trend_t"],
                         k(min(f["split"][p]["se_52"] for p in POOLS)), k(max(f["split"][p]["se_52"] for p in POOLS))), 7, 68)
    _widths(ws, (70, 13, 13, 13, 11, 11, 11))
    ws.freeze_panes = "B5"


def notes_sheet(wb, f):
    ws = wb.create_sheet("Notes")
    c = f["counts"]
    _title(ws, "Sources and conventions")
    rows = [
        ("As of", "Annual count of %s; records to that date." % day(c["count_dates"][-1])),
        ("Requirement, fleet, shortfall", "FS-04 issue 3, 2.1 to 2.3: at customers, full in the cold store, at the depots, in wash "
                                          "and repair, plus a float of two sevenths of the week's deliveries; the fleet with no "
                                          "purchase and no hire after the count."),
        ("Season and cases", "FS-04 3.1 to 3.4. The season as contracted and planned at the review: accounts supplied, the "
                             "Maplestead agreement's outlets from their listing dates, the range and brew plan as issued."),
        ("Deliveries", "%s docket lines over %s weeks from %s; %s lines re-sent by a handheld counted once; %s lines with no "
                       "container code read from the product; %s renumbered accounts under their current number."
         % (k(c["delivery_lines"]), c["weeks"], day(c["first_week"]), k(c["resent_rows"]), k(c["blank_codes"]), k(c["renumbered"]))),
        ("Forecast", "Weekly deliveries by type fitted on the season, the trend and the week's mean daily maximum temperature at Calder Vale, "
                     "with the estate's scheduled volume added from each outlet's listing date."),
        ("Tagged kegs", "%s tag reads; %s repeated reads within two minutes dropped; delivery reads cover %s per cent of the "
                        "dockets' 20 litre deliveries and the count of kegs at customers is scaled for that."
         % (k(f["tags"]["reads"]), k(f["tags"]["double_reads"]), f["tags"]["read_share_pct"])),
        ("Rounding", "Whole containers. A negative shortfall is a surplus."),
    ]
    ws.append([])
    for a, b in rows:
        ws.append([a, b])
        ws.cell(row=ws.max_row, column=1).font = Font(bold=True)
        ws.cell(row=ws.max_row, column=2).alignment = Alignment(wrap_text=True, vertical="top")
        ws.row_dimensions[ws.max_row].height = 44
    _widths(ws, (28, 110))


def workbook(path, f):
    wb = Workbook()
    first_sheet(wb, f)
    path_sheet(wb, f)
    cellars_sheet(wb, f)
    account_sheet(wb, f)
    store_sheet(wb, f)
    summers_sheet(wb, f)
    routes_sheet(wb, f)
    sensitivity_sheet(wb, f)
    notes_sheet(wb, f)
    wb.save(path)


# ------------------------------------------------------------------------------------------------- the slides
def _axes(ax):
    ax.set_facecolor(BG)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(RULE)
    ax.tick_params(axis="x", labelsize=8, colors=INK2)
    ax.tick_params(axis="y", length=0, labelsize=9, colors=INK)


def chart_cover(path, f):
    fig, ax = plt.subplots(figsize=(7.4, 3.5), dpi=200)
    fig.patch.set_facecolor(BG)
    _axes(ax)
    order = list(POOLS)[::-1]
    for i, p in enumerate(order):
        col = COLOR[f["cover"][p]]
        ax.barh(i, f["plan"][p], height=0.42, color=col, zorder=3)
        ax.plot([f["min_run"][p]] * 2, [i - 0.36, i + 0.36], color=INK2, lw=2.0, zorder=4)
        ax.plot([f["hot"][p]], [i], "o", ms=6.5, mfc=BG, mec=INK, mew=1.4, zorder=5)
        x = f["plan"][p]
        ax.text(x + (60 if x >= 0 else -60), i + 0.33, k(x), ha="left" if x >= 0 else "right", va="center", fontsize=8.5, color=INK)
    ax.axvline(0, color=INK2, lw=0.9, zorder=2)
    ax.set_yticks(range(len(order)))
    ax.set_yticklabels([f["plural"][p].capitalize() for p in order])
    ax.set_ylim(-0.7, len(order) - 0.3)
    ax.set_xlabel("Containers short in the worst week of the season", fontsize=8.5, color=INK2)
    ax.xaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: k(v)))
    ax.grid(axis="x", color="#e6e5df", lw=0.6, zorder=0)
    ax.set_axisbelow(True)
    for c in ("buy", "hire", "nothing"):
        ax.barh([0], [0], color=COLOR[c], label=COVER[c] + ", planning case")
    ax.plot([], [], "o", ms=6.5, mfc=BG, mec=INK, mew=1.4, ls="", label="Hot case")
    ax.plot([], [], marker="|", color=INK2, ls="", ms=11, mew=2, label="Maker's minimum order run")
    ax.legend(loc="lower right", frameon=False, fontsize=7.5)
    fig.tight_layout()
    fig.savefig(path, facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)


def chart_weeks(path, f):
    fig, axes = plt.subplots(1, 5, figsize=(11.6, 2.9), dpi=200)
    fig.patch.set_facecolor(BG)
    for ax, p in zip(axes, POOLS):
        _axes(ax)
        rows = [x for x in f["path"][p] if x["in_season"]]
        xs = [dt.date.fromisoformat(x["week"]) for x in rows]
        ys = [x["shortfall"] for x in rows]
        col = COLOR[f["cover"][p]]
        ax.plot(xs, ys, color=col, lw=2.0, zorder=3)
        ax.axhline(0, color=INK2, lw=0.9)
        ax.axhline(f["min_run"][p], color=INK2, lw=0.9, ls=(0, (4, 3)))
        j = max(range(len(ys)), key=lambda i: ys[i])
        ax.plot([xs[j]], [ys[j]], "o", ms=6, color=col, mec=BG, mew=1.2, zorder=4)
        ax.annotate(k(ys[j]), (xs[j], ys[j]), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8, color=INK)
        lo, hi = min(min(ys), 0), max(max(ys), f["min_run"][p])
        pad = 0.12 * (hi - lo)
        ax.set_ylim(lo - pad, hi + 1.6 * pad)
        # the line's label goes where the curve leaves it most room: either end, above or below the line
        line, tall, n = f["min_run"][p], 0.10 * (hi - lo), len(ys)
        span = {"left": ys[:int(0.6 * n)], "right": ys[int(0.4 * n):]}
        room = lambda side, up: min(max(0.0, (line - y) if up else (y - line), (y - line - tall) if up else (line - tall - y))
                                    for y in span[side])
        side, up = max(((s, u) for s in ("left", "right") for u in (True, False)), key=lambda c: room(*c))
        ax.text(xs[0] if side == "left" else xs[-1], line + (0.01 if up else -0.02) * (hi - lo),
                (" minimum run %s" if side == "left" else "minimum run %s ") % k(line),
                va="bottom" if up else "top", ha=side, fontsize=7, color=INK2)
        ax.set_title(f["plural"][p].capitalize(), fontsize=9.5, loc="left", color=INK, pad=6)
        ax.set_xticks([dt.date(2027, m, 1) for m in (5, 7, 9)])
        ax.set_xticklabels(["May", "Jul", "Sep"])
        ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: k(v)))
        ax.tick_params(axis="y", labelsize=7.5, colors=INK2)
        ax.grid(axis="y", color="#e6e5df", lw=0.6)
        ax.set_axisbelow(True)
    fig.tight_layout(w_pad=1.3)
    fig.savefig(path, facecolor=fig.get_facecolor(), metadata={"Software": None})
    plt.close(fig)


SW, SH = 12192000, 6858000


def _box(slide, left, top, width, height, lines, size=16, color="0B0B0B", bold_first=False):
    tb = slide.shapes.add_textbox(Emu(left), Emu(top), Emu(width), Emu(height))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines):
        par = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        par.text = line
        par.font.size = Pt(size)
        par.font.color.rgb = RGBColor.from_string(color)
        par.font.bold = bool(bold_first and i == 0)
        par.space_after = Pt(8)
    return tb


def _heading(slide, text):
    t = slide.shapes.title
    t.left, t.top, t.width, t.height = Emu(560000), Emu(300000), Emu(SW - 1120000), Emu(800000)
    t.text = text
    par = t.text_frame.paragraphs[0]
    par.alignment = 1
    par.font.size = Pt(24)
    par.font.bold = True
    par.font.color.rgb = RGBColor.from_string("0B0B0B")
    t.text_frame.word_wrap = True


def _foot(slide, n, total):
    _box(slide, 560000, SH - 430000, SW - 1120000, 300000,
         ["Wrenfold Brewery supply chain. Fleet standard FS-04 issue 3. Workings in %s.   %d of %d" % (FILES["wb"], n, total)],
         size=10, color="7F7F7F")


def _table(slide, left, top, width, rows, widths, size=13, row_h=380000):
    nr, nc = len(rows), len(rows[0])
    gt = slide.shapes.add_table(nr, nc, Emu(left), Emu(top), Emu(width), Emu(row_h * nr)).table
    for j, wd in enumerate(widths):
        gt.columns[j].width = Emu(int(width * wd))
    for i, row in enumerate(rows):
        for j, val in enumerate(row):
            cell = gt.cell(i, j)
            cell.text = str(val)
            cell.fill.solid()
            cell.fill.fore_color.rgb = RGBColor.from_string("2F3E46" if i == 0 else "F4F4F1" if i % 2 else "FFFFFF")
            for par in cell.text_frame.paragraphs:
                par.font.size = Pt(size)
                par.font.bold = i == 0
                par.font.color.rgb = RGBColor.from_string("FFFFFF" if i == 0 else "0B0B0B")
                par.alignment = 1 if j == 0 else 3
    return gt


def deck(path, f, png_cover, png_weeks):
    total = 5
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(SW), Emu(SH)
    lay = prs.slide_layouts[5]
    nm = lambda p: f["plural"][p].capitalize()
    # 1: the cover
    s = prs.slides.add_slide(lay)
    _heading(s, headline(f))
    s.shapes.add_picture(png_cover, Emu(560000), Emu(1250000), width=Emu(7200000))
    lines = ["Largest weekly shortfall of the 2027 season, planning case, against the maker's minimum order run:"]
    lines += ["%s: %s against %s, %s" % (nm(p), k(f["plan"][p]), k(f["min_run"][p]), COVER[f["cover"][p]].lower()) for p in POOLS]
    lines += ["The usual sizing would have given %s." % rejected(f)]
    _box(s, 7950000, 1300000, SW - 7950000 - 500000, 4800000, lines, size=14, bold_first=True)
    _foot(s, 1, total)
    # 2: the weeks
    s = prs.slides.add_slide(lay)
    kegs = [p for p in POOLS if p.startswith("K") and p != "KIL"]
    wk = lambda p: dt.date.fromisoformat(f["plan_week"][p])
    _heading(s, "The keg fleets are shortest in %s, the cask fleets at the end of the season" % _list(
        sorted({wk(p).strftime("%B") for p in kegs}, key=lambda m: dt.datetime.strptime(m, "%B").month)))
    s.shapes.add_picture(png_weeks, Emu(380000), Emu(1350000), width=Emu(SW - 760000))
    _box(s, 560000, 4450000, SW - 1120000, 1700000, [
        "Shortfall by week of the season, planning case (requirement less the fleet counted on %s, no purchase and no hire). "
        "Worst weeks: %s." % (day(f["counts"]["count_dates"][-1]),
                              "; ".join("%s, week of %s" % (f["plural"][p], day(f["plan_week"][p])) for p in POOLS)),
        "The Maplestead outlets join from April and the summer range and racking plan start on 3 May; containers lost at "
        "customers and condemned at the wash come off the fleet week by week."], size=14)
    _foot(s, 2, total)
    # 3: what it is made of
    s = prs.slides.add_slide(lay)
    _heading(s, "Most of the requirement is out of sight: at customers and in the cold store")
    rows = [["Worst week, planning case"] + [nm(p) for p in POOLS]]
    pick = {p: [x for x in f["path"][p] if x["week"] == f["plan_week"][p]][0] for p in POOLS}
    for label, key in (("At customers", "at_customers"), ("Full in the cold store", "store"), ("Depots, wash and repair", "other"),
                       ("Float", "float"), ("Requirement", "requirement"), ("Fleet", "fleet"), ("Shortfall", "shortfall")):
        rows.append([label] + [k(pick[p][key]) for p in POOLS])
    _table(s, 700000, 1350000, SW - 1400000, rows, [0.30, 0.14, 0.14, 0.14, 0.14, 0.14], size=13)
    _box(s, 700000, 4600000, SW - 1400000, 1500000, [
        "From the count to the worst week the stock at customers rises by %s containers over the five types, the new "
        "estate's cellars included. The cold store holds %s under the 2027 brew plan. The four types without tags lost "
        "%s containers at customers in the year to the count." % (k(f["trade_rise"]), k(f["store_2027"]), k(f["year_loss"]))], size=14)
    _foot(s, 3, total)
    # 4: the hot case
    s = prs.slides.add_slide(lay)
    over = [p for p in POOLS if f["cover"][p] == "hire" and f["hot"][p] >= f["min_run"][p]]
    _heading(s, "A hot summer mostly hits the 50 litre kegs" if "K50" in over or f["hot"]["K50"] - f["plan"]["K50"] == max(
        f["hot"][p] - f["plan"][p] for p in POOLS) else "The hot case moves the keg fleets most")
    rows = [["Largest weekly shortfall", "Planning case", "Hot case", "Summer it comes from", "Minimum order run", "Cover"]]
    for p in POOLS:
        rows.append([nm(p), k(f["plan"][p]), k(f["hot"][p]), str(f["hot_year"][p]), k(f["min_run"][p]), COVER[f["cover"][p]]])
    _table(s, 700000, 1350000, SW - 1400000, rows, [0.24, 0.15, 0.15, 0.17, 0.15, 0.14], size=13)
    extra = []
    if over:
        extra.append("In the hot case %s would be short by more than a minimum order run. The standard reads the cover on the "
                     "planning case (4.1), so the hire stands; the hire terms have no upper limit on a booking made by "
                     "26 February 2027." % _short([f["plural"][p] for p in over]))
    _box(s, 700000, 3900000, SW - 1400000, 2000000, [
        "The hot case is the second highest of the season's largest weekly shortfall over the ten summers %d to %d, each "
        "run on its recorded weekly temperatures." % (f["counts"]["summers"][0], f["counts"]["summers"][1])] + extra, size=14)
    _foot(s, 4, total)
    # 5: the routes
    s = prs.slides.add_slide(lay)
    _heading(s, "The usual sizing would have ordered the wrong fleets")
    rows = [["How the fleets are sized"] + [nm(p) for p in POOLS]]
    for key, label in ROUTES[:5]:
        rows.append([label] + ["%s, %s" % (k(f["routes"][key][p]["plan"]),
                                           {"buy": "buy", "hire": "hire", "nothing": "none"}[f["routes"][key][p]["cover"]]) for p in POOLS])
    _table(s, 480000, 1350000, SW - 960000, rows, [0.35, 0.13, 0.13, 0.13, 0.13, 0.13], size=12)
    rf = f["referee"]
    _box(s, 560000, 4250000, SW - 1120000, 1900000, [
        "Check on the tagged 20 litre kegs: from the December 2025 count to the busiest weeks of summer 2026 the tags show "
        "%s more kegs at customers. What a cellar holds line by line gives %s; stock moved in step with deliveries would "
        "have been %s." % (k(rf["seen"]), k(rf["golden"]), k(rf["proportional"])),
        "The cover is the same on all %s rebuilds with other conventions and when each fitted input is moved "
        "(Sensitivity sheet)." % k(f["variants"] - 1)], size=14)
    _foot(s, 5, total)
    prs.save(path)


def build(folder, f, scratch):
    os.makedirs(folder)
    os.makedirs(scratch, exist_ok=True)
    workbook(os.path.join(folder, FILES["wb"]), f)
    a, b = os.path.join(scratch, "cover.png"), os.path.join(scratch, "weeks.png")
    chart_cover(a, f)
    chart_weeks(b, f)
    deck(os.path.join(folder, FILES["deck"]), f, a, b)
    return a, b
