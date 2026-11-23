"""Completely standalone independent verifier for task27 (Arch 2, v4-hardened).

Unzips task27/target.zip and task27/golden.zip into a fresh temporary directory and recomputes
C1, C2, C3, all 6 corridor 2027 BCRs, avoidable EUR, funded slate, and CSV/XLSX tie-outs
directly from the raw shipped files WITHOUT importing core.py or analysis.py.
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

PORTS = ("BHV", "HAM", "WHV")
DCS = ("HAN", "OSN", "KAS", "MAG")
ZONES = ("Z02", "Z07", "Z13")
LINES = ("LINE_A", "LINE_B", "LINE_C", "LINE_D")
CORRIDORS = ("BHV-HAN", "BHV-KAS", "BHV-OSN", "HAM-HAN", "HAM-MAG", "WHV-OSN")
PORT_IDX = {p: i for i, p in enumerate(PORTS)}
DC_IDX = {d: i for i, d in enumerate(DCS)}
ZONE_IDX = {z: i for i, z in enumerate(ZONES)}
LINE_IDX = {l: i for i, l in enumerate(LINES)}
CORR_IDX = {c: i for i, c in enumerate(CORRIDORS)}
BUDGET_CAP_EUR = 1_750_000.0


def _d(s):
    s = s.strip()
    if "." in s:
        dd, mm, yy = s.split(".")
        return dt.date(int(yy), int(mm), int(dd))
    return dt.date.fromisoformat(s)


def _ts(s):
    s = s.strip()
    return dt.datetime.fromisoformat(s[:-1] + "+00:00" if s.endswith("Z") else s)


def _sigmoid(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30.0, 30.0)))


def _demean(arr, grp, n_grp):
    cnt = np.maximum(1.0, np.bincount(grp, minlength=n_grp).astype(float))
    if arr.ndim == 1:
        return arr - (np.bincount(grp, weights=arr, minlength=n_grp) / cnt)[grp]
    out = np.empty_like(arr, dtype=float)
    for j in range(arr.shape[1]):
        out[:, j] = arr[:, j] - (np.bincount(grp, weights=arr[:, j], minlength=n_grp) / cnt)[grp]
    return out


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

        # 1. Budgets & plan
        plan = {}
        with open(os.path.join(tdir, "remediation_program_budgets_2027.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                plan[r["corridor_id"]] = {
                    "port": r["port_id"],
                    "dc": r["dc_id"],
                    "budget": float(r["remediation_budget_eur"]),
                    "cap": float(r["capture_rate_2027"]),
                    "vg": float(r["vol_growth_2027"]),
                    "pf": float(r["plug_capacity_factor_2027"]),
                    "rf": float(r["rail_fleet_factor_2027"]),
                    "df": float(r["dray_contract_factor_2027"]),
                    "t_plug": float(r["tariff_reefer_plug_eur"]),
                    "t_rail": float(r["tariff_rail_handoff_eur"]),
                    "t_dray": float(r["tariff_drayage_carrier_eur"]),
                }

        # 2. SKU catalog, chamber register, aggregate DC stock, warehouse pallet movements
        sku_z, sku_cpp = {}, {}
        with open(os.path.join(tdir, "sku_thermal_catalog.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sku_z[r["sku_id"]] = ZONE_IDX[r["thermal_zone"]]
                sku_cpp[r["sku_id"]] = int(r["cases_per_pallet"])

        ch_cap = np.zeros((4, 3), dtype=float)
        ch_open = np.zeros((4, 3), dtype=int)
        with open(os.path.join(tdir, "dc_chamber_register_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                ch_cap[DC_IDX[r["dc_id"]], ZONE_IDX[r["thermal_zone"]]] = float(r["pallet_bay_capacity"])
                ch_open[DC_IDX[r["dc_id"]], ZONE_IDX[r["thermal_zone"]]] = int(r["opening_pallets_2026_01_01"])

        dc_tot = np.zeros((4, 365), dtype=int)
        with open(os.path.join(tdir, "coldstore_inventory_daily_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                dc_tot[DC_IDX[r["dc_id"]], (_d(r["date_iso"]) - BASE_DATE).days] = int(r["total_pallets_on_hand"])

        mv_lat = {}
        with open(os.path.join(tdir, "warehouse_pallet_movements_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                mid, v = r["movement_id"], int(r["extract_version"])
                if mid not in mv_lat or v > mv_lat[mid][0]:
                    mv_lat[mid] = (v, r)

        p_in = np.zeros((4, 3, 365), dtype=int)
        p_out = np.zeros((4, 3, 365), dtype=int)
        for _, r in mv_lat.values():
            t = (_d(r["move_date"]) - BASE_DATE).days
            d, z = DC_IDX[r["dc_id"]], sku_z[r["sku_id"]]
            q = int(r["quantity"])
            pal = q // sku_cpp[r["sku_id"]] if r["unit"] == "CASE" else q
            if r["direction"] == "IN":
                p_in[d, z, t] += pal
            else:
                p_out[d, z, t] += pal

        ch_nf = (p_in - p_out).astype(float)
        ch_st = np.zeros((4, 3, 365), dtype=float)
        for d in range(4):
            for z in range(3):
                ch_st[d, z] = ch_open[d, z] + np.cumsum(ch_nf[d, z])
        assert np.allclose(ch_st.sum(axis=1), dc_tot, atol=1e-9), "Chamber conservation failed!"
        ch_u = ch_st / ch_cap[:, :, None]

        # 3. Shuttles, consignments, BIP notices
        sh_rows = []
        sh_idx = {}
        with open(os.path.join(tdir, "rail_shuttle_departures_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                sh_idx[r["shuttle_id"]] = len(sh_rows)
                sh_rows.append(r)
        n_sh = len(sh_rows)
        n_slots = n_sh // 6
        sh_corr = np.array([CORR_IDX[r["corridor_id"]] for r in sh_rows], dtype=int)
        sh_port = np.array([PORT_IDX[r["port_id"]] for r in sh_rows], dtype=int)
        sh_dep = [_ts(r["scheduled_departure_ts_utc"]) for r in sh_rows]
        sh_planned = np.array([int(r["planned_wf_slots"]) for r in sh_rows], dtype=int)
        sh_rolled = np.array([int(r["wf_standby_rolled"]) for r in sh_rows], dtype=float)
        sh_cs = np.array([int(r["consist_wagons_short"]) for r in sh_rows], dtype=float)
        sh_ld = np.array([int(r["loco_derate_events"]) for r in sh_rows], dtype=float)
        port_slot_dep = {(int(sh_port[s]), s % n_slots): sh_dep[s] for s in range(n_sh)}

        c_ched = {}
        with open(os.path.join(tdir, "customs_consignment_bol_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                c_ched[r["container_id"]] = r["ched_lot_id"]

        bip_ts = {}
        with open(os.path.join(tdir, "bip_inspection_notices_2026.jsonl"), encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    bip_ts[rec["ched_lot_id"]] = _ts(rec["exam_notice_ts_utc"])

        # 4. Milestones
        ms_lat = {}
        with open(os.path.join(tdir, "container_milestones_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r["record_status"] == "VOID":
                    continue
                cid, v = r["container_id"], int(r["extract_version"])
                if cid not in ms_lat or v > ms_lat[cid][0]:
                    ms_lat[cid] = (v, r)
        cids = sorted(ms_lat.keys())
        n = len(cids)
        assert n == 24000

        v_sorted = sorted({ms_lat[c][1]["vessel_id"] for c in cids})
        v_map = {v: i for i, v in enumerate(v_sorted)}
        n_v = len(v_sorted)

        cont_v = np.zeros(n, dtype=int)
        cont_c = np.zeros(n, dtype=int)
        cont_p = np.zeros(n, dtype=int)
        cont_dc = np.zeros(n, dtype=int)
        cont_z = np.zeros(n, dtype=int)
        cont_l = np.zeros(n, dtype=int)
        cont_d = np.zeros(n, dtype=int)
        cont_ud = np.zeros(n, dtype=int)
        cont_rail = np.zeros(n, dtype=bool)
        cont_roll = np.zeros(n, dtype=bool)
        cont_sh = np.zeros(n, dtype=int)
        cont_bip = np.zeros(n, dtype=bool)
        cont_samp = np.zeros(n, dtype=bool)
        cont_lead = np.full(n, 999.0, dtype=float)
        y_yard = np.zeros(n, dtype=float)
        y_rail = np.zeros(n, dtype=float)
        y_dray = np.zeros(n, dtype=float)

        for i, cid in enumerate(cids):
            r = ms_lat[cid][1]
            cont_v[i] = v_map[r["vessel_id"]]
            cont_c[i] = CORR_IDX[r["corridor_id"]]
            cont_p[i] = PORT_IDX[r["port_id"]]
            cont_dc[i] = DC_IDX[r["dc_id"]]
            cont_z[i] = ZONE_IDX[r["thermal_zone"]]
            cont_l[i] = LINE_IDX[r["shipping_line_id"]]
            cont_d[i] = (_ts(r["discharge_ts_utc"]).astimezone(UTC).date() - BASE_DATE).days
            cont_ud[i] = (_ts(r["unload_complete_ts_cet"]).astimezone(BERLIN).date() - BASE_DATE).days
            ir = r["mode"] == "RAIL"
            cont_rail[i] = ir
            if ir:
                cont_sh[i] = sh_idx[r["planned_shuttle_id"]]
                cont_roll[i] = r["departed_shuttle_id"] != r["planned_shuttle_id"]
            else:
                cont_sh[i] = cont_c[i] * n_slots + (cont_d[i] // 3)
            ch_id = c_ched[cid]
            if ch_id in bip_ts:
                cont_bip[i] = True
                dep_t = port_slot_dep[(cont_p[i], cont_d[i] // 3)]
                cont_lead[i] = (dep_t - bip_ts[ch_id]).total_seconds() / 3600.0
            cont_samp[i] = int(r["bip_sampled_ind"]) == 1
            y_yard[i] = float(r["excess_port_yard_cdays"])
            y_rail[i] = float(r["excess_rail_cdays"])
            y_dray[i] = float(r["excess_dray_empty_cdays"])

        # 5. S1: Asymmetric convex filling-vs-draining chamber pull-back
        u_c = ch_u[cont_dc, cont_z, cont_d]
        nf_c = ch_nf[cont_dc, cont_z, cont_d]
        ex = np.maximum(0.0, u_c - 0.78)
        f_ind, d_ind = (nf_c > 0).astype(float), (nf_c <= 0).astype(float)
        X1 = np.column_stack([ex * f_ind, (ex ** 2) * f_ind, ex * d_ind, (ex ** 2) * d_ind])
        c_dum = np.column_stack([(cont_c == k).astype(float) for k in range(1, 6)])
        X1f = np.column_stack([X1, c_dum])
        b1, _, _, _ = np.linalg.lstsq(_demean(X1f, cont_v, n_v), _demean(y_yard, cont_v, n_v), rcond=None)
        pred_pb = np.maximum(0.0, X1 @ np.maximum(0.0, b1[:4]))
        rem1 = y_yard - X1f @ b1
        fe1 = (np.bincount(cont_v, weights=rem1, minlength=n_v) / np.maximum(1.0, np.bincount(cont_v, minlength=n_v)))[cont_v]
        pred_b1 = np.maximum(0.02, fe1 + X1f[:, 4:] @ b1[4:])
        pb = np.where(pred_pb > 0.0, y_yard * (pred_pb / (pred_pb + pred_b1)), 0.0)
        plug = y_yard - pb
        C1 = float(pb.sum())

        # 6. S2: Joint terminal-varying BIP lock vs Nordbahn short-consist & loco cuts
        unr_clean = cont_rail & (~cont_bip) & (~cont_roll)
        mu_base = float(y_rail[unr_clean].mean())
        sib_r = np.where(cont_rail & cont_bip & (~cont_samp), np.maximum(0.0, y_rail - mu_base), 0.0)
        roll_d = np.where(cont_rail & cont_roll, np.maximum(0.0, y_rail - mu_base), 0.0)
        base_r = np.where(cont_rail, np.where(cont_roll | (cont_bip & (~cont_samp)), np.minimum(y_rail, mu_base), y_rail), 0.0)
        sh_roll_d = np.bincount(cont_sh, weights=roll_d, minlength=n_sh)
        sh_base_d = np.bincount(cont_sh, weights=base_r, minlength=n_sh)

        act = sh_planned > 0
        cuts = []
        for p in range(3):
            mp = act & (sh_port == p)
            bc, brss = 20.0, 1e18
            for cand in (10.0, 12.0, 14.0, 16.0, 18.0, 20.0, 22.0, 24.0, 26.0, 28.0, 30.0, 32.0):
                lp = _sigmoid((cand - cont_lead) / 1.8)
                lk = np.bincount(cont_sh, weights=np.where(cont_rail & cont_bip, lp, 0.0), minlength=n_sh)
                Xp = np.column_stack([np.ones(mp.sum()), lk[mp], sh_cs[mp], sh_ld[mp]])
                bp, _, _, _ = np.linalg.lstsq(Xp, sh_rolled[mp], rcond=None)
                rss = float(np.sum((sh_rolled[mp] - Xp @ bp) ** 2))
                if rss < brss:
                    brss, bc = rss, cand
            cuts.append(bc)
        lp = _sigmoid((np.array(cuts)[cont_p] - cont_lead) / 1.8)
        n_lk = np.bincount(cont_sh, weights=np.where(cont_rail & cont_bip, lp, 0.0), minlength=n_sh)
        X2 = np.column_stack([n_lk * (sh_port == p) for p in range(3)] + [np.ones(n_sh), sh_cs, sh_ld])
        b2, _, _, _ = np.linalg.lstsq(X2[act], sh_rolled[act], rcond=None)
        bip_h = X2[:, :3] @ np.maximum(0.0, b2[:3])
        rail_h = np.maximum(0.02, X2[:, 3:] @ b2[3:])
        b_share = np.where((sh_rolled > 0) & (bip_h > 0), bip_h / np.maximum(bip_h + rail_h, 1e-9), 0.0)
        bip_d = sh_roll_d * b_share
        rail_d = sh_roll_d - bip_d + sh_base_d
        C2 = float(bip_d.sum())

        # 7. S3: Exact stock-flow shipping-line empty-depot backlog queue
        p_rows = []
        max_pt = 0
        with open(os.path.join(tdir, "depot_portal_requests_2026.csv"), encoding="utf-8") as f:
            for r in csv.DictReader(f):
                t = (_d(r["date_iso"]) - BASE_DATE).days
                max_pt = max(max_pt, t)
                p_rows.append((t, PORT_IDX[r["depot_port_id"]], LINE_IDX[r["shipping_line_id"]], int(r["confirmed_bookings"])))
        nq = max_pt + 1
        p_conf = np.zeros((3, 4, nq), dtype=int)
        for t, p, l, cf in p_rows:
            p_conf[p, l, t] = cf
        q_days = np.zeros((3, 4, nq), dtype=float)
        for p in range(3):
            for l in range(4):
                un = np.bincount(cont_ud[(cont_p == p) & (cont_l == l)], minlength=nq)
                bal = np.maximum(0.0, np.cumsum(un - p_conf[p, l]).astype(float))
                q_days[p, l] = bal / max(1.0, float(un[:365].mean()))
        q_c = q_days[cont_p, cont_l, cont_ud]
        X3 = np.column_stack([q_c * (cont_c == k) for k in range(6)])
        dow_d = np.column_stack([((cont_ud % 7) == wd).astype(float) for wd in range(1, 7)])
        X3f = np.column_stack([X3, c_dum, dow_d])
        grp3 = cont_dc * 56 + (cont_ud // 7)
        n_g3 = 4 * 56
        b3, _, _, _ = np.linalg.lstsq(_demean(X3f, grp3, n_g3), _demean(y_dray, grp3, n_g3), rcond=None)
        pred_blk = np.maximum(0.0, X3 @ np.maximum(0.0, b3[:6]))
        rem3 = y_dray - X3f @ b3
        fe3 = (np.bincount(grp3, weights=rem3, minlength=n_g3) / np.maximum(1.0, np.bincount(grp3, minlength=n_g3)))[grp3]
        pred_b3 = np.maximum(0.02, fe3 + X3f[:, 6:] @ b3[6:])
        blk = np.where(pred_blk > 0.0, y_dray * (pred_blk / (pred_blk + pred_b3)), 0.0)
        dray = y_dray - blk
        C3 = float(blk.sum())

        # 8. Corridor 2027 BCRs & Funding Slate
        bcrs = {}
        avoids = {}
        for ci, cn in enumerate(CORRIDORS):
            pl = plan[cn]
            mc = cont_c == ci
            ms = sh_corr == ci
            p27 = float(plug[mc].sum()) * pl["vg"] * pl["pf"]
            r27 = float(rail_d[ms].sum()) * pl["vg"] * pl["rf"]
            d27 = float(dray[mc].sum()) * pl["vg"] * pl["df"]
            av = (p27 * pl["t_plug"] + r27 * pl["t_rail"] + d27 * pl["t_dray"]) * pl["cap"]
            avoids[cn] = av
            bcrs[cn] = av / pl["budget"]

        ranked = sorted(CORRIDORS, key=lambda c: (-bcrs[c], c))
        funded, sp = [], 0.0
        for c in ranked:
            if sp + plan[c]["budget"] <= BUDGET_CAP_EUR + 1e-9:
                funded.append(c)
                sp += plan[c]["budget"]
        funded = sorted(funded)

        # 9. Tie out against figures.json and golden.zip CSV + XLSX
        fig = json.load(open(os.path.join(HERE, "figures.json"), encoding="utf-8"))
        assert funded == fig["funded_slate"], f"Slate mismatch: {funded} vs {fig['funded_slate']}"
        assert abs(C1 - fig["C1_coldstore_pullback_2026"]) < 0.15
        assert abs(C2 - fig["C2_phyto_rail_roll_2026"]) < 0.15
        assert abs(C3 - fig["C3_depot_backlog_2026"]) < 0.15
        for cn in CORRIDORS:
            fk = "BCR_" + cn.replace("-", "_")
            assert abs(bcrs[cn] - fig[fk]) < 0.001, f"BCR mismatch on {cn}: {bcrs[cn]:.4f} vs {fig[fk]:.4f}"

        with open(os.path.join(gdir, "weserfrucht_corridor_allocation_2027.csv"), encoding="utf-8") as f:
            csv_rows = list(csv.DictReader(f))
        assert [r["corridor_id"] for r in csv_rows] == ranked
        for r in csv_rows:
            cn = r["corridor_id"]
            assert abs(float(r["bcr_2027"]) - bcrs[cn]) < 0.001
            assert abs(float(r["avoidable_eur_2027"]) - avoids[cn]) < 0.50

        wb = load_workbook(os.path.join(gdir, "weserfrucht_corridor_capital_model_2027.xlsx"), data_only=True)
        ws1 = wb["Executive_Allocation"]
        assert abs(float(ws1["C16"].value) - sp) < 0.05
        assert abs(float(ws1["C18"].value) - sum(avoids[c] for c in funded)) < 0.50
        assert abs(float(ws1["G15"].value) - C1) < 0.15
        assert abs(float(ws1["G16"].value) - C2) < 0.15
        assert abs(float(ws1["G17"].value) - C3) < 0.15

        print(
            f"VERIFY PASS task27 (standalone from target.zip & golden.zip) | "
            f"funded={funded} | C1={C1:.1f} C2={C2:.1f} C3={C3:.1f} | "
            f"BCRs={ {c: round(bcrs[c], 3) for c in ranked} }"
        )
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    verify()
