"""Materialize all tabular, JSONL, and XLSX input files in task27/target/ directly from core.py.

Every quantitative array comes directly from core.simulate_world(SEED) with zero post-hoc tweaks.
Layer 1 operational mess (mixed DD.MM.YYYY / YYYY-MM-DD dates, UTC vs Europe/Berlin CET/CEST
timestamps, duplicate superseded extract_version rows, VOID test EDI rows, CASE-to-PALLET units,
legacy store/carrier crosswalks, and two unlabelled distractors) emerges from standard logistics IT
interfaces and is strictly neutral on the clean analytical path.

No data dictionary, readme, notes sheet, or manifest file ships under target/ (H9 compliance).
"""
import csv
import datetime as dt
import json
import math
import os
from zoneinfo import ZoneInfo

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import core

ORG = "Weserfrucht Import GmbH"
ORG_RAIL = "Nordbahn Intermodal AG"
ORG_TOLL = "Bundesamt fuer Logistik und Mobilitaet"

PEOPLE = {
    "procurement": "Friedhilde Naser",
    "logistics": "Hilma Hofmann",
    "coldstore": "Vanessa Hoerle",
    "rail_ops": "Hans-Peter Briemer",
    "customs": "Carmelo Hermighausen",
    "drayage": "Mariechen Reuter",
    "controlling": "Meinhard Herrmann",
    "analyst": "Pero Kusch",
}

FILES = {
    "milestones": "container_milestones_2026.csv",
    "pallets": "warehouse_pallet_movements_2026.csv",
    "turnin": "depot_turnin_log_2026.csv",
    "port_yard": "terminal_yard_daily_2026.csv",
    "dc_inv": "coldstore_inventory_daily_2026.csv",
    "chambers": "dc_chamber_register_2026.csv",
    "skus": "sku_thermal_catalog.csv",
    "consignments": "customs_consignment_bol_2026.csv",
    "bip_notices": "bip_inspection_notices_2026.jsonl",
    "shuttles": "rail_shuttle_departures_2026.csv",
    "portal": "depot_portal_requests_2026.csv",
    "disputes": "carrier_dispute_closeout_2026.xlsx",
    "plan_2027": "import_plan_2027.csv",
    "crosswalk": "entity_crosswalk_2026.csv",
    "charter": "weserfrucht_remediation_charter_rc2027.pdf",
    "dist_bunker": "north_sea_bunker_fuel_index_2026.csv",
    "dist_maut": "german_toll_maut_rates_2026_2027.xlsx",
}

FREE_TIME_H = {
    "berth": 0.0,
    "edi": 6.0,
    "port_yard": 24.0,
    "phyto": 0.0,
    "rail": 6.0,
    "dc_dock": 4.0,
    "dray_empty": 24.0,
    "depot_gate": 0.0,
}

BASE_DATE = dt.date(2026, 1, 1)
UTC = dt.timezone.utc
BERLIN = ZoneInfo("Europe/Berlin")

PORT_SHUTTLE_DEP_UTC = {"BHV": (21, 30), "HAM": (22, 15), "WHV": (22, 45)}
ZONE_SETPOINTS = {"Z02": "+2C", "Z07": "+7C", "Z13": "+13C"}

PRODUCE_BY_ZONE = {
    "Z02": [
        ("Strawberries", "081010"),
        ("Blueberries", "081040"),
        ("Raspberries", "081020"),
        ("Nectarines", "080930"),
        ("Sweet Cherries", "080929"),
        ("Baby Spinach", "070970"),
    ],
    "Z07": [
        ("Navel Oranges", "080510"),
        ("Clementines", "080522"),
        ("Table Grapes", "080610"),
        ("Conference Pears", "080830"),
        ("Gala Apples", "080810"),
        ("Lemons", "080550"),
    ],
    "Z13": [
        ("Cavendish Bananas", "080390"),
        ("Hass Avocados", "080440"),
        ("Kent Mangoes", "080450"),
        ("MD2 Pineapples", "080430"),
        ("Red Grapefruit", "080540"),
        ("Papayas", "080720"),
    ],
}

ORIGINS_BY_ZONE = {
    "Z02": ["ES", "MA", "CL", "PE", "ZA"],
    "Z07": ["ZA", "EG", "ES", "AR", "CL"],
    "Z13": ["EC", "CR", "CO", "PE", "BR"],
}

LINE_NAMES = {
    "LINE_A": "Nordic Reefer Line",
    "LINE_B": "Hanseatic Ocean Alliance",
    "LINE_C": "Atlantic Fruit Carriers",
    "LINE_D": "Baltic Cold Express",
}

PORT_NAMES = {
    "BHV": "Bremerhaven",
    "HAM": "Hamburg",
    "WHV": "Wilhelmshaven",
}

DC_NAMES = {
    "HAN": "Hannover",
    "OSN": "Osnabrueck",
    "KAS": "Kassel",
    "MAG": "Magdeburg",
}


def _fmt_utc(ts):
    return ts.astimezone(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def _fmt_berlin(ts):
    loc = ts.astimezone(BERLIN)
    return loc.strftime("%Y-%m-%dT%H:%M:%S%z")[:-2] + ":" + loc.strftime("%z")[-2:]


def _shuttle_id(port_idx, day_idx):
    d = BASE_DATE + dt.timedelta(days=int(day_idx))
    return f"NBI-{core.PORTS[int(port_idx)]}-{d.strftime('%Y%m%d')}"


def _shuttle_dep_ts(port_idx, day_idx, jitter_min=0):
    d = BASE_DATE + dt.timedelta(days=int(day_idx) + 1)
    hh, mm = PORT_SHUTTLE_DEP_UTC[core.PORTS[int(port_idx)]]
    return dt.datetime(d.year, d.month, d.day, hh, mm, 0, tzinfo=UTC) + dt.timedelta(minutes=int(jitter_min))


def _split_int_total(total, n_parts, rng):
    if total <= 0:
        return []
    k = min(int(n_parts), int(total))
    if k <= 1:
        return [int(total)]
    weights = rng.dirichlet(np.ones(k) * 2.2)
    raw = np.maximum(1, np.floor(weights * total).astype(int))
    diff = int(total - raw.sum())
    if diff > 0:
        idx = rng.choice(k, size=diff, replace=True)
        for j in idx:
            raw[j] += 1
    elif diff < 0:
        need = -diff
        order = np.argsort(-raw)
        for j in order:
            take = min(need, int(raw[j] - 1))
            if take > 0:
                raw[j] -= take
                need -= take
            if need == 0:
                break
    assert int(raw.sum()) == int(total)
    return raw.tolist()


def _write_xlsx_styled(path, sheets):
    wb = Workbook()
    head_fill = PatternFill("solid", fgColor="1E3A5F")
    zebra_fill = PatternFill("solid", fgColor="F5F7FA")
    tot_fill = PatternFill("solid", fgColor="E8EEF5")
    thin = Side(style="thin", color="C5CDD8")
    med = Side(style="medium", color="1E3A5F")
    border_cell = Border(left=thin, right=thin, top=thin, bottom=thin)
    border_hdr = Border(bottom=med)

    for idx, spec in enumerate(sheets):
        ws = wb.active if idx == 0 else wb.create_sheet(spec["name"])
        ws.title = spec["name"]
        ws["A1"] = spec["title"]
        ws["A1"].font = Font(name="Calibri", size=12, bold=True, color="1E3A5F")
        ws["A2"] = spec["subtitle"]
        ws["A2"].font = Font(name="Calibri", size=9, italic=True, color="555555")

        r0 = 4
        headers = spec["headers"]
        for c_idx, h in enumerate(headers, start=1):
            cell = ws.cell(row=r0, column=c_idx, value=h)
            cell.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
            cell.fill = head_fill
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = border_hdr
        ws.row_dimensions[r0].height = 28

        fmts = spec.get("formats", {})
        for row_offset, rvals in enumerate(spec["rows"]):
            r = r0 + 1 + row_offset
            is_total = bool(spec.get("total_last") and row_offset == len(spec["rows"]) - 1)
            for c_idx, val in enumerate(rvals, start=1):
                cell = ws.cell(row=r, column=c_idx, value=val)
                cell.font = Font(name="Calibri", size=10, bold=is_total, color="111111")
                if is_total:
                    cell.fill = tot_fill
                elif row_offset % 2 == 1:
                    cell.fill = zebra_fill
                cell.border = border_cell
                if c_idx in fmts:
                    cell.number_format = fmts[c_idx]
                    cell.alignment = Alignment(horizontal="right", vertical="center")
                else:
                    cell.alignment = Alignment(horizontal="left", vertical="center")
            ws.row_dimensions[r].height = 19

        for i, w_col in enumerate(spec["widths"]):
            col = chr(65 + i) if i < 26 else "A" + chr(65 + i - 26)
            ws.column_dimensions[col].width = w_col
        ws.freeze_panes = "A5"
        ws.views.sheetView[0].showGridLines = True
    wb.save(path)


def build(target_dir, world=None):
    os.makedirs(target_dir, exist_ok=True)
    w = world if world is not None else core.simulate_world(core.SEED)
    rng = np.random.default_rng(core.SEED + 77)

    n = core.N_CONTAINERS
    n_sh = 3 * core.N_DAYS
    n_portal_days = int(w["portal_confirmed"].shape[2])

    # 1. Crosswalk
    store_canonical = [f"STR-{dc}-{k:03d}" for dc in core.DCS for k in range(1, 21)]
    store_legacy_map = {}
    xwalk_rows = []
    for idx_s, sc in enumerate(store_canonical):
        if idx_s % 3 == 0:
            leg = f"DE-RET-{1000 + idx_s}"
            store_legacy_map[sc] = leg
            xwalk_rows.append(("RETAIL_STORE", leg, sc, "2025-11-01"))

    carriers_canonical = [
        "CAR-ELBE-01", "CAR-WESER-02", "CAR-NORD-03", "CAR-HEIDE-04",
        "CAR-HARZ-05", "CAR-EMSLAND-06", "CAR-HANS-07", "CAR-MITTE-08",
    ]
    carrier_legacy_map = {
        "CAR-ELBE-01": "TRK-ELB-91",
        "CAR-WESER-02": "TRK-WSR-92",
        "CAR-NORD-03": "TRK-NRD-93",
        "CAR-HEIDE-04": "TRK-HDE-94",
    }
    for canon, leg in carrier_legacy_map.items():
        xwalk_rows.append(("DRAYAGE_CARRIER", leg, canon, "2025-09-15"))

    with open(os.path.join(target_dir, FILES["crosswalk"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["entity_type", "legacy_code", "canonical_code", "effective_from"])
        wr.writerows(xwalk_rows)

    # 2. SKU Thermal Catalog (180 SKUs; pallet weights aligned with ~23.8 t net payload per 20-22 pallet reefer)
    skus = []
    skus_by_zone = {0: [], 1: [], 2: []}
    cpp_choices = [40, 48, 56, 60, 64, 72, 80, 96]
    sku_counter = 1
    for z_idx, z_code in enumerate(core.ZONES):
        fams = PRODUCE_BY_ZONE[z_code]
        for k in range(60):
            fam_name, hs_code = fams[k % len(fams)]
            sku_id = f"WF-{z_code}-{sku_counter:03d}"
            sku_counter += 1
            cpp = int(cpp_choices[int(rng.integers(0, len(cpp_choices)))])
            ppr = int(rng.choice([20, 22], p=[0.60, 0.40]))
            net_kg = int(rng.integers(1040, 1210))
            rec = {
                "sku_id": sku_id,
                "produce_family": fam_name,
                "hs_code": hs_code,
                "thermal_zone": z_code,
                "cases_per_pallet": cpp,
                "pallets_per_40ft_reefer": ppr,
                "std_net_kg_per_pallet": net_kg,
            }
            skus.append(rec)
            skus_by_zone[z_idx].append(rec)

    with open(os.path.join(target_dir, FILES["skus"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow([
            "sku_id", "produce_family", "thermal_zone", "cases_per_pallet",
            "pallets_per_40ft_reefer", "std_net_kg_per_pallet",
        ])
        for s in skus:
            wr.writerow([
                s["sku_id"], s["produce_family"], s["thermal_zone"], s["cases_per_pallet"],
                s["pallets_per_40ft_reefer"], s["std_net_kg_per_pallet"],
            ])

    # 3. DC Chamber Register & Aggregate Daily DC Inventory
    with open(os.path.join(target_dir, FILES["chambers"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["dc_id", "thermal_zone", "setpoint_c", "pallet_bay_capacity", "opening_pallets_2026_01_01"])
        for d_idx, dc in enumerate(core.DCS):
            for z_idx, zc in enumerate(core.ZONES):
                wr.writerow([
                    dc, zc, ZONE_SETPOINTS[zc],
                    int(w["dc_caps"][d_idx, z_idx]),
                    int(w["chamber_opening"][d_idx, z_idx]),
                ])

    with open(os.path.join(target_dir, FILES["dc_inv"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["date_iso", "dc_id", "total_pallets_on_hand", "total_pallet_capacity", "total_util_pct"])
        for t in range(core.N_DAYS):
            d_str = (BASE_DATE + dt.timedelta(days=t)).isoformat()
            for d_idx, dc in enumerate(core.DCS):
                st = int(w["dc_total_stock"][d_idx, t])
                cap = int(w["dc_total_cap"][d_idx])
                wr.writerow([d_str, dc, st, cap, f"{100.0 * st / cap:.3f}"])

    # 4. Terminal Yard Daily
    with open(os.path.join(target_dir, FILES["port_yard"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["date_iso", "port_id", "reefer_yard_util_pct", "total_lifts_teu", "crane_hours"])
        for t in range(core.N_DAYS):
            d_str = (BASE_DATE + dt.timedelta(days=t)).isoformat()
            for p_idx, port in enumerate(core.PORTS):
                u = float(w["port_yard_util"][p_idx, t])
                base_lifts = [1850, 1620, 740][p_idx]
                lifts = int(round(base_lifts * (0.72 + 0.52 * u) + rng.normal(0, 35)))
                crane_h = round(lifts / rng.uniform(26.5, 29.5), 1)
                wr.writerow([d_str, port, f"{100.0 * u:.3f}", lifts, f"{crane_h:.1f}"])

    # 5. Warehouse Pallet Movements (~180k rows, Large Messy CSV #1)
    stores_by_dc = {d_idx: [f"STR-{dc}-{k:03d}" for k in range(1, 21)] for d_idx, dc in enumerate(core.DCS)}
    mv_path = os.path.join(target_dir, FILES["pallets"])
    mv_count = 0
    mv_superseded = 0
    with open(mv_path, "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow([
            "movement_id", "move_date", "dc_id", "sku_id", "direction",
            "quantity", "unit", "store_code", "edi_batch_id", "extract_version",
        ])
        mid = 1
        for t in range(core.N_DAYS):
            cur_d = BASE_DATE + dt.timedelta(days=t)
            iso_d = cur_d.isoformat()
            de_d = cur_d.strftime("%d.%m.%Y")
            for d_idx, dc in enumerate(core.DCS):
                dc_stores = stores_by_dc[d_idx]
                batch_base = f"WMS-{dc}-{cur_d.strftime('%Y%m%d')}"
                for z_idx in range(3):
                    z_skus = skus_by_zone[z_idx]
                    in_tot = int(w["pallet_in"][d_idx, z_idx, t])
                    out_tot = int(w["pallet_out"][d_idx, z_idx, t])

                    in_parts = _split_int_total(in_tot, int(rng.integers(12, 16)), rng)
                    out_parts = _split_int_total(out_tot, int(rng.integers(24, 30)), rng)

                    in_sku_idxs = rng.choice(len(z_skus), size=len(in_parts), replace=True)
                    for p_qty, sk_i in zip(in_parts, in_sku_idxs):
                        sk = z_skus[int(sk_i)]
                        m_id = f"WMV-{mid:07d}"
                        mid += 1
                        use_case = rng.random() < 0.34
                        unit = "CASE" if use_case else "PALLET"
                        qty = int(p_qty * sk["cases_per_pallet"]) if use_case else int(p_qty)
                        d_fmt = de_d if (rng.random() < 0.38) else iso_d
                        if rng.random() < 0.024:
                            step = sk["cases_per_pallet"] if use_case else 1
                            old_qty = max(1, qty + int(rng.choice([-2, -1, 1, 2]) * step))
                            wr.writerow([m_id, d_fmt, dc, sk["sku_id"], "IN", old_qty, unit, "", batch_base + "-R1", 1])
                            wr.writerow([m_id, d_fmt, dc, sk["sku_id"], "IN", qty, unit, "", batch_base + "-R2", 2])
                            mv_superseded += 1
                            mv_count += 2
                        else:
                            wr.writerow([m_id, d_fmt, dc, sk["sku_id"], "IN", qty, unit, "", batch_base + "-R1", 1])
                            mv_count += 1

                    out_sku_idxs = rng.choice(len(z_skus), size=len(out_parts), replace=True)
                    out_st_idxs = rng.integers(0, len(dc_stores), size=len(out_parts))
                    for p_qty, sk_i, st_i in zip(out_parts, out_sku_idxs, out_st_idxs):
                        sk = z_skus[int(sk_i)]
                        m_id = f"WMV-{mid:07d}"
                        mid += 1
                        use_case = rng.random() < 0.36
                        unit = "CASE" if use_case else "PALLET"
                        qty = int(p_qty * sk["cases_per_pallet"]) if use_case else int(p_qty)
                        d_fmt = de_d if (rng.random() < 0.38) else iso_d
                        st_canon = dc_stores[int(st_i)]
                        st_out = store_legacy_map[st_canon] if (st_canon in store_legacy_map and rng.random() < 0.55) else st_canon
                        if rng.random() < 0.024:
                            step = sk["cases_per_pallet"] if use_case else 1
                            old_qty = max(1, qty + int(rng.choice([-1, 1, 2]) * step))
                            wr.writerow([m_id, d_fmt, dc, sk["sku_id"], "OUT", old_qty, unit, st_out, batch_base + "-R1", 1])
                            wr.writerow([m_id, d_fmt, dc, sk["sku_id"], "OUT", qty, unit, st_out, batch_base + "-R2", 2])
                            mv_superseded += 1
                            mv_count += 2
                        else:
                            wr.writerow([m_id, d_fmt, dc, sk["sku_id"], "OUT", qty, unit, st_out, batch_base + "-R1", 1])
                            mv_count += 1

    # 6. Rail Shuttle Departures (daily multi-consist corridor blocks; realistic <=38 wagons / <=2,000 t per BR-193 consist)
    is_rail = w["cont_is_rail"]
    lot_bip = w["lot_bip"]
    cont_ched = w["cont_ched"]
    cont_shuttle = w["cont_shuttle"]
    rolled_flag = w["cont_rolled_rail"]
    cont_rail_excess = w["cont_rail_excess"] + w["obs_phyto_sibling_tms_rail"]
    assert np.isclose(
        cont_rail_excess.sum(),
        w["obs_phyto_sibling_tms_rail"].sum() + w["obs_rail_roll_days_sh"].sum() + w["obs_rail_base_sh"].sum(),
        atol=1e-6,
    )

    locos = [f"NBI-BR193-{201 + k}" for k in range(32)]
    shuttle_jitter_min = rng.integers(-22, 26, size=n_sh)
    shuttle_dep_ts_arr = [
        _shuttle_dep_ts(int(w["shuttle_port"][s]), int(w["shuttle_day"][s]), int(shuttle_jitter_min[s]))
        for s in range(n_sh)
    ]

    with open(os.path.join(target_dir, FILES["shuttles"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow([
            "shuttle_id", "port_id", "departure_ts_utc", "consists_dispatched",
            "contracted_wf_slots", "booked_wf_slots", "loaded_wf_slots", "wf_standby_rolled",
            "train_wagon_count", "train_total_gross_tonnes", "lead_loco_id",
        ])
        for s in range(n_sh):
            p_idx = int(w["shuttle_port"][s])
            d_idx = int(w["shuttle_day"][s])
            booked = int(w["wf_booked_slots_sh"][s])
            contracted = booked + int(rng.integers(0, 4))
            wagons = int(w["train_wagon_count_sh"][s])
            consists = max(1, int(math.ceil(wagons / 38.0)))
            wr.writerow([
                _shuttle_id(p_idx, d_idx),
                core.PORTS[p_idx],
                _fmt_utc(shuttle_dep_ts_arr[s]),
                consists,
                contracted,
                booked,
                int(w["wf_actual_loaded_sh"][s]),
                int(w["wf_standby_rolled_total_sh"][s]),
                wagons,
                f"{float(w['train_gross_tonnes_sh'][s]):.2f}",
                locos[int(rng.integers(0, len(locos)))],
            ])

    # 7. Customs Consignment BoL Register (24,000 rows; gross weight <= 30,480 kg ISO 40' HC limit, mean ~28.5 t)
    cont_ids = [f"WFRE{2600001 + i}" for i in range(n)]
    vessel_ids = [f"VSL-NS26-{v + 1:04d}" for v in range(core.N_VESSELS)]
    with open(os.path.join(target_dir, FILES["consignments"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow([
            "container_id", "vessel_id", "ched_lot_id", "origin_country",
            "hs_commodity_code", "declared_net_kg", "reefer_tare_kg",
        ])
        for i in range(n):
            z_idx = int(w["cont_zone"][i])
            z_code = core.ZONES[z_idx]
            fams = PRODUCE_BY_ZONE[z_code]
            _, hs_code = fams[int(rng.integers(0, len(fams)))]
            orig = ORIGINS_BY_ZONE[z_code][int(rng.integers(0, len(ORIGINS_BY_ZONE[z_code])))]
            tare_kg = int(round(np.clip(4700 + rng.normal(0, 55), 4520, 4880)))
            net_kg = int(round(np.clip(23820 + rng.normal(0, 920), 20800, 30480 - tare_kg)))
            wr.writerow([
                cont_ids[i],
                vessel_ids[int(w["cont_vessel"][i])],
                f"CHEDPP-DE-2026-{int(cont_ched[i]) + 1:05d}",
                orig,
                hs_code,
                net_kg,
                tare_kg,
            ])

    # 8. Build Container Milestones in memory first (strict forward chronology + interleaved VOID rows)
    vessel_base_hour = rng.uniform(3.5, 9.5, size=core.N_VESSELS)
    cont_carriers = [carriers_canonical[int(rng.integers(0, len(carriers_canonical)))] for _ in range(n)]

    unload_ts_utc_arr = [None] * n
    depot_arr_ts_utc_arr = [None] * n
    empty_gate_ts_utc_arr = [None] * n
    lot_sampled_bip_ts = {}

    live_milestone_blocks = []  # list of lists of rows (1 or 2 rows per container)
    ms_superseded_count = 0

    for i in range(n):
        v_idx = int(w["cont_vessel"][i])
        p_idx = int(w["cont_port"][i])
        d_idx = int(w["cont_day"][i])
        dc_idx = int(w["cont_dc"][i])
        z_idx = int(w["cont_zone"][i])
        l_idx = int(w["cont_line"][i])
        rail = bool(is_rail[i])

        dis_d = BASE_DATE + dt.timedelta(days=d_idx)
        dis_h = float(vessel_base_hour[v_idx] + rng.uniform(0.0, 2.0))
        dis_ts = dt.datetime(dis_d.year, dis_d.month, dis_d.day, tzinfo=UTC) + dt.timedelta(hours=dis_h)

        ex_berth = float(w["obs_vessel_berth"][i])
        ex_edi = float(w["obs_edi_docs"][i])
        ex_yard = float(w["obs_term_yard_hold"][i])
        ex_phyto = float(w["obs_phyto_hold_direct"][i])
        ex_rail = float(cont_rail_excess[i])
        ex_dc = float(w["obs_dc_dock_wait"][i])
        ex_dray = float(w["obs_dray_empty_hold"][i])
        ex_depot = float(w["obs_depot_turnaway"][i])
        ex_tot = ex_berth + ex_edi + ex_yard + ex_phyto + ex_rail + ex_dc + ex_dray + ex_depot

        eta_ts = dis_ts - dt.timedelta(hours=ex_berth * 24.0)
        cust_ts = dis_ts + dt.timedelta(hours=FREE_TIME_H["edi"] + ex_edi * 24.0)
        ready_ts = cust_ts + dt.timedelta(hours=FREE_TIME_H["port_yard"] + ex_yard * 24.0)
        bip_ts = ready_ts + dt.timedelta(hours=ex_phyto * 24.0)

        if bool(w["cont_bip_sampled"][i]):
            lot_sampled_bip_ts[int(cont_ched[i])] = bip_ts

        if rail:
            p_sh = _shuttle_id(p_idx, d_idx)
            act_day = d_idx + (2 if bool(rolled_flag[i]) else 0)
            a_sh = _shuttle_id(p_idx, act_day)
            rail_dep_ts = bip_ts + dt.timedelta(hours=FREE_TIME_H["rail"] + ex_rail * 24.0)
            rail_dep_str = _fmt_utc(rail_dep_ts)
            min_dc_in_utc = rail_dep_ts + dt.timedelta(hours=float(rng.uniform(4.0, 6.5)))
        else:
            p_sh = ""
            a_sh = ""
            rail_dep_ts = None
            rail_dep_str = ""
            min_dc_in_utc = bip_ts + dt.timedelta(hours=float(rng.uniform(3.0, 5.5)))

        dc_stage_td = dt.timedelta(hours=FREE_TIME_H["dc_dock"] + ex_dc * 24.0)
        min_unload_utc = min_dc_in_utc + dc_stage_td

        u_day = BASE_DATE + dt.timedelta(days=int(w["cont_unload_day"][i]))
        u_day_start = dt.datetime(u_day.year, u_day.month, u_day.day, 7, 0, 0, tzinfo=BERLIN).astimezone(UTC)
        u_day_pref_end = dt.datetime(u_day.year, u_day.month, u_day.day, 21, 30, 0, tzinfo=BERLIN).astimezone(UTC)
        u_day_hard_end = dt.datetime(u_day.year, u_day.month, u_day.day, 23, 50, 0, tzinfo=BERLIN).astimezone(UTC)

        lo_utc = max(min_unload_utc, u_day_start)
        if lo_utc < u_day_pref_end:
            span_s = (u_day_pref_end - lo_utc).total_seconds()
            unload_utc = lo_utc + dt.timedelta(seconds=float(rng.uniform(0.0, span_s)))
        else:
            assert lo_utc <= u_day_hard_end, f"Chronology violation on container {i}: {lo_utc} > {u_day_hard_end}"
            span_s = max(60.0, (u_day_hard_end - lo_utc).total_seconds())
            unload_utc = lo_utc + dt.timedelta(seconds=float(rng.uniform(0.0, span_s)))

        unload_local = unload_utc.astimezone(BERLIN)
        assert unload_local.date() == u_day, f"Unload date drift on {i}: {unload_local.date()} != {u_day}"
        dc_in_utc = unload_utc - dc_stage_td
        assert dc_in_utc >= (rail_dep_ts if rail else bip_ts), f"Inland arrival before port exit on {i}"
        dc_in_local = dc_in_utc.astimezone(BERLIN)

        depot_arr_utc = unload_utc + dt.timedelta(hours=FREE_TIME_H["dray_empty"] + ex_dray * 24.0)
        empty_in_utc = depot_arr_utc + dt.timedelta(hours=ex_depot * 24.0)

        unload_ts_utc_arr[i] = unload_utc
        depot_arr_ts_utc_arr[i] = depot_arr_utc
        empty_gate_ts_utc_arr[i] = empty_in_utc

        stage_map = [
            ("VESSEL_LATE", ex_berth),
            ("EDI_DOC_HOLD", ex_edi),
            ("TERM_YARD_HOLD", ex_yard),
            ("PHYTO_HOLD", ex_phyto),
            ("RAIL_CAP_ROLL", ex_rail),
            ("DC_DOCK_WAIT", ex_dc),
            ("DRAY_EMPTY_HOLD", ex_dray),
            ("DEPOT_TURN_AWAY", ex_depot),
        ]
        prim_code = max(stage_map, key=lambda kv: kv[1])[0]

        row_live = [
            cont_ids[i], vessel_ids[v_idx], core.PORTS[p_idx], core.DCS[dc_idx],
            core.ZONES[z_idx], core.LINES[l_idx], "RAIL" if rail else "TRUCK",
            p_sh, a_sh,
            _fmt_utc(eta_ts), _fmt_utc(dis_ts), _fmt_utc(cust_ts),
            _fmt_utc(ready_ts), _fmt_utc(bip_ts), rail_dep_str,
            _fmt_berlin(dc_in_local), _fmt_berlin(unload_local),
            _fmt_utc(depot_arr_utc), _fmt_utc(empty_in_utc),
            f"{ex_berth:.6f}", f"{ex_edi:.6f}", f"{ex_yard:.6f}",
            f"{ex_phyto:.6f}", f"{ex_rail:.6f}", f"{ex_dc:.6f}",
            f"{ex_dray:.6f}", f"{ex_depot:.6f}", f"{ex_tot:.6f}",
            prim_code, 1 if bool(w["cont_bip_sampled"][i]) else 0, "SETTLED", 1,
        ]

        if rng.random() < 0.0135:
            rev_delta = float(rng.uniform(0.08, 0.34))
            dt_shift = dt.timedelta(hours=rev_delta * 24.0)
            row_v1 = list(row_live)
            # Preliminary v1 EDI carried an unrevised yard gate-ready stamp consistent with its excess column
            row_v1[12] = _fmt_utc(ready_ts + dt_shift)
            row_v1[13] = _fmt_utc(bip_ts + dt_shift)
            if rail:
                row_v1[14] = _fmt_utc(rail_dep_ts + dt_shift)
            row_v1[15] = _fmt_berlin(dc_in_utc + dt_shift)
            row_v1[16] = _fmt_berlin(unload_utc + dt_shift)
            row_v1[17] = _fmt_utc(depot_arr_utc + dt_shift)
            row_v1[18] = _fmt_utc(empty_in_utc + dt_shift)
            row_v1[21] = f"{ex_yard + rev_delta:.6f}"
            row_v1[27] = f"{ex_tot + rev_delta:.6f}"
            row_v1[31] = 1
            row_live[31] = 2
            live_milestone_blocks.append([row_v1, row_live])
            ms_superseded_count += 1
        else:
            live_milestone_blocks.append([row_live])

    # Build 190 realistic VOID EDI test rows with internally consistent timestamps and interleave them
    void_rows = []
    for v_k in range(190):
        ref_i = int(rng.integers(0, n))
        d_v = BASE_DATE + dt.timedelta(days=int(rng.integers(0, core.N_DAYS - 5)))
        ts0 = dt.datetime(d_v.year, d_v.month, d_v.day, tzinfo=UTC) + dt.timedelta(
            hours=int(rng.integers(4, 18)), minutes=int(rng.integers(1, 59)), seconds=int(rng.integers(1, 59))
        )
        vy = round(float(rng.uniform(0.15, 0.85)), 6)
        vd = round(float(rng.uniform(0.10, 0.65)), 6)
        v_cust = ts0 + dt.timedelta(hours=6.0)
        v_ready = v_cust + dt.timedelta(hours=24.0 + vy * 24.0)
        v_dc_in = v_ready + dt.timedelta(hours=float(rng.uniform(4.0, 9.0)))
        v_unload = v_dc_in + dt.timedelta(hours=4.0)
        v_dep_arr = v_unload + dt.timedelta(hours=24.0 + vd * 24.0)
        void_rows.append([
            f"WFRE99{v_k + 1:05d}", vessel_ids[int(w["cont_vessel"][ref_i])],
            core.PORTS[int(w["cont_port"][ref_i])], core.DCS[int(w["cont_dc"][ref_i])],
            core.ZONES[int(w["cont_zone"][ref_i])], core.LINES[int(w["cont_line"][ref_i])],
            "TRUCK", "", "",
            _fmt_utc(ts0), _fmt_utc(ts0), _fmt_utc(v_cust),
            _fmt_utc(v_ready), _fmt_utc(v_ready), "",
            _fmt_berlin(v_dc_in), _fmt_berlin(v_unload),
            _fmt_utc(v_dep_arr), _fmt_utc(v_dep_arr),
            "0.000000", "0.000000", f"{vy:.6f}", "0.000000", "0.000000", "0.000000",
            f"{vd:.6f}", "0.000000", f"{vy + vd:.6f}",
            "TERM_YARD_HOLD" if vy >= vd else "DRAY_EMPTY_HOLD", 0, "VOID", 1,
        ])

    void_insert_slots = sorted(rng.integers(0, n, size=len(void_rows)).tolist())
    void_by_slot = {}
    for sl, vr in zip(void_insert_slots, void_rows):
        void_by_slot.setdefault(sl, []).append(vr)

    ms_rows_written = 0
    ms_void_count = len(void_rows)
    with open(os.path.join(target_dir, FILES["milestones"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow([
            "container_id", "vessel_id", "port_id", "dc_id", "thermal_zone", "shipping_line_id",
            "mode", "planned_shuttle_id", "departed_shuttle_id",
            "scheduled_eta_utc", "discharge_ts_utc", "customs_doc_ts_utc",
            "port_gate_ready_ts_utc", "bip_release_ts_utc", "rail_depart_ts_utc",
            "dc_gate_in_ts_cet", "unload_complete_ts_cet",
            "depot_gate_arr_ts_utc", "empty_gate_in_ts_utc",
            "excess_berth_cdays", "excess_edi_cdays", "excess_port_yard_cdays",
            "excess_phyto_cdays", "excess_rail_cdays", "excess_dc_dock_cdays",
            "excess_dray_empty_cdays", "excess_depot_gate_cdays", "excess_cdays_total",
            "tms_primary_exception_code", "bip_sampled_ind", "record_status", "extract_version",
        ])
        for i in range(n):
            for r in live_milestone_blocks[i]:
                wr.writerow(r)
                ms_rows_written += 1
            if i in void_by_slot:
                for vr in void_by_slot[i]:
                    wr.writerow(vr)
                    ms_rows_written += 1

    # 9. BIP Inspection Notices (JSONL; lab_release_ts_utc aligned to sampled container bip_release_ts_utc)
    exam_types = ["PHYSICAL_IDENTITY_SAMPLE", "PRIORITY_PEST_LAB", "COLD_CHAIN_PHYTOSANITARY"]
    bip_path = os.path.join(target_dir, FILES["bip_notices"])
    bip_count = 0
    used_traces_ids = set()
    with open(bip_path, "w", encoding="utf-8") as f:
        for lid in range(len(lot_bip)):
            if not lot_bip[lid]:
                continue
            p_idx = int(w["lot_port"][lid])
            d_idx = int(w["lot_day"][lid])
            s_idx = p_idx * core.N_DAYS + d_idx
            dep_ts = shuttle_dep_ts_arr[s_idx]
            lead_h = float(w["lot_lead_hours"][lid])
            notice_ts = dep_ts - dt.timedelta(hours=lead_h)
            samp_bip = lot_sampled_bip_ts.get(lid)
            if samp_bip is not None:
                release_ts = max(notice_ts + dt.timedelta(hours=4.0), samp_bip - dt.timedelta(minutes=int(rng.integers(3, 25))))
            else:
                release_ts = notice_ts + dt.timedelta(hours=float(rng.uniform(16.0, 30.0)))
            ref_num = int(rng.integers(100000, 999999))
            while ref_num in used_traces_ids:
                ref_num = int(rng.integers(100000, 999999))
            used_traces_ids.add(ref_num)
            rec = {
                "ched_lot_id": f"CHEDPP-DE-2026-{lid + 1:05d}",
                "port_id": core.PORTS[p_idx],
                "exam_notice_ts_utc": _fmt_utc(notice_ts),
                "lab_release_ts_utc": _fmt_utc(release_ts),
                "exam_type": exam_types[int(w["lot_zone"][lid])],
                "lot_container_count": int(w["lot_size"][lid]),
                "traces_ref_no": f"TRACES-NT-{core.PORTS[p_idx]}-2026-{ref_num}",
            }
            f.write(json.dumps(rec, separators=(",", ":")) + "\n")
            bip_count += 1

    # 10. Depot Turn-in Log (~25,350 rows, Large Messy CSV #3; randomized revision lag)
    ti_rows = 0
    ti_turnaways = 0
    ti_superseded = 0
    with open(os.path.join(target_dir, FILES["turnin"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow([
            "gate_event_id", "container_id", "depot_port_id", "shipping_line_id",
            "carrier_code", "arrival_ts_cet", "gate_status", "turnaway_delay_hours", "extract_version",
        ])
        gid = 1
        for i in range(n):
            p_code = core.PORTS[int(w["cont_port"][i])]
            l_code = core.LINES[int(w["cont_line"][i])]
            c_canon = cont_carriers[i]
            c_out = carrier_legacy_map[c_canon] if (c_canon in carrier_legacy_map and rng.random() < 0.45) else c_canon
            ex_dep = float(w["obs_depot_turnaway"][i])
            if ex_dep > 0.0:
                ev_id1 = f"DGT-{gid:07d}"
                gid += 1
                wr.writerow([
                    ev_id1, cont_ids[i], p_code, l_code, c_out,
                    _fmt_berlin(depot_arr_ts_utc_arr[i]), "TURN_AWAY", f"{ex_dep * 24.0:.4f}", 1,
                ])
                ti_turnaways += 1
                ti_rows += 1
            ev_id2 = f"DGT-{gid:07d}"
            gid += 1
            row_acc = [
                ev_id2, cont_ids[i], p_code, l_code, c_out,
                _fmt_berlin(empty_gate_ts_utc_arr[i]), "ACCEPTED", "0.0000", 1,
            ]
            if rng.random() < 0.018:
                lag_m = int(rng.integers(6, 38))
                row_old = list(row_acc)
                row_old[5] = _fmt_berlin(empty_gate_ts_utc_arr[i] - dt.timedelta(minutes=lag_m))
                row_old[8] = 1
                row_acc[8] = 2
                wr.writerow(row_old)
                wr.writerow(row_acc)
                ti_superseded += 1
                ti_rows += 2
            else:
                wr.writerow(row_acc)
                ti_rows += 1

    # 11. Depot Portal Requests (379 days: 2026-01-01 to 2027-01-14; ZERO container_id, ZERO Dec 31 clamp!)
    with open(os.path.join(target_dir, FILES["portal"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["date_iso", "depot_port_id", "shipping_line_id", "confirmed_bookings", "quota_closed_rejections"])
        for t in range(n_portal_days):
            d_str = (BASE_DATE + dt.timedelta(days=t)).isoformat()
            for p_idx, p_code in enumerate(core.PORTS):
                for l_idx, l_code in enumerate(core.LINES):
                    wr.writerow([
                        d_str, p_code, l_code,
                        int(w["portal_confirmed"][p_idx, l_idx, t]),
                        int(w["portal_rejected"][p_idx, l_idx, t]),
                    ])

    # 12. Carrier Dispute Close-Out 2026 (XLSX #1)
    obs_by_cause_c = {
        "vessel_berth": w["obs_vessel_berth"],
        "edi_docs": w["obs_edi_docs"],
        "reefer_plug": w["obs_term_yard_hold"],
        "coldstore_dock": w["obs_dc_dock_wait"],
        "phyto_insp": w["obs_phyto_hold_direct"],
        "drayage_carrier": w["obs_dray_empty_hold"],
        "empty_depot": w["obs_depot_turnaway"],
    }
    settle_ratio = {
        "vessel_berth": 0.98, "edi_docs": 0.96, "reefer_plug": 0.97, "coldstore_dock": 0.95,
        "rail_handoff": 0.94, "phyto_insp": 0.97, "drayage_carrier": 0.96, "empty_depot": 0.95,
    }
    disp_summary = []
    disp_detail = []
    tot_claimed, tot_settled, tot_eur = 0.0, 0.0, 0.0
    for c_id in ("vessel_berth", "edi_docs", "reefer_plug", "coldstore_dock",
                 "rail_handoff", "phyto_insp", "drayage_carrier", "empty_depot"):
        rat = settle_ratio[c_id]
        claimed = float(cont_rail_excess.sum()) if c_id == "rail_handoff" else float(obs_by_cause_c[c_id].sum())
        settled = claimed * rat
        eur_val = settled * core.TARIFF_EUR[c_id]
        tot_claimed += claimed
        tot_settled += settled
        tot_eur += eur_val
        disp_summary.append([
            c_id, round(claimed, 2), round(settled, 2), round(100.0 * rat, 1),
            core.TARIFF_EUR[c_id], round(eur_val, 2),
        ])
        for p_idx, p_code in enumerate(core.PORTS):
            for q_idx in range(4):
                m_pq = (w["cont_port"] == p_idx) & (w["cont_quarter"] == q_idx)
                cl_pq = float(cont_rail_excess[m_pq].sum()) if c_id == "rail_handoff" else float(obs_by_cause_c[c_id][m_pq].sum())
                st_pq = cl_pq * rat
                disp_detail.append([
                    f"2026-Q{q_idx + 1}", p_code, c_id,
                    round(cl_pq, 2), round(st_pq, 2), round(st_pq * core.TARIFF_EUR[c_id], 2),
                ])
    disp_summary.append([
        "TOTAL", round(tot_claimed, 2), round(tot_settled, 2),
        round(100.0 * tot_settled / tot_claimed, 1), "", round(tot_eur, 2),
    ])

    _write_xlsx_styled(
        os.path.join(target_dir, FILES["disputes"]),
        [
            {
                "name": "Annual_Closeout_Summary",
                "title": "Weserfrucht Import GmbH - 2026 Commercial Dispute and Demurrage Settlement Summary",
                "subtitle": "Settled counterparty invoices and documentary credit claims by TMS stage category (as of 12 January 2027)",
                "headers": [
                    "TMS Cause Category", "Claimed Excess C-Days", "Settled Documentary C-Days",
                    "Settlement Rate (%)", "Daily Tariff (EUR)", "Settled Exposure (EUR)",
                ],
                "rows": disp_summary,
                "widths": [22, 22, 24, 19, 18, 24],
                "formats": {2: "#,##0.00", 3: "#,##0.00", 4: "0.0", 5: "#,##0", 6: "#,##0.00"},
                "total_last": True,
            },
            {
                "name": "Port_Quarter_Detail",
                "title": "2026 Documentary Settlement Ledger by Port and Calendar Quarter",
                "subtitle": "Counterparty invoice reconciliation under 2026 carrier service agreements",
                "headers": ["Quarter", "Port", "TMS Cause Category", "Claimed C-Days", "Settled C-Days", "Settled EUR"],
                "rows": disp_detail,
                "widths": [14, 10, 22, 18, 18, 20],
                "formats": {4: "#,##0.00", 5: "#,##0.00", 6: "#,##0.00"},
                "total_last": False,
            },
        ],
    )

    # 13. Import Plan 2027
    plan_rows = []
    for p in core.PORTS:
        plan_rows.append(("port_volume_growth", p, "vol_growth_port", 1.00, core.PLAN_2027["vol_growth_port"][p], core.PLAN_2027["vol_growth_port"][p], "multiplier"))
    for p in core.PORTS:
        plan_rows.append(("port_berth_plugs", p, "plug_capacity_factor_2027", 1.00, core.PLAN_2027["plug_capacity_factor_2027"][p], core.PLAN_2027["plug_capacity_factor_2027"][p], "multiplier"))
    for z in core.ZONES:
        plan_rows.append(("coldstore_zone_plan", z, "dc_zone_load_factor_2027", 1.00, core.PLAN_2027["dc_zone_load_factor_2027"][z], core.PLAN_2027["dc_zone_load_factor_2027"][z], "multiplier"))
    for p in core.PORTS:
        plan_rows.append(("border_bip_schedule", p, "bip_sampling_factor_2027", 1.00, core.PLAN_2027["bip_sampling_factor_2027"][p], core.PLAN_2027["bip_sampling_factor_2027"][p], "multiplier"))
    plan_rows.append(("rail_fleet_plan", "NETWORK", "rail_fleet_factor_2027", 1.00, core.PLAN_2027["rail_fleet_factor_2027"], core.PLAN_2027["rail_fleet_factor_2027"], "multiplier"))
    plan_rows.append(("drayage_contract", "NETWORK", "dray_contract_factor_2027", 1.00, core.PLAN_2027["dray_contract_factor_2027"], core.PLAN_2027["dray_contract_factor_2027"], "multiplier"))
    for l in core.LINES:
        s26 = core.PLAN_2027["line_share_2026"][l]
        s27 = core.PLAN_2027["line_share_2027"][l]
        plan_rows.append(("ocean_line_mix", l, "line_volume_share", s26, s27, round(s27 / s26, 6), "share"))
    for l in core.LINES:
        lf = core.PLAN_2027["depot_load_factor_2027"][l]
        plan_rows.append(("empty_depot_plan", l, "depot_load_factor_2027", 1.00, lf, lf, "multiplier"))

    with open(os.path.join(target_dir, FILES["plan_2027"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["parameter_group", "entity_id", "metric_code", "value_2026", "value_2027", "multiplier_2027", "unit"])
        for r in plan_rows:
            wr.writerow([r[0], r[1], r[2], f"{r[3]:.4f}", f"{r[4]:.4f}", f"{r[5]:.6f}", r[6]])

    # 14. Distractor #1: North Sea Bunker Fuel Index 2026 (independent hub ETS spread)
    with open(os.path.join(target_dir, FILES["dist_bunker"]), "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["week_start_iso", "bunker_hub", "vlsfo_eur_per_tonne", "mgo_eur_per_tonne", "eu_ets_surcharge_eur_teu"])
        v_rot = 548.0
        for wk in range(52):
            wd = (BASE_DATE + dt.timedelta(days=wk * 7)).isoformat()
            v_rot = float(np.clip(v_rot + rng.normal(0.4, 9.5), 485.0, 645.0))
            v_ham = float(np.clip(v_rot + rng.uniform(10.0, 19.0), 498.0, 665.0))
            m_rot = v_rot + float(rng.uniform(118.0, 148.0))
            m_ham = v_ham + float(rng.uniform(122.0, 152.0))
            ets_rot = round(42.0 + 0.03 * (v_rot - 500.0) + float(rng.uniform(-1.5, 1.5)), 2)
            ets_ham = round(ets_rot + float(rng.uniform(1.05, 2.65)), 2)
            wr.writerow([wd, "ROTTERDAM", f"{v_rot:.2f}", f"{m_rot:.2f}", f"{ets_rot:.2f}"])
            wr.writerow([wd, "HAMBURG", f"{v_ham:.2f}", f"{m_ham:.2f}", f"{ets_ham:.2f}"])

    # 15. Distractor #2: German Autobahn LKW-Maut Rates 2026-2027 (XLSX #2)
    maut_rates = [
        ["Class 1 (Diesel Euro VI, >18t, 5+ axles)", "CO2-1", 0.348, 0.362, "+4.0%"],
        ["Class 2 (Low-Emission LNG, >18t, 5+ axles)", "CO2-2", 0.332, 0.345, "+3.9%"],
        ["Class 3 (HVO / Bio-Diesel Fleet, >18t, 5+ axles)", "CO2-3", 0.316, 0.328, "+3.8%"],
        ["Class 4 (Heavy Hybrid, >18t, 5+ axles)", "CO2-4", 0.254, 0.264, "+3.9%"],
        ["Class 5 (Zero-Emission BEV, >18t, 5+ axles)", "CO2-5", 0.087, 0.091, "+4.6%"],
    ]
    corridor_km = [
        ["BHV", "HAN", 174, 158, "A27 / A7"],
        ["BHV", "OSN", 168, 152, "A27 / A1"],
        ["BHV", "KAS", 318, 296, "A27 / A7"],
        ["BHV", "MAG", 295, 274, "A27 / A2"],
        ["HAM", "HAN", 156, 144, "A7"],
        ["HAM", "OSN", 214, 198, "A1"],
        ["HAM", "KAS", 308, 289, "A7"],
        ["HAM", "MAG", 248, 229, "A39 / A2"],
        ["WHV", "HAN", 218, 199, "A29 / A7"],
        ["WHV", "OSN", 162, 149, "A29 / A1"],
        ["WHV", "KAS", 342, 319, "A29 / A7"],
        ["WHV", "MAG", 336, 312, "A29 / A2"],
    ]
    _write_xlsx_styled(
        os.path.join(target_dir, FILES["dist_maut"]),
        [
            {
                "name": "LKW_Maut_Tariff_Schedule",
                "title": "Federal Autobahn LKW-Maut Road Toll Rates (2026-2027)",
                "subtitle": "Published toll schedule per kilometer by CO2 emission class for refrigerated heavy articulated vehicles",
                "headers": ["Vehicle Class", "CO2 Class", "2026 Rate (EUR/km)", "2027 Rate (EUR/km)", "YoY Change"],
                "rows": maut_rates,
                "widths": [42, 12, 20, 20, 14],
                "formats": {3: "0.000", 4: "0.000"},
                "total_last": False,
            },
            {
                "name": "Port_DC_Autobahn_Distances",
                "title": "North Sea Port to Inland Cold-Store Tollable Highway Distances",
                "subtitle": "Standard routing table maintained by Weserfrucht Transport Procurement",
                "headers": ["Port", "Cold Store DC", "Total Distance (km)", "Tollable Autobahn (km)", "Primary Route"],
                "rows": corridor_km,
                "widths": [10, 16, 20, 24, 18],
                "formats": {3: "#,##0", 4: "#,##0"},
                "total_last": False,
            },
        ],
    )

    return {
        "milestones_rows": ms_rows_written,
        "milestones_live": n,
        "milestones_void": ms_void_count,
        "milestones_superseded": ms_superseded_count,
        "pallets_rows": mv_count,
        "pallets_superseded": mv_superseded,
        "turnin_rows": ti_rows,
        "turnin_turnaways": ti_turnaways,
        "turnin_superseded": ti_superseded,
        "bip_notices": bip_count,
        "shuttles": n_sh,
        "portal_rows": 3 * 4 * n_portal_days,
    }
