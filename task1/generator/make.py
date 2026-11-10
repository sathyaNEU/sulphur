"""Build the pack, compute every owed figure from it, write the goldens, figures.json, effort.json, submission.md and
metadata.json, run the checks and the independent verifier, rebuild into a scratch folder and require
byte-identical output, then cut target.zip and the golden ZIP.

    python3 task1/generator/make.py            (full: two builds, checks, verify, both zips)
    python3 task1/generator/make.py --once     (one build, no checks, no zips)
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
import build as BD
import effort_passes as EP
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


ABOUT = {
    "lines": "billing system export of Business contract lines (subscriptions, true-ups, onboarding fees, credit "
             "notes), January 2022 to October 2026, with the lines in force at January 2022",
    "team": "Team plan invoices, January 2022 to October 2026",
    "activity": "monthly active users and boards edited per workspace, January 2022 to October 2026",
    "links": "which billing account each workspace belongs to, with dates",
    "crm": "CRM account export: Business accounts, parent accounts, country, industry, lead source, status",
    "snap": "month-end snapshots of open sales opportunities, January 2023 to October 2026",
    "closed": "closed sales opportunities, January 2022 to October 2026",
    "price": "2026 price book",
    "policy": "ARR reporting policy, version 4",
    "kpi": "monthly revenue KPI export, January to September 2026",
    "tickets": "support tickets opened in 2026",
    "nps": "NPS survey responses, July to September 2026",
}


def metadata(target):
    files = []
    for k in BD.PACK:
        f = BD.FILES[k]
        p = os.path.join(target, f)
        rows = sum(1 for _ in open(p, encoding="utf-8")) - 1 if f.endswith(".csv") else None
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "covers": ABOUT[k], "source": "Constructed (seeded generator, task1/generator)",
                      "pull_date": "2026-11-03", "license": "CC0-1.0 (original work)"})
    return {
        "task": "task1", "architecture": 2,
        "title": "December 2027 ARR that a Utrecht diagramming SaaS company can commit to in its 2027 plan",
        "domain": "Product Analytics",
        "subdomain": "Cohort and LTV modeling (retention curves, customer lifetime value)",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-11-03", "deliverables": [GD.XLSX, GD.DOCX],
        "distractor_files": [BD.FILES[k] for k in BD.DISTRACTORS],
        "files": files,
        "provenance": "Every file is constructed by the seeded generator in task1/generator from a simulated "
                      "process; company names are drawn from Faker's nl_NL, de_DE and en_GB locales; the "
                      "organisation, people, accounts, workspaces, invoices, deals and figures are invented.",
    }


def one(target, gold):
    if os.path.exists(target):
        shutil.rmtree(target)
    BD.run(target)
    F, B, g, R = GD.write(target, gold)
    return F, B, g, R


def zipdir(folder, out):
    if os.path.exists(out):
        os.remove(out)
    postprocess.zip_folder(folder, out, zone="Europe/Amsterdam")


def main():
    once = "--once" in sys.argv
    F, B, g, R = one(TARGET, GOLDEN)
    figs = WU.figures(F, B, g, R)
    json.dump(figs, open(os.path.join(HERE, "figures.json"), "w"), indent=1, sort_keys=True, ensure_ascii=False)
    WU.write(os.path.join(TASK, "submission.md"), figs)
    EP.write(F, B, g, R, figs)
    json.dump(metadata(TARGET), open(os.path.join(TASK, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    d1, g1 = digest(TARGET), digest(GOLDEN)
    print("build 1 target %s golden %s" % (d1[:16], g1[:16]))
    if once:
        return
    for script in ("checks.py", "verify.py"):
        r = subprocess.run([sys.executable, "-W", "ignore", os.path.join(HERE, script), TARGET], capture_output=True,
                           text=True)
        sys.stdout.write(r.stdout[-4000:])
        if r.returncode:
            sys.stderr.write(r.stderr[-3000:])
            sys.exit("%s failed" % script)
    tmp = tempfile.mkdtemp(prefix="task1-rebuild-")
    t2, gg2 = os.path.join(tmp, "target"), os.path.join(tmp, "golden")
    one(t2, gg2)
    d2, g2 = digest(t2), digest(gg2)
    print("build 2 target %s golden %s" % (d2[:16], g2[:16]))
    if (d1, g1) != (d2, g2):
        for a, b in ((TARGET, t2), (GOLDEN, gg2)):
            for f in sorted(os.listdir(a)):
                if open(os.path.join(a, f), "rb").read() != open(os.path.join(b, f), "rb").read():
                    print("differs:", f)
        sys.exit("two builds differ")
    shutil.rmtree(tmp)
    zipdir(TARGET, os.path.join(TASK, "target.zip"))
    zipdir(GOLDEN, os.path.join(TASK, "golden.zip"))
    print("byte-identical; target.zip", hashlib.sha256(open(os.path.join(TASK, "target.zip"), "rb").read()).hexdigest()[:16],
          "golden.zip", hashlib.sha256(open(os.path.join(TASK, "golden.zip"), "rb").read()).hexdigest()[:16])


if __name__ == "__main__":
    main()
