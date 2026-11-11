"""Build the pack, compute every owed figure from it, write the goldens, figures.json, effort.json, submission.md
and metadata.json, run the checks and the independent verifier, rebuild into a scratch folder and require
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
import warnings

warnings.filterwarnings("ignore")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
WRITERS = os.path.join(os.path.dirname(os.path.dirname(HERE)), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
sys.path.insert(0, WRITERS)
import postprocess  # noqa: E402

import build as B  # noqa: E402
import effort_passes as EP  # noqa: E402
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
        "task": "task4", "architecture": 11,
        "title": "Which weeks of the 2027 peak a fulfilment centre's two small-parts zones need the evening shift, and "
                 "how many agency picker hours to book each peak week, once a second brand's orders share the zones",
        "domain": "Supply Chain & Logistics (house domain) in General Statistics & Data Science",
        "subdomain": "regression, classification & model diagnostics (an e-commerce fulfilment centre's peak labour plan)",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-11-06", "deliverables": [GD.XLSX, GD.DOCX],
        "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
        "files": files,
        "provenance": "Every file is constructed by the seeded generator in task4/generator; the logistics provider, "
                      "the retailer, its brands, the agency, the people, the articles and every record are invented "
                      "(Finnish names from a name generator, Finnish warehouse and payroll vocabulary). No real "
                      "organisation's records are used.",
    }


def one(target, gold):
    if os.path.exists(target):
        shutil.rmtree(target)
    if os.path.exists(gold):
        shutil.rmtree(gold)
    w, n = B.run(target)
    f, G, figs = GD.write(target, gold)
    postprocess.normalize_ooxml(os.path.join(gold, GD.XLSX), P.PEOPLE["director"], P.PEOPLE["director"],
                                "2026-11-09T07:40:00Z", "2026-11-10T13:21:00Z", excel=True, company=P.ORG)
    postprocess.normalize_docx(os.path.join(gold, GD.DOCX), P.PEOPLE["director"], P.PEOPLE["director"],
                               "2026-11-09T12:05:00Z", "2026-11-10T14:02:00Z", revision=6, total_time=118,
                               seed="task4-memo", title="Saarnela peak 2027: evening shifts and agency booking",
                               company=P.ORG)
    postprocess.own_mtimes(gold, {})
    return f, G, figs, n


def main():
    once = "--once" in sys.argv
    f, G, figs, n = one(TARGET, GOLDEN)
    rg = GD.compute(TARGET)[3]
    E, rivals, extra = EP.build(f, G, figs, rg)
    flat = WU.flat(figs, G, f, rivals)
    flat.update(extra)
    WU.write_figures(os.path.join(HERE, "figures.json"), flat)
    EP.write(os.path.join(HERE, "effort.json"), E)
    open(os.path.join(TASK, "submission.md"), "w").write(WU.submission(flat))
    json.dump(metadata(TARGET, n), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    for script in ("checks.py", "verify.py"):
        p = os.path.join(HERE, script)
        if os.path.exists(p):
            r = subprocess.run([sys.executable, p], capture_output=True, text=True)
            print(r.stdout[-2500:])
            if r.returncode:
                print(r.stderr[-2500:])
                sys.exit("%s failed" % script)
    d1, g1 = digest(TARGET), digest(GOLDEN)
    print("target %s golden %s" % (d1[:16], g1[:16]))
    if once:
        return
    tmp = tempfile.mkdtemp()
    one(os.path.join(tmp, "t"), os.path.join(tmp, "g"))
    d2, g2 = digest(os.path.join(tmp, "t")), digest(os.path.join(tmp, "g"))
    assert (d1, g1) == (d2, g2), "the two builds differ"
    print("byte-identical rebuild")
    shutil.rmtree(tmp)
    postprocess.zip_folder(TARGET, os.path.join(TASK, "target.zip"), zone="Europe/Helsinki")
    postprocess.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"), zone="Europe/Helsinki")
    for z in ("target.zip", "golden.zip"):
        print(z, hashlib.sha256(open(os.path.join(TASK, z), "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
