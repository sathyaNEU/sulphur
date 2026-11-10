"""Build the pack under target/: the clean truth (sim.py), the data files (pack.py), the three documents (docs.py),
every office container laid out as Office saves it and scrubbed of the library that wrote it (the house writers)."""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402

FILES = pack.FILES
PACK = list(FILES)
DISTRACTORS = pack.DISTRACTORS
OFFICE = {"blocks": ("2021-09-06T07:40:00Z", "2026-08-24T11:17:00Z", "Simo Virta"),
          "vehicles": ("2019-02-11T12:05:00Z", "2026-10-02T08:33:00Z", "Eveliina Pajunen"),
          "plan": ("2026-09-14T09:21:00Z", "2026-10-27T15:48:00Z", "Simo Virta"),
          "tyres": ("2026-01-19T13:02:00Z", "2026-02-03T10:14:00Z", "Eveliina Pajunen")}
FI = dt.timezone(dt.timedelta(hours=2))
EXPORTED = {"fuel": dt.datetime(2026, 11, 3, 9, 41, 12, tzinfo=FI),
            "dispatch": dt.datetime(2026, 11, 2, 14, 7, 55, tzinfo=FI),
            "ebus": dt.datetime(2026, 11, 2, 7, 22, 31, tzinfo=FI),
            "sessions": dt.datetime(2026, 11, 2, 7, 26, 4, tzinfo=FI),
            "weather": dt.datetime(2026, 11, 3, 11, 58, 40, tzinfo=FI),
            "workshop": dt.datetime(2026, 11, 4, 15, 36, 9, tzinfo=FI),
            "power": dt.datetime(2026, 11, 4, 16, 2, 47, tzinfo=FI)}


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.world()
    n = pack.write_tables(w, target)
    docs.standard(F["standard"])
    docs.agreement(F["agreement"])
    docs.quotation(F["quote"])
    for k, (created, modified, who) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, created, modified, excel=True, company=P.ORG)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return w, n


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    w, n = run(t)
    print(n)
