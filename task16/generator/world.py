"""Quellstein's process, simulated: parcels run on time or late by depot and day, recipients ask (or not) by how the
parcel ran, an unhelped customer comes back through whichever channel is open, the telephone line stops asking for the
tracking number when its queue is long, and a written case stays open for as long as its queue is behind.

Returns the raw process record (with the truth the files never hold) for pack.py to export and checks.py to compare.
Internal time is local wall-clock hours since Monday 3 August 2026, 00:00.
"""
import math

import numpy as np

import params as P

EXT_H = P.DAYS * 24.0
NC = len(P.CLASSES)
NF = len(P.FAM)
FI = {f: i for i, f in enumerate(P.FAM)}
CI = {c: i for i, c in enumerate(P.CLASSES)}
SLOT0, NSLOT = 7 * 4, 13 * 4          # telephone open 07:00 to 20:00, quarter-hours


def _sig(x):
    return 1.0 / (1.0 + math.exp(-x))


def network(rng):
    """Parcels due by day x depot x class, and the daily multipliers behind them."""
    nd = len(P.DEPOTS)
    N = np.zeros((P.DAYS, nd, NC), dtype=np.int64)
    dsum = sum(P.DOW)
    for t in range(P.DAYS):
        dow = t % 7
        for i, (code, _, wk) in enumerate(P.DEPOTS):
            if P.DOW[dow] == 0:
                continue
            n = wk * 1000 * P.DOW[dow] / dsum * (1 + 0.004 * (t // 7)) * math.exp(rng.normal(0, 0.06))
            m1 = math.exp(rng.normal(0, 0.22)); m2 = math.exp(rng.normal(0, 0.28)); m3 = math.exp(rng.normal(0, 0.20))
            if rng.random() < 0.02:                       # an ordinary bad day at one depot
                m1 *= 2.2; m2 *= 2.6
            if code in P.STORM and 14 <= t <= 21:          # the August storms and flooding, and their tail
                g = {14: 0.5, 15: 0.9, 16: 1.0, 17: 1.0, 18: 0.8, 19: 0.55, 20: 0.0, 21: 0.3}[t]
                m1 *= 1 + 3.0 * g; m2 *= 1 + 6.5 * g
            if code in P.HUB and t >= 62:                  # the move onto Hub Traunfeld, easing unevenly
                g = 0.25 if t == 62 else math.exp(-(t - 63) / 8.5) * (1.25 if t in (65, 66, 72) else 1.0)
                m1 *= 1 + 1.0 * g; m2 *= 1 + 1.6 * g; m3 *= 1 + 0.3 * g
            s1 = P.BASE_SHARE["L1"] * m1; s2 = P.BASE_SHARE["L2"] * m2
            s3 = P.BASE_SHARE["EX"] * m3 * P.EX_TILT.get(code, 1.0)
            n = int(round(n))
            k = rng.multinomial(n, [1 - s1 - s2 - s3, s1, s2, s3])
            N[t, i] = k
    return N


def _tod(rng, ch):
    """Hour of day a customer starts a contact."""
    if ch in ("A", "W"):
        h = rng.choice(24, p=_TOD_ANY) + rng.random()
    else:
        h = rng.choice(24, p=_TOD_OPEN) + rng.random()
    return h


_w = np.array([.3, .2, .1, .1, .1, .3, .8, 2.2, 4.2, 5.6, 6.0, 5.6, 4.6, 4.4, 4.2, 4.0, 4.2, 5.0, 5.6, 5.2, 4.2, 2.6, 1.4, .7])
_TOD_ANY = _w / _w.sum()
_o = np.array([0, 0, 0, 0, 0, 0, 0, 3.6, 5.6, 6.6, 6.8, 6.2, 5.0, 4.8, 4.6, 4.4, 4.6, 4.8, 4.2, 3.0, 0, 0, 0, 0])
_TOD_OPEN = _o / _o.sum()


def _open_time(ch, t, rng):
    """Move a start time into the channel's opening hours (telephone 07 to 20, live chat 08 to 20, Monday to Saturday)."""
    if ch in ("A", "W"):
        return t
    lo = 7.0 if ch == "P" else 8.0
    for _ in range(10):
        day = int(t // 24); h = t - day * 24
        if day % 7 == 6 or h >= 20.0:
            t = (day + 1) * 24 + lo + rng.exponential(0.7)
        elif h < lo:
            t = day * 24 + lo + rng.exponential(0.7)
        else:
            return t
    return t


def simulate():
    rng = np.random.default_rng(P.SEED)
    N = network(rng)
    nd = len(P.DEPOTS)
    u_day = rng.normal(0, P.DAY_SD, P.DAYS + 30)
    u_fd = rng.normal(0, P.FAMDAY_SD, (NF, P.DAYS + 30))
    fam_p = {c: np.array(P.FAM_GIVEN[c]) / sum(P.FAM_GIVEN[c]) for c in P.CLASSES}
    cons = []        # depot index, due day, class index, delivered day (or -1), exception code, alerted
    contacts = []    # consignment, order, channel, family index, start h, end h, handover flag
    for t in range(P.DAYS):
        for i, (code, _, _) in enumerate(P.DEPOTS):
            for c in P.CLASSES:
                ci = CI[c]
                alerted = code in P.PILOT and t >= P.ALERT_DAY and c in ("L1", "L2")
                p = P.CONTACT[c] * ((1 - P.ALERT_CUT) if alerted else 1.0)
                n = rng.binomial(N[t, i, ci], p)
                for _ in range(n):
                    rng_c = np.random.default_rng((P.SEED, 1, len(cons)))
                    if c == "ON":
                        deliv = t - 1 if rng_c.random() < 0.08 else t
                        first_day = t - 1 if rng_c.random() < 0.32 else t
                    elif c == "L1":
                        deliv = t + 1
                        first_day = t if rng_c.random() < 0.3 else t + 1
                    elif c == "L2":
                        deliv = t + 2 + min(int(rng_c.geometric(0.45)) - 1, 9)
                        first_day = t + 1 + min(int(rng_c.geometric(0.55)) - 1, 3)
                    else:
                        deliv = -1 if rng_c.random() < 0.06 else t + 3 + int(rng_c.integers(0, 12))
                        first_day = t + int(rng_c.integers(0, 4))
                    exc = "" if c != "EX" else str(rng_c.choice(["CUSTOMS_HOLD", "DAMAGED", "ADDRESS_QUERY", "REFUSED", "TRACE_OPEN"],
                                                                    p=[.34, .22, .22, .08, .14]))
                    idx = len(cons)
                    cons.append((i, t, ci, deliv, exc, alerted))
                    fam = int(rng_c.choice(NF, p=fam_p[c]))
                    f0 = P.FAM[fam]
                    ch = str(rng_c.choice(P.CH, p=P.FIRST_CH.get(f0, P.FIRST_CH["*"])))
                    tt = max(first_day, 0) * 24 + _tod(rng_c, ch)
                    k = 0
                    while k < 6:
                        start = _open_time(ch, tt, rng_c)
                        if start >= EXT_H:
                            break
                        dur = {"A": rng_c.gamma(3.0, 1.4) / 60, "C": rng_c.gamma(4.0, 3.0) / 60, "P": rng_c.gamma(3.5, 1.6) / 60,
                               "W": 0.0}[ch]
                        end = start + dur
                        day = int(start // 24)
                        f = P.FAM[fam]
                        if ch == "A":
                            a = P.A_ON[f]
                            if c != "ON":
                                sh = P.CLASS_SHIFT[c]; a += sh.get(f, sh["*"])
                            if start < P.V3_DAY * 24:
                                a += P.V2_SHIFT[f]
                            a += u_day[day] + u_fd[fam, day] - (0.45 if k > 0 else 0.0)
                            more = 1 - _sig(a)
                        else:
                            more = P.HUMAN_MORE[ch] * {"ON": 1.0, "L1": 1.15, "L2": 1.5, "EX": 1.3}[c]
                        go = rng_c.random() < more
                        hand = False
                        if go:
                            nxt = str(rng_c.choice(P.CH, p=P.NEXT_AFTER_A.get(f, P.NEXT_AFTER_A["*"]) if ch == "A" else P.NEXT_AFTER_H[ch]))
                            h_end = end - int(end // 24) * 24
                            if ch == "A" and nxt == "C" and rng_c.random() < P.HANDOVER and int(end // 24) % 7 != 6 and 8.0 <= h_end < 19.9:
                                hand = True
                                delay = rng_c.uniform(8, 100) / 3600
                            else:
                                delay = 0.2 + rng_c.lognormal(math.log(14.0), 1.15)
                        contacts.append((idx, k, ch, fam, start, end, hand))
                        if not go:
                            break
                        tt = end + delay
                        if rng_c.random() < 0.10:
                            fam = int(rng_c.choice(NF, p=fam_p[c]))
                        ch = nxt
                        k += 1
    return {"N": N, "cons": cons, "contacts": contacts, "rng": rng}


def telephone(W):
    """The IVR and the queue: which calls carry a tracking number, each call's wait, and the advisers' tick."""
    rng = W["rng"]
    contacts = W["contacts"]
    calls = [j for j, r in enumerate(contacts) if r[2] == "P"]
    # other calls on the general menu option (no consignment): the line's ordinary noise
    extra = []
    rx = np.random.default_rng((P.SEED, 4))
    for t in range(P.DAYS):
        if t % 7 == 6:
            continue
        for _ in range(rx.poisson(150 if t % 7 < 5 else 70)):
            extra.append(t * 24 + rx.choice(24, p=_TOD_OPEN) + rx.random())
    arr = np.zeros((P.DAYS, NSLOT, len(P.QUEUES)))
    qi = {q: i for i, q in enumerate(P.QUEUES)}

    def slot(h):
        day = int(h // 24); s = int((h - day * 24) * 4) - SLOT0
        return day, min(max(s, 0), NSLOT - 1)
    cq = {}
    for j in calls:
        _, _, _, fam, start, _, _ = contacts[j]
        q = qi[P.QUEUE_OF[P.FAM[fam]]]
        d, s = slot(start); arr[d, s, q] += 1; cq[j] = (d, s, q)
    eq = []
    for h in extra:
        d, s = slot(h); arr[d, s, qi["GENERAL"]] += 1; eq.append((d, s, qi["GENERAL"]))
    # staffing follows the ordinary weeks' pattern by weekday and quarter-hour (the rota is set a month ahead)
    calm = [t for t in range(21, 56)]
    cap = np.zeros((7, NSLOT, len(P.QUEUES)))
    for dow in range(6):
        days = [t for t in calm if t % 7 == dow]
        cap[dow] = np.maximum(arr[days].mean(axis=0) * 1.02, 1.2)
    load = np.zeros_like(arr)
    for t in range(P.DAYS):
        if t % 7 == 6:
            continue
        a = arr[t]; c = cap[t % 7]
        for s in range(NSLOT):
            lo = max(0, s - 3)
            load[t, s] = a[lo:s + 1].sum(axis=0) / c[lo:s + 1].sum(axis=0)
    offered = load > P.BYPASS_AT * np.exp(np.random.default_rng((P.SEED, 3)).normal(0, 0.07, load.shape))
    rec = {}
    for j in calls:
        d, s, q = cq[j]
        ld = load[d, s, q]
        r = np.random.default_rng((P.SEED, 2, contacts[j][0], contacts[j][1]))
        wait = min(40.0 * math.exp(3.3 * (ld - 0.7)) * r.lognormal(0, 0.45), 1500.0)
        u1, u2 = r.random(), r.random()
        if offered[d, s, q] and u1 < P.BYPASS_TAKE:
            path = "BYPASS"
        elif u2 < P.KEY_RATE:
            path = "KEYED"
        else:
            path = "NO_ENTRY"
        rec[j] = (path, wait)
    other = []
    for h, (d, s, q) in zip(extra, eq):
        ld = load[d, s, q]
        wait = min(40.0 * math.exp(3.3 * (ld - 0.7)) * rx.lognormal(0, 0.45), 1500.0)
        path = "BYPASS" if (offered[d, s, q] and rx.random() < P.BYPASS_TAKE) else "NO_ENTRY"
        other.append((h, path, wait))
    W["phone"] = rec
    W["other_calls"] = other
    W["load"] = load
    return W


def truth(W):
    """What the files never hold whole: for every assistant conversation, whether anyone came back within seven days,
    through which channels; and each adviser contact's true previous contact."""
    contacts = W["contacts"]
    by = {}
    for j, r in enumerate(contacts):
        by.setdefault(r[0], []).append(j)
    follow = {}     # conversation index -> list of later contact indices within 168 h of its end
    prev = {}       # contact index -> channel of the latest earlier contact within 168 h, and whether an assistant one exists
    for idx, js in by.items():
        for a, j in enumerate(js):
            r = contacts[j]
            if r[2] == "A":
                follow[j] = [k for k in js[a + 1:] if contacts[k][4] <= r[5] + 168.0]
            pa = [k for k in js[:a] if contacts[j][4] <= contacts[k][5] + 168.0]
            prev[j] = (contacts[pa[-1]][2] if pa else "", any(contacts[k][2] == "A" for k in pa))
    W["follow"] = follow
    W["prev"] = prev
    return W


def cases(W):
    """Written cases: the customers' own (web form, e-mail) and those advisers open during a call or chat, each
    closed after a lag that grows when its queue is behind."""
    rng = W["rng"]
    contacts = W["contacts"]
    out = []        # contact index or -1, created h, origin, family index or -1, queue, closed h, consignment or -1

    def mult(t, g):
        d = t / 24.0
        m = 1.0 + 0.85 / (1.0 + math.exp(-(d - 66.0) / 2.6))
        if 16 <= d <= 27:
            m += 0.35 * math.exp(-(d - 16) / 5.0)
        return m * math.exp(g.normal(0, 0.10))
    for j, r in enumerate(contacts):
        idx, k, ch, fam, start, end, _ = r
        f = P.FAM[fam]
        g = np.random.default_rng((P.SEED, 5, idx, k))
        if ch == "W":
            q = P.CASE_QUEUE_OF[f]
            lag = P.CASE_LAG[q] * mult(start, g) * g.lognormal(0, P.CASE_SIGMA)
            out.append((j, start, "WEB_FORM" if g.random() < 0.7 else "EMAIL", fam, q, start + lag * 24, idx))
        elif ch in ("P", "C") and g.random() < 0.11:
            q = P.CASE_QUEUE_OF[f]
            lag = P.CASE_LAG[q] * mult(end, g) * g.lognormal(0, P.CASE_SIGMA)
            out.append((-1, end, "ADVISER", fam, q, end + lag * 24, idx))
    g = np.random.default_rng((P.SEED, 6))
    for t in range(P.DAYS):                         # written contacts about no consignment (compliments, complaints, general)
        for _ in range(g.poisson(26)):
            h = t * 24 + g.choice(24, p=_TOD_ANY) + g.random()
            lag = 2.5 * mult(h, g) * g.lognormal(0, P.CASE_SIGMA)
            out.append((-1, h, "WEB_FORM" if g.random() < 0.6 else "EMAIL", -1, "GENERAL", h + lag * 24, -1))
    out.sort(key=lambda x: x[1])
    W["cases"] = out
    return W


def build():
    W = simulate()
    W = telephone(W)
    W = truth(W)
    W = cases(W)
    return W
