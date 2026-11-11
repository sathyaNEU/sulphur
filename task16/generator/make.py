"""task16 build: the simulated process, the pack under target/, the analysis, the checks, the golden deliverables,
figures.json, effort.json, submission.md, metadata.json and both zips.

    python3 make.py            builds in place
    python3 make.py --twice    builds twice into scratch folders and fails unless everything is byte-identical
"""
import filecmp
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)
os.environ.setdefault("OMP_NUM_THREADS", "1")

import checks as CK  # noqa: E402
import deliver as DL  # noqa: E402
import effort_passes as EP  # noqa: E402
import golden as GD  # noqa: E402
import pack as PK  # noqa: E402
import postprocess as PP  # noqa: E402
import results as RS  # noqa: E402
import world as WD  # noqa: E402
import writeup as WU  # noqa: E402

TITLE = "Quellstein Paket: which reason families the assistant keeps first through the 2026 peak season, and the resolution rate to expect"
COVERS = {
    "assistant": "the assistant platform's conversation export, 3 August to 8 November 2026 (weekly files stitched)",
    "calls": "the telephony platform's call legs, 3 August to 8 November 2026, in UTC",
    "chat": "the live chat tool's sessions, 3 August to 8 November 2026",
    "cases": "the case system's resolution extract: cases closed by 8 November 2026",
    "backlog": "the case team's weekly backlog report: open cases by queue, who raised them and days open at each Monday, and the weekly flow",
    "cons": "the network system's record of every consignment a contact referred to: depot, promised date, delivery, outcome class",
    "network": "the network's daily service record by depot: parcels due and how they ran",
    "plan": "workforce planning's season plan for 16 November 2026 to 3 January 2027: parcels, service levels, notification roll-out, adviser rota",
    "intents": "the assistant's intents and the reason family of each",
    "wrapup": "advisers' wrap-up codes and the reason family of each",
    "categories": "the case system's categories, queues and reason families",
    "standard": "KS-07, the contact service standard: contacts, resolution, the assistant-first rule",
    "release": "the release note of assistant version 3.0",
    "acd": "telephony's weekly summary of handled calls by queue",
    "csat": "responses to the post-contact survey, 3 August to 8 November 2026",
    "roster": "the adviser roster",
    "depots": "the depot list",
}


def metadata(target, counts):
    files = sorted(os.listdir(target))
    key_of = {v: k for k, v in PK.FILES.items()}
    return {
        "task": "task16", "title": TITLE,
        "domain": "Machine Learning Research, General Statistics & Data Science",
        "task_type": "data integration, record linkage and entity resolution",
        "objective": "Data Extraction & Conformation (ETL / Pipeline Build)", "as_of": "2026-11-09",
        "deliverables": [DL.WORKBOOK, DL.NOTE],
        "distractor_files": [PK.FILES[k] for k in PK.DISTRACTORS],
        "stated_inputs": ["75"],
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "categories": ["spreadsheet", "text"],
                        "largest_file": PK.FILES["cons"], "largest_file_rows": counts["cons"],
                        "long_file": PK.FILES["calls"], "long_file_rows": counts["calls"]},
        "sources": [{"files": "all files under target/",
                     "origin": "generated for this task by simulating the process that makes the files: parcels running on time or late by "
                               "depot and day, recipients contacting the carrier by how the parcel ran, unhelped customers coming back through "
                               "the assistant, live chat, the telephone line or a written case, the telephone line's IVR and queue, and the "
                               "case team's closing times. The carrier, its depots' figures, the standard and the people are invented.",
                     "date": "2026-11-11", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS[key_of[f]], "made": "written by task16/generator/make.py from the simulated process (deterministic)"}
                  for f in files],
    }


def build(task_dir, gen_out, prompt_path):
    target = os.path.join(task_dir, "target")
    golden = os.path.join(task_dir, "golden")
    shutil.rmtree(golden, ignore_errors=True)
    os.makedirs(gen_out, exist_ok=True)
    W = WD.build()
    counts = PK.write_all(W, target)
    O = RS.analyse(target)
    F = GD.assemble(O)
    E = EP.build(O, F)
    CK.run(W, O, F, E, target, prompt_path)
    bad = [r for r in CK.RESULTS if not r[1]]
    for name, ok, d in bad:
        print("FAIL", name, d)
    if bad:
        raise SystemExit("checks failed: %d of %d" % (len(bad), len(CK.RESULTS)))
    scratch = tempfile.mkdtemp(prefix="t16chart-")
    try:
        DL.write_all(F, golden, scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    with open(os.path.join(gen_out, "figures.json"), "w", encoding="utf-8") as fh:
        json.dump(F, fh, indent=1, ensure_ascii=False)
    with open(os.path.join(gen_out, "effort.json"), "w", encoding="utf-8") as fh:
        json.dump(E, fh, indent=1, ensure_ascii=False)
    WU.write(F, os.path.join(task_dir, "submission.md"))
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(metadata(target, counts), fh, indent=1, ensure_ascii=False)
    PP.own_mtimes(golden, {})
    PP.zip_folder(target, os.path.join(task_dir, "target.zip"), zone=PK.P.ZONE)
    PP.zip_folder(golden, os.path.join(task_dir, "golden.zip"), zone=PK.P.ZONE)
    return len(CK.RESULTS), counts


def same(a, b):
    out = []
    for root, _, names in os.walk(a):
        for n in sorted(names):
            pa = os.path.join(root, n); pb = os.path.join(b, os.path.relpath(pa, a))
            if not os.path.exists(pb) or not filecmp.cmp(pa, pb, shallow=False):
                out.append(os.path.relpath(pa, a))
    return out


if __name__ == "__main__":
    prompt = os.path.join(TASK, "prompt.txt")
    if "--twice" in sys.argv:
        a, b = tempfile.mkdtemp(prefix="t16a-"), tempfile.mkdtemp(prefix="t16b-")
        try:
            for d in (a, b):
                CK.RESULTS.clear()
                build(d, os.path.join(d, "generator"), prompt)
            diff = same(a, b) + same(b, a)
            print("two builds: %s" % ("byte-identical (%d files)" % sum(len(f) for _, _, f in os.walk(a)) if not diff else "DIFFER: %s" % sorted(set(diff))))
            sys.exit(1 if diff else 0)
        finally:
            shutil.rmtree(a, ignore_errors=True); shutil.rmtree(b, ignore_errors=True)
    n, counts = build(TASK, HERE, prompt)
    print("built: %d checks green; pack %s" % (n, counts))
