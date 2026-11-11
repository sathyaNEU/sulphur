"""task9: the golden analysis and the routes a hurried analyst takes, on the solver-side record only.

The forecast is a posterior predictive count of replacements per vault and quarter: each family's replacement hazard
by age (Weibull wear-out with an infant term, fitted by Poisson regression on age-banded exposure with delayed entry),
each vault's frailty shrunk toward its family (gamma, empirical Bayes), the hot batch's ramp by months since build
(onset and doubling fitted on its own exposure), the P2 policy's spurious pulls at their steady rate after the harvest,
and the counts' extra-Poisson spread estimated from the record's vault-quarter counts. The same machinery cut at
30 September 2025 is the back-test.
"""
import datetime as dt

import numpy as np
import pandas as pd

import params as P

FAMS = ["OM-6", "M-14", "M-16", "T-20", "W-22", "HX-8", "KS-10", "VB-12"]
DCS = ["DC-1", "DC-2", "DC-3"]
BAND_Y = 0.5                     # age bands of half a year for the hazard fit (months in the first year)
INFANT_MONTHS = 6.0


def qbounds(q):
    y, k = int(q[:4]), int(q[-1])
    a = pd.Timestamp(y, 3 * (k - 1) + 1, 1)
    b = pd.Timestamp(y + (k == 4), 1 if k == 4 else 3 * k + 1, 1)
    return a, b


def quarters_after(cut, n=4):
    q = []
    a = pd.Timestamp(cut) + pd.Timedelta(days=1)
    for i in range(n):
        y, m = a.year, a.month
        k = (m - 1) // 3 + 1
        q.append("%dQ%d" % (y, k))
        a = qbounds(q[-1])[1]
    return q


def poisson_glm(X, y, off, w=None, iters=60):
    """Poisson regression with an exposure offset by Newton steps; returns coefficients and their covariance."""
    beta = np.zeros(X.shape[1])
    beta[0] = np.log(max(y.sum(), 0.5) / np.exp(off).sum())
    for _ in range(iters):
        eta = X @ beta + off
        mu = np.exp(np.clip(eta, -30, 30))
        g = X.T @ (y - mu)
        H = (X * mu[:, None]).T @ X + 1e-9 * np.eye(X.shape[1])
        step = np.linalg.solve(H, g)
        beta += step
        if np.abs(step).max() < 1e-9:
            break
    mu = np.exp(X @ beta + off)
    cov = np.linalg.inv((X * mu[:, None]).T @ X + 1e-9 * np.eye(X.shape[1]))
    return beta, cov


class Analysis:
    def __init__(self, rec, cut=P.END, spur_from=dt.date(2025, 9, 1), frailty=True, ages="rebuilt", events="split",
                 hot="bma", spread="overdispersed", seed=P.SEED, infant=None, shrink=True, hot_set="scan", hot_scale=1.0,
                 ramp_slow=1.0, migrate_rule="vault"):
        self.rec = rec
        self.hot_set = hot_set
        self.hot_scale, self.ramp_slow = hot_scale, ramp_slow     # perturbations: the batch's level, its forward growth
        self.migrate_rule = migrate_rule      # "vault": each vault on its own replacements; "batch": every batch vault on the batch's share
        self.cut = pd.Timestamp(cut)
        self.spur_from = pd.Timestamp(spur_from)
        self.frailty, self.ages, self.events, self.hot_mode, self.spread = frailty, ages, events, hot, spread
        self.infant_fixed, self.shrink = infant, shrink
        self.rng = np.random.default_rng(seed)
        d = rec.d.copy()
        how, _, widen = hot_set.partition(":")
        d["hot"] = rec.hot_flags(cut, how, widen=int(widen or 0)).values
        self.hot_window = getattr(rec, "hot_scan", {}).get("window") if how == "scan" else None
        if ages == "first_seen":
            d["install"] = d.install_date
        d = d[d.entry <= self.cut].copy()
        d["exit_c"] = d.exit.where(d.exit <= self.cut, self.cut)
        d["ev"] = d.event & (d.exit <= self.cut)
        d["spur"] = d.ev & (d.trigger == "187")
        self.d = d
        self.fit()

    # ---- exposure by family and age band between two dates, events of a kind
    def _bands(self, d, a, b, kind):
        lo = np.maximum(d.entry.values.astype("datetime64[D]"), np.datetime64(a.date()))
        hi = np.minimum(d.exit_c.values.astype("datetime64[D]"), np.datetime64(b.date()))
        ok = hi > lo
        inst = d.install.values.astype("datetime64[D]")
        a0 = (lo - inst).astype(float) / 365.25
        a1 = (hi - inst).astype(float) / 365.25
        evd = d.exit_c.values.astype("datetime64[D]")
        evage = (evd - inst).astype(float) / 365.25
        if kind == "fail":
            e = d.ev.values & ~d.spur.values
        else:
            e = d.spur.values
        e = e & (evd >= np.datetime64(a.date())) & (evd < np.datetime64(b.date()))
        rows = []
        fam = d.family.values
        for f in FAMS:
            m = (fam == f) & ok
            if not m.any():
                continue
            top = int(np.ceil(max(a1[m].max(), 1.0) / BAND_Y)) + 1
            edges = np.concatenate([np.arange(12) / 12.0, np.arange(1.0 / BAND_Y, top + 1) * BAND_Y])
            nb = len(edges) - 1
            expo = np.zeros(nb)
            for k in range(nb):
                expo[k] = np.clip(np.minimum(a1[m], edges[k + 1]) - np.maximum(a0[m], edges[k]), 0, None).sum()
            cnt = np.bincount(np.clip(np.searchsorted(edges, evage[m & e], side="right") - 1, 0, nb - 1), minlength=nb)
            for k in range(nb):
                if expo[k] > 0.5:
                    rows.append((f, (edges[k] + edges[k + 1]) / 2, expo[k], cnt[k]))
        return pd.DataFrame(rows, columns=["family", "age", "expo", "events"])

    # ---- fit: family curves, the spurious rate, vault frailty, the hot batch's ramp, the counts' spread
    def fit(self):
        d = self.d
        start = pd.Timestamp(P.REC_START)
        hot_d = d[d.hot] if self.hot_mode != "family" else d.iloc[0:0]
        base = d[~d.hot] if self.hot_mode != "family" else d
        B = self._bands(base, start, self.cut, "fail" if self.events == "split" else "all")
        if self.events != "split":
            B2 = self._bands_all(base, start, self.cut)
            B = B2
        best = None
        for im in ((self.infant_fixed,) if self.infant_fixed else (1.0, 2.0, 3.0, 4.0, 6.0)):
            self.infant_months = im
            cv = self._fit_curves(B)
            if best is None or self._pool_ll > best[0]:
                best = (self._pool_ll, im, cv, self.pool)
        self._pool_ll, self.infant_months, self.curve, self.pool = best
        for f, sib in (("W-22", "T-20"), ("T-20", "M-16"), ("X-24", "W-22")):
            if f not in self.curve:
                self.curve[f] = self.curve[sib]
        # spurious 187 pulls at P2's steady rate, after the harvest
        if self.events == "split":
            S = self._bands(d, max(self.spur_from, start), self.cut, "spur")
            self.spur = float(S.events.sum() / max(S.expo.sum(), 1e-9)) if len(S) else 0.0
        else:
            self.spur = 0.0
        # vault frailty, gamma empirical Bayes on observed against expected
        self.vault_ab = {}
        if self.frailty:
            O, E = self._obs_exp(base)
            for f in FAMS:
                vs = [v for v in O if v[0] == f]
                if len(vs) < 2:
                    continue
                r = np.array([O[v] / max(E[v], 1e-9) for v in vs])
                e = np.array([E[v] for v in vs])
                var = max(np.var(r) - np.mean(1.0 / np.maximum(e, 1e-9)) * np.mean(r), 1e-3)
                a = 1.0 / var
                for v in vs:
                    self.vault_ab[v] = (a + O[v], a + E[v])
        # the hot batch's ramp: onset and doubling by months since build
        self.hot = None
        if self.hot_mode in ("ramp", "linear", "flat", "power", "bma") and len(hot_d):
            self.hot = self._fit_hot(hot_d)
        # extra-Poisson spread of vault-quarter counts (frailty taken out)
        self.k = self._dispersion(base)

    def _fit_curves(self, B):
        """Family levels, one infant term for the fleet, and each family's age slope shrunk toward the fleet's slope by
        empirical Bayes (a family whose records cover only its first years borrows the fleet's shape)."""
        fams = [f for f in FAMS if (B.family == f).any() and B[B.family == f].events.sum() >= 1]
        B = B[B.family.isin(fams)]
        idx = {f: i for i, f in enumerate(fams)}
        age = B.age.values
        fi = np.array([idx[f] for f in B.family])
        nf = len(fams)
        y, off = B.events.values.astype(float), np.log(B.expo.values)
        inf = np.exp(-age * 12.0 / self.infant_months)
        la = np.log(np.maximum(age, 0.05))

        def design(slopes_free):
            cols = [np.eye(nf)[fi]]
            cols.append(inf[:, None])
            if slopes_free:
                cols.append(np.eye(nf)[fi] * la[:, None])
            else:
                cols.append(la[:, None])
            return np.column_stack(cols)
        # stage 1: each family's own slope (with the shared infant term)
        X1 = design(True)
        b1, c1 = poisson_glm(X1, y, off)
        slope, se = b1[nf + 1:], np.sqrt(np.diag(c1)[nf + 1:])
        # stage 2: the fleet's slope and the between-family spread, method of moments
        w = 1.0 / np.maximum(se ** 2, 1e-6)
        sbar = float((w * slope).sum() / w.sum())
        tau2 = max(float(((slope - sbar) ** 2 - se ** 2).clip(min=0).mean()), 0.02)
        shrunk = (slope / np.maximum(se ** 2, 1e-6) + sbar / tau2) / (1.0 / np.maximum(se ** 2, 1e-6) + 1.0 / tau2)
        if not self.shrink:
            shrunk = slope.copy()
        # stage 3: levels and the infant term given the shrunk slopes
        X3 = np.column_stack([np.eye(nf)[fi], inf[:, None]])
        b3, c3 = poisson_glm(X3, y, off + shrunk[fi] * la)
        mu3 = np.exp(X3 @ b3 + off + shrunk[fi] * la)
        self._pool_ll = float((y * np.log(np.maximum(mu3, 1e-12)) - mu3).sum())
        self.pool = dict(fleet_slope=sbar, tau2=tau2, slopes=dict(zip(fams, shrunk)), own=dict(zip(fams, slope)), se=dict(zip(fams, se)))
        out = {}
        for f in fams:
            i = idx[f]
            beta = np.array([b3[i], shrunk[i], b3[nf]])
            cov = np.zeros((3, 3))
            cov[0, 0], cov[2, 2], cov[0, 2] = c3[i, i], c3[nf, nf], c3[i, nf]
            cov[2, 0] = cov[0, 2]
            post_var = 1.0 / (1.0 / np.maximum(se[i] ** 2, 1e-6) + 1.0 / tau2)
            cov[1, 1] = post_var
            # a slope drawn away from its value moves the level that keeps the family's events fixed at its mean age
            ma = float(np.average(la[fi == i], weights=B.expo.values[fi == i]))
            cov[0, 1] = cov[1, 0] = -ma * post_var
            cov[0, 0] += ma * ma * post_var
            out[f] = (beta, cov)
        return out

    def _bands_all(self, d, a, b):
        x = self._bands(d.assign(spur=False), a, b, "fail")
        return x

    def _hz(self, f, age, beta=None):
        beta = self.curve[f][0] if beta is None else beta
        age = np.maximum(age, 0.01)
        return np.exp(beta[0] + beta[1] * np.log(age) + beta[2] * np.exp(-age * 12.0 / self.infant_months))

    def _cum(self, f, a0, a1, beta=None, steps=6):
        """Integral of the family hazard over each drive's age interval, by Simpson's rule."""
        t = np.linspace(0, 1, steps + 1)
        w = np.ones(steps + 1)
        w[1:-1:2], w[2:-1:2] = 4, 2
        w = w / (3 * steps)
        ages = a0[:, None] + (a1 - a0)[:, None] * t[None, :]
        return ((self._hz(f, ages, beta) * w[None, :]).sum(axis=1)) * (a1 - a0)

    def _obs_exp(self, d):
        start = pd.Timestamp(P.REC_START)
        lo = np.maximum(d.entry.values.astype("datetime64[D]"), np.datetime64(start.date()))
        hi = d.exit_c.values.astype("datetime64[D]")
        inst = d.install.values.astype("datetime64[D]")
        a0 = np.maximum((lo - inst).astype(float) / 365.25, 0)
        a1 = np.maximum((hi - inst).astype(float) / 365.25, a0)
        O, E = {}, {}
        ev = (d.ev.values & ~d.spur.values) if self.events == "split" else d.ev.values
        for f in FAMS:
            if f not in self.curve:
                continue
            m = d.family.values == f
            e = self._cum(f, a0[m], a1[m])
            vv = d.vault_id.values[m]
            for v, x, o in zip(vv, e, ev[m]):
                O[(f, v)] = O.get((f, v), 0) + int(o)
                E[(f, v)] = E.get((f, v), 0.0) + float(x)
        return O, E

    def _fit_hot(self, h):
        """Poisson fit of the hot drives' events against the HX-8 curve, the ramp in months since build."""
        start = pd.Timestamp(P.REC_START)
        rows = []
        for _, r in h.iterrows():
            lo, hi = max(r.entry, start), r.exit_c
            if hi <= lo:
                continue
            m0 = (lo - r.build).days / 30.4375
            m1 = (hi - r.build).days / 30.4375
            a_inst = (lo - r.install).days / 365.25
            mon = np.arange(np.floor(m0), np.ceil(m1))
            for mm in mon:
                x0, x1 = max(mm, m0), min(mm + 1, m1)
                if x1 <= x0:
                    continue
                age = a_inst + (x0 - m0) / 12.0
                e = self._hz("HX-8", np.array([age]))[0] * (x1 - x0) / 12.0
                em = (r.exit_c - r.build).days / 30.4375
                ev = int(bool(r.ev) and not bool(r.spur) and (x0 <= em < x1 or (x1 >= m1 and em >= x0)))
                rows.append((mm, e, ev))
        df = pd.DataFrame(rows, columns=["m", "e", "ev"]).groupby("m").sum().reset_index()
        self.hot_months = df
        off = np.log(np.maximum(df.e.values, 1e-12))
        y = df.ev.values.astype(float)

        def ll_of(mu):
            return float((y * np.log(np.maximum(mu, 1e-12)) - mu).sum())
        shapes = {}
        if self.hot_mode in ("ramp", "flat", "bma"):
            g = {}
            for onset in np.arange(0.0, 22.01, 1.0):
                x = np.maximum(df.m.values + 0.5 - onset, 0.0)
                X = np.column_stack([np.ones(len(df)), x])
                beta, cov = poisson_glm(X, y, off)
                g[float(onset)] = (ll_of(np.exp(X @ beta + off)), beta, cov)
            shapes["exp"] = g
        if self.hot_mode in ("linear", "bma"):
            g = {}
            for onset in np.arange(0.0, 22.01, 1.0):
                bb = self._lin_fit(df, onset)
                g[float(onset)] = (bb[1], np.array(bb[0]), np.zeros((2, 2)))
            shapes["lin"] = g
        if self.hot_mode in ("power", "bma"):
            X = np.column_stack([np.ones(len(df)), np.log(df.m.values + 0.5)])
            beta, cov = poisson_glm(X, y, off)
            shapes["pow"] = {0.0: (ll_of(np.exp(X @ beta + off)), beta, cov)}
        # each shape's weight: its likelihood averaged over its onset grid (a flat prior on the onset)
        wt = {}
        for k, g in shapes.items():
            lls = np.array([v[0] for v in g.values()])
            wt[k] = float(np.log(np.mean(np.exp(lls - lls.max()))) + lls.max())
        mx = max(wt.values())
        w = {k: np.exp(v - mx) for k, v in wt.items()}
        tot = sum(w.values())
        w = {k: v / tot for k, v in w.items()}
        best_shape = max(w, key=w.get)
        best_onset = max(shapes[best_shape], key=lambda o: shapes[best_shape][o][0])
        return dict(shapes=shapes, weights=w, best=(best_shape, best_onset), mode=self.hot_mode)

    def _lin_fit(self, df, onset):
        best = None
        for slope in np.linspace(0.0, 1.5, 151):
            x = np.maximum(df.m.values + 0.5 - onset, 0.0)
            mult = 1.0 + slope * x
            z = df.ev.sum() / max((df.e.values * mult).sum(), 1e-9)
            mu = z * df.e.values * mult
            ll = float((df.ev.values * np.log(np.maximum(mu, 1e-12)) - mu).sum())
            if best is None or ll > best[1]:
                best = ((z, slope), ll)
        return best

    def _hot_build_mid(self):
        b = self.d[self.d.hot].build
        return b.median()

    def _dispersion(self, d):
        """The extra-Poisson spread of vault-quarter counts after frailty: method of moments on (O - E)^2 against E."""
        if self.spread != "overdispersed":
            return np.inf
        rows = []
        qs = []
        q = "2023Q1"
        while qbounds(q)[1] <= self.cut + pd.Timedelta(days=1):
            qs.append(q)
            a, b = qbounds(q)
            nq = b
            q = "%dQ%d" % (nq.year, (nq.month - 1) // 3 + 1)
        for q in qs:
            a, b = qbounds(q)
            sub = d[(d.entry < b) & (d.exit_c >= a)]
            lo = np.maximum(sub.entry.values.astype("datetime64[D]"), np.datetime64(a.date()))
            hi = np.minimum(sub.exit_c.values.astype("datetime64[D]"), np.datetime64(b.date()))
            inst = sub.install.values.astype("datetime64[D]")
            a0 = np.maximum((lo - inst).astype(float) / 365.25, 0)
            a1 = np.maximum((hi - inst).astype(float) / 365.25, a0)
            evd = sub.exit_c.values.astype("datetime64[D]")
            ev = sub.ev.values & ~sub.spur.values & (evd >= np.datetime64(a.date())) & (evd < np.datetime64(b.date()))
            for f in FAMS:
                if f not in self.curve:
                    continue
                m = sub.family.values == f
                if not m.any():
                    continue
                e = self._cum(f, a0[m], a1[m])
                for v in np.unique(sub.vault_id.values[m]):
                    mv = sub.vault_id.values[m] == v
                    zf = self.vault_ab.get((f, v), (1.0, 1.0))
                    E = float(e[mv].sum()) * zf[0] / zf[1]
                    O = int(ev[m][mv].sum())
                    if E > 0.5:
                        rows.append((O, E))
        O = np.array([r[0] for r in rows], float)
        E = np.array([r[1] for r in rows], float)
        excess = ((O - E) ** 2 - O).sum() / max((E ** 2).sum(), 1e-9)
        return 1.0 / excess if excess > 1e-4 else np.inf

    # ---- the forecast: one cell per quarter, family, vault and hot flag
    def cells(self, quarters):
        """Each cell's expected replacements at the fitted values, with what a parameter draw scales: the exposure-weighted
        mean log age and infant term (family curve), and for hot cells the ramp's exposure at each onset on the grid."""
        d = self.d
        live = d[(d.exit_c >= self.cut) & ~(d.ev & (d.exit <= self.cut))]
        rows = []
        for q in quarters:
            a, b = qbounds(q)
            a0 = np.maximum((a - live.install).dt.days.values / 365.25, 0)
            a1 = np.maximum((b - live.install).dt.days.values / 365.25, 0)
            for f in FAMS:
                if f not in self.curve:
                    continue
                m = live.family.values == f
                if not m.any():
                    continue
                e = self._cum(f, a0[m], a1[m])
                mid = (a0[m] + a1[m]) / 2
                la = np.log(np.maximum(mid, 1.0 / 24))      # a draw's slope is read where the curves were fitted
                inf = np.exp(-mid * 12.0 / self.infant_months)
                hotm = live.hot.values[m]
                mon = ((a + (b - a) / 2) - live.build[m]).dt.days.values / 30.4375
                if self.ramp_slow != 1.0:
                    mcut = (self.cut - live.build[m]).dt.days.values / 30.4375
                    mon = mcut + (mon - mcut) / self.ramp_slow
                vv = live.vault_id.values[m]
                for v in np.unique(vv):
                    for hv in (False, True):
                        mv = (vv == v) & (hotm == hv)
                        if not mv.any():
                            continue
                        ab = self.vault_ab.get((f, v))          # None: no frailty fitted, the vault at its family's level
                        zbar = ab[0] / ab[1] if ab else 1.0
                        ev = e[mv]
                        w = ev / max(ev.sum(), 1e-12)
                        row = dict(q=q, family=f, vault=v, hot=hv, dc=live.dc.values[m][mv][0], drives=int(mv.sum()),
                                   base=float(ev.sum()), zbar=zbar, ab=ab, L=float((w * la[mv]).sum()), I=float((w * inf[mv]).sum()),
                                   spur=self.spur * (b - a).days / 365.25 * int(mv.sum()), ramp=None)
                        if hv and self.hot is not None:
                            row["ramp"] = {(k, o): (float((ev * self._ramp(mon[mv], o, bb, k)).sum()) / max(ev.sum(), 1e-12),
                                                    float((w * self._covariate(mon[mv], o, k)).sum()))
                                           for k, g in self.hot["shapes"].items() for o, (ll, bb, cc) in g.items()}
                        rows.append(row)
        # scheduled installs of a new model, at the newest Tamsin family's early-life hazard
        for qq, dc, fam, n in P.INSTALLS_PLAN:
            if qq not in quarters:
                continue
            i0 = quarters.index(qq)
            a, b = qbounds(qq)
            mid = a + (b - a) / 2
            for q in quarters[i0:]:
                qa, qb = qbounds(q)
                x0, x1 = max((qa - mid).days, 0) / 365.25, max((qb - mid).days, 0) / 365.25
                e = self._cum("W-22", np.array([x0]), np.array([x1]))[0] * n * P.VAULT_DRIVES
                rows.append(dict(q=q, family=fam, vault="NEW-%s-%s" % (qq, dc), hot=False, dc=dc, drives=n * P.VAULT_DRIVES,
                                 base=float(e), zbar=1.0, ab=None, L=float(np.log(max((x0 + x1) / 2, 1.0 / 24))),
                                 I=float(np.exp(-(x0 + x1) / 2 * 12 / self.infant_months)), spur=self.spur * (x1 - x0) * n * P.VAULT_DRIVES,
                                 ramp=None, curve="W-22"))
        return rows

    def _ramp(self, months, onset, beta, shape):
        x = np.maximum(months - onset, 0.0)
        if shape == "lin":
            return beta[0] * (1.0 + beta[1] * x)
        if shape == "pow":
            return np.exp(beta[0] + beta[1] * np.log(np.maximum(months, 1.0)))
        if self.hot_mode == "flat":
            xc = max((self.cut - self._hot_build_mid()).days / 30.4375 - onset, 0.0)
            x = np.minimum(x, xc)
        return np.minimum(np.exp(beta[0] + beta[1] * x), 60.0)

    def _covariate(self, months, onset, shape):
        if shape == "pow":
            return np.log(np.maximum(months, 1.0))
        if shape == "lin":
            return np.zeros_like(months)
        return np.maximum(months - onset, 0.0)

    def simulate(self, quarters, sims=2000, draws=True):
        """Posterior predictive counts: family curves from their sampling distribution, vault frailty from its posterior,
        the ramp's onset from its profile likelihood and its slope given the onset, counts over Poisson by the record's
        spread; with draws=False the fitted values and Poisson counts alone."""
        rng = np.random.default_rng(P.SEED + 11)
        rows = self.cells(quarters)
        n = len(rows)
        fams = sorted({r.get("curve", r["family"]) for r in rows})
        mean = np.zeros((sims, n))
        if draws:
            dbeta = {f: rng.multivariate_normal(np.zeros(3), self.curve[f][1], sims) for f in fams}
            vz = {}
            for r in rows:
                if r["ab"] is not None and (r["family"], r["vault"]) not in vz:
                    a, b = r["ab"]
                    vz[(r["family"], r["vault"])] = rng.gamma(a, 1.0 / b, sims)
            if self.hot is not None:
                opts, pw, hd = [], [], {}
                for k, g in self.hot["shapes"].items():
                    os_ = sorted(g)
                    ll = np.array([g[o][0] for o in os_])
                    p_in = np.exp(ll - ll.max())
                    p_in /= p_in.sum()
                    for o, p in zip(os_, p_in):
                        opts.append((k, o))
                        pw.append(self.hot["weights"][k] * p)
                        hd[(k, o)] = rng.multivariate_normal(np.zeros(2), g[o][2], sims)
                pw = np.array(pw) / np.sum(pw)
                pick = rng.choice(len(opts), size=sims, p=pw)
        for j, r in enumerate(rows):
            f = r.get("curve", r["family"])
            if draws:
                db = dbeta[f]
                scale = np.exp(db[:, 0] + db[:, 1] * r["L"] + db[:, 2] * r["I"])
                z = vz[(r["family"], r["vault"])] if r["ab"] is not None else np.ones(sims)
            else:
                scale, z = np.ones(sims), np.full(sims, r["zbar"])
            base = r["base"] * scale * z
            if r["ramp"] is not None:
                if draws:
                    rm = np.array([r["ramp"][o][0] for o in opts])[pick]
                    xb = np.array([r["ramp"][o][1] for o in opts])[pick]
                    dh = np.array([hd[opts[p]][i] for i, p in enumerate(pick)])
                    base = base * np.minimum(rm * np.exp(np.clip(dh[:, 0] + dh[:, 1] * xb, -20, 20)), 60.0) * self.hot_scale
                else:
                    base = base * sum(self._mean_ramp(r, k) * w for k, w in self.hot["weights"].items()) * self.hot_scale
            mean[:, j] = base + r["spur"]
        mean = self._deplete(rows, quarters, mean)
        echo = self._echo(rows, quarters, mean)
        mean = mean + echo
        if draws and np.isfinite(self.k):
            lam = rng.gamma(self.k, mean / self.k)
        else:
            lam = mean
        return rows, rng.poisson(lam), mean

    def _mean_ramp(self, r, shape):
        g = self.hot["shapes"][shape]
        os_ = sorted(g)
        ll = np.array([g[o][0] for o in os_])
        p = np.exp(ll - ll.max())
        p /= p.sum()
        return float(sum(r["ramp"][(shape, o)][0] * pp for o, pp in zip(os_, p)))

    def _deplete(self, rows, quarters, mean):
        """A cell's drives are used up as they are replaced: each quarter's expected count is taken on the drives that
        survived the quarters before (their replacements are ordinary spares, carried by the echo)."""
        out = mean.copy()
        chains = {}
        for j, r in enumerate(rows):
            chains.setdefault((r["family"], r["vault"], r["hot"]), []).append((quarters.index(r["q"]), j))
        for key, lst in chains.items():
            lst.sort()
            drives = rows[lst[0][1]]["drives"]
            if drives <= 0:
                continue
            surv = np.ones(mean.shape[0])
            for _, j in lst:
                x = mean[:, j] / drives
                out[:, j] = drives * surv * (1.0 - np.exp(-x))
                surv = surv * np.exp(-x)
        return out

    def _echo(self, rows, quarters, mean):
        """Spares installed this year fail early too: each quarter's replacements carry a new drive's infant hazard into
        the quarters after."""
        out = np.zeros_like(mean)
        idx = {}
        for j, r in enumerate(rows):
            idx.setdefault((r["family"], r["vault"], r["hot"]), {})[r["q"]] = j
        for key, byq in idx.items():
            f = key[0] if key[0] in self.curve else "W-22"
            for i, q in enumerate(quarters):
                if q not in byq:
                    continue
                for k2, q2 in enumerate(quarters[i + 1:], start=1):
                    if q2 not in byq:
                        continue
                    x0, x1 = (k2 - 0.5) * 0.25, (k2 + 0.5) * 0.25
                    out[:, byq[q2]] += mean[:, byq[q]] * self._cum(f, np.array([x0]), np.array([x1]))[0]
        return out

    def point(self, quarters):
        rows, counts, mean = self.simulate(quarters, sims=1, draws=False)
        return rows, mean[0]


def agg(keys, draws, by):
    """Totals per group: by(key) gives the group label."""
    lab = [by(k) for k in keys]
    groups = sorted(set(lab))
    idx = {g: [i for i, l in enumerate(lab) if l == g] for g in groups}
    return {g: draws[:, idx[g]].sum(axis=1) for g in groups}


def stayed_vaults(rec, cut):
    """Vaults with drives in service at the cut and no decommissioning before the record's end."""
    d = rec.d
    cut = pd.Timestamp(cut)
    present = set(d[(d.entry <= cut) & (d.exit >= cut)].vault_id)
    ev = rec.events
    gone = set(ev[ev.event_type == "DECOM_START"].vault_id)
    return present - gone


def quarter_actuals(rec, quarters, vaults=None):
    """Replacements per family and quarter as the record shows them (reseats merged, every pull counted)."""
    d = rec.d if vaults is None else rec.d[rec.d.vault_id.isin(vaults)]
    out = {}
    for q in quarters:
        a, b = qbounds(q)
        m = d.event & (d.removal_date >= a) & (d.removal_date < b)
        for f, n in d[m].family.value_counts().items():
            out[(q, f)] = int(n)
    return out


def backtest(rec, sims=2000, **kw):
    """Intervals built the same way at 30 September 2025, scored on the four quarters to 30 September 2026: the share of
    family-quarter cells whose count fell inside its 80 per cent interval."""
    A = Analysis(rec, cut=P.BACKTEST_CUT, **kw)
    rows, counts, mean = A.simulate(P.BACKTEST_Q, sims=sims, draws=(A.spread != "poisson"))
    stayed = stayed_vaults(rec, P.BACKTEST_CUT)
    act = quarter_actuals(rec, P.BACKTEST_Q, vaults=stayed)
    cells = []
    for q in P.BACKTEST_Q:
        for f in FAMS:
            idx = [j for j, r in enumerate(rows) if r["q"] == q and r["family"] == f and r["vault"] in stayed]
            if not idx:
                continue
            t = counts[:, idx].sum(axis=1)
            lo, hi = np.percentile(t, P.BAND[0]), np.percentile(t, P.BAND[1])
            a_ = act.get((q, f), 0)
            cells.append(dict(q=q, family=f, lo=float(lo), hi=float(hi), mean=float(t.mean()), actual=a_, inside=bool(lo <= a_ <= hi)))
    cov = float(np.mean([c["inside"] for c in cells]))
    return cov, cells


def decisions(A, sims=4000):
    """The fourth-quarter spare order per family at the stock-out tolerance, and the hot batch's migrate call."""
    rows, counts, mean = A.simulate(P.FORECAST_Q, sims=sims, draws=(A.spread != "poisson"))
    q4 = P.FORECAST_Q[0]
    spares = {}
    for f in FAMS + ["X-24"]:
        idx = [j for j, r in enumerate(rows) if r["q"] == q4 and r["family"] == f]
        if not idx:
            continue
        t = counts[:, idx].sum(axis=1)
        need = float(np.percentile(t, 100 * (1 - P.COSTS["stockout"])))
        spares[f] = dict(p90=need, mean=float(t.mean()), order=max(int(np.ceil(need)) - P.SPARES_ON_HAND.get(f, 0), 0))
    # migrate: over the 24 months from 1 October 2026 a vault pays when its replacements exceed the break-even share of its
    # 1,200 drives; the batch's own share is the same test for a vault made wholly of the batch
    qs8 = P.FORECAST_Q + ["2027Q4", "2028Q1", "2028Q2", "2028Q3"]
    r8, c8, m8 = A.simulate(qs8, sims=sims, draws=(A.spread != "poisson"))
    hot = [j for j, r in enumerate(r8) if r["hot"]]
    drives = sum(r["drives"] for r in r8 if r["hot"] and r["q"] == qs8[0])
    frac = c8[:, hot].sum(axis=1) / max(drives, 1)
    be = P.COSTS["migrate_vault"] / (P.VAULT_DRIVES * P.COSTS["failure_handling"])
    line = be * P.VAULT_DRIVES
    vaults = {}
    for v in sorted({r["vault"] for r in r8 if r["hot"]}):
        idx = [j for j, r in enumerate(r8) if r["vault"] == v]
        n_hot = sum(r["drives"] for r in r8 if r["vault"] == v and r["hot"] and r["q"] == qs8[0])
        n_all = sum(r["drives"] for r in r8 if r["vault"] == v and r["q"] == qs8[0])
        if n_all <= 0 or n_hot < 0.10 * n_all:
            continue
        x = c8[:, idx].sum(axis=1)
        vaults[v] = dict(drives=int(n_all), batch=int(n_hot), mean=float(x.mean()), p_pays=float((x > line).mean()))
    if A.migrate_rule == "vault":
        pick = sorted(v for v, s in vaults.items() if s["mean"] > line)
    else:
        pick = sorted(vaults) if float(frac.mean()) > be else []
    return dict(spares=spares, frac_mean=float(frac.mean()), frac_p10=float(np.percentile(frac, 10)),
                frac_p90=float(np.percentile(frac, 90)), p_pays=float((frac > be).mean()), breakeven=be, hot_drives=int(drives),
                flip_doubling=flip_doubling(A, be), vaults=vaults, migrate=pick, line=line)


def flip_doubling(A, be):
    """The doubling time (months) at which the hot drives' expected 24-month replacement fraction equals the break-even,
    holding their current annualized rate."""
    h0 = current_rate(A) / 12.0
    target = -np.log(1 - be)
    lo, hi = 0.5, 600.0
    for _ in range(200):
        mid = (lo + hi) / 2
        H = h0 * mid / np.log(2) * (2 ** (24.0 / mid) - 1)
        if H > target:
            lo = mid
        else:
            hi = mid
    return float((lo + hi) / 2)


def current_rate(A):
    """The hot batch's annualized replacement rate at the cut: its last quarter's replacements per drive-year."""
    d = A.d
    a, b = qbounds("%dQ%d" % (A.cut.year, (A.cut.month - 1) // 3 + 1))
    h = d[d.hot]
    lo = np.maximum(h.entry.values.astype("datetime64[D]"), np.datetime64(a.date()))
    hi = np.minimum(h.exit_c.values.astype("datetime64[D]"), np.datetime64((b - pd.Timedelta(days=1)).date()))
    ex = np.clip((hi - lo).astype(float), 0, None).sum() / 365.25
    ev = int((h.ev & (h.exit_c >= a) & (h.exit_c < b)).sum())
    return ev / max(ex, 1e-9)
