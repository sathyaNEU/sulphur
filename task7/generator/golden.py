"""task7 architecture 9: the golden analysis and its rivals, on a season-by-building table of normalised gas use read
from the pack (verify.py), with each building's owner, its service visits, its 2025 week of electricity and its roof per
square metre of floor. The same code runs on the generator's clean truth and on the cleaned pack, so a figure in the
golden is the figure the pack yields.

The pilot's places were drawn by lot among the owners who answered the May 2019 offer, within each measure, an owner's
buildings together, so for each measure and each season since the works the drawn buildings that had them are set
against the owners the draw passed over, both against their own 2018/19 season. What a measure saves depends on the
building (roof insulation on its roof per floor and none of its hot water, controls on the share of the week it stands
empty, nothing where it is lived in round the clock) and on its owner, whose facility manager runs every one of its
buildings the same way. Heating optimisation's saving falls as the heating curve creeps back up; from September 2022 the
state campaign's heating checks set the curve back down in every building that took one, and a balanced system holds
what the check gives it, so the pilot's works buildings saved more after their check than their works alone would have
kept. The campaign closed in March 2026, so the 2026 works will keep only what their own balancing holds: the golden
reads heating optimisation's saving off each works building's seasons before its campaign check (and the owners who
declined it), against the passed-over owners outside the season of their own check. Every 2026 application is priced on
its own building, each measure's grant per lifetime tonne carries the 90 per cent range a fresh draw of the pilot's
owners would give, every step repeated, and the committee funds a measure only where that range's upper end is within
the limit."""
import datetime as dt
import math

import numpy as np

MEASURES = ["insulation", "heating optimisation", "heating controls"]
TYPES = ["office", "retail", "hotel", "workshop", "care home", "restaurant"]
ROUND_CLOCK = ("hotel", "care home")      # heated round the clock, for the class-level rival
LIFE = {"insulation": 30, "heating optimisation": 15, "heating controls": 10}
EF = 0.201                 # tonnes of CO2 per MWh of gas, the climate action plan's factor
LIMIT = 120.0              # euro of grant per lifetime tonne of CO2
PILOT = 2019
PIPELINE = 2026
NOTICE = {PILOT: dt.date(2019, 5, 20), PIPELINE: dt.date(2026, 5, 20)}   # the notices that carried each offer
CLOSE = {PILOT: dt.date(2019, 6, 30), PIPELINE: dt.date(2026, 6, 30)}    # the day each offer closed
RECEIVED_TO = dt.date(2026, 6, 12)                                          # the applications passed to the utility
CUT_DAY = (RECEIVED_TO - NOTICE[PIPELINE]).days                              # 23 days after the notice


class Panel:
    """seasons, si; U: buildings x seasons normalised use in kWh (nan where not connected); typ: the use on the
    building's 2019 notice (the register's use where it had none); owner: the owner number on the register; answered,
    drawn, works, withdrawn, measure: the 2019 pilot; answers19: the pilot's responses (b, measure, date, cost, grant,
    drawn, withdrawn, works, owner); visits: the days of the service team's reads at a check, building by building;
    pipe: the 2026 applications received by 12 June, a revised application replacing the earlier one (no, b, measure,
    grant, ref_kwh, date, typ)."""
    pass


# ---------------------------------------------------------------- the lottery, season by season

def _arms(P, m, typ=None, cls=None):
    sel = P.measure == m
    if typ is not None:
        sel = sel & (P.typ == TYPES.index(typ))
    if cls is not None:
        rc = np.isin(P.typ, [TYPES.index(t) for t in ROUND_CLOCK])
        sel = sel & (rc if cls == "round the clock" else ~rc)
    return np.where(P.works & sel)[0], np.where(P.answered & ~P.drawn & sel)[0]


def log_changes(P, idx, base="notice"):
    """each building's log change from its baseline in every season after the pilot (rows: idx; nan where missing)"""
    k0 = P.si[PILOT]
    ks = list(range(k0 + 1, len(P.seasons)))
    if base == "notice":
        b = np.log(P.U[idx, k0])
    else:                                   # the two seasons to 2018/19
        b = np.log(P.U[idx, k0 - 1:k0 + 1]).mean(1)
    out = np.log(P.U[np.ix_(idx, ks)]) - b[:, None]
    return out


def season_savings(P, m, how="ratio_of_totals", base="notice", typ=None, cls=None, rows=None):
    """the measure's saving in each season 2019/20 to 2025/26 (seven shares): works buildings against the passed-over
    owners of the same measure"""
    g, c = _arms(P, m, typ, cls)
    if rows is not None:
        g, c = rows
    k0 = P.si[PILOT]
    out = []
    for j, k in enumerate(range(k0 + 1, len(P.seasons))):
        lo = k0 if base == "notice" else k0 - 1
        need = list(range(lo, k0 + 1)) + [k]
        gg = g[np.all(np.isfinite(P.U[np.ix_(g, need)]), 1)]
        cc = c[np.all(np.isfinite(P.U[np.ix_(c, need)]), 1)]
        if base == "notice":
            bg, bc = P.U[gg, k0], P.U[cc, k0]
        else:
            bg = np.exp(np.log(P.U[gg, lo:k0 + 1]).mean(1))
            bc = np.exp(np.log(P.U[cc, lo:k0 + 1]).mean(1))
        if how == "mean_log":
            d = np.log(P.U[gg, k] / bg).mean() - np.log(P.U[cc, k] / bc).mean()
            out.append(1.0 - math.exp(d))
        elif how == "ratio_of_totals":
            out.append(1.0 - (P.U[gg, k].sum() / bg.sum()) / (P.U[cc, k].sum() / bc.sum()))
        elif how == "mean_ratio":
            out.append(1.0 - (P.U[gg, k] / bg).mean() / (P.U[cc, k] / bc).mean())
        elif how == "median":
            out.append(1.0 - float(np.median(P.U[gg, k] / bg)) / float(np.median(P.U[cc, k] / bc)))
    return np.array(out)


def before_after(P, m):
    """the works buildings' own change against their 2018/19 season, no comparison (the quick pass)"""
    g, _ = _arms(P, m)
    k0 = P.si[PILOT]
    out = []
    for k in range(k0 + 1, len(P.seasons)):
        gg = g[np.isfinite(P.U[g, k0]) & np.isfinite(P.U[g, k])]
        out.append(1.0 - math.exp(np.log(P.U[gg, k] / P.U[gg, k0]).mean()))
    return np.array(out)


# ---------------------------------------------------------------- persistence over the service life

def _fit_floor(s):
    """least squares on s(a) = f + d exp(-(a-1)/tau), tau on a fine grid, (f, d) linear: (f, d, tau)"""
    a = np.arange(1, len(s) + 1, dtype=float)
    best = None
    for tau in np.arange(0.20, 8.0001, 0.01):
        X = np.column_stack([np.ones_like(a), np.exp(-(a - 1.0) / tau)])
        coef, res, *_ = np.linalg.lstsq(X, s, rcond=None)
        sse = float(((X @ coef - s) ** 2).sum())
        if best is None or sse < best[0] - 1e-15:
            best = (sse, float(coef[0]), float(coef[1]), float(tau))
    return best[1], best[2], best[3], best[0]


def _fit_zero(s):
    a = np.arange(1, len(s) + 1, dtype=float)
    best = None
    for tau in np.arange(0.20, 60.0001, 0.02):
        x = np.exp(-(a - 1.0) / tau)
        s1 = float((x * s).sum() / (x * x).sum())
        sse = float(((s1 * x - s) ** 2).sum())
        if best is None or sse < best[0] - 1e-15:
            best = (sse, s1, float(tau))
    return best[1], best[2], best[0]


def profile(s, L, how="floor"):
    """the measure's saving at each age 1 to L of the works, from its seven observed seasons"""
    s = np.asarray(s, float)
    n = len(s)
    ages = np.arange(1, L + 1, dtype=float)
    if how == "floor":                       # the golden: a fitted approach to the level it settles at
        f, d, tau, _ = _fit_floor(s)
        return f + d * np.exp(-(ages - 1.0) / tau)
    if how == "floor_observed":              # the seasons as observed, the fitted level after them
        f, d, tau, _ = _fit_floor(s)
        out = f + d * np.exp(-(ages - 1.0) / tau)
        out[:min(n, L)] = s[:min(n, L)]
        return out
    if how == "last":                        # the seasons as observed, the last carried
        return np.concatenate([s[:min(n, L)], np.full(max(0, L - n), s[-1])])
    if how == "last3":
        return np.concatenate([s[:min(n, L)], np.full(max(0, L - n), s[-3:].mean())])
    if how == "flat":                        # the seven-season average carried flat
        return np.full(L, s.mean())
    if how == "first":                       # the first season's saving carried
        return np.full(L, s[0])
    if how == "zero":                        # an exponential fall to nothing
        s1, tau, _ = _fit_zero(s)
        return s1 * np.exp(-(ages - 1.0) / tau)
    if how == "linear":                      # a straight line through the seasons, floored at nothing
        a = np.arange(1, n + 1, dtype=float)
        b1, b0 = np.polyfit(a, s, 1)
        return np.clip(b0 + b1 * ages, 0.0, None)
    raise ValueError(how)


def lifetime(s, m, how="floor"):
    return float(profile(s, LIFE[m], how).mean())


# ---------------------------------------------------------------- by building type, carried to the applications

def type_levels(P, m, how="ratio_of_totals", base="notice", min_n=3):
    """each type's saving, averaged over the seven seasons, from the type's own works and passed-over buildings"""
    out = {}
    for t in TYPES:
        g, c = _arms(P, m, typ=t)
        if len(g) >= min_n and len(c) >= min_n:
            out[t] = float(season_savings(P, m, how, base, typ=t).mean())
    return out


def class_levels(P, m, how="ratio_of_totals"):
    return {cl: float(season_savings(P, m, how, cls=cl).mean()) for cl in ("intermittent", "round the clock")}


# ---------------------------------------------------------------- what suits the building

DOSE_BINS = 6
DRIVEN = ("insulation", "heating controls")


def driver(P, m, empty=None):
    """the building property a measure's saving follows: the share of the week a building stands empty (controls), the
    logarithm of its roof area per square metre of heated floor (insulation)"""
    if m == "heating controls":
        return P.empty if empty is None else empty
    if m == "insulation":
        return np.log(P.roof_ratio)
    return None


def dose_groups(P, m, nb=DOSE_BINS, rows=None, x=None):
    """the measure's answers in nb bands of its driver, cut at the quantiles of the works and passed-over buildings
    together (controls: the buildings lived in round the clock a band of their own at no empty hours): a list of (works,
    passed-over) index arrays"""
    x = driver(P, m) if x is None else x
    g, c = _arms(P, m) if rows is None else rows
    g, c = g[np.isfinite(x[g])], c[np.isfinite(x[c])]
    groups = []
    if m == "heating controls":
        lg, lc = g[x[g] <= 0.0], c[x[c] <= 0.0]
        if len(lg) >= 3 and len(lc) >= 3:
            groups.append((lg, lc))
        g, c = g[x[g] > 0.0], c[x[c] > 0.0]
    qs = np.quantile(np.concatenate([x[g], x[c]]), np.linspace(0, 1, nb + 1))
    qs[0], qs[-1] = -np.inf, np.inf
    for b in range(nb):
        gb = g[(x[g] >= qs[b]) & (x[g] < qs[b + 1])]
        cb = c[(x[c] >= qs[b]) & (x[c] < qs[b + 1])]
        if len(gb) >= 3 and len(cb) >= 3:
            groups.append((gb, cb))
    return groups


def dose_points(P, m, nb=DOSE_BINS, rows=None, x=None, heat_part=True):
    """each band's seven-season saving, works against passed-over, as the plan sets a saving; insulation's taken on the
    heating part (the band's works buildings' gas-weighted hot-water share, the benchmarking method's by use). Returns
    (driver, saving, the band's 2018/19 gas) per band"""
    x = driver(P, m) if x is None else x
    k0 = P.si[PILOT]
    pts = []
    for gb, cb in dose_groups(P, m, nb, rows, x):
        wts = np.nan_to_num(P.U[gb, k0])
        sv = float(season_savings(P, m, rows=(gb, cb)).mean())
        if m == "insulation" and heat_part:
            sv = sv / (1.0 - float(np.average(P.hvec[gb], weights=wts)))
        pts.append((float(np.average(x[gb], weights=wts)), sv, float(wts.sum())))
    return pts


def dose_fit(pts, m, form=None):
    """controls: nothing up to a threshold of the empty week, then a straight rise (the threshold on a grid, the rise by
    weighted least squares through the bands of buildings that close), the buildings lived in round the clock at their
    own band's saving; insulation: a straight line in the log of the roof per floor"""
    form = form or ("hinge" if m == "heating controls" else "line")
    lived = [p for p in pts if p[0] <= 0.0] if m == "heating controls" else []
    rest = [p for p in pts if p not in lived]
    out = {"form": form, "pts": pts, "lived": (lived[0][1] if lived and form != "linear_all" else None)}
    px, py, pw = (np.array(v) for v in zip(*(pts if form == "linear_all" else rest)))
    if form == "hinge":
        best = None
        for e0 in np.arange(0.20, 0.6001, 0.005):
            X = np.clip(px - e0, 0.0, None)
            if (X > 0).sum() < 2:
                continue
            b = float((pw * X * py).sum() / (pw * X * X).sum())
            sse = float((pw * (b * X - py) ** 2).sum())
            if best is None or sse < best[0] - 1e-15:
                best = (sse, float(e0), b)
        out.update(e0=best[1], slope=best[2])
    elif form in ("line", "linear", "linear_all"):
        b1, b0 = np.polyfit(px, py, 1, w=np.sqrt(pw))
        out.update(a=float(b0), b=float(b1))
    elif form == "bins":
        out["pts"] = sorted(rest)
    else:
        raise ValueError(form)
    return out


def dose_at(fit, x):
    x = np.atleast_1d(np.asarray(x, float))
    f = fit["form"]
    if f == "hinge":
        out = fit["slope"] * np.clip(x - fit["e0"], 0.0, None)
    elif f == "line":
        out = fit["a"] + fit["b"] * x
    elif f in ("linear", "linear_all"):
        out = np.clip(fit["a"] + fit["b"] * x, 0.0, None)
    else:
        pts = fit["pts"]
        cuts = [(pts[k][0] + pts[k + 1][0]) / 2.0 for k in range(len(pts) - 1)]
        out = np.array([pts[int(np.searchsorted(cuts, v))][1] for v in x])
    if fit.get("lived") is not None:
        out = np.where(x <= 0.0, fit["lived"], out)
    return out


def apps(P, m):
    return [a for a in P.pipe if a["measure"] == m]


# ---------------------------------------------------------------- the campaign's checks and what the works keep

CAMPAIGN_FROM = dt.date(2022, 9, 1)        # the state campaign's heating checks, September 2022 to March 2026
CAMPAIGN_TO = dt.date(2026, 3, 31)


def campaign_season(P):
    """the season of each building's campaign check (its first service read on or after 1 September 2022), 0 if none"""
    out = np.zeros(len(P.typ), int)
    for i, vs in enumerate(P.visits):
        cs = [d for d in vs if d >= CAMPAIGN_FROM]
        if cs:
            d = min(cs)
            out[i] = d.year + 1 if d.month >= 5 else d.year
    return out


def own_savings(P, m="heating optimisation", rows=None, how="ratio_of_totals", exclude_check_season=True,
                works_rule="before_check", with_sizes=False):
    """the measure's saving in each season 2019/20 to 2025/26 as its works alone keep it: each works building counted
    only in the seasons before its campaign check (all of them if it took none), each passed-over building in every
    season but the one of its own check (works_rule "declined": only the works buildings that took no campaign check)"""
    g, c = _arms(P, m) if rows is None else rows
    cs = P.check_season
    k0 = P.si[PILOT]
    out, sizes = [], []
    for k in range(k0 + 1, len(P.seasons)):
        s = P.seasons[k]
        if works_rule == "declined":
            gg = g[cs[g] == 0]
        else:
            gg = g[(cs[g] == 0) | (cs[g] > s)]
        cc = c[cs[c] != s] if exclude_check_season else c
        gg = gg[np.isfinite(P.U[gg, k0]) & np.isfinite(P.U[gg, k])]
        cc = cc[np.isfinite(P.U[cc, k0]) & np.isfinite(P.U[cc, k])]
        if how == "mean_log":
            out.append(1.0 - math.exp(np.log(P.U[gg, k] / P.U[gg, k0]).mean() - np.log(P.U[cc, k] / P.U[cc, k0]).mean()))
        else:
            out.append(1.0 - (P.U[gg, k].sum() / P.U[gg, k0].sum()) / (P.U[cc, k].sum() / P.U[cc, k0].sum()))
        sizes.append(float(P.U[gg, k0].sum()))
    if with_sizes:
        return np.array(out), np.array(sizes)
    return np.array(out)


def own_lifetime(s, sizes, m="heating optimisation", how="settled"):
    """the measure's saving over its life from the seasons its works alone keep: each observed season as it came, then
    the level it settles at (the last three seasons weighted by the 2018/19 gas of the works buildings each rests on)
    over the rest of the life; "floor": the fitted approach to a level instead"""
    L = LIFE[m]
    if how == "floor":
        return lifetime(s, m, "floor")
    level = float(np.average(s[-3:], weights=sizes[-3:]))
    if how == "settled_last2":
        level = float(np.average(s[-2:], weights=sizes[-2:]))
    return float((s[:min(len(s), L)].sum() + max(0, L - len(s)) * level) / L)


def heat_share(P, idx, wts=None):
    """the gas-weighted heating share (1 less the benchmarking method's hot-water share by use) of the buildings idx"""
    idx = np.asarray(idx, int)
    return float(np.average(1.0 - P.hvec[idx], weights=wts)) if len(idx) else float("nan")


def app_rates(P, m, route="golden", persist="floor", how="ratio_of_totals", base="notice", nb=DOSE_BINS, form=None,
              empty=None, heat_part=True, rows=None, s_given=None):
    """each 2026 application's saving over the measure's life, as a share of its reference consumption. Heating
    optimisation (golden): the saving its works alone keep, fitted over its life, carried from the pilot's works buildings'
    heating share to each application's; route "measured": the pilot's seasons as measured, the campaign's lift and all"""
    A = apps(P, m)
    if m == "heating optimisation":
        g, c = _arms(P, m) if rows is None else rows
        if route in ("golden", "pooled_own"):
            s, sz = own_savings(P, m, rows=(g, c), how=how, with_sizes=True)
            life = own_lifetime(s, sz, m, "settled" if persist == "floor" else persist)
        else:
            s = season_savings(P, m, how, base, rows=(g, c)) if s_given is None else s_given
            life = lifetime(s, m, "flat" if route == "flat" else persist)
        if route in ("golden", "measured", "flat"):
            k0 = P.si[PILOT]
            hp = heat_share(P, g, np.nan_to_num(P.U[g, k0]))
            return np.array([life * (1.0 - P.hvec[a["b"]]) / hp for a in A])
        return np.full(len(A), life)
    s = season_savings(P, m, how, base, rows=rows)
    life_factor = lifetime(s, m, persist) / s.mean()
    if route == "golden" and m in DRIVEN:   # its own building's saving along the measure's driver, faded
        x = driver(P, m, empty)
        fit = dose_fit(dose_points(P, m, nb, rows=rows, x=x, heat_part=heat_part), m, form)
        r = dose_at(fit, np.array([x[a["b"]] for a in A]))
        if m == "insulation" and heat_part:
            r = r * np.array([1.0 - P.hvec[a["b"]] for a in A])
        return r * life_factor
    if route in ("golden", "use"):          # its own use's saving, faded as the measure's saving fades
        lv = type_levels(P, m, how, base)
        pooled = float(s.mean())
        return np.array([lv.get(TYPES[a["typ"]], pooled) * life_factor for a in A])
    if route == "pooled":                   # the pilot's own mix, faded
        return np.full(len(A), lifetime(s, m, persist))
    if route == "pooled_flat":              # the pilot's seven-season average, carried flat
        return np.full(len(A), float(s.mean()))
    raise ValueError(route)


def appraisal(P, m, rates):
    A = apps(P, m)
    ref = np.array([a["ref_kwh"] for a in A])
    gr = np.array([a["grant"] for a in A])
    L = LIFE[m]
    tonnes = rates * ref / 1000.0 * EF * L
    return {"n": len(A), "grant": float(gr.sum()), "ref_mwh": float(ref.sum() / 1000.0), "tonnes": float(tonnes.sum()),
            "eur_t": float(gr.sum() / tonnes.sum()), "rate": float((rates * ref).sum() / ref.sum()),
            "break_even_rate": float(gr.sum() / (LIMIT * ref.sum() / 1000.0 * EF * L)),
            "app_tonnes": tonnes, "app_grant": gr}


# ---------------------------------------------------------------- the range a fresh draw of the pilot would give

def arm_owners(P, m):
    """the measure's drawn owners (their works buildings) and passed-over owners (their answering buildings): the
    draw's own unit"""
    g, c = _arms(P, m)
    og, oc = {}, {}
    for i in g:
        og.setdefault(int(P.owner[i]), []).append(int(i))
    for i in c:
        oc.setdefault(int(P.owner[i]), []).append(int(i))
    return [np.array(v) for _, v in sorted(og.items())], [np.array(v) for _, v in sorted(oc.items())]


def draw_rows(P, m, rng, unit="owner"):
    """one fresh draw of the pilot's arms: owners resampled within each arm (unit "owner", the draw's unit), or
    buildings within each use and arm (unit "building")"""
    if unit == "owner":
        og, oc = arm_owners(P, m)
        gi = np.concatenate([og[j] for j in rng.integers(0, len(og), len(og))])
        ci = np.concatenate([oc[j] for j in rng.integers(0, len(oc), len(oc))])
        return gi, ci
    g, c = _arms(P, m)
    tg, tc = P.typ[g], P.typ[c]
    gi = np.concatenate([rng.choice(g[tg == t], (tg == t).sum()) for t in np.unique(tg)])
    ci = np.concatenate([rng.choice(c[tc == t], (tc == t).sum()) for t in np.unique(tc)])
    return gi, ci


def eur_t_on_rows(P, m, rows, route="golden"):
    r = app_rates(P, m, route=route, rows=rows)
    return appraisal(P, m, r)["eur_t"]


def draw_range(P, m, B=400, seed=2026, unit="owner", route="golden"):
    """the grant per tonne's 5th and 95th percentiles over B fresh draws, every step repeated"""
    rng = np.random.default_rng(seed + MEASURES.index(m) + (0 if unit == "owner" else 100))
    vals = np.array([eur_t_on_rows(P, m, draw_rows(P, m, rng, unit), route) for _ in range(B)])
    return float(np.percentile(vals, 5)), float(np.percentile(vals, 95)), vals


def funded(eur_t_hi):
    """the committee's rule: a measure is funded where the upper end of its 90 per cent range is within the limit"""
    return eur_t_hi <= LIMIT


# ---------------------------------------------------------------- the round once the offer closes

def pilot_timing(P, m=None):
    rows = [a for a in P.answers19 if m is None or a["measure"] == m]
    early = [a for a in rows if (a["date"] - NOTICE[PILOT]).days <= CUT_DAY]
    late = [a for a in rows if (a["date"] - NOTICE[PILOT]).days > CUT_DAY]
    return rows, early, late


def at_close(P, m, how="golden"):
    """the measure's applications, their grant and the grant paid once the offer has closed and the withdrawals are in"""
    rows, early, late = pilot_timing(P, None if how == "pooled" else m)
    share = len(early) / float(len(rows))
    _, e_m, l_m = pilot_timing(P, m)
    size = np.mean([a["grant"] for a in l_m]) / np.mean([a["grant"] for a in e_m])
    if how in ("count", "pooled"):
        size = 1.0
    de, dl = [a for a in e_m if a["drawn"]], [a for a in l_m if a["drawn"]]
    w_e = np.mean([a["withdrawn"] for a in de]) if de else 0.0
    w_l = np.mean([a["withdrawn"] for a in dl]) if dl else 0.0
    if how in ("one withdrawal rate", "count", "pooled"):
        w_e = w_l = np.mean([a["withdrawn"] for a in de + dl])
    if how in ("no withdrawals", "received"):
        w_e = w_l = 0.0
    A = apps(P, m)
    n = len(A)
    G = sum(a["grant"] for a in A)
    if how == "received":
        return {"n": n, "grant": G, "paid": G, "n_close": n, "grant_close": G, "share": 1.0, "size": 1.0,
                "w_early": 0.0, "w_late": 0.0}
    n_close = n / share
    late_grant = (n_close - n) * (G / n) * size
    if how == "by type":                    # the late applications priced by the 2019 late answers' types and sizes
        late_grant = (n_close - n) * float(np.mean([a["grant"] for a in l_m])) * (G / n) / float(np.mean([a["grant"] for a in e_m]))
    grant_close = G + late_grant
    paid = G * (1 - w_e) + late_grant * (1 - w_l)
    return {"n": n, "grant": G, "share": share, "size": float(size), "w_early": float(w_e), "w_late": float(w_l),
            "n_close": n_close, "grant_close": grant_close, "paid": paid}


def season_saving_2026(P, how="golden", rates=None):
    """tonnes of CO2: what the pilot's works buildings would have used in 2025/26 without the works, less what they
    used, in normal weather, at the plan's factor"""
    k = P.si[PIPELINE]
    k0 = P.si[PILOT]
    tot = 0.0
    for m in MEASURES:
        g, _ = _arms(P, m)
        s = season_savings(P, m)
        if how == "golden":
            s26 = s[-1]
            gg = g[np.isfinite(P.U[g, k])]
            tot += (P.U[gg, k] * s26 / (1.0 - s26)).sum()
        elif how == "by type":
            for t in TYPES:
                gt = g[(P.typ[g] == TYPES.index(t)) & np.isfinite(P.U[g, k])]
                if len(gt) == 0:
                    continue
                st = season_savings(P, m, typ=t)[-1] if len(_arms(P, m, typ=t)[1]) >= 3 else s[-1]
                tot += (P.U[gt, k] * st / (1.0 - st)).sum()
        elif how == "on the use with the works":
            gg = g[np.isfinite(P.U[g, k])]
            tot += (P.U[gg, k] * s[-1]).sum()
        elif how == "average on the 2018/19 use":
            gg = g[np.isfinite(P.U[g, k0])]
            tot += (P.U[gg, k0] * s.mean()).sum()
        elif how == "2025/26 rate on the 2018/19 use":
            gg = g[np.isfinite(P.U[g, k0]) & np.isfinite(P.U[g, k])]
            tot += (P.U[gg, k0] * s[-1]).sum()
        elif how == "before and after":
            gg = g[np.isfinite(P.U[g, k0]) & np.isfinite(P.U[g, k])]
            tot += (P.U[gg, k0] - P.U[gg, k]).sum()
        elif how == "given rates":
            gg = g[np.isfinite(P.U[g, k])]
            tot += (P.U[gg, k] * rates[m] / (1.0 - rates[m])).sum()
    return tot / 1000.0 * EF
