"""Build target/: lay the records over the core's arrays (world.py), write each board's exports, the registers, the
review marks and the unused files (pack.py) and the documents (docs.py), and give every file its own save time."""
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

UTC = dt.timezone.utc
F = pack.FILES
# when each board's systems wrote its exports for Carrow (the protocol asks for them by 5 February 2027)
SENT = {"Carrow": (2027, 1, 25, 9, 12, 40), "Ardkeel": (2027, 1, 28, 14, 3, 11), "Brannock": (2027, 2, 2, 16, 47, 5),
        "Dunmoyle": (2027, 1, 29, 10, 31, 52), "Eskerry": (2027, 2, 4, 11, 20, 18), "Fennor": (2027, 2, 5, 15, 58, 33),
        "Gortavale": (2027, 2, 3, 9, 6, 27)}
STEP = {"marks": 0, "samples": 97, "outcomes": 151, "scripts": 208, "trial": 263}
EXPORTED = {
    F["register"]: dt.datetime(2027, 1, 21, 8, 30, 14, tzinfo=UTC),
    F["centres"]: dt.datetime(2027, 1, 21, 8, 31, 2, tzinfo=UTC),
    F["review"]: dt.datetime(2023, 11, 28, 13, 44, 9, tzinfo=UTC),
    F["enquiries"]: dt.datetime(2027, 1, 22, 10, 15, 37, tzinfo=UTC),
    F["entries"]: dt.datetime(2026, 9, 30, 12, 2, 48, tzinfo=UTC),
}
OFFICE = [
    (F["Eskerry_outcomes"], "Michelle Slattery", "Michelle Slattery", "2019-07-02T09:14:00Z", "2027-02-04T11:23:47Z", "Eskerry Examining Board"),
    (F["Eskerry_scripts"], "Cody Lavan", "Michelle Slattery", "2015-02-11T10:40:00Z", "2027-02-04T11:26:12Z", "Eskerry Examining Board"),
    (F["Gortavale_outcomes"], "Conchur Gillespie", "Carl MacDwyer", "2016-07-08T08:51:00Z", "2027-02-03T09:09:30Z", "Gortavale Examining Board"),
    (F["Gortavale_scripts"], "Conchur Gillespie", "Conchur Gillespie", "2015-03-04T14:05:00Z", "2027-02-03T09:11:56Z", "Gortavale Examining Board"),
    (F["visits"], "Patrick Pender", "Elizabeth Reynolds", "2022-01-12T09:02:00Z", "2026-12-18T15:37:21Z", WL.REGULATOR),
]
for _b, _t in SENT.items():
    for _k, _s in STEP.items():
        _n = F.get("%s_%s" % (_b, _k))
        if _n and not _n.endswith(".xlsx"):
            EXPORTED[_n] = dt.datetime(*_t, tzinfo=UTC) + dt.timedelta(seconds=_s + 7 * len(_b))


def build(target, WD=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    WD = WD or WL.build()
    counts = pack.build(WD, target)
    docs.write_all(target)
    for name, creator, last, created, modified, company in OFFICE:
        postprocess.normalize_ooxml(os.path.join(target, name), creator, last, created, modified, excel=True,
                                    company=company)
    postprocess.own_mtimes(target, EXPORTED)
    return dict(counts=counts, WD=WD)


if __name__ == "__main__":
    o = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(o)
    for name in sorted(os.listdir(o)):
        print("%10d  %8s  %s" % (os.path.getsize(os.path.join(o, name)), r["counts"].get(name, ""), name))
