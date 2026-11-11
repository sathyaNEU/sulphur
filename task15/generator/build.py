"""Build task15: the world and its three runs, every file under target/, the golden analysis, figures.json and
effort.json, the golden deliverables, submission.md, metadata.json, the checks, and both zips.

    python3 build.py              build into the task folder
    python3 build.py --data-only  the pack only
    python3 build.py --twice      two builds into scratch folders, compared byte for byte
    python3 build.py --out DIR    one build into DIR (the gates' rebuild check)"""
import datetime as dt
import filecmp
import json
import os
import pickle
import shutil
import sys
import tempfile

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
REPO = os.path.dirname(TASK)
TARGET = os.path.join(TASK, "target")
CACHE = os.path.join(REPO, ".cache", "task15_world.pkl")
sys.path.insert(0, HERE)

import docs as DC  # noqa: E402
import pack as PK  # noqa: E402
import world as W  # noqa: E402

UTC = dt.timezone.utc
# the exports' own times (the systems write no stamp into a CSV), in the fiction's calendar
EXPORTED = {
    PK.F_D25: dt.datetime(2026, 9, 2, 4, 5, tzinfo=UTC), PK.F_D26: dt.datetime(2026, 9, 2, 4, 9, tzinfo=UTC),
    PK.F_FC: dt.datetime(2026, 9, 2, 4, 21, tzinfo=UTC), PK.F_BI: dt.datetime(2026, 9, 7, 3, 40, tzinfo=UTC),
    PK.F_PROF: dt.datetime(2025, 9, 12, 7, 33, tzinfo=UTC), PK.F_COMP: dt.datetime(2026, 8, 25, 8, 2, tzinfo=UTC),
    PK.F_WEATHER: dt.datetime(2026, 9, 1, 1, 15, tzinfo=UTC), PK.F_STAFF: dt.datetime(2026, 9, 3, 10, 40, tzinfo=UTC),
}
ZONE = "Europe/Copenhagen"


def world_and_runs(seed=W.SEED, use_cache=True):
    key = (seed, os.path.getmtime(os.path.join(HERE, "world.py")))
    if use_cache and os.path.exists(CACHE):
        try:
            obj = pickle.load(open(CACHE, "rb"))
            if obj["key"] == key:
                return obj["w"]
        except Exception:
            pass
    w = W.World(seed)
    w.run(W.ISPILOT, "actual")
    w.run(np.zeros(W.NS, bool), "L")
    w.run(np.ones(W.NS, bool), "N")
    if use_cache:
        os.makedirs(os.path.dirname(CACHE), exist_ok=True)
        pickle.dump({"key": key, "w": w}, open(CACHE, "wb"))
    return w


def data_files(w, target=TARGET):
    if os.path.exists(target):
        shutil.rmtree(target)
    os.makedirs(target)
    R = PK.Records(w, w.runs["actual"])
    PK.write_daily(target, R)
    PK.write_forecasts(target, R)
    PK.write_bi(target, R)
    PK.write_profile(target, w)
    PK.write_competitors(target)
    PK.write_weather(target, w)
    PK.write_staff(target, w)
    st = PK.STAMPS
    PK.write_items(target, st[PK.F_ITEMS])
    PK.write_stores(target, w, st[PK.F_STORES])
    PK.write_promo(target, w, st[PK.F_PROMO])
    DC.write_docs(target, R)
    return R


COVERS = {
    PK.F_D25: "the ERP's daily store and fresh item extract for 2025 in the old export layout (from 3 March 2025)",
    PK.F_D26: "the ERP's daily store and fresh item extract for 2026 in the new export layout (to 30 August 2026)",
    PK.F_FC: "the order proposal log from 1 January 2026: both forecasts, the safety stock, the order and its basis",
    PK.F_BI: "business intelligence's weekly history by store and category, fresh and ambient, from 2025 week 10",
    PK.F_PROF: "the hourly fresh sales profile by format, category and weekday behind the store app's empty-shelf alert",
    PK.F_ITEMS: "the fresh item register: numbers, pairs, shelf life, case packs, prices and costs",
    PK.F_STORES: "the store register: format, address, opening hours, sales area",
    PK.F_PROMO: "the weekly leaflet plan for 2025 and 2026",
    PK.F_COMP: "market intelligence's log of competitor openings and closures near Fjordkob stores",
    PK.F_PILOT: "the pilot agreement with Kornblomst Analytics, with the 2027 price list",
    PK.F_DASH: "business intelligence's pilot dashboard to week 35",
    PK.F_WEATHER: "daily weather by town from the chain's weather service",
    PK.F_STAFF: "weekly fresh department and ordering hours by store in 2026",
}


def metadata(target):
    import deliver as D
    files = sorted(os.listdir(target))
    rows = {}
    for f in files:
        if f.endswith(".csv"):
            with open(os.path.join(target, f), "rb") as fh:
                rows[f] = sum(1 for _ in fh) - 1
    return {
        "task": "task15",
        "architecture": 2,
        "title": "Which Fjordkob store formats move their fresh ordering to Kornblomst's forecast for 2027, and why the pilot "
                 "stores' fresh sales grew less and their waste fell further than the other stores'",
        "domain": "Machine Learning Research, General Statistics & Data Science",
        "task_type": "benchmarking and ablations (controlled evaluation, isolating component effects)",
        "objective": "Comparative Analysis & Explanation",
        "as_of": "2026-09-07",
        "deliverables": [D.WORKBOOK, D.NOTE],
        "distractor_files": list(PK.DISTRACTORS),
        "stated_inputs": ["{:,}".format(int(W.LICENCE[f])) for f in W.FORMATS],
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "categories": ["spreadsheet", "text"],
                        "largest_file": PK.F_D25, "largest_file_rows": rows[PK.F_D25],
                        "long_file": PK.F_BI, "long_file_rows": rows[PK.F_BI]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated for this task by simulating the process that makes the files: customers arriving "
                               "through each store's trading day and buying what is on the shelf, the ERP's order-up-to rule "
                               "ordering on AutoOrdre's or Kornblomst's forecast, write-offs at the end of shelf life, the "
                               "systems' exports, a regional weather and event signal, the formats' trends and seasons, and "
                               "discounter openings. The chain, its stores' figures, the vendor, the documents and the people "
                               "are invented; the towns are real.",
                     "date": "2026-11-11", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   **({"rows": rows[f]} if f in rows else {}), "covers": COVERS[f],
                   "made": "written by task15/generator/build.py from the simulated process (deterministic)"}
                  for f in files],
    }


def build(task_dir, gen_out, use_cache=True, zips=True, checks=True):
    import checks as CK
    import deliver as D
    import figures as FG
    import golden as GD
    import writeup as WU
    target = os.path.join(task_dir, "target")
    golden_dir = os.path.join(task_dir, "golden")
    os.makedirs(gen_out, exist_ok=True)
    w = world_and_runs(use_cache=use_cache)
    data_files(w, target)
    T = GD.load(target)
    R = GD.results(T, reps=400)
    R = FG.extras(R, T)
    F, E = FG.write(R, gen_out)
    if checks:
        CK.run(w, R, F, E, target)
    scratch = tempfile.mkdtemp(prefix="t15chart-")
    try:
        D.write_all(R, F, golden_dir, scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    WU.write(F, D.WORKBOOK, D.NOTE, task_dir)
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(metadata(target), fh, indent=1, ensure_ascii=False)
    import postprocess as PP
    PP.own_mtimes(target, EXPORTED)
    PP.own_mtimes(golden_dir, {})
    if zips:
        PP.zip_folder(target, os.path.join(task_dir, "target.zip"), zone=ZONE)
        PP.zip_folder(golden_dir, os.path.join(task_dir, "golden.zip"), zone=ZONE)
    return F


def same(a, b):
    out = []
    for root, _, names in os.walk(a):
        for n in sorted(names):
            pa = os.path.join(root, n)
            pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.exists(pb) or not filecmp.cmp(pa, pb, shallow=False):
                out.append(os.path.relpath(pa, a))
    return out


if __name__ == "__main__":
    if "--data-only" in sys.argv:
        data_files(world_and_runs())
        print("data files written:", sorted(os.listdir(TARGET)))
    elif "--out" in sys.argv:
        out = sys.argv[sys.argv.index("--out") + 1]
        build(out, os.path.join(out, "generator"), use_cache=False, checks=False)
        print("built into", out)
    elif "--twice" in sys.argv:
        a, b = tempfile.mkdtemp(prefix="t15a-"), tempfile.mkdtemp(prefix="t15b-")
        try:
            for d in (a, b):
                build(d, os.path.join(d, "generator"), use_cache=False, checks=False)
            diff = same(a, b) + same(b, a)
            n = sum(len(f) for _, _, f in os.walk(a))
            print("two builds: %s" % ("byte-identical (%d files)" % n if not diff else "DIFFER: %s" % sorted(set(diff))))
            sys.exit(1 if diff else 0)
        finally:
            shutil.rmtree(a, ignore_errors=True)
            shutil.rmtree(b, ignore_errors=True)
    else:
        F = build(TASK, HERE)
        print("built: switch %s; savings %s" % (F["switch"], F["saving"]))
