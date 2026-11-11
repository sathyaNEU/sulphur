"""task9: the independent verifier. It reads only the shipped pack under target/ (CSV, XLSX and PDF) and recomputes the
graded figures on its own code path, importing nothing from the generator; it compares against the figures the answer
blocks state (generator/figures.json) and their bands.

    python3 task9/generator/verify.py        (exit 1 on any FAIL)
"""
import json
import os
import subprocess
import sys

import numpy as np
import pandas as pd
from openpyxl import load_workbook

HERE = os.path.dirname(os.path.abspath(__file__))
TASK = os.path.dirname(HERE)
TGT = os.path.join(TASK, "target")
F = json.load(open(os.path.join(HERE, "figures.json")))
ROWS = []
GROUPS = ["Equity long/short", "Quantitative equity", "Rates", "Currencies", "Credit", "Commodities", "Volatility"]
LAST = pd.Timestamp("2026-11-06")


def ok(label, cond, detail=""):
    ROWS.append(bool(cond))
    print("%s  %-84s %s" % ("PASS" if cond else "FAIL", label, str(detail)[:160]))


def t(name):
    return os.path.join(TGT, name)


def find(prefix):
    return [f for f in sorted(os.listdir(TGT)) if f.startswith(prefix)][0]


# ---------------------------------------------------------------- the record
def record():
    old = pd.read_csv(t(find("risk_pnl_daily_legacy")), dtype={"pod_code": str}).drop_duplicates()
    new = pd.read_csv(t(find("risk_pnl_daily_2023")), dtype={"book_id": str})
    cm = pd.read_csv(t(find("book_code_map")), dtype=str)
    m = dict(zip(cm.old_pod_code, cm.new_book_id))
    a = pd.DataFrame({"date": pd.to_datetime(old.cob_date), "pod": old.pod_code.map(lambda c: m.get(c, c)), "pnl": old.gross_pnl_usd,
                      "cap": old.capital_usd.astype(float)})
    b = pd.DataFrame({"date": pd.to_datetime(new.trade_date, format="%m/%d/%Y"), "pod": new.book_id, "pnl": new.pnl_usd_000 * 1000.0,
                      "cap": new.alloc_capital_usd_mm * 1e6})
    rec = pd.concat([a, b], ignore_index=True)
    reg = pd.read_csv(t(find("pod_register")), dtype=str)
    return rec, reg


def fred(name):
    d = pd.read_csv(t(name + ".csv"))
    d.columns = ["date", "v"]
    return pd.Series(pd.to_numeric(d.v, errors="coerce").values, index=pd.to_datetime(d.date))


def cboe(name):
    d = pd.read_csv(t(name + "_History.csv"))
    d.columns = [c.upper() for c in d.columns]
    col = "CLOSE" if "CLOSE" in d.columns else d.columns[-1]
    return pd.Series(d[col].astype(float).values, index=pd.to_datetime(d["DATE"], format="%m/%d/%Y"))


def holdings():
    """What a passive holding of each market earned each S&P 500 trading day, carry included."""
    spx = cboe("SPX")
    days = spx.loc["2016-12-30":LAST].index

    def on(s):
        return s.reindex(s.index.union(days)).ffill().reindex(days)
    y10, y2, bill, baa = on(fred("DGS10")), on(fred("DGS2")), on(fred("DTB3")), on(fred("DBAA"))
    dt_ = pd.Series(np.r_[np.nan, (days[1:] - days[:-1]).days], index=days) / 365.0
    H = pd.DataFrame(index=days)
    H["MKT"] = spx.reindex(days).pct_change()
    H["TECH"] = on(fred("NASDAQ100")).pct_change() - H["MKT"]
    H["RATES"] = -8 * y10.diff() / 100 + (y10 - bill).shift(1) / 100 * dt_
    H["CURVE"] = 4 * (y10 - y2).diff() / 100
    H["CREDIT"] = -6 * (baa - y10).diff() / 100 + (baa - y10).shift(1) / 100 * dt_
    H["USD"] = on(fred("DTWEXBGS")).pct_change()
    H["OIL"] = on(fred("DCOILBRENTEU")).pct_change()
    H["VOL"] = -on(cboe("VIX")).diff() / 100
    # the G10 basket: long the three highest 3-month rates of the month before, short the three lowest
    fx = {"AUD": ("DEXUSAL", 0, "IR3TIB01AUM156N"), "NZD": ("DEXUSNZ", 0, "IR3TIB01NZM156N"), "GBP": ("DEXUSUK", 0, "IR3TIB01GBM156N"),
          "EUR": ("DEXUSEU", 0, "IR3TIB01EZM156N"), "JPY": ("DEXJPUS", 1, "IR3TIB01JPM156N"), "CHF": ("DEXSZUS", 1, "IR3TIB01CHM156N"),
          "CAD": ("DEXCAUS", 1, "IR3TIB01CAM156N"), "NOK": ("DEXNOUS", 1, "IR3TIB01NOM156N"), "SEK": ("DEXSDUS", 1, "IR3TIB01SEM156N")}
    back = {"GBP": "IRSTCI01GBM156N", "EUR": "IR3TIB01DEM156N"}
    spot, rate = {}, {}
    for c, (s, inv, r) in fx.items():
        x = fred(s)
        spot[c] = on(1 / x if inv else x)
        rr = fred(r)
        rr.index = rr.index.to_period("M")
        if c in back:
            b2 = fred(back[c])
            b2.index = b2.index.to_period("M")
            rr = rr.combine_first(b2)
        rate[c] = rr
    spot, rate = pd.DataFrame(spot), pd.DataFrame(rate).sort_index().ffill()
    ret = spot.pct_change()
    mon = days.to_period("M")
    basket = pd.Series(0.0, index=days)
    for mth in sorted(set(mon)):
        if mth - 1 not in rate.index:
            continue
        r0 = rate.loc[mth - 1].dropna().sort_values()
        lo, hi = list(r0.index[:3]), list(r0.index[-3:])
        idx = mon == mth
        g = dt_[idx].values[:, None]
        basket[idx] = ((ret.loc[idx, hi] + r0[hi].values / 100 * g).mean(axis=1) - (ret.loc[idx, lo] + r0[lo].values / 100 * g).mean(axis=1)).values
    H["FXCARRY"] = basket
    return H.iloc[1:].fillna(0.0)


def main():
    rec, reg = record()
    group = dict(zip(reg.pod, reg.strategy_group))
    ok("every code in the record is in the register once the 2022 map is applied", set(rec.pod) <= set(reg.pod), len(set(rec.pod) - set(reg.pod)))
    H = holdings()
    days = pd.DatetimeIndex(sorted(rec.date.unique()))
    pos = np.searchsorted(days, H.index[(H.index >= days[0]) & (H.index <= days[-1])])
    Hd = H.loc[(H.index >= days[0]) & (H.index <= days[-1])].groupby(days[pos]).sum()
    # ---- R1
    res = {}
    for pod, d in rec.groupby("pod"):
        if len(d) < 60:
            continue
        d = d.set_index("date").sort_index()
        r = d.pnl / d.cap
        X = np.column_stack([np.ones(len(r)), Hd.loc[r.index].values])
        b = np.linalg.lstsq(X, r.values, rcond=None)[0]
        e = r.values - Hd.loc[r.index].values @ b[1:]
        res[pod] = (pd.Series(e, index=r.index), d.cap, float(np.std(r.values - X @ b) * np.sqrt(252)), b[1:])
    for g in GROUPS:
        num = sum(float((e * k).sum()) for p, (e, k, _, _) in res.items() if group[p] == g)
        den = sum(float(k.sum()) / 252 for p, (e, k, _, _) in res.items() if group[p] == g)
        v = num / den * 100
        ok("R1 %s alpha a year inside its band" % g, F["R1_bands"][g][0] <= v <= F["R1_bands"][g][1], "%.2f%% against %s" % (v, F["R1_bands"][g]))
    # ---- R3
    rows = []
    for p, (e, k, _, _) in res.items():
        for y in sorted(set(e.index.year)):
            mm = e.index.year == y
            if mm.sum() >= 120:
                rows.append((p, float(e[mm].mean() * 252), float(k[mm].mean())))
    D = pd.DataFrame(rows, columns=["p", "a", "k"])
    best = None
    for th in np.arange(0.0, 1.0001, 0.005):
        x = (D.k.values / 150e6) ** (-th)
        num = pd.Series(D.a.values * x).groupby(D.p.values).transform("sum").values
        den = pd.Series(x * x).groupby(D.p.values).transform("sum").values
        sse = float(((D.a.values - num / den * x) ** 2).sum())
        if best is None or sse < best[1]:
            best = (th, sse)
    fall = (1 - 2 ** (-best[0])) * 100
    ok("R3 fall per doubling within pods inside its band", F["R3_band"][0] <= fall <= F["R3_band"][1], "%.1f%% against %s" % (fall, F["R3_band"]))
    # ---- the draft, read from the workbook
    ws = load_workbook(t(find("draft_allocation_plan_2027")), data_only=True)["Draft 2027"]
    draft = {r[0]: (float(r[2]) * 1e6, float(r[3]) * 1e6, r[4]) for r in ws.iter_rows(min_row=4, values_only=True) if r[0] and r[0] != "Total"}
    inc = sorted(p for p, v in draft.items() if v[2] == "Increase")
    ok("the draft's increases are the figures' increases", inc == sorted(x["pod"] for x in F["increases"]), len(inc))
    # ---- R4 and R6 on a smaller simulation of my own
    th = best[0]
    first = dict(zip(reg.pod, pd.to_datetime(reg.first_trading_day)))
    edge, se = {}, {}
    for p, (e, k, sd, _) in res.items():
        x = (k.values / 150e6) ** (-th)
        bb = float((e.values * x).sum() / (x * x).sum())
        edge[p] = bb * 252
        se[p] = float(np.std(e.values - bb * x) * np.sqrt(252)) / np.sqrt((x * x).sum() / 252)
    prior = {}
    for g in GROUPS:
        ps = [p for p in res if group[p] == g and len(res[p][0]) >= 120]
        a = np.array([edge[p] for p in ps])
        v = np.array([se[p] ** 2 for p in ps])
        tau2 = max(0.0, a.var(ddof=1) - v.mean())
        for _ in range(500):
            w = 1 / (tau2 + v)
            mu = float((w * a).sum() / w.sum())
            tn = max(0.0, float((w * ((a - mu) ** 2 - v)).sum() / w.sum()))
            if abs(tn - tau2) < 1e-14:
                break
            tau2 = tn
        prior[g] = (mu, tau2)
    exp = {}
    for p in draft:
        g = group[p]
        if p in res and len(res[p][0]) >= 60:
            exp[p] = prior[g][0] + prior[g][1] / (prior[g][1] + se[p] ** 2) * (edge[p] - prior[g][0])
        else:
            exp[p] = prior[g][0]
    yr = [d for d in pd.bdate_range("2027-01-01", "2027-12-31") if d.strftime("%m-%d") not in
          ("01-01", "01-18", "02-15", "03-26", "05-31", "06-18", "07-05", "09-06", "11-25", "12-24")]
    Hn = len(yr)
    gap = np.diff(np.r_[pd.Timestamp("2026-12-31").value, [d.value for d in yr]]) / 86400e9 / 365.0
    Hm = (Hd - Hd.mean()).values
    rng = np.random.default_rng(7)
    S = 6000
    starts = rng.integers(0, len(Hm), size=(S, int(np.ceil(Hn / 63))))
    idx = ((starts[:, :, None] + np.arange(63)[None, None, :]) % len(Hm)).reshape(S, -1)[:, :Hn]
    paths = Hm[idx]
    bill = float(fred("DTB3").dropna().loc[:LAST].iloc[-1]) / 100
    lead = len([d for d in pd.bdate_range("2026-11-09", "2026-12-31") if d.strftime("%m-%d") not in ("11-26", "12-25")])
    tday = H.index[(H.index >= "2017-01-03")]

    def year(p, K, seed):
        g = group[p]
        if p in res and len(res[p][0]) >= 60:
            beta, idio = res[p][3], res[p][2]
        else:
            peers = [q for q in res if group[q] == g and len(res[q][0]) >= 120]
            beta, idio = np.mean([res[q][3] for q in peers], axis=0), float(np.mean([res[q][2] for q in peers]))
        r = paths @ beta + np.random.default_rng(seed).standard_normal((S, Hn)) * idio / np.sqrt(252) + exp[p] * (K / 150e6) ** (-th) * gap
        cum, peak, cut, alive = np.zeros(S), np.zeros(S), np.ones(S), np.ones(S)
        tot, capd = np.zeros(S), np.zeros(S)
        for i in range(Hn):
            x = K[i] * cut * alive * r[:, i]
            tot += x
            cum += x
            peak = np.maximum(peak, cum)
            dd = (peak - cum) / K[i]
            alive = np.where(dd >= 0.075, 0.0, alive)
            cut = np.where((dd >= 0.05) & (alive > 0), 0.5, cut)
            capd += K[i] * cut * alive * gap[i]
        after = tot - 0.2 * (bill + 0.0035) * capd
        return after - 0.18 * np.maximum(after, 0)

    total = np.zeros(S)
    for k, (p, (k26, k27, chg)) in enumerate(sorted(draft.items())):
        if chg == "Onboarding":
            age = int(np.searchsorted(tday, LAST, side="right")) - int(np.searchsorted(tday, first[p])) + lead + np.arange(Hn)
            K = k27 * np.where(age >= 252, 1.0, np.where(age >= 126, 0.5, 0.25))
        else:
            K = np.full(Hn, k27)
        total += year(p, K, 100 + k)
    mean = float(total.mean() - 218.4e6) / 1e6
    ok("R4 expected 2027 net P&L on my own simulation inside its band", F["R4_band"][0] <= mean <= F["R4_band"][1], "%.1f against %s" % (mean, F["R4_band"]))
    flag = []
    for k, p in enumerate(inc):
        k26, k27, _ = draft[p]
        a = year(p, np.full(Hn, k26), 500 + k).mean()
        b = year(p, np.full(Hn, k27), 500 + k).mean()
        if (b - a) / (k27 - k26) < 0.015:
            flag.append(p)
    core, either = set(F["R6_fail"]), set(F["R6_either"])
    ok("R6 my increases below the hurdle hold every failing one and no clear pass", core <= set(flag) <= core | either, "%s against %s (+ %s)" % (
        flag, sorted(core), sorted(either)))
    # ---- the documents say what the blocks rely on
    pol = " ".join(subprocess.run(["pdftotext", "-layout", t(find("Capital_Review_Policy")), "-"], capture_output=True, text=True).stdout.split())
    ok("the policy states the hurdle, the payout, the drawdown rules and the planning conventions",
       all(s in pol for s in ("1.5 per cent", "18 per cent", "5 per cent", "7.5 per cent", "markets themselves to earn nothing", "10th to the 90th percentile")))
    print("verify: %d of %d PASS" % (sum(ROWS), len(ROWS)))
    return 0 if all(ROWS) else 1


if __name__ == "__main__":
    sys.exit(main())
