"""task15 build: the world, the pack under target/, the conformed record read back from the pack alone, every
figure with its rivals and hurried passes, the checks, the golden deliverables, figures.json, effort.json,
submission.md, metadata.json and both zips.

    python3 build.py                 builds in place (task15/)
    python3 build.py --out <dir>     builds the same tree into <dir> (gates.py compares two of these byte for byte)
"""
import os

for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")

import datetime as dt  # noqa: E402
import hashlib  # noqa: E402
import json  # noqa: E402
import pickle  # noqa: E402
import shutil  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import docs as DC  # noqa: E402
import figs as FG  # noqa: E402
import golden as G  # noqa: E402
import pack as PK  # noqa: E402
import panel as PN  # noqa: E402
import postprocess as PP  # noqa: E402
import verify as V  # noqa: E402
import world as W  # noqa: E402

Y = W.SOW                                # the year the pack is cut in (the season after the last harvest)
AS_OF = "%d-02-12" % Y
ZONE = "Australia/Melbourne"
UTC = dt.timezone.utc
FN = W.FILES
DISTRACTORS = [FN["quality"], FN["disease"], FN["seed"]]
# workbooks: creator, last saved by, created, modified (UTC), title, company
BOOKS = {
    FN["sites"]: ("Jesse Gibson", "Jesse Gibson", "%d-03-14T02:41:00Z" % (W.FIRST + 4), "%d-04-21T23:18:00Z" % (Y - 1),
                  "Trial sites", "Banyena Grain Genetics"),
    FN["register"]: ("Banyena breeding database", "Jesse Gibson", "%d-02-08T22:52:00Z" % Y, "%d-02-08T22:57:00Z" % Y,
                     "Line register", "Banyena Grain Genetics"),
    FN["nominations"]: ("Meredith Cooke", "Meredith Cooke", "%d-02-13T04:26:00Z" % W.FIRST_SOW,
                        "%d-02-20T05:34:00Z" % (Y - 1), "HRBS nominations", "Banyena Grain Genetics"),
    FN["seed"]: ("Jesse Gibson", "Jesse Gibson", "%d-02-02T22:07:00Z" % Y, "%d-02-04T03:45:00Z" % Y,
                 "Seed store inventory, February %d" % Y, "Banyena Grain Genetics"),
}
# the systems' exports, each written when its job ran
EXPORTS = {
    FN["old"]: dt.datetime(W.OLD_LAST + 1, 2, 25, 3, 12, 40, tzinfo=UTC),
    FN["new"]: dt.datetime(Y, 2, 8, 22, 41, 7, tzinfo=UTC),
    FN["entries"]: dt.datetime(Y, 2, 8, 22, 43, 52, tzinfo=UTC),
    FN["trials"]: dt.datetime(Y, 2, 8, 22, 44, 15, tzinfo=UTC),
    FN["rain"]: dt.datetime(Y, 1, 19, 4, 5, 33, tzinfo=UTC),
    FN["irrigation"]: dt.datetime(Y - 1, 12, 2, 1, 26, 19, tzinfo=UTC),
    FN["results"]: dt.datetime(Y, 2, 5, 2, 30, 11, tzinfo=UTC),
    FN["seasons"]: dt.datetime(Y, 2, 5, 2, 30, 48, tzinfo=UTC),
    FN["quality"]: dt.datetime(Y, 1, 27, 5, 51, 2, tzinfo=UTC),
    FN["disease"]: dt.datetime(Y - 1, 12, 11, 3, 17, 26, tzinfo=UTC),
}
COVERS = {
    FN["old"]: "Banyena's plot harvest record from the old logger, every trial plot %d to %d" % (W.FIRST, W.OLD_LAST),
    FN["new"]: "Banyena's plot harvest record from the harvest system, every trial plot %d to %d" % (W.OLD_LAST + 1,
                                                                                                   W.LAST),
    FN["entries"]: "each programme trial's entry list (entry number to line)",
    FN["trials"]: "the programme's trials: season, stage, site, sowing and harvest dates, layout",
    FN["sites"]: "the ten trial sites",
    FN["rain"]: "monthly rain at the gauge nearest each trial site",
    FN["irrigation"]: "every watering of the Kerang trials",
    FN["register"]: "every line's cross code, WI number, cross, first trial season and status; the check varieties",
    FN["nominations"]: "Banyena's nominations to the series with the index quoted for each",
    FN["results"]: "the series' published site means for every entry, yield and lodging",
    FN["seasons"]: "the series' site seasons: dates, April to October rain, trial mean and CV",
    FN["protocol"]: "the series' trial protocol, with its definition of relative yield",
    FN["deed"]: "the option deed's schedule on nominations and the uptake standard",
    FN["handbook"]: "Banyena's trial handbook: stages, codes, plot records, the high-rainfall index",
    FN["review"]: "the trials team's close-out of the %d season" % W.LAST,
    FN["quality"]: "the quality laboratory's Stage 3 results",
    FN["disease"]: "the disease nurseries' scores",
    FN["seed"]: "the seed store's inventory of Stage 3 lines",
}


def make_pack(target):
    shutil.rmtree(target, ignore_errors=True)
    os.makedirs(target)
    w = W.build()
    facts, counts, paths = PK.write_all(w, target)
    for name, (creator, last_by, created, modified, title, company) in BOOKS.items():
        PP.normalize_ooxml(os.path.join(target, name), creator, last_by, created, modified, title=title, excel=True,
                           company=company)
    DC.write_all(target, w, facts, counts)
    PP.own_mtimes(target, EXPORTS)
    return w, facts, counts


def digest(target):
    h = hashlib.sha256()
    for name in sorted(os.listdir(target)):
        if name.endswith((".csv", ".xlsx")):
            h.update(name.encode())
            h.update(open(os.path.join(target, name), "rb").read())
    for src in ("golden.py", "figs.py", "verify.py"):
        h.update(open(os.path.join(HERE, src), "rb").read())
    h.update(("%s|%s|%s" % (FG.SIMS, FG.RIVAL_SIMS, W.STANDARD)).encode())
    h.update(open(os.path.join(target, FN["deed"]), "rb").read())
    return h.hexdigest()


def analysis(target, cache=True):
    """Every figure, computed from the pack as shipped. Kept by the pack's digest (generator/.cache, not tracked),
    so checks.py and a second look do not pay for the simulation twice."""
    key = digest(target)
    cdir = os.path.join(HERE, ".cache")
    path = os.path.join(cdir, "analysis_%s.pkl" % key[:16])
    if cache and os.path.exists(path):
        with open(path, "rb") as fh:
            return pickle.load(fh)
    P = V.load(target)
    A = FG.compute(P)
    if cache:
        os.makedirs(cdir, exist_ok=True)
        for old in os.listdir(cdir):
            if old.startswith("analysis_"):
                os.remove(os.path.join(cdir, old))
        with open(path, "wb") as fh:
            pickle.dump(A, fh)
    return A


def build(task_dir, gen_dir, cache=True):
    import checks as CK
    import deliver as DL
    import writeup as WU
    t0 = time.time()
    target = os.path.join(task_dir, "target")
    golden = os.path.join(task_dir, "golden")
    os.makedirs(gen_dir, exist_ok=True)
    w, facts, counts = make_pack(target)
    A = analysis(target, cache=cache)
    counts = dict(counts)
    files = sorted(os.listdir(target))
    counts["files"] = len(files)
    F = FG.figures(A, counts, files=dict(FN, book=DL.BOOK, chart=DL.CHART, note=DL.NOTE))
    E, B = FG.effort(A, F)
    CK.RESULTS.clear()
    CK.run(target, w, A, F, E, B)
    bad = [r for r in CK.RESULTS if not r[1]]
    for name, ok, d in bad:
        print("FAIL", name, d)
    if bad:
        raise SystemExit("checks failed: %d of %d" % (len(bad), len(CK.RESULTS)))
    shutil.rmtree(golden, ignore_errors=True)
    os.makedirs(golden)
    DL.write_all(F, golden)
    PP.own_mtimes(golden, DL.STAMPS)
    with open(os.path.join(gen_dir, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False, sort_keys=True)
    with open(os.path.join(gen_dir, "effort.json"), "w", encoding="utf-8") as fh:
        json.dump(E, fh, indent=1, ensure_ascii=False)
    WU.write(F, os.path.join(task_dir, "submission.md"))
    meta = {
        "task": "task15",
        "title": "Banyena Grain Genetics: why its nominations to the High Rainfall Barley Series came in under its own "
                 "index, and the lines to nominate for %d" % Y,
        "domain": "General Statistics & Data Science",
        "task_type": "multiple testing and selective inference (selection on noisy means across a staged trial programme)",
        "objective": "Comparative Analysis & Explanation", "as_of": AS_OF,
        "deliverables": sorted(os.listdir(golden)),
        "distractor_files": DISTRACTORS,
        "stated_inputs": ["%.1f" % W.STANDARD],
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "largest_file": FN["new"], "largest_file_rows": counts["new_rows"],
                        "long_file": FN["entries"], "long_file_rows": counts["entry_rows"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated for this task by simulating a staged barley breeding programme in western "
                               "Victoria (its trial designs, seasons, plots, harvest systems and advancement decisions) "
                               "and the independent trial series its lines are nominated to; every organisation, "
                               "person, variety, line, record and figure is invented",
                     "date": "2026-11-10", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS.get(f, ""), "made": "generated by task15/generator/build.py (seeded, deterministic)"}
                  for f in files],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
    PP.zip_folder(target, os.path.join(task_dir, "target.zip"), zone=ZONE)
    PP.zip_folder(golden, os.path.join(task_dir, "golden.zip"), zone=ZONE)
    return A, F, E, counts, time.time() - t0


def main():
    if "--out" in sys.argv:
        out = os.path.abspath(sys.argv[sys.argv.index("--out") + 1])
        A, F, E, counts, secs = build(out, os.path.join(out, "generator"), cache=False)
    else:
        A, F, E, counts, secs = build(TASK, HERE)
    import checks as CK
    print("nominate %s; first left out %s, %.1f behind; shortfall %.1f = %.1f + %.1f + %.1f, left %.1f; back-test %.1f "
          "(index %.1f); %d checks passed; %.0fs"
          % (F["nominate"], F["first_left_out"], F["cut_points"], F["shortfall_points"],
             F["overstated_at_own_sites_points"], F["benchmark_water_response_points"], F["lodging_points"],
             F["left_over_points"], F["backtest_rmse_points"], F["index_rmse_points"], len(CK.RESULTS), secs))


if __name__ == "__main__":
    main()
