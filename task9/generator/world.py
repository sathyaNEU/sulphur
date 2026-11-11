"""task9: the platform's books, run day by day on the real market returns.

The process simulated: a pod is hired with a base edge, loadings on the markets its strategy trades and its own
noise; every trading day it earns its loadings times what a passive holding of those markets earned (market.HOLDING),
plus its edge at its current capital, plus noise. Capital moves the way the platform moves it: once a year at the
January review, up or down with the pod's Sharpe ratio over the year just ended; down by half on a 5 per cent
drawdown from the year's peak, to nothing on 7.5 per cent; new pods are hired at the start of each quarter to keep
about sixty running. The edge per dollar falls as capital grows (C0, THETA). The risk system keeps the gross daily P&L and estimates loadings on its own factor set
(market.RISK_FACTORS); the administrator keeps month-end P&L net of the funding charge.
"""
import numpy as np
import pandas as pd

import market as MK
import params as P


class World:
    def __init__(self, mk=None, seed=P.SEED, theta=P.THETA, kappa=P.KAPPA):
        self.mk = mk or MK.Market()
        self.rng = np.random.default_rng(seed)
        self.theta, self.kappa = theta, kappa
        self.days = self.mk.hold.index[(self.mk.hold.index >= P.LAUNCH) & (self.mk.hold.index <= P.LAST_DAY)]
        self.F = self.mk.hold.loc[self.days]
        self.T = len(self.days)
        years = sorted(set(self.days.year)) + [P.PLAN_YEAR]
        self.gy = {}
        for g in P.GROUP_ORDER:
            sd, prev, cyc = P.GROUPS[g]["gy"], 0.0, {}
            for y in years:
                prev = P.CYCLE * prev + float(self.rng.normal(0.0, sd * np.sqrt(1.0 - P.CYCLE ** 2)))
                cyc[y] = prev
            self.gy[g] = cyc
        self.pods = []
        self._serial = {g: 0 for g in P.GROUP_ORDER}
        for g in P.GROUP_ORDER:
            for _ in range(P.GROUPS[g]["n0"]):
                self._hire(g, 0)
        self.run()

    # ---- hiring
    def _hire(self, g, i):
        G = P.GROUPS[g]
        r = self.rng
        load = {f: float(r.normal(m, s)) for f, (m, s) in G["load"].items()}
        self._serial[g] += 1
        a0 = float(r.normal(*G["a0"]))
        skill = (a0 - G["a0"][0]) / G["a0"][1]
        pod = dict(n=len(self.pods), g=g, serial=self._serial[g], start=i, end=None, load=load,
                   a0=a0, iv=float(G["iv"] * r.uniform(0.8, 1.25)),
                   k0=float(max(P.K_MIN, round(np.exp(np.log(170e6) + P.HIRE_SKILL * skill + r.normal(0.0, 0.25)) / 5e6) * 5e6)), z=r.standard_normal(self.T), why_end=None)
        # PM teams leave on their own (other platforms, retirement) at a steady hazard, whatever their results
        stay = r.exponential(1.0 / P.LEAVE_RATE) * 252.0
        pod["leave"] = int(i + stay) if i + stay < self.T else None
        pod["target"] = pod["k0"]                       # the capital the pod is hired to run
        pod["ramp"] = 1.0 if i == 0 else P.RAMP[0][1]     # founding pods start at their target; new pods ramp up
        pod["cut"] = 1.0                                  # 0.5 after a mid-year halving, until the next review
        pod["K"] = pod["target"] * pod["ramp"]
        self.pods.append(pod)
        return pod

    def active(self, i):
        return [p for p in self.pods if p["start"] <= i and (p["end"] is None or p["end"] > i)]

    # ---- the daily run
    def run(self):
        d, T, F = self.days, self.T, self.F
        fac = {f: F[f].values for f in F.columns}
        gap = np.r_[1.0, (d[1:] - d[:-1]).days] / 365.0 * 252.0      # trading-day units the edge accrues over
        n_max = 400
        self.pnl = np.full((n_max, T), np.nan)
        self.cap = np.full((n_max, T), np.nan)
        self.reviews = []                     # (pod, date, old capital, new capital, reason)
        self.plans = {}                       # plan year: the pods at the January review and the capital it set
        yr = d.year.values
        q_start = np.r_[True, d.quarter[1:] != d.quarter[:-1]]
        ytd, peak, halved = {}, {}, {}
        for i in range(T):
            if i > 0 and yr[i] != yr[i - 1]:
                act = self.active(i)
                new, ramping = self.review(i, P.BUDGET[int(yr[i])])
                self.plans[int(yr[i])] = dict(day=i, pods=[p["n"] for p in act], capital={p["n"]: new.get(p["n"], p["target"] * p["ramp"]) for p in act},
                                             reviewed=sorted(new))
                for p in act:
                    if p["n"] in new:
                        old = p["K"]
                        p["target"] = new[p["n"]]
                        p["cut"] = 1.0
                        p["K"] = p["target"] * p["ramp"]
                        self.reviews.append((p["n"], d[i], old, p["K"], "annual review"))
                for p in self.active(i):
                    ytd[p["n"]], peak[p["n"]], halved[p["n"]] = 0.0, 0.0, False
            if q_start[i] and i > 0:
                while len(self.active(i)) < P.PODS[int(yr[i])]:
                    g = self.rng.choice(P.GROUP_ORDER, p=[P.GROUPS[x]["hire"] for x in P.GROUP_ORDER])
                    p = self._hire(str(g), i)
                    self.reviews.append((p["n"], d[i], 0.0, p["K"], "new pod"))
            for p in self.active(i):
                if p["ramp"] < 1.0:
                    age = i - p["start"]
                    frac = [f for a, f in P.RAMP if age >= a][-1]
                    if frac != p["ramp"]:
                        old = p["K"]
                        p["ramp"] = frac
                        p["K"] = p["target"] * p["ramp"] * p["cut"]
                        self.reviews.append((p["n"], d[i], old, p["K"], "onboarding step"))
                n = p["n"]
                if n not in ytd:
                    ytd[n], peak[n], halved[n] = 0.0, 0.0, False
                    if p["start"] == 0:
                        self.reviews.append((n, d[0], 0.0, p["K"], "launch"))
                K = p["K"]
                beta = sum(b * fac[f][i] for f, b in p["load"].items())
                edge = (p["a0"] * (K / P.C0) ** (-self.theta) + self.gy[p["g"]][int(yr[i])]) / 252.0 * gap[i]
                noise = p["iv"] / np.sqrt(252.0) * p["z"][i]
                x = K * (beta + edge + noise)
                self.pnl[n, i], self.cap[n, i] = x, K
                ytd[n] += x
                peak[n] = max(peak[n], ytd[n])
                # the drawdown is measured on the capital the pod runs before any halving this year
                dd = (peak[n] - ytd[n]) / (p["target"] * p["ramp"])
                if dd >= P.STOP_DD:
                    p["end"], p["why_end"] = i + 1, "stopped"
                    self.reviews.append((n, d[i], K, 0.0, "closed at the drawdown limit"))
                elif p["leave"] is not None and i >= p["leave"]:
                    p["end"], p["why_end"] = i + 1, "left"
                    self.reviews.append((n, d[i], K, 0.0, "PM team left the platform"))
                elif dd >= P.HALVE_DD and not halved[n]:
                    p["cut"], halved[n] = 0.5, True
                    p["K"] = p["target"] * p["ramp"] * p["cut"]
                    self.reviews.append((n, d[i], K, K * 0.5, "halved at the drawdown limit"))
        self.pnl, self.cap = self.pnl[:len(self.pods)], self.cap[:len(self.pods)]

    # ---- the annual review
    def review(self, i, budget, year_end=None):
        """The capital the review sets for each pod past its onboarding schedule, from the record before day i: its
        target moved by its Sharpe ratio over the last three years and its group's over the year just ended, with the
        committee's own judgment, scaled so the platform runs `budget`. Pods still on the schedule keep their target."""
        d, yr = self.days, self.days.year.values
        act = self.active(i)
        ye = int(yr[i - 1]) if year_end is None else year_end
        gs = {}
        for g in P.GROUP_ORDER:
            rows = [p["n"] for p in self.pods if p["g"] == g]
            m = (yr[:i] == ye)
            tot = np.nansum(self.pnl[rows][:, :i][:, m], axis=0)
            cap = np.nansum(self.cap[rows][:, :i][:, m], axis=0)
            ok = cap > 0
            gr = tot[ok] / cap[ok]
            gs[g] = gr.mean() / gr.std() * np.sqrt(252) if ok.sum() > 60 else 0.0
        prop = {}
        for p in act:
            if i - p["start"] < P.RAMP[-1][0]:
                continue
            lo = max(0, i - 756)
            m = ~np.isnan(self.pnl[p["n"], lo:i])
            sr = 0.0
            if m.sum() >= 120:
                ret = self.pnl[p["n"], lo:i][m] / self.cap[p["n"], lo:i][m]
                sr = ret.mean() / ret.std() * np.sqrt(252)
            prop[p["n"]] = p["target"] * np.exp(self.kappa * np.clip(sr, -1.5, 2.5) + P.GROUP_TILT * np.clip(gs[p["g"]], -2.0, 2.5)
                                                + self.rng.normal(0.0, P.DISCRETION))
        ramping = sum(p["target"] for p in act if p["n"] not in prop)
        tgt = {p["n"]: p["target"] for p in act if p["n"] in prop}
        # the committee leaves a pod where it is when the record moves it by less than BAND, and rounds the rest to
        # USD 5 million, spreading the budget over the pods it moves
        fixed = {}
        scale = 1.0
        for _ in range(50):
            free = {n: v for n, v in prop.items() if n not in fixed}
            if not free:
                break
            scale = (budget - ramping - sum(fixed.values())) / sum(free.values())
            moved = {}
            for n, v in free.items():
                x = float(np.clip(v * scale, P.K_MIN, P.K_MAX))
                if abs(x / tgt[n] - 1.0) < P.BAND:
                    moved[n] = tgt[n]
            if not moved:
                break
            fixed.update(moved)
        out = {}
        for n, v in prop.items():
            x = fixed[n] if n in fixed else float(np.clip(v * scale, P.K_MIN, P.K_MAX))
            out[n] = x if n in fixed else max(P.K_MIN, round(x / 5e6) * 5e6)
        return out, ramping

    # ---- the draft plan for the coming year
    def draft(self, budget, lead):
        """The committee's draft for the coming year, made the way every review has been made, on the record to the
        last day: each pod past its onboarding schedule by the plan year's first trading day (`lead` trading days
        after the record ends) gets the review's capital; a pod still on the schedule keeps it."""
        T = self.T
        act = self.active(T - 1)
        save = {p["n"]: p["start"] for p in act}
        for p in act:                                      # ages at the plan year's first day
            p["start"] -= lead
        new, ramping = self.review(T, budget, year_end=int(self.days[-1].year))
        for p in act:
            p["start"] = save[p["n"]]
        out = {}
        for p in act:
            k26 = p["target"] * p["ramp"] if p["n"] not in new else p["target"]
            if p["n"] in new:
                k27 = new[p["n"]]
                chg = "increase" if k27 > k26 * 1.0005 else ("decrease" if k27 < k26 * 0.9995 else "unchanged")
            else:
                k27, chg = p["target"], "onboarding"
            out[p["n"]] = dict(k2026=k26, k2027=k27, change=chg, age=T + lead - p["start"], target=p["target"])
        return out

    # ---- views
    def pod_frame(self):
        rows = []
        for p in self.pods:
            n = p["n"]
            ok = ~np.isnan(self.pnl[n])
            for i in np.where(ok)[0]:
                rows.append((self.days[i], n, p["g"], self.cap[n, i], self.pnl[n, i]))
        return pd.DataFrame(rows, columns=["date", "n", "g", "capital", "pnl"])

    def true_edge(self, p, K, year):
        """The pod's edge a year at capital K in a year (the world's truth; checks only)."""
        return p["a0"] * (K / P.C0) ** (-self.theta) + self.gy[p["g"]][year]
