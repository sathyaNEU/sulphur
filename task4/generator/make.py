"""Build the pack, compute every owed figure from it, write the goldens, figures.json, submission.md and
metadata.json, run the checks, the independent verifier and the effort passes, rebuild into a scratch folder and
require byte-identical output, then cut target.zip and the golden ZIP.

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

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

import build as B  # noqa: E402
import golden as GD  # noqa: E402
import params as P  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")


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
        "task": "task4", "architecture": 10,
        "title": "How many battery-electric buses a municipal bus operator should order for its Niittylä depot's weekday "
                 "blocks for 2027, and which blocks they take, under its depot electrification standard",
        "domain": "Supply Chain & Logistics (house domain) in General Statistics & Data Science",
        "subdomain": "regression, classification & model diagnostics (depot electrification: which weekday blocks "
                     "battery-electric buses can run on one overnight charge)",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-11-06", "deliverables": [GD.XLSX, GD.PPTX],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "stated_inputs": [85, 150, 480, 690, 35, 3.9],
        "files": files,
        "provenance": "Every file is constructed by the seeded generator in task4/generator; the town, the company, the "
                      "distribution company, the dealer, the people, the vehicles, the blocks, the transactions, the "
                      "telematics and the weather are invented (Finnish names from a name generator, Finnish bus-industry "
                      "vocabulary). No real organisation's records are used.",
    }


def one(target, gold):
    if os.path.exists(target):
        shutil.rmtree(target)
    if os.path.exists(gold):
        shutil.rmtree(gold)
    w, n = B.run(target)
    pk, g, figs = GD.write(target, gold)
    postprocess.normalize_ooxml(os.path.join(gold, GD.XLSX), "Simo Virta", "Simo Virta", "2026-11-09T07:40:00Z",
                                "2026-11-10T14:21:00Z", excel=True, company=P.ORG)
    postprocess.normalize_pptx(os.path.join(gold, GD.PPTX), "Simo Virta", "Simo Virta", "2026-11-10T09:05:00Z",
                               "2026-11-10T15:02:00Z", "Niittylä 2027: battery-electric buses", P.ORG)
    postprocess.own_mtimes(gold, {})
    return pk, g, figs, n


def zipdir(folder, out):
    if os.path.exists(out):
        os.remove(out)
    postprocess.zip_folder(folder, out, zone="Europe/Helsinki")


def main():
    once = "--once" in sys.argv
    pk, g, figs, n = one(TARGET, GOLDEN)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, ensure_ascii=False)
    WU.write(os.path.join(TASK, "submission.md"), pk, g, figs)
    json.dump(metadata(TARGET, n), open(os.path.join(TASK, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    for script in ("effort_passes.py", "checks.py", "verify.py"):
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
            if open(os.path.join(TARGET, f), "rb").read() != open(os.path.join(t2, f), "rb").read():
                print("differs:", f)
        for f in sorted(os.listdir(GOLDEN)):
            if open(os.path.join(GOLDEN, f), "rb").read() != open(os.path.join(gg2, f), "rb").read():
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
