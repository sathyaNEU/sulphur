"""task10 architecture 5: the analyst's computations on clean tables (the truth's or the parsed pack's).

Every route the design note's ladder names is a function here, so checks.py can run each on the clean truth and on
the pack: the default path (each zone's event-window reduction against a weather-adjusted baseline, carried at its
average delivery per MW scheduled), its variants, and the golden (the reduction net of the neighbouring primary's
rise in the same half-hours, its delivery read at the design condition)."""
import datetime as dt

import numpy as np
import pandas as pd

UTC = dt.timezone.utc
BASE_T = 15.5
T_DESIGN = -3.0
SENS_TS = (-6.0,)        # the prompt's colder working weekday of winter 2027/28 (daily mean, guideline 2's station)
CREDIT_HH = ("17:30", "18:00")
WINDOW = ("16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30")   # half-hours ending, local
BANK_HOLIDAYS = {dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29),
                 dt.date(2024, 12, 25), dt.date(2024, 12, 26), dt.date(2025, 1, 1),
                 dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
WINTER_OF = lambda d: "%d/%02d" % ((d.year, (d.year + 1) % 100) if d.month >= 7 else (d.year - 1, d.year % 100))


def _last_sunday(year, month):
    d = dt.date(year, month + 1, 1) - dt.timedelta(days=1)
    while d.weekday() != 6:
        d -= dt.timedelta(days=1)
    return d


def local_end(t_utc):
    """UK local time of a half-hour's end stamp given in UTC."""
    y = t_utc.year
    s = dt.datetime.combine(_last_sunday(y, 3), dt.time(1, 0), UTC)
    e = dt.datetime.combine(_last_sunday(y, 10), dt.time(1, 0), UTC)
    off = 1 if s <= t_utc - dt.timedelta(minutes=30) < e else 0
    return (t_utc + dt.timedelta(hours=off)).replace(tzinfo=None)


def prepare(demand):
    """Adds the local date of each half-hour's start and the local half-hour label 'HH:MM' (its end)."""
    d = demand.copy()
    ends = [local_end(t.to_pydatetime()) for t in d["t_utc"]]
    starts = [e - dt.timedelta(minutes=30) for e in ends]
    d["ldate"] = [s.date() for s in starts]
    d["hh"] = [e.strftime("%H:%M") if e.strftime("%H:%M") != "00:00" else "24:00" for e in ends]
    return d


def daily_mean(weather):
    """The mean of the station's hourly readings over each GMT day, for days with at least 20 of their 24 readings."""
    w = weather.copy()
    w["date"] = [t.date() for t in w["t_utc"]]
    g = w.groupby("date")["temp_c"]
    n = g.size()
    return g.mean()[n >= 20]


def _christmas(d):
    return (d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 2)


def _workday(d):
    """A weekday outside the bank holidays and the Christmas and New Year period (24 December to 2 January)."""
    return d.weekday() < 5 and d not in BANK_HOLIDAYS and not _christmas(d)


def _fit(y, T, winters, base=BASE_T):
    """y ~ winter fixed effects + slope x heating degrees below base; returns (levels by winter, slope)."""
    ws = sorted(set(winters))
    X = np.column_stack([(np.array(winters) == w).astype(float) for w in ws] +
                        [np.maximum(0.0, base - np.array(T))])
    beta, *_ = np.linalg.lstsq(X, np.array(y, float), rcond=None)
    return dict(zip(ws, beta[:-1])), beta[-1]


def daily_peaks(prep, code):
    """Each local day's highest half-hour, for days the export covers (at least 44 of their half-hours): the half-hours
    of a day cut by the export's first or last stamp are not that day's peak."""
    s = prep[prep["code"] == code]
    g = s.groupby("ldate")["mw"]
    n = g.size()
    return g.max()[n >= 44]


def design_peak(prep, tmean, code, exclude=(), base=BASE_T, winters=None, restore=None):
    """2025/26 weather-corrected peak half-hour on a workday at the design condition."""
    pk = daily_peaks(prep, code)
    if restore:
        pk = pk.copy()
        for d, v in restore.items():
            if d in pk.index:
                pk[d] += v
    dates = [d for d in pk.index if _workday(d) and d in tmean.index and d not in exclude]
    if winters:
        dates = [d for d in dates if WINTER_OF(d) in winters]
    lev, b = _fit([pk[d] for d in dates], [tmean[d] for d in dates], [WINTER_OF(d) for d in dates], base)
    return lev["2025/26"] + b * max(0.0, base - T_DESIGN), b


def hh_table(prep, code, hhs=CREDIT_HH):
    s = prep[(prep["code"] == code) & (prep["hh"].isin(hhs))]
    return s.pivot_table(index="ldate", columns="hh", values="mw", aggfunc="mean")


def baseline_excess(prep, tmean, code, dates, exclude, hhs=CREDIT_HH, base=BASE_T):
    """For each date: actual minus a weather-adjusted baseline (winter levels + heating slope, fitted per half-hour
    on workdays outside `exclude`), averaged over the half-hours `hhs`."""
    tab = hh_table(prep, code, hhs)
    out = {}
    preds = {}
    for h in hhs:
        train = [d for d in tab.index if _workday(d) and d in tmean.index and d not in exclude and not np.isnan(tab.loc[d, h])]
        lev, b = _fit([tab.loc[d, h] for d in train], [tmean[d] for d in train], [WINTER_OF(d) for d in train], base)
        preds[h] = (lev, b)
    for d in dates:
        v = []
        for h in hhs:
            if d in tab.index and not np.isnan(tab.loc[d, h]):
                lev, b = preds[h]
                v.append(tab.loc[d, h] - (lev[WINTER_OF(d)] + b * max(0.0, base - tmean[d])))
        out[d] = float(np.mean(v)) if v else None
    return out


def cbl_excess(prep, code, dates, exclude, hhs=CREDIT_HH, n=10):
    """Actual minus the mean of the n previous workdays outside `exclude` (no weather adjustment)."""
    tab = hh_table(prep, code, hhs).mean(axis=1)
    days = sorted(d for d in tab.index if _workday(d))
    out = {}
    for d in dates:
        if d not in tab.index or np.isnan(tab[d]):
            out[d] = None
            continue
        prior = [x for x in days if x < d and x not in exclude and not np.isnan(tab[x])][-n:]
        out[d] = float(tab[d] - np.mean([tab[x] for x in prior]))
    return out


def zone_events(events, zone):
    e = events[(events["zone"] == zone) & (events["status"] == "Completed")]
    return {r.date: float(r.scheduled_mw) for r in e.itertuples()}


def delivery_records(prep, tmean, events, zone, partner=None, method="regression", partner_clean=True):
    """Per event: (date, temperature, scheduled MW, reduction at the credited half-hours, partner rise)."""
    ev = zone_events(events, zone)
    dates = sorted(ev)
    allz = set(events[events["zone"] == zone]["date"])   # every scheduled day, cancelled included
    if method == "regression":
        red = {d: (-v if v is not None else None) for d, v in baseline_excess(prep, tmean, zone, dates, allz).items()}
    else:
        red = {d: (-v if v is not None else None) for d, v in cbl_excess(prep, zone, dates, allz).items()}
    rise = {d: 0.0 for d in dates}
    if partner:
        excl = allz if partner_clean else set()
        rise = baseline_excess(prep, tmean, partner, dates, excl)
    return [(d, float(tmean[d]), ev[d], red[d], rise[d]) for d in dates if red.get(d) is not None and rise.get(d) is not None]


def delivery_at(recs, net=True, at=T_DESIGN, temperature=True, did=False):
    """Delivery per MW scheduled: each event's reduction (net of the partner's rise, or with the partner as a control),
    regressed on the event day's daily mean temperature and read at `at`, or averaged."""
    y = []
    for d, T, mw, red, rise in recs:
        r = red - rise if net else (red + rise if did else red)
        y.append(r / mw)
    T = np.array([r[1] for r in recs])
    y = np.array(y)
    if not temperature:
        return float(y.mean())
    A = np.column_stack([np.ones(len(T)), T])
    c, *_ = np.linalg.lstsq(A, y, rcond=None)
    return float(c[0] + c[1] * at)


def pair_records(prep, tmean, events, zone, partner):
    """Per event: the zone and its partner taken together (what the transfer moves between them cancels)."""
    ev = zone_events(events, zone)
    dates = sorted(ev)
    allz = set(events[events["zone"] == zone]["date"])
    pz = prep[prep["code"].isin([zone, partner])].copy()
    # a half-hour counts only where both primaries reported it; a sum of one is not the pair's demand
    pz = pz.groupby(["t_utc", "ldate", "hh"], as_index=False)["mw"].agg(["sum", "count"])
    pz = pz[pz["count"] == 2].rename(columns={"sum": "mw"}).drop(columns="count")
    pz["code"] = "PAIR"
    red = {d: (-v if v is not None else None) for d, v in baseline_excess(pz, tmean, "PAIR", dates, allz).items()}
    return [(d, float(tmean[d]), ev[d], red[d], 0.0) for d in dates if red[d] is not None]


def form_check(X, zones):
    """The correction's form tested where the record allows it: winter 2023/24 ran no flexibility, so its cold working
    weekdays are untouched. Fitted on its working weekdays at or above the coldest daily mean the zone's 2025/26
    correction is fitted on (the extrapolation guideline 3 makes), each form predicts its working weekdays below 0 C;
    returns, per zone, the mean error (predicted less recorded peak, MW) of the linear and the quadratic form."""
    prep = X["_prep"]
    tm = daily_mean(X["weather"])
    ev = X["events"]
    out = {}
    for z in zones:
        code = z["code"]
        pk = daily_peaks(prep, code)
        sched = set(ev[ev["zone"] == code]["date"])
        t26 = min(tm[d] for d in pk.index if _workday(d) and d in tm.index and d not in sched
                  and WINTER_OF(d) == "2025/26")
        days = [d for d in pk.index if _workday(d) and d in tm.index and WINTER_OF(d) == "2023/24"]
        T = np.array([tm[d] for d in days])
        y = np.array([pk[d] for d in days])
        fit, cold = T >= t26, T < 0.0
        err = {}
        for name, deg in (("linear", 1), ("quadratic", 2)):
            c = np.polyfit(T[fit], y[fit], deg)
            err[name] = float(np.mean(np.polyval(c, T[cold]) - y[cold]))
        out[z["primary"]] = dict(train_min=float(t26), n_cold=int(cold.sum()), **err)
    return out


def forecast(before26, dfes_pct, register_mw, growth_years=2):
    return before26 * (1 + dfes_pct / 100.0) ** growth_years + register_mw


ZONE_PROVIDER = {"PS40617": "Corvane Flex Ltd", "PS41108": "Quillon Energy Services Ltd",
                 "PS41474": "Quillon Energy Services Ltd", "PS41236": "Corvane Flex Ltd"}
ZONE_LABEL = {"PS40617": "Ashcombe Road CMZ", "PS41108": "Charlecote Way CMZ", "PS41474": "Fenwick Street CMZ",
              "PS41236": "Hartwell Common CMZ"}
MATERIAL_RISE = 0.3   # MW in the credited half-hours, averaged over the zone's events


def golden_from(X, linked_rule="largest", temperature=True, design_T=T_DESIGN, base=BASE_T, sens_Ts=SENS_TS,
                hold_credit=False):
    """The golden on the parsed pack: each zone primary's 2025/26 design-day demand (event days excluded), grown to
    2027/28 by the guideline; each zone's events read at the zone and at every primary its open points reach, the
    neighbour whose demand rises in the same half-hours netted off; the provider's reduction per MW scheduled
    regressed on the event day's daily mean temperature and read at the design condition; credited on the 2027/28
    contracts. The prompt's colder working weekdays (sens_Ts) are assessed the same way: the same 2025/26 correction
    read at each daily mean and grown, less the provider's reduction read at that daily mean on the same contract
    (hold_credit keeps the design day's credit instead, the unfinished chain the asks price)."""
    prep = X.get("_prep")
    if prep is None:
        prep = prepare(X["demand"])
        X["_prep"] = prep
    tm = daily_mean(X["weather"])
    ev = X["events"]
    zones, evidence = [], []
    for code in sorted(ZONE_LABEL, key=lambda c: ZONE_LABEL[c]):
        name = X["names"][code]
        excl = set(ev[ev["zone"] == code]["date"])
        d26, slope = design_peak(prep, tm, code, exclude=excl, base=base, winters=["2025/26"])
        r1, r2 = X["rates"][code]
        before = d26 * (1 + r1 / 100.0) * (1 + r2 / 100.0) + X["growth"].get(code, 0.0)
        rises = {}
        for nb in sorted(X["links"][code]):
            recs = delivery_records(prep, tm, ev, code, partner=nb)
            rises[nb] = (float(np.mean([r[4] for r in recs])), recs)
        base_recs = delivery_records(prep, tm, ev, code)
        linked = None
        if linked_rule == "largest":
            nb = max(rises, key=lambda k: rises[k][0])
            if rises[nb][0] > MATERIAL_RISE:
                linked = nb
            recs = rises[linked][1] if linked else base_recs
        elif linked_rule == "sum":   # every neighbour's rise netted
            byd = {r[0]: list(r) for r in base_recs}
            for nb, (m, rr) in rises.items():
                for r in rr:
                    if r[0] in byd:
                        byd[r[0]][4] += r[4]
            recs = [tuple(v) for v in byd.values() if all(r[0] in {x[0] for x in rr} for rr in [q for _, q in rises.values()])]
            linked = max(rises, key=lambda k: rises[k][0])
        delivery = delivery_at(recs, net=True, temperature=temperature, at=design_T)
        measured = delivery_at(base_recs, net=False, temperature=False)
        mw28 = X["contracts"][name]
        credited = delivery * mw28
        after = before - credited
        firm = X["firm"][code]
        # the colder working weekdays: the 2025/26 correction read at each daily mean, grown as guideline 4 grows it
        sens = {}
        for sT in sens_Ts:
            d26_s = d26 + slope * (max(0.0, base - sT) - max(0.0, base - design_T))
            before_s = d26_s * (1 + r1 / 100.0) * (1 + r2 / 100.0) + X["growth"].get(code, 0.0)
            delivery_s = delivery if hold_credit else delivery_at(recs, net=True, temperature=temperature, at=sT)
            sens[sT] = dict(before=before_s, delivery=delivery_s, after=before_s - delivery_s * mw28,
                            over=before_s - delivery_s * mw28 > firm)
        zones.append(dict(zone=ZONE_LABEL[code], primary=name, code=code, provider=ZONE_PROVIDER[code], mw28=mw28,
                          d26=d26, slope=slope, before=before, delivery=delivery, credited=credited, after=after,
                          firm=firm, over=after > firm, measured=measured, over_by=after - firm, sens=sens,
                          linked=X["names"][linked] if linked else "", linked_code=linked or "",
                          linked_rise=rises[linked][0] if linked else max(m for m, _ in rises.values()),
                          rises={k: v[0] for k, v in rises.items()}, n_events=len(recs)))
        for d, T, mw, fall, rise in recs:
            evidence.append(dict(date=d, zone=ZONE_LABEL[code], mw=mw, T=T, fall=fall,
                                 linked=X["names"][linked] if linked else "none", rise=rise if linked else 0.0))
    evidence.sort(key=lambda r: (r["date"], r["zone"]))
    return dict(zones=zones, evidence=evidence, commit=[z["primary"] for z in zones if z["over"]],
                commit_sens={sT: [z["primary"] for z in zones if z["sens"][sT]["over"]] for sT in sens_Ts}, sens_Ts=sens_Ts)
