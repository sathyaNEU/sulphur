"""The golden's analysis, run on the shipped files only: assembly of the records, the year's loss, the usable fleet,
the 2027 busiest week's deliveries and range, the Maplestead pubs' kegs, the Foundry cold store, the kegs needed in
circulation and the order; and the hurried analyst's routes beside each, for effort.json. Nothing here reads the
simulation."""
import datetime as dt
import os
import re
import sqlite3
import subprocess

import numpy as np
import pandas as pd

import params as P

SIZES = (50, 30, 20)
T1 = pd.Timestamp("2025-11-30 23:59:59")   # the close of the stocktake days
T2 = pd.Timestamp("2026-11-30 23:59:59")


def _size(x):
    return int(re.sub(r"[^0-9]", "", str(x)))


# ------------------------------------------------------------------------------------------------- loading
def load(target):
    F = {}
    p = lambda k: os.path.join(target, k)
    import pack
    FL = pack.FILES
    g = pd.read_csv(p(FL["gate"]), dtype={"fulls_out": "float", "empties_in": "float"})
    g["size"] = g.keg_size.map(_size)
    g["date"] = pd.to_datetime(g.count_date)
    F["gate"] = g
    wsh = pd.read_csv(p(FL["washer"]))
    wsh["date"] = pd.to_datetime(wsh.wash_date)
    wsh["size"] = wsh.keg_size_l
    F["washer"] = wsh
    fl = pd.read_csv(p(FL["fills"]))
    fl["date"] = pd.to_datetime(fl.fill_date)
    F["fills"] = fl
    rep = pd.read_csv(p(FL["repairs"]))
    rep["received"] = pd.to_datetime(rep.received)
    rep["back"] = pd.to_datetime(rep.back_to_washer)
    F["repairs"] = rep
    F["audits"] = pd.read_csv(p(FL["audits"]), parse_dates=["count_date"])
    wx = pd.read_csv(p(FL["weather"]), parse_dates=["date"])
    F["weather"] = wx
    v = pd.read_csv(p(FL["visits"]), parse_dates=["visit_date"])
    F["visits"] = v.drop_duplicates()
    r = pd.read_csv(p(FL["rfid"]), parse_dates=["read_time"])
    F["rfid"] = r
    reg = pd.read_excel(p(FL["register"]), sheet_name=None)
    F["register"] = reg["Kegs"]
    F["tagchanges"] = reg["Tag changes"]
    st = pd.read_excel(p(FL["stocktake"]), sheet_name=None)
    F["stocktake"] = {int(k.split()[-1]): v.dropna(subset=["condition"]) for k, v in st.items()}
    rc = pd.read_excel(p(FL["recovery"]), sheet_name=None)
    F["recovery"] = rc["Returned"]
    pl = pd.read_excel(p(FL["plan"]), sheet_name=None)
    F["plan"] = pl
    con = sqlite3.connect(p(FL["erp"]))
    for t in ("accounts", "account_changes", "products", "delivery_schedule", "dispense_lines", "deposit_ledger"):
        F[t] = pd.read_sql("select * from %s" % t, con)
    con.close()
    F["exchange"] = exchange_statements(p(FL["exchange"]))
    return F


def exchange_statements(path):
    txt = subprocess.run(["pdftotext", "-layout", path, "-"], capture_output=True, text=True).stdout
    rows = []
    month = None
    for line in txt.splitlines():
        m = re.search(r"Member statement: .*?, (\w+ \d{4})", line)
        if m:
            month = pd.Timestamp(dt.datetime.strptime(m.group(1), "%B %Y"))
            continue
        for key, lab in (("handed", "Kegs handed in"), ("returned", "own kegs returned"), ("held", "held at month end")):
            if lab in line and month is not None:
                nums = [int(x) for x in re.findall(r"\b\d+\b", line.split(lab)[-1])][-3:]
                if len(nums) == 3:
                    rows.append((month, key) + tuple(nums))
    df = pd.DataFrame(rows, columns=["month", "line", 50, 30, 20])
    return df


# ------------------------------------------------------------------------------------------------- RFID trips
def tag_map(F):
    reg = F["register"]
    m = dict(zip(reg.tag_epc.dropna(), reg.loc[reg.tag_epc.notna(), "serial"]))
    for _, r in F["tagchanges"].iterrows():
        m[r.new_tag_epc] = r.serial
    size = dict(zip(reg.serial, reg.size_l))
    return m, size


def trips(F):
    """each tagged keg's trips: from a fill (or a delivery read with no fill read since its last return) to its next
    return read; a duplicate read seconds apart is one read"""
    m, size = tag_map(F)
    r = F["rfid"].copy()
    r["serial"] = r.tag_epc.map(m)
    r = r.dropna(subset=["serial"]).sort_values(["serial", "read_time"])
    r["gap"] = r.groupby("serial").read_time.diff().dt.total_seconds()
    same = (r.read_point == r.groupby("serial").read_point.shift()) & (r.gap < 120)
    r = r[~same]
    out = []
    for s, g in r.groupby("serial", sort=False):
        start = None
        dlv = None
        loc = None
        for t, pt, lc in zip(g.read_time.values, g.read_point.values, g.location.values):
            if pt == "FILL":
                if start is not None:
                    out.append((s, start, dlv, loc, t - np.timedelta64(1, "D")))   # a missed return read
                start, dlv, loc = t, None, None
            elif pt == "DELIVER":
                if start is None:
                    start = t
                if dlv is None:
                    dlv, loc = t, lc
            else:
                if start is not None:
                    out.append((s, start, dlv, loc, t))
                start, dlv, loc = None, None, None
        if start is not None:
            out.append((s, start, dlv, loc, pd.NaT))
    tp = pd.DataFrame(out, columns=["serial", "start", "deliver", "account", "ret"])
    tp["size"] = tp.serial.map(size)
    tp["start"] = pd.to_datetime(tp.start)
    tp["deliver"] = pd.to_datetime(tp.deliver)
    tp["ret"] = pd.to_datetime(tp.ret)
    return tp


def seasonal_accounts(F):
    a = F["accounts"]
    return set(a.loc[a.season != "ALL YEAR", "account"])


def out_at(F, tp, T, horizon_end=T2):
    """tagged kegs out (filled and not yet back) at T that come back: settled where the record shows the return,
    completed from the same weeks a year earlier where it cannot yet"""
    o = tp[(tp.start <= T) & ((tp.ret > T) | tp.ret.isna())].copy()
    o["age"] = (T - o.start).dt.days
    seas = seasonal_accounts(F)
    o["seasonal"] = o.account.isin(seas)
    res = {}
    if T + pd.Timedelta(days=365) <= horizon_end:
        # settled: the kegs that came back, and each keg never seen again weighted by the chance it was still out at
        # T, read off the returned kegs' own times out at the same age (by account type)
        done = tp[tp.ret.notna() & (tp.start > T - pd.Timedelta(days=240)) & (tp.start <= T + pd.Timedelta(days=120))]
        surv = {}
        for flag in (False, True):
            x = done[done.account.isin(seas) == flag]
            dur = np.sort(((x.ret - x.start).dt.days).values)
            surv[flag] = dur
        for s in SIZES:
            os_ = o[o["size"] == s]
            back = os_.ret.notna().sum()
            gone = os_[os_.ret.isna()]
            wsum = 0.0
            for flag in (False, True):
                dur = surv[flag]
                ages = gone[gone.seasonal == flag].age.values
                if len(dur):
                    wsum += float(np.sum(1.0 - np.searchsorted(dur, ages, side="right") / len(dur)))
            res[s] = float(back + wsum)
        return res, o
    prior = T - pd.Timedelta(days=365)
    base = tp[(tp.start <= prior)]
    p = {}
    for s in SIZES:
        tot = 0.0
        os_ = o[o["size"] == s]
        bs = base[(base["size"] == s)]
        for seas_flag in (False, True):
            oo = os_[os_.seasonal == seas_flag]
            bb = bs[bs.account.isin(seas) == seas_flag]
            for lo, hi in ((0, 30), (30, 90), (90, 180), (180, 100000)):
                n_open = ((oo.age >= lo) & (oo.age < hi)).sum()
                if not n_open:
                    continue
                st = prior - pd.Timedelta(days=hi)
                en = prior - pd.Timedelta(days=lo)
                c = bb[(bb.start > st) & (bb.start <= en) & ((bb.ret > prior) | bb.ret.isna())]
                if len(c) >= 15:
                    q = ((c.ret.notna()) & (c.ret <= c.start + pd.Timedelta(days=400))).mean()
                else:
                    q = 0.0 if lo >= 180 else 0.97
                p[(s, seas_flag, lo)] = float(q)
                tot += n_open * q
        res[s] = tot
    return res, o


def tagged_share(F, tp, a, b):
    """the tagged kegs' share of every keg filled, from the trips' starts against the filling log"""
    fl = F["fills"]
    out = {}
    for s in SIZES:
        n_all = fl[(fl.date > a) & (fl.date <= b) & (fl.keg_l == s)].kegs_filled.sum()
        n_tag = ((tp.start > a) & (tp.start <= b) & (tp["size"] == s)).sum()
        out[s] = n_tag / n_all if n_all else 1.0
    return out


def stock_on_site(F, year, which):
    st = F["stocktake"][year]
    cols = {50: "50 l", 30: "30 l", 20: "20 l"}
    out = {}
    for s in SIZES:
        sel = st[st.condition.isin(which)]
        out[s] = float(sel[cols[s]].sum())
    return out


# ------------------------------------------------------------------------------------------------- R1 and R2
def own_back(F, a, b):
    """the fleet's own kegs that came back to Brighouse in (a, b]: presented at the washer and not another brewer's,
    less the repaired kegs presented a second time"""
    w = F["washer"]
    sel = w[(w.date > a) & (w.date <= b)]
    rep = F["repairs"]
    rr = rep[(rep.outcome == "REPAIRED") & (rep.back > a) & (rep.back <= b)]
    out = {}
    for s in SIZES:
        x = sel[sel["size"] == s]
        own = x.washed_ok.sum() + x.rejected_to_repair.sum() + x.condemned_at_inspection.sum()
        out[s] = float(own - (rr.size_l == s).sum())
    return out


def fills_between(F, a, b):
    fl = F["fills"]
    return {s: float(fl[(fl.date > a) & (fl.date <= b) & (fl.keg_l == s)].kegs_filled.sum()) for s in SIZES}


SHARE_DAYS = [120]
SHARE_BASIS = ["fills"]


def register_tag_share(F):
    reg = F["register"]
    act = reg[reg.status == "ACTIVE"]
    return {s: float(act[act.size_l == s].tag_epc.notna().mean()) for s in SIZES}


def out_scaled(F, tp, T):
    res, _ = out_at(F, tp, T)
    if SHARE_BASIS[0] == "register":
        sh = register_tag_share(F)
    else:
        sh = tagged_share(F, tp, T - pd.Timedelta(days=SHARE_DAYS[0]), T)
    return {s: res[s] / sh[s] for s in SIZES}, sh


def year_loss(F, tp):
    sent = fills_between(F, T1, T2)
    back = own_back(F, T1, T2)
    o1, sh1 = out_scaled(F, tp, T1)
    o2, sh2 = out_scaled(F, tp, T2)
    loss = {s: sent[s] - back[s] - (o2[s] - o1[s]) for s in SIZES}
    return {"loss": loss, "sent": sent, "back": back, "out1": o1, "out2": o2, "share1": sh1, "share2": sh2}


def usable(F, tp, out2=None):
    on = stock_on_site(F, 2026, ["clean empty", "awaiting repair"])
    if out2 is None:
        out2, _ = out_scaled(F, tp, T2)
    return {s: on[s] + out2[s] for s in SIZES}, on


def register_active(F):
    reg = F["register"]
    return {s: float(((reg.size_l == s) & (reg.status == "ACTIVE")).sum()) for s in SIZES}


def gate_loss(F, a=T1, b=T2):
    g = F["gate"]
    sel = g[(g.date > a) & (g.date <= b)]
    return {s: float(sel[sel["size"] == s].fulls_out.sum() - sel[sel["size"] == s].empties_in.sum()) for s in SIZES}


# ------------------------------------------------------------------------------------------------- R3 the forecast
def weekly_weather(F):
    wx = F["weather"]
    lw = wx[wx.station == "Leeds Weather Centre"].set_index("date").tmax_c
    lw = lw.reindex(pd.date_range("2016-01-01", "2026-11-30")).interpolate()
    return lw


def normal_day(lw):
    df = lw.to_frame("t")
    df = df[df.index.year <= 2025]
    df["md"] = df.index.strftime("%m-%d")
    return df.groupby("md").t.mean()


def features(days, temps):
    """daily drivers: the calendar (two harmonics of the year), the warmth over 17 C, the cool under it, bank
    holidays and the day before, the Christmas fortnight, January, the trend"""
    bh = set(pd.to_datetime(P.BANK_HOLIDAYS))
    d = pd.DatetimeIndex(days)
    doy = d.dayofyear.values
    X = pd.DataFrame(index=d)
    for k in (1, 2):
        X["c%d" % k] = np.cos(2 * np.pi * k * doy / 365.25)
        X["s%d" % k] = np.sin(2 * np.pi * k * doy / 365.25)
    t = np.asarray(temps, dtype=float)
    X["warm"] = np.maximum(0, t - 17.0)
    X["cool"] = np.minimum(0, t - 17.0)
    X["bank"] = [1.0 if x in bh else 0.0 for x in d]
    X["eve"] = [1.0 if (x + pd.Timedelta(days=1)) in bh else 0.0 for x in d]
    X["xmas"] = ((d.month == 12) & (d.day >= 10)).astype(float)
    X["jan"] = (d.month == 1).astype(float)
    X["trend"] = (d - pd.Timestamp("2024-01-01")).days / 365.25
    return X


def fit_weekly(F, s, lw):
    """weekly deliveries of a size (the depot gates' fulls out) on the week's own drivers, log-linear"""
    g = F["gate"]
    gs = g[g["size"] == s].groupby("date").fulls_out.sum()
    gs = gs.reindex(pd.date_range(P.H0, P.ASOF), fill_value=0.0)
    wk = gs.resample("W-SUN").sum()
    wk = wk[(wk.index > pd.Timestamp("2023-12-03")) & (wk.index <= pd.Timestamp("2026-11-29"))]
    days = pd.date_range(P.H0, P.ASOF)
    X = features(days, lw.reindex(days).values).resample("W-SUN").mean()
    X = X.loc[wk.index]
    A = np.column_stack([np.ones(len(X)), X.values])
    y = np.log(wk.values)
    beta, *_ = np.linalg.lstsq(A, y, rcond=None)
    resid = y - A @ beta
    return beta, list(X.columns), float(np.std(resid, ddof=A.shape[1]))


def predict_days(beta, days, temps):
    X = features(days, temps)
    A = np.column_stack([np.ones(len(X)), X.values])
    return pd.Series(np.exp(A @ beta), index=X.index)


def season_weeks():
    return pd.date_range("2027-05-03", "2027-09-26", freq="W-MON")


def daily_profile(beta, temps27):
    """the model's daily deliveries rate through 2027, from 1 December 2026"""
    days = pd.date_range("2026-12-01", "2027-10-31")
    return predict_days(beta, days, temps27.reindex(days).values) / 7.0


def temps_2027(lw, like=None):
    days = pd.date_range("2026-12-01", "2027-10-31")
    if like is None:
        nd = normal_day(lw)
        return pd.Series([nd[x.strftime("%m-%d") if x.strftime("%m-%d") != "02-29" else "02-28"] for x in days],
                         index=days)
    nd = normal_day(lw)
    vals = []
    for x in days:
        day = min(x.day, 28) if x.month == 2 else x.day
        if x.year == 2027:
            vals.append(lw[pd.Timestamp(like, x.month, day)])
        else:
            vals.append(nd[x.strftime("%m-%d")])
    return pd.Series(vals, index=days)


def extra_lines(F, s):
    """the plan's new lines of a size: Maplestead's pubs from their first delivery week, the new Foundry taps"""
    pl = F["plan"]
    out = []
    if s in (50, 30):
        mp = pl["Maplestead pubs"]
        for _, r in mp[mp.keg_l == s].iterrows():
            out.append((pd.Timestamp(r.first_delivery_week), float(r.expected_kegs_per_week), r.pub, r.beer_code))
    if s == 20:
        for _, r in pl["New Foundry taps"].iterrows():
            out.append((pd.Timestamp(r.tap_from), float(r.expected_kegs_per_week), r.account, "FOUNDRY"))
    return out


def weekly_2027(F, s, lw, like=None, beta=None):
    if beta is None:
        beta, cols, sd = fit_weekly(F, s, lw)
    t27 = temps_2027(lw, like)
    base = daily_profile(beta, t27)
    # the plan's expected kegs a week are a year's average: carried through the year by the size's own profile
    nt = temps_2027(lw, None)
    prof = daily_profile(beta, nt)
    year = prof[(prof.index >= "2027-01-01") & (prof.index <= "2027-10-31")]
    rel = base / year.mean()
    extra = pd.Series(0.0, index=base.index)
    for start, rate, who, code in extra_lines(F, s):
        extra[extra.index >= start] += rate / 7.0 * rel[rel.index >= start]
    tot = (base + extra).resample("W-SUN").sum()
    weeks = [x + pd.Timedelta(days=6) for x in season_weeks()]
    return tot.loc[weeks], (base.resample("W-SUN").sum().loc[weeks]), (extra.resample("W-SUN").sum().loc[weeks])


def busiest_deliveries(F, lw):
    out = {}
    for s in SIZES:
        beta, cols, sd = fit_weekly(F, s, lw)
        tot, base, extra = weekly_2027(F, s, lw, None, beta)
        peaks = []
        for y in range(2016, 2026):
            t, b, e = weekly_2027(F, s, lw, y, beta)
            peaks.append(float(t.max()))
        prof = daily_profile(beta, temps_2027(lw, None))
        for start, rate, who, code in extra_lines(F, s):
            prof[prof.index >= start] += rate / 7.0
        sent = gate_daily(F, s)
        out[s] = {"profile": prof, "year_sent": float(sent[(sent.index > T1) & (sent.index <= T2)].sum()),
                  "point": float(tot.max()), "week": tot.idxmax(), "lo": float(np.percentile(peaks, 10)),
                  "hi": float(np.percentile(peaks, 90)), "peaks": peaks, "weekly": tot, "base": base, "extra": extra,
                  "beta": beta}
    return out


# ------------------------------------------------------------------------------------------------- R4 holdings
def account_rates(F, a, b):
    """each account's kegs delivered a week by size in (a, b], renumbered accounts carried to their new number"""
    v = F["visits"]
    sel = v[(v.visit_date > a) & (v.visit_date <= b)]
    weeks = (b - a).days / 7.0
    out = sel.groupby("account")[["fulls_50", "fulls_30", "fulls_20"]].sum() / weeks
    return out


def holding_data(F, months=(5, 6, 7, 8, 9)):
    """the reps' summer counts against each account's own year: kegs held of a size, the lines and taps of that size
    on the dispense register, the account's kegs delivered a week over the twelve months to November 2026 (accounts
    trading the whole year), its delivery interval"""
    au = F["audits"]
    au = au[au.count_date.dt.month.isin(months)]
    dl = F["dispense_lines"]
    ch = F["account_changes"]
    alias = dict(zip(ch.new_account, ch.old_account))
    sched = F["delivery_schedule"]
    freq = sched.groupby("account").frequency.first()
    lines = dl.groupby(["account", "keg_l"]).taps.agg(["count", "sum"])
    acc = F["accounts"].set_index("account")
    v = F["visits"]
    yr = v[(v.visit_date > T1) & (v.visit_date <= T2)].groupby("account")[["fulls_50", "fulls_30", "fulls_20"]].sum() / 52.18
    for old, new in alias.items():
        pass
    rows = []
    for _, r in au.iterrows():
        a = r.account
        if a not in yr.index:
            continue
        op = acc.opened.get(a)
        cl = acc.closed.get(a)
        if op is None or str(op) > "2025-11-30" or (cl is not None and str(cl) != "None" and str(cl) <= "2026-11-30"):
            continue
        f = freq.get(a, "weekly")
        interval = 7.0 if f == "weekly" else 3.5
        for s in SIZES:
            key = (a, s)
            if key not in lines.index:
                continue
            nl, taps = lines.loc[key]
            held = r["full_%d" % s] + r["on_tap_%d" % s] + r["empty_%d" % s]
            rows.append((a, s, r.count_date, nl, taps, float(yr.loc[a, "fulls_%d" % s]), interval, held))
    return pd.DataFrame(rows, columns=["account", "size", "date", "lines", "taps", "rate", "interval", "held"])


def fit_holding(hd):
    """kegs a customer holds of a size: one on each tap, the rest its order cover, by line"""
    X = np.column_stack([hd.taps.values, (hd.rate * (hd.interval + 7.0) / 7.0).values, hd.lines.values])
    y = hd.held.values
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    return beta


def predict_holding(beta, taps, rate, interval, lines):
    return beta[0] * taps + beta[1] * rate * (interval + 7.0) / 7.0 + beta[2] * lines


def estate_kegs(F, R3, beta):
    """Maplestead's pubs' kegs at the size's busiest week: each line at its expected rate carried to that week"""
    pl = F["plan"]["Maplestead pubs"]
    out = {}
    for s in (50, 30):
        wk = R3[s]["week"]
        # the week's level against the year's average, from the size's own 2027 profile
        prof = R3[s]["base"]
        yr = R3[s]["beta"]
        rel = rel_level(F, s, wk)
        sel = pl[pl.keg_l == s]
        tot = 0.0
        for _, r in sel.iterrows():
            if pd.Timestamp(r.first_delivery_week) > wk:
                continue
            tot += predict_holding(beta, 1, r.expected_kegs_per_week * rel, 7.0, 1)
        out[s] = tot
    return out


_REL = {}


def rel_level(F, s, wk, lw=None):
    key = (s, wk)
    if key in _REL:
        return _REL[key]
    if lw is None:
        lw = weekly_weather(F)
    beta, cols, sd = fit_weekly(F, s, lw)
    prof = daily_profile(beta, temps_2027(lw, None))
    year = prof[(prof.index >= "2027-01-01") & (prof.index <= "2027-10-31")].mean()
    week = prof[(prof.index > wk - pd.Timedelta(days=7)) & (prof.index <= wk)].mean()
    _REL[key] = week / year
    return _REL[key]


def holding_binned(hd, s, rate, interval=7.0, width=0.2):
    """kegs held per line at a line rate, read off the counted customers of that delivery interval with one line
    per tap near that rate"""
    x = hd[(hd["size"] == s) & (hd.interval == interval) & (hd.lines == hd.taps) & (hd.lines > 0)].copy()
    x["per_line"] = x.held / x.lines
    x["r_line"] = x.rate / x.lines
    near = x[(x.r_line > rate - width) & (x.r_line < rate + width)]
    if len(near) < 12:
        near = x.iloc[(x.r_line - rate).abs().argsort()[:30]]
    return float(near.per_line.mean())


# ------------------------------------------------------------------------------------------------- R5, R6, R7
def clean_path(F, a, b):
    """clean empties at the washer day by day from the stocktake at a: washed in, filled out"""
    st = stock_on_site(F, a.year, ["clean empty"])
    w = F["washer"]
    fl = F["fills"]
    days = pd.date_range(a.normalize() + pd.Timedelta(days=1), b.normalize())
    out = {}
    for s in SIZES:
        wi = w[w["size"] == s].groupby("date").washed_ok.sum().reindex(days, fill_value=0)
        fo = fl[fl.keg_l == s].groupby("date").kegs_filled.sum().reindex(days, fill_value=0)
        out[s] = st[s] + (wi - fo).cumsum()
    return out


def foundry_store_2026(F, a, b):
    """full Foundry kegs in the cold store through the year from the 2025 stocktake: racked in, sent to the depots"""
    st = stock_on_site(F, a.year, ["full"])
    cold = F["stocktake"][a.year]
    c0 = float(cold[(cold.site == "Brighouse cold store") & (cold.condition == "full")]["20 l"].sum())
    days = pd.date_range(a.normalize() + pd.Timedelta(days=1), b.normalize())
    fl = F["fills"]
    rk = fl[fl.keg_l == 20].groupby("date").kegs_filled.sum().reindex(days, fill_value=0)
    g = F["gate"]
    out = g[g["size"] == 20].groupby("date").fulls_out.sum().reindex(days, fill_value=0)
    return c0 + (rk - out).cumsum()


DEPOT_RULE = ["beers"]


def foundry_store_2027(F, R3, lw):
    """the cold store's full Foundry kegs through 2027 from the November stocktake: the brew plan's racking in, the
    range's forecast deliveries out (the depots' stock moving with the deliveries)"""
    cold = F["stocktake"][2026]
    c0 = float(cold[(cold.site == "Brighouse cold store") & (cold.condition == "full")]["20 l"].sum())
    br = F["plan"]["Foundry brews"]
    days = pd.date_range("2026-12-01", "2027-10-31")
    rk = br.groupby(pd.to_datetime(br.racking_date)).kegs.sum().reindex(days, fill_value=0)
    beta = R3[20]["beta"]
    base = daily_profile(beta, temps_2027(lw, None))
    extra = pd.Series(0.0, index=days)
    nt = base[(base.index >= "2027-01-01")].mean()
    for start, rate, who, code in extra_lines(F, 20):
        extra[extra.index >= start] += rate / 7.0 * (base[base.index >= start] / nt)
    disp = base + extra
    # the depots hold the range beer by beer: their 20 litre fulls at the stocktake, per beer then on sale, carried
    # by the beers on sale through the year
    rng_ = F["plan"]["Foundry range"]
    on = pd.Series([((pd.to_datetime(rng_.on_sale_from) <= d) & (pd.to_datetime(rng_.on_sale_to) >= d)).sum()
                    for d in days], index=days).astype(float)
    dep0 = float(cold[(cold.site.str.endswith("depot")) & (cold.condition == "full")]["20 l"].sum())
    depot = dep0 * on / on.iloc[0]
    if DEPOT_RULE[0] == "beers_and_rate":
        depot = depot * disp.rolling(14, min_periods=1).mean() / disp.iloc[:14].mean()
    out_ = disp + depot.diff().fillna(0.0)
    # oldest first out of the store; beer past its 120 days poured away (the range's own life)
    from collections import deque
    q = deque([[days[0] - pd.Timedelta(days=30), c0]])
    fg = []
    for d in days:
        if rk.loc[d] > 0:
            q.append([d, float(rk.loc[d])])
        need = float(out_.loc[d])
        while need > 1e-9 and q:
            take = min(need, q[0][1])
            q[0][1] -= take
            need -= take
            if q[0][1] <= 1e-9:
                q.popleft()
        while q and (d - q[0][0]).days > 120:
            q.popleft()
        fg.append(sum(x[1] for x in q))
    fg = pd.Series(fg, index=days)
    return fg, disp


def circulation_2026(F, tp, yl):
    """kegs in circulation through the year to November 2026: the fleet less the clean empties, the fleet from the
    2025 stocktake's count run down by the year's loss"""
    on25 = stock_on_site(F, 2025, ["clean empty", "awaiting repair"])
    u1 = {s: on25[s] + yl["out1"][s] for s in SIZES}
    cp = clean_path(F, T1, T2)
    out = {}
    for s in SIZES:
        idx = cp[s].index
        frac = np.arange(1, len(idx) + 1) / len(idx)
        fleet = u1[s] - yl["loss"][s] * frac
        out[s] = pd.Series(fleet, index=idx) - cp[s]
    return out, u1


def gate_daily(F, s):
    g = F["gate"]
    days = pd.date_range(P.H0, P.ASOF)
    return g[g["size"] == s].groupby("date").fulls_out.sum().reindex(days, fill_value=0.0)


def need_2027(F, tp, yl, R3, lw, hd, hold_fn=None, fg27=None, elastic=None):
    """kegs needed in circulation in each size's busiest week: the existing trade's circulation carried from 2026
    week for week by its deliveries (at the response the 2026 weeks show), the Foundry cold store walked from the brew
    plan, Maplestead's and the new taps' lines held as counted customers hold such lines, with their kegs on the way
    back; and the washer's float"""
    c26, u1 = circulation_2026(F, tp, yl)
    if fg27 is None:
        fg27, disp20 = foundry_store_2027(F, R3, lw)
    fg26 = foundry_store_2026(F, T1, T2)
    res = {}
    for s in SIZES:
        dl = gate_daily(F, s)
        d26 = dl[(dl.index > T1) & (dl.index <= T2)].rolling(7).mean()
        base = c26[s] - (fg26 if s == 20 else 0.0)
        x = pd.DataFrame({"c": base, "d": d26}).dropna()
        x = x[(x.d > 0) & (x.index.month >= 5) & (x.index.month <= 9)]      # the 2026 season's own days
        fit = np.polyfit(np.log(x.d), np.log(x.c), 1)
        el = elastic.get(s) if isinstance(elastic, dict) else elastic
        e = fit[0] if el is None else el
        a0 = fit[1] if el is None else float(np.mean(np.log(x.c) - e * np.log(x.d)))
        beta = R3[s]["beta"]
        b27 = daily_profile(beta, temps_2027(lw, None)).rolling(7).mean()
        weeks = season_weeks()
        rows = []
        for wk in weeks:
            end = wk + pd.Timedelta(days=6)
            ex = float(np.exp(a0) * b27.loc[wk:end].mean() ** e)
            rel = b27.loc[end] / b27[(b27.index >= "2027-01-01")].mean()
            new = 0.0
            pipe = 0.0
            for start, rate, who, code in extra_lines(F, s):
                if start > end:
                    continue
                rr = rate * rel
                new += hold_fn(s, rate) if hold_fn else holding_binned(hd, s, rate)
                pipe += rr / 7.0 * PIPE_DAYS[s]
            fg = fg27.loc[wk:end].mean() if s == 20 else 0.0
            rows.append((end, ex, new, pipe, fg))
        df = pd.DataFrame(rows, columns=["week", "existing", "new_lines", "new_pipe", "foundry_store"]).set_index("week")
        df["total"] = df.sum(axis=1)
        res[s] = {"weekly": df, "elasticity": e, "week": df.total.idxmax(), "peak": float(df.total.max())}
    return res


PIPE_DAYS = {}


def pipe_days(F, tp):
    """the days a keg of a size spends off the customer's premises in a trip: filled to delivered (the tagged trips'
    median in 2026), and collected to the washer (the depots' empties and the trunks at the stocktake against the
    empties collected a day in November); for 20 litre kegs the cold store is walked on its own, so the return leg"""
    v = F["visits"]
    nov = v[(v.visit_date > "2026-10-31") & (v.visit_date <= "2026-11-30")]
    st = F["stocktake"][2026]
    out = {}
    for s in SIZES:
        col = {50: "50 l", 30: "30 l", 20: "20 l"}[s]
        held = st[(st.condition == "empty")][col].sum()
        per_day = pd.to_numeric(nov["empties_%d" % s], errors="coerce").sum() / 30.0
        back = held / per_day if per_day else 2.0
        t = tp[(tp["size"] == s) & tp.deliver.notna() & (tp.start > "2026-01-01")]
        fwd = float(((t.deliver - t.start).dt.total_seconds() / 86400).median())
        out[s] = back + (fwd if s != 20 else 0.0)
    PIPE_DAYS.update(out)
    return out


def season_float(F, R3, s):
    if s == 20:
        br = F["plan"]["Foundry brews"]
        r = pd.to_datetime(br.racking_date)
        kegs = br[(r >= "2027-05-03") & (r <= "2027-09-26")].kegs.sum()
    else:
        kegs = R3[s]["weekly"].sum()
    return 2.0 * kegs / (21 * 6)


def order(F, tp, yl, u2, R3, R6):
    out = {}
    for s in SIZES:
        wk = R6[s]["week"]
        mid = wk - pd.Timedelta(days=3)
        # the year's loss is a loss per keg sent out: carried to the busiest week by the kegs the forecast sends out
        prof = R3[s]["profile"]
        lost = yl["loss"][s] * float(prof[:mid].sum()) / R3[s]["year_sent"]
        need = R6[s]["peak"] + season_float(F, R3, s)
        have = u2[s] - lost
        out[s] = {"need": need, "have": have, "lost_to_week": lost, "float": season_float(F, R3, s),
                  "buy": max(0.0, need - have)}
    return out


# ------------------------------------------------------------------------------------------------- hurried routes
def dwell_at_customers(tp, s, a=T1, b=T2):
    """the size's average time out per trip, filled to back at the washer, over the year's settled trips (days)"""
    t = tp[(tp["size"] == s) & tp.ret.notna() & (tp.start > a) & (tp.start <= b - pd.Timedelta(days=60))]
    return float(((t.ret - t.start).dt.total_seconds() / 86400).mean())


def turns_holding(F, tp, R3, s, extra_only=True):
    """a new line's kegs at the fleet's turns: its busiest-week deliveries times the size's average days out"""
    days = dwell_at_customers(tp, s)
    rel = rel_level(F, s, R3[s]["week"])
    tot = 0.0
    for start, rate, who, code in extra_lines(F, s):
        tot += rate * rel / 7.0 * days
    return tot


def foundry_days_of_cover(F, R3, wk):
    """the cold store at the November stocktake's days of cover, carried to the week's deliveries"""
    cold = F["stocktake"][2026]
    c0 = float(cold[(cold.site == "Brighouse cold store") & (cold.condition == "full")]["20 l"].sum())
    g = gate_daily(F, 20)
    nov = g["2026-11-01":"2026-11-30"].mean()
    wkd = R3[20]["weekly"]
    d = float(wkd.loc[wkd.index[np.argmin(np.abs((wkd.index - wk).days))]]) / 7.0
    return c0 / nov * d
