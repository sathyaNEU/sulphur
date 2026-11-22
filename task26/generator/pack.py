"""Materialize the 19 operational dataset files under target/ from core.simulate() arrays (v2).

Every physical array comes directly from core.simulate() (seed 2622). Layer 1 ETL texture (superseded SCADA
re-export batches, legacy RTU date formatting on Raudfjord, Europe/Oslo CET/CEST vs CET standard alignment,
legacy DMS feeder IDs bridged by feeder_id_crosswalk.csv, kW/MW and kWh/MWh unit conventions, and benign summer
comms nulls) resolves deterministically back to the exact clean arrays.
"""
import csv
import datetime as dt
import os
import sqlite3
from zoneinfo import ZoneInfo

import numpy as np
from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side

import core as C

ORG = "Vesterdal Nett AS"
OSLO = ZoneInfo("Europe/Oslo")
UTC = dt.timezone.utc
CET_FIXED = dt.timezone(dt.timedelta(hours=1))
# Calendar year 2026 in Europe/Oslo standard time: 2026-01-01 00:00+01:00 == 2025-12-31 23:00Z
BASE_UTC = dt.datetime(2025, 12, 31, 23, 0, tzinfo=UTC)

PEOPLE = {
    "head": "Espen Eide",
    "scada": "Mona Thomassen",
    "asset": "Eli Hanssen",
    "metering": "Ida Jensen",
    "analyst": "Solveig Johansen",
    "field": "Astrid Pettersen",
}

ALPHA_SUBS = tuple(sorted(C.ALL_SUBS))

REGIONS = {
    "Drangvik": "Fjord Vest",
    "Fossheim": "Elvedal",
    "Hestmark": "Indre Dal",
    "Kvernholm": "Kyst Nord",
    "Lindberg": "Industri Vest",
    "Malmnes": "Havneby",
    "Ostervik": "Sentrum Ost",
    "Raudfjord": "Nordfjord",
    "Solberg": "Solberg Vest",
    "Svarthaug": "Sunnmark",
    "Tverrli": "Fjellbygd",
}

MUNICIPALITIES = {
    "Drangvik": "Drangvik Kommune",
    "Fossheim": "Fossheim Kommune",
    "Hestmark": "Hestmark Kommune",
    "Kvernholm": "Kvernholm Kommune",
    "Lindberg": "Lindberg Kommune",
    "Malmnes": "Malmnes Kommune",
    "Ostervik": "Ostervik Kommune",
    "Raudfjord": "Raudfjord Kommune",
    "Solberg": "Solberg Kommune",
    "Svarthaug": "Sunnmark Kommune",
    "Tverrli": "Tverrli Kommune",
}

FILES = {
    "scada_sub": "scada_substation_hourly_2026.csv",
    "gsp_v": "gsp_66kv_voltages_2026.csv",
    "cor_lines": "subtransmission_66kv_lines.csv",
    "scada_fdr": "feeder_scada_hourly_2026.csv",
    "fdr_m15": "feeder_demand_registers_monthly_2026.csv",
    "bus_vph": "substation_phase_bus_voltages_2026.csv",
    "ami_db": "ami_lateral_telemetry_2026.db",
    "ref_pq": "pq_archive_15min_2026.csv",
    "ref_tracer": "commissioning_phase_log_2025.csv",
    "rev_xlsx": "revenue_meter_monthly_2026.xlsx",
    "tx_xlsx": "substation_transformer_register.xlsx",
    "gis_lat": "gis_lateral_connectivity_2026.csv",
    "xwalk": "feeder_id_crosswalk.csv",
    "class_pf": "engineering_manual_class_pf.csv",
    "ctx_2025": "substation_annual_energy_summary_2025.xlsx",
    "dist_light": "streetlighting_inventory_2026.csv",
    "dist_dga": "transformer_oil_dga_lab_2026.csv",
}

PH_NAME = {0: "A", 1: "B", 2: "C"}

HEAD_FILL = PatternFill("solid", fgColor="1F3B5C")
THIN = Side(style="thin", color="C4CBD4")


def _style_hdr(ws, row_idx, ncols):
    for c in ws[row_idx][:ncols]:
        c.font = Font(bold=True, color="FFFFFF", name="Calibri", size=10)
        c.fill = HEAD_FILL
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(bottom=THIN)
    ws.row_dimensions[row_idx].height = 28


def _hour_timestamps():
    """Return 8,760 UTC datetimes spanning 2026-01-01 00:00+01:00 through 2026-12-31 23:00+01:00 Europe/Oslo."""
    return [BASE_UTC + dt.timedelta(hours=h) for h in range(C.N_HOURS)]


def _build_crosswalk(world):
    """Build deterministic 1-to-1 legacy DMS ID -> current SCADA feeder ID crosswalk (non-arithmetic IDs)."""
    rng = np.random.default_rng([C.SEED, 811])
    rows = []
    legacy_map = {}
    used = set()
    for s in ALPHA_SUBS:
        for fm in world["subs"][s]["f_meta"]:
            scada_id = fm["feeder_id"]
            while True:
                num = int(rng.integers(2100, 8990))
                if num not in used:
                    used.add(num)
                    break
            legacy_id = f"DMS-{num}"
            keep_legacy = bool(rng.random() < 0.45)
            status = "PENDING_SCADA_RENAME" if keep_legacy else "SCADA_CUTOVER_2024"
            cut_date = "" if keep_legacy else f"2024-{int(rng.integers(4, 11)):02d}-{int(rng.integers(5, 25)):02d}"
            rows.append((legacy_id, scada_id, s, status, cut_date))
            legacy_map[scada_id] = legacy_id if keep_legacy else scada_id
    return rows, legacy_map


def _write_scada_substation(world, out_dir, ts_utc):
    """Write scada_substation_hourly_2026.csv spanning 2026 Europe/Oslo time (zone substations lack HV bus PTs)."""
    rng = np.random.default_rng([C.SEED, 801])
    path = os.path.join(out_dir, FILES["scada_sub"])
    iso_oslo = [t.astimezone(OSLO).isoformat(timespec="minutes") for t in ts_utc]
    cet_legacy = [t.astimezone(CET_FIXED).strftime("%d.%m.%Y %H:%M") for t in ts_utc]

    summer_hours = np.where((C.HOUR_MONTH == 5) | (C.HOUR_MONTH == 6))[0]
    null_set = set()
    for s_i, s in enumerate(ALPHA_SUBS):
        chosen = rng.choice(summer_hours, size=6 if s_i < 6 else 4, replace=False)
        for h in chosen:
            null_set.add((s, int(h)))

    n_rows = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["substation_id", "timestamp_local", "scada_clock", "p_active_mw", "v_lv_kv",
                    "ltc_tap_step", "extract_batch", "extract_ts"])
        # Preliminary batch (B20270104_PRELIM, 480 January hours x 10 non-Raudfjord substations) superseded by B20270112_FINAL
        for s in ALPHA_SUBS:
            if s == "Raudfjord":
                continue
            sd = world["subs"][s]
            for h in range(480):
                p_pre = sd["sub_p60"][h] * 0.985
                vl_pre = sd["v_lv_meas"][h] - 0.14
                w.writerow([s, iso_oslo[h], "Europe/Oslo", f"{p_pre:.5f}", f"{vl_pre:.4f}",
                            int(sd["tap_step_int"][h]), "B20270104_PRELIM", "2027-01-04T06:15:00Z"])
                n_rows += 1
        # Final authoritative 2026 export for all 11 substations x 8,760 hours
        for s in ALPHA_SUBS:
            sd = world["subs"][s]
            is_raud = (s == "Raudfjord")
            clk = "CET_Standard" if is_raud else "Europe/Oslo"
            tlist = cet_legacy if is_raud else iso_oslo
            for h in range(C.N_HOURS):
                vl_str = "" if (s, h) in null_set else f"{sd['v_lv_meas'][h]:.4f}"
                w.writerow([s, tlist[h], clk, f"{sd['sub_p60'][h]:.5f}",
                            vl_str, int(sd["tap_step_int"][h]), "B20270112_FINAL", "2027-01-12T04:30:00Z"])
                n_rows += 1
    return n_rows


def _write_subtransmission(world, out_dir, ts_utc):
    """Write gsp_66kv_voltages_2026.csv (GSP-Nord & GSP-Sor) and subtransmission_66kv_lines.csv."""
    ts_iso = [t.strftime("%Y-%m-%dT%H:%M:%SZ") for t in ts_utc]
    n_gsp = 0
    with open(os.path.join(out_dir, FILES["gsp_v"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["gsp_id", "ts_utc", "v_hv_kv"])
        for gsp_id in sorted(world["gsp_v"]):
            arr = world["gsp_v"][gsp_id]
            for h in range(C.N_HOURS):
                w.writerow([gsp_id, ts_iso[h], f"{arr[h]:.4f}"])
                n_gsp += 1

    n_seg = 0
    with open(os.path.join(out_dir, FILES["cor_lines"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["segment_id", "corridor_id", "from_bus", "to_bus", "length_km",
                    "r_ohm_per_km", "x_ohm_per_km", "nominal_kv"])
        for c_id in sorted(world["corridors"]):
            c_info = world["corridors"][c_id]
            for s_i, (frm, to, l_km, r_km, x_km) in enumerate(c_info["segs"]):
                seg_id = f"{c_id}-S{s_i + 1:02d}"
                w.writerow([seg_id, c_id, frm, to, f"{l_km:.1f}", f"{r_km:.3f}", f"{x_km:.3f}", f"{C.V_NOM_HV:.1f}"])
                n_seg += 1
    return n_gsp, n_seg


def _write_feeder_files(world, out_dir, ts_utc, xwalk_rows, legacy_map):
    """Write feeder_id_crosswalk.csv, feeder_scada_hourly_2026.csv (kW), and feeder_demand_registers_monthly_2026.csv (MW)."""
    with open(os.path.join(out_dir, FILES["xwalk"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["legacy_dms_id", "scada_feeder_id", "substation_id", "migration_status", "cutover_date"])
        w.writerows(xwalk_rows)

    ts_iso = [t.strftime("%Y-%m-%dT%H:%M:%SZ") for t in ts_utc]
    n_fscada = 0
    with open(os.path.join(out_dir, FILES["scada_fdr"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["feeder_code", "substation_id", "ts_utc", "p_active_kw"])
        for s in ALPHA_SUBS:
            sd = world["subs"][s]
            for f_i, fm in enumerate(sd["f_meta"]):
                fcode = legacy_map[fm["feeder_id"]]
                arr_kw = sd["f_p60"][f_i] * 1000.0
                for h in range(C.N_HOURS):
                    w.writerow([fcode, s, ts_iso[h], f"{arr_kw[h]:.2f}"])
                    n_fscada += 1

    n_m15 = 0
    with open(os.path.join(out_dir, FILES["fdr_m15"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["feeder_code", "substation_id", "billing_month", "max_15min_demand_mw", "register_reset_date"])
        for s in ALPHA_SUBS:
            sd = world["subs"][s]
            for f_i, fm in enumerate(sd["f_meta"]):
                fcode = legacy_map[fm["feeder_id"]]
                for m in range(12):
                    m_str = f"2026-{m + 1:02d}"
                    end_day = C.MONTH_DAYS[m]
                    reset_d = f"2026-{m + 1:02d}-{end_day:02d}"
                    w.writerow([fcode, s, m_str, f"{sd['feeder_m15'][f_i, m]:.5f}", reset_d])
                    n_m15 += 1
    return n_fscada, n_m15


def _weekdays(year, month, start_day, count):
    """Return `count` consecutive weekday ISO date strings starting on or after start_day."""
    out = []
    d = dt.date(year, month, start_day)
    while len(out) < count:
        if d.weekday() < 5:
            out.append(d.isoformat())
        d += dt.timedelta(days=1)
    return out


def _write_phase_bus_and_ami(world, out_dir, ts_utc):
    """Write substation_phase_bus_voltages_2026.csv, gis_lateral_connectivity_2026.csv (all 36 laterals/sub),
    commissioning_phase_log_2025.csv (80 AMI laterals on modernized sites), and ami_lateral_telemetry_2026.db
    (20 AMI_SMART laterals/sub x 4,368 heating hours).
    """
    ts_iso = [t.strftime("%Y-%m-%dT%H:%M:%SZ") for t in ts_utc]
    n_bus = 0
    with open(os.path.join(out_dir, FILES["bus_vph"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["substation_id", "ts_utc", "va_kv", "vb_kv", "vc_kv"])
        for s in ALPHA_SUBS:
            vp = world["subs"][s]["v_bus_ph"]
            for h in range(C.N_HOURS):
                w.writerow([s, ts_iso[h], f"{vp[0, h]:.5f}", f"{vp[1, h]:.5f}", f"{vp[2, h]:.5f}"])
                n_bus += 1

    rng = np.random.default_rng([C.SEED, 802])
    ref_dates = {
        "Fossheim": _weekdays(2025, 8, 4, 15),
        "Lindberg": _weekdays(2025, 9, 2, 15),
        "Ostervik": _weekdays(2025, 10, 2, 15),
        "Solberg": _weekdays(2025, 11, 3, 15),
    }
    gis_rows = []
    tracer_rows = []
    ami_lookup = []
    ami_global_idx = 0
    for s in ALPHA_SUBS:
        sd = world["subs"][s]
        perm = rng.permutation(C.N_LATERALS)
        dlist = ref_dates.get(s, [])
        tr_dates = sorted(rng.choice(dlist, size=C.N_AMI_LAT, replace=True).tolist()) if s in C.REFS else []
        tr_pos = 0
        for disp_i, l_i in enumerate(perm):
            l_i = int(l_i)
            lid = f"{s[:3].upper()}-L{disp_i + 1:03d}"
            g_ph = PH_NAME[int(sd["lat_gis_ph"][l_i])]
            t_ph = PH_NAME[int(sd["lat_true_ph"][l_i])]
            lcls = sd["lat_cls"][l_i]
            is_ami = bool(sd["lat_is_ami"][l_i])
            tier = "AMI_SMART" if is_ami else "LEGACY_NON_AMI"
            ver_yr = int(rng.choice([2016, 2017, 2018, 2019, 2020, 2021, 2022]))
            mwh = round(float(sd["lat_mwh"][l_i]), 2)
            sp_cnt = (max(20, int(round(mwh / float(rng.uniform(16.0, 24.0)))))
                      if lcls == "residential_heat"
                      else max(5, int(round(mwh / float(rng.uniform(60.0, 120.0))))))
            gis_rows.append((lid, s, g_ph, lcls, tier, ver_yr, sp_cnt, f"{mwh:.2f}"))
            if is_ami:
                # l_i < N_AMI_LAT maps directly into lat_v_ami / lat_p_ami
                ami_lookup.append((ami_global_idx, lid, s, l_i))
                if s in C.REFS:
                    t_date = tr_dates[tr_pos]
                    tr_pos += 1
                    eng = PEOPLE["field"] if rng.random() < 0.72 else PEOPLE["scada"]
                    tracer_rows.append((lid, s, t_ph, t_date, eng))
                ami_global_idx += 1

    with open(os.path.join(out_dir, FILES["gis_lat"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lateral_id", "substation_id", "gis_phase", "customer_class", "metering_tier",
                    "gis_last_verified_year", "service_points", "annual_billed_mwh"])
        w.writerows(gis_rows)

    with open(os.path.join(out_dir, FILES["ref_tracer"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["lateral_id", "substation_id", "traced_phase", "tracer_date", "commissioning_engineer"])
        w.writerows(tracer_rows)

    db_path = os.path.join(out_dir, FILES["ami_db"])
    if os.path.exists(db_path):
        os.remove(db_path)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA page_size = 4096;")
    conn.execute("PRAGMA journal_mode = OFF;")
    conn.execute("PRAGMA synchronous = OFF;")
    conn.execute("CREATE TABLE hours (hour_idx INTEGER PRIMARY KEY, ts_utc TEXT NOT NULL);")
    conn.execute("CREATE TABLE laterals (lateral_idx INTEGER PRIMARY KEY, lateral_id TEXT NOT NULL, substation_id TEXT NOT NULL);")
    conn.execute("CREATE TABLE lateral_hourly (lateral_idx INTEGER NOT NULL, hour_idx INTEGER NOT NULL, "
                 "v_volts REAL NOT NULL, p_kw REAL NOT NULL, PRIMARY KEY (lateral_idx, hour_idx)) WITHOUT ROWID;")

    heat_idx = np.where(C.HEATING_HOURS)[0].tolist()
    conn.executemany("INSERT INTO hours VALUES (?, ?)", [(int(h), ts_iso[h]) for h in heat_idx])
    conn.executemany("INSERT INTO laterals VALUES (?, ?, ?)", [(g, lid, s) for (g, lid, s, _) in ami_lookup])

    batch = []
    for g_idx, _lid, s, ami_i in ami_lookup:
        sd = world["subs"][s]
        lv = sd["lat_v_ami"][ami_i]
        lp = sd["lat_p_ami"][ami_i]
        for h in heat_idx:
            batch.append((g_idx, int(h), round(float(lv[h]), 2), round(float(lp[h]), 2)))
        if len(batch) >= 50000:
            conn.executemany("INSERT INTO lateral_hourly VALUES (?, ?, ?, ?)", batch)
            batch.clear()
    if batch:
        conn.executemany("INSERT INTO lateral_hourly VALUES (?, ?, ?, ?)", batch)
    conn.commit()
    conn.execute("VACUUM;")
    conn.close()
    return n_bus, len(heat_idx) * len(ami_lookup)


def _write_ref_pq_15min(world, out_dir):
    """Write pq_archive_15min_2026.csv for the four modernized substations (substation main-bay 3-phase only)."""
    path = os.path.join(out_dir, FILES["ref_pq"])
    qh_iso = [(BASE_UTC + dt.timedelta(minutes=15 * k)).strftime("%Y-%m-%dT%H:%M:%SZ") for k in range(C.N_QH)]
    n_rows = 0
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["substation_id", "ts_utc", "sub_pa_mw", "sub_pb_mw", "sub_pc_mw", "sub_p15_mw", "sub_q15_mvar"])
        for r in sorted(C.REFS):
            sd = world["subs"][r]
            pa = sd["sub_p15_ph"][0].reshape(-1)
            pb = sd["sub_p15_ph"][1].reshape(-1)
            pc = sd["sub_p15_ph"][2].reshape(-1)
            sp = sd["sub_p15"].reshape(-1)
            sq = sd["q_15"].reshape(-1)
            for k in range(C.N_QH):
                w.writerow([r, qh_iso[k], f"{pa[k]:.5f}", f"{pb[k]:.5f}", f"{pc[k]:.5f}", f"{sp[k]:.5f}", f"{sq[k]:.5f}"])
                n_rows += 1
    return n_rows


def _write_workbooks_and_lookups(world, out_dir):
    """Write revenue_meter_monthly_2026.xlsx, substation_transformer_register.xlsx (no synthetic cluster labels),
    substation_annual_energy_summary_2025.xlsx, and engineering_manual_class_pf.csv.
    """
    with open(os.path.join(out_dir, FILES["class_pf"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["customer_class", "nominal_pf", "manual_section"])
        handbook = [
            ("industrial_batch", 0.87, "EM-4.2"),
            ("maritime_port", 0.89, "EM-4.3"),
            ("commercial_mixed", 0.92, "EM-4.4"),
            ("residential_heat", 0.95, "EM-4.5"),
            ("agricultural_rural", 0.91, "EM-4.6"),
            ("public_lighting", 0.96, "EM-4.7"),
            ("small_hydro_aux", 0.93, "EM-4.8"),
        ]
        for k, v, sec in handbook:
            w.writerow([k, f"{v:.2f}", sec])

    wb = Workbook()
    ws = wb.active
    ws.title = "Monthly_Revenue_Meters"
    ws.append(["substation_id", "billing_month", "active_energy_kwh", "net_reactive_energy_kvarh",
               "meter_serial", "settlement_status"])
    _style_hdr(ws, 1, 6)
    rng_m = np.random.default_rng([C.SEED, 812])
    serials = {s: f"VN-REV-{int(rng_m.integers(4100, 8900))}" for s in ALPHA_SUBS}
    for s in ALPHA_SUBS:
        sd = world["subs"][s]
        for m in range(12):
            ws.append([s, f"2026-{m + 1:02d}", round(float(sd["sub_kwh_m"][m]), 2),
                       round(float(sd["sub_net_kvarh_m"][m]), 2), serials[s], "SETTLED"])
            r_idx = ws.max_row
            ws.cell(row=r_idx, column=3).number_format = "#,##0.00"
            ws.cell(row=r_idx, column=4).number_format = "#,##0.00"
    for col, w_ in zip("ABCDEF", [16, 15, 20, 24, 16, 18]):
        ws.column_dimensions[col].width = w_
    wb.save(os.path.join(out_dir, FILES["rev_xlsx"]))

    wb2 = Workbook()
    ws_s = wb2.active
    ws_s.title = "Substations"
    ws_s.append(["substation_id", "operating_district", "hv_nom_kv", "lv_nom_kv", "firm_n1_mva",
                 "r_ohm", "x_ohm", "ltc_tap_step_pct", "ltc_min_tap", "ltc_max_tap", "modernization_status"])
    _style_hdr(ws_s, 1, 11)
    for s in ALPHA_SUBS:
        cfg = world["subs"][s]["cfg"]
        is_ref = s in C.REFS
        ws_s.append([s, REGIONS[s], C.V_NOM_HV, C.V_NOM_LV, cfg["firm_mva"],
                     cfg["r_ohm"], cfg["x_ohm"], 1.25, -8, 8,
                     "modernized_2023_2024" if is_ref else "standard_transformer_bay"])
        r_idx = ws_s.max_row
        ws_s.cell(row=r_idx, column=5).number_format = "0.0"
        ws_s.cell(row=r_idx, column=6).number_format = "0.000"
        ws_s.cell(row=r_idx, column=7).number_format = "0.00"
    for col, w_ in zip("ABCDEFGHIJK", [15, 16, 12, 12, 14, 10, 10, 16, 12, 12, 26]):
        ws_s.column_dimensions[col].width = w_

    ws_f = wb2.create_sheet("Feeders")
    ws_f.append(["scada_feeder_id", "substation_id", "customer_class", "nominal_kv", "circuit_length_km"])
    _style_hdr(ws_f, 1, 5)
    rng = np.random.default_rng([C.SEED, 803])
    mv_km_by_sub = {s: 0.0 for s in ALPHA_SUBS}
    for s in ALPHA_SUBS:
        for fm in world["subs"][s]["f_meta"]:
            km = round(float(rng.uniform(4.2, 28.6)), 1)
            mv_km_by_sub[s] += km
            ws_f.append([fm["feeder_id"], s, fm["fcls"], C.V_NOM_LV, km])
    for col, w_ in zip("ABCDE", [18, 15, 20, 13, 18]):
        ws_f.column_dimensions[col].width = w_
    wb2.save(os.path.join(out_dir, FILES["tx_xlsx"]))

    wb3 = Workbook()
    ws_c = wb3.active
    ws_c.title = "Annual_Summary_2025"
    ws_c.append(["substation_id", "operating_district", "energy_delivered_2025_mwh",
                 "connected_customers_2025", "mv_feeders_count", "total_mv_lv_network_km"])
    _style_hdr(ws_c, 1, 6)
    rng_c = np.random.default_rng([C.SEED, 804])
    for s in ALPHA_SUBS:
        sd = world["subs"][s]
        e25 = float(sd["sub_kwh_m"].sum() / 1000.0) * float(rng_c.uniform(0.952, 0.994))
        cust = int(rng_c.integers(3200, 9400))
        nf = len(sd["f_meta"])
        tot_km = round(mv_km_by_sub[s] * float(rng_c.uniform(1.95, 2.55)), 1)
        ws_c.append([s, REGIONS[s], round(e25, 1), cust, nf, tot_km])
        r_idx = ws_c.max_row
        ws_c.cell(row=r_idx, column=3).number_format = "#,##0.0"
        ws_c.cell(row=r_idx, column=4).number_format = "#,##0"
    for col, w_ in zip("ABCDEF", [16, 16, 26, 24, 18, 24]):
        ws_c.column_dimensions[col].width = w_
    wb3.save(os.path.join(out_dir, FILES["ctx_2025"]))


def _write_distractors(world, out_dir):
    """Write two unlabelled domain distractor CSVs with realistic varying counts and dates."""
    rng = np.random.default_rng([C.SEED, 805])
    lamp_types = ["LED_45W", "LED_68W", "LED_92W", "HPS_150W", "MH_100W"]
    with open(os.path.join(out_dir, FILES["dist_light"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["circuit_id", "municipality", "lamp_type", "fixture_count", "rated_kw", "burn_hours_2026", "controller"])
        cid = 104
        for s in ALPHA_SUBS:
            muni = MUNICIPALITIES[s]
            n_circ = int(rng.integers(31, 64))
            for _ in range(n_circ):
                lt = str(rng.choice(lamp_types))
                watt = int(lt.split("_")[1].rstrip("W"))
                cnt = int(rng.integers(12, 88))
                rkw = round(cnt * watt / 1000.0, 3)
                bh = int(rng.integers(3920, 4190))
                ctrl = str(rng.choice(["astro_clock", "photocell", "dali_dimming"]))
                w.writerow([f"SL-{cid:04d}", muni, lt, cnt, f"{rkw:.3f}", bh, ctrl])
                cid += int(rng.integers(1, 4))

    with open(os.path.join(out_dir, FILES["dist_dga"]), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["sample_id", "substation_id", "transformer_unit", "sample_date",
                    "h2_ppm", "ch4_ppm", "c2h2_ppm", "c2h4_ppm", "co_ppm", "moisture_ppm", "lab_status"])
        base_quarters = [dt.date(2026, 2, 10), dt.date(2026, 5, 12), dt.date(2026, 8, 11), dt.date(2026, 11, 10)]
        sid = 26103
        for s_i, s in enumerate(ALPHA_SUBS):
            for unit in ("T1", "T2"):
                for q_i, bd in enumerate(base_quarters):
                    d = bd + dt.timedelta(days=int((s_i * 2 + q_i) % 11))
                    if d.weekday() >= 5:
                        d += dt.timedelta(days=7 - d.weekday())
                    h2 = round(float(rng.uniform(8.0, 46.0)), 1)
                    ch4 = round(float(rng.uniform(4.0, 31.0)), 1)
                    c2h2 = round(float(rng.uniform(0.0, 0.9)), 2)
                    c2h4 = round(float(rng.uniform(3.0, 21.0)), 1)
                    co = round(float(rng.uniform(140.0, 445.0)), 1)
                    moist = round(float(rng.uniform(6.0, 17.5)), 1)
                    status = "MONITOR" if (co > 420.0 or h2 > 43.0) else "NORMAL"
                    w.writerow([f"DGA-{sid}", s, unit, d.isoformat(), h2, ch4, c2h2, c2h4, co, moist, status])
                    sid += int(rng.integers(2, 9))


def build(out_dir, world=None):
    world = world or C.simulate()
    ts_utc = _hour_timestamps()
    xwalk_rows, legacy_map = _build_crosswalk(world)
    n_scada = _write_scada_substation(world, out_dir, ts_utc)
    n_gsp, n_seg = _write_subtransmission(world, out_dir, ts_utc)
    n_fscada, n_m15 = _write_feeder_files(world, out_dir, ts_utc, xwalk_rows, legacy_map)
    n_bus, n_ami = _write_phase_bus_and_ami(world, out_dir, ts_utc)
    n_refpq = _write_ref_pq_15min(world, out_dir)
    _write_workbooks_and_lookups(world, out_dir)
    _write_distractors(world, out_dir)
    return dict(scada_rows=n_scada, gsp_rows=n_gsp, corridor_segments=n_seg,
                feeder_scada_rows=n_fscada, feeder_m15_rows=n_m15,
                bus_vph_rows=n_bus, ami_rows=n_ami, ref_pq_rows=n_refpq)
