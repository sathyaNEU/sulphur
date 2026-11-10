"""task16 build: the pilot (real training runs, trained once and kept in generator/cache), the pack under target/,
the checks, the golden deliverables, figures.json, effort.json, submission.md, metadata.json and both zips.

    python3 make.py            builds in place (trains whatever the cache lacks first)
    python3 make.py --twice    builds twice into scratch folders and fails unless the two packs, goldens, zips,
                               figures, effort and answer blocks are byte-identical
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OMP_NUM_THREADS", "1")

import build as BD  # noqa: E402
import checks as CK  # noqa: E402
import deliver as DL  # noqa: E402
import effort_passes as EP  # noqa: E402
import pack as PK  # noqa: E402
import postprocess as PP  # noqa: E402
import runner as R  # noqa: E402
import sweep as S  # noqa: E402
import writeup as WU  # noqa: E402

ZONE = "Europe/Oslo"
COVERS = {
    "metrics": "every scalar the pilot's training jobs logged to the tracking server (training loss, learning rate, gradient norm, development loss and accuracy), 28 September to 1 November 2026",
    "runs": "the tracking server's run records for the pilot: status, model width, learning rate, schedule, label shards, seed, logger and code revision",
    "items": "the loss of each finished run's final checkpoint on every development item (one column per run)",
    "devsplit": "the development split: each item's hold-out shard, point reference and class",
    "shards": "the register of label shards: route, points, lot, survey block, date registered, use",
    "routes": "the three labelling routes and their source",
    "classes": "the ten Folk sediment classes the model predicts",
    "jobs": "scheduler accounting for the group's account, 21 September to 1 November 2026",
    "ckpt": "the checkpoint store's listing for the pilot: periodic and final checkpoints and item dumps, with size, digest and time",
    "bench": "the benchmark server's record of the team's uploads in the pilot period: digest, score, status, quota left",
    "notes": "the group's meeting notes of 5 November 2026: the slot's rules, the recipe, the shortlist, actions",
    "shortlist": "the shortlisted configurations with steps and timings for the slot",
    "defaults": "the trainer's defaults file",
    "launch": "the batch script that submitted the vendor-label trials",
    "probe": "the engineer's September throughput probe by node, width and batch size",
    "counts": "data preparation's count of class labels in every shard",
}
TITLE = "MML group: which shortlisted training configuration to name for the NSSMP 2027 slot, and the benchmark loss to state"


def metadata(target, counts):
    files = sorted(os.listdir(target))
    key_of = {v: k for k, v in PK.FILES.items()}
    return {
        "task": "task16", "title": TITLE,
        "domain": "Machine Learning Research, General Statistics & Data Science", "task_type": "scaling laws",
        "objective": "Forecasting & Predictive Modeling", "as_of": "2026-11-05",
        "deliverables": [DL.WORKBOOK, DL.NOTE],
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "field_terms": ["seed"],
        "stated_inputs": ["0.0005", "0.001", "512", "256", "1024", "128", "128,000", "1,024,000", "0.002"],
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "categories": ["spreadsheet", "text", "code"],
                        "largest_file": PK.FILES["metrics"], "largest_file_rows": counts["metrics"],
                        "long_file": PK.FILES["ckpt"], "long_file_rows": counts["ckpt"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated for this task. Every training run is a real optimisation run of a small classifier (the "
                               "generator's own trainer) on a simulated population of survey points with three simulated labelling "
                               "routes; the cluster, tracking, store and benchmark records are simulated around those runs. The "
                               "research group, the contractor, the programme and the people are invented.",
                     "date": "2026-11-10", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS[key_of[f]], "made": "written by task16/generator/make.py from the cached training runs (deterministic)"}
                  for f in files],
    }


def build(task_dir, gen_out, prompt_path):
    target = os.path.join(task_dir, "target")
    golden = os.path.join(task_dir, "golden")
    shutil.rmtree(golden, ignore_errors=True)
    os.makedirs(target, exist_ok=True)
    os.makedirs(gen_out, exist_ok=True)
    jobs, counts = BD.run(target)
    G, F, E = CK.run(target, gen_out, prompt_path)
    bad = [r for r in CK.RESULTS if not r[1]]
    for name, ok, d in bad:
        print("FAIL", name, d)
    if bad:
        raise SystemExit("checks failed: %d of %d" % (len(bad), len(CK.RESULTS)))
    scratch = tempfile.mkdtemp(prefix="t16chart-")
    try:
        DL.write_all(G, F, golden, scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    with open(os.path.join(gen_out, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(gen_out, "effort.json"), "w", encoding="utf-8") as fh:
        json.dump(E, fh, indent=1, ensure_ascii=False)
    WU.write(F, os.path.join(task_dir, "submission.md"))
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(metadata(target, counts), fh, indent=1, ensure_ascii=False)
    PP.own_mtimes(golden, {})
    PP.zip_folder(target, os.path.join(task_dir, "target.zip"), zone=ZONE)
    PP.zip_folder(golden, os.path.join(task_dir, "golden.zip"), zone=ZONE)
    return len(CK.RESULTS), counts


def same(a, b):
    out = []
    for root, _, names in os.walk(a):
        for n in sorted(names):
            pa = os.path.join(root, n); pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.exists(pb) or not filecmp.cmp(pa, pb, shallow=False):
                out.append(os.path.relpath(pa, a))
    return out


if __name__ == "__main__":
    # the pilot's runs, then the author-side truth runs checks.py compares the forecast with (trained once, kept in cache/)
    R.run_all([j["train"] for j in S.pilot_specs()], verbose=False)
    R.run_all([j["train"] for j in S.truth_specs()] + [j["train"] for j in S.clean_truth_specs()], verbose=False)
    prompt = os.path.join(TASK, "prompt.txt")
    if "--twice" in sys.argv:
        a, b = tempfile.mkdtemp(prefix="t16a-"), tempfile.mkdtemp(prefix="t16b-")
        try:
            for d in (a, b):
                build(d, os.path.join(d, "generator"), prompt)
            diff = same(a, b) + same(b, a)
            print("two builds: %s" % ("byte-identical (%d files)" % sum(len(f) for _, _, f in os.walk(a)) if not diff else "DIFFER: %s" % sorted(set(diff))))
            sys.exit(1 if diff else 0)
        finally:
            shutil.rmtree(a, ignore_errors=True); shutil.rmtree(b, ignore_errors=True)
    n, counts = build(TASK, HERE, prompt)
    print("built: %d checks green; pack %s" % (n, counts))
