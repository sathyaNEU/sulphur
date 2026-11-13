"""Build the pack: the world, what the systems observe, the data files, the documents and the workbooks, each container
through the house writers with its owner's stamps and its own save time."""
import os
import shutil
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402
import docs  # noqa: E402
import obs as OB  # noqa: E402
import pack  # noqa: E402
import params as P  # noqa: E402
import world as W  # noqa: E402

import datetime as dt  # noqa: E402
CST = dt.timezone(dt.timedelta(hours=-6))
# the year's exports were pulled once 2026 closed; the trial's own records when it ended; the queue at its October cut
_E = {"ami": (2027, 1, 5, 7, 14, 9), "head": (2027, 1, 5, 7, 31, 40), "bus": (2027, 1, 6, 10, 2, 18), "ltc": (2027, 1, 6, 10, 5, 3),
      "bell": (2027, 1, 5, 8, 46, 51), "reg": (2026, 11, 16, 9, 12, 26), "sched": (2026, 11, 16, 9, 20, 7),
      "wx": (2027, 1, 4, 13, 37, 45), "out": (2027, 1, 7, 11, 8, 30), "der": (2026, 10, 30, 16, 22, 12)}
EXPORTED = {pack.FILES[k]: dt.datetime(y, m, d, hh, mm, ss, tzinfo=CST) for k, (y, m, d, hh, mm, ss) in _E.items()}
EXPORTED[pack.FILES["survey"]] = dt.datetime(2025, 12, 11, 15, 50, 2, tzinfo=CST)


def build(target, seed=P.SEED):
    if os.path.isdir(target):
        shutil.rmtree(target)
    os.makedirs(target)
    w = W.build(seed)
    O = OB.observe(w, seed + 1)
    rng = np.random.default_rng(seed + 7)
    ids = pack.feeder_ids(w)
    n = {}
    n["ami"] = pack.write_ami(w, O, ids, target, rng)
    n["head"] = pack.write_head(w, O, ids, target)
    n["bus"] = pack.write_bus(w, O, target, rng)
    n["ltc"] = pack.write_ltc(w, target)
    n["bell"] = pack.write_bell(w, O, ids, target, rng)
    n["reg"] = pack.write_reg(w, O, ids, target, rng)
    n["sched"] = pack.write_sched(w, ids, target)
    n["wx"] = pack.write_wx(w, target, rng)
    n["survey"] = pack.write_survey(w, O, ids, target, rng)
    n["out"], n["der"] = pack.write_distractors(w, ids, target, rng)
    docs.write_pdfs(target, w)
    docs.write_register(os.path.join(target, pack.FILES["reg_x"]), w, O, ids)
    docs.write_plan(os.path.join(target, pack.FILES["plan_x"]), w, ids)
    postprocess.normalize_ooxml(os.path.join(target, pack.FILES["reg_x"]), "Joseph Harmon", "Anthony Harris",
                                "2023-05-16T14:02:00Z", "2026-11-04T16:41:27Z", excel=True, company=docs.ORG)
    postprocess.normalize_ooxml(os.path.join(target, pack.FILES["plan_x"]), "Bruce Hart", "Bruce Hart",
                                "2026-08-25T13:20:00Z", "2026-10-29T21:07:44Z", excel=True, company=docs.ORG)
    postprocess.own_mtimes(target, EXPORTED)
    return dict(w=w, O=O, ids=ids, counts=n)


if __name__ == "__main__":
    out = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(os.path.dirname(HERE), "target")
    r = build(out)
    print(r["counts"])
