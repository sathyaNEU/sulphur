"""Build the pack under target/: the world (sim.py), the data files (pack.py), the ARR reporting policy (docs.py),
every office container laid out as Office saves it and scrubbed of the library that wrote it, each file's time its
own last save.

    python3 build.py [--out <folder>]
"""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import docs
import pack
import params as P
import postprocess
import sim

FILES = pack.FILES
PACK = list(FILES)
DISTRACTORS = pack.DISTRACTORS
ORG = "Tekenbord B.V."
OFFICE = {"crm": ("2026-11-02T07:12:00Z", "2026-11-02T07:12:00Z", "Floortje Huisman"),
          "price": ("2025-12-03T10:31:00Z", "2026-01-14T15:06:00Z", "Naomi Weijters"),
          "kpi": ("2026-01-08T08:45:00Z", "2026-10-06T09:27:00Z", "Niels Thout")}
CET = dt.timezone(dt.timedelta(hours=1))
# the exports carry no stamp of their own: each file's time is when its system wrote it
EXPORTED = {"lines": dt.datetime(2026, 11, 3, 2, 14, 37, tzinfo=CET),
            "team": dt.datetime(2026, 11, 3, 2, 31, 8, tzinfo=CET),
            "activity": dt.datetime(2026, 11, 2, 4, 5, 51, tzinfo=CET),
            "links": dt.datetime(2026, 11, 2, 4, 6, 19, tzinfo=CET),
            "snap": dt.datetime(2026, 11, 2, 7, 44, 2, tzinfo=CET),
            "closed": dt.datetime(2026, 11, 2, 7, 46, 40, tzinfo=CET),
            "tickets": dt.datetime(2026, 11, 3, 8, 58, 13, tzinfo=CET),
            "nps": dt.datetime(2026, 10, 7, 16, 20, 45, tzinfo=CET)}


def run(target):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.build_history()
    n = pack.write_tables(w, target)
    docs.policy(F["policy"])
    for k, (created, modified, who) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, created, modified, excel=True, company=ORG)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return w, n


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE),
                                                                                          "target")
    run(out)
