"""task3 verify: an independent recomputation from the shipped files, by another road.

pandas readers instead of the analysis module's; the rain-snow temperature from binned snow shares at the SNOTEL
pillows (the bin where half the precipitation stays as snow) instead of a logistic fit, applied as a sharp line; the
lapse rate from the SNOTEL pair; storms in the airport's hourly record grouped on a pandas index; log-Pearson III by the
moments of the logs with the station skew weighted with the regional skew, written here. It must land on the golden's
span, its 1 per cent flood within 8 per cent of the golden's, the golden's 5,000 cfs cells and its two largest
floods; the drainage-area transfer on the 140 ft span; and it reads back every format the pack ships (CSV, text,
workbook, PDF) with a positive control on each.
"""
import json
import os
import re
import subprocess
import sys

import numpy as np
import pandas as pd
from scipy import stats

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
KM = 3280.84


def lp3(x, gr, mse_r, aep):
    lx = np.log10(np.asarray(x, float))
    n = len(lx)
    m, s, g = lx.mean(), lx.std(ddof=1), stats.skew(lx, bias=False)
    ga = abs(g)
    a = -0.33 + 0.08 * ga if ga <= 0.9 else -0.52 + 0.30 * ga
    b = 0.94 - 0.26 * ga if ga <= 1.5 else 0.55
    mse_s = 10 ** (a - b * np.log10(n / 10.0))
    gw = (mse_r * g + mse_s * gr) / (mse_r + mse_s)
    return 10 ** (m + stats.pearson3.ppf(1 - aep, gw) * s)


def rdb(path):
    lines = [l.rstrip("\n") for l in open(path) if not l.startswith("#")]
    hdr = lines[0].split("\t")
    body = [l.split("\t") for l in lines[2:] if l]
    return pd.DataFrame(body, columns=hdr)


def pdf(path):
    return re.sub(r"\s+", " ", subprocess.run(["pdftotext", path, "-"], capture_output=True, text=True).stdout)


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    ok = []
    # every format read back, positive control on each
    std = pdf(os.path.join(TGT, "pelton_county_road_standards_ch7_excerpt.pdf"))
    rep = pdf(os.path.join(TGT, "wsdot_region3_flood_frequency_excerpt.pdf"))
    tm = pdf(os.path.join(TGT, "hess_tm_durrow_creek_bridge_span_ratings.pdf"))
    ok.append(("pdf control", "shortest whose rated flow" in std and "regional skew coefficient" in rep and "Rated flow" in tm))
    gr = float(re.search(r"regional skew coefficient of the logarithms of annual peak flows for Region 3 is (-?\d\.\d+)", rep).group(1))
    mse_r = float(re.search(r"mean square error of (\d\.\d+)", rep).group(1))
    rated = {}
    lay = subprocess.run(["pdftotext", "-layout", os.path.join(TGT, "hess_tm_durrow_creek_bridge_span_ratings.pdf"), "-"],
                         capture_output=True, text=True).stdout
    for span, q in re.findall(r"^\s*[ABC]\s+(140|185|240)\s+[\d.]+\s+([\d,]+)\s", lay, re.M):
        rated[int(span)] = int(q.replace(",", ""))
    ok.append(("memo spans", sorted(rated) == [140, 185, 240]))
    # the workbook through pandas
    xl = pd.read_excel(os.path.join(TGT, "region3_basin_characteristics.xlsx"), sheet_name=None, header=None)
    eb = xl["Elevation bands"]
    head = [str(h) for h in eb.iloc[2]]
    bands = eb.iloc[3:].dropna(how="all")
    zc = np.array([np.mean([float(x) for x in str(v).split("-")]) for v in bands[0]])
    ar = bands[next(j for j, h in enumerate(head) if h.startswith("Coyner"))].astype(float).values
    ac = bands[next(j for j, h in enumerate(head) if h.startswith("Durrow"))].astype(float).values / 640.0
    gauged = xl["Gauged basins"].iloc[3:].dropna(how="all")
    area_r = float(gauged[gauged[0].astype(str) == "12183450"][2].iloc[0])
    dk = xl["Durrow Ck at Ransom Bar Rd"]
    area_c = float(dk[dk[0] == "Drainage area (sq mi)"][1].iloc[0])
    ok.append(("workbook control", len(zc) > 15 and area_c > 50))
    # the valley record: each station at its own elevation, multi-day totals spread
    v = pd.read_csv(os.path.join(TGT, "ghcnd_tessel_daily_1950-2025.csv"), dtype=str).fillna("")
    v["DATE"] = pd.to_datetime(v["DATE"])
    last_old = v[v.STATION == "USC00458114"].DATE.max()
    v = v[(v.STATION == "USC00458114") | (v.DATE > last_old)].copy()
    v["z"] = np.where(v.STATION == "USC00458117", 1340.0, 1180.0)
    v["p"] = pd.to_numeric(v.PRCP, errors="coerce")
    md = pd.to_numeric(v.MDPR, errors="coerce")
    da = pd.to_numeric(v.DAPR, errors="coerce")
    v = v.set_index("DATE")
    for d, m_, n_ in zip(v.index[md.notna().values], md[md.notna()].values, da[md.notna()].values):
        for k in range(int(n_)):
            dd = d - pd.Timedelta(days=k)
            if dd in v.index:
                v.loc[dd, "p"] = m_ / n_
    v["t"] = ((pd.to_numeric(v.TMAX, errors="coerce") + pd.to_numeric(v.TMIN, errors="coerce")) / 2 - 32) * 5 / 9
    ok.append(("valley control", len(v) > 27000))
    r = pd.read_csv(os.path.join(TGT, "ghcnd_durrow_ridge_daily_1950-2025.csv"), dtype=str).fillna("")
    r["DATE"] = pd.to_datetime(r["DATE"])
    r = r.set_index("DATE")
    r["p"] = pd.to_numeric(r.PRCP, errors="coerce")

    def snotel(name):
        s = pd.read_csv(os.path.join(TGT, name), comment="#")
        s.columns = ["date", "swe", "prec", "tmax", "tmin", "tavg", "depth"]
        s["date"] = pd.to_datetime(s["date"])
        return s.set_index("date")
    sh, sc = snotel("snotel_1187_hatchet_meadow_daily.csv"), snotel("snotel_1203_corbel_ridge_daily.csv")
    # the lapse rate from the SNOTEL pair on days both catch 0.5 in or more
    dph = sh.prec.shift(-1) - sh.prec
    dpc = sc.prec.shift(-1) - sc.prec
    j = pd.concat([sh.tavg, sc.tavg, dph, dpc], axis=1, keys=["th", "tc", "ph", "pc"]).dropna()
    j = j[(j.ph >= 0.5) & (j.pc >= 0.5)]
    lapse = float(((j.th - j.tc) * 5 / 9 / (1470 / KM)).median())
    # the rain-snow temperature: the half-degree bin where the snow share crosses one half
    shares = []
    for s in (sh, sc):
        dp = s.prec.shift(-1) - s.prec
        ds = s.swe.shift(-1) - s.swe
        t = (s.tavg - 32) * 5 / 9
        f = pd.DataFrame(dict(t=t, sh=(ds / dp).clip(0, 1), dp=dp)).dropna()
        f = f[(f.dp >= 0.4) & (f.dp <= 8) & (~f.index.month.isin([6, 7, 8, 9]))]
        shares.append(f)
    f = pd.concat(shares)
    bins = np.arange(-4, 6.01, 0.5)
    mid = f.groupby(pd.cut(f.t, bins)).sh.mean()
    centres = np.array([iv.mid for iv in mid.index])
    vals = mid.values
    i = int(np.argmax(vals < 0.5))
    t50 = float(np.interp(0.5, [vals[i], vals[i - 1]], [centres[i], centres[i - 1]]))
    # orographic gain from the warm storms' ridge and valley totals; storms as wet runs of 0.10 in or more
    vp = v.p.fillna(0.0)
    wet = vp >= 0.10
    run_id = (wet != wet.shift()).cumsum()
    storms = []
    for _, grp in vp[wet].groupby(run_id[wet]):
        if grp.sum() >= 1.0:
            storms.append(grp)
    ratios = []
    for grp in storms:
        tv = np.average(v.t.reindex(grp.index).fillna(v.t.mean()), weights=grp.values)
        zv = v.z.reindex(grp.index).iloc[0]
        if zv + (tv - t50) / lapse * KM < 2710 + 1500:
            continue
        days = list(grp.index) + [grp.index[-1] + pd.Timedelta(days=1)]
        rp = r.p.reindex(days)
        if rp.isna().any():
            continue
        ratios.append(rp.sum() / grp.sum())
    rr = float(np.median(ratios))
    g = (rr - 1) / (1.71 - rr * 0.18)
    # the airport's routine hourly reports, on a full hourly index
    lcd = pd.read_csv(os.path.join(TGT, "lcd_tessel_field_hourly_1950-2025.csv"), dtype=str,
                      usecols=["DATE", "ELEVATION", "REPORT_TYPE", "HourlyDryBulbTemperature", "HourlyPrecipitation"])
    ok.append(("hourly control", len(lcd) > 600000 and (lcd.REPORT_TYPE == "FM-16").sum() > 1000))
    lcd = lcd[lcd.REPORT_TYPE == "FM-15"]
    zv_air = float(lcd.ELEVATION.iloc[0]) / 0.3048
    hour = pd.to_datetime(lcd.DATE).dt.floor("h")
    temp = (pd.to_numeric(lcd.HourlyDryBulbTemperature.str.rstrip("s*"), errors="coerce") - 32) * 5 / 9
    pr = pd.to_numeric(lcd.HourlyPrecipitation.str.rstrip("s*").replace("T", "0.001"), errors="coerce")
    full = pd.date_range("1950-10-01 00:00", "2025-09-30 23:00", freq="h")
    H = pd.DataFrame({"t": temp.values, "p": pr.values}, index=hour.values).groupby(level=0).last().reindex(full)
    wet = (H.p.fillna(0.0) >= 0.005).values
    tt, pp = H.t.values, H.p.fillna(0.0).values
    # storms: wet hours joined across dry spells of six hours or less
    idx = np.nonzero(wet)[0]
    brk = np.nonzero(np.diff(idx) > 7)[0]
    starts = np.concatenate([[idx[0]], idx[brk + 1]])
    ends = np.concatenate([idx[brk], [idx[-1]]])
    # floods with their peak hours
    ann = rdb(os.path.join(TGT, "usgs_12183450_coyner_r_annual_peaks.txt"))
    pot = rdb(os.path.join(TGT, "usgs_12183450_coyner_r_peaks_above_base.txt"))
    pot_tm = dict(zip(pot.peak_dt, pot.peak_tm))
    ann["peak_tm"] = [tm if tm else pot_tm.get(d, "12:00") for d, tm in zip(ann.peak_dt, ann.peak_tm)]
    fl = pd.concat([ann[["peak_dt", "peak_tm", "peak_va"]], pot[["peak_dt", "peak_tm", "peak_va"]]])
    fl["ts"] = pd.to_datetime(fl.peak_dt + " " + fl.peak_tm)
    fl["q"] = fl.peak_va.astype(float)
    fl["d"] = fl.ts.dt.date
    fl = fl.sort_values("q").groupby("d").last()
    ann_q = ann.peak_va.astype(float).values
    b = float(F["equations"]["100"]["b"])

    def depth(areas, tv, zv):
        tz = tv - lapse * (zc - zv) / KM
        rain = (tz > t50).astype(float)
        rel = 1 + g * (zc - 1000) / 1000
        return float((areas * rel * rain).sum() / areas.sum())
    series = {}
    for d, row in fl.iterrows():
        i = int((row.ts - full[0]) / pd.Timedelta(hours=1))
        k = np.searchsorted(starts, i, side="right") - 1
        if k < 0:
            continue
        last = min(ends[k], i)
        if i - last > 36 or last < starts[k]:
            continue
        h = np.arange(starts[k], last + 1)
        h = h[wet[h] & np.isfinite(tt[h])]
        if len(h) < 2:
            continue
        tv = float(np.average(tt[h], weights=pp[h]))
        dr, dc = depth(ar, tv, zv_air), depth(ac, tv, zv_air)
        if dr <= 0.01:
            continue
        wy = d.year + (1 if d.month >= 10 else 0)
        series[wy] = max(series.get(wy, 0.0), row.q * (area_c / area_r) ** b * dc / dr)
    vals = np.array([series[y] for y in sorted(series)])
    golden = F["golden_raw"]
    mine = {a: lp3(vals, gr, mse_r, a) for a in (0.5, 0.1, 0.04, 0.02, 0.01, 0.002)}
    span = min(sp for sp, q in rated.items() if q >= mine[0.01])
    r0 = lp3(ann_q, gr, mse_r, 0.01) * (area_c / area_r) ** b
    span0 = min(sp for sp, q in rated.items() if q >= r0)
    top2 = sorted(series, key=lambda y: -series[y])[:2]
    k5 = lambda x: int(round(x / 5000.0)) * 5000  # noqa: E731
    ok.append(("span", span == F["call_span_ft"]))
    # log-Pearson III by plain moments without the low-flood test (not the filed expected-moments fit) runs lower in the tail
    ok.append(("1 per cent within 8 per cent", abs(mine[0.01] / golden["0.01"] - 1) < 0.08))
    ok.append(("the graded flows land the golden's 5,000 cfs cells", k5(mine[0.5]) == F["q50_5000"] and k5(mine[0.01]) == F["q01_5000"]))
    ok.append(("the two largest floods", sorted(top2) == sorted(F["top2"])))
    ok.append(("drainage-area transfer files 140 ft", span0 == 140))
    gcsv = pd.read_csv(os.path.join(TASK, "golden", "durrow_creek_estimated_annual_peaks.csv"), dtype=str).fillna("")
    ok.append(("golden csv agrees with figures.json", len(gcsv) == 75 and list(gcsv.estimated_peak_flow_cfs.astype(int)) ==
               [p["cfs"] for p in F["peaks"]] and list(gcsv.qualifier) == [p["qualifier"] for p in F["peaks"]]))
    big = gcsv[gcsv.qualifier == ""].astype({"estimated_peak_flow_cfs": int}).nlargest(2, "estimated_peak_flow_cfs")
    ok.append(("golden csv's two largest are the report's", sorted(big.water_year.astype(int)) == sorted(F["top2"])))
    rep_g = pdf(os.path.join(TASK, "golden", "durrow_creek_bridge_hydrology_report.pdf"))
    ok.append(("golden report states the span, the flows, the bands and the floods",
               "Build the %d ft span" % F["call_span_ft"] in rep_g and "{:,}".format(F["q01_5000"]) in rep_g
               and "{:,}".format(F["q50_5000"]) in rep_g and all(F["bands"][s] in rep_g for s in F["bands"])
               and all(str(y) in rep_g for y in F["top2"])))
    print("verify: lapse %.2f (SNOTEL pair) t50 %.2f (binned) g %.3f | floods %d years %d | 1%% %.0f (golden %.0f) | "
          "quantiles %s | top2 %s | drainage area %.0f -> %d ft | span %d" % (
              lapse, t50, g, len(fl), len(series), mine[0.01], golden["0.01"],
              {a: int(round(x)) for a, x in mine.items()}, top2, r0, span0, span))
    for name, good in ok:
        print("%s  %s" % ("PASS" if good else "FAIL", name))
    allok = all(good for _, good in ok)
    print("VERIFY", "PASS" if allok else "FAIL")
    return 0 if allok else 1


if __name__ == "__main__":
    sys.exit(main())
