"""Build target/: the data files written from the core's world (pack.py), the documents and small files (docs.py),
the workbooks passed through the house writer, and every file given its own save time."""
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
import world as WL  # noqa: E402

UTC = dt.timezone.utc
F = WL.FILES
P = WL.PEOPLE


def at(mo, d, hh, mm, ss, year=2026):
    return dt.datetime(year, mo, d, hh, mm, ss, tzinfo=UTC)


# when each system wrote its extract for the reliability review (the records as extracted on 12 October 2026)
EXPORTED = {
    F["sessions"]: at(10, 12, 6, 41, 17),
    F["mart"]: at(10, 12, 5, 12, 3),
    F["status"]: at(10, 12, 7, 2, 55),
    F["gaps"]: at(10, 12, 8, 26, 39),
    F["batches"]: at(10, 12, 8, 50, 8),
    F["lags"]: at(10, 12, 9, 17, 44),
    F["scoring"]: at(10, 12, 10, 3, 21),
    F["seller_traffic"]: at(10, 12, 10, 11, 52),
    F["experiments"]: at(10, 12, 11, 34, 6),
    F["cache"]: at(10, 12, 6, 48, 30),
    F["render"]: at(10, 12, 7, 25, 13),
    F["registry"]: at(9, 1, 13, 20, 47),
    F["pipeline"]: at(9, 28, 14, 6, 19),
    F["store"]: at(8, 31, 9, 55, 2),
    F["markets"]: at(3, 4, 10, 15, 36),
    F["regions"]: at(3, 4, 10, 18, 9),
    F["promo"]: at(10, 2, 15, 42, 28),
    F["importance"]: at(9, 9, 16, 30, 51),
    F["releases"]: at(9, 9, 16, 44, 12),
}
OFFICE = [
    (F["shares"], P["analyst"], P["analyst"], "2026-02-03T10:12:00Z", "2026-10-12T12:07:41Z"),
    (F["incidents"], P["sre"], P["sre"], "2026-01-05T08:31:00Z", "2026-10-09T15:22:10Z"),
    (F["replay"], P["mlops"], P["mlops"], "2026-10-02T09:40:00Z", "2026-10-06T11:18:27Z"),
]


def build(target, W=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = W if W is not None else C.make_world()
    counts = pack.build(W, target)
    counts[F["incidents"]] = docs.write_all(W, target)
    for name, creator, last, created, modified in OFFICE:
        postprocess.normalize_ooxml(os.path.join(target, name), creator, last, created, modified, excel=True,
                                    company=WL.ORG)
    postprocess.own_mtimes(target, EXPORTED)
    return dict(counts=counts, W=W)


if __name__ == "__main__":
    o = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(o)
    for name in sorted(os.listdir(o)):
        print("%10d  %8s  %s" % (os.path.getsize(os.path.join(o, name)), r["counts"].get(name, ""), name))
