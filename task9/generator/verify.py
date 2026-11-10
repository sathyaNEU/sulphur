"""task9: the independent verifier. It reads only the shipped pack under target/ (every format the pack ships: CSV,
XLSX, PDF) and recomputes every graded figure on its own code path, importing nothing from the generator. The figures
it compares against are the ones the answer blocks state (generator/figures.json).

    python3 task9/generator/verify.py        (exit 1 on any FAIL)
"""
import datetime as dt
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
REVIEW = pd.Timestamp("2026-11-09")
START = pd.Timestamp("2007-01-01")
TERM = {"VIX9D": 9, "VIX": 30, "VIX3M": 93, "VIX6M": 184, "VIX1Y": 365}
OWN = {3: "VIX3M", 6: "VIX6M", 12: "VIX1Y"}
CAP, OLD, PER, YEAR = 2.5, 50000.0, 100000.0, 2027
ROWS = []


def ok(label, cond, detail=""):
    ROWS.append(bool(cond))
    print("%s  %-84s %s" % ("PASS" if cond else "FAIL", label, str(detail)[:140]))


def close(a, b, tol):
    return abs(a - b) <= tol


def k(x):
    return int(round(x / 1000.0) * 1000)


def text(name):
    out = subprocess.run(["pdftotext", "-layout", os.path.join(TGT, name), "-"], capture_output=True, text=True).stdout
    return " ".join(out.split())


def series(name):
    d = pd.read_csv(os.path.join(TGT, name + "_History.csv"))
    d.columns = [c.strip().upper() for c in d.columns]
    col = "CLOSE" if "CLOSE" in d.columns else d.columns[-1]
    s = pd.Series(d[col].astype(float).values, index=pd.to_datetime(d["DATE"], format="%m/%d/%Y"))
    return s[s.index <= REVIEW]


# ---------------------------------------------------------------------------------------------- the record and calendar
spx = series("SPX")
days = spx.index
vix = pd.DataFrame({n: series(n) for n in TERM}).reindex(days)
r2 = np.log(spx / spx.shift(1)).fillna(0.0) ** 2
cum = r2.cumsum().values
hol = pd.read_csv(os.path.join(TGT, "NYSE_Holidays_2026_2028.csv"))
closed = set(pd.to_datetime(hol[hol["Market status"] == "Closed"]["Date"]))
future = [d for d in pd.bdate_range(REVIEW + pd.Timedelta(days=1), "2028-02-29") if d not in closed]
sched = days.append(pd.DatetimeIndex(future))
pos = {d: i for i, d in enumerate(sched)}
i_rev, i_0 = pos[REVIEW], int(days.searchsorted(START))


def third_friday(y, m):
    d = dt.date(y, m, 15)
    while d.weekday() != 4:
        d += dt.timedelta(days=1)
    return pd.Timestamp(d)


def sale_date(y, m):
    return sched[sched.searchsorted(third_friday(y, m), side="right")]


def expiry(y, m):
    return sched[sched.searchsorted(third_friday(y, m), side="right") - 1]


def pay(strike, rv):
    rv = np.minimum(rv, CAP * strike)
    return (strike * strike - rv * rv) / (2.0 * strike)


def rvol(a, b):
    return float(np.sqrt(1e4 * 252.0 * (cum[pos[b]] - cum[pos[a]]) / (pos[b] - pos[a])))


# implied volatility for every record day and every remaining term in calendar days, read in total variance between
# the maturities published that day
GRID = np.arange(401, dtype=float)
CURVE = np.full((len(days), 401), np.nan)
T_ALL = np.array([TERM[c] for c in vix.columns], dtype=float)
V_ALL = vix.values
for i in range(i_0, len(days)):
    have = ~np.isnan(V_ALL[i])
    t, v = T_ALL[have], V_ALL[i][have]
    g = np.clip(GRID, t[0], t[-1])
    CURVE[i] = np.sqrt(np.interp(g, t, v * v * t) / g)


def fit(target, lo, hi):
    j = vix[[target, lo, hi]].dropna()
    X = np.column_stack([np.ones(len(j)), j[lo].values, j[hi].values])
    return np.linalg.lstsq(X, j[target].values, rcond=None)[0], j, X


FITS = {}


def strike(mat, d):
    """The maturity's index on the day, or its level rebuilt from the published maturities on both sides."""
    own = OWN[mat]
    v = vix.at[d, own]
    if not np.isnan(v):
        return float(v), False
    row = vix.loc[d]
    lo = max((c for c in TERM if TERM[c] < TERM[own] and TERM[c] >= 30 and not np.isnan(row[c])), key=lambda c: TERM[c])
    hi = min((c for c in TERM if TERM[c] > TERM[own] and not np.isnan(row[c])), key=lambda c: TERM[c])
    if (own, lo, hi) not in FITS:
        FITS[(own, lo, hi)] = fit(own, lo, hi)[0]
    b = FITS[(own, lo, hi)]
    return float(b[0] + b[1] * row[lo] + b[2] * row[hi]), True


def ladder(mat):
    rows = []
    y, m = 2007, 1
    while True:
        s = sale_date(y, m)
        if s > REVIEW:
            break
        j = (m - 1) + mat
        e = expiry(y + j // 12, j % 12 + 1)
        kk, rebuilt = strike(mat, s)
        done = e <= REVIEW
        rows.append(dict(sale=s, expiry=e, k=kk, rebuilt=rebuilt, pay=pay(kk, rvol(s, e)) if done else np.nan))
        y, m = (y + 1, 1) if m == 12 else (y, m + 1)
    return pd.DataFrame(rows)


def marks(L):
    """The ladder's open swaps valued together on every record day, per unit of vega."""
    out = np.zeros(len(days))
    dnum = days.values.astype("datetime64[D]").astype(int)
    for s in L.itertuples():
        a, b = pos[s.sale], pos[s.expiry]
        j = np.arange(a + 1, min(b, len(days)))
        if not len(j):
            continue
        ne, nr = (j - a).astype(float), (b - j).astype(float)
        cal = np.clip(int(np.datetime64(s.expiry, "D").astype(int)) - dnum[j], 0, 400)
        iv = CURVE[j, cal]
        w = np.minimum((1e4 * 252.0 * (cum[j] - cum[a]) + nr * iv * iv) / (ne + nr), (CAP * s.k) ** 2)
        out[j] += (s.k * s.k - w) / (2.0 * s.k)
    return pd.Series(out, index=days)


def room(Ln, mn, yo, mo, ls, lc):
    done = Ln.dropna(subset=["pay"])
    yn = done.groupby(done.expiry.dt.year).pay.sum()
    best, why = np.inf, None
    for y in yn.index:
        if yn[y] < 0:
            r = (ls + float(yo.get(y, 0.0)) * OLD) / -yn[y]
            if r < best:
                best, why = r, ("settlement", str(y))
    neg = mn < 0
    r = (lc + mo[neg] * OLD) / -mn[neg]
    if float(r.min()) < best:
        best, why = float(r.min()), ("collateral", str(r.idxmin().date()))
    return best, int(np.floor(best / 100.0 + 1e-9) * 100), why


def block_range(x, block, seed):
    n = len(x)
    nb = int(np.ceil(n / float(block)))
    st = np.random.default_rng(seed).integers(0, n, size=(20000, nb))
    idx = ((st[:, :, None] + np.arange(block)[None, None, :]) % n).reshape(20000, nb * block)[:, :n]
    m = x[idx].mean(axis=1) * PER
    return float(np.percentile(m, 10)), float(np.percentile(m, 90))


def main():
    # ------------------------------------------------------------------ the documents (PDF) and what they file
    pol = text("IPS_Schedule_D_Volatility_Premium_Sleeve.pdf")
    conf = text("Master_Confirmation_SPX_Variance_Swap.pdf")
    csa = text("CSA_Summary_Volatility_Sleeve.pdf")
    terms = text("Indicative_Terms_3M_6M_Variance_Swaps_2027.pdf")
    assets = text("CFF_Statement_of_Net_Assets_FY2026.pdf")
    ok("PDF read back: the policy names its schedule (positive control)", "Schedule D: Volatility Premium Sleeve" in pol)
    ok("policy: both limits and Reference Assets", "shall not exceed 2.0 percent of Reference Assets" in pol and "shall not exceed 3.0 percent of Reference Assets" in pol
       and "audited net assets at the most recent fiscal year end" in pol)
    ok("policy: the record from January 2007, every ladder on every sale date, published index or not", "from January 2007 through the review date" in pol and
       "every ladder of the Sleeve been sold at its size on every monthly sale date of the record" in pol and
       "whether or not the volatility index for that ladder's maturity was yet being published" in pol)
    ok("policy: collateral is the open swaps valued together, no discounting", "open swaps taken together are valued against the Sleeve" in pol and "No discounting is applied" in pol)
    ok("policy: the cash plan's basis and its two ranges", "expected to pay, as estimated at the review date" in pol and "average settlement amount per sale their ladder shows on the record" in pol
       and "the whole record and not of the Sleeve's own years alone" in pol and "the average itself, as distinct from a single settlement" in pol and
       "the year's settlements, receipts net of payments" in pol)
    ok("policy: sizes in multiples of USD 100, the cap at 2.5 times the strike", "multiples of USD 100 a point" in pol and "capped at 2.5 times the strike" in pol)
    ok("confirmation: realized volatility, observation days, the cap and the settlement amount", "252 divided by N" in conf and "publishes an official closing level" in conf and
       "2.5 multiplied by the Volatility Strike" in conf and "Variance Units multiplied by" in conf)
    ok("annex summary: exposure is capped at the capped settlement", "were Final Realized Volatility equal to the Volatility Cap" in csa)
    ok("term sheet: the size quoted for and the 12-month ladder continuing", "Quoted for up to USD 200,000" in terms and "continues on its present terms" in terms)
    ok("net assets: USD 1,487.6 million at June 30, 2026", "1,487.6" in assets and "June 30, 2026" in assets)
    ref = 1487.6e6
    ls, lc = 0.02 * ref, 0.03 * ref
    ok("the limits in dollars", k(ls) == F["policy"]["settlement_limit_usd"] and k(lc) == F["policy"]["collateral_limit_usd"], "%.0f and %.0f" % (ls, lc))

    # ------------------------------------------------------------------ the blotter (XLSX) and the settlements (CSV)
    ws = load_workbook(os.path.join(TGT, "CFF_VolPremium_Blotter.xlsx"), read_only=True)["Tickets"]
    rows = list(ws.values)
    blot = pd.DataFrame(rows[1:], columns=[str(c) for c in rows[0]])
    ok("XLSX read back: the blotter's header (positive control)", list(blot.columns[:4]) == ["Order No", "Status", "Trade Date", "Expiration Date"], len(blot))
    live = blot[blot["Status"] == "LIVE"]
    good = blot[blot["Status"].isin(["LIVE", "SETTLED"])]
    ok("blotter: 128 confirmations, 24 open in twelve sale months at 50,000 a month", len(good) == F["confirmations"]["total"] and len(live) == F["open_confirmations"]
       and live.groupby("Trade Date")["Vega Notional (USD/pt)"].sum().eq(OLD).all() and live["Trade Date"].nunique() == 12)
    ok("blotter: every trade date and expiration follows the program's calendar", all(sale_date(d.year, d.month) == pd.Timestamp(d) for d in good["Trade Date"]) and
       all(expiry(d.year + 1, d.month) == pd.Timestamp(e) for d, e in zip(good["Trade Date"], good["Expiration Date"])))
    ok("blotter: every strike is the 1-year index close of its trade date", max(abs(float(s) - vix.at[pd.Timestamp(d), "VIX1Y"]) for d, s in zip(good["Trade Date"], good["Volatility Strike"])) < 1e-9)
    setl = pd.read_csv(os.path.join(TGT, "CFF_VolPremium_Settlements.csv"))
    rv = np.array([rvol(pd.Timestamp(a), pd.Timestamp(b)) for a, b in zip(setl.trade_date, setl.expiration_date)])
    ok("CSV read back: 104 settlements reproduce from the closes by the confirmation's formula", len(setl) == F["confirmations"]["settled"] and
       float(np.abs(rv - setl.realized_volatility).max()) < 6e-5 and float(np.abs(setl.vega_notional_usd * pay(setl.volatility_strike.values, rv) - setl.settlement_amount_usd).max()) < 500)
    val = pd.read_csv(os.path.join(TGT, "Larkhill_DealerValuations_Daily.csv"), dtype=str)
    one = val[(val.dealer == "BSS")].iloc[-1]
    kk, ne, nt = float(one.strike), float(one.days_elapsed), float(one.days_total)
    calc = float(one.notional) * (kk * kk - min((ne * float(one.realized_to_date) ** 2 + (nt - ne) * float(one.implied_to_expiration) ** 2) / nt, (CAP * kk) ** 2)) / (2 * kk)
    ok("valuation file: a dealer's value is realized-to-date and implied-to-expiry variance weighted by days", len(val) > 20000 and abs(calc - float(one.value_usd)) <= 1.0,
       "%s rows; %.0f against %s" % (len(val), calc, one.value_usd))

    # ------------------------------------------------------------------ the ladders on the record
    L3, L6, L12 = ladder(3), ladder(6), ladder(12)
    d3, d12 = L3.dropna(subset=["pay"]), L12.dropna(subset=["pay"])
    y3 = d3.groupby(d3.expiry.dt.year).pay.sum()
    ok("R1 the 3-month ladder's average settlement per sale", k(d3.pay.mean() * PER) == F["R1_avg_3m_usd"] and len(d3) == F["ladder_counts"]["settled"] and
       int(L3.rebuilt.sum()) == F["ladder_counts"]["rebuilt"], "%.0f over %d swaps, %d strikes rebuilt" % (d3.pay.mean() * PER, len(d3), L3.rebuilt.sum()))
    ok("R2 its worst calendar year", int(y3.idxmin()) == F["R2_worst_year"] and k(-y3.min() * PER) == F["R2_worst_year_loss_usd"], "%d, %.0f" % (y3.idxmin(), -y3.min() * PER))
    b, j, X = fit("VIX3M", "VIX", "VIX6M")
    res = j.VIX3M.values - X @ b
    hot = j.VIX.values > 35
    ok("the rebuild's fit on the days all three are published", len(j) == F["rebuild"]["overlap_days"] and round(float(np.sqrt((res ** 2).mean())), 2) == F["rebuild"]["rmse"]
       and int(hot.sum()) == F["rebuild"]["hot_days"] and round(float(np.sqrt((res[hot] ** 2).mean())), 2) == F["rebuild"]["rmse_hot"])
    o = vix[["VIX", "VIX3M"]].dropna()
    b1 = np.linalg.lstsq(np.column_stack([np.ones(len(o)), o.VIX.values]), o.VIX3M.values, rcond=None)[0]
    e1 = b1[0] + b1[1] * o.VIX.values - o.VIX3M.values
    ok("the 30-day index alone: a high R-squared and too high on the stressed days", round(1 - (e1 ** 2).sum() / ((o.VIX3M - o.VIX3M.mean()) ** 2).sum(), 2) == F["rebuild"]["proxy_r2"]
       and round(float(e1[o.VIX.values > 35].mean()), 1) == F["rebuild"]["proxy_bias_hot"])
    m3, m6, m12 = marks(L3), marks(L6), marks(L12)
    ok("R3 the 12-month ladder's peak collateral", close(-m12.min() * OLD, F["R3_old_peak_usd"], 600) and str(m12.idxmin().date()) == F["R3_old_peak_day"], "%.0f on %s" % (-m12.min() * OLD, m12.idxmin().date()))
    y12 = d12.groupby(d12.expiry.dt.year).pay.sum()
    raw3, size3, why3 = room(L3, m3, y12, m12, ls, lc)
    raw6, size6, why6 = room(L6, m6, y12, m12, ls, lc)
    ok("R4 the largest 3-month size, its limit and day", size3 == F["R4_size_usd"] and why3 == (F["R4_binds"]["limit"], F["R4_binds"]["day"]), "%.1f -> %d, %s" % (raw3, size3, why3))
    ok("R5 the largest 6-month size, its limit and day", size6 == F["R5_alt_size_usd"] and why6 == (F["R5_binds"]["limit"], F["R5_binds"]["day"]), "%.1f -> %d, %s" % (raw6, size6, why6))
    sleeve = m12 * OLD + m3 * size3
    ok("at the size the sleeve's collateral peaks under the limit, and 100 more breaches", -sleeve.min() <= lc < -(m12 * OLD + m3 * (size3 + 100)).min() and
       k(-sleeve.min()) == F["at_size"]["peak_usd"])
    ok("the size quoted for breaches", k(-(m12 * OLD + m3 * 200000.0).min()) == F["quoted"]["peak_usd"])
    daily = pd.read_csv(os.path.join(TASK, "golden", "sleeve_collateral_on_record.csv"))
    rec = sleeve[sleeve.index >= START]
    ok("the golden daily file is that sleeve, day by day", len(daily) == len(rec) == F["daily"]["rows"] and
       float(np.abs(daily.collateral_usd.values - np.maximum(0.0, -rec.values)).max()) <= 501)

    # ------------------------------------------------------------------ how well the record pins each average
    for mat, d_, key, bands, seed in ((12, d12, "R6_avg_range_12m", "R6_bands", 4242), (3, d3, "R7_avg_range_3m", "R7_bands", 4243)):
        lo, hi = block_range(d_.pay.values, 2 * mat, seed)
        b_ = F[bands]
        ok("%s the %d-month average's range, resampled in blocks on another seed" % (key[:2], mat), b_["low_usd"][0] <= lo <= b_["low_usd"][1] and
           b_["high_usd"][0] <= hi <= b_["high_usd"][1] and close(lo, F[key]["low_usd"], 12000) and close(hi, F[key]["high_usd"], 12000), "%.0f to %.0f" % (lo, hi))
        x = d_.pay.values
        e = x - x.mean()
        ok("   neighbouring sales are tied (%d-month)" % mat, round(float((e[1:] * e[:-1]).sum() / (e * e).sum()), 2) == F["avg_%dm" % mat]["next_sale_correlation"])
    ok("the 12-month ladder's average per sale", k(d12.pay.mean() * PER) == F["avg_12m"]["avg_per_sale_usd"] and len(d12) == F["avg_12m"]["n"])

    # ------------------------------------------------------------------ the open swaps that expire in the plan year
    ob = live.groupby("Trade Date").agg(expiry=("Expiration Date", "first"), k=("Volatility Strike", "first")).reset_index()
    ob["sale"], ob["expiry"] = pd.to_datetime(ob["Trade Date"]), pd.to_datetime(ob["expiry"])
    ob = ob[ob.expiry.dt.year == YEAR].reset_index(drop=True)
    ne = np.array([pos[REVIEW] - pos[s] for s in ob.sale], dtype=float)
    nr = np.array([pos[e] - pos[REVIEW] for e in ob.expiry])
    acc = np.array([rvol(s, REVIEW) ** 2 for s in ob.sale])
    cal = np.array([(e - REVIEW).days for e in ob.expiry])
    iv2 = CURVE[i_rev, cal] ** 2
    kk = ob.k.values.astype(float)

    def settle(rem):
        w = np.minimum((ne * acc + nr * rem) / (ne + nr), (CAP * kk) ** 2)
        return (kk * kk - w) / (2 * kk)

    starts = np.arange(i_0, i_rev - int(nr.max()) + 1)
    rem = np.column_stack([1e4 * 252.0 * (cum[starts + n_] - cum[starts]) / n_ / CURVE[starts, c] ** 2 * v for n_, c, v in zip(nr, cal, iv2)])
    tot = settle(rem).sum(axis=1) * OLD
    mark = float(settle(iv2).sum() * OLD)
    ok("R8 the open swaps' expected settlement, against their value", len(ob) == 10 and close(tot.mean(), F["R8_expected_usd"], 600) and close(mark, F["replay"]["mark_usd"], 600)
       and len(starts) == F["replay"]["start_dates"], "%.0f expected, %.0f value, %d start dates" % (tot.mean(), mark, len(starts)))
    ok("R9 their 80 per cent range", close(np.percentile(tot, 10), F["R9_range"]["low_usd"], 600) and close(np.percentile(tot, 90), F["R9_range"]["high_usd"], 600),
       "%.0f to %.0f" % (np.percentile(tot, 10), np.percentile(tot, 90)))
    ok("   the value sits below the outcome from four start dates in five", int(round(100 * (tot > mark).mean())) == F["replay"]["share_above_mark_pct"])

    # ------------------------------------------------------------------ the plan year
    legs = []
    for m in range(1, 13):
        s = sale_date(YEAR - 1, m)
        if s > REVIEW:
            legs.append((12, s, expiry(YEAR, m)))
    for m in range(1, 13):
        j_ = (m - 1) + 3
        e = expiry(YEAR + j_ // 12, j_ % 12 + 1)
        if e.year == YEAR:
            legs.append((3, sale_date(YEAR, m), e))
    n12, n3 = sum(g[0] == 12 for g in legs), sum(g[0] == 3 for g in legs)
    a3, a12 = float(d3.pay.mean()), float(d12.pay.mean())
    twelve = k(tot.mean()) + k(n12 * a12 * OLD)
    three = k(n3 * size3 * a3)
    ok("R10 the plan by ladder", (n12, n3) == (2, 9) and close(twelve, F["R10_plan"]["twelve_month_usd"], 1000) and close(three, F["R10_plan"]["three_month_usd"], 1000)
       and close(twelve + three, F["R10_plan"]["total_usd"], 1500), "12-month %d, 3-month %d, sleeve %d" % (twelve, three, twelve + three))
    def level(d_):                      # a day with no longer maturity published carries the day before
        try:
            return strike(3, d_)[0]
        except ValueError:
            return np.nan

    s3 = pd.Series([level(d_) if d_ >= START else np.nan for d_ in days], index=days).ffill().values
    s12 = vix.VIX1Y.ffill().values
    so = [pos[g[1]] - i_rev for g in legs]
    eo = [pos[g[2]] - i_rev for g in legs]
    ps = np.arange(i_0, i_rev - max(eo) + 1)
    total = tot[:len(ps)].copy()
    for (mat, _, _), a_, b_ in zip(legs, so, eo):
        kx = (s12 if mat == 12 else s3)[ps + a_]
        total += pay(kx, np.sqrt(1e4 * 252.0 * (cum[ps + b_] - cum[ps + a_]) / (b_ - a_))) * (OLD if mat == 12 else size3)
    lo, hi = float(np.percentile(total, 10)), float(np.percentile(total, 90))
    ok("R10 the plan's range over every settlement together", close(lo, F["R10_plan"]["low_usd"], 2000) and close(hi, F["R10_plan"]["high_usd"], 2000) and
       len(ps) == F["plan"]["start_dates"], "%.0f to %.0f from %d start dates" % (lo, hi, len(ps)))
    ok("R11 the recommendation is the size and that plan", F["R11_call"] == dict(size_usd=size3, plan_usd=F["R10_plan"]["total_usd"], low_usd=F["R10_plan"]["low_usd"],
                                                                                 high_usd=F["R10_plan"]["high_usd"]))
    fails = ROWS.count(False)
    print("%s  task9 verify: %d assertions, %d FAIL" % ("PASS" if not fails else "FAIL", len(ROWS), fails))
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
