"""Build the pack under target/: the clean truth (sim.py), the data files (pack.py), the standard and the quotation
(docs.py), every office container laid out as Office saves it and scrubbed of the library that wrote it."""
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


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.world()
    n = pack.write_tables(w, target)
    docs.standard(F["standard"])
    docs.quotation(F["quote"])
    for k, (created, modified, who) in OFFICE.items():
        postprocess.scrub(F[k], P.ORG, modified[:10])
        postprocess.finish_office(F[k], created, modified, P.ORG)
    return w, n
