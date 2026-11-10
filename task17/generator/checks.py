"""The build's assertions, run on the cut pack (python3 checks.py [target]): the bar block (R1 to R7 of
dataset-generation 7.1), every semantic fork of the design note (SF1 to SF22), the input gates, the realism sweep,
the distractor deletion test, the clean truth against the parsed tables, the C kernel against the Python scheduler,
and the stored golden state's margins. Exit 1 on any failure."""
import datetime as dt
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import analysis as A
import des
import load as L
import pack as PK
import params as P
import pydes
import sim
import tables as T

FAIL = []
N = [0]
STEP = 10000


def ok(name, cond, detail=""):
    N[0] += 1
    if not cond:
        FAIL.append("%s %s" % (name, detail))


def edge(v, unit):
    """distance of v to the nearest edge of its printed cell"""
    return unit / 2.0 - abs(v - round(v / unit) * unit)


def pdf_text(path):
    r = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True)
    return r.stdout


def main(target):
    figs = json.load(open(os.path.join(HERE, "figures.json")))
    g = json.load(open(os.path.join(HERE, "golden_state.json")))
    w = sim.world()
    clean = T.from_world(w)
    pk = L.load_pack(target)
    cap = figs["cap"]
    req = figs["requests_total"]
    F = {k: os.path.join(target, v) for k, v in PK.FILES.items()}

    # ---------------------------------------------------------------- the parsed tables equal the clean truth
    for name, a, b, keys, cols in (
            ("jobs", clean.jobs, pk.jobs, ["jobid", "epoch"], ["account", "qos", "nodes", "wall_h", "submit_h", "elig_h", "start_h", "elapsed_h", "nh", "restarts"]),
            ("events", clean.events, pk.events, ["node", "start_h"], ["end_h", "reason"]),
            ("grants", clean.grants, pk.grants, ["project", "year"], ["granted", "first_year"])):
        a = a.sort_values(keys).reset_index(drop=True)
        b = b.sort_values(keys).reset_index(drop=True)
        ok("parsed %s rows equal the clean truth" % name, len(a) == len(b), "%d vs %d" % (len(a), len(b)))
        if len(a) == len(b):
            for c in cols:
                x, y = a[c].values, b[c].values
                if x.dtype.kind in "fi":
                    same = np.all((np.isnan(x.astype(float)) & np.isnan(y.astype(float))) | (np.abs(x.astype(float) - y.astype(float)) < 1e-6))
                else:
                    same = all(str(u) == str(v) for u, v in zip(x, y))
                ok("parsed %s.%s equals the clean truth" % (name, c), same)
    # the capacity report (the context artifact) at zero diff
    rw, rp = clean.report["weekly"], pk.report["weekly"]
    ok("capacity report weekly rebuilt at zero diff", len(rw) == len(rp) and np.allclose(rw[["utilisation", "delivered_nh", "p50_wait_h", "p90_wait_h", "lost_node_days"]].values,
                                                                                         rp[["utilisation", "delivered_nh", "p50_wait_h", "p90_wait_h", "lost_node_days"]].values, atol=1e-6))
    rq = A.assembly(pk)
    ok("report's Q3 2026 delivered node-hours equal the rebuilt clock delivery", abs(rq["delivered"] - rq["report_delivered"]) < 0.1)

    # ---------------------------------------------------------------- R1: the field's raw material ships
    ok("R1 raw material: segments per job, not results", len(pk.seg) >= 20000 and "p90" not in " ".join(pk.jobs.columns).lower())
    cols_all = []
    for f in (F["sacct"], F["events"], F["rack"], F["users"], F["storage"], F["tickets"]):
        cols_all += open(f, encoding="utf-8").readline().strip().lower().split(",")
    ok("R1 no shipped column holds a result or a flag", not any(re.search(r"(is_|flag|_true|seed|planted|class|rework|cap|answer|p90|hazard)", c) for c in cols_all), str(cols_all))
    ok("R1 the record's run times are censored at each job's limit (TIMEOUT rows exist at 24 and 48)",
       ((pk.jobs["state"] == "TIMEOUT") & (np.abs(pk.jobs["wall_h"] - 24) < 1e-6)).sum() > 500 and ((pk.jobs["state"] == "TIMEOUT") & (np.abs(pk.jobs["wall_h"] - 48) < 1e-6)).sum() > 50)

    # ---------------------------------------------------------------- R2: every mess item real and neutral
    raw = pd.read_csv(F["sacct"], dtype=str, keep_default_na=False)
    n_raw, n_dedup = len(raw), len(raw.drop_duplicates())
    ok("mess: the export carries duplicate rows (batches, the August re-run)", n_raw - n_dedup > 3000, "%d dup" % (n_raw - n_dedup))
    aug = raw[(raw["Submit_UTC"] >= "2026-08-01") & (raw["Submit_UTC"] < "2026-09-01")]
    ok("mess: August 2026's rows appear twice", len(aug) >= 2 * aug.drop_duplicates().shape[0] - 5)
    ok("mess: the hurried Q3 count (rows started, batches not de-duplicated) lands outside R1's cell",
       abs(figs["q3_segments"] - figs["q3_jobs_raw"]) >= 20, "%d vs %d" % (figs["q3_segments"], figs["q3_jobs_raw"]))
    ids = pk.jobs["jobid"].values
    ok("mess: the id counter wrapped (ids repeat across epochs)", (pk.jobs["epoch"] > 0).sum() > 1000 and len(set(ids)) < len(ids))
    merged = pk.jobs.groupby("jobid").agg(e=("elig_h", "min"), nh=("nh", "sum"))
    a, b = A.quarter(2026, 3)
    n_merged = int(((merged["e"] >= a) & (merged["e"] < b)).sum())
    ok("mess: merging ids across the wrap lands outside R1's cell", abs(n_merged - figs["q3_jobs_raw"]) >= 20, "%d" % n_merged)
    ok("mess: clocks differ (submit UTC, start local)", (raw["Start_local"].str.len() > 0).any())
    bi_utc, bi_loc = g["burst"]["utc"], g["burst"]["local"]
    ok("mess: the burst index is the same integer under either clock and over ran jobs",
       int(round(bi_utc)) == int(round(bi_loc)) == int(round(g["burst"]["ran"])), str(g["burst"]))
    ok("mess: node lists are compressed ranges", raw["NodeList"].str.contains(r"\[").sum() > 1000)
    ok("mess: time limits are day-hour strings", raw["Timelimit"].str.contains("-").sum() > 1000)
    ok("mess: states carry suffixes", raw["State"].str.startswith("CANCELLED by").sum() > 100)
    ok("mess: node event reasons are free text with variants", pk.events["reason"].nunique() > 30)
    nr = figs["rows_not_rejoined"]
    ok("mess: intervals cut by restarts rejoined or not, the medians print the same",
       int(round(nr["software_h"])) == figs["repair_software_h"] and round(nr["hardware_d"] * 2) / 2 == figs["repair_hardware_d"] and int(round(nr["rack_h"])) == figs["repair_rack_h"], str(nr))
    ok("mess: restarts cut rows (rows end exactly where the next starts, same reason)", len(pk.events) - len(A.intervals(pk)) > 300)

    # ---------------------------------------------------------------- R3: each result's hurried figure
    rc = figs["route_caps"]
    for k, v in rc.items():
        if k == "node-hours arithmetic (quick)":
            ok("R3 quick route caps at or above the requests (no cut)", v >= req - STEP / 2, "%d vs %d" % (v, req))
        else:
            ok("R3 route %s lands at least two steps above the cap" % k, v >= cap + 2 * STEP, "%d vs %d" % (v, cap))
    ok("R3 the routes land on five or more distinct wrong caps", len({v for v in rc.values()}) >= 5, str(rc))
    ok("R3 careful backtest outside R6's cell", abs(figs["backtest_careful_h"] - figs["backtest_p90_h"]) >= 1)
    ok("R3 Weibull outside R3's cells", figs["weibull_mean96_h"] != figs["mean96_h"] and figs["weibull_share48_pct"] != figs["share48_pct"])
    ok("R3 Weibull fails the 24 to 48 hour validation", not figs["families"]["weibull"]["passes"] and abs(figs["families"]["weibull"]["z"]) > 3.0)
    ok("R3 the record cut at 48 outside R3's cell", figs["cut48_mean96_h"] != figs["mean96_h"])
    ok("R3 counting killed runs whole lands outside R5's cell", figs["rework_whole_segment_pct"] != figs["rework_pct"])
    ok("R3 the careful pass's burst (Poisson, 1) outside the cell", figs["burst_index"] >= 3)
    ok("R3 one pooled ratio moves the expected use by a step or more", abs(figs["expected_use_pooled"] - figs["expected_use_requests"]) >= STEP)

    # ---------------------------------------------------------------- R4: no plant
    weekly = pk.report["weekly"]
    ok("R4 no identical weekly counts", weekly["jobs_started"].nunique() > 0.8 * len(weekly))
    ok("R4 no round headline totals", figs["q3_nh_raw"] % 1000 != 0 and figs["requests_total"] % 10000 != 0)
    for col, df, name in (("jobid", pk.jobs.sort_values("submit_h"), "jobid"),):
        d = np.diff(np.sort(df[col].unique()))
        ok("R4 id column is not one constant step over the record", not (len(set(d)) == 1))
    pids = sorted(pk.projects)
    ok("R4 project ids are not sequential", np.std(np.diff([int(p[1:]) for p in pids])) > 5)
    gr = pd.read_excel(F["alloc"], sheet_name="Grants 2023-2026")
    ok("R4 the allocation workbook is not in alphabetical or id order", list(gr["project_id"]) != sorted(gr["project_id"]) and list(gr["title"]) != sorted(gr["title"]))
    ok("R4 names take more than two shapes", pd.Series([re.sub(r"\d+", "#", n) for n in pk.jobs["name"].sample(3000, random_state=1)]).nunique() > 50)

    # ---------------------------------------------------------------- R5: no one thing (footprints)
    cats = pd.Series({pid: pr["category"] for pid, pr in pk.projects.items()})
    for c in sorted(cats.unique()):
        accs = set(cats[cats == c].index)
        sub = pk.jobs[pk.jobs["account"].isin(accs)]
        # sessions in every category: more than one job within half an hour by the same user and stem, often
        js = A.sessions(pk, pk.cut_h)
        jc = js[js["account"].isin(accs)]
        ok("R5 sessions in every category (%s)" % c, jc.groupby("session").size().gt(1).mean() > 0.3)
    ev = A.intervals(pk)
    rk = ev[ev["cls"] == "rack"]
    ok("R5 rack events in every rack", rk["rack"].nunique() == 8)
    sw = ev[(ev["cls"] == "software") & (ev["start_h"] >= A.H(2024))]
    ok("R5 software failures on every node", sw["node"].nunique() == 64)
    hz = np.array(g["outage"]["sw_hazard"])
    ok("R5 the hazard rises with uptime across the record", hz[5] > 1.5 * hz[0])
    ok("R5 requeued jobs in every category and every year", all(pk.jobs[(pk.jobs["restarts"] > 0) & pk.jobs["account"].isin(set(cats[cats == c].index))].shape[0] > 10 for c in cats.unique()))
    rw = A.rework(pk)
    per = rw["per_project"]
    ok("R5 checkpointing differs across projects (redone fractions spread)", per["frac"].std() > 0.2 and len(per) > 60)
    ok("R5 the TIMEOUT share after the change shows the tail beyond 24 h across kinds",
       figs["validation_n_beyond"] > 200)

    # ---------------------------------------------------------------- R6: the one-fact test (effort.json)
    ef = json.load(open(os.path.join(HERE, "effort.json"))) if os.path.exists(os.path.join(HERE, "effort.json")) else None
    if ef:
        ok("R6 the largest single hint rescues at most a third of the results", max(len(h["rescues"]) for h in ef["hints"]) <= 7 / 3.0, str([h["rescues"] for h in ef["hints"]]))

    # ---------------------------------------------------------------- R7: the rivals inside each band
    fine = {int(k): v for k, v in g["cap_fine"].items()}
    ok("R7 the cap step is met in at least 0.85 of futures", fine[cap]["p"] >= 0.85, "%.3f" % fine[cap]["p"])
    ok("R7 the step above the cap is met in at most 0.75", fine[cap + STEP]["p"] <= 0.75, "%.3f" % fine[cap + STEP]["p"])
    ok("R7 the step below the cap is met in at least 0.85", fine[cap - STEP]["p"] >= 0.85, "%.3f" % fine[cap - STEP]["p"])
    for k, v in g["rivals"].items():
        ok("R7 rival %s gives the same cap" % k, v["cap"] == cap, "%s vs %d" % (v["cap"], cap))
        ok("R7 rival %s clears 0.80 at the cap and fails it at the next step" % k, v["p"][str(cap)] >= 0.80 and v["p"][str(cap + STEP)] < 0.80, str(v["p"]))
    passing = {k: v for k, v in figs["families"].items() if v["passes"]}
    ok("R7 two or more families pass the validation", len(passing) >= 2)
    m96 = [v["mean96"] for v in passing.values()]
    ok("R7 the passing families' mean run time spans at most two adjacent hour cells", int(round(max(m96))) - int(round(min(m96))) <= 1, str(m96))
    s48 = [v["share48_pct"] for v in passing.values()]
    ok("R7 the passing families' share beyond 48 h lands in one 5-point cell", len({int(round(x / 5.0)) for x in s48}) == 1, str(s48))
    ok("R7 the nodes-only stratification lands in R3's cells", int(round(g["r3_nodes_strata"]["mean96"])) == figs["mean96_h"] and int(round(100 * g["r3_nodes_strata"]["share48"] / 5.0)) * 5 == figs["share48_pct"], str(g["r3_nodes_strata"]))
    ok("R7 requeued jobs included land in R3's cells", int(round(g["r3_with_requeued"]["mean96"])) == figs["mean96_h"] and int(round(100 * g["r3_with_requeued"]["share48"] / 5.0)) * 5 == figs["share48_pct"], str(g["r3_with_requeued"]))
    ok("R7 rework by stem reference lands in R5's cell", int(round(figs["rework_stem_raw"])) == figs["rework_pct"], "%s vs %s" % (figs["rework_stem_raw"], figs["rework_pct"]))
    ok("R7 the backtest's mean and median print the same hour", int(round(g["backtest"]["mean"])) == int(round(g["backtest"]["median"])), str(g["backtest"]))

    # ---------------------------------------------------------------- the semantic forks
    jj = pk.jobs[(pk.jobs["elig_h"] >= a) & (pk.jobs["elig_h"] < b) & pk.jobs["start_h"].notna()]
    w_el = (jj["start_h"] - jj["elig_h"]).values
    w_sub = (jj["start_h"] - jj["submit_h"]).values
    ok("SF1 the report's P90 reconciles from eligible time, not submit", abs(np.percentile(w_el, 90) - rq["report_p90"]) < 0.02 and abs(np.percentile(w_sub, 90) - rq["report_p90"]) > 0.2)
    ok("SF2 the quarter by eligibility differs from the quarter by submission", figs["q3_jobs_by_submit"] != figs["q3_jobs_raw"])
    ok("SF3 nearest-rank and interpolated percentiles agree within 0.05 h", abs(np.percentile(w_el, 90, method="lower") - np.percentile(w_el, 90)) < 0.05)
    ok("SF4 cancelled-before-start jobs are excluded (none has a start)", (pk.jobs[pk.jobs["state"] == "CANCELLED"]["start_h"].isna()).sum() > 500)
    ok("SF5 a job is one id within one epoch", pk.jobs.duplicated(["jobid", "epoch"]).sum() == 0)
    ok("SF6 node-hours are nodes times elapsed over every run", abs(pk.jobs["nh"].sum() - pk.seg["nh"].sum()) < 1e-3)
    ok("SF7 the duplicated month counts once", n_dedup < n_raw)
    ok("SF9 EASY and conservative backfill give the same cap", g["rivals"]["EASY backfill"]["cap"] == cap)
    ok("SF10 the limits by date parse as 24, 48 and 96 hours", [l for _, l in pk.limits["normal"]] == [24.0, 48.0, 96.0])
    ok("SF11 the 2027 limit applies from 1 April 2027", abs(pk.limits["normal"][2][0] - A.H(2027, 4, 1)) < 1e-6)
    ok("SF12 the cap is judged over the whole year's jobs", fine[cap]["n"] >= 2000)
    ok("SF13 and SF14 the cap is the largest step at or above 0.80", all(fine[t]["p"] < 0.8 for t in fine if t > cap) and fine[cap]["p"] >= 0.8)
    ok("SF15 expected use by standing differs from pooled and from the grants", figs["expected_use_requests"] != figs["expected_use_pooled"] and figs["expected_use_requests"] != figs["expected_use_grant"])
    ok("SF16 the requests on file sum to the stated total", abs(pk.requests["requested"].sum() - req) < 1)
    ok("SF17 every passing family gives the cap", all(v["cap"] == cap for k, v in g["rivals"].items() if k.startswith("family")))
    ok("SF18 Poisson submissions land on another cap", rc["Poisson submissions"] != cap)
    ok("SF19 independent failures land on another cap", rc["independent node failures"] != cap)
    ok("SF20 with or without the inputs' sampling error the cap holds", g["rivals"]["no parameter uncertainty"]["cap"] == cap)
    ok("SF22 the 2027 maintenance calendar carries thirteen windows", int(((pk.maint["start_h"] >= A.H(2027)) & (pk.maint["start_h"] < A.H(2028))).sum()) == 13)
    # SF21: every graded figure clear of its cell's edge
    margins = {"use_new": (100 * g["ratios"]["new"], 1, 0.08), "use_cont": (100 * g["ratios"]["cont"], 1, 0.08),
               "burst": (g["burst"]["utc"], 1, 0.1), "mean96": (figs["mean96_raw"], 1, 0.08), "share48": (figs["share48_raw"], 5, 0.4),
               "q3_jobs": (figs["q3_jobs_raw"], 10, 1.0), "q3_nh": (figs["q3_nh_raw"], 1000, 60), "multi": (figs["multi_share_raw"], 1, 0.08),
               "repair_sw": (figs["repair_software_raw"], 1, 0.08), "repair_hw": (figs["repair_hardware_raw"], 0.5, 0.05), "repair_rack": (figs["repair_rack_raw"], 1, 0.1),
               "rework": (figs["rework_raw"], 1, 0.08), "backtest": (figs["backtest_p90_raw"], 1, 0.1), "cut": (100 * (1 - cap / req), 1, 0.08)}
    for k, (v, unit, need) in margins.items():
        ok("SF21 %s is %.3g or more from its cell edge" % (k, need), edge(v, unit) >= need, "%.4f (edge %.4f)" % (v, edge(v, unit)))
    for q, v in figs["lost_raw"].items():
        if q != "4":
            ok("SF21 lost node-days Q%s clear of the edge" % q, edge(v, 10) >= 0.6, "%.2f" % v)

    # ---------------------------------------------------------------- input gates
    files = sorted(os.listdir(target))
    ok("gate: 12 files, 10 usable", len(files) == 12)
    ok("gate: four file categories", {f.rsplit(".", 1)[1] for f in files} >= {"csv", "xlsx", "pdf", "txt"})
    ok("gate: the job log has 20,000 rows or more", n_raw >= 20000, str(n_raw))
    ok("gate: the node event log runs 10 printed pages or more", len(pk.events) >= 600)
    ok("gate: no file describes the pack", not any(re.search(r"readme|dictionar|notes|manifest|schema|codebook", f, re.I) for f in files))
    for f in (F["alloc"], F["maint"], F["report"]):
        with zipfile.ZipFile(f) as z:
            names = re.findall(r'name="([^"]+)"', z.read("xl/workbook.xml").decode())
        ok("gate: no notes or dictionary sheet in %s" % os.path.basename(f), not any(re.match(r"(read ?me|notes?|dictionary|definitions|glossary|about)", n, re.I) for n in names), str(names))
    ok("gate: distractors unnamed in the pack", not any("distractor" in f.lower() for f in files))
    # distractor deletion: the cheap figures unchanged without the two files
    tmp = tempfile.mkdtemp(prefix="task17-nodistract-")
    for f in files:
        if f not in (PK.FILES["storage"], PK.FILES["tickets"]):
            shutil.copy(os.path.join(target, f), tmp)
    try:
        q = L.load_pack(tmp)
        ok("gate: the golden's R1, R2 and burst index unchanged without the distractors",
           A.assembly(q)["jobs"] == rq["jobs"] and abs(A.use_ratios(q)["new"] - g["ratios"]["new"]) < 1e-9 and abs(A.burst_index(q)[0] - g["burst"]["utc"]) < 1e-9)
    except FileNotFoundError:
        ok("gate: the golden reads neither distractor", False)
    shutil.rmtree(tmp, ignore_errors=True)

    # ---------------------------------------------------------------- documents: positive controls and no handover
    pol = pdf_text(F["policy"])
    ok("doc: the policy's cap rule reads back", "largest multiple of 10,000 node-hours" in pol and "80 per cent" in pol)
    ok("doc: the policy files what the outcomes carry", "uncertainty of every rate estimated from the record" in pol)
    ok("doc: the policy names the queue wait from eligibility", "becoming eligible to run to its first start" in pol)
    plan = pdf_text(F["plan"])
    ok("doc: the plan raises the limit to 96 hours from 1 April 2027", "96 hours on 1 April 2027" in plan)
    for word in ("log-logistic", "Weibull", "lognormal", "checkpoint", "burst", "cluster process", "simulation", "Monte Carlo", "backtest", "rework"):
        ok("doc: the policy and the plan never say '%s'" % word, word.lower() not in pol.lower() and word.lower() not in plan.lower())
    cfg = open(F["config"], encoding="utf-8").read()
    ok("doc: the configuration states the scheduling policy", "sched/backfill" in cfg and "priority/basic" in cfg and "select/linear" in cfg)
    txtfiles = [open(F[k], encoding="utf-8").read().lower() for k in ("config",)] + [pol.lower(), plan.lower()]
    ok("doc: no document states a golden figure", not any(figs["cap_str"] in t or str(figs["q3_jobs"]) in t for t in txtfiles))
    ok("doc: no document is dated after the export", "2026-11-1" not in cfg or "2026-11-16" not in cfg)

    # ---------------------------------------------------------------- the two schedulers agree on a slice of the record
    K, wo, wm = w.kernel_inputs
    m = (K["submit"] >= A.H(2026, 9, 1)) & (K["submit"] < A.H(2026, 9, 1) + 24 * 20)
    idx = np.where(m)[0]
    sub = {k: (v[idx] if k not in ("dep", "after") else np.full(len(idx), -1, dtype=np.int32)) for k, v in K.items()}
    oo = [x[(wo[1] >= A.H(2026, 9, 1) - 24) & (wo[1] < A.H(2026, 9, 1) + 24 * 25)] for x in wo]
    mm = [x[(wm[0] >= A.H(2026, 9, 1) - 24) & (wm[0] < A.H(2026, 9, 1) + 24 * 25)] for x in wm]
    Rc = des.simulate(64, sub, (oo[0], oo[1], oo[2]), (mm[0], mm[1]), A.H(2026, 9, 1) + 24 * 30, mode=1, bf_max=P.BF_MAX, hold=P.REQUEUE_HOLD)
    Rp = pydes.simulate(64, sub, (oo[0], oo[1], oo[2]), (mm[0], mm[1]), A.H(2026, 9, 1) + 24 * 30, bf_max=P.BF_MAX, hold=P.REQUEUE_HOLD)
    ok("the C kernel and the Python scheduler agree on twenty days of the record",
       np.allclose(Rc["first_start"], Rp["first_start"]) and np.allclose(Rc["rework"], Rp["rework"]) and np.allclose(Rc["nh"], Rp["nh"]))

    # ---------------------------------------------------------------- the golden's figures tie to the stored state
    ok("figures: the cut share follows the cap", figs["cut_share_pct"] == int(round(100 * (1 - cap / req))))
    ok("figures: the quick cap is above the requests", figs["quick_cap"] >= req)
    ok("figures: the careful cap is two or more steps above the golden", rc["careful but hurried"] >= cap + 2 * STEP)
    ok("figures: the backtest lands within two hours of the report", abs(figs["backtest_p90_raw"] - figs["report_p90"]) <= 2.0, "%s vs %s" % (figs["backtest_p90_raw"], figs["report_p90"]))

    print("%d checks, %d failed" % (N[0], len(FAIL)))
    for f in FAIL:
        print("FAIL", f)
    return 1 if FAIL else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")))
