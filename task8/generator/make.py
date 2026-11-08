"""task8 architecture 18: builds the pack, the goldens, submission.md, metadata.json and figures.json twice (the
second time from the seed again, in a scratch folder), requires the two builds byte-identical, cuts target.zip and
golden.zip deterministically and runs checks.py, verify.py and ceiling.py on the cut pack."""
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import checks as CK   # noqa: E402
import core as C      # noqa: E402
import deliver as DL  # noqa: E402
import golden as G    # noqa: E402
import pack as PK     # noqa: E402
import world as W     # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
STAMPS = {PK.FILES["responses"]: (2026, 11, 6, 7, 42, 18), PK.FILES["register"]: (2026, 11, 6, 8, 3, 51),
          PK.FILES["bank"]: (2026, 11, 4, 16, 21, 9), PK.FILES["layouts"]: (2026, 11, 4, 11, 42, 0),
          PK.FILES["centres"]: (2026, 11, 2, 10, 15, 37), PK.FILES["spec"]: (2026, 3, 13, 9, 12, 0),
          PK.FILES["standard"]: (2022, 5, 20, 16, 48, 0), PK.FILES["minute"]: (2026, 9, 21, 11, 54, 0),
          PK.FILES["email"]: (2026, 11, 9, 9, 41, 12), PK.FILES["survey"]: (2026, 7, 2, 13, 30, 44),
          PK.FILES["audit"]: (2026, 8, 28, 10, 31, 0)}
GOLD_STAMPS = {"pass_mark_2027.docx": (2026, 11, 27, 15, 42, 0), "l1_2027_items.xlsx": (2026, 11, 27, 14, 58, 0)}


def digest(folder):
    h = hashlib.sha256()
    for root, _, files in sorted(os.walk(folder)):
        for f in sorted(files):
            p = os.path.join(root, f)
            h.update(os.path.relpath(p, folder).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


def one(target, golden, extra, figs):
    w = W.build()
    r = C.compute(w)
    n = PK.write(target, w, r)
    f = G.write_figures(w, r, figs)
    DL.write_all(w, r, f, golden)
    WU.submission(f, os.path.join(extra, "submission.md"))
    WU.metadata(os.path.join(extra, "metadata.json"), n)
    return (w, r), (digest(target), digest(golden), open(os.path.join(extra, "submission.md"), "rb").read(),
                    open(figs, "rb").read())


def cut(folder, stamps, path):
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=stamps[f])
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def main():
    (w, r), t1 = one(TARGET, GOLDEN, TASK, os.path.join(HERE, "figures.json"))
    with tempfile.TemporaryDirectory() as tmp:
        _, t2 = one(os.path.join(tmp, "target"), os.path.join(tmp, "golden"), tmp, os.path.join(tmp, "figures.json"))
    same = [a == b for a, b in zip(t1, t2)]
    print("byte-identical rebuild: target %s, golden %s, submission %s, figures %s" % tuple(same))
    if not all(same):
        return 1
    assert sorted(STAMPS) == sorted(os.listdir(TARGET)), sorted(set(STAMPS) ^ set(os.listdir(TARGET)))
    print("target.zip sha256", cut(TARGET, STAMPS, os.path.join(TASK, "target.zip")))
    print("golden.zip sha256", cut(GOLDEN, GOLD_STAMPS, os.path.join(TASK, "golden.zip")))
    rc = CK.run(w, r, TARGET)
    for s in ("verify.py", "ceiling.py"):
        rc |= subprocess.call([sys.executable, os.path.join(HERE, s)])
    return rc


if __name__ == "__main__":
    sys.exit(main())
