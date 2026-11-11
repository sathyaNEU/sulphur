"""Every owed figure computed from the shipped files (frames read from target/, or the same frames built in memory for
calibration): the golden route, the careful but hurried route and the quick route, and the rivals each result's band
is measured on."""
import datetime as dt
import math

import numpy as np
import pandas as pd

import cal
import params as P

CL = list(P.CLASSES)
Z_SMALL = ["P1", "P2"]
LS_KEYS_DAY = list(range(6, 15))
LS_KEYS_EVE = list(range(14, 23))


# ----------------------------------------------------------------------------------------------------- assembly
def aisles_on(zone, dates):
    """The standard's zone table: the small-parts zones' aisles before and after the January 2024 extension."""
    new = pd.Series(dates).ge(pd.Timestamp(P.EXTENSION)).to_numpy()
    return np.where(new, P.AISLES[zone], P.AISLES_OLD[zone])


def zone_hours(f):
    z = f["zone_hours"].drop_duplicates().copy()
    z["date"] = pd.to_datetime(z["date"])
    iso = z["date"].dt.isocalendar()
    z["iy"], z["iw"] = iso["year"].astype(int), iso["week"].astype(int)
    z["ais"] = 0
    for zz in P.ZONES:
        m = z["zone"] == zz
        z.loc[m, "ais"] = aisles_on(zz, z.loc[m, "date"])
    z["dpa"] = z["pickers_logged"] / z["ais"]
    z["extra"] = z["units"] - z["lines"]
    z["kot"] = z["lines"] - z["lines_hui"]
    return z


def timesheet(f):
    t = f["timesheets"].copy()
    t["date"] = pd.to_datetime(t["date"])
    t = t.drop_duplicates(subset=["date", "person", "zone", "shift", "paid", "absence"])
    iso = t["date"].dt.isocalendar()
    t["iy"], t["iw"] = iso["year"].astype(int), iso["week"].astype(int)
    return t


def budgets(f):
    b = f["forecasts"]
    b = b[b["round"].str.startswith("budget")].copy()
    b["issued"] = pd.to_datetime(b["issued"])
    b = b.sort_values("issued").groupby(["round", "brand", "group", "iso_year", "iso_week"], as_index=False).tail(1)
    return b


# ----------------------------------------------------------------------------------------------------- R1
def r1_paid_hours(t, year=2025):
    w = t[(t["iy"] == year) & t["iw"].isin(P.PEAK_WEEKS) & (t["absence"] == "")]
    return w.groupby("zone")["paid"].sum().round(0).to_dict()


def logged_pattern(z, t, years=(2024, 2025)):
    """Minutes of each paid hour a picker is logged in to the zone, by hour of the day shift and of the evening
    shift, read from peak days: the WMS's pickers logged against the day's crew on the timesheets."""
    w = t[(t["absence"] == "") & t["iy"].isin(years) & t["iw"].isin(P.PEAK_WEEKS)]
    crew = w.groupby(["date", "zone", "shift"]).size().unstack("shift", fill_value=0).reset_index()
    if "EVE" not in crew:
        crew["EVE"] = 0
    zz = z[z["iy"].isin(years) & z["iw"].isin(P.PEAK_WEEKS) & z["zone"].isin(Z_SMALL)]
    m = zz.merge(crew, on=["date", "zone"])
    day = {}
    for h in LS_KEYS_DAY:
        r = m[(m["hour"] == h) & (m["EVE"] == 0)]
        day[h] = float(r["pickers_logged"].sum() / r["DAY"].sum()) if len(r) else 0.0
    eve = {}
    me = m[m["EVE"] > 0]
    for h in LS_KEYS_EVE:
        r = me[me["hour"] == h]
        if h == 14:
            eve[h] = float((r["pickers_logged"].sum() - day[14] * r["DAY"].sum()) / r["EVE"].sum())
        else:
            eve[h] = float(r["pickers_logged"].sum() / r["EVE"].sum()) if len(r) else 0.0
    return day, eve


# ----------------------------------------------------------------------------------------------------- R2
def picked_by_week(z):
    k = z.groupby(["iy", "iw", "zone"])[["kot", "lines_hui"]].sum().reset_index()
    return k


def placed_by_week(f):
    """Kotikaari's order lines by the ISO week they were placed (the WMS's order import: web and showroom lines),
    the quantity the budgets forecast."""
    k = f["k_orders"].copy()
    d = pd.to_datetime(k["received"])
    iso = d.dt.isocalendar()
    k["iy"], k["iw"] = iso["year"].astype(int), iso["week"].astype(int)
    k["lines"] = k["web_lines"] + k["store_lines"]
    return k.groupby(["iy", "iw", "group"])["lines"].sum().reset_index()


def r2_overstatement(z, f, years=range(2022, 2026), basis="placed"):
    b = budgets(f)
    b = b[(b["brand"] == P.BRAND_K) & b["iso_year"].isin(list(years)) & b["iso_week"].isin(P.PEAK_WEEKS)]
    if basis == "picked":
        k = picked_by_week(z)
        k = k[k["iy"].isin(list(years)) & k["iw"].isin(P.PEAK_WEEKS)]
        return float(b["order_lines"].sum() / k["kot"].sum() - 1.0)
    k = placed_by_week(f)
    k = k[k["iy"].isin(list(years)) & k["iw"].isin(P.PEAK_WEEKS)]
    return float(b["order_lines"].sum() / k["lines"].sum() - 1.0)


def overstatement_by_year(z, f, years=range(2022, 2026), weeks=None):
    b = budgets(f)
    b = b[b["brand"] == P.BRAND_K]
    k = placed_by_week(f)
    out = []
    for y in years:
        for grp in ("small parts", "bulky"):
            fb = b[(b["iso_year"] == y) & (b["group"] == grp)]
            kk = k[(k["iy"] == y) & (k["group"] == grp)]
            if weeks is not None:
                fb = fb[fb["iso_week"].isin(weeks)]
                kk = kk[kk["iw"].isin(weeks)]
            out.append({"year": y, "group": grp, "forecast": fb["order_lines"].sum(), "placed": kk["lines"].sum()})
    o = pd.DataFrame(out)
    o["over"] = o["forecast"] / o["placed"] - 1.0
    return o


def plan_growth(f):
    """The commercial plan's growth each budget states (the note on its first row)."""
    b = f["forecasts"]
    out = {}
    for _, r in b[b["note"].fillna("") != ""].iterrows():
        txt = r["note"]
        if not txt.startswith("Budget"):
            continue
        y = int(txt.split()[1].rstrip(":"))
        brand = r["brand"]
        nums = [float(x.replace(",", ".")) for x in __import__("re").findall(r"\+(\d+(?:[.,]\d+)?) ?%", txt)]
        out[(brand, y)] = (nums[0] / 100.0, nums[1] / 100.0)
    return out


# ----------------------------------------------------------------------------------------------------- R5
def calibration(z, f, form="loglog", weeks=None, intercept=True):
    o = overstatement_by_year(z, f, weeks=weeks)
    g = plan_growth(f)
    o["plan"] = [g[(P.BRAND_K, y)][0 if grp == "small parts" else 1] for y, grp in zip(o["year"], o["group"])]
    x = np.log1p(o["plan"].to_numpy()) if form == "loglog" else o["plan"].to_numpy()
    yv = np.log1p(o["over"].to_numpy()) if form == "loglog" else o["over"].to_numpy()
    if intercept:
        A = np.c_[np.ones_like(x), x]
    else:
        A = x[:, None]
    coef, *_ = np.linalg.lstsq(A, yv, rcond=None)
    res = yv - A @ coef

    def pred(plan):
        xx = math.log1p(plan) if form == "loglog" else plan
        v = (coef[0] + coef[1] * xx) if intercept else coef[0] * xx
        return math.expm1(v) if form == "loglog" else v

    sd = float(np.sqrt((res ** 2).sum() / max(1, len(res) - A.shape[1])))
    return {"coef": coef.tolist(), "pred": pred, "sd": sd, "table": o}


# ----------------------------------------------------------------------------------------------------- R3 and R4
def design(zz, with_density=True, knot=0.8, power=2.0):
    n = zz["lines"].to_numpy(float)
    X = [zz["lines_cls_%s" % c.lower()].to_numpy(float) for c in CL]
    X.append(zz["extra"].to_numpy(float))
    X.append(np.where(zz["zone"] == "P1", n, 0.0))
    X.append(zz["lines_hui"].to_numpy(float))
    names = ["A", "B", "C", "D", "F", "unit", "P1", "HUI"]
    if with_density:
        X.append(n * np.maximum(0.0, zz["dpa"].to_numpy() - knot) ** power)
        names.append("gamma")
    return np.column_stack(X), names


def fit_time(z, years=None, with_density=True, knot=None, power=None, min_lines=30, grid=True):
    """Task minutes of each small-parts zone-hour on its lines by handling class, the extra units, the zone, the
    pilot's Huippu lines and the aisle congestion gamma * max(0, d - knot) ** power at d pickers logged an aisle,
    by least squares on per-line times weighted by lines; knot and power by grid on the residual sum of squares."""
    zz = z[z["zone"].isin(Z_SMALL) & (z["lines"] >= min_lines)]
    if years is not None:
        zz = zz[zz["iy"].isin(list(years))]
    y = zz["task_min"].to_numpy(float)
    n = zz["lines"].to_numpy(float)
    w = 1.0 / n

    def one(k, p):
        X, names = design(zz, with_density, k, p)
        sw = np.sqrt(w)
        coef, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
        r = (y - X @ coef) * sw
        return float(r @ r), dict(zip(names, coef))

    if not with_density:
        s, c = one(0.0, 1.0)
        return {"coef": c, "knot": None, "power": None, "sse": s, "n": len(zz)}
    if knot is not None and power is not None and not grid:
        s, c = one(knot, power)
        return {"coef": c, "knot": knot, "power": power, "sse": s, "n": len(zz)}
    best = None
    for k in np.arange(0.40, 1.41, 0.05):
        for p in np.arange(1.0, 3.01, 0.1):
            s, c = one(float(k), float(p))
            if best is None or s < best[0]:
                best = (s, c, float(k), float(p))
    return {"coef": best[1], "knot": round(best[2], 2), "power": round(best[3], 1), "sse": best[0], "n": len(zz)}


def cong(fit, d):
    if fit.get("knot") is None:
        return 0.0
    return float(fit["coef"]["gamma"] * max(0.0, d - fit["knot"]) ** fit["power"])


def t_line(fit, shares, upl, p1, hui):
    c = fit["coef"]
    return float(sum(shares[k] * c[k] for k in CL) + c["unit"] * (upl - 1.0) + c["P1"] * p1 + c["HUI"] * hui)


def kot_mix(z, zone, year=2025):
    """Kotikaari's lines in a zone over the peak weeks of a year: class shares and units a line."""
    r = z[(z["zone"] == zone) & (z["iy"] == year) & z["iw"].isin(P.PEAK_WEEKS)]
    c = np.array([r["lines_cls_%s" % k.lower()].sum() for k in CL], float)
    c[0] -= r["lines_hui"].sum()
    upl = (r["units"].sum() - r["lines_hui"].sum() * 1.0) / max(1.0, r["kot"].sum())
    return dict(zip(CL, c / c.sum())), float(upl)


def hui_mix(f, months=("2025-11", "2025-12")):
    """Huippu Sport's small-parts lines in the peak months by their 2027 zone: class shares, units a line, share."""
    a = f["h_monthly"]
    a = a[a["month"].isin(list(months))]
    im = f["item_master"]
    im = im[im["owner"] == "HUI"][["owner_article", "handling_class"]]
    sl = f["slotting"][["owner_article", "zone"]]
    m = a.merge(im, left_on="article_no", right_on="owner_article").merge(sl, on="owner_article")
    out = {}
    tot = m[m["zone"].isin(Z_SMALL)]["order_lines"].sum()
    for zz in P.ZONES:
        r = m[m["zone"] == zz]
        c = r.groupby("handling_class")["order_lines"].sum().reindex(CL, fill_value=0).to_numpy(float)
        out[zz] = {"shares": dict(zip(CL, c / c.sum())), "upl": float(r["units"].sum() / r["order_lines"].sum()),
                   "share": float(r["order_lines"].sum() / tot) if zz in Z_SMALL else 1.0}
    return out


def r4_extra_minutes(fit, z, f, months=("2025-11", "2025-12"), year=2025):
    hm = hui_mix(f, months)
    th = sum(hm[zz]["share"] * t_line(fit, hm[zz]["shares"], hm[zz]["upl"], 1.0 if zz == "P1" else 0.0, 1.0)
             for zz in Z_SMALL)
    kz = picked_by_week(z)
    kz = kz[(kz["iy"] == year) & kz["iw"].isin(P.PEAK_WEEKS)]
    kp1 = float(kz[kz["zone"] == "P1"]["kot"].sum() / kz[kz["zone"].isin(Z_SMALL)]["kot"].sum())
    tk = 0.0
    for zz, sh in (("P1", kp1), ("P2", 1.0 - kp1)):
        s, u = kot_mix(z, zz, year)
        tk += sh * t_line(fit, s, u, 1.0 if zz == "P1" else 0.0, 0.0)
    return float(th - tk), th, tk


# ----------------------------------------------------------------------------------------------------- R6
def kot_daily_picks(z, zones):
    d = z[z["zone"].isin(zones)].groupby("date")["kot"].sum()
    d.index = pd.to_datetime(d.index)
    return d


def week_days(y, w):
    return [dt.date.fromisocalendar(y, w, k) for k in range(1, 8)]


def rekeyed_weeks(daily, shift_days=728, src_year=2025, target_year=2027, how="weekday"):
    """Lines a working-day series puts into each target-year peak week once the source year's days are moved onto
    the target year's: by the same weekday two years on (728 days, Black Friday onto Black Friday), or by date.
    A source day's lines landing on a closed target day go to the next working day of the same week."""
    out = {}
    s = daily.to_dict()
    for w in P.PEAK_WEEKS:
        tot = 0.0
        for d in week_days(target_year, w):
            if how == "weekday":
                src = d - dt.timedelta(days=shift_days)
            else:
                src = dt.date(src_year, d.month, d.day)
            tot += float(s.get(pd.Timestamp(src), 0.0))
        out[w] = tot
    return out


def copied_weeks(daily, src_year=2025):
    out = {}
    s = daily.to_dict()
    for w in P.PEAK_WEEKS:
        out[w] = sum(float(s.get(pd.Timestamp(d), 0.0)) for d in week_days(src_year, w))
    return out


def huippu_daily_series(f, grp="small parts"):
    h = f["h_daily"]
    h = h[h["group"] == grp].copy()
    s = pd.Series(h["order_lines"].to_numpy(float), index=pd.to_datetime(h["order_date"]))
    return s


def to_pickdays(s):
    """Orders onto pick days by the site's release (before noon the same working day, the rest the next)."""
    out = {}
    for d, v in s.items():
        dd = d.date()
        same = cal.next_working(dd)
        nxt = cal.next_working(dd + dt.timedelta(days=1))
        out[same] = out.get(same, 0.0) + 0.38 * v
        out[nxt] = out.get(nxt, 0.0) + 0.62 * v
    return pd.Series(out).sort_index().rename(lambda x: pd.Timestamp(x))


def budget_totals(f, brand, grp, year):
    b = budgets(f)
    b = b[(b["brand"] == brand) & (b["group"] == grp) & (b["iso_year"] == year)]
    return b.set_index("iso_week")["order_lines"].to_dict()


# ----------------------------------------------------------------------------------------------------- the plan
def capacity(zone, n, t, fit, ls, days):
    return days * sum(n * 60.0 * v / (t + cong(fit, n * v / P.AISLES[zone])) for v in ls.values())


def crew(zone, lines, t, fit, ls, days, top):
    if lines <= 0:
        return 0.0
    lo, hi = 0.0, float(top)
    for _ in range(60):
        n = (lo + hi) / 2
        lo, hi = (n, hi) if capacity(zone, n, t, fit, ls, days) < lines else (lo, n)
    return hi


def week_plan(zone, lines, t, fit, ls_day, ls_eve, days, evenings, limit=None):
    """The standard's rule: the day shifts at the zone's limit pick what they can; if lines remain, the evening shift
    of every working weekday picks them; paid hours are the crews times eight paid hours."""
    lim = limit or P.LIMIT[zone]
    cap = capacity(zone, lim, t, fit, ls_day, days)
    if lines > cap:
        ne = crew(zone, lines - cap, t, fit, ls_eve, evenings, lim)
        return {"evening": True, "cap": cap, "hours": (lim * days + ne * evenings) * P.SHIFT_PAID, "n_day": lim,
                "n_eve": ne, "ratio": lines / cap}
    nd = crew(zone, lines, t, fit, ls_day, days, lim)
    return {"evening": False, "cap": cap, "hours": nd * days * P.SHIFT_PAID, "n_day": nd, "n_eve": 0.0,
            "ratio": lines / cap}


def days_2027(w):
    ds = week_days(2027, w)
    wd = [d for d in ds if cal.working(d)]
    return len(wd), len([d for d in wd if d.weekday() < 5])


def own_hours(f, t, week):
    """The standard 4.1: own pickers on the day shift of every working weekday in their home zone, less the zone's
    sickness absence in the same weeks of the last peak (2025)."""
    ro = f["roster"]
    a, b = dt.date.fromisocalendar(2027, week, 1), dt.date.fromisocalendar(2027, week, 7)
    wk = [d for d in week_days(2027, week) if cal.working(d) and d.weekday() < 5]
    out = {}
    for zz in P.ZONES:
        r = ro[ro["home_zone"] == zz]
        n = 0
        for _, x in r.iterrows():
            st = pd.Timestamp(x["employment_start"]).date()
            en = pd.Timestamp(x["leave_until"]).date() if isinstance(x.get("leave_until"), str) and x["leave_until"] else None
            on = sum(1 for d in wk if d >= st and not (en and d <= en))
            n += on
        sick = sickness(t, zz)
        out[zz] = n * P.SHIFT_PAID * (1.0 - sick)
    return out


def sickness(t, zone, year=2025):
    w = t[(t["iy"] == year) & t["iw"].isin(P.PEAK_WEEKS) & (t["zone"] == zone) & (t["employer"] == P.ORG)
          & (t["date"].dt.weekday < 5)]
    s = (w["absence"] == "SICK").sum()
    worked = (w["absence"] == "").sum()
    return float(s / (s + worked))


# ----------------------------------------------------------------------------------------------------- the routes
def plans_2027(f):
    g = plan_growth(f)
    return g[(P.BRAND_K, 2027)], g[(P.BRAND_H, 2027)]


def b1_rate(z, year=2025):
    r = z[(z["zone"] == "B1") & (z["iy"] == year) & z["iw"].isin(P.PEAK_WEEKS) & (z["lines"] > 0)]
    X = np.c_[r["lines"].to_numpy(float), r["extra"].to_numpy(float)]
    coef, *_ = np.linalg.lstsq(X, r["task_min"].to_numpy(float), rcond=None)
    return float(coef[0]), float(coef[1])


def to_pickdays(s):
    """Web orders onto the day the WMS releases them: 06:00 on the next working day of the 2027 calendar."""
    out = {}
    for d, v in s.items():
        p = cal.next_working(d.date() + dt.timedelta(days=1))
        out[p] = out.get(p, 0.0) + v
    return out


def order_series(f, brand, grp):
    if brand == P.BRAND_K:
        k = f["k_orders"]
        k = k[k["group"] == grp]
        return pd.Series(k["web_lines"].to_numpy(float), index=pd.to_datetime(k["received"])), \
            pd.Series(k["store_lines"].to_numpy(float), index=pd.to_datetime(k["received"]))
    h = f["h_daily"]
    h = h[h["group"] == grp]
    return pd.Series(h["order_lines"].to_numpy(float), index=pd.to_datetime(h["order_date"])), None


def volumes(z, f, over_k, over_h, how="weekday", shift=728, src=2025):
    """Each 2027 peak week's lines by brand and group: the source year's orders moved onto 2027's days (the same
    weekday two years on, which puts Black Friday on Black Friday), released by 2027's calendar, grown by the growth
    the 2027 budget carries over the source year and divided by the overstatement it is expected to carry."""
    out = {}
    for brand, grp in ((P.BRAND_K, "small parts"), (P.BRAND_K, "bulky"), (P.BRAND_H, "small parts"),
                       (P.BRAND_H, "bulky")):
        bud = budget_totals(f, brand, grp, 2027)
        web, store = order_series(f, brand, grp)
        iso = web.index.isocalendar()
        base = float(web[(iso["year"] == src).to_numpy()].sum())
        if store is not None:
            base += float(store[(store.index.isocalendar()["year"] == src).to_numpy()].sum())
        growth = sum(bud.values()) / base
        ov = (over_k if brand == P.BRAND_K else over_h)[0 if grp == "small parts" else 1]
        if how == "copy":
            out[(brand, grp)] = {w: bud[w] / (1.0 + ov) for w in P.PEAK_WEEKS}
            continue
        moved = {}
        for d, v in web.items():
            if d.year < src - 1 or d.year > src + 1:
                continue
            nd = d + pd.Timedelta(days=shift) if how == "weekday" else pd.Timestamp(d.year + 2, d.month, d.day) \
                if not (d.month == 2 and d.day == 29) else None
            if nd is None:
                continue
            moved[nd] = moved.get(nd, 0.0) + v
        picks = to_pickdays(pd.Series(moved))
        if store is not None:
            for d, v in store.items():
                if d.year != src:
                    continue
                nd = (d + pd.Timedelta(days=shift)).date() if how == "weekday" else dt.date(d.year + 2, d.month, d.day)
                if cal.working(nd) and nd.weekday() < 5:
                    picks[nd] = picks.get(nd, 0.0) + v
                elif v:
                    q = cal.next_working(nd)
                    while q.weekday() >= 5:
                        q = cal.next_working(q + dt.timedelta(days=1))
                    picks[q] = picks.get(q, 0.0) + v
        wk = {}
        for p_, v in picks.items():
            if cal.isoyear(p_) == 2027 and cal.isoweek(p_) in P.PEAK_WEEKS:
                wk[cal.isoweek(p_)] = wk.get(cal.isoweek(p_), 0.0) + v
        out[(brand, grp)] = {w: wk.get(w, 0.0) * growth / (1.0 + ov) for w in P.PEAK_WEEKS}
    return out


def golden(f, opts=None):
    o = {"how": "weekday", "fit_years": None, "months": ("2025-11", "2025-12"), "form": "loglog", "cal_weeks": None,
         "intercept": True, "ls": "measured", "src": 2025, "shift": 728}
    o.update(opts or {})
    z = zone_hours(f)
    t = timesheet(f)
    R = {}
    R["r1"] = {k: v for k, v in r1_paid_hours(t).items() if k in P.ZONES}
    ls_day, ls_eve = logged_pattern(z, t)
    if o["ls"] == "flat":
        m = sum(ls_day.values()) / len(ls_day)
        ls_day = {h: m for h in ls_day}
        me = sum(ls_eve.values()) / len(ls_eve)
        ls_eve = {h: me for h in ls_eve}
    R["ls_day"], R["ls_eve"] = ls_day, ls_eve
    R["logged_share"] = sum(ls_day.values()) / P.SHIFT_PAID
    if o.get("cong") == "quad":
        best = None
        for k in np.arange(0.40, 1.41, 0.05):
            c = fit_time(z, years=o["fit_years"], knot=float(k), power=2.0, grid=False)
            if best is None or c["sse"] < best["sse"]:
                best = c
        fit = best
    elif o.get("cong") == "linear":
        best = None
        for k in np.arange(0.40, 1.41, 0.05):
            c = fit_time(z, years=o["fit_years"], knot=float(k), power=1.0, grid=False)
            if best is None or c["sse"] < best["sse"]:
                best = c
        fit = best
    else:
        fit = fit_time(z, years=o["fit_years"])
    if o.get("gamma_mult"):
        fit = dict(fit, coef=dict(fit["coef"], gamma=fit["coef"]["gamma"] * o["gamma_mult"]))
    R["fit"] = fit
    R["r3"] = cong(fit, 1.8)
    R["r4"], R["t_hui"], R["t_kot"] = r4_extra_minutes(fit, z, f, o["months"])
    R["r2"] = r2_overstatement(z, f)
    cl = calibration(z, f, o["form"], o["cal_weeks"], o["intercept"])
    pk, ph = plans_2027(f)
    om = o.get("over_mult", 1.0)
    over_k = (cl["pred"](pk[0]) * om, cl["pred"](pk[1]) * om)
    over_h = (cl["pred"](ph[0]) * om, cl["pred"](ph[1]) * om)
    R["r5"] = {"K_sp": over_k[0], "K_bu": over_k[1], "H_sp": over_h[0], "H_bu": over_h[1]}
    R["cal"] = cl
    if o["src"] == "avg":
        V25 = volumes(z, f, over_k, over_h, o["how"], 728, 2025)
        V24 = volumes(z, f, over_k, over_h, o["how"], 1092, 2024)
        V = {k: {w: 0.5 * (V25[k][w] + V24[k][w]) for w in V25[k]} for k in V25}
    else:
        V = volumes(z, f, over_k, over_h, o["how"], o["shift"], o["src"])
    R["vol"] = V
    ks = V[(P.BRAND_K, "small parts")]
    bud = budget_totals(f, P.BRAND_K, "small parts", 2027)
    R["r6"] = ks[47] / sum(ks.values())
    R["r6_budget"] = bud[47] / sum(bud[w] for w in P.PEAK_WEEKS)
    kz = picked_by_week(z)
    kz = kz[(kz["iy"] == 2025) & kz["iw"].isin(P.PEAK_WEEKS)]
    kp1 = float(kz[kz["zone"] == "P1"]["kot"].sum() / kz[kz["zone"].isin(Z_SMALL)]["kot"].sum())
    hm = hui_mix(f, o["months"])
    b1a, b1u = b1_rate(z)
    plan = {}
    for w in P.PEAK_WEEKS:
        days, eves = days_2027(w)
        for zz in P.ZONES:
            if zz == "B1":
                L = V[(P.BRAND_K, "bulky")][w] + V[(P.BRAND_H, "bulky")][w]
                tk = b1a + b1u * 0.10
                th = b1a + b1u * (hm["B1"]["upl"] - 1.0)
                t_ = (V[(P.BRAND_K, "bulky")][w] * tk + V[(P.BRAND_H, "bulky")][w] * th) / L
                hrs = L * t_ / 60.0 / (sum(ls_day.values()) / P.SHIFT_PAID)
                plan[(zz, w)] = {"lines": L, "t": t_, "hours": hrs, "evening": False, "ratio": None}
                continue
            sh_k = kp1 if zz == "P1" else 1.0 - kp1
            lk = V[(P.BRAND_K, "small parts")][w] * sh_k
            lh = V[(P.BRAND_H, "small parts")][w] * hm[zz]["share"]
            s, u = kot_mix(z, zz)
            tk = t_line(fit, s, u, 1.0 if zz == "P1" else 0.0, 0.0)
            th = t_line(fit, hm[zz]["shares"], hm[zz]["upl"], 1.0 if zz == "P1" else 0.0, 1.0)
            if o.get("hui_mult"):
                th = tk + (th - tk) * o["hui_mult"]
            L = lk + lh
            t_ = (lk * tk + lh * th) / L
            wp = week_plan(zz, L, t_, fit, ls_day, ls_eve, days, eves)
            wp.update({"lines": L, "t": t_, "lines_k": lk, "lines_h": lh})
            plan[(zz, w)] = wp
    R["plan"] = plan
    own = {w: own_hours(f, t, w) for w in P.PEAK_WEEKS}
    R["own"] = own
    R["agency"] = {w: sum(max(0.0, plan[(zz, w)]["hours"] - own[w][zz]) for zz in P.ZONES) for w in P.PEAK_WEEKS}
    R["evening"] = {(zz, w): plan[(zz, w)]["evening"] for zz in Z_SMALL for w in P.PEAK_WEEKS}
    return R


def pilot_times(f):
    """The pilot's Huippu lines: minutes from one pick confirmation to the next by the same picker in the same hour
    (the draft's and the pilot review's reading), and P2's other lines in the same weeks from the labour log."""
    c = f["pilot_conf"].copy()
    c["t"] = pd.to_datetime(c["confirmed_at"])
    c = c.drop_duplicates(subset=["task_id"]).sort_values(["picker_id", "t"])
    g = c.groupby("picker_id")["t"].diff().dt.total_seconds() / 60.0
    g = g[(g > 0) & (g < 5)]
    return float(g.mean())


def paid_per_line(z, t, year, weeks, zone):
    tt = t[(t["iy"] == year) & t["iw"].isin(weeks) & (t["zone"] == zone) & (t["absence"] == "")]
    zz = z[(z["iy"] == year) & z["iw"].isin(weeks) & (z["zone"] == zone)]
    return float(tt["paid"].sum() / zz["lines"].sum())


def hurried(f, fix=()):
    """The careful but hurried route (the site manager's draft method with the pooled overstatement): the 2027
    budget's weeks as issued over the pooled overstatement of past budgets, the 2025 peak's paid hours a line by
    zone, Huippu Sport's lines at the pilot's time a line against P2's; `fix` puts one or more judgments right."""
    z = zone_hours(f)
    t = timesheet(f)
    R = {}
    R["r2"] = r2_overstatement(z, f)
    g = golden(f) if fix else None
    ov = (R["r2"], R["r2"])
    over_k, over_h = (ov, ov)
    if "calibration" in fix:
        over_k = (g["r5"]["K_sp"], g["r5"]["K_bu"])
        over_h = (g["r5"]["H_sp"], g["r5"]["H_bu"])
    V = volumes(z, f, over_k, over_h, how="weekday" if "calendar" in fix else "copy")
    R["vol"] = V
    rate = {zz: paid_per_line(z, t, 2025, P.PEAK_WEEKS, zz) for zz in P.ZONES}
    R["rate"] = rate
    zp = z[(z["zone"] == "P2") & (z["date"] >= pd.Timestamp(P.PILOT[0])) & (z["date"] <= pd.Timestamp(P.PILOT[1]))]
    tp = pilot_times(f)
    kot_t = float((zp["task_min"].sum() - tp * zp["lines_hui"].sum()) / zp["kot"].sum())
    R["pilot_t"], R["p2_t"] = tp, kot_t
    R["r4"] = tp - kot_t
    kz = picked_by_week(z)
    kz = kz[(kz["iy"] == 2025) & kz["iw"].isin(P.PEAK_WEEKS)]
    kp1 = float(kz[kz["zone"] == "P1"]["kot"].sum() / kz[kz["zone"].isin(Z_SMALL)]["kot"].sum())
    hm = hui_mix(f)
    plan = {}
    for w in P.PEAK_WEEKS:
        days, eves = days_2027(w)
        for zz in P.ZONES:
            if zz == "B1":
                L = V[(P.BRAND_K, "bulky")][w] + V[(P.BRAND_H, "bulky")][w]
                plan[(zz, w)] = {"lines": L, "hours": L * rate["B1"], "evening": False}
                continue
            lk = V[(P.BRAND_K, "small parts")][w] * (kp1 if zz == "P1" else 1.0 - kp1)
            lh = V[(P.BRAND_H, "small parts")][w] * hm[zz]["share"]
            hpl_k = rate[zz]
            hpl_h = rate[zz] * tp / kot_t
            if "huippu" in fix:
                hpl_h = rate[zz] * g["t_hui"] / g["t_kot"]
            L = lk + lh
            hours = lk * hpl_k + lh * hpl_h
            cap_hours = P.LIMIT[zz] * days * P.SHIFT_PAID
            if "congestion" in fix:
                s_, u_ = kot_mix(z, zz)
                tk = t_line(g["fit"], s_, u_, 1.0 if zz == "P1" else 0.0, 0.0)
                th = t_line(g["fit"], hm[zz]["shares"], hm[zz]["upl"], 1.0 if zz == "P1" else 0.0, 1.0) \
                    if "huippu" in fix else tk * tp / kot_t
                t_ = (lk * tk + lh * th) / L
                wp = week_plan(zz, L, t_, g["fit"], g["ls_day"], g["ls_eve"], days, eves)
                plan[(zz, w)] = {"lines": L, "hours": wp["hours"], "evening": wp["evening"], "ratio": wp["ratio"]}
                continue
            plan[(zz, w)] = {"lines": L, "hours": hours, "evening": hours > cap_hours, "ratio": hours / cap_hours}
    R["plan"] = plan
    own = {w: own_hours(f, t, w) for w in P.PEAK_WEEKS}
    R["agency"] = {w: sum(max(0.0, plan[(zz, w)]["hours"] - own[w][zz]) for zz in P.ZONES) for w in P.PEAK_WEEKS}
    R["evening"] = {(zz, w): plan[(zz, w)]["evening"] for zz in Z_SMALL for w in P.PEAK_WEEKS}
    return R


# ----------------------------------------------------------------------------------------------------- reading the pack
OLD_CC = {"4111": "P1", "4112": "P2", "4113": "B1", "4150": "PACK"}


def load(target):
    """The shipped files read as they are and conformed: the two payroll layouts onto one, the archive's budgets with
    the 2027 workbook's Huippu Sport sheet, Huippu's own day-first dates."""
    import os
    import pack
    F = {k: os.path.join(target, v) for k, v in pack.FILES.items()}
    f = {}
    f["zone_hours"] = pd.read_csv(F["zone_hours"])
    o = pd.read_csv(F["pay_old"], sep=";", dtype=str, keep_default_na=False)
    old = pd.DataFrame({"date": pd.to_datetime(o["pvm"], format="%d.%m.%Y").dt.date, "person": o["henkilonumero"],
                        "employer": o["tyonantaja"], "zone": o["kustannuspaikka"].map(OLD_CC),
                        "shift": o["vuoro"].map({"A": "DAY", "I": "EVE"}), "start": o["alkoi"], "end": o["paattyi"],
                        "paid": o["tunnit"].str.replace(",", ".").astype(float),
                        "absence": o["poissaolo"].map({"S": "SICK", "L": "VAC", "": ""}),
                        "absence_hours": pd.to_numeric(o["poissaolotunnit"].str.replace(",", "."), errors="coerce").fillna(0.0)})
    n = pd.read_csv(F["pay_new"], dtype=str, keep_default_na=False)
    new = pd.DataFrame({"date": pd.to_datetime(n["work_date"]).dt.date, "person": n["person_id"],
                        "employer": n["employer"], "zone": n["cost_centre"].str.replace("SAA-", "", regex=False),
                        "shift": n["shift"], "start": n["start"], "end": n["end"], "paid": n["paid_hours"].astype(float),
                        "absence": n["absence_code"],
                        "absence_hours": pd.to_numeric(n["absence_hours"], errors="coerce").fillna(0.0)})
    f["timesheets"] = pd.concat([old, new], ignore_index=True)
    a = pd.read_csv(F["archive"], keep_default_na=False)
    a["issued"] = pd.to_datetime(a["issued"]).dt.date
    from openpyxl import load_workbook
    wb = load_workbook(F["budget27"], data_only=False)
    extra = []
    for sheet, brand in (("Huippu Sport", P.BRAND_H),):
        ws = wb[sheet]
        for row in ws.iter_rows(min_row=2, values_only=True):
            if isinstance(row[0], int):
                extra.append((dt.date(2026, 10, 15), "budget 2027", brand, "small parts", 2027, row[0], row[1], ""))
                extra.append((dt.date(2026, 10, 15), "budget 2027", brand, "bulky", 2027, row[0], row[2], ""))
    cov = {r[0]: r[1] for r in wb["Cover"].iter_rows(values_only=True) if r[0]}
    hp = cov["Commercial plan 2027, Huippu Sport"]
    extra[0] = extra[0][:-1] + ("Budget 2027: commercial plan %s" % hp,)
    a = pd.concat([a, pd.DataFrame(extra, columns=a.columns)], ignore_index=True)
    f["forecasts"] = a
    f["k_orders"] = pd.read_csv(F["k_orders"])
    h = pd.read_csv(F["h_daily"])
    h["order_date"] = pd.to_datetime(h["order_date"], format="%d/%m/%Y").dt.date
    f["h_daily"] = h.rename(columns={"product_line": "group"})
    f["h_monthly"] = pd.read_csv(F["h_monthly"], dtype={"month": str})
    f["item_master"] = pd.read_excel(F["item_master"], dtype={"owner_article": str})
    f["slotting"] = pd.read_excel(F["slotting"], header=2, dtype={"owner_article": str})
    f["pilot_conf"] = pd.read_csv(F["pilot"], dtype={"picker_id": str})
    f["roster"] = pd.read_excel(F["roster"], dtype={"leave_until": str}).fillna({"leave_until": ""})
    return f


# ----------------------------------------------------------------------------------------------------- R8
def profile_error(f, z):
    """How far a re-keyed profile misses a peak's weeks: 2024's orders moved onto 2025's days by the Black Friday
    step (364 days), grown to 2025's year, against 2025's own peak weeks, as log errors."""
    errs = []
    for brand, grp in ((P.BRAND_K, "small parts"), (P.BRAND_K, "bulky")):
        web, store = order_series(f, brand, grp)
        tot = {}
        for y in (2024, 2025):
            sel = web[web.index.year == y].sum() + (store[store.index.year == y].sum() if store is not None else 0.0)
            tot[y] = float(sel)
        g = tot[2025] / tot[2024]
        moved = {}
        for d, v in web.items():
            if d.year == 2024:
                nd = d + pd.Timedelta(days=364)
                moved[nd] = moved.get(nd, 0.0) + v
        picks = {}
        for d, v in moved.items():
            p = cal.next_working(d.date() + dt.timedelta(days=1))
            picks[p] = picks.get(p, 0.0) + v
        act = {}
        for d, v in web.items():
            if d.year in (2025,):
                p = cal.next_working(d.date() + dt.timedelta(days=1))
                act[p] = act.get(p, 0.0) + v
        for w in P.PEAK_WEEKS:
            ds = week_days(2025, w)
            pr = sum(picks.get(d, 0.0) for d in ds) * g
            ac = sum(act.get(d, 0.0) for d in ds)
            errs.append(math.log(ac / pr))
    e = np.array(errs)
    return float(np.sqrt(((e - e.mean()) ** 2).mean()))


def model_error(z, fit):
    """The time model's error on whole peak zone-weeks of 2024 and 2025, as log errors of task minutes."""
    zz = z[z["zone"].isin(Z_SMALL) & z["iy"].isin([2024, 2025]) & z["iw"].isin(P.PEAK_WEEKS) & (z["lines"] > 0)]
    X, names = design(zz, True, fit["knot"], fit["power"])
    pred = X @ np.array([fit["coef"][k] for k in names])
    g = pd.DataFrame({"k": list(zip(zz["iy"], zz["iw"], zz["zone"])), "a": zz["task_min"].to_numpy(), "p": pred})
    s = g.groupby("k")[["a", "p"]].sum()
    e = np.log(s["a"] / s["p"]).to_numpy()
    return float(np.sqrt((e ** 2).mean()))


def ranges(f, z, R, q=1.2815515655446004):
    sl = R["cal"]["sd"]
    sw = profile_error(f, z)
    sm = model_error(z, R["fit"])
    sL = math.sqrt(sl ** 2 + sw ** 2)
    out = {}
    for (zz, w), p in R["plan"].items():
        days, eves = days_2027(w)
        h = p["hours"]
        if zz == "B1":
            lo, hi = h * math.exp(-q * sL), h * math.exp(q * sL)
        else:
            lo = week_plan(zz, p["lines"] * math.exp(-q * sL), p["t"], R["fit"], R["ls_day"], R["ls_eve"], days, eves)["hours"]
            hi = week_plan(zz, p["lines"] * math.exp(q * sL), p["t"], R["fit"], R["ls_day"], R["ls_eve"], days, eves)["hours"]
        dl = math.sqrt(math.log(h / lo) ** 2 + (q * sm) ** 2)
        du = math.sqrt(math.log(hi / h) ** 2 + (q * sm) ** 2)
        out[(zz, w)] = (h * math.exp(-dl), h * math.exp(du))
    return out, {"level": sl, "week": sw, "model": sm, "lines": sL}
