"""task9: the market record as pulled, and the calendar the swaps run on.

Every market value here is read from the raw Cboe downloads under raw/ (see raw/manifest.json); nothing is altered or
simulated. The calendar is the S&P 500's own publishing days to the cut-off, then weekdays less the exchange's
published holidays.
"""
import datetime as dt
import os

import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
CUT = pd.Timestamp("2026-11-09")            # the last close in the pull, and the review date
RECORD_START = pd.Timestamp("2007-01-01")   # the policy's record: sale dates from January 2007

# maturity of each Cboe volatility index in calendar days, as its methodology states it
TERM_DAYS = {"VIX9D": 9, "VIX": 30, "VIX3M": 93, "VIX6M": 184, "VIX1Y": 365}
MATURITY_INDEX = {1: "VIX", 3: "VIX3M", 6: "VIX6M", 12: "VIX1Y"}
TMAX = 400                                  # longest remaining term a swap can have, in calendar days

# New York Stock Exchange holidays after the cut-off, as the exchange publishes them
HOLIDAYS = [
    ("2026-11-26", "Thanksgiving Day"), ("2026-12-25", "Christmas Day"),
    ("2027-01-01", "New Year's Day"), ("2027-01-18", "Martin Luther King, Jr. Day"), ("2027-02-15", "Washington's Birthday"),
    ("2027-03-26", "Good Friday"), ("2027-05-31", "Memorial Day"), ("2027-06-18", "Juneteenth National Independence Day (observed)"),
    ("2027-07-05", "Independence Day (observed)"), ("2027-09-06", "Labor Day"), ("2027-11-25", "Thanksgiving Day"),
    ("2027-12-24", "Christmas Day (observed)"),
    ("2028-01-17", "Martin Luther King, Jr. Day"), ("2028-02-21", "Washington's Birthday"),
]


def _read(name):
    d = pd.read_csv(os.path.join(RAW, name + "_History.csv"))
    d.columns = [c.strip().upper() for c in d.columns]
    d["DATE"] = pd.to_datetime(d["DATE"], format="%m/%d/%Y")
    col = "CLOSE" if "CLOSE" in d.columns else d.columns[-1]
    s = d.set_index("DATE")[col].astype(float)
    return s[s.index <= CUT].rename(name)


class Market:
    def __init__(self):
        self.spx = _read("SPX")
        self.idx_all = pd.concat([_read(n) for n in TERM_DAYS], axis=1, sort=True)
        self.days = self.spx.index                      # every day the index published a close
        self.idx = self.idx_all.reindex(self.days)      # the volatility indices on the S&P 500's days
        self.lr2 = (np.log(self.spx / self.spx.shift(1)) ** 2).fillna(0.0)
        self.cum = self.lr2.cumsum()                    # running sum of squared log returns
        hol = {pd.Timestamp(d) for d, _ in HOLIDAYS}
        fut = pd.bdate_range(CUT + pd.Timedelta(days=1), "2028-02-29")
        self.future = pd.DatetimeIndex([d for d in fut if d not in hol])
        self.sched = self.days.append(self.future)      # the schedule: past publishing days, then scheduled days
        self._pos = {d: i for i, d in enumerate(self.sched)}
        self._curves = {}

    def actual3m(self):
        """The 3-month index's published closes before the Cboe download begins (FRED series VXVCLS, from 4 December
        2007), on the S&P 500's days. A cross-check held outside the pack: only rival runs and checks read it."""
        if "actual3m" not in self._curves:
            f = pd.read_csv(os.path.join(HERE, "raw_check", "VXVCLS.csv"), na_values=["."])
            f.columns = ["DATE", "VXV"]
            s = f.assign(DATE=pd.to_datetime(f.DATE)).set_index("DATE").VXV.astype(float)
            self._curves["actual3m"] = s.reindex(self.days)
        return self._curves["actual3m"]

    # ---- the calendar
    @staticmethod
    def third_friday(y, m):
        d = dt.date(y, m, 15)
        while d.weekday() != 4:
            d += dt.timedelta(days=1)
        return pd.Timestamp(d)

    def on_or_before(self, d):
        i = self.sched.searchsorted(d, side="right") - 1
        return self.sched[i]

    def after(self, d):
        i = self.sched.searchsorted(d, side="right")
        return self.sched[i]

    def expiry(self, y, m):
        """The third Friday of the month, or the scheduled day before it when the exchange is shut."""
        return self.on_or_before(self.third_friday(y, m))

    def sale_date(self, y, m):
        """The first scheduled day after the third Friday of the month."""
        return self.after(self.third_friday(y, m))

    def pos(self, d):
        return self._pos[d]

    def count(self, a, b):
        """Scheduled trading days after a up to and including b."""
        return self._pos[b] - self._pos[a]

    # ---- realised variance
    def realised_var(self, a, b):
        """Annualised realised variance in volatility points squared over the closes after a to b (both in the record)."""
        n = self.count(a, b)
        return 1e4 * 252.0 * (self.cum[b] - self.cum[a]) / n if n > 0 else np.nan

    # ---- the implied term structure
    def quoted(self, date, extra=None):
        row = self.idx.loc[date]
        pts = {TERM_DAYS[k]: float(row[k]) for k in TERM_DAYS if not np.isnan(row[k])}
        if extra is not None:
            for t, s in extra.items():
                if t not in pts and date in s.index and not np.isnan(s[date]):
                    pts[t] = float(s[date])
        return sorted(pts.items())

    def implied(self, date, cal_days, how="variance", points=None, extra=None):
        """Implied volatility for the next cal_days calendar days from the maturities quoted on the date.

        how: 'variance' interpolates total variance (variance times days) between the neighbouring quoted maturities,
        'vol' interpolates the volatility itself, 'nearest' takes the nearest quoted maturity; flat outside the quoted
        range. `points` restricts the maturities used; `extra` adds rebuilt maturities where none is quoted.
        """
        pts = [p for p in self.quoted(date, extra) if points is None or p[0] in points]
        return _interp(pts, cal_days, how)

    def curve(self, how="variance", points=None, extra=None, key=None):
        """Implied volatility for every day of the record (rows) and every remaining term 0..TMAX days (columns)."""
        k = (how, tuple(points) if points else None, key)
        if k in self._curves:
            return self._curves[k]
        cols = [c for c in TERM_DAYS if points is None or TERM_DAYS[c] in points]
        T = np.array([TERM_DAYS[c] for c in cols], dtype=float)
        V = self.idx[cols].values.copy()
        if extra is not None:
            for t, s in extra.items():
                j = list(T).index(float(t))
                fill = s.reindex(self.days).values
                V[:, j] = np.where(np.isnan(V[:, j]), fill, V[:, j])
        grid = np.arange(TMAX + 1, dtype=float)
        out = np.full((len(self.days), TMAX + 1), np.nan)
        for i in range(len(self.days)):
            ok = ~np.isnan(V[i])
            if not ok.any():
                continue
            t, v = T[ok], V[i][ok]
            if how == "vol":
                out[i] = np.interp(grid, t, v)
            elif how == "nearest":
                out[i] = v[np.abs(grid[:, None] - t[None, :]).argmin(axis=1)]
            else:
                g = np.clip(grid, t[0], t[-1])
                out[i] = np.sqrt(np.interp(g, t, v * v * t) / g)
        self._curves[k] = out
        return out


def _interp(pts, cal_days, how):
    if cal_days <= pts[0][0]:
        return pts[0][1]
    if cal_days >= pts[-1][0]:
        return pts[-1][1]
    if how == "nearest":
        return min(pts, key=lambda p: abs(p[0] - cal_days))[1]
    for (t0, v0), (t1, v1) in zip(pts[:-1], pts[1:]):
        if t0 <= cal_days <= t1:
            w = (cal_days - t0) / (t1 - t0)
            if how == "vol":
                return v0 + (v1 - v0) * w
            tv = v0 * v0 * t0 + (v1 * v1 * t1 - v0 * v0 * t0) * w
            return float(np.sqrt(tv / cal_days))
    raise ValueError("no bracket")
