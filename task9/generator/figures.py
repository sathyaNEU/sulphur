"""task9: every figure the answer blocks and the golden files state, written once from the analysis.

figures.json is this object. The blocks, the memo, the workbook and effort.json are all drafted from it, so a figure
shared by two of them agrees to the same rounding.
"""
import math

import analysis as AN
import params as P
import swaps as SW

K = 1000
GOLD_E = "start dates replayed, ratio to implied (the golden)"
GOLD_R = "start dates replayed jointly, ratio to implied (the golden)"
GOLD_P = "every settlement from the same start dates (the golden)"
MARK_E = "the mark (implied variance for the remaining term)"
OWN = "its index's own history"
PROXY = AN.CAREFUL_PROXY


def r1000(x):
    return int(round(x / K) * K)


def fl(x, unit):
    return int(math.floor(x / unit + 1e-9) * unit)


def ce(x, unit):
    return int(math.ceil(x / unit - 1e-9) * unit)


def ladder_cells(f):
    """A ladder's record per USD 100,000 a point, as the blocks state it."""
    return dict(avg_per_sale_usd=r1000(f["avg_per_sale"] * P.PER), worst_year=int(f["worst_year"]), worst_year_loss_usd=r1000(-f["worst"] * P.PER))


def range_cells(pair, scale):
    return dict(low_usd=r1000(pair[0] * scale), high_usd=r1000(pair[1] * scale))


def range_bands(pairs, scale, unit, pad=0.0):
    lows, highs = [p[0] * scale for p in pairs], [p[1] * scale for p in pairs]
    return dict(low_usd=[fl(min(lows) - pad * abs(min(lows)), unit), ce(max(lows) + pad * abs(max(lows)), unit)],
                high_usd=[fl(min(highs) - pad * abs(min(highs)), unit), ce(max(highs) + pad * abs(max(highs)), unit)])


def vols(ob):
    return {s.strftime("%Y-%m"): round(float(v), 2) for s, v in zip(ob.sale, ob.acc_vol)}


def plan_cells(open_usd, unsold_usd, new_usd, rng):
    """The plan by ladder: every figure the sum of the rounded parts it is stated with."""
    twelve = open_usd + unsold_usd
    return dict(twelve_month_usd=twelve, three_month_usd=new_usd, total_usd=twelve + new_usd, low_usd=r1000(rng[0]), high_usd=r1000(rng[1]))


def make(A, R):
    F = {}
    F["as_of"] = str(P.REVIEW.date())
    F["statement_date"] = str(P.STATEMENT.date())
    F["policy"] = dict(reference_assets_usd=int(P.REF_ASSETS), reference_assets_usd_m=P.REF_ASSETS / 1e6, settlement_limit_pct=P.LIM_SETTLE_PCT,
                       collateral_limit_pct=P.LIM_COLL_PCT, settlement_limit_usd=int(P.LIM_SETTLE), collateral_limit_usd=int(P.LIM_COLL),
                       cap_multiple=SW.CAP, standing_size_usd=P.OLD_SIZE, confirmation_vega_usd=P.OLD_CONF_VEGA, quoted_size_usd=P.PROPOSED,
                       per_usd=P.PER, size_step_usd=P.SIZE_STEP, hot_level=P.HOT, record_from="2007-01-01")
    # ---------------- the book at the review close (workbook content; not graded)
    ob = R["open"]
    F["open_vols"] = vols(ob)
    F["statement_vols"] = {k[:7]: round(v, 2) for k, v in R["statement_acc"].items()}
    F["open_swaps"] = [dict(sale=str(s.sale.date()), expiry=str(s.expiry.date()), strike=round(float(s.k), 2), days_elapsed=int(s.n_e),
                            days_remaining=int(s.n_r), realized_vol=round(float(s.acc_vol), 2), implied_vol=round(float(s.iv), 2),
                            value_usd=int(round(s.mark * P.OLD_SIZE))) for s in ob.itertuples()]
    live = A.book.trades[~A.book.trades.settled]
    F["open_sale_months"] = int(len(ob))
    F["open_confirmations"] = int(len(live))
    F["confirmations"] = dict(total=int(len(A.book.trades)), settled=int(A.book.trades.settled.sum()), blotter_rows=int(len(A.book.trades) + len(A.book.dead)),
                              valuation_rows=int(len(A.book.val)))
    import pandas as pd
    F["blotter"] = dict(amended_wrong_vega_usd=int(P.AMENDED[3]), amended_month=pd.Timestamp(P.AMENDED[0], P.AMENDED[1], 1).strftime("%B %Y"),
                        novated_month=pd.Timestamp(P.NOVATED[0], P.NOVATED[1], 1).strftime("%B %Y"), novation_month=P.NOVATED[4].strftime("%B %Y"),
                        novation_date=str(P.NOVATED[4].date()))
    F["book_value_usd"] = r1000(R["book_value"]["total variance (the golden)"])
    F["book_value_rivals"] = {k: r1000(v) for k, v in R["book_value"].items()}
    F["book_value_hurried"] = {k: r1000(v) for k, v in R["book_value_hurried"].items()}
    # ---------------- R1 and R2: the new ladder on the record
    lad, riv, lh = R["ladder"][P.NEW_MAT], R["ladder_rivals"], R["ladder_hurried"]
    avg = [v["avg_per_sale"] * P.PER for v in riv.values()]
    worst = [-v["worst"] * P.PER for v in riv.values()]
    cells = ladder_cells(lad)
    F["R1_avg_3m_usd"] = cells["avg_per_sale_usd"]
    F["R1_band"] = [fl(min(avg), K), ce(max(avg), K)]
    F["R1_partly"] = [fl(min(avg) * 0.98, K), ce(max(avg) * 1.02, K)]
    F["R2_worst_year_loss_usd"] = cells["worst_year_loss_usd"]
    F["R2_worst_year"] = cells["worst_year"]
    F["R2_band"] = [fl(min(worst), 10 * K), ce(max(worst), 10 * K)]
    F["R2_partly"] = [fl(min(worst) * 0.97, 10 * K), ce(max(worst) * 1.03, 10 * K)]
    F["ladder_rivals"] = {k: ladder_cells(v) for k, v in riv.items()}
    F["ladder_hurried"] = {k: dict(ladder_cells(v), first_sale=v["first_sale"], settled=v["n_settled"]) for k, v in lh.items()}
    F["ladder_counts"] = dict(settled=lad["n_settled"], rebuilt=lad["n_rebuilt"])
    rb, aa = R["rebuild"], R["against_actual"]
    px = rb["proxies"]
    F["rebuild"] = dict(first_published=rb["first_published"], six_month_first=rb["six_first"], one_year_first=rb["one_first"],
                        nine_day_first=rb["nine_first"], overlap_days=rb["overlap_days"], hot_days=rb["hot_days"], rmse=round(rb["rmse"], 2),
                        rmse_hot=round(rb["rmse_hot"], 2), ratio_all_pct=round(100 * (rb["ratio_all"] - 1), 1),
                        ratio_hot_pct=round(100 * (1 - rb["ratio_hot"]), 1), coef=[round(c, 3) for c in rb["coef"]],
                        proxy_r2=round(rb["proxy_r2"], 2), proxy_rmse=round(rb["proxy_rmse"], 2), proxy_bias_hot=round(px[PROXY]["bias_hot"], 1),
                        proxy_rmse_hot=round(px[PROXY]["rmse_hot"], 2), ratio_bias_hot=round(px["30-day index times the average ratio"]["bias_hot"], 1),
                        as_stands_bias_hot=round(px["30-day index as it stands"]["bias_hot"], 1))
    F["cross_check"] = dict(first=aa["first"], overlap_days=aa["overlap_days"], max_diff=round(aa["max_diff"], 2), sale_dates=aa["sale_dates"],
                            mean_abs={k: round(v, 2) for k, v in aa["mean_abs"].items()}, proxy_bias={k: round(v, 2) for k, v in aa["proxy_bias"].items()},
                            stressed=[{k: (round(v, 2) if isinstance(v, float) else v) for k, v in x.items()} for x in aa["stressed"]],
                            actual=ladder_cells(riv["actual"]))
    F["ladders_per_100k"] = {str(m): dict(ladder_cells(v), settled=v["n_settled"], rebuilt=v["n_rebuilt"],
                                          by_year={str(y): r1000(x * P.PER) for y, x in v["by_year"].items()}) for m, v in R["ladder"].items()}
    # ---------------- R3: the standing ladder's peak collateral
    op = R["old_peak"]
    peaks = [v["peak"] for v in op.values()]
    F["R3_old_peak_usd"] = r1000(op["total variance"]["peak"])
    F["R3_old_peak_day"] = op["total variance"]["day"]
    F["R3_band"] = [fl(min(peaks), 100 * K), ce(max(peaks), 100 * K)]
    F["R3_partly"] = [fl(min(peaks) * 0.95, 100 * K), ce(max(peaks) * 1.05, 100 * K)]
    F["old_peak_rivals"] = {k: dict(peak_usd=r1000(v["peak"]), day=v["day"]) for k, v in op.items()}
    F["old_peak_hurried"] = {k: r1000(v) for k, v in R["old_peak_hurried"].items()}
    F["old_peak_episodes"] = {y: dict(peak_usd=r1000(v["peak"]), day=v["day"]) for y, v in R["old_episodes"].items()}
    # ---------------- R4 and R5: the largest new ladder
    for tag, rid, key in (("size_new", "R4", "R4_size_usd"), ("size_alt", "R5", "R5_alt_size_usd")):
        s, rv = R[tag], R[tag + "_rivals"]
        F[key] = int(s["size"])
        F[rid + "_binds"] = dict(limit=s["limit"], day=str(s["when"]))
        F[rid + "_band"] = [fl(min(rv.values()), K), ce(max(rv.values()), K)]
        F[rid + "_partly"] = [fl(min(rv.values()) * 0.97, K), ce(max(rv.values()) * 1.03, K)]
        F[rid + "_rivals"] = {k: fl(v, P.SIZE_STEP) for k, v in rv.items()}
        F[rid + "_hurried"] = {k: fl(v, P.SIZE_STEP) for k, v in R[tag + "_hurried"].items()}
        F[rid + "_rival_binds"] = [[a, str(b)] for a, b in R[tag + "_binds"]]
    size = F["R4_size_usd"]
    pr, at, alt = R["proposal"], R["at_size"], R["alt_at_size"]
    F["quoted"] = dict(worst_year=pr["worst_year"], worst_usd=r1000(pr["worst"]), peak_usd=r1000(pr["peak"]), peak_day=pr["peak_day"],
                       over_usd=r1000(pr["peak"]) - int(P.LIM_COLL))
    F["at_size"] = dict(worst_year=at["worst_year"], worst_usd=r1000(at["worst"]), peak_usd=r1000(at["peak"]), peak_day=at["peak_day"],
                        old_at_peak_usd=r1000(at["old_at_peak"]), new_at_peak_usd=r1000(at["new_at_peak"]),
                        new_per_100k_at_peak_usd=r1000(at["new_at_peak"] / size * P.PER))
    F["at_size"]["room_usd"] = int(P.LIM_COLL) - F["at_size"]["old_at_peak_usd"]
    F["alt_at_size"] = dict(worst_year=alt["worst_year"], worst_usd=r1000(alt["worst"]), peak_usd=r1000(alt["peak"]), peak_day=alt["peak_day"],
                            old_at_peak_usd=r1000(alt["old_at_peak"]), new_at_peak_usd=r1000(alt["new_at_peak"]),
                            new_per_100k_at_peak_usd=r1000(alt["new_at_peak"] / R["size_alt"]["size"] * P.PER))
    # ---------------- R6 and R7: how well the record pins each ladder's average
    for mat, key in ((P.OLD_MAT, "R6_avg_range_12m"), (P.NEW_MAT, "R7_avg_range_3m")):
        d = R["avg_range"][mat]
        pairs = list(d["sound"].values()) + (list(d["by_rebuild"].values()) if mat == P.NEW_MAT else [])
        F[key] = range_cells(d["sound"][d["golden"]], P.PER)
        F[key[:2] + "_bands"] = range_bands(pairs, P.PER, K)
        st = d["stats"]
        F["avg_%dm" % mat] = dict(n=st["n"], avg_per_sale_usd=r1000(st["mean"] * P.PER), next_sale_correlation=round(st["ac1"], 2),
                                  block_sales=2 * mat, methods=len(d["sound"]), few_lags=st["few_lags"], shared_months=mat - 1,
                                  sound={k: range_cells(v, P.PER) for k, v in d["sound"].items()},
                                  hurried={k: range_cells(v, P.PER) for k, v in d["hurried"].items()})
    px3 = R["avg_range"][P.NEW_MAT]["proxy"]
    F["avg_3m"]["proxy"] = dict(hurried=range_cells(px3["hurried"]["single settlements resampled"], P.PER),
                                blocks=range_cells(px3["sound"][R["avg_range"][P.NEW_MAT]["golden"]], P.PER))
    # ---------------- R8 and R9: the open swaps that expire in the plan year
    ex, exh, rs = R["expect"], R["expect_hurried"], R["range_stats"]
    gold = ex[GOLD_E]
    F["R8_expected_usd"] = r1000(gold * P.OLD_SIZE)
    F["R8_band"] = [fl(min(ex.values()) * P.OLD_SIZE, 10 * K), ce(max(ex.values()) * P.OLD_SIZE, 10 * K)]
    F["R8_partly"] = [fl(min(ex.values()) * P.OLD_SIZE * 0.95, 10 * K), ce(max(ex.values()) * P.OLD_SIZE * 1.03, 10 * K)]
    F["expect_rivals"] = {k: r1000(v * P.OLD_SIZE) for k, v in ex.items()}
    F["expect_hurried"] = {k: r1000(v * P.OLD_SIZE) for k, v in exh.items()}
    obp = R["replay"]["ob"]
    F["plan_year"] = P.PLAN_YEAR
    F["plan_sale_months"] = int(len(obp))
    F["open_per_swap"] = [dict(sale=str(s.date()), expiry=str(e.date()), expected_usd=r1000(m * P.OLD_SIZE), value_usd=int(round(v * P.OLD_SIZE)))
                          for s, e, m, v in zip(obp.sale, obp.expiry, rs["per_swap_mean"], obp.mark)]
    rg, rgh = R["range"], R["range_hurried"]
    F["R9_range"] = range_cells(rg[GOLD_R], P.OLD_SIZE)
    lows, highs = [v[0] * P.OLD_SIZE for v in rg.values()], [v[1] * P.OLD_SIZE for v in rg.values()]
    F["R9_bands"] = dict(low_usd=[fl(min(lows) * 0.9, 10 * K), ce(max(lows) * 1.05, 10 * K)], high_usd=[fl(min(highs) * 0.97, 10 * K), ce(max(highs) * 1.03, 10 * K)])
    F["open_range_rivals"] = {k: range_cells(v, P.OLD_SIZE) for k, v in rg.items()}
    F["open_range_hurried"] = {k: range_cells(v, P.OLD_SIZE) for k, v in rgh.items()}
    mark_plan = exh[MARK_E]
    F["replay"] = dict(start_dates=rs["n_starts"], first_start=rs["first_start"], last_start=rs["last_start"], median_usd=r1000(rs["median"] * P.OLD_SIZE),
                       share_above_mark_pct=int(round(100 * (1 - rs["share_below_mark"]))), share_below_zero_pct=round(100 * rs["share_below_zero"], 1),
                       mark_usd=r1000(mark_plan * P.OLD_SIZE), one_month_ratio=round(R["pooled"]["one_month"], 2),
                       twelve_month_ratio=round(R["pooled"]["twelve_month"], 2))
    # ---------------- R10: every settlement that falls in the plan year
    pl = R["plan"]
    a3, a6, a12 = (R["ladder"][m]["avg_per_sale"] for m in (P.NEW_MAT, P.ALT_MAT, P.OLD_MAT))
    cal = R["new_calendar"]
    inyr = cal[cal.in_year]
    n3, n12 = pl["n_new"], pl["n_old"]
    unsold = r1000(pl["old_unsold"])
    new_cash = r1000(pl["three"])
    F["R10_plan"] = plan_cells(F["R8_expected_usd"], unsold, new_cash, pl["sound"][GOLD_P])
    lo3, hi3 = F["R1_band"]
    three_band = [fl(n3 * F["R4_band"][0] * lo3 / P.PER, 10 * K), ce(n3 * F["R4_band"][1] * hi3 / P.PER, 10 * K)]
    twelve_band = [F["R8_band"][0] + unsold, F["R8_band"][1] + unsold]
    rb_ = range_bands(list(pl["sound"].values()), 1.0, 100 * K)
    F["R10_bands"] = dict(twelve_month_usd=twelve_band, three_month_usd=three_band, total_usd=[twelve_band[0] + three_band[0], twelve_band[1] + three_band[1]],
                          low_usd=rb_["low_usd"], high_usd=rb_["high_usd"])
    legs12 = [g for g in pl["legs"] if g["ladder"] == P.OLD_MAT]
    F["plan"] = dict(settlements=F["plan_sale_months"] + n12 + n3, open_sale_months=F["plan_sale_months"], unsold_12m=n12, new_3m=n3,
                     unsold_12m_usd=unsold, avg_12m_per_sale_usd=r1000(a12 * P.OLD_SIZE), avg_12m_per_100k_usd=r1000(a12 * P.PER),
                     unsold_sales=[str(g["sale"].date()) for g in legs12], unsold_expiries=[str(g["expiry"].date()) for g in legs12],
                     low_paid_usd=-F["R10_plan"]["low_usd"], start_dates=pl["stats"]["n_starts"], first_start=pl["stats"]["first_start"],
                     last_start=pl["stats"]["last_start"], replay_mean_usd=r1000(pl["stats"]["replay_mean"]),
                     worst_usd=r1000(-pl["stats"]["minimum"]), worst_start=pl["stats"]["worst_start"],
                     share_below_zero_pct=int(round(100 * pl["stats"]["share_below_zero"])),
                     rivals={k: range_cells(v, 1.0) for k, v in pl["sound"].items()}, hurried={k: range_cells(v, 1.0) for k, v in pl["hurried"].items()})
    F["plan"]["unrelated_low_paid_usd"] = -F["plan"]["hurried"]["unsold swaps drawn one by one from their ladder's record"]["low_usd"]
    F["new_calendar"] = dict(settlements_in_year=n3, sales_in_year=int(len(cal)), first_sale=str(cal.sale.iloc[0].date()),
                             last_sale_settling_in_year=str(inyr.sale.iloc[-1].date()), first_expiry=str(inyr.expiry.iloc[0].date()),
                             last_expiry_in_year=str(inyr.expiry.iloc[-1].date()), per_settlement_usd=r1000(size * a3), twelve_usd=r1000(12 * size * a3),
                             rows=[dict(sale=str(s.date()), expiry=str(e.date()), in_year=bool(i)) for s, e, i in zip(cal.sale, cal.expiry, cal.in_year)])
    # ---------------- R11: the recommendation
    p10 = F["R10_plan"]
    F["R11_call"] = dict(size_usd=size, plan_usd=p10["total_usd"], low_usd=p10["low_usd"], high_usd=p10["high_usd"])
    F["R11_bands"] = dict(size_usd=F["R4_band"], plan_usd=F["R10_bands"]["total_usd"], low_usd=F["R10_bands"]["low_usd"], high_usd=F["R10_bands"]["high_usd"])
    # ---------------- the careful but hurried analysis the recommendation rejects, and the index's own history
    hs = R["size_new_hurried"]
    csize = fl(hs["missing strikes from the " + PROXY], P.SIZE_STEP)
    c_new = r1000(n3 * csize * lh[PROXY]["avg_per_sale"])
    at_c = A.usage(P.NEW_MAT, csize)
    F["hurried"] = dict(size_usd=csize, avg_3m_usd=r1000(lh[PROXY]["avg_per_sale"] * P.PER), worst_year_loss_usd=r1000(-lh[PROXY]["worst"] * P.PER),
                        new_cash_usd=c_new, open_usd=r1000(mark_plan * P.OLD_SIZE), plan_usd=r1000(mark_plan * P.OLD_SIZE) + unsold + c_new,
                        peak_on_record_usd=r1000(at_c["peak"]), peak_day=at_c["peak_day"], over_usd=r1000(at_c["peak"]) - int(P.LIM_COLL))
    osize = fl(hs[OWN], P.SIZE_STEP)
    at_o = A.usage(P.NEW_MAT, osize)
    F["own_history"] = dict(size_usd=osize, first_sale=lh[OWN]["first_sale"], avg_3m_usd=r1000(lh[OWN]["avg_per_sale"] * P.PER),
                            worst_year=int(lh[OWN]["worst_year"]), worst_year_loss_usd=r1000(-lh[OWN]["worst"] * P.PER),
                            peak_on_record_usd=r1000(at_o["peak"]), peak_day=at_o["peak_day"])
    g_open = F["R8_expected_usd"]

    def route(name, sz=size, av=a3, open_usd=g_open, with_unsold=True, n_new=n3):
        return dict(route=name, size_usd=int(sz), plan_usd=int(open_usd + (unsold if with_unsold else 0) + r1000(n_new * sz * av)))

    F["routes"] = [
        route("the golden"),
        route("missing strikes from a regression on the 30-day index alone, open swaps at their marks", csize, lh[PROXY]["avg_per_sale"], F["hurried"]["open_usd"]),
        route("missing strikes from a regression on the 30-day index alone", csize, lh[PROXY]["avg_per_sale"]),
        route("missing strikes from the 30-day index times its average ratio", fl(hs["missing strikes from the 30-day index times the average ratio"], P.SIZE_STEP),
              lh["30-day index times the average ratio"]["avg_per_sale"]),
        route("missing strikes read straight off the 30-day index", fl(hs["missing strikes from the 30-day index as it stands"], P.SIZE_STEP),
              lh["30-day index as it stands"]["avg_per_sale"]),
        route("the 3-month ladder run only from its index's first date", osize, lh[OWN]["avg_per_sale"]),
        route("each swap valued at its own index", fl(hs["marks at each swap's own index"], P.SIZE_STEP)),
        route("every swap valued at the 30-day index", fl(hs["marks at the 30-day index"], P.SIZE_STEP)),
        route("no cap in the valuation", fl(hs["no cap in the mark"], P.SIZE_STEP)),
        route("the new ladder sized on its own", fl(hs["the new ladder on its own"], P.SIZE_STEP)),
        route("the settlement limit alone", fl(hs["the settlement limit alone"], P.SIZE_STEP)),
        route("open swaps at their marks", open_usd=F["expect_hurried"][MARK_E]),
        route("open swaps on a volatility forecast, squared", open_usd=F["expect_hurried"]["a volatility forecast, squared"]),
        route("open swaps at the median start date", open_usd=F["expect_hurried"]["the median start date"]),
        route("the standing ladder's two sales still to come left out", with_unsold=False),
        route("twelve settlements counted for the new ladder", n_new=12),
    ]
    d = R["daily"]
    F["daily"] = dict(rows=int(len(d)), first_day=str(d.date.iloc[0].date()), last_day=str(d.date.iloc[-1].date()),
                      peak_usd=r1000(d.collateral.max()), peak_day=str(d.loc[d.collateral.idxmax(), "date"].date()),
                      days_with_collateral=int((d.collateral > 0).sum()))
    return F
