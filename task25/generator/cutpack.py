"""Write target/ from the simulated record: the pack Saukko Labs' infrastructure team pulled on 6 November 2026."""
import os
import shutil

import numpy as np

import docs as DC
import pack as PK
import params as P
import records as RC

FILES = {
    "registry": "runs/run_registry_2026.csv",
    "steps": "runs/step_log_2026.csv",
    "stops": "runs/interruptions_2026.csv",
    "alloc": "runs/node_allocations_2026.csv",
    "samples": "profiling/rank_step_samples_2026.csv",
    "manifests": "profiling/packing_manifests_2026.jsonl",
    "states": "cluster/node_states_2026.csv",
    "meter": "provider/hall_it_load_2026.csv",
    "works": "provider/work_orders_2025_2026.csv",
    "incidents": "provider/incident_log_2026.csv",
    "schedule": "provider/service_schedule_S3_kaivola.pdf",
    "notice": "provider/planned_works_h1_2027.pdf",
    "energy": "provider/energy_invoices_2026.xlsx",
    "bench": "benchmark/tpbench_results.csv",
    "harness": "benchmark/tpbench_harness.yaml",
    "roadmap": "plan_2027/roadmap_h1_2027.xlsx",
    "lengths": "data/doc_length_sample.csv",
    "mixes": "data/data_mixes.csv",
    "rules": "policy/compute_allocation_rules_CAR-2027-1.pdf",
    "evals": "evals/checkpoint_evals_2026.csv",
}
DISTRACTORS = ("energy", "evals")


def write(target, rec):
    if os.path.isdir(target):
        shutil.rmtree(target)
    for rel in FILES.values():
        os.makedirs(os.path.join(target, os.path.dirname(rel)), exist_ok=True)
    os.makedirs(os.path.join(target, "plan_2027", "configs"), exist_ok=True)
    rng = np.random.default_rng(P.SEED + 41)
    f = lambda k: os.path.join(target, FILES[k])
    alloc = PK.allocations(rec)              # assigns the failed node to each hardware stop first
    alloc.to_csv(f("alloc"), index=False)
    PK.interruptions(rec).to_csv(f("stops"), index=False)
    PK.registry(rec).to_csv(f("registry"), index=False)
    PK.step_log(rec, rng).to_csv(f("steps"), index=False)
    samples, man = PK.profiles(rec, rec["x"], np.random.default_rng(P.SEED + 43))
    samples.to_csv(f("samples"), index=False)
    with open(f("manifests"), "w") as fh:
        fh.write("\n".join(man) + "\n")
    PK.node_states(rec, np.random.default_rng(P.SEED + 45)).to_csv(f("states"), index=False)
    PK.hall_meter(rec, np.random.default_rng(P.SEED + 47)).to_csv(f("meter"), index=False)
    PK.work_orders(rec).to_csv(f("works"), index=False)
    PK.incident_log(rec, rng).to_csv(f("incidents"), index=False)
    PK.benchmark(rec, np.random.default_rng(P.SEED + 49)).to_csv(f("bench"), index=False)
    with open(f("harness"), "w") as fh:
        fh.write(PK.harness_yaml())
    PK.length_sample(np.random.default_rng(P.SEED + 51)).to_csv(f("lengths"), index=False)
    PK.mixes().to_csv(f("mixes"), index=False)
    for run in P.ROADMAP_2027:
        with open(os.path.join(target, "plan_2027", "configs", "%s.yaml" % run[0]), "w") as fh:
            fh.write(PK.config_yaml(run))
    PK.checkpoint_evals(rec, np.random.default_rng(P.SEED + 53)).to_csv(f("evals"), index=False)
    DC.energy_xlsx(f("energy"), PK.energy_invoices(rec))
    DC.roadmap_xlsx(f("roadmap"))
    DC.allocation_rules(f("rules"))
    DC.service_schedule(f("schedule"))
    DC.works_notice(f("notice"))
