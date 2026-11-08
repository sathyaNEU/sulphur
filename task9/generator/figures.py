"""task9: figures.json, every owed figure as the write-up states it, from one analysis run."""
import math

import analysis as A


def r1(x):
    return round(100.0 * x, 1)


def r2(x):
    return round(100.0 * x, 2)


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
    E, G, LK = R["est"], R["lgd"], R["link"]
    golden = {}
    for k, s in R["ports"].items():
        golden[k] = dict(p5_pct=r1(s["p5"]), p5_raw=round(s["p5"], 6), by_year_pct=[r1(v) for v in s["by_year"]],
                         by_year_raw=[round(v, 6) for v in s["by_year"]],
                         need_pct=[int(math.ceil(100 * v - 1e-9)) for v in s["need"][:2]],
                         need_raw=[round(100 * v, 2) for v in s["need"]], n=s["n"], houses=s["houses"],
                         funds=s["funds"], sectors=s["sectors"], par_eur_m=round(s["par_eur"], 1),
                         ratings=s["ratings"], exceed_raw=[round(v, 6) for v in s["exceed"]],
                         el_port_pct=round(100 * s["el_port"], 2), pd1_pct=round(100 * s["pd1"], 2),
                         age=round(s["age"], 2))
    rv = R["rivals"]
    rung = {name: {k: dict(p5_pct=r1(v["p5"]), p5_raw=round(v["p5"], 6), by_year_pct=[r1(x) for x in v["by_year"]],
                           need_pct=[int(math.ceil(100 * x - 1e-9)) for x in v["need"][:2]])
                   for k, v in d.items()} for name, d in rv.items()}
    for name, d in rung.items():
        d["call"] = call_of(d["KL"]["p5_raw"], d["OS"]["p5_raw"])
    ev = R["evidence"]
    sh, oh = ev["same_house_same_sector_year"], ev["other_house_same_sector_year"]
    sy, oy = ev["same_house_same_year"], ev["same_house_other_year"]
    base = ev["base_rate"]
    band = {k: [math.floor(1000 * lo) / 10.0, math.ceil(1000 * hi) / 10.0] for k, (lo, hi) in R["band"].items()}
    bc = R["by_cluster"]
    Ly, Lc, Lh = R["link_year_only"], R["link_closed"], R["link_house_only"]
    F = {
        "call": call_of(golden["KL"]["p5_raw"], golden["OS"]["p5_raw"]),
        "band_pct": band,
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
        "link": dict(a=round(LK["a"], 3), bm=round(LK["bm"], 3), bh=round(LK["bh"], 3), n=LK["n"]),
        "link_year_only": dict(a=round(Ly["a"], 3), bm=round(Ly["bm"], 3), n=Ly["n"]),
        "link_closed": dict(a=round(Lc["a"], 3), bm=round(Lc["bm"], 3), bh=round(Lc["bh"], 3), n=Lc["n"]),
        "link_house_only": dict(a=round(Lh["a"], 3), bh=round(Lh["bh"], 3), n=Lh["n"]),
        "recovery_by_other_defaults": {str(k): dict(recovery_pct=round(100 * v[0], 1), n=v[1]) for k, v in bc.items()},
        "estimates": {k: round(E[k], 3) for k in ("am", "ak", "ck", "ch", "ah", "cf", "af", "cq", "aq", "cqh")},
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
    return F
