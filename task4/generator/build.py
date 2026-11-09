"""Build the pack under target/: the clean truth (sim.py), the data files (pack.py), the standard and the quotation
(docs.py), every office container laid out as Office saves it and scrubbed of the library that wrote it."""
import datetime as dt
import os

import docs
import pack
import params as P
import postprocess
import sim

FILES = pack.FILES
PACK = list(FILES)
DISTRACTORS = pack.DISTRACTORS
OFFICE = {"routes": ("2022-03-14T08:10:00Z", "2026-10-12T13:41:00Z", "Inger Norman"),
          "fleet": ("2021-01-11T09:30:00Z", "2026-09-28T07:55:00Z", "Georg Pålsson"),
          "shippers": ("2020-08-24T12:02:00Z", "2026-08-31T10:18:00Z", "Ekonomi"),
          "plan": ("2026-10-05T09:44:00Z", "2026-10-21T15:12:00Z", "Inger Norman")}
SE = dt.timezone(dt.timedelta(hours=1))
# the exports carry no stamp of their own: each file's time is when its system wrote it
EXPORTED = {"weighbridge": dt.datetime(2026, 11, 2, 6, 14, 22, tzinfo=SE),
            "bev": dt.datetime(2026, 11, 2, 7, 3, 51, tzinfo=SE),
            "tms": dt.datetime(2026, 11, 3, 13, 26, 9, tzinfo=SE),
            "temps": dt.datetime(2026, 11, 2, 9, 40, 37, tzinfo=SE),
            "fuel": dt.datetime(2026, 11, 4, 11, 2, 15, tzinfo=SE),
            "workshop": dt.datetime(2026, 11, 4, 14, 48, 3, tzinfo=SE)}


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.world()
    n = pack.write_tables(w, target)
    docs.standard(F["standard"])
    docs.quotation(F["quote"])
    for k, (created, modified, who) in OFFICE.items():
        postprocess.normalize_ooxml(F[k], who, who, created, modified, excel=True, company=P.ORG)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return w, n
