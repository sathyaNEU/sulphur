"""task23 architecture 1: the graded results computed from the cut pack under the golden and each pass's route,
figures.json (what the answer blocks state) and effort.json (what effort.py scores), with the routes, the hints, the
stump factorial and the forcing on both sides."""
import json
import math
import os

import numpy as np

import analysis as A
import params as P

PK = list(P.PACKAGES)
REFLEX = dict(baro="none", kwet=False, r3="collected", ox="mean")
ROUTES = {"golden": {}, "careful": dict(REFLEX)}
STUMPS = [
    ("J1", "the recirculated decay read on the wells the leachate did not flood, carried to cell 5 from July 2026",
     dict(kwet=False, r3="collected"), dict(kwet=True, r3="zones"), ["L02", "L26", "N04"],
     "cell 4's flat collected gas read as no change in its decay; cell 5 carried at the dry decay"),
    ("J2", "the campaigns and drone flights carried to every hour through the pressure response the chambers record",
     dict(baro="none"), dict(baro="ema"), ["N12", "L28"],
     "the campaigns' mean rate times the year's hours, confirmed by the drone flights"),
    ("J3", "the cover's oxidation evaluated at each cell's own flux",
     dict(ox="mean"), dict(ox="sat"), ["N04", "L22"], "the 2019 study's mean share for each cover"),
]
REFLEXES = [("J4", "the forecast built cell by cell, each package acting on its own cell", ["R25"]),
            ("J5", "the greenhouse gas report's figure reproduced from its own equation", ["R18"]),
            ("J6", "the pilot pumps' gain read from the pumped wells' flows", ["R14"]),
            ("J7", "the tickets' voids, reissues and missing cell codes", ["R01"])]
FAMILY = [("the golden: an exponential pressure lag fitted on both soil-cover chambers, the state's campaigns, cell 5 "
           "calibrated on its spring 2026 campaigns, a saturating oxidation", {}),
          ("the pressure lag fixed at 12 hours", dict(baro="ema_tau12")),
          ("the pressure lag fixed at 20 hours", dict(baro="ema_tau20")),
          ("cell 4's chamber alone", dict(baro="ema_ac1")),
          ("the campaigns and the drone flights weighted by their uncertainty", dict(level="tcm_drone")),
          ("oxidation as a logistic in the log of the flux", dict(ox="loglin")),
          ("cell 5 on cell 4's methane potential", dict(c5="waste")),
          ("the faster decay ramped in over three months", dict(ramp=3)),
          ("the faster decay ramped in over six months", dict(ramp=6)),
          ("package C's gain as the pilot's mean flow ratio", dict(pumps="ratio")),
          ("the level set by the closed cells' collected gas at the closure plan's design collection",
           dict(calib="closed")),
          ("all three chambers pooled in the pressure fit", dict(baro="ema_all")),
          ("oxidation as a capacity with its own half-saturation flux", dict(ox="mm")),
          ("cell 4's collection efficiency held at its August to October 2026 level", dict(ce4="flat"))]
SHORTCUTS = [("the careful but hurried route", dict(REFLEX)),
             ("no pressure correction", dict(baro="none")),
             ("one decay for every cell", dict(kwet=False, r3="collected")),
             ("the study's cover-type oxidation", dict(ox="mean")),
             ("the reporting rule's 10 per cent oxidation", dict(ox="default")),
             ("no pressure correction and one decay", dict(baro="none", kwet=False, r3="collected")),
             ("no pressure correction and the study's oxidation", dict(baro="none", ox="mean")),
             ("one decay and the study's oxidation", dict(kwet=False, r3="collected", ox="mean")),
             ("the rule's default decay and potential, uncalibrated, with the study's oxidation",
              dict(calib="rule", kd_scale="rule", kwet=False, r3="collected", ox="mean")),
             ("the rule's default potential, uncalibrated, with both decay rates and a saturating oxidation",
              dict(calib="rule")),
             ("the rule's default potential, uncalibrated, with both decay rates and the study's oxidation",
              dict(calib="rule", ox="mean")),
             ("the closed cells' level with both decay rates and the study's oxidation",
              dict(calib="closed", ox="mean"))]
PERTURB = [("the campaigns' pressure factor +0.03", dict(corr_shift=0.03)),
           ("the campaigns' pressure factor -0.03", dict(corr_shift=-0.03)),
           ("the recirculated decay rate +8 per cent", dict(kw_scale=1.08)),
           ("the recirculated decay rate -8 per cent", dict(kw_scale=0.92)),
           ("the dry decay rate +10 per cent", dict(kd_scale=1.10)),
           ("the dry decay rate -10 per cent", dict(kd_scale=0.90)),
           ("the covers' oxidation capacity +15 per cent", dict(v_scale=1.15)),
           ("the covers' oxidation capacity -15 per cent", dict(v_scale=0.85)),
           ("package C's pump gain +20 per cent", dict(gain_scale=1.2)),
           ("package C's pump gain -20 per cent", dict(gain_scale=0.8)),
           ("cell 5's spring calibration +7 per cent", dict(s5_scale=1.07)),
           ("cell 5's spring calibration -7 per cent", dict(s5_scale=0.93))]
HINTS = [("Cell 4's collected gas is flat because the leachate that sped its decay also flooded its lower wells; the "
          "wells it did not flood show the faster decay.", dict(kwet=True, r3="zones")),
         ("Waste holds gas while the barometer rises and lets it out as it falls, and the campaigns only fly on "
          "settled days after fronts.", dict(baro="ema")),
         ("A cover oxidizes a nearly fixed amount per square metre, so the share it oxidizes falls as the flux "
          "through it rises.", dict(ox="sat"))]


def ans(R8):
    """The package a route picks, as the answer blocks name it."""
    return "no package" if R8 in (None, "none") else "package %s" % R8


def figures(R):
    f = {}
    f["R1_cell5_msw_tons"] = round(R["R1"])
    f["R2_actual_2025_t"] = round(R["R2"])
    f["R3_cell4_generation_change_pct"] = round(R["R3"], 1)
    f["R4_cell5_generation_2027_t"] = round(R["R4"])
    f["R5_cell5_oxidized_share_2027_pct"] = round(R["R5"], 1)
    b = R["R6"]
    f["R6_bridge"] = {"collection efficiency": round(b["collection"]), "oxidation": round(b["oxidation"]),
                      "the hours the campaigns did not sample": round(R["R2"]) - round(b["survey"])}
    f["R7_emissions_2027_t"] = {"package %s" % p: round(R["R7"][p]) for p in PK}
    f["R8_package"] = ans(R["R8"])
    return f


def band_scalar(key, v):
    return {"R1_cell5_msw_tons": (v * 0.99, v * 1.01), "R2_actual_2025_t": (v * 0.90, v * 1.10),
            "R3_cell4_generation_change_pct": (v - 8.0, v + 8.0), "R4_cell5_generation_2027_t": (v * 0.88, v * 1.12),
            "R5_cell5_oxidized_share_2027_pct": (v - 4.0, v + 4.0)}[key]


def partly_scalar(key, v):
    return {"R1_cell5_msw_tons": (v * 0.97, v * 1.03), "R2_actual_2025_t": (v * 0.80, v * 1.20),
            "R3_cell4_generation_change_pct": (v - 16.0, v + 16.0), "R4_cell5_generation_2027_t": (v * 0.75, v * 1.25),
            "R5_cell5_oxidized_share_2027_pct": (v - 8.0, v + 8.0)}[key]


GAP_HALF_T = 490.0   # the survey's gap is the actual emission less a filed figure: R2's band (10 per cent) carried


def band_cell(key, k, v):
    if key == "R6_bridge":
        if k == "oxidation":
            return (v - 250.0, v + 250.0)
        if k == "the hours the campaigns did not sample":
            return (v - GAP_HALF_T, v + GAP_HALF_T)
        return (v * 0.85, v * 1.15)
    return (v * 0.93, v * 1.07)


META = [
    ("R1", "the municipal waste placed in cell 5 through October 2026, in short tons", "R1_cell5_msw_tons", "Ask 3", [], "the scale tickets and the daily log", None),
    ("R2", "the site's actual methane emission in 2025, metric tons", "R2_actual_2025_t", "Component 1", [],
     "the campaigns, the drone flights, the chambers and the barometer", ["N12", "L28"]),
    ("R3", "the per cent change in cell 4's methane generation from 2022 to the twelve months to October 2026",
     "R3_cell4_generation_change_pct", "Component 2", [], "the wellfield readings, the register and the pump work orders",
     ["L02", "L26"]),
    ("R4", "the methane cell 5 will generate in 2027, metric tons", "R4_cell5_generation_2027_t", "Ask 5", ["R1", "R3"], "",
     ["L11", "L02", "N04"]),
    ("R5", "the share of the methane reaching cell 5's cover in 2027 that it oxidizes, per cent",
     "R5_cell5_oxidized_share_2027_pct", "Ask 6", ["R4"], "", ["N04", "L22"]),
    ("R6", "the bridge from the 2025 report and the survey to the actual 2025 emission, metric tons", "R6_bridge",
     "Ask 2", ["R2"], "", ["N12", "L22"]),
    ("R7", "the 2027 emission under each package in a year of normal weather, metric tons", "R7_emissions_2027_t",
     "Component 3", ["R2", "R4", "R5"], "", ["L11", "N12", "N04", "L22"]),
    ("R8", "the cheapest package that keeps 2027 at or under the limit", "R8_package", "Recommendation", ["R7"], "",
     ["N12", "N04", "L22"]),
]


def quick_figures(F, Rg):
    """The ten-minute pass: the tickets summed as filed, the report's figure taken as the emission, cell 4's collected
    gas, cell 5 on the rule's default decay, the rule's 10 per cent oxidation, no bridge, no forecast."""
    pot = A.waste_potential(F, "raw")
    g5, _ = A.fod(pot[5], P.RULE["k_default"], P.RULE["k_default"], 0.0, None)
    y27 = slice(A.mi(2027, 1), A.mi(2028, 1))
    rep = Rg["R6"]["report"]
    f = {}
    f["R1_cell5_msw_tons"] = round(A.r1_cell5_msw(F, "raw"))
    f["R2_actual_2025_t"] = round(rep)
    f["R3_cell4_generation_change_pct"] = round(Rg["_r3_collected"], 1)
    f["R4_cell5_generation_2027_t"] = round(float(g5[y27].sum()) * P.RHO_CH4)
    f["R5_cell5_oxidized_share_2027_pct"] = 10.0
    f["R6_bridge"] = {"collection efficiency": 0, "oxidation": 0, "the hours the campaigns did not sample": 0}
    f["R7_emissions_2027_t"] = {"package %s" % p: round(rep) for p in PK}
    f["R8_package"] = "package A"
    return f


def _inside(v, b):
    return b[0] <= v <= b[1]


def grade(key, golden, val):
    if isinstance(golden, str):
        return "right" if golden == val else "missed"
    if isinstance(golden, dict):
        ins = [_inside(val[k], band_cell(key, k, golden[k])) for k in golden]
        if all(ins):
            return "right"
        return "partly" if np.mean(ins) >= 0.5 else "missed"
    if _inside(val, band_scalar(key, golden)):
        return "right"
    return "partly" if _inside(val, partly_scalar(key, golden)) else "missed"


def run_all(F):
    cache = {}
    out = {k: A.run(F, o, cache) for k, o in ROUTES.items()}
    out["golden"]["_r3_collected"] = A.run(F, dict(r3="collected"), cache)["R3"]
    fam = [(n, A.run(F, o, cache)) for n, o in FAMILY]
    sc = [(n, A.run(F, o, cache)) for n, o in SHORTCUTS]
    pt = [(n, A.run(F, o, cache)) for n, o in PERTURB]
    drops = [(j, A.run(F, d, cache)) for j, _, d, _, _, _ in STUMPS]
    alones = []
    for j, _, _, fx, _, _ in STUMPS:
        o = dict(REFLEX)
        o.update(fx)
        alones.append((j, A.run(F, o, cache)))
    hints = []
    for sent, o in HINTS:
        oo = dict(REFLEX)
        oo.update(o)
        hints.append((sent, A.run(F, oo, cache)))
    return out, fam, sc, pt, drops, alones, hints, cache


def write(F, gen_out):
    out, fam, sc, pt, drops, alones, hints, cache = run_all(F)
    Rg = out["golden"]
    G = figures(Rg)
    Cf = figures(out["careful"])
    Qf = quick_figures(F, Rg)
    res = []
    for rid, name, fig, graded, dep, indep, prec in META:
        g = G[fig]
        r = dict(id=rid, name=name, graded_as=graded, figure=fig, depends=dep, independent=indep, golden=g)
        if isinstance(g, dict):
            r["bands"] = {k: [round(x, 1) for x in band_cell(fig, k, v)] for k, v in g.items()}
            r["partly_share"] = 0.5
        elif not isinstance(g, str):
            r["band"] = [round(x, 2) for x in band_scalar(fig, g)]
            r["partly"] = [round(x, 2) for x in partly_scalar(fig, g)]
        r["passes"] = {"quick": Qf[fig], "careful": Cf[fig], "thorough": g}
        if prec:
            r["precedent"] = prec
        res.append(r)

    def rescued(R):
        h = figures(R)
        return [rid for rid, _, fig, *_ in META if grade(fig, G[fig], h[fig]) == "right"
                and grade(fig, G[fig], Cf[fig]) != "right"]
    hint_rows = [dict(sentence=s, rescues=rescued(R)) for s, R in hints]
    routes = [dict(name="the golden", answer=ans(Rg["R8"]), golden=True)]
    routes += [dict(name=n, answer=ans(R["R8"])) for n, R in sc]
    routes.append(dict(name="the quick pass", answer=Qf["R8_package"]))
    forcing = dict(kind="set", line="the Council's 2027 limit of %s metric tons" % "{:,.0f}".format(P.LIMIT_T),
                   golden_answer=ans(Rg["R8"]),
                   golden_family=[dict(name=n, answer=ans(R["R8"])) for n, R in fam],
                   perturbations=[dict(input=n, answer=ans(R["R8"])) for n, R in pt],
                   shortcuts=[dict(name=n, answer=ans(R["R8"])) for n, R in sc])
    jud = []
    for (j, name, d, fx, prec, hurried), (_, Rd), (_, Ra) in zip(STUMPS, drops, alones):
        fd = figures(Rd)
        moved = [rid for rid, _, fig, *_ in META if grade(fig, G[fig], fd[fig]) != "right"]
        jud.append(dict(id=j, name=name, kind="stump", precedent=prec, hurried=hurried,
                        dropped={"answer": ans(Rd["R8"]), "results_moved": moved,
                                 "packages_t": {p: round(Rd["R7"][p]) for p in PK}},
                        alone={"answer": ans(Ra["R8"]), "results_rescued": rescued(Ra),
                               "packages_t": {p: round(Ra["R7"][p]) for p in PK}}))
    for j, name, prec in REFLEXES:
        jud.append(dict(id=j, name=name, kind="reflex", precedent=prec))
    factorial = dict(golden_answer=ans(Rg["R8"]),
                     reflex_route={"answer": ans(out["careful"]["R8"]),
                                   "packages_t": {p: round(out["careful"]["R7"][p]) for p in PK}},
                     judgments=jud)
    margins = {"limit_t": P.LIMIT_T,
               "golden": {p: round(Rg["R7"][p]) for p in PK},
               "family": {n: {p: round(R["R7"][p]) for p in PK} for n, R in fam},
               "perturbations": {n: {p: round(R["R7"][p]) for p in PK} for n, R in pt},
               "shortcuts": {n: {p: round(R["R7"][p]) for p in PK} for n, R in sc}}
    E = dict(results=res, hints=hint_rows, routes=routes, forcing=forcing, factorial=factorial, margins=margins,
             weights={"recommendation": 14, "components": 24, "asks": 55, "instruction": 7})
    figs = dict(G)
    figs["limit_t"] = P.LIMIT_T
    figs["report_2025_t"] = round(Rg["R6"]["report"])
    figs["survey_2025_t"] = round(Rg["R6"]["survey"])
    b = G["R6_bridge"]
    figs["residual_2025_t"] = G["R2_actual_2025_t"] - figs["report_2025_t"] - b["collection efficiency"] - b["oxidation"]
    figs["collected_2025_t"] = round(Rg["R6"]["collected_2025"])
    figs["generated_2025_t"] = round(Rg["R6"]["generated_2025"])
    figs["pressure_lag_h"] = Rg["baro"]["tau"]
    figs["pressure_coef_per_hpa"] = round(Rg["baro"]["c"], 3)
    figs["campaign_factor_2025"] = round(float(Rg["campaigns"][Rg["campaigns"]["date"].map(lambda d: d.year) == 2025]["m"].mean()), 3)
    figs["campaign_factor_2026"] = round(float(Rg["campaigns"][Rg["campaigns"]["date"].map(lambda d: d.year) == 2026]["m"].mean()), 3)
    figs["kd_per_year"] = round(Rg["kd"], 4)
    figs["kw_per_year"] = round(Rg["kw"], 4)
    figs["share_wet"] = round(Rg["share_wet"], 3)
    figs["r_dry"] = round(Rg["r_dry"], 3)
    figs["r_wet"] = round(Rg["r_wet"], 3)
    figs["ce4_now"] = round(Rg["ce4_now"], 3)
    figs["pump_gain_t_month"] = round(Rg["pump_gain_t_month"], 1)
    figs["careful_package"] = ans(out["careful"]["R8"])
    figs["careful_R7"] = {"package %s" % p: round(out["careful"]["R7"][p]) for p in PK}
    figs["drops"] = {j["id"]: j["dropped"]["answer"] for j in jud if j["kind"] == "stump"}
    figs["cells_2027_D"] = {"cell %d" % c: round(v) for c, v in Rg["R7_cells"]["D"].items()}
    figs["cells_2027_C"] = {"cell %d" % c: round(v) for c, v in Rg["R7_cells"]["C"].items()}
    figs["_extra"] = extra(F, Rg, out["careful"], fam, sc, pt, jud, cache)
    figs["_quick"] = Qf
    json.dump(figs, open(os.path.join(gen_out, "figures.json"), "w"), indent=1, default=str)
    json.dump(E, open(os.path.join(gen_out, "effort.json"), "w"), indent=1, default=str)
    return figs, E, out, cache


def extra(F, Rg, Rc, fam, sc, pt, jud, cache):
    """The supporting figures the answer blocks cite beside the graded ones, each computed here."""
    import pandas as pd
    c, d = Rg["campaigns"], Rg["drone"]
    y25c = c[pd.to_datetime(c["date"]).dt.year == 2025]
    y25d = d[pd.to_datetime(d["date"]).dt.year == 2025]
    y26c = c[pd.to_datetime(c["date"]).dt.year == 2026]
    ox_mean = A.ox_fit(F, "mean")["means"]
    sat = cache["OX_sat"]
    z = Rg["z"]
    x = {}
    x["drone_2025_t"] = round(float(y25d["flux_kg_h"].mean()) * 8.76)
    x["drone_2025_corr_t"] = round(float(y25d["flux_corr"].mean()) * 8.76)
    x["campaigns_2025"] = len(y25c)
    x["campaigns_2026"] = len(y26c)
    x["flights_2025"] = len(y25d)
    x["campaign_mean_2025_kg_h"] = round(float(y25c["site_kg_h"].mean()), 1)
    x["campaign_corr_2025_kg_h"] = round(float(y25c["site_corr"].mean()), 1)
    x["drone_factor_2025"] = round(float(y25d["m"].mean()), 3)
    x["hours_in_year"] = 8760
    x["study_mean_pct"] = {k: round(100 * v, 1) for k, v in ox_mean.items()}
    x["sat_v15_g_m2_d"] = {k: round(v, 1) for k, v in sat["v15"].items()}
    x["sat_q10"] = round(sat["q10"], 2)
    x["rule"] = {"ox_pct": round(100 * P.RULE["ox"]), "de": P.RULE["de"], "ce_2025": round(
        sum(a * P.RULE["ce"][k] for k, a in P.RULE_AREAS_2025.items()) / sum(P.RULE_AREAS_2025.values()), 4)}
    x["cell4"] = {"wells": z["n_wells"], "dry": z["n_dry"], "flooded": z["n_wet"], "pumped": z["n_pumped"],
                  "dry_change_pct": round(100 * (z["r_dry"] - 1), 1),
                  "pumped_change_pct": round(100 * (z["r_pump"] - 1), 1),
                  "pumped_full_yield_change_pct": round(100 * (z["r_wet"] - 1), 1),
                  "collected_change_pct": round(100 * (z["r_collected"] - 1), 1),
                  "share_reached_pct": round(100 * Rg["share_wet"], 1),
                  "yield_loss": round(z["L"], 2), "pumped_submergence": round(z["s_after"], 2)}
    x["decay"] = {"kd": round(Rg["kd"], 4), "kw": round(Rg["kw"], 4)}
    x["s5_over_s4"] = round(Rg["s5"] / Rg["s4"], 3)
    x["pressure"] = {"lag_h": Rg["baro"]["tau"], "coef_per_hpa": round(Rg["baro"]["c"], 3)}
    x["costs_usd_m"] = {"package %s" % p: P.PACKAGES[p]["cost"] for p in P.PACKAGES}
    x["careful"] = {"R1": round(Rc["R1"]), "R2": round(Rc["R2"]), "R3": round(Rc["R3"], 1), "R4": round(Rc["R4"]),
                    "R5": round(Rc["R5"], 1), "R7": {"package %s" % p: round(Rc["R7"][p]) for p in PK},
                    "R8": ans(Rc["R8"])}
    x["drops"] = {j["id"]: {"answer": j["dropped"]["answer"], "R7": {"package %s" % p: v for p, v in
                                                                     j["dropped"]["packages_t"].items()}}
                  for j in jud if j["kind"] == "stump"}
    x["shortcuts"] = {n: {"answer": ans(R["R8"]), "R7": {"package %s" % p: round(R["R7"][p]) for p in PK}}
                      for n, R in sc}
    x["family"] = {n: {"answer": ans(R["R8"]), "R7": {"package %s" % p: round(R["R7"][p]) for p in PK},
                       "R2": round(R["R2"]), "R3": round(R["R3"], 1), "R4": round(R["R4"]), "R5": round(R["R5"], 1),
                       "R6": {"collection efficiency": round(R["R6"]["collection"]),
                              "oxidation": round(R["R6"]["oxidation"]),
                              "the hours the campaigns did not sample": round(R["R6"]["survey_gap"])}}
                   for n, R in fam}
    lim = P.LIMIT_T
    famC = [(R["R7"]["C"], n) for n, R in fam] + [(R["R7"]["C"], n) for n, R in pt]
    famD = [(R["R7"]["D"], n) for n, R in fam] + [(R["R7"]["D"], n) for n, R in pt]
    cmin, dmax = min(famC), max(famD)
    x["nearest"] = {"C_min_t": round(cmin[0]), "C_min_pct": round(100 * (cmin[0] / lim - 1), 1), "C_name": cmin[1],
                    "C_over_t": round(cmin[0]) - round(lim),
                    "D_max_t": round(dmax[0]), "D_max_pct": round(100 * (1 - dmax[0] / lim), 1), "D_name": dmax[1]}
    x["perturbations"] = {n: {"answer": ans(R["R8"]), "C": round(R["R7"]["C"]), "D": round(R["R7"]["D"])}
                          for n, R in pt}
    closed = next(R for n, R in fam if n.startswith("the level set by the closed cells"))
    x["implied_l0_m3_per_ton"] = {"campaigns cell 4": round(P.L0_RULE["MSW"] * Rg["s4"] / P.RHO_CH4 * 0.90718474),
                                  "campaigns cell 5": round(P.L0_RULE["MSW"] * Rg["s5"] / P.RHO_CH4 * 0.90718474),
                                  "closed cells": round(P.L0_RULE["MSW"] * closed["s4"] / P.RHO_CH4 * 0.90718474)}
    x["plots"] = int(F["oxplots"]["plot_id"].nunique())
    x["ce4_zones"] = {k: round(v, 2) for k, v in Rg["ce4_zones"].items()}
    x["cell5_acres"] = float(F["cells"].set_index("cell").loc[5, "footprint_acres"])
    x["cell5_acres_2025_report"] = round(P.RULE_AREAS_2025["none"] / 4046.86, 1)
    x["bands"] = {"R1_pct": 1, "R2_pct": 10, "R3_points": 8, "R4_pct": 12, "R5_points": 4, "R6_collection_pct": 15,
                  "R6_oxidation_t": 250, "R6_survey_gap_t": round(GAP_HALF_T), "R7_pct": 7}
    x["ce4_cap_pct"] = round(100 * P.CE4_CAP)
    x["ce_closed_pct"] = round(100 * P.CE_CLOSED_DESIGN)
    x["s5_spread_pct"] = 7
    x["tau_rivals_h"] = [12, 20]
    x["tau_grid_h"] = [4, 48]
    return x
