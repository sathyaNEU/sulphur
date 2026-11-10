"""task10 architecture 6: the analyst's computations on clean tables (the truth's or the parsed pack's).

Every result of the design note's chain is a function here, with the hurried methods beside the golden's, so
checks.py can run each on the clean truth and on the pack and effort_passes.py can price them:

  R1 the event record (each completed event's megawatts delivered in the credited half-hours, against a
     weather-adjusted baseline, days with logged switching at the primary left out)
  R2 each zone primary's design-day demand before flexibility, winter 2027/28 (guideline sections 2 to 5)
  R3 the share of its contracted megawatts each provider has available on the design day
  R4 the same model fitted on winter 2024/25 alone and set against winter 2025/26's events
  R5 what comes back after the window, the design day's half-hours with the contract called, the half-hour that
     then peaks and the megawatts the contract takes off the day's peak
  R6 and R7 each primary's design-day peak with flexibility, expected and at the one-day-in-ten level
  R8 the primaries to reinforce; R9 each contract's megawatts bridged to the megawatts credited
"""
import datetime as dt
import math

import numpy as np
import pandas as pd

UTC = dt.timezone.utc
BASE_T = 15.5
T_DESIGN = -3.0
CREDIT_HH = ("17:30", "18:00")
WINDOW = ("16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30")   # half-hours ending, local
POST = ("20:00", "20:30", "21:00", "21:30")
EVENING = ("16:00",) + WINDOW + POST + ("22:00",)
BANK_HOLIDAYS = {dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29),
                 dt.date(2024, 12, 25), dt.date(2024, 12, 26), dt.date(2025, 1, 1),
                 dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
WINTER_OF = lambda d: "%d/%02d" % ((d.year, (d.year + 1) % 100) if d.month >= 7 else (d.year - 1, d.year % 100))
ASSURANCE = 0.90      # guideline 7: within firm capacity on nine design days in ten
Z90 = 1.2815515655446004


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


# ------------------------------------------------------------------------------------------------ switching
def switch_dates(switching, code):
    """Local dates on which a logged 11 kV transfer was in place at the primary (either side of the open point)."""
    out = set()
    if switching is None or len(switching) == 0:
        return out
    for r in switching.itertuples():
        if code not in (r.frm, r.to):
            continue
        a = local_end(pd.Timestamp(r.start).to_pydatetime()).date()
        b = local_end(pd.Timestamp(r.end).to_pydatetime()).date()
        d = a
        while d <= b:
            out.add(d)
            d += dt.timedelta(days=1)
    return out


# ------------------------------------------------------------------------------------------------ the demand side
def daily_peaks(prep, code):
    """Each local day's highest half-hour, for days the export covers (at least 44 of their half-hours)."""
    s = prep[prep["code"] == code]
    g = s.groupby("ldate")["mw"]
    n = g.size()
    return g.max()[n >= 44]


def design_peak(prep, tmean, code, exclude=(), base=BASE_T, winters=None, at=T_DESIGN):
    """2025/26 weather-corrected peak half-hour on a workday at the design condition; also the fit's relative spread."""
    pk = daily_peaks(prep, code)
    dates = [d for d in pk.index if _workday(d) and d in tmean.index and d not in exclude]
    if winters:
        dates = [d for d in dates if WINTER_OF(d) in winters]
    y = [pk[d] for d in dates]
    T = [tmean[d] for d in dates]
    wn = [WINTER_OF(d) for d in dates]
    lev, b = _fit(y, T, wn, base)
    fitted = np.array([lev[w] + b * max(0.0, base - t) for w, t in zip(wn, T)])
    rel = (np.array(y) - fitted) / fitted
    return lev["2025/26"] + b * max(0.0, base - at), b, float(np.std(rel, ddof=len(lev) + 1)), len(dates)


def hh_table(prep, code, hhs):
    s = prep[(prep["code"] == code) & (prep["hh"].isin(hhs))]
    return s.pivot_table(index="ldate", columns="hh", values="mw", aggfunc="mean")


def hh_fits(prep, tmean, code, exclude, hhs, base=BASE_T, winters=None):
    """Per half-hour: winter levels and a heating slope, fitted on workdays outside `exclude`."""
    tab = hh_table(prep, code, hhs)
    fits = {}
    for h in hhs:
        train = [d for d in tab.index if _workday(d) and d in tmean.index and d not in exclude and
                 not np.isnan(tab.loc[d, h]) and (winters is None or WINTER_OF(d) in winters)]
        fits[h] = _fit([tab.loc[d, h] for d in train], [tmean[d] for d in train], [WINTER_OF(d) for d in train], base)
    return tab, fits


def excess(prep, tmean, code, dates, exclude, hhs, base=BASE_T):
    """For each date and half-hour: actual minus the weather-adjusted baseline (NaN where the half-hour is absent)."""
    tab, fits = hh_fits(prep, tmean, code, exclude, hhs, base)
    out = {}
    for d in dates:
        row = {}
        for h in hhs:
            lev, b = fits[h]
            if d in tab.index and not np.isnan(tab.loc[d, h]) and WINTER_OF(d) in lev:
                row[h] = float(tab.loc[d, h] - (lev[WINTER_OF(d)] + b * max(0.0, base - tmean[d])))
            else:
                row[h] = float("nan")
        out[d] = row
    return out


def design_profile(prep, tmean, code, exclude, growth_factor, add_mw, hhs=EVENING, base=BASE_T, at=T_DESIGN):
    """The design day's half-hours before flexibility in winter 2027/28: each half-hour's 2025/26 level corrected to
    the design condition and grown in the proportion the peak grows (guideline 4)."""
    tab, fits = hh_fits(prep, tmean, code, exclude, hhs, base, winters=["2025/26"])
    raw = {h: fits[h][0]["2025/26"] + fits[h][1] * max(0.0, base - at) for h in hhs}
    return raw


def forecast(before26, r1, r2, register_mw):
    return before26 * (1 + r1 / 100.0) * (1 + r2 / 100.0) + register_mw


# ------------------------------------------------------------------------------------------------ the event record
def event_table(X, code, method="regression", net_switching=True, exclude_switch_days=True, credit="mean"):
    """One row per completed event at the zone: date, winter, daily mean temperature, megawatts scheduled and
    contracted, megawatts delivered in the credited half-hours, the reduction in each window half-hour and the
    rise in each of the four half-hours after it."""
    prep, tm, ev = X["_prep"], X["_tm"], X["events"]
    e = ev[(ev["zone"] == code)]
    allz = set(e["date"])                       # every scheduled day, cancelled included
    sw = switch_dates(X.get("switching"), code)
    done = e[e["status"] == "Completed"]
    dates = sorted(d for d in done["date"] if d in tm.index)
    mw = {r.date: float(r.scheduled_mw) for r in done.itertuples()}
    excl = allz | (sw if exclude_switch_days else set())
    hhs = WINDOW + POST
    ex = excess(prep, tm, code, dates, excl, hhs)
    rows = []
    for d in dates:
        x = ex[d]
        cred = [x[h] for h in CREDIT_HH if not math.isnan(x[h])]
        if len(cred) < 2:
            continue
        w = WINTER_OF(d)
        rows.append(dict(date=d, winter=w, zone=code, T=float(tm[d]), scheduled=mw[d], contract=X["contract"][(code, w)],
                         delivered=-float(np.mean(cred) if credit == "mean" else max(cred)), switch=d in sw,
                         **{"win_" + h: -x[h] for h in WINDOW}, **{"post_" + h: x[h] for h in POST}))
    t = pd.DataFrame(rows)
    if exclude_switch_days and len(t):
        t = t[~t["switch"]].reset_index(drop=True)
    return t


def placebo_sd(X, code):
    """The spread of the same measurement on working weekdays with nothing scheduled and no switching: what an
    event's measured megawatts carry from the baseline alone."""
    prep, tm, ev = X["_prep"], X["_tm"], X["events"]
    allz = set(ev[ev["zone"] == code]["date"])
    sw = switch_dates(X.get("switching"), code)
    tab = hh_table(prep, code, CREDIT_HH)
    days = [d for d in tab.index if _workday(d) and d in tm.index and d not in allz and d not in sw and
            WINTER_OF(d) in ("2023/24", "2024/25", "2025/26")]
    ex = excess(prep, tm, code, days, allz | sw, CREDIT_HH)
    v = [np.mean([ex[d][h] for h in CREDIT_HH]) for d in days if not any(math.isnan(ex[d][h]) for h in CREDIT_HH)]
    return float(np.std(v, ddof=2)), len(v)


# ------------------------------------------------------------------------------------------------ availability
def _norm_cdf(z):
    return 0.5 * (1.0 + np.vectorize(math.erf)(np.asarray(z, float) / math.sqrt(2.0)))


def _basis(T, form):
    T = np.asarray(T, float)
    if form == "linear":
        return np.column_stack([np.ones(len(T)), T])
    if form == "quadratic":
        return np.column_stack([np.ones(len(T)), T, T * T])
    if form == "hinge":            # flat above a knee at +1.0 C, a slope below it
        return np.column_stack([np.ones(len(T)), np.minimum(T - 1.0, 0.0)])
    raise ValueError(form)


def met(ev, tol_mw=0.2, tol_share=0.07):
    """An event on which the provider delivered what was scheduled (within the measurement's noise): its megawatts
    show only that at least that much was available."""
    return (ev["delivered"] >= ev["scheduled"] - np.maximum(tol_mw, tol_share * ev["scheduled"])).values


def availability_fit(ev, form="linear", censor=True, tol_mw=0.2, tol_share=0.07, iters=400):
    """The available share of the contracted megawatts against the day's temperature. Events that fell short of the
    schedule show the share itself (delivered over contracted); events that met it show only a floor (scheduled over
    contracted). A normal censored regression, fitted by Newton steps on the mean's coefficients and the spread."""
    y = (ev["delivered"] / ev["contract"]).values.astype(float)
    u = (ev["scheduled"] / ev["contract"]).values.astype(float)
    c = met(ev, tol_mw, tol_share)
    B = _basis(ev["T"].values, form)
    obs = ~c
    beta, *_ = np.linalg.lstsq(B[obs], y[obs], rcond=None)
    s = float(np.std(y[obs] - B[obs] @ beta)) or 0.05
    if not censor:
        return dict(beta=beta, sigma=s, form=form, n_short=int(obs.sum()), n_met=int(c.sum()))
    # EM for the censored normal: replace each floor by the conditional mean above it
    for _ in range(iters):
        mu = B @ beta
        z = (u - mu) / s
        lam = np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi) / np.maximum(1.0 - _norm_cdf(z), 1e-12)
        ey = np.where(c, mu + s * lam, y)
        ey2 = np.where(c, mu * mu + s * s + s * (u + mu) * lam, y * y)
        nb, *_ = np.linalg.lstsq(B, ey, rcond=None)
        m2 = B @ nb
        ns = math.sqrt(max(float(np.mean(ey2 - 2 * ey * m2 + m2 * m2)), 1e-8))
        if np.max(np.abs(nb - beta)) < 1e-9 and abs(ns - s) < 1e-9:
            beta, s = nb, ns
            break
        beta, s = nb, ns
    return dict(beta=beta, sigma=s, form=form, n_short=int(obs.sum()), n_met=int(c.sum()))


def share_at(fit, T=T_DESIGN):
    return float((_basis([T], fit["form"]) @ fit["beta"])[0])


def local_share(ev, T=T_DESIGN, half_width=2.0):
    """A straight line through delivered over contracted on the short events within a band of the design day's
    temperature, read at it."""
    e = ev[(~met(ev)) & (np.abs(ev["T"] - T) <= half_width)]
    y = (e["delivered"] / e["contract"]).values
    c = np.polyfit(e["T"].values, y, 1)
    return float(np.polyval(c, T)), len(e)


def cold_share(ev, T=T_DESIGN, below=-1.0, form="linear", short_only=False):
    """Delivered over contracted against temperature on the days at or below `below`, where every call outran what
    was available; read at the design day."""
    e = ev[ev["T"] <= below]
    if short_only:
        e = e[~met(e)]
    y = (e["delivered"] / e["contract"]).values
    B = _basis(e["T"].values, form)
    beta, *_ = np.linalg.lstsq(B, y, rcond=None)
    resid = y - B @ beta
    return float((_basis([T], form) @ beta)[0]), len(e), beta, resid, e


# ------------------------------------------------------------------------------------------------ per megawatt scheduled
def rate_per_scheduled(ev, T=T_DESIGN, form="linear"):
    """The hurried reading: megawatts delivered per megawatt scheduled, against temperature, read at the design day."""
    s = ev["scheduled"].values.astype(float)
    y = ev["delivered"].values.astype(float)
    B = _basis(ev["T"].values, form) * s[:, None]
    beta, *_ = np.linalg.lstsq(B, y, rcond=None)
    return float((_basis([T], form) @ beta)[0])


def ratio_mean(ev):
    return float(ev["delivered"].sum() / ev["scheduled"].sum())


# ------------------------------------------------------------------------------------------------ window and come-back
def _through_origin(x, d):
    ok = ~np.isnan(x)
    return float(np.sum(x[ok] * d[ok]) / np.sum(d[ok] * d[ok]))


def window_shape(ev):
    """Each window half-hour's reduction as a share of the megawatts delivered in the credited half-hours (the
    half-hours the export lacks left out)."""
    d = ev["delivered"].values.astype(float)
    return {h: _through_origin(ev["win_" + h].values.astype(float), d) for h in WINDOW}


def comeback(ev):
    """The rise in each of the four half-hours after the window per megawatt delivered (through the origin)."""
    d = ev["delivered"].values.astype(float)
    return {h: _through_origin(ev["post_" + h].values.astype(float), d) for h in POST}


def with_flex(profile, delivered, shape, back):
    """The design day's half-hours with `delivered` megawatts taken in the credited half-hours."""
    out = {}
    for h, v in profile.items():
        out[h] = v - shape.get(h, 0.0) * delivered + back.get(h, 0.0) * delivered
    return out


def peak_of(day):
    h = max(day, key=lambda k: day[k])
    return h, day[h]


# ------------------------------------------------------------------------------------------------ the spread
def cold_spread(ev, below=-1.0, form="linear", noise_sd_by_zone=None, net_noise=True):
    """Day-to-day spread of the available megawatts as a share of their level, from the days at or below `below`:
    the scatter of delivered over contracted about its line, relative to the line, less what the baseline's own
    noise puts there (the same measurement on days with nothing scheduled)."""
    share, n, beta, resid, e = cold_share(ev, below=below, form=form)
    mu = _basis(e["T"].values, form) @ beta
    rel = resid / mu
    raw = float(np.sqrt(np.sum(rel ** 2) / (len(rel) - len(beta))))
    if not net_noise or noise_sd_by_zone is None:
        return raw, raw, n
    noise = np.array([noise_sd_by_zone[z] for z in e["zone"]]) / (e["contract"].values * mu)
    var = raw ** 2 - float(np.mean(noise ** 2))
    return math.sqrt(max(var, 1e-6)), raw, n


def one_in_ten(profile, delivered, shape, back, cv_avail, cv_base, n=20001):
    """The level the day's highest half-hour stays under on nine design days in ten: the baseline's day effect and
    the provider's availability each drawn on an even grid of their own spread (independent, normal), the day
    recomputed half-hour by half-hour."""
    q = (np.arange(n) + 0.5) / n
    from statistics import NormalDist
    nd = NormalDist()
    g = 141
    zq = np.array([nd.inv_cdf((i + 0.5) / g) for i in range(g)])
    hs = list(profile)
    P = np.array([profile[h] for h in hs])
    net = np.array([back.get(h, 0.0) - shape.get(h, 0.0) for h in hs])
    peaks = []
    for zb in zq:
        base = P * (1 + cv_base * zb)
        for za in zq:
            a = delivered * (1 + cv_avail * za)
            peaks.append(float(np.max(base + net * a)))
    peaks = np.sort(np.array(peaks))
    return float(np.quantile(peaks, ASSURANCE)), float(np.mean(peaks)), float(np.mean(peaks > 0))


def exceed_share(profile, delivered, shape, back, cv_avail, cv_base, firm, g=141):
    from statistics import NormalDist
    nd = NormalDist()
    zq = np.array([nd.inv_cdf((i + 0.5) / g) for i in range(g)])
    hs = list(profile)
    P = np.array([profile[h] for h in hs])
    net = np.array([back.get(h, 0.0) - shape.get(h, 0.0) for h in hs])
    over = 0
    for zb in zq:
        base = P * (1 + cv_base * zb)
        for za in zq:
            over += float(np.max(base + net * delivered * (1 + cv_avail * za))) > firm
    return over / float(g * g)


# ------------------------------------------------------------------------------------------------ the chain, end to end
ZONE_PROVIDER = {"PS40617": "Corvane Flex Ltd", "PS41108": "Quillon Energy Services Ltd",
                 "PS41474": "Quillon Energy Services Ltd", "PS41236": "Corvane Flex Ltd"}
ZONE_LABEL = {"PS40617": "Ashcombe Road CMZ", "PS41108": "Charlecote Way CMZ", "PS41474": "Fenwick Street CMZ",
              "PS41236": "Hartwell Common CMZ"}
ZONES = sorted(ZONE_LABEL, key=lambda c: ZONE_LABEL[c])
TRAIN_WINTERS = ("2023/24", "2024/25")
TEST_WINTER = "2025/26"
COLD = -1.0          # the days on which every call outran what its provider had available
FREEZING = 0.0       # the backtest counts its range on last winter's days below 0 C
RANGE = 0.80         # the range the backtest counts last winter's events inside
G_GRID = 141


def conform(X):
    """Adds the working views: local half-hours, daily means, contracted megawatts by zone and winter, awards."""
    if "_prep" not in X:
        X["_prep"] = prepare(X["demand"])
    if "_tm" not in X:
        X["_tm"] = daily_mean(X["weather"])
    if "contract" not in X:
        X["contract"] = {(c, w): X["previous"][X["names"][c]][w] for c in ZONES for w in X["previous"][X["names"][c]]}
    if "award" not in X:
        X["award"] = {c: X["contracts"][X["names"][c]] for c in ZONES}
    return X


def _zq(g=G_GRID):
    from statistics import NormalDist
    nd = NormalDist()
    return np.array([nd.inv_cdf((i + 0.5) / g) for i in range(g)])


def day_quantile(profile, delivered, shape, back, cv_avail, cv_base, q=ASSURANCE, g=G_GRID):
    """The q-quantile of the design day's highest half-hour, the baseline's day effect and the megawatts available
    each on an even grid of their own normal spread, independent."""
    zq = _zq(g)
    hs = list(profile)
    P = np.array([profile[h] for h in hs])
    net = np.array([back.get(h, 0.0) - shape.get(h, 0.0) for h in hs])
    base = P[None, :] * (1 + cv_base * zq)[:, None]                       # g x H
    a = delivered * (1 + cv_avail * zq)                                    # g
    peaks = (base[:, None, :] + net[None, None, :] * a[None, :, None]).max(axis=2).ravel()
    return float(np.quantile(peaks, q)), peaks


def provider_fit(ev, noise, below=COLD, form="linear", winters=None):
    """One provider's cold days: the line of delivered over contracted against temperature, its value on the design
    day, the day-to-day spread about it net of the baseline's noise, the window's shape and what comes back."""
    e = ev if winters is None else ev[ev["winter"].isin(winters)]
    share, n, beta, resid, cold = cold_share(e, below=below, form=form)
    cv, raw, _ = cold_spread(e, below=below, form=form, noise_sd_by_zone=noise)
    return dict(share=share, beta=[float(b) for b in beta], form=form, n_cold=int(n), cv=cv, cv_raw=raw,
                shape=window_shape(e), back=comeback(e),
                cold_dates=int(cold["date"].nunique()), cold_met=int(met(cold).sum()))


def line_share(fit, T):
    return _basis(np.atleast_1d(np.asarray(T, float)), fit["form"]) @ np.array(fit["beta"])


def backtest(ev, noise, below=COLD, form="linear", model="share", rng_q=RANGE):
    """Winter 2025/26's completed events predicted from the two winters before: megawatts delivered in the credited
    half-hours as the lesser of the megawatts scheduled and the share of the contract available that day. Returns
    the mean absolute error, the mean error, and the share of the events inside the central `rng_q` range."""
    tr = ev[ev["winter"].isin(TRAIN_WINTERS)]
    te = ev[ev["winter"] == TEST_WINTER]
    f = provider_fit(tr, noise, below=below, form=form)
    # on the days a call was met, how far the megawatts measured sat from the megawatts scheduled (by zone)
    mt = tr[met(tr)]
    track = {z: float(np.std((mt[mt["zone"] == z]["delivered"] - mt[mt["zone"] == z]["scheduled"]).values)) for z in sorted(set(tr["zone"]))}
    s = te["scheduled"].values.astype(float)
    y = te["delivered"].values.astype(float)
    C = te["contract"].values.astype(float)
    mu = line_share(f, te["T"].values)
    if model == "share":
        avail = mu * C
        pred = np.minimum(s, avail)
    elif model == "per_mw":
        pred = np.zeros(len(te))
        for z in sorted(set(te["zone"])):
            trz = tr[tr["zone"] == z]
            m = (te["zone"] == z).values
            sz = trz["scheduled"].values.astype(float)
            B = np.column_stack([sz, sz * trz["T"].values])
            b, *_ = np.linalg.lstsq(B, trz["delivered"].values.astype(float), rcond=None)
            pred[m] = (b[0] + b[1] * te["T"].values[m]) * s[m]
        avail = None
    else:
        raise ValueError(model)
    err = pred - y
    inside, n_in, rows = None, 0, []
    cold = (te["T"] < FREEZING).values
    if model == "share":
        # on last winter's freezing days: was the megawatts delivered inside the central range the earlier winters
        # gave, the lesser of the megawatts scheduled (give or take how closely met calls tracked their schedule) and
        # the line's share of the contract (give or take the day-to-day scatter measured about it)
        z = _zq(2001)
        lo_z, hi_z = np.quantile(z, (1 - rng_q) / 2.0), np.quantile(z, 1 - (1 - rng_q) / 2.0)
        tk = np.array([track[zz] for zz in te["zone"]])
        lo = np.minimum(s + tk * lo_z, avail * (1 + f["cv_raw"] * lo_z))
        hi = np.minimum(s + tk * hi_z, avail * (1 + f["cv_raw"] * hi_z))
        ins = (y >= lo) & (y <= hi)
        inside = float(np.mean(ins[cold]))
        n_in = int(np.sum(ins[cold]))
        rows = [dict(date=te["date"].values[i], zone=te["zone"].values[i], T=float(te["T"].values[i]), scheduled=float(s[i]),
                     contract=float(C[i]), predicted=float(pred[i]), low=float(lo[i]), high=float(hi[i]),
                     delivered=float(y[i]), inside=bool(ins[i])) for i in range(len(te)) if cold[i]]
    return dict(n=int(len(te)), mae=float(np.mean(np.abs(err))), bias=float(np.mean(err)), inside=inside, n_inside=n_in,
                n_cold=int(cold.sum()), mae_cold=float(np.mean(np.abs(err[cold]))), bias_cold=float(np.mean(err[cold])),
                fit=f, rows=rows)


def golden_from(X, below=COLD, form="linear", pooled=True, net_noise=True, base=BASE_T, comeback_on=True,
                spread="scaled", use_switching=True, credit="mean"):
    """The golden on the parsed pack, result by result. Options name the reasonable variants the bands are set by."""
    X = conform(X)
    prep, tm = X["_prep"], X["_tm"]
    evs = {c: event_table(X, c, exclude_switch_days=use_switching, credit=credit) for c in ZONES}
    noise = {c: placebo_sd(X, c)[0] for c in ZONES}
    provs = sorted(set(ZONE_PROVIDER.values()))
    pev = {p: pd.concat([evs[c] for c in ZONES if ZONE_PROVIDER[c] == p], ignore_index=True) for p in provs}
    fits = {p: provider_fit(pev[p], noise if net_noise else None, below=below, form=form) for p in provs}
    if not pooled:
        zfits = {c: provider_fit(evs[c], noise if net_noise else None, below=below, form=form) for c in ZONES}
    zones = []
    for c in ZONES:
        p = ZONE_PROVIDER[c]
        f = fits[p] if pooled else zfits[c]
        excl = set(X["events"][X["events"]["zone"] == c]["date"]) | (switch_dates(X.get("switching"), c) if use_switching else set())
        d26, slope, cvb, nb = design_peak(prep, tm, c, exclude=excl, base=base, winters=["2025/26"])
        r1, r2 = X["rates"][c]
        before = forecast(d26, r1, r2, X["growth"].get(c, 0.0))
        g = before / d26
        raw = design_profile(prep, tm, c, excl, None, None, base=base)
        top = max(raw.values())
        prof = {h: v * before / top for h, v in raw.items()}    # the day's highest half-hour is the guideline's figure
        award, firm = X["award"][c], X["firm"][c]
        delivered = f["share"] * award
        shape, back = fits[p]["shape"], (fits[p]["back"] if comeback_on else {})
        day = with_flex(prof, delivered, shape, back)
        hh, peak = peak_of(day)
        cv_a = f["cv"]
        if spread == "constant":      # the megawatts of scatter seen in the record carried unchanged to the award
            e = evs[c][evs[c]["T"] <= below]
            cv_a = float(np.std(e["delivered"].values - line_share(f, e["T"].values) * e["contract"].values)) / delivered
        p90, peaks = day_quantile(prof, delivered, shape, back, cv_a, cvb)
        zones.append(dict(zone=ZONE_LABEL[c], primary=X["names"][c], code=c, provider=p, award=award, firm=firm,
                          d26=d26, slope=slope, cv_base=cvb, n_base_days=nb, before=before, profile=prof,
                          share=f["share"], delivered=delivered, peak_hh=hh, peak=peak, in_window=day["18:00"],
                          after_window=day["20:00"], off_peak=before - peak, p90=p90, mean_peak=float(np.mean(peaks)),
                          exceed=float(np.mean(peaks > firm)), over=bool(p90 > firm), over_by=p90 - firm,
                          not_available=award - delivered, comeback_loss=delivered - (before - peak),
                          n_events=int(len(evs[c])), n_cold=int((evs[c]["T"] <= below).sum()),
                          per_scheduled=rate_per_scheduled(evs[c]), noise=noise[c]))
    bt = {p: backtest(pev[p], noise) for p in provs}
    allev = pd.concat([pev[p] for p in provs], ignore_index=True)
    te_n = sum(bt[p]["n"] for p in provs)
    nc = sum(bt[p]["n_cold"] for p in provs)
    bt_all = dict(n=te_n, mae=sum(bt[p]["mae"] * bt[p]["n"] for p in provs) / te_n,
                  bias=sum(bt[p]["bias"] * bt[p]["n"] for p in provs) / te_n, n_cold=nc,
                  n_inside=sum(bt[p]["n_inside"] for p in provs),
                  inside=sum(bt[p]["n_inside"] for p in provs) / float(nc),
                  mae_cold=sum(bt[p]["mae_cold"] * bt[p]["n_cold"] for p in provs) / float(nc),
                  bias_cold=sum(bt[p]["bias_cold"] * bt[p]["n_cold"] for p in provs) / float(nc))
    cold_rows = []
    for c in ZONES:
        e = evs[c][evs[c]["T"] <= below]
        for r in e.itertuples():
            cold_rows.append(dict(date=r.date, zone=ZONE_LABEL[c], T=r.T, scheduled=r.scheduled, contract=r.contract,
                                  delivered=r.delivered, share=r.delivered / r.contract))
    cold_rows.sort(key=lambda r: (r["date"], r["zone"]))
    return dict(zones=zones, providers=fits, backtest=bt, backtest_all=bt_all, events=evs, noise=noise, cold_rows=cold_rows,
                commit=[z["primary"] for z in zones if z["over"]],
                record=dict(completed={c: int(len(evs[c])) for c in ZONES}))
