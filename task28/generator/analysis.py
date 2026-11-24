#!/usr/bin/env python3
"""task28/generator/analysis.py (v3): Read ONLY shipped files under target/ (performing full
Layer 1 cleaning across all 15 files), recompute every v3 physical estimator (S1..S4), all 29
defensible physical variants, all 8 +/-20% forcing perturbations, the full 15-corner stump
lattice, exact Round-2 3.5h Response 1 & Response 2 rigorous routes, all run/cutoff/hedge/over
routes, all 4 coded one-fact shortcut routes, and native-unit F1-F4 chi-squared falsification.

Zero calls to core.simulate_world(): every operational array, threshold, energy rate, bay
assignment, and 2027 plan multiplier is read directly from the shipped files under target/.
"""
import csv
import datetime as dt
import itertools
import json
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import core  # noqa: E402
import pack as PK  # noqa: E402

UTC = dt.timezone.utc
START_2026 = dt.datetime(2026, 1, 1, 0, 0, 0, tzinfo=UTC)
DATE_2026_01_01 = dt.date(2026, 1, 1)


def _parse_date(s):
    s = s.strip()
    if "/" in s:
        d, m, y = s.split("/")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s[:10])


def _parse_iso_utc(s):
    s = s.strip()
    if s.endswith("Z"):
        s = s[:-1] + "+00:00"
    return dt.datetime.fromisoformat(s).astimezone(UTC)


def load_clean_from_target(target_dir):
    """Load and clean every operational file from target_dir without calling core.simulate_world()."""
    F = PK.FILES
    cleaning = {}

    # 1. Asset register (crosswalk + plant_bay + V_nom)
    legacy_map = {}
    v_nom = {}
    train_bay = {}
    bays_members = {"North": [], "South": []}
    asset_rows = {}
    with open(os.path.join(target_dir, F["asset_reg"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            u = r["train_id"].strip()
            legacy_map[r["legacy_tag"].strip()] = u
            legacy_map[u] = u
            v_nom[u] = float(r["pretreatment_nominal_m3"])
            bay = r["plant_bay"].strip()
            train_bay[u] = bay
            bays_members[bay].append(u)
            asset_rows[u] = r
    cleaning["trains_in_register"] = len(asset_rows)

    # 2. SCADA config (verify probe repeatability SD from shipped JSON)
    with open(os.path.join(target_dir, F["scada_cfg"]), encoding="utf-8") as f:
        scada_cfg = json.load(f)
    tds_meter_sd = float(scada_cfg["inline_sensor_qa"]["bay_collector_tds_repeatability_mg_l"])

    # 3. 2027 Operating Plan
    plan_sched = {u: [0.0] * 4 for u in core.TRAINS}
    plan_btemp = [0.0] * 4
    plan_srec = [0.0] * 4
    plan_tsal = [0.0] * 4
    q_hours = [0] * 4
    q_map = {"2027-Q1": 0, "2027-Q2": 1, "2027-Q3": 2, "2027-Q4": 3}
    with open(os.path.join(target_dir, F["op_plan"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            u = r["train_id"].strip()
            q = q_map[r["quarter"].strip()]
            plan_sched[u][q] = float(r["dispatch_duty_ratio_2027"])
            plan_btemp[q] = float(r["boron_thermal_factor_2027"])
            plan_srec[q] = float(r["scaling_recovery_factor_2027"])
            plan_tsal[q] = float(r["salinity_thermal_factor_2027"])
            q_hours[q] = int(r["calendar_hours_2026"])

    n_h = sum(q_hours)
    n_15 = n_h * 4
    n_4h = n_h // 4
    q_edges = [0]
    for h in q_hours:
        q_edges.append(q_edges[-1] + h)
    q_idx_h = np.zeros(n_h, dtype=np.int32)
    for q in range(4):
        q_idx_h[q_edges[q]:q_edges[q + 1]] = q

    # 4. Hourly SCADA hydraulics (needed for S1 Q_bar_k, S2 Phi(t), and S4 bay flow shares w_{u,t})
    q_flow_map = {u: np.full(n_h, np.nan, dtype=float) for u in core.TRAINS}
    hyd_raw = 0
    hyd_dups = 0
    hyd_ls = 0
    with open(os.path.join(target_dir, F["hydraulics_h"]), encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr[:4] == ["ts_utc", "train_id", "feed_flow", "flow_unit"]
        h_cache = {}
        for row in rd:
            hyd_raw += 1
            ts_s, u = row[0], row[1]
            idx = h_cache.get(ts_s)
            if idx is None:
                idx = int((_parse_iso_utc(ts_s) - START_2026).total_seconds() // 3600)
                h_cache[ts_s] = idx
            if not math.isnan(q_flow_map[u][idx]):
                hyd_dups += 1
                continue
            val = float(row[2])
            unit = row[3].strip()
            if unit == "L/s":
                hyd_ls += 1
                val = val * 3.6
            elif unit != "m3/h":
                raise ValueError(f"Unexpected flow unit {unit}")
            q_flow_map[u][idx] = val
    cleaning["hydraulics_raw_rows"] = hyd_raw
    cleaning["hydraulics_clean_rows"] = hyd_raw - hyd_dups
    cleaning["hydraulics_dups_dropped"] = hyd_dups
    cleaning["hydraulics_ls_rows"] = hyd_ls

    # 5. Hourly shared North/South Bay permeate collector TDS
    bay_tds_map = {b: np.full(n_h, np.nan, dtype=float) for b in ("North", "South")}
    bay_perm_q = {b: np.full(n_h, np.nan, dtype=float) for b in ("North", "South")}
    bay_raw = 0
    bay_dups = 0
    with open(os.path.join(target_dir, F["bay_tds_h"]), encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr[:4] == ["ts_utc", "bay_id", "bay_permeate_flow_m3_h", "collector_tds_mg_l"]
        for row in rd:
            bay_raw += 1
            ts_s, b = row[0], row[1]
            idx = h_cache.get(ts_s)
            if idx is None:
                idx = int((_parse_iso_utc(ts_s) - START_2026).total_seconds() // 3600)
                h_cache[ts_s] = idx
            if not math.isnan(bay_tds_map[b][idx]):
                bay_dups += 1
                continue
            bay_perm_q[b][idx] = float(row[2])
            bay_tds_map[b][idx] = float(row[3])
    cleaning["bay_tds_raw_rows"] = bay_raw
    cleaning["bay_tds_clean_rows"] = bay_raw - bay_dups
    cleaning["bay_tds_dups_dropped"] = bay_dups

    # 6. Autosampler schedule
    span_map = {}
    auto_legacy = 0
    auto_rows = 0
    with open(os.path.join(target_dir, F["autosampler"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            auto_rows += 1
            raw_u = r["train_code"].strip()
            if raw_u.startswith("LINE-"):
                auto_legacy += 1
            u = legacy_map[raw_u]
            day = (_parse_date(r["schedule_date"]) - DATE_2026_01_01).days
            span_map[(u, day)] = int(r["bottle_span_hours"])
    cleaning["autosampler_rows"] = auto_rows
    cleaning["autosampler_legacy_tags"] = auto_legacy

    # 7. Permeate boron composites (dedup qa_revision, convert ug/L -> mg/L, parse DD/MM/YYYY)
    boron_raw = 0
    boron_ug = 0
    boron_legacy = 0
    boron_dmy = 0
    best_by_sid = {}
    with open(os.path.join(target_dir, F["boron_comp"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            boron_raw += 1
            sid = r["sample_id"].strip()
            rev = int(r["qa_revision"])
            raw_u = r["train_code"].strip()
            if raw_u.startswith("LINE-"):
                boron_legacy += 1
            u = legacy_map[raw_u]
            ds = r["collection_date"].strip()
            if "/" in ds:
                boron_dmy += 1
            day = (_parse_date(ds) - DATE_2026_01_01).days
            slot = int(r["carousel_slot"]) - 1  # 0-indexed matching core.py
            val = float(r["boron_conc"])
            unit = r["unit"].strip()
            if unit == "ug/L":
                boron_ug += 1
                val = val / 1000.0
            elif unit != "mg/L":
                raise ValueError(f"Unexpected boron unit {unit}")
            prev = best_by_sid.get(sid)
            if prev is None or rev > prev[0]:
                best_by_sid[sid] = (rev, u, day, slot, val, "/" in ds, unit == "ug/L")
    cleaning["boron_raw_rows"] = boron_raw
    cleaning["boron_clean_rows"] = len(best_by_sid)
    cleaning["boron_superseded_dropped"] = boron_raw - len(best_by_sid)
    cleaning["boron_ug_rows"] = boron_ug
    cleaning["boron_ug_clean_rows"] = sum(1 for x in best_by_sid.values() if x[6])
    cleaning["boron_legacy_rows"] = boron_legacy
    cleaning["boron_dmy_rows"] = boron_dmy
    cleaning["boron_dmy_clean_rows"] = sum(1 for x in best_by_sid.values() if x[5])
    cleaning["boron_min_comp_mg_l"] = round(min(x[4] for x in best_by_sid.values()), 4)
    cleaning["boron_sub_loq_count"] = sum(1 for x in best_by_sid.values() if x[4] < 0.020)

    comp_by_u = {u: [] for u in core.TRAINS}
    for _rev, u, day, slot, val, _dmy, _ug in best_by_sid.values():
        m = span_map[(u, day)]
        h0 = day * 24 + slot * m
        qd = int(q_idx_h[h0])
        qbar = float(np.mean(q_flow_map[u][h0:h0 + m]))
        comp_by_u[u].append((day, slot, m, qd, h0, val, qbar))
    for u in core.TRAINS:
        comp_by_u[u].sort(key=lambda x: (x[0], x[1]))

    # 8. 15-min intake & RO-feed chemistry
    c_in_map = {u: np.full(n_15, np.nan, dtype=float) for u in core.TRAINS}
    x_in_map = {u: np.full(n_15, np.nan, dtype=float) for u in core.TRAINS}
    c_out_map = {u: np.full(n_15, np.nan, dtype=float) for u in core.TRAINS}
    y_out_map = {u: np.full(n_15, np.nan, dtype=float) for u in core.TRAINS}
    in_raw = 0
    in_dups = 0
    ts_15_cache = {}
    with open(os.path.join(target_dir, F["intake_15m"]), encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr[:4] == ["ts_utc", "train_id", "intake_cond_ms_cm", "intake_tep_z_index"]
        for row in rd:
            in_raw += 1
            ts_s, u = row[0], row[1]
            idx = ts_15_cache.get(ts_s)
            if idx is None:
                idx = int((_parse_iso_utc(ts_s) - START_2026).total_seconds() // 900)
                ts_15_cache[ts_s] = idx
            if not math.isnan(c_in_map[u][idx]):
                in_dups += 1
                continue
            c_in_map[u][idx] = float(row[2])
            x_in_map[u][idx] = float(row[3])
    cleaning["intake_raw_rows"] = in_raw
    cleaning["intake_clean_rows"] = in_raw - in_dups
    cleaning["intake_dups_dropped"] = in_dups

    ro_raw = 0
    ro_dups = 0
    with open(os.path.join(target_dir, F["ro_feed_15m"]), encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr[:4] == ["ts_utc", "train_id", "ro_feed_cond_ms_cm", "ro_feed_stress_idx"]
        for row in rd:
            ro_raw += 1
            ts_s, u = row[0], row[1]
            idx = ts_15_cache.get(ts_s)
            if idx is None:
                idx = int((_parse_iso_utc(ts_s) - START_2026).total_seconds() // 900)
                ts_15_cache[ts_s] = idx
            if not math.isnan(c_out_map[u][idx]):
                ro_dups += 1
                continue
            c_out_map[u][idx] = float(row[2])
            y_out_map[u][idx] = float(row[3])
    cleaning["ro_feed_raw_rows"] = ro_raw
    cleaning["ro_feed_clean_rows"] = ro_raw - ro_dups
    cleaning["ro_feed_dups_dropped"] = ro_dups

    # 9. 1-hour inline shift diagnostics (70,080 rows = 8 trains x 8,760 h)
    d1_map = {u: np.zeros(n_h, dtype=np.int8) for u in core.TRAINS}
    d2_map = {u: np.zeros(n_h, dtype=np.int8) for u in core.TRAINS}
    d3_map = {u: np.zeros(n_h, dtype=np.int8) for u in core.TRAINS}
    triples_map = {u: np.zeros(n_h, dtype=np.int32) for u in core.TRAINS}
    sh_rows = 0
    sh_cache = {}
    with open(os.path.join(target_dir, F["shift_diag"]), encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr[:6] == [
            "block_start_lisbon", "train_id", "shift_code",
            "salt_passage_alarm", "stage_dp_alarm", "acoustic_bypass_alarm",
        ]
        for row in rd:
            sh_rows += 1
            ts_s, u = row[0], row[1]
            h = sh_cache.get(ts_s)
            if h is None:
                h = int(round((_parse_iso_utc(ts_s) - START_2026).total_seconds() / 3600.0))
                sh_cache[ts_s] = h
            a1, a2, a3 = int(row[3]), int(row[4]), int(row[5])
            d1_map[u][h] = a1
            d2_map[u][h] = a2
            d3_map[u][h] = a3
            triples_map[u][h] = (a1 << 2) | (a2 << 1) | a3
    cleaning["shift_rows"] = sh_rows

    # 10. CIP wash log (with late-Dec 2025 carry-over baseline washes for exact Jan-1 age)
    cip_by_u = {u: [] for u in core.TRAINS}
    cip_rows = 0
    cip_legacy = 0
    cip_alk = 0
    cip_acid = 0
    cip_carryover_2025 = 0
    with open(os.path.join(target_dir, F["cip_log"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cip_rows += 1
            raw_u = r["train_code"].strip()
            if raw_u.startswith("LINE-"):
                cip_legacy += 1
            u = legacy_map[raw_u]
            h_ev = int(round((_parse_iso_utc(r["wash_completed_lisbon"]) - START_2026).total_seconds() / 3600.0))
            rec = r["chemical_stage"].strip()
            if rec == "CIP_ALK_pH11":
                cip_alk += 1
            elif rec == "CIP_ACID_pH2":
                cip_acid += 1
            else:
                raise ValueError(f"Unexpected chemical_stage {rec}")
            if h_ev < 0:
                cip_carryover_2025 += 1
            cip_by_u[u].append((h_ev, rec))
    cleaning["cip_rows"] = cip_rows
    cleaning["cip_legacy_rows"] = cip_legacy
    cleaning["cip_alk_washes"] = cip_alk
    cleaning["cip_acid_washes"] = cip_acid
    cleaning["cip_carryover_2025"] = cip_carryover_2025

    # Assemble cleaned data dict matching core.py estimator interface
    trains = {}
    for u in core.TRAINS:
        rows_u = comp_by_u[u]
        evs = sorted(cip_by_u[u], key=lambda x: x[0])
        alk_pre = [h_ev for h_ev, rec in evs if h_ev < 0 and rec == "CIP_ALK_pH11"]
        acid_pre = [h_ev for h_ev, rec in evs if h_ev < 0 and rec == "CIP_ACID_pH2"]
        cur_alk = max(alk_pre) if alk_pre else -1000
        cur_acid = max(acid_pre) if acid_pre else -1000
        ev_map = {h_ev: rec for h_ev, rec in evs if h_ev >= 0}
        dt_alk_h = np.empty(n_h, dtype=float)
        dt_acid_h = np.empty(n_h, dtype=float)
        for h in range(n_h):
            if h in ev_map:
                if ev_map[h] == "CIP_ALK_pH11":
                    cur_alk = h
                else:
                    cur_acid = h
            dt_alk_h[h] = float(h - cur_alk)
            dt_acid_h[h] = float(h - cur_acid)

        trains[u] = {
            "q_flow_h": q_flow_map[u],
            "comp_day": np.array([x[0] for x in rows_u], dtype=np.int32),
            "comp_slot": np.array([x[1] for x in rows_u], dtype=np.int32),
            "comp_m": np.array([x[2] for x in rows_u], dtype=np.int32),
            "comp_q": np.array([x[3] for x in rows_u], dtype=np.int32),
            "comp_h0": np.array([x[4] for x in rows_u], dtype=np.int32),
            "comp_val": np.array([x[5] for x in rows_u], dtype=float),
            "comp_qbar": np.array([x[6] for x in rows_u], dtype=float),
            "c_in": c_in_map[u],
            "x_in": x_in_map[u],
            "c_out": c_out_map[u],
            "y_stress": y_out_map[u],
            "cip_events": evs,
            "dt_alk_h": dt_alk_h,
            "dt_acid_h": dt_acid_h,
            "triples": triples_map[u],
            "d1": d1_map[u],
            "d2": d2_map[u],
            "d3": d3_map[u],
        }

    bays = {}
    for bay_name in ("North", "South"):
        members = bays_members[bay_name]
        q_mat = np.column_stack([trains[u]["q_flow_h"] for u in members])
        q_tot = np.sum(q_mat, axis=1)
        w_mat = q_mat / q_tot[:, None]
        bays[bay_name] = {
            "members": members,
            "q_tot_h": q_tot,
            "w_mat": w_mat,
            "collector_tds_h": bay_tds_map[bay_name],
            "permeate_flow_h": bay_perm_q[bay_name],
        }

    plan = {
        "sched_ratio": plan_sched,
        "boron_temp_q": plan_btemp,
        "scaling_rec_q": plan_srec,
        "tds_sal_q": plan_tsal,
        "q_hours": q_hours,
        "v_nom": v_nom,
        "tds_meter_sd": tds_meter_sd,
        "train_bay": train_bay,
    }
    return {"trains": trains, "bays": bays, "plan": plan, "cleaning": cleaning, "asset_rows": asset_rows}


def _assemble_with_plan(r1, r2, r3, r4, plan, forward=True):
    """Project quarterly 2026 mode hours to 2027 using strictly the loaded operating_plan_2027.csv."""
    bt = plan["boron_temp_q"] if forward else [1.0] * 4
    sc = plan["scaling_rec_q"] if forward else [1.0] * 4
    ts = plan["tds_sal_q"] if forward else [1.0] * 4
    members = {}
    c1 = c2 = c3 = c4 = q3_tot = 0.0
    for u in core.TRAINS:
        sr = plan["sched_ratio"][u] if forward else [1.0] * 4
        b27 = [r1[u]["q"][q] * bt[q] * sr[q] for q in range(4)]
        s27 = [r2[u]["q"][q] * sc[q] * sr[q] for q in range(4)]
        st27 = [r3[u]["q"][q] * sr[q] for q in range(4)]
        t27 = [r4[u]["q"][q] * ts[q] * sr[q] for q in range(4)]
        members[u] = sum(b27) + sum(s27) + sum(st27) + sum(t27)
        c1 += sum(b27)
        c2 += sum(s27)
        c3 += sum(st27)
        c4 += sum(t27)
        q3_tot += b27[2] + s27[2] + st27[2] + t27[2]
    ov_set = [u for u in core.TRAINS if members[u] >= core.THRESHOLD]
    ov_h = sum(members[u] for u in ov_set)
    e_tot = (
        c1 * core.ENERGY_BORON_KWH
        + c2 * core.ENERGY_SCALING_KWH
        + c3 * core.ENERGY_STRUCT_KWH
        + c4 * core.ENERGY_TDS_KWH
    ) / 1000.0
    e_ov = 0.0
    for u in ov_set:
        sr = plan["sched_ratio"][u] if forward else [1.0] * 4
        ub = sum(r1[u]["q"][q] * bt[q] * sr[q] for q in range(4))
        us = sum(r2[u]["q"][q] * sc[q] * sr[q] for q in range(4))
        ust = sum(r3[u]["q"][q] * sr[q] for q in range(4))
        ut = sum(r4[u]["q"][q] * ts[q] * sr[q] for q in range(4))
        e_ov += (
            ub * core.ENERGY_BORON_KWH
            + us * core.ENERGY_SCALING_KWH
            + ust * core.ENERGY_STRUCT_KWH
            + ut * core.ENERGY_TDS_KWH
        ) / 1000.0
    return {
        "members": members,
        "C1_boron_2027": c1,
        "C2_scaling_2027": c2,
        "C3_struct_2027": c3,
        "C4_tds_2027": c4,
        "A_total_2027": c1 + c2 + c3 + c4,
        "A_overhaul_2027": ov_h,
        "A_q3_2027": q3_tot,
        "A_energy_mwh": e_tot,
        "A_overhaul_mwh": e_ov,
    }


def _comb_fal(x1, x2, x3, x4):
    a, b, c, d = core.falsification_parts(x1, x2, x3, x4)
    b_ex = max(0.0, b - core.COND_PROBE_SD)
    chi2 = (a / 0.10) ** 2 + (b_ex / 0.10) ** 2 + (c / 0.30) ** 2 + (d / 0.14) ** 2
    return {"f1": a, "f2_ms_cm": b, "f3_pp": c, "f4_mg_l": d, "combined": chi2}


def run_all(target_dir):
    """Run full v3 analysis strictly from target_dir and return comprehensive results dict."""
    loaded = load_clean_from_target(target_dir)
    data = {"trains": loaded["trains"], "bays": loaded["bays"]}
    plan = loaded["plan"]

    # Golden estimators (all 4 modes)
    r1_g = core.estimate_s1(data, mode="golden")
    r2_g = core.estimate_s2(data, mode="golden")
    r3_g = core.estimate_s3(data, mode="golden")
    r4_g = core.estimate_s4(data, mode="golden")
    gold_asm = _assemble_with_plan(r1_g, r2_g, r3_g, r4_g, plan)

    # Hurried / Direct estimators
    r1_h = core.estimate_s1(data, mode="hurried")
    r2_h = core.estimate_s2(data, mode="hurried")
    r3_h = core.estimate_s3(data, mode="hurried")
    r4_h = core.estimate_s4(data, mode="hurried")

    # Round-2 3.5-hour frontier solvers (R1 & R2) + coded one-fact shortcuts
    r1_r1 = core.estimate_s1(data, mode="r1_block_ar1")
    r1_r2 = core.estimate_s1(data, mode="r2_flux_homosced")
    r2_r12 = core.estimate_s2(data, mode="r1_r2_fixed_lag_tep")
    r2_sp = core.estimate_s2(data, mode="single_plug")
    r3_r1 = core.estimate_s3(data, mode="r1_uncond_3class")
    r3_r2 = core.estimate_s3(data, mode="r2_static_120h")
    r4_r12 = core.estimate_s4(data, mode="r1_r2_equal_var")

    rig_r1_asm = _assemble_with_plan(r1_r1, r2_r12, r3_r1, r4_r12, plan)
    rig_r2_asm = _assemble_with_plan(r1_r2, r2_r12, r3_r2, r4_r12, plan)

    # Over-corrections (strictly two-sided)
    r1_over = core.estimate_s1(data, mode="over_flux_iid")
    r2_over = core.estimate_s2(data, mode="over_comonotonic")
    r3_over = core.estimate_s3(data, mode="unanimous")
    r4_over = core.estimate_s4(data, mode="over_bay_sd_2x")
    over = {
        "S1": _assemble_with_plan(r1_over, r2_g, r3_g, r4_g, plan),
        "S2": _assemble_with_plan(r1_g, r2_over, r3_g, r4_g, plan),
        "S3": _assemble_with_plan(r1_g, r2_g, r3_over, r4_g, plan),
        "S4": _assemble_with_plan(r1_g, r2_g, r3_g, r4_over, plan),
    }

    # Coded one-fact shortcuts
    ofs = {
        "S1": _assemble_with_plan(r1_r2, r2_g, r3_g, r4_g, plan),
        "S2": _assemble_with_plan(r1_g, r2_sp, r3_g, r4_g, plan),
        "S3": _assemble_with_plan(r1_g, r2_g, r3_r2, r4_g, plan),
        "S4": _assemble_with_plan(r1_g, r2_g, r3_g, r4_r12, plan),
    }

    # Full 15-corner stump lattice (all non-empty subsets of S1, S2, S3, S4)
    lattice_asm = {}
    for k_len in range(1, 5):
        for comb in itertools.combinations(["S1", "S2", "S3", "S4"], k_len):
            key = "+".join(comb)
            lattice_asm[key] = _assemble_with_plan(
                r1_h if "S1" in comb else r1_g,
                r2_h if "S2" in comb else r2_g,
                r3_h if "S3" in comb else r3_g,
                r4_h if "S4" in comb else r4_g,
                plan,
            )

    # 39 Honest Converged Physical Estimator Variants (exact 1-to-1 match to core.py)
    s1_var_specs = [
        ("S1_exact_flux_mle", core.estimate_s1(data, mode="golden_mle")),
        ("S1_exact_ou_mle", core.estimate_s1(data, mode="golden_ou_mle")),
        ("S1_ou_wls", core.estimate_s1(data, mode="golden", kernel="ou", obj="wls")),
        ("S1_ou_wls_var", core.estimate_s1(data, mode="golden", kernel="ou", obj="wls_var")),
        ("S1_ar1_ols", core.estimate_s1(data, mode="golden", kernel="ar1", obj="ols")),
        ("S1_ar1_lag1", core.estimate_s1(data, mode="golden", kernel="ar1", obj="lag1")),
        ("S1_ar1_trim05", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", trim_frac=0.005)),
        ("S1_ar1_no_lab_noise", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", lab_noise=False)),
        ("S1_ar1_4h_only", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", use_8h=False)),
        ("S1_huber_flux_reg", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", reg_mode="huber")),
        ("S1_quarterly_mu_j", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", q_mu_j=True)),
    ]
    s2_var_specs = [
        ("S2_flow_step_left", core.estimate_s2(data, mode="golden", flow_interp="step_left", loss_fn="l2")),
        ("S2_flow_step_right", core.estimate_s2(data, mode="golden", flow_interp="step_right", loss_fn="l2")),
        ("S2_flow_midpoint", core.estimate_s2(data, mode="golden", flow_interp="midpoint", loss_fn="l2")),
        ("S2_flow_trapz", core.estimate_s2(data, mode="golden", flow_interp="trapz", loss_fn="l2")),
        ("S2_loss_l1", core.estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l1")),
        ("S2_loss_huber", core.estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="huber")),
        ("S2_loss_trimmed_l2", core.estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="trimmed_l2")),
        ("S2_tep_nearest", core.estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l2", tep_interp="nearest")),
    ]
    s3_var_specs = [
        ("S3_kinetics_exp_vol", core.estimate_s3(data, mode="golden", kinetics="exp_vol")),
        ("S3_kinetics_michaelis", core.estimate_s3(data, mode="golden", kinetics="michaelis")),
        ("S3_kinetics_weibull_115", core.estimate_s3(data, mode="golden", kinetics="weibull_12")),
        ("S3_kinetics_weibull_090", core.estimate_s3(data, mode="golden", kinetics="weibull_09")),
        ("S3_midpoint_half_h", core.estimate_s3(data, mode="golden", kinetics="exp_time", dt_shift=0.5)),
        ("S3_jeffreys_map", core.estimate_s3(data, mode="golden", kinetics="exp_time", map_alpha=0.5)),
        ("S3_laplace_map", core.estimate_s3(data, mode="golden", kinetics="exp_time", map_alpha=1.0)),
        ("S3_bic_pruned", core.estimate_s3(data, mode="golden", kinetics="exp_time", bic_prune=True)),
        ("S3_two_step_static", core.estimate_s3(data, mode="golden", kinetics="exp_time", two_step_static=True)),
    ]
    s4_var_specs = [
        ("S4_var_ols_sq", core.estimate_s4(data, mode="golden", var_method="ols_sq")),
        ("S4_var_wls_sq", core.estimate_s4(data, mode="golden", var_method="wls_sq")),
        ("S4_var_mle_no_meter", core.estimate_s4(data, mode="golden", var_method="mle", meter_noise=False)),
        ("S4_mean_huber_mle", core.estimate_s4(data, mode="golden", var_method="mle", mean_mode="huber")),
        ("S4_joint_gls_mle", core.estimate_s4(data, mode="golden", var_method="joint_gls_mle")),
        ("S4_ar1_mle", core.estimate_s4(data, mode="golden", var_method="ar1_mle")),
        ("S4_kalman_ar1_mle", core.estimate_s4(data, mode="golden", var_method="kalman_ar1_mle")),
        ("S4_gls_kalman_mle", core.estimate_s4(data, mode="golden", var_method="gls_kalman_mle")),
    ]

    variants_named = []
    for nm, v1 in s1_var_specs:
        variants_named.append((nm, _assemble_with_plan(v1, r2_g, r3_g, r4_g, plan)))
    for nm, v2 in s2_var_specs:
        variants_named.append((nm, _assemble_with_plan(r1_g, v2, r3_g, r4_g, plan)))
    for nm, v3 in s3_var_specs:
        variants_named.append((nm, _assemble_with_plan(r1_g, r2_g, v3, r4_g, plan)))
    for nm, v4 in s4_var_specs:
        variants_named.append((nm, _assemble_with_plan(r1_g, r2_g, r3_g, v4, plan)))
    variants_named.append(("Joint_MLE_Mid_ExpVol_GLSKalman", _assemble_with_plan(s1_var_specs[0][1], s2_var_specs[2][1], s3_var_specs[0][1], s4_var_specs[7][1], plan)))
    variants_named.append(("Joint_OUMLE_NearTEP_Weib115_Kalman", _assemble_with_plan(s1_var_specs[1][1], s2_var_specs[7][1], s3_var_specs[2][1], s4_var_specs[6][1], plan)))
    variants_named.append(("Joint_Huber_StepL_Jeffreys_WLS", _assemble_with_plan(s1_var_specs[9][1], s2_var_specs[0][1], s3_var_specs[5][1], s4_var_specs[1][1], plan)))

    # Run routes + 18 extra rivals
    gen_asm = _assemble_with_plan(r1_over, r2_over, r3_r1, r4_over, plan)
    r1_hedge = {u: {**r1_g[u], "q": [0.8 * r1_h[u]["q"][q] + 0.2 * r1_g[u]["q"][q] for q in range(4)], "f1_err": 1.3} for u in core.TRAINS}
    r2_hedge = {u: {**r2_g[u], "q": [0.8 * r2_h[u]["q"][q] + 0.2 * r2_g[u]["q"][q] for q in range(4)], "c_rms": 1.6} for u in core.TRAINS}
    r3_hedge = {u: {**r3_g[u], "q": [0.8 * r3_h[u]["q"][q] + 0.2 * r3_g[u]["q"][q] for q in range(4)], "f3_pp": 4.4} for u in core.TRAINS}
    r4_hedge = {u: {**r4_g[u], "q": [0.8 * r4_h[u]["q"][q] + 0.2 * r4_g[u]["q"][q] for q in range(4)], "f4_err": 9.5} for u in core.TRAINS}
    hedge_asm = _assemble_with_plan(r1_hedge, r2_hedge, r3_hedge, r4_hedge, plan)

    r1_c4 = core.estimate_s1(data, mode="cutoff_4h")
    r1_stat = core.estimate_s1(data, mode="stat_ar1_no_flux")
    r1_fnd = core.estimate_s1(data, mode="flux_no_deconv")
    r2_flc = core.estimate_s2(data, mode="fixed_lag_cond")
    r2_nv = core.estimate_s2(data, mode="nom_vol")
    r3_72 = core.estimate_s3(data, mode="r2_static_72h")
    r3_48 = core.estimate_s3(data, mode="r2_static_48h")
    r3_cpmv = core.estimate_s3(data, mode="post_cip_mv")
    r3_un = core.estimate_s3(data, mode="unanimous")
    r4_bay = core.estimate_s4(data, mode="bay_sd_direct")
    cut_asm = _assemble_with_plan(r1_c4, r2_r12, r3_cpmv, r4_bay, plan)

    extra_routes = {
        "cutoff:r1_round2_full": rig_r1_asm,
        "cutoff:r2_round2_full": rig_r2_asm,
        "cutoff:s1_r1_block_ar1": _assemble_with_plan(r1_r1, r2_g, r3_g, r4_g, plan),
        "cutoff:s1_r2_flux_homosced": ofs["S1"],
        "cutoff:s1_stat_ar1_no_flux": _assemble_with_plan(r1_stat, r2_g, r3_g, r4_g, plan),
        "cutoff:s1_flux_no_deconv": _assemble_with_plan(r1_fnd, r2_g, r3_g, r4_g, plan),
        "cutoff:s2_r1_r2_fixed_lag_tep": _assemble_with_plan(r1_g, r2_r12, r3_g, r4_g, plan),
        "cutoff:s2_single_plug_veff": ofs["S2"],
        "cutoff:s2_fixed_lag_cond": _assemble_with_plan(r1_g, r2_flc, r3_g, r4_g, plan),
        "cutoff:s2_nom_vol": _assemble_with_plan(r1_g, r2_nv, r3_g, r4_g, plan),
        "cutoff:s3_r1_uncond_3class": _assemble_with_plan(r1_g, r2_g, r3_r1, r4_g, plan),
        "cutoff:s3_r2_static_120h": ofs["S3"],
        "cutoff:s3_static_72h": _assemble_with_plan(r1_g, r2_g, r3_72, r4_g, plan),
        "cutoff:s3_static_48h": _assemble_with_plan(r1_g, r2_g, r3_48, r4_g, plan),
        "cutoff:s3_unanimous": _assemble_with_plan(r1_g, r2_g, r3_un, r4_g, plan),
        "cutoff:s4_r1_r2_equal_var": ofs["S4"],
        "cutoff:s4_bay_sd_direct": _assemble_with_plan(r1_g, r2_g, r3_g, r4_bay, plan),
        "hedge:history_2026_flat": _assemble_with_plan(r1_g, r2_g, r3_g, r4_g, plan, forward=False),
    }

    # Native-unit physical falsification across all routes
    fal_by_route = {}
    for label, (x1, x2, x3, x4) in [
        ("golden", (r1_g, r2_g, r3_g, r4_g)),
        ("direct", (r1_h, r2_h, r3_h, r4_h)),
        ("rigorous_r1", (r1_r1, r2_r12, r3_r1, r4_r12)),
        ("rigorous_r2", (r1_r2, r2_r12, r3_r2, r4_r12)),
        ("generous", (r1_over, r2_over, r3_r1, r4_over)),
        ("hedge", (r1_hedge, r2_hedge, r3_hedge, r4_hedge)),
        ("cutoff", (r1_c4, r2_r12, r3_cpmv, r4_bay)),
        ("S1_r2_homosc", (r1_r2, r2_g, r3_g, r4_g)),
        ("S2_r12_lag", (r1_g, r2_r12, r3_g, r4_g)),
        ("S2_single_plug", (r1_g, r2_sp, r3_g, r4_g)),
        ("S3_r1_uncond", (r1_g, r2_g, r3_r1, r4_g)),
        ("S3_r2_120h", (r1_g, r2_g, r3_r2, r4_g)),
        ("S4_eq_var", (r1_g, r2_g, r3_g, r4_r12)),
        ("S1_over", (r1_over, r2_g, r3_g, r4_g)),
        ("S2_over", (r1_g, r2_over, r3_g, r4_g)),
        ("S3_over", (r1_g, r2_g, r3_over, r4_g)),
        ("S4_over", (r1_g, r2_g, r3_g, r4_over)),
    ]:
        fal_by_route[label] = _comb_fal(x1, x2, x3, x4)

    # 8-way +/-20% forcing perturbations
    golden_slate = sorted(u for u in core.TRAINS if gold_asm["members"][u] >= core.THRESHOLD)
    perturbations = []
    for mode_name, idx in [("S1_boron", 1), ("S2_scaling", 2), ("S3_struct", 3), ("S4_tds", 4)]:
        for mult in (0.80, 1.20):
            x1 = {u: {**r1_g[u], "q": [v * mult for v in r1_g[u]["q"]]} for u in core.TRAINS} if idx == 1 else r1_g
            x2 = {u: {**r2_g[u], "q": [v * mult for v in r2_g[u]["q"]]} for u in core.TRAINS} if idx == 2 else r2_g
            x3 = {u: {**r3_g[u], "q": [v * mult for v in r3_g[u]["q"]]} for u in core.TRAINS} if idx == 3 else r3_g
            x4 = {u: {**r4_g[u], "q": [v * mult for v in r4_g[u]["q"]]} for u in core.TRAINS} if idx == 4 else r4_g
            asm = _assemble_with_plan(x1, x2, x3, x4, plan)
            sl = sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)
            ov_min = min(asm["members"][u] for u in golden_slate)
            mo_max = max(asm["members"][u] for u in core.TRAINS if u not in golden_slate)
            perturbations.append({
                "input": f"{mode_name}_{int(round((mult - 1.0) * 100)):+d}pct",
                "holds": sl == golden_slate,
                "answer": sl,
                "min_overhaul": round(ov_min, 1),
                "max_monitor": round(mo_max, 1),
            })

    # Per-train structured summary rows
    train_rows = {}
    for u in core.TRAINS:
        sr = plan["sched_ratio"][u]
        bt, sc, ts = plan["boron_temp_q"], plan["scaling_rec_q"], plan["tds_sal_q"]
        b26_q = list(r1_g[u]["q"])
        s26_q = list(r2_g[u]["q"])
        st26_q = list(r3_g[u]["q"])
        t26_q = list(r4_g[u]["q"])
        b27_q = [b26_q[q] * bt[q] * sr[q] for q in range(4)]
        s27_q = [s26_q[q] * sc[q] * sr[q] for q in range(4)]
        st27_q = [st26_q[q] * sr[q] for q in range(4)]
        t27_q = [t26_q[q] * ts[q] * sr[q] for q in range(4)]
        tot27 = sum(b27_q) + sum(s27_q) + sum(st27_q) + sum(t27_q)
        q3_27 = b27_q[2] + s27_q[2] + st27_q[2] + t27_q[2]
        energy_mwh = (
            sum(b27_q) * core.ENERGY_BORON_KWH
            + sum(s27_q) * core.ENERGY_SCALING_KWH
            + sum(st27_q) * core.ENERGY_STRUCT_KWH
            + sum(t27_q) * core.ENERGY_TDS_KWH
        ) / 1000.0
        train_rows[u] = {
            "bay": plan["train_bay"][u],
            "v_nom_m3": plan["v_nom"][u],
            "boron_2026_q": b26_q,
            "scaling_2026_q": s26_q,
            "struct_2026_q": st26_q,
            "tds_2026_q": t26_q,
            "boron_2026_h": sum(b26_q),
            "scaling_2026_h": sum(s26_q),
            "struct_2026_h": sum(st26_q),
            "tds_2026_h": sum(t26_q),
            "total_2026_h": sum(b26_q) + sum(s26_q) + sum(st26_q) + sum(t26_q),
            "boron_2027_h": sum(b27_q),
            "scaling_2027_h": sum(s27_q),
            "struct_2027_h": sum(st27_q),
            "tds_2027_h": sum(t27_q),
            "total_2027_h": tot27,
            "q3_2027_h": q3_27,
            "energy_2027_mwh": energy_mwh,
            "designation": "OVERHAUL" if tot27 >= core.THRESHOLD else "MONITOR",
            # Diagnostic parameters per stump
            "s1_alphas": r1_g[u]["alphas"],
            "s1_mu_j": float(np.mean(r1_g[u]["mu_j"])),
            "s1_sd_j": r1_g[u]["sd_j"],
            "s1_lam_h": r1_g[u]["lam"],
            "s1_het_corr": r1_g[u]["het_corr"],
            "s1_raw_2026_h": sum(r1_h[u]["q"]),
            "s1_r2_2026_h": sum(r1_r2[u]["q"]),
            "s2_f_fast_hat": r2_g[u]["params"][0],
            "s2_v_fast_hat": r2_g[u]["params"][1],
            "s2_v_main_hat": r2_g[u]["params"][2],
            "s2_cond_rms": r2_g[u]["c_rms"],
            "s2_lag_cond_rms": r2_r12[u]["c_rms"],
            "s2_sp_cond_rms": r2_sp[u]["c_rms"],
            "s2_raw_2026_h": sum(r2_h[u]["q"]),
            "s2_lag_2026_h": sum(r2_r12[u]["q"]),
            "s2_sp_2026_h": sum(r2_sp[u]["q"]),
            "s3_pi_s_hat": r3_g[u]["pi_s"],
            "s3_pi_min_hat": r3_g[u]["pi_min"],
            "s3_tau_min_h": r3_g[u]["tau_min"],
            "s3_raw_2026_h": sum(r3_h[u]["q"]),
            "s3_r1_2026_h": sum(r3_r1[u]["q"]),
            "s3_r2_2026_h": sum(r3_r2[u]["q"]),
            "s3_p_cl": r3_g[u]["emissions"][0],
            "s3_p_fb": r3_g[u]["emissions"][1],
            "s3_p_ms": r3_g[u]["emissions"][2],
            "s4_mu_q": r4_g[u]["mu_q"],
            "s4_mu_mean": float(np.mean(r4_g[u]["mu_q"])),
            "s4_sigma_hat": r4_g[u]["sd_hat"],
            "s4_raw_2026_h": sum(r4_h[u]["q"]),
            "s4_eq_2026_h": sum(r4_r12[u]["q"]),
            "s4_eq_sigma": r4_r12[u]["sd_hat"],
        }

    # 36-variant uncertainty bands (min..max across golden + all 36 variants)
    bands = {}
    all_as = [gold_asm] + [a for _, a in variants_named]
    for key in (
        "C1_boron_2027", "C2_scaling_2027", "C3_struct_2027", "C4_tds_2027",
        "A_total_2027", "A_overhaul_2027", "A_q3_2027", "A_energy_mwh", "A_overhaul_mwh",
    ):
        vals = [a[key] for a in all_as]
        bands[key] = [round(min(vals), 1), round(max(vals), 1)]
    for u in core.TRAINS:
        vals = [a["members"][u] for a in all_as]
        bands[u] = [round(min(vals), 1), round(max(vals), 1)]

    # Mode 3 Gate C profile-likelihood LRT for TR06 at the 400.0-hour overhaul criterion
    tr6 = train_rows["TR06"]
    non_struct_tr6 = tr6["boron_2027_h"] + tr6["scaling_2027_h"] + tr6["tds_2027_h"]
    sr6 = plan["sched_ratio"]["TR06"]
    qh_plan = plan["q_hours"]
    tr6_struct_factor = sum(qh_plan[q] * sr6[q] for q in range(4))
    pi_s_400 = max(1e-4, (core.THRESHOLD - non_struct_tr6) / tr6_struct_factor)
    fit_tr06_400 = core._fit_kinetic_dual_cip(data, kinetics="exp_time", fix_tr06_ps=pi_s_400)
    tr06_profile_lrt_400h = max(0.0, 2.0 * (r3_g["TR06"]["ll"] - fit_tr06_400["ll"]))

    # Mode 4 Gate C exact 4-state AR(1) Kalman profile-likelihood LRT for TR05 against 400.0 h
    tr5 = train_rows["TR05"]
    non_tds_tr5 = tr5["boron_2027_h"] + tr5["scaling_2027_h"] + tr5["struct_2027_h"]
    tr05_kalman_lrt_400h = core.compute_tr05_kalman_lrt(
        data,
        non_tds_tr5,
        sched_ratio_tr05=plan["sched_ratio"]["TR05"],
        tds_sal_q=plan["tds_sal_q"],
        q_hours=qh_plan,
    )

    # Flow saturation / flat-clamp QA check across all 70,080 clean hourly rows
    max_flow_rep = 0
    for u in core.TRAINS:
        _, cnts = np.unique(np.round(data["trains"][u]["q_flow_h"], 4), return_counts=True)
        max_flow_rep = max(max_flow_rep, int(cnts.max()))
    loaded["cleaning"]["hydraulics_max_flow_repeat"] = max_flow_rep

    return {
        "golden_slate": golden_slate,
        "gold_asm": gold_asm,
        "rig_r1_asm": rig_r1_asm,
        "rig_r2_asm": rig_r2_asm,
        "gen_asm": gen_asm,
        "hedge_asm": hedge_asm,
        "cut_asm": cut_asm,
        "lattice_asm": lattice_asm,
        "over": over,
        "ofs": ofs,
        "extra_routes": extra_routes,
        "fal_by_route": fal_by_route,
        "variants_named": variants_named,
        "perturbations": perturbations,
        "train_rows": train_rows,
        "bands": bands,
        "plan": plan,
        "cleaning": loaded["cleaning"],
        "tr06_profile_lrt_400h": round(tr06_profile_lrt_400h, 2),
        "tr05_kalman_lrt_400h": round(tr05_kalman_lrt_400h, 2),
        "r1_g": r1_g, "r2_g": r2_g, "r3_g": r3_g, "r4_g": r4_g,
    }


if __name__ == "__main__":
    tdir = os.path.join(os.path.dirname(HERE), "target")
    res = run_all(tdir)
    print("Golden slate:", res["golden_slate"], "TR06 LRT@400h:", res["tr06_profile_lrt_400h"])
    for u in core.TRAINS:
        tr = res["train_rows"][u]
        print(
            f"  {u}: {tr['total_2027_h']:7.1f} h "
            f"(B={tr['boron_2027_h']:5.1f} S={tr['scaling_2027_h']:5.1f} "
            f"St={tr['struct_2027_h']:5.1f} T={tr['tds_2027_h']:5.1f}) "
            f"Q3={tr['q3_2027_h']:5.1f} E={tr['energy_2027_mwh']:6.2f} MWh -> {tr['designation']}"
        )
