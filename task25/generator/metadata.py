"""metadata.json, outside target/: what the task is about, the deliverables, the distractors and each file's
provenance. Nothing here narrates a method or carries a graded figure."""
import json
import os

import cutpack as CP
import params as P

ABOUT = {
    "registry": "every pretraining, extension, scale-test and ablation run launched in 2026, as the run tracker exports it",
    "steps": "the trainer's step log for every 2026 run, one row each time the trainer logs",
    "stops": "the alerting system's record of every stop and resume in 2026",
    "alloc": "the scheduler's node allocations for each run between stops",
    "samples": "the profiler's per-rank timings on its sampled steps",
    "manifests": "the data loader's manifests for a share of the profiler's sampled steps",
    "states": "the scheduler's node states per hall, every five minutes",
    "meter": "the provider's five-minute IT load per hall",
    "works": "the provider's work orders, 2025 and 2026",
    "incidents": "the provider's facility incident log, 2026",
    "schedule": "the provider's service schedule for the two halls",
    "notice": "the provider's notice of planned works for January to June 2027",
    "energy": "the provider's monthly energy invoices for 2026",
    "bench": "the infrastructure team's throughput benchmark results for 2026 and 2027 configurations",
    "harness": "the benchmark harness configuration",
    "roadmap": "the H1 2027 roadmap as filed for the committee",
    "lengths": "the data team's sample of document lengths by source",
    "mixes": "the data team's 2026 and 2027 data mixes",
    "rules": "the compute committee's allocation rules for the H1 2027 round",
    "evals": "checkpoint evaluation scores for the 2026 runs",
}


def write(task_dir):
    files = {}
    for k, rel in CP.FILES.items():
        files[rel] = {"source": "generated (simulated %s systems)" % P.ORG if k not in ("schedule", "notice", "works",
                      "incidents", "meter", "energy") else "generated (simulated %s systems)" % P.PROVIDER,
                      "covers": ABOUT[k], "license": "synthetic, CC0"}
    for run in P.ROADMAP_2027:
        files["plan_2027/configs/%s.yaml" % run[0]] = {"source": "generated (simulated %s systems)" % P.ORG,
                                                       "covers": "the training team's launch config for %s" % run[0],
                                                       "license": "synthetic, CC0"}
    meta = {
        "task": "task25",
        "organisation": "%s (fictional)" % P.ORG,
        "decision": "which H1 2027 pretraining runs will not reach their token budgets inside their reserved GPU windows, and how many days each will take against its benchmark",
        "deliverables": ["h1_2027_throughput_bridge.xlsx", "h1_2027_run_windows_note.md"],
        "pull_date": "2026-11-06",
        "as_of": "2026-11-06",
        "record_window": "2026-01-01 to 2026-10-31",
        "generated": True,
        "license": "synthetic data, CC0; no third-party data",
        "distractor_files": [CP.FILES[k] for k in CP.DISTRACTORS],
        "files": files,
    }
    with open(os.path.join(task_dir, "metadata.json"), "w") as fh:
        json.dump(meta, fh, indent=1)
