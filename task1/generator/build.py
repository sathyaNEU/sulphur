"""Build the pack under target/: the simulated business (world.py), the system exports (pack.py), the documents and
finance's workbook (docs.py), every office container through the house writers with its owner's stamps, and each
file's time its own last save or its system's export time.

    python3 build.py [--out <folder>]
"""
import collections
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
CET = dt.timezone(dt.timedelta(hours=1))
EXPORTED = {pack.FILES["acc"]: dt.datetime(2026, 11, 3, 2, 14, 7, tzinfo=GMT),
            pack.FILES["plan"]: dt.datetime(2026, 11, 3, 2, 19, 52, tzinfo=GMT),
            pack.FILES["pay"]: dt.datetime(2026, 11, 3, 2, 41, 19, tzinfo=GMT),
            pack.FILES["prof"]: dt.datetime(2026, 11, 3, 3, 6, 44, tzinfo=GMT),
            pack.FILES["live"]: dt.datetime(2026, 11, 4, 5, 2, 11, tzinfo=GMT),
            pack.FILES["lic"]: dt.datetime(2026, 11, 4, 6, 47, 36, tzinfo=GMT),
            pack.FILES["cat"]: dt.datetime(2026, 11, 2, 22, 30, 58, tzinfo=GMT),
            pack.FILES["xw"]: dt.datetime(2025, 3, 3, 9, 12, 40, tzinfo=CET),
            pack.FILES["stm"]: dt.datetime(2026, 11, 3, 7, 55, 3, tzinfo=GMT),
            pack.FILES["pod"]: dt.datetime(2026, 11, 4, 5, 31, 27, tzinfo=GMT),
            pack.FILES["ebk"]: dt.datetime(2026, 11, 4, 5, 38, 2, tzinfo=GMT),
            pack.FILES["rev"]: dt.datetime(2026, 11, 2, 8, 0, 19, tzinfo=GMT),
            pack.FILES["riv"]: dt.datetime(2026, 10, 30, 16, 42, 9, tzinfo=CET)}


def kpi_rows(W):
    acc = {a["aid"]: a for a in W["accounts"]}
    paying = collections.defaultdict(collections.Counter)
    seen = set()
    for c in W["charges"]:
        if c["status"] in ("collected", "re-presented") and c["price"] > 0 and acc[c["aid"]]["kind"] == "consumer":
            if (c["aid"], c["m"]) in seen:
                continue
            seen.add((c["aid"], c["m"]))
            paying[c["m"]][c["plan"]] += 1
    rev = collections.Counter()
    for c in W["charges"]:
        rev[c["m"]] += pack.net_revenue(c)
    trials = collections.Counter(a["created"][0] for a in W["accounts"] if a["trial_days"] and a["kind"] == "consumer")
    rows = []
    for m in range(36, 45):
        pc = paying[m]
        rows.append([P.month_label(m)] + [pc[p] for p in P.PLANS] + [sum(pc.values()), trials[m],
                                                                    round(rev[m], 2), round(P.SHARE26 * rev[m], 2)])
    return rows


def build(target):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    W = world.simulate()
    rng = np.random.default_rng(P.SEED + 5)
    counts = pack.write(W, target, rng)
    counts["stm"] = pack.write_statements(W, target)
    counts["pod"], counts["ebk"], counts["rev"] = pack.write_distractors(W, target, rng)
    counts["riv"] = pack.write_rival(target, rng)
    docs.write_pdfs(target)
    docs.write_kpi(os.path.join(target, docs.FILES["kpi"]), kpi_rows(W))
    postprocess.normalize_ooxml(os.path.join(target, docs.FILES["kpi"]), "Hugo Brouwer", "Hugo Brouwer",
                                "2026-01-08T08:41:00Z", "2026-10-07T14:16:33Z", excel=True, company=docs.ORG)
    postprocess.own_mtimes(target, EXPORTED)
    return {"W": W, "counts": counts}


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(out)
    print(r["counts"])
