"""Build the pack, compute every owed figure from it, write the goldens, figures.json, effort.json, submission.md and
metadata.json, run the checks and the independent verifier, rebuild into a scratch folder and require byte-identical
output, then cut target.zip and the golden ZIP.

    python3 task1/generator/make.py            (full: two builds, checks, verify, both zips)
    python3 task1/generator/make.py --once     (one build and the goldens, no checks, no zips)
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
import build as BD  # noqa: E402
import deliver  # noqa: E402
import effort_passes as EP  # noqa: E402
import golden as GD  # noqa: E402
import params as P  # noqa: E402
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

ABOUT = {
    "subs": "subscription system export: one row per subscription (digital consumer, staff, gift, company licence), "
            "January 2023 to October 2026, with the subscriptions running in January 2023",
    "periods": "subscription system export: each subscription's price periods",
    "exceptions": "subscription system export: returned or declined debits, collections, write-offs and refunds",
    "customers": "subscription system export: customer accounts with their postal address",
    "methods": "subscription system export: each customer's payment methods with the payment service provider's "
               "fingerprint",
    "reading": "analytics platform: reading days, articles and app days by login and month, January 2024 to "
               "October 2026",
    "logins": "analytics platform: logins and the customer account each belongs to",
    "spend": "marketing system export: spend, attributed starts and clicks by channel, title and month",
    "offers": "offer catalogue: introductory offers in use",
    "codes": "marketing system: channel codes with their validity",
    "plan": "digital marketing: the 2027 acquisition plan, version 2.1",
    "standard": "controlling: digital subscription KPI standard, version 3",
    "prices": "sales: digital subscription list prices, issued September 2026",
    "kpi": "controlling: monthly digital KPI, January to September 2026",
    "print": "circulation: print and e-paper copies by quarter",
    "newsletter": "editorial: newsletter sign-ups by month",
    "survey": "reader research: 2026 reader survey responses",
    "ads": "advertising sales: digital display revenue by month",
}


def digest(folder):
    h = hashlib.sha256()
    for f in sorted(os.listdir(folder)):
        h.update(f.encode())
        h.update(open(os.path.join(folder, f), "rb").read())
    return h.hexdigest()


def metadata(target):
    files = []
    for k, f in BD.FILES.items():
        p = os.path.join(target, f)
        rows = sum(1 for _ in open(p, encoding="utf-8")) - 1 if f.endswith(".csv") else None
        files.append({"path": f, "format": f.rsplit(".", 1)[1], "bytes": os.path.getsize(p), "rows": rows,
                      "covers": ABOUT[k], "source": "Constructed (seeded generator, task1/generator)",
                      "pull_date": "2026-11-04", "license": "CC0-1.0 (original work)"})
    return {
        "task": "task1", "architecture": 3,
        "title": "Which 2027 digital acquisition lines a regional newspaper group funds, and the budget they need",
        "domain": "Product Analytics",
        "subdomain": "Cohort and LTV modeling (retention curves, customer lifetime value)",
        "objective": "Forecasting & Predictive Modeling",
        "as_of": "2026-11-04", "deliverables": [deliver.XLSX, deliver.PDF],
        "distractor_files": [BD.FILES[k] for k in BD.DISTRACTORS],
        "files": files,
        "provenance": "Every file is constructed by the seeded generator in task1/generator from a simulated "
                      "subscription business (households, offers, billing, reading, marketing); the organisation, "
                      "titles, towns, people, accounts and figures are invented.",
    }


def one(target, gold, full=True):
    if os.path.exists(target):
        shutil.rmtree(target)
    BD.run(target)
    G = GD.compute(target, with_rivals=full, with_routes=full, with_boot=full)
    if gold:
        deliver.write(gold, G)
    return G


def main():
    once = "--once" in sys.argv
    G = one(TARGET, GOLDEN)
    F = WU.write(G, os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    E = EP.build(G, os.path.join(HERE, "effort.json"))
    json.dump(metadata(TARGET), open(os.path.join(TASK, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    print("funded", F["funded"], "budget", F["budget"], "careful", len(F["careful_funded"]))
    if once:
        return
    r = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")], capture_output=True, text=True)
    print(r.stdout[-3000:])
    assert r.returncode == 0, "checks failed"
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), TARGET], capture_output=True, text=True)
    print(r.stdout[-2000:])
    assert r.returncode == 0, "verify failed"
    scratch = tempfile.mkdtemp(prefix="task1-rebuild-")
    try:
        BD.run(os.path.join(scratch, "target"))
        a, b = digest(TARGET), digest(os.path.join(scratch, "target"))
        print("rebuild", "byte-identical" if a == b else "DIFFERENT", a[:16])
        assert a == b, "the rebuild is not byte-identical"
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    WRITERS = os.path.join(os.path.dirname(TASK), ".claude", "skills", "reduce-house-fixes", "scripts", "writers")
    sys.path.insert(0, WRITERS)
    import postprocess
    for folder, out in [(TARGET, os.path.join(TASK, "target.zip")), (GOLDEN, os.path.join(TASK, "golden.zip"))]:
        if os.path.exists(out):
            os.remove(out)
        postprocess.zip_folder(folder, out, zone="Europe/Berlin")
    print("zips cut")


if __name__ == "__main__":
    main()
