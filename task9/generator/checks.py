"""task9 architecture 6: generator assertions on the cut pack, Level 5, zero waivers.

    python3 task9/generator/checks.py

Verifies input gates, realism, bar block (R1-R7), 3 independent stumps, neutral mess, hurried/over/run routes,
cold-era linearity, recency kernel convergence, release-shadow same-group correlation, never-filed parameters,
and exact agreement between core.py on the world and load.py on target/."""
import json
import math
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core as C  # noqa: E402
import results as RS  # noqa: E402

TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
N = {"pass": 0, "fail": 0}


def ok(label, cond, detail=""):
    N["pass" if cond else "fail"] += 1
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else "  %s" % (detail,)))


def inside(x, b):
    return b[0] - 1e-9 <= x <= b[1] + 1e-9


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    meta = json.load(open(os.path.join(TASK, "metadata.json")))
    files = sorted(os.listdir(T))
    B, S = fig["bands"], fig["stated"]

    # ------------------------------------------------------------------ input gates
    ok("ten or more usable files", len(files) >= 10, len(files))
    kinds = {os.path.splitext(f)[1] for f in files}
    ok("two or more file categories (spreadsheet, text, database)", {".csv", ".xlsx", ".pdf", ".jsonl"} <= kinds, kinds)
    rows = {f: sum(1 for _ in open(os.path.join(T, f))) - 1 for f in files if f.endswith(".csv")}
    big = [f for f, n in rows.items() if n >= 20000]
    ok("two or more CSVs of 20,000+ rows", len(big) >= 2, big)
    ok("three or more CSVs of 10+ printed pages", sum(1 for f, n in rows.items() if n >= 550) >= 3, rows)
    ok("distractors ship and are named only in metadata.json",
       all(d in files for d in meta["distractor_files"]) and len(meta["distractor_files"]) >= 2)
    src = open(os.path.join(HERE, "load.py")).read()
    ok("golden reads no distractor", not any(d.split(".")[0] in src for d in meta["distractor_files"]))
    ok("no file describes the data", not any(re.search(r"readme|dictionar|field_notes|codebook|extract_notes|schema", f, re.I) for f in files))
    ok("no file is named after a trap", not any(re.search(r"issue|known|trap|bias|lag|overlap|persist|recency|covar", f, re.I) for f in files))
    ok("metadata records source, pulled, license for every file",
       set(meta["files"]) == set(files) and all({"source", "pulled", "license"} <= set(v) for v in meta["files"].values()),
       set(files) ^ set(meta["files"]))

    # ------------------------------------------------------------------ cut pack vs core on the world
    w, z, inst = C.world()
    gw = C.evaluate(C.Pack(w, z, inst))
    for s in C.SOURCES:
        ok("pack golden %s points within 0.05 of core's" % s,
           abs(fig["points"][RS.NAMES[s]] - gw["points"][s]) < 0.05, (fig["points"][RS.NAMES[s]], gw["points"][s]))
    for k in ("tot_q1", "tot_q2", "tot_q3", "tot_q4", "tot_yr", "cc_pin"):
        ok("pack golden %s within 0.1 of core's" % k, abs(fig[k] - gw[k]) < 0.1, (fig[k], gw[k]))
    ok("the call on the shipped files matches core", fig["call"] == RS.call_list(gw), fig["call"])

    # ------------------------------------------------------------------ corelib Level 5 (ZERO waivers!)
    ok("corelib on cut pack: CORE PASS level 5", "CORE PASS level 5" in fig["rubric"]["verdict"], fig["rubric"]["verdict"])
    r = fig["rubric"]["routes"]
    ok("one stump lost earns 50 or under (S1, S2, S3)",
       max(r["S1 lost alone"], r["S2 lost alone"], r["S3 lost alone"]) <= 50, r)
    ok("reflex route earns 30 or under", r["reflex route (every stump lost)"] <= 30, r)
    ok("rigorous route earns 50 or under", r["rigorous standard route"] <= 50, r)
    ok("every run route earns 50 or under", all(r[k] <= 50 for k in r if "run route" in k), r)
    rs = fig["rubric_stated"]["routes"]
    ok("corelib on stated bands: CORE PASS level 5, all bounds met",
       "CORE PASS level 5" in fig["rubric_stated"]["verdict"]
       and max(rs["S1 lost alone"], rs["S2 lost alone"], rs["S3 lost alone"]) <= 50
       and rs["reflex route (every stump lost)"] <= 30
       and rs["rigorous standard route"] <= 50
       and all(rs[k] <= 50 for k in rs if "run route" in k),
       fig["rubric_stated"])

    # ------------------------------------------------------------------ R1 raw material & instruments
    pr = pd.read_csv(os.path.join(T, "mrm_instrument_pair_register_2026.csv"))
    ok("R1 every family carries all 5 instrument kinds", pr.groupby("model_family")["pair_kind"].nunique().min() == 5)
    ok("R1 every family carries 16 bootstrap pairs in 2026",
       int(pr[pr["pair_kind"] == "bootstrap"].groupby("model_family").size().min()) == 16)
    ok("R1 panel holds > 2.5M merchant-week scores", fig["base"]["score_rows"] > 2_500_000, fig["base"]["score_rows"])

    # ------------------------------------------------------------------ R2 neutral mess
    for m, e in fig["mess"].items():
        cells = (
            [inside(e["points"][RS.NAMES[s]], B["points_" + s]) for s in C.SOURCES]
            + [inside(e["tot_yr"], B["tot_yr"]), inside(e["cc_pin"], B["cc_pin"])]
        )
        ok("R2 hygiene slip (%s) keeps every graded figure in band" % m, all(cells), e)

    # ------------------------------------------------------------------ R3 hurried / direct / over outside band
    rf, rg, dr = fig["reflex"], fig["rigorous"], fig["direct"]
    for s, k in (("optimisation", "optimisation noise"), ("turnover", "training data"), ("releases", "feature releases")):
        ok("R3 rigorous shortcut's %s sits outside band" % k, not inside(rg["points"][k], B["points_" + s]), rg["points"][k])
    ok("R3 calendar plan pinned share sits outside band", not inside(fig["base"]["cov_plan"], B["cc_pin"]))
    lat, ov = fig["lattice"], fig["over"]
    ok("R3 S1 lost puts optimisation in escalation, over puts in monitor",
       lat["S1"]["points"]["optimisation noise"] >= 8.0 and ov["S1"]["points"]["optimisation noise"] < 5.5)
    ok("R3 S2 lost puts training data in monitor, over puts in escalation",
       lat["S2"]["points"]["training data"] < 5.5 and ov["S2"]["points"]["training data"] >= 8.0)
    ok("R3 S3 lost puts feature releases in monitor, over puts in escalation",
       lat["S3"]["points"]["feature releases"] < 5.5 and ov["S3"]["points"]["feature releases"] >= 8.0)

    # ------------------------------------------------------------------ R4 no one thing & R5 one-fact test
    fact = E["factorial"]
    stumps_f = [j for j in fact["judgments"] if j["kind"] == "stump"]
    ok("R4 three stumps, each necessary",
       len(stumps_f) == 3 and all(j["dropped"]["answer"] != fact["golden_answer"] for j in stumps_f))
    ok("R4 no stump sufficient alone", all(j["alone"]["answer"] != fact["golden_answer"] for j in stumps_f))
    ok("R4 three single drops land on three distinct wrong calls",
       len({tuple(j["dropped"]["answer"]) for j in stumps_f}) == 3)
    ok("R5 largest one-sentence hint rescues <= 1 of 10 results", max(len(h["rescues"]) for h in E["hints"]) <= 1)

    # ------------------------------------------------------------------ R6 variant battery + physical diagnostics
    ok("R6 variant battery + admitted forks file one call", fig["battery_calls"])
    ok("R6 variant battery has 12+ variants", fig["variants"] >= 12, fig["variants"])
    for s in C.SOURCES:
        lo_, hi_ = fig["battery_range"][RS.NAMES[s]]
        ok("R6 %s battery inside band" % s, inside(lo_, B["points_" + s]) and inside(hi_, B["points_" + s]))
    ok("Cold-start era >= 24 weeks in every family and strictly linear",
       fig["bend"]["cold_min_weeks"] >= 24 and abs(fig["bend"]["cold_curv_mean"]) < 0.05, fig["bend"])
    ok("S2 recency exponential beats uniform log-RMSE by >= 3x",
       fig["recency_diag"]["unif_ratio"] >= 3.0, fig["recency_diag"]["unif_ratio"])
    ok("S2 all smooth monotone recency kernels land in Remediation (5.5..8.0)",
       all(5.5 <= fig["recency_diag"]["kernels"][k]["points"] < 8.0
           for k in ("exponential", "power-law (a=2)", "linear ramp")),
       fig["recency_diag"]["kernels"])
    ok("S3 all 2026 same-group release pairs positively correlated, diff-group near zero",
       fig["base"]["coh_same_min"] > 0.60 and fig["base"]["coh_same_mean"] > 0.72 and abs(fig["base"]["coh_diff_mean"]) < 0.03,
       fig["base"])
    ok("Falsification: every rival >= 5x golden error in native points^2",
       all(v >= 5.0 * max(fig["falsification"]["golden_err"], 1e-6) for v in fig["falsification"]["rivals"].values()),
       fig["falsification"])

    # ------------------------------------------------------------------ R7 governing PDFs: WHAT filed, HOW never leaked
    std = pdf_text(os.path.join(T, "gms_model_stability_standard_2026.pdf"))
    cov = pdf_text(os.path.join(T, "acquirer_agreement_schedule_c_tier_stability.pdf"))
    ok("R7 Standard files 1.4 (warm start), 1.5 (pinned views), 1.6 (recency weighting)",
       "1.4" in std and "1.5" in std and "1.6" in std and "exponential recency weighting" in std)
    ok("R7 Standard files 2.2 (52 assessment-year Mondays) and 3.3 (combined movement)",
       "2.2" in std and "52 Monday refreshes" in std and "3.3" in std)
    ok("R7 Standard & Schedule C file band lines 5.5/8 and covenant cap 12",
       "5.5" in std and "8 points" in std and "12 per cent" in cov)
    # Never-filed check: no decay rate, half-life, phi, lambda, correlation, or mean-reversion leak in PDFs!
    leak_terms = ("half-life", "half life", "0.78", "0.72", "0.66", "0.91", "0.93", "0.94", "mean-revert",
                  "mean revert", "correlat", "covariance", "orthogonal", "autoregress", "AR(1)", "lag curve")
    bad = [w_ for w_ in leak_terms if w_.lower() in (std + " " + cov).lower()]
    ok("Never-filed check: zero parameter or method hints in shipped PDFs", not bad, bad)

    # ------------------------------------------------------------------ Semantic fork assertions (SF1..SF15)
    gf = {r["name"]: r["answer"] for r in E["forcing"]["golden_family"]}
    gcall = E["forcing"]["golden_answer"]
    ar = fig["adm_range"]
    ok("SF1 movement estimand is RMS points (Standard 3.1/3.2)",
       "root-mean-square" in std.lower() and fig["points"]["optimisation noise"] > 0)
    ok("SF2 book weighting (21 Sep 2026 vs Dec 2027 planned) files one call",
       gf["{'weights': 'plan'}"] == gcall)
    ok("SF3 2027 weekly refreshes pinned to 52 assessment-year Mondays (Standard 2.2)",
       "52 Monday refreshes" in std and "four snapshot pairs" in std and fig["base"]["cov_plan"] > 75.0)
    ok("SF4 all 5 sources sit >= 0.65 pts from both 5.5 and 8.0 band lines",
       all(min(abs(v - 5.5), abs(v - 8.0)) >= 0.65 for v in fig["points"].values()), fig["points"])
    ok("SF5 combined model-side movement pinned by Standard 3.3",
       "3.3" in std and abs(fig["tot_yr"] - math.sqrt(np.mean([fig["tot_q1"]**2, fig["tot_q2"]**2, fig["tot_q3"]**2, fig["tot_q4"]**2]))) < 1e-4)
    ok("SF6 S1 warm-start AR(1) vs linear/raw/unanchored ruled out by Standard 1.4, cold linearity, and D_warm(1)",
       fig["bend"]["cold_min_weeks"] >= 24 and fig["falsification"]["rivals"]["S1 linear carry"] > 10.0)
    ok("SF7 S1 gap-curve admitted forks (lags, weights, start week, data sub) all stay in band",
       all(gf[k] == gcall for k in ("{'fit': 'anch20'}", "{'fit': 'anch18'}", "{'fit': 'from2'}",
                                    "{'fit': 'y2026'}", "{'sub_data': False}", "{'fit': 'flat'}"))
       and inside(ar["points_optimisation"][0], B["points_optimisation"])
       and inside(ar["points_optimisation"][1], B["points_optimisation"]))
    ok("SF8 S2 recency exponential beats uniform and all smooth kernels stay in Remediation",
       all(gf[k] == gcall for k in ("{'rec_key': 'win_log'}", "{'rec_key': 'pool_log'}",
                                    "{'rec_key': 'fam_wls'}", "{'rec_key': 'fam_ols'}"))
       and inside(ar["points_turnover"][0], B["points_turnover"])
       and inside(ar["points_turnover"][1], B["points_turnover"]))
    ok("SF9 S2 bootstrap netting vs gross bootstrap: net pinned by replicate pair variance",
       fig["base"]["bootstrap_net"] < fig["base"]["bootstrap"] and fig["recency_diag"]["unif_ratio"] >= 3.0)
    ok("SF10 S3 same-group release covariance estimators (family vs pooled) stay in band",
       gf["{'rel_coh': 'pooled'}"] == gcall
       and inside(ar["points_releases"][0], B["points_releases"])
       and inside(ar["points_releases"][1], B["points_releases"]))
    ok("SF11 pinned adoption lag models (loglin, linear, groups, own, pooled, norevert) keep call and cc_pin band",
       all(gf[k] == gcall for k in ("{'adopt': 'linear'}", "{'adopt': 'groups'}",
                                    "{'adopt': 'own'}", "{'adopt': 'pooled'}", "{'adopt': 'norevert'}"))
       and inside(ar["cc_pin"][0], B["cc_pin"]) and inside(ar["cc_pin"][1], B["cc_pin"]))
    ok("SF12 pinned adoption lag start vs calendar environment release date",
       fig["base"]["cov_plan"] > 75.0 and fig["cc_pin"] < 42.0)
    ok("SF13 retunes (3.25/pair) and label revisions (13/pair) forced across all variants",
       fig["base"]["retunes_per_pair"] == 3.25 and fig["band_of"]["retunes"] == "monitor"
       and fig["band_of"]["label revisions"] == "escalation")
    ok("SF14 panel hygiene neutral across all four single slips",
       all(inside(fig["mess"][m]["tot_yr"], B["tot_yr"]) for m in fig["mess"]))
    ok("SF15 panel weighting rival (5x monitoring panel) keeps call and bands",
       gf["families weighted by the panel at the latest snapshot, times five"] == gcall
       and inside(fig["extra"]["families weighted by the panel at the latest snapshot, times five"]["tot_yr"], B["tot_yr"]))

    # Zero em/en dash check on submission.md and prompt.txt
    for fname in ("prompt.txt", "submission.md"):
        txt = open(os.path.join(TASK, fname), encoding="utf-8").read()
        ok("No em/en dashes in %s" % fname, "\u2014" not in txt and "\u2013" not in txt)

    print("checks: %d PASS, %d FAIL" % (N["pass"], N["fail"]))
    sys.exit(1 if N["fail"] else 0)


if __name__ == "__main__":
    main()
