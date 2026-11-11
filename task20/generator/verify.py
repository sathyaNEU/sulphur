"""task20 verify: an independent recomputation of the graded figures from target/ (its own readers, its own book
roll-forward, its own engine), held against figures.json. Shares no code with analysis.py.

    python3 task20/generator/verify.py
"""
import json
import os
import sys
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TGT = os.path.join(os.path.dirname(HERE), "target")
NY = ZoneInfo("America/New_York")


def find(prefix):
    return os.path.join(TGT, next(f for f in sorted(os.listdir(TGT)) if f.startswith(prefix)))


def main():
    F = json.load(open(os.path.join(HERE, "figures.json")))
    fails = []

    def ok(label, cond, detail=""):
        print("%s  %s %s" % ("PASS" if cond else "FAIL", label, detail))
        if not cond:
            fails.append(label)
    m = pd.read_csv(find("smcf_instrument_master"), dtype=str, keep_default_na=False).sort_values("instrument_id")
    ids = list(m.instrument_id)
    col = {x: j for j, x in enumerate(ids)}
    v1 = dict(zip(m.legacy_eqx_id, m.instrument_id))
    vend = pd.read_csv(find("vendor_eod_closes"), dtype={"vendor_id": str}).drop_duplicates(["vendor_id", "price_date"])
    vend["id"] = vend.vendor_id.map(dict(zip(m.vendor_id, m.instrument_id)))
    px = vend.pivot(index="price_date", columns="id", values="close")[ids]
    dates = list(pd.to_datetime(px.index))
    PX = px.values.astype(float)
    di = {d: n for n, d in enumerate(dates)}
    spx = pd.read_csv(os.path.join(TGT, "SPX_History.csv"))
    spx.index = pd.to_datetime(spx.DATE, format="%m/%d/%Y")
    ndx = pd.read_csv(os.path.join(TGT, "NASDAQ100.csv"))
    ndx.index = pd.to_datetime(ndx.observation_date)
    S = spx.SPX.reindex(dates).values
    N = pd.to_numeric(ndx.NASDAQ100, errors="coerce").reindex(dates).values
    ret = PX[1:] / PX[:-1] - 1
    rs, rn = S[1:] / S[:-1] - 1, N[1:] / N[:-1] - 1          # ret[j] is the return of day j+1
    st = pd.read_csv(find("cme_es_nq_daily_settlements"))
    settle = {(c, pd.Timestamp(t)): float(x) for c, t, x in zip(st.contract, st.trade_date, st.settlement)}
    mp = pd.read_csv(find("ere_proxy_mapping"), dtype=str)
    mp["id"] = [v1.get(x, x) for x in mp.eqx_instrument]
    vint = {pd.Timestamp(v): g.set_index("id").reindex(ids) for v, g in mp.groupby("vintage")}
    cal = sorted(set(spx.index) | {pd.Timestamp(r[0]) for r in load_workbook(find("SMCF_H2_2025_business_plan"),
                                                                              data_only=True)["Calendar"].iter_rows(
        min_row=2, values_only=True) if r[0]})
    ci = {d: n for n, d in enumerate(cal)}
    start = np.array([np.searchsorted(cal, pd.Timestamp(x)) for x in m.desk_start])

    def var(q, fut, d, own=False, on=None, beta_day=None, lam=None):
        r = di[d]
        R = ret[r - 500:r].copy()
        sw, nw = rs[r - 500:r], rn[r - 500:r]
        if not own:
            vt = vint[max(v for v in vint if v <= (beta_day or d))]
            prox = (ci[on or d] - start) < 500
            b = vt.beta.astype(float).values
            nd = (vt.proxy_index == "NDX").values
            for j in np.where(prox)[0]:
                R[:, j] = b[j] * (nw if nd[j] else sw)
        pnl = R @ (q * PX[r]) + sum(n * (50.0 if c.startswith("ES") else 20.0) * settle[(c, d)] *
                                    (sw if c.startswith("ES") else nw) for c, n in fut.items())
        if lam:
            var0 = np.var(pnl[:50])
            hist = []
            for x in pnl:
                hist.append(var0)
                var0 = lam * var0 + (1 - lam) * x * x
            pnl = pnl * np.sqrt(var0 / np.array(hist))
        return -np.sort(pnl)[4]
    # the book: the first extract rolled forward by trade date with each ticket's last version
    e1 = pd.read_csv(find("eqx_position_extract_v1"), dtype=str)
    first = e1.EXTRACT_ID.iloc[0]
    q0 = np.zeros(len(ids))
    for i, q in zip(e1[e1.EXTRACT_ID == first].INSTR_ID, e1[e1.EXTRACT_ID == first].POS_QTY):
        q0[col[v1[i]]] = float(q)
    d0 = pd.Timestamp(pd.to_datetime(e1.EXTRACT_TS.iloc[0]).date())
    bl = pd.read_csv(find("oms_trade_blotter"), dtype=str, keep_default_na=False).drop_duplicates()
    bl["version"] = bl.version.astype(int)
    last = bl.sort_values("version").groupby("trade_id").tail(1)
    eq = last[(last.asset_class == "EQ") & (last.status != "CANCEL")]
    sgn = np.where(eq.side == "BUY", 1.0, -1.0) * eq.quantity.astype(float)
    flow = pd.DataFrame(dict(td=pd.to_datetime(eq.trade_date), j=[col[v1.get(x, x)] for x in eq.eqx_instrument], q=sgn))
    book = {d0: q0.copy()}
    cur = q0.copy()
    for d in [x for x in dates if x > d0]:
        f = flow[flow.td == d]
        np.add.at(cur, f.j.values, f.q.values)
        book[d] = cur.copy()
    fu = pd.read_csv(find("futs_position_snapshots"))
    futs = {pd.Timestamp(d): dict(zip(g.contract, g.net_contracts.astype(float))) for d, g in fu.groupby("position_date")}
    pc = pd.read_csv(find("pc_daily_pnl")).sort_values("version").groupby("business_date").tail(1)
    pc.index = pd.to_datetime(pc.business_date)
    rl = pd.read_csv(find("ere_run_log"), dtype=str, keep_default_na=False)
    rl = rl[rl.status != "FAILED"]
    rep = {pd.Timestamp(d): float(x) for d, x in zip(rl.business_date, rl.var_99_1d_usd)}
    days = list(pc.index)
    prev = {d: dates[di[d] - 1] for d in days}
    hyp = {d: float(pc.loc[d, "hypothetical_pnl_usd"]) for d in days}
    bk = {d: float(pc.loc[d, "booked_pnl_usd"]) for d in days}
    exc = [d for d in days if min(hyp[d], bk[d]) < -rep[prev[d]]]
    ok("exceptions on either P&L", len(exc) == F["exceptions_total"], "%d" % len(exc))
    ok("on booked P&L", sum(bk[d] < -rep[prev[d]] for d in days) == F["official_count"])
    heads = {}
    for d in exc:
        p = prev[d]
        if hyp[d] >= -rep[p]:
            heads[d] = 1
        elif hyp[d] >= -var(book[p], futs[p], p):
            heads[d] = 2
        elif hyp[d] >= -var(book[p], futs[p], p, own=True):
            heads[d] = 3
        elif hyp[d] >= -var(book[p], futs[p], p, own=True, lam=0.94):
            heads[d] = 4
        else:
            heads[d] = 5
    mine = {d.date().isoformat(): c for d, c in heads.items()}
    ok("every exception's heading", mine == {k: int(v) for k, v in F["r6_headings"].items()})
    snd = sum(hyp[d] < -var(book[prev[d]], futs[prev[d]], prev[d], own=True, lam=0.94) for d in days)
    ok("the sound model's count", snd == F["sound_count"], "%d" % snd)
    reused = [d for d, e in zip(rl.business_date, rl.eqx_extract) if not e.replace("-", "").replace(".", "")
              .count(d.replace("-", ""))]
    ok("runs that read an older extract", len(reused) == F["outage_runs"], "%d" % len(reused))
    # the add-on: the 30 June run's extract scaled by segment, hedged at 86 per cent, priced on the 30 June window
    dl = dates[-1]
    e2 = pd.read_csv(find("eqx_position_extract_v2"), dtype=str)
    run30 = rl[rl.business_date == dl.date().isoformat()].eqx_extract.iloc[0]
    qb = np.zeros(len(ids))
    sel = e2[e2.extract_id == run30]
    for i, q in zip(sel.instrument_id, sel.quantity):
        qb[col[i]] = float(q)
    seg = m.segment.values
    wb = load_workbook(find("SMCF_H2_2025_business_plan"), data_only=True)
    plan = [r for r in wb["Plan"].iter_rows(min_row=2, values_only=True) if r[0] and str(r[0]).startswith("2025-")]
    vt = vint[max(vint)]
    b = vt.beta.astype(float).values
    nd = (vt.proxy_index == "NDX").values
    out = []
    for r in plan:
        mv = qb * PX[-1]
        f = np.where(seg == "Small cap", r[2] * 1e6 / np.abs(mv[seg == "Small cap"]).sum(),
                     r[1] * 1e6 / np.abs(mv[seg == "Mid cap"]).sum())
        q = np.round(qb * f)
        mvq = q * PX[-1]
        fut = {"ESU5": round(-0.86 * (mvq * b)[~nd].sum() / (50 * settle[("ESU5", dl)])),
               "NQU5": round(-0.86 * (mvq * b)[nd].sum() / (20 * settle[("NQU5", dl)]))}
        firstday = min(d for d in cal if d.strftime("%Y-%m") == r[0])
        on = cal[ci[firstday] - 1]
        a = var(q, fut, dl, own=True) - var(q, fut, dl, on=on, beta_day=dl)
        out.append(round(max(0.0, a) / 1e6, 2))
    ok("the add-on by month", out == F["addon_m"], str(out))
    print("%d FAIL" % len(fails))
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
