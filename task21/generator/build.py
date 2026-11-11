"""Build the pack under target/: the simulated book (world.py), the exports (pack.py), the documents and workbooks
(docs.py), every office container through the house writers with its owner's stamps, and each file's time its own
last save or its system's export time.

    python3 build.py [--out <folder>]
"""
import datetime as dt
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

sys.path.insert(0, HERE)
import docs  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import world  # noqa: E402

GMT = dt.timezone.utc
EXPORTED = {pack.FILES["kc"]: dt.datetime(2026, 11, 2, 23, 14, 7, tzinfo=GMT),
            pack.FILES["ct"]: dt.datetime(2026, 11, 2, 23, 41, 52, tzinfo=GMT),
            pack.FILES["bq"]: dt.datetime(2026, 11, 3, 0, 8, 19, tzinfo=GMT),
            pack.FILES["pl"]: dt.datetime(2026, 11, 3, 0, 26, 44, tzinfo=GMT),
            pack.FILES["pol"]: dt.datetime(2026, 11, 3, 5, 3, 11, tzinfo=GMT),
            pack.FILES["clm"]: dt.datetime(2026, 11, 3, 5, 47, 36, tzinfo=GMT),
            pack.FILES["ren"]: dt.datetime(2026, 11, 3, 14, 22, 58, tzinfo=GMT),
            pack.FILES["log"]: dt.datetime(2026, 7, 6, 8, 52, 14, tzinfo=dt.timezone(dt.timedelta(hours=1))),
            pack.FILES["idx"]: dt.datetime(2026, 10, 21, 7, 0, 3, tzinfo=dt.timezone(dt.timedelta(hours=1)))}
WORKBOOKS = {"tri": ("Jeremy Sanders", dt.datetime(2026, 10, 9, 8, 31, 0, tzinfo=GMT),
                     dt.datetime(2026, 10, 14, 16, 4, 27, tzinfo=GMT)),
             "ret": ("Frances Green", dt.datetime(2026, 11, 2, 9, 2, 0, tzinfo=GMT),
                     dt.datetime(2026, 11, 3, 11, 37, 45, tzinfo=GMT)),
             "rates": ("Roy Osborne", dt.datetime(2024, 2, 19, 10, 12, 0, tzinfo=GMT),
                       dt.datetime(2026, 1, 26, 15, 48, 2, tzinfo=GMT)),
             "direct": ("Distribution MI", dt.datetime(2026, 11, 1, 6, 0, 0, tzinfo=GMT),
                        dt.datetime(2026, 11, 2, 7, 19, 30, tzinfo=GMT))}


def build(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = world.build()
    CB = world.ClaimBook(W["claims_full"], P.SEED + 43)
    HB = world.ClaimBook(world.history_claims(np.random.default_rng(P.SEED + 41)), P.SEED + 47)
    counts = pack.write_feeds(W, target)
    npol = pack.write_policies(W, target)
    nclm = pack.write_claims(W, target, CB)
    nren = pack.write_renewals(W, target)
    pack.write_notes(target)
    pack.write_index(target)
    docs.write_pdfs(target)
    docs.write_triangles(os.path.join(target, docs.FILES["tri"]), [HB, CB])
    docs.write_retention(os.path.join(target, docs.FILES["ret"]), W["RH"])
    docs.write_rates(os.path.join(target, docs.FILES["rates"]))
    docs.write_direct(os.path.join(target, docs.FILES["direct"]), np.random.default_rng(P.SEED + 131))
    for k, (who, created, modified) in WORKBOOKS.items():
        postprocess.normalize_ooxml(os.path.join(target, docs.FILES[k]), who, who,
                                    created.strftime("%Y-%m-%dT%H:%M:%SZ"), modified.strftime("%Y-%m-%dT%H:%M:%SZ"),
                                    excel=True, company=docs.ORG)
    postprocess.own_mtimes(target, EXPORTED)
    return dict(W=W, CB=CB, HB=HB, counts=counts, policies=npol, claims=nclm, renewals=nren)


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(out)
    print("feeds", r["counts"], "policies", r["policies"], "claims", r["claims"], "renewals", r["renewals"])
