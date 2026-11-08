"""task7 architecture 6: the golden analysis and every rung of the ladder, on a season-by-building table of normalised
gas use. The same code runs on the generator's clean truth (world.py) and on the cleaned pack (verify.py), so a figure
in the golden is the figure the pack yields.

A measure's saving rate is the cut its works make in a building's normal-weather gas use with nothing else changed.
The pilot's places were drawn by lot among the owners who answered the May 2019 offer, so the owners the draw passed
over are the comparison; but the utility's service team tuned the burners of most of them, district by district, from
September 2019, and passed over every building with pilot works. A tuned burner cuts a building's use for good, so a
passed-over building stops being a comparison from the season of its visit (the visit shows in the meter reads as a
read taken at a service visit). For each measure and each season since the works, the drawn buildings that had the
works are set against the passed-over buildings of the same measure not yet visited, both against their own notice
season; the rate is one minus the exponential of the mean log gap over every works building and season."""
import datetime as dt
import math

import numpy as np

MEASURES = ["insulation", "heating optimisation", "heating controls"]
LIFE = {"insulation": 30, "heating optimisation": 15, "heating controls": 10}
EF = 0.201                 # tonnes of CO2 per MWh of gas, the climate action plan's factor
LIMIT = 120.0              # euro of grant per tonne of CO2 over the measure's life
PILOT = 2019
PIPELINE = 2026
NOTICE = {PILOT: dt.date(2019, 5, 20), PIPELINE: dt.date(2026, 5, 20)}   # the notices that carried each offer
CLOSE = {PILOT: dt.date(2019, 6, 30), PIPELINE: dt.date(2026, 6, 30)}    # the day each offer closed
RECEIVED_TO = dt.date(2026, 6, 12)                                          # the applications passed to the utility


class Panel:
    """seasons: list of season years; si: season -> index; U: buildings x seasons normalised use in kWh (nan where not
    connected); typ: type index; ntype; answered: answered the 2019 offer; drawn: given a place by the draw; works:
    pilot works done; measure: the measure asked for (pilot answers and 2026 applications); offered2019: offered in the
    May 2019 notice; tune_season: the season of the building's service visit (0 if none); pipe: the 2026 applications
    (building index, measure, grant, reference kWh)."""
    pass


def untuned(P, idx, k):
    """buildings not visited by the service team by the end of season k"""
    ts = P.tune_season[idx]
    return idx[(ts == 0) | (ts > P.seasons[k])]


def _ok(P, idx, ks):
    sub = P.U[np.ix_(idx, ks)]
    return idx[np.all(np.isfinite(sub) & (sub > 0), axis=1)]


def gaps(P, comparison="losers", tuning=True, base="notice", by_measure=True, seasons=None):
    """per works building and season since the works: (measure, building, season index, log gap, cf kWh, kWh)"""
    k0 = P.si[PILOT]
    S = P.seasons
    ks = [k for k in range(k0 + 1, len(S)) if seasons is None or S[k] in seasons]
    out = []
    for m in MEASURES:
        g_all = np.where(P.works & (P.measure == m))[0]
        if comparison == "losers":
            c_all = np.where(P.answered & ~P.drawn & ((P.measure == m) if by_measure else True))[0]
        elif comparison == "offered":
            c_all = np.where(P.offered2019 & ~P.answered)[0]
        else:
            c_all = np.where(~P.answered & ~P.offered2019)[0]
        for k in ks:
            lo = 0 if base == "all" else (k0 - 1 if base == "two" else k0)
            need = list(range(lo, k0 + 1)) + [k]
            c = _ok(P, untuned(P, c_all, k) if tuning else c_all, need)
            g = _ok(P, g_all, need)
            if len(g) == 0 or len(c) == 0:
                continue
            bg = np.log(P.U[g, lo:k0 + 1]).mean(1)
            bc = np.log(P.U[c, lo:k0 + 1]).mean(1)
            shift = (np.log(P.U[c, k]) - bc).mean()
            gap = np.log(P.U[g, k]) - bg - shift
            for j, i in enumerate(g):
                cf = math.exp(math.log(P.U[i, k]) - gap[j])
                out.append((m, i, k, gap[j], cf, P.U[i, k]))
    return out


def rates_from(gp, how="mean_log"):
    res = {}
    for m in MEASURES:
        rows = [x for x in gp if x[0] == m]
        if how == "mean_log":
            res[m] = 1 - math.exp(np.mean([x[3] for x in rows]))
        elif how == "ratio_of_totals":
            res[m] = 1 - sum(x[5] for x in rows) / sum(x[4] for x in rows)
        elif how == "per_building":
            by = {}
            for x in rows:
                by.setdefault(x[1], []).append(x[3])
            res[m] = 1 - math.exp(np.mean([np.mean(v) for v in by.values()]))
    return res


def filed_rates(P, comparison="losers", tuning=True, by_measure=True, how="mean"):
    """the plan's 4.2 as filed: for each works building and season since the works, its use as a share of its 2018/19
    use, set against the average of that share over the comparison buildings (the passed-over owners of the same
    measure, each dropped from the season of its service visit), one less the first over the second; the rate is the
    average over the works buildings and seasons. how: "mean" (as filed), or the comparison's share taken as a ratio of
    totals, a geometric mean or a median (rivals the filed average rules out)"""
    k0 = P.si[PILOT]
    S = P.seasons
    res = {}
    for m in MEASURES:
        g_all = np.where(P.works & (P.measure == m))[0]
        if comparison == "losers":
            c_all = np.where(P.answered & ~P.drawn & ((P.measure == m) if by_measure else True))[0]
        else:
            c_all = np.where(P.offered2019 & ~P.answered)[0]
        v = []
        for k in range(k0 + 1, len(S)):
            c = _ok(P, untuned(P, c_all, k) if tuning else c_all, [k0, k])
            g = _ok(P, g_all, [k0, k])
            if len(g) == 0 or len(c) == 0:
                continue
            rc = P.U[c, k] / P.U[c, k0]
            if how == "mean":
                ref = rc.mean()
            elif how == "totals":
                ref = P.U[c, k].sum() / P.U[c, k0].sum()
            elif how == "geometric":
                ref = math.exp(np.log(rc).mean())
            else:
                ref = float(np.median(rc))
            v += list(1 - (P.U[g, k] / P.U[g, k0]) / ref)
        res[m] = float(np.mean(v))
    return res


def golden_rates(P):
    return filed_rates(P)


def post_mean_difference(P, tuning=True, by_measure=True, per_m2=False):
    """the lottery read as drawn: the works buildings' mean log use against the passed-over buildings', season by
    season, with no baseline (the draw balanced them)"""
    k0 = P.si[PILOT]
    res = {}
    for m in MEASURES:
        g_all = np.where(P.works & (P.measure == m))[0]
        c_all = np.where(P.answered & ~P.drawn & ((P.measure == m) if by_measure else True))[0]
        num = den = 0.0
        for k in range(k0 + 1, len(P.seasons)):
            c = _ok(P, untuned(P, c_all, k) if tuning else c_all, [k])
            g = _ok(P, g_all, [k])
            sg = P.area[g] if per_m2 else 1.0
            sc = P.area[c] if per_m2 else 1.0
            num += (np.log(P.U[g, k] / sg).mean() - np.log(P.U[c, k] / sc).mean()) * len(g)
            den += len(g)
        res[m] = 1 - math.exp(num / den)
    return res


def by_season(P, tuning=False):
    """each measure's gap season by season since the works (the lottery comparison's event study)"""
    gp = gaps(P, tuning=tuning)
    out = {}
    for m in MEASURES:
        for k in sorted({x[2] for x in gp if x[0] == m}):
            v = [x[3] for x in gp if x[0] == m and x[2] == k]
            out[(m, P.seasons[k])] = 1 - math.exp(np.mean(v))
    return out


def avoided_to_date(gp):
    mwh = sum(x[4] - x[5] for x in gp) / 1000.0
    return mwh, mwh * EF


def appraisal(P, rates, limit=LIMIT):
    """the climate action plan's appraisal of the 2026 round: each application's tonnes are its measure's saving rate
    times its reference consumption times the factor times the measure's life; a measure is funded when its grant per
    tonne over the round's applications for it is at the limit or under"""
    per = {}
    for m in MEASURES:
        apps = [a for a in P.pipe if a["measure"] == m]
        grant = sum(a["grant"] for a in apps)
        ref = sum(a["ref_kwh"] for a in apps) / 1000.0
        tonnes = rates[m] * ref * EF * LIFE[m]
        per[m] = {"n": len(apps), "grant": grant, "ref_mwh": ref, "tonnes": tonnes,
                  "eur_t": grant / tonnes if tonnes > 0 else float("inf"),
                  "fund": tonnes > 0 and grant / tonnes <= limit,
                  "break_even_rate": grant / (limit * ref * EF * LIFE[m])}
    return per


def rung_rates(P):
    R = {}
    k0 = P.si[PILOT]
    S = P.seasons
    res = {}
    for m in MEASURES:
        g = np.where(P.works & (P.measure == m))[0]
        v = []
        for k in range(k0 + 1, len(S)):
            gg = _ok(P, g, [k0, k])
            v += list(np.log(P.U[gg, k]) - np.log(P.U[gg, k0]))
        res[m] = 1 - math.exp(np.mean(v))
    R["R0 before and after"] = res
    R["R1 lottery, every passed-over building, notice season base"] = rates_from(gaps(P, tuning=False))
    R["R1a lottery, every passed-over building, as drawn"] = post_mean_difference(P, tuning=False)
    if getattr(P, "area", None) is not None:
        R["R1f lottery, every passed-over building, as drawn, use per square metre"] = post_mean_difference(
            P, tuning=False, per_m2=True)
    R["R1b lottery, every passed-over building, panel base"] = rates_from(gaps(P, tuning=False, base="all"))
    R["R1c lottery, every passed-over building, first season only"] = rates_from(gaps(P, tuning=False, seasons=(2020,)))
    R["R1d lottery, every passed-over building, last two seasons"] = rates_from(gaps(P, tuning=False, seasons=(2025, 2026)))
    R["R1e lottery, every passed-over building, seasons to 2022"] = rates_from(
        gaps(P, tuning=False, seasons=(2020, 2021, 2022)))
    R["R2 offered owners who did not answer"] = rates_from(gaps(P, comparison="offered", tuning=False))
    R["R2b everyone outside the pilot, panel base"] = rates_from(gaps(P, comparison="everyone", tuning=False, base="all"))
    R["G1 lottery, passed-over buildings not yet visited"] = golden_rates(P)
    R["G1a lottery, not yet visited, as drawn"] = post_mean_difference(P)
    R["G1b lottery, not yet visited, panel base"] = rates_from(gaps(P, base="all"))
    R["G1c lottery, not yet visited, two-season base"] = rates_from(gaps(P, base="two"))
    R["G1d lottery, not yet visited, every measure pooled"] = rates_from(gaps(P, by_measure=False))
    R["G1t lottery, not yet visited, ratio of totals"] = rates_from(gaps(P), "ratio_of_totals")
    R["G1p lottery, not yet visited, by building"] = rates_from(gaps(P), "per_building")
    R["G2 offered owners who did not answer, not yet visited"] = rates_from(gaps(P, comparison="offered"))
    R["G2b everyone outside the pilot not yet visited, panel base"] = rates_from(gaps(P, comparison="everyone", base="all"))
    return R


GOLDEN_FAMILY = ["G1 lottery, passed-over buildings not yet visited", "G1a lottery, not yet visited, as drawn",
                 "G1b lottery, not yet visited, panel base", "G1c lottery, not yet visited, two-season base",
                 "G1d lottery, not yet visited, every measure pooled", "G1t lottery, not yet visited, ratio of totals",
                 "G1p lottery, not yet visited, by building", "G2 offered owners who did not answer, not yet visited"]


def whole(rates):
    """the council's saving rates: the pilot's, in whole per cent (the climate action plan, 4.2)"""
    return {m: math.floor(100 * rates[m] + 0.5) / 100.0 for m in MEASURES}


def answered_share(P, day, measures=None, typ=None):
    """the share of the 2019 answers (for the given measures, of the given use type) in by the given day after the
    notice"""
    xs = [a for a in P.answers19 if (measures is None or a["measure"] in measures) and (typ is None or P.typ[a["b"]] == typ)]
    return sum((a["date"] - NOTICE[PILOT]).days <= day for a in xs) / float(len(xs))


def at_close(P, rates, funded, how="by measure"):
    """the funded round once the offer closes on 30 June: each funded measure's applications received by 12 June, with
    their grant and lifetime tonnes, scaled up by the share of the 2019 answers for that measure that had come in by the
    same day after the notice"""
    day = (RECEIVED_TO - NOTICE[PIPELINE]).days
    span = (CLOSE[PIPELINE] - NOTICE[PIPELINE]).days
    out = {"n": 0.0, "grant": 0.0, "tonnes": 0.0}

    def add(apps, m, f):
        out["n"] += len(apps) / f
        out["grant"] += sum(a["grant"] for a in apps) / f
        out["tonnes"] += sum(rates[m] * a["ref_kwh"] / 1000.0 * EF * LIFE[m] for a in apps) / f
    for m in funded:
        apps = [a for a in P.pipe if a["measure"] == m]
        if how == "by measure and use type":
            for t in range(P.ntype):
                at = [a for a in apps if P.typ[a["b"]] == t]
                if at:
                    add(at, m, answered_share(P, day, [m], t))
            continue
        if how == "by measure":
            f = answered_share(P, day, [m])
        elif how == "by measure, weeks":
            lo, hi = answered_share(P, 21, [m]), answered_share(P, 28, [m])
            f = lo + (hi - lo) * (day - 21) / 7.0
        elif how == "by measure, calendar date":
            f = sum(a["date"] <= dt.date(2019, RECEIVED_TO.month, RECEIVED_TO.day) for a in P.answers19
                    if a["measure"] == m) / float(sum(a["measure"] == m for a in P.answers19))
        elif how == "pooled over the funded measures":
            f = answered_share(P, day, list(funded))
        elif how == "pooled":
            f = answered_share(P, day)
        elif how == "linear":
            f = day / float(span)
        else:
            f = 1.0
        add(apps, m, f)
    return out


def season_saving(P, rates, season=PIPELINE, how="grossed up", visited_share=0.0, step=0.0):
    """what the pilot's works saved in a season (the plan's annual report): each measure's saving rate on the gas its
    buildings would have used that season without the works, normalised, in tonnes of CO2"""
    k = P.si[season]
    k0 = P.si[PILOT]
    t = 0.0
    for m in MEASURES:
        idx = np.where(P.works & (P.measure == m))[0]
        ok = idx[np.isfinite(P.U[idx, k]) & (P.U[idx, k] > 0)]
        if how == "grossed up":
            t += rates[m] * (P.U[ok, k] / (1 - rates[m])).sum()
        elif how == "had they been visited":
            t += rates[m] * (P.U[ok, k] / (1 - rates[m])).sum() * (1 - visited_share * step)
        elif how == "use with the works":
            t += rates[m] * P.U[ok, k].sum()
        elif how == "notice season, buildings still connected":
            ok0 = ok[np.isfinite(P.U[ok, k0])]
            t += rates[m] * P.U[ok0, k0].sum()
        elif how == "notice season, every works building":
            ok0 = idx[np.isfinite(P.U[idx, k0])]
            t += rates[m] * P.U[ok0, k0].sum()
    return t / 1000.0 * EF


def season_saving_counterfactual(gp, rates, season_index):
    """the same, the gas without the works read off the comparison: each works building's own notice season moved as
    the comparison moved"""
    return sum(rates[x[0]] * x[4] for x in gp if x[2] == season_index) / 1000.0 * EF
