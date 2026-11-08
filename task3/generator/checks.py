"""task3 architecture 3: the generator's assertions on the cut pack and the rungs (generator/rungs.json).

    python3 task3/generator/checks.py <target> <rungs.json>

The Sulfur block (R1 to R6), the ladder, the fork table (SF1 to SF8), the input gates, the realism sweep and the
distractor deletion test. Exit 1 on any failure."""
import csv
import json
import math
import os
import re
import sys

import openpyxl

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build  # noqa: E402
import solve as S  # noqa: E402

RESULTS = []


def check(label, ok, detail=""):
    RESULTS.append((label, bool(ok), detail))


def ft(x):
    return int(math.floor(x + 0.5))


def bins(r):
    return [ft(r["peaks"][str(o)]) for o in S.OPTIONS]


def main(target, rungs_path):
    R = json.load(open(rungs_path))
    g = R["golden"]
    gb = bins(g)
    files = sorted(os.listdir(target))

    # ---------------------------------------------------------------- R1 the field's raw material ships
    n_tr = sum(1 for _ in open(os.path.join(target, build.FILES["transducers"]))) - 1
    check("R1 the logger export carries minute readings at six wells (20,000 rows or more)", n_tr >= 20000, n_tr)
    headers = []
    for f in files:
        if f.endswith(".csv"):
            headers += next(csv.reader(open(os.path.join(target, f))))
        if f.endswith(".xlsx"):
            wb = openpyxl.load_workbook(os.path.join(target, f), read_only=True)
            for ws in wb.worksheets:
                headers += [str(c) for c in next(ws.iter_rows(values_only=True)) if c]
    bad = [h for h in headers if re.search(r"drawdown|leak|transmiss|storativ|natural|attribut", h, re.I)]
    check("R1 no shipped column holds a drawdown, a leakage, an aquifer property or a natural level", not bad, bad)

    # ---------------------------------------------------------------- the ladder
    check("golden files 1,000 gpm", g["call"] == 1000, g["call"])
    check("golden peaks sit at 4, 6, 8 and 10 ft", gb == [4, 6, 8, 10], gb)
    check("R4 link 3 skipped is ruled out by the record: its hindcast of MS-MW misses by 0.3 ft or more",
          abs(R["chain3_test_leaky"]["msmw_2025_model"] - g["msmw_2025"]) >= 0.3, R["chain3_test_leaky"]["msmw_2025_model"])
    check("golden: every schedule's greatest month in the term falls in 2046",
          all(v == 2046 for v in g["peak_year"].values()), g["peak_year"])
    check("golden: 1,000 gpm clears the limit by 0.5 ft or more", S.LIMIT - g["peaks"]["1000"] >= 0.5, g["peaks"]["1000"])
    check("golden: 1,250 gpm exceeds the limit by 0.5 ft or more", g["peaks"]["1250"] - S.LIMIT >= 0.5, g["peaks"]["1250"])
    for k in ("450", "700", "1000", "1250"):
        v = g["peaks"][k]
        check("golden %s gpm peak at least 0.08 ft from a rounding edge" % k, abs(v - math.floor(v) - 0.5) >= 0.08, v)
    check("golden MS-MW 2025 drawdown rounds to 5 ft, 0.2 ft or more from an edge",
          ft(g["msmw_2025"]) == 5 and abs(g["msmw_2025"] - math.floor(g["msmw_2025"]) - 0.5) >= 0.2, g["msmw_2025"])
    check("rung 0 (Theis from the test) files none of the schedules", R["rung0_theis"]["call"] is None,
          R["rung0_theis"]["call"])
    check("rung 0's own hindcast puts MS-MW's 2025 drawdown at twice the golden or more",
          R["theis_msmw_2025"] >= 2 * g["msmw_2025"], (R["theis_msmw_2025"], g["msmw_2025"]))
    for k in ("rung1_raw", "rung1_cv07", "rung1_trend", "rung1_cv07_clean"):
        check("%s files 1,250 gpm" % k, R[k]["call"] == 1250, R[k]["call"])
        check("%s misses three or more A1 cells" % k, sum(a != b for a, b in zip(bins(R[k]), gb)) >= 3, bins(R[k]))
    check("rung 1 (CV-07) misses A2", ft(R["rung1_cv07"]["msmw_2025"]) != ft(g["msmw_2025"]), R["rung1_cv07"]["msmw_2025"])
    check("rung 1 (raw) misses A2", ft(R["rung1_raw"]["msmw_2025"]) != ft(g["msmw_2025"]), R["rung1_raw"]["msmw_2025"])
    check("dominance: the rung 1 leakage factor is under two thirds of the golden's",
          R["rung1_cv07"]["B"] < 0.67 * g["B"], (R["rung1_cv07"]["B"], g["B"]))

    # ---------------------------------------------------------------- R3 the analyst test and the decisive step alone
    check("R3a the default path (leaky calibrated against CV-07) files a wrong answer", R["rung1_cv07"]["call"] != g["call"])
    check("R3b the default path with only the reference changed (CV-02 and CV-11) files the golden",
          g["call"] == 1000 and R["rung1_cv07"]["call"] == 1250)
    check("R3b each lower rung's single correction stays wrong (raw, trend, CV-07 mixed with the far wells)",
          all(R[k]["call"] != 1000 for k in ("rung1_raw", "rung1_trend", "rung1_cv07_clean")))
    check("R3c no plant: the pack carries no memo, draft or figure stating a drawdown or a leakage factor",
          not any(re.search(r"memo|draft_|briefing", f, re.I) for f in files), files)

    # ---------------------------------------------------------------- R4 the chain, link by link
    check("R4 link 1 skipped (the test's fit carried forward) files a wrong call", R["rung0_theis"]["call"] != 1000)
    check("R4 link 2 skipped (no clean reference) files a wrong call", R["rung1_raw"]["call"] != 1000)
    check("R4 link 3 skipped (the leakage read from the test alone) files a wrong call",
          R["chain3_test_leaky"]["call"] != 1000, R["chain3_test_leaky"])
    check("R4 link 4 skipped (annual averages, no monthly schedule) files a wrong call",
          R["chain4_annual"]["call"] != 1000, R["chain4_annual"]["call"])

    # ---------------------------------------------------------------- R5 the one-fact test
    check("R5 the hint 'the aquifer leaks' leaves the default path on 1,250 gpm (it already fits a leaky aquifer)",
          R["rung1_cv07"]["call"] == 1250 and R["rung1_raw"]["call"] == 1250)

    # ---------------------------------------------------------------- R6 the rivals, every standing one on the call
    for k in R["standing"]:
        check("R6 rival %s files 1,000 gpm" % k, R[k]["call"] == 1000, R[k]["call"])
        check("R6 rival %s lands every A1 cell" % k, bins(R[k]) == gb, bins(R[k]))
        check("R6 rival %s lands A2" % k, ft(R[k]["msmw_2025"]) == ft(g["msmw_2025"]), R[k]["msmw_2025"])
    gdw = ft(g["dw"])
    check("A3 golden: the nearest domestic well is DW-17", g["dw_id"] == "DW-17", g["dw_id"])
    check("A3 golden DW-17 2046 peak at least 0.12 ft from a rounding edge", abs(g["dw"] - math.floor(g["dw"]) - 0.5) >= 0.12, g["dw"])
    for k in R["plate_readings"]:
        check("A3 plate reading %s lands DW-17" % k, ft(R[k]["dw"]) == gdw, R[k]["dw"])
    check("A3 the walls left out (the calibration fits without them) misses DW-17", ft(R["walls_none"]["dw"]) != gdw,
          R["walls_none"]["dw"])
    check("A2 the like-for-like slip (far wells anchored to 2005 to 2008) misses MS-MW",
          ft(R["msmw_anchor_slip"]) != ft(g["msmw_2025"]), R["msmw_anchor_slip"])
    prof = R["ows_only_profile"]["range_within_chi2"]
    check("R6 the OW-S-only rival is ruled out by the record it leaves out: its model misses MS-MW's 2025 drawdown by "
          "0.4 ft or more", abs(R["rival_ows_only"]["msmw_2025_model"] - g["msmw_2025"]) >= 0.4,
          (R["rival_ows_only"]["msmw_2025_model"], g["msmw_2025"]))
    jp = R["joint_profile"]["range_within_chi2"]
    check("the golden's joint calibration pins the leakage factor within 25 per cent", jp[1] <= 1.25 * jp[0], jp)
    check("the golden's model reproduces MS-MW's 2025 drawdown within 0.15 ft",
          abs(g["msmw_2025_model"] - g["msmw_2025"]) <= 0.15, (g["msmw_2025_model"], g["msmw_2025"]))

    # ---------------------------------------------------------------- the decisive evidence is in the data
    check("CV-07's departure from the far wells grew 1 ft or more from 2008 to 2025",
          R["cv07_departure"]["2025"] - R["cv07_departure"]["2008"] <= -1.0, R["cv07_departure"])
    check("CV-07's departure follows the Mill Street pumping (correlation 0.4 or more)", R["cv07_pump_corr"] >= 0.4,
          R["cv07_pump_corr"])
    check("CV-02 less CV-11 does not follow the pumping (|correlation| under 0.25)", abs(R["far_pair_pump_corr"]) < 0.25,
          R["far_pair_pump_corr"])
    check("OW-S moved with the far wells before 2009 (correlation 0.8 or more)", R["ows_far_pre_corr"] >= 0.8,
          R["ows_far_pre_corr"])
    check("the golden reproduces MS-MW's drawdown to 0.3 ft rms", R["golden_resid"]["MS-MW"] <= 0.3, R["golden_resid"])

    # ---------------------------------------------------------------- the fork table
    check("SF1 drawdown is the withdrawals' (raw reading against its 2005 to 2008 level files 1,250 gpm)",
          R["rung1_raw"]["call"] == 1250)
    check("SF2 the Mill Street future is the filed projection (Rule WR-4 2.2), carried in the application",
          True, "filed")
    check("SF3 monthly, not annual: the annual-average route files another call, ruled out by Rule WR-4 4.1 and 4.3",
          R["chain4_annual"]["call"] != 1000)
    check("SF4 walls from 4,000 ft to none: same call", all(R[k]["call"] == 1000 for k in ("walls_4000", "walls_6500", "walls_none")))
    check("SF5 T and S from any observation well: same call",
          all(R[k]["call"] == 1000 for k in ("test_ow1", "test_ow2", "test_ow3", "test_five")))
    check("SF6 readings with TW-1 running kept: same call (it moves the ledgered asks only)", R["keep_running"]["call"] == 1000)
    check("SF7 CV-02 or CV-11 alone: same call", R["ref_cv02"]["call"] == 1000 and R["ref_cv11"]["call"] == 1000)
    check("SF8 the Reidel Road start: the application files April 2027", True, "filed")
    check("SF9 the domestic well with the plate's walls (7 ft) against none (6 ft): ruled out by Plate 3's mapped edges",
          ft(R["walls_none"]["dw"]) != ft(g["dw"]) and all(ft(R[k]["dw"]) == ft(g["dw"]) for k in R["plate_readings"]))

    # ---------------------------------------------------------------- R2 mess neutrality
    for k in ("no_baro", "clock_naive", "no_rehang", "keep_running"):
        check("R2 %s leaves the call at 1,000 gpm" % k, R[k]["call"] == 1000, R[k]["call"])

    # ---------------------------------------------------------------- input gates
    cats = {"spreadsheet" if f.endswith((".csv", ".xlsx")) else "text" if f.endswith(".pdf") else "image"
            for f in files}
    check("ten or more usable files", len(files) >= 10, len(files))
    check("two or more file categories", len(cats) >= 2, cats)
    n_net = sum(1 for _ in open(os.path.join(target, build.FILES["network"]))) - 1
    check("a long messy CSV (the network export) runs 10 printed pages or more (500 rows or more)", n_net >= 500, n_net)
    for d in (build.FILES["step"], build.FILES["quality"]):
        check("distractor %s ships and the solution never reads it" % d, d in files and d not in S.FILES.values())
    check("no file name says distractor, decoy or trap", not any(re.search(r"distract|decoy|trap", f, re.I) for f in files))

    # ---------------------------------------------------------------- realism
    rows = list(csv.DictReader(open(os.path.join(target, build.FILES["network"]))))
    dup = len(rows) - len({(r["site_id"], r["date"]) for r in rows})
    check("the network export carries keyed-twice rows (texture)", 3 <= dup <= 40, dup)
    regw = openpyxl.load_workbook(os.path.join(target, build.FILES["register"]), read_only=True)
    eastings = sorted(r[3] for r in list(regw["Wells"].iter_rows(values_only=True))[1:])
    steps = {round(b - a, 1) for a, b in zip(eastings, eastings[1:])}
    check("register coordinates are not an arithmetic sequence", len(steps) > 3, steps)
    for f in files:
        if f.endswith(".csv"):
            txt = open(os.path.join(target, f), encoding="utf-8").read()
            check("no em dash in %s" % f, "—" not in txt)
    check("the 9.0 ft limit is filed once (Rule WR-4 Table 1), not in the application",
          True, "application text carries no limit (asserted in verify.py by extraction)")

    fails = [r for r in RESULTS if not r[1]]
    for label, ok, detail in RESULTS:
        if not ok:
            print("FAIL  %s  %s" % (label, detail))
    print("checks: %d of %d PASS" % (len(RESULTS) - len(fails), len(RESULTS)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2]))
