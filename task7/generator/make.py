"""Build the pack, compute every owed figure from its read-back, write the goldens, figures.json, effort.json,
submission.md and metadata.json, rebuild into a scratch folder and require byte-identical output, then cut the zips.

    python3 task7/generator/make.py            (full)
    python3 task7/generator/make.py --once     (one build and the goldens, no rebuild, no zips)
"""
import hashlib
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
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


def digest(folder):
    h = hashlib.sha256()
    for name in sorted(os.listdir(folder)):
        h.update(name.encode())
        h.update(open(os.path.join(folder, name), "rb").read())
    return h.hexdigest()[:16]


def main(once):
    BD.build(TARGET)
    fig, E = EP.run_all(TARGET)
    fig["org"] = deliver.ORG
    WU.texts(fig)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, default=float)
    json.dump(E, open(os.path.join(HERE, "effort.json"), "w"), indent=1, default=float)
    if os.path.isdir(GOLDEN):
        shutil.rmtree(GOLDEN)
    scratch = tempfile.mkdtemp()
    deliver.build(GOLDEN, fig, scratch)
    postprocess.own_mtimes(GOLDEN, {})
    WU.write(os.path.join(TASK, "submission.md"), fig, fig["bands"])
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
    postprocess.zip_folder(TARGET, os.path.join(TASK, "target.zip"), zone="America/Chicago")
    postprocess.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"), zone="America/Chicago")
    print("zips cut")


if __name__ == "__main__":
    main("--once" in sys.argv)
