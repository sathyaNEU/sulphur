"""Every owed figure, computed on the shipped files: figures.json (what the answer blocks and the goldens state)
and effort.json (each result's golden, band and the three passes, the stump factorial, the forcing on both sides),
with the core's spec rebuilt on the cut pack and re-priced by corelib."""
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
UNTAGGED = tuple(p for p in POOLS if p != A.TAGGED)
KEYS = ["S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"]
REFLEX = "S1+S2+S3"
ALONE = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
LOST = {"S1": "the containers off site at the count moved in step with deliveries",
        "S2": "the store's weeks of cover in the same weeks of 2026 carried to 2027's deliveries",
        "S3": "the tracked kegs' loss per keg delivered carried to every container type"}
ROUTE_NAME = {k: "; ".join(LOST[s] for s in k.split("+")) for k in KEYS}
COVER = {"nothing": "no cover", "hire": "seasonal hire", "buy": "purchase"}
STUMPS = {
    "S1": dict(axis="unit", opens="K50", steps_left=4, precedents=["N01", "L15", "L40"],
               said_out_loud="A cellar holds a number of containers for each line whatever it sells, plus cover for "
                             "its delivery interval, so the trade's stock does not move in step with its sales."),
    "S2": dict(axis="when", opens="K20", steps_left=3, precedents=["N17", "N02", "L37"],
               said_out_loud="The store receives each beer a whole racking run at a time, so its stock follows the "
                             "runs and the number of beers on sale, and both change in 2027."),
    "S3": dict(axis="who", opens="FIR", steps_left=4, precedents=["N08", "N12", "L53"],
               said_out_loud="The register never loses a container, and the only pool whose losses are seen is the "
                             "tracked one, which loses far fewer."),
}
ROOM = 0.10                  # a band: the battery's range (every convention alone and every two together) and a
ROOM_MIN = {"pool": 15.0, "component": 25.0}    # tenth of its width as room on each side, 15 or 25 containers at least


def band_of(g, fam, kind="pool"):
    lo, hi = min(list(fam) + [g]), max(list(fam) + [g])
    room = max(ROOM * (hi - lo), ROOM_MIN[kind])
    return [int(math.floor(lo - room)), int(math.ceil(hi + room))]


def call_of(v):
    return ["%s: %s" % (A.PLURAL[p], COVER[A.cover_of(v[p], p)]) for p in POOLS]


def total(X, key, field, pools=POOLS, idx=None):
    if idx is not None:
        return float(sum(X["fam"][p][idx][field] for p in pools))
    src = X["gold"] if key is None else X["rigorous"] if key == "rigorous" else None
    if src is not None:
        return float(sum(src[p][field] for p in pools))
    return float(sum(X["lat"][p][key][field] for p in pools))


def figures(X):
    R = X["R"]
    n = len(A.FAMILY)
    gold = {p: X["gold"][p]["short"] for p in POOLS}
    hot = {p: X["hot"][p][0] for p in POOLS}
    fam = {p: [x["short"] for x in X["fam"][p]] for p in POOLS}
    lat = {k: {p: X["lat"][p][k]["short"] for p in POOLS} for k in KEYS}
    hlat = {k: {p: X["hot_lat"][p][k] for p in POOLS} for k in KEYS}
    comp = {"C1": ("swing", POOLS), "C2": ("store", POOLS), "C3": ("year_loss", UNTAGGED)}
    cg = {c: total(X, None, f, ps) for c, (f, ps) in comp.items()}
    cfam = {c: [total(X, None, f, ps, i) for i in range(n)] for c, (f, ps) in comp.items()}
    clat = {c: {k: total(X, k, f, ps) for k in KEYS} for c, (f, ps) in comp.items()}
    crig = {c: total(X, "rigorous", f, ps) for c, (f, ps) in comp.items()}
    last, cnt = R.counts[-1], R.counts
    iso = lambda d: d.isoformat()
    fig = {"call": call_of(gold), "cover": {p: A.cover_of(gold[p], p) for p in POOLS},
           "plan": {p: int(round(gold[p])) for p in POOLS}, "plan_band": {p: band_of(gold[p], fam[p]) for p in POOLS},
           "plan_week": {p: iso(X["gold"][p]["date"]) for p in POOLS},
           "hot": {p: int(round(hot[p])) for p in POOLS},
           "hot_band": {p: band_of(hot[p], X["hot_fam"][p]) for p in POOLS},
           "trade_rise": int(round(cg["C1"])), "trade_rise_band": band_of(cg["C1"], cfam["C1"], "component"),
           "store_2027": int(round(cg["C2"])), "store_2027_band": band_of(cg["C2"], cfam["C2"], "component"),
           "year_loss": int(round(cg["C3"])), "year_loss_band": band_of(cg["C3"], cfam["C3"], "component"),
           "trade_rise_by_pool": {p: int(round(X["gold"][p]["swing"])) for p in POOLS},
           "store_by_pool": {p: int(round(X["gold"][p]["store"])) for p in POOLS},
           "year_loss_by_pool": {p: int(round(X["gold"][p]["year_loss"])) for p in POOLS},
           "min_run": dict(A.MIN_RUN), "names": dict(A.NAMES), "plural": dict(A.PLURAL)}
    fig["off_site"] = {p: int(round(X["gold"][p]["X"][last])) for p in POOLS}
    fig["account"] = {p: {iso(R.week_dates[b]): dict(register=int(R.register[p][b]), on_site=int(R.takes[b][p]["onsite"]),
                                                    off_site=int(R.register[p][b] - R.takes[b][p]["onsite"]),
                                                    store=int(R.takes[b][p]["store"]), depots_wash_repair=int(R.takes[b][p]["other"]),
                                                    clean_empty=int(R.takes[b][p]["idle"])) for b in cnt} for p in POOLS}
    fig["deliveries"] = {p: {"total": int(R.flow[p].sum()), "last_year": int(R.flow[p][last - 52:last].sum()),
                             "year_before": int(R.flow[p][last - 104:last - 52].sum()),
                             "first_year": int(R.flow[p][:52].sum())} for p in POOLS}
    par = {}
    for p in POOLS:
        g = X["gold"][p]
        pk = g["pick"]
        par[p] = dict(fixed_per_line=round(g["a"], 2), per_sale_weekly=round(g["slope1"], 2), per_sale_twice=round(g["slope_half"], 2),
                      per_sale_pool=round(g["bm"], 3), audit_counts=int(g["n_counts"]), lines=int(len(R.line[p])),
                      store_cover_weeks=round(g["cov"], 3), half_runs_2026=int(round(g["half26"])),
                      beers_2026=len(R.runs[p]), beers_at_week=int(pk["beers"]), other_weeks=round(g["c2"], 3),
                      loss_pct=round(100.0 * g["lam"], 2), account_loss_pct=round(100.0 * g["lam_acc"], 2),
                      tag_loss_pct=round(100.0 * g["lam_tag"], 2), condemned_pct=round(100.0 * g["scr"], 3),
                      condemned_last_year=int(R.condemned_year[p]), bend_c=round(g["hinge"], 1),
                      level_at_count=int(round(g["lev"][last])), level_year_before=int(round(g["lev"][cnt[-2]])),
                      off_site_gain=int(round(g["X"][last] - g["X"][cnt[-2]])), trade_change=int(round(g["gone"] - (g["X"][last] - g["X"][cnt[-2]]))) * -1,
                      deliveries_at_week=int(round(pk["D"])), estate_at_week=int(round(pk["es"])), estate_cellars=int(round(pk["est"])),
                      swing=int(round(pk["swing"])), store=int(round(pk["store"])), other=int(round(pk["other"])),
                      float=int(round(pk["float"])), drain=int(round(pk["drain"])), on_site=int(g["onsite"]),
                      temp_at_week=round(pk["temp"], 1))
    fig["pool"] = par
    fig["estate"] = dict(pubs=R.estate_pubs, lines={p: int(sum(n for _, n in R.estate[p])) for p in POOLS},
                         volume={p: R.estate_volume[p] for p in POOLS})
    t = X["gold"][A.TAGGED]
    fig["tags"] = dict(not_traced=int(t["n_tag"]), window=[iso(R.week_dates[t["tag_window"][0]]), iso(R.week_dates[t["tag_window"][1]])],
                       delivered=int(R.flow[A.TAGGED][t["tag_window"][0]:t["tag_window"][1]].sum()),
                       loss_pct=round(100.0 * t["lam_tag"], 2), reads=int(R.tag_reads), double_reads=int(R.double_reads),
                       read_share_pct=round(100.0 * R.read_share, 1), cases=int(R.cases), not_traced_all=int(R.not_traced),
                       response=round(A.tracked_response(R, A.GOLDEN), 3))
    fig["season"] = [iso(R.week_dates[X["season"][0]]), iso(R.week_dates[X["season"][-1]])]
    fig["summers"] = {p: {str(y): int(round(A.chain(R, p, None, A.summer_temps(R, y))["short"])) for y in A.SUMMERS} for p in POOLS}
    fig["hot_year"] = {p: int(sorted(fig["summers"][p], key=lambda y: fig["summers"][p][y])[A.HOT_RANK]) for p in POOLS}
    routes = {"golden": (gold, hot), "direct": (X["direct"], X["hot_direct"]),
              "rigorous": ({p: X["rigorous"][p]["short"] for p in POOLS}, X["hot_rigorous"])}
    routes.update({k: (lat[k], hlat[k]) for k in KEYS})
    fig["routes"] = {k: {p: {"plan": int(round(v[p])), "hot": int(round(h[p])), "cover": A.cover_of(v[p], p)} for p in POOLS}
                     for k, (v, h) in routes.items()}
    fig["route_calls"] = {k: call_of(v) for k, (v, h) in routes.items()}
    fig["route_components"] = {k: {c: int(round(clat[c][k])) for c in comp} for k in KEYS}
    fig["route_components"]["rigorous"] = {c: int(round(crig[c])) for c in comp}
    fig["distinct_wrong_calls"] = len({tuple(call_of(lat[k])) for k in KEYS})
    fig["variants"] = n
    fig["singles"] = len(A.SINGLES)
    fig["refused"] = {name: {p: int(round(v[p])) for p in POOLS} for name, v in X["refused"].items()}
    fig["refused_hot"] = {name: {p: int(round(v[p])) for p in POOLS} for name, v in X["refused_hot"].items()}
    fig["refused_cover"] = {name: {p: A.cover_of(v[p], p) for p in POOLS} for name, v in X["refused"].items()}
    fig["tests"] = {p: {"bend_F": round(X["tests"][p]["bend_F"], 1), "harmonic_F": round(X["tests"][p]["harmonic_F"], 1),
                        "df": int(X["tests"][p]["df"]), "trend_t": round(X["tests"][p]["trend_t"], 1),
                        "trend_pct": round(X["tests"][p]["trend_pct"], 1), "quad_sse_pct": round(X["tests"][p]["quad_sse_pct"], 1),
                        "flat_sse_pct": round(X["tests"][p]["flat_sse_pct"], 1)} for p in POOLS}
    fig["tests"]["f_crit"], fig["tests"]["t_crit"], fig["tests"]["level_pct"] = A.F_CRIT, A.T_CRIT, 5
    fig["rebuilds"] = len(A.FAMILY) - 1
    fig["off_site_gain_untagged"] = int(sum(fig["pool"][p]["off_site_gain"] for p in UNTAGGED))
    fig["split"] = {p: dict(zip(("fixed_104", "se_104", "fixed_52", "se_52"),
                                [int(round(v)) for v in A.split_fit(R, p, 104) + A.split_fit(R, p, 52)])) for p in POOLS}
    for p in POOLS:
        fig["split"][p]["half_runs"] = int(round(X["gold"][p]["half26"]))
        fig["split"][p]["within_se"] = round(abs(fig["split"][p]["fixed_104"] - X["gold"][p]["half26"]) / fig["split"][p]["se_104"], 2)
        for cw, (fx, se) in X["split_windows"][p].items():
            fig["split"][p]["fixed_%d" % cw], fig["split"][p]["se_%d" % cw] = int(round(fx)), int(round(se))
            fig["split"][p]["errors_%d" % cw] = round(abs(fx - X["gold"][p]["half26"]) / se, 2)
        fig["split"][p]["cover_by_year"] = [round(v, 3) for v in X["cover_by_year"][p]]
    fig["first_count"] = {p: dict(off_site=int(round(v["off_site"])), relation=int(round(v["relation"])), lines=v["lines"],
                                  gap_pct=round(100.0 * (v["off_site"] / v["relation"] - 1.0), 1))
                          for p, v in X["first_count"].items()}
    fig["family_calls_all_golden"] = all(call_of({p: fam[p][i] for p in POOLS}) == fig["call"] for i in range(n))
    fig["variant_range"] = {p: [int(round(min(fam[p]))), int(round(max(fam[p])))] for p in POOLS}
    fig["variant_range_hot"] = {p: [int(round(min(X["hot_fam"][p]))), int(round(max(X["hot_fam"][p])))] for p in POOLS}
    fig["variant_names"] = [name for name, _ in A.FAMILY]
    fig["variant_plan"] = {p: [int(round(x)) for x in fam[p]] for p in POOLS}
    lines_of = lambda p: (0.0, float(A.MIN_RUN[p]))
    near = min((min(abs(fam[p][i] - l) for l in lines_of(p)), p, A.FAMILY[i][0]) for p in POOLS for i in range(n))
    fig["nearest_variant"] = {"distance": int(round(near[0])), "pool": near[1], "variant": near[2]}
    fig["perturbations"] = [{"input": name, "call_holds": call_of(v) == fig["call"], "plan": {p: int(round(v[p])) for p in POOLS}}
                            for name, v in X["forcing"].items()]
    fig["perturbations"] += [{"input": "all four fitted inputs %s together, two measured spreads each" % side,
                              "call_holds": call_of(v) == fig["call"], "plan": {p: int(round(v[p])) for p in POOLS}}
                             for side, v in X["corners"].items()]
    fig["spreads_pct"] = {p: {k: round(100.0 * v, 1) for k, v in X["spreads"][p].items()} for p in POOLS}
    r = X["referee"]
    fig["referee"] = dict(week=iso(r["date"]), seen=int(round(r["seen"])), golden=int(round(r["golden"])),
                          proportional=int(round(r["proportional"])), start=int(round(r["start"])), top=int(round(r["top"])),
                          level=int(round(r["level"])), at=int(round(r["at"])))
    mid = r["week"]
    fig["referee"]["weeks"] = [iso(R.week_dates[mid - 1]), iso(R.week_dates[mid]), iso(R.week_dates[mid + 1])]
    fig["referee"]["mondays"] = [iso(R.week_dates[mid]), iso(R.week_dates[mid + 1]), iso(R.week_dates[mid + 2])]
    fig["referee"]["counted_on"] = iso(R.week_dates[R.counts[-2]])
    tr = X["tag_rules"]
    fig["tags"].update(deliver_reads=int(R.deliver_reads), docket_deliveries=int(R.flow[A.TAGGED].sum()),
                       rise_lost_in=int(round(tr["lost_in"])), rise_unscaled=int(round(tr["unscaled"])),
                       per_container=round(tr["response"], 2), share_pct=int(round(100.0 * tr["share"])),
                       line_pct=int(round(100.0 * tr["line"])),
                       fill=[[iso(d), int(round(v))] for d, v in X["tag_fill"]])
    pr = X["pairing"]
    fig["pairing"] = {p: dict(fixed_ended=int(round(pr[p]["ended"][0])), se_ended=int(round(pr[p]["ended"][1])),
                              r2_ended=round(pr[p]["ended"][2], 2), fixed_beginning=int(round(pr[p]["beginning"][0])),
                              se_beginning=int(round(pr[p]["beginning"][1])), r2_beginning=round(pr[p]["beginning"][2], 2))
                      for p in POOLS}
    fig["apart"] = {p: {k: {kk: round(v, 2) for kk, v in x.items()} for k, x in X["apart"][p].items()} for p in POOLS}
    ow = X["own"]
    fig["own_dockets"] = dict(per_sale={str(w): {p: round(v, 2) for p, v in ow["per_sale"][w].items()} for w in ow["per_sale"]},
                              rise={str(w): int(round(v)) for w, v in ow["rise"].items()})
    fig["wash_log"] = {p: {k: ([int(round(x)) for x in v] if isinstance(v, list) else int(round(v))) for k, v in X["washlog"][p].items()}
                       for p in POOLS}
    fig["at_customers_tag_rate"] = {p: int(round(X["lat"][p][REFLEX]["alive_out"])) for p in POOLS}
    lv = X["levels"]
    fig["levels"] = {p: dict(fit=int(round(lv[p]["fit"])), week_before=int(round(lv[p]["w1"])), four_weeks=int(round(lv[p]["w4"])),
                             eight_weeks=int(round(lv[p]["w8"])), thirteen_weeks=int(round(lv[p]["w13"])),
                             eight_over_fit_pct=round(100.0 * (lv[p]["w8"] / lv[p]["fit"] - 1.0), 1),
                             thirteen_over_fit_pct=round(100.0 * (lv[p]["w13"] / lv[p]["fit"] - 1.0), 1),
                             weekly_scatter_pct=round(100.0 * lv[p]["scatter"], 1),
                             plan_one_week=int(round(lv[p]["short1"])), plan_two_weeks=int(round(lv[p]["short2"])),
                             plan_eight_weeks=int(round(lv[p]["short8"])), plan_thirteen_weeks=int(round(lv[p]["short13"])),
                             cover_eight=A.cover_of(lv[p]["short8"], p), cover_thirteen=A.cover_of(lv[p]["short13"], p),
                             cover_one=A.cover_of(lv[p]["short1"], p), cover_two=A.cover_of(lv[p]["short2"], p)) for p in POOLS}
    fig["counts"] = dict(docket_rows=int(R.docket_rows), resent_rows=int(R.resent_rows), delivery_lines=int(R.del_rows),
                         blank_codes=int(R.blank_codes), dockets=int(R.dockets), accounts=int(R.n_accounts),
                         renumbered=int(R.renumbered), register_rows=int(R.register_rows), rackings=int(R.rackings),
                         audit_rows=int(R.audit_rows), audit_visits=int(R.audit_visits), weeks=int(R.WH),
                         first_week=iso(R.D0), count_dates=[iso(R.week_dates[b]) for b in cnt], summers=[A.SUMMERS[0], A.SUMMERS[-1]],
                         season_weeks=A.SEASON_WEEKS, pools=len(POOLS))
    fig["stated"] = dict(float_sevenths=2, hot_rank=2, summers=10, season_weeks=21, fs04=["2.1", "2.2", "2.3", "3.1", "3.2", "3.3", "3.4", "4.1", "4.2"],
                         issue=3, quotation="Q26-1187", bend_grid=[12, 22, 0.5], intervals=[1, 0.5], year_weeks=[52, 104, 156],
                         forcing_pct=[20, 5], spreads=2)
    fig["tests"]["tag_reads_window"] = 120
    path = {}
    for p in POOLS:
        g = X["gold"][p]
        rows = []
        for x in g["path"]:
            parts = dict(at_customers=int(round(g["alive_out"] + x["swing"])), store=int(round(x["store"])),
                         other=int(round(x["other"])), float=int(round(x["float"])))
            req, short = sum(parts.values()), int(round(x["short"]))
            rows.append(dict(week=iso(x["date"]), in_season=bool(x["i"] in X["season"]), deliveries=int(round(x["D"])),
                             requirement=req, fleet=req - short, shortfall=short, **parts))
        path[p] = rows
    fig["path"] = path
    fig["beers"] = {p: [dict(sku=s, first=iso(a), last=iso(b), run=int(run),
                             on_sale_at_week=bool(a <= X["gold"][p]["date"] <= b)) for s, a, b, run in R.plan[p]] for p in POOLS}
    fig["runs_2026"] = {p: {s: int(round(v)) for s, v in sorted(R.runs[p].items())} for p in POOLS}
    fig["half_runs_at_week"] = {p: int(round(sum(b["run"] for b in fig["beers"][p] if b["on_sale_at_week"]) / 2.0)) for p in POOLS}
    WHn = R.WH
    fig["store_weeks"] = {p: round(float(R.store[p][WHn - 103:WHn + 1].mean() / R.flow[p][WHn - 104:].mean()), 2) for p in POOLS}
    fig["store_weeks_at_week"] = {p: round(X["gold"][p]["pick"]["store"] / X["gold"][p]["pick"]["D"], 2) for p in POOLS}
    fig["response_pct"] = {p: round(100.0 * X["gold"][p]["bm"] * X["gold"][p]["lev"][last] / X["gold"][p]["alive_out"], 0) for p in POOLS}
    fig["at_customers_count"] = {p: int(round(X["gold"][p]["alive_out"])) for p in POOLS}
    fig["tag_rate_loss_year"] = {p: int(round(X["lat"][p]["S3"]["year_loss"])) for p in POOLS}
    fig["store_cover_route"] = {p: int(round(X["lat"][p]["S2"]["store"])) for p in POOLS}
    fig["swing_prop_route"] = {p: int(round(X["lat"][p]["S1"]["swing"])) for p in POOLS}
    fig["loss_tag_route"] = {p: int(round(X["lat"][p]["S3"]["year_loss"])) for p in POOLS}
    Rr = dict(gold=gold, hot=hot, fam=fam, lat=lat, hlat=hlat, cg=cg, cfam=cfam, clat=clat, crig=crig)
    return fig, Rr


def spec_of(X, fig, Rr, truth):
    """the core's spec rebuilt on the cut pack, each figure with the band the answer blocks state"""
    members = {p: dict(lines=[0.0, float(A.MIN_RUN[p])], truth=float(truth[p]), golden=float(Rr["gold"][p]),
                       family=[float(x) for x in Rr["fam"][p]],
                       routes=dict(direct=float(X["direct"][p]), rigorous=float(X["rigorous"][p]["short"]))) for p in POOLS}
    figs = []
    for c, key in (("C1", "trade_rise"), ("C2", "store_2027"), ("C3", "year_loss")):
        figs.append(dict(id=c, block="component", golden=float(Rr["cg"][c]), family=[float(x) for x in Rr["cfam"][c]],
                         band=fig[key + "_band"], lattice={k: float(Rr["clat"][c][k]) for k in KEYS},
                         routes=dict(rigorous=float(Rr["crig"][c]))))
    for p in POOLS:
        figs.append(dict(id="plan " + p, block="ask", member=p, band=fig["plan_band"][p]))
    for p in POOLS:
        figs.append(dict(id="hot " + p, block="ask", golden=float(Rr["hot"][p]), family=[float(x) for x in X["hot_fam"][p]],
                         band=fig["hot_band"][p], lattice={k: float(Rr["hlat"][k][p]) for k in KEYS},
                         routes=dict(rigorous=float(X["hot_rigorous"][p]))))
    r = X["referee"]
    ref = dict(slice="the tracked 20 litre kegs in the trade, from the December 2025 count to the busiest three weeks of "
                     "summer 2026, which the tags count and no 2027 week or other container type shares",
               covers_target=False, truth=float(r["seen"]), golden=float(r["golden"]),
               rivals={"the trade's stock moved in step with deliveries": float(r["proportional"])})
    return dict(task="task4 architecture 14, cut pack", call="lines", members=members, stumps=STUMPS,
                lattice={k: {p: float(Rr["lat"][k][p]) for p in POOLS} for k in KEYS}, referee=ref, figures=figs)


def result_values(plan, hot, comps, off_site):
    r = lambda d: {p: int(round(d[p])) for p in POOLS}
    return {"R1": off_site, "R2": int(round(comps["C1"])), "R3": int(round(comps["C3"])), "R4": int(round(comps["C2"])),
            "R5": r(plan), "R6": r(hot), "R7": call_of(plan)}


def effort(X, fig, Rr):
    comps_at = lambda k: {c: Rr["clat"][c][k] for c in ("C1", "C2", "C3")}
    gold = result_values(Rr["gold"], Rr["hot"], Rr["cg"], fig["off_site"])
    quick = result_values(X["direct"], X["hot_direct"], {"C1": 0, "C2": 0, "C3": 0}, None)
    quick.update({"R1": None, "R2": None, "R3": None, "R4": None})
    careful = result_values(Rr["lat"][REFLEX], Rr["hlat"][REFLEX], comps_at(REFLEX), fig["off_site"])
    meta = [
        ("R1", "each container type's stock account at the four counts: on the register, counted on site, off site",
         "Step-by-Step", "off_site", [], "", {}, []),
        ("R2", "the rise in the trade's stock from the 30 November 2026 count to each type's worst week, the new estate's "
               "cellars included, over the five types (containers)", "Component 1", "trade_rise", [],
         "the cellar audits, the dockets, the route plan and the supply agreement's schedule",
         dict(band=fig["trade_rise_band"]), ["N01", "L15", "L40"]),
        ("R3", "the containers the trade lost in the year to 30 November 2026 on the four types without tags",
         "Component 3", "year_loss", [], "the counts, the register and the dockets", dict(band=fig["year_loss_band"]),
         ["N08", "N12", "L53"]),
        ("R4", "the full containers in the cold store in each type's worst week under the 2027 brew plan, over the five "
               "types", "Component 2", "store_2027", [], "the Monday position, the racking log and the brew plan",
         dict(band=fig["store_2027_band"]), ["N17", "N02", "L37"]),
        ("R5", "each type's largest weekly shortfall of the 2027 season in the planning case (containers)", "Asks 1 to 5",
         "plan", ["R2", "R3", "R4"], "", dict(bands=fig["plan_band"], partly_share=0.5), ["N01", "N17", "N08"]),
        ("R6", "the same in the hot case, the second highest of the ten summers (containers)", "Asks 6 to 10", "hot",
         ["R2", "R3", "R4"], "", dict(bands=fig["hot_band"], partly_share=0.5), ["N01", "N17", "N08"]),
        ("R7", "the cover for each container type", "Recommendation", "call", ["R5"], "", {}, ["N01", "N17", "N08"]),
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
        v = result_values(Rr["lat"][k], Rr["hlat"][k], comps_at(k), fig["off_site"])
        return {rid: EF.grade(v[rid], by[rid])[0] for rid in by}
    g_lost = {k: grades(k) for k in KEYS}
    nm = {"S1": "what a cellar holds is fitted line by line on the reps' counts (a number per line and a number per "
                "container sold a week by delivery interval), and the trade's stock is moved by that, not in step with "
                "deliveries",
          "S2": "the store's stock is split into its cover and half a racking run for each beer on sale, and rebuilt "
                "from the 2027 brew plan's runs and range",
          "S3": "the containers lost where nothing is tracked are read from the stock account (the register less the "
                "count, net of the trade's own change), not from the tracked kegs"}
    judgments = []
    for s in ("S1", "S2", "S3"):
        ak = ALONE[s]
        judgments.append({"id": s, "name": nm[s], "kind": "stump", "precedent": STUMPS[s]["precedents"],
                          "dropped": {"answer": call_of(Rr["lat"][s]), "results_moved": [r for r, x in g_lost[s].items() if x != "right"]},
                          "alone": {"answer": call_of(Rr["lat"][ak]),
                                    "results_rescued": [r for r, x in g_lost[ak].items() if x == "right" and r != "R1"]}})
    judgments += [
        {"id": "J4", "name": "the dockets on one footing: a re-sent docket counted once, a blank container code read from "
                             "the product, a renumbered account under its current number, three codings to one",
         "kind": "reflex", "precedent": ["R01"]},
        {"id": "J5", "name": "the stock account: the register's containers at each count less the count on site",
         "kind": "reflex", "precedent": ["R93"]},
        {"id": "J6", "name": "weekly deliveries fitted on the season, the trend and the week's temperature, checked on a "
                             "held-out year", "kind": "reflex", "precedent": ["R03"]},
        {"id": "J7", "name": "the requirement, the fleet, the float, the season, the two cases and the cover lines as the "
                             "fleet standard and the quotation file them", "kind": "reflex", "precedent": []},
        {"id": "J8", "name": "the new estate's lines and volumes read from the supply agreement and added from their "
                             "listing dates", "kind": "reflex", "precedent": []},
        {"id": "J9", "name": "the season run on each of the ten recorded summers and the second highest taken",
         "kind": "reflex", "precedent": ["R53"]},
        {"id": "J10", "name": "a bootstrap of the fitted inputs and a sensitivity grid on nearby choices",
         "kind": "reflex", "precedent": ["R04"]}]
    F = {"golden_answer": fig["call"], "reflex_route": {"answer": call_of(Rr["lat"][REFLEX])}, "judgments": judgments}
    routes = [{"name": "the golden", "answer": fig["call"], "golden": True}]
    routes += [{"name": ROUTE_NAME[k], "answer": call_of(Rr["lat"][k])} for k in KEYS]
    routes.append({"name": "the register read as the fleet and moved with the busiest week's deliveries over the year's",
                   "answer": call_of(X["direct"])})
    routes.append({"name": "the trade's stock moved by the tracked kegs' own measured response, the store regressed on "
                           "deliveries and the tracked kegs' loss carried to every type",
                   "answer": call_of({p: X["rigorous"][p]["short"] for p in POOLS})})
    fam_rows = [{"name": name, "answer": call_of({p: Rr["fam"][p][i] for p in POOLS})} for i, (name, _) in enumerate(A.FAMILY)]
    forcing = {"kind": "set", "golden_answer": fig["call"], "golden_family": fam_rows,
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": name, "answer": call_of(v)} for name, v in X["forcing"].items()] +
                                [{"input": "all four fitted inputs %s together, two measured spreads each" % side,
                                  "answer": call_of(v)} for side, v in X["corners"].items()]}
    hints = [{"sentence": STUMPS[s]["said_out_loud"],
              "rescues": [r for r, x in g_lost[ALONE[s]].items() if x == "right" and r != "R1"]} for s in ("S1", "S2", "S3")]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


def run(target):
    import world as WL
    X = A.run(target)
    fig, Rr = figures(X)
    WD = WL.build(light=True)
    truth = {p: WL.truth(WD, p)[0]["short"] for p in POOLS}
    truth_hot = {p: WL.truth_hot(WD, p)[0] for p in POOLS}
    spec = spec_of(X, fig, Rr, truth)
    rows, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))
    fig["rubric"] = {"level": level, "fails": [r[0] + ": " + r[2] for r in rows if r[1] == "FAIL"],
                     "one_lost": {s: round(earn["earn"][key(s)], 1) for s in ("S1", "S2", "S3")},
                     "fixed_alone": {s: round(earn["earn"][key(ALONE[s])], 1) for s in ("S1", "S2", "S3")},
                     "reflex": round(earn["earn"][key(REFLEX)], 1), "rigorous": round(earn["rigorous"], 1)}
    fig["truth"] = {p: int(round(truth[p])) for p in POOLS}
    fig["truth_hot"] = {p: int(round(truth_hot[p])) for p in POOLS}
    E, g_lost = effort(X, fig, Rr)
    fig["result_grades"] = g_lost
    X["WD"] = WD
    return X, fig, E, spec


if __name__ == "__main__":
    import json
    X, fig, E, spec = run(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target"))
    code = corelib.run(spec)
    print(json.dumps({k: fig[k] for k in ("call", "rubric", "nearest_variant", "result_grades", "referee", "truth", "truth_hot")}, default=float))
    for p in POOLS:
        print("%-4s plan %6d %-16s hot %6d %-16s week %s cover %s (hot year %d)" % (
            p, fig["plan"][p], fig["plan_band"][p], fig["hot"][p], fig["hot_band"][p], fig["plan_week"][p], fig["cover"][p], fig["hot_year"][p]))
    print("C1", fig["trade_rise"], fig["trade_rise_band"], "C2", fig["store_2027"], fig["store_2027_band"], "C3", fig["year_loss"], fig["year_loss_band"])
    for x in fig["perturbations"]:
        print("%-62s %s %s" % (x["input"][:62], "same call" if x["call_holds"] else "CALL MOVES", x["plan"]))
    sys.exit(code)
