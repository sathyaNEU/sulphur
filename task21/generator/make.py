"""Build the pack, compute every owed figure from it, write the goldens, figures.json, effort.json, submission.md and
metadata.json, rebuild into a scratch folder and require byte-identical output, then cut target.zip and the golden
ZIP.

    python3 task21/generator/make.py            (full: two builds, the goldens, both zips)
    python3 task21/generator/make.py --once     (one build and the goldens, no rebuild, no zips)
"""
import datetime as dt
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts",
                       "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402
import build as BD  # noqa: E402
import deliver  # noqa: E402
import effort_passes as EP  # noqa: E402
import metadata  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
GMT = dt.timezone.utc


def digest(folder):
    h = hashlib.sha256()
    for name in sorted(os.listdir(folder)):
        h.update(name.encode())
        h.update(open(os.path.join(folder, name), "rb").read())
    return h.hexdigest()[:16]


def goldens(fig, GD):
    if os.path.isdir(GOLDEN):
        shutil.rmtree(GOLDEN)
    deliver.build(GOLDEN, fig, GD)
    postprocess.normalize_ooxml(os.path.join(GOLDEN, deliver.FILES["wb"]), "Frances Green", "Frances Green",
                                "2026-11-09T08:14:00Z", "2026-11-11T16:52:31Z", excel=True,
                                company="Halvergate Mutual Insurance Society Limited")
    postprocess.normalize_pptx(os.path.join(GOLDEN, deliver.FILES["deck"]), "Frances Green", "Jeremy Sanders",
                               "2026-11-10T09:30:00Z", "2026-11-11T17:05:12Z",
                               title="2027 comparison-site new-business rates",
                               company="Halvergate Mutual Insurance Society Limited")
    postprocess.own_mtimes(GOLDEN, {})


def main(once):
    BD.build(TARGET)
    fig, E, GD = EP.run(TARGET)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, default=float)
    json.dump(E, open(os.path.join(HERE, "effort.json"), "w"), indent=1, default=float)
    goldens(fig, GD)
    WU.write(os.path.join(TASK, "submission.md"), fig)
    metadata.write(os.path.join(TASK, "metadata.json"))
    first = digest(TARGET)
    print("target", first, "golden", digest(GOLDEN))
    if once:
        return
    tmp = tempfile.mkdtemp()
    BD.build(os.path.join(tmp, "target"))
    second = digest(os.path.join(tmp, "target"))
    shutil.rmtree(tmp)
    assert first == second, "the rebuild differs: %s against %s" % (first, second)
    print("rebuild byte-identical", second)
    postprocess.zip_folder(TARGET, os.path.join(TASK, "target.zip"), zone="Europe/London")
    postprocess.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"), zone="Europe/London")
    print("zips cut")


if __name__ == "__main__":
    main("--once" in sys.argv)
