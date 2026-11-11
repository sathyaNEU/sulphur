"""The nine results of the chain for one set of choices (a route): R1 the paying subscribers at 31 October 2026 by
title; R2 the realised 36-month net revenue per start of the July to September 2023 starts by channel; R3 the share
of each 2027 offer's starts leaving at the end of the introductory price at 2026 prices; R4 the points the April 2027
prices add to it; R5 the share of the November 2025 to April 2026 starts still paying two years after starting, by
channel; R6 the extra cancellations the April 2027 rise brings by 31 December 2027 among the subscriptions paying at
31 October 2026, by title; R7 every 2027 line's expected 36-month net revenue per start; R8 the funded lines; R9 the
households of the October 2026 base paying at 31 December 2027, by title."""
import numpy as np

import lines as LN
import models
import params as P
import sim

R2_MONTHS = (6, 7, 8)           # July to September 2023
R5_MONTHS = (34, 39)            # November 2025 to April 2026
R5_AT = 36                      # months after the start


def fit(pn, o):
    M = models.fit_all(pn, o)
    M["settled"] = models.fit_settled(pn, o)
    return M


def paying_oct(pn):
    return pn["gross"][:, P.CUT] > 0


def r1(pn):
    pay = paying_oct(pn)
    return {t: int((pay & (pn["title"] == sim.T_IDX[t])).sum()) for t in P.TITLES}


def r2(pn, o):
    """Realised net revenue per start over each start's first 36 months, with the household's later subscriptions
    inside those months."""
    hh = models.link(pn, o["link"]) if o["link"] != ("fingerprint", "address") else pn["household"]
    net = net_matrix(pn)
    sel = np.isin(pn["start"], R2_MONTHS) & (pn["kind"] == "new") & ~pn["withdrawn"]
    by_hh = {}
    for i in range(pn["n"]):
        by_hh.setdefault(hh[i], []).append(i)
    out = {}
    for c in P.CHANNELS:
        idx = np.where(sel & (pn["channel"] == sim.C_IDX[c]))[0]
        vals = []
        for i in idx:
            a, b = pn["start"][i], pn["start"][i] + P.HORIZON - 1
            v = net[i, a: b + 1].sum()
            if o["returns"]:
                for q in by_hh[hh[i]]:
                    if q != i and pn["start"][q] > pn["start"][i] and pn["start"][q] <= b:
                        v += net[q, pn["start"][q]: b + 1].sum()
            vals.append(v)
        out[c] = float(np.mean(vals))
    return out


def net_matrix(pn):
    """Net revenue by subscription and month from the charges: VAT out, the store's fee by paid month."""
    g = pn["gross"]
    paid = (g > 0).cumsum(axis=1)
    if "tenure0" in pn:
        paid = paid + pn["tenure0"][:, None]
    f = models.net_factor(np.repeat(pn["route"][:, None], g.shape[1], axis=1), paid)
    return g * f


def r3_r4(M, plan):
    """For each 2027 offer, over the lines that carry it (weighted by planned starts): the share leaving at the
    end of the introductory price at 2026 prices, and the points the April 2027 prices add for a start stepping up
    after them."""
    out3, out4 = {}, {}
    for code in sim.OFFER_CODES:
        ls = [(l, sum(s["starts"])) for l, s in plan.items() if s["offer"] == code]
        if not ls:
            continue
        a26, a27, w = 0.0, 0.0, 0
        for (c, t), n in ls:
            ch = np.array([sim.C_IDX[c]])
            ti = np.array([sim.T_IDX[t]])
            of = np.array([sim.O_IDX[code]])
            m_st = np.array([P.PLAN0 + 6])
            step = m_st + P.OFFERS[code]["months"]
            p27 = models.su_prob(M["su"], ch, ti, of, m_st, step)[0]
            p26 = models.su_prob(M["su"], ch, ti, of, m_st, np.array([P.RISE_2027 - 1]))[0]
            a26 += n * p26
            a27 += n * p27
            w += n
        out3[code] = a26 / w
        out4[code] = (a27 - a26) / w
    return out3, out4


def continuation(M, pn, idx, H, rise_on=True, no_rise_price=False):
    """From the cut forward: each subscription's chance of paying in each later month (it is running at the
    cut), and of leaving at each month's end."""
    k0 = (P.CUT - pn["start"][idx] + 1).astype(int)
    ten0 = pn["tenure0"][idx]
    rev, leave, pay = models.spell(M, pn["channel"][idx], pn["title"][idx], pn["offer"][idx], pn["start"][idx],
                                   pn["proxy"][idx], pn["route"][idx], H, rise_on=rise_on, k0=k0, ten0=ten0,
                                   no_rise_price=no_rise_price)
    return rev, leave, pay


def r5(M, pn):
    out = {}
    sel = (pn["start"] >= R5_MONTHS[0]) & (pn["start"] <= R5_MONTHS[1]) & (pn["kind"] == "new") & ~pn["withdrawn"]
    for c in P.CHANNELS:
        idx = np.where(sel & (pn["channel"] == sim.C_IDX[c]))[0]
        run = idx[pn["running"][idx]]
        # the 25th billing comes R5_AT months after the start
        need = (pn["start"][run] + R5_AT - P.CUT).astype(int)
        H = int(need.max())
        _, _, pay = continuation(M, pn, run, H)
        p = pay[np.arange(len(run)), need - 1]
        out[c] = float(p.sum() / len(idx))
    return out


def base_rows(pn):
    return np.where(paying_oct(pn) | (pn["running"] & (pn["gross"][:, P.CUT] == 0) & False))[0]


def r6(M, pn):
    idx = np.where(paying_oct(pn) & pn["running"])[0]
    H = P.BASE_END - P.CUT
    _, _, pay_r = continuation(M, pn, idx, H, rise_on=True)
    _, _, pay_n = continuation(M, pn, idx, H, rise_on=False, no_rise_price=True)
    # still paying in December 2027 with and without the rise
    diff = pay_n[:, -1] - pay_r[:, -1]
    return {t: float(diff[pn["title"][idx] == sim.T_IDX[t]].sum()) for t in P.TITLES}


def r9(M, pn, o, since=None):
    sel = paying_oct(pn) & pn["running"]
    if since is not None:
        sel &= (pn["start"] >= since) & (pn["kind"] != "base")
    idx = np.where(sel)[0]
    H = P.BASE_END - P.CUT
    _, leave, pay = continuation(M, pn, idx, H, rise_on=True)
    p = pay[:, -1].copy()
    if o["returns"]:
        # a household that leaves after the cut and comes back by December 2027, paying then
        px = pn["proxy"][idx]
        px_r = np.where(np.isnan(px), np.nanmean(pn["proxy"]), px)
        for e in range(H - 1):
            pe = leave[:, e]
            surv = np.ones(len(idx))
            for s in range(1, H - e):
                r = models.ret_hazard(M["ret"], s, px_r) * surv
                surv = surv - r
                m_ret = P.CUT + 1 + e + s
                Hr = P.BASE_END - m_ret + 1
                if Hr <= 0:
                    break
                ch = np.full(len(idx), sim.C_IDX["DIR"])
                off_new = np.full(len(idx), sim.O_IDX[sim.dir_offer(m_ret)])
                _, _, pn_new = models.spell(M, ch, pn["title"][idx], off_new, np.full(len(idx), m_ret), px_r,
                                            pn["route"][idx], Hr)
                _, _, pn_old = models.spell(M, ch, pn["title"][idx], np.full(len(idx), -1), np.full(len(idx), m_ret),
                                            px_r, pn["route"][idx], Hr)
                q = M["newacc"]
                p += pe * r * (q * pn_new[:, -1] + (1 - q) * pn_old[:, -1])
    return {t: float(p[pn["title"][idx] == sim.T_IDX[t]].sum()) for t in P.TITLES}


def r9_plan(M, pn, plan):
    """The plan's 2027 starts, every line run as planned: the number paying on 31 December 2027, by channel."""
    out = {c: 0.0 for c in P.PAID}
    for (c, t), spec in plan.items():
        px, rt = LN.line_inputs(pn, (c, t))
        K = len(px)
        L = P.OFFERS[spec["offer"]]["months"]
        free = P.OFFERS[spec["offer"]].get("fixed", 1.0) == 0.0
        for mi, n in enumerate(spec["starts"]):
            if n <= 0:
                continue
            m0 = P.PLAN0 + mi
            # paying on 31 December 2027: charged above zero, so a start still in a free month is not paying
            if free and (P.BASE_END - m0) < L:
                continue
            _, _, pay = models.spell(M, np.full(K, sim.C_IDX[c]), np.full(K, sim.T_IDX[t]),
                                     np.full(K, sim.O_IDX[spec["offer"]]), np.full(K, m0), px, rt,
                                     P.BASE_END - m0 + 1, line=(c, t))
            out[c] += n * float(pay[:, -1].mean())
    return out


def all_results(pn, plan, o, M=None):
    M = M or fit(pn, o)
    v, _ = LN.values(pn, plan, o, M=M)
    R = {"R1": r1(pn), "R2": r2(pn, o)}
    R["R3"], R["R4"] = r3_r4(M, plan)
    R["R5"] = r5(M, pn)
    R["R6"] = r6(M, pn)
    R["R7"] = v
    R["R9"] = r9_plan(M, pn, plan)
    return R, M


def r9_intro(M, pn):
    """The subscriptions on an introductory price at 31 October 2026: the number paying the full price on that
    subscription at 31 December 2027, by title."""
    sel = pn["running"] & (pn["offer"] >= 0) & (pn["stepup"] > P.CUT) & (pn["kind"] != "base")
    idx = np.where(sel)[0]
    H = P.BASE_END - P.CUT
    _, _, pay = continuation(M, pn, idx, H, rise_on=True)
    p = pay[:, -1]
    return {t: float(p[pn["title"][idx] == sim.T_IDX[t]].sum()) for t in P.TITLES}, {
        t: int((pn["title"][idx] == sim.T_IDX[t]).sum()) for t in P.TITLES}
