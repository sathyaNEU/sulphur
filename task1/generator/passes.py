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
        recent = self.W[self.W["m"] >= P.PRICE_RISE]
        self.per_seat_se = float(recent["per_quoted"].std() / np.sqrt(max(len(recent), 1)))
        big = self.Tp[(self.Tp["members"] >= P.UPGRADE_AT) & (self.Tp["m"] >= 11) & (self.Tp["m"] < CUT)]
        self.upr_counts = (int(big["upgrade"].sum()), int(len(big)))
        self.timing, self.creation = {}, {}
        cur = self.Tp[self.Tp["m"] == CUT]
        self.open_team = float((cur["seats"] * cur["cur"].map(P.TEAM_PRICE) * 12 * cur["cur"].map(An.FX)).sum())
        self.open_bus = float(self.st["arr"].sum())


# ------------------------------------------------------------------------------------------------ pipeline timing
def win_timing(B, keys=("stage", "sb"), lookback_from=12):
    """P(won j months after a month-end snapshot), j = 1..SPAN, by stage and staleness, from snapshots with a full
    follow-up window; with each cell's count, for the estimation draws."""
    S = B.S
    hist = S[(S["m"] <= CUT - SPAN) & (S["m"] >= lookback_from)].copy()
    hist["lag"] = hist["won_m"] - hist["m"]
    out = {}
    for k, g in hist.groupby(list(keys)):
        n = len(g)
        out[k] = (np.array([float(((g["lag"] == j)).sum()) / n for j in range(1, SPAN + 1)]), n)
    return out


def creation_timing(B, lookback_from=12, window=12):
    """The monthly creation rate over the trailing window (one full seasonal cycle), the mean quoted seats of those
    deals, and the chance a deal is won j months after creation (j = 0..SPAN) from creations with full follow-up."""
    S, C = B.S, B.F["closed"]
    created = pd.concat([S[["id", "created", "seats"]], C[["id", "created", "seats"]]]).drop_duplicates("id")
    won = C[C["outcome"] == "won"].set_index("id")["m"]
    old = created[(created["created"] >= lookback_from) & (created["created"] <= CUT - SPAN)].copy()
    old["lag"] = old["id"].map(won) - old["created"]
    lagp = np.array([float((old["lag"] == j).mean()) for j in range(0, SPAN + 1)])
    rec = created[(created["created"] > CUT - window) & (created["created"] <= CUT)]
    lam = len(rec) / float(window)
    seats = float(rec["seats"].mean())
    stats = {"n_created": len(rec), "window": window, "seats_sd": float(rec["seats"].std()), "n_old": len(old)}
    return lam, seats, lagp, stats


def new_business_expect(B, crm=False, runrate=False, stage_only=False, keys=None, draw=None, window=12):
    """Expected new Business ARR signed in each forecast month: (open deals, deals not yet created, upgrades). With
    draw (an rng) every estimated rate is redrawn from its sampling error."""
    rng = draw
    per_seat = B.per_seat
    if rng is not None:
        per_seat = float(per_seat + rng.normal(0, B.per_seat_se))
    if runrate:
        L = B.F["lines"]
        nw = L[(L["type"] == "new") & (L["m"] > CUT - 12) & (L["m"] <= CUT)]
        per_m = float((nw["seats"] * nw["price"] * 12 * nw["cur"].map(An.FX)).sum()) / 12.0
        return np.zeros(SPAN), np.full(SPAN, per_m), np.zeros(SPAN)
    op = B.S[B.S["m"] == CUT]
    if crm:
        val = float((op["seats"] * per_seat * np.array(P.CRM_PROB)[op["stage"].values] / 100.0).sum())
        open_path = np.full(SPAN, val / SPAN)
    else:
        keys = keys or (("stage",) if stage_only else ("stage", "sb"))
        tim = B.timing.get(keys)
        if tim is None:
            tim = win_timing(B, keys=keys)
            B.timing[keys] = tim
        open_path = np.zeros(SPAN)
        cell = {}
        for k, (p, n) in tim.items():
            if rng is not None:
                probs = np.append(p, max(1.0 - p.sum(), 0.0))
                cell[k] = rng.multinomial(n, probs / probs.sum())[:SPAN] / float(n)
            else:
                cell[k] = p
        for r in op.itertuples():
            key = tuple(getattr(r, k) for k in keys)
            open_path += cell.get(key, np.zeros(SPAN)) * r.seats * per_seat
    lam, seats, lagp, st = B.creation.get(window) or creation_timing(B, window=window)
    B.creation[window] = (lam, seats, lagp, st)
    if rng is not None:
        lam = float(rng.gamma(st["n_created"] + 0.5, 1.0 / st["window"]))
        seats = float(seats + rng.normal(0, st["seats_sd"] / math.sqrt(max(st["n_created"], 1))))
        probs = np.append(lagp, max(1.0 - lagp.sum(), 0.0))
        lagp = rng.multinomial(st["n_old"], probs / probs.sum())[:SPAN + 1] / float(st["n_old"])
    fut = np.zeros(SPAN)
    for i, c in enumerate(MONTHS):
        for j in range(0, SPAN - i):
            fut[i + j] += lam * lagp[j] * seats * per_seat
    up = upgrades_path(B, rng)
    return open_path, fut, up


def upgrades_path(B, rng=None):
    acc, L = B.F["acc"], B.F["lines"]
    new = L[L["type"] == "new"].set_index("acc")
    ups = acc[(acc["source"] == "upgrade") & (acc["start"] >= P.PRICE_RISE) & (acc["acc"].isin(new.index))]
    vals = [new.loc[a, "seats"] * new.loc[a, "price"] * 12 * An.FX[new.loc[a, "cur"]] for a in ups["acc"]]
    per = float(np.mean(vals)) if len(ups) else 0.0
    nine = int((B.Tp[B.Tp["m"] == CUT]["members"] >= P.UPGRADE_AT).sum())
    upr = B.upr
    if rng is not None and len(vals) > 1:
        per = float(per + rng.normal(0, np.std(vals) / math.sqrt(len(vals))))
        upr = float(rng.beta(B.upr_counts[0] + 0.5, B.upr_counts[1] - B.upr_counts[0] + 0.5))
    return np.full(SPAN, nine * upr * per)


def team_new_expect(B, rng=None):
    """Expected ARR in each forecast month from Team accounts that sign up after the cut, at the sign-up rate and the
    member mix since the minimum, surviving on the base hazard of young accounts."""
    Tp = B.Tp
    first = Tp.groupby("acc").first()
    rec = first[(first["start"] >= P.TEAM_MIN) & (first["start"] <= CUT)]
    months = float(CUT - P.TEAM_MIN + 1)
    lam = len(rec) / months
    if rng is not None:
        lam = float(rng.gamma(len(rec) + 0.5, 1.0 / months))
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
    """The forecast, flow by flow, with its band: every replication redraws each fitted rate from its sampling
    error (the policy's estimation uncertainty) unless the variant switches it off, and nothing is added beyond
    what the records show unless the variant adds the common factor the policy rules out."""
    v = variant or {}
    rng = np.random.default_rng(seed)
    pu = v.get("param_unc", True)
    fit = An.fit_business(B.E, use_util=v.get("util", True), use_sib=v.get("sib", True),
                          use_first=v.get("first", True), util_form=v.get("util_form", "hinge"),
                          uplift_form=v.get("uplift_form", "log"))
    if v.get("uplift_flat"):
        fit["uplift_fn"] = lambda s, u=fit["uplift_mean"]: u
        fit["uplift_override"] = True
    if v.get("uplift_list"):
        fit["uplift_fn"] = lambda s: (P.BUS_LIST_NEW["EUR"] / P.BUS_LIST_OLD["EUR"] - 1)
        fit["uplift_override"] = True
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
                               exp_rate=exp_rate, acc_rate=acc_rate, drift=drift, param_unc=pu,
                               common=v.get("common"))
    tfit = An.fit_team(B.Tp, v.get("team", "golden"), season=v.get("season", "month"))
    team = An.simulate_team(B.Tp, tfit, B.moves, reps, rng, B.upr, param_unc=pu)
    tpaths = np.array(An.simulate_team.paths)
    nb = dict(crm=v.get("crm", False), runrate=v.get("runrate", False), stage_only=v.get("stage_only", False),
              keys=v.get("pipe_keys"), window=v.get("creation_window", 12))
    open_p, fut_p, up_p = new_business_expect(B, **nb)
    tnew = team_new_expect(B)
    # draws for the band: the estimated rates redrawn, then wins and sign-ups as counts of whole deals and teams
    bpaths = np.array([r["path"] for r in bus])
    deal = B.per_seat * float(B.S[B.S["m"] == CUT]["seats"].mean())
    new_cum = np.cumsum(open_p + fut_p + up_p)
    totals = []
    for i in range(reps):
        if pu:
            o_r, f_r, u_r = new_business_expect(B, draw=rng, **nb)
            cum_r = np.cumsum(o_r + f_r + u_r)
            tn_r = team_new_expect(B, rng=rng)
        else:
            cum_r, tn_r = new_cum, tnew
        n = rng.poisson(max(cum_r[-1], 1.0) / deal)
        newv = n * deal * (cum_r / cum_r[-1])
        tn = tn_r * rng.normal(1.0, 0.04)
        totals.append(bpaths[i] + tpaths[i] + newv + tn)
    totals = np.array(totals)
    # the expected path is the sum of the flows' expectations, so the bridge adds back to it exactly
    mean_path = bpaths.mean(axis=0) + tpaths.mean(axis=0) + new_cum + tnew
    dec = totals[:, -1]
    com, met, met_next = An.commitment(dec)
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
        "commitment": com, "commitment_met": met, "commitment_next_met": met_next,
        "path": [float(x) for x in mean_path],
        "path_p10": [float(x) for x in np.percentile(totals, 10, axis=0)],
        "path_p90": [float(x) for x in np.percentile(totals, 90, axis=0)],
        "uplift_fit": [float(x) for x in fit["uplift"]], "churn_fit": [float(x) for x in fit["b"]],
        "team_persist": tfit["persist"], "team_season": tfit["season"],
        "draws": [float(x) for x in dec],
    }
    f["bridge_check"] = (f["open_total"] + f["new_bus"] + f["expansion"] + f["price"] - f["contraction"] - f["churn"]
                         + (f["team_left"] - f["open_team"]) + f["team_new"])
    return f


def naive(B):
    """Every trailing extrapolation a ten-minute pass would take, as point forecasts of December 2027: the trailing
    twelve months' growth compounded forward (the quick pass), the trailing twelve, six and three months' net new
    ARR carried forward in a straight line, the policy's six movement lines at their trailing monthly rates over
    twelve months, six months and the months since the price rise, and new Business at its run-rate since the price
    rise beside the other lines at their trailing twelve-month rates."""
    F, T = B.F, B.T
    arr = {m: sum(An.arr_at(F, m)[:2]) for m in (CUT - 12, CUT - 6, CUT - 3, CUT)}
    now = arr[CUT]
    out = {"trailing twelve months' growth compounded": now * (now / arr[CUT - 12]) ** (SPAN / 12.0),
           "trailing twelve months' net new ARR carried forward": now + (now - arr[CUT - 12]) * SPAN / 12.0,
           "trailing six months' net new ARR carried forward": now + (now - arr[CUT - 6]) * SPAN / 6.0,
           "trailing three months' net new ARR carried forward": now + (now - arr[CUT - 3]) * SPAN / 3.0}
    mv = {}
    for name, (m0, m1) in {"twelve": (CUT - 11, CUT), "six": (CUT - 5, CUT), "recent": (P.PRICE_RISE, CUT)}.items():
        mv[name] = movements(F, T, m0, m1)
        n = m1 - m0 + 1
        d = mv[name]
        net = (d["new"] + d["expansion"] + d["price"] - d["contraction"] - d["lost"] + d["team"]) / n * SPAN
        out["movement lines at their trailing %s" % ("twelve-month rates" if name == "twelve" else
                                                    "six-month rates" if name == "six" else
                                                    "monthly rates since January 2026")] = now + net
    nr = CUT - P.PRICE_RISE + 1
    d12, dr = mv["twelve"], mv["recent"]
    out["new Business at its run-rate since January 2026, other lines at their trailing twelve-month rates"] = now + (
        dr["new"] / nr + (d12["expansion"] + d12["price"] - d12["contraction"] - d12["lost"] + d12["team"]) / 12) * SPAN
    return out


def movements(F, T, m0, m1):
    """The policy's six movement lines summed over months m0 to m1 from the contract lines and Team invoices."""
    L = F["lines"]
    w = lambda d: d[(d["m"] >= m0) & (d["m"] <= m1)]
    new = w(L[L["type"] == "new"])
    tu = w(L[L["type"] == "true_up"])
    T = T.copy()
    T["prev_seats"] = T.groupby("acc")["seats_end"].shift(1)
    T["prev_price"] = T.groupby("acc")["price"].shift(1)
    ren = w(T[(T["type"] == "renewal") & T["prev_seats"].notna()])
    fx = ren["cur"].map(An.FX)
    last = T.sort_values("m").groupby("acc").tail(1)
    lost = last[(last["end"] >= m0) & (last["end"] <= m1) & (last["end"] <= CUT)]
    return {"new": float((new["seats"] * new["price"] * 12 * new["cur"].map(An.FX)).sum()),
            "expansion": float((tu["seats"] * tu["price"] * 12 * tu["cur"].map(An.FX)).sum()) +
            float(((ren["seats0"] - ren["prev_seats"]).clip(lower=0) * ren["price"] * 12 * fx).sum()),
            "price": float((ren["prev_seats"] * (ren["price"] - ren["prev_price"]) * 12 * fx).sum()),
            "contraction": float(((ren["prev_seats"] - ren["seats0"]).clip(lower=0) * ren["price"] * 12 * fx).sum()),
            "lost": float((lost["seats_end"] * lost["price"] * 12 * lost["cur"].map(An.FX)).sum()),
            "team": An.arr_at(F, m1)[1] - An.arr_at(F, m0 - 1)[1]}


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
