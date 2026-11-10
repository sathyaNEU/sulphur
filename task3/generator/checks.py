"""task3 checks: the pack's input gates, every semantic fork (SF1 to SF20) and the bar block (each hurried figure
outside its band, the shortcuts naming different pairs, the funded pair across the defensible family), run on the
installed pack against figures.json.

    python3 task3/generator/checks.py
"""
import csv
import glob
import json
import os
import re
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import docs as DC  # noqa: E402
import world as W  # noqa: E402

TGT = os.path.join(TASK, "target")
RES = []


def ok(cid, cond, msg):
    RES.append((cid, bool(cond), msg))


def inside(v, b):
    return b[0] <= v <= b[1]


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    R = A.run(TGT)
    B = F["bands"]
    files = sorted(os.listdir(TGT))
    # P0: the input gates
    ok("P0", len(files) >= 10, "%d files in the pack" % len(files))
    kinds = {os.path.splitext(f)[1] for f in files}
    ok("P1", {".csv", ".txt"} & kinds and {".xlsx"} & kinds and {".pdf"} & kinds, "spreadsheet, text and document categories: %s" % sorted(kinds))
    rows = {f: sum(1 for _ in open(os.path.join(TGT, f), errors="ignore")) for f in files if f.endswith(".csv")}
    ok("P2", max(rows.values()) >= 20000, "a CSV of 20,000 rows or more (%d)" % max(rows.values()))
    ok("P3", rows[A.F_311] >= 750, "the 311 export runs %d rows (more than ten printed pages)" % rows[A.F_311])
    for f in files:
        if f.endswith((".csv", ".txt")):
            ok("P4", "—" not in open(os.path.join(TGT, f), encoding="utf-8", errors="ignore").read(), "no em dash in %s" % f)
    src = open(os.path.join(HERE, "analysis.py")).read()
    run_src = src[src.index("def run(tgt):"):]
    for d in (A.F_311, A.F_SLR, A.F_RAIN):
        name = [k for k, v in vars(A).items() if v == d][0]
        ok("P5", name not in run_src, "distractor %s unread by the golden" % d)
    txt = open(os.path.join(TASK, "prompt.txt")).read()
    for f in files:
        ok("P6", f not in txt, "the prompt names no file (%s)" % f)

    # SF1 tide year
    ok("SF1", list(A.tide_year(pd.to_datetime(["2025-04-30", "2025-05-01"]))) == [2024, 2025], "tide years start on 1 May")
    # SF2 calendar day, at or above
    t = pd.to_datetime(["2025-06-01 23:50", "2025-06-02 00:10"])
    ok("SF2", A.count_days(t, np.array([0.0, -0.01]), 0.0) == 1 and A.count_days(t, np.array([0.0, 0.0]), 0.0) == 2,
       "a day counts when a high water reaches the level, by local standard date")
    # SF3 the lane, Front Street's from the sensor
    ok("SF3", abs(R["front_level"] - W.SITES["front"]["level"]) <= 0.03,
       "Front Street's lane from the sensor %.3f against the street's %.2f" % (R["front_level"], W.SITES["front"]["level"]))
    inv = A.read_inventory(TGT)
    ok("SF3b", inv["front"]["lane"] is None and inv["front"]["rim"] < R["front_level_navd88"] - 0.25,
       "Front Street's lane is not in the inventory and its rim sits below the lane")
    # SF4 rain ponding not counted
    sen = A.read_sensor(TGT)
    dep = sen.depth_in.rolling(5, center=True, min_periods=3).median()
    hw = A.Harbor(TGT).year_hw(2025, "obs")
    wet_any = 0
    for tt, h in hw.items():
        w = dep[(dep.index >= tt - pd.Timedelta(hours=2)) & (dep.index <= tt + pd.Timedelta(hours=2))]
        wet_any += int(len(w) >= 30 and w.max() >= 0.5 and h < R["front_level"])
    ok("SF4", wet_any >= 1 and F["front_sensor_days"] + F["front_outage_days"] == F["hind"]["front"],
       "%d high tides below the lane met rain ponding on the sensor and are not counted" % wet_any)
    # SF5 the weather years
    ok("SF5", A.WX_YEARS == list(range(1990, 2026)), "36 weather years, 1990-91 to 2025-26")
    # SF6 the planning sea level
    import pypdf
    gtxt = " ".join(p.extract_text() for p in pypdf.PdfReader(os.path.join(TGT, A.F_GUIDE)).pages)
    gtxt = re.sub(r"\s+", " ", gtxt)
    ok("SF6", A.PLAN == DC.PLANNING_MSL and "%.2f ft above its 1983-2001 mean sea level" % A.PLAN in gtxt,
       "the planning sea level %.2f is the guidelines' value" % A.PLAN)
    # SF7 percentile estimators inside the range bands
    for nm, f in R["family"].items():
        for k in [x for x in f if x.startswith("harbor_lo")]:
            ok("SF7", inside(f[k], B["harbor_lo"]), "%s %s %.2f inside %s" % (nm, k, f[k], B["harbor_lo"]))
        for k in [x for x in f if x.startswith("harbor_hi")]:
            ok("SF7", inside(f[k], B["harbor_hi"]), "%s %s %.2f inside %s" % (nm, k, f[k], B["harbor_hi"]))
    # SF8 detrending by month
    ok("SF8", inside(R["family"]["month_detrend"]["harbor"], B["harbor_exp"]), "month detrending %.2f inside the band" %
       R["family"]["month_detrend"]["harbor"])
    # SF9 alignment; the day's largest refuted by the replay
    ok("SF9", inside(R["family"]["nearest"]["harbor"], B["harbor_exp"]) and R["replay_2025"]["interp"] == F["harbor_2025"]
       and R["replay_2025"]["nearest"] == F["harbor_2025"] and R["replay_2025"]["daymax"] != F["harbor_2025"],
       "replays of 2025-26: %s against the observed %d" % (R["replay_2025"], F["harbor_2025"]))
    # SF10 the marsh forms; the straight line's residuals past the bend
    for k, v in zip(("quadratic", "cubic", "upper-half line"), R["alt"]["marsh_hind"]):
        ok("SF10", inside(v, B["hind_marsh"]), "Marsh Road 2025-26 by the %s: %d" % (k, v))
    for k, v in zip(("quadratic", "cubic", "upper-half line"), R["alt"]["marsh_exp"]):
        ok("SF10", inside(v, B["exp_marsh"]), "Marsh Road 2027-28 by the %s: %.2f" % (k, v))
    s = A.read_logger(TGT, "marsh")
    H = A.Harbor(TGT)
    d = A.pair_site(H, A.hilo_series(s), H.nav, H.monthly)
    lf = A.fit_linear(d)
    past = d[d.harbor >= 8.3]
    resid = past.site - (lf["a"] + lf["b"] * past.harbor)
    ok("SF10b", (resid < 0).all() and len(past) >= 10 and F["marsh_sd"][1] >= 2.5 * F["marsh_sd"][0],
       "the straight line runs above all %d high waters at harbor 8.3 ft or more; residuals %.2f against %.2f" %
       (len(past), F["marsh_sd"][1], F["marsh_sd"][0]))
    # SF11 river flow forms
    rf = R["river_fit"]
    ok("SF11", inside(R["var"]["river_lin"]["hind"], B["hind_river"]) and inside(R["var"]["river_lin"]["exp"], B["exp_river"])
       and rf["log"]["sse"] > 1.5 * rf["pow"]["sse"], "linear inside the bands; logarithmic refuted (%.2f against %.2f)" %
       (rf["log"]["sse"], rf["pow"]["sse"]))
    # SF12 drift ruled out
    from openpyxl import load_workbook
    ws = load_workbook(os.path.join(TGT, A.F_INV), data_only=True)["Logger campaigns"]
    chk = [r for r in ws.iter_rows(min_row=2, values_only=True) if r[0] and "River Road" in r[0]][0]
    ok("SF12", abs(chk[5]) <= 0.02 and abs(chk[6]) <= 0.02, "River Road staff checks %.2f and %.2f" % (chk[5], chk[6]))
    # SF13 logger clocks
    for site in ("marsh", "oyster", "river"):
        hdr = open(os.path.join(TGT, A.F_LOG[site]), encoding="utf-8").read().split("\n")[1]
        ok("SF13", re.search(r"GMT-0[45]:00", hdr) is not None, "%s logger carries its launch offset" % site)
    # SF14 datum
    ok("SF14", abs(H.nav - 3.42) < 1e-9, "NAVD88 3.42 ft above MLLW")
    # SF15 the bridge adds up; one at a time does not
    b = F["bridge"]
    ok("SF15", abs(b["sea"] + b["tides"] + b["weather"] - b["total"]) <= 0.15, "the shares add to the change")
    v = R["bridge_vals"]
    oat = (v["plan|25|25"] - v["25|25|25"]) + (v["25|27|25"] - v["25|25|25"]) + (v["25|25|clim"] - v["25|25|25"])
    ok("SF15b", abs(oat - b["total"]) >= 2.0, "one at a time adds to %.2f against %.2f" % (oat, b["total"]))
    # SF16 the harbor's 2025-26 count from the hourly heights
    hr = A.read_hourly(TGT)
    hv = hr["Verified (ft)"][(hr.index >= "2025-05-01") & (hr.index < "2026-05-01")]
    n_hourly = int((hv.groupby(hv.index.floor("D")).max() >= A.HARBOR_MINOR).sum())
    ok("SF16", abs(n_hourly - F["harbor_2025"]) <= 1, "hourly maxima %d against the high waters' %d" % (n_hourly, F["harbor_2025"]))
    # SF17, SF18 flows and years paired with the weather years
    ok("SF17", "self.Q[y] = Q.reindex(qd)" in src, "each weather year carries its own flows")
    ok("SF18", F["n_weather_years"] == 36 and len(F["per_year"]["front"]) == 36, "the pair count runs on the same 36 years")
    # SF19 nothing preliminary in the counts
    hl = A.read_hilo(TGT, A.F_HL)
    ok("SF19", hl.t.max() < pd.Timestamp("2026-10-01"), "verified high waters stop at September 2026")
    # SF20 margins across the family
    for nm, f in R["family"].items():
        top = sorted(A.ORDER, key=lambda k: -f[k])
        ok("SF20", set(top[:2]) == set(F["call_keys"]) and f[top[1]] >= 1.25 * f[top[2]],
           "%s: %s then %s at %.1f against %.1f" % (nm, top[0], top[1], f[top[1]], f[top[2]]))
    # the bar block: each hurried figure outside its band, the routes' pairs distinct
    V = F["variants_hind"]
    ok("H1", not inside(V["marsh_linear"], B["hind_marsh"]) and not inside(F["route_exp"]["marsh straight line"]["marsh"], B["exp_marsh"]),
       "the straight line: Marsh Road %d and %.1f" % (V["marsh_linear"], F["route_exp"]["marsh straight line"]["marsh"]))
    ok("H2", not inside(V["river_pooled"], B["hind_river"]) and not inside(F["route_exp"]["river one offset"]["river"], B["exp_river"]),
       "one offset: River Road %d and %.1f" % (V["river_pooled"], F["route_exp"]["river one offset"]["river"]))
    ok("H3", not inside(V["front_rim"], B["hind_front"]) and not inside(F["front_sensor_days"], B["hind_front"]),
       "the drain rim %d and the sensor alone %d against %s" % (V["front_rim"], F["front_sensor_days"], B["hind_front"]))
    ok("H4", not inside(F["harbor_count_trend"], B["harbor_exp"]) and not inside(F["harbor_raw_skew"], B["harbor_exp"]),
       "the count trend %.1f and the raw residuals %.1f" % (F["harbor_count_trend"], F["harbor_raw_skew"]))
    ok("H5", not inside(F["harbor_poisson"][1], B["harbor_hi"]) and not inside(F["harbor_poisson"][0], B["harbor_lo"]),
       "the Poisson range %s" % F["harbor_poisson"])
    pairs = [tuple(sorted(p)) for k, p in F["routes"].items() if k != "golden"]
    ok("H6", len(set(pairs)) == len(pairs) and tuple(sorted(F["routes"]["golden"])) not in pairs,
       "four routes, four different wrong pairs")
    ok("H7", "oyster" not in F["call_keys"] and all(A.NAMES["oyster"] not in p for p in F["routes"].values()),
       "Oyster Creek Road bends like Marsh Road and is in no route's pair")
    ok("H8", not inside(R["careful_pair_hold"], B["pair_hold"]), "the hurried pair's own count %d" % R["careful_pair_hold"])
    for cid, good, msg in RES:
        print("%s  %-5s %s" % ("PASS" if good else "FAIL", cid, msg))
    nf = sum(1 for _, g, _ in RES if not g)
    print("checks: %d, %d FAIL" % (len(RES), nf))
    return 1 if nf else 0


if __name__ == "__main__":
    sys.exit(main())
