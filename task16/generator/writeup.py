"""submission.md, the four answer blocks, emitted from the figures (never typed)."""
import deliver as DL

DOMAIN = ("Machine Learning Research, General Statistics & Data Science, scaling laws (performance trends across model, "
          "data, and compute size).")
OBJECTIVE = "Forecasting & Predictive Modeling."


def n(x):
    return "{:,}".format(int(x))


def l2(x):
    return "%.2f" % x


def l3(x):
    return "%.3f" % x


def l4(x):
    return "%.4f" % x


def rate(x):
    s = "%.5f" % x
    return s.rstrip("0") if "." in s else s


def words(k):
    """A small count as a word."""
    return {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}.get(int(k), n(k))


def band(b, f=l3):
    """A band as it reads after the word between."""
    return "%s and %s" % (f(b[0]), f(b[1]))


def text(F):
    h = F["hurried"]; ex = F["expected"]; c = F["constants"]; bd = F["bands"]; pl = F["pooled"]; bo = F["bounds"]
    opt = {o["option"]: o for o in c["shortlist"]}
    call = F["call"]; B = opt[call]
    trial = c["trial"]
    lines = []
    A = lines.append
    A("## Tags")
    A("")
    A("**Domain:** %s" % DOMAIN)
    A("**Analytical objective:** %s" % OBJECTIVE)
    A("")
    A("## Final Recommendation")
    A("")
    A("**Name option %s**, the %s-wide model on the %s expert and %s contractor labels at learning rate %s: its expected "
      "benchmark log loss for one run is **%s**, with a four-in-five range of %s to %s, the lowest of the four under "
      "every sound reading of the pilot. Not option C: the logged development loss and a single scaling curve fitted "
      "through every pilot run both put C first (at %s to %s on the curve, depending on its form), but past the "
      "%s-example expert pool each doubling of examples returns about half of the one before, and C comes out at %s "
      "(no lower than %s even with the last doubling's gain carried on undiminished), because the million "
      "map-transfer labels cost more than the extra examples return."
      % (call, n(B["width"]), n(B["expert"]), n(B["contractor"]), rate(B["lr"]), l3(ex[call]), l3(F["range_low"]),
         l3(F["range_high"]), l2(pl["C"][0]), l2(pl["C"][1]), n(c["expert_pool"]), l3(ex["C"]), l3(bo["C"][0])))
    A("")
    A("## Supplementary Questions")
    A("")
    A("### %s" % DL.WORKBOOK)
    A("")
    A("1. A ranking sheet with one row per shortlisted configuration (hidden width, labelled points by route, learning "
      "rate, expected benchmark log loss for one run), sorted by expected loss: B %s (sound methods land between %s), "
      "A %s (between %s), C %s (between %s), D %s (between %s). B is first; the other three sit within %s of each "
      "other and their order is not a finding."
      % (l3(ex["B"]), band(bd["expected"]["B"]), l3(ex["A"]), band(bd["expected"]["A"]), l3(ex["C"]), band(bd["expected"]["C"]),
         l3(ex["D"]), band(bd["expected"]["D"]), l3(F["others_spread"])))
    A("2. The four-in-five range for the named configuration, on its row: %s to %s for one run of B, a half-width of "
      "%s. It combines the run-to-run spread (%s), the forecast's error on the pilot's largest configurations when "
      "built without them (%s) and the error of carrying expert-item loss to the benchmark (%s). A sound range is "
      "drawn round B's expected loss with a half-width between %s (what the first and the last of those give "
      "together) and %s; run-to-run spread alone, %s to %s, is too narrow."
      % (l3(F["range_low"]), l3(F["range_high"]), l3(F["range_half"]), l4(F["range_parts"]["run"]),
         l4(F["range_parts"]["forecast"]), l4(F["range_parts"]["yardstick"]), l3(bd["range_half"][0]), l3(bd["range_half"][1]),
         l3(h["seed_range"][0]), l3(h["seed_range"][1])))
    A("3. Underneath, the benchmark loss matching the width-%s trial on %s expert plus %s map-transfer labels: %s "
      "(between %s)." % (n(128), n(trial[0]), n(trial[2]), l3(F["trial_map384"]), band(bd["trial"])))
    A("4. Each tenth of a training set moved from expert labels adds %s to the benchmark loss with contractor labels "
      "(between %s) and %s with map-transfer labels (between %s)."
      % (l4(F["cost_ctr"]), band(bd["costs_contractor"], l4), l4(F["cost_map"]), band(bd["costs_map"], l4)))
    A("5. %s expert labels would give a benchmark loss of %s at width %s and learning rate %s (between %s). The "
      "workbook also carries the working: the level by training-set size, the vendor-label trials against expert "
      "labels at the same size, the check on the largest runs held back, the best learning rate by width, what other "
      "routes give, and every finished run with its scores."
      % (n(c["level_at"]), l3(F["level_512k"]), n(128), rate(c["level_lr"]), band(bd["level"])))
    A("")
    A("### %s" % DL.NOTE)
    A("")
    A("6. A short note, under two pages, that opens with the call (name B, %s, four in five between %s and %s), says "
      "why C is left out, and carries one chart of the benchmark loss against training-set size with the size "
      "ladder's straight line and the forecast curve." % (l3(ex[call]), l3(F["range_low"]), l3(F["range_high"])))
    A("")
    A("## Critical Components")
    A("")
    A("1. At the same examples, width and learning rate, each tenth of a training set moved from expert labels adds "
      "**%s** to the benchmark loss with contractor labels (between %s) and **%s** with map-transfer labels "
      "(between %s)."
      % (l4(F["cost_ctr"]), band(bd["costs_contractor"], l4), l4(F["cost_map"]), band(bd["costs_map"], l4)))
    A("2. %s expert labels would give **%s** at width %s and learning rate %s (between %s): past the %s-example expert "
      "pool a doubling returns about %s and then %s, not the %s of the size ladder."
      % (n(c["level_at"]), l3(F["level_512k"]), n(128), rate(c["level_lr"]), band(bd["level"]), n(c["expert_pool"]),
         l3(F["gain_first"]), l3(F["gain_second"]), l3(F["gain_ladder"])))
    A("3. Option C, on all %s labels, comes out at **%s** (between %s: the low end is the last doubling's gain carried "
      "on undiminished, the high end no further gain), not the %s to %s of a single curve through every run; B, at "
      "**%s** (between %s), is the lower of the two under every one of those readings."
      % (n(opt["C"]["total"]), l3(ex["C"]), band(bd["expected"]["C"]), l2(pl["C"][0]), l2(pl["C"][1]), l3(ex["B"]),
         band(bd["expected"]["B"])))
    A("")
    A("## Step-by-Step")
    A("")
    A("1. From `tracking_runs_export_2026-11-04.csv` and `tracking_metrics_export_2026-11-04.csv` (the two logger "
      "vocabularies read as one, a resumed job's repeated steps taken from the later row), %s of the %s run records "
      "finished their schedule; joining `nssmp_benchmark_submissions_mml.csv` to `checkpoint_store_listing_2026-11-04.csv` "
      "on the file digest, %s of the %s benchmark rows score a final checkpoint."
      % (n(F["runs_finished"]), n(F["run_records"]), n(F["bench_final"]), n(F["bench_rows"])))
    A("2. The shallow read: the logged development loss, carried to the benchmark by a line on the scored runs and "
      "extended along the size ladder's straight line, puts C first at about %s, below the benchmark score of every "
      "pilot run (the lowest is %s). It does not stand: joining `dev_split_items.csv` to `label_shard_register.csv` "
      "shows only %s of the %s development items carry expert labels, so a model trained on a vendor's labels is "
      "partly scored against that vendor's own labels."
      % (l2(F["quick_C"]), l3(F["min_bench"]), n(F["dev_expert_items"]), n(F["dev_items"])))
    A("3. From `dev_item_loss_final_checkpoints.csv`, each final checkpoint's mean loss on the expert-labelled items "
      "tracks its benchmark score on the scored final checkpoints (benchmark = %s + %s x expert-item loss, residual "
      "%s), so the width-%s trial on %s expert plus %s map-transfer labels corresponds to %s on the benchmark; the "
      "logged loss carried the same way says %s."
      % (l4(F["cal_intercept"]), l3(F["cal_slope"]), l4(F["cal_sd"]), n(128), n(trial[0]), n(trial[2]),
         l3(F["trial_map384"]), l3(h["quick_trial"])))
    A("4. The size ladder ran at tabled learning rates, about %s worse at width %s than the rate the trials used, so no "
      "trial is read against the ladder as it ran. Every total the trials ran is given a level of its own, and each "
      "route's cost is read from the contrasts between mixes at one total, width and rate, the expert-label run at "
      "the trials' rate standing at %s examples as a mix with no vendor labels: each tenth of a training set moved to "
      "contractor labels adds %s and to map-transfer labels %s. Pair by pair at %s examples the map-transfer cost is "
      "%s with half the set moved and %s with three quarters, so the cost is linear in the share. Putting the ladder "
      "on the trials' rate and reading the trials at or under the pool against it gives %s and %s; the bands hold both "
      "readings. Read against the ladder as it ran, the contractor's labels come out better than expert labels (%s), "
      "which nothing supports."
      % (l3(h["lr_cost_128"]), n(128), n(c["expert_pool"]), l4(F["cost_ctr"]), l4(F["cost_map"]), n(c["expert_pool"]),
         l4(F["same_total_map"][0]), l4(F["same_total_map"][1]), l4(F["pool_reading"]["ctr"]), l4(F["pool_reading"]["map"]),
         l4(h["nomatch_ctr"])))
    A("5. A cost that is the same at every share is what pins the bend: taken out of the trials at %s and %s examples "
      "it leaves %s and %s for expert-quality labels at width %s (%s and %s on the other reading of the costs), so a "
      "doubling returns %s and then %s against the %s of the size ladder. The hurried analysis misses this: one "
      "scaling curve fitted through every run (a straight line, a quadratic or a power law with a floor in examples, "
      "with terms for width, each route's share and the learning rate) puts the %s level at %s to %s, and the ladder's "
      "own straight line reaches %s there, because both let the routes' costs absorb what is a bend in the return."
      % (n(256000), n(c["level_at"]), l3(F["level_256k"]), l3(F["level_512k"]), n(128), l3(F["pool_reading"]["level_256k"]),
         l3(F["pool_reading"]["level_512k"]), l3(F["gain_first"]), l3(F["gain_second"]), l3(F["gain_ladder"]),
         n(c["level_at"]), l2(pl["level"][0]), l2(pl["level"][1]), l3(F["line_as_run_512k"])))
    A("6. The check on the pilot's own largest runs: built from the runs at or under %s examples alone, every forecast "
      "undershoots the three larger configurations. Carried on from the separated levels the miss is %s on average "
      "(%s to %s across the sound readings, %s with a floor fitted by least squares to every level); the straight "
      "line misses by about %s and the single curve through every run by about %s. The larger runs sit above "
      "everything fitted without them, which is the bend and not noise, and the size of the miss is carried into the "
      "range."
      % (n(c["held_above"]), l4(F["gap"]), l4(F["gap_family"][0]), l4(F["gap_family"][1]), l4(F["gap_floor_ls"]),
         l3(F["gap_line"]), l2(pl["gap"])))
    A("7. Past %s examples each doubling is taken to return %s of the one before (%s against %s). Carrying the level "
      "to each configuration's size, taking off the width steps the pilot shows and adding each route's cost at the "
      "configuration's shares gives A %s, B %s, C %s and D %s (A at learning rate %s, where each width's best rate in "
      "the learning-rate check points one doubling past %s). Two things are carried past what the pilot ran, and are "
      "bounded, not measured. What the examples past the largest trial return: with the last doubling's gain carried "
      "on undiminished C is %s and D %s, with no further gain %s and %s. And the step from width %s to %s, which no "
      "run with B's labels took: the benchmark's own scores of %s expert-label runs show a gain of %s, while the "
      "carried loss of the same runs reads it the other way and puts B at %s; B's band holds both. The single curve "
      "through every run puts C at %s to %s against %s to %s for B and names C under each of its three forms: its C "
      "sits below what the last doubling's gain carried on undiminished gives."
      % (n(c["level_at"]), l2(F["curve_ratio"]), l3(F["gain_second"]), l3(F["gain_first"]), l3(ex["A"]), l3(ex["B"]),
         l3(ex["C"]), l3(ex["D"]), rate(F["lr_1024"]), n(512), l3(bo["C"][0]), l3(bo["D"][0]), l3(bo["C"][1]), l3(bo["D"][1]),
         n(256), n(512), words(F["width_step_512_runs"]), l3(F["width_step_512"]), l3(F["carried_B"]),
         l2(pl["C"][0]), l2(pl["C"][1]), l2(pl["B"][0]), l2(pl["B"][1])))
    A("8. One run of B varies with the run (%s), with the forecast (%s on the held-back configurations) and with the "
      "yardstick (%s); combined, four results in five fall between %s and %s. Seed spread alone would give %s to %s."
      % (l4(F["range_parts"]["run"]), l4(F["range_parts"]["forecast"]), l4(F["range_parts"]["yardstick"]),
         l3(F["range_low"]), l3(F["range_high"]), l3(h["seed_range"][0]), l3(h["seed_range"][1])))
    A("9. B has the lowest expected benchmark loss, %s ahead of A and %s ahead of C, and is the configuration to name."
      % (l3(F["margin"]), l3(F["lead_over_C"])))
    A("")
    A("No other conclusion survives the files. Ranking on the logged development loss fails because that loss is "
      "scored partly on the vendors' own labels, which the development split and the shard register show. A single "
      "curve through every run, or the size ladder's straight line, names C only by missing the pilot's own largest "
      "configurations, all in the same direction, when they are held back. Every reading that separates the level "
      "from the routes' costs names B: by %s to %s over the next configuration across the choices the files leave "
      "open (the benchmark calibration as a line or an offset, the width step at the largest totals or averaged, a "
      "level of its own past the pool or at every total, a scored run on its own benchmark score or on the carried "
      "loss), and still by %s over C with the last doubling's gain carried on undiminished. Using only the runs the "
      "benchmark scored leaves B, C and D with no figure at all and A at about %s (the %s-wide runs' own score less "
      "one more width step), which B's %s beats."
      % (l3(F["lead_central"][0]), l3(F["lead_central"][1]), l3(F["lead_least"]), l3(h["scored_only_A"]), n(512),
         l3(ex["B"])))
    return "\n".join(lines) + "\n"


def write(F, path):
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text(F))
