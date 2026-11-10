"""Build the pack, compute every owed figure from the shipped files, write the goldens, figures.json, submission.md
and metadata.json, run the checks, the independent verifier and the effort passes, rebuild into a scratch folder and
require byte-identical output, then cut target.zip and golden.zip.

    python3 task17/generator/make.py            (full: two builds, both zips)
    python3 task17/generator/make.py --once     (one build, no zips, no second build)
    python3 task17/generator/make.py --golden   (goldens, figures, submission and metadata only, on the built pack)
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
import build as B
import golden as GD
import postprocess
import writeup as WU

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
                      "source": "Constructed (seeded generator, task17/generator)", "pull_date": "2026-11-16",
                      "license": "CC0-1.0 (original work)"})
    return {
        "task": "task17", "architecture": 1,
        "title": "How many node-hours of GPU grants the Landesrechenzentrum Ravensfeld's 2027 allocation round can "
                 "carry under its service level, and what share of the requests that cuts",
        "domain": "General Statistics & Data Science",
        "subdomain": "Resampling, simulation & Monte Carlo methods (sizing a shared GPU partition's allocation round "
                     "under a queue-wait service level)",
        "objective": "Descriptive & Distribution Analysis",
        "as_of": "2026-11-16", "deliverables": [GD.XLSX, GD.DOCX],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "files": files,
        "provenance": "Every file is constructed by the seeded generator in task17/generator: the organisation, its "
                      "universities, people, projects, jobs, nodes, outages and figures are invented; German names "
                      "come from a name generator. No real organisation's records are used.",
    }


def goldens_only():
    g, pk = GD.write(TARGET, GOLDEN)
    figs = WU.figures(pk, g)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, ensure_ascii=False)
    WU.write(os.path.join(TASK, "submission.md"), pk, g, figs)
    return g, pk, figs


def one(target, gold):
    w, pk, n = B.run(target)
    g, pk2 = GD.write(target, gold)
    return g, pk2, n


def zipdir(folder, out):
    if os.path.exists(out):
        os.remove(out)
    postprocess.zip_folder(folder, out, zone="Europe/Berlin")


def main():
    once = "--once" in sys.argv
    if "--golden" in sys.argv:
        g, pk, figs = goldens_only()
        json.dump(metadata(TARGET, None), open(os.path.join(TASK, "metadata.json"), "w"), indent=1, ensure_ascii=False)
        print("goldens, figures.json, submission.md and metadata.json written")
        return
    g, pk, n = one(TARGET, GOLDEN)
    figs = WU.figures(pk, g)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, ensure_ascii=False)
    WU.write(os.path.join(TASK, "submission.md"), pk, g, figs)
    json.dump(metadata(TARGET, n), open(os.path.join(TASK, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    for script in ("checks.py", "verify.py", "effort_passes.py"):
        r = subprocess.run([sys.executable, os.path.join(HERE, script), TARGET], capture_output=True, text=True)
        sys.stdout.write(r.stdout[-4000:])
        if r.returncode:
            sys.stderr.write(r.stderr[-4000:])
            sys.exit("%s failed" % script)
    d1, g1 = digest(TARGET), digest(GOLDEN)
    print("build 1 target %s golden %s" % (d1[:16], g1[:16]))
    if once:
        return
    tmp = tempfile.mkdtemp(prefix="task17-rebuild-")
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
