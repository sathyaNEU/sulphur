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
    """The form's stump question (How is each model stumped?), written from the two saved responses of the reshipped
    pack's first pair (runs/run1.md, runs/run2.md). Every response figure and phrase is held here exactly as the
    response writes it and asserted against the saved text; every golden-side figure comes from figures.json. It is
    mandatory once both responses are on file and sits directly after the Final Recommendation."""
    import os
    here = os.path.dirname(os.path.abspath(__file__))
    r1p, r2p = (os.path.join(os.path.dirname(here), "runs", n) for n in ("run1.md", "run2.md"))
    if not (os.path.exists(r1p) and os.path.exists(r2p)):
        return []
    t1, t2 = open(r1p, encoding="utf-8").read(), open(r2p, encoding="utf-8").read()
    q1 = {"rec": "Escalate optimisation noise and label revisions to the board risk committee; place training data and "
                 "feature releases in remediation plans; monitor retunes",
          "perm": "warm-started sources were treated as permanent 13-week random-walk accumulations rather than "
                  "decaying effects",
          "half": "one weekly refit's noise shock is half the replicate pair mean-square",
          "slopes": "slopes near zero",
          "adopt": "It is actual adoption measured from prior platform changes, not the planned schedule",
          "on": "9.10", "td": "6.61", "fr": "6.54", "cc3": "58.97%", "own": "34.79%", "frr": "8.52%",
          "rows": "3,360,865", "map": "4,568 Tolka Pay identifier pairs", "pairs": "644 instruments"}
    sh1 = {"label revisions": "34.52%", "optimisation noise": "28.66%", "feature releases": "14.79%",
           "training data": "15.10%", "retunes": "6.92%"}
    q2 = {"rec": "Place optimisation noise and label revisions in escalation, training data in a remediation plan, and "
                 "feature releases and retunes in monitor for 2027",
          "s14": "Standard 1.4 says a warm-started refit starts from prior weights, so earlier refit randomness carries "
                 "into later refits",
          "carry": "Warm-start treated as full carry/random-walk accumulation, with no decay",
          "flag": "this is the assumption most capable of changing the recommendation, and I flag rather than hide it",
          "cal": "every family pinned by Monday 22 February 2027",
          "sched": "Pinned weeks taken on schedule", "cond": "the Monitor placement is conditional",
          "on": "12.870", "td": "7.278", "fr": "4.001", "cc3": "92.857%", "own": "17.73%", "frr": "6.63%",
          "rows": "3,360,865", "map": "4,568 Tolka Pay old merchant IDs", "pairs": "644 pairs"}
    flat2 = ("75.610", "78.493", "75.005")
    sh2 = {"label revisions": "28.15%", "optimisation noise": "46.74%", "feature releases": "4.52%",
           "training data": "14.95%", "retunes": "5.64%"}
    for q in list(q1.values()) + list(sh1.values()):
        assert q in t1, "Response 1 quote missing from runs/run1.md: %r" % q
    for q in list(q2.values()) + list(sh2.values()) + list(flat2):
        assert q in t2, "Response 2 quote missing from runs/run2.md: %r" % q

    P, S, B, st, b, pr, lat, bd = (fig[k] for k in ("points", "share", "bands", "stated", "base", "probe", "lattice",
                                                     "bend"))
    f2, f1 = (lambda x: "%.2f" % x), (lambda x: "%.1f" % x)
    pc = lambda q: q[:-1] if q.endswith("%") else q
    key = {NAMES[s]: s for s in ORDER}
    inside = lambda x, k: st[k][0] <= x <= st[k][1]
    mapped = b["panel_merchants_unmapped"] - b["panel_merchants"]
    # the calls the block gives each response, against the core's lattice
    c1 = {"optimisation noise: escalation", "label revisions: escalation", "training data: a remediation plan",
          "feature releases: a remediation plan", "retunes: monitor"}
    c2 = (c1 - {"feature releases: a remediation plan"}) | {"feature releases: monitor"}
    assert c1 == set(lat["S2"]["call"]), "Response 1's call is not the lattice's noise step missed alone"
    assert set(lat["S1"]["call"]) == (set(fig["call"]) - {"training data: a remediation plan"}) | {
        "training data: escalation"}, "the training-data step missed alone moves more than training data"
    assert pr["feature releases on the calendar's planned weeks"] < 5.5 and fig["rigorous"]["points"][
        "feature releases"] < 5.5, "the calendar's routes no longer put feature releases on monitor"
    assert c2 - c1 == {"feature releases: monitor"}
    # each response figure the block calls lost sits outside its stated band, each one it calls made inside
    assert float(q1["on"]) >= 8 and float(q2["on"]) >= 8 and not inside(float(q1["on"]), "points_optimisation")
    assert q1["on"] == f2(pr["thirteen refits added up"]) == f2(lat["S2"]["points"]["optimisation noise"])
    assert f2(float(q2["on"])) == f2(pr["a whole replicate pair a refit"])
    assert inside(float(q1["td"]), "points_turnover") and inside(float(q2["td"]), "points_turnover")
    assert inside(float(q1["fr"]), "points_releases") and float(q2["fr"]) < 5.5
    assert inside(float(q1["cc3"][:-1]), "cc3") and not inside(float(q2["cc3"][:-1]), "cc3")
    for q in (q1, q2):
        assert not inside(float(q["own"][:-1]), "own_share") and not inside(float(q["frr"][:-1]), "fr_removed")
        assert "{:,}".format(b["score_rows"]) in q["rows"] and "{:,}".format(mapped) in q["map"]
        assert str(b["pairs"]) in q["pairs"]
    for sh in (sh1, sh2):
        assert all(not inside(float(v[:-1]), "share_" + key[n]) for n, v in sh.items()), sh
    assert bd["intercept8_min"] > 0 and b["past_lag_range"][0] > 0

    bo, bt, bc, bw = (band(B[k], d) for k, d in (("points_optimisation", 2), ("points_turnover", 2), ("cc3", 1),
                                                   ("own_share", 1)))
    p1 = (f"**Response 1** files optimisation noise in escalation at {q1['on']} points, where the answer is a "
          f"remediation plan at {f2(fig['cc2'])} (band {bo}), and it is right on the other four sources. It saw that "
          "a warm start carries noise from one refit into the next, but assumed the carried noise never fades: "
          f"\"{q1['perm']}\". Taking \"{q1['half']}\" and adding thirteen of them gives its {q1['on']}. It tested "
          f"the decay only on releases, regressing later panel changes on release effects (\"{q1['slopes']}\"), and "
          "never fitted how the score history's change grows with the gap between snapshots, which is where the "
          f"decay shows. The overstated noise runs downstream: merchants' own share comes out at {pc(q1['own'])} per cent "
          f"against {f1(fig['own_share'])} (band {bw}), every model-side share sits outside its band (label "
          f"revisions {pc(sh1['label revisions'])} against {f1(S['label revisions'])}), and tier changes with the plan "
          f"and escalation sources removed come to {pc(q1['frr'])} per cent against {f1(fig['fr_removed'])}. It made the other "
          f"two hard steps: training data at {q1['td']} points against {f2(fig['cc1'])}, by scaling the bootstrap "
          f"spread to each window's rows, and actual use of pinned views at {pc(q1['cc3'])} per cent (band {bc}), measured from "
          f"the three past platform changes, which keeps feature releases on a plan at {q1['fr']}.")
    p2 = (f"**Response 2** files optimisation noise in escalation at {q2['on']} points and feature releases on "
          f"monitor at {q2['fr']}, where the answer is a plan for both ({f2(fig['cc2'])} and "
          f"{f2(P['feature releases'])}). It read section 1.4 (\"{q2['s14']}\") as a carry that never fades and "
          f"counted a whole replicate pair for each refit, and it named the choice itself: \"{q2['carry']} ... "
          f"{q2['flag']}\". The check it ran on that choice was that the 2026 residual stayed flat across three "
          f"quarters ({flat2[0]}, {flat2[1]} and {flat2[2]}), which cannot tell a full carry from a decayed one, "
          "since both hold the model side steady from quarter to quarter. It then took the platform calendar's "
          f"rollout as the pinned views' actual use, \"{q2['cal']}\", which gives {pc(q2['cc3'])} per cent "
          f"against {f1(fig['cc3'])} and drops releases to monitor; its own words show the risk seen and set aside: "
          f"\"{q2['sched']} ... {q2['cond']}\". Downstream, merchants' own share is {pc(q2['own'])} per cent against "
          f"{f1(fig['own_share'])} and tier changes with the plan and escalation sources removed {pc(q2['frr'])} per cent against "
          f"{f1(fig['fr_removed'])}. It made the training-data step, {q2['td']} points inside the band {bt}, by a "
          "turnover estimator of its own.")
    p3 = ("**Why this is a fair stump.** Neither step turns on a planted defect or a buried sentence. Both responses "
          f"cleaned the record to the golden's own counts ({'{:,}'.format(b['score_rows'])} scored merchant-weeks, "
          f"{'{:,}'.format(mapped)} Tolka Pay identifiers mapped, {b['pairs']} instrument pairs), so the losses came "
          "after the cleaning. The definitions are the standard's own and the responses cite them: Response 2 quotes "
          "section 1.4 on the carried noise, and Response 1 reads the ask as actual use "
          f"(\"{q1['adopt']}\"). The evidence is the shape of whole files, not one line in one: the decay is in "
          "the gap curve of the ten panel files in every family, where a straight line through gaps 8 to 26 meets "
          f"gap 0 at {f1(bd['intercept8_book'])} points squared, book weighted, and above zero in every family "
          f"({f1(bd['intercept8_min'])} or more), which a carry that never fades cannot produce; actual use is in "
          f"the scheduler manifests set against the change calendar, where all {b['past_family_rollouts']} past "
          f"family rollouts first trained {b['past_lag_range'][0]} to {b['past_lag_range'][1]} weeks after the "
          "calendar marked them complete. Response 1 reached the pinned-views step unprompted from the same files, "
          "so it is reachable.")
    p4 = ("**Why it takes rigour.** Each step has an obvious repair that still files the wrong band. For the noise, "
          f"the replicate pairs read at face value give {f2(pr['the replicate pair read as the gap' + chr(39) + 's whole noise'])} "
          f"points (monitor), each refit's draw added in full gives {f2(pr['thirteen refits added up'])} or "
          f"{f2(pr['a whole replicate pair a refit'])} (escalation), and the gap curve fitted free of the replicate "
          f"pairs gives {f2(pr['unanchored fit'])} but implies replicate pairs of "
          f"{f2(pr['unanchored implied replicate'])} where {f2(b['replicate'])} is measured. The answer needs the "
          "curve fitted family by family on the settled warm weeks, its start tied to the measured replicate "
          f"variance, which gives a persistence of {f2(b['phi_fit'][0])} to {f2(b['phi_fit'][1])} and "
          f"{f2(fig['cc2'])} points. For pinned views, the calendar's planned weeks give {f1(b['cov_plan'])} per cent "
          f"and releases at {f2(pr['feature releases on the calendar' + chr(39) + 's planned weeks'])}, its completed "
          f"dates {f1(b['cov_declared'])} per cent and {f2(fig['rigorous']['points']['feature releases'])}, monitor "
          "either way; the answer needs the take-up lag modelled from the past rollouts, with its spread and the "
          f"reverted weeks, which gives {f1(fig['cc3'])} per cent and releases at {f2(P['feature releases'])}. The "
          "steps are independent: missing only the noise step moves optimisation noise to escalation "
          f"({f2(lat['S2']['points']['optimisation noise'])}) and nothing else, which is Response 1's call; taking "
          "the calendar for use as well drops feature releases to monitor, which is Response 2's call; and the "
          "training-data step, which both responses made, moves only training data when missed (to escalation at "
          f"{f2(lat['S1']['points']['training data'])}).")
    for p in (p1, p2, p3, p4):
        assert "\u2014" not in p and "\u2013" not in p
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
    a("The first sheet, 2027 placements, lists the five sources by band with their points, share and band, and the "
      "four measures beneath; then sheets for the instruments by family, training data, gap curves, pinned feature "
      "views, the weekly check, other routes and notes.")
    a("")
    a("1. Each model-side source in 2027: the points it alone moves a merchant's score between consecutive "
      "quarter-end snapshots (book weighted), its share of model-side movement and its band, with merchants' own "
      "share of all movement.")
    for i, s in enumerate(ORDER):
        n = NAMES[s]
        a("   %s. %s: %.2f points (band %s), %.1f per cent of model-side movement (band %s), %s." % (
            "abcde"[i], cap(n), P[n], band(B["points_" + s], 2), S[n], band(B["share_" + s], 1), fig["band_of"][n]))
    a("   f. Merchants' own change: %.1f per cent of all movement between quarter-end snapshots (band %s)." % (
        fig["own_share"], band(B["own_share"], 1)))
    a("2. Pinned feature views: %.1f per cent of 2027's weekly retrains are expected to actually run on them, family-weeks across the "
      "fourteen families (band %s)." % (fig["cc3"], band(B["cc3"], 1)))
    a("3. Tier changes between consecutive quarter-end snapshots in 2027, against the covenant's cap of 12 per cent:")
    a("   a. %.1f per cent of merchants expected (band %s)." % (fig["fr_sched"], band(B["fr_sched"], 1)))
    a("   b. %.1f per cent with label revisions, optimisation noise, feature releases and training data removed "
      "(band %s)." % (fig["fr_removed"], band(B["fr_removed"], 1)))
    a("")
    a("### garrane_stability_review_2027.pptx")
    a("Four slides: the call with each source's points, share and band; a bar chart of each source's points against "
      "dashed lines at 5.5 and 8; a column chart of each part's share of all movement; the tier changes against the "
      "cap.")
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
    a("6. Shares. Over the same settled weeks the record's mean-square change across thirteen refreshes is %.2f, "
      "book weighted; less the model-side sources as they stood, retunes at one every fourth week and feature "
      "releases at the mean count a thirteen-week gap of those weeks holds, "
      "it leaves merchants' own change, carried into 2027 beside the five sources' 2027 movement, at %.1f per cent "
      "of all movement, section 5.2's quantity estimated from every thirteen-week gap of the settled weeks; the three "
      "snapshot pairs closed in 2026 taken alone give %.1f. As a share of the record's own movement it would be %.1f, "
      "which is not the share section 5.2 reports. Each source's share of model-side movement is in answer 1. Reading "
      "each instrument as it stands puts merchants' own change at %.1f per cent, with %d families' instruments "
      "adding to more than the record's change and their own change floored at zero, and training data at %.1f "
      "per cent of model-side movement; across the book the thirteen-week total still closes (%.2f of the "
      "record's %.2f), so the closing total does not catch it. Taking every thirteen-week gap from July 2024 puts "
      "merchants' own share at %.1f, but before each family's settled weeks the manifests show cold retrains on a "
      "26-week window and the calendar's three rollouts, so the record's change there runs %.2f to %.2f times the "
      "settled weeks' and is not the 2026 sources' movement." % (
          b["d13"], fig["own_share"], fig["extra"]["merchants' own change from the 2026 snapshot pairs only"]["own_share"],
          pr["merchants' own change as a share of the record's own movement"], rf["own_share"], rf["families_floored"], rf["share"]["training data"], rf["model_side_2026"], b["d13"],
          fig["ruled"]["merchants' own change over every thirteen-week gap from July 2024"]["own_share"],
          fig["pre_settled"]["ratio_range"][0], fig["pre_settled"]["ratio_range"][1]))
    a("7. The check. Each route's own model of how a source's variance grows with the gap is asked for the "
      "mean-square change between consecutive weekly refreshes over the same settled weeks, which the record holds "
      "at %.2f, book weighted: this assessment gives %.2f; both the bootstrap and the replicate pairs read at face "
      "value give %.2f; the bootstrap spread at any gap %.2f; the replicate pairs at any gap %.2f." % (
          fa["record"], fa["golden"], fa["rivals"]["both at face value"], fa["rivals"]["bootstrap spread at any gap"],
          fa["rivals"]["replicate variance at any gap"]))
    a("8. Tier changes. The 2026 snapshot pairs ran at %.1f per cent on the monitoring panel. Each family's rate "
      "scaled by the root of its 2027 movement against 2026's gives %.1f per cent for 2027, and %.1f per cent with "
      "the four sources in a plan or escalation removed; the reflex route's placements give %.1f and %.1f." % (
          fig["fr26"], fig["fr_sched"], fig["fr_removed"], rf["fr_sched"], rf["fr_removed"]))
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
