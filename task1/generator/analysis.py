"""Every result's golden construction and every rival and hurried route, on the clean tables.

golden.py feeds these functions the frames it rebuilds from the shipped files; the design-stage pricing feeds them the
world's own records. Nothing here reads generator state."""
import math

import numpy as np
import pandas as pd

import params as P

FX = {"EUR": 1.0, "GBP": P.PLAN_RATE_GBP}
CUT, H = P.CUT, P.HORIZON


# ---------------------------------------------------------------------------------------------- helpers
def logit_fit(X, y, iters=50, ridge=1e-6):
    X = np.column_stack([np.ones(len(X)), X])
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-X @ b))
        W = p * (1 - p)
        g = X.T @ (y - p) - ridge * b
        Hm = (X * W[:, None]).T @ X + ridge * np.eye(len(b))
        step = np.linalg.solve(Hm, g)
        b += step
        if np.abs(step).max() < 1e-9:
            break
    p = 1 / (1 + np.exp(-X @ b))
    W = p * (1 - p)
    cov = np.linalg.inv((X * W[:, None]).T @ X + ridge * np.eye(len(b)))
    return b, cov


def logit_p(b, X):
    X = np.column_stack([np.ones(len(X)), X])
    return 1 / (1 + np.exp(-X @ b))


# ---------------------------------------------------------------------------------------------- Business book
def account_actives(F):
    """Active users per account and month: workspace actives through the workspace map valid in that month."""
    ws, wm = F["ws"], F["wmap"].copy()
    wm["to"] = wm["to"].fillna(10 ** 6)
    j = ws.merge(wm, on="ws")
    j = j[(j["m"] >= j["from"]) & (j["m"] <= j["to"])]
    return j.groupby(["owner", "m"])["active"].sum()


def terms(F):
    """One row per contract term (new or renewal line) with the seats it ended on (true-ups added)."""
    L = F["lines"]
    base = L[L["type"].isin(["new", "renewal"])].sort_values(["acc", "m"]).copy()
    tu = L[L["type"] == "true_up"]
    base["end"] = base["m"] + 12
    rows = []
    tu_by = {k: g for k, g in tu.groupby("acc")}
    for r in base.itertuples():
        g = tu_by.get(r.acc)
        add_cut = 0
        add_all = 0
        if g is not None:
            inn = g[(g["m"] >= r.m) & (g["m"] < r.end)]
            add_all = int(inn["seats"].sum())
            add_cut = int(inn[inn["m"] <= CUT]["seats"].sum())
        rows.append({"acc": r.acc, "m": r.m, "end": r.end, "type": r.type, "opening": r.opening, "seats0": r.seats,
                     "price": r.price, "cur": r.cur, "seats_end": r.seats + add_all, "seats_cut": r.seats + add_cut})
    T = pd.DataFrame(rows)
    T["n"] = T.groupby("acc").cumcount()
    T["next_m"] = T.groupby("acc")["m"].shift(-1)
    return T


def business_state(F, T=None):
    T = terms(F) if T is None else T
    cur = T[(T["m"] <= CUT) & (T["end"] > CUT)].copy()
    cur["arr"] = cur["seats_cut"] * cur["price"] * 12 * cur["cur"].map(FX)
    # renewal number of the coming anniversary: lines on file before it; an opening renewal line counts as later
    first_open = T.groupby("acc")["opening"].first()
    first_type = T.groupby("acc")["type"].first()
    cur["rc_next"] = cur["n"] + 1 + np.where(cur["acc"].map(first_open) & (cur["acc"].map(first_type) == "renewal"),
                                             2, 0)
    cur["repriced"] = cur["m"] >= P.PRICE_RISE
    return cur.set_index("acc")


def arr_at(F, m):
    """ARR at the end of month m on the policy's definition: Business contracts in force (seats with the true-ups
    to date, at the contracted price) and Team subscriptions invoiced for the month; with the accounts counted."""
    L = F["lines"]
    base = L[L["type"].isin(["new", "renewal"]) & (L["m"] <= m) & (L["m"] + 12 > m)]
    tu = L[(L["type"] == "true_up") & (L["m"] <= m)]
    add = {}
    for r in tu.itertuples():
        add.setdefault(r.acc, []).append((r.m, r.seats))
    b = 0.0
    for r in base.itertuples():
        s = r.seats + sum(k for (mm, k) in add.get(r.acc, []) if r.m <= mm <= m)
        b += s * r.price * 12 * FX[r.cur]
    T = F["team"]
    t = T[T["m"] == m]
    tv = float((t["seats"] * t["cur"].map(P.TEAM_PRICE) * 12 * t["cur"].map(FX)).sum())
    return b, tv, int(base["acc"].nunique()), int(t["acc"].nunique())


def churned_months(T):
    """Month each account left: the end of a term with no line after it, at or before the cut."""
    last = T.sort_values("m").groupby("acc").tail(1)
    ch = last[last["end"] <= CUT]
    return dict(zip(ch["acc"], ch["end"]))


def renewal_events(F, T=None, A=None):
    T = terms(F) if T is None else T
    A = account_actives(F) if A is None else A
    acc = F["acc"].set_index("acc")
    ch = churned_months(T)
    par_of = acc["parent"].to_dict()
    by_parent = {}
    for a, mm in ch.items():
        by_parent.setdefault(par_of[a], []).append((mm, a))
    first_open = T.groupby("acc")["opening"].first()
    first_type = T.groupby("acc")["type"].first()
    ev = T[(T["end"] <= CUT) & (T["end"] >= 1)].copy()
    out = []
    for r in ev.itertuples():
        k = r.end
        acts = [A.get((r.acc, mm), np.nan) for mm in (k - 3, k - 2, k - 1)]
        acts = [x for x in acts if not (isinstance(x, float) and math.isnan(x))]
        if not acts:
            continue
        U = float(np.mean(acts)) / r.seats_end
        renewed = not (isinstance(r.next_m, float) and math.isnan(r.next_m))
        nxt = T[(T["acc"] == r.acc) & (T["m"] == k)] if renewed else None
        rc = r.n + 1 + (2 if (first_open[r.acc] and first_type[r.acc] == "renewal") else 0)
        sib = any((a != r.acc) and (k - 12 <= mm < k) for (mm, a) in by_parent.get(par_of[r.acc], []))
        row = {"acc": r.acc, "k": k, "U": U, "rc": rc, "first": int(rc == 1), "sib": int(sib),
               "seats": r.seats_end, "price": r.price, "cur": r.cur, "renewed": int(renewed),
               "arr": r.seats_end * r.price * 12 * FX[r.cur]}
        if renewed:
            n0 = nxt.iloc[0]
            row["new_seats"] = int(n0["seats0"])
            row["new_price"] = float(n0["price"])
        out.append(row)
    return pd.DataFrame(out)


U_BINS = [0, 0.6, 0.7, 0.8, 0.88, 10]


UP_BANDS = [0, 15, 30, 60, 120, 10 ** 6]


def util_feats(U, form):
    if form == "bins":
        return [1.0 if U < 0.6 else 0.0, 1.0 if 0.6 <= U < 0.7 else 0.0, 1.0 if 0.7 <= U < 0.8 else 0.0]
    return [max(0.0, 0.70 - U)]


def fit_business(E, use_util=True, use_sib=True, use_first=True, since=1, util_form="hinge", uplift_form="log"):
    E = E[E["k"] >= since]
    cols = []
    if use_first:
        cols.append(E["first"].values)
    if use_util and util_form != "none":
        cols.append(np.array([util_feats(u, util_form) for u in E["U"].values]))
    if use_sib:
        cols.append(E["sib"].values)
    X = np.column_stack(cols) if cols else np.zeros((len(E), 0))
    b, cov = logit_fit(X, 1 - E["renewed"].values)
    R = E[E["renewed"] == 1].copy()
    R["ratio"] = R["new_seats"] / R["seats"]
    R["ub"] = pd.cut(R["U"], U_BINS, labels=False) if use_util else 0
    R["f"] = R["first"] if use_first else 0
    rg = R.groupby(["ub", "f"])["ratio"]
    ratio = rg.mean().to_dict()
    ratio_se = (rg.std().fillna(0.0) / np.sqrt(rg.size().clip(lower=1))).to_dict()
    up = E[(E["k"] >= P.PRICE_RISE) & (E["renewed"] == 1)].copy()
    up = up[up["price"] < (up["new_price"] - 0.005)]
    up["r"] = up["new_price"] / up["price"] - 1
    xs = np.log(np.maximum(up["seats"].values, 5) / 20.0)
    ub, ucov = np.polyfit(xs, up["r"].values, 1, cov=True)
    bands = up.groupby(pd.cut(up["seats"], UP_BANDS, labels=False))["r"].mean().to_dict()
    bands_se = (up.groupby(pd.cut(up["seats"], UP_BANDS, labels=False))["r"].std().fillna(0.0) /
                np.sqrt(up.groupby(pd.cut(up["seats"], UP_BANDS, labels=False))["r"].size().clip(lower=1))).to_dict()
    return {"b": b, "cov": cov, "ratio": ratio, "ratio_se": ratio_se, "util": use_util, "sib": use_sib,
            "first": use_first, "uplift": ub, "uplift_cov": ucov, "uplift_fn": uplift_function(uplift_form, ub, bands,
                                                                                                float(up["r"].mean())),
            "uplift_form": uplift_form, "util_form": util_form, "uplift_bands": bands, "uplift_bands_se": bands_se,
            "uplift_mean": float(up["r"].mean()), "uplift_n": len(up)}


def uplift_function(form, ub, bands, mean):
    if form == "bands":
        def ufn(seats):
            k = int(np.digitize([seats], UP_BANDS[1:-1])[0])
            return bands.get(k, mean)
    else:
        def ufn(seats):
            return float(np.polyval(ub, math.log(max(seats, 5) / 20.0)))
    return ufn


def perturb_business(fit, rng):
    """The fitted renewal model redrawn from its own sampling error (the policy's estimation uncertainty): the exit
    model's coefficients from their covariance, the uplift fit from its covariance, each seat-ratio cell from its
    standard error. Routes that override the uplift (flat or list) keep their override."""
    f = dict(fit)
    f["b"] = rng.multivariate_normal(fit["b"], fit["cov"])
    f["ratio"] = {k: float(np.clip(v + rng.normal(0, fit["ratio_se"].get(k, 0.0)), 0.3, 1.0))
                  for k, v in fit["ratio"].items()}
    if not fit.get("uplift_override"):
        if fit["uplift_form"] == "bands":
            bands = {k: v + rng.normal(0, fit["uplift_bands_se"].get(k, 0.0)) for k, v in fit["uplift_bands"].items()}
            f["uplift_fn"] = uplift_function("bands", fit["uplift"], bands, fit["uplift_mean"])
        else:
            ub = rng.multivariate_normal(fit["uplift"], fit["uplift_cov"])
            f["uplift_fn"] = uplift_function("log", ub, fit["uplift_bands"], fit["uplift_mean"])
    return f


def normal_cdf(x):
    return 0.5 * (1.0 + np.vectorize(math.erf)(x / math.sqrt(2.0)))


def commitment(draws, step=1e5, chance=0.80):
    """The largest multiple of the step that is met or beaten in at least the stated share of the outcomes, with the
    share met at that step and the one above it."""
    d = np.asarray(draws, float)
    x = math.floor(np.percentile(d, 100 * (1 - chance)) / step) * step
    while np.mean(d >= x) < chance:
        x -= step
    while np.mean(d >= x + step) >= chance:
        x += step
    return float(x), float(np.mean(d >= x)), float(np.mean(d >= x + step))


def growth_model(F, A, T):
    """Monthly growth of active users by months since the account started, from accounts' own histories."""
    acc = F["acc"].set_index("acc")
    df = A.reset_index()
    df.columns = ["acc", "m", "a"]
    df = df[df["acc"].isin(acc.index)]
    df["start"] = df["acc"].map(acc["start"])
    df = df.sort_values(["acc", "m"])
    df["prev"] = df.groupby("acc")["a"].shift(1)
    df = df[(df["prev"] > 0) & (df["a"] > 0)]
    df["age"] = df["m"] - df["start"]
    df["lg"] = np.log(df["a"] / df["prev"])
    g = df.groupby(np.minimum(df["age"], 13))["lg"].mean()
    return g.to_dict()


def trueup_model(F, A, T, since=CUT - 11):
    """Seats added at true-ups in a month per seat in force, by the account's utilisation the month before, over the
    trailing twelve months."""
    L = F["lines"]
    tu = L[(L["type"] == "true_up") & (L["m"] >= since) & (L["m"] <= CUT)].groupby(["acc", "m"])["seats"].sum()
    rows = []
    for r in T[(T["end"] > since) & (T["m"] <= CUT)].itertuples():
        seats = r.seats0
        for m in range(max(r.m + 1, since), min(r.end, CUT + 1)):
            prev = A.get((r.acc, m - 1), np.nan)
            add = int(tu.get((r.acc, m), 0))
            if not (isinstance(prev, float) and math.isnan(prev)):
                rows.append((prev / seats, seats, add))
            seats += add
    D = pd.DataFrame(rows, columns=["U", "seats", "add"])
    D["ub"] = pd.cut(D["U"], [0, 0.85, 0.95, 10], labels=False)
    g = D.groupby("ub")[["seats", "add"]].sum()
    return (g["add"] / g["seats"]).to_dict()


def account_trueup_rate(F, T, state, window=12, young=None):
    """Each account's own monthly true-up growth over its trailing months (seats added at true-ups over the seats it
    carried, a month); accounts younger than the window take the pooled rate of accounts at their age."""
    L = F["lines"]
    tu = L[(L["type"] == "true_up") & (L["m"] > CUT - window) & (L["m"] <= CUT)].groupby("acc")["seats"].sum()
    rates = []
    for acc, r in state.iterrows():
        add = float(tu.get(acc, 0.0))
        base = max(r["seats_cut"] - add, 1.0)
        rates.append(add / base / window)
    return np.array(rates)


def account_drift(F, A, state, growth, window=18, min_age=4, min_months=6):
    """Each account's own monthly drift in active users: the slope of log actives over its last months (past its
    first months), shrunk toward the book's mature drift by the spread the slopes show beyond their noise."""
    acc = F["acc"].set_index("acc")
    mu = float(growth.get(13, 0.0))
    est = []
    for i in state.index:
        st0 = acc.loc[i, "start"]
        ms = [m for m in range(max(CUT - window + 1, st0 + min_age), CUT + 1)]
        ys = [A.get((i, m), np.nan) for m in ms]
        pts = [(m, math.log(y)) for m, y in zip(ms, ys) if not (isinstance(y, float) and math.isnan(y)) and y > 0]
        if len(pts) < min_months:
            est.append((np.nan, np.nan))
            continue
        x = np.array([p[0] for p in pts], float)
        y = np.array([p[1] for p in pts])
        xc = x - x.mean()
        sxx = float((xc ** 2).sum())
        b = float((xc * (y - y.mean())).sum() / sxx)
        res = y - y.mean() - b * xc
        s2 = float((res ** 2).sum() / max(len(pts) - 2, 1))
        est.append((b, s2 / sxx))
    est = np.array(est)
    ok = ~np.isnan(est[:, 0])
    tau2 = max(float(np.var(est[ok, 0]) - np.mean(est[ok, 1])), 1e-8)
    w = np.where(ok, tau2 / (tau2 + np.nan_to_num(est[:, 1], nan=1.0)), 0.0)
    return mu + w * (np.nan_to_num(est[:, 0], nan=mu) - mu), mu


def simulate_business(F, fit, state, A, growth, reps, rng, per_account=False, independent=False, consolidating=None,
                      exp_rate=None, acc_rate=None, drift=None, param_unc=True, common=None):
    """Monte Carlo of the fitted renewal model over the book in force at the cut; returns per-rep flows and the
    December 2027 ARR. Siblings' churn feeds each account's next renewal through the sibling term unless
    independent is set. With param_unc each replication redraws the fitted model from its sampling error; common
    adds a Gaussian common factor (its correlation) to every exit draw, the allowance the policy rules out."""
    acc = F["acc"].set_index("acc")
    st = state[state.index.isin(acc.index)]
    ids = st.index.values
    par = acc.loc[ids, "parent"].values
    seats0 = st["seats_cut"].values.astype(float)
    price0 = st["price"].values
    fx = st["cur"].map(FX).values
    anniv0 = st["end"].values
    rc0 = st["rc_next"].values
    rep0 = st["repriced"].values
    a0 = np.array([np.nanmean([A.get((i, mm), np.nan) for mm in (CUT - 2, CUT - 1, CUT)]) for i in ids])
    age0 = CUT - acc.loc[ids, "start"].values
    # recent sibling churn already on file
    T = terms(F)
    ch = churned_months(T)
    par_all = acc["parent"].to_dict()
    lastch = {}
    for a, mm in ch.items():
        p = par_all[a]
        lastch[p] = max(lastch.get(p, -99), mm)
    out = []
    for _ in range(reps):
        fr = perturb_business(fit, rng) if param_unc else fit
        b = fr["b"]
        seats = seats0.copy()
        price = price0.copy()
        alive = np.ones(len(ids), bool)
        anniv = anniv0.copy()
        rc = rc0.copy()
        rep = rep0.copy()
        a = a0.copy()
        lc = dict(lastch)
        fl = {"price": 0.0, "contraction": 0.0, "churn": 0.0, "expansion": 0.0, "path": []}
        price_window = 0.0
        for m in range(CUT + 1, H + 1):
            age = age0 + (m - CUT)
            gr = np.array([growth.get(min(x, 13), 0.0) for x in age])
            if drift is not None:
                a = a * np.exp(gr - drift[1] + drift[0])
            else:
                a = a * np.exp(gr)
            due = alive & (anniv == m)
            idx = np.where(due)[0]
            z = rng.normal() if common else 0.0
            for i in idx:
                U = a[i] / seats[i]
                feats = []
                if fit["first"]:
                    feats.append(1.0 if rc[i] == 1 else 0.0)
                if fit["util"] and fit["util_form"] != "none":
                    feats.extend(util_feats(U, fit["util_form"]))
                if fit["sib"]:
                    feats.append(1.0 if (not independent and lc.get(par[i], -99) >= m - 12) else 0.0)
                pch = float(logit_p(b, np.array([feats]))[0]) if feats else float(1 / (1 + math.exp(-b[0])))
                arr_i = seats[i] * price[i] * 12 * fx[i]
                if common:
                    u = 0.5 * (1.0 + math.erf((math.sqrt(common) * z + math.sqrt(1 - common) * rng.normal()) / math.sqrt(2)))
                else:
                    u = rng.random()
                if u < pch:
                    alive[i] = False
                    fl["churn"] += arr_i
                    lc[par[i]] = m
                    continue
                ub = int(np.digitize([U], U_BINS[1:-1])[0]) if fit["util"] else 0
                f = (1 if rc[i] == 1 else 0) if fit["first"] else 0
                ratio = fr["ratio"].get((ub, f), 1.0)
                ns = max(5.0, min(seats[i], seats[i] * ratio))
                np_ = price[i]
                if not rep[i]:
                    upl = fr["uplift_fn"](seats[i])
                    upl = min(max(upl, 0.0), P.UPLIFT_FULL)
                    np_ = price[i] * (1 + upl)
                    rep[i] = True
                    fl["price"] += seats[i] * (np_ - price[i]) * 12 * fx[i]
                fl["contraction"] += (seats[i] - ns) * np_ * 12 * fx[i]
                seats[i], price[i] = ns, np_
                anniv[i] = m + 12
                rc[i] += 1
            if acc_rate is not None:
                grow = alive & (acc_rate > 0)
                add = np.where(grow, seats * acc_rate, 0.0)
                a = np.where(grow, a * (1 + acc_rate) / np.exp(gr), a)
                add = np.where(alive, np.maximum(add, a * 1.04 - seats), 0.0)
            else:
                Um = a / seats
                ubm = np.digitize(Um, [0.85, 0.95])
                add = seats * np.array([exp_rate.get(int(x), 0.0) for x in ubm]) if exp_rate else np.zeros(len(seats))
                add = np.where(alive, np.maximum(add, a * 1.04 - seats), 0.0)
            add = np.maximum(add, 0.0)
            fl["expansion"] += float((add * price * 12 * fx).sum())
            seats = seats + add
            fl["path"].append(float((seats * price * 12 * fx)[alive].sum()))
        fl["dec27"] = float((seats * price * 12 * fx)[alive].sum())
        out.append(fl)
    return out


# ---------------------------------------------------------------------------------------------- Team book
def team_panel(F):
    T = F["team"][["acc", "m", "members", "seats", "cur"]].sort_values(["acc", "m"])
    T["next"] = T.groupby("acc")["m"].shift(-1)
    T["exit"] = ((T["next"] != T["m"] + 1) & (T["m"] < CUT)).astype(int)
    # an exit whose workspace moves to a Business account the next month is an upgrade, not a cancellation
    wm = F["wmap"]
    tws = F["tacc"].set_index("acc")["ws"]
    bus_ids = set(F["acc"]["acc"])
    moved = wm[wm["owner"].isin(bus_ids)].groupby("ws")["from"].min()
    up_m = {a: moved[w] for a, w in tws.items() if w in moved.index}
    T["upgrade"] = [int(e == 1 and up_m.get(a, -99) == m + 1) for a, m, e in zip(T["acc"], T["m"], T["exit"])]
    T["cancel"] = T["exit"] - T["upgrade"]
    T["start"] = T.groupby("acc")["m"].transform("min")
    T["age"] = T["m"] - T["start"]
    mar = T[T["m"] == P.TEAM_MIN - 1].set_index("acc")["members"]
    pad = set(mar[mar < P.TEAM_MIN_SEATS].index)
    T["padded"] = T["acc"].isin(pad) & (T["m"] >= P.TEAM_MIN - 1)
    T["k"] = T["m"] + 1 - P.TEAM_MIN
    T["cal"] = (P.M0_MONTH - 1 + T["m"] + 1) % 12 + 1   # calendar month of the transition month (m + 1)
    T["mb"] = np.minimum(T["members"], 3)
    T["ab"] = np.select([T["age"] < 3, T["age"] < 12], [0, 1], 2)
    return T


def season_index(rows, base, form):
    """Multiplicative calendar index of the cancel hazard, read against the base cells: observed cancels over the
    cancels the base cells expect, by calendar month (form month), by quarter, or the monthly index smoothed over
    three months (circular); none gives a flat index. Normalised to an exposure-weighted mean of one."""
    cal = rows["cal"].values
    exp = np.array([base.get((a, b), np.nan) for a, b in zip(rows["mb"], rows["ab"])])
    obs = rows["cancel"].values.astype(float)
    keep = ~np.isnan(exp)
    cal, exp, obs = cal[keep], exp[keep], obs[keep]
    if form == "none":
        return {c: 1.0 for c in range(1, 13)}, {c: (0.0, 0.0) for c in range(1, 13)}
    if form == "quarter":
        grp = (cal - 1) // 3
    else:
        grp = cal - 1
    o = np.bincount(grp, weights=obs, minlength=12 if form != "quarter" else 4)
    e = np.bincount(grp, weights=exp, minlength=12 if form != "quarter" else 4)
    idx = o / np.maximum(e, 1e-9)
    if form == "quarter":
        idx = np.repeat(idx, 3)
        o, e = np.repeat(o, 3), np.repeat(e, 3)
    if form == "smooth":
        idx = np.array([(idx[(i - 1) % 12] + idx[i] + idx[(i + 1) % 12]) / 3.0 for i in range(12)])
    w = np.bincount(cal - 1, weights=exp, minlength=12)
    idx = idx / float((idx * w).sum() / w.sum())
    return {c + 1: float(idx[c]) for c in range(12)}, {c + 1: (float(o[c]), float(e[c])) for c in range(12)}


def fit_team(Tp, mode="golden", season="month"):
    """Hazard of leaving the Team plan next month. The base hazard by members and age is read on months before the
    minimum, with the calendar index of the cancel rate fitted alongside it (the golden forms); padded accounts carry
    an excess by months since padding over that base. The pooled rivals read one window flat, with no index."""
    hist = Tp[(Tp["m"] < CUT)]
    flat = {c: 1.0 for c in range(1, 13)}
    if mode == "recent_pooled":
        rec = hist[hist["m"] >= P.TEAM_MIN - 1]
        return {"base": rec.groupby(["mb", "ab"])["cancel"].mean().to_dict(), "excess": {}, "persist": 0.0,
                "season": flat, "stats": None}
    if mode == "long_pooled":
        pre = hist[hist["m"] < P.TEAM_MIN - 1]
        return {"base": pre.groupby(["mb", "ab"])["cancel"].mean().to_dict(), "excess": {}, "persist": 0.0,
                "season": flat, "stats": None}
    if mode == "last3_pooled":
        rec = hist[hist["m"] >= CUT - 3]
        return {"base": rec.groupby(["mb", "ab"])["cancel"].mean().to_dict(), "excess": {}, "persist": 0.0,
                "season": flat, "stats": None}
    if mode == "trailing12":
        rec = hist[hist["m"] >= CUT - 12]
        return {"base": rec.groupby(["mb", "ab"])["cancel"].mean().to_dict(), "excess": {}, "persist": 0.0,
                "season": flat, "stats": None}
    pre = hist[(hist["m"] < P.TEAM_MIN - 1) & (hist["m"] >= 12)].copy()
    base = pre.groupby(["mb", "ab"])["cancel"].mean().to_dict()
    sidx = flat
    for _ in range(4):
        sidx, counts = season_index(pre, base, season)
        sv = pre["cal"].map(sidx).values
        g = pre.assign(sv=sv).groupby(["mb", "ab"])
        base = (g["cancel"].sum() / g["sv"].sum()).to_dict()
    cell = pre.assign(sv=pre["cal"].map(sidx).values).groupby(["mb", "ab"]).agg(k=("cancel", "sum"), n=("sv", "sum"))
    pd_ = hist[hist["padded"] & (hist["k"] >= 0)].copy()
    pd_["pred"] = [base.get((a, b), np.nan) * sidx[c] for a, b, c in zip(pd_["mb"], pd_["ab"], pd_["cal"])]
    byk = pd_.groupby("k")
    ex = (byk["cancel"].mean() - byk["pred"].mean()).to_dict()
    exn = byk.size().to_dict()
    ks = sorted(ex)
    if mode == "golden":
        last = ks[-3:]
    elif mode == "golden_last2":
        last = ks[-2:]
    else:
        last = ks[-3:]
    persist = float(np.mean([ex[k] for k in last]))
    if mode == "golden_expfit":
        best = None
        for tau in np.arange(1.0, 6.01, 0.1):
            xs = np.array([math.exp(-k / tau) for k in ks])
            Xm = np.column_stack([np.ones(len(ks)), xs])
            coef, *_ = np.linalg.lstsq(Xm, np.array([ex[k] for k in ks]), rcond=None)
            sse = float(((Xm @ coef - np.array([ex[k] for k in ks])) ** 2).sum())
            if best is None or sse < best[0]:
                best = (sse, coef, tau)
        persist = float(best[1][0])
    pk = {k: float(byk["cancel"].mean()[k]) for k in last}
    persist_se = float(math.sqrt(sum(pk[k] * (1 - pk[k]) / exn[k] for k in last)) / len(last))
    return {"base": base, "excess": ex, "persist": persist, "season": sidx,
            "stats": {"cell": {k: (float(r.k), float(r.n)) for k, r in cell.iterrows()}, "season_counts": counts,
                      "season_form": season, "persist_se": persist_se}}


def perturb_team(fit, rng):
    """The Team hazard model redrawn from its sampling error: each base cell from its cancels and exposure, the
    calendar index from its observed and expected cancels, the lasting excess from its standard error."""
    st = fit.get("stats")
    if not st:
        return fit
    f = dict(fit)
    f["base"] = {k: float(rng.gamma(kk + 0.5, 1.0 / max(n, 1e-9))) for k, (kk, n) in st["cell"].items()}
    if st["season_form"] != "none":
        raw = {c: rng.gamma(o + 0.5, 1.0 / max(e, 1e-9)) for c, (o, e) in st["season_counts"].items()}
        if st["season_form"] == "quarter":
            raw = {c: float(np.mean([raw[q] for q in range(((c - 1) // 3) * 3 + 1, ((c - 1) // 3) * 3 + 4)]))
                   for c in range(1, 13)}
        elif st["season_form"] == "smooth":
            raw = {c: (raw[(c - 2) % 12 + 1] + raw[c] + raw[c % 12 + 1]) / 3.0 for c in range(1, 13)}
        w = {c: st["season_counts"][c][1] for c in range(1, 13)}
        norm = sum(raw[c] * w[c] for c in w) / max(sum(w.values()), 1e-9)
        f["season"] = {c: float(raw[c] / norm) for c in range(1, 13)}
    f["persist"] = float(fit["persist"] + rng.normal(0, st["persist_se"]))
    return f


def team_moves(Tp):
    """Monthly chances that a staying Team account gains or loses members, and that a nine-plus team upgrades."""
    s = Tp[(Tp["exit"] == 0) & (Tp["m"] < CUT)].copy()
    nx = Tp.set_index(["acc", "m"])["members"]
    s["nm"] = [nx.get((a, m + 1), np.nan) for a, m in zip(s["acc"], s["m"])]
    s = s.dropna(subset=["nm"])
    d = s["nm"] - s["members"]
    up = float((d > 0).mean())
    upsize = float(d[d > 0].mean())
    two = float((d[d > 0] >= 2).mean())
    dn = float(((d < 0) & (s["members"] > 1)).mean())
    return {"up": up, "upsize": upsize, "two": two, "down": dn}


def simulate_team(Tp, fit, moves, reps, rng, upgrade_rate, param_unc=True):
    cur = Tp[Tp["m"] == CUT]
    mem0 = cur["members"].values
    age0 = cur["age"].values
    pad = cur["padded"].values
    fx = cur["cur"].map(FX).values
    price = cur["cur"].map(P.TEAM_PRICE).values
    res = []
    paths = []
    for _ in range(reps):
        fr = perturb_team(fit, rng) if param_unc else fit
        mem = mem0.copy()
        alive = np.ones(len(mem), bool)
        path = []
        for m in range(CUT + 1, H + 1):
            age = age0 + (m - CUT)
            mb = np.minimum(mem, 3)
            ab = np.select([age < 3, age < 12], [0, 1], 2)
            cal = (P.M0_MONTH - 1 + m) % 12 + 1
            h = np.array([fr["base"].get((x, y), 0.03) for x, y in zip(mb, ab)]) * fr["season"][cal]
            k = m - P.TEAM_MIN
            h = h + np.where(pad, fr["excess"].get(k, fr["persist"]) if k in fr["excess"] else fr["persist"], 0.0)
            h = h + np.where(mem >= P.UPGRADE_AT, upgrade_rate, 0.0)
            leave = rng.random(len(mem)) < np.clip(h, 0, 1)
            alive &= ~leave
            u = rng.random(len(mem))
            size = np.where(rng.random(len(mem)) < moves["two"], 2, 1)
            mem = mem + np.where(u < moves["up"], size, 0) - \
                np.where((u >= moves["up"]) & (u < moves["up"] + moves["down"]) & (mem > 1), 1, 0)
            path.append(float((np.maximum(mem, P.TEAM_MIN_SEATS) * price * 12 * fx)[alive].sum()))
        seats = np.maximum(mem, P.TEAM_MIN_SEATS)
        res.append(float((seats * price * 12 * fx)[alive].sum()))
        paths.append(path)
    simulate_team.paths = paths
    return res


def upgrade_rate(Tp, F):
    """Monthly chance that a Team account with nine or more members moves to Business: the CRM's upgrade-sourced
    accounts against the nine-plus account-months."""
    acc = F["acc"]
    ups = acc[acc["source"] == "upgrade"]
    ups = ups[(ups["start"] >= 12) & (ups["start"] <= CUT)]
    big = Tp[(Tp["members"] >= P.UPGRADE_AT) & (Tp["m"] >= 11) & (Tp["m"] < CUT)]
    return float(big["upgrade"].sum()) / max(len(big), 1)


# ---------------------------------------------------------------------------------------------- pipeline
def pipeline_tables(F):
    S = F["snap"].copy()
    C = F["closed"].copy()
    won = C[C["outcome"] == "won"].set_index("id")["m"].to_dict()
    S["won_m"] = S["id"].map(won)
    S["stale"] = np.minimum(np.maximum(S["mis"] - np.array(P.TYPICAL)[S["stage"]], 0), 4)
    S["sb"] = np.select([S["stale"] == 0, S["stale"] <= 2], [0, 1], 2)
    S["agb"] = np.minimum((S["m"] - S["created"]) // 3, 4)
    return S


def deal_value(F, A=None):
    """First-contract ARR of won deals against their quoted seats, and the price per quoted seat now charged."""
    C = F["closed"]
    W = C[C["outcome"] == "won"]
    L = F["lines"]
    new = L[L["type"] == "new"].set_index("acc")
    W = W[W["acc"].isin(new.index)].copy()
    W["arr"] = [new.loc[a, "seats"] * new.loc[a, "price"] * 12 * FX[new.loc[a, "cur"]] for a in W["acc"]]
    W["per_quoted"] = W["arr"] / W["seats"]
    recent = W[W["m"] >= P.PRICE_RISE]
    return W, float(recent["arr"].sum() / recent["seats"].sum())


def pipeline_golden(F, S, horizon=H, by="stage_stale", lookback_from=12):
    """Expected ARR signed by the horizon from deals open at the cut: win chance within the remaining months by
    stage and staleness, read from every past month-end snapshot whose follow-up window is complete."""
    span = horizon - CUT
    W, per_seat = deal_value(F)
    hist = S[(S["m"] <= CUT - span) & (S["m"] >= lookback_from)].copy()
    hist["win"] = ((hist["won_m"] > hist["m"]) & (hist["won_m"] <= hist["m"] + span)).astype(int)
    keys = {"stage_stale": ["stage", "sb"], "stage": ["stage"], "stage_age": ["stage", "ab"]}[by]
    if by == "stage_age":
        hist["ab"] = np.minimum((hist["m"] - hist["created"]) // 3, 4)
    rate = hist.groupby(keys)["win"].mean()
    open_ = S[S["m"] == CUT].copy()
    if by == "stage_age":
        open_["ab"] = np.minimum((open_["m"] - open_["created"]) // 3, 4)
    p = [rate.get(tuple(r) if len(keys) > 1 else r[0], 0.0) for r in open_[keys].values]
    open_["p"] = p
    return float((open_["p"] * open_["seats"] * per_seat).sum()), open_, rate


def future_deals(F, S, horizon=H, recent_from=P.PRICE_RISE):
    """Deals not yet created: the monthly creation rate since the price rise times the chance a deal created in each
    month is won by the horizon (read from past creations), times the value of a won deal."""
    C = F["closed"]
    W, per_seat = deal_value(F)
    created = pd.concat([S[["id", "created", "seats"]], C[["id", "created", "seats"]]]).drop_duplicates("id")
    rate = created[(created["created"] >= recent_from) & (created["created"] <= CUT)].groupby("created").size()
    lam = float(rate.mean())
    seats_mean = float(created[created["created"] >= recent_from]["seats"].mean())
    won = C[C["outcome"] == "won"].set_index("id")["m"]
    old = created[(created["created"] >= 12) & (created["created"] <= CUT - (horizon - CUT))].copy()
    old["lag"] = old["id"].map(won) - old["created"]
    tot = 0.0
    for c in range(CUT + 1, horizon + 1):
        pw = float(((old["lag"] >= 0) & (old["lag"] <= horizon - c)).mean())
        tot += lam * pw * seats_mean * per_seat
    return tot


def upgrades_golden(Tp, F, rate):
    """Business ARR from Team accounts upgrading by the horizon: nine-plus teams at the cut and those that grow into
    it, at the first-contract ARR per member the past upgrades carried."""
    acc = F["acc"]
    L = F["lines"]
    new = L[L["type"] == "new"].set_index("acc")
    ups = acc[(acc["source"] == "upgrade") & (acc["start"] >= P.PRICE_RISE)]
    ups = ups[ups["acc"].isin(new.index)]
    arr_up = [new.loc[a, "seats"] * new.loc[a, "price"] * 12 * FX[new.loc[a, "cur"]] for a in ups["acc"]]
    per = float(np.mean(arr_up)) if arr_up else 0.0
    n_month = len(ups) / max(CUT - P.PRICE_RISE + 1, 1)
    return n_month * (H - CUT) * per
