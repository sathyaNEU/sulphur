"""Build the pack under target/: the clean truth (sim.py), the data files (pack.py), the documents (docs.py), every
office container laid out as Office saves it (the house writers), each file's own save time."""
import datetime as dt
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

import analysis as A  # noqa: E402
import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import sim  # noqa: E402

FILES = pack.FILES
PACK = list(FILES)
DISTRACTORS = pack.DISTRACTORS
CET = dt.timezone(dt.timedelta(hours=1))
OFFICE = {"vendor": ("2026-11-27T13:02:00Z", "2026-12-01T15:47:00Z", "Erik Aasen", P.ORG),
          "register": ("2026-11-30T09:12:00Z", "2026-12-01T07:58:00Z", P.PEOPLE["stores"], P.ORG),
          "pool": ("2026-11-30T21:04:00Z", "2026-11-30T21:04:00Z", P.PEOPLE["stores"], P.ORG),
          "programme": ("2026-10-14T11:36:00Z", "2026-11-18T08:21:00Z", "Irene Brekke", P.ORG),
          "shopplan": ("2026-11-04T12:20:00Z", "2026-11-19T10:06:00Z", P.PEOPLE["shop"], P.ORG)}
EXPORTED = {"legs": dt.datetime(2026, 12, 1, 6, 41, 18, tzinfo=CET),
            "changes": dt.datetime(2026, 12, 1, 7, 3, 55, tzinfo=CET),
            "shop": dt.datetime(2026, 12, 1, 7, 15, 9, tzinfo=CET),
            "roster": dt.datetime(2026, 12, 1, 16, 2, 44, tzinfo=CET),
            "weather": dt.datetime(2026, 12, 1, 11, 26, 30, tzinfo=CET),
            "ecm": dt.datetime(2026, 12, 1, 14, 48, 12, tzinfo=CET)}


def run(target):
    os.makedirs(target, exist_ok=True)
    Fp = {k: os.path.join(target, v) for k, v in FILES.items()}
    w = sim.history()
    w.movers = sim.movers_of(w.hist)
    n = {}
    n["legs"] = pack.legs(w, Fp["legs"])
    n["changes"] = pack.changes(w, Fp["changes"])
    n["shop"] = pack.shop(w, Fp["shop"])
    n["roster"] = pack.roster(w, Fp["roster"])
    n["vendor"] = pack.vendor(w, Fp["vendor"])
    pack.register(w, Fp["register"])
    pack.pool(w, Fp["pool"])
    pack.programme(w, Fp["programme"])
    pack.shop_plan(w, Fp["shopplan"])
    n["weather"] = pack.weather(w, Fp["weather"])
    n["ecm"] = pack.ecm(w, Fp["ecm"])
    docs.standard(Fp["standard"])
    docs.offer(Fp["offer"])
    F = A.load(target)
    rep = docs.report(Fp["report"], F)
    for k, (c, m, who, comp) in OFFICE.items():
        postprocess.normalize_ooxml(Fp[k], who, who, c, m, excel=True, company=comp)
    postprocess.own_mtimes(target, {FILES[k]: v for k, v in EXPORTED.items()})
    return w, n, rep
