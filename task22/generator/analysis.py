"""task22 architecture 2: the analysis read back from the cut pack alone (never from the simulation), with every
method choice a switch, so the golden and each hurried route run on the same code.

    route options:
      cal     shape (each district's regulator-station daily sendout) | fit (base plus degree days fitted per
              district) | uniform (even by day) | hdd65 (by heating degree days below 65 F)
      temp    soil (the loggers' gas temperature tied to the soil at 20 inches and the air) | evc (the loggers tied
              to the commercial correctors' gas temperature) | logger_air (the study memo's straight line on the
              airport's air) | monthly_air (the 2019 consultant's monthly mean) | none (60 F)
      div     golden (collapses split into diversion and absence by the summer base load and the winter heating
              response) | all (every collapse booked as diversion) | none
      drs     rebuild (faulty station days rebuilt from the gate balance) | raw (as recorded, gaps as zero)
      z       dak | hy | fit (every corrector put on the real-gas basis: the pressure-and-temperature-only
              correctors' volumes times the supercompressibility factor, from Dranchuk and Abou-Kassem, from Hall and
              Yarborough, or fitted on the EVC-II stations' own records) | rec (every corrector's volume as recorded)
"""
import datetime as dt
import os

import numpy as np
import pandas as pd

import params as P
import zfactor as ZF

DAY0 = dt.date(2023, 8, 1)
DAY1 = P.SIM1
DAYS = pd.date_range(DAY0, DAY1, freq="D")
ND = len(DAYS)
MONTHS = pd.period_range("2023-10", "2026-09", freq="M")
WIN = (DAYS >= pd.Timestamp(P.W0)) & (DAYS <= pd.Timestamp(P.W1))
GOLDEN = dict(cal="shape", temp="soil", div="golden", drs="rebuild", z="dak", k_scale=1.0, in_shift=0.0,
              dmg_scale=1.0, own_scale=1.0, div_scale=1.0, home_cut=0.7, df_cut=0.3, df_tmax=10)


def _d(x):
    return pd.to_datetime(x).dt.date


def _di(d):
    return (d - DAY0).days


def load(target):
    f = {k: os.path.join(target, v) for k, v in P.FILES.items()}
    F = {}
    F["reads"] = pd.read_csv(f["reads"], dtype={"MeterID": str})
    F["reads"]["ReadDate"] = _d(F["reads"]["ReadDate"])
    reg = pd.read_excel(f["register"], sheet_name=None)
    F["register"] = reg["Premises"]
    F["models"] = reg["Meter models"]
    F["stations"] = reg["Regulator stations"]
    F["correctors"] = reg["Corrector accounts"]
    F["accounts"] = pd.read_csv(f["accounts"])
    for c in ("StartDate", "EndDate"):
        F["accounts"][c] = pd.to_datetime(F["accounts"][c]).dt.date
    F["drs"] = pd.read_csv(f["drs"])
    F["drs"]["GasDay"] = _d(F["drs"]["GasDay"])
    F["gate"] = pd.read_csv(f["gate"])
    F["gate"]["GasDay"] = _d(F["gate"]["GasDay"])
    F["evc"] = pd.read_csv(f["evc"])
    F["evc"]["GasDay"] = _d(F["evc"]["GasDay"])
    F["airport"] = pd.read_csv(f["airport"])
    F["airport"]["DATE"] = _d(F["airport"]["DATE"])
    F["soil"] = pd.read_csv(f["soil"], na_values=["M"])
    F["soil"]["Date"] = _d(F["soil"]["Date"])
    F["loggers"] = pd.read_csv(f["loggers"])
    F["loggers"]["Date"] = _d(F["loggers"]["Date"])
    F["damage"] = pd.read_excel(f["damage"])
    F["damage"]["Date"] = pd.to_datetime(F["damage"]["Date"]).dt.date
    F["own_use"] = pd.read_excel(f["own_use"], skiprows=2).dropna(subset=["Month"])
    F["own_use"] = F["own_use"][F["own_use"]["Month"].astype(str).str.match(r"^\d{4}-\d{2}$")]
    F["lauf_report"] = pd.read_excel(f["lauf_report"], skiprows=2)
    F["rebates"] = pd.read_csv(f["rebates"])
    F["rebates"]["InstallDate"] = _d(F["rebates"]["InstallDate"])
    F["_rp_path"] = f["rp_cases"]
    return F


# ------------------------------------------------------------------------------------------------- weather inputs
def weather(F):
    ap = F["airport"].set_index("DATE").reindex([d.date() for d in DAYS])
    tavg = ap["TAVG"].astype(float)
    tavg = tavg.fillna((ap["TMAX"].astype(float) + ap["TMIN"].astype(float)) / 2).interpolate().bfill().ffill()
    so = F["soil"].set_index("Date").reindex([d.date() for d in DAYS])
    s20 = so["Soil20inF"].astype(float).interpolate().bfill().ffill()
    s40 = so["Soil40inF"].astype(float).interpolate().bfill().ffill()
    return dict(air=tavg.values, s20=s20.values, s40=s40.values,
                hdd60=np.clip(60 - tavg.values, 0, None), hdd65=np.clip(65 - tavg.values, 0, None))


# ---------------------------------------------------------------------------------------------- the meter register
def register(F):
    r = F["register"].copy()
    tcmodel = dict(zip(F["models"]["Model"], F["models"]["TempComp"]))
    r["tc_now"] = r["TempComp"].where(r["TempComp"].notna(), r["MeterModel"].map(tcmodel)).eq("Y")
    r["tc_prev"] = r["PreviousModel"].map(tcmodel).eq("Y")
    r["outdoor"] = r["MeterLocation"].eq("Outside")
    code = {v: k for k, v in P.DNAME.items()}
    r["district"] = r["PressureDistrict"].map(code)
    r["ExchangeDate"] = pd.to_datetime(r["ExchangeDate"]).dt.date
    meter_tc = {}
    for x in r.itertuples():
        meter_tc[x.MeterID] = bool(x.tc_now)
        if isinstance(x.PreviousMeterID, str):
            meter_tc[x.PreviousMeterID] = bool(x.tc_prev)
    return r, meter_tc


# --------------------------------------------------------------------------------------------- read periods
def periods(F, reg, meter_tc):
    """Actual-to-actual periods per meter: estimated reads skipped (their period folds into the next actual read),
    the re-run's repeated rows dropped, the index difference taken on the four dials with rollover."""
    rd = F["reads"].drop_duplicates()
    rd = rd[rd["ReadType"] != "E"].copy()
    order = {"F": 0, "I": 1, "A": 2, "S": 3}
    rd["o"] = rd["ReadType"].map(order)
    rd = rd.sort_values(["PremiseID", "MeterID", "ReadDate", "o"])
    rd = rd.drop_duplicates(["PremiseID", "MeterID", "ReadDate"], keep="first")
    g = rd.groupby(["PremiseID", "MeterID"], sort=False)
    rd["prev_idx"] = g["MeterIndex"].shift(1)
    rd["prev_date"] = g["ReadDate"].shift(1)
    p = rd.dropna(subset=["prev_idx"]).copy()
    diff = (p["MeterIndex"] - p["prev_idx"]) % 10000
    p["ccf"] = diff * p["Multiplier"]
    p = p.rename(columns={"prev_date": "start", "ReadDate": "end"})
    info = reg.set_index("PremiseID")
    p["district"] = p["PremiseID"].map(info["district"])
    p["outdoor"] = p["PremiseID"].map(info["outdoor"])
    p["cls"] = p["PremiseID"].map(info["ServiceClass"])
    p["tc"] = p["MeterID"].map(meter_tc).fillna(False).astype(bool)
    p = p[p["start"] < p["end"]]
    return p[["PremiseID", "MeterID", "district", "cls", "outdoor", "tc", "start", "end", "ccf"]].reset_index(drop=True)


# ------------------------------------------------------------------------------------------- real-gas basis
def p_atm(F):
    """The absolute pressure the correctors add to gauge pressure: solved from the customer correctors' own
    corrected-to-uncorrected ratios on their measured temperature (each is (gauge + atmospheric) / 14.73 x 519.67 /
    (temperature + 459.67) for a pressure-and-temperature corrector)."""
    ev = F["evc"]
    ok = ev["Status"].eq("OK") & ev["UncorrectedMcf"].gt(1)
    r = ev.loc[ok, "CorrectedMcf"] / ev.loc[ok, "UncorrectedMcf"]
    pa = r * P.P_BASE * (ev.loc[ok, "AvgGasTempF"] + 459.67) / P.R_BASE - ev.loc[ok, "AvgPressurePsig"]
    return float(np.round(np.median(pa), 2))


def station_factor(F):
    """Each station corrector's recorded factor over the pressure-and-temperature factor, gas day by gas day."""
    drs = F["drs"]
    pa = p_atm(F)
    ok = drs["Alarm"].fillna("").eq("") & drs["UncorrectedMcf"].gt(1)
    d = drs[ok].copy()
    d["ptf"] = (d["AvgPressurePsig"] + pa) / P.P_BASE * P.R_BASE / (d["AvgTempF"] + 459.67)
    d["excess"] = d["CorrectedMcf"] / d["UncorrectedMcf"] / d["ptf"]
    return d, pa


def pt_only_stations(F):
    d, _ = station_factor(F)
    med = d.groupby("Station")["excess"].median()
    return sorted(med.index[med < 1.0015]), med


def fit_fpv2(F):
    """Supercompressibility fitted on the EVC-II stations' own records: the factor's excess over one on the
    absolute pressure's excess over base, and on that times the gas temperature."""
    d, pa = station_factor(F)
    pto, _ = pt_only_stations(F)
    d = d[~d["Station"].isin(pto)]
    dp = d["AvgPressurePsig"] + pa - P.P_BASE
    X = np.column_stack([dp, dp * (d["AvgTempF"] - 50.0)])
    b = np.linalg.lstsq(X, d["excess"].values - 1.0, rcond=None)[0]
    return lambda p_psia, t_f, sg: 1.0 + b[0] * (p_psia - P.P_BASE) + b[1] * (p_psia - P.P_BASE) * (t_f - 50.0)


def fpv2_fn(F, how):
    if how in ("dak", "hy", "papay"):
        return lambda p, t, sg: ZF.fpv2(p, t, sg, how)
    if how == "fit":
        return fit_fpv2(F)
    return None


def gate_sg(F):
    g = F["gate"].set_index("GasDay")["SpecificGravity"].astype(float)
    return g.reindex([d.date() for d in DAYS]).interpolate().bfill().ffill()


# ------------------------------------------------------------------------------------------- regulator stations
def stations_daily(F, how="rebuild", z="dak"):
    st = F["stations"].set_index("Station")["PressureDistrict"]
    code = {v: k for k, v in P.DNAME.items()}
    drs = F["drs"].copy()
    f = fpv2_fn(F, z)
    if f is not None:
        # the EVC-I stations correct for pressure and temperature only: put them on the EVC-II stations' basis
        pto, _ = pt_only_stations(F)
        pa = p_atm(F)
        sg = gate_sg(F)
        m = drs["Station"].isin(pto) & drs["CorrectedMcf"].notna()
        sgd = drs.loc[m, "GasDay"].map(sg)
        drs.loc[m, "CorrectedMcf"] = drs.loc[m, "CorrectedMcf"] * f(drs.loc[m, "AvgPressurePsig"] + pa,
                                                                    drs.loc[m, "AvgTempF"], sgd)
    drs["bad"] = drs["CorrectedMcf"].isna() | drs["Alarm"].isin(["COMM FAIL", "PXDCR FAIL FIXED P", "TXMTR STUCK"])
    piv = drs.pivot(index="GasDay", columns="Station", values="CorrectedMcf")
    bad = drs.pivot(index="GasDay", columns="Station", values="bad").fillna(True).astype(bool)
    piv = piv.reindex([d.date() for d in DAYS])
    bad = bad.reindex([d.date() for d in DAYS]).astype(float).fillna(1.0).astype(bool)
    gate = F["gate"].set_index("GasDay")["CorrectedMcf"].reindex(piv.index)
    if how == "raw":
        q = piv.fillna(0.0)
    elif how == "share":
        # each faulty day carried at the station's own share of the gate, interpolated from the days around it
        q = piv.copy()
        share = piv.where(~bad).div(gate, axis=0)
        share = share.interpolate(limit_direction="both")
        for s in piv.columns:
            m = bad[s] & gate.notna()
            q.loc[m, s] = gate[m] * share.loc[m, s]
        q = q.fillna(0.0)
    else:
        q = piv.copy()
        allbad = bad.any(axis=1)
        good_sum = piv.where(~bad).sum(axis=1)
        ratio = ((gate - piv.sum(axis=1)) / gate).where(~allbad)
        month = pd.Series([d.strftime("%Y-%m") for d in piv.index], index=piv.index)
        r_m = ratio.groupby(month).transform("median")
        r_m = r_m.fillna(ratio.median())
        share = piv.div(piv.sum(axis=1), axis=0).where(~allbad)
        for d in piv.index[allbad & gate.notna()]:
            bads = [s for s in piv.columns if bad.at[d, s]]
            avail = gate[d] * (1 - r_m[d]) - good_sum[d]
            win = [x for x in piv.index if abs((x - d).days) <= 10]
            sh = share.loc[win, bads].median()
            sh = sh / sh.sum()
            for s in bads:
                q.at[d, s] = avail * sh[s]
        q = q.fillna(0.0)
    dist = {}
    for s in q.columns:
        c = code[st[s]]
        dist[c] = dist.get(c, 0.0) + q[s].values
    return {c: np.nan_to_num(v) for c, v in dist.items()}


# ------------------------------------------------------------------------------------------- corrector customers
def evc_daily(F, z="dak"):
    ev = F["evc"].copy()
    ev["ratio"] = ev["CorrectedMcf"] / ev["UncorrectedMcf"].replace(0, np.nan)
    ev = ev.sort_values(["Account", "GasDay"])
    good = ev["Status"].eq("OK")
    ev["r_ok"] = ev["ratio"].where(good)
    ev["r_fill"] = ev.groupby("Account")["r_ok"].transform(lambda s: s.rolling(15, center=True, min_periods=3).median())
    ev["r_fill"] = ev.groupby("Account")["r_fill"].transform(lambda s: s.ffill().bfill())
    ev["mcf"] = np.where(good, ev["CorrectedMcf"], ev["UncorrectedMcf"] * ev["r_fill"])
    f = fpv2_fn(F, z)
    if f is not None:
        # every customer corrector corrects for pressure and temperature only: the real-gas volume at base
        # conditions is its volume times the supercompressibility factor at its own pressure and temperature
        ev["t_ok"] = ev["AvgGasTempF"].where(good)
        ev["t_fill"] = ev.groupby("Account")["t_ok"].transform(
            lambda s: s.rolling(15, center=True, min_periods=3).median().ffill().bfill())
        sg = gate_sg(F)
        ev["mcf"] = ev["mcf"] * f(ev["AvgPressurePsig"] + p_atm(F), ev["t_fill"], ev["GasDay"].map(sg))
    acc = F["correctors"].set_index("Account")["PressureDistrict"]
    code = {v: k for k, v in P.DNAME.items()}
    ev["district"] = ev["Account"].map(acc).map(code)
    out = {}
    idx = {d.date(): i for i, d in enumerate(DAYS)}
    for c, g in ev.groupby("district"):
        a = np.zeros(ND)
        for d, v in zip(g["GasDay"], g["mcf"]):
            a[idx[d]] += v
        out[c] = a
    return out, ev


# --------------------------------------------------------------------------------------------- gas temperature
def gas_temp(F, Wx, how="soil"):
    lg = F["loggers"].copy()
    reg = F["register"].set_index("PremiseID")
    lg["outdoor"] = lg["PremiseID"].map(reg["MeterLocation"]).eq("Outside")
    idx = {d.date(): i for i, d in enumerate(DAYS)}
    lg["t"] = lg["Date"].map(idx)
    air, s20, s40 = Wx["air"], Wx["s20"], Wx["s40"]
    o = lg[lg["outdoor"]]
    ins = lg[~lg["outdoor"]]
    a_i = np.polyfit(s40[ins["t"].values] - 46.0, ins["GasTempF"].values, 1)
    T_in = a_i[1] + a_i[0] * (s40 - 46.0)
    if how == "soil":
        y = o["GasTempF"].values - s20[o["t"].values]
        X = np.column_stack([air[o["t"].values] - s20[o["t"].values], (air[o["t"].values] < 45).astype(float),
                             np.ones(len(o))])
        k, wall, c0 = np.linalg.lstsq(X, y, rcond=None)[0]
        T_out = s20 + k * (air - s20) + wall * (air < 45) + c0
        par = dict(k=k, wall=wall, c0=c0)
    elif how == "evc":
        ev = F["evc"]
        acc = F["correctors"].set_index("Account")
        outacc = acc.index[acc["MeterLocation"] == "Outside"]
        e = ev[ev["Account"].isin(outacc) & ev["Status"].eq("OK")].groupby("GasDay")["AvgGasTempF"].mean()
        te = pd.Series(e).reindex([d.date() for d in DAYS]).interpolate().bfill().ffill().values
        y = o["GasTempF"].values
        X = np.column_stack([te[o["t"].values], air[o["t"].values], np.ones(len(o))])
        b1, b2, b0 = np.linalg.lstsq(X, y, rcond=None)[0]
        T_out = b0 + b1 * te + b2 * air
        par = dict(b0=b0, b1=b1, b2=b2)
    elif how == "logger_air":
        b, a = np.polyfit(air[o["t"].values], o["GasTempF"].values, 1)
        T_out = a + b * air
        par = dict(a=a, b=b)
    elif how == "monthly_air":
        mm = pd.Series(air, index=DAYS).groupby([DAYS.year, DAYS.month]).transform("mean").values
        T_out = mm
        T_in = mm
        par = {}
    else:
        T_out = np.full(ND, 60.0)
        T_in = np.full(ND, 60.0)
        par = {}
    return T_out, T_in, par


# -------------------------------------------------------------------------------------------- calendarization
def weights(how, inflow, Wx):
    if how == "billed":
        return None
    if how == "uniform":
        return {c: np.ones(ND) for c in P.DCODES}
    if how == "hdd65":
        return {c: Wx["hdd65"] + 1e-6 for c in P.DCODES}
    if how == "fit":
        out = {}
        for c in P.DCODES:
            y = inflow[c]
            X = np.column_stack([np.ones(ND), Wx["hdd60"]])
            m = (y > 0)
            b = np.linalg.lstsq(X[m], y[m], rcond=None)[0]
            out[c] = np.clip(X @ b, 1e-6, None)
        return out
    return {c: np.clip(inflow[c], 1e-6, None) for c in P.DCODES}


def allocate(per, wts):
    """Each period's ccf over its days in proportion to the district's daily weights; returns the daily ccf by
    district, compensation and location, and each premise's monthly ccf."""
    per = per.copy()
    per["s"] = per["start"].map(_di)
    per["e"] = per["end"].map(_di)
    if wts is None:
        # bills by the month they were read: each period's volume on its closing read's day
        per["s"] = (per["e"] - 1).clip(0)
        wts = {c: np.ones(ND) for c in P.DCODES}
    daily = {}
    cum = {c: np.concatenate([[0.0], np.cumsum(wts[c])]) for c in P.DCODES}
    for (c, tc, od), g in per.groupby(["district", "tc", "outdoor"]):
        agg = g.groupby(["s", "e"])["ccf"].sum()
        arr = np.zeros(ND)
        w = wts[c]
        for (s, e), v in agg.items():
            tot = cum[c][e] - cum[c][s]
            arr[s:e] += v * w[s:e] / tot
        daily[(c, bool(tc), bool(od))] = arr
    # monthly ccf per premise (for diversion)
    mp = pd.period_range("2023-09", "2026-10", freq="M")
    mstart = np.array([_di(m.start_time.date()) for m in mp])
    mend = np.array([_di(m.end_time.date()) + 1 for m in mp])
    s = per["s"].values.clip(0, ND)
    e = per["e"].values.clip(0, ND)
    di = per["district"].map({c: i for i, c in enumerate(P.DCODES)}).values
    cumM = np.stack([cum[c] for c in P.DCODES])
    tot = cumM[di, e] - cumM[di, s]
    mon = np.zeros((len(per), len(mp)))
    for j, (a, b) in enumerate(zip(mstart, mend)):
        lo = np.clip(np.maximum(s, a), 0, ND)
        hi = np.clip(np.minimum(e, b), 0, ND)
        part = np.where(hi > lo, cumM[di, hi] - cumM[di, lo], 0.0)
        mon[:, j] = per["ccf"].values * part / np.where(tot > 0, tot, 1.0)
    mdf = pd.DataFrame(mon, columns=[str(m) for m in mp])
    mdf["PremiseID"] = per["PremiseID"].values
    pm = mdf.groupby("PremiseID").sum()
    return daily, pm


# --------------------------------------------------------------------------------------------------- diversion
def history_diversion(F):
    """The revenue protection cases found before the window: each case's back-billed volume spread evenly over the
    months its finding estimated, by district and month (Mcf at base conditions)."""
    import openpyxl  # noqa: F401
    path = F.get("_rp_path")
    cases = pd.read_excel(path) if path else pd.DataFrame()
    code = {v: k for k, v in P.DNAME.items()}
    out = {c: np.zeros(len(MONTHS)) for c in P.DCODES}
    for r in cases.itertuples():
        found = pd.Timestamp(r.FoundDate).to_period("M")
        months = [found - k for k in range(1, int(r.EstimatedMonths) + 1)]
        per_m = float(r.BackBilledCcf) * P.PF / 10.0 / len(months)
        for m in months:
            if m in MONTHS:
                out[code[r.PressureDistrict]][list(MONTHS).index(m)] += per_m
    return out


def cold_day_response(F, per, Wx, prem, start_month, b_slope, grid=(-10, -5, 0, 5, 10, 15, 30, 60)):
    """A collapsed premise's FY2026 heating read period by period against the degree days of its cold days only: a
    dual-fuel heat pump leaves the furnace (on the meter) the whole load below its switchover and none above, so the
    period's gas is the base plus the premise's own past slope times the degree days on days colder than the
    switchover. Returns the best switchover and the fitted cold-day slope over the premise's own past slope."""
    p = per[(per["PremiseID"] == prem)]
    t0 = _di(start_month)
    p = p[(p["start"].map(_di) >= t0) & (p["end"] <= P.W1) & (p["end"].map(lambda d: d.month in (11, 12, 1, 2, 3, 4)))]
    if len(p) < 3 or b_slope <= 0:
        return None, 0.0
    air, hdd = Wx["air"], Wx["hdd60"]
    best = (None, 0.0, np.inf)
    for T in grid:
        ch = np.where(air < T, hdd, 0.0)
        cum = np.concatenate([[0.0], np.cumsum(ch)])
        X = np.column_stack([(p["end"].map(_di) - p["start"].map(_di)).values.astype(float),
                             (cum[p["end"].map(_di).values] - cum[p["start"].map(_di).values])])
        y = p["ccf"].values.astype(float)
        bb = np.linalg.lstsq(X, y, rcond=None)[0]
        bb = np.clip(bb, 0, None)
        sse = float(((X @ bb - y) ** 2).sum())
        if sse < best[2]:
            best = (T, float(bb[1]) / b_slope, sse)
    return best[0], best[1]


def diversion(F, reg, pm, Wx, how="golden", fac=None, cut=0.4, run=3, home_cut=0.7, df_cut=0.3, df_tmax=10,
              summer_cut=0.4, vacant_months=2, heating_month=True, per=None, tap_cut=None):
    """Premises whose use collapsed against their own weather response of the year before, outside vacant spells
    and meter exchanges. Those whose summer base load also went (a bypass) or whose winter use lost its heating
    response (a furnace tap) took gas without authorization; those whose winter use kept a reduced heating response
    (an absence) did not; and a lost heating response that comes back in full on the coldest days, read period by
    read period, is a dual-fuel heat pump the household added (no gas taken), as is any premise with a dual-fuel
    controls rebate on file. A run of low months must reach into the heating season (October to April): a student
    rental's summer away recurs every year and is no collapse.
        how  golden (bypasses and taps) | nodf (no cold-day test: dual-fuel homes kept as taps) | allx (every
             collapse booked but the dual-fuel homes) | all (every collapse booked, rebated homes aside) | none"""
    if how == "none":
        return pd.DataFrame(columns=["PremiseID", "district", "kind", "mcf_window"])
    rebated = set(F["rebates"].loc[F["rebates"]["Equipment"].eq("Dual-fuel heat pump controls"), "PremiseID"])
    months = [str(m) for m in pd.period_range("2023-09", "2026-10", freq="M")]
    mp = pd.period_range("2023-09", "2026-10", freq="M")
    hdd = np.array([Wx["hdd60"][(DAYS.year == m.year) & (DAYS.month == m.month)].sum() for m in mp])
    ndays = np.array([((DAYS.year == m.year) & (DAYS.month == m.month)).sum() for m in mp])
    fy25 = [i for i, m in enumerate(mp) if dt.date(2024, 10, 1) <= m.start_time.date() <= dt.date(2025, 9, 1)]
    fy26 = [i for i, m in enumerate(mp) if P.W0 <= m.start_time.date() <= dt.date(2026, 9, 1)]
    summer26 = [i for i, m in enumerate(mp) if m.start_time.date() in
                [dt.date(2026, 6, 1), dt.date(2026, 7, 1), dt.date(2026, 8, 1)]]
    home26 = [i for i, m in enumerate(mp) if (m.year, m.month) == (2026, 5)]
    acc = F["accounts"]
    exch = reg.set_index("PremiseID")["ExchangeDate"]
    res = reg.set_index("PremiseID")
    out = []
    X25 = np.column_stack([ndays[fy25], hdd[fy25]])
    for prem, row in pm.iterrows():
        y25 = row.values[fy25]
        if y25.sum() <= 0:
            continue
        b = np.linalg.lstsq(X25, y25, rcond=None)[0]
        b = np.clip(b, 0, None)
        pred = ndays * b[0] + hdd * b[1]
        y = row.values
        ratio = np.where(pred > 1, y / np.maximum(pred, 1e-9), 1.0)
        low = [i for i in fy26 if ratio[i] < cut and pred[i] > 3]
        if len(low) < run:
            continue
        # consecutive run of three or more
        runs, cur, heat, best_heat = 0, 0, False, False
        for i in fy26:
            if ratio[i] < cut and pred[i] > 3:
                cur, heat = cur + 1, heat or mp[i].month in (10, 11, 12, 1, 2, 3, 4)
            else:
                cur, heat = 0, False
            if cur >= run:
                best_heat = best_heat or heat
            runs = max(runs, cur)
        if runs < run or (heating_month and not best_heat):
            continue
        # vacant spells: no open account during the low months
        a = acc[acc["PremiseID"] == prem]
        vacant_low = 0
        for i in low:
            m0, m1 = mp[i].start_time.date(), mp[i].end_time.date()
            open_days = 0
            for r in a.itertuples():
                s = r.StartDate
                e = dt.date(2100, 1, 1) if pd.isna(r.EndDate) else r.EndDate
                if pd.isna(s):
                    continue
                lo, hi = max(s, m0), min(e, m1)
                open_days += max(0, (hi - lo).days)
            if open_days < 0.5 * (m1 - m0).days:
                vacant_low += 1
        if vacant_low >= vacant_months:
            continue
        ex = exch.get(prem)
        if not pd.isna(ex) and P.W0 <= ex <= P.W1:
            continue
        summer_ratio = y[summer26].sum() / max(pred[summer26].sum(), 1e-9)
        home_ratio = y[home26].sum() / max(pred[home26].sum(), 1e-9)
        w_idx = low[1:] if len(low) >= 4 else list(low)     # the month the fall began is part old, part new
        Xw = np.column_stack([ndays[w_idx], hdd[w_idx]])
        bw = np.linalg.lstsq(Xw, y[w_idx], rcond=None)[0]
        heat_kept = bw[1] / max(b[1], 1e-9)
        base_kept = bw[0] / max(b[0], 1e-9)
        # May 2026: the heating month after the winter when an away household is home again
        m0, m1 = dt.date(2026, 5, 1), dt.date(2026, 5, 31)
        may_open = 0
        for r in a.itertuples():
            s_ = r.StartDate
            e_ = dt.date(2100, 1, 1) if pd.isna(r.EndDate) else r.EndDate
            if pd.isna(s_):
                continue
            may_open += max(0, (min(e_, m1) - max(s_, m0)).days)
        if summer_ratio < summer_cut:
            kind = "bypass"
        elif may_open < 15:
            kind = "turnover"        # the premise changed hands over the spring: no test month
        elif home_ratio >= home_cut:
            kind = "absence"         # the heating response is back in May, when the household is home
        else:
            kind = "furnace tap"
        first = min(low)
        start = first
        for i in range(first - 1, max(first - 4, 0), -1):
            if ratio[i] < 0.8:
                start = i
            else:
                break
        t_sw, df_ratio = None, 0.0
        if kind == "furnace tap" and per is not None:
            t_sw, df_ratio = cold_day_response(F, per, Wx, prem, mp[first].start_time.date(), b[1])
        is_df = t_sw is not None and t_sw <= df_tmax and df_ratio >= df_cut
        reb = int(prem) in rebated
        if how != "diag":
            if reb or kind == "turnover":
                continue
            if how in ("golden", "nodf") and kind == "absence":
                continue
            if how in ("golden", "allx") and is_df:
                continue
        f = 1.0
        if fac is not None and not res.at[prem, "tc_now"]:
            f = fac["out" if res.at[prem, "outdoor"] else "in"]
        short = sum(max(0.0, pred[i] - y[i]) * (f[i] if fac is not None and not np.isscalar(f) else 1.0)
                    for i in fy26 if i >= start)
        out.append(dict(PremiseID=int(prem), district=res.at[prem, "district"], kind=kind, ccf_window=short,
                        first_month=months[start], heat_kept=round(float(heat_kept), 3),
                        home=round(float(home_ratio), 3), summer=round(float(summer_ratio), 3),
                        dual_fuel=bool(is_df), rebated=bool(reb),
                        cold_day_slope=round(float(df_ratio), 3), switchover=t_sw))
    df = pd.DataFrame(out)
    if len(df):
        df["mcf_window"] = df["ccf_window"] * P.PF / 10.0
    return df


# --------------------------------------------------------------------------------------------------- the route
def run(F, opts=None, cache=None):
    o = dict(GOLDEN)
    o.update(opts or {})
    cache = cache if cache is not None else {}
    if "wx" not in cache:
        cache["wx"] = weather(F)
        cache["reg"], cache["meter_tc"] = register(F)
        cache["per"] = periods(F, cache["reg"], cache["meter_tc"])
    Wx, reg, per = cache["wx"], cache["reg"], cache["per"]
    key = ("evc", o["z"])
    if key not in cache:
        cache[key] = evc_daily(F, o["z"])
    evc = cache[key][0]
    key = ("drs", o["drs"], o["z"])
    if key not in cache:
        cache[key] = stations_daily(F, o["drs"], o["z"])
    inflow = cache[key]
    key = ("alloc", o["cal"], o["drs"], o["z"])
    if key not in cache:
        cache[key] = allocate(per, weights(o["cal"], inflow, Wx))
    daily, pm = cache[key]
    key = ("temp", o["temp"])
    if key not in cache:
        cache[key] = gas_temp(F, Wx, o["temp"])
    T_out, T_in, tpar = cache[key]
    if o["k_scale"] != 1.0 and o["temp"] == "soil":
        dk = tpar["k"] * (o["k_scale"] - 1.0)
        T_out = T_out + dk * (Wx["air"] - Wx["s20"])
    if o["in_shift"]:
        T_in = T_in + o["in_shift"]
    fac_out = P.R_BASE / (T_out + 459.67)
    fac_in = P.R_BASE / (T_in + 459.67)
    mp = pd.period_range("2023-09", "2026-10", freq="M")
    fac = {k: np.array([v[(DAYS.year == m.year) & (DAYS.month == m.month)].mean() for m in mp])
           for k, v in (("out", fac_out), ("in", fac_in))}
    key = ("div", o["div"], o["cal"], o["drs"], o["z"], o["temp"], o["k_scale"], o["in_shift"], o["home_cut"],
           o["df_cut"], o["df_tmax"])
    if key not in cache:
        cache[key] = diversion(F, reg, pm, Wx, o["div"], fac, home_cut=o["home_cut"], df_cut=o["df_cut"],
                               df_tmax=o["df_tmax"], per=per)
    div = cache[key]
    if "hist_div" not in cache:
        cache["hist_div"] = history_diversion(F)
    hist_div = cache["hist_div"]
    # own use and damage, by district and day
    code = {v: k for k, v in P.DNAME.items()}
    own = {c: np.zeros(ND) for c in P.DCODES}
    ou = F["own_use"].dropna(subset=["PressureDistrict"])
    for r in ou.itertuples():
        m = pd.Period(r.Month, "M")
        msk = (DAYS.year == m.year) & (DAYS.month == m.month)
        own[code[r.PressureDistrict]][msk] += o["own_scale"] * float(r.EstimatedMcf) / max(1, msk.sum())
    dmg = {c: np.zeros(ND) for c in P.DCODES}
    idx = {d.date(): i for i, d in enumerate(DAYS)}
    for r in F["damage"].itertuples():
        if r.Date in idx:
            dmg[code[r.PressureDistrict]][idx[r.Date]] += o["dmg_scale"] * float(r.EstimatedGasLostMcf)
    # diversion spread over the window months it covers, monthly
    divm = {c: np.zeros(len(MONTHS)) for c in P.DCODES}
    out = {}
    for c in P.DCODES:
        billed = np.zeros(ND)
        delivered = np.zeros(ND)
        under = np.zeros(ND)
        billed_ntc = np.zeros(ND)
        for (cc, tc, od), arr in daily.items():
            if cc != c:
                continue
            b = arr * P.PF / 10.0
            billed += b
            if tc:
                delivered += b
            else:
                f = fac_out if od else fac_in
                delivered += b * f
                under += b * (f - 1)
                billed_ntc += b
        out[c] = dict(inflow=inflow[c], billed=billed, delivered=delivered, under=under, billed_ntc=billed_ntc,
                      evc=evc.get(c, np.zeros(ND)), own=own[c], dmg=dmg[c])
    # monthly table
    rows = []
    for c in P.DCODES:
        d = out[c]
        dv = o["div_scale"] * (div[div["district"] == c]["mcf_window"].sum() if len(div) else 0.0)
        win_days = WIN.sum()
        for m in MONTHS:
            msk = (DAYS.year == m.year) & (DAYS.month == m.month)
            in_w = P.W0 <= m.start_time.date() <= P.W1
            # diversion for the window months only, spread by the district's delivered volume in the window
            dm = hist_div[c][list(MONTHS).index(m)] if not in_w else 0.0
            if in_w and dv > 0:
                dm = dv * d["delivered"][msk].sum() / d["delivered"][WIN].sum()
            row = dict(district=c, month=str(m), inflow=d["inflow"][msk].sum(), billed=d["billed"][msk].sum(),
                       under=d["under"][msk].sum(), evc=d["evc"][msk].sum(), own=d["own"][msk].sum(),
                       dmg=d["dmg"][msk].sum(), div=dm)
            row["leak"] = row["inflow"] - row["billed"] - row["under"] - row["evc"] - row["own"] - row["dmg"] - row["div"]
            rows.append(row)
    mon = pd.DataFrame(rows)
    w = mon[mon["month"].isin([str(m) for m in pd.period_range("2025-10", "2026-09", freq="M")])]
    agg = w.groupby("district")[["inflow", "billed", "under", "evc", "own", "dmg", "div", "leak"]].sum()
    agg["leak_pct"] = 100 * agg["leak"] / agg["inflow"]
    ntc_billed = {c: out[c]["billed_ntc"][WIN].sum() for c in P.DCODES}
    agg["ntc_billed"] = pd.Series(ntc_billed)
    agg["ur_pct"] = 100 * agg["under"] / agg["ntc_billed"].replace(0, np.nan)
    nmeters = reg[~reg["tc_now"] & reg["district"].notna()].groupby("district").size()
    agg["ntc_meters"] = nmeters.reindex(agg.index).fillna(0).astype(int)
    designated = sorted(agg.index[agg["leak_pct"] > P.LEAK_LINE])
    elig = agg[agg["ntc_meters"] >= P.CHANGEOUT_MIN_METERS]
    changeout = sorted(elig.index[elig["ur_pct"] > P.CHANGEOUT_LINE])
    return dict(opts=o, monthly=mon, agg=agg, designated=designated, changeout=changeout, diversion=div,
                tpar=tpar, daily=out)
