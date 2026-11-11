"""Medienhaus Brückenhafen's record, January 2023 to October 2026, and the clean truths beyond it.

history() draws the subscriptions running in January 2023, every start on the eighteen paid lines and the paywall,
the households' returns, their customer accounts, payment methods and addresses, and the monthly reading of every
login; the pack is cut from it. The truths (the 2027 lines' value, the base's December 2027) are the same process run
forward with the true parameters, used only to check the golden and to set nothing else."""
import numpy as np

import params as P
import sim


def line_level(c, t, m):
    """Expected new starts in month m on a line (or the paywall), before the month's draw."""
    base = P.LINES[(c, t)][2] if c != "DIR" else P.DIR_STARTS[t]
    trend = (1 - P.LINE_GROWTH) + P.LINE_GROWTH * m / P.CUT
    season = P.START_SEASON[sim.cal_month(m)]
    news = 1 + (P.NEWS.get(m, 0.0) if c == "DIR" else 0.3 * P.NEWS.get(m, 0.0))
    return base * trend * season * news


def base_book(rng):
    rows = []
    for t, n in P.BASE.items():
        ten = np.minimum(1 + rng.geometric(1 / 34.0, size=n), 140)
        h, p = sim.draw_hp(n, P.BASE_H + P.TITLE_H[t], P.BASE_P, rng)
        app = rng.random(n) < 0.08
        web = rng.choice([sim.R_IDX[r] for r in ["SEPA", "PAYPAL", "CARD"]], size=n, p=[0.70, 0.20, 0.10])
        apr = rng.choice([sim.R_IDX[r] for r in P.ROUTE_MIX_APP], size=n, p=list(P.ROUTE_MIX_APP.values()))
        rows.append({"start": np.zeros(n, int), "title": np.full(n, sim.T_IDX[t]),
                     "channel": np.full(n, sim.C_IDX["DIR"]), "offer": np.full(n, -1),
                     "route": np.where(app, apr, web), "h": h, "p": p, "su_shock": np.zeros(n),
                     "post_shock": np.zeros(n), "tenure0": ten, "cohort": np.zeros(n)})
    return {k: np.concatenate([r[k] for r in rows]) for k in rows[0]}


def cat(a, b):
    return {k: np.concatenate([a[k], b[k]]) for k in a}


def history(seed=P.SEED):
    rng = np.random.default_rng(seed)
    base = base_book(rng)
    plan = []
    for m in range(0, P.CUT + 1):
        for (c, t) in P.LINES:
            n = rng.poisson(line_level(c, t, m))
            plan.append((c, t, m, n, sim.line_offer(c, t, m)))
        for t in P.TITLES:
            n = rng.poisson(line_level("DIR", t, m))
            plan.append(("DIR", t, m, n, sim.line_offer("DIR", t, m)))
    new = sim.new_starts(plan, rng)
    S = cat(base, new)
    n_base = len(base["start"])
    S["kind"] = np.array(["base"] * n_base + ["new"] * len(new["start"]), dtype=object)
    S["parent"] = np.full(len(S["start"]), -1)
    S["newacc"] = np.ones(len(S["start"]), bool)
    # simulate, then the returns in rounds (a household that comes back may leave and come back again)
    res = sim.engine(S, P.CUT, rng)
    allS, allR = [S], [res]
    cur_S, cur_R, offset = S, res, 0
    for _ in range(6):
        R, idx, newacc = sim.returns_of(cur_S, cur_R, P.CUT, rng)
        if R is None or len(R["start"]) == 0:
            break
        R["kind"] = np.array(["return"] * len(R["start"]), dtype=object)
        R["parent"] = idx + offset
        R["newacc"] = newacc
        rr = sim.engine(R, P.CUT, rng)
        offset += len(cur_S["start"])
        allS.append(R)
        allR.append(rr)
        cur_S, cur_R = R, rr
    return assemble(allS, allR, rng)


def assemble(allS, allR, rng):
    """One table of subscriptions (one row per subscription, gross charges by month 0..CUT), with household and
    customer numbers."""
    T = P.CUT + 1
    keys = ["start", "title", "channel", "offer", "route", "h", "p", "su_shock", "post_shock", "tenure0", "cohort",
            "kind", "parent", "newacc"]
    S = {k: np.concatenate([s[k] for s in allS]) for k in keys}
    G = np.zeros((len(S["start"]), T))
    end, reason, L, ip, su_exit, rise_exit = [], [], [], [], [], []
    row = 0
    rec = []
    for s, r in zip(allS, allR):
        n = len(s["start"])
        m0 = r["m0"]
        G[row:row + n, m0:] = r["gross"][:, : T - m0]
        end.append(r["end"])
        reason.append(r["reason"])
        L.append(r["L"])
        ip.append(r["ip"])
        su_exit.append(r["su_exit"])
        rise_exit.append(r["rise_exit"])
        rec += [(row + i, m) for i, m in r["recovered"]]
        row += n
    S["end"] = np.concatenate(end)
    S["reason"] = np.concatenate(reason)
    S["L"] = np.concatenate(L)
    S["ip"] = np.concatenate(ip)
    S["su_exit"] = np.concatenate(su_exit)
    S["rise_exit"] = np.concatenate(rise_exit)
    S["gross"] = G
    S["recovered"] = rec
    n = len(S["start"])
    # households and customer numbers: a new subscription is a new household with a new customer number; a return
    # keeps the household and, on its old account, the customer number
    hh = np.zeros(n, int)
    cust = np.zeros(n, int)
    next_c = 100000
    for i in range(n):
        par = S["parent"][i]
        if par < 0:
            hh[i] = i
            cust[i] = next_c
            next_c += int(rng.integers(1, 4))
        else:
            hh[i] = hh[par]
            if S["newacc"][i]:
                cust[i] = next_c
                next_c += int(rng.integers(1, 4))
            else:
                cust[i] = cust[par]
    S["household"] = hh
    S["customer"] = cust
    # payment fingerprints and addresses: a household keeps both on its old account; on a new account it keeps its
    # payment method in RET_SAME_PAYMENT of cases and its address in RET_SAME_ADDRESS
    fp = np.zeros(n, int)
    ad = np.zeros(n, int)
    nxt_f, nxt_a = 1, 1
    for i in range(n):
        par = S["parent"][i]
        if par < 0:
            fp[i], ad[i] = nxt_f, nxt_a
            nxt_f += 1
            nxt_a += 1
        elif not S["newacc"][i]:
            fp[i], ad[i] = fp[par], ad[par]
        else:
            if rng.random() < P.RET_SAME_PAYMENT:
                fp[i] = fp[par]
            else:
                fp[i] = nxt_f
                nxt_f += 1
            if rng.random() < P.RET_SAME_ADDRESS:
                ad[i] = ad[par]
            else:
                ad[i] = nxt_a
                nxt_a += 1
    S["fingerprint"] = fp
    S["address"] = ad
    S["reading"] = reading(S, rng)
    return S


def reading(S, rng):
    """Reading days in each month a subscription runs, January 2024 to the cut (a matrix, subscriptions x months)."""
    n = len(S["start"])
    T = P.CUT + 1
    R = np.zeros((n, T), dtype=np.int16)
    end = np.where(S["end"] == -2, P.CUT, S["end"])
    for m in range(P.READ_FROM, T):
        act = (S["start"] <= m) & (end >= m) & (S["end"] != -1)
        idx = np.where(act)[0]
        if len(idx) == 0:
            continue
        k = m - S["start"][idx] + 1
        nov = np.where(k == 1, P.R_NOVELTY[0], np.where(k == 2, P.R_NOVELTY[1], 0.0))
        nov = np.where(S["kind"][idx] == "base", 0.0, nov)
        x = (P.R0 + P.R_H * S["h"][idx] + nov + P.R_SEASON.get(sim.cal_month(m), 0.0) + 0.6 * P.NEWS.get(m, 0.0)
             + rng.normal(0, P.R_NOISE, len(idx)))
        R[idx, m] = rng.binomial(sim.days_in(m), sim.sig(x))
    return R


def plan_2027(rng=None):
    """The 2027 media plan's planned starts by line and month: the line's 2026 level, its season and the plan's
    growth, rounded as the marketing team plans them."""
    out = {}
    for (c, t), (_, offer, lvl) in P.LINES.items():
        g = P.PLAN_GROWTH.get((c, t), 1.0)
        months = []
        for m in range(P.PLAN0, P.PLAN1 + 1):
            x = lvl * g * P.START_SEASON[sim.cal_month(m)]
            months.append(int(round(x)))
        out[(c, t)] = {"offer": offer, "starts": months}
    return out


def truth_lines(plan, reps=20, seed=P.SEED + 7, return_detail=False):
    """Clean-truth 36-month net revenue per start for each 2027 line: the plan's starts drawn many times from the
    true process (the line's current habit mean, fresh line-month shocks, the April 2027 rise, returns within the
    36 months), net of VAT and store fees."""
    rng = np.random.default_rng(seed)
    out = {}
    for (c, t), spec in plan.items():
        tot, n_all = 0.0, 0
        su_n, su_k = 0, 0
        for r in range(reps):
            lm = [(c, t, P.PLAN0 + i, n, spec["offer"]) for i, n in enumerate(spec["starts"])]
            S = sim.new_starts(lm, rng, ref_window=(P.CUT - 11, P.CUT))
            # 2027 starts resemble the line's starts of the twelve months to the cut (the plan's convention)
            res = sim.engine(S, P.PLAN1 + P.HORIZON, rng)
            net = sim.store_net(res["gross"], S["route"])
            m0 = res["m0"]
            val = np.zeros(len(S["start"]))
            for i in range(len(val)):
                a = S["start"][i] - m0
                val[i] = net[i, a: a + P.HORIZON].sum()
            # returns within the 36 months
            R, idx, newacc = sim.returns_of(S, res, P.PLAN1 + P.HORIZON, rng)
            depth = 0
            curS, curR, curIdx = S, res, np.arange(len(val))
            while R is not None and len(R["start"]) and depth < 4:
                rr = sim.engine(R, P.PLAN1 + P.HORIZON, rng)
                rn = sim.store_net(rr["gross"], R["route"])
                owner = curIdx[idx]
                for q in range(len(R["start"])):
                    o = owner[q]
                    a0 = S["start"][o]
                    lo, hi = R["start"][q], a0 + P.HORIZON - 1
                    if lo <= hi:
                        val[o] += rn[q, lo - rr["m0"]: hi - rr["m0"] + 1].sum()
                curS, curR, curIdx = R, rr, owner
                R, idx, newacc = sim.returns_of(curS, curR, P.PLAN1 + P.HORIZON, rng)
                depth += 1
            ok = res["end"] != -1
            tot += val[ok].sum()
            n_all += ok.sum()
            su_n += (res["su_exit"] & ok).sum()
            su_k += ok.sum()
        out[(c, t)] = {"ltv": tot / max(n_all, 1), "su": su_n / max(su_k, 1)}
    return out
