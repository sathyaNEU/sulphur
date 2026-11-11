"""task10 architecture 7: the analyst's computations on clean tables (the truth's or the parsed pack's).

Every result of the design note's chain is a function here, with the hurried methods beside the golden's, so
checks.py can run each on the clean truth and on the pack and effort_passes.py can price them:

  R1 each zone primary's design-day demand in winter 2025/26 (every working weekday at the design temperature,
     with or without a service): mornings on every working weekday against temperature, evenings against mornings
     on the days no service ran
  R2 what the register's connections will have added by the assessment date (each customer's build-up from the
     large-customer summary, the customers still to connect on their type's)
  R3 demand before flexibility in winter 2027/28
  R4 the megawatts each provider will have commissioned by the assessment date (sites still to come, each on its
     class's record of commissioning across the licence area's register)
  R5 the share of its commissioned megawatts each provider has available on the design day
  R6 megawatts each contract delivers at 17:00 to 18:00; R7 megawatts off the day's peak; R8 the expected peak;
  R9 the level it stays under on nine design days in ten; R10 the primaries to reinforce
"""
import datetime as dt
import math

import numpy as np
import pandas as pd

UTC = dt.timezone.utc
T_DESIGN = -3.0
H48 = ["%02d:%02d" % ((i + 1) // 2, 30 if (i + 1) % 2 else 0) for i in range(48)]   # half-hours ending 00:30 ... 24:00
MORNING = H48[13:31]          # half-hours ending 07:00 ... 15:30
MORNING_LATE = H48[17:30]     # half-hours ending 09:00 ... 15:00
CREDIT_HH = ("17:30", "18:00")
WINDOW = ("16:30", "17:00", "17:30", "18:00", "18:30", "19:00", "19:30")   # half-hours ending, local
POST = ("20:00", "20:30", "21:00", "21:30")
IW = [H48.index(h) for h in WINDOW]
IP = [H48.index(h) for h in POST]
IC = [H48.index(h) for h in CREDIT_HH]
BANK_HOLIDAYS = {dt.date(2023, 12, 25), dt.date(2023, 12, 26), dt.date(2024, 1, 1), dt.date(2024, 3, 29),
                 dt.date(2024, 12, 25), dt.date(2024, 12, 26), dt.date(2025, 1, 1),
                 dt.date(2025, 12, 25), dt.date(2025, 12, 26), dt.date(2026, 1, 1)}
ASSESS = dt.date(2028, 1, 15)
BASIS = dt.date(2026, 1, 15)
ASSURANCE = 0.90      # the guideline: within firm capacity on nine design days in ten
LATEST = "2025/26"


def winter_of(d):
    return "%d/%02d" % ((d.year, (d.year + 1) % 100) if d.month >= 7 else (d.year - 1, d.year % 100))


def _christmas(d):
    return (d.month == 12 and d.day >= 24) or (d.month == 1 and d.day <= 2)


def workday(d):
    """A weekday outside the bank holidays and the Christmas and New Year period (24 December to 2 January)."""
    return d.weekday() < 5 and d not in BANK_HOLIDAYS and not _christmas(d)


def months_between(d0, d1):
    return (d1 - d0).days / 30.4375


def _isdate(x):
    return x is not None and not (isinstance(x, float) and math.isnan(x)) and x is not pd.NaT and pd.notna(x)


# ------------------------------------------------------------------------------------------------ preparation
def prepare(demand):
    """Adds the local date of each half-hour's start and the local half-hour label 'HH:MM' (its end)."""
    d = demand.copy()
    end = pd.DatetimeIndex(d["t_utc"]).tz_convert("Europe/London")
    start = end - pd.Timedelta(minutes=30)
    d["ldate"] = start.date
    lab = end.strftime("%H:%M")
    d["hh"] = np.where(lab == "00:00", "24:00", lab)
    return d


def daily_mean(weather):
    """The mean of the station's hourly readings over each GMT day, for days with at least 20 of their 24 readings."""
    w = weather.copy()
    w["date"] = [t.date() for t in w["t_utc"]]
    g = w.groupby("date")["temp_c"]
    n = g.size()
    return g.mean()[n >= 20]


def switch_dates(switching, code):
    """Local dates on which a logged 11 kV transfer was in place at the primary (either side of the open point)."""
    out = set()
    if switching is None or len(switching) == 0:
        return out
    for r in switching.itertuples():
        if code not in (r.frm, r.to):
            continue
        a = pd.Timestamp(r.start).tz_convert("Europe/London").date()
        b = pd.Timestamp(r.end).tz_convert("Europe/London").date()
        d = a
        while d <= b:
            out.add(d)
            d += dt.timedelta(days=1)
    return out


def day_frame(X, code, morning=MORNING):
    """One row per local day at a primary: its 48 half-hours, the day's mean temperature, its morning mean (the
    half-hours before any service window), and whether a service ran or a transfer was in place."""
    prep = X["prep"]
    s = prep[prep["code"] == code]
    P = s.pivot_table(index="ldate", columns="hh", values="mw", aggfunc="mean").reindex(columns=H48)
    tm = X["tmean"]
    P = P[P.index.isin(tm.index)]
    D = pd.DataFrame(index=P.index)
    D["T"] = [tm[d] for d in P.index]
    D["winter"] = [winter_of(d) for d in P.index]
    D["work"] = [workday(d) for d in P.index]
    D["M"] = P[list(morning)].mean(axis=1).where(P[list(morning)].notna().sum(axis=1) >= len(morning) - 2)
    D["dj"] = [(d - dt.date(d.year if d.month < 7 else d.year + 1, 1, 15)).days / 100.0 for d in P.index]
    ev = X["events"]
    mine = ev[(ev["zone"] == code) & (ev["status"] == "Completed") & (ev["scheduled_mw"] > 0)]
    served = set(mine["date"])
    D["service"] = [d in served for d in D.index]
    smw = dict(zip(mine["date"], mine["scheduled_mw"]))
    D["sched"] = [float(smw.get(d, 0.0)) for d in D.index]
    sw = switch_dates(X.get("switching"), code)
    D["switch"] = [d in sw for d in D.index]
    D["complete"] = P.notna().sum(axis=1) >= 46
    return D, P


# ------------------------------------------------------------------------------------------------ R1 the demand side
SPLINE_KNOTS = (-3.0, 0.0, 2.5, 6.0)


def _rcs(T, knots):
    """Restricted cubic spline basis in temperature (straight below the first knot and above the last)."""
    T = np.asarray(T, float)
    k = list(knots)
    cols = [T]
    p3 = lambda x: np.maximum(x, 0.0) ** 3
    for j in range(len(k) - 2):
        cols.append((p3(T - k[j]) - p3(T - k[-2]) * (k[-1] - k[j]) / (k[-1] - k[-2])
                     + p3(T - k[-1]) * (k[-2] - k[j]) / (k[-1] - k[-2])) / (k[-1] - k[0]) ** 2)
    return np.column_stack(cols)


def _levels(d, trend):
    ws = sorted(set(d["winter"]))
    cols = [(d["winter"] == w).values.astype(float) for w in ws]
    if trend:      # each winter's level may drift through the winter; the level is read at 15 January
        cols += [((d["winter"] == w).values * d["dj"].values) for w in ws]
    return ws, np.column_stack(cols)


def _mfit(D, form, winters=None, trend=False):
    """Mornings on every working weekday against the day's temperature: winter levels, a slope, and a second slope
    below a knee the fit chooses (or a square term below it, or a straight line only, or the cold days alone)."""
    d = D[D["work"] & ~D["switch"] & D["M"].notna()]
    if winters:
        d = d[d["winter"].isin(winters)]
    ws, FE = _levels(d, trend)
    nf = FE.shape[1]
    T = d["T"].values
    y = d["M"].values

    def design(Tv, k):
        if form == "spline":       # a smooth curve: a restricted cubic spline, straight beyond its outer knots
            return _rcs(Tv, SPLINE_KNOTS)
        if form == "hinge":
            return np.column_stack([Tv, np.maximum(0.0, k - Tv)])
        if form == "quadratic":
            return np.column_stack([Tv, np.maximum(0.0, k - Tv) ** 2])
        if form == "linear":
            return np.column_stack([Tv])
        raise ValueError(form)
    if form == "cold":           # a straight line through the days at 1 C or colder, read at the design temperature
        c = (d["T"] <= 1.0).values
        Xc = np.column_stack([FE[c], T[c]])
        b, *_ = np.linalg.lstsq(Xc, y[c], rcond=None)
        lev = dict(zip(ws, b[:len(ws)]))
        fitted = Xc @ b
        return dict(form=form, levels=lev, at=lambda Tv, w=LATEST: lev[w] + b[-1] * Tv, knee=None,
                    rel=(y[c] - fitted) / fitted, n=int(c.sum()), T=T[c], resid=y[c] - fitted)
    best = None
    grid = np.arange(-1.0, 6.01, 0.5) if form not in ("linear", "spline") else [0.0]
    for k in grid:
        Xk = np.column_stack([FE, design(T, k)])
        b, *_ = np.linalg.lstsq(Xk, y, rcond=None)
        sse = float(((y - Xk @ b) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, k, b, Xk)
    _, k, b, Xk = best
    lev = dict(zip(ws, b[:len(ws)]))
    fitted = Xk @ b

    def at(Tv, w=LATEST):
        return lev[w] + float((design(np.array([Tv], float), k) @ b[nf:])[0])
    return dict(form=form, levels=lev, at=at, knee=float(k) if form in ("hinge", "quadratic") else None, rel=(y - fitted) / fitted,
                n=len(y), coef=b[nf:], T=T, resid=y - fitted)


def _efit(D, P, m=None, winters=None):
    """Each half-hour on the working weekdays no service ran, against the morning expected at the day's temperature,
    with winter levels. With the morning model m, each day's half-hours are first divided by how far its own morning
    ran above or below the morning expected (so a day that ran high or low all day does not tilt the relation);
    without it, each half-hour is regressed on the day's own morning."""
    d = D[D["work"] & ~D["service"] & ~D["switch"] & D["M"].notna() & D["complete"]]
    if winters:
        d = d[d["winter"].isin(winters)]
    ws = sorted(set(d["winter"]))
    FE = np.column_stack([(d["winter"] == w).values.astype(float) for w in ws])
    Y = P.loc[d.index].values
    if m is not None:
        mhat = np.array([m["at"](t, w) for t, w in zip(d["T"].values, d["winter"].values)])
        f = d["M"].values / mhat
        Y = Y / f[:, None]
        x = mhat
    else:
        x = d["M"].values
    Xm = np.column_stack([FE, x])
    ok = ~np.isnan(Y).any(axis=1)
    B, *_ = np.linalg.lstsq(Xm[ok], Y[ok], rcond=None)
    resid = Y[ok] - Xm[ok] @ B
    return dict(winters=ws, alpha={w: B[i] for i, w in enumerate(ws)}, beta=B[-1], sd=np.std(resid, axis=0), n=int(ok.sum()),
                coldest=float(d["T"].min()), n_latest=int((d["winter"] == LATEST).sum()), ratio=m is not None,
                coldest_latest=float(d[d["winter"] == LATEST]["T"].min()) if (d["winter"] == LATEST).any() else float("nan"))


def anchored(D, P, form="spline", winters=None, trend=False, anchor="ratio"):
    """The design-day profile on the latest winter's footing: the morning expected at the design temperature from
    every working weekday, carried to each half-hour by its relation to the morning on the days no service ran."""
    # the line through the cold days alone answers only for the cold end: the days' own running is still read
    # against the curve through every day
    m = _mfit(D, "spline" if form == "cold" else form, winters, trend)
    e = _efit(D, P, m if anchor == "ratio" else None, winters)
    mstar = (_mfit(D, "cold", winters, trend) if form == "cold" else m)["at"](T_DESIGN, LATEST)
    w = LATEST if LATEST in e["alpha"] else e["winters"][-1]
    prof = e["alpha"][w] + e["beta"] * mstar
    return dict(profile=np.asarray(prof, float), mstar=float(mstar), mfit=m, efit=e, level_winter=w,
                rel_sd=float(np.std(m["rel"], ddof=4)))


def counterfactual(model, D, date):
    """What a day's half-hours would have been with no service, from its own morning."""
    e, m = model["efit"], model["mfit"]
    w = D.loc[date, "winter"]
    we = w if w in e["alpha"] else e["winters"][-1]
    if e["ratio"]:
        wm = w if w in m["levels"] else sorted(m["levels"])[-1]
        mhat = m["at"](D.loc[date, "T"], wm)
        return (e["alpha"][we] + e["beta"] * mhat) * (D.loc[date, "M"] / mhat)
    return e["alpha"][we] + e["beta"] * D.loc[date, "M"]


def line_profile(D, P, mode="pooled", at=T_DESIGN):
    """The hurried reading: each half-hour against temperature on the working weekdays no service ran, a straight
    line carried to the design temperature (winter levels and one slope; the latest winter alone; or with a square)."""
    d = D[D["work"] & ~D["service"] & ~D["switch"] & D["complete"]]
    if mode == "sched":        # every working weekday, with the megawatts scheduled as a regressor
        d = D[D["work"] & ~D["switch"] & D["complete"]]
    if mode == "latest":
        d = d[d["winter"] == LATEST]
    ws = sorted(set(d["winter"]))
    FE = np.column_stack([(d["winter"] == w).values.astype(float) for w in ws])
    T = d["T"].values
    cols = [FE, T[:, None]] + ([T[:, None] ** 2] if mode == "quadratic" else []) + ([d["sched"].values[:, None]] if mode == "sched" else [])
    Xm = np.column_stack(cols)
    Y = P.loc[d.index].values
    ok = ~np.isnan(Y).any(axis=1)
    Xm, Y, T = Xm[ok], Y[ok], T[ok]
    B, *_ = np.linalg.lstsq(Xm, Y, rcond=None)
    i = ws.index(LATEST) if LATEST in ws else len(ws) - 1
    prof = B[i] + B[len(ws)] * at + (B[len(ws) + 1] * at * at if mode == "quadratic" else 0.0)
    pk = Y.max(axis=1)
    fit_pk = (Xm @ B).max(axis=1)
    return dict(profile=np.asarray(prof, float), n=len(T), coldest=float(T.min()),
                n_latest=int((d["winter"] == LATEST).sum()),
                rel_sd=float(np.std((pk - fit_pk) / fit_pk, ddof=len(ws) + 1)), winters=ws,
                alpha={w: B[j] for j, w in enumerate(ws)}, slope=B[len(ws)])


# ------------------------------------------------------------------------------------------------ R2 connections
def conn_frame(X):
    """The register's connections with each energised customer's monthly evening draw as a share of its agreed kVA."""
    C = X["connections"].copy()
    M = X["monitor"].merge(C[["conn", "type", "kva", "energised"]], on="conn")
    M["age"] = [months_between(e, m + dt.timedelta(days=14)) for e, m in zip(M["energised"], M["month"])]
    M["ratio"] = M["evening_kw"] / M["kva"]
    return C, M


def _g(a, tau, k):
    return 1.0 - np.exp(-(np.maximum(np.asarray(a, float), 0.0) / tau) ** k)


def buildup_fit(M, by_type=True, shape="weibull"):
    """Each type's established draw as a share of agreed kVA and its build-up with age: least squares over a grid of
    the build-up's scale and shape, the level in closed form. Types the summary holds too thinly take the pooled fit."""
    def fit(d):
        a, y = d["age"].values, d["ratio"].values
        best = None
        for tau in np.linspace(4.0, 32.0, 57):
            for k in (np.linspace(0.8, 2.2, 15) if shape == "weibull" else (1.0,)):
                g = _g(a, tau, k)
                U = float((g * y).sum() / max((g * g).sum(), 1e-9))
                sse = float(((y - U * g) ** 2).sum())
                if best is None or sse < best[0]:
                    best = (sse, U, tau, k)
        return dict(U=best[1], tau=best[2], k=best[3], n=len(d), n_conn=int(d["conn"].nunique()))
    pooled = fit(M)
    out = {"_pooled": pooled}
    if by_type:
        for t, d in M.groupby("type"):
            out[t] = fit(d) if d["conn"].nunique() >= 3 and d["age"].max() >= 24 else dict(pooled, borrowed=True)
    return out


def connections_add(X, code, method="own", fits=None, C=None, M=None, months=3):
    """Megawatts the register's connections at a primary will have added to its evening peak between the latest
    winter's assessment date and the assessment date of the winter assessed.
      own      each energised customer on its own level, carried up its type's build-up; customers still to connect
               on their type's level and build-up (the golden)
      type     every customer on its type's level and build-up
      pooled   one level and build-up for every type
      new_buildup   the type's level and build-up, for the customers energised since the latest winter only
      mature   the type's established level, no build-up, customers energised since the latest winter only
      ratio    one average of what the energised customers draw today over their agreed kVA, the same customers
      full     agreed capacity in full at a power factor of 0.95, the same customers
      observed every customer at what the summary's latest months show (no further build-up); customers still to
               connect at their type's established level"""
    if C is None:
        C, M = conn_frame(X)
    fits = fits or buildup_fit(M)
    mine = C[C["code"] == code]
    total, rows = 0.0, []
    avg_ratio = None
    if method == "ratio":
        last = M.sort_values("month").groupby("conn").tail(1)
        avg_ratio = float(last["ratio"].mean())
    for c in mine.itertuples():
        energised = _isdate(c.energised)
        start = c.energised if energised else c.planned
        if not _isdate(start) or start >= ASSESS:
            continue
        new = start > BASIS
        f = fits.get(c.type, fits["_pooled"]) if method != "pooled" else fits["_pooled"]
        a1 = months_between(start, ASSESS)
        a0 = months_between(start, BASIS)
        if method == "observed":
            mm = M[M["conn"] == c.conn].sort_values("month") if energised else None
            if energised and mm is not None and len(mm):
                lvl1 = c.kva * float(mm.tail(3)["ratio"].mean())
                seen = mm[(mm["month"] >= dt.date(2025, 12, 1)) & (mm["month"] <= dt.date(2026, 2, 1))]
                lvl0 = c.kva * float(seen["ratio"].mean()) if (a0 > 0 and len(seen)) else 0.0
                add = lvl1 - lvl0
            else:
                add = c.kva * f["U"]
        elif method in ("full", "ratio", "mature", "new_buildup"):
            if not new:
                continue
            if method == "full":
                add = c.kva * 0.95
            elif method == "ratio":
                add = c.kva * avg_ratio
            elif method == "mature":
                add = c.kva * f["U"]
            else:
                add = c.kva * f["U"] * float(_g(a1, f["tau"], f["k"]))
        else:
            scale = 1.0
            mm = M[M["conn"] == c.conn].sort_values("month") if energised else None
            if method == "own" and energised and mm is not None and len(mm) >= 6:
                recent = mm.tail(months)
                exp = f["U"] * _g(recent["age"].values, f["tau"], f["k"])
                if exp.mean() > 0.05 * f["U"]:
                    scale = float(np.clip(recent["ratio"].mean() / exp.mean(), 0.5, 1.9))
            lvl1 = c.kva * scale * f["U"] * float(_g(a1, f["tau"], f["k"]))
            lvl0 = 0.0
            if energised and a0 > 0:
                seen = mm[(mm["month"] >= dt.date(2025, 12, 1)) & (mm["month"] <= dt.date(2026, 2, 1))] if mm is not None else None
                if method == "own" and seen is not None and len(seen) >= 2:
                    lvl0 = c.kva * float(seen["ratio"].mean())
                else:
                    lvl0 = c.kva * scale * f["U"] * float(_g(a0, f["tau"], f["k"]))
            add = lvl1 - lvl0
        total += add
        rows.append((c.conn, c.type, int(c.kva), start, bool(energised), add / 1000.0))
    return total / 1000.0, rows


# ------------------------------------------------------------------------------------------------ R4 commissioning
def in_service(assets, zone, day):
    """Megawatts a zone's provider had commissioned and in service on a day."""
    a = assets[assets["zone"] == zone]
    tot = 0.0
    for r in a.itertuples():
        if _isdate(r.commissioned) and r.commissioned <= day and not (_isdate(r.left) and r.left <= day):
            tot += r.kw
    return tot / 1000.0


def register_as_at(assets, as_at):
    """The register as it stood on a day: sites signed by then, with only what had happened by then."""
    a = assets[np.array([s <= as_at for s in assets["signed"]], bool)].copy()
    for col in ("commissioned", "lost", "left"):
        a[col] = pd.Series([c if (_isdate(c) and c <= as_at) else None for c in a[col]], index=a.index, dtype=object)
    return a


def _records(d, as_at, losses):
    rec = []
    for r in d.itertuples():
        if _isdate(r.commissioned):
            rec.append(((r.commissioned - r.planned).days, 1))
        elif _isdate(r.lost):
            if losses == "drop":
                continue
            rec.append(((r.lost - r.planned).days, 2 if losses == "competing" else 0))
        else:
            rec.append(((as_at - r.planned).days, 0))
    return rec


def incidence(assets, as_at, group=("cls",), losses="competing"):
    """For sites whose planned commissioning date has passed: the share commissioned, and the share lost, by days
    since the planned date, with the sites still to come counted for as long as they have been watched."""
    a = assets[np.array([p <= as_at for p in assets["planned"]], bool)]
    out = {}
    keys = sorted(set(map(tuple, a[list(group)].values.tolist()))) if group else [()]
    for g in keys:
        d = a
        for col, val in zip(group, g):
            d = d[d[col] == val]
        rec = _records(d, as_at, losses)
        if not rec:
            continue
        t_arr = np.array([t for t, _ in rec])
        e_arr = np.array([e for _, e in rec])
        S, F1, F2 = 1.0, 0.0, 0.0
        curve = []
        for t in sorted(set(t_arr[e_arr > 0].tolist())):
            at_risk = int((t_arr >= t).sum())
            d1 = int(((t_arr == t) & (e_arr == 1)).sum())
            d2 = int(((t_arr == t) & (e_arr == 2)).sum())
            if at_risk == 0:
                break
            F1 += S * d1 / at_risk
            F2 += S * d2 / at_risk
            S *= 1.0 - (d1 + d2) / at_risk
            curve.append((t, F1, F2))
        late = t_arr[e_arr == 1]
        out[g] = dict(curve=curve, n=len(rec), commissioned=int((e_arr == 1).sum()), lost=int((e_arr == 2).sum()),
                      median_late=float(np.median(late)) if len(late) else float("nan"))
    return out


def _at(curve, t):
    f1 = f2 = 0.0
    for tt, a, b in curve:
        if tt > t:
            break
        f1, f2 = a, b
    return f1, f2


def _chance(c, planned, as_at, by):
    elapsed = (as_at - planned).days
    horizon = (by - planned).days
    if horizon <= 0:
        return 0.0
    f1h, _ = _at(c["curve"], horizon)
    if elapsed <= 0:
        return f1h
    f1e, f2e = _at(c["curve"], elapsed)
    alive = 1.0 - f1e - f2e
    return max(f1h - f1e, 0.0) / alive if alive > 1e-9 else 0.0


def lognormal_by_class(assets, as_at):
    """Each class's days late as a lognormal fitted to the sites whose planned date has passed (the sites still to
    come counted as later than they have been watched), with the share of sites lost."""
    a = assets[np.array([p <= as_at for p in assets["planned"]], bool)]
    out = {}
    for cls, d in a.groupby("cls"):
        t, e = [], []
        nl = 0
        for r in d.itertuples():
            if _isdate(r.commissioned):
                t.append(max((r.commissioned - r.planned).days, 1))
                e.append(1)
            elif _isdate(r.lost):
                nl += 1
            else:
                t.append(max((as_at - r.planned).days, 1))
                e.append(0)
        t, e = np.log(np.array(t, float)), np.array(e)
        mu, s = float(t[e == 1].mean()), float(t[e == 1].std()) or 0.5
        for _ in range(200):       # expectation steps for the sites still to come
            z = (t - mu) / s
            lam = np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi) / np.maximum(1.0 - _norm_cdf(z), 1e-12)
            ey = np.where(e == 1, t, mu + s * lam)
            ey2 = np.where(e == 1, t * t, mu * mu + s * s + s * (t + mu) * lam)
            nmu = float(ey.mean())
            ns = math.sqrt(max(float(ey2.mean() - nmu * nmu), 1e-6))
            if abs(nmu - mu) < 1e-9 and abs(ns - s) < 1e-9:
                break
            mu, s = nmu, ns
        out[cls] = dict(mu=mu, sigma=s, lost=nl / max(len(d), 1), n=len(d))
    return out


def expected_commissioned(assets, zone, as_at, by, method="class", contracted=None, history=None):
    """Megawatts a zone's provider can be expected to have commissioned and in service by a day, from the register as
    at as_at.
      class       sites still to come, each on its class's record of commissioning across the register (the golden)
      class_provider   the same on the record of its class with its own provider
      lognormal   each class's days late as a fitted lognormal, with its share of sites lost
      class_median  every site still to come moved by its class's median days late
      class_done  every site still to come at the share of its class's commissioned sites that were no later than
                  the days it has to the day asked about (the sites still outstanding and withdrawn left out of
                  the record)
      class_done_cond   the same share among the commissioned sites that were later than it already is
      provider    sites still to come on the provider's record across its classes
      all         sites still to come on the register's record across every class and provider
      slip        every site still to come moved by the register's median days late
      planned     every site still to come commissioned on its planned date
      zone_ratio  the megawatts contracted, times the share of its contract the zone had in service in mid January
                  of past winters
      contract    the megawatts contracted"""
    reg = register_as_at(assets, as_at)
    now = in_service(reg, zone, as_at)
    pending = np.array([not _isdate(c) and not _isdate(l) for c, l in zip(reg["commissioned"], reg["lost"])], bool)
    mine = reg[(reg["zone"] == zone).values & pending]
    if method == "contract":
        return float(contracted), now, []
    if method == "zone_ratio":
        rs = [in_service(reg, zone, dt.date(int(w[:4]) + 1, 1, 15)) / mw for w, mw in (history or {}).items()
              if mw and dt.date(int(w[:4]) + 1, 1, 15) <= as_at]
        return float(contracted) * float(np.mean(rs)), now, []
    if method == "planned":
        add = float(sum(r.kw for r in mine.itertuples() if r.planned <= by)) / 1000.0
        return now + add, now, []
    done = reg[np.array([_isdate(c) for c in reg["commissioned"]], bool)]
    if method == "slip":
        med = float(np.median([(c - p).days for c, p in zip(done["commissioned"], done["planned"])]))
        add = float(sum(r.kw for r in mine.itertuples() if r.planned + dt.timedelta(days=med) <= by)) / 1000.0
        return now + add, now, []
    if method == "class_median":
        med = {cls: float(np.median([(c - p).days for c, p in zip(d["commissioned"], d["planned"])])) for cls, d in done.groupby("cls")}
        add = float(sum(r.kw for r in mine.itertuples() if r.planned + dt.timedelta(days=med.get(r.cls, 60.0)) <= by)) / 1000.0
        return now + add, now, []
    rows, add = [], 0.0
    if method in ("class_done", "class_done_cond"):
        late = {cls: np.sort(np.array([(c - p).days for c, p in zip(d["commissioned"], d["planned"])], float))
                for cls, d in done.groupby("cls")}
        for r in mine.itertuples():
            l = late.get(r.cls)
            el, hz = (as_at - r.planned).days, (by - r.planned).days
            if l is None or not len(l):
                pr = 0.0
            elif method == "class_done" or el <= 0:
                pr = float((l <= hz).mean())
            else:
                later = l[l > el]
                pr = float((later <= hz).mean()) if len(later) else 0.0
            add += r.kw * pr
            rows.append((r.site, r.cls, int(r.kw), r.planned, pr))
        return now + add / 1000.0, now, rows
    if method == "lognormal":
        ln = lognormal_by_class(reg, as_at)
        for r in mine.itertuples():
            c = ln[r.cls]
            F = lambda days: float(_norm_cdf((math.log(days) - c["mu"]) / c["sigma"])) if days > 0 else 0.0
            el, hz = (as_at - r.planned).days, (by - r.planned).days
            alive = (1 - c["lost"]) * (1 - F(el)) + c["lost"] * (1.0 if el <= 0 else max(1 - el / 260.0, 0.0))
            pr = (1 - c["lost"]) * max(F(hz) - F(el), 0.0) / alive if alive > 1e-9 else 0.0
            add += r.kw * pr
            rows.append((r.site, r.cls, int(r.kw), r.planned, pr))
        return now + add / 1000.0, now, rows
    provider = reg[reg["zone"] == zone]["provider"].iloc[0]
    if method == "provider":
        inc = incidence(reg[reg["provider"] == provider], as_at, group=())
        key = lambda r: ()
    elif method == "all":
        inc = incidence(reg, as_at, group=())
        key = lambda r: ()
    elif method == "class_provider":
        inc = incidence(reg, as_at, group=("cls", "provider"))
        key = lambda r: (r.cls, r.provider)
    else:
        inc = incidence(reg, as_at, group=("cls",), losses={"class": "competing", "nolost": "censor", "drop": "drop"}[method])
        key = lambda r: (r.cls,)
    fallback = None
    for r in mine.itertuples():
        c = inc.get(key(r))
        if c is None or c["n"] < 8:
            fallback = fallback or incidence(reg, as_at, group=("cls",))
            c = fallback[(r.cls,)]
        pr = _chance(c, r.planned, as_at, by)
        add += r.kw * pr
        rows.append((r.site, r.cls, int(r.kw), r.planned, pr))
    return now + add / 1000.0, now, rows


# ------------------------------------------------------------------------------------------------ R5 the events
def event_table(X, code, D, P, model, base="commissioned", exclude_switch=True):
    """One row per completed event at a zone: megawatts scheduled, megawatts delivered in the credited half-hours
    (what the day would have been with no service, less what was metered), the reduction through the window and what
    came back after it, with the megawatts the provider had in service that day."""
    ev = X["events"]
    mine = ev[(ev["zone"] == code) & (ev["status"] == "Completed") & (ev["scheduled_mw"] > 0)]
    rows = []
    zone_contract = X["previous"].get(X["names"][code], {})
    reg = X["assets"][X["assets"]["zone"] == code]
    for e in mine.itertuples():
        d = e.date
        if d not in D.index or pd.isna(D.loc[d, "M"]) or (exclude_switch and D.loc[d, "switch"]):
            continue
        obs = P.loc[d].values
        if np.isnan(obs[IW + IP]).any():
            continue
        cf = counterfactual(model, D, d)
        red = cf - obs
        delivered = float(np.mean(red[IC]))
        rows.append(dict(date=d, winter=D.loc[d, "winter"], T=float(D.loc[d, "T"]), scheduled=float(e.scheduled_mw),
                         delivered=delivered, provider=e.provider, window=red[IW], post=-red[IP],
                         commissioned=in_service(reg, code, d),
                         contract=float(zone_contract.get(D.loc[d, "winter"], np.nan))))
    t = pd.DataFrame(rows)
    if len(t):
        t["base"] = t["commissioned"] if base == "commissioned" else t["contract"]
    return t


def _norm_cdf(z):
    return 0.5 * (1.0 + np.vectorize(math.erf)(np.asarray(z, float) / math.sqrt(2.0)))


def _basis(T, form):
    T = np.asarray(T, float)
    if form == "linear":
        return np.column_stack([np.ones(len(T)), T])
    if form == "quadratic":
        return np.column_stack([np.ones(len(T)), T, T * T])
    if form == "hinge":            # flat above a knee at +2.0 C, a slope below it
        return np.column_stack([np.ones(len(T)), np.minimum(T - 2.0, 0.0)])
    raise ValueError(form)


def floor_mw(ev, tol_mw=0.2, tol_share=0.07):
    """The megawatts an event that met its schedule shows were available at least: the schedule less the margin by
    which a met schedule can read short (the provider's tracking of an instruction and the measurement's noise)."""
    return (ev["scheduled"] - np.maximum(tol_mw, tol_share * ev["scheduled"])).values


def met(ev, tol_mw=0.2, tol_share=0.07):
    """An event on which the provider delivered what was scheduled (within that margin): its megawatts show only
    that at least the floor was available."""
    return ev["delivered"].values >= floor_mw(ev, tol_mw, tol_share)


def availability_fit(ev, form="linear", censor=True, iters=500):
    """The available share of the base megawatts (in service, or contracted) against the day's temperature, on the
    log scale. Events that fell short of the schedule show the share itself; events that met it show only a floor. A
    normal censored regression, fitted by expectation steps on the mean's coefficients and the spread."""
    y = np.log(np.maximum(ev["delivered"].values.astype(float), 0.05) / ev["base"].values.astype(float))
    u = np.log(floor_mw(ev) / ev["base"].values.astype(float))
    c = met(ev)
    B = _basis(ev["T"].values, form)
    obs = ~c
    beta, *_ = np.linalg.lstsq(B[obs], y[obs], rcond=None)
    s = float(np.std(y[obs] - B[obs] @ beta)) or 0.05
    if censor:
        for _ in range(iters):
            mu = B @ beta
            z = (u - mu) / s
            lam = np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi) / np.maximum(1.0 - _norm_cdf(z), 1e-12)
            ey = np.where(c, mu + s * lam, y)
            ey2 = np.where(c, mu * mu + s * s + s * (u + mu) * lam, y * y)
            nb, *_ = np.linalg.lstsq(B, ey, rcond=None)
            m2 = B @ nb
            ns = math.sqrt(max(float(np.mean(ey2 - 2 * ey * m2 + m2 * m2)), 1e-8))
            done = np.max(np.abs(nb - beta)) < 1e-9 and abs(ns - s) < 1e-9
            beta, s = nb, ns
            if done:
                break
    return dict(beta=beta, sigma=s, form=form, n_short=int(obs.sum()), n_met=int(c.sum()))


def share_at(fit, T=T_DESIGN):
    """The expected available share at a temperature."""
    return float(math.exp((_basis([T], fit["form"]) @ fit["beta"])[0] + 0.5 * fit["sigma"] ** 2))


def shapes(ev, noise):
    """The window's shape (each half-hour's reduction over the megawatts delivered), what comes back in each of the
    four half-hours after it per megawatt delivered, and how much each of those varies from evening to evening (net
    of the measurement's own noise, as a share of the half-hour's come-back)."""
    e = ev[ev["delivered"] > 0.5]
    dl = e["delivered"].values
    W = np.vstack(e["window"].values)
    Pb = np.vstack(e["post"].values)
    ramp = (W * dl[:, None]).sum(axis=0) / (dl * dl).sum()
    reb = (Pb * dl[:, None]).sum(axis=0) / (dl * dl).sum()
    res = Pb - dl[:, None] * reb[None, :]
    var = np.maximum((res ** 2).mean(axis=0) - np.asarray(noise) ** 2, 0.0)
    rel = np.sqrt(var / np.maximum((dl * dl).mean(), 1e-9)) / np.maximum(reb, 1e-6)
    return ramp, reb, np.minimum(rel, 0.6), len(e)


# ------------------------------------------------------------------------------------------------ R6 to R9 the day
def replay(profile, delivered, ramp, reb):
    p = np.array(profile, float).copy()
    p[IW] -= delivered * np.asarray(ramp)
    p[IP] += delivered * np.asarray(reb)
    return p


IO = [i for i in range(48) if i not in IW and i not in IP]
DRAWS = 120000        # guideline 7: at least 100,000 design days


class DesignDays:
    """The design days of guideline 7 for one primary, drawn once: the day's demand above or below its usual level by
    the same proportion in every half-hour, the share of its sites' megawatts the provider has available that evening
    (independently of the demand), and the load that comes back after the window, each varying as the record shows it.
    Every question about the day (the contract in full, a further contract, a shorter schedule, a customer added) is
    answered on the same days."""

    def __init__(self, profile, sd_day, cv, ramp, reb, reb_rel=None, n=DRAWS, seed=20261110):
        rng = np.random.default_rng(seed)
        self.r = rng.normal(0, sd_day, n)
        self.a = np.exp(cv * rng.normal(0, 1, n) - 0.5 * cv * cv)
        self.rb = 1.0 + (np.asarray(reb_rel if reb_rel is not None else np.zeros(4))[None, :] * rng.normal(0, 1, (n, 4)))
        self.profile = np.asarray(profile, float)
        self.ramp, self.reb = np.asarray(ramp, float), np.asarray(reb, float)
        self.rescale(1.0)

    def rescale(self, scale):
        """Every half-hour of the day grown in one proportion (a customer added, guideline 4)."""
        B = (self.profile * scale)[None, :] * (1 + self.r[:, None])
        self.bo, self.bw, self.bp = B[:, IO].max(axis=1), B[:, IW], B[:, IP]
        return self

    def peaks(self, delivered, cap=None, sched=None, fixed=None):
        d = delivered * self.a
        if cap is not None:
            d = np.minimum(d, cap)
        if sched is not None:      # scheduled short of what is available: the provider delivers the schedule
            d = np.minimum(d, sched)
        w = (self.bw - d[:, None] * self.ramp[None, :]).max(axis=1)
        if fixed is None:
            p = (self.bp + d[:, None] * self.reb[None, :] * self.rb).max(axis=1)
        else:                      # the hurried reading: the come-back as the megawatts the record's events show
            p = (self.bp + np.asarray(fixed, float)[None, :]).max(axis=1)
        return np.maximum(np.maximum(self.bo, w), p)

    def stats(self, delivered, firm=None, **kw):
        pk = self.peaks(delivered, **kw)
        return float(pk.mean()), float(np.quantile(pk, ASSURANCE)), (float((pk > firm).mean()) if firm is not None else None)


def predictive(profile, delivered, cv, ramp, reb, sd_day, reb_rel=None, cap=None, firm=None, n=DRAWS, seed=20261110):
    """Design days drawn from the day-to-day spread of demand, of what the provider has available and of what comes
    back: each day's highest half-hour with the service delivered through its window; the mean, the level the
    highest half-hour stays under on nine days in ten, and the share of days it is over firm capacity."""
    return DesignDays(profile, sd_day, cv, ramp, reb, reb_rel, n=n, seed=seed).stats(delivered, firm=firm, cap=cap)


# ------------------------------------------------------------------------------------------------ R12 to R14 the choices
def step_per_mw(X, code, method="class"):
    """Megawatts in service on the assessment date for each megawatt of the zone's 2027/28 step, the terms a further
    megawatt would be signed on: the register's sites signed for that winter at the zone, each on its chance of being in
    service by then (the golden), or the hurried readings of the same."""
    name = X["names"][code]
    hist = X["previous"].get(name, {})
    contracted = X["contracts_code"][code]
    step_mw = contracted - float(hist.get("2026/27", 0.0))
    if method in ("every", "contract"):   # every further megawatt contracted taken as a megawatt in service
        return 1.0
    if method == "zone_ratio":            # the whole contract's megawatts in service over its megawatts contracted
        comm, _, _ = expected_commissioned(X["assets"], code, X["register_date"], ASSESS, method="class")
        return comm / contracted
    reg = register_as_at(X["assets"], X["register_date"])
    step = reg[(reg["zone"] == code) & (reg["winter"] == "2027/28")]
    if method in ("planned", "slip", "class_median"):
        done = reg[np.array([_isdate(c) for c in reg["commissioned"]], bool)]
        if method == "planned":
            lag = {c: 0.0 for c in CLASSES_SEEN(reg)}
        elif method == "slip":
            med = float(np.median([(c - p).days for c, p in zip(done["commissioned"], done["planned"])]))
            lag = {c: med for c in CLASSES_SEEN(reg)}
        else:
            lag = {cls: float(np.median([(c - p).days for c, p in zip(d["commissioned"], d["planned"])]))
                   for cls, d in done.groupby("cls")}
        kw_in = float(sum(r.kw for r in step.itertuples() if r.planned + dt.timedelta(days=lag.get(r.cls, 60.0)) <= ASSESS))
        return kw_in / 1000.0 / step_mw
    _, _, rows = expected_commissioned(X["assets"], code, X["register_date"], ASSESS, method=method,
                                       contracted=contracted, history=hist)
    pr = {r[0]: r[4] for r in rows}
    kw_in = float(sum(r.kw * pr.get(r.site, 0.0) for r in step.itertuples()))
    return kw_in / 1000.0 / step_mw


def CLASSES_SEEN(reg):
    return sorted(set(reg["cls"]))


def further_mw(days, z, per_mw, top=40.0, fixed=None):
    """The further megawatts a primary would have to contract on its 2027/28 award's terms for its peak to exceed firm
    capacity on no more than one design day in ten: (megawatts, None) when an amount up to `top` does it, (None, (the
    lowest share any amount reaches, where)) when none does."""
    def share(x):
        comm, cap = z["commissioned"] + x * per_mw, z["contracted"] + x
        return days.stats(min(z["share"] * comm, cap), firm=z["firm"], cap=cap, fixed=fixed)[2]
    if share(0.0) <= 1.0 - ASSURANCE:
        return 0.0, None
    coarse = [(x, share(x)) for x in np.arange(1.0, top + 1e-9, 1.0)]
    hit = next((x for x, s in coarse if s <= 1.0 - ASSURANCE), None)
    if hit is not None:
        for x in np.arange(hit - 0.9, hit + 1e-9, 0.1):
            if share(x) <= 1.0 - ASSURANCE:
                return round(float(x), 1), None
        return float(hit), None
    x0 = min(coarse, key=lambda t: t[1])[0]
    fine = [(x, share(x)) for x in np.arange(max(x0 - 1.0, 0.0), x0 + 1.0 + 1e-9, 0.1)]
    xb, sb = min(fine, key=lambda t: (t[1], t[0]))
    return None, (sb, round(float(xb), 1))


def linear_further(z, per_mw):
    """The hurried reading of the same: the nine-days-in-ten level's excess over firm capacity divided by what a
    further megawatt delivers."""
    if z["p90"] <= z["firm"]:
        return 0.0
    return round(float((z["p90"] - z["firm"]) / max(z["share"] * per_mw, 1e-9)), 1)


def best_schedule(days, z, fixed=None):
    """The megawatts to schedule for the whole window, at most the contract, that make the share of design days over
    firm capacity smallest (the lower nine-days-in-ten level breaking a tie, then the larger schedule): the schedule,
    its mean peak, nine-days-in-ten level and share."""
    def at(s):
        m, p90, ex = days.stats(z["delivered"], firm=z["firm"], cap=z["contracted"], sched=s, fixed=fixed)
        return (ex, round(p90, 9), -s, m)
    coarse = [(s,) + at(s) for s in list(np.arange(0.0, z["contracted"], 0.5)) + [z["contracted"]]]
    s0 = min(coarse, key=lambda t: t[1:4])[0]
    fine = [(s,) + at(s) for s in np.arange(max(s0 - 0.5, 0.0), min(s0 + 0.5, z["contracted"]) + 1e-9, 0.1)]
    s, ex, p90, _, m = min(coarse + fine, key=lambda t: t[1:4])
    return dict(schedule=round(float(s), 1), mean=m, p90=p90, exceed=ex, full=bool(s >= z["contracted"] - 1e-9))


CUSTOMER = dict(type="Data hall", kva=4000, energised=dt.date(2027, 8, 2))    # the prompt's customer at Hartwell Common


def customer_adds(fits, M=None, how="type", c=CUSTOMER):
    """Megawatts a customer energised before the assessment date adds to its primary's evening peak by then: on its
    type's level and build-up (the golden), or the hurried readings of the same."""
    f = fits.get(c["type"], fits["_pooled"])
    age = months_between(c["energised"], ASSESS)
    if how == "pooled":
        f = fits["_pooled"]
        return c["kva"] * f["U"] * float(_g(age, f["tau"], f["k"])) / 1000.0
    if how == "mature":
        return c["kva"] * f["U"] / 1000.0
    if how == "full":
        return c["kva"] * 0.95 / 1000.0
    if how == "ratio":
        last = M.sort_values("month").groupby("conn").tail(1)
        return c["kva"] * float(last["ratio"].mean()) / 1000.0
    return c["kva"] * f["U"] * float(_g(age, f["tau"], f["k"])) / 1000.0


# ------------------------------------------------------------------------------------------------ the whole analysis
DEFAULT = dict(baseline="anchored", anchor="ratio", mform="spline", morning="full", winters=None, trend=False,
               conn="own", conn_shape="weibull", conn_by_type=True, conn_months=3,
               comm="class", avail_form="linear", avail_base="commissioned", censor=True,
               replay=True, tail=True, comeback="scaled", further=None, customer=None, scan=True)
SCHEDULE_AT = ("Ashcombe Road",)      # the primary whose schedule the review asks about
CUSTOMER_AT = "Hartwell Common"       # the primary the prompt's customer would connect to
# how each reading of the register's customers carries a customer not yet connected
CUSTOMER_HOW = {"own": "type", "type": "type", "new_buildup": "type", "pooled": "pooled", "mature": "mature",
                "observed": "mature", "full": "full", "ratio": "ratio"}
# how each reading of the sites still to come carries a further megawatt on the award's terms
FURTHER_HOW = {"contract": "contract", "zone_ratio": "zone_ratio"}


def analyse(X, **opt):
    """Every result for the zone primaries under one set of choices (DEFAULT is the golden's)."""
    o = dict(DEFAULT, **opt)
    if "prep" not in X:
        X["prep"] = prepare(X["demand"])
        X["tmean"] = daily_mean(X["weather"])
    codes = sorted(X["contracts_code"])
    morning = MORNING if o["morning"] == "full" else MORNING_LATE
    out = {"options": o, "zones": {}}
    C, M = conn_frame(X)
    fits = buildup_fit(M, by_type=o["conn_by_type"], shape=o["conn_shape"])
    out["buildup"] = fits
    frames, models, lines, evs = {}, {}, {}, []
    for code in codes:
        key = (code, o["morning"])
        cache = X.setdefault("_frames", {})
        if key not in cache:
            cache[key] = day_frame(X, code, morning)
        D, P = cache[key]
        frames[code] = (D, P)
        models[code] = anchored(D, P, form=o["mform"], winters=o["winters"], trend=o["trend"], anchor=o["anchor"])
        if o["baseline"] != "anchored":
            lines[code] = line_profile(D, P, mode=o["baseline"])
        ev = event_table(X, code, D, P, models[code], base=o["avail_base"])
        ev["code"] = code
        evs.append(ev)
    EV = pd.concat(evs, ignore_index=True)
    out["events"] = EV
    # the come-back as the megawatts each zone's events showed after the window, whatever they delivered (the hurried
    # reading); the golden carries it per megawatt delivered
    back_mw = {}
    for code in codes:
        e = EV[(EV["code"] == code) & (EV["delivered"] > 0.5)]
        back_mw[code] = np.vstack(e["post"].values).mean(axis=0) if len(e) else np.zeros(4)
    prov_of = {code: X["provider_of"][code] for code in codes}
    share, cvs, ramps, rebs, rebrel = {}, {}, {}, {}, {}
    for prov in sorted(set(prov_of.values())):
        pcodes = [c for c in codes if prov_of[c] == prov]
        e = EV[EV["code"].isin(pcodes)]
        fit = availability_fit(e, form=o["avail_form"], censor=o["censor"])
        noise = np.mean([models[c]["efit"]["sd"][IP] for c in pcodes], axis=0)
        share[prov] = share_at(fit)
        cvs[prov] = float(math.sqrt(max(math.exp(fit["sigma"] ** 2) - 1.0, 0.0)))
        ramps[prov], rebs[prov], rebrel[prov], _ = shapes(e, noise)
        out.setdefault("fits", {})[prov] = dict(fit=fit, share=share[prov], cv=cvs[prov], ramp=ramps[prov], reb=rebs[prov],
                                                reb_rel=rebrel[prov], n=len(e), n_short=fit["n_short"], n_met=fit["n_met"])
    for code in codes:
        D, P = frames[code]
        mdl = models[code]
        if o["baseline"] == "anchored":
            prof26, sd_day = mdl["profile"], mdl["rel_sd"]
        else:
            prof26, sd_day = lines[code]["profile"], lines[code]["rel_sd"]
        before26 = float(np.nanmax(prof26))
        r1, r2 = X["rates"][code]
        g = (1 + r1 / 100.0) * (1 + r2 / 100.0)
        add, rows = connections_add(X, code, method=o["conn"], fits=fits, C=C, M=M, months=o["conn_months"])
        before28 = before26 * g + add
        prof28 = prof26 * (before28 / before26)
        contracted = X["contracts_code"][code]
        comm, now, sites = expected_commissioned(X["assets"], code, X["register_date"], ASSESS, method=o["comm"],
                                                 contracted=contracted, history=X["previous"].get(X["names"][code]))
        prov = prov_of[code]
        delivered = min(share[prov] * comm, contracted)
        fixed = back_mw[code] if o["comeback"] == "fixed" else None
        if o["replay"]:
            with_ = replay(prof28, delivered, ramps[prov], rebs[prov] if fixed is None else np.zeros(4))
            if fixed is not None:
                with_[IP] += fixed
            peak = float(with_.max())
            peak_hh = H48[int(with_.argmax())]
        else:
            with_ = prof28 - 0.0
            peak = before28 - delivered
            peak_hh = H48[int(prof28.argmax())]
        firm = X["firm"][code]
        days = None
        if o["tail"] and o["replay"]:
            days = DesignDays(prof28, sd_day, cvs[prov], ramps[prov], rebs[prov], rebrel[prov])
            mean_pk, p90, exceed = days.stats(delivered, firm=firm, cap=contracted, fixed=fixed)
        elif o["tail"]:
            sd = math.hypot(sd_day * before28, cvs[prov] * delivered)
            mean_pk, p90 = peak, peak + 1.2815515655446004 * sd
            exceed = float(1.0 - _norm_cdf((firm - peak) / max(sd, 1e-9)))
        else:
            mean_pk, p90, exceed = peak, peak, (1.0 if peak > firm else 0.0)
        out["zones"][code] = dict(name=X["names"][code], provider=prov, firm=firm, before26=before26, growth=g, conn_add=add,
                                  conn_rows=rows, before28=before28, contracted=contracted, commissioned_now=now,
                                  commissioned=comm, sites=sites, share=share[prov], delivered=delivered,
                                  off_peak=before28 - peak, peak=peak, peak_hh=peak_hh, mean_peak=mean_pk, p90=p90,
                                  exceed=exceed,
                                  commit=bool(p90 > firm), margin=p90 - firm, profile26=prof26, profile28=prof28,
                                  with_service=with_, sd_day=sd_day, cv=cvs[prov],
                                  clean_days=mdl["efit"]["n_latest"], coldest_clean=mdl["efit"]["coldest_latest"],
                                  clean_all=mdl["efit"]["n"], coldest_all=mdl["efit"]["coldest"],
                                  morning_days=mdl["mfit"]["n"], morning_cold=int((mdl["mfit"]["T"] <= 0.0).sum()),
                                  knee=mdl["mfit"].get("knee"), reb_total=float(np.sum(rebs[prov])),
                                  back_mw=[float(v) for v in back_mw[code]])
        z = out["zones"][code]
        if not o["scan"]:
            continue
        # R12: what a further contract on the 2027/28 award's terms would do
        how = o["further"] or FURTHER_HOW.get(o["comm"], o["comm"])
        per = step_per_mw(X, code, method="class" if how == "linear" else how)
        z["further_per_mw"] = per
        if days is None or how == "linear":
            z["further"], z["further_low"] = linear_further(z, per), None
        else:
            z["further"], z["further_low"] = further_mw(days, z, per, fixed=fixed)
        # R13: the schedule that makes the share of design days over firm capacity smallest
        if X["names"][code] in SCHEDULE_AT:
            if days is None:
                z["schedule"] = dict(schedule=float(contracted), mean=mean_pk, p90=p90, exceed=exceed, full=True)
            else:
                z["schedule"] = best_schedule(days, z, fixed=fixed)
        # R14: the prompt's customer added to the primary it would connect to
        if X["names"][code] == CUSTOMER_AT:
            adds = customer_adds(fits, M, how=o["customer"] or CUSTOMER_HOW.get(o["conn"], "type"))
            scale = (before28 + adds) / before28
            if days is None:
                cm, cp, ce = mean_pk + adds, p90 + adds, (1.0 if p90 + adds > firm else 0.0)
            else:
                cdays = DesignDays(prof28, sd_day, cvs[prov], ramps[prov], rebs[prov], rebrel[prov]).rescale(scale)
                cm, cp, ce = cdays.stats(delivered, firm=firm, cap=contracted, fixed=fixed)
            z["customer"] = dict(adds=adds, mean=cm, p90=cp, exceed=ce, holds=bool(cp <= firm))
    out["commit"] = [X["names"][c] for c in codes if out["zones"][c]["commit"]]
    return out


def from_world(W, T=None, season_only=True):
    """The analyst's inputs straight from the clean truth (the pack's parser builds the same from the files). The
    pack's SCADA export runs November to March, so October is dropped here too."""
    T = T or W.build()
    X = W.tables(T)
    if season_only:
        d = X["demand"]
        loc = pd.DatetimeIndex(d["t_utc"]).tz_convert("Europe/London") - pd.Timedelta(minutes=30)
        X["demand"] = d[loc.month != 10].reset_index(drop=True)
    X["names"] = {p["code"]: p["name"] for p in W.PRIMARIES}
    X["rates"] = {p["code"]: (p["dfes"], p["dfes"]) for p in W.PRIMARIES}
    X["firm"] = {p["code"]: p["firm"] for p in W.PRIMARIES}
    X["contracts_code"] = {W.BY[z["key"]]["code"]: z["mw"]["2027/28"] for z in W.ZONES}
    X["provider_of"] = {W.BY[z["key"]]["code"]: z["provider"] for z in W.ZONES}
    X["previous"] = {W.BY[z["key"]]["name"]: {w: z["mw"][w] for w in W.CONTRACT_WINTERS} for z in W.ZONES}
    X["register_date"] = W.REGISTER_DATE
    return X
