"""task9: the golden deliverables the prompt asks for (a short memo, a spreadsheet, the daily collateral CSV), written
from the analysis (R, unrounded working) and the figures (F, as stated). Nothing is typed.

    write_all(A, R, F, golden_dir, scratch)

The memo and the workbook pass through the house container writers, each with its own stamps after the pack's.
"""
import datetime as dt
import os

import numpy as np
import openpyxl
import pandas as pd
from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.shared import Mm, Pt, RGBColor
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import params as P
import postprocess as PP

MEMO, BOOK, DAILY = "sleeve_ladder_2027_memo.docx", "sleeve_ladder_2027.xlsx", "sleeve_collateral_on_record.csv"
AUTHOR = "Treasury Analysis"
UTC = dt.timezone.utc
STAMPS = {BOOK: ("2026-11-10T14:26:11Z", "2026-11-10T21:27:48Z"), MEMO: ("2026-11-10T15:38:00Z", "2026-11-10T21:52:00Z")}
CSV_TIME = dt.datetime(2026, 11, 10, 21, 19, 5, tzinfo=UTC)

INK, INK2, GRID = "#0b0b0b", "#52514e", "#e3e2de"
BLUE, ORANGE = "#2a78d6", "#eb6834"                      # validated together (dataviz palette, light surface)
HEAD_FILL = PatternFill("solid", fgColor="E9EEF4")
THIN = Side(style="thin", color="B8BEC6")
LIMIT_NAME = {"collateral": "Collateral limit", "settlement": "Settlement limit"}
SOUND_LABEL = {"circular blocks": "Record resampled in blocks of %s consecutive sales", "Newey-West": "Standard error allowing for %s lags",
               "averages by calendar year of expiry": "Calendar-year averages, one observation a year"}
SMALL = Font(size=9, color="52514E")


def day(s, year=True):
    return pd.Timestamp(s).strftime("%B %-d, %Y" if year else "%B %-d")


def n(v):
    return "{:,}".format(v)


def k1000(s):
    return (np.round(np.asarray(s, dtype=float) / 1000.0) * 1000).astype("int64")


def method_label(key):
    if key.startswith("circular blocks"):
        return SOUND_LABEL["circular blocks"] % key.split()[3]
    if key.startswith("Newey-West"):
        return SOUND_LABEL["Newey-West"] % key.split()[1]
    return SOUND_LABEL.get(key, key[0].upper() + key[1:])


# ------------------------------------------------------------------------------------------------------ daily CSV
def write_daily(path, R):
    d = R["daily"]
    out = pd.DataFrame(dict(date=d.date.dt.strftime("%Y-%m-%d"), ladder_12m_value_usd=k1000(d.old), ladder_3m_value_usd=k1000(d.new),
                            sleeve_value_usd=k1000(d.sleeve), collateral_usd=k1000(d.collateral)))
    out.to_csv(path, index=False, lineterminator="\n")
    return out


# ------------------------------------------------------------------------------------------------------ workbook
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


def _put(ws, r, vals, fmts=None, bold=False):
    for j, v in enumerate(vals, 1):
        c = ws.cell(row=r, column=j, value=v)
        f = (fmts or {}).get(j)
        if f:
            c.number_format = f
        if bold:
            c.font = Font(bold=True)
        if isinstance(v, str) and len(v) > 40:
            c.alignment = Alignment(wrap_text=True, vertical="top")


def _date(s):
    return pd.Timestamp(s).to_pydatetime()


def write_workbook(path, A, R, F):
    pol, at, alt, q, plan, pl = F["policy"], F["at_size"], F["alt_at_size"], F["quoted"], F["R10_plan"], F["plan"]
    size, size6 = F["R4_size_usd"], F["R5_alt_size_usd"]
    wb = openpyxl.Workbook()
    money, vol, dfmt, signed = "#,##0", "0.00", "mm/dd/yyyy", "#,##0;-#,##0"

    # 1. summary
    ws = wb.active
    ws.title = "Summary"
    _title(ws, "Volatility Premium Sleeve: 3-month ladder no larger than USD %s a point" % n(size),
           "Closes through %s. Dollars to the nearest thousand; sizes in multiples of USD 100 a point." % day(F["as_of"]))
    _head(ws, 4, ["Largest size inside both limits (Schedule D.4, D.5)", "Size (USD a point)", "Binds on", "Binding day",
                  "Sleeve collateral that day (USD)", "Collateral limit (USD)", "Worst calendar year", "Net settlements paid that year (USD)",
                  "Settlement limit (USD)"], [58, 14, 18, 13, 17, 15, 11, 18, 15])
    fm = {2: money, 4: dfmt, 5: money, 6: money, 8: money, 9: money}
    _put(ws, 5, ["3-month ladder beside the 12-month ladder", size, LIMIT_NAME[F["R4_binds"]["limit"]], _date(F["R4_binds"]["day"]), at["peak_usd"],
                 pol["collateral_limit_usd"], at["worst_year"], at["worst_usd"], pol["settlement_limit_usd"]], fm, bold=True)
    _put(ws, 6, ["6-month ladder instead", size6, LIMIT_NAME[F["R5_binds"]["limit"]], _date(F["R5_binds"]["day"]), alt["peak_usd"],
                 pol["collateral_limit_usd"], alt["worst_year"], alt["worst_usd"], pol["settlement_limit_usd"]], fm)
    _put(ws, 7, ["3-month ladder at the size quoted for (outside the collateral limit)", pol["quoted_size_usd"], "Breaches", _date(q["peak_day"]),
                 q["peak_usd"], pol["collateral_limit_usd"], q["worst_year"], q["worst_usd"], pol["settlement_limit_usd"]], fm)
    _head(ws, 9, ["On the record, January 2007 to %s, per USD %s a point" % (day(F["as_of"]), n(pol["per_usd"])), "Figure", "80% range, low", "80% range, high", "Note"])
    r6, r7 = F["R6_avg_range_12m"], F["R7_avg_range_3m"]
    rows = [("3-month ladder: average settlement per sale (USD)", F["R1_avg_3m_usd"], r7["low_usd"], r7["high_usd"],
             "%d expired swaps, %d of them on rebuilt strikes (sheet Rebuild check)" % (F["ladder_counts"]["settled"], F["ladder_counts"]["rebuilt"])),
            ("3-month ladder: worst calendar year, net paid (USD)", F["R2_worst_year_loss_usd"], None, None, "Calendar year %d" % F["R2_worst_year"]),
            ("12-month ladder: average settlement per sale (USD)", F["avg_12m"]["avg_per_sale_usd"], r6["low_usd"], r6["high_usd"],
             "%d expired swaps (sheet Average ranges)" % F["avg_12m"]["n"])]
    for i, row in enumerate(rows):
        _put(ws, 10 + i, list(row), {2: money, 3: money, 4: money})
    _put(ws, 13, ["12-month ladder at its USD %s a point: peak collateral (USD)" % n(pol["standing_size_usd"]), F["R3_old_peak_usd"], None, None,
                  "%s; %s on %s" % (day(F["R3_old_peak_day"]), n(F["old_peak_episodes"]["2008"]["peak_usd"]), day(F["old_peak_episodes"]["2008"]["day"]))],
         {2: money})
    _head(ws, 15, ["Cash plan %d at USD %s a point (Schedule D.7)" % (F["plan_year"], n(size)), "Figure", "80% range, low", "80% range, high", "Note"])
    o9 = F["R9_range"]
    cash = [("12-month ladder (USD)", plan["twelve_month_usd"], None, None,
             "%d open sale months and the %d sales still to come (sheet Plan 2027)" % (pl["open_sale_months"], pl["unsold_12m"])),
            ("  of which the open swaps that expire in %d: expected settlement (USD)" % F["plan_year"], F["R8_expected_usd"], o9["low_usd"], o9["high_usd"],
             "Valued at %s at the review close" % n(F["replay"]["mark_usd"])),
            ("3-month ladder (USD)", plan["three_month_usd"], None, None,
             "%d settlements, %s to %s" % (pl["new_3m"], day(F["new_calendar"]["first_expiry"], False), day(F["new_calendar"]["last_expiry_in_year"]))),
            ("Sleeve (USD)", plan["total_usd"], plan["low_usd"], plan["high_usd"], "All %d settlements together, from %s start dates" % (pl["settlements"], n(pl["start_dates"])))]
    for i, row in enumerate(cash):
        _put(ws, 16 + i, list(row), {2: money, 3: signed, 4: signed}, bold=(i == len(cash) - 1))
    _put(ws, 21, ["Value of the open swaps to the Sleeve at the %s close (USD)" % day(F["as_of"], False), F["book_value_usd"], None, None,
                  "%d confirmations in %d sale months (sheet Open swaps)" % (F["open_confirmations"], F["open_sale_months"])], {2: money})
    ws.freeze_panes = "A4"

    # 2. the plan
    ws = wb.create_sheet("Plan 2027")
    _title(ws, "Every settlement that falls in %d: USD %s expected" % (F["plan_year"], n(plan["total_usd"])),
           "Receipts fall in the calendar year of expiry (Schedule D.5(c)). Open swaps at their expected settlement (D.7(a)); swaps not yet sold "
           "at their ladder's average on the record (D.7(b)).")
    _head(ws, 4, ["Ladder", "Sale date", "Expiration", "Status at the review date", "Size (USD a point)", "Expected settlement (USD)"], [16, 13, 13, 26, 16, 20])
    r = 5
    for x in F["open_per_swap"]:
        _put(ws, r, ["12-month", _date(x["sale"]), _date(x["expiry"]), "Open", pol["standing_size_usd"], x["expected_usd"]], {2: dfmt, 3: dfmt, 5: money, 6: money})
        r += 1
    for s, e in zip(pl["unsold_sales"], pl["unsold_expiries"]):
        _put(ws, r, ["12-month", _date(s), _date(e), "Not yet sold", pol["standing_size_usd"], pl["avg_12m_per_sale_usd"]], {2: dfmt, 3: dfmt, 5: money, 6: money})
        r += 1
    _put(ws, r, ["12-month ladder", None, None, None, None, plan["twelve_month_usd"]], {6: money}, bold=True)
    r += 1
    for x in F["new_calendar"]["rows"]:
        if x["in_year"]:
            _put(ws, r, ["3-month", _date(x["sale"]), _date(x["expiry"]), "Not yet sold", size, F["new_calendar"]["per_settlement_usd"]],
                 {2: dfmt, 3: dfmt, 5: money, 6: money})
            r += 1
    _put(ws, r, ["3-month ladder", None, None, None, None, plan["three_month_usd"]], {6: money}, bold=True)
    _put(ws, r + 1, ["Sleeve", None, None, None, None, plan["total_usd"]], {6: money}, bold=True)
    _put(ws, r + 2, ["80% range, low", None, None, None, None, plan["low_usd"]], {6: signed})
    _put(ws, r + 3, ["80% range, high", None, None, None, None, plan["high_usd"]], {6: signed})
    ws.cell(row=r + 5, column=1, value="The range replays all %d settlements together from each of %s start dates, %s to %s: the open swaps over their "
            "remaining days, and each swap not yet sold struck and run the same number of days after the start date. Ladder totals are rounded "
            "from unrounded figures, so rows may differ from them by a thousand or two. The 3-month ladder's sales of October to December %d "
            "expire in %d." % (pl["settlements"], n(pl["start_dates"]), day(pl["first_start"]), day(pl["last_start"]), F["plan_year"], F["plan_year"] + 1)
            ).font = SMALL
    ws.freeze_panes = "A5"

    # 3. the open swaps
    ws = wb.create_sheet("Open swaps")
    _title(ws, "Open swaps at the %s close" % day(F["as_of"]),
           "Two confirmations of USD %s a point for each trade date. Value is to the Sleeve." % n(pol["confirmation_vega_usd"]))
    _head(ws, 4, ["Trade date", "Expiration", "Confirmations", "Vega notional (USD a point)", "Volatility strike", "Days elapsed", "Days remaining",
                  "Realized volatility to date", "Implied volatility, remaining term", "Value (USD)", "Expected settlement, %d expiries (USD)" % F["plan_year"]],
          [12, 12, 13, 14, 10, 9, 10, 12, 13, 13, 17])
    exp = {x["sale"]: x["expected_usd"] for x in F["open_per_swap"]}
    r = 5
    for o in F["open_swaps"]:
        _put(ws, r, [_date(o["sale"]), _date(o["expiry"]), 2, pol["standing_size_usd"], o["strike"], o["days_elapsed"], o["days_remaining"],
                     o["realized_vol"], o["implied_vol"], int(k1000(o["value_usd"])), exp.get(o["sale"])],
             {1: dfmt, 2: dfmt, 4: money, 5: vol, 8: vol, 9: vol, 10: money, 11: money})
        r += 1
    _put(ws, r, ["Total", None, F["open_confirmations"], None, None, None, None, None, None, F["book_value_usd"], F["R8_expected_usd"]],
         {10: money, 11: money}, bold=True)
    ws.freeze_panes = "A5"

    # 4. the ladders on the record
    ws = wb.create_sheet("Ladders on record")
    _title(ws, "Each ladder on the record, per USD %s a point per monthly sale" % n(pol["per_usd"]),
           "Net settlements by calendar year of expiry (USD; negative is paid). Sale dates from January 2007; swaps expired by %s." % day(F["as_of"]))
    _head(ws, 4, ["Calendar year", "3-month ladder", "6-month ladder", "12-month ladder"], [34, 16, 16, 16])
    L = F["ladders_per_100k"]
    years = sorted({int(y) for m in L.values() for y in m["by_year"]})
    r = 5
    for y in years:
        _put(ws, r, [y] + [L[m]["by_year"].get(str(y)) for m in ("3", "6", "12")], {2: signed, 3: signed, 4: signed})
        r += 1
    r += 1
    for label, key, f in (("Average settlement per sale (USD)", "avg_per_sale_usd", money), ("Swaps expired", "settled", "0"),
                          ("of which on rebuilt strikes", "rebuilt", "0"), ("Worst calendar year", "worst_year", "0"),
                          ("Net paid in the worst year (USD)", "worst_year_loss_usd", money)):
        _put(ws, r, [label] + [L[m][key] for m in ("3", "6", "12")], {2: f, 3: f, 4: f}, bold=(key in ("avg_per_sale_usd", "worst_year_loss_usd")))
        r += 1
    ws.freeze_panes = "B5"

    # 5. how well the record pins each average
    ws = wb.create_sheet("Average ranges")
    _title(ws, "The 80%% range of each ladder's average settlement per sale, per USD %s a point" % n(pol["per_usd"]),
           "Sales a month apart share most of their days: the correlation between one sale's settlement and the next is %.2f for the 12-month "
           "ladder and %.2f for the 3-month ladder." % (F["avg_12m"]["next_sale_correlation"], F["avg_3m"]["next_sale_correlation"]))
    _head(ws, 4, ["Method", "12-month ladder, low", "12-month ladder, high", "3-month ladder, low", "3-month ladder, high"], [62, 16, 16, 16, 16])
    a12, a3 = F["avg_12m"], F["avg_3m"]
    _put(ws, 5, ["Used: record resampled in blocks of consecutive sales twice the swap's life (%d and %d sales)" % (a12["block_sales"], a3["block_sales"]),
                 r6["low_usd"], r6["high_usd"], r7["low_usd"], r7["high_usd"]], {2: money, 3: money, 4: money, 5: money}, bold=True)
    r = 6
    for k12, k3 in zip(a12["sound"], a3["sound"]):
        lab = method_label(k12) if k12 == k3 else "%s (%s for the 3-month ladder)" % (method_label(k12), k3.split()[3 if k3.startswith("circular") else 1])
        _put(ws, r, [lab, a12["sound"][k12]["low_usd"], a12["sound"][k12]["high_usd"], a3["sound"][k3]["low_usd"], a3["sound"][k3]["high_usd"]],
             {2: money, 3: money, 4: money, 5: money})
        r += 1
    iid12, iid3 = a12["hurried"]["single settlements resampled"], a3["hurried"]["single settlements resampled"]
    _put(ws, r + 1, ["Not used: settlements resampled one at a time, as if unrelated", iid12["low_usd"], iid12["high_usd"], iid3["low_usd"], iid3["high_usd"]],
         {2: money, 3: money, 4: money, 5: money})
    few12, few3 = a12["hurried"]["a standard error with too few lags"], a3["hurried"]["a standard error with too few lags"]
    _put(ws, r + 2, ["Not used: a standard error allowing for fewer lags than the months neighboring swaps share (%d and %d lags)" % (a12["few_lags"], a3["few_lags"]),
                     few12["low_usd"], few12["high_usd"], few3["low_usd"], few3["high_usd"]], {2: money, 3: money, 4: money, 5: money})
    _put(ws, r + 4, ["Average settlement per sale (USD)", a12["avg_per_sale_usd"], None, a3["avg_per_sale_usd"], None], {2: money, 4: money})
    _put(ws, r + 5, ["Swaps expired", a12["n"], None, a3["n"], None], {2: "0", 4: "0"})
    ws.freeze_panes = "A5"

    # 6. the sizing
    ws = wb.create_sheet("Sizing")
    _title(ws, "Room beside the 12-month ladder on the binding day, %s" % day(F["R4_binds"]["day"]),
           "Every ladder sold at its size on every monthly sale date of the record (Schedule D.5(b)); collateral is the open swaps valued together.")
    _head(ws, 4, ["", "3-month ladder", "6-month ladder"], [72, 16, 16])
    rows = [("Collateral limit, %.1f%% of net assets of USD %s million (USD)" % (pol["collateral_limit_pct"], "{:,.1f}".format(pol["reference_assets_usd_m"])),
             pol["collateral_limit_usd"], pol["collateral_limit_usd"], money),
            ("12-month ladder at USD %s a point, value against the Sleeve that day (USD)" % n(pol["standing_size_usd"]), at["old_at_peak_usd"],
             alt["old_at_peak_usd"], money),
            ("Room for the new ladder (USD)", at["room_usd"], at["room_usd"], money),
            ("New ladder, value against the Sleeve that day per USD 100,000 a point (USD)", at["new_per_100k_at_peak_usd"], alt["new_per_100k_at_peak_usd"], money),
            ("Largest size, in multiples of USD 100 (USD a point)", size, size6, money),
            ("Sleeve collateral that day at the size (USD)", at["peak_usd"], alt["peak_usd"], money),
            ("Settlement limit, %.1f%% of net assets (USD)" % pol["settlement_limit_pct"], pol["settlement_limit_usd"], pol["settlement_limit_usd"], money),
            ("Worst calendar year for the Sleeve at the size", at["worst_year"], alt["worst_year"], "0"),
            ("Net settlements paid that year (USD)", at["worst_usd"], alt["worst_usd"], money)]
    for i, (a, b, c, f) in enumerate(rows):
        _put(ws, 5 + i, [a, b, c], {2: f, 3: f}, bold=(i == 4))
    ws.cell(row=15, column=1, value="The settlement limit on its own would allow USD %s a point for the 3-month ladder." % n(F["R4_hurried"]["the settlement limit alone"])).font = SMALL

    # 7. the routes
    ws = wb.create_sheet("Routes")
    _title(ws, "What each shorter route gives", "The first row is the figure used; the others are shown so the difference can be traced.")
    _head(ws, 4, ["Route", "Largest 3-month size (USD a point)", "Sleeve plan, %d (USD)" % F["plan_year"]], [86, 18, 18])
    for i, x in enumerate(F["routes"]):
        name = ("As used: strikes rebuilt from both neighboring maturities, swaps valued on the remaining term under the cap, both ladders together, "
                "expected settlement from the record") if i == 0 else x["route"][0].upper() + x["route"][1:]
        _put(ws, 5 + i, [name, x["size_usd"], x["plan_usd"]], {2: money, 3: money}, bold=(i == 0))

    # 8. the rebuild
    ws = wb.create_sheet("Rebuild check")
    rb = F["rebuild"]
    _title(ws, "3-month strikes before the index's first close in the folder (%s)" % day(rb["first_published"]),
           "Least squares of the 3-month index on the 30-day index and the next longer published index, over the days all are published.")
    _head(ws, 4, ["Check on the overlap", "Both neighbors", "30-day index alone"], [58, 14, 16, 16, 16])
    chk = [("Days all three indices are published", rb["overlap_days"], None, "#,##0"),
           ("Root mean squared error, volatility points", rb["rmse"], rb["proxy_rmse"], vol),
           ("Days the 30-day index closed above %d" % pol["hot_level"], rb["hot_days"], None, "0"),
           ("Root mean squared error on those days", rb["rmse_hot"], rb["proxy_rmse_hot"], vol),
           ("Average error on those days (points too high)", None, rb["proxy_bias_hot"], "0.0"),
           ("R-squared of the 30-day index alone", None, rb["proxy_r2"], vol),
           ("3-month index above the 30-day index, average (%)", rb["ratio_all_pct"], None, "0.0"),
           ("3-month index below the 30-day index on those days (%)", rb["ratio_hot_pct"], None, "0.0")]
    for i, (a, b, c, f) in enumerate(chk):
        _put(ws, 5 + i, [a, b, c], {2: f, 3: f})
    r = 14
    _head(ws, r, ["Sale date", "30-day index", "Longer index", "Its close", "Rebuilt 3-month strike"])
    t = A.ladder(P.NEW_MAT).t
    for s in t[t.how == "rebuilt"].itertuples():
        r += 1
        hi = "VIX6M" if not np.isnan(A.mk.idx.at[s.sale, "VIX6M"]) else "VIX1Y"
        _put(ws, r, [s.sale.to_pydatetime(), float(A.mk.idx.at[s.sale, "VIX"]), {"VIX6M": "6-month", "VIX1Y": "1-year"}[hi], float(A.mk.idx.at[s.sale, hi]),
                     round(float(s.k), 2)], {1: dfmt, 2: vol, 4: vol, 5: vol})
    ws.freeze_panes = "A5"

    # 9. notes
    ws = wb.create_sheet("Notes")
    _title(ws, "Basis")
    ws.column_dimensions["A"].width = 132
    notes = [
        "As of the close of %s; S&P 500 and Cboe volatility index closes as published. Reference Assets are the audited net assets at June 30, 2026." % day(F["as_of"]),
        "Realized volatility, the cap and the settlement amount follow the Amended and Restated Master Confirmation; a settlement falls in the calendar year "
        "of its expiration (Schedule D.5(c)).",
        "Open swaps are valued on the basis the dealers' statements show: variance realized to date and the variance implied for the remaining term, weighted "
        "by days, capped as the credit support annexes cap exposure. Implied volatility between published maturities is read in total variance. No "
        "discounting (Schedule D.5(e)).",
        "The record is every monthly sale date from January 2007, whether or not a ladder's index was yet published (Schedule D.5(b)). The 3-month index "
        "file begins on %s and the 6-month on %s; earlier strikes are rebuilt (sheet Rebuild check)." % (day(rb["first_published"]), day(rb["six_month_first"])),
        "The blotter's superseded %s ticket and the original of the confirmation novated in %s are not counted; the dealers' daily files "
        "are used to confirm the valuation basis and are not an input to any figure." % (F["blotter"]["amended_month"], F["blotter"]["novation_month"]),
        "Expected settlement of the open swaps is the average over the record's start dates of what the same swaps would have paid, with realized variance "
        "taken as a share of the variance implied on the start date for the same remaining term (Schedule D.7(a), (c)).",
        "Ranges of an average (Schedule D.7(d)) resample the record in blocks of consecutive sales; the plan's range (Schedule D.7(e)) is the 10th and 90th "
        "percentiles of the plan year's settlements taken together from each start date.",
    ]
    for i, text in enumerate(notes):
        c = ws.cell(row=3 + i, column=1, value=text)
        c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(path)
    created, modified = STAMPS[BOOK]
    PP.normalize_ooxml(path, AUTHOR, AUTHOR, created, modified, excel=True, company=P.FOUNDATION)


# ------------------------------------------------------------------------------------------------------ chart
def write_chart(path, R, F):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.dates as mdates
    import matplotlib.pyplot as plt
    d = R["daily"]
    lim = P.LIM_COLL / 1e6
    size = F["R4_size_usd"]
    fig, ax = plt.subplots(figsize=(6.6, 3.7), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")
    ax.plot(d.date, d.collateral / 1e6, color=BLUE, lw=1.3, solid_joinstyle="round", label="Sleeve with the 3-month ladder at USD %s a point" % n(size), zorder=3)
    ax.plot(d.date, np.maximum(0.0, -d.old) / 1e6, color=ORANGE, lw=1.3, solid_joinstyle="round",
            label="12-month ladder alone at USD %s a point" % n(P.OLD_SIZE), zorder=4)
    ax.axhline(lim, color=INK2, lw=0.9, ls=(0, (5, 3)), zorder=2)
    ax.annotate("Collateral limit, USD %.1f million" % lim, (pd.Timestamp("2026-06-30"), lim), textcoords="offset points", xytext=(0, 4), ha="right",
                fontsize=8, color=INK2)
    pk = pd.Timestamp(F["at_size"]["peak_day"])
    ax.annotate("%s: USD %.1f million" % (pk.strftime("%b %-d, %Y"), F["at_size"]["peak_usd"] / 1e6), (pk, F["at_size"]["peak_usd"] / 1e6),
                textcoords="offset points", xytext=(10, -12), ha="left", fontsize=8, color=INK)
    p20 = pd.Timestamp(F["R3_old_peak_day"])
    v20 = float(d.loc[d.date == p20, "collateral"].iloc[0]) / 1e6
    ax.annotate("%s: USD %.1f million" % (p20.strftime("%b %-d, %Y"), v20), (p20, v20), textcoords="offset points", xytext=(8, -4), ha="left",
                fontsize=8, color=INK)
    ax.set_ylim(0, 50)
    ax.set_yticks([0, 10, 20, 30, 40, 50])
    ax.set_xlim(pd.Timestamp("2007-01-01"), pd.Timestamp("2026-12-31"))
    ax.xaxis.set_major_locator(mdates.YearLocator(3))
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.grid(axis="y", color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color(GRID)
    ax.tick_params(colors=INK2, length=0, labelsize=8)
    ax.set_ylabel("Collateral posted, USD million", color=INK2, fontsize=8)
    ax.set_title("At USD %s a point the sleeve reaches the collateral limit once, on %s" % (n(size), day(F["at_size"]["peak_day"])),
                 loc="left", fontsize=9.5, color=INK, pad=10)
    leg = ax.legend(loc="center", bbox_to_anchor=(0.41, 0.60), frameon=False, fontsize=8, handlelength=2.2)
    for t in leg.get_texts():
        t.set_color(INK2)
    fig.tight_layout()
    fig.savefig(path, dpi=200, metadata={"Software": None})
    plt.close(fig)


# ------------------------------------------------------------------------------------------------------ memo
def memo_paragraphs(F):
    """The memo's prose, built from the figures (the checks read it too, so the words and the numbers cannot part)."""
    pol, at, q, h, own, rb, rp = F["policy"], F["at_size"], F["quoted"], F["hurried"], F["own_history"], F["rebuild"], F["replay"]
    plan, pl, cal = F["R10_plan"], F["plan"], F["new_calendar"]
    size, size6 = F["R4_size_usd"], F["R5_alt_size_usd"]
    r6, r7, a12, a3 = F["R6_avg_range_12m"], F["R7_avg_range_3m"], F["avg_12m"], F["avg_3m"]
    iid12, iid3 = a12["hurried"]["single settlements resampled"], a3["hurried"]["single settlements resampled"]
    p = {}
    p["title"] = "3-month ladder: no more than USD %s a point; the USD %s quoted for would have breached the collateral limit in November 2008" % (
        n(size), n(pol["quoted_size_usd"]))
    p["call"] = ("Confirm the 3-month ladder to the panel at USD %s a point per monthly sale. That is the largest size, in the USD 100 steps of Schedule "
                 "D.2(a), at which the Sleeve stays inside both Schedule D.4 limits on the record. With the 12-month ladder at its USD %s beside it, "
                 "collateral would have peaked at USD %s on %s, against the limit of USD %s (%.1f%% of the USD %s million of net assets at June 30). "
                 "The settlement limit is not the constraint: the worst calendar year is %d, with USD %s paid against USD %s. For the %d cash plan "
                 "carry USD %s from the Sleeve at that size, and plan for a year that lands anywhere from a net payment of USD %s to receipts of "
                 "USD %s four times in five."
                 % (n(size), n(pol["standing_size_usd"]), n(at["peak_usd"]), day(at["peak_day"]), n(pol["collateral_limit_usd"]),
                    pol["collateral_limit_pct"], "{:,.1f}".format(pol["reference_assets_usd_m"]), at["worst_year"], n(at["worst_usd"]),
                    n(pol["settlement_limit_usd"]), F["plan_year"], n(plan["total_usd"]), n(pl["low_paid_usd"]), n(plan["high_usd"])))
    p["reject"] = ("The USD %s the dealers quoted for does not fit: on the same day the Sleeve would have posted USD %s, USD %s over the limit. The "
                   "size turns on 2008, and the 3-month index file begins on %s. Schedule D.5(b) keeps every monthly sale date from January 2007 in "
                   "the record whether or not the index was yet published, so the %d strikes before that date have to be rebuilt. I rebuilt them "
                   "from the two published maturities either side of three months (the 30-day index and the 6-month index, or the 1-year index "
                   "before the 6-month index begins in January 2008), fitted on the %s days all are published; the fit is off by %.2f points on "
                   "average and by %.2f on the %d days the 30-day index closed above %d, which are the days that decide this. The 30-day index "
                   "alone looks like a good stand-in and is not: it explains %.2f of the 3-month index's variation over the same days, but the "
                   "3-month index runs %.1f%% above the 30-day index on average and %.1f%% below it on those stressed days, so the stand-in is %.1f "
                   "points too high exactly where the limit is set. Strikes that are too high make 2008 look milder, and the size comes out at USD "
                   "%s, at which the Sleeve would have posted USD %s on %s. Leaving the early sale dates out altogether gives USD %s."
                   % (n(pol["quoted_size_usd"]), n(q["peak_usd"]), n(q["over_usd"]), day(rb["first_published"]), F["ladder_counts"]["rebuilt"],
                      n(rb["overlap_days"]), rb["rmse"], rb["rmse_hot"], rb["hot_days"], pol["hot_level"], rb["proxy_r2"], rb["ratio_all_pct"],
                      rb["ratio_hot_pct"], rb["proxy_bias_hot"], n(h["size_usd"]), n(h["peak_on_record_usd"]), day(h["peak_day"]), n(own["size_usd"])))
    p["alt"] = "A 6-month ladder instead could be no larger than USD %s a point, bound by the same limit on the same day." % n(size6)
    p["caption"] = "Collateral the Sleeve would have posted on each day of the record, January 2007 to %s." % day(F["as_of"])
    p["cash"] = ("The %d plan is every settlement that falls in the year, %d in all. The 12-month ladder brings USD %s: the %d open sale months "
                 "that expire in %d, expected to settle at USD %s, and its November and December 2026 sales, which are not yet made and expire in "
                 "November and December %d, at the ladder's average of USD %s a sale (Schedule D.7(b)). The 3-month ladder brings USD %s: its "
                 "first sale is %s, and only the %d sales to %s expire inside the year, at the record's average of USD %s a sale per USD %s a "
                 "point. The open swaps' figure is not their value. They are valued at USD %s at the %s close, but a value is a price. Taking "
                 "each of the record's %s start dates since January 2007 and letting the S&P 500 run from there over each swap's remaining days, "
                 "the same swaps would have gone on to pay more than that value from %d%% of start dates, USD %s on average (Schedule D.7(a) and "
                 "(c)), and between USD %s and USD %s four times in five."
                 % (F["plan_year"], pl["settlements"], n(plan["twelve_month_usd"]), pl["open_sale_months"], F["plan_year"], n(F["R8_expected_usd"]),
                    F["plan_year"], n(pl["avg_12m_per_sale_usd"]), n(plan["three_month_usd"]), day(cal["first_sale"]), pl["new_3m"],
                    day(cal["last_sale_settling_in_year"], False), n(F["R1_avg_3m_usd"]), n(pol["per_usd"]), n(rp["mark_usd"]), day(F["as_of"], False),
                    n(rp["start_dates"]), rp["share_above_mark_pct"], n(F["R8_expected_usd"]), n(F["R9_range"]["low_usd"]), n(F["R9_range"]["high_usd"])))
    p["range"] = ("The year as a whole is much less certain than its parts suggest, because a bad stretch hits the open swaps and the new sales "
                  "together. Replaying all %d settlements from the same start dates (%s of them, the last on %s), the plan lands between a net "
                  "payment of USD %s and receipts of USD %s four times in five, and below zero from %d%% of start dates; the worst start date, "
                  "%s, would have cost USD %s."
                  % (pl["settlements"], n(pl["start_dates"]), day(pl["last_start"]), n(pl["low_paid_usd"]), n(plan["high_usd"]),
                     pl["share_below_zero_pct"], day(pl["worst_start"]), n(pl["worst_usd"])))
    p["averages"] = ("Nor does the record pin either ladder's average tightly. Sales a month apart share most of their days (the correlation "
                     "between one sale's settlement and the next is %.2f for the 12-month ladder and %.2f for the 3-month), so %d and %d expired "
                     "swaps are far fewer independent observations. Resampling the record in blocks of consecutive sales, the 12-month ladder's "
                     "average of USD %s per USD %s a point lies between USD %s and USD %s four times in five, and the 3-month ladder's USD %s "
                     "between USD %s and USD %s (Schedule D.7(d)). Treated as unrelated, the same settlements would give USD %s to USD %s and "
                     "USD %s to USD %s, which is too narrow."
                     % (a12["next_sale_correlation"], a3["next_sale_correlation"], a12["n"], a3["n"], n(a12["avg_per_sale_usd"]), n(pol["per_usd"]),
                        n(r6["low_usd"]), n(r6["high_usd"]), n(F["R1_avg_3m_usd"]), n(r7["low_usd"]), n(r7["high_usd"]), n(iid12["low_usd"]),
                        n(iid12["high_usd"]), n(iid3["low_usd"]), n(iid3["high_usd"])))
    p["record"] = ("On the record the 3-month ladder's worst calendar year is %d, a loss of USD %s per USD %s a point. The 12-month ladder at its "
                   "USD %s would have needed USD %s of collateral at its peak (%s, with %s at USD %s), which leaves the new ladder USD %s of room "
                   "on the binding day. At the %s close the open book, %d confirmations in %d sale months, is worth USD %s to the Sleeve."
                   % (F["R2_worst_year"], n(F["R2_worst_year_loss_usd"]), n(pol["per_usd"]), n(pol["standing_size_usd"]), n(F["R3_old_peak_usd"]),
                      day(F["R3_old_peak_day"]), day(F["old_peak_episodes"]["2008"]["day"]), n(F["old_peak_episodes"]["2008"]["peak_usd"]),
                      n(at["room_usd"]), day(F["as_of"], False), F["open_confirmations"], F["open_sale_months"], n(F["book_value_usd"])))
    p["source"] = ("Source: blotter, dealer statements and custodian files; S&P 500 and Cboe volatility index closes through %s. Workings in %s; "
                   "daily collateral in %s." % (day(F["as_of"]), BOOK, DAILY))
    p["plan_rows"] = [("12-month ladder", plan["twelve_month_usd"], None, None),
                      ("of which the open swaps that expire in %d" % F["plan_year"], F["R8_expected_usd"], F["R9_range"]["low_usd"], F["R9_range"]["high_usd"]),
                      ("3-month ladder at USD %s a point" % n(size), plan["three_month_usd"], None, None),
                      ("Sleeve", plan["total_usd"], plan["low_usd"], plan["high_usd"])]
    p["notes"] = [
        "Open swaps are valued on the basis the dealers' statements show (variance realized to date and the variance implied for the remaining term, "
        "weighted by days, with the cap), read from the published term structure. No discounting (Schedule D.5(e)).",
        "The blotter's %s Altamere ticket booked at USD %s was superseded the next morning at USD %s, and the %s Wexcombe confirmation was "
        "novated to Brecon Sound in %s; both swaps have since expired and each is counted once."
        % (F["blotter"]["amended_month"], n(F["blotter"]["amended_wrong_vega_usd"]), n(pol["confirmation_vega_usd"]), F["blotter"]["novated_month"],
           F["blotter"]["novation_month"]),
    ]
    return p


def write_memo(path, F, png):
    p_ = memo_paragraphs(F)
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Mm(215.9), Mm(279.4)
    sec.left_margin = sec.right_margin = Mm(24)
    sec.top_margin, sec.bottom_margin = Mm(21), Mm(19)
    st = doc.styles["Normal"]
    st.font.name = "Calibri"
    st.font.size = Pt(10)
    hp = sec.header.paragraphs[0]
    hp.text = "%s | Treasury" % P.FOUNDATION
    hp.runs[0].font.size = Pt(8)
    hp.runs[0].font.color.rgb = RGBColor(0x52, 0x51, 0x4E)
    t = doc.add_paragraph()
    r = t.add_run(p_["title"])
    r.bold = True
    r.font.size = Pt(13)
    for k, v in (("To", "%s, Director of Treasury" % P.TREASURY), ("Cc", "%s, Chief Investment Officer" % P.CIO), ("From", "Treasury Analysis"),
                 ("Date", "November 10, 2026"), ("Re", "Size of the new variance swap ladder and the Sleeve's line in the %d cash plan" % F["plan_year"])):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(0)
        a = p.add_run("%s: " % k)
        a.bold = True
        p.add_run(v)
    doc.add_paragraph()
    for key in ("call", "reject", "alt"):
        p = doc.add_paragraph(p_[key])
        p.paragraph_format.space_after = Pt(6)
    doc.add_picture(png, width=Mm(122))
    doc.paragraphs[-1].paragraph_format.keep_with_next = True
    c = doc.add_paragraph(p_["caption"])
    c.runs[0].font.size = Pt(8.5)
    c.runs[0].italic = True
    p = doc.add_paragraph(p_["cash"])
    p.paragraph_format.space_after = Pt(6)
    tb = doc.add_table(rows=1, cols=4)
    tb.style = "Light Grid Accent 1"
    tb.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, h in enumerate(["Cash plan %d (USD)" % F["plan_year"], "Expected", "80% range, low", "80% range, high"]):
        tb.rows[0].cells[j].text = h
    for label, exp_, lo, hi in p_["plan_rows"]:
        cells = tb.add_row().cells
        cells[0].text = label
        cells[1].text = n(exp_)
        cells[2].text = n(lo) if lo is not None else ""
        cells[3].text = n(hi) if hi is not None else ""
    for row in tb.rows:
        for cell in row.cells:
            for par in cell.paragraphs:
                for run in par.runs:
                    run.font.size = Pt(9)
    s = doc.add_paragraph(p_["source"])
    s.runs[0].font.size = Pt(8.5)
    for key in ("range", "averages", "record"):
        p = doc.add_paragraph(p_[key])
        p.paragraph_format.space_after = Pt(6)
    for i, note in enumerate(p_["notes"], 1):
        q = doc.add_paragraph("%d. %s" % (i, note))
        q.runs[0].font.size = Pt(8.5)
        q.paragraph_format.space_after = Pt(2)
    doc.save(path)
    created, modified = STAMPS[MEMO]
    PP.normalize_docx(path, AUTHOR, AUTHOR, created, modified, 7, 126, "task9-sleeve-memo", title="3-month ladder size and the 2027 cash plan",
                      company=P.FOUNDATION)


def write_all(A, R, F, golden_dir, scratch):
    os.makedirs(golden_dir, exist_ok=True)
    for f in os.listdir(golden_dir):
        os.remove(os.path.join(golden_dir, f))
    png = os.path.join(scratch, "sleeve_collateral.png")
    write_chart(png, R, F)
    write_daily(os.path.join(golden_dir, DAILY), R)
    write_workbook(os.path.join(golden_dir, BOOK), A, R, F)
    write_memo(os.path.join(golden_dir, MEMO), F, png)
    PP.own_mtimes(golden_dir, {DAILY: CSV_TIME})
    return png
