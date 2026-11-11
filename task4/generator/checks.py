"""The build's assertions on the cut pack: the input gates, the realism sweep, the bar block (R1 to R7 of
dataset-generation 7.1), every semantic fork row, the margins of the call and the distractors' deletion test.
Exit 1 on any failure."""
import json
import os
import re
import sys
import warnings
import zipfile

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402

import analysis as A  # noqa: E402
import build as B  # noqa: E402
import params as P  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
OK, BAD = [], []


def check(label, cond, detail=""):
    (OK if cond else BAD).append((label, detail))


def main():
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(TARGET))
    f = A.load(TARGET)
    z = A.zone_hours(f)
    t = A.timesheet(f)
    G = A.golden(f)
    H = A.hurried(f)

    # ---------------------------------------------------------------- input gates
    check("gate: ten or more usable files", len(files) >= 10, "%d files" % len(files))
    cats = {x.rsplit(".", 1)[1] for x in files}
    check("gate: two or more file categories", len({"csv"} & cats) + len({"xlsx"} & cats) + len({"pdf", "docx"} & cats) >= 3,
          ", ".join(sorted(cats)))
    rows = {x: sum(1 for _ in open(os.path.join(TARGET, x), encoding="utf-8")) - 1 for x in files if x.endswith(".csv")}
    check("gate: a CSV of 20,000 rows or more", max(rows.values()) >= 20000, "%d" % max(rows.values()))
    check("gate: a second CSV of 10 to 20 printed pages or more (500 rows)",
          sorted(rows.values())[-2] >= 500, str(sorted(rows.values())[-2]))
    check("gate: two distractors named only in metadata", len(meta["distractor_files"]) >= 2 and
          all(d in files for d in meta["distractor_files"]))
    check("gate: no file names a distractor, readme, dictionary or notes", not any(
        re.search(r"distract|readme|dictionary|notes|manifest|trap", x, re.I) for x in files))
    for x in files:
        if x.endswith(".xlsx"):
            with zipfile.ZipFile(os.path.join(TARGET, x)) as zz:
                names = " ".join(zz.namelist())
                body = zz.read("xl/workbook.xml").decode()
            check("gate: %s has no notes or readme sheet" % x, not re.search(r'name="(notes|readme|about)', body, re.I))
    loaded = set(B.FILES[k] for k in ("zone_hours", "pay_old", "pay_new", "archive", "budget27", "k_orders", "h_daily",
                                      "h_monthly", "item_master", "slotting", "pilot", "roster"))
    check("distractors: the golden reads neither distractor", not (set(meta["distractor_files"]) & loaded))

    # ---------------------------------------------------------------- realism sweep
    zh = f["zone_hours"]
    wk = z.groupby(["iy", "iw", "zone"])["lines"].sum().unstack("zone")
    check("realism: no two zones pick the same lines in a week", int((wk["P1"] == wk["P2"]).sum()) == 0)
    check("realism: no week repeats another's zone-hour block", not z.groupby(["iy", "iw"])["task_min"].sum().duplicated().any())
    tid = f["pilot_conf"]["task_id"].drop_duplicates().sort_values().diff().dropna()
    check("realism: pick task ids are not one constant step", tid.nunique() > 1)
    emp = pd.to_numeric(f["roster"]["employee_no"]).sort_values().diff().dropna()
    check("realism: employee numbers are not one constant step", emp.nunique() > 3)
    check("realism: the pilot's confirmations are at line level with their own picker sequences",
          f["pilot_conf"]["picker_id"].nunique() >= 4 and len(f["pilot_conf"]) > 20000)
    tot = [figs["agency_total"], figs["r1"]["P1"], figs["r1"]["P2"]]
    check("realism: no headline total is a round thousand", all(v % 1000 for v in tot), str(tot))
    names = set(f["roster"]["name"])
    check("realism: the roster's names are the drawn personas (38 drawn)", len(names) >= 20)
    check("dates: no zone-hour after the extract", z["date"].max() <= pd.Timestamp(P.DATA_END))
    check("dates: no payroll row after the extract", t["date"].max() <= pd.Timestamp(P.DATA_END))
    check("dates: the archive's last issue is the 2027 budget's", str(f["forecasts"]["issued"].max()) == "2026-10-15")

    # ---------------------------------------------------------------- the bar block (dataset-generation 7.1)
    check("R1 raw material: the zone hours carry task minutes, pickers and class counts, no time a line",
          {"task_min", "pickers_logged", "lines_cls_a"} <= set(zh.columns) and not any("per_line" in c for c in zh.columns))
    check("R1 raw material: the budgets carry order lines by week, no overstatement column",
          not any("over" in c for c in f["forecasts"].columns))
    # R2 mess neutral, one item at a time
    zd = pd.concat([f["zone_hours"], f["zone_hours"][f["zone_hours"]["date"].astype(str).isin(["2023-03-14", "2023-03-15", "2025-06-02"])]])
    fd = dict(f, zone_hours=zd)
    zz = A.zone_hours(fd)
    fit_dup = A.fit_time(zz.assign(task_min=zz["task_min"]), knot=G["fit"]["knot"], power=G["fit"]["power"], grid=False)
    check("R2 mess: the zone hours' double export left in moves the congestion term under 2 per cent",
          abs(A.cong(fit_dup, 1.8) / G["r3"] - 1.0) < 0.02)
    tt = f["timesheets"]
    with_pack = t.copy()
    check("R2 mess: packing hours sit only on their own cost centre", "PACK" not in G["r1"])
    b = f["forecasts"]
    first = b[~((b["round"] == "budget 2024") & (b["group"] == "bulky") & (b["issued"].astype(str) == "2023-10-27"))]
    r2_first = A.r2_overstatement(z, dict(f, forecasts=first))
    check("R2 mess: the 2024 bulky budget read at its first issue keeps the overstatement in its band",
          figs["bands"]["r2"][0] <= 100 * r2_first <= figs["bands"]["r2"][1], "%.2f" % (100 * r2_first))
    t_dup = A.timesheet(dict(f, timesheets=tt))
    check("R2 mess: the March 2024 correction run drops out", len(t_dup) < len(tt))
    # R3 each hurried figure off its band
    res = {r["id"]: r for r in E["results"]}
    for rid in ("R3", "R4", "R5", "R6"):
        r = res[rid]
        v = r["passes"]["careful"]
        check("R3 hurried: %s's careful figure %.2f sits outside its band %s" % (rid, v, r["band"]),
              not (r["band"][0] <= v <= r["band"][1]))
    check("R3 hurried: the careful route's evening cells differ from the golden's",
          sorted(res["R9"]["passes"]["careful"]) != sorted(res["R9"]["golden"]))
    check("R3 hurried: the careful route books fewer agency hours by a fifth or more",
          figs["hurried"]["agency_total"] < 0.8 * figs["agency_total"])
    # R4 no plant
    dr = pd.read_excel(os.path.join(TARGET, B.FILES["draft"]), header=3)
    check("R4 no plant: the draft's evening column reads 'to confirm' throughout",
          set(dr["Evening shift"].dropna()) == {"to confirm"})
    # R5 no one thing: footprints outside the deciding units
    dense_old = z[(z["iy"] <= 2023) & (z["dpa"] > 1.6) & z["zone"].isin(A.Z_SMALL)]
    check("R5 footprint: congestion shows in the 2022 and 2023 dense hours (outside the 2027 weeks)",
          len(dense_old) > 300, "%d hours" % len(dense_old))
    o = A.overstatement_by_year(z, f)
    g = A.plan_growth(f)
    o["plan"] = [g[(P.BRAND_K, y)][0 if grp == "small parts" else 1] for y, grp in zip(o["year"], o["group"])]
    check("R5 footprint: the overstatement rises with the plan's growth across every budget year",
          float(np.corrcoef(o["plan"], o["over"])[0, 1]) > 0.7, "%.3f" % float(np.corrcoef(o["plan"], o["over"])[0, 1]))
    bud = A.budgets(f)
    pkw = A.placed_by_week(f)
    for y in (2024, 2025):
        bb = bud[(bud["brand"] == P.BRAND_K) & (bud["group"] == "small parts") & (bud["iso_year"] == y)]
        bb = bb[bb["iso_week"].isin(P.PEAK_WEEKS)].set_index("iso_week")["order_lines"]
        pp = pkw[(pkw["iy"] == y) & pkw["iw"].isin(P.PEAK_WEEKS) & (pkw["group"] == "small parts")].set_index("iw")["lines"]
        sb, sp_ = bb[47] / bb.sum(), pp[47] / pp.sum()
        check("R5 footprint: the %d budget phased by %d's week numbers put more of the peak in week 47 than was placed "
              "there (%.3f against %.3f)" % (y, y - 2, sb, sp_), sb > sp_ + 0.03)
    hm = A.hui_mix(f)
    check("R5 footprint: Huippu Sport's full peak mix is heavier than the pilot's (class A share under a half)",
          hm["P1"]["shares"]["A"] < 0.5 and hm["P2"]["shares"]["A"] < 0.9)
    # R6 the one-fact test computed
    for fx, rt in figs["routes"].items():
        cells = sorted("%s-%d" % (zn, w) for zn in A.Z_SMALL for w in rt["evening"][zn])
        check("R6 one fact: the draft's route with only %s right misses the golden's evening cells" % fx,
              cells != sorted(res["R9"]["golden"]))
    # R7 the rivals
    for k, v in figs["rivals"]["cells"].items():
        check("R7 rivals: %s files the golden evening cells" % k, sorted(v) == sorted(res["R9"]["golden"]))
    bd = figs["bands"]
    for key, rk in (("r3", "r3"), ("r4", "r4"), ("r5_K_sp", "r5_K_sp"), ("r6", "r6"), ("r2", "r2")):
        for k, v in figs["rivals"][rk].items():
            check("R7 rivals: %s under %s (%.3f) inside its band %s" % (key, k, v, bd[key]), bd[key][0] <= v <= bd[key][1])
        gv = figs[key] if key != "r5_K_sp" else figs["r5"]["K_sp"]
        check("R7 bands: %s's golden %.3f sits inside its band" % (key, gv), bd[key][0] <= gv <= bd[key][1])
    # ruled out by named data
    Gd = A.golden(f, {"how": "date"})
    check("ruled out: a date alignment puts Black Friday 2025 on Sunday 28 November 2027 (and moves week 47)",
          Gd["evening"][("P1", 47)] is False or Gd["r6"] < 0.18)
    lin = A.fit_time(z, knot=0.8, power=1.0, grid=False)
    check("ruled out: a straight-line congestion term fits the zone hours at least three times worse",
          lin["sse"] > 3 * G["fit"]["sse"], "%.0f against %.0f" % (lin["sse"], G["fit"]["sse"]))
    nod = A.fit_time(z, with_density=False)
    check("ruled out: a fit without density returns an impossible class rate (D below A)",
          nod["coef"]["D"] < nod["coef"]["A"])

    # ---------------------------------------------------------------- the semantic fork rows
    check("SF1 the peak is ISO weeks 46 to 50 (standard 2.1)", list(P.PEAK_WEEKS) == [46, 47, 48, 49, 50])
    check("SF2 picker hours are worked paid hours; absence and packing excluded",
          (t[t["absence"] != ""]["paid"] == 0).all())
    check("SF3 lines are the WMS's order lines picked", G["plan"][("P1", 47)]["lines"] > 0)
    r2_mean = figs["rivals"]["r2"]["mean of the years' ratios"]
    picked_basis = 100 * A.r2_overstatement(z, f, basis="picked")
    check("SF4 ruled out: the lines picked in the peak weeks are another quantity (the peaks' backlog spills into "
          "week 51), %.1f against the placed basis" % picked_basis, abs(picked_basis - figs["r2"]) > 2.0)
    check("SF4 the overstatement as a ratio of totals or a mean of the years' ratios lands in one band",
          bd["r2"][0] <= r2_mean <= bd["r2"][1], "%.2f" % r2_mean)
    roll = f["forecasts"][f["forecasts"]["round"].str.startswith("rolling")]
    check("SF5 the year-ahead forecasts are the October budget rounds (rolling issues run 13 weeks)",
          int(roll.groupby("issued").size().max()) <= 26)
    check("SF6 the 2024 bulky re-issue: latest or first issue, one band", bd["r2"][0] <= 100 * r2_first <= bd["r2"][1])
    check("SF7 the aisles by era are the standard's (8 and 7 before 8 January 2024)",
          P.AISLES_OLD == {"P1": 8, "P2": 7, "B1": 6} and P.AISLES["P1"] == 12)
    check("SF8 the time a line is WMS task time (the Huippu difference in task minutes)",
          abs(figs["r4"] - round(G["t_hui"] - G["t_kot"], 2)) < 0.011)
    check("SF9 the evening rule: the day shifts at the limit, then the evenings (standard 3.4)",
          all(G["plan"][(zn, w)]["n_day"] == P.LIMIT[zn] for zn in A.Z_SMALL for w in P.PEAK_WEEKS
              if G["plan"][(zn, w)]["evening"]))
    check("SF10 own hours on every working weekday less the 2025 peak's sickness (standard 4.1)",
          all(0.0 < A.sickness(t, zn) < 0.2 for zn in P.ZONES))
    check("SF11 the range covers the volume and the time a line (standard 3.5)",
          figs["sd"]["level"] > 0 and figs["sd"]["week"] > 0 and figs["sd"]["model"] > 0)
    ko = f["k_orders"]
    ko = ko[ko["group"] == "small parts"].copy()
    ko["received"] = pd.to_datetime(ko["received"])
    ser = ko.set_index("received")["web_lines"]
    dp = z[z["zone"].isin(A.Z_SMALL)].groupby("date")["kot"].sum()
    j = pd.DataFrame({"pick": dp, "same": ser.reindex(dp.index), "prev": ser.shift(1).reindex(dp.index)}).dropna()
    j = j[j.index.weekday.isin([1, 2, 3])]
    check("SF12 the release rule: a midweek day's picks follow the day before's orders, not its own (standard 2.4)",
          np.corrcoef(j["pick"], j["prev"])[0, 1] > np.corrcoef(j["pick"], j["same"])[0, 1])
    check("SF13 Huippu Sport's budget on the same basis as Kotikaari's (the cover sheet)",
          figs["r5"]["H_sp"] != figs["r2"])
    check("SF14 the 2027 closures: week 49 has five day shifts and week 51 is outside the peak",
          A.days_2027(49) == (5, 4) and A.days_2027(46) == (6, 5))

    Ga = A.golden(f, {"src": "avg"})
    check("SF15 the profile from 2025's days or 2024's and 2025's averaged lands the same cells and R6 in its band",
          Ga["evening"] == G["evening"] and bd["r6"][0] <= 100 * Ga["r6"] <= bd["r6"][1])
    Gq = A.golden(f, {"cong": "quad"})
    cub = A.fit_time(z, knot=0.4, power=3.0, grid=False)
    check("SF16 the congestion form: a quadratic lands the same cells; a straight line and a cubic fit worse",
          Gq["evening"] == G["evening"] and lin["sse"] > G["fit"]["sse"] and cub["sse"] > G["fit"]["sse"])

    # ---------------------------------------------------------------- margins
    for zn in A.Z_SMALL:
        for w in P.PEAK_WEEKS:
            rr = G["plan"][(zn, w)]["ratio"]
            check("margin: %s week %d at %.2f of the day shifts' capacity, 10 per cent or more from the line" % (zn, w, rr),
                  rr >= 1.10 or rr <= 0.90)
    check("forcing: every perturbation holds the golden cells", all(
        sorted(p["answer"]) == sorted(res["R9"]["golden"]) for p in E["forcing"]["perturbations"]))
    check("effort: different shortcuts land on three or more different wrong sets",
          len({json.dumps(sorted(r["answer"])) for r in E["routes"] if not r.get("golden")}) >= 3)
    check("effort: no single hint rescues more than one result", all(len(h["rescues"]) <= 1 for h in E["hints"]))

    for label, d in BAD:
        print("FAIL  %s  %s" % (label, d))
    print("checks: %d passed, %d failed" % (len(OK), len(BAD)))
    sys.exit(1 if BAD else 0)


if __name__ == "__main__":
    main()
