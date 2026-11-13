"""task23 build entry point for the gates: the whole build (pack, golden, figures.json, effort.json, the golden files,
submission.md, metadata.json) into a task folder.

    python3 task23/generator/build.py              builds in place (as make.py)
    python3 task23/generator/build.py --out DIR    builds into DIR (DIR/target, DIR/golden, DIR/generator/...)
"""
import argparse
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
for _v in ("OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import warnings  # noqa: E402

warnings.filterwarnings("ignore")
import make  # noqa: E402

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    if a.out:
        os.makedirs(os.path.join(a.out, "generator"), exist_ok=True)
        make.build(a.out, os.path.join(a.out, "generator"))
        print("built", a.out)
    else:
        make.build(make.TASK, HERE)
        print("built", make.TASK)
