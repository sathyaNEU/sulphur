#!/usr/bin/env python3
"""task28/generator/analysis.py (v2): Read ONLY shipped files under target/ (performing full
Layer 1 cleaning), recompute every v2 physical estimator, all 26 defensible variants, all 6
+/-20% forcing perturbations, the full 7-corner stump lattice, Response 1 & Response 2 Round-1
rigorous routes, run/cutoff/hedge/over-correction routes, and native-unit F1-F3 falsification.

Zero hidden generator constants: every threshold, energy rate, and 2027 plan multiplier comes
from the shipped files (operating_plan_2027.csv, train_asset_register.csv, Protocol SWRO-Q27).
"""
import csv
import datetime as dt
import itertools
import json
import math
import os
import sys

import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator

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
    """Load and clean every operational file from target_dir without touching core.simulate_world()."""
    F = PK.FILES
    cleaning = {}

    # 1. Asset register (crosswalk + V_nom)
    legacy_map = {}
    v_nom = {}
    asset_rows = {}
    with open(os.path.join(target_dir, F["asset_reg"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            u = r["train_id"].strip()
            legacy_map[r["legacy_tag"].strip()] = u
            legacy_map[u] = u
            v_nom[u] = float(r["pretreatment_nominal_m3"])
            asset_rows[u] = r
    cleaning["trains_in_register"] = len(asset_rows)

    # 2. 2027 Operating Plan
    plan_sched = {u: [0.0] * 4 for u in core.TRAINS}
    plan_btemp = [0.0] * 4
    plan_srec = [0.0] * 4
    q_hours = [0] * 4
    q_map = {"2027-Q1": 0, "2027-Q2": 1, "2027-Q3": 2, "2027-Q4": 3}
    with open(os.path.join(target_dir, F["op_plan"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            u = r["train_id"].strip()
            q = q_map[r["quarter"].strip()]
            plan_sched[u][q] = float(r["dispatch_duty_ratio_2027"])
            plan_btemp[q] = float(r["boron_thermal_factor_2027"])
            plan_srec[q] = float(r["scaling_recovery_factor_2027"])
            q_hours[q] = int(r["calendar_hours_2026"])

    n_h = sum(q_hours)
    n_15 = n_h * 4
    n_sh = n_h // 4
    q_starts = [0]
    for h in q_hours:
        q_starts.append(q_starts[-1] + h)
    q_h = [0] * n_h
    for q in range(4):
        for t in range(q_starts[q], q_starts[q + 1]):
            q_h[t] = q
    q_15 = [q_h[t // 4] for t in range(n_15)]
    q_sh = [q_h[b * 4] for b in range(n_sh)]

    # 3. Hourly SCADA hydraulics (needed first to compute exact bottle mean flow Q_bar_k!)
    q_flow_map = {u: [None] * n_h for u in core.TRAINS}
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
            if q_flow_map[u][idx] is not None:
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

    # 4. Autosampler schedule
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

    # 5. Permeate boron composites (dedup qa_revision, convert ug/L -> mg/L, parse DD/MM/YYYY)
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
            slot = int(r["carousel_slot"])
            val = float(r["boron_conc"])
            unit = r["unit"].strip()
            if unit == "ug/L":
                boron_ug += 1
                val = val / 1000.0
            elif unit != "mg/L":
                raise ValueError(f"Unexpected boron unit {unit}")
            prev = best_by_sid.get(sid)
            if prev is None or rev > prev[0]:
                best_by_sid[sid] = (rev, u, day, slot, val)

    cleaning["boron_raw_rows"] = boron_raw
    cleaning["boron_clean_rows"] = len(best_by_sid)
    cleaning["boron_superseded_dropped"] = boron_raw - len(best_by_sid)
    cleaning["boron_ug_rows"] = boron_ug
    cleaning["boron_legacy_rows"] = boron_legacy
    cleaning["boron_dmy_rows"] = boron_dmy

    comp_by_u = {u: [] for u in core.TRAINS}
    for _rev, u, day, slot, val in best_by_sid.values():
        m = span_map[(u, day)]
        qd = q_h[day * 24]
        h0 = day * 24 + (slot - 1) * m
        qbar = sum(q_flow_map[u][h0:h0 + m]) / m
        comp_by_u[u].append((day, slot, m, qd, val, qbar))
    for u in core.TRAINS:
        comp_by_u[u].sort(key=lambda x: (x[0], x[1]))

    # 6. 15-min intake chemistry
    c_in_map = {u: [None] * n_15 for u in core.TRAINS}
    x_in_map = {u: [None] * n_15 for u in core.TRAINS}
    in_raw = 0
    in_dups = 0
    with open(os.path.join(target_dir, F["intake_15m"]), encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr[:4] == ["ts_utc", "train_id", "intake_cond_ms_cm", "intake_tep_z_index"]
        ts_cache = {}
        for row in rd:
            in_raw += 1
            ts_s, u = row[0], row[1]
            idx = ts_cache.get(ts_s)
            if idx is None:
                idx = int((_parse_iso_utc(ts_s) - START_2026).total_seconds() // 900)
                ts_cache[ts_s] = idx
            if c_in_map[u][idx] is not None:
                in_dups += 1
                continue
            c_in_map[u][idx] = float(row[2])
            x_in_map[u][idx] = float(row[3])
    cleaning["intake_raw_rows"] = in_raw
    cleaning["intake_clean_rows"] = in_raw - in_dups
    cleaning["intake_dups_dropped"] = in_dups

    # 7. 15-min RO-feed header chemistry
    c_out_map = {u: [None] * n_15 for u in core.TRAINS}
    y_out_map = {u: [None] * n_15 for u in core.TRAINS}
    ro_raw = 0
    ro_dups = 0
    with open(os.path.join(target_dir, F["ro_feed_15m"]), encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        assert hdr[:4] == ["ts_utc", "train_id", "ro_feed_cond_ms_cm", "ro_feed_stress_idx"]
        for row in rd:
            ro_raw += 1
            ts_s, u = row[0], row[1]
            idx = ts_cache[ts_s]
            if c_out_map[u][idx] is not None:
                ro_dups += 1
                continue
            c_out_map[u][idx] = float(row[2])
            y_out_map[u][idx] = float(row[3])
    cleaning["ro_feed_raw_rows"] = ro_raw
    cleaning["ro_feed_clean_rows"] = ro_raw - ro_dups
    cleaning["ro_feed_dups_dropped"] = ro_dups

    # 8. 4-hour shift diagnostics (Europe/Lisbon offset -> UTC block index)
    pat_map = {u: [None] * n_sh for u in core.TRAINS}
    sh_raw = 0
    with open(os.path.join(target_dir, F["shift_diag"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            sh_raw += 1
            u = r["train_id"].strip()
            b = int((_parse_iso_utc(r["block_start_lisbon"]) - START_2026).total_seconds() // 14400)
            d1 = int(r["salt_passage_alarm"])
            d2 = int(r["stage_dp_alarm"])
            d3 = int(r["acoustic_bypass_alarm"])
            pat_map[u][b] = (d1 << 2) | (d2 << 1) | d3
    cleaning["shift_rows"] = sh_raw

    # 9. CIP wash log (Europe/Lisbon offset -> UTC block index, legacy tag resolution, dual recipe!)
    cip_events = {u: [] for u in core.TRAINS}
    cip_raw = 0
    cip_legacy = 0
    cip_alk = 0
    cip_acid = 0
    with open(os.path.join(target_dir, F["cip_log"]), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            cip_raw += 1
            raw_u = r["train_code"].strip()
            if raw_u.startswith("LINE-"):
                cip_legacy += 1
            u = legacy_map[raw_u]
            cb = int((_parse_iso_utc(r["wash_completed_lisbon"]) - START_2026).total_seconds() // 14400)
            recipe = r["chemical_stage"].strip()
            if recipe == "CIP_ALK_pH11":
                cip_alk += 1
            elif recipe == "CIP_ACID_pH2":
                cip_acid += 1
            else:
                raise ValueError(f"Unexpected CIP recipe {recipe}")
            cip_events[u].append((cb, recipe))
    for u in core.TRAINS:
        cip_events[u].sort(key=lambda x: x[0])
    cleaning["cip_rows"] = cip_raw
    cleaning["cip_alk_rows"] = cip_alk
    cleaning["cip_acid_rows"] = cip_acid
    cleaning["cip_legacy_tags"] = cip_legacy

    # Build exact core-compatible data dictionary
    data = {"q_h": q_h, "q_15": q_15, "q_sh": q_sh, "trains": {}}
    for u in core.TRAINS:
        assert all(v is not None for v in c_in_map[u]), f"missing intake {u}"
        assert all(v is not None for v in c_out_map[u]), f"missing ro_feed {u}"
        assert all(v is not None for v in q_flow_map[u]), f"missing hydraulics {u}"
        assert all(v is not None for v in pat_map[u]), f"missing shifts {u}"
        regime_sh = [0] * n_sh
        for cb, rec in cip_events[u]:
            code = 1 if rec == "CIP_ALK_pH11" else 2
            for j in range(cb, min(n_sh, cb + 30)):
                regime_sh[j] = code
        cnt_reg = [[0] * 8 for _ in range(3)]
        for b in range(n_sh):
            cnt_reg[regime_sh[b]][pat_map[u][b]] += 1

        data["trains"][u] = {
            "comp_day": [x[0] for x in comp_by_u[u]],
            "comp_slot": [x[1] for x in comp_by_u[u]],
            "comp_m": [x[2] for x in comp_by_u[u]],
            "comp_q": [x[3] for x in comp_by_u[u]],
            "comp_val": [x[4] for x in comp_by_u[u]],
            "comp_qbar": [x[5] for x in comp_by_u[u]],
            "q_flow_h": q_flow_map[u],
            "v_nom": v_nom[u],
            "c_in_15": c_in_map[u],
            "c_out_15": c_out_map[u],
            "x_in_15": x_in_map[u],
            "y_out_15": y_out_map[u],
            "pat_sh": pat_map[u],
            "cip_events": cip_events[u],
            "regime_sh": regime_sh,
            "cnt_reg": cnt_reg,
        }

    plan = {
        "sched_ratio": plan_sched,
        "boron_temp_q": plan_btemp,
        "scaling_rec_q": plan_srec,
        "q_hours": q_hours,
        "asset_rows": asset_rows,
    }
    return data, plan, cleaning


def _project_train(bq26, sq26, stq26, u, plan):
    sr = plan["sched_ratio"][u]
    bt = plan["boron_temp_q"]
    sc = plan["scaling_rec_q"]
    b27 = [bq26[q] * bt[q] * sr[q] for q in range(4)]
    s27 = [sq26[q] * sc[q] * sr[q] for q in range(4)]
    st27 = [stq26[q] * sr[q] for q in range(4)]
    return b27, s27, st27


def run_all(target_dir):
    """Run complete golden, 26-variant battery, forcing perturbations, lattice, Round-1 frontier
    rivals (R1 & R2), run/cutoff/hedge/over-correction routes, and native-unit F1-F3 checks
    strictly on shipped files under target_dir."""
    data, plan, cleaning = load_clean_from_target(target_dir)

    # Golden estimators
    r1_g = core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls")
    r2_g = core.estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l2")
    r3_g = core.estimate_s3(data, mode="golden", post_blocks=30, shared_clear=True)
    gold_asm = core.assemble(r1_g, r2_g, r3_g)

    # Hurried / Direct
    r1_h = core.estimate_s1(data, mode="hurried")
    r2_h = core.estimate_s2(data, mode="hurried")
    r3_h = core.estimate_s3(data, mode="hurried")

    # Round-1 Frontier Solvers (Response 1 & Response 2 exact architectures!)
    r1_stat = core.estimate_s1(data, mode="rigorous_stat_ar1")
    r2_sp = core.estimate_s2(data, mode="single_plug")
    r3_r1 = core.estimate_s3(data, mode="r1_pooled_cip_3state")
    r3_r2 = core.estimate_s3(data, mode="post_cip_ds2")
    rig_r1_asm = core.assemble(r1_stat, r2_sp, r3_r1)
    rig_r2_asm = core.assemble(r1_stat, r2_sp, r3_r2)

    # Over-corrections (strictly two-sided on all 3 stumps)
    r1_over = core.estimate_s1(data, mode="over_iid")
    r2_over = core.estimate_s2(data, mode="over_comonotonic")
    r3_over = core.estimate_s3(data, mode="over_raw_d3_post_acid")
    over_s1 = core.assemble(r1_over, r2_g, r3_g)
    over_s2 = core.assemble(r1_g, r2_over, r3_g)
    over_s3 = core.assemble(r1_g, r2_g, r3_over)

    # Detailed per-train 2026 & 2027 breakdown for golden + diagnostic comparison columns
    train_rows = {}
    for u in core.TRAINS:
        td = data["trains"][u]
        bq26, sq26, stq26 = r1_g[u]["q"], r2_g[u]["q"], r3_g[u]["q"]
        b27, s27, st27 = _project_train(bq26, sq26, stq26, u, plan)
        hb, hs, hst = sum(b27), sum(s27), sum(st27)
        htot = hb + hs + hst
        hq3 = b27[2] + s27[2] + st27[2]
        energy_kwh = hb * core.ENERGY_BORON_KWH + hs * core.ENERGY_SCALING_KWH + hst * core.ENERGY_STRUCT_KWH

        # Mode-level rival projections for backup sheets
        b27_raw = sum(_project_train(r1_h[u]["q"], [0] * 4, [0] * 4, u, plan)[0])
        b27_stat = sum(_project_train(r1_stat[u]["q"], [0] * 4, [0] * 4, u, plan)[0])
        s27_raw = sum(_project_train([0] * 4, r2_h[u]["q"], [0] * 4, u, plan)[1])
        s27_sp = sum(_project_train([0] * 4, r2_sp[u]["q"], [0] * 4, u, plan)[1])
        st27_raw = sum(_project_train([0] * 4, [0] * 4, r3_h[u]["q"], u, plan)[2])
        st27_r1 = sum(_project_train([0] * 4, [0] * 4, r3_r1[u]["q"], u, plan)[2])
        st27_r2 = sum(_project_train([0] * 4, [0] * 4, r3_r2[u]["q"], u, plan)[2])

        # Flux-residual moments for S1 backup sheet
        alphas_u, beta_u, res_u = core._fit_flux_ols(td["comp_val"], td["comp_q"], td["comp_qbar"])
        st_m = core._comp_moments(res_u, td["comp_m"], td["comp_day"], lab_var=0.004 ** 2)
        n_alk = sum(1 for _, rec in td["cip_events"] if rec == "CIP_ALK_pH11")
        n_acid = sum(1 for _, rec in td["cip_events"] if rec == "CIP_ACID_pH2")

        train_rows[u] = {
            "train_id": u,
            "legacy_tag": PK.TRAIN_META[u]["legacy"],
            "plant_bay": PK.TRAIN_META[u]["bay"],
            "v_nom_m3": td["v_nom"],
            "boron_2026_q": bq26,
            "scaling_2026_q": sq26,
            "struct_2026_q": stq26,
            "boron_2026_h": sum(bq26),
            "scaling_2026_h": sum(sq26),
            "struct_2026_h": sum(stq26),
            "total_2026_h": sum(bq26) + sum(sq26) + sum(stq26),
            "boron_2027_q": b27,
            "scaling_2027_q": s27,
            "struct_2027_q": st27,
            "boron_2027_h": hb,
            "scaling_2027_h": hs,
            "struct_2027_h": hst,
            "total_2027_h": htot,
            "q3_2027_h": hq3,
            "energy_2027_kwh": energy_kwh,
            "energy_2027_mwh": energy_kwh / 1000.0,
            "designation": "OVERHAUL" if htot >= core.THRESHOLD else "MONITOR",
            # S1 flux-coupled + AR(1) diagnostics
            "s1_beta_hat": r1_g[u]["beta_hat"],
            "s1_alphas": r1_g[u]["alphas"],
            "s1_sd1": r1_g[u]["sd1"],
            "s1_lam_h": r1_g[u]["lam"],
            "s1_v4": st_m[4][0],
            "s1_v8": st_m[8][0],
            "s1_v8_v4_obs": r1_g[u]["v8_v4_obs"],
            "s1_v8_v4_pred": r1_g[u]["v8_v4_pred"],
            "s1_r1_4_obs": r1_g[u]["r1_4_obs"],
            "s1_r1_4_pred": r1_g[u]["r1_4_pred"],
            "s1_raw_2026_h": sum(r1_h[u]["q"]),
            "s1_stat_ar1_2026_h": sum(r1_stat[u]["q"]),
            "s1_raw_2027_h": b27_raw,
            "s1_stat_ar1_2027_h": b27_stat,
            # S2 two-path hydraulic diagnostics
            "s2_f_fast_hat": r2_g[u]["f_hat"],
            "s2_v_fast_hat": r2_g[u]["v1_hat"],
            "s2_v_main_hat": r2_g[u]["v2_hat"],
            "s2_cond_rms": r2_g[u]["c_rms"],
            "s2_sp_v_hat": r2_sp[u]["v2_hat"],
            "s2_sp_cond_rms": r2_sp[u]["c_rms"],
            "s2_raw_cond_rms": r2_h[u]["c_rms"],
            "s2_raw_2026_h": sum(r2_h[u]["q"]),
            "s2_sp_2026_h": sum(r2_sp[u]["q"]),
            "s2_raw_2027_h": s27_raw,
            "s2_sp_2027_h": s27_sp,
            # S3 4-state dual-recipe CIP diagnostics
            "s3_n_alk": n_alk,
            "s3_n_acid": n_acid,
            "s3_pi_s_hat": r3_g[u]["pi_s"],
            "s3_pi_bio_hat": r3_g[u]["pi_bio"],
            "s3_pi_min_hat": r3_g[u]["pi_min"],
            "s3_p0": r3_g[u]["p0"],
            "s3_p_bio": r3_g[u]["p_bio"],
            "s3_p_min": r3_g[u]["p_min"],
            "s3_p_str": r3_g[u]["p_str"],
            "s3_obs_drops": r3_g[u]["obs"],
            "s3_pred_drops": r3_g[u]["preds"],
            "s3_raw_2026_h": sum(r3_h[u]["q"]),
            "s3_r1_2026_h": sum(r3_r1[u]["q"]),
            "s3_r2_2026_h": sum(r3_r2[u]["q"]),
            "s3_raw_2027_h": st27_raw,
            "s3_r1_2027_h": st27_r1,
            "s3_r2_2027_h": st27_r2,
        }

    # Full 7-corner stump lattice
    lattice_asm = {}
    for n in (1, 2, 3):
        for comb in itertools.combinations(["S1", "S2", "S3"], n):
            key = "+".join(comb)
            a1 = r1_h if "S1" in comb else r1_g
            a2 = r2_h if "S2" in comb else r2_g
            a3 = r3_h if "S3" in comb else r3_g
            lattice_asm[key] = core.assemble(a1, a2, a3)

    # 26 defensible honest physical estimator variants (all must hold exact 4-of-8 slate!)
    def _estimate_s2_parcel_variant(kind):
        q_15_arr = np.array(data["q_15"], dtype=int)
        out_v = {}
        for u in core.TRAINS:
            td = data["trains"][u]
            q_h = np.array(td["q_flow_h"], dtype=float)
            x_in = np.array(td["x_in_15"], dtype=float)
            y_out = np.array(td["y_out_15"], dtype=float)
            c_in = np.array(td["c_in_15"], dtype=float)
            c_out = np.array(td["c_out_15"], dtype=float)
            n_15 = len(x_in)

            if kind == "step_left":
                q15 = np.repeat(q_h, 4)
                phi = np.concatenate([[0.0], np.cumsum(q15[:-1] * 0.25)])
                f_hat, v1_hat, v2_hat, c_rms = core._profile_two_path(phi.tolist(), td["c_in_15"], td["c_out_15"], loss_fn="l2")
                x1 = np.interp(phi - v1_hat, phi, x_in)
                x2 = np.interp(phi - v2_hat, phi, x_in)
                xa = f_hat * x1 + (1.0 - f_hat) * x2
                hit = (xa[32:] > core.SCALING_X_LIM) & (y_out[32:] > core.SCALING_Y_LIM)
                q_hrs = [float(np.sum(hit & (q_15_arr[32:] == q)) * 0.25) for q in range(4)]
                out_v[u] = {"q": q_hrs, "f_hat": f_hat, "v1_hat": v1_hat, "v2_hat": v2_hat, "c_rms": c_rms}
                continue

            phi_list, _ = core._build_phi_hat(td["q_flow_h"], flow_interp="linear")
            phi = np.array(phi_list, dtype=float)
            f_hat = r2_g[u]["f_hat"]
            v1_hat = r2_g[u]["v1_hat"]
            v2_hat = r2_g[u]["v2_hat"]
            xq1 = np.clip(phi - v1_hat, phi[0], phi[-1])
            xq2 = np.clip(phi - v2_hat, phi[0], phi[-1])

            if kind == "pchip":
                fn = PchipInterpolator(phi, x_in)
                xa = f_hat * fn(xq1) + (1.0 - f_hat) * fn(xq2)
                hit = (xa[32:] > core.SCALING_X_LIM) & (y_out[32:] > core.SCALING_Y_LIM)
                q_hrs = [float(np.sum(hit & (q_15_arr[32:] == q)) * 0.25) for q in range(4)]
            elif kind == "cubic":
                fn = CubicSpline(phi, x_in)
                xa = f_hat * fn(xq1) + (1.0 - f_hat) * fn(xq2)
                hit = (xa[32:] > core.SCALING_X_LIM) & (y_out[32:] > core.SCALING_Y_LIM)
                q_hrs = [float(np.sum(hit & (q_15_arr[32:] == q)) * 0.25) for q in range(4)]
            elif kind == "nearest":
                def _nn(xq):
                    ir = np.clip(np.searchsorted(phi, xq, side="left"), 1, n_15 - 1)
                    il = ir - 1
                    idx_n = np.where(np.abs(phi[ir] - xq) < np.abs(xq - phi[il]), ir, il)
                    return x_in[idx_n]
                xa = f_hat * _nn(xq1) + (1.0 - f_hat) * _nn(xq2)
                hit = (xa[32:] > core.SCALING_X_LIM) & (y_out[32:] > core.SCALING_Y_LIM)
                q_hrs = [float(np.sum(hit & (q_15_arr[32:] == q)) * 0.25) for q in range(4)]
            elif kind == "ou_krig":
                q_mu = np.array([float(np.mean(x_in[q_15_arr == q])) for q in range(4)])
                xr = x_in - q_mu[q_15_arr]
                var_x = float(np.var(xr, ddof=1))
                r1_x = float(np.corrcoef(xr[:-1], xr[1:])[0, 1])
                dv_med = float(np.median(np.diff(phi)))
                L_hat = max(35.0, -dv_med / math.log(max(0.05, min(0.995, r1_x))))

                def _krig(xq):
                    ir = np.clip(np.searchsorted(phi, xq, side="left"), 1, n_15 - 1)
                    il = ir - 1
                    dL = np.maximum(0.0, xq - phi[il])
                    dR = np.maximum(0.0, phi[ir] - xq)
                    dT = np.maximum(1e-6, phi[ir] - phi[il])
                    rL = np.exp(-dL / L_hat)
                    rR = np.exp(-dR / L_hat)
                    rT = np.exp(-dT / L_hat)
                    den = np.maximum(1e-9, 1.0 - rT * rT)
                    wL = (rL - rT * rR) / den
                    wR = (rR - rT * rL) / den
                    mu_k = q_mu[q_15_arr] + wL * xr[il] + wR * xr[ir]
                    var_k = np.maximum(1e-9, var_x * (1.0 - (rL * rL + rR * rR - 2.0 * rL * rR * rT) / den))
                    return mu_k, var_k

                m1, v1 = _krig(xq1)
                m2, v2 = _krig(xq2)
                mu_mix = f_hat * m1 + (1.0 - f_hat) * m2
                sd_mix = np.sqrt(np.maximum(1e-9, (f_hat ** 2) * v1 + ((1.0 - f_hat) ** 2) * v2))
                z_k = (core.SCALING_X_LIM - mu_mix[32:]) / sd_mix[32:]
                p_exc = np.array([core._norm_sf(float(zv)) for zv in z_k])
                y_hit = (y_out[32:] > core.SCALING_Y_LIM).astype(float)
                q_hrs = [float(np.sum(p_exc * y_hit * (q_15_arr[32:] == q)) * 0.25) for q in range(4)]
            else:
                raise ValueError(kind)
            out_v[u] = {"q": q_hrs, "f_hat": f_hat, "v1_hat": v1_hat, "v2_hat": v2_hat, "c_rms": r2_g[u]["c_rms"]}
        return out_v

    s1_vars = [
        ("S1: continuous OU kernel (1h-normalized WLS)", core.estimate_s1(data, mode="golden", kernel="ou", obj="wls")),
        ("S1: discrete AR(1) OLS moments", core.estimate_s1(data, mode="golden", kernel="ar1", obj="ols")),
        ("S1: discrete AR(1) lag-1-weighted moments", core.estimate_s1(data, mode="golden", kernel="ar1", obj="lag1")),
        ("S1: AR(1) WLS with 0.5% residual trimming", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", trim_frac=0.005)),
        ("S1: AR(1) WLS without lab-noise subtraction", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", lab_noise=False)),
        ("S1: AR(1) WLS on 4h residual moments only", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", use_8h=False)),
        ("S1: span-weighted WLS 1/Q_bar flux regression", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", flux_fit="wls_span")),
        ("S1: Huber IRLS 1/Q_bar flux regression", core.estimate_s1(data, mode="golden", kernel="ar1", obj="wls", flux_fit="huber")),
    ]
    s2_vars = [
        ("S2: piecewise-constant step flow (right)", core.estimate_s2(data, mode="golden", flow_interp="step", loss_fn="l2")),
        ("S2: piecewise-constant step flow (left)", _estimate_s2_parcel_variant("step_left")),
        ("S2: midpoint flow integration", core.estimate_s2(data, mode="golden", flow_interp="midpoint", loss_fn="l2")),
        ("S2: L1 two-path conductivity profile loss", core.estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="l1")),
        ("S2: Huber two-path conductivity profile loss", core.estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="huber")),
        ("S2: 2% trimmed L2 two-path conductivity loss", core.estimate_s2(data, mode="golden", flow_interp="linear", loss_fn="trimmed_l2")),
        ("S2: Gaussian OU kriging two-path TEP lookup", _estimate_s2_parcel_variant("ou_krig")),
        ("S2: PCHIP interpolation two-path TEP lookup", _estimate_s2_parcel_variant("pchip")),
        ("S2: nearest 15-min two-path TEP lookup", _estimate_s2_parcel_variant("nearest")),
        ("S2: cubic spline two-path TEP lookup", _estimate_s2_parcel_variant("cubic")),
    ]
    s3_vars = [
        ("S3: per-train CIP clearing ratios", core.estimate_s3(data, mode="golden", post_blocks=30, shared_clear=False)),
        ("S3: cross-recipe clearing allowance", core.estimate_s3(data, mode="golden", post_blocks=30, shared_clear=True, allow_cross_clear=True)),
        ("S3: 96-hour (24-block) post-CIP window", core.estimate_s3(data, mode="golden", post_blocks=24)),
        ("S3: 144-hour (36-block) post-CIP window", core.estimate_s3(data, mode="golden", post_blocks=36)),
        ("S3: inclusive <=120h (31-block) post-CIP window", core.estimate_s3(data, mode="golden", post_blocks=31)),
    ]
    variants_named = []
    for nm, v1 in s1_vars:
        variants_named.append((nm, core.assemble(v1, r2_g, r3_g)))
    for nm, v2 in s2_vars:
        variants_named.append((nm, core.assemble(r1_g, v2, r3_g)))
    for nm, v3 in s3_vars:
        variants_named.append((nm, core.assemble(r1_g, r2_g, v3)))
    variants_named.append(("Joint A: OU flux-AR1 + L1 two-path + per-train CIP", core.assemble(s1_vars[0][1], s2_vars[3][1], s3_vars[0][1])))
    variants_named.append(("Joint B: Huber flux + Huber two-path + 96h CIP", core.assemble(s1_vars[7][1], s2_vars[4][1], s3_vars[2][1])))
    variants_named.append(("Joint C: trimmed flux + trimmed-L2 two-path + 144h CIP", core.assemble(s1_vars[3][1], s2_vars[5][1], s3_vars[3][1])))

    # Run routes + 16 extra cutoff/hedge/Round-1 rival routes
    gen_asm = core.assemble(r1_over, r2_over, r3_r2)
    r1_hedge = {
        u: {
            **r1_g[u],
            "q": [0.8 * r1_h[u]["q"][q] + 0.2 * r1_g[u]["q"][q] for q in range(4)],
            "beta_hat": 0.2 * r1_g[u]["beta_hat"],
        }
        for u in core.TRAINS
    }
    r2_hedge = {
        u: {
            **r2_g[u],
            "q": [0.8 * r2_h[u]["q"][q] + 0.2 * r2_g[u]["q"][q] for q in range(4)],
            "c_rms": 0.8 * r2_h[u]["c_rms"] + 0.2 * r2_g[u]["c_rms"],
        }
        for u in core.TRAINS
    }
    r3_hedge = {
        u: {
            **r3_g[u],
            "q": [0.8 * r3_h[u]["q"][q] + 0.2 * r3_g[u]["q"][q] for q in range(4)],
            "preds": {k: 0.2 * r3_g[u]["preds"][k] for k in r3_g[u]["preds"]},
        }
        for u in core.TRAINS
    }
    hedge_asm = core.assemble(r1_hedge, r2_hedge, r3_hedge)

    r1_c4 = core.estimate_s1(data, mode="cutoff_4h")
    r1_linq = core.estimate_s1(data, mode="linear_q_no_deconv")
    r1_fnd = core.estimate_s1(data, mode="flux_only_no_deconv")
    r1_fiid = core.estimate_s1(data, mode="over_flux_iid")
    r2_fl = core.estimate_s2(data, mode="fixed_lag")
    r2_nv = core.estimate_s2(data, mode="nom_vol")
    r3_cpmv = core.estimate_s3(data, mode="post_cip_mv")
    r3_ds2_all = core.estimate_s3(data, mode="ds2_all")
    r3_un = core.estimate_s3(data, mode="unanimous")
    cut_asm = core.assemble(r1_c4, r2_fl, r3_cpmv)

    extra_routes = {
        "cutoff:r1_round1_full": rig_r1_asm,
        "cutoff:r2_round1_full": rig_r2_asm,
        "cutoff:s1_stationary_ar1_mle": core.assemble(r1_stat, r2_g, r3_g),
        "cutoff:s1_4h_only": core.assemble(r1_c4, r2_g, r3_g),
        "cutoff:s1_linear_q_no_deconv": core.assemble(r1_linq, r2_g, r3_g),
        "cutoff:s1_flux_no_deconv": core.assemble(r1_fnd, r2_g, r3_g),
        "cutoff:s1_flux_iid_over": core.assemble(r1_fiid, r2_g, r3_g),
        "cutoff:s2_single_plug_veff": core.assemble(r1_g, r2_sp, r3_g),
        "cutoff:s2_fixed_lag": core.assemble(r1_g, r2_fl, r3_g),
        "cutoff:s2_nom_vol": core.assemble(r1_g, r2_nv, r3_g),
        "cutoff:s3_r1_pooled_cip_3state": core.assemble(r1_g, r2_g, r3_r1),
        "cutoff:s3_r2_post_cip_ds2": core.assemble(r1_g, r2_g, r3_r2),
        "cutoff:s3_post_cip_mv": core.assemble(r1_g, r2_g, r3_cpmv),
        "cutoff:s3_ds2_all": core.assemble(r1_g, r2_g, r3_ds2_all),
        "cutoff:s3_unanimous": core.assemble(r1_g, r2_g, r3_un),
        "hedge:history_2026_flat": core.assemble(r1_g, r2_g, r3_g, forward=False),
    }

    # Native-unit physical falsification F1, F2, F3
    fal_by_route = {}
    for label, (x1, x2, x3) in [
        ("golden", (r1_g, r2_g, r3_g)),
        ("direct", (r1_h, r2_h, r3_h)),
        ("rigorous_r1", (r1_stat, r2_sp, r3_r1)),
        ("rigorous_r2", (r1_stat, r2_sp, r3_r2)),
        ("generous", (r1_over, r2_over, r3_r2)),
        ("hedge", (r1_hedge, r2_hedge, r3_hedge)),
        ("cutoff", (r1_c4, r2_fl, r3_cpmv)),
        ("S1_stat_ar1", (r1_stat, r2_g, r3_g)),
        ("S2_single_plug", (r1_g, r2_sp, r3_g)),
        ("S3_r1_pooled", (r1_g, r2_g, r3_r1)),
        ("S1_lost", (r1_h, r2_g, r3_g)),
        ("S2_lost", (r1_g, r2_h, r3_g)),
        ("S3_lost", (r1_g, r2_g, r3_h)),
        ("S1_over", (r1_over, r2_g, r3_g)),
        ("S2_over", (r1_g, r2_over, r3_g)),
        ("S3_over", (r1_g, r2_g, r3_over)),
        ("s2_fixed_lag", (r1_g, r2_fl, r3_g)),
        ("s2_nom_vol", (r1_g, r2_nv, r3_g)),
    ]:
        f1, f2, f3 = core.falsification_score(data, x1, x2, x3)
        comb = f1 * 10.0 + max(0.0, f2 - 0.335) * 15.0 + f3 * 2.5
        fal_by_route[label] = {"f1": f1, "f2_ms_cm": f2, "f3_pp": f3, "combined": comb}

    # Six +/-20% forcing perturbations
    g_slate = sorted(u for u in core.TRAINS if gold_asm["members"][u] >= core.THRESHOLD)
    perturbations = []
    for name, f1m, f2m, f3m in [
        ("S1 boron -20%", 0.80, 1.0, 1.0),
        ("S1 boron +20%", 1.20, 1.0, 1.0),
        ("S2 scaling -20%", 1.0, 0.80, 1.0),
        ("S2 scaling +20%", 1.0, 1.20, 1.0),
        ("S3 structural -20%", 1.0, 1.0, 0.80),
        ("S3 structural +20%", 1.0, 1.0, 1.20),
    ]:
        p1 = {u: {"q": [x * f1m for x in r1_g[u]["q"]]} for u in core.TRAINS}
        p2 = {u: {"q": [x * f2m for x in r2_g[u]["q"]]} for u in core.TRAINS}
        p3 = {u: {"q": [x * f3m for x in r3_g[u]["q"]]} for u in core.TRAINS}
        asm = core.assemble(p1, p2, p3)
        sl = sorted(u for u in core.TRAINS if asm["members"][u] >= core.THRESHOLD)
        min_ov = min(asm["members"][u] for u in g_slate)
        max_mo = max(asm["members"][u] for u in core.TRAINS if u not in g_slate)
        perturbations.append(
            {
                "input": name,
                "answer": sl,
                "holds": sl == g_slate,
                "min_overhaul": min_ov,
                "max_monitor": max_mo,
            }
        )

    # Variant uncertainty ranges (exact min/max across golden + all 26 variants, padded gently)
    all_var_asms = [gold_asm] + [v for _, v in variants_named]

    def _band_for(key, is_member=False):
        vals = [a["members"][key] if is_member else a[key] for a in all_var_asms]
        lo, hi = min(vals), max(vals)
        span = hi - lo
        pad = max(0.08 * span, 0.012 * abs(vals[0]))
        return [round(lo - pad, 1), round(hi + pad, 1)], round(span, 2)

    bands = {}
    spreads = {}
    for u in core.TRAINS:
        b, sp = _band_for(u, is_member=True)
        bands[f"A_{u}"] = b
        spreads[u] = sp
    for fid in [
        "C1_boron_2027",
        "C2_scaling_2027",
        "C3_struct_2027",
        "A_total_2027",
        "A_overhaul_2027",
        "A_q3_2027",
        "A_energy_mwh",
        "A_overhaul_mwh",
    ]:
        b, sp = _band_for(fid, is_member=False)
        bands[fid] = b
        spreads[fid] = sp

    return {
        "cleaning": cleaning,
        "plan": plan,
        "train_rows": train_rows,
        "gold_asm": gold_asm,
        "rig_r1_asm": rig_r1_asm,
        "rig_r2_asm": rig_r2_asm,
        "rig_asm": rig_r1_asm,
        "gen_asm": gen_asm,
        "hedge_asm": hedge_asm,
        "cut_asm": cut_asm,
        "lattice_asm": lattice_asm,
        "over": {"S1": over_s1, "S2": over_s2, "S3": over_s3},
        "extra_routes": extra_routes,
        "variants_named": variants_named,
        "fal_by_route": fal_by_route,
        "perturbations": perturbations,
        "bands": bands,
        "spreads": spreads,
        "golden_slate": g_slate,
        "r1_g": r1_g,
        "r2_g": r2_g,
        "r3_g": r3_g,
        "r1_h": r1_h,
        "r2_h": r2_h,
        "r3_h": r3_h,
        "r1_stat": r1_stat,
        "r2_sp": r2_sp,
        "r3_r1": r3_r1,
        "r3_r2": r3_r2,
        "data": data,
    }


if __name__ == "__main__":
    tdir = os.path.join(os.path.dirname(HERE), "target")
    res = run_all(tdir)
    print("Cleaning:", json.dumps(res["cleaning"], indent=2))
    print("Golden slate:", res["golden_slate"])
    for u in core.TRAINS:
        tr = res["train_rows"][u]
        print(
            f"  {u}: 2027={tr['total_2027_h']:6.1f} h (B={tr['boron_2027_h']:5.1f} S={tr['scaling_2027_h']:5.1f} "
            f"St={tr['struct_2027_h']:5.1f} Q3={tr['q3_2027_h']:5.1f} MWh={tr['energy_2027_mwh']:7.2f}) -> {tr['designation']}"
        )
    print(
        f"Plant 2027: Total={res['gold_asm']['A_total_2027']:.1f} Overhaul={res['gold_asm']['A_overhaul_2027']:.1f} "
        f"Q3={res['gold_asm']['A_q3_2027']:.1f} Energy={res['gold_asm']['A_energy_mwh']:.1f} MWh "
        f"OvEnergy={res['gold_asm']['A_overhaul_mwh']:.1f} MWh"
    )
