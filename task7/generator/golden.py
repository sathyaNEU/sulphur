"""task7 architecture 11: the estimators, from the pack alone (verify.Pack).

A summer like 2026 is July and August 2026 as metered, with each charger enrolled on 1 November 2026 charged as an option
would charge its 2026 sessions (Board Policy EV-4). The golden replays every transformer night by night at the quarter-hour:
its homes' hourly reads less the enrolled chargers' own charging, lifted to the quarter-hour by the monitored transformers'
highest quarter-hour above each hour, plus the enrolled chargers' sessions as each option would run them: the members' own
schedules (each charger's own-schedule history, the managed quarter's read from summer 2024, else what the member said at
enrolment), Quillpoint Stagger's random start (each transformer at its chance of being over, over many draws) and Quillpoint
Sequence (one charger at a time in ready-by order, a late charger alongside). The hurried routes are coded beside it."""
import datetime as dt
from collections import Counter, defaultdict

import numpy as np

import verify as V

Q = V.Q
ND = V.NDAY
L = (ND + 1) * Q
WIN = ND * Q
OFF = 23 * 4
LIMIT, PF = 1.20, 0.95
FEE = {"own": 0.0, "stagger": 18.0, "sequence": 40.0}
COST = {25.0: 10800, 37.5: 11400, 50.0: 18200, 75.0: 21500, 100.0: 26900}
OPTIONS = ("own", "stagger", "sequence")
EVE0 = dt.date(2026, 6, 30)        # the first evening whose charging reaches into July
K_RANDOM = 400
DECLARED = {"Charger timer 23:00": "t2300", "Charger timer 23:30": "t2330", "Charger timer 00:00": "t0000",
            "Car's departure schedule": "ready", "When I plug in": "now"}


def qofday(t):
    return t.hour * 4 + t.minute // 15


def evening_q(night, t):
    """quarter index of time t counted from 00:00 on the evening's own date"""
    return (t.date() - night).days * Q + qofday(t)


def place(series, a, e, p):
    qn = e / p * 4.0
    k = a
    while qn > 1e-9 and k < len(series):
        if k >= 0:
            series[k] += p * min(1.0, qn)
        qn -= 1.0
        k += 1


def actual_quarters(P, k, n=WIN):
    """a charger's metered charging in July and August 2026 at the quarter-hour, from its session times"""
    s15 = np.zeros(n)
    t0 = dt.datetime(2026, 7, 1, tzinfo=V.MDT)
    for s in P.sess.get(k, []):
        a = (s["start"] - t0).total_seconds() / 900.0
        b = (s["end"] - t0).total_seconds() / 900.0
        if b <= 0 or a >= n:
            continue
        p = s["kwh"] / ((b - a) / 4.0)
        for q in range(max(0, int(np.floor(a))), min(n, int(np.ceil(b)))):
            ov = min(b, q + 1) - max(a, q)
            if ov > 0:
                s15[q] += p * ov
    return s15


def own_setting(P, k, mode="history"):
    """a charger's own setting: read from its own-schedule sessions (2026 for the own three-quarters, summer 2024 for the
    managed quarter), or what the member said at enrolment where it has none"""
    cache = P.__dict__.setdefault("_own_cache", {})
    if (k, mode) not in cache:
        cache[(k, mode)] = _own_setting(P, k, mode)
    return cache[(k, mode)]


def _own_setting(P, k, mode):
    decl = DECLARED.get(P.ch[k].get("declared"))
    if mode == "declared":
        return decl
    half = P.half.get(k)
    cand = [s for s in P.sess.get(k, []) if (s["night"].year == 2026 if half == "own" else s["night"] < dt.date(2025, 5, 12))]
    votes = Counter()
    for s in cand:
        if s["mode"] == "IMMEDIATE":
            votes["now"] += 1
        elif s["mode"] == "VEHICLE_SCHEDULE":
            votes["ready"] += 1
        elif s["mode"] == "CHARGER_SCHEDULE":
            votes[{"23:00": "t2300", "23:30": "t2330", "00:00": "t0000"}.get(s["start"].strftime("%H:%M"), "t2300")] += 1
    return votes.most_common(1)[0][0] if votes else decl


def own_start(setting, plug, dep, e, p):
    q = int(np.ceil(e / p * 4))
    if setting == "t2300":
        return max(plug, OFF)
    if setting == "t2330":
        return max(plug, OFF + 2)
    if setting == "t0000":
        return max(plug, Q)
    if setting == "ready":
        return max(plug, dep - q - 2)
    return plug


# ---- one pass over the pack: every transformer's base and sessions --------------------------------------------------------
class Book:
    def __init__(self, P):
        self.P = P
        self.tx_ch = defaultdict(list)
        for k in P.enrolled:
            self.tx_ch[P.sp_tx[P.ch[k]["sp"]]].append(k)
        self.rate_ch = defaultdict(list)
        for k, c in P.ch.items():
            self.rate_ch[P.sp_tx[c["sp"]]].append(k)
        self.ev15 = {k: actual_quarters(P, k) for k in P.ch}
        self.sess = {k: self._sessions(k) for k in P.enrolled}
        self.bh = {t: self._base_hourly(t) for t in self.tx_ch}
        self.bh_mon = {t: self._base_hourly(t) for t in P.mon}
        self.obs = {t: self._observed(t) for t in self.tx_ch}

    def _sessions(self, k):
        P = self.P
        out = []
        for s in P.sess.get(k, []):
            if not (EVE0 <= s["night"] <= dt.date(2026, 8, 31)):
                continue
            o = (s["night"] - V.JUL1).days * Q
            pq = evening_q(s["night"], s["plug"]) + (1 if (s["plug"].minute % 15 or s["plug"].second) else 0)
            out.append((o, pq, evening_q(s["night"], s["unplug"]), s["kwh"], P.ch[k]["kw"], s))
        return out

    def _base_hourly(self, t):
        """the transformer's homes as metered, less the charging of the chargers enrolled on 1 November 2026"""
        P = self.P
        b = np.zeros(ND * 24)
        for sp in P.tx_sps[t]:
            if sp in P.ami:
                b += P.ami[sp]
        for k in self.tx_ch.get(t, []):
            b -= self.ev15[k].reshape(-1, 4).mean(1)
        return b

    def _observed(self, t):
        b = np.zeros(ND * 24)
        for sp in self.P.tx_sps[t]:
            if sp in self.P.ami:
                b += self.P.ami[sp]
        return b

    def homes(self, t):
        return len(self.P.tx_sps[t])


def hourly_excess(B):
    """the monitored transformers' highest quarter-hour above its hour, by hour of day, per square root of homes"""
    P = B.P
    rec = defaultdict(list)
    for t, mon in P.mon.items():
        bh = B.bh_mon[t]
        ev = np.zeros(WIN)
        for k in B.tx_ch.get(t, []):
            ev += B.ev15[k]
        tot_m = np.nanmean(mon.reshape(-1, 4), axis=1)
        tot_h = bh + ev.reshape(-1, 4).mean(1)
        ok = ~np.isnan(tot_m)
        ratio = float(np.sum(tot_m[ok]) / np.sum(tot_h[ok]))           # the monitor reads its own losses too
        base = mon / ratio - ev
        m = base.reshape(-1, 4)
        good = ~np.isnan(m).any(axis=1)
        excess = (np.nanmax(m, axis=1) - np.nanmean(m, axis=1))[good]
        hours = (np.arange(ND * 24) % 24)[good]
        n = max(B.homes(t), 1)
        for h in range(24):
            rec[h].append(np.mean(excess[hours == h]) / np.sqrt(n))
    return np.array([np.mean(rec[h]) for h in range(24)])


def peak_lift(B, K=60):
    """rival: each option's summer peak on a monitored transformer's quarter-hour base less the same on its hourly base,
    fitted to the square root of its homes"""
    P = B.P
    rec = {o: [] for o in OPTIONS}
    for t, mon in P.mon.items():
        bh = B.bh_mon[t]
        ev = np.zeros(WIN)
        for k in B.tx_ch.get(t, []):
            ev += B.ev15[k]
        tot_m = np.nanmean(mon.reshape(-1, 4), axis=1)
        tot_h = bh + ev.reshape(-1, 4).mean(1)
        ok = ~np.isnan(tot_m)
        ratio = float(np.sum(tot_m[ok]) / np.sum(tot_h[ok]))
        hb = np.repeat(bh, 4)
        b15 = np.where(np.isnan(mon), hb * 1.0, mon / ratio - ev)
        f15 = np.concatenate([b15, np.repeat(b15[-32:].mean(), Q)])
        fh = np.concatenate([hb, np.repeat(hb[-32:].mean(), Q)])
        sess = [s for k in B.tx_ch.get(t, []) for s in B.sess[k]]
        sets = [own_setting(P, k) for k in B.tx_ch.get(t, []) for _ in B.sess[k]]
        n = B.homes(t)
        rec["own"].append((n, season_max(f15, own_blocks(sess, sets)) - season_max(fh, own_blocks(sess, sets))))
        rec["sequence"].append((n, season_max(f15, sequence_blocks(sess)) - season_max(fh, sequence_blocks(sess))))
        _, a = random_peaks(f15, sess, np.random.default_rng(1), K)
        _, b = random_peaks(fh, sess, np.random.default_rng(1), K)
        rec["stagger"].append((n, float(np.mean(a - b))))
    fit = {}
    for o, v in rec.items():
        x = np.sqrt(np.array([a for a, _ in v], dtype=float))
        y = np.array([b for _, b in v])
        fit[o] = float((x * y).sum() / (x * x).sum())
    return fit


def base15(bh, n_homes, lift):
    up = np.tile(lift, ND) * np.sqrt(max(n_homes, 1))
    s = np.repeat(bh + up, 4)
    return np.concatenate([s, np.repeat(s[-32:].mean(), Q)])        # the night after 31 August is outside the window


# ---- the three options ---------------------------------------------------------------------------------------------------------
def season_max(base, blocks):
    s = base.copy()
    for (a, e, p) in blocks:
        place(s, a, e, p)
    return s[:WIN].max()


def own_blocks(sess, settings):
    return [(o + own_start(st, plug, dep, e, p), e, p) for (o, plug, dep, e, p, _), st in zip(sess, settings)]


def sequence_blocks(sess, perfect=False):
    bynight = defaultdict(list)
    for i, s in enumerate(sess):
        bynight[s[0]].append(i)
    out = []
    for o, idx in bynight.items():
        free = OFF
        for i in sorted(idx, key=lambda i: (sess[i][2], sess[i][1])):
            _, plug, dep, e, p, _ = sess[i]
            q = int(np.ceil(e / p * 4))
            lo = max(plug, OFF)
            st = max(free, lo)
            if not perfect and st + q > dep:
                st = max(lo, dep - q)
            out.append((o + st, e, p))
            free = max(free, st + q)
    return out


def random_peaks(base, sess, rng, K=K_RANDOM):
    """the summer peak under Stagger over K draws of every session's random start"""
    if not sess:
        return None, np.full(K, base[:WIN].max())
    S = len(sess)
    lo = np.array([max(s[1], OFF) for s in sess])
    qn = np.array([s[3] / s[4] * 4 for s in sess])
    qi = np.ceil(qn).astype(int)
    hi = np.maximum(lo, np.array([s[2] for s in sess]) - qi)
    st = lo[None, :] + np.floor(rng.random((K, S)) * (hi - lo + 1)[None, :]).astype(int)
    o = np.array([s[0] for s in sess]) + 2 * Q
    p = np.array([s[4] for s in sess])
    nf = np.floor(qn).astype(int)
    fr = qn - nf
    diff = np.zeros((K, L + 2 * Q + 64))
    a = o[None, :] + st
    rows = np.repeat(np.arange(K), S)
    np.add.at(diff, (rows, a.ravel()), np.tile(p, K))
    np.add.at(diff, (rows, (a + nf[None, :]).ravel()), np.tile(p * (fr - 1), K))
    np.add.at(diff, (rows, (a + nf[None, :] + 1).ravel()), -np.tile(p * fr, K))
    ev = np.cumsum(diff, axis=1)[:, 2 * Q:2 * Q + L]
    return None, (base[None, :] + ev)[:, :WIN].max(axis=1)


def managed_profile(B):
    """the managed quarter's mean charging per enrolled charger per night, by quarter from the evening's 00:00"""
    P = B.P
    prof = np.zeros(2 * Q + 16)
    n = 0
    for k in P.enrolled:
        if P.half.get(k) != "managed":
            continue
        n += 1
        for (o, plug, dep, e, p, s) in B.sess[k]:
            if s["night"] < V.JUL1:
                continue
            place(prof, evening_q(s["night"], s["start"]), e, p)
    return prof / max(n, 1) / ND


# ---- the replay -----------------------------------------------------------------------------------------------------------------
def replay(B, seed=7, lift="excess", own="history", stagger="draws", sequence="filed", K=K_RANDOM, tables=None):
    """every transformer serving an enrolled charger, each option's summer peak and its chance of being over its limit"""
    P = B.P
    rng = np.random.default_rng(seed)
    tables = tables or {}
    exc = tables.get("excess") if lift in ("excess",) else None
    if lift == "excess" and exc is None:
        exc = hourly_excess(B)
    pl = tables.get("peak") if lift == "peak" else None
    if lift == "peak" and pl is None:
        pl = peak_lift(B)
    mprof = managed_profile(B) if stagger == "profile" else None
    out = {}
    for t in sorted(B.tx_ch):
        kva = P.kva[t]
        limit = LIMIT * kva * PF
        n_h = B.homes(t)
        b = base15(B.bh[t], n_h, exc if lift == "excess" else np.zeros(24))
        up = {o: (pl[o] * np.sqrt(n_h) if lift == "peak" else 0.0) for o in OPTIONS}
        sess = [s for k in B.tx_ch[t] for s in B.sess[k]]
        sets = [own_setting(P, k, own if own != "observed" else "history") for k in B.tx_ch[t] for _ in B.sess[k]]
        r = dict(kva=kva, limit=limit, chargers=len(B.tx_ch[t]), homes=n_h, cost=COST.get(kva, 0), area=P.area.get(t, ""))
        if own == "observed":                     # the 2026 loads as metered, a quarter of the chargers managed
            pk = B.obs[t].max()
        else:
            pk = season_max(b, own_blocks(sess, sets)) + up["own"]
        r["own_peak"], r["own_p"] = float(pk), float(pk > limit)
        if stagger == "draws":
            _, pks = random_peaks(b, sess, rng, K)
            pks = pks + up["stagger"]
            r["stagger_peak"], r["stagger_p"] = float(np.mean(pks)), float((pks > limit).mean())
        else:                                    # the managed quarter's average night times the transformer's chargers
            s = b.copy()
            for d in range(-1, ND):
                lo = d * Q
                seg = mprof * len(B.tx_ch[t])
                a0, a1 = max(0, lo), min(L, lo + len(seg))
                s[a0:a1] += seg[a0 - lo:a1 - lo]
            pk = s[:WIN].max() + up["stagger"]
            r["stagger_peak"], r["stagger_p"] = float(pk), float(pk > limit)
        if sequence == "as_stagger":
            r["sequence_peak"], r["sequence_p"] = r["stagger_peak"], r["stagger_p"]
        else:
            pk = season_max(b, sequence_blocks(sess, perfect=(sequence == "perfect"))) + up["sequence"]
            r["sequence_peak"], r["sequence_p"] = float(pk), float(pk > limit)
        out[t] = r
    return out


def totals(out, n_chargers):
    res = {}
    for o in OPTIONS:
        over = sum(r[o + "_p"] for r in out.values())
        rep = sum(r[o + "_p"] * r["cost"] for r in out.values())
        fee = FEE[o] * n_chargers
        res[o] = dict(over=over, replace=rep, fee=fee, total=fee + rep)
    res["call"] = min(OPTIONS, key=lambda o: res[o]["total"])
    return res


def pilot_effect(B):
    """kW per enrolled charger in the 23:00 to 23:15 quarter, July and August 2026, managed quarter less own three-quarters"""
    P = B.P
    tot = {"managed": [], "own": []}
    for k, c in P.ch.items():
        if c["enrolled"] > V.JUL1 or (c["closed"] is not None and c["closed"] <= dt.date(2026, 9, 1)):
            continue
        h = P.half.get(k)
        if h is None:
            continue
        tot[h].append(B.ev15[k].reshape(ND, Q)[:, OFF].mean())
    return dict(effect=float(np.mean(tot["managed"]) - np.mean(tot["own"])), n_managed=len(tot["managed"]),
                n_own=len(tot["own"]), own=float(np.mean(tot["own"])), managed=float(np.mean(tot["managed"])))


def flip_fee(res, n_chargers):
    """the Sequence fee per charger-year at which Stagger would cost the same"""
    return (res["stagger"]["total"] - res["sequence"]["replace"]) / n_chargers


ROUTES = {
    # the careful but hurried pass: the pilot's per-charger effect as an average night, coordination as one charger at a
    # time, own schedules as metered in 2026, peaks off the hourly reads
    "careful": dict(lift="none", own="observed", stagger="profile", sequence="perfect"),
    "quick": dict(lift="none", own="observed", stagger="profile", sequence="as_stagger"),
    "no_J1": dict(stagger="profile"),
    "no_J3_perfect": dict(sequence="perfect"),
    "no_J3_as_stagger": dict(sequence="as_stagger"),
    "no_own": dict(own="observed"),
    "no_lift": dict(lift="none"),
}
RIVALS = {
    "peak_lift": dict(lift="peak"),
    "no_lift": dict(lift="none"),
    "declared_own": dict(own="declared"),
    "seed_11": dict(seed=11),
    "seed_23": dict(seed=23),
}


def solve(P):
    B = Book(P)
    tables = {"excess": hourly_excess(B)}
    g = replay(B, tables=tables)
    n = len(P.enrolled)
    res = totals(g, n)
    return dict(B=B, tables=tables, out=g, res=res, n=n, pilot=pilot_effect(B), flip=flip_fee(res, n))
