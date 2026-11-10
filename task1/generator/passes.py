"""The golden and the hurried routes, end to end, on the clean tables (or on the tables golden.load() rebuilds from
the pack). Every graded figure comes out of golden(); every effort pass and rival comes out of the routes here."""
import math

import numpy as np
import pandas as pd

import analysis as An
import params as P

CUT, H = P.CUT, P.HORIZON
SPAN = H - CUT
MONTHS = list(range(CUT + 1, H + 1))


class Book:
    """Everything the routes share, computed once per pack."""

    def __init__(self, F):
        self.F = F
        self.T = An.terms(F)
        self.A = An.account_actives(F)
        self.st = An.business_state(F, self.T)
        self.E = An.renewal_events(F, self.T, self.A)
        self.Tp = An.team_panel(F)
        self.S = An.pipeline_tables(F)
        self.growth = An.growth_model(F, self.A, self.T)
        self.moves = An.team_moves(self.Tp)
        self.upr = An.upgrade_rate(self.Tp, F)
        self.W, self.per_seat = An.deal_value(F)
        cur = self.Tp[self.Tp["m"] == CUT]
        self.open_team = float((cur["seats"] * cur["cur"].map(P.TEAM_PRICE) * 12 * cur["cur"].map(An.FX)).sum())
        self.open_bus = float(self.st["arr"].sum())


# ------------------------------------------------------------------------------------------------ pipeline timing
def win_timing(B, keys=("stage", "sb"), lookback_from=12):
    """P(won j months after a month-end snapshot), j = 1..SPAN, by stage and staleness, from snapshots with a full
    follow-up window."""
    S = B.S
    hist = S[(S["m"] <= CUT - SPAN) & (S["m"] >= lookback_from)].copy()
    hist["lag"] = hist["won_m"] - hist["m"]
    out = {}
    for k, g in hist.groupby(list(keys)):
        n = len(g)
        out[k] = np.array([float(((g["lag"] == j)).sum()) / n for j in range(1, SPAN + 1)])
    return out


def creation_timing(B, lookback_from=12):
    S, C = B.S, B.F["closed"]
    created = pd.concat([S[["id", "created", "seats"]], C[["id", "created", "seats"]]]).drop_duplicates("id")
    won = C[C["outcome"] == "won"].set_index("id")["m"]
    old = created[(created["created"] >= lookback_from) & (created["created"] <= CUT - SPAN)].copy()
    old["lag"] = old["id"].map(won) - old["created"]
    lagp = np.array([float((old["lag"] == j).mean()) for j in range(0, SPAN + 1)])
    rate = created[(created["created"] >= P.PRICE_RISE) & (created["created"] <= CUT)].groupby("created").size()
    seats = float(created[created["created"] >= P.PRICE_RISE]["seats"].mean())
    return float(rate.mean()), seats, lagp


def new_business_expect(B, crm=False, runrate=False, stage_only=False, keys=None):
    """Expected new Business ARR signed in each forecast month: (open deals, deals not yet created, upgrades)."""
    if runrate:
        L = B.F["lines"]
        nw = L[(L["type"] == "new") & (L["m"] > CUT - 12) & (L["m"] <= CUT)]
        per_m = float((nw["seats"] * nw["price"] * 12 * nw["cur"].map(An.FX)).sum()) / 12.0
        return np.zeros(SPAN), np.full(SPAN, per_m), np.zeros(SPAN)
    op = B.S[B.S["m"] == CUT]
    if crm:
        val = float((op["seats"] * B.per_seat * np.array(P.CRM_PROB)[op["stage"].values] / 100.0).sum())
        open_path = np.full(SPAN, val / SPAN)
    else:
        keys = keys or (("stage",) if stage_only else ("stage", "sb"))
        tim = win_timing(B, keys=keys)
        open_path = np.zeros(SPAN)
        for r in op.itertuples():
            key = tuple(getattr(r, k) for k in keys)
            open_path += tim.get(key, np.zeros(SPAN)) * r.seats * B.per_seat
    lam, seats, lagp = creation_timing(B)
    fut = np.zeros(SPAN)
    for i, c in enumerate(MONTHS):
        for j in range(0, SPAN - i):
            fut[i + j] += lam * lagp[j] * seats * B.per_seat
    up = upgrades_path(B)
    return open_path, fut, up


def upgrades_path(B):
    acc, L = B.F["acc"], B.F["lines"]
    new = L[L["type"] == "new"].set_index("acc")
    ups = acc[(acc["source"] == "upgrade") & (acc["start"] >= P.PRICE_RISE) & (acc["acc"].isin(new.index))]
    per = float(np.mean([new.loc[a, "seats"] * new.loc[a, "price"] * 12 * An.FX[new.loc[a, "cur"]]
                         for a in ups["acc"]])) if len(ups) else 0.0
    nine = int((B.Tp[B.Tp["m"] == CUT]["members"] >= P.UPGRADE_AT).sum())
    return np.full(SPAN, nine * B.upr * per)


def team_new_expect(B):
    """Expected ARR in each forecast month from Team accounts that sign up after the cut, at the sign-up rate and the
    member mix since the minimum, surviving on the base hazard of young accounts."""
    Tp = B.Tp
    first = Tp.groupby("acc").first()
    rec = first[(first["start"] >= P.TEAM_MIN) & (first["start"] <= CUT)]
    lam = len(rec) / float(CUT - P.TEAM_MIN + 1)
    seats = float(np.maximum(rec["members"], P.TEAM_MIN_SEATS).mean())
    price = float((rec["cur"].map(P.TEAM_PRICE) * rec["cur"].map(An.FX)).mean()) * 12
    hist = Tp[(Tp["m"] < P.TEAM_MIN - 1) & (Tp["m"] >= 12)]
    mbmix = np.minimum(rec["members"], 3).value_counts(normalize=True).to_dict()
    base = hist.groupby(["mb", "ab"])["exit"].mean().to_dict()
    path = np.zeros(SPAN)
    for i in range(SPAN):
        for age in range(0, SPAN - i):
            s = 1.0
            for a in range(1, age + 1):
                ab = 0 if a < 3 else (1 if a < 12 else 2)
                h = sum(w * base.get((mb, ab), 0.03) for mb, w in mbmix.items())
                s *= 1 - h
            path[i + age] += lam * s * seats * price
    return path


# ------------------------------------------------------------------------------------------------ routes
def golden(B, reps=400, seed=11, variant=None):
    v = variant or {}
    rng = np.random.default_rng(seed)
    fit = An.fit_business(B.E, use_util=v.get("util", True), use_sib=v.get("sib", True),
                          use_first=v.get("first", True), util_form=v.get("util_form", "hinge"),
                          uplift_form=v.get("uplift_form", "log"))
    if v.get("uplift_flat"):
        fit["uplift_fn"] = lambda s, u=fit["uplift_mean"]: u
    if v.get("uplift_list"):
        fit["uplift_fn"] = lambda s: (P.BUS_LIST_NEW["EUR"] / P.BUS_LIST_OLD["EUR"] - 1)
    if v.get("expansion") == "runrate":
        # the book's trailing true-up rate, carried by the accounts at or near their seats
        L = B.F["lines"]
        tu = L[(L["type"] == "true_up") & (L["m"] > CUT - 12) & (L["m"] <= CUT)]
        a0 = np.array([np.nanmean([B.A.get((i, mm), np.nan) for mm in (CUT - 2, CUT - 1, CUT)]) for i in B.st.index])
        near = a0 / B.st["seats_cut"].values >= 0.9
        base = float(B.st["arr"].values[near].sum())
        mrate = float((tu["seats"] * tu["price"] * 12 * tu["cur"].map(An.FX)).sum()) / 12 / base
        acc_rate = np.where(near, mrate, 0.0)
    elif v.get("expansion") == "ubin":
        acc_rate = None
    elif v.get("expansion") == "acc":
        acc_rate = An.account_trueup_rate(B.F, B.T, B.st)
    else:
        acc_rate = np.zeros(len(B.st))
    exp_rate = An.trueup_model(B.F, B.A, B.T) if acc_rate is None else None
    B.acc_rate = acc_rate
    drift = An.account_drift(B.F, B.A, B.st, B.growth, window=v.get("drift_window", 24)) \
        if v.get("expansion", "drift") == "drift" else None
    bus = An.simulate_business(B.F, fit, B.st, B.A, B.growth, reps, rng, independent=v.get("independent", False),
                               exp_rate=exp_rate, acc_rate=acc_rate, drift=drift)
    tfit = An.fit_team(B.Tp, v.get("team", "golden"))
    team = An.simulate_team(B.Tp, tfit, B.moves, reps, rng, B.upr)
    tpaths = np.array(An.simulate_team.paths)
    open_p, fut_p, up_p = new_business_expect(B, crm=v.get("crm", False), runrate=v.get("runrate", False),
                                              stage_only=v.get("stage_only", False), keys=v.get("pipe_keys"))
    tnew = team_new_expect(B)
    # draws for the band: wins and sign-ups vary around their expectation (counts of whole deals)
    bpaths = np.array([r["path"] for r in bus])
    deal = B.per_seat * float(B.S[B.S["m"] == CUT]["seats"].mean())
    new_cum = np.cumsum(open_p + fut_p + up_p)
    totals = []
    for i in range(reps):
        n = rng.poisson(max(new_cum[-1], 1.0) / deal)
        newv = n * deal * (new_cum / new_cum[-1])
        tn = tnew * rng.normal(1.0, 0.04)
        totals.append(bpaths[i] + tpaths[i] + newv + tn)
    totals = np.array(totals)
    # the expected path is the sum of the flows' expectations, so the bridge adds back to it exactly
    mean_path = bpaths.mean(axis=0) + tpaths.mean(axis=0) + new_cum + tnew
    dec = totals[:, -1]
    f = {
        "open_bus": B.open_bus, "open_team": B.open_team, "open_total": B.open_bus + B.open_team,
        "price": float(np.mean([r["price"] for r in bus])),
        "contraction": float(np.mean([r["contraction"] for r in bus])),
        "churn": float(np.mean([r["churn"] for r in bus])),
        "expansion": float(np.mean([r["expansion"] for r in bus])),
        "book_dec27": float(np.mean([r["dec27"] for r in bus])),
        "team_left": float(np.mean(team)),
        "team_new": float(tnew[-1]),
        "new_open": float(open_p.sum()), "new_future": float(fut_p.sum()), "new_upgrade": float(up_p.sum()),
        "new_bus": float(open_p.sum() + fut_p.sum() + up_p.sum()),
        "dec27": float(mean_path[-1]), "p10": float(np.percentile(dec, 10)), "p90": float(np.percentile(dec, 90)),
        "p20": float(np.percentile(dec, 20)),
        "path": [float(x) for x in mean_path],
        "path_p10": [float(x) for x in np.percentile(totals, 10, axis=0)],
        "path_p90": [float(x) for x in np.percentile(totals, 90, axis=0)],
        "uplift_fit": [float(x) for x in fit["uplift"]], "churn_fit": [float(x) for x in fit["b"]],
        "team_persist": tfit["persist"],
        "draws": [float(x) for x in dec],
    }
    f["bridge_check"] = (f["open_total"] + f["new_bus"] + f["expansion"] + f["price"] - f["contraction"] - f["churn"]
                         + (f["team_left"] - f["open_team"]) + f["team_new"])
    return f


def topdown(B):
    """The quick pass: the book's own growth over the last twelve months carried fourteen more."""
    F = B.F
    tp = B.Tp
    T = B.T
    L = F["lines"]
    tu = L[L["type"] == "true_up"]

    def bus_at(m):
        c = T[(T["m"] <= m) & (T["end"] > m)]
        tot = 0.0
        for r in c.itertuples():
            add = tu[(tu["acc"] == r.acc) & (tu["m"] >= r.m) & (tu["m"] <= m)]["seats"].sum()
            tot += (r.seats0 + add) * r.price * 12 * An.FX[r.cur]
        return tot
    t12 = tp[tp["m"] == CUT - 12]
    team12 = float((t12["seats"] * t12["cur"].map(P.TEAM_PRICE) * 12 * t12["cur"].map(An.FX)).sum())
    a12 = bus_at(CUT - 12) + team12
    now = B.open_bus + B.open_team
    g = now / a12
    return {"dec27": now * g ** (SPAN / 12.0), "growth12": g, "arr_12": a12}
