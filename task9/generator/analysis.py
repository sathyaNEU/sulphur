"""task9 (architecture 10): the analysis on the pack, as one engine over the routes.

A route is a set of choices: how a request's outcome at another quote is known (the exact replay from the covers on
wins and the winners' prints on the tape for losses, or a win model fitted on the desk's own quotes), how far after a
trade its cost is read on Ashcote's evaluations (net of the Treasury curve and the rating band's spreads), what the
trades a tighter quote adds are taken to cost (their own cost, or what today's wins cost), and how the year's range is
drawn (blocks of the record's days, or single days). The golden is one route; the hurried passes are others.
"""
import numpy as np
import pandas as pd
from numpy.linalg import solve

import params as P
from record import OFFLOAD_CHARGE, Record

MATCH_SECONDS = 180


class Analysis:
    def __init__(self, rec):
        self.rec = rec
        R = rec.R
        self.R = R
        self.T = len(rec.days)
        self._band_moves()
        self._rivals()
        R["off"] = [OFFLOAD_CHARGE[(bd, bk)] for bd, bk in zip(R.band, R.bucket)]
        inb = (R.day >= pd.Timestamp(P.BASE_FROM)) & (R.day <= pd.Timestamp(P.BASE_TO))
        R["inbase"] = inb
        R["seg"] = R.band + "|" + R.bucket + "|" + R.ty
        n_all = R.groupby("seg").size()
        n_base = R[inb].groupby("seg").size().reindex(n_all.index).fillna(0)
        self.scale = {tuple(k.split("|")): v for k, v in (n_base / n_all).items()}
        self.n_base = {tuple(k.split("|")): v for k, v in n_base.items()}
        self._costs = {}

    # ---- each rating's own spread move, from the evaluations of every bond the issuer ratings history gives that rating
    def _band_moves(self):
        rec = self.rec
        S = rec.spread
        rat = np.empty(S.shape, dtype=object)
        for b in range(S.shape[1]):
            g = rec.ratings[rec.issuer[b]]
            idx = np.searchsorted(g.effective_date.values, rec.days.values, side="right") - 1
            rat[:, b] = g.rating.values[np.maximum(idx, 0)]
        self.rating_of = rat
        dS = np.diff(S, axis=0)
        cum = {}
        for rr in P.RATINGS:
            x = np.where(rat[1:] == rr, dS, np.nan)
            with np.errstate(all="ignore"):
                med = np.nanmedian(x, axis=1)
            med = np.where(np.isnan(med), 0.0, med)
            cum[rr] = np.r_[0.0, np.cumsum(med)]
        self.band_cum = cum

    # ---- the best rival level for each traded request: the cover on a win, the winner's print on a loss
    def _rivals(self):
        rec, R = self.rec, self.R
        r = np.full(len(R), np.nan)
        won = R.won.values
        r[won] = (R.side.values * (R.cover.values - R.ref.values) * 100.0)[won]
        tp = rec.tape
        cust = tp[tp.contra == "C"].copy()
        cust["qnum"] = pd.to_numeric(cust.qty, errors="coerce")
        cust["capped"] = cust.qty.str.endswith("+")
        lost = R[R.status.isin(["COVER", "TRADED_AWAY"])].copy()
        lost["rside"] = np.where(lost.side > 0, "S", "B")          # the winner sold to a buying client
        lost["cap"] = np.where(lost.band == "IG", P.CAP["IG"], P.CAP["HY"])
        lost["i"] = np.arange(len(lost))
        m = lost.merge(cust[["k", "day", "rpt_side", "sec", "price", "qnum", "capped", "msg_seq"]],
                       left_on=["k", "day", "rside"], right_on=["k", "day", "rpt_side"], how="inner", suffixes=("", "_p"))
        dt_ = m.sec_p - m.sec
        size_ok = (m.capped & (m.q > m.cap)) | (~m.capped & (np.abs(m.qnum - m.q) < 0.5))
        m = m[(dt_ >= 0) & (dt_ <= MATCH_SECONDS) & size_ok].copy()
        m["dt"] = m.sec_p - m.sec
        m = m.sort_values(["i", "dt"]).drop_duplicates("i")
        # a print matched to two requests goes to the nearer one
        m = m.sort_values(["msg_seq", "dt"]).drop_duplicates("msg_seq")
        idx = lost.index.values[m.i.values]
        r[R.index.get_indexer(idx)] = R.side.values[R.index.get_indexer(idx)] * (m.price.values - R.ref.values[R.index.get_indexer(idx)]) * 100.0
        R["r"] = r
        self.match_rate = float(np.isfinite(r[R.status.isin(["COVER", "TRADED_AWAY"]).values]).mean())

    # ---- a request's cost after the trade, read H trading days on, net of the curve and the band's spreads
    def cost(self, H):
        if H in self._costs:
            return self._costs[H]
        rec, R = self.rec, self.R
        t0 = R.t.values.astype(int)
        b = R.b.values.astype(int)
        t1 = np.minimum(t0 + H, self.T - 1)
        ev = rec.eval
        e1 = ev[t1, b]
        # a bond that stops being evaluated (it matured) keeps its last evaluation
        bad = np.isnan(e1)
        for j in np.where(bad)[0]:
            col = ev[t0[j]:t1[j] + 1, b[j]]
            ok = np.where(~np.isnan(col))[0]
            e1[j] = col[ok[-1]] if len(ok) else R.ref.values[j]
            t1[j] = t0[j] + (ok[-1] if len(ok) else 0)
        rr = self.rating_of[t0, b]
        bc = np.zeros(len(R))
        for x in P.RATINGS:
            m = rr == x
            bc[m] = self.band_cum[x][t1[m]] - self.band_cum[x][t0[m]]
        cpn, mat0 = rec.coupon[b], rec.mat[t0, b]
        s0 = rec.spread[t0, b]
        s0 = np.where(np.isnan(s0), np.nanmedian(rec.spread[t0], axis=1), s0)
        import market as MK
        mm = MK.price(rec.tsy[t1, b] + s0 + bc, cpn, mat0) - MK.price(rec.tsy[t0, b] + s0, cpn, mat0)
        c = R.side.values * ((e1 - R.ref.values) - mm) * 100.0
        self._costs[H] = c
        return c

    # ---- win models
    @staticmethod
    def _logit(x, y):
        X = np.c_[np.ones_like(x), x]
        w = np.zeros(2)
        for _ in range(50):
            p = 1 / (1 + np.exp(-X @ w))
            Wt = p * (1 - p) + 1e-9
            w = w + solve(X.T @ (X * Wt[:, None]) + 1e-6 * np.eye(2), X.T @ (y - p))
        return w

    def plan(self, win="exact", H=40, added="own", unmatched="lost"):
        """Each segment's P&L over the record at the current and the proposed schedule, scaled to the base year."""
        R = self.R
        c = self.cost(H)
        d_old = np.nan_to_num(R.d_old.values)              # a passed request has no distance; it stays passed
        d_cur = d_old * R.h_cur.values / R.h_actual.values
        d_prop = d_old * R.h_prop.values / R.h_actual.values
        traded = R.traded.values
        won = R.won.values
        r = R.r.values
        q = R.q.values
        off = R.off.values
        segs = R.seg.values
        out = {}
        daily_cur = np.zeros(self.T)
        daily_prop = np.zeros(self.T)
        tt = R.t.values.astype(int)
        for sk in sorted(set(segs)):
            m = segs == sk
            s = tuple(sk.split("|"))
            sc = self.scale[s]
            if win == "exact":
                known = np.isfinite(r) & traded & m
                wc = known & (d_cur < r)
                wp = known & (d_prop < r)
                if unmatched == "share":
                    # an unmatched loss is taken to fall to the new quote at the matched losses' rate
                    lostm = m & traded & ~won & np.isfinite(r)
                    um = m & traded & ~won & ~np.isfinite(r)
                    rate = (lostm & (d_prop < r)).sum() / max(lostm.sum(), 1)
                    extra = um.astype(float) * rate
                else:
                    extra = np.zeros(len(R))
                pc = np.where(wc, (d_cur - c - off) * q / 1e4, 0.0)
                ca = c if added == "own" else np.full(len(R), np.average(c[m & won], weights=q[m & won]) if (m & won).any() else 0.0)
                pp = np.where(wp & wc, (d_prop - c - off) * q / 1e4, 0.0) + np.where(wp & ~wc, (d_prop - ca - off) * q / 1e4, 0.0)
                pp = pp + extra * (d_prop - ca - off) * q / 1e4
                add_mask = wp & ~wc
                share = (wp.sum() + extra.sum()) / m.sum()
                add_cost = np.average(ca[add_mask], weights=q[add_mask]) if add_mask.any() else np.nan
            else:
                f = m & traded
                w = self._logit(d_old[f] / 10.0, won[f].astype(float))
                pf = lambda d: 1 / (1 + np.exp(-(w[0] + w[1] * d / 10.0)))
                p_c = np.where(f, pf(d_cur), 0.0)
                p_p = np.where(f, pf(d_prop), 0.0)
                cw = np.average(c[m & won], weights=q[m & won]) if (m & won).any() else 0.0
                ca = c if added == "own" else np.full(len(R), cw)
                pc = p_c * (d_cur - ca - off) * q / 1e4
                pp = p_p * (d_prop - ca - off) * q / 1e4
                share = p_p[m].sum() / m.sum()
                gain = np.clip(p_p - p_c, 0, None)
                add_cost = np.average(ca[m], weights=(gain * q)[m]) if (gain * q)[m].sum() > 0 else np.nan
            np.add.at(daily_cur, tt[m], pc[m] * sc * self.T / P.PLAN_DAYS)
            np.add.at(daily_prop, tt[m], pp[m] * sc * self.T / P.PLAN_DAYS)
            won_cost = np.average(c[m & won], weights=q[m & won]) if (m & won).any() else np.nan
            out[s] = dict(cur=float(pc[m].sum() * sc), prop=float(pp[m].sum() * sc), share=float(share),
                          add_cost=float(add_cost) * 100 if add_cost == add_cost else None,
                          won_cost=float(won_cost) * 100 if won_cost == won_cost else None)
        return out, daily_cur, daily_prop

    @staticmethod
    def year_range(daily, block=P.BLOCK, sims=P.SIMS, days=P.PLAN_DAYS, seed=P.SEED, iid=False):
        rng = np.random.default_rng(seed)
        n = len(daily)
        tot = np.zeros(sims)
        if iid or block <= 1:
            idx = rng.integers(0, n, (sims, days))
            tot = daily[idx].sum(axis=1)
        else:
            nb = int(np.ceil(days / block))
            starts = rng.integers(0, n, (sims, nb))
            idx = (starts[:, :, None] + np.arange(block)[None, None, :]) % n
            tot = daily[idx.reshape(sims, -1)[:, :days]].sum(axis=1)
        return float(np.percentile(tot, P.RANGE_P[0])), float(np.percentile(tot, P.RANGE_P[1])), float(tot.mean())


def run(tgt, **kw):
    A = Analysis(Record(tgt))
    return A, A.plan(**kw)
