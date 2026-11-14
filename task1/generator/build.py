"""Build target/: simulate Zancada's world, write the exports, the documents and the plan, stamp every file with its
own save time."""
import datetime as dt
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import world  # noqa: E402

UTC = dt.timezone.utc
CET = dt.timezone(dt.timedelta(hours=1))
EXPORTED = {pack.FILES["acc"]: dt.datetime(2026, 11, 9, 3, 12, 41, tzinfo=UTC),
            pack.FILES["bill"]: dt.datetime(2026, 11, 9, 3, 26, 5, tzinfo=UTC),
            pack.FILES["attr"]: dt.datetime(2026, 11, 9, 6, 1, 37, tzinfo=UTC),
            pack.FILES["skan"]: dt.datetime(2026, 11, 9, 6, 14, 52, tzinfo=UTC),
            pack.FILES["apple"]: dt.datetime(2026, 11, 9, 8, 47, 20, tzinfo=CET),
            pack.FILES["google"]: dt.datetime(2026, 11, 9, 8, 55, 3, tzinfo=CET),
            pack.FILES["spend"]: dt.datetime(2026, 11, 9, 7, 30, 11, tzinfo=UTC),
            pack.FILES["creat"]: dt.datetime(2026, 11, 2, 12, 18, 40, tzinfo=CET),
            pack.FILES["rate"]: dt.datetime(2026, 11, 1, 9, 3, 26, tzinfo=CET),
            }


def build(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = world.simulate()
    rng = np.random.default_rng(P.SEED + 5)
    counts, frame = pack.build(W, target, rng)
    docs.write_all(target)
    postprocess.normalize_ooxml(os.path.join(target, docs.FILES["plan"]), "Rafa Naranjo", "Rafa Naranjo",
                                "2026-10-21T08:40:00Z", "2026-10-30T16:12:44Z", excel=True, company=P.ORG)
    postprocess.own_mtimes(target, EXPORTED)
    return {"W": W, "counts": counts, "frame": frame}


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(out)
    print(r["counts"])
