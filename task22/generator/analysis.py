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
      plan    pace (the 2024-25 work orders' completion by meter location) | plan (every meter on its date)
"""
import datetime as dt
import os

import numpy as np
import pandas as pd

import params as P

DAY0 = dt.date(2023, 8, 1)
DAY1 = P.SIM1
DAYS = pd.date_range(DAY0, DAY1, freq="D")
ND = len(DAYS)
MONTHS = pd.period_range("2023-10", "2026-09", freq="M")
WIN = (DAYS >= pd.Timestamp(P.W0)) & (DAYS <= pd.Timestamp(P.W1))
GOLDEN = dict(cal="shape", temp="soil", div="golden", drs="rebuild", plan="pace", k_scale=1.0, in_shift=0.0,
              dmg_scale=1.0, own_scale=1.0, div_scale=1.0)


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
    F["workorders"] = pd.read_csv(f["workorders"])
    for c in ("PlannedDate", "CompletedDate"):
        F["workorders"][c] = pd.to_datetime(F["workorders"][c]).dt.date
    F["plan2027"] = pd.read_excel(f["plan2027"], skiprows=2).dropna(subset=["PremiseID"])
    F["plan2027"] = F["plan2027"][pd.to_numeric(F["plan2027"]["PremiseID"], errors="coerce").notna()]
    F["plan2027"]["PlannedDate"] = pd.to_datetime(F["plan2027"]["PlannedDate"]).dt.date
    F["lauf_report"] = pd.read_excel(f["lauf_report"], skiprows=2)
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


# ------------------------------------------------------------------------------------------- regulator stations
def stations_daily(F, how="rebuild"):
    st = F["stations"].set_index("Station")["PressureDistrict"]
    code = {v: k for k, v in P.DNAME.items()}
    drs = F["drs"].copy()
    drs["bad"] = drs["CorrectedMcf"].isna() | drs["Alarm"].isin(["COMM FAIL", "PXDCR FAIL FIXED P", "TXMTR STUCK"])
    piv = drs.pivot(index="GasDay", columns="Station", values="CorrectedMcf")
    bad = drs.pivot(index="GasDay", columns="Station", values="bad").fillna(True).astype(bool)
    piv = piv.reindex([d.date() for d in DAYS])
    bad = bad.reindex([d.date() for d in DAYS]).astype(float).fillna(1.0).astype(bool)
    gate = F["gate"].set_index("GasDay")["CorrectedMcf"].reindex(piv.index)
    if how == "raw":
        q = piv.fillna(0.0)
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
def evc_daily(F):
    ev = F["evc"].copy()
    ev["ratio"] = ev["CorrectedMcf"] / ev["UncorrectedMcf"].replace(0, np.nan)
    ev = ev.sort_values(["Account", "GasDay"])
    good = ev["Status"].eq("OK")
    ev["r_ok"] = ev["ratio"].where(good)
    ev["r_fill"] = ev.groupby("Account")["r_ok"].transform(lambda s: s.rolling(15, center=True, min_periods=3).median())
    ev["r_fill"] = ev.groupby("Account")["r_fill"].transform(lambda s: s.ffill().bfill())
    ev["mcf"] = np.where(good, ev["CorrectedMcf"], ev["UncorrectedMcf"] * ev["r_fill"])
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


def diversion(F, reg, pm, Wx, how="golden", fac=None, cut=0.4, run=3, heat_kept_cut=0.15, base_kept_cut=0.5,
              summer_cut=0.4, vacant_months=2, heating_month=True):
    """Accounts whose use collapsed against their own weather response of the year before, outside vacant spells
    and meter exchanges: those whose summer base load also went (a bypass) or whose winter use lost its heating
    response while keeping its base (a furnace tap) took gas without authorization; those whose winter use kept a
    reduced heating response and whose summer came back (an absence) did not. A run of low months must reach into
    the heating season (October to April): a student rental's summer away recurs every year and is no collapse."""
    if how == "none":
        return pd.DataFrame(columns=["PremiseID", "district", "kind", "mcf_window"])
    months = [str(m) for m in pd.period_range("2023-09", "2026-10", freq="M")]
    mp = pd.period_range("2023-09", "2026-10", freq="M")
    hdd = np.array([Wx["hdd60"][(DAYS.year == m.year) & (DAYS.month == m.month)].sum() for m in mp])
    ndays = np.array([((DAYS.year == m.year) & (DAYS.month == m.month)).sum() for m in mp])
    fy25 = [i for i, m in enumerate(mp) if dt.date(2024, 10, 1) <= m.start_time.date() <= dt.date(2025, 9, 1)]
    fy26 = [i for i, m in enumerate(mp) if P.W0 <= m.start_time.date() <= dt.date(2026, 9, 1)]
    summer26 = [i for i, m in enumerate(mp) if m.start_time.date() in
                [dt.date(2026, 6, 1), dt.date(2026, 7, 1), dt.date(2026, 8, 1)]]
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
        w_idx = [i for i in low]
        Xw = np.column_stack([ndays[w_idx], hdd[w_idx]])
        bw = np.linalg.lstsq(Xw, y[w_idx], rcond=None)[0]
        heat_kept = bw[1] / max(b[1], 1e-9)
        base_kept = bw[0] / max(b[0], 1e-9)
        if summer_ratio < summer_cut:
            kind = "bypass"
        elif heat_kept < heat_kept_cut and base_kept > base_kept_cut:
            kind = "furnace tap"
        else:
            kind = "absence"
        if how == "golden" and kind == "absence":
            continue
        first = min(low)
        start = first
        for i in range(first - 1, max(first - 4, 0), -1):
            if ratio[i] < 0.8:
                start = i
            else:
                break
        f = 1.0
        if fac is not None and not res.at[prem, "tc_now"]:
            f = fac["out" if res.at[prem, "outdoor"] else "in"]
        short = sum(max(0.0, pred[i] - y[i]) * (f[i] if fac is not None and not np.isscalar(f) else 1.0)
                    for i in fy26 if i >= start)
        out.append(dict(PremiseID=int(prem), district=res.at[prem, "district"], kind=kind, ccf_window=short,
                        first_month=months[start]))
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
        cache["evc"], cache["evc_rows"] = evc_daily(F)
    Wx, reg, per = cache["wx"], cache["reg"], cache["per"]
    key = ("drs", o["drs"])
    if key not in cache:
        cache[key] = stations_daily(F, o["drs"])
    inflow = cache[key]
    key = ("alloc", o["cal"], o["drs"])
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
    key = ("div", o["div"], o["cal"], o["drs"], o["temp"], o["k_scale"], o["in_shift"])
    if key not in cache:
        cache[key] = diversion(F, reg, pm, Wx, o["div"], fac)
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
                      evc=cache["evc"].get(c, np.zeros(ND)), own=own[c], dmg=dmg[c])
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
    plan = plan_2027(F, o["plan"])
    return dict(opts=o, monthly=mon, agg=agg, designated=designated, changeout=changeout, diversion=div,
                plan=plan, tpar=tpar, daily=out)


def plan_2027(F, how="pace"):
    pl = F["plan2027"]
    n = len(pl)
    if how == "plan":
        return dict(n=n, done=n, by_loc={})
    wo = F["workorders"]
    lag = {}
    for loc, g in wo.groupby("MeterLocation"):
        l = [10 ** 6 if pd.isna(c) else (c - p).days for p, c in zip(g["PlannedDate"], g["CompletedDate"])]
        lag[loc] = np.array(l)
    done = 0.0
    by = {}
    for r in pl.itertuples():
        room = (P.SEASON_2027 - r.PlannedDate).days - 1
        p = float((lag[r.MeterLocation] <= room).mean())
        done += p
        by[r.MeterLocation] = by.get(r.MeterLocation, 0.0) + p
    return dict(n=n, done=done, by_loc=by)
