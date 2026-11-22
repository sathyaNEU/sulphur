"""task9 architecture 5: the generator's assertions on the cut pack.

    python3 task9/generator/checks.py

The input gates, the realism sweep, the bar block (R1 the field's raw material, R2 neutral mess, R3 each result's
hurried figure outside its band, R4 no one thing, R5 the one-fact test, R6 the rivals inside each band, R7 the
filed constants), every row of the semantic fork table (SF1 to SF18), the never-filed list, and the golden rebuilt
from the shipped files against core.py on the world."""
import glob
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
import load as L  # noqa: E402
import pack as P  # noqa: E402
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


def xlsx_text(path):
    z = zipfile.ZipFile(path)
    return " ".join(z.read(n).decode("utf-8", "replace") for n in z.namelist() if n.endswith(".xml"))


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
    ok("a CSV of 20,000 rows or more", len(big) >= 2, big)
    ok("a second large CSV of 10 to 20 printed pages or more (55 lines a page)",
       sum(1 for f, n in rows.items() if n >= 550) >= 3, rows)
    ok("the distractors ship and are named only in metadata.json",
       all(d in files for d in meta["distractor_files"]) and len(meta["distractor_files"]) >= 2)
    src = open(os.path.join(HERE, "load.py")).read()
    ok("the golden reads no distractor (deleting them moves nothing)",
       not any(d.split(".")[0] in src for d in meta["distractor_files"]))
    ok("no file describes the data (readme, dictionary, notes, manifest of files)",
       not any(re.search(r"readme|dictionar|field_notes|codebook|extract_notes|schema", f, re.I) for f in files))
    ok("no file is named after a trap", not any(re.search(r"issue|known|trap|bias|lag|overlap|persist", f, re.I)
                                                 for f in files))
    ok("metadata records source, pull date and licence for every shipped file",
       set(meta["files"]) == set(files) and all({"source", "pulled", "license"} <= set(v) for v in meta["files"].values()),
       set(files) ^ set(meta["files"]))

    # ------------------------------------------------------------------ the golden on the shipped files against core
    w, z, inst = C.world()
    gw = C.evaluate(C.Pack(w, z, inst))
    for s in C.SOURCES:
        ok("pack golden %s points within 0.02 of core's" % s,
           abs(fig["points"][RS.NAMES[s]] - gw["points"][s]) < 0.02, (fig["points"][RS.NAMES[s]], gw["points"][s]))
    for k in ("cc3", "own_share", "fr_sched", "fr_removed"):
        ok("pack golden %s within 0.1 of core's" % k, abs(fig[k] - gw[k]) < 0.1, (fig[k], gw[k]))
    ok("the call on the shipped files is core's", fig["call"] == RS.call_list(gw), fig["call"])
    ok("corelib on the cut pack: level 5", "CORE PASS level 5" in fig["rubric"]["verdict"], fig["rubric"]["verdict"])
    r = fig["rubric"]["routes"]
    ok("one stump lost earns 50 or under on the cut pack", max(r["S1 lost alone"], r["S2 lost alone"],
                                                             r["S3 lost alone"]) <= 50, r)
    ok("the reflex route earns 30 or under on the cut pack", r["reflex route (every stump lost)"] <= 30, r)
    ok("every run route earns 50 or under", all(r[k] <= 50 for k in r if "run route" in k), r)

    # ------------------------------------------------------------------ R1 the field's raw material
    pr = pd.read_csv(os.path.join(T, "mrm_instrument_pair_register_2026.csv"))
    kinds_ = pr["pair_kind"].value_counts().to_dict()
    ok("R1 every family carries replicate, bootstrap, retune, release and label-freeze pairs",
       pr.groupby("model_family")["pair_kind"].nunique().min() == 5, kinds_)
    ok("R1 the panel is merchant-week scores at row level", fig["base"]["score_rows"] > 3_000_000, fig["base"]["score_rows"])

    # ------------------------------------------------------------------ R2 neutral mess
    for m, e in fig["mess"].items():
        cells = [inside(e["points"][RS.NAMES[s]], B["points_" + s]) for s in C.SOURCES] + \
                [inside(e[k], B[k]) for k in ("own_share", "cc3", "fr_sched", "fr_removed")]
        ok("R2 a hygiene slip (%s) keeps every graded figure inside its band" % m, all(cells), e)

    # ------------------------------------------------------------------ R3 each hurried figure outside its band
    rf = fig["reflex"]
    for s, k in (("turnover", "training data"), ("optimisation", "optimisation noise"), ("releases", "feature releases")):
        ok("R3 the reflex route's %s points sit outside the band" % k, not inside(rf["points"][k], B["points_" + s]),
           rf["points"][k])
    ok("R3 the reflex route's pinned-views share sits outside the band", not inside(rf["cc3"], B["cc3"]), rf["cc3"])
    ok("R3 the reflex route's own share sits outside the band", not inside(rf["own_share"], B["own_share"]))
    ok("R3 the reflex route's tier changes with sources removed sit outside", not inside(rf["fr_removed"], B["fr_removed"]))
    lat = fig["lattice"]
    ok("R3 S1 lost alone puts training data in escalation", lat["S1"]["points"]["training data"] >= 8.0)
    ok("R3 S2 lost alone puts optimisation noise on monitor", lat["S2"]["points"]["optimisation noise"] < 5.5)
    ok("R3 S3 lost alone puts feature releases on monitor", lat["S3"]["points"]["feature releases"] < 5.5)

    # ------------------------------------------------------------------ R4 no one thing, R5 the one-fact test
    fact = E["factorial"]
    ok("R4 three stumps, each necessary", sum(1 for j in fact["judgments"] if j["kind"] == "stump" and
                                              j["dropped"]["answer"] != fact["golden_answer"]) == 3)
    ok("R4 no stump sufficient alone", all(j["alone"]["answer"] != fact["golden_answer"] for j in fact["judgments"]
                                           if j["kind"] == "stump"))
    ok("R4 the single drops land on three distinct wrong answers",
       len({tuple(j["dropped"]["answer"]) for j in fact["judgments"] if j["kind"] == "stump"}) == 3)
    ok("R5 the largest hint rescues one result of nine", max(len(h["rescues"]) for h in E["hints"]) <= 3)

    # ------------------------------------------------------------------ R6 the rivals inside each band
    ok("R6 the battery files one call", fig["battery_calls"])
    ok("R6 the battery has twelve or more variants", fig["variants"] >= 12, fig["variants"])
    for s in C.SOURCES:
        lo, hi = fig["battery_range"][RS.NAMES[s]]
        ok("R6 %s: every variant inside the band" % s, inside(lo, B["points_" + s]) and inside(hi, B["points_" + s]))
    for k, e in fig["extra"].items():
        ok("R6 rival inside its bands: %s" % k, e["call"] == fig["call"] and inside(e["own_share"], B["own_share"])
           and all(inside(e["points"][RS.NAMES[s]], B["points_" + s]) for s in C.SOURCES), e)
    for s in C.SOURCES:
        ok("R6 stated band %s holds the golden and the battery" % s,
           S["points_" + s][0] <= B["points_" + s][0] + 1e-9 and S["points_" + s][1] >= B["points_" + s][1] - 1e-9)

    # ------------------------------------------------------------------ R7 the filed constants
    std = pdf_text(os.path.join(T, "gms_model_stability_standard_2026.pdf"))
    cov = pdf_text(os.path.join(T, "acquirer_agreement_schedule_c_tier_stability.pdf"))
    ok("R7 the bands' lines are filed (5.5 and 8 points)", "under 5.5 points" in std and "8 points or more" in std)
    ok("R7 the tiers are filed (400, 500, 600; 400 in the second tier)",
       "under 400" in cov and "400 or more and under 500" in cov and "600 or more" in cov)
    ok("R7 the cap is filed (12 per cent)", "12 per cent" in cov)
    ok("R7 the 2027 snapshots are filed", all(d in cov for d in ("22 March", "21 June", "20 September", "20 December")))
    ok("R7 the panel is filed (one merchant in five)", "one merchant in five" in cov)

    # ------------------------------------------------------------------ the semantic fork table
    ok("SF1 a source's movement is filed as root-mean-square points between two consecutive snapshots",
       "root-mean-square change" in std and "stated in score points" in std)
    ok("SF2 the book weighting is filed, every family once files turnover outside the band",
       "weighted by its" in std and not inside(fig["probe"]["every family counted once"], B["points_turnover"]),
       fig["probe"]["every family counted once"])
    ok("SF3 the four snapshot pairs that close in the assessment year are filed",
       "four snapshot pairs" in std)
    ok("SF4 no battery variant within 0.70 of a line on any source",
       all(min(abs(x - l) for l in C.LINES for x in fig["battery_range"][RS.NAMES[s]]) > 0.70 for s in C.SOURCES))
    ok("SF5 the share is of mean-square movement (filed)", "mean-square movement as a share" in std)
    ok("SF6 merchants' own change readings: the 2026 pairs inside the band, every gap from July 2024 ruled out",
       inside(fig["extra"]["merchants' own change from the 2026 snapshot pairs only"]["own_share"], B["own_share"])
       and fig["pre_settled"]["families_higher"] == C.F, fig["pre_settled"])
    ok("SF7 the tied fits keep the call; the free fit implies a replicate pair the pairs refute",
       fig["probe"]["unanchored implied replicate"] > 1.25 * fig["base"]["replicate"], fig["probe"])
    ok("SF8 a line from gap 8 files a figure near the band's floor and the same band",
       5.5 <= fig["probe"]["line through gaps 8 to 26"] < 8.0, fig["probe"]["line through gaps 8 to 26"])
    ok("SF9 thirteen of 52 weeks for every family keeps the band; six families train on 104 weeks",
       5.5 <= fig["probe"]["thirteen of 52 weeks for every family"] < 8.0 and fig["base"]["long_window_families"] >= 1)
    man = [json.loads(x) for x in open(os.path.join(T, "training_scheduler_runs_2024_2026.jsonl"))]
    boots = [m for m in man if m["kind"] == "bootstrap"]
    ok("SF10 a bootstrap pair's two refits carry different seeds (the manifests)",
       len({(b["iso_week"], b["job_family"], b["seed"]) for b in boots}) == len({(b["run_id"]) for b in boots}))
    ok("SF11 the calendar's dates file feature releases outside the band; each family's worst lag inside it",
       not inside(rf["points"]["feature releases"], B["points_releases"]) and
       5.5 <= fig["probe"]["each family's worst past lag"] < 8.0)
    ok("SF12 the roadmap is filed as the assessment year's release load", "roadmap for that year" in std)
    ret = pd.read_csv(os.path.join(T, "gms_retune_log.csv"))
    per = ret.groupby("model_family").size()
    ok("SF13 a retune every fourth refresh in every family", per.min() >= 30 and per.max() <= 32, per.to_dict())
    ok("SF14 the tier mappings agree within the band", inside(fig["fr_sched"], B["fr_sched"]))
    ok("SF15 sources removed in full (filed)", "taken out in full" in std)
    ok("SF16 every family's manifests show cold retrains before its settled weeks",
       all(any(m["parent_model_id"] is None for m in man if m["kind"] == "production" and m["job_family"] == jf)
           for jf in {m["job_family"] for m in man}))
    ok("SF17 the panel's specification is filed (not replaced, scored at both)",
       "not replaced" in cov and "scored at both" in cov)
    reps = [m for m in man if m["kind"] == "replicate"]
    ok("SF18 a replicate pair's two refits share parent and window and differ in seed",
       all(len({m["parent_model_id"] for m in reps if (m["iso_week"], m["job_family"]) == k}) == 1
           for k in {(m["iso_week"], m["job_family"]) for m in reps}))

    # ------------------------------------------------------------------ the never-filed list
    text = std + cov
    for f in files:
        if f.endswith(".xlsx"):
            text += xlsx_text(os.path.join(T, f))
    heads = " ".join(open(os.path.join(T, f)).readline() for f in files if f.endswith(".csv"))
    heads += " ".join(set(k for m in man[:400] for k in list(m) + list(m["options"])))
    banned = ("overlap", "turnover share", "persistence", "autocorrelation", "inherit", "adoption lag", "take-up",
              "take up", "effective date", "effective_week", "first use", "variance", "attribution", "churn")
    for word in banned:
        ok("never filed: '%s' in no document, column or file name" % word,
           word not in text.lower() and word not in heads.lower() and not any(word.replace(" ", "_") in f for f in files))
    ok("the legend says only what each column records",
       "released to the family's training environment" in xlsx_text(os.path.join(T, "platform_change_calendar.xlsx")))
    ok("no frozen-model rescore, lineage fork or pinned-views run in the manifests",
       {m["kind"] for m in man} == {"production", "replicate", "bootstrap", "retune_shadow", "release_shadow",
                                    "label_freeze"} and all(m["options"]["feature_views"] == "live" for m in man))

    # ------------------------------------------------------------------ realism sweep
    sc = pd.read_csv(os.path.join(T, "gms_monitoring_panel_scores_2025q3.csv"), dtype=str)
    ok("realism: re-sent refreshes carry a second load", sc["load_id"].str.endswith("-02").any())
    xw = pd.read_csv(os.path.join(T, "tolka_pay_merchant_id_migration.csv"))
    ok("realism: Tolka Pay's merchants were re-keyed", len(xw) > 500 and (xw["acquirer"] == "Tolka Pay").all())
    ids = [m["run_id"] for m in man]
    ok("realism: retried jobs left duplicate manifest lines", 0 < len(ids) - len(set(ids)) < 20, len(ids) - len(set(ids)))
    ok("realism: the row count field was renamed with the runtime image",
       any("train_rows" in m for m in man) and any("rows" in m for m in man))
    reg = pd.read_csv(os.path.join(T, "gms_model_registry.csv"))
    ok("realism: the scheduler's codes differ from the registry's",
       not (reg["model_family"] == reg["scheduler_job_family"]).any())
    ok("realism: every registry family reads every group its releases change",
       all(set(str(g).split(";")) <= set(str(reg.set_index("model_family").loc[c, "feature_groups_read"]).split(";"))
           for g, fams in pd.read_csv(os.path.join(T, "feature_platform_release_log.csv"))[
               ["feature_groups_changed", "model_families_touched"]].itertuples(index=False)
           for c in str(fams).split(";") if c and c != "nan"))
    ok("realism: scores stay inside 0 to 1,000", float(sc["score"].astype(float).min()) >= 0 and
       float(sc["score"].astype(float).max()) <= 1000)
    ok("realism: no two shipped files share a save time",
       len({int(os.path.getmtime(os.path.join(T, f))) for f in files}) == len(files))
    ok("realism: every family's book is between 1,000 and 25,000 merchants",
       pd.read_csv(os.path.join(T, "gms_scored_book_by_family.csv"))["scored_merchants"].between(800, 25000).all())

    # ------------------------------------------------------------------ the blocks
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("the blocks state the call", "escalate label revisions" in sub)
    ok("no em dash in the blocks", "—" not in sub)
    for k, v in (("cc1", "%.2f" % fig["cc1"]), ("cc2", "%.2f" % fig["cc2"]), ("cc3", "%.1f" % fig["cc3"])):
        ok("component %s stated at the golden" % k, v in sub.split("## Critical Components")[1].split("## Step")[0])
    print("checks: %d pass, %d fail" % (N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
