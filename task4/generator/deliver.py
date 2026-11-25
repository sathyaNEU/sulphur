"""The two golden files: the workbook the head of supply chain opens (the cover for each container type on its first
sheet, the fleet account second, the working behind them, and a routes sheet) and the slides for the order meeting.
Every number comes from figures.json."""
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
STEP = {"S1": "cellar checks as they stand", "S2": "store at 2026's weeks of cover", "S3": "no loss in the trade"}
ROUTES = [("golden", "This review"),
          ("S1", "Cellar checks read as what a line holds"),
          ("S2", "Cold store at summer 2026's weeks of cover"),
          ("S3", "Register less condemned read as the fleet (no loss in the trade)"),
          ("S1+S2", "First two together"), ("S1+S3", "First and third together"), ("S2+S3", "Second and third together"),
          ("S1+S2+S3", "All three together"),
          ("direct", "Every container on the register counted as fleet"),
          ("rigorous", "Checks and store regressed as they stand, no loss"),
          ("run calibrated", "Checks as they stand, scaled to the trade's stock the lots imply"),
          ("run cutoff", "Checks within four days of the dray, as they stand"),
          ("run generous", "A whole delivery added to each check, a whole run per beer, every missing container written off")]


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
        parts.append("hire %s for the season" % _short(by["hire"]))
    if by["nothing"]:
        parts.append("leave %s alone" % _short(by["nothing"]))
    s = ", ".join(parts)
    return s[0].upper() + s[1:] if cap else s


def rejected(f, key="S1+S2+S3"):
    r = f["routes"][key]
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
    for col, w in zip("ABCDEFGHIJKLMNOPQRSTU", ws_):
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


def _rows(ws, hdr, rows, top, fmts, height=46):
    for j, h in enumerate(hdr):
        ws.cell(row=top, column=1 + j, value=h)
    _hdr(ws, top, len(hdr), height)
    for i, r in enumerate(rows):
        for j, v in enumerate(r):
            ws.cell(row=top + 1 + i, column=1 + j, value=v)
        for cols, fmt in fmts:
            _num(ws, top + 1 + i, cols, fmt)
    return top + 1 + len(rows)


def first_sheet(wb, f):
    ws = wb.active
    ws.title = "Cover 2027"
    c = f["counts"]
    _title(ws, "Container fleets for summer 2027: " + headline(f, cap=False),
           "Fleet standard FS-04 issue 3, sections 2 to 4. Count of every site on %s. %s, %s." % (
               day(c["count_date"]), AUTHOR, DATED))
    ws["A3"] = ("Not what the records give read as they stand. Taking the reps' cellar checks as what a line holds, the cold "
                "store at summer 2026's weeks of cover and the register less the condemned as the fleet, the same files "
                "give %s. The Routes sheet sets each of those readings beside this review, alone and in pairs." % rejected(f))
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:G3")
    ws.row_dimensions[3].height = 48
    hdr = ["Container type", "Largest weekly shortfall, planning case (containers)", "Range on other conventions",
           "Hot case (containers)", "Week of the planning case's figure (week beginning)",
           "Maker's minimum order run (containers)", "Cover"]
    ws.append([])
    ws.append(hdr)
    _hdr(ws, 5, len(hdr), 60)
    for i, p in enumerate(POOLS):
        lo, hi = f["plan_band"][p]
        ws.append([f["names"][p].capitalize(), f["plan"][p], "%s to %s" % (k(lo), k(hi)), f["hot"][p],
                   dt.date.fromisoformat(f["plan_week"][p]), f["min_run"][p], COVER[f["cover"][p]]])
        row = 6 + i
        _num(ws, row, (2, 4, 6))
        ws.cell(row=row, column=5).number_format = "dd mmm yyyy"
        ws.cell(row=row, column=7).fill = PatternFill("solid", fgColor=FILL[f["cover"][p]])
        ws.cell(row=row, column=7).alignment = Alignment(horizontal="center")
        ws.cell(row=row, column=3).alignment = Alignment(horizontal="right")
    last = 5 + len(POOLS)
    notes = [
        "Cover is read on the planning case (FS-04 4.1): nil or negative, no cover; above nil and below the maker's minimum "
        "order run (quotation Q26-1187), a seasonal hire; the minimum order run or more, a purchase. A negative figure is a "
        "surplus (2.3). The hot case is reported beside it and does not change the cover.",
        "The season is the %d weeks beginning %s to %s (3.1). The planning case takes every week at the Calder Vale normal "
        "(3.2); the hot case is the second highest of the ten summers %s to %s, each run week by week on its own recorded "
        "temperatures (3.3)." % (len([x for x in f["path"]["K50"] if x["in_season"]]), day(f["season"][0]),
                                 day(f["season"][1]), min(f["summers"]["K50"]), max(f["summers"]["K50"])),
        "Nobody counts what is out in the trade or what has been lost there, so every line of this is an estimate: the "
        "Fleet account sheet gives the three estimates each figure stands on, and the range is the lowest and highest "
        "planning-case figure over %d rebuilds on other reasonable conventions (the cover is the same in every one)."
        % (f["variants"] - 1)]
    for i, t in enumerate(notes):
        _note(ws, last + 2 + i, t, 7, 40)
    _widths(ws, (17, 17, 17, 13, 17, 15, 15))
    ws.freeze_panes = "B6"
    ch = 5 + len(POOLS) + 2 + len(notes) + 2
    ws.cell(row=ch, column=1, value="Chart data").font = Font(bold=True, size=9, color="555555")
    ws.cell(row=ch + 1, column=1, value="Container type")
    ws.cell(row=ch + 1, column=2, value="Planning case")
    ws.cell(row=ch + 1, column=3, value="Minimum order run")
    for i, p in enumerate(POOLS):
        ws.cell(row=ch + 2 + i, column=1, value=f["plural"][p].capitalize())
        ws.cell(row=ch + 2 + i, column=2, value=f["plan"][p])
        ws.cell(row=ch + 2 + i, column=3, value=f["min_run"][p])
        _num(ws, ch + 2 + i, (2, 3))
    bar = BarChart()
    bar.type = "col"
    bar.title = "Largest weekly shortfall of summer 2027 against the maker's minimum order run"
    bar.y_axis.title = "Containers"
    bar.add_data(Reference(ws, min_col=2, max_col=3, min_row=ch + 1, max_row=ch + 1 + len(POOLS)), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=ch + 2, max_row=ch + 1 + len(POOLS)))
    bar.y_axis.number_format = "#,##0"
    bar.y_axis.delete = False
    bar.x_axis.delete = False
    bar.x_axis.tickLblPos = "low"
    for s, col in zip(bar.series, ("2A78D6", "8A8F98")):
        s.graphicalProperties.solidFill = col
        s.graphicalProperties.line.solidFill = col
    bar.gapWidth = 80
    bar.height, bar.width = 8.6, 19.5
    bar.legend.position = "b"
    ws.add_chart(bar, "A%d" % (ch + 9))
    ws.print_area = "A1:G%d" % (ch + 26)
    ws.page_setup.orientation = "landscape"


def account_sheet(wb, f):
    ws = wb.create_sheet("Fleet account")
    _title(ws, "Fleet account by container type for the 2027 summer season",
           "Count of every site on %s against the register; the trade's stock, the store and the loss each estimated."
           % day(f["counts"]["count_date"]))
    ws.append([])
    rows = []
    lines = [("On the register at the count (bought, not condemned)", "register"),
             ("Counted on Wrenfold's sites", "on_site"),
             ("Alive at the count (estimated from the lots on site)", "alive"),
             ("At customers at the count, alive", "in_trade_alive"),
             ("On the register and not coming back", "never_coming_back"),
             ("Lost in the trade in a year", "lost_year"),
             ("More held by the trade at its summer peak than at the count", "rise"),
             ("Full in the cold store at its fullest under the 2027 brew plan", "store_fullest"),
             ("Largest weekly shortfall, planning case", "plan"),
             ("Largest weekly shortfall, hot case", "hot")]
    hdr = ["Containers"] + [f["names"][p].capitalize() for p in POOLS] + ["All five"]
    whole = {"rise": f["trade_rise"], "store_fullest": f["store_2027"], "lost_year": f["year_loss"]}
    for label, key in lines:
        v = [f["account"][p][key] for p in POOLS]
        rows.append([label] + v + ([whole.get(key, sum(v))] if key not in ("plan", "hot") else [None]))
    end = _rows(ws, hdr, rows, 4, [(range(2, 8), "#,##0")])
    for r in (4 + 1 + 5, 4 + 1 + 6, 4 + 1 + 7):                  # the three estimates: lost, rise, store
        for col in range(1, 8):
            ws.cell(row=r, column=col).font = Font(bold=True)
    r = end + 1
    hdr2 = ["Rates and inputs"] + [f["names"][p].capitalize() for p in POOLS]
    rows2 = [["Share of the fleet leaving the trade a year (per cent)"] + [f["account"][p]["leaving_pct"] for p in POOLS],
             ["Share of the fleet alive on site at the count"] + [f["account"][p]["share_on_site"] for p in POOLS],
             ["Purchase lots on the register"] + [f["account"][p]["lots"] for p in POOLS],
             ["Condemned at the wash in the year to the count"] + [f["account"][p]["condemned_year"] for p in POOLS],
             ["Delivered in the year to the count"] + [f["account"][p]["deliveries_year"] for p in POOLS],
             ["Dispense lines supplied at the count"] + [f["account"][p]["lines"] for p in POOLS],
             ["Maplestead lines from April 2027"] + [f["account"][p]["estate_lines"] for p in POOLS]]
    _rows(ws, hdr2, rows2, r, [(range(2, 7), "#,##0")])
    for i in (0, 1):
        _num(ws, r + 1 + i, range(2, 7), "0.0" if i == 0 else "0.00")
    _note(ws, r + len(rows2) + 2,
          "The register keeps every container bought until the wash line condemns it, so it still carries every container "
          "lost in the trade since 2011. The trade's rise is from the count to its largest week of the season, the "
          "Maplestead cellars included; the store is at its largest week of the season. Each sheet behind this one gives "
          "the working.", 7, 44)
    _widths(ws, (58, 13, 13, 13, 13, 13, 13))
    ws.freeze_panes = "B5"


def path_sheet(wb, f):
    ws = wb.create_sheet("Weekly path")
    _title(ws, "Requirement, fleet and shortfall by week, planning case",
           "FS-04 2.1 to 2.3. Weeks from the count of %s to the end of the season; the fleet is the count's, with no "
           "purchase and no hire." % day(f["counts"]["count_date"]))
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
    ws = wb.create_sheet("Cellar checks")
    _title(ws, "What a dispense line holds, rebuilt from the reps' checks and the dockets",
           "TQ-02 checks of 2025 and 2026: full containers and the one on dispense, with the line's sales since the dray "
           "last called at the account added back.")
    ws.append([])
    hdr = ["Container type", "Line checks used", "Full and on dispense, mean per check", "Days since the dray, mean",
           "Sold since the dray, mean per check", "Held per line whatever it sells",
           "Held per container sold a week, weekly delivery", "Held per container sold a week, twice weekly",
           "Same, from the checks as they stand (weekly)", "Trade's stock per container delivered a week",
           "Rise to the summer peak"]
    rows = []
    for p in POOLS:
        d = f["pool"][p]
        rows.append([f["names"][p].capitalize(), d["checks"], d["mean_full"], d["mean_days"], d["mean_added_back"],
                     d["fixed_per_line"], d["per_sale_weekly"], d["per_sale_twice"], d["face_per_sale_weekly"],
                     d["trade_per_sale"], f["trade_rise_by_pool"][p]])
    end = _rows(ws, hdr, rows, 4, [((2, 11), "#,##0"), ((3, 5, 6, 7, 8, 9, 10), "0.00"), ((4,), "0.0")], 62)
    ws.cell(row=end, column=1, value="All five types").font = Font(bold=True)
    ws.cell(row=end, column=11, value=f["trade_rise"]).font = Font(bold=True)
    _num(ws, end, (11,))
    fs = f["falsification"]
    _note(ws, end + 2,
          "Check on the rebuild: across %s line checks, with each line's weekly sales and delivery interval held, the full "
          "containers counted fall by %.2f (standard error %.2f) for each container the line has sold since the dray last "
          "called, where the checks read as the whole holding would fall by none. The rise carries the fitted relation "
          "from the count's week to each 2027 week, the Maplestead lines added from their listing dates." % (
              k(fs["checks"]), fs["fall"], fs["se"]), 11, 46)
    _widths(ws, (16, 10, 12, 11, 12, 12, 13, 13, 13, 13, 12))
    ws.freeze_panes = "B5"


def lots_sheet(wb, f):
    ws = wb.create_sheet("Lots")
    _title(ws, "Containers found on site by purchase lot against the register",
           "Count of %s, tally by the lot stamped on the chime; register rows not condemned by the count." %
           day(f["counts"]["count_date"]))
    ws.append([])
    hdr = ["Container type", "Lot", "Age at the count (years)", "On the register", "Found on site", "Share found on site"]
    rows = []
    for p in POOLS:
        for x in f["lots"][p]:
            rows.append([f["names"][p].capitalize(), x["lot"], x["age"], x["register"], x["on_site"], x["share"]])
    end = _rows(ws, hdr, rows, 4, [((4, 5), "#,##0"), ((3,), "0.0"), ((6,), "0.000")])
    ws.auto_filter.ref = "A4:F%d" % (end - 1)
    r = end + 1
    hdr2 = ["Container type", "Leaving the trade a year (per cent)", "Share of the fleet on site", "Alive at the count",
            "Lost in the trade in a year"]
    rows2 = [[f["names"][p].capitalize(), f["account"][p]["leaving_pct"], f["account"][p]["share_on_site"],
              f["account"][p]["alive"], f["account"][p]["lost_year"]] for p in POOLS]
    end2 = _rows(ws, hdr2, rows2, r, [((4, 5), "#,##0"), ((2,), "0.0"), ((3,), "0.00")])
    ws.cell(row=end2, column=1, value="All five types").font = Font(bold=True)
    ws.cell(row=end2, column=5, value=f["year_loss"]).font = Font(bold=True)
    _num(ws, end2, (5,))
    _note(ws, end2 + 2, "Each lot's share on site falls with its age at one rate a year for its container type; the fit "
                        "weights each lot by the containers found. The fleet alive is each lot on the register times its "
                        "fitted survival.", 6, 34)
    _widths(ws, (16, 12, 12, 12, 12, 12))
    ws.freeze_panes = "C5"


def store_sheet(wb, f):
    ws = wb.create_sheet("Cold store")
    _title(ws, "The cold store under the 2027 brew plan",
           "Monday position against the racking log, December 2024 to November 2026; brew plan 2027 issue 1.")
    ws.append([])
    hdr = ["Container type", "Cover beside the runs (weeks of deliveries)", "Beers racked in 2025 and 2026",
           "Half a run per beer, 2026", "Beers on sale at the store's fullest, 2027", "Runs on sale then, 2027 plan",
           "Full in the cold store at its fullest", "Same on 2026's weeks of cover", "2026 stock over deliveries (weeks)"]
    rows = []
    for p in POOLS:
        d = f["pool"][p]
        rows.append([f["names"][p].capitalize(), d["store_cover_weeks"], d["beers_2026"], d["half_runs_2026"],
                     d["beers_at_fullest"], d["runs_on_sale_at_fullest"], f["store_2027_by_pool"][p],
                     d["store_cover_route"], d["cover_weeks_2026"]])
    end = _rows(ws, hdr, rows, 4, [((3, 4, 5, 6, 7, 8), "#,##0"), ((2,), "0.000"), ((9,), "0.00")], 62)
    ws.cell(row=end, column=1, value="All five types").font = Font(bold=True)
    ws.cell(row=end, column=7, value=f["store_2027"]).font = Font(bold=True)
    ws.cell(row=end, column=8, value=f["route_components"]["S2"]["C2"])
    _num(ws, end, (7, 8))
    r = end + 2
    hdr2 = ["Container type", "Product", "Racking run 2025 and 2026 (median filled)", "2027 plan period", "First on sale",
            "Last on sale", "2027 racking run"]
    rows2 = []
    for p in POOLS:
        for b in f["beers"][p]:
            rows2.append([f["names"][p].capitalize(), b["sku"], f["runs_2026"][p].get(b["sku"]), None,
                          dt.date.fromisoformat(b["first"]), dt.date.fromisoformat(b["last"]), b["run"]])
            rows2[-1][3] = "from 3 May" if b["first"] >= "2027-05-03" else "to 2 May"
    end2 = _rows(ws, hdr2, rows2, r, [((3, 7), "#,##0"), ((5, 6), "dd mmm yyyy")])
    _widths(ws, (16, 14, 14, 13, 14, 13, 13, 13, 13))
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
        ws.append([f["names"][p].capitalize()] + [f["summers"][p][y] for y in yrs] + [f["hot"][p], f["hot_year"][p],
                                                                                       f["plan"][p]])
        _num(ws, 5 + i, list(range(2, 12)) + [12, 14])
        j = yrs.index(str(f["hot_year"][p]))
        ws.cell(row=5 + i, column=2 + j).font = Font(bold=True)
    _widths(ws, (16,) + (9,) * 10 + (10, 12, 11))
    ws.freeze_panes = "B5"


def routes_sheet(wb, f):
    ws = wb.create_sheet("Routes")
    _title(ws, "What each shortcut would have ordered",
           "Largest weekly shortfall, planning case, and the cover it implies; then the three estimates on each route.")
    ws.append([])
    hdr = ["How the fleets are sized"]
    for p in POOLS:
        hdr += [f["names"][p].capitalize(), "Cover"]
    hdr += ["Trade's rise", "Store at its fullest", "Lost in a year"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 34)
    for i, (key, label) in enumerate(ROUTES):
        row = [label]
        for p in POOLS:
            row += [f["routes"][key][p]["plan"], COVER[f["routes"][key][p]["cover"]]]
        rc = f["route_components"].get(key) or ({"C1": f["trade_rise"], "C2": f["store_2027"], "C3": f["year_loss"]}
                                                if key == "golden" else {})
        row += [rc.get("C1"), rc.get("C2"), rc.get("C3")]
        ws.append(row)
        for j, p in enumerate(POOLS):
            _num(ws, 5 + i, (2 + 2 * j,))
            if f["routes"][key][p]["cover"] != f["cover"][p]:
                ws.cell(row=5 + i, column=3 + 2 * j).fill = PatternFill("solid", fgColor="F6D5D2")
        _num(ws, 5 + i, (12, 13, 14))
        if key == "golden":
            for col in range(1, len(hdr) + 1):
                ws.cell(row=5 + i, column=col).font = Font(bold=True)
    r = 5 + len(ROUTES) + 1
    _note(ws, r, "Shaded covers differ from this review's. The second to eighth rows leave out one, two or all three of "
                 "the estimates this review makes and take the records as they stand there instead; every other step is "
                 "this review's.", 14, 34)
    _widths(ws, (58, 10, 12, 10, 12, 10, 12, 10, 12, 10, 12, 11, 11, 11))
    ws.freeze_panes = "B5"


def notes_sheet(wb, f):
    ws = wb.create_sheet("Notes")
    c = f["counts"]
    _title(ws, "Sources and conventions")
    rows = [
        ("As of", "Count of every site on %s; records to that date." % day(c["count_date"])),
        ("Requirement, fleet, shortfall", "FS-04 issue 3, 2.1 to 2.3: at customers (full, on dispense, or empty and awaiting "
                                          "collection), full in the cold store, at the depots, in wash and repair, plus a "
                                          "float of two sevenths of the week's deliveries; the fleet with no purchase and no "
                                          "hire after the count."),
        ("Deliveries", "%s docket lines over %d weeks from %s; %s lines re-sent by a handheld counted once; %s lines with no "
                       "container code read from the product; %s renumbered accounts under their current number."
         % (k(c["delivery_lines"]), c["weeks"], day(c["first_week"]), k(c["resent_rows"]), k(c["blank_codes"]),
            k(c["renumbered"]))),
        ("Cellar checks", "%s TQ-02 line checks on %s calls; %s lines entered twice on one call taken once."
         % (k(c["checks"]), k(c["check_calls"]), k(c["check_doubles"]))),
        ("Forecast", "Weekly deliveries by type fitted on the season, the trend and the week's mean daily maximum "
                     "temperature at Calder Vale; the Maplestead outlets added from their listing dates at the scheduled "
                     "volume, shaped by the season."),
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
    account_sheet(wb, f)
    routes_sheet(wb, f)
    path_sheet(wb, f)
    cellars_sheet(wb, f)
    lots_sheet(wb, f)
    store_sheet(wb, f)
    summers_sheet(wb, f)
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
    total = 4
    prs = Presentation()
    prs.slide_width, prs.slide_height = Emu(SW), Emu(SH)
    lay = prs.slide_layouts[5]
    nm = lambda p: f["plural"][p].capitalize()
    # 1: the cover
    s = prs.slides.add_slide(lay)
    _heading(s, headline(f))
    s.shapes.add_picture(png_cover, Emu(560000), Emu(1250000), width=Emu(7200000))
    lines = ["Largest weekly shortfall of the 2027 season, planning case, against the maker's minimum order run:"]
    lines += ["%s: %s against %s, %s" % (nm(p), k(f["plan"][p]), k(f["min_run"][p]), COVER[f["cover"][p]].lower())
              for p in POOLS]
    _box(s, 7950000, 1300000, SW - 7950000 - 500000, 4800000, lines, size=14, bold_first=True)
    _foot(s, 1, total)
    # 2: the fleet account
    s = prs.slides.add_slide(lay)
    _heading(s, "Three estimates carry the order: the trade's summer stock, the store and the loss")
    rows = [["Containers"] + [nm(p) for p in POOLS] + ["All five"]]
    for label, key in (("On the register", "register"), ("Counted on site", "on_site"), ("Alive at the count", "alive"),
                       ("Lost in the trade in a year", "lost_year"), ("Trade's rise to its summer peak", "rise"),
                       ("Cold store at its fullest", "store_fullest")):
        v = [f["account"][p][key] for p in POOLS]
        tot = {"rise": f["trade_rise"], "store_fullest": f["store_2027"], "lost_year": f["year_loss"]}.get(key, sum(v))
        rows.append([label] + [k(x) for x in v] + [k(tot)])
    _table(s, 480000, 1350000, SW - 960000, rows, [0.28, 0.12, 0.12, 0.12, 0.12, 0.12, 0.12], size=13)
    _box(s, 560000, 4500000, SW - 1120000, 1700000, [
        "The register still holds every container lost in the trade since 2011: %s of its %s are not coming back. The reps' "
        "checks count only full containers, so the trade holds more than they show and rises by %s to its summer peak. The "
        "2027 brew plan's longer runs and wider range fill the store to %s." % (
            k(sum(f["account"][p]["never_coming_back"] for p in POOLS)), k(f["counts"]["register"]), k(f["trade_rise"]),
            k(f["store_2027"]))], size=14)
    _foot(s, 2, total)
    # 3: the weeks and the hot case
    s = prs.slides.add_slide(lay)
    _heading(s, "In a hot summer the 50 litre fleet is short by %s in its worst week" % k(f["hot"]["K50"]))
    s.shapes.add_picture(png_weeks, Emu(1096000), Emu(1150000), width=Emu(10000000))
    rows = [["Largest weekly shortfall", "Planning case", "Hot case", "Summer it comes from", "Cover"]]
    for p in POOLS:
        rows.append([nm(p), k(f["plan"][p]), k(f["hot"][p]), str(f["hot_year"][p]), COVER[f["cover"][p]]])
    _table(s, 700000, 3800000, SW - 1400000, rows, [0.28, 0.17, 0.17, 0.2, 0.18], size=12, row_h=300000)
    _box(s, 700000, 5720000, SW - 1400000, 500000, [
        "The hot case is the second highest of the ten summers %s to %s run week by week; the cover is read on the planning "
        "case (FS-04 4.1)." % (min(f["summers"]["K50"]), max(f["summers"]["K50"]))], size=12)
    _foot(s, 3, total)
    # 4: the routes
    s = prs.slides.add_slide(lay)
    _heading(s, "The records read as they stand would have ordered the wrong fleets")
    rows = [["How the fleets are sized"] + [nm(p) for p in POOLS]]
    for key, label in [ROUTES[0], ROUTES[1], ROUTES[2], ROUTES[3], ROUTES[7]]:
        rows.append([label] + ["%s, %s" % (k(f["routes"][key][p]["plan"]),
                                           {"buy": "buy", "hire": "hire", "nothing": "none"}[f["routes"][key][p]["cover"]])
                               for p in POOLS])
    _table(s, 480000, 1350000, SW - 960000, rows, [0.35, 0.13, 0.13, 0.13, 0.13, 0.13], size=12)
    _box(s, 560000, 4350000, SW - 1120000, 1800000, [
        "Each of the three readings alone files a wrong cover on at least one fleet, and together they order nothing for "
        "the 50 and 20 litre kegs or the firkins and only a hire of 30 litre kegs. The cover holds on all %d rebuilds with other reasonable conventions and with each fitted input "
        "moved by twice its measured spread (workbook, Routes sheet)." % (f["variants"] - 1)], size=14)
    _foot(s, 4, total)
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
