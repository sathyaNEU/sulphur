"""Build the pack, compute every owed figure from it, write the goldens, figures.json, submission.md and
metadata.json, run the checks and the independent verifier, rebuild into a scratch folder and require
byte-identical output, then cut target.zip and the golden ZIP.

    python3 task4/generator/make.py            (full: two builds, both zips)
    python3 task4/generator/make.py --once     (one build, no zips)
"""
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
import build as B
import golden as GD
import postprocess
import writeup as WU

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
ZSTAMP = (2026, 11, 6, 8, 5, 0)


def digest(folder):
    h = hashlib.sha256()
    for f in sorted(os.listdir(folder)):
        h.update(f.encode())
        h.update(open(os.path.join(folder, f), "rb").read())
    return h.hexdigest()


def metadata(target, n):
    files = []
    for k in B.PACK:
        f = B.FILES[k]
        p = os.path.join(target, f)
        rows = sum(1 for _ in open(p, encoding="utf-8")) - 1 if f.endswith(".csv") else None
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "source": "Constructed (seeded generator, task4/generator)", "pull_date": "2026-11-06",
                      "license": "CC0-1.0 (original work)"})
    return {
        "task": "task4", "architecture": 6,
        "title": "How many battery-electric tractors a Småland road haulier should order for its Värnamo duties for "
                 "2027, and which duties they take, under its fleet electrification standard",
        "domain": "Supply Chain & Logistics (house domain) in General Statistics & Data Science",
        "subdomain": "regression, classification & model diagnostics (fleet electrification: which regular duties "
                     "battery-electric tractors can run on one charge)",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-11-06", "deliverables": [GD.XLSX, GD.PDF],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "files": files,
        "provenance": "Every file is constructed by the seeded generator in task4/generator; Swedish town names are "
                      "real places used for realism (distances approximate), the organisations, people, vehicle "
                      "registrations, consignments, weighings, temperatures and figures are invented. No real "
                      "organisation's records, weather service data or domain is used.",
    }


def one(target, gold):
    if os.path.exists(target):
        shutil.rmtree(target)
    w, n = B.run(target)
    pk, g = GD.write(target, gold)
    postprocess.normalize_ooxml(os.path.join(gold, GD.XLSX), "Inger Norman", "Inger Norman", "2026-11-04T09:10:00Z",
                                "2026-11-06T14:42:00Z", excel=True, company="Fryele Åkeri AB")
    postprocess.own_mtimes(gold, {})
    return pk, g, n


def zipdir(folder, out):
    if os.path.exists(out):
        os.remove(out)
    postprocess.zip_folder(folder, out, zone="Europe/Stockholm")


def main():
    once = "--once" in sys.argv
    pk, g, n = one(TARGET, GOLDEN)
    figs = WU.figures(pk, g)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, ensure_ascii=False)
    WU.write(os.path.join(TASK, "submission.md"), pk, g, figs)
    json.dump(metadata(TARGET, n), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    for script in ("checks.py", "verify.py", "effort_passes.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, script), TARGET], capture_output=True, text=True)
        sys.stdout.write(r.stdout[-3000:])
        if r.returncode:
            sys.stderr.write(r.stderr[-3000:])
            sys.exit("%s failed" % script)
    d1, g1 = digest(TARGET), digest(GOLDEN)
    print("build 1 target %s golden %s" % (d1[:16], g1[:16]))
    if once:
        return
    tmp = tempfile.mkdtemp(prefix="task4-rebuild-")
    t2, gg2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
    one(t2, gg2)
    d2, g2 = digest(t2), digest(gg2)
    print("build 2 target %s golden %s" % (d2[:16], g2[:16]))
    if (d1, g1) != (d2, g2):
        for f in sorted(os.listdir(TARGET)):
            a, b = open(os.path.join(TARGET, f), "rb").read(), open(os.path.join(t2, f), "rb").read()
            if a != b:
                print("differs:", f)
        for f in sorted(os.listdir(GOLDEN)):
            a, b = open(os.path.join(GOLDEN, f), "rb").read(), open(os.path.join(gg2, f), "rb").read()
            if a != b:
                print("differs (golden):", f)
        sys.exit("two builds differ")
    shutil.rmtree(tmp)
    zipdir(TARGET, os.path.join(TASK, "target.zip"))
    zipdir(GOLDEN, os.path.join(TASK, "golden.zip"))
    z = hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()
    print("byte-identical; target.zip", z[:16], "golden.zip",
          hashlib.sha256(open(os.path.join(TASK, "golden.zip"), "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
