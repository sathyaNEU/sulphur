"""task7 architecture 7 build: the world, the pack under target/, the documents, the checks, the golden deliverables, figures.json,
submission.md, metadata.json and both zips. `python3 make.py` builds in place; `python3 make.py --twice` builds twice
into scratch folders and fails unless the two packs, goldens and zips are byte-identical."""
import filecmp
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import zipfile

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

ZIP_TIME = (2026, 6, 24, 17, 20, 0)
DISTRACTORS = ["electricity_customers_annual_2019_2025.csv", "solar_cadastre_rooftops_2024.xlsx",
               "municipal_heat_plan_2026_summary.pdf", "federal_funding_overview_2025.pdf"]
COVERS = {
    "gas_meter_reads_2013_2026.csv": "every read of every commercial gas meter point, 30 April 2013 to 30 April 2026",
    "meter_points_2026.csv": "meter points, their buildings, meters, factors, z-numbers and network areas",
    "calorific_values_2013_2026.csv": "the billing calorific value by network area and season",
    "buildings_register_2026.xlsx": "commercial buildings supplied with gas: address, district, use, floor area",
    "benchmarking_notices_2019_2026.csv": "every benchmarking notice sent, May 2019 to May 2026, with the grant offer",
    "pilot_2019_responses_and_draw.xlsx": "the 2019 pilot's responses, the draw, withdrawals and completion dates",
    "applications_2026.xlsx": "the 2026 round's applications received by 12 June, with their reference consumption",
    "weather_haldenau_daily_2013_2026.csv": "the Haldenau station's daily mean temperature",
    "degree_days_haldenau.csv": "monthly G20/15 degree days by season and the 1991 to 2020 means",
    "climate_action_plan_2023_extract.pdf": "the climate action plan's section on efficiency grants",
    "pilot_2019_rules.pdf": "the terms of the 2019 pilot",
    "benchmarking_method_2022.pdf": "the utility's benchmarking method",
    "committee_request_2026-06-15.docx": "the committee chair's request for the 2026 round",
    "grant_offer_2026_terms.pdf": "the terms of the 2026 grant offer",
    "electricity_customers_annual_2019_2025.csv": "the utility's commercial electricity customers' annual use",
    "solar_cadastre_rooftops_2024.xlsx": "rooftop solar potential by address",
    "municipal_heat_plan_2026_summary.pdf": "the municipal heat plan's summary",
    "federal_funding_overview_2025.pdf": "the regional energy agency's overview of federal grants",
}


UTC = dt.timezone.utc
EXPORTS = {  # the systems' exports, each written when its job ran (UTC)
    "gas_meter_reads_2013_2026.csv": dt.datetime(2026, 6, 15, 5, 12, 41, tzinfo=UTC),
    "meter_points_2026.csv": dt.datetime(2026, 6, 15, 5, 14, 3, tzinfo=UTC),
    "calorific_values_2013_2026.csv": dt.datetime(2026, 6, 12, 13, 2, 17, tzinfo=UTC),
    "benchmarking_notices_2019_2026.csv": dt.datetime(2026, 6, 15, 5, 20, 55, tzinfo=UTC),
    "degree_days_haldenau.csv": dt.datetime(2026, 6, 3, 6, 45, 9, tzinfo=UTC),
    "weather_haldenau_daily_2013_2026.csv": dt.datetime(2026, 6, 3, 6, 44, 32, tzinfo=UTC),
    "electricity_customers_annual_2019_2025.csv": dt.datetime(2026, 6, 12, 14, 31, 50, tzinfo=UTC),
}


def zip_dir(src, path, names=None):
    names = sorted(names or os.listdir(src))
    with zipfile.ZipFile(path, "w") as z:
        for n in names:
            zi = zipfile.ZipInfo(n, date_time=ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            with open(os.path.join(src, n), "rb") as fh:
                z.writestr(zi, fh.read())


def build(task_dir, gen_dir):
    target = os.path.join(task_dir, "target")
    golden = os.path.join(task_dir, "golden")
    for d in (target, golden):
        shutil.rmtree(d, ignore_errors=True)
        os.makedirs(d)
    w = W.build()
    P, counts = PK.write_all(w, target)
    DC.write_all(target, w)
    CK.RESULTS.clear()
    C = CK.run(target, gen_dir)
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
        "task": "task7", "title": "Stadtwerke Haldenau: which retrofit measures the 2026 grant round funds, and what it will pay",
        "domain": "Energy Systems & Utilities", "task_type": "energy efficiency and demand response evaluation",
        "objective": "Experiment & Causal Analysis", "as_of": "2026-06-15",
        "deliverables": ["grant_round_2026_note.docx", "grant_round_2026_appraisal.xlsx"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "largest_file": "gas_meter_reads_2013_2026.csv", "largest_file_rows": counts["reads"],
                        "long_file": "benchmarking_notices_2019_2026.csv", "long_file_rows": counts["notices"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task around a fictional German municipal utility, its commercial gas "
                               "customers, the city's retrofit grants and its weather station; every record and figure is "
                               "invented",
                     "date": "2026-06-24", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS.get(f, ""), "made": "constructed by task7/generator/make.py (seeded, deterministic)"}
                  for f in files],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
    # every file's own save time: the Office files and PDFs from their own stamps, the system exports when they ran
    PP.own_mtimes(target, EXPORTS)
    PP.own_mtimes(golden, {})
    PP.zip_folder(target, os.path.join(task_dir, "target.zip"), zone="Europe/Berlin")
    PP.zip_folder(golden, os.path.join(task_dir, "golden.zip"), zone="Europe/Berlin")
    return F, C, counts


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False, (cmp.left_only, cmp.right_only, cmp.diff_files)
    return True, None


def main():
    if "--twice" in sys.argv:
        roots = []
        for n in (1, 2):
            r = tempfile.mkdtemp(prefix="t7build%d-" % n)
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
    print("funded %s; eur/t %s; ranges %s; flip %s; rates %s; life %s; at close paid %s million; 2025/26 %s t"
          % (F["funded"], F["R5_eur_per_tonne"], F["R6_range_eur"], F["R6_break_even_pct"],
             F["R4_rate_on_applications_pct"], F["R2_life_saving_pct"], F["R7_funded_paid_million"], F["R8_tonnes"]))
    print("%d checks passed" % len(CK.RESULTS))


if __name__ == "__main__":
    main()
