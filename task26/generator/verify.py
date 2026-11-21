"""Independent standalone verifier for task26.

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
WINTER_HOURS = np.isin(HOUR_MONTH, WINTER_MONTHS)
V_NOM_LV = 22.0
V_NOM_HV = 66.0
TAP_STEP = 0.0125


def main():
    fig = json.load(open(FIG_PATH, encoding="utf-8"))
    tmp = tempfile.mkdtemp(prefix="task26-verify-")
    try:
        with zipfile.ZipFile(TARGET_ZIP) as zt:
            zt.extractall(tmp)

        # 1. Transformer & feeder register
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
        feeders_by_sub = {}
        f_lookup = {}
        zmap, nz = {}, 1
        for _, r in df_fdr.iterrows():
            s = r["substation_id"]
            fid = r["scada_feeder_id"]
            raw_zn = r["industrial_park_zone"]
            zn = "" if pd.isna(raw_zn) else str(raw_zn).strip()
            if zn.lower() in ("none", "", "na", "nan"):
                pg = 0
            else:
                if zn not in zmap:
                    zmap[zn] = nz
                    nz += 1
                pg = zmap[zn]
            feeders_by_sub.setdefault(s, []).append((fid, pg))
            f_lookup[fid] = (s, len(feeders_by_sub[s]) - 1)

        # 2. Crosswalk
        xw = pd.read_csv(os.path.join(tmp, "feeder_id_crosswalk.csv"))
        fmap = dict(zip(xw["legacy_dms_id"], xw["scada_feeder_id"]))
        for fid in xw["scada_feeder_id"]:
            fmap[fid] = fid

        # 3. Substation hourly SCADA (dedup latest extract_ts, parse mixed timestamps, interp summer nulls)
        sc = pd.read_csv(os.path.join(tmp, "scada_substation_hourly_2026.csv"))
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

        sub_p60, v_hv, v_lv, taps = {}, {}, {}, {}
        for s, g in sc.groupby("substation_id"):
            assert len(g) == 8760
            sub_p60[s] = g["p_active_mw"].to_numpy(dtype=float)
            v_hv[s] = g["v_hv_kv"].to_numpy(dtype=float)
            v_lv[s] = g["v_lv_kv"].interpolate(method="linear").to_numpy(dtype=float)
            taps[s] = g["ltc_tap_step"].to_numpy(dtype=int)

        # 4. Feeder hourly SCADA (kW -> MW) & monthly 15-min registers
        base_pd = pd.Timestamp("2025-12-31T23:00Z")
        f_p60 = {s: np.zeros((len(feeders_by_sub[s]), 8760)) for s in all_subs}
        df_fs = pd.read_csv(os.path.join(tmp, "feeder_scada_hourly_2026.csv"))
        df_fs["scada_id"] = df_fs["feeder_code"].map(fmap)
        df_fs["h"] = ((pd.to_datetime(df_fs["ts_utc"], utc=True) - base_pd).dt.total_seconds() // 3600).astype(int)
        for fid, g in df_fs.groupby("scada_id"):
            s, fi = f_lookup[fid]
            f_p60[s][fi, g["h"].to_numpy()] = g["p_active_kw"].to_numpy(dtype=float) / 1000.0

        f_m15 = {s: np.zeros((len(feeders_by_sub[s]), 12)) for s in all_subs}
        df_m15 = pd.read_csv(os.path.join(tmp, "feeder_demand_registers_monthly_2026.csv"))
        df_m15["scada_id"] = df_m15["feeder_code"].map(fmap)
        df_m15["m"] = df_m15["billing_month"].str.slice(5, 7).astype(int) - 1
        for _, r in df_m15.iterrows():
            s, fi = f_lookup[r["scada_id"]]
            f_m15[s][fi, int(r["m"])] = float(r["max_15min_demand_mw"])
        f_p60_m = {s: np.column_stack([f_p60[s][:, HOUR_MONTH == m].max(axis=1) for m in range(12)]) for s in all_subs}

        # 5. Modernized sites 15-min PQ calibration
        df_rpq = pd.read_csv(os.path.join(tmp, "pq_archive_15min_2026.csv"))
        df_rpq["k"] = ((pd.to_datetime(df_rpq["ts_utc"], utc=True) - base_pd).dt.total_seconds() // 900).astype(int)
        park_c, indep_c, dqdp_l = [], [], []
        ref_p15, ref_q15 = {}, {}
        for r in refs:
            g = df_rpq[df_rpq["substation_id"] == r].sort_values("k")
            nf = len(feeders_by_sub[r])
            sp15 = g["sub_p15_mw"].to_numpy(dtype=float).reshape(8760, 4)
            sq15 = g["sub_q15_mvar"].to_numpy(dtype=float).reshape(8760, 4)
            ref_p15[r], ref_q15[r] = sp15, sq15
            fp15 = np.stack([g[f"f{i+1:02d}_p15_mw"].to_numpy(dtype=float).reshape(8760, 4) for i in range(nf)])
            dpf = fp15[:, WINTER_HOURS, :] - f_p60[r][:, WINTER_HOURS, None]
            cc = np.corrcoef(dpf.reshape(nf, -1))
            for i in range(nf):
                for j in range(i + 1, nf):
                    gi, gj = feeders_by_sub[r][i][1], feeders_by_sub[r][j][1]
                    (park_c if (gi > 0 and gi == gj) else indep_c).append(float(cc[i, j]))
            dps = (sp15[WINTER_HOURS, :] - sp15[WINTER_HOURS, :].mean(axis=1, keepdims=True)).ravel()
            dqs = (sq15[WINTER_HOURS, :] - sq15[WINTER_HOURS, :].mean(axis=1, keepdims=True)).ravel()
            dqdp_l.append(float(np.dot(dps, dqs) / np.dot(dps, dps)))
        rho_park = float(np.mean(park_c))
        rho_indep = float(np.mean(indep_c))
        dq_dp = float(np.mean(dqdp_l))

        def raw_quad(s, m_list):
            nf = len(feeders_by_sub[s])
            idx_h = np.where(np.isin(HOUR_MONTH, m_list))[0]
            pk_h = int(idx_h[np.argmax(sub_p60[s][idx_h])])
            d = np.zeros(nf)
            for i in range(nf):
                rel = np.mean([(f_m15[s][i, m] - f_p60_m[s][i, m]) / f_p60_m[s][i, m] for m in m_list])
                d[i] = max(0.0, rel) * f_p60[s][i, pk_h]
            vs = 0.0
            for i in range(nf):
                vs += d[i] ** 2
                for j in range(i + 1, nf):
                    gi, gj = feeders_by_sub[s][i][1], feeders_by_sub[s][j][1]
                    rho = rho_park if (gi > 0 and gi == gj) else rho_indep
                    vs += 2.0 * rho * d[i] * d[j]
            return float(np.sqrt(max(0.0, vs)))

        obs_l, raw_l = [], []
        for r in refs:
            for m in WINTER_MONTHS:
                hm = HOUR_MONTH == m
                obs_l.append(float(ref_p15[r][hm, :].max() - sub_p60[r][hm].max()))
                raw_l.append(raw_quad(r, [m]))
            obs_l.append(float(ref_p15[r].max() - sub_p60[r].max()))
            raw_l.append(raw_quad(r, list(WINTER_MONTHS)))
        k_ord = float(sum(obs_l) / sum(raw_l))

        # 6. Revenue meter monthly net kVARh
        wb_rev = openpyxl.load_workbook(os.path.join(tmp, "revenue_meter_monthly_2026.xlsx"), data_only=True)
        df_rev = pd.DataFrame(wb_rev["Monthly_Revenue_Meters"].values)
        df_rev.columns = df_rev.iloc[0]
        df_rev = df_rev.iloc[1:].reset_index(drop=True)
        net_kvarh = {s: np.zeros(12) for s in all_subs}
        for _, r in df_rev.iterrows():
            m = int(str(r["billing_month"]).split("-")[1]) - 1
            net_kvarh[r["substation_id"]][m] = float(r["net_reactive_energy_kvarh"])

        # 7. 3-phase bus voltages & SQLite AMI lateral telemetry
        df_bus = pd.read_csv(os.path.join(tmp, "substation_phase_bus_voltages_2026.csv"))
        df_bus["h"] = ((pd.to_datetime(df_bus["ts_utc"], utc=True) - base_pd).dt.total_seconds() // 3600).astype(int)
        v_bus = {}
        for s, g in df_bus.groupby("substation_id"):
            g = g.sort_values("h")
            v_bus[s] = np.vstack([g["va_kv"].to_numpy(dtype=float),
                                  g["vb_kv"].to_numpy(dtype=float),
                                  g["vc_kv"].to_numpy(dtype=float)])

        conn = sqlite3.connect(os.path.join(tmp, "ami_lateral_telemetry_2026.db"))
        lats_df = pd.read_sql_query("SELECT lateral_idx, lateral_id, substation_id FROM laterals ORDER BY lateral_idx", conn)
        win_idx = np.where(WINTER_HOURS)[0]
        win_set = set(win_idx.tolist())
        lat_v = {s: np.full((36, 8760), np.nan) for s in all_subs}
        lat_p = {s: np.full((36, 8760), np.nan) for s in all_subs}
        lpos = {}
        cnt = {s: 0 for s in all_subs}
        for _, r in lats_df.iterrows():
            s = r["substation_id"]
            lpos[int(r["lateral_idx"])] = (s, cnt[s])
            cnt[s] += 1
        cur = conn.execute("SELECT lateral_idx, hour_idx, v_volts, p_kw FROM lateral_hourly")
        for li, hi, vv, pk in cur:
            if hi in win_set:
                s, pos = lpos[li]
                lat_v[s][pos, hi] = vv
                lat_p[s][pos, hi] = pk
        conn.close()

        # 8. Recompute every substation independently
        recomp = {}
        for s in all_subs:
            p60_pk = float(sub_p60[s].max())
            p15 = p60_pk + k_ord * raw_quad(s, list(WINTER_MONTHS))

            tau = (V_NOM_LV / V_NOM_HV) * (1.0 + TAP_STEP * taps[s])
            dv = v_hv[s] * tau - v_lv[s]
            q_unc = (V_NOM_LV * dv - sub_meta[s]["R"] * sub_p60[s]) / sub_meta[s]["X"]
            pk_h = int(np.argmax(sub_p60[s]))
            pk_m = int(HOUR_MONTH[pk_h])
            hm = HOUR_MONTH == pk_m
            q_hat = q_unc - float(np.mean(q_unc[hm])) + net_kvarh[s][pk_m] / (1000.0 * int(hm.sum()))
            top5 = np.argsort(sub_p60[s])[-5:]
            q_h = float(np.mean(q_hat[top5]))
            q15 = q_h + dq_dp * (p15 - p60_pk)
            s15 = float(np.sqrt(p15 ** 2 + q15 ** 2))

            vb = v_bus[s] * (230.0 / V_NOM_LV)
            vcm = vb.mean(axis=0, keepdims=True)
            vt = vb - vcm
            rv = lat_v[s] - vcm
            d_vt = np.diff(vt[:, win_idx], axis=1)
            d_rv = np.diff(rv[:, win_idx], axis=1)
            d_lp = np.diff(lat_p[s][:, win_idx], axis=1)
            ph_assign = np.zeros(36, dtype=int)
            for li in range(36):
                y, xp = d_rv[li], d_lp[li]
                rss = []
                for ph in range(3):
                    X = np.column_stack([d_vt[ph], xp])
                    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
                    rss.append(float(np.sum(y ** 2)) if beta[0] <= 0.1 else float(np.sum((y - X @ beta) ** 2)))
                ph_assign[li] = int(np.argmin(rss))
            w_list = []
            for h in top5:
                bal = sub_p60[s][h] * 1000.0 - lat_p[s][:, h].sum()
                ph_kw = np.array([lat_p[s][ph_assign == ph, h].sum() + bal / 3.0 for ph in range(3)])
                w_list.append(float(ph_kw.max() / ph_kw.sum()))
            w_max = float(np.mean(w_list))
            lim_mva = 3.0 * w_max * s15
            load_pct = 100.0 * lim_mva / sub_meta[s]["firm"]
            relief = max(0.0, lim_mva - 0.85 * sub_meta[s]["firm"])
            recomp[s] = dict(p15=p15, q_h=q_h, w_max_pct=100.0 * w_max, lim_mva=lim_mva,
                             loading_pct=load_pct, relief=relief)

        # 9. Compare against figures.json AND golden.zip
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
              f"(C1={c1:.2f} MW, C2={c2:.2f} MVAr, C3={c3:.2f}%, TotalRelief={tot_rel:.2f} MVA)")
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


if __name__ == "__main__":
    main()
