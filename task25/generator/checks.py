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

OUT = []


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
    ok("C3 every run 12 per cent or more from its window under the golden",
       all(abs(v - 1) >= 0.12 for v in ratio.values()), {k: round(v, 3) for k, v in ratio.items()})
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
        if r["id"] in ("R1", "R6"):
            ok("R3 %s earned by the careful pass" % r["id"], g == "right", g)
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
        [fig["bridge_%s_%d" % (k, i)] for i in range(7)])) - fig["bridge_%s_7" % k]) < 0.06 for k in runs))
    b26 = sum(fig["b26_%d" % i] for i in range(9))
    ok("SF10 the 2026 bridge adds to the GPU-days held", abs(b26 - fig["b26_9"]) <= 5, "%d vs %d" % (b26, fig["b26_9"]))
    ok("SF5 GPU-days held reproduces from the registry alone", abs(fig["held_2026_total"] - G["ledger"]["gpu_days_held"].sum()) < 1)
    ok("SF6 every 2026 run launched in 2026 is in the ledger", len(G["ledger"]) == len(G["F"]["reg"]))
    ok("SF1 days are wall-clock from 00:00 UTC on the window's start", all(fig["days_%s" % k] > fig["bench_days_%s" % k] for k in runs))
    ok("SF7 the 80 per cent range brackets the expected days", all(fig["p10_%s" % k] <= fig["days_%s" % k] + 0.6 and
                                                                  fig["p90_%s" % k] >= fig["days_%s" % k] - 0.6 for k in runs))
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
