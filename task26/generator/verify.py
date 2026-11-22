"""Independent standalone verifier for task26 (v3).

Reads ONLY task26/target.zip, recomputes every conformed substation figure and pool aggregate from scratch using
pandas/numpy/sqlite3/openpyxl (importing ZERO generator modules: no core.py, analysis.py, or results.py),
and verifies exact agreement with task26/golden.zip and task26/generator/figures.json.
"""
import csv
import datetime as dt
import io
import json
import os
import shutil
import sqlite3
import tempfile
import zipfile

import numpy as np
import openpyxl
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TARGET_ZIP = os.path.join(TASK, "target.zip")
GOLDEN_ZIP = os.path.join(TASK, "golden.zip")
FIG_PATH = os.path.join(HERE, "figures.json")

UTC = dt.timezone.utc
CET_FIXED = dt.timezone(dt.timedelta(hours=1))
BASE_UTC = dt.datetime(2025, 12, 31, 23, 0, tzinfo=UTC)
MONTH_DAYS = (31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31)
HOUR_MONTH = np.concatenate([np.full(d * 24, m, dtype=int) for m, d in enumerate(MONTH_DAYS)])
WINTER_MONTHS = (0, 1, 10, 11)
HEATING_MONTHS = (0, 1, 2, 9, 10, 11)
COMM_MONTHS = (8, 9)
WINTER_HOURS = np.isin(HOUR_MONTH, WINTER_MONTHS)
HEATING_HOURS = np.isin(HOUR_MONTH, HEATING_MONTHS)
COMM_HOURS = np.isin(HOUR_MONTH, COMM_MONTHS)
V_NOM_LV = 22.0
V_NOM_HV = 66.0
TAP_STEP = 0.0125


def main():
    fig = json.load(open(FIG_PATH, encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="task26-verify-")
    try:
        with zipfile.ZipFile(TARGET_ZIP) as zt:
            zt.extractall(tmp)

        # 1. Transformer & feeder register (no industrial_park_zone column)
        wb_tx = openpyxl.load_workbook(os.path.join(tmp, "substation_transformer_register.xlsx"), data_only=True)
        df_sub = pd.DataFrame(wb_tx["Substations"].values)
        df_sub.columns = df_sub.iloc[0]
        df_sub = df_sub.iloc[1:].reset_index(drop=True)
        targets = sorted(df_sub.loc[df_sub["modernization_status"] != "modernized_2023_2024", "substation_id"].tolist())
        refs = sorted(df_sub.loc[df_sub["modernization_status"] == "modernized_2023_2024", "substation_id"].tolist())
        all_subs = targets + refs
        sub_meta = {r["substation_id"]: dict(firm=float(r["firm_n1_mva"]), R=float(r["r_ohm"]), X=float(r["x_ohm"]))
                    for _, r in df_sub.iterrows()}

        df_fdr = pd.DataFrame(wb_tx["Feeders"].values)
        df_fdr.columns = df_fdr.iloc[0]
        df_fdr = df_fdr.iloc[1:].reset_index(drop=True)
        assert "industrial_park_zone" not in df_fdr.columns, "industrial_park_zone must not be shipped!"
        feeders_by_sub = {}
        f_lookup = {}
        for _, r in df_fdr.iterrows():
            s = r["substation_id"]
            fid = r["scada_feeder_id"]
            feeders_by_sub.setdefault(s, []).append((fid, r["customer_class"]))
            f_lookup[fid] = (s, len(feeders_by_sub[s]) - 1)

        # 2. Crosswalk
        xw = pd.read_csv(os.path.join(tmp, "feeder_id_crosswalk.csv"))
        fmap = dict(zip(xw["legacy_dms_id"], xw["scada_feeder_id"]))
        for fid in xw["scada_feeder_id"]:
            fmap[fid] = fid

        # 3. Substation hourly SCADA (no v_hv_kv column; dedup latest extract_ts, parse mixed clocks, interp summer nulls)
        sc = pd.read_csv(os.path.join(tmp, "scada_substation_hourly_2026.csv"))
        assert "v_hv_kv" not in sc.columns, "v_hv_kv must not be shipped in zone-substation SCADA!"
        h_idx = np.empty(len(sc), dtype=int)
        for i, (ts_s, clk) in enumerate(zip(sc["timestamp_local"], sc["scada_clock"])):
            if clk == "CET_Standard":
                d = dt.datetime.strptime(ts_s, "%d.%m.%Y %H:%M").replace(tzinfo=CET_FIXED).astimezone(UTC)
            else:
                d = dt.datetime.fromisoformat(ts_s).astimezone(UTC)
            h_idx[i] = int(round((d - BASE_UTC).total_seconds() / 3600.0))
        sc["h"] = h_idx
        sc = sc.sort_values("extract_ts").drop_duplicates(subset=["substation_id", "h"], keep="last")
        sc = sc.sort_values(["substation_id", "h"])

        sub_p60, v_lv, taps = {}, {}, {}
        for s, g in sc.groupby("substation_id"):
            assert len(g) == 8760
            sub_p60[s] = g["p_active_mw"].to_numpy(dtype=float)
            v_lv[s] = g["v_lv_kv"].interpolate(method="linear").to_numpy(dtype=float)
            taps[s] = g["ltc_tap_step"].to_numpy(dtype=int)

        # 4. GSP 66 kV voltages & radial 66 kV sub-transmission corridors (4 corridors including upstream modernized hubs)
        base_pd = pd.Timestamp("2025-12-31T23:00Z")
        df_gsp = pd.read_csv(os.path.join(tmp, "gsp_66kv_voltages_2026.csv"))
        df_gsp["h"] = ((pd.to_datetime(df_gsp["ts_utc"], utc=True) - base_pd).dt.total_seconds() // 3600).astype(int)
        gsp_v = {}
        for gid, g in df_gsp.groupby("gsp_id"):
            g = g.sort_values("h")
            gsp_v[gid] = g["v_hv_kv"].to_numpy(dtype=float)

        df_cor = pd.read_csv(os.path.join(tmp, "subtransmission_66kv_lines.csv"))
        corridors = {}
        for cid, g in df_cor.groupby("corridor_id"):
            segs = [(r["from_bus"], r["to_bus"], float(r["length_km"]), float(r["r_ohm_per_km"]), float(r["x_ohm_per_km"]))
                    for _, r in g.iterrows()]
            to_set = {x[1] for x in segs}
            root = [x[0] for x in segs if x[0] not in to_set][0]
            by_from = {x[0]: x for x in segs}
            ordered = []
            cur = root
            while cur in by_from:
                ordered.append(by_from[cur])
                cur = by_from[cur][1]
            corridors[cid] = {"gsp": root, "segs": ordered}

        # 5. Feeder hourly SCADA (kW -> MW), class hourly aggregates p_cls & monthly 15-min registers
        f_p60 = {s: np.zeros((len(feeders_by_sub[s]), 8760)) for s in all_subs}
        df_fs = pd.read_csv(os.path.join(tmp, "feeder_scada_hourly_2026.csv"))
        df_fs["scada_id"] = df_fs["feeder_code"].map(fmap)
        df_fs["h"] = ((pd.to_datetime(df_fs["ts_utc"], utc=True) - base_pd).dt.total_seconds() // 3600).astype(int)
        for fid, g in df_fs.groupby("scada_id"):
            s, fi = f_lookup[fid]
            f_p60[s][fi, g["h"].to_numpy()] = g["p_active_kw"].to_numpy(dtype=float) / 1000.0

        p_cls = {}
        for s in all_subs:
            pc = {c: np.zeros(8760) for c in ("residential_heat", "commercial_mixed", "industrial_batch", "maritime_port")}
            for fi, (_fid, fcls) in enumerate(feeders_by_sub[s]):
                pc[fcls] += f_p60[s][fi]
            p_cls[s] = pc

        f_m15 = {s: np.zeros((len(feeders_by_sub[s]), 12)) for s in all_subs}
        df_m15 = pd.read_csv(os.path.join(tmp, "feeder_demand_registers_monthly_2026.csv"))
        df_m15["scada_id"] = df_m15["feeder_code"].map(fmap)
        df_m15["m"] = df_m15["billing_month"].str.slice(5, 7).astype(int) - 1
        for _, r in df_m15.iterrows():
            s, fi = f_lookup[r["scada_id"]]
            f_m15[s][fi, int(r["m"])] = float(r["max_15min_demand_mw"])
        f_p60_m = {s: np.column_stack([f_p60[s][:, HOUR_MONTH == m].max(axis=1) for m in range(12)]) for s in all_subs}

        # 6. S1: strip top-4 regional SVD factors across other substations -> innovation correlation R_mats
        all_log = {}
        for s in all_subs:
            L = np.log(np.maximum(f_p60[s] / f_p60[s].mean(axis=1, keepdims=True), 1e-4))
            L -= L.mean(axis=1, keepdims=True)
            all_log[s] = L
        R_mats = {}
        for s in all_subs:
            other_L = np.vstack([all_log[s2] for s2 in all_subs if s2 != s])
            _, _, Vt = np.linalg.svd(other_L, full_matrices=False)
            F = Vt[:4]
            E = all_log[s] - (all_log[s] @ F.T) @ F
            R = np.corrcoef(E)
            np.fill_diagonal(R, 1.0)
            R_mats[s] = np.clip(R, 0.0, 1.0)

        def raw_quad(s, m_list):
            nf = len(feeders_by_sub[s])
            idx_h = np.where(np.isin(HOUR_MONTH, m_list))[0]
            pk_h = int(idx_h[np.argmax(sub_p60[s][idx_h])])
            d = np.zeros(nf)
            for i in range(nf):
                rel = np.mean([(f_m15[s][i, m] - f_p60_m[s][i, m]) / f_p60_m[s][i, m] for m in m_list])
                d[i] = max(0.0, rel) * f_p60[s][i, pk_h]
            return float(np.sqrt(max(0.0, float(d @ R_mats[s] @ d))))

        # 7. Sep-Oct active-only commissioning 15-min log on Fossheim & Lindberg -> calibrate k_ord on within-hour surge
        assert not os.path.exists(os.path.join(tmp, "pq_archive_15min_2026.csv")), "old full-year PQ file must not exist!"
        df_cpq = pd.read_csv(os.path.join(tmp, "pq_commissioning_autumn2026.csv"))
        assert list(df_cpq.columns) == ["substation_id", "ts_utc", "sub_p15_mw"], f"unexpected PQ cols {list(df_cpq.columns)}"
        assert len(df_cpq) == 11712, f"expected 11,712 Sep-Oct rows, got {len(df_cpq)}"
        df_cpq["k"] = ((pd.to_datetime(df_cpq["ts_utc"], utc=True) - base_pd).dt.total_seconds() // 900).astype(int)
        obs_c, raw_c = [], []
        for r in sorted(df_cpq["substation_id"].unique()):
            g = df_cpq[df_cpq["substation_id"] == r].sort_values("k")
            sp15 = g["sub_p15_mw"].to_numpy(dtype=float).reshape(-1, 4)
            obs_ex = float((sp15.max(axis=1) - sub_p60[r][COMM_HOURS]).max())
            obs_c.append(obs_ex)
            raw_c.append(raw_quad(r, list(COMM_MONTHS)))
        k_ord = float(sum(obs_c) / sum(raw_c))

        # 8. S2: coupled 4-corridor 66 kV impedance inversion (including upstream hubs) anchored to peak-month net kVARh
        wb_rev = openpyxl.load_workbook(os.path.join(tmp, "revenue_meter_monthly_2026.xlsx"), data_only=True)
        df_rev = pd.DataFrame(wb_rev["Monthly_Revenue_Meters"].values)
        df_rev.columns = df_rev.iloc[0]
        df_rev = df_rev.iloc[1:].reset_index(drop=True)
        net_kvarh = {s: np.zeros(12) for s in all_subs}
        for _, r in df_rev.iterrows():
            m = int(str(r["billing_month"]).split("-")[1]) - 1
            net_kvarh[r["substation_id"]][m] = float(r["net_reactive_energy_kvarh"])

        q_h_all = {}
        for cid, c_info in corridors.items():
            v_gsp = gsp_v[c_info["gsp"]]
            segs = c_info["segs"]
            subs = [seg[1] for seg in segs]
            m = len(subs)
            r_segs = [seg[2] * seg[3] for seg in segs]
            x_segs = [seg[2] * seg[4] for seg in segs]

            p_sub = np.vstack([sub_p60[s] for s in subs])
            vlv_m = np.vstack([v_lv[s] for s in subs])
            tp_m = np.vstack([taps[s] for s in subs])
            tau = (V_NOM_LV / V_NOM_HV) * (1.0 + TAP_STEP * tp_m)
            r_tx = np.array([sub_meta[s]["R"] for s in subs])
            x_tx = np.array([sub_meta[s]["X"] for s in subs])

            dv_rp = np.zeros((m, 8760))
            for i in range(m):
                for e in range(i + 1):
                    dv_rp[i] += (r_segs[e] * p_sub[e:].sum(axis=0)) / V_NOM_HV
            x_sh = np.zeros((m, m))
            for i in range(m):
                for j in range(m):
                    x_sh[i, j] = sum(x_segs[:min(i, j) + 1]) / V_NOM_HV

            y = v_gsp[None, :] * tau - vlv_m - tau * dv_rp - (r_tx[:, None] * p_sub) / V_NOM_LV
            pk_m = int(HOUR_MONTH[int(np.argmax(p_sub.sum(axis=0)))])
            amask = HOUR_MONTH == pk_m
            q_bar_m = np.array([net_kvarh[s][pk_m] / (1000.0 * int(amask.sum())) for s in subs])
            M_all = tau[:, None, :] * x_sh[:, :, None] + np.eye(m)[:, :, None] * (x_tx[:, None] / V_NOM_LV)[:, None, :]
            M_inv = np.linalg.inv(np.transpose(M_all, (2, 0, 1)))
            q_y_a = (M_inv[amask] @ y[:, amask].T[:, :, None]).squeeze(-1).mean(axis=0)
            delta_pt = np.linalg.solve(M_inv[amask].mean(axis=0), q_bar_m - q_y_a)
            Q_hat = (M_inv @ (y + delta_pt[:, None]).T[:, :, None]).squeeze(-1).T

            for i, s in enumerate(subs):
                top5 = np.argsort(p_sub[i])[-5:]
                q_h_all[s] = float(np.mean(Q_hat[i, top5]))

        # 9. S3: measure per-class tan_phi directly from SQLite AMI (p_kw, q_kvar) & run multi-class 3-phase bus-sag OLS
        df_gis = pd.read_csv(os.path.join(tmp, "gis_lateral_connectivity_2026.csv"))
        assert len(df_gis) == 440, f"expected 440 laterals (40 x 11), got {len(df_gis)}"
        conn = sqlite3.connect(os.path.join(tmp, "ami_lateral_telemetry_2026.db"))
        df_ami_lat = pd.read_sql_query(
            "SELECT l.lateral_id, SUM(h.p_kw * h.q_kvar) AS pq_sum, SUM(h.p_kw * h.p_kw) AS pp_sum "
            "FROM lateral_hourly h JOIN laterals l ON h.lateral_idx = l.lateral_idx "
            "GROUP BY l.lateral_id",
            conn,
        )
        n_ami_db = conn.execute("SELECT COUNT(*) FROM laterals").fetchone()[0]
        conn.close()
        assert n_ami_db == 220, f"expected 220 AMI laterals in DB, got {n_ami_db}"
        df_ami_lat = df_ami_lat.merge(df_gis[["lateral_id", "customer_class"]], on="lateral_id", how="left")
        grp_tp = df_ami_lat.groupby("customer_class")[["pq_sum", "pp_sum"]].sum()
        tphi_ami = (grp_tp["pq_sum"] / grp_tp["pp_sum"]).to_dict()
        tp_res = float(tphi_ami["residential_heat"])
        tp_com = float(tphi_ami["commercial_mixed"])

        df_bus = pd.read_csv(os.path.join(tmp, "substation_phase_bus_voltages_2026.csv"))
        df_bus["h"] = ((pd.to_datetime(df_bus["ts_utc"], utc=True) - base_pd).dt.total_seconds() // 3600).astype(int)
        v_bus = {}
        for s, g in df_bus.groupby("substation_id"):
            g = g.sort_values("h")
            v_bus[s] = np.vstack([g["va_kv"].to_numpy(dtype=float),
                                  g["vb_kv"].to_numpy(dtype=float),
                                  g["vc_kv"].to_numpy(dtype=float)])

        # 10. Recompute every substation independently
        recomp = {}
        for s in all_subs:
            p60 = sub_p60[s]
            pk_h = int(np.argmax(p60))
            p60_pk = float(p60[pk_h])
            p15 = p60_pk + k_ord * raw_quad(s, list(WINTER_MONTHS))
            q_h = q_h_all[s]
            s15 = float(np.sqrt(p15 ** 2 + q_h ** 2))

            v_ex = v_bus[s] - v_bus[s].mean(axis=0, keepdims=True)
            p_res = p_cls[s]["residential_heat"]
            p_com = p_cls[s]["commercial_mixed"]
            p_bal = p_cls[s]["industrial_batch"] + p_cls[s]["maritime_port"]
            X = np.column_stack([np.ones(8760), p_res, p_com, p_bal])
            B, *_ = np.linalg.lstsq(X, v_ex.T, rcond=None)
            b_res, b_com = B[1], B[2]
            c_res = 3.0 * (sub_meta[s]["R"] + sub_meta[s]["X"] * tp_res) / V_NOM_LV
            c_com = 3.0 * (sub_meta[s]["R"] + sub_meta[s]["X"] * tp_com) / V_NOM_LV
            dw_res = -b_res / c_res
            dw_com = -b_com / c_com
            dw_res -= dw_res.mean()
            dw_com -= dw_com.mean()
            w_pk = (1.0 / 3.0) + (dw_res * p_res[pk_h] + dw_com * p_com[pk_h]) / p60[pk_h]
            w_max = float(w_pk.max())

            lim_mva = 3.0 * w_max * s15
            load_pct = 100.0 * lim_mva / sub_meta[s]["firm"]
            relief = max(0.0, lim_mva - 0.85 * sub_meta[s]["firm"])
            recomp[s] = dict(p15=p15, q_h=q_h, w_max_pct=100.0 * w_max, lim_mva=lim_mva,
                             loading_pct=load_pct, relief=relief)

        # 11. Compare against figures.json AND golden.zip
        for s in targets:
            rec = fig["substations"][s]
            v = recomp[s]
            assert abs(v["p15"] - rec["p15_peak_mw"]) <= 0.01, (s, "p15", v["p15"], rec["p15_peak_mw"])
            assert abs(v["q_h"] - rec["q_peak_h_mvar"]) <= 0.01, (s, "q_h", v["q_h"], rec["q_peak_h_mvar"])
            assert abs(v["w_max_pct"] - rec["w_max_pct"]) <= 0.01, (s, "w", v["w_max_pct"], rec["w_max_pct"])
            assert abs(v["lim_mva"] - rec["lim_mva"]) <= 0.01, (s, "mva", v["lim_mva"], rec["lim_mva"])
            assert abs(v["loading_pct"] - rec["loading_pct"]) <= 0.01, (s, "load", v["loading_pct"], rec["loading_pct"])
            assert abs(v["relief"] - rec["relief_mva"]) <= 0.01, (s, "rel", v["relief"], rec["relief_mva"])

        c1 = sum(recomp[s]["p15"] for s in targets)
        c2 = sum(recomp[s]["q_h"] for s in targets)
        c3 = float(np.mean([recomp[s]["w_max_pct"] for s in targets]))
        tot_rel = sum(recomp[s]["relief"] for s in targets)
        assert abs(c1 - fig["c1_total_p15_mw"]) <= 0.02
        assert abs(c2 - fig["c2_total_qpeak_mvar"]) <= 0.02
        assert abs(c3 - fig["c3_mean_lim_phase_pct"]) <= 0.02
        assert abs(tot_rel - fig["total_relief_mva"]) <= 0.02

        with zipfile.ZipFile(GOLDEN_ZIP) as zg:
            csv_txt = zg.read("vesterdal_substation_conformed_2026.csv").decode("utf-8")
            rows = list(csv.DictReader(io.StringIO(csv_txt)))
            assert len(rows) == 7
            for r in rows:
                s = r["substation_id"]
                assert abs(float(r["firm_n1_loading_pct"]) - recomp[s]["loading_pct"]) <= 0.01

        print(f"VERIFY PASS: independent recomputation from target.zip matches figures.json & golden.zip "
              f"(k_ord={k_ord:.4f}, tp_res={tp_res:.4f}, tp_com={tp_com:.4f}, "
              f"C1={c1:.2f} MW, C2={c2:.2f} MVAr, C3={c3:.2f}%, TotalRelief={tot_rel:.2f} MVA)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
