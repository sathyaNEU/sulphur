"""submission.md: the tags and the four answer blocks, every figure from figures.json."""
import deliver
import docs
import pack

F = dict(pack.FILES)
F.update(docs.FILES)


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _b(f, fid, nd=2, money=False):
    lo, hi = f["figure_band"][fid]
    if money:
        return "%s to %s" % (format(lo, ","), format(hi, ","))
    return "%.*f to %.*f" % (nd, lo, nd, hi)


def write(path, f):
    chans = deliver.order(f)
    b = f["by_band"]
    rp, R = f["return_plan"], f["routes"]
    ch, st, u = f["channels"], f["stores"], f["unnamed"]
    gp, ap = st["Google Play"], st["App Store"]
    L = ["# task1 answer blocks", "", "## Tags", "",
         "**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer lifetime value).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "", "## Final Recommendation", ""]
    L.append(
        "**Scale %s, hold %s and cut %s for 2027**: at the plan's weekly spend the returns are %s euros of 12-month net "
        "revenue per euro of spend, against the growth policy's lines of %.2f and %.2f. This rejects scaling Meta iOS (%.2f) "
        "and cutting Google Android (%.2f) and AppLovin Android (%.2f), the bands filed when the billing records are trued up "
        "to the stores' reports month by month, every install postback is valued like the installs the attribution export "
        "names and the response is fitted on weekly spend: the stores' excess belongs to subscriptions whose owners stopped "
        "opening the app, the named installs are worth more than the rest at the same first two days, and a week's spend "
        "moves with what the platform delivered of the budget, not with the budget." % (
            _list(b["scale"]), _list(b["hold"]), _list(b["cut"]), _list("%s %.2f" % (c, rp[c]) for c in chans),
            f["policy"]["lines"][0], f["policy"]["lines"][1], R["S1+S2+S3"]["Meta iOS"]["return"],
            R["S1+S2+S3"]["Google Android"]["return"], R["S1+S2+S3"]["AppLovin Android"]["return"]))
    L += ["", "## Supplementary Questions", "", "### %s" % deliver.FILES["wb"], ""]
    L.append("1. First sheet: one row per channel of the plan's growth sheet with its band and the four figures of items 3 to "
             "%d, and a chart of each channel's return at the plan's and the stretch spend against the %.2f and %.2f lines." % (
                 2 + len(chans), f["policy"]["lines"][0], f["policy"]["lines"][1]))
    L += ["", "### %s" % deliver.FILES["csv"], ""]
    L.append("2. Seven rows, one per channel, highest return first: the band, the return at the plan's weekly spend and at its "
             "stretch spend (euros of 12-month net revenue per euro of spend), the 12-month net revenue per install of the "
             "installs the plan's spend buys (euros) and what one more euro on top of the plan's weekly spend returns (euros "
             "of 12-month net revenue). Each figure's band is in brackets.")
    for i, c in enumerate(chans):
        L.append("%d. %s (%s): return %.2f (%s) at the plan's weekly spend and %.2f (%s) at the stretch spend; EUR %.2f (%s) "
                 "per install; EUR %.2f (%s) from one more euro." % (
                     3 + i, c, f["bands"][c], rp[c], _b(f, "return " + c), f["return_stretch"][c], _b(f, "stretch return " + c),
                     f["value_plan"][c], _b(f, "value at plan " + c), f["next_euro"][c], _b(f, "next euro " + c)))
    L += ["", "## Critical Components", ""]
    L.append("1. The billing records never took in **%.1f per cent** (band %s) of the 12-month net revenue of the installs "
             "AppLovin Android bought from 4 November 2024 to 2 November 2025." % (
                 f["unrecorded_share_applovin_android_pct"], _b(f, "unrecorded share AppLovin Android", 1)))
    L.append("2. Over every install Meta iOS bought in those %d weeks, named in the attribution export or not, the 12-month net "
             "revenue is **EUR %.2f** per install (band %s)." % (
                 f["steps"]["mature_weeks"], f["value_per_install_meta_ios"], _b(f, "value per install Meta iOS")))
    L.append("3. At the plan's weekly spend the five iOS networks buy **EUR %s** of 12-month net revenue in 2027 (band %s)." % (
        format(f["plan_and_stretch_revenue"]["plan revenue iOS networks"], ","), _b(f, "plan revenue iOS networks", money=True)))
    L.append("4. The stretch spend adds **EUR %s** of 12-month net revenue across the seven channels (band %s)." % (
        format(f["plan_and_stretch_revenue"]["stretch adds"], ","), _b(f, "stretch adds", money=True)))
    L += ["", "## Step-by-Step", ""]
    s = f["steps"]
    w, a, pc = f["check_web"], f["check_search_ads"], f["pct"]
    ga, me, al = ch["Google Android"], ch["Meta iOS"], ch["AppLovin Android"]
    mv = f["check_moves"]["Google Android"]
    mw = f["check_moves_weeks"]
    cont = ("%.3f on both stores" % gp["continuation"] if gp["continuation"] == ap["continuation"]
            else "%.3f and %.3f" % (gp["continuation"], ap["continuation"]))
    steps = [
        "Kept the %s consumer accounts of `%s` (%d staff and test accounts out) and the production charges of `%s` (a re-sent "
        "checkout row counted once, the %s refunded purchases out); took each account's install row and channel from `%s` "
        "(re-sent rows and reinstalls dropped) and counted each iOS network's installs from `%s` (one per postback, "
        "redownloads out, the install placed three days before the postback arrived)." % (
            format(s["consumer_accounts"], ","), F["acc"], s["other_accounts"], F["bill"], format(s["refunded_purchases"], ","),
            F["attr"], F["skan"]),
        "Valued every charge at its transaction time under `%s` (VAT by storefront, the stores' %d per cent, the checkout's "
        "%d per cent) and summed each account's %d days from its `created_at`, which also sets its install week (counted "
        "from the attribution export's `install_time` instead, every return is the same to two decimals); the %d install "
        "weeks from 4 November 2024 have their twelve months on file." % (
            F["policy"], f["policy"]["commission_pct"], f["policy"]["fee_pct"], s["days"], s["mature_weeks"]),
        "Set `%s` and `%s` against the billing events by store and by period of %s days counted from 4 November 2024 "
        "(App Store charges on Pacific days): Google Play "
        "reports %s monthly charges against %s in the records and the App Store %s against %s." % (
            F["google"], F["apple"], f["policy"]["cadence_days"], format(gp["store_monthly_charges"], ","),
            format(gp["recorded_monthly_charges"], ","),
            format(ap["store_monthly_charges"], ","), format(ap["recorded_monthly_charges"], ",")),
        "The excess sits on subscriptions last seen still set to renew whose next charge fell after the account's last open "
        "(%s on Google Play, %s on the App Store) and on trials last seen set to renew. From the stores' first charges "
        "beyond the records, %.3f and %.3f of the monthly trials and %.3f and %.3f of the %s and %s annual trials (%s and "
        "%s annual first charges beyond the records) were charged at the trial's end; from the stores' renewals beyond the "
        "records, a subscription the app no longer sees continues at %s a month; each such account's expected "
        "charges inside its %d days were added. That leaves %.1f to "
        "%.1f per cent of a plan channel's 12-month net revenue outside the records, AppLovin Android's the highest. The "
        "hurried route scales each recorded charge by its store-month's ratio, which puts %.1f to %.1f per cent on every "
        "channel and AppLovin Android's return at %.2f; on AppLovin Android's %d monthly web-checkout subscribers last "
        "seen set to renew with a charge up to their last open, whose every charge is on file, EUR %.2f each was charged "
        "after the last open inside the twelve months, the fitted rule puts %.2f there and the ratio %.2f." % (format(gp["renewal_candidates"], ","), format(ap["renewal_candidates"], ","),
                   gp["trial_end_share_monthly"], ap["trial_end_share_monthly"], gp["trial_end_share_annual"],
                   ap["trial_end_share_annual"], format(gp["trial_candidates_annual"], ","),
                   format(ap["trial_candidates_annual"], ","), format(gp["annual_excess"], ","),
                   format(ap["annual_excess"], ","), cont, s["days"],
                   pc["unrecorded_low"], pc["unrecorded_high"], pc["prop_low"], pc["prop_high"],
                   R["S1"]["AppLovin Android"]["return"], w["subscribers"], w["charged"], w["estimate"], w["true_up"]),
        "The attribution export names %.1f to %.1f per cent of an iOS network's installs. Counted the rest by first-48-hour "
        "value (postbacks less named installs), took the organic remainder among the %s accounts with no channel, and priced "
        "the unnamed installs of each first-48-hour value at the named installs' value times that value's own ratio, the "
        "one at which the accounts with no channel at that value add up to what they paid (EUR %s in all): Meta iOS EUR "
        "%.2f per install against %.2f for its named installs. Where a network has fewer than %d named installs at a "
        "first-48-hour value, that value takes what all named installs are worth there, scaled by the network's named "
        "total over that pricing; where fewer than %d accounts with no channel sit at a value, it takes the ratio of all "
        "values together. The hurried route values every "
        "postback like the named installs at the same first-48-hour value (Meta iOS %.2f, a return of %.2f, scale), which "
        "puts the accounts with no channel at %.2f times what they paid; Apple Search Ads' %s installs that did not allow "
        "tracking, named on every account, paid EUR %.2f each against %.2f from the pricing and %.2f from the named "
        "installs' value." % (pc["consent_low"], pc["consent_high"], format(u["accounts"], ","), format(u["paid"], ","),
                             me["value_per_install"], me["named_value"], s["thin_cell"], s["thin_cell"],
                             me["bridge_value"], R["S2"]["Meta iOS"]["return"],
                             u["adding_up_named_price"], format(a["installs"], ","), a["paid"], a["estimate"],
                             a["named_by_cell"]),
        "Regressed the log of each week's installs and of its value per install on the log of the week's budget (`%s`) "
        "and the log of the share of it the platform spent (`%s` over the budget), each channel of the records with its "
        "own level and slopes and one month pattern shared by all of them, Apple Search Ads included, over the %d weeks. A "
        "week takes the month of its Thursday, as the plan's blocks do, and its value per install prices its installs by "
        "first-48-hour value at what that value was worth over the %d weeks with twelve months on file. Google Android's "
        "installs rise %.2f per cent for one per cent of budget, against %.2f when fitted on spend. The hurried route's fit "
        "on spend passes a hold-out of weeks and files Google Android at %.2f, a cut; over the %d weeks the team raised "
        "Google Android's budget and the %d it lowered it, each move left out of the fit, total installs in the raised "
        "weeks over total installs in the lowered weeks were %.2f, the budget fit gives %.2f and the spend fit %.2f." % (
            F["budget"], F["spend"], s["weeks"], s["mature_weeks"], ga["budget_elasticity"], ga["spend_elasticity"],
            R["S3"]["Google Android"]["return"], mw["raised"], mw["lowered"], mv["actual"], mv["budget_fit"],
            mv["spend_fit"]),
        "Carried each channel to the %d weeks of `%s` at the budget that delivers the plan's spend (the spend divided by "
        "the channel's spend over budget across the %d weeks). Installs come from the installs equation's budget slope "
        "and month pattern, scaled so that those two terms alone, over the %d weeks, add up to the installs counted (which "
        "leaves the share spent at its average effect over those weeks); value per install comes from the value "
        "equation's budget slope and month pattern, scaled so that over the %d complete weeks, weighted by installs, they "
        "give the channel's 12-month net revenue per install; then again with every week raised to the stretch column. "
        "The next euro is the return times the sum of the two budget slopes, every week raised in the same proportion." % (
            s["plan_weeks"], F["plan"], s["weeks"], s["weeks"], s["mature_weeks"]),
        "Placed each return against %.2f and %.2f: %s scale, %s hold, %s are cut." % (
            f["policy"]["lines"][0], f["policy"]["lines"][1], _list(b["scale"]), _list(b["hold"]), _list(b["cut"])),
    ]
    for i, t in enumerate(steps):
        L.append("%d. %s" % (i + 1, t))
    nv = f["nearest_variant"]
    ro = {}
    for r in f["ruled_out"]:
        ro.setdefault(r["by"], r)
    bl, ho = ro["media plan"]["blocks"], ro["moved weeks"]["holdout"]
    sa, an = ro["Apple Search Ads"]["search_ads"], ro["annual first charges"]["annual"]
    sg = ro["Apple Search Ads by sessions"]["groups"]
    sc = f["shortcut_conventions"]
    L += ["", "No other conclusion survives. The %d other defensible ways of taking the steps file the same seven bands, and "
              "each band above is the range of their figures with %s per cent of the figure either side. For the stores' "
              "excess: one fit across both stores, a two-rate "
              "continuation, a 30-day cadence, the fit without its last two months, calendar months, the App Store's report "
              "days taken as UTC days, the refunds netted on the refund's day or from the renewals, the annual trials at the "
              "monthly trials' share, the two rates fitted together, the continuation read on the web subscribers. For the "
              "unnamed installs: the first-48-hour values in eight or four groups, by the sessions bucket or by the trial "
              "and purchase bits alone, cells of fifty or more or every value on its own installs, one tilt per source, the "
              "accounts with no channel's own value by first-48-hour value, Apple Search Ads' own ratio of unnamed to named "
              "value (by two groups of the value or value by value), a postback placed four days back. For "
              "the response: each channel's own month pattern, the plan's seven channels alone, installs fitted on the %d "
              "complete weeks, without the launch quarter or on the last 78 weeks, the complete weeks' own values, one value "
              "slope across channels, the budget conversion at the complete weeks' delivery share, the last 52 weeks' "
              "delivery share in the conversion and in the share spent, a trend or a second-year level, spend instrumented "
              "by the budget, the budget alone. Each of these was also run with the two equations carried as fitted, the "
              "share spent at its two-year ratio, at its mean log or averaged over its weeks (the bare carries with and "
              "without the smearing factor). The closest any comes to a line is %s at %.3f from it." % (
                  f["variants"], f["band_pad_pct"], s["mature_weeks"], nv["channel"], nv["distance"]),
          "",
          "Five ways of taking a step are refuted by the files and are left out of the bands; each still files the same "
          "seven bands of the policy. A week's month taken from its "
          "Monday: the plan's weekly spend changes on %d weeks, each the first whose Thursday falls in a new month, and on "
          "%d of them the Monday is still in the old month. The two equations in levels, or in levels on the logs: over the "
          "%d weeks the team moved a budget on the %d channels, each move left out of the fit, they miss the installs by "
          "about %d and %d per cent against %d, and by more on every channel. One price ratio for all first-48-hour values: "
          "it prices Apple Search Ads' %s unnamed installs at EUR %.2f against the %.2f they paid. Apple Search Ads' own "
          "ratio as one number for every value: of its unnamed installs that started a trial and bought nothing in the "
          "first 48 hours, the %s in the four lower session buckets paid EUR %.2f each against the %.2f it puts there and "
          "the %s in the four upper %.2f against %.2f. The annual trials left "
          "out: the stores report %s and %s annual first charges the records do not hold." % (
              bl["changes"], bl["apart_on_thursday"], ho["weeks"], ho["channels"], ho["error_whole"]["levels"],
              ho["error_whole"]["semilog"], ho["error_whole"]["log"], format(sa["installs"], ","), sa["priced"], sa["paid"],
              format(sg["lower"]["installs"], ","), sg["lower"]["paid"], sg["lower"]["priced"],
              format(sg["upper"]["installs"], ","), sg["upper"]["paid"], sg["upper"]["priced"],
              format(an["excess"]["Google Play"], ","), format(an["excess"]["App Store"], ",")),
          "",
          "The bands also stand with the stores' fitted rates, the unnamed installs' price ratio and each channel's two "
          "budget slopes moved a fifth either way, and with the budget that delivers the plan's spend moved by the %.1f "
          "per cent that the delivery share's widest quarter departs from the two-year share on any channel. The true-up "
          "in proportion, the named installs' value and "
          "the fit on spend are each refuted by a record the plan's channels do not reach (the web checkout's charges, "
          "Apple Search Ads' unnamed installs, the weeks the team moved a budget). Each keeps its channel in the wrong band "
          "however the response is carried (AppLovin Android %.2f to %.2f, Meta iOS %.2f to %.2f, Google Android %.2f to "
          "%.2f), and taken singly or together they file %d different wrong sets of bands." % (
              f["delivery_share_spread_pct"], sc["S1"]["low"], sc["S1"]["high"], sc["S2"]["low"], sc["S2"]["high"],
              sc["S3"]["low"], sc["S3"]["high"], f["distinct_wrong_calls"])]
    open(path, "w").write("\n".join(L) + "\n")
