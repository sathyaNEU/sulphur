"""Completely standalone independent verifier for task27.

Unzips task27/target.zip and task27/golden.zip into a fresh temporary directory and recomputes
every headline figure, Critical Component (C1, C2, C3), 2027 corridor/Q3/EUR ask, and native-unit
physical conservation diagnostic directly from raw shipped files WITHOUT importing core.py or
analysis.py, asserting exact agreement with figures.json and golden deliverables.
"""
import csv
import datetime as dt
import json
import os
import shutil
import sys
import tempfile
import zipfile
from collections import defaultdict
from zoneinfo import ZoneInfo

import numpy as np
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK_DIR = os.path.dirname(HERE)
UTC = dt.timezone.utc
BERLIN = ZoneInfo("Europe/Berlin")
BASE_DATE = dt.date(2026, 1, 1)

TARIFF_EUR = {
    "vessel_berth": 195.0,
    "edi_docs": 140.0,
    "reefer_plug": 210.0,
    "coldstore_dock": 285.0,
    "rail_handoff": 175.0,
    "phyto_insp": 260.0,
    "drayage_carrier": 160.0,
    "empty_depot": 230.0,
}


def _d(s):
    s = s.strip()
    if "." in s:
        dd, mm, yy = s.split(".")
        return dt.date(int(yy), int(mm), int(dd))
    return dt.date.fromisoformat(s)


def _ts(s):
    s = s.strip()
    return dt.datetime.fromisoformat(s[:-1] + "+00:00" if s.endswith("Z") else s)


def _q(day_idx):
    if day_idx < 90:
        return 0
    if day_idx < 181:
        return 1
    if day_idx < 273:
        return 2
    return 3


def verify():
    tmp = tempfile.mkdtemp(prefix="verify-task27-")
    try:
        tdir = os.path.join(tmp, "target")
        gdir = os.path.join(tmp, "golden")
        os.makedirs(tdir)
        os.makedirs(gdir)
        with zipfile.ZipFile(os.path.join(TASK_DIR, "target.zip")) as z:
            z.extractall(tdir)
        with zipfile.ZipFile(os.path.join(TASK_DIR, "golden.zip")) as z:
            z.extractall(gdir)

        # 1. Load plan, catalog, chamber register, aggregate DC stock
        plan = defaultdict(dict)
        with open(os.path.join(tdir, "import_plan_2027.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                plan[r["metric_code"]][r["entity_id"]] = (float(r["value_2026"]), float(r["value_2027"]))

        sku_z, sku_cpp = {}, {}
        with open(os.path.join(tdir, "sku_thermal_catalog.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sku_z[r["sku_id"]] = r["thermal_zone"]
                sku_cpp[r["sku_id"]] = int(r["cases_per_pallet"])

        ch_cap, ch_open = {}, {}
        with open(os.path.join(tdir, "dc_chamber_register_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                k = (r["dc_id"], r["thermal_zone"])
                ch_cap[k] = float(r["pallet_bay_capacity"])
                ch_open[k] = int(r["opening_pallets_2026_01_01"])

        dc_tot = {}
        with open(os.path.join(tdir, "coldstore_inventory_daily_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                dc_tot[(r["dc_id"], (_d(r["date_iso"]) - BASE_DATE).days)] = int(r["total_pallets_on_hand"])

        # 2. Reconstruct per-chamber daily utilization from warehouse_pallet_movements_2026.csv
        mv_latest = {}
        with open(os.path.join(tdir, "warehouse_pallet_movements_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                mid = r["movement_id"]
                v = int(r["extract_version"])
                if mid not in mv_latest or v > mv_latest[mid][0]:
                    mv_latest[mid] = (v, r)

        net_flow = defaultdict(int)
        for _, r in mv_latest.values():
            t = (_d(r["move_date"]) - BASE_DATE).days
            z = sku_z[r["sku_id"]]
            qty = int(r["quantity"])
            p = qty // sku_cpp[r["sku_id"]] if r["unit"] == "CASE" else qty
            net_flow[(r["dc_id"], z, t)] += p if r["direction"] == "IN" else -p

        ch_util = {}
        for dc in ("HAN", "OSN", "KAS", "MAG"):
            for z in ("Z02", "Z07", "Z13"):
                cur = ch_open[(dc, z)]
                cap = ch_cap[(dc, z)]
                for t in range(365):
                    cur += net_flow[(dc, z, t)]
                    ch_util[(dc, z, t)] = cur / cap
            for t in range(365):
                rec_tot = sum(round(ch_util[(dc, z, t)] * ch_cap[(dc, z)]) for z in ("Z02", "Z07", "Z13"))
                assert rec_tot == dc_tot[(dc, t)], f"Stock mismatch at {dc} day {t}"

        # 3. Load rail shuttles, consignments, BIP notices
        sh_dep, sh_booked, sh_loaded, sh_rolled, sh_wag, sh_ton, sh_port, sh_day = {}, {}, {}, {}, {}, {}, {}, {}
        with open(os.path.join(tdir, "rail_shuttle_departures_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sid = r["shuttle_id"]
                sh_dep[sid] = _ts(r["departure_ts_utc"])
                sh_booked[sid] = int(r["booked_wf_slots"])
                sh_loaded[sid] = int(r["loaded_wf_slots"])
                sh_rolled[sid] = int(r["wf_standby_rolled"])
                sh_wag[sid] = int(r["train_wagon_count"])
                sh_ton[sid] = float(r["train_total_gross_tonnes"])
                sh_port[sid] = r["port_id"]
                d_s = sid.split("-")[-1]
                sh_day[sid] = (dt.date(int(d_s[:4]), int(d_s[4:6]), int(d_s[6:8])) - BASE_DATE).days

        c_ched = {}
        with open(os.path.join(tdir, "customs_consignment_bol_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                c_ched[r["container_id"]] = r["ched_lot_id"]

        bip_notice_ts = {}
        with open(os.path.join(tdir, "bip_inspection_notices_2026.jsonl"), encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    bip_notice_ts[rec["ched_lot_id"]] = _ts(rec["exam_notice_ts_utc"])

        # 4. Load depot portal rejections
        portal_rej = {}
        with open(os.path.join(tdir, "depot_portal_requests_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                t = (_d(r["date_iso"]) - BASE_DATE).days
                portal_rej[(r["depot_port_id"], r["shipping_line_id"], t)] = int(r["quota_closed_rejections"])

        # 5. Load & clean container_milestones_2026.csv
        ms_latest = {}
        with open(os.path.join(tdir, "container_milestones_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["record_status"] == "VOID":
                    continue
                cid = r["container_id"]
                v = int(r["extract_version"])
                if cid not in ms_latest or v > ms_latest[cid][0]:
                    ms_latest[cid] = (v, r)
        rows = [v[1] for v in ms_latest.values()]
        assert len(rows) == 24000

        # S1: same-vessel unsaturated twin contrast
        uncap_by_v = defaultdict(list)
        uncap_by_p = defaultdict(list)
        for r in rows:
            t = (_ts(r["discharge_ts_utc"]).astimezone(UTC).date() - BASE_DATE).days
            u = ch_util[(r["dc_id"], r["thermal_zone"], t)]
            y = float(r["excess_port_yard_cdays"])
            if u < 0.92:
                uncap_by_v[r["vessel_id"]].append(y)
                uncap_by_p[r["port_id"]].append(y)
        v_mean = {k: float(np.mean(v)) for k, v in uncap_by_v.items()}
        p_mean = {k: float(np.mean(v)) for k, v in uncap_by_p.items()}

        # S3: same-DC same-unload-day open-quota shipping-line contrast
        open_by_dc_day = defaultdict(list)
        open_by_dc = defaultdict(list)
        for r in rows:
            ut = (_ts(r["unload_complete_ts_cet"]).astimezone(BERLIN).date() - BASE_DATE).days
            rej = portal_rej[(r["port_id"], r["shipping_line_id"], ut)]
            dr = float(r["excess_dray_empty_cdays"])
            if rej == 0:
                open_by_dc_day[(r["dc_id"], ut)].append(dr)
                open_by_dc[r["dc_id"]].append(dr)
        dd_mean = {k: float(np.mean(v)) for k, v in open_by_dc_day.items()}
        dc_mean = {k: float(np.mean(v)) for k, v in open_by_dc.items()}

        # S2: empirical lock cutoff + locked wagon count + weighbridge regression
        sids = sorted(sh_dep.keys())
        sid_to_i = {s: i for i, s in enumerate(sids)}
        shortfall = np.array([sh_booked[s] - sh_loaded[s] for s in sids], dtype=float)
        # Collect rail boxes & notice lead hours
        rail_boxes = []
        clean_rail_by_sh = defaultdict(list)
        all_rail_nonbip_by_sh = defaultdict(list)
        for r in rows:
            if r["mode"] != "RAIL":
                continue
            sid = r["planned_shuttle_id"]
            ched = c_ched[r["container_id"]]
            is_bip = ched in bip_notice_ts
            lead_h = (sh_dep[sid] - bip_notice_ts[ched]).total_seconds() / 3600.0 if is_bip else 999.0
            rolled = (r["departed_shuttle_id"] != sid)
            ex_r = float(r["excess_rail_cdays"])
            rail_boxes.append((r, sid, is_bip, lead_h, rolled, ex_r))
            if not is_bip:
                all_rail_nonbip_by_sh[sid].append(ex_r)
                if not rolled:
                    clean_rail_by_sh[sid].append(ex_r)

        best_c, best_r2 = 24.0, -1.0
        for cand in (12.0, 18.0, 24.0, 30.0, 36.0):
            cnt = np.zeros(len(sids))
            for _, sid, is_bip, lead_h, _, _ in rail_boxes:
                if is_bip and lead_h <= cand:
                    cnt[sid_to_i[sid]] += 1.0
            r2 = float(np.corrcoef(cnt, shortfall)[0, 1] ** 2)
            if r2 > best_r2:
                best_r2, best_c = r2, cand
        assert best_c == 24.0, f"Unexpected empirical lock cutoff: {best_c}"

        n_locked_sh = np.zeros(len(sids))
        for _, sid, is_bip, lead_h, _, _ in rail_boxes:
            if is_bip and lead_h <= best_c:
                n_locked_sh[sid_to_i[sid]] += 1.0
        non_phyto_short = np.maximum(0.0, shortfall - n_locked_sh)
        Xw = np.column_stack([
            np.ones(len(sids)),
            [sh_wag[s] for s in sids],
            [sh_booked[s] for s in sids],
            n_locked_sh,
            non_phyto_short,
        ])
        bw, _, _, _ = np.linalg.lstsq(Xw, np.array([sh_ton[s] for s in sids]), rcond=None)
        f2_tonnes = float(bw[3])

        # Compute exact container-level and shuttle-level 2026 & 2027 attributions
        c26 = defaultdict(float)
        c27 = defaultdict(float)
        p27 = defaultdict(float)
        q27 = defaultdict(float)
        f1_gaps, f3_gaps = [], []

        for r in rows:
            p = r["port_id"]
            z = r["thermal_zone"]
            l = r["shipping_line_id"]
            t = (_ts(r["discharge_ts_utc"]).astimezone(UTC).date() - BASE_DATE).days
            ut = (_ts(r["unload_complete_ts_cet"]).astimezone(BERLIN).date() - BASE_DATE).days
            q = _q(t)

            vg = plan["vol_growth_port"][p][1]
            pf = plan["plug_capacity_factor_2027"][p][1]
            zf = plan["dc_zone_load_factor_2027"][z][1]
            bf = plan["bip_sampling_factor_2027"][p][1]
            df = plan["dray_contract_factor_2027"]["NETWORK"][1]
            s26, s27 = plan["line_volume_share"][l]
            dl = plan["depot_load_factor_2027"][l][1]

            vb = float(r["excess_berth_cdays"])
            ed = float(r["excess_edi_cdays"])
            c26["vessel_berth"] += vb
            c27["vessel_berth"] += vb * vg
            c26["edi_docs"] += ed
            c27["edi_docs"] += ed * vg

            # S1 split
            y = float(r["excess_port_yard_cdays"])
            dc_w = float(r["excess_dc_dock_cdays"])
            u = ch_util[(r["dc_id"], z, t)]
            if u >= 0.95:
                base_y = v_mean.get(r["vessel_id"], p_mean[p])
                pb = max(0.0, y - base_y)
                f1_gaps.append((y - base_y) * 24.0)
            else:
                pb = 0.0
            rp = y - pb
            cs_tot = dc_w + pb
            c26["reefer_plug"] += rp
            c27["reefer_plug"] += rp * vg * pf
            c26["coldstore_dock"] += cs_tot
            c27["coldstore_dock"] += cs_tot * zf

            # Direct phyto
            ph_d = float(r["excess_phyto_cdays"])
            c26["phyto_insp"] += ph_d
            c27["phyto_insp"] += ph_d * vg * bf

            # S3 split
            dr = float(r["excess_dray_empty_cdays"])
            dep_g = float(r["excess_depot_gate_cdays"])
            rej = portal_rej[(p, l, ut)]
            if rej >= 1:
                base_d = dd_mean.get((r["dc_id"], ut), dc_mean[r["dc_id"]])
                blk = max(0.0, dr - base_d)
                f3_gaps.append((dr - base_d) * 24.0)
            else:
                blk = 0.0
            dr_true = dr - blk
            edep_tot = dep_g + blk
            c26["drayage_carrier"] += dr_true
            c27["drayage_carrier"] += dr_true * vg * df
            c26["empty_depot"] += edep_tot
            c27["empty_depot"] += edep_tot * vg * (s27 / s26) * dl

            box_27 = (
                vb * vg + ed * vg + rp * vg * pf + cs_tot * zf
                + ph_d * vg * bf + dr_true * vg * df + edep_tot * vg * (s27 / s26) * dl
            )
            p27[p] += box_27
            q27[q] += box_27

        # Rail siblings + shuttle rollover split (S2)
        rolled_ex = [ex for _, _, is_bip, _, rolled, ex in rail_boxes if (not is_bip) and rolled]
        unrolled_ex = [ex for _, _, is_bip, _, rolled, ex in rail_boxes if (not is_bip) and (not rolled)]
        roll_dur = float(np.mean(rolled_ex) - np.mean(unrolled_ex))

        sh_base_box = {}
        for s in sids:
            if clean_rail_by_sh[s]:
                sh_base_box[s] = float(np.mean(clean_rail_by_sh[s]))
            elif all_rail_nonbip_by_sh[s]:
                sh_base_box[s] = max(0.0, float(np.mean(all_rail_nonbip_by_sh[s]) - roll_dur))
            else:
                sh_base_box[s] = 0.0

        sh_roll_days = defaultdict(float)
        sh_all_rail_minus_sib = defaultdict(float)
        for r, sid, is_bip, _, rolled, ex_r in rail_boxes:
            p = r["port_id"]
            t = (_ts(r["discharge_ts_utc"]).astimezone(UTC).date() - BASE_DATE).days
            q = _q(t)
            vg = plan["vol_growth_port"][p][1]
            bf = plan["bip_sampling_factor_2027"][p][1]
            is_sib = is_bip and (r["bip_sampled_ind"] == "0")
            if is_sib:
                sib_d = max(0.0, ex_r - sh_base_box[sid])
                c26["phyto_insp"] += sib_d
                c27["phyto_insp"] += sib_d * vg * bf
                p27[p] += sib_d * vg * bf
                q27[q] += sib_d * vg * bf
                sh_all_rail_minus_sib[sid] += ex_r - sib_d
            else:
                sh_all_rail_minus_sib[sid] += ex_r
                if rolled:
                    sh_roll_days[sid] += max(0.0, ex_r - sh_base_box[sid])

        rf = plan["rail_fleet_factor_2027"]["NETWORK"][1]
        for i, s in enumerate(sids):
            p = sh_port[s]
            q = _q(sh_day[s])
            vg = plan["vol_growth_port"][p][1]
            bf = plan["bip_sampling_factor_2027"][p][1]
            rolled_tot = float(sh_rolled[s])
            base_s = sh_all_rail_minus_sib[s] - sh_roll_days[s]
            locked_b = min(rolled_tot, float(n_locked_sh[i]))
            if rolled_tot > 0:
                ph_b = sh_roll_days[s] * (locked_b / rolled_tot)
                rh_b = sh_roll_days[s] - ph_b
            else:
                ph_b = 0.0
                rh_b = 0.0
            c26["phyto_insp"] += ph_b
            c27["phyto_insp"] += ph_b * vg * bf
            c26["rail_handoff"] += rh_b + base_s
            c27["rail_handoff"] += (rh_b + base_s) * vg * rf
            p27[p] += ph_b * vg * bf + (rh_b + base_s) * vg * rf
            q27[q] += ph_b * vg * bf + (rh_b + base_s) * vg * rf

        # Compare against figures.json and golden deliverables
        fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
        for row in fig["causes"]:
            m = row["cause_id"]
            assert abs(c26[m] - row["cdays_2026"]) < 0.05, f"2026 {m}: {c26[m]} vs {row['cdays_2026']}"
            assert abs(c27[m] - row["cdays_2027"]) < 0.05, f"2027 {m}: {c27[m]} vs {row['cdays_2027']}"

        tot_27 = sum(c27.values())
        remed_set = sorted(m for m in c27 if c27[m] >= 2500.0)
        remed_days = sum(c27[m] for m in remed_set)
        cost_m = sum(c27[m] * TARIFF_EUR[m] for m in c27) / 1e6
        avoid_m = sum(c27[m] * TARIFF_EUR[m] for m in remed_set) / 1e6

        assert remed_set == fig["remediate_set"]
        assert abs(tot_27 - fig["routes"]["golden"]["total_2027"]) < 0.1
        assert abs(remed_days - fig["routes"]["golden"]["remed_days"]) < 0.1
        assert abs(cost_m - fig["A_cost_eur_m"]) < 0.002
        assert abs(avoid_m - fig["A_avoidable_eur_m"]) < 0.002
        assert abs(p27["BHV"] - fig["by_port_2027"]["BHV"]) < 0.1
        assert abs(p27["HAM"] - fig["by_port_2027"]["HAM"]) < 0.1
        assert abs(q27[2] - fig["by_quarter_2027"]["Q3"]) < 0.1
        assert abs(float(np.mean(f1_gaps)) - fig["R5_diagnostics"]["F1_twin_gap_h"]) < 0.05
        assert abs(f2_tonnes - fig["R5_diagnostics"]["F2_tonnes_per_slot"]) < 0.05
        assert abs(float(np.mean(f3_gaps)) - fig["R5_diagnostics"]["F3_line_gap_h"]) < 0.05

        # Also check unzipped golden CSV & XLSX match recomputed values
        with open(os.path.join(gdir, "weserfrucht_delay_attribution_2027.csv"), encoding="utf-8") as f:
            g_rows = list(csv.DictReader(f))
        for gr in g_rows:
            m = gr["cause_id"]
            assert abs(float(gr["cdays_2027"]) - c27[m]) < 0.05

        wb = load_workbook(os.path.join(gdir, "weserfrucht_coldchain_remediation_2027.xlsx"), data_only=True)
        ws1 = wb["Remediation_Summary"]
        assert abs(float(ws1["E14"].value) - tot_27) < 0.1
        assert abs(float(ws1["E15"].value) - remed_days) < 0.1

        print(
            f"PASS  verify.py task27 (standalone from target.zip): "
            f"2026={sum(c26.values()):,.2f}, 2027={tot_27:,.2f}, remed={remed_days:,.2f}, "
            f"EUR {cost_m:.3f}M (avoidable {avoid_m:.3f}M), "
            f"F1=+{np.mean(f1_gaps):.2f}h, F2={f2_tonnes:.2f}t, F3=+{np.mean(f3_gaps):.2f}h"
        )
        return 0
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(verify())
