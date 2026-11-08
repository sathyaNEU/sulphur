"""task3 architecture 4: an independent recomputation from the cut pack (pandas, a different estimator at every step):
the delay to the water table from the matured conversions, the leachate under irrigated vegetables from samples whose
water left the root zone since 2012, and the forecast as each well's 2024-2026 level plus each cleared parcel's step at
its own arrival. It must reproduce the call, the first year at 10, the 2034 entry point and the highest well to the
asked rounding.

    python3 verify.py <target>"""
import json
import math
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
SHARE = {"W3": 0.08, "W5": 0.30, "W6": 0.32, "W7": 0.30}
CODES = {"FOR": ["F1", "F2", "141", "142"], "GRS": ["G1", "G2", "176", "37"], "DRY": ["A1", "A2", "24", "36"],
         "IRC": ["A3", "301"], "IRV": ["A4", "304"], "RES": ["U1", "121"], "WAT": ["W", "111"]}
C2 = {c: k for k, v in CODES.items() for c in v}


def decimal_year(s):
    d = pd.to_datetime(s)
    start = pd.to_datetime(d.dt.year.astype(str) + "-01-01")
    end = pd.to_datetime((d.dt.year + 1).astype(str) + "-01-01")
    return d.dt.year + (d - start).dt.total_seconds() / (end - start).dt.total_seconds()


def nitrate_n(res, units):
    v = res.str.lstrip("<").astype(float)
    v = np.where(res.str.startswith("<"), v / 2.0, v)
    return np.where(units.str.contains("NO3"), v / 4.427, v)


def main(target):
    out = {}
    r = pd.read_csv(os.path.join(target, "corlinden_raw_water_nitrate_results_1988-2026.csv"), dtype=str)
    r["n"] = nitrate_n(r["result"], r["units"])
    pt = {"WELL 3": "W3", "HR-W03": "W3", "WELL 5": "W5", "HR-W05": "W5", "WELL 6": "W6", "HR-W06": "W6",
          "WELL 7": "W7", "HR-W07": "W7", "EP-01": "EP"}
    r["w"] = r["sample_point"].map(pt)
    r = r.groupby(["w", "collected"], as_index=False)["n"].mean()
    r["year"] = r["collected"].str[:4].astype(int)
    ann = r.groupby(["w", "year"])["n"].mean()
    # land cover
    lc = pd.read_csv(os.path.join(target, "ravell_county_parcel_land_cover_1986-2026.csv"), dtype=str).drop_duplicates()
    lc["cls"] = lc["land_cover_code"].map(C2)
    lc["year"] = lc["year"].astype(int)
    hist = {}
    for pid, g in lc.groupby("parcel_id"):
        hist.setdefault(pid, {}).update(dict(zip(g["year"], g["cls"])))
    for _, row in lc[lc["parent_parcel_id"].notna()].iterrows():
        for y, c in hist.get(row["parent_parcel_id"], {}).items():
            hist[row["parcel_id"]].setdefault(y, c)
    # network
    sites = pd.read_excel(os.path.join(target, "ravell_county_groundwater_network_sites.xlsx"), sheet_name="Sites")
    alias = {r_.site_id: str(r_.notes).replace("replaced by ", "") for r_ in sites.itertuples()
             if str(r_.status).startswith("abandoned")}
    sites = sites[~sites["status"].astype(str).str.startswith("abandoned")].set_index("site_id")
    ages = pd.read_excel(os.path.join(target, "ravell_county_groundwater_age_survey_2019.xlsx"), sheet_name="Results")
    ages = ages[ages["notes"].astype(str).str.startswith("water-table")].set_index("site")["apparent_age_yr"]
    ns = pd.read_csv(os.path.join(target, "ravell_county_groundwater_network_samples_1990-2026.csv"), dtype=str)
    ns["site_id"] = ns["site_id"].replace(alias)
    ns["n"] = nitrate_n(ns["nitrate_result"], ns["units"])
    ns = ns.groupby(["site_id", "sample_date"], as_index=False)["n"].mean()
    ns["t"] = decimal_year(ns["sample_date"])
    # matured conversions: a step fitted by least squares, the step time half-way between the two samples it parts
    X, Y = [], []
    for sid, g in ns.groupby("site_id"):
        h = hist[sites.loc[sid, "parcel_id"]]
        ch = [y for y in range(1987, 2027) if h[y] != h[y - 1]]
        if len(ch) != 1 or not (1987 <= ch[0] <= 2010) or h[ch[0] - 1] not in ("FOR", "GRS", "DRY") or \
                h[ch[0]] not in ("IRC", "IRV"):
            continue
        c = ch[0]
        g = g.sort_values("t")
        g = g[g["t"] >= c - 3]
        if (g["t"] < c + 1).sum() == 0:
            continue
        v = g["n"].to_numpy()
        t = g["t"].to_numpy()
        e = [((v[:k] - v[:k].mean()) ** 2).sum() + ((v[k:] - v[k:].mean()) ** 2).sum() for k in range(1, len(v))]
        k = int(np.argmin(e)) + 1
        step = 0.5 * (t[k - 1] + t[k])
        X.append(float(sites.loc[sid, "mean_depth_to_water_ft"]))
        Y.append(step - c - float(ages.get(sid, ages.mean())))
    b, a = np.polyfit(X, Y, 1)
    out["b"], out["a"], out["n"] = float(b), float(a), len(X)
    # leachate under irrigated vegetables and forest: steady sites, samples whose water left the root zone since 2012
    lvl = {}
    for cls in ("IRV", "FOR"):
        vals = []
        for sid, g in ns.groupby("site_id"):
            h = hist[sites.loc[sid, "parcel_id"]]
            if set(h[y] for y in range(1986, 2027)) != {cls}:
                continue
            lag = float(ages.get(sid, ages.mean())) + a + b * float(sites.loc[sid, "mean_depth_to_water_ft"])
            vals += list(g.loc[g["t"] - lag >= 2012, "n"])
        lvl[cls] = float(np.mean(vals))
    out["irv"] = lvl["IRV"]
    # the protection area: each well's 2024-2026 level, plus each cleared parcel's step at its own arrival
    pa = pd.read_excel(os.path.join(target, "sallow_road_WHPA_parcel_attributes_2019.xlsx"), sheet_name="Parcels")
    rch = pd.read_excel(os.path.join(target, "sallow_road_WHPA_parcel_attributes_2019.xlsx"), sheet_name="Recharge")
    q = dict(zip(rch["land_cover"], rch["recharge_in_per_yr"]))
    qc = {"FOR": q["forest"], "GRS": q["grass and pasture"], "DRY": q["cropland, not irrigated"],
          "IRC": q["irrigated corn and soybean"], "IRV": q["irrigated vegetables"], "RES": q["residential"], "WAT": 0.0}
    pa["w"] = "W" + pa["zone"].str.split().str[-1]
    fc = {}
    for w, g in pa.groupby("w"):
        base = float(np.mean([ann[(w, y)] for y in (2024, 2025, 2026)]))
        flux = sum(row.acres * qc[hist[row.parcel_id][2026]] for row in g.itertuples())
        steps = []
        for row in g.itertuples():
            h = hist[row.parcel_id]
            cl = [y for y in range(2013, 2027) if h[y] in ("IRC", "IRV") and h[y - 1] not in ("IRC", "IRV")]
            if not cl:
                continue
            arr = cl[0] + a + b * row.depth_to_water_ft + row.gw_time_of_travel_yr
            share = row.acres * qc[h[2026]] / flux
            steps.append((arr, share * (lvl["IRV"] - lvl["FOR"])))
        fc[w] = {y: base + sum(dv * np.mean([1.0 if y + f >= arr else 0.0 for f in (0.125, 0.375, 0.625, 0.875)])
                               for arr, dv in steps) for y in range(2027, 2041)}
    ep = {y: sum(SHARE[w] * fc[w][y] for w in SHARE) for y in range(2027, 2041)}
    cross = next((y for y in ep if ep[y] >= 10.0), None)
    hi = max(SHARE, key=lambda w: fc[w][2034])
    out.update({"cross": cross, "call": 2027 if (cross and cross < 2034) else 2031, "ep2034": ep[2034],
                "hi": hi, "hi2034": fc[hi][2034]})
    F = json.load(open(os.path.join(HERE, "figures.json")))
    mg = lambda x: int(math.floor(x + 0.5))
    ok = [("call", out["call"] == F["call"]), ("first year at 10", out["cross"] == F["cross"]),
          ("2034 entry point (whole mg/L)", mg(out["ep2034"]) == F["ep2034_int"]),
          ("highest well", out["hi"] == F["hi_well"]), ("its 2034 mean (whole mg/L)", mg(out["hi2034"]) == F["hi_2034_int"]),
          ("delay per foot (0.01 yr)", abs(out["b"] - F["b3"]) < 0.01)]
    print("verify: b %.4f a %.3f n %d, IRV %.2f, cross %s, call %s, EP 2034 %.2f, highest %s %.2f" %
          (out["b"], out["a"], out["n"], out["irv"], out["cross"], out["call"], out["ep2034"], out["hi"], out["hi2034"]))
    bad = [k for k, v in ok if not v]
    print("verify:", "PASS" if not bad else "FAIL " + ", ".join(bad))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1]))
