"""task23 architecture 1, the independent verifier: the graded figures recomputed from target/ by code that shares
nothing with analysis.py (its own ticket clean-up, plant sums, pressure fit, well split and oxidation fit), each
checked against figures.json inside a tolerance far tighter than its band; the documents' filed figures read back from
the PDFs; the golden workbook and deck read back and tied to figures.json. Cell 5's monthly 2027 generation is the one
input taken from the golden workbook, re-used here to recompute the cover's share.

    python3 task23/generator/verify.py
"""
import datetime as dt
import json
import os
import re
import subprocess
import sys
import zipfile

import numpy as np
import openpyxl
import pandas as pd
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
GD = os.path.join(TASK, "golden")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
sys.path.insert(0, HERE)
import params as P  # noqa: E402

N = {"pass": 0, "fail": 0}
OLD = {"MSW-COM": "MSW", "MSW-RES": "MSW", "MSW-TS": "MSW"}


def ok(label, cond, detail=""):
    N["pass" if cond else "fail"] += 1
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else "  %s" % (detail,)))


def text(path, layout=True):
    return subprocess.run(["pdftotext"] + (["-layout"] if layout else []) + [path, "-"], capture_output=True,
                          text=True).stdout


def num(s):
    return float(s.replace(",", ""))


def main():
    f = {k: os.path.join(T, v) for k, v in P.FILES.items()}

    # ---- R1: the tickets
    t = pd.read_csv(f["tickets"], dtype=str)
    t = t[t["status"].fillna("") != "VOID"].copy()
    t["d"] = pd.to_datetime(t["ticket_date"]).dt.date
    log = pd.read_csv(f["dailylog"], dtype=str)
    active = dict(zip(pd.to_datetime(log["log_date"]).dt.date, log["active_cell"]))
    area = []
    for a, d in zip(t["disposal_area"], t["d"]):
        if isinstance(a, str) and a.strip():
            area.append(a.strip())
        else:
            area.append(active.get(d, "C5" if d >= dt.date(2025, 2, 3) else "C4"))
    t["area"] = area
    t["mat"] = t["material_code"].map(lambda c: OLD.get(c, c))
    sel = (t["area"] == "C5") & (t["mat"] == "MSW") & (t["d"] <= dt.date(2026, 10, 31))
    r1 = float(t.loc[sel, "net_tons"].astype(float).sum())
    ok("R1 municipal waste in cell 5 through October 2026 (%.0f)" % r1, abs(r1 / FIG["R1_cell5_msw_tons"] - 1) < 0.002)

    # ---- the plant's 2025 methane and the report
    s = pd.read_csv(f["scada"])
    s["y"] = s["timestamp_local"].str[:4].astype(int)
    fl = s["flare_ch4_pct"].where(s["flare_ch4_pct"] > 5.0)
    eng = s[["eng1_ch4_pct", "eng2_ch4_pct"]].mean(axis=1)
    fl = fl.fillna(eng)
    scfm = (s["flare_flow_scfm"] * fl + s["eng1_fuel_scfm"] * s["eng1_ch4_pct"].fillna(0)
            + s["eng2_fuel_scfm"] * s["eng2_ch4_pct"].fillna(0)) / 100.0
    tch4 = scfm * 60 * 0.0192 / 1000.0
    col25 = float(tch4[s["y"] == 2025].sum())
    rep = text(f["ghg2025"])
    m1 = re.search(r"Methane collected and sent to the flare and engines \(t\)\s+([\d,]+)", rep)
    m2 = re.search(r"Methane emissions \(t\)\s+([\d,]+)", rep)
    m3 = re.search(r"Area-weighted collection efficiency\s+([0-9.]+)", rep)
    ok("the report's collected methane is the plant's 2025 sum (%.0f)" % col25,
       m1 is not None and abs(num(m1.group(1)) - col25) <= 1.0)
    ce = float(m3.group(1)) if m3 else 0.0
    em = (col25 / ce - col25) * 0.9 + col25 * 0.01 if ce else 0.0
    ok("the report's figure is its own equation (%.0f)" % em, m2 is not None and abs(num(m2.group(1)) - em) <= 1.5
       and abs(em - FIG["report_2025_t"]) <= 1.5)

    # ---- the survey
    sv = text(f["survey"])
    ms = re.search(r"equivalent to ([\d,]+) metric tons", re.sub(r"\s+", " ", sv))
    c = pd.read_csv(f["campaigns"])
    c["date"] = pd.to_datetime(c["date"])
    c25 = c[c["date"].dt.year == 2025]
    ok("the survey's figure is the 2025 campaigns' mean over 8,760 hours", ms is not None and
       abs(num(ms.group(1)) - c25["site_kg_h"].mean() * 8.76) <= 1.0 and num(ms.group(1)) == FIG["survey_2025_t"])

    # ---- R2: the chambers' pressure response, fitted here from scratch
    wx = pd.read_csv(f["weather"])
    wx.index = pd.to_datetime(wx["timestamp_lst"].str[:16])
    wx = wx[~wx.index.duplicated()]
    full = pd.date_range(wx.index.min(), wx.index.max(), freq="h")
    wx = wx.reindex(full)
    baro = wx["baro_hpa"].interpolate(limit=48)
    rain6 = wx["rain_mm"].fillna(0.0).rolling(6, min_periods=1).sum()
    ch = pd.read_csv(f["chambers"])
    ch = ch[(ch["qc"] == "OK") & (ch["chamber"].isin(["AC-1", "AC-3"])) & (ch["flux_g_m2_d"] > 0)].copy()
    ch["t"] = pd.to_datetime(ch["utc"].str[:19]) - pd.Timedelta(hours=8)
    ch = ch[ch["t"].isin(full)]
    ch["grp"] = ch["chamber"] + ch["t"].dt.strftime("%Y%m")
    y = np.log(ch["flux_g_m2_d"].values)
    g = ch["grp"].values
    dT = ch["soil_temp_c"].values - ch.groupby("grp")["soil_temp_c"].transform("mean").values

    def demean(v):
        return v - pd.Series(v).groupby(g).transform("mean").values
    best = None
    for tau in (4, 6, 8, 10, 12, 14, 16, 18, 20, 24, 30, 36, 48):
        gap = baro.ewm(alpha=1.0 / tau, adjust=False).mean() - baro
        X = np.c_[demean(gap.reindex(ch["t"]).values), demean(dT), demean(rain6.reindex(ch["t"]).values)]
        b, *_ = np.linalg.lstsq(X, demean(y), rcond=None)
        sse = float(((demean(y) - X @ b) ** 2).sum())
        if best is None or sse < best[0]:
            best = (sse, tau, float(b[0]))
    _, tau, coef = best
    ok("R2 the pressure lag the chambers choose (%d h) and its response (%.3f per hPa)" % (tau, coef),
       tau == FIG["pressure_lag_h"] and abs(coef - FIG["pressure_coef_per_hpa"]) < 0.005)
    gap = baro.ewm(alpha=1.0 / tau, adjust=False).mean() - baro
    mod = np.exp(coef * gap)
    mod = mod / mod.groupby(mod.index.year).transform("mean")

    def local_to_lst(d, hhmm):
        hh, mm = map(int, hhmm.split(":"))
        aware = pd.Timestamp(dt.datetime(d.year, d.month, d.day, hh, mm)).tz_localize("America/Los_Angeles")
        return aware.tz_convert("UTC").tz_localize(None) - pd.Timedelta(hours=8)
    fac = []
    for _, r in c25.iterrows():
        a, b2 = local_to_lst(r["date"], r["start_local"]), local_to_lst(r["date"], r["end_local"])
        fac.append(float(mod[(mod.index >= a.floor("h")) & (mod.index < b2)].mean()))
    r2 = float(np.mean(c25["site_kg_h"].values / np.array(fac))) * 8.76
    ok("R2 the actual 2025 emission from the campaigns carried to every hour (%.0f)" % r2,
       abs(r2 / FIG["R2_actual_2025_t"] - 1) < 0.015)
    ok("R2 the campaigns' mean factor (%.3f)" % np.mean(fac), abs(np.mean(fac) - FIG["campaign_factor_2025"]) < 0.01)

    # ---- R3: cell 4's wells, split here by their own liquid levels; pumped wells from the work orders
    reg = pd.read_excel(f["register"], sheet_name="Wells")
    reg = reg[reg["type"] == "VW"]
    cell = {w: int(cc) if not pd.isna(cc) else int(str(w).split("-")[1][0]) for w, cc in zip(reg["well_id"], reg["cell"])}
    bot = dict(zip(reg["well_id"], reg["screen_bottom_ft"]))
    top = dict(zip(reg["well_id"], reg["screen_top_ft"]))
    w = pd.read_csv(f["wells"], dtype={"depth_to_liquid_ft": str})
    w["d"] = pd.to_datetime(w["visit_date"])
    w["cell"] = w["well_id"].map(cell)
    w["q"] = w["adj_flow_scfm"] * w["ch4_pct"] / 100.0
    lv = pd.to_numeric(w["depth_to_liquid_ft"], errors="coerce")
    w["sub"] = [np.nan if (pd.isna(x) and str(raw).upper() != "DRY") else
                (0.0 if str(raw).upper() == "DRY" or x >= bot[i] else min(1.0, (bot[i] - x) / (bot[i] - top[i])))
                for x, raw, i in zip(lv, w["depth_to_liquid_ft"], w["well_id"])]
    c4 = w[w["cell"] == 4]
    wet = set(c4[(c4["d"] >= "2023-01-01") & (c4["sub"] > 0.02)]["well_id"])
    allw = set(c4["well_id"])
    dry = allw - wet
    wo = pd.read_csv(f["workorders"])
    inst = wo[wo["description"].fillna("").str.contains("pump", case=False)
              & wo["description"].fillna("").str.contains("install", case=False)]
    pumped = set(inst["asset"].astype(str)) & wet

    def ratio(ids):
        a = c4[c4["well_id"].isin(ids) & (c4["d"].dt.year == 2022)].groupby("well_id")["q"].mean()
        b = c4[c4["well_id"].isin(ids) & (c4["d"] >= "2025-11-01") & (c4["d"] < "2026-11-01")].groupby("well_id")["q"].mean()
        k = sorted(set(a.index) & set(b.index))
        return float(b[k].sum() / a[k].sum())
    r_dry, r_pump = ratio(dry), ratio(pumped)
    Ls, after = [], []
    for i in pumped:
        x = c4[c4["well_id"] == i]
        a = x[(x["d"] >= "2025-01-01") & (x["d"] < "2025-06-01")]["q"].mean()
        b = x[(x["d"] >= "2025-07-01") & (x["d"] < "2025-11-01")]["q"].mean()
        sp = x[(x["d"] >= "2025-01-01") & (x["d"] < "2025-06-01")]["sub"].dropna()
        sq = x[x["d"] >= "2025-07-01"]["sub"].dropna()
        if sp.empty or np.isnan(a) or np.isnan(b):
            continue
        rr, s0, s1 = b / a, float(sp.iloc[-1]), float(sq.mean()) if not sq.empty else 0.0
        after.append(s1)
        if rr * s0 - s1 > 0:
            Ls.append(min(0.98, max(0.3, (rr - 1) / (rr * s0 - s1))))
    L, s1 = float(np.mean(Ls)), float(np.mean(after))
    r_wet = r_pump / (1 - L * s1)
    share = len(wet) / len(allw)
    r3 = 100 * ((1 - share) * r_dry + share * r_wet - 1)
    ok("R3 the pumped wells read from the work orders are the register's (%d)" % len(pumped),
       len(pumped) == FIG["_extra"]["cell4"]["pumped"])
    ok("R3 cell 4's generation change (%.1f per cent)" % r3, abs(r3 - FIG["R3_cell4_generation_change_pct"]) < 1.0)

    # ---- R5: the study's plots fitted here, at the golden's monthly flux
    pl = pd.read_csv(f["oxplots"]).dropna(subset=["fraction_oxidized"])
    pl = pl[pl["fraction_oxidized"] < 0.995]
    J = pl["surface_flux_g_m2_d"] / (1 - pl["fraction_oxidized"])
    covers = {"final": 0, "intermediate": 1, "active": 2}
    ci = pl["cover"].map(covers).values

    def model(X, q10, v0, v1, v2):
        Jx, Tx, cx = X
        V = np.choose(cx.astype(int), [v0, v1, v2]) * q10 ** ((Tx - 15) / 10.0)
        return V / (V + Jx)
    p, _ = curve_fit(model, (J.values, pl["soil_temp_c"].values, ci), pl["fraction_oxidized"].values,
                     p0=[2.0, 20, 15, 10], bounds=([1.0, 0.1, 0.1, 0.1], [4.0, 200, 200, 200]))
    wb = openpyxl.load_workbook(os.path.join(GD, "fernhallow_methane_2025_2027.xlsx"), data_only=True)
    c5 = wb["Cell 5"]
    soil = wx["soil_temp_10cm_c"].interpolate(limit=48)
    soil = soil[(soil.index.year >= 2016) & (soil.index.year <= 2025)]
    norm = soil.groupby(soil.index.month).mean()
    gen, oxt = 0.0, 0.0
    for k in range(12):
        g5 = float(c5.cell(row=7 + k, column=2).value)
        days = (dt.date(2027 + (k == 11), (k + 1) % 12 + 1, 1) - dt.date(2027, k + 1, 1)).days
        Jm = g5 * 1e6 / P.CELLS[5]["area"] / days
        fr = model((np.array([Jm]), np.array([norm[k + 1]]), np.array([2])), *p)[0]
        gen += g5
        oxt += g5 * fr
    r5 = 100 * oxt / gen
    ok("R5 the share cell 5's cover oxidizes in 2027 (%.1f per cent)" % r5,
       abs(r5 - FIG["R5_cell5_oxidized_share_2027_pct"]) < 0.5)
    ok("R4 the golden workbook's monthly generation sums to the figure (%.0f)" % gen,
       abs(gen - FIG["R4_cell5_generation_2027_t"]) <= 6)

    # ---- the bridge, the packages, the call and the golden files
    b = FIG["R6_bridge"]
    ok("R6 the report's bridge ties to the actual emission", FIG["report_2025_t"] + b["collection efficiency"]
       + b["oxidation"] + FIG["residual_2025_t"] == FIG["R2_actual_2025_t"])
    ok("R6 the survey's bridge ties to the actual emission",
       FIG["survey_2025_t"] + b["the hours the campaigns did not sample"] == FIG["R2_actual_2025_t"])
    plan = re.sub(r"\s+", " ", text(f["plan"], layout=False))
    ml = re.search(r"shall not exceed ([\d,]+) metric tons", plan)
    lim = num(ml.group(1)) if ml else None
    costs = {}
    for pk in "ABCDE":
        mc = re.search(r"\b%s\b[^\n]*?(\d+\.\d\d)" % pk, text(f["plan"]))
        costs[pk] = float(mc.group(1)) if mc else None
    ok("the limit is filed in the resolution (%s)" % lim, lim == P.LIMIT_T)
    ok("the costs are filed in the options paper", costs == {k: v["cost"] for k, v in P.PACKAGES.items()}, costs)
    ws = wb["Package call"]
    tab = {ws.cell(row=r, column=1).value: ws.cell(row=r, column=4).value for r in range(5, 10)}
    ok("the workbook's package table is figures.json's",
       all(tab[p] == FIG["R7_emissions_2027_t"]["package %s" % p] for p in "ABCDE"), tab)
    cheapest = min((p for p in "ABCDE" if tab[p] <= lim), key=lambda p: costs[p])
    ok("the cheapest package at or under the limit is the call (%s)" % cheapest,
       "package %s" % cheapest == FIG["R8_package"])
    wc = wb["2027 by cell"]
    for j, p in enumerate("ABCDE", 2):
        parts = sum(wc.cell(row=r, column=j).value for r in range(4, 8))
        ok("the workbook's sources sum to package %s's total (within rounding)" % p,
           abs(parts - wc.cell(row=8, column=j).value) <= 2)
    br = wb["2025 bridge"]
    vals = [br.cell(row=r, column=2).value for r in range(5, 10)]
    ok("the workbook's bridge is figures.json's", vals == [FIG["report_2025_t"], b["collection efficiency"],
                                                         b["oxidation"], FIG["residual_2025_t"],
                                                         FIG["R2_actual_2025_t"]], vals)
    ok("the workbook's cell 4 and cell 5 figures are figures.json's",
       wb["Cell 4"]["D12"].value == FIG["R3_cell4_generation_change_pct"] and wb["Cell 5"]["E4"].value ==
       FIG["R1_cell5_msw_tons"] and c5.cell(row=19, column=5).value == FIG["R5_cell5_oxidized_share_2027_pct"])
    with zipfile.ZipFile(os.path.join(GD, "council_briefing_2027_gas_package.pptx")) as z:
        slides = " ".join(re.sub(r"<[^>]+>", " ", z.read(n).decode("utf8")) for n in sorted(z.namelist())
                          if re.match(r"ppt/slides/slide\d+\.xml$", n))
        charts = " ".join(z.read(n).decode("utf8") for n in z.namelist() if re.match(r"ppt/charts/chart\d+\.xml$", n))
    ok("the deck's first slide makes the call", ("Fund package %s" % cheapest) in slides)
    ok("the deck's chart carries every package's figure",
       all(">%d<" % FIG["R7_emissions_2027_t"]["package %s" % p] in charts.replace(".0<", "<") for p in "ABCDE"))
    sub = open(os.path.join(TASK, "submission.md")).read()
    ok("the answer blocks make the same call", ("**Fund package %s" % cheapest) in sub)
    print("\n%d checks, %d passed, %d failed" % (N["pass"] + N["fail"], N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
