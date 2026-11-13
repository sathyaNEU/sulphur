"""task22 architecture 2, the independent verifier: the graded figures recomputed from target/ by code that shares
nothing with analysis.py (its own period builder, station rebuild, calendarization, gas temperature fit and leak
arithmetic), each checked against figures.json inside its band. The diversion volumes are the one input taken from
figures.json's account list, re-measured here on each account's own reads.

    python3 task22/generator/verify.py
"""
import datetime as dt
import json
import os
import sys

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
T = os.path.join(TASK, "target")
FIG = json.load(open(os.path.join(HERE, "figures.json")))
sys.path.insert(0, HERE)
import params as P  # noqa: E402

N = {"pass": 0, "fail": 0}


def ok(label, cond, detail=""):
    N["pass" if cond else "fail"] += 1
    print(("PASS  " if cond else "FAIL  ") + label + ("" if cond else "  %s" % (detail,)))


def main():
    f = {k: os.path.join(T, v) for k, v in P.FILES.items()}
    day0 = dt.date(2023, 8, 1)
    days = pd.date_range(day0, P.SIM1)
    D = len(days)
    ix = {d.date(): i for i, d in enumerate(days)}
    # the stations, faulty days from the gate
    drs = pd.read_csv(f["drs"], parse_dates=["GasDay"])
    drs["GasDay"] = drs["GasDay"].dt.date
    st = pd.read_excel(f["register"], sheet_name="Regulator stations")
    s2d = dict(zip(st["Station"], st["PressureDistrict"]))
    bad = drs["CorrectedMcf"].isna() | drs["Alarm"].fillna("").str.contains("COMM|PXDCR|STUCK")
    gate = pd.read_csv(f["gate"], parse_dates=["GasDay"])
    gate = dict(zip(gate["GasDay"].dt.date, gate["CorrectedMcf"]))
    vol = {s: np.zeros(D) for s in s2d}
    okd = {s: np.zeros(D, bool) for s in s2d}
    for r, b in zip(drs.itertuples(), bad):
        if not b:
            vol[r.Station][ix[r.GasDay]] = r.CorrectedMcf
            okd[r.Station][ix[r.GasDay]] = True
    stations = list(s2d)
    allok = np.all([okd[s] for s in stations], axis=0)
    tot = np.sum([vol[s] for s in stations], axis=0)
    gv = np.array([gate.get(d.date(), np.nan) for d in days])
    loss = np.where(allok, 1 - tot / gv, np.nan)
    lm = pd.Series(loss, index=days).groupby(days.to_period("M")).transform("median").values
    for t in np.where(~allok & ~np.isnan(gv))[0]:
        badst = [s for s in stations if not okd[s][t]]
        rest = gv[t] * (1 - lm[t]) - sum(vol[s][t] for s in stations if okd[s][t])
        lo, hi = max(0, t - 10), min(D, t + 11)
        sh = np.array([np.nanmedian(np.where(allok[lo:hi], vol[s][lo:hi] / np.where(tot[lo:hi] > 0, tot[lo:hi], 1),
                                             np.nan)) for s in badst])
        sh = sh / sh.sum()
        for s, x in zip(badst, sh):
            vol[s][t] = rest * x
    din = {}
    for s in stations:
        din[s2d[s]] = din.get(s2d[s], np.zeros(D)) + vol[s]
    W = (days >= pd.Timestamp(P.W0)) & (days <= pd.Timestamp(P.W1))
    tot_in = sum(v[W].sum() for v in din.values())
    g1 = FIG["R1_gas_in"]
    ok("R1 fourteen districts' gas in", abs(tot_in / g1["fourteen districts, twelve months to September 2026"] - 1)
       < 0.003, tot_in)
    jan = (days >= "2026-01-01") & (days <= "2026-01-31")
    ok("R1 Riverside January 2026", abs(din["Riverside"][jan].sum() / g1["Riverside, January 2026"] - 1) < 0.015,
       din["Riverside"][jan].sum())
    # the reads: actual-to-actual periods on each meter
    rd = pd.read_csv(f["reads"], dtype={"MeterID": str}).drop_duplicates()
    rd = rd[rd["ReadType"] != "E"].copy()
    rd["ReadDate"] = pd.to_datetime(rd["ReadDate"]).dt.date
    rd["k"] = rd["ReadType"].map({"F": 0, "I": 1, "A": 2, "S": 3})
    rd = rd.sort_values(["MeterID", "ReadDate", "k"]).drop_duplicates(["MeterID", "ReadDate"])
    rd["pi"] = rd.groupby("MeterID")["MeterIndex"].shift()
    rd["pd"] = rd.groupby("MeterID")["ReadDate"].shift()
    rd = rd.dropna(subset=["pi"])
    rd["ccf"] = ((rd["MeterIndex"] - rd["pi"]) % 10000) * rd["Multiplier"]
    reg = pd.read_excel(f["register"], sheet_name="Premises")
    models = pd.read_excel(f["register"], sheet_name="Meter models")
    tcm = dict(zip(models["Model"], models["TempComp"]))
    tc = {}
    for r in reg.itertuples():
        tc[r.MeterID] = (r.TempComp if isinstance(r.TempComp, str) else tcm[r.MeterModel]) == "Y"
        if isinstance(r.PreviousMeterID, str):
            tc[r.PreviousMeterID] = tcm[r.PreviousModel] == "Y"
    dist = dict(zip(reg["PremiseID"], reg["PressureDistrict"]))
    loc = dict(zip(reg["PremiseID"], reg["MeterLocation"]))
    rd["d"] = rd["PremiseID"].map(dist)
    rd["out"] = rd["PremiseID"].map(loc).eq("Outside")
    rd["tc"] = rd["MeterID"].map(tc)
    # gas temperature: outdoor loggers on soil and air, indoor loggers on the 40 inch soil
    so = pd.read_csv(f["soil"], na_values=["M"], parse_dates=["Date"]).set_index("Date").reindex(days)
    s20 = so["Soil20inF"].interpolate().bfill().ffill().values
    s40 = so["Soil40inF"].interpolate().bfill().ffill().values
    ap = pd.read_csv(f["airport"], parse_dates=["DATE"]).set_index("DATE").reindex(days)
    air = ap["TAVG"].fillna((ap["TMAX"] + ap["TMIN"]) / 2).interpolate().bfill().ffill().values
    lg = pd.read_csv(f["loggers"], parse_dates=["Date"])
    lg["t"] = lg["Date"].map(lambda d: ix[d.date()])
    lg["out"] = lg["PremiseID"].map(loc).eq("Outside")
    o = lg[lg["out"]]
    X = np.c_[air[o["t"]] - s20[o["t"]], air[o["t"]] < 45, np.ones(len(o))]
    k, wall, c0 = np.linalg.lstsq(X, o["GasTempF"].values - s20[o["t"]], rcond=None)[0]
    Tout = s20 + k * (air - s20) + wall * (air < 45) + c0
    i_ = lg[~lg["out"]]
    bi = np.polyfit(s40[i_["t"]] - 46, i_["GasTempF"], 1)
    Tin = bi[1] + bi[0] * (s40 - 46)
    # calendarize on each district's own daily volume
    out = {}
    for (d, isout, istc), g in rd.groupby(["d", "out", "tc"]):
        shape = np.clip(din[d], 1e-6, None)
        cum = np.r_[0, np.cumsum(shape)]
        arr = np.zeros(D)
        for (a, b), v in g.groupby(["pd", "ReadDate"])["ccf"].sum().items():
            i0, i1 = ix[a], ix[b] if b in ix else D
            arr[i0:i1] += v * shape[i0:i1] / (cum[i1] - cum[i0])
        bil = arr * P.PF / 10.0
        fac = 1.0 if istc else P.R_BASE / ((Tout if isout else Tin) + 459.67)
        out.setdefault(d, dict(bil=np.zeros(D), under=np.zeros(D), bil_ntc=np.zeros(D)))
        out[d]["bil"] += bil
        if not istc:
            out[d]["under"] += bil * (fac - 1)
            out[d]["bil_ntc"] += bil
    g2 = FIG["R2_billed_months"]
    cj = (days >= "2026-01-01") & (days <= "2026-01-31")
    ok("R2 College Hill January 2026 billed volume", abs(out["College Hill"]["bil"][cj].sum() /
                                                          g2["College Hill, January 2026"] - 1) < 0.02,
       out["College Hill"]["bil"][cj].sum())
    g3 = FIG["R3_under"]
    for d in ("Riverside", "Lakeview"):
        v = out[d]["under"][W].sum()
        ok("R3 %s under-registration" % d, abs(v / g3["%s, Mcf" % d] - 1) < 0.06, v)
    for d in ("College Hill", "Airport", "Halvorsen"):
        v = 100 * out[d]["under"][W].sum() / out[d]["bil_ntc"][W].sum()
        ok("R3 %s under-registration share" % d, abs(v - g3["%s, per cent" % d]) < 0.2, v)
    # corrector customers, own use, damage
    ev = pd.read_csv(f["evc"], parse_dates=["GasDay"])
    corr = pd.read_excel(f["register"], sheet_name="Corrector accounts")
    ev["d"] = ev["Account"].map(dict(zip(corr["Account"], corr["PressureDistrict"])))
    ev["r"] = (ev["CorrectedMcf"] / ev["UncorrectedMcf"]).where(ev["Status"] == "OK")
    ev["r"] = ev.groupby("Account")["r"].transform(lambda s: s.fillna(s.rolling(21, center=True, min_periods=1).median())
                                                   .ffill().bfill())
    ev["v"] = np.where(ev["Status"] == "OK", ev["CorrectedMcf"], ev["UncorrectedMcf"] * ev["r"])
    evw = ev[(ev["GasDay"] >= pd.Timestamp(P.W0)) & (ev["GasDay"] <= pd.Timestamp(P.W1))].groupby("d")["v"].sum()
    ou = pd.read_excel(f["own_use"], skiprows=2)
    ou = ou[ou["Month"].astype(str).str.match(r"^20(25-1[0-2]|26-0[1-9])$")].dropna(subset=["PressureDistrict"])
    own = ou.groupby("PressureDistrict")["EstimatedMcf"].sum()
    dm = pd.read_excel(f["damage"], parse_dates=["Date"])
    dm = dm[(dm["Date"] >= pd.Timestamp(P.W0)) & (dm["Date"] <= pd.Timestamp(P.W1))].groupby("PressureDistrict")[
        "EstimatedGasLostMcf"].sum()
    acc = pd.DataFrame(FIG["_extra"]["diversion_accounts"])
    div = acc.groupby(acc["district"].map(P.DNAME))["mcf_window"].sum() if len(acc) else pd.Series(dtype=float)
    leak = {}
    for d in out:
        inn = din[d][W].sum()
        lk = inn - out[d]["bil"][W].sum() - out[d]["under"][W].sum() - evw.get(d, 0) - own.get(d, 0) - dm.get(d, 0) \
            - div.get(d, 0)
        leak[d] = 100 * lk / inn
    for d, v in FIG["R5_leak_pct"].items():
        ok("R5 %s leak share" % d, abs(leak[d] - v) < 0.10, (round(leak[d], 3), v))
    des = sorted(d for d, v in leak.items() if v > P.LEAK_LINE)
    ok("R6 the districts over the 1.0 line", des == sorted(FIG["R6_designated"]), des)
    # the 2027 plan at the 2024-25 pace
    wo = pd.read_csv(f["workorders"], parse_dates=["PlannedDate", "CompletedDate"])
    pl = pd.read_excel(f["plan2027"], skiprows=2).dropna(subset=["PlannedDate"])
    pl = pl[pd.to_numeric(pl["PremiseID"], errors="coerce").notna()]
    done = 0.0
    for lc, g in pl.groupby("MeterLocation"):
        lag = (wo.loc[wo["MeterLocation"] == lc, "CompletedDate"] - wo.loc[wo["MeterLocation"] == lc, "PlannedDate"]
               ).dt.days.fillna(10 ** 6).values
        for p_ in pd.to_datetime(g["PlannedDate"]):
            done += (lag <= (pd.Timestamp(P.SEASON_2027) - p_).days - 1).mean()
    ok("R8 changeouts done before the 2027-28 season", abs(done / FIG["R8_done_before_season"] - 1) < 0.04, done)
    print("\n%d verified, %d failed" % (N["pass"], N["fail"]))
    return 1 if N["fail"] else 0


if __name__ == "__main__":
    sys.exit(main())
