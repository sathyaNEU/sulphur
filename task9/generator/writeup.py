"""task9 architecture 6: submission.md, the four platform answer blocks, every figure from figures.json at the
blocks' rounding, each band rounded outward."""
import math

import results as RS

NAMES = RS.NAMES
ORDER = RS.ORDER


def lo(x, dp):
    return math.floor(x * 10 ** dp + 1e-9) / 10 ** dp


def hi(x, dp):
    return math.ceil(x * 10 ** dp - 1e-9) / 10 ** dp


def band(b, dp):
    return "%.*f to %.*f" % (dp, lo(b[0], dp), dp, hi(b[1], dp))


def stated(fig):
    """The bands stated in submission.md, rounded outward (written to figures.json)."""
    B = fig["bands"]
    out = {}
    for s in ORDER:
        out["points_" + s] = [lo(B["points_" + s][0], 2), hi(B["points_" + s][1], 2)]
        out["share_" + s] = [lo(B["share_" + s][0], 1), hi(B["share_" + s][1], 1)]
    for k in ("tot_q1", "tot_q2", "tot_q3", "tot_q4", "tot_yr"):
        out[k] = [lo(B[k][0], 2), hi(B[k][1], 2)]
    for k in ("cc_pin", "own_share", "fr_sched", "fr_removed"):
        out[k] = [lo(B[k][0], 1), hi(B[k][1], 1)]
    out["cc1"] = out["points_optimisation"]
    out["cc2"] = out["points_turnover"]
    out["cc3"] = out["points_releases"]
    return out


def cap(s):
    return s[0].upper() + s[1:]


def _stump_block(fig):
    """Answer to the platform's stump question (How is each model stumped?), built from runs/run1.md and
    runs/run2.md (architecture 6, pair 1). Every quoted response phrase and figure is asserted verbatim against
    the saved responses; every golden figure comes from figures.json."""
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    r1p, r2p = (os.path.join(task, "runs", n) for n in ("run1.md", "run2.md"))
    if not (os.path.exists(r1p) and os.path.exists(r2p)):
        return []
    t1 = open(r1p, encoding="utf-8").read()
    t2 = open(r2p, encoding="utf-8").read()

    q1 = {
        "call": "Escalate optimisation noise (12.119 points) and label revisions (9.795 points); file a "
                "remediation plan for training data (6.685 points); monitor retunes (4.295 points) and "
                "feature releases (4.563 points).",
        "lag": "Warm-start lag fits drove persistence toward one/linear accumulation",
        "lin": "Refit randomness accumulates linearly over 13 warm-started refreshes; each source's weekly "
               "mean-squares add.",
        "mod": "it is a model, not a contractual formula",
        "flip": "Misreading warm-start accumulation is the one judgment that could flip noise",
        "rel": "Event effects are independent mean-square contributions; instruments carry no sign/cross-term, "
               "and repeated same-group releases have no special rule. If releases are correlated within group, "
               "actual combined could differ though each source's placement would likely not.",
        "rec": "Group fits favored lambda 0.91 (52-week) and 0.94 (104-week); per-family nonlinear fits "
               "clustered near 0.906-0.917 and 0.923-0.942.",
        "pin": "Share of 2027's weekly retrains expected to actually run on pinned feature views: 35.256%, "
               "i.e. 256.667 of 728 family-week retrains",
        "sep": "Sep 2026 rather than Dec 2027 book gives noise 12.130, data 6.761, retunes 4.294, releases "
               "4.571, labels 9.818, combined 18.127",
        "own": "mean 111.378 mean-square = 10.554 points",
        "clean": "25,007 roster merchants",
        "runs": "leaving 2,858",
        "pairs": "all 870 instrument pairs",
        "comb": "18.076",
    }
    q2 = {
        "call": "Escalate optimisation noise and label revisions to the board risk committee, put training "
                "data on a remediation plan, and keep retunes and feature releases on monitor.",
        "noise": "noise pair MS = Σ over 13 refreshes of R/2 (warm-start carries randomness, §1.4)",
        "dec": "Result: 52-week d = 0.911755, weighted χ² = 93.86 on 104 df; 104-week d = 0.933962, χ² = "
               "126.94 on 104 df.",
        "turn": "training pair MS = mean over the 13 refreshes of C/N_eff",
        "marg": "training's year margin over the 5.5 floor is only 0.450 points",
        "comp": "Compounding training-data sensitivity across 13 refreshes (treating it like warm-start noise): "
                "year training 21.453 points and combined 26.935",
        "pin": "607 of 728 family-week retrains = 83.379%",
        "pinrule": "pins from PC-26-058 planned ISO weeks, inclusive",
        "rel": "Feature-group identity is not separately modelled; family instrument levels were stable across "
               "release groups, so releases use family MS.",
        "own": "mean 124.034, RMS 11.137",
        "book": "125,031 merchants",
        "runs": "2,867 JSONL rows; 9 run IDs appeared twice",
        "pairs": "870 pairs",
        "on": "12.117",
        "td": "5.950",
        "fr": "1.960",
        "comb": "17.339",
    }
    nt1 = t1.replace("\u2019", "'").replace("\u2018", "'")
    nt2 = t2.replace("\u2019", "'").replace("\u2018", "'")
    for k, q in q1.items():
        assert q in nt1, "Response 1 quote %s missing from runs/run1.md: %r" % (k, q)
    for k, q in q2.items():
        assert q in nt2, "Response 2 quote %s missing from runs/run2.md: %r" % (k, q)

    B, b, bd, rd, pr, fa = (fig[k] for k in ("bands", "base", "bend", "recency_diag", "probe", "falsification"))
    f2, f1 = (lambda x: "%.2f" % x), (lambda x: "%.1f" % x)
    bo = band(B["cc1"], 2)
    bt = band(B["cc2"], 2)
    bf = band(B["cc3"], 2)
    bp = band(B["cc_pin"], 1)
    by = band(B["tot_yr"], 2)

    p1 = (
        f"Response 1 files the wrong call: \"{q1['call']}\" (combined {q1['comb']} against {f2(fig['tot_yr'])}, "
        f"band {by}). It solves two hard steps unprompted: recency-weighted training turnover (6.685 on December "
        f"2027 weights; 6.761 on September 2026 weights inside {bt}, \"{q1['rec']}\") and pinned-view adoption "
        f"(\"{q1['pin']}\", inside {bp} per cent). It fails two independent decisive steps. On optimisation noise "
        f"it files 12.119 (12.130 September book, escalation) against {f2(fig['cc1'])} (band {bo}, remediation "
        f"plan), writing \"{q1['lag']}\" and \"{q1['lin']}\" while conceding \"{q1['mod']}\" and \"{q1['flip']}\"; "
        f"its 2026 residual (111.378 points squared against {f2(fig['own_ms'])}) absorbs the overshoot. On "
        f"feature releases it files 4.563 (4.571 September book, monitor) against {f2(fig['cc3'])} (band {bf}, "
        f"remediation plan), claiming \"{q1['rel']}\" without checking signed deltas in "
        f"mrm_instrument_pair_scores_2026.csv, where same-group pairs correlate at {b['coh_same_mean']:.3f} "
        f"across {b['coh_same_n']} pairs."
    )
    p2 = (
        f"Response 2 files the same wrong call (\"{q2['call']}\") and misses four requested figures: optimisation "
        f"noise {q2['on']} (band {bo}), training data {q2['td']} (band {bt}, remediation by proximity only), "
        f"feature releases {q2['fr']} (band {bf}), and pinned views \"{q2['pin']}\" (against {f1(fig['cc_pin'])} "
        f"per cent, band {bp}; combined {q2['comb']} against {f2(fig['tot_yr'])}). On optimisation noise it sums "
        f"\"{q2['noise']}\" without checking warm-versus-cold lag curves, letting its 2026 residual (124.034 "
        f"against {f2(fig['own_ms'])}) absorb the error. On training data it inverts decay (\"{q2['dec']}\") but "
        f"substitutes single-refit \"{q2['turn']}\" ({q2['td']}, flagging \"{q2['marg']}\") for overlapping "
        f"weighted-window turnover. On pinned views it uses \"{q2['pinrule']}\" (83.379 per cent), ignoring 42 "
        f"historical lags and rollbacks, and on releases it sums variances orthogonally (\"{q2['rel']}\"), "
        f"dropping releases to {q2['fr']} monitor."
    )
    p3 = (
        f"The stump is fair, with no planted defect and no buried sentence. Both runs passed Layer 1 hygiene "
        f"before losing on modeling: Response 1 matched {b['panel_merchants']:,} merchants, "
        f"{b['manifest_runs']:,} runs, {b['pairs']} pairs, and covenant_tier_change_monitor_2026.csv exactly; "
        f"Response 2 matched {b['manifest_runs']:,} runs, {b['pairs']} pairs, and the {b['book_sep26']:,} "
        f"September 2026 book. Governing definitions sit plainly in gms_model_stability_standard_2026.pdf "
        f"(sections 1.4 to 1.6, 2.2, 3.1), and every mechanism spans all 14 families: warm lag curves bend "
        f"(lag 8 to 25 intercepts average {f1(bd['intercept8_book'])}, minimum {f1(bd['intercept8_min'])}) while "
        f"{bd['cold_min_weeks']} to {bd['cold_max_weeks']} cold weeks stay linear (curvature "
        f"{bd['cold_curv_mean']:+.3f}); {b['pairs_by_kind']['bootstrap']} bootstrap pairs identify decay "
        f"(reached by Response 1 at 6.761 and inverted by Response 2); 42 past rollouts show take-up lags "
        f"(reached by Response 1 at 35.256 per cent); and all {b['coh_same_n']} same-group release pairs across "
        f"12 groups and 14 families correlate positively (minimum {b['coh_same_min']:.3f}, mean "
        f"{b['coh_same_mean']:.3f}, versus {b['coh_diff_mean']:+.3f} across {b['coh_diff_n']} cross-group pairs)."
    )
    p4 = (
        f"Solving the task takes real statistical modeling because every shortcut fails the 2026 record. On "
        f"optimisation noise, linear carry ({f2(pr['linear 13 refits (half pair)'])} half-pair, "
        f"{f2(pr['full replicate pair per refit'])} full pair, escalation), one replicate "
        f"({f2(pr['single replicate pair (over)'])} monitor), and unanchored lag fits "
        f"({f2(pr['unanchored fit (raw curve)'])} escalation, implied replicate "
        f"{f2(pr['unanchored raw implied rep'])} against {f2(b['replicate'])}) fail; anchored AR(1) decay "
        f"verified by cold linearity reproduces 1-week variance ({f2(fa['golden_parts']['d1'])} vs "
        f"{f2(fa['obs_d1'])}, discrepancy {f2(fa['golden_err'])} vs {f2(fa['rivals']['S1 linear carry'])}) and "
        f"lands {f2(fig['cc1'])}. On training data, raw bootstrap ({f2(pr['raw bootstrap face value'])}), net "
        f"bootstrap ({f2(pr['net bootstrap face value (over)'])}), uniform turnover "
        f"({f2(pr['uniform window turnover'])} monitor, log-RMSE {rd['log_rmse_unif']:.4f} vs "
        f"{rd['log_rmse_exp']:.4f}, discrepancy {f2(fa['rivals']['S2 uniform window'])}), and single-refit mean "
        f"({q2['td']}) miss; {f2(fig['cc2'])} needs decay inversion plus overlapping weighted-window turnover. "
        f"On pinned views and releases, planned dates ({f1(b['cov_plan'])} per cent, "
        f"{f2(pr['orthogonal releases (calendar plan)'])} monitor) and slip alone ({f1(b['cov_declared'])} per "
        f"cent) fail 42 rollouts (leave-one-out {f1(100.0 * fig['loo']['runtime']['record'])} vs "
        f"{f1(100.0 * fig['loo']['runtime']['model'])}, {f1(100.0 * fig['loo']['warm']['record'])} vs "
        f"{f1(100.0 * fig['loo']['warm']['model'])}, {f1(100.0 * fig['loo']['amp']['record'])} vs "
        f"{f1(100.0 * fig['loo']['amp']['model'])} per cent, landing {f1(fig['cc_pin'])} per cent); orthogonal "
        f"releases give {f2(pr['orthogonal releases (actual lag)'])} monitor (discrepancy "
        f"{f2(fa['rivals']['S3 orthogonal releases'])}) and all-aligned releases give "
        f"{f2(pr['all releases aligned (over)'])} escalation, so {f2(fig['cc3'])} needs within-group covariance "
        f"({f2(fa['golden_parts']['rel_cov'])} vs {f2(fa['obs_rel_cov'])}) with joint live probabilities. Each "
        f"step owns a separate source or ask, and the two runs failed different subsets."
    )
    return ["## How is each model stumped?", "", p1, "", p2, "", p3, "", p4, ""]


def write(path, fig):
    B = fig["bands"]
    P = fig["points"]
    b = fig["base"]
    bd = fig["bend"]
    rd = fig["recency_diag"]
    rf = fig["reflex"]
    rg = fig["rigorous"]
    dr = fig["direct"]
    pr = fig["probe"]
    fa = fig["falsification"]
    lat = fig["lattice"]
    ov = fig["over"]
    L = []
    a = L.append

    a("# task9: Garrane Merchant Score, model-side sources of score movement for 2027")
    a("")
    a("## Tags")
    a("")
    a("**Domain:** General Statistics & Data Science, Interpretability (feature attribution, probing, mechanistic "
      "analysis).")
    a("**Analytical objective:** Root-Cause Analysis.")
    a("")
    a("## Final Recommendation")
    a("")
    a("For 2027, escalate label revisions (%.2f points between consecutive quarter-end snapshots), place feature "
      "releases (%.2f), optimisation noise (%.2f) and training data (%.2f) on remediation plans, and keep retunes "
      "on monitor (%.2f). Combined model-side movement is %.2f points for 2027 (Q1 %.2f, Q2 %.2f, Q3 %.2f, Q4 %.2f), "
      "and %.1f per cent of 2027's weekly retrains are expected to actually run on pinned feature views. This "
      "rejects accumulating warm-start noise linearly over thirteen refits (escalating optimisation noise at %.2f "
      "points), applying equal-weight window turnover when the recency decay rate is unfiled (dropping training data "
      "to monitor at %.2f points), and treating multi-phase feature releases on the same feature group as orthogonal "
      "(dropping feature releases to monitor at %.2f points, or %.2f on calendar planned dates)." % (
          P["label revisions"], P["feature releases"], P["optimisation noise"], P["training data"], P["retunes"],
          fig["tot_yr"], fig["tot_q1"], fig["tot_q2"], fig["tot_q3"], fig["tot_q4"], fig["cc_pin"],
          rf["points"]["optimisation noise"], rf["points"]["training data"],
          rf["points"]["feature releases"], dr["points"]["feature releases"]))
    a("")
    L.extend(_stump_block(fig))
    a("## Supplementary Questions")
    a("")
    a("### garrane_score_stability_sources_2027.xlsx")
    a("The opening sheet, 2027 placements, leads with the five source placements, the four quarter-pair and full-year "
      "combined model-side movements, and the expected share of 2027 weekly retrains on pinned feature views, all "
      "linked by formulas to supporting sheets for quarter pairs, instruments by family, warm-start noise and "
      "cold-era linearity, recency-weighted training data, feature releases and pinned adoption, the 2026 internal "
      "record check, rival routes and Standard sections 5 and 6 context, and notes.")
    a("")
    a("1. Each model-side source in 2027: the points it alone moves a merchant's score between consecutive "
      "quarter-end snapshots (book weighted at 21 September 2026) and its band.")
    a("   a. Feature releases: %.2f points (band %s), %s." % (
        P["feature releases"], band(B["points_releases"], 2), fig["band_of"]["feature releases"]))
    a("   b. Optimisation noise: %.2f points (band %s), %s." % (
        P["optimisation noise"], band(B["points_optimisation"], 2), fig["band_of"]["optimisation noise"]))
    a("   c. Training data: %.2f points (band %s), %s." % (
        P["training data"], band(B["points_turnover"], 2), fig["band_of"]["training data"]))
    a("   d. Forced sources: label revisions sit in %s at %.2f points (band %s) and retunes stay on %s at %.2f "
      "points (band %s)." % (
          fig["band_of"]["label revisions"], P["label revisions"], band(B["points_labels"], 2),
          fig["band_of"]["retunes"], P["retunes"], band(B["points_retunes"], 2)))
    a("2. Combined model-side movement across all five sources in 2027 (root-mean-square points, book weighted): "
      "Q1 (21 December 2026 to 22 March 2027) %.2f points (band %s), Q2 (22 March to 21 June 2027) %.2f points "
      "(band %s), Q3 (21 June to 20 September 2027) %.2f points (band %s), Q4 (20 September to 20 December 2027) "
      "%.2f points (band %s), and full assessment year %.2f points (band %s)." % (
          fig["tot_q1"], band(B["tot_q1"], 2), fig["tot_q2"], band(B["tot_q2"], 2),
          fig["tot_q3"], band(B["tot_q3"], 2), fig["tot_q4"], band(B["tot_q4"], 2),
          fig["tot_yr"], band(B["tot_yr"], 2)))
    a("3. Pinned feature views: %.1f per cent of 2027's 52 assessment-year weekly retrains across the fourteen "
      "families (28 December 2026 to 20 December 2027, per section 2 of the standard) are expected to actually run on "
      "pinned feature views (band %s)." % (fig["cc_pin"], band(B["cc_pin"], 1)))
    a("")
    a("### garrane_stability_review_2027.pptx")
    a("Five slides leading with the committee call: 2027 placements and headline metrics; source movements against "
      "the 5.5 and 8.0 point thresholds beside standard shortcuts; the quarter-pair profile of combined model-side "
      "movement across 2027; the three structural estimations (warm-start decay, recency weighting, within-group "
      "release covariance); and the 2026 internal record check with 31 January 2027 filing deadlines.")
    a("")
    a("## Critical Components")
    a("")
    a("1. Optimisation noise alone moves a merchant's score **%.2f points** between consecutive quarter-end snapshots "
      "in 2027 (band %s), placing it on a remediation plan." % (fig["cc1"], band(B["cc1"], 2)))
    a("2. Training data alone moves a merchant's score **%.2f points** between consecutive quarter-end snapshots in "
      "2027 (band %s), placing it on a remediation plan." % (fig["cc2"], band(B["cc2"], 2)))
    a("3. Feature releases alone move a merchant's score **%.2f points** between consecutive quarter-end snapshots in "
      "2027 (band %s), placing them on a remediation plan." % (fig["cc3"], band(B["cc3"], 2)))
    a("")
    a("## Step-by-Step")
    a("")
    pk = b["pairs_by_kind"]
    a("1. Assemble and clean the record. Keep the later load_id on the four re-sent weekly refreshes across the ten "
      "quarterly panel CSVs and map Tolka Pay's re-keyed merchant identifiers through tolka_pay_merchant_id_migration.csv, "
      "producing %s unique panel merchants (%s identifiers before mapping) and %s scored merchant-weeks (%s raw rows). "
      "Deduplicate training_scheduler_runs_2024_2026.jsonl on run_id (%s lines, %s distinct runs, %s production refits), "
      "reconcile the renamed rows / train_rows field across the runtime image change, map scheduler job families to "
      "registry codes via gms_model_registry.csv, and align ISO weeks with Monday dates. The 2026 instrument register "
      "contains %s pairs (%d replicate, %d bootstrap, %d retune shadow, %d release shadow, %d label freeze). Book "
      "weights follow section 3 of the stability standard at the latest closed quarter-end snapshot (21 September "
      "2026, %s scored merchants). Leaving any single hygiene step undone keeps every graded figure inside its band." % (
          "{:,}".format(b["panel_merchants"]), "{:,}".format(b["panel_merchants_unmapped"]),
          "{:,}".format(b["score_rows"]), "{:,}".format(b["raw_score_rows"]),
          "{:,}".format(b["manifest_lines"]), "{:,}".format(b["manifest_runs"]),
          "{:,}".format(b["production_runs"]), b["pairs"], pk["replicate"], pk["bootstrap"],
          pk["retune_shadow"], pk["release_shadow"], pk["label_freeze"], "{:,}".format(b["book_sep26"])))
    a("2. Baseline forced sources (retunes and label revisions). Compute each family's mean pair variance from "
      "mrm_instrument_pair_scores_2026.csv and scale by snapshot-pair frequency (one retune every fourth Monday, "
      "%.2f per pair; thirteen weekly label revisions per pair). Book weighted, retunes contribute %.2f "
      "points squared (%.2f points, monitor) and label revisions contribute %.2f points squared (%.2f points, "
      "escalation). Every route lands both placements." % (
          b["retunes_per_pair"], fig["agg"]["retunes"], P["retunes"],
          fig["agg"]["label revisions"], P["label revisions"]))
    a("3. Optimisation noise (Component 1, warm-start persistence). Section 1 of the standard notes that warm-started "
      "refits carry prior training randomness, and the replicate pairs measure fresh single-refit spread (book-weighted "
      "mean-square %.2f points squared). Treating thirteen weekly refits as independent permanent shocks gives %.2f "
      "points (half a replicate pair per refit, escalation) or %.2f points (a full replicate pair per refit, escalation), "
      "while reading a single replicate pair at face value gives %.2f points (monitor). Instead, measure each family's "
      "mean-square score change D_warm(h) across lags h = 1 to 25 over its settled warm weeks (starting 13 weeks after "
      "each family's last cold-start week, or October 2025 where later). Every family's curve is strongly concave: "
      "straight lines fitted on lags 8 to 25 cross lag 0 at %.1f points squared book weighted (at least %.1f in every "
      "family). To verify that this concavity comes from warm-start decay rather than mean-reverting merchant risk, "
      "inspect each family's cold-start era (at least %d weeks before warm-start adoption, range %d to %d weeks): "
      "D_cold(h) across lags 1 to 14 is linear (mean relative quadratic curvature %+.3f, range %+.3f to %+.3f), "
      "ruling out mean-reverting merchant change from the data alone. Fitting D_warm(h) - D_data(h) = b*h + A*(1 - phi^h) "
      "with 1/D^2 weights across lags 1 to 25, anchored to each family's replicate pair variance A*(1 - phi^2) = rep, "
      "gives persistence phi from %.2f to %.2f and 13-week optimisation noise A*(1 - phi^13) of %.2f points (band %s, "
      "remediation plan). Without subtracting the smooth data curve, the anchored fit remains %.2f points (inside the "
      "band), confirming independence from Step 4. Fitting the raw warm curve unanchored absorbs the data curve's bend "
      "and overshoots to %.2f points (implied replicate %.2f against %.2f measured)." % (
          b["replicate"], pr["linear 13 refits (half pair)"], pr["full replicate pair per refit"],
          pr["single replicate pair (over)"], bd["intercept8_book"], bd["intercept8_min"],
          bd["cold_min_weeks"], bd["cold_min_weeks"], bd["cold_max_weeks"],
          bd["cold_curv_mean"], bd["cold_curv_min"], bd["cold_curv_max"],
          b["phi_fit"][0], b["phi_fit"][1], fig["cc1"], band(B["cc1"], 2),
          fig["adm_range"]["points_optimisation"][0],
          pr["unanchored fit (raw curve)"], pr["unanchored raw implied rep"], b["replicate"]))
    a("4. Training data (Component 2, recency-weighted turnover). Section 1 of the standard and the scheduler manifests "
      "(options.sample_weights = recency_decay on 52-week and 104-week windows, versus uniform on 26-week cold windows) "
      "state that long-window refits apply exponential recency weighting and that bootstrap pairs resample with those "
      "production weights, without listing the decay factor. Taking raw bootstrap variance at face value gives %.2f "
      "points (%.2f net of replicate, both escalation), while ignoring recency weighting and applying uniform-window "
      "turnover (entering + leaving)/(2N) drops training data to %.2f points (monitor). Under exponential recency "
      "weighting across a W-week window ending at week t, week u carries normalised weight share p_u(lambda) = "
      "n_u * lambda^(t - u) / sum_v (n_v * lambda^(t - v)), so across each family's 16 bootstrap pairs in 2026 net "
      "bootstrap variance Var_net(f, t) = 2 * row2_f * sum_u (p_u(lambda)^2 / n_u) swings sharply in phase-lagged "
      "anti-phase with the trailing labelled row waves in warehouse_labelled_rows_weekly.csv. Inverting lambda_f and "
      "row2_f by matching log net bootstrap variance across the 16 dates yields lambda_f from %.3f to %.3f and cuts "
      "mean log-RMSE from %.4f (uniform lambda = 1) and %.4f (lag-0 1/n_t) down to %.4f (%.1fx better than uniform). "
      "Alternative smooth recency kernels fitted to the same 16 pairs keep training data in remediation (shifted "
      "power-law (1 + age/g)^(-2) %.2f, linear ramp %.2f) while exponential achieves the lowest log-RMSE. Evaluating "
      "the exact weighted-window "
      "turnover variance row2_f * sum_u (p_{t1, u} - p_{t0, u})^2 / n_u across the four 2027 snapshot spans in "
      "labelled_row_plan_2027.xlsx yields %.2f points (band %s, remediation plan)." % (
          pr["raw bootstrap face value"], pr["net bootstrap face value (over)"], pr["uniform window turnover"],
          b["lam_fit"][0], b["lam_fit"][1], rd["log_rmse_unif"], rd["log_rmse_lag0"], rd["log_rmse_exp"],
          rd["unif_ratio"], rd["kernels"]["power-law (a=2)"]["points"], rd["kernels"]["linear ramp"]["points"],
          fig["cc2"], band(B["cc2"], 2)))
    a("5. Feature releases and pinned feature views (Component 3, within-group merchant covariance). First, model "
      "actual pinned-view take-up from the three completed rollouts (PC-24-031, PC-24-047, PC-25-012) by pairing "
      "platform_change_calendar.xlsx against first actual use and 26-week post-adoption reverts in the scheduler "
      "manifests. Fitting log-lag from environment completion to first actual use on each family's "
      "custom_training_components (validated leave-one-rollout-out: runtime %.1f vs %.1f per cent, warm start %.1f vs "
      "%.1f, bf16 %.1f vs %.1f) and evaluating the log-normal adoption curve from planned week plus mean calendar slip "
      "scaled by (1 - mean revert share) over the 52 assessment-year Mondays (28 December 2026 to 20 December 2027, "
      "section 2 of the standard) gives %.1f per cent of 2027 retrains on pinned views (band %s), against %.1f per "
      "cent on calendar planned weeks and %.1f per cent on environment-release slip alone. Second, inspect the "
      "merchant-level signed score deltas (score_b - score_a) across the 2026 release_shadow pairs in "
      "mrm_instrument_pair_scores_2026.csv joined to feature_platform_release_log.csv via excluded_release. "
      "Single-release variance is flat across groups (book-weighted mean %.2f points squared), and 2026's semi-annual "
      "releases were spaced 27 weeks apart per group so weekly panel regressions see no clustering. At the merchant "
      "level, however, every pair of releases modifying the same feature group moves the same merchants in the same "
      "direction: across all %d same-group pairs in 2026, pairwise correlation is strictly positive (mean %.3f, "
      "minimum %.3f), whereas the %d cross-group pairs average %+.3f. In 2027, feature_platform_roadmap_2027.xlsx "
      "packs multi-phase sprints (three phased releases per priority group per quarter-pair). Evaluating each family's "
      "pair variance sum_k P_live(t_k) * v_f + 2 * sum_{k < l, same group} P_live(max(t_k, t_l)) * c_f * v_f yields "
      "%.2f points (band %s, remediation plan). Treating releases as orthogonal drops feature releases to monitor at "
      "%.2f points (%.2f on calendar planned dates), while treating all releases in a pair as perfectly aligned "
      "regardless of group pushes them to escalation at %.2f points." % (
          100.0 * fig["loo"]["runtime"]["record"], 100.0 * fig["loo"]["runtime"]["model"],
          100.0 * fig["loo"]["warm"]["record"], 100.0 * fig["loo"]["warm"]["model"],
          100.0 * fig["loo"]["amp"]["record"], 100.0 * fig["loo"]["amp"]["model"],
          fig["cc_pin"], band(B["cc_pin"], 1), b["cov_plan"], b["cov_declared"],
          b["release"], b["coh_same_n"], b["coh_same_mean"], b["coh_same_min"],
          b["coh_diff_n"], b["coh_diff_mean"], fig["cc3"], band(B["cc3"], 2),
          pr["orthogonal releases (actual lag)"], pr["orthogonal releases (calendar plan)"],
          pr["all releases aligned (over)"]))
    a("6. Internal 2026 record falsification check. Without observing any 2027 target, test every route against three "
      "2026 statistics in native points squared: (i) settled warm 1-week panel variance D_warm(1) = %.2f (committed "
      "model implies %.2f), (ii) high-minus-low trailing-volume bootstrap net-variance contrast = %.2f (committed model "
      "implies %.2f), and (iii) same-group release-shadow cross-release merchant covariance = %.2f (committed model "
      "implies %.2f). Total absolute discrepancy is %.2f points squared for the committed model, versus %.2f when S1 is "
      "dropped (linear carry), %.2f when S2 is dropped (uniform window), %.2f when S3 is dropped (orthogonal releases), "
      "%.2f for the direct route, and %.2f for the rigorous standard shortcut." % (
          fa["obs_d1"], fa["golden_parts"]["d1"], fa["obs_boot_contrast"], fa["golden_parts"]["boot_c"],
          fa["obs_rel_cov"], fa["golden_parts"]["rel_cov"], fa["golden_err"],
          fa["rivals"]["S1 linear carry"], fa["rivals"]["S2 uniform window"],
          fa["rivals"]["S3 orthogonal releases"], fa["rivals"]["direct"],
          fa["rivals"]["rigorous (Response 1)"]))
    a("7. Combined model-side movement and 2027 placements. Summing the five independent sources' expected mean-square "
      "movements per snapshot pair (section 3 of the standard) yields combined model-side movement of %.2f points in Q1, "
      "%.2f in Q2, %.2f in Q3, %.2f in Q4, and %.2f points across the assessment year (root of the four pairs' mean "
      "square). Comparing each source's annual points against section 4's 5.5 and 8.0 thresholds places label revisions "
      "in escalation (%.2f), feature releases (%.2f), optimisation noise (%.2f) and training data (%.2f) on remediation "
      "plans, and retunes on monitor (%.2f). For sections 5 and 6 context, the workbook also reports model-side shares, "
      "merchants' own share of all movement (%.1f per cent), and Schedule C tier-change rates scaled from 2026 "
      "empirical rates by each family's root-variance ratio (%.1f per cent as scheduled versus %.1f per cent with "
      "designated sources removed, against the 12 per cent cap; a direct Gaussian projection on the 21 September 2026 "
      "panel reaches the same cap conclusion)." % (
          fig["tot_q1"], fig["tot_q2"], fig["tot_q3"], fig["tot_q4"], fig["tot_yr"],
          P["label revisions"], P["feature releases"], P["optimisation noise"], P["training data"], P["retunes"],
          fig["own_share"], fig["fr_sched"], fig["fr_removed"]))
    a("8. Why no other conclusion survives. Across %d estimation variants spanning lag horizons (18 to 25 weeks, 2026 "
      "only, lag 2 start, flat weights, with and without subtracting the data curve), recency fitting choices (by "
      "family, by window length, pooled, log-OLS, WLS, OLS), pooled vs per-family release coherence, six pinned-view "
      "adoption specifications (log-linear, linear, grouped, family-own, pooled, no-revert, plug-in medians), settled-week "
      "start rules, and December 2027 planned weights, every single variant files the exact same five placements and "
      "keeps every source at least 0.70 points away from the 5.5 and 8.0 lines (holding under +/-20 per cent variance "
      "perturbations on every source). Every alternative band call requires violating at least one direct 2026 "
      "instrument check (5.3 to 28.5 points squared discrepancy against 0.53 for the golden): S1 alone flips "
      "optimisation noise to escalation (%.2f) or monitor (%.2f), S2 alone flips training data to monitor (%.2f) or "
      "escalation (%.2f), and S3 alone flips feature releases to monitor (%.2f) or escalation (%.2f)." % (
          fig["variants"],
          lat["S1"]["points"]["optimisation noise"], ov["S1"]["points"]["optimisation noise"],
          lat["S2"]["points"]["training data"], ov["S2"]["points"]["training data"],
          lat["S3"]["points"]["feature releases"], ov["S3"]["points"]["feature releases"]))

    text = "\n".join(L) + "\n"
    assert "\u2014" not in text and "\u2013" not in text, "em/en dash found in submission.md"
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)
    return text
