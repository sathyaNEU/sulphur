"""Build the pack, compute every owed figure from it, write the goldens, figures.json, effort.json, submission.md and
metadata.json, run the checks and the independent verifier, rebuild into a scratch folder and require byte-identical
output, then cut target.zip and the golden ZIP.

    python3 task4/generator/make.py            (full: two builds, both zips)
    python3 task4/generator/make.py --once     (one build, no zips)
"""
import hashlib
import json
import os
import re
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
import results as RS  # noqa: E402
import truth as TR  # noqa: E402
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
                      "source": "Constructed (seeded generator, task4/generator)", "pull_date": "2026-12-01",
                      "license": "CC0-1.0 (original work)"})
    return {"task": "task4", "architecture": 13,
            "title": "How many 50, 30 and 20 litre kegs a regional brewer buys for summer 2027",
            "domain": "General Statistics & Data Science (house domain Supply Chain & Logistics, inventory planning)",
            "subdomain": "Regression, classification & model diagnostics",
            "objective": "Forecasting & Predictive Modeling", "as_of": "2026-11-30",
            "deliverables": [GD.XLSX, GD.PDF],
            "distractor_files": [B.FILES[k] for k in B.DISTRACTORS],
            "stated_inputs": ["50", "30", "20", "2016", "2025", "2027", "17", "120", "200", "300"],
            "field_terms": ["keg", "cask", "Foundry", "ullage"],
            "files": files,
            "provenance": "Every file is constructed by the seeded generator in task4/generator from a simulated "
                          "regional brewer: the weather, each customer line's sales, the cellars' orders, the drivers' "
                          "visits and the other brewers' kegs they pick up, kegs lost in the trade, the keg exchange and "
                          "the recovery agent, the depots, the washer, repairs, the brew-house and every RFID read. The "
                          "brewer, its customers, the pub company, the exchange, the agent and the keg maker are "
                          "invented; place names are real names used as setting. No real organisation's records are "
                          "used."}


def one(target, gold):
    for d in (target, gold):
        if os.path.exists(d):
            shutil.rmtree(d)
    w, plans, n = B.run(target)
    G = RS.compute(target)
    f = WU.flat(G)
    GD.write(f, G, gold)
    postprocess.normalize_ooxml(os.path.join(gold, GD.XLSX), P.PEOPLE["analyst"], P.PEOPLE["analyst"],
                                "2026-12-03T08:12:00Z", "2026-12-07T10:46:00Z", excel=True, company=P.ORG)
    postprocess.own_mtimes(gold, {})
    return G, f, n, w, plans


def main():
    once = "--once" in sys.argv
    G, f, n, w, plans = one(TARGET, GOLDEN)
    E = EP.build(G, f)
    WU.write_figures(os.path.join(HERE, "figures.json"), f)
    EP.write(os.path.join(HERE, "effort.json"), E)
    open(os.path.join(TASK, "submission.md"), "w").write(WU.submission(f, G))
    json.dump(metadata(TARGET, n), open(os.path.join(TASK, "metadata.json"), "w"), indent=1)
    tpath = os.path.join(tempfile.gettempdir(), "task4_truth.json")
    json.dump(TR.truth(w, plans), open(tpath, "w"), indent=1, default=str)
    env = dict(os.environ, TASK4_TRUTH=tpath)
    for script in ("checks.py", "verify.py"):
        p = os.path.join(HERE, script)
        if os.path.exists(p):
            r = subprocess.run([sys.executable, p], capture_output=True, text=True, env=env)
            print(r.stdout[-4000:])
            if r.returncode:
                print(r.stderr[-3000:])
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
    postprocess.zip_folder(TARGET, os.path.join(TASK, "target.zip"), zone="Europe/London")
    postprocess.zip_folder(GOLDEN, os.path.join(TASK, "golden.zip"), zone="Europe/London")
    for z in ("target.zip", "golden.zip"):
        print(z, hashlib.sha256(open(os.path.join(TASK, z), "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
