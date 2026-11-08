"""task3 architecture 3: the whole build. The pack into <task>/target, every rung and rival on the cut pack
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
MTIME = calendar.timegm((2026, 11, 6, 14, 40, 0, 0, 0, 0))


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
        print("  %-56s %10d bytes %s" % (f, os.path.getsize(os.path.join(target, f)), ("%d rows" % n[f]) if f in n else ""))
    rpath = os.path.join(HERE, "rungs.json")
    if a.reuse_rungs and os.path.exists(rpath):
        import solve
        rungs = json.load(open(rpath))
        g = solve.run(target)
    else:
        rungs, full = rivals.main(target, rpath)
        g = full["golden"]
    gdir = os.path.join(TASK, "golden")
    if os.path.isdir(gdir):
        shutil.rmtree(gdir)
    scratch = tempfile.mkdtemp(prefix="t3g_")
    G.write(g, rungs, gdir, scratch)
    shutil.rmtree(scratch)
    stamp(gdir)
    fig = writeup.figures(g, rungs)
    json.dump(fig, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True)
    writeup.submission(g, rungs, fig, os.path.join(TASK, "submission.md"))
    metadata.write(TASK)
    ok_c = subprocess.run([sys.executable, os.path.join(HERE, "checks.py"), target, rpath]).returncode == 0
    ok_v = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), target,
                           os.path.join(HERE, "figures.json")]).returncode == 0
    same = True
    if not a.no_rebuild:
        tmp = tempfile.mkdtemp(prefix="t3b_", dir=os.path.dirname(TASK))
        try:
            t2, _ = pack(tmp)
            same = digest(target) == digest(t2)
            g2 = os.path.join(tmp, "golden")
            s2 = tempfile.mkdtemp(prefix="t3g_")
            G.write(g, rungs, g2, s2)
            shutil.rmtree(s2)
            same = same and digest(gdir) == digest(g2)
            print("rebuild byte-identical: %s" % same)
        finally:
            shutil.rmtree(tmp)
    z = cut_zip(target, os.path.join(TASK, "target.zip"))
    gz = cut_zip(gdir, os.path.join(TASK, "golden.zip"))
    for p in (z, gz):
        print("zip %s %d bytes sha256 %s" % (p, os.path.getsize(p), hashlib.sha256(open(p, "rb").read()).hexdigest()[:8]))
    sys.exit(0 if (ok_c and ok_v and same) else 1)


if __name__ == "__main__":
    main()
