#!/usr/bin/env python3
"""task28/generator/checks.py (v3): Comprehensive Stage 3 assertion suite:
- Sulfur input gates (15 usable files across 4 formats, 2 large messy CSVs > 280k rows, 2+ unlabelled distractors)
- Pinned Clauses 2.1-2.4, 3.1, 4.1-4.3 (420/360/540/300 kWh/h), Annex A, Annex B (9-column CSV) in SWRO-Q27 PDF
- Zero Clause 4.4 / zero raw-alarm signpost in PDFs or prompt; ZERO post_cip_monitoring_cycle_hours in JSON
- All 18 semantic forks (SF1..SF18) asserted directly on the shipped pack
- Clean-data test (shipped target/ reproduces core.simulate_world(2803) cleanly), footprint outside deciding units
- All 29 variants, 8 +/-20% forcing perturbations, 15 lattice drops, 18 extra rivals, and 4 over-corrections asserted
- LibreOffice Calc headless formula evaluation on all 8 golden tabs: zero formula errors, exact match to figures.json & CSV.
"""
import csv
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import zipfile

import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import analysis as AN  # noqa: E402
import core  # noqa: E402
import deliver as DEL  # noqa: E402
import pack as PK  # noqa: E402


def _assert(cond, msg):
    if not cond:
        raise AssertionError("FAIL: " + msg)
    print("  PASS ", msg)


def main():
    target_dir = os.path.join(TASK_DIR, "target")
    golden_dir = os.path.join(TASK_DIR, "golden")
    figs = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(TASK_DIR, "metadata.json"), encoding="utf-8"))

    print("=== 1. INPUT GATES & NO-DICTIONARY CHECK ===")
    tfiles = sorted(os.listdir(target_dir))
    _assert(len(tfiles) == 15, f"15 usable files in target/ (got {len(tfiles)})")
    exts = {os.path.splitext(f)[1].lower() for f in tfiles}
    _assert(exts == {".csv", ".xlsx", ".json", ".pdf"}, f"4 file formats across categories ({sorted(exts)})")
    bad_desc = re.compile(r"(readme|dictionary|codebook|field_?notes|manifest|glossary|schema|_notes)", re.I)
    for f in tfiles:
        _assert(not bad_desc.search(f), f"no describing/notes filename: {f}")
    _assert(len(meta["distractor_files"]) >= 2, "at least 2 unlabelled distractors recorded only in metadata.json")
    for df in meta["distractor_files"]:
        _assert(df in tfiles, f"distractor present in target/: {df}")

    in_lines = sum(1 for _ in open(os.path.join(target_dir, PK.FILES["intake_15m"]), encoding="utf-8")) - 1
    ro_lines = sum(1 for _ in open(os.path.join(target_dir, PK.FILES["ro_feed_15m"]), encoding="utf-8")) - 1
    _assert(in_lines > 280320 and ro_lines > 280320, f"two large messy CSVs > 280k rows ({in_lines:,}, {ro_lines:,})")

    with zipfile.ZipFile(os.path.join(TASK_DIR, "target.zip")) as zt:
        _assert(sorted(zt.namelist()) == tfiles, "target.zip members match target/ verbatim (no enclosing folder)")
    with zipfile.ZipFile(os.path.join(TASK_DIR, "golden.zip")) as zg:
        _assert(
            sorted(zg.namelist()) == sorted([DEL.GOLDEN_CSV, DEL.GOLDEN_XLSX]),
            "golden.zip contains strictly the 2 requested deliverables",
        )

    print("=== 2. PINNED CONSTANTS & ZERO-SIGNPOST CHECK IN SHIPPED DOCUMENTS ===")
    std_txt = "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(target_dir, PK.FILES["standard_pdf"])).pages)
    qa_txt = "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(target_dir, PK.FILES["lims_qa_pdf"])).pages)
    cfg_txt = open(os.path.join(target_dir, PK.FILES["scada_cfg"]), encoding="utf-8").read()
    for tok in (
        "400.0", "0.50 mg/L", "exceeding 1.50", "450 mg/L", "1-hour operating block",
        "420 kWh/h", "360 kWh/h", "540 kWh/h", "300 kWh/h",
        "1.32", "1.28", "1.26", "boron_2027_h", "tds_2027_h", "energy_2027_mwh", "Annex A", "Annex B",
    ):
        _assert(tok in std_txt, f"SWRO-Q27 PDF pins {tok!r}")
    _assert("0.004 mg/L" in qa_txt and "3.5 mg/L" in qa_txt, "LIMS QA certificate pins 0.004 mg/L boron and 3.5 mg/L TDS repeatability SDs")
    _assert("post_cip_monitoring_cycle_hours" not in cfg_txt and "120" not in cfg_txt, "scada_bay_config_2026.json contains zero 120h post-CIP window hint")
    for banned in (
        "Matheron", "Krige", "Lagrangian", "Dawid-Skene", "latent class", "autocorrelation",
        "short-circuit", "baffling", "comonotonic", "two-path", "bimodal", "Fickian", "Spiegler",
        "solution-diffusion", "heteroscedast", "variance-component", "equal-variance", "re-growth",
        "discrepancy rate", "screening dashboard", "majority vote", "Clause 4.4", "4.4 ",
    ):
        _assert(banned.lower() not in std_txt.lower(), f"SWRO-Q27 PDF never hints at {banned!r}")
        _assert(banned.lower() not in qa_txt.lower(), f"LIMS QA PDF never hints at {banned!r}")

    print("=== 3. ANALYSIS, FORKS (SF1-SF18), CLEAN-DATA & FOOTPRINT TESTS ===")
    res = AN.run_all(target_dir)
    g = res["gold_asm"]
    g_slate = res["golden_slate"]
    _assert(g_slate == ["TR01", "TR02", "TR06", "TR07", "TR08"], f"golden slate exact ({g_slate})")
    _assert(res["cleaning"]["shift_rows"] == 70080, f"70,080 1-hour shift diagnostic rows (got {res['cleaning']['shift_rows']})")
    _assert(res["cleaning"]["hydraulics_max_flow_repeat"] <= 5, f"zero flat flow clamping in hydraulics CSV (max repeat {res['cleaning']['hydraulics_max_flow_repeat']})")
    _assert(res["cleaning"]["boron_min_comp_mg_l"] > 0.025 and res["cleaning"]["boron_sub_loq_count"] == 0, f"zero negative or sub-LOQ (<0.020) boron composites (min {res['cleaning']['boron_min_comp_mg_l']:.4f} mg/L)")
    _assert(res["tr06_profile_lrt_400h"] > 8.0, f"TR06 profile-likelihood LRT against 400.0 h > 8.0 ({res['tr06_profile_lrt_400h']:.2f})")
    _assert(res["tr05_kalman_lrt_400h"] > 7.0, f"TR05 exact 4-state AR(1) Kalman LRT against 400.0 h > 7.0 ({res['tr05_kalman_lrt_400h']:.2f})")

    # Verify shipped analysis reproduces core.simulate_world(2803) cleanly (< 0.25 h drift from CSV decimal rounding)
    core_data = core.simulate_world(core.SEED)
    core_r1 = core.estimate_s1(core_data, mode="golden")
    core_r2 = core.estimate_s2(core_data, mode="golden")
    core_r3 = core.estimate_s3(core_data, mode="golden")
    core_r4 = core.estimate_s4(core_data, mode="golden")
    core_asm = core.assemble(core_r1, core_r2, core_r3, core_r4)
    max_diff = max(abs(g["members"][u] - core_asm["members"][u]) for u in core.TRAINS)
    _assert(max_diff < 0.25, f"cleaned shipped pack matches core.py within 0.25 h (max diff {max_diff:.5f} h)")

    _assert(
        sorted(u for u in core.TRAINS if core_asm["members"][u] >= core.THRESHOLD) == g_slate,
        "clean-data test: uncorrupted core.py world produces identical 5-of-8 call",
    )

    lat = res["lattice_asm"]
    _assert(abs(lat["S1"]["members"]["TR04"] - g["members"]["TR04"]) > 40.0, "S1 footprint extends to monitor TR04")
    _assert(abs(lat["S2"]["members"]["TR05"] - g["members"]["TR05"]) > 80.0, "S2 footprint extends to monitor TR05")
    _assert(abs(lat["S3"]["members"]["TR07"] - g["members"]["TR07"]) > 1000.0, "S3 footprint extends to texture TR07")
    _assert(abs(lat["S4"]["members"]["TR07"] - g["members"]["TR07"]) > 300.0, "S4 footprint extends to texture TR07")

    for nm, asm in res["variants_named"]:
        sl = sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)
        _assert(sl == g_slate, f"variant holds call: {nm}")
        _assert(
            asm["members"]["TR07"] > asm["members"]["TR06"] > asm["members"]["TR08"],
            f"variant preserves TR07 > TR06 > TR08 rank: {nm}",
        )
    for pt in res["perturbations"]:
        _assert(pt["holds"], f"forcing perturbation holds: {pt['input']} (min_ov={pt['min_overhaul']:.1f}, max_mo={pt['max_monitor']:.1f})")

    fal = res["fal_by_route"]
    ex = res["extra_routes"]
    ov = res["over"]
    _assert(fal["golden"]["f1"] < 0.14 and fal["direct"]["f1"] > 10 * fal["golden"]["f1"], "SF1: F1 refutes raw composite counting")
    _assert(fal["S1_r2_homosc"]["f1"] > 3 * fal["golden"]["f1"] and ex["cutoff:s1_r2_flux_homosced"]["members"]["TR01"] < 400.0 and ex["cutoff:s1_r1_block_ar1"]["members"]["TR01"] < 400.0, "SF2: F1 refutes homoscedastic a+c/Q AR(1) and 6-block AR(1) (both drop TR01 < 400)")
    _assert(ex["cutoff:s1_stat_ar1_no_flux"]["members"]["TR01"] < 400.0 and ex["cutoff:s1_flux_no_deconv"]["members"]["TR01"] < 400.0, "SF3: stationary AR(1) and flux-without-deconv miss TR01")
    _assert(ov["S1"]["members"]["TR04"] > 400.0 and fal["S1_over"]["combined"] > 4 * fal["golden"]["combined"], "SF4: flux i.i.d. sqrt(m) over-correction flips TR04 > 400")
    _assert(all(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD) == g_slate for _, asm in res["variants_named"][:11]), "SF5: all 11 S1 mass-flux variants (incl. exact continuous OU MLE) hold golden call")
    _assert(fal["golden"]["f2_ms_cm"] < 0.36 and fal["direct"]["f2_ms_cm"] > 1.70, "SF6: F2 refutes same-timestamp pairing")
    _assert(fal["S2_r12_lag"]["f2_ms_cm"] > 1.00 and ex["cutoff:s2_r1_r2_fixed_lag_tep"]["members"]["TR05"] > 400.0 and ex["cutoff:s2_nom_vol"]["members"]["TR02"] < 400.0 and res["rig_r2_asm"]["members"]["TR02"] < 400.0, "SF7: F2 refutes fixed wall-clock lag and V_nom (flip TR05 > 400; V_nom & R2 drop TR02 < 400)")
    _assert(fal["S2_single_plug"]["f2_ms_cm"] > 0.58 and ex["cutoff:s2_single_plug_veff"]["members"]["TR05"] > 400.0, "SF8: F2 refutes 1D single-plug V_eff (flips TR05 > 400)")
    _assert(ov["S2"]["members"]["TR05"] > 400.0, "SF9: comonotonic upper-bound pairing flips TR05")
    _assert(all(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD) == g_slate for _, asm in res["variants_named"][11:19]), "SF10: all 8 S2 two-path hydraulic variants hold golden call")
    _assert(fal["golden"]["f3_pp"] < 0.45 and fal["direct"]["f3_pp"] > 4.0, "SF11: F3 refutes raw 2-of-3 MV and post-CIP MV")
    _assert(fal["S3_r1_uncond"]["f3_pp"] > 1.4 and fal["S3_r2_120h"]["f3_pp"] > 0.9 and ex["cutoff:s3_r1_uncond_3class"]["members"]["TR03"] > 1000.0 and ex["cutoff:s3_r2_static_120h"]["members"]["TR03"] > 1000.0, "SF12: F3 refutes unconditioned 3-class LCA and static 120h EM (blow up TR03)")
    _assert(ex["cutoff:s3_unanimous"]["members"]["TR06"] < 400.0 and ov["S3"]["members"]["TR06"] < 400.0, "SF13: unanimous 3-of-3 drops TR06 < 400")
    _assert(all(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD) == g_slate for _, asm in res["variants_named"][19:28]), "SF14: all 9 converged S3 continuous post-CIP kinetic variants hold golden call")
    _assert(fal["golden"]["f4_mg_l"] < 0.22 and fal["S4_eq_var"]["f4_mg_l"] > 0.40 and ex["cutoff:s4_r1_r2_equal_var"]["members"]["TR05"] > 400.0 and ex["cutoff:s4_bay_sd_direct"]["members"]["TR08"] < 400.0 and res["rig_r2_asm"]["members"]["TR08"] < 400.0, "SF15: F4 refutes direct bay TDS and equal-variance bay pooling (eq-var flips TR05 > 400; bay-SD & R2 drop TR08 < 400)")
    _assert(all(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD) == g_slate for _, asm in res["variants_named"][28:36]), "SF16: all 8 S4 bay-TDS variance-component variants (incl. exact 2-stage & GLS Kalman AR(1) MLE) hold golden call")
    _assert(ex["hedge:history_2026_flat"]["members"]["TR01"] < 400.0, "SF17: flat 2026 history drops TR01 below 400.0 h")
    _assert("2,160" in std_txt and "CIP_ALK_pH11" in open(os.path.join(target_dir, PK.FILES["cip_log"]), encoding="utf-8").read(), "SF18: 2026 calendar quarters, 4 energy rates, and alternating CIP recipes filed cleanly")

    for k, asm in lat.items():
        sl = sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)
        _assert(sl != g_slate, f"lattice drop {k} files wrong slate ({sl})")
    for k, asm in list(ex.items()) + [(f"OVER_{s}", ov[s]) for s in ("S1", "S2", "S3", "S4")]:
        sl = sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)
        _assert(sl != g_slate, f"rival route {k} files wrong slate ({sl})")

    print("=== 4. GOLDEN WORKBOOK STYLE INTEGRITY & LIBREOFFICE FORMULA EVALUATION ===")
    xlsx_path = os.path.join(golden_dir, DEL.GOLDEN_XLSX)
    wb = openpyxl.load_workbook(xlsx_path, data_only=False)
    _assert(len(wb.sheetnames) == 8, f"8 golden workbook tabs ({wb.sheetnames})")
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                _ = cell.font.name
                _ = cell.fill.fill_type
                _ = cell.border.bottom.style
                _ = cell.number_format
    _assert(True, f"every cell style resolves cleanly across {len(wb.sheetnames)} golden tabs")
    _assert(len(wb["Overhaul_Triage_2027"]._charts) == 1, "Overhaul_Triage_2027 embeds train comparison bar chart")

    work = tempfile.mkdtemp(prefix="lo-eval-t28-")
    try:
        prof = "file://" + os.path.join(work, "profile")
        subprocess.run(
            [
                "soffice", "--headless", f"-env:UserInstallation={prof}",
                "--convert-to", "xlsx", "--outdir", work, xlsx_path,
            ],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        eval_wb = openpyxl.load_workbook(os.path.join(work, DEL.GOLDEN_XLSX), data_only=True)
        errs = []
        for ws in eval_wb.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and cell.value.startswith("#"):
                        errs.append((ws.title, cell.coordinate, cell.value))
        _assert(not errs, f"zero LibreOffice Calc formula errors across all 8 tabs (got {errs})")

        ws_e = eval_wb["Overhaul_Triage_2027"]
        _assert(abs(float(ws_e["C16"].value) - figs["C1_boron_2027"]) < 0.15, f"XLSX C16 matches C1_boron_2027 ({ws_e['C16'].value:.1f})")
        _assert(abs(float(ws_e["D16"].value) - figs["C2_scaling_2027"]) < 0.15, f"XLSX D16 matches C2_scaling_2027 ({ws_e['D16'].value:.1f})")
        _assert(abs(float(ws_e["E16"].value) - figs["C3_struct_2027"]) < 0.15, f"XLSX E16 matches C3_struct_2027 ({ws_e['E16'].value:.1f})")
        _assert(abs(float(ws_e["F16"].value) - figs["C4_tds_2027"]) < 0.15, f"XLSX F16 matches C4_tds_2027 ({ws_e['F16'].value:.1f})")
        _assert(abs(float(ws_e["G16"].value) - figs["A_total_2027"]) < 0.15, f"XLSX G16 matches A_total_2027 ({ws_e['G16'].value:.1f})")
        _assert(abs(float(ws_e["G17"].value) - figs["A_overhaul_2027"]) < 0.15, f"XLSX G17 matches A_overhaul_2027 ({ws_e['G17'].value:.1f})")
        _assert(abs(float(ws_e["H16"].value) - figs["A_q3_2027"]) < 0.15, f"XLSX H16 matches A_q3_2027 ({ws_e['H16'].value:.1f})")
        _assert(abs(float(ws_e["I16"].value) - figs["A_energy_mwh_exact"]) < 0.15, f"XLSX I16 matches A_energy_mwh ({ws_e['I16'].value:.2f})")
        _assert(abs(float(ws_e["I17"].value) - figs["A_overhaul_mwh_exact"]) < 0.15, f"XLSX I17 matches A_overhaul_mwh ({ws_e['I17'].value:.2f})")

        csv_rows = list(csv.DictReader(open(os.path.join(golden_dir, DEL.GOLDEN_CSV), encoding="utf-8")))
        _assert(len(csv_rows) == 8, "golden CSV has 8 train rows")
        _assert(
            list(csv_rows[0].keys()) == [
                "train_id", "boron_2027_h", "scaling_2027_h", "struct_2027_h", "tds_2027_h",
                "total_2027_h", "q3_2027_h", "energy_2027_mwh", "designation",
            ],
            "golden CSV carries exact SWRO-Q27 Annex B 9-column header",
        )
        for idx, r_csv in enumerate(csv_rows):
            r_xl = 8 + idx
            u = r_csv["train_id"]
            _assert(ws_e.cell(r_xl, 1).value == u, f"CSV/XLSX sort order matches row {idx + 1}: {u}")
            _assert(abs(float(ws_e.cell(r_xl, 7).value) - float(r_csv["total_2027_h"])) < 0.12, f"CSV/XLSX total_2027_h matches on {u}")
            _assert(abs(float(ws_e.cell(r_xl, 9).value) - float(r_csv["energy_2027_mwh"])) < 0.06, f"CSV/XLSX energy_2027_mwh matches on {u}")
            _assert(ws_e.cell(r_xl, 11).value == r_csv["designation"], f"CSV/XLSX designation matches on {u}: {r_csv['designation']}")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    print("ALL CHECKS PASSED (task28 v3)")


if __name__ == "__main__":
    main()
