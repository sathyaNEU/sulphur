"""Every owed figure, computed on the shipped files: figures.json (what the answer blocks and the goldens state) and
effort.json (each result's golden, band and the three passes, the stump factorial, the forcing on both sides), with
the core's spec rebuilt on the cut pack (the same shape as core.py: members, lattice, falsification, run routes with
their settings, each stump pushed past its fit, the figures with their routes) and re-proved by corelib.

    python3 task4/generator/results.py [target]      prints the core table and CORE PASS level N on the cut pack
"""
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "stumping"))
import analysis as A  # noqa: E402
import corelib  # noqa: E402
import effort as EF  # noqa: E402

POOLS = A.POOLS
KEYS = ["S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"]
REFLEX = "S1+S2+S3"
ALONE = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
BASE_RUNS = ("hedge", "generous", "calibrated", "cutoff")
COVER = {"nothing": "no cover", "hire": "seasonal hire", "buy": "purchase"}
COMPS = (("C1", "rise", "trade_rise"), ("C2", "fullest", "store_2027"), ("C3", "year_loss", "year_loss"))
STUMPS = {
    "S1": dict(axis="what", opens="K50", steps_left=5, precedents=["L56", "L57", "L07"],
               said_out_loud="A rep's cellar count is of the full containers of a line on its order day, and the "
                             "empties wait there for the dray, so what the trade holds is more than the counts show "
                             "and does not move in step with its sales."),
    "S2": dict(axis="when", opens="K20", steps_left=4, precedents=["N17", "N02", "L37"],
               said_out_loud="The store receives each beer a whole racking run at a time, so its stock follows the runs "
                             "and the number of beers on sale, and both change in 2027."),
    "S3": dict(axis="who", opens="FIR", steps_left=4, precedents=["L53", "L43", "N13"],
               said_out_loud="A container lost in the trade is never taken off the register, so the register is not "
                             "the fleet and nothing records how many are lost."),
}
BAND_ROOM = corelib.BAND_ROOM


def band_of(g, fam):
    """the band the answer blocks state: the battery's range and a quarter of its width as room on each side (the
    rule corelib prices the rubric on)"""
    lo, hi = min(list(fam) + [g]), max(list(fam) + [g])
    w = hi - lo
    return [int(math.floor(lo - BAND_ROOM * w)), int(math.ceil(hi + BAND_ROOM * w))]


def cover_set(v):
    return ["%s: %s" % (A.PLURAL[p], COVER[A.cover_of(v[p], p)]) for p in POOLS]


def total(rows, field):
    return float(sum(rows[p][field] for p in POOLS))


def figures(X):
    R = X["R"]
    n = len(A.FAMILY)
    gold = {p: X["gold"][p]["short"] for p in POOLS}
    hot = {p: X["hot"][p][0] for p in POOLS}
    fam = {p: [x["short"] for x in X["fam"][p]] for p in POOLS}
    hfam = {p: X["hot_fam"][p] for p in POOLS}
    lat = {k: {p: X["lat"][p][k]["short"] for p in POOLS} for k in KEYS}
    hlat = {k: {p: X["hot_lat"][p][k] for p in POOLS} for k in KEYS}
    runs = {k: {p: X["runs"][p][k]["short"] for p in POOLS} for k in A.RUN}
    hruns = {k: {p: X["hot_runs"][p][k] for p in POOLS} for k in A.RUN}
    over = {s: {p: X["over"][p][s]["short"] for p in POOLS} for s in A.OVER}
    comp = {}
    for cid, field, key in COMPS:
        comp[cid] = dict(key=key, golden=total(X["gold"], field),
                         family=[float(sum(X["fam"][p][i][field] for p in POOLS)) for i in range(n)],
                         lattice={k: float(sum(X["lat"][p][k][field] for p in POOLS)) for k in KEYS},
                         rigorous=total(X["rigorous"], field),
                         runs={k: float(sum(X["runs"][p][k][field] for p in POOLS)) for k in A.RUN},
                         by_pool={p: X["gold"][p][field] for p in POOLS})
    iso = lambda d: d.isoformat()
    r0 = lambda x: int(round(x))
    fig = {"call": cover_set(gold), "cover": {p: A.cover_of(gold[p], p) for p in POOLS},
           "plan": {p: r0(gold[p]) for p in POOLS}, "plan_band": {p: band_of(gold[p], fam[p]) for p in POOLS},
           "plan_week": {p: iso(X["gold"][p]["date"]) for p in POOLS},
           "hot": {p: r0(hot[p]) for p in POOLS}, "hot_band": {p: band_of(hot[p], hfam[p]) for p in POOLS},
           "min_run": dict(A.MIN_RUN), "names": dict(A.NAMES), "plural": dict(A.PLURAL)}
    for cid, field, key in COMPS:
        c = comp[cid]
        fig[key] = int(sum(r0(c["by_pool"][p]) for p in POOLS))           # the stated total is the sum of its parts
        fig[key + "_band"] = band_of(c["golden"], c["family"])
        fig[key + "_by_pool"] = {p: r0(c["by_pool"][p]) for p in POOLS}
        fig[key + "_band_by_pool"] = {p: band_of(X["gold"][p][field], [x[field] for x in X["fam"][p]]) for p in POOLS}
    last = R.WH
    year = {p: float(R.flow[p][last - 52:last].sum()) for p in POOLS}
    fig["account_at_count"] = {p: {"register": int(R.register[p]), "on_site": int(R.take[p]["onsite"])} for p in POOLS}
    fig["account"] = {}
    for p in POOLS:
        g = X["gold"][p]
        fig["account"][p] = dict(register=int(R.register[p]), on_site=int(R.take[p]["onsite"]),
                                 store=int(R.take[p]["store"]), clean_empty=int(R.take[p]["idle"]),
                                 depots_wash_repair=int(R.take[p]["other"]), alive=r0(g["alive"]),
                                 in_trade_alive=r0(g["alive"] - R.take[p]["onsite"]),
                                 never_coming_back=r0(R.register[p] - g["alive"]), lost_year=r0(g["year_loss"]),
                                 lost_pct=round(100.0 * g["year_loss"] / g["alive"], 1),
                                 leaving_pct=round(100.0 * (1.0 - math.exp(-g["lam_y"])), 1),
                                 share_on_site=round(g["share_on"], 2), condemned_year=int(R.condemned[p]),
                                 deliveries_year=r0(year[p]), deliveries_week_at_count=r0(g["lev"]),
                                 deliveries_week_last=r0(R.flow[p][R.WH - 1]),
                                 lines=int(g["L"]), estate_lines=int(sum(x for _, x in R.estate[p])),
                                 rise=r0(g["rise"]), store_fullest=r0(g["fullest"]), plan=r0(gold[p]), hot=r0(hot[p]),
                                 lots=len(R.lots[p]["lot"]))
    fig["pool"] = {}
    for p in POOLS:
        g = X["gold"][p]
        pk = g["pick"]
        c = R.counts[p]
        sold = c["count_rate"] * c["count_days"] / 7.0
        fig["pool"][p] = dict(fixed_per_line=round(g["a"], 2), per_sale_weekly=round(g["slope1"], 2),
                              per_sale_twice=round(g["slope_half"], 2), per_sale_half=round(g["b"], 2),
                              trade_per_sale=round(g["b"] * g["m"], 2), checks=int(g["n_counts"]),
                              face_per_sale_weekly=round(X["lat"][p]["S1"]["slope1"], 2),
                              face_fixed=round(X["lat"][p]["S1"]["a"], 2),
                              mean_full=round(float(c["count_full"].mean()), 2),
                              mean_added_back=round(float(sold.mean()), 2),
                              mean_days=round(float(c["count_days"].mean()), 1),
                              store_cover_weeks=round(g["cov"], 3), share_runs_2026=r0(g["half26"]),
                              runs_2026_total=r0(g["full26"]),
                              beers_2026=len(A.runs_of(R, p)), beers_at_fullest=int(max(R.beers_on[p][i] for i in R.season)),
                              runs_on_sale_at_fullest=r0(max(R.runs_on[p][i] for i in R.season)),
                              other_weeks=round(g["c2"], 3), leaving_rate=round(g["lam_y"], 4), bend_c=round(g["hinge"], 1),
                              week=iso(pk["date"]), deliveries_at_week=r0(pk["D"]), estate_at_week=r0(pk["es"]),
                              swing=r0(pk["swing"]), store=r0(pk["store"]), other=r0(pk["other"]), float=r0(pk["float"]),
                              drain=r0(pk["drain"]), temp_at_week=round(pk["temp"], 1),
                              store_cover_route=r0(X["lat"][p]["S2"]["fullest"]),
                              face_rise=r0(X["lat"][p]["S1"]["rise"]), cover_weeks_2026=round(float(
                                  R.store[p][52:].mean() / R.flow[p][52:].mean()), 2))
    fig["lots"] = {p: [dict(lot=L, age=round(float(a), 1), register=int(r), on_site=int(o),
                            share=round(float(o) / float(r), 3) if r else None)
                       for L, a, r, o in zip(R.lots[p]["lot"], R.lots[p]["age"], R.lots[p]["reg"], R.lots[p]["ons"])]
                   for p in POOLS}
    fig["summers"] = {p: {str(y): r0(A.chain(R, p, None, A.summer_temps(R, y))["short"]) for y in A.SUMMERS}
                      for p in POOLS}
    fig["hot_year"] = {p: int(sorted(fig["summers"][p], key=lambda y: fig["summers"][p][y])[A.HOT_RANK]) for p in POOLS}
    fig["season"] = [iso(R.week_dates[R.season[0]]), iso(R.week_dates[R.season[-1]])]
    routes = {"golden": (gold, hot), "direct": (X["direct"], X["hot_direct"]),
              "rigorous": ({p: X["rigorous"][p]["short"] for p in POOLS}, X["hot_rigorous"])}
    routes.update({k: (lat[k], hlat[k]) for k in KEYS})
    routes.update({"run " + k: (runs[k], hruns[k]) for k in A.RUN})
    routes.update({"over " + s: (over[s], {p: None for p in POOLS}) for s in A.OVER})
    fig["routes"] = {k: {p: {"plan": r0(v[p]), "hot": None if h[p] is None else r0(h[p]),
                             "cover": A.cover_of(v[p], p)} for p in POOLS} for k, (v, h) in routes.items()}
    fig["route_calls"] = {k: cover_set(v) for k, (v, h) in routes.items()}
    rc = {k: {cid: r0(comp[cid]["lattice"][k]) for cid in comp} for k in KEYS}
    rc["rigorous"] = {cid: r0(comp[cid]["rigorous"]) for cid in comp}
    rc.update({"run " + k: {cid: r0(comp[cid]["runs"][k]) for cid in comp} for k in A.RUN})
    fig["route_components"] = rc
    fig["distinct_wrong_calls"] = len({tuple(cover_set(lat[k])) for k in KEYS})
    fig["allowances"] = {k: {"plan": {p: r0(X["allowances"][k][p]["short"]) for p in POOLS},
                             "C1": r0(sum(X["allowances"][k][p]["rise"] for p in POOLS)),
                             "cover": {p: A.cover_of(X["allowances"][k][p]["short"], p) for p in POOLS}}
                         for k in X["allowances"]}
    fig["joint"] = {p: r0(X["joint"][p]["short"]) for p in POOLS}
    fig["joint_coef"] = {p: round(X["joint"][p]["days_coef"], 2) for p in POOLS}
    fig["level_fit_week"] = iso(R.week_dates[R.WH - 1])
    fig["level_fit_temp"] = round(R.temp_hist[R.WH - 1], 1)
    fig["store_fit"] = {k: {"share": round(v["theta"], 3), "se": round(v["se"], 3), "n": v["n"],
                            "cover": {p: round(c, 3) for p, c in v["cov"].items()}} for k, v in X["store_fits"].items()}
    fig["typeown"] = {p: {str(w): round(v, 2) for w, v in d.items()} for p, d in X["typeown"].items()}
    fig["typeown_range"] = [round(min(v for d in X["typeown"].values() for v in d.values()), 2),
                            round(max(v for d in X["typeown"].values() for v in d.values()), 2)]
    fig["beer_cover"] = {p: {"plan": r0(X["beer_cover"][p]["short"]), "cover": A.cover_of(X["beer_cover"][p]["short"], p),
                             "store": r0(X["beer_cover"][p]["fullest"])} for p in POOLS}
    fig["beer_cover_C2"] = r0(sum(X["beer_cover"][p]["fullest"] for p in POOLS))
    fig["nearest_by_pool"] = {}
    for p in POOLS:
        best = min((min(abs(x - ln) for ln in (0.0, float(A.MIN_RUN[p]))), i) for i, x in enumerate(fam[p]))
        x = fam[p][best[1]]
        ln = min((0.0, float(A.MIN_RUN[p])), key=lambda l: abs(x - l))
        fig["nearest_by_pool"][p] = {"distance": r0(best[0]), "figure": r0(x), "line": r0(ln),
                                     "variant": A.FAMILY[best[1]][0]}
    fig["deviance"] = {p: {"exponential": round(v[0], 1), "line": round(v[1], 1), "gap": round(v[1] - v[0], 1)}
                       for p, v in X["deviance"].items()}
    fig["deviance"]["pooled"] = {"gap": round(sum(v[1] - v[0] for v in X["deviance"].values()), 1)}
    fig["absolute_gap"] = {p: r0(v) for p, v in X["absolute_gap"].items()}
    fig["slope_se"] = {p: {k: round(v, 3) for k, v in X["slope_se"][p].items()} for p in POOLS}
    fig["refused"] = {name: {p: r0(v[p]) for p in POOLS} for name, v in X["refused"].items()}
    fig["refused_cover"] = {name: {p: A.cover_of(v[p], p) for p in POOLS} for name, v in X["refused"].items()}
    fig["rate_diag"] = {k: {"slope": {p: round(v["slope"][p], 2) for p in POOLS}, "fall": round(-v["fall"][0], 3)}
                        for k, v in X["rate_diag"].items()}
    fig["level_diag"] = {p: {k: round(v, 3) if k in ("scatter", "count_week") else r0(v) for k, v in d.items()}
                         for p, d in X["level_diag"].items()}
    for p in POOLS:
        fig["level_diag"][p]["count_week_pct"] = round(100.0 * X["level_diag"][p]["count_week"], 1)
        fig["level_diag"][p]["scatter_pct"] = round(100.0 * X["level_diag"][p]["scatter"], 1)
    fig["level4"] = {p: r0(X["level4"][p]) for p in POOLS}
    # the worst week, with any week next to it that sits within the worst week's own measured spread of deliveries
    fig["worst_weeks"] = {}
    for p in POOLS:
        g = X["gold"][p]
        sea = [x for x in g["path"] if x["i"] in R.season]
        k = [x["i"] for x in sea].index(g["week"])
        tol = X["spreads"][p]["x_del"] * g["pick"]["D"]
        lo, hi = k, k
        while lo > 0 and sea[lo - 1]["short"] >= g["short"] - tol:
            lo -= 1
        while hi < len(sea) - 1 and sea[hi + 1]["short"] >= g["short"] - tol:
            hi += 1
        fig["worst_weeks"][p] = [iso(x["date"]) for x in sea[lo:hi + 1]]
    dc, se, nn = X["days_check"]
    fig["falsification"] = dict(fall=round(-dc, 2), coef=round(dc, 2), se=round(se, 2), checks=nn)
    fig["variants"] = n
    fig["battery"] = len(A.BATTERY)
    bat = {p: [x["short"] for x in X["bat"][p]] for p in POOLS}
    hbat = {p: X["hot_bat"][p] for p in POOLS}
    fig["battery_range"] = {p: [r0(min(bat[p])), r0(max(bat[p]))] for p in POOLS}
    fig["battery_range_hot"] = {p: [r0(min(hbat[p])), r0(max(hbat[p]))] for p in POOLS}
    fig["battery_calls_all_golden"] = all(cover_set({p: bat[p][i] for p in POOLS}) == fig["call"]
                                          for i in range(len(A.BATTERY)))
    fig["battery_outside_band"] = {p: sum(1 for x in bat[p] if not fig["plan_band"][p][0] <= x <= fig["plan_band"][p][1])
                                   for p in POOLS}
    fig["singles"] = len(A.SINGLES)
    fig["variant_range"] = {p: [r0(min(fam[p])), r0(max(fam[p]))] for p in POOLS}
    fig["variant_range_hot"] = {p: [r0(min(hfam[p])), r0(max(hfam[p]))] for p in POOLS}
    fig["family_calls_all_golden"] = all(cover_set({p: fam[p][i] for p in POOLS}) == fig["call"] for i in range(n))
    near = min((min(abs(fam[p][i] - ln) for ln in (0.0, float(A.MIN_RUN[p]))), p, A.FAMILY[i][0])
               for p in POOLS for i in range(n))
    fig["nearest_variant"] = {"distance": r0(near[0]), "pool": near[1], "variant": near[2]}
    fig["perturbations"] = [{"input": name, "call_holds": cover_set(v) == fig["call"], "plan": {p: r0(v[p]) for p in POOLS}}
                            for name, v in X["forcing"].items()]
    fig["perturbations"] += [{"input": "all four fitted inputs %s together, two measured spreads each" % side,
                              "call_holds": cover_set(v) == fig["call"], "plan": {p: r0(v[p]) for p in POOLS}}
                             for side, v in X["corners"].items()]
    fig["spreads_pct"] = {p: {k: round(100.0 * v, 1) for k, v in X["spreads"][p].items()} for p in POOLS}
    fig["stated"] = dict(fs04=["1.1", "2.1", "2.2", "2.3", "3.1", "3.2", "3.3", "3.4", "4.1", "4.2", "5.1", "5.2"],
                         quotation="Q26-1187", float_sevenths=2, hot_rank=2, summers=10, season_weeks=len(R.season),
                         store_weeks=104, window_weeks=[4, 13], forcing_pct=[20, 5], spreads=2, bend_grid=[12, 22, 0.5])
    fig["counts"] = dict(docket_rows=int(R.docket_rows), resent_rows=int(R.resent_rows), delivery_lines=int(R.del_rows),
                         blank_codes=int(R.blank_codes), dockets=int(R.dockets), accounts=int(R.n_accounts),
                         renumbered=int(R.renumbered), register_rows=int(R.register_rows), rackings=int(R.rackings),
                         check_rows=int(R.check_rows), check_doubles=int(R.check_doubles),
                         check_calls=int(R.check_calls), checks=int(sum(len(R.counts[p]["count_full"]) for p in POOLS)),
                         weeks=int(R.WH), first_week=iso(R.D0), count_date=iso(R.asof), estate_pubs=int(R.estate_pubs),
                         lines=int(sum(len(R.lines[p]["keys"]) for p in POOLS)),
                         register=int(sum(R.register[p] for p in POOLS)),
                         on_site=int(sum(R.take[p]["onsite"] for p in POOLS)))
    path = {}
    for p in POOLS:
        g = X["gold"][p]
        rows = []
        for x in g["path"]:
            parts = dict(at_customers=r0(g["alive_out"] + x["swing"]), store=r0(x["store"]), other=r0(x["other"]),
                         float=r0(x["float"]))
            req, short = sum(parts.values()), r0(x["short"])
            rows.append(dict(week=iso(x["date"]), in_season=bool(x["i"] in R.season), deliveries=r0(x["D"]),
                             requirement=req, fleet=req - short, shortfall=short, **parts))
        path[p] = rows
    fig["path"] = path
    fig["beers"] = {p: [dict(sku=s, first=iso(a), last=iso(b), run=int(run)) for s, a, b, run in R.plan[p]]
                    for p in POOLS}
    fig["runs_2026"] = {p: {s: r0(v) for s, v in sorted(A.runs_of(R, p).items())} for p in POOLS}
    Rr = dict(gold=gold, hot=hot, fam=fam, hfam=hfam, lat=lat, hlat=hlat, runs=runs, hruns=hruns, over=over, comp=comp)
    return fig, Rr


def spec_of(X, fig, Rr, truth):
    """the core's spec rebuilt on the cut pack, each figure with the band the answer blocks state"""
    members = {p: dict(lines=[0.0, float(A.MIN_RUN[p])], truth=float(truth[p]), golden=float(Rr["gold"][p]),
                       family=[float(x) for x in Rr["fam"][p]],
                       routes=dict(direct=float(X["direct"][p]), rigorous=float(X["rigorous"][p]["short"])))
               for p in POOLS}
    figs = []
    for cid, field, key in COMPS:
        c = Rr["comp"][cid]
        routes = {"rigorous": c["rigorous"]}
        routes.update({k: c["runs"][k] for k in BASE_RUNS})
        figs.append(dict(id=cid, block="component", golden=c["golden"], family=c["family"], band=fig[key + "_band"],
                         lattice=dict(c["lattice"]), routes=routes))
    # the asks: the fleet account, one row a pool and one sentence a row (lost over the year to the count, the trade's
    # rise to its summer peak, the store at its fullest, the planning and the hot case's largest weekly shortfall)
    for p in POOLS:
        figs.append(dict(id="A-%s" % p, block="ask", member=p, sentence="row-%s" % p, band=fig["plan_band"][p]))
        routes = {"rigorous": float(X["hot_rigorous"][p])}
        routes.update({k: float(Rr["hruns"][k][p]) for k in BASE_RUNS})
        figs.append(dict(id="H-%s" % p, block="ask", sentence="row-%s" % p, golden=float(Rr["hot"][p]),
                         family=[float(x) for x in Rr["hfam"][p]], band=fig["hot_band"][p],
                         lattice={k: float(Rr["hlat"][k][p]) for k in KEYS}, routes=routes))
        for tag, field, key in (("T", "rise", "trade_rise"), ("S", "fullest", "store_2027"), ("L", "year_loss", "year_loss")):
            routes = {"rigorous": float(X["rigorous"][p][field])}
            routes.update({k: float(X["runs"][p][k][field]) for k in BASE_RUNS})
            figs.append(dict(id="%s-%s" % (tag, p), block="ask", sentence="row-%s" % p, golden=float(X["gold"][p][field]),
                             family=[float(x[field]) for x in X["fam"][p]], band=fig[key + "_band_by_pool"][p],
                             lattice={k: float(X["lat"][p][k][field]) for k in KEYS}, routes=routes))
    dc, se, nn = X["days_check"]
    falsification = dict(check="across the cellar checks, with a line's weekly sales and delivery interval held, the "
                               "full containers counted fall with each container the line has sold since the dray "
                               "last called (the dockets give the day); no file holds a line's empties, the trade's "
                               "stock or any pool's shortfall",
                         observes_target=False, truth=dc, golden=-1.0,
                         rivals={"the count as it stands is what the line holds": 0.0,
                                 "the count and a whole delivery is what the line holds": 0.0,
                                 "the count and half a delivery is what the line holds": 0.0})
    stumps = {s: dict(STUMPS[s], sides={"over": {p: float(Rr["over"][s][p]) for p in POOLS}}) for s in STUMPS}
    return dict(task="task4 architecture 14 loop 1, cut pack", call="lines", members=members,
                lattice={k: {p: float(Rr["lat"][k][p]) for p in POOLS} for k in KEYS}, falsification=falsification,
                run_routes={k: {p: float(Rr["runs"][k][p]) for p in POOLS} for k in A.RUN}, figures=figs, stumps=stumps)


def result_values(plan, hot, comps, account):
    r = lambda d: {p: int(round(d[p])) for p in POOLS}
    return {"R1": account, "R2": int(round(comps["C1"])), "R3": int(round(comps["C3"])), "R4": int(round(comps["C2"])),
            "R5": r(plan), "R6": r(hot), "R7": cover_set(plan)}


def effort(X, fig, Rr):
    comps_at = lambda k: {c: Rr["comp"][c]["lattice"][k] for c in ("C1", "C2", "C3")}
    acct = fig["account_at_count"]
    gold = result_values(Rr["gold"], Rr["hot"], {c: Rr["comp"][c]["golden"] for c in ("C1", "C2", "C3")}, acct)
    gold.update(R2=fig["trade_rise"], R3=fig["year_loss"], R4=fig["store_2027"])     # the stated totals
    quick = {"R1": None, "R2": None, "R3": None, "R4": None, "R5": {p: int(round(X["direct"][p])) for p in POOLS},
             "R6": {p: int(round(X["hot_direct"][p])) for p in POOLS}, "R7": cover_set(X["direct"])}
    careful = result_values(Rr["lat"][REFLEX], Rr["hlat"][REFLEX], comps_at(REFLEX), acct)
    meta = [
        ("R1", "each pool's account at the count of 30 November 2026: on the register and counted on site",
         "Step-by-Step", "account_at_count", [], "", {}, []),
        ("R2", "the rise in the trade's stock from the count to its summer peak, the estate's cellars included, over "
               "the five pools (containers)", "Component 1", "trade_rise", [],
         "the cellar checks, the dockets, the route plan and the supply agreement's schedule",
         dict(band=fig["trade_rise_band"]), ["L56", "L57", "L07"]),
        ("R3", "the containers the trade lost over the year to the count over the five pools", "Component 3", "year_loss", [],
         "the count by lot, the register and the dockets", dict(band=fig["year_loss_band"]), ["L53", "L43", "N13"]),
        ("R4", "the full containers in the cold store at its fullest in the 2027 season under the brew plan, over the "
               "five pools", "Component 2", "store_2027", [], "the Monday position, the racking log and the brew plan",
         dict(band=fig["store_2027_band"]), ["N17", "N02", "L37"]),
        ("R5", "each pool's largest weekly shortfall of the 2027 season in the planning case (containers)", "Ask 1",
         "plan", ["R2", "R3", "R4"], "", dict(bands=fig["plan_band"], partly_share=0.5), ["L56", "N17", "L53"]),
        ("R6", "the same in the hot case, the second highest of the ten summers (containers)", "Ask 1", "hot",
         ["R2", "R3", "R4"], "", dict(bands=fig["hot_band"], partly_share=0.5), ["L56", "N17", "L53"]),
        ("R7", "the cover for each pool", "Recommendation", "call", ["R5"], "", {}, ["L56", "N17", "L53"]),
    ]
    res = []
    for rid, name, graded, key, dep, indep, extra, prec in meta:
        r = {"id": rid, "name": name, "graded_as": graded, "figure": key, "depends": dep, "independent": indep,
             "golden": gold[rid], "passes": {"quick": quick[rid], "careful": careful[rid], "thorough": gold[rid]},
             "precedent": prec}
        r.update(extra)
        res.append(r)
    by = {r["id"]: r for r in res}

    def grades(k):
        v = result_values(Rr["lat"][k], Rr["hlat"][k], comps_at(k), acct)
        return {rid: EF.grade(v[rid], by[rid])[0] for rid in by}
    g_lost = {k: grades(k) for k in KEYS}
    nm = {"S1": "a cellar check is of the full containers of a line on the account's order day, so what each checked "
                "line held is rebuilt from the dray's last call and the line's weekly sales before what a line holds "
                "is fitted and carried to the trade's summer peak",
          "S2": "the store's stock is split into its cover and the measured share of a racking run for each beer on sale, and rebuilt "
                "from the 2027 brew plan's runs, range and on-sale dates",
          "S3": "the containers the trade loses are estimated from the share of each purchase lot found on site "
                "against the lot's age, the share on site fitted beside the rate, never taken as nil"}
    judgments = []
    for s in ("S1", "S2", "S3"):
        ak = ALONE[s]
        judgments.append({"id": s, "name": nm[s], "kind": "stump", "precedent": STUMPS[s]["precedents"],
                          "dropped": {"answer": cover_set(Rr["lat"][s]),
                                      "results_moved": [r for r, x in g_lost[s].items() if x != "right"]},
                          "alone": {"answer": cover_set(Rr["lat"][ak]),
                                    "results_rescued": [r for r, x in g_lost[ak].items() if x == "right" and r != "R1"]}})
    judgments += [
        {"id": "J4", "name": "the dockets, the checks, the count and the register cleaned: re-sent docket lines, blank "
                             "container codes, renumbered accounts, three container codings, lot prefixes, a line "
                             "checked twice", "kind": "reflex", "precedent": ["R01", "R13"]},
        {"id": "J5", "name": "deliveries fitted on the season, the trend and the week's temperature, held out and run "
                             "through the recorded summers", "kind": "reflex", "precedent": ["R03", "R04", "R11", "R14"]},
        {"id": "J6", "name": "the estate's new lines sized from the schedule and carried at the fitted relation",
         "kind": "reflex", "precedent": ["R41"]},
        {"id": "J7", "name": "the worst week found over every week of the season, in each case", "kind": "reflex",
         "precedent": ["R06", "R53"]},
        {"id": "J8", "name": "the standard's requirement, fleet, season, cases, float and lines as filed",
         "kind": "reflex", "precedent": []},
        {"id": "J9", "name": "the register, the count and the dockets reconciled to one account by pool, the "
                             "condemnations netted", "kind": "reflex", "precedent": ["R93"]}]
    F = {"golden_answer": fig["call"], "reflex_route": {"answer": cover_set(Rr["lat"][REFLEX])}, "judgments": judgments}
    names = {"S1": "the cellar checks fitted as they stand", "S2": "the store at the same weeks' cover as 2026",
             "S3": "the fleet carried forward with the wash line's condemnations only"}
    routes = [{"name": "the golden", "answer": fig["call"], "golden": True}]
    routes += [{"name": "; ".join(names[s] for s in k.split("+")), "answer": cover_set(Rr["lat"][k])} for k in KEYS]
    routes.append({"name": "the register read as the fleet", "answer": cover_set(X["direct"])})
    routes.append({"name": "the checks regressed as they stand, the store regressed on deliveries, no loss",
                   "answer": cover_set({p: X["rigorous"][p]["short"] for p in POOLS})})
    routes += [{"name": "the %s run route" % k, "answer": cover_set(Rr["runs"][k])} for k in A.RUN]
    fam_rows = [{"name": name, "answer": cover_set({p: Rr["fam"][p][i] for p in POOLS})}
                for i, (name, _) in enumerate(A.FAMILY)]
    forcing = {"kind": "set", "golden_answer": fig["call"], "golden_family": fam_rows,
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": name, "answer": cover_set(v)} for name, v in X["forcing"].items()] +
                                [{"input": "all four fitted inputs %s together, two measured spreads each" % side,
                                  "answer": cover_set(v)} for side, v in X["corners"].items()]}
    hints = [{"sentence": STUMPS[s]["said_out_loud"],
              "rescues": [r for r, x in g_lost[ALONE[s]].items() if x == "right" and r != "R1"]} for s in ("S1", "S2", "S3")]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


def world_figures(WD):
    """the world's own figures, the truth the bands are reported against (never shipped)"""
    import world as WL
    out = {}
    for p in POOLS:
        P = WD.pools[p]
        best, fut = WL.truth(WD, p)
        season = [f for f in fut if f["i"] in WL.C.SEASON]
        out[p] = dict(plan=float(best["short"]), hot=float(WL.truth_hot(WD, p)[0]),
                      rise=float(max(f["cellar"] for f in season) - P.trade[WL.WH]),
                      store=float(max(f["store"] for f in season)),
                      year_loss=float(P.lost_w[WL.WH - 52:].sum()), alive=float(P.alive[WL.WH]))
    return out


def run(target):
    import world as WL
    X = A.run(target)
    fig, Rr = figures(X)
    WD = WL.build(light=True)
    W = world_figures(WD)
    spec = spec_of(X, fig, Rr, {p: W[p]["plan"] for p in POOLS})
    rows, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))
    fig["rubric"] = {"level": level, "fails": [r[0] + ": " + r[2] for r in rows if r[1] == "FAIL"],
                     "warns": [r[0] + ": " + r[2] for r in rows if r[1] == "WARN"],
                     "one_lost": {s: round(earn["earn"][key(s)], 1) for s in ("S1", "S2", "S3")},
                     "fixed_alone": {s: round(earn["earn"][key(ALONE[s])], 1) for s in ("S1", "S2", "S3")},
                     "reflex": round(earn["earn"][key(REFLEX)], 1), "rigorous": round(earn["rigorous"], 1),
                     "runs": {k: round(v, 1) for k, v in (earn.get("runs") or {}).items()}}
    fig["truth"] = {p: int(round(W[p]["plan"])) for p in POOLS}
    fig["truth_hot"] = {p: int(round(W[p]["hot"])) for p in POOLS}
    fig["world"] = {p: {k: int(round(v)) for k, v in W[p].items()} for p in POOLS}
    E, g_lost = effort(X, fig, Rr)
    fig["result_grades"] = g_lost
    X["WD"] = WD
    return X, fig, E, spec


if __name__ == "__main__":
    X, fig, E, spec = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    code = corelib.run(spec)
    for p in POOLS:
        print("%-4s plan %6d %-16s hot %6d %-16s week %s cover %-8s truth %6d hot truth %6d" % (
            p, fig["plan"][p], fig["plan_band"][p], fig["hot"][p], fig["hot_band"][p], fig["plan_week"][p],
            fig["cover"][p], fig["truth"][p], fig["truth_hot"][p]))
    for cid, f, key in COMPS:
        print("%s %6d %s  world %d" % (cid, fig[key], fig[key + "_band"],
                                      sum(fig["world"][p][{"C1": "rise", "C2": "store", "C3": "year_loss"}[cid]]
                                          for p in POOLS)))
    print("falsification", fig["falsification"], "rubric", fig["rubric"]["one_lost"], fig["rubric"]["reflex"])
    for x in fig["perturbations"]:
        print("%-62s %s %s" % (x["input"][:62], "same call" if x["call_holds"] else "CALL MOVES", x["plan"]))
    sys.exit(code)
