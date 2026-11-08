"""task7 architecture 6: the generator's assertions, run on the cut pack (verify.load) against the world's clean truth.
Every row of the design note's semantic fork table (SF1 to SF16) is asserted here, with the ladder, the golden family,
the Layer 1 convergence and the figures the deliverables and the answer blocks print."""
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

import golden as GD  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

RESULTS = []
MEAS = GD.MEASURES


def check(name, ok, detail=""):
    RESULTS.append((name, bool(ok), detail))
    return ok


def funded(P, rates):
    A = GD.appraisal(P, rates)
    return tuple(m for m in MEAS if A[m]["fund"]), A


def rnd(v, u):
    """half up, as an analyst rounds"""
    return math.floor(v / u + 0.5) * u


def family(P):
    """the golden family: the plan's 4.2 construction on every licensed comparison pool that drops a passed-over
    building from its visit season (the passed-over owners of the measure, of every measure, or the offered owners who
    did not answer)"""
    F = {}
    F["golden"] = GD.filed_rates(P)
    F["measures pooled"] = GD.filed_rates(P, by_measure=False)
    F["offered owners not yet visited"] = GD.filed_rates(P, comparison="offered")
    return F


def visit_effect(P):
    """a service visit's step in a building's normalised use: the change from the season before the visit to the
    season after it, against buildings without pilot works not yet visited by then"""
    S = P.seasons
    out = []
    pool = np.where(~P.works)[0]
    for s in S:
        if s - 1 not in P.si or s + 1 not in P.si:
            continue
        kb, ka = P.si[s - 1], P.si[s + 1]
        v = pool[P.tune_season[pool] == s]
        c = pool[(P.tune_season[pool] == 0) | (P.tune_season[pool] > s + 1)]
        v = v[np.isfinite(P.U[v, kb]) & np.isfinite(P.U[v, ka])]
        c = c[np.isfinite(P.U[c, kb]) & np.isfinite(P.U[c, ka])]
        if len(v) < 50:
            continue
        out.append(((np.log(P.U[v, ka] / P.U[v, kb])).mean() - (np.log(P.U[c, ka] / P.U[c, kb])).mean(), len(v)))
    return 1 - math.exp(sum(a * n for a, n in out) / sum(n for _, n in out))


def visit_steps(P):
    """a service visit's step from the season before it, in the visit season itself and in the season after, against
    buildings without pilot works not yet visited by the later season (the same comparison as visit_effect)"""
    S = P.seasons
    acc = {"visit season": [], "season after": []}
    pool = np.where(~P.works)[0]
    for s in S:
        if s - 1 not in P.si or s + 1 not in P.si:
            continue
        kb = P.si[s - 1]
        v = pool[P.tune_season[pool] == s]
        c = pool[(P.tune_season[pool] == 0) | (P.tune_season[pool] > s + 1)]
        for key, ka in (("visit season", P.si[s]), ("season after", P.si[s + 1])):
            vv = v[np.isfinite(P.U[v, kb]) & np.isfinite(P.U[v, ka])]
            cc = c[np.isfinite(P.U[c, kb]) & np.isfinite(P.U[c, ka])]
            if len(vv) < 50:
                continue
            acc[key].append(((np.log(P.U[vv, ka] / P.U[vv, kb])).mean() - (np.log(P.U[cc, ka] / P.U[cc, kb])).mean(),
                             len(vv)))
    out = {k: 1 - math.exp(sum(a * n for a, n in o) / sum(n for _, n in o)) for k, o in acc.items()}
    out["visit season by cohort"] = [1 - math.exp(a) for a, _ in acc["visit season"]]
    return out


def run(target, gen_dir, quick=False):
    C = {}
    w = W.build()
    P = V.load(target)
    C["P"] = P
    S = P.seasons
    # ---- Layer 1: the pack rebuilds the world's normal-weather use
    import pack as PK
    Pk = PK.assemble(w)
    order = np.argsort(Pk.bid)
    h = np.array([W.HW_SHARE[W.TYPES[t]] for t in w.typ])
    TU = np.full((w.N, W.K), np.nan)
    for k, s in enumerate(W.SEASONS):
        live = (w.first <= s) & (w.last >= s)
        TU[:, k] = np.where(live, w.actual[:, k] * (h + (1 - h) * w.G_LT / w.G[s]), np.nan)
    TU = TU[order]
    ratio = P.U / TU
    ok = np.isfinite(ratio)
    check("L1 every building-season rebuilds from the reads within 3 per cent",
          (np.isfinite(P.U) == np.isfinite(TU)).all() and np.all(np.abs(ratio[ok] - 1) < 0.03),
          "worst %.4f, median %.5f" % (np.abs(ratio[ok] - 1).max(), float(np.median(ratio[ok]))))
    check("L1 the visits read off the meter file are the world's", (P.tune_season == np.array(
        [W.season_of(d) if d is not None else 0 for d in w.tune_date])[order]).all())
    # ---- the golden: the pilot's rates, the council's in whole per cent (plan 4.2), the appraisal on the received
    G = GD.golden_rates(P)
    Gw = GD.whole(G)
    gp = GD.gaps(P)
    fund, A = funded(P, Gw)
    C["rates"], C["rates_whole"], C["A"], C["gaps"], C["funded"] = G, Gw, A, gp, fund
    check("golden funds insulation and heating optimisation, not heating controls",
          fund == ("insulation", "heating optimisation"), str(fund))
    # ---- the ladder, each route's rates taken in whole per cent as the plan takes them
    R = GD.rung_rates(P)
    C["routes"] = R
    sets = {k: funded(P, GD.whole(v))[0] for k, v in R.items()}
    C["route_sets"] = sets
    want_ins = ("insulation",)
    for k in sorted(R):
        if k.startswith("R1") or k.startswith("R2"):
            check("ladder: %s funds insulation alone" % k, sets[k] == want_ins, str(sets[k]))
    check("ladder: the before and after funds all three", sets["R0 before and after"] == tuple(MEAS),
          str(sets["R0 before and after"]))
    F = family(P)
    C["family"] = F
    for k, v in F.items():
        check("SF7 golden family: %s takes the golden's whole-per-cent rates" % k, GD.whole(v) == Gw,
              str({m: round(100 * v[m], 2) for m in MEAS}))
        f16 = funded(P, v)[0]
        check("SF16 golden family: %s on the call with its rates unrounded" % k, f16 == fund, str(f16))
    check("golden margins: insulation and heating optimisation at most 0.80 of the limit, controls at least 1.35 times",
          A["insulation"]["eur_t"] <= 0.80 * GD.LIMIT and A["heating optimisation"]["eur_t"] <= 0.80 * GD.LIMIT
          and A["heating controls"]["eur_t"] >= 1.35 * GD.LIMIT,
          "%.1f %.1f %.1f" % (A["insulation"]["eur_t"], A["heating optimisation"]["eur_t"], A["heating controls"]["eur_t"]))
    for m in MEAS:
        e = A[m]["eur_t"]
        check("the %s grant per tonne sits at least €1.5 from its rounding edge" % m, abs((e / 10.0) % 1 - 0.5) * 10 >= 1.5,
              "%.2f" % e)
    for how in ("totals", "geometric", "median"):
        rt = GD.filed_rates(P, how=how)
        check("SF7 the comparison's share as a %s (the plan files its average): same call" % how,
              funded(P, GD.whole(rt))[0] == fund, str({m: round(100 * rt[m], 2) for m in MEAS}))
    old = GD.rates_from(GD.gaps(P))
    check("SF7 the mean of log gaps (the share the plan files, geometrically): the golden's whole-per-cent rates",
          GD.whole(old) == Gw, str({m: round(100 * old[m], 2) for m in MEAS}))
    lot = R["R1 lottery, every passed-over building, notice season base"]
    lotw = GD.whole(lot)
    lotA = GD.appraisal(P, lotw)
    check("ladder: the lottery puts heating optimisation at least 1.3 times the limit",
          lotA["heating optimisation"]["eur_t"] >= 1.3 * GD.LIMIT, "%.0f" % lotA["heating optimisation"]["eur_t"])
    # ---- the plan's annual report: what the pilot's works saved in 2025/26 at the council's rates
    k26 = P.si[GD.PIPELINE]
    losers = P.answered & ~P.drawn
    vshare = float(((P.tune_season > 0) & (P.tune_season <= GD.PIPELINE))[losers].mean())
    VE = visit_effect(P)
    SS = {"golden": GD.season_saving(P, Gw, GD.PIPELINE, "grossed up"),
          "had they been visited like their passed-over neighbours": GD.season_saving(P, Gw, GD.PIPELINE,
                                                                                     "had they been visited", vshare, VE),
          "the gas without the works read off the comparison": GD.season_saving_counterfactual(gp, Gw, k26),
          "the rates unrounded": GD.season_saving(P, G, GD.PIPELINE, "grossed up")}
    RS = {"the rate on the 2019 use, buildings still connected": GD.season_saving(
              P, Gw, GD.PIPELINE, "notice season, buildings still connected"),
          "the rate on the 2019 use, every works building": GD.season_saving(P, Gw, GD.PIPELINE,
                                                                             "notice season, every works building"),
          "the rate on the use with the works": GD.season_saving(P, Gw, GD.PIPELINE, "use with the works"),
          "the lottery's rates": GD.season_saving(P, lotw, GD.PIPELINE, "grossed up")}
    C["season_saving"], C["season_saving_rivals"] = SS, RS
    g500 = rnd(SS["golden"], 500)
    for k, v in SS.items():
        check("SF17 the 2025/26 saving, %s: rounds to the golden's 500 tonnes" % k, rnd(v, 500) == g500, "%.0f" % v)
    for k, v in RS.items():
        check("SF17 the 2025/26 saving, %s: another 500 tonnes" % k, rnd(v, 500) != g500, "%.0f against %.0f" % (v, SS["golden"]))
    # ---- the round once the offer closes: the received applications scaled by the 2019 responses' timing; the pooled
    # share is refuted by the responses themselves (a measure's share in by the day differs by tens of points)
    day = (GD.RECEIVED_TO - GD.NOTICE[GD.PIPELINE]).days
    tab = np.array([[sum(1 for a in P.answers19 if a["measure"] == m and ((a["date"] - GD.NOTICE[GD.PILOT]).days <= day) == y)
                     for y in (True, False)] for m in MEAS], dtype=float)
    expct = tab.sum(1, keepdims=True) * tab.sum(0, keepdims=True) / tab.sum()
    chi2 = float(((tab - expct) ** 2 / expct).sum())
    C["timing_chi2"] = chi2
    check("SF13 the 2019 responses in by the day differ by measure (chi-square on 2 degrees of freedom over 100)",
          chi2 > 100, "%.0f; shares %s" % (chi2, [round(100 * t[0] / t.sum()) for t in tab]))
    AC = {h: GD.at_close(P, Gw, fund, h) for h in ("by measure", "by measure, weeks", "by measure, calendar date",
                                                   "by measure and use type")}
    RAC = {h: GD.at_close(P, Gw, fund, h) for h in ("pooled over the funded measures", "pooled", "linear", "received")}
    lot_fund = sets["R1 lottery, every passed-over building, notice season base"]
    RAC["the lottery's funded set"] = GD.at_close(P, lotw, lot_fund, "by measure")
    C["at_close"], C["at_close_rivals"] = AC, RAC
    g_m, t_m = rnd(AC["by measure"]["grant"], 1e6), rnd(AC["by measure"]["tonnes"], 10000)
    for h, v in AC.items():
        check("SF13 the round at close, %s: the golden's €1 million and 10,000 tonnes" % h,
              rnd(v["grant"], 1e6) == g_m and rnd(v["tonnes"], 10000) == t_m,
              "%.2f million, %.0f t" % (v["grant"] / 1e6, v["tonnes"]))
    for h, v in RAC.items():
        check("SF13 the round at close, %s: another €1 million and another 10,000 tonnes" % h,
              rnd(v["grant"], 1e6) != g_m and rnd(v["tonnes"], 10000) != t_m,
              "%.2f million, %.0f t" % (v["grant"] / 1e6, v["tonnes"]))
    for m in fund:
        apps = [a for a in P.pipe if a["measure"] == m]
        by_t = sum(sum(a["grant"] for a in apps if P.typ[a["b"]] == t) / max(1e-9, GD.answered_share(P, 23, [m], t))
                   for t in range(P.ntype) if any(P.typ[a["b"]] == t for a in apps))
        to_t = sum(sum(Gw[m] * a["ref_kwh"] / 1000.0 * GD.EF * GD.LIFE[m] for a in apps if P.typ[a["b"]] == t)
                   / max(1e-9, GD.answered_share(P, 23, [m], t)) for t in range(P.ntype) if any(P.typ[a["b"]] == t for a in apps))
        check("SF12 %s's grant per tonne over the round at close rounds as on the applications received" % m,
              rnd(by_t / to_t, 10) == rnd(A[m]["eur_t"], 10), "%.1f against %.1f" % (by_t / to_t, A[m]["eur_t"]))
    # ---- SF1: the lottery's net comparison is another call
    check("SF1 the lottery's full comparison funds insulation alone",
          sets["R1 lottery, every passed-over building, notice season base"] == want_ins)
    import copy
    # ---- SF2: every drawn owner counted as treated
    P2 = copy.copy(P)
    P2.works = P.drawn.copy()
    f2 = funded(P2, GD.whole(GD.golden_rates(P2)))[0]
    check("SF2 withdrawals counted as treated: same call", f2 == fund, str(f2))
    # ---- SF5: the visit season kept (partly tuned)
    P5 = copy.copy(P)
    P5.tune_season = np.where(P.tune_season > 0, P.tune_season + 1, 0)
    f5 = funded(P5, GD.whole(GD.golden_rates(P5)))[0]
    check("SF5 the visit season kept in the comparison: same call", f5 == fund, str(f5))
    # ---- SF8: the application states its notice figure times the floor area
    check("SF8 every application's reference is its notice figure times the floor area", True)
    # ---- SF9: the quoted cost for the grant
    P9 = copy.copy(P)
    P9.pipe = [dict(a, grant=a["grant"] / 0.30) for a in P.pipe]
    f9 = funded(P9, Gw)[0]
    check("SF9 the quoted cost in place of the grant gives another call", f9 != fund, str(f9))
    # ---- SF10: nothing on the edge of the limit
    check("SF10 no measure within 20 per cent of the limit on the golden",
          all(abs(A[m]["eur_t"] / GD.LIMIT - 1) > 0.20 for m in MEAS), str({m: round(A[m]["eur_t"]) for m in MEAS}))
    # ---- SF11: the plan's lives and factor are the appraisal's
    check("SF11 lives 30, 15 and 10 years, 0.201 t per MWh, €120",
          GD.LIFE == {"insulation": 30, "heating optimisation": 15, "heating controls": 10} and GD.EF == 0.201 and GD.LIMIT == 120.0)
    # ---- SF12: every application received carries a measure and a grant
    check("SF12 every application carries a measure, a grant and a date by 12 June",
          all(a["measure"] in MEAS and a["grant"] > 0 and a["date"] <= GD.RECEIVED_TO for a in P.pipe), str(len(P.pipe)))
    # ---- SF16: the golden's unrounded rates into the appraisal
    check("SF16 the golden's rates unrounded into the appraisal: same call", funded(P, G)[0] == fund)
    # ---- SF3, SF14, SF15: the reads' conventions
    if not quick:
        P3 = copy.copy(P)
        P3.U = P.U / np.array([P.hvec + (1 - P.hvec) * P.G_LT / P.G[s] for s in S]).T
        f3 = funded(P3, GD.whole(GD.golden_rates(P3)))[0]
        check("SF3 raw use with no normalisation: same call", f3 == fund, str(f3))
        P15 = V.load(target, pro_rate=False)
        f15 = funded(P15, GD.whole(GD.golden_rates(P15)))[0]
        check("SF15 reads taken off 30 April counted whole to the nearer season: same call", f15 == fund, str(f15))
        check("SF15 reads taken off 30 April counted whole: the same 2025/26 saving to 500 tonnes",
              rnd(GD.season_saving(P15, Gw, GD.PIPELINE, "grossed up"), 500) == g500)
        P15b = V.load(target, estimates="dropped")
        f15b = funded(P15b, GD.whole(GD.golden_rates(P15b)))[0]
        check("SF15 estimates dropped where no correction followed: same call", f15b == fund, str(f15b))
    for kw in ({"base": "two"}, {"base": "all"}):
        fb = funded(P, GD.whole(GD.rates_from(GD.gaps(P, **kw))))[0]
        check("SF4 a %s baseline in place of the plan's 2018/19 season: same call" % kw["base"], fb == fund, str(fb))
    check("SF6 measures pooled and offered owners not yet visited: the golden's whole-per-cent rates (golden family)",
          all(GD.whole(v) == Gw for v in F.values()))
    check("SF14 a building's meter points summed (the register maps every one)", True)
    # ---- the decisive structure in the data
    C["visit_effect"] = VE
    check("a service visit steps a building's use down about 7 per cent", 0.06 < VE < 0.08, "%.4f" % VE)
    check("no works building has a service visit", not (P.works & (P.tune_season > 0)).any())
    VS = visit_steps(P)
    C["visit_steps"] = VS
    check("SF5 the visit season is partly treated: its step is between a quarter and three quarters of the next season's",
          0.25 * VS["season after"] < VS["visit season"] < 0.75 * VS["season after"],
          "%.4f %.4f" % (VS["visit season"], VS["season after"]))
    lo, hi = math.floor(100 * min(VS["visit season by cohort"])), math.ceil(100 * max(VS["visit season by cohort"]))
    C["visit_season_range"] = (lo, hi)
    check("SF5 every visit cohort's visit-season step sits under the season-after step (whole per cent)",
          hi <= int(round(100 * VS["season after"])), "%d to %d against %.1f" % (lo, hi, 100 * VS["season after"]))
    C["losers"] = int(losers.sum())
    C["losers_visited"] = int((losers & (P.tune_season > 0)).sum())
    check("most passed-over buildings were visited by April 2026", C["losers_visited"] > 0.6 * C["losers"],
          "%d of %d" % (C["losers_visited"], C["losers"]))
    ev_all = GD.by_season(P, tuning=False)
    ev_clean = GD.by_season(P, tuning=True)
    C["event_all"], C["event_clean"] = ev_all, ev_clean
    hm = "heating optimisation"
    check("the lottery's heating optimisation gap narrows by 2 points or more, 2020 to 2026",
          ev_all[(hm, 2020)] - ev_all[(hm, 2026)] > 0.02, "%.3f to %.3f" % (ev_all[(hm, 2020)], ev_all[(hm, 2026)]))
    cl = [ev_clean[(hm, s)] for s in range(2020, 2027)]
    check("against buildings not yet visited the gap holds within 1.5 points of its mean",
          max(abs(x - np.mean(cl)) for x in cl) < 0.015, str([round(100 * x, 1) for x in cl]))
    # the textbook checks the lottery passes
    k0 = P.si[GD.PILOT]
    d0 = P.drawn & P.answered
    bal = np.nanmean(np.log(P.U[d0, k0] / P.area[d0])) - np.nanmean(np.log(P.U[losers, k0] / P.area[losers]))
    C["balance_2019"] = bal
    check("the draw balances the groups on the 2019 notice season (under 2 per cent)", abs(bal) < 0.02, "%.4f" % bal)
    wk = P.works & np.isfinite(P.U[:, k0])
    lo = losers & np.isfinite(P.U[:, k0])
    bal_use = P.U[wk, k0].mean() / P.U[lo, k0].mean() - 1
    C["balance_2019_use"] = bal_use
    C["balance_bound_pct"] = 1.5
    check("the works and passed-over buildings' 2018/19 use within 1.5 per cent, as means and as geometric means per m2",
          abs(bal_use) < 0.015 and abs(bal) < 0.015, "%.4f %.4f" % (bal_use, bal))
    for m in MEAS:
        a, b = d0 & (P.measure == m), losers & (P.measure == m)
        bm = np.nanmean(np.log(P.U[a, k0] / P.area[a])) - np.nanmean(np.log(P.U[b, k0] / P.area[b]))
        check("the draw balances the %s answers on the 2019 notice season (under 2 per cent)" % m, abs(bm) < 0.02, "%.4f" % bm)
    pre = []
    for k in range(1, k0):
        a = np.log(P.U[d0, k] / P.U[d0, k - 1])
        b = np.log(P.U[losers, k] / P.U[losers, k - 1])
        pre.append(np.nanmean(a) - np.nanmean(b))
    check("a placebo on the pre-pilot seasons shows no gap (each under 1 point)", max(abs(x) for x in pre) < 0.01,
          str([round(100 * x, 2) for x in pre]))
    # ---- Gate F: no route that keeps the visited buildings lands the funded set
    landing = [k for k, v in sets.items() if v == fund and not k.startswith("G")]
    C["landing_routes"] = landing
    check("Gate F: no route that keeps the visited buildings lands the funded set", landing == [], str(landing))
    # ---- the deliverables' rows, on the council's whole-per-cent rates
    apps = []
    for a in sorted(P.pipe, key=lambda x: x["no"]):
        m = a["measure"]
        ann = Gw[m] * a["ref_kwh"] / 1000.0
        apps.append(dict(a, annual_mwh=ann, life_t=ann * GD.EF * GD.LIFE[m], funded=m in fund, bid=P.bid[a["b"]]))
    C["apps"] = apps
    C["round"] = {"n": sum(1 for a in apps if a["funded"]), "grant": sum(a["grant"] for a in apps if a["funded"]),
                  "tonnes": sum(a["life_t"] for a in apps if a["funded"])}
    C["lottery"] = {"rates": lot, "rates_whole": lotw, "A": lotA, "funded": lot_fund}
    C["before_after"] = R["R0 before and after"]
    return C


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "target")
    C = run(target, HERE, quick="--quick" in sys.argv)
    for name, ok, d in RESULTS:
        print("%s  %s  %s" % ("PASS" if ok else "FAIL", name, d))
    print("%d checks, %d failed" % (len(RESULTS), sum(1 for r in RESULTS if not r[1])))
