"""Every owed figure, computed on the shipped files: figures.json (what the answer blocks and the goldens state)
and effort.json (each result's golden, band and the three passes, the stump factorial, the forcing on both sides),
with the core's rubric table re-priced on the cut pack by corelib on the ranges the blocks state."""
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
LOST = {"S1": "each recorded charge scaled by its store's ratio of charged to recorded in the charge's period",
        "S2": "every postback priced at what the network's named installs of the same first-48-hour value paid",
        "S3": "installs and value per install fitted on the week's spend"}
ROUTE_NAME = {k: "; ".join(LOST[s] for s in k.split("+")) for k in KEYS}
FAM_KEY = {"return ": "return_plan", "stretch return ": "return_stretch", "installs a week ": "installs_week",
           "value at plan ": "value_plan", "next euro ": "next_euro", "stretch next euro ": "next_euro_stretch",
           "paid per install ": "paid_per_install"}
ANDROID = [c for c in MEM if not C.CH[c]["ios"]]
IOS = [c for c in MEM if C.CH[c]["ios"]]
STORE = ((0, "Google Play"), (1, "App Store"))
BAND_PAD, BESIDE_PAD = C.BAND_PAD, C.BESIDE_PAD                    # the stated ranges' rule lives in the core
FPOINT = 1.95                                                      # the five per cent point of F on 8 and 789
CHI = {1: 3.84, 2: 5.99, 3: 7.81, 4: 9.49, 5: 11.07}                # the five per cent points
unit, band_of = C.unit, C.band_of


def stated(fid, x):
    nd = unit(fid)
    return int(round(float(x))) if nd == 0 else round(float(x), nd)


def call_of(res):
    return sorted("%s: %s" % (c, C.band(res[c]["roas"])) for c in MEM)


STUMPS = {
    "S1": dict(axis="what", opens="AppLovin Android", steps_left=4, precedents=["N21", "L44"],
               said_out_loud="A store charge reaches the app's billing records only when the subscriber next opens "
                             "the app, so the stores' excess over the records belongs to subscriptions last seen "
                             "still set to renew, not to every account in proportion."),
    "S2": dict(axis="who", opens="Meta iOS", steps_left=5, precedents=["L53", "N27", "L58"],
               said_out_loud="On iOS the attribution export names an install's channel only where the user allowed "
                             "tracking; each network's other installs sit unnamed among the accounts with no "
                             "channel, and how much less they are worth than its named ones differs from network "
                             "to network."),
    "S3": dict(axis="against", opens="Google Android", steps_left=3, precedents=["L51", "L37", "L28"],
               said_out_loud="A week's spend is what the platform chose to deliver of the week's budget given that "
                             "week's auction, so weeks of high and low spend are not weeks of high and low "
                             "budgets; what a budget buys shows in the weeks the team moved it."),
}


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
            periods=[dict(first=int(round(a)), renewals=int(round(b)), fitted=round(float(c_), 1))
                     for a, b, c_ in zip(f["F"], f["R"], f["fitted"])])
    return out, webq


def ratio_block(O, v):
    """each source's fitted ratio with its standard error, the adding-up overall and by market, which sources could
    share a ratio, and how far the fitted ratios stand from the ratios another source would lend"""
    srcs, b, V = C.s2_fit(O, v, cov=True)
    _s, _b, Vc = C.s2_fit(O, v, cov="classical")
    b = np.array(b)
    names = [C.SOURCES[i] for i in srcs]
    S = C.s2_strata(O, v)
    T = S["T"]
    r = C.s2_fit(O, v)
    out = dict(sources={nm: dict(ratio=round(float(b[j]), 3), se=round(float(np.sqrt(V[j, j])), 3),
                                 se_one_variance=round(float(np.sqrt(Vc[j, j])), 3),
                                 declined=int(round(float(S["nc"][i].sum()))),
                                 named=int(round(float(T["n"][i].sum()))))
                        for j, (nm, i) in enumerate(zip(names, srcs))})
    paid = S["pv"].sum((1, 2))
    asa = C.asa_ratio(O, v)

    def priced(f):
        return sum((S["nc"][i] * (T["vc"][i] * f(i))[None, None, :]).sum((1, 2)) for i in srcs)
    ways = {"named": priced(lambda i: 1.0), "search_ads": priced(lambda i: asa), "fitted": priced(lambda i: r[i])}
    out["adding_up"] = {k: round(float(x.sum() / paid.sum()), 2) for k, x in ways.items()}
    out["adding_up_by_market"] = {k: {m: round(float(x[j] / paid[j]), 2) for j, m in enumerate(C.MARKETS)}
                                  for k, x in ways.items()}
    out["pool"] = dict(accounts=int(S["pool"].sum()), paid=int(round(float(paid.sum()))),
                       paid_per_account=round(float(paid.sum() / S["pool"].sum()), 2),
                       network_installs=int(round(sum(float(S["nc"][i].sum()) for i in S["hidden"]))),
                       organic_installs=int(round(float(S["nc"][S["org"]].sum()))),
                       market_weeks=int((S["pn"].sum(2) > 0).sum()))
    tests = {}
    for key, nms in (("Meta and TikTok", ("Meta iOS", "TikTok iOS")), ("TikTok and Snapchat", ("TikTok iOS", "Snapchat iOS")),
                     ("Meta and Snapchat", ("Meta iOS", "Snapchat iOS")),
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
    # the five networks' fitted ratios against the ratio another source would lend them
    net = [names.index(c) for c in C.GATED]
    Vn, Vcn = V[np.ix_(net, net)], Vc[np.ix_(net, net)]
    lend = {"search_ads": np.full(len(net), C.asa_one(O, v)),
            "android": np.array([C.labelled_one(O, v, C.ANALOGUE[c]) for c in C.GATED])}
    out["lent"] = {k: dict(stat=round(float((b[net] - x) @ np.linalg.solve(Vn, b[net] - x)), 1),
                           stat_one_variance=round(float((b[net] - x) @ np.linalg.solve(Vcn, b[net] - x)), 1), df=len(net),
                           point=CHI[len(net)], ratios={c: round(float(x[j]), 3) for j, c in enumerate(C.GATED)})
                   for k, x in lend.items()}
    out["search_ads_ratio"] = round(float(C.asa_one(O, v)), 3)
    # Apple Search Ads' ratio as the simpler way uses it: the installs that declined tracking over the others, by
    # whether a trial or a purchase is flagged in the first 48 hours (neither, either)
    out["search_ads_by_flag"] = [round(float(x), 3) for x in C.asa_ratio(O, v, "tier2", "tier2")]
    out["android_ratio"] = {c: round(float(C.labelled_one(O, v, c)), 3) for c in sorted(set(C.ANALOGUE.values()))}
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


SHORTCUTS = [
    ("S1", "AppLovin Android", "by_period", "each recorded charge scaled by its store's ratio of charged to recorded in the charge's period",
     dict(s1="prop_month")),
    ("S1", "AppLovin Android", "one_factor", "each recorded charge scaled by its store's ratio of charged to recorded over the whole record",
     dict(s1="prop")),
    ("S1", "AppLovin Android", "seen_rate", "the candidates carried at one less the cancellations the app saw per charge on file",
     dict(s1="awake")),
    ("S1", "AppLovin Android", "web_rate", "the candidates carried at the continuation of the web checkout's subscribers after "
     "their last open", dict(webq=True)),
    ("S1", "AppLovin Android", "as_recorded", "the billing records as they stand", dict(s1="raw")),
    ("S2", "Meta iOS", "named_by_cell", "every postback valued like the network's named installs of the same first-48-hour value",
     dict(s2="bridge")),
    ("S2", "Meta iOS", "named_average", "every postback valued at the network's named installs' average", dict(s2="consenters")),
    ("S2", "Meta iOS", "pool_value", "every unnamed install valued at what the accounts with no channel paid at its "
     "first-48-hour value", dict(s2="flat")),
    ("S2", "Meta iOS", "search_ads", "the unnamed installs at Apple Search Ads' ratio of declined to allowed", dict(s2="ratio")),
    ("S2", "Meta iOS", "android", "the unnamed installs at the ratio the same kind of network shows on Android", dict(s2="analogue")),
    ("S2", "Meta iOS", "one_ratio", "one ratio for every source", dict(s2="common")),
    ("S2", "Meta iOS", "organic_pinned", "organic at Apple Search Ads' ratio and one ratio for the five networks", dict(s2="paid")),
    ("S2", "Meta iOS", "four_social", "the fit with Meta, TikTok, Snapchat and Pinterest sharing one ratio", dict(group="kind")),
    ("S2", "Meta iOS", "three_social", "the fit with Meta, TikTok and Snapchat sharing one ratio", dict(group="social")),
    ("S3", "Google Android", "on_spend", "installs and value per install fitted on the week's spend", dict(s3="spend")),
    ("S3", "Google Android", "last_year", "the return of the year to 2 November 2025 carried over", dict(s3="average")),
]


def shortcuts(O, g):
    """each named shortcut, the other two steps as estimated: its open channel's figures and the bands it files; and
    every figure of the route with its call, for the rubric's price of it"""
    out, vals = {}, {}
    gold = {c: C.band(g[c]["roas"]) for c in MEM}
    for step, mem, key, rule, kw in SHORTCUTS:
        r = A.route(O, **kw)
        out[key] = dict(step=step, rule=rule, channel=mem, return_plan=stated("return " + mem, r[mem]["roas"]),
                        band=C.band(r[mem]["roas"]), paid_per_install=round(float(r[mem]["v12"]), 2),
                        installs_week=int(round(float(r[mem]["installs_week"]))),
                        wrong=[c for c in MEM if C.band(r[c]["roas"]) != gold[c]])
        vals[key] = (C.figure_values(r), call_of(r))
    return out, vals


def market_week_miss(O, v):
    """what the accounts with no channel paid in each market and week, against three ways of pricing them: mean
    absolute miss as a share of the revenue, and the miss squared over the accounts, relative to the fitted ratios'"""
    S = C.s2_strata(O, v)
    T = S["T"]
    srcs = S["hidden"] + [S["org"]]
    pn, pv = S["pn"], S["pv"]
    act, n = pv.sum(2), np.maximum(pn.sum(2), 1)
    X = {i: (S["nc"][i] * T["vc"][i][None, None, :]).sum(2) for i in srcs}
    r, rc, rp = C.s2_fit(O, v), C.s2_fit(O, v, common=True), C.s2_fit(O, v, markets="pooled")
    ways = {"fitted": sum(X[i] * r[i] for i in srcs), "one_ratio": sum(X[i] * rc[i] for i in srcs),
            "markets_pooled": sum(X[i] * rp[i] for i in srcs),
            "pool_value": (pn * (pv.sum((0, 1)) / np.maximum(pn.sum((0, 1)), 1))[None, None, :]).sum(2)}
    miss = {k: float(np.abs(p - act).sum() / act.sum()) for k, p in ways.items()}
    sq = {k: float((((p - act) ** 2) / n).sum()) for k, p in ways.items()}
    return dict(miss_pct={k: round(100 * x, 1) for k, x in miss.items()},
                squared_over_fitted={k: round(x / sq["fitted"], 2) for k, x in sq.items()})


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


def pooled_block(O, v, g):
    """the second step's fit with the three markets pooled, week by week: each ratio and its spread beside the
    market-weeks', and what it files"""
    srcs, b, V = C.s2_fit(O, v, cov=True)
    _s, bp, Vp = C.s2_fit(O, v, cov=True, markets="pooled")
    se, sep = np.sqrt(np.diag(V)), np.sqrt(np.diag(Vp))
    names = [C.SOURCES[i] for i in srcs]
    r = A.route(O, markets="pooled")
    return dict(rows=C.MATURE, rows_market_weeks=3 * C.MATURE,
                sources={nm: dict(ratio=round(float(bp[j]), 3), se=round(float(sep[j]), 3),
                                  ratio_market_weeks=round(float(b[j]), 3), se_market_weeks=round(float(se[j]), 3))
                         for j, nm in enumerate(names)},
                se_times=[math.floor(10 * float((sep / se).min())) / 10.0, math.floor(10 * float((sep / se).max())) / 10.0],
                paid_per_install={c: round(float(r[c]["v12"]), 2) for c in IOS},
                return_plan={c: stated("return " + c, r[c]["roas"]) for c in MEM},
                wrong=[c for c in MEM if C.band(r[c]["roas"]) != C.band(g[c]["roas"])])


CARRY_SHARE = (("at_share", "plain"), ("weekly_shares", "plain-dist"), ("geometric_mean", "plain-geo"),
               ("median_week", "plain-median"))
CARRY_HELD = ("at_share", "weekly_shares")                         # the two forms that add up to the installs counted
CARRY_WEEKS = (("both_years", {}, slice(0, C.WEEKS)), ("first_year", dict(dbar_weeks=C.MATURE), slice(0, C.MATURE)),
               ("second_year", dict(dbar_from=C.MATURE), slice(C.MATURE, C.WEEKS)))


def carry_block(O, v, g):
    """how the fitted installs are carried to the plan. The golden's carry scales the installs equation's budget and
    month terms so that they add up to the installs on record; the equation's own prediction with the share of the
    budget spent put in from outside need not. For each such prediction (the share over both years, the first or the
    second; put at its ratio of totals, put week by week through the delivery term and averaged, put at its geometric
    mean or at its median week): what it adds up to over the weeks the share is taken from, at their own budgets, as
    a percentage of the installs counted in those weeks, and the returns it would file"""
    coef = C.response(O, v)
    out = dict(rescale={}, adds_up_pct={}, returns={}, installs_week={}, wrong={})
    for wkey, wkw, sl in CARRY_WEEKS:
        for skey, carry in CARRY_SHARE:
            key = skey + "_" + wkey
            r = A.route(O, carry=carry, **wkw)
            out["returns"][key] = {c: stated("return " + c, r[c]["roas"]) for c in MEM}
            out["installs_week"][key] = {c: stated("installs a week " + c, r[c]["installs_week"]) for c in MEM}
            out["wrong"][key] = [c for c in MEM if C.band(r[c]["roas"]) != C.band(g[c]["roas"])]
            out["adds_up_pct"][key] = {}
    for c in MEM:
        ci = C.ORDER.index(c)
        Bc = O.B[c]
        lb = np.log(Bc["budget"])
        ld = np.log(Bc["spend"]) - lb
        d = float(coef["i"]["d"][ci])
        fit = np.exp(coef["i"]["a"][ci] + coef["i"]["s"][ci] * (lb - lb.mean()) + coef["i"]["mon"][ci][C.WMONTH - 1])
        out["rescale"][c] = round(float(O.agg[c].sum() / fit.sum()), 3)
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
    # how far short of some channel's installs each refused prediction falls, over the weeks its share is taken from
    short = [round(100 - min(out["adds_up_pct"][k].values()), 1) for k in refused]
    out["refused_short_pct"] = [min(short), max(short)]
    out["held_short_pct"] = round(100 - min(hv), 1)
    out["refused_pct"] = [min(out["adds_up_pct"][k][c] for k in refused for c in MEM),
                          max(out["adds_up_pct"][k][c] for k in refused for c in MEM)]
    out["delivery_slopes"] = [round(float(min(coef["i"]["d"][C.ORDER.index(c)] for c in MEM)), 2),
                              round(float(max(coef["i"]["d"][C.ORDER.index(c)] for c in MEM)), 2)]
    return out


def _response_rows(O, v, eq="i"):
    """the weekly record as the response fit sees it, every channel of the records: the channel, the week's budget over
    the channel's mean budget, the log of the share of it spent about its mean, the month, and the log of the week's
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
    """the form of the response, on the weekly record of every channel with the month pattern and the delivery term
    refitted each time. Installs: a power of the budget (the fit), a straight line in it and an exponential in it,
    each with the other's term added channel by channel, as an F on the added terms. Value per install: each plan
    channel's budget slope against its own spread"""
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
    # the value equation's budget slopes with their spreads (one variance for every week)
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
    # each form on the weeks the team moved a budget, each move left out of the fit in turn: the installs missed in
    # them. The straight line here is fitted on the installs themselves, each channel its own line, the month pattern
    # added on and the log of the share spent beside it; the power form and the exponential are fitted on the log
    I = np.exp(y)
    rows = np.arange(n)
    Xp, Xb = _design(ch, z, mo, [lB]), _design(ch, z, mo, [B])
    how = {"power": (Xp, y, np.exp), "line": (Xb, I, lambda x: x), "exponential": (Xb, y, np.exp)}
    miss = {k: [0.0, 0.0] for k in how}
    ga = C.ORDER.index("Google Android")
    up = dn = 0.0
    for ci, c in enumerate(C.ORDER):
        for w0, kk, f_ in O.pushes[c]:
            te = ci * C.WEEKS + np.arange(w0, min(w0 + kk, C.WEEKS))
            tr = np.setdiff1d(rows, te)
            for key, (Xk, yk, back) in how.items():
                pr = back(Xk[te] @ np.linalg.lstsq(Xk[tr], yk[tr], rcond=None)[0])
                miss[key][0] += float(np.abs(pr - I[te]).sum())
                miss[key][1] += float(I[te].sum())
                if key == "line" and ci == ga:
                    up, dn = up + (float(pr.sum()) if f_ > 1 else 0.0), dn + (float(pr.sum()) if f_ < 1 else 0.0)
    # the two straight lines carried to the plan the way step 7 carries the fit: the budget and month terms scaled to
    # add up to the installs on record, the value equation as fitted. "levels" is the line fitted on the installs,
    # "log" the budget plus a constant times the month pattern and the delivery term, fitted on the log
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
        lines = {"levels": lambda bn, mon_: bl[3 * ci] + bl[3 * ci + 2] * bn + monl[mon_ - 1],
                 "log": lambda bn, mon_: (bn + k_line[ci]) * np.exp(bm[2 * ci] + monm[mon_ - 1])}
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
                sse={k: round(x, 4) for k, x in (("power", s_pow), ("line", s_line), ("exponential", s_exp),
                                                  ("power_and_budget", s_both), ("line_and_log", s_line_log))},
                value_slopes=slopes,
                value_slope_range=[min(x["slope"] for x in slopes.values()), max(x["slope"] for x in slopes.values())],
                value_slope_spreads=min(x["spreads_from_nought"] for x in slopes.values()))


def figures(X):
    O, g, fam, lat, direct, rig = X["O"], X["golden"], X["family"], X["lattice"], X["direct"], X["rigorous"]
    gf = C.figure_values(g)
    ff = [C.figure_values(r) for _n, r in fam]
    lf = {k: C.figure_values(lat[k]) for k in KEYS}
    df, rf = C.figure_values(direct), C.figure_values(rig)
    fids = [nm + c for nm, _k in C.FAMILIES for c in MEM]
    fig = {"call": call_of(g), "bands": {c: C.band(g[c]["roas"]) for c in MEM}}
    fig["by_band"] = {b: [c for c in MEM if fig["bands"][c] == b] for b in ("scale", "hold", "cut")}
    nb = X["counts"].get("beside", 0)                          # the ways beside the battery sit last in the family
    val, band = {}, {}
    for fid in fids:
        val[fid] = stated(fid, gf[fid])
        band[fid] = band_of(fid, gf[fid], [x[fid] for x in ff[:len(ff) - nb]], [x[fid] for x in ff[len(ff) - nb:]])
    fig["figure"], fig["figure_band"] = val, band
    for nm, key in FAM_KEY.items():
        fig[key] = {c: val[nm + c] for c in MEM}
        fig[key + "_band"] = {c: band[nm + c] for c in MEM}
    fig["paid_per_install_android"] = {c: val["paid per install " + c] for c in ANDROID}
    fig["paid_per_install_ios"] = {c: val["paid per install " + c] for c in IOS}
    fig["returns"] = {fid: val[fid] for fid in fids if fid.startswith(("return ", "stretch return "))}
    fig["next_euros"] = {fid: val[fid] for fid in fids if fid.startswith(("next euro ", "stretch next euro "))}
    fig["components"] = {s: dict(id=fid, value=val[fid], band=band[fid]) for s, fid in C.COMPONENTS.items()}
    # the routes, for the workbook's routes sheet and the blocks' rejected figures
    routes = {"golden": g, "direct": direct, "rigorous": rig}
    routes.update({k: lat[k] for k in KEYS})
    fig["routes"] = {k: {c: {FAM_KEY[nm]: stated(nm + c, r[c][kk]) for nm, kk in C.FAMILIES} | {"band": C.band(r[c]["roas"])}
                         for c in MEM} for k, r in routes.items()}
    fig["route_calls"] = {k: call_of(r) for k, r in routes.items()}
    fig["route_names"] = dict(ROUTE_NAME, direct="the records as they stand, the installs the export names, the mature year's "
                                                 "return carried over",
                              rigorous="the stores' true-up period by period, every postback at the named installs' value "
                                       "times Apple Search Ads' ratio, the response fitted on spend")
    fig["distinct_wrong_calls"] = len({tuple(call_of(lat[k])) for k in KEYS})
    fig["route_outside"] = {k: [fid for fid in fids if not band[fid][0] <= stated(fid, x[fid]) <= band[fid][1]]
                            for k, x in list(lf.items()) + [("direct", df), ("rigorous", rf)]}
    bat, bes = fam[:len(fam) - nb], fam[len(fam) - nb:]
    fig["variants"] = len(bat)
    fig["variant_counts"] = X["counts"]
    fig["band_pad_pct"] = round(100 * BAND_PAD, 1)
    fig["beside_pad_pct"] = round(100 * BESIDE_PAD, 1)
    fig["single_variants"] = [n for n, _r in fam[:X["counts"]["singles"]]]
    # the ways beside the battery: the finer rows of the second step's fit, the unrescaled prediction of the third's
    kwof = dict(C.BESIDE)
    of = lambda key: [(n, r) for n, r in bes if key in kwof[n]]
    rows_, carry_, cells_, weeks_ = of("rows"), of("carry"), of("cells"), of("weeks_v")
    assert len(rows_) + len(carry_) + len(cells_) + len(weeks_) == len(bes), "every way beside the battery sits in a family"
    span = lambda rs, c, k, nd: [round(min(float(r[c][k]) for _n, r in rs), nd), round(max(float(r[c][k]) for _n, r in rs), nd)]
    fig["beside"] = dict(
        names=[n for n, _r in bes],
        finer_rows=dict(ways=len(rows_), paid_per_install={c: span(rows_, c, "v12", 2) for c in IOS},
                        return_plan={c: span(rows_, c, "roas", 3) for c in IOS}),
        unrescaled=dict(ways=len(carry_), return_plan={c: [stated("return " + c, r[c]["roas"]) for _n, r in carry_] for c in MEM},
                        installs_week={c: [int(round(float(r[c]["installs_week"]))) for _n, r in carry_] for c in MEM},
                        return_span={c: span(carry_, c, "roas", 3) for c in MEM},
                        installs_span={c: [int(round(x)) for x in span(carry_, c, "installs_week", 6)] for c in MEM}),
        grouped=dict(ways=len(cells_), next_euro={c: span(cells_, c, "marginal", 3) for c in MEM},
                     next_euro_stretch={c: span(cells_, c, "marginal_s", 3) for c in MEM},
                     return_plan={c: span(cells_, c, "roas", 3) for c in MEM}),
        value_weeks=dict(ways=len(weeks_), next_euro={c: span(weeks_, c, "marginal", 3) for c in MEM},
                         next_euro_stretch={c: span(weeks_, c, "marginal_s", 3) for c in MEM},
                         return_plan={c: span(weeks_, c, "roas", 3) for c in MEM}),
        edges=sorted(fid for fid in fids if band[fid] != band_of(fid, gf[fid], [x[fid] for x in ff[:len(ff) - nb]])))
    worst = min((abs(r[c]["roas"] - l), c, n) for n, r in bat for c in MEM for l in C.LINES)
    fig["nearest_variant"] = {"distance": math.floor(worst[0] * 1000) / 1000.0, "channel": worst[1], "variant": worst[2]}
    worst = min((abs(r[c]["roas"] - l), c, n) for n, r in bes for c in MEM for l in C.LINES)
    fig["nearest_beside"] = {"distance": math.floor(worst[0] * 1000) / 1000.0, "channel": worst[1], "variant": worst[2]}
    fig["family_calls_all_golden"] = all(call_of(r) == fig["call"] for _n, r in fam)
    # the ways beside the battery crossed with it (each with every single way it can be taken with, and with one way
    # of each of the other two steps at once): whether any crossing moves a band, and the nearest to a line
    cr = X.get("crossed") or []
    if cr:
        worst = min((abs(r[c]["roas"] - l), c, n, float(r[c]["roas"]), l) for n, r in cr for c in MEM for l in C.LINES)
        fig["crossed"] = dict(
            crossings=len(cr), moved=sorted(n for n, r in cr if call_of(r) != fig["call"]),
            nearest=dict(distance=math.floor(worst[0] * 1000) / 1000.0, channel=worst[1], variant=worst[2],
                         return_plan=stated("return " + worst[1], worst[3]), line=worst[4]),
            return_range={c: [round(min(float(r[c]["roas"]) for _n, r in cr), 3),
                              round(max(float(r[c]["roas"]) for _n, r in cr), 3)] for c in MEM})
    fig["variant_range"] = {c: [round(min(float(r[c]["roas"]) for _n, r in fam), 3),
                                round(max(float(r[c]["roas"]) for _n, r in fam), 3)] for c in MEM}
    # the corners two ranges could carry a return to: installs a week and value per install at their far edges together
    corners = {}
    for c in MEM:
        sp = float(O.plan[c].sum())
        lo = band["installs a week " + c][0] * 52 * band["value at plan " + c][0] / sp
        hi = band["installs a week " + c][1] * 52 * band["value at plan " + c][1] / sp
        corners[c] = dict(low=round(lo, 3), high=round(hi, 3), band_holds=C.band(lo) == C.band(hi) == fig["bands"][c])
    fig["corners"] = corners
    # every channel of the records, for the working sheets (Apple Search Ads sits outside the plan)
    v = X["v"]
    T = C.s2_cells(O, v)
    ch = {}
    for ci, c in enumerate(C.ORDER):
        n12 = float(O.agg[c][:C.MATURE].sum())
        lab = (O.label == ci) & O.mature
        Bc = O.B[c]
        dbar = float(Bc["spend"].sum() / Bc["budget"].sum())
        sp = O.plan[c] if c in O.plan else O.brand[c]
        row = dict(installs_mature=int(round(n12)), named_mature=int(lab.sum()),
                   paid_per_install=round(float(g[c]["v12"]), 2), recorded_per_install=round(float(g[c]["rec12"] / n12), 2),
                   unrecorded_pct=round(100 * float(g[c]["unrec"]), 1),
                   true_up_per_install=round(float(lat["S1"][c]["v12"]), 2),
                   spend_mature=round(float(Bc["spend"][:C.MATURE].sum()), 2),
                   delivery_share=round(dbar, 3),
                   budget_elasticity=round(float(g[c]["el"]), 3), value_slope=round(float(g[c]["qs"]), 3),
                   spend_elasticity=round(float(lat["S3"][c]["el"]), 3), spend_value_slope=round(float(lat["S3"][c]["qs"]), 3),
                   installs_week_plan=int(round(float(g[c]["installs_week"]))),
                   installs_week_spend_fit=int(round(float(lat["S3"][c]["installs_week"]))),
                   installs_week_history=int(round(float(O.agg[c].sum() / C.WEEKS))),
                   plan_weekly_spend=int(round(float(sp.mean()))), plan_year_spend=int(round(float(sp.sum()))),
                   plan_weekly_budget=int(round(float((sp / dbar).mean()))),
                   history_weekly_spend=int(round(float(Bc["spend"].mean()))),
                   year_weekly_spend=int(round(float(Bc["spend"][:C.MATURE].mean()))),
                   history_weekly_budget=int(round(float(Bc["budget"].mean()))),
                   budget_low=int(Bc["budget"].min()), budget_high=int(Bc["budget"].max()), moves=len(O.pushes[c]),
                   live_weeks={m: int((O.spend_mw[ci, j] > 0).sum()) for j, m in enumerate(C.MARKETS)})
        if c in MEM:
            row.update(stretch_weekly_spend=round(float(O.stretch[c].mean()), 1),
                       stretch_factor=round(float((O.stretch[c] / O.plan[c]).mean()), 2))
        if c in C.GATED:
            n_named = float(T["n"][ci].sum())
            v_named = float(v[lab & O.consent].mean())
            row.update(named_pct=round(100 * n_named / n12, 1), named_value=round(v_named, 2),
                       declined_value=round((float(g[c]["v12"]) * n12 - n_named * v_named) / (n12 - n_named), 2),
                       named_price_per_install=round(float(lat["S2"][c]["v12"]), 2),
                       search_ads_ratio_per_install=round(float(A.route(O, s2="ratio")[c]["v12"]), 2))
        ch[c] = row
    fig["channels"] = ch
    fig["stores"], webq = store_block(O, X["fits"])
    fig["web_continuation"] = round(webq, 3)
    fig["period_starts"] = [(dt.date(2024, 11, 4) + dt.timedelta(days=int(math.ceil(k * C.MONTH_DAYS)))).isoformat()
                            for k in range(A.NM)]
    fig["ratios"] = ratio_block(O, v)
    fig["ratios"]["market_weeks"] = market_week_miss(O, v)
    fig["ratios"]["markets_pooled"] = pooled_block(O, v, g)
    fig["carry"] = carry_block(O, v, g)
    fig["forms"] = form_block(O, v)
    fig["shortcuts"], sv = shortcuts(O, g)
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
        monthly_charges_recorded=int(O.rec.sum()), web_subscribers=int((O.web & (O.rec[:, 0] | O.rec_a0)).sum()),
        thin_cell=20, market_weeks=3 * C.MATURE, early_postback_installs=O.rows["early_halves"])
    fig["policy"] = dict(lines=[0.90, 1.20], vat_pct=[21, 22, 23], commission_pct=15, fee_pct=3, monthly=9.99, annual=59.99,
                         trial_days=7, version=3, cadence_days=C.MONTH_DAYS)
    fig["plan_blocks"] = A.plan_blocks(O)
    fig["unrecorded_pct"] = dict(low=min(ch[c]["unrecorded_pct"] for c in MEM), high=max(ch[c]["unrecorded_pct"] for c in MEM))
    return fig, dict(gf=gf, ff=ff, lf=lf, df=df, rf=rf, fids=fids, sv=sv)


def spec_of(X, fig, R):
    """the core's spec rebuilt on the cut pack, each figure with the range the answer blocks state"""
    g, fam, lat, direct, rig = X["golden"], X["family"], X["lattice"], X["direct"], X["rigorous"]
    T = C.truth_at_plan()
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
                         band=list(fig["figure_band"][fid]), family=[float(x[fid]) for x in R["ff"]],
                         lattice={k: float(R["lf"][k][fid]) for k in KEYS}, routes=dict(rigorous=float(R["rf"][fid]))))
    refs = list(X["refs"].values())

    def sep(r):
        ge = abs(r["golden"] - r["truth"])
        return min(abs(x - r["truth"]) for x in r["rivals"].values()) / max(ge, 1e-12)
    weakest = min(refs, key=sep)
    return dict(task="task1", call="lines", members=members, stumps=STUMPS,
                lattice={k: {c: float(lat[k][c]["roas"]) for c in MEM} for k in KEYS},
                referee=dict(slice=weakest["slice"], covers_target=False, truth=weakest["truth"], golden=weakest["golden"],
                             rivals=weakest["rivals"]), figures=C.as_stated(figs)), T, [sep(r) for r in refs]


def result_values(fv, call):
    """one route's answers in the shape of the seven results"""
    pick = lambda nm, cs: {c: fv[nm + c] for c in cs}
    return {"R1": pick("paid per install ", ANDROID), "R2": pick("paid per install ", IOS),
            "R3": pick("installs a week ", MEM), "R4": pick("value at plan ", MEM),
            "R5": {k: fv[k] for k in fv if k.startswith(("return ", "stretch return "))},
            "R6": {k: fv[k] for k in fv if k.startswith(("next euro ", "stretch next euro "))}, "R7": call}


def effort(X, fig, R, pert):
    g, fam, lat, direct = X["golden"], X["family"], X["lattice"], X["direct"]
    st = lambda figs: {fid: stated(fid, figs[fid]) for fid in R["fids"]}
    gold = result_values(fig["figure"], fig["call"])
    quick = result_values(st(R["df"]), call_of(direct))
    careful = result_values(st(R["lf"]["S1+S2+S3"]), call_of(lat["S1+S2+S3"]))
    fb = fig["figure_band"]
    cells = lambda nm, cs: {c: fb[nm + c] for c in cs}
    meta = [
        ("R1", "what an install on each Android channel went on to pay in twelve months", "Component 1, Ask 4",
         "paid_per_install_android", [], "the stores' reports, the billing records and the accounts' last opens",
         dict(bands=cells("paid per install ", ANDROID)), ["L44", "N21"]),
        ("R2", "what an install on each iOS network went on to pay in twelve months", "Component 2, Ask 4",
         "paid_per_install_ios", ["R1"], "", dict(bands=cells("paid per install ", IOS)), ["L57", "L53", "N27", "L58"]),
        ("R3", "the installs a week the plan's spend buys", "Component 3, Ask 2", "installs_week", [],
         "the budget sheet, the daily spend and the weekly installs",
         dict(bands=cells("installs a week ", MEM), partly_share=0.25), ["L51", "L37", "L28"]),
        ("R4", "the twelve-month net revenue per install of the installs the plan's spend buys", "Ask 2", "value_plan",
         ["R1", "R2", "R3"], "", dict(bands=cells("value at plan ", MEM)), ["N21", "N27", "L56"]),
        ("R5", "each channel's return per euro at the plan's and at the stretch spend", "Ask 1", "returns", ["R3", "R4"], "",
         dict(bands={k: fb[k] for k in gold["R5"]}), ["N21", "N27", "L56"]),
        ("R6", "what one more euro returns on top of the plan's weekly spend and on top of the stretch spend", "Ask 3",
         "next_euros", ["R3", "R4"], "", dict(bands={k: fb[k] for k in gold["R6"]}), ["L51", "L37", "L28"]),
        ("R7", "each channel's band", "Recommendation", "call", ["R5"], "", {}, ["N21", "N27", "L56"]),
    ]
    res = []
    for rid, name, graded, key, dep, indep, extra, prec in meta:
        r = {"id": rid, "name": name, "graded_as": graded, "figure": key, "depends": dep, "independent": indep,
             "golden": gold[rid], "passes": {"quick": quick[rid], "careful": careful[rid], "thorough": gold[rid]},
             "precedent": prec}
        r.update(extra)
        res.append(r)
    by = {r["id"]: r for r in res}

    def grades(figs, call):
        v = result_values(st(figs), call)
        return {rid: EF.grade(v[rid], by[rid])[0] for rid in by}
    g_lost = {k: grades(R["lf"][k], call_of(lat[k])) for k in KEYS}
    alone_key = {"S1": "S2+S3", "S2": "S1+S3", "S3": "S1+S2"}
    names = {"S1": "the stores' excess over the billing records belongs to the subscriptions last seen still set to renew, "
                   "carried at a continuation fitted to that excess",
             "S2": "each network's installs that declined tracking sit unnamed among the accounts with no channel and are "
                   "worth a different fraction of its named ones, one fraction per source fitted together",
             "S3": "a week's spend is the platform's delivery of the week's budget, so what a budget buys is read on the "
                   "budget with the delivery beside it and carried to the budget that delivers the plan's spend"}
    judgments = []
    for s in ("S1", "S2", "S3"):
        ak = alone_key[s]
        judgments.append({"id": s, "name": names[s], "kind": "stump", "precedent": STUMPS[s]["precedents"],
                          "dropped": {"answer": call_of(lat[s]), "results_moved": [r for r, x in g_lost[s].items() if x != "right"]},
                          "alone": {"answer": call_of(lat[ak]), "results_rescued": [r for r, x in g_lost[ak].items() if x == "right"]}})
    judgments += [
        {"id": "J4", "name": "each iOS network's installs counted from its install postbacks", "kind": "reflex", "precedent": ["R81"]},
        {"id": "J5", "name": "re-sent rows, reinstalls, staff and test accounts and sandbox charges left out", "kind": "reflex",
         "precedent": ["R80"]},
        {"id": "J6", "name": "net revenue at the policy's VAT, commission and fee, over the 365 days from the install",
         "kind": "reflex", "precedent": []},
        {"id": "J7", "name": "a response curve with a month pattern and held-out weeks fitted to the weekly record",
         "kind": "reflex", "precedent": ["R92"]}]
    F = {"golden_answer": fig["call"], "reflex_route": {"answer": call_of(lat["S1+S2+S3"])}, "judgments": judgments}
    routes = [{"name": "the golden", "answer": fig["call"], "golden": True}]
    routes += [{"name": ROUTE_NAME[k], "answer": call_of(lat[k])} for k in KEYS]
    routes.append({"name": fig["route_names"]["direct"], "answer": call_of(direct)})
    singles = fam[:X["counts"]["singles"]]
    nb = X["counts"].get("beside", 0)
    crossed = fam[len(singles):len(fam) - nb]
    forcing = {"kind": "set", "golden_answer": fig["call"],
               "golden_family": [{"name": "the golden", "answer": fig["call"]}] + [{"name": n, "answer": call_of(r)} for n, r in singles]
               + [{"name": "every pair and every triple of those ways, one from each step (%d)" % len(crossed),
                   "answer": fig["call"] if all(call_of(r) == fig["call"] for _n, r in crossed) else ["a crossed way moves the call"]}]
               + [{"name": n, "answer": call_of(r)} for n, r in fam[len(fam) - nb:]],
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": "%s, times %.3f" % (n, f), "answer": sorted("%s: %s" % (c, C.band(x[c])) for c in MEM)}
                                 for n, f, x, _ok in pert]}
    hints = [{"sentence": STUMPS[s]["said_out_loud"], "rescues": [r for r, x in g_lost[alone_key[s]].items() if x == "right"]}
             for s in ("S1", "S2", "S3")]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


def run(target, cross=True):
    X = A.run(target, cross=cross)
    fig, R = figures(X)
    pert = C.forcing(X["O"])
    fig["perturbations"] = [{"input": n, "factor": round(f, 3), "call_holds": bool(ok),
                             "returns": {c: round(x[c], 3) for c in MEM},
                             "nearest": round(min(abs(x[c] - l) for c in MEM for l in C.LINES), 3)} for n, f, x, ok in pert]
    fig["delivery_share_spread_pct"] = round(100 * C.quarter_departure(X["O"]), 1)
    spec, T, seps = spec_of(X, fig, R)
    rows, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))
    lines = corelib._criteria([f for f in earn["figs"] if f["block"] == "asks"])     # one criterion per answer line
    comps = [f for f in earn["figs"] if f["block"] == "components"]

    def landed(val):
        """the answer lines a route's figures earn whole, the components it earns, and every figure it lands"""
        return ([c[0]["sentence"] for c in lines if all(corelib._earned(f, val(f)) for f in c)],
                [f["id"] for f in comps if corelib._earned(f, val(f))],
                [f["id"] for f in earn["figs"] if f["id"] == C.stated_id(f["id"]) and corelib._earned(f, val(f))])
    lands = {k: landed(lambda f, k=k: f["values"][key(k)]) for k in KEYS}
    fig["rubric"] = {"level": level, "fails": [r[0] + ": " + r[2] for r in rows if r[1] == "FAIL"],
                     "rows": [list(r) for r in rows],
                     "one_lost": {s: round(earn["earn"][key(s)], 1) for s in ("S1", "S2", "S3")},
                     "fixed_alone": {"S1": round(earn["earn"][key("S2+S3")], 1), "S2": round(earn["earn"][key("S1+S3")], 1),
                                     "S3": round(earn["earn"][key("S1+S2")], 1)},
                     "two_lost": {k: round(earn["earn"][key(k)], 1) for k in ("S1+S2", "S1+S3", "S2+S3")},
                     "reflex": round(earn["earn"][key("S1+S2+S3")], 1), "rigorous": round(earn["rigorous"], 1),
                     "lines": len(lines), "figures": len({C.stated_id(f["id"]) for f in earn["figs"]}),
                     "lands": {k: len(v[0]) for k, v in lands.items()},
                     "figures_landed": {k: len(v[2]) for k, v in lands.items()},
                     "reflex_lands": lands["S1+S2+S3"][0], "reflex_figures": lands["S1+S2+S3"][2],
                     "referee_separation": [round(x, 1) for x in seps]}
    gcall = call_of(X["golden"])
    for k, (fv, call) in R["sv"].items():                      # each simpler way on the rubric, the other two steps golden
        val = lambda f, fv=fv: fv[C.stated_id(f["id"])]
        kept = landed(val)
        fig["shortcuts"][k].update(
            earns=round(corelib._score(earn["figs"], call == gcall, val), 1), asks_kept=len(kept[0]),
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
    print(json.dumps({k: fig[k] for k in ("call", "rubric", "nearest_variant", "result_grades", "check_web", "check_android",
                                           "check_moves", "holdout", "stores", "ratios", "corners", "steps", "plan_blocks",
                                           "variant_counts", "perturbations")}, indent=1, default=float)[:30000])
    for fid in fig["figure"]:
        print("%-36s %10s  %s" % (fid, fig["figure"][fid], fig["figure_band"][fid]))
