"""task25 assertions on the cut pack: the bar block (R1 to R7), the forks, the truth, the margins, the input gates,
the realism sweep and the deliverables' agreement. python3 checks.py [--fast]; exit 1 on any failure."""
import copy
import datetime as dt
import json
import os
import re
import shutil
import sys
import tempfile

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as A  # noqa: E402
import cutpack as CP  # noqa: E402
import params as P  # noqa: E402
import results as RS  # noqa: E402
import truth2027 as T  # noqa: E402
import world as W  # noqa: E402

OUT = []
OPEN = {"kide-8b-v4": "P", "kide-34b-v3": "Q"}     # the two members of the call a run can get wrong, and the stump that opens each


def ok(label, cond, detail=""):
    OUT.append((label, bool(cond), detail))


def main(fast=False):
    target = os.path.join(TASK, "target")
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    E = json.load(open(os.path.join(HERE, "effort.json")))
    G = A.golden(target)
    late = fig["call_late_runs"]
    runs = {r["run_id"]: r for r in G["runs"]}
    ratio = {k: G["days"][k] / r["window_days"] for k, r in runs.items()}

    # ---------------- the call and its margins
    ok("C1 golden late set reproduces from the pack", A.late_set(G, G["days"]) == late, str(late))
    ok("C2 seven late, four fitting", len(late) == 7 and len(runs) == 11)
    ok("C3 every forced run 12 per cent or more from its window under the golden",
       all(abs(v - 1) >= 0.12 for k, v in ratio.items() if k not in OPEN), {k: round(v, 3) for k, v in ratio.items()})
    RPg = G["RP"]
    d_noP, d_noQ, d_none = RPg.run(pod=False), RPg.run(phi=False), RPg.run(pod=False, phi=False)
    rr = lambda d, k: d[k] / runs[k]["window_days"]
    ok("C4 the pod-boundary member: late by 4 to 9 per cent, fitting without the pod penalty by 6 or more, the reflex "
       "route fitting by 2 or more", 1.04 <= ratio["kide-8b-v4"] <= 1.09 and rr(d_noP, "kide-8b-v4") <= 0.94 and
       rr(d_none, "kide-8b-v4") <= 0.98, (round(ratio["kide-8b-v4"], 3), round(rr(d_noP, "kide-8b-v4"), 3), round(rr(d_none, "kide-8b-v4"), 3)))
    ok("C4 the pool member: fitting by 3 to 8 per cent, late without the pool's back-off by 3 or more, the reflex "
       "route late by 3 or more", 0.92 <= ratio["kide-34b-v3"] <= 0.97 and rr(d_noQ, "kide-34b-v3") >= 1.03 and
       rr(d_none, "kide-34b-v3") >= 1.03, (round(ratio["kide-34b-v3"], 3), round(rr(d_noQ, "kide-34b-v3"), 3), round(rr(d_none, "kide-34b-v3"), 3)))
    ok("C4 each open member lies between the honest family's spread and its stump's worth: the battery moves no run's days "
       "by more than 2.5 per cent and each open member's margin is 4 per cent or more",
       fig["battery_worst_pct"] <= 2.5 and all(abs(ratio[k] - 1) >= 0.04 for k in OPEN), fig["battery_worst_pct"])
    ok("C4 the other nine members are forced: the reflex route and every single drop file each as the golden does",
       all((rr(d, k) > 1) == (ratio[k] > 1) for d in (d_noP, d_noQ, d_none) for k in runs if k not in OPEN))
    ok("C5 the reflex route's call differs from the golden's in exactly the two open members",
       sorted(set(A.late_set(G, d_none)) ^ set(late)) == sorted(OPEN), sorted(set(A.late_set(G, d_none)) ^ set(late)))
    # ---------------- truth: the world replayed
    specs = T.run_specs()
    tr = T.replay(specs, n=12 if fast else 30)
    tmean = {k: float(v.mean()) for k, v in tr.items()}
    tlate = sorted(k for k, v in tmean.items() if v > runs[k]["window_days"])
    ok("T1 the world's own replay files the same late set", tlate == late, str(tlate))
    for k in runs:
        ok("T2 %s expected days within 4 per cent of the world's" % k, abs(G["days"][k] / tmean[k] - 1) <= 0.04,
           "%.2f vs %.2f" % (G["days"][k], tmean[k]))
    ok("T3 the fitted attention coefficient within 2 per cent of the world's", abs(G["CM"]["beta"] / P.BETA - 1) <= 0.02,
       "%.4f" % G["CM"]["beta"])
    for k in RS.LC_RUNS:
        s = [x for x in specs if x["run_id"] == k][0]
        ok("T4 %s slowest-rank overhead within 3 points of the world's" % k,
           abs(100 * (runs[k]["emax"] / runs[k]["emean"] - s["emax"] / s["emean"])) <= 3.0,
           "%.1f vs %.1f" % (100 * (runs[k]["emax"] / runs[k]["emean"] - 1), 100 * (s["emax"] / s["emean"] - 1)))
    s = [x for x in specs if x["run_id"] == "kide-34b-sci"][0]
    ok("T5 the scientific run's fill within 0.015 of the world's", abs(runs["kide-34b-sci"]["fill"] - s["fill"]) <= 0.015)
    ok("T6 the throttle response at 20 per cent over within 3 points of the world's (on the rebuilt excess)",
       abs(fig["throttle_pct_x20"] - 100 * (P.THR1 * 0.2 + P.THR2 * 0.04)) <= 6.0, fig["throttle_pct_x20"])
    # ---------------- the bar block
    used = {"runs/run_registry_2026.csv", "runs/step_log_2026.csv", "runs/interruptions_2026.csv",
            "runs/node_allocations_2026.csv", "profiling/rank_step_samples_2026.csv", "profiling/packing_manifests_2026.jsonl",
            "cluster/node_states_2026.csv", "provider/hall_it_load_2026.csv", "provider/work_orders_2025_2026.csv",
            "provider/incident_log_2026.csv", "benchmark/tpbench_results.csv", "benchmark/tpbench_harness.yaml",
            "plan_2027/roadmap_h1_2027.xlsx", "data/doc_length_sample.csv", "data/data_mixes.csv",
            "provider/planned_works_h1_2027.pdf"}
    ok("R1 the golden reads raw rows (per-rank samples, manifests, step logs, the meter, node states)",
       all(os.path.exists(os.path.join(target, u)) for u in used))
    cols = set()
    for rel in CP.FILES.values():
        if rel.endswith(".csv"):
            cols |= set(pd.read_csv(os.path.join(target, rel), nrows=2).columns)
    ok("R1 no shipped column holds a result", not any(re.search(r"overhead|slowest|stretch|throttle|fill|expected_days|excess", c) for c in cols), sorted(cols)[:5])
    # R2: each mess item mishandled moves no verdict
    for name, mutate in mess_variants():
        G2 = variant(target, mutate)
        ok("R2 mess neutral: %s" % name, A.late_set(G2, G2["days"]) == late)
    # R3: each lost result's careful figure outside its band, each earned one inside
    for r in E["results"]:
        g = grade(r, r["passes"]["careful"])
        if r["id"] in ("R1", "R3", "R4"):
            ok("R3 %s earned by the careful pass (a move the runs make unprompted)" % r["id"], g == "right", g)
        else:
            ok("R3 %s lost by the careful pass" % r["id"], g in ("missed", "partly"), g)
    # R4: no plant
    for rel in CP.FILES.values():
        if rel.endswith((".csv", ".yaml", ".jsonl")):
            txt = open(os.path.join(target, rel)).read(400000).lower()
            ok("R4 no decisive vocabulary in %s" % rel, not re.search(r"straggler|slowest rank|throttl|power cap|capping|padding waste", txt))
    # R5: each factor's footprint outside the deciding units
    prof = [v for k, v in G["CM"]["per_run"].items()]
    pr = G["pred"]
    lc26 = [k for k in pr if "-lc" in k]
    ok("R5 the slowest-rank wait shows in every 2026 long-context run (5 per cent or more)",
       all(pr[k]["emax"] / pr[k]["emean"] - 1 > 0.05 for k in lc26), {k: round(pr[k]["emax"] / pr[k]["emean"], 3) for k in lc26})
    bf26 = [k for k in pr if G["F"]["reg"].set_index("run_id").loc[k, "packing"] == "best_fit"]
    ok("R5 best-fit padding shows in the 2026 best-fit runs", all(pr[k]["fill"] < 1.0 for k in bf26) and len(bf26) >= 2)
    ok("R5 the hall B cap shows on 20 or more 2026 days across several runs", fig["capped_days_2026"] >= 20)
    capped_runs = G["S"][(G["S"]["x"] > 0)]["run_id"].nunique()
    ok("R5 capped intervals touch four or more 2026 runs", capped_runs >= 4, capped_runs)
    fl = G["flags"]
    reg26 = G["F"]["reg"].set_index("run_id")
    regB = [k for k in reg26.index if reg26.loc[k, "hall"] == "B" and k.startswith("kide-") and k != "kide-70b-scale"]
    ok("R5 the pod boundary shows in three or more registered 2026 runs, and three or more sit inside one pod",
       sum(fl.get(k, False) for k in regB) >= 3 and sum(not fl.get(k, False) for k in regB) >= 3,
       {k: fl.get(k, False) for k in regB})
    ok("R5 each 2026 run across both pods runs 10 per cent or more over its predicted step; none inside one pod does",
       all((r.ratio / G["PEN"]["ratio_one"] - 1 >= 0.10) == bool(r.both) for r in G["PEN"]["runs"].itertuples()
           if r.run_id.startswith("kide-")), G["PEN"]["runs"][G["PEN"]["runs"].both][["run_id", "ratio"]].values.tolist())
    ok("R5 the pod penalty reads within 2 points of the world's", abs(G["PEN"]["pen"] - P.STRADDLE) <= 0.02, G["PEN"]["pen"])
    PRg = G["PR"]
    lo, hi = PRg["cen"] < 0.88, PRg["cen"] > 0.97
    ok("R5 the pool backs off in the 2026 record: its share is 0.9 or more of the plateau below 88 per cent of the contract "
       "and under 0.1 of it above 97 per cent, each over 7 days of intervals",
       PRg["phi"][lo].min() >= 0.9 and PRg["phi"][hi].max() <= 0.1 and
       sum(c for c, h in zip(PRg["counts"], hi) if h) * 300 / 86400 >= 7, PRg["phi"].round(2).tolist())
    ok("R5 the draw line reads within 0.5 per cent of the world's slope and 1 per cent of its intercept",
       abs(G["kwB"][1] / (P.HALLS["B"]["node_kw"] - P.HALLS["B"]["idle_kw"]) - 1) <= 0.005 and
       abs(G["kwB"][0] / (P.HALLS["B"]["infra_kw"] + 1024 * P.HALLS["B"]["idle_kw"]) - 1) <= 0.01, list(G["kwB"]))
    for j in E["factorial"]["judgments"]:
        if j["kind"] == "stump":
            ok("R5 %s fixed alone rescues a third of the results or fewer" % j["id"], len(j["alone"]["results_rescued"]) <= 3)
    # R6: hints rescue only what they list
    ok("R6 the largest hint rescues one result", max(len(h["rescues"]) for h in E["hints"]) <= 3)
    # R7: rivals
    for f in E["forcing"]["golden_family"]:
        ok("R7 rival on the golden's side: %s" % f["name"], f["answer"] == late)
    for p in E["forcing"]["perturbations"]:
        ok("R7 perturbation holds: %s" % p["input"], p["answer"] == late)
    ok("R7 the variant battery is fifteen variants, each filing the golden's seven and moving no run's days by more than 3 "
       "per cent", fig["battery_n"] >= 12 and fig["battery_worst_pct"] <= 3.0, (fig["battery_n"], fig["battery_worst_pct"]))
    for s_ in E["forcing"]["shortcuts"]:
        ok("R7 shortcut across the line: %s" % s_["name"], s_["answer"] != late)
    # ---------------- forks
    RP = G["RP"]
    p90 = sorted(k for k in runs if fig["p90_%s" % k] > runs[k]["window_days"])
    p10 = sorted(k for k in runs if fig["p10_%s" % k] > runs[k]["window_days"])
    ok("SF3 finishing four times in five reads the same set as the expected finish", p90 == late and p10 == late)
    ok("SF2 the trainer counts real tokens: 2026 best-fit runs log fewer tokens per step than their positions",
       all(pr[k]["fill"] < 1 for k in bf26))
    ok("SF4 benchmark days are the benchmark's measured rate (tokens over tokens per GPU-second over GPUs); the bridge's end, the expected days, does not depend on that starting convention",
       all(abs(fig["bench_days_%s" % k] - runs[k]["budget"] / (runs[k]["tps_bench"] * 8 * runs[k]["D"]) / 86400) < 0.06 for k in runs))
    idle = RP.run(hold="idle_after_finish")
    ok("SF8 nodes idle after an early finish instead of backfill: same set", A.late_set(G, idle) == late, A.late_set(G, idle))
    win = RP.run(hold="window_only")
    ok("SF9 blocks released at the window's end instead of extended: same set", A.late_set(G, win) == late, A.late_set(G, win))
    ok("SF10 the 2027 bridge adds to the expected days", all(abs(sum(X for i, X in enumerate(
        [fig["bridge_%s_%d" % (k, i)] for i in range(8)])) - fig["bridge_%s_8" % k]) < 0.06 for k in runs))
    b26 = sum(fig["b26_%d" % i] for i in range(10))
    ok("SF10 the 2026 bridge adds to the GPU-days held", abs(b26 - fig["b26_10"]) <= 5, "%d vs %d" % (b26, fig["b26_10"]))
    ok("SF10 only a run with a block across both pods has a pod item in the 2027 bridge",
       all((fig["bridge_%s_4" % k] > 0.05) == bool(runs[k]["both"]) for k in runs))
    ok("SF5 GPU-days held reproduces from the registry alone", abs(fig["held_2026_total"] - G["ledger"]["gpu_days_held"].sum()) < 1)
    ok("SF6 every 2026 run launched in 2026 is in the ledger", len(G["ledger"]) == len(G["F"]["reg"]))
    ok("SF1 days are wall-clock from 00:00 UTC on the window's start", all(fig["days_%s" % k] > fig["bench_days_%s" % k] for k in runs))
    ok("SF7 the 80 per cent range brackets the expected days", all(fig["p10_%s" % k] <= fig["days_%s" % k] + 0.6 and
                                                                  fig["p90_%s" % k] >= fig["days_%s" % k] - 0.6 for k in runs))
    # BT1 to BT3: the reflex route back-tested on the 2026 runs, and the pooled benchmark-to-held ratio held out one run at a time
    b26_, per26 = A.bridge_2026(G)
    bt = pd.DataFrame([dict(run_id=k, held=v["held"], bench=v["bench"], resid=100 * (v["other"] + v["pod"]) / v["held"],
                            both=bool(G["flags"].get(k, False))) for k, v in per26.items()])
    big_ = bt[bt["held"] > 2000]
    ok("BT1 the reflex route leaves 2.5 per cent or less on every run of over 2,000 GPU-days inside one pod and 13 to 18 per cent "
       "on each run across both pods, and every run across both pods is one of the large ones",
       len(big_) == 13 and big_[~big_["both"]]["resid"].abs().max() <= 2.5 and 13 <= big_[big_["both"]]["resid"].min() and
       big_[big_["both"]]["resid"].max() <= 18 and bool(bt[bt["both"]]["held"].gt(2000).all()),
       (len(big_), round(big_[~big_["both"]]["resid"].abs().max(), 2), round(big_[big_["both"]]["resid"].min(), 1), round(big_[big_["both"]]["resid"].max(), 1)))
    ok("BT2 so the reflex route's median miss over the 53 runs is 1.5 per cent or less and its mean over the 13 large runs 4 to 7",
       len(bt) == 53 and bt["resid"].abs().median() <= 1.5 and 4 <= big_["resid"].abs().mean() <= 7,
       (round(bt["resid"].abs().median(), 2), round(big_["resid"].abs().mean(), 2)))
    loo = []
    for k in big_["run_id"]:
        o = bt[bt["run_id"] != k]
        loo.append(abs(100 * (o["held"].sum() / o["bench"].sum() * float(bt.loc[bt["run_id"] == k, "bench"].iloc[0]) /
                              float(bt.loc[bt["run_id"] == k, "held"].iloc[0]) - 1)))
    ok("BT3 the pooled benchmark-to-held ratio (%.3f over 2026) fails a leave-one-run-out check by 25 per cent or more on a large run"
       % (bt["held"].sum() / bt["bench"].sum()), max(loo) >= 25 and abs(bt["held"].sum() / bt["bench"].sum() - fig["f26_ratio"]) < 0.0006,
       (round(max(loo), 1), round(bt["held"].sum() / bt["bench"].sum(), 3)))
    # BT4 to BT6: the benchmark corpus's slowest-rank cost and the 2027 overheads across independent streams. The harness file
    # files the corpus by its length distribution only, so each analyst draws a stream of their own.
    hc = G["F"]["harness"]["corpus"]["doc_length"]
    Nb, Lb, db = P.MODELS["8B"]
    Cb, gb = 65536, 2
    kfb = Lb * db * Cb / Nb

    def harness_cost(ntok, seed):
        rng = np.random.default_rng(seed)
        docs = W.draw_docs({"x": 1.0}, ntok, rng, sources={"x": (hc["median_tokens"], hc["sigma"], hc["max_tokens"])})
        Sx, _, _ = W.pack_sequential(docs, Cb)
        return A.step_units(Sx, kfb, G["CM"]["beta"], 64, gb, seed=int(Cb + gb))[0]

    Sg, _ = G["PK"].harness(G["F"], Cb)
    cost_g = A.step_units(Sg, kfb, G["CM"]["beta"], 64, gb, seed=int(Cb + gb))[0]
    conv = [harness_cost(A.HARNESS_TOKENS, 5000 + i) for i in range(3)]
    ok("BT4 the golden's replay of the benchmark corpus has converged: three other streams of its length put the 64k-context "
       "slowest-rank cost within 0.5 per cent of it", max(abs(c / cost_g - 1) for c in conv) <= 0.005,
       [round(c / cost_g - 1, 4) for c in conv])
    few = np.array([harness_cost(3.0e8, 6000 + i) for i in range(40)])
    ok("BT5 a stream of 3e8 tokens does not converge: its cost moves by 1.0 per cent or more (sd over forty streams), which "
       "is why the expected days of kide-8b-lc64 carry a band of 5 per cent", few.std(ddof=1) / few.mean() >= 0.010,
       round(few.std(ddof=1) / few.mean(), 4))
    ovs = {}
    for k in ("kide-13b-code-lc32", "kide-34b-lc64", "kide-8b-lc64"):
        r_ = runs[k]
        kf_ = r_["L"] * r_["d"] * r_["C"] / r_["N"]
        vals = []
        for sd_ in (31, 32, 33, 34):
            Sx, _ = A.Packer(G["F"], seed=sd_).stream(r_["mix"], r_["C"], r_["rule"])
            em, eb = A.step_units(Sx, kf_, G["CM"]["beta"], r_["D"], r_["g"], seed=sd_)
            vals.append(100 * (em / eb - 1))
        ovs[k] = [round(v - fig["overhead_pct_%s" % k], 2) for v in vals]
    ok("BT6 the three few-sequence runs' slowest-rank overheads move by 1.0 point or less across four other production streams "
       "(the band is 3 points)", all(abs(d_) <= 1.0 for v in ovs.values() for d_ in v), ovs)
    cfg_dir = os.path.join(target, "plan_2027", "configs")
    cfg_txt = [open(os.path.join(cfg_dir, f)).read() for f in sorted(os.listdir(cfg_dir))]
    mix_cols = list(pd.read_csv(os.path.join(target, "data", "data_mixes.csv"), nrows=1).columns)
    harn_txt = open(os.path.join(target, "benchmark", "tpbench_harness.yaml")).read()
    ok("BT7 the files pin the replay's three readings: the mixes' unit is named token_share, every config files the cut at seq_len and "
       "its data-parallel size, and the harness file files the same cut",
       "token_share" in mix_cols and len(cfg_txt) == 11 and
       all(("cut at seq_len" in t or "cut into seq_len pieces" in t) and re.search(r"parallelism:\n\s+tensor: \d+\n\s+data: \d+", t) for t in cfg_txt) and
       "cut at the sequence length" in harn_txt, (mix_cols, len(cfg_txt)))
    # SF13: the pool's busy nodes in the 2027 plan, three readings
    pr0 = dict(G["PR"])
    pr0["plateau"] = 0.0
    d_none = RPg.run(pool_delta=-G["PR"]["plateau"])
    ok("SF13 the pool's busy nodes in the plan: none and the measured response file the golden's set, its 2026 mean share "
       "files kide-34b-v3 late", A.late_set(G, d_none) == late and
       sorted(set(A.late_set(G, d_noQ)) ^ set(late)) == ["kide-34b-v3"], (A.late_set(G, d_none), A.late_set(G, d_noQ)))
    # SF14: hall B's draw as one line in the allocated nodes against a line in the registered and the pool's nodes apart
    exb, led_ = G["exB"], G["ledger"]
    tt = exb["t"].values.astype("datetime64[ns]")
    held_ = np.zeros(len(exb))
    for r_ in led_[led_["hall"] == "B"].itertuples():
        held_ += ((tt >= np.datetime64(r_.launch)) & (tt < np.datetime64(r_.finish))) * r_.nodes
    alloc_ = exb["allocated"].values.astype(float)
    sel = (exb["it_load_kw"].notna() & (exb["it_load_kw"] < 8100 - 40) & (alloc_ > 0)).values & (alloc_ - held_ >= 0)
    Xs = np.c_[np.ones(sel.sum()), held_[sel], (alloc_ - held_)[sel]]
    cs, *_ = np.linalg.lstsq(Xs, exb["it_load_kw"].values[sel], rcond=None)
    ok("SF14 hall B's draw: a node held by a registered run and a node the pool keeps busy draw alike (the two slopes "
       "within 0.5 per cent), so one line in the allocated nodes is the whole of it", abs(cs[1] / cs[2] - 1) < 0.005, cs.round(3).tolist())
    # ---------------- the ledger is feasible under the stated rules (CAR-2027-1 section 2)
    gfin = {k: runs[k]["ws"] + dt.timedelta(days=G["days"][k]) for k in runs}
    ok("SF11 hall B never holds more than its 1,024 nodes at the golden's finishes (blocks kept until the run finishes)",
       max(sum(r["D"] for r in G["runs"] if r["hall"] == "B" and r["ws"] <= (T0d + dt.timedelta(days=t)).date() <=
               max(r["we"], gfin[r["run_id"]])) for T0d in [dt.datetime(2027, 1, 1)] for t in range(0, 190)) <= 1024)
    sharing = [(a, b) for b in runs for a in runs[b]["preds"]]
    ok("SF11 every pair of blocks that share rows is booked with the earlier run's expected finish and the world's slowest "
       "of %d draws at least 7 days before the later window opens" % len(next(iter(tr.values()))),
       all((runs[a]["ws"] + dt.timedelta(days=float(tr[a].max()))) + dt.timedelta(days=7) <= runs[b]["ws"] for a, b in sharing) and
       all(gfin[a] + dt.timedelta(days=7) <= runs[b]["ws"] for a, b in sharing), sharing)
    ok("SF11 so the rule that a later run waits for its nodes never binds, at the golden or in the world",
       all(abs(G["days"][k] - RPg.run(precedence=False)[k]) < 1e-9 for k in runs))
    ok("SF11 no two reservations in a hall name the same rows inside the same window",
       all(not (runs[a]["rows"] & runs[b]["rows"]) or runs[a]["we"] <= runs[b]["ws"] or runs[b]["we"] <= runs[a]["ws"]
           for a in runs for b in runs if a < b and runs[a]["hall"] == runs[b]["hall"]))
    ok("SF12 each roadmap block holds as many nodes as its run's configuration reserves",
       all(len(P.BLOCKS_2027[k]) == 3 and (P.BLOCKS_2027[k][2] - P.BLOCKS_2027[k][1] + 1) * 32 == runs[k]["D"] for k in runs))
    # ---------------- the pinning list: each filed value is in its file
    from pypdf import PdfReader
    def pdf_text(rel):
        return " ".join(pg.extract_text() for pg in PdfReader(os.path.join(target, rel)).pages)
    s3, car = pdf_text(CP.FILES["schedule"]), pdf_text(CP.FILES["rules"])
    ok("PL1 hall B's node count and contract are in Service Schedule S-3", "1,024" in s3 and "8,100 kW" in s3 and "6,600 kW" in s3)
    ok("PL2 S-3 does not say how the nodes are laid out in pods", not re.search(r"pod", s3, re.I))
    ok("PL3 CAR section 2 files the window, the extension and the next run's wait",
       all(t in car.replace("\n", " ") for t in ("00:00 UTC", "extended until the run finishes", "whichever is later")))
    ok("PL4 CAR files the token count without padding, the test and the GPU-days held",
       "padding positions" in car and "four times in five" in car and "eight GPUs" in car)
    cfgs = [open(os.path.join(target, "plan_2027", "configs", f)).read() for f in sorted(os.listdir(os.path.join(target, "plan_2027", "configs")))]
    ok("PL5 every config files the checkpoint interval and eight GPUs a node", all("every_minutes: 30" in t and "tensor: 8" in t for t in cfgs))
    from openpyxl import load_workbook as _lw
    rm = _lw(os.path.join(target, CP.FILES["roadmap"]), data_only=True)["H1 2027 runs"]
    hdr = [c.value for c in rm[3]]
    ok("PL6 the roadmap files each run's block, the window's start and end and the token budget",
       all(h in hdr for h in ("block", "window_start", "window_end", "token_budget")) and
       all(r[hdr.index("block")] for r in rm.iter_rows(min_row=4, max_row=14, values_only=True) if r[0]))
    works_txt = pdf_text(CP.FILES["notice"])
    ok("PL7 the notice files the 2027 works' planned starts and hours", all(w[0] in works_txt for w in P.WORKS_2027))
    # units: each graded column is in the unit its name says, by its range
    un = [("steps", "step_time_ms", 300, 90000), ("samples", "fwd_bwd_ms", 100, 90000), ("meter", "it_load_kw", 1000, 9000),
          ("bench", "tokens_per_gpu_s", 300, 20000), ("registry", "token_budget", 1e11, 1e14)]
    for key, col, lo_, hi_ in un:
        v = pd.to_numeric(pd.read_csv(os.path.join(target, CP.FILES[key]), usecols=[col])[col], errors="coerce").dropna()
        ok("U1 %s.%s is in %s (median %.4g)" % (key, col, col.split("_")[-1], v.median()), lo_ <= v.median() <= hi_)
    ok("U2 UTC columns end in Z and the provider's columns are Helsinki local",
       pd.read_csv(os.path.join(target, CP.FILES["steps"]), nrows=5)["ts_utc"].str.endswith("Z").all() and
       "timestamp_local" in pd.read_csv(os.path.join(target, CP.FILES["meter"]), nrows=2).columns)
    # ---------------- inputs
    files = [os.path.join(dp, f) for dp, _, fs in os.walk(target) for f in fs]
    ok("I1 ten or more usable files", len(files) >= 10, len(files))
    exts = {os.path.splitext(f)[1] for f in files}
    ok("I2 two or more file categories", len(exts & {".csv", ".jsonl"}) >= 1 and len(exts & {".pdf", ".yaml", ".xlsx"}) >= 2, sorted(exts))
    big = max(sum(1 for _ in open(f)) for f in files if f.endswith(".csv"))
    ok("I3 a CSV of 20,000 rows or more", big >= 20000, big)
    stops = os.path.join(target, CP.FILES["stops"])
    ok("I4 a CSV of ten printed pages or more (the interruption log, 40,000 characters or more)",
       os.path.getsize(stops) >= 40000, os.path.getsize(stops))
    ok("I5 two distractors, unused by the golden", len(CP.DISTRACTORS) == 2 and not used & {CP.FILES[k] for k in CP.DISTRACTORS})
    ok("I6 no readme, dictionary or notes file", not any(re.search(r"readme|dictionary|field_notes|manifest_of|notes\.", os.path.basename(f), re.I) for f in files))
    # distractor deletion
    tmp = tempfile.mkdtemp()
    t2 = os.path.join(tmp, "target")
    shutil.copytree(target, t2)
    for k in CP.DISTRACTORS:
        os.remove(os.path.join(t2, CP.FILES[k]))
    G3 = A.golden(t2)
    ok("I7 the golden is unchanged with both distractors deleted", A.late_set(G3, G3["days"]) == late and
       all(abs(G3["days"][k] - G["days"][k]) < 1e-9 for k in runs))
    shutil.rmtree(tmp)
    # ---------------- realism
    reg = pd.read_csv(os.path.join(target, CP.FILES["registry"]))
    ok("Z1 registry node counts are not one value", reg["nodes"].nunique() > 4)
    ok("Z2 no round headline: GPU-days held is not a round thousand", fig["held_2026_total"] % 1000 != 0)
    st = pd.read_csv(os.path.join(target, CP.FILES["states"]))
    ok("Z3 the halls' node states differ", st[st.hall == "A"]["allocated"].mean() != st[st.hall == "B"]["allocated"].mean())
    al = pd.read_csv(os.path.join(target, CP.FILES["stops"]))
    ok("Z4 alert ids are not an arithmetic sequence", al["alert_id"].str[4:].astype(int).diff().nunique() > 5)
    ok("Z5 personas are the guard's draw", P.INFRA_LEAD in ("Pia Kuosmanen",) and P.COMMITTEE_CHAIR == "Esa Airaksinen")
    meter = pd.read_csv(os.path.join(target, CP.FILES["meter"]))
    ok("Z6 the meter carries collector gaps", len(meter) < 2 * 87840)
    ok("Z7 the meter carries the repeated autumn hour", meter[meter.hall == "HALL-B"]["timestamp_local"].duplicated().sum() >= 12)
    # ---------------- deliverables agree with figures.json
    note = open(os.path.join(TASK, "golden", "h1_2027_run_windows_note.md")).read()
    for k in late:
        ok("D1 the note names %s with its expected days" % k, k in note and ("%.1f" % fig["days_%s" % k]) in note)
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("D2 no em dash in the answer blocks or the note", "—" not in sub and "—" not in note and "–" not in sub)
    from openpyxl import load_workbook
    wb = load_workbook(os.path.join(TASK, "golden", "h1_2027_throughput_bridge.xlsx"), data_only=True)
    ws = wb["Runs H1 2027"]
    vals = {r[0]: r for r in ws.iter_rows(min_row=5, max_row=15, values_only=True) if r[0]}
    ok("D3 the workbook's expected days match figures.json", all(abs(vals[k][6] - fig["days_%s" % k]) < 1e-9 for k in runs))
    ok("D4 the golden folder holds exactly the two requested files",
       sorted(os.listdir(os.path.join(TASK, "golden"))) == ["h1_2027_run_windows_note.md", "h1_2027_throughput_bridge.xlsx"])
    fails = [o for o in OUT if not o[1]]
    for label, good, detail in OUT:
        print("%s  %s%s" % ("PASS" if good else "FAIL", label, ("  [%s]" % str(detail)[:160]) if (not good and detail != "") else ""))
    print("%d checks, %d FAIL" % (len(OUT), len(fails)))
    return 1 if fails else 0


def fig_days(fig, prefix):
    return {k[len(prefix):]: v for k, v in fig.items() if k.startswith(prefix)}


def grade(res, entry):
    import importlib.util
    spec = importlib.util.spec_from_file_location("effort", os.path.join(TASK, "..", ".claude", "skills", "stumping", "effort.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.grade(entry, res)[0]


def mess_variants():
    def keep_duplicates(F):
        F["steps"] = pd.concat([F["steps"], F["steps"].iloc[::997]]).reset_index(drop=True)

    def meter_as_utc(F):
        pass   # the meter read without the clock change resolution is checked by the repeated hour (Z7)

    def drop_alert_duplicates(F):
        F["stops"] = F["stops"].drop_duplicates(subset=["run_id", "failed_at_utc"]).reset_index(drop=True)

    return [("step-log repeats kept", keep_duplicates), ("alert repeats collapsed by time", drop_alert_duplicates)]


def variant(target, mutate):
    orig = A.load
    def load2(T):
        F = orig(T)
        mutate(F)
        return F
    A.load = load2
    try:
        return A.golden(target)
    finally:
        A.load = orig


if __name__ == "__main__":
    sys.exit(main(fast="--fast" in sys.argv))
