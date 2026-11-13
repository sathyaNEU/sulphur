"""The world behind task20: Hallingvass Kraft AS, a fictional Norwegian hydro generator, its exchange hedge book at a
fictional clearing house (NEX Clearing), its plants and reservoir, its supply customers and the day-ahead market.

History 2017 to 2026 is simulated as the real process; the 2027 replay of 2022 (the liquidity standard's stress year)
is computed here only as the truth the golden (analysis.py, from target/ alone) is checked against."""
import datetime as dt
import math
import numpy as np
import common as C
from common import mi, mi_date, month_hours, hours_year, year_months, cprice

SEED = 7
SEAS = np.array([0.13, 0.11, 0.06, 0.0, -0.08, -0.16, -0.13, -0.09, -0.01, 0.05, 0.10, 0.13])
KAPPA = 4.0

P = dict(
    year_factor={2017: 1.02, 2018: 0.84, 2019: 1.03, 2020: 1.24, 2021: 1.06, 2022: 0.80, 2023: 1.06, 2024: 0.96,
                 2025: 0.84, 2026: 0.66},
    inflow_sd=0.10, res_open=1300.0, res_normal_jan=1300.0, res_floor=700.0, res_cap=2600.0, ror_share=0.26,
    ror_cap=60.0, plan_winter=75.0, plan_spring=40.0, plan_summer=50.0, release_slope=1.2, release_min=0.0,
    release_max=1.30, level0=38.0, kappaL=0.6, sdL=0.006, sdL_crisis=0.012, sdS=0.024, sdS_crisis=0.050,
    sd_spot=0.07, sd_spot_crisis=0.14, hydro_beta=1.6,
    spot_spikes=[(dt.date(2022, 3, 8), dt.date(2022, 4, 8), 0.45), (dt.date(2018, 8, 13), dt.date(2018, 8, 31), 0.25)],
    jumpsS={dt.date(2021, 12, 15): 0.22, dt.date(2021, 12, 16): 0.20, dt.date(2021, 12, 21): 0.18,
            dt.date(2021, 12, 23): -0.30, dt.date(2021, 12, 28): -0.22, dt.date(2022, 3, 7): 0.30,
            dt.date(2022, 3, 9): -0.26, dt.date(2022, 8, 23): 0.10, dt.date(2022, 8, 30): -0.08,
            dt.date(2018, 8, 20): 0.10},
    jumpsL={dt.date(2021, 12, 16): 0.10, dt.date(2021, 12, 21): 0.08, dt.date(2021, 12, 23): -0.12,
            dt.date(2022, 3, 7): 0.08, dt.date(2022, 8, 23): 0.07, dt.date(2022, 8, 30): -0.06},
    knots=[(dt.date(2017, 1, 1), 0.0), (dt.date(2018, 1, 1), 0.0), (dt.date(2018, 5, 1), 0.0),
           (dt.date(2018, 9, 28), 0.28), (dt.date(2019, 3, 29), 0.05), (dt.date(2019, 12, 31), 0.0),
           (dt.date(2020, 1, 31), 0.0), (dt.date(2020, 6, 30), -0.5), (dt.date(2020, 12, 31), -0.1),
           (dt.date(2021, 6, 30), 0.15), (dt.date(2021, 12, 31), 0.40), (dt.date(2022, 3, 15), 0.80),
           (dt.date(2022, 6, 15), 0.85), (dt.date(2022, 8, 26), 1.12), (dt.date(2022, 12, 30), 1.05),
           (dt.date(2023, 6, 30), 0.45), (dt.date(2023, 12, 31), 0.30), (dt.date(2024, 12, 31), 0.18),
           (dt.date(2025, 12, 31), 0.22), (dt.date(2026, 12, 31), 0.25)],
    # the desk and the policy
    ladder=[(0.0, 0.70, 0.90), (1.0, 0.40, 0.60), (2.0, 0.15, 0.35), (3.0, 0.0, 0.10)],
    theta=math.log(1.25), speed=0.03,
    # NEX Clearing's rule
    look=250, q=0.99, band=0.10, review_wd=3,
    # supply
    smelter_mw=100.0, smelter_px={y: (33.0 if y < 2020 else 38.0) for y in range(2010, 2031)},
    pulp_mw=70.0, affiliate_gwh=1800.0, grid_gwh=300.0,
    aff_window=12, aff_lag=2,
    lags={"SMELTER": 38.0, "PULP": 30.0, "AFFILIATE": 50.0, "GRID": 21.0},
    lag_sd={"SMELTER": 3.0, "PULP": 3.0, "AFFILIATE": 4.0, "GRID": 2.0},
    budget_gen=3950.0e3,
)
RETAIL_SHAPE = np.array([1.45, 1.30, 1.15, 0.95, 0.80, 0.70, 0.68, 0.72, 0.85, 1.05, 1.25, 1.40])
LOSS_SHAPE = np.array([1.25, 1.18, 1.08, 0.98, 0.88, 0.82, 0.82, 0.85, 0.92, 1.02, 1.12, 1.22])
CUSTOMERS = ("SMELTER", "PULP", "AFFILIATE", "GRID")


def committed(k):
    """committed supply in MWh per customer for delivery month k."""
    h, m = month_hours(k), k % 12
    return {"SMELTER": P["smelter_mw"] * h, "PULP": P["pulp_mw"] * h,
            "AFFILIATE": P["affiliate_gwh"] * 1e3 * RETAIL_SHAPE[m] / RETAIL_SHAPE.sum(),
            "GRID": P["grid_gwh"] * 1e3 * LOSS_SHAPE[m] / LOSS_SHAPE.sum()}


class World:
    def __init__(self, seed=SEED):
        self.rng = np.random.default_rng(seed)
        self.days = C.business_days(C.Y0, 2026)
        self.didx = {d: i for i, d in enumerate(self.days)}
        self.cdays = [dt.date(C.Y0, 1, 1) + dt.timedelta(days=x) for x in range((dt.date(2026, 12, 31) - dt.date(C.Y0, 1, 1)).days + 1)]
        self.hydro()
        self.market()
        self.budgets()
        self.book()
        self.supply()

    # ------------------------------------------------------------------------------------------ hydrology (weekly)
    @staticmethod
    def normal_week(w):
        x = (w - 1) / 52.0
        return (26 + 8 * math.cos(2 * math.pi * (x - 0.05)) + 205 * math.exp(-((w - 23.5) / 3.6) ** 2)
                + 55 * math.exp(-((w - 41) / 4.5) ** 2) + 70 * math.exp(-((w - 31) / 7.0) ** 2))

    def plan_raw(self, w):
        return P["plan_winter"] if (w <= 13 or w >= 45) else (P["plan_spring"] if w <= 26 else P["plan_summer"])

    def guide(self):
        if hasattr(self, "_guide"):
            return self._guide
        tot_in = sum((1 - P["ror_share"]) * self.normal_week(w) for w in range(1, 53))
        self._scale = tot_in / sum(self.plan_raw(w) for w in range(1, 53))
        lev, g = P["res_normal_jan"], {}
        for _ in range(3):
            for w in range(1, 53):
                lev = lev + (1 - P["ror_share"]) * self.normal_week(w) - self.plan_raw(w) * self._scale
                g[w] = lev
        self._guide = g
        return g

    def plan(self, w):
        self.guide()
        return self.plan_raw(w) * self._scale

    def reservoir(self, inflow, lev0, wnum):
        g = self.guide()
        lev = lev0
        L, O, ROR, REL = [], [], [], []
        for infl, w in zip(inflow, wnum):
            ror = min(P["ror_share"] * infl, P["ror_cap"])
            to_res = infl - P["ror_share"] * infl
            mult = min(max(1 + P["release_slope"] * (lev / g[w] - 1), P["release_min"]), P["release_max"])
            rel = min(self.plan(w) * mult, max(0.0, lev + to_res - P["res_floor"]))
            lev = min(lev + to_res - rel, P["res_cap"])
            L.append(lev); O.append(ror + rel); ROR.append(ror); REL.append(rel)
        return np.array(L), np.array(O), np.array(ROR), np.array(REL)

    def hydro(self):
        rng = self.rng
        self.weeks, d = [], dt.date(2017, 1, 2)
        while d <= dt.date(2026, 12, 31):
            self.weeks.append(d)
            d += dt.timedelta(days=7)
        self.wnum = np.array([min(w.isocalendar()[1], 52) for w in self.weeks])
        self.normal = np.array([self.normal_week(w) for w in self.wnum])
        z, ratio = 0.0, []
        for w in self.weeks:
            z = 0.72 * z + rng.normal(0, P["inflow_sd"])
            ratio.append(P["year_factor"][w.isocalendar()[0] if w.isocalendar()[0] in P["year_factor"] else w.year] * math.exp(z - 0.02))
        self.inflow = self.normal * np.array(ratio)
        self.level, self.output_w, self.ror_w, self.rel_w = self.reservoir(self.inflow, P["res_open"], self.wnum)

    def output_by_day(self, weeks, output_w):
        out = {}
        for i, wk in enumerate(weeks):
            for dd in range(7):
                out[wk + dt.timedelta(days=dd)] = output_w[i] / 7.0 * 1000.0  # MWh
        return out

    # ------------------------------------------------------------------------------------------ market (daily)
    def market(self):
        rng = self.rng
        n = len(self.days)
        kx = np.array([k[0].toordinal() for k in P["knots"]], float)
        ky = np.array([k[1] for k in P["knots"]])
        wk_ord = np.array([w.toordinal() for w in self.weeks])
        g = self.guide()
        L = np.zeros(n); S = np.zeros(n)
        u = s = 0.0
        for i, d in enumerate(self.days):
            crisis = dt.date(2021, 7, 1) <= d <= dt.date(2023, 3, 31)
            u = u * (1 - P["kappaL"] / 252.0) + rng.normal(0, P["sdL_crisis"] if crisis else P["sdL"]) + P["jumpsL"].get(d, 0.0)
            lv = math.log(P["level0"]) + float(np.interp(d.toordinal(), kx, ky)) + u
            w = int(np.searchsorted(wk_ord, d.toordinal(), side="right") - 1)
            dev = (self.level[w] - g[self.wnum[w]]) / P["res_cap"]
            s = s + (KAPPA / 252.0) * (-P["hydro_beta"] * dev - s) + rng.normal(0, P["sdS_crisis"] if crisis else P["sdS"]) + P["jumpsS"].get(d, 0.0)
            L[i] = lv; S[i] = s
        self.L, self.S = L, S
        # spot on every calendar day: the last business day's factors plus a daily noise and the spikes
        spot, eta, bi = {}, 0.0, 0
        for c in self.cdays:
            while bi + 1 < n and self.days[bi + 1] <= c:
                bi += 1
            crisis = dt.date(2021, 7, 1) <= c <= dt.date(2023, 3, 31)
            eta = 0.55 * eta + rng.normal(0, P["sd_spot_crisis"] if crisis else P["sd_spot"])
            for a, b, amp in P["spot_spikes"]:
                if a <= c <= b:
                    eta += amp * 0.45
            spot[c] = math.exp(SEAS[c.month - 1] + L[bi] + S[bi] + eta)
        self.spot = spot
        self.curves = []
        for i, d in enumerate(self.days):
            k0 = mi(d.year, d.month)
            self.curves.append({k: self.fwd(i, k) for k in range(k0, k0 + 65)})

    def fwd(self, i, k):
        d = self.days[i]
        tau = max((mi_date(k) - d).days, 0) / 365.0
        return math.exp(SEAS[k % 12] + self.L[i] + math.exp(-KAPPA * tau) * self.S[i])

    # ------------------------------------------------------------------------------------------ budgets
    def budgets(self):
        """budget price and generation per delivery year, set on the first business day of October for y+1..y+4."""
        self.bud = []  # (set_on, year, price, generation MWh)
        rng = np.random.default_rng(91)
        for Y in range(2016, 2027):
            if Y < 2017:
                set_on = self.days[0]
                idx = list(range(60))
            else:
                set_on = next(d for d in self.days if d >= dt.date(Y, 10, 1))
                idx = [i for i, d in enumerate(self.days) if d < dt.date(Y, 10, 1)][-60:]
            for y in range(Y + 1, Y + 5):
                ks = year_months(y)
                vals = [cprice(self.curves[i], ks) for i in idx if all(k in self.curves[i] for k in ks)]
                if vals:
                    gen = P["budget_gen"] * (1 + rng.normal(0, 0.004))
                    self.bud.append((set_on, y, round(0.92 * float(np.mean(vals)), 2), round(gen / 1e3) * 1e3))

    def budget_px(self, d, y):
        best = None
        for (s, yy, px, g) in self.bud:
            if yy == y and s <= d and (best is None or s > best[0]):
                best = (s, px)
        return best[1]

    def budget_gen(self, d, y):
        best = None
        for (s, yy, px, g) in self.bud:
            if yy == y and s <= d and (best is None or s > best[0]):
                best = (s, g)
        return best[1]

    @staticmethod
    def fixed_phys(y):
        return P["smelter_mw"] * hours_year(y) if 2020 <= y <= 2029 else 0.0

    # ------------------------------------------------------------------------------------------ the book (history)
    def book(self):
        self.ref_px, self.ref_ret = C.ref_series(self.days, self.curves)
        self.rates, self.notices = C.rule_rates(self.days, self.ref_px, self.ref_ret, P["look"], P["q"], P["band"],
                                                P["review_wd"])
        d0 = self.days[0]
        mw0 = {}
        for j, h in ((0, 0.72), (1, 0.42), (2, 0.15)):
            y = d0.year + j
            exch = h * P["budget_gen"] - self.fixed_phys(y)
            m = math.floor(max(exch, 0.0) / hours_year(y))
            for k in year_months(y):
                if m > 0:
                    mw0[k] = -m
        self.mw0 = mw0
        self.desk = C.make_desk(P["ladder"], self.budget_px, self.budget_gen, self.fixed_phys, "step", P["theta"], P["speed"])
        self.res = C.run_book(self.days, self.curves, self.spot, self.rates, mw0, self.desk)

    # ------------------------------------------------------------------------------------------ supply and day-ahead
    def supply(self):
        self.out_day = self.output_by_day(self.weeks, self.output_w)
        spm = {}
        for c, v in self.spot.items():
            spm.setdefault(mi(c.year, c.month), []).append(v)
        self.spot_m = {k: float(np.mean(v)) for k, v in spm.items()}
        # invoices for each month's committed supply and the day each customer actually paid
        rng = np.random.default_rng(55)
        self.invoices = []
        for k in range(mi(2018, 1), mi(2026, 12) + 1):
            com = committed(k)
            inv = invoice_date(k)
            for cu in CUSTOMERS:
                px = customer_price(cu, k, self.spot_m)
                lag = P["lags"][cu] + rng.normal(0, P["lag_sd"][cu])
                self.invoices.append(dict(cu=cu, k=k, doc=inv, mwh=com[cu], px=px, amt=com[cu] * px,
                                          pay=pay_date(inv, lag)))


def affiliate_price(spot_m, k, window, lag):
    return float(np.mean([spot_m[x] for x in range(k - lag - window + 1, k - lag + 1) if x in spot_m]))


def invoice_date(k):
    d, cnt = mi_date(k + 1), 0
    while True:
        if C.is_bday(d):
            cnt += 1
            if cnt == 3:
                return d
        d += dt.timedelta(days=1)


def pay_date(inv, lag_days):
    d = inv + dt.timedelta(days=int(round(lag_days)))
    while not C.is_bday(d):
        d += dt.timedelta(days=1)
    return d


def customer_price(cu, k, spot_m, window=None, lag=None, aff_formula=True):
    y = mi_date(k).year
    if cu == "SMELTER":
        return P["smelter_px"][y]
    if cu == "AFFILIATE" and aff_formula:
        return affiliate_price(spot_m, k, window or P["aff_window"], P["aff_lag"] if lag is None else lag)
    return spot_m[k]


# ---------------------------------------------------------------------------------------------------- the 2027 truth
def replay_truth(W, rule="step", rates_kind="rule", out_kind="res", aff_formula=True, count_phys=True):
    """the standard's stress year on the 2027 book, as the world would run it."""
    days27 = C.business_days(2027, 2027)
    d22 = [max(d for d in W.days if d <= dt.date(2022, x.month, min(x.day, 28) if x.month == 2 else x.day)) for x in days27]
    prev22 = max(d for d in W.days if d <= dt.date(2021, 12, 31))
    F = dict(W.curves[-1])
    curves = []
    prev_i = W.didx[prev22]
    for t, d in enumerate(days27):
        i22 = W.didx[d22[t]]
        k_now = mi(d.year, d.month)
        F = {k: (f * W.curves[i22][k - 60] / W.curves[prev_i][k - 60] if (k - 60) in W.curves[i22] and (k - 60) in W.curves[prev_i] else f)
             for k, f in F.items() if k >= k_now}
        curves.append(dict(F))
        prev_i = i22
    # spot on calendar days of 2027 (and the last days of 2026 from history)
    spot = dict(W.spot)
    bi = 0
    c = dt.date(2027, 1, 1)
    while c.year == 2027:
        while bi + 1 < len(days27) and days27[bi + 1] <= c:
            bi += 1
        b = days27[bi] if days27[bi] <= c else None
        c22 = dt.date(2022, c.month, min(c.day, 28) if c.month == 2 else c.day)
        i22b = W.didx[max(d for d in W.days if d <= c22)]
        k22 = mi(c22.year, c22.month) + 1
        if b is None:
            fwd27 = W.curves[-1][mi(2027, 1)]  # 1 to 3 January: the opening curve's January
            fwd27 = W.curves[-1][mi(2027, 2)]
        else:
            fwd27 = curves[bi][mi(c.year, c.month) + 1]
        spot[c] = fwd27 * W.spot[c22] / W.curves[i22b][k22]
        c += dt.timedelta(days=1)
    return dict(days=days27, curves=curves, spot=spot, d22=d22)


# ---------------------------------------------------------------------------------------------------- the truth
import replay as RP


def open_state(W):
    rec_open = [(x["pay"], x["amt"]) for x in W.invoices if x["pay"].year == 2027]
    return dict(mw=W.res["mw"], open_curve=W.curves[-1], im0=float(W.res["im"][-1]), f_last=W.res["f_last"],
                spot_hist=W.spot, rates_in_force={t: float(W.rates[t][-1]) for t in "MQY"},
                hist_two={t: W.rates[t + "_two"] for t in "MQY"}, last1={t: W.rates[t + "_last1"] for t in "MQY"},
                level=float(W.level[-1]), rec_open=rec_open, spot_m=dict(W.spot_m))


def truth_models(W, desk_rule="step", rates_kind="rule", out_kind="res", aff_formula=True, count_phys=True):
    def rates(days, curves, st):
        px, ret = C.ref_series(days, curves, st["open_curve"])
        if rates_kind == "rule":
            r, _ = C.rule_rates(days, px, ret, P["look"], P["q"], P["band"], P["review_wd"], st["rates_in_force"],
                                st["hist_two"], st["last1"])
            return r
        if rates_kind == "const":
            return {t: np.full(len(days), st["rates_in_force"][t]) for t in "MQY"}
        if rates_kind == "price":
            p0 = {t: cprice(st["open_curve"], C.front_months(W.days[-1])[t]) for t in "MQY"}
            return {t: st["rates_in_force"][t] * px[t] / p0[t] for t in "MQY"}
        if rates_kind == "ewma":
            out = {}
            for t in "MQY":
                v = float(np.var(W.ref_ret[t][-250:]))
                ser = []
                for j in range(len(days)):
                    v = 0.94 * v + 0.06 * ret[t][j] ** 2
                    ser.append(2.576 * math.sqrt(2) * math.sqrt(v) * px[t][j])
                out[t] = np.array(ser)
            return out
        if rates_kind in ("ewma_cal", "ewma_cal97"):
            lam = 0.94 if rates_kind == "ewma_cal" else 0.97
            out = {}
            for t in "MQY":
                # calibrate k on history: rate = k * sigma_ewma * price
                v = float(np.var(W.ref_ret[t][:60])); sig = []
                for x in W.ref_ret[t]:
                    v = lam * v + (1 - lam) * x ** 2
                    sig.append(math.sqrt(v))
                sig = np.array(sig)
                sel = slice(250, None)
                kfit = float(np.exp(np.mean(np.log(W.rates[t][sel] / (sig[sel] * W.ref_px[t][sel])))))
                v = sig[-1] ** 2
                ser = []
                for j in range(len(days)):
                    v = lam * v + (1 - lam) * ret[t][j] ** 2
                    ser.append(kfit * math.sqrt(v) * px[t][j])
                out[t] = np.array(ser)
            return out
        if rates_kind == "pct2022":
            out = {}
            for t in "MQY":
                ser = []
                for j, d in enumerate(days):
                    c22 = RP.corresponding_2022(d, set(W.days))
                    i22 = W.didx[c22]
                    ser.append(px[t][j] * W.rates[t][i22] / W.ref_px[t][i22])
                out[t] = np.array(ser)
            return out
        raise ValueError(rates_kind)

    def desk(days, curves, st):
        bud = list(W.bud)
        oct1 = dt.date(2027, 10, 1)
        idx = [j for j, d in enumerate(days) if d < oct1][-60:]
        set_on = next(d for d in days if d >= oct1)
        for y in range(2028, 2032):
            ks = year_months(y)
            vals = [cprice(curves[j], ks) for j in idx if all(k in curves[j] for k in ks)]
            if vals:
                bud.append((set_on, y, round(0.92 * float(np.mean(vals)), 2), P["budget_gen"]))

        def bpx(d, y):
            return max(((s, px) for (s, yy, px, g) in bud if yy == y and s <= d), key=lambda x: x[0])[1]

        def bgen(d, y):
            return max(((s, g) for (s, yy, px, g) in bud if yy == y and s <= d), key=lambda x: x[0])[1]
        fp = W.fixed_phys if count_phys else (lambda y: 0.0)
        return C.make_desk(P["ladder"], bpx, bgen, fp, desk_rule, P["theta"], P["speed"])

    def supply(days, curves, spot_all, st):
        weeks, infl = RP.stress_inflows(W.normal_week, {w.isocalendar()[1]: W.inflow[i] for i, w in enumerate(W.weeks) if w.isocalendar()[0] == 2022},
                                        {w.isocalendar()[1]: W.normal[i] for i, w in enumerate(W.weeks) if w.isocalendar()[0] == 2022})
        wn = np.array([min(w.isocalendar()[1], 52) for w in weeks])
        lev, outw, _, _ = W.reservoir(infl, st["level"], wn)
        if out_kind != "res":
            # budget output by week (normal inflows from a normal level), and the shortcuts built on it
            nlev, nout, _, _ = W.reservoir(np.array([W.normal_week(n) for n in wn]), W.guide()[52], wn)
            if out_kind == "budget":
                outw = nout
            elif out_kind == "inflow":
                outw = nout * infl / np.array([W.normal_week(n) for n in wn])
            elif out_kind == "ratio22":
                o22 = {w.isocalendar()[1]: W.output_w[i] for i, w in enumerate(W.weeks) if w.isocalendar()[0] == 2022}
                outw = np.array([nout[i] * o22[n] / nout_n for i, (n, nout_n) in enumerate(zip(wn, nout))])
                # 2022's output relative to the same normal output
            else:
                raise ValueError(out_kind)
        out_day = dict(W.out_day)
        for i, wk in enumerate(weeks):
            for dd in range(7):
                out_day[wk + dt.timedelta(days=dd)] = outw[i] / 7.0 * 1000.0
        spm = dict(st["spot_m"])
        acc = {}
        for c, v in spot_all.items():
            if c.year == 2027:
                acc.setdefault(mi(c.year, c.month), []).append(v)
        spm.update({k: float(np.mean(v)) for k, v in acc.items()})
        com_day = {}
        c = dt.date(2026, 12, 1)
        while c <= dt.date(2027, 12, 31):
            k = mi(c.year, c.month)
            com_day[c] = sum(committed(k).values()) / C.month_days(k)
            c += dt.timedelta(days=1)
        invoices = [x for x in st["rec_open"]]
        for k in range(mi(2027, 1), mi(2027, 12) + 1):
            com = committed(k)
            for cu in CUSTOMERS:
                invoices.append((pay_date(invoice_date(k), P["lags"][cu]), com[cu] * customer_price(cu, k, spm, aff_formula=aff_formula)))
        return out_day, com_day, invoices

    return dict(rates=rates, desk=desk, supply=supply)


def truth(W=None, **kw):
    W = W or World()
    st = open_state(W)
    days22 = [d for d in W.days if d.year == 2022 or d == max(x for x in W.days if x.year == 2021)]
    curves22 = {d: W.curves[W.didx[d]] for d in days22}
    prices = RP.stress_prices(W.curves[-1], curves22, W.spot, sorted(curves22))
    return RP.run(st, prices, truth_models(W, **kw)), W


if __name__ == "__main__":
    r, W = truth()
    j = r["j"]
    print("truth peak %.1f m on %s  VM %.1f DLV %.1f dIM %.1f DA %.1f REC %.1f" % (
        r["peak"] / 1e6, r["peak_day"], r["vm"][:j + 1].sum() / 1e6, r["dlv"][:j + 1].sum() / 1e6,
        r["dim"][:j + 1].sum() / 1e6, r["da"][:j + 1].sum() / 1e6, r["rec"][:j + 1].sum() / 1e6))
    for kw in (dict(desk_rule="min"), dict(desk_rule="max_now"), dict(desk_rule="frozen"), dict(desk_rule="linear"),
               dict(rates_kind="const"), dict(rates_kind="price"), dict(rates_kind="ewma"), dict(rates_kind="ewma_cal"), dict(rates_kind="ewma_cal97"), dict(rates_kind="pct2022"),
               dict(out_kind="budget"), dict(out_kind="ratio22"), dict(out_kind="inflow"),
               dict(aff_formula=False), dict(count_phys=False)):
        x, _ = truth(W, **kw)
        print("  ", kw, "%.1f (%+.1f%%)" % (x["peak"] / 1e6, 100 * (x["peak"] / r["peak"] - 1)))
