"""The analysis, from the loaded pack alone: the linked record, the follow-ups it cannot see, the season's
conversations, each family's expected rate and its range. Every method choice is an option, so the golden, the hurried
routes and the rivals behind each band are the same code run with different settings.
"""
import numpy as np
import pandas as pd

import params as P

FAM = P.FAM
CLS = P.CLASSES
FI = {f: i for i, f in enumerate(FAM)}
CI = {c: i for i, c in enumerate(CLS)}
NF, NC = len(FAM), len(CLS)
LATE = np.array([0, 1, 1, 0], dtype=float)
W0, W1 = P.V3_DAY, P.ACHIEVED_END          # conversations that ended on these days are version 3 and seven days old
GOLD = dict(capture="state", written="backlog", transport="propensity", alerts="did", boot="day")


def prep(D):
    """Link every in-scope conversation to the later contacts on its consignment, once."""
    A = D["A"]; Pc = D["P"]; C = D["C"]; K = D["K"]
    S = {}
    # ---- capture of the tracking number on consignment-reason calls
    cq = Pc[Pc.fam != ""].copy()
    allc = Pc.copy()
    allc["slot"] = np.floor(allc.start * 4).astype(int)
    byp = set(zip(allc.slot[allc.ivr_path == "BYPASS"], allc.queue[allc.ivr_path == "BYPASS"]))
    cq["slot"] = np.floor(cq.start * 4).astype(int)
    cq["on"] = [(s, q) in byp for s, q in zip(cq.slot, cq.queue)]
    cq["day"] = (cq.start // 24).astype(int); cq["week"] = cq.day // 7; cq["hour"] = np.floor(cq.start).astype(int)
    cq["wband"] = np.minimum((cq.wait // 45).astype(int), 12)
    S["cq"] = cq
    # ---- events by tracking number
    ev = {}
    for ch, df, extra in (("A", A, None), ("C", C, None), ("P", cq[cq.keyed], None), ("W", K[K.customer], None)):
        for i, t, s in zip(df.index.values, df.trk.values, df.start.values):
            ev.setdefault(t, []).append((s, ch, i))
    for t in ev:
        ev[t].sort()
    n = len(A)
    na = np.zeros(n, int); nc = np.zeros(n, int); nw = np.zeros(n, int)
    calls = [()] * n; wcase = np.full(n, -1)
    last = {}                                   # event (channel, index) -> the latest conversation it follows
    ends = A.end.values; starts = A.start.values; trks = A.trk.values
    for i in range(n):
        e = ends[i]; lst = []
        for s, ch, j in ev.get(trks[i], ()):
            if ch == "A":
                if j != i and starts[j] > e and s <= e + 168.0:
                    na[i] += 1
                continue
            if s < e or s > e + 168.0:
                continue
            if ch == "C":
                nc[i] += 1
            elif ch == "P":
                lst.append(j)
            else:
                nw[i] += 1
                if wcase[i] < 0:
                    wcase[i] = j
            key = (ch, j)
            if key not in last or ends[last[key]] < e:
                last[key] = i
        calls[i] = tuple(lst)
    S.update(na=na, nc=nc, nw=nw, calls=calls, wcase=wcase, last=last)
    A = A.copy()
    A["day"] = (A.end // 24).astype(int)
    A["fi"] = A.fam.map(FI).astype(int)
    A["ci"] = A.cls.map(CI).fillna(-1).astype(int)
    S["A"] = A
    S["win"] = (A.v3 & (A.day >= W0) & (A.day < W1) & (A.ci >= 0)).values
    # ---- written cases: closed customer cases by queue and week raised, and the open ones in the last backlog count
    Kc = K[K.customer]
    S["closed_qw"] = Kc.groupby(["queue", "week"]).size().to_dict()
    S["closed_qd"] = Kc.groupby(["queue", "day"]).size().to_dict()
    b = D["backlog"]; snap = b.snap.max()
    b = b[(b.snap == snap) & (b.who == "Customer")]
    last_day = P.DAYS - 1
    S["open_qd"] = {(q, last_day - a): o for q, a, o in zip(b.queue, b.age0, b.open) if a < 42}
    S["open_qw"] = {}
    for (q, d), o in S["open_qd"].items():
        S["open_qw"][(q, d // 7)] = S["open_qw"].get((q, d // 7), 0) + o
    S["open_old"] = {q: o for q, a, o in zip(b.queue, b.age0, b.open) if a >= 42}
    # ---- conversations per parcel: all in-scope conversations by the consignment's due day, depot, class and family
    dep = {d[0]: i for i, d in enumerate(P.DEPOTS)}
    ok = (A.ci >= 0) & A.depot.notna()
    conv = np.zeros((P.DAYS, len(dep), NC, NF))
    np.add.at(conv, (A.due[ok].astype(int).values, A.depot[ok].map(dep).values, A.ci[ok].values, A.fi[ok].values), 1)
    parc = np.zeros((P.DAYS, len(dep), NC))
    net = D["net"]
    for col, c in (("on_time", 0), ("late_1", 1), ("late_2plus", 2), ("exception", 3)):
        np.add.at(parc, (net.due.values, net.depot.map(dep).values, c), net[col].values)
    alert = np.zeros((P.DAYS, len(dep)), bool)
    for code, d0 in D["alerts_from"].items():
        if d0 < P.DAYS:
            alert[d0:, dep[code]] = True
    S.update(conv=conv, parc=parc, alert=alert, pilot=alert.any(axis=0))
    S["Wc"] = (D["plan_parcels"][:, None] * D["plan_service"]).sum(axis=0)
    S["weeks"] = len(D["plan_parcels"])
    return S


def capture(S, how):
    """Each consignment-reason call's chance of carrying a tracking number, by the chosen grain."""
    c = S["cq"]
    v3 = (c.day >= W0)
    if how == "none":
        return pd.Series(1.0, index=c.index)
    if how == "pooled":
        return pd.Series(c.keyed[v3].mean(), index=c.index)
    keys = {"state": ["queue", "on"], "week": ["week", "queue"], "day": ["day", "queue"], "hour": ["hour", "queue"],
            "wait": ["queue", "wband"]}[how]
    g = c.groupby(keys).keyed
    p = g.transform("mean")
    if how in ("hour", "day"):                      # small cells are pulled to the queue's share at the same bypass state
        base = c.groupby(["queue", "on"]).keyed.transform("mean")
        m = g.transform("size")
        p = (p * m + base * 8.0) / (m + 8.0)
    return p.clip(lower=0.02)


def weights(S, capture_how="state", written="backlog"):
    """Each conversation's contribution to the unresolved count, and the follow-up contacts it stands for."""
    cap = capture(S, capture_how)
    capd = cap.to_dict()
    na, nc, nw, calls, wcase = S["na"], S["nc"], S["nw"], S["calls"], S["wcase"]
    A = S["A"]
    n = len(A)
    K = None
    U = np.zeros(n)
    seen = (na + nc + nw) > 0
    U[seen] = 1.0
    for i in np.where(~seen)[0]:
        if calls[i]:
            miss = 1.0
            for j in calls[i]:
                miss *= 1.0 - capd[j]
            U[i] = 1.0 / (1.0 - miss) if capture_how != "none" else 1.0
    g = np.zeros(n)
    if written != "none":
        sole = (nw > 0) & (na + nc == 0) & np.array([len(x) == 0 for x in calls])
        gq = S["_g"][written]
        for i in np.where(sole)[0]:
            g[i] = gq.get(wcase[i], 0.0)
    return U + g, cap


def case_growth(S, D):
    """What each closed customer case stands for beyond itself: the cases raised in its queue on its day (or, for the
    coarser routes, in its week) that are still open at the extract."""
    K = D["K"]; Kc = K[K.customer]
    out = {"backlog": {}, "daily": {}, "weekly": {}, "pooled": {}, "stationary": {}}
    cl, op = S["closed_qw"], S["open_qw"]
    cd, od = S["closed_qd"], S["open_qd"]
    wk0 = W0 // 7
    tot = {}
    for (q, w), o in op.items():
        if w >= wk0:
            a = tot.setdefault(q, [0, 0]); a[0] += o; a[1] += cl.get((q, w), 0)
    old = Kc[Kc.week < wk0 - 2]                       # the weeks long closed, for the route that assumes the lag never changed
    lag = {q: np.sort(((d.closed - d.start) / 24).values) for q, d in old.groupby("queue")}
    ext = P.DAYS * 24.0

    def near(q, d):                                   # the day and its neighbours either side, so no day stands on a handful of cases
        o = sum(od.get((q, x), 0) for x in (d - 1, d, d + 1)); c = sum(cd.get((q, x), 0) for x in (d - 1, d, d + 1))
        return (o / c) if c else 0.0
    for j, q, w, d, s in zip(Kc.index.values, Kc.queue.values, Kc.week.values, Kc.day.values, Kc.start.values):
        out["backlog"][j] = near(q, d)
        c = cd.get((q, d), 0)
        out["daily"][j] = (od.get((q, d), 0) / c) if c else 0.0
        c = cl.get((q, w), 0)
        out["weekly"][j] = (op.get((q, w), 0) / c) if c else 0.0
        out["pooled"][j] = (tot[q][0] / tot[q][1]) if (w >= wk0 and q in tot and tot[q][1]) else 0.0
        F = np.searchsorted(lag[q], (ext - s) / 24.0, side="right") / len(lag[q]) if q in lag else 1.0
        out["stationary"][j] = (1.0 / max(F, 0.05) - 1.0)
    return out


def tables(S, U):
    """Conversations and unresolved (estimated) by day ended, family and class, for the seven-day-old version 3 set."""
    A = S["A"]; w = S["win"]
    n = np.zeros((P.DAYS, NF, NC)); u = np.zeros((P.DAYS, NF, NC))
    np.add.at(n, (A.day.values[w], A.fi.values[w], A.ci.values[w]), 1)
    np.add.at(u, (A.day.values[w], A.fi.values[w], A.ci.values[w]), U[w])
    return n, u


def contacts(S, cap, D, written="backlog"):
    """Follow-up contacts to the windowed conversations by channel, each counted once against the latest conversation
    it follows: per day, family and class of that conversation."""
    A = S["A"]; w = S["win"]
    out = {ch: np.zeros((P.DAYS, NF, NC)) for ch in "PCW"}
    capd = cap.to_dict()
    gq = S["_g"][written] if written != "none" else {}
    day, fi, ci = A.day.values, A.fi.values, A.ci.values
    keyed = 0
    for (ch, j), i in S["last"].items():
        if not w[i]:
            continue
        if ch == "P":
            val = 1.0 / capd[j]; keyed += 1
        elif ch == "C":
            val = 1.0
        else:
            val = 1.0 + gq.get(j, 0.0)
        out[ch][day[i], fi[i], ci[i]] += val
    return out, keyed


def open_written(S, D, written="backlog"):
    """Customer cases still open at the extract that follow a windowed conversation: each closed follow-up case
    stands for the cases raised beside it that are still open."""
    gq = S["_g"][written] if written != "none" else {}
    tot = 0.0; n = 0
    for (ch, j), i in S["last"].items():
        if ch == "W" and S["win"][i]:
            n += 1
            tot += gq.get(j, 0.0)
    return tot, n


def alert_effect(S, m=None, how="did", pre0=0):
    """The delay alerts' effect on in-scope assistant conversations per late parcel: pilot depots against the rest,
    after against before, class by class."""
    if how == "none":
        return 0.0, {}
    conv, parc, pilot = S["conv"], S["parc"], S["pilot"]
    d0 = int(np.argmax(S["alert"].any(axis=1)))
    if m is None:
        m = np.ones(P.DAYS)
    wpre = m.copy(); wpre[:pre0] = 0; wpre[d0:] = 0
    wpost = m.copy(); wpost[:d0] = 0; wpost[W1:] = 0
    es, ws = {}, {}
    for c in (1, 2):
        r = {}
        for grp, cols in (("p", pilot), ("n", ~pilot)):
            for per, wt in (("0", wpre), ("1", wpost)):
                cv = (conv[:, cols, c, :].sum(axis=(1, 2)) * wt).sum()
                pc = (parc[:, cols, c].sum(axis=1) * wt).sum()
                r[grp + per] = cv / pc
        es[c] = 1 - (r["p1"] / r["p0"]) / (r["n1"] / r["n0"])
        ws[c] = (conv[:, pilot, c, :].sum(axis=(1, 2)) * wpost).sum()
    if how == "byclass":
        return es, es
    e = (es[1] * ws[1] + es[2] * ws[2]) / (ws[1] + ws[2])
    return e, es


def season(S, n, u, m=None, transport="propensity", alerts="did", pre0=0):
    """Each family's expected rate over the season plan, and the conversations the plan generates."""
    if m is None:
        m = np.ones(P.DAYS)
    wt = m.copy(); wt[:W0] = 0; wt[W1:] = 0
    nn = (n * wt[:, None, None]).sum(axis=0); uu = (u * wt[:, None, None]).sum(axis=0)
    r = 1 - uu / np.maximum(nn, 1e-9)
    ach = 100 * (1 - uu.sum(axis=1) / nn.sum(axis=1))
    ach_all = 100 * (1 - uu.sum() / nn.sum())
    out = dict(cell=r, n=nn, achieved=ach, achieved_all=ach_all)
    Wc = S["Wc"]
    if transport == "asis":
        out.update(expected=ach, expected_all=ach_all, M=None, e=0.0)
        return out
    if transport == "parcel":
        M = np.tile(Wc / Wc.sum(), (NF, 1)) * (nn.sum(axis=1, keepdims=True)) * (nn > 0)
        out.update(expected=100 * (M * r).sum(axis=1) / M.sum(axis=1), expected_all=100 * (M * r).sum() / M.sum(), M=None, e=0.0)
        return out
    e, es = alert_effect(S, m, alerts, pre0)
    un = ~S["alert"]                                      # depot-days with no alerts running
    cv = (S["conv"] * (un * wt[:, None])[:, :, None, None]).sum(axis=(0, 1))      # class x family
    pc = (S["parc"] * (un * wt[:, None])[:, :, None]).sum(axis=(0, 1))
    # the on-time and exception classes get no alert, so every depot-day counts for them
    cv2 = (S["conv"] * wt[:, None, None, None]).sum(axis=(0, 1)); pc2 = (S["parc"] * wt[:, None, None]).sum(axis=(0, 1))
    for c in (0, 3):
        cv[c] = cv2[c]; pc[c] = pc2[c]
    rho = (cv / pc[:, None]).T                            # family x class
    cut = np.ones(NC)
    if isinstance(e, dict):
        cut[1] -= e[1]; cut[2] -= e[2]
    else:
        cut -= e * LATE
    M = Wc[None, :] * rho * cut[None, :]
    out.update(expected=100 * (M * r).sum(axis=1) / np.maximum(M.sum(axis=1), 1e-9), expected_all=100 * (M * r).sum() / M.sum(),
               M=M, e=e, es=es, rho=rho, per_week=M.sum() / S["weeks"], late_share=100 * M[:, 1:].sum() / M.sum(),
               obs_per_week=nn.sum() / ((W1 - W0) / 7.0), obs_late_share=100 * nn[:, 1:].sum() / nn.sum())
    return out


def run(S, D, capture_how="state", written="backlog", transport="propensity", alerts="did", pre0=0):
    """One whole analysis under the chosen methods."""
    U, cap = weights(S, capture_how, written)
    n, u = tables(S, U)
    R = season(S, n, u, None, transport, alerts, pre0)
    R["n_day"], R["u_day"] = n, u
    A = S["A"]; w = S["win"]
    na, nc, nw = S["na"][w], S["nc"][w], S["nw"][w]
    hasp = np.array([len(x) > 0 for x in S["calls"]])[w]
    R["conversations"] = int(w.sum())
    R["linked_any"] = int(((na + nc + nw > 0) | hasp).sum())
    R["linked_rate"] = 100 * (1 - R["linked_any"] / w.sum())
    R["by_channel"] = dict(assistant=int((na > 0).sum()), chat=int((nc > 0).sum()), phone=int(hasp.sum()), written=int((nw > 0).sum()))
    K, keyed = contacts(S, cap, D, written)
    R["K"] = K
    R["phone_keyed"] = keyed
    R["phone_total"] = float(K["P"].sum())
    R["phone_unkeyed_share"] = 100 * (1 - keyed / K["P"].sum()) if capture_how != "none" else 0.0
    ow, wl = open_written(S, D, written)
    R["written_closed"] = wl
    R["written_open"] = ow if written != "none" else 0.0
    if R.get("M") is not None:
        kap = {ch: K[ch][W0:W1].sum(axis=0) / np.maximum(R["n"], 1e-9) for ch in "PCW"}
        R["adviser"] = {ch: float((R["M"] * kap[ch]).sum() / S["weeks"]) for ch in "PCW"}
    else:
        R["adviser"] = None
    return R


def bootstrap(S, D, R, B=600, unit="day", seed=7, transport="propensity", alerts="did"):
    """The range: days resampled whole (the three calendar blocks the estimates use kept apart), every estimate redone."""
    rng = np.random.default_rng(P.SEED + seed)
    n, u = R["n_day"], R["u_day"]
    ex = np.zeros((B, NF)); ex_all = np.zeros(B); pw = np.zeros(B)
    if unit == "day":
        blocks = [np.arange(0, W0), np.arange(W0, P.ALERT_DAY), np.arange(P.ALERT_DAY, W1)]
        for b in range(B):
            m = np.zeros(P.DAYS)
            for blk in blocks:
                pick = rng.choice(blk, size=len(blk), replace=True)
                np.add.at(m, pick, 1)
            r = season(S, n, u, m, transport, alerts)
            ex[b] = r["expected"]; ex_all[b] = r["expected_all"]; pw[b] = r.get("per_week", np.nan)
    else:                                               # conversations resampled one by one, everything else held fixed
        nn = n[W0:W1].sum(axis=0); uu = u[W0:W1].sum(axis=0)
        M = R["M"] if R.get("M") is not None else nn
        p = np.clip(uu / np.maximum(nn, 1), 0, 1)
        for b in range(B):
            ub = rng.binomial(nn.astype(int), p)
            rb = 1 - ub / np.maximum(nn, 1)
            ex[b] = 100 * (M * rb).sum(axis=1) / np.maximum(M.sum(axis=1), 1e-9); ex_all[b] = 100 * (M * rb).sum() / M.sum()
            pw[b] = R.get("per_week", np.nan)
    lo, hi = np.percentile(ex, 5, axis=0), np.percentile(ex, 95, axis=0)
    return dict(low=lo, high=hi, half=(hi - lo) / 2, low_all=float(np.percentile(ex_all, 5)), high_all=float(np.percentile(ex_all, 95)),
                half_all=float((np.percentile(ex_all, 95) - np.percentile(ex_all, 5)) / 2),
                per_week_low=float(np.nanpercentile(pw, 5)) if np.isfinite(pw).any() else None,
                per_week_high=float(np.nanpercentile(pw, 95)) if np.isfinite(pw).any() else None)


def setup(D):
    S = prep(D)
    S["_g"] = case_growth(S, D)
    return S


def tag_check(S, D):
    """A second reading of the telephone follow-ups, from the advisers' previous-contact tick: how often the tick is
    set on keyed calls that do and do not follow an assistant conversation, carried to the calls with no number."""
    cq = S["cq"]
    A = S["A"]
    follows = set(j for (ch, j), i in S["last"].items() if ch == "P")
    c = cq[(cq.day >= W0)]
    k = c[c.keyed]
    isf = k.index.isin(list(follows))
    tick = (k.previous_contact == "ASSISTANT").values
    sens = tick[isf].mean(); fp = tick[~isf].mean()
    u = c[~c.keyed]
    tu = (u.previous_contact == "ASSISTANT").mean()
    share_u = (tu - fp) / (sens - fp)
    cap = capture(S, "state")
    ipw = float((1.0 / cap[k.index[isf]] - 1.0).sum())
    return dict(sens=float(sens), false=float(fp), keyed_calls=int(len(k)), unkeyed_calls=int(len(u)), keyed_follow=int(isf.sum()),
                unkeyed_follow_tick=float(share_u * len(u)), unkeyed_follow_capture=ipw)


def reconcile(S, D):
    """The cleaned call and case counts against telephony's and the case system's own weekly totals."""
    Pc = D["P"]
    wk = (Pc.start // 168).astype(int)
    mine = Pc.groupby([wk, Pc.queue]).size()
    acd = D["acd"]
    theirs = {(i // len(P.QUEUES), q): v for i, (q, v) in enumerate(zip(acd.queue, acd.inbound))}
    diff = sum(abs(mine.get((w, q), 0) - v) for (w, q), v in theirs.items())
    K = D["K"]; Kc = K[K.customer]
    fl = D["flow"]; fl = fl[fl.who == "Customer"]
    opened = float(fl.opened.sum())
    return dict(calls=int(len(Pc)), acd_calls=int(acd.inbound.sum()), call_gap=int(diff), cases_closed=int(len(Kc)),
                cases_opened=int(opened), cases_open_now=int(sum(S["open_qd"].values()) + sum(S["open_old"].values())))


def diagnostics(S, D, U):
    """Two readings the write-up leans on: how much more the daily rate moves than independent conversations would,
    and whether late-parcel conversations resolve differently where the delay alerts ran."""
    A = S["A"]; w = S["win"]
    day = A.day.values[w]; u = U[w]
    n_d = np.bincount(day, minlength=P.DAYS)[W0:W1].astype(float); u_d = np.bincount(day, weights=u, minlength=P.DAYS)[W0:W1]
    keep = n_d > 0
    p = u_d.sum() / n_d.sum()
    x2 = (((u_d - n_d * p) ** 2) / (n_d * p * (1 - p)))[keep].sum() / (keep.sum() - 1)
    dep = {d[0]: i for i, d in enumerate(P.DEPOTS)}
    di = A.depot.map(dep).fillna(-1).astype(int).values
    due = A.due.fillna(-1).astype(int).values
    al = np.zeros(len(A), bool)
    ok = (di >= 0) & (due >= 0) & (due < P.DAYS)
    al[ok] = S["alert"][due[ok], di[ok]]
    late = np.isin(A.ci.values, (1, 2))
    post = A.day.values >= int(np.argmax(S["alert"].any(axis=1)))
    a = w & late & post & al; b = w & late & post & ~al
    # like for like: the unalerted conversations weighted to the alerted ones' family and class mix
    key = A.fi.values * 4 + A.ci.values
    ra = 1 - U[a].sum() / a.sum()
    na = np.bincount(key[a], minlength=NF * 4).astype(float); nb = np.bincount(key[b], minlength=NF * 4).astype(float)
    ub = np.bincount(key[b], weights=U[b], minlength=NF * 4)
    use = (na > 0) & (nb > 0)
    rb = 1 - (na[use] * ub[use] / nb[use]).sum() / na[use].sum()
    return dict(day_dispersion=float(x2), alerted_rate=float(100 * ra), unalerted_like_rate=float(100 * rb), alerted_n=int(a.sum()))
