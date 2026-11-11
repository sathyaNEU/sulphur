"""task9 (architecture 10): the market record as pulled.

Every market value is read from the public files under raw10/ (raw10/manifest.json holds each file's URL, pull date
and sha256) or from a cut pack's copies of them; nothing is altered, filled into the files or simulated here. The
record's calendar is the bond market's: the days the Treasury curve is published inside the window.
"""
import hashlib
import json
import os

import numpy as np
import pandas as pd

import params as P

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw10")
SRC = [RAW]                       # where the series are read from: the pull, or a cut pack's copy of it
TENORS = {"DGS1": 1.0, "DGS2": 2.0, "DGS3": 3.0, "DGS5": 5.0, "DGS7": 7.0, "DGS10": 10.0, "DGS20": 20.0, "DGS30": 30.0}
FRED_IDS = list(TENORS) + ["DBAA", "DAAA", "SOFR"]
CBOE_IDS = ["VIX", "SPX"]
USED = list(TENORS) + ["DBAA", "DAAA", "SOFR", "VIX"]     # SPX ships as published and nothing reads it


def manifest():
    return json.load(open(os.path.join(RAW, "manifest.json")))


def check_raw():
    for f in manifest()["files"]:
        b = open(os.path.join(RAW, f["file"]), "rb").read()
        assert hashlib.sha256(b).hexdigest() == f["sha256"], "%s differs from its pull" % f["file"]


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
    return d.set_index("DATE")["CLOSE"].astype(float)


class Market:
    """The window's bond-market days with every series on them (a blank carried from the last published level)."""

    def __init__(self, src=None):
        if src:
            SRC[0] = src
        y = pd.DataFrame({k: fred(k) for k in TENORS})
        days = y.loc[P.START:P.END].dropna(how="all").index
        self.days = pd.DatetimeIndex(days)
        self.n = len(self.days)
        full = y.loc[:P.END].ffill()
        self.curve = full.reindex(self.days).values / 100.0          # decimals, days x tenors
        self.tenor = np.array(list(TENORS.values()))
        baa, aaa = fred("DBAA").loc[:P.END].ffill(), fred("DAAA").loc[:P.END].ffill()
        t10 = full["DGS10"]
        self.baa_spread = ((baa - t10).reindex(self.days).ffill().values) / 100.0
        self.aaa_spread = ((aaa - t10).reindex(self.days).ffill().values) / 100.0
        self.sofr = fred("SOFR").loc[:P.END].ffill().reindex(self.days).ffill().values / 100.0
        v = cboe("VIX").loc[:P.END]
        self.vix = v.reindex(v.index.union(self.days)).ffill().reindex(self.days).values
        assert not np.isnan(self.curve).any() and not np.isnan(self.vix).any() and not np.isnan(self.sofr).any()

    def treasury(self, i, mat):
        """Constant-maturity Treasury yield on day i at maturities mat (years), linear in maturity, flat beyond."""
        return np.interp(np.clip(mat, self.tenor[0], self.tenor[-1]), self.tenor, self.curve[i])

    def index_of(self, date):
        return int(self.days.searchsorted(pd.Timestamp(date)))


def price(yld, coupon, mat):
    """Clean price per 100 of a semiannual bullet bond, yield and coupon in decimals, mat in years."""
    mat = np.maximum(mat, 1.0 / 365)
    n = np.maximum(np.ceil(mat * 2 - 1e-9), 1)
    acc = n - mat * 2                                                       # fraction of a period accrued
    r = yld / 2.0
    c = coupon * 100 / 2.0
    disc = (1 + r) ** (-(n - acc))
    annuity = np.where(np.abs(r) > 1e-12, (1 - (1 + r) ** (-n)) / r, n)
    dirty = (c * annuity + 100 * (1 + r) ** (-n)) * (1 + r) ** acc
    return dirty - c * acc


def mod_duration(yld, coupon, mat):
    h = 1e-4
    p0 = price(yld, coupon, mat)
    return -(price(yld + h, coupon, mat) - price(yld - h, coupon, mat)) / (2 * h * p0)
