"""task25 build: the simulated record, the pack under target/, the golden read back from the pack alone,
figures.json and effort.json, the golden workbook and note, submission.md and metadata.json.

    python3 make.py
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OMP_NUM_THREADS", "1")

import warnings  # noqa: E402

warnings.filterwarnings("ignore")

import analysis as A  # noqa: E402
import cutpack as CP  # noqa: E402
import deliver as DL  # noqa: E402
import metadata as MD  # noqa: E402
import records as RC  # noqa: E402
import results as RS  # noqa: E402
import writeup as WU  # noqa: E402


def main(out=None):
    """Build in place, or with out= into a scratch folder (target/, golden/, generator outputs, submission.md,
    metadata.json under it) so two builds can be compared byte for byte without touching the task folder."""
    base = out or TASK
    gen_out = os.path.join(out, "generator") if out else HERE
    os.makedirs(gen_out, exist_ok=True)
    target = os.path.join(base, "target")
    rec = RC.simulate()
    CP.write(target, rec)
    G = A.golden(target)
    fig, E, X = RS.build(G, mc_n=160)
    with open(os.path.join(gen_out, "figures.json"), "w") as fh:
        json.dump(fig, fh, indent=1, sort_keys=True)
    with open(os.path.join(gen_out, "effort.json"), "w") as fh:
        json.dump(E, fh, indent=1)
    DL.write(os.path.join(base, "golden"), G, fig, X)
    WU.write(os.path.join(base, "submission.md"), fig, G)
    MD.write(base)
    print("late:", fig["call_late_runs"])
    return rec, G, fig, E, X


if __name__ == "__main__":
    o = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else None
    main(o)
