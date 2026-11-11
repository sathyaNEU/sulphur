"""The analysis, written once against the panel (panel.py) and run with switches, so the golden, the careful but
hurried pass and every rival are the same code with different choices.

Choices (opts):
  su_price     the end-of-intro model carries the full price stepped up to (golden) or a post-April-2025 period term
               (careful) or neither
  su_form      'offer' (offer terms) or 'depth' (discount depth and log intro months)
  completion   'proxy' (hazard on full price by tenure, channel and early reading; golden) or 'channel' (by tenure
               and channel only, every month kept: the chain-ladder a careful run builds)
  proxy_adj    early reading taken raw (golden) or against the month's average across subscribers
  rise_window  months of the April 2025 rise's extra leaving: (26, 27, 28) golden (notice letters, the first and
               second new-price months), (27, 28) careful
  rise_bands   'tenure' (golden) or 'pooled'
  link         ('fingerprint', 'address') golden, ('fingerprint',) or ('address',) rivals, () careful
  returns      True (golden) or False
"""
import numpy as np
import statsmodels.api as sm

import params as P
import sim

CH = P.CHANNELS
TI = P.TITLES
TBINS = [(1, 1), (2, 2), (3, 3), (4, 6), (7, 12), (13, 24), (25, 999)]
BASE_PRICE = np.array([P.PRICE[t][0] for t in TI])

GOLD = {"su_price": "price", "su_form": "offer", "completion": "proxy", "proxy_adj": False, "proxy_form": "log",
        "rise_window": (26, 27, 28), "rise_bands": "tenure", "link": ("fingerprint", "address"), "returns": True,
        "second_returns": False}


def opts(**kw):
    o = dict(GOLD)
    o.update(kw)
    return o


def fit_logit(X, y):
    m = sm.GLM(y, X, family=sm.families.Binomial()).fit()
    return m.params


def tbin(j):
    j = np.asarray(j)
    out = np.zeros((len(j), len(TBINS)))
    for b, (lo, hi) in enumerate(TBINS):
        out[:, b] = (j >= lo) & (j <= hi)
    return out


def onehot(v, k, drop_first=True):
    v = np.asarray(v).astype(int)
    out = np.zeros((len(v), k))
    out[np.arange(len(v)), v] = 1
    return out[:, 1:] if drop_first else out


# ---------------------------------------------------------------- the end of the introductory price

def su_rows(pn):
    """Subscriptions that reached the decision at the first full-price billing, by the cut."""
    ok = (pn["offer"] >= 0) & ~pn["withdrawn"] & (pn["stepup"] <= P.CUT) & (pn["last"] >= pn["stepup"] - 1)
    idx = np.where(ok)[0]
    y = (pn["end"][idx] == pn["stepup"][idx] - 1) & (pn["reason"][idx] == "CANCELLED")
    return idx, y.astype(float)


def su_design(ch, ti, offer, L, ip, m_step, o, proxy=None):
    fp = sim.full_price(ti, m_step)
    cols = [np.ones(len(ch)), onehot(ch, len(CH)), onehot(ti, len(TI))]
    if o["su_form"] == "offer":
        cols.append(onehot(offer, len(sim.OFFER_CODES)))
    else:
        d = 1 - ip / fp
        cols += [d[:, None], np.log(np.maximum(L, 1))[:, None]]
    if o["su_price"] == "price":
        cols.append(np.log(fp / BASE_PRICE[ti])[:, None])
    elif o["su_price"] == "period":
        cols.append((m_step >= P.RISE_2025)[:, None].astype(float))
    if o.get("su_proxy"):
        px = np.full(len(ch), SU_PROXY_FILL[0]) if proxy is None else np.asarray(proxy, float)
        cols.append(np.nan_to_num(px, nan=SU_PROXY_FILL[0])[:, None])
    return np.column_stack([c if c.ndim == 2 else c[:, None] for c in cols])


SU_PROXY_FILL = [7.0]


def fit_su(pn, o):
    SU_PROXY_FILL[0] = float(np.nanmean(pn["proxy"]))
    idx, y = su_rows(pn)
    X = su_design(pn["channel"][idx], pn["title"][idx], pn["offer"][idx], pn["L"][idx], pn["ip"][idx],
                  pn["stepup"][idx], o, pn["proxy"][idx])
    return {"b": fit_logit(X, y), "o": o}


def su_prob(model, ch, ti, offer, m_start, m_step, proxy=None):
    o = model["o"]
    L = sim.intro_months(offer)
    ip = sim.intro_price(offer, ti, m_start)
    X = su_design(ch, ti, offer, L, ip, m_step, o, proxy)
    if o["su_price"] == "period":
        X[:, -1] = (m_step >= P.RISE_2025).astype(float)
    return sim.sig(X @ model["b"])


# ---------------------------------------------------------------- leaving on the full price

def hazard_rows(pn, o, kinds=("new", "return")):
    """Subscription-months on the full price: j months since the first full-price billing."""
    use_proxy = o["completion"] == "proxy"
    ok = np.isin(pn["kind"], kinds) & ~pn["withdrawn"] & (pn["last"] >= pn["stepup"]) & (pn["stepup"] <= P.CUT)
    if use_proxy:
        ok &= ~np.isnan(pn["proxy"])
    rows_i, rows_m = [], []
    for i in np.where(ok)[0]:
        a, b = pn["stepup"][i], min(pn["last"][i], P.CUT - 1)
        if b < a:
            continue
        rows_i.append(np.full(b - a + 1, i))
        rows_m.append(np.arange(a, b + 1))
    ii = np.concatenate(rows_i)
    mm = np.concatenate(rows_m)
    y = ((pn["end"][ii] == mm) & (pn["reason"][ii] == "CANCELLED")).astype(float)
    # the April 2025 rise's months are left out for the subscriptions it reached (the golden reads its excess
    # separately); the careful pass keeps every month
    if use_proxy or o.get("drop_rise_months"):
        exposed = (pn["stepup"][ii] <= 26) & (mm >= 26) & (mm <= 28)
        keep = ~exposed
        ii, mm, y = ii[keep], mm[keep], y[keep]
    return ii, mm, y


def proxy_of(pn, o):
    px = pn["proxy"].copy()
    if o["proxy_adj"]:
        px = px - np.nanmean(px)
    return px


PBINS = [0, 2, 4, 7, 11, 16, 32]


def proxy_cols(px, form):
    px = np.atleast_1d(px).astype(float)
    if form == "linear":
        return px[:, None]
    if form == "log":
        return np.log1p(np.maximum(px, 0))[:, None]
    if form == "quad":
        return np.column_stack([px, px ** 2 / 10.0])
    out = np.zeros((len(px), len(PBINS) - 2))
    b = np.digitize(px, PBINS[1:-1])
    for q in range(1, len(PBINS) - 1):
        out[:, q - 1] = b == q
    return out


CAL = np.array([sim.cal_month(m) for m in range(0, 200)])


def hz_design(ch, j, proxy, m, o, ti=None):
    j = np.atleast_1d(j)
    m = np.broadcast_to(np.atleast_1d(m), j.shape)
    if o.get("tenure_form", "bins") == "decay":
        jt = j.astype(float)
        cols = [np.column_stack([np.ones(len(jt)), np.exp(-(jt - 1) / 8.0), np.log(jt)]), onehot(ch, len(CH))]
    else:
        cols = [tbin(j), onehot(ch, len(CH))]
    if o.get("hz_title") and ti is not None:
        cols.append(onehot(np.broadcast_to(np.atleast_1d(ti), j.shape), len(TI)))
    if o["completion"] == "proxy":
        cols.append(proxy_cols(np.broadcast_to(np.atleast_1d(proxy), j.shape), o.get("proxy_form", "log")))
    summer = np.isin(CAL[m.astype(int)], [7, 8]).astype(float)
    cols.append(summer[:, None])
    return np.column_stack(cols)


def fit_hazard(pn, o):
    ii, mm, y = hazard_rows(pn, o)
    j = mm - pn["stepup"][ii] + 1
    px = proxy_of(pn, o)[ii] if o["completion"] == "proxy" else np.zeros(len(ii))
    X = hz_design(pn["channel"][ii], j, px, mm, o, pn["title"][ii])
    b = fit_logit(X, y)
    return {"b": b, "o": o, "mean_proxy": float(np.nanmean(pn["proxy"]))}


def hazard(model, ch, j, proxy, m, ti=None):
    o = model["o"]
    X = hz_design(np.atleast_1d(ch), np.atleast_1d(j), np.atleast_1d(proxy) if o["completion"] == "proxy"
                  else np.zeros(np.size(j)), m, o, ti)
    return sim.sig(X @ model["b"])


def invol_rates(pn):
    """Debits that ended a subscription, per billed month, by payment route."""
    out = {}
    for r, ri in sim.R_IDX.items():
        sel = (pn["route"] == ri) & (pn["kind"] != "base")
        billed = (pn["gross"][sel] > 0).sum()
        fails = ((pn["reason"][sel] == "PAYMENT_FAILED")).sum()
        out[ri] = fails / max(billed, 1)
    return out


def intro_rate(pn):
    sel = (pn["offer"] >= 0) & ~pn["withdrawn"] & (pn["kind"] != "base")
    months = np.minimum(pn["L"][sel], np.maximum(np.minimum(pn["last"][sel], P.CUT) - pn["start"][sel] + 1, 0))
    early = sel & (pn["reason"] == "CANCELLED") & (pn["end"] < pn["stepup"] - 1)
    return early.sum() / max(months.sum(), 1)


# ---------------------------------------------------------------- the April 2025 rise

def rise_model(pn, hz, o):
    """Extra leaving the April 2025 rise caused among subscriptions on the full price at the notice, by paid tenure:
    the window's cancellations against what the full-price hazard expects there."""
    m_notice = P.RISE_2025 - 1
    exp_set = (~pn["withdrawn"]) & (pn["stepup"] <= m_notice) & (pn["last"] >= m_notice) & (pn["start"] <= m_notice)
    ten = m_notice - pn["start"] + 1 + pn["tenure0"]
    band = np.where(ten < 12, 0, np.where(ten < 36, 1, 2))
    win = o["rise_window"]
    out = {}
    groups = [0, 1, 2] if o["rise_bands"] == "tenure" else [None]
    # what the hazard expects, by band: the band's own cancelling rate in the twelve months either side
    for g in groups:
        sel = exp_set & ((band == g) if g is not None else True)
        n = sel.sum()
        obs = sum(((pn["end"] == m) & (pn["reason"] == "CANCELLED") & sel).sum() for m in win)
        # the band's monthly rate outside the window
        rate_rows, rate_ev = 0, 0
        for m in list(range(14, 25)) + list(range(30, 41)):
            if sim.cal_month(m) in (7, 8):
                continue
            ten_m = m - pn["start"] + 1 + pn["tenure0"]
            bm = np.where(ten_m < 12, 0, np.where(ten_m < 36, 1, 2))
            at = (~pn["withdrawn"]) & (pn["stepup"] <= m) & (pn["last"] >= m) & (pn["start"] <= m)
            if g is not None:
                at &= bm == g
            rate_rows += at.sum()
            rate_ev += (at & (pn["end"] == m) & (pn["reason"] == "CANCELLED")).sum()
        base = rate_ev / max(rate_rows, 1)
        extra = obs / max(n, 1) - (1 - (1 - base) ** len(win))
        out[g] = max(extra, 0.0)
    return {"extra": out, "o": o}


def rise_extra(rm, paid_tenure):
    if rm["o"]["rise_bands"] == "pooled":
        return np.full(np.size(paid_tenure), rm["extra"][None])
    t = np.asarray(paid_tenure)
    return np.where(t < 12, rm["extra"][0], np.where(t < 36, rm["extra"][1], rm["extra"][2]))


# ---------------------------------------------------------------- returns

def fit_returns(pn, o):
    """Monthly chance that a household that left comes back, by months since it left and its early reading."""
    hh = pn["household"] if o["link"] == ("fingerprint", "address") else link(pn, o["link"])
    order = np.lexsort((pn["start"], hh))
    nxt = np.full(pn["n"], -1)
    for a, b in zip(order[:-1], order[1:]):
        if hh[a] == hh[b]:
            nxt[a] = b
    use_px = o.get("ret_proxy", True)
    ok = (pn["end"] >= 0) & (pn["end"] < P.CUT - 1) & ~pn["withdrawn"]
    if use_px:
        ok &= ~np.isnan(pn["proxy"])
    else:
        ok &= pn["start"] >= 0
    idx = np.where(ok)[0]
    rows_s, rows_p, rows_y = [], [], []
    newacc, n_ret = 0, 0
    for i in idx:
        e = pn["end"][i]
        nx = nxt[i]
        back = nx >= 0 and pn["start"][nx] > e
        smax = (pn["start"][nx] - e) if back else (P.CUT - e)
        s = np.arange(1, smax + 1)
        y = np.zeros(len(s))
        if back:
            y[-1] = 1
            n_ret += 1
            newacc += int(pn["customer"][nx] != pn["customer"][i])
        rows_s.append(s)
        rows_p.append(np.full(len(s), pn["proxy"][i] if use_px else 0.0))
        rows_y.append(y)
    s = np.concatenate(rows_s).astype(float)
    px = np.concatenate(rows_p)
    y = np.concatenate(rows_y)
    X = np.column_stack([np.ones(len(s)), px, s]) if use_px else np.column_stack([np.ones(len(s)), s])
    b = fit_logit(X, y)
    return {"b": b, "newacc": newacc / max(n_ret, 1), "o": o, "px": use_px}


def ret_hazard(rmod, s, proxy):
    s = np.asarray(s, float)
    if not rmod["px"]:
        return sim.sig(rmod["b"][0] + rmod["b"][1] * s) * np.ones(np.shape(proxy))
    return sim.sig(rmod["b"][0] + rmod["b"][1] * proxy + rmod["b"][2] * s)


def link(pn, use):
    import panel
    if use == ():
        return pn["customer"].copy()
    return panel.households(pn["customer"], pn["fingerprint"], pn["address"], use=use)


# ---------------------------------------------------------------- the value of a start, by survival arithmetic

def net_factor(route, paid_idx):
    """Net revenue per gross euro in a subscription's paid month number paid_idx (1-based): VAT out, then the
    store's fee (Apple 30 per cent for the first 12 paid months and 15 after, Google 15)."""
    f = np.full(np.shape(paid_idx), 1.0 / (1 + P.VAT))
    for r, (f1, f2) in P.STORE_FEE.items():
        sel = route == sim.R_IDX[r]
        f = np.where(sel, f * (1 - np.where(paid_idx <= 12, f1, f2)), f)
    return f


def spell(M, ch, ti, offer, m_start, proxy, route, H, rise_on=True, k0=None, alive0=None, ten0=None,
          no_rise_price=False):
    """Expected net revenue by month, the chance of leaving at each month's end and the chance of paying each
    month, for subscriptions starting at m_start (one per row), over H months. k0 starts the arithmetic part-way
    through a subscription (the months already billed), ten0 adds months paid before the record began (the
    subscriptions running in January 2023), no_rise_price keeps the full price at its April 2025 level."""
    n = len(ch)
    L = np.where(offer >= 0, sim.intro_months(np.maximum(offer, 0)), 0)
    ip = np.where(offer >= 0, sim.intro_price(np.maximum(offer, 0), ti, m_start), 0.0)
    alive = np.ones(n) if alive0 is None else alive0.astype(float).copy()
    k_first = np.zeros(n, int) if k0 is None else k0.astype(int)
    t0 = np.zeros(n, int) if ten0 is None else ten0.astype(int)
    rev = np.zeros((n, H))
    leave = np.zeros((n, H))
    pay = np.zeros((n, H))
    inv = np.array([M["inv"][int(r)] for r in route])
    paid = np.where(k_first > 0, np.minimum(k_first, L) * (ip > 0) + np.maximum(k_first - L, 0), 0).astype(float)
    paid = paid + t0
    pending = np.zeros((n, H + 3))
    rise_done = np.zeros(n, bool)
    for h in range(H):
        k = k_first + h
        m = m_start + k
        mp = np.minimum(m, P.RISE_2027 - 1) if no_rise_price else m
        intro = k < L
        step = (k == L) & (offer >= 0)
        if step.any():
            sel = np.where(step)[0]
            p = np.zeros(n)
            p[sel] = su_prob(M["su"], ch[sel], ti[sel], np.maximum(offer[sel], 0), m_start[sel], mp[sel], proxy[sel])
            out = alive * p
            if h > 0:
                leave[:, h - 1] += out
            alive = alive - out
        if rise_on and not no_rise_price:
            at = (m == P.RISE_2027 - 1) & (k >= L) & ~rise_done
            if at.any():
                x = rise_extra(M["rise"], k + 1 + t0) * alive
                for t_off, share in enumerate(P.RISE_TIMING):
                    pending[:, h + t_off] += np.where(at, x * share, 0.0)
                rise_done |= at
        price = np.where(intro, ip, sim.full_price(ti, mp))
        f = alive * inv * (price > 0) * (k >= 1)
        alive = alive - f
        if h > 0:
            leave[:, h - 1] += f
        paid = paid + (price > 0)
        pay[:, h] = alive
        rev[:, h] = alive * price * net_factor(route, paid)
        r_go = np.minimum(pending[:, h], alive)
        alive = alive - r_go
        leave[:, h] += r_go
        hz = np.where(intro, M["intro"], 0.0)
        full = ~intro
        if full.any():
            j = (k - L + 1 + t0)[full]
            if "settled" in M and M["settled"] is not None:
                hz[full] = settled_or_young(M, ch[full], j, proxy[full], m[full], ti[full])
            else:
                hz[full] = hazard(M["hz"], ch[full], j, proxy[full], m[full], ti[full])
        c = alive * hz
        alive = alive - c
        leave[:, h] += c
    return rev, leave, pay


def return_profiles(M, title, proxies, routes, m_first, m_last):
    """Expected net revenue by month of a return spell through the paywall starting at each month m_first..m_last,
    on a new account (at that month's paywall offer) or the old one (the full price), for each proxy row."""
    K = len(proxies)
    out = {}
    ti = np.full(K, sim.T_IDX[title])
    ch = np.full(K, sim.C_IDX["DIR"])
    for m in range(m_first, m_last + 1):
        H = m_last - m + 1
        off_new = np.full(K, sim.O_IDX[sim.dir_offer(m)])
        rn, _, _ = spell(M, ch, ti, off_new, np.full(K, m), proxies, routes, H, rise_on=False)
        ro, _, _ = spell(M, ch, ti, np.full(K, -1), np.full(K, m), proxies, routes, H, rise_on=False)
        q = M["newacc"]
        out[m] = np.cumsum(q * rn + (1 - q) * ro, axis=1)
    return out


def with_returns(M, leave, ms, proxies, prof, m_until):
    """Add the first return's expected revenue inside the window to each row's value."""
    n, H = leave.shape
    val = np.zeros(n)
    for e in range(H):
        pe = leave[:, e]
        if pe.max() <= 0:
            continue
        surv = np.ones(n)
        for s in range(1, H):
            m_ret = ms + e + s
            if np.all(m_ret > m_until):
                break
            r = ret_hazard(M["ret"], s, proxies) * surv
            surv = surv - r
            for mr in np.unique(m_ret[m_ret <= m_until]):
                sel = m_ret == mr
                cum = prof[int(mr)]
                upto = (m_until[sel] - mr).astype(int)
                val[sel] += pe[sel] * r[sel] * cum[np.where(sel)[0], upto]
    return val


def line_value(M, line, starts_by_month, offer_code, proxies, routes, o):
    """Expected 36-month net revenue per start of a 2027 line, over the plan's start months and the line's starts
    of the twelve months to the cut (their early reading and payment routes)."""
    c, t = line
    K = len(proxies)
    ti = np.full(K, sim.T_IDX[t])
    ch = np.full(K, sim.C_IDX[c])
    off = np.full(K, sim.O_IDX[offer_code])
    prof = None
    if o["returns"]:
        prof = return_profiles(M, t, proxies, routes, P.PLAN0 + 1, P.PLAN1 + P.HORIZON - 1)
    tot_w, tot_v = 0.0, 0.0
    for mi, w in enumerate(starts_by_month):
        if w <= 0:
            continue
        m0 = P.PLAN0 + mi
        ms = np.full(K, m0)
        rev, leave, _ = spell(M, ch, ti, off, ms, proxies, routes, P.HORIZON)
        v = rev.sum(axis=1)
        if o["returns"]:
            v = v + with_returns(M, leave, ms, proxies, prof, ms + P.HORIZON - 1)
        tot_v += w * v.mean()
        tot_w += w
    return tot_v / tot_w


def fit_all(pn, o):
    M = {"su": fit_su(pn, o), "hz": fit_hazard(pn, o), "inv": invol_rates(pn), "intro": intro_rate(pn), "o": o}
    M["rise"] = rise_model(pn, M["hz"], o)
    if o["returns"]:
        r = fit_returns(pn, o)
        M["ret"] = r
        M["newacc"] = r["newacc"]
    return M


# ---------------------------------------------------------------- subscriptions with no early reading

def fit_settled(pn, o):
    """Monthly cancelling on the full price for the subscriptions that started before the reading log (no early
    reading): by months on the full price in bands, from the months since November 2024 outside the April 2025
    rise's window."""
    bands = [(1, 23), (24, 35), (36, 59), (60, 95), (96, 10 ** 6)]
    sel = np.isnan(pn["proxy"]) & ~pn["withdrawn"] & (pn["stepup"] <= P.CUT) & np.isin(pn["kind"], ("base", "new",
                                                                                                    "return"))
    rate = {}
    for lo, hi in bands:
        ev, at = 0, 0
        for m in range(22, P.CUT):
            if 26 <= m <= 28:
                continue
            j = m - pn["stepup"] + 1 + pn["tenure0"]
            a = sel & (pn["stepup"] <= m) & (pn["last"] >= m) & (j >= lo) & (j <= hi)
            at += a.sum()
            ev += (a & (pn["end"] == m) & (pn["reason"] == "CANCELLED")).sum()
        rate[(lo, hi)] = ev / max(at, 1)
    return rate


def settled_or_young(M, ch, j, proxy, m, ti):
    out = np.zeros(len(j))
    young = ~np.isnan(proxy)
    if young.any():
        out[young] = hazard(M["hz"], ch[young], j[young], proxy[young], m[young], ti[young])
    old = ~young
    if old.any():
        jj = j[old]
        r = np.zeros(len(jj))
        for (lo, hi), v in M["settled"].items():
            r[(jj >= lo) & (jj <= hi)] = v
        out[old] = r
    return out
