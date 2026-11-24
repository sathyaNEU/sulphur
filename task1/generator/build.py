"""Build target/: simulate Zancada's world (core.py), write the systems' exports and the organisation's documents,
and give every file its own save time."""
import os  # noqa: E402
# numpy runs on Apple's Accelerate here, whose threads do not survive a fork: one thread, set before numpy loads
for _v in ("VECLIB_MAXIMUM_THREADS", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import datetime as dt
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402
import core as C  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402

UTC = dt.timezone.utc
CET = dt.timezone(dt.timedelta(hours=1))
EXPORTED = {pack.FILES["acc"]: dt.datetime(2026, 11, 9, 3, 12, 41, tzinfo=UTC),
            pack.FILES["bill"]: dt.datetime(2026, 11, 9, 3, 26, 5, tzinfo=UTC),
            pack.FILES["attr"]: dt.datetime(2026, 11, 9, 6, 1, 37, tzinfo=UTC),
            pack.FILES["skan"]: dt.datetime(2026, 11, 9, 6, 14, 52, tzinfo=UTC),
            pack.FILES["apple"]: dt.datetime(2026, 11, 9, 8, 47, 20, tzinfo=CET),
            pack.FILES["google"]: dt.datetime(2026, 11, 9, 8, 55, 3, tzinfo=CET),
            pack.FILES["web"]: dt.datetime(2026, 11, 9, 9, 6, 48, tzinfo=CET),
            pack.FILES["spend"]: dt.datetime(2026, 11, 9, 7, 30, 11, tzinfo=UTC),
            pack.FILES["creat"]: dt.datetime(2026, 11, 2, 12, 18, 40, tzinfo=CET),
            pack.FILES["rate"]: dt.datetime(2026, 11, 1, 9, 3, 26, tzinfo=CET),
            docs.FILES["schema"]: dt.datetime(2024, 10, 24, 15, 37, 9, tzinfo=dt.timezone(dt.timedelta(hours=2))),
            }


def build(target, W=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = W or C.simulate()
    out = pack.build(W, target)
    out["changes"] = docs.write_all(target, W)
    # the growth analyst opened the 2027 plan for the head of growth, whose policy it is placed under; the paid
    # acquisition manager keeps both workbooks from there (three documents, three authors)
    postprocess.normalize_ooxml(os.path.join(target, docs.FILES["plan"]), "Ester Rey", "Rafa Naranjo",
                                "2026-10-21T08:40:00Z", "2026-10-30T16:12:44Z", excel=True, company=docs.ORG)
    postprocess.normalize_ooxml(os.path.join(target, docs.FILES["budget"]), "Rafa Naranjo", "Rafa Naranjo",
                                "2024-10-29T10:05:00Z", "2026-11-02T09:41:17Z", excel=True, company=docs.ORG)
    postprocess.own_mtimes(target, EXPORTED)
    out["W"] = W
    return out


if __name__ == "__main__":
    o = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(o)
    print(r["counts"], "log rows", r["changes"])
