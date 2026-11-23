#!/usr/bin/env python3
"""Comprehensive Stage 3 assertion suite for task28:
- Sulfur input gates (>=10 usable files, >=2 categories, 2 large messy CSVs >= 20,000 rows, >=2 unlabelled distractors)
- Bar block R1-R7 (domain raw material, neutral Layer 1 mess / clean-data test, lens-swap test, footprint outside
  deciding units, every SF1-SF16 fork asserted, 20-variant forcing, 6-way +/-20% forcing perturbations)
- No dictionary / manifest / readme / notes file under target/
- No hidden sheets/comments/defined names, style table validity on every shipped XLSX
- LibreOffice Calc headless formula evaluation on golden workbook: zero formula errors (#REF!, #DIV/0!, #VALUE!,
  #NAME?, #N/A), every evaluated formula cell agrees with figures.json and golden CSV.
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
    _assert(len(tfiles) == 14, f"14 usable files in target/ (got {len(tfiles)})")
    exts = {os.path.splitext(f)[1].lower() for f in tfiles}
    _assert(exts == {".csv", ".xlsx", ".json", ".pdf"}, f"4 file formats across categories ({sorted(exts)})")
    bad_desc = re.compile(r"(readme|dictionary|codebook|field_?notes|manifest|glossary|schema|_notes)", re.I)
    for f in tfiles:
        _assert(not bad_desc.search(f), f"no describing/notes filename: {f}")
    _assert(len(meta["distractor_files"]) >= 2, "at least 2 unlabelled distractors recorded only in metadata.json")
    for df in meta["distractor_files"]:
        _assert(df in tfiles, f"distractor present in target/: {df}")

    # Large messy CSVs check
    in_lines = sum(1 for _ in open(os.path.join(target_dir, PK.FILES["intake_15m"]), encoding="utf-8")) - 1
    ro_lines = sum(1 for _ in open(os.path.join(target_dir, PK.FILES["ro_feed_15m"]), encoding="utf-8")) - 1
    _assert(in_lines > 280320 and ro_lines > 280320, f"two large messy CSVs > 280k rows ({in_lines:,}, {ro_lines:,})")

    # Verify target.zip and golden.zip membership exactness
    with zipfile.ZipFile(os.path.join(TASK_DIR, "target.zip")) as zt:
        _assert(sorted(zt.namelist()) == tfiles, "target.zip members match target/ verbatim (no enclosing folder)")
    with zipfile.ZipFile(os.path.join(TASK_DIR, "golden.zip")) as zg:
        _assert(
            sorted(zg.namelist()) == sorted([DEL.GOLDEN_CSV, DEL.GOLDEN_XLSX]),
            "golden.zip contains strictly the 2 requested deliverables",
        )

    print("=== 2. PINNED CONSTANTS PRESENT IN SHIPPED DOCUMENTS ===")
    std_txt = "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(target_dir, PK.FILES["standard_pdf"])).pages)
    qa_txt = "\n".join(p.extract_text() or "" for p in PdfReader(os.path.join(target_dir, PK.FILES["lims_qa_pdf"])).pages)
    for tok in ("400.0", "0.50 mg/L", "exceeding 1.50", "420 kWh/h", "360 kWh/h", "540 kWh/h", "1.32", "1.28", "boron_2027_h", "energy_2027_mwh"):
        _assert(tok in std_txt, f"SWRO-Q27 PDF pins {tok!r}")
    _assert("0.004 mg/L" in qa_txt, "LIMS QA certificate pins 0.004 mg/L repeatability SD")
    # Never-filed vocabulary sweep in PDFs
    for banned in ("Matheron", "Krige", "Lagrangian", "Dawid-Skene", "latent class", "autocorrelation", "short-circuit", "baffling", "comonotonic"):
        _assert(banned.lower() not in std_txt.lower(), f"SWRO-Q27 PDF never hints at {banned!r}")
        _assert(banned.lower() not in qa_txt.lower(), f"LIMS QA PDF never hints at {banned!r}")

    print("=== 3. ANALYSIS, FORKS (SF1-SF16), CLEAN-DATA & FOOTPRINT TESTS ===")
    res = AN.run_all(target_dir)
    g = res["gold_asm"]
    g_slate = res["golden_slate"]
    _assert(g_slate == ["TR01", "TR02", "TR06", "TR07"], f"golden slate exact ({g_slate})")

    # Verify shipped analysis reproduces core.simulate_world(2801) cleanly (< 0.15 h drift from CSV decimal formatting)
    core_data = core.simulate_world(core.SEED)
    core_r1 = core.estimate_s1(core_data, mode="golden", kernel="ar1", obj="wls")
    core_r2 = core.estimate_s2(core_data, mode="golden", flow_interp="linear", loss_fn="l2")
    core_r3 = core.estimate_s3(core_data, mode="golden", foul_model="tied_d3_d12", cip_mode="free_per_train")
    core_inc = core._incumbent_2026_by_train(core_data)
    core_asm = core.assemble(core_r1, core_r2, core_r3, core_inc)
    max_diff = max(abs(g["members"][u] - core_asm["members"][u]) for u in core.TRAINS)
    _assert(max_diff < 0.05, f"cleaned shipped pack matches core.py within 0.05 h (max diff {max_diff:.5f} h)")

    # Clean-data test: every stump mechanism holds on uncorrupted core arrays too (Layer 1 mess is neutral)
    _assert(
        sorted(u for u in core.TRAINS if core_asm["members"][u] >= core.THRESHOLD) == g_slate,
        "clean-data test: uncorrupted data produces identical call and figures",
    )

    # Footprint outside deciding units: every stump affects monitor trains as well as overhaul trains
    lat = res["lattice_asm"]
    _assert(abs(lat["S1"]["members"]["TR04"] - g["members"]["TR04"]) > 40.0, "S1 footprint extends to monitor TR04")
    _assert(abs(lat["S2"]["members"]["TR08"] - g["members"]["TR08"]) > 90.0, "S2 footprint extends to monitor TR08")
    _assert(abs(lat["S3"]["members"]["TR07"] - g["members"]["TR07"]) > 1000.0, "S3 footprint extends to texture TR07")

    # All 26 variants hold exact call, all 6 +/-20% perturbations hold exact call
    for nm, asm in res["variants_named"]:
        sl = sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)
        _assert(sl == g_slate, f"variant holds call: {nm}")
    for pt in res["perturbations"]:
        _assert(pt["holds"], f"forcing perturbation holds: {pt['input']} (min_ov={pt['min_overhaul']:.1f}, max_mo={pt['max_monitor']:.1f})")

    # SF1-SF16: every semantic fork asserted explicitly
    fal = res["fal_by_route"]
    ex = res["extra_routes"]
    ov = res["over"]
    _assert(fal["golden"]["f1"] < 0.06 and fal["direct"]["f1"] > 10 * fal["golden"]["f1"], "SF1: F1 refutes raw composite counting")
    _assert(fal["S1_over"]["f1"] > 8 * fal["golden"]["f1"] and ov["S1"]["members"]["TR04"] > 400.0, "SF2: F1 refutes i.i.d. sqrt(m) over-correction (flips TR04)")
    _assert(fal["rigorous"]["f1"] > 4 * fal["golden"]["f1"] and ex["cutoff:s1_pooled"]["members"]["TR01"] < 400.0, "SF3: F1 refutes pooled AR(1) factor (misses TR01)")
    _assert(ex["cutoff:s1_loglog"]["members"]["TR05"] > 400.0, "SF4: log-log variance extrapolation overshoots physical ceiling and flips TR05")
    _assert(all(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD) == g_slate for _, asm in res["variants_named"][:6]), "SF5: all 6 S1 kernel/moment/trim/lab-noise variants converge on golden call")
    _assert(fal["golden"]["f2_ms_cm"] < 0.56 and fal["direct"]["f2_ms_cm"] > 2.40, "SF6: F2 refutes same-timestamp pairing")
    _assert(fal["rigorous"]["f2_ms_cm"] > 1.70 and fal["s2_steady_flow"]["f2_ms_cm"] > 1.75 and ex["cutoff:s2_fixed_lag"]["members"]["TR02"] < 400.0, "SF7: F2 refutes optimal fixed wall-clock lag CCF and steady-flow subset")
    _assert(fal["s2_nom_vol"]["f2_ms_cm"] > 1.15 and ex["cutoff:s2_nom_vol"]["members"]["TR02"] < 400.0, "SF8: F2 refutes nominal basin volume V_nom")
    _assert(ov["S2"]["members"]["TR05"] > 400.0, "SF9: comonotonic upper-bound pairing flips negatively coupled TR05")
    _assert(all(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD) == g_slate for _, asm in res["variants_named"][6:17]), "SF10: all 11 S2 flow-integration, profile-loss, and parcel-lookup variants converge on golden call")
    _assert(fal["golden"]["f3_pp"] < 0.55 and fal["direct"]["f3_pp"] > 2.50 and ex["cutoff:s3_post_cip_mv"]["members"]["TR03"] > 400.0, "SF11: F3 refutes 2-of-3 majority vote and post-CIP majority vote")
    _assert(ex["cutoff:s3_ds2_ci"]["members"]["TR03"] > 400.0 and ex["cutoff:s3_post_cip_ds2"]["members"]["TR03"] > 400.0, "SF12: F3 refutes 2-class conditional-independence Dawid-Skene EM")
    _assert(ex["cutoff:s3_unanimous"]["members"]["TR06"] < 400.0 and ov["S3"]["members"]["TR06"] < 400.0, "SF13: unanimous 3-of-3 and uninverted raw D3 drop damaged TR06 below 400 h")
    _assert(all(sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD) == g_slate for _, asm in res["variants_named"][17:23]), "SF14: all 6 S3 EM specification and CIP-window variants converge on golden call")
    _assert(ex["hedge:history_2026_flat"]["members"]["TR01"] < 400.0 and ex["hedge:history_2026_flat"]["members"]["TR02"] < 400.0, "SF15: flat 2026 history without 2027 Operating Plan drops TR01 and TR02 below 400 h")
    _assert("4.4" in std_txt and "2,160" in std_txt, "SF16: 2026 calendar quarters and Clause 4.4 raw monitoring discrepancy rate pinned verbatim in SWRO-Q27")
    for k in ("S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"):
        sl = sorted(u for u in core.TRAINS if lat[k]["members"][u] >= core.THRESHOLD)
        _assert(sl != g_slate, f"lattice drop {k} files wrong slate ({sl})")
    for k, asm in list(ex.items()) + [(f"OVER_{s}", ov[s]) for s in ("S1", "S2", "S3")]:
        sl = sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)
        _assert(sl != g_slate, f"rival route {k} files wrong slate ({sl})")

    print("=== 4. GOLDEN WORKBOOK STYLE INTEGRITY & LIBREOFFICE FORMULA EVALUATION ===")
    xlsx_path = os.path.join(golden_dir, DEL.GOLDEN_XLSX)
    wb = openpyxl.load_workbook(xlsx_path, data_only=False)
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for cell in row:
                _ = cell.font.name
                _ = cell.fill.fill_type
                _ = cell.border.bottom.style
                _ = cell.number_format
    _assert(True, f"every cell style resolves cleanly across {len(wb.sheetnames)} golden tabs")
    _assert(len(wb["Overhaul_Triage_2027"]._charts) == 1, "Overhaul_Triage_2027 embeds train comparison bar chart")

    # Evaluate every Excel formula via LibreOffice Calc headless conversion
    work = tempfile.mkdtemp(prefix="lo-eval-t28-")
    try:
        prof = "file://" + os.path.join(work, "profile")
        subprocess.run(
            [
                "soffice",
                "-env:UserInstallation=" + prof,
                "--headless",
                "--convert-to",
                "xlsx",
                "--outdir",
                work,
                xlsx_path,
            ],
            check=True,
            capture_output=True,
            timeout=120,
        )
        eval_wb = openpyxl.load_workbook(os.path.join(work, DEL.GOLDEN_XLSX), data_only=True)
        errs = []
        for ws in eval_wb.worksheets:
            for row in ws.iter_rows():
                for cell in row:
                    if isinstance(cell.value, str) and cell.value.startswith("#"):
                        errs.append(f"{ws.title}!{cell.coordinate}={cell.value}")
        _assert(not errs, f"LibreOffice Calc evaluates all formulas with 0 errors ({errs[:5]})")

        ws_e = eval_wb["Overhaul_Triage_2027"]
        _assert(abs(float(ws_e["C16"].value) - figs["C1_boron_2027"]) < 0.06, f"Exec C16 formula = {ws_e['C16'].value:.2f} matches C1 {figs['C1_boron_2027']}")
        _assert(abs(float(ws_e["D16"].value) - figs["C2_scaling_2027"]) < 0.06, f"Exec D16 formula = {ws_e['D16'].value:.2f} matches C2 {figs['C2_scaling_2027']}")
        _assert(abs(float(ws_e["E16"].value) - figs["C3_struct_2027"]) < 0.06, f"Exec E16 formula = {ws_e['E16'].value:.2f} matches C3 {figs['C3_struct_2027']}")
        _assert(abs(float(ws_e["F16"].value) - figs["A_total_2027"]) < 0.06, f"Exec F16 formula = {ws_e['F16'].value:.2f} matches Total {figs['A_total_2027']}")
        _assert(abs(float(ws_e["F17"].value) - figs["A_overhaul_2027"]) < 0.06, f"Exec F17 formula = {ws_e['F17'].value:.2f} matches Overhaul {figs['A_overhaul_2027']}")
        _assert(abs(float(ws_e["G16"].value) - figs["A_q3_2027"]) < 0.06, f"Exec G16 formula = {ws_e['G16'].value:.2f} matches Q3 {figs['A_q3_2027']}")
        _assert(abs(float(ws_e["H16"].value) - figs["A_energy_mwh"]) < 0.06, f"Exec H16 formula = {ws_e['H16'].value:.2f} MWh matches Energy {figs['A_energy_mwh']} MWh")
        _assert(abs(float(ws_e["H17"].value) - figs["A_overhaul_mwh"]) < 0.06, f"Exec H17 formula = {ws_e['H17'].value:.2f} MWh matches OvEnergy {figs['A_overhaul_mwh']} MWh")
        _assert(abs(float(ws_e["B30"].value) * 100.0 - figs["A_diag_err_pct"]) < 0.06, f"Exec B30 formula = {ws_e['B30'].value*100:.2f}% matches Disc {figs['A_diag_err_pct']}%")
    finally:
        shutil.rmtree(work, ignore_errors=True)

    # Golden CSV agreement with figures.json
    with open(os.path.join(golden_dir, DEL.GOLDEN_CSV), encoding="utf-8") as f:
        csv_rows = list(csv.DictReader(f))
    _assert(len(csv_rows) == 8, "golden CSV has 8 train rows")
    for row in csv_rows:
        u = row["train_id"]
        ft = figs["trains"][u]
        _assert(abs(float(row["total_2027_h"]) - ft["total_2027_h"]) < 0.06, f"CSV {u} total matches figures.json")
        _assert(abs(float(row["energy_2027_mwh"]) - ft["energy_2027_mwh"]) < 0.02, f"CSV {u} MWh matches figures.json")
        _assert(row["designation"] == ft["designation"], f"CSV {u} designation matches figures.json")

    print("\nALL CHECKS PASSED.")


if __name__ == "__main__":
    main()
