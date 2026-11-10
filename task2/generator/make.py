"""task2 architecture 6: build the pack, run the checks, write the goldens, submission.md, metadata.json and both
zips. `python3 make.py` builds in place; `python3 make.py --twice` builds twice in scratch folders and compares."""
import datetime as dt
import filecmp
import json
import os
import shutil
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import checks as CK  # noqa: E402
import deliver as DL  # noqa: E402
import docs as DC  # noqa: E402
import effort_passes as EP  # noqa: E402
import pack as PK  # noqa: E402
import postprocess as PP  # noqa: E402
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

DISTRACTORS = ["support_tickets_2024_2026.csv", "headset_inventory_2026.xlsx", "ehr_integration_uptime_2026.xlsx"]
COVERS = {
    "dictation_audits_2023_2026.csv": "every audited dictation at the group's hospitals, January 2023 to December 2026",
    "dictation_volumes_2022_2026.csv": "each clinician's dictations by month, January 2022 to December 2026",
    "clinician_register_2026.xlsx": "the group's HR register of medical and advanced practice posts held since 1 January 2022",
    "shannonside_dictation_rollout_2027.xlsx": "the group's 2027 go-live plan for its two teaching hospitals",
    "quality_reports_2023_2026.xlsx": "Larkmoor's quarterly quality reports to the group",
    "services_agreement_schedule2_deployment.pdf": "the services agreement's deployment schedule (amendment 4)",
    "QA-07_recognition_quality_audit.pdf": "Larkmoor's recognition quality audit procedure",
    "recognition_releases_2023_2026.pdf": "Larkmoor's recognition release notes",
    "service_notice_SN-2026-14.pdf": "Larkmoor's notice of the 2027 Dublin migration",
    "draft_schedule4_quality_2027.docx": "the group's draft 2027 quality schedule",
    "support_tickets_2024_2026.csv": "the service desk's tickets from the group's clinicians",
    "headset_inventory_2026.xlsx": "headsets issued to clinicians",
    "ehr_integration_uptime_2026.xlsx": "monthly availability of the EHR integration by site",
}
UTC = dt.timezone.utc
EXPORTS = {  # the systems' exports, each written when its job ran (UTC)
    "dictation_audits_2023_2026.csv": dt.datetime(2027, 1, 8, 6, 14, 22, tzinfo=UTC),
    "dictation_volumes_2022_2026.csv": dt.datetime(2027, 1, 8, 6, 31, 7, tzinfo=UTC),
    "support_tickets_2024_2026.csv": dt.datetime(2027, 1, 7, 17, 2, 45, tzinfo=UTC),
}


def build(task_dir, gen_dir):
    target = os.path.join(task_dir, "target")
    golden = os.path.join(task_dir, "golden")
    for d in (target, golden):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    W.records(w)
    counts = PK.write_all(w, target)
    DC.write_all(target)
    CK.RESULTS.clear()
    C = CK.run(target, gen_dir, w)
    bad = [r for r in CK.RESULTS if not r[1]]
    if bad:
        for name, ok, d in bad:
            print("FAIL", name, d)
        raise SystemExit("checks failed: %d" % len(bad))
    scratch = tempfile.mkdtemp(prefix="t2chart-")
    try:
        F = DL.write_all(C, golden, gen_dir, scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    EP.write(C, F, gen_dir)
    WU.write(F, os.path.join(task_dir, "submission.md"))
    files = sorted(os.listdir(target))
    meta = {
        "task": "task2", "title": "Larkmoor Speech: the heavy-correction ceiling for Shannonside Hospital Group's 2027 schedule",
        "domain": "General Statistics & Data Science", "task_type": "robustness analysis",
        "objective": "Descriptive & Distribution Analysis", "as_of": "2027-01-11",
        "deliverables": ["quality_schedule_2027_ceiling.pdf", "heavy_correction_2027.xlsx"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "largest_file": "dictation_volumes_2022_2026.csv", "largest_file_rows": counts["volumes"],
                        "long_file": "dictation_audits_2023_2026.csv", "long_file_rows": counts["audits"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task around a fictional Irish medical speech-recognition vendor and a "
                               "fictional hospital group; every record and figure is invented",
                     "date": "2027-01-12", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS.get(f, ""), "made": "constructed by task2/generator/make.py (seeded, deterministic)"}
                  for f in files],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
    PP.own_mtimes(target, EXPORTS)
    PP.own_mtimes(golden, {})
    PP.zip_folder(target, os.path.join(task_dir, "target.zip"), zone="Europe/Dublin")
    PP.zip_folder(golden, os.path.join(task_dir, "golden.zip"), zone="Europe/Dublin")
    return F, C, counts


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False, (cmp.left_only, cmp.right_only, cmp.diff_files)
    return True, None


def main():
    if "--twice" in sys.argv:
        roots = []
        for k in (1, 2):
            r = tempfile.mkdtemp(prefix="t2build%d-" % k)
            gen = os.path.join(r, "generator")
            os.makedirs(gen)
            build(r, gen)
            roots.append(r)
        ok = True
        for part in ("target", "golden"):
            same, why = same_tree(os.path.join(roots[0], part), os.path.join(roots[1], part))
            print("%s %s" % ("SAME" if same else "DIFF", part), "" if same else why)
            ok &= same
        for f in ("target.zip", "golden.zip", "submission.md", "metadata.json", "generator/figures.json",
                  "generator/effort.json"):
            same = filecmp.cmp(os.path.join(roots[0], f), os.path.join(roots[1], f), shallow=False)
            print("%s %s" % ("SAME" if same else "DIFF", f))
            ok &= same
        for r in roots:
            shutil.rmtree(r, ignore_errors=True)
        sys.exit(0 if ok else 1)
    F, C, counts = build(TASK, HERE)
    print(json.dumps(counts, indent=1))
    r = F["results"]
    print("ceiling %s; lowest ceilings %s; quarters %s; univ Q4 %s; BKU Q4 dictations %s; p90 %s; bridge %s"
          % (r["r9_ceiling"], r["r7_lowest_ceilings"], F["evidence"]["quarters_1dp"], r["r6_univ_q4_share"],
             r["r5_bku_q4_dictations"], r["r8_p90_q4"], r["r2_bridge_split"]))
    print("%d checks passed" % len(CK.RESULTS))


if __name__ == "__main__":
    main()
