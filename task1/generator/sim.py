"""The process behind Medienhaus Brückenhafen's digital subscriptions (task1 architecture 3).

Households carry a reading habit h and a price sensitivity p. A household starts a subscription on one title through
one channel at the offer that channel ran that month; it pays the introductory price, decides at the first full-price
billing whether to stay (the decision rides on the discount it is losing, how long the introduction lasted, the full
price it is stepping up to, its price sensitivity and a little on its habit), then cancels month by month at a rate
that falls with time on the full price and with its habit. Debits fail and are re-presented or end the subscription.
A list-price rise takes effect at each subscription's first billing on or after the 1st of April; the notice letters
of February move part of the extra leaving to the end of March. A household that has left may come back through the
paywall, under its old customer number or a new one.

engine() steps any batch of subscriptions month by month and is used for the history, the base's future and the
clean-truth value of the 2027 lines; history() builds the record the pack is cut from."""
import math

import numpy as np

import params as P

T_IDX = {t: i for i, t in enumerate(P.TITLES)}
C_IDX = {c: i for i, c in enumerate(P.CHANNELS)}
ROUTES = ["SEPA", "PAYPAL", "CARD", "APPLE", "GOOGLE"]
R_IDX = {r: i for i, r in enumerate(ROUTES)}
OFFER_CODES = list(P.OFFERS)
O_IDX = {o: i for i, o in enumerate(OFFER_CODES)}


def ym(m):
    return P.M0_YEAR + (P.M0_MONTH - 1 + m) // 12, (P.M0_MONTH - 1 + m) % 12 + 1


def cal_month(m):
    return ym(m)[1]


def days_in(m):
    y, mo = ym(m)
    if mo == 12:
        return 31
    import datetime as dt
    return (dt.date(y, mo + 1, 1) - dt.date(y, mo, 1)).days


def full_price(title_idx, m):
    """Gross full price in force at month m (arrays allowed)."""
    t = np.asarray(title_idx)
    m = np.asarray(m)
    tab = np.array([P.PRICE[x] for x in P.TITLES])          # titles x 3
    era = np.where(m >= P.RISE_2027, 2, np.where(m >= P.RISE_2025, 1, 0))
    return tab[t, era]


def intro_price(offer_idx, title_idx, start_m):
    """Gross monthly introductory price, fixed at the start."""
    o = np.asarray(offer_idx)
    out = np.zeros(o.shape)
    fp = full_price(title_idx, start_m)
    for code, i in O_IDX.items():
        sel = o == i
        spec = P.OFFERS[code]
        out[sel] = spec["fixed"] if "fixed" in spec else np.round(spec["share"] * fp[sel], 2)
    return out


def intro_months(offer_idx):
    tab = np.array([P.OFFERS[c]["months"] for c in OFFER_CODES])
    return tab[np.asarray(offer_idx)]


def sig(x):
    return 1.0 / (1.0 + np.exp(-x))


def engine(S, m_end, rng, rise_months=(P.RISE_2025, P.RISE_2027), record=False):
    """Step subscriptions S (dict of equal-length arrays) month by month to m_end inclusive.

    S keys: start (month index), title, channel, offer (-1 for none: a returning household on its old account pays
    full price at once), route, h, p, su_shock, post_shock, tenure0 (months already paid before month 'start' for
    the subscriptions running in January 2023, else 0), lead (paid months before start for the base, so the store
    fee clock and tenure count from the real start).
    Returns end (last month the subscription is billed, -1 if withdrawn), reason, gross (N x T charges), and the
    step-up month, with month 0 of the gross matrix at min(start)."""
    N = len(S["start"])
    m0 = int(S["start"].min()) if N else 0
    T = m_end - m0 + 1
    start = S["start"].astype(int)
    L = np.where(S["offer"] >= 0, intro_months(np.maximum(S["offer"], 0)), 0)
    ip = np.where(S["offer"] >= 0, intro_price(np.maximum(S["offer"], 0), S["title"], start), 0.0)
    alive = np.ones(N, bool)
    end = np.full(N, 10 ** 6)
    reason = np.full(N, "", dtype=object)
    gross = np.zeros((N, T))
    failed_recovered = []                  # (index, month) of re-presented debits, for the texture
    rise_exit = np.full(N, -1)             # month the rise's extra leaving takes effect
    su_exit = np.zeros(N, bool)
    ch = S["channel"].astype(int)
    ti = S["title"].astype(int)
    route = S["route"].astype(int)
    h, p = S["h"], S["p"]
    tenure0 = S.get("tenure0", np.zeros(N, int)).astype(int)
    stepup_m = start + L
    inv = np.array([P.INVOL[r] for r in ROUTES])
    wd = np.array([P.WITHDRAW[c] for c in P.CHANNELS])
    su_ch = np.array([P.SU_CH[c] for c in P.CHANNELS])
    su_ti = np.array([P.SU_TITLE[t] for t in P.TITLES])
    post_ch = np.array([P.POST_CH[c] for c in P.CHANNELS])
    base_price = np.array([P.PRICE[t][0] for t in P.TITLES])
    depth = np.where(S["offer"] >= 0, 1.0, 0.0)
    for m in range(m0, m_end + 1):
        j = m - m0
        act = alive & (start <= m)
        if not act.any():
            continue
        k = m - start + 1                              # billed month of this subscription (1 at start)
        first = act & (k == 1)
        # withdrawal in the first 14 days
        if first.any():
            w = first & (S["offer"] >= 0) & (rng.random(N) < wd[ch])
            alive[w] = False
            end[w] = -1
            reason[w] = "WITHDRAWN"
            act = act & ~w
        # the decision at the first full-price billing
        su = act & (S["offer"] >= 0) & (k == L + 1)
        if su.any():
            fp = full_price(ti, m)
            d = 1.0 - ip / fp
            x = (P.SU_A0 + su_ch[ch] + su_ti[ti] + P.SU_DEPTH * d * depth + P.SU_LEN * np.log(np.maximum(L, 1))
                 + P.SU_PRICE * np.log(fp / base_price[ti]) + P.SU_P * p + P.SU_H * h + S["su_shock"])
            leave = su & (rng.random(N) < sig(x))
            alive[leave] = False
            end[leave] = m - 1
            reason[leave] = "CANCELLED"
            su_exit[leave] = True
            act = act & ~leave
        if not act.any():
            continue
        # the rise: decided on the notice (the month before the new price), for those already on the full price
        for R in rise_months:
            if m == R - 1:
                on_full = act & (k >= L + 1) & (rise_exit < 0)
                paid_ten = k + tenure0
                x = (P.RISE_X0 + P.RISE_YOUNG * (paid_ten < 12) + P.RISE_MID * ((paid_ten >= 12) & (paid_ten < 36))
                     + P.RISE_P * p + P.RISE_H * h)
                go = on_full & (rng.random(N) < sig(x))
                tm = rng.choice(3, size=N, p=list(P.RISE_TIMING))
                rise_exit[go] = R - 1 + tm[go]
        # charge the month
        intro = act & (k <= L)
        fullm = act & (k > L)
        gross[intro, j] = ip[intro]
        gross[fullm, j] = full_price(ti[fullm], m)
        # a failed debit: re-presented next month, or the end
        fail = act & (gross[:, j] > 0) & (k >= 2) & (rng.random(N) < inv[route])
        rec = fail & (rng.random(N) < P.RECOVER)
        for i in np.where(rec)[0]:
            failed_recovered.append((i, m))
        lost = fail & ~rec
        gross[lost, j] = 0.0
        alive[lost] = False
        end[lost] = m - 1
        reason[lost] = "PAYMENT_FAILED"
        act = act & ~lost
        # the rise's leaving takes effect after the month it is due
        r_go = act & (rise_exit == m)
        alive[r_go] = False
        end[r_go] = m
        reason[r_go] = "CANCELLED"
        act = act & ~r_go
        # cancelling at the end of the month
        haz = np.zeros(N)
        haz[intro] = P.INTRO_HAZ
        jj = (k - L + tenure0)[fullm].astype(float)
        hz = (P.POST_BASE * (P.POST_FLOOR + (1 - P.POST_FLOOR) * np.exp(-(jj - 1) / P.POST_TAU))
              * post_ch[ch[fullm]] * np.exp(-P.POST_H * h[fullm] + P.POST_P * p[fullm] + S["post_shock"][fullm])
              * P.SUMMER.get(cal_month(m), 1.0))
        haz[fullm] = np.minimum(hz, 0.6)
        go = act & (rng.random(N) < haz)
        alive[go] = False
        end[go] = m
        reason[go] = "CANCELLED"
    end = np.where(end == 10 ** 6, -2, end)            # -2: still running at m_end
    return {"end": end, "reason": reason, "gross": gross, "m0": m0, "L": L, "ip": ip, "stepup": stepup_m,
            "su_exit": su_exit, "recovered": failed_recovered, "rise_exit": rise_exit}


def store_net(gross, route, lead=None):
    """Net revenue matrix: gross less VAT, less the store's fee (Apple 30 per cent for a subscription's first 12
    paid months, then 15; Google 15)."""
    net = gross / (1.0 + P.VAT)
    paid = (gross > 0).cumsum(axis=1)
    if lead is not None:
        paid = paid + lead[:, None]
    for r, (f1, f2) in P.STORE_FEE.items():
        sel = route == R_IDX[r]
        if sel.any():
            fee = np.where(paid[sel] <= 12, f1, f2)
            net[sel] = net[sel] * (1 - fee)
    return net


def draw_hp(n, h_mean, p_mean, rng):
    z1 = rng.standard_normal(n)
    z2 = rng.standard_normal(n)
    h = h_mean + z1
    p = p_mean + P.HP_CORR * z1 + math.sqrt(1 - P.HP_CORR ** 2) * z2
    return h, p


def h_shift(channel, m):
    if channel not in P.DRIFT:
        return 0.0
    a, b, s = P.DRIFT[channel]
    if m < a:
        return 0.0
    if m >= b:
        return s
    return s * (m - a + 1) / (b - a + 1)


def dir_offer(m):
    if m in P.DIR_BF_ANNUAL:
        return "J12"
    return P.DIR_OFFER[cal_month(m)]


def line_offer(channel, title, m):
    if channel == "DIR":
        return dir_offer(m)
    hist = P.LINES[(channel, title)][0]
    cur = hist[0][1]
    for frm, o in hist:
        if m >= frm:
            cur = o
    return cur


def routes_for(channel, n, rng):
    if channel == "APP":
        mix = P.ROUTE_MIX_APP
    elif channel == "DIR":
        app = rng.random(n) < P.DIR_APP_SHARE
        a = rng.choice([R_IDX[r] for r in P.ROUTE_MIX_APP], size=n, p=list(P.ROUTE_MIX_APP.values()))
        w = rng.choice([R_IDX[r] for r in P.ROUTE_MIX_WEB], size=n, p=list(P.ROUTE_MIX_WEB.values()))
        return np.where(app, a, w)
    else:
        mix = P.ROUTE_MIX_WEB
    return rng.choice([R_IDX[r] for r in mix], size=n, p=list(mix.values()))


def new_starts(lines_months, rng, plan=None, ref_window=None):
    """New subscriptions for (channel, title, month, count) tuples: households drawn with the line's habit mean, its
    drift and a line-month shock shared by everyone the month brought in."""
    cols = {k: [] for k in ["start", "title", "channel", "offer", "route", "h", "p", "su_shock", "post_shock",
                            "tenure0", "cohort"]}
    for (c, t, m, n, offer) in lines_months:
        if n <= 0:
            continue
        eta = rng.normal(0, P.COHORT_SD)
        su_s = rng.normal(0, P.COHORT_SU_SD)
        po_s = rng.normal(0, P.COHORT_POST_SD)
        if ref_window is None:
            hm = P.H_MEAN[c] + P.TITLE_H[t] + h_shift(c, min(m, P.CUT)) + eta
        else:
            # a 2027 start resembles the line's starts of a month drawn from the reference window
            refs = rng.integers(ref_window[0], ref_window[1] + 1, size=n)
            hm = P.H_MEAN[c] + P.TITLE_H[t] + np.array([h_shift(c, int(x)) for x in refs]) + eta
        h, p = draw_hp(n, hm, P.P_MEAN[c], rng)
        cols["start"].append(np.full(n, m))
        cols["title"].append(np.full(n, T_IDX[t]))
        cols["channel"].append(np.full(n, C_IDX[c]))
        cols["offer"].append(np.full(n, O_IDX[offer]))
        cols["route"].append(routes_for(c, n, rng))
        cols["h"].append(h)
        cols["p"].append(p)
        cols["su_shock"].append(np.full(n, su_s))
        cols["post_shock"].append(np.full(n, po_s))
        cols["tenure0"].append(np.zeros(n, int))
        cols["cohort"].append(np.full(n, eta))
    return {k: np.concatenate(v) if v else np.zeros(0) for k, v in cols.items()}


def returns_of(S, res, m_end, rng):
    """Each household that left (not withdrawn) may come back through the paywall: under a new customer number at
    that month's paywall offer, or on its old account at the full price."""
    end = res["end"]
    left = np.where(end >= 0)[0]
    left = left[end[left] < m_end]
    if len(left) == 0:
        return None, left, None
    h = S["h"][left]
    lam = P.RET_R0 * np.exp(P.RET_H * h) * P.RET_TAU
    u = rng.random(len(left))
    tot = 1 - np.exp(-lam)
    back = u < tot
    # invert H(s) = lam (1 - exp(-s / tau)) = -log(1 - u)
    s = np.full(len(left), 10 ** 6, float)
    val = 1 - (-np.log(1 - u[back])) / lam[back]
    s[back] = np.ceil(-P.RET_TAU * np.log(np.maximum(val, 1e-12)))
    rm = end[left] + np.maximum(s, 1).astype(int)
    ok = back & (rm <= m_end)
    idx = left[ok]
    rm = rm[ok]
    n = len(idx)
    newacc = rng.random(n) < P.RET_NEW_ACCOUNT
    offer = np.array([O_IDX[dir_offer(int(x))] for x in rm]) if n else np.zeros(0, int)
    R = {"start": rm, "title": S["title"][idx], "channel": np.full(n, C_IDX["DIR"]),
         "offer": np.where(newacc, offer, -1), "route": S["route"][idx], "h": S["h"][idx], "p": S["p"][idx],
         "su_shock": np.zeros(n), "post_shock": np.zeros(n), "tenure0": np.zeros(n, int),
         "cohort": np.zeros(n)}
    return R, idx, newacc
