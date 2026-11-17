"""Build target/: lay the world out on the calendar (world.py), write the instruments' exports (pack.py) and the
Service's documents (docs.py), and give every file its own save time."""
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
CET = dt.timezone(dt.timedelta(hours=1))
F = pack.FILES
EXPORTED = {
    F["tips"] % "VFO": dt.datetime(2026, 11, 5, 9, 18, 42, tzinfo=CET),
    F["tips"] % "PRD": dt.datetime(2026, 11, 5, 10, 31, 7, tzinfo=CET),
    F["tips"] % "RSC": dt.datetime(2026, 11, 5, 11, 22, 55, tzinfo=CET),
    F["tips"] % "MSO": dt.datetime(2026, 11, 5, 12, 14, 30, tzinfo=CET),
    F["tips"] % "FRC": dt.datetime(2026, 11, 6, 9, 47, 13, tzinfo=CET),
    F["tips"] % "CSR": dt.datetime(2026, 11, 6, 11, 5, 49, tzinfo=CET),
    F["visits"]: dt.datetime(2026, 11, 9, 8, 52, 16, tzinfo=CET),
    F["pw"]: dt.datetime(2026, 11, 9, 14, 3, 28, tzinfo=CET),
    F["wx"]: dt.datetime(2019, 3, 12, 10, 40, 5, tzinfo=CET),
    F["radar"]: dt.datetime(2026, 11, 10, 7, 15, 44, tzinfo=UTC),
    F["pixels"]: dt.datetime(2019, 2, 27, 13, 8, 20, tzinfo=UTC),
    F["normal"]: dt.datetime(2022, 6, 14, 9, 30, 2, tzinfo=UTC),
    F["rs_events"]: dt.datetime(2026, 11, 11, 16, 26, 39, tzinfo=CET),
    F["rs_gauges"]: dt.datetime(2026, 11, 11, 16, 27, 12, tzinfo=CET),
    F["daily"]: dt.datetime(2026, 11, 3, 8, 12, 57, tzinfo=CET),
    F["traffic"]: dt.datetime(2026, 11, 2, 6, 0, 11, tzinfo=CET),
}


def build(target, WD=None):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    WD = WD or WL.build()
    counts, TX = pack.build(WD, target)
    docs.write_all(target)
    postprocess.normalize_ooxml(os.path.join(target, docs.FILES["stations"]), "Luca Comboni", "Alfio Cundari",
                                "2015-03-04T09:12:00Z", "2026-04-20T07:48:31Z", excel=True, company=docs.ORG)
    postprocess.normalize_ooxml(os.path.join(target, docs.FILES["crossings"]), "Biagio Borroni", "Biagio Borroni",
                                "2016-05-17T08:41:00Z", "2025-10-08T15:21:09Z", excel=True, company=docs.ORG)
    postprocess.own_mtimes(target, EXPORTED)
    return dict(counts=counts, TX=TX, WD=WD)


if __name__ == "__main__":
    o = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(o)
    print(r["counts"])
