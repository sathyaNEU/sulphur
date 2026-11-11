"""Build the pack under target/: the world (world.py), the exports (pack.py), the distractors, the documents and
the Brightway workbook through the house writers, and each file's time its own system's export or last save.

    python3 build.py [--out <folder>]
"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

sys.path.insert(0, HERE)
import distractors as DI  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import world  # noqa: E402

FILES = pack.FILES
DISTRACTORS = pack.DISTRACTORS
BST = dt.timezone(dt.timedelta(hours=1))
EXPORTED = {"census": dt.datetime(2026, 10, 2, 7, 41, 9, tzinfo=BST),
            "ks2": dt.datetime(2026, 9, 18, 13, 2, 55, tzinfo=BST),
            "lexis": dt.datetime(2026, 10, 5, 16, 27, 31, tzinfo=BST),
            "quill": dt.datetime(2026, 10, 12, 9, 14, 3, tzinfo=BST),
            "quillmap": dt.datetime(2026, 10, 12, 9, 15, 47, tzinfo=BST),
            "quilllog": dt.datetime(2026, 10, 12, 9, 22, 18, tzinfo=BST),
            "academies": dt.datetime(2026, 9, 1, 10, 33, 40, tzinfo=BST),
            "cpt": dt.datetime(2026, 10, 7, 11, 48, 12, tzinfo=BST),
            "attendance": dt.datetime(2026, 10, 12, 6, 30, 1, tzinfo=BST),
            "survey": dt.datetime(2026, 10, 1, 17, 5, 44, tzinfo=BST),
            "tutorlog": dt.datetime(2026, 7, 21, 14, 19, 26, tzinfo=BST)}


def run(target):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    W = world.build()
    pk, n = pack.write_all(W, target)
    import numpy as np
    rng = np.random.default_rng(P.SEED + 202)
    for key, fn in [("cpt", DI.cognitive), ("attendance", DI.attendance), ("survey", DI.survey),
                    ("tutorlog", DI.sessions)]:
        head, rows = fn(W, rng)
        n[key] = pack.write_csv(F[key], head, rows)
    docs.policy(F["policy"])
    for t, k in [("LEXIS", "lexis_tech"), ("QUILL", "quill_tech"), ("BRIGHTWAY", "brightway_tech")]:
        docs.technical(F[k], t)
    docs.brightway_workbook(F["brightway"], n.pop("brightway_sheets"))
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return W, pk, n


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    W, pk, n = run(out)
    print({k: v for k, v in n.items()})
