"""task9: figures.json, every owed figure as the write-up states it, from one analysis run."""
import math

import numpy as np

import analysis as A
import world as WD

SECTOR_NAMES = [s[1] for s in WD.SECTORS]


def r1(x):
    return round(100.0 * x, 1)


def r2(x):
    return round(100.0 * x, 2)


def up(x):
    return int(math.ceil(100 * x - 1e-9))


def call_of(pk, po, bar=A.BAR):
    ok_k, ok_o = pk < bar, po < bar
    if ok_k and ok_o:
        return "Kestrel Lane" if pk < po else "Ostvale"
    if ok_k:
        return "Kestrel Lane"
    if ok_o:
        return "Ostvale"
    return "neither"


def make(R):
    E, G, LK, S = R["est"], R["lgd"], R["link"], R["sectors"]
    golden = {}
    for k, s in R["ports"].items():
        golden[k] = dict(p5_pct=r1(s["p5"]), p5_raw=round(s["p5"], 6), by_year_pct=[r1(v) for v in s["by_year"]],
                         by_year_raw=[round(v, 6) for v in s["by_year"]],
                         need_pct=[up(v) for v in s["need"][:2]],
                         need_raw=[round(100 * v, 2) for v in s["need"]], n=s["n"], houses=s["houses"],
                         funds=s["funds"], sectors=s["sectors"], par_eur_m=round(s["par_eur"], 1),
                         ratings=s["ratings"], exceed_raw=[round(v, 6) for v in s["exceed"]],
                         el_port_pct=round(100 * s["el_port"], 2), el_pct=r1(s["el_port"]), el_raw=round(s["el_port"], 6),
                         pd1_pct=round(100 * s["pd1"], 2), age=round(s["age"], 2),
                         loading=round(s["loading"], 3), loading_raw=round(s["loading"], 6),
                         swing_share_pct=round(100 * s["swing_share"], 1))
    rv = R["rivals"]
    rung = {name: {k: dict(p5_pct=r1(v["p5"]), p5_pct2=r2(v["p5"]), p5_raw=round(v["p5"], 6),
                           by_year_pct=[r1(x) for x in v["by_year"]],
                           need_pct=[up(x) for x in v["need"][:2]], el_pct=r1(v["el"]), el_raw=round(v["el"], 6))
                   for k, v in d.items()} for name, d in rv.items()}
    for name, d in rung.items():
        d["call"] = call_of(d["KL"]["p5_raw"], d["OS"]["p5_raw"])
    ev, se = R["evidence"], R["sector_evidence"]
    sh, oh = ev["same_house_same_sector_year"], ev["other_house_same_sector_year"]
    sy, oy = ev["same_house_same_year"], ev["same_house_other_year"]
    base = ev["base_rate"]
    band = {k: [math.floor(1000 * lo) / 10.0, math.ceil(1000 * hi) / 10.0] for k, (lo, hi) in R["band"].items()}
    bc = R["by_cluster"]
    swing = S["swing"]
    yrs = se["years"]
    yi = {y: i for i, y in enumerate(yrs)}
    l = np.array(S["l"])
    rest = [s_ for s_ in range(16) if s_ not in swing]
    worst = sorted(yrs, key=lambda y: -se["swing_rate"][yi[y]])[:3]
    Ly, Lc, Lh, Lp, Lg = R["link_year_only"], R["link_closed"], R["link_house_only"], R["link_pooled"], R["link_given_year"]
    F = {
        "call": call_of(golden["KL"]["p5_raw"], golden["OS"]["p5_raw"]),
        "band_pct": band,
        "band_members": [dict(key=m["key"], KL=r2(m["KL"]), OS=r2(m["OS"]), loading_OS=round(m["loading_OS"], 3),
                              house_share=round(m["house_share"], 3), link=[round(x, 3) for x in m["link"]],
                              full={k: dict(by_year_pct=[r1(x) for x in m[k + "_full"]["by_year"]],
                                            need_pct=[up(x) for x in m[k + "_full"]["need"]],
                                            el_pct=r1(m[k + "_full"]["el"])) for k in ("KL", "OS")})
                         for m in R["band_members"]],
        "moment_dependence": {k: round(v, 3) for k, v in R["moment_dependence"].items()},
        "bar_pct": round(100 * A.BAR, 1),
        "subordination_pct": {k: round(100 * v, 1) for k, v in A.SUBORD.items()},
        "targets_pct": [100 * t for t in A.TARGETS[:2]],
        "paths": A.NSIM,
        "chart_loss_axis_max_pct": 30,
        "mp_rn_2_sections_cited": ["2.1", "2.2", "3.2", "3.4", "4.1", "4.2"],
        "golden": golden,
        "grid": R["ports"]["KL"]["grid"],
        "default_path": rung["industry"],
        "rungs": {k: rung[k] for k in rung if k != "industry"},
        "link": dict(a=round(LK["a"], 3), bm=round(LK["bm"], 3), bh=round(LK["bh"], 3), n=LK["n"],
                     ordinary_pct=round(100 * LK["a"], 1), bad_pct=round(100 * (LK["a"] - 1.5 * LK["bh"]), 1)),
        "link_year_only": dict(a=round(Ly["a"], 3), bm=round(Ly["bm"], 3), n=Ly["n"]),
        "link_pooled": dict(a=round(Lp["a"], 3), bm=round(Lp["bm"], 3), bh=round(Lp["bh"], 3), n=Lp["n"]),
        "link_closed": dict(a=round(Lc["a"], 3), bm=round(Lc["bm"], 3), bh=round(Lc["bh"], 3), n=Lc["n"]),
        "link_house_only": dict(a=round(Lh["a"], 3), bh=round(Lh["bh"], 3), n=Lh["n"]),
        "link_given_year": dict(a=round(Lg["a"], 3), bm=round(Lg["bm"], 3), bh=round(Lg["bh"], 3), n=Lg["n"]),
        "recovery_by_other_defaults": {str(k): dict(recovery_pct=round(100 * v[0], 1), n=v[1]) for k, v in bc.items()},
        "count_link": dict(cells_pct=[round(100 * v, 1) for v in R["count_link"]["cells"]], a=round(R["count_link"]["a"], 3),
                           b=round(R["count_link"]["b"], 3), n=R["count_link"]["n"],
                           book_seen_median=R["count_link"]["book_seen_median"],
                           book_seen_mean=round(R["count_link"]["book_seen_mean"], 1)),
        "grain": {k: dict(v) for k, v in R["grain"].items()},
        "pooled_moment_pct": {k: r2(v) for k, v in R["pooled_moment"].items()},
        "band_links": {k: [round(x, 3) for x in v] for k, v in R["band_links"].items()},
        "band_all_pct": {k: [r2(x) for x in v] for k, v in R["band_all"].items()},
        "estimates": {k: round(E[k], 3) for k in ("am", "ak", "ck", "ch", "ah", "cf", "af", "cq", "aq", "cqh")},
        "house_share": round(S["ah_lat"], 3),
        "sectors": dict(loadings={SECTOR_NAMES[i]: round(float(l[i]), 3) for i in range(16)},
                        k=round(S["k"], 3), pooled_l=round(S["pooled_l"], 3), pooled_k=round(S["pooled_k"], 3),
                        loglik=round(S["loglik"], 1), pooled_loglik=round(S["pooled_loglik"], 1),
                        lr=round(2 * (S["loglik"] - S["pooled_loglik"]), 1), df=15,
                        ll_gain=round(S["loglik"] - S["pooled_loglik"], 1),
                        swing=[SECTOR_NAMES[i] for i in swing],
                        swing_min=round(float(min(l[swing])), 3), swing_max=round(float(max(l[swing])), 3),
                        rest_max=round(float(max(l[rest])), 3),
                        moment=[round(x, 3) for x in R["moment_loadings"]],
                        two_group=dict(swing=round(R["two_group"]["l"][swing[0]], 3), rest=round(R["two_group"]["l"][rest[0]], 3),
                                       k=round(R["two_group"]["k"], 3))),
        "sector_evidence": dict(worst_years=worst,
                                swing_rate_pct={str(y): round(100 * se["swing_rate"][yi[y]], 1) for y in yrs},
                                rest_rate_pct={str(y): round(100 * se["rest_rate"][yi[y]], 1) for y in yrs},
                                swing_corr_within=round(se["swing_corr_within"], 2),
                                rest_corr_within=round(se["rest_corr_within"], 2),
                                swing_rest_corr=round(se["swing_rest_corr"], 2)),
        "open_evidence": {k: (round(v, 2) if isinstance(v, float) else v) for k, v in R["open_evidence"].items()},
        "loglik": {k: round(E[k], 1) for k in ("ll_h", "ll_f", "ll_q", "ll_qh", "ll_h0", "ll_pd")},
        "lgd": dict(lgd_pct=round(100 * G["lgd"], 1), lgd_closed_pct=round(100 * G["lgd_closed"], 1),
                    n_mature=G["n_mature"], n_closed=G["n_closed"], open=sum(G["open_by_year"].values())),
        "panel": dict(company_years=R["panel_n"], defaults=R["panel_defaults"], houses=R["n_houses"],
                      funds=R["n_funds"], unlinked=R["unlinked"]),
        "evidence": dict(same_house_same_sector_year_pct=round(100 * sh[0] / sh[1], 2),
                         other_house_same_sector_year_pct=round(100 * oh[0] / oh[1], 2),
                         same_house_same_year_pct=round(100 * sy[0] / sy[1], 3),
                         same_house_other_year_pct=round(100 * oy[0] / oy[1], 3),
                         independent_pair_pct=round(100 * base * base, 3),
                         ratio_same_sector_year=round((sh[0] / sh[1]) / (oh[0] / oh[1]), 1),
                         counts=dict(same_house_same_sector_year=list(sh), other_house_same_sector_year=list(oh),
                                     same_house_same_year=list(sy), same_house_other_year=list(oy))),
    }
    # the band each graded ask carries: the span of every sound estimator's figure and the golden's (the five-year
    # chance at the end of 2031 is the same band as the five-year chance itself)
    full = [m["full"] for m in F["band_members"]]

    def span(vals, unit):
        return [round(math.floor(min(vals) / unit + 1e-9) * unit, 6), round(math.ceil(max(vals) / unit - 1e-9) * unit, 6)]

    F["ask_bands"] = {k: dict(
        p5=band[k],
        el=span([f[k]["el_pct"] for f in full] + [golden[k]["el_pct"]], 0.1),
        need=[span([f[k]["need_pct"][i] for f in full] + [golden[k]["need_pct"][i]], 1) for i in (0, 1)],
        by_year=[span([f[k]["by_year_pct"][i] for f in full] + [golden[k]["by_year_pct"][i]], 0.1) for i in range(4)]
        + [band[k]]) for k in ("KL", "OS")}
    return F
