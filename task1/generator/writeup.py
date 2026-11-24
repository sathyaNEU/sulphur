"""submission.md: the tags and the four answer blocks, every figure from figures.json. The answer to the form's stump
question (How is each model stumped?) is written from the platform's two responses once both are saved for this cut;
architecture 7's pair answered for a world this cut does not ship, so no stump block is written until then."""
import os  # noqa: E402
# numpy runs on Apple's Accelerate here, whose threads do not survive a fork: one thread, set before numpy loads
for _v in ("VECLIB_MAXIMUM_THREADS", "OPENBLAS_NUM_THREADS", "OMP_NUM_THREADS"):
    os.environ.setdefault(_v, "1")
import deliver
import docs
import pack

F = dict(pack.FILES)
F.update(docs.FILES)
LETTERS = "abcdefghijklmnopqrstuvwxyz"
A, G, M, GI = "AppLovin Android", "Google Android", "Meta iOS", "Google iOS"


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _n(x):
    return format(int(x), ",")


def _r(f, fam, c):
    """a channel's stated figure with its range"""
    x = f["figure"][fam + c]
    lo, hi = f["figure_band"][fam + c]
    nd = 3 if fam == "return " else 1
    return "%.*f (range %.*f to %.*f)" % (nd, x, nd, lo, nd, hi)


def _moved(f, key):
    """the channels a route files in another band, each with its return"""
    r = f["routes"][key]
    return ["%s %s (%.3f)" % (c, r[c]["band"], r[c]["return_plan"]) for c in deliver.order(f) if r[c]["band"] != f["bands"][c]]


def _two(t):
    return "%.2f and %.2f against %.2f" % (t["stat"], t["stat_one_variance"], t["point"])


def write(path, f):
    chans = deliver.order(f)
    b = f["by_band"]
    rp, R = f["return_plan"], f["routes"]
    ch, st, Q, P = f["channels"], f["stores"], f["ratios"], f["pooled"]
    gp, ap = st["Google Play"], st["App Store"]
    lo, hi = f["policy"]["lines"]
    s, sc = f["steps"], f["shortcuts"]
    rx = R["S1+S2+S3"]
    rej = [c for c in chans if rx[c]["band"] != f["bands"][c]]
    by = lambda band: [c for c in rej if rx[c]["band"] == band]   # noqa: E731
    assert by("scale") and by("cut"), rej
    L = ["# task1 answer blocks", "", "## Tags", "",
         "**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer lifetime value).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "", "## Final Recommendation", ""]
    L.append(
        "**Scale %s and hold %s for 2027**: at the plan's weekly spend their returns are %s euros of 12-month net revenue "
        "per euro of spend, against the growth policy's lines of %.2f and %.2f, and no channel is cut. This rejects scaling "
        "%s and cutting %s, the bands filed when the billing records are taken as they stand, the iOS installs the "
        "attribution export cannot name are valued at the shift the fully named channels show, and the plan's billed "
        "spend is read as a budget billed in full." % (
            _list(b["scale"]), _list(b["hold"]), _list("%s %.3f" % (c, rp[c]) for c in chans), lo, hi,
            _list("%s (%.3f)" % (c, rx[c]["return_plan"]) for c in by("scale")),
            _list("%s (%.3f)" % (c, rx[c]["return_plan"]) for c in by("cut"))))
    L += ["", "## Supplementary Questions", "", "### %s" % deliver.FILES["csv"], "",
          "One row per channel, highest return first (its band, return and payments per 100 installs), then one row for "
          "the whole plan (its installs and their revenue).", ""]
    L.append("1. Each channel's 2027 return in euros of 12-month net revenue per euro of spend at the plan's weekly spend, "
             "and the payments on the monthly plan that the installs it bought in the year to 2 November 2025 made in "
             "their first 12 months, per 100 installs:")
    for i, c in enumerate(chans):
        L.append("   %s. %s (%s): a return of %s, and %s payments on the monthly plan per 100 installs." % (
            LETTERS[i], c, f["bands"][c], _r(f, "return ", c), _r(f, "payments per 100 ", c)))
    pi, pv = f["figure_band"]["installs the plan buys"], f["figure_band"]["revenue the plan's installs bring"]
    L.append("2. The whole plan: its 2027 spend buys %s installs (range %s to %s), and those installs bring EUR %s of "
             "12-month net revenue (range %s to %s)." % (_n(f["plan_installs"]), _n(pi[0]), _n(pi[1]),
                                                        _n(f["plan_revenue"]), _n(pv[0]), _n(pv[1])))
    L += ["", "### %s" % deliver.FILES["wb"], "",
          "The first sheet gives the bands: one row per channel with its band, return and payments per 100 installs, the "
          "whole plan's installs and revenue beneath, and a chart of the returns against the %.2f and %.2f lines; the "
          "sheets behind it hold the working, every figure's range and the simpler routes." % (lo, hi)]
    L += ["", "## Critical Components", ""]
    k = f["components"]
    L.append("1. The installs AppLovin Android bought in the year to 2 November 2025 made **%.1f payments on the monthly "
             "plan per 100 installs** in their first 12 months (range **%.1f to %.1f**)." % (
                 k["S1"]["value"], k["S1"]["band"][0], k["S1"]["band"][1]))
    L.append("2. The installs Meta iOS bought in the year to 2 November 2025 made **%.1f payments on the monthly plan per "
             "100 installs** in their first 12 months (range **%.1f to %.1f**)." % (
                 k["S2"]["value"], k["S2"]["band"][0], k["S2"]["band"][1]))
    L.append("3. The plan's 2027 spend buys **%s installs** (range **%s to %s**)." % (
        _n(k["S3"]["value"]), _n(k["S3"]["band"][0]), _n(k["S3"]["band"][1])))
    L += ["", "## Step-by-Step", ""]
    w, mv, dl, fm = f["check_web"], f["check_moves"], f["delivery"], f["forms"]
    al, me, gi = ch[A], ch[M], ch[GI]
    aa = f["check_android"][A]
    named = [ch[c]["named_pct"] for c in ch if "named_pct" in ch[c]]
    src = Q["sources"]
    ho = f["holdout"]["every_fourth_week"]
    cad = f["policy"]["cadence_days"]
    cv = f["conventions"]
    gm = mv["channels"][GI]
    steps = [
        "Kept the %s consumer accounts of `%s` (%d staff and test accounts out) and the production charges of `%s` (a "
        "re-sent checkout row counted once, the %s refunded purchases taken out on the day they were charged); took each "
        "account's install row and channel from `%s` (re-sent rows and reinstalls dropped) and counted each iOS network's "
        "installs from `%s`, one per postback with redownloads and twice-delivered postbacks out, in the market its "
        "campaign runs in (the `country` of `%s`), on an install day three days before the postback arrived for half of "
        "each postback and four days for the other half (`%s` sends it 24 to 48 hours after the 48-hour window closes); "
        "a half dated before 4 November 2024 is counted in the week of 4 November 2024 (%s installs in all)." % (
            _n(s["consumer_accounts"]), F["acc"], s["other_accounts"], F["bill"], _n(s["refunded_purchases"]), F["attr"],
            F["skan"], F["spend"], F["schema"], _n(s["early_postback_installs"])),
        "Valued every charge at its transaction time under `%s` (VAT by storefront, the stores' %d per cent, the "
        "checkout's %d per cent) and summed each account's %d days from its `created_at`, which also sets its install "
        "week; the %d install weeks from 4 November 2024 to 2 November 2025 have their twelve months on file. A payment "
        "on the monthly plan is any charge of the EUR %.2f plan in those %d days, on either store or the web checkout: "
        "the first, at the trial's end, is a `first_charge` of the plan in the billing events and the web settlements "
        "count the web plan's charges as `payments` (policy 2.3 and 2.5). Counting the window as twelve months of %s "
        "days, or counting refunded charges, puts AppLovin Android at %.1f and %.1f, inside its range; leaving out the "
        "trial-end charge or the web checkout's (%.1f and %.1f) counts fewer payments than the plan's subscribers made." % (
            F["policy"], f["policy"]["commission_pct"], f["policy"]["fee_pct"], s["days"], s["mature_weeks"],
            f["policy"]["monthly"], s["days"], cad, cv["months_365_25"]["pay100"][A], cv["refunds_counted"]["pay100"][A],
            cv["first_left_out"]["pay100"][A], cv["web_left_out"]["pay100"][A]),
        "Set `%s` and `%s` against the billing events by store and by period of %s days counted from 4 November 2024 "
        "(the App Store's charges on its report's Pacific days): Google Play reports %s renewals against %s in the records "
        "and the App Store %s against %s, so %s and %s renewals were never taken in, with %s and %s first monthly charges "
        "and %s and %s annual first charges." % (
            F["google"], F["apple"], cad, _n(gp["store_renewals"]), _n(gp["recorded_renewals"]),
            _n(ap["store_renewals"]), _n(ap["recorded_renewals"]), _n(gp["renewal_excess"]), _n(ap["renewal_excess"]),
            _n(gp["first_excess"]), _n(ap["first_excess"]), _n(gp["annual_excess"]), _n(ap["annual_excess"])),
        "The excess sits on store subscriptions the app last saw still set to renew: monthly subscriptions with a charge "
        "on file whose next charge fell after the day of the account's last open and by 8 November 2026 (%s on Google "
        "Play, %s on the App Store; a subscription's charges fall %s days apart counted from its first, each rounded to "
        "the day), and trials last seen unconverted with auto-renew on and no charge on file (%s monthly and %s annual on "
        "Google Play, %s and %s on the App Store). The share of those trials charged at the trial's end, on day 7, is the "
        "stores' first charges beyond the records over them (monthly %.3f and %.3f, annual %.3f and %.3f), kept as that "
        "average for each store and plan and spread across the trials in proportion to the share that bought among the "
        "store's trial starters of the same first-48-hour sessions level (the conversion value's sessions bucket in four "
        "pairs) whose outcome the records hold: a first charge on file, an open on or after day 7, or auto-renew off; a "
        "trial starter with no subscription at its last open counts to its platform's store. The monthly continuation of a subscription nobody opens was fitted by "
        "least squares to the stores' renewals beyond the records, period by period over every period but the last, "
        "which the pull cuts short: a subscription's j-th charge after its last one on file, %s times j days on and "
        "rounded to the day, counts the continuation to the power j in the period it falls in, and a monthly trial's j-th "
        "renewal after day 7 the store's monthly share charged times the same power. It is %.3f on Google Play and %.3f "
        "on the App Store, and each such account's expected charges inside its %d days and by 8 November 2026 were added. "
        "AppLovin Android's installs of the year to 2 November 2025 made %.1f payments on the monthly plan per 100 "
        "installs against %.1f in the records (EUR %.2f of 12-month net revenue per install against %.2f), and the "
        "records as they stand put its return at %.3f, a cut. On the %d monthly web-checkout subscribers among those "
        "installs who had been charged by their last open and were last seen set to renew, whose every charge is on "
        "file, EUR %.2f each was charged after the last open inside the twelve months; the same fit run on the web "
        "checkout's own record (its %s monthly subscribers charged by their last open and last seen set to renew) gives "
        "a continuation of %.3f and puts %.2f on those %d, and the scaling puts %.2f (each of their charges up to the "
        "last open raised by Google Play's first monthly charges and renewals over the recorded ones in the charge's "
        "period, less one)." % (
            _n(gp["renewal_candidates"]), _n(ap["renewal_candidates"]), cad,
            _n(gp["trial_candidates_monthly"]), _n(gp["trial_candidates_annual"]), _n(ap["trial_candidates_monthly"]),
            _n(ap["trial_candidates_annual"]), gp["trial_end_share_monthly"], ap["trial_end_share_monthly"],
            gp["trial_end_share_annual"], ap["trial_end_share_annual"], cad, gp["continuation"], ap["continuation"],
            s["days"], al["pay100"], al["recorded_pay100"], al["paid_per_install"], al["recorded_per_install"],
            R["S1"][A]["return_plan"], w["subscribers"], w["charged"], _n(w["fit_subscribers"]), w["web_rate"],
            w["estimate"], w["subscribers"], w["true_up"]),
        "The attribution export names %.1f to %.1f per cent of an iOS network's installs. For each market, install week "
        "and first-48-hour value, a network's unnamed installs are its postbacks less its named installs, and what is "
        "left of the accounts with no channel is organic: over the %d weeks %s such accounts paid EUR %s, %s of them the "
        "five networks' and %s organic. Priced each source's unnamed installs at its named installs' 12-month net revenue "
        "at the same first-48-hour value (a value with fewer than %d named installs of the source takes all named "
        "installs' figure there, scaled by the source's own level), and fitted one ratio per source by least squares "
        "across the %d market-weeks, each weighted by one over its accounts with no channel, so that the priced installs "
        "add up to what those accounts paid: Meta %.3f, TikTok %.3f, Snapchat %.3f, Google %.3f, Pinterest %.3f and "
        "organic %.3f. The payments per 100 installs come from the same fit run on the monthly payments themselves (Meta "
        "%.3f, Google %.3f); the revenue ratios carried onto the payments would price the accounts with no channel at "
        "%.3f times the monthly payments they made, against %.3f, and put Meta iOS at %.1f. Meta iOS's installs of the year made %.1f payments on "
        "the monthly plan per 100 installs. The simpler way fits each network's declined installs' chance of paying on "
        "the pool and shifts their revenue per payer by the gap the fully named channels show: it puts Meta iOS at %.1f "
        "and a return of %.3f, a scale, and prices the accounts with no channel at %.3f times what they paid; valued "
        "like the named installs they come to %.3f. On Android, where the export names every install, AppLovin "
        "Android's %s installs that declined tracking paid EUR %.2f each, the same fit with their channel set aside "
        "gives %.2f and the value of its installs that allowed tracking %.2f." % (
            min(named), max(named), s["mature_weeks"], _n(Q["pool"]["accounts"]), _n(Q["pool"]["paid"]),
            _n(Q["pool"]["network_installs"]), _n(Q["pool"]["organic_installs"]), s["thin_cell"], Q["pool"]["market_weeks"],
            src[M]["ratio"], src["TikTok iOS"]["ratio"], src["Snapchat iOS"]["ratio"], src[GI]["ratio"],
            src["Pinterest iOS"]["ratio"], src["organic iOS"]["ratio"], src[M]["ratio_payments"], src[GI]["ratio_payments"],
            Q["payments_adding_up"]["revenue_ratios"], Q["payments_adding_up"]["payment_ratios"], Q["payments_at_revenue_ratios"][M], me["pay100"],
            R["S2"][M]["pay100"], R["S2"][M]["return_plan"], Q["adding_up"]["borrowed_shift"], Q["adding_up"]["named"],
            _n(aa["installs"]), aa["paid"], aa["fitted"], aa["named"]),
        "Regressed the log of each week's installs and of its value per install on the log of the week's budget (`%s`) "
        "and the log of the share of it the platform billed (`%s` over the budget), each channel of the records with its "
        "own level and slopes and one month pattern shared by all of them, Apple Search Ads included, over the %d weeks. "
        "A week takes the month of its Thursday, as the plan's blocks do, and its value per install prices its installs "
        "by first-48-hour value at what that value was worth over the %d weeks with twelve months on file (for an iOS "
        "network, what its named and unnamed installs of that value came to together under step 5). Fitted on "
        "billed spend instead, the fit passes a hold-out of every fourth week (it misses the held-out installs by %.1f "
        "per cent, the budget alone by %.1f), but over the %d weeks of the %d moves the team logged, each move left out "
        "of the fit in turn, it misses the installs by %.1f per cent and the fit on the budget by %.1f; on Google iOS the "
        "installs of the raised weeks over those of the lowered weeks were %.3f, the budget fit gives %.3f and the spend "
        "fit %.3f. Every plan channel's value per install falls with the budget (slopes %.2f to %.2f, each at least %.1f "
        "of its spreads below nought)." % (
            F["budget"], F["spend"], s["weeks"], s["mature_weeks"], ho["spend"], ho["budget"], mv["weeks"], mv["moves"],
            mv["missed_pct"]["spend"], mv["missed_pct"]["golden"], gm["actual"], gm["budget_fit"], gm["spend_fit"],
            fm["value_slope_range"][0], fm["value_slope_range"][1], fm["value_slope_spreads"]),
        "The growth sheet of `%s` gives each channel's weekly spend in euros \"as the platforms bill it\", and over the %d weeks "
        "the platforms billed %.1f to %.1f per cent of a channel's budgets (a whole budget in %d to %d weeks of %d, the "
        "best quarter %.1f to %.1f per cent). So each plan week was carried at the budget that bills it, the plan's spend "
        "over the channel's billed share of the %d weeks. Installs come from the installs equation's budget slope and "
        "month pattern, scaled so that those two terms alone, over the %d weeks, add up to the installs counted; value "
        "per install comes from the value equation's budget slope and month pattern, scaled so that over the %d complete "
        "weeks, weighted by installs, they give the channel's 12-month net revenue per install. The plan's EUR %s of "
        "spend buys %s installs, which bring EUR %s. Read as a budget billed in full, the same spend buys %s installs and "
        "Google iOS returns %.3f, a scale; that reading has the installs equation, run over the record's own budgets at "
        "a share of one, add up to %.1f to %.1f per cent of the installs counted." % (
            F["plan"], s["weeks"], 100 * dl["share"][0], 100 * dl["share"][1], dl["whole"][0], dl["whole"][1], s["weeks"],
            dl["best_quarter_pct"][0], dl["best_quarter_pct"][1], s["weeks"], s["weeks"], s["mature_weeks"],
            _n(f["plan_spend"]), _n(f["plan_installs"]), _n(f["plan_revenue"]), _n(R["S3"]["plan"]["installs"]),
            R["S3"][GI]["return_plan"], dl["adds_up_pct"][0], dl["adds_up_pct"][1]),
        "Placed each return against %.2f and %.2f: %s scale and %s hold." % (lo, hi, _list(b["scale"]), _list(b["hold"])),
    ]
    for i, t in enumerate(steps):
        L.append("%d. %s" % (i + 1, t))
    nv, nb = f["nearest_variant"], f["nearest_beside"]
    T = Q["share_tests"]
    mw = Q["market_week_miss_pct"]
    gr, ar = gp["rivals"], ap["rivals"]
    bs, ky = f["beside"], f["carry"]
    un, fr = bs["unrescaled"], bs["finer_rows"]
    thin = min(f["perturbations"], key=lambda p: p["nearest"])
    thin_c = min(thin["returns"], key=lambda c: min(abs(thin["returns"][c] - x) for x in (lo, hi)))
    names = f["single_variants"]
    assert f["family_calls_all_golden"]
    xr = f["crossed"]
    assert not xr["moved"], xr["moved"][:5]                        # no call moves on any single way or crossing
    sp = P["split_pack"]
    tk = P["ratio"]["TikTok iOS"]
    gk = P["ratio"]["Google iOS"]
    assert all(x < tk["pooled"] for x in tk["markets"]) and all(x > gk["pooled"] for x in gk["markets"]), (tk, gk)
    L += ["", "No other conclusion survives. Every other defensible way of taking the steps files the same seven bands, "
              "each taken singly (%s), and every way of crossing them: every two that can be taken together, one way of "
              "each step at once, and each of the four families below with every single way and every pair of the "
              "other two steps it can be taken with (%s more ways, %s in all). Each range above holds the span of their "
              "figures with %s per cent of the figure either side. The closest a single way comes to a line is %s at "
              "%.3f from it, and the closest of all the crossings %s at %.3f." % (
                  "; ".join(names), _n(xr["crossings"]), _n(xr["ways"]), f["band_pad_pct"], nv["channel"],
                  nv["distance"], xr["nearest"]["channel"], xr["nearest"]["distance"]),
          "",
          "Four more families stand beside those ways, and wherever one of them or one of its crossings moves a figure its "
          "range reaches %g per cent of the figure beyond it; alone, each files the same seven bands. The ratios fitted on each market-week's "
          "accounts split by their own first-48-hour sessions (weighted by one over the accounts, unweighted, or by the "
          "revenue the fit expects) put Meta iOS at %.1f to %.1f payments per 100 installs and its return at %.3f to "
          "%.3f, and TikTok iOS's return at %.3f to %.3f. The installs equation's own prediction at the plan, not scaled, "
          "with the share billed put in from outside (over the %d weeks, the first %d or the last %d; as that one share "
          "or week by week) puts AppLovin Android between %.3f and %.3f and the plan's installs at %s to %s; each adds up "
          "to between %.1f and %.1f per cent of every channel's installs counted over the weeks its share is taken from, "
          "while the geometric mean and the median week's share fall %.1f to %.1f per cent short of some channel's. The "
          "nearest of these ways to a line is %s at %.3f from it." % (
              f["beside_pad_pct"], fr["pay100"][M][0], fr["pay100"][M][1], fr["return_plan"][M][0],
              fr["return_plan"][M][1], fr["return_plan"]["TikTok iOS"][0], fr["return_plan"]["TikTok iOS"][1],
              s["weeks"], s["mature_weeks"], s["weeks"] - s["mature_weeks"], un["return_span"][A][0],
              un["return_span"][A][1], _n(min(un["installs"])), _n(max(un["installs"])), ky["held_pct"][0],
              ky["held_pct"][1], ky["refused_short_pct"][0], ky["refused_short_pct"][1], nb["channel"], nb["distance"]),
          "",
          "Each simpler way of taking a step is refuted by a figure from the files, and each files a wrong band with the "
          "other two steps as estimated. The stores' excess: the records as they stand (AppLovin Android %.3f); each "
          "recorded charge raised by its store's charges over the recorded ones period by period (%.3f) or over the "
          "whole record (%.3f), which puts EUR %.2f and %.2f on the web checkout's subscribers against the %.2f they were "
          "charged; the candidates carried at the web checkout's continuation (%.3f; AppLovin Android %.3f) or at one "
          "less the cancellations the app saw per charge on file (%.3f and %.3f; TikTok iOS %.3f), which take in %s and "
          "%s, and %s and %s, of the stores' %s and %s renewals beyond the records over the fitted periods, where the "
          "fitted continuations take in %s and %s. The unnamed installs: each network's declined installs at the gap the "
          "fully named channels show (Meta iOS %.3f), like its named installs of the same first-48-hour value (%.3f), at "
          "Apple Search Ads' ratio (%.3f), at the ratio its kind of network shows on Android (%.3f) or at one ratio for "
          "every source (%.3f): the accounts with no channel come to %.3f, %.3f and %.3f times what they paid on the "
          "first three, the five networks' fitted ratios stand %.1f from Apple Search Ads' ratio and %.1f from the "
          "Android ratios against a five per cent point of %.2f, and one ratio misses the market-weeks' revenue by %.1f "
          "per cent against %.1f. Sources sharing one ratio are refused by the fit's own test wherever it refuses them "
          "(the five networks %s; Meta with TikTok %s) and kept where it cannot (TikTok with Snapchat %s). The ratios "
          "fitted on the %d weeks with the three markets summed file TikTok iOS in scale (%.3f, its ratio %.3f) and "
          "Google iOS at %.3f (its ratio %.3f): each market's own weeks put TikTok's ratio at %s, every one under %.3f, "
          "and Google's at %s, every one over %.3f; priced market-week by market-week at the summed-markets ratios, the "
          "accounts with no channel come to %.3f of what they paid in the %d market-weeks TikTok iOS spent in and %.3f in "
          "the %d it did not (Google iOS %.3f and %.3f), where the 156-row ratios give %.3f to %.3f for every network's "
          "weeks; the summed-markets ratios stand %.1f from the 156-row fit's on %d degrees of freedom against %.2f. The "
          "response: fitted on billed spend (Google iOS %.3f) it fails on the moved weeks as step 6 shows, and the year "
          "to 2 November 2025's return carried over (%.3f) holds the weekly spend at that year's; a straight line or an "
          "exponential in the budget is refused when the fitted form's term is added channel by channel (F %.1f and "
          "%.1f against %.2f, where the budget added to the fitted form gives %.1f). The plan's spend read as a budget "
          "billed in full, in the fit's own prediction (Google iOS %.3f) or scaled to the installs on record (AppLovin "
          "Android %.3f), is refused by the plan's own header and by the record's billed shares (step 7)." % (
              sc["as_recorded"]["return_plan"][A], sc["by_period"]["return_plan"][A], sc["one_factor"]["return_plan"][A],
              w["true_up"], w["true_up_one_factor"], w["charged"], gr["web"]["rate"], sc["web_rate"]["return_plan"][A],
              gr["seen"]["rate"], ar["seen"]["rate"], sc["seen_rate"]["return_plan"]["TikTok iOS"],
              _n(gr["web"]["takes_in"]), _n(ar["web"]["takes_in"]), _n(gr["seen"]["takes_in"]), _n(ar["seen"]["takes_in"]),
              _n(gp["renewal_excess_fitted_periods"]), _n(ap["renewal_excess_fitted_periods"]),
              _n(gr["fitted"]["takes_in"]), _n(ar["fitted"]["takes_in"]),
              sc["borrowed_shift"]["return_plan"][M], sc["named_by_cell"]["return_plan"][M], sc["search_ads"]["return_plan"][M],
              sc["android"]["return_plan"][M], sc["one_ratio"]["return_plan"][M], Q["adding_up"]["borrowed_shift"],
              Q["adding_up"]["named"], Q["adding_up"]["search_ads"], Q["lent"]["search_ads"]["stat"],
              Q["lent"]["android"]["stat"], Q["lent"]["search_ads"]["point"], mw["one_ratio"], mw["fitted"],
              _two(T["the five networks"]), _two(T["Meta and TikTok"]), _two(T["TikTok and Snapchat"]),
              s["mature_weeks"], P["return_plan"]["TikTok iOS"], tk["pooled"], P["return_plan"][GI], gk["pooled"],
              _list("%.3f" % x for x in tk["markets"]), tk["pooled"], _list("%.3f" % x for x in gk["markets"]),
              gk["pooled"], sp["TikTok iOS"]["pooled"][0], sp["TikTok iOS"]["live"], sp["TikTok iOS"]["pooled"][1],
              sp["TikTok iOS"]["dark"], sp[GI]["pooled"][0], sp[GI]["pooled"][1], P["golden_split_pack_range"][0],
              P["golden_split_pack_range"][1], P["wald"], P["wald_df"], P["wald_point"],
              sc["on_spend"]["return_plan"][GI], sc["last_year"]["return_plan"][GI], fm["line"], fm["exponential"],
              fm["point"], fm["power"], sc["full_delivery"]["return_plan"][GI], sc["full_delivery_rescaled"]["return_plan"][A]),
          "",
          "The three steps are independent. With the stores' excess alone taken the simpler way the bands are the same but "
          "for %s; with the unnamed installs alone, but for %s; with the plan's spend alone, but for %s. With two of them "
          "taken the simpler way (%s; %s; %s) and with all three (%s), the bands move further, %d different wrong sets of "
          "bands in all, and each step's own figure moves with that step alone: AppLovin Android's payments per 100 "
          "installs stay at %.1f when the unnamed installs or the plan's spend are taken the simpler way, Meta iOS's stay "
          "inside their range at %.1f when the stores' excess is and at %.1f when the plan's spend is, and the plan's %s "
          "installs stay where they are with either of the other two. "
          "The bands also stand with the stores' fitted rates, each source's ratio by two of its standard errors and each "
          "channel's two budget slopes moved a fifth either way, and with the budget that bills the plan's spend moved by "
          "the %.1f per cent that the billed share's widest quarter departs from the %d-week share on any channel: the "
          "thinnest of those is %s at %.3f." % (
              _list(_moved(f, "S1")), _list(_moved(f, "S2")), _list(_moved(f, "S3")), _list(_moved(f, "S1+S2")),
              _list(_moved(f, "S1+S3")), _list(_moved(f, "S2+S3")), _list(_moved(f, "S1+S2+S3")), f["distinct_wrong_calls"],
              R["S2"][A]["pay100"], R["S1"][M]["pay100"], R["S3"][M]["pay100"], _n(f["plan_installs"]), f["delivery_share_spread_pct"],
              s["weeks"], thin_c, thin["returns"][thin_c])]
    # each step's own figure untouched by the other two steps' simpler ways
    assert R["S2"][A]["pay100"] == R["S3"][A]["pay100"] == f["pay100"][A], R
    assert R["S3"][M]["pay100"] == f["pay100"][M], R
    assert R["S1"]["plan"]["installs"] == R["S2"]["plan"]["installs"] == f["plan_installs"], R
    assert f["pay100_band"][M][0] <= R["S1"][M]["pay100"] <= f["pay100_band"][M][1], R["S1"][M]
    open(path, "w").write("\n".join(L) + "\n")
