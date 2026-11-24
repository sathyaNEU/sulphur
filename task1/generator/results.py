"""Every owed figure, computed on the shipped files: figures.json (what the answer blocks and the goldens state)
and effort.json (each result's golden, band and the three passes, the stump factorial, the run routes, the forcing
on both sides), with the core's rubric table re-priced on the cut pack by corelib on the ranges the blocks state."""
import datetime as dt
import math
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(REPO, ".claude", "skills", "stumping"))
import core as C  # noqa: E402
import analysis as A  # noqa: E402
import corelib  # noqa: E402
import effort as EF  # noqa: E402

MEM = C.MEMBERS
KEYS = ["S1", "S2", "S3", "S1+S2", "S1+S3", "S2+S3", "S1+S2+S3"]
# each stump made the way the runs of record made it (core.HURRIED)
LOST = {"S1": "the billing records taken as they stand",
        "S2": "the declined installs' revenue per payer carried at the shift the fully named channels show",
        "S3": "the plan's billed spend read as a budget billed in full"}
ROUTE_NAME = {k: "; ".join(LOST[s] for s in k.split("+")) for k in KEYS}
FAM_KEY = {"return ": "return_plan", "payments per 100 ": "pay100"}
PLAN_KEY = {"installs the plan buys": "plan_installs", "revenue the plan's installs bring": "plan_revenue"}
ANDROID = [c for c in MEM if not C.CH[c]["ios"]]
IOS = [c for c in MEM if C.CH[c]["ios"]]
STORE = ((0, "Google Play"), (1, "App Store"))
BAND_PAD, BESIDE_PAD = C.BAND_PAD, C.BESIDE_PAD                    # the stated ranges' rule lives in the core
FPOINT = 1.95                                                      # the five per cent point of F on 8 and 789
CHI = {1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07, 6: 12.59}     # the five per cent points
unit, band_of = C.unit, C.band_of
OWN = C.OWN                                                        # the channel each stump opens
_KEEP = []                                                         # arrays the core caches by id() stay alive


def stated(fid, x):
    nd = unit(fid)
    return int(round(float(x), nd)) if nd <= 0 else round(float(x), nd)


def call_of(res):
    return sorted("%s: %s" % (c, C.band(res[c]["roas"])) for c in MEM)


def plan_of(res):
    return {"installs": stated("installs the plan buys", res["plan"][0]),
            "revenue": stated("revenue the plan's installs bring", res["plan"][1])}


# ----------------------------------------------------------------------------------------------------------------
# the checks the blocks quote: each a figure from the shipped files
# ----------------------------------------------------------------------------------------------------------------

def store_block(O, fits):
    """each store's charges against the records, the candidates, the fit, and what each other continuation takes in"""
    out = {}
    wq = lambda q: q ** np.arange(1, C.K + 1)
    webq = float(C.s1_web_fit(O))
    for pl, name in STORE:
        f = fits[pl]
        mk = (O.ios == bool(pl)) & ~O.web
        use = f["use"]
        fitted = lambda q: wq(q) @ f["Mr"] + f["c_m"] * (wq(q) @ f["Mf"])
        seen = float(C.s1_seen_rate(O, pl))
        rival = {}
        for key, q in (("fitted", f["q"]), ("web", webq), ("seen", seen)):
            y = fitted(q)
            rival[key] = dict(rate=round(float(q), 3), takes_in=int(round(float(y[use].sum()))),
                              period_error=int(round(float(np.abs(y - f["R"])[use].mean()))))
        out[name] = dict(
            trial_end_share_monthly=round(f["c_m"], 3), trial_end_share_annual=round(f["c_a"], 3),
            continuation=round(f["q"], 3), first_excess=int(round(f["F"].sum())),
            renewal_excess=int(round(f["R"].sum())), renewal_excess_fitted_periods=int(round(float(f["R"][use].sum()))),
            annual_excess=int(round(f["A"].sum())),
            trial_candidates_monthly=f["first_candidates"], trial_candidates_annual=f["annual_candidates"],
            renewal_candidates=f["renew_candidates"],
            store_first=int(round(O.store[pl]["first"].sum())), store_renewals=int(round(O.store[pl]["ren"].sum())),
            store_annual=int(round(O.store[pl]["ann"].sum())),
            recorded_first=int(O.rec[mk][:, 0].sum()), recorded_renewals=int(O.rec[mk][:, 1:].sum()),
            recorded_annual=int(O.rec_a0[mk].sum()), rivals=rival,
            charged_over_recorded=round(float((O.store[pl]["first"].sum() + O.store[pl]["ren"].sum()) / O.rec[mk].sum()), 2),
            periods=[dict(first=int(round(a)), renewals=int(round(b)), fitted=round(float(c_), 1))
                     for a, b, c_ in zip(f["F"], f["R"], f["fitted"])])
    return out, webq


def ratio_block(O, v, vm):
    """each source's fitted ratio with its standard error (on the revenue, and refitted on the monthly payments), the
    adding-up overall and by market, which sources could share a ratio, and how far the fitted ratios stand from the
    ratios another source would lend"""
    srcs, b, V = C.s2_fit(O, v, cov=True)
    _s, _b, Vc = C.s2_fit(O, v, cov="classical")
    bm = C.s2_fit(O, vm)
    b = np.array(b)
    names = [C.SOURCES[i] for i in srcs]
    S = C.s2_strata(O, v)
    T = S["T"]
    r = C.s2_fit(O, v)
    out = dict(sources={nm: dict(ratio=round(float(b[j]), 3), se=round(float(np.sqrt(V[j, j])), 3),
                                 se_one_variance=round(float(np.sqrt(Vc[j, j])), 3),
                                 ratio_payments=round(float(bm[i]), 3),
                                 declined=int(round(float(S["nc"][i].sum()))),
                                 named=int(round(float(T["n"][i].sum()))))
                        for j, (nm, i) in enumerate(zip(names, srcs))})
    paid = S["pv"].sum((1, 2))
    asa = C.asa_ratio(O, v)

    def priced(f):
        return sum((S["nc"][i] * (T["vc"][i] * f(i))[None, None, :]).sum((1, 2)) for i in srcs)
    ways = {"named": priced(lambda i: 1.0), "search_ads": priced(lambda i: asa), "fitted": priced(lambda i: r[i])}
    out["adding_up"] = {k: round(float(x.sum() / paid.sum()), 3) for k, x in ways.items()}
    out["adding_up"]["borrowed_shift"] = round(float(C.falsification_s2(O, v, C.values(O, which="payers"), "r1mix")), 3)
    out["adding_up_by_market"] = {k: {m: round(float(x[j] / paid[j]), 3) for j, m in enumerate(C.MARKETS)}
                                  for k, x in ways.items()}
    out["pool"] = dict(accounts=int(S["pool"].sum()), paid=int(round(float(paid.sum()))),
                       paid_per_account=round(float(paid.sum() / S["pool"].sum()), 2),
                       network_installs=int(round(sum(float(S["nc"][i].sum()) for i in S["hidden"]))),
                       organic_installs=int(round(float(S["nc"][S["org"]].sum()))),
                       market_weeks=int((S["pn"].sum(2) > 0).sum()))
    # SF7: the revenue ratios carried onto the monthly payments against the ratios refitted on them; the accounts
    # with no channel priced each way over the monthly payments they made, and what each network's payments per 100
    # installs come to at the revenue ratios
    Sm = C.s2_strata(O, vm)
    Tm = Sm["T"]
    tot = lambda rr: sum(float((Sm["nc"][i].sum((0, 1)) * Tm["vc"][i] * rr[i]).sum()) for i in srcs)
    out["payments_adding_up"] = dict(revenue_ratios=round(tot(r) / float(Sm["pv"].sum()), 3),
                                     payment_ratios=round(tot(bm) / float(Sm["pv"].sum()), 3))
    carried, own = {}, {}
    for c in IOS:
        ci = C.ORDER.index(c)
        vc, n = Tm["vc"][ci], Tm["n"][ci]
        nc = np.maximum(Sm["nc"][ci].sum((0, 1)), 0)
        t_ = n + nc
        for d, rr in ((carried, r), (own, bm)):
            price = np.where(t_ > 0, (n * vc + nc * vc * rr[ci]) / np.maximum(t_, 1e-9), vc)
            d[c] = round(100.0 * float((t_ * price).sum() / t_.sum()), 1)
    out["payments_at_revenue_ratios"] = carried
    out["payments_at_payment_ratios"] = own
    tests = {}
    for key, nms in (("Meta and TikTok", ("Meta iOS", "TikTok iOS")), ("TikTok and Snapchat", ("TikTok iOS", "Snapchat iOS")),
                     ("Meta, TikTok and Snapchat", ("Meta iOS", "TikTok iOS", "Snapchat iOS")),
                     ("the four social networks", ("Meta iOS", "TikTok iOS", "Snapchat iOS", "Pinterest iOS")),
                     ("the five networks", ("Meta iOS", "TikTok iOS", "Snapchat iOS", "Google iOS", "Pinterest iOS")),
                     ("Google and Pinterest", ("Google iOS", "Pinterest iOS")),
                     ("Google, Pinterest and organic", ("Google iOS", "Pinterest iOS", "organic iOS")),
                     ("Pinterest and organic", ("Pinterest iOS", "organic iOS")),
                     ("Google and organic", ("Google iOS", "organic iOS"))):
        st, _d = C.s2_equal_test(O, v, nms)
        sc, _d = C.s2_equal_test(O, v, nms, cov="classical")
        pt = CHI[len(nms) - 1]
        tests[key] = dict(stat=round(float(st), 2), stat_one_variance=round(float(sc), 2), df=len(nms) - 1, point=pt,
                          refused=bool(st > pt and sc > pt))
    out["share_tests"] = tests
    net = [names.index(c) for c in C.GATED]
    Vn, Vcn = V[np.ix_(net, net)], Vc[np.ix_(net, net)]
    lend = {"search_ads": np.full(len(net), C.asa_one(O, v)),
            "android": np.array([C.labelled_one(O, v, C.ANALOGUE[c]) for c in C.GATED])}
    out["lent"] = {k: dict(stat=round(float((b[net] - x) @ np.linalg.solve(Vn, b[net] - x)), 1),
                           stat_one_variance=round(float((b[net] - x) @ np.linalg.solve(Vcn, b[net] - x)), 1), df=len(net),
                           point=CHI[len(net)], ratios={c: round(float(x[j]), 3) for j, c in enumerate(C.GATED)})
                   for k, x in lend.items()}
    out["search_ads_ratio"] = round(float(C.asa_one(O, v)), 3)
    out["android_ratio"] = {c: round(float(C.labelled_one(O, v, c)), 3) for c in sorted(set(C.ANALOGUE.values()))}
    return out


def live_of(O):
    """each network's live market-weeks of the mature year as the spend export shows them (a campaign spends)"""
    return {c: O.spend_mw[C.ORDER.index(c)][:, :C.MATURE] > 0 for c in C.GATED}


def pooled_block(O, v, g):
    """SF32: the second step's ratios fitted on the 52 weeks with the three markets summed, against each market's own
    fit, each network's live and dark market-weeks priced at the pooled ratios and at the golden's, and the Wald
    distance; with what the pooled fit and each market's own fit file"""
    pp = C.pooled_pins(O, v)
    srcs, b, V = C.s2_fit(O, v, cov=True)
    _s, bp, Vp = C.s2_fit(O, v, cov=True, markets="pooled")
    se, sep = np.sqrt(np.diag(V)), np.sqrt(np.diag(Vp))
    r = A.route(O, markets="pooled")
    out = dict(ratio={nm: dict(golden=round(float(x["golden"]), 3), pooled=round(float(x["pooled"]), 3),
                               markets=[round(float(m), 3) for m in x["markets"]])
                      for nm, x in pp["ratio"].items()},
               split={nm: dict(live=x["live"], dark=x["dark"], golden=[round(float(a), 3) for a in x["golden"]],
                               pooled=[round(float(a), 3) for a in x["pooled"]]) for nm, x in pp["split"].items()},
               wald=round(float(pp["wald"][0]), 1), wald_df=int(pp["wald"][1]), wald_point=CHI.get(int(pp["wald"][1])),
               se_times=[math.floor(10 * float((sep / se).min())) / 10.0, math.floor(10 * float((sep / se).max())) / 10.0],
               return_plan={c: stated("return " + c, r[c]["roas"]) for c in MEM},
               pay100={c: stated("payments per 100 " + c, r[c]["pay100"]) for c in IOS},
               wrong=[c for c in MEM if C.band(r[c]["roas"]) != C.band(g[c]["roas"])])
    gl = list(pp["split"].values())
    out["golden_split_range"] = [round(float(min(min(x["golden"]) for x in gl)), 3),
                                 round(float(max(max(x["golden"]) for x in gl)), 3)]
    # the same split read off the shipped spend export: a network's campaign is live in a market and week it spent in
    # (the export carries a day or two of trailing delivery into the first dark week, so this is the figure the files
    # reproduce; the core's calendar split rides along above)
    S = C.s2_strata(O, v)
    T = S["T"]
    srcs = S["hidden"] + [S["org"]]
    Xs = np.stack([(S["nc"][i] * T["vc"][i][None, None, :]).sum(2) for i in srcs], 0)
    y = S["pv"].sum(2)
    fits = {"golden": C.s2_fit(O, v), "pooled": C.s2_fit(O, v, markets="pooled")}
    live = live_of(O)
    sp = {}
    for i in S["hidden"]:
        nm = C.SOURCES[i]
        lv = live[nm]
        row = dict(live=int(lv.sum()), dark=int((~lv).sum()))
        for k, r in fits.items():
            pred = np.tensordot(np.array([r[j] for j in srcs]), Xs, 1)
            row[k] = [round(float(pred[lv].sum() / y[lv].sum()), 3), round(float(pred[~lv].sum() / y[~lv].sum()), 3)]
        sp[nm] = row
    out["split_pack"] = sp
    out["golden_split_pack_range"] = [min(min(x["golden"]) for x in sp.values()), max(max(x["golden"]) for x in sp.values())]
    return out


def holdout(O, v, leave_w):
    """the hold-out a careful analyst makes of the installs response: the named weeks left out for every channel,
    mean absolute error of the installs predicted for them"""
    out = {}
    for how in ("spend", "golden", "budget"):
        coef = C.response(O, v, how=how, leave=[(c, w) for c in C.ORDER for w in leave_w])
        ae = []
        wk = np.array(leave_w)
        for ci, c in enumerate(C.ORDER):
            Bc = O.B[c]
            lb, ls = np.log(Bc["budget"]), np.log(Bc["spend"])
            ld = ls - lb
            a, s_, d_, mon = coef["i"]["a"][ci], coef["i"]["s"][ci], coef["i"]["d"][ci], coef["i"]["mon"][ci]
            x = (lb[wk] - lb.mean()) if how in ("golden", "budget") else (ls[wk] - ls.mean())
            p = np.exp(a + s_ * x + d_ * (ld[wk] - ld.mean()) + mon[C.WMONTH[wk] - 1])
            ae += list(np.abs(p / O.agg[c][wk] - 1))
        out[how] = float(np.mean(ae))
    return out


def moves_block(O, v):
    """the weeks the team moved a budget, each move left out of the fit in turn: the installs missed in them, and
    each channel's raised over lowered weeks"""
    tot = {"spend": [0.0, 0.0], "golden": [0.0, 0.0]}
    nmoves = nweeks = 0
    for ci, c in enumerate(C.ORDER):
        Bc = O.B[c]
        lb, ls = np.log(Bc["budget"]), np.log(Bc["spend"])
        ld = ls - lb
        for w0, k, _f in O.pushes[c]:
            wk = np.arange(w0, min(w0 + k, C.WEEKS))
            nmoves += 1
            nweeks += wk.size
            for how in tot:
                coef = C.response(O, v, how=how, leave=[(c, int(w)) for w in wk])
                a, s_, d_, mon = coef["i"]["a"][ci], coef["i"]["s"][ci], coef["i"]["d"][ci], coef["i"]["mon"][ci]
                x = (lb[wk] - lb.mean()) if how == "golden" else (ls[wk] - ls.mean())
                p = np.exp(a + s_ * x + d_ * (ld[wk] - ld.mean()) + mon[C.WMONTH[wk] - 1])
                tot[how][0] += float(np.abs(p - O.agg[c][wk]).sum())
                tot[how][1] += float(O.agg[c][wk].sum())
    by = {}
    for c in C.ORDER:
        r = C.referee_s3(O, v, c)
        pu = O.pushes[c]
        by[c] = dict(actual=round(r["truth"], 3), budget_fit=round(r["golden"], 3),
                     spend_fit=round(r["rivals"]["response fitted on spend"], 3),
                     spend_by_budget=round(r["other"]["spend instrumented by the budget"], 3),
                     budget_alone=round(r["other"]["the budget alone"], 3), moves=len(pu),
                     raised=int(sum(min(w0 + k, C.WEEKS) - w0 for w0, k, f_ in pu if f_ > 1)),
                     lowered=int(sum(min(w0 + k, C.WEEKS) - w0 for w0, k, f_ in pu if f_ < 1)))
    return dict(moves=nmoves, weeks=nweeks, missed_pct={k: round(100 * a / b_, 1) for k, (a, b_) in tot.items()},
                channels=by)


def delivery_block(O):
    """SF33 on full delivery: the share of each channel's budgets billed over the 104 weeks, the weeks that billed the
    whole budget, the best quarter, and the installs the budget fit puts on the record's own weeks at a share of one
    over the installs counted"""
    d = C.delivery_pins(O)
    return dict(channels={c: dict(share=round(x["share"], 3), whole=x["whole"], best_quarter=round(x["best_quarter"], 3),
                                  adds_up_pct=round(100 * x["adds_up"], 1)) for c, x in d.items()},
                share=[round(min(x["share"] for x in d.values()), 3), round(max(x["share"] for x in d.values()), 3)],
                whole=[min(x["whole"] for x in d.values()), max(x["whole"] for x in d.values())],
                best_quarter=[round(min(x["best_quarter"] for x in d.values()), 3),
                              round(max(x["best_quarter"] for x in d.values()), 3)],
                best_quarter_pct=[round(100 * min(x["best_quarter"] for x in d.values()), 1),
                                  round(100 * max(x["best_quarter"] for x in d.values()), 1)],
                adds_up_pct=[round(100 * min(x["adds_up"] for x in d.values()), 1),
                             round(100 * max(x["adds_up"] for x in d.values()), 1)],
                quarter_departure=round(float(C.quarter_departure(O)), 3))


# each simpler way of taking one step, the other two taken as estimated: the step it stands in for and its rule
SHORTCUTS = [
    ("S1", "as_recorded", "the billing records as they stand", dict(s1="raw")),
    ("S1", "by_period", "each recorded charge scaled by its store's charges over the recorded ones in the charge's period",
     dict(s1="prop_month")),
    ("S1", "one_factor", "each recorded charge scaled by its store's charges over the recorded ones over the whole record",
     dict(s1="prop")),
    ("S1", "web_rate", "the candidates carried at the continuation of the web checkout's subscribers after their last open",
     dict(webq=True)),
    ("S1", "seen_rate", "the candidates carried at one less the cancellations the app saw per charge on file",
     dict(s1="awake")),
    ("S1", "keep_3", "a subscription still set to renew counted as paying three months after its last open",
     dict(s1="keep:3")),
    ("S2", "borrowed_shift", "the declined installs' chance of paying fitted per network and their revenue per payer "
     "shifted by the gap the fully named channels show", dict(s2="r1mix")),
    ("S2", "named_by_cell", "every postback valued like the network's named installs of the same first-48-hour value",
     dict(s2="bridge")),
    ("S2", "named_average", "every install valued at the network's named installs' average", dict(s2="consenters")),
    ("S2", "search_ads", "the declined installs at Apple Search Ads' ratio of declined to allowed", dict(s2="ratio")),
    ("S2", "android", "the declined installs at the ratio the same kind of network shows on Android", dict(s2="analogue")),
    ("S2", "one_ratio", "one ratio for every source", dict(s2="common")),
    ("S2", "markets_pooled", "the ratios fitted on the 52 weeks with the three markets summed", dict(markets="pooled")),
    ("S3", "full_delivery", "the plan's billed spend read as a budget billed in full, the fit's own prediction",
     dict(carry="plain", dbar_set=1.0)),
    ("S3", "full_delivery_rescaled", "the plan's billed spend read as a budget billed in full, the fit scaled to the "
     "installs on record", dict(dbar_set=1.0)),
    ("S3", "on_spend", "installs and value per install fitted on the week's billed spend", dict(s3="spend")),
    ("S3", "last_year", "the return of the year to 2 November 2025 carried over", dict(s3="average")),
]


def shortcuts(O, g):
    """each named shortcut, the other two steps as estimated: its open channel's figures and the bands it files; and
    every figure of the route with its call, for the rubric's price of it"""
    out, vals = {}, {}
    gold = {c: C.band(g[c]["roas"]) for c in MEM}
    for step, key, rule, kw in SHORTCUTS:
        r = A.route(O, **kw)
        mem = OWN[step]
        out[key] = dict(step=step, rule=rule, channel=mem, return_plan={c: stated("return " + c, r[c]["roas"]) for c in MEM},
                        pay100={c: stated("payments per 100 " + c, r[c]["pay100"]) for c in MEM},
                        plan=plan_of(r), band=C.band(r[mem]["roas"]),
                        wrong=[c for c in MEM if C.band(r[c]["roas"]) != gold[c]])
        vals[key] = (C.figure_values(r), call_of(r))
    return out, vals


def market_week_miss(O, v):
    """what the accounts with no channel paid in each market and week, against three ways of pricing them: mean
    absolute miss as a share of the revenue"""
    S = C.s2_strata(O, v)
    T = S["T"]
    srcs = S["hidden"] + [S["org"]]
    act = S["pv"].sum(2)
    X = {i: (S["nc"][i] * T["vc"][i][None, None, :]).sum(2) for i in srcs}
    r, rc, rp = C.s2_fit(O, v), C.s2_fit(O, v, common=True), C.s2_fit(O, v, markets="pooled")
    ways = {"fitted": sum(X[i] * r[i] for i in srcs), "one_ratio": sum(X[i] * rc[i] for i in srcs),
            "markets_pooled": sum(X[i] * rp[i] for i in srcs)}
    return {k: round(100 * float(np.abs(p - act).sum() / act.sum()), 1) for k, p in ways.items()}


def web_one_factor(O, c="AppLovin Android"):
    """the web checkout's check under one ratio per store over the whole record"""
    ci = C.ORDER.index(c)
    idx, n_open = C._web_silent(O, (O.label == ci) & O.mature)
    idx, n_open = idx[n_open >= 1], n_open[n_open >= 1]
    pl = int(C.CH[c]["ios"])
    mk = (O.ios == bool(pl)) & ~O.web
    fac = (O.store[pl]["first"].sum() + O.store[pl]["ren"].sum()) / O.rec[mk].sum()
    wend = O.day[idx] + 365
    seen = O.true_charge[idx] & (O.rdays[idx] <= O.last_open[idx][:, None]) & (O.rdays[idx] < wend[:, None])
    return float((seen.sum(1) * (fac - 1) * O.netm[idx]).sum() / idx.size)


CARRY_SHARE = (("at_share", "plain"), ("weekly_shares", "plain-dist"), ("geometric_mean", "plain-geo"),
               ("median_week", "plain-median"))
CARRY_HELD = ("at_share", "weekly_shares")                         # the two forms that add up to the installs counted
CARRY_WEEKS = (("both_years", {}, slice(0, C.WEEKS)), ("first_year", dict(dbar_weeks=C.MATURE), slice(0, C.MATURE)),
               ("second_year", dict(dbar_from=C.MATURE), slice(C.MATURE, C.WEEKS)))


def carry_block(O, v, g):
    """how the fitted installs are carried to the plan (SF33). The golden's carry scales the installs equation's budget
    and month terms so that they add up to the installs on record; the equation's own prediction with the share of the
    budget billed put in from outside need not. For each such prediction: what it adds up to over the weeks the share
    is taken from, at their own budgets, as a percentage of the installs counted in those weeks, and what it files"""
    coef = C.response(O, v)
    out = dict(adds_up_pct={}, returns={}, plan={}, wrong={})
    for wkey, wkw, _sl in CARRY_WEEKS:
        for skey, carry in CARRY_SHARE:
            key = skey + "_" + wkey
            r = A.route(O, carry=carry, **wkw)
            out["returns"][key] = {c: stated("return " + c, r[c]["roas"]) for c in MEM}
            out["plan"][key] = plan_of(r)
            out["wrong"][key] = [c for c in MEM if C.band(r[c]["roas"]) != C.band(g[c]["roas"])]
            out["adds_up_pct"][key] = {}
    for c in MEM:
        ci = C.ORDER.index(c)
        Bc = O.B[c]
        lb = np.log(Bc["budget"])
        ld = np.log(Bc["spend"]) - lb
        d = float(coef["i"]["d"][ci])
        fit = np.exp(coef["i"]["a"][ci] + coef["i"]["s"][ci] * (lb - lb.mean()) + coef["i"]["mon"][ci][C.WMONTH - 1])
        for wkey, _kw, sl in CARRY_WEEKS:
            share = Bc["spend"][sl] / Bc["budget"][sl]
            term = dict(at_share=float(np.exp(d * (np.log(Bc["spend"][sl].sum() / Bc["budget"][sl].sum()) - ld.mean()))),
                        weekly_shares=float(np.exp(d * (np.log(share) - ld.mean())).mean()),
                        geometric_mean=float(np.exp(d * (np.log(share).mean() - ld.mean()))),
                        median_week=float(np.exp(d * (np.log(np.median(share)) - ld.mean()))))
            for skey, _carry in CARRY_SHARE:
                out["adds_up_pct"][skey + "_" + wkey][c] = round(100 * float(fit[sl].sum() * term[skey] / O.agg[c][sl].sum()), 1)
    keys = lambda forms: [k + "_" + w for k in forms for w, _kw, _sl in CARRY_WEEKS]
    held, refused = keys(CARRY_HELD), keys([k for k, _c in CARRY_SHARE if k not in CARRY_HELD])
    hv = [out["adds_up_pct"][k][c] for k in held for c in MEM]
    out["held"], out["refused"] = held, refused
    out["held_pct"] = [min(hv), max(hv)]
    short = [round(100 - min(out["adds_up_pct"][k].values()), 1) for k in refused]
    out["refused_short_pct"] = [min(short), max(short)]
    out["held_short_pct"] = round(100 - min(hv), 1)
    return out


def _response_rows(O, v, eq="i"):
    """the weekly record as the response fit sees it, every channel of the records: the channel, the week's budget over
    the channel's mean budget, the log of the share of it billed about its mean, the month, and the log of the week's
    installs (eq "i") or of its value per install (eq "v")"""
    ch, B, z, y, mo = [], [], [], [], []
    for ci, c in enumerate(C.ORDER):
        Bc = O.B[c]
        ld = np.log(Bc["spend"]) - np.log(Bc["budget"])
        ch += [ci] * C.WEEKS
        B += list(Bc["budget"] / Bc["budget"].mean())
        z += list(ld - ld.mean())
        y += list(np.log(O.agg[c] if eq == "i" else C.weekly_quality(O, v, c)))
        mo += list(C.WMONTH)
    return np.array(ch), np.array(B), np.array(z), np.array(y), np.array(mo)


def _design(ch, z, mo, extra):
    """each channel's level and delivery slope, the extra regressors channel by channel, and the shared month pattern"""
    cols = []
    for c in range(len(C.ORDER)):
        cols.append((ch == c).astype(float))
        cols.append((ch == c) * z)
        cols += [(ch == c) * f for f in extra]
    cols += [(mo == m).astype(float) for m in range(2, 13)]
    return np.stack(cols, 1)


def _line_sse(ch, B, y, X):
    """least squares with installs a straight line in the budget (the log of the budget plus a constant, one constant
    per channel, set against the other terms in X): the constants searched one channel at a time until none moves"""
    Q = np.linalg.qr(X)[0]
    nc = len(C.ORDER)
    lo = np.array([-float(B[ch == c].min()) for c in range(nc)])
    k = np.full(nc, 0.3)

    def sse(kv):
        r = y - np.log(B + kv[ch])
        r = r - Q @ (Q.T @ r)
        return float(r @ r)
    gr = (math.sqrt(5) - 1) / 2
    best = sse(k)
    for _sweep in range(200):
        for c in range(nc):
            def f(x, c=c):
                kv = k.copy()
                kv[c] = x
                return sse(kv)
            grid = lo[c] + np.concatenate([np.linspace(0.02, 1.0, 50), np.linspace(1.1, 6.0, 50)])
            j = int(np.argmin([f(x) for x in grid]))
            a_, b_ = grid[max(j - 1, 0)], grid[min(j + 1, grid.size - 1)]
            c_, d_ = b_ - gr * (b_ - a_), a_ + gr * (b_ - a_)
            for _ in range(60):
                if f(c_) < f(d_):
                    b_ = d_
                else:
                    a_ = c_
                c_, d_ = b_ - gr * (b_ - a_), a_ + gr * (b_ - a_)
            k[c] = (a_ + b_) / 2
        now = sse(k)
        if best - now < 1e-10:
            break
        best = now
    return sse(k), k


def form_block(O, v):
    """the form of the response (SF34), on the weekly record of every channel with the month pattern and the delivery
    term refitted each time: a power of the budget (the fit), a straight line in it and an exponential in it, each with
    the other's term added channel by channel, as an F on the added terms; each form on the moved weeks; and (SF35)
    each plan channel's value slope on the budget against its own spread"""
    ch, B, z, y, mo = _response_rows(O, v)
    n, nc = y.size, len(C.ORDER)

    def ols(extra, yy):
        X = _design(ch, z, mo, extra)
        e = yy - X @ np.linalg.lstsq(X, yy, rcond=None)[0]
        return float(e @ e), X.shape[1]
    lB = np.log(B)
    s_pow, p_pow = ols([lB], y)
    s_both, p_both = ols([lB, B], y)
    s_exp, _p = ols([B], y)
    s_line, k_line = _line_sse(ch, B, y, _design(ch, z, mo, []))
    s_line_log, _k = _line_sse(ch, B, y, _design(ch, z, mo, [lB]))
    p_line_log = p_pow + nc
    F = lambda s0, s1, p1: ((s0 - s1) / nc) / (s1 / (n - p1))
    coef = C.response(O, v)
    assert abs(s_pow - sum(float(((np.log(O.agg[c]) - (coef["i"]["a"][ci] + coef["i"]["s"][ci] * (np.log(O.B[c]["budget"])
               - np.log(O.B[c]["budget"]).mean()) + coef["i"]["d"][ci] * z[ch == ci] + coef["i"]["mon"][ci][C.WMONTH - 1])) ** 2).sum())
               for ci, c in enumerate(C.ORDER))) < 1e-6, "the power form here is the response fit"
    _c, _B, _z, yv, _m = _response_rows(O, v, "v")
    X = _design(ch, z, mo, [lB])
    beta = np.linalg.lstsq(X, yv, rcond=None)[0]
    e = yv - X @ beta
    cov = np.linalg.inv(X.T @ X) * float(e @ e) / (n - X.shape[1])
    slopes = {}
    for c in MEM:
        ci = C.ORDER.index(c)
        j = 3 * ci + 2
        assert abs(beta[j] - coef["v"]["s"][ci]) < 1e-8, "the value slope here is the response fit's"
        slopes[c] = dict(slope=round(float(beta[j]), 3), se=round(float(math.sqrt(cov[j, j])), 3),
                         spreads_from_nought=math.floor(10 * abs(float(beta[j])) / math.sqrt(cov[j, j])) / 10.0)
    I = np.exp(y)
    rows = np.arange(n)
    Xp, Xb = _design(ch, z, mo, [lB]), _design(ch, z, mo, [B])
    how = {"power": (Xp, y, np.exp), "line": (Xb, I, lambda x: x), "exponential": (Xb, y, np.exp)}
    miss = {k: [0.0, 0.0] for k in how}
    gi = C.ORDER.index("Google iOS")
    up = dn = 0.0
    for ci, c in enumerate(C.ORDER):
        for w0, kk, f_ in O.pushes[c]:
            te = ci * C.WEEKS + np.arange(w0, min(w0 + kk, C.WEEKS))
            tr = np.setdiff1d(rows, te)
            for key, (Xk, yk, back) in how.items():
                pr = back(Xk[te] @ np.linalg.lstsq(Xk[tr], yk[tr], rcond=None)[0])
                miss[key][0] += float(np.abs(pr - I[te]).sum())
                miss[key][1] += float(I[te].sum())
                if key == "line" and ci == gi:
                    up, dn = up + (float(pr.sum()) if f_ > 1 else 0.0), dn + (float(pr.sum()) if f_ < 1 else 0.0)
    # the two straight lines carried to the plan the way the golden carries the fit: the budget and month terms scaled
    # to add up to the installs on record, at the budget that bills the plan's spend, the value equation as fitted
    bl = np.linalg.lstsq(Xb, I, rcond=None)[0]
    X0 = _design(ch, z, mo, [])
    bm = np.linalg.lstsq(X0, y - np.log(B + k_line[ch]), rcond=None)[0]
    monl, monm = np.concatenate([[0.0], bl[3 * nc:]]), np.concatenate([[0.0], bm[2 * nc:]])
    carried = {"levels": {}, "log": {}}
    for c in MEM:
        ci = C.ORDER.index(c)
        Bc = O.B[c]
        sp = C.plan_spend(c)
        mb, lbm = float(Bc["budget"].mean()), float(np.log(Bc["budget"]).mean())
        dbar = float(Bc["spend"].sum() / Bc["budget"].sum())
        sv, mv = coef["v"]["s"][ci], coef["v"]["mon"][ci]
        fm = np.exp(sv * (np.log(Bc["budget"]) - lbm)[:C.MATURE] + mv[C.WMONTH[:C.MATURE] - 1])
        wt = O.agg[c][:C.MATURE]
        level = float(C.channel_values(O, v)[c]) / ((fm * wt).sum() / wt.sum())
        vp = level * np.exp(sv * (np.log(sp / dbar) - lbm) + mv[C.PLAN_MONTH - 1])
        lines = {"levels": lambda bn, mon_, ci=ci: bl[3 * ci] + bl[3 * ci + 2] * bn + monl[mon_ - 1],
                 "log": lambda bn, mon_, ci=ci: (bn + k_line[ci]) * np.exp(bm[2 * ci] + monm[mon_ - 1])}
        for key, fn in lines.items():
            back = float(O.agg[c].sum() / fn(Bc["budget"] / mb, C.WMONTH).sum())
            n_plan = back * fn(sp / dbar / mb, C.PLAN_MONTH)
            carried[key][c] = float((n_plan * vp).sum() / sp.sum())
    gold_band = {c: C.band(float(C.route(O)[c]["roas"])) for c in MEM}
    return dict(weeks=n, channels=nc, added_terms=nc, point=FPOINT,
                line=round(F(s_line, s_line_log, p_line_log), 1), exponential=round(F(s_exp, s_both, p_both), 1),
                power=round(F(s_pow, s_both, p_both), 1),
                moved_missed_pct={k: round(100 * a_ / b_, 1) for k, (a_, b_) in miss.items()},
                line_raised_over_lowered=round(up / dn, 3),
                line_returns={k: {c: stated("return " + c, x) for c, x in d.items()} for k, d in carried.items()},
                line_wrong={k: [c for c in MEM if C.band(d[c]) != gold_band[c]] for k, d in carried.items()},
                value_slopes=slopes,
                value_slope_range=[min(x["slope"] for x in slopes.values()), max(x["slope"] for x in slopes.values())],
                value_slope_spreads=min(x["spreads_from_nought"] for x in slopes.values()))


# ----------------------------------------------------------------------------------------------------------------
# the monthly-plan payment counts under the counting conventions a run could take (the re-banding of R1 and R2)
# ----------------------------------------------------------------------------------------------------------------

def counts(O, W=365.0, first=True, web=True, annual=0.0):
    """each account's monthly-plan payments in its first twelve months, the first step's charges the records never
    took in put on the subscriptions set to take them, under a counting convention: the window W days from the
    install, the first monthly charge at the trial's end counted or not, the web checkout's payments counted or not"""
    MD = C.MONTH_DAYS
    one = np.where(O.web, 1.0 if web else 0.0, 1.0)
    win = O.rdays < (O.day + W)[:, None]
    cnt = O.rec & win
    if not first:
        cnt = cnt.copy()
        cnt[:, 0] = False
    out = cnt.sum(1) * one + annual * (O.rec_a0 & (O.conv_day < O.day + W)) * one
    fits = C.s1_fit(O)
    ren, fst = C.s1_candidates(O)
    wend = O.day + W
    for pl in (0, 1):
        f = fits[pl]
        idx = np.where(ren & (O.ios == bool(pl)))[0]
        last = O.rdays[idx, O.n_rec[idx] - 1]
        for j in range(1, C.K):
            d = last + np.round(MD * j).astype(int)
            out[idx] += f["q"] ** j * one[idx] * ((d < wend[idx]) & (d <= C.END_DAY))
        fi = np.where(fst & (O.ios == bool(pl)))[0]
        te = O.day[fi] + 7
        mon = O.plan_seen[fi] == 1
        rel = C.s1_trial_rel(O, pl)[np.minimum((O.cv[fi] & 7) // 2, 3)]
        for sel in (mon, ~mon):
            if sel.any():
                rel[sel] = rel[sel] / rel[sel].mean()
        cm, ca = f["c_m"] * rel, f["c_a"] * rel
        out[fi] += np.where(mon, cm * (1.0 if first else 0.0), ca * annual) * one[fi]
        for j in range(1, C.K):
            d = te + np.round(MD * j).astype(int)
            out[fi] += mon * cm * f["q"] ** j * one[fi] * ((d < wend[fi]) & (d <= C.END_DAY))
    _KEEP.append(out)
    return out


CONVENTIONS = [
    ("golden", "every monthly-plan charge in the 365 days from the install, the first at the trial's end among them, "
     "refunded charges netted, the web checkout's payments counted", {}),
    ("months_365_25", "the first twelve months taken as twelve months of 30.4375 days (365.25 days)", dict(W=365.25)),
    ("days_366", "the first twelve months taken as 366 days", dict(W=366.0)),
    ("refunds_counted", "refunded charges counted, in the billing records and in the stores' reports", "refund"),
    ("first_left_out", "the first monthly charge, at the trial's end, left out", dict(first=False)),
    ("web_left_out", "the web checkout's payments left out", dict(web=False)),
    ("annual_as_one", "an annual-plan charge counted as one payment", dict(annual=1.0)),
    ("annual_as_twelve", "an annual-plan charge counted as twelve payments", dict(annual=12.0)),
]


def payment_conventions(O, target):
    """each channel's payments per 100 installs of the year to 2 November 2025 under each counting convention; the iOS
    networks' through the second step refitted on those counts, as the golden's are"""
    out = {}
    for key, rule, kw in CONVENTIONS:
        if kw == "refund":
            Or = A.PackObs(target, slip="refund")
            A.use_plan(Or)
            r = A.route(Or)
            vals = {c: float(r[c]["pay100"]) for c in MEM}
            _KEEP.append(Or)
        else:
            arr = counts(O, **kw)
            cv = C.channel_values(O, arr, pay=C.values(O, which="payers"))
            vals = {c: 100.0 * float(cv[c]) for c in MEM}
        out[key] = dict(rule=rule, pay100={c: round(vals[c], 1) for c in MEM}, exact={c: vals[c] for c in MEM})
    return out


# ----------------------------------------------------------------------------------------------------------------
# the figures
# ----------------------------------------------------------------------------------------------------------------

ROUTES_SHOWN = ["golden", "S1", "S2", "S3", "S1+S2+S3", "direct", "rigorous", "generous", "hedge", "calibrated", "cutoff",
                "generous:pooled-markets", "generous:careful-on-both", "generous:named-value", "hedge:fit-on-spend"]


def figures(X):
    O, g, fam, lat, direct, rig = X["O"], X["golden"], X["family"], X["lattice"], X["direct"], X["rigorous"]
    runs = X["runs"]
    gf = C.figure_values(g)
    ff = [C.figure_values(r) for _n, r in fam]
    lf = {k: C.figure_values(lat[k]) for k in KEYS}
    df, rf = C.figure_values(direct), C.figure_values(rig)
    fids = [nm + c for nm, _k in C.FAMILIES for c in MEM] + [nm for nm, _i in C.PLAN_FIGURES]
    fig = {"call": call_of(g), "bands": {c: C.band(g[c]["roas"]) for c in MEM}}
    fig["by_band"] = {b: [c for c in MEM if fig["bands"][c] == b] for b in ("scale", "hold", "cut")}
    nb = X["counts"].get("beside", 0)                          # the ways beside the battery sit last in the family
    ns = X["counts"]["singles"]                                # the ranges hold the single ways; the pairs and the
    # triples are run for the call (the design note's battery line)
    val, band = {}, {}
    for fid in fids:
        val[fid] = stated(fid, gf[fid])
        band[fid] = band_of(fid, gf[fid], [x[fid] for x in ff[:ns]], [x[fid] for x in ff[len(ff) - nb:]])
    fig["figure"], fig["figure_band"] = val, band
    for nm, key in FAM_KEY.items():
        fig[key] = {c: val[nm + c] for c in MEM}
        fig[key + "_band"] = {c: band[nm + c] for c in MEM}
    for nm, key in PLAN_KEY.items():
        fig[key], fig[key + "_band"] = val[nm], band[nm]
    fig["payments_android"] = {c: val["payments per 100 " + c] for c in ANDROID}
    fig["payments_ios"] = {c: val["payments per 100 " + c] for c in IOS}
    fig["components"] = {s: dict(id=fid, value=val[fid], band=band[fid]) for s, fid in C.COMPONENTS.items()}
    # the routes, for the workbook's routes sheet and the blocks' rejected figures
    routes = {"golden": g, "direct": direct, "rigorous": rig}
    routes.update({k: lat[k] for k in KEYS})
    routes.update(runs)
    fig["routes"] = {k: dict({c: {"return_plan": stated("return " + c, r[c]["roas"]),
                                  "pay100": stated("payments per 100 " + c, r[c]["pay100"]),
                                  "band": C.band(r[c]["roas"])} for c in MEM}, plan=plan_of(r))
                     for k, r in routes.items()}
    fig["route_calls"] = {k: call_of(r) for k, r in routes.items()}
    fig["route_names"] = dict(ROUTE_NAME, direct="the billing records as they stand, the installs the export names, the "
                                                 "mature year's return carried over",
                              rigorous="the records scaled to the stores' charges store by store and period by period, "
                                       "the second and third steps as estimated")
    fig["routes_shown"] = ROUTES_SHOWN
    fig["distinct_wrong_calls"] = len({tuple(call_of(lat[k])) for k in KEYS})
    fig["route_outside"] = {k: [fid for fid in fids if not band[fid][0] <= stated(fid, x[fid]) <= band[fid][1]]
                            for k, x in list(lf.items()) + [("direct", df), ("rigorous", rf)]
                            + [(k, C.figure_values(r)) for k, r in runs.items()]}
    bat, bes = fam[:len(fam) - nb], fam[len(fam) - nb:]
    fig["variants"] = len(bat)
    fig["variant_counts"] = X["counts"]
    fig["band_pad_pct"] = round(100 * BAND_PAD, 1)
    fig["beside_pad_pct"] = round(100 * BESIDE_PAD, 1)
    fig["single_variants"] = [n for n, _r in fam[:X["counts"]["singles"]]]
    kwof = dict(C.BESIDE)
    of = lambda key: [(n, r) for n, r in bes if key in kwof[n]]
    rows_, carry_, cells_, weeks_ = of("rows"), of("carry"), of("cells"), of("weeks_v")
    assert len(rows_) + len(carry_) + len(cells_) + len(weeks_) == len(bes), "every way beside the battery sits in a family"
    span = lambda rs, c, k, nd: [round(min(float(r[c][k]) for _n, r in rs), nd), round(max(float(r[c][k]) for _n, r in rs), nd)]
    fig["beside"] = dict(
        names=[n for n, _r in bes],
        finer_rows=dict(ways=len(rows_), pay100={c: span(rows_, c, "pay100", 1) for c in IOS},
                        return_plan={c: span(rows_, c, "roas", 3) for c in IOS},
                        each={n: {c: stated("return " + c, r[c]["roas"]) for c in IOS} for n, r in rows_}),
        unrescaled=dict(ways=len(carry_), return_span={c: span(carry_, c, "roas", 3) for c in MEM},
                        installs=[stated("installs the plan buys", r["plan"][0]) for _n, r in carry_]),
        grouped=dict(ways=len(cells_), return_plan={c: span(cells_, c, "roas", 3) for c in MEM}),
        value_weeks=dict(ways=len(weeks_), return_plan={c: span(weeks_, c, "roas", 3) for c in MEM}),
        edges=sorted(fid for fid in fids if band[fid] != band_of(fid, gf[fid], [x[fid] for x in ff[:ns]])))
    worst = min((abs(r[c]["roas"] - l), c, n) for n, r in bat for c in MEM for l in C.LINES)
    fig["nearest_variant"] = {"distance": math.floor(worst[0] * 1000) / 1000.0, "channel": worst[1], "variant": worst[2]}
    worst = min((abs(r[c]["roas"] - l), c, n) for n, r in bes for c in MEM for l in C.LINES)
    fig["nearest_beside"] = {"distance": math.floor(worst[0] * 1000) / 1000.0, "channel": worst[1], "variant": worst[2]}
    fig["family_calls_all_golden"] = all(call_of(r) == fig["call"] for _n, r in fam)
    cr = X.get("crossed") or []
    if cr:
        worst = min((abs(r[c]["roas"] - l), c, n, float(r[c]["roas"]), l) for n, r in cr for c in MEM for l in C.LINES)
        fig["crossed"] = dict(
            crossings=len(cr), moved=sorted(n for n, r in cr if call_of(r) != fig["call"]),
            nearest=dict(distance=math.floor(worst[0] * 1000) / 1000.0, channel=worst[1], variant=worst[2],
                         return_plan=stated("return " + worst[1], worst[3]), line=worst[4]),
            return_range={c: [round(min(float(r[c]["roas"]) for _n, r in cr), 3),
                              round(max(float(r[c]["roas"]) for _n, r in cr), 3)] for c in MEM})
    crossed_ = [C.figure_values(r) for _n, r in fam[ns:len(fam) - nb]]
    past = {}
    for fid in fids:
        lo, hi = band[fid]
        xs = [stated(fid, x[fid]) for x in crossed_]
        out_ = [x for x in xs if not lo <= x <= hi]
        if out_:
            past[fid] = dict(ways=len(out_), low=min(xs), high=max(xs), range=band[fid],
                             crossed_range=list(band_of(fid, gf[fid], [x[fid] for x in ff[:len(ff) - nb]],
                                                        [x[fid] for x in ff[len(ff) - nb:]])))
    fig["pairs_and_triples"] = dict(ways=len(crossed_), calls_all_golden=all(call_of(r) == fig["call"] for _n, r in
                                                                            fam[ns:len(fam) - nb]),
                                    past_range=past)
    fig["variant_range"] = {c: [round(min(float(r[c]["roas"]) for _n, r in fam), 3),
                                round(max(float(r[c]["roas"]) for _n, r in fam), 3)] for c in MEM}
    # every channel of the records, for the working sheets (Apple Search Ads sits outside the plan)
    v = X["v"]
    T = C.s2_cells(O, v)
    raw = lat["S1"]
    full = lat["S3"]
    ch = {}
    for ci, c in enumerate(C.ORDER):
        n12 = float(O.agg[c][:C.MATURE].sum())
        lab = (O.label == ci) & O.mature
        Bc = O.B[c]
        dbar = float(Bc["spend"].sum() / Bc["budget"].sum())
        sp = O.plan[c] if c in O.plan else O.brand[c]
        row = dict(installs_mature=int(round(n12)), named_mature=int(lab.sum()),
                   paid_per_install=round(float(g[c]["v12"]), 2), recorded_per_install=round(float(raw[c]["v12"]), 2),
                   pay100=round(float(g[c]["pay100"]), 1), recorded_pay100=round(float(raw[c]["pay100"]), 1),
                   unrecorded_pct=round(100 * (1 - float(raw[c]["v12"]) / float(g[c]["v12"])), 1),
                   delivery_share=round(dbar, 3),
                   budget_elasticity=round(float(g[c]["el"]), 3), value_slope=round(float(g[c]["qs"]), 3),
                   spend_fit_elasticity=round(float(X["spendfit"][c]["el"]), 3),
                   installs_week_plan=round(float(g[c]["installs_week"]), 1),
                   installs_week_full=round(float(full[c]["installs_week"]), 1),
                   installs_week_history=round(float(O.agg[c].sum() / C.WEEKS), 1),
                   plan_weekly_spend=int(round(float(sp.mean()))), plan_year_spend=int(round(float(sp.sum()))),
                   plan_weekly_budget=int(round(float((sp / dbar).mean()))),
                   history_weekly_spend=int(round(float(Bc["spend"].mean()))),
                   history_weekly_budget=int(round(float(Bc["budget"].mean()))),
                   budget_low=int(Bc["budget"].min()), budget_high=int(Bc["budget"].max()), moves=len(O.pushes[c]),
                   live_weeks={m: int((O.spend_mw[ci, j] > 0).sum()) for j, m in enumerate(C.MARKETS)})
        if c in MEM:
            row.update(revenue_plan=int(round(float(g[c]["revenue"]))))
        if c in C.GATED:
            n_named = float(T["n"][ci].sum())
            v_named = float(v[lab & O.consent].mean())
            row.update(named_pct=round(100 * n_named / n12, 1), named_value=round(v_named, 2),
                       declined_value=round((float(g[c]["v12"]) * n12 - n_named * v_named) / (n12 - n_named), 2),
                       borrowed_pay100=round(float(lat["S2"][c]["pay100"]), 1))
        ch[c] = row
    fig["channels"] = ch
    fig["plan_spend"] = int(sum(ch[c]["plan_year_spend"] for c in MEM))
    fig["stores"], webq = store_block(O, X["fits"])
    fig["web_continuation"] = round(webq, 3)
    fig["period_starts"] = [(dt.date(2024, 11, 4) + dt.timedelta(days=int(math.ceil(k * C.MONTH_DAYS)))).isoformat()
                            for k in range(A.NM)]
    vm = C.values(O, unit="months")
    fig["ratios"] = ratio_block(O, v, vm)
    fig["ratios"]["market_week_miss_pct"] = market_week_miss(O, v)
    fig["pooled"] = pooled_block(O, v, g)
    live = live_of(O)
    fig["pooled"]["live_from_spend"] = bool(all(np.array_equal(live[c], C.CH[c]["live"][:, :C.MATURE]) for c in C.GATED))
    fig["pooled"]["live_mismatch"] = {c: int((live[c] != C.CH[c]["live"][:, :C.MATURE]).sum()) for c in C.GATED}
    fig["carry"] = carry_block(O, v, g)
    fig["delivery"] = delivery_block(O)
    fig["forms"] = form_block(O, v)
    fig["shortcuts"], sv = shortcuts(O, g)
    fig["conventions"] = payment_conventions(O, X["target"])
    r1, r2 = X["refs"]["S1"], X["refs"]["S2"]
    fig["check_web"] = dict(subscribers=r1["n"], charged=round(r1["truth"], 2), estimate=round(r1["golden"], 2),
                            true_up=round(r1["rivals"]["proportional true-up"], 2),
                            true_up_one_factor=round(web_one_factor(O), 2),
                            store_rate_carried=round(r1["other"]["the stores' fitted continuation carried over"], 2),
                            web_rate=round(r1["other"]["continuation fitted on the web"], 3),
                            fit_subscribers=int((C._web_silent(O)[1] >= 1).sum()))
    fig["check_android"] = {}
    for c in ANDROID:
        r = r2 if c == "AppLovin Android" else C.referee_s2(O, v, c)
        fig["check_android"][c] = dict(
            installs=r["n"], paid=round(r["truth"], 2), fitted=round(r["golden"], 2),
            named=round(r["rivals"]["priced at its installs that allowed tracking, by first-48-hour value"], 2),
            search_ads=round(r["rivals"]["at Apple Search Ads' ratio"], 2),
            one_ratio=round(r["rivals"]["at one ratio for every source"], 2))
    fa = C.s2_fit(O, v, ios=False)
    fig["android_ratios"] = {C.SOURCES[i]: round(float(x), 3) for i, x in fa.items()}
    fig["check_moves"] = moves_block(O, v)
    h4 = holdout(O, v, list(range(0, C.WEEKS, 4)))
    hl = holdout(O, v, list(range(C.WEEKS - 13, C.WEEKS)))
    fig["holdout"] = dict(every_fourth_week={k: round(100 * x, 1) for k, x in h4.items()},
                          last_quarter={k: round(100 * x, 1) for k, x in hl.items()})
    pay = C.values(O, which="payers")
    fig["falsification"] = {k: round(float(C.falsification_s2(O, v, pay, k)), 3) for k in ("golden", "r1mix", "bridge", "ratio")}
    pool = O.mature & O.pool
    n_cons = int(O.n)
    ren, fst = C.s1_candidates(O)
    fig["steps"] = dict(
        accounts=O.rows["accounts"], consumer_accounts=n_cons, other_accounts=O.rows["accounts"] - n_cons,
        ios_accounts=int(O.ios.sum()), android_accounts=int((~O.ios).sum()),
        attribution_rows=O.rows["attribution"], postbacks=O.rows["postbacks"], postbacks_used=O.rows["postbacks_used"],
        postbacks_dropped=O.rows["postbacks"] - O.rows["postbacks_used"],
        billing_rows=O.rows["billing"], billing_used=O.rows["billing_used"], billing_twice=O.rows["billing_twice"],
        refunded_purchases=O.rows["refunds"], campaigns=O.rows["campaigns"], mature_weeks=C.MATURE, weeks=C.WEEKS,
        plan_weeks=52, days=365, mature_accounts=int(O.mature.sum()), mature_no_channel=int(pool.sum()),
        no_channel=int(O.pool.sum()), declined_ios_pct=round(100 * float(1 - O.consent[O.ios].mean()), 1),
        declined_android_pct=round(100 * float(1 - O.consent[~O.ios].mean()), 1),
        renewal_candidates=int(ren.sum()), trial_end_candidates=int(fst.sum()),
        monthly_charges_recorded=int(O.rec.sum()), thin_cell=20, market_weeks=3 * C.MATURE,
        early_postback_installs=O.rows["early_halves"])
    fig["policy"] = dict(lines=[0.90, 1.20], vat_pct=[21, 22, 23], commission_pct=15, fee_pct=3, monthly=9.99, annual=59.99,
                         trial_days=7, cadence_days=C.MONTH_DAYS)
    fig["plan_blocks"] = A.plan_blocks(O)
    fig["unrecorded_pct"] = dict(low=min(ch[c]["unrecorded_pct"] for c in MEM), high=max(ch[c]["unrecorded_pct"] for c in MEM))
    return fig, dict(gf=gf, ff=ff, lf=lf, df=df, rf=rf, fids=fids, sv=sv,
                     runf={k: C.figure_values(r) for k, r in runs.items()})


def spec_of(X, fig, R):
    """the core's spec rebuilt on the cut pack, each figure with the range the answer blocks state"""
    g, fam, lat, direct, rig, runs, over = (X["golden"], X["family"], X["lattice"], X["direct"], X["rigorous"], X["runs"],
                                            X["over"])
    T = C.truth_at_plan()
    ns, nb = X["counts"]["singles"], X["counts"].get("beside", 0)
    fam = fam[:ns] + fam[len(fam) - nb:]                           # the core's family: the single ways and the ways
    ffs = R["ff"][:ns] + R["ff"][len(R["ff"]) - nb:]               # beside them (core.build_spec), as the ranges are
    members = {c: dict(lines=list(C.LINES), truth=float(T[c]["roas"]), golden=float(g[c]["roas"]),
                       family=[float(r[c]["roas"]) for _n, r in fam],
                       routes=dict(direct=float(direct[c]["roas"]), rigorous=float(rig[c]["roas"])))
               for c in MEM}
    own = set(C.COMPONENTS.values())
    figs = []
    for c in MEM:
        figs.append(dict(id="return " + c, block="ask", weight=1.0, member=c, band=list(fig["figure_band"]["return " + c])))
    for fid in R["fids"]:
        if fid.startswith("return "):
            continue
        figs.append(dict(id=fid, block="component" if fid in own else "ask", weight=1.0, golden=float(R["gf"][fid]),
                         band=list(fig["figure_band"][fid]), family=[float(x[fid]) for x in ffs],
                         lattice={k: float(R["lf"][k][fid]) for k in KEYS},
                         routes=dict(rigorous=float(R["rf"][fid]), **{k: float(x[fid]) for k, x in R["runf"].items()})))
    refs = list(X["refs"].values())

    def sep(r):
        ge = abs(r["golden"] - r["truth"])
        return min(abs(x - r["truth"]) for x in r["rivals"].values()) / max(ge, 1e-12)
    ref = X["refs"]["S1"]
    stumps = {s: dict(st, opens=OWN[s], sides=dict(over={c: float(over[s][c]["roas"]) for c in MEM}))
              for s, st in C.STUMPS.items()}
    v, pay = X["v"], C.values(X["O"], which="payers")
    fal = dict(check="the unattributed iOS accounts of the mature weeks: their twelve-month revenue as each route prices "
                     "them (every network's declined installs and the organic installs that declined) over what they "
                     "paid", observes_target=False, truth=1.0,
               golden=C.falsification_s2(X["O"], v, pay, "golden"),
               rivals={k: C.falsification_s2(X["O"], v, pay, k) for k in ("r1mix", "bridge", "ratio")})
    return dict(call="lines", members=members, stumps=stumps,
                lattice={k: {c: float(lat[k][c]["roas"]) for c in MEM} for k in KEYS},
                run_routes={k: {c: float(r[c]["roas"]) for c in MEM} for k, r in runs.items()},
                referee=dict(slice=ref["slice"], covers_target=False, truth=ref["truth"], golden=ref["golden"],
                             rivals=ref["rivals"]),
                falsification=fal, figures=C.as_stated(figs)), T, [sep(r) for r in refs]


def result_values(fv, call):
    """one route's answers in the shape of the six results"""
    pick = lambda nm, cs: {c: stated(nm + c, fv[nm + c]) for c in cs}
    return {"R1": pick("payments per 100 ", ANDROID), "R2": pick("payments per 100 ", IOS),
            "R3": stated("installs the plan buys", fv["installs the plan buys"]),
            "R4": stated("revenue the plan's installs bring", fv["revenue the plan's installs bring"]),
            "R5": pick("return ", MEM), "R6": call}


PREC = {"R1": ["L70", "N21", "L44"], "R2": ["L71"], "R3": ["N46", "L37", "L28"], "R4": ["L70", "L71", "N46", "L56"],
        "R5": ["L70", "L71", "N46", "L56"], "R6": ["L70", "L71", "N46", "L56"]}


def effort(X, fig, R, pert):
    lat, direct, fam, runs = X["lattice"], X["direct"], X["family"], X["runs"]
    gold = result_values(R["gf"], fig["call"])
    quick = result_values(R["df"], call_of(direct))
    careful = result_values(R["lf"]["S1+S2+S3"], call_of(lat["S1+S2+S3"]))
    fb = fig["figure_band"]
    cells = lambda nm, cs: {c: fb[nm + c] for c in cs}
    meta = [
        ("R1", "monthly-plan payments per 100 installs, Android channels", "Component 1, Ask 1", "payments_android", [],
         "the stores' reports, the billing records and the accounts' last opens", dict(bands=cells("payments per 100 ", ANDROID))),
        ("R2", "monthly-plan payments per 100 installs, iOS networks", "Component 2, Ask 1", "payments_ios", ["R1"], "",
         dict(bands=cells("payments per 100 ", IOS))),
        ("R3", "the installs the 2027 plan buys", "Component 3, Ask 2", "plan_installs", [],
         "the media plan, the budget sheet, the daily spend and the weekly installs",
         dict(band=fb["installs the plan buys"])),
        ("R4", "the twelve-month net revenue those installs bring", "Ask 2", "plan_revenue", ["R1", "R2", "R3"], "",
         dict(band=fb["revenue the plan's installs bring"])),
        ("R5", "each channel's 2027 return per euro at the plan's spend", "Ask 1", "return_plan", ["R1", "R2", "R3"], "",
         dict(bands=cells("return ", MEM), partly_share=0.25)),
        ("R6", "each channel's band", "Recommendation", "call", ["R5"], "", {}),
    ]
    res = []
    for rid, name, graded, key, dep, indep, extra in meta:
        r = {"id": rid, "name": name, "graded_as": graded, "figure": key, "depends": dep, "independent": indep,
             "golden": gold[rid], "passes": {"quick": quick[rid], "careful": careful[rid], "thorough": gold[rid]},
             "precedent": PREC[rid]}
        r.update(extra)
        res.append(r)
    by = {r["id"]: r for r in res}

    def grades(figs, call):
        vv = result_values(figs, call)
        return {rid: EF.grade(vv[rid], by[rid])[0] for rid in by}
    g_lost = {k: grades(R["lf"][k], call_of(lat[k])) for k in KEYS}
    alone_key = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
    names = {"S1": "the stores' excess over the billing records belongs to the subscriptions nobody opens, carried at a "
                   "continuation of their own fitted to that excess",
             "S2": "an iOS network steers its blind buys by the first-48-hour value its postbacks return, so each "
                   "network's declined installs are worth a fraction of its named ones fitted from the pool across "
                   "156 market-weeks, not the fully named channels' gap",
             "S3": "the plan's weekly figures are billed spend, so what they buy is read at the budget that bills them, "
                   "at the record's share"}
    judgments = []
    for s in ("S1", "S2", "S3"):
        ak = alone_key[s]
        judgments.append({"id": s, "name": names[s], "kind": "stump", "precedent": C.STUMPS[s]["precedents"],
                          "dropped": {"answer": call_of(lat[s]), "results_moved": [r for r, x in g_lost[s].items() if x != "right"]},
                          "alone": {"answer": call_of(lat[ak]), "results_rescued": [r for r, x in g_lost[ak].items() if x == "right"]}})
    judgments += [
        {"id": "J4", "name": "each iOS network's installs counted from its install postbacks and set against its named "
                             "installs", "kind": "reflex", "precedent": ["R81", "R93"]},
        {"id": "J5", "name": "re-sent rows, reinstalls, staff and test accounts and sandbox charges left out", "kind": "reflex",
         "precedent": ["R93"]},
        {"id": "J6", "name": "net revenue at the policy's VAT, commission and fee, over the 365 days from the install",
         "kind": "reflex", "precedent": []},
        {"id": "J7", "name": "each network's declined installs valued source by source against the pool; installs on the "
                             "budget with the delivery beside it; the value falling with the budget", "kind": "reflex",
         "precedent": ["R102", "R103", "R104"]}]
    F = {"golden_answer": fig["call"], "reflex_route": {"answer": call_of(lat["S1+S2+S3"])}, "judgments": judgments}
    routes = [{"name": "the golden", "answer": fig["call"], "golden": True}]
    routes += [{"name": ROUTE_NAME[k], "answer": call_of(lat[k])} for k in KEYS]
    routes.append({"name": fig["route_names"]["direct"], "answer": call_of(direct)})
    routes.append({"name": fig["route_names"]["rigorous"], "answer": call_of(X["rigorous"])})
    routes += [{"name": "run route " + k, "answer": call_of(r)} for k, r in runs.items()]
    singles = fam[:X["counts"]["singles"]]
    nb = X["counts"].get("beside", 0)
    crossed = fam[len(singles):len(fam) - nb]
    forcing = {"kind": "set", "golden_answer": fig["call"],
               "golden_family": [{"name": "the golden", "answer": fig["call"]}]
               + [{"name": n, "answer": call_of(r)} for n, r in singles]
               + [{"name": "every pair and every triple of those ways, one from each step (%d)" % len(crossed),
                   "answer": fig["call"] if all(call_of(r) == fig["call"] for _n, r in crossed) else ["a crossed way moves the call"]}]
               + [{"name": n, "answer": call_of(r)} for n, r in fam[len(fam) - nb:]],
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": "%s, times %.3f" % (n, f), "answer": sorted("%s: %s" % (c, C.band(x[c])) for c in MEM)}
                                 for n, f, x, _ok in pert]}
    hints = [{"sentence": C.STUMPS[s]["said_out_loud"], "rescues": [r for r, x in g_lost[alone_key[s]].items() if x == "right"]}
             for s in ("S1", "S2", "S3")]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


def run(target, cross=True):
    X = A.run(target, cross=cross)
    O = X["O"]
    X["target"] = target
    X["runs"] = {k: A.route(O, **kw) for k, kw in C.RUNS.items()}
    X["over"] = {s: A.route(O, **kw) for s, kw in C.OVER.items()}
    X["spendfit"] = A.route(O, s3="spend")
    fig, R = figures(X)
    pert = C.forcing(O)
    fig["perturbations"] = [{"input": n, "factor": round(f, 3), "call_holds": bool(ok),
                             "returns": {c: round(x[c], 3) for c in MEM},
                             "nearest": round(min(abs(x[c] - l) for c in MEM for l in C.LINES), 3)} for n, f, x, ok in pert]
    pert5 = C.forcing(O, fifth=True)
    fig["perturbations_fifth"] = [{"input": n, "factor": round(f, 3), "call_holds": bool(ok),
                                   "returns": {c: round(x[c], 3) for c in MEM}} for n, f, x, ok in pert5 if "ratio" in n]
    fig["delivery_share_spread_pct"] = round(100 * C.quarter_departure(O), 1)
    spec, T, seps = spec_of(X, fig, R)
    rows, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))
    lines = corelib._criteria([f for f in earn["figs"] if f["block"] == "asks"])     # one criterion per answer line
    comps = [f for f in earn["figs"] if f["block"] == "components"]
    gcall_c = corelib._calls(spec, {m: spec["members"][m]["golden"] for m in spec["members"]})
    gcall = call_of(X["golden"])

    def landed(val):
        """the answer lines a route's figures earn whole, the components it earns, and every figure it lands"""
        return ([c[0]["sentence"] for c in lines if all(corelib._earned(f, val(f)) for f in c)],
                [f["id"] for f in comps if corelib._earned(f, val(f))],
                [f["id"] for f in earn["figs"] if f["id"] == C.stated_id(f["id"]) and corelib._earned(f, val(f))])
    lands = {k: landed(lambda f, k=k: f["values"][key(k)]) for k in KEYS}
    run_earn = {}
    for k, mp in spec["run_routes"].items():
        sc, _miss = corelib._run_route_score(spec, earn["figs"], k, mp, gcall_c)
        run_earn[k] = None if sc is None else round(sc, 1)
    fig["rubric"] = {"level": level, "fails": [r[0] + ": " + r[2] for r in rows if r[1] == "FAIL"],
                     "rows": [list(r) for r in rows],
                     "one_lost": {s: round(earn["earn"][key(s)], 1) for s in ("S1", "S2", "S3")},
                     "fixed_alone": {"S1": round(earn["earn"][key("S2+S3")], 1), "S2": round(earn["earn"][key("S1+S3")], 1),
                                     "S3": round(earn["earn"][key("S1+S2")], 1)},
                     "two_lost": {k: round(earn["earn"][key(k)], 1) for k in ("S1+S2", "S1+S3", "S2+S3")},
                     "reflex": round(earn["earn"][key("S1+S2+S3")], 1), "rigorous": round(earn["rigorous"], 1),
                     "runs": run_earn, "runs_max": max(x for x in run_earn.values() if x is not None),
                     "lines": len(lines), "figures": len({C.stated_id(f["id"]) for f in earn["figs"]}),
                     "lands": {k: len(v[0]) for k, v in lands.items()},
                     "figures_landed": {k: len(v[2]) for k, v in lands.items()},
                     "reflex_lands": lands["S1+S2+S3"][0], "reflex_figures": lands["S1+S2+S3"][2],
                     "referee_separation": [round(x, 1) for x in seps]}
    for k, (fv, call) in R["sv"].items():                      # each simpler way on the rubric, the other two steps golden
        val = lambda f, fv=fv: fv[C.stated_id(f["id"])]
        kept = landed(val)
        fig["shortcuts"][k].update(
            earns=round(corelib._score(earn["figs"], call == gcall, val), 1), lines_kept=len(kept[0]),
            components_kept=[s for s in ("S1", "S2", "S3") if C.COMPONENTS[s] in kept[1]])
    fig["truth"] = {c: round(float(T[c]["roas"]), 3) for c in MEM}
    E, g_lost = effort(X, fig, R, pert)
    fig["result_grades"] = g_lost
    return X, fig, E, spec


if __name__ == "__main__":
    import json
    import time
    t0 = time.time()
    X, fig, E, spec = run(sys.argv[1], cross="--singles" not in sys.argv)
    print("%.0fs" % (time.time() - t0))
    print(json.dumps({k: fig[k] for k in ("call", "rubric", "nearest_variant", "nearest_beside", "result_grades",
                                           "check_web", "check_android", "conventions", "pooled", "delivery",
                                           "variant_counts", "route_outside", "shortcuts")},
                     indent=1, default=float)[:60000])
    for fid in fig["figure"]:
        print("%-44s %10s  %s" % (fid, fig["figure"][fid], fig["figure_band"][fid]))
