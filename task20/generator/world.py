"""task20 world: Tarrant Hale Securities' Small and Mid Cap Facilitation desk on the published S&P 500, Nasdaq-100 and
VIX tape. The names, their prices, the desk's client flow, its books in two position systems, its middle office, its
ledger and its historical-simulation VaR engine (nightly snapshot, feed outages, proxy mapping) are simulated here.
Nothing in this module writes a file; pack.py turns a World into the shipped records."""
import os
import numpy as np
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
RAW = os.path.join(HERE, "raw")

W_DAYS = 500            # the engine's scenario window
Q_RANK = 5              # the 99% VaR: the fifth-largest loss of 500
HEDGE = 0.86            # the desk mandate's futures hedge ratio on beta-weighted net exposure
WIN_END = pd.Timestamp("2025-06-30")
SECTORS = ["Technology", "Health Care", "Financials", "Industrials", "Consumer Discretionary",
           "Communication Services", "Energy", "Materials", "Consumer Staples", "Real Estate"]
TECH_SECTORS = (0, 5)
MULT = {"ES": 50.0, "NQ": 20.0}
CARRY = {"ES": 0.034, "NQ": 0.039}


def load_market():
    spx = pd.read_csv(os.path.join(RAW, "SPX_History.csv"))
    spx["DATE"] = pd.to_datetime(spx["DATE"], format="%m/%d/%Y")
    spx = spx.set_index("DATE")["SPX"].astype(float)
    vix = pd.read_csv(os.path.join(RAW, "VIX_History.csv"))
    vix["DATE"] = pd.to_datetime(vix["DATE"], format="%m/%d/%Y")
    vix = vix.set_index("DATE")["CLOSE"].astype(float)
    ndx = pd.read_csv(os.path.join(RAW, "NASDAQ100.csv"))
    ndx.columns = ["d", "v"]
    ndx["d"] = pd.to_datetime(ndx["d"])
    ndx["v"] = pd.to_numeric(ndx["v"], errors="coerce")
    ndx = ndx.set_index("d")["v"]
    m = pd.concat({"spx": spx, "ndx": ndx}, axis=1, sort=True).dropna()
    future_days = m.loc["2025-07-01":"2025-12-31"].index      # the exchange calendar for the plan's months
    m = m.loc["2022-05-31":str(WIN_END.date())].copy()
    m["vix"] = vix.reindex(m.index).ffill()
    return m, future_days


MKT, FUTURE_DAYS = load_market()
DATES = MKT.index
SPX = MKT.spx.values
NDX = MKT.ndx.values
VIX = MKT.vix.values
RS = np.r_[0.0, SPX[1:] / SPX[:-1] - 1]
RN = np.r_[0.0, NDX[1:] / NDX[:-1] - 1]
E_IDX = len(DATES) - 1                 # 2025-06-30
S_IDX = E_IDX - 249                    # 2024-07-01, the first of the 250 days


def third_friday(y, m):
    d = pd.Timestamp(y, m, 1)
    off = (4 - d.weekday()) % 7
    return d + pd.Timedelta(days=off + 14)


def contract_schedule():
    """Quarterly E-mini expiries and the desk's roll dates (eight calendar days before expiry)."""
    codes = {3: "H", 6: "M", 9: "U", 12: "Z"}
    out = []
    for y in (2022, 2023, 2024, 2025):
        for m in (3, 6, 9, 12):
            exp = third_friday(y, m)
            out.append((codes[m] + str(y)[-1], exp, exp - pd.Timedelta(days=8)))
    return out


SCHED = contract_schedule()


def front_contract(date):
    """The contract the desk holds at the close of `date` (it rolls on the roll date)."""
    for code, exp, roll in SCHED:
        if date < roll:
            return code, exp
    return SCHED[-1][0], SCHED[-1][1]


def settlement(root, idx_level, date, expiry):
    tau = max((expiry - date).days, 0) / 365.0
    px = idx_level * np.exp(CARRY[root] * tau)
    return np.round(px * 4.0) / 4.0


def default_params():
    return dict(N=190, n_pairs=12, idio_k=1.15, sec_k=0.9, sec_base=0.0055, idio_mid=0.013, idio_small=0.024,
                jump_p=0.0025, earn_sd_mid=0.055, earn_sd_small=0.10, size_mid=2.2e6, size_small=1.1e6,
                long_share=0.82, flow_mu=20, notional_med=0.45e6, fee_rate=0.002, fee_p=0.12, fee_lo=1.6e5,
                fee_hi=5.2e5, comm_bp=2.0, hs_bp=6.0, outage_p=0.06, moc_mu=6, moc_amp=1.5, moc_tilt=0.3,
                moc_med=3.0e6, late_client=0.02, unwind_floor=1.5e5, unwind_share=0.10, unwind_rate=0.35, onboard_small_start="2023-02-01", store_days=500)


class World:
    pass


def simulate(seed, **kw):
    P = default_params()
    P.update(kw)
    w = World()
    w.seed, w.P = seed, P
    ra = np.random.default_rng(seed)                 # the names and their prices
    rb = np.random.default_rng(seed * 7919 + 17)     # the desk, its flow and its middle office
    rc = np.random.default_rng(seed * 104729 + 3)    # the engine's feed and run times
    T0, N = len(DATES), P["N"]
    vmed = np.median(VIX[:250])
    scl = np.r_[VIX[0], VIX[:-1]] / vmed
    # ---------------- names ----------------
    seg = np.where(np.arange(N) < int(N * 0.52), "MID", "SMALL")
    sec = ra.integers(0, len(SECTORS), N)
    tech = np.isin(sec, TECH_SECTORS)
    bS = np.where(seg == "MID", ra.uniform(0.75, 1.3, N), ra.uniform(0.8, 1.55, N))
    bT = np.where(tech, ra.uniform(0.25, 0.75, N), 0.0)
    gS = ra.uniform(0.6, 1.4, N)
    idv = np.where(seg == "MID", P["idio_mid"], P["idio_small"]) * ra.uniform(0.6, 1.5, N)
    F = np.zeros((T0, len(SECTORS)))
    for t in range(1, T0):
        F[t] = P["sec_base"] * scl[t] ** P["sec_k"] * ra.standard_t(5, len(SECTORS)) / np.sqrt(5 / 3)
    E = np.zeros((T0, N))
    for t in range(1, T0):
        E[t] = idv * scl[t] ** P["idio_k"] * ra.standard_t(4, N) / np.sqrt(2)
    earn_sd = np.where(seg == "MID", P["earn_sd_mid"], P["earn_sd_small"])
    earn_days = []
    for i in range(N):
        off = int(ra.integers(0, 25))
        for yr in (2022, 2023, 2024, 2025):
            for mo in (1, 4, 7, 10):
                k = DATES.searchsorted(pd.Timestamp(yr, mo, 20) + pd.Timedelta(days=off))
                if 0 < k < T0:
                    E[k, i] += ra.normal(0, earn_sd[i]) * np.sqrt(scl[k])
                    earn_days.append((k, i))
    jumps = ra.random((T0, N)) < P["jump_p"]
    E[jumps] += ra.normal(-0.01, 0.07, jumps.sum())
    R = bS * RS[:, None] + bT * (RN - RS)[:, None] + gS * F[:, sec] + E
    R[0] = 0.0
    R = np.clip(R, -0.6, 1.5)
    p0 = np.exp(ra.uniform(np.log(6), np.log(180), N))
    PX = np.round(np.maximum(p0 * np.cumprod(1 + R, axis=0), 0.5), 2)
    RR = np.vstack([np.zeros(N), PX[1:] / PX[:-1] - 1])     # returns as the vendor's closes give them
    w.seg, w.sec, w.tech, w.PX, w.RR, w.N = seg, sec, tech, PX, RR, N
    w.earn_days = earn_days
    # ---------------- onboarding, the store and the mapping ----------------
    s, e = S_IDX, E_IDX
    onboard = np.full(N, -1)                                # -1: on the desk and in the store before the record
    small = np.where(seg == "SMALL")[0]
    mid = np.where(seg == "MID")[0]
    k0 = DATES.searchsorted(pd.Timestamp(P["onboard_small_start"]))
    onboard[small] = np.sort(rb.integers(k0, e - 20, len(small)))
    recent_mid = rb.choice(mid, int(len(mid) * 0.12), replace=False)
    onboard[recent_mid] = rb.integers(k0, e - 60, len(recent_mid))
    w.onboard = onboard
    w.store_days = P["store_days"]

    def is_proxy(k):
        """the mapping in force for the run made on the evening of trading day k"""
        return (onboard >= 0) & (k < onboard + P["store_days"])
    w.is_proxy = is_proxy
    qstarts = [DATES.searchsorted(pd.Timestamp(y, m, 1)) for y in (2022, 2023, 2024, 2025) for m in (1, 4, 7, 10)]
    qstarts = sorted(set(q for q in qstarts if 260 < q <= e))
    bcache = {}

    def betas_at(k):
        q = max([qq for qq in qstarts if qq <= k] or [qstarts[0]])
        if q not in bcache:
            win = slice(q - 250, q)
            y = RR[win]
            out = np.zeros(N)
            for ridx, msk in ((RN, tech), (RS, ~tech)):
                x = ridx[win]
                b = ((y - y.mean(0)) * (x - x.mean())[:, None]).sum(0) / ((x - x.mean()) ** 2).sum()
                out[msk] = b[msk]
            bcache[q] = (q, np.round(out, 3))
        return bcache[q]
    w.betas_at, w.qstarts = betas_at, qstarts
    # ---------------- the desk ----------------
    size = np.where(seg == "MID", P["size_mid"], P["size_small"]) * np.exp(rb.normal(0, 0.6, N))
    side = np.where(rb.random(N) < P["long_share"], 1.0, -1.0)
    tgt = size * side
    pairs = []
    cand = [i for i in small if onboard[i] < s]
    rb.shuffle(cand)
    for i in cand[:P["n_pairs"]]:
        peers = [j for j in mid if sec[j] == sec[i] and not is_proxy(s)[j] and j not in [p[1] for p in pairs]]
        if peers:
            j = peers[int(rb.integers(len(peers)))]
            tgt[i] = abs(tgt[i]) * 2.6
            tgt[j] = -abs(tgt[i]) * 0.9 * gS[i] / gS[j]
            pairs.append((i, j))
    w.pairs = pairs
    T = e - s + 1
    sh = np.zeros((T + 1, N))           # sh[k]: shares held at the close of trading day s-1+k
    act0 = onboard <= s - 1
    sh[0] = np.where(act0, np.round(tgt * np.exp(rb.normal(0, 0.2, N)) / PX[s - 1]), 0.0)
    fut = [dict() for _ in range(T + 1)]   # fut[k]: {(root, code): contracts} at the close of day s-1+k
    trades = []                          # dicts: one per executed trade (cash and futures)
    newpnl = np.zeros(T)
    comm = np.zeros(T)
    flow_usd = np.zeros(T)
    run_start = np.zeros(T + 1)          # minutes after midnight, New York, the run on the evening of day s-1+k
    for k in range(T + 1):
        run_start[k] = 18 * 60 + 31 + min(max(rc.normal(4, 3), 0), 22)

    def hedge_targets(shares, k_day):
        _, b = betas_at(k_day)
        mv = shares * PX[k_day]
        return (-HEDGE * float((mv * np.where(tech, 0, b)).sum()), -HEDGE * float((mv * np.where(tech, b, 0)).sum()))

    def set_hedge(k, k_day, shares, prev):
        d = DATES[k_day]
        code, exp = front_contract(d)
        tgt_es, tgt_nq = hedge_targets(shares, k_day)
        new = {}
        for root, tg, lvl in (("ES", tgt_es, SPX[k_day]), ("NQ", tgt_nq, NDX[k_day])):
            stl = settlement(root, lvl, d, exp)
            n = int(np.round(tg / (MULT[root] * stl)))
            new[(root, code)] = n
        # trades: close any other contract (the roll), then adjust to the new count
        for key, n_old in prev.items():
            if key not in new and n_old != 0:
                trades.append(dict(k=k, kind="FUT", root=key[0], code=key[1], qty=-n_old, when="hedge"))
        for key, n_new in new.items():
            dq = n_new - prev.get(key, 0)
            if dq != 0:
                trades.append(dict(k=k, kind="FUT", root=key[0], code=key[1], qty=dq, when="hedge"))
        return new
    fut[0] = set_hedge(-1, s - 1, sh[0], {})
    for k in range(T):
        t = s + k
        z = RS[t] / np.std(RS[t - 60:t])
        hold = sh[k].copy()
        act = np.where(onboard <= t)[0]
        n = rb.poisson(P["flow_mu"] * (1 + 0.45 * min(abs(z), 3)))
        for _ in range(n):
            i = int(act[rb.integers(len(act))])
            buy = rb.random() < 0.5 - 0.24 * np.tanh(z)
            notional = np.exp(rb.normal(np.log(P["notional_med"]), 0.8))
            f = rb.beta(1, 2.5)
            mid_px = PX[t - 1, i] * (1 + f * RR[t, i])
            px = round(mid_px * (1 - P["hs_bp"] * 1e-4 if buy else 1 + P["hs_bp"] * 1e-4), 2)
            qty = float(np.round(notional / px)) * (1 if buy else -1)
            if qty == 0:
                continue
            late = rb.random() < P["late_client"]
            tmin = 9 * 60 + 30 + f * 390
            trades.append(dict(k=k, kind="EQ", i=i, qty=qty, px=px, tmin=tmin, when="client", late=late))
            newpnl[k] += qty * (PX[t, i] - px)
            comm[k] += abs(qty * px) * P["comm_bp"] * 1e-4
            flow_usd[k] += abs(qty * px)
            hold[i] += qty
        # the desk works its inventory toward target in the closing cross (booked straight away)
        mv = hold * PX[t]
        gap = tgt - mv
        material = np.isin(np.arange(N), act) & (np.abs(gap) > np.maximum(P["unwind_floor"], P["unwind_share"] * np.abs(tgt)))
        dq = np.where(material, np.round(P["unwind_rate"] * gap / PX[t]), 0.0)
        for i in np.where(dq != 0)[0]:
            trades.append(dict(k=k, kind="EQ", i=int(i), qty=float(dq[i]), px=float(PX[t, i]), tmin=16 * 60,
                               when="desk", late=False))
        hold = hold + dq
        # client closing-auction orders, allocated by the middle office after the close
        n_moc = rb.poisson(P["moc_mu"] * (1 + P["moc_amp"] * min(abs(z), 4)))
        for _ in range(n_moc):
            i = int(act[rb.integers(len(act))])
            sgn = 1.0 if rb.random() < 0.5 - P["moc_tilt"] * np.tanh(z) else -1.0
            notional = np.exp(rb.normal(np.log(P["moc_med"]), 0.7))
            qty = sgn * float(np.round(notional / PX[t, i]))
            if qty == 0:
                continue
            trades.append(dict(k=k, kind="EQ", i=i, qty=qty, px=float(PX[t, i]), tmin=16 * 60, when="alloc",
                               late=True))
            flow_usd[k] += abs(qty * PX[t, i])
            hold[i] += qty
        sh[k + 1] = hold
        fut[k + 1] = set_hedge(k, t, hold, fut[k])
        tgt = tgt * np.exp(rb.normal(0, 0.015, N))
    w.sh, w.fut, w.trades, w.T, w.s, w.e = sh, fut, trades, T, s, e
    w.newpnl, w.comm, w.flow_usd, w.run_start = newpnl, comm, flow_usd, run_start
    # ---------------- futures prices ----------------
    codes = sorted({key for d in fut for key in d})
    w.fut_codes = codes
    stl = {}
    for root, code in codes:
        exp = next(x[1] for x in SCHED if x[0] == code)
        lv = SPX if root == "ES" else NDX
        stl[(root, code)] = np.array([settlement(root, lv[t], DATES[t], exp) for t in range(T0)])
    w.stl = stl
    # ---------------- P&L ----------------
    hyp = np.zeros(T)
    for k in range(T):
        t = s + k
        hyp[k] = float(sh[k] @ (PX[t] - PX[t - 1]))
        for key, n in fut[k].items():
            hyp[k] += n * MULT[key[0]] * (stl[key][t] - stl[key][t - 1])
    fees = P["fee_rate"] * flow_usd * np.exp(rb.normal(0, 0.35, T))
    lump = rb.random(T) < P["fee_p"]
    fees[lump] += rb.uniform(P["fee_lo"], P["fee_hi"], lump.sum())
    month_end = np.array([DATES[s + k].month != DATES[min(s + k + 1, len(DATES) - 1)].month or s + k == len(DATES) - 1
                          for k in range(T)])
    resv = np.zeros(T)
    resv[month_end] = rb.normal(-6e4, 3.2e5, month_end.sum())
    fund = np.array([-abs(sh[k] * PX[s + k - 1]).sum() * 0.052 / 360 * 0.4 for k in range(T)])
    w.hyp, w.fees, w.resv, w.fund = hyp, fees, resv, fund
    w.booked = hyp + newpnl + comm + fees + resv + fund
    # ---------------- the engine's snapshots ----------------
    # trades booked after the run started on their trade date: closing allocations always, a few client tickets
    late_by_day = [np.zeros(N) for _ in range(T)]
    for tr in trades:
        if tr["kind"] == "EQ" and tr.get("late") and tr["k"] >= 0:
            late_by_day[tr["k"]][tr["i"]] += tr["qty"]
    snap_sh = np.zeros((T + 1, N))
    snap_fut = [dict() for _ in range(T + 1)]
    snap_sh[0] = sh[0]
    snap_fut[0] = dict(fut[0])
    for k in range(T):
        snap_sh[k + 1] = sh[k + 1] - late_by_day[k]
        snap_fut[k + 1] = dict(fut[k + 1])
    stale = np.zeros(T + 1, int)
    k = 1
    while k <= T:
        if rc.random() < P["outage_p"]:
            L = int(rc.integers(1, 4))
            for m in range(L):
                if k + m <= T:
                    stale[k + m] = m + 1
            k += L
        else:
            k += 1
    used = np.array([k - stale[k] for k in range(T + 1)])     # which evening's snapshot each run used
    w.snap_sh, w.snap_fut, w.stale, w.used, w.late_by_day = snap_sh, snap_fut, stale, used, late_by_day
    eng_sh = np.array([snap_sh[used[k]] for k in range(T + 1)])
    eng_fut = [snap_fut[used[k]] for k in range(T + 1)]
    w.eng_sh, w.eng_fut = eng_sh, eng_fut
    # reported VaR for window day k comes from the run on the evening of day s-1+k (index k)
    w.rep = np.array([var(w, eng_sh[k], eng_fut[k], k) for k in range(T)])
    return w


def scenario_matrix(w, k, mode="engine", mapping_k=None):
    """the 500 scenario returns for the run on the evening of trading day s-1+k (forecasting window day k)."""
    t = w.s + k                          # the forecast day; the window is the 500 days ending t-1
    Rw = w.RR[t - W_DAYS:t].copy()
    Sw, Nw = RS[t - W_DAYS:t], RN[t - W_DAYS:t]
    if mode == "engine":
        kk = (t - 1) if mapping_k is None else mapping_k
        px = w.is_proxy(kk)
        _, b = w.betas_at(t - 1)
        Rw[:, px] = (np.where(w.tech[px], 1.0, 0.0) * np.outer(Nw, b[px]) +
                     np.where(w.tech[px], 0.0, 1.0) * np.outer(Sw, b[px]))
    return Rw, Sw, Nw


def scen_pnl(w, shares, futs, k, mode="engine", mapping_k=None):
    t = w.s + k
    Rw, Sw, Nw = scenario_matrix(w, k, mode, mapping_k)
    mv = shares * w.PX[t - 1]
    sc = Rw @ mv
    for key, n in futs.items():
        notional = n * MULT[key[0]] * w.stl[key][t - 1]
        sc = sc + notional * (Sw if key[0] == "ES" else Nw)
    return sc


def fhs(sc, lam, scale_series=None):
    v = np.var(sc[:50])
    vs = np.zeros(len(sc))
    for i in range(len(sc)):
        vs[i] = v
        v = lam * v + (1 - lam) * sc[i] ** 2
    return sc * np.sqrt(v) / np.sqrt(vs)


def var_from(sc, q="fifth"):
    srt = np.sort(sc)
    if q == "interp":
        return -(srt[Q_RANK - 1] + srt[Q_RANK]) / 2.0
    return -srt[Q_RANK - 1]


def var(w, shares, futs, k, mode="engine", lam=None, scale="portfolio", q="fifth", mapping_k=None):
    if lam and scale == "series":
        t = w.s + k
        Rw, Sw, Nw = scenario_matrix(w, k, mode, mapping_k)
        X = np.column_stack([Rw, Sw, Nw])
        v = X[:50].var(0)
        vs = np.zeros_like(X)
        for i in range(len(X)):
            vs[i] = v
            v = lam * v + (1 - lam) * X[i] ** 2
        X = X * np.sqrt(v) / np.sqrt(vs)
        Rw, Sw, Nw = X[:, :w.N], X[:, w.N], X[:, w.N + 1]
        mv = shares * w.PX[t - 1]
        sc = Rw @ mv
        for key, n in futs.items():
            sc = sc + n * MULT[key[0]] * w.stl[key][t - 1] * (Sw if key[0] == "ES" else Nw)
        return var_from(sc, q)
    sc = scen_pnl(w, shares, futs, k, mode, mapping_k)
    if lam:
        sc = fhs(sc, lam)
    return var_from(sc, q)


def classify(w, lam=0.94, scale="portfolio", q="fifth"):
    T = w.T
    rep = w.rep if q == "fifth" else np.array([var(w, w.eng_sh[k], w.eng_fut[k], k, q=q) for k in range(T)])
    good = np.array([var(w, w.sh[k], w.fut[k], k, q=q) for k in range(T)])
    full = np.array([var(w, w.sh[k], w.fut[k], k, "full", q=q) for k in range(T)])
    sound = np.array([var(w, w.sh[k], w.fut[k], k, "full", lam=lam, scale=scale, q=q) for k in range(T)])
    off = w.booked < -rep
    hx = w.hyp < -rep
    union = off | hx
    cls = np.full(T, "", object)
    for k in np.where(union)[0]:
        if off[k] and not hx[k]:
            cls[k] = "income"
        elif w.hyp[k] >= -good[k]:
            cls[k] = "inputs"
        elif w.hyp[k] >= -full[k]:
            cls[k] = "omitted"
        elif w.hyp[k] >= -sound[k]:
            cls[k] = "volatility"
        else:
            cls[k] = "sound"
    st = w.stale[:T] > 0
    out = dict(official=int(off.sum()), hyp=int(hx.sum()), union=int(union.sum()), masked=int((hx & ~off).sum()),
               booked_only=int((off & ~hx).sum()), sound_count=int((w.hyp < -sound).sum()),
               stale_runs=int((w.stale[:T] > 0).sum()), stale_coincident=int((st & union).sum()),
               stale_caused=int((st & (cls == "inputs")).sum()), late_caused=int((~st & (cls == "inputs")).sum()))
    for c in ("income", "inputs", "omitted", "volatility", "sound"):
        out[c] = int((cls == c).sum())
    out.update(cls=cls, v_good=good, v_full=full, v_sound=sound, off=off, hx=hx)
    return out
