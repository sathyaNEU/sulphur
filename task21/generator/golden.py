"""The golden: every graded figure computed from target/ alone through methods.py.

    python3 golden.py            prints the figures
    golden.compute(target)       returns them (figures.json, the deliverables and the checks read this)
"""
import datetime as dt
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import methods as M  # noqa: E402

PROPOSAL_U25 = 0.21        # the pricing team's under-25 rise (the prompt)
PROPOSAL_O65 = -0.03       # the over-65 cut (the prompt)
V7_FROM = dt.date(2026, 2, 1)       # HPM v7, deployed with the last rate change


def prepare(target):
    D = M.load(target)
    cdf_inc = M.cdfs(D["tri"], "incurred")
    cdf_cnt = M.cdfs(D["tri"], "notified")
    D["pattern"] = M.report_pattern(D["clm"])
    D["clm_dev"] = M.developed(D["clm"], D["pattern"])
    D["expo"] = M.month_exposure(D["pol"])
    D["s_cost"] = M.seasonal_factors(D["pol"], D["clm_dev"], D["expo"], "cost")
    D["s_cnt"] = M.seasonal_factors(D["pol"], D["clm_dev"], D["expo"], "count")
    D["sales"] = M.sales_frame(D["feeds"], D["pol"])
    D["af"] = M.ae_frame(D["pol"], D["clm_dev"], D["expo"], D["s_cnt"], D["sales"])
    D["cdf_inc"], D["cdf_cnt"] = cdf_inc, cdf_cnt
    return D


def current_mask(D, seg):
    cur_refs = set(D["sales"][(D["sales"].seg == seg) & (D["sales"].date >= M.CURRENT_FROM)].quote_reference)
    return D["pol"].quote_reference.isin(cur_refs).values


def segment(D, seg, curve_form="loglinear", pool_from=None, seasonal=True):
    pol = D["pol"]
    base = M.base_lr(pol, D["clm_dev"], D["expo"], D["s_cost"], current_mask(D, seg), seasonal=seasonal)
    af = D["af"][D["af"].seg == seg]
    if pool_from is None:
        pool_from = V7_FROM if seg == "mid" else dt.date(2025, 1, 1)
    curve, info = M.gap_curve(af[af.date >= pool_from], curve_form)
    conv = M.conversion_by_rank(D["feeds"], seg)
    cur = D["sales"][(D["sales"].seg == seg) & (D["sales"].date >= M.CURRENT_FROM)]
    fn = lambda L: M.lr_2027(base, cur, curve, conv, L)
    return dict(base=base, curve=curve, info=info, conv=conv, cur=cur, lr=fn)


def o65_cut(D, S, L=PROPOSAL_O65, slope_mult=1.0):
    """2027 underwriting profit with the cut against without it: comparison-site new business replayed (every
    quote since 1 February 2026 at its weight), and the renewal book its lower equivalent new-business price caps."""
    feeds, comm = D["feeds"], D["comm"]
    f = feeds[(feeds.seg == "o65") & (feeds.date >= M.CURRENT_FROM)]
    cur = S["cur"]
    load = np.median(cur.written_premium_gbp.values / cur.risk_premium_gbp.values)
    k = S["base"] * cur.written_premium_gbp.sum() / (cur.risk_premium_gbp.values * S["curve"](cur.gap.values)).sum()

    def nb(Lx):
        rk = M.new_rank(f.gross.values, f.r1.values, f.r2.values, f.r3.values, Lx)
        pr = np.array([S["conv"][x] for x in rk]) * f.w.values * M.SCALE
        net = f.gross.values / 1.12
        claims = net / load * S["curve"](f.gap.values) * k * (1 + M.INFL)
        com = np.array([comm[s] for s in f.site])
        return (pr * (net * (1 + Lx) - claims - com - M.SERVICING)).sum()

    ren = D["ren"]
    ret = D["ret"]
    x, y, n = ret["mid"].values, ret["Retention"].values, ret["Invitations"].values
    ok = (y > 0) & (y < 1) & (n >= 30)
    A = np.polyfit(x[ok], np.log(y[ok] / (1 - y[ok])), 1, w=np.sqrt(n[ok]))
    A = np.array([A[0] * slope_mult, A[1]])
    retention = lambda dp: 1 / (1 + np.exp(-np.polyval(A, dp)))

    def renewals(Lx):
        off = np.minimum(ren.intended_renewal_premium_ex_ipt_gbp.values, ren.enbp_ex_ipt_at_current_nb_rates_gbp.values * (1 + Lx))
        dp = off / ren.current_premium_ex_ipt_gbp.values - 1
        r = retention(dp)
        return (r * (off - ren.renewal_risk_premium_2027_gbp.values - M.SERVICING)).sum(), r.mean()

    nb0, nb1 = nb(0.0), nb(L)
    (rp0, rt0), (rp1, rt1) = renewals(0.0), renewals(L)
    return dict(nb=nb1 - nb0, ren=rp1 - rp0, net=nb1 - nb0 + rp1 - rp0, ret0=rt0, ret1=rt1, slope=A[0],
                nb0=nb0, nb1=nb1, rp0=rp0, rp1=rp1)


def lr_range(D, S, L, draws=1500, seed=20271):
    """80 per cent range of the segment's 2027 loss ratio at change L: the year's policies (the replayed book at its
    expected count) each drawing its claims, numbers from its expected frequency and costs from the segment's own
    developed capped claims."""
    rng = np.random.default_rng(seed)
    cur = S["cur"]
    r0 = np.minimum(cur.pos.values, 4)
    r1_ = M.new_rank(cur.gross.values, cur.r1.values, cur.r2.values, cur.r3.values, L)
    v = np.array([S["conv"][x] for x in r1_]) / np.array([S["conv"][x] for x in r0])
    n_pol = int(round(M.volumes(D["feeds"], cur.seg.iloc[0], S["conv"], L)[0]))
    p = v / v.sum()
    seg = cur.seg.iloc[0]
    sev = D["clm_dev"][D["clm_dev"].policy_number.isin(set(D["sales"][D["sales"].seg == seg].policy_number))]
    sev = sev[sev.capped > 0].capped.values * (1 + M.INFL)
    exp_lr = S["lr"](L)
    lam = cur.predicted_claim_frequency.values * S["curve"](cur.gap.values)
    prem = cur.written_premium_gbp.values * (1 + L)
    # scale expected claims so the draws centre on the expected loss ratio
    out = np.empty(draws)
    for d in range(draws):
        idx = rng.choice(len(cur), n_pol, p=p)
        nclm = rng.poisson(lam[idx]).sum()
        out[d] = rng.choice(sev, nclm).sum() / prem[idx].sum()
    out = out / out.mean() * exp_lr
    return np.quantile(out, 0.10), np.quantile(out, 0.90)


def r1_table(D):
    f = D["feeds"][(D["feeds"].date >= dt.date(2026, 1, 1))]
    out = {}
    for seg in M.SEGS:
        g = f[f.seg == seg]
        q = g.w.sum()
        s = (g.w == 1).sum()
        out[seg] = (int(q), int(s), s / q)
    return out


def compute(target):
    D = prepare(target)
    S = {g: segment(D, g) for g in M.SEGS}
    out = dict(D=D, S=S)
    out["u25_lr_at_proposal"] = S["u25"]["lr"](PROPOSAL_U25)
    out["u25_rise"] = M.smallest_change(S["u25"]["lr"])
    out["mid_rise"] = M.smallest_change(S["mid"]["lr"])
    out["cut"] = o65_cut(D, S["o65"])
    for g, L in (("u25", out["u25_rise"] / 100.0), ("mid", out["mid_rise"] / 100.0)):
        out[g + "_lr_at_rise"] = S[g]["lr"](L)
        out[g + "_vol_at_rise"] = M.volumes(D["feeds"], g, S[g]["conv"], L)
    out["vol_u25_proposal"] = M.volumes(D["feeds"], "u25", S["u25"]["conv"], PROPOSAL_U25)
    out["vol_o65_proposal"] = M.volumes(D["feeds"], "o65", S["o65"]["conv"], PROPOSAL_O65)
    out["vol_o65_hold"] = M.volumes(D["feeds"], "o65", S["o65"]["conv"], 0.0)
    out["mid_range"] = lr_range(D, S["mid"], out["mid_rise"] / 100.0)
    out["r1"] = r1_table(D)
    return out


if __name__ == "__main__":
    t = sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(HERE), "target")
    G = compute(t)
    S = G["S"]
    for g in M.SEGS:
        print(g, "base %.3f slope %.2f conv %s" % (S[g]["base"], S[g]["info"].get("slope", 0),
                                                  {k: round(v, 4) for k, v in S[g]["conv"].items()}))
    print("u25 LR at the proposal: %.3f  u25 rise %+d  mid rise %+d" % (G["u25_lr_at_proposal"], G["u25_rise"], G["mid_rise"]))
    print("u25 at rise: LR %.3f vol %.0f prem %.0f | mid at rise: LR %.3f vol %.0f prem %.0f" % (
        G["u25_lr_at_rise"], *G["u25_vol_at_rise"], G["mid_lr_at_rise"], *G["mid_vol_at_rise"]))
    print("volumes at proposals: u25 %.0f, o65 -3 %.0f (hold %.0f)" % (G["vol_u25_proposal"][0],
                                                                      G["vol_o65_proposal"][0], G["vol_o65_hold"][0]))
    c = G["cut"]
    print("o65 cut: NB %+.0f renewals %+.0f net %+.0f (retention %.4f -> %.4f, slope %.2f)" % (
        c["nb"], c["ren"], c["net"], c["ret0"], c["ret1"], c["slope"]))
    print("mid 80%% range at the rise: %.3f to %.3f" % G["mid_range"])


# ---- the rival family, run on the pack (bands and forcing) -----------------------------------------------------------
def onlevel_factors(D):
    if "_onl" in D:
        return D["_onl"]
    rates = D["rates"]

    def rf(seg, d):
        f = 1.0
        for _, r in rates[rates.seg == seg].iterrows():
            if d >= r["Effective"]:
                f *= 1 + r["Change to new-business rates"]
        return f
    qd = dict(zip(D["sales"].policy_number, D["sales"].date))
    pol = D["pol"]
    cur = {g: rf(g, dt.date(2026, 10, 1)) for g in M.SEGS}
    dates = [qd.get(p) for p in pol.policy_number]
    memo = {}
    f = []
    for s, d in zip(pol.seg, dates):
        if d is None:
            f.append(1.0)
            continue
        if (s, d) not in memo:
            memo[(s, d)] = cur[s] / rf(s, d)
        f.append(memo[(s, d)])
    D["_onl"] = (np.array(f), dates)
    return D["_onl"]


def seasons(D, dev="extract"):
    """The readings of the claims seasons a careful analyst could defend, from either development: claims cost per
    unit of earned premium over 2025 and 2026 (the golden's), claims per vehicle-year, cost over 2025 alone, and a
    two-harmonic smoothing of the first."""
    key = "_seasons_" + dev
    if key in D:
        return D[key]
    if dev != "extract" and "_cl" not in D:
        D["_cl"] = M.developed_cl(D["clm"], D["cdf_inc"], D["cdf_cnt"])
    clm = D["clm_dev"] if dev == "extract" else D["_cl"]
    pol, ex = D["pol"], D["expo"]
    cost = M.seasonal_factors(pol, clm, ex, "cost")
    m = np.arange(12)
    X = np.column_stack([np.ones(12), np.cos(2 * np.pi * m / 12), np.sin(2 * np.pi * m / 12),
                         np.cos(4 * np.pi * m / 12), np.sin(4 * np.pi * m / 12)])
    sm = np.exp(X @ np.linalg.lstsq(X, np.log(cost), rcond=None)[0])
    D[key] = {"cost": cost, "count": M.seasonal_factors(pol, clm, ex, "count"),
              "cost2025": M.seasonal_factors(pol, clm, ex, "cost", last=dt.date(2025, 12, 1)),
              "smooth": sm / sm.mean()}
    return D[key]


def base_variant(D, seg, window="current", dev="extract", seasonal=True, sv=None):
    pol = D["pol"]
    onl, dates = onlevel_factors(D)
    if dev != "extract" and "_cl" not in D:
        D["_cl"] = M.developed_cl(D["clm"], D["cdf_inc"], D["cdf_cnt"])
    clm = D["clm_dev"] if dev == "extract" else D["_cl"]
    cost, _ = M.claims_by_policy(pol, clm)
    s = (pol.seg == seg).values & np.array([d is not None for d in dates])
    start = {"current": M.CURRENT_FROM, "v7": V7_FROM, "pooled": dt.date(2025, 1, 1)}[window]
    m = s & np.array([d is not None and d >= start for d in dates])
    sv = D["s_cost"] if sv is None else sv
    w = np.array([sv[mm.month - 1] for mm in M.MONTHS]) if seasonal else np.ones(len(M.MONTHS))
    ep = D["expo"][m] * (pol.written_premium_gbp.values[m] * onl[m])[:, None]
    return cost[m].sum() / (ep * w[None, :]).sum()


def own_claims_lr(D, S, seg, L):
    """The rival that reads no curve: the current sold book reweighted by its conversion at the new rank, each
    policy's own developed claims per unit of its seasonally weighted earned premium."""
    cur = S[seg]["cur"]
    pol = D["pol"]
    pidx = dict(zip(pol.policy_number, range(len(pol))))
    j = np.array([pidx[p] for p in cur.policy_number])
    cost, _ = M.claims_by_policy(pol, D["clm_dev"])
    w = np.array([D["s_cost"][mm.month - 1] for mm in M.MONTHS])
    epw = (D["expo"][j] * pol.written_premium_gbp.values[j][:, None] * w[None, :]).sum(1)
    r0 = np.minimum(cur.pos.values, 4)
    rk = M.new_rank(cur.gross.values, cur.r1.values, cur.r2.values, cur.r3.values, L)
    v = np.array([S[seg]["conv"][x] for x in rk]) / np.array([S[seg]["conv"][x] for x in r0])
    return (v * cost[j]).sum() / (v * epw).sum() * (1 + M.INFL) / (1 + L)


def family(D, S, seg):
    """Every defensible construction of the segment's 2027 loss ratio function: the business written at the rates in
    force (for 25-to-64s, all the business HPM v7 has priced) and, for under-25s (whose frequency model v7 carried
    over), also the latest twelve months on level;
    each under either development and each reading of the gap curve. All of 2025 and 2026 on level is not one: it
    spans the March 2025 and February 2026 rate changes and the market's own move, and bringing it on level by the
    rate changes assumes the won book's risk does not move with its price, which the gap curve refutes. The decile
    means are read as a step only where they fall with the gap (no reversal over 0.05); where the selection is small
    against their noise, as for the 25-to-64s, a step reading of them reads the noise."""
    af = D["af"][D["af"].seg == seg]
    pool = V7_FROM if seg == "mid" else dt.date(2025, 1, 1)
    curves = {"loglinear": M.gap_curve(af[af.date >= pool], "loglinear")[0],
              "poisson": M.gap_curve(af[af.date >= pool], "poisson")[0]}
    if seg != "mid":           # for 25-to-64s the golden's own curve is already HPM v7's 2026 sales
        curves["loglinear_2026"] = M.gap_curve(af[af.date >= dt.date(2026, 1, 1)], "loglinear")[0]
    step, info = M.gap_curve(af[af.date >= pool], "deciles")
    if np.diff(info["y"]).max() <= 0.05:
        curves["deciles"] = step
    cur, conv = S[seg]["cur"], S[seg]["conv"]
    out = {}
    for dv in ("extract", "chainladder"):
        bases = {"current/" + sn: base_variant(D, seg, "current", dv, True, sv) for sn, sv in seasons(D, dv).items()}
        if seg != "mid":
            bases["latest12"] = latest12(D, seg, dv)
        for bn, b in bases.items():
            for cn, cv in curves.items():
                out["%s/%s/%s" % (bn, dv, cn)] = (lambda L, b=b, cv=cv: M.lr_2027(b, cur, cv, conv, L))
    return out


def shortcuts(D, S, seg):
    """The hurried constructions, each a loss-ratio function of the change, under either development."""
    t = lambda b: (lambda L, b=b: b * (1 + M.INFL) / (1 + L))
    out = {}
    for dv, tag in (("extract", ""), ("chainladder", ", triangles' development")):
        out["loss-ratio method, current book completed" + tag] = t(base_variant(D, seg, "current", dv, True))
        out["loss-ratio method, latest twelve months" + tag] = t(latest12(D, seg, dv))
        out["loss-ratio method, 2026 to date" + tag] = t(base_variant(D, seg, "current", dv, False))
        out["loss-ratio method, 2025 and 2026 pooled" + tag] = t(base_variant(D, seg, "pooled", dv, False))
    return out


def latest12(D, seg, dev="extract"):
    pol = D["pol"]
    onl, dates = onlevel_factors(D)
    m = (pol.seg == seg).values & np.array([d is not None for d in dates])
    last = np.array([mm >= dt.date(2025, 11, 1) for mm in M.MONTHS])
    if dev != "extract" and "_cl" not in D:
        D["_cl"] = M.developed_cl(D["clm"], D["cdf_inc"], D["cdf_cnt"])
    cd = D["clm_dev"] if dev == "extract" else D["_cl"]
    pn = set(pol.policy_number[m])
    sel = cd.policy_number.isin(pn).values & np.array([a >= dt.date(2025, 11, 1) for a in cd.accident_date])
    ep = (D["expo"][m][:, last] * (pol.written_premium_gbp.values[m] * onl[m])[:, None]).sum()
    return cd.dev_cost.values[sel].sum() / ep
