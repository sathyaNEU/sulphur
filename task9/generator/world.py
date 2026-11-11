"""task9 (architecture 10): the simulated request-for-quote market around Brindlemoor's credit desk.

The process, as the systems record it:
  * bonds price off the real Treasury curve and Moody's Baa spread (with a VIX term in high yield), plus each
    issuer's own news, which reaches a bond's value over a few days and moves thin bonds further than their
    issuer's liquid benchmark (a liquidity beta);
  * Ashcote evaluates every bond at each close: the curve and the rating-sector move in full, the issuer's own move
    from the prints of the issuer's tradeable bonds, and a bond's extra share of it only from that bond's own prints;
  * clients send requests to several dealers; some hedge funds and a few asset managers trade on issuer news before
    it is in the price; two large rivals see enough flow to read many of those requests and mark thin bonds near the
    market, the other rivals mark on evaluations as the desk does; a rival is sometimes axed the client's way;
  * the desk's auto-quoter prices each request from its schedule (segment half-spread, size and stress multiples,
    inventory skew, its own jitter) around its evaluated mark; the best price wins, the winner sees the cover;
  * every trade prints on the public tape (delays, capped sizes, cancels and corrections, interdealer trades from
    both sides); the desk sells part of its inventory to dealers each evening.
The world never reads a hurried method's answer; analysis.py reads the pack it writes.
"""
import numpy as np
import pandas as pd

import market as MK
import params as P

SECTORS = ["Industrials", "Utilities", "Financials", "Energy", "Consumer", "Technology", "Healthcare", "Telecom",
           "Materials", "Transport"]
ROOT_A = ["Al", "Bra", "Cor", "Dal", "Em", "Fen", "Gal", "Hal", "Ir", "Jor", "Kel", "Lun", "Mar", "Nor", "Os", "Pel",
          "Quin", "Ros", "Sel", "Tor", "Ul", "Ver", "Wes", "Yar", "Zan"]
ROOT_B = ["ston", "vane", "mere", "cott", "ridge", "bourne", "wick", "dale", "ford", "hurst", "brook", "field",
          "gate", "worth", "ley", "more", "stead", "holm", "crest", "vale"]
SUFFIX = {"Industrials": "Industries", "Utilities": "Power", "Financials": "Capital", "Energy": "Energy",
          "Consumer": "Brands", "Technology": "Systems", "Healthcare": "Health", "Telecom": "Communications",
          "Materials": "Materials", "Transport": "Logistics"}


def cusip_check(base8):
    """The CUSIP check digit of an eight-character base."""
    s = 0
    for i, ch in enumerate(base8):
        v = int(ch) if ch.isdigit() else ord(ch) - 55
        if i % 2 == 1:
            v *= 2
        s += v // 10 + v % 10
    return str((10 - s % 10) % 10)


def bucket_of(prints_q):
    return "liquid" if prints_q >= P.BUCKET_PRINTS[0] else ("medium" if prints_q >= P.BUCKET_PRINTS[1] else "thin")


class World:
    def __init__(self, mk, seed=P.SEED):
        self.mk = mk
        self.rng = np.random.default_rng(seed)
        self.T = mk.n
        self._universe()
        self._paths()
        self._clients()
        self._news_flow()
        self._run()

    # ---------------------------------------------------------------------------------------------- the universe
    def _universe(self):
        rng, mk = self.rng, self.mk
        names = set()
        iss = []
        for i in range(P.N_ISSUERS):
            r = rng.choice(P.RATINGS, p=P.RATING_SHARE)
            sec = SECTORS[rng.integers(len(SECTORS))]
            while True:
                nm = "%s%s %s" % (ROOT_A[rng.integers(len(ROOT_A))], ROOT_B[rng.integers(len(ROOT_B))], SUFFIX[sec])
                if nm not in names:
                    names.add(nm)
                    break
            code = "".join(rng.choice(list("ABCDEFGHJKLMNPRSTUVWXYZ0123456789"), 6))
            iss.append(dict(issuer=i, name=nm, sector=sec, rating0=r, code=code))
        self.issuers = pd.DataFrame(iss)
        bonds = []
        start = mk.days[0]
        for row in iss:
            ig = row["rating0"] in P.IG
            nb = int(rng.choice([2, 3, 3, 4]) if ig else rng.choice([1, 1, 2, 2, 3]))
            for j in range(nb):
                new = rng.random() < 0.24
                if new:
                    issue = mk.days[rng.integers(0, mk.n - 40)]
                else:
                    issue = start - pd.Timedelta(days=int(rng.integers(120, 3200)))
                tenor = int(rng.choice([3, 5, 7, 10, 20, 30] if ig else [5, 7, 8, 10], p=None))
                mat = issue + pd.DateOffset(years=tenor)
                if mat <= start + pd.Timedelta(days=60):
                    mat = start + pd.DateOffset(years=int(rng.integers(2, 9)))
                amt = float(np.round(np.exp(rng.normal(np.log(1.1e9 if ig else 5.5e8), 0.45)) / 5e7) * 5e7)
                amt = max(amt, 2.5e8)
                bonds.append(dict(issuer=row["issuer"], j=j, issue=issue, maturity=mat, amount=amt, ig0=ig,
                                  is144a=(not ig) and new and rng.random() < 0.6))
        B = pd.DataFrame(bonds)
        # trim or pad to the universe's size, keeping every issuer's first bond
        if len(B) > P.N_BONDS:
            drop = B[B.j > 0].sample(len(B) - P.N_BONDS, random_state=int(rng.integers(1e9))).index
            B = B.drop(drop)
        B = B.sort_values(["issuer", "j"]).reset_index(drop=True)
        B["j"] = B.groupby("issuer").cumcount()
        # coupons from the yield at issue (the Treasury and the rating's spread on the closest record day)
        cps, ids = [], []
        for k, b in B.iterrows():
            i0 = max(0, min(mk.n - 1, mk.index_of(b["issue"])))
            r = self.issuers.rating0[b["issuer"]]
            tenor = (b["maturity"] - b["issue"]).days / 365.25
            y = mk.treasury(i0, np.array([tenor]))[0] + P.SPREAD_MULT[r] * mk.baa_spread[i0] + rng.normal(0, 0.002)
            if b["issue"] < start:
                y += rng.normal(-0.004, 0.008)        # seasoned bonds came at the rates of their own day
            cps.append(max(0.5, np.round(y * 100 * 8) / 8) / 100.0)
            base = self.issuers.code[b["issuer"]] + "%02d" % (10 + 7 * k % 89)
            ids.append(base[:8] + cusip_check(base[:8]))
        B["coupon"] = cps
        B["cusip"] = ids
        # how much a bond trades: size, age and grade; the issuer's largest, newest bond is its benchmark
        age = np.maximum((start - B.issue).dt.days.values / 365.25, 0)
        lam = 0.55 * (B.amount.values / 1e9) ** 1.1 * np.where(B.ig0, 1.25, 0.95) * (0.55 + 0.9 * np.exp(-age / 2.5))
        lam *= np.exp(rng.normal(0, 0.55, len(B)))
        B["lam"] = lam
        bench = B.groupby("issuer").amount.transform("max") == B.amount
        B["bench"] = bench & ~B.duplicated(["issuer", "amount"])
        # a thin bond moves further than its issuer's benchmark on the issuer's news
        B["beta"] = np.where(B.bench, 1.0, 1.0 + np.clip(0.75 - 0.9 * np.log1p(B.lam.values), 0.2, 0.9))
        B["basis"] = np.clip((B.maturity - start).dt.days.values / 365.25 - 5, 0, 25) * 0.00012 + \
            rng.normal(0, 0.0012, len(B))
        # 144A bonds are exchanged for registered bonds under a new identifier some months after issue
        exch, newid = [], []
        for k, b in B.iterrows():
            if b["is144a"]:
                d = b["issue"] + pd.Timedelta(days=int(rng.integers(140, 230)))
                exch.append(d if d < mk.days[-1] else pd.NaT)
                base = self.issuers.code[b["issuer"]] + "%02d" % (60 + k % 39)
                newid.append(base[:8] + cusip_check(base[:8]))
            else:
                exch.append(pd.NaT)
                newid.append("")
        B["exchange_date"], B["cusip_reg"] = exch, newid
        self.B = B
        self.nb = len(B)
        self.alive = np.zeros((self.T, self.nb), bool)
        for k, b in B.iterrows():
            self.alive[:, k] = (mk.days >= b["issue"]) & (mk.days < b["maturity"])

    # ----------------------------------------------------------------------------------------------- the paths
    def _paths(self):
        rng, mk, B, T = self.rng, self.mk, self.B, self.T
        S = mk.baa_spread
        Sbar = S.mean()
        vix = mk.vix
        ni = P.N_ISSUERS
        # the issuer's own spread: information every day (a random walk) and now and then a larger event that
        # reaches value over a few days
        I = np.zeros((T, ni))
        self.news = []
        rating = np.array([self.issuers.rating0[i] for i in range(ni)], dtype=object)
        sd = np.array([P.IDIO_SD[r] for r in rating]) * 1e-4
        for i in range(ni):
            r = rating[i]
            n = rng.poisson(P.NEWS_RATE[r] * T / 252.0)
            for _ in range(n):
                t0 = int(rng.integers(5, T - 1))
                jump = float(np.clip(rng.standard_t(6) / np.sqrt(1.5), -3.5, 3.5)) * P.NEWS_SD[r] * 1e-4
                D = int(rng.integers(P.NEWS_DAYS[0], P.NEWS_DAYS[1] + 1))
                I[:, i] += jump * np.clip((np.arange(T) - t0 + 1) / D, 0, 1)
                self.news.append(dict(issuer=i, t0=t0, days=D, jump=jump))
        walk = np.zeros((T, ni))
        z = rng.normal(0, 1, (T, ni))
        for t in range(1, T):
            walk[t] = walk[t - 1] * (1 - 0.002) + z[t] * sd
        I += walk
        # ratings move with the issuer's own spread; the issuer's move is re-based so its total spread is continuous
        rat = np.empty((T, ni), dtype=object)
        lvl = {r: k for k, r in enumerate(P.RATINGS)}
        cur = rating.copy()
        mp = mk.days.to_period("M")
        month_end = np.r_[mp[1:] != mp[:-1], True]
        shift = np.zeros(ni)
        mkt_lvl = np.zeros((T, ni))
        Ieff = np.zeros((T, ni))
        for t in range(T):
            lv = {r: P.SPREAD_MULT[r] * Sbar * (S[t] / Sbar) ** P.CREDIT_BETA[r] + P.VIX_BETA[r] * (vix[t] - 17.0) * 1e-4
                  for r in P.RATINGS}
            if month_end[t]:
                for i in range(ni):
                    r = cur[i]
                    x = I[t, i] - shift[i]
                    if x > 0.9 * P.SPREAD_MULT[r] * Sbar and lvl[r] < len(P.RATINGS) - 1 and rng.random() < 0.5:
                        nr = P.RATINGS[lvl[r] + 1]
                    elif x < -0.45 * P.SPREAD_MULT[r] * Sbar and lvl[r] > 0 and rng.random() < 0.35:
                        nr = P.RATINGS[lvl[r] - 1]
                    else:
                        continue
                    shift[i] += lv[nr] - lv[r]
                    cur[i] = nr
            rat[t] = cur
            mkt_lvl[t] = [lv[r] for r in cur]
            Ieff[t] = I[t] - shift
        self.rating = rat
        self.mkt_lvl = mkt_lvl
        self.I = Ieff                              # the issuer's own move, net of its rating label's level
        # each bond's own residual drift
        e = np.zeros((T, self.nb))
        for t in range(1, T):
            e[t] = e[t - 1] * (1 - 0.01) + rng.normal(0, 0.18e-4, self.nb) * np.where(B.ig0, 1.0, 2.2)
        self.e = e
        bi = B.issuer.values
        self.mat = np.array([[(b - d).days / 365.25 for b in B.maturity] for d in mk.days])
        self.mat = np.maximum(self.mat, 1.0 / 365)
        tsy = np.array([mk.treasury(t, self.mat[t]) for t in range(T)])
        self.tsy = tsy
        self.mkt_spread = mkt_lvl[:, bi] + B.basis.values[None, :]
        self.true_spread = self.mkt_spread + B.beta.values[None, :] * self.I[:, bi] + e
        self.V = MK.price(tsy + self.true_spread, B.coupon.values[None, :], self.mat)
        self.ig = np.array([[rat[t, i] in P.IG for i in bi] for t in range(T)])

    # --------------------------------------------------------------------------------------------- the clients
    def _clients(self):
        rng = self.rng
        rows = []
        k = 0
        for t, n in P.N_CLIENTS.items():
            for _ in range(n):
                k += 1
                inf = rng.random() < P.INFORMED_SHARE[t]
                rows.append(dict(client=k, ctype=t, weight=float(np.exp(rng.normal(0, 0.8))),
                                 include=float(np.clip(rng.beta(6, 2.2) if t != "RET" else rng.beta(12, 1.5), 0.2, 0.99)),
                                 informed=inf, hy_pref=float(np.clip(P.HY_PREF[t] + rng.normal(0, 0.12), 0.02, 0.95)),
                                 onboard=self.mk.days[0] - pd.Timedelta(days=int(rng.integers(30, 2500)))
                                 if rng.random() < 0.86 else self.mk.days[int(rng.integers(20, self.T - 120))]))
        C = pd.DataFrame(rows)
        codes = rng.choice(np.arange(1000, 9999), len(C), replace=False)
        C["code"] = ["TW" + str(c) for c in codes]
        cover = []
        for _, c in C.iterrows():
            if c["informed"]:
                pool = np.arange(P.N_ISSUERS)
                w = np.array([3.0 if self.issuers.rating0[i] not in P.IG else 1.0 for i in pool]) if c["ctype"] == "HF" \
                    else np.ones(len(pool))
                cover.append(set(rng.choice(pool, int(rng.integers(14, 30)), replace=False, p=w / w.sum())))
            else:
                cover.append(set())
        C["covers"] = cover
        self.C = C

    def _news_flow(self):
        """The requests informed clients send when they can see the issuer's coming week before it is in the price."""
        rng = self.rng
        out = []
        H = P.INFORMED_HORIZON
        lead = np.zeros_like(self.I)
        lead[:-H] = self.I[H:] - self.I[:-H]
        thr = np.array([P.INFORMED_THRESHOLD["IG" if self.issuers.rating0[i] in P.IG else "HY"]
                        for i in range(P.N_ISSUERS)]) * 1e-4
        inf = self.C[self.C.informed]
        for _, c in inf.iterrows():
            for i in c["covers"]:
                hot = np.where(np.abs(lead[:, i]) > thr[i])[0]
                hot = hot[(hot >= 1) & (rng.random(len(hot)) < P.INFORMED_DAILY[c["ctype"]])]
                for t in hot:
                    bonds = np.where((self.B.issuer.values == i) & self.alive[t])[0]
                    if len(bonds) == 0:
                        continue
                    w = self.B.lam.values[bonds]
                    b = int(rng.choice(bonds, p=w / w.sum()))
                    out.append(dict(t=int(t), client=int(c["client"]), bond=b, side=-1 if lead[t, i] > 0 else 1,
                                    informed=True, mult=float(rng.uniform(1.0, 1.8))))
        self.inf_req = pd.DataFrame(out)

    # -------------------------------------------------------------------------------------------- the schedule
    def schedule_h(self, t, seg):
        b, l, c = seg
        h = P.SCHEDULE_V1[(b, l)][c]
        d = self.mk.days[t]
        if d >= pd.Timestamp(P.V2_DATE) and seg in P.V2_CHANGES:
            h = P.V2_CHANGES[seg]
        if d >= pd.Timestamp(P.V3_DATE) and seg in P.V3_CHANGES:
            h = P.V3_CHANGES[seg]
        return h

    # ------------------------------------------------------------------------------------------------ the run
    def _run(self):
        rng, mk, B, C, T = self.rng, self.mk, self.B, self.C, self.T
        nb = self.nb
        bi = B.issuer.values
        cpn = B.coupon.values
        # the evaluator's state: the issuer's move it has taken in, and each bond's extra share
        Ihat = np.zeros(P.N_ISSUERS)
        ehat = np.zeros(nb)
        eval_mid = np.zeros((T, nb))
        eval_spread_prev = None
        prints_q = np.zeros(nb)                     # prints this quarter (the security master's buckets)
        bucket = np.array([bucket_of(l * 63 * 1.6) for l in B.lam.values], dtype=object)
        self.bucket_hist = []
        pos = np.zeros(nb)                          # the desk's position, face
        req_rows, trade_rows, print_rows, pnl_rows = [], [], [], []
        rid = 100000
        tid = 500000
        ctype = dict(zip(C.client, C.ctype))
        cinc = dict(zip(C.client, C.include))
        cw = {t: C[C.ctype == t] for t in P.CLIENT_TYPES}
        inf_by_t = {t: g for t, g in self.inf_req.groupby("t")} if len(self.inf_req) else {}
        outage = set(rng.choice(np.arange(20, T - 20), 3, replace=False).tolist())
        early = set(i for i, d in enumerate(mk.days) if (d.month == 11 and d.dayofweek == 4 and 22 <= d.day <= 28) or
                    (d.month == 12 and d.day == 24) or (d.month == 7 and d.day == 3))
        years = (mk.days - mk.days[0]).days.values / 365.25
        quarter = mk.days.to_period("Q")
        for t in range(T):
            d = mk.days[t]
            if t > 0 and quarter[t] != quarter[t - 1]:
                bucket = np.array([bucket_of(x) for x in prints_q], dtype=object)
                prints_q[:] = 0
            self.bucket_hist.append((quarter[t], bucket.copy()))
            alive = self.alive[t]
            pos[~alive] = 0.0                       # a bond that has matured is redeemed
            vix_prev = mk.vix[max(t - 1, 0)]
            stress = next(m for b_, m in P.STRESS if vix_prev < b_)
            V = self.V[t]
            # the evaluator's mark for today's quotes: today's curve and sector, yesterday's issuer and own moves
            mark_spread = self.mkt_spread[t] + Ihat[bi] + ehat
            mark = MK.price(self.tsy[t] + mark_spread, cpn, self.mat[t])
            gap = mark - V
            large_mark = V + P.LARGE_MARK_SD * gap
            seg_ig = self.ig[t]
            # ---- the day's requests to the desk
            mf = {1: 1.08, 8: 0.82, 12: 0.80}.get(d.month, 1.0)
            dow = [0.96, 1.04, 1.06, 1.04, 0.90][d.dayofweek]
            me = 1.22 if (t + 2 < T and mk.days[t + 2].month != d.month) else 1.0
            lam_day = P.RFQ_PER_DAY * (1 + P.RFQ_GROWTH) ** years[t] * mf * dow * me * \
                (1 + 0.025 * np.clip(vix_prev - 16, -6, 30)) * (0.55 if t in early else 1.0)
            n_req = rng.poisson(lam_day)
            types = rng.choice(P.CLIENT_TYPES, n_req, p=[P.TYPE_SHARE[x] for x in P.CLIENT_TYPES])
            reqs = []
            live = np.where(alive)[0]
            lamw = B.lam.values[live] ** 0.8
            for ty in P.CLIENT_TYPES:
                k = int((types == ty).sum())
                if k == 0:
                    continue
                pool = cw[ty][(cw[ty].onboard <= d)]
                w = (pool.weight * pool.include).values
                cl = rng.choice(pool.client.values, k, p=w / w.sum())
                hyp = dict(zip(pool.client, pool.hy_pref))
                for c in cl:
                    hy = rng.random() < hyp[c]
                    cand = live[~seg_ig[live]] if hy else live[seg_ig[live]]
                    if len(cand) == 0:
                        cand = live
                    ww = B.lam.values[cand] ** P.REQ_LAM_POW
                    b = int(rng.choice(cand, p=ww / ww.sum()))
                    reqs.append(dict(client=int(c), bond=b, side=int(rng.choice([-1, 1])), informed=False, mult=1.0))
            for _, r in inf_by_t.get(t, pd.DataFrame()).iterrows():
                if not alive[int(r["bond"])]:
                    continue
                reqs.append(dict(client=int(r["client"]), bond=int(r["bond"]), side=int(r["side"]), informed=True,
                                 mult=float(r["mult"]), to_desk=rng.random() < cinc[int(r["client"])]))
            # times through the day, New York
            close_h = 14.0 if t in early else 17.0
            day_prints = np.zeros(nb)
            for r in reqs:
                ty = ctype[r["client"]]
                mu, sd = P.SIZE[ty]
                q = np.exp(rng.normal(mu, sd)) * r["mult"]
                q = max(5000.0, np.round(q / (5000 if ty == "RET" else 100000)) * (5000 if ty == "RET" else 100000))
                r["q"] = float(min(q, 0.02 * B.amount.values[r["bond"]]))
                u = rng.random()
                r["hour"] = 8.0 + (close_h - 8.0) * (0.5 + 0.5 * np.sin(np.pi * (u - 0.5)) if rng.random() < 0.5
                                                     else rng.random())
                r["n"] = int(rng.integers(P.DEALERS_ASKED[ty][0], P.DEALERS_ASKED[ty][1] + 1))
                r["ty"] = ty
            reqs.sort(key=lambda r: r["hour"])
            for r in reqs:
                b, s, q, ty = r["bond"], r["side"], r["q"], r["ty"]
                ig = bool(seg_ig[b])
                band = "IG" if ig else "HY"
                bk = bucket[b]
                seg = (band, bk, ty)
                h_mkt = P.SCHEDULE_V1[(band, bk)][ty] * P.RIVAL_BASE[band] * stress
                # rivals
                n_riv = min(len(P.DEALERS), r["n"] - 1 if r.get("to_desk", True) else r["n"])
                riv = rng.choice(len(P.DEALERS), n_riv, replace=False, p=P.DEALER_WEIGHT)
                best_r, cover_r = None, None
                rp = []
                for k in riv:
                    dk = P.DEALERS[k]
                    is_large = dk in P.LARGE
                    hk = h_mkt * P.DEALER_AGGR[k] * (1 + P.QUOTE_SD * rng.normal())
                    if r["informed"] and rng.random() < P.DETECT["large" if is_large else "regular"]:
                        hk *= P.WIDEN
                    if rng.random() < P.AXE_P[bk]:
                        hk *= P.AXE_H * (1 + 0.5 * rng.random())
                    hk = max(hk, 0.05)
                    mk_k = large_mark[b] if is_large else mark[b] + rng.normal(0, 0.12 * h_mkt / 100.0)
                    rp.append((mk_k + s * hk / 100.0, dk))        # s = +1 client buys (offer), -1 client sells (bid)
                # the desk
                desk_in = r.get("to_desk", True)
                our = None
                status = None
                passed = False
                if desk_in:
                    h0 = self.schedule_h(t, seg)
                    smult = 1.0
                    for (kind, lim), m in P.SIZE_MULT:
                        if (kind == band and q > lim) or (kind == "ANY" and q < lim):
                            smult = m
                            break
                    lim_ = P.POS_LIMIT[band]
                    skew = 1.0 - P.SKEW * np.clip(pos[b] / lim_, -1, 1) * s     # long and the client buys: tighter
                    dq = max(0.05, h0 * smult * stress * (1 + P.JITTER * np.clip(rng.normal(), -2.5, 2.5)) * skew)
                    our = mark[b] + s * dq / 100.0
                    if (t in outage) or rng.random() < P.PASS_SHARE or abs(pos[b] - s * q) > lim_:
                        passed = True
                quotes = list(rp) + ([] if (our is None or passed) else [(our, "DESK")])
                if not quotes:
                    continue
                quotes.sort(key=lambda x: s * x[0])            # best first: lowest offer, highest bid
                best_p, best_d = quotes[0]
                dist_true = s * (best_p - V[b]) * 100
                trades = r["informed"] or dist_true <= 3.5 * h_mkt + 1.0
                cover_p = quotes[1][0] if len(quotes) > 1 else None
                if desk_in:
                    rid += 1
                    if passed:
                        status = "PASSED"
                    elif not trades:
                        status = "DNT"
                    elif best_d == "DESK":
                        status = "DONE"
                    elif len(quotes) > 1 and quotes[1][1] == "DESK":
                        status = "COVER"
                    else:
                        status = "TRADED_AWAY"
                    best_rival = min([x[0] * s for x in rp]) * s if rp else None
                    req_rows.append(dict(rfq=rid, t=t, hour=r["hour"], client=r["client"], bond=b, side=s, q=q, n=r["n"],
                                         status=status, quote=None if passed else our, ref_mid=mark[b],
                                         done_price=best_p if status == "DONE" else None,
                                         cover=cover_p if status == "DONE" else None, ty=ty, band=band, bucket=bk,
                                         informed=r["informed"], best_rival=best_rival, V=V[b],
                                         h_sched=self.schedule_h(t, seg), stress=stress))
                if trades:
                    ex_h = r["hour"] + rng.uniform(15, 75) / 3600.0
                    print_rows.append(dict(t=t, hour=ex_h, bond=b, price=best_p, q=q, dealer_side=-s, kind="C",
                                           dealer=best_d, rfq=rid if desk_in else None))
                    day_prints[b] += 1
                    if best_d == "DESK":
                        tid += 1
                        pos[b] -= s * q
                        trade_rows.append(dict(trade=tid, t=t, hour=ex_h, bond=b, side=-s, q=q, price=best_p,
                                               cpty="client", client=r["client"], rfq=rid, mark=mark[b], V=V[b]))
            # ---- other customer trades the bond prints (requests not to the desk, voice)
            act = (1 + 0.02 * np.clip(vix_prev - 16, -6, 30)) * mf * dow
            n_other = rng.poisson(B.lam.values * P.OTHER_PRINT_SCALE * act * alive)
            for b in np.where(n_other > 0)[0]:
                band = "IG" if seg_ig[b] else "HY"
                for _ in range(n_other[b]):
                    s = int(rng.choice([-1, 1]))
                    ty = rng.choice(P.CLIENT_TYPES, p=[0.5, 0.12, 0.23, 0.15])
                    hh = P.SCHEDULE_V1[(band, bucket[b])][ty] * stress * rng.uniform(0.5, 1.3)
                    q = float(max(5000, np.round(np.exp(rng.normal(*P.SIZE[ty])) / 5000) * 5000))
                    print_rows.append(dict(t=t, hour=8.0 + (close_h - 8.0) * rng.random(), bond=b,
                                           price=V[b] + s * hh / 100.0, q=q, dealer_side=-s, kind="C", dealer="OTHER",
                                           rfq=None))
                    day_prints[b] += 1
            # ---- the desk sells part of each position to dealers at the close; other dealers trade with each other
            for b in np.where(pos != 0)[0]:
                band = "IG" if seg_ig[b] else "HY"
                bk = bucket[b]
                if rng.random() > P.OFFLOAD[bk]:
                    continue
                qq = abs(pos[b]) if abs(pos[b]) < 2_000_000 else np.round(abs(pos[b]) * rng.uniform(0.5, 1.0) / 1000) * 1000
                if qq <= 0:
                    continue
                side = -np.sign(pos[b])                                 # the desk's side: +1 buys, -1 sells
                px = V[b] + side * P.D2D_HALF[(band, bk)] / 100.0 * rng.uniform(0.7, 1.3)
                tid += 1
                trade_rows.append(dict(trade=tid, t=t, hour=close_h - rng.uniform(0.05, 0.6), bond=b, side=int(side),
                                       q=float(qq), price=px, cpty="dealer", client=None, rfq=None, mark=mark[b], V=V[b]))
                pos[b] += side * qq
                print_rows.append(dict(t=t, hour=trade_rows[-1]["hour"], bond=b, price=px, q=float(qq), dealer_side=0,
                                       kind="D", dealer="DESK", rfq=None))
                day_prints[b] += 1
            n_dd = rng.poisson(0.25 * B.lam.values * alive)
            for b in np.where(n_dd > 0)[0]:
                band = "IG" if seg_ig[b] else "HY"
                for _ in range(n_dd[b]):
                    print_rows.append(dict(t=t, hour=8.0 + (close_h - 8.0) * rng.random(), bond=b,
                                           price=V[b] + rng.normal(0, 0.5) * P.D2D_HALF[(band, bucket[b])] / 100.0,
                                           q=float(np.round(np.exp(rng.normal(14.2, 0.7)) / 1000) * 1000), dealer_side=0,
                                           kind="D", dealer="OTHER", rfq=None))
                    day_prints[b] += 1
            prints_q += day_prints
            # ---- the evaluator's close: the issuer's move from its tradeable bonds' prints, a bond's own share from
            # its own prints
            tradeable = np.isin(bucket, ["liquid", "medium"])
            iss_prints = np.bincount(bi, weights=day_prints * tradeable, minlength=P.N_ISSUERS)
            kI = 1 - (1 - P.EVAL_PRINT_PULL) ** iss_prints * (1 - P.EVAL_ISSUER_DAILY)
            Ihat = Ihat + kI * (self.I[t] - Ihat)
            own = (B.beta.values - 1.0) * self.I[t, bi] + self.e[t]
            kb = 1 - (1 - P.EVAL_PRINT_PULL) ** day_prints * (1 - np.array([P.EVAL_OWN_DAILY[x] for x in bucket]))
            ehat = ehat + kb * (own - ehat)
            esp = self.mkt_spread[t] + Ihat[bi] + ehat
            noise = rng.normal(0, 1, nb) * np.where(seg_ig, P.EVAL_NOISE["IG"], P.EVAL_NOISE["HY"]) / 100.0
            eval_mid[t] = MK.price(self.tsy[t] + esp, cpn, self.mat[t]) + noise
        self.eval_mid = eval_mid
        self.req = pd.DataFrame(req_rows)
        self.trades = pd.DataFrame(trade_rows)
        self.prints = pd.DataFrame(print_rows)
        self.pos_end = pos
