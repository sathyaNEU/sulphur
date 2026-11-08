"""task3 architecture 3: every rung of the ladder and every rival of the fork table, run on the cut pack through
solve.py with one switch changed, written to generator/rungs.json for checks.py, ceiling.py and the write-up."""
import json
import math
import os
import sys

import numpy as np

import solve as S

VARIANTS = [
    ("golden", {}),
    ("ref_cv02", {"control": ("CV-02",)}),
    ("ref_cv11", {"control": ("CV-11",)}),
    ("walls_4000", {"width": 4000.0}),
    ("walls_6500", {"width": 6500.0}),
    ("walls_4500", {"width": 4500.0}),
    ("walls_5500", {"width": 5500.0}),
    ("walls_none", {"width": None}),
    ("test_ow1", {"fit_test": ("OW-1",)}),
    ("test_ow2", {"fit_test": ("OW-2",)}),
    ("test_ow3", {"fit_test": ("OW-3",)}),
    ("test_five", {"fit_test": ("OW-1", "OW-2", "OW-3", "PW-2", "OW-S")}),
    ("no_baro", {"baro_correct": False}),
    ("fit_msmw", {"fit_wells": ("MS-MW",)}),
    ("fit_msmw_ows", {"fit_wells": ("MS-MW", "OW-S")}),
    ("keep_running", {"keep_running": True}),
    ("clock_naive", {"clock_naive": True}),
    ("no_rehang", {"ignore_rehang": True}),
    ("chain3_test_leaky", {"test_leaky": True}),
    ("chain4_annual", {"seasonal": False}),
    # the wrong rungs
    ("rung0_theis", {"leaky": False}),
    ("rung1_raw", {"control": None}),
    ("rung1_cv07", {"control": ("CV-07",), "fit_wells": ("MS-MW", "OW-S")}),
    ("rung1_trend", {"control": None, "trend": True}),
    ("rung1_cv07_clean", {"control": ("CV-07", "CV-02", "CV-11")}),
    ("rival_ows_only", {"fit_wells": ("OW-S",)}),
]
STANDING = ["golden", "ref_cv02", "ref_cv11", "walls_4000", "walls_6500", "walls_4500", "walls_5500", "walls_none",
            "test_ow1", "test_ow2", "test_ow3", "test_five", "no_baro", "fit_msmw", "fit_msmw_ows"]
# the plate maps the walls: the domestic-well ask is held to the readings of the plate within 500 ft
PLATE_READINGS = ["golden", "ref_cv02", "ref_cv11", "walls_4500", "walls_5500", "test_ow1", "test_ow2", "test_ow3",
                  "test_five", "no_baro", "fit_msmw", "fit_msmw_ows"]


def summarise(r):
    return {"T": round(r["T"], 1), "S": float("%.4g" % r["S"]), "B": r["B"], "width": r["width"],
            "peaks": {str(k): round(v, 3) for k, v in r["peaks"].items()},
            "peak_term": {str(k): round(v, 3) for k, v in r["peak_term"].items()},
            "peak_year": {str(k): v for k, v in r["peak_year"].items()},
            "call": r["call"], "dw": None if r["dw"] is None else round(r["dw"], 3), "dw_id": r["dw_id"],
            "msmw_2025": round(r["msmw_2025"], 3), "msmw_2025_model": round(r["msmw_2025_model"], 3),
            "town_dec2046": round(r["town_dec2046"], 3)}


def main(target, out):
    res = {}
    full = {}
    for name, kw in VARIANTS:
        r = S.run(target, **kw)
        res[name] = summarise(r)
        if name in ("golden", "rung0_theis", "rung1_cv07"):
            full[name] = r
        print("  %-18s B %-7s call %-5s peaks %s msmw %.2f" % (name, r["B"], r["call"],
              [round(r["peaks"][o], 2) for o in S.OPTIONS], r["msmw_2025"]), flush=True)
    g = full["golden"]
    # the Theis hindcast at MS-MW in 2025, the default path's own check
    th = full["rung0_theis"]
    res["theis_msmw_2025"] = round(th["msmw_2025_model"], 3)
    res["cv07_B"] = full["rung1_cv07"]["B"]
    res["cv07_peak_max"] = round(max(full["rung1_cv07"]["peaks"].values()), 3)
    # OW-S alone: the profile of the misfit over the leakage factor, and how flat it is
    att = g["att"]
    prof = S.profile(g["q"], g["frame"], att, g["T"], g["S"], g["width"], ("OW-S",), g["B"])
    best = min(v for _, v in prof)
    n = int(np.sum(S.FIT & ~np.isnan(att["OW-S"])))
    sig2 = best / n
    flat = [b for b, v in prof if (v - best) / sig2 < 3.84]
    res["ows_only_profile"] = {"n": n, "range_within_chi2": [min(flat), max(flat)]}
    prof_all = S.profile(g["q"], g["frame"], att, g["T"], g["S"], g["width"], ("MS-MW", "CV-07", "OW-S"), g["B"])
    best_a = min(v for _, v in prof_all)
    n_a = sum(int(np.sum(S.FIT & ~np.isnan(att[w]))) for w in ("MS-MW", "CV-07", "OW-S"))
    flat_a = [b for b, v in prof_all if (v - best_a) / (best_a / n_a) < 3.84]
    res["joint_profile"] = {"n": n_a, "range_within_chi2": [min(flat_a), max(flat_a)]}
    # CV-07's departure from the far wells, before and after pumping began, and its seasonal link to pumping
    lv = g["lv"]
    far = np.nanmean(np.vstack([lv["CV-02"] - np.nanmean(lv["CV-02"][:48]), lv["CV-11"] - np.nanmean(lv["CV-11"][:48])]), axis=0)
    dep = (lv["CV-07"] - np.nanmean(lv["CV-07"][:48])) - far
    yrs = np.array([y for y, _ in S.MONTHS])
    res["cv07_departure"] = {str(y): round(float(np.nanmean(dep[yrs == y])), 2) for y in range(2005, 2027)}
    q = g["q"]["TW-1"] + g["q"]["TW-2"]
    ok = (yrs >= 2015) & (yrs <= 2025) & ~np.isnan(dep)
    res["cv07_pump_corr"] = round(float(np.corrcoef(dep[ok], -q[ok])[0, 1]), 3)
    dep2 = (lv["CV-02"] - np.nanmean(lv["CV-02"][:48])) - (lv["CV-11"] - np.nanmean(lv["CV-11"][:48]))
    ok2 = (yrs >= 2015) & (yrs <= 2025) & ~np.isnan(dep2)
    res["far_pair_pump_corr"] = round(float(np.corrcoef(dep2[ok2], -q[ok2])[0, 1]), 3)
    pre = yrs <= 2008
    ows = lv["OW-S"] - np.nanmean(lv["OW-S"][:48])
    okp = pre & ~np.isnan(ows) & ~np.isnan(far)
    res["ows_far_pre_corr"] = round(float(np.corrcoef(ows[okp], far[okp])[0, 1]), 3)
    res["golden_resid"] = {k: round(v, 3) for k, v in g["resid"].items()}
    res["standing"] = STANDING
    res["plate_readings"] = PLATE_READINGS
    # the like-for-like slip: the far wells anchored to 2005 to 2008 while MS-MW is anchored to its own months
    win, w05 = S._win("MS-MW"), S._win("OW-S")
    shift = float(np.mean([np.nanmean(lv[c][win]) - np.nanmean(lv[c][w05]) for c in S.CLEAN]))
    res["msmw_anchor_slip"] = round(g["msmw_2025"] + shift, 3)
    json.dump(res, open(out, "w"), indent=1, sort_keys=True)
    return res, full


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
