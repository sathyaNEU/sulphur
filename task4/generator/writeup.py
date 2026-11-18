"""submission.md: the tags and the four answer blocks, every figure from figures.json."""
import datetime as dt

import analysis as A
import deliver
import docs
import pack

F = dict(pack.FILES)
F.update(docs.FILES)
POOLS = deliver.POOLS
COVER = {"buy": "purchase", "hire": "seasonal hire", "nothing": "no cover"}
WORD = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine", 10: "ten"}


def k(x):
    return "{:,}".format(int(x))


def _list(xs):
    xs = list(xs)
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _b(band):
    return "%s to %s" % (k(band[0]), k(band[1]))


def day(iso, year=True):
    d = dt.date.fromisoformat(iso)
    return "%d %s %d" % (d.day, d.strftime("%B"), d.year) if year else "%d %s" % (d.day, d.strftime("%B"))


def each(f, fn, pools=POOLS):
    """one clause a container type, in the pack's order"""
    return _list("%s %s" % (f["plural"][p], fn(p)) for p in pools)


def write(path, f):
    nm, pl = f["names"], f["plural"]
    P, c, R, rc = f["pool"], f["counts"], f["routes"], f["route_components"]
    refl = R["S1+S2+S3"]
    moved = [p for p in POOLS if refl[p]["cover"] != f["cover"][p]]
    by = {x: [p for p in POOLS if f["cover"][p] == x] for x in ("buy", "hire", "nothing")}
    untag = [p for p in POOLS if p != A.TAGGED]
    count = day(c["count_dates"][-1])
    L = ["# task4 answer blocks", "", "## Tags", "",
         "**Domain:** Machine Learning Research, General Statistics & Data Science (regression, classification & model "
         "diagnostics: a seasonal delivery forecast and three stocks no record holds, estimated for a returnable container "
         "fleet).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "", "## Final Recommendation", ""]
    L.append(
        "**%s.** In the fleet standard's planning case the largest weekly shortfall of the 2027 summer season is %s "
        "containers, against the maker's minimum order runs of %s: at or above the run for %s, above nil and below it for "
        "%s, and a surplus for %s. This rejects the order the usual sizing gives from the same records, %s, which moves the "
        "stock at customers in step with deliveries, holds the cold store at summer 2026's weeks of cover and uses the "
        "tagged kegs' loss rate for every type: a cellar holds a fixed stock for each line whatever it sells, the 2027 brew "
        "plan racks each beer in larger runs across a wider range, and the types without tags lose %s to %s per cent of the "
        "containers delivered against the tagged kegs' %s." % (
            deliver.headline(f), each(f, lambda p: k(f["plan"][p])), _list(k(f["min_run"][p]) for p in POOLS),
            _list(pl[p] for p in by["buy"]), _list(pl[p] for p in by["hire"]), _list(pl[p] for p in by["nothing"]),
            _list("%s for %s (%s)" % ({"buy": "a purchase", "hire": "a seasonal hire", "nothing": "no cover"}[refl[p]["cover"]],
                                      pl[p], k(refl[p]["plan"])) for p in moved),
            "%.2f" % min(P[p]["loss_pct"] for p in untag), "%.2f" % max(P[p]["loss_pct"] for p in untag),
            "%.2f" % f["tags"]["loss_pct"]))
    L += ["", "## Supplementary Questions", "", "### %s" % deliver.FILES["wb"], ""]
    L.append("1. The first sheet states the cover for each container type, one row a type, with its largest weekly "
             "shortfall in the planning case and in the hot case beside the maker's minimum order run.")
    for i, p in enumerate(POOLS):
        L.append("%d. %s: largest weekly shortfall %s containers in the planning case (band %s) and %s in the hot case "
                 "(band %s)%s; cover: %s." % (
                     2 + i, pl[p].capitalize(), k(f["plan"][p]), _b(f["plan_band"][p]), k(f["hot"][p]), _b(f["hot_band"][p]),
                     ", a surplus in both" if f["hot"][p] < 0 else "", COVER[f["cover"][p]]))
    L += ["", "### %s" % deliver.FILES["deck"], ""]
    L.append("%d. A few slides for the order meeting that open on the cover for each container type, with the same "
             "figures as the workbook." % (2 + len(POOLS)))
    L += ["", "## Critical Components", ""]
    L.append("1. From the count of %s to each type's worst week of the season, the stock at customers rises by **%s** "
             "containers over the five types, the new estate's cellars included (band %s)." % (
                 count, k(f["trade_rise"]), _b(f["trade_rise_band"])))
    L.append("2. Under the 2027 brew plan the cold store holds **%s** full containers over the five types, each type in "
             "its own worst week (band %s)." % (k(f["store_2027"]), _b(f["store_2027_band"])))
    L.append("3. In the year to the count of %s the four types without tags lost **%s** containers at customers (band %s)."
             % (count, k(f["year_loss"]), _b(f["year_loss_band"])))
    L += ["", "## Step-by-Step", ""]
    last = c["count_dates"][-1]
    acc = f["account"]
    lv, rf, t, ts = f["levels"], f["referee"], f["tags"], f["tests"]
    ref = f["refused"]
    r8, r13 = ref["deliveries at each count as the eight weeks before it"], ref["deliveries at each count as the thirteen weeks before it"]
    flat, noc = ref["a single slope in the weather response"], ref["containers condemned at the wash after the count left out"]
    notrend, split52 = ref["no trend in the deliveries fit for any type"], ref["the store's stock split fitted on the last year's Mondays alone"]
    sp = f["split"]
    vr, vh = f["variant_range"], f["variant_range_hot"]
    od, ap, pg, wq = f["own_dockets"], f["apart"]["K50"], f["pairing"], f["wash_log"]["K50"]
    own4 = ref["a line's sales from its own dockets over the four weeks to the count"]
    pairb = ref["the store's stock split fitted with each Monday set against the week beginning"]
    heldr = ref["the wash line and the repair bay held at the last count's level"]
    apartw = ref["the cellar counts fitted with a line's level and its movement apart, on the count's week"]
    fc = f["first_count"]
    fit156, slope156 = ref["the store's stock split fitted on all three years' Mondays"], ref["the fitted slope beside half the plan's runs, on all three years' Mondays"]
    slope52 = ref["the fitted slope beside half the plan's runs, on the last year's Mondays alone"]
    before_count = (dt.date.fromisoformat(c["count_dates"][-1]) - dt.timedelta(days=7)).isoformat()
    win = lambda p: tuple(k(sp[p][key]) for key in ("fixed_52", "fixed_104", "fixed_156", "se_52", "se_104", "se_156", "half_runs"))
    steps = [
        "Put the dockets on one footing (`%s`, %s rows): a docket line a handheld sent twice counted once (%s rows), a blank "
        "container code read from the product (`%s`, %s lines), the three codings of a container type brought to one "
        "(`%s`) and %s renumbered accounts read under their current number (`%s`). That gives each type's deliveries for "
        "the %d weeks from %s, a week running Monday to Sunday." % (
            F["dockets"], k(c["docket_rows"]), k(c["resent_rows"]), F["products"], k(c["blank_codes"]), F["codes"],
            k(c["renumbered"]), F["accounts"], c["weeks"], day(c["first_week"])),
        "Built each type's stock account at the four counts: the containers on `%s` bought before the count and not "
        "condemned before it, less the containers counted on Wrenfold's sites in `%s`. Off site at the count of %s: %s. "
        "The register strikes a container only when the wash line condemns it, so off site holds the containers at "
        "customers and every container lost there since the first count, where the account starts clear of them: off "
        "site then stood at the stock step 4's relation gives the cellars (a line's fixed stock for each of the type's "
        "lines on the dockets, plus the weighted figure times the deliveries at that count), %s." % (
            F["register"], F["stocktake"], count, each(f, lambda p: k(acc[p][last]["off_site"])),
            each(f, lambda p: "%s against %s" % (k(fc[p]["off_site"]), k(fc[p]["relation"])))),
        "Fitted each type's weekly deliveries by least squares on logs: a level, a straight trend, two yearly harmonics "
        "(on the day of the year of the week's Thursday, over 365) and the week's mean daily maximum temperature at the "
        "station (`%s`) with one slope above and one below a bend, the bend set "
        "on a half-degree grid from %d to %d degrees where the squared error is least (%s). The fit's value for the week "
        "that ends at a count is the type's deliveries at that count (%s a week at %s); the first count has no week of "
        "dockets behind it and takes the fit's value for the first week on record. Against a single slope in "
        "temperature the bend's F statistic on 2 and %d degrees of freedom is %s, against a 5 per cent point of %s: the "
        "bend is kept for all five types, a single slope for the types under that point is one of step 11's conventions, "
        "and a single slope for every type is not used. The trend's t "
        "statistic is %s: it is kept for all five, dropping it for the types under 2 is one of step 11's conventions, "
        "and dropping it for every type is not used (the planning case would be %s, the same covers). A mean of the "
        "weeks before the count is not used for the count's "
        "deliveries beyond four weeks: for 50 litre kegs the eight weeks before it average %s a week and the thirteen "
        "weeks %s, %s and %s per cent above the count's own week, because the season is still falling; read that way "
        "the planning case would be %s and %s, the same cover." % (
            F["weather"], f["stated"]["bend_grid"][0], f["stated"]["bend_grid"][1],
            each(f, lambda p: "%.1f" % P[p]["bend_c"]), each(f, lambda p: k(P[p]["level_at_count"])), count,
            ts["K50"]["df"], each(f, lambda p: "%.1f" % ts[p]["bend_F"]), "%.2f" % ts["f_crit"],
            each(f, lambda p: "%.1f" % ts[p]["trend_t"]), each(f, lambda p: k(notrend[p])),
            k(lv["K50"]["eight_weeks"]), k(lv["K50"]["thirteen_weeks"]), lv["K50"]["eight_over_fit_pct"],
            lv["K50"]["thirteen_over_fit_pct"], k(r8["K50"]), k(r13["K50"])),
        "Estimated what a cellar holds from the reps' counts (`%s`, %s line counts on %s visits): the containers at a line "
        "(full, on dispense and empty) regressed by least squares on a constant, the line's deliveries a week in the "
        "week of the count, and that figure times the weeks between the account's deliveries (one, or a half for an "
        "account with two delivery days in `%s`). A line's deliveries in a week are its share of its type's deliveries "
        "over the whole record times the type's deliveries that week; the 20 litre kegs of an account are one guest "
        "line whatever the beer. A line holds %s containers whatever it sells, and per container it sells a week %s "
        "on a weekly call. Weighted by the deliveries on weekly and twice-weekly calls, customers hold %s containers "
        "for each container delivered a week. A line's own dockets over a few weeks are not used for its sales, because "
        "a line takes whole containers: for 50 litre kegs the same fit gives %s containers at customers for each "
        "container delivered a week on one week of a line's own dockets, %s on four and %s on thirteen, and on four "
        "weeks it puts the tagged kegs' rise of step 5's check at %s against the %s their tags counted (the planning "
        "case would be %s, the same covers). Thirteen weeks of a line's own dockets is one of step 11's conventions. A "
        "fit that gives a line's average weekly deliveries and the week's departure from that average a slope each is "
        "not used on the count's week: on a weekly call the departure's slope for 50 litre kegs is %s on the count's "
        "week, %s on the fitted week and %s on four weeks of deliveries beside an average's slope of %s, %s and %s, so "
        "one week understates how far a line's stock follows its trade (the planning case would be %s, the same "
        "covers). On all the counts and four weeks of deliveries, where the two slopes stand that close, it is one of "
        "step 11's conventions." % (
            F["audits"], k(c["audit_rows"]), k(c["audit_visits"]), F["routes"],
            each(f, lambda p: "%.2f" % P[p]["fixed_per_line"]), each(f, lambda p: "%.2f" % P[p]["per_sale_weekly"]),
            each(f, lambda p: "%.3f" % P[p]["per_sale_pool"]),
            "%.2f" % od["per_sale"]["1"]["K50"], "%.2f" % od["per_sale"]["4"]["K50"], "%.2f" % od["per_sale"]["13"]["K50"],
            k(od["rise"]["4"]), k(rf["seen"]), each(f, lambda p: k(own4[p])),
            "%.2f" % ap["week"]["move"], "%.2f" % ap["fit"]["move"], "%.2f" % ap["four"]["move"],
            "%.2f" % ap["week"]["level"], "%.2f" % ap["fit"]["level"], "%.2f" % ap["four"]["level"],
            each(f, lambda p: k(apartw[p]))),
        "The rise in the stock at customers from the count to a week is that last figure times the change in the weekly "
        "deliveries of the accounts supplied today (the fit at the week's temperature in the case being run, its normal in "
        "the planning case and the summer's own in the hot case, less the deliveries at the count), plus the new estate's cellars from each outlet's listing date in `%s`: its lines at the fixed stock and "
        "its scheduled volume at the weekly-call figure, the schedule's average weekly volume carried with the type's "
        "fitted season (the harmonics and the temperature terms of step 3's fit without its level or trend, at the "
        "week's own temperature in the hot case) relative to the mean of the last %d weeks at the normal. The estate's volume counts in the week's deliveries for the store, the depots, wash and repair, the "
        "float and the losses of steps 7 to 9. To each type's worst week the rise is %s, "
        "**%s** over the five types (Component 1). The hurried route moves the stock at customers at the count (off "
        "site less the loss since the first count at step 6's rate, %s for 50 litre kegs) in step with deliveries, the "
        "week's over the count's; for the tagged kegs it takes their tags' count at the close of the week 52 weeks "
        "earlier, times the week's deliveries over that earlier week's, less the tags' count at the count. It gives %s "
        "over the five types and %s 50 litre kegs short, a purchase. The tagged "
        "20 litre kegs check it. In `%s` a keg is at a customer from a delivery read to its next read of any kind, a "
        "tag replaced at the wash followed to its keg's serial, a repeat read of the same point within two minutes "
        "dropped, and the stay after a keg's last delivery left out where the recovery agent closed that delivery as "
        "not traced (the keg's earlier stays count); the count is scaled "
        "for the %s per cent of the dockets' deliveries that have a delivery read (%s of %s). From the start of the "
        "count's Monday, %s, to the mean of the three Mondays (%s, %s and %s, each at its start) that close the three "
        "consecutive weeks of 2026 with the most 20 litre kegs delivered, the tags count %s more kegs at customers (%s "
        "to %s); the line relation gives %s and "
        "stock in step with deliveries %s. With the kegs closed as not traced left in the rise is %s, and without the "
        "scaling %s. The tags' count is read from the count of December 2024 on: the reads begin on %s and the count "
        "is still filling through the first months (%s)." % (
            F["schedule"], f["stated"]["year_weeks"][0], each(f, lambda p: k(f["trade_rise_by_pool"][p])), k(f["trade_rise"]),
            k(f["at_customers_count"]["K50"]), k(rc["S1"]["C1"]), k(R["S1"]["K50"]["plan"]), F["tags"],
            "%.1f" % t["read_share_pct"], k(t["deliver_reads"]), k(t["docket_deliveries"]), day(rf["counted_on"]),
            day(rf["mondays"][0], False), day(rf["mondays"][1], False), day(rf["mondays"][2]), k(rf["seen"]), k(rf["start"]),
            k(rf["top"]), k(rf["golden"]), k(rf["proportional"]), k(t["rise_lost_in"]), k(t["rise_unscaled"]),
            day(c["first_week"]), _list("%s kegs on %s" % (k(v), day(d)) for d, v in t["fill"])),
        "Read the year's loss from the stock account: over the year to %s off site rose by %s containers while the "
        "stock customers hold changed by %s (step 4's figure on the change in the deliveries at the two counts), so "
        "customers lost %s, **%s** on the four types without tags (Component 3), which is %s per cent of the year's "
        "deliveries. The 20 litre kegs carry tags and their loss is read from the recovery agent's cases (`%s`): %s kegs "
        "not traced of %s delivered in the 52 weeks before %s, the latest whose cases have all closed, %s per cent. The "
        "hurried route uses that rate for every type: %s lost on the four types and %s firkins short, a seasonal hire." % (
            count, each(f, lambda p: k(P[p]["off_site_gain"]), untag), each(f, lambda p: k(P[p]["trade_change"]), untag),
            each(f, lambda p: k(f["year_loss_by_pool"][p]), untag), k(f["year_loss"]),
            each(f, lambda p: "%.2f" % P[p]["loss_pct"], untag), F["recovery"], k(t["not_traced"]), k(t["delivered"]),
            day(t["window"][1]), "%.2f" % t["loss_pct"], k(rc["S3"]["C3"]), k(R["S3"]["FIR"]["plan"])),
        "Split the cold store's stock: over the last %d Mondays of `%s`, each Monday's stock set against the "
        "deliveries of the week that ended the day before, the mean full stock, less half of each beer's "
        "racking run summed over the type's beers (a beer's run is its median containers filled in `%s` since the count "
        "of December 2024), is %s weeks of deliveries. For a week of 2027 the store is that cover times the week's "
        "deliveries plus half the runs `%s` gives the beers on sale that week: %s, **%s** over the five types "
        "(Component 2). The hurried route carries the store's stock over deliveries around the same week of 2026 (the "
        "five Mondays centred on the Monday that closes the week 52 weeks earlier, over the five weeks that ended at "
        "them) to 2027's deliveries: %s over the five types and a surplus of %s 20 litre kegs, no cover. Fitting the split in "
        "place of the half runs (the Monday stock regressed on the week's deliveries, the fitted fixed part then scaled "
        "by the 2027 half runs over today's) is used where it agrees with the racking log, which records the runs: over "
        "the same 104 Mondays the fixed part is %s containers with standard errors of %s against half runs of %s, "
        "within one standard error for every type, and it is one of step 11's conventions, as is the fitted slope kept "
        "as the cover beside half the plan's runs. On the last 52 Mondays or on all 156 the fit is not used in either "
        "form. Its fixed part moves with the window where the log's half runs do not: for firkins %s, %s and %s on 52, "
        "104 and 156 Mondays (standard errors %s, %s and %s; half runs %s), for kilderkins %s, %s and %s (%s, %s and "
        "%s; %s) and for 50 litre kegs %s, %s and %s (%s, %s and %s; %s), more than one standard error from the log for "
        "kilderkins on 52 Mondays and for firkins and 50 litre kegs on 156, while the cover beside the log's half runs "
        "holds year by year (for firkins %s in the three years to the count, the latest first). The planning case "
        "would be %s with the 52 Mondays' fixed part and %s with their slope, %s with the 156 Mondays' fixed part and "
        "%s with their slope, the same covers each time. The mean split over all 156 Mondays is one of step 11's "
        "conventions. Set against the week beginning each Monday (the 104 Mondays to %s) the fit is not used: its R "
        "squared falls from %s to %s for the five types in order, and for 50 litre kegs its fixed part is %s (standard "
        "error %s) where the racking log's half runs are %s (the planning case would be %s, the same covers)." % ((
            f["stated"]["year_weeks"][1], F["store"], F["racking"], each(f, lambda p: "%.3f" % P[p]["store_cover_weeks"]),
            F["plan"], each(f, lambda p: k(f["store_by_pool"][p])), k(f["store_2027"]), k(rc["S2"]["C2"]),
            k(-R["S2"]["K20"]["plan"]), each(f, lambda p: k(sp[p]["fixed_104"])), _list(k(sp[p]["se_104"]) for p in POOLS),
            _list(k(sp[p]["half_runs"]) for p in POOLS)) + win("FIR") + win("KIL") + win("K50") + (
            _list("%.3f" % v for v in sp["FIR"]["cover_by_year"]),
            each(f, lambda p: k(split52[p])), each(f, lambda p: k(slope52[p])), each(f, lambda p: k(fit156[p])),
            each(f, lambda p: k(slope156[p])), day(before_count),
            _list("%.2f" % pg[p]["r2_ended"] for p in POOLS), _list("%.2f" % pg[p]["r2_beginning"] for p in POOLS),
            k(pg["K50"]["fixed_beginning"]), k(pg["K50"]["se_beginning"]), k(sp["K50"]["half_runs"]),
            each(f, lambda p: k(pairb[p])))),
        "Took the rest of the requirement from `%s` section 2.1: the depots, wash and repair at the mean over the four "
        "counts of their counted containers over the deliveries at the count (%s weeks), and the float at two sevenths "
        "of the week's deliveries. Holding the wash line and the repair bay at the count's level through the season is "
        "not used: in `%s` the 50 litre kegs awaiting wash stood at %s on average at the close of step 5's three "
        "weeks of summer 2026 against %s at the count, and the repair bay (the containers in repair at the first count, plus "
        "those sent to repair, less those back) at %s against %s, while the week's deliveries stood at %s against %s "
        "(the planning case would be %s, the same covers). The fleet after the count falls each week by the type's "
        "loss rate and by the wash "
        "line's condemnations (the register's condemned in the year to the count over that year's deliveries), both on "
        "the week's deliveries. Leaving the condemnations out is not a reading of 2.2: the register strikes %s "
        "containers in the year, and the planning case would be %s." % (
            F["standard"], each(f, lambda p: "%.3f" % P[p]["other_weeks"]), F["wash"], k(wq["awaiting_peak"]),
            k(wq["awaiting_count"]), k(wq["repair_peak"]), k(wq["repair_count"]), k(wq["deliveries_peak"]),
            k(wq["deliveries_count"]), each(f, lambda p: k(heldr[p])),
            each(f, lambda p: k(P[p]["condemned_last_year"])), each(f, lambda p: k(noc[p]))),
        "Ran each week from the count to the week beginning %s. The containers at customers at the count stand in both "
        "the requirement and the fleet, so a week's shortfall (2.3) is the rise at customers, the store, the depots, "
        "wash and repair and the float, less the containers counted on Wrenfold's sites at the count, plus the "
        "containers lost and condemned since, the week's own included. The planning case (3.1, 3.2) is the largest of the %d season weeks with "
        "every week at its normal: %s." % (day(f["season"][1]), c["season_weeks"], each(f, lambda p: k(f["plan"][p]))),
        "Ran the season on each of the ten summers %d to %d (3.3), each summer's %d season weeks in order from its own "
        "first Monday of May and every other week at its normal; the hot case is the second highest of the ten largest "
        "weekly shortfalls: %s." % (c["summers"][0], c["summers"][1], c["season_weeks"], each(f, lambda p: k(f["hot"][p]))),
        "Read the cover on the planning case (4.1) against the minimum order runs of `%s`: %s. Rebuilt the route with "
        "each of %d conventions changed alone and every two of them together, %s rebuilds (the loss over two or three "
        "years of the account, without the customers' own change, or counted to the end of the week before; the cellar "
        "counts fitted apart for each delivery interval, on the summer's counts only, or with a slope each for a line's "
        "average deliveries and the week's departure from it on four weeks of deliveries; a line's deliveries from the fit, from its share of the type's four weeks around the count or "
        "from thirteen weeks of its own dockets, or its share from the last year; one or three harmonics, or the "
        "harmonics on a 52 week year; the bend a degree either way, kept only where its F statistic "
        "asks for it, or a quadratic in temperature in its place; the trend kept only where its t statistic shows one, "
        "or not carried past the count; the deliveries at a count as the one, two or four weeks before it, or at the "
        "first count from the fit carried back a week; the estate's scheduled volume level through the year, or its "
        "season at the normal in the hot case; the store's cover as the "
        "median week's, on the last year's Mondays or on all three years', the split fitted, or the fitted slope beside half the plan's "
        "runs; a beer's run as the mean of its rackings; "
        "the condemnations over the three years of the account; the depots, wash and repair at the last count alone, "
        "the depots from `%s`, or the depots, the wash line's backlog and the repair bay week by week from their own "
        "records; the tagged kegs' "
        "stock at customers from their tags, scaled or not, their response from the tags' rise to summer 2026, and "
        "their loss from the stock account or on the year to "
        "the count with open cases as not traced). Every one files the same five covers (planning case %s; hot case "
        "%s), and each band holds them all. "
        "With what a line holds, the store's cover or the loss rate moved by %d per cent either way, or the season's "
        "deliveries by %d per cent, the covers stay." % (
            F["quotation"], each(f, lambda p: COVER[f["cover"][p]]), f["singles"], k(f["rebuilds"]), F["depots"],
            "; ".join("%s %s to %s" % (pl[p], k(vr[p][0]), k(vr[p][1])) for p in POOLS),
            "; ".join("%s %s to %s" % (pl[p], k(vh[p][0]), k(vh[p][1])) for p in POOLS),
            f["stated"]["forcing_pct"][0], f["stated"]["forcing_pct"][1]),
    ]
    for i, s in enumerate(steps):
        L.append("%d. %s" % (1 + i, s))
    resp = f["response_pct"]
    L += ["",
          "No other cover survives the files. Stock at customers in step with deliveries passes a look at the totals and "
          "fails the one type whose stock at customers can be counted (%s against the %s the tags saw): by the reps' "
          "counts the stock at customers moves %s per cent as far as deliveries do, by type. The tagged kegs' own "
          "measured response (%s per cent as far over step 5's rise, %s against %s, and %s per cent by a least squares line "
          "of their weekly count on the week's deliveries over the last %d weeks) cannot be carried to the other types either: their lines sell more "
          "against the same fixed stock. The store's weeks of cover are not a property of the store: they run from %s to %s "
          "weeks across the five types over the last two years, while the cover beside half the racking runs is %s to "
          "%s in every one, and the 2027 plan changes the runs. The tagged kegs' loss rate leaves the other types' "
          "stock accounts open: at %s per cent of deliveries the four types would have lost %s containers in the year "
          "where off site rose by %s. The register read as the fleet counts every lost container as stock. All three "
          "shortcuts together (the stock at customers at the count then being off site less the loss at the tagged "
          "kegs' rate, %s for 50 litre kegs, and the tagged kegs' stock moved from their tags as in step 5) give %s." % (
              k(rf["proportional"]), k(rf["seen"]), "%d to %d" % (min(resp.values()), max(resp.values())),
              t["share_pct"], k(rf["seen"]), k(rf["proportional"]), t["line_pct"], f["stated"]["year_weeks"][1],
              "%.2f" % min(f["store_weeks"].values()), "%.2f" % max(f["store_weeks"].values()),
              "%.3f" % min(P[p]["store_cover_weeks"] for p in POOLS), "%.3f" % max(P[p]["store_cover_weeks"] for p in POOLS),
              "%.2f" % t["loss_pct"], k(rc["S3"]["C3"]), k(f["off_site_gain_untagged"]), k(f["at_customers_tag_rate"]["K50"]),
              _list("%s for %s (%s)" % ({"buy": "a purchase", "hire": "a seasonal hire", "nothing": "no cover"}[refl[p]["cover"]],
                                        pl[p], k(refl[p]["plan"])) for p in POOLS)), ""]
    open(path, "w").write("\n".join(L))
