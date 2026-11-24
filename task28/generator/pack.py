#!/usr/bin/env python3
"""Materialize the 13 non-PDF input files in task28/target/ directly from core.simulate_world(core.SEED).

Every cleaned operational series reproduces core.py bit-for-bit (within formatting precision <= 5e-6).
Authentic plant IT Layer 1 boundary conventions:
- Mixed Portuguese DD/MM/YYYY (South Bay) and ISO YYYY-MM-DD (North Bay) LIMS collection dates
- Mixed mg/L (North Bay) and ug/L (South Bay) boron units, and m3/h (North Bay) vs L/s (South Bay) feed flow
- Re-transmitted LIMS QA revisions (qa_revision 1 superseded by qa_revision 2) uniformly across all 8 trains
- Exact duplicate SCADA/telemetry re-transmission frames (~0.25-0.30%) uniformly across all 8 trains and 2 bays
- Legacy LINE-A..H train tags on Q1 autosampler, selected Q1 LIMS, and H1 CIP wash records
- UTC historian and bay-collector timestamps (Z) vs Europe/Lisbon (+00:00 / +01:00) local shift and CIP timestamps
- Two unlabelled regional Algarve context distractors (MIBEL power spot prices, Algarve reservoir levels)
"""
import csv
import datetime as dt
import json
import math
import os
import random
import sys
from zoneinfo import ZoneInfo

import openpyxl
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core  # noqa: E402

ORG = "Barlavento Dessalinizacao Municipal, E.M."
AS_OF = "2027-01-18"
UTC = dt.timezone.utc
LISBON = ZoneInfo("Europe/Lisbon")

PEOPLE = {
    "lead": "Ines Guerreiro",          # Process Engineering and Membrane Integrity Lead
    "scada": "Duarte Monteiro",        # SCADA & Instrumentation Supervisor
    "lims": "Filipa Nogueira",         # LIMS Analytical Chemistry Lead
    "hydraulics": "Vasco Figueiredo",  # Hydraulic Operations Engineer
    "maint": "Beatriz Lourenco",       # Membrane Maintenance Planner
    "compliance": "Tiago Castanheira", # Membrane Reliability Engineering Lead
    "inspector": "Mafalda Tavares",    # Chief Desalination Process Engineer
    "analyst": "Goncalo Peixoto",      # Plant Reliability Analyst
}

FILES = {
    "standard_pdf": "swro_integrity_standard_q27.pdf",
    "lims_qa_pdf": "lims_qa_certificate_2026.pdf",
    "asset_reg": "train_asset_register.csv",
    "op_plan": "operating_plan_2027.csv",
    "boron_comp": "permeate_boron_composites_2026.csv",
    "autosampler": "autosampler_schedule_2026.csv",
    "intake_15m": "intake_chemistry_15m_2026.csv",
    "ro_feed_15m": "ro_feed_header_15m_2026.csv",
    "hydraulics_h": "train_hydraulics_hourly_2026.csv",
    "bay_tds_h": "bay_permeate_tds_hourly_2026.csv",
    "shift_diag": "shift_diagnostics_2026.csv",
    "cip_log": "cip_wash_log_2026.csv",
    "scada_cfg": "scada_bay_config_2026.json",
    "dist_mibel": "mibel_iberian_power_spot_2026.csv",
    "dist_reservoir": "algarve_reservoir_levels_2026.xlsx",
}

TRAIN_META = {
    "TR01": dict(legacy="LINE-A", bay="North", comm=2017, vessels=96, epv=7, model="SWC6-LD-400", header="HDR-N1"),
    "TR02": dict(legacy="LINE-B", bay="North", comm=2018, vessels=96, epv=7, model="SWC6-LD-400", header="HDR-N1"),
    "TR03": dict(legacy="LINE-C", bay="North", comm=2019, vessels=96, epv=7, model="SWC6-LD-400", header="HDR-N2"),
    "TR04": dict(legacy="LINE-D", bay="North", comm=2018, vessels=96, epv=7, model="SWC6-LD-400", header="HDR-N2"),
    "TR05": dict(legacy="LINE-E", bay="South", comm=2020, vessels=96, epv=7, model="TM820M-400", header="HDR-S1"),
    "TR06": dict(legacy="LINE-F", bay="South", comm=2016, vessels=96, epv=7, model="TM820M-400", header="HDR-S1"),
    "TR07": dict(legacy="LINE-G", bay="South", comm=2015, vessels=96, epv=7, model="TM820M-400", header="HDR-S2"),
    "TR08": dict(legacy="LINE-H", bay="South", comm=2022, vessels=96, epv=7, model="TM820M-440", header="HDR-S2"),
}

LEGACY_TO_TRAIN = {m["legacy"]: u for u, m in TRAIN_META.items()}
START_2026 = dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)


def _fmt_utc(t_dt):
    return t_dt.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _fmt_lisbon(t_dt):
    return t_dt.astimezone(LISBON).isoformat()


def _write_csv(path, header, rows):
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        w.writerow(header)
        w.writerows(rows)
    return len(rows)


def _build_reservoir_xlsx(path, rng):
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Weekly_Storage_2026"

    hdr_fill = PatternFill("solid", fgColor="1F4E78")
    hdr_font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
    body_font = Font(name="Calibri", size=10, color="111111")
    thin = Side(style="thin", color="D0D7DE")
    border = Border(left=thin, right=thin, top=thin, bottom=thin)

    headers = [
        "week_ending_date",
        "odelouca_pct_full",
        "bravura_pct_full",
        "funcho_pct_full",
        "beliche_pct_full",
        "barlavento_basin_hm3",
        "municipal_offtake_hm3",
    ]
    ws.append(headers)
    for col_i in range(1, len(headers) + 1):
        c = ws.cell(row=1, column=col_i)
        c.fill = hdr_fill
        c.font = hdr_font
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = border

    od, br, fu, be = 48.2, 21.6, 54.5, 42.1
    d0 = dt.date(2026, 1, 4)
    for w_idx in range(52):
        wk_d = d0 + dt.timedelta(days=7 * w_idx)
        seas = math.cos(2.0 * math.pi * (w_idx - 10) / 52.0)
        rain = max(0.0, 0.85 * seas + rng.gauss(0.25, 0.45))
        draw = 0.65 + 0.55 * max(0.0, -seas) + rng.gauss(0.0, 0.08)
        od = max(18.0, min(88.0, od + 0.9 * rain - 0.85 * draw))
        br = max(9.5, min(68.0, br + 0.7 * rain - 0.75 * draw))
        fu = max(22.0, min(91.0, fu + 1.0 * rain - 0.80 * draw))
        be = max(16.0, min(85.0, be + 0.8 * rain - 0.72 * draw))
        basin_hm3 = round(1.34 * od + 0.35 * br + 0.48 * fu + 0.48 * be, 2)
        offtake = round(1.15 + 0.62 * max(0.0, -seas) + rng.gauss(0.0, 0.05), 3)
        row_vals = [
            wk_d.isoformat(),
            round(od, 2),
            round(br, 2),
            round(fu, 2),
            round(be, 2),
            basin_hm3,
            offtake,
        ]
        ws.append(row_vals)
        r_idx = w_idx + 2
        for col_i in range(1, len(headers) + 1):
            c = ws.cell(row=r_idx, column=col_i)
            c.font = body_font
            c.border = border
            if col_i == 1:
                c.alignment = Alignment(horizontal="center")
            elif col_i <= 5:
                c.number_format = "0.00"
                c.alignment = Alignment(horizontal="right")
            elif col_i == 6:
                c.number_format = "#,##0.00"
                c.alignment = Alignment(horizontal="right")
            else:
                c.number_format = "0.000"
                c.alignment = Alignment(horizontal="right")

    ws.freeze_panes = "A2"
    widths = [18, 18, 17, 17, 17, 22, 22]
    for idx, w in enumerate(widths, 1):
        ws.column_dimensions[get_column_letter(idx)].width = w
    wb.save(path)
    return 52


def build(target_dir, world=None):
    """Build the 13 non-PDF files in target_dir. Returns a dict of row counts."""
    data = world if world is not None else core.simulate_world(core.SEED)
    rng = random.Random(core.SEED + 7701)
    counts = {}

    # 1. train_asset_register.csv
    reg_rows = []
    for u in core.TRAINS:
        m = TRAIN_META[u]
        wp = core.WORLD[u]
        reg_rows.append([
            u,
            m["legacy"],
            m["bay"],
            m["comm"],
            m["vessels"],
            m["epv"],
            int(round(wp["v_nom"])),
            m["model"],
            m["header"],
        ])
    counts[FILES["asset_reg"]] = _write_csv(
        os.path.join(target_dir, FILES["asset_reg"]),
        [
            "train_id",
            "legacy_tag",
            "plant_bay",
            "commission_year",
            "pressure_vessels",
            "elements_per_vessel",
            "pretreatment_nominal_m3",
            "membrane_model",
            "feed_header_line",
        ],
        reg_rows,
    )

    # 2. operating_plan_2027.csv
    plan_rows = []
    q_labels = ["2027-Q1", "2027-Q2", "2027-Q3", "2027-Q4"]
    q_edges = core.Q_EDGES_H
    for u in core.TRAINS:
        sr = core.PLAN_SCHED_RATIO[u]
        qh_flow = data["trains"][u]["q_flow_h"]
        for q in range(4):
            cal_h = core.Q_HOURS[q]
            q_feed_m3 = float(qh_flow[q_edges[q]:q_edges[q + 1]].sum())
            out26_km3 = int(round(q_feed_m3 * 0.45 / 1000.0))
            out27_km3 = round(out26_km3 * sr[q], 2)
            plan_rows.append([
                u,
                q_labels[q],
                cal_h,
                out26_km3,
                f"{out27_km3:.2f}",
                f"{sr[q]:.4f}",
                f"{core.PLAN_BORON_TEMP_Q[q]:.4f}",
                f"{core.PLAN_SCALING_REC_Q[q]:.4f}",
                f"{core.PLAN_TDS_SAL_Q[q]:.4f}",
            ])
    counts[FILES["op_plan"]] = _write_csv(
        os.path.join(target_dir, FILES["op_plan"]),
        [
            "train_id",
            "quarter",
            "calendar_hours_2026",
            "baseline_output_2026_km3",
            "scheduled_output_2027_km3",
            "dispatch_duty_ratio_2027",
            "boron_thermal_factor_2027",
            "scaling_recovery_factor_2027",
            "salinity_thermal_factor_2027",
        ],
        plan_rows,
    )

    # 3. autosampler_schedule_2026.csv
    auto_rows = []
    ops = ["FN", "IG", "DM", "BL", "VF"]
    for day in range(core.DAYS_2026):
        cur_d = dt.date(2026, 1, 1) + dt.timedelta(days=day)
        m_hrs = 8 if ((3 + day) % 7) in (1, 2) else 4
        prog = "PROG_4H_STD" if m_hrs == 4 else "PROG_8H_EXT"
        bpd = 24 // m_hrs
        wk = day // 7
        op_north = ops[wk % 3]
        op_south = ops[2 + (wk % 3)]
        for u in core.TRAINS:
            tcode = TRAIN_META[u]["legacy"] if day < 90 else u
            base_op = op_north if TRAIN_META[u]["bay"] == "North" else op_south
            op = rng.choice(ops) if rng.random() < 0.14 else base_op
            auto_rows.append([
                cur_d.isoformat(),
                tcode,
                prog,
                bpd,
                m_hrs,
                "FLOW_PROPORTIONAL",
                op,
            ])
    counts[FILES["autosampler"]] = _write_csv(
        os.path.join(target_dir, FILES["autosampler"]),
        [
            "schedule_date",
            "train_code",
            "carousel_program",
            "bottles_per_day",
            "bottle_span_hours",
            "sampling_mode",
            "operator_initials",
        ],
        auto_rows,
    )

    # 4. permeate_boron_composites_2026.csv (15,024 clean + ~2.8% superseded QA revision 1 rows)
    boron_rows = []
    superseded_count = 0
    for u in core.TRAINS:
        td = data["trains"][u]
        meta = TRAIN_META[u]
        is_south = meta["bay"] == "South"
        bench = "ICP-OES-B2" if is_south else "ICP-OES-B1"
        cd, cs, cv = td["comp_day"], td["comp_slot"], td["comp_val"]
        for idx in range(len(cv)):
            day = int(cd[idx])
            slot = int(cs[idx]) + 1
            cur_d = dt.date(2026, 1, 1) + dt.timedelta(days=day)
            d_str = cur_d.strftime("%d/%m/%Y") if is_south else cur_d.isoformat()
            tcode = meta["legacy"] if (day < 90 and u in ("TR02", "TR06")) else u
            sid = f"B26-{u}-{day + 1:03d}-S{slot}"
            batch_id = f"LIMS-26W{min(52, (day // 7) + 1):02d}-{meta['bay'][0]}"
            val_mg = float(cv[idx])

            if rng.random() < 0.0283:
                superseded_count += 1
                prelim_mg = max(0.05, val_mg + rng.choice([-1.0, 1.0]) * rng.uniform(0.011, 0.024))
                if is_south:
                    boron_rows.append([sid, tcode, d_str, slot, f"{prelim_mg * 1000.0:.3f}", "ug/L", 1, batch_id + "P", bench])
                else:
                    boron_rows.append([sid, tcode, d_str, slot, f"{prelim_mg:.6f}", "mg/L", 1, batch_id + "P", bench])
                rev = 2
            else:
                rev = 1

            if is_south:
                boron_rows.append([sid, tcode, d_str, slot, f"{val_mg * 1000.0:.3f}", "ug/L", rev, batch_id, bench])
            else:
                boron_rows.append([sid, tcode, d_str, slot, f"{val_mg:.6f}", "mg/L", rev, batch_id, bench])

    counts[FILES["boron_comp"]] = _write_csv(
        os.path.join(target_dir, FILES["boron_comp"]),
        [
            "sample_id",
            "train_code",
            "collection_date",
            "carousel_slot",
            "boron_conc",
            "unit",
            "qa_revision",
            "lims_batch_id",
            "lab_bench",
        ],
        boron_rows,
    )
    counts["_boron_superseded"] = superseded_count

    # 5 & 6. intake_chemistry_15m_2026.csv & ro_feed_header_15m_2026.csv (280,320 clean + ~0.3% dup frames each)
    ts_15_strs = [_fmt_utc(START_2026 + dt.timedelta(minutes=15 * i)) for i in range(core.STEPS_15M)]

    intake_path = os.path.join(target_dir, FILES["intake_15m"])
    ro_path = os.path.join(target_dir, FILES["ro_feed_15m"])
    n_in = 0
    n_ro = 0
    dup_in = 0
    dup_ro = 0

    burn_rng = random.Random(core.SEED + 9901)
    with open(intake_path, "w", encoding="utf-8", newline="") as fin, \
         open(ro_path, "w", encoding="utf-8", newline="") as fro:
        win = csv.writer(fin, lineterminator="\n")
        wro = csv.writer(fro, lineterminator="\n")
        win.writerow(["ts_utc", "train_id", "intake_cond_ms_cm", "intake_tep_z_index", "frame_seq"])
        wro.writerow(["ts_utc", "train_id", "ro_feed_cond_ms_cm", "ro_feed_stress_idx", "frame_seq"])
        seq_in = 100001
        seq_ro = 500001
        for u in core.TRAINS:
            td = data["trains"][u]
            cin = td["c_in"]
            xin = td["x_in"]
            cout = [float(v) for v in td["c_out"]]
            yout = [float(v) for v in td["y_stress"]]
            # Smooth strictly inside excluded Clause 2.2 burn-in (i < 32) where phi_lag <= 0 clamped opening rows
            k0 = 1
            while k0 < core.BURN_IN_15M and abs(yout[k0] - yout[0]) < 1e-12:
                k0 += 1
            if k0 > 1:
                yc = yout[k0]
                cc = cout[k0]
                for j in range(k0 - 1, -1, -1):
                    yc = 0.85 * yc + burn_rng.gauss(0.0, 0.28)
                    cc = 52.0 + 0.88 * (cc - 52.0) + burn_rng.gauss(0.0, 0.35)
                    yout[j] = yc
                    cout[j] = cc
            for i in range(core.STEPS_15M):
                ts = ts_15_strs[i]
                row_in = [ts, u, f"{float(cin[i]):.5f}", f"{float(xin[i]):.5f}", seq_in]
                win.writerow(row_in)
                n_in += 1
                seq_in += 1
                if rng.random() < 0.003:
                    win.writerow([ts, u, f"{float(cin[i]):.5f}", f"{float(xin[i]):.5f}", seq_in])
                    n_in += 1
                    dup_in += 1
                    seq_in += 1

                row_ro = [ts, u, f"{cout[i]:.5f}", f"{yout[i]:.5f}", seq_ro]
                wro.writerow(row_ro)
                n_ro += 1
                seq_ro += 1
                if rng.random() < 0.003:
                    wro.writerow([ts, u, f"{cout[i]:.5f}", f"{yout[i]:.5f}", seq_ro])
                    n_ro += 1
                    dup_ro += 1
                    seq_ro += 1

    counts[FILES["intake_15m"]] = n_in
    counts[FILES["ro_feed_15m"]] = n_ro
    counts["_intake_dups"] = dup_in
    counts["_ro_dups"] = dup_ro

    # 7. train_hydraulics_hourly_2026.csv (70,080 clean + ~0.26% duplicate SCADA poll rows)
    ts_h_strs = [_fmt_utc(START_2026 + dt.timedelta(hours=t)) for t in range(core.HOURS_2026)]
    hyd_rows = []
    hyd_dups = 0
    for u in core.TRAINS:
        td = data["trains"][u]
        meta = TRAIN_META[u]
        is_south = meta["bay"] == "South"
        qh = td["q_flow_h"]
        for t in range(core.HOURS_2026):
            ts = ts_h_strs[t]
            q_m3h = float(qh[t])
            seas_p = 1.4 * math.cos(2.0 * math.pi * (t - 400) / 8760.0)
            p_bar = 57.5 + 0.0085 * q_m3h + seas_p + rng.gauss(0.0, 0.22)
            if is_south:
                f_val = f"{q_m3h / 3.6:.6f}"
                f_unit = "L/s"
            else:
                f_val = f"{q_m3h:.5f}"
                f_unit = "m3/h"
            hyd_rows.append([ts, u, f_val, f_unit, f"{p_bar:.2f}", "OK"])
            if rng.random() < 0.0026:
                hyd_rows.append([ts, u, f_val, f_unit, f"{p_bar:.2f}", "RETRY_OK"])
                hyd_dups += 1

    counts[FILES["hydraulics_h"]] = _write_csv(
        os.path.join(target_dir, FILES["hydraulics_h"]),
        ["ts_utc", "train_id", "feed_flow", "flow_unit", "feed_pressure_bar", "poll_status"],
        hyd_rows,
    )
    counts["_hyd_dups"] = hyd_dups

    # 8. bay_permeate_tds_hourly_2026.csv (17,520 clean rows across North & South Bay + ~0.25% exact PLC retries)
    bay_rows = []
    bay_dups = 0
    for bay_name in ("North", "South"):
        bd = data["bays"][bay_name]
        qt = bd["q_tot_h"]
        ct = bd["collector_tds_h"]
        for t in range(core.HOURS_2026):
            ts = ts_h_strs[t]
            perm_q = f"{0.45 * float(qt[t]):.4f}"
            tds_v = f"{float(ct[t]):.4f}"
            bay_rows.append([ts, bay_name, perm_q, tds_v, "OK"])
            if rng.random() < 0.0025:
                bay_rows.append([ts, bay_name, perm_q, tds_v, "RETRY_OK"])
                bay_dups += 1
    counts[FILES["bay_tds_h"]] = _write_csv(
        os.path.join(target_dir, FILES["bay_tds_h"]),
        ["ts_utc", "bay_id", "bay_permeate_flow_m3_h", "collector_tds_mg_l", "poll_status"],
        bay_rows,
    )
    counts["_bay_tds_dups"] = bay_dups

    # 9. shift_diagnostics_2026.csv (70,080 hourly rows = 8 trains x 8,760 h, Europe/Lisbon ISO timestamps with explicit offset)
    shift_names = ["S1_0008", "S2_0816", "S3_1624"]
    ts_sh_lisbon = [_fmt_lisbon(START_2026 + dt.timedelta(hours=h)) for h in range(core.HOURS_2026)]
    sh_rows = []
    for u in core.TRAINS:
        td = data["trains"][u]
        d1_a, d2_a, d3_a = td["d1"], td["d2"], td["d3"]
        for h in range(core.HOURS_2026):
            sh_rows.append([
                ts_sh_lisbon[h],
                u,
                shift_names[(START_2026 + dt.timedelta(hours=h)).astimezone(LISBON).hour // 8],
                int(d1_a[h]),
                int(d2_a[h]),
                int(d3_a[h]),
            ])
    counts[FILES["shift_diag"]] = _write_csv(
        os.path.join(target_dir, FILES["shift_diag"]),
        [
            "block_start_lisbon",
            "train_id",
            "shift_code",
            "salt_passage_alarm",
            "stage_dp_alarm",
            "acoustic_bypass_alarm",
        ],
        sh_rows,
    )

    # 10. cip_wash_log_2026.csv (~551 alternating alkaline/acid inline chemical flushes incl. 16 late-Dec 2025 carry-over baseline washes)
    cip_events = []
    techs = [PEOPLE["maint"], PEOPLE["hydraulics"], PEOPLE["compliance"], PEOPLE["analyst"]]
    for u in core.TRAINS:
        td = data["trains"][u]
        meta = TRAIN_META[u]
        for h_ev, recipe in td["cip_events"]:
            t_dt = START_2026 + dt.timedelta(hours=h_ev)
            tcode = meta["legacy"] if h_ev < 4344 else u
            soak_h = round(rng.uniform(0.4, 0.9), 1)
            cip_events.append((t_dt, u, h_ev, tcode, recipe, soak_h))
    cip_events.sort(key=lambda e: (e[0], e[1]))
    cip_rows = []
    c25 = 0
    c26 = 0
    for t_dt, _u, h_ev, tcode, recipe, soak_h in cip_events:
        if h_ev < 0:
            c25 += 1
            wid = f"CIP-2025-{900 + c25:04d}"
            idx_t = c25
        else:
            c26 += 1
            wid = f"CIP-2026-{c26:04d}"
            idx_t = c26
        cip_rows.append([
            wid,
            tcode,
            _fmt_lisbon(t_dt),
            recipe,
            f"{soak_h:.1f}",
            techs[(idx_t + abs(h_ev)) % len(techs)],
        ])
    counts[FILES["cip_log"]] = _write_csv(
        os.path.join(target_dir, FILES["cip_log"]),
        [
            "wash_id",
            "train_code",
            "wash_completed_lisbon",
            "chemical_stage",
            "soak_duration_h",
            "technician",
        ],
        cip_rows,
    )

    # 11. scada_bay_config_2026.json (authentic PLC/historian config; ZERO post-CIP window hint!)
    cfg = {
        "facility": ORG,
        "station": "Estacao Dessalinizadora de Alvor",
        "region": "Algarve, Portugal",
        "config_effective_date": "2026-01-01",
        "historian_export_timezone": "UTC",
        "mes_shift_and_maintenance_timezone": "Europe/Lisbon",
        "historian_supervisor": PEOPLE["scada"],
        "nominal_permeate_recovery": 0.45,
        "bays": {
            "North": {
                "trains": ["TR01", "TR02", "TR03", "TR04"],
                "plc_cluster": "PLC-N-S71500",
                "flow_telemetry_unit": "m3/h",
                "lims_boron_bench": "ICP-OES-B1",
                "lims_boron_unit": "mg/L",
                "lims_date_format": "ISO-8601 (YYYY-MM-DD)",
                "permeate_collector_tag": "COLL-N-TDS01",
            },
            "South": {
                "trains": ["TR05", "TR06", "TR07", "TR08"],
                "plc_cluster": "PLC-S-S71500",
                "flow_telemetry_unit": "L/s",
                "lims_boron_bench": "ICP-OES-B2",
                "lims_boron_unit": "ug/L",
                "lims_date_format": "Portuguese local (DD/MM/YYYY)",
                "permeate_collector_tag": "COLL-S-TDS01",
            },
        },
        "autosampler_programs": {
            "PROG_4H_STD": {"bottles_per_day": 6, "window_hours": 4, "mode": "flow-proportional"},
            "PROG_8H_EXT": {"bottles_per_day": 3, "window_hours": 8, "mode": "flow-proportional"},
        },
        "telemetry_cadence_minutes": {
            "header_chemistry": 15,
            "feed_hydraulics": 60,
            "bay_permeate_tds": 60,
            "integrity_alarms": 60,
        },
        "inline_sensor_qa": {
            "bay_collector_tds_repeatability_mg_l": core.TDS_METER_SD,
        },
        "cip_protocol": {
            "cip_recipes": ["CIP_ALK_pH11", "CIP_ACID_pH2"],
        },
    }
    with open(os.path.join(target_dir, FILES["scada_cfg"]), "w", encoding="utf-8", newline="\n") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")
    counts[FILES["scada_cfg"]] = 1

    # 12. mibel_iberian_power_spot_2026.csv (Unlabelled Distractor #1: 8,760 hourly Iberian electricity prices)
    mibel_rows = []
    m_ar = 0.0
    for t in range(core.HOURS_2026):
        hr = t % 24
        seas_m = 14.0 * math.cos(2.0 * math.pi * (t - 200) / 8760.0)
        diurnal = -24.0 * math.exp(-((hr - 13.5) ** 2) / 10.0) + 28.0 * math.exp(-((hr - 20.5) ** 2) / 6.0)
        m_ar = 0.88 * m_ar + rng.gauss(0.0, 5.5)
        price = max(4.5, 68.0 + seas_m + diurnal + m_ar)
        mibel_rows.append([ts_h_strs[t], "PT_MIBEL", f"{price:.2f}", "EUR/MWh"])
    counts[FILES["dist_mibel"]] = _write_csv(
        os.path.join(target_dir, FILES["dist_mibel"]),
        ["ts_utc", "market_zone", "day_ahead_price", "currency_unit"],
        mibel_rows,
    )

    # 13. algarve_reservoir_levels_2026.xlsx (Unlabelled Distractor #2: 52 weekly reservoir rows)
    counts[FILES["dist_reservoir"]] = _build_reservoir_xlsx(
        os.path.join(target_dir, FILES["dist_reservoir"]), rng
    )

    return counts


if __name__ == "__main__":
    out_d = os.path.join(os.path.dirname(HERE), "target")
    os.makedirs(out_d, exist_ok=True)
    print(build(out_d))
