"""Build the pack, compute every owed figure from it, write the goldens, figures.json, effort.json, submission.md and
metadata.json, rebuild into a scratch folder and require byte-identical output, then cut target.zip and the golden
ZIP.

    python3 task1/generator/make.py            (full: two builds, the goldens, both zips)
    python3 task1/generator/make.py --once     (one build and the goldens, no rebuild, no zips)
"""
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
import metadata  # noqa: E402
import params as P  # noqa: E402
import results as RS  # noqa: E402
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


def goldens(fig):
    if os.path.isdir(GOLDEN):
        shutil.rmtree(GOLDEN)
    deliver.build(GOLDEN, fig)
    postprocess.normalize_ooxml(os.path.join(GOLDEN, deliver.FILES["wb"]), "Ester Rey", "Ester Rey",
                                "2026-11-09T09:12:00Z", "2026-11-10T15:38:27Z", excel=True, company=P.ORG)
    postprocess.normalize_docx(os.path.join(GOLDEN, deliver.FILES["note"]), "Ester Rey", "Ester Rey",
                               "2026-11-10T11:05:00Z", "2026-11-10T16:02:00Z", 4, 41, 2026111, title=None,
                               company=P.ORG)
    postprocess.own_mtimes(GOLDEN, {})


def main(once):
    BD.build(TARGET)
    fig, R, fam, pk, cache = RS.run(TARGET)
    E = RS.effort(fig, R, fam)
    fig["result_bands"] = {r["id"]: r["bands"] for r in E["results"] if r.get("bands")}
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, default=float)
    json.dump(E, open(os.path.join(HERE, "effort.json"), "w"), indent=1, default=float)
    goldens(fig)
    WU.write(os.path.join(TASK, "submission.md"), fig, E)
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
    postprocess.zip_folder(TARGET, os.path.join(TASK, "target.zip"), zone="Europe/Madrid")
    postprocess.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"), zone="Europe/Madrid")
    print("zips cut")


if __name__ == "__main__":
    main("--once" in sys.argv)
