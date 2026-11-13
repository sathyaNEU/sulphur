"""Shared calendar, contract and cash mechanics for task20 (Hallingvass Kraft's margin facility).

Used by sim.py (the world) and analysis.py (the golden, read from target/ only). Nothing here knows the world's
hidden parameters: the clearing house's rule, the desk's rule, the plants' operation and the customers' formulas are
passed in by the caller."""
import datetime as dt
import math
import numpy as np

Y0 = 2017
HOL_FIXED = [(1, 1), (5, 1), (5, 17), (12, 24), (12, 25), (12, 26), (12, 31)]


def easter(y):
    a = y % 19; b = y // 100; c = y % 100; d = b // 4; e = b % 4; f = (b + 8) // 25; g = (b - f + 1) // 3
    h = (19 * a + b - d - g + 15) % 30; i = c // 4; k = c % 4; l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 22 * l) // 451; mo = (h + l - 7 * m + 114) // 31; da = ((h + l - 7 * m + 114) % 31) + 1
    return dt.date(y, mo, da)


def holidays(y):
    e = easter(y)
    s = {dt.date(y, m, d) for m, d in HOL_FIXED}
    for off in (-3, -2, 1, 39, 50):
        s.add(e + dt.timedelta(days=off))
    return s


def business_days(y0, y1):
    hol = set()
    for y in range(y0, y1 + 1):
        hol |= holidays(y)
    out, d = [], dt.date(y0, 1, 1)
    while d <= dt.date(y1, 12, 31):
        if d.weekday() < 5 and d not in hol:
            out.append(d)
        d += dt.timedelta(days=1)
    return out


def is_bday(d):
    return d.weekday() < 5 and d not in holidays(d.year)


def next_bday(d):
    d = d + dt.timedelta(days=1)
    while not is_bday(d):
        d += dt.timedelta(days=1)
    return d


def prev_bday(d):
    d = d - dt.timedelta(days=1)
    while not is_bday(d):
        d -= dt.timedelta(days=1)
    return d


def mi(y, m):
    return (y - Y0) * 12 + (m - 1)


def mi_date(k):
    return dt.date(Y0 + k // 12, k % 12 + 1, 1)


def month_days(k):
    return (mi_date(k + 1) - mi_date(k)).days


def month_hours(k):
    return month_days(k) * 24


def hours_year(y):
    return sum(month_hours(mi(y, m)) for m in range(1, 13))


def year_months(y):
    return [mi(y, m) for m in range(1, 13)]


def cprice(curve, ks):
    hrs = np.array([month_hours(k) for k in ks], float)
    return float((hrs * np.array([curve[k] for k in ks])).sum() / hrs.sum())


def margin_class(k, d):
    """the clearing class a delivery month sits in on day d after cascades: Y before its year, Q before its quarter,
    M from its quarter's start to the end of its delivery."""
    s = mi_date(k)
    if s.year > d.year:
        return "Y"
    if d <= prev_bday(dt.date(s.year, 3 * ((s.month - 1) // 3) + 1, 1)):
        return "Q"
    return "M"


def front_months(d):
    """delivery months of the front month, quarter and year contracts listed on day d."""
    k0 = mi(d.year, d.month)
    q0 = (d.month - 1) // 3
    fq0 = mi(d.year, q0 * 3 + 1) + 3
    return {"M": [k0 + 1], "Q": [fq0, fq0 + 1, fq0 + 2], "Y": year_months(d.year + 1)}


# ---------------------------------------------------------------------------------------------------- margin rule
def rule_rates(days, ref_px, ref_ret, look, q, band, review_wd=3, start=None, hist_two=None, last1=None,
               method="linear"):
    """NEX's rate for each class: front price times the q-quantile of |two-day log return| over `look` days;
    reviewed on `review_wd`, a new rate (effective next business day) only when the indicated rate is more than `band`
    away from the rate in force. hist_two: earlier two-day returns to seed the window."""
    rates, notices = {}, []
    for t in ("M", "Q", "Y"):
        two = list(hist_two[t]) if hist_two else []
        cur = start[t] if start else None
        pend = None
        ser = []
        r = ref_ret[t]
        for i, d in enumerate(days):
            if pend is not None:
                cur = pend
                pend = None
                notices.append((d, t, cur))
            prev = r[i - 1] if i > 0 else (last1[t] if last1 else 0.0)
            two.append(r[i] + prev)
            win = np.abs(np.array(two[-look:]))
            ind = ref_px[t][i] * float(np.quantile(win, q, method=method))
            if (cur is None or cur <= 0) and ind > 0:
                cur = round(ind, 2)
                notices.append((d, t, cur))
            if cur and (review_wd is None or d.weekday() == review_wd) and abs(ind / cur - 1) > band:
                pend = round(ind, 2)
            ser.append(cur or 0.0)
        rates[t] = np.array(ser)
        rates[t + "_two"] = two
        rates[t + "_last1"] = float(r[-1])
    return rates, notices


def ref_series(days, curves, prev_curve=None, decimals=3):
    """front contract settlement price (as published, rounded) and the same contract's daily log return."""
    px = {t: np.zeros(len(days)) for t in "MQY"}
    ret = {t: np.zeros(len(days)) for t in "MQY"}
    for i, d in enumerate(days):
        fm = front_months(d)
        pc = curves[i - 1] if i > 0 else prev_curve
        for t in "MQY":
            p = round(cprice(curves[i], fm[t]), decimals)
            px[t][i] = p
            if pc is not None and all(k in pc for k in fm[t]):
                ret[t][i] = math.log(p / round(cprice(pc, fm[t]), decimals))
    return px, ret


# ---------------------------------------------------------------------------------------------------- the book
def run_book(days, curves, spot_cd, rates, mw0, desk=None, f_last0=None, prev_curve=None):
    """Clearing cash day by day for a book held per delivery month (MW, negative sold).
    spot_cd: dict calendar day -> spot. VM on months not yet in delivery; each delivery day settles against spot on
    the next business day; IM on undelivered hours at the class rate. desk(i, d, curve, mw) -> {k: dMW}."""
    mw = {k: v for k, v in mw0.items() if v}
    f_last = dict(f_last0 or {})
    out = {"vm": [], "dlv": [], "im": [], "trades": [], "mw_by_day": []}
    pc = prev_curve
    for i, d in enumerate(days):
        cur = curves[i]
        pd = days[i - 1] if i > 0 else prev_bday(d)
        vm = 0.0
        for k, m in mw.items():
            s = mi_date(k)
            if pc is not None and k in pc:
                if s > d:
                    vm += -m * month_hours(k) * (cur[k] - pc[k])
        # months whose delivery starts after today but whose last trading day is today: fix F_last at today's price
        for k in mw:
            if k not in f_last and mi_date(k) > d and prev_bday(mi_date(k)) == d:
                f_last[k] = cur[k]
        for k in mw:
            if k not in f_last and mi_date(k) <= d:
                f_last[k] = (pc or cur)[k]
        # delivery days settled today: calendar days from the previous business day up to yesterday
        dlv = 0.0
        c = pd
        while c < d:
            k = mi(c.year, c.month)
            if k in mw:
                dlv += -mw[k] * 24.0 * (spot_cd[c] - f_last[k])
            c += dt.timedelta(days=1)
        add = desk(i, d, cur, mw) if desk else {}
        for k, dm in add.items():
            mw[k] = mw.get(k, 0.0) + dm
        if add:
            out["trades"].append((d, dict(add)))
        # drop months whose last delivery day has been settled
        for k in [k for k in mw if mi_date(k + 1) <= d]:
            mw.pop(k)
        im = 0.0
        for k, m in mw.items():
            s, e = mi_date(k), mi_date(k + 1)
            if s > d:
                hrs = month_hours(k)
            else:
                hrs = max((e - d).days - 1, 0) * 24.0 + 24.0  # today's delivery and the rest are still to settle
            im += abs(m) * hrs * rates[margin_class(k, d)][i]
        out["vm"].append(vm)
        out["dlv"].append(dlv)
        out["im"].append(im)
        out["mw_by_day"].append(dict(mw))
        pc = cur
    for key in ("vm", "dlv", "im"):
        out[key] = np.array(out[key])
    out["mw"] = mw
    out["f_last"] = f_last
    return out


# ---------------------------------------------------------------------------------------------------- the desk
def ladder(tau, knots):
    xs = [k[0] for k in knots]
    lo = float(np.interp(tau, xs, [k[1] for k in knots]))
    hi = float(np.interp(tau, xs, [k[2] for k in knots]))
    return lo, hi


def make_desk(knots, budget_px, budget_gen, fixed_phys, rule="step", theta=math.log(1.25), speed=0.03, beta=0.30,
              trade_wd=1, years_ahead=(1, 2, 3)):
    """the desk sells year contracts on `trade_wd` to keep each delivery year's fixed-price share of budgeted output on
    its rule. fixed_phys(y) -> MWh sold at a fixed price outside the exchange that the ratio counts.
    rule: step (policy maximum once the price is theta above budget), linear, min (the policy minimum), max_now,
    frozen."""
    state = {"maxed": False}

    def desk(i, d, curve, mw):
        if rule == "frozen" or d.weekday() != trade_wd or (rule == "max_now" and state["maxed"]):
            return {}
        add = {}
        for j in years_ahead:
            y = d.year + j
            ks = year_months(y)
            if any(k not in curve for k in ks):
                continue
            hy = hours_year(y)
            g = budget_gen(d, y)
            exch = -sum(mw.get(k, 0.0) for k in ks) / 12.0
            ratio = (exch * hy + fixed_phys(y)) / g
            tau = max((dt.date(y, 1, 1) - d).days / 365.25, 0.0)
            lo, hi = ladder(tau, knots)
            if hi <= 0:
                continue
            x = math.log(cprice(curve, ks) / budget_px(d, y))
            if rule == "step":
                target = hi if x > theta else lo
                step = min(target - ratio, speed) if target - ratio > 0.02 else 0.0
            elif rule == "linear":
                target = min(max(lo + beta * max(0.0, x), lo), hi)
                step = min(target - ratio, speed) if target - ratio > 0.02 else 0.0
            elif rule == "min":
                step = lo - ratio
            else:
                step = hi - ratio
            if step > 0:
                dmw = math.floor(step * g / hy)
                if dmw >= 1:
                    for k in ks:
                        add[k] = add.get(k, 0.0) - dmw
        if rule == "max_now":
            state["maxed"] = True
        return add
    return desk


# ---------------------------------------------------------------------------------------------------- physical cash
def dayahead_cash(days, out_day, com_day, spot_cd):
    """net day-ahead sales (positive) or purchases (negative) for each calendar day, settled on the next business
    day: days[i] receives the calendar days from the previous business day up to the day before."""
    res = np.zeros(len(days))
    for i, d in enumerate(days):
        c = days[i - 1] if i > 0 else prev_bday(d)
        while c < d:
            res[i] += (out_day[c] - com_day[c]) * spot_cd[c]
            c += dt.timedelta(days=1)
    return res


def receipts_cash(days, invoices):
    """invoices: list of (pay_date, amount); returns the cash received on each business day."""
    idx = {d: i for i, d in enumerate(days)}
    res = np.zeros(len(days))
    for pay, amt in invoices:
        if pay in idx:
            res[idx[pay]] += amt
    return res


def per_day(month_totals, cdays):
    """spread monthly MWh evenly over the month's calendar days."""
    out = {}
    for c in cdays:
        k = mi(c.year, c.month)
        out[c] = month_totals[k] / month_days(k)
    return out
