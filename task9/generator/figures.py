"""task9: every graded figure, its band and the hurried routes, computed on the cut pack (generator/figures.json).

The golden runs first; each band is the span of the sound rivals run on the same record (named below), widened by a
stated margin for simulation noise; each hurried route is the same machinery with one judgment taken the quick way.
"""
import json

import numpy as np

import analysis as AN
import params as P
import record as RC

SIMS = 10000
M_NET = 0.015          # a forecast band's margin for simulation noise, as a share of the golden
M_TAIL = 12e6          # the same for a percentile of the plan year, USD
M_ALPHA = 0.0015       # a group's alpha a year
M_RISK = 0.04          # a group's risk over a year, as a share of the golden
M_FALL = 0.01          # the fall per doubling
SOUND_THETA = ("pod", "pod-weighted", "pod-quarter", "ramp", "onboard", "pod200")
EPS = 0.0015           # an increase whose margin over the hurdle any rival comes within this of is either way


def rnd(x, k):
    return float(round(x, k))


class Run:
    def __init__(self, tgt, sims=SIMS):
        self.R = RC.Record(tgt)
        self.A = AN.Analysis(self.R)
        self.sims = sims
        A = self.A
        self.theta = {h: A.capacity(h) for h in ("pod", "pod-weighted", "pod-quarter", "ramp", "onboard", "pod200", "pooled")}
        sound = [self.theta[h] for h in SOUND_THETA]
        self.theta_lo, self.theta_hi = min(sound), max(sound)
        self.paths = {b: A.year_paths(sims=sims, block=b) for b in (21, 63, 126)}
        self.paths["iid"] = A.year_paths(sims=sims, iid=True)
        self.KP = A.capital_paths(A.draft)

    def plan(self, fac="hold", theta=None, shrink="group", stops=True, block=63, hurdle="marginal", est="ls"):
        """The draft year under one set of choices: mean, P10, P90 and each increase's net P&L per dollar added (or,
        hurdle="average", its net return on its whole 2027 capital)."""
        A = self.A
        th = self.theta["pod"] if theta is None else theta
        E, _ = A.expected_edges(th, fac, shrink, est)
        paths = self.paths[block]
        r = A.simulate(self.KP, E, th, fac, paths=paths, stops=stops)
        m = A.marginals(A.draft, E, th, fac, paths=paths, stops=stops, how=hurdle)
        out = dict(mean=r["mean"], p10=r["p10"], p90=r["p90"], marg=m, edges=E, sim=r)
        return out

    def without(self, fail, fac="hold", theta=None, shrink="group", stops=True, block=63, hurdle=None, est="ls"):
        A = self.A
        th = self.theta["pod"] if theta is None else theta
        E, _ = A.expected_edges(th, fac, shrink, est)
        KP = dict(self.KP)
        for n in fail:
            KP[n] = np.full(A.H, A.draft[n]["k2026"])
        return A.simulate(KP, E, th, fac, paths=self.paths[block], stops=stops)["mean"]


def compute(tgt, sims=SIMS):
    X = Run(tgt, sims)
    A, R = X.A, X.R
    code = R.code
    F = {}
    G = P.GROUP_ORDER
    name = {g: P.GROUPS[g]["name"] for g in G}
    # ---- R1: each group's alpha a year since launch, net of what a passive holding of its markets earned
    gold = A.group_alpha(factors="hold")
    riv = {"monthly regression": A.group_alpha(factors="hold", freq="monthly"),
           "one lag of each factor": A.group_alpha(factors="hold", lags=1),
           "only the group's own markets": A.group_alpha(factors="hold", own_only=True),
           "a two-a-side carry basket": A.group_alpha(factors="hold-fx2"),
           "a four-a-side carry basket": A.group_alpha(factors="hold-fx4"),
           "one regression for each group's whole book": group_level_alpha(A)}
    F["R1_alpha"] = {name[g]: rnd(gold[g] * 100, 2) for g in G}
    F["R1_bands"] = {name[g]: [rnd((min([gold[g]] + [r[g] for r in riv.values()]) - M_ALPHA) * 100, 2),
                               rnd((max([gold[g]] + [r[g] for r in riv.values()]) + M_ALPHA) * 100, 2)] for g in G}
    F["R1_rivals"] = {k: {name[g]: rnd(v[g] * 100, 2) for g in G} for k, v in riv.items()}
    F["R1_risk_model"] = {name[g]: rnd(v * 100, 2) for g, v in A.group_alpha(factors="risk").items()}
    raw = raw_roc(A)
    F["R1_raw"] = {name[g]: rnd(raw[g] * 100, 2) for g in G}
    # ---- R2: each group's standard deviation of P&L over a year, as a percent of capital
    gm = A.group_risk("monthly")
    rr = {"quarterly P&L": A.group_risk("quarterly"), "daily P&L with 21 lags of autocovariance": A.group_risk("daily", nw_lags=21)}
    F["R2_risk"] = {name[g]: rnd(gm[g] * 100, 2) for g in G}
    F["R2_bands"] = {name[g]: [rnd(min([gm[g]] + [r[g] for r in rr.values()]) * (1 - M_RISK) * 100, 2),
                               rnd(max([gm[g]] + [r[g] for r in rr.values()]) * (1 + M_RISK) * 100, 2)] for g in G}
    F["R2_rivals"] = {k: {name[g]: rnd(v[g] * 100, 2) for g in G} for k, v in rr.items()}
    F["R2_daily"] = {name[g]: rnd(v * 100, 2) for g, v in A.group_risk("daily").items()}
    # ---- R3: how much alpha per dollar falls when a pod's capital doubles
    fall = {k: AN.fall_per_doubling(v) for k, v in X.theta.items()}
    F["theta"] = {k: rnd(v, 3) for k, v in X.theta.items()}
    F["R3_fall"] = rnd(fall["pod"] * 100, 1)
    lo = min(fall[k] for k in SOUND_THETA)
    hi = max(fall[k] for k in SOUND_THETA)
    F["R3_band"] = [rnd((lo - M_FALL) * 100, 1), rnd((hi + M_FALL) * 100, 1)]
    F["R3_partly"] = [rnd((lo - 4 * M_FALL) * 100, 1), rnd((hi + 4 * M_FALL) * 100, 1)]
    F["R3_rivals"] = {k: rnd(v * 100, 1) for k, v in fall.items()}
    # ---- R4, R5, R6: the draft year
    g0 = X.plan()
    rivals = {"capacity at the lowest sound estimate": dict(theta=X.theta_lo),
              "capacity at the highest sound estimate": dict(theta=X.theta_hi),
              "group priors fitted by maximum likelihood": dict(shrink="group-ml"),
              "one spread for every group's prior": dict(shrink="pooled-tau"),
              "a simple average of the group's pods as the prior's centre": dict(shrink="group-simple"),
              "each pod's edge as the average of its days scaled to USD 150 million": dict(est="ratio"),
              "markets resampled a month at a time": dict(block=21),
              "markets resampled half a year at a time": dict(block=126)}
    rv = {k: X.plan(**v) for k, v in rivals.items()}
    allm = [g0] + list(rv.values())
    F["R4_net"] = rnd(g0["mean"] / 1e6, 1)
    F["R4_band"] = [rnd(min(r["mean"] for r in allm) * (1 - M_NET) / 1e6, 1), rnd(max(r["mean"] for r in allm) * (1 + M_NET) / 1e6, 1)]
    F["R4_partly"] = [rnd(F["R4_band"][0] - 0.05 * F["R4_net"], 1), rnd(F["R4_band"][1] + 0.05 * F["R4_net"], 1)]
    F["R4_rivals"] = {k: rnd(r["mean"] / 1e6, 1) for k, r in rv.items()}
    F["R5_range"] = {"P10": rnd(g0["p10"] / 1e6, 1), "P90": rnd(g0["p90"] / 1e6, 1)}
    F["R5_bands"] = {"P10": [rnd((min(r["p10"] for r in allm) - M_TAIL) / 1e6, 1), rnd((max(r["p10"] for r in allm) + M_TAIL) / 1e6, 1)],
                     "P90": [rnd((min(r["p90"] for r in allm) - M_TAIL) / 1e6, 1), rnd((max(r["p90"] for r in allm) + M_TAIL) / 1e6, 1)]}
    F["R5_rivals"] = {k: {"P10": rnd(r["p10"] / 1e6, 1), "P90": rnd(r["p90"] / 1e6, 1)} for k, r in rv.items()}
    inc = sorted(g0["marg"], key=lambda n: code[n])
    lo_m = {n: min(r["marg"][n] for r in allm) for n in inc}
    hi_m = {n: max(r["marg"][n] for r in allm) for n in inc}
    fail = [n for n in inc if hi_m[n] + EPS < P.HURDLE]
    clear = [n for n in inc if lo_m[n] - EPS > P.HURDLE]
    either = [n for n in inc if n not in fail and n not in clear]
    F["R6_fail"] = [code[n] for n in fail]
    F["R6_either"] = [code[n] for n in either]
    F["R6_pass"] = [code[n] for n in clear]
    F["R6_margins"] = {code[n]: dict(golden=rnd(g0["marg"][n] * 100, 2), low=rnd(lo_m[n] * 100, 2), high=rnd(hi_m[n] * 100, 2)) for n in inc}
    # ---- R7: the year without the failing increases (either-way pods at their draft figure, and dropped, both in band)
    w0 = X.without(fail)
    wv = [X.without(fail, **v) for v in rivals.values()]
    w_alt = X.without(fail + either)
    F["R7_net"] = rnd(w0 / 1e6, 1)
    F["R7_band"] = [rnd(min([w0, w_alt] + wv) * (1 - M_NET) / 1e6, 1), rnd(max([w0, w_alt] + wv) * (1 + M_NET) / 1e6, 1)]
    F["R7_partly"] = [rnd(F["R7_band"][0] - 0.05 * F["R7_net"], 1), rnd(F["R7_band"][1] + 0.05 * F["R7_net"], 1)]
    F["R7_with_either_dropped"] = rnd(w_alt / 1e6, 1)
    # ---- the hurried routes: one judgment the quick way at a time, then the careful but hurried pass
    hur = {"risk model's factors": dict(fac="risk"), "each pod's own record": dict(shrink=None), "no drawdown rules": dict(stops=False),
           "capacity across pods": dict(theta=X.theta["pooled"], shrink=None), "daily resampling": dict(block="iid"),
           "average return at the new size": dict(hurdle="average"),
           "careful but hurried": dict(fac="risk", block="iid", hurdle="average"),
           "careful but hurried, carry netted": dict(block="iid", hurdle="average"),
           "careful but hurried, a year's horizon": dict(fac="risk", hurdle="average"),
           "careful but hurried, the added dollar": dict(fac="risk", block="iid")}
    routes = {}
    for k, v in hur.items():
        r = X.plan(**v)
        f = [n for n in inc if r["marg"][n] < P.HURDLE]
        routes[k] = dict(mean=rnd(r["mean"] / 1e6, 1), p10=rnd(r["p10"] / 1e6, 1), p90=rnd(r["p90"] / 1e6, 1), fail=[code[n] for n in f],
                         without=rnd(X.without(f, **{a: b for a, b in v.items()}) / 1e6, 1),
                         margins={code[n]: rnd(r["marg"][n] * 100, 2) for n in inc})
    F["routes"] = routes
    q = quick_plan(X)
    F["quick"] = q
    # ---- the workbook's tables
    F["increases"] = [dict(pod=code[n], group=name[R.groups[n]], k2026=rnd(A.draft[n]["k2026"] / 1e6, 1), k2027=rnd(A.draft[n]["k2027"] / 1e6, 1),
                           added=rnd((A.draft[n]["k2027"] - A.draft[n]["k2026"]) / 1e6, 1), per_dollar=rnd(g0["marg"][n] * 100, 2),
                           added_net=rnd(g0["marg"][n] * (A.draft[n]["k2027"] - A.draft[n]["k2026"]) / 1e6, 2),
                           call="fails" if n in fail else ("either way" if n in either else "passes")) for n in inc]
    sim = g0["sim"]["pods"]
    F["pods"] = [dict(pod=code[n], group=name[R.groups[n]], change=A.draft[n]["change"], k2026=rnd(A.draft[n]["k2026"] / 1e6, 1),
                      k2027=rnd(A.draft[n]["k2027"] / 1e6, 1), edge_c0=rnd(g0["edges"][n] * 100, 2),
                      alpha_2027=rnd(g0["edges"][n] * (A.draft[n]["k2027"] / P.C0) ** (-X.theta["pod"]) * 100, 2),
                      trade=rnd(sim[n]["trade"] / 1e6, 2), funding=rnd(sim[n]["fund"] / 1e6, 2), payout=rnd(sim[n]["pay"] / 1e6, 2),
                      net=rnd(sim[n]["net"] / 1e6, 2)) for n in sorted(A.draft, key=lambda n: code[n])]
    F["platform"] = dict(trade=rnd(sum(v["trade"] for v in sim.values()) / 1e6, 1), funding=rnd(sum(v["fund"] for v in sim.values()) / 1e6, 1),
                         payouts=rnd(sum(v["pay"] for v in sim.values()) / 1e6, 1), costs=rnd(P.PLATFORM_COST_2027 / 1e6, 1),
                         capital_2026=rnd(sum(r["k2026"] for r in A.draft.values()) / 1e6, 1),
                         capital_2027=rnd(sum(r["k2027"] for r in A.draft.values()) / 1e6, 1),
                         bill=rnd(float(A.level.DTB3.loc[:P.LAST_DAY].dropna().iloc[-1]), 2), pods=len(A.draft),
                         increases=len(inc), sims=sims)
    tday = R.mk.hold.index[(R.mk.hold.index >= R.days[0]) & (R.mk.hold.index <= R.days[-1])]
    F["record"] = dict(days=len(R.days), pods=len(R.groups), dupes=R.n_dupes, first=str(R.days[0].date()), last=str(R.days[-1].date()),
                       missing=[str(t.date()) for t in tday if t not in set(R.days)], active=len(A.draft),
                       stopped=int(sum(1 for s in R.status.values() if s.startswith("Closed"))), left=int(sum(1 for s in R.status.values() if s.startswith("PM team"))))
    F["past_plans"] = past_plans(tgt)
    pp = F["past_plans"]
    F["past_gap"] = rnd(sum(v["expected"] - v["earned"] for v in pp.values()) / len(pp), 1)
    F["past_over"] = sum(1 for v in pp.values() if v["expected"] > v["earned"])
    F["R6_added"] = rnd(sum(x["added"] for x in F["increases"] if x["pod"] in F["R6_fail"]), 1)
    F["conventions"] = dict(hurdle_pct=P.HURDLE * 100, payout_pct=P.PAYOUT * 100, funding_share_pct=P.FIN_SHARE * 100,
                            funding_spread_pct=P.FIN_SPREAD * 100, c0_usd_m=P.C0 / 1e6, floor_days=AN.FLOOR_DAYS, nw_lags=21,
                            halve_pct=P.HALVE_DD * 100, close_pct=P.STOP_DD * 100)
    return F


def past_plans(tgt):
    """Each completed plan year: what the approved plan expected of its pods, net, against what those pods went on to
    earn (the administrator's net P&L, payouts included, less the year's platform costs)."""
    import os
    import pandas as pd
    from openpyxl import load_workbook
    import pack as PK
    cmap = pd.read_csv(os.path.join(tgt, PK.F["codes"]), dtype=str)
    to_new = dict(zip(cmap.old_pod_code, cmap.new_book_id))
    adm = pd.read_csv(os.path.join(tgt, PK.F["admin"]), dtype={"sleeve": str})
    adm["pod"] = adm.sleeve.map(lambda c: to_new.get(c, c))
    adm["year"] = adm.period_end.str[:4].astype(int)
    wb = load_workbook(os.path.join(tgt, PK.F["plans"]), data_only=True)
    out = {}
    for y in P.PLAN_YEARS:
        if y >= P.LAST_DAY.year:
            continue
        ws = wb["Plan %d" % y]
        pods, net, costs = [], None, None
        for row in ws.iter_rows(min_row=4, values_only=True):
            if row[0] and row[1] and isinstance(row[2], (int, float)):
                pods.append(to_new.get(row[0], row[0]))
            if row[0] == "Expected net P&L":
                net = float(row[4])
            if row[0] == "Platform costs":
                costs = -float(row[4])
        got = float(adm[(adm.year == y) & adm.pod.isin(pods)].net_pnl.sum()) / 1e6 - costs
        out[str(y)] = dict(expected=rnd(net, 1), earned=rnd(got, 1), pods=len(pods))
    return out


def group_level_alpha(A):
    """A group's alpha from one regression of the whole group's daily return on capital on the holdings."""
    G = A.group_returns("daily")
    out = {}
    for g in P.GROUP_ORDER:
        r = G[g].dropna()
        Z = np.column_stack([np.ones(len(r)), A.hold.loc[r.index].values])
        out[g] = float(np.linalg.lstsq(Z, r.values, rcond=None)[0][0] * AN.YEAR)
    return out


def raw_roc(A):
    """A group's return on capital since launch with nothing taken out (the quick reading)."""
    out = {}
    p = A.panel
    for g in P.GROUP_ORDER:
        d = p[p.n.map(A.groups) == g]
        out[g] = float(d.pnl.sum() / d.capital.sum() * AN.YEAR)
    return out


def quick_plan(X):
    """The plan priced the way the committee has always priced it: each pod's return on capital over the three years
    to the record's end, or its group's when it has less than six months, times its 2027 capital, less funding,
    payouts and costs; an increase earns that same return less funding and payout."""
    A, R = X.A, X.R
    p = A.panel
    end = R.days[-1]
    lo = end - np.timedelta64(365 * 3, "D")
    w = p[p.date > lo]
    groc = {g: float(w[w.n.map(A.groups) == g].pnl.sum() / w[w.n.map(A.groups) == g].capital.sum() * AN.YEAR) for g in P.GROUP_ORDER}
    bill = float(A.level.DTB3.loc[:P.LAST_DAY].dropna().iloc[-1]) / 100.0
    fr = P.FIN_SHARE * (bill + P.FIN_SPREAD)
    tot, fails = 0.0, []
    for n, r in A.draft.items():
        d = w[w.n == n]
        roc = float(d.pnl.sum() / d.capital.sum() * AN.YEAR) if len(d) >= 126 else groc[R.groups[n]]
        k = r["k2027"] if r["change"] != "onboarding" else float(np.mean(X.KP[n]))
        e = roc * k - fr * k
        tot += e - P.PAYOUT * max(e, 0.0)
        if r["change"] == "increase" and (roc - fr) * (1 - P.PAYOUT) < P.HURDLE:
            fails.append(R.code[n])
    return dict(mean=rnd((tot - P.PLATFORM_COST_2027) / 1e6, 1), fail=sorted(fails))


def write(F, path):
    json.dump(F, open(path, "w"), indent=1, sort_keys=True)
