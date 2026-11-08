"""task3 architecture 3: the independent verifier. Reads only the cut pack, on its own code path (pandas for the
tables, pdftotext for the documents, Cooper-Jacob straight lines for the test, its own Hantush quadrature and its
own calibration search), and recomputes the call and every graded figure; then compares with figures.json.

    python3 task3/generator/verify.py <target> [figures.json]"""
import json
import math
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd

PSI_FT = 0.43353
GPM = 192.5


def pdf_text(path):
    return subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True, check=True).stdout


def hantush(u, rho):
    """W(u, rho) by Simpson's rule on x = ln(y), from ln u to ln u + 25 (a second quadrature, not solve.py's)."""
    u = np.atleast_1d(u).astype(float)
    x0 = np.log(u)[:, None]
    n = 801
    h = (np.log(60.0) - x0).clip(min=3.0) / (n - 1)
    k = np.arange(n)[None, :]
    x = x0 + h * k
    y = np.exp(x)
    f = np.exp(-y - (rho ** 2) / (4 * y))
    wts = np.where((k == 0) | (k == n - 1), 1, np.where(k % 2 == 1, 4, 2))
    return h[:, 0] / 3 * np.sum(wts * f, axis=1)


def frame(reg):
    az = math.radians(18.0)
    ua, uc = (math.sin(az), math.cos(az)), (math.cos(az), -math.sin(az))
    cx, cy = 409800.0 + uc[0] * 2500, 1687555.0 + uc[1] * 2500
    return {r["Well ID"]: ((r["Easting (ft)"] - cx) * ua[0] + (r["Northing (ft)"] - cy) * ua[1],
                           (r["Easting (ft)"] - cx) * uc[0] + (r["Northing (ft)"] - cy) * uc[1])
            for _, r in reg.iterrows()}


def kernel(T, S, B, well, obs, width, n):
    t = (np.arange(n) + 0.5) * 30.4375
    s0 = well[1] + width / 2
    imgs = [p - width / 2 for m in range(-4, 5) for p in (2 * m * width + s0, 2 * m * width - s0)]
    tot = np.zeros(n)
    for c in imgs:
        r = max(math.hypot(obs[0] - well[0], obs[1] - c), 0.5)
        if r / B > 14:
            continue
        tot += hantush(r * r * S / (4 * T * t), r / B) / (4 * math.pi * T)
    return tot


def main(target, figs=None):
    out = {}
    # documents: the limit, the schedules, the projection
    rule = pdf_text(os.path.join(target, "CVWCD_Rule_WR-4_groundwater_withdrawal_permits.pdf"))
    m = re.search(r"Harlow reach\s+OW-S.*?(\d+\.\d)\s*$", rule, re.M | re.S)
    limit = float(m.group(1))
    app = pdf_text(os.path.join(target, "reidel_road_WR-4_application_requested_schedules.pdf"))
    rates = [int(x.replace(",", "")) for x in re.findall(r"^\s*[A-D]\s+([\d,]+)\s+[\d.]+\s*$", app, re.M)]
    facs = [list(map(float, re.findall(r"\d\.\d\d", line))) for line in app.splitlines() if line.strip().startswith("Factor")]
    new_f, town_f = facs[0], facs[1]
    base = float(re.search(r"^\s*2026\s+(\d+)\s*$", app, re.M).group(1))
    growth = float(re.search(r"grow at ([\d.]+) per cent", app).group(1)) / 100
    out["doc_limit"] = limit
    out["doc_rates"] = rates
    out["application_states_no_limit"] = not re.search(r"\b9\.0\b", app)
    # register and measuring points
    reg = pd.read_excel(os.path.join(target, "cvwcd_well_register.xlsx"), sheet_name="Wells")
    mph = pd.read_excel(os.path.join(target, "cvwcd_well_register.xlsx"), sheet_name="MP history")
    fr = frame(reg)

    def mp(w, day):
        h = mph[mph["Well ID"] == w]
        for _, r in h.iterrows():
            if pd.Timestamp(r["From"]) <= day and (pd.isna(r["To"]) or r["To"] == "" or day <= pd.Timestamp(r["To"])):
                return float(r["MP elev (ft)"])
        return float(reg.loc[reg["Well ID"] == w, "MP elev (ft)"].iloc[0])
    # the test: Cooper-Jacob on the late half-log-cycle of each observation well
    lg = pd.read_excel(os.path.join(target, "PW-1_constant_rate_2026-09_field_readings.xlsx"), sheet_name="Loggers")
    tr = pd.read_csv(os.path.join(target, "PW-1_constant_rate_2026-09_transducers.csv")).drop_duplicates(["well_id", "date_time"])
    baro = pd.read_csv(os.path.join(target, "barologger_BL-2231_2026-09.csv"))
    EPOCH = pd.Timestamp("1970-01-01")
    bt = (pd.to_datetime(baro["date_time_utc"]) - EPOCH).dt.total_seconds().values
    disch = pd.read_excel(os.path.join(target, "PW-1_constant_rate_2026-09_field_readings.xlsx"), sheet_name="Discharge")
    q = (disch["Totalizer (gal)"].iloc[-1] - disch["Totalizer (gal)"].iloc[0]) / (
        (pd.Timestamp(disch["Date"].iloc[-1] + " " + disch["Time (EDT)"].iloc[-1]) -
         pd.Timestamp(disch["Date"].iloc[0] + " " + disch["Time (EDT)"].iloc[0])).total_seconds() / 60)
    on = (pd.Timestamp("2026-09-14 13:00:00") - pd.Timestamp("1970-01-01")).total_seconds()   # 09:00 EDT
    Ts, Ss = [], []
    reg_i = reg.set_index("Well ID")
    pw = (reg_i.loc["PW-1", "Easting (ft)"], reg_i.loc["PW-1", "Northing (ft)"])
    windows = {"OW-1": (0.03, 0.5), "OW-2": (0.3, 1.0)}     # Cooper-Jacob where u stays under 0.05
    for w in ("OW-1", "OW-2"):
        rows = lg[lg["Well"] == w]
        first = rows.iloc[0]
        d = tr[tr["well_id"] == w].copy()
        t = (pd.to_datetime(d["date_time"]) - EPOCH).dt.total_seconds()
        if first["Clock"] != "UTC":
            t = t + 4 * 3600
        depth = np.full(len(d), float(first["Sensor depth below MP (ft)"]))
        if len(rows) > 1:
            rh = (pd.Timestamp(rows.iloc[1]["Set"]) - EPOCH).total_seconds() + 4 * 3600
            depth[t.values >= rh] = float(rows.iloc[1]["Sensor depth below MP (ft)"])
        lvl = -(depth - (d["pressure_psi"].values - np.interp(t, bt, baro["pressure_psi"])) / PSI_FT)
        tt = (t.values - on) / 86400
        pre = (tt > -5.5) & (tt < -0.05)
        a, b = np.polyfit(tt[pre], lvl[pre], 1)[::-1]
        s = a + b * tt - lvl
        r = math.hypot(reg_i.loc[w, "Easting (ft)"] - pw[0], reg_i.loc[w, "Northing (ft)"] - pw[1])
        win = (tt >= windows[w][0]) & (tt <= windows[w][1])
        slope, icpt = np.polyfit(np.log10(tt[win]), s[win], 1)
        T = 2.303 * q * GPM / (4 * math.pi * slope)
        t0 = 10 ** (-icpt / slope)
        Ts.append(T)
        Ss.append(2.25 * T * t0 / r ** 2)
    T, S = float(np.mean(Ts)), float(np.exp(np.mean(np.log(Ss))))
    out["T_cj"] = round(T)
    out["S_cj"] = S
    # the record
    mor = pd.read_csv(os.path.join(target, "harlow_springs_MOR_well_production_2009-2026.csv"))
    mor["well"] = mor["source"].replace({"WELL 1": "TW-1", "WELL 2": "TW-2"})
    mor["gal"] = mor["metered_volume"] * np.where(mor["units"] == "1000 gal", 1000, 1)
    per = pd.PeriodIndex(mor["report_month"], freq="M")
    mor["gpm"] = mor["gal"] / (per.days_in_month * 1440)
    months = pd.period_range("2005-01", "2046-12", freq="M")
    n = len(months)
    idx = {p: i for i, p in enumerate(months)}
    q1, q2 = np.zeros(n), np.zeros(n)
    for _, r in mor.iterrows():
        (q1 if r["well"] == "TW-1" else q2)[idx[pd.Period(r["report_month"], "M")]] = r["gpm"]
    lv = {}
    ms = pd.read_csv(os.path.join(target, "mill_street_MW_water_levels_2008-2026.csv"))
    ms = ms[~ms["remarks"].fillna("").str.contains("running")]
    s = np.full(n, np.nan)
    for _, r in ms.iterrows():
        day = pd.Timestamp(pd.to_datetime(r["date"], format="%m/%d/%Y"))
        s[idx[day.to_period("M")]] = mp("MS-MW", day) - r["depth_to_water_ft"]
    lv["MS-MW"] = s
    net = pd.read_csv(os.path.join(target, "cvwcd_network_water_levels_2005-2026.csv")).drop_duplicates(["site_id", "date"])
    net = net[net["qualifier"].fillna("") != "E"]
    for _, r in net.iterrows():
        day = pd.Timestamp(r["date"])
        lv.setdefault(r["site_id"], np.full(n, np.nan))[idx[day.to_period("M")]] = mp(r["site_id"], day) - r["dtw_ft_below_mp"]
    yrs = np.array([p.year for p in months])
    win05 = (yrs >= 2005) & (yrs <= 2008)
    win_ms = np.array([pd.Period("2008-06", "M") <= p <= pd.Period("2009-02", "M") for p in months])

    def att(w):
        wn = win_ms if w == "MS-MW" else win05
        nat = np.nanmean(np.vstack([lv[c] - np.nanmean(lv[c][wn]) for c in ("CV-02", "CV-11")]), axis=0)
        return np.nanmean(lv[w][wn]) + nat - lv[w]
    A = {w: att(w) for w in ("MS-MW", "CV-07", "OW-S")}
    out["msmw_2025"] = float(np.nanmean(A["MS-MW"][yrs == 2025]))
    fit = np.array([pd.Period("2009-03", "M") <= p <= pd.Period("2026-09", "M") for p in months])

    def town_model(w, B, a1, a2):
        return sum(np.convolve(np.diff(np.concatenate([[0.0], qq])) * GPM, kernel(T, S, B, fr[src], fr[w], 5000.0, n))[:n]
                   for qq, src in ((a1, "TW-1"), (a2, "TW-2")))
    best = None
    for B in np.geomspace(1500, 12000, 44):
        e = 0.0
        for w in ("MS-MW", "CV-07", "OW-S"):
            mdl = town_model(w, B, q1, q2)
            ok = fit & ~np.isnan(A[w])
            e += float(np.sum((A[w][ok] - mdl[ok]) ** 2))
        if best is None or e < best[0]:
            best = (e, B)
    B = best[1]
    out["B"] = round(B)
    fut = np.array([p >= pd.Period("2026-10", "M") for p in months])
    proj = np.array([base * (1 + growth) ** (p.year - 2026) * town_f[p.month - 1] if p >= pd.Period("2026-10", "M") else 0
                     for p in months])
    a1, a2 = np.where(fut, 0.56 * proj, q1), np.where(fut, 0.44 * proj, q2)
    town = town_model("OW-S", B, a1, a2)
    peaks = {}
    for rate in rates:
        newq = np.array([rate * new_f[p.month - 1] if p >= pd.Period("2027-04", "M") else 0.0 for p in months])
        fld = sum(np.convolve(np.diff(np.concatenate([[0.0], newq / 2])) * GPM,
                              kernel(T, S, B, fr[src], fr["OW-S"], 5000.0, n))[:n] for src in ("PW-1", "PW-2"))
        peaks[rate] = float((town + fld)[yrs == 2046].max())
    out["peaks"] = {str(k): round(v, 2) for k, v in peaks.items()}
    ok = [r for r in rates if peaks[r] <= limit]
    out["call"] = max(ok) if ok else None
    ft = lambda x: int(math.floor(x + 0.5))
    out["peaks_ft"] = {str(k): ft(v) for k, v in peaks.items()}
    out["msmw_2025_ft"] = ft(out["msmw_2025"])
    fails = []
    if figs:
        F = json.load(open(figs))
        if out["call"] != F["call"]:
            fails.append("call %s against %s" % (out["call"], F["call"]))
        if out["peaks_ft"] != F["peaks_ft"]:
            fails.append("peaks %s against %s" % (out["peaks_ft"], F["peaks_ft"]))
        if out["msmw_2025_ft"] != F["msmw_2025_ft"]:
            fails.append("MS-MW %s against %s" % (out["msmw_2025_ft"], F["msmw_2025_ft"]))
        if abs(out["doc_limit"] - F["limit"]) > 1e-9:
            fails.append("limit")
    if not out["application_states_no_limit"]:
        fails.append("the application restates the limit")
    print(json.dumps(out, indent=1))
    print("verify: %s" % ("PASS" if not fails else "FAIL " + "; ".join(fails)))
    return 0 if not fails else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None))
