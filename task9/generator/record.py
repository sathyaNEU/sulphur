"""task9 (architecture 10): the record as a solver rebuilds it from the pack alone (no World).

Requests from both generations of Tidewell's audit on one footing (New York dates, client side +1 buys / -1 sells,
face in units, the latest version of each request, re-sent duplicates dropped, 144A identifiers mapped to their
registered successors' original key); each request's segment (rating band on its date, the security master's bucket
for its quarter, the client's type); the schedule in force; the tape cleaned (cancelled reports dropped, corrected
reports in place of their originals); Ashcote's evaluated mids by bond and day; the Treasury curve and VIX.
"""
import os
from zoneinfo import ZoneInfo

import numpy as np
import pandas as pd
from openpyxl import load_workbook

import market as MK
import pack as PK
import params as P

NY = ZoneInfo(P.ZONE)
S1 = {v: k for k, v in PK.STATUS1.items()}
S2 = {v: k for k, v in PK.STATUS2.items()}
TYPE_CODE = {v: k for k, v in PK.TYPE_NAME.items()}
OFFLOAD_CHARGE = {("IG", "liquid"): 1.2, ("IG", "medium"): 2.4, ("IG", "thin"): 4.8,
                  ("HY", "liquid"): 4.2, ("HY", "medium"): 8.4, ("HY", "thin"): 15.6}     # policy 5(c), cents per 100


class Record:
    def __init__(self, tgt):
        self.tgt = tgt
        self.mk = MK.Market(src=tgt)
        self.days = self.mk.days
        self.dindex = {d: i for i, d in enumerate(self.days)}
        self._bonds()
        self._requests()
        self._schedules()
        self._evals()
        self._tape()

    # ---- bonds: the security master, the 144A map, buckets by quarter, ratings by date
    def _bonds(self):
        m = pd.read_csv(os.path.join(self.tgt, PK.F["master"]))
        self.master = m
        self.key = {c: c for c in m.cusip}
        for _, r in m.iterrows():
            if isinstance(r["registered_cusip"], str) and r["registered_cusip"]:
                self.key[r["registered_cusip"]] = r["cusip"]
        self.bix = {c: i for i, c in enumerate(m.cusip)}
        self.coupon = m.coupon_pct.values / 100.0
        self.maturity = pd.to_datetime(m.maturity).values
        self.issuer = m.issuer.values
        bk = pd.read_csv(os.path.join(self.tgt, PK.F["buckets"]))
        bk["k"] = bk.cusip.map(self.key)
        self.bucket = {(q, k): b for q, k, b in zip(bk.quarter, bk.k, bk.liquidity_bucket)}
        rt = pd.read_csv(os.path.join(self.tgt, PK.F["ratings"]))
        rt["effective_date"] = pd.to_datetime(rt.effective_date)
        self.ratings = {i: g.sort_values("effective_date") for i, g in rt.groupby("issuer")}
        cl = pd.read_csv(os.path.join(self.tgt, PK.F["clients"]))
        self.ctype = dict(zip(cl.client_code, cl.client_type.map(TYPE_CODE)))

    def band(self, issuer, day):
        g = self.ratings[issuer]
        r = g.rating.values[np.searchsorted(g.effective_date.values, np.datetime64(day), side="right") - 1]
        return "IG" if r in P.IG else "HY"

    # ---- requests
    def _requests(self):
        g1 = pd.read_csv(os.path.join(self.tgt, PK.F["rfq1"]))
        g2 = pd.read_csv(os.path.join(self.tgt, PK.F["rfq2"]))
        a = pd.DataFrame({"rfq": g1.RFQ_ID, "version": g1.MSG_VERSION,
                          "ts": pd.to_datetime(g1.RECEIVED_ET).dt.tz_localize(NY), "cusip": g1.CUSIP, "client": g1.CLIENT_CODE,
                          "side": np.where(g1.CLIENT_SIDE == "BUY", 1, -1), "q": g1.QTY.astype(float), "n": g1.DEALERS_IN_COMP,
                          "quote": g1.DESK_RESPONSE_PX, "ref": g1.DESK_REF_MID, "status": g1.STATUS.map(S1),
                          "done": g1.DONE_PX, "cover": g1.COVER_PX})
        b = pd.DataFrame({"rfq": g2.rfq_ref, "version": g2.msg_version,
                          "ts": pd.to_datetime(g2.received_utc, utc=True).dt.tz_convert(NY), "cusip": g2.security_id,
                          "client": g2.client, "side": np.where(g2.dir == "CB", 1, -1), "q": g2.quantity_000 * 1000.0,
                          "n": g2.n_dealers, "quote": g2.response_price, "ref": g2.ref_mid, "status": g2.outcome.map(S2),
                          "done": g2.executed_price, "cover": g2.cover_price})
        R = pd.concat([a, b], ignore_index=True)
        R = R.drop_duplicates()
        R = R.sort_values(["rfq", "version"]).drop_duplicates("rfq", keep="last").sort_values(["ts", "rfq"]).reset_index(drop=True)
        R["k"] = R.cusip.map(self.key)
        R["b"] = R.k.map(self.bix)
        R["day"] = R.ts.dt.tz_localize(None).dt.normalize()
        R["t"] = R.day.map(self.dindex)
        R["sec"] = (R.ts.dt.hour * 3600 + R.ts.dt.minute * 60 + R.ts.dt.second).astype(int)
        R["ty"] = R.client.map(self.ctype)
        R["quarter"] = R.day.dt.to_period("Q").astype(str)
        R["bucket"] = [self.bucket.get((q, k)) for q, k in zip(R.quarter, R.k)]
        R["band"] = [self.band(self.issuer[b], d) for b, d in zip(R.b, R.day)]
        R["traded"] = R.status.isin(["DONE", "COVER", "TRADED_AWAY"])
        R["won"] = R.status == "DONE"
        R["d_old"] = R.side * (R.quote - R.ref) * 100.0             # cents per 100 face from the reference mid
        self.R = R

    # ---- the schedule in force for each request, and the draft
    def _schedules(self):
        def read(path, sheet):
            ws = load_workbook(path, read_only=True)[sheet]
            out, eff = {}, None
            for row in ws.iter_rows(values_only=True):
                if row[0] and isinstance(row[0], str) and row[0].startswith("Effective from"):
                    eff = row[0]
                if row and row[0] in ("IG", "HY") and row[1] in P.BUCKETS:
                    out[(row[0], row[1], TYPE_CODE[row[2]])] = float(row[3])
            return out
        p = os.path.join(self.tgt, PK.F["schedule"])
        self.versions = [(pd.Timestamp("2023-01-03"), read(p, "v1")), (pd.Timestamp("2024-07-01"), read(p, "v2")),
                         (pd.Timestamp("2025-03-03"), read(p, "v3"))]
        self.current = self.versions[-1][1]
        self.proposed = read(os.path.join(self.tgt, PK.F["draft"]), "Draft 2027")
        R = self.R
        h = np.zeros(len(R))
        for (start, sched) in self.versions:
            m = (R.day >= start).values
            h[m] = [sched[(bd, bk, ty)] for bd, bk, ty in zip(R.band[m], R.bucket[m], R.ty[m])]
        R["h_actual"] = h
        R["h_cur"] = [self.current[(bd, bk, ty)] for bd, bk, ty in zip(R.band, R.bucket, R.ty)]
        R["h_prop"] = [self.proposed[(bd, bk, ty)] for bd, bk, ty in zip(R.band, R.bucket, R.ty)]
        self.changed = sorted([k for k in self.proposed if self.proposed[k] != self.current[k]],
                              key=lambda s: (s[0] != "IG", P.BUCKETS.index(s[1]), P.CLIENT_TYPES.index(s[2])))

    # ---- Ashcote's evaluated mids by bond and day
    def _evals(self):
        e = pd.read_csv(os.path.join(self.tgt, PK.F["eval"]))
        e["k"] = e.cusip.map(self.key)
        e["b"] = e.k.map(self.bix)
        e["t"] = pd.to_datetime(e.eval_date).map(self.dindex)
        M = np.full((len(self.days), len(self.master)), np.nan)
        M[e.t.values, e.b.values] = e.eval_mid.values
        self.eval = M
        # evaluated spread over the Treasury at each bond's maturity, and each band's median daily spread change
        mat = (self.maturity[None, :] - self.days.values[:, None]) / np.timedelta64(1, "D") / 365.25
        self.mat = np.maximum(mat, 1.0 / 365)
        tsy = np.array([self.mk.treasury(t, self.mat[t]) for t in range(len(self.days))])
        self.tsy = tsy
        yld = np.full_like(M, np.nan)
        for t in range(len(self.days)):
            ok = ~np.isnan(M[t])
            yld[t, ok] = _yield(M[t, ok], self.coupon[ok], self.mat[t, ok])
        self.spread = yld - tsy

    def market_move(self, t0, t1, b, band_spread_change):
        """The price change the Treasury curve and the band's spreads alone would give the bond from close t0 to t1."""
        c, m = self.coupon[b], self.mat[t0, b]
        s = self.spread[t0, b]
        p0 = MK.price(self.tsy[t0, b] + s, c, m)
        p1 = MK.price(self.tsy[t1, b] + s + band_spread_change, c, m)
        return p1 - p0

    # ---- the tape, cleaned
    def _tape(self):
        tp = pd.read_csv(os.path.join(self.tgt, PK.F["tape"]), dtype={"qty": str})
        cancelled = set(tp.orig_seq[tp.msg_type == "X"].dropna().astype(int))
        corrected = set(tp.orig_seq[tp.msg_type == "C"].dropna().astype(int))
        tp = tp[(tp.msg_type != "X") & ~tp.msg_seq.isin(cancelled) & ~tp.msg_seq.isin(corrected)].copy()
        tp["k"] = tp.cusip.map(self.key)
        tp["day"] = pd.to_datetime(tp.exec_date)
        hh = tp.exec_time.str.split(":", expand=True).astype(int)
        tp["sec"] = hh[0] * 3600 + hh[1] * 60 + hh[2]
        self.tape = tp


def _yield(price, coupon, mat, iters=40):
    """Yield of a clean price, by Newton steps on the house pricing formula."""
    y = coupon.copy() + 0.0
    for _ in range(iters):
        p = MK.price(y, coupon, mat)
        h = 1e-5
        dp = (MK.price(y + h, coupon, mat) - p) / h
        y = y - (p - price) / np.where(np.abs(dp) > 1e-9, dp, -1e-9)
    return y
