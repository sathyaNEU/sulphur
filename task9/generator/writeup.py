"""task9 architecture 5: submission.md, the four answer blocks, every figure from figures.json at the blocks'
rounding, each band rounded outward."""
import math

import results as RS

NAMES = RS.NAMES
ORDER = RS.ORDER
KEY = {"optimisation": "optimisation", "turnover": "turnover", "retunes": "retunes", "releases": "releases",
       "labels": "labels"}


def lo(x, dp):
    return math.floor(x * 10 ** dp + 1e-9) / 10 ** dp


def hi(x, dp):
    return math.ceil(x * 10 ** dp - 1e-9) / 10 ** dp


def band(b, dp):
    return "%.*f to %.*f" % (dp, lo(b[0], dp), dp, hi(b[1], dp))


def stated(fig):
    """The bands the blocks state, at the blocks' rounding (written to figures.json)."""
    B = fig["bands"]
    out = {}
    for s in ORDER:
        out["points_" + s] = [lo(B["points_" + s][0], 2), hi(B["points_" + s][1], 2)]
        out["share_" + s] = [lo(B["share_" + s][0], 1), hi(B["share_" + s][1], 1)]
    for k in ("cc3", "own_share", "fr_sched", "fr_removed"):
        out[k] = [lo(B[k][0], 1), hi(B[k][1], 1)]
    return out


def cap(s):
    return s[0].upper() + s[1:]


def _stump_block(fig):
    """The form's stump question (How is each model stumped?), written from the two saved responses of the trimmed
    prompt's first pair (pair 3: runs/run1.md and runs/run2.md; the earlier pairs are archived as
    runs/arch5_pair1_* and runs/arch5_pair2_*). Every response figure and phrase is held here exactly as the
    response writes it and asserted against the saved text; every golden-side figure comes from figures.json. It is
    mandatory once both responses are on file and sits directly after the Final Recommendation."""
    import csv
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    task = os.path.dirname(here)
    r1p, r2p = (os.path.join(task, "runs", n) for n in ("run1.md", "run2.md"))
    if not (os.path.exists(r1p) and os.path.exists(r2p)):
        return []
    t1, t2 = open(r1p, encoding="utf-8").read(), open(r2p, encoding="utf-8").read()
    rec1 = ("escalate Label revisions (9.99 points) and Optimisation noise (9.10 points); place Training data (6.57 "
            "points) and Feature releases (6.41 points) on remediation plans; keep Retunes (4.47 points) on monitor")
    rec2 = ("Escalate optimisation noise and label revisions; put training data and feature releases on remediation "
            "plans; monitor retunes")
    q1 = {"inc": "A next refit carries one increment, so per-refit variance is half the pair MS; 13 refits "
                 "accumulate linearly",
          "add": "Weekly increments and sources accumulate linearly in MS; source effects persist once landed",
          "alt": "giving noise 12.87; still Escalation and does not change the call",
          "ols": "OLS with family fixed effects",
          "turn": "turnover = (entering + leaving)/(2N)",
          "obs": "I used planned Monday to first production refit week, not environment release",
          "on": "9.10", "td": "6.57", "fr": "6.41", "cc3": "61.17%", "ms": "82.8161", "own": "159.1608",
          "rows": "3,360,865 rows", "runs": "2,464 unique runs", "map": "4,568 IDs", "pairs": "644 pairs"}
    q2 = {"s14": "§1.4 gives no decay/rho parameter",
          "unstated": "I did not fit an unstated decay to panel time series and then present it as the standard",
          "exam": "I examined panel time-series behavior but did not impose an unstated decaying-persistence model "
                  "on the placement arithmetic",
          "stable": "own-change residuals under full accumulation were stable across the three closed pairs",
          "tier": "the tier model reproduced monitor rates",
          "raw": "Raw bootstrap MSE would overstate training movement by roughly two orders of magnitude",
          "lags": "scheduler history systematically lags planned weeks",
          "monitor": "reproduced all 42 counts and changes exactly",
          "on": "12.8698", "td": "6.7516", "fr": "6.3016", "iso": "63.0495%", "py": "61.1264%",
          "ms": "165.6321", "own": "74.128653", "map": "4,568 old",
          "pairs": "644 pairs; 224 release-shadow, 168 retune-shadow, 112 label-freeze, 84 replicate, 56 bootstrap"}
    for q in list(q1.values()) + [rec1]:
        assert q in t1, "Response 1 quote missing from runs/run1.md: %r" % q
    for q in list(q2.values()) + [rec2]:
        assert q in t2, "Response 2 quote missing from runs/run2.md: %r" % q

    P, B, st, b, pr, lat, bd = (fig[k] for k in ("points", "bands", "stated", "base", "probe", "lattice", "bend"))
    f2, f1 = (lambda x: "%.2f" % x), (lambda x: "%.1f" % x)
    pc = lambda q: q[:-1] if q.endswith("%") else q
    inside = lambda x, k: st[k][0] <= x <= st[k][1]
    mapped = b["panel_merchants_unmapped"] - b["panel_merchants"]
    # both responses file the call the lattice gives for the noise step missed alone
    c = {"optimisation noise: escalation", "label revisions: escalation", "training data: a remediation plan",
         "feature releases: a remediation plan", "retunes: monitor"}
    assert c == set(lat["S2"]["call"]), "the responses' call is not the lattice's noise step missed alone"
    assert set(lat["S1"]["call"]) == (set(fig["call"]) - {"training data: a remediation plan"}) | {
        "training data: escalation"}, "the training-data step missed alone moves more than training data"
    assert pr["feature releases on the calendar's planned weeks"] < 5.5
    # the noise figures are the two full sums, outside the band; the steps called made sit inside their bands
    assert q1["on"] == f2(pr["thirteen refits added up"]) == f2(lat["S2"]["points"]["optimisation noise"])
    assert f2(float(q2["on"])) == f2(pr["a whole replicate pair a refit"])
    assert all(float(q["on"]) >= 8 and not inside(float(q["on"]), "points_optimisation") for q in (q1, q2))
    assert inside(float(q1["td"]), "points_turnover") and inside(float(q2["td"]), "points_turnover")
    assert inside(float(q1["fr"]), "points_releases") and 5.5 <= float(q2["fr"]) < 8.0
    assert all(float(x[:-1]) > st["cc3"][1] for x in (q1["cc3"], q2["iso"], q2["py"]))
    # the cleaning counts each response reports are the golden's
    assert "{:,}".format(b["score_rows"]) in q1["rows"] and "{:,}".format(b["manifest_runs"]) in q1["runs"]
    assert "{:,}".format(mapped) in q1["map"] and "{:,}".format(mapped) in q2["map"]
    assert str(b["pairs"]) in q1["pairs"] and str(b["pairs"]) in q2["pairs"]
    assert all("%d %s" % (n, k.replace("_", "-")) in q2["pairs"] for k, n in b["pairs_by_kind"].items())
    with open(os.path.join(task, "target", "covenant_tier_change_monitor_2026.csv"), newline="") as fh:
        assert sum(1 for _ in csv.DictReader(fh)) == 42
    # merchants' own change, the record less the sources, takes up the noise model's difference one for one
    d_ms, d_own = float(q2["ms"]) - float(q1["ms"]), float(q1["own"]) - float(q2["own"])
    assert d_ms > 50 and abs(d_ms - d_own) < 0.05 * d_ms, (d_ms, d_own)
    assert bd["intercept8_min"] > 0

    bo, bt, bf, bc = (band(B[k], d) for k, d in (("points_optimisation", 2), ("points_turnover", 2),
                                                   ("points_releases", 2), ("cc3", 1)))
    p1 = (f"**Response 1** files optimisation noise in escalation at {q1['on']} points, where the answer is a "
          f"remediation plan at {f2(fig['cc2'])} (band {bo}); its other four placements are the answer's, so it "
          "escalates two sources where the answer escalates one. It saw that a warm-started refit carries the noise "
          f"of the refits before it, and assumed that noise never fades: \"{q1['inc']}\", and among its "
          f"assumptions, \"{q1['add']}\". The one alternative it weighed was another full sum, a whole replicate "
          f"pair a refit (\"{q1['alt']}\"). Its validation could not catch the choice: the weekly regression it ran "
          f"on the panel (\"{q1['ols']}\") gives every family its own constant, and that constant takes up whatever "
          "the noise adds week to week, so the fit tested releases, retunes and training rows and never the noise. "
          f"It made the training-data step, {q1['td']} points against {f2(fig['cc1'])} (band {bt}), by scaling the "
          f"bootstrap spread to each window's turnover (\"{q1['turn']}\"), and the pinned-views step's deciding "
          f"move, \"{q1['obs']}\", which keeps feature releases on a plan at {q1['fr']} against "
          f"{f2(P['feature releases'])} (band {bf}). Its pinned share is {pc(q1['cc3'])} per cent against "
          f"{f1(fig['cc3'])} (band {bc}).")
    p2 = (f"**Response 2** files the same call, with optimisation noise at {q2['on']} points: a whole replicate pair "
          "counted for each of the thirteen refits between two snapshots. It ruled the decay out on the standard's "
          f"silence (\"{q2['s14']}\"; \"{q2['unstated']}\") and set aside the evidence it had looked at: "
          f"\"{q2['exam']}\". The check it offers for the full carry cannot fail: its 2026 \"{q2['stable']}\" and "
          f"\"{q2['tier']}\". Merchants' own change is what the record leaves once the sources are taken out, so it "
          f"takes up whatever the noise model puts in: Response 2's noise mean-square ({q2['ms']}) is {d_ms:.2f} "
          f"above Response 1's ({q1['ms']}), and its own change ({q2['own']}) is {d_own:.2f} below Response 1's "
          f"({q1['own']}), and both responses' tier checks fit 2026 whatever the split, since they see only the "
          f"sum. It made the training-data step, {q2['td']} points inside the band, by scaling the bootstrap pairs "
          f"to each week's turnover (\"{q2['raw']}\"), and it refused the calendar for actual use (\"{q2['lags']}\"), "
          f"keeping feature releases on a plan at {q2['fr']}. Its pinned share is {pc(q2['iso'])} per cent over "
          f"calendar 2027's Mondays and {pc(q2['py'])} over the four pairs' refreshes, against {f1(fig['cc3'])}.")
    p3 = ("**Why this is a fair stump.** No planted row and no buried sentence decides it. Both responses cleaned the "
          f"record to the answer's own counts before they went wrong: Response 1 reports "
          f"{'{:,}'.format(b['score_rows'])} scored merchant-weeks, {'{:,}'.format(b['manifest_runs'])} distinct "
          f"runs, {'{:,}'.format(mapped)} Tolka Pay identifiers mapped and {b['pairs']} instrument pairs, and "
          f"Response 2 the same {b['pairs']} pairs by kind and the 2026 covenant monitor \"{q2['monitor']}\". The "
          "standard says a warm-started refit's randomness carries (section 1.4, which Response 2 cites) and nowhere "
          "says it carries in full. How far it carries is in the shape of whole files: in every family's panel "
          "history the mean-square change between two scores bends towards a ceiling as the gap between them grows, "
          f"and a straight line through gaps 8 to 26 meets gap 0 at {f1(bd['intercept8_book'])} points squared, book "
          f"weighted, and at {f1(bd['intercept8_min'])} or more in every family, where a carry that never fades "
          "runs through the origin. The carry is how the scheduler warm-starts all fourteen families, not a "
          "property of the units that decide the call, and both responses had the files open (Response 1 regressed "
          "on the weekly panel; Response 2 says it examined its time-series behaviour). The two steps both responses "
          "made from the same pack, training data and pinned views' actual use, show the evidence is reachable.")
    p4 = ("**Why it takes rigour.** The noise has three ready readings and each files the wrong band: the replicate "
          f"pairs at face value give {f2(pr['the replicate pair read as the gap' + chr(39) + 's whole noise'])} "
          f"points (monitor); each refit's fresh draw added in full gives {f2(pr['thirteen refits added up'])}, "
          f"Response 1's figure, and a whole replicate pair a refit {f2(pr['a whole replicate pair a refit'])}, "
          "Response 2's (escalation both); and the bend fitted free of the replicate pairs gives "
          f"{f2(pr['unanchored fit'])} but implies replicate pairs of {f2(pr['unanchored implied replicate'])} where "
          f"{f2(b['replicate'])} is measured. The answer needs each family's curve fitted on its settled warm weeks "
          f"with its start tied to the measured replicate variance, which gives a persistence of "
          f"{f2(b['phi_fit'][0])} to {f2(b['phi_fit'][1])} and {f2(fig['cc2'])} points, a remediation plan. The "
          "steps are independent and each moves its own source: with only the noise step missed, optimisation noise "
          f"goes to escalation at {f2(lat['S2']['points']['optimisation noise'])} and nothing else moves, the call "
          "both responses file; with only the training-data step missed, training data goes to escalation at "
          f"{f2(lat['S1']['points']['training data'])} and nothing else moves; with the calendar taken for actual "
          "use, feature releases drop to monitor at "
          f"{f2(pr['feature releases on the calendar' + chr(39) + 's planned weeks'])}. Both responses made the "
          "training-data step and refused the calendar, and both missed the noise step.")
    for p in (p1, p2, p3, p4):
        assert "—" not in p and "–" not in p
    return ["## How is each model stumped?", "", p1, "", p2, "", p3, "", p4, ""]


def write(path, fig):
    B = fig["bands"]
    P, S = fig["points"], fig["share"]
    b = fig["base"]
    rf = fig["reflex"]
    pr = fig["probe"]
    fa = fig["falsification"]
    lat = fig["lattice"]
    L = []
    a = L.append
    a("# task9: Garrane Merchant Score, sources of score movement for 2027")
    a("")
    a("## Tags")
    a("")
    a("**Domain:** General Statistics & Data Science, Interpretability (feature attribution, probing, mechanistic "
      "analysis).")
    a("**Analytical objective:** Root-Cause Analysis.")
    a("")
    a("## Final Recommendation")
    a("")
    a("For 2027, escalate label revisions (%.2f points between consecutive quarter-end snapshots) and put optimisation "
      "noise (%.2f), feature releases (%.2f) and training data (%.2f) on remediation plans; keep retunes on monitor "
      "(%.2f). This rejects reading the bootstrap pairs as the movement and adding the thirteen refits' fresh noise "
      "up in full, which escalates training data at %.2f points and optimisation noise at %.2f." % (
          P["label revisions"], P["optimisation noise"], P["feature releases"], P["training data"], P["retunes"],
          rf["points"]["training data"], rf["points"]["optimisation noise"]))
    a("")
    L.extend(_stump_block(fig))
    a("## Supplementary Questions")
    a("")
    a("### garrane_score_stability_sources_2027.xlsx")
    a("The first sheet, 2027 placements, lists the five sources by band with their points and band, and the share of "
      "2027's retrains expected on pinned feature views beneath; then sheets for the instruments by family, training "
      "data, gap curves, pinned feature views, the weekly check, other routes and notes.")
    a("")
    a("1. Each model-side source in 2027: the points it alone moves a merchant's score between consecutive "
      "quarter-end snapshots (book weighted) and its band.")
    for i, s in enumerate(ORDER):
        n = NAMES[s]
        a("   %s. %s: %.2f points (band %s), %s." % ("abcde"[i], cap(n), P[n], band(B["points_" + s], 2),
                                                    fig["band_of"][n]))
    a("2. Pinned feature views: %.1f per cent of 2027's weekly retrains are expected to actually run on them, family-weeks across the "
      "fourteen families (band %s)." % (fig["cc3"], band(B["cc3"], 1)))
    a("")
    a("### garrane_stability_review_2027.pptx")
    a("Three slides: the call with each source's points and band; a bar chart of each source's points against "
      "dashed lines at 5.5 and 8; the share of 2027's retrains expected on pinned views against the calendar's two "
      "readings, with feature releases' points under each.")
    a("")
    a("## Critical Components")
    a("")
    a("1. Training data alone moves a merchant's score **%.2f points** between consecutive quarter-end snapshots in 2027 "
      "(band %s)." % (fig["cc1"], band(B["cc1"], 2)))
    a("2. Optimisation noise alone moves a merchant's score **%.2f points** between consecutive quarter-end snapshots in "
      "2027 (band %s)." % (fig["cc2"], band(B["cc2"], 2)))
    a("")
    a("## Step-by-Step")
    a("")
    pk = b["pairs_by_kind"]
    a("1. Assemble the record. The ten quarterly panel files keep the later load where a refresh was re-sent and map "
      "Tolka Pay's re-keyed merchants through the migration file, which leaves %s panel merchants (%s identifiers "
      "before the mapping) and %s scored merchant-weeks; the registry's family codes are matched to the "
      "scheduler's; the manifests' %s lines carry %s distinct runs, %s of them production refits; the pair register "
      "holds %s pairs (%d replicate, %d bootstrap, %d retune shadow, %d release shadow, %d label freeze)." % (
          "{:,}".format(b["panel_merchants"]), "{:,}".format(b["panel_merchants_unmapped"]),
          "{:,}".format(b["score_rows"]), "{:,}".format(b["manifest_lines"]), "{:,}".format(b["manifest_runs"]),
          "{:,}".format(b["production_runs"]), b["pairs"], pk["replicate"], pk["bootstrap"], pk["retune_shadow"],
          pk["release_shadow"], pk["label_freeze"]))
    a("2. Retunes and label revisions. Each instrument's pair variance by family, book weighted at the 21 September "
      "2026 snapshot, scaled by what a snapshot pair holds (a retune every fourth week, a label revision every "
      "week): retunes %.2f points and label revisions %.2f. Every route lands these two; they are not where the "
      "call is decided." % (P["retunes"], P["label revisions"]))
    a("3. Training data. The bootstrap pairs differ by %.2f points squared, book weighted (%.2f net of the replicate "
      "pairs' seed part). Read as the movement, that is %.2f points and escalation. But a bootstrap pair resamples "
      "the whole window, while two quarter-end models share every row of their windows except the thirteen weeks "
      "that left and the thirteen that entered: the bootstrap spread gives the noise per training row, and the "
      "manifests' windows (%d families on 104 weeks, the rest on 52) and the warehouse and plan rows give how many "
      "rows each 2027 snapshot pair turns over, the change in a window fit between two snapshots carrying the "
      "per-row noise times 1/N1 + 1/N2 - 2S/(N1 N2), with N1 and N2 the rows in the two windows and S the rows they "
      "share. Training data alone is %.2f points, a remediation plan." % (
          b["bootstrap_raw"], b["bootstrap_net"], rf["points"]["training data"], b["long_window_families"],
          fig["cc1"]))
    sf = fig["settled_floor"]
    aw = fig["assessment_weeks"]
    a("4. Optimisation noise. The replicate pairs differ by %.2f points squared, book weighted, which would be %.2f "
      "points and monitor if a refit's fresh noise were all two snapshot models differ by; the standard's section "
      "1.4 rules that out, since a warm-started refit carries the randomness of the refits before it, so the later "
      "snapshot model holds the noise of the thirteen refits between. Added up in full, each refit's fresh draw "
      "(half a replicate pair) gives %.2f points and escalation, and a whole replicate pair a refit %.2f; but the "
      "carried noise decays. Each family's settled warm weeks run from thirteen weeks after its last cold-started retrain in the "
      "manifests, and not before the refresh of %s (the record's last %d weeks). Over them the score history's "
      "mean-square change by gap h bends towards a ceiling: fitted family by family over gaps 1 to 26 as "
      "b h + A(1 - p^h), with A(1 - p^2) set to the family's replicate-pair variance, each gap weighted by the "
      "inverse square of its mean-square change and p searched from %.2f to %.3f in steps of %.4f, it gives a persistence p of %.2f "
      "to %.2f by family and %.2f points, a remediation plan. The full sums are refused by the bend: a persistence "
      "of 1 puts every source on a straight line through the origin, but every family's line through gaps 8 to 26 "
      "meets gap 0 above zero (%.1f points squared, book weighted, and at least %.1f in every family), and a line "
      "through the origin misfits every family's curve, by the same weights, %.1f times or more as badly as the "
      "fitted curve (%.0f times at the median family). Fitted free of the replicate pairs the curve gives %.2f points "
      "but implies replicate pairs of %.2f where %.2f is measured, so it is refused by the pairs. A straight line's "
      "start moves with its first gap (%.2f points from gap 1, %.2f from gap 8, %.2f from gap 20), so the curve is "
      "still bending, and the fitted curve put through the same line on gaps 8 to 26 returns %.2f against its own "
      "%.2f: a line's start is not the movement at thirteen weeks." % (
          b["replicate"], pr["the replicate pair read as the gap's whole noise"], rf["points"]["optimisation noise"],
          pr["a whole replicate pair a refit"], sf["date"], sf["weeks"], fig["fit_grid"][0],
          fig["fit_grid"][1], fig["fit_grid"][2], b["phi_fit"][0], b["phi_fit"][1], fig["cc2"],
          fig["bend"]["intercept8_book"], fig["bend"]["intercept8_min"], fig["bend"]["misfit_min"],
          fig["bend"]["misfit_median"], pr["unanchored fit"], pr["unanchored implied replicate"], b["replicate"],
          fig["bend"]["line_from_1"], fig["bend"]["line_from_8"], fig["bend"]["line_from_20"],
          fig["bend"]["fitted_line8"], fig["cc2"]))
    a("5. Pinned feature views and feature releases. 2027's retrains are the %d weekly refreshes of the four "
      "snapshot pairs closing in 2027, %s to %s, and the share asked for is of those expected to actually run on "
      "pinned views. On the calendar's planned weeks %.1f per cent of them would, and %.1f per cent on its "
      "completed dates. The calendar marks a change complete when the image "
      "is released; the manifests show when each family first trained on the three past changes: %d family "
      "rollouts, first use %d to %d weeks after completion (median %.0f), a median of %.1f weeks with no custom "
      "training components and %.1f with %d, and %.1f per cent of the following 26 weeks reverted. A lag model "
      "carries this to the pinned views: each family's 2027 rollout is placed at its planned week plus the past "
      "rollouts' mean slip, counted in weekly refreshes from the planned week to the refresh week of the completed "
      "date (%.2f weeks); the lag from that week to first use is fitted log-linear on custom components with its "
      "spread integrated, and the reverted share is netted from the weeks on, which puts %.1f per cent of 2027's "
      "retrains on pinned views; every take-up form, log-linear or linear, by group, by family or pooled, integrated "
      "or as a plug-in median lag, with or without reverts, puts it between %.1f and %.1f per cent. Leaving each past "
      "rollout out in turn, the model puts %.1f, %.1f and %.1f per cent of its first 39 weeks, counted from each "
      "family's completed date, on the change, against %.1f, %.1f and %.1f recorded. Under the standard's section "
      "1.5 no feature release moves a family's scores in the weeks it trains and scores on pinned views: with the "
      "release shadows' variance and the roadmap's %d releases, feature releases alone are %.2f points, a "
      "remediation plan (%.2f on the calendar's planned weeks and %.2f on its completed dates, monitor either way; "
      "%.2f left whole on pinned weeks, which section 1.5 refuses; %.2f if the release level of the settled weeks "
      "is carried instead of the roadmap, which section 2.1 refuses)." % (
          aw["refreshes"], aw["first"], aw["last"], b["cov_plan"], b["cov_declared"], b["past_family_rollouts"],
          b["past_lag_range"][0], b["past_lag_range"][1], b["past_lag_median"], b["lag_median_custom0"],
          b["lag_median_custom_max"], b["custom_max"], 100 * b["revert_share"], b["slip_mean"], fig["cc3"],
          fig["takeup_range"][0], fig["takeup_range"][1], 100 * fig["loo"]["runtime"]["model"], 100 * fig["loo"]["warm"]["model"], 100 * fig["loo"]["amp"]["model"],
          100 * fig["loo"]["runtime"]["record"], 100 * fig["loo"]["warm"]["record"],
          100 * fig["loo"]["amp"]["record"], b["releases_2027"], P["feature releases"],
          pr["feature releases on the calendar's planned weeks"], fig["rigorous"]["points"]["feature releases"],
          pr["feature releases left whole on pinned views"], pr["2026's release level carried"]))
    a("6. The check. Each route's own model of how a source's variance grows with the gap is asked for the "
      "mean-square change between consecutive weekly refreshes over the same settled weeks, which the record holds "
      "at %.2f, book weighted: this assessment gives %.2f; both the bootstrap and the replicate pairs read at face "
      "value give %.2f; the bootstrap spread at any gap %.2f; the replicate pairs at any gap %.2f." % (
          fa["record"], fa["golden"], fa["rivals"]["both at face value"], fa["rivals"]["bootstrap spread at any gap"],
          fa["rivals"]["replicate variance at any gap"]))
    lt = lambda k, n: lat[k]["points"][n]
    a("")
    nl = fig["nearest_line"]
    a("No other conclusion survives. %d variants (the gap fit over 20, 26 or 30 gaps, weighted or flat, pooled or "
      "per family, events taken out, on 2026 only; the settled weeks started at the first warm retrain, thirteen "
      "weeks after the last cold one with no floor, or at the last past rollout's first use; the take-up model "
      "log-linear, linear, by group or by family, integrated or as a plug-in median lag, and pooled or without "
      "reverts; the planned "
      "book, the latest bootstrap week, four tier mappings, and the panel's weights in place of the book's) file "
      "the same five bands, the nearest a variant comes to a line being %s at %.2f against %s. The two decisive "
      "steps are independent: with only the training-data step missed, training data goes to escalation (%.2f) and "
      "nothing else moves; with only the optimisation step missed, optimisation noise goes to escalation (%.2f) and "
      "nothing else moves; with both missed both move (training data %.2f and optimisation noise %.2f), the hurried "
      "call in the Final Recommendation. The pinned-views take-up supports the call: with the calendar's dates taken "
      "for first use, feature releases drop to monitor (%.2f on its planned weeks, %.2f on its completed dates). "
      "The thinnest margin is optimisation noise's floor: its band starts "
      "at %.2f, between the flat fit on settled weeks from thirteen weeks after the last cold retrain with no floor "
      "(%.2f) and the line through gaps 8 to 26 (%.2f)." % (
          fig["variants_all"], nl["source"], nl["points"], ("%g" % nl["line"]), lt("S1", "training data"),
          lt("S2", "optimisation noise"), lt("S1+S2", "training data"), lt("S1+S2", "optimisation noise"),
          pr["feature releases on the calendar's planned weeks"], fig["rigorous"]["points"]["feature releases"],
          fig["stated"]["points_optimisation"][0],
          fig["forks"]["admitted_range"]["points_optimisation"][0], pr["line through gaps 8 to 26"]))
    a("")
    open(path, "w").write("\n".join(L))
