"""Comprehensive deterministic assertion suite for task26 (v3, 70+ checks).

Covers:
  - Every Semantic Fork SF1 through SF18 explicitly by token
  - Zero-PQ-handle pack hygiene (pq_commissioning_autumn2026.csv active-only on Fossheim & Lindberg; no pq_archive_15min_2026.csv)
  - Exact reproduction of simulator arrays after Layer 1 ETL conformance (19 files)
  - IEC 60038 / EN 50160 physical voltage realism across all 11 substations (66 kV, 22 kV, 230 V AMI)
  - Layer 1 mess neutrality (superseded batch dedup, comms nulls drop vs interp)
  - Corelib level 5 and +/-20% forcing holds on the cut pack
  - Internal physics-balance separation (all 37 rivals >= 3.0x golden index; 80/80 AMI field phase-tracer match)
  - Frontier score checks (RESPONSE1_V2 <= 45 and >= 4/7 wrong; all 4 run_routes <= 50)
  - Distractor deletion invariance (removing the 3 distractors leaves every figure byte-identical)
  - Container & surface hygiene (no README/dictionary/notes under target/, zero em dashes in prompt/submission)
  - PDF multi-reader text extraction check (H25: pypdf AND pdftotext both extract all governing thresholds)
  - Golden deliverables exact tie-out against figures.json + cell-by-cell style readback
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

    # --- 1. File inventory & zero-PQ-handle hygiene (19 files; no readme/dictionary/manifest under target/) ---
    tfiles = sorted(os.listdir(TARGET))
    check(len(tfiles) == 19, f"expected 19 files in target/, found {len(tfiles)}")
    exts = {os.path.splitext(f)[1].lower() for f in tfiles}
    check(exts == {".csv", ".xlsx", ".db", ".pdf"}, f"expected 4 file categories, got {exts}")
    banned_names = re.compile(r"readme|dictionary|data_dict|manifest|field_notes|notes|schema", re.I)
    check(not any(banned_names.search(f) for f in tfiles), "banned helper/dictionary filename in target/")
    check("pq_archive_15min_2026.csv" not in tfiles, "old full-year 3-phase pq_archive_15min_2026.csv must NOT exist in v3")
    check("pq_commissioning_autumn2026.csv" in tfiles, "v3 active-only pq_commissioning_autumn2026.csv present")
    with open(os.path.join(TARGET, "pq_commissioning_autumn2026.csv"), encoding="utf-8") as f:
        rd = csv.DictReader(f)
        check(rd.fieldnames == ["substation_id", "ts_utc", "sub_p15_mw"],
              f"pq_commissioning_autumn2026.csv columns must be active-only, got {rd.fieldnames}")
        pq_subs = set()
        pq_months = set()
        pq_rows = 0
        for row in rd:
            pq_rows += 1
            pq_subs.add(row["substation_id"])
            pq_months.add(row["ts_utc"][:7])
    check(pq_subs == set(C.PQ_COMM_SITES), f"commissioning PQ sites {pq_subs} != {set(C.PQ_COMM_SITES)}")
    check(pq_months == {"2026-08", "2026-09", "2026-10"}, f"commissioning PQ months unexpected: {pq_months}")
    check(pq_rows == 11712, f"expected 11,712 Sep-Oct 15-min rows (2x61x96), got {pq_rows}")
    check(stats["raw_scada_rows"] >= 20000, f"scada CSV rows {stats['raw_scada_rows']} < 20,000")
    check(os.path.getsize(os.path.join(TARGET, PK.FILES["scada_fdr"])) > 10_000_000, "large feeder CSV > 10 MB")
    check(len(meta["distractor_files"]) == 3, "3 unlabelled distractors declared in metadata.json")
    for df in meta["distractor_files"]:
        check(df in tfiles, f"distractor {df} missing from target/")

    # --- 2. SF1-SF4: Governing standard definitions & scope ---
    check(stats["in_pool"] == sorted(C.TARGETS), "SF1: in-scope pool matches the 7 non-modernized substations")
    check(stats["refs"] == sorted(C.REFS), "SF1: Fossheim, Lindberg, Ostervik, and Solberg excluded from 2027-2029 pool")
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

    # --- 3. SF5-SF7: Layer 1 ETL exact conformance, IEC/EN voltage realism & mess neutrality ---
    check(stats["superseded_dropped"] == 4800, f"SF5: dropped 4,800 superseded preliminary SCADA rows ({stats['superseded_dropped']})")
    check(stats["vlv_nulls"] == 56, f"SF6: found 56 benign summer v_lv_kv comms nulls ({stats['vlv_nulls']})")
    for gid in ("GSP-Nord", "GSP-Sor"):
        check(np.allclose(pack_world["gsp_v"][gid], sim_world["gsp_v"][gid], atol=1e-3), f"SF5: {gid} 66 kV voltage matches simulator")
    hm = C.HEATING_HOURS
    for s in C.ALL_SUBS:
        sd_p = pack_world["subs"][s]
        sd_s = sim_world["subs"][s]
        check(np.allclose(sd_p["sub_p60"], sd_s["sub_p60"], atol=1e-4), f"SF5/SF6: {s} clean SCADA P60 matches simulator")
        check(np.array_equal(sd_p["tap_step_int"], sd_s["tap_step_int"]), f"SF5/SF6: {s} clean tap_step matches simulator")
        check(int(sd_p["tap_step_int"].min()) >= C.TAP_MIN and int(sd_p["tap_step_int"].max()) <= C.TAP_MAX,
              f"OLTC tap steps for {s} within [{C.TAP_MIN}, {C.TAP_MAX}]")
        check(np.allclose(sd_p["f_p60"], sd_s["f_p60"], atol=1e-3), f"SF7: {s} crosswalked feeder P60 matches simulator")
        check(np.allclose(sd_p["feeder_m15"], sd_s["feeder_m15"], atol=1e-4), f"SF7: {s} crosswalked feeder M15 matches simulator")
        check(np.allclose(sd_p["sub_net_kvarh_m"], sd_s["sub_net_kvarh_m"], atol=0.1), f"SF5: {s} monthly net kVARh matches")
        check(np.allclose(sd_p["v_bus_ph"], sd_s["v_bus_ph"], atol=1e-4), f"SF6: {s} 3-phase bus voltages match")
        check(int(sd_p["lat_is_ami"].sum()) == C.N_AMI_LAT and len(sd_p["lat_is_ami"]) == C.N_LATERALS,
              f"SF7: {s} has {C.N_AMI_LAT} AMI_SMART and {C.N_LEG_LAT} LEGACY_NON_AMI laterals")
        check(np.array_equal(np.sort(sd_p["lat_gis_ph"]), np.sort(sd_s["lat_gis_ph"])), f"SF7: {s} GIS lateral phase counts match")
        check(np.allclose(sd_p["lat_v_ami"][:, hm].mean(axis=0), sd_s["lat_v_ami"][:, hm].mean(axis=0), atol=6e-3),
              f"SF6: {s} AMI lateral mean voltage matches across all 4,368 heating hours")
        check(np.allclose(sd_p["lat_p_ami"][:, hm].sum(axis=0), sd_s["lat_p_ami"][:, hm].sum(axis=0), atol=0.25),
              f"SF6: {s} AMI lateral total kW matches across all 4,368 heating hours")
        check(np.allclose(sd_p["lat_q_ami"][:, hm].sum(axis=0), sd_s["lat_q_ami"][:, hm].sum(axis=0), atol=0.25),
              f"SF6: {s} AMI lateral total kVAr matches across all 4,368 heating hours")
        # IEC 60038 / EN 50160 voltage bounds
        check(59.4 <= float(sd_s["v_hv_true"].min()) and float(sd_s["v_hv_true"].max()) <= 72.5,
              f"IEC 60038 66 kV bounds on {s}: [{sd_s['v_hv_true'].min():.2f}, {sd_s['v_hv_true'].max():.2f}]")
        check(20.9 <= float(sd_p["v_lv_meas"].min()) and float(sd_p["v_lv_meas"].max()) <= 23.1,
              f"IEC 60038 22 kV bounds on {s}: [{sd_p['v_lv_meas'].min():.2f}, {sd_p['v_lv_meas'].max():.2f}]")
        check(207.0 <= float(sd_p["lat_v_ami"][:, hm].min()) and float(sd_p["lat_v_ami"][:, hm].max()) <= 253.0,
              f"EN 50160 230 V AMI bounds on {s}: [{sd_p['lat_v_ami'][:, hm].min():.1f}, {sd_p['lat_v_ami'][:, hm].max():.1f}]")
        if s in C.PQ_COMM_SITES:
            check(np.allclose(sd_p["comm_p15"], sd_s["comm_p15"], atol=1e-4),
                  f"SF5: {s} Sep-Oct active-only commissioning 15-min log matches simulator")

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

    # --- 4. SF8-SF18: All 27 honest variants & forcing perturbations hold the schedule and bands ---
    gold_sched = fig["r8_schedule"]
    check(len(fig["variants"]) == len(C.FAMILY) == 27,
          f"SF8, SF9, SF10, SF11, SF12, SF13, SF14, SF15, SF16: expected 27 variants, got {len(fig['variants'])}")
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

    # SF17: single-phase AMI covers ~48% of single-phase (res+com) load across all sites (8-55% of total peak)
    for s in C.ALL_SUBS:
        sd_p = pack_world["subs"][s]
        pk_h = int(np.argmax(sd_p["sub_p60"]))
        ami_frac = float(sd_p["lat_p_ami"][:, pk_h].sum() / (sd_p["sub_p60"][pk_h] * 1000.0))
        sp_kw = float((sd_p["p_cls"]["residential_heat"][pk_h] + sd_p["p_cls"]["commercial_mixed"][pk_h]) * 1000.0)
        ami_sp_frac = float(sd_p["lat_p_ami"][:, pk_h].sum() / sp_kw)
        check(0.08 <= ami_frac <= 0.55 and 0.38 <= ami_sp_frac <= 0.60,
              f"SF17: {s} AMI share total={ami_frac:.3f}, single-phase={ami_sp_frac:.3f} realistic partial coverage")

    # Forcing +/- 20% perturbations all HOLD
    check(len(fig["forcing"]) == 6, "6 forcing perturbations recorded")
    for p in fig["forcing"]:
        check(p["holds"] and p["answer"] == gold_sched, f"Forcing perturbation {p['input']} holds schedule")

    # --- 5. Corelib level 5 re-proved on cut pack + internal physics separation + frontier collapse ---
    spec, *_ = C.build_spec(pack_world)
    check(corelib.run(spec) == 0, "corelib passes level 5 on cut pack")
    check(fig["ref_params"]["tracer_matched"] == 80 and fig["ref_params"]["tracer_total"] == 80,
          "AMI Phase-ID matches 80/80 field-traced AMI laterals on Fossheim, Lindberg, Ostervik, and Solberg")
    check(fig["ref_params"]["gis_tracer_matched"] <= 64,
          f"GIS matches {fig['ref_params']['gis_tracer_matched']}/80 on modernized reference sites (expected <= 80%)")
    check(len(fig["phys_ratios"]) == len(C.RIVAL_OPTS) == 37,
          f"Expected 37 physics-validation rivals, got {len(fig['phys_ratios'])}")
    for rname, mult in fig["phys_ratios"].items():
        check(mult >= 3.0, f"Physics rival {rname} is {mult}x golden index (< 3.0x)")
    check(fig["routes"]["response1_v2"]["wrong_count"] >= 4,
          f"RESPONSE1_V2 must miss >= 4/7 sites (got {fig['routes']['response1_v2']['wrong_count']}/7)")
    check(fig["route_scores"]["response1_v2"] <= 45.0,
          f"RESPONSE1_V2 score must be <= 45 (got {fig['route_scores']['response1_v2']})")
    for rn in ("generous", "calibrated", "hedge", "cutoff"):
        check(fig["route_scores"][rn] <= 50.0, f"Frontier run_route {rn} score {fig['route_scores'][rn]} > 50")

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
        for tok in ("NS-2026", "85.0%", "100.0%", "Fossheim", "Lindberg", "Ostervik", "Solberg",
                    "Drangvik", "Hestmark", "Kvernholm", "Malmnes", "Raudfjord", "Svarthaug", "Tverrli", "Lim_MVA"):
            check(tok in txt, f"H25 PDF {label} missing token {tok!r}")
        for banned in ("quadrature", "capacitor", "kVARh", "PT offset", "demean", "storm", "regression",
                       "corridor", "SVD", "PCA", "sag", "LEGACY_NON_AMI", "tan_phi"):
            check(banned.lower() not in txt.lower(), f"Leak check: planning standard PDF mentions {banned!r}")

    # --- 8. Golden deliverables exact tie-out + cell-by-cell style readback + zero em dashes ---
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

    wb_path = os.path.join(GOLDEN, DL.FILES["wb"])
    wb_g = openpyxl.load_workbook(wb_path, data_only=True)
    wb_f = openpyxl.load_workbook(wb_path, data_only=False)
    check(wb_g.sheetnames == ["Relief_Schedule", "Critical_Components", "Physics_Validation",
                              "Routes_Comparison", "Variant_Battery"], f"Golden XLSX tabs: {wb_g.sheetnames}")
    ws0 = wb_g["Relief_Schedule"]
    ws0_f = wb_f["Relief_Schedule"]
    check(len(ws0._charts) == 1, "Golden XLSX Relief_Schedule carries 1 embedded chart")
    check(abs(float(ws0["D13"].value) - fig["c1_total_p15_mw"]) <= 0.01, "Golden XLSX D13 C1 P15 tie-out")
    check(abs(float(ws0["E13"].value) - fig["c2_total_qpeak_mvar"]) <= 0.01, "Golden XLSX E13 C2 Q tie-out")
    check(abs(float(ws0["F13"].value) - fig["c3_mean_lim_phase_pct"]) <= 0.01, "Golden XLSX F13 C3 w_max tie-out")
    check(abs(float(ws0["G13"].value) - fig["pool_lim_mva_sum"]) <= 0.01, "Golden XLSX G13 unrounded Lim_MVA sum tie-out")
    check(abs(float(ws0["I13"].value) - fig["total_relief_mva"]) <= 0.01, "Golden XLSX Total Relief tie-out")
    check(str(ws0_f["E13"].value) == "=SUM(E6:E12)", f"Golden XLSX E13 is live SUM formula ({ws0_f['E13'].value})")
    n_formulas = sum(
        1 for sn in wb_f.sheetnames for row_c in wb_f[sn].iter_rows()
        for c in row_c if isinstance(c.value, str) and c.value.startswith("=")
    )
    check(n_formulas >= 80, f"Golden XLSX carries >= 80 live Excel formulas (found {n_formulas})")
    with zipfile.ZipFile(wb_path) as zxw:
        ch_xml = zxw.read("xl/charts/chart1.xml").decode("utf-8")
        check("strRef" in ch_xml, "Golden XLSX chart1.xml uses strRef for category labels")
    check(all(not cid.startswith(("COR-R", "COR-T")) for cid in pack_world["corridors"]),
          f"Corridor IDs use neutral regional naming (found {sorted(pack_world['corridors'])})")
    ch0 = ws0._charts[0]
    check(ch0.y_axis.axPos == "b" and ch0.x_axis.axPos == "l", "Golden XLSX horizontal bar chart axis positions correct")

    styled_cells = 0
    for sname in wb_g.sheetnames:
        ws_s = wb_g[sname]
        for row_cells in ws_s.iter_rows():
            for cell in row_cells:
                _ = (cell.font.name, cell.font.bold, cell.font.color, cell.fill.fill_type,
                     cell.fill.fgColor, cell.border.top.style, cell.border.bottom.style, cell.number_format)
                styled_cells += 1
    check(styled_cells > 500, f"Read back styles for {styled_cells} golden cells without index error")
    for col in range(1, 11):
        hc = ws0.cell(row=5, column=col)
        check(hc.font.bold and str(hc.font.color.rgb or "").upper().endswith("FFFFFF"),
              f"Header col {col} carries bold white font ({hc.font.color.rgb})")
        check(hc.fill.fill_type == "solid" and str(hc.fill.fgColor.rgb or "").upper().endswith("1F3B5C"),
              f"Header col {col} carries solid navy fill ({hc.fill.fgColor.rgb})")
        check(hc.border.bottom.style == "medium",
              f"Header col {col} carries medium bottom border ({hc.border.bottom.style})")
    for col in range(1, 11):
        tc = ws0.cell(row=13, column=col)
        check(tc.font.bold and tc.border.top.style == "thin" and tc.border.bottom.style == "medium",
              f"Total row col {col} carries bold font + thin top / medium bottom border")

    for fn in ("prompt.txt", "submission.md"):
        t = open(os.path.join(TASK, fn), encoding="utf-8").read()
        check("\u2014" not in t and "\u2013" not in t, f"Zero em/en dashes in {fn}")

    with zipfile.ZipFile(os.path.join(TASK, "target.zip")) as zt:
        check(sorted(zt.namelist()) == tfiles, "target.zip entries match target/")
    with zipfile.ZipFile(os.path.join(TASK, "golden.zip")) as zg:
        check(sorted(zg.namelist()) == sorted(os.listdir(GOLDEN)), "golden.zip entries match golden/")

    print(f"CHECKS PASS: {COUNT} assertions passed on task26")


if __name__ == "__main__":
    main()
