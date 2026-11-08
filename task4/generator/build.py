"""Build the pack under target/: the clean truth (sim.py), the data files (pack.py), the offer and the standard
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
OFFICE = {"register": ("2023-01-09T09:12:00Z", "2026-10-12T08:44:00Z", "Aislinn Duffin"),
          "plan": ("2026-10-14T10:05:00Z", "2026-10-19T15:31:00Z", "Commercial Planning"),
          "rates": ("2026-09-22T11:20:00Z", "2026-09-30T16:02:00Z", "Finance"),
          "fleet": ("2024-06-03T08:30:00Z", "2026-07-14T12:10:00Z", "Aislinn Duffin")}


def run(target):
    os.makedirs(target, exist_ok=True)
    F = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.world()
    n = pack.write_tables(w, target)
    docs.offer(F["offer"])
    docs.standard(F["standard"])
    for k, (created, modified, who) in OFFICE.items():
        postprocess.scrub(F[k], P.ORG, modified[:10])
        postprocess.finish_office(F[k], created, modified, P.ORG)
    return w, n
