"""Build target/: lay the records over the core's yearly arrays (world.py), write the systems' exports and tables
(pack.py) and the documents (docs.py), and give every file its own save time."""
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
EXPORTED = {
    F["register"]: dt.datetime(2027, 2, 19, 13, 22, 7, tzinfo=UTC),
    F["tables"]: dt.datetime(2027, 2, 3, 8, 41, 15, tzinfo=UTC),
    F["vital"]: dt.datetime(2027, 2, 3, 8, 44, 52, tzinfo=UTC),
    F["codes"]: dt.datetime(2019, 3, 12, 10, 5, 31, tzinfo=UTC),
    F["muni"]: dt.datetime(2025, 1, 8, 9, 17, 44, tzinfo=UTC),
    F["pop"]: dt.datetime(2026, 7, 2, 12, 30, 9, tzinfo=UTC),
    F["traffic"]: dt.datetime(2027, 1, 29, 7, 56, 38, tzinfo=UTC),
}
OFFICE = [
    (F["census"], "Kerstin Bürger", "Viktoria Schöberl", "2022-11-14T09:12:00Z", "2023-03-21T14:36:27Z", WL.HUB),
    (F["c14"], WL.PEOPLE["census"], WL.PEOPLE["census"], "2022-06-08T07:45:00Z", "2022-06-30T12:08:51Z", WL.ORG),
    (F["count16"], "Mogens Iversen", "Gerda Carlsen", "2017-04-19T08:20:00Z", "2017-05-02T10:44:16Z", "Statistics Fenmark"),
    (F["estab"], WL.PEOPLE["secretary"], WL.PEOPLE["secretary"], "2023-06-14T08:03:00Z", "2027-01-11T09:51:40Z",
     "Ministry of Foreign Affairs"),
]


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
    print(r["counts"])
    for name in sorted(os.listdir(o)):
        print("%10d  %s" % (os.path.getsize(os.path.join(o, name)), name))
