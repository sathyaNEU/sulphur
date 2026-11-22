"""submission.md: the tags and the four answer blocks, every figure from figures.json; once the platform's two
responses are on file under runs/, the answer to the form's stump question as well, first after the recommendation."""
import os

import deliver
import docs
import pack

F = dict(pack.FILES)
F.update(docs.FILES)
LETTERS = "abcdefghijklmnopqrstuvwxyz"
ND = {"return ": 3, "stretch return ": 3, "installs a week ": 0, "value at plan ": 2, "next euro ": 3,
      "stretch next euro ": 3, "paid per install ": 2}
# the simpler ways the closing passage says file a wrong band, and the one it says leaves the bands as they are
WRONG = ("by_period", "one_factor", "seen_rate", "web_rate", "named_by_cell", "search_ads", "android", "one_ratio",
         "organic_pinned", "pool_value", "four_social", "on_spend", "last_year")
SAME = ("three_social",)
RUNS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "runs")
STUMP = "How is each model stumped?"
# The platform's two responses to this cut under the prompt as reworded (runs/rerun1.md and runs/rerun2.md, pasted by
# the author on 2026-11-21; the pair from before the rewording stays in runs/run1.md and runs/run2.md): the figures and
# the words the stump block takes from them, each exactly as the response writes it. checks.py finds every one of them
# in the response's own text.
RESPONSES = {
    1: dict(file="rerun1.md",
            returns={"Meta iOS": "1.0160", "Google Android": "0.8154", "AppLovin Android": "0.6183"},
            paid={"Meta iOS": "5.65", "TikTok iOS": "3.83", "Snapchat iOS": "4.93", "Google iOS": "8.56",
                  "Pinterest iOS": "7.46", "Google Android": "6.61", "AppLovin Android": "3.13"},
            installs={"Meta iOS": "780.54", "TikTok iOS": "745.84", "Snapchat iOS": "636.16", "Google iOS": "621.28",
                      "Pinterest iOS": "326.88", "Google Android": "608.91", "AppLovin Android": "914.54"},
            counts=("1,190",),
            words=("inspected but not used", "transaction-level billing is the policy source for net revenue",
                   "fit a mixture model for nonauthorized conversion",
                   "rejected because actual ratios average 0.83-0.87 and plan text fixes billed spend, not budget",
                   "Place Google iOS and Pinterest iOS in Scale; Meta iOS in Hold; TikTok iOS, Snapchat iOS, Google "
                   "Android and AppLovin Android in Cut", "One common iOS status gap: rejected")),
    2: dict(file="rerun2.md",
            returns={"Meta iOS": "1.074", "Google Android": "0.977", "AppLovin Android": "0.754"},
            paid={"Meta iOS": "5.105", "AppLovin Android": "3.136"},
            installs={"Meta iOS": "892.72", "TikTok iOS": "863.13", "Snapchat iOS": "723.03", "Google iOS": "727.28",
                      "Pinterest iOS": "395.62", "Google Android": "719.02", "AppLovin Android": "1,072.57"},
            counts=("748,034",),
            words=("aggregate store reports, not account charges", "at delivery ratio 1.00",
                   "a judgment call, not a fact in the data", "falls below 0.90 and would be Cut",
                   "Place Google iOS and Pinterest iOS in Scale; Meta iOS and Google Android in Hold; TikTok iOS, "
                   "Snapchat iOS and AppLovin Android in Cut", "with organic as a separate component")),
}


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _n(x):
    return format(int(x), ",")


def _v(f, fam, c):
    """a stated figure with its range"""
    nd = ND[fam]
    x = f["figure"][fam + c]
    lo, hi = f["figure_band"][fam + c]
    if nd == 0:
        return "%d (%d to %d)" % (x, lo, hi)
    return "%.*f (%.*f to %.*f)" % (nd, x, nd, lo, nd, hi)


def _moved(f, key):
    """the channels a route files in another band, each with its return"""
    r = f["routes"][key]
    return ["%s %s (%.3f)" % (c, r[c]["band"], r[c]["return_plan"]) for c in deliver.order(f) if r[c]["band"] != f["bands"][c]]


def quoted(r):
    """every string the stump block takes from one response"""
    return (list(r["returns"].values()) + list(r["paid"].values()) + list(r["installs"].values()) + list(r["counts"])
            + list(r["words"]) + list(r.get("factors", ())))


def _x(t):
    return float(t.replace(",", ""))


def _stumped(f):
    """The form's stump question, answered from the two responses on file; nothing until they are."""
    if not os.path.exists(os.path.join(RUNS_DIR, RESPONSES[1]["file"])):
        return []
    r1, r2 = RESPONSES[1], RESPONSES[2]
    rp, s, sc, ch, st, Q, w = (f["return_plan"], f["steps"], f["shortcuts"], f["channels"], f["stores"], f["ratios"],
                               f["check_web"])
    fg, fb = f["figure"], f["figure_band"]
    lo, hi = f["policy"]["lines"]
    chans = deliver.order(f)
    band = lambda x: "scale" if x >= hi else ("hold" if x >= lo else "cut")   # noqa: E731
    inside = lambda k, x: fb[k][0] <= _x(x) <= fb[k][1]                       # noqa: E731
    A, G, M = "AppLovin Android", "Google Android", "Meta iOS"
    pa, pg, pm, ig = "paid per install " + A, "paid per install " + G, "paid per install " + M, "installs a week " + G
    assert all(f["bands"][c] == "hold" for c in (A, G, M))
    assert [band(_x(r1["returns"][c])) for c in (M, G, A)] == ["hold", "cut", "cut"]
    assert [band(_x(r2["returns"][c])) for c in (M, G, A)] == ["hold", "hold", "cut"]
    # the first response: the stores' charges lost, the other two steps' figures inside their ranges
    assert not inside(pa, r1["paid"][A]) and inside(pm, r1["paid"][M]) and inside(ig, r1["installs"][G])
    # the missing charges run through its figures: every channel but Meta iOS pays under its range
    low = [c for c in chans if _x(r1["paid"][c]) < fb["paid per install " + c][0]]
    assert len(chans) == 7 and low == [c for c in chans if c != M], low
    raw = sc["as_recorded"]
    assert raw["channel"] == A and G in raw["wrong"] and raw["components_kept"] == ["S3"]
    assert "%.2f" % raw["paid_per_install"] == r1["paid"][A]
    # the second: the stores' charges and the carry to the plan lost, its Meta iOS figure under the range
    assert not inside(pa, r2["paid"][A]) and _x(r2["paid"][M]) < fb[pm][0]
    over = [100.0 * (_x(r2["installs"][c]) / fg["installs a week " + c] - 1) for c in chans]
    gb = fb[ig]
    assert min(over) > 0 and _x(r2["installs"][G]) > gb[1]
    assert (_n(s["refunded_purchases"]), _n(s["consumer_accounts"])) == (r1["counts"][0], r2["counts"][0])
    for k in ("by_period", "named_by_cell", "search_ads", "pool_value", "on_spend"):
        assert sc[k]["channel"] in sc[k]["wrong"], k
    share = [100.0 * ch[c]["delivery_share"] for c in chans]
    named = [ch[c]["named_pct"] for c in ch if "named_pct" in ch[c]]
    gp, ap = st["Google Play"], st["App Store"]
    p1 = (
        "**Response 1** files Google Android and AppLovin Android as cut (%s and %s where they are holds at %.3f and "
        "%.3f), both through one step, and makes the other two. It took the billing events as they stand: the stores' "
        "reports were \"%s\" because \"%s\", so AppLovin Android's installs of the year to 2 November 2025 pay EUR %s "
        "each against %.2f (the reference's own estimators give the same %.2f on the billing events as they stand) and "
        "Google Android's EUR %s against %.2f. On the unnamed installs it \"%s\" with a gap for each network, and Meta "
        "iOS's installs of that year pay EUR %s each against %.2f (range %.2f to %.2f). It fitted installs on the "
        "budget with the delivery beside it and carried the plan at the delivery the record shows (full delivery "
        "\"%s\"): Google Android's plan spend buys %s installs a week against %d (range %d to %d)." % (
            r1["returns"][G], r1["returns"][A], rp[G], rp[A], r1["words"][0], r1["words"][1], r1["paid"][A], fg[pa],
            raw["paid_per_install"], r1["paid"][G], fg[pg], r1["words"][2], r1["paid"][M], fg[pm], fb[pm][0], fb[pm][1],
            r1["words"][3], r1["installs"][G], fg[ig], gb[0], gb[1]))
    p2 = (
        "**Response 2** files AppLovin Android as cut (%s where it is a hold at %.3f) and loses two steps. It set the "
        "stores' reports aside the same way (\"%s\"), so AppLovin Android's installs of that year pay EUR %s each "
        "against %.2f. It fitted the response on the budget with the delivery beside it, then priced the plan \"%s\" "
        "where the platforms billed %.0f to %.0f per cent of the budgets, called this \"%s\" and kept the delivery the "
        "record shows as a sensitivity under which Google Android \"%s\". Its hold on Google Android (%s against %.3f) "
        "therefore rests on two errors that offset: the missing store charges, and installs that run %.0f to %.0f per "
        "cent high on every channel (Google Android %s a week against %d, range %d to %d). It separated the unnamed "
        "installs by source (\"%s\"); its Meta iOS figure (EUR %s against %.2f) sits under the range of %.2f to %.2f, "
        "as the reference's own fit does on the billing events as they stand." % (
            r2["returns"][A], rp[A], r2["words"][0], r2["paid"][A], fg[pa], r2["words"][1], min(share), max(share),
            r2["words"][2], r2["words"][3], r2["returns"][G], rp[G], min(over), max(over), r2["installs"][G], fg[ig],
            gb[0], gb[1], r2["words"][5], r2["paid"][M], fg[pm], fb[pm][0], fb[pm][1]))
    p3 = (
        "**Why it is fair.** Nothing is planted and nothing rests on a sentence in a file. Both responses cleaned the "
        "files to the reference's own counts (Response 1 finds the same %s refunds, Response 2 the same %s consumer "
        "accounts) and took the growth policy's rates, windows and lines as written; they went wrong afterwards, in "
        "estimation. "
        "Each of the three problems is how the records come to be and runs through every channel, not only the one it "
        "decides: the stores' unrecorded charges are %.1f to %.1f per cent of a channel's 12-month net revenue, the "
        "attribution export names %.1f to %.1f per cent of an iOS network's installs, and the platforms billed %.0f to "
        "%.0f per cent of a channel's budgets over the %d weeks. Each shows when two of the files are set side by side "
        "(Google Play reports %s renewals against %s in the billing events, the App Store %s against %s), and the "
        "responses found most of the evidence unprompted: both measured what the platforms delivered of each budget "
        "and saw that the installs the export names pay more than the rest, and both opened the stores' reports, "
        "though neither reports setting their totals beside the billing events." % (
            r1["counts"][0], r2["counts"][0], f["unrecorded_pct"]["low"], f["unrecorded_pct"]["high"],
            min(named), max(named), min(share), max(share), s["weeks"], _n(gp["store_renewals"]),
            _n(gp["recorded_renewals"]), _n(ap["store_renewals"]), _n(ap["recorded_renewals"])))
    p4 = (
        "**Why it takes rigour.** Seeing a problem does not give its figure. With the stores' excess in view, the obvious "
        "repair raises the recorded charges to the stores' totals period by period, and it still cuts AppLovin Android "
        "(%.3f): on the channel's web-checkout subscribers, whose every charge is on file, it puts EUR %.2f where %.2f was "
        "charged after the last open, because the excess belongs to subscribers who stopped opening the app; placing it "
        "takes a continuation fitted to the excess period by period and carried account by account. Valuing the unnamed "
        "installs like the named ones, at Apple Search Ads' ratio or at what the accounts with no channel paid all "
        "scale Meta iOS (%.3f, %.3f and %.3f); only one ratio per source, fitted together across the %d market-weeks, "
        "tells Meta (%.3f) from Google (%.3f), and it took Response 1 a fitted mixture to land inside the range. A "
        "response fitted on weekly spend beats the budget alone on held-out weeks and still cuts Google Android (%.3f), "
        "and the budget fit still has to be carried to the plan at what the platforms deliver of a budget, which "
        "Response 2 computed and set aside. The three steps are independent, each alone moving a different channel "
        "across a line: Response 1 lost the first and kept the other two steps' figures inside their ranges, Response 2 "
        "lost the first and the third." % (
            sc["by_period"]["return_plan"], w["true_up"], w["charged"], sc["named_by_cell"]["return_plan"],
            sc["search_ads"]["return_plan"], sc["pool_value"]["return_plan"], Q["pool"]["market_weeks"],
            Q["sources"]["Meta iOS"]["ratio"], Q["sources"]["Google iOS"]["ratio"], sc["on_spend"]["return_plan"]))
    return ["", "## " + STUMP, "", p1, "", p2, "", p3, "", p4]


def _two(t):
    """a test of sources sharing one ratio under both readings of the fit's spread, against its five per cent point"""
    return "%.1f and %.1f against %.2f" % (t["stat"], t["stat_one_variance"], t["point"])


def write(path, f):
    chans = deliver.order(f)
    b = f["by_band"]
    rp, R = f["return_plan"], f["routes"]
    ch, st, Q = f["channels"], f["stores"], f["ratios"]
    gp, ap = st["Google Play"], st["App Store"]
    lo, hi = f["policy"]["lines"]
    s, sc = f["steps"], f["shortcuts"]
    for k in WRONG:
        assert sc[k]["channel"] in sc[k]["wrong"], (k, sc[k])
    for k in SAME:
        assert not sc[k]["wrong"], (k, sc[k])
    L = ["# task1 answer blocks", "", "## Tags", "",
         "**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer lifetime value).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "", "## Final Recommendation", ""]
    L.append(
        "**Scale %s, hold %s and cut %s for 2027**: at the plan's weekly spend the returns are %s euros of 12-month net "
        "revenue per euro of spend, against the growth policy's lines of %.2f and %.2f. This rejects scaling Meta iOS (%.3f) "
        "and cutting Google Android (%.3f) and AppLovin Android (%.3f), the bands filed when the billing records are trued up "
        "to the stores' reports period by period, every install postback is valued like the installs the attribution export "
        "names and the response is fitted on weekly spend: the stores' excess belongs to subscriptions whose owners stopped "
        "opening the app, the installs the export cannot name are worth a different fraction of the named ones on each "
        "network, and a week's spend moves with what the platform delivered of the budget, not with the budget." % (
            _list(b["scale"]), _list(b["hold"]), _list(b["cut"]), _list("%s %.3f" % (c, rp[c]) for c in chans), lo, hi,
            R["S1+S2+S3"]["Meta iOS"]["return_plan"], R["S1+S2+S3"]["Google Android"]["return_plan"],
            R["S1+S2+S3"]["AppLovin Android"]["return_plan"]))
    L += _stumped(f)
    L += ["", "## Supplementary Questions", "", "### %s" % deliver.FILES["wb"], ""]
    L.append("First sheet: one row per channel of the plan's growth sheet with its band and the seven figures of entries 1 "
             "to 4 below, and a chart of each channel's return at the plan's and the stretch spend against the %.2f and "
             "%.2f lines." % (lo, hi))
    L += ["", "### %s" % deliver.FILES["csv"], ""]
    L.append("Seven rows, one per channel, highest return first: the band and the seven figures of entries 1 to 4. Each "
             "figure's range is in brackets.")
    L.append("")
    L.append("1. Return in 2027 at the plan's weekly spend and at its stretch spend, in euros of 12-month net revenue per "
             "euro of spend:")
    for i, c in enumerate(chans):
        L.append("   %s. %s (%s): %s at the plan's weekly spend and %s at the stretch spend." % (
            LETTERS[i], c, f["bands"][c], _v(f, "return ", c), _v(f, "stretch return ", c)))
    L.append("2. Installs a week the plan's spend buys, and the 12-month net revenue per install of those installs, in "
             "euros:")
    for i, c in enumerate(chans):
        L.append("   %s. %s: %s installs a week, EUR %s per install." % (
            LETTERS[i], c, _v(f, "installs a week ", c), _v(f, "value at plan ", c)))
    L.append("3. What one more euro returns on top of the plan's weekly spend and on top of the stretch spend, in euros of "
             "12-month net revenue:")
    for i, c in enumerate(chans):
        L.append("   %s. %s: %s on top of the plan's weekly spend and %s on top of the stretch spend." % (
            LETTERS[i], c, _v(f, "next euro ", c), _v(f, "stretch next euro ", c)))
    L.append("4. The 12-month net revenue per install of the installs each channel bought in the year to 2 November 2025, "
             "in euros:")
    for i, c in enumerate(chans):
        L.append("   %s. %s: EUR %s." % (LETTERS[i], c, _v(f, "paid per install ", c)))
    L += ["", "## Critical Components", ""]
    k = f["components"]
    L.append("1. The installs AppLovin Android bought in the year to 2 November 2025 went on to pay **EUR %.2f** of 12-month "
             "net revenue per install (range **%.2f to %.2f**)." % (k["S1"]["value"], k["S1"]["band"][0], k["S1"]["band"][1]))
    L.append("2. The installs Meta iOS bought in the year to 2 November 2025 went on to pay **EUR %.2f** of 12-month net "
             "revenue per install (range **%.2f to %.2f**)." % (k["S2"]["value"], k["S2"]["band"][0], k["S2"]["band"][1]))
    L.append("3. The plan's weekly spend on Google Android buys **%d installs a week** in 2027 (range **%d to %d**)." % (
        k["S3"]["value"], k["S3"]["band"][0], k["S3"]["band"][1]))
    L += ["", "## Step-by-Step", ""]
    w, mv = f["check_web"], f["check_moves"]
    ga, me, al = ch["Google Android"], ch["Meta iOS"], ch["AppLovin Android"]
    aa = f["check_android"]["AppLovin Android"]
    gm = mv["channels"]["Google Android"]
    named = [ch[c]["named_pct"] for c in ch if "named_pct" in ch[c]]
    src = Q["sources"]
    ho = f["holdout"]["every_fourth_week"]
    cad = f["policy"]["cadence_days"]
    steps = [
        "Kept the %s consumer accounts of `%s` (%d staff and test accounts out) and the production charges of `%s` (a re-sent "
        "checkout row counted once, the %s refunded purchases taken out on the day they were charged); took each account's "
        "install row and channel from `%s` (re-sent rows and reinstalls dropped) and counted each iOS network's installs "
        "from `%s`, one per postback with redownloads and twice-delivered postbacks out, in the market its campaign runs in "
        "(the `country` of `%s`), on an install day three days before the postback arrived for half of each postback and "
        "four days for the other half (`%s` sends it 24 to 48 hours after the 48-hour window closes); a half dated before 4 "
        "November 2024 is counted in the week of 4 November 2024 (%s installs in all)." % (
            _n(s["consumer_accounts"]), F["acc"], s["other_accounts"], F["bill"], _n(s["refunded_purchases"]), F["attr"],
            F["skan"], F["spend"], F["schema"], _n(s["early_postback_installs"])),
        "Valued every charge at its transaction time under `%s` (VAT by storefront, the stores' %d per cent, the checkout's "
        "%d per cent) and summed each account's %d days from its `created_at`, which also sets its install week; the %d "
        "install weeks from 4 November 2024 to 2 November 2025 have their twelve months on file." % (
            F["policy"], f["policy"]["commission_pct"], f["policy"]["fee_pct"], s["days"], s["mature_weeks"]),
        "Set `%s` and `%s` against the billing events by store and by period of %s days counted from 4 November 2024 (the "
        "App Store's charges on its report's Pacific days): Google Play reports %s renewals against %s in the records and "
        "the App Store %s against %s, so %s and %s renewals were never taken in, with %s and %s first monthly charges and "
        "%s and %s annual first charges." % (
            F["google"], F["apple"], cad, _n(gp["store_renewals"]), _n(gp["recorded_renewals"]),
            _n(ap["store_renewals"]), _n(ap["recorded_renewals"]), _n(gp["renewal_excess"]), _n(ap["renewal_excess"]),
            _n(gp["first_excess"]), _n(ap["first_excess"]), _n(gp["annual_excess"]), _n(ap["annual_excess"])),
        "The excess sits on store subscriptions the app last saw still set to renew: monthly subscriptions with a charge on "
        "file whose next charge fell after the day of the account's last open and by 8 November 2026 (%s on Google Play, "
        "%s on the App Store; a subscription's charges fall %s days apart counted from its first, each rounded to the "
        "day), and trials last seen unconverted with auto-renew on and no charge on file (%s monthly and %s annual on "
        "Google Play, %s and %s on the App Store). The share of those trials charged at the trial's end, on day 7, is the "
        "stores' first charges beyond the records over them (monthly %.3f and %.3f, annual %.3f and %.3f); it varies "
        "across them, keeping that average for each store and plan, in proportion to the share that bought among the "
        "store's trial starters of the same first-48-hour sessions level (the conversion value's sessions bucket in four "
        "pairs) whose outcome the records hold: a first charge on file, an open on or after day 7, or auto-renew off; a "
        "trial starter with no subscription at its last open counts to its platform's store. The "
        "monthly continuation of a subscription nobody opens was fitted by least squares to the stores' renewals beyond "
        "the records, period by period over every period but the last, which the pull cuts short: a subscription's j-th "
        "charge after its last one on file, %s times j days on and rounded to the day, counts the continuation to the "
        "power j in the period it falls in, and a monthly trial's j-th renewal after day 7 the store's monthly share "
        "charged times the same power. It is %.3f on Google Play and %.3f on the App Store, and each such account's expected charges inside "
        "its %d days and by 8 November 2026 were added at the net price. AppLovin Android's installs of the year to 2 "
        "November 2025 went on to pay EUR %.2f each against %.2f in the records. The simpler way raises each recorded "
        "monthly charge by its store's first monthly charges and renewals over the recorded ones in the charge's period, "
        "and each recorded annual charge by the store's annual first charges over the recorded ones in its period, which "
        "gives %.2f and a return of %.3f, a cut. On the %d monthly web-checkout subscribers among AppLovin Android's "
        "installs of the year to 2 November 2025 who had been charged by their last open and were last seen set to "
        "renew, whose every charge is on file, EUR %.2f each was charged after the last open inside the twelve months: "
        "the same fit run on the web checkout's own record (its %s monthly subscribers charged by their last open and "
        "last seen set to renew, of every "
        "channel and install week, their charges after the last open counted period by period and the last period left "
        "out) gives a continuation of %.3f and puts %.2f on those %d, and the scaling puts %.2f (each of "
        "their charges up to the last open raised by Google Play's first monthly charges and renewals over the recorded "
        "ones in the charge's period, less one)." % (
            _n(gp["renewal_candidates"]), _n(ap["renewal_candidates"]), cad,
            _n(gp["trial_candidates_monthly"]), _n(gp["trial_candidates_annual"]), _n(ap["trial_candidates_monthly"]),
            _n(ap["trial_candidates_annual"]), gp["trial_end_share_monthly"], ap["trial_end_share_monthly"],
            gp["trial_end_share_annual"], ap["trial_end_share_annual"], cad, gp["continuation"], ap["continuation"],
            s["days"],
            al["paid_per_install"], al["recorded_per_install"], al["true_up_per_install"],
            R["S1"]["AppLovin Android"]["return_plan"], w["subscribers"], w["charged"], _n(w["fit_subscribers"]),
            w["web_rate"], w["estimate"], w["subscribers"], w["true_up"]),
        "The attribution export names %.1f to %.1f per cent of an iOS network's installs. For each market, install week "
        "and first-48-hour value, a network's unnamed installs are its postbacks less its named installs, and what is "
        "left of the accounts with no channel is organic: over the %d weeks %s such accounts paid EUR %s, %s of them the "
        "five networks' and %s organic. Priced each source's unnamed installs at its named installs' 12-month net revenue "
        "at the same first-48-hour value (a value with fewer than %d named installs of the source takes all named "
        "installs' figure there, scaled by the source's own level), and fitted one ratio per source by least squares "
        "across the %d market-weeks, each weighted by one over its accounts with no channel, so that the priced installs "
        "add up to what those accounts paid: Meta %.3f, TikTok %.3f, Snapchat %.3f, Google %.3f, Pinterest %.3f and "
        "organic %.3f. Meta iOS's installs of the year went on to pay EUR %.2f each, against %.2f for its named installs. "
        "The simpler way values every postback like the named installs of the same first-48-hour value (Meta iOS %.2f, a "
        "return of %.3f, scale), which puts the accounts with no channel at %.2f times what they paid; on Android, where "
        "the export names every install, AppLovin Android's %s installs that declined tracking paid EUR %.2f each, the "
        "same fit with their channel set aside gives %.2f and the value of its installs that allowed tracking %.2f." % (
            min(named), max(named), s["mature_weeks"], _n(Q["pool"]["accounts"]), _n(Q["pool"]["paid"]),
            _n(Q["pool"]["network_installs"]), _n(Q["pool"]["organic_installs"]), s["thin_cell"], Q["pool"]["market_weeks"],
            src["Meta iOS"]["ratio"], src["TikTok iOS"]["ratio"], src["Snapchat iOS"]["ratio"], src["Google iOS"]["ratio"],
            src["Pinterest iOS"]["ratio"], src["organic iOS"]["ratio"], me["paid_per_install"], me["named_value"],
            me["named_price_per_install"], R["S2"]["Meta iOS"]["return_plan"], Q["adding_up"]["named"], _n(aa["installs"]),
            aa["paid"], aa["fitted"], aa["named"]),
        "Regressed the log of each week's installs and of its value per install on the log of the week's budget (`%s`) "
        "and the log of the share of it the platform spent (`%s` over the budget), each channel of the records with its "
        "own level and slopes and one month pattern shared by all of them, Apple Search Ads included, over the %d weeks. A "
        "week takes the month of its Thursday, as the plan's blocks do, and its value per install prices its installs by "
        "first-48-hour value at what that value was worth over the %d weeks with twelve months on file (for an iOS "
        "network, what its named and unnamed installs of that value came to together under step 5). Google Android's "
        "installs rise %.3f per cent for one per cent of budget, against %.3f when fitted on spend. The simpler way's fit "
        "on spend passes a hold-out of every fourth week (it misses the held-out installs by %.1f per cent, the budget "
        "alone by %.1f) and gives %d installs a week at the plan's spend and a return of %.3f, a cut; over the %d weeks "
        "of the %d moves the team logged, each move left out of the fit in turn, the fit on spend misses the installs by "
        "%.1f per cent and the fit on the budget by %.1f, and on Google Android the total installs of the %d raised weeks "
        "over the total installs of the %d lowered weeks were %.3f, the budget fit gives %.3f and the spend fit %.3f." % (
            F["budget"], F["spend"], s["weeks"], s["mature_weeks"], ga["budget_elasticity"], ga["spend_elasticity"],
            ho["spend"], ho["budget"], ga["installs_week_spend_fit"], R["S3"]["Google Android"]["return_plan"], mv["weeks"],
            mv["moves"], mv["missed_pct"]["spend"], mv["missed_pct"]["golden"], gm["raised"], gm["lowered"], gm["actual"],
            gm["budget_fit"], gm["spend_fit"]),
        "Carried each channel to the %d weeks of `%s` at the budget that delivers the plan's spend (the spend divided by "
        "the channel's spend over budget across the %d weeks). Installs come from the installs equation's budget slope "
        "and month pattern, scaled so that those two terms alone, over the %d weeks, add up to the installs counted (which "
        "leaves the share spent at its average effect over those weeks); value per install comes from the value "
        "equation's budget slope and month pattern, scaled so that over the %d complete weeks, weighted by installs, they "
        "give the channel's 12-month net revenue per install; then again with every week raised to the stretch column. "
        "One more euro returns the return at that spend times the sum of the two budget slopes, every week raised in the "
        "same proportion, on top of the plan's spend and on top of the stretch spend. Google Android's plan spend buys %d "
        "installs a week." % (
            s["plan_weeks"], F["plan"], s["weeks"], s["weeks"], s["mature_weeks"], f["installs_week"]["Google Android"]),
        "Placed each return against %.2f and %.2f: %s scale, %s hold, %s are cut." % (
            lo, hi, _list(b["scale"]), _list(b["hold"]), _list(b["cut"])),
    ]
    for i, t in enumerate(steps):
        L.append("%d. %s" % (i + 1, t))
    nv = f["nearest_variant"]
    T = Q["share_tests"]
    mw = Q["market_weeks"]
    gr, ar = gp["rivals"], ap["rivals"]
    thin = min(f["perturbations"], key=lambda p: p["nearest"])
    thin_c = min(thin["returns"], key=lambda c: min(abs(thin["returns"][c] - x) for x in (lo, hi)))
    mer = [p for p in f["perturbations"] if p["input"].startswith("Meta iOS")]
    # each step's own figure under the other steps' simpler ways: inside its range, and untouched where the step
    # does not reach it
    own = {k: {c: f["routes"][k][c]["paid_per_install"] for c in ("AppLovin Android", "Meta iOS")} for k in ("S1", "S2", "S3")}
    inside = lambda fam, c, x: f[fam + "_band"][c][0] <= x <= f[fam + "_band"][c][1]
    assert inside("paid_per_install", "Meta iOS", own["S1"]["Meta iOS"]), own
    assert own["S2"]["AppLovin Android"] == f["paid_per_install"]["AppLovin Android"], own
    assert all(own["S3"][c] == f["paid_per_install"][c] for c in own["S3"]), own
    assert all(f["routes"][k]["Google Android"]["installs_week"] == f["installs_week"]["Google Android"] for k in ("S1", "S2"))
    bs, ky, P, fm = f["beside"], f["carry"], Q["markets_pooled"], f["forms"]
    un, gd, vw = bs["unrescaled"], bs["grouped"], bs["value_weeks"]
    al_un = un["return_plan"]["AppLovin Android"]
    thin_un = min(al_un)
    y1 = {k: k + "_first_year" for k in ("at_share", "weekly_shares", "geometric_mean", "median_week")}
    assert s["early_postback_installs"] == int(s["early_postback_installs"])
    assert (bs["finer_rows"]["ways"], un["ways"], gd["ways"], vw["ways"]) == (6, 6, 4, 1), bs
    # the two forms kept file the seven bands whichever weeks the share is taken from; the thinnest of them is the
    # first year's share put in as one figure, and the two forms refused would cut AppLovin Android there
    assert all(not ky["wrong"][k] for k in ky["held"]), ky["wrong"]
    assert thin_un == ky["returns"][y1["at_share"]]["AppLovin Android"], (thin_un, ky["returns"][y1["at_share"]])
    assert all(ky["wrong"][y1[k]] == ["AppLovin Android"] for k in ("geometric_mean", "median_week")), ky["wrong"]
    assert ky["refused_short_pct"][0] > ky["held_short_pct"] + 1.0, ky
    assert not fm["line_wrong"]["levels"] and not fm["line_wrong"]["log"], fm["line_wrong"]
    # crossed with the battery, no way beside it moves a band; the nearest to a line is the unscaled twin of the
    # battery's own nearest way
    xr = f["crossed"]
    assert not xr["moved"] and xr["nearest"]["channel"] == "AppLovin Android" and xr["nearest"]["line"] == lo, xr["nearest"]
    assert ("not rescaled, at the last 52 weeks'" in xr["nearest"]["variant"]
            and xr["nearest"]["variant"].endswith("the budget alone, the delivery left out")), xr["nearest"]
    L += ["", "No other conclusion survives. Every other defensible way of taking the steps files the same seven bands, and "
              "each range above holds the span of their figures with %s per cent of the figure either side: each convention "
              "below taken singly, every two of them that can be taken together, and one for each step at once. For the "
              "stores' excess: one fit across both stores, a two-rate continuation, the fit without its last two periods, a "
              "30-day cadence, one share charged for every trial-end candidate, calendar months, the App Store's report days "
              "taken as UTC days, the refunds netted on the refund's day or from the renewals, the install clock taken from "
              "the attribution export's `install_time`. For the unnamed installs: the first-48-hour values in eight "
              "groups (the sessions bucket's four pairs, each with and without a trial or a purchase flagged) or in four "
              "(no trial below sessions bucket 3, no trial from it, a trial below sessions bucket 4, a trial from it or a "
              "purchase), cells of fifty or more, one tilt per source, the ratios fitted separately for lighter and heavier "
              "first-48-hour use, unweighted, by fortnight, by four-week period, weighted by one over the fitted revenue, with "
              "organic's ratio taken from Apple Search Ads, without market-weeks of fewer than a hundred accounts, drawn "
              "toward their pooled ratio, every postback dated back three days or four, and sources sharing one ratio "
              "wherever a five per cent test of their ratios being equal lets them, with the fit's spread taken row by row "
              "or with one variance for every row: Google with Pinterest, Google with organic, Pinterest with organic, "
              "those three, Meta with TikTok (%s) and TikTok with Snapchat (%s). For the response: each channel's own month "
              "pattern, without the launch quarter or on the last 78 weeks, the Android channels' value response fitted on "
              "the complete weeks' own 12-month net revenue per install, one value slope across channels, the delivery "
              "share from the complete weeks or the last 52, spend "
              "instrumented by the budget, the budget alone, a week's month taken from its Monday. The closest any comes "
              "to a line is %s at %.3f from it." % (
                  f["band_pad_pct"], _two(T["Meta and TikTok"]), _two(T["TikTok and Snapchat"]), nv["channel"], nv["distance"]),
          "",
          "Four more families were run as they stand, each way alone, and wherever one of them moves a figure the "
          "figure's range reaches %g per cent of the figure beyond it; each files the same seven bands. The ratios "
          "fitted on each market-week's accounts split "
          "by their own first-48-hour sessions (the eight sessions buckets or their four pairs; weighted by one over the "
          "accounts, unweighted, or by one over the fitted revenue) put Meta iOS's installs of the year at EUR %.2f to "
          "%.2f each and its return at %.3f to %.3f. The first-48-hour values grouped by the sessions bucket alone (its "
          "eight values or their four pairs) or by the flags alone (neither, a trial, a purchase, both; or those four "
          "with the sessions bucket split at 4) put what one more euro returns on top of the plan's spend at %.3f to %.3f "
          "on Meta iOS, %.3f to %.3f on Snapchat iOS and %.3f to %.3f on Google iOS. The value equation fitted on the %d "
          "complete weeks alone puts what one more euro returns on TikTok iOS at %.3f on top of the plan's spend and %.3f "
          "on top of the stretch spend. The installs equation's "
          "own prediction at the plan, without step 7's scaling and with the share spent put in from outside (the spend "
          "over budget of the %d weeks, of the first %d or of the last %d; put in as that one share, or week by week "
          "through the delivery term and averaged), puts AppLovin Android between %.3f and %.3f and Google Android's plan "
          "spend at %d to %d installs a week; the thinnest of the six is AppLovin Android at %.3f, %.3f over the %.2f "
          "line, with the first %d weeks' share put in as one figure. Each of the six adds up, over the weeks its share "
          "is taken from and at their own budgets, to between %.1f and %.1f per cent of every channel's installs counted "
          "in those weeks, where step 7's scaling adds up to them. The same prediction with the share put at the "
          "geometric mean of the weekly shares or at the median week's is refused: whichever weeks the share is taken "
          "from it falls %.1f to %.1f per cent short of some channel's installs counted in them, where the six fall at "
          "most %.1f short, and at the first %d weeks' share it would put AppLovin Android at %.3f and %.3f, a cut, "
          "adding up to %.1f and %.1f per cent of its installs of those weeks where the two forms kept add up to %.1f "
          "and %.1f. Crossed with the battery (each of the four families' %d ways with every single way of the battery "
          "it can be taken with, "
          "and with one way of each of the other two steps at once, %s crossings), none of them moves a band: the "
          "nearest to a line is AppLovin Android at %.3f, on the installs equation fitted with the delivery left out, "
          "its own prediction not rescaled, at the last %d weeks' share of the budgets spent." % (
              f["beside_pad_pct"], bs["finer_rows"]["paid_per_install"]["Meta iOS"][0],
              bs["finer_rows"]["paid_per_install"]["Meta iOS"][1], bs["finer_rows"]["return_plan"]["Meta iOS"][0],
              bs["finer_rows"]["return_plan"]["Meta iOS"][1],
              gd["next_euro"]["Meta iOS"][0], gd["next_euro"]["Meta iOS"][1], gd["next_euro"]["Snapchat iOS"][0],
              gd["next_euro"]["Snapchat iOS"][1], gd["next_euro"]["Google iOS"][0], gd["next_euro"]["Google iOS"][1],
              s["mature_weeks"], vw["next_euro"]["TikTok iOS"][0], vw["next_euro_stretch"]["TikTok iOS"][0],
              s["weeks"], s["mature_weeks"], s["weeks"] - s["mature_weeks"],
              un["return_span"]["AppLovin Android"][0], un["return_span"]["AppLovin Android"][1],
              un["installs_span"]["Google Android"][0], un["installs_span"]["Google Android"][1],
              thin_un, thin_un - lo, lo, s["mature_weeks"], ky["held_pct"][0], ky["held_pct"][1],
              ky["refused_short_pct"][0], ky["refused_short_pct"][1], ky["held_short_pct"], s["mature_weeks"],
              ky["returns"][y1["geometric_mean"]]["AppLovin Android"], ky["returns"][y1["median_week"]]["AppLovin Android"],
              ky["adds_up_pct"][y1["geometric_mean"]]["AppLovin Android"], ky["adds_up_pct"][y1["median_week"]]["AppLovin Android"],
              ky["adds_up_pct"][y1["at_share"]]["AppLovin Android"], ky["adds_up_pct"][y1["weekly_shares"]]["AppLovin Android"],
              len(bs["names"]), _n(xr["crossings"]), xr["nearest"]["return_plan"], s["weeks"] - s["mature_weeks"]),
          "",
          "Each simpler way of taking a step is refuted by a figure from the files, and each files its channel in the wrong "
          "band with the other two steps as estimated. The stores' excess: each recorded monthly charge raised by its "
          "store's first monthly charges and renewals over the recorded ones, and each annual one by the store's annual "
          "first charges over the recorded ones, period by period (AppLovin Android %.3f) or over the whole record (%.3f), "
          "puts EUR %.2f and %.2f on the web checkout's subscribers against the %.2f they were charged; the candidates "
          "carried at one less the store's monthly subscriptions with a charge on file that were last seen with "
          "auto-renew off, divided by the monthly charges on file for the store (%.3f on Google Play and %.3f on the App "
          "Store a month; AppLovin Android %.3f) take in %s of Google Play's %s renewals beyond the records over the "
          "fitted periods and %s of the App Store's %s, and at the share that was made of the next twelve charges "
          "falling due after the last open, and by 8 November 2026, on the web checkout's subscribers of step 4's fit, "
          "each counted only where the one before it was made (%.3f; AppLovin Android %.3f) %s and %s, where the "
          "fitted continuations take in %s and %s. The unnamed installs: valued like the named ones (Meta iOS %.3f) the "
          "accounts with no channel come to %.2f times what they paid, and with Apple Search Ads' ratio, its installs "
          "that declined tracking over its others, taken apart for the accounts with neither a trial nor a purchase "
          "flagged in the first 48 hours and for those with either (%.3f and %.3f; Meta iOS %.3f), %.2f; taken together "
          "(the five differences weighed by the inverse of the fit's own covariance of the five ratios, its spread taken "
          "row by row; five degrees of freedom), the five networks' fitted ratios stand %.1f from "
          "Apple Search Ads' ratio at the same first-48-hour value (%.3f) and %.1f from the ratios the same kind of "
          "network shows on Android (AppLovin Android's %.3f for the four social networks and Google Android's %.3f for "
          "Google; Meta iOS %.3f) against a five per cent point of %.2f, or %.1f and %.1f with one variance for every "
          "row; one "
          "ratio for every source (%.3f), organic at Apple Search Ads' ratio with one ratio for the networks (%.3f) and the "
          "accounts' own value by first-48-hour value (%.3f) are refused by the test of the five networks sharing one ratio "
          "(%s) and miss the market-weeks' revenue by %.1f and %.1f per cent against %.1f; the four social networks sharing "
          "one ratio (%.3f) is refused by its test (%s). Meta, TikTok and Snapchat sharing one ratio is refused as well "
          "(%s; Meta with Snapchat %s), though it would leave the seven bands as they are. So would the ratios fitted "
          "with the three markets pooled, on %d weeks in place of %d market-weeks (Google %.3f, Google iOS %.3f): their "
          "spreads are %.1f to %.1f times the market-weeks' (Google's %.3f against %.3f) and they miss the market-weeks' "
          "revenue by %.1f per cent against %.1f. The response: the fit on spend "
          "(Google Android %.3f) fails on the moved weeks as step 6 shows, and the year to 2 November 2025's return carried "
          "over (%.3f) holds the weekly spend at that year's EUR %s where the plan gives EUR %s. A straight line in the "
          "budget is refused in both of its forms, though either would leave the seven bands as they are: fitted on the "
          "installs themselves, each channel with its own line, the month pattern added on and the log of the share spent "
          "beside it, it misses the installs of the moved weeks by %.1f per cent against the fitted form's %.1f and puts "
          "Google Android's raised weeks over its lowered ones at %.3f against the %.3f counted; fitted on the log of "
          "installs as the log of the budget plus a constant for each channel, with the same month pattern and delivery "
          "term, it is refused when the log of the budget is added, channel by channel (F %.1f against a five per cent "
          "point of %.2f, where the budget added to the fitted form gives %.1f). An exponential in the budget is refused "
          "the same way (F %.1f) and misses the moved weeks by %.1f per cent; and value per install held at the year's figure "
          "whatever the spend is refused by the value slopes (%.2f to %.2f, each at least %.1f of its spreads below "
          "nought)." % (
              sc["by_period"]["return_plan"], sc["one_factor"]["return_plan"], w["true_up"], w["true_up_one_factor"],
              w["charged"], gr["seen"]["rate"], ar["seen"]["rate"], sc["seen_rate"]["return_plan"], _n(gr["seen"]["takes_in"]),
              _n(gp["renewal_excess_fitted_periods"]), _n(ar["seen"]["takes_in"]), _n(ap["renewal_excess_fitted_periods"]),
              gr["web"]["rate"], sc["web_rate"]["return_plan"], _n(gr["web"]["takes_in"]), _n(ar["web"]["takes_in"]),
              _n(gr["fitted"]["takes_in"]), _n(ar["fitted"]["takes_in"]),
              sc["named_by_cell"]["return_plan"], Q["adding_up"]["named"], Q["search_ads_by_flag"][0],
              Q["search_ads_by_flag"][1], sc["search_ads"]["return_plan"],
              Q["adding_up"]["search_ads"], Q["lent"]["search_ads"]["stat"], Q["search_ads_ratio"], Q["lent"]["android"]["stat"],
              Q["android_ratio"]["AppLovin Android"], Q["android_ratio"]["Google Android"],
              sc["android"]["return_plan"], Q["lent"]["search_ads"]["point"], Q["lent"]["search_ads"]["stat_one_variance"],
              Q["lent"]["android"]["stat_one_variance"],
              sc["one_ratio"]["return_plan"], sc["organic_pinned"]["return_plan"], sc["pool_value"]["return_plan"],
              _two(T["the five networks"]), mw["miss_pct"]["one_ratio"], mw["miss_pct"]["pool_value"], mw["miss_pct"]["fitted"],
              sc["four_social"]["return_plan"], _two(T["the four social networks"]), _two(T["Meta, TikTok and Snapchat"]),
              _two(T["Meta and Snapchat"]),
              P["rows"], P["rows_market_weeks"], P["sources"]["Google iOS"]["ratio"], P["return_plan"]["Google iOS"],
              P["se_times"][0], P["se_times"][1], P["sources"]["Google iOS"]["se"], P["sources"]["Google iOS"]["se_market_weeks"],
              mw["miss_pct"]["markets_pooled"], mw["miss_pct"]["fitted"],
              sc["on_spend"]["return_plan"], sc["last_year"]["return_plan"], _n(ga["year_weekly_spend"]),
              _n(ga["plan_weekly_spend"]), fm["moved_missed_pct"]["line"], fm["moved_missed_pct"]["power"],
              fm["line_raised_over_lowered"], gm["actual"], fm["line"], fm["point"], fm["power"], fm["exponential"],
              fm["moved_missed_pct"]["exponential"],
              fm["value_slope_range"][0], fm["value_slope_range"][1], fm["value_slope_spreads"]),
          "",
          "The three steps are independent. With the stores' excess alone taken the simpler way the bands are the same but "
          "for %s; with the unnamed installs alone, but for %s; with the response alone, but for %s. With two of them taken "
          "the simpler way both of their channels move (%s; %s; %s), and with all three, %s. Taken singly or together they "
          "file %d different wrong sets of bands, and each leaves the other steps' own figures inside their ranges: with "
          "the stores' excess taken the simpler way Meta iOS's installs of the year went on to pay EUR %.2f each (range "
          "%.2f to %.2f), with the unnamed installs taken the simpler way AppLovin Android's stay at EUR %.2f, neither "
          "figure moves with the response, and Google Android's %d installs a week move with neither of the other two "
          "steps. The bands also stand with the stores' fitted rates, each "
          "source's ratio and each channel's two budget slopes moved a fifth either way, and with the budget that delivers "
          "the plan's spend moved by the %.1f per cent that the delivery share's widest quarter departs from the %d-week "
          "share on any channel: the thinnest of those is %s at %.3f, and Meta iOS with its own ratio a fifth lower or "
          "higher sits at %.3f and %.3f." % (
              _list(_moved(f, "S1")), _list(_moved(f, "S2")), _list(_moved(f, "S3")), _list(_moved(f, "S1+S2")),
              _list(_moved(f, "S1+S3")), _list(_moved(f, "S2+S3")), _list(_moved(f, "S1+S2+S3")), f["distinct_wrong_calls"],
              own["S1"]["Meta iOS"], f["paid_per_install_band"]["Meta iOS"][0], f["paid_per_install_band"]["Meta iOS"][1],
              own["S2"]["AppLovin Android"],
              f["installs_week"]["Google Android"], f["delivery_share_spread_pct"], s["weeks"], thin_c, thin["returns"][thin_c],
              min(p["returns"]["Meta iOS"] for p in mer), max(p["returns"]["Meta iOS"] for p in mer))]
    open(path, "w").write("\n".join(L) + "\n")
