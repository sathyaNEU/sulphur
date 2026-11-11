"""task9: the market record as pulled, and the returns the pods ride on.

Every market value is read from the public files under raw/ (raw/manifest.json holds each file's URL, pull date and
sha256); nothing is altered, filled into the files or simulated. Two sets of daily returns are built from them:

  RISK_FACTORS   the platform's risk model as its methodology states it: price, yield and spread changes only
  HOLDING        what a passive holding of each exposure earned: the same moves plus the carry the holding earns
                 (the bill-financed yield of a duration position, the Baa spread of a credit position, the interest
                 differential of a G10 carry basket)

The pods' books are authored on HOLDING (world.py); the risk system reports them on RISK_FACTORS.
"""
import hashlib
import json
import os

import numpy as np
import pandas as pd

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")
START = pd.Timestamp("2016-12-30")

DUR = 8.0        # the risk model's 10-year duration
SDUR = 6.0       # its spread duration for credit
CURVE_DV = 4.0   # its steepener's return per unit change in the 10s less 2s spread
G10 = {"AUD": ("DEXUSAL", False, "IR3TIB01AUM156N"), "NZD": ("DEXUSNZ", False, "IR3TIB01NZM156N"),
       "GBP": ("DEXUSUK", False, "IR3TIB01GBM156N"), "EUR": ("DEXUSEU", False, "IR3TIB01EZM156N"),
       "JPY": ("DEXJPUS", True, "IR3TIB01JPM156N"), "CHF": ("DEXSZUS", True, "IR3TIB01CHM156N"),
       "CAD": ("DEXCAUS", True, "IR3TIB01CAM156N"), "NOK": ("DEXNOUS", True, "IR3TIB01NOM156N"),
       "SEK": ("DEXSDUS", True, "IR3TIB01SEM156N")}
# where a monthly rate series stops before the record ends, the next series for the same rate
RATE_FALLBACK = {"GBP": "IRSTCI01GBM156N", "EUR": "IR3TIB01DEM156N"}
CARRY_LEGS = 3
RISK_FACTORS = ["MKT", "TECH", "RATES", "CURVE", "CREDIT", "USD", "OIL", "VOL"]
HOLDING = RISK_FACTORS + ["FXCARRY"]


def manifest():
    return json.load(open(os.path.join(RAW, "manifest.json")))


def check_raw():
    for f in manifest()["files"]:
        b = open(os.path.join(RAW, f["file"]), "rb").read()
        assert hashlib.sha256(b).hexdigest() == f["sha256"], "%s differs from its pull" % f["file"]


SRC = [RAW]          # where the series are read from: the pull, or a cut pack's copy of it


def fred(sid):
    d = pd.read_csv(os.path.join(SRC[0], sid + ".csv"))
    d.columns = ["date", "v"]
    d["date"] = pd.to_datetime(d["date"])
    d["v"] = pd.to_numeric(d["v"], errors="coerce")
    return d.set_index("date")["v"]


def cboe(sym):
    d = pd.read_csv(os.path.join(SRC[0], sym + "_History.csv"))
    d.columns = [c.strip().upper() for c in d.columns]
    d["DATE"] = pd.to_datetime(d["DATE"], format="%m/%d/%Y")
    col = "CLOSE" if "CLOSE" in d.columns else d.columns[-1]
    return d.set_index("DATE")[col].astype(float)


def monthly(sid):
    s = fred(sid)
    s.index = s.index.to_period("M")
    return s


class Market:
    def __init__(self, src=RAW):
        SRC[0] = src
        spx = cboe("SPX")
        self.days = spx.loc[START:P.LAST_DAY].index            # the S&P 500's trading days
        d = self.days

        def on_days(s):
            return s.reindex(s.index.union(d)).ffill().reindex(d)

        self.level = pd.DataFrame({
            "SPX": spx.reindex(d), "NDX": on_days(fred("NASDAQ100")), "DGS2": on_days(fred("DGS2")), "DGS10": on_days(fred("DGS10")),
            "DTB3": on_days(fred("DTB3")), "DBAA": on_days(fred("DBAA")), "USD": on_days(fred("DTWEXBGS")),
            "BRENT": on_days(fred("DCOILBRENTEU")), "VIX": on_days(cboe("VIX"))})
        L = self.level
        mkt = L.SPX.pct_change()
        f = pd.DataFrame(index=d)
        f["MKT"] = mkt
        f["TECH"] = L.NDX.pct_change() - mkt
        f["RATES"] = -DUR * L.DGS10.diff() / 100.0
        f["CURVE"] = CURVE_DV * (L.DGS10 - L.DGS2).diff() / 100.0
        spread = L.DBAA - L.DGS10
        f["CREDIT"] = -SDUR * spread.diff() / 100.0
        f["USD"] = L.USD.pct_change()
        f["OIL"] = L.BRENT.pct_change()
        f["VOL"] = -L.VIX.diff() / 100.0
        self.risk = f.iloc[1:].fillna(0.0)
        gap = pd.Series(np.r_[np.nan, (d[1:] - d[:-1]).days], index=d) / 365.0     # the calendar time each return spans
        h = self.risk.copy()
        h["RATES"] = h["RATES"] + ((L.DGS10 - L.DTB3).shift(1) / 100.0 * gap).iloc[1:]
        h["CREDIT"] = h["CREDIT"] + (spread.shift(1) / 100.0 * gap).iloc[1:]
        h["FXCARRY"] = self.carry_basket(gap)
        self.hold = h.fillna(0.0)
        # the same holdings with a carry basket of two or four currencies a side (a rival construction)
        self.hold_alt = {}
        for legs in (2, 4):
            a = self.hold.copy()
            a["FXCARRY"] = self.carry_basket(gap, legs).fillna(0.0)
            self.hold_alt[legs] = a
        self.bill = (L.DTB3 / 100.0).reindex(self.risk.index)
        SRC[0] = RAW

    def carry_basket(self, gap, legs=CARRY_LEGS):
        """A dollar-neutral G10 carry basket: at each month end, long the three currencies with the highest 3-month
        rate that month and short the three with the lowest, equal weights; each leg earns its spot move against the
        dollar and its own rate, so the basket earns the spot spread plus the rate differential."""
        d = self.days
        spot = {}
        for c, (sid, per_usd, _) in G10.items():
            s = fred(sid)
            s = 1.0 / s if per_usd else s                               # US dollars per unit of the currency
            spot[c] = s.reindex(s.index.union(d)).ffill().reindex(d)
        spot = pd.DataFrame(spot)
        rates = {}
        for c, (_, _, rid) in G10.items():
            r = monthly(rid)
            if c in RATE_FALLBACK:
                r = r.combine_first(monthly(RATE_FALLBACK[c]))
            rates[c] = r
        rates = pd.DataFrame(rates).sort_index().ffill()
        months = d.to_period("M")
        ret = spot.pct_change()
        out = pd.Series(0.0, index=d)
        self.legs = {}
        for m in sorted(set(months)):
            prev = m - 1
            if prev not in rates.index:
                continue
            rr = rates.loc[prev].dropna().sort_values()
            lo, hi = list(rr.index[:legs]), list(rr.index[-legs:])
            if legs == CARRY_LEGS:
                self.legs[str(m)] = (hi, lo)
            idx = months == m
            dr = ret.loc[idx]
            g = gap[idx]
            long = (dr[hi] + rr[hi].values / 100.0 * g.values[:, None]).mean(axis=1)
            short = (dr[lo] + rr[lo].values / 100.0 * g.values[:, None]).mean(axis=1)
            out.loc[idx] = (long - short).values
        return out.iloc[1:]


def annual_sd(x, how="daily"):
    """The standard deviation of a daily return series over a year, read three ways."""
    if how == "daily":
        return float(x.std() * np.sqrt(252))
    if how == "monthly":
        m = x.groupby(x.index.to_period("M")).sum()
        return float(m.std() * np.sqrt(12))
    if how == "quarterly":
        q = x.groupby(x.index.to_period("Q")).sum()
        return float(q.std() * 2.0)
    raise ValueError(how)
