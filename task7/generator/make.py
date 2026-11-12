"""task7 architecture 10 build: the world, the pack under target/, the documents, the checks, the golden deliverables,
figures.json, effort.json, submission.md, metadata.json and both zips. `python3 make.py` builds in place;
`python3 make.py --twice` builds twice into scratch folders and fails unless the two packs, goldens and zips are
byte-identical."""
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
import pack as PK  # noqa: E402
import postprocess as PP  # noqa: E402
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

DISTRACTORS = ["ercot_residential_dr_potential_2025.pdf", "der_interconnections_2026.csv"]
COVERS = {
    "ami_15min_reads_peak_partners_2024_2026.csv": "the research sample's 15-minute reads, 13:00 to 21:00, on event days and quiet weekdays, 2024 to 2026",
    "member_accounts_2026.csv": "residential member accounts: service address, meter, meter type and exchanges, substation",
    "peak_partners_roster_2026-10-30.csv": "every thermostat ever enrolled in Peak Partners, its provider, account, channel, dates and swaps",
    "mv_event_assignments_2024_2026.csv": "the randomised halves of every test event",
    "peak_partners_event_log_2024_2026.xlsx": "every event called, 2024 to 2026, and each provider's event settings",
    "corvane_event_report_2024_2026.csv": "Corvane's event reports",
    "lumivale_dr_events_cedar_brake.csv": "Lumivale's event reports",
    "ardena_event_outcomes.csv": "Ardena's event reports",
    "ondera_events_cbec.csv": "Ondera's event reports",
    "kitebrook_events_2024_2026.csv": "Kitebrook's event reports",
    "pinecrest_home_events.csv": "Pinecrest Home's event reports",
    "ercot_4cp_intervals_2016_2026.csv": "ERCOT's 4CP intervals, 2016 to 2026",
    "weather_kcdr_hourly_2024_2026.csv": "hourly temperature at the KCDR station, June to September 2024 to 2026",
    "calder_cad_residential_2026.csv": "the Calder appraisal district's residential roll: situs, living area, year built",
    "provider_quotes_summer_2027.xlsx": "the six providers' quotes for summer 2027",
    "board_policy_412_demand_response_providers.pdf": "the board's policy on demand-response provider renewals",
    "transmission_charge_notice_2027.pdf": "the co-op's 2027 transmission charge per kW of 4CP load",
    "peak_partners_mv_plan_2024.pdf": "the programme's measurement and verification plan",
    "peak_partners_member_guide_2026.pdf": "the member and provider guide to an event",
    "ercot_residential_dr_potential_2025.pdf": "a research group's study of residential demand response potential in ERCOT",
    "der_interconnections_2026.csv": "members' interconnected rooftop solar systems",
}
UTC = dt.timezone.utc
EXPORTS = {
    "ami_15min_reads_peak_partners_2024_2026.csv": dt.datetime(2026, 11, 2, 7, 12, 41, tzinfo=UTC),
    "member_accounts_2026.csv": dt.datetime(2026, 11, 2, 7, 20, 3, tzinfo=UTC),
    "peak_partners_roster_2026-10-30.csv": dt.datetime(2026, 10, 30, 23, 2, 17, tzinfo=UTC),
    "mv_event_assignments_2024_2026.csv": dt.datetime(2026, 10, 1, 14, 45, 9, tzinfo=UTC),
    "corvane_event_report_2024_2026.csv": dt.datetime(2026, 10, 3, 2, 10, 55, tzinfo=UTC),
    "lumivale_dr_events_cedar_brake.csv": dt.datetime(2026, 10, 2, 16, 31, 12, tzinfo=UTC),
    "ardena_event_outcomes.csv": dt.datetime(2026, 10, 5, 20, 4, 38, tzinfo=UTC),
    "ondera_events_cbec.csv": dt.datetime(2026, 10, 6, 13, 22, 50, tzinfo=UTC),
    "kitebrook_events_2024_2026.csv": dt.datetime(2026, 10, 2, 9, 1, 27, tzinfo=UTC),
    "pinecrest_home_events.csv": dt.datetime(2026, 10, 7, 18, 47, 3, tzinfo=UTC),
    "ercot_4cp_intervals_2016_2026.csv": dt.datetime(2026, 10, 15, 21, 15, 0, tzinfo=UTC),
    "weather_kcdr_hourly_2024_2026.csv": dt.datetime(2026, 10, 1, 6, 44, 32, tzinfo=UTC),
    "calder_cad_residential_2026.csv": dt.datetime(2026, 8, 3, 15, 30, 11, tzinfo=UTC),
    "der_interconnections_2026.csv": dt.datetime(2026, 10, 27, 17, 8, 50, tzinfo=UTC),
}


def build(task_dir, gen_dir):
    target = os.path.join(task_dir, "target")
    golden = os.path.join(task_dir, "golden")
    for d in (target, golden):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    counts = PK.write_all(w, target)
    DC.write_all(target, w)
    CK.RESULTS.clear()
    C = CK.run(target)
    if os.environ.get("T7_CHECK_LOG"):
        with open(os.environ["T7_CHECK_LOG"], "w", encoding="utf-8") as fh:
            for name, ok, d in CK.RESULTS:
                fh.write("%s  %s  %s\n" % ("PASS" if ok else "FAIL", name, d))
    bad = [r for r in CK.RESULTS if not r[1]]
    if bad:
        for name, ok, d in bad:
            print("FAIL", name, d)
        raise SystemExit("checks failed: %d" % len(bad))
    scratch = tempfile.mkdtemp(prefix="t7chart-")
    try:
        F = DL.write_all(C, golden, gen_dir, scratch)
    finally:
        shutil.rmtree(scratch, ignore_errors=True)
    WU.write(F, os.path.join(task_dir, "submission.md"))
    files = sorted(os.listdir(target))
    meta = {
        "task": "task7", "title": "Cedar Brake Electric Cooperative: which thermostat providers to renew for summer 2027",
        "domain": "Energy Systems & Utilities", "task_type": "energy efficiency and demand response evaluation",
        "objective": "Experiment & Causal Analysis", "as_of": "2026-11-02",
        "deliverables": ["provider_renewals_2027_memo.docx", "provider_renewals_2027_workbook.xlsx"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "largest_file": "ami_15min_reads_peak_partners_2024_2026.csv", "largest_file_rows": counts["ami_rows"],
                        "long_file": "corvane_event_report_2024_2026.csv",
                        "long_file_rows": counts["reports"]["Corvane"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task around a fictional Texas electric cooperative, its members, its "
                               "thermostat providers, a fictional appraisal district and weather station; every record "
                               "and figure is invented", "date": "2026-11-02", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS.get(f, ""), "made": "constructed by task7/generator/make.py (seeded, deterministic)"}
                  for f in files],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
    PP.own_mtimes(target, EXPORTS)
    PP.own_mtimes(golden, {})
    PP.zip_folder(target, os.path.join(task_dir, "target.zip"), zone="America/Chicago")
    PP.zip_folder(golden, os.path.join(task_dir, "golden.zip"), zone="America/Chicago")
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
            r = tempfile.mkdtemp(prefix="t7build%d-" % k)
            gen = os.path.join(r, "generator")
            os.makedirs(gen)
            build(r, gen)
            roots.append(r)
        ok = True
        for part in ("target", "golden"):
            same, why = same_tree(os.path.join(roots[0], part), os.path.join(roots[1], part))
            print("%s %s" % ("SAME" if same else "DIFF", part), "" if same else why)
            ok &= same
        for f in ("target.zip", "golden.zip", "submission.md", "metadata.json", "generator/figures.json"):
            same = filecmp.cmp(os.path.join(roots[0], f), os.path.join(roots[1], f), shallow=False)
            print("%s %s" % ("SAME" if same else "DIFF", f))
            ok &= same
        for r in roots:
            shutil.rmtree(r, ignore_errors=True)
        sys.exit(0 if ok else 1)
    F, C, counts = build(TASK, HERE)
    print(json.dumps(counts, indent=1))
    print("renewed %s; kW %s; lines %s; careful %s -> %s; MW %.2f net %s; n27 %s" % (
        F["renewed"], F["kw"], F["bar_kw"], F["care_kw"], F["care_set"], F["mw"], F["net_usd"], F["n27"]))
    print("%d checks passed" % len(CK.RESULTS))


if __name__ == "__main__":
    main()
