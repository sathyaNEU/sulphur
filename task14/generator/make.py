"""task14 build: the simulated rental market, the pack under target/, the golden analysis, figures.json, effort.json,
the golden workbook and slides, submission.md and metadata.json.

    python3 make.py            builds in place
    python3 make.py --twice    builds twice into scratch folders and fails unless target/ and golden/ are byte-identical
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OMP_NUM_THREADS", "1")

import golden as GD  # noqa: E402
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
    counts = PK.write(W, target)
    res = RS.compute(target)
    F, E = RS.write(res, gen_out)
    GD.write(F, res, gold)
    WU.write(F, os.path.join(task_dir, "submission.md"), GD.WORKBOOK, GD.SLIDES)
    json.dump(MD.metadata(target, counts), open(os.path.join(task_dir, "metadata.json"), "w"), indent=1)
    return W, res, F, E


def same_tree(a, b):
    for root, _, files in os.walk(a):
        for f in files:
            pa = os.path.join(root, f)
            pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.exists(pb) or not filecmp.cmp(pa, pb, shallow=False):
                return False, os.path.relpath(pa, a)
    return True, ""


if __name__ == "__main__":
    if "--twice" in sys.argv:
        outs = []
        for k in range(2):
            d = tempfile.mkdtemp(prefix="task14-build%d-" % k)
            os.makedirs(os.path.join(d, "generator"))
            build(d, os.path.join(d, "generator"))
            outs.append(d)
        ok = True
        for sub in ("target", "golden"):
            same, which = same_tree(os.path.join(outs[0], sub), os.path.join(outs[1], sub))
            print("%s byte-identical: %s %s" % (sub, same, which))
            ok = ok and same
        for f in ("generator/figures.json", "generator/effort.json", "submission.md", "metadata.json"):
            same = filecmp.cmp(os.path.join(outs[0], f), os.path.join(outs[1], f), shallow=False)
            print("%s byte-identical: %s" % (f, same))
            ok = ok and same
        for d in outs:
            shutil.rmtree(d, ignore_errors=True)
        sys.exit(0 if ok else 1)
    build(TASK, HERE)
    print("built", TASK)
