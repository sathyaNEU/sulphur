"""task3 architecture 4: the whole build. The pack into <task>/target, every rung and rival on the cut pack
(generator/rungs.json), the goldens into <task>/golden, submission.md and generator/figures.json, metadata.json;
then the checks and the independent verifier; then a second pack build compared byte for byte; then target.zip and
golden.zip.

    python3 task3/generator/make.py            everything
    python3 task3/generator/make.py --no-rebuild"""
import argparse
import calendar
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B     # noqa: E402
import golden as G    # noqa: E402
import metadata       # noqa: E402
import rivals         # noqa: E402
import writeup        # noqa: E402

TASK = os.path.dirname(HERE)
PULL_DONE = (2026, 11, 6, 9, 40, 0)
MTIME = calendar.timegm((2026, 11, 6, 15, 40, 0, 0, 0, 0))


def stamp(folder):
    for f in os.listdir(folder):
        os.utime(os.path.join(folder, f), (MTIME, MTIME))


def digest(folder):
    return {f: hashlib.sha256(open(os.path.join(folder, f), "rb").read()).hexdigest() for f in sorted(os.listdir(folder))}


def cut_zip(folder, zpath):
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for f in sorted(os.listdir(folder)):
            zi = zipfile.ZipInfo(f, date_time=PULL_DONE)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, open(os.path.join(folder, f), "rb").read())
    return zpath


def pack(root):
    target = os.path.join(root, "target")
    if os.path.isdir(target):
        shutil.rmtree(target)
    n, _ = B.build_pack(target)
    stamp(target)
    return target, n


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-rebuild", action="store_true")
    ap.add_argument("--reuse-rungs", action="store_true")
    a = ap.parse_args()
    target, n = pack(TASK)
    for f in sorted(os.listdir(target)):
        print("  %-60s %10d bytes %s" % (f, os.path.getsize(os.path.join(target, f)), ("%d rows" % n[f]) if f in n else ""))
    rpath = os.path.join(HERE, "rungs.json")
    import solve
    if a.reuse_rungs and os.path.exists(rpath):
        rungs = json.load(open(rpath))
        g = solve.run(target)
    else:
        rungs, full = rivals.main(target, rpath)
        g = full["golden"]
    F = writeup.figures(g, rungs)
    json.dump(F, open(os.path.join(HERE, "figures.json"), "w"), indent=1)
    gdir = os.path.join(TASK, "golden")
    if os.path.isdir(gdir):
        shutil.rmtree(gdir)
    scratch = tempfile.mkdtemp(prefix="t3g_")
    G.write(g, rungs, F, gdir, scratch)
    stamp(gdir)
    writeup.submission(g, rungs, F, os.path.join(TASK, "submission.md"))
    metadata.write(TASK)
    print("call %s cycle, first year at 10: %s, EP-01 2034 %.2f, highest well %s %.2f" %
          (g["call"], g["cross"], g["ep"][2034], F["hi_well"], F["hi_2034"]))
    rc = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")]).returncode
    rc |= subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target]).returncode
    if not a.no_rebuild:
        d1 = digest(target)
        tmp = tempfile.mkdtemp(prefix="t3r_")
        t2, _ = pack(tmp)
        d2 = digest(t2)
        same = d1 == d2
        print("byte-identical rebuild:", "yes" if same else "NO " + str([k for k in d1 if d1[k] != d2.get(k)]))
        rc |= 0 if same else 1
        shutil.rmtree(tmp, ignore_errors=True)
    cut_zip(target, os.path.join(TASK, "target.zip"))
    cut_zip(gdir, os.path.join(TASK, "golden.zip"))
    shutil.rmtree(scratch, ignore_errors=True)
    sys.exit(rc)


if __name__ == "__main__":
    main()
