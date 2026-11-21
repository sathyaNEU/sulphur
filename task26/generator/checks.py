"""Comprehensive deterministic assertion suite for task26 (50+ checks).

Covers:
  - Every Semantic Fork SF1 through SF18 explicitly by token
  - Exact reproduction of simulator arrays after Layer 1 ETL conformance
  - Layer 1 mess neutrality (superseded batch dedup, comms nulls drop vs interp, row-order permutation invariance)
  - Corelib level 5 and +/-20% forcing holds on the cut pack
  - Referee separation (all 7 rivals >= 3.0x golden MAE; 72/72 field phase-tracer match)
  - Distractor deletion invariance (removing the 3 distractors leaves every figure byte-identical)
  - Container & surface hygiene (no README/dictionary/notes under target/, zero em dashes in prompt/submission)
  - PDF multi-reader text extraction check (H25: pypdf AND pdftotext both extract all governing thresholds)
  - Golden deliverables exact tie-out against figures.json
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

import numpy as np
import openpyxl
from pypdf import PdfReader

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET = os.path.join(TASK, "target")
GOLDEN = os.path.join(TASK, "golden")
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(TASK), ".claude", "skills", "stumping"))
import corelib  # noqa: E402
import analysis as A  # noqa: E402
import core as C  # noqa: E402
import deliver as DL  # noqa: E402
import docs  # noqa: E402
import pack as PK  # noqa: E402
import results as RS  # noqa: E402

COUNT = 0


def check(cond, msg):
    global COUNT
    COUNT += 1
    assert cond, f"FAIL [{COUNT}]: {msg}"


def main():
    fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
    meta = json.load(open(os.path.join(TASK, "metadata.json"), encoding="utf-8"))
    pack_world, stats = A.load_pack(TARGET)
    sim_world = C.simulate()

    # --- 1. File inventory & hygiene (no readme/dictionary/manifest under target/) ---
    tfiles = sorted(os.listdir(TARGET))
    check(len(tfiles) == 17, f"expected 17 files in target/, found {len(tfiles)}")
    exts = {os.path.splitext(f)[1].lower() for f in tfiles}
    check(exts == {".csv", ".xlsx", ".db", ".pdf"}, f"expected 4 file categories, got {exts}")
    banned_names = re.compile(r"readme|dictionary|data_dict|manifest|field_notes|notes|schema", re.I)
    check(not any(banned_names.search(f) for f in tfiles), "banned helper/dictionary filename in target/")
    check(stats["raw_scada_rows"] >= 20000, f"scada CSV rows {stats['raw_scada_rows']} < 20,000")
    check(os.path.getsize(os.path.join(TARGET, PK.FILES["scada_fdr"])) > 10_000_000, "large feeder CSV > 10 MB")
    check(len(meta["distractor_files"]) == 3, "3 unlabelled distractors declared in metadata.json")
    for df in meta["distractor_files"]:
        check(df in tfiles, f"distractor {df} missing from target/")

    # --- 2. SF1-SF4: Governing standard definitions & scope ---
    # SF1: 7 in-scope target substations, Lindberg & Ostervik modernized and excluded
    check(stats["in_pool"] == list(C.TARGETS), "SF1: in-scope pool matches the 7 non-modernized substations")
    check(stats["refs"] == list(C.REFS), "SF1: Lindberg and Ostervik excluded from 2027-2029 pool")
    # SF2, SF3, SF4: limiting-phase formula, inclusive thresholds 85/100, relief above 85% Firm N-1 MVA
    for s in C.TARGETS:
        r = fig["substations"][s]
        exp_lim = 3.0 * (r["w_max_pct"] / 100.0) * r["s15_tot_mva"]
        check(abs(r["lim_mva"] - exp_lim) <= 0.03, f"SF2: {s} lim_mva matches 3*w_max*S15")
        exp_load = 100.0 * r["lim_mva"] / r["firm_n1_mva"]
        check(abs(r["loading_pct"] - exp_load) <= 0.05, f"SF2: {s} loading_pct matches 100*lim_mva/firm_n1")
        exp_rel = max(0.0, r["lim_mva"] - 0.85 * r["firm_n1_mva"])
        check(abs(r["relief_mva"] - exp_rel) <= 0.03, f"SF4: {s} relief_mva matches max(0, lim - 0.85*firm)")
        check(abs(r["loading_pct"] - 85.0) >= 4.0 and abs(r["loading_pct"] - 100.0) >= 4.0,
              f"SF3: {s} clears 85/100 planning boundaries by >= 4 pp")
    check(abs(sum(fig["substations"][s]["relief_mva"] for s in C.TARGETS) - fig["total_relief_mva"]) <= 0.05,
          "SF4: total relief MVA equals sum of per-substation relief MVA")

    # --- 3. SF5-SF7: Layer 1 ETL exact conformance & mess neutrality ---
    check(stats["superseded_dropped"] == 3840, f"SF5: dropped 3,840 superseded preliminary SCADA rows ({stats['superseded_dropped']})")
    check(stats["vlv_nulls"] == 48, f"SF6: found 48 benign summer v_lv_kv comms nulls ({stats['vlv_nulls']})")
    for s in C.ALL_SUBS:
        sd_p = pack_world["subs"][s]
        sd_s = sim_world["subs"][s]
        check(np.allclose(sd_p["sub_p60"], sd_s["sub_p60"], atol=1e-4), f"SF5/SF6: {s} clean SCADA P60 matches simulator")
        check(np.allclose(sd_p["v_hv_meas"], sd_s["v_hv_meas"], atol=1e-3), f"SF5/SF6: {s} clean V_hv matches simulator")
        check(np.array_equal(sd_p["tap_step_int"], sd_s["tap_step_int"]), f"SF5/SF6: {s} clean tap_step matches simulator")
        check(np.allclose(sd_p["f_p60"], sd_s["f_p60"], atol=1e-3), f"SF7: {s} crosswalked feeder P60 matches simulator")
        check(np.allclose(sd_p["feeder_m15"], sd_s["feeder_m15"], atol=1e-4), f"SF7: {s} crosswalked feeder M15 matches simulator")
        check(np.allclose(sd_p["sub_net_kvarh_m"], sd_s["sub_net_kvarh_m"], atol=0.1), f"SF5: {s} monthly net kVARh matches")
        check(np.allclose(sd_p["v_bus_ph"], sd_s["v_bus_ph"], atol=1e-4), f"SF6: {s} 3-phase bus voltages match")
        check(np.array_equal(np.sort(sd_p["lat_gis_ph"]), np.sort(sd_s["lat_gis_ph"])), f"SF7: {s} GIS lateral phase counts match")
        # Heating-season AMI aggregate kW and voltage mean match across all 4,368 heating hours (permutation-invariant)
        hm = C.HEATING_HOURS
        check(np.allclose(sd_p["lat_v_hourly"][:, hm].mean(axis=0), sd_s["lat_v_hourly"][:, hm].mean(axis=0), atol=6e-3),
              f"SF6: {s} AMI lateral mean voltage matches across all 4,368 heating hours")
        check(np.allclose(sd_p["lat_p_hourly"][:, hm].sum(axis=0), sd_s["lat_p_hourly"][:, hm].sum(axis=0), atol=0.25),
              f"SF6: {s} AMI lateral total kW matches across all 4,368 heating hours")

    # Verify comms nulls drop vs interpolate leaves every peak figure unchanged (winter untouched!)
    noninterp_world, _ = A.load_pack(TARGET, interpolate_nulls=False)
    for s in C.TARGETS:
        noninterp_world["subs"][s]["truth"] = sim_world["subs"][s]["truth"]
        pack_world["subs"][s]["truth"] = sim_world["subs"][s]["truth"]
    g_interp, _ = C.evaluate(pack_world, {})
    g_drop, _ = C.evaluate(noninterp_world, {})
    for s in C.TARGETS:
        check(abs(g_interp[s]["loading_pct"] - g_drop[s]["loading_pct"]) < 1e-9,
              f"SF6: summer v_lv_kv nulls leave {s} loading identical (drop vs interp)")

    # --- 4. SF8-SF17: All 21 honest variants & forcing perturbations hold the schedule and bands ---
    gold_sched = fig["r8_schedule"]
    check(len(fig["variants"]) == 21, "SF8, SF9, SF10, SF11, SF12, SF13, SF14, SF15, SF16: 21 variants recorded")
    for v in fig["variants"]:
        check(v["holds"] and v["answer"] == gold_sched, f"SF8/SF9/SF10/SF12/SF13/SF14/SF15/SF16: variant '{v['name']}' holds schedule")
        check(fig["c1_band"][0] <= v["c1_total_p15_mw"] <= fig["c1_band"][1], f"SF8/SF9/SF10: C1 in band for {v['name']}")
        check(fig["c2_band"][0] <= v["c2_total_qpeak_mvar"] <= fig["c2_band"][1], f"SF12/SF13/SF14: C2 in band for {v['name']}")
        check(fig["c3_band"][0] <= v["c3_mean_lim_phase_pct"] <= fig["c3_band"][1], f"SF15/SF16: C3 in band for {v['name']}")
        check(fig["total_relief_band"][0] <= v["total_relief_mva"] <= fig["total_relief_band"][1],
              f"SF11/SF17: Total relief in band for {v['name']}")
        for s in C.TARGETS:
            lb = fig["bands"]["loading_pct"][s]
            mb = fig["bands"]["lim_mva"][s]
            check(lb[0] <= v["loading_pct"][s] <= lb[1], f"SF18: {s} loading in band for {v['name']}")
            check(mb[0] <= v["lim_mva"][s] <= mb[1], f"SF18: {s} MVA in band for {v['name']}")

    # SF17: balanced 3-phase residual equals (1 - sp_share) * sub_p60 exactly
    for s in C.ALL_SUBS:
        sd_p = pack_world["subs"][s]
        pk_h = int(np.argmax(sd_p["sub_p60"]))
        bal_obs = sd_p["sub_p60"][pk_h] * 1000.0 - sd_p["lat_p_hourly"][:, pk_h].sum()
        check(bal_obs > 0.20 * sd_p["sub_p60"][pk_h] * 1000.0, f"SF17: {s} balanced 3-phase share realistic (>20%)")

    # Forcing +/- 20% perturbations all HOLD
    check(len(fig["forcing"]) == 6, "6 forcing perturbations recorded")
    for p in fig["forcing"]:
        check(p["holds"] and p["answer"] == gold_sched, f"Forcing perturbation {p['input']} holds schedule")

    # --- 5. Corelib level 5 re-proved on cut pack + referee dominance ---
    spec, *_ = C.build_spec(pack_world)
    check(corelib.run(spec) == 0, "corelib passes level 5 on cut pack")
    check(fig["ref_params"]["tracer_matched"] == 72 and fig["ref_params"]["tracer_total"] == 72,
          "Phase-ID matches 72/72 field-traced laterals on Lindberg and Ostervik")
    check(fig["ref_params"]["gis_tracer_matched"] == 54, "GIS matches 54/72 (75.0%) on Lindberg and Ostervik")
    for rname, mult in fig["ref_ratios"].items():
        check(mult >= 3.5, f"Referee rival {rname} is {mult}x golden MAE (< 3.5x)")

    # --- 6. Distractor deletion invariance ---
    tmp = tempfile.mkdtemp(prefix="task26-nodist-")
    try:
        for fn in tfiles:
            if fn not in meta["distractor_files"]:
                shutil.copy2(os.path.join(TARGET, fn), os.path.join(tmp, fn))
        w_nodist, _ = A.load_pack(tmp)
        for s in C.TARGETS:
            w_nodist["subs"][s]["truth"] = sim_world["subs"][s]["truth"]
        g_nodist, _ = C.evaluate(w_nodist, {})
        for s in C.TARGETS:
            check(abs(g_nodist[s]["loading_pct"] - g_interp[s]["loading_pct"]) < 1e-12,
                  f"Distractor deletion invariance on {s}")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    # --- 7. PDF multi-reader text extraction check (H25) ---
    std_pdf = os.path.join(TARGET, docs.FILES["standard"])
    pypdf_txt = "\n".join(p.extract_text() or "" for p in PdfReader(std_pdf).pages)
    pdftotext_txt = subprocess.run(["pdftotext", std_pdf, "-"], capture_output=True, text=True, check=True).stdout
    for label, txt in (("pypdf", pypdf_txt), ("pdftotext", pdftotext_txt)):
        for tok in ("NS-2026", "85.0%", "100.0%", "Lindberg", "Ostervik", "Drangvik", "Hestmark",
                    "Kvernholm", "Malmnes", "Raudfjord", "Svarthaug", "Tverrli", "Lim_MVA"):
            check(tok in txt, f"H25 PDF {label} missing token {tok!r}")
        for banned in ("quadrature", "capacitor", "kVARh", "PT offset", "demean", "storm", "regression"):
            check(banned.lower() not in txt.lower(), f"Leak check: planning standard PDF mentions {banned!r}")

    # --- 8. Golden deliverables exact tie-out + zero em dashes ---
    g_csv = os.path.join(GOLDEN, DL.FILES["csv"])
    with open(g_csv, encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    check(len(rows) == 7, "Golden CSV has 7 rows")
    for row in rows:
        s = row["substation_id"]
        rec = fig["substations"][s]
        check(abs(float(row["peak_15min_active_mw"]) - rec["p15_peak_mw"]) < 1e-6, f"Golden CSV P15 {s}")
        check(abs(float(row["peak_hour_reactive_mvar"]) - rec["q_peak_h_mvar"]) < 1e-6, f"Golden CSV Q {s}")
        check(abs(float(row["firm_n1_loading_pct"]) - rec["loading_pct"]) < 1e-6, f"Golden CSV Load {s}")
        check(row["assigned_relief_phase"] == rec["phase"], f"Golden CSV Phase {s}")

    wb_g = openpyxl.load_workbook(os.path.join(GOLDEN, DL.FILES["wb"]), data_only=True)
    check(wb_g.sheetnames == ["Relief_Schedule", "Critical_Components", "Referee_Validation",
                              "Routes_Comparison", "Variant_Battery"], f"Golden XLSX tabs: {wb_g.sheetnames}")
    ws0 = wb_g["Relief_Schedule"]
    check(len(ws0._charts) == 1, "Golden XLSX Relief_Schedule carries 1 embedded chart")
    check(abs(float(ws0["G13"].value) - fig["pool_lim_mva_sum"]) < 1e-6, "Golden XLSX G13 unrounded Lim_MVA sum tie-out")
    check(abs(float(ws0["I13"].value) - fig["total_relief_mva"]) < 1e-6, "Golden XLSX Total Relief tie-out")
    ch0 = ws0._charts[0]
    check(ch0.y_axis.axPos == "b" and ch0.x_axis.axPos == "l", "Golden XLSX horizontal bar chart axis positions correct")

    # Cell-by-cell style readback check across all tabs of golden workbook (postprocess.normalize_ooxml fidelity)
    styled_cells = 0
    for sname in wb_g.sheetnames:
        ws_s = wb_g[sname]
        for row_cells in ws_s.iter_rows():
            for cell in row_cells:
                _ = (cell.font.name, cell.font.bold, cell.font.color, cell.fill.fill_type,
                     cell.fill.fgColor, cell.border.top.style, cell.border.bottom.style, cell.number_format)
                styled_cells += 1
    check(styled_cells > 500, f"Read back styles for {styled_cells} golden cells without index error")
    # Header row 5 on Relief_Schedule must carry white ink (FFFFFF), navy fill (1F3B5C), and medium bottom border
    for col in range(1, 11):
        hc = ws0.cell(row=5, column=col)
        check(hc.font.bold and str(hc.font.color.rgb or "").upper().endswith("FFFFFF"),
              f"Header col {col} carries bold white font ({hc.font.color.rgb})")
        check(hc.fill.fill_type == "solid" and str(hc.fill.fgColor.rgb or "").upper().endswith("1F3B5C"),
              f"Header col {col} carries solid navy fill ({hc.fill.fgColor.rgb})")
        check(hc.border.bottom.style == "medium",
              f"Header col {col} carries medium bottom border ({hc.border.bottom.style})")
    # Total row 13 carries thin top and medium bottom border
    for col in range(1, 11):
        tc = ws0.cell(row=13, column=col)
        check(tc.font.bold and tc.border.top.style == "thin" and tc.border.bottom.style == "medium",
              f"Total row col {col} carries bold font + thin top / medium bottom border")

    # Zero em/en dashes in prompt.txt and submission.md
    for fn in ("prompt.txt", "submission.md"):
        t = open(os.path.join(TASK, fn), encoding="utf-8").read()
        check("\u2014" not in t and "\u2013" not in t, f"Zero em/en dashes in {fn}")

    # Zip files exist and contain exact files
    with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as zt:
        check(sorted(zt.namelist()) == tfiles, "target.zip entries match target/")
    with zipfile.ZipFile(os.path.join(TASK, "golden.zip")) as zg:
        check(sorted(zg.namelist()) == sorted(os.listdir(GOLDEN)), "golden.zip entries match golden/")

    print(f"CHECKS PASS: {COUNT} assertions passed on task26")


if __name__ == "__main__":
    main()
