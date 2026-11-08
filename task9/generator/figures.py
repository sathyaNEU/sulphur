"""task9: figures.json, every owed figure as the write-up states it, from one analysis run."""
import analysis as A


def r2(x):
    return round(100.0 * x, 2)


def make(R):
    E, G = R["est"], R["lgd"]
    golden = {}
    for k, s in R["ports"].items():
        golden[k] = dict(p5_pct=r2(s["p5"]), by_year_pct=[r2(v) for v in s["by_year"]],
                         need_pct=[round(100 * v, 1) for v in s["need"]], n=s["n"], houses=s["houses"],
                         funds=s["funds"], sectors=s["sectors"], par_eur_m=round(s["par_eur"], 1),
                         ratings=s["ratings"], exceed_raw=[round(v, 6) for v in s["exceed"]],
                         el_note_bp_a_year=round(1e4 * s["el_note"] / 5, 2), el_port_pct=round(100 * s["el_port"], 2),
                         pd1_pct=round(100 * s["pd1"], 2), age=round(s["age"], 2))
    rv = R["rivals"]
    rung = {name: {k: dict(p5_pct=r2(v["p5"]), by_year_pct=[r2(x) for x in v["by_year"]],
                           need_pct=[round(100 * x, 1) for x in v["need"]]) for k, v in d.items()}
            for name, d in rv.items()}
    ev = R["evidence"]
    sh, oh = ev["same_house_same_sector_year"], ev["other_house_same_sector_year"]
    sy, oy = ev["same_house_same_year"], ev["same_house_other_year"]
    base = ev["base_rate"]
    import math
    band = {k: [math.floor(1000 * lo) / 10.0, math.ceil(1000 * hi) / 10.0] for k, (lo, hi) in R["band"].items()}
    F = {
        "call": "Ostvale",
        "band_pct": band,
        "moment_dependence": {k: round(v, 3) for k, v in R["moment_dependence"].items()},
        "bar_pct": round(100 * A.BAR, 1),
        "subordination_pct": {k: round(100 * v, 1) for k, v in A.SUBORD.items()},
        "targets_pct": [100 * t for t in A.TARGETS],
        "paths": A.NSIM,
        "chart_loss_axis_max_pct": 30,
        "mp_rn_2_sections_cited": ["2.1", "2.2", "3.2", "3.3", "3.4", "3.5", "4.1", "4.2"],
        "golden": golden,
        "grid": R["ports"]["KL"]["grid"],
        "default_path": rung.pop("industry"),
        "rungs": {"one_factor": rung["one_factor"], "fund_persistent": rung["fund_persistent"],
                  "fund_year": rung["fund_year"], "closed_lgd": rung["golden_closed_lgd"]},
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
