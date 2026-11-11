"""Build the pack, compute every owed figure from it, write the goldens, figures.json, effort.json, submission.md and
metadata.json, run the checks and the independent verifier, rebuild into a scratch folder and require byte-identical
output, then cut target.zip and the golden ZIP.

    python3 task8/generator/make.py            (full)
    python3 task8/generator/make.py --once     (one build and the goldens, no checks, no zips)
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
import writeup as WU  # noqa: E402

TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")

ABOUT = {
    "census": "the trust's MIS: Year 7 students on roll at the 1 October 2026 census",
    "ks2": "KS2 2026 results from the common transfer files: reading, maths and GPS scaled scores and codes",
    "lexis": "the Lexis platform's results export, every sitting this year",
    "quill": "Quill's results export for the trust's Quill academies",
    "quillmap": "Quill's rostering sync: Quill student numbers to the trust's admission numbers",
    "quilllog": "Quill's question-level session log",
    "brightway": "the Brightway academies' results, typed by each academy's staff",
    "academies": "the trust's academy list with each academy's entry reading test",
    "policy": "the trust's Reading Forward policy, version 3 (July 2026)",
    "lexis_tech": "Lexis 11-14 Reading technical summary (publisher)",
    "quill_tech": "Quill Reading technical summary, UK edition (publisher)",
    "brightway_tech": "Brightway Reading Check technical summary (publisher)",
    "cpt": "cognitive profile test results at some academies",
    "attendance": "Year 7 attendance by week, autumn 2026",
    "survey": "Year 7 settling-in survey responses",
    "tutorlog": "Reading Forward tutor session log, 2025-26",
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
                      "covers": ABOUT[k], "source": "Constructed (seeded generator, task8/generator)",
                      "pull_date": "2026-10-12", "license": "CC0-1.0 (original work)"})
    return {
        "task": "task8", "architecture": 19,
        "title": "How much Reading Forward tutor time each academy of a multi-academy trust needs for its Year 7 intake",
        "domain": "Education & Learning Sciences",
        "subdomain": "Psychometrics (scale validation, item response theory, test equating)",
        "objective": "Data Extraction & Conformation (ETL / Pipeline Build)",
        "as_of": "2026-10-12", "deliverables": [deliver.XLSX, deliver.PDF],
        "distractor_files": [BD.FILES[k] for k in BD.DISTRACTORS],
        "stated_inputs": ["339,500", "339500", "27.80", "0.4", "848", "36", "85"],
        "files": files,
        "provenance": "Every file is constructed by the seeded generator in task8/generator from a simulated trust "
                      "(students' reading, KS2, three entry tests and their sittings, the trust's MIS and the "
                      "vendors' exports); the trust, academies, tests, people and figures are invented.",
    }


def one(target, gold, full=True):
    if os.path.exists(target):
        shutil.rmtree(target)
    BD.run(target)
    G = GD.compute(target, with_rivals=True, with_routes=True, with_boot=full)
    return G


def main():
    once = "--once" in sys.argv
    G = one(TARGET, GOLDEN, full=True)
    F = WU.write(G, os.path.join(HERE, "figures.json"), os.path.join(TASK, "submission.md"))
    deliver.write(GOLDEN, G)
    EP.build(G, F, os.path.join(HERE, "effort.json"))
    json.dump(metadata(TARGET), open(os.path.join(TASK, "metadata.json"), "w"), indent=1, ensure_ascii=False)
    print("programme", F["programme_total"], "hours", F["hours_total"], "cost", F["cost_total"],
          "careful", F["careful"]["programme_total"], "range", F.get("range_students"))
    if once:
        return
    r = subprocess.run([sys.executable, os.path.join(HERE, "checks.py")], capture_output=True, text=True)
    print(r.stdout[-4000:])
    assert r.returncode == 0, "checks failed"
    r = subprocess.run([sys.executable, os.path.join(HERE, "verify.py"), TARGET], capture_output=True, text=True)
    print(r.stdout[-2500:])
    assert r.returncode == 0, "verify failed"
    scratch = tempfile.mkdtemp(prefix="task8-rebuild-")
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
        postprocess.zip_folder(folder, out, zone="Europe/London")
    print("zips cut")


if __name__ == "__main__":
    main()
