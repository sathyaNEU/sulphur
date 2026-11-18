"""The two golden files: the workbook the head of population statistics sends the Posting Board's secretary (the
establishment on its first sheet, the working behind it) and each district's population account by year as a CSV.
Every number comes from figures.json."""
import csv
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import world as WL

FILES = {"wb": "orlava_consular_staffing_estimate_2027.xlsx", "csv": "orlava_citizens_abroad_account_2011_2027.csv"}
HOSTS = WL.HOSTS
HEAD = PatternFill("solid", fgColor="24405A")
UP, DOWN, OFF = PatternFill("solid", fgColor="D6E8F7"), PatternFill("solid", fgColor="F6E3C8"), PatternFill("solid", fgColor="F3D6D2")
THIN = Side(style="thin", color="B8BEC8")
WORD = {0: "no", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven"}
ROUTES = ["S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3", "direct", "mirror", "rigorous", "mean"]
LABEL = {
    "S1": "Each host's arrivals table taken as the arrivals; the rest as estimated",
    "S2": "Each host's departures table taken as the exits; the rest as estimated",
    "S3": "2021 to 2023 carried through 2024 to 2026; the rest as estimated",
    "S1+S2": "The hosts' tables at face value to 2023, 2024 to 2026 from Orlava's register",
    "S1+S3": "Arrivals as tabled, exits from the census pair, 2021 to 2023 carried forward",
    "S2+S3": "Arrivals corrected, departures as tabled, 2021 to 2023 carried forward",
    "S1+S2+S3": "The hosts' tables at face value from the 2021 census, 2021 to 2023 carried forward",
    "direct": "The 2021 census count and the host's own tables to 1 January 2024, taken as the latest figure",
    "mirror": "The larger of the two reports of every flow, 2021 to 2023 repeated",
    "rigorous": "Recording shares scaled so the fullest recorder is complete",
    "mean": "Recording shares scaled to a geometric mean of one",
}


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _hdr(ws, row, n, height=44):
    for c in ws[row][:n]:
        c.font = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = Border(bottom=THIN)
    ws.row_dimensions[row].height = height


def _widths(ws, widths):
    for k, w in enumerate(widths):
        ws.column_dimensions[chr(65 + k) if k < 26 else "A" + chr(65 + k - 26)].width = w


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


def changes(f):
    up = ["%s more in %s" % (WORD[f["officers_change"][h]], h) for h in HOSTS if f["officers_change"][h] > 0]
    down = ["%s fewer in %s" % (WORD[-f["officers_change"][h]], h) for h in HOSTS if f["officers_change"][h] < 0]
    return up, down


def headline(f):
    up, down = changes(f)
    return "%d consular officers for 2027 to 2029 against %d in force: %s; %s" % (
        f["officers_total"][1], f["officers_total"][0], ", ".join(up), ", ".join(down))


def first_sheet(wb, f):
    ws = wb.active
    ws.title = "Establishment 2027-2029"
    st = f["stated"]
    _title(ws, headline(f),
           "Order No. %d of %d, clauses 2.1 and 4.1. Orlavan citizens usually resident on 1 January 2027, estimated. "
           "%s, Population Statistics, 25 February 2027." % (st["order_no"], st["order_year"], WL.PEOPLE["analyst"]))
    r = f["routes"]["S1+S2+S3"]
    ws["A3"] = ("This is not the establishment the partner states' tables give when each state's arrivals and departures "
                "tables are taken as the moves and 2021 to 2023 are carried through 2024 to 2026: that files %s (%d "
                "officers). The Routes sheet sets that reading and each of its three choices beside the estimate." % (
                    _list("%s %d" % (h, r["officers"][h]) for h in HOSTS), sum(r["officers"].values())))
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:I3")
    ws.row_dimensions[3].height = 44
    hdr = ["District", "Consulate general", "Citizens at the census of 1 January 2021",
           "Citizens usually resident on 1 January 2027 (estimate)", "Officers in force", "Officers the Order gives",
           "Change", "Citizens who moved away, 2021 census to end 2026", "Citizens above the last %s line" % format(f["rate"], ",")]
    ws.append([])
    ws.append(hdr)
    _hdr(ws, 5, len(hdr), 58)
    for i, h in enumerate(HOSTS):
        n = f["citizens"][h]
        ws.append([h, WL.SEAT[h], f["census_2021"][h], n, f["officers_in_force"][h], f["officers"][h],
                   f["officers_change"][h], f["left"][h], n - f["rate"] * (f["officers"][h] - 1)])
        row = 6 + i
        for col in (3, 4, 8, 9):
            ws.cell(row=row, column=col).number_format = "#,##0"
        ws.cell(row=row, column=7).number_format = "+0;-0;0"
        for col in (5, 6, 7):
            ws.cell(row=row, column=col).alignment = Alignment(horizontal="center")
        if f["officers_change"][h]:
            ws.cell(row=row, column=6).fill = UP if f["officers_change"][h] > 0 else DOWN
    last = 5 + len(HOSTS)
    ws.append(["All districts", "", sum(f["census_2021"].values()), sum(f["citizens"].values()), f["officers_total"][0],
               f["officers_total"][1], f["officers_total"][1] - f["officers_total"][0], sum(f["left"].values()), None])
    for c in ws[last + 1][:9]:
        c.font = Font(bold=True)
        c.border = Border(top=THIN)
    for col in (3, 4, 8):
        ws.cell(row=last + 1, column=col).number_format = "#,##0"
    ws.cell(row=last + 1, column=7).number_format = "+0;-0;0"
    for col in (5, 6, 7):
        ws.cell(row=last + 1, column=col).alignment = Alignment(horizontal="center")
    n = f["counts"]
    notes = [
        "One officer for every %s citizens or part of %s usually resident in the district on 1 January 2027 (Order, clause "
        "2.1). Usual residence and citizenship as in Regulation %d/%d, article 2." % (
            format(f["rate"], ","), format(f["rate"], ","), st["regulation_no"][0], st["regulation_no"][1]),
        "No state has counted its Orlavan citizens since the censuses of 1 January 2021 and the partner states' migration "
        "tables end with %d, so each figure is an estimate: the 2021 census count carried forward by the arrivals, exits, "
        "births and deaths of the Account sheet. Whole persons; a total is the sum of the rounded rows." % n["years_tables"][1],
        "Moved away (clause 4.1): citizens who ceased to be usually resident in the district from 1 January 2021 to 31 "
        "December 2026, whatever state they moved to.",
    ]
    for i, t in enumerate(notes):
        _note(ws, last + 3 + i, t, 9, 28)
    _widths(ws, (14, 17, 14, 17, 10, 11, 9, 17, 14))
    ws.freeze_panes = "B6"
    up = [h for h in HOSTS if f["officers_change"][h] > 0]
    down = [h for h in HOSTS if f["officers_change"][h] < 0]
    bar = BarChart()
    bar.type = "col"
    bar.title = "%s have crossed into a higher band of %s since the 2021 census; %s have dropped one" % (
        _list(up), format(f["rate"], ","), _list(down))
    bar.y_axis.title = "Orlavan citizens usually resident"
    bar.add_data(Reference(ws, min_col=3, max_col=4, min_row=5, max_row=last), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=6, max_row=last))
    bar.y_axis.scaling.min = 0
    bar.y_axis.scaling.max = f["rate"] * (max(max(f["citizens"].values()), max(f["census_2021"].values())) // f["rate"] + 1)
    bar.y_axis.majorUnit = f["rate"]
    bar.y_axis.number_format = "#,##0"
    bar.y_axis.delete = False
    bar.x_axis.delete = False
    bar.gapWidth = 60
    bar.overlap = -8
    bar.series[0].graphicalProperties.solidFill = "B56D12"
    bar.series[1].graphicalProperties.solidFill = "2374B8"
    for s in bar.series:
        s.graphicalProperties.line.noFill = True
    bar.height, bar.width = 9.2, 19.5
    bar.legend.position = "b"
    ws.add_chart(bar, "A%d" % (last + 7))
    ws.print_area = "A1:I%d" % (last + 27)


def account_sheet(wb, f):
    ws = wb.create_sheet("Account")
    n = f["counts"]
    _title(ws, "Each district's Orlavan citizens by year: the census counts and the estimated arrivals, exits and births less deaths",
           "Citizens on 1 January and the events of the year. Counts of 1 January 2011 and 2021 are the censuses; arrivals "
           "and exits to %d rest on the partner state's tables, after it on Orlava's register." % n["years_tables"][1])
    ws.append([])
    hdr = ["District", "Year", "Citizens on 1 January", "Arrivals in the year", "Exits in the year", "Births less deaths in the year"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 40)
    r = 5
    for h in HOSTS:
        for a in f["account"][h]:
            ws.append([h, a["year"], a["citizens_1_january"], a["arrivals"], a["exits"], a["births_less_deaths"]])
            for col in (3, 4, 5, 6):
                ws.cell(row=r, column=col).number_format = "#,##0"
            if a["year"] in (2011, 2021):
                ws.cell(row=r, column=3).font = Font(bold=True)
            r += 1
    ws.auto_filter.ref = "A4:F%d" % (r - 1)
    _note(ws, r + 1, "Births less deaths after %d are each district's 2021 to %d rate (per 1,000 citizens a year: %s) on "
                     "the citizens at the start of the year." % (
                         n["years_tables"][1], n["years_tables"][1],
                         _list("%s %.2f" % (h, f["natural_rate_per_1000"][h]) for h in HOSTS)), 6, 40)
    _widths(ws, (14, 8, 14, 14, 12, 14))
    ws.freeze_panes = "C5"


def shares_sheet(wb, f):
    ws = wb.create_sheet("Recording shares")
    st, n = f["stated"], f["counts"]
    _title(ws, "What each table holds of the moves it reports",
           "Orlava's register recorded %.1f per cent of the citizens of the seven states who arrived in 2020: %s "
           "registrations against %s counted by census table %s as abroad on 1 January 2020." % (
               f["share_home_arrivals_pct"], format(f["register_arrivals_2020_total"], ","),
               format(f["census_table_abroad_total"], ","), st["c14"]))
    ws.append([])
    hdr = ["State", "Its own emigrants to Orlava it recorded (Table B)", "Arrivals of other states' citizens it recorded (Table A)",
           "Orlavan citizens' exits its departures table holds (Table C), census 2011 to census 2021",
           "Orlavan citizens who left between the two censuses", "Orlava's register: share of the citizens who moved there, 2011 to %d" % n["years_tables"][1],
           "Orlava's register: share of the citizens who left it, 2011 to %d" % n["years_tables"][1],
           "Exits 2024 to 2026 over exits 2021 to 2023"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 74)
    for i, h in enumerate(HOSTS):
        ws.append([h, f["share_partner_emigrants_pct"][h] / 100.0, f["share_host_arrivals_pct"][h] / 100.0,
                   f["share_host_departures_pct"][h] / 100.0, f["exits_decade"][h], f["share_home_moves_pct"][h] / 100.0,
                   f["share_home_exits_pct"][h] / 100.0, f["late_ratio"][h]])
        for col in (2, 3, 4, 6, 7):
            ws.cell(row=5 + i, column=col).number_format = "0.0%"
        ws.cell(row=5 + i, column=5).number_format = "#,##0"
        ws.cell(row=5 + i, column=8).number_format = "0.00"
    r = 5 + len(HOSTS) + 1
    _note(ws, r, "Of the Orlavan citizens who moved to the seven states in 2011 to %d, %.1f per cent deregistered in Orlava. "
                 "A share above 100 per cent is a table that holds more arrivals than took place (stays that did not "
                 "last twelve months)." % (n["years_tables"][1], f["c1"]), 8, 30)
    _widths(ws, (12, 15, 15, 17, 14, 17, 15, 12))
    ws.freeze_panes = "B5"


def check_sheet(wb, f):
    ws = wb.create_sheet("Checks")
    rf = f["referee"]
    _title(ws, "Fenmark counted %s Orlavan citizens on 1 January 2016; the estimate's route gives %s" % (
        format(rf["count"], ","), format(rf["golden"], ",")),
        "Fenmark's 2011 census count carried five years. The count of 2016 is used nowhere in the estimate.")
    ws.append([])
    hdr = ["Route from the 2011 census to 1 January 2016", "Citizens", "Off the count"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 30)
    rows = [["The estimate's route", rf["golden"], rf["off"]]]
    names = {"the host's tables at face value": "Fenmark's tables at face value",
             "the larger report of each flow": "The larger of the two reports of every flow",
             "shares scaled to the fullest recorder": "Recording shares scaled so the fullest recorder is complete",
             "arrivals as recorded, the account closed on departures": "Arrivals as tabled, departures scaled to close 2011 to 2021",
             "shares scaled about their own average": "Recording shares scaled to a geometric mean of one"}
    for k, v in rf["rivals"].items():
        rows.append([names[k], v["value"], v["off"]])
    own = f["closure"]["fits"]["unweighted, both"]
    rows.append(["Fenmark's two shares fitted on its own census accounts of seven citizenships", own["referee_value"], own["referee_off"]])
    for i, row in enumerate(rows):
        ws.append(row)
        for col in (2, 3):
            ws.cell(row=5 + i, column=col).number_format = "#,##0"
    r = 5 + len(rows) + 1
    ws.cell(row=r, column=1, value="Arrivals of 2021 to 2023, held out").font = Font(bold=True)
    hdr = ["District", "From the partner state's table, corrected", "From Orlava's register at its 2011 to 2020 share",
           "2018 to 2020 carried"]
    for k, v in enumerate(hdr):
        ws.cell(row=r + 1, column=k + 1, value=v)
    _hdr(ws, r + 1, len(hdr), 44)
    for i, h in enumerate(HOSTS):
        x = f["held_out"][h]
        for k, v in enumerate([h, x["arrivals"], x["register_scaled"], x["carried"]]):
            c = ws.cell(row=r + 2 + i, column=k + 1, value=v)
            if k:
                c.number_format = "#,##0"
    _widths(ws, (52, 20, 22, 14))


def sensitivity_sheet(wb, f):
    ws = wb.create_sheet("Sensitivity")
    nv = f["nearest_variant"]
    _title(ws, "Every rebuild of the estimate files the same officers; the nearest any district comes to a %s line is %s citizens" % (
        format(f["rate"], ","), format(nv["distance"], ",")),
        "%d rebuilds of the route (other windows, other averages, one home share for all districts, and pairs of these) "
        "and each fitted share moved by its own spread." % f["variants"])
    ws.append([])
    hdr = ["Citizens on 1 January 2027"] + list(HOSTS) + ["Officers"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 30)
    rows = [["The estimate"] + [f["citizens"][h] for h in HOSTS] + ["as filed"],
            ["Lowest rebuild"] + [f["variant_range"][h][0] for h in HOSTS] + ["same"],
            ["Highest rebuild"] + [f["variant_range"][h][1] for h in HOSTS] + ["same"]]
    for p in f["perturbations"]:
        rows.append([p["input"][0].upper() + p["input"][1:]] + [p["citizens"][h] for h in HOSTS] + ["same" if p["call_holds"] else "moves"])
    for i, row in enumerate(rows):
        ws.append(row)
        for col in range(2, 9):
            ws.cell(row=5 + i, column=col).number_format = "#,##0"
    r = 5 + len(rows) + 1
    sp = f["spreads_pct"]
    _note(ws, r, "A share's spread is the furthest any rebuild moves that host's own share from the estimate's value; across the hosts, an arrival share "
                 "%s per cent, a departure share %s, the home register's share of moves %s and of exits %s." % tuple(
                     "%.1f to %.1f" % (min(sp[h][k] for h in HOSTS), max(sp[h][k] for h in HOSTS))
                     for k in ("x_a", "x_d", "x_b", "x_r")), 9, 30)
    _widths(ws, (50, 11, 11, 11, 11, 11, 11, 11, 10))
    ws.freeze_panes = "B5"


def routes_sheet(wb, f):
    ws = wb.create_sheet("Routes")
    _title(ws, "What each shorter route files, beside the estimate",
           "Citizens on 1 January 2027 and the officers clause 2.1 gives on them. Shaded: officers that differ from the estimate's.")
    ws.append([])
    hdr = ["Route"] + ["%s, citizens" % h for h in HOSTS] + ["%s, officers" % h for h in HOSTS] + ["All officers"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 44)
    rows = [("The estimate", f["citizens"], f["officers"])] + [(LABEL[k], f["routes"][k]["citizens"], f["routes"][k]["officers"]) for k in ROUTES]
    for i, (name, cit, off) in enumerate(rows):
        ws.append([name] + [cit[h] for h in HOSTS] + [off[h] for h in HOSTS] + [sum(off.values())])
        for j, h in enumerate(HOSTS):
            ws.cell(row=5 + i, column=2 + j).number_format = "#,##0"
            c = ws.cell(row=5 + i, column=9 + j)
            c.alignment = Alignment(horizontal="center")
            if off[h] != f["officers"][h]:
                c.fill = OFF
        ws.cell(row=5 + i, column=16).alignment = Alignment(horizontal="center")
    for c in ws[5][:16]:
        c.font = Font(bold=True)
    _widths(ws, (62,) + (10,) * 7 + (9,) * 7 + (9,))
    ws.freeze_panes = "B5"


def build(folder, f):
    os.makedirs(folder, exist_ok=True)
    wb = Workbook()
    first_sheet(wb, f)
    account_sheet(wb, f)
    shares_sheet(wb, f)
    check_sheet(wb, f)
    sensitivity_sheet(wb, f)
    routes_sheet(wb, f)
    wb.save(os.path.join(folder, FILES["wb"]))
    with open(os.path.join(folder, FILES["csv"]), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["district", "year", "citizens_1_january", "arrivals", "exits", "births_less_deaths"])
        for h in HOSTS:
            for a in f["account"][h]:
                w.writerow([h, a["year"], a["citizens_1_january"]] + ["" if a[k] is None else a[k]
                                                                     for k in ("arrivals", "exits", "births_less_deaths")])
