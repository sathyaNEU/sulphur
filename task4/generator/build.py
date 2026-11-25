"""Build target/: lay the world out on the calendar (world.py), write the systems' exports (pack.py) and the
documents (docs.py), and give every file its own save time."""
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
import docs  # noqa: E402
import pack  # noqa: E402
import world as WL  # noqa: E402

GMT = dt.timezone.utc
F = pack.FILES
EXPORTED = {
    F["dockets"]: dt.datetime(2026, 12, 1, 7, 42, 18, tzinfo=GMT),
    F["register"]: dt.datetime(2026, 12, 1, 9, 14, 3, tzinfo=GMT),
    F["store"]: dt.datetime(2026, 11, 30, 6, 31, 44, tzinfo=GMT),
    F["racking"]: dt.datetime(2026, 12, 1, 10, 27, 9, tzinfo=GMT),
    F["checks"]: dt.datetime(2026, 12, 2, 11, 48, 36, tzinfo=GMT),
    F["accounts"]: dt.datetime(2026, 12, 1, 14, 2, 27, tzinfo=GMT),
    F["lines"]: dt.datetime(2026, 12, 1, 14, 6, 55, tzinfo=GMT),
    F["products"]: dt.datetime(2026, 11, 13, 16, 20, 12, tzinfo=GMT),
    F["codes"]: dt.datetime(2024, 9, 17, 11, 3, 40, tzinfo=GMT),
    F["weather"]: dt.datetime(2026, 11, 30, 8, 15, 6, tzinfo=GMT),
    F["depots"]: dt.datetime(2026, 11, 30, 7, 58, 23, tzinfo=GMT),
    F["wash"]: dt.datetime(2026, 12, 1, 6, 49, 31, tzinfo=GMT),
    F["purchases"]: dt.datetime(2026, 12, 1, 9, 36, 47, tzinfo=GMT),
    F["packaging"]: dt.datetime(2026, 12, 1, 15, 33, 58, tzinfo=GMT),
}
OFFICE = [
    (pack.FILES["count"], WL.PEOPLE["fleet"], WL.PEOPLE["fleet"], "2026-11-23T15:42:00Z", "2026-11-30T17:21:38Z"),
    (docs.FILES["plan"], WL.PEOPLE["brewer"], WL.PEOPLE["brewer"], "2026-10-19T09:30:00Z", "2026-11-12T14:46:09Z"),
    (docs.FILES["schedule"], WL.PEOPLE["sales"], WL.PEOPLE["sales"], "2026-09-28T10:12:00Z", "2026-10-23T11:02:45Z"),
    (docs.FILES["routes"], WL.PEOPLE["depot"], WL.PEOPLE["depot"], "2026-08-24T08:40:00Z", "2026-09-07T12:18:20Z"),
    (docs.FILES["prices"], WL.PEOPLE["sales"], WL.PEOPLE["sales"], "2026-02-09T13:25:00Z", "2026-02-23T15:54:02Z"),
]


def build(target, WD=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    WD = WD or WL.build()
    counts, TX = pack.build(WD, target)
    docs.write_all(target, WD)
    for name, creator, last, created, modified in OFFICE:
        postprocess.normalize_ooxml(os.path.join(target, name), creator, last, created, modified, excel=True,
                                    company=WL.ORG)
    postprocess.own_mtimes(target, EXPORTED)
    return dict(counts=counts, TX=TX, WD=WD)


if __name__ == "__main__":
    o = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(o)
    print(r["counts"])
    for name in sorted(os.listdir(o)):
        print("%10d  %s" % (os.path.getsize(os.path.join(o, name)), name))
