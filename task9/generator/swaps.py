"""task9: the variance swap as the confirmation writes it, a monthly ladder, its marks and its collateral.

All amounts are per unit of vega notional (one US dollar per volatility point) unless a size is passed.
"""
import numpy as np
import pandas as pd

import market as MK

CAP = 2.5            # realised volatility is capped at 2.5 times the strike (the confirmation's cap)
MATURITIES = (1, 3, 6, 12)


def pay(k, rv, cap=CAP):
    """Settlement to the seller per unit of vega: (K^2 - min(RV, cap K)^2) / (2K)."""
    rvc = np.minimum(rv, cap * k) if cap else rv
    return (k * k - rvc * rvc) / (2.0 * k)


def add_months(y, m, n):
    j = (m - 1) + n
    return y + j // 12, j % 12 + 1


class Ladder:
    """One swap of one maturity sold on every monthly sale date."""

    def __init__(self, mk, maturity, rebuild="calibrated", cap=CAP, start=MK.RECORD_START, last_sale=None, first_quoted=False):
        self.mk, self.maturity, self.cap, self.rebuild = mk, maturity, cap, rebuild
        rows = []
        y, m = start.year, start.month
        last_sale = last_sale or MK.CUT
        while True:
            sale = mk.sale_date(y, m)
            if sale > last_sale:
                break
            ey, em = add_months(y, m, maturity)
            exp = mk.expiry(ey, em)
            k, how = self.strike(sale) if sale <= MK.CUT else (np.nan, "future")
            rows.append(dict(sale=sale, expiry=exp, k=k, how=how))
            y, m = add_months(y, m, 1)
        self.t = pd.DataFrame(rows)
        self.t["n"] = [mk.count(a, b) for a, b in zip(self.t.sale, self.t.expiry)]
        done = self.t.expiry <= MK.CUT
        self.t["rv"] = [np.sqrt(mk.realised_var(a, b)) if d else np.nan for a, b, d in zip(self.t.sale, self.t.expiry, done)]
        self.t["pay"] = pay(self.t.k, self.t.rv, cap)

    # ---- strikes
    def strike(self, sale):
        mk, ix = self.mk, MK.MATURITY_INDEX[self.maturity]
        v = mk.idx.at[sale, ix]
        if not np.isnan(v):
            return float(v), "quoted"
        if self.rebuild == "none":
            return np.nan, "missing"
        return rebuilt_strike(mk, sale, self.maturity, self.rebuild), "rebuilt"

    # ---- results on the record
    def settled(self):
        return self.t.dropna(subset=["pay"])

    def by_year(self):
        d = self.settled()
        return d.groupby(d.expiry.dt.year).pay.sum()

    # ---- daily marks
    def marks(self, how="variance", remaining="term", cap_in_mark=True, points=None, extra=None, key=None, parts=False):
        """The ladder's net mark per unit of vega on every day of the record (the sum over its open swaps).

        remaining: 'term' marks the rest of each swap at the implied volatility for its remaining term; 'original'
        at the index level for its own maturity; 'vix' at the 30-day index.
        """
        mk = self.mk
        C = mk.curve(how, points, extra, key)
        days = mk.days
        cum = mk.cum.values
        total = np.zeros(len(days))
        nopen = np.zeros(len(days), dtype=int)
        acc_part = np.zeros(len(days))
        dnum = days.values.astype("datetime64[D]").astype(int)
        t_own = MK.TERM_DAYS[MK.MATURITY_INDEX[self.maturity]]
        for s in self.t.itertuples():
            if np.isnan(s.k) or s.sale > MK.CUT:
                continue
            i0, i1 = mk.pos(s.sale), mk.pos(s.expiry)
            j = np.arange(i0 + 1, min(i1, len(days)))          # days after the sale and before the expiry
            if not len(j):
                continue
            n_e = (j - i0).astype(float)
            n_r = (i1 - j).astype(float)
            acc = 1e4 * 252.0 * (cum[j] - cum[i0])              # the sum of squared returns so far, annualised later
            cal = np.clip(int(np.datetime64(s.expiry, "D").astype(int)) - dnum[j], 0, MK.TMAX)
            if remaining == "term":
                iv = C[j, cal]
            elif remaining == "original":
                iv = C[j, t_own]
            else:
                iv = C[j, 30]
            w = (acc + n_r * iv * iv) / (n_e + n_r)
            if cap_in_mark and self.cap:
                w = np.minimum(w, (self.cap * s.k) ** 2)
            total[j] += (s.k * s.k - w) / (2.0 * s.k)
            nopen[j] += 1
            if parts:
                wa = acc / (n_e + n_r)
                if cap_in_mark and self.cap:
                    wa = np.minimum(wa, (self.cap * s.k) ** 2)
                acc_part[j] += (s.k * s.k * n_e / (n_e + n_r) - wa) / (2.0 * s.k)
        out = pd.Series(total, index=days)
        if parts:
            return out, pd.Series(nopen, index=days), pd.Series(acc_part, index=days)
        return out, pd.Series(nopen, index=days)


def rebuilt_strike(mk, sale, maturity, how="calibrated"):
    """The strike a swap of this maturity would have been sold at on a date before its Cboe index was published."""
    t = MK.TERM_DAYS[MK.MATURITY_INDEX[maturity]]
    if how == "actual":               # the published close where the public record has one, total variance before it
        v = mk.actual3m().get(sale, np.nan) if maturity == 3 else np.nan
        return float(v) if not np.isnan(v) else mk.implied(sale, t, "variance")
    if how in ("variance", "vol"):
        return mk.implied(sale, t, how)
    if how == "calibrated-1y":        # the two maturities published through the whole gap: 30 days and one year
        b = calibration(mk, maturity, (30, 365))
        return float(np.array([1.0, mk.idx.at[sale, b["lo"]], mk.idx.at[sale, b["hi"]]]) @ b["coef"])
    b = calibration(mk, maturity, tuple(p[0] for p in mk.quoted(sale)))
    x = np.array([1.0, mk.idx.at[sale, b["lo"]], mk.idx.at[sale, b["hi"]]])
    if how == "calibrated-log":
        return float(np.exp(np.array([1.0, np.log(x[1]), np.log(x[2])]) @ b["coef_log"]))
    return float(x @ b["coef"])


def rebuilt_series(mk, maturity, how="calibrated"):
    """The maturity's index on every day of the record: published where it is, rebuilt where it is not."""
    ix = MK.MATURITY_INDEX[maturity]
    s = mk.idx[ix].copy()
    for d in s.index[s.isna() & (s.index >= MK.RECORD_START)]:
        try:
            s[d] = rebuilt_strike(mk, d, maturity, how)
        except Exception:
            pass
    return s


_CAL = {}


def calibration(mk, maturity, quoted_days):
    """Least squares of the maturity's index on its two neighbouring quoted maturities, over every day all three are
    published (the overlap), used to rebuild the index where it is missing."""
    key = (maturity, quoted_days)
    if key in _CAL:
        return _CAL[key]
    ix = MK.MATURITY_INDEX[maturity]
    t = MK.TERM_DAYS[ix]
    inv = {v: k for k, v in MK.TERM_DAYS.items()}
    lo = inv[max(d for d in quoted_days if d < t and d >= 30)]
    hi = inv[min(d for d in quoted_days if d > t)]
    j = mk.idx[[ix, lo, hi]].dropna()
    X = np.column_stack([np.ones(len(j)), j[lo].values, j[hi].values])
    coef, *_ = np.linalg.lstsq(X, j[ix].values, rcond=None)
    res = j[ix].values - X @ coef
    Xl = np.column_stack([np.ones(len(j)), np.log(j[lo].values), np.log(j[hi].values)])
    coef_log, *_ = np.linalg.lstsq(Xl, np.log(j[ix].values), rcond=None)
    hot = j[lo].values > 35
    _CAL[key] = dict(coef=coef, coef_log=coef_log, lo=lo, hi=hi, n=len(j), rmse=float(np.sqrt((res ** 2).mean())), bias=float(res.mean()),
                     n_hot=int(hot.sum()), rmse_hot=float(np.sqrt((res[hot] ** 2).mean())), bias_hot=float(res[hot].mean()))
    return _CAL[key]
