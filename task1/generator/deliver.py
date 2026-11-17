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
LOST = {"S1": "Records trued up to the stores month by month", "S2": "Every postback at the named installs' value",
        "S3": "Response fitted on weekly spend", "S1+S2+S3": "All three together",
        "direct": "Records as they stand, named installs only"}


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def order(f):
    return sorted(f["return_plan"], key=lambda c: -f["routes"]["golden"][c]["return"] * 1000 - f["value_plan"][c] / 1000.0)


def _hdr(ws, row, n):
    for c in ws[row][:n]:
        c.font = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
        c.fill = HEAD
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center")
        c.border = Border(bottom=THIN)
    ws.row_dimensions[row].height = 44


def _widths(ws, ws_):
    for col, w in zip("ABCDEFGHIJKLMN", ws_):
        ws.column_dimensions[col].width = w


def _title(ws, text, sub=None):
    ws["A1"] = text
    ws["A1"].font = Font(bold=True, size=12, name="Calibri")
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(italic=True, size=9, color="555555", name="Calibri")


def first_sheet(wb, f, chans):
    ws = wb.active
    ws.title = "Bands 2027"
    b = f["by_band"]
    _title(ws, "2027 media plan: scale %s, hold %s, cut %s" % (_list(b["scale"]), _list(b["hold"]), _list(b["cut"])),
           "Growth policy v3, section 3. Return = 12-month net revenue per euro of spend at the plan's weekly spend. "
           "Records to 8 November 2026. E. Rey, growth analytics.")
    r = f["routes"]["S1+S2+S3"]
    ws["A3"] = ("Not the reading the raw reconciliation gives: with the billing records trued up to the stores month by month, "
                "every postback valued like the named installs and the response fitted on weekly spend, Meta iOS would "
                "scale (%.2f) and Google Android (%.2f) and AppLovin Android (%.2f) would be cut. The Routes sheet sets "
                "each of those choices beside the estimate." % (r["Meta iOS"]["return"], r["Google Android"]["return"],
                                                             r["AppLovin Android"]["return"]))
    ws["A3"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A3:I3")
    ws.row_dimensions[3].height = 46
    hdr = ["Channel", "Band", "Return at plan spend (EUR per EUR)", "Return at stretch spend (EUR per EUR)",
           "12-month net revenue per install at plan spend (EUR)", "Return on one more euro at plan spend (EUR)",
           "Plan weekly spend, average (EUR)", "Hold from %.2f" % f["policy"]["lines"][0],
           "Scale from %.2f" % f["policy"]["lines"][1]]
    ws.append([])
    ws.append(hdr)
    _hdr(ws, 5, len(hdr))
    for i, c in enumerate(chans):
        ws.append([c, f["bands"][c].capitalize(), f["return_plan"][c], f["return_stretch"][c], f["value_plan"][c],
                   f["next_euro"][c], f["channels"][c]["plan_weekly_spend"], f["policy"]["lines"][0], f["policy"]["lines"][1]])
        row = 6 + i
        ws.cell(row=row, column=2).fill = PatternFill("solid", fgColor=FILL[f["bands"][c]])
        ws.cell(row=row, column=2).alignment = Alignment(horizontal="center")
        for k in (3, 4, 6, 8, 9):
            ws.cell(row=row, column=k).number_format = "0.00"
        ws.cell(row=row, column=5).number_format = "#,##0.00"
        ws.cell(row=row, column=7).number_format = "#,##0"
    last = 5 + len(chans)
    ws.cell(row=last + 2, column=1, value="Plan spend on the five iOS networks buys (12-month net revenue, EUR)")
    ws.cell(row=last + 2, column=5, value=f["plan_and_stretch_revenue"]["plan revenue iOS networks"]).number_format = "#,##0"
    ws.cell(row=last + 3, column=1, value="Stretch spend adds across the seven channels (12-month net revenue, EUR)")
    ws.cell(row=last + 3, column=5, value=f["plan_and_stretch_revenue"]["stretch adds"]).number_format = "#,##0"
    ws.cell(row=last + 4, column=1, value="Of AppLovin Android's 12-month net revenue, never taken into the billing records")
    ws.cell(row=last + 4, column=5, value=f["unrecorded_share_applovin_android_pct"] / 100.0).number_format = "0.0%"
    ws.cell(row=last + 5, column=1, value="Meta iOS, 12-month net revenue per install over every install bought, "
                                         "4 Nov 2024 to 2 Nov 2025 (EUR)")
    ws.cell(row=last + 5, column=5, value=f["value_per_install_meta_ios"]).number_format = "0.00"
    notes = ["Bands: scale from 1.20, hold from 0.90, cut under 0.90 (policy 3.1). Apple Search Ads is on the brand "
             "sheet of the plan and is not placed.",
             "Installs are first installs of consumer accounts (policy 2.2); the iOS networks' installs are counted "
             "from their install postbacks.",
             "Net revenue is after VAT by storefront, the stores' 15 per cent and the checkout's 3 per cent "
             "(policy 2.4), on every charge made in the 365 days from the install.",
             "Returns to two decimals, euros per install to the cent; the working sheets carry the same figures."]
    for i, t in enumerate(notes):
        ws.cell(row=last + 7 + i, column=1, value=t).font = Font(size=9, color="444444", name="Calibri")
    _widths(ws, (26, 9, 14, 14, 18, 16, 14, 8, 8))
    ws.freeze_panes = "B6"
    bar = BarChart()
    bar.type = "col"
    bar.title = "%s clear %.2f at the plan's spend; %s stay under %.2f" % (
        _list(b["scale"]), f["policy"]["lines"][1], _list(b["cut"]), f["policy"]["lines"][0])
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
    line.add_data(Reference(ws, min_col=8, max_col=9, min_row=5, max_row=last), titles_from_data=True)
    line.series[0].graphicalProperties.line.solidFill = "52514E"    # the two lines in neutral ink, told apart by
    line.series[1].graphicalProperties.line.solidFill = "52514E"    # their dash and named with their values
    line.series[0].graphicalProperties.line.dashStyle = "dash"
    for s in line.series:
        s.graphicalProperties.line.width = 19050
        s.marker.symbol = "none"
        s.smooth = False
    bar += line
    bar.height, bar.width = 8.6, 19.5
    bar.legend.position = "b"
    ws.add_chart(bar, "A%d" % (last + 13))
    ws.print_area = "A1:I%d" % (last + 31)


def unrecorded_sheet(wb, f, all_ch):
    ws = wb.create_sheet("Unrecorded charges")
    _title(ws, "Store charges the billing records never took in, installs of 4 Nov 2024 to 2 Nov 2025",
           "Stores' daily reports against the billing events, by 30.4375-day period from 4 Nov 2024 (App Store on Pacific days).")
    ws.append([])
    hdr = ["Channel", "Installs bought", "Recorded 12-month net revenue per install (EUR)",
           "12-month net revenue per install (EUR)", "Not in the records", "If the gap were spread in proportion"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr))
    for i, c in enumerate(all_ch):
        x = f["channels"][c]
        ws.append([c, x["installs_mature"], x["recorded_per_install"], x["value_per_install"], x["unrecorded_pct"] / 100.0,
                   x["prop_unrecorded_pct"] / 100.0])
        ws.cell(row=5 + i, column=2).number_format = "#,##0"
        for k in (3, 4):
            ws.cell(row=5 + i, column=k).number_format = "0.00"
        for k in (5, 6):
            ws.cell(row=5 + i, column=k).number_format = "0.0%"
    r0 = 5 + len(all_ch) + 1
    ws.cell(row=r0, column=1, value="Fitted to the stores' excess").font = Font(bold=True)
    hdr2 = ["Store", "Monthly charges in the store's report", "Monthly charges in the records", "Trials last seen set to renew",
            "Share of them charged at the trial's end", "Subscriptions last seen set to renew, next charge after the last open",
            "Monthly continuation once the app is not opened"]
    for k, h in enumerate(hdr2):
        ws.cell(row=r0 + 1, column=1 + k, value=h)
    _hdr(ws, r0 + 1, len(hdr2))
    for i, (name, s) in enumerate(f["stores"].items()):
        vals = [name, s["store_monthly_charges"], s["recorded_monthly_charges"], s["trial_candidates_monthly"],
                s["trial_end_share_monthly"], s["renewal_candidates"], s["continuation"]]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r0 + 2 + i, column=1 + k, value=v)
            cell.number_format = "0.000" if k in (4, 6) else ("#,##0" if k else "General")
    r1 = r0 + 5
    w = f["check_web"]
    ws.cell(row=r1, column=1, value="Check on the web checkout (every charge on file): AppLovin Android's %d web subscribers were "
                                    "charged EUR %.2f each after their last open inside twelve months; the estimate's rule puts "
                                    "%.2f there, a spread in proportion %.2f. Web continuation %.3f a month." % (
                                        w["subscribers"], w["charged"], w["estimate"], w["true_up"], f["web_continuation"]))
    ws.cell(row=r1, column=1).alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells(start_row=r1, start_column=1, end_row=r1, end_column=7)
    ws.row_dimensions[r1].height = 34
    r2 = r1 + 2
    hdr3 = ["Period from", "Google Play renewals: report less records", "fitted", "App Store renewals: report less records",
            "fitted", "Google Play first charges: report less records", "App Store first charges: report less records"]
    for k, h in enumerate(hdr3):
        ws.cell(row=r2, column=1 + k, value=h)
    _hdr(ws, r2, len(hdr3))
    gp, ap = f["stores"]["Google Play"]["periods"], f["stores"]["App Store"]["periods"]
    for i, d in enumerate(f["period_starts"]):
        vals = [d, gp[i]["renewals"], gp[i]["fitted"], ap[i]["renewals"], ap[i]["fitted"], gp[i]["first"], ap[i]["first"]]
        for k, v in enumerate(vals):
            cell = ws.cell(row=r2 + 1 + i, column=1 + k, value=v)
            if k:
                cell.number_format = "#,##0"
    _widths(ws, (22, 16, 18, 18, 16, 22, 18))
    ws.freeze_panes = "B5"


def unnamed_sheet(wb, f, gated):
    ws = wb.create_sheet("Unnamed installs")
    u = f["unnamed"]
    _title(ws, "iOS networks: installs the attribution export does not name, installs of 4 Nov 2024 to 2 Nov 2025",
           "Postbacks by first-48-hour value less the named installs, priced so the accounts with no channel add up to what they paid.")
    ws.append([])
    hdr = ["Network", "Installs (postbacks)", "Named in the export", "Share named", "Named installs, 12-month net revenue each (EUR)",
           "Unnamed installs, priced (EUR)", "All installs (EUR)", "If every postback were valued like the named installs (EUR)"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr))
    for i, c in enumerate(gated):
        x = f["channels"][c]
        ws.append([c, x["installs_mature"], x["named_mature"], x["consent_pct"] / 100.0, x["named_value"], x["unnamed_value"],
                   x["value_per_install"], x["bridge_value"]])
        for k in (2, 3):
            ws.cell(row=5 + i, column=k).number_format = "#,##0"
        ws.cell(row=5 + i, column=4).number_format = "0.0%"
        for k in (5, 6, 7, 8):
            ws.cell(row=5 + i, column=k).number_format = "0.00"
    r = 5 + len(gated) + 1
    s = f["check_search_ads"]
    lines = [
        "Adding up: %s iOS accounts of those weeks have no channel and paid EUR %s (%.2f each); %s of them are the five "
        "networks' unnamed installs and %s are organic." % (format(u["accounts"], ","), format(u["paid"], ","),
                                                            u["paid_per_account"], format(u["network_installs"], ","),
                                                            format(u["organic_installs"], ",")),
        "Valued like the named installs at the same first-48-hour value, those accounts come to %.2f times what they paid; "
        "the pricing used comes to %.2f." % (u["adding_up_named_price"], u["adding_up_golden"]),
        "Check on Apple Search Ads (named on every account): its %s installs that did not allow tracking paid EUR %.2f each; "
        "the pricing puts %.2f, the named installs' value at the same first-48-hour value %.2f." % (
            format(s["installs"], ","), s["paid"], s["estimate"], s["named_by_cell"])]
    for i, t in enumerate(lines):
        ws.cell(row=r + i, column=1, value=t).alignment = Alignment(wrap_text=True, vertical="top")
        ws.merge_cells(start_row=r + i, start_column=1, end_row=r + i, end_column=8)
        ws.row_dimensions[r + i].height = 30
    _widths(ws, (18, 14, 14, 10, 18, 16, 12, 22))
    ws.freeze_panes = "B5"


def response_sheet(wb, f, all_ch):
    ws = wb.create_sheet("Budget response")
    _title(ws, "What a weekly budget buys: 104 weeks to 1 Nov 2026, carried to the plan's 52 weeks",
           "Installs and value per install against the week's budget with the share of it spent beside it; month pattern shared across channels.")
    ws.append([])
    hdr = ["Channel", "Spend over budget, 104 weeks", "Installs: elasticity to the budget", "Value per install: slope on the budget",
           "Installs: elasticity fitted on spend", "Weekly spend, history (EUR)", "Weekly spend, 2027 plan (EUR)",
           "Installs a week at plan spend", "Budget moves logged",
           "Moved weeks, each left out of the fit: installs raised over lowered, actual", "from the budget fit", "from the spend fit"]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr))
    ws.row_dimensions[4].height = 70
    for i, c in enumerate(all_ch):
        x, m = f["channels"][c], f["check_moves"][c]
        ws.append([c, x["delivery_share"], x["budget_elasticity"], x["value_slope"], x["spend_elasticity"],
                   x["history_weekly_spend"], x["plan_weekly_spend"], x["installs_week_plan"], x["moves"], m["actual"],
                   m["budget_fit"], m["spend_fit"]])
        ws.cell(row=5 + i, column=2).number_format = "0.000"
        for k in (3, 4, 5, 10, 11, 12):
            ws.cell(row=5 + i, column=k).number_format = "0.00"
        for k in (6, 7):
            ws.cell(row=5 + i, column=k).number_format = "#,##0"
        ws.cell(row=5 + i, column=8).number_format = "#,##0.0"
    r = 5 + len(all_ch) + 1
    ws.cell(row=r, column=1, value="Apple Search Ads is shown for the record; it sits on the plan's brand sheet at a fixed budget.").font = \
        Font(size=9, color="444444")
    _widths(ws, (18, 12, 12, 12, 12, 12, 12, 12, 9, 18, 11, 11))
    ws.freeze_panes = "B5"


def routes_sheet(wb, f, chans):
    ws = wb.create_sheet("Routes")
    _title(ws, "Return at plan spend under each simpler choice, beside the estimate",
           "One choice changed at a time, then all three; the band each would file.")
    ws.append([])
    keys = ["golden", "S1", "S2", "S3", "S1+S2+S3", "direct"]
    hdr = ["Channel", "Estimate"] + [LOST[k] for k in keys[1:]] + ["Band: estimate"] + ["Band: " + LOST[k].lower() for k in keys[1:]]
    ws.append(hdr)
    _hdr(ws, 4, len(hdr))
    ws.row_dimensions[4].height = 58
    for i, c in enumerate(chans):
        ws.append([c] + [f["routes"][k][c]["return"] for k in keys] + [f["routes"][k][c]["band"] for k in keys])
        for k in range(2, 2 + len(keys)):
            ws.cell(row=5 + i, column=k).number_format = "0.00"
        for j, k in enumerate(keys):
            cell = ws.cell(row=5 + i, column=2 + len(keys) + j)
            cell.fill = PatternFill("solid", fgColor=FILL[f["routes"][k][c]["band"]])
            cell.alignment = Alignment(horizontal="center")
    _widths(ws, (18, 10, 14, 14, 14, 12, 14, 10, 14, 14, 14, 12, 14))
    ws.freeze_panes = "B5"


def build(folder, f):
    os.makedirs(folder, exist_ok=True)
    chans = order(f)
    all_ch = list(f["channels"])
    gated = [c for c in all_ch if "consent_pct" in f["channels"][c]]
    wb = Workbook()
    first_sheet(wb, f, chans)
    unrecorded_sheet(wb, f, all_ch)
    unnamed_sheet(wb, f, gated)
    response_sheet(wb, f, all_ch)
    routes_sheet(wb, f, chans)
    wb.save(os.path.join(folder, FILES["wb"]))
    with open(os.path.join(folder, FILES["csv"]), "w", newline="") as fh:
        w = csv.writer(fh, lineterminator="\n")
        w.writerow(["channel", "band", "return_plan_spend", "return_stretch_spend", "net_revenue_12m_per_install_plan_spend_eur",
                    "return_next_euro_plan_spend"])
        for c in chans:
            w.writerow([c, f["bands"][c], "%.2f" % f["return_plan"][c], "%.2f" % f["return_stretch"][c],
                        "%.2f" % f["value_plan"][c], "%.2f" % f["next_euro"][c]])
    return chans
