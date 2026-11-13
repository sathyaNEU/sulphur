"""task22 architecture 2 build: the simulated gas system, the pack under target/, the analysis read back from the pack,
figures.json and effort.json, the golden workbook and deck, submission.md and metadata.json.

    python3 make.py            builds in place
"""
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OMP_NUM_THREADS", "1")

import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import analysis as A  # noqa: E402
import deliver as DL  # noqa: E402
import metadata as MD  # noqa: E402
import pack as PK  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402
import writeup as WU  # noqa: E402


def build(task_dir, gen_out):
    target = os.path.join(task_dir, "target")
    gold = os.path.join(task_dir, "golden")
    for d in (target, gold):
        if os.path.isdir(d):
            shutil.rmtree(d)
    W = WD.build()
    F0 = PK.frames(W)
    counts = PK.write(W, F0, target)
    F = A.load(target)
    figs, E, out, cache = RS.write(F, gen_out)
    DL.write(F, out["golden"], figs, gold)
    WU.write(figs, E, os.path.join(task_dir, "submission.md"))
    json.dump(MD.metadata(target, counts), open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
    return W, F, figs, E, out


if __name__ == "__main__":
    build(TASK, HERE)
    print("built", TASK)
