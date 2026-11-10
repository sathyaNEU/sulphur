"""task15: submission.md, the four answer blocks, written from the figures object (generator/figures.json). No figure
is typed here."""


def and_list(xs):
    xs = [str(x) for x in xs]
    if not xs:
        return "none"
    if len(xs) == 1:
        return xs[0]
    return ", ".join(xs[:-1]) + " and " + xs[-1]


def nums(xs, fmt="%.1f"):
    return and_list([fmt % x for x in xs])


def pcts(xs):
    return and_list(["%d%%" % round(x) for x in xs])


def rng(b):
    return "%.1f to %.1f" % (b[0], b[1])


def irng(b):
    return "%d to %d" % (round(b[0]), round(b[1]))


def pick(d, word):
    return [k for k in d if word in k][0]


WORDS = {1: "one", 2: "two", 3: "three"}


def write(F, path):
    L, std, B, ev, T = F["lines"], F["standard"], F["bands"], F["evidence"], F["tolerances"]
    yr, fn, bm = F["years"], F["files"], F["bridge_means"]
    picks, nxt, idx = F["nominate"], F["first_left_out"], F["index_would_nominate"]
    h, cnt, pl = F["hurried"], F["counts"], F["proportional_loss"]
    n = F["completed_nominations"]
    own, wat, lod = F["overstated_at_own_sites_points"], F["benchmark_water_response_points"], F["lodging_points"]
    left = F["left_over_points"]
    ro, riv = F["ruled_out"], F["rivals"]
    k_plain = pick(riv, "no pooling")
    ry = lambda w: L[w]["expected_ry"]
    order = sorted(L, key=lambda k: F["rank"][k])
    npk = len(picks)
    idx_only = [w for w in idx if w not in picks]
    o = []
    add = o.append

    add("## Tags")
    add("")
    add("**Domain:** Machine Learning Research, General Statistics & Data Science (multiple testing & selective "
        "inference: lines picked on noisy trial means across a staged programme, and what they return elsewhere).")
    add("**Analytical objective:** Comparative Analysis & Explanation.")
    add("")

    add("## Final Recommendation")
    add("")
    add("**Nominate %s for %d sowing:** they are the %s Stage 3 lines to expect most from in the series, at %s over "
        "two seasons against %.1f for the next line (%s). The index would put up %s (%s), but at the series' trials "
        "%s expected to return %s with %s of %s plots lodged, the way the %d completed nominations came to return "
        "%.1f against %.1f quoted."
        % (and_list(picks), yr["decision_sow"], WORDS[npk], nums([ry(w) for w in picks]), ry(nxt), nxt,
           and_list(idx), nums([L[w]["index"] for w in idx]),
           "%s %s" % (and_list(idx_only), "are" if len(idx_only) > 1 else "is"),
           nums([ry(w) for w in idx_only]), pcts([L[w]["lodging_pct"] for w in idx_only]),
           "their" if len(idx_only) > 1 else "its", n, F["realised_mean"], F["quoted_mean"]))
    add("")

    add("## Supplementary Questions")
    add("")
    add("### %s" % fn["book"])
    add("")
    add("1. Sheet \"Bridge\", the %d nominations sown from %d to %d with both series seasons published (the three "
        "sown in %d have one season): mean index quoted %.1f, mean relative yield returned %.1f, a gap of %.1f points. "
        "The returned figure is the series' own relative yield, each line's mean yield over its series trials as a "
        "percentage of Byaduk's mean over the same trials (protocol section 7); the mean of the trial-by-trial "
        "percentages (%.1f, a gap of %.1f) is not the series' figure and is not accepted."
        % (n, yr["first_sow"], yr["last_completed_sow"], yr["pending_sow"], F["quoted_mean"], F["realised_mean"],
           F["shortfall_points"], ev["returned_mean_of_site_percentages"], ev["gap_on_mean_of_site_percentages"]))
    add("2. Sheet \"Bridge\", the gap under the four heads of the option deed's review clause (schedule 2, clause "
        "4.2), each a mean over the %d lines and rounded on its own: the index %.1f points (accept %s); the move to "
        "the Series %.1f (accept %s); lodging %.1f (accept %s); the remainder %.1f (accept %s)."
        % (n, own, rng(B["own"]), wat, rng(B["water"]), lod, rng(B["lodging"]), left, rng(B["left"])))
    add("3. Sheet \"Stage 3 lines\", one row for each of the %d Stage 3 lines of %d not yet nominated, highest "
        "expected relative yield first, with its Stage 3 seasons, its index (over all its Stage 3 trials at the "
        "three index sites, both seasons where it has two), the relative yield to expect over two series seasons like "
        "those the series has had, the 80%% range of what those two seasons return and its expected lodging in the "
        "series. Sound fits differ on a single line, so accept an expected relative yield within %.1f points, within "
        "%.1f for a line expected to lodge %d%% or more and within %.1f for one expected to lodge %d%% or more (the "
        "more of the plot lodges, the more the size of the lodging loss, which sound fits read differently, moves "
        "the line), a range end within %.1f points more than that, and an expected lodging within %d points of the "
        "plot; a wider allowance is given beside a line where the fits run further apart. The rows, as line: expected "
        "relative yield (range), expected lodging:"
        % (F["candidates"], yr["last_season"], T["ry_points"], T["ry_points_lodged"], T["lodged_at_pct"],
           T["ry_points_heavy"], T["heavy_at_pct"], T["range_extra_points"], T["lodging_points"]))
    for w in order:
        d = L[w]
        extra = []
        if w in T["wider_ry"]:
            extra.append("relative yield within %.1f" % T["wider_ry"][w])
        if w in T["wider_lodging"]:
            extra.append("lodging within %d" % round(T["wider_lodging"][w]))
        add("   - %s: %.1f (%.1f to %.1f), %d%%%s" % (w, d["expected_ry"], d["low"], d["high"], d["lodging_pct"],
                                                      (" (%s)" % ", ".join(extra)) if extra else ""))
    add("4. Sheet \"Nominations\": the %s lines with the highest expected relative yield are %s; the next, %s, is %.1f "
        "points behind the %s. Accept the same %s lines."
        % (WORDS[npk], and_list(picks), nxt, F["cut_points"], "second" if npk == 2 else "last of them", WORDS[npk]))
    add("")
    add("### %s" % fn["chart"])
    add("")
    add("5. A bridge chart of the gap: the mean index quoted (%.1f) stepping through the index head (%.1f), the move "
        "to the Series (%.1f) and lodging (%.1f) to the %.1f expected in the series, then the remainder (%.1f) to "
        "the %.1f returned, each step carrying its value, with the deed's %.1f standard drawn across."
        % (F["quoted_mean"], own, wat, lod, F["expected_in_series_mean"], left, F["realised_mean"], std))
    add("")
    add("### %s" % fn["note"])
    add("")
    add("6. A two-page note that opens with the call (%s, not the index's %s), gives the lines nominated, the "
        "first line left out and the index's other choice their index, expected relative yield, range and lodging in "
        "one table, then the bridge in a paragraph with the chart." % (and_list(picks), and_list(idx)))
    add("")

    add("## Critical Components")
    add("")
    add("1. At the trials their index was taken from, the %d nominations should have been expected to give a "
        "relative yield of %.1f, not the %.1f quoted: the index head is **%.1f points** (accept %s)."
        % (n, F["worth_at_own_sites_mean"], F["quoted_mean"], own, rng(B["own"])))
    add("2. Before lodging the lines stand %.2f t/ha over Byaduk at their index trials (Byaduk %.2f t/ha, %d mm of "
        "season water) and %.2f t/ha at their series trials (Byaduk %.2f t/ha, %d mm): the move to the Series is "
        "**%.1f points** (accept %s)."
        % (bm["advantage_at_index_trials_t_ha"], bm["byaduk_at_index_trials_t_ha"], bm["water_at_index_trials_mm"],
           bm["advantage_at_series_trials_t_ha"], bm["byaduk_at_series_trials_t_ha"], bm["water_at_series_trials_mm"],
           wat, rng(B["water"])))
    add("3. A tenth of a plot lodged costs %.3f t/ha inside a line and trial, and the lines lodged %.1f points more "
        "than Byaduk at their index trials and %.1f points more at their series trials: the lodging head is **%.1f "
        "points** (accept %s)."
        % (ev["loss_per_tenth_within"], bm["lodging_over_byaduk_at_index_trials_pct"],
           bm["lodging_over_byaduk_at_series_trials_pct"], lod, rng(B["lodging"])))
    add("4. The three standards lodge %.1f%% of the plot at the series' trials against %.1f%% at the index trials; "
        "carried to that pressure %s %s expected to lodge %s there (accept %s) and the index's %s %s (accept %s)."
        % (ev["standards_lodging_pct_series"], ev["standards_lodging_pct_index_trials"], and_list(picks),
           "are" if npk > 1 else "is", and_list(["**%d%%**" % L[w]["lodging_pct"] for w in picks]),
           and_list([irng(B["lodging_pct"][w]) for w in picks]), and_list(idx_only),
           and_list(["**%d%%**" % L[w]["lodging_pct"] for w in idx_only]),
           and_list([irng(B["lodging_pct"][w]) for w in idx_only])))
    add("")

    add("## Step-by-Step")
    add("")
    add("1. Conformed the plot record from %s (a header at every trial, yields in kilograms a hectare) and %s (the "
        "later weighing of the %d plots weighed twice, %s section 5), with lines from %s carried to one code through "
        "%s: %s plots in %d trials, %d of them abandoned with a lodging figure and no weight."
        % (fn["old"], fn["new"], cnt["reweighed"], fn["handbook"], fn["entries"], fn["register"],
           format(ev["plots"], ","), ev["trials"], ev["abandoned"]))
    add("2. Rebuilt the index quoted in %s as the handbook's section 6 defines it and the returned relative yield "
        "from %s as %s section 7 defines it: %d of the %d nominations have both seasons, quoted %.1f, returned %.1f, "
        "a gap of %.1f; %d of them met the deed's %.1f standard. Reading the whole gap as luck in the picking keeps "
        "the index's order and nominates %s."
        % (fn["nominations"], fn["results"], fn["protocol"], n, cnt["nominations"], F["quoted_mean"],
           F["realised_mean"], F["shortfall_points"], F["past_meeting_standard"], std, and_list(idx)))
    lv = ro[pick(ro, "yield level")]
    add("3. Built each trial's season water from %s (April to October, as %s gives it for the series) plus %s: "
        "Kerang yields %.2f t/ha where the other sites' curve gives %.2f on its rain alone and %.2f with its "
        "waterings. Byaduk's advantage over the lines rises %.2f t/ha per 100 mm across the %d trials (t %.1f). At "
        "our own trials season water and the trial's yield level (the mean yield of the trial's entries on neither "
        "side of the comparison) move together (correlation %.2f) and neither stands out with both entered (t %.1f "
        "and %.1f); the series' trials separate them: Byaduk's advantage over our nominated lines there goes with "
        "season water (t %.1f) while the trial's yield level, entered beside it, takes the opposite sign (t %.1f), "
        "as it does over Wando and Carapook (t %.1f and %.1f). A response fitted on yield level leaves %.1f points of the gap on the "
        "%d nominations unexplained (t %.1f); fitted on season water it leaves %.1f (t %.1f)."
        % (fn["rain"], fn["seasons"], fn["irrigation"], ev["kerang_mean_yield"], ev["kerang_curve_at_rain_alone"],
           ev["kerang_curve_with_waterings"], ev["adv_per_100mm"], ev["trials"], ev["adv_water_t"],
           ev["water_level_corr"], ev["joint_water_t"], ev["joint_level_t"], ev["series_lines_joint_water_t"],
           ev["series_lines_joint_level_t"], ev["series_joint_water_t"], ev["series_joint_level_t"], lv["left"], n,
           lv["left_t"], left, F["left_over_t"]))
    add("4. Priced lodging from the plots: inside a line and trial a tenth of a plot lodged costs %.3f t/ha, where a "
        "plain comparison across plots has lodged plots yielding %.3f more (wet trials both lodge and yield). "
        "Abandoned plots average %.1f%% lodged against %.1f%% for harvested ones, so a line's lodging is taken over "
        "every plot sown; the three standards lodge %.1f%% at the index trials and %.1f%% in the series. Read as a "
        "share of the plot's yield the same loss is %.1f%% a tenth and gives a lodging head of %.1f with a move of "
        "%.1f, inside the ranges above."
        % (ev["loss_per_tenth_within"], ev["gain_per_tenth_across_plots"], ev["lodging_pct_abandoned"],
           ev["lodging_pct_harvested"], ev["standards_lodging_pct_index_trials"], ev["standards_lodging_pct_series"],
           pl["share_per_tenth_pct"], pl["lodging"], pl["water"]))
    add("5. Fitted, on Banyena's own plot record alone (the series' results stay aside as what the lines returned), "
        "every line's yield over Byaduk's in the same trial, lodging loss added back, as a level and a "
        "response to season water, lines drawn within their Stage 1 intake and their cross so that the %s lines "
        "that entered Stage 1 set how far a high mean is believed (the %d advanced from Stage 1 stood %.2f t/ha "
        "over the check varieties there and %.2f a season later). Reading each nomination's fitted line at its "
        "index trials and at its series trials, with the lodging recorded at each, gives the deed's heads: the "
        "index %.1f, the move to the Series %.1f, lodging %.1f, the remainder %.1f. Each line fitted on its own "
        "trials alone, with no pooling, gives %.1f, %.1f and %.1f. One response for all lines gives %.1f for the "
        "index head and %.1f for the move; the lines do differ: fitted one at a time, the responses of the %d lines "
        "with ten or more trials have %.1f times the variance their own standard errors allow."
        % (format(ev["stage1_lines"], ","), ev["advanced_lines"], ev["advanced_stage1_over_checks"],
           ev["advanced_stage2_over_checks"], own, wat, lod, left, riv[k_plain]["own"], riv[k_plain]["water"],
           riv[k_plain]["lodging"], h["own"], h["water"], ev["response_lines"], ev["response_spread_ratio"]))
    hp = h["nominate"]
    add("6. Carried each Stage 3 line to the series: its lodging as a multiple of the three standards' lodging in "
        "the same trial, applied to the standards' lodging at each of the %d trials the series has harvested, and "
        "its fitted line read at those trials' season water, less the lodging loss. %s at %s; the next line, %s, is "
        "at %.1f, %.1f behind. They should lodge %s there; the index's %s should lodge %s. The one-response route "
        "puts every line between %.1f and %.1f, has %s at %s and nominates %s, expected here at %s; it reads lodging "
        "off each line's own trials and puts every line between %d%% and %d%%."
        % (ev["series_trials"], ("%s stand" % and_list(picks)) if npk > 1 else ("%s stands" % picks[0]),
           nums([ry(w) for w in picks]), nxt, ry(nxt), F["cut_points"], pcts([L[w]["lodging_pct"] for w in picks]),
           and_list(idx_only), pcts([L[w]["lodging_pct"] for w in idx_only]), h["its_ry_low"], h["its_ry_high"],
           and_list(picks), nums(h["its_ry_of_the_nominees"]), and_list(hp), nums(h["golden_ry_of_its_picks"]),
           h["its_lodging_low"], h["its_lodging_high"]))
    d0 = L[picks[0]]
    eo = F["estimate_only"]
    add("7. Drew what two series seasons would return: two seasons taken from the series' own history with their "
        "trials, season water and lodging, each line's level, response and lodging drawn from what the record leaves "
        "unsure, and Byaduk's own season swing shared by every entry. %s runs from %.1f to %.1f (from the spread of "
        "its estimate alone, %.1f to %.1f). The one-response route takes its ranges from the scatter of its past "
        "misses, plus or minus %.1f."
        % (picks[0], d0["low"], d0["high"], eo["lo"][0], eo["hi"][0], h["interval_half_width"]))
    add("")
    cr = F["closest_rival"]
    add("No other answer survives. Every other defensible way of doing a step (each line fitted on its own trials "
        "alone, lines taken as unrelated to their sisters, one prior for all cohorts, blocks ignored, a slope along "
        "the range, lodging fitted on the lushest trials or on every trial or left unshrunk, lodging set against "
        "Byaduk's alone, the series' last six seasons only, the lodging head on fitted lodging or as a share of "
        "yield) names the same %s lines, the %s never less than %.1f points clear of the next, and lands inside "
        "every range above. Leaving Kerang's waterings out of its season water is ruled out by its yield (%.2f t/ha "
        "against %.2f on rain alone), a response to yield level by the series' own trials (entered together, season "
        "water carries Byaduk's gain over our lines at t %.1f and yield level takes the opposite sign, t %.1f) and by "
        "the nominations already "
        "made (it leaves %.1f points of their gap unexplained, t %.1f), and one response for all lines by the lines "
        "themselves (their fitted responses have %.1f times the variance their standard errors allow). The index "
        "keeps a weak-strawed line the series will lodge; as quoted it was out by %.1f points root mean square on the "
        "nominations already made."
        % (WORDS[npk], "second" if npk == 2 else "last", cr["cut"], ev["kerang_mean_yield"],
           ev["kerang_curve_at_rain_alone"], ev["series_lines_joint_water_t"], ev["series_lines_joint_level_t"],
           lv["left"], lv["left_t"], ev["response_spread_ratio"], F["index_rmse_points"]))
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(o) + "\n")
