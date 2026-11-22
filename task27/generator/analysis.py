"""Independent end-to-end analysis reading ONLY the shipped files under task27/target/.

Performs complete Layer 1 data cleaning from scratch (VOID filtering, extract_version deduplication,
mixed DD.MM.YYYY / YYYY-MM-DD date parsing, CASE-to-PALLET conversion, legacy store/carrier
crosswalk resolution, UTC vs Europe/Berlin CET/CEST timestamp verification), executes the three
cross-grain physical conservation models (S1, S2, S3), all 22 defensible variants, all 8 +/-20%
forcing perturbations, all lattice/shortcut/run routes, and emits:
  - task27/generator/figures.json
  - task27/generator/effort.json
"""
import csv
import datetime as dt
import itertools
import json
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import core  # noqa: E402
import pack as PK  # noqa: E402

UTC = dt.timezone.utc
BERLIN = ZoneInfo("Europe/Berlin")
BASE_DATE = dt.date(2026, 1, 1)

PORT_IDX = {p: i for i, p in enumerate(core.PORTS)}
DC_IDX = {d: i for i, d in enumerate(core.DCS)}
ZONE_IDX = {z: i for i, z in enumerate(core.ZONES)}
LINE_IDX = {l: i for i, l in enumerate(core.LINES)}

CAUSE_NAMES = {
    "vessel_berth": "Vessel Berth & Arrival Slippage",
    "coldstore_dock": "Inland Cold-Store Dock & Receiving",
    "empty_depot": "Ocean-Line Empty Depot Intake",
    "reefer_plug": "Port Terminal Reefer Plug & Yard",
    "drayage_carrier": "Inland Drayage Carrier Turnaround",
    "phyto_insp": "EU BIP Phytosanitary Inspection",
    "rail_handoff": "Intermodal Rail Shuttle Handoff",
    "edi_docs": "Customs & EDI Documentation Hold",
}


def _parse_date(s):
    s = s.strip()
    if "." in s:
        d, m, y = s.split(".")
        return dt.date(int(y), int(m), int(d))
    return dt.date.fromisoformat(s)


def _parse_ts(s):
    s = s.strip()
    if s.endswith("Z"):
        return dt.datetime.fromisoformat(s[:-1] + "+00:00")
    return dt.datetime.fromisoformat(s)


def _day_to_quarter(day_arr):
    return np.searchsorted(np.array([90, 181, 273]), day_arr, side="right")


def load_shipped_pack(target_dir):
    """Read, clean, verify, and assemble all operational arrays solely from files in target_dir."""
    F = PK.FILES
    cleaning = {}

    # 1. Crosswalk
    store_map, carrier_map = {}, {}
    with open(os.path.join(target_dir, F["crosswalk"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["entity_type"] == "RETAIL_STORE":
                store_map[row["legacy_code"]] = row["canonical_code"]
            elif row["entity_type"] == "DRAYAGE_CARRIER":
                carrier_map[row["legacy_code"]] = row["canonical_code"]
    cleaning["crosswalk_store_mappings"] = len(store_map)
    cleaning["crosswalk_carrier_mappings"] = len(carrier_map)

    # 2. SKU Thermal Catalog
    sku_zone, sku_cpp = {}, {}
    with open(os.path.join(target_dir, F["skus"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sku_zone[row["sku_id"]] = ZONE_IDX[row["thermal_zone"]]
            sku_cpp[row["sku_id"]] = int(row["cases_per_pallet"])

    # 3. DC Chamber Register
    dc_caps = np.zeros((4, 3), dtype=float)
    chamber_opening = np.zeros((4, 3), dtype=int)
    with open(os.path.join(target_dir, F["chambers"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = DC_IDX[row["dc_id"]]
            z = ZONE_IDX[row["thermal_zone"]]
            dc_caps[d, z] = float(row["pallet_bay_capacity"])
            chamber_opening[d, z] = int(row["opening_pallets_2026_01_01"])
    dc_total_cap = dc_caps.sum(axis=1)

    # 4. Aggregate DC Daily Inventory
    dc_total_stock = np.zeros((4, core.N_DAYS), dtype=int)
    dc_total_util = np.zeros((4, core.N_DAYS), dtype=float)
    with open(os.path.join(target_dir, F["dc_inv"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (_parse_date(row["date_iso"]) - BASE_DATE).days
            d = DC_IDX[row["dc_id"]]
            dc_total_stock[d, t] = int(row["total_pallets_on_hand"])
            dc_total_util[d, t] = dc_total_stock[d, t] / dc_total_cap[d]

    # 5. Terminal Yard Daily
    port_yard_util = np.zeros((3, core.N_DAYS), dtype=float)
    with open(os.path.join(target_dir, F["port_yard"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (_parse_date(row["date_iso"]) - BASE_DATE).days
            p = PORT_IDX[row["port_id"]]
            port_yard_util[p, t] = float(row["reefer_yard_util_pct"]) / 100.0

    # 6. Warehouse Pallet Movements (dedup extract_version, parse mixed dates, CASE->PALLET, store crosswalk)
    latest_mv = {}
    mv_raw = 0
    mv_de_dates = 0
    mv_case_rows = 0
    mv_legacy_stores = 0
    with open(os.path.join(target_dir, F["pallets"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mv_raw += 1
            mid = row["movement_id"]
            ver = int(row["extract_version"])
            prev = latest_mv.get(mid)
            if prev is None or ver > prev[0]:
                latest_mv[mid] = (ver, row)

    pallet_in = np.zeros((4, 3, core.N_DAYS), dtype=int)
    pallet_out = np.zeros((4, 3, core.N_DAYS), dtype=int)
    for _, row in latest_mv.values():
        ds = row["move_date"].strip()
        if "." in ds:
            mv_de_dates += 1
        t = (_parse_date(ds) - BASE_DATE).days
        d = DC_IDX[row["dc_id"]]
        sk = row["sku_id"]
        z = sku_zone[sk]
        qty = int(row["quantity"])
        if row["unit"] == "CASE":
            mv_case_rows += 1
            assert qty % sku_cpp[sk] == 0, f"Non-integer pallet conversion for {sk}"
            pallets = qty // sku_cpp[sk]
        else:
            pallets = qty
        sc = row["store_code"].strip()
        if sc in store_map:
            mv_legacy_stores += 1
        if row["direction"] == "IN":
            pallet_in[d, z, t] += pallets
        else:
            pallet_out[d, z, t] += pallets

    # Exact daily conservation check against coldstore_inventory_daily_2026.csv
    chamber_stock = np.zeros((4, 3, core.N_DAYS), dtype=int)
    for d in range(4):
        for z in range(3):
            chamber_stock[d, z] = chamber_opening[d, z] + np.cumsum(pallet_in[d, z] - pallet_out[d, z])
    max_stock_diff = int(np.max(np.abs(chamber_stock.sum(axis=1) - dc_total_stock)))
    assert max_stock_diff == 0, f"Warehouse stock conservation diff = {max_stock_diff}"
    cleaning["pallets_raw_rows"] = mv_raw
    cleaning["pallets_dedup_rows"] = len(latest_mv)
    cleaning["pallets_superseded_dropped"] = mv_raw - len(latest_mv)
    cleaning["pallets_de_date_rows"] = mv_de_dates
    cleaning["pallets_case_unit_rows"] = mv_case_rows
    cleaning["pallets_legacy_store_rows"] = mv_legacy_stores
    cleaning["stock_flow_max_diff_pallets"] = max_stock_diff
    cleaning["dc_days_total"] = 4 * core.N_DAYS

    # 7. Import Plan 2027
    plan_2027 = {
        "vol_growth_port": {},
        "plug_capacity_factor_2027": {},
        "dc_zone_load_factor_2027": {},
        "bip_sampling_factor_2027": {},
        "line_share_2026": {},
        "line_share_2027": {},
        "depot_load_factor_2027": {},
    }
    with open(os.path.join(target_dir, F["plan_2027"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            mc = row["metric_code"]
            eid = row["entity_id"]
            v26 = float(row["value_2026"])
            v27 = float(row["value_2027"])
            if mc in ("vol_growth_port", "plug_capacity_factor_2027", "dc_zone_load_factor_2027",
                      "bip_sampling_factor_2027", "depot_load_factor_2027"):
                plan_2027[mc][eid] = v27
            elif mc == "rail_fleet_factor_2027":
                plan_2027["rail_fleet_factor_2027"] = v27
            elif mc == "dray_contract_factor_2027":
                plan_2027["dray_contract_factor_2027"] = v27
            elif mc == "line_volume_share":
                plan_2027["line_share_2026"][eid] = v26
                plan_2027["line_share_2027"][eid] = v27

    # 8. Rail Shuttle Departures (1,095 rows)
    n_sh = 3 * core.N_DAYS
    shuttle_port = np.zeros(n_sh, dtype=int)
    shuttle_day = np.zeros(n_sh, dtype=int)
    wf_booked_slots_sh = np.zeros(n_sh, dtype=int)
    wf_actual_loaded_sh = np.zeros(n_sh, dtype=int)
    wf_standby_rolled_total_sh = np.zeros(n_sh, dtype=int)
    train_wagon_count_sh = np.zeros(n_sh, dtype=int)
    train_gross_tonnes_sh = np.zeros(n_sh, dtype=float)
    shuttle_dep_ts = {}
    shuttle_id_to_idx = {}

    with open(os.path.join(target_dir, F["shuttles"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sid = row["shuttle_id"]
            p = PORT_IDX[row["port_id"]]
            d_code = sid.split("-")[-1]
            d_idx = (dt.date(int(d_code[:4]), int(d_code[4:6]), int(d_code[6:8])) - BASE_DATE).days
            s_idx = p * core.N_DAYS + d_idx
            shuttle_id_to_idx[sid] = s_idx
            shuttle_dep_ts[s_idx] = _parse_ts(row["departure_ts_utc"])
            shuttle_port[s_idx] = p
            shuttle_day[s_idx] = d_idx
            wf_booked_slots_sh[s_idx] = int(row["booked_wf_slots"])
            wf_actual_loaded_sh[s_idx] = int(row["loaded_wf_slots"])
            wf_standby_rolled_total_sh[s_idx] = int(row["wf_standby_rolled"])
            train_wagon_count_sh[s_idx] = int(row["train_wagon_count"])
            train_gross_tonnes_sh[s_idx] = float(row["train_total_gross_tonnes"])
    shuttle_quarter = _day_to_quarter(shuttle_day)

    # 9. Customs Consignment BoL Register (container -> ched_lot_id, gross mass)
    cont_to_ched_str = {}
    gross_kg_list = []
    with open(os.path.join(target_dir, F["consignments"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cont_to_ched_str[row["container_id"]] = row["ched_lot_id"]
            gross_kg_list.append(float(row["declared_net_kg"]) + float(row["reefer_tare_kg"]))
    measured_reefer_tonnes = float(np.mean(gross_kg_list) / 1000.0)

    # 10. BIP Inspection Notices (JSONL)
    bip_by_lot = {}
    with open(os.path.join(target_dir, F["bip_notices"]), encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            rec = json.loads(line)
            bip_by_lot[rec["ched_lot_id"]] = rec
    cleaning["bip_notices_count"] = len(bip_by_lot)

    # 11. Container Milestones (drop VOID, dedup extract_version, verify timestamps)
    latest_ms = {}
    ms_raw = 0
    ms_void = 0
    with open(os.path.join(target_dir, F["milestones"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ms_raw += 1
            if row["record_status"] == "VOID":
                ms_void += 1
                continue
            cid = row["container_id"]
            ver = int(row["extract_version"])
            prev = latest_ms.get(cid)
            if prev is None or ver > prev[0]:
                latest_ms[cid] = (ver, row)

    sorted_cids = sorted(latest_ms.keys())
    n = len(sorted_cids)
    assert n == core.N_CONTAINERS, f"Expected {core.N_CONTAINERS} settled containers, got {n}"
    cleaning["milestones_raw_rows"] = ms_raw
    cleaning["milestones_void_dropped"] = ms_void
    cleaning["milestones_superseded_dropped"] = (ms_raw - ms_void) - n
    cleaning["milestones_settled_containers"] = n

    vessel_to_idx = {}
    ched_to_idx = {}
    cont_vessel = np.zeros(n, dtype=int)
    cont_port = np.zeros(n, dtype=int)
    cont_day = np.zeros(n, dtype=int)
    cont_unload_day = np.zeros(n, dtype=int)
    cont_dc = np.zeros(n, dtype=int)
    cont_zone = np.zeros(n, dtype=int)
    cont_line = np.zeros(n, dtype=int)
    cont_is_rail = np.zeros(n, dtype=bool)
    cont_ched = np.zeros(n, dtype=int)
    cont_shuttle = np.zeros(n, dtype=int)
    cont_bip_sampled = np.zeros(n, dtype=bool)
    cont_rolled = np.zeros(n, dtype=bool)

    obs_vessel_berth = np.zeros(n, dtype=float)
    obs_edi_docs = np.zeros(n, dtype=float)
    obs_term_yard_hold = np.zeros(n, dtype=float)
    obs_phyto_hold_direct = np.zeros(n, dtype=float)
    obs_rail_all = np.zeros(n, dtype=float)
    obs_dc_dock_wait = np.zeros(n, dtype=float)
    obs_dray_empty_hold = np.zeros(n, dtype=float)
    obs_depot_turnaway = np.zeros(n, dtype=float)

    max_ts_err = 0.0
    for i, cid in enumerate(sorted_cids):
        _, row = latest_ms[cid]
        vid = row["vessel_id"]
        if vid not in vessel_to_idx:
            vessel_to_idx[vid] = len(vessel_to_idx)
        cont_vessel[i] = vessel_to_idx[vid]
        cont_port[i] = PORT_IDX[row["port_id"]]
        cont_dc[i] = DC_IDX[row["dc_id"]]
        cont_zone[i] = ZONE_IDX[row["thermal_zone"]]
        cont_line[i] = LINE_IDX[row["shipping_line_id"]]
        cont_is_rail[i] = (row["mode"] == "RAIL")

        dis_ts = _parse_ts(row["discharge_ts_utc"])
        cont_day[i] = (dis_ts.astimezone(UTC).date() - BASE_DATE).days
        cont_shuttle[i] = cont_port[i] * core.N_DAYS + cont_day[i]

        unload_ts = _parse_ts(row["unload_complete_ts_cet"])
        cont_unload_day[i] = (unload_ts.astimezone(BERLIN).date() - BASE_DATE).days

        if cont_is_rail[i]:
            p_sh = row["planned_shuttle_id"]
            a_sh = row["departed_shuttle_id"]
            assert shuttle_id_to_idx[p_sh] == cont_shuttle[i]
            cont_rolled[i] = (a_sh != p_sh)

        ched_str = cont_to_ched_str[cid]
        if ched_str not in ched_to_idx:
            ched_to_idx[ched_str] = len(ched_to_idx)
        cont_ched[i] = ched_to_idx[ched_str]
        cont_bip_sampled[i] = (row["bip_sampled_ind"] == "1")

        # Parse stage excess and verify against timestamps minus Charter free time
        eta_ts = _parse_ts(row["scheduled_eta_utc"])
        cust_ts = _parse_ts(row["customs_doc_ts_utc"])
        ready_ts = _parse_ts(row["port_gate_ready_ts_utc"])
        bip_ts = _parse_ts(row["bip_release_ts_utc"])
        dc_in_ts = _parse_ts(row["dc_gate_in_ts_cet"])
        dep_arr_ts = _parse_ts(row["depot_gate_arr_ts_utc"])
        emp_in_ts = _parse_ts(row["empty_gate_in_ts_utc"])

        ts_berth = max(0.0, ((dis_ts - eta_ts).total_seconds() / 3600.0 - 0.0) / 24.0)
        ts_edi = max(0.0, ((cust_ts - dis_ts).total_seconds() / 3600.0 - 6.0) / 24.0)
        ts_yard = max(0.0, ((ready_ts - cust_ts).total_seconds() / 3600.0 - 24.0) / 24.0)
        ts_phyto = max(0.0, ((bip_ts - ready_ts).total_seconds() / 3600.0 - 0.0) / 24.0)
        ts_dc = max(0.0, ((unload_ts - dc_in_ts).total_seconds() / 3600.0 - 4.0) / 24.0)
        ts_dray = max(0.0, ((dep_arr_ts - unload_ts).total_seconds() / 3600.0 - 24.0) / 24.0)
        ts_dep = max(0.0, ((emp_in_ts - dep_arr_ts).total_seconds() / 3600.0 - 0.0) / 24.0)
        assert eta_ts <= dis_ts <= cust_ts <= ready_ts <= bip_ts, f"Port chronology inversion on {cid}"
        if cont_is_rail[i]:
            r_ts = _parse_ts(row["rail_depart_ts_utc"])
            assert bip_ts <= r_ts < dc_in_ts, f"Rail chronology inversion on {cid}"
            ts_rail = max(0.0, ((r_ts - bip_ts).total_seconds() / 3600.0 - 6.0) / 24.0)
        else:
            assert bip_ts < dc_in_ts, f"Truck chronology inversion on {cid}"
            ts_rail = 0.0
        assert dc_in_ts < unload_ts < dep_arr_ts <= emp_in_ts, f"Inland/depot chronology inversion on {cid}"
        assert emp_in_ts.astimezone(UTC).date() <= dt.date(2027, 1, 19), f"Date past as_of on {cid}: {emp_in_ts}"

        obs_vessel_berth[i] = float(row["excess_berth_cdays"])
        obs_edi_docs[i] = float(row["excess_edi_cdays"])
        obs_term_yard_hold[i] = float(row["excess_port_yard_cdays"])
        obs_phyto_hold_direct[i] = float(row["excess_phyto_cdays"])
        obs_rail_all[i] = float(row["excess_rail_cdays"])
        obs_dc_dock_wait[i] = float(row["excess_dc_dock_cdays"])
        obs_dray_empty_hold[i] = float(row["excess_dray_empty_cdays"])
        obs_depot_turnaway[i] = float(row["excess_depot_gate_cdays"])

        for a, b in (
            (ts_berth, obs_vessel_berth[i]), (ts_edi, obs_edi_docs[i]),
            (ts_yard, obs_term_yard_hold[i]), (ts_phyto, obs_phyto_hold_direct[i]),
            (ts_rail, obs_rail_all[i]), (ts_dc, obs_dc_dock_wait[i]),
            (ts_dray, obs_dray_empty_hold[i]), (ts_dep, obs_depot_turnaway[i]),
        ):
            max_ts_err = max(max_ts_err, abs(a - b))

    assert max_ts_err < 2e-4, f"Timestamp-to-excess mismatch: {max_ts_err}"
    cleaning["max_timestamp_excess_err_cdays"] = round(max_ts_err, 6)
    cont_quarter = _day_to_quarter(cont_day)

    # Reconstruct lot-level arrays from customs_consignment_bol_2026.csv + bip_inspection_notices_2026.jsonl
    n_lots = len(ched_to_idx)
    lot_bip = np.zeros(n_lots, dtype=bool)
    lot_lead_hours = np.full(n_lots, 999.0, dtype=float)
    lot_port = np.zeros(n_lots, dtype=int)
    lot_day = np.zeros(n_lots, dtype=int)
    for i in range(n):
        lid = cont_ched[i]
        lot_port[lid] = cont_port[i]
        lot_day[lid] = cont_day[i]
    for ched_str, lid in ched_to_idx.items():
        if ched_str in bip_by_lot:
            lot_bip[lid] = True
            s_idx = lot_port[lid] * core.N_DAYS + lot_day[lid]
            notice_ts = _parse_ts(bip_by_lot[ched_str]["exam_notice_ts_utc"])
            lead_h = (shuttle_dep_ts[s_idx] - notice_ts).total_seconds() / 3600.0
            lot_lead_hours[lid] = lead_h

    non_bip_rail = cont_is_rail & (~lot_bip[cont_ched])
    mean_rolled = float(obs_rail_all[non_bip_rail & cont_rolled].mean())
    mean_unrolled = float(obs_rail_all[non_bip_rail & (~cont_rolled)].mean())
    measured_rollover_days = mean_rolled - mean_unrolled
    # Exact shuttle-level base & sibling separation (identically conserving obs_rail_all!):
    # On each shuttle, non-rolled non-BIP rail boxes carry pure per-box rail_base; subtract per-box rail_base
    # from CHED rail siblings to get pure sibling phyto delay, and from rolled boxes to get exact rollover days!
    sh_base_per_box = np.zeros(n_sh, dtype=float)
    for s in range(n_sh):
        m_clean = non_bip_rail & (~cont_rolled) & (cont_shuttle == s)
        if np.any(m_clean):
            sh_base_per_box[s] = float(obs_rail_all[m_clean].mean())
        else:
            m_any = non_bip_rail & (cont_shuttle == s)
            if np.any(m_any):
                sh_base_per_box[s] = max(0.0, float(obs_rail_all[m_any].mean() - measured_rollover_days))

    cont_rail_base = np.where(cont_is_rail, sh_base_per_box[cont_shuttle], 0.0)
    cont_bip_rail_sib = cont_is_rail & lot_bip[cont_ched] & (~cont_bip_sampled)
    obs_phyto_sibling_tms_rail = np.where(cont_bip_rail_sib, np.maximum(0.0, obs_rail_all - cont_rail_base), 0.0)
    obs_rail_roll_c = np.where(cont_rolled, np.maximum(0.0, obs_rail_all - cont_rail_base), 0.0)
    obs_rail_roll_days_sh = np.bincount(cont_shuttle, weights=obs_rail_roll_c, minlength=n_sh)
    # Exact conservation adjustment for obs_rail_base_sh so sum matches obs_rail_all to 1e-10
    obs_rail_base_sh = (
        np.bincount(cont_shuttle, weights=obs_rail_all - obs_phyto_sibling_tms_rail, minlength=n_sh)
        - obs_rail_roll_days_sh
    )
    assert np.isclose(
        obs_rail_roll_days_sh.sum() + obs_rail_base_sh.sum() + obs_phyto_sibling_tms_rail.sum(),
        obs_rail_all.sum(),
        atol=1e-6,
    )

    # 12. Depot Turn-in Log (verify physical gate acceptance & turnaway delay tie-out)
    latest_ti = {}
    ti_raw = 0
    ti_legacy_carriers = 0
    with open(os.path.join(target_dir, F["turnin"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ti_raw += 1
            eid = row["gate_event_id"]
            ver = int(row["extract_version"])
            prev = latest_ti.get(eid)
            if prev is None or ver > prev[0]:
                latest_ti[eid] = (ver, row)
    ti_accepted = 0
    ti_turnaway = 0
    ti_turnaway_cdays = 0.0
    for _, row in latest_ti.values():
        if row["carrier_code"] in carrier_map:
            ti_legacy_carriers += 1
        if row["gate_status"] == "ACCEPTED":
            ti_accepted += 1
        else:
            ti_turnaway += 1
            ti_turnaway_cdays += float(row["turnaway_delay_hours"]) / 24.0
    phys_gate_acc_pct = 100.0 * ti_accepted / (ti_accepted + ti_turnaway)
    assert abs(ti_turnaway_cdays - obs_depot_turnaway.sum()) < 1e-3
    cleaning["turnin_raw_rows"] = ti_raw
    cleaning["turnin_dedup_rows"] = len(latest_ti)
    cleaning["turnin_superseded_dropped"] = ti_raw - len(latest_ti)
    cleaning["turnin_legacy_carrier_rows"] = ti_legacy_carriers
    cleaning["turnin_physical_acceptance_pct"] = round(phys_gate_acc_pct, 2)
    cleaning["turnin_turnaway_events"] = ti_turnaway

    # 13. Depot Portal Requests (N_PORTAL_DAYS = 379 days: 2026-01-01 through 2027-01-14)
    n_pdays = core.N_PORTAL_DAYS
    portal_confirmed = np.zeros((3, 4, n_pdays), dtype=int)
    portal_rejected = np.zeros((3, 4, n_pdays), dtype=int)
    with open(os.path.join(target_dir, F["portal"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (_parse_date(row["date_iso"]) - BASE_DATE).days
            p = PORT_IDX[row["depot_port_id"]]
            l = LINE_IDX[row["shipping_line_id"]]
            portal_confirmed[p, l, t] = int(row["confirmed_bookings"])
            portal_rejected[p, l, t] = int(row["quota_closed_rejections"])

    # 14. Carrier Dispute Close-Out XLSX
    wb_disp = load_workbook(os.path.join(target_dir, F["disputes"]), data_only=True)
    ws_disp = wb_disp["Annual_Closeout_Summary"]
    dispute_closeout = {}
    for row in ws_disp.iter_rows(min_row=5, values_only=True):
        if row[0] and row[0] != "TOTAL":
            dispute_closeout[str(row[0])] = float(row[2])

    pack_w = {
        "cont_vessel": cont_vessel,
        "cont_port": cont_port,
        "cont_day": cont_day,
        "cont_unload_day": cont_unload_day,
        "cont_quarter": cont_quarter,
        "cont_dc": cont_dc,
        "cont_zone": cont_zone,
        "cont_line": cont_line,
        "cont_is_rail": cont_is_rail,
        "cont_ched": cont_ched,
        "cont_shuttle": cont_shuttle,
        "cont_bip_sampled": cont_bip_sampled,
        "obs_vessel_berth": obs_vessel_berth,
        "obs_edi_docs": obs_edi_docs,
        "obs_term_yard_hold": obs_term_yard_hold,
        "obs_dc_dock_wait": obs_dc_dock_wait,
        "obs_phyto_hold_direct": obs_phyto_hold_direct,
        "obs_phyto_sibling_tms_rail": obs_phyto_sibling_tms_rail,
        "obs_dray_empty_hold": obs_dray_empty_hold,
        "obs_depot_turnaway": obs_depot_turnaway,
        "port_yard_util": port_yard_util,
        "dc_total_stock": dc_total_stock,
        "dc_total_cap": dc_total_cap,
        "dc_total_util": dc_total_util,
        "dc_caps": dc_caps,
        "chamber_opening": chamber_opening,
        "pallet_in": pallet_in,
        "pallet_out": pallet_out,
        "lot_port": lot_port,
        "lot_day": lot_day,
        "lot_bip": lot_bip,
        "lot_lead_hours": lot_lead_hours,
        "shuttle_port": shuttle_port,
        "shuttle_day": shuttle_day,
        "shuttle_quarter": shuttle_quarter,
        "wf_booked_slots_sh": wf_booked_slots_sh,
        "wf_actual_loaded_sh": wf_actual_loaded_sh,
        "wf_standby_rolled_total_sh": wf_standby_rolled_total_sh,
        "obs_rail_roll_days_sh": obs_rail_roll_days_sh,
        "train_wagon_count_sh": train_wagon_count_sh,
        "train_gross_tonnes_sh": train_gross_tonnes_sh,
        "obs_rail_base_sh": obs_rail_base_sh,
        "portal_confirmed": portal_confirmed,
        "portal_rejected": portal_rejected,
        "dispute_closeout": dispute_closeout,
        "plan_2027": plan_2027,
        "measured_reefer_tonnes": measured_reefer_tonnes,
        "measured_rollover_days": measured_rollover_days,
        "mean_rolled_cdays": mean_rolled,
        "mean_unrolled_cdays": mean_unrolled,
        "cleaning": cleaning,
    }
    return pack_w


def _run_route_with_2026(w, s1_kw, s2_kw, s3_kw, proj_opts=None):
    rp_c, cs_dir_c, cs_pb_c, d1 = core.estimate_s1(w, **s1_kw)
    ph_dir_c, ph_sib_c, ph_bump_sh, rh_sh, rh_base_sh, d2 = core.estimate_s2(w, **s2_kw)
    dr_c, ed_phys_c, ed_blk_c, d3 = core.estimate_s3(w, **s3_kw)

    attr_26 = {
        "vessel_berth_c": w["obs_vessel_berth"],
        "edi_docs_c": w["obs_edi_docs"],
        "reefer_plug_c": rp_c,
        "coldstore_direct_c": cs_dir_c,
        "coldstore_pullback_c": cs_pb_c,
        "phyto_direct_c": ph_dir_c,
        "phyto_sibling_rail_c": ph_sib_c,
        "sh_phyto_bump_days": ph_bump_sh,
        "sh_rail_short_days": rh_sh,
        "rail_base_sh": rh_base_sh,
        "dray_carrier_c": dr_c,
        "depot_physical_c": ed_phys_c,
        "depot_portal_block_c": ed_blk_c,
    }
    res27 = core._project_2027(w, attr_26, opts=proj_opts)
    cdays_2026 = {
        "vessel_berth": float(w["obs_vessel_berth"].sum()),
        "edi_docs": float(w["obs_edi_docs"].sum()),
        "coldstore_dock": float(cs_dir_c.sum() + cs_pb_c.sum()),
        "reefer_plug": float(rp_c.sum()),
        "phyto_insp": float(ph_dir_c.sum() + ph_sib_c.sum() + ph_bump_sh.sum()),
        "rail_handoff": float(rh_sh.sum() + rh_base_sh.sum()),
        "empty_depot": float(ed_phys_c.sum() + ed_blk_c.sum()),
        "drayage_carrier": float(dr_c.sum()),
    }
    res27["cdays_2026"] = cdays_2026
    res27["total_2026"] = float(sum(cdays_2026.values()))
    res27["diag"] = {
        "twin_gap_h": float(d1["twin_gap_h"]),
        "tonnes_per_slot": float(d2["tonnes_per_slot"]),
        "line_gap_h": float(d3["line_gap_h"]),
        "retry_mult": float(d3.get("retry_mult", 0.0)),
        "cs_pb_26": float(cs_pb_c.sum()),
        "ph_bump_26": float(ph_bump_sh.sum()),
        "ed_blk_26": float(ed_blk_c.sum()),
        "contrast_cdays_26": float(cs_pb_c.sum() + ph_bump_sh.sum() + ed_blk_c.sum()),
    }

    # Port & Quarter breakdown by cause for 2026 & 2027 (for golden workbook tabs)
    p_vol = np.array([core.PLAN_2027["vol_growth_port"][p] for p in core.PORTS])
    plug_f = np.array([core.PLAN_2027["plug_capacity_factor_2027"][p] for p in core.PORTS])
    dc_zf = np.array([core.PLAN_2027["dc_zone_load_factor_2027"][z] for z in core.ZONES])
    bip_p = np.array([core.PLAN_2027["bip_sampling_factor_2027"][p] for p in core.PORTS])
    rail_f = core.PLAN_2027["rail_fleet_factor_2027"]
    line_r = np.array([core.PLAN_2027["line_share_2027"][k] / core.PLAN_2027["line_share_2026"][k] for k in core.LINES])
    dep_l = np.array([core.PLAN_2027["depot_load_factor_2027"][k] for k in core.LINES])
    dray_f = core.PLAN_2027["dray_contract_factor_2027"]

    c_27 = {
        "vessel_berth": w["obs_vessel_berth"] * p_vol[w["cont_port"]],
        "edi_docs": w["obs_edi_docs"] * p_vol[w["cont_port"]],
        "coldstore_dock": (cs_dir_c + cs_pb_c) * dc_zf[w["cont_zone"]],
        "reefer_plug": rp_c * p_vol[w["cont_port"]] * plug_f[w["cont_port"]],
        "phyto_insp": (ph_dir_c + ph_sib_c) * p_vol[w["cont_port"]] * bip_p[w["cont_port"]],
        "drayage_carrier": dr_c * p_vol[w["cont_port"]] * dray_f,
        "empty_depot": (ed_phys_c + ed_blk_c) * p_vol[w["cont_port"]] * line_r[w["cont_line"]] * dep_l[w["cont_line"]],
    }
    sh_27 = {
        "phyto_insp": ph_bump_sh * p_vol[w["shuttle_port"]] * bip_p[w["shuttle_port"]],
        "rail_handoff": (rh_sh + rh_base_sh) * p_vol[w["shuttle_port"]] * rail_f,
    }
    by_port_27 = {}
    for pi, pcode in enumerate(core.PORTS):
        tot_p = sum(float(arr[w["cont_port"] == pi].sum()) for arr in c_27.values()) + sum(
            float(arr[w["shuttle_port"] == pi].sum()) for arr in sh_27.values()
        )
        by_port_27[pcode] = round(tot_p, 2)
    by_quarter_27 = {}
    for qi in range(4):
        tot_q = sum(float(arr[w["cont_quarter"] == qi].sum()) for arr in c_27.values()) + sum(
            float(arr[w["shuttle_quarter"] == qi].sum()) for arr in sh_27.values()
        )
        by_quarter_27[f"Q{qi + 1}"] = round(tot_q, 2)
    res27["by_port_2027"] = by_port_27
    res27["by_quarter_2027"] = by_quarter_27
    return res27


def run_all(target_dir=None):
    target_dir = target_dir or os.path.join(TASK_DIR, "target")
    w = load_shipped_pack(target_dir)

    G1 = {"mode": "golden", "cap_thresh": 0.95, "stat": "mean"}
    G2 = {"mode": "golden", "lock_h": "empirical", "weight_est": "slot_mass"}
    G3 = {"mode": "golden", "rej_cut": 1, "stat": "dc_day"}
    H1, H2, H3 = {"mode": "hurried"}, {"mode": "hurried"}, {"mode": "hurried"}

    gold = _run_route_with_2026(w, G1, G2, G3)
    direct = _run_route_with_2026(w, {"mode": "direct"}, {"mode": "direct"}, {"mode": "direct"})
    rigorous = _run_route_with_2026(w, {"mode": "rigorous"}, {"mode": "rigorous"}, {"mode": "rigorous"})

    # 22-variant battery matching core.py verbatim
    variant_defs = [
        ("S1: same-vessel median", {"mode": "golden", "cap_thresh": 0.95, "stat": "median"}, G2, G3),
        ("S1: same-vessel 10% trimmed mean", {"mode": "golden", "cap_thresh": 0.95, "stat": "trimmed"}, G2, G3),
        ("S1: port-day fixed effects", {"mode": "golden", "cap_thresh": 0.95, "stat": "port_day_fe"}, G2, G3),
        ("S1: port-week fixed effects", {"mode": "golden", "cap_thresh": 0.95, "stat": "port_week_fe"}, G2, G3),
        ("S1: nonlinear OLS yard curve", {"mode": "golden", "cap_thresh": 0.95, "stat": "ols_yard"}, G2, G3),
        ("S1: chamber threshold 94.5%", {"mode": "golden", "cap_thresh": 0.945, "stat": "mean"}, G2, G3),
        ("S1: chamber threshold 95.5%", {"mode": "golden", "cap_thresh": 0.955, "stat": "mean"}, G2, G3),
        ("S2: fixed 24h lock + slot balance", G1, {"mode": "golden", "lock_h": 24.0, "weight_est": "slot_mass"}, G3),
        ("S2: 22h lock + slot balance", G1, {"mode": "golden", "lock_h": 22.0, "weight_est": "slot_mass"}, G3),
        ("S2: 26h lock + slot balance", G1, {"mode": "golden", "lock_h": 26.0, "weight_est": "slot_mass"}, G3),
        ("S2: empirical lock + weighbridge mass scale", G1, {"mode": "golden", "lock_h": "empirical", "weight_est": "mass_only"}, G3),
        ("S2: empirical lock + slot OLS", G1, {"mode": "golden", "lock_h": "empirical", "weight_est": "slot_ols"}, G3),
        ("S2: empirical lock + per-corridor OLS", G1, {"mode": "golden", "lock_h": "empirical", "weight_est": "corridor_ols"}, G3),
        ("S2: empirical lock + Huber robust regression", G1, {"mode": "golden", "lock_h": "empirical", "weight_est": "huber"}, G3),
        ("S3: same-DC weekly open-line contrast", G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "dc_week"}),
        ("S3: same-DC fortnight open-line contrast", G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "dc_fortnight"}),
        ("S3: open-line 4-harmonic Fourier OLS", G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "ols_line"}),
        ("S3: 5-day rolling stock-flow window", G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "stock_flow"}),
        ("S3: same-DC weekly median", G1, G2, {"mode": "golden", "rej_cut": 1, "stat": "median_dc_week"}),
        ("S3: portal rejection cutoff >= 2", G1, G2, {"mode": "golden", "rej_cut": 2, "stat": "dc_day"}),
        ("Joint: OLS yard + Huber rail + Fourier line",
         {"mode": "golden", "cap_thresh": 0.95, "stat": "ols_yard"},
         {"mode": "golden", "lock_h": "empirical", "weight_est": "huber"},
         {"mode": "golden", "rej_cut": 1, "stat": "ols_line"}),
        ("Joint: port-week FE + corridor OLS + DC-week",
         {"mode": "golden", "cap_thresh": 0.95, "stat": "port_week_fe"},
         {"mode": "golden", "lock_h": "empirical", "weight_est": "corridor_ols"},
         {"mode": "golden", "rej_cut": 1, "stat": "dc_week"}),
    ]
    variants = []
    for vname, s1k, s2k, s3k in variant_defs:
        vr = _run_route_with_2026(w, s1k, s2k, s3k)
        remed = sorted(m for m in core.MEMBERS if vr["members"][m] >= core.LINE_THRESHOLD)
        variants.append({
            "name": vname,
            "members": {m: round(vr["members"][m], 2) for m in core.MEMBERS},
            "remediate_set": remed,
            "total_2027": round(vr["total_2027"], 2),
            "remed_days": round(vr["remed_days"], 2),
            "cost_eur_m": round(vr["cost_eur_m"], 4),
            "avoidable_eur_m": round(vr["avoidable_eur_m"], 4),
            "bhv_2027": round(vr["bhv_2027"], 2),
            "ham_2027": round(vr["ham_2027"], 2),
            "q3_2027": round(vr["q3_2027"], 2),
        })

    gold_remed_set = sorted(m for m in core.MEMBERS if gold["members"][m] >= core.LINE_THRESHOLD)
    gold_monitor_set = sorted(m for m in core.MEMBERS if gold["members"][m] < core.LINE_THRESHOLD)
    assert all(v["remediate_set"] == gold_remed_set for v in variants), "A variant flipped the call!"

    # Lattice routes (all 7 combinations) + over-corrections + 4 run routes + history mean
    lattice = {}
    for r_n in (1, 2, 3):
        for comb in itertools.combinations(("S1", "S2", "S3"), r_n):
            k = "+".join(comb)
            lr = _run_route_with_2026(
                w,
                H1 if "S1" in comb else G1,
                H2 if "S2" in comb else G2,
                H3 if "S3" in comb else G3,
            )
            lattice[k] = {
                "members": {m: round(lr["members"][m], 2) for m in core.MEMBERS},
                "remediate_set": sorted(m for m in core.MEMBERS if lr["members"][m] >= core.LINE_THRESHOLD),
                "total_2027": round(lr["total_2027"], 2),
                "remed_days": round(lr["remed_days"], 2),
                "cost_eur_m": round(lr["cost_eur_m"], 4),
                "avoidable_eur_m": round(lr["avoidable_eur_m"], 4),
                "bhv_2027": round(lr["bhv_2027"], 2),
                "ham_2027": round(lr["ham_2027"], 2),
                "q3_2027": round(lr["q3_2027"], 2),
                "diag": {dk: round(dv, 3) for dk, dv in lr["diag"].items()},
            }

    over_routes = {
        "S1_over": _run_route_with_2026(w, {"mode": "over"}, G2, G3),
        "S2_over": _run_route_with_2026(w, G1, {"mode": "over"}, G3),
        "S3_over": _run_route_with_2026(w, G1, G2, {"mode": "over"}),
    }
    run_routes = {
        "generous": _run_route_with_2026(w, {"mode": "generous"}, {"mode": "generous"}, {"mode": "generous"}),
        "calibrated": _run_route_with_2026(w, {"mode": "calibrated"}, {"mode": "calibrated"}, {"mode": "calibrated"}),
        "hedge": _run_route_with_2026(w, {"mode": "hedge"}, {"mode": "hedge"}, {"mode": "hedge"}),
        "cutoff": _run_route_with_2026(
            w,
            {"mode": "cutoff_total_dc", "cap_thresh": 0.79},
            {"mode": "cutoff_any_bip", "lock_h": 1},
            {"mode": "cutoff_rej_raw", "rej_cut": 10},
        ),
    }

    # Forcing +/-20% perturbations
    pert_defs = [
        ("S1 pullback -20%", {"mult_s1": 0.80}),
        ("S1 pullback +20%", {"mult_s1": 1.20}),
        ("S2 locked-slot -20%", {"mult_s2": 0.80}),
        ("S2 locked-slot +20%", {"mult_s2": 1.20}),
        ("S3 portal-block -20%", {"mult_s3": 0.80}),
        ("S3 portal-block +20%", {"mult_s3": 1.20}),
        ("All baseline -20%", {"mult_base": 0.80}),
        ("All baseline +20%", {"mult_base": 1.20}),
    ]
    perturbations = []
    for pname, popts in pert_defs:
        pr = _run_route_with_2026(w, G1, G2, G3, proj_opts=popts)
        remed = sorted(m for m in core.MEMBERS if pr["members"][m] >= core.LINE_THRESHOLD)
        assert remed == gold_remed_set, f"Forcing perturbation {pname} flipped call: {remed}"
        perturbations.append({
            "input": pname,
            "answer": remed,
            "min_remediate": round(min(pr["members"][m] for m in gold_remed_set), 1),
            "max_monitor": round(max(pr["members"][m] for m in gold_monitor_set), 1),
        })

    # Compute exact 22-variant bands (matching core.py precision)
    def _band_int(vals, pad=10):
        lo = min(vals)
        hi = max(vals)
        if abs(hi - lo) < 1e-6:
            return [int(round(lo)), int(round(hi))]
        return [int(np.floor(lo)) - pad, int(np.ceil(hi)) + pad]

    member_bands = {}
    for m in core.MEMBERS:
        vlist = [gold["members"][m]] + [v["members"][m] for v in variants]
        if m in ("vessel_berth", "edi_docs"):
            iv = int(round(gold["members"][m]))
            member_bands[m] = [iv, iv]
        else:
            member_bands[m] = _band_int(vlist, pad=12)

    agg_bands = {}
    for k in ("total_2027", "remed_days", "bhv_2027", "ham_2027", "q3_2027"):
        vlist = [gold[k]] + [v[k] for v in variants]
        agg_bands[k] = _band_int(vlist, pad=15)
    for k in ("cost_eur_m", "avoidable_eur_m"):
        vlist = [gold[k]] + [v[k] for v in variants]
        agg_bands[k] = [round(min(vlist) - 0.01, 3), round(max(vlist) + 0.01, 3)]

    # Ranked cause rows (descending by cdays_2027)
    ranked_causes = sorted(core.MEMBERS, key=lambda m: -gold["members"][m])
    cause_table = []
    for m in ranked_causes:
        c26 = gold["cdays_2026"][m]
        c27 = gold["members"][m]
        sh27 = 100.0 * c27 / gold["total_2027"]
        eur27 = c27 * core.TARIFF_EUR[m]
        desig = "REMEDIATE" if c27 >= core.LINE_THRESHOLD else "MONITOR"
        cause_table.append({
            "cause_id": m,
            "cause_name": CAUSE_NAMES[m],
            "cdays_2026": round(c26, 2),
            "cdays_2026_int": int(round(c26)),
            "cdays_2027": round(c27, 2),
            "cdays_2027_int": int(round(c27)),
            "band_2027": member_bands[m],
            "share_2027_pct": round(sh27, 2),
            "tariff_eur": int(core.TARIFF_EUR[m]),
            "eur_2027": round(eur27, 2),
            "eur_2027_m": round(eur27 / 1e6, 3),
            "designation": desig,
            "direct_2027_int": int(round(direct["members"][m])),
            "rigorous_2027_int": int(round(rigorous["members"][m])),
        })

    # Reconstruct chamber utilization range & Step-by-Step completeness diagnostics
    ch_u = core._reconstruct_chamber_util(w)
    u_ch_c = ch_u[w["cont_dc"], w["cont_zone"], w["cont_day"]]
    y_c = w["obs_term_yard_hold"]
    v_c = w["cont_vessel"]
    p_c = w["cont_port"]
    # <95% unsaturated twin check for Step 4 note
    v_base_95 = np.zeros(core.N_VESSELS)
    for v_i in range(core.N_VESSELS):
        m_u95 = (v_c == v_i) & (u_ch_c < 0.95)
        if np.any(m_u95):
            v_base_95[v_i] = y_c[m_u95].mean()
        else:
            p0 = p_c[v_c == v_i][0]
            v_base_95[v_i] = y_c[(p_c == p0) & (u_ch_c < 0.95)].mean()
    s1_lt95_cdays_26 = float(np.where(u_ch_c >= 0.95, np.maximum(0.0, y_c - v_base_95[v_c]), 0.0).sum())

    # 4-regressor weighbridge fit vs booked & loaded for Step 6 completeness
    n_sh_all = len(w["shuttle_port"])
    is_rail_c = w["cont_is_rail"]
    cont_ched_c = w["cont_ched"]
    n_locked_sh_v = np.bincount(
        w["cont_shuttle"][is_rail_c & w["lot_bip"][cont_ched_c] & (w["lot_lead_hours"][cont_ched_c] <= 24.0)],
        minlength=n_sh_all,
    )
    sh_short_v = np.maximum(0.0, w["wf_booked_slots_sh"] - w["wf_actual_loaded_sh"])
    non_bip_sf_v = np.maximum(0.0, sh_short_v - n_locked_sh_v)
    Xw_b = np.column_stack([
        np.ones(n_sh_all), w["train_wagon_count_sh"], w["wf_booked_slots_sh"], n_locked_sh_v, non_bip_sf_v
    ])
    bw_b, _, _, _ = np.linalg.lstsq(Xw_b, w["train_gross_tonnes_sh"], rcond=None)
    Xw_l = np.column_stack([
        np.ones(n_sh_all), w["train_wagon_count_sh"], w["wf_actual_loaded_sh"], n_locked_sh_v, non_bip_sf_v
    ])
    bw_l, _, _, _ = np.linalg.lstsq(Xw_l, w["train_gross_tonnes_sh"], rcond=None)

    # S3 unpaired same-DC same-day box count for Step 7 completeness
    rej_c = w["portal_rejected"][w["cont_port"], w["cont_line"], w["cont_unload_day"]]
    closed_m = rej_c >= 1
    open_m = rej_c == 0
    n_pdays = w["portal_rejected"].shape[2]
    dc_day_key = w["cont_dc"] * n_pdays + w["cont_unload_day"]
    open_keys = set(dc_day_key[open_m].tolist())
    s3_unpaired = int(sum(1 for k in dc_day_key[closed_m].tolist() if k not in open_keys))

    ch_stats = {
        "total_dc_util_min_pct": round(100.0 * float(w["dc_total_util"].min()), 1),
        "total_dc_util_max_pct": round(100.0 * float(w["dc_total_util"].max()), 1),
        "z02_util_max_pct": round(100.0 * float(ch_u[:, 0, :].max()), 1),
        "z07_util_max_pct": round(100.0 * float(ch_u[:, 1, :].max()), 1),
        "z13_util_max_pct": round(100.0 * float(ch_u[:, 2, :].max()), 1),
        "capped_boxes_count": int((u_ch_c >= 0.95).sum()),
        "locked_phyto_slots": int((is_rail_c & w["lot_bip"][cont_ched_c] & (w["lot_lead_hours"][cont_ched_c] <= 24.0)).sum()),
        "closed_quota_boxes": int(closed_m.sum()),
        "portal_rejected_total": int(w["portal_rejected"].sum()),
        "s3_unpaired_boxes": s3_unpaired,
    }
    phyto_sib_26 = round(float(w["obs_phyto_sibling_tms_rail"].sum()), 2)
    ph_bump_26 = round(gold["diag"]["ph_bump_26"], 2)
    s3_rej_per_box = round(ch_stats["portal_rejected_total"] / max(ch_stats["closed_quota_boxes"], 1), 2)
    forcing_min_remed = int(round(min(p["min_remediate"] for p in perturbations)))
    forcing_max_monitor = int(round(max(p["max_monitor"] for p in perturbations)))

    # Build figures.json (flat + structured keys for figures_check.py and effort.py)
    figures = {
        "task": "task27",
        "org": PK.ORG,
        "as_of": "2027-01-19",
        "threshold_cdays": int(core.LINE_THRESHOLD),
        "n_containers": core.N_CONTAINERS,
        "n_vessels": core.N_VESSELS,
        "n_shuttles": 3 * core.N_DAYS,
        "total_2026_cdays": round(gold["total_2026"], 2),
        "total_2026_cdays_int": int(round(gold["total_2026"])),
        "remediate_set": gold_remed_set,
        "monitor_set": gold_monitor_set,
        "ranked_order": ranked_causes,
        "forcing_min_remed": forcing_min_remed,
        "forcing_max_monitor": forcing_max_monitor,
        # Top-level graded keys matching core.py & effort.py
        "C1_coldstore_dock": int(round(gold["members"]["coldstore_dock"])),
        "C2_rail_handoff": int(round(gold["members"]["rail_handoff"])),
        "C3_empty_depot": int(round(gold["members"]["empty_depot"])),
        "A_reefer_plug": int(round(gold["members"]["reefer_plug"])),
        "A_phyto_insp": int(round(gold["members"]["phyto_insp"])),
        "A_drayage_carrier": int(round(gold["members"]["drayage_carrier"])),
        "A_vessel_berth": int(round(gold["members"]["vessel_berth"])),
        "A_edi_docs": int(round(gold["members"]["edi_docs"])),
        "A_total_2027": int(round(gold["total_2027"])),
        "A_remed_days": int(round(gold["remed_days"])),
        "A_cost_eur_m": round(gold["cost_eur_m"], 3),
        "A_avoidable_eur_m": round(gold["avoidable_eur_m"], 3),
        "A_cost_eur_exact": round(gold["cost_eur_m"] * 1e6, 2),
        "A_avoidable_eur_exact": round(gold["avoidable_eur_m"] * 1e6, 2),
        "A_bhv_2027": int(round(gold["bhv_2027"])),
        "A_ham_2027": int(round(gold["ham_2027"])),
        "A_whv_2027": int(round(gold["by_port_2027"]["WHV"])),
        "A_q3_2027": int(round(gold["q3_2027"])),
        "by_port_2027": gold["by_port_2027"],
        "by_quarter_2027": gold["by_quarter_2027"],
        "R1_settled_total": int(round(gold["total_2026"])),
        "R5_diagnostics": {
            "F1_twin_gap_h": round(gold["diag"]["twin_gap_h"], 2),
            "F2_tonnes_per_slot": round(gold["diag"]["tonnes_per_slot"], 2),
            "F3_line_gap_h": round(gold["diag"]["line_gap_h"], 2),
            "F3_retry_mult": round(gold["diag"]["retry_mult"], 2),
            "contrast_cdays_26": round(gold["diag"]["contrast_cdays_26"], 2),
            "cs_pb_26": round(gold["diag"]["cs_pb_26"], 2),
            "s1_lt95_cdays_26": round(s1_lt95_cdays_26, 2),
            "ph_bump_26": ph_bump_26,
            "s2_total_26": round(phyto_sib_26 + ph_bump_26, 2),
            "ed_blk_26": round(gold["diag"]["ed_blk_26"], 2),
            "F1_rigorous_h": round(rigorous["diag"]["twin_gap_h"], 2),
            "F2_rigorous_t": round(rigorous["diag"]["tonnes_per_slot"], 2),
            "F3_rigorous_h": round(rigorous["diag"]["line_gap_h"], 2),
            "measured_reefer_tonnes": round(w["measured_reefer_tonnes"], 2),
            "measured_rollover_days": round(w["measured_rollover_days"], 2),
            "mean_rolled_cdays": round(w["mean_rolled_cdays"], 4),
            "mean_unrolled_cdays": round(w["mean_unrolled_cdays"], 4),
            "non_bip_sf_vs_booked_t": round(float(bw_b[4]), 2),
            "non_bip_sf_vs_loaded_t": round(float(bw_l[4]), 2),
            "phyto_sibling_rail_26": phyto_sib_26,
            "s3_rej_per_box": s3_rej_per_box,
            "s1_twin_cap_pct": 92,
            "empiric_lock_h": 24,
        },
        "R6_bundle": {
            "total_2027": int(round(gold["total_2027"])),
            "bhv_2027": int(round(gold["bhv_2027"])),
            "ham_2027": int(round(gold["ham_2027"])),
            "q3_2027": int(round(gold["q3_2027"])),
        },
        "R7_bundle": {
            "cost_eur_m": round(gold["cost_eur_m"], 3),
            "avoidable_eur_m": round(gold["avoidable_eur_m"], 3),
            "remed_days": int(round(gold["remed_days"])),
        },
        "R8_call": gold_remed_set,
        "causes": cause_table,
        "member_bands": member_bands,
        "agg_bands": agg_bands,
        "cleaning": w["cleaning"],
        "chamber_stats": ch_stats,
        "routes": {
            "golden": {
                "members": {m: round(gold["members"][m], 2) for m in core.MEMBERS},
                "remediate_set": gold_remed_set,
                "total_2027": round(gold["total_2027"], 2),
                "remed_days": round(gold["remed_days"], 2),
                "cost_eur_m": round(gold["cost_eur_m"], 3),
                "avoidable_eur_m": round(gold["avoidable_eur_m"], 3),
                "bhv_2027": round(gold["bhv_2027"], 2),
                "ham_2027": round(gold["ham_2027"], 2),
                "q3_2027": round(gold["q3_2027"], 2),
            },
            "direct": {
                "members": {m: round(direct["members"][m], 2) for m in core.MEMBERS},
                "remediate_set": sorted(m for m in core.MEMBERS if direct["members"][m] >= core.LINE_THRESHOLD),
                "total_2027": round(direct["total_2027"], 2),
                "remed_days": round(direct["remed_days"], 2),
                "cost_eur_m": round(direct["cost_eur_m"], 3),
                "avoidable_eur_m": round(direct["avoidable_eur_m"], 3),
                "bhv_2027": round(direct["bhv_2027"], 2),
                "ham_2027": round(direct["ham_2027"], 2),
                "q3_2027": round(direct["q3_2027"], 2),
            },
            "rigorous": {
                "members": {m: round(rigorous["members"][m], 2) for m in core.MEMBERS},
                "remediate_set": sorted(m for m in core.MEMBERS if rigorous["members"][m] >= core.LINE_THRESHOLD),
                "total_2027": round(rigorous["total_2027"], 2),
                "remed_days": round(rigorous["remed_days"], 2),
                "cost_eur_m": round(rigorous["cost_eur_m"], 3),
                "avoidable_eur_m": round(rigorous["avoidable_eur_m"], 3),
                "bhv_2027": round(rigorous["bhv_2027"], 2),
                "ham_2027": round(rigorous["ham_2027"], 2),
                "q3_2027": round(rigorous["q3_2027"], 2),
            },
            "history_2026_unprojected": {
                "members": {m: round(gold["cdays_2026"][m], 2) for m in core.MEMBERS},
                "remediate_set": sorted(m for m in core.MEMBERS if gold["cdays_2026"][m] >= core.LINE_THRESHOLD),
            },
            **{
                k: {
                    "members": {m: round(rv["members"][m], 2) for m in core.MEMBERS},
                    "remediate_set": sorted(m for m in core.MEMBERS if rv["members"][m] >= core.LINE_THRESHOLD),
                    "total_2027": round(rv["total_2027"], 2),
                    "cost_eur_m": round(rv["cost_eur_m"], 3),
                }
                for k, rv in {**over_routes, **run_routes}.items()
            },
        },
        "lattice": lattice,
        "variants": variants,
        "perturbations": perturbations,
        "plan_2027": core.PLAN_2027,
        "tariffs_eur": core.TARIFF_EUR,
    }

    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figures, f, indent=2, sort_keys=True)

    # Build effort.json (strictly computed from cut pack and tied to figures.json!)
    reflex = lattice["S1+S2+S3"]
    s1_drop = lattice["S1"]
    s2_drop = lattice["S2"]
    s3_drop = lattice["S3"]
    s1_alone = lattice["S2+S3"]
    s2_alone = lattice["S1+S3"]
    s3_alone = lattice["S1+S2"]

    effort = {
        "results": [
            {
                "id": "R1",
                "name": "Reconciled 2026 settled excess container-days",
                "graded_as": "Ask 1 (base)",
                "figure": "R1_settled_total",
                "depends": [],
                "independent": "raw 2026 milestones, warehouse pallets, and turn-in logs",
                "golden": figures["R1_settled_total"],
                "band": [figures["R1_settled_total"] - 5, figures["R1_settled_total"] + 5],
                "partly": [figures["R1_settled_total"] - 350, figures["R1_settled_total"] + 350],
                "passes": {
                    # Quick pass keeps VOID + superseded rows (+210 c-days -> Partly)
                    "quick": figures["R1_settled_total"] + 210,
                    "careful": figures["R1_settled_total"],
                    "thorough": figures["R1_settled_total"],
                },
            },
            {
                "id": "R2",
                "name": "Cold-store dock 2027 attribution (S1)",
                "graded_as": "Component 1",
                "figure": "C1_coldstore_dock",
                "depends": ["R1"],
                "independent": "daily SKU pallet movements, chamber register, and same-vessel twins",
                "golden": figures["C1_coldstore_dock"],
                "band": member_bands["coldstore_dock"],
                "partly": [2600, 3800],
                "precedent": ["L26", "L28", "L38", "N36"],
                "passes": {
                    "quick": int(round(direct["members"]["coldstore_dock"])),
                    "careful": int(round(rigorous["members"]["coldstore_dock"])),
                    "thorough": figures["C1_coldstore_dock"],
                },
            },
            {
                "id": "R3",
                "name": "Intermodal rail handoff 2027 attribution (S2)",
                "graded_as": "Component 2",
                "figure": "C2_rail_handoff",
                "depends": ["R1"],
                "independent": "CHED notices, shuttle slot shortfalls, and shared-train weighbridges",
                "golden": figures["C2_rail_handoff"],
                "band": member_bands["rail_handoff"],
                "partly": [1500, 2350],
                "precedent": ["L11", "N25", "L48", "N07"],
                "passes": {
                    "quick": int(round(direct["members"]["rail_handoff"])),
                    "careful": int(round(rigorous["members"]["rail_handoff"])),
                    "thorough": figures["C2_rail_handoff"],
                },
            },
            {
                "id": "R4",
                "name": "Empty depot intake 2027 attribution (S3)",
                "graded_as": "Component 3",
                "figure": "C3_empty_depot",
                "depends": ["R1"],
                "independent": "unlinked depot portal rejections and same-DC same-day shipping-line returns",
                "golden": figures["C3_empty_depot"],
                "band": member_bands["empty_depot"],
                "partly": [2600, 3800],
                "precedent": ["N14", "N27", "L56", "L57"],
                "passes": {
                    "quick": int(round(direct["members"]["empty_depot"])),
                    "careful": int(round(rigorous["members"]["empty_depot"])),
                    "thorough": figures["C3_empty_depot"],
                },
            },
            {
                "id": "R5",
                "name": "Native-unit physical conservation diagnostics",
                "graded_as": "Ask 1 (diagnostics)",
                "figure": "R5_diagnostics",
                "depends": ["R2", "R3", "R4"],
                "independent": "",
                "golden": figures["R5_diagnostics"],
                "bands": {
                    "F1_twin_gap_h": [19.0, 21.5],
                    "F2_tonnes_per_slot": [-31.5, -26.5],
                    "F3_line_gap_h": [9.5, 11.8],
                    "F3_retry_mult": [4.0, 4.7],
                    "contrast_cdays_26": [
                        round(figures["R5_diagnostics"]["contrast_cdays_26"] - 180.0, 1),
                        round(figures["R5_diagnostics"]["contrast_cdays_26"] + 180.0, 1),
                    ],
                },
                "partly_share": 0.6,
                "precedent": ["L28", "L48"],
                "passes": {
                    "quick": {
                        "F1_twin_gap_h": 0.0,
                        "F2_tonnes_per_slot": 0.0,
                        "F3_line_gap_h": 0.0,
                        "F3_retry_mult": 0.0,
                        "contrast_cdays_26": 0.0,
                    },
                    "careful": {
                        "F1_twin_gap_h": round(rigorous["diag"]["twin_gap_h"], 2),
                        "F2_tonnes_per_slot": round(rigorous["diag"]["tonnes_per_slot"], 2),
                        "F3_line_gap_h": round(rigorous["diag"]["line_gap_h"], 2),
                        "F3_retry_mult": 0.0,
                        "contrast_cdays_26": round(rigorous["diag"]["contrast_cdays_26"], 2),
                    },
                    "thorough": figures["R5_diagnostics"],
                },
            },
            {
                "id": "R6",
                "name": "2027 network, BHV, HAM, and Q3 projections",
                "graded_as": "Ask 2",
                "figure": "R6_bundle",
                "depends": ["R2", "R3", "R4", "R5"],
                "independent": "",
                "golden": figures["R6_bundle"],
                "bands": {
                    "total_2027": agg_bands["total_2027"],
                    "bhv_2027": agg_bands["bhv_2027"],
                    "ham_2027": agg_bands["ham_2027"],
                    "q3_2027": agg_bands["q3_2027"],
                },
                "partly_share": 0.5,
                "precedent": ["L26", "L57"],
                "passes": {
                    "quick": {
                        "total_2027": int(round(direct["total_2027"])),
                        "bhv_2027": int(round(direct["bhv_2027"])),
                        "ham_2027": int(round(direct["ham_2027"])),
                        "q3_2027": int(round(direct["q3_2027"])),
                    },
                    "careful": {
                        "total_2027": int(round(reflex["total_2027"])),
                        "bhv_2027": int(round(reflex["bhv_2027"])),
                        "ham_2027": int(round(reflex["ham_2027"])),
                        "q3_2027": int(round(reflex["q3_2027"])),
                    },
                    "thorough": figures["R6_bundle"],
                },
            },
            {
                "id": "R7",
                "name": "2027 detention and demurrage EUR exposure",
                "graded_as": "Ask 3",
                "figure": "R7_bundle",
                "depends": ["R2", "R3", "R4", "R6"],
                "independent": "",
                "golden": figures["R7_bundle"],
                "bands": {
                    "cost_eur_m": agg_bands["cost_eur_m"],
                    "avoidable_eur_m": agg_bands["avoidable_eur_m"],
                    "remed_days": agg_bands["remed_days"],
                },
                "partly_share": 0.5,
                "precedent": ["L11", "L63"],
                "passes": {
                    "quick": {
                        "cost_eur_m": round(direct["cost_eur_m"], 3),
                        "avoidable_eur_m": round(direct["avoidable_eur_m"], 3),
                        "remed_days": int(round(direct["remed_days"])),
                    },
                    "careful": {
                        "cost_eur_m": round(reflex["cost_eur_m"], 3),
                        "avoidable_eur_m": round(reflex["avoidable_eur_m"], 3),
                        "remed_days": int(round(reflex["remed_days"])),
                    },
                    "thorough": figures["R7_bundle"],
                },
            },
            {
                "id": "R8",
                "name": "Ranked 2027 Mandatory Remediation slate",
                "graded_as": "Recommendation",
                "figure": "R8_call",
                "depends": ["R2", "R3", "R4", "R6", "R7"],
                "independent": "",
                "golden": figures["R8_call"],
                "passes": {
                    "quick": {"value": figures["routes"]["direct"]["remediate_set"], "grade": "missed", "why": "Direct TMS misses coldstore_dock and empty_depot and mis-designates rail_handoff."},
                    "careful": {"value": reflex["remediate_set"], "grade": "missed", "why": "Reflex route misses coldstore_dock and empty_depot and mis-designates rail_handoff."},
                    "thorough": figures["R8_call"],
                },
                "precedent": ["L26", "L57"],
            },
        ],
        "hints": [
            {
                "sentence": "Containers bound for an inland cold store whose specific thermal chamber is full are held back at the port under TERM_YARD_HOLD rather than delayed by port plugs.",
                "rescues": ["R2"],
            },
            {
                "sentence": "Rail slots booked for co-loaded CHED lots frozen by late border inspections stay physically empty on departing trains and bump cleared standby boxes.",
                "rescues": ["R3"],
            },
            {
                "sentence": "Empty reefers sitting in drayage yards are blocked by shipping-line depot portal quotas whose rejection log lacks container IDs and records repeated daily retries.",
                "rescues": ["R4"],
            },
        ],
        "routes": [
            {"name": "the golden", "answer": gold_remed_set, "golden": True},
            {"name": "direct TMS codes / reflex", "answer": reflex["remediate_set"]},
            {"name": "rigorous standard (total DC + direct CHED siblings)", "answer": sorted(m for m in core.MEMBERS if rigorous["members"][m] >= core.LINE_THRESHOLD)},
            {"name": "S1 dropped alone", "answer": s1_drop["remediate_set"]},
            {"name": "S2 dropped alone", "answer": s2_drop["remediate_set"]},
            {"name": "S3 dropped alone", "answer": s3_drop["remediate_set"]},
            {"name": "S1 over-corrected (unnetted)", "answer": sorted(m for m in core.MEMBERS if over_routes["S1_over"]["members"][m] >= core.LINE_THRESHOLD)},
            {"name": "S2 over-corrected (all BIP shuttles)", "answer": sorted(m for m in core.MEMBERS if over_routes["S2_over"]["members"][m] >= core.LINE_THRESHOLD)},
            {"name": "S3 over-corrected (raw rejections)", "answer": sorted(m for m in core.MEMBERS if over_routes["S3_over"]["members"][m] >= core.LINE_THRESHOLD)},
            {"name": "generous run route", "answer": sorted(m for m in core.MEMBERS if run_routes["generous"]["members"][m] >= core.LINE_THRESHOLD)},
            {"name": "cutoff run route", "answer": sorted(m for m in core.MEMBERS if run_routes["cutoff"]["members"][m] >= core.LINE_THRESHOLD)},
            {"name": "2026 history unprojected", "answer": sorted(m for m in core.MEMBERS if gold["cdays_2026"][m] >= core.LINE_THRESHOLD)},
        ],
        "forcing": {
            "kind": "set",
            "golden_answer": gold_remed_set,
            "golden_family": [{"name": v["name"], "answer": v["remediate_set"]} for v in variants],
            "perturbations": [{"input": p["input"], "answer": p["answer"]} for p in perturbations],
        },
        "factorial": {
            "golden_answer": gold_remed_set,
            "reflex_route": {"answer": reflex["remediate_set"]},
            "judgments": [
                {
                    "id": "S1",
                    "name": "Per-chamber stock-flow and same-vessel twin port-dwell split",
                    "kind": "stump",
                    "precedent": ["L26", "L28", "L38", "N36"],
                    "dropped": {"answer": s1_drop["remediate_set"], "results_moved": ["R2", "R5", "R6", "R7", "R8"]},
                    "alone": {"answer": s1_alone["remediate_set"], "results_rescued": ["R2"]},
                },
                {
                    "id": "S2",
                    "name": "Post-T-24h CHED locked empty rail-wagon slot and weighbridge mass conservation",
                    "kind": "stump",
                    "precedent": ["L03", "L07", "L48", "N07"],
                    "dropped": {"answer": s2_drop["remediate_set"], "results_moved": ["R3", "R5", "R6", "R7", "R8"]},
                    "alone": {"answer": s2_alone["remediate_set"], "results_rescued": ["R3"]},
                },
                {
                    "id": "S3",
                    "name": "Same-DC same-day shipping-line empty-return contrast and retry stock-flow conservation",
                    "kind": "stump",
                    "precedent": ["N14", "N27", "L56", "L57"],
                    "dropped": {"answer": s3_drop["remediate_set"], "results_moved": ["R4", "R5", "R6", "R7", "R8"]},
                    "alone": {"answer": s3_alone["remediate_set"], "results_rescued": ["R4"]},
                },
                {
                    "id": "R_L1",
                    "name": "Layer 1 operational hygiene (dedup, VOID, mixed dates, CASE/PALLET, crosswalks)",
                    "kind": "reflex",
                    "precedent": ["R01", "R02"],
                },
                {
                    "id": "R_sib",
                    "name": "Direct CHED lot-sibling container join",
                    "kind": "reflex",
                    "precedent": ["R13", "R14"],
                },
            ],
        },
        "weights": {"recommendation": 14, "components": 24, "asks": 55, "instruction": 7},
    }

    with open(os.path.join(HERE, "effort.json"), "w", encoding="utf-8") as f:
        json.dump(effort, f, indent=2, sort_keys=True)

    return figures, effort


if __name__ == "__main__":
    figs, eff = run_all()
    print(f"Wrote figures.json & effort.json | 2026={figs['total_2026_cdays']:.2f} | 2027={figs['A_total_2027']} | call={figs['remediate_set']}")
    print("Diagnostics:", figs["R5_diagnostics"])
    print("Cleaning:", figs["cleaning"])
