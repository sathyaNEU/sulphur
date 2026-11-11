"""Build the pack under target/: the record (world.py), the exports (pack.py), the neighbouring files
(distractors.py), the four documents (docs.py), every office container through the house writers with its owner's
stamps, and each file's time its own last save or its system's export time.

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
import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402
import world  # noqa: E402

FILES = pack.FILES
DISTRACTORS = pack.DISTRACTORS
CET = dt.timezone(dt.timedelta(hours=1))
EXPORTED = {"subs": dt.datetime(2026, 11, 3, 2, 12, 41, tzinfo=CET),
            "periods": dt.datetime(2026, 11, 3, 2, 19, 7, tzinfo=CET),
            "exceptions": dt.datetime(2026, 11, 3, 2, 21, 55, tzinfo=CET),
            "customers": dt.datetime(2026, 11, 3, 2, 24, 30, tzinfo=CET),
            "methods": dt.datetime(2026, 11, 3, 2, 26, 3, tzinfo=CET),
            "reading": dt.datetime(2026, 11, 2, 5, 40, 18, tzinfo=CET),
            "logins": dt.datetime(2026, 11, 2, 5, 41, 52, tzinfo=CET),
            "spend": dt.datetime(2026, 11, 4, 9, 7, 26, tzinfo=CET),
            "codes": dt.datetime(2026, 11, 4, 9, 9, 3, tzinfo=CET),
            "offers": dt.datetime(2026, 10, 12, 14, 33, 9, tzinfo=dt.timezone(dt.timedelta(hours=2))),
            "print": dt.datetime(2026, 10, 21, 10, 15, 44, tzinfo=dt.timezone(dt.timedelta(hours=2))),
            "newsletter": dt.datetime(2026, 11, 2, 7, 58, 31, tzinfo=CET),
            "survey": dt.datetime(2026, 7, 14, 16, 3, 12, tzinfo=dt.timezone(dt.timedelta(hours=2))),
            "ads": dt.datetime(2026, 11, 3, 8, 46, 20, tzinfo=CET)}
OFFICE = {"plan": ("2026-09-02T08:11:00Z", "2026-10-28T15:47:00Z", "Jost Reising"),
          "kpi": ("2026-01-12T07:55:00Z", "2026-10-08T06:31:00Z", "Rosa-Maria Herrmann")}


def kpi_rows(S):
    import models
    net = sim.store_net(S["gross"], S["route"], lead=S["tenure0"])
    rows = []
    for m in range(36, 45):
        y, mo = sim.ym(m)
        pay = S["gross"][:, m] > 0
        cnt = [int((pay & (S["title"] == sim.T_IDX[t])).sum()) for t in P.TITLES]
        rev = [round(float(net[S["title"] == sim.T_IDX[t], m].sum()), 2) for t in P.TITLES]
        rows.append(["%04d-%02d" % (y, mo)] + cnt + rev)
    return rows


def run(target):
    os.makedirs(target, exist_ok=True)
    for f in os.listdir(target):
        os.remove(os.path.join(target, f))
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    S = world.history()
    pk, n = pack.write_all(S, target)
    plan = world.plan_2027()
    docs.standard(F["standard"])
    docs.price_list(F["prices"])
    docs.media_plan(F["plan"], plan)
    docs.kpi(F["kpi"], kpi_rows(S))
    for k, (created, modified, who) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, created, modified, excel=True, company=docs.ORG)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return S, pk, n, plan


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE),
                                                                                          "target")
    S, pk, n, plan = run(out)
    print({k: v for k, v in n.items()})
