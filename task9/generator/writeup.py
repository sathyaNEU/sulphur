"""submission.md: the four answer blocks, every figure emitted from figures.json."""
import core as C
import deliver
import world as WL

G = C.GROUPS
F = WL.FILES
MONTHS = [n for n, _, _ in C.Q3_MONTHS]
RANK = [j for j in G if C.G[j]["pre"]]
RERANK = [j for j in G if not C.G[j]["pre"]]


def lst(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def rng(b, nd=3):
    return "%.*f to %.*f" % (nd, b[0], nd, b[1])


def each(vals, nd=3, groups=G):
    return ", ".join("%s %.*f" % (j, nd, vals[j]) for j in groups)


def banded(vals, bands, nd=3, keys=G):
    return "; ".join("%s %.*f (%s)" % (k, nd, vals[k], rng(bands[k], nd)) for k in keys)


def write(path, f):
    on, off = f["list"], f["off_list"]
    h, R, a, nv, k = f["hurried"], f["routes"], f["april"], f["nearest_variant"], f["counts"]
    wb, csv = deliver.FILES["wb"], deliver.FILES["csv"]
    hon = h["list"]
    hoff = [j for j in on if j not in hon]
    hextra = [j for j in hon if j not in on]
    fs, fe, me = f["fresh_share_pct"], f["full_effect"], f["measured_effect"]
    out = []
    w = out.append
    w("# task9 answer blocks\n")
    w("## Tags\n")
    w("**Domain:** General Statistics & Data Science (Machine Learning Research), Interpretability (feature attribution: "
      "what the degraded service of each of a search ranking model's seven feature groups cost conversion).")
    w("**Analytical objective:** Root-Cause Analysis.\n")
    w("## Final Recommendation\n")
    w("**Put %s on the 2027 tier one list and leave %s off it: trend's degraded service cost %.3f points of search "
      "conversion over the third quarter of 2026 and promise's %.3f, both over the charter's %.2f, and seller's %.3f.** "
      "This rejects the ablation tests as reported applied to the status record's unhealthy share, which list %s (%.3f "
      "points) beside %s and leave %s off: a test withholds a group only on result pages built at origin, a failed "
      "source's value goes on being served for its validity, and promise is also read by a page component no ablation "
      "test withholds.\n" % (
          lst(on), lst(off), f["cost"]["trend"], f["cost"]["promise"], f["line"], f["cost"]["seller"],
          lst(hextra), h["cost"]["seller"], lst(j for j in hon if j in on),
          lst("%s (%.3f)" % (j, h["cost"][j]) for j in hoff)))
    w("## Supplementary Questions\n")
    w("### %s\n" % wb)
    w("1. Each feature group's cost over the third quarter of 2026, in points of search conversion (the range any sound "
      "set of estimating conventions gives is in brackets): %s." % banded(f["cost"], f["cost_band"]))
    w("2. All the groups together over the quarter: %.2f points (%s)." % (f["all"], rng(f["all_band"], 2)))
    w("3. All the groups together in each month, over that month's search sessions: %s." % (
        banded(f["month"], f["month_band"], 2, MONTHS)))
    w("4. The groups on the list together: %.2f points (%s)." % (f["listed_cost"], rng(f["listed_band"], 2)))
    w("5. The workbook opens on the list: one row per feature group with its cost, its range and its tier, rows for all "
      "the groups and for the listed groups together, the three months, and a column chart of the seven costs against "
      "the %.2f line.\n" % f["line"])
    w("### %s\n" % csv)
    w("6. One row per feature group and month: the group, the month and the group's cost over that month's search "
      "sessions in points of search conversion.\n")
    w("## Critical Components\n")
    w("1. A session served trend's default loses **%.2f points** of search conversion (%s), the effect its ablation tests "
      "report taken over the share of the held users' result page views that were built at origin and not served from "
      "the page cache." % (f["c1"], rng(f["c1_band"], 2)))
    w("2. Seller's failed scoring runs put **%.2f per cent** of the quarter's search sessions on a default score over "
      "what normal service leaves there (%s per cent), each seller's score replayed night by night with its five days' "
      "validity and weighted by the seller's traffic." % (f["c2"], rng(f["c2_band"], 2)))
    w("3. The delivery promise badge, which reads promise and is in no ablation test, cost **%.3f points** over the "
      "quarter (%s), from its own holdout test and its eligible sessions at promise's default share." % (
          f["c3"], rng(f["c3_band"])))
    w("4. April's missed price batches in one serving region, called by the same route, come to **%.3f points** over "
      "the business days touched (%s), which the conversion mart by serving region then tests.\n" % (
          f["c4"], rng(f["c4_band"])))
    w("## Step-by-Step\n")
    w("1. Brought the records to UTC hours and one market and device scheme (`%s` maps the mart's keys; `%s` is in local "
      "time with its offset). `%s` holds %s rows, %s of them the earlier load of an hour the monitor loaded again (the "
      "later load stands), and the former shard names of the chains moved to the new gateway map through `%s`. `%s` "
      "holds %s rows, %s written twice, so %s runs of %s sellers, with two status vocabularies. `%s` holds %d "
      "experiments: %d completed ablation tests (%d a group, %d days each), %d aborted run, %d component holdouts (%d "
      "days). Search conversion (`%s`) was %.2f per cent in the second quarter and %.2f in the third, over %.1f million "
      "third-quarter search sessions (`%s`)." % (
          F["markets"], F["gaps"], F["status"], format(k["status_rows"], ","), format(k["status_rows_reloaded"], ","),
          F["shares"], F["scoring"], format(k["scoring_rows"], ","), format(k["scoring_repeats"], ","),
          format(k["scoring_runs"], ","), format(k["sellers"], ","), F["experiments"], k["experiments"],
          k["ablation_tests"], k["tests_per_group"], k["test_days"], k["aborted"], k["holdouts"], k["holdout_days"],
          F["mart"], f["conversion"]["q2"], f["conversion"]["q3"], f["q3_sessions_m"], F["sessions"]))
    w("2. The hurried reading multiplies two records as they stand. The status record's unhealthy share, with each "
      "shard weighted by the traffic it carries, is %s per cent of the quarter's sessions. Each group's ablation "
      "tests, pooled by device and netted for that share on the tests' own days (every route here nets a group's "
      "tests for the default share that route gives the group), report an effect of %s points a session. Their "
      "product is %s points, which lists %s. Three things about what those two records hold overturn it (steps 3 to "
      "5)." % (each(f["status_unhealthy_pct"], 2), each(h["effect"], 2), each(h["cost"]), lst(hon)))
    rh = f["reported_effect_halves"]
    w("3. What an ablation test withholds. `%s` applies a feature ablation at the rank and rerank stages and sets the "
      "page cache between them: the first-pass page is read from the cache on every request and written only by "
      "requests without overrides, and the key carries no arm. A held user's request for a cached page is served the "
      "ranking built with the group. %s are read at the first pass; %s at the second, per request. `%s` gives the "
      "share of result page views built at origin by market, device and day: %d per cent on app and %d on web until "
      "the cache lifetime changed on 9 June, %d and %d after. The tests show it: trend's report %.2f points in the "
      "January to May tests and %.2f in the July to September ones, where stock's report %.2f and %.2f. Each "
      "first-pass group's full effect is, by device, the sum over its tests, days and markets of the reported effect "
      "(control conversion less held, in points) times the held sessions, over the sum of the share built at origin "
      "times one less the group's default share that day times the held sessions; a second-pass group's leaves the "
      "share built at origin out. At the quarter's device mix that is %s points a session at the default: trend %.2f "
      "(%s) against %.2f taken over every held session. Taking the tests that way puts trend at %.3f points and leaves "
      "it off the list." % (
          F["pipeline"], lst(RANK).capitalize(), lst(RERANK), F["cache"], fs["app"]["before"], fs["web"]["before"],
          fs["app"]["after"], fs["web"]["after"], rh["trend"]["jan_may"], rh["trend"]["jul_sep"], rh["stock"]["jan_may"],
          rh["stock"]["jul_sep"], each(fe, 2), f["c1"], rng(f["c1_band"], 2), me["trend"], R["S1"]["cost"]["trend"]))
    s = f["seller"]
    sd = f["served_default_pct"]
    w("4. What was served. `%s` serves a value until its validity runs out and the group default after (stock 2 hours, "
      "price 36, trend 6, seller 120), so a failure and a default served are different hours. Replayed each source's "
      "state from its own log. Stock (`%s`, %s gaps): a chain's snapshot is at the default from %.1f minutes after its "
      "feed stops (2 hours less half a 15-minute sync interval) until %.1f minutes after it resumes, and a gap that ends before then never reaches the default. Price (`%s`): a "
      "batch loaded at 04:00 is served 36 hours, so one missed batch leaves the source at the default from 16:00 until "
      "the next loaded batch. Trend (`%s`, %d episodes): a partition's counters are at the default from 6 hours into a "
      "lag until one hourly window after it catches up. Seller (`%s`): a seller is at the default score from the "
      "fifth night after its last scored run. Sources are weighted by the traffic they carry (`%s`; `%s` by month), "
      "and the request-time groups take the status record's share of requests. Over the quarter %s per cent of "
      "sessions were served a default over normal service. For seller, %.2f per cent of the quarter's runs failed, "
      "but %.2f per cent of sessions were served a default score, and %.2f per cent would have been with every failed "
      "run scored (a seller with nothing newly settled is at the default in normal service, charter 3.2), which "
      "leaves %.2f per cent (%s). Taking the status record's share (and seller's tests netted for it, %.2f points a "
      "session) puts seller at %.3f points and lists it." % (
          F["store"], F["gaps"], format(k["gaps"], ","), f["stated"]["stock_default_after_minutes"],
          f["stated"]["half_sync_minutes"], F["batches"], F["lags"], k["lag_episodes"], F["scoring"], F["shares"],
          F["seller_traffic"], each(sd, 2), s["failed_share_q3_pct"], s["total_default_pct"], s["usual_default_pct"],
          f["c2"], rng(f["c2_band"], 2), R["S2"]["effect"]["seller"], R["S2"]["cost"]["seller"]))
    rp, re_, rc, rf = f["reader_per_eligible"], f["reader_eligible_pct"], f["reader_cost"], f["render_failed_pct"]
    w("5. Who else reads the group. `%s` lists three page components that read a feature group and are suppressed when "
      "its value is missing: %s (promise), %s (price) and %s (history). An ablation applies at rank and rerank and "
      "never at render, so no ablation test holds their loss. Each has its own holdout in `%s` (%d per cent held): by "
      "device, the control arm's conversion less the held arm's over the control arm's eligible share of sessions "
      "gives a loss of %.2f, %.2f and %.2f points an eligible session, with %d, %d and %d per cent of sessions "
      "eligible. `%s` counts each component's eligible sessions by market, device and hour, and its failed renders "
      "move with the group's default (the badge failed %.2f per cent of eligible sessions in the second quarter and "
      "%.2f in the third). A component's cost is its loss an eligible session times its eligible sessions at the "
      "group's default share: the badge %.3f points (%s), the label %.3f, the strip %.3f. Pricing each group through "
      "the ranking model alone puts promise at %.3f points and leaves it off the list." % (
          F["pipeline"], WL.COMPONENT["promise"], WL.COMPONENT["price"], WL.COMPONENT["history"], F["experiments"],
          f["stated"]["holdout_pct"], rp["promise"], rp["price"], rp["history"], re_["promise"], re_["price"],
          re_["history"], F["render"], rf["promise"]["q2"], rf["promise"]["q3"], f["c3"], rng(f["c3_band"]), rc["price"],
          rc["history"], R["S3"]["cost"]["promise"]))
    rv = a["rivals"]
    w("6. Checked the route on a record it does not use. On %d nights in April the price batch did not reach serving "
      "region fra2 (`%s`). `%s` assigns users to a region by hash and gives each region its own page cache, so fra2's "
      "users met the price default on every page and on the label from 16:00 to 04:00 after each missed batch. `%s` "
      "shows ams1 converting %.3f points above fra2 over the %d business days those hours touch (standard error "
      "%.3f). The route calls %.3f (%s): price's full effect plus the label's loss on its eligible share, times the "
      "share of the window's sessions in the expired hours. The tests as reported call %.3f, the batches' failed "
      "hours in place of the expired ones %.3f, the ranking model alone %.3f, and the three together %.3f (each with "
      "its tests netted for its own share, as in step 2)." % (
          a["batches"], F["batches"], F["regions"], F["mart"], a["record"], a["days"], a["record_se"], a["golden"],
          rng(a["band"]), rv["S1 lost"]["value"], rv["S2 lost"]["value"], rv["S3 lost"]["value"],
          rv["every stump lost"]["value"]))
    w("7. Each group's cost by market, device and hour is its full effect times the share of sessions served its default "
      "over normal service, plus its component's cost; averaged over the quarter's search sessions (charter 3.3) that "
      "is %s points, and %.2f for all the groups together (3.4). Over each month's sessions the groups together cost "
      "%s (`%s`, %d rows)." % (
          each(f["cost"]), f["all"], lst("%.2f points in %s" % (f["month"][n], n) for n in MONTHS), csv, f["csv_rows"]))
    near = min(G, key=lambda j: f["margin"][j])
    w("8. Applied the charter's 4.1: %s are %.2f points or more and go on the list (%.2f points together); %s are below "
      "it. The nearest group to the line is %s, %.3f points from it." % (
          lst(on), f["line"], f["listed_cost"], lst(off), near, f["margin"][near]))
    w("9. Rebuilt the route under %d sets of conventions (effects by device, by market and device or pooled, weighted "
      "by sessions or precision, on every completed test, the first half's or those from April, netted or not for the "
      "default on a test's own days; the share built at origin by day or over each test; a snapshot fresh, half or a "
      "whole sync interval old when its feed stops; counters back at once, one or two hours after catch-up; sellers "
      "weighted by the month's or the quarter's traffic; what normal service leaves for sellers from the same nights "
      "replayed or from the level of the second quarter, June or the first half (the first half taken from 11 "
      "January throughout, the record's first nights having no five nights behind them); a component's loss by device or "
      "pooled, on its eligible sessions at the group's default share or on its failed renders over the rate at which "
      "it fails with the value present, or over its rate in the second quarter, June or the first half; and every "
      "pair of these that changes two different choices): all give the same list, the nearest any comes to the line "
      "is %.4f points (%s), and the stated ranges hold every one. Each fitted input moved by the furthest any rebuild "
      "moves it, alone and all three together, leaves the list unchanged.\n" % (
          f["variants"], nv["distance"], nv["group"]))
    dr, rg = R["direct"], R["rigorous"]
    reg = f["rival_daily_regression"]
    ar = f["rival_april_ratio"]
    w("No other list survives the files. The tests on the status record pass every check they offer (the held arm is "
      "%.2f per cent of the two arms' sessions, as designed, a group's tests agree within a half-year, the status record's seller and "
      "price rows equal the scoring and batch logs' own failure counts) and miss the one record that tests them: they "
      "call April at %.3f points where the mart shows %.3f. The same route with every test pooled by market and "
      "device and weighted by precision files %s points and lists %s; each job's unhealthy share of the quarter's "
      "session hours with every chain, price source and click-stream partition counted once (the other four groups "
      "as the status record gives them), times its latest test's reported effect with every market and device "
      "pooled, files %s and lists %s. April used as one calibration ratio (%.2f on the "
      "hurried call) and carried to every group gives %s points and is wrong for %s: one ratio cannot stand for three "
      "corrections that differ by group. Each correction left out alone moves a group: without the share built at "
      "origin trend is left off, without the replay seller is listed, without the components promise is left off.\n" % (
          f["held_share_pct"], rv["every stump lost"]["value"], a["record"], each(rg["cost"]), lst(rg["list"]),
          each(dr["cost"]), lst(dr["list"]), ar["ratio"], each(ar["cost"]), lst(ar["wrong"])))
    un_ = f["rival_daily_regression_unplaced"]
    rr, ta, arms = f["rival_replayed_regression"], f["test_agreement"], f["trend_arms"]
    w("The daily record cannot draw the list. A regression of daily conversion by market and device on the status "
      "shares (with market and device, weekday and month effects and one promotion-day effect, weighted by sessions, standard errors "
      "clustered by day) gives %s points with standard errors of %.3f to %.3f; by its point estimates it lists %s, "
      "and it cannot place %s against the line (%s standard errors from it). The same regression on the replayed "
      "shares of step 4 gives %s points, %.2f together, and puts trend at %.3f. That is %.2f points a session at the "
      "default, where trend's nine randomised tests measure %.2f (standard error %.3f). Trend's default share is the "
      "same in every market and on both devices on a day, so the daily record sets it against nothing but other "
      "days, and on those days the held users of trend's own tests, whose pages built at origin never carried it, "
      "lose %.2f points per unit of that share (standard error %.2f; the arm's daily conversion by market and "
      "device with the other groups' cost added back, on that share with market and device, weekday and month "
      "effects, weighted by the arm's sessions, clustered by day) where trend's effect on their cached pages "
      "accounts for %.2f, and the control arm loses %.2f. What the regression loads on trend does not pass through a "
      "reader of the group, and the charter's 3.3 prices the group's service to the services that read it.\n" % (
          each({j: reg[j]["cost"] for j in G}), min(reg[j]["se"] for j in G), max(reg[j]["se"] for j in G),
          lst(f["rival_daily_regression_list"]), lst(j for j in G if j in un_),
          lst("%.1f" % un_[j] for j in G if j in un_), each(rr["cost"]),
          rr["all"], rr["cost"]["trend"], rr["per_session"]["trend"], f["c1"],
          ta["trend"]["se_all"], arms["held"], arms["held_se"], arms["held_expected"], arms["control"]))
    sub = f["rival_test_subsets"]
    q3s, chg, lt = (sub[n] for n in ("the quarter's own tests", "the four tests from June", "the latest test alone"))
    st = f["rival_test_subsets_stacked"]
    w("Which tests carry a group's effect. Taking it from the quarter's own three tests, or from the four from June "
      "on, keeps the list (trend %.3f and %.3f points, price %.3f and %.3f) and leaves the stated ranges of trend, "
      "price and components 1 and 4 (%.2f and %.2f points a session; April called at %.3f and %.3f). The tests "
      "refuse it as the estimate: a group's tests agree once each is taken over the pages built without the group "
      "(each test's full effect at the quarter's device mix with the binomial standard error of its two arms, and "
      "Cochran's Q about their precision-weighted mean: %.1f for trend and %.1f for price on %d degrees of freedom), "
      "so the quarter's three measure the same effect at over twice the standard error (trend %.3f points a session "
      "against %.3f, price %.3f against %.3f). On them trend's cost is %.3f plus or minus %.3f, %.1f standard errors "
      "over the line; on all nine it stands %.1f over it. April reads the same way: the quarter's tests call it "
      "%.1f standard errors from the mart's figure, all nine %.1f. With counters back at once, and then with no netting as "
      "well, the quarter's tests put trend at %.4f and %.4f, still on the list. The latest test alone gives trend "
      "%.3f plus or minus %.3f and would leave it off the list on one test of nine.\n" % (
          q3s["cost"]["trend"], chg["cost"]["trend"], q3s["cost"]["price"], chg["cost"]["price"], q3s["c1"], chg["c1"],
          q3s["c4"], chg["c4"], ta["trend"]["q"], ta["price"]["q"], ta["trend"]["df"], ta["trend"]["se_quarter"],
          ta["trend"]["se_all"], ta["price"]["se_quarter"], ta["price"]["se_all"], q3s["cost"]["trend"],
          ta["trend"]["cost_se_quarter"], q3s["trend_from_line_se"], ta["trend"]["from_line_all"],
          q3s["april_off_se"], a["golden_off_se"], st["trend"][0],
          st["trend"][1], lt["cost"]["trend"], ta["trend"]["cost_se_latest"]))
    bs = {b["name"]: b for b in f["beside"]}
    nb = f["nearest_beside"]
    w("Beside the conventions of step 9, seven further readings were run and all keep the list inside every stated "
      "range: the quarter cut on Utrecht's calendar days in place of the mart's business days; the monitor's first load "
      "of each hour kept in place of the later; the aborted test read with the completed ones; a component's loss taken "
      "per session of its own test, eligible or not; a component's loss an eligible session market by market; each "
      "group's full effect as the mean of its tests' own ratios (trend %.2f points a session); and every default share "
      "taken day by day before it meets the sessions, a source's as its share of the day's hours at the default and "
      "a request-time group's as the day's failed requests over the day's requests (stock %.4f points, match %.4f). The nearest any of them comes to "
      "the line is %.4f points (%s).\n" % (
          bs["each group's full effect as the mean of its tests' own ratios"]["c"][0],
          bs["every default share taken day by day before it meets the sessions"]["cost"]["stock"],
          bs["every default share taken day by day before it meets the sessions"]["cost"]["match"],
          nb["distance"], nb["group"]))
    un, ind, us = f["rival_seller_not_netted"], f["rival_seller_independent_nights"], f["rival_usual_level"]
    w("Three readings the files refuse. Seller's default charged in full, with nothing taken off for sellers who had "
      "nothing new to score, gives %.2f per cent of sessions and %.3f points, still off the list; the charter's 3.2 "
      "counts a source refreshing on its schedule as normal service. Seller's failures taken as independent from night "
      "to night (a score lost only after five failed runs in a row at the job's nightly rate) give %.2f per cent and "
      "%.4f points; over the quarter's runs, each set against the same seller's run before it, a seller whose last run failed "
      "fails %.1f per cent of the time, against %.1f per cent after a scored run. Normal service read as the "
      "second quarter's level of service (each default share over its second-quarter mean, %s per cent, and the "
      "components' failed renders over their second-quarter rate) gives %s points and the same list; the charter's "
      "3.2 defines normal service as sources refreshing on schedule and services answering, which the second quarter "
      "was not throughout.\n" % (
          un["served_pct"], un["cost"], ind["served_pct"], ind["cost"], f["seller"]["fail_after_fail_pct"],
          f["seller"]["fail_after_scored_pct"], each(us["q2_default_pct"], 2), each(us["cost"])))
    text = "\n".join(out)
    assert "—" not in text
    open(path, "w").write(text)
