"""task20 analysis: every figure the goldens and the answer blocks state, computed from the shipped files in target/
alone (never from world.py), with the rivals that set each band and the quick and careful-but-hurried passes that
effort.json prices. The engine is re-implemented from the methodology note; checks.py holds it to the run log."""
import datetime as dt
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import pack as PK
import docs as DC

NY = ZoneInfo("America/New_York")
W_DAYS, Q_RANK, HEDGE = 500, 5, 0.86
MULT = {"ES": 50.0, "NQ": 20.0}
TECH = ("Technology", "Communication Services")
LAMS = (0.94, 0.95, 0.96, 0.97)
GOLD_LAM, GOLD_SCALE = 0.94, "portfolio"
HEAD = {"income": "Other income", "inputs": "Inputs", "omitted": "Risks not in the model", "volatility": "Volatility",
        "sound": "Model accuracy"}
CODE = {"income": 1, "inputs": 2, "omitted": 3, "volatility": 4, "sound": 5}


# ------------------------------------------------------------------------------------------------ reading the pack
def ts_ny(s):
    t = pd.Timestamp(s)
    return t.tz_localize(NY) if t.tzinfo is None else t.tz_convert(NY)


def load(tgt):
    P = {}
    master = pd.read_csv(os.path.join(tgt, PK.F_MASTER), dtype=str, keep_default_na=False)
    P["master"] = master
    inst = list(master.instrument_id)
    P["inst"] = inst
    pos = {x: n for n, x in enumerate(inst)}
    P["pos"] = pos
    xw = pd.read_csv(os.path.join(tgt, PK.F_XWALK), dtype=str)
    v1to2 = dict(zip(xw.eqx_v1_instrument, xw.eqx_v2_instrument))
    P["v1to2"] = v1to2

    def to_v2(x):
        return v1to2.get(x, x)
    # vendor closes: the re-sent days loaded twice are the same rows; keyed by the vendor's id (one name was renamed)
    v = pd.read_csv(os.path.join(tgt, PK.F_VENDOR), dtype={"vendor_id": str, "ticker": str})
    v = v.drop_duplicates()
    assert not v.duplicated(["vendor_id", "price_date"]).any()
    v2inst = dict(zip(master.vendor_id, master.instrument_id))
    v["inst"] = v.vendor_id.map(v2inst)
    px = v.pivot(index="price_date", columns="inst", values="close")[inst]
    px.index = pd.to_datetime(px.index)
    # the index tape (Cboe and FRED as published; FRED leaves market holidays blank)
    spx = pd.read_csv(os.path.join(tgt, PK.F_SPX))
    spx["DATE"] = pd.to_datetime(spx["DATE"], format="%m/%d/%Y")
    spx = spx.set_index("DATE")["SPX"].astype(float)
    ndx = pd.read_csv(os.path.join(tgt, PK.F_NDX))
    ndx.columns = ["d", "v"]
    ndx["d"] = pd.to_datetime(ndx["d"])
    ndx["v"] = pd.to_numeric(ndx["v"], errors="coerce")
    ndx = ndx.dropna().set_index("d")["v"]
    dates = px.index
    assert spx.reindex(dates).notna().all() and ndx.reindex(dates).notna().all()
    P["dates"] = dates
    P["PX"] = px.values
    P["SPX"] = spx.reindex(dates).values
    P["NDX"] = ndx.reindex(dates).values
    P["exch_cal"] = list(spx.index)              # the exchange calendar from 1975, for the store's day counts
    P["R"] = np.vstack([np.zeros(len(inst)), P["PX"][1:] / P["PX"][:-1] - 1])
    P["RS"] = np.r_[0.0, P["SPX"][1:] / P["SPX"][:-1] - 1]
    P["RN"] = np.r_[0.0, P["NDX"][1:] / P["NDX"][:-1] - 1]
    P["seg"] = np.array(["SMALL" if s == "Small cap" else "MID" for s in master.segment])
    P["tech"] = np.isin(master.gics_sector.values, TECH)
    P["store_start"] = [pd.Timestamp(x) for x in master.desk_start]
    # settlements
    st = pd.read_csv(os.path.join(tgt, PK.F_SETTLE))
    st["trade_date"] = pd.to_datetime(st["trade_date"])
    P["settle"] = {(r.contract, r.trade_date): float(r.settlement) for r in st.itertuples()}
    # mapping vintages
    mp = pd.read_csv(os.path.join(tgt, PK.F_MAP), dtype=str)
    mp["inst"] = mp.eqx_instrument.map(to_v2)
    mp["vintage"] = pd.to_datetime(mp["vintage"])
    vint = {}
    for vd, g in mp.groupby("vintage"):
        g = g.set_index("inst").reindex(inst)
        vint[vd] = dict(beta=g.beta.astype(float).values, index=g.proxy_index.values,
                        series=g.series_at_vintage.values)
    P["vintages"] = vint
    P["map_store_start"] = mp.groupby("inst").store_start.first().reindex(inst).values
    # the EQX extracts (two schemas; the cutover day is in both)
    e1 = pd.read_csv(os.path.join(tgt, PK.F_EQX1), dtype={"INSTR_ID": str})
    e1["at"] = [pd.Timestamp(dt.datetime.strptime(x, "%m/%d/%Y %H:%M:%S")).tz_localize(NY) for x in e1.EXTRACT_TS]
    e1 = pd.DataFrame(dict(extract_id=e1.EXTRACT_ID, at=e1["at"], inst=e1.INSTR_ID.map(to_v2), qty=e1.POS_QTY.astype(float)))
    e2 = pd.read_csv(os.path.join(tgt, PK.F_EQX2), dtype={"instrument_id": str})
    e2 = pd.DataFrame(dict(extract_id=e2.extract_id, at=[ts_ny(x) for x in e2.extracted_at], inst=e2.instrument_id,
                           qty=e2.quantity.astype(float)))
    ex = {}
    ex_at = {}
    ids = {}
    for df in (e1, e2):
        for eid, g in df.groupby("extract_id", sort=False):
            at = g["at"].iloc[0]
            d = pd.Timestamp(at.date())
            q = np.zeros(len(inst))
            q[[pos[i] for i in g.inst]] = g.qty.values
            if d in ex:
                assert np.array_equal(ex[d], q), "the two schemas disagree on %s" % d.date()
            ex[d], ex_at[d] = q, at
            ids[eid] = d
    P["extract"], P["extract_at"], P["extract_day"] = ex, ex_at, ids
    # FUTS snapshots (stamped in UTC)
    fu = pd.read_csv(os.path.join(tgt, PK.F_FUTS))
    snaps, snap_day = {}, {}
    for sid, g in fu.groupby("snapshot_id", sort=False):
        d = pd.Timestamp(pd.Timestamp(g.snapshot_utc.iloc[0]).tz_convert(NY).date())
        snaps[d] = {c: float(n) for c, n in zip(g.contract, g.net_contracts)}
        snap_day[sid] = d
    P["futs"], P["futs_day"] = snaps, snap_day
    # the run log: the run of record for each business date
    rl = pd.read_csv(os.path.join(tgt, PK.F_RUNLOG), dtype=str, keep_default_na=False)
    ok = rl[rl.status.isin(["COMPLETE", "COMPLETE_WITH_WARNINGS"])].copy()
    assert not ok.business_date.duplicated().any()
    ok["d"] = pd.to_datetime(ok.business_date)
    P["runs"] = ok.set_index("d")
    P["runlog_all"] = rl
    # product control's daily P&L, latest version
    pc = pd.read_csv(os.path.join(tgt, PK.F_PC))
    pc = pc.sort_values(["business_date", "version"]).groupby("business_date").tail(1)
    pc["d"] = pd.to_datetime(pc.business_date)
    P["pc"] = pc.set_index("d")
    # the blotter: exact repeats dropped, versions in order, cancels to zero
    bl = pd.read_csv(os.path.join(tgt, PK.F_BLOTTER), dtype=str, keep_default_na=False)
    bl = bl.drop_duplicates()
    assert not bl.duplicated(["trade_id", "version"]).any()
    bl["version"] = bl.version.astype(int)
    bl["q"] = np.where(bl.side == "BUY", 1.0, -1.0) * bl.quantity.astype(float)
    bl.loc[bl.status == "CANCEL", "q"] = 0.0
    bl["at"] = [ts_ny(x) for x in bl.booked_at]
    bl["td"] = pd.to_datetime(bl.trade_date)
    bl["inst"] = bl.eqx_instrument.map(to_v2)
    P["blotter"] = bl.sort_values(["trade_id", "version"])
    # the plan
    wb = load_workbook(os.path.join(tgt, DC.F_PLAN), data_only=True)
    plan = [r for r in wb["Plan"].iter_rows(min_row=2, values_only=True) if r[0] and str(r[0]).startswith("2025-")]
    P["plan"] = [dict(month=r[0], mid=float(r[1]) * 1e6, small=float(r[2]) * 1e6) for r in plan]
    P["h2_cal"] = [pd.Timestamp(r[0]) for r in wb["Calendar"].iter_rows(min_row=2, values_only=True) if r[0]]
    wb2 = load_workbook(os.path.join(tgt, DC.F_BACKTEST), data_only=True)
    bt = [r for r in wb2["Daily"].iter_rows(min_row=2, values_only=True) if r[0]]
    P["official"] = pd.DataFrame(bt, columns=["d", "booked", "var", "run", "exc", "cum"])
    P["official"]["d"] = pd.to_datetime(P["official"]["d"])
    return P


# ------------------------------------------------------------------------------------------------ the engine
class Engine:
    def __init__(self, P):
        self.P = P
        self.di = {d: n for n, d in enumerate(P["dates"])}
        cal = sorted(set(P["exch_cal"]) | set(P["h2_cal"]))
        self.cal_i = {d: n for n, d in enumerate(cal)}
        self.ss_i = np.array([self.cal_i.get(d, np.searchsorted(cal, d)) for d in P["store_start"]])
        self.vdates = sorted(P["vintages"])

    def proxied(self, on):
        """the names the engine maps to a proxy in its run on date `on`: fewer than 500 own returns in the store"""
        n = self.cal_i[on] - self.ss_i
        return n < W_DAYS

    def vintage(self, on):
        return self.P["vintages"][max(v for v in self.vdates if v <= on)]

    def scen(self, r, mode="engine", proxy_on=None, beta_on=None):
        """the 500 scenario returns for the run on date index r (window: returns of days r-499..r)"""
        P = self.P
        R = P["R"][r - W_DAYS + 1:r + 1].copy()
        S = P["RS"][r - W_DAYS + 1:r + 1]
        N = P["RN"][r - W_DAYS + 1:r + 1]
        if mode == "engine":
            on = P["dates"][r] if proxy_on is None else proxy_on
            vt = self.vintage(P["dates"][r] if beta_on is None else beta_on)
            px = self.proxied(on)
            b = vt["beta"]
            idx_is_ndx = (vt["index"] == "NDX")
            R[:, px] = np.where(idx_is_ndx[px], 1.0, 0.0) * np.outer(N, b[px]) + \
                np.where(idx_is_ndx[px], 0.0, 1.0) * np.outer(S, b[px])
        return R, S, N

    def pnl(self, q, futs, r, R, S, N):
        P = self.P
        d = P["dates"][r]
        sc = R @ (q * P["PX"][r])
        for c, n in futs.items():
            notional = n * MULT[c[:2]] * P["settle"][(c, d)]
            sc = sc + notional * (S if c[:2] == "ES" else N)
        return sc

    def var(self, q, futs, r, mode="engine", lam=None, scale="portfolio", qrule="fifth", proxy_on=None, beta_on=None,
            window=W_DAYS):
        R, S, N = self.scen(r, mode, proxy_on, beta_on)
        if lam and scale == "series":
            X = np.column_stack([R, S, N])
            X = ewma_scale(X, lam)
            R, S, N = X[:, :-2], X[:, -2], X[:, -1]
        sc = self.pnl(q, futs, r, R, S, N)
        if lam and scale == "portfolio":
            sc = ewma_scale(sc, lam)
        if window != W_DAYS:
            sc = sc[-window:]
        return quantile_loss(sc, qrule, window)


def ewma_scale(x, lam):
    """filtered historical simulation: each scenario rescaled by current over then-current EWMA volatility"""
    x = np.asarray(x, float)
    v = np.var(x[:50], axis=0)
    vs = np.zeros_like(x)
    for i in range(len(x)):
        vs[i] = v
        v = lam * v + (1 - lam) * x[i] ** 2
    return x * np.sqrt(v) / np.sqrt(vs)


def quantile_loss(sc, qrule="fifth", n=W_DAYS):
    s = np.sort(sc)
    k = int(round(Q_RANK * n / W_DAYS))
    if qrule == "interp":
        return -(s[k - 1] + s[k]) / 2.0
    return -s[k - 1]


# ------------------------------------------------------------------------------------------------ the books
def close_books(P, bl=None):
    """the positions the desk held at each close: the evening extract plus every booking for that trade date or
    earlier made after the extract was cut (the blotter's booking times against the extract's), and the same book
    rolled forward from the opening extract by trade date"""
    bl = P["blotter"] if bl is None else bl
    eq = bl[bl.asset_class == "EQ"]
    pos = P["pos"]
    grp = {tid: g for tid, g in eq.groupby("trade_id", sort=False)}
    tick = pd.DataFrame(dict(tid=list(grp), td=[g.td.iloc[0] for g in grp.values()],
                             last=[g["at"].max() for g in grp.values()], inst=[g.inst.iloc[0] for g in grp.values()],
                             final=[g.q.iloc[-1] for g in grp.values()]))
    books, late, late_gross = {}, {}, {}
    days = sorted(P["extract"])
    for d in days:
        X = P["extract_at"][d]
        m = (tick.td <= d) & (tick["last"] > X)
        adj = np.zeros(len(P["inst"]))
        for tid, inst, fin in zip(tick.tid[m], tick.inst[m], tick.final[m]):
            g = grp[tid]
            before = g[g["at"] <= X]
            asof = before.q.iloc[-1] if len(before) else 0.0
            adj[pos[inst]] += fin - asof
        books[d] = P["extract"][d] + adj
        late[d] = adj
    # roll forward by trade date from the opening extract
    first = days[0]
    cum = P["extract"][first].copy()
    roll = {first: cum.copy()}
    fin = tick.groupby(["td", "inst"]).final.sum()
    by_day = {}
    for (td, inst), q in fin.items():
        by_day.setdefault(td, []).append((pos[inst], q))
    for d in days[1:]:
        for i, q in by_day.get(d, []):
            cum[i] += q
        roll[d] = cum.copy()
    fut = {d: dict(P["futs"][d]) for d in days}
    return books, roll, late, fut


# ------------------------------------------------------------------------------------------------ the analysis
def run(tgt):
    P = load(tgt)
    E = Engine(P)
    dates = P["dates"]
    di = E.di
    runs = P["runs"]
    books, roll, late, fut = close_books(P)
    window = [d for d in P["pc"].index]                       # the 250 business days
    assert len(window) == 250
    prev = {d: dates[di[d] - 1] for d in window}
    out = dict(P=P, E=E, window=window, prev=prev, books=books, roll=roll, late=late, fut=fut)
    # ---- the run of record, replicated on the extract it read
    rep, rep_rep, used_day, outage = {}, {}, {}, []
    for d, r in runs.iterrows():
        u = P["extract_day"][r.eqx_extract]
        fu = P["futs_day"][r.futs_snapshot]
        used_day[d] = (u, fu)
        rep[d] = float(r.var_99_1d_usd)
        rep_rep[d] = E.var(P["extract"][u], P["futs"][fu], di[d])
        if u != d:
            outage.append(d)
    out.update(rep=rep, rep_rep=rep_rep, used_day=used_day, outage_runs=outage)
    # ---- R1 the exceptions on either P&L
    pc = P["pc"]
    hyp = {d: float(pc.loc[d, "hypothetical_pnl_usd"]) for d in window}
    booked = {d: float(pc.loc[d, "booked_pnl_usd"]) for d in window}
    vr = {d: rep[prev[d]] for d in window}
    off = [d for d in window if booked[d] < -vr[d]]
    hx = [d for d in window if hyp[d] < -vr[d]]
    union = sorted(set(off) | set(hx))
    out.update(hyp=hyp, booked=booked, vr=vr, off=off, hx=hx, union=union)
    raw_pc = pd.read_csv(os.path.join(tgt, PK.F_PC))
    out["pc_restated"] = int((raw_pc.groupby("business_date").version.max() > 1).sum())
    out["failed_runs"] = int((P["runlog_all"].status == "FAILED").sum())
    # ---- the counterfactual VaRs on the book held at the previous close
    good, full, sound = {}, {}, {}
    fam = {}
    for d in window:
        p = prev[d]
        r = di[p]
        good[d] = E.var(books[p], fut[p], r)
        full[d] = E.var(books[p], fut[p], r, "own")
    for lam in LAMS:
        for scale in ("portfolio", "series"):
            fam[(lam, scale)] = {d: E.var(books[prev[d]], fut[prev[d]], di[prev[d]], "own", lam=lam, scale=scale)
                                 for d in window}
    sound = fam[(GOLD_LAM, GOLD_SCALE)]
    out.update(good=good, full=full, sound=sound, fam=fam)

    def classify(hypd, vgood, vfull, vsound, offset, hxset):
        cls = {}
        for d in sorted(set(offset) | set(hxset)):
            if d not in hxset:
                cls[d] = "income"
            elif hypd[d] >= -vgood[d]:
                cls[d] = "inputs"
            elif hypd[d] >= -vfull[d]:
                cls[d] = "omitted"
            elif hypd[d] >= -vsound[d]:
                cls[d] = "volatility"
            else:
                cls[d] = "sound"
        return cls
    cls = classify(hyp, good, full, sound, off, hx)
    out["cls"] = cls
    out["sound_days"] = [d for d in window if hyp[d] < -sound[d]]
    out["fam_cls"] = {k: classify(hyp, good, full, v, off, hx) for k, v in fam.items()}
    out["fam_count"] = {k: sum(hyp[d] < -v[d] for d in window) for k, v in fam.items()}
    # the reused extracts: did any decide an exception on the book actually held?
    out["outage_exc"] = [d for d in union if prev[d] in outage]
    out["outage_caused"] = [d for d in out["outage_exc"] if cls[d] == "inputs"]
    out["cutoff_caused"] = [d for d in union if cls[d] == "inputs" and prev[d] not in outage]
    # the closing allocations each run never saw
    out["late_gross"] = {d: float(np.abs(late[d] * P["PX"][di[d]]).sum()) for d in late}
    out["late_net"] = {d: float((late[d] * P["PX"][di[d]]).sum()) for d in late}
    run_days = [prev[d] for d in window]
    out["late_gross_median"] = float(np.median([out["late_gross"][d] for d in run_days]))
    out["runs_missing"] = sum(out["late_gross"][d] > 0 for d in run_days)
    out["late_var_effect"] = {d: good[d] - E.var(P["extract"][prev[d]], fut[prev[d]], di[prev[d]]) for d in window}
    # ---- the workbook's run-by-run and day-by-day tables
    out["input_rows"] = []
    for d in window:
        p = prev[d]
        u, _ = used_day[p]
        out["input_rows"].append([p.date().isoformat(), runs.loc[p, "eqx_extract"], "Yes" if u != p else "",
                                  round(out["late_gross"][p] / 1e6, 1), round(rep[p] / 1e6, 2), round(good[d] / 1e6, 2),
                                  round((good[d] - rep[p]) / 1e6, 2)])
    out["sound_rows"] = [[d.date().isoformat(), round(hyp[d] / 1e6, 2), round(sound[d] / 1e6, 2),
                          "Y" if hyp[d] < -sound[d] else ""] for d in window]
    # ---- the quantile rule the note rules out (interpolated between the fifth and sixth losses)
    gi = {d: E.var(books[prev[d]], fut[prev[d]], di[prev[d]], qrule="interp") for d in window}
    fi = {d: E.var(books[prev[d]], fut[prev[d]], di[prev[d]], "own", qrule="interp") for d in window}
    si = {d: E.var(books[prev[d]], fut[prev[d]], di[prev[d]], "own", lam=GOLD_LAM, qrule="interp") for d in window}
    out["interp_cls"] = classify(hyp, gi, fi, si, off, hx)
    # ---- the forward add-on
    out.update(addon(P, E))
    # ---- the hurried passes
    out.update(passes(P, E, out, classify))
    out["shortcuts"] = shortcuts(P, E, out)
    return out


def planned_book(P, E, base_q, mid, small, whole=True):
    d0 = P["dates"][-1]
    r0 = len(P["dates"]) - 1
    mv = base_q * P["PX"][r0]
    f = np.where(P["seg"] == "SMALL", small / np.abs(mv[P["seg"] == "SMALL"]).sum(),
                 mid / np.abs(mv[P["seg"] == "MID"]).sum())
    q = np.round(base_q * f) if whole else base_q * f
    vt = E.vintage(d0)
    m = q * P["PX"][r0]
    ndx = vt["index"] == "NDX"
    es = -HEDGE * float((m * vt["beta"])[~ndx].sum()) / (MULT["ES"] * P["settle"][("ESU5", d0)])
    nq = -HEDGE * float((m * vt["beta"])[ndx].sum()) / (MULT["NQ"] * P["settle"][("NQU5", d0)])
    if whole:
        es, nq = round(es), round(nq)
    return q, {"ESU5": es, "NQU5": nq}


def addon(P, E):
    d0 = P["dates"][-1]
    r0 = len(P["dates"]) - 1
    run30 = P["runs"].loc[d0]
    base = P["extract"][P["extract_day"][run30.eqx_extract]]
    cal = sorted(set(P["exch_cal"]) | set(P["h2_cal"]))
    months = P["plan"]
    firsts = [min(d for d in P["h2_cal"] if d.strftime("%Y-%m") == m["month"]) for m in months]
    run_for = [cal[cal.index(f) - 1] for f in firsts]          # the run whose VaR is reported for the month's first day
    res = dict(addon_months=[m["month"] for m in months], addon_run_for=run_for, addon_first_days=firsts)

    def path(proxy_days, books_by_month, floor=True):
        vals, parts = [], []
        for (q, fu), on in zip(books_by_month, proxy_days):
            full = E.var(q, fu, r0, "own")
            eng = E.var(q, fu, r0, "engine", proxy_on=on, beta_on=d0)
            a = full - eng
            vals.append(max(0.0, a) if floor else a)
            parts.append((full, eng, int(E.proxied(on).sum())))
        return vals, parts
    bk = [planned_book(P, E, base, m["mid"], m["small"]) for m in months]
    gold, parts = path(run_for, bk)
    res.update(addon=gold, addon_parts=parts, addon_books=bk)
    res["addon_unfloored"] = path(run_for, bk, floor=False)[0]
    # the golden family and the rival readings that set each month's band
    fam = {}
    fam["fractional shares and contracts"] = path(run_for, [planned_book(P, E, base, m["mid"], m["small"], whole=False)
                                                            for m in months])[0]
    fam["mapping of the month's first run"] = path(firsts, bk)[0]
    fam["mapping a business day earlier"] = path([cal[cal.index(x) - 1] for x in run_for], bk)[0]
    res["addon_family"] = fam
    # the shortcuts
    res["addon_ramp_only"] = path([d0] * len(months), bk)[0]
    tgt_book = [bk[-1]] * len(months)
    res["addon_grad_only"] = path(run_for, tgt_book)[0]
    now_full = E.var(base, P["futs"][P["futs_day"][run30.futs_snapshot]], r0, "own")
    now_eng = float(run30.var_99_1d_usd)
    a_now = max(0.0, now_full - now_eng)
    g0 = float(np.abs(base * P["PX"][r0]).sum())
    res["addon_now"] = a_now
    res["addon_now_parts"] = (now_full, now_eng)
    res["addon_prop"] = [a_now * (m["mid"] + m["small"]) / g0 for m in months]
    res["gross_30jun"] = {s: float(np.abs((base * P["PX"][r0])[P["seg"] == s]).sum()) for s in ("MID", "SMALL")}
    pxd = E.proxied(d0)
    res["proxied_30jun"] = int(pxd.sum())
    res["proxied_small_share"] = float(np.abs((base * P["PX"][r0])[pxd & (P["seg"] == "SMALL")]).sum() /
                                       res["gross_30jun"]["SMALL"])
    grads = []
    for i in np.where(pxd)[0]:
        for on in cal[cal.index(d0) + 1:]:
            if E.cal_i[on] - E.ss_i[i] >= W_DAYS:
                grads.append((on, P["inst"][i]))
                break
    res["graduations"] = sorted(grads)
    res["proxied_by_month"] = [int(E.proxied(on).sum()) for on in run_for]
    return res


def passes(P, E, out, classify):
    """the careful but hurried pass: product control's hypothetical P&L, the engine replicated on the extracts it
    read, the reused extracts re-run on that day's extract, the counterfactuals on the extract book, the add-on on the
    plan's ramp with the 30 June mapping held; the quick pass: the official file and the 30 June add-on"""
    di = E.di
    window, prev = out["window"], out["prev"]
    ex, fu = P["extract"], out["fut"]
    good_x = {d: E.var(ex[prev[d]], fu[prev[d]], di[prev[d]]) for d in window}
    full_x = {d: E.var(ex[prev[d]], fu[prev[d]], di[prev[d]], "own") for d in window}
    sound_x = {}
    for lam in (0.94, 0.97):
        for scale in ("portfolio", "series"):
            sound_x[(lam, scale)] = {d: E.var(ex[prev[d]], fu[prev[d]], di[prev[d]], "own", lam=lam, scale=scale)
                                     for d in window}
    cls_c = classify(out["hyp"], good_x, full_x, sound_x[(0.94, "portfolio")], out["off"], out["hx"])
    hyp = out["hyp"]
    res = dict(careful_cls=cls_c, careful_good=good_x, careful_full=full_x,
               careful_count={k: sum(hyp[d] < -v[d] for d in window) for k, v in sound_x.items()},
               careful_sound_days=[d for d in window if hyp[d] < -sound_x[(0.94, "portfolio")][d]])
    return res


def shortcuts(P, E, out):
    """the counts the forcing line is read against: the official figure, the corrected book with the proxies kept, no
    volatility response, and the extract book"""
    di, window, prev, books, fut = E.di, out["window"], out["prev"], out["books"], out["fut"]
    hyp = out["hyp"]
    noprox = {d: E.var(books[prev[d]], fut[prev[d]], di[prev[d]], "engine", lam=GOLD_LAM) for d in window}
    s = dict(official=len(out["off"]),
             noprox=sum(hyp[d] < -noprox[d] for d in window),
             novol=sum(hyp[d] < -out["full"][d] for d in window),
             extract_book=out["careful_count"][(0.94, "portfolio")])
    # perturbations of the sound model: the quantile interpolated, a slower decay, a one-year window
    s["interp"] = sum(hyp[d] < -E.var(books[prev[d]], fut[prev[d]], di[prev[d]], "own", lam=GOLD_LAM, qrule="interp")
                      for d in window)
    s["lam099"] = sum(hyp[d] < -E.var(books[prev[d]], fut[prev[d]], di[prev[d]], "own", lam=0.99) for d in window)
    s["win250"] = sum(hyp[d] < -E.var(books[prev[d]], fut[prev[d]], di[prev[d]], "own", lam=GOLD_LAM, window=250)
                      for d in window)
    return s
