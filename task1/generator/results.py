"""Every owed figure, computed on the shipped files: figures.json (what the answer blocks and the goldens state)
and effort.json (each result's golden, band and the three passes, the stump factorial, the forcing on both sides),
with the core's rubric table re-priced on the cut pack by corelib."""
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
LOST = {"S1": "the billing records trued up to the stores' reports month by month",
        "S2": "every postback priced at the named installs' value by first-48-hour value",
        "S3": "installs and value per install fitted on the week's spend"}
ROUTE_NAME = {k: "; ".join(LOST[s] for s in k.split("+")) for k in KEYS}
FAM_KEY = {"return ": "return_plan", "stretch return ": "return_stretch", "value at plan ": "value_plan",
           "next euro ": "next_euro"}
REVENUE = ("plan revenue iOS networks", "stretch adds", "plan revenue", "stretch revenue", "plan revenue Android")


BAND_PAD = 0.005


def unit(fid):
    """(scale, decimals) a figure is stated at"""
    if fid.startswith("unrecorded share"):
        return 100.0, 1
    if fid in REVENUE:
        return 1.0, -3
    return 1.0, 2


def stated(fid, x):
    s, nd = unit(fid)
    v = round(float(x) * s, nd)
    return int(v) if nd <= 0 else v


def band_of(fid, g, fam):
    """the battery's range with half a per cent of the figure each side (what two builds of one variant differ by),
    stated outward at the figure's precision"""
    s, nd = unit(fid)
    lo, hi = min(list(fam) + [g]), max(list(fam) + [g])
    w = BAND_PAD * abs(g)
    f = 10.0 ** nd
    a = math.floor((lo - w) * s * f + 1e-9) / f
    b = math.ceil((hi + w) * s * f - 1e-9) / f
    return [int(round(a)), int(round(b))] if nd <= 0 else [round(a, nd), round(b, nd)]


def call_of(res):
    return sorted("%s: %s" % (c, C.band(res[c]["roas"])) for c in MEM)


def at_plan_x(O, coef, c, v12, dbar_scale=1.0):
    """core.at_plan with the workbook's plan and stretch columns and a movable delivery share"""
    ci = C.ORDER.index(c)
    Bc = O.B[c]
    sp = O.plan[c] if c in O.plan else O.brand[c]
    dbar = Bc["spend"].sum() / Bc["budget"].sum() * dbar_scale
    x_hist = np.log(Bc["budget"]) - np.log(Bc["budget"]).mean()
    x_plan = np.log(sp / dbar) - np.log(Bc["budget"]).mean()
    si, sv = coef["i"]["s"][ci], coef["v"]["s"][ci]
    mi, mv = coef["i"]["mon"][ci], coef["v"]["mon"][ci]
    back = O.agg[c].sum() / np.exp(coef["i"]["a"][ci] + si * x_hist + mi[C.WMONTH - 1]).sum()
    fm = np.exp(sv * x_hist[:C.MATURE] + mv[C.WMONTH[:C.MATURE] - 1])
    wt = O.agg[c][:C.MATURE]
    level = v12 / ((fm * wt).sum() / wt.sum())
    st = float(np.log((O.stretch[c] / O.plan[c]).mean())) if c in O.plan else 0.0
    out = {}
    for tag, lift in (("", 0.0), ("_s", st)):
        n = back * np.exp(coef["i"]["a"][ci] + si * (x_plan + lift) + mi[C.PLAN_MONTH - 1])
        vp = level * np.exp(sv * (x_plan + lift) + mv[C.PLAN_MONTH - 1])
        out["roas" + tag] = (n * vp).sum() / (sp.sum() * np.exp(lift))
        out["revenue" + tag] = (n * vp).sum()
        if not tag:
            out.update(installs_week=n.mean(), vpi=(n * vp).sum() / n.sum())
    out.update(marginal=out["roas"] * (si + sv), el=si, qs=sv)
    return out


def route_from(O, v, r_scale=1.0, el_scale=1.0, qs_scale=1.0, dbar_scale=1.0):
    """the golden route from a given set of account values, with one fitted input moved"""
    T = C.s2_cells(O, v)
    r0 = T["r"]
    T["r"] = r0 * r_scale
    try:
        v12 = C.channel_values(O, v)
        coef = C.response(O, v)
    finally:
        T["r"] = r0
    coef["i"]["s"] = coef["i"]["s"] * el_scale
    coef["v"]["s"] = coef["v"]["s"] * qs_scale
    return {c: at_plan_x(O, coef, c, v12[c], dbar_scale) for c in C.ORDER}


def perturbations(O, X):
    """each fitted input moved by a fifth (the delivery share, a ratio of two recorded totals, by its widest
    quarter's departure on any channel), the rest of the golden route unchanged"""
    out = []
    fits = X["fits"]

    def with_fits(name, f):
        v = C.s1_values(O, "golden", fits=f)[0]
        out.append((name, route_from(O, v)))
    for sgn, tag in ((0.8, "a fifth lower"), (1.2, "a fifth higher")):
        f = {pl: dict(x, c_m=x["c_m"] * sgn, c_a=x["c_a"] * sgn) for pl, x in fits.items()}
        with_fits("the share of trial-end candidates the stores charged, " + tag, f)
        f = {pl: dict(x, q=1 - (1 - x["q"]) * sgn, q1=1 - (1 - x["q"]) * sgn) for pl, x in fits.items()}
        with_fits("the monthly lapse of a subscription the app no longer sees, " + tag, f)
    v = X["v"]
    halves = []
    for c in C.ORDER:
        b, s = O.B[c]["budget"], O.B[c]["spend"]
        whole = s.sum() / b.sum()
        halves += [abs(s[i:i + 13].sum() / b[i:i + 13].sum() / whole - 1) for i in range(0, C.WEEKS, 13)]
    dsp = float(max(halves))
    for sgn, tag in ((0.8, "a fifth lower"), (1.2, "a fifth higher")):
        out.append(("the price ratio of the unnamed installs, " + tag, route_from(O, v, r_scale=sgn)))
        out.append(("each channel's budget elasticity of installs, " + tag, route_from(O, v, el_scale=sgn)))
        out.append(("each channel's value slope on the budget, " + tag, route_from(O, v, qs_scale=sgn)))
    for sgn, tag in ((1 - dsp, "lower"), (1 + dsp, "higher")):
        out.append(("the budget that delivers the plan's spend, %.1f per cent %s (the delivery share's widest quarter's "
                    "departure on any channel)" % (100 * dsp, "higher" if sgn < 1 else "lower"),
                    route_from(O, v, dbar_scale=sgn)))
    return out, dsp


STUMPS = {
    "S1": dict(axis="what", opens="AppLovin Android", steps_left=4, precedents=["N21", "L44"],
               said_out_loud="A store charge reaches the app's billing records only when the subscriber next opens "
                             "the app, so the stores' excess over the records belongs to subscriptions last seen "
                             "still set to renew, not to every account in proportion."),
    "S2": dict(axis="who", opens="Meta iOS", steps_left=4, precedents=["L53", "N27", "L13"],
               said_out_loud="The attribution export holds an iOS network's installs only where the user allowed "
                             "tracking, and those users are worth more than the rest even at the same first two "
                             "days; the rest sit among the accounts with no channel."),
    "S3": dict(axis="against", opens="Google Android", steps_left=3, precedents=["L51", "L37", "L28"],
               said_out_loud="A week's spend is what the platform chose to deliver of the week's budget given that "
                             "week's auction, so weeks of high and low spend are not weeks of high and low "
                             "budgets; what a budget buys shows in the weeks the team moved it."),
}


def figures(X):
    O, g, fam, lat, direct = X["O"], X["golden"], X["family"], X["lattice"], X["direct"]
    gf = C.figure_values(g)
    ff = [C.figure_values(r) for _n, r in fam]
    lf = {k: C.figure_values(lat[k]) for k in KEYS}
    df = C.figure_values(direct)
    ask_ids = [nm + c for nm, _k in C.FAMILIES for c in MEM]
    fids = ask_ids + list(C.COMPONENTS)
    fig = {"call": call_of(g), "bands": {c: C.band(g[c]["roas"]) for c in MEM}}
    fig["by_band"] = {b: [c for c in MEM if fig["bands"][c] == b] for b in ("scale", "hold", "cut")}
    val, band = {}, {}
    for fid in fids:
        val[fid] = stated(fid, gf[fid])
        band[fid] = band_of(fid, gf[fid], [x[fid] for x in ff])
    fig["figure"], fig["figure_band"] = val, band
    for nm, key in FAM_KEY.items():
        fig[key] = {c: val[nm + c] for c in MEM}
        fig[key + "_band"] = {c: band[nm + c] for c in MEM}
    fig["unrecorded_share_applovin_android_pct"] = val["unrecorded share AppLovin Android"]
    fig["value_per_install_meta_ios"] = val["value per install Meta iOS"]
    fig["return_and_value_plan"] = {fid: val[fid] for fid in ask_ids if fid.startswith(("return ", "value at plan "))}
    fig["plan_and_stretch_revenue"] = {k: val[k] for k in ("plan revenue iOS networks", "stretch adds")}
    # the routes, for the workbook's routes sheet and the blocks' rejected figures
    routes = {"golden": g, "direct": direct}
    routes.update({k: lat[k] for k in KEYS})
    fig["routes"] = {k: {c: {"return": round(float(r[c]["roas"]), 2), "stretch": round(float(r[c]["roas_s"]), 2),
                             "value": round(float(r[c]["vpi"]), 2), "next_euro": round(float(r[c]["marginal"]), 2),
                             "band": C.band(r[c]["roas"])} for c in MEM} for k, r in routes.items()}
    fig["route_calls"] = {k: call_of(r) for k, r in routes.items()}
    fig["route_figures"] = {k: {fid: stated(fid, x[fid]) for fid in fids} for k, x in list(lf.items()) + [("direct", df)]}
    fig["distinct_wrong_calls"] = len({tuple(call_of(lat[k])) for k in KEYS})
    fig["variants"] = len(fam)
    fig["band_pad_pct"] = round(100 * BAND_PAD, 1)
    fig["variant_names"] = [n for n, _r in fam]
    worst = min((abs(r[c]["roas"] - l), c, n) for n, r in fam for c in MEM for l in C.LINES)
    fig["nearest_variant"] = {"distance": math.floor(worst[0] * 1000) / 1000.0, "channel": worst[1], "variant": worst[2]}
    fig["family_calls_all_golden"] = all(call_of(r) == fig["call"] for _n, r in fam)
    fig["variant_range"] = {c: [round(min(float(r[c]["roas"]) for _n, r in fam), 3),
                                round(max(float(r[c]["roas"]) for _n, r in fam), 3)] for c in MEM}
    # the ways of taking a step that a figure from the shipped files refutes: what each files, and that figure
    ro = []
    for r in X["ruled_out"]:
        rf = C.figure_values(r["route"])
        e = dict(name=r["name"], by=r["by"], call_holds=call_of(r["route"]) == fig["call"],
                 returns={c: round(float(r["route"][c]["roas"]), 2) for c in MEM},
                 outside=[fid for fid in fids if not band[fid][0] <= stated(fid, rf[fid]) <= band[fid][1]])
        if r["by"] == "media plan":
            e["blocks"] = r["blocks"]
        elif r["by"] == "moved weeks":
            h = r["holdout"]
            e["holdout"] = dict(weeks=h["weeks"], channels=h["channels"], lower_on=h["lower_on"],
                                error_pct={k: round(100 * x, 1) for k, x in h["error"].items()},
                                error_whole={k: int(round(100 * x)) for k, x in h["error"].items()})
        elif r["by"] == "Apple Search Ads":
            e["search_ads"] = dict(installs=r["installs"], paid=round(r["paid"], 2), priced=round(r["priced"], 2))
            e["stretch_adds"] = stated("stretch adds", rf["stretch adds"])
        elif r["by"] == "Apple Search Ads by sessions":
            e["ratio"] = round(r["ratio"], 2)
            e["groups"] = {k: dict(installs=d["installs"], paid=round(d["paid"], 2), priced=round(d["priced"], 2))
                           for k, d in r["groups"].items()}
        else:
            e["annual"] = dict(excess={("Google Play", "App Store")[pl]: int(round(x)) for pl, x in r["excess"].items()},
                               candidates={("Google Play", "App Store")[pl]: x for pl, x in r["candidates"].items()})
            e["unrecorded_share"] = stated("unrecorded share AppLovin Android", rf["unrecorded share AppLovin Android"])
        ro.append(e)
    fig["ruled_out"] = ro
    # each shortcut under the other ways of taking the response: its own channel stays in the wrong band
    fig["shortcut_conventions"] = {
        sid: dict(member=d["member"], conventions=len(d["values"]), low=round(min(x for _n, x in d["values"]), 2),
                  high=round(max(x for _n, x in d["values"]), 2),
                  band=sorted({C.band(x) for _n, x in d["values"]}), golden_band=fig["bands"][d["member"]])
        for sid, d in X["shortcuts"].items()}
    fig["clock_install_time"] = {"call_holds": call_of(X["clock"]) == fig["call"],
                                 "returns": {c: round(float(X["clock"][c]["roas"]), 3) for c in MEM}}
    # every channel of the records, for the working sheets (Apple Search Ads sits outside the plan)
    v = X["v"]
    T = C.s2_cells(O, v)
    raw = C.values(O, "raw")
    ch = {}
    for ci, c in enumerate(C.ORDER):
        n12 = float(O.agg[c][:C.MATURE].sum())
        lab = (O.label == ci) & O.mature
        row = dict(installs_mature=int(round(n12)), named_mature=int(lab.sum()),
                   value_per_install=round(float(g[c]["v12"]), 2), recorded_per_install=round(float(g[c]["rec12"] / n12), 2),
                   unrecorded_pct=round(100 * float(g[c]["unrec"]), 1),
                   prop_unrecorded_pct=round(100 * float(lat["S1"][c]["unrec"]), 1),
                   spend_mature=round(float(O.B[c]["spend"][:C.MATURE].sum()), 2),
                   delivery_share=round(float(O.B[c]["spend"].sum() / O.B[c]["budget"].sum()), 3),
                   budget_elasticity=round(float(g[c]["el"]), 2), value_slope=round(float(g[c]["qs"]), 2),
                   spend_elasticity=round(float(lat["S3"][c]["el"]), 2), spend_value_slope=round(float(lat["S3"][c]["qs"]), 2),
                   installs_week_plan=round(float(g[c]["installs_week"]), 1),
                   plan_weekly_spend=int(round(float((O.plan[c] if c in O.plan else O.brand[c]).mean()))),
                   history_weekly_spend=int(round(float(O.B[c]["spend"].mean()))),
                   moves=len(O.pushes[c]))
        if c in C.GATED:
            n_named = float(T["n"][ci].sum())
            v_named = float(v[lab & O.consent].mean())
            row.update(consent_pct=round(100 * n_named / n12, 1), named_value=round(v_named, 2),
                       unnamed_value=round((float(g[c]["v12"]) * n12 - n_named * v_named) / (n12 - n_named), 2),
                       bridge_value=round(float(lat["S2"][c]["v12"]), 2))
        ch[c] = row
    fig["channels"] = ch
    fits = X["fits"]
    st = {}
    for pl, name in ((0, "Google Play"), (1, "App Store")):
        f = fits[pl]
        mk = (O.ios == bool(pl)) & ~O.web
        st[name] = dict(trial_end_share_monthly=round(f["c_m"], 3), trial_end_share_annual=round(f["c_a"], 3),
                        continuation=round(f["q"], 3), first_excess=int(round(f["F"].sum())),
                        renewal_excess=int(round(f["R"].sum())), annual_excess=int(round(f["A"].sum())),
                        trial_candidates_monthly=f["first_candidates"], trial_candidates_annual=f["annual_candidates"],
                        renewal_candidates=f["renew_candidates"],
                        store_monthly_charges=int(round(O.store[pl]["first"].sum() + O.store[pl]["ren"].sum())),
                        recorded_monthly_charges=int(O.rec[mk].sum()),
                        periods=[dict(first=int(round(a)), renewals=int(round(b)), fitted=round(float(c_), 1))
                                 for a, b, c_ in zip(f["F"], f["R"], f["fitted"])])
    fig["stores"] = st
    fig["period_starts"] = [(dt.date(2024, 11, 4) + dt.timedelta(days=int(math.ceil(k * C.MONTH_DAYS)))).isoformat()
                            for k in range(A.NM)]
    fig["web_continuation"] = round(float(C.s1_web_fit(O)), 3)
    r1, r2, r3 = X["refs"]["S1"], X["refs"]["S2"], X["refs"]["S3"]
    fig["check_web"] = dict(subscribers=r1["n"], charged=round(r1["truth"], 2), estimate=round(r1["golden"], 2),
                            true_up=round(r1["rivals"]["proportional true-up"], 2))
    fig["check_search_ads"] = dict(installs=r2["n"], paid=round(r2["truth"], 2), estimate=round(r2["golden"], 2),
                                   named_by_cell=round(r2["rivals"]["consenting installs' value by first-48-hour value"], 2),
                                   named_mean=round(r2["rivals"]["consenting installs' value"], 2))
    fig["check_moves"] = {}
    for c in C.ORDER:
        r = r3 if c == "Google Android" else C.referee_s3(O, v, c)
        fig["check_moves"][c] = dict(actual=round(r["truth"], 2), budget_fit=round(r["golden"], 2),
                                     spend_fit=round(r["rivals"]["response fitted on spend"], 2))
    pu = O.pushes["Google Android"]
    fig["check_moves_weeks"] = dict(raised=int(sum(min(w0 + k, C.WEEKS) - w0 for w0, k, f_ in pu if f_ > 1)),
                                    lowered=int(sum(min(w0 + k, C.WEEKS) - w0 for w0, k, f_ in pu if f_ < 1)),
                                    moves=len(pu))
    pool = O.mature & O.pool
    fig["unnamed"] = dict(accounts=int(pool.sum()), paid=int(round(float(v[pool].sum()))),
                          paid_per_account=round(float(v[pool].mean()), 2),
                          adding_up_named_price=round(C.adding_up(O, v, "bridge"), 2),
                          adding_up_search_ads_ratio=round(C.adding_up(O, v, "ratio"), 2),
                          adding_up_golden=round(C.adding_up(O, v, "golden"), 2),
                          network_installs=int(round(sum(T["nc"][C.ORDER.index(c)].sum() for c in C.GATED))),
                          organic_installs=int(round(float(T["nc"][len(C.ORDER)].sum()))),
                          cells=int((T["pool_n"] > 0).sum()))
    n_cons = int(O.n)
    fig["steps"] = dict(consumer_accounts=n_cons, other_accounts=O.rows["accounts"] - n_cons,
                        attribution_rows=O.rows["attribution"], attribution_extra=O.rows["attribution"] - n_cons - (O.rows["accounts"] - n_cons),
                        postbacks=O.rows["postbacks"], postbacks_used=O.rows["postbacks_used"],
                        postbacks_dropped=O.rows["postbacks"] - O.rows["postbacks_used"],
                        refunded_purchases=O.rows["refunds"], mature_weeks=C.MATURE, weeks=C.WEEKS, plan_weeks=52,
                        days=365, mature_accounts=int(O.mature.sum()), thin_cell=20)
    fig["policy"] = dict(lines=[0.90, 1.20], vat_pct=[21, 22, 23], commission_pct=15, fee_pct=3, monthly=9.99, annual=59.99,
                         trial_days=7, version=3, cadence_days=C.MONTH_DAYS)
    fig["words"] = dict(months=12, first_hours=48, cadence_alt_days=30, last_weeks=78, launch_weeks=13)
    fig["pct"] = dict(
        unrecorded_low=min(ch[c]["unrecorded_pct"] for c in MEM), unrecorded_high=max(ch[c]["unrecorded_pct"] for c in MEM),
        prop_low=min(ch[c]["prop_unrecorded_pct"] for c in MEM), prop_high=max(ch[c]["prop_unrecorded_pct"] for c in MEM),
        consent_low=min(ch[c]["consent_pct"] for c in C.GATED), consent_high=max(ch[c]["consent_pct"] for c in C.GATED),
        named_over_all={c: int(round(100 * (ch[c]["named_value"] / ch[c]["value_per_install"] - 1))) for c in C.GATED},
        bridge_over={c: int(round(100 * (float(lat["S2"][c]["v12"]) / float(g[c]["v12"]) - 1))) for c in C.GATED},
        next_euro_spend_over={c: int(round(100 * (float(lat["S3"][c]["marginal"]) / float(g[c]["marginal"]) - 1))) for c in MEM})
    return fig, dict(gf=gf, ff=ff, lf=lf, df=df, fids=fids, ask_ids=ask_ids)


def spec_of(X, fig, R):
    """the core's spec rebuilt on the cut pack, each figure with the band the answer blocks state"""
    g, fam, lat, direct = X["golden"], X["family"], X["lattice"], X["direct"]
    T = C.truth_at_plan()
    members = {c: dict(lines=list(C.LINES), truth=float(T[c]["roas"]), golden=float(g[c]["roas"]),
                       family=[float(r[c]["roas"]) for _n, r in fam],
                       routes=dict(direct=float(direct[c]["roas"]), rigorous=float(lat["S1+S2+S3"][c]["roas"])))
               for c in MEM}
    raw_band = lambda fid: [b / unit(fid)[0] for b in fig["figure_band"][fid]]
    figs = []
    for c in MEM:
        figs.append(dict(id="return " + c, block="ask", weight=1.0, member=c, band=raw_band("return " + c)))
    for fid in R["fids"]:
        if fid.startswith("return "):
            continue
        figs.append(dict(id=fid, block="component" if fid in C.COMPONENTS else "ask", weight=1.0, golden=float(R["gf"][fid]),
                         band=raw_band(fid), family=[float(x[fid]) for x in R["ff"]],
                         lattice={k: float(R["lf"][k][fid]) for k in KEYS},
                         routes=dict(rigorous=float(R["lf"]["S1+S2+S3"][fid]))))
    refs = list(X["refs"].values())

    def sep(r):
        ge = abs(r["golden"] - r["truth"])
        return min(abs(x - r["truth"]) for x in r["rivals"].values()) / max(ge, 1e-12)
    weakest = min(refs, key=sep)
    return dict(call="lines", members=members, stumps=STUMPS,
                lattice={k: {c: float(lat[k][c]["roas"]) for c in MEM} for k in KEYS},
                referee=dict(slice=weakest["slice"], covers_target=False, truth=weakest["truth"], golden=weakest["golden"],
                             rivals=weakest["rivals"]), figures=figs), T


def result_values(fig_vals, call):
    """one route's answers in the shape of the seven results"""
    return {"R1": fig_vals["unrecorded share AppLovin Android"], "R2": fig_vals["value per install Meta iOS"],
            "R3": {c: fig_vals["next euro " + c] for c in MEM},
            "R4": {k: fig_vals[k] for k in fig_vals if k.startswith(("return ", "value at plan "))},
            "R5": {c: fig_vals["stretch return " + c] for c in MEM},
            "R6": {k: fig_vals[k] for k in ("plan revenue iOS networks", "stretch adds")}, "R7": call}


def effort(X, fig, R, pert):
    g, fam, lat, direct = X["golden"], X["family"], X["lattice"], X["direct"]
    st = lambda figs: {fid: stated(fid, figs[fid]) for fid in R["fids"]}
    gold = result_values(fig["figure"], fig["call"])
    quick = result_values(st(R["df"]), call_of(direct))
    careful = result_values(st(R["lf"]["S1+S2+S3"]), call_of(lat["S1+S2+S3"]))
    fb = fig["figure_band"]
    meta = [
        ("R1", "the share of AppLovin Android's twelve-month net revenue the billing records never took in (per cent)",
         "Component 1", "unrecorded_share_applovin_android_pct", [], "the stores' reports, the billing records and the accounts' last opens",
         dict(band=fb["unrecorded share AppLovin Android"]), ["L44", "N21"]),
        ("R2", "Meta iOS's twelve-month net revenue per install over every install it bought in the 52 mature weeks",
         "Component 2", "value_per_install_meta_ios", ["R1"], "", dict(band=fb["value per install Meta iOS"]), ["L13", "N27", "L53"]),
        ("R3", "what one more euro on top of the plan's weekly spend returns, by channel", "Ask 4", "next_euro", ["R1", "R2"], "",
         dict(bands={c: fb["next euro " + c] for c in MEM}, partly_share=0.14), ["L51", "L37", "L28"]),
        ("R4", "each channel's 2027 return per euro and net revenue per install at the plan's weekly spend", "Ask 1, Ask 3",
         "return_and_value_plan", ["R1", "R2", "R3"], "", dict(bands={k: fb[k] for k in gold["R4"]}), ["N21", "N27"]),
        ("R5", "each channel's return per euro at the plan's stretch spend", "Ask 2", "return_stretch", ["R1", "R2", "R3"], "",
         dict(bands={c: fb["stretch return " + c] for c in MEM}), ["L51", "L37", "L28"]),
        ("R6", "the plan's twelve-month net revenue on the five iOS networks and what the stretch spend adds",
         "Component 3, Component 4", "plan_and_stretch_revenue", ["R4", "R5"], "",
         dict(bands={k: fb[k] for k in gold["R6"]}), ["L13", "N27", "L53"]),
        ("R7", "each channel's band", "Recommendation", "call", ["R4"], "", {}, ["N21", "N27"]),
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
    names = {"S1": "the stores' excess over the billing records belongs to the subscriptions last seen still set to renew "
                   "whose owners stopped opening the app",
             "S2": "the installs the export does not name are worth less than the named ones at the same first two days and "
                   "sit among the accounts with no channel",
             "S3": "a week's spend is the auction's outcome, so what a budget buys is read on the budget with the delivery "
                   "beside it"}
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
    routes.append({"name": "the records as they stand, the named installs, the mature year's return carried over",
                   "answer": call_of(direct)})
    forcing = {"kind": "set", "golden_answer": fig["call"],
               "golden_family": [{"name": "the golden", "answer": fig["call"]}] + [{"name": n, "answer": call_of(r)} for n, r in fam],
               "shortcuts": [{"name": r["name"], "answer": r["answer"]} for r in routes[1:]],
               "perturbations": [{"input": n, "answer": call_of(r)} for n, r in pert]}
    hints = [{"sentence": STUMPS[s]["said_out_loud"], "rescues": [r for r, x in g_lost[alone_key[s]].items() if x == "right"]}
             for s in ("S1", "S2", "S3")]
    return {"results": res, "hints": hints, "factorial": F, "forcing": forcing, "routes": routes,
            "weights": {"recommendation": 18, "components": 20, "asks": 53, "instruction": 9}}, g_lost


def run(target):
    X = A.run(target)
    fig, R = figures(X)
    pert, dsp = perturbations(X["O"], X)
    fig["perturbations"] = [{"input": n, "call_holds": call_of(r) == fig["call"],
                             "nearest": round(min(abs(r[c]["roas"] - l) for c in MEM for l in C.LINES), 3)} for n, r in pert]
    fig["delivery_share_spread_pct"] = round(100 * dsp, 1)
    spec, T = spec_of(X, fig, R)
    rows, level = corelib.check(spec)
    earn = corelib.earnings(spec)
    key = lambda k: corelib._key(k.split("+"))
    fig["rubric"] = {"level": level, "fails": [r[0] + ": " + r[2] for r in rows if r[1] == "FAIL"],
                     "one_lost": {s: round(earn["earn"][key(s)], 1) for s in ("S1", "S2", "S3")},
                     "fixed_alone": {"S1": round(earn["earn"][key("S2+S3")], 1), "S2": round(earn["earn"][key("S1+S3")], 1),
                                     "S3": round(earn["earn"][key("S1+S2")], 1)},
                     "reflex": round(earn["earn"][key("S1+S2+S3")], 1), "rigorous": round(earn["rigorous"], 1)}
    fig["truth"] = {c: round(float(T[c]["roas"]), 3) for c in MEM}
    E, g_lost = effort(X, fig, R, pert)
    fig["result_grades"] = g_lost
    return X, fig, E, spec


if __name__ == "__main__":
    import json
    X, fig, E, spec = run(sys.argv[1])
    print(json.dumps({k: fig[k] for k in ("call", "rubric", "perturbations", "nearest_variant", "result_grades", "check_moves",
                                           "unnamed", "check_web", "check_search_ads", "stores")}, indent=1, default=float)[:9000])
    for fid in fig["figure"]:
        print("%-36s %10s  %s" % (fid, fig["figure"][fid], fig["figure_band"][fid]))
