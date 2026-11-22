"""Load and conform the 19-file shipped evidence pack under target/ strictly from disk (zero imports of core.simulate())."""
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
    """Read target_dir and return (pack_world, stats) with every array reconstructed strictly from shipped files."""
    F = PK.FILES

    # 1. Transformer & feeder register (no synthetic industrial_park_zone column)
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
    for row in ws_f.iter_rows(min_row=2, values_only=True):
        if not row[0]:
            continue
        rec = dict(zip(f_hdr, row))
        s = str(rec["substation_id"])
        fid = str(rec["scada_feeder_id"])
        f_idx_lookup[fid] = (s, len(f_meta_by_sub[s]))
        f_meta_by_sub[s].append(dict(
            feeder_id=fid,
            fcls=str(rec["customer_class"]),
        ))

    # 2. 66 kV sub-transmission radial corridors & GSP voltages
    cor_raw = {}
    with open(os.path.join(target_dir, F["cor_lines"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            cid = rec["corridor_id"]
            cor_raw.setdefault(cid, []).append((
                rec["from_bus"], rec["to_bus"],
                float(rec["length_km"]), float(rec["r_ohm_per_km"]), float(rec["x_ohm_per_km"]),
            ))
    corridors = {}
    sub_corridor = {}
    for cid, segs in cor_raw.items():
        to_set = {x[1] for x in segs}
        root = [x[0] for x in segs if x[0] not in to_set][0]
        by_from = {x[0]: x for x in segs}
        ordered = []
        cur = root
        while cur in by_from:
            seg = by_from[cur]
            ordered.append(seg)
            sub_corridor[seg[1]] = (cid, root)
            cur = seg[1]
        corridors[cid] = {"gsp": root, "segs": ordered}

    gsp_v = {}
    with open(os.path.join(target_dir, F["gsp_v"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            gid = rec["gsp_id"]
            if gid not in gsp_v:
                gsp_v[gid] = np.full(C.N_HOURS, np.nan)
            gsp_v[gid][_parse_utc_hour(rec["ts_utc"])] = float(rec["v_hv_kv"])

    # 3. Feeder crosswalk & engineering manual nominal PFs
    legacy_to_scada = {}
    with open(os.path.join(target_dir, F["xwalk"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            legacy_to_scada[rec["legacy_dms_id"]] = rec["scada_feeder_id"]
            legacy_to_scada[rec["scada_feeder_id"]] = rec["scada_feeder_id"]

    class_pf = {}
    with open(os.path.join(target_dir, F["class_pf"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            class_pf[rec["customer_class"]] = float(rec["nominal_pf"])

    # 4. Hourly substation SCADA (no v_hv_kv column; deduplicate on latest extract_ts)
    sub_p60 = {s: np.full(C.N_HOURS, np.nan) for s in sub_cfg}
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

    # 9. GIS lateral connectivity (all 36 laterals/sub, with metering_tier and annual_billed_mwh)
    lat_ids_by_sub = {s: [] for s in sub_cfg}
    lat_gis_ph = {s: [] for s in sub_cfg}
    lat_cls = {s: [] for s in sub_cfg}
    lat_is_ami = {s: [] for s in sub_cfg}
    lat_mwh = {s: [] for s in sub_cfg}
    ami_loc_map = {}   # lateral_id -> (substation_id, local_ami_idx 0..19)
    ami_cnt = {s: 0 for s in sub_cfg}
    with open(os.path.join(target_dir, F["gis_lat"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            s = rec["substation_id"]
            lid = rec["lateral_id"]
            is_ami = rec["metering_tier"].strip() == "AMI_SMART"
            lat_ids_by_sub[s].append(lid)
            lat_gis_ph[s].append(PH_IDX[rec["gis_phase"]])
            lat_cls[s].append(rec["customer_class"])
            lat_is_ami[s].append(is_ami)
            lat_mwh[s].append(float(rec["annual_billed_mwh"]))
            if is_ami:
                ami_loc_map[lid] = (s, ami_cnt[s])
                ami_cnt[s] += 1
    for s in sub_cfg:
        lat_gis_ph[s] = np.array(lat_gis_ph[s], dtype=int)
        lat_is_ami[s] = np.array(lat_is_ami[s], dtype=bool)
        lat_mwh[s] = np.array(lat_mwh[s], dtype=float)

    # Commissioning tracer log (20 AMI_SMART laterals x 4 modernized sites = 80 rows)
    ref_traced_ami = {r: np.full(ami_cnt[r], -1, dtype=int) for r in refs}
    with open(os.path.join(target_dir, F["ref_tracer"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            s, a_i = ami_loc_map[rec["lateral_id"]]
            ref_traced_ami[s][a_i] = PH_IDX[rec["traced_phase"]]

    # 10. SQLite AMI lateral hourly voltages & loads (20 AMI_SMART laterals/sub x 4,368 heating hours)
    lat_v_ami = {s: np.full((ami_cnt[s], C.N_HOURS), np.nan) for s in sub_cfg}
    lat_p_ami = {s: np.full((ami_cnt[s], C.N_HOURS), np.nan) for s in sub_cfg}
    conn = sqlite3.connect(os.path.join(target_dir, F["ami_db"]))
    db_map = {}
    for lidx, lid, _s in conn.execute("SELECT lateral_idx, lateral_id, substation_id FROM laterals"):
        db_map[lidx] = ami_loc_map[lid]
    for lidx, hidx, vv, pk in conn.execute("SELECT lateral_idx, hour_idx, v_volts, p_kw FROM lateral_hourly"):
        s, a_i = db_map[lidx]
        lat_v_ami[s][a_i, hidx] = vv
        lat_p_ami[s][a_i, hidx] = pk
    conn.close()

    # 11. Modernized substations continuous 15-min 3-phase main-bay PQ archive (no feeder columns!)
    ref_p15 = {r: np.zeros((C.N_HOURS, 4)) for r in refs}
    ref_q15 = {r: np.zeros((C.N_HOURS, 4)) for r in refs}
    ref_p15_ph = {r: np.zeros((3, C.N_HOURS, 4)) for r in refs}
    with open(os.path.join(target_dir, F["ref_pq"]), encoding="utf-8") as f:
        for rec in csv.DictReader(f):
            r = rec["substation_id"]
            d = dt.datetime.strptime(rec["ts_utc"], "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=UTC)
            k = int(round((d - BASE_UTC).total_seconds() / 900.0))
            h, q = divmod(k, 4)
            ref_p15_ph[r][0, h, q] = float(rec["sub_pa_mw"])
            ref_p15_ph[r][1, h, q] = float(rec["sub_pb_mw"])
            ref_p15_ph[r][2, h, q] = float(rec["sub_pc_mw"])
            ref_p15[r][h, q] = float(rec["sub_p15_mw"])
            ref_q15[r][h, q] = float(rec["sub_q15_mvar"])

    # Assemble pack_world dict matching core.evaluate() contract
    world = {"subs": {}, "gsp_v": gsp_v, "corridors": corridors, "class_pf": class_pf}
    for s in sorted(sub_cfg):
        cid, gsp_id = sub_corridor[s]
        sd = dict(
            cfg=sub_cfg[s],
            corridor=cid,
            gsp=gsp_id,
            f_meta=f_meta_by_sub[s],
            f_p60=f_p60[s],
            sub_p60=sub_p60[s],
            feeder_m15=feeder_m15[s],
            feeder_p60_m=feeder_p60_m[s],
            sub_kwh_m=sub_kwh_m[s],
            sub_net_kvarh_m=sub_net_kvarh_m[s],
            v_lv_meas=v_lv_meas[s],
            tap_step_int=tap_step[s],
            v_bus_ph=v_bus_ph[s],
            lat_gis_ph=lat_gis_ph[s],
            lat_cls=lat_cls[s],
            lat_is_ami=lat_is_ami[s],
            lat_mwh=lat_mwh[s],
            lat_v_ami=lat_v_ami[s],
            lat_p_ami=lat_p_ami[s],
        )
        if s in refs:
            sp15 = ref_p15[s]
            sq15 = ref_q15[s]
            sp15_ph = ref_p15_ph[s]
            sub_s15 = np.sqrt(sp15 ** 2 + sq15 ** 2)
            s_flat = int(np.argmax(sub_s15))
            s_h, s_q = divmod(s_flat, 4)
            true_s15 = float(sub_s15[s_h, s_q])
            true_p15 = float(sp15.max())
            true_qh = float(sq15[s_h, :].mean())
            true_q15 = float(sq15[s_h, s_q])
            true_w = float(sp15_ph[:, s_h, s_q].max() / sp15[s_h, s_q])
            true_lim = float(3.0 * true_w * true_s15)
            true_load = float(100.0 * true_lim / sub_cfg[s]["firm_mva"])
            sd.update(dict(
                sub_p15=sp15,
                sub_p15_ph=sp15_ph,
                q_15=sq15,
                q_hourly=sq15.mean(axis=1),
                ami_true_ph=ref_traced_ami[s],
                truth=dict(
                    p15_peak=true_p15,
                    p60_peak=float(sub_p60[s].max()),
                    q_peak_h=true_qh,
                    q15_at_peak=true_q15,
                    s15_tot=true_s15,
                    w_max=true_w,
                    lim_mva=true_lim,
                    loading_pct=true_load,
                    relief_mva=max(0.0, true_lim - 0.85 * sub_cfg[s]["firm_mva"]),
                    s_peak_h=s_h,
                ),
            ))
        world["subs"][s] = sd

    stats = dict(
        raw_scada_rows=raw_scada_rows,
        superseded_dropped=superseded_dropped,
        vlv_nulls=vlv_nulls,
        in_pool=sorted(in_pool),
        refs=sorted(refs),
        n_corridors=len(corridors),
        n_gsp=len(gsp_v),
        n_ami_per_sub=ami_cnt[in_pool[0]],
        n_leg_per_sub=C.N_LATERALS - ami_cnt[in_pool[0]],
    )
    return world, stats
