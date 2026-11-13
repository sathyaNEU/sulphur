"""task7 architecture 11 build: the world, the pack under target/, the documents, the checks, the golden deliverables,
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

DISTRACTORS = ["state_ev_registrations_by_zip_2019-2026.csv", "net_metering_interconnections_2026.csv"]
COVERS = {
    "mdm_hourly_phw_2026-07-01_2026-08-31.csv": "hourly net kWh for every meter on the Prairie Hollow substation, July and August 2026",
    "mdm_hourly_lkr_2026-07-01_2026-08-31.csv": "hourly net kWh for every meter on the Larkin Ridge substation, July and August 2026",
    "mdm_hourly_stb_2026-07-01_2026-08-31.csv": "hourly net kWh for every meter on the Stonebrook substation, July and August 2026",
    "quillpoint_sessions_2024-06_2026-09.csv": "every enrolled charger's charging sessions, June to September 2024 to 2026, in UTC",
    "ev_overnight_roster_2026-11-02.csv": "every charger ever enrolled on the EV Overnight rate, with swaps and closures",
    "pilot_assignment_2025.csv": "each charger's half of the managed-charging pilot",
    "gis_service_points_2026-10-30.csv": "each service point's meter, address and transformer location",
    "ami_meter_exchanges_2026.csv": "meters exchanged in 2026",
    "transformer_register_2026.csv": "the distribution transformer register",
    "distribution_work_orders_2025_2026.xlsx": "completed distribution work orders, 2025 and 2026",
    "transformer_monitors_15min_2026-07_08.csv": "15-minute kW and kVA on the 48 monitored transformers, July and August 2026",
    "weather_station_hourly_2024-2026.csv": "hourly temperature and humidity at the association's station, June to September",
    "quillpoint_proposal_2027.xlsx": "the charging platform's 2027 products and fees",
    "board_policy_EV-4_charging_default.pdf": "the board's policy for choosing the EV Overnight charging default",
    "dps-7_distribution_transformer_loading.pdf": "the planning standard for transformer limits and replacement costs",
    "ev_overnight_pilot_plan_2025.pdf": "the managed-charging pilot's plan",
    "rate_schedule_EV-1_2026.pdf": "the EV Overnight rate",
    "state_ev_registrations_by_zip_2019-2026.csv": "the state's quarterly EV registrations by ZIP code",
    "net_metering_interconnections_2026.csv": "members' net-metered rooftop solar systems",
}
UTC = dt.timezone.utc
EXPORTS = {
    "mdm_hourly_phw_2026-07-01_2026-08-31.csv": dt.datetime(2026, 11, 3, 14, 12, 41, tzinfo=UTC),
    "mdm_hourly_lkr_2026-07-01_2026-08-31.csv": dt.datetime(2026, 11, 3, 14, 19, 8, tzinfo=UTC),
    "mdm_hourly_stb_2026-07-01_2026-08-31.csv": dt.datetime(2026, 11, 3, 14, 27, 55, tzinfo=UTC),
    "quillpoint_sessions_2024-06_2026-09.csv": dt.datetime(2026, 10, 2, 9, 4, 17, tzinfo=UTC),
    "ev_overnight_roster_2026-11-02.csv": dt.datetime(2026, 11, 2, 15, 41, 3, tzinfo=UTC),
    "pilot_assignment_2025.csv": dt.datetime(2026, 10, 2, 9, 6, 50, tzinfo=UTC),
    "gis_service_points_2026-10-30.csv": dt.datetime(2026, 10, 30, 22, 15, 29, tzinfo=UTC),
    "ami_meter_exchanges_2026.csv": dt.datetime(2026, 11, 2, 16, 2, 11, tzinfo=UTC),
    "transformer_register_2026.csv": dt.datetime(2026, 10, 1, 13, 30, 2, tzinfo=UTC),
    "transformer_monitors_15min_2026-07_08.csv": dt.datetime(2026, 9, 8, 18, 44, 36, tzinfo=UTC),
    "weather_station_hourly_2024-2026.csv": dt.datetime(2026, 10, 5, 12, 0, 9, tzinfo=UTC),
    "state_ev_registrations_by_zip_2019-2026.csv": dt.datetime(2026, 10, 20, 17, 25, 0, tzinfo=UTC),
    "net_metering_interconnections_2026.csv": dt.datetime(2026, 10, 27, 20, 8, 50, tzinfo=UTC),
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
    C = CK.run(target, w)
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
        "task": "task7", "title": "Hollins Creek Electric Association: the EV Overnight rate's charging default for 2027",
        "domain": "Energy Systems & Utilities", "task_type": "energy efficiency and demand response evaluation",
        "objective": "Experiment & Causal Analysis", "as_of": "2026-11-06",
        "deliverables": ["ev_overnight_default_2027_memo.docx", "ev_overnight_transformers_2027.csv"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "largest_file": "quillpoint_sessions_2024-06_2026-09.csv", "largest_file_rows": counts["sessions"],
                        "long_file": "mdm_hourly_stb_2026-07-01_2026-08-31.csv",
                        "long_file_rows": counts["mdm_hourly_stb_2026-07-01_2026-08-31.csv"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task around a fictional Colorado electric cooperative, its members, its "
                               "charging platform, its network and its weather station; every record and figure is invented",
                     "date": "2026-11-06", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS.get(f, ""), "made": "constructed by task7/generator/make.py (seeded, deterministic)"}
                  for f in files],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
    PP.own_mtimes(target, EXPORTS)
    PP.own_mtimes(golden, {"ev_overnight_transformers_2027.csv": dt.datetime(2026, 11, 12, 22, 31, 4, tzinfo=UTC)})
    PP.zip_folder(target, os.path.join(task_dir, "target.zip"), zone="America/Denver")
    PP.zip_folder(golden, os.path.join(task_dir, "golden.zip"), zone="America/Denver")
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
    print("call %s; over own %s stagger %s sequence %s; totals %s %s %s; flip %s; pilot %s; chargers %s; transformers %s" % (
        F["call"], F["own"]["over"], F["stagger"]["over"], F["sequence"]["over"], F["own"]["total"], F["stagger"]["total"],
        F["sequence"]["total"], F["flip_fee"], F["pilot_effect"], F["n_chargers"], F["n_tx"]))
    print("%d checks passed" % len(CK.RESULTS))


if __name__ == "__main__":
    main()
