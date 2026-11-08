"""task3 architecture 4: submission.md (the four platform blocks) and generator/figures.json, every figure from the
solution and the rungs on the cut pack."""
import math

import numpy as np

import golden as G
import params as P
import solve as S


def mg(x):
    return int(math.floor(x + 0.5))


def c(n):
    return "{:,}".format(int(n))


def figures(g, R):
    D = g["D"]
    fit = g["fit"]
    hi = max(P.WELLS, key=lambda w: g["fc"][w][2034])
    co = [r for r in G.cohort_rows(g) if r[9] is not None]
    pr = G.parcel_rows(g)
    ridge = [r for r in pr if r[7] is not None]
    epo = G.ep_observed(D)
    # the network's own recent clearings
    recent = []
    for sid, s in D["sites"].items():
        h = D["lc"][s["pid"]]
        ch = [y for y in range(2013, 2027) if h[y] in P.IRRIGATED and h[y - 1] not in P.IRRIGATED]
        if ch:
            recent.append((sid, s["dtw"], ch[0]))
    irv_pre = float(np.mean([v for y, v in g["curves_full"]["IRV"]["val"].items() if 1986 <= y <= 1995]))
    F = {
        "call": g["call"], "cross": g["cross"], "cycle_alt": 2031, "in_service": dict((str(k), v) for k, v in P.CYCLES.items()),
        "ep2034": round(g["ep"][2034], 2), "ep2034_int": mg(g["ep"][2034]), "ep2040_int": mg(g["ep"][2040]),
        "ep": {str(y): round(v, 2) for y, v in g["ep"].items()},
        "hi_well": hi, "hi_well_name": P.WELL_NAMES[hi], "hi_2034": round(g["fc"][hi][2034], 2),
        "hi_2034_int": mg(g["fc"][hi][2034]),
        "w2034": {w: round(g["fc"][w][2034], 2) for w in P.WELLS},
        "w6_2034_int": mg(g["fc"]["W6"][2034]), "w7_2034_int": mg(g["fc"]["W7"][2034]),
        "a": round(fit["a"], 2), "b": round(fit["b"], 2), "b3": round(fit["b"], 3), "n": fit["n"],
        "fit_rmse": round(fit["rmse"], 1),
        "cohort_years": [min(r[3] for r in co), max(r[3] for r in co)],
        "cohort_dtw": [min(r[2] for r in co), max(r[2] for r in co)],
        "cohort_delay_ends": [round(co[0][9], 1), round(co[-1][9], 1)],
        "cohort_mean_delay": round(float(np.mean([r[9] for r in co])), 1),
        "wt_age_max": round(max(D["ages"].values()), 2),
        "recent_n": len(recent), "recent_dtw": [int(min(r[1] for r in recent)), int(max(r[1] for r in recent))],
        "recent_years": [min(r[2] for r in recent), max(r[2] for r in recent)],
        "ridge_n": len(ridge), "ridge_acres": int(round(sum(r[2] for r in ridge))),
        "ridge_dtw": [int(min(r[3] for r in ridge)), int(max(r[3] for r in ridge))],
        "ridge_years": [min(r[7] for r in ridge), max(r[7] for r in ridge)],
        "ridge_T": [min(r[4] for r in ridge), max(r[4] for r in ridge)],
        "ridge_delay": [round(min(r[8] for r in ridge), 1), round(max(r[8] for r in ridge), 1)],
        "arrive_lo": int(math.floor(min(r[9] for r in ridge))), "arrive_hi": int(math.floor(max(r[9] for r in ridge))),
        "arrive_range": [round(min(r[9] for r in ridge), 1), round(max(r[9] for r in ridge), 1)],
        "wt_arrive_lo": int(math.floor(min(r[7] + r[8] for r in ridge))),
        "irv": round(g["curves"]["IRV"]["last"], 1), "irv_int": mg(g["curves"]["IRV"]["last"]),
        "irc": round(g["curves"]["IRC"]["last"], 1), "irv_pre_int": mg(irv_pre),
        "ep_obs_2010": round(epo[2012] if 2010 not in epo else epo[2010], 1), "ep_obs_first_year": min(epo),
        "ep_obs_2025": round(epo[2025], 1),
        "single_lag": round(R["rung1_single_lag"]["lag"], 1),
        "rung0_ep2034": round(float(R["rung0_trend"]["ep"]["2034"]), 1),
        "rung1_ep2034": round(float(R["rung1_single_lag"]["ep"]["2034"]), 1),
        "rung1_k": {k: R[k]["k"] for k in ("rung1_gw_travel_time", "rung1_pooled_cohort_delay", "rung1_single_lag")},
        "rung1_misfit": R["rung1_gw_travel_time"]["misfit_2026_k1"],
        "rung1_lag_misfit": R["rung1_single_lag"]["misfit_2026_k1"],
        "golden_sse": R["golden"]["sse_2019_2026"],
        "pooled_delay": R["rung1_pooled_cohort_delay"]["a"],
        "area_w_2034": round(R["area_weights"]["w2034"][hi], 1),
        "allyears_irv": round(R["leach_all_years"]["irv"], 1),
        "rmse": {w: round(v, 2) for w, v in g["rmse"].items()},
        "cohort_dtw_most": [min(sorted(r[2] for r in co)[:-3]), max(sorted(r[2] for r in co)[:-3])],
        "w67_obs": [round(g["obs"]["W6"][2010], 1), round(g["obs"]["W7"][2010], 1), round(g["obs"]["W6"][2026], 1),
                    round(g["obs"]["W7"][2026], 1)],
        "shares": P.PLAN_SHARE,
        "share_pct": [round(100 * P.PLAN_SHARE[w]) for w in P.WELLS],
        "no3_per_n": P.NO3_PER_N, "point_rename_year": 2014,
        "resid_range": [round(min(g["resid"].values()), 2), round(max(g["resid"].values()), 2)],
    }
    return F


def submission(g, R, F, path):
    L = []
    A = L.append
    A("## Tags")
    A("")
    A("> **Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (physical-model calibration "
      "and data assimilation, spatiotemporal exposure: a well field's nitrate forecast from the land over it).")
    A("> **Analytical objective:** Forecasting & Predictive Modeling.")
    A("")
    A("## 1. Final Recommendation")
    A("")
    A("**Put Project NR-1 on the 2027 cycle.** The entry point's annual mean nitrate first reaches 10 mg/L as N in "
      "%d and is about %d mg/L in 2034, so a plant funded in the 2031 cycle (in service 1 January %d) comes too late. "
      "Not the 2031 cycle: the wells' falling record, a trend on it, and every model fitted to it with the wellhead "
      "model's groundwater travel time or one lag for every parcel set the Sallow Ridge clearing's effect to nothing, "
      "because the ridge's leachate is still in the %d to %d ft of sand above the water table."
      % (F["cross"], F["ep2034_int"], P.CYCLES[2031], F["ridge_dtw"][0], F["ridge_dtw"][1]))
    A("")
    A("## 2. Supplementary Questions")
    A("")
    A("### corlinden_nitrate_plant_timing_memo.pdf")
    A("")
    A("1. Opens with the call (the 2027 cycle), the first year EP-01's annual mean reaches 10 mg/L as N (%d) and the "
      "2034 level (about %d), with a row of the forecast for 2027, 2029 to 2032, 2034 and 2040, then the chart."
      % (F["cross"], F["ep2034_int"]))
    A("2. Explains why the record looks safe (the wells fell from about %.1f mg/L at EP-01 in %d to %.1f in 2025 and "
      "show no rise where the travel time or the wells' own lag says the ridge should already show) and why the rise "
      "is coming (the unsaturated delay read from the county's matured conversions, carried to each ridge parcel's "
      "depth), with what the forecast rests on." % (F["ep_obs_2010"], F["ep_obs_first_year"], F["ep_obs_2025"]))
    A("")
    A("### corlinden_entry_point_nitrate_forecast.xlsx")
    A("")
    A("3. Sheet Forecast: one row per year 2027 to 2040 with each well's forecast, the plan's shares (Well 3 %d, "
      "Well 5 %d, Well 6 %d, Well 7 %d per cent) and EP-01's annual mean, flagged at or above 10 from %d."
      % (round(100 * P.PLAN_SHARE["W3"]), round(100 * P.PLAN_SHARE["W5"]), round(100 * P.PLAN_SHARE["W6"]),
         round(100 * P.PLAN_SHARE["W7"]), F["cross"]))
    A("4. Sheets Unsaturated delay (the %d matured conversions, each one's half-way arrival and delay, the fit "
      "a + b x depth with b = %.2f years a foot), Leachate (each land cover's current level and the land-surface-year "
      "record), Protection area parcels (each parcel's delay and, for the ridge, its arrival at the well) and Wells "
      "record (observed against the model, 1990 to 2026)." % (F["n"], F["b"]))
    A("")
    A("### corlinden_entry_point_nitrate_2027-2040.png")
    A("")
    A("5. EP-01's annual mean from %d to 2026 (record) and 2027 to 2040 (forecast) against a dashed 10 mg/L line, "
      "with the two cycles' in-service dates marked; the forecast steps from about %.0f in 2030 to past 10 in %d."
      % (F["ep_obs_first_year"], g["ep"][2030], F["cross"]))
    A("")
    A("### Answers the Council asked for")
    A("")
    A("6. First year EP-01's annual mean reaches 10 mg/L as N: %d." % F["cross"])
    A("7. EP-01's 2034 annual mean: %d mg/L as N." % F["ep2034_int"])
    A("8. Well with the highest 2034 annual mean: %s, at %d mg/L as N." % (F["hi_well_name"], F["hi_2034_int"]))
    A("")
    A("## 3. Critical Components")
    A("")
    A("1. The county's %d network wells put under irrigation between %d and %d stepped up after a delay that grows "
      "with depth to water, **%.2f years a foot** (about %.0f year at %d ft to %.0f at %d ft), while their water-table "
      "ages are under half a year: the delay is in the unsaturated sand, and the wellhead model's travel time starts "
      "below it." % (F["n"], F["cohort_years"][0], F["cohort_years"][1], F["b"], F["cohort_delay_ends"][0],
                     F["cohort_dtw"][0], F["cohort_delay_ends"][1], F["cohort_dtw"][1]))
    A("2. The Sallow Ridge parcels cleared for irrigated vegetables in %d to %d (%s acres, %d to %d ft to water, %.0f "
      "to %.0f years' groundwater travel from Wells 6 and 7) send their leachate to the wells **around the start of %d**; with "
      "the travel time alone, or the one lag of about %.1f years that fits the wells' record, it would already show, "
      "and fitting the record then sets the clearing's effect to nil."
      % (F["ridge_years"][0], F["ridge_years"][1], c(F["ridge_acres"]), F["ridge_dtw"][0], F["ridge_dtw"][1],
         F["ridge_T"][0], F["ridge_T"][1], F["arrive_lo"] + 1, F["single_lag"]))
    A("3. Water under irrigated vegetables now carries about **%d mg/L as N** (the land-surface years since nutrient "
      "management; about %d before it), mixed into each well by its parcels' recharge at the time the water left the "
      "water table." % (F["irv_int"], F["irv_pre_int"]))
    A("4. EP-01 first reaches **10 mg/L in %d** and is **%d mg/L in 2034**; %s is highest, at **%d mg/L**."
      % (F["cross"], F["ep2034_int"], F["hi_well_name"], F["hi_2034_int"]))
    A("")
    A("## 4. Step-by-Step")
    A("")
    A("1. Read corlinden_raw_water_nitrate_results_1988-2026.csv as nitrate-N (county laboratory results before 2004 "
      "reported as nitrate, divided by 4.427; field duplicates and re-runs averaged; the 2014 point names mapped): "
      "EP-01 fell from %.1f mg/L in %d to %.1f in 2025, Wells 6 and 7 from %.1f and %.1f in 2010 to %.1f and %.1f in "
      "2026." % (F["ep_obs_2010"], F["ep_obs_first_year"], F["ep_obs_2025"], F["w67_obs"][0], F["w67_obs"][1],
                 F["w67_obs"][2], F["w67_obs"][3]))
    A("2. A trend on each well, blended by the plan's shares, puts EP-01 near %.0f mg/L in 2034 and never at 10, so "
      "the 2031 cycle (the reasonable but insufficient reading of the record)." % F["rung0_ep2034"])
    A("3. In ravell_county_parcel_land_cover_1986-2026.csv (local codes to 2007, cropland-layer codes after; split and "
      "re-numbered parcels joined through parent_parcel_id) and sallow_road_WHPA_parcel_attributes_2019.xlsx, the "
      "Sallow Ridge parcels in the zones of Wells 6 and 7 turn from forest to irrigated vegetables in %d to %d. "
      "Taken at the wellhead model's groundwater travel time (%.0f to %.0f years), or at the one lag of %.1f years that "
      "best fits the wells' 1998 to 2018 record, the ridge would already have raised Well 6 by %.0f mg/L in 2026; "
      "fitted to the 2019 to 2026 record the clearing's effect comes out at %.0f per cent, and the forecast stays "
      "near %.0f mg/L: the same 2031 cycle." % (F["ridge_years"][0], F["ridge_years"][1], F["ridge_T"][0],
                                               F["ridge_T"][1], F["single_lag"], F["rung1_lag_misfit"]["W6"],
                                               100 * F["rung1_k"]["rung1_single_lag"], F["rung1_ep2034"]))
    A("4. In ravell_county_groundwater_network_samples_1990-2026.csv with the sites workbook (two rebuilt wells' old "
      "numbers carried to the new), the %d wells whose land went under irrigation in %d to %d each step up from their "
      "earlier level; the half-way arrival less the year irrigation began and the well's tritium-helium age "
      "(ravell_county_groundwater_age_survey_2019.xlsx) gives the delay to the water table, which fits a + b x "
      "depth with b = %.3f years a foot (residual %.1f years). Their average delay, %.1f years, is the wrong number for "
      "the ridge: all but three of the matured conversions sit on %d to %d ft of sand, the ridge on %d to %d."
      % (F["n"], F["cohort_years"][0], F["cohort_years"][1], F["b3"], F["fit_rmse"], F["cohort_mean_delay"],
         F["cohort_dtw_most"][0], F["cohort_dtw_most"][1], F["ridge_dtw"][0], F["ridge_dtw"][1]))
    A("5. The network's %d wells under the %d to %d upland clearings (%d to %d ft to water) show no rise yet, as the "
      "fit says: absence here is the leachate not yet arrived, not the land leaching nothing."
      % (F["recent_n"], F["recent_years"][0], F["recent_years"][1], F["recent_dtw"][0], F["recent_dtw"][1]))
    A("6. Each land cover's leachate by land-surface year from the network's wells on unchanged land (each sample "
      "dated back by its own age and delay): irrigated vegetables %.1f and irrigated corn and soybean %.1f mg/L in the "
      "latest five years, against about %d for vegetables before nutrient management." % (F["irv"], F["irc"],
                                                                                      F["irv_pre_int"]))
    A("7. Each protection-area parcel reaches its well after its own delay and its groundwater travel time, mixed by "
      "acres times the recharge it had when the water left the water table (sallow_road_WHPA_parcel_attributes_2019"
      ".xlsx, Recharge), each well's model carried to its 2019-2026 level (residuals %.2f to %.2f mg/L), and the wells "
      "blended by corlinden_water_supply_plan_2025.pdf's shares with land cover held at 2026: the ridge reaches the wells "
      "around the start of %d, EP-01 passes 10 in %d and is %d mg/L in 2034, %s at %d."
      % (min(g["resid"].values()), max(g["resid"].values()), F["arrive_lo"] + 1, F["cross"],
         F["ep2034_int"], F["hi_well_name"], F["hi_2034_int"]))
    A("")
    A("No other conclusion survives. The record, a trend on it and any fit to it read the ridge's absence as no "
      "effect, but every delay that would put the leachate at the wells by 2026 (the travel time alone, one lag for "
      "every parcel, the matured conversions' average) also predicts the rise at the county's three upland clearings, "
      "which the depth-specific delay alone explains; and under the delay that fits the matured conversions, the "
      "2019 to 2026 record is silent on the clearing (its fit is the same at none of the effect and all of it). Read "
      "as a fitted step, through the origin, without the water-table age, or uncarried to the wells' level, the first "
      "year at 10 stays %d and the 2034 entry point %d mg/L, well before 2034. Mixing by acres alone, though the "
      "wellhead model's recharge differs by land cover, puts %s at %.0f (or, weighting by the recharge at the time the "
      "nitrate left the root zone and carrying that model to the wells' level, which reads the ridge's early dilution as "
      "bias, the same); taking vegetable leachate over all years (%.0f mg/L) overstates it; neither moves the cycle." % (F["cross"], F["ep2034_int"], F["hi_well_name"],
                                                                     F["area_w_2034"], F["allyears_irv"]))
    open(path, "w").write("\n".join(L) + "\n")
