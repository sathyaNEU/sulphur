"""Load and conform the shipped evidence pack under target/ strictly from disk (zero imports of core.simulate())."""
import csv
import datetime as dt
import os
import sqlite3

import numpy as np
import openpyxl

import core as C
import pack as PK

UTC = dt.timezone.utc
CET_FIXED = dt.timezone(dt.timedelta(hours=1))
BASE_UTC = PK.BASE_UTC
PH_IDX = {"A": 0, "B": 1, "C": 2}


def _parse_scada_hour(ts_str, scada_clock):
    if scada_clock == "CET_Standard":
        d = dt.datetime.strptime(ts_str, "%d.%m.%Y %H:%M").replace(tzinfo=CET_FIXED).astimezone(UTC)
    else:
        d = dt.datetime.fromisoformat(ts_str).astimezone(UTC)
    return int(round((d - BASE_UTC).total_seconds() / 3600.0))


def _parse_utc_hour(ts_str):
    d = dt.datetime.strptime(ts_str, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
    return int(round((d - BASE_UTC).total_seconds() / 3600.0))


def _interp_nans(arr):
    out = arr.copy()
    bad = np.isnan(out)
    if bad.any():
        good = np.where(~bad)[0]
        out[bad] = np.interp(np.where(bad)[0], good, out[good])
    return out


def load_pack(target_dir, include_superseded=False, interpolate_nulls=True):
    """Read target_dir and return (pack_world, stats) with every array reconstructed from shipped files."""
    F = PK.FILES

    # 1. Transformer & feeder register
    wb_tx = openpyxl.load_workbook(os.path.join(target_dir, F["tx_xlsx"]), data_only=True)
    ws_s = wb_tx["Substations"]
    s_hdr = [c.value for c in ws_s[1]]
    sub_cfg = {}
    in_pool = []
    refs = []
    for row in ws_s.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        rec = dict(zip(s_hdr, row))
        s = str(rec["substation_id"])
        is_mod = str(rec["modernization_status"]).strip().lower() == "modernized_2023_2024"
        sub_cfg[s] = dict(
            firm_mva=float(rec["firm_n1_mva"]),
            r_ohm=float(rec["r_ohm"]),
            x_ohm=float(rec["x_ohm"]),
            hv_nom_kv=float(rec["hv_nom_kv"]),
            lv_nom_kv=float(rec["lv_nom_kv"]),
            tap_step_pct=float(rec["ltc_tap_step_pct"]),
            in_pool=(not is_mod),
        )
        if not is_mod:
            in_pool.append(s)
        else:
            refs.append(s)

    ws_f = wb_tx["Feeders"]
    f_hdr = [c.value for c in ws_f[1]]
    f_meta_by_sub = {s: [] for s in sub_cfg}
    f_idx_lookup = {}
    zone_to_id = {}
    next_zid = 1
    for row in ws_f.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        rec = dict(zip(f_hdr, row))
        s = str(rec["substation_id"])
        fid = str(rec["scada_feeder_id"])
        zname = str(rec["industrial_park_zone"] or "None").strip()
        if zname.lower() in ("none", "", "na"):
            pg = 0
        else:
            if zname not in zone_to_id:
                zone_to_id[zname] = next_zid
                next_zid += 1
            pg = zone_to_id[zname]
        f_idx_lookup[fid] = (s, len(f_meta_by_sub[s]))
        f_meta_by_sub[s].append(dict(
            feeder_id=fid,
            fcls=str(rec["customer_class"]),
            park_group=pg,
            park_zone=zname,
        ))

    # 2. Feeder crosswalk (legacy_dms_id -> scada_feeder_id)
    legacy_to_scada = {}
    with open(os.path.join(target_dir, F["xwalk"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            legacy_to_scada[rec["legacy_dms_id"]] = rec["scada_feeder_id"]
            legacy_to_scada[rec["scada_feeder_id"]] = rec["scada_feeder_id"]

    # 3. Engineering manual nominal class PFs
    class_pf = {}
    with open(os.path.join(target_dir, F["class_pf"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            class_pf[rec["customer_class"]] = float(rec["nominal_pf"])

    # 4. Hourly substation SCADA (deduplicate on latest extract_ts)
    sub_p60 = {s: np.full(C.N_HOURS, np.nan) for s in sub_cfg}
    v_hv_meas = {s: np.full(C.N_HOURS, np.nan) for s in sub_cfg}
    v_lv_meas = {s: np.full(C.N_HOURS, np.nan) for s in sub_cfg}
    tap_step = {s: np.zeros(C.N_HOURS, dtype=int) for s in sub_cfg}
    latest_ts = {s: [""] * C.N_HOURS for s in sub_cfg}
    raw_scada_rows = 0
    superseded_dropped = 0
    vlv_nulls = 0

    with open(os.path.join(target_dir, F["scada_sub"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            raw_scada_rows += 1
            s = rec["substation_id"]
            h = _parse_scada_hour(rec["timestamp_local"], rec["scada_clock"])
            ets = rec["extract_ts"]
            prev = latest_ts[s][h]
            if prev:
                if include_superseded:
                    if ets > prev:
                        superseded_dropped += 1
                        continue
                else:
                    if ets < prev:
                        superseded_dropped += 1
                        continue
                    superseded_dropped += 1
            latest_ts[s][h] = ets
            sub_p60[s][h] = float(rec["p_active_mw"])
            v_hv_meas[s][h] = float(rec["v_hv_kv"])
            if rec["v_lv_kv"] == "":
                v_lv_meas[s][h] = np.nan
                vlv_nulls += 1
            else:
                v_lv_meas[s][h] = float(rec["v_lv_kv"])
            tap_step[s][h] = int(rec["ltc_tap_step"])

    if interpolate_nulls:
        for s in sub_cfg:
            v_lv_meas[s] = _interp_nans(v_lv_meas[s])

    # 5. Hourly feeder SCADA (kW -> MW, legacy crosswalk)
    f_p60 = {s: np.zeros((len(f_meta_by_sub[s]), C.N_HOURS)) for s in sub_cfg}
    with open(os.path.join(target_dir, F["scada_fdr"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            fid = legacy_to_scada[rec["feeder_code"]]
            s, f_i = f_idx_lookup[fid]
            h = _parse_utc_hour(rec["ts_utc"])
            f_p60[s][f_i, h] = float(rec["p_active_kw"]) / 1000.0

    # 6. Monthly feeder 15-min max registers
    feeder_m15 = {s: np.zeros((len(f_meta_by_sub[s]), 12)) for s in sub_cfg}
    feeder_p60_m = {s: np.zeros((len(f_meta_by_sub[s]), 12)) for s in sub_cfg}
    with open(os.path.join(target_dir, F["fdr_m15"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            fid = legacy_to_scada[rec["feeder_code"]]
            s, f_i = f_idx_lookup[fid]
            m = int(rec["billing_month"].split("-")[1]) - 1
            feeder_m15[s][f_i, m] = float(rec["max_15min_demand_mw"])
    for s in sub_cfg:
        for m in range(12):
            hm = C.HOUR_MONTH == m
            feeder_p60_m[s][:, m] = f_p60[s][:, hm].max(axis=1)

    # 7. Monthly revenue meter kWh and net kVARh
    sub_kwh_m = {s: np.zeros(12) for s in sub_cfg}
    sub_net_kvarh_m = {s: np.zeros(12) for s in sub_cfg}
    wb_rev = openpyxl.load_workbook(os.path.join(target_dir, F["rev_xlsx"]), data_only=True)
    ws_r = wb_rev["Monthly_Revenue_Meters"]
    r_hdr = [c.value for c in ws_r[1]]
    for row in ws_r.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        rec = dict(zip(r_hdr, row))
        s = str(rec["substation_id"])
        m = int(str(rec["billing_month"]).split("-")[1]) - 1
        sub_kwh_m[s][m] = float(rec["active_energy_kwh"])
        sub_net_kvarh_m[s][m] = float(rec["net_reactive_energy_kvarh"])

    # 8. Hourly 3-phase LV bus voltages
    v_bus_ph = {s: np.zeros((3, C.N_HOURS)) for s in sub_cfg}
    with open(os.path.join(target_dir, F["bus_vph"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            s = rec["substation_id"]
            h = _parse_utc_hour(rec["ts_utc"])
            v_bus_ph[s][0, h] = float(rec["va_kv"])
            v_bus_ph[s][1, h] = float(rec["vb_kv"])
            v_bus_ph[s][2, h] = float(rec["vc_kv"])

    # 9. GIS lateral connectivity & commissioning phase log (modernized sites)
    lat_ids_by_sub = {s: [] for s in sub_cfg}
    lat_gis_ph = {s: [] for s in sub_cfg}
    lat_cls = {s: [] for s in sub_cfg}
    lat_pos = {}
    with open(os.path.join(target_dir, F["gis_lat"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            s = rec["substation_id"]
            lid = rec["lateral_id"]
            lat_pos[lid] = (s, len(lat_ids_by_sub[s]))
            lat_ids_by_sub[s].append(lid)
            lat_gis_ph[s].append(PH_IDX[rec["gis_phase"]])
            lat_cls[s].append(rec["customer_class"])
    for s in sub_cfg:
        lat_gis_ph[s] = np.array(lat_gis_ph[s], dtype=int)

    ref_traced_ph = {r: np.full(C.N_LATERALS, -1, dtype=int) for r in refs}
    with open(os.path.join(target_dir, F["ref_tracer"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            s, l_i = lat_pos[rec["lateral_id"]]
            ref_traced_ph[s][l_i] = PH_IDX[rec["traced_phase"]]

    # 10. SQLite AMI lateral hourly voltages & loads (6-month heating season Oct-Mar)
    lat_v_hourly = {s: np.full((C.N_LATERALS, C.N_HOURS), np.nan) for s in sub_cfg}
    lat_p_hourly = {s: np.full((C.N_LATERALS, C.N_HOURS), np.nan) for s in sub_cfg}
    conn = sqlite3.connect(os.path.join(target_dir, F["ami_db"]))
    lat_map = {}
    for lidx, lid, s in conn.execute("SELECT lateral_idx, lateral_id, substation_id FROM laterals"):
        lat_map[lidx] = lat_pos[lid]
    for lidx, hidx, vv, pk in conn.execute("SELECT lateral_idx, hour_idx, v_volts, p_kw FROM lateral_hourly"):
        s, l_i = lat_map[lidx]
        lat_v_hourly[s][l_i, hidx] = vv
        lat_p_hourly[s][l_i, hidx] = pk
    conn.close()

    for s in sub_cfg:
        pk_h = int(np.argmax(sub_p60[s]))
        sp_share_obs = float(lat_p_hourly[s][:, pk_h].sum() / (sub_p60[s][pk_h] * 1000.0))
        sub_cfg[s]["sp_share"] = sp_share_obs

    # 11. Modernized substations continuous 15-min PQ archive (Fossheim, Lindberg, Ostervik & Solberg)
    ref_p15 = {r: np.zeros((C.N_HOURS, 4)) for r in refs}
    ref_q15 = {r: np.zeros((C.N_HOURS, 4)) for r in refs}
    ref_fp15 = {r: np.zeros((len(f_meta_by_sub[r]), C.N_HOURS, 4)) for r in refs}
    with open(os.path.join(target_dir, F["ref_pq"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            r = rec["substation_id"]
            d = dt.datetime.strptime(rec["ts_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            k = int(round((d - BASE_UTC).total_seconds() / 900.0))
            h, q = divmod(k, 4)
            ref_p15[r][h, q] = float(rec["sub_p15_mw"])
            ref_q15[r][h, q] = float(rec["sub_q15_mvar"])
            for fi in range(len(f_meta_by_sub[r])):
                ref_fp15[r][fi, h, q] = float(rec[f"f{fi + 1:02d}_p15_mw"])

    pack_world = {"subs": {}, "class_pf": class_pf}
    for s in sub_cfg:
        sd = dict(
            cfg=sub_cfg[s],
            f_meta=f_meta_by_sub[s],
            f_p60=f_p60[s],
            sub_p60=sub_p60[s],
            feeder_m15=feeder_m15[s],
            feeder_p60_m=feeder_p60_m[s],
            sub_kwh_m=sub_kwh_m[s],
            sub_net_kvarh_m=sub_net_kvarh_m[s],
            v_hv_meas=v_hv_meas[s],
            v_lv_meas=v_lv_meas[s],
            tap_step_int=tap_step[s],
            v_bus_ph=v_bus_ph[s],
            lat_gis_ph=lat_gis_ph[s],
            lat_cls=lat_cls[s],
            lat_p_hourly=lat_p_hourly[s],
            lat_v_hourly=lat_v_hourly[s],
        )
        if s in refs:
            sd["sub_p15"] = ref_p15[s]
            sd["q_15"] = ref_q15[s]
            sd["q_hourly"] = ref_q15[s].mean(axis=1)
            sd["f_p15"] = ref_fp15[s]
            sd["lat_true_ph"] = ref_traced_ph[s]
            sub_s15 = np.sqrt(ref_p15[s] ** 2 + ref_q15[s] ** 2)
            sp_h, sp_q = divmod(int(np.argmax(sub_s15)), 4)
            true_s15 = float(sub_s15[sp_h, sp_q])
            bal_kw = sub_p60[s][sp_h] * 1000.0 - lat_p_hourly[s][:, sp_h].sum()
            ph_kw = np.array([lat_p_hourly[s][ref_traced_ph[s] == ph, sp_h].sum() + bal_kw / 3.0 for ph in range(3)])
            true_w = float(ph_kw.max() / ph_kw.sum())
            true_lim = float(3.0 * true_w * true_s15)
            sd["truth"] = dict(
                p15_peak=float(ref_p15[s].max()),
                p60_peak=float(sub_p60[s].max()),
                q_peak_h=float(sd["q_hourly"][sp_h]),
                s15_tot=true_s15,
                w_max=true_w,
                lim_mva=true_lim,
                loading_pct=float(100.0 * true_lim / sub_cfg[s]["firm_mva"]),
                relief_mva=float(max(0.0, true_lim - 0.85 * sub_cfg[s]["firm_mva"])),
                s_peak_h=sp_h,
            )
        pack_world["subs"][s] = sd

    stats = dict(
        raw_scada_rows=raw_scada_rows,
        superseded_dropped=superseded_dropped,
        vlv_nulls=vlv_nulls,
        in_pool=sorted(in_pool),
        refs=sorted(refs),
    )
    return pack_world, stats
