"""task9: the golden analysis, every sound rival of it and every hurried route, run on the real record.

Nothing here reads the prompt. Each function is one method; run() calls the golden's, then each rival's and each
shortcut's, so the bands and the margins in figures.json are measurements.
"""
import math

import numpy as np
import pandas as pd

import book as BK
import market as MK
import params as P
import swaps as SW

# two-sided rebuilds of a missing strike; "actual" takes the index's published closes from the public record where the
# Cboe download has none (4 December 2007 on, held outside the pack) and total variance before that
REBUILDS = ("calibrated", "variance", "vol", "calibrated-log", "calibrated-1y", "actual")
MARKS = {                                                             # sound ways to read the implied term structure
    "total variance": dict(),
    "linear in volatility": dict(how="vol"),
    "nearest published term": dict(how="nearest"),
    "without the 9-day index": dict(points=(30, 93, 184, 365)),
}
PROXIES = ("30-day index as it stands", "30-day index times the average ratio", "regression on the 30-day index alone")
CAREFUL_PROXY = "regression on the 30-day index alone"               # the one-index stand-in the careful pass validates and keeps
BLOCKS = {12: (12, 18, 24, 36), 6: (6, 12, 18, 24), 3: (3, 6, 12, 24)}    # block lengths in monthly sales, by maturity
NW_LAGS = {12: (11, 17, 23), 6: (5, 11, 17), 3: (2, 5, 11)}
Z80 = 1.2816


def floor_to(x, step):
    return math.floor(x / step + 1e-9) * step


class Analysis:
    def __init__(self, mk=None, book=None):
        self.mk = mk or MK.Market()
        self.book = book or BK.Book(self.mk)
        self._lad, self._mk = {}, {}

    # ------------------------------------------------------------------ ladders on the record
    def ladder(self, mat, rebuild="calibrated"):
        key = (mat, rebuild)
        if key not in self._lad:
            self._lad[key] = SW.Ladder(self.mk, mat, rebuild=rebuild)
        return self._lad[key]

    def marks(self, mat, rebuild="calibrated", name="total variance", **extra):
        key = (mat, rebuild, name, tuple(sorted(extra.items())))
        if key not in self._mk:
            kw = dict(MARKS.get(name, {}))
            kw.update(extra)
            if kw.pop("rebuilt_terms", False):
                kw.update(extra={93: SW.rebuilt_series(self.mk, 3), 184: SW.rebuilt_series(self.mk, 6)}, key="rebuilt-terms")
            if kw.pop("actual_terms", False):
                kw.update(extra={93: self.mk.actual3m()}, key="actual-terms")
            self._mk[key] = self.ladder(mat, rebuild).marks(**kw)[0]
        return self._mk[key]

    def ladder_figs(self, mat, rebuild="calibrated", ladder=None):
        L = ladder or self.ladder(mat, rebuild)
        s = L.settled()
        y = L.by_year()
        return dict(avg_per_sale=float(s.pay.mean()), n_settled=int(len(s)), n_rebuilt=int((s.how == "rebuilt").sum()), worst=float(y.min()),
                    worst_year=int(y.idxmin()), by_year={int(k): float(v) for k, v in y.items()}, first_sale=str(s.sale.min().date()))

    def proxy_fit(self, mat):
        """The one-index stand-ins for a maturity's index, fitted on every day it is published with the 30-day index."""
        key = ("proxy", mat)
        if key not in self._lad:
            ix = MK.MATURITY_INDEX[mat]
            ov = self.mk.idx[["VIX", ix]].dropna()
            b = np.linalg.lstsq(np.column_stack([np.ones(len(ov)), ov.VIX.values]), ov[ix].values, rcond=None)[0]
            res = ov[ix].values - (b[0] + b[1] * ov.VIX.values)
            hot = ov.VIX.values > P.HOT
            self._lad[key] = dict(ratio=float((ov[ix] / ov.VIX).mean()), b=b, r2=float(1 - (res ** 2).sum() / ((ov[ix] - ov[ix].mean()) ** 2).sum()),
                                  rmse=float(np.sqrt((res ** 2).mean())), n=int(len(ov)), ov=ov, hot=hot)
        return self._lad[key]

    def proxy_value(self, mat, method, v):
        f = self.proxy_fit(mat)
        return {"30-day index as it stands": v, "30-day index times the average ratio": v * f["ratio"],
                "regression on the 30-day index alone": f["b"][0] + f["b"][1] * v}[method]

    def proxy_ladder(self, mat, method):
        """A ladder whose missing strikes come from a one-sided proxy (the hurried rebuilds)."""
        key = ("proxy-ladder", mat, method)
        if key not in self._lad:
            L = SW.Ladder(self.mk, mat)
            t = L.t.copy()
            for i in t.index[t.how == "rebuilt"]:
                t.at[i, "k"] = self.proxy_value(mat, method, float(self.mk.idx.at[t.at[i, "sale"], "VIX"]))
            t["pay"] = SW.pay(t.k, t.rv, SW.CAP)
            L.t = t
            self._lad[key] = L
        return self._lad[key]

    def strike_series(self, mat, how="calibrated"):
        """The maturity's index on every day of the record: published where it is, and where it is not by a rebuild
        (one of REBUILDS) or a one-index stand-in (one of PROXIES); carried over a day with no close."""
        key = ("series", mat, how)
        if key not in self._lad:
            if how in PROXIES:
                s = self.mk.idx[MK.MATURITY_INDEX[mat]].copy()
                gap = s.isna() & (s.index >= MK.RECORD_START)
                s[gap] = self.proxy_value(mat, how, self.mk.idx.VIX[gap])
            else:
                s = SW.rebuilt_series(self.mk, mat, how)
            self._lad[key] = s.ffill()
        return self._lad[key]

    # ------------------------------------------------------------------ the room beside the standing ladder
    def room(self, new_mat, rebuild="calibrated", marks="total variance", with_old=True, use_s=True, use_c=True, ladder=None, old_marks=None,
             ls=P.LIM_SETTLE, lc=P.LIM_COLL, **extra):
        Ln = ladder or self.ladder(new_mat, rebuild)
        yn = Ln.by_year()
        if ladder is not None:
            mn = Ln.marks(**MARKS.get(marks, {}))[0]
        else:
            mn = self.marks(new_mat, rebuild, marks, **extra)
        yo = self.ladder(P.OLD_MAT).by_year()
        mo = self.marks(P.OLD_MAT, "calibrated", old_marks or marks, **extra)
        best, why = np.inf, None
        if use_s:
            for y in yn.index:
                used = -float(yo.get(y, 0.0)) * P.OLD_SIZE if with_old else 0.0
                if yn[y] < 0 and (ls - used) / -yn[y] < best:
                    best, why = (ls - used) / -yn[y], ("settlement", int(y))
        if use_c:
            used = (-mo * P.OLD_SIZE) if with_old else 0.0 * mo
            neg = mn < 0
            b = (lc - used[neg]) / -mn[neg]
            if float(b.min()) < best:
                best, why = float(b.min()), ("collateral", str(b.idxmin().date()))
        return dict(raw=float(best), size=int(floor_to(best, P.SIZE_STEP)), limit=why[0], when=why[1])

    def usage(self, new_mat, size, rebuild="calibrated", marks="total variance"):
        """The sleeve's worst calendar year and peak collateral on the record with a new ladder at a size."""
        yn, yo = self.ladder(new_mat, rebuild).by_year(), self.ladder(P.OLD_MAT).by_year()
        yrs = sorted(set(yn.index) | set(yo.index))
        tot = pd.Series({y: float(yn.get(y, 0.0)) * size + float(yo.get(y, 0.0)) * P.OLD_SIZE for y in yrs})
        v = self.marks(new_mat, rebuild, marks) * size + self.marks(P.OLD_MAT, "calibrated", marks) * P.OLD_SIZE
        return dict(worst_year=int(tot.idxmin()), worst=float(-tot.min()), peak=float(-v.min()), peak_day=str(v.idxmin().date()),
                    old_at_peak=float(-self.marks(P.OLD_MAT, "calibrated", marks)[v.idxmin()] * P.OLD_SIZE),
                    new_at_peak=float(-self.marks(new_mat, rebuild, marks)[v.idxmin()] * size))

    # ------------------------------------------------------------------ the open book at the review date
    def open_book(self, date=None, how="variance", remaining="term"):
        mk, date = self.mk, date or P.REVIEW
        C = mk.curve(how)
        i = mk.pos(date)
        t = self.book.ladder.t
        t = t[(t.sale < date) & (t.expiry > date)].copy()
        t["n_e"] = [mk.count(s, date) for s in t.sale]
        t["n_r"] = [mk.count(date, e) for e in t.expiry]
        t["acc2"] = [mk.realised_var(s, date) for s in t.sale]
        t["acc_vol"] = np.sqrt(t.acc2)
        t["cal"] = [(e - date).days for e in t.expiry]
        if remaining == "term":
            t["iv"] = [float(C[i, min(c, MK.TMAX)]) for c in t.cal]
        elif remaining == "original":
            t["iv"] = float(mk.idx.at[date, MK.MATURITY_INDEX[P.OLD_MAT]])
        else:
            t["iv"] = float(mk.idx.at[date, "VIX"])
        w = np.minimum((t.n_e * t.acc2 + t.n_r * t.iv ** 2) / (t.n_e + t.n_r), (SW.CAP * t.k) ** 2)
        t["mark"] = (t.k ** 2 - w) / (2 * t.k)
        return t.reset_index(drop=True)

    # ------------------------------------------------------------------ what the open swaps go on to pay
    def replay(self, year=P.PLAN_YEAR, how="variance"):
        """Every start date of the record applied to the swaps that expire in the plan year: for each start date and
        swap, realised variance over the swap's remaining number of days as a share of the variance implied that day
        for its remaining term (ratio), and that realised variance itself (level)."""
        mk = self.mk
        ob = self.open_book()
        ob = ob[ob.expiry.dt.year == year].reset_index(drop=True)
        C = mk.curve(how)
        cum = mk.cum.values
        i0 = int(mk.days.searchsorted(pd.Timestamp("2007-01-01")))
        starts = np.arange(i0, mk.pos(P.REVIEW) - int(ob.n_r.max()) + 1)
        rat = np.empty((len(starts), len(ob)))
        lev = np.empty((len(starts), len(ob)))
        imp = np.empty((len(starts), len(ob)))
        for j, s in enumerate(ob.itertuples()):
            rv = 1e4 * 252.0 * (cum[starts + s.n_r] - cum[starts]) / s.n_r
            iv = C[starts, min(s.cal, MK.TMAX)]
            rat[:, j], lev[:, j], imp[:, j] = rv / (iv * iv), rv, iv * iv
        return dict(ob=ob, starts=mk.days[starts], ratio=rat, level=lev, implied=imp)

    @staticmethod
    def settle(ob, rem_var):
        """Settlement per unit of vega of each swap (columns) given the variance of its remaining days."""
        k, ne, a2, nr = ob.k.values, ob.n_e.values.astype(float), ob.acc2.values, ob.n_r.values.astype(float)
        w = np.minimum((ne * a2 + nr * rem_var) / (ne + nr), (SW.CAP * k) ** 2)
        return (k * k - w) / (2 * k)

    def expectations(self, rp):
        """The open swaps' expected settlement in total (per unit of vega per monthly sale) under each method."""
        ob, rat, lev, imp = rp["ob"], rp["ratio"], rp["level"], rp["implied"]
        iv2 = ob.iv.values ** 2
        mk = self.mk
        out = {}
        out["start dates replayed, ratio to implied (the golden)"] = self.settle(ob, rat * iv2).sum(axis=1).mean()
        out["start dates replayed, realised level"] = self.settle(ob, lev).sum(axis=1).mean()
        out["ratio of means at each remaining term"] = self.settle(ob, lev.sum(axis=0) / imp.sum(axis=0) * iv2).sum()
        out["mean of ratios at each remaining term"] = self.settle(ob, rat.mean(axis=0) * iv2).sum()
        reg, loc, smear = [], [], []
        for j in range(len(ob)):
            X = np.column_stack([np.ones(len(imp)), imp[:, j]])
            b = np.linalg.lstsq(X, lev[:, j], rcond=None)[0]
            reg.append(b[0] + b[1] * iv2[j])
            near = np.abs(np.sqrt(imp[:, j]) - ob.iv.values[j]) < 4.0
            loc.append(lev[near, j].mean())
            Xl = np.column_stack([np.ones(len(imp)), np.log(imp[:, j])])
            bl = np.linalg.lstsq(Xl, np.log(lev[:, j]), rcond=None)[0]
            res = np.log(lev[:, j]) - Xl @ bl
            smear.append(np.exp(bl[0] + bl[1] * np.log(iv2[j])) * np.exp(res).mean())
        out["regression of realised on implied variance"] = self.settle(ob, np.array(reg)).sum()
        out["start dates with implied within 4 points"] = self.settle(ob, np.array(loc)).sum()
        out["log regression, retransformed"] = self.settle(ob, np.array(smear)).sum()
        d0 = pd.Timestamp("2007-01-01")
        r1 = self._pooled_ratio(21, 30)
        r12 = self._pooled_ratio(252, 365)
        out["one ratio, measured at one month"] = self.settle(ob, r1 * iv2).sum()
        out["one ratio, measured at twelve months"] = self.settle(ob, r12 * iv2).sum()
        out["average realised variance since 2007"] = self.settle(ob, np.full(len(ob), 1e4 * 252 * mk.lr2[mk.lr2.index >= d0].mean())).sum()
        hurried = {}
        # experience from before the record begins, which schedule D.5(a) and D.7(c) leave out
        hurried["average realised variance since 1990 (before the record)"] = self.settle(
            ob, np.full(len(ob), 1e4 * 252 * mk.lr2[mk.lr2.index >= "1990-01-02"].mean())).sum()
        hurried["the mark (implied variance for the remaining term)"] = self.settle(ob, iv2).sum()
        hurried["the median start date"] = float(np.median(self.settle(ob, rat * iv2).sum(axis=1)))
        # realised volatility forecast as a share of implied volatility and then squared: the settlement is linear in
        # variance, so the average has to be taken of the variance
        hurried["a volatility forecast, squared"] = self.settle(ob, np.sqrt(rat).mean(axis=0) ** 2 * iv2).sum()
        hurried["a volatility forecast from realised levels, squared"] = self.settle(ob, np.sqrt(lev).mean(axis=0) ** 2).sum()
        own = rp["starts"] >= pd.Timestamp("2021-07-01")
        hurried["ratio on the sleeve's own years"] = self.settle(ob, lev[own].sum(axis=0) / imp[own].sum(axis=0) * iv2).sum()
        hurried["the record's average per 12-month swap"] = float(self.ladder(P.OLD_MAT).settled().pay.mean()) * len(ob)
        i = mk.pos(P.REVIEW)
        tr = 1e4 * 252 * (mk.cum.iloc[i] - mk.cum.iloc[i - 63]) / 63
        hurried["the last three months' realised variance carried on"] = self.settle(ob, np.full(len(ob), tr)).sum()
        return {k: float(v) for k, v in out.items()}, {k: float(v) for k, v in hurried.items()}

    def _pooled_ratio(self, n, cal):
        mk = self.mk
        C = mk.curve()
        cum = mk.cum.values
        i0 = int(mk.days.searchsorted(pd.Timestamp("2007-01-01")))
        s = np.arange(i0, mk.pos(P.REVIEW) - n + 1)
        rv = 1e4 * 252.0 * (cum[s + n] - cum[s]) / n
        iv2 = C[s, cal] ** 2
        return float(rv.sum() / iv2.sum())

    def ranges(self, rp):
        ob, rat, lev = rp["ob"], rp["ratio"], rp["level"]
        iv2 = ob.iv.values ** 2
        pay = self.settle(ob, rat * iv2)
        tot = pay.sum(axis=1)
        q = lambda x, p: float(np.percentile(x, p))
        sound = {
            "start dates replayed jointly, ratio to implied (the golden)": (q(tot, 10), q(tot, 90)),
            "start dates replayed jointly, realised level": (q(self.settle(ob, lev).sum(axis=1), 10), q(self.settle(ob, lev).sum(axis=1), 90)),
            "each swap's own percentile, added": (sum(q(pay[:, j], 10) for j in range(len(ob))), sum(q(pay[:, j], 90) for j in range(len(ob)))),
            "every fifth start date": (q(tot[::5], 10), q(tot[::5], 90)),
        }
        rng = np.random.default_rng(20261109)
        ind = np.zeros(200_000)
        for j in range(len(ob)):
            ind += rng.choice(pay[:, j], size=len(ind))
        sd_i = float(np.sqrt((pay.std(axis=0) ** 2).sum()))
        y = self.ladder(P.OLD_MAT).by_year()
        full = y[(y.index >= 2008) & (y.index <= P.REVIEW.year - 1)] * len(ob) / 12.0
        hurried = {
            "swaps drawn independently": (q(ind, 10), q(ind, 90)),
            "normal, the swaps' spreads added in quadrature": (float(tot.mean() - 1.2816 * sd_i), float(tot.mean() + 1.2816 * sd_i)),
            "the 12-month ladder's calendar years": (q(full.values, 10), q(full.values, 90)),
        }
        stats = dict(mean=float(tot.mean()), median=q(tot, 50), p10=q(tot, 10), p20=q(tot, 20), p80=q(tot, 80), p90=q(tot, 90), minimum=float(tot.min()),
                     share_below_mark=float((tot < self.settle(ob, iv2).sum()).mean()), share_below_zero=float((tot < 0).mean()), n_starts=int(len(tot)),
                     first_start=str(rp["starts"][0].date()), last_start=str(rp["starts"][-1].date()), per_swap_mean=[float(v) for v in pay.mean(axis=0)])
        return sound, hurried, stats

    # ------------------------------------------------------------------ how well the record pins a ladder's average
    @staticmethod
    def _nw_se(x, lags):
        n, e = len(x), x - x.mean()
        v = (e * e).sum() / n
        for l in range(1, lags + 1):
            v += 2 * (1 - l / (lags + 1.0)) * (e[l:] * e[:-l]).sum() / n
        return float(np.sqrt(v / n))

    @staticmethod
    def _block_means(x, block, seed, draws=20000):
        """Averages of the series resampled in circular blocks of consecutive sales."""
        n = len(x)
        nb = int(np.ceil(n / float(block)))
        st = np.random.default_rng(seed).integers(0, n, size=(draws, nb))
        idx = ((st[:, :, None] + np.arange(block)[None, None, :]) % n).reshape(draws, nb * block)[:, :n]
        return x[idx].mean(axis=1)

    def avg_ranges(self, mat, rebuild="calibrated", ladder=None):
        """The 80 per cent range of a ladder's average settlement per sale on the record (per unit of vega): methods
        that keep neighbouring sales together (sound), and methods that treat each settlement as unrelated (hurried)."""
        L = ladder or self.ladder(mat, rebuild)
        s = L.settled()
        x = s.pay.values
        n, mean, sd = len(x), float(x.mean()), float(x.std(ddof=1))
        q = lambda v: (float(np.percentile(v, 10)), float(np.percentile(v, 90)))
        sound = {}
        for b in BLOCKS[mat]:
            sound["circular blocks of %d sales" % b] = q(self._block_means(x, b, 20261109 + 100 * mat + b))
        for l in NW_LAGS[mat]:
            se = self._nw_se(x, l)
            sound["Newey-West, %d lags" % l] = (mean - Z80 * se, mean + Z80 * se)
        yr = s.groupby(s.expiry.dt.year).pay.mean()
        se_y = float(yr.std(ddof=1) / np.sqrt(len(yr)))
        by_year = (float(yr.mean() - Z80 * se_y), float(yr.mean() + Z80 * se_y))
        sound["averages by calendar year of expiry"] = by_year
        se_n = sd / np.sqrt(n / float(mat))                      # as many observations as there are swaps that do not overlap
        sound["counted as swaps that do not overlap"] = (mean - Z80 * se_n, mean + Z80 * se_n)
        rng = np.random.default_rng(20261109 + mat)
        iid = x[rng.integers(0, n, size=(20000, n))].mean(axis=1)
        few = max(1, mat // 2 - 1)                               # fewer lags than the months two neighbouring swaps share
        se_few = self._nw_se(x, few)
        hurried = {"single settlements resampled": q(iid),
                   "normal, the standard error of unrelated sales": (mean - Z80 * sd / np.sqrt(n), mean + Z80 * sd / np.sqrt(n)),
                   "a standard error with too few lags": (mean - Z80 * se_few, mean + Z80 * se_few)}
        e = x - mean
        stats = dict(n=n, mean=mean, sd=sd, iid_se=sd / np.sqrt(n), nw_se=self._nw_se(x, NW_LAGS[mat][1]), few_lags=few,
                     ac1=float((e[1:] * e[:-1]).sum() / (e * e).sum()), ac_half=float((e[mat // 2:] * e[:-(mat // 2)]).sum() / (e * e).sum()),
                     by_year=by_year, years=int(len(yr)))
        return sound, hurried, stats

    # ------------------------------------------------------------------ every settlement that falls in the plan year
    def plan_legs(self, year=P.PLAN_YEAR):
        """The swaps not yet sold at the review date that expire in the plan year: the standing ladder's remaining
        sales and the new ladder's, each with its sale and expiry counted in scheduled days from the review date."""
        mk = self.mk
        legs = []
        for m in range(1, 13):
            sale, exp = mk.sale_date(year - 1, m), mk.expiry(year, m)
            if sale > P.REVIEW:
                legs.append(dict(ladder=P.OLD_MAT, sale=sale, expiry=exp))
        cal = self.new_calendar(P.NEW_MAT, year)
        for r in cal[cal.in_year].itertuples():
            legs.append(dict(ladder=P.NEW_MAT, sale=r.sale, expiry=r.expiry))
        for g in legs:
            g["so"], g["eo"] = mk.count(P.REVIEW, g["sale"]), mk.count(P.REVIEW, g["expiry"])
        return legs

    def plan(self, size, rebuild="calibrated", basis="ratio", year=P.PLAN_YEAR, with_unsold_old=True):
        """What the plan year's settlements would have come to from every start date of the record: the open swaps
        over their remaining days, and each swap not yet sold struck and run the same number of days later. US dollars
        by start date, for the standing ladder at its size and the new ladder at `size`."""
        mk = self.mk
        rp = self.replay(year)
        ob = rp["ob"]
        iv2 = ob.iv.values ** 2
        legs = self.plan_legs(year)
        cum = mk.cum.values
        i0 = int(mk.days.searchsorted(MK.RECORD_START))
        starts = np.arange(i0, mk.pos(P.REVIEW) - max(g["eo"] for g in legs) + 1)
        n = len(starts)
        rem = rp["ratio"][:n] * iv2 if basis == "ratio" else rp["level"][:n]
        open_ = self.settle(ob, rem).sum(axis=1) * P.OLD_SIZE
        k12 = self.strike_series(P.OLD_MAT).values
        k3 = self.strike_series(P.NEW_MAT, rebuild).values
        old, new, cols = np.zeros(n), np.zeros(n), [self.settle(ob, rem)[:, j] * P.OLD_SIZE for j in range(len(ob))]
        for g in legs:
            k = (k12 if g["ladder"] == P.OLD_MAT else k3)[starts + g["so"]]
            rv = np.sqrt(1e4 * 252.0 * (cum[starts + g["eo"]] - cum[starts + g["so"]]) / (g["eo"] - g["so"]))
            pay = SW.pay(k, rv)
            if g["ladder"] == P.OLD_MAT:
                if with_unsold_old:
                    old += pay * P.OLD_SIZE
                    cols.append(pay * P.OLD_SIZE)
            else:
                new += pay * size
                cols.append(pay * size)
        return dict(starts=mk.days[starts], open=open_, old=old, new=new, total=open_ + old + new, cols=np.column_stack(cols), legs=legs)

    def plan_unrelated(self, size, ladder3=None, seed=20261111, draws=20000):
        """The plan's 80 per cent range with each swap not yet sold drawn on its own from its ladder's settlements on
        the record, unrelated to the others and to the open swaps (the hurried range)."""
        rp = self.replay()
        ob = rp["ob"]
        open_ = self.settle(ob, rp["ratio"] * ob.iv.values ** 2).sum(axis=1) * P.OLD_SIZE
        legs = self.plan_legs()
        n_old, n_new = sum(g["ladder"] == P.OLD_MAT for g in legs), sum(g["ladder"] == P.NEW_MAT for g in legs)
        x12 = self.ladder(P.OLD_MAT).settled().pay.values
        x3 = (ladder3 or self.ladder(P.NEW_MAT)).settled().pay.values
        rng = np.random.default_rng(seed)
        tot = (rng.choice(open_, draws) + rng.choice(x12, (draws, n_old)).sum(axis=1) * P.OLD_SIZE
               + rng.choice(x3, (draws, n_new)).sum(axis=1) * size)
        return float(np.percentile(tot, 10)), float(np.percentile(tot, 90))

    # ------------------------------------------------------------------ the calendar of a new ladder
    def new_calendar(self, mat, year=P.PLAN_YEAR):
        L = SW.Ladder(self.mk, mat, start=pd.Timestamp(P.FIRST_NEW[0], P.FIRST_NEW[1], 1), last_sale=pd.Timestamp(year, 12, 31))
        t = L.t[["sale", "expiry", "n"]].copy()
        t["in_year"] = t.expiry.dt.year == year
        return t

    # ------------------------------------------------------------------ everything
    def run(self):
        mk, R = self.mk, {}
        # ---- R1 and R2: the open book
        ob = self.open_book()
        R["open"] = ob
        R["book_value"] = {"total variance (the golden)": float(ob.mark.sum() * P.OLD_SIZE)}
        for nm, kw in (("linear in volatility", dict(how="vol")), ("nearest published term", dict(how="nearest"))):
            R["book_value"][nm] = float(self.open_book(**kw).mark.sum() * P.OLD_SIZE)
        R["book_value_hurried"] = {
            "each swap at the 1-year index": float(self.open_book(remaining="original").mark.sum() * P.OLD_SIZE),
            "each swap at the 30-day index": float(self.open_book(remaining="vix").mark.sum() * P.OLD_SIZE),
            "the statements' total at the month end": float(self.book.val[self.book.val.date == P.STATEMENT].mtm.sum()),
        }
        st = self.open_book(P.STATEMENT)
        R["statement_acc"] = {str(s.date()): float(v) for s, v in zip(st.sale, st.acc_vol)}
        # ---- R3: the new ladder on the record
        R["ladder"] = {m: self.ladder_figs(m) for m in SW.MATURITIES if m != 1}
        R["ladder_rivals"] = {rb: self.ladder_figs(P.NEW_MAT, rb) for rb in REBUILDS}
        R["ladder_hurried"] = {"its index's own history": self.ladder_figs(P.NEW_MAT, "none")}
        for meth in ("30-day index as it stands", "30-day index times the average ratio", "regression on the 30-day index alone"):
            R["ladder_hurried"][meth] = self.ladder_figs(P.NEW_MAT, ladder=self.proxy_ladder(P.NEW_MAT, meth))
        c = SW.calibration(mk, P.NEW_MAT, (30, 184, 365))
        c2 = SW.calibration(mk, P.NEW_MAT, (30, 365))
        ov = mk.idx[["VIX", "VIX3M"]].dropna()
        hot = ov.VIX > P.HOT
        R["rebuild"] = dict(first_published=str(mk.idx.VIX3M.dropna().index[0].date()), overlap_days=int(c["n"]), hot_days=int(c["n_hot"]),
                            rmse=c["rmse"], rmse_hot=c["rmse_hot"], bias_hot=c["bias_hot"], coef=[float(v) for v in c["coef"]],
                            rmse_1y=c2["rmse"], ratio_all=float((ov.VIX3M / ov.VIX).mean()), ratio_hot=float((ov.VIX3M / ov.VIX)[hot].mean()),
                            six_first=str(mk.idx.VIX6M.dropna().index[0].date()), one_first=str(mk.idx.VIX1Y.dropna().index[0].date()),
                            nine_first=str(mk.idx.VIX9D.dropna().index[0].date()))
        # the one-index stand-ins on the same days: how they look on the whole overlap, and on its stressed days
        pf = self.proxy_fit(P.NEW_MAT)
        prox = {}
        for meth in PROXIES:
            err = self.proxy_value(P.NEW_MAT, meth, pf["ov"].VIX.values) - pf["ov"].VIX3M.values
            prox[meth] = dict(rmse=float(np.sqrt((err ** 2).mean())), bias_hot=float(err[pf["hot"]].mean()),
                              rmse_hot=float(np.sqrt((err[pf["hot"]] ** 2).mean())))
        R["rebuild"].update(proxy_r2=pf["r2"], proxy_rmse=pf["rmse"], proxy_coef=[float(v) for v in pf["b"]], proxies=prox)
        # against the index's published closes before the Cboe download begins (public, held outside the pack)
        act = mk.actual3m()
        both = pd.concat([mk.idx.VIX3M, act], axis=1).dropna()
        t3 = self.ladder(P.NEW_MAT).t
        gap = t3[(t3.how == "rebuilt") & act.reindex(t3.sale).notna().values]
        a = act[gap.sale].values
        cmp_ = {rb: float(np.abs(self.ladder(P.NEW_MAT, rb).t.loc[gap.index, "k"].values - a).mean()) for rb in REBUILDS if rb != "actual"}
        bias = {meth: float((self.proxy_ladder(P.NEW_MAT, meth).t.loc[gap.index, "k"].values - a).mean()) for meth in PROXIES}
        stress = gap[mk.idx.VIX[gap.sale].values > P.HOT]
        R["against_actual"] = dict(
            first=str(act.dropna().index[0].date()), overlap_days=int(len(both)), max_diff=float((both.iloc[:, 0] - both.iloc[:, 1]).abs().max()),
            sale_dates=int(len(gap)), mean_abs=cmp_, proxy_bias=bias,
            stressed=[dict(sale=str(s.date()), actual=float(act[s]), calibrated=float(self.ladder(P.NEW_MAT).t.loc[i, "k"]),
                           variance=float(self.ladder(P.NEW_MAT, "variance").t.loc[i, "k"]),
                           proxy=float(self.proxy_ladder(P.NEW_MAT, CAREFUL_PROXY).t.loc[i, "k"])) for i, s in zip(stress.index, stress.sale)])
        # ---- R4: the standing ladder's collateral on the record
        m12 = self.marks(P.OLD_MAT)
        R["old_peak"] = {nm: dict(peak=float(-self.marks(P.OLD_MAT, "calibrated", nm).min() * P.OLD_SIZE), day=str(self.marks(P.OLD_MAT, "calibrated", nm).idxmin().date()))
                         for nm in MARKS}
        for nm, kw in (("rebuilt terms in the gap", dict(rebuilt_terms=True)), ("published 3-month closes in the gap", dict(actual_terms=True))):
            mm = self.marks(P.OLD_MAT, "calibrated", "total variance", **kw)
            R["old_peak"][nm] = dict(peak=float(-mm.min() * P.OLD_SIZE), day=str(mm.idxmin().date()))
        L12 = self.ladder(P.OLD_MAT)
        R["old_peak_hurried"] = {
            "each swap at the 1-year index": float(-L12.marks(remaining="original")[0].min() * P.OLD_SIZE),
            "each swap at the 30-day index": float(-L12.marks(remaining="vix")[0].min() * P.OLD_SIZE),
            "no cap in the mark": float(-L12.marks(cap_in_mark=False)[0].min() * P.OLD_SIZE),
            "its worst calendar year of settlements": float(-L12.by_year().min() * P.OLD_SIZE),
            "the sleeve's own ledger": float(self.book.ledger.groupby("date").posted.sum().max()),
        }
        R["old_episodes"] = {str(y): dict(peak=float(-m12[str(y)].min() * P.OLD_SIZE), day=str(m12[str(y)].idxmin().date())) for y in (2008, 2020)}
        R["old_worst_year"] = dict(year=int(L12.by_year().idxmin()), loss=float(-L12.by_year().min() * P.OLD_SIZE))
        # ---- R5 and R6: the largest new ladder
        for tag, mat in (("size_new", P.NEW_MAT), ("size_alt", P.ALT_MAT)):
            R[tag] = self.room(mat)
            riv, binds = {}, set()
            for rb in REBUILDS:
                for nm in MARKS:
                    r = self.room(mat, rb, nm)
                    riv["%s strikes, %s marks" % (rb, nm)] = r["raw"]
                    binds.add((r["limit"], r["when"]))
            for nm, rb, kw in (("calibrated strikes, rebuilt terms in the gap", "calibrated", dict(rebuilt_terms=True)),
                               ("published 3-month closes for strikes and terms in the gap", "actual", dict(actual_terms=True))):
                r = self.room(mat, rb, **kw)
                riv[nm] = r["raw"]
                binds.add((r["limit"], r["when"]))
            R[tag + "_rivals"] = riv
            R[tag + "_binds"] = sorted(binds)
            L = self.ladder(mat)
            hur = {
                "its index's own history": self.room(mat, "none")["raw"],
                "marks at each swap's own index": self._room_marks(mat, dict(remaining="original")),
                "marks at the 30-day index": self._room_marks(mat, dict(remaining="vix")),
                "no cap in the mark": self._room_marks(mat, dict(cap_in_mark=False)),
                "the new ladder on its own": self.room(mat, with_old=False)["raw"],
                "the settlement limit alone": self.room(mat, use_c=False)["raw"],
                "its index's own history, marks at each swap's own index": self._room_marks(mat, dict(remaining="original"), rebuild="none"),
                "its index's own history, the new ladder on its own": self.room(mat, "none", with_old=False)["raw"],
            }
            if mat == P.NEW_MAT:
                for meth in ("30-day index as it stands", "30-day index times the average ratio", "regression on the 30-day index alone"):
                    hur["missing strikes from the " + meth] = self.room(mat, ladder=self.proxy_ladder(mat, meth))["raw"]
            R[tag + "_hurried"] = hur
        R["proposal"] = self.usage(P.NEW_MAT, P.PROPOSED)
        R["at_size"] = self.usage(P.NEW_MAT, R["size_new"]["size"])
        R["alt_at_size"] = self.usage(P.ALT_MAT, R["size_alt"]["size"])
        R["room_sensitivity"] = {"%.1f" % lc: self.room(P.NEW_MAT, lc=lc * P.REF_ASSETS / 100.0) | {"pct": lc} for lc in (2.5, 3.0, 3.5, 4.0)}
        R["pooled"] = dict(one_month=self._pooled_ratio(21, 30), twelve_month=self._pooled_ratio(252, 365))
        # ---- R7 and R9: the open swaps that expire in the plan year
        rp = self.replay()
        R["replay"] = rp
        R["expect"], R["expect_hurried"] = self.expectations(rp)
        R["range"], R["range_hurried"], R["range_stats"] = self.ranges(rp)
        # ---- R8: the new ladder's first year
        cal = self.new_calendar(P.NEW_MAT)
        R["new_calendar"] = cal
        R["alt_calendar"] = self.new_calendar(P.ALT_MAT)
        # ---- how well the record pins each ladder's average settlement per sale
        R["avg_range"] = {}
        for mat in (P.NEW_MAT, P.OLD_MAT):
            sound, hur, st = self.avg_ranges(mat)
            R["avg_range"][mat] = dict(sound=sound, hurried=hur, stats=st, golden="circular blocks of %d sales" % (2 * mat))
        g3 = R["avg_range"][P.NEW_MAT]["golden"]
        R["avg_range"][P.NEW_MAT]["by_rebuild"] = {rb: self.avg_ranges(P.NEW_MAT, rb)[0][g3] for rb in REBUILDS}
        cs, ch, cst = self.avg_ranges(P.NEW_MAT, ladder=self.proxy_ladder(P.NEW_MAT, CAREFUL_PROXY))
        R["avg_range"][P.NEW_MAT]["proxy"] = dict(sound=cs, hurried=ch, stats=cst)
        # ---- the plan year: every settlement that falls in it, from the same start dates
        size = R["size_new"]["size"]
        a3, a12 = R["ladder"][P.NEW_MAT]["avg_per_sale"], R["ladder"][P.OLD_MAT]["avg_per_sale"]
        pl = self.plan(size)
        n_old = sum(g["ladder"] == P.OLD_MAT for g in pl["legs"])
        n_new = sum(g["ladder"] == P.NEW_MAT for g in pl["legs"])
        q = lambda v: (float(np.percentile(v, 10)), float(np.percentile(v, 90)))
        lo_size = math.floor(min(R["size_new_rivals"].values()) / 1000.0) * 1000
        hi_size = math.ceil(max(R["size_new_rivals"].values()) / 1000.0) * 1000
        gold_open = R["expect"]["start dates replayed, ratio to implied (the golden)"] * P.OLD_SIZE
        sound = {"every settlement from the same start dates (the golden)": q(pl["total"]),
                 "open swaps on realised levels": q(self.plan(size, basis="level")["total"]),
                 "every fifth start date": q(pl["total"][::5]),
                 "total-variance strikes": q(self.plan(size, "variance")["total"]),
                 "published 3-month closes in the gap": q(self.plan(size, "actual")["total"]),
                 "the size at the low end of its band": q(self.plan(lo_size)["total"]),
                 "the size at the high end of its band": q(self.plan(hi_size)["total"])}
        rng = np.random.default_rng(20261110)
        ind = sum(rng.permutation(pl["cols"][:, j]) for j in range(pl["cols"].shape[1]))
        parts = [pl["open"], pl["old"], pl["new"]]
        sd_q = float(np.sqrt(sum(p.var() for p in parts)))
        no_old = self.plan(size, with_unsold_old=False)["total"]
        hurried = {"settlements drawn independently": q(ind),
                   "unsold swaps drawn one by one from their ladder's record": self.plan_unrelated(size),
                   "each part's spread added in quadrature": (float(pl["total"].mean() - Z80 * sd_q), float(pl["total"].mean() + Z80 * sd_q)),
                   "each part's own range, added": (sum(q(p)[0] for p in parts), sum(q(p)[1] for p in parts)),
                   "the standing ladder's unsold sales left out": q(no_old)}
        R["plan"] = dict(size=size, n_old=n_old, n_new=n_new, legs=pl["legs"], open_expected=gold_open, old_unsold=n_old * a12 * P.OLD_SIZE,
                         twelve=gold_open + n_old * a12 * P.OLD_SIZE, three=n_new * size * a3,
                         total=gold_open + n_old * a12 * P.OLD_SIZE + n_new * size * a3, sound=sound, hurried=hurried,
                         stats=dict(n_starts=int(len(pl["total"])), first_start=str(pl["starts"][0].date()), last_start=str(pl["starts"][-1].date()),
                                    replay_mean=float(pl["total"].mean()), minimum=float(pl["total"].min()), worst_start=str(pl["starts"][int(pl["total"].argmin())].date()),
                                    share_below_zero=float((pl["total"] < 0).mean()),
                                    corr_open_new=float(np.corrcoef(pl["open"], pl["new"])[0, 1])))
        # ---- the sleeve's collateral day by day at the size
        v_old, v_new = m12 * P.OLD_SIZE, self.marks(P.NEW_MAT) * size
        days = v_old.index[v_old.index >= MK.RECORD_START]           # every day of the record, from the first close of 2007
        R["daily"] = pd.DataFrame(dict(date=days, old=v_old[days].values, new=v_new[days].values))
        R["daily"]["sleeve"] = R["daily"].old + R["daily"].new
        R["daily"]["collateral"] = np.maximum(0.0, -R["daily"].sleeve)
        return R

    def _room_marks(self, mat, kw, rebuild="calibrated"):
        """The room when both ladders are marked a hurried way."""
        Ln, Lo = self.ladder(mat, rebuild), self.ladder(P.OLD_MAT)
        mn, mo = Ln.marks(**kw)[0], Lo.marks(**kw)[0]
        yn, yo = Ln.by_year(), Lo.by_year()
        best = min(((P.LIM_SETTLE + float(yo.get(y, 0.0)) * P.OLD_SIZE) / -yn[y]) for y in yn.index if yn[y] < 0)
        neg = mn < 0
        return float(min(best, ((P.LIM_COLL + mo[neg] * P.OLD_SIZE) / -mn[neg]).min()))


if __name__ == "__main__":
    import time
    t0 = time.time()
    A = Analysis()
    R = A.run()
    pd.set_option("display.width", 250)
    print("built in %.0fs" % (time.time() - t0))
    ob = R["open"]
    print(ob[["sale", "expiry", "k", "n_e", "n_r", "acc_vol", "iv", "mark"]].round(2).to_string())
    print("book value", {k: round(v) for k, v in R["book_value"].items()}, "| hurried", {k: round(v) for k, v in R["book_value_hurried"].items()})
    for m, f in R["ladder"].items():
        print("ladder %2dM: avg per sale %.3f worst %.1f (%d) settled %d rebuilt %d" % (m, f["avg_per_sale"], f["worst"], f["worst_year"], f["n_settled"], f["n_rebuilt"]))
    print("3M rivals", {k: (round(v["avg_per_sale"], 3), round(v["worst"], 1)) for k, v in R["ladder_rivals"].items()})
    print("3M hurried", {k: (round(v["avg_per_sale"], 3), round(v["worst"], 1), v["worst_year"]) for k, v in R["ladder_hurried"].items()})
    print("rebuild", R["rebuild"])
    print("old peak", R["old_peak"], "\n  hurried", {k: round(v) for k, v in R["old_peak_hurried"].items()}, "\n  episodes", R["old_episodes"], R["old_worst_year"])
    for tag in ("size_new", "size_alt"):
        print(tag, R[tag])
        rv = R[tag + "_rivals"]
        print("   rivals min %.1f max %.1f" % (min(rv.values()), max(rv.values())), {k: round(v / 1000, 1) for k, v in rv.items()})
        print("   hurried", {k: round(v / 1000, 1) for k, v in R[tag + "_hurried"].items()})
    print("proposal", R["proposal"], "\nat size", R["at_size"], "\nalt at size", R["alt_at_size"])
    print("sensitivity", R["room_sensitivity"])
    print("expect", {k: round(v, 1) for k, v in R["expect"].items()})
    print("expect hurried", {k: round(v, 1) for k, v in R["expect_hurried"].items()})
    print("range", {k: (round(a, 1), round(b, 1)) for k, (a, b) in R["range"].items()})
    print("range hurried", {k: (round(a, 1), round(b, 1)) for k, (a, b) in R["range_hurried"].items()})
    print("range stats", {k: v for k, v in R["range_stats"].items() if k != "per_swap_mean"})
    print(R["new_calendar"].to_string())
    print("daily rows", len(R["daily"]), "peak", R["daily"].collateral.max(), R["daily"].loc[R["daily"].collateral.idxmax(), "date"].date())
    b = A.book
    print("book: confirmations %d, open %d, valuation rows %d, ledger rows %d, own peak %.0f" % (len(b.trades), (~b.trades.settled).sum(), len(b.val), len(b.ledger), b.ledger.groupby("date").posted.sum().max()))
