"""The liquidity standard's stress year (2022 replayed on 2027) for a given set of process models.

Inputs are the opening state at 31 December 2026 and 2022's records; the process models (the desk, NEX's rate rule,
the plants, the customers) are passed in, so the same code runs the world's truth (sim.py) and the golden read from
the pack (analysis.py), and each hurried route by swapping one model."""
import datetime as dt
import math
import numpy as np
import common as C
from common import mi, mi_date


def corresponding_2022(c, bdays22):
    """the same date in 2022, or the latest 2022 business day before it."""
    c22 = dt.date(2022, c.month, min(c.day, 28) if c.month == 2 else c.day)
    while c22 not in bdays22:
        c22 -= dt.timedelta(days=1)
    return c22


def stress_prices(open_curve, curves22, spot22, bdays22_sorted, year=2027):
    """replayed curves on the stress year's business days and spot on every calendar day."""
    bset = set(bdays22_sorted)
    days = C.business_days(year, year)
    prev = max(d for d in curves22 if d.year == 2021)  # the last business day before the stress year starts
    F = dict(open_curve)
    curves = []
    for d in days:
        c22 = corresponding_2022(d, bset)
        k_now = mi(d.year, d.month)
        newF = {}
        for k, f in F.items():
            if k < k_now:
                continue
            k22 = k - 12 * (year - 2022)
            a, b = curves22[c22], curves22[prev]
            newF[k] = f * a[k22] / b[k22] if (k22 in a and k22 in b) else f
        F = newF
        curves.append(dict(F))
        prev = c22
    spot = {}
    c = dt.date(year, 1, 1)
    bi = -1
    while c.year == year:
        while bi + 1 < len(days) and days[bi + 1] <= c:
            bi += 1
        cur = curves[bi] if bi >= 0 else open_curve
        nxt = mi(c.year, c.month) + 1
        c22 = dt.date(2022, c.month, min(c.day, 28) if c.month == 2 else c.day)
        b22 = corresponding_2022(c22, bset)
        spot[c] = cur[nxt] * spot22[c22] / curves22[b22][mi(2022, c.month) + 1]
        c += dt.timedelta(days=1)
    return days, curves, spot


def stress_inflows(normal_by_week, inflow22_by_isoweek, normal22_by_isoweek, year=2027):
    """each week's inflow: the normal for that week times 2022's inflow over its normal for the same ISO week."""
    weeks, d = [], dt.date.fromisocalendar(year, 1, 1)
    while d.year == year:
        weeks.append(d)
        d += dt.timedelta(days=7)
    out = []
    for w in weeks:
        n = w.isocalendar()[1]
        out.append(normal_by_week(n) * inflow22_by_isoweek[n] / normal22_by_isoweek[n])
    return weeks, np.array(out)


def run(state, prices, models, year=2027):
    """state: opening book, rates and rule window, last prices, reservoir, receivables, budgets.
    prices: (days, curves, spot) from stress_prices. models: desk, rates, output, supply.
    Returns the cumulative net cash path and its parts."""
    days, curves, spot = prices
    spot_all = dict(state["spot_hist"])
    spot_all.update(spot)
    rates = models["rates"](days, curves, state)
    desk = models["desk"](days, curves, state)
    res = C.run_book(days, curves, spot_all, rates, state["mw"], desk, state.get("f_last"), state["open_curve"])
    dim = np.diff(np.concatenate([[state["im0"]], res["im"]]))
    out_day, com_day, invoices = models["supply"](days, curves, spot_all, state)
    da = C.dayahead_cash(days, out_day, com_day, spot_all)
    rec = C.receipts_cash(days, invoices)
    flow = res["vm"] + res["dlv"] + dim - da - rec
    c = np.cumsum(flow)
    j = int(np.argmax(c))
    return dict(days=days, cum=c, peak=float(c[j]), peak_day=days[j], j=j, vm=res["vm"], dlv=res["dlv"], dim=dim,
                im=res["im"], da=da, rec=rec, book=res, rates=rates, out_day=out_day)


def book_twh(mw_by_day, j, years):
    mw = mw_by_day[j]
    out = {}
    for y in years:
        out[y] = -sum(mw.get(k, 0.0) * C.month_hours(k) for k in C.year_months(y)) / 1e6
    return out
