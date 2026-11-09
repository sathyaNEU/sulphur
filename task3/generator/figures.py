"""task3: figures.json, every figure the write-up and the goldens state, from one analysis run on the shipped pack."""
import numpy as np

import analysis as A
import docs as DC
import freq as F

AEPS = (0.5, 0.1, 0.04, 0.02, 0.01, 0.002)
BANDS = ((0.10, "more often than once in 10 years"), (0.01, "once in 10 to 100 years"),
         (0.001, "once in 100 to 1,000 years"), (0.0, "less often than once in 1,000 years"))


def k5000(v):
    return int(round(v / 5000.0)) * 5000


def r100(v):
    return int(round(v / 100.0)) * 100


def band(aep):
    for lo, label in BANDS:
        if aep > lo:
            return label
    return BANDS[-1][1]


def spans_of(q01):
    return min([sp for sp, rated in DC.SPANS if rated >= q01] or [None])


def top_years(series, n=2):
    return sorted(series, key=lambda y: -series[y])[:n]


def summary(par, series):
    q = {a: F.quantile(par, a) for a in AEPS}
    return {"q": {str(a): r100(v) for a, v in q.items()}, "q50_5000": k5000(q[0.5]), "q01_5000": k5000(q[0.01]),
            "span": spans_of(q[0.01]), "bands": {str(sp): band(F.aep_of(par, rated)) for sp, rated in DC.SPANS},
            "top2": top_years(series)}


def make(R, tgt):
    q = R["q"]
    par = R["par"]
    call = spans_of(q[0.01])
    zc, ar, ac, areas, area_c = A.bands(tgt)
    zv, lapse, t50, k = R["zv"], R["lapse"], R["t50"], R["k"]
    # how much of each basin drained rain in the river's floods, from the matched floods with the golden constants
    rows = []
    best = {}
    for d, qq, tv, tot, dr, dc, v in R["rows"]:
        tz = tv - lapse * (zc - zv) / A.FT_PER_KM
        rain = 1.0 - 1.0 / (1.0 + np.exp((tz - t50) / k))
        f = v / qq
        rows.append((qq, (ar * rain).sum() / ar.sum(), (ac * rain).sum() / ac.sum(), zv + (tv - t50) / lapse * A.FT_PER_KM, f))
        wy = d.year + (1 if d.month >= 10 else 0)
        if wy not in best or v > best[wy][1]:
            best[wy] = (d, v, qq)
    r = np.array(rows)
    big = r[:, 0] >= np.quantile(r[:, 0], 0.9)
    annual = R["annual"]
    river = {y: annual[y][1] for y in annual}
    river1 = F.quantile(R["river_par"], 0.01)
    rated = dict(DC.SPANS)
    from openpyxl import load_workbook
    wbk = load_workbook(A.os.path.join(tgt, "region3_basin_characteristics.xlsx"), data_only=True)
    zmean_c = next(float(r[1]) for r in wbk["Durrow Ck at Ransom Bar Rd"].iter_rows(values_only=True)
                   if r and r[0] == "Mean basin elevation (ft)")
    zmean_r = next(float(r[3]) for r in wbk["Gauged basins"].iter_rows(min_row=4, values_only=True) if r and str(r[0]) == "12183450")
    low_thr = par["low_threshold"]
    # the creek's estimated annual peaks, one row per water year
    peaks = []
    for wy in range(1951, 2026):
        if wy in best:
            d, v, qq = best[wy]
            peaks.append(dict(water_year=wy, cfs=r100(v), qualifier="", river_date=d.isoformat(), river_cfs=int(qq)))
        else:
            peaks.append(dict(water_year=wy, cfs=r100(low_thr), qualifier="<", river_date="", river_cfs=None))
    default = summary(R["river_par"], river)
    default["q"] = {a: r100(F.quantile(R["river_par"], float(a)) * (area_c / R["area_r"]) ** A.STATE_B) for a in default["q"]}
    rpar_c = dict(R["river_par"])
    rpar_c["mean"] = rpar_c["mean"] + A.STATE_B * np.log10(area_c / R["area_r"])
    default.update({"q50_5000": k5000(F.quantile(rpar_c, 0.5)), "q01_5000": k5000(F.quantile(rpar_c, 0.01)),
                    "span": spans_of(F.quantile(rpar_c, 0.01)),
                    "bands": {str(sp): band(F.aep_of(rpar_c, rq)) for sp, rq in DC.SPANS}})
    V = {name: summary(v["par"], v["series"]) for name, v in R["variants"].items()}
    Fg = {
        "call_span_ft": call,
        "spans": {str(s): v for s, v in DC.SPANS},
        "golden_raw": {str(a): round(q[a], 1) for a in AEPS},
        "q50_5000": k5000(q[0.5]), "q01_5000": k5000(q[0.01]),
        "bands": {str(sp): band(F.aep_of(par, rq)) for sp, rq in DC.SPANS},
        "aep_rated_pct": {str(sp): round(100 * F.aep_of(par, rq), 2) for sp, rq in DC.SPANS},
        "top2": top_years(R["series"]),
        "top2_cfs": [r100(R["series"][y]) for y in top_years(R["series"])],
        "top2_dates": [best[y][0].isoformat() for y in top_years(R["series"])],
        "third_cfs": r100(sorted(R["series"].values(), reverse=True)[2]),
        "river_top2": top_years(river), "river_top2_cfs": [int(river[y]) for y in top_years(river)],
        "river_top2_dates": [annual[y][0].isoformat() for y in top_years(river)],
        "peaks": peaks, "missing_years": R["missing"], "low_threshold": r100(low_thr),
        "par": {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in par.items()},
        "river_par": {kk: (round(vv, 4) if isinstance(vv, float) else vv) for kk, vv in R["river_par"].items()},
        "river_1pct": r100(river1), "river_50pct": r100(F.quantile(R["river_par"], 0.5)),
        "drainage_area": r100(R["r0"]), "default": default,
        "regional_equation": r100(R["regional_eq"]), "regional_unit_flood": r100(R["regional_unit_flood"]),
        "elevation_regression": r100(R["elev_reg"]),
        "area_r": R["area_r"], "area_c": R["area_c"], "zv": int(round(zv)),
        "mean_elev_r": int(round(zmean_r, -1)), "mean_elev_c": int(round(zmean_c, -1)),
        "lapse": round(lapse, 2), "lapse_1": round(lapse, 1), "n_lapse": R["n_lapse"],
        "t50": round(t50, 2), "t50_1": round(t50, 1), "t50_sites": [round(x, 2) for x in R["t50_sites"]],
        "k": round(k, 2), "g": round(R["g"], 3), "g_pct": int(round(100 * R["g"])),
        "g_ratio": round(R["station_means"]["ratio"], 2), "g_n": R["station_means"]["n"],
        "n_floods": R["n_floods"], "n_matched": R["n_matched"], "n_years": len(R["series"]),
        "share_river_median_pct": int(round(100 * np.median(r[:, 1]))),
        "share_river_big_pct": int(round(100 * np.median(r[big, 1]))),
        "share_creek_median_pct": int(round(100 * np.median(r[:, 2]))),
        "snowline_median_ft": int(round(np.median(r[:, 3]), -1)),
        "factor_median": round(float(np.median(r[:, 4])), 2), "factor_big": round(float(np.median(r[big, 4])), 2),
        "big_threshold": r100(np.quantile(r[:, 0], 0.9)),
        "own_r": round(R["own_r"], 2), "total_rain_r": round(R["total_rain_r"], 2), "own_n": R["own_n"],
        "dry_at_peak_pct": int(round(100 * R["peak_hour"]["dry_share"])),
        "peak_hour_colder_c": round(-R["peak_hour"]["median_diff"], 1),
        "ratio_creek_river_1pct": round(q[0.01] / river1, 2),
        "variants": V,
        "validation": {k: {"bias_pct": int(round(100 * (np.exp(v[0]) - 1))), "mad": round(v[1], 2), "n": v[2]}
                       for k, v in R["validation"].items()},
        "val_site": R["val_site"], "val_area": R["val_area"], "short_years": R["short_years"],
        "sc_ratio": r100(R["sc_ratio"]), "sc_move1": r100(R["sc_move1"]), "sc_own": r100(R["sc_own"]),
        "variant_q01": {name: r100(v["q"]["0.01"]) for name, v in V.items()},
        "regional_skew": F.REGIONAL_SKEW,
        "lapse_snotel": round(R["lapse_snotel"], 2), "lapse_snotel_1": round(R["lapse_snotel"], 1),
        "n_lapse_snotel": R["n_lapse_snotel"],
        "constants": {"standard_section": 7.4, "freeboard_ft": 2.0, "distance_mi": 6.2, "min_record_years": 25,
                      "base_cfs": 2500, "rounding_cfs": 5000, "rounding_file_cfs": 100, "zmin_c": 610, "zmax_c": 4380,
                      "zmax_r": 10380, "zmin_r": 1640, "textbook_lapse": 6.5, "per_1000_ft": 1000, "basin_limit_sq_mi": 10,
                      "peaks_n": 75, "span_lengths_ft": [140, 185, 240], "site_no": 12183450, "gap_hours": 6,
                      "lookback_hours": 36, "band_years": [10, 100, 1000], "first_wy": 1951, "last_wy": 2025},
        "as_of": "2026-11-06",
    }
    return Fg
