"""task7 architecture 7: the golden analysis and its rivals, on a season-by-building table of normalised gas use read
from the pack (verify.py). The same code runs on the generator's clean truth and on the cleaned pack, so a figure in the
golden is the figure the pack yields.

The pilot's places were drawn by lot among the owners who answered the May 2019 offer, within each measure, so for each
measure and each season since the works the drawn buildings that had them are set against the owners the draw passed
over, both against their own 2018/19 season (the notice season). A measure's works are not equally good everywhere and
do not stay equally good: insulation saves a share of a building's heating and none of its hot water, controls save by
setting the heating back when a building is empty, and heating optimisation's saving falls as heating curves are turned
back up. So the golden carries each measure's season-by-season saving over its service life by fitting its approach to
the level it settles at, takes each building type's own saving from the pilot, and prices every 2026 application at the
saving its own type would make over the measure's life. The round once the offer closes is projected measure by measure
from the 2019 answers: how many were in by the same day after the notice, how much larger the late ones were, and how
many drawn owners withdrew, early and late."""
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
    building's 2019 notice (the register's use where it had none); answered, drawn, works, withdrawn, measure: the 2019
    pilot; answers19: the pilot's responses (b, measure, date, cost, grant, drawn, withdrawn, works); tune_season: the
    season of the building's service visit (0 if none); pipe: the 2026 applications received by 12 June, a revised
    application replacing the earlier one (no, b, measure, grant, ref_kwh, date, typ)."""
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


def apps(P, m):
    return [a for a in P.pipe if a["measure"] == m]


def app_rates(P, m, route="golden", persist="floor", how="ratio_of_totals", base="notice"):
    """each 2026 application's saving over the measure's life, as a share of its reference consumption"""
    s = season_savings(P, m, how, base)
    life_factor = lifetime(s, m, persist) / s.mean()
    A = apps(P, m)
    if route == "golden":                   # its own type's saving, faded as the measure's saving fades
        lv = type_levels(P, m, how, base)
        pooled = float(s.mean())
        return np.array([lv.get(TYPES[a["typ"]], pooled) * life_factor for a in A])
    if route == "class":                    # intermittent against round-the-clock buildings
        lv = class_levels(P, m, how)
        return np.array([lv["round the clock" if TYPES[a["typ"]] in ROUND_CLOCK else "intermittent"] * life_factor
                         for a in A])
    if route == "pooled":                   # the pilot's own mix, faded
        return np.full(len(A), lifetime(s, m, persist))
    if route == "pooled_flat":              # the pilot's seven-season average, carried flat
        return np.full(len(A), float(s.mean()))
    if route == "type_flat":
        lv = type_levels(P, m, how, base)
        return np.array([lv.get(TYPES[a["typ"]], float(s.mean())) for a in A])
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


def funded_set(P, rate_fn):
    out = []
    for m in MEASURES:
        if appraisal(P, m, rate_fn(m))["eur_t"] <= LIMIT:
            out.append(m)
    return tuple(out)


def bootstrap(P, m, B=400, seed=2026, persist="floor"):
    """the grant per tonne's spread when the pilot's buildings are drawn again within each type and arm, every step
    repeated (the seasons' savings, their fit, the types' savings, the applications priced)"""
    rng = np.random.default_rng(seed + MEASURES.index(m))
    A = apps(P, m)
    ref = np.array([a["ref_kwh"] for a in A])
    gr = np.array([a["grant"] for a in A])
    L = LIFE[m]
    g_all, c_all = _arms(P, m)
    k0 = P.si[PILOT]
    ks = list(range(k0 + 1, len(P.seasons)))
    def mats(idx):
        base = P.U[idx, k0]
        cur = P.U[np.ix_(idx, ks)]
        ok = np.isfinite(cur) & np.isfinite(base)[:, None]
        return np.where(ok, cur, 0.0), np.where(ok, base[:, None], 0.0)
    Gc, Gb = mats(g_all)
    Cc, Cb = mats(c_all)
    tg, tc = P.typ[g_all], P.typ[c_all]
    def share(gc, gb, cc, cb):
        return 1.0 - (gc.sum(0) / gb.sum(0)) / (cc.sum(0) / cb.sum(0))
    vals = []
    types_g = {t: np.where(tg == t)[0] for t in np.unique(tg)}
    types_c = {t: np.where(tc == t)[0] for t in np.unique(tc)}
    for _ in range(B):
        gi = np.concatenate([rng.choice(v, len(v)) for v in types_g.values()])
        ci = np.concatenate([rng.choice(v, len(v)) for v in types_c.values()])
        s = share(Gc[gi], Gb[gi], Cc[ci], Cb[ci])
        lf = float(profile(s, L, persist).mean() / s.mean())
        lv = {}
        for t in range(len(TYPES)):
            a_ = gi[tg[gi] == t]
            b_ = ci[tc[ci] == t]
            if len(a_) >= 3 and len(b_) >= 3:
                lv[t] = float(share(Gc[a_], Gb[a_], Cc[b_], Cb[b_]).mean())
        r = np.array([lv.get(a["typ"], float(s.mean())) * lf for a in A])
        vals.append(gr.sum() / (r * ref / 1000.0 * EF * L).sum())
    vals = np.array(vals)
    return float(np.percentile(vals, 5)), float(np.percentile(vals, 95)), vals


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


# ---------------------------------------------------------------- the pilot's saving in the season to April 2026

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
