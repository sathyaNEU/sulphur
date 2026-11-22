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
    a("## Final Recommendation")
    a("")
    a("For 2027, escalate label revisions (%.2f points between consecutive quarter-end snapshots) and put optimisation "
      "noise (%.2f), feature releases (%.2f) and training data (%.2f) on remediation plans; keep retunes on monitor "
      "(%.2f). This rejects reading each instrument as it stands, which escalates training data at %.2f points and "
      "leaves optimisation noise (%.2f) and feature releases (%.2f) on monitor." % (
          P["label revisions"], P["optimisation noise"], P["feature releases"], P["training data"], P["retunes"],
          rf["points"]["training data"], rf["points"]["optimisation noise"], rf["points"]["feature releases"]))
    a("")
    a("## Supplementary Questions")
    a("")
    a("1. Each model-side source in 2027: the points it alone moves a merchant's score between consecutive "
      "quarter-end snapshots (book weighted), its share of model-side movement and its band.")
    for s in ORDER:
        n = NAMES[s]
        a("   - %s: %.2f points (band %s), %.1f per cent of model-side movement (band %s), %s." % (
            cap(n), P[n], band(B["points_" + s], 2), S[n], band(B["share_" + s], 1),
            fig["band_of"][n]))
    a("   - Merchants' own change is %.1f per cent of all movement between quarter-end snapshots (band %s)." % (
        fig["own_share"], band(B["own_share"], 1)))
    a("2. Pinned feature views: %.1f per cent of 2027's weekly retrains will run on them, family-weeks across the "
      "fourteen families (band %s)." % (fig["cc3"], band(B["cc3"], 1)))
    a("3. Tier changes between consecutive quarter-end snapshots in 2027: %.1f per cent of merchants expected "
      "(band %s), and %.1f per cent with label revisions, optimisation noise, feature releases and training data "
      "removed (band %s), against the covenant's cap of 12 per cent." % (
          fig["fr_sched"], band(B["fr_sched"], 1), fig["fr_removed"], band(B["fr_removed"], 1)))
    a("4. Files: a workbook whose first sheet, 2027 placements, lists each source's points, share and band with the "
      "four measures beneath, followed by sheets for the instruments by family, training data, gap curves, pinned "
      "feature views, the weekly check and other routes; and a four-slide deck whose first slide states the call, "
      "then a bar chart of each source's points against the 5.5 and 8 point lines, a column chart of each part's "
      "share of all movement, and the tier-change table.")
    a("")
    a("## Critical Components")
    a("")
    a("1. Training data alone moves a merchant's score %.2f points between consecutive quarter-end snapshots in 2027 "
      "(band %s)." % (fig["cc1"], band(B["cc1"], 2)))
    a("2. Optimisation noise alone moves a merchant's score %.2f points between consecutive quarter-end snapshots in "
      "2027 (band %s)." % (fig["cc2"], band(B["cc2"], 2)))
    a("3. %.1f per cent of 2027's weekly retrains will run on pinned feature views (band %s)." % (
        fig["cc3"], band(B["cc3"], 1)))
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
      "rows each 2027 snapshot pair turns over. Training data alone is %.2f points, a remediation plan." % (
          b["bootstrap_raw"], b["bootstrap_net"], rf["points"]["training data"], b["long_window_families"],
          fig["cc1"]))
    a("4. Optimisation noise. The replicate pairs differ by %.2f points squared, book weighted, which is %.2f points "
      "and monitor if a refit's fresh noise is all two snapshot models differ by. But each weekly model starts from "
      "the previous week's weights, so the noise persists and builds over the thirteen refits between snapshots. "
      "The score history's mean-square change by gap, over each family's settled warm weeks, bends towards a "
      "ceiling; a saturating term tied to the replicate pairs gives a persistence of %.2f to %.2f by family and "
      "%.2f points, a remediation plan. Fitted free of the replicate pairs it gives %.2f points but implies "
      "replicate pairs of %.2f where %.2f is measured; a straight line through gaps 8 to 26 starts at %.2f while "
      "the curve is still bending; thirteen refits each adding a whole replicate pair's variance gives %.2f." % (
          b["replicate"], rf["points"]["optimisation noise"], b["phi_fit"][0], b["phi_fit"][1], fig["cc2"],
          pr["unanchored fit"], pr["unanchored implied replicate"], b["replicate"], pr["line through gaps 8 to 26"],
          pr["a whole replicate pair a refit"]))
    a("5. Pinned feature views and feature releases. On the calendar's planned weeks %.1f per cent of 2027's "
      "retrains run on pinned views, and %.1f per cent on its completed dates. The calendar marks a change complete "
      "when the image is released; the manifests show when each family first trained on the three past changes: "
      "%d family rollouts, first use %d to %d weeks after completion (median %.0f), a median of %.1f weeks with no "
      "custom training components and %.1f with %d, and %.1f per cent of the following 26 weeks reverted. A lag "
      "model on custom components carries this to the pinned views: %.1f per cent of 2027's retrains. Leaving each "
      "past rollout out in turn, the model predicts its first 39 weeks on at %.1f, %.1f and %.1f per cent against "
      "%.1f, %.1f and %.1f recorded. A roadmap release moves a family's scores only in the weeks it is not on "
      "pinned views: with the release shadows' variance and the roadmap's %d releases, feature releases alone are "
      "%.2f points, a remediation plan (%.2f on the calendar's dates, monitor; %.2f if 2026's %d releases are "
      "carried instead of the roadmap)." % (
          b["cov_plan"], b["cov_declared"], b["past_family_rollouts"], b["past_lag_range"][0],
          b["past_lag_range"][1], b["past_lag_median"], b["lag_median_custom0"], b["lag_median_custom_max"],
          b["custom_max"], 100 * b["revert_share"], fig["cc3"], 100 * fig["loo"]["runtime"]["model"],
          100 * fig["loo"]["warm"]["model"], 100 * fig["loo"]["amp"]["model"], 100 * fig["loo"]["runtime"]["record"],
          100 * fig["loo"]["warm"]["record"], 100 * fig["loo"]["amp"]["record"], b["releases_2027"],
          P["feature releases"], rf["points"]["feature releases"], pr["2026's release level carried"],
          b["releases_2026"]))
    a("6. Shares. The record's mean-square change over thirteen refreshes in the settled weeks is %.2f, book "
      "weighted; less the model-side sources as they stood in 2026 it leaves merchants' own change at %.1f per cent "
      "of all movement (%.1f on the 2026 snapshot pairs alone). Each source's share of model-side movement is in "
      "answer 1. Reading each instrument as it stands puts merchants' own change at %.1f per cent and training data "
      "at %.1f per cent of model-side movement, and the thirteen-week total still closes, so the closing total "
      "checks nothing. Taking every thirteen-week gap from July 2024 puts merchants' own share at %.1f, but before "
      "each family's settled weeks the manifests show cold retrains on a 26-week window and the calendar's three "
      "rollouts, so the record's change there runs %.2f to %.2f times the settled weeks' and is not the 2026 "
      "sources' movement." % (
          b["d13"], fig["own_share"], fig["extra"]["merchants' own change from the 2026 snapshot pairs only"]["own_share"],
          rf["own_share"], rf["share"]["training data"],
          fig["ruled"]["merchants' own change over every thirteen-week gap from July 2024"]["own_share"],
          fig["pre_settled"]["ratio_range"][0], fig["pre_settled"]["ratio_range"][1]))
    a("7. The check. Each route's own model of how a source's variance grows with the gap is asked for the weekly "
      "score-change variance of the settled weeks, which the record holds at %.2f: this assessment gives %.2f; both "
      "the bootstrap and the replicate pairs read at face value give %.2f; the bootstrap spread at any gap %.2f; the "
      "replicate pairs at any gap %.2f." % (
          fa["record"], fa["golden"], fa["rivals"]["both at face value"], fa["rivals"]["bootstrap spread at any gap"],
          fa["rivals"]["replicate variance at any gap"]))
    a("8. Tier changes. The 2026 snapshot pairs ran at %.1f per cent on the monitoring panel. Each family's rate "
      "scaled by the root of its 2027 movement against 2026's gives %.1f per cent for 2027, and %.1f per cent with "
      "the four sources in a plan or escalation removed; the reflex route's placements give %.1f and %.1f." % (
          fig["fr26"], fig["fr_sched"], fig["fr_removed"], rf["fr_sched"], rf["fr_removed"]))
    a("9. Why no other conclusion survives. %d variants (the gap fit over 20, 26 or 30 gaps, pooled or per family, "
      "events taken out, the take-up model linear, by group, by family or pooled, the planned book, the latest "
      "bootstrap week, four tier mappings, and the panel's weights in place of the book's) file the same five bands. "
      "Losing any one judgment moves a source across a line: the bootstrap pairs as the movement put training data "
      "in escalation (%.2f); the replicate pairs as the movement put optimisation noise on monitor (%.2f); the "
      "calendar's dates put feature releases on monitor (%.2f)." % (
          fig["variants"], lat["S1"]["points"]["training data"], lat["S2"]["points"]["optimisation noise"],
          lat["S3"]["points"]["feature releases"]))
    a("")
    open(path, "w").write("\n".join(L))
