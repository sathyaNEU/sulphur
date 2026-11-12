"""task9: the golden analysis and the hurried routes, computed from the pack alone (record.py), never from the
simulator. Every figure the answer blocks state comes from here.

  R1  the ring's loss at sort on wafers sorted 1 April to 31 August: points of mean wafer sort yield, good die by product
  R2  each candidate cause's share of that loss: the conditioner disk's wear, the pad's life on top of it, the retaining
      ring, deposition chamber DEP-3, scanner SC-4 and the chambers' RF hours
  R3  the units final test lost to the ring on the lots it finished from 1 April to 31 August, by product
  R4  each unit's onset (wafers of its disk's own use) and the climb after it (outer-band fail rate per 1,000 wafers) on
      the disks the units will be fitted with from September
  REC each unit's count for the disk once Rev G takes it out of the full PM, the ring costed at sort and at final test
  R5  the yearly saving of those counts against Rev F as it stands

The ring's loss on a wafer is its outer-band fails above what the band fails with no ring: the wafer's own interior
fail rate plus the band's normal fallout, the band's excess on wafers whose disk has not reached its onset. Each disk
is read on its own supplier lot (the serial the PM entry fitted, in the receipt's serial range): the lots wear at
their own rates, and the disks stores will issue from September are the lot every unit runs now.
"""
import os
import sqlite3

import numpy as np
import pandas as pd
import yaml

import pack as PK
import record as RC

WIN = ("2026-04-01", "2026-09-01")
SUMMER = "2026-06-01"
REV_F = pd.Timestamp("2026-04-02")
GRID = np.arange(300, 2001, 5)
UNITS = ["PU-1", "PU-2", "PU-3", "PU-4"]
PAD_LIFE = 600.0
CAUSES = ["disk", "pad", "ring", "dep3", "sc4", "rf"]
RIVALS = ("dep3", "sc4", "rf100")
REV_F_DISK = 2800
AGES = np.arange(1, 6001)
U0_GRID = np.round(np.arange(0.20, 0.901, 0.01), 2)
US_GRID = np.round(np.arange(0.06, 0.801, 0.02), 2)


def hinge_fit(g, dose="disk", grid=GRID, weight=True, pad=True, ring=False, extra=()):
    """Weighted least squares of the outer band's excess over the interior on a hinge in the dose, profiled over the
    onset; the pad's life multiplies the slope."""
    x = g[dose].values.astype(float)
    y = g.y.values
    wt = g.tested_band.values.astype(float) if weight else np.ones(len(g))
    sw = np.sqrt(wt)
    tail = ([g.ring.values / 1000.0] if ring else []) + [g[c].values.astype(float) for c in extra]
    best = None
    for w0 in grid:
        h = np.maximum(0.0, x - w0)
        X = np.column_stack([np.ones(len(g)), h] + ([h * g.pad.values / PAD_LIFE] if pad else []) + tail)
        b, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
        sse = float(np.sum(wt * (y - X @ b) ** 2))
        if best is None or sse < best[0]:
            best = (sse, float(w0), b)
    sse, w0, b = best
    out = dict(w0=w0, r0=float(b[0]), beta=float(b[1]), sse=sse, gamma=0.0, n=int(len(g)))
    k = 2
    if pad:
        out["gamma"] = float(b[2] / b[1]) if b[1] > 0 else 0.0
        k = 3
    if ring:
        out["ring"] = float(b[k])
        k += 1
    for c in extra:
        out[c] = float(b[k])
        k += 1
    return out


def linear_fit(g, dose="disk"):
    """A dose taken straight from zero."""
    x = g[dose].values.astype(float)
    wt = g.tested_band.values.astype(float)
    X = np.column_stack([np.ones(len(g)), x])
    sw = np.sqrt(wt)
    b, *_ = np.linalg.lstsq(X * sw[:, None], g.y.values * sw, rcond=None)
    return dict(w0=0.0, r0=float(b[0]), beta=float(b[1]), gamma=0.0)


def poisson_identity(X, y, iters=60):
    """Poisson regression with an identity link (the counts add over the lot's die): iteratively reweighted least
    squares, coefficients held at or above zero."""
    b = np.linalg.lstsq(X, y, rcond=None)[0].clip(1e-9)
    for _ in range(iters):
        mu = np.maximum(X @ b, 1e-9)
        w = 1.0 / mu
        sw = np.sqrt(w)
        nb = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)[0].clip(0.0)
        if np.max(np.abs(nb - b) / np.maximum(np.abs(b), 1e-12)) < 1e-10:
            b = nb
            break
        b = nb
    mu = np.maximum(X @ b, 1e-9)
    return b, float(np.sum(mu - y * np.log(mu)))


def ramp(u, u0, us):
    return np.clip((u - u0) / us, 0.0, 1.0)


class Analysis:
    def __init__(self, tgt):
        self.tgt = tgt
        R = RC.Record(tgt)
        self.R = R
        d = R.d.copy()
        d["y"] = d.f_band - d.f_in
        d["win"] = (d.sort_ts >= WIN[0]) & (d.sort_ts < WIN[1])
        d["q1"] = d.sort_ts < WIN[0]
        # the units pair by the downforce recipe their polish record carries
        df = R.fdc.groupby("unit").downforce_psi.median()
        hi = sorted(u for u in UNITS if df[u] > df.median())
        self.pairs = {"high": hi, "low": sorted(u for u in UNITS if u not in hi)}
        self.pair_of = {u: p for p, us in self.pairs.items() for u in us}
        d["pair"] = d.unit.map(self.pair_of)
        rf = pd.read_csv(os.path.join(tgt, PK.F["rf"]))
        d = d.merge(rf.rename(columns={"chamber_id": "dep", "date": "dep_day"})[["dep", "dep_day", "rf_hours_since_clean"]],
                    on=["dep", "dep_day"], how="left")
        d["dep3"] = (d.dep == "DEP-3").astype(float)
        d["sc4"] = (d.m1_scanner == "SC-4").astype(float)
        d["rf100"] = d.rf_hours_since_clean.fillna(d.rf_hours_since_clean.mean()) / 100.0
        d["gb"] = d.tested_band * (1.0 - d.f_band)          # the outer band's good die
        self.d = d
        self.costs = yaml.safe_load(open(os.path.join(tgt, PK.F["costs"])))
        cz = self.costs
        self.value = {p: float(v["value_per_good_die"]) for p, v in cz["die"].items()}
        self.assy = {p: float(v["assembly_and_test_per_unit"]) for p, v in cz["die"].items()}
        self.n_band = d.groupby("product").tested_band.median().to_dict()
        self.allin = {k: float(v) for k, v in cz["all_in"].items()}
        self.disk_price = float(cz["parts"]["conditioner_disk"])
        self.mix = {p: float(v) for p, v in cz["volume"]["product_mix"].items()}
        self.vol = {u: float(v) for u, v in cz["volume"]["wafers_per_year_by_unit"].items()}
        self.f_in_bar = float(np.average(d.f_in, weights=d.tested_band))
        self.lots()
        self.fit()
        self.r1()
        self.causes()
        self.final_test()
        self.counts()
        self.saving()

    # ---- the disk lots: every unit's current disk and the stock left on the shelf come from one lot
    def lots(self):
        d, R = self.d, self.R
        last = d.sort_values("polish_ts").groupby("unit").disk_lot.last()
        used = R.events.dropna(subset=["disk_serial"]).groupby(R.events.disk_serial.map(R.lot_of)).disk_serial.max()
        left = {r.supplier_lot: int(r.serial_last - used.get(r.supplier_lot, r.serial_first - 1)) for r in R.disk_lots.itertuples()}
        self.stock_left = left
        cur = set(last.values)
        assert len(cur) == 1, cur
        self.fwd_lot = cur.pop()
        assert all(v <= 0 for k, v in left.items() if k != self.fwd_lot), left
        assert d.disk_lot.notna().all()
        self.lot_names = sorted(d.disk_lot.unique())
        d["fwd"] = d.disk_lot == self.fwd_lot

    # ---- the dose-response by downforce pair and disk lot (golden), and the shortcuts' fits
    def fit(self):
        d = self.d
        self.gfit = {(p, L): hinge_fit(d[(d.pair == p) & (d.disk_lot == L)]) for p in self.pairs for L in self.lot_names}
        self.fwd_fit = {p: self.gfit[(p, self.fwd_lot)] for p in self.pairs}
        self.onset = {u: self.fwd_fit[self.pair_of[u]]["w0"] for u in UNITS}
        self.slope = {u: self.fwd_fit[self.pair_of[u]]["beta"] * 1000 for u in UNITS}   # band fail rate per 1,000 wafers
        key = list(zip(d.pair, d.disk_lot))
        d["r0"] = [self.gfit[k]["r0"] for k in key]
        d["w0g"] = [self.gfit[k]["w0"] for k in key]
        d["wear"] = d.disk / d.w0g                                   # each disk's use as a share of its own lot's onset
        self.pooled_fit = {p: hinge_fit(d[d.pair == p]) for p in self.pairs}
        self.old_fit = {p: hinge_fit(d[(d.pair == p) & ~d.fwd]) for p in self.pairs}
        self.unit_fit = {u: hinge_fit(d[d.unit == u]) for u in UNITS}
        self.unit_fwd_fit = {u: hinge_fit(d[(d.unit == u) & d.fwd]) for u in UNITS}
        self.fleet_fit = hinge_fit(d)

    def excess(self, a, f, padbar=PAD_LIFE / 2):
        return f["beta"] * np.maximum(0.0, np.asarray(a, float) - f["w0"]) * (1 + f.get("gamma", 0.0) * padbar / PAD_LIFE)

    # ---- R1: the loss at sort on every sorted wafer in the window
    def r1(self):
        d = self.d
        d["ring_die"] = d.tested_band * (d.y - d.r0)
        w = d[d.win]
        self.n_win = int(len(w))
        self.R1 = float(np.mean(w.ring_die / w.gross) * 100)
        self.R1_die = {p: float(v) for p, v in w.groupby("product").ring_die.sum().items()}
        self.R1_usd = float(sum(self.R1_die[p] * self.value[p] for p in self.R1_die))
        q = d[d.q1]
        self.R1_q1 = float(np.mean(q.ring_die / q.gross) * 100)
        lab = w.adc_label == "EDGE_RING"
        self.unflagged_share = float(w.ring_die[~lab].sum() / w.ring_die.sum())
        self.R1_fwd_share = float(w.ring_die[w.fwd].sum() / w.ring_die.sum())

    # ---- R2: every candidate in one model per pair and lot
    def cause_shares(self, fits, groups):
        d, w = self.d, self.d[self.d.win]
        contrib = {k: 0.0 for k in CAUSES}
        for key, f in fits.items():
            gw = w[groups(w) == key]
            if not len(gw):
                continue
            h = np.maximum(0.0, gw.disk.values - f["w0"])
            sc = gw.tested_band.values / gw.gross.values * 100 / len(w)
            contrib["disk"] += float(np.sum(f["beta"] * h * sc))
            contrib["pad"] += float(np.sum(f["beta"] * f["gamma"] * h * gw.pad.values / PAD_LIFE * sc))
            contrib["ring"] += float(np.sum(f.get("ring", 0.0) * gw.ring.values / 1000.0 * sc))
            contrib["dep3"] += float(np.sum(f.get("dep3", 0.0) * gw.dep3.values * sc))
            contrib["sc4"] += float(np.sum(f.get("sc4", 0.0) * gw.sc4.values * sc))
            contrib["rf"] += float(np.sum(f.get("rf100", 0.0) * (gw.rf100.values - d.rf100.min()) * sc))
        tot = contrib["disk"] + contrib["pad"]
        return {k: v / tot for k, v in contrib.items()}

    def causes(self):
        d = self.d
        self.cfit = {"%s|%s" % (p, L): hinge_fit(d[(d.pair == p) & (d.disk_lot == L)], ring=True, extra=RIVALS)
                     for p in self.pairs for L in self.lot_names}
        self.R2 = self.cause_shares(self.cfit, lambda g: g.pair + "|" + g.disk_lot)
        self.ring_swaps = self.swap_steps()

    def swap_steps(self, span=300):
        """The step at each ring-only swap, the disk running on: the no-ring model's mean residual over the next span
        wafers on the unit less its mean over the last span."""
        d, ev = self.d, self.R.events
        fit = d.r0 + [self.excess(a, self.gfit[k], padbar=pd_) for a, k, pd_ in zip(d.disk, zip(d.pair, d.disk_lot), d.pad)]
        d["resid"] = d.y - fit
        out = []
        for _, e in ev[(ev.event_class == "UNSCHED") & ev.parts.map(lambda s: s == {"ring"})].iterrows():
            g = d[(d.unit == e.unit) & (d.platen >= e.counter - span) & (d.platen < e.counter + span)]
            before, after = g[g.platen < e.counter], g[g.platen >= e.counter]
            if len(before) < span // 2 or len(after) < span // 2:
                continue
            step = np.average(after.resid, weights=after.tested_band) - np.average(before.resid, weights=before.tested_band)
            out.append((e.unit, str(e.event_ts)[:10], float(step)))
        return out

    # ---- R3: final test's lots, each lot's burn-in failures against its wafers' outer-band good die and their wear
    def ft_design(self, clock="wear"):
        ft = self.R.ft
        idx = {l: i for i, l in enumerate(ft.lot_id)}
        g = self.d[self.d.lot_id.isin(idx)]
        self._ft_li = g.lot_id.map(idx).values
        self._ft_gb = g.gb.values
        self._ft_clock = g[clock].values.astype(float)
        self._ft_ring = np.clip(g.ring_die.values, 0, None)
        return ft

    def ft_fit(self, clock="wear", u0s=U0_GRID, uss=US_GRID, split=None):
        """Burn-in failures on a lot: a base rate on its units plus a share of its wafers' outer-band good die that rises
        over a span of the clock and levels off; the span profiled on a grid, the rates by Poisson regression (with
        split, each group of wafers its own level)."""
        ft = self.ft_design(clock)
        U = ft.units_in.values.astype(float)
        Y = ft.burnin_fail.values.astype(float)
        n = len(ft)
        g = self.d[self.d.lot_id.isin(set(ft.lot_id))]
        groups = [np.ones(len(g), bool)] if split is None else [(g[split] == k).values for k in sorted(g[split].unique())]
        best = None
        for u0 in u0s:
            for us in uss:
                rr = self._ft_gb * ramp(self._ft_clock, u0, us)
                exs = [np.bincount(self._ft_li[m], weights=rr[m], minlength=n) for m in groups]
                b, nll = poisson_identity(np.column_stack([U] + exs), Y)
                if best is None or nll < best[0]:
                    best = (nll, float(u0), float(us), b, exs)
        nll, u0, us, b, exs = best
        out = dict(base=float(b[0]), L=float(b[1]), u0=u0, us=us, nll=nll, latent=sum(bk * e for bk, e in zip(b[1:], exs)))
        if split is not None:
            out["L_by"] = {k: float(bk) for k, bk in zip(sorted(g[split].unique()), b[1:])}
        return out

    def ft_by_product(self, per_lot):
        ft = self.R.ft
        prod = self.d.drop_duplicates("lot_id").set_index("lot_id")["product"]
        win = ((ft.ft_date >= WIN[0]) & (ft.ft_date < WIN[1])).values
        s = pd.Series(np.asarray(per_lot)[win], index=ft.lot_id.values[win])
        return {p: float(v) for p, v in s.groupby(prod.reindex(s.index).values).sum().items()}

    def final_test(self):
        self.ft = self.ft_fit("wear")
        ft = self.R.ft
        self.R3 = self.ft_by_product(self.ft["latent"])
        self.R3_observed = self.ft_by_product(ft.burnin_fail.values - self.ft["base"] * ft.units_in.values)
        self.R3_usd = float(sum(v * (self.value[p] + self.assy[p]) for p, v in self.R3.items()))
        win = ((ft.ft_date >= WIN[0]) & (ft.ft_date < WIN[1])).values
        self.n_ft_win = int(win.sum())

    # ---- REC: each unit's count, R5: the saving
    def loss_curve(self, f, ftm="golden", prop=0.0, ages=AGES):
        """Dollars the ring costs per wafer at each wafer of the disk's own use: good die at sort, and the outer band's
        good die that final test scraps, each at its die value plus assembly and test."""
        ft = self.ft if ftm == "golden" else ftm
        ex = self.excess(ages, f)
        out = np.zeros(len(ages))
        for p, m in self.mix.items():
            nb = self.n_band[p]
            out += m * nb * self.value[p] * ex
            if ft is not None:
                lam = ft["L"] * ramp(ages / f["w0"], ft["u0"], ft["us"]) if ft.get("clock", "wear") == "wear" else \
                    ft["L"] * ramp(ages, ft["u0"], ft["us"])
                good = np.clip(1.0 - self.f_in_bar - f["r0"] - ex, 0.0, None)
                out += m * nb * good * lam * (self.value[p] + self.assy[p])
            if prop:
                out += m * nb * ex * prop * (self.value[p] + self.assy[p])
        return out

    def tstar(self, lc, c=None):
        c = self.allin["disk_change"] if c is None else c
        cpw = (c + np.cumsum(lc)) / AGES[:len(lc)]
        return int(AGES[int(np.argmin(cpw))])

    def counts(self):
        self.curve = {p: self.loss_curve(self.fwd_fit[p]) for p in self.pairs}
        self.REC_pair = {p: self.tstar(self.curve[p]) for p in self.pairs}
        self.REC = {u: self.REC_pair[self.pair_of[u]] for u in UNITS}

    def cpw_g(self, lc, T):
        return (self.allin["disk_change"] + float(np.sum(lc[:T]))) / T

    def yearly(self, lc, T, vol, rev_f_ring=None):
        """Rev F's cost per wafer (its full PM, and the ring over a disk run to the full PM's 2,800 wafers) less Rev G's
        (the full PM less the disk's price, and the disk on its own count T), over a year of the unit's wafers."""
        full = self.allin["full_pm"]
        ring_f = float(np.sum(lc[:REV_F_DISK])) / REV_F_DISK if rev_f_ring is None else rev_f_ring
        rev_f = full / REV_F_DISK + ring_f
        rev_g = (full - self.disk_price) / REV_F_DISK + self.cpw_g(lc, T)
        return (rev_f - rev_g) * vol

    def saving(self):
        self.R5_unit = {u: self.yearly(self.curve[self.pair_of[u]], self.REC[u], self.vol[u]) for u in UNITS}
        self.R5 = float(sum(self.R5_unit.values()))
        self.R5_pair = {p: float(sum(self.R5_unit[u] for u in us)) for p, us in self.pairs.items()}

    # ======================================================================== the hurried routes
    def routes(self):
        d, w = self.d, self.d[self.d.win]
        out = {}
        pts = lambda die, sub: float(np.mean(die / sub.gross) * 100)
        byp = lambda s: {p: float(v) for p, v in s.groupby(w["product"]).sum().items()}
        # R1
        q1 = d[d.q1].y.mean()
        out["R1_q1_baseline"] = pts(w.tested_band * (w.y - q1), w)
        out["R1_die_q1_baseline"] = byp(w.tested_band * (w.y - q1))
        lab = (w.adc_label == "EDGE_RING").values
        out["R1_labels"] = pts(np.where(lab, w.tested_band * w.y, 0.0), w)
        out["R1_die_labels"] = byp(pd.Series(np.where(lab, w.tested_band * w.y, 0.0), index=w.index))
        out["R1_no_rolloff"] = pts(w.tested_band * w.y, w)
        out["R1_die_no_rolloff"] = byp(w.tested_band * w.y)
        r0p = w.pair.map({p: f["r0"] for p, f in self.pooled_fit.items()})
        out["R1_pooled"] = pts(w.tested_band * (w.y - r0p), w)
        out["R1_die_pooled"] = byp(w.tested_band * (w.y - r0p))
        con = sqlite3.connect(os.path.join(self.tgt, PK.F["diemaps"]))
        maps = set(r[0] for r in con.execute("SELECT wafer_id FROM wafer_index"))
        con.close()
        wm = w[w.wafer_id.isin(maps)]
        out["R1_diemap_sample"] = pts(wm.ring_die, wm)
        out["R1_before_after"] = float((d[d.q1].sort_yield.mean() - w.sort_yield.mean()) * 100)
        # R2: one joint regression per pair over every lot, read wafer by wafer; tool commonality
        self.naive = {p: hinge_fit(d[d.pair == p], ring=True, extra=RIVALS) for p in self.pairs}
        out["R2_joint"] = self.cause_shares(self.naive, lambda g: g.pair)
        out["R2_joint_ring_t"] = self.naive_t()
        gaps = {}
        for col, name in (("unit", "unit"), ("dep", "dep"), ("m1_scanner", "scanner")):
            m = w.groupby(col).y.mean()
            for k, v in m.items():
                gaps["%s %s" % (name, k)] = float(v - w.y.mean())
        out["R2_commonality_top"] = sorted(gaps, key=lambda k: -gaps[k])[:4]
        out["R2_commonality"] = {"disk": 0.0, "pad": 0.0, "ring": 0.0, "dep3": float(gaps["dep DEP-3"] / max(w.y.mean(), 1e-9)),
                                 "sc4": float(gaps.get("scanner SC-4", 0.0) / max(w.y.mean(), 1e-9)), "rf": 0.0}
        # R3: burn-in in proportion to the ring's die at sort; a baseline from lots with no ring label, from the first
        # quarter's lots; the same rise and level on the disk's raw use, every lot pooled
        ft = self.ft_design("wear")
        U, Y = ft.units_in.values.astype(float), ft.burnin_fail.values.astype(float)
        rd = np.bincount(self._ft_li, weights=self._ft_ring, minlength=len(ft))
        bp, _ = poisson_identity(np.column_stack([U, rd]), Y)
        self.prop = dict(base=float(bp[0]), k=float(bp[1]))
        out["R3_proportional"] = self.ft_by_product(bp[1] * rd)
        g = d[d.lot_id.isin(set(ft.lot_id))]
        lab_lot = g.groupby("lot_id").adc_label.apply(lambda s: (s == "EDGE_RING").sum()).reindex(ft.lot_id).fillna(0).values
        clean = lab_lot == 0
        base_c = Y[clean].sum() / U[clean].sum()
        out["R3_clean_lot_base"] = self.ft_by_product(Y - base_c * U)
        q1l = (ft.ft_date < WIN[0]).values
        base_q = Y[q1l].sum() / U[q1l].sum()
        out["R3_q1_base"] = self.ft_by_product(Y - base_q * U)
        raw = self.ft_fit("disk", u0s=np.arange(100, 1501, 20), uss=np.arange(50, 1201, 25))
        raw["clock"] = "raw"
        self.ft_raw = raw
        out["R3_raw_age"] = self.ft_by_product(raw["latent"])
        out["R3_none"] = {p: 0.0 for p in self.R3}
        self.ft_design("wear")
        # R4: every lot pooled by pair, the earlier lots, each unit over every lot, the fleet, a dose from zero
        out["R4_pooled"] = {u: (self.pooled_fit[self.pair_of[u]]["w0"], self.pooled_fit[self.pair_of[u]]["beta"] * 1000) for u in UNITS}
        out["R4_old_lots"] = {u: (self.old_fit[self.pair_of[u]]["w0"], self.old_fit[self.pair_of[u]]["beta"] * 1000) for u in UNITS}
        out["R4_unit"] = {u: (self.unit_fit[u]["w0"], self.unit_fit[u]["beta"] * 1000) for u in UNITS}
        out["R4_unit_fwd"] = {u: (self.unit_fwd_fit[u]["w0"], self.unit_fwd_fit[u]["beta"] * 1000) for u in UNITS}
        out["R4_fleet"] = {u: (self.fleet_fit["w0"], self.fleet_fit["beta"] * 1000) for u in UNITS}
        summer = {p: hinge_fit(d[(d.pair == p) & (d.polish_ts >= SUMMER)]) for p in self.pairs}
        out["R4_summer"] = {u: (summer[self.pair_of[u]]["w0"], summer[self.pair_of[u]]["beta"] * 1000) for u in UNITS}
        lin = {p: linear_fit(d[d.pair == p]) for p in self.pairs}
        out["R4_linear"] = {u: (0.0, lin[self.pair_of[u]]["beta"] * 1000) for u in UNITS}
        self.route_fits = dict(pooled=self.pooled_fit, old=self.old_fit, summer=summer, lin=lin)
        # REC: the count on each combination of curve and final-test model
        per = lambda f, **kw: {u: self.tstar(self.loss_curve(f(u), **kw)) for u in UNITS}
        fwd = lambda u: self.fwd_fit[self.pair_of[u]]
        pooled = lambda u: self.pooled_fit[self.pair_of[u]]
        out["REC_sort_only"] = per(fwd, ftm=None)
        out["REC_proportional"] = per(fwd, ftm=None, prop=self.prop["k"])
        out["REC_raw_age_ft"] = per(fwd, ftm=raw)
        out["REC_pooled"] = per(pooled)
        out["REC_pooled_sort_only"] = per(pooled, ftm=None)
        out["REC_pooled_proportional"] = per(pooled, ftm=None, prop=self.prop["k"])
        out["REC_old_lots"] = per(lambda u: self.old_fit[self.pair_of[u]])
        out["REC_summer"] = per(lambda u: summer[self.pair_of[u]])
        out["REC_unit_fwd"] = per(lambda u: self.unit_fwd_fit[u])
        out["REC_fleet_sort_only"] = per(lambda u: self.fleet_fit, ftm=None)
        out["REC_linear"] = per(lambda u: lin[self.pair_of[u]], ftm=None)
        # R5: Rev F priced on the summer's own loss rate; on the shortcuts' curves and counts
        sm = d[d.sort_ts >= SUMMER]
        usd = sm.ring_die * sm["product"].map(self.value)
        rate = usd.groupby(sm.unit).sum() / sm.groupby("unit").size()
        out["R5_summer_rate"] = float(sum(self.yearly(self.curve[self.pair_of[u]], self.REC[u], self.vol[u], rev_f_ring=float(rate[u]))
                                          for u in UNITS))
        sav = lambda f, T, **kw: float(sum(self.yearly(self.loss_curve(f(u), **kw), T[u], self.vol[u]) for u in UNITS))
        out["R5_sort_only"] = sav(fwd, out["REC_sort_only"], ftm=None)
        out["R5_proportional"] = sav(fwd, out["REC_proportional"], ftm=None, prop=self.prop["k"])
        out["R5_pooled"] = sav(pooled, out["REC_pooled"])
        out["R5_pooled_sort_only"] = sav(pooled, out["REC_pooled_sort_only"], ftm=None)
        out["R5_pooled_proportional"] = sav(pooled, out["REC_pooled_proportional"], ftm=None, prop=self.prop["k"])
        sh = d[d.polish_ts >= SUMMER].unit.value_counts(normalize=True)
        out["R5_summer_share"] = float(sum(self.yearly(self.curve[self.pair_of[u]], self.REC[u], sh[u] * sum(self.vol.values()))
                                           for u in UNITS))
        self.out = out
        return out

    def naive_t(self):
        """The retaining ring's coefficient over its standard error with the wafers taken as independent, and with the
        disk lives as the units that vary."""
        d = self.d
        res = {}
        for p in self.pairs:
            g = d[d.pair == p]
            f = self.naive[p]
            h = np.maximum(0.0, g.disk.values - f["w0"])
            X = np.column_stack([np.ones(len(g)), h, h * g.pad.values / PAD_LIFE, g.ring.values / 1000.0] +
                                [g[c].values.astype(float) for c in RIVALS])
            wt = g.tested_band.values.astype(float)
            sw = np.sqrt(wt)
            Xw, yw = X * sw[:, None], g.y.values * sw
            b, *_ = np.linalg.lstsq(Xw, yw, rcond=None)
            e = yw - Xw @ b
            XtX = np.linalg.pinv(Xw.T @ Xw)
            se_iid = np.sqrt(np.diag(XtX) * np.sum(e ** 2) / (len(g) - X.shape[1]))
            meat = np.zeros((X.shape[1], X.shape[1]))
            for _, ix in g.groupby("disk_life").indices.items():
                s = Xw[ix].T @ e[ix]
                meat += np.outer(s, s)
            se_cl = np.sqrt(np.diag(XtX @ meat @ XtX))
            res[p] = (float(b[3] / se_iid[3]), float(b[3] / se_cl[3]))
        return res


if __name__ == "__main__":
    import sys
    import time
    t0 = time.time()
    A = Analysis(sys.argv[1])
    t1 = time.time()
    o = A.routes()
    print("golden %.0fs, routes %.0fs" % (t1 - t0, time.time() - t1))
    print("pairs", A.pairs, "forward lot", A.fwd_lot, "stock left", A.stock_left)
    for k, f in sorted(A.gfit.items()):
        print("fit", k, f["n"], {x: round(f[x], 6) for x in ("w0", "r0", "beta", "gamma")})
    print("R1 %.3f (Q1 %.3f, unflagged share %.3f, forward-lot share %.3f)" % (A.R1, A.R1_q1, A.unflagged_share, A.R1_fwd_share),
          "routes: q1 %.3f labels %.3f no-rolloff %.3f pooled %.3f diemap %.3f before/after %.3f"
          % (o["R1_q1_baseline"], o["R1_labels"], o["R1_no_rolloff"], o["R1_pooled"], o["R1_diemap_sample"], o["R1_before_after"]))
    print("R1 die", {k: round(v) for k, v in A.R1_die.items()}, "USD %.0f" % A.R1_usd, "pooled", {k: round(v) for k, v in o["R1_die_pooled"].items()})
    print("R2", {k: round(v, 4) for k, v in A.R2.items()}, "joint", {k: round(v, 4) for k, v in o["R2_joint"].items()}, "ring t", o["R2_joint_ring_t"])
    print("R2 commonality top", o["R2_commonality_top"], "ring-only swap steps", [(u, t, round(s, 4)) for u, t, s in A.ring_swaps])
    print("FT", {k: round(v, 5) for k, v in A.ft.items() if k != "latent"}, "lots in window", A.n_ft_win)
    print("R3", {k: round(v) for k, v in A.R3.items()}, "observed", {k: round(v) for k, v in A.R3_observed.items()}, "USD %.0f" % A.R3_usd)
    for k in ("R3_proportional", "R3_clean_lot_base", "R3_q1_base", "R3_raw_age"):
        print("  ", k, {a: round(b) for a, b in o[k].items()})
    print("   raw-age FT", {k: round(v, 5) for k, v in A.ft_raw.items() if k not in ("latent", "clock")}, "prop", A.prop)
    print("R4 onset", A.onset, "slope", {u: round(v, 3) for u, v in A.slope.items()})
    for k in ("R4_pooled", "R4_old_lots", "R4_unit", "R4_unit_fwd", "R4_fleet", "R4_summer", "R4_linear"):
        print("  ", k, {u: (round(a), round(b, 3)) for u, (a, b) in o[k].items()})
    print("REC", A.REC)
    for k in sorted(x for x in o if x.startswith("REC_")):
        print("  ", k, o[k])
    print("R5 %.0f" % A.R5, {u: round(v) for u, v in A.R5_unit.items()}, "pairs", {p: round(v) for p, v in A.R5_pair.items()})
    for k in sorted(x for x in o if x.startswith("R5_")):
        print("  ", k, round(o[k]))
