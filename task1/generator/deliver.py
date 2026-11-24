"""The two golden files: the workbook the head of financial planning opens (the bands on its first sheet, the
working behind it) and the channel and plan figures as a CSV. Every number comes from figures.json."""
import os  # noqa: E402
# numpy runs on Apple's Accelerate here, whose threads do not survive a fork: one thread, set before numpy loads
for _v in ("VECLIB_MAXIMUM_THREADS", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import csv
import os

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

FILES = {"wb": "paid_channels_2027.xlsx", "csv": "paid_channels_2027.csv"}
FILL = {"scale": "D7EAD3", "hold": "FBEBC8", "cut": "F3D3CF"}
HEAD = PatternFill("solid", fgColor="22364F")
THIN = Side(style="thin", color="B8BEC8")
LOST = {"S1": "Billing records as they stand", "S2": "Unnamed installs at the named channels' shift",
        "S3": "Plan spend read as a budget billed in full", "S1+S2+S3": "All three together",
        "direct": "Records as they stand, named revenue only, last year's return",
        "rigorous": "Records scaled to the stores period by period"}
ROUTES = ["golden", "S1", "S2", "S3", "S1+S2+S3", "rigorous", "direct"]
PAY = "Monthly-plan payments per 100 installs, first 12 months (installs of 4 Nov 2024 to 2 Nov 2025)"
CSV_COLS = ["row", "channel", "band", "return_per_eur_plan_spend",
            "monthly_plan_payments_per_100_installs_2024-11-04_to_2025-11-02", "installs_2027", "net_revenue_12m_eur"]


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def order(f):
    """the plan's channels, highest return at the plan's spend first"""
    return sorted(f["return_plan"], key=lambda c: (-f["return_plan"][c], -f["pay100"][c]))


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


def _row(ws, row, vals, fmts):
    for k, (v, nf) in enumerate(zip(vals, fmts)):
        cell = ws.cell(row=row, column=1 + k, value=v)
        if nf:
            cell.number_format = nf


def _band(cell, b):
    cell.value = b.capitalize()
    cell.fill = PatternFill("solid", fgColor=FILL[b])
    cell.alignment = Alignment(horizontal="center")


def first_sheet(wb, f, chans):
    ws = wb.active
    ws.title = "Bands 2027"
    b = f["by_band"]
    lo, hi = f["policy"]["lines"]
    _title(ws, "2027 media plan: scale %s, hold %s%s" % (_list(b["scale"]), _list(b["hold"]),
                                                        (", cut " + _list(b["cut"])) if b["cut"] else ""),
           "Growth policy v3, section 3. Return = 12-month net revenue per euro of spend at the plan's weekly spend, as "
           "the platforms bill it. Records to 8 November 2026. E. Rey, growth analytics.")
    r = f["routes"]["S1+S2+S3"]
    moved = [c for c in chans if r[c]["band"] != f["bands"][c]]
    ws["A3"] = ("Not the bands the quick reading gives: with the billing records as they stand, the unnamed iOS installs "
                "valued at the shift the fully named channels show and the plan's spend read as a budget billed in full, "
                "%s. The Routes sheet sets each of those choices beside the estimate." % _list(
                    "%s would %s (%.3f)" % (c, r[c]["band"], r[c]["return_plan"]) for c in moved))
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:H3")
    ws.row_dimensions[3].height = 58
    hdr = ["Channel", "Band", "Return at plan spend (EUR per EUR)", PAY, "Plan weekly spend, average (EUR)",
           "Plan spend, 2027 (EUR)", "Hold from %.2f" % lo, "Scale from %.2f" % hi]
    ws.append([])
    ws.append(hdr)
    _hdr(ws, 5, len(hdr), 70)
    for i, c in enumerate(chans):
        row = 6 + i
        x = f["channels"][c]
        _row(ws, row, [c, None, f["return_plan"][c], f["pay100"][c], x["plan_weekly_spend"], x["plan_year_spend"], lo, hi],
             [None, None, "0.000", "0.0", "#,##0", "#,##0", "0.00", "0.00"])
        _band(ws.cell(row=row, column=2), f["bands"][c])
    last = 5 + len(chans)
    pr = last + 2
    ws.cell(row=pr, column=1, value="Whole growth plan, 2027").font = Font(bold=True)
    _row(ws, pr + 1, ["Installs the plan's spend buys", f["plan_installs"]], [None, "#,##0"])
    _row(ws, pr + 2, ["Their 12-month net revenue (EUR)", f["plan_revenue"]], [None, "#,##0"])
    _row(ws, pr + 3, ["Plan spend, seven growth channels (EUR)", f["plan_spend"]], [None, "#,##0"])
    notes = ["Bands: scale from %.2f, hold from %.2f, cut under %.2f (policy 3.1). Apple Search Ads is on the brand "
             "sheet of the plan and is not placed." % (hi, lo, lo),
             "Installs are first installs of consumer accounts (policy 2.2), named in the attribution export or not; the "
             "iOS networks' installs are counted from their install postbacks.",
             "Net revenue is after VAT by storefront, the stores' %d per cent and the checkout's %d per cent "
             "(policy 2.4), on every charge made in the %d days from the install, refunds netted." % (
                 f["policy"]["commission_pct"], f["policy"]["fee_pct"], f["steps"]["days"]),
             "Payments on the monthly plan count every monthly charge in the 365 days from the install, the first at "
             "the trial's end among them, on both stores and the web checkout. The Ranges sheet gives each figure's "
             "range across the other ways the estimates could be taken."]
    for i, t in enumerate(notes):
        ws.cell(row=pr + 5 + i, column=1, value=t).font = Font(size=9, color="444444", name="Calibri")
    _widths(ws, (34, 9, 14, 24, 14, 14, 9, 9))
    ws.freeze_panes = "B6"
    bar = BarChart()
    bar.type = "col"
    bar.title = "%s clear %.2f at the plan's spend; %s sit between the lines" % (_list(b["scale"]), hi, _list(b["hold"]))
    bar.y_axis.title = "EUR of 12-month net revenue per EUR of spend"
    bar.add_data(Reference(ws, min_col=3, max_col=3, min_row=5, max_row=last), titles_from_data=True)
    bar.set_categories(Reference(ws, min_col=1, min_row=6, max_row=last))
    bar.y_axis.scaling.min = 0
    bar.y_axis.number_format = "0.00"
    bar.y_axis.delete = False
    bar.x_axis.delete = False
    bar.series[0].graphicalProperties.solidFill = "2A78D6"
    line = LineChart()
    line.add_data(Reference(ws, min_col=7, max_col=8, min_row=5, max_row=last), titles_from_data=True)
    for s in line.series:
        s.graphicalProperties.line.solidFill = "52514E"
        s.graphicalProperties.line.width = 19050
        s.marker.symbol = "none"
        s.smooth = False
    line.series[0].graphicalProperties.line.dashStyle = "dash"
    bar += line
    bar.height, bar.width = 8.6, 19.0
    bar.legend.position = "b"
    ws.add_chart(bar, "A%d" % (pr + 10))
    ws.print_area = "A1:H%d" % (pr + 28)


def unrecorded_sheet(wb, f, all_ch):
    ws = wb.create_sheet("Unrecorded charges")
    _title(ws, "Store charges the billing records never took in, installs of 4 Nov 2024 to 2 Nov 2025",
           "Stores' daily reports against the billing events, by %s-day period from 4 Nov 2024 (App Store on Pacific days)."
           % f["policy"]["cadence_days"])
    ws.append([])
    hdr = ["Channel", "Installs bought", "Monthly-plan payments per 100 installs, in the records", PAY,
           "12-month net revenue per install, in the records (EUR)", "12-month net revenue per install (EUR)",
           "Revenue not in the records"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 70)
    for i, c in enumerate(all_ch):
        x = f["channels"][c]
        _row(ws, 5 + i, [c, x["installs_mature"], x["recorded_pay100"], x["pay100"], x["recorded_per_install"],
                         x["paid_per_install"], x["unrecorded_pct"] / 100.0],
             [None, "#,##0", "0.0", "0.0", "0.00", "0.00", "0.0%"])
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
        _row(ws, r0 + 2 + i, [name, st["first_excess"], st["trial_candidates_monthly"], st["trial_end_share_monthly"],
                              st["annual_excess"], st["trial_candidates_annual"], st["trial_end_share_annual"],
                              st["renewal_excess"], st["renewal_candidates"], st["continuation"]],
             [None, "#,##0", "#,##0", "0.000", "#,##0", "#,##0", "0.000", "#,##0", "#,##0", "0.000"])
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
        _row(ws, r1 + 2 + i, vals, [None, "#,##0"] + ["0.000", "#,##0", "#,##0"] * 3)
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
        _row(ws, r3 + 1 + i, [d, gp[i]["renewals"], gp[i]["fitted"], ap[i]["renewals"], ap[i]["fitted"], gp[i]["first"],
                              ap[i]["first"]], [None] + ["#,##0"] * 6)
    ws.cell(row=r3 + 1 + len(f["period_starts"]), column=1,
            value="The last period runs to the pull and is left out of the fit.").font = Font(size=9, color="444444")
    _widths(ws, (22, 16, 18, 18, 16, 16, 14, 16, 20, 16, 14))
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
           "Named installs, 12-month net revenue each (EUR)", "Unnamed over named at the same first-48-hour value, revenue",
           "standard error", "the same, monthly-plan payments", "Unnamed installs, 12-month net revenue each (EUR)",
           "All installs (EUR)", PAY, "With the named channels' shift"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 84)
    for i, c in enumerate(gated):
        x, q = f["channels"][c], R["sources"][c]
        _row(ws, 5 + i, [c, x["installs_mature"], x["named_mature"], x["named_pct"] / 100.0, x["named_value"], q["ratio"],
                         q["se"], q["ratio_payments"], x["declined_value"], x["paid_per_install"], x["pay100"],
                         x["borrowed_pay100"]],
             [None, "#,##0", "#,##0", "0.0%", "0.00", "0.000", "0.000", "0.000", "0.00", "0.00", "0.0", "0.0"])
    ro = 5 + len(gated)
    q = R["sources"]["organic iOS"]
    _row(ws, ro, ["Organic (the accounts left over)", q["declined"] + q["named"], q["named"], None, None, q["ratio"], q["se"],
                  q["ratio_payments"]], [None, "#,##0", "#,##0", None, None, "0.000", "0.000", "0.000"])
    r = ro + 2
    _note(ws, r, "Adding up: %s iOS accounts of those weeks have no channel and paid EUR %s (%.2f each); %s of them are the "
                 "five networks' unnamed installs and %s are organic. Fitted over %d market-weeks." % (
                     format(u["accounts"], ","), format(u["paid"], ","), u["paid_per_account"],
                     format(u["network_installs"], ","), format(u["organic_installs"], ","), u["market_weeks"]), 12)
    r += 2
    ws.cell(row=r, column=1, value="What the accounts with no channel come to, over what they paid").font = Font(bold=True)
    hdr2 = ["Unnamed installs valued", "All markets", "ES", "IT", "PT"]
    for k, h in enumerate(hdr2):
        ws.cell(row=r + 1, column=1 + k, value=h)
    _hdr(ws, r + 1, len(hdr2), 30)
    for i, (key, lab) in enumerate((("named", "like the named installs"), ("search_ads", "with Apple Search Ads' ratio"),
                                    ("fitted", "with each source's fitted ratio"))):
        _row(ws, r + 2 + i, [lab, R["adding_up"][key]] + [R["adding_up_by_market"][key][m] for m in ("ES", "IT", "PT")],
             [None] + ["0.000"] * 4)
    P = f["pooled"]
    r += 6
    ws.cell(row=r, column=1, value="Each source's ratio fitted on the 156 market-weeks, on the 52 weeks with the three "
                                    "markets summed, and on each market's own weeks").font = Font(bold=True)
    hdr5 = ["Source", "156 market-weeks", "52 weeks, markets summed", "Spain alone", "Italy alone", "Portugal alone"]
    for k, h in enumerate(hdr5):
        ws.cell(row=r + 1, column=1 + k, value=h)
    _hdr(ws, r + 1, len(hdr5), 30)
    for i, (nm, x) in enumerate(P["ratio"].items()):
        _row(ws, r + 2 + i, [nm, x["golden"], x["pooled"]] + x["markets"], [None] + ["0.000"] * 5)
    r += 3 + len(P["ratio"])
    hdr6 = ["Network", "Market-weeks it spent in", "Market-weeks with no spend", "At the 156-row ratios: weeks it spent in",
            "weeks with no spend", "At the summed-markets ratios: weeks it spent in", "weeks with no spend"]
    for k, h in enumerate(hdr6):
        ws.cell(row=r, column=1 + k, value=h)
    _hdr(ws, r, len(hdr6), 44)
    for i, (nm, x) in enumerate(P["split_pack"].items()):
        _row(ws, r + 1 + i, [nm, x["live"], x["dark"]] + x["golden"] + x["pooled"], [None, "#,##0", "#,##0"] + ["0.000"] * 4)
    r += 2 + len(P["split_pack"])
    ws.cell(row=r, column=1, value="Could sources share one ratio? Difference of their ratios against the fit's "
                                    "spread, taken row by row and with one variance for every row").font = Font(bold=True)
    hdr3 = ["Sources", "Statistic, spread row by row", "Statistic, one variance", "Degrees of freedom", "Five per cent point",
            "Share one ratio"]
    for k, h in enumerate(hdr3):
        ws.cell(row=r + 1, column=1 + k, value=h)
    _hdr(ws, r + 1, len(hdr3), 44)
    for i, (nm, t) in enumerate(R["share_tests"].items()):
        _row(ws, r + 2 + i, [nm, t["stat"], t["stat_one_variance"], t["df"], t["point"], "no" if t["refused"] else "could"],
             [None, "0.00", "0.00", None, "0.00", None])
    r += 3 + len(R["share_tests"])
    ws.cell(row=r, column=1, value="Check on Android, where every install carries its channel: installs that declined "
                                    "tracking, 12-month net revenue each (EUR)").font = Font(bold=True)
    hdr4 = ["Channel", "Installs that declined tracking", "Paid", "Same fit, channel set aside",
            "Valued like the installs that allowed tracking", "With Apple Search Ads' ratio", "With one ratio for every source"]
    for k, h in enumerate(hdr4):
        ws.cell(row=r + 1, column=1 + k, value=h)
    _hdr(ws, r + 1, len(hdr4), 44)
    for i, (c, a) in enumerate(f["check_android"].items()):
        _row(ws, r + 2 + i, [c, a["installs"], a["paid"], a["fitted"], a["named"], a["search_ads"], a["one_ratio"]],
             [None, "#,##0"] + ["0.00"] * 5)
    _widths(ws, (30, 13, 13, 12, 17, 17, 10, 14, 17, 12, 18, 14))
    ws.freeze_panes = "B5"


def response_sheet(wb, f, all_ch):
    ws = wb.create_sheet("Budget response")
    m, d = f["check_moves"], f["delivery"]
    _title(ws, "What a weekly budget buys: %d weeks to 1 Nov 2026, carried to the plan's %d weeks" % (
        f["steps"]["weeks"], f["steps"]["plan_weeks"]),
           "Installs and value per install against the week's budget with the share of it billed beside it; month pattern "
           "shared across channels. The plan's weekly figures are billed spend, carried at the budget that bills them at "
           "the channel's share.")
    ws.append([])
    hdr = ["Channel", "Billed over budget, %d weeks" % f["steps"]["weeks"], "Weeks billing the whole budget",
           "Best quarter, billed over budget", "Installs: elasticity to the budget", "Value per install: slope on the budget",
           "Installs: elasticity fitted on billed spend", "Weekly spend, history (EUR)", "Weekly spend, 2027 plan (EUR)",
           "Weekly budget that bills it (EUR)", "Installs a week at plan spend", "Installs a week, plan read as budget",
           "Budget moves logged", "Moved weeks, each move left out of the fit: installs raised over lowered, actual",
           "from the budget fit", "from the spend fit"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 84)
    for i, c in enumerate(all_ch):
        x, mv = f["channels"][c], m["channels"][c]
        dc = d["channels"].get(c, {})
        _row(ws, 5 + i, [c, x["delivery_share"], dc.get("whole"), dc.get("best_quarter"), x["budget_elasticity"],
                         x["value_slope"], x["spend_fit_elasticity"], x["history_weekly_spend"], x["plan_weekly_spend"],
                         x["plan_weekly_budget"], x["installs_week_plan"], x["installs_week_full"], mv["moves"],
                         mv["actual"], mv["budget_fit"], mv["spend_fit"]],
             [None, "0.000", "0", "0.000", "0.000", "0.000", "0.000", "#,##0", "#,##0", "#,##0", "#,##0", "#,##0", "0",
              "0.000", "0.000", "0.000"])
    r = 5 + len(all_ch) + 1
    h = f["holdout"]["every_fourth_week"]
    _note(ws, r, "Across the %d weeks of the %d logged moves, each move left out of the fit in turn, the fit on billed "
                 "spend misses the installs by %.1f per cent and the fit on the budget by %.1f. With every fourth week held "
                 "out instead, the fit on spend misses by %.1f per cent, the budget with the share billed by %.1f and the "
                 "budget alone by %.1f." % (m["weeks"], m["moves"], m["missed_pct"]["spend"], m["missed_pct"]["golden"],
                                            h["spend"], h["golden"], h["budget"]), 16, 34)
    _note(ws, r + 1, "Run over the record's own budgets at a share of one, the installs fit adds up to %.1f to %.1f per cent "
                     "of the installs counted." % (d["adds_up_pct"][0], d["adds_up_pct"][1]), 16, 20)
    ws.cell(row=r + 2, column=1, value="Apple Search Ads is shown for the record; it sits on the plan's brand sheet at a "
                                        "fixed budget.").font = Font(size=9, color="444444")
    _widths(ws, (18, 11, 10, 11, 11, 11, 11, 11, 11, 12, 11, 12, 8, 16, 10, 10))
    ws.freeze_panes = "B5"


def ranges_sheet(wb, f, chans):
    ws = wb.create_sheet("Ranges")
    _title(ws, "Each figure with its range across the other ways the estimates could be taken",
           "Each alternative alone; low and high hold their span with %s per cent of the figure either side. Every "
           "alternative, and every two that can be made together and one change to each estimate at once, files the "
           "same seven bands." % f["band_pad_pct"])
    ws["A3"] = ("Low and high also reach %g per cent of the figure beyond the readings run on their own, wherever one "
                "moves the figure: the finer-row fits of the ratios, the unscaled installs prediction, the other "
                "groupings of the first-48-hour values and the value equation on the complete weeks."
                % f["beside_pad_pct"])
    ws["A3"].font = Font(italic=True, size=9, color="555555", name="Calibri")
    hdr = ["Channel", "Band", "Return at plan spend (EUR per EUR)", "low", "high", PAY, "low", "high"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr), 70)
    for i, c in enumerate(chans):
        _row(ws, 5 + i, [c, None, f["return_plan"][c]] + list(f["return_plan_band"][c]) + [f["pay100"][c]]
             + list(f["pay100_band"][c]), [None, None, "0.000", "0.000", "0.000", "0.0", "0.0", "0.0"])
        _band(ws.cell(row=5 + i, column=2), f["bands"][c])
    r = 6 + len(chans)
    _row(ws, r, ["Installs the plan's 2027 spend buys", None, f["plan_installs"]] + list(f["plan_installs_band"]),
         [None, None, "#,##0", "#,##0", "#,##0"])
    _row(ws, r + 1, ["Their 12-month net revenue (EUR)", None, f["plan_revenue"]] + list(f["plan_revenue_band"]),
         [None, None, "#,##0", "#,##0", "#,##0"])
    _widths(ws, (34, 9, 15, 8, 8, 22, 8, 8))
    ws.freeze_panes = "C5"


def routes_sheet(wb, f, chans):
    ws = wb.create_sheet("Routes")
    _title(ws, "The figures under each simpler choice, beside the estimate",
           "One choice changed at a time, then all three, then the stores' ratio period by period, then the dashboard "
           "reading; the band each would file.")
    ws.append([])
    nk = len(ROUTES)
    blocks = [("return_plan", "Return at plan spend (EUR per EUR)", "0.000", True), ("pay100", PAY, "0.0", False)]
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
            _row(ws, row + 2 + i, [c] + [f["routes"][k][c][key] for k in ROUTES], [None] + [nf] * nk)
            if with_band:
                for j, k in enumerate(ROUTES):
                    _band(ws.cell(row=row + 2 + i, column=2 + nk + j), f["routes"][k][c]["band"])
        row += 2 + len(chans) + 2
    ws.cell(row=row, column=1, value="Whole plan").font = Font(bold=True)
    hdr = ["", "Estimate"] + [LOST[k] for k in ROUTES[1:]]
    for k, h in enumerate(hdr):
        ws.cell(row=row + 1, column=1 + k, value=h)
    _hdr(ws, row + 1, len(hdr), 58)
    _row(ws, row + 2, ["Installs the plan buys"] + [f["routes"][k]["plan"]["installs"] for k in ROUTES], [None] + ["#,##0"] * nk)
    _row(ws, row + 3, ["Their 12-month net revenue (EUR)"] + [f["routes"][k]["plan"]["revenue"] for k in ROUTES],
         [None] + ["#,##0"] * nk)
    _widths(ws, (30, 10) + (15,) * (nk - 1) + (11,) * nk)
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
            w.writerow(["channel", c, f["bands"][c], "%.3f" % f["return_plan"][c], "%.1f" % f["pay100"][c], "", ""])
        w.writerow(["plan", "all seven growth channels", "", "", "", "%d" % f["plan_installs"], "%d" % f["plan_revenue"]])
    return chans
