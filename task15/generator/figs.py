"""task15: every graded figure, each rival's and each hurried pass's version of it, the bands, and effort.json.

compute(P) runs the golden, the rivals, the hurried passes and the one-fact routes on a conformed record and
returns one object; figures(A) is what the answer blocks state (generator/figures.json); effort(A) is the effort
test's input (generator/effort.json). Nothing here reads the prompt.
"""
import math

import numpy as np
import pandas as pd

import golden as G

# Other defensible ways to do one step: each lands inside every band (checks.py).
RIVALS = {
    "each line fitted on its own trials alone (no pooling)": dict(engine="plain"),
    "lines taken as unrelated (no cross level)": dict(family=False),
    "one prior for all cohorts": dict(pooled_prior=True),
    "blocks ignored (replicates only)": dict(blocks=False),
    "a slope along the range as well as blocks": dict(trend=True),
    "lodging fitted on the lushest trials only": dict(pmin=1.0),
    "lodging fitted on every trial with any": dict(pmin=0.25),
    "lodging multiples not shrunk": dict(shrink_lodging=False),
    "lodging above a dry-trial floor": dict(baseline=True),
    "the series' last six seasons only": dict(recent=6),
    "the review's lodging head on fitted lodging": dict(obs_lodging=False),
    "lodging set against Byaduk's alone": dict(press="bench"),
}
# Tempting, and ruled out by named data (checks.py asserts the data that rule each out).
RULED_OUT = {
    "response to the trial's yield level, not its season water": dict(covar="level"),
    "Kerang's waterings left out of its season water": dict(irrigation=False),
}
HINTS = [
    ("every line has its own response to season water against the benchmark's", dict(lodging=False)),
    ("weak-strawed lines lodge harder at the series' sites than at ours, and it costs them yield there",
     dict(slope=False)),
]
SIMS = 20000
RIVAL_SIMS = 4000
# The least a line's figures may differ by between sound fits. A line's expected relative yield is known to about
# 2.6 points (the spread of its own estimate), so two sound fits can stand 5 apart; where a line is expected to
# lodge heavily the size of the lodging loss differs between sound ways of pricing it and the room is 9. A range
# end carries the same room and 3 more (the season draw is modelled differently). Lodging: 6 points of the plot.
# Where it is expected to lodge 65% or more the loss is most of what moves the line and the room is 13.
RY_TOL, RY_TOL_LODGED, LODGED_AT, RANGE_EXTRA, LODGE_TOL = 5.0, 9.0, 45, 3.0, 6.0
RY_TOL_HEAVY, HEAVY_AT = 13.0, 65


def ry_room(lodging_pct):
    """The least room a line's expected relative yield is given, by how much of its plot is expected to lodge."""
    return RY_TOL_HEAVY if lodging_pct >= HEAVY_AT else (RY_TOL_LODGED if lodging_pct >= LODGED_AT else RY_TOL)


def r1(x):
    return round(float(x) + 1e-9, 1)


def pct(x):
    return int(round(100.0 * float(x)))


def summary(R, P):
    """One route's answers in the units the blocks use."""
    cd = R["cands"]
    wi = P.wi
    quoted, realised = r1(R["promised"]), r1(R["realised"])
    short = r1(R["shortfall"])                    # from the unrounded means
    own, water, lodg = r1(R["own_sites"]), r1(R["water_part"]), r1(R["lodging_part"])
    out = dict(quoted=quoted, realised=realised, shortfall=short, own=own, water=water, lodging_part=lodg,
               series=r1(R["water_part"] + R["lodging_part"]), left=r1(R["left_over"]),
               picks=[wi[l] for l in R["picks"]], next=wi[R["next"]] if R.get("next") else None,
               margin=r1(R["margin"]),
               ry={wi[l]: r1(v) for l, v in zip(cd["line"], cd["ry"])},
               lodging={wi[l]: int(round(float(v))) for l, v in zip(cd["line"], cd["lodging"])})   # whole per cent
    if R["margin"] == R["margin"]:                # stated as a bound over a family of fits, the cut rounds down
        out["cut_raw"] = float(R["margin"])
        out["cut_floor"] = math.floor(float(R["margin"]) * 10.0 + 1e-9) / 10.0
    if R.get("bridge_rows") is not None:          # the remainder across the nominations: is it there at all
        e = (R["bridge_rows"]["C"] - R["bridge_rows"]["D"]).to_numpy(float)
        out["left_t"] = r1(e.mean() / (e.std(ddof=1) / math.sqrt(len(e))))
        by = R["bridge_rows"].assign(e=e).groupby("sow")["e"].mean()
        out["left_years_positive"], out["left_years"] = int((by > 0).sum()), int(len(by))
    if R.get("rmse_method") is not None:
        out["rmse"] = r1(R["rmse_method"])
        if R.get("bias_method") is not None:
            out["bias"] = r1(R["bias_method"])
    if "lo" in cd:
        out["lo"] = {wi[l]: r1(v) for l, v in zip(cd["line"], cd["lo"])}
        out["hi"] = {wi[l]: r1(v) for l, v in zip(cd["line"], cd["hi"])}
    return out


def ols(y, cols):
    X = np.column_stack([np.ones(len(y))] + list(cols))
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    res = y - X @ beta
    s2 = float((res ** 2).sum() / (len(y) - X.shape[1]))
    cov = s2 * np.linalg.inv(X.T @ X)
    return beta, beta / np.sqrt(np.diag(cov)), 1.0 - float((res ** 2).sum() / ((y - y.mean()) ** 2).sum())


def evidence(P, R):
    """What the record itself shows about each mechanism, across all of it (not only on the nominees)."""
    F = R["F"]
    c = F["cells"]
    c = c[c["n"] > 0]
    d = F["d"]
    E = {}
    # the benchmark's advantage by trial: season water against the trial's yield level
    b = c[c["line"] == G.BENCH].set_index("trial")
    ln = c[~c["line"].isin(P.checks)]
    t = ln.groupby("trial").agg(pot=("pot", "mean"), x=("x", "first"), site=("site", "first"))
    t["adv"] = b["pot"].reindex(t.index) - t["pot"]                      # benchmark over the lines' mean, t/ha
    # the trial's yield level: the other check varieties' mean, which sits on neither side of the difference
    t["m"] = c[c["line"].isin(P.checks) & (c["line"] != G.BENCH)].groupby("trial")["yh"].mean().reindex(t.index)
    y = t["adv"].to_numpy(float)
    bw, tw, r2w = ols(y, [t["x"].to_numpy(float)])
    bl, tl, r2l = ols(y, [t["m"].to_numpy(float)])
    bb, tb, r2b = ols(y, [t["x"].to_numpy(float), t["m"].to_numpy(float)])
    E["trials"] = int(len(t))
    E["adv_per_100mm"] = round(float(bw[1]), 3)
    E["adv_water_t"], E["adv_water_r2"] = round(float(tw[1]), 1), round(r2w, 2)
    E["adv_level_t"], E["adv_level_r2"] = round(float(tl[1]), 1), round(r2l, 2)
    E["joint_water_t"], E["joint_level_t"] = round(float(tb[1]), 1), round(float(tb[2]), 1)
    E["water_level_corr"] = round(float(np.corrcoef(t["x"], t["m"])[0, 1]), 2)
    dry = t[t["x"] <= t["x"].quantile(0.25)]["adv"].mean()
    wet = t[t["x"] >= t["x"].quantile(0.75)]["adv"].mean()
    E["adv_driest_quarter"], E["adv_wettest_quarter"] = round(float(dry), 2), round(float(wet), 2)
    # do the lines differ in their response? each line with ten or more trials over 100 mm or more of season water
    # fitted on its own: the spread of the fitted responses against what trial noise alone would give
    dl = ln.assign(dy=ln["pot"] - ln["trial"].map(b["pot"]))
    fits = []
    for _, g_ in dl.groupby("line", sort=True):
        xs = g_["x"].to_numpy(float)
        if len(g_) >= 10 and float(np.ptp(xs)) >= 1.0:
            X = np.column_stack([np.ones(len(g_)), xs])
            XtXi = np.linalg.inv(X.T @ X)
            beta = XtXi @ X.T @ g_["dy"].to_numpy(float)
            res = g_["dy"].to_numpy(float) - X @ beta
            fits.append((float(beta[1]), float(XtXi[1, 1]), float(res @ res), len(g_) - 2))
    fa = np.array(fits)
    s2r = float(fa[:, 2].sum() / fa[:, 3].sum())
    se2 = fa[:, 1] * s2r
    wq = 1.0 / se2
    mbar = float((wq * fa[:, 0]).sum() / wq.sum())
    E["response_lines"] = int(len(fa))
    E["response_common_per_100mm"] = round(-mbar, 2)            # what the average line loses to Byaduk per 100 mm
    E["response_spread_ratio"] = round(float(np.var(fa[:, 0], ddof=1) / se2.mean()), 1)
    E["response_q"], E["response_df"] = int(round(float((wq * (fa[:, 0] - mbar) ** 2).sum()))), int(len(fa) - 1)
    # the spread of the lines' own levels and responses
    Sig = np.asarray(F["fit"]["Sig"])
    E["sd_level_t_ha"] = round(float(math.sqrt(Sig[0, 0])), 3)
    E["sd_response_per_100mm"] = round(float(math.sqrt(Sig[1, 1])), 3)
    # lodging: the cost inside a line and trial, and what plainer comparisons give
    h = d[d["ab"] == 0]
    E["loss_per_tenth_within"] = round(float(F["gam"]), 3)
    L, yv = h["L"].to_numpy(float), h["y"].to_numpy(float)
    E["loss_per_tenth_across_plots"] = round(float(-np.cov(L, yv)[0, 1] / np.var(L, ddof=1)), 3)
    E["gain_per_tenth_across_plots"] = round(-E["loss_per_tenth_across_plots"], 3)
    tm = h.groupby("trial")["y"].transform("mean")
    lm = h.groupby("trial")["L"].transform("mean")
    yy, ll = (h["y"] - tm).to_numpy(float), (h["L"] - lm).to_numpy(float)
    E["loss_per_tenth_within_trial"] = round(float(-(yy * ll).sum() / (ll * ll).sum()), 3)
    E["plots"] = int(len(d))
    E["abandoned"] = int(d["ab"].sum())
    E["abandoned_pct"] = round(100.0 * float(d["ab"].mean()), 2)
    wetp = d[d["site"].isin(G.INDEX_SITES)]
    E["abandoned_pct_index_sites"] = round(100.0 * float(wetp["ab"].mean()), 2)
    E["lodging_pct_abandoned"] = round(10.0 * float(d[d["ab"] == 1]["L"].mean()), 1)
    E["lodging_pct_harvested"] = round(10.0 * float(h["L"].mean()), 1)
    E["trials_with_abandoned"] = int(d[d["ab"] == 1]["trial"].nunique())
    E["lines_with_abandoned"] = int(d[d["ab"] == 1]["line"].nunique())
    # lodging pressure: the three standards in the programme's index trials and in the series
    s, tt = G.series_frame(P)
    Pt = F["Ptrial"]
    it = sorted(set(c[(c["stage"] == "S3") & (c["site"].isin(G.INDEX_SITES))]["trial"]))
    E["standards_lodging_pct_index_trials"] = round(10.0 * float(Pt.reindex(it).mean()), 1)
    E["standards_lodging_pct_series"] = round(10.0 * float(tt["P"].mean()), 1)
    E["water_mm_index_trials"] = int(round(float(np.mean([P.water[t_] for t_ in it]))))
    seas = c.groupby("trial")["season"].first()
    E["index_water_by_season"] = {int(y_): int(round(float(np.mean([P.water[t_] for t_ in it if seas[t_] == y_]))))
                                  for y_ in sorted(set(int(seas[t_]) for t_ in it))}
    E["water_mm_series"] = int(round(float(np.mean([P.series_water[t_] for t_ in tt.index]))))
    E["water_mm_all_programme_trials"] = int(round(float(np.mean(list(P.water.values())))))
    E["series_trials"] = int(len(tt))
    E["series_seasons"] = int(tt["season"].nunique())
    # the series' own trials: the benchmark against the other two standards, by season water and by yield level
    oth = s[s["line"].isin([v for v in G.STANDARDS if v != G.BENCH])].groupby("trial")["y"].mean()
    adv_s = (tt["yb"] - oth.reindex(tt.index)).to_numpy(float)
    # yield level there: the other entries' mean (no standard in it, so it sits on neither side of the difference)
    lev_s = s[~s["line"].isin(G.STANDARDS)].groupby("trial")["y"].mean().reindex(tt.index).to_numpy(float)
    b1, t1, _ = ols(adv_s, [tt["x"].to_numpy(float)])
    b2, t2, _ = ols(adv_s, [tt["x"].to_numpy(float), lev_s])
    E["series_adv_per_100mm"], E["series_adv_water_t"] = round(float(b1[1]), 3), round(float(t1[1]), 1)
    E["series_joint_water_t"], E["series_joint_level_t"] = round(float(t2[1]), 1), round(float(t2[2]), 1)
    E["series_water_level_corr"] = round(float(np.corrcoef(tt["x"].to_numpy(float), lev_s)[0, 1]), 2)
    # the same for the programme's own nominated lines in the series: Byaduk over their mean, trial by trial, with
    # the mean yield of the trial's other entries (neither Byaduk nor a Banyena line) as the trial's yield level
    noml = {nm["line"] for nm in P.noms}
    advn = (tt["yb"] - s[s["line"].isin(noml)].groupby("trial")["y"].mean().reindex(tt.index)).dropna()
    lev_n = s[~s["line"].isin(noml | {G.BENCH})].groupby("trial")["y"].mean()
    b3, t3, _ = ols(advn.to_numpy(float), [tt["x"].reindex(advn.index).to_numpy(float),
                                           lev_n.reindex(advn.index).to_numpy(float)])
    E["series_lines_trials"] = int(len(advn))
    E["series_lines_joint_water_t"], E["series_lines_joint_level_t"] = round(float(t3[1]), 1), round(float(t3[2]), 1)
    br = R["bridge_rows"]
    E["in_sample_rmse"] = round(float(np.sqrt(((br["C"] - br["D"]) ** 2).mean())), 1)
    mor = []
    for l in br["line"]:
        dl_ = s[s["line"] == l].set_index("trial")
        mor.append(100.0 * float((dl_["y"] / tt["yb"].reindex(dl_.index)).mean()))
    E["returned_mean_of_site_percentages"] = round(float(np.mean(mor)), 1)
    E["gap_on_mean_of_site_percentages"] = round(float(br["quoted"].mean() - np.mean(mor)), 1)
    # Kerang: its yields against the other sites' curve of yield on season water, with and without its waterings
    tm = c.groupby("trial").agg(yh=("yh", "mean"), site=("site", "first"))
    tm["W"] = [P.water[t_] for t_ in tm.index]
    tm["rain"] = [P.water[t_] - P.irrigation.get(t_, 0.0) for t_ in tm.index]
    oth_t, ker = tm[tm["site"] != "Kerang"], tm[tm["site"] == "Kerang"]
    curve = np.polyfit(oth_t["W"].to_numpy(float), oth_t["yh"].to_numpy(float), 2)
    E["kerang_trials"] = int(len(ker))
    E["kerang_mean_yield"] = round(float(ker["yh"].mean()), 2)
    E["kerang_curve_at_rain_alone"] = round(float(np.polyval(curve, ker["rain"].to_numpy(float)).mean()), 2)
    E["kerang_curve_with_waterings"] = round(float(np.polyval(curve, ker["W"].to_numpy(float)).mean()), 2)
    E["kerang_rain_mm"] = int(round(float(ker["rain"].mean())))
    E["kerang_water_mm"] = int(round(float(ker["W"].mean())))
    # selection, across every line advanced out of Stage 1 (not only the nominees): what its Stage 1 trials showed
    # against the check varieties in the same trials, and what its Stage 2 trials showed a season later
    chk = c[c["line"].isin(P.checks)].groupby("trial")["yh"].mean()
    cl = c[~c["line"].isin(P.checks)].copy()
    cl["advc"] = cl["yh"] - cl["trial"].map(chk)
    s1 = cl[cl["stage"] == "S1"].groupby("line").agg(a1=("advc", "mean"), y1=("season", "first"))
    s2 = cl[cl["stage"] == "S2"].groupby("line").agg(a2=("advc", "mean"), y2=("season", "first"))
    j = s1.join(s2, how="inner")
    j = j[j["y2"] == j["y1"] + 1]
    E["stage1_lines"] = int(len(s1))
    E["advanced_lines"] = int(len(j))
    E["stage1_all_over_checks"] = round(float(s1["a1"].mean()), 2)
    E["advanced_stage1_over_checks"] = round(float(j["a1"].mean()), 2)
    E["advanced_stage2_over_checks"] = round(float(j["a2"].mean()), 2)
    # the benchmark's own season swing in the series (shared by every entry's relative yield that season)
    sw = G.bench_swing(P, F, tt, s)
    E["bench_swing_sd_t_ha"] = round(float(sw.std(ddof=1)), 2)
    E["bench_swing_sd_points"] = round(100.0 * float(sw.std(ddof=1)) / float(tt["yb"].mean()), 1)
    # the lines' lodging multiples (every line with a fitted one)
    hv = np.array([v for l, v in F["hl"].items() if l not in P.checks])
    E["lines_with_lodging_multiple"] = int(len(hv))
    E["lodging_multiple_p10"] = round(float(np.percentile(hv, 10)), 2)
    E["lodging_multiple_p90"] = round(float(np.percentile(hv, 90)), 2)
    return E


def prop_heads(P, R):
    """A rival for the review's heads (b) and (c): the lodging loss taken as a share of the plot's yield, not as
    tonnes a hectare. The share lost per tenth of a plot lodged is read inside line and trial on the log of plot
    yield and applied to each nomination's recorded lodging and Byaduk's at both sets of trials; head (b) is the
    move less this head (c)."""
    F = R["F"]
    d, c, gam = F["d"], F["cells"], F["gam"]
    h = d[(d["ab"] == 0) & (d["yadj"] > 0)]
    ly, L = np.log(h["yadj"].to_numpy(float)), h["L"].to_numpy(float)
    ci = pd.factorize((h["trial"] + "|" + h["line"]).to_numpy())[0]
    n = np.bincount(ci)
    yt = ly - (np.bincount(ci, weights=ly) / n)[ci]
    lt = L - (np.bincount(ci, weights=L) / n)[ci]
    k = float(-(yt * lt).sum() / (lt * lt).sum())            # share of yield lost per tenth of the plot lodged
    s, tt = G.series_frame(P)
    P._cells = c
    out = []
    for nm in P.noms:
        l = nm["line"]
        mine = s[s["line"] == l]
        if mine["season"].nunique() < 2:
            continue
        mine = mine.set_index("trial")
        tj = tt.loc[mine.index]
        th = F["fit"]["theta"][l]
        pot_b = tj["yb"].to_numpy(float) / np.maximum(1.0 - k * tj["Lb"].to_numpy(float), 0.2)
        pot_l = pot_b + th[0] + th[1] * tj["x"].to_numpy(float)
        at_series = 100.0 * float(np.sum(k * (mine["L"].to_numpy(float) * pot_l - tj["Lb"].to_numpy(float) * pot_b))) \
            / float(tj["yb"].sum())
        it = G.index_trials(P, l, nm["s3"]).set_index("trial")
        bi = c[(c["line"] == G.BENCH) & (c["trial"].isin(it.index))].set_index("trial").reindex(it.index)
        net_b = (bi["pot"] - gam * bi["L"]).to_numpy(float)
        pot_bi = net_b / np.maximum(1.0 - k * bi["L"].to_numpy(float), 0.2)
        pot_li = pot_bi + th[0] + th[1] * it["x"].to_numpy(float)
        at_index = 100.0 * float(np.sum(k * (it["L"].to_numpy(float) * pot_li - bi["L"].to_numpy(float) * pot_bi))) \
            / float(net_b.sum())
        out.append(at_series - at_index)
    c_prop = float(np.mean(out))
    return dict(share=k, lodging=c_prop, water=float(R["water_part"] + R["lodging_part"] - c_prop))


def compute(P, sims=SIMS, rivals=True):
    A = dict(P=P)
    R = G.analyse(P, sims=sims)
    A["R"] = R
    A["gold"] = summary(R, P)
    cd = R["cands"]
    picks = list(R["picks"])
    # the range a nominated line would be given from the spread of its estimate alone
    s, tt = G.series_frame(P)
    F = R["F"]
    est = []
    for l in picks:
        th, V = F["fit"]["theta"][l], F["fit"]["V"][l]
        z = np.array([1.0, float((tt["x"] * 1.0).mean())])[:len(th)]
        sd_t = math.sqrt(float(z @ V @ z) + (F["gam"] * float(tt["P"].mean())) ** 2 * F["hv"].get(l, 0.0))
        sd = 100.0 * sd_t / float(tt["yb"].mean())
        ry = float(cd.set_index("line").loc[l, "ry"])
        est.append((ry, sd))
    A["estimate_only"] = dict(sd=[r1(e[1]) for e in est], lo=[r1(e[0] - 1.2816 * e[1]) for e in est],
                              hi=[r1(e[0] + 1.2816 * e[1]) for e in est])
    A["index_picks"] = [P.wi[l] for l in R["index_picks"]]
    A["index"] = {P.wi[l]: r1(v) for l, v in zip(cd["line"], cd["index"])}
    A["seasons"] = {P.wi[l]: int(v) for l, v in zip(cd["line"], cd["seasons"])}
    A["evidence"] = evidence(P, R)
    A["prop"] = prop_heads(P, R)
    # Monte Carlo steadiness of the ranges: the nominated lines' range ends on two other seeds
    A["mc"] = []
    idx = [P.cands.index(l) for l in picks]
    for sd_ in (11, 23):
        sim = G.simulate(P, F, tt, s, P.cands, n=sims, seed=sd_)
        A["mc"].append(dict(lo=[r1(np.percentile(sim[:, j], 10)) for j in idx],
                            hi=[r1(np.percentile(sim[:, j], 90)) for j in idx]))
    # the hurried passes
    Q = G.quick(P)
    C = G.careful(P)
    Cw = G.careful(P, covar="water")
    C0 = G.careful(P, with_lodging=False)
    A["quick"], A["careful"], A["careful_water"], A["careful_plain"] = Q, C, Cw, C0
    A["quick_s"], A["careful_s"], A["careful_water_s"] = summary(Q, P), summary(C, P), summary(Cw, P)
    A["careful_plain_s"] = summary(C0, P)
    IR = G.index_route(P)
    A["index_route"] = dict(picks=[P.wi[l] for l in IR["picks"]], slope=IR["slope"],
                            ry={P.wi[l]: r1(v) for l, v in zip(IR["cands"]["line"], IR["cands"]["ry"])})
    # rivals, the ruled-out routes and the one-fact routes
    A["rivals"], A["ruled_out"], A["hints"] = {}, {}, {}
    if rivals:
        for name, opt in RIVALS.items():
            A["rivals"][name] = summary(G.analyse(P, sims=RIVAL_SIMS, backtest=True, **opt), P)
        for name, opt in RULED_OUT.items():
            A["ruled_out"][name] = summary(G.analyse(P, sims=RIVAL_SIMS, backtest=True, **opt), P)
        for sentence, opt in HINTS:
            sm = summary(G.analyse(P, sims=RIVAL_SIMS, backtest=True, **opt), P)
            if opt.get("lodging") is False:           # told about the response only: lodging stays as it read it
                sm["lodging"] = dict(A["careful_s"]["lodging"])
            A["hints"][sentence] = sm
    return A


def bands(A):
    """Each result's band: what every rival spans, with a little room; per line for the tables."""
    g = A["gold"]
    rv = list(A["rivals"].values())
    pr = A["prop"]

    def span(key, pad, extra=()):
        vals = [g[key]] + [r[key] for r in rv] + [r1(x) for x in extra]
        return [r1(min(vals) - pad), r1(max(vals) + pad)]

    B = dict(own=span("own", 0.4), water=span("water", 0.5, [pr["water"]]),
             lodging_part=span("lodging_part", 0.5, [pr["lodging"]]), series=span("series", 0.6),
             left=span("left", 0.5), rmse=span("rmse", 0.4))
    B["ry"], B["lodging"], B["lo"], B["hi"], B["tol"], B["tol_lodging"] = {}, {}, {}, {}, {}, {}
    for wi, v in g["ry"].items():
        base = ry_room(g["lodging"][wi])
        dev = max([abs(r["ry"][wi] - v) for r in rv] + [0.0])
        w = max(base, dev + 0.8)
        B["tol"][wi] = r1(w)
        B["ry"][wi] = [r1(v - w), r1(v + w)]
        dlo = max([abs(r["lo"][wi] - g["lo"][wi]) for r in rv] + [0.0])
        dhi = max([abs(r["hi"][wi] - g["hi"][wi]) for r in rv] + [0.0])
        wlo, whi = max(w + RANGE_EXTRA, dlo + 1.0), max(w + RANGE_EXTRA, dhi + 1.0)
        B["lo"][wi] = [r1(g["lo"][wi] - wlo), r1(g["lo"][wi] + wlo)]
        B["hi"][wi] = [r1(g["hi"][wi] - whi), r1(g["hi"][wi] + whi)]
        devl = max([abs(r["lodging"][wi] - g["lodging"][wi]) for r in rv] + [0.0])
        wl = max(LODGE_TOL, devl + 2.0)
        B["tol_lodging"][wi] = r1(wl)
        B["lodging"][wi] = [r1(max(0.0, g["lodging"][wi] - wl)), r1(min(100.0, g["lodging"][wi] + wl))]
    return B


def figures(A, counts=None, files=None):
    """What the answer blocks and the golden files state, at the rounding the prompt asks."""
    g, P, R = A["gold"], A["P"], A["R"]
    wi = P.wi
    B = bands(A)
    F = dict(standard=float(P.standard), nominations_allowed=G.CAP, places=int(P.places))
    sows = sorted({int(nm["sow"]) for nm in P.noms})
    done = sorted({int(v) for v in R["bridge_rows"]["sow"]})
    F["years"] = dict(first_season=int(P.plots["season"].min()), last_season=int(P.last), decision_sow=int(P.last) + 1,
                      first_sow=done[0], last_completed_sow=done[-1], pending_sow=sows[-1],
                      pending=int(len(P.noms) - len(R["bridge_rows"])))
    if files:
        F["files"] = dict(files)
    F["nominate"] = g["picks"]
    F["first_left_out"] = g["next"]
    F["cut_points"] = g["margin"]
    F["index_would_nominate"] = A["index_picks"]
    F["completed_nominations"] = int(R["n_completed"])
    F["quoted_mean"], F["realised_mean"], F["shortfall_points"] = g["quoted"], g["realised"], g["shortfall"]
    F["overstated_at_own_sites_points"] = g["own"]
    F["benchmark_water_response_points"] = g["water"]
    F["lodging_points"] = g["lodging_part"]
    F["series_sites_points"] = g["series"]
    F["left_over_points"] = g["left"]
    F["left_over_t"] = g["left_t"]
    F["expected_in_series_mean"] = r1(R["bridge_rows"]["C"].mean())
    F["worth_at_own_sites_mean"] = r1(R["bridge_rows"]["B"].mean())
    F["backtest_rmse_points"] = g["rmse"]
    F["index_rmse_points"] = r1(R["rmse_index"])
    F["backtest_mean_error_points"] = r1(R["bias_method"])
    br = R["bridge_rows"]
    F["bridge"] = {wi[l]: dict(sowing=int(s_), quoted=r1(q), worth_at_own_sites=r1(b), water=r1(w_), lodging=r1(lg),
                               expected_in_series=r1(c), realised=r1(d))
                   for l, s_, q, b, w_, lg, c, d in zip(br["line"], br["sow"], br["quoted"], br["B"], br["water"],
                                                        br["lodging"], br["C"], br["D"])}
    F["bridge_means"] = dict(
        advantage_at_index_trials_t_ha=round(float(br["adv_index"].mean()), 2),
        advantage_at_series_trials_t_ha=round(float(br["adv_series"].mean()), 2),
        byaduk_at_index_trials_t_ha=round(float(br["bench_index"].mean()), 2),
        byaduk_at_series_trials_t_ha=round(float(br["bench_series"].mean()), 2),
        lodging_over_byaduk_at_index_trials_pct=r1(10.0 * float(br["lod_index"].mean())),
        lodging_over_byaduk_at_series_trials_pct=r1(10.0 * float(br["lod_series"].mean())),
        water_at_index_trials_mm=int(round(float(br["water_index"].mean()))),
        water_at_series_trials_mm=int(round(float(br["water_series"].mean()))))
    by = br.assign(short=br["quoted"] - br["D"], own=br["quoted"] - br["B"]).groupby("sow")
    iw = A["evidence"]["index_water_by_season"]
    F["bridge_by_sowing"] = {}
    for y, v in by:
        row = dict(quoted=r1(v["quoted"].mean()), realised=r1(v["D"].mean()), own=r1(v["own"].mean()),
                   water=r1(v["water"].mean()), lodging=r1(v["lodging"].mean()))
        row["shortfall"] = r1(row["quoted"] - row["realised"])
        row["left"] = r1(row["shortfall"] - row["own"] - row["water"] - row["lodging"])
        row["index_water_mm"] = int(iw[int(y) - 1])       # season water at the index trials the season before sowing
        F["bridge_by_sowing"][int(y)] = row
    worst = max(F["bridge_by_sowing"], key=lambda y_: F["bridge_by_sowing"][y_]["water"])
    F["worst_year"] = dict(F["bridge_by_sowing"][worst], sow=int(worst), season=int(worst) - 1)
    F["lines"] = {w_: dict(expected_ry=g["ry"][w_], low=g["lo"][w_], high=g["hi"][w_], lodging_pct=g["lodging"][w_],
                           index=A["index"][w_], stage3_seasons=A["seasons"][w_])
                  for w_ in g["ry"]}
    F["ry_table"] = dict(g["ry"])
    F["range_table"] = range_cells(g)
    F["lodging_table"] = dict(g["lodging"])
    F["past_meeting_standard"] = int(sum(1 for v in R["bridge_rows"]["D"] if v >= float(P.standard)))
    F["constants"] = dict(range_pct=80, per_mm=100, moisture_pct=12.5)
    F["references"] = dict(deed_clause=2.1, handbook_index_section=6, protocol_relative_yield_section=7,
                           handbook_plots_section=5)
    order = sorted(g["ry"], key=lambda k_: -g["ry"][k_])
    F["rank"] = {w_: i + 1 for i, w_ in enumerate(order)}
    F["index_rank"] = {w_: i + 1 for i, w_ in enumerate(sorted(A["index"], key=lambda k_: -A["index"][k_]))}
    F["candidates"] = len(order)
    F["estimate_only"] = A["estimate_only"]
    pr = A["prop"]
    F["proportional_loss"] = dict(share_per_tenth_pct=r1(100.0 * pr["share"]), lodging=r1(pr["lodging"]),
                                  water=r1(pr["water"]))
    c = A["careful_s"]
    F["hurried"] = dict(nominate=c["picks"], own=c["own"], water=c["water"], lodging=c["lodging_part"],
                        left=c["left"], rmse=c["rmse"], ry_of_its_picks=[c["ry"][w_] for w_ in c["picks"]],
                        golden_ry_of_its_picks=[g["ry"][w_] for w_ in c["picks"]],
                        its_ry_of_the_nominees=[c["ry"][w_] for w_ in g["picks"]],
                        its_lodging_of_the_nominees=[c["lodging"][w_] for w_ in g["picks"]],
                        its_ry_low=min(c["ry"].values()), its_ry_high=max(c["ry"].values()),
                        its_lodging_low=min(c["lodging"].values()), its_lodging_high=max(c["lodging"].values()),
                        interval_half_width=r1(1.2816 * A["careful"]["sd"]))
    F["index_route"] = dict(nominate=A["index_route"]["picks"], slope=round(A["index_route"]["slope"], 2))

    def brief(v):
        return dict(nominate=v["picks"], own=v["own"], water=v["water"], lodging=v["lodging_part"], left=v["left"],
                    left_t=v.get("left_t"), left_years_positive=v.get("left_years_positive"),
                    left_years=v.get("left_years"), rmse=v.get("rmse"), bias=v.get("bias"), cut=v["margin"],
                    ry_of_the_nominees=[v["ry"][w_] for w_ in g["picks"]],
                    ry_first_left_out=v["ry"][g["next"]])

    F["quick"] = dict(nominate=A["quick_s"]["picks"], own=A["quick_s"]["own"])
    fam = [g] + list(A["rivals"].values())          # the golden and every rival: a lower bound, rounded down
    F["closest_rival"] = dict(cut=min(v["cut_floor"] for v in fam))
    F["hurried_on_water"] = brief(A["careful_water_s"])
    F["one_fact"] = {k_: brief(v) for k_, v in A["hints"].items()}
    F["ruled_out"] = {k_: brief(v) for k_, v in A["ruled_out"].items()}
    F["rivals"] = {k_: brief(v) for k_, v in A["rivals"].items()}
    base_of = {w_: ry_room(g["lodging"][w_]) for w_ in g["ry"]}
    wide_ry = {w_: B["tol"][w_] for w_ in g["ry"] if B["tol"][w_] > base_of[w_] + 0.05}
    wide_lod = {w_: B["tol_lodging"][w_] for w_ in g["ry"] if B["tol_lodging"][w_] > LODGE_TOL + 0.05}
    F["tolerances"] = dict(ry_points=RY_TOL, ry_points_lodged=RY_TOL_LODGED, lodged_at_pct=LODGED_AT,
                           ry_points_heavy=RY_TOL_HEAVY, heavy_at_pct=HEAVY_AT,
                           range_extra_points=RANGE_EXTRA, lodging_points=LODGE_TOL, wider_ry=wide_ry,
                           wider_lodging=wide_lod)
    F["bands"] = dict(own=B["own"], water=B["water"], lodging=B["lodging_part"], rmse=B["rmse"], left=B["left"],
                      series=B["series"], ry=B["ry"], low=B["lo"], high=B["hi"], lodging_pct=B["lodging"])
    F["evidence"] = A["evidence"]
    if counts:
        F["counts"] = counts
    return F


def share_in(val, band):
    keys = [k for k in band if k in val]
    return sum(band[k][0] <= val[k] <= band[k][1] for k in keys) / float(len(keys) or 1)


def range_cells(sm):
    return dict({k + " low": v for k, v in sm.get("lo", {}).items()},
                **{k + " high": v for k, v in sm.get("hi", {}).items()})


def range_bands(B):
    return dict({k + " low": v for k, v in B["lo"].items()}, **{k + " high": v for k, v in B["hi"].items()})


# the chain: R1 the gap, R2 the index head, R3 the move to the series, R4 every line's expected lodging, R5 the
# lodging head, R6 every line's expected relative yield, R7 its 80% range, R8 the nominations, R9 the remainder
RESULTS = ["R1", "R2", "R3", "R4", "R5", "R6", "R7", "R8", "R9"]


def graded(sm, A, B):
    """Which results one route's summary earns (Right), by the bands."""
    g = A["gold"]
    ok = set()
    if abs(sm["shortfall"] - g["shortfall"]) <= 0.1 + 1e-9:
        ok.add("R1")
    if B["own"][0] <= sm["own"] <= B["own"][1]:
        ok.add("R2")
    if B["water"][0] <= sm["water"] <= B["water"][1]:
        ok.add("R3")
    if share_in(sm["lodging"], B["lodging"]) >= 0.999:
        ok.add("R4")
    if B["lodging_part"][0] <= sm["lodging_part"] <= B["lodging_part"][1]:
        ok.add("R5")
    if share_in(sm["ry"], B["ry"]) >= 0.999:
        ok.add("R6")
    if "lo" in sm and share_in(range_cells(sm), range_bands(B)) >= 0.999:
        ok.add("R7")
    if set(sm["picks"]) == set(g["picks"]):
        ok.add("R8")
    if B["left"][0] <= sm["left"] <= B["left"][1]:
        ok.add("R9")
    return ok


def effort(A, F):
    """The effort test's input: every result, its golden and band, and what each pass files."""
    g, B = A["gold"], bands(A)
    q, c = A["quick_s"], A["careful_s"]
    res = []

    def add(rid, name, graded_as, figure, golden, passes, band=None, partly=None, bands_=None, depends=(),
            independent=""):
        r = dict(id=rid, name=name, graded_as=graded_as, figure=figure, depends=list(depends), independent=independent,
                 golden=golden, passes=passes)
        if band:
            r["band"] = band
        if partly:
            r["partly"] = partly
        if bands_:
            r["bands"] = bands_
        res.append(r)

    def wide(b, pad):
        return [r1(b[0] - pad), r1(b[1] + pad)]

    add("R1", "the gap on the completed nominations", "Ask 1", "shortfall_points", g["shortfall"],
        dict(quick=q["shortfall"], careful=c["shortfall"], thorough=g["shortfall"]),
        band=[r1(g["shortfall"] - 0.1), r1(g["shortfall"] + 0.1)])
    add("R2", "the index head: how far the index overstated the lines at the trials it was taken from", "Component 1",
        "overstated_at_own_sites_points", g["own"], dict(quick=q["own"], careful=c["own"], thorough=g["own"]),
        band=B["own"], partly=wide(B["own"], 0.6), depends=["R1"])
    add("R3", "the move to the series: what the lines lose against Byaduk there, lodging apart", "Component 2",
        "benchmark_water_response_points", g["water"],
        dict(quick=q["water"], careful=c["water"], thorough=g["water"]), band=B["water"],
        partly=wide(B["water"], 0.8), depends=["R1"])
    add("R4", "every Stage 3 line's expected lodging in the series", "Ask 3 (lodging)", "lodging_table",
        dict(g["lodging"]), dict(quick=dict(q["lodging"]), careful=dict(c["lodging"]), thorough=dict(g["lodging"])),
        bands_=B["lodging"], independent="the lodging figures of both records")
    add("R5", "the lodging head: what lodging at the series' trials took beyond the index trials", "Component 3",
        "lodging_points", g["lodging_part"],
        dict(quick=q["lodging_part"], careful=c["lodging_part"], thorough=g["lodging_part"]),
        band=B["lodging_part"], partly=wide(B["lodging_part"], 0.5),
        independent="the lodging recorded in both records and the plots' own yields")
    add("R6", "every Stage 3 line's expected relative yield in the series", "Ask 3 (relative yield)", "ry_table",
        dict(g["ry"]), dict(quick=dict(q["ry"]), careful=dict(c["ry"]), thorough=dict(g["ry"])), bands_=B["ry"],
        depends=["R3", "R4"])
    add("R7", "the 80% range of what two seasons return, line by line", "Ask 3 (range)", "range_table",
        range_cells(g), dict(quick=None, careful=range_cells(c), thorough=range_cells(g)), bands_=range_bands(B),
        depends=["R6"])
    add("R8", "the nominations", "Recommendation", "nominate", g["picks"],
        dict(quick=q["picks"], careful=c["picks"], thorough=g["picks"]), depends=["R6"])
    add("R9", "the remainder: what the heads leave of the gap", "Ask 2 (remainder)", "left_over_points", g["left"],
        dict(quick=q["left"], careful=c["left"], thorough=g["left"]), band=B["left"], partly=wide(B["left"], 0.5),
        depends=["R2", "R3", "R5"])
    lost = set(RESULTS) - graded(c, A, B)
    hints = []
    for sentence, sm in A["hints"].items():
        hints.append(dict(sentence=sentence, rescues=sorted(graded(sm, A, B) & lost)))
    hints.sort(key=lambda h: -len(h["rescues"]))
    routes = [dict(name="the golden", answer=sorted(g["picks"]), golden=True),
              dict(name="the breeder's index as quoted", answer=sorted(A["index_picks"])),
              dict(name="the index scaled by what past nominees realised", answer=sorted(A["index_route"]["picks"])),
              dict(name="one slope for all lines, the miss and its lodging share taken off (the careful pass)",
                   answer=sorted(c["picks"])),
              dict(name="the same on season water", answer=sorted(A["careful_water_s"]["picks"])),
              dict(name="the same without the lodging term", answer=sorted(A["careful_plain_s"]["picks"]))]
    for sentence, sm in A["hints"].items():
        routes.append(dict(name="the careful pass told: " + sentence, answer=sorted(sm["picks"])))
    for name, sm in A["ruled_out"].items():
        routes.append(dict(name=name, answer=sorted(sm["picks"])))
    return dict(results=res, hints=hints, routes=routes,
                weights=dict(recommendation=14, components=24, asks=55, instruction=7)), B
