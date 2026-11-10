"""task3: figures.json (every figure the answer blocks and the goldens state) and effort.json (each result's golden,
band and the value each pass files), from one analysis run on the cut pack."""
import json
import os

import numpy as np

import analysis as A

HERE = os.path.dirname(os.path.abspath(__file__))


def r1(x):
    return float(round(x + 1e-9, 1))


def r0(x):
    return int(np.floor(x + 0.5))


def make(R):
    names = A.NAMES
    exp = R["exp"]
    fam = R["family"]
    alt = R["alt"]
    v = R["var"]
    order = R["rank"]
    F = {
        "call_pair": [names[k] for k in R["funded"]],
        "call_keys": R["funded"],
        "rank": [names[k] for k in order],
        "rank_keys": order,
        "harbor_exp": r1(exp["harbor"]["mean"]),
        "harbor_lo": r0(exp["harbor"]["lo"]),
        "harbor_hi": r0(exp["harbor"]["hi"]),
        "harbor_2025": int(R["harbor_obs"][2025]),
        "harbor_minor": A.HARBOR_MINOR,
        "plan": A.PLAN,
        "A25": float(round(R["A25"], 2)),
        "bridge": {"sea": r1(R["bridge"]["sea"]["shapley"]), "tides": r1(R["bridge"]["tides"]["shapley"]),
                   "weather": r1(R["bridge"]["weather"]["shapley"]), "total": r1(R["bridge_full"] - R["bridge_base"])},
        "bridge_range": {k: [r1(R["bridge"][k]["lo"]), r1(R["bridge"][k]["hi"])] for k in ("sea", "tides", "weather")},
        "front_level_navd88": float(round(R["front_level_navd88"], 2)),
        "front_level_mllw": float(round(R["front_level"], 2)),
        "front_wet_tides": R["front_wet_tides"],
        "replay_2025": R["replay_2025"],
        "pair_hold": int(R["pair_hold"]),
        "pair_displaced": {k: int(v) for k, v in R["pair_displaced"].items()},
        "n_weather_years": len(A.WX_YEARS),
        "per_year": R["per_year"],
        "river_setup_25k": float(round(R["river_fit"][R["river_form"]]["c1"] * (2.5 ** 0.85 - 0.5 ** 0.85)
                                       if R["river_form"] == "pow" else R["river_fit"][R["river_form"]]["c1"] * 2.0, 2)),
        "front_sensor_days": R["hind"]["front_sensor_only"],
        "front_outage_days": R["hind"]["front_outage_days"],
        "hind": {k: int(R["hind"][k]) for k in A.ORDER},
        "exp": {k: r1(exp[k]["mean"]) for k in A.ORDER},
        "exp_range": {k: [r0(exp[k]["lo"]), r0(exp[k]["hi"])] for k in A.ORDER},
        "marsh_Hstar": float(round(R["fits"]["marsh"]["Hstar"], 2)),
        "oyster_Hstar": float(round(R["fits"]["oyster"]["Hstar"], 2)),
        "marsh_P": float(round(R["fits"]["marsh"]["hinge"]["P"], 2)),
        "oyster_P": float(round(R["fits"]["oyster"]["hinge"]["P"], 2)),
        "marsh_slopes": [float(round(R["fits"]["marsh"]["hinge"]["b1"], 2)),
                         float(round(R["fits"]["marsh"]["hinge"]["b1"] + R["fits"]["marsh"]["hinge"]["b2"], 2))],
        "marsh_linear_slope": float(round(R["fits"]["marsh"]["linear"]["b"], 2)),
        "marsh_Hlin": float(round(R["fits"]["marsh"]["Hlin"], 2)),
        "marsh_above": R["fits"]["marsh"]["above"],
        "marsh_n": R["fits"]["marsh"]["n"],
        "marsh_top_n": R["fits"]["marsh"]["top_n"],
        "marsh_top_below": R["fits"]["marsh"]["top_below_line"],
        "marsh_top_resid": float(round(R["fits"]["marsh"]["top_resid"], 2)),
        "marsh_sd": [float(round(R["fits"]["marsh"]["sd_hinge"], 2)), float(round(R["fits"]["marsh"]["sd_line"], 2))],
        "river_form": R["river_form"],
        "river_setup_10k": float(round(R["river_fit"][R["river_form"]]["c1"] * ((1.0) ** 0.85 - (0.5) ** 0.85)
                                       if R["river_form"] == "pow" else R["river_fit"][R["river_form"]]["c1"] * 0.5, 2)),
        "river_r": float(round(R["river_fit"][R["river_form"]]["r"], 2)),
        "river_q": [int(round(x, -2)) for x in R["river_campaign_q"]],
        "river_pooled_offset": float(round(R["river_pooled"]["c0"], 2)),
        "routes": {},
        "variants": {k: (r1(x["exp"]) if isinstance(x, dict) else x) for k, x in v.items()},
        "variants_hind": {k: x["hind"] for k, x in v.items() if isinstance(x, dict)},
        "datums_nav": float(round(R["nav"], 2)),
        "constants": {"range_pct": 90, "setup_flows_cfs": [5000, 25000], "top_harbor_ft": 8.3, "station": 8673718,
                      "years": [1983, 1990, 2001, 2024, 2025, 2026, 2027, 2028], "marsh_platform_navd88": 4.29},
        "marsh_top_resid_abs": float(round(-R["fits"]["marsh"]["top_resid"], 2)),
        "as_of": "2026-11-10",
    }
    # the funded pair under each route
    def top2(d):
        return [names[k] for k in sorted(d, key=lambda k: -d[k])[:2]]
    g = {k: exp[k]["mean"] for k in A.ORDER}
    routes = {
        "golden": top2(g),
        "marsh straight line": top2(dict(g, marsh=v["marsh_linear"]["exp"], oyster=v["oyster_linear"]["exp"])),
        "river one offset": top2(dict(g, river=v["river_pooled"]["exp"])),
        "both (careful but hurried)": top2(dict(g, marsh=v["marsh_linear"]["exp"], oyster=v["oyster_linear"]["exp"],
                                                river=v["river_pooled"]["exp"])),
        "no transfer, drain rim (quick)": top2(dict(front=v["front_rim"]["exp"], marsh=v["marsh_none"]["exp"],
                                                    river=v["river_none"]["exp"], wharf=g["wharf"],
                                                    oyster=v["oyster_none"]["exp"])),
    }
    F["routes"] = routes
    F["route_exp"] = {
        "marsh straight line": {"marsh": r1(v["marsh_linear"]["exp"]), "oyster": r1(v["oyster_linear"]["exp"])},
        "river one offset": {"river": r1(v["river_pooled"]["exp"])},
        "no transfer, drain rim (quick)": {"front": r1(v["front_rim"]["exp"]), "marsh": r1(v["marsh_none"]["exp"]),
                                           "river": r1(v["river_none"]["exp"]), "oyster": r1(v["oyster_none"]["exp"])},
    }
    F["harbor_count_trend"] = r1(v["harbor_count_trend"])
    F["harbor_poisson"] = [int(x) for x in v["harbor_poisson_range"]]
    F["harbor_raw_skew"] = r1(v["harbor_raw_skew"])
    F["harbor_month_detrend"] = r1(v["harbor_month_detrend"])
    # bands: the defensible family (alignments, the residual detrending, the marsh forms, the river forms)
    def span(vals, pad=0.0):
        return [float(round(min(vals) - pad, 2)), float(round(max(vals) + pad, 2))]
    fams = list(fam.values())
    B = {"harbor_exp": span([f["harbor"] for f in fams], 0.5),
         "harbor_lo": span([f[k] for f in fams for k in f if k.startswith("harbor_lo")], 0.5),
         "harbor_hi": span([f[k] for f in fams for k in f if k.startswith("harbor_hi")], 0.5)}
    for k in A.ORDER:
        vals = [f[k] for f in fams]
        if k in ("marsh", "oyster"):
            vals += alt[k + "_exp"]
        if k == "river":
            vals += [v["river_lin"]["exp"], v["river_pow"]["exp"]]
        B["exp_" + k] = span(vals, 0.5)
    hb = {"front": [F["hind"]["front"]], "wharf": [F["hind"]["wharf"]],
          "marsh": alt["marsh_hind"] + [F["hind"]["marsh"]], "oyster": alt["oyster_hind"] + [F["hind"]["oyster"]],
          "river": [v["river_lin"]["hind"], v["river_pow"]["hind"], F["hind"]["river"]]}
    for k, vals in hb.items():
        B["hind_" + k] = [min(vals) - 1, max(vals) + 1]
    B["front_level_navd88"] = [round(F["front_level_navd88"] - 0.03, 2), round(F["front_level_navd88"] + 0.03, 2)]
    B["bridge"] = {k: [F["bridge_range"][k][0] - 0.3, F["bridge_range"][k][1] + 0.3] for k in ("sea", "tides", "weather")}
    B["bridge"]["total"] = [F["bridge"]["total"] - 1.0, F["bridge"]["total"] + 1.0]
    B["pair_hold"] = [F["pair_hold"] - 2, F["pair_hold"] + 2]
    F["bands"] = B
    return F


def effort(F, R):
    v = R["var"]
    B = F["bands"]
    n = A.NAMES
    hind_careful = dict(F["hind"], marsh=v["marsh_linear"]["hind"], oyster=v["oyster_linear"]["hind"], river=v["river_pooled"]["hind"])
    exp_careful = dict(F["exp"], marsh=r1(v["marsh_linear"]["exp"]), oyster=r1(v["oyster_linear"]["exp"]),
                       river=r1(v["river_pooled"]["exp"]))
    vals = R["bridge_vals"]
    base = vals["25|25|25"]
    oat = {"sea": r1(vals["plan|25|25"] - base), "tides": r1(vals["25|27|25"] - base), "weather": r1(vals["25|25|clim"] - base)}
    oat["total"] = r1(sum(oat.values()))
    res = [
        dict(id="R1", name="the harbor gauge's expected days at its minor flood threshold, 2027-28", graded_as="Ask 1",
             figure="harbor_exp", depends=[], independent="", golden=F["harbor_exp"], band=B["harbor_exp"],
             partly=[B["harbor_exp"][0] - 3, B["harbor_exp"][1] + 3],
             passes={"quick": F["harbor_count_trend"], "careful": F["harbor_exp"], "thorough": F["harbor_exp"]}),
        dict(id="R2", name="its 90 per cent range over the weather years", graded_as="Ask 2", figure="harbor_range",
             depends=["R1"], independent="", golden={"lo": F["harbor_lo"], "hi": F["harbor_hi"]},
             bands={"lo": B["harbor_lo"], "hi": B["harbor_hi"]},
             passes={"quick": None, "careful": {"lo": F["harbor_poisson"][0], "hi": F["harbor_poisson"][1]},
                     "thorough": {"lo": F["harbor_lo"], "hi": F["harbor_hi"]}}),
        dict(id="R3", name="the harbor's change from 2025-26 split into sea level, tides and weather", graded_as="Ask 3",
             figure="bridge", depends=["R1"], independent="", golden=F["bridge"], bands=B["bridge"],
             passes={"quick": None, "careful": oat, "thorough": F["bridge"]}),
        dict(id="R4", name="Front Street's 2025-26 tidal flood days from its street sensor", graded_as="Component 3",
             figure="front_hind", depends=[], independent="the street sensor and the harbor's verified high waters",
             golden=F["hind"]["front"], band=B["hind_front"],
             passes={"quick": v["front_rim"]["hind"], "careful": F["hind"]["front"], "thorough": F["hind"]["front"]}),
        dict(id="R5", name="Marsh Road's and Oyster Creek Road's 2025-26 days through their overmarsh transfers",
             graded_as="Component 1", figure="marsh_hind", depends=[], independent="each campaign and the harbor's high waters",
             golden={"marsh": F["hind"]["marsh"], "oyster": F["hind"]["oyster"]},
             bands={"marsh": B["hind_marsh"], "oyster": B["hind_oyster"]},
             passes={"quick": {"marsh": v["marsh_none"]["hind"], "oyster": v["oyster_none"]["hind"]},
                     "careful": {"marsh": hind_careful["marsh"], "oyster": hind_careful["oyster"]},
                     "thorough": {"marsh": F["hind"]["marsh"], "oyster": F["hind"]["oyster"]}}),
        dict(id="R6", name="River Road's 2025-26 days through its flow-dependent transfer", graded_as="Component 2",
             figure="river_hind", depends=[], independent="the campaign, the river's daily flows and the harbor's high waters",
             golden=F["hind"]["river"], band=B["hind_river"],
             passes={"quick": v["river_none"]["hind"], "careful": hind_careful["river"], "thorough": F["hind"]["river"]}),
        dict(id="R7", name="the five low points' expected 2027-28 tidal flood days", graded_as="Ask 4", figure="exp",
             depends=["R1", "R4", "R5", "R6"], independent="", golden=F["exp"],
             bands={k: B["exp_" + k] for k in A.ORDER},
             passes={"quick": {k: r1(F["route_exp"]["no transfer, drain rim (quick)"].get(k, F["exp"][k])) for k in A.ORDER},
                     "careful": exp_careful, "thorough": F["exp"]}),
        dict(id="R8", name="the two low points funded", graded_as="Recommendation", figure="call_pair",
             depends=["R7"], independent="", golden=F["call_pair"],
             passes={"quick": F["routes"]["no transfer, drain rim (quick)"], "careful": F["routes"]["both (careful but hurried)"],
                     "thorough": F["call_pair"]}),
    ]
    # the careful but hurried pass's own pair and how often it holds on its own models
    res.append(dict(id="R9", name="how many of the 36 weather years keep the funded pair on top", graded_as="Ask 5",
                    figure="pair_hold", depends=["R7", "R8"], independent="", golden=F["pair_hold"], band=B["pair_hold"],
                    passes={"quick": None, "careful": int(R["var"].get("careful_pair_hold", 0)), "thorough": F["pair_hold"]}))
    hints = [
        {"sentence": "River Road's high waters ride on the river's flow, and its campaign sat in a wet late winter", "rescues": ["R6"]},
        {"sentence": "Marsh Road's creek rises ever more slowly once the tide tops the marsh", "rescues": ["R5"]},
        {"sentence": "the harbor's days cluster within a year, so its range comes from the weather years, not a Poisson count",
         "rescues": ["R2"]},
    ]
    routes = [dict(name=k, answer=v_, golden=(k == "golden")) for k, v_ in F["routes"].items()]
    return {"results": res, "hints": hints, "routes": routes}


def write(R, gen_dir=HERE):
    F = make(R)
    F["harbor_range"] = {"lo": F["harbor_lo"], "hi": F["harbor_hi"]}
    F["front_hind"] = F["hind"]["front"]
    F["marsh_hind"] = {"marsh": F["hind"]["marsh"], "oyster": F["hind"]["oyster"]}
    F["river_hind"] = F["hind"]["river"]
    E = effort(F, R)
    json.dump(F, open(os.path.join(gen_dir, "figures.json"), "w"), indent=1, sort_keys=True)
    json.dump(E, open(os.path.join(gen_dir, "effort.json"), "w"), indent=1)
    return F, E
