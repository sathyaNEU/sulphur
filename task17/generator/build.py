"""Build the pack under target/: the world (sim.py), the clean tables (tables.py), the data files (pack.py), the
policy, the plan and the configuration history (docs.py), every office container laid out as Office saves it and
scrubbed of the library that wrote it, each file's time its own last save.

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
import tables as T

FILES = pack.FILES
PACK = list(FILES)
DISTRACTORS = pack.DISTRACTORS
OFFICE = {"alloc": ("2023-11-22T09:14:00Z", "2026-11-09T15:37:00Z", "Carolin Hofig", "Allocation committee"),
          "maint": ("2023-12-04T13:02:00Z", "2026-11-03T08:21:00Z", "Tobias Koehl", "HPC systems group"),
          "report": ("2024-01-15T10:40:00Z", "2026-11-16T07:52:00Z", "Mehdi Renner", "HPC systems group")}
CET = dt.timezone(dt.timedelta(hours=1))
# the exports carry no stamp of their own: each file's time is when its system wrote it
EXPORTED = {"sacct": dt.datetime(2026, 11, 16, 6, 10, 42, tzinfo=CET),
            "events": dt.datetime(2026, 11, 16, 6, 14, 5, tzinfo=CET),
            "rack": dt.datetime(2026, 11, 16, 6, 15, 31, tzinfo=CET),
            "users": dt.datetime(2026, 11, 16, 6, 18, 9, tzinfo=CET),
            "config": dt.datetime(2026, 11, 12, 16, 48, 27, tzinfo=CET),
            "storage": dt.datetime(2026, 11, 16, 5, 2, 18, tzinfo=CET),
            "tickets": dt.datetime(2026, 11, 16, 8, 31, 54, tzinfo=CET)}


def run(target):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.world()
    pk = T.from_world(w)
    n = pack.write_tables(pk, w, target)
    docs.config_history(F["config"], [sim.local(t) for t in pk.restarts_h])
    docs.policy(F["policy"])
    docs.plan(F["plan"])
    for k, (created, modified, who, company) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, created, modified, excel=True, company=P.ORG)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return w, pk, n


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    run(out)
