"""The two golden files: the workbook the head of financial planning opens (the bands on its first sheet, the
working behind it) and the channel figures as a CSV. Every number comes from figures.json."""
import csv
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

FILES = {"wb": "paid_channels_2027.xlsx", "csv": "paid_channels_2027.csv"}
FILL = {"scale": "D7EAD3", "hold": "FBEBC8", "cut": "F3D3CF"}
HEAD = PatternFill("solid", fgColor="22364F")
THIN = Side(style="thin", color="B8BEC8")
LOST = {"S1": "Records trued up to the stores period by period", "S2": "Every postback at the named installs' value",
        "S3": "Response fitted on weekly spend", "S1+S2+S3": "All three together",
        "direct": "Records as they stand, named revenue only, last year's return"}
ROUTES = ["golden", "S1", "S2", "S3", "S1+S2+S3", "direct"]
COLS = [("return_plan", "Return at plan spend (EUR per EUR)", "0.000"),
        ("return_stretch", "Return at stretch spend (EUR per EUR)", "0.000"),
        ("installs_week", "Installs a week at plan spend", "#,##0"),
        ("value_plan", "12-month net revenue per install at plan spend (EUR)", "0.00"),
        ("next_euro", "Return on one more euro at plan spend (EUR)", "0.000"),
        ("next_euro_stretch", "Return on one more euro at stretch spend (EUR)", "0.000"),
        ("paid_per_install", "12-month net revenue per install, installs of 4 Nov 2024 to 2 Nov 2025 (EUR)", "0.00")]
CSV_COLS = ["channel", "band", "return_plan_spend", "return_stretch_spend", "installs_per_week_plan_spend",
            "net_revenue_12m_per_install_plan_spend_eur", "return_next_euro_plan_spend", "return_next_euro_stretch_spend",
            "net_revenue_12m_per_install_installs_2024-11-04_to_2025-11-02_eur"]
CSV_FMT = {"return_plan": "%.3f", "return_stretch": "%.3f", "installs_week": "%d", "value_plan": "%.2f",
           "next_euro": "%.3f", "next_euro_stretch": "%.3f", "paid_per_install": "%.2f"}


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def order(f):
    """the plan's channels, highest return at the plan's spend first"""
    return sorted(f["return_plan"], key=lambda c: (-f["return_plan"][c], -f["value_plan"][c]))


def _hdr(ws, row, n, height=44):
    for c in ws[row][:n]:
        c.font = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = Border(bottom=THIN)
    ws.row_dimensions[row].height = height


def _widths(ws, ws_):
    for i, w in enumerate(ws_):
        ws.column_dimensions[ws.cell(row=1, column=1 + i).column_letter].width = w
    ws.page_setup.orientation = "landscape"                        # a sheet prints one page wide, on A4
    ws.page_setup.paperSize = 9
    ws.sheet_properties.pageSetUpPr.fitToPage = True
    ws.page_setup.fitToWidth, ws.page_setup.fitToHeight = 1, 0


def _title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12, name="Calibri")
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, size=9, color="555555", name="Calibri")


def _note(ws, row, text, cols, height=30):
    c = ws.cell(row=row, column=1, value=text)
    c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=row, start_column=1, end_row=row, end_column=cols)
    ws.row_dimensions[row].height = height


def first_sheet(wb, f, chans):
    ws = wb.active
    ws.title = "Bands 2027"
    b = f["by_band"]
    lo, hi = f["policy"]["lines"]
    _title(ws, "2027 media plan: scale %s, hold %s, cut %s" % (_list(b["scale"]), _list(b["hold"]), _list(b["cut"])),
           "Growth policy v3, section 3. Return = 12-month net revenue per euro of spend at the plan's weekly spend. "
           "Records to 8 November 2026. E. Rey, growth analytics.")
    r = f["routes"]["S1+S2+S3"]
    ws["A3"] = ("Not the reading the raw reconciliation gives: with the billing records trued up to the stores period by "
                "period, every postback valued like the installs the export names and the response fitted on weekly "
                "spend, Meta iOS would scale (%.3f) and Google Android (%.3f) and AppLovin Android (%.3f) would be cut. "
                "The Routes sheet sets each of those choices beside the estimate." % (
                    r["Meta iOS"]["return_plan"], r["Google Android"]["return_plan"], r["AppLovin Android"]["return_plan"]))
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:L3")
    ws.row_dimensions[3].height = 46
    hdr = ["Channel", "Band"] + [h for _k, h, _n in COLS] + ["Plan weekly spend, average (EUR)", "Hold from %.2f" % lo,
                                                               "Scale from %.2f" % hi]
    ws.append([])
    ws.append(hdr)
    _hdr(ws, 5, len(hdr), 58)
    for i, c in enumerate(chans):
        ws.append([c, f["bands"][c].capitalize()] + [f[k][c] for k, _h, _n in COLS] +
                  [f["channels"][c]["plan_weekly_spend"], lo, hi])
        row = 6 + i
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=FILL[f["bands"][c]])
        ws.cell(row=row, column=2).alignment = Alignment(horizontal="center")
        for j, (_k, _h, nf) in enumerate(COLS):
            ws.cell(row=row, column=3 + j).number_format = nf
        ws.cell(row=row, column=3 + len(COLS)).number_format = "#,##0"
        for k in (4 + len(COLS), 5 + len(COLS)):
            ws.cell(row=row, column=k).number_format = "0.00"
    last = 5 + len(chans)
    notes = ["Bands: scale from %.2f, hold from %.2f, cut under %.2f (policy 3.1). Apple Search Ads is on the brand "
             "sheet of the plan and is not placed." % (hi, lo, lo),
             "Installs are first installs of consumer accounts (policy 2.2); the iOS networks' installs are counted "
             "from their install postbacks.",
             "Net revenue is after VAT by storefront, the stores' %d per cent and the checkout's %d per cent "
             "(policy 2.4), on every charge made in the %d days from the install." % (
                 f["policy"]["commission_pct"], f["policy"]["fee_pct"], f["steps"]["days"]),
             "One more euro raises every week in the same proportion, on top of the plan's spend and on top of the "
             "stretch spend (policy 2.6). The Ranges sheet gives each figure's range across the other ways the three "
             "estimates could be taken."]
    for i, t in enumerate(notes):
        ws.cell(row=last + 2 + i, column=1, value=t).font = Font(size=9, color="444444", name="Calibri")
    _widths(ws, (22, 9, 13, 13, 11, 17, 14, 14, 21, 14, 8, 8))
    ws.freeze_panes = "B6"
    bar = BarChart()
    bar.type = "col"
    bar.title = "%s clear %.2f at the plan's spend; %s stay under %.2f" % (_list(b["scale"]), hi, _list(b["cut"]), lo)
    bar.y_axis.title = "EUR of 12-month net revenue per EUR of spend"
    bar.add_data(Reference(ws, min_col=3, max_col=4, min_row=5, max_row=last), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=6, max_row=last))
    bar.y_axis.scaling.min = 0
    bar.y_axis.number_format = "0.00"
    bar.y_axis.delete = False
    bar.x_axis.delete = False
    bar.series[0].graphicalProperties.solidFill = "2A78D6"          # plan spend
    bar.series[1].graphicalProperties.solidFill = "EB6834"          # stretch spend
    line = LineChart()
    line.add_data(Reference(ws, min_col=4 + len(COLS), max_col=5 + len(COLS), min_row=5, max_row=last), titles_from_data=True)
    line.series[0].graphicalProperties.line.solidFill = "52514E"    # the two lines in neutral ink, told apart by
    line.series[1].graphicalProperties.line.solidFill = "52514E"    # their dash and named with their values
    line.series[0].graphicalProperties.line.dashStyle = "dash"
    for s in line.series:
        s.graphicalProperties.line.width = 19050
        s.marker.symbol = "none"
        s.smooth = False
    bar += line
    bar.height, bar.width = 8.6, 21.5
    bar.legend.position = "b"
    ws.add_chart(bar, "A%d" % (last + 8))
    ws.print_area = "A1:L%d" % (last + 26)


def unrecorded_sheet(wb, f, all_ch):
    ws = wb.create_sheet("Unrecorded charges")
    s = f["steps"]
    _title(ws, "Store charges the billing records never took in, installs of 4 Nov 2024 to 2 Nov 2025",
           "Stores' daily reports against the billing events, by %s-day period from 4 Nov 2024 (App Store on Pacific days)."
           % f["policy"]["cadence_days"])
    ws.append([])
    hdr = ["Channel", "Installs bought", "Recorded 12-month net revenue per install (EUR)",
           "12-month net revenue per install (EUR)", "Not in the records",
           "If each recorded charge were scaled by its store's ratio for the period (EUR)"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr))
    for i, c in enumerate(all_ch):
        x = f["channels"][c]
        ws.append([c, x["installs_mature"], x["recorded_per_install"], x["paid_per_install"], x["unrecorded_pct"] / 100.0,
                   x["true_up_per_install"]])
        ws.cell(row=5 + i, column=2).number_format = "#,##0"
        for k in (3, 4, 6):
            ws.cell(row=5 + i, column=k).number_format = "0.00"
        ws.cell(row=5 + i, column=5).number_format = "0.0%"
    r0 = 5 + len(all_ch) + 1
    ws.cell(row=r0, column=1, value="Fitted to the stores' excess").font = Font(bold=True)
    hdr2 = ["Store", "First monthly charges: report less records", "Trials last seen unconverted on a monthly plan",
            "Share of them charged", "Annual first charges: report less records",
            "Trials last seen unconverted on an annual plan", "Share of them charged",
            "Renewals: report less records", "Subscriptions last seen set to renew, next charge after the last open",
            "Monthly continuation once the app is not opened"]
    for k, h in enumerate(hdr2):
        ws.cell(row=r0 + 1, column=1 + k, value=h)
    _hdr(ws, r0 + 1, len(hdr2), 70)
    for i, (name, st) in enumerate(f["stores"].items()):
        vals = [name, st["first_excess"], st["trial_candidates_monthly"], st["trial_end_share_monthly"], st["annual_excess"],
                st["trial_candidates_annual"], st["trial_end_share_annual"], st["renewal_excess"], st["renewal_candidates"],
                st["continuation"]]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r0 + 2 + i, column=1 + k, value=v)
            cell.number_format = "0.000" if k in (3, 6, 9) else ("#,##0" if k else "General")
    r1 = r0 + 5
    ws.cell(row=r1, column=1, value="Renewals beyond the records that each monthly continuation takes in "
                                    "(complete periods)").font = Font(bold=True)
    hdr3 = ["Store", "Renewals: report less records", "Fitted continuation", "takes in", "average miss a period",
            "Continuation of the web checkout's subscribers after their last open", "takes in", "average miss a period",
            "One less the cancellations the app saw per charge on file", "takes in", "average miss a period"]
    for k, h in enumerate(hdr3):
        ws.cell(row=r1 + 1, column=1 + k, value=h)
    _hdr(ws, r1 + 1, len(hdr3), 70)
    for i, (name, st) in enumerate(f["stores"].items()):
        rv = st["rivals"]
        vals = [name, st["renewal_excess_fitted_periods"]]
        for k in ("fitted", "web", "seen"):
            vals += [rv[k]["rate"], rv[k]["takes_in"], rv[k]["period_error"]]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r1 + 2 + i, column=1 + k, value=v)
            cell.number_format = "0.000" if k in (2, 5, 8) else ("#,##0" if k else "General")
    r2 = r1 + 5
    w = f["check_web"]
    _note(ws, r2, "Check on the web checkout (every charge on file): the %d monthly web subscribers among AppLovin "
                  "Android's installs of the year to 2 November 2025 who had been charged by their last open and were "
                  "last seen set to renew were charged EUR %.2f each after that open inside twelve months. The same fit, "
                  "run on the months those charges fell in, gives a continuation of %.3f and puts EUR %.2f there; scaling "
                  "the recorded charges by the stores' ratio for the period puts EUR %.2f." % (
                      w["subscribers"], w["charged"], w["web_rate"], w["estimate"], w["true_up"]), 10, 48)
    r3 = r2 + 2
    hdr4 = ["Period from", "Google Play renewals: report less records", "fitted", "App Store renewals: report less records",
            "fitted", "Google Play first charges: report less records", "App Store first charges: report less records"]
    for k, h in enumerate(hdr4):
        ws.cell(row=r3, column=1 + k, value=h)
    _hdr(ws, r3, len(hdr4), 58)
    gp, ap = f["stores"]["Google Play"]["periods"], f["stores"]["App Store"]["periods"]
    for i, d in enumerate(f["period_starts"]):
        vals = [d, gp[i]["renewals"], gp[i]["fitted"], ap[i]["renewals"], ap[i]["fitted"], gp[i]["first"], ap[i]["first"]]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r3 + 1 + i, column=1 + k, value=v)
            if k:
                cell.number_format = "#,##0"
    ws.cell(row=r3 + 1 + len(f["period_starts"]), column=1,
            value="The last period runs to the pull and is left out of the fit.").font = Font(size=9, color="444444")
    _widths(ws, (22, 16, 18, 16, 16, 20, 14, 16, 20, 16, 14))
    ws.freeze_panes = "B5"


def unnamed_sheet(wb, f, gated):
    ws = wb.create_sheet("Unnamed installs")
    R = f["ratios"]
    u = R["pool"]
    _title(ws, "iOS networks: installs the attribution export does not name, installs of 4 Nov 2024 to 2 Nov 2025",
           "Postbacks by market, week and first-48-hour value less the named installs; one ratio per source, fitted so the "
           "accounts with no channel add up to what they paid in each market and week.")
    ws.append([])
    hdr = ["Source", "Installs (postbacks)", "Named in the export", "Share named",
           "Named installs, 12-month net revenue each (EUR)", "Unnamed over named at the same first-48-hour value",
           "standard error", "Unnamed installs, 12-month net revenue each (EUR)", "All installs (EUR)",
           "If every postback were valued like the named installs (EUR)", "With Apple Search Ads' ratio (EUR)"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 70)
    for i, c in enumerate(gated):
        x, q = f["channels"][c], R["sources"][c]
        ws.append([c, x["installs_mature"], x["named_mature"], x["named_pct"] / 100.0, x["named_value"], q["ratio"], q["se"],
                   x["declined_value"], x["paid_per_install"], x["named_price_per_install"],
                   x["search_ads_ratio_per_install"]])
        for k in (2, 3):
            ws.cell(row=5 + i, column=k).number_format = "#,##0"
        ws.cell(row=5 + i, column=4).number_format = "0.0%"
        for k in (6, 7):
            ws.cell(row=5 + i, column=k).number_format = "0.000"
        for k in (5, 8, 9, 10, 11):
            ws.cell(row=5 + i, column=k).number_format = "0.00"
    ro = 5 + len(gated)
    q = R["sources"]["organic iOS"]
    ws.cell(row=ro, column=1, value="Organic (the accounts left over)")
    ws.cell(row=ro, column=2, value=q["declined"] + q["named"]).number_format = "#,##0"
    ws.cell(row=ro, column=3, value=q["named"]).number_format = "#,##0"
    ws.cell(row=ro, column=6, value=q["ratio"]).number_format = "0.000"
    ws.cell(row=ro, column=7, value=q["se"]).number_format = "0.000"
    r = ro + 2
    _note(ws, r, "Adding up: %s iOS accounts of those weeks have no channel and paid EUR %s (%.2f each); %s of them are the "
                 "five networks' unnamed installs and %s are organic. Fitted over %d market-weeks." % (
                     format(u["accounts"], ","), format(u["paid"], ","), u["paid_per_account"],
                     format(u["network_installs"], ","), format(u["organic_installs"], ","), u["market_weeks"]), 11)
    r += 2
    ws.cell(row=r, column=1, value="What the accounts with no channel come to, over what they paid").font = Font(bold=True)
    hdr2 = ["Unnamed installs valued", "All markets", "ES", "IT", "PT"]
    for k, h in enumerate(hdr2):
        ws.cell(row=r + 1, column=1 + k, value=h)
    _hdr(ws, r + 1, len(hdr2), 30)
    for i, (key, lab) in enumerate((("named", "like the named installs"), ("search_ads", "with Apple Search Ads' ratio"),
                                    ("fitted", "with each source's fitted ratio"))):
        vals = [lab, R["adding_up"][key]] + [R["adding_up_by_market"][key][m] for m in ("ES", "IT", "PT")]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r + 2 + i, column=1 + k, value=v)
            if k:
                cell.number_format = "0.00"
    r += 6
    ws.cell(row=r, column=1, value="Could sources share one ratio? Difference of their ratios against the fit's "
                                    "spread, taken row by row and with one variance for every row").font = Font(bold=True)
    hdr3 = ["Sources", "Statistic, spread row by row", "Statistic, one variance", "Degrees of freedom", "Five per cent point",
            "Share one ratio"]
    for k, h in enumerate(hdr3):
        ws.cell(row=r + 1, column=1 + k, value=h)
    _hdr(ws, r + 1, len(hdr3), 44)
    for i, (nm, t) in enumerate(R["share_tests"].items()):
        vals = [nm, t["stat"], t["stat_one_variance"], t["df"], t["point"], "no" if t["refused"] else "could"]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r + 2 + i, column=1 + k, value=v)
            if k in (1, 2, 4):
                cell.number_format = "0.00"
    r += 3 + len(R["share_tests"])
    ws.cell(row=r, column=1, value="Check on Android, where every install carries its channel: installs that declined "
                                    "tracking, 12-month net revenue each (EUR)").font = Font(bold=True)
    hdr4 = ["Channel", "Installs that declined tracking", "Paid", "Same fit, channel set aside",
            "Valued like the installs that allowed tracking", "With Apple Search Ads' ratio", "With one ratio for every source"]
    for k, h in enumerate(hdr4):
        ws.cell(row=r + 1, column=1 + k, value=h)
    _hdr(ws, r + 1, len(hdr4), 44)
    for i, (c, a) in enumerate(f["check_android"].items()):
        vals = [c, a["installs"], a["paid"], a["fitted"], a["named"], a["search_ads"], a["one_ratio"]]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r + 2 + i, column=1 + k, value=v)
            cell.number_format = "#,##0" if k == 1 else ("0.00" if k else "General")
    _widths(ws, (30, 13, 13, 10, 17, 17, 10, 17, 12, 20, 16))
    ws.freeze_panes = "B5"


def response_sheet(wb, f, all_ch):
    ws = wb.create_sheet("Budget response")
    m = f["check_moves"]
    _title(ws, "What a weekly budget buys: %d weeks to 1 Nov 2026, carried to the plan's %d weeks" % (
        f["steps"]["weeks"], f["steps"]["plan_weeks"]),
           "Installs and value per install against the week's budget with the share of it spent beside it; month pattern "
           "shared across channels.")
    ws.append([])
    hdr = ["Channel", "Spend over budget, %d weeks" % f["steps"]["weeks"], "Installs: elasticity to the budget",
           "Value per install: slope on the budget", "Installs: elasticity fitted on spend", "Weekly spend, history (EUR)",
           "Weekly spend, 2027 plan (EUR)", "Weekly budget that delivers it (EUR)", "Installs a week at plan spend",
           "Installs a week, response fitted on spend", "Budget moves logged", "Weeks raised", "Weeks lowered",
           "Moved weeks, each move left out of the fit: installs raised over lowered, actual", "from the budget fit",
           "from the spend fit"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 84)
    for i, c in enumerate(all_ch):
        x, mv = f["channels"][c], m["channels"][c]
        ws.append([c, x["delivery_share"], x["budget_elasticity"], x["value_slope"], x["spend_elasticity"],
                   x["history_weekly_spend"], x["plan_weekly_spend"], x["plan_weekly_budget"], x["installs_week_plan"],
                   x["installs_week_spend_fit"], mv["moves"], mv["raised"], mv["lowered"], mv["actual"], mv["budget_fit"],
                   mv["spend_fit"]])
        for k in (2, 3, 4, 5, 14, 15, 16):
            ws.cell(row=5 + i, column=k).number_format = "0.000"
        for k in (6, 7, 8, 9, 10):
            ws.cell(row=5 + i, column=k).number_format = "#,##0"
    r = 5 + len(all_ch) + 1
    h = f["holdout"]["every_fourth_week"]
    _note(ws, r, "Across the %d weeks of the %d logged moves, each move left out of the fit in turn, the fit on spend misses "
                 "the installs by %.1f per cent and the fit on the budget by %.1f. With every fourth week held out instead, "
                 "the fit on spend misses by %.1f per cent, the budget with the share spent by %.1f and the budget alone by "
                 "%.1f." % (m["weeks"], m["moves"], m["missed_pct"]["spend"], m["missed_pct"]["golden"], h["spend"], h["golden"],
                           h["budget"]), 16, 34)
    ws.cell(row=r + 1, column=1, value="Apple Search Ads is shown for the record; it sits on the plan's brand sheet at a "
                                        "fixed budget.").font = Font(size=9, color="444444")
    _widths(ws, (18, 11, 11, 11, 11, 11, 11, 12, 11, 12, 8, 8, 8, 16, 10, 10))
    ws.freeze_panes = "B5"


def ranges_sheet(wb, f, chans):
    ws = wb.create_sheet("Ranges")
    _title(ws, "Each figure with its range across the other ways the three estimates could be taken",
           "Each alternative alone, every two that can be made together and one change to each estimate at once; low and "
           "high hold their span with %s per cent of the figure either side. Every alternative files the same seven "
           "bands." % f["band_pad_pct"])
    ws.append([])
    hdr = ["Channel", "Band"]
    for _k, h, _n in COLS:
        hdr += [h, "low", "high"]
    ws.append(hdr)
    ws["A3"] = ("Low and high also reach %g per cent of the figure beyond four further readings, each run on its own, "
                "wherever one moves the figure: the finer-row fits of the ratios, the unscaled installs prediction, the "
                "other groupings of the first-48-hour values and the value equation on the complete weeks."
                % f["beside_pad_pct"])
    ws["A3"].font = Font(italic=True, size=9, color="555555", name="Calibri")
    _hdr(ws, 4, len(hdr), 70)
    for i, c in enumerate(chans):
        row = [c, f["bands"][c].capitalize()]
        for k, _h, _n in COLS:
            row += [f[k][c]] + list(f[k + "_band"][c])
        ws.append(row)
        ws.cell(row=5 + i, column=2).fill = PatternFill("solid", fgColor=FILL[f["bands"][c]])
        ws.cell(row=5 + i, column=2).alignment = Alignment(horizontal="center")
        for j, (_k, _h, nf) in enumerate(COLS):
            for d in range(3):
                ws.cell(row=5 + i, column=3 + 3 * j + d).number_format = nf
    _widths(ws, (20, 9) + (15, 8, 8) * len(COLS))
    ws.freeze_panes = "C5"


def routes_sheet(wb, f, chans):
    ws = wb.create_sheet("Routes")
    _title(ws, "The figures under each simpler choice, beside the estimate",
           "One choice changed at a time, then all three, then the dashboard reading; the band each would file.")
    ws.append([])
    nk = len(ROUTES)
    blocks = [("return_plan", "Return at plan spend (EUR per EUR)", "0.000", True),
              ("paid_per_install", "12-month net revenue per install, installs of 4 Nov 2024 to 2 Nov 2025 (EUR)", "0.00", False),
              ("installs_week", "Installs a week at plan spend", "#,##0", False)]
    row = 4
    for key, title, nf, with_band in blocks:
        ws.cell(row=row, column=1, value=title).font = Font(bold=True)
        hdr = ["Channel", "Estimate"] + [LOST[k] for k in ROUTES[1:]]
        if with_band:
            hdr += ["Band: estimate"] + ["Band: " + LOST[k][0].lower() + LOST[k][1:] for k in ROUTES[1:]]
        for k, h in enumerate(hdr):
            ws.cell(row=row + 1, column=1 + k, value=h)
        _hdr(ws, row + 1, len(hdr), 58)
        for i, c in enumerate(chans):
            vals = [c] + [f["routes"][k][c][key] for k in ROUTES]
            for k, v in enumerate(vals):
                cell = ws.cell(row=row + 2 + i, column=1 + k, value=v)
                if k:
                    cell.number_format = nf
            if with_band:
                for j, k in enumerate(ROUTES):
                    cell = ws.cell(row=row + 2 + i, column=2 + nk + j, value=f["routes"][k][c]["band"].capitalize())
                    cell.fill = PatternFill("solid", fgColor=FILL[f["routes"][k][c]["band"]])
                    cell.alignment = Alignment(horizontal="center")
        row += 2 + len(chans) + 2
    _widths(ws, (20, 10, 15, 15, 15, 12, 17, 10, 15, 15, 15, 12, 17))
    ws.freeze_panes = "B4"


def build(folder, f):
    os.makedirs(folder, exist_ok=True)
    chans = order(f)
    all_ch = list(f["channels"])
    gated = [c for c in all_ch if "named_pct" in f["channels"][c]]
    wb = Workbook()
    first_sheet(wb, f, chans)
    unrecorded_sheet(wb, f, all_ch)
    unnamed_sheet(wb, f, gated)
    response_sheet(wb, f, all_ch)
    ranges_sheet(wb, f, chans)
    routes_sheet(wb, f, chans)
    wb.save(os.path.join(folder, FILES["wb"]))
    with open(os.path.join(folder, FILES["csv"]), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(CSV_COLS)
        for c in chans:
            w.writerow([c, f["bands"][c]] + [CSV_FMT[k] % f[k][c] for k, _h, _n in COLS])
    return chans
