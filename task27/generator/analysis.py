"""Independent end-to-end analysis reading ONLY the shipped files under task27/target/ (Arch 2, v4-hardened).

Performs complete Layer 1 data cleaning from scratch (VOID filtering, extract_version deduplication,
mixed DD.MM.YYYY / YYYY-MM-DD date parsing, CASE-to-PALLET conversion, legacy store/carrier
crosswalk resolution, UTC vs Europe/Berlin CET/CEST timestamp alignment), executes the three
open-book econometric separation models (S1 asymmetric convex chamber hysteresis, S2 joint
terminal-varying BIP lock vs Nordbahn short-consist/loco rail rollover model, S3 conserved
shipping-line empty-depot backlog queue model), runs all 21 defensible variants, all 8 +/-15%
forcing perturbations, all 7 lattice drops, and all run routes & shortcuts, and emits:
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
CORR_IDX = {c: i for i, c in enumerate(core.CORRIDORS)}


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
    """Read, clean, verify, and assemble all operational arrays solely from shipped files in target_dir."""
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

    # 2. Budgets & 2027 Operating Plan Parameters
    corr_budget = {}
    corr_capture = {}
    corr_dist = np.zeros(6, dtype=float)
    vol_growth = {}
    plug_cap_27 = {}
    rail_fleet_27 = {}
    dray_cont_27 = {}
    tariffs = {}
    with open(os.path.join(target_dir, F["budgets_2027"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cname = row["corridor_id"]
            p_name = row["port_id"]
            c_idx = CORR_IDX[cname]
            corr_budget[cname] = float(row["remediation_budget_eur"])
            corr_capture[cname] = float(row["capture_rate_2027"])
            corr_dist[c_idx] = float(row["haul_distance_km"])
            vol_growth[cname] = float(row["vol_growth_2027"])
            plug_cap_27[p_name] = float(row["plug_capacity_factor_2027"])
            rail_fleet_27[p_name] = float(row["rail_fleet_factor_2027"])
            dray_cont_27[p_name] = float(row["dray_contract_factor_2027"])
            tariffs["reefer_plug"] = float(row["tariff_reefer_plug_eur"])
            tariffs["rail_handoff"] = float(row["tariff_rail_handoff_eur"])
            tariffs["drayage_carrier"] = float(row["tariff_drayage_carrier_eur"])

    # 3. SKU Thermal Catalog
    sku_zone, sku_cpp = {}, {}
    with open(os.path.join(target_dir, F["skus"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sku_zone[row["sku_id"]] = ZONE_IDX[row["thermal_zone"]]
            sku_cpp[row["sku_id"]] = int(row["cases_per_pallet"])

    # 4. DC Chamber Register
    dc_caps = np.zeros((4, 3), dtype=float)
    chamber_opening = np.zeros((4, 3), dtype=int)
    with open(os.path.join(target_dir, F["chambers"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d = DC_IDX[row["dc_id"]]
            z = ZONE_IDX[row["thermal_zone"]]
            dc_caps[d, z] = float(row["pallet_bay_capacity"])
            chamber_opening[d, z] = int(row["opening_pallets_2026_01_01"])
    dc_total_cap = dc_caps.sum(axis=1)

    # 5. Aggregate DC Daily Inventory
    dc_total_stock = np.zeros((4, core.N_DAYS), dtype=int)
    dc_total_util = np.zeros((4, core.N_DAYS), dtype=float)
    with open(os.path.join(target_dir, F["dc_inv"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (_parse_date(row["date_iso"]) - BASE_DATE).days
            d = DC_IDX[row["dc_id"]]
            dc_total_stock[d, t] = int(row["total_pallets_on_hand"])
            dc_total_util[d, t] = dc_total_stock[d, t] / dc_total_cap[d]

    # 6. Terminal Yard Daily
    port_yard_util = np.zeros((3, core.N_DAYS), dtype=float)
    with open(os.path.join(target_dir, F["port_yard"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (_parse_date(row["date_iso"]) - BASE_DATE).days
            p = PORT_IDX[row["port_id"]]
            port_yard_util[p, t] = float(row["reefer_yard_util_pct"]) / 100.0

    # 7. Warehouse Pallet Movements (dedup extract_version, parse mixed dates, CASE->PALLET, store crosswalk)
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
        sid = row["sku_id"]
        z = sku_zone[sid]
        qty = int(row["quantity"])
        if row["unit"] == "CASE":
            mv_case_rows += 1
            cpp = sku_cpp[sid]
            assert qty % cpp == 0
            pallets = qty // cpp
        else:
            pallets = qty
        sc = row["store_code"]
        if sc in store_map:
            mv_legacy_stores += 1
        if row["direction"] == "IN":
            pallet_in[d, z, t] += pallets
        else:
            pallet_out[d, z, t] += pallets

    # Verify exact chamber stock-flow conservation against dc_total_stock
    ch_stock = np.zeros((4, 3, core.N_DAYS), dtype=int)
    for d in range(4):
        for z in range(3):
            ch_stock[d, z] = chamber_opening[d, z] + np.cumsum(pallet_in[d, z] - pallet_out[d, z])
    assert np.array_equal(ch_stock.sum(axis=1), dc_total_stock), "Chamber stock conservation failed!"
    cleaning["pallets_raw_rows"] = mv_raw
    cleaning["pallets_dedup_rows"] = len(latest_mv)
    cleaning["pallets_superseded_removed"] = mv_raw - len(latest_mv)
    cleaning["pallets_de_date_rows"] = mv_de_dates
    cleaning["pallets_case_converted_rows"] = mv_case_rows
    cleaning["pallets_legacy_store_mapped"] = mv_legacy_stores

    # 8. Rail Shuttle Departures (732 every-3-day corridor block trains)
    sh_rows = []
    sh_id_to_idx = {}
    with open(os.path.join(target_dir, F["shuttles"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sh_id_to_idx[row["shuttle_id"]] = len(sh_rows)
            sh_rows.append(row)
    n_sh = len(sh_rows)
    shuttle_corr = np.array([CORR_IDX[r["corridor_id"]] for r in sh_rows], dtype=int)
    shuttle_port = np.array([PORT_IDX[r["port_id"]] for r in sh_rows], dtype=int)
    shuttle_dep_ts = [_parse_ts(r["scheduled_departure_ts_utc"]) for r in sh_rows]
    shuttle_day = np.array(
        [(_parse_ts(r["scheduled_departure_ts_utc"]).astimezone(UTC).date() - BASE_DATE).days - 1 for r in sh_rows],
        dtype=int,
    )
    shuttle_quarter = _day_to_quarter(np.clip(shuttle_day, 0, core.N_DAYS - 1))
    planned_on_shuttle = np.array([int(r["planned_wf_slots"]) for r in sh_rows], dtype=int)
    wf_booked_slots_sh = np.array([int(r["booked_wf_slots"]) for r in sh_rows], dtype=int)
    wf_actual_loaded_sh = np.array([int(r["loaded_wf_slots"]) for r in sh_rows], dtype=int)
    wf_standby_rolled_total_sh = np.array([int(r["wf_standby_rolled"]) for r in sh_rows], dtype=int)
    consist_wagons_short_sh = np.array([int(r["consist_wagons_short"]) for r in sh_rows], dtype=int)
    loco_derate_sh = np.array([int(r["loco_derate_events"]) for r in sh_rows], dtype=int)
    train_wagon_count_sh = np.array([int(r["train_wagon_count"]) for r in sh_rows], dtype=int)
    train_gross_tonnes_sh = np.array([float(r["train_total_gross_tonnes"]) for r in sh_rows], dtype=float)

    # Map (port_idx, slot_idx) -> scheduled departure timestamp for exact CHED notice lead calculation
    n_slots = n_sh // 6
    port_slot_dep_ts = {}
    for s_idx in range(n_sh):
        p_idx = int(shuttle_port[s_idx])
        sl_idx = s_idx % n_slots
        port_slot_dep_ts[(p_idx, sl_idx)] = shuttle_dep_ts[s_idx]

    # 9. Container Milestones (filter VOID, retain max extract_version)
    ms_raw = 0
    ms_void = 0
    ms_latest = {}
    with open(os.path.join(target_dir, F["milestones"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ms_raw += 1
            if row["record_status"] == "VOID":
                ms_void += 1
                continue
            cid = row["container_id"]
            ver = int(row["extract_version"])
            prev = ms_latest.get(cid)
            if prev is None or ver > prev[0]:
                ms_latest[cid] = (ver, row)
    cids_sorted = sorted(ms_latest.keys())
    n = len(cids_sorted)
    assert n == core.N_CONTAINERS, f"Expected {core.N_CONTAINERS} settled containers, got {n}"
    cleaning["milestones_raw_rows"] = ms_raw
    cleaning["milestones_void_removed"] = ms_void
    cleaning["milestones_superseded_removed"] = ms_raw - ms_void - n
    cleaning["milestones_settled_containers"] = n

    # 10. Customs Consignments & BIP Notices
    cont_ched_str = {}
    ched_ids_set = set()
    with open(os.path.join(target_dir, F["consignments"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            cont_ched_str[row["container_id"]] = row["ched_lot_id"]
            ched_ids_set.add(row["ched_lot_id"])
    ched_sorted = sorted(ched_ids_set)
    ched_to_idx = {s: i for i, s in enumerate(ched_sorted)}
    n_lots = len(ched_sorted)

    bip_map = {}
    with open(os.path.join(target_dir, F["bip_notices"]), encoding="utf-8") as f:
        for line in f:
            if line.strip():
                rec = json.loads(line)
                bip_map[rec["ched_lot_id"]] = rec
    cleaning["bip_notice_lots"] = len(bip_map)

    # Assemble container arrays
    vessels_sorted = sorted({ms_latest[c][1]["vessel_id"] for c in cids_sorted})
    v_to_idx = {v: i for i, v in enumerate(vessels_sorted)}

    cont_vessel = np.zeros(n, dtype=int)
    cont_corr = np.zeros(n, dtype=int)
    cont_port = np.zeros(n, dtype=int)
    cont_dc = np.zeros(n, dtype=int)
    cont_zone = np.zeros(n, dtype=int)
    cont_line = np.zeros(n, dtype=int)
    cont_day = np.zeros(n, dtype=int)
    cont_unload_day = np.zeros(n, dtype=int)
    cont_is_rail = np.zeros(n, dtype=bool)
    cont_rolled_rail = np.zeros(n, dtype=bool)
    cont_shuttle = np.zeros(n, dtype=int)
    cont_ched = np.zeros(n, dtype=int)
    cont_bip_sampled = np.zeros(n, dtype=bool)

    obs_vessel_berth = np.zeros(n, dtype=float)
    obs_edi_docs = np.zeros(n, dtype=float)
    obs_term_yard_hold = np.zeros(n, dtype=float)
    obs_phyto_hold_direct = np.zeros(n, dtype=float)
    obs_rail_tms_raw = np.zeros(n, dtype=float)
    obs_dc_dock_wait = np.zeros(n, dtype=float)
    obs_dray_empty_hold = np.zeros(n, dtype=float)
    obs_depot_turnaway = np.zeros(n, dtype=float)

    lot_port = np.zeros(n_lots, dtype=int)
    lot_day = np.zeros(n_lots, dtype=int)
    lot_zone = np.zeros(n_lots, dtype=int)
    lot_size = np.zeros(n_lots, dtype=int)
    lot_bip = np.zeros(n_lots, dtype=bool)
    lot_lead_hours = np.full(n_lots, 999.0, dtype=float)

    for i, cid in enumerate(cids_sorted):
        r = ms_latest[cid][1]
        cont_vessel[i] = v_to_idx[r["vessel_id"]]
        cont_corr[i] = CORR_IDX[r["corridor_id"]]
        cont_port[i] = PORT_IDX[r["port_id"]]
        cont_dc[i] = DC_IDX[r["dc_id"]]
        cont_zone[i] = ZONE_IDX[r["thermal_zone"]]
        cont_line[i] = LINE_IDX[r["shipping_line_id"]]
        dis_d = _parse_ts(r["discharge_ts_utc"]).astimezone(UTC).date()
        un_d = _parse_ts(r["unload_complete_ts_cet"]).astimezone(BERLIN).date()
        cont_day[i] = (dis_d - BASE_DATE).days
        cont_unload_day[i] = (un_d - BASE_DATE).days
        is_r = r["mode"] == "RAIL"
        cont_is_rail[i] = is_r
        if is_r:
            psh = r["planned_shuttle_id"]
            cont_shuttle[i] = sh_id_to_idx[psh]
            cont_rolled_rail[i] = (r["departed_shuttle_id"] != psh)
        else:
            cont_shuttle[i] = cont_corr[i] * n_slots + (cont_day[i] // 3)
        cs = cont_ched_str[cid]
        lid = ched_to_idx[cs]
        cont_ched[i] = lid
        lot_port[lid] = cont_port[i]
        lot_day[lid] = cont_day[i]
        lot_zone[lid] = cont_zone[i]
        lot_size[lid] += 1
        cont_bip_sampled[i] = (int(r["bip_sampled_ind"]) == 1)

        obs_vessel_berth[i] = float(r["excess_berth_cdays"])
        obs_edi_docs[i] = float(r["excess_edi_cdays"])
        obs_term_yard_hold[i] = float(r["excess_port_yard_cdays"])
        obs_phyto_hold_direct[i] = float(r["excess_phyto_cdays"])
        obs_rail_tms_raw[i] = float(r["excess_rail_cdays"])
        obs_dc_dock_wait[i] = float(r["excess_dc_dock_cdays"])
        obs_dray_empty_hold[i] = float(r["excess_dray_empty_cdays"])
        obs_depot_turnaway[i] = float(r["excess_depot_gate_cdays"])

    for cs, rec in bip_map.items():
        lid = ched_to_idx[cs]
        lot_bip[lid] = True
        p_idx = int(lot_port[lid])
        sl_idx = int(lot_day[lid]) // 3
        dep_ts = port_slot_dep_ts[(p_idx, sl_idx)]
        notice_ts = _parse_ts(rec["exam_notice_ts_utc"])
        lot_lead_hours[lid] = (dep_ts - notice_ts).total_seconds() / 3600.0

    # Strictly observable decomposition of obs_rail_tms_raw on container grain:
    # - unrolled non-BIP rail containers observe pure rail_base (~0.025 c-days)
    # - BIP non-sampled rail sibling containers carry rail_base + sibling BIP wait
    # - rolled non-BIP rail containers carry rail_base + rollover wait (~3.25 c-days)
    is_bip_c = lot_bip[cont_ched]
    is_sib_rail = cont_is_rail & is_bip_c & (~cont_bip_sampled)
    unrolled_clean_rail = cont_is_rail & (~is_bip_c) & (~cont_rolled_rail)
    mean_base_rail = float(obs_rail_tms_raw[unrolled_clean_rail].mean())

    obs_phyto_sibling_tms_rail = np.where(
        is_sib_rail, np.maximum(0.0, obs_rail_tms_raw - mean_base_rail), 0.0
    )
    cont_rail_roll_dur = np.where(
        cont_is_rail & cont_rolled_rail, np.maximum(0.0, obs_rail_tms_raw - mean_base_rail), 0.0
    )
    cont_rail_base = np.where(
        cont_is_rail,
        np.where(cont_rolled_rail | is_sib_rail, np.minimum(obs_rail_tms_raw, mean_base_rail), obs_rail_tms_raw),
        0.0,
    )
    assert np.allclose(
        cont_rail_base + cont_rail_roll_dur + obs_phyto_sibling_tms_rail, obs_rail_tms_raw, atol=1e-9
    ), "Rail stage conservation failed!"

    # 11. Depot Turn-in Log audit (Layer 1 verification)
    ti_latest = {}
    ti_raw = 0
    ti_legacy_car = 0
    with open(os.path.join(target_dir, F["turnin"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            ti_raw += 1
            gid = row["gate_event_id"]
            ver = int(row["extract_version"])
            prev = ti_latest.get(gid)
            if prev is None or ver > prev[0]:
                ti_latest[gid] = (ver, row)
    ti_turn_h = 0.0
    for _, row in ti_latest.values():
        if row["carrier_code"] in carrier_map:
            ti_legacy_car += 1
        if row["gate_status"] == "TURN_AWAY":
            ti_turn_h += float(row["turnaway_delay_hours"])
    assert abs(ti_turn_h / 24.0 - obs_depot_turnaway.sum()) < 1e-2, "Depot turnaway log mismatch!"
    cleaning["turnin_raw_rows"] = ti_raw
    cleaning["turnin_superseded_removed"] = ti_raw - len(ti_latest)
    cleaning["turnin_legacy_carrier_mapped"] = ti_legacy_car

    # 12. Empty-Depot Booking Portal Log (exact stock-flow conservation)
    portal_rows = []
    max_pday = 0
    with open(os.path.join(target_dir, F["portal"]), encoding="utf-8") as f:
        for row in csv.DictReader(f):
            t = (_parse_date(row["date_iso"]) - BASE_DATE).days
            max_pday = max(max_pday, t)
            portal_rows.append((t, PORT_IDX[row["depot_port_id"]], LINE_IDX[row["shipping_line_id"]],
                                int(row["confirmed_bookings"]), int(row["quota_closed_rejections"])))
    n_q_days = max_pday + 1
    portal_confirmed = np.zeros((3, 4, n_q_days), dtype=int)
    portal_rejected = np.zeros((3, 4, n_q_days), dtype=int)
    for t, p, l, cf, rj in portal_rows:
        portal_confirmed[p, l, t] = cf
        portal_rejected[p, l, t] = rj

    daily_empty_unloads = np.zeros((3, 4, n_q_days), dtype=int)
    for p in range(3):
        for l in range(4):
            m = (cont_port == p) & (cont_line == l)
            daily_empty_unloads[p, l] = np.bincount(cont_unload_day[m], minlength=n_q_days)
    daily_empty_gateins = portal_confirmed.copy()

    # 13. Carrier Dispute Close-Out XLSX (invoice-scope reconciliation reference)
    wb_d = load_workbook(os.path.join(target_dir, F["disputes"]), data_only=True)
    ws_d = wb_d["Annual_Closeout_Summary"]
    dispute_settled_eur = {}
    for r_i in range(5, 13):
        dispute_settled_eur[str(ws_d.cell(r_i, 1).value)] = float(ws_d.cell(r_i, 6).value)

    world = {
        "N_QUEUE_DAYS": n_q_days,
        "cont_vessel": cont_vessel,
        "cont_corr": cont_corr,
        "cont_port": cont_port,
        "cont_day": cont_day,
        "cont_unload_day": cont_unload_day,
        "cont_quarter": _day_to_quarter(cont_day),
        "cont_dc": cont_dc,
        "cont_zone": cont_zone,
        "cont_line": cont_line,
        "cont_is_rail": cont_is_rail,
        "cont_rolled_rail": cont_rolled_rail,
        "cont_rail_excess": cont_rail_base + cont_rail_roll_dur,
        "cont_rail_base": cont_rail_base,
        "cont_rail_roll_dur": cont_rail_roll_dur,
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
        "lot_zone": lot_zone,
        "lot_size": lot_size,
        "lot_bip": lot_bip,
        "lot_lead_hours": lot_lead_hours,
        "shuttle_corr": shuttle_corr,
        "shuttle_port": shuttle_port,
        "shuttle_day": shuttle_day,
        "shuttle_quarter": shuttle_quarter,
        "planned_on_shuttle": planned_on_shuttle,
        "wf_booked_slots_sh": wf_booked_slots_sh,
        "wf_actual_loaded_sh": wf_actual_loaded_sh,
        "wf_standby_rolled_total_sh": wf_standby_rolled_total_sh,
        "loco_derate_sh": loco_derate_sh,
        "consist_wagons_short_sh": consist_wagons_short_sh,
        "train_wagon_count_sh": train_wagon_count_sh,
        "train_gross_tonnes_sh": train_gross_tonnes_sh,
        "portal_confirmed": portal_confirmed,
        "portal_rejected": portal_rejected,
        "daily_empty_unloads": daily_empty_unloads,
        "daily_empty_gateins": daily_empty_gateins,
        "budgets_meta": {
            "corr_budget": corr_budget,
            "corr_capture": corr_capture,
            "corr_dist": corr_dist,
            "vol_growth": vol_growth,
            "plug_cap_27": plug_cap_27,
            "rail_fleet_27": rail_fleet_27,
            "dray_cont_27": dray_cont_27,
            "tariffs": tariffs,
            "dispute_settled_eur": dispute_settled_eur,
        },
        "cleaning": cleaning,
    }
    return world


def _slate_from_bcrs(bcrs):
    ranked = sorted(core.CORRIDORS, key=lambda c: (-bcrs[c], c))
    funded, spent = [], 0.0
    for c in ranked:
        b = core.CORR_BUDGET_EUR[c]
        if spent + b <= core.BUDGET_CAP_EUR + 1e-9:
            funded.append(c)
            spent += b
    return sorted(funded), ranked


def _corridor_detail(w, rp, pb, rh, bb, sb, dr, db):
    """Compute full per-corridor 2026 attribution, 2027 projection, avoidable EUR, BCR, rank, and FUND/DEFER."""
    rows = []
    for c_idx, cname in enumerate(core.CORRIDORS):
        p_name = core.PORTS[int(core.CORR_PORT[c_idx])]
        d_name = core.DCS[int(core.CORR_DC[c_idx])]
        mc = w["cont_corr"] == c_idx
        ms = w["shuttle_corr"] == c_idx

        plug_26 = float(rp[mc].sum())
        c1_26 = float(pb[mc].sum())
        rail_26 = float(rh[ms].sum())
        c2_26 = float(bb[ms].sum())
        sib_26 = float(sb[ms].sum())
        dray_26 = float(dr[mc].sum())
        c3_26 = float(db[mc].sum())
        cc_26 = plug_26 + rail_26 + dray_26

        vg = core.PLAN_2027["vol_growth_corridor"][cname]
        pf = core.PLAN_2027["plug_capacity_factor_2027"][p_name]
        rf = core.PLAN_2027["rail_fleet_factor_2027"][p_name]
        df = core.PLAN_2027["dray_contract_factor_2027"][p_name]

        plug_27 = plug_26 * vg * pf
        rail_27 = rail_26 * vg * rf
        dray_27 = dray_26 * vg * df
        cc_27 = plug_27 + rail_27 + dray_27

        gross_27 = (
            plug_27 * core.TARIFF_EUR["reefer_plug"]
            + rail_27 * core.TARIFF_EUR["rail_handoff"]
            + dray_27 * core.TARIFF_EUR["drayage_carrier"]
        )
        cap_rate = core.CORR_CAPTURE_RATE[cname]
        avoid_27 = gross_27 * cap_rate
        bud = core.CORR_BUDGET_EUR[cname]
        bcr = avoid_27 / bud

        rows.append({
            "corridor_id": cname,
            "port_id": p_name,
            "dc_id": d_name,
            "haul_distance_km": int(core.CORR_DIST_KM[c_idx]),
            "containers_2026": int(mc.sum()),
            "rail_containers_2026": int((mc & w["cont_is_rail"]).sum()),
            "budget_eur": round(bud, 2),
            "capture_rate_2027": cap_rate,
            "vol_growth_2027": vg,
            "plug_factor_2027": pf,
            "rail_factor_2027": rf,
            "dray_factor_2027": df,
            "raw_port_yard_2026": round(float(w["obs_term_yard_hold"][mc].sum()), 4),
            "raw_rail_tms_2026": round(float((w["cont_rail_excess"] + w["obs_phyto_sibling_tms_rail"])[mc].sum()), 4),
            "raw_dray_empty_2026": round(float(w["obs_dray_empty_hold"][mc].sum()), 4),
            "reefer_plug_2026": round(plug_26, 4),
            "rail_handoff_2026": round(rail_26, 4),
            "drayage_carrier_2026": round(dray_26, 4),
            "c1_coldstore_pullback_2026": round(c1_26, 4),
            "c2_phyto_rail_roll_2026": round(c2_26, 4),
            "phyto_sibling_rail_2026": round(sib_26, 4),
            "c3_depot_backlog_2026": round(c3_26, 4),
            "carrier_ctrl_cdays_2026": round(cc_26, 4),
            "reefer_plug_2027": round(plug_27, 4),
            "rail_handoff_2027": round(rail_27, 4),
            "drayage_carrier_2027": round(dray_27, 4),
            "carrier_ctrl_cdays_2027": round(cc_27, 4),
            "gross_eur_2027": round(gross_27, 2),
            "avoidable_eur_2027": round(avoid_27, 2),
            "bcr_2027": round(bcr, 6),
        })

    rows.sort(key=lambda r: (-r["bcr_2027"], r["corridor_id"]))
    spent = 0.0
    for rank, r in enumerate(rows, start=1):
        r["rank"] = rank
        if spent + r["budget_eur"] <= core.BUDGET_CAP_EUR + 1e-9:
            r["decision"] = "FUND"
            spent += r["budget_eur"]
        else:
            r["decision"] = "DEFER"
    return rows


def run_all(target_dir=None):
    target_dir = target_dir or os.path.join(TASK_DIR, "target")
    w = load_shipped_pack(target_dir)

    # Golden run directly from shipped files
    rp_g, pb_g, m1_g = core.estimate_s1(w, mode="golden")
    rh_g, bb_g, sb_g, m2_g = core.estimate_s2(w, mode="golden")
    dr_g, db_g, m3_g = core.estimate_s3(w, mode="golden")
    gold = core.evaluate_corridors(w, rp_g, pb_g, rh_g, bb_g, sb_g, dr_g, db_g)
    corridor_rows = _corridor_detail(w, rp_g, pb_g, rh_g, bb_g, sb_g, dr_g, db_g)
    gold_slate, gold_ranked = _slate_from_bcrs(gold["members"])

    # Verify exact parity with core.py on simulated world (within tiny observable base_rail separation tolerance)
    w_core = core.simulate_world(core.SEED)
    gold_core = core._run_combo(w_core, {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden"})
    assert abs(gold["C1_coldstore_pullback_2026"] - gold_core["C1_coldstore_pullback_2026"]) < 0.05
    assert abs(gold["C2_phyto_rail_roll_2026"] - gold_core["C2_phyto_rail_roll_2026"]) < 15.0
    assert abs(gold["C3_depot_backlog_2026"] - gold_core["C3_depot_backlog_2026"]) < 0.05
    for cn in core.CORRIDORS:
        assert abs(gold["members"][cn] - gold_core["members"][cn]) < 0.003, (
            f"Parity drift on {cn}: pack={gold['members'][cn]:.4f} vs core={gold_core['members'][cn]:.4f}"
        )

    # 21-variant family directly on shipped pack
    fam_configs = [
        ("S1: binned non-param", {"mode": "golden", "spec_form": "bins"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: piecewise spline", {"mode": "golden", "spec_form": "spline"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: Huber robust FE", {"mode": "golden", "spec_form": "huber"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: port-day FE", {"mode": "golden", "fe": "port_day"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: corr-week FE", {"mode": "golden", "fe": "corr_week"}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: hinge 0.76", {"mode": "golden", "hinge": 0.76}, {"mode": "golden"}, {"mode": "golden"}),
        ("S1: hinge 0.80", {"mode": "golden", "hinge": 0.80}, {"mode": "golden"}, {"mode": "golden"}),
        ("S2: Poisson IRLS", {"mode": "golden"}, {"mode": "golden", "method": "poisson_irls"}, {"mode": "golden"}),
        ("S2: Huber robust", {"mode": "golden"}, {"mode": "golden", "method": "huber"}, {"mode": "golden"}),
        ("S2: binned lead (no cut)", {"mode": "golden"}, {"mode": "golden", "method": "binned_lead"}, {"mode": "golden"}),
        ("S2: hard step cut", {"mode": "golden"}, {"mode": "golden", "method": "hard_step"}, {"mode": "golden"}),
        ("S2: month+corr FE", {"mode": "golden"}, {"mode": "golden", "method": "month_fe"}, {"mode": "golden"}),
        ("S2: pooled slope", {"mode": "golden"}, {"mode": "golden", "method": "pooled_slope"}, {"mode": "golden"}),
        ("S2: booked-slot ctrl", {"mode": "golden"}, {"mode": "golden", "method": "booked_ctrl"}, {"mode": "golden"}),
        ("S3: dc-day FE", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "fe": "dc_day"}),
        ("S3: port-day FE", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "fe": "port_day"}),
        ("S3: corr-week FE", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "fe": "corr_week"}),
        ("S3: harmonic OLS", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "fe": "harmonic"}),
        ("S3: Huber robust FE", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "spec_form": "huber"}),
        ("S3: distance param", {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden", "spec_form": "dist_param"}),
        ("Joint: spline+poisson+dcday", {"mode": "golden", "spec_form": "spline"},
         {"mode": "golden", "method": "poisson_irls"}, {"mode": "golden", "fe": "dc_day"}),
    ]
    variants = []
    for nm, k1, k2, k3 in fam_configs:
        res = core._run_combo(w, k1, k2, k3)
        sl, _ = _slate_from_bcrs(res["members"])
        assert sl == gold_slate, f"Variant {nm} flipped call: {sl} != {gold_slate}"
        variants.append({
            "name": nm,
            "funded_slate": sl,
            "C1_coldstore_pullback_2026": round(res["C1_coldstore_pullback_2026"], 2),
            "C2_phyto_rail_roll_2026": round(res["C2_phyto_rail_roll_2026"], 2),
            "C3_depot_backlog_2026": round(res["C3_depot_backlog_2026"], 2),
            "bcrs": {c: round(res["members"][c], 4) for c in core.CORRIDORS},
            "fal_err": round(res["fal_err"], 2),
        })

    # Tight empirical bands from the 21-variant family (25% padding beyond family spread, matching corelib)
    def _band(vals, pad=0.25, dec=3):
        lo, hi = min(vals), max(vals)
        sp = max(hi - lo, 1e-6)
        return [round(lo - pad * sp, dec), round(hi + pad * sp, dec)]

    bands = {
        "C1_coldstore_pullback_2026": _band([gold["C1_coldstore_pullback_2026"]] + [v["C1_coldstore_pullback_2026"] for v in variants], dec=1),
        "C2_phyto_rail_roll_2026": _band([gold["C2_phyto_rail_roll_2026"]] + [v["C2_phyto_rail_roll_2026"] for v in variants], dec=1),
        "C3_depot_backlog_2026": _band([gold["C3_depot_backlog_2026"]] + [v["C3_depot_backlog_2026"] for v in variants], dec=1),
    }
    for cn in core.CORRIDORS:
        bands["BCR_" + cn.replace("-", "_")] = _band(
            [gold["members"][cn]] + [v["bcrs"][cn] for v in variants], dec=4
        )

    # 8 +/-15% Forcing stress tests
    perturbations = []
    for label, opts in (
        ("S1 -15%", {"mult_s1": 0.85}),
        ("S1 +15%", {"mult_s1": 1.15}),
        ("S2 -15%", {"mult_s2": 0.85}),
        ("S2 +15%", {"mult_s2": 1.15}),
        ("S3 -15%", {"mult_s3": 0.85}),
        ("S3 +15%", {"mult_s3": 1.15}),
        ("base -15%", {"mult_base": 0.85}),
        ("base +15%", {"mult_base": 1.15}),
    ):
        pr = core._run_combo(w, {"mode": "golden"}, {"mode": "golden"}, {"mode": "golden"}, opts=opts)
        psl, _ = _slate_from_bcrs(pr["members"])
        assert psl == gold_slate, f"Forcing stress {label} flipped: {psl} != {gold_slate}"
        perturbations.append({
            "input": label,
            "answer": psl,
            "bcrs": {c: round(pr["members"][c], 4) for c in core.CORRIDORS},
        })

    # Lattice, run routes, shortcuts, over-corrections
    def _eval_route(k1, k2, k3):
        r = core._run_combo(w, k1, k2, k3)
        sl, rnk = _slate_from_bcrs(r["members"])
        return {
            "funded_slate": sl,
            "ranking": rnk,
            "bcrs": {c: round(r["members"][c], 4) for c in core.CORRIDORS},
            "avoid_eur": {c: round(r["avoid_eur"][c], 2) for c in core.CORRIDORS},
            "C1_coldstore_pullback_2026": round(r["C1_coldstore_pullback_2026"], 1),
            "C2_phyto_rail_roll_2026": round(r["C2_phyto_rail_roll_2026"], 1),
            "C3_depot_backlog_2026": round(r["C3_depot_backlog_2026"], 1),
            "fal_err": round(r["fal_err"], 2),
        }

    routes = {
        "golden": _eval_route({"mode": "golden"}, {"mode": "golden"}, {"mode": "golden"}),
        "direct": _eval_route({"mode": "direct"}, {"mode": "direct"}, {"mode": "direct"}),
        "rigorous": _eval_route({"mode": "rigorous"}, {"mode": "rigorous"}, {"mode": "rigorous"}),
        "generous": _eval_route({"mode": "generous"}, {"mode": "generous"}, {"mode": "generous"}),
        "hedge": _eval_route({"mode": "hedge"}, {"mode": "hedge"}, {"mode": "hedge"}),
        "cutoff": _eval_route({"mode": "cutoff_95"}, {"mode": "cutoff_any_bip"}, {"mode": "one_fact_binary"}),
        "S1_drop": _eval_route({"mode": "hurried"}, {"mode": "golden"}, {"mode": "golden"}),
        "S2_drop": _eval_route({"mode": "golden"}, {"mode": "hurried"}, {"mode": "golden"}),
        "S3_drop": _eval_route({"mode": "golden"}, {"mode": "golden"}, {"mode": "hurried"}),
        "S1_S2_drop": _eval_route({"mode": "hurried"}, {"mode": "hurried"}, {"mode": "golden"}),
        "S1_S3_drop": _eval_route({"mode": "hurried"}, {"mode": "golden"}, {"mode": "hurried"}),
        "S2_S3_drop": _eval_route({"mode": "golden"}, {"mode": "hurried"}, {"mode": "hurried"}),
        "S1_over": _eval_route({"mode": "over"}, {"mode": "golden"}, {"mode": "golden"}),
        "S2_over": _eval_route({"mode": "golden"}, {"mode": "over"}, {"mode": "golden"}),
        "S3_over": _eval_route({"mode": "golden"}, {"mode": "golden"}, {"mode": "over"}),
        "S1_one_fact": _eval_route({"mode": "one_fact_sym"}, {"mode": "golden"}, {"mode": "golden"}),
        "S2_one_fact": _eval_route({"mode": "golden"}, {"mode": "one_fact_crosstab"}, {"mode": "golden"}),
        "S3_one_fact": _eval_route({"mode": "golden"}, {"mode": "golden"}, {"mode": "one_fact_binary"}),
        "S1_sym_lin": _eval_route({"mode": "cutoff_sym_lin"}, {"mode": "golden"}, {"mode": "golden"}),
        "S3_port_raw": _eval_route({"mode": "golden"}, {"mode": "golden"}, {"mode": "cutoff_raw"}),
    }

    # Verify exact integer knapsack == greedy top-3
    best_eur, best_set = -1.0, None
    for r_k in range(1, len(core.CORRIDORS) + 1):
        for comb in itertools.combinations(core.CORRIDORS, r_k):
            if sum(core.CORR_BUDGET_EUR[c] for c in comb) <= core.BUDGET_CAP_EUR + 1e-9:
                tot = sum(gold["avoid_eur"][c] for c in comb)
                if tot > best_eur:
                    best_eur, best_set = tot, sorted(comb)
    assert best_set == gold_slate, f"Knapsack {best_set} != Greedy {gold_slate}"

    # Observable physical diagnostics for deck / workbook / Step-by-Step
    ch_u, ch_nf = core._reconstruct_chambers(w)
    u_ch_c = ch_u[w["cont_dc"], w["cont_zone"], w["cont_day"]]
    nf_c = ch_nf[w["cont_dc"], w["cont_zone"], w["cont_day"]]
    bm = (u_ch_c >= 0.84) & (u_ch_c <= 0.94)
    raw_asym_gap_h = float((w["obs_term_yard_hold"][bm & (nf_c > 0)].mean() - w["obs_term_yard_hold"][bm & (nf_c <= 0)].mean()) * 24.0)
    res_plug_dm = core._demean_by_group(rp_g, w["cont_vessel"] * 6 + w["cont_corr"], core.N_VESSELS * 6)
    res_asym_gap_h = float((res_plug_dm[bm & (nf_c > 0)].mean() - res_plug_dm[bm & (nf_c <= 0)].mean()) * 24.0)

    q_grid = core._reconstruct_depot_queue(w)
    q_c = q_grid[w["cont_port"], w["cont_line"], w["cont_unload_day"]]
    rej_c = w["portal_rejected"][w["cont_port"], w["cont_line"], w["cont_unload_day"]]
    op = rej_c == 0
    raw_drain_gap_h = float((w["obs_dray_empty_hold"][op & (q_c >= 0.8)].mean() - w["obs_dray_empty_hold"][op & (q_c < 0.15)].mean()) * 24.0)
    res_dray_dm = core._demean_by_group(dr_g, w["cont_corr"] * 56 + (w["cont_unload_day"] // 7), 6 * 56)
    res_drain_gap_h = float((res_dray_dm[op & (q_c >= 0.8)].mean() - res_dray_dm[op & (q_c < 0.15)].mean()) * 24.0)

    # S2 empirical port cuts (profiled from shipped data)
    emp_cuts = {}
    act = w["planned_on_shuttle"] > 0
    is_rail = w["cont_is_rail"]
    lot_bip = w["lot_bip"]
    lot_lead = w["lot_lead_hours"]
    cont_ched = w["cont_ched"]
    sh_id = w["cont_shuttle"]
    rolled_sh = w["wf_standby_rolled_total_sh"].astype(float)
    n_sh = len(rolled_sh)
    for p_idx, p_name in enumerate(core.PORTS):
        mp = act & (w["shuttle_port"] == p_idx)
        best_c, best_rss = 20.0, 1e18
        for cand in (10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0):
            lp_c = core._sigmoid((cand - lot_lead[cont_ched]) / 1.8)
            lk = np.bincount(sh_id, weights=np.where(is_rail & lot_bip[cont_ched], lp_c, 0.0), minlength=n_sh)
            Xp = np.column_stack([np.ones(mp.sum()), lk[mp], w["consist_wagons_short_sh"][mp], w["loco_derate_sh"][mp]])
            bp, _, _, _ = np.linalg.lstsq(Xp, rolled_sh[mp], rcond=None)
            rss = float(np.sum((rolled_sh[mp] - Xp @ bp) ** 2))
            if rss < best_rss:
                best_rss, best_c = rss, cand
        emp_cuts[p_name] = best_c

    # Portfolio totals
    funded_rows = [r for r in corridor_rows if r["decision"] == "FUND"]
    deferred_rows = [r for r in corridor_rows if r["decision"] == "DEFER"]
    funded_budget = round(sum(r["budget_eur"] for r in funded_rows), 2)
    unspent_budget = round(core.BUDGET_CAP_EUR - funded_budget, 2)
    funded_avoid_eur = round(sum(r["avoidable_eur_2027"] for r in funded_rows), 2)
    portfolio_bcr = round(funded_avoid_eur / funded_budget, 4)
    all6_avoid_eur = round(sum(r["avoidable_eur_2027"] for r in corridor_rows), 2)
    all6_cc_2026 = round(sum(r["carrier_ctrl_cdays_2026"] for r in corridor_rows), 1)
    all6_cc_2027 = round(sum(r["carrier_ctrl_cdays_2027"] for r in corridor_rows), 1)

    total_2026_all8 = round(float(
        w["obs_vessel_berth"].sum()
        + w["obs_edi_docs"].sum()
        + w["obs_term_yard_hold"].sum()
        + w["obs_dc_dock_wait"].sum()
        + w["obs_phyto_hold_direct"].sum()
        + w["obs_phyto_sibling_tms_rail"].sum()
        + w["cont_rail_excess"].sum()
        + w["obs_dray_empty_hold"].sum()
        + w["obs_depot_turnaway"].sum()
    ), 2)

    figures = {
        "task": "task27",
        "architecture": 2,
        "v4_hardened": True,
        "seed": core.SEED,
        "budget_cap_eur": core.BUDGET_CAP_EUR,
        "funded_slate": gold_slate,
        "deferred_slate": sorted(r["corridor_id"] for r in deferred_rows),
        "ranked_corridors": gold_ranked,
        "funded_budget_eur": funded_budget,
        "unspent_budget_eur": unspent_budget,
        "funded_avoidable_eur_2027": funded_avoid_eur,
        "funded_portfolio_bcr": portfolio_bcr,
        "all6_avoidable_eur_2027": all6_avoid_eur,
        "all6_carrier_ctrl_cdays_2026": all6_cc_2026,
        "all6_carrier_ctrl_cdays_2027": all6_cc_2027,
        "total_2026_all8_cdays": total_2026_all8,
        "R1_reconciled_containers": core.N_CONTAINERS,
        "golden_fal_err": round(gold["fal_err"], 2),
        "corridor_bcrs": {c: round(gold["members"][c], 3) for c in core.CORRIDORS},
        "C1_coldstore_pullback_2026": round(gold["C1_coldstore_pullback_2026"], 1),
        "C2_phyto_rail_roll_2026": round(gold["C2_phyto_rail_roll_2026"], 1),
        "C3_depot_backlog_2026": round(gold["C3_depot_backlog_2026"], 1),
        "total_non_carrier_removed_2026": round(
            gold["C1_coldstore_pullback_2026"] + gold["C2_phyto_rail_roll_2026"] + gold["C3_depot_backlog_2026"], 1
        ),
        "n_variants": len(variants),
        "phyto_sibling_rail_2026": round(float(sb_g.sum()), 1),
        "BCR_BHV_HAN": round(gold["members"]["BHV-HAN"], 3),
        "BCR_BHV_KAS": round(gold["members"]["BHV-KAS"], 3),
        "BCR_BHV_OSN": round(gold["members"]["BHV-OSN"], 3),
        "BCR_HAM_HAN": round(gold["members"]["HAM-HAN"], 3),
        "BCR_HAM_MAG": round(gold["members"]["HAM-MAG"], 3),
        "BCR_WHV_OSN": round(gold["members"]["WHV-OSN"], 3),
        "corridors": corridor_rows,
        "bands": bands,
        "diagnostics": {
            "golden_fal_err": round(gold["fal_err"], 2),
            "direct_fal_err": routes["direct"]["fal_err"],
            "rigorous_fal_err": routes["rigorous"]["fal_err"],
            "generous_fal_err": routes["generous"]["fal_err"],
            "cutoff_fal_err": routes["cutoff"]["fal_err"],
            "s1_one_fact_fal_err": routes["S1_one_fact"]["fal_err"],
            "s2_one_fact_fal_err": routes["S2_one_fact"]["fal_err"],
            "s3_one_fact_fal_err": routes["S3_one_fact"]["fal_err"],
            "s1_raw_asym_gap_h": round(raw_asym_gap_h, 2),
            "s1_resid_asym_gap_h": round(res_asym_gap_h, 2),
            "s1_dc_total_util_min_pct": round(float(w["dc_total_util"].min() * 100.0), 1),
            "s1_dc_total_util_max_pct": round(float(w["dc_total_util"].max() * 100.0), 1),
            "s2_emp_port_cuts_h": emp_cuts,
            "s2_bip_slope": round(float(m2_g["bip_slope"]), 3),
            "s3_raw_open_drain_gap_h": round(raw_drain_gap_h, 2),
            "s3_resid_open_drain_gap_h": round(res_drain_gap_h, 2),
            "s3_open_day_backlog_share_pct": round(float(100.0 * db_g[op].sum() / max(1e-9, db_g.sum())), 1),
            "knapsack_matches_greedy": True,
        },
        "variants": variants,
        "perturbations": perturbations,
        "routes": routes,
        "cleaning": w["cleaning"],
        "dispute_settled_eur": w["budgets_meta"]["dispute_settled_eur"],
        "reference": {
            "plan_year": 2027,
            "n_vessels": int(len(np.unique(w["cont_vessel"]))),
            "n_shuttles": int(len(w["shuttle_corr"])),
            "n_portal_days": int(w["N_QUEUE_DAYS"]),
            "tariffs_eur": w["budgets_meta"]["tariffs"],
            "min_4corridor_budget_eur": round(float(sum(sorted(core.CORR_BUDGET_EUR.values())[:4])), 2),
            "whv_osn_unconstrained_line_pct": round(
                100.0 * float((w["cont_line"][w["cont_corr"] == CORR_IDX["WHV-OSN"]] >= 2).mean()), 1
            ),
            "s1_hinge_pct": 78,
            "s1_band_lo_pct": 84,
            "s1_band_hi_pct": 94,
            "s1_shortcut_cut_pct": 92,
            "s2_lead_min_h": 1.5,
            "s2_lead_max_h": 72,
            "s3_clean_queue_thresh": 0.15,
            "s3_high_queue_thresh": 0.8,
        },
    }

    with open(os.path.join(HERE, "figures.json"), "w", encoding="utf-8") as f:
        json.dump(figures, f, indent=2, sort_keys=True)

    # Effort JSON aligned 100% with DESIGN_NOTE.md R1-R7 and effort.py / precut.py
    effort = {
        "task": "task27",
        "results": [
            {
                "id": "R1",
                "name": "Reconciled 2026 lifecycle spine and daily chamber/depot stock-flow series",
                "graded_as": "Supporting",
                "figure": "R1_reconciled_containers",
                "depends": [],
                "independent": "",
                "golden": 24000,
                "band": [24000, 24000],
                "precedent": [],
                "passes": {
                    "quick": 24525,
                    "careful": 24000,
                    "thorough": 24000,
                },
            },
            {
                "id": "R2",
                "name": "2026 inland cold-store chamber pull-back attribution C1 (S1)",
                "graded_as": "Component 1",
                "figure": "C1_coldstore_pullback_2026",
                "depends": ["R1"],
                "independent": "reconstructed (DC, zone) chamber daily stock and net flow filling-vs-draining hysteresis",
                "golden": figures["C1_coldstore_pullback_2026"],
                "band": bands["C1_coldstore_pullback_2026"],
                "partly": [6600.0, 8200.0],
                "precedent": ["L26", "L28", "L38", "N36"],
                "passes": {
                    "quick": routes["direct"]["C1_coldstore_pullback_2026"],
                    "careful": routes["rigorous"]["C1_coldstore_pullback_2026"],
                    "thorough": figures["C1_coldstore_pullback_2026"],
                },
            },
            {
                "id": "R3",
                "name": "2026 BIP-induced rail rollover attribution C2 (S2)",
                "graded_as": "Component 2",
                "figure": "C2_phyto_rail_roll_2026",
                "depends": ["R1"],
                "independent": "joint shuttle-level terminal-varying BIP lock cutoffs vs Nordbahn short-consist & loco cuts",
                "golden": figures["C2_phyto_rail_roll_2026"],
                "band": bands["C2_phyto_rail_roll_2026"],
                "partly": [3700.0, 4900.0],
                "precedent": ["L03", "L07", "L48", "N07"],
                "passes": {
                    "quick": routes["direct"]["C2_phyto_rail_roll_2026"],
                    "careful": routes["rigorous"]["C2_phyto_rail_roll_2026"],
                    "thorough": figures["C2_phyto_rail_roll_2026"],
                },
            },
            {
                "id": "R4",
                "name": "2026 ocean-line empty-depot backlog attribution C3 (S3)",
                "graded_as": "Component 3",
                "figure": "C3_depot_backlog_2026",
                "depends": ["R1"],
                "independent": "conserved (port, shipping_line) unbooked empty queue across multi-day open drain tails",
                "golden": figures["C3_depot_backlog_2026"],
                "band": bands["C3_depot_backlog_2026"],
                "partly": [6200.0, 8000.0],
                "precedent": ["N14", "N27", "L56", "L57"],
                "passes": {
                    "quick": routes["direct"]["C3_depot_backlog_2026"],
                    "careful": routes["rigorous"]["C3_depot_backlog_2026"],
                    "thorough": figures["C3_depot_backlog_2026"],
                },
            },
            {
                "id": "R5",
                "name": "Observable two-sided physical residual validation diagnostic",
                "graded_as": "Supporting",
                "figure": "golden_fal_err",
                "depends": ["R2", "R3", "R4"],
                "independent": "",
                "golden": figures["diagnostics"]["golden_fal_err"],
                "band": [0.0, 100.0],
                "precedent": ["L28", "L48"],
                "passes": {
                    "quick": routes["direct"]["fal_err"],
                    "careful": routes["rigorous"]["fal_err"],
                    "thorough": figures["diagnostics"]["golden_fal_err"],
                },
            },
            {
                "id": "R6",
                "name": "Six coupled 2027 corridor Benefit-Cost Ratios",
                "graded_as": "Ask 1",
                "figure": "corridor_bcrs",
                "depends": ["R2", "R3", "R4", "R5"],
                "independent": "",
                "golden": {c: round(gold["members"][c], 3) for c in core.CORRIDORS},
                "bands": {c: bands["BCR_" + c.replace("-", "_")] for c in core.CORRIDORS},
                "partly_share": 0.5,
                "precedent": ["L11", "L63"],
                "passes": {
                    "quick": {c: round(routes["direct"]["bcrs"][c], 3) for c in core.CORRIDORS},
                    "careful": {c: round(routes["rigorous"]["bcrs"][c], 3) for c in core.CORRIDORS},
                    "thorough": {c: round(gold["members"][c], 3) for c in core.CORRIDORS},
                },
            },
            {
                "id": "R7",
                "name": "2027 EUR 1.75M corridor remediation capital allocation slate",
                "graded_as": "Recommendation",
                "figure": "funded_slate",
                "depends": ["R2", "R3", "R4", "R5", "R6"],
                "independent": "",
                "golden": gold_slate,
                "precedent": ["L26", "L57", "L11"],
                "passes": {
                    "quick": {"value": routes["direct"]["funded_slate"], "grade": "missed", "why": "Direct TMS funds BHV-HAN, BHV-KAS, HAM-MAG (all three wrong)."},
                    "careful": {"value": routes["rigorous"]["funded_slate"], "grade": "missed", "why": "Rigorous baseline funds BHV-HAN, BHV-KAS, HAM-MAG (all three wrong)."},
                    "thorough": gold_slate,
                },
            },
        ],
        "hints": [
            {
                "sentence": "Inland DC thermal chambers pull back containers at the port yard more steeply when filling than when draining.",
                "rescues": ["R2"],
            },
            {
                "sentence": "Late EU BIP inspection notices lock booked rail slots with terminal-specific cutoffs and overlap Nordbahn short-consist cuts.",
                "rescues": ["R3"],
            },
            {
                "sentence": "Ocean-line empty-depot portal closures build multi-day return queues that outlive portal reopening across inland corridors.",
                "rescues": ["R4"],
            },
        ],
        "routes": [
            {"name": "the golden", "answer": gold_slate, "golden": True},
            {"name": "direct TMS codes / reflex", "answer": routes["direct"]["funded_slate"]},
            {"name": "rigorous standard (flat DC + direct CHED siblings)", "answer": routes["rigorous"]["funded_slate"]},
            {"name": "S1 dropped alone", "answer": routes["S1_drop"]["funded_slate"]},
            {"name": "S2 dropped alone", "answer": routes["S2_drop"]["funded_slate"]},
            {"name": "S3 dropped alone", "answer": routes["S3_drop"]["funded_slate"]},
            {"name": "S1 over-corrected", "answer": routes["S1_over"]["funded_slate"]},
            {"name": "S2 over-corrected", "answer": routes["S2_over"]["funded_slate"]},
            {"name": "S3 over-corrected", "answer": routes["S3_over"]["funded_slate"]},
            {"name": "generous run route", "answer": routes["generous"]["funded_slate"]},
            {"name": "cutoff run route", "answer": routes["cutoff"]["funded_slate"]},
            {"name": "S1 one-fact shortcut (>=92% binary)", "answer": routes["S1_one_fact"]["funded_slate"]},
            {"name": "S2 one-fact shortcut (bivariate 24h OLS)", "answer": routes["S2_one_fact"]["funded_slate"]},
            {"name": "S3 one-fact shortcut (unload-day portal rejection)", "answer": routes["S3_one_fact"]["funded_slate"]},
        ],
        "forcing": {
            "kind": "set",
            "golden_answer": gold_slate,
            "golden_family": [{"name": v["name"], "answer": v["funded_slate"]} for v in variants],
            "perturbations": [{"input": p["input"], "answer": p["answer"]} for p in perturbations],
        },
        "factorial": {
            "golden_answer": gold_slate,
            "reflex_route": {"answer": routes["direct"]["funded_slate"]},
            "judgments": [
                {
                    "id": "S1",
                    "name": "Asymmetric convex chamber-load hysteresis",
                    "kind": "stump",
                    "precedent": ["L26", "L28", "L38", "N36"],
                    "dropped": {"answer": routes["S1_drop"]["funded_slate"], "results_moved": ["R2", "R5", "R6", "R7"]},
                    "alone": {"answer": routes["S2_S3_drop"]["funded_slate"], "results_rescued": ["R2"]},
                },
                {
                    "id": "S2",
                    "name": "Joint terminal-varying BIP lock vs Nordbahn short-consist rail model",
                    "kind": "stump",
                    "precedent": ["L03", "L07", "L48", "N07"],
                    "dropped": {"answer": routes["S2_drop"]["funded_slate"], "results_moved": ["R3", "R5", "R6", "R7"]},
                    "alone": {"answer": routes["S1_S3_drop"]["funded_slate"], "results_rescued": ["R3"]},
                },
                {
                    "id": "S3",
                    "name": "Conserved shipping-line empty-depot queue stock across open drain days",
                    "kind": "stump",
                    "precedent": ["N14", "N27", "L56", "L57"],
                    "dropped": {"answer": routes["S3_drop"]["funded_slate"], "results_moved": ["R4", "R5", "R6", "R7"]},
                    "alone": {"answer": routes["S1_S2_drop"]["funded_slate"], "results_rescued": ["R4"]},
                },
                {
                    "id": "R1",
                    "name": "Layer 1 EDI deduplication, date/timezone harmonization, and SKU case-to-pallet crosswalk",
                    "kind": "reflex",
                    "precedent": ["R01", "R04"],
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
    print(f"Wrote figures.json & effort.json | funded={figs['funded_slate']} | budget=EUR {figs['funded_budget_eur']:,.2f} | avoidable=EUR {figs['funded_avoidable_eur_2027']:,.2f} | BCR={figs['funded_portfolio_bcr']:.4f}")
    print(f"Components: C1={figs['C1_coldstore_pullback_2026']} C2={figs['C2_phyto_rail_roll_2026']} C3={figs['C3_depot_backlog_2026']}")
    print("BCRs:", {r["corridor_id"]: round(r["bcr_2027"], 3) for r in figs["corridors"]})
    print("Diagnostics:", figs["diagnostics"])
