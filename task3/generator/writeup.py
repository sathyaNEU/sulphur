"""task3 architecture 3: submission.md (the four platform blocks) and generator/figures.json, every figure taken
from the solution and the rungs computed on the cut pack."""
import json
import math

import solve as S


def ft(x):
    return int(math.floor(x + 0.5))


def c(n):
    return "{:,}".format(int(n))


def figures(g, rungs):
    th = rungs["rung0_theis"]
    cv = rungs["rung1_cv07"]
    raw = rungs["rung1_raw"]
    return {
        "call": g["call"], "call_text": "%s gpm" % c(g["call"]), "next": 1250, "limit": S.LIMIT,
        "peaks_ft": {str(r): ft(g["peaks"][r]) for r in S.OPTIONS},
        "peaks_2dp": {str(r): round(g["peaks"][r], 2) for r in S.OPTIONS},
        "msmw_2025_ft": ft(g["msmw_2025"]), "msmw_2025_2dp": round(g["msmw_2025"], 2),
        "dw_ft": ft(g["dw"]), "dw_2dp": round(g["dw"], 2), "dw_id": g["dw_id"],
        "dw_nowalls_ft": ft(rungs["walls_none"]["dw"]), "msmw_slip_ft": ft(rungs["msmw_anchor_slip"]),
        "T": int(round(g["T"], -1)), "T_text": c(round(g["T"], -1)), "S": "%.1e" % g["S"], "rms": round(g["rms"], 2),
        "q_avg": round(g["q_avg"]), "B": int(g["B"]), "B_text": c(g["B"]), "width": c(g["width"]),
        "theis_msmw_2025": ft(rungs["theis_msmw_2025"]),
        "theis_peak_450": ft(th["peaks"]["450"]),
        "cv07_B": c(round(cv["B"], -2)), "cv07_peaks_ft": {k: ft(v) for k, v in cv["peaks"].items()},
        "cv07_msmw": ft(cv["msmw_2025"]), "raw_msmw": ft(raw["msmw_2025"]),
        "raw_peak_top": ft(raw["peaks"]["1250"]), "cv07_peak_top": ft(cv["peaks"]["1250"]),
        "cv07_departure_2025": rungs["cv07_departure"]["2025"], "cv07_departure_2008": rungs["cv07_departure"]["2008"],
        "cv07_pump_corr": rungs["cv07_pump_corr"], "far_pair_pump_corr": rungs["far_pair_pump_corr"],
        "ows_far_pre_corr": rungs["ows_far_pre_corr"],
        "standing_1000_range": [min(rungs[k]["peaks"]["1000"] for k in rungs["standing"]),
                                max(rungs[k]["peaks"]["1000"] for k in rungs["standing"])],
        "standing_top_range": [min(rungs[k]["peaks"]["1250"] for k in rungs["standing"]),
                                max(rungs[k]["peaks"]["1250"] for k in rungs["standing"])],
        "ows_only_msmw": round(rungs["rival_ows_only"]["msmw_2025_model"], 1),
        "ows_only_B": c(rungs["rival_ows_only"]["B"]), "msmw_1dp": round(g["msmw_2025"], 1),
        "years": [2005, 2008, 2009, 2025, 2026, 2027, 2046],
        "options": list(S.OPTIONS), "rule_clauses": ["2.1", "2.2", "4.1", "4.2", "4.3", "4.4"],
        "dw_inside_edge_ft": 200, "walls_tried": [4000, 4500, 5000, 5500, 6500],
    }


def submission(g, rungs, fig, path):
    p = fig["peaks_ft"]
    cv = fig["cv07_peaks_ft"]
    lines = []
    A = lines.append
    A("## Tags")
    A("")
    A("> **Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (inverse problems: physical-"
      "model calibration and uncertainty propagation, a groundwater withdrawal forecast).")
    A("> **Analytical objective:** Forecasting & Predictive Modeling.")
    A("")
    A("## 1. Final Recommendation")
    A("")
    A("**The district will permit the %s gpm schedule.** Its greatest monthly drawdown at OW-S in 2046 is %d ft "
      "against Rule WR-4's 9 ft limit, and the 1,250 gpm schedule reaches %d ft. Not 1,250 gpm: calibrating the far "
      "field on the Mill Street record read against the nearest network well CV-07 or the wells' own pre-pumping "
      "levels credits the region's wet years to leakage and puts every schedule under %d ft; and not none of them: "
      "the test's Theis fit, carried twenty years, puts even 450 gpm at %d ft."
      % (c(g["call"]), p["1000"], p["1250"], max(cv.values()) + 1, fig["theis_peak_450"]))
    A("")
    A("## 2. Supplementary Questions")
    A("")
    A("### reidel_road_WR-4_demonstration.pdf")
    A("")
    A("1. Page 1 states that the district will permit the %s gpm schedule, with a table of the four schedules "
      "(450, 700, 1,000 and 1,250 gpm), each one's greatest monthly drawdown at OW-S in 2046 (%d, %d, %d and %d ft) "
      "and whether it is within 9.0 ft (yes, yes, yes, no)." % (c(g["call"]), p["450"], p["700"], p["1000"], p["1250"]))
    A("2. The chart under the table plots the drawdown at OW-S in every month from January 2027 to December 2046 for "
      "each schedule, one line per schedule with the 1,000 gpm line heaviest, against a dashed 9.0 ft limit line; "
      "every schedule's greatest month falls in 2046.")
    A("3. The text below gives the test fit (transmissivity %s ft2/day, storativity %s), the separation of the Mill "
      "Street record against CV-02 and CV-11, the leakage factor of %s ft with the walls %s ft apart, and the "
      "schedules and projection used." % (fig["T_text"], fig["S"], fig["B_text"], fig["width"]))
    A("")
    A("### reidel_road_sentinel_forecast.xlsx")
    A("")
    A("4. Sheet Demonstration: one row per schedule with the greatest monthly drawdown at OW-S in 2046 (to the "
      "hundredth and to the nearest foot: %d, %d, %d and %d ft), the greatest in the term and whether it meets 4.1; "
      "then the permitted schedule, %s gpm." % (p["450"], p["700"], p["1000"], p["1250"], c(g["call"])))
    A("5. Sheet Forecast OW-S: one row per month from 2027-01 to 2046-12 with the Mill Street projection (gpm), the "
      "drawdown from the Mill Street wells, and for each schedule its Reidel Road rate and the total drawdown at OW-S.")
    A("6. Sheets Aquifer test, Mill Street record and Calibration: the test fit, the monthly record from 2005 with "
      "each well's drawdown against the far wells and the model's, and the leakage factor with its residuals.")
    A("")
    A("### Answers the district asked for")
    A("")
    A("7. Greatest monthly drawdown at OW-S in 2046: 450 gpm %d ft; 700 gpm %d ft; 1,000 gpm %d ft; 1,250 gpm %d ft."
      % (p["450"], p["700"], p["1000"], p["1250"]))
    A("8. Drawdown the Mill Street wells caused at the Mill Street monitoring well, 2025 average: %d ft."
      % fig["msmw_2025_ft"])
    A("9. Greatest monthly drawdown in 2046 at the registered domestic well nearest the Reidel Road field (%s), "
      "under the %s gpm schedule: %d ft." % (fig["dw_id"], c(g["call"]), fig["dw_ft"]))
    A("")
    A("## 3. Critical Components")
    A("")
    A("1. The test's Theis fit (transmissivity **%s ft2/day**, storativity **%s**) matches the three observation wells "
      "to %.2f ft, yet carried forward it puts the Mill Street wells' 2025 drawdown at MS-MW at **%d ft**: the test "
      "cannot see the far field." % (fig["T_text"], fig["S"], fig["rms"], fig["theis_msmw_2025"]))
    A("2. CV-07 sits inside the Mill Street cone (its departure from CV-02 and CV-11 grew from **%.2f ft** in 2008 to "
      "**%.2f ft** in 2025), so the natural level comes from CV-02 and CV-11, and against it the Mill Street wells drew "
      "MS-MW down **%d ft** in 2025." % (fig["cv07_departure_2008"], fig["cv07_departure_2025"], fig["msmw_2025_ft"]))
    A("3. The bounded leaky aquifer reproducing that drawdown has a leakage factor of **%s ft**; against CV-07 the "
      "record asks for about **%s ft**." % (fig["B_text"], fig["cv07_B"]))
    A("4. Greatest monthly drawdown at OW-S in 2046: **%d ft** at 1,000 gpm and **%d ft** at 1,250 gpm, against the "
      "**9 ft** limit." % (p["1000"], p["1250"]))
    A("")
    A("## 4. Step-by-Step")
    A("")
    A("1. From PW-1_constant_rate_2026-09_transducers.csv, barologger_BL-2231_2026-09.csv and the field readings' "
      "Loggers sheet: each logger on its own clock, pressure less the barologger, the OW-2 re-hang and OW-3's rewritten "
      "rows taken out, drawdown against each well's pre-test trend and barometric response.")
    A("2. Fitted Theis to OW-1, OW-2 and OW-3 at the totalizer's %d gpm: transmissivity %s ft2/day, storativity %s, "
      "residual %.2f ft (the field's method)." % (fig["q_avg"], fig["T_text"], fig["S"], fig["rms"]))
    A("3. Hindcast the Mill Street wells (monthly gpm from harlow_springs_MOR_well_production_2009-2026.csv, thousand "
      "gallons before July 2016) with that fit: %d ft at MS-MW in 2025, more than twice the record, so the far field is "
      "calibrated on the record." % fig["theis_msmw_2025"])
    A("4. Read MS-MW (dropping readings taken with TW-1 running, the measuring point from cvwcd_well_register.xlsx) and "
      "the network wells: against its own 2005 to 2008 level or against CV-07 the record calibrates a leakage factor "
      "near %s ft and every schedule under %d ft at OW-S, filing 1,250 gpm (the reasonable but insufficient route)."
      % (fig["cv07_B"], max(cv.values()) + 1))
    A("5. CV-07's departure from CV-02 and CV-11 deepens with Mill Street pumping (correlation %.2f with the monthly "
      "rate, against %.2f for CV-02 less CV-11), and OW-S moved with CV-02 and CV-11 before 2009 (correlation %.2f): "
      "the natural level is CV-02 and CV-11's, and against it the Mill Street wells drew MS-MW down %d ft in 2025."
      % (fig["cv07_pump_corr"], fig["far_pair_pump_corr"], fig["ows_far_pre_corr"], fig["msmw_2025_ft"]))
    A("6. With the walls at Plate 3's mapped edges (%s ft apart) and the test's T and S, the leakage factor that "
      "reproduces the drawdown at MS-MW, CV-07 and OW-S from March 2009 to September 2026 is %s ft."
      % (fig["width"], fig["B_text"]))
    A("7. Superposed the Mill Street projection (reidel_road_WR-4_application_requested_schedules.pdf) and each "
      "Reidel Road schedule from April 2027 month by month at OW-S: greatest monthly drawdown in 2046 %d, %d, %d and "
      "%d ft for 450, 700, 1,000 and 1,250 gpm, so Rule WR-4 4.2 permits 1,000 gpm."
      % (p["450"], p["700"], p["1000"], p["1250"]))
    A("8. Rule WR-4 4.4's domestic well is %s, nearest PW-1 and PW-2 in cvwcd_well_register.xlsx and about 200 ft "
      "inside the plate's west edge, where the wall's image matters: %d ft in 2046 under %s gpm, against %d ft if "
      "the walls are left out (the record alone fits either way)." % (fig["dw_id"], fig["dw_ft"], c(g["call"]),
                                                                     fig["dw_nowalls_ft"]))
    A("")
    A("No other schedule survives. Theis from the test alone fails every schedule, but its own hindcast of the Mill "
      "Street record is more than twice the record. Every far-field calibration read against CV-07, the wells' own baselines or a "
      "fitted trend files 1,250 gpm, and CV-07's growing departure and the wet 2010s rule each of those out. Against "
      "CV-02, CV-11 or both, with the walls from 4,000 ft apart to absent and T from any observation well, the "
      "1,000 gpm peak stays under 9 ft and the 1,250 gpm peak over it. Calibrated on OW-S alone, whose record carries "
      "half a foot of Mill Street drawdown, the leakage factor (%s ft) puts MS-MW's 2025 drawdown at %.1f ft against "
      "the record's %.1f." % (fig["ows_only_B"], fig["ows_only_msmw"], fig["msmw_1dp"]))
    open(path, "w").write("\n".join(lines) + "\n")
