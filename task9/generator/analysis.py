"""task9: the golden analysis, every sound rival of it and every hurried route, run on the record.

Nothing here reads the prompt. Each function is one method; run() calls the golden's, then each rival's and each
shortcut's, so the bands and the margins in figures.json are measurements. The record is the pods' daily gross P&L
and capital (the risk system's, cleaned), the administrator's month-end P&L, the capital history, the plans and the
public market series; world.py's truth (edges, capacity, loadings) is read only by checks.py.
"""
import numpy as np
import pandas as pd

import params as P

YEAR = 252
SIMS = 4000
BLOCK = 63                 # trading days in a resampled block of the record's market (a quarter)
FLOOR_DAYS = 120           # a pod-year counts for capacity once it has this many trading days


def fall_per_doubling(theta):
    return 1.0 - 2.0 ** (-theta)


class WorldSource:
    """The world's books read straight off the simulation (for scanning worlds); the golden reads record.Record."""

    def __init__(self, W):
        self.days = W.days
        self.hold = W.F
        self.riskf = W.mk.risk.loc[W.days]
        self.hold_alt = {k: v.loc[W.days] for k, v in W.mk.hold_alt.items()}
        self.groups = {p["n"]: p["g"] for p in W.pods}
        self.panel = W.pod_frame()
        self.start_i = {p["n"]: p["start"] for p in W.pods}
        self.level = W.mk.level
        import record as RC
        self.plan_days = RC.nyse_days("2027-01-01", "2027-12-31")
        self.draft = W.draft(P.BUDGET_PLAN, P.LEAD)


class Analysis:
    def __init__(self, src):
        self.src = src
        self.days = src.days
        self.hold = src.hold                                # what a passive holding of each market earned
        self.riskf = src.riskf                              # the risk model's factors
        self.groups = src.groups
        self.panel = src.panel                              # pod x day: capital and gross P&L
        self.start_i = src.start_i
        self.level = src.level
        self.draft = src.draft
        pd_ = src.plan_days
        self.H = len(pd_)                                   # trading days in the plan year
        self.gap = np.r_[(pd_[0] - pd.Timestamp(pd_[0].year - 1, 12, 31)).days, (pd_[1:] - pd_[:-1]).days].astype(float) / 365.0
        self._attr = {}

    # ------------------------------------------------------------------ R3: alpha net of what the markets paid
    def attribution(self, factors="hold", freq="daily", lags=0, own_only=False):
        """Each pod's returns on its capital regressed on the factor set; alpha is the residual mean a year.

        factors 'hold' uses what a passive holding earned (carry included); 'risk' the risk model's factor moves.
        freq 'monthly' fits month sums; lags>0 adds lagged factor terms (summed betas); own_only fits only the
        markets the pod's strategy group trades."""
        key = (factors, freq, lags, own_only)
        if key in self._attr:
            return self._attr[key]
        Fx = {"hold": self.hold, "risk": self.riskf, "hold-fx2": self.src.hold_alt[2], "hold-fx4": self.src.hold_alt[4]}[factors]
        cols = list(Fx.columns)
        out = {}
        for n, g in self.groups.items():
            d = self.panel[self.panel.n == n]
            if len(d) < 60:
                continue
            r = pd.Series((d.pnl / d.capital).values, index=pd.DatetimeIndex(d.date))
            use = cols
            if own_only:
                use = [f for f in P.GROUPS[g]["load"] if f in cols] or cols
            X = Fx.loc[r.index, use]
            if lags:
                parts = [X] + [Fx[use].shift(k).loc[r.index].add_suffix("_l%d" % k) for k in range(1, lags + 1)]
                X = pd.concat(parts, axis=1).fillna(0.0)
            if freq == "monthly":
                per = r.index.to_period("M")
                r2, X2 = r.groupby(per).sum(), X.groupby(per).sum()
                scale = 12.0
            else:
                r2, X2, scale = r, X, float(YEAR)
            A = np.column_stack([np.ones(len(r2)), X2.values])
            coef = np.linalg.lstsq(A, r2.values, rcond=None)[0]
            fitted = X2.values @ coef[1:]
            resid_d = r - (X.values @ coef[1:] if freq == "daily" else pd.Series(0.0, index=r.index))
            if freq == "monthly":
                # daily residual from the monthly betas, so capacity and the simulation read the same series
                resid_d = r - X.values @ coef[1:]
            beta = dict(zip(X2.columns, coef[1:]))
            if lags:
                beta = {f: sum(v for k, v in beta.items() if k == f or k.startswith(f + "_l")) for f in use}
            out[n] = dict(g=g, alpha=float((r2.values - fitted).mean() * scale), beta=beta, resid=resid_d,
                          idio=float(resid_d.std() * np.sqrt(YEAR)), days=len(r), capital=pd.Series(d.capital.values, index=r.index))
        self._attr[key] = out
        return out

    def group_alpha(self, **kw):
        """A group's alpha a year: its pods' alpha P&L over their capital-years, on the record since launch."""
        A = self.attribution(**kw)
        res = {}
        for g in P.GROUP_ORDER:
            num = den = 0.0
            for n, a in A.items():
                if a["g"] != g:
                    continue
                k = a["capital"]
                num += float((a["resid"] * k).sum())
                den += float(k.sum()) / YEAR
            res[g] = num / den if den else float("nan")
        return res

    # ------------------------------------------------------------------ R2: a year's risk
    def group_returns(self, freq="monthly"):
        """A group's P&L over its capital by period: each day's P&L summed over the group's pods, over the period's
        summed P&L divided by the group's average daily capital in the period."""
        p = self.panel.copy()
        p["g"] = p.n.map(self.groups)
        t = p.groupby(["date", "g"]).agg(pnl=("pnl", "sum"), cap=("capital", "sum")).reset_index()
        if freq == "daily":
            t["r"] = t.pnl / t.cap
            return t.pivot(index="date", columns="g", values="r")
        per = {"monthly": "M", "quarterly": "Q", "annual": "Y"}[freq]
        t["per"] = pd.DatetimeIndex(t.date).to_period(per)
        u = t.groupby(["per", "g"]).agg(pnl=("pnl", "sum"), cap=("cap", "mean")).reset_index()
        u["r"] = u.pnl / u.cap
        return u.pivot(index="per", columns="g", values="r")

    def group_risk(self, how="monthly", nw_lags=0):
        if how == "daily":
            R = self.group_returns("daily")
            if nw_lags:
                out = {}
                for g in R.columns:
                    x = R[g].dropna() - R[g].mean()
                    v = (x * x).mean()
                    for k in range(1, nw_lags + 1):
                        v += 2.0 * (1 - k / (nw_lags + 1.0)) * (x * x.shift(k)).mean()
                    out[g] = float(np.sqrt(max(v, 0.0) * YEAR))
                return out
            return {g: float(R[g].std() * np.sqrt(YEAR)) for g in R.columns}
        R = self.group_returns(how)
        k = {"monthly": 12.0, "quarterly": 4.0}[how]
        return {g: float(R[g].std() * np.sqrt(k)) for g in R.columns}

    # ------------------------------------------------------------------ R4: how alpha per dollar falls with capital
    def pod_years(self, factors="hold", per="Y", floor=FLOOR_DAYS):
        """Each pod's alpha a year and mean capital in each calendar year (per "Y") or quarter (per "Q") it ran for
        at least `floor` trading days."""
        A = self.attribution(factors=factors)
        rows = []
        for n, a in A.items():
            res, k = a["resid"], a["capital"]
            key = res.index.year if per == "Y" else res.index.to_period("Q")
            for y in sorted(set(key)):
                m = key == y
                if m.sum() < floor:
                    continue
                rows.append(dict(n=n, g=a["g"], y=str(y), alpha=float(res[m].mean() * YEAR), K=float(k[m].mean()), w=int(m.sum())))
        return pd.DataFrame(rows)

    def ramp_phases(self, factors="hold", upto=504):
        A = self.attribution(factors=factors)
        start = self.start_i
        rows = []
        for n, a in A.items():
            if start[n] == 0:
                continue
            res, k = a["resid"], a["capital"]
            age = np.arange(len(res))
            for lo, hi in [(lo_, hi_) for lo_, hi_ in [(0, 126), (126, 252), (252, 504)] if hi_ <= upto]:
                m = (age >= lo) & (age < hi)
                if m.sum() < 60:
                    continue
                rows.append(dict(n=n, alpha=float(res.values[m].mean() * YEAR), K=float(k.values[m].mean()), w=int(m.sum())))
        return pd.DataFrame(rows)

    @staticmethod
    def fit_theta(D, by=None, weight=False):
        """alpha = a x (K/C0)^-theta by least squares, a common a or one a per `by` (a pod), on a grid of theta."""
        best = None
        w = D.w.values if weight else np.ones(len(D))
        for th in np.round(np.arange(-0.30, 1.2001, 0.005), 3):
            x = (D.K.values / P.C0) ** (-th)
            if by is None:
                a = (w * D.alpha.values * x).sum() / (w * x * x).sum()
                sse = (w * (D.alpha.values - a * x) ** 2).sum()
            else:
                g = D[by].values
                num = pd.Series(w * D.alpha.values * x).groupby(g).transform("sum").values
                den = pd.Series(w * x * x).groupby(g).transform("sum").values
                sse = (w * (D.alpha.values - num / den * x) ** 2).sum()
            if best is None or sse < best[1] - 1e-15:
                best = (float(th), sse)
        return best[0]

    def capacity(self, how="pod", factors="hold"):
        if how == "none":
            return 0.0
        if how == "pooled":
            return self.fit_theta(self.pod_years(factors))
        if how == "pooled-weighted":
            return self.fit_theta(self.pod_years(factors), weight=True)
        if how == "pod":
            return self.fit_theta(self.pod_years(factors), by="n")
        if how == "pod-weighted":
            return self.fit_theta(self.pod_years(factors), by="n", weight=True)
        if how == "pod-quarter":
            return self.fit_theta(self.pod_years(factors, per="Q", floor=40), by="n")
        if how == "ramp":
            return self.fit_theta(self.ramp_phases(factors), by="n")
        if how == "onboard":
            D = self.ramp_phases(factors, upto=252)
            return self.fit_theta(D[D.n.map(D.n.value_counts()) >= 2], by="n")
        if how == "pod200":
            return self.fit_theta(self.pod_years(factors, floor=200), by="n")
        if how == "loglinear":
            # alpha on log2 capital with a constant per pod; the fall per doubling at the average alpha, as theta
            D = self.pod_years(factors)
            x = np.log2(D.K.values)
            xd = x - D.groupby("n").K.transform(lambda k: np.log2(k).mean()).values
            yd = D.alpha.values - D.groupby("n").alpha.transform("mean").values
            b = float((xd * yd).sum() / (xd * xd).sum())
            fall = -b / float(D.alpha.mean())
            return float(-np.log2(1.0 - fall)) if fall < 1 else float("nan")
        raise ValueError(how)

    # ------------------------------------------------------------------ each pod's base edge, and what to expect of it
    def base_edges(self, theta, factors="hold", est="ls"):
        """Each pod's edge a year at C0 from its residual on the record: est "ls" fits the residual on (K/C0)^-theta
        by least squares, "ratio" averages each day's residual scaled back to C0; with the edge's standard error
        from the pod's own residual noise."""
        out = {}
        for n, a in self.attribution(factors=factors).items():
            x = (a["capital"].values / P.C0) ** (-theta)
            r = a["resid"].values
            if est == "ls":
                b = float((r * x).sum() / (x * x).sum())
                e = r - b * x
                sd = float(e.std() * np.sqrt(YEAR))
                se = sd / np.sqrt((x * x).sum() / YEAR)
            else:
                z = r / x
                b = float(z.mean())
                sd = float(z.std() * np.sqrt(YEAR))
                se = sd / np.sqrt(len(z) / YEAR)
            out[n] = dict(g=a["g"], a=b * YEAR, se=se, sd=sd, days=a["days"])
        return out

    def expected_edges(self, theta, factors="hold", shrink="group", est="ls"):
        """The edge to expect of each pod: its own estimate pulled toward its group's by the share of its spread the
        group's pods really differ by (empirical Bayes, a normal prior per group). shrink "group" fits each group's
        prior by the method of moments, "group-ml" by maximum likelihood, "pooled-tau" with one spread for every
        group around its own mean; None takes each pod's own estimate as it stands."""
        E = self.base_edges(theta, factors, est)
        if shrink is None:
            out = {n: e["a"] for n, e in E.items()}
            for n, g in self.groups.items():
                if n not in out:
                    peers = [e for e in E.values() if e["g"] == g and e["days"] >= FLOOR_DAYS]
                    out[n] = float(np.average([e["a"] for e in peers], weights=[e["days"] for e in peers]))
            return out, {}
        fit = {}
        for g in P.GROUP_ORDER:
            rows = [e for e in E.values() if e["g"] == g and e["days"] >= FLOOR_DAYS]
            fit[g] = (np.array([e["a"] for e in rows]), np.array([e["se"] ** 2 for e in rows]))

        def moments(a, v, tau2=None):
            tau2 = max(0.0, float(a.var(ddof=1) - v.mean())) if tau2 is None else tau2
            for _ in range(500):
                w = 1.0 / (tau2 + v)
                mu = float((w * a).sum() / w.sum())
                t_new = max(0.0, float((w * ((a - mu) ** 2 - v)).sum() / w.sum()))
                if abs(t_new - tau2) < 1e-14:
                    break
                tau2 = t_new
            return mu, tau2

        def ml(a, v):
            best = None
            for t in np.linspace(0.0, 0.08, 1601) ** 2:
                w = 1.0 / (t + v)
                mu = float((w * a).sum() / w.sum())
                ll = float(-0.5 * (np.log(t + v) + (a - mu) ** 2 / (t + v)).sum())
                if best is None or ll > best[0]:
                    best = (ll, mu, float(t))
            return best[1], best[2]

        prior = {}
        if shrink == "group":
            prior = {g: moments(*fit[g]) for g in P.GROUP_ORDER}
        elif shrink == "group-simple":
            for g in P.GROUP_ORDER:
                a_, v_ = fit[g]
                prior[g] = (float(a_.mean()), max(0.0, float(((a_ - a_.mean()) ** 2).mean() - v_.mean())))
        elif shrink == "group-ml":
            prior = {g: ml(*fit[g]) for g in P.GROUP_ORDER}
        elif shrink == "pooled-tau":
            tau2 = 0.02 ** 2
            for _ in range(200):
                mus = {g: float(((1.0 / (tau2 + v)) * a).sum() / (1.0 / (tau2 + v)).sum()) for g, (a, v) in fit.items()}
                num = sum(float(((1.0 / (tau2 + v)) * ((a - mus[g]) ** 2 - v)).sum()) for g, (a, v) in fit.items())
                den = sum(float((1.0 / (tau2 + v)).sum()) for g, (a, v) in fit.items())
                t_new = max(0.0, num / den)
                if abs(t_new - tau2) < 1e-14:
                    break
                tau2 = t_new
            prior = {g: (mus[g], tau2) for g in P.GROUP_ORDER}
        else:
            raise ValueError(shrink)
        out = {}
        for n, e in E.items():
            mu, tau2 = prior[e["g"]]
            B = tau2 / (tau2 + e["se"] ** 2)
            out[n] = mu + B * (e["a"] - mu)
        for n, g in self.groups.items():               # a pod with too short a record to read: its group's
            if n not in out:
                out[n] = prior[g][0]
        return out, prior

    def pod_model(self, n, factors="hold"):
        """A pod's loadings and own noise from its record, or its group's averages when its record is too short."""
        A = self.attribution(factors=factors)
        if n in A:
            return A[n]["beta"], A[n]["idio"]
        g = self.groups[n]
        peers = [a for a in A.values() if a["g"] == g and a["days"] >= FLOOR_DAYS]
        keys = sorted({k for a in peers for k in a["beta"]})
        beta = {k: float(np.mean([a["beta"].get(k, 0.0) for a in peers])) for k in keys}
        return beta, float(np.mean([a["idio"] for a in peers]))

    # ------------------------------------------------------------------ the plan year, simulated
    def year_paths(self, sims=SIMS, block=BLOCK, seed=P.SEED + 27, demean=True, iid=False):
        """Market paths for a plan year resampled from the record's own days in blocks of `block` trading days, which
        keeps each market's serial dependence and the markets' co-movement inside a block; demeaned, since the plan
        carries market returns at zero (iid=True resamples single days)."""
        F = self.hold.copy()
        if demean:
            F = F - F.mean()
        V = F.values
        T = len(V)
        rng = np.random.default_rng(seed)
        b = 1 if iid else block
        nb = int(np.ceil(self.H / b))
        starts = rng.integers(0, T, size=(sims, nb))
        idx = (starts[:, :, None] + np.arange(b)[None, None, :]) % T
        idx = idx.reshape(sims, nb * b)[:, :self.H]
        return V[idx], list(F.columns)

    def capital_paths(self, plan, use="k2027"):
        """Each planned pod's capital on each trading day of the plan year: its planned figure, or its onboarding
        schedule's step on the day it falls due."""
        out = {}
        for n, r in plan.items():
            if r["change"] == "onboarding":
                age = r["age"] + np.arange(self.H)
                frac = np.ones(self.H)
                for lo, f in P.RAMP:
                    frac[age >= lo] = f
                out[n] = r["target"] * frac
            else:
                out[n] = np.full(self.H, r[use])
        return out

    def simulate(self, paths_K, edges, theta, factors="hold", stops=True, payout="pod", paths=None, seed=P.SEED + 29):
        """The plan year: each pod's daily P&L at its capital, its drawdown rules, its funding and its payout."""
        Fp, cols = paths if paths is not None else self.year_paths()
        S = Fp.shape[0]
        bill = float(self.level.DTB3.loc[:P.LAST_DAY].dropna().iloc[-1]) / 100.0
        H, gap = self.H, self.gap
        net = np.zeros(S)
        gross_all = np.zeros(S)
        fund_all = np.zeros(S)
        pods = {}
        for n in sorted(paths_K):
            K = paths_K[n]
            beta, idio = self.pod_model(n, factors)
            b = np.zeros(len(cols))
            for f, v in beta.items():
                if f in cols:
                    b[cols.index(f)] = v
            mkt = Fp @ b
            rng = np.random.default_rng(seed + 1000 + int(n))
            noise = rng.standard_normal((S, H)) * idio / np.sqrt(YEAR)
            edge = edges[n] * (K / P.C0) ** (-theta) * gap
            ret = mkt + edge[None, :] + noise
            if stops:
                pnl = np.zeros((S, H))
                cum = np.zeros(S)
                peak = np.zeros(S)
                cut = np.ones(S)
                alive = np.ones(S)
                capd = np.zeros((S, H))
                for t in range(H):
                    x = K[t] * cut * alive * ret[:, t]
                    pnl[:, t] = x
                    cum += x
                    peak = np.maximum(peak, cum)
                    dd = (peak - cum) / K[t]
                    stop = (dd >= P.STOP_DD) & (alive > 0)
                    alive = np.where(stop, 0.0, alive)
                    half = (dd >= P.HALVE_DD) & (cut > 0.5) & (alive > 0)
                    cut = np.where(half, 0.5, cut)
                    capd[:, t] = K[t] * cut * alive
                fund = P.FIN_SHARE * (P.FIN_SPREAD + bill) * (capd * gap[None, :]).sum(axis=1)
                trade = pnl.sum(axis=1)
            else:
                trade = (K[None, :] * ret).sum(axis=1)
                fund = np.full(S, P.FIN_SHARE * (P.FIN_SPREAD + bill) * float((K * gap).sum()))
            after = trade - fund
            pay = P.PAYOUT * np.maximum(after, 0.0) if payout == "pod" else np.zeros(S)
            pods[n] = dict(trade=float(trade.mean()), fund=float(fund.mean()), pay=float(pay.mean()), net=float((after - pay).mean()),
                           draws=after - pay)
            net += after - pay
            gross_all += trade
            fund_all += fund
        if payout == "rate":                  # the payout rate on the expected year, booked once
            net = gross_all - fund_all - P.PAYOUT * max(float((gross_all - fund_all).mean()), 0.0)
        net = net - P.PLATFORM_COST_2027
        return dict(mean=float(net.mean()), p10=float(np.percentile(net, 10)), p90=float(np.percentile(net, 90)), pods=pods, draws=net)

    def marginals(self, plan, edges, theta, factors="hold", paths=None, how="marginal", **kw):
        """Each increase's expected net P&L per dollar it adds: the pod at its 2027 figure against its 2026 figure on
        the same simulated years (how="average" takes instead the pod's expected net return on its whole 2027 capital,
        the hurried reading of the hurdle)."""
        out = {}
        for n, r in plan.items():
            if r["change"] != "increase":
                continue
            k1 = {n: np.full(self.H, r["k2027"])}
            b = self.simulate(k1, edges, theta, factors, paths=paths, **kw)["pods"][n]["net"]
            if how == "average":
                out[n] = b / r["k2027"]
                continue
            k0 = {n: np.full(self.H, r["k2026"])}
            a = self.simulate(k0, edges, theta, factors, paths=paths, **kw)["pods"][n]["net"]
            out[n] = (b - a) / (r["k2027"] - r["k2026"])
        return out
