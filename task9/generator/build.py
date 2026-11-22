"""Build target/: simulate Garrane Risk's world (core.py), write the systems' exports and the organisation's
workbooks and documents, and give every file its own save time.

    python3 task9/generator/build.py [--out <folder>]
"""
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(HERE, "..", "..", ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402
import core as C  # noqa: E402
import docs  # noqa: E402
import pack as P  # noqa: E402

UTC = dt.timezone.utc


def stamps():
    """Each export's own write time (the systems ran their extracts in the week of 23 November 2026)."""
    out = {}
    for i, q in enumerate(("2024q3", "2024q4", "2025q1", "2025q2", "2025q3", "2025q4", "2026q1", "2026q2", "2026q3",
                           "2026q4")):
        out[P.FILES["panel"] % q] = dt.datetime(2026, 11, 24, 2, 11 + 3 * i, 7 + 5 * i, tzinfo=UTC)
    for name, s in (("roster", (24, 2, 58, 41)), ("xwalk", (2, 9, 14, 30)), ("book", (24, 3, 6, 12)),
                    ("runs", (24, 4, 40, 55)), ("rows", (24, 5, 2, 18)), ("pairs", (25, 9, 47, 26)),
                    ("preg", (25, 9, 31, 3)), ("registry", (23, 18, 5, 44)), ("releases", (24, 7, 15, 9)),
                    ("retunes", (24, 4, 52, 37)), ("monitor", (6, 8, 30, 2)), ("perf", (24, 6, 0, 49)),
                    ("drift", (24, 6, 13, 20)), ("compute", (24, 5, 26, 51))):
        d, h, m, sec = s
        month = 10 if name == "monitor" else 11
        if name == "xwalk":
            out[P.FILES[name]] = dt.datetime(2025, 8, 21, 16, 44, 12, tzinfo=UTC)
            continue
        out[P.FILES[name]] = dt.datetime(2026, month, d, h, m, sec, tzinfo=UTC)
    return out


def build(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    keep = {}
    w, z, inst = C.world(keep)
    ids = P.Ids(w)
    counts = {}
    Z, c = P.panel(w, z, keep, ids, target)
    counts.update(c)
    counts[P.FILES["book"]] = P.book(w, target)
    prod, inst_runs, cfg, counts[P.FILES["runs"]] = P.manifests(w, keep, ids, target)
    counts[P.FILES["pairs"]], counts[P.FILES["preg"]] = P.pairs(w, z, keep, ids, inst_runs, target)
    counts[P.FILES["rows"]] = P.warehouse(w, target)
    counts[P.FILES["registry"]] = P.registry(w, ids, target)
    counts[P.FILES["releases"]] = len(P.release_log(w, target))
    counts[P.FILES["retunes"]] = P.retune_log(w, cfg, target)
    counts[P.FILES["monitor"]] = P.monitor(w, Z, ids, target)
    counts[P.FILES["perf"]], counts[P.FILES["drift"]], counts[P.FILES["compute"]] = P.distractors(w, prod, target)
    docs.write_all(w, target)
    postprocess.own_mtimes(target, stamps())
    return {"w": w, "z": z, "inst": inst, "keep": keep, "ids": ids, "counts": counts}


if __name__ == "__main__":
    o = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(o)
    print(r["counts"])
