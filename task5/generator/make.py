"""Build the pack, compute every owed figure from it, write figures.json, effort.json, the goldens, submission.md and
metadata.json, rebuild into a scratch folder and require byte-identical output, then cut target.zip and the golden ZIP.

    python3 task5/generator/make.py            (full: two builds, the goldens, both zips)
    python3 task5/generator/make.py --once     (one build and the goldens, no rebuild, no zips)
    python3 task5/generator/make.py --keep     (the pack as it stands: figures, goldens and blocks only)
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
import metadata  # noqa: E402
import results as RS  # noqa: E402
import world as WL  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
CET = dt.timezone(dt.timedelta(hours=1))
ZONE = "Europe/Ljubljana"


def digest(folder):
    h = hashlib.sha256()
    for name in sorted(os.listdir(folder)):
        h.update(name.encode())
        h.update(open(os.path.join(folder, name), "rb").read())
    return h.hexdigest()[:16]


def goldens(fig, folder=GOLDEN):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    deliver.build(folder, fig)
    postprocess.normalize_ooxml(os.path.join(folder, deliver.FILES["wb"]), WL.PEOPLE["analyst"], WL.PEOPLE["head"],
                                "2027-02-23T08:37:00Z", "2027-02-25T14:12:46Z", excel=True, company=WL.ORG)
    postprocess.own_mtimes(folder, {deliver.FILES["csv"]: dt.datetime(2027, 2, 25, 14, 51, 20, tzinfo=CET)})


def main(argv):
    if "--keep" not in argv:
        BD.build(TARGET)
    X, fig, E, spec = RS.run(TARGET)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, default=float)
    json.dump(E, open(os.path.join(HERE, "effort.json"), "w"), indent=1, default=float)
    fig = json.load(open(os.path.join(HERE, "figures.json")))
    goldens(fig)
    WU.write(os.path.join(TASK, "submission.md"), fig)
    metadata.write(os.path.join(TASK, "metadata.json"))
    first = digest(TARGET)
    print("target", first, "golden", digest(GOLDEN), "rubric", fig["rubric"])
    if "--once" in argv or "--keep" in argv:
        return
    tmp = tempfile.mkdtemp()
    BD.build(os.path.join(tmp, "target"))
    second = digest(os.path.join(tmp, "target"))
    goldens(fig, os.path.join(tmp, "golden"))
    g2 = digest(os.path.join(tmp, "golden"))
    shutil.rmtree(tmp)
    assert first == second, "the rebuild differs: %s against %s" % (first, second)
    assert g2 == digest(GOLDEN), "the goldens rebuild differently"
    print("rebuild byte-identical", second)
    postprocess.zip_folder(TARGET, os.path.join(TASK, "target.zip"), zone=ZONE)
    postprocess.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"), zone=ZONE)
    print("zips cut", os.path.getsize(os.path.join(TASK, "target.zip")), os.path.getsize(os.path.join(TASK, "golden.zip")))


if __name__ == "__main__":
    main(sys.argv[1:])
