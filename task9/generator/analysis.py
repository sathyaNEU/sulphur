"""task9: the golden analysis and the hurried routes, computed from the pack alone (record.py), never from the
simulator. Every figure the answer blocks state comes from here.

  R1  the ring's loss on wafers sorted 1 April to 31 August, in points of mean wafer sort yield
  R2  the same loss in good die for each product
  R3  each candidate cause's share of that loss: the conditioner disk's wear, the pad's life on top of it, the retaining
      ring, deposition chamber DEP-3, scanner SC-4 and the chambers' RF hours
  R4  each unit's onset (wafers of its disk's own use) and the slope after it (outer-band fail rate per 1,000 wafers)
  R5  the shares of the loss from the 2,000-wafer rule's own exposure, Rev F's extension and the EW-118 retained disks
  R6  each unit's count for the disk once Rev G takes it out of the full PM (the call)
  R7  the yearly saving of that against Rev F as it stands

The ring's loss on a wafer is its outer-band fails above what the band fails with no ring: the wafer's own interior
fail rate plus the band's normal fallout, the band's excess on wafers whose disk has not reached its onset.
"""
import os
import sqlite3

import numpy as np
import pandas as pd
import yaml

import pack as PK
import record as RC

WIN = ("2026-04-01", "2026-09-01")
REV_F = pd.Timestamp("2026-04-02")
CURRENT = "2026-06-01"            # the summer's mix and loading, the current state the count and the saving are set at
GRID = np.arange(400, 2001, 5)
UNITS = ["PU-1", "PU-2", "PU-3", "PU-4"]
PAD_LIFE = 600.0
CAUSES = ["disk", "pad", "ring", "dep3", "sc4", "rf"]
RIVALS = ("dep3", "sc4", "rf100")


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
    out = dict(w0=w0, r0=float(b[0]), beta=float(b[1]), sse=sse, gamma=0.0)
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


def life_fit(g, grid=np.arange(600, 1801, 10), extra=RIVALS):
    """The same hinge with each disk life's own slope (the disk lives wear at their own rates), the pad's life as a
    common interaction, the retaining ring's usage and the rivals beside it."""
    lives = sorted(g.disk_life.unique())
    idx = {l: i for i, l in enumerate(lives)}
    li = g.disk_life.map(idx).values
    wt = g.tested_band.values.astype(float)
    sw = np.sqrt(wt)
    y = g.y.values
    best = None
    for w0 in grid:
        h = np.maximum(0.0, g.disk.values - w0)
        H = np.zeros((len(g), len(lives)))
        H[np.arange(len(g)), li] = h
        X = np.column_stack([np.ones(len(g)), H, h * g.pad.values / PAD_LIFE, g.ring.values / 1000.0] +
                            [g[c].values.astype(float) for c in extra])
        b, *_ = np.linalg.lstsq(X * sw[:, None], y * sw, rcond=None)
        sse = float(np.sum(wt * (y - X @ b) ** 2))
        if best is None or sse < best[0]:
            best = (sse, float(w0), b, X)
    sse, w0, b, X = best
    n = len(lives)
    return dict(w0=w0, r0=float(b[0]), betas=dict(zip(lives, b[1:1 + n])), theta=float(b[1 + n]), ring=float(b[2 + n]),
                **{c: float(b[3 + n + i]) for i, c in enumerate(extra)})


def linear_fit(g, dose="disk"):
    """A dose taken straight from zero."""
    x = g[dose].values.astype(float)
    wt = g.tested_band.values.astype(float)
    X = np.column_stack([np.ones(len(g)), x])
    sw = np.sqrt(wt)
    b, *_ = np.linalg.lstsq(X * sw[:, None], g.y.values * sw, rcond=None)
    return dict(w0=0.0, r0=float(b[0]), beta=float(b[1]), gamma=0.0)


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
        self.d = d
        self.costs = yaml.safe_load(open(os.path.join(tgt, PK.F["costs"])))
        self.value = {p: float(v["value_per_good_die"]) for p, v in self.costs["die"].items()}
        self.n_band = d.groupby("product").tested_band.median().to_dict()
        self.allin = {k: float(v) for k, v in self.costs["all_in"].items()}
        self.part_price = {"pad": float(self.costs["parts"]["polishing_pad"]), "disk": float(self.costs["parts"]["conditioner_disk"]),
                           "ring": float(self.costs["parts"]["retaining_ring"])}
        self.wpy = float(self.costs["volume"]["wafers_per_year_ild_cmp"])
        self.fit()
        self.r1()
        self.causes()
        self.bridge()
        self.counts()
        self.saving()

    # ---- R4: the dose-response, by downforce pair (golden), by unit and over the fleet (rival and shortcut)
    def fit(self):
        d = self.d
        self.pair_fit = {p: hinge_fit(d[d.pair == p]) for p in self.pairs}
        self.unit_fit = {u: hinge_fit(d[d.unit == u]) for u in UNITS}
        self.fleet_fit = hinge_fit(d)
        self.onset = {u: self.pair_fit[self.pair_of[u]]["w0"] for u in UNITS}
        self.slope = {u: self.pair_fit[self.pair_of[u]]["beta"] * 1000 for u in UNITS}   # band fail rate per 1,000 wafers
        self.r0 = {p: f["r0"] for p, f in self.pair_fit.items()}

    def excess(self, disk, pad, f):
        return f["beta"] * np.maximum(0.0, np.asarray(disk, float) - f["w0"]) * (1 + f["gamma"] * np.asarray(pad, float) / PAD_LIFE)

    # ---- R1, R2: the loss on every sorted wafer in the window
    def r1(self):
        d = self.d
        d["ring_die"] = d.f_band * d.tested_band - d.tested_band * (d.f_in + d.pair.map(self.r0))
        w = d[d.win]
        self.n_win = int(len(w))
        self.R1 = float(np.mean(w.ring_die / w.gross) * 100)
        self.R2 = {p: float(v) for p, v in w.groupby("product").ring_die.sum().items()}
        self.R2_usd = float(sum(self.R2[p] * self.value[p] for p in self.R2))
        q = d[d.q1]
        self.R1_q1 = float(np.mean(q.ring_die / q.gross) * 100)
        lab = w.adc_label == "EDGE_RING"
        self.unflagged_share = float(w.ring_die[~lab].sum() / w.ring_die.sum())

    # ---- R3: every candidate in one model, each disk life at its own rate
    def causes(self):
        d, w = self.d, self.d[self.d.win]
        contrib = {k: 0.0 for k in CAUSES}
        self.life = {}
        for p in self.pairs:
            g = d[d.pair == p]
            f = life_fit(g)
            self.life[p] = f
            gw = w[w.pair == p]
            h = np.maximum(0.0, gw.disk.values - f["w0"])
            bd = gw.disk_life.map(f["betas"]).fillna(np.mean(list(f["betas"].values()))).values
            sc = gw.tested_band.values / gw.gross.values * 100 / len(w)
            contrib["disk"] += float(np.sum(bd * h * sc))
            contrib["pad"] += float(np.sum(f["theta"] * h * gw.pad.values / PAD_LIFE * sc))
            contrib["ring"] += float(np.sum(f["ring"] * gw.ring.values / 1000.0 * sc))
            contrib["dep3"] += float(np.sum(f["dep3"] * gw.dep3.values * sc))
            contrib["sc4"] += float(np.sum(f["sc4"] * gw.sc4.values * sc))
            contrib["rf"] += float(np.sum(f["rf100"] * (gw.rf100.values - g.rf100.min()) * sc))
        tot = contrib["disk"] + contrib["pad"]
        self.R3 = {k: v / tot for k, v in contrib.items()}
        self.ring_swaps = self.swap_steps()

    def swap_steps(self, span=300):
        """The step at each ring-only swap, the disk running on: the no-ring model's mean residual over the next span
        wafers on the unit less its mean over the last span."""
        d, ev = self.d, self.R.events
        fit = np.zeros(len(d))
        for p in self.pairs:
            s = (d.pair == p).values
            fit[s] = self.r0[p] + self.excess(d.disk[s], d.pad[s], self.pair_fit[p])
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

    # ---- R5: each rule run on each unit's own wafers
    def schedule(self, u, rule):
        R = self.R
        f = R.fdc[R.fdc.unit == u].sort_values("platen")
        e = R.events[R.events.unit == u]
        first = f.platen.min()
        pre = e[e.counter < first]
        full_c = pre[pre.event_class == "FULL_PM"].counter.max()
        pad_c = pre[pre.parts.map(lambda s: "pad" in s)].counter.max()
        st = dict(disk=first - full_c, ring=first - full_c, full=first - full_c, pad=first - pad_c)
        uns = {}
        for _, r in e[e.event_class == "UNSCHED"].iterrows():
            uns.setdefault(int(r.counter), set()).update(r.parts)
        out_d, out_p = np.empty(len(f)), np.empty(len(f))
        for i, (plat, ts) in enumerate(zip(f.platen.values, f.polish_ts.values)):
            for part in uns.get(int(plat), ()):
                st[part] = 0
            out_d[i], out_p[i] = st["disk"], st["pad"]
            for k in st:
                st[k] += 1
            iv = 2000 if rule == "E" or pd.Timestamp(ts) < REV_F else 2800
            if st["full"] >= iv:
                st["full"] = st["pad"] = st["ring"] = st["disk"] = 0
            elif st["pad"] >= PAD_LIFE:
                st["pad"] = 0
        return pd.DataFrame(dict(wafer_id=f.wafer_id.values, disk_cf=out_d, pad_cf=out_p))

    def loss_under(self, sched, fits=None):
        w = self.d[self.d.win]
        m = w.merge(sched, on="wafer_id")
        fits = fits or self.pair_fit
        ex = np.zeros(len(m))
        for p in self.pairs:
            s = (m.pair == p).values
            ex[s] = self.excess(m.disk_cf[s], m.pad_cf[s], fits[p]) * (m.tested_band[s] / m.gross[s]).values
        return float(ex.sum() / len(w) * 100)

    def bridge(self, fits=None):
        sE = pd.concat([self.schedule(u, "E") for u in UNITS])
        sF = pd.concat([self.schedule(u, "F") for u in UNITS])
        w = self.d[self.d.win]
        act = w[["wafer_id", "disk", "pad"]].rename(columns={"disk": "disk_cf", "pad": "pad_cf"})
        LE, LF, LA = self.loss_under(sE, fits), self.loss_under(sF, fits), self.loss_under(act, fits)
        if fits is None:
            self.sched_E, self.sched_F = sE, sF
            self.L = dict(old_rule=LE, rev_f=LF, actual=LA)
            self.R5 = {"old_rule": LE / LA, "rev_f": (LF - LE) / LA, "ew118": (LA - LF) / LA}
        return {"old_rule": LE / LA, "rev_f": (LF - LE) / LA, "ew118": (LA - LF) / LA}

    # ---- R6: each unit's count, R7: the saving
    def mix_value(self, frm=CURRENT):
        m = self.d[self.d.sort_ts >= frm]["product"].value_counts(normalize=True)
        return float(sum(m[p] * self.n_band[p] * self.value[p] for p in m.index))

    def k_of(self, f, V=None, padbar=PAD_LIFE / 2):
        """Dollars of good die the ring costs per wafer, per wafer of disk use past the onset."""
        V = self.mix_value() if V is None else V
        return V * f["beta"] * (1 + f.get("gamma", 0.0) * padbar / PAD_LIFE)

    def tstar(self, f, c=None, V=None):
        c = self.allin["disk_change"] if c is None else c
        k = self.k_of(f, V)
        return float(np.sqrt(f["w0"] ** 2 + 2 * c / k)) if k > 0 else float("nan")

    def counts(self):
        self.V = self.mix_value()
        self.R6 = {u: self.tstar(self.pair_fit[self.pair_of[u]]) for u in UNITS}

    def cpw(self, f, T):
        """The disk's cost per wafer on its own count T: its changes at their all-in and the good die the ring takes."""
        k = self.k_of(f)
        return (self.allin["disk_change"] + k * max(0.0, T - f["w0"]) ** 2 / 2) / T

    def unit_share(self, frm=CURRENT):
        return self.d[self.d.polish_ts >= frm].unit.value_counts(normalize=True)

    def yearly(self, f, T, share, rev_f_ring=None):
        """Rev F's cost per wafer (its full PM and the ring over a 2,800-wafer disk) less Rev G's (the full PM less the
        disk's price, and the disk on its own count T), over a year of the unit's wafers."""
        k = self.k_of(f)
        full = self.allin["full_pm"]
        ring_f = k * max(0.0, 2800 - f["w0"]) ** 2 / 2 / 2800 if rev_f_ring is None else rev_f_ring
        rev_f = full / 2800 + ring_f
        rev_g = (full - self.part_price["disk"]) / 2800 + (self.allin["disk_change"] + k * max(0.0, T - f["w0"]) ** 2 / 2) / T
        return (rev_f - rev_g) * self.wpy * share

    def saving(self):
        sh = self.unit_share()
        self.R7_unit = {u: self.yearly(self.pair_fit[self.pair_of[u]], self.R6[u], sh[u]) for u in UNITS}
        self.R7 = float(sum(self.R7_unit.values()))

    # ======================================================================== the hurried routes
    def routes(self):
        d, w = self.d, self.d[self.d.win]
        out = {}
        pts = lambda die, sub: float(np.mean(die / sub.gross) * 100)
        # R1, R2
        q1 = d[d.q1].y.mean()
        out["R1_q1_baseline"] = pts(w.tested_band * (w.y - q1), w)
        out["R2_q1_baseline"] = {p: float(v) for p, v in (w.tested_band * (w.y - q1)).groupby(w["product"]).sum().items()}
        lab = (w.adc_label == "EDGE_RING").values
        out["R1_labels"] = pts(np.where(lab, w.tested_band * w.y, 0.0), w)
        out["R2_labels"] = {p: float(v) for p, v in pd.Series(np.where(lab, w.tested_band * w.y, 0.0), index=w.index)
                            .groupby(w["product"]).sum().items()}
        out["R1_no_rolloff"] = pts(w.tested_band * w.y, w)
        out["R2_no_rolloff"] = {p: float(v) for p, v in (w.tested_band * w.y).groupby(w["product"]).sum().items()}
        con = sqlite3.connect(os.path.join(self.tgt, PK.F["diemaps"]))
        maps = set(r[0] for r in con.execute("SELECT wafer_id FROM wafer_index"))
        con.close()
        wm = w[w.wafer_id.isin(maps)]
        out["R1_diemap_sample"] = pts(wm.ring_die, wm)
        out["R1_before_after"] = float((d[d.q1].sort_yield.mean() - w.sort_yield.mean()) * 100)
        # R3: the joint regression read wafer by wafer (every counter and rival, one slope per pair)
        contrib = {k: 0.0 for k in CAUSES}
        self.naive = {}
        for p in self.pairs:
            g = d[d.pair == p]
            f = hinge_fit(g, ring=True, extra=RIVALS)
            self.naive[p] = f
            gw = w[w.pair == p]
            h = np.maximum(0.0, gw.disk.values - f["w0"])
            sc = gw.tested_band.values / gw.gross.values * 100 / len(w)
            contrib["disk"] += float(np.sum(f["beta"] * h * sc))
            contrib["pad"] += float(np.sum(f["beta"] * f["gamma"] * h * gw.pad.values / PAD_LIFE * sc))
            contrib["ring"] += float(np.sum(f["ring"] * gw.ring.values / 1000.0 * sc))
            contrib["dep3"] += float(np.sum(f["dep3"] * gw.dep3.values * sc))
            contrib["sc4"] += float(np.sum(f["sc4"] * gw.sc4.values * sc))
            contrib["rf"] += float(np.sum(f["rf100"] * (gw.rf100.values - g.rf100.min()) * sc))
        tot = contrib["disk"] + contrib["pad"]
        out["R3_joint"] = {k: v / tot for k, v in contrib.items()}
        out["R3_joint_ring_t"] = self.naive_t()
        # tool commonality: the outer band's excess by tool at every step, the largest gaps as the causes
        gaps = {}
        for col, name in (("unit", "unit"), ("dep", "dep"), ("m1_scanner", "scanner")):
            m = w.groupby(col).y.mean()
            for k, v in m.items():
                gaps["%s %s" % (name, k)] = float(v - w.y.mean())
        out["R3_commonality_top"] = sorted(gaps, key=lambda k: -gaps[k])[:4]
        top_share = w.groupby("pair").ring_die.sum() / w.ring_die.sum()
        out["R3_commonality"] = {"disk": 0.0, "pad": 0.0, "ring": 0.0, "dep3": float(gaps["dep DEP-3"] / max(w.y.mean(), 1e-9)),
                                 "sc4": float(gaps.get("scanner SC-4", 0.0) / max(w.y.mean(), 1e-9)), "rf": 0.0}
        out["R3_commonality_pair_share"] = float(top_share.get("high", 0.0))
        # R4: per-unit fits, the fleet in one fit, the pad counter, wafers since the full PM, a dose from zero
        out["R4_unit"] = {u: (self.unit_fit[u]["w0"], self.unit_fit[u]["beta"] * 1000) for u in UNITS}
        out["R4_fleet"] = {u: (self.fleet_fit["w0"], self.fleet_fit["beta"] * 1000) for u in UNITS}
        d["pad_ctr"] = d.pad_life_ctr.astype(float)
        padf = {p: hinge_fit(d[d.pair == p], dose="pad_ctr", grid=np.arange(0, 600, 5), pad=False) for p in self.pairs}
        out["R4_pad_counter"] = {u: (padf[self.pair_of[u]]["w0"], padf[self.pair_of[u]]["beta"] * 1000) for u in UNITS}
        fullf = {p: hinge_fit(d[d.pair == p], dose="full") for p in self.pairs}
        out["R4_since_full"] = {u: (fullf[self.pair_of[u]]["w0"], fullf[self.pair_of[u]]["beta"] * 1000) for u in UNITS}
        lin = {p: linear_fit(d[d.pair == p]) for p in self.pairs}
        out["R4_linear"] = {u: (0.0, lin[self.pair_of[u]]["beta"] * 1000) for u in UNITS}
        self.route_fits = dict(fleet=self.fleet_fit, pad=padf, full=fullf, lin=lin)
        # R5: the loss sliced by the disk's usage at 2,000 and 2,800; the whole rise put on Rev F
        lw = w.ring_die / w.gross
        tot = lw.sum()
        out["R5_slice"] = {"old_rule": float(lw[w.disk < 2000].sum() / tot), "rev_f": float(lw[(w.disk >= 2000) & (w.disk < 2800)].sum() / tot),
                           "ew118": float(lw[w.disk >= 2800].sum() / tot)}
        out["R5_all_rev_f"] = {"old_rule": 0.0, "rev_f": 1.0, "ew118": 0.0}
        out["R5_ring_term"] = self.bridge(fits={p: hinge_fit(d[d.pair == p], ring=True) for p in self.pairs})
        out["R5_unweighted"] = self.bridge(fits={p: hinge_fit(d[d.pair == p], weight=False) for p in self.pairs})
        out["R5_fleet"] = self.bridge(fits={p: self.fleet_fit for p in self.pairs})
        # R6: per-unit fits, the fleet's one count, a dose from zero, the full PM moved to its own best interval, the pad
        out["R6_unit"] = {u: self.tstar(self.unit_fit[u]) for u in UNITS}
        out["R6_fleet"] = {u: self.tstar(self.fleet_fit) for u in UNITS}
        out["R6_linear"] = {u: self.tstar(lin[self.pair_of[u]]) for u in UNITS}
        out["R6_full_pm_lever"] = {u: self.tstar(fullf[self.pair_of[u]], c=self.allin["full_pm"]) for u in UNITS}
        out["R6_pad_lever"] = {u: self.tstar(padf[self.pair_of[u]], c=self.allin["pad_change"]) for u in UNITS}
        out["R6_apr_aug_mix"] = {u: self.tstar(self.pair_fit[self.pair_of[u]], V=self.mix_value(WIN[0])) for u in UNITS}
        out["R6_joint_ring"] = {u: self.tstar(self.naive[self.pair_of[u]]) for u in UNITS}
        # R7: the summer's own loss rate taken as Rev F's; the fleet's one count; Rev F's steady state with the fleet fit
        sh = self.unit_share()
        summer = d[d.sort_ts >= CURRENT]
        usd = (summer.ring_die * summer["product"].map(self.value))
        rate = usd.groupby(summer.unit).sum() / summer.groupby("unit").size()
        out["R7_summer_rate"] = float(sum(self.yearly(self.pair_fit[self.pair_of[u]], self.R6[u], sh[u], rev_f_ring=float(rate[u]))
                                          for u in UNITS))
        out["R7_fleet"] = float(sum(self.yearly(self.fleet_fit, out["R6_fleet"][u], sh[u]) for u in UNITS))
        out["R7_unit"] = float(sum(self.yearly(self.unit_fit[u], out["R6_unit"][u], sh[u]) for u in UNITS))
        out["R7_apr_aug"] = float(sum(self.yearly(self.pair_fit[self.pair_of[u]], self.R6[u], self.unit_share(WIN[0])[u]) for u in UNITS))
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
    A = Analysis(sys.argv[1])
    o = A.routes()
    print("pairs", A.pairs)
    for p, f in A.pair_fit.items():
        print("fit", p, {k: round(v, 6) for k, v in f.items()})
    print("R1 %.3f (Q1 %.3f, unflagged share %.3f)" % (A.R1, A.R1_q1, A.unflagged_share), "routes: q1 %.3f labels %.3f no-rolloff %.3f diemap %.3f before/after %.3f"
          % (o["R1_q1_baseline"], o["R1_labels"], o["R1_no_rolloff"], o["R1_diemap_sample"], o["R1_before_after"]))
    print("R2", {k: round(v) for k, v in A.R2.items()}, "USD %.0f" % A.R2_usd, "q1 route", {k: round(v) for k, v in o["R2_q1_baseline"].items()})
    print("R3", {k: round(v, 4) for k, v in A.R3.items()}, "joint", {k: round(v, 4) for k, v in o["R3_joint"].items()}, "ring t", o["R3_joint_ring_t"])
    print("R3 commonality top", o["R3_commonality_top"], "ring-only swap steps", [(u, t, round(s, 4)) for u, t, s in A.ring_swaps])
    print("R4 onset", A.onset, "slope", {u: round(v, 3) for u, v in A.slope.items()})
    for k in ("R4_unit", "R4_fleet", "R4_pad_counter", "R4_since_full", "R4_linear"):
        print("  ", k, {u: (round(a), round(b, 3)) for u, (a, b) in o[k].items()})
    print("R5", {k: round(v, 3) for k, v in A.R5.items()}, "L", {k: round(v, 3) for k, v in A.L.items()})
    for k in ("R5_slice", "R5_ring_term", "R5_unweighted", "R5_fleet"):
        print("  ", k, {a: round(b, 3) for a, b in o[k].items()})
    print("R6", {u: round(v) for u, v in A.R6.items()}, "V %.2f" % A.V)
    for k in ("R6_unit", "R6_fleet", "R6_linear", "R6_full_pm_lever", "R6_pad_lever", "R6_apr_aug_mix", "R6_joint_ring"):
        print("  ", k, {u: (round(v) if v == v else None) for u, v in o[k].items()})
    print("R7 %.0f" % A.R7, {u: round(v) for u, v in A.R7_unit.items()}, "routes", {k: round(o[k]) for k in ("R7_summer_rate", "R7_fleet", "R7_unit", "R7_apr_aug")})
