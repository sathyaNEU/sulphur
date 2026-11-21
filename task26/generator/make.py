"""Orchestrate full deterministic build for task26:
1. Build target/ from core.py via build.py
2. Recompute every owed figure strictly from target/ via results.py -> figures.json, effort.json
3. Build golden/ via deliver.py + normalize_ooxml + own_mtimes
4. Emit submission.md via writeup.py and metadata.json via metadata.py
5. Rebuild both target/ and golden/ into a temporary folder and assert byte-identical digests
6. Cut target.zip and golden.zip via postprocess.zip_folder (Europe/Oslo clock)

    python3 task26/generator/make.py          (full build + byte-identical check + zips)
    python3 task26/generator/make.py --keep   (reuse target/, refresh figures/goldens/writeup/zips)
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
import deliver as DL  # noqa: E402
import metadata as MD  # noqa: E402
import pack as PK  # noqa: E402
import results as RS  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
CET = dt.timezone(dt.timedelta(hours=1))
ZONE = "Europe/Oslo"


def digest(folder):
    h = hashlib.sha256()
    for name in sorted(os.listdir(folder)):
        h.update(name.encode())
        h.update(open(os.path.join(folder, name), "rb").read())
    return h.hexdigest()[:16]


def build_goldens(fig, folder=GOLDEN):
    if os.path.isdir(folder):
        shutil.rmtree(folder)
    DL.build(folder, fig)
    postprocess.normalize_ooxml(
        os.path.join(folder, DL.FILES["wb"]),
        PK.PEOPLE["analyst"], PK.PEOPLE["head"],
        "2027-01-19T09:14:00Z", "2027-01-20T11:32:18Z",
        excel=True, company=PK.ORG,
    )
    postprocess.own_mtimes(folder, {
        DL.FILES["csv"]: dt.datetime(2027, 1, 20, 12, 48, 10, tzinfo=CET),
    })


def main(argv):
    if "--keep" not in argv:
        BD.build(TARGET)
    _, fig, E, _spec = RS.run(TARGET)
    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(fig, f, indent=1, sort_keys=True, default=float)
    with open(os.path.join(HERE, "effort.json"), "w", encoding="utf-8") as f:
        json.dump(E, f, indent=1, sort_keys=True, default=float)
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    build_goldens(fig)
    WU.write(os.path.join(TASK, "submission.md"), fig)
    MD.write(os.path.join(TASK, "metadata.json"))
    first_t = digest(TARGET)
    first_g = digest(GOLDEN)
    print(f"target={first_t}  golden={first_g}  total_relief={fig['total_relief_mva']:.2f} MVA")
    if "--once" not in argv and "--keep" not in argv:
        tmp = tempfile.mkdtemp(prefix="task26-rebuild-")
        try:
            BD.build(os.path.join(tmp, "target"))
            second_t = digest(os.path.join(tmp, "target"))
            build_goldens(fig, os.path.join(tmp, "golden"))
            second_g = digest(os.path.join(tmp, "golden"))
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        assert first_t == second_t, f"target rebuild differs: {first_t} vs {second_t}"
        assert first_g == second_g, f"golden rebuild differs: {first_g} vs {second_g}"
        print(f"rebuild byte-identical: target={second_t} golden={second_g}")
    postprocess.zip_folder(TARGET, os.path.join(TASK, "target.zip"), zone=ZONE)
    postprocess.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"), zone=ZONE)
    print("zips cut:", os.path.getsize(os.path.join(TASK, "target.zip")),
          os.path.getsize(os.path.join(TASK, "golden.zip")))


if __name__ == "__main__":
    main(sys.argv[1:])
