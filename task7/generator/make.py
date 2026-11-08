"""task7 build: the world, the pack under target/, the documents, the checks, the golden deliverables, figures.json,
submission.md, metadata.json and both zips. `python3 make.py` builds in place; `python3 make.py --twice` builds twice
into scratch folders and fails unless the two packs, goldens and zips are byte-identical."""
import filecmp
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
import world as W  # noqa: E402
import writeup as WU  # noqa: E402

ZIP_TIME = (2027, 1, 13, 18, 40, 0)
DISTRACTORS = ["rent_roll_2026-12.csv", "buildings_insurance_register_2026.xlsx", "irish_cre_outlook_2027.pdf",
               "cre_concentration_report_2026Q3.pdf"]
COVERS = {
    "dw_fact_loan_month_end_2022_2026.csv": "the warehouse's month-end facility fact, January 2022 to December 2026",
    "dw_dim_property_valuation_2004_2026.csv": "every valuation the warehouse holds for each property, as type 2 rows",
    "dw_dim_property_2026-12.csv": "the property dimension at December 2026",
    "dw_bridge_facility_security_2026-12.csv": "which properties secure which facilities, with effective dates",
    "facility_register_2026-12.xlsx": "facilities since 2012 with their earlier numbers, and customers",
    "default_register_2012_2026.csv": "defaults recorded since the warehouse went live in 2012",
    "receiver_sales_2012_2026.csv": "receivers' sales of security after default",
    "recovery_postings_2012_2027.csv": "sale proceeds and costs posted to defaulted facilities",
    "brackley_rowe_cre_index_2004_2026.csv": "the commercial property index by sector and region, every release",
    "ardcarn_credit_risk_policy_part4_2025.pdf": "credit risk policy, measurement: master scale, default, ECL, valuations",
    "cre_lgd_model_documentation_2025.pdf": "the commercial property LGD model and its back-test",
    "plan_2027_credit_loss_request.pdf": "the chief financial officer's request for the 2027 plan line",
    "rent_roll_2026-12.csv": "tenancies of the investment properties at December 2026",
    "buildings_insurance_register_2026.xlsx": "buildings insurance cover on the security",
    "irish_cre_outlook_2027.pdf": "a research house's 2027 outlook for Irish commercial property",
    "cre_concentration_report_2026Q3.pdf": "the September 2026 concentration report",
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
    DC.write_all(target, P)
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
        "task": "task7", "title": "Ardcarn Bank: 2027 plan credit loss on commercial property lending",
        "domain": "Banking, Credit & Financial Risk", "task_type": "expected credit loss provisioning",
        "objective": "Forecasting & Predictive Modeling", "as_of": "2027-01-15",
        "deliverables": ["exco_cre_credit_loss_2027.pptx", "cre_expected_loss_2027_by_loan.csv"],
        "distractor_files": DISTRACTORS,
        "input_gates": {"files": len(files), "formats": sorted({os.path.splitext(f)[1][1:] for f in files}),
                        "largest_file": "dw_fact_loan_month_end_2022_2026.csv",
                        "largest_file_rows": C["n_fact"], "long_file": "dw_dim_property_valuation_2004_2026.csv",
                        "long_file_rows": C["n_val"]},
        "sources": [{"files": "all files under target/",
                     "origin": "constructed for this task around a fictional Irish commercial property lender, its "
                               "customers, properties, valuers and index publisher; every record and figure is invented",
                     "date": "2027-01-13", "license": "CC BY 4.0 (original work)"}],
        "files": [{"path": f, "format": os.path.splitext(f)[1][1:], "bytes": os.path.getsize(os.path.join(target, f)),
                   "covers": COVERS.get(f, ""), "made": "constructed by task7/generator/make.py (seeded, deterministic)"}
                  for f in files],
    }
    with open(os.path.join(task_dir, "metadata.json"), "w", encoding="utf-8") as fh:
        json.dump(meta, fh, indent=1, ensure_ascii=False)
    zip_dir(target, os.path.join(task_dir, "target.zip"))
    zip_dir(golden, os.path.join(task_dir, "golden.zip"))
    return F, C, counts


def same_tree(a, b):
    cmp = filecmp.dircmp(a, b)
    if cmp.left_only or cmp.right_only or cmp.diff_files or cmp.funny_files:
        return False, (cmp.left_only, cmp.right_only, cmp.diff_files)
    for sub in cmp.common_dirs:
        ok, why = same_tree(os.path.join(a, sub), os.path.join(b, sub))
        if not ok:
            return ok, why
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
    print("plan %s, investment %s, owner-occupied %s, five %s" % (
        F["call"]["plan_figure_display"], F["asks"]["investment_display"], F["asks"]["owner_occupied_display"],
        F["asks"]["five_facilities"]))
    print("%d checks passed" % len(CK.RESULTS))


if __name__ == "__main__":
    main()
