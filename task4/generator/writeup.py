"""submission.md: the tags and the four answer blocks, every figure from figures.json."""
import datetime as dt

import deliver
import docs
import pack

F = dict(pack.FILES)
F.update(docs.FILES)
POOLS = deliver.POOLS
COVER = {"buy": "purchase", "hire": "seasonal hire", "nothing": "no cover"}
COMP = (("trade_rise", "C1"), ("store_2027", "C2"), ("year_loss", "C3"))


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


def five(f, d, fmt=None):
    return ", ".join((fmt % d[p]) if fmt else k(d[p]) for p in POOLS)


def covers(f, route):
    r = f["routes"][route]
    return each(f, lambda p: "%s (%s)" % (COVER[r[p]["cover"]], k(r[p]["plan"])))


def wrong(f, route):
    r = f["routes"][route]
    moved = [p for p in POOLS if r[p]["cover"] != f["cover"][p]]
    return _list("%s for %s (%s)" % ({"buy": "a purchase", "hire": "a seasonal hire", "nothing": "no cover"}[r[p]["cover"]],
                                     f["plural"][p], k(r[p]["plan"])) for p in moved)


def reflex_words(f):
    """what the records read as they stand order, a figure near nil stated as next to nothing"""
    r = f["routes"]["S1+S2+S3"]
    out = []
    for p in POOLS:
        if r[p]["cover"] == f["cover"][p]:
            continue
        x = r[p]["plan"]
        if abs(x) < 0.5 * (f["plan_band"][p][1] - f["plan_band"][p][0]):
            out.append("about nil for %s (%s; the route sits on the nil line)" % (f["plural"][p], k(x)))
        else:
            out.append("%s for %s (%s)" % ({"buy": "a purchase", "hire": "a seasonal hire", "nothing": "no cover"}[r[p]["cover"]],
                                            f["plural"][p], k(x)))
    return _list(out)


WOC = ("for each type and each 2027 week, the Monday positions over the five weeks centred on the same week of 2026, "
       "each Monday the stock at the close of the week that ended the day before, summed and divided by the type's "
       "deliveries over those five weeks, times the 2027 week's deliveries")


def nm(f, k, p, q="plan"):
    return f["pass3"]["alone"][k][p][q]


def weekword(f, p):
    ws = [day(x) for x in f["worst_weeks"][p]]
    return "worst week beginning " + ws[0] if len(ws) == 1 else "worst week beginning " + " or ".join(ws)


def write(path, f):
    pl = f["plural"]
    P, A, c, rc = f["pool"], f["account"], f["counts"], f["route_components"]
    fs = f["falsification"]
    count = day(c["count_date"])
    L = ["# task4 answer blocks", "", "## Tags", "",
         "**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (a seasonal "
         "delivery forecast and three stocks no record holds, each estimated from a record that sees part of it, for a "
         "returnable container fleet).",
         "**Analytical objective:** Forecasting & Predictive Modeling.", "", "## Final Recommendation", ""]
    L.append(
        "**%s.** The largest weekly shortfall of the 2027 summer season in the fleet standard's planning case is %s "
        "containers against the maker's minimum order runs of %s; this rejects the order the records give read as they "
        "stand (the reps' cellar checks as what a line holds, the cold store at summer 2026's weeks of cover and the "
        "register less the condemned as the fleet; the weeks of cover are, %s), which orders %s." % (
            deliver.headline(f), each(f, lambda p: k(f["plan"][p])), _list(k(f["min_run"][p]) for p in POOLS),
            WOC, reflex_words(f)))
    L += ["", "## Supplementary Questions", "", "### %s" % deliver.FILES["wb"], "",
          "The first sheet gives the cover for each container type (largest weekly shortfall in the planning case and the "
          "hot case, the worst week, the maker's minimum order run, the cover, with a chart against the runs); the second "
          "is the fleet account by type; behind them the routes, the weekly path, the cellar checks rebuilt, the lots, the "
          "cold store and the ten summers.", "",
          "1. The fleet account for each container type under FS-04, in containers, one row a type:"]
    for j, p in enumerate(POOLS):
        L.append("   %s. %s: lost in the trade over the year to the November count %s (band %s); %s more held by the "
                 "trade at its summer peak than at that count (band %s); %s full in the cold store at its fullest under "
                 "the 2027 brew plan (band %s); largest weekly shortfall of the 2027 season %s in the planning case (band "
                 "%s, %s) and %s in the hot case (band %s); cover: %s." % (
                     "abcde"[j], pl[p].capitalize(), k(f["year_loss_by_pool"][p]), _b(f["year_loss_band_by_pool"][p]),
                     k(f["trade_rise_by_pool"][p]), _b(f["trade_rise_band_by_pool"][p]), k(f["store_2027_by_pool"][p]),
                     _b(f["store_2027_band_by_pool"][p]), k(f["plan"][p]), _b(f["plan_band"][p]), weekword(f, p),
                     k(f["hot"][p]), _b(f["hot_band"][p]), COVER[f["cover"][p]]))
    L += ["", "### %s" % deliver.FILES["deck"], "",
          "Four slides for the order meeting: the cover for each type with the chart, the fleet account, the season week by "
          "week with the hot case, and what the records read as they stand would have ordered; the workbook's figures.", "",
          "## Critical Components", ""]
    L.append("1. The trade's stock at its summer peak stands **%s** containers above the count of %s over the five types "
             "(%s; band %s)." % (k(f["trade_rise"]), count, each(f, lambda p: k(f["trade_rise_by_pool"][p])),
                                 _b(f["trade_rise_band"])))
    L.append("2. The cold store at its fullest in the 2027 season holds **%s** full containers over the five types (%s; "
             "band %s)." % (k(f["store_2027"]), each(f, lambda p: k(f["store_2027_by_pool"][p])), _b(f["store_2027_band"])))
    L.append("3. The trade lost **%s** containers over the year to the count of %s over the five types (%s; band %s)." % (
        k(f["year_loss"]), count, each(f, lambda p: k(f["year_loss_by_pool"][p])), _b(f["year_loss_band"])))
    L += ["", "## Step-by-Step", ""]
    st = [
        "Put the dockets on one footing (`%s`, %s rows): a docket line a handheld sent twice counted once (%s rows), a "
        "blank container code read from the product (`%s`, %s lines), the three codings brought to one (`%s`) and %s "
        "renumbered accounts read under their current number (`%s`); that gives each type's deliveries for the %d weeks "
        "from %s and each account's and line's dockets by day." % (
            F["dockets"], k(c["docket_rows"]), k(c["resent_rows"]), F["products"], k(c["blank_codes"]), F["codes"],
            k(c["renumbered"]), F["accounts"], c["weeks"], day(c["first_week"])),
        "Built each type's account at the count of %s (`%s`, every site by state, and its tally by the lot on the chime; "
        "`%s`, the lot's prefix dropped): on the register %s and counted on site %s containers. The register strikes a "
        "container only when the wash line condemns it, so it is not the fleet: read as the fleet it files a surplus on "
        "every type (%s)." % (count, F["count"], F["register"], each(f, lambda p: k(A[p]["register"])),
                              five(f, {p: A[p]["on_site"] for p in POOLS}),
                              five(f, {p: f["routes"]["direct"][p]["plan"] for p in POOLS})),
        "Fitted each type's weekly deliveries by least squares on logs: a level, a trend, two yearly harmonics and the "
        "week's mean daily maximum at Calder Vale (`%s`) with a slope either side of a bend set on a half-degree grid "
        "(%s degrees); the level at the count is the fit's value for the week beginning %s at its recorded %s C (the count is "
        "taken on the morning of Monday 30 November 2026, before that week's deliveries; the week beginning 30 November at "
        "its normal and the count week's own dockets are in the battery), as a single week's dockets scatter %s per cent about the fit on 50 litre kegs; the 2027 weeks run at the normal (planning case) or a summer's recorded "
        "weeks (hot case), the Maplestead outlets added from their listing dates in `%s` at the schedule's average weekly "
        "volume over the twelve months to September 2026, shaped by the season. A seasonal profile from the last three "
        "summers as recorded is not the planning case: FS-04 3.2 takes every week at its normal, and the 2024, 2025 and "
        "2026 seasons ran %s, %s and %s C from their normals on average (%s over the three)." % (
            F["weather"], five(f, {p: P[p]["bend_c"] for p in POOLS}, "%.1f"), day(f["level_fit_week"]),
            "%.1f" % f["level_fit_temp"], "%.1f" % (100 * f["level_diag"]["K50"]["scatter"]), F["schedule"],
            *["%.2f" % f["pass3"]["summer_departure"][y] for y in ("2024", "2025", "2026")],
            "%.2f" % f["pass3"]["summer_departure_mean"]),
        "Rebuilt what each checked line held (`%s`, %s line checks on %s calls, a line entered twice on one call taken once, its first entry in the file kept; %s of "
        "those pairs differ): the "
        "TQ-02 form (`%s`) records the full containers and the one on dispense on the account's order day, and the empties "
        "wait for the dray (FS-04 5.1), so each check gets back the line's weekly sales (its share of its type's deliveries over the "
        "record times the type's deliveries that week) times the days since the dray last called at the account over seven (on average %s days and %s containers a "
        "check for 50 litre kegs). Read as they stand the checks give 50 litre kegs %s containers per container sold a "
        "week on a weekly delivery; rebuilt, %s. The checks' own fall is the check: one least-squares fit over all %s "
        "checks of the five types (a line entered twice taken once), each check's full containers and the one on "
        "dispense on, for each type, a constant, the line's weekly sales (the share measure) and those sales times the "
        "weeks between its deliveries, and one common term, the line's weekly sales times the days since the dray last "
        "called over seven: its coefficient is -%s (standard error %s), where a count of the whole holding would not "
        "fall at all. The rebuild adds back one container for each sold; adding back the fit's own %s instead is in the "
        "battery (it files %s)." % (
            F["checks"], k(c["checks"]), k(c["check_calls"]), f["pass3"]["check_doubles_differ"], F["form"], P["K50"]["mean_days"],
            P["K50"]["mean_added_back"], P["K50"]["face_per_sale_weekly"], P["K50"]["per_sale_weekly"], k(fs["checks"]),
            "%.2f" % fs["fall"], fs["se"], "%.2f" % fs["fall"], five(f, {p: nm(f, "recon=pooled", p) for p in POOLS})),
        "Fitted what a line holds by type on the rebuilt checks: a number per line whatever it sells (%s) and a number "
        "per container sold a week that grows with the weeks between deliveries (`%s`); carried to every line supplied "
        "and to the Maplestead lines, the trade's rise from the count to its summer peak is %s, **%s** (Component 1). "
        "Read as they stand the checks give %s." % (
            five(f, {p: P[p]["fixed_per_line"] for p in POOLS}, "%.2f"), F["routes"],
            five(f, f["trade_rise_by_pool"]), k(f["trade_rise"]), k(rc["S1"]["C1"])),
        "Read the loss from the lots (`%s` tally against `%s` by lot and purchase date): the share of each lot found on "
        "site, weighted by the containers found, falls with the lot's age at %s per cent of the fleet a year by type, "
        "with %s of the fleet on site. Each lot on the register times its survival gives %s alive at the count, and the "
        "trade lost %s over the year to the count, **%s** (Component 3): the year's loss is each lot's survivors a year "
        "before the count less its survivors at the count (the lot times its survival at its age a year earlier less at "
        "its age now; no lot was bought in the year). The fitted rate times the fleet alive at the count (%s, %s in all) "
        "and the yearly share leaving times that fleet (%s, %s in all) are in the battery and inside the bands. The "
        "fleet carried forward with the condemnations only loses none. Survival is exponential in a lot's age (one rate "
        "a year, the log of a lot's share on site a straight line in its age, weighted by the containers found); "
        "survival as a straight line in age (each lot's share on site, found over registered, fitted on its age by "
        "least squares weighted by the lot's registered containers over the lots with any found; survival that fit over "
        "its value at age nought, held at nil past the age it reaches nil; the year's loss each surviving lot's "
        "registered containers times the fitted fall a year) fits the lots' found-out-of-registered counts worse by a binomial deviance of %s on 50 litre kegs, %s on 30 litre kegs, %s on 20 litre "
        "kegs, %s on firkins and %s on kilderkins, %s pooled, and is not used (it files %s)." % (
            F["count"], F["register"], five(f, {p: A[p]["leaving_pct"] for p in POOLS}, "%.1f"),
            ", ".join("%.2f" % A[p]["share_on_site"] for p in POOLS), five(f, {p: A[p]["alive"] for p in POOLS}),
            five(f, f["year_loss_by_pool"]), k(f["year_loss"]),
            five(f, {p: nm(f, "loss_form=hazard", p, "year_loss") for p in POOLS}),
            k(f["pass3"]["alone"]["loss_form=hazard"]["total_year_loss"]),
            five(f, {p: nm(f, "loss_form=share", p, "year_loss") for p in POOLS}),
            k(f["pass3"]["alone"]["loss_form=share"]["total_year_loss"]),
            *["%.1f" % f["deviance"][p]["gap"] for p in POOLS], "%.1f" % f["deviance"]["pooled"]["gap"],
            five(f, f["refused"]["survival a straight line in a lot's age"])),
        "Measured the cold store from its Monday position by product (`%s`, the last 104 Mondays) against each "
        "product's deliveries and its racking run (`%s`, the median filled): a beer's stock saws between its cover and "
        "its cover and a run, and a heavy week of deliveries is itself what draws it down, so the beers' means are "
        "fitted, not the weeks inside a beer: each beer's mean stock on its mean weekly deliveries and its run, across "
        "the %s beers, ordinary least squares with no intercept, gives a cover of %s weeks of deliveries and a share of "
        "%s of a run (standard error %s). In the fit and in the projection each Monday's position is the stock at the "
        "close of the week that ended the day before, paired with that week's deliveries. The means barely move with "
        "the pairing (a share of %s with each Monday against the week it opens), and the files take this one: paired "
        "so, no beer's Monday stock falls below %s weeks of its deliveries (the fitted cover), where pairing "
        "each Monday with the week it opens puts the lowest at %s, and on the beer-weeks with one cover the residual "
        "spread is %s containers against %s. The beer-weeks with a cover for each type read %s, because a heavy week draws a "
        "beer down (the 20 litre cover comes out at %s against %s to %s for the other types); that and the beer-weeks "
        "with one cover (%s), the same fit on every Monday of the record (the 156 Mondays from 11 December 2023 to 30 "
        "November 2026, each against the week that ended the day before: %s), the beer-weeks with one cover and each Monday against the "
        "week it opens (%s) and a run as the mean of its rackings are in the battery. "
        "Each type's own regression of its Monday total on deliveries with the intercept read as the share is not used: "
        "it runs from %s to %s by type and window, its runs never having changed in the record. Under the 2027 plan's "
        "runs, range and on-sale dates (`%s`, a new beer at the share of its planned run) the store at its fullest in the "
        "season is %s, **%s** (Component 2). At its fullest over the whole plan year rather than the season the store "
        "holds %s firkins (week beginning %s) and %s kilderkins (week beginning %s), the other types as in the "
        "season, %s in all, inside the bands. Summer 2026's weeks of cover carried to 2027 (%s) give %s, and pass a hold-out of "
        "2026 because the runs did not change in the record; each beer's own weeks of cover carried to its 2027 deliveries "
        "give %s." % (
            F["store"], F["racking"], f["store_fit"]["between"]["n"], "%.3f" % f["store_fit"]["between"]["cover"]["K50"],
            "%.3f" % f["store_fit"]["between"]["share"], "%.3f" % f["store_fit"]["between"]["se"],
            "%.3f" % f["pass3"]["pairing"]["between_open"]["share"], "%.3f" % f["pass3"]["pairing_min_cover"]["ended"][0],
            "%.3f" % f["pass3"]["pairing_min_cover"]["opens"][0], "%.1f" % f["pass3"]["pairing"]["one_cover"]["resid_sd"],
            "%.1f" % f["pass3"]["pairing"]["one_cover_open"]["resid_sd"],
            "%.3f" % f["store_fit"]["panel"]["share"], "%.3f" % f["store_fit"]["panel"]["cover"]["K20"],
            "%.3f" % min(v for q, v in f["store_fit"]["panel"]["cover"].items() if q != "K20"),
            "%.3f" % max(v for q, v in f["store_fit"]["panel"]["cover"].items() if q != "K20"),
            "%.3f" % f["store_fit"]["one_cover"]["share"], "%.3f" % f["store_fit"]["between_all"]["share"],
            "%.3f" % f["pass3"]["pairing"]["one_cover_open"]["share"],
            "%.2f" % f["typeown_range"][0], "%.2f" % f["typeown_range"][1], F["plan"],
            five(f, f["store_2027_by_pool"]), k(f["store_2027"]),
            k(nm(f, "fullest_window=year", "FIR", "fullest")), day(nm(f, "fullest_window=year", "FIR", "fullest_date")),
            k(nm(f, "fullest_window=year", "KIL", "fullest")), day(nm(f, "fullest_window=year", "KIL", "fullest_date")),
            k(f["pass3"]["alone"]["fullest_window=year"]["total_fullest"]), WOC, k(rc["S2"]["C2"]), k(f["beer_cover_C2"])),
        "Ran each week from the count to the week beginning %s (FS-04 2.1 to 2.3). The containers at customers on the "
        "count's day stand in both the requirement and the fleet, so they are estimated once and cancel: a week's "
        "shortfall is the trade's rise since the count, the store, the depots, wash and repair and a float of two "
        "sevenths of the week's deliveries, less the containers counted on site, plus the containers lost and condemned "
        "since. Taking the trade in level instead, from the checks' model for the requirement and from the lots' "
        "survivors for the fleet, counts the two instruments' disagreement at the count (%s) as shortfall and files %s; "
        "it is not used. The rules: the losses and the condemnations accrue per container delivered (step 6's loss and "
        "the year to the count's condemnations, %s, each over that year's deliveries), cumulated week by week from the "
        "count's week, the week itself included; the depots', wash line's and repair bay's count is read against the "
        "count week's own deliveries (%s), which is what they hold, and carried as that many weeks of each 2027 week's "
        "deliveries (the fitted level instead is in the battery). Their own weekly files give the same reading: the "
        "depots' full stock (each Monday's, against the week that ended the day before) and the wash queue (each week's "
        "last daily reading) regressed on the type's deliveries, %s and %s a container delivered on 50 litre kegs, "
        "with the rest scaled, is in the battery, and so is the same with the depots' empties bays held at the count. "
        "The count's empties bays move with deliveries: across the three depots and five types (%s cells) they run "
        "%s to %s of the depot's count-week deliveries, correlation %s, intercept %s containers, so scaling them is "
        "the reading and holding them stays in the battery as a rival. The Maplestead volume is the schedule's twelve-month "
        "average times the type's fitted season for the week, at the week's temperature, over the fitted season's mean "
        "across the same twelve months (October 2025 to September 2026, at their recorded temperatures). The planning "
        "case's largest week (3.1, 3.2) is %s; the hot case, the second highest of the ten summers %s to %s run week by "
        "week (3.3), is %s." % (
            day(f["season"][1]), five(f, f["absolute_gap"]),
            five(f, f["refused"]["the trade in level: the checks' model for the requirement, the lots' survivors for the fleet"]),
            five(f, {p: A[p]["condemned_year"] for p in POOLS}), five(f, {p: A[p]["deliveries_week_last"] for p in POOLS}),
            "%.2f" % f["pass3"]["files_fit"]["K50"]["depot"], "%.2f" % f["pass3"]["files_fit"]["K50"]["wash"],
            f["pass3"]["empties"]["n"], "%.3f" % f["pass3"]["empties"]["ratio_lo"], "%.3f" % f["pass3"]["empties"]["ratio_hi"],
            "%.2f" % f["pass3"]["empties"]["corr"], "%.1f" % f["pass3"]["empties"]["intercept"],
            five(f, f["plan"]), min(f["summers"]["K50"]), max(f["summers"]["K50"]), five(f, f["hot"])),
        "Read the cover on the planning case (4.1) against the minimum runs of `%s`: %s. Rebuilt on %s other "
        "conventions, each alone and every two together (the bands), every cover holds; across those rebuilds the nearest each pool comes to a "
        "line is %s. With each fitted input moved alone the covers hold: %s. Not used: a line's own dockets over thirteen or four weeks for its sales (the fitted holding per "
        "container sold on 20 litre kegs rises from %s on the share to %s and %s, as a line's whole containers lump its "
        "own dockets), the mean of the count's last four weeks for its level (it files %s), a fall for each type on its "
        "own in place of the checks' one fit (the types' own falls are %s, none more than %s standard errors from the "
        "one fit's %s, so the types share one fall and a fall for each adds only its scatter; it files %s), the dray's "
        "last call read as the line's own last docket (FS-04 5.1: the dray collects at its next delivery to the "
        "account, and \"the driver takes every Wrenfold empty on the premises, of every type\"; it files %s) and the "
        "Maplestead volumes flat through the season (Schedule B files each as the average weekly volume over the "
        "twelve months to September 2026, and 50 litre kegs' 2026 season ran at %s times their twelve-month mean "
        "deliveries, the peak week at %s); each files the same covers." % (
            F["quotation"], each(f, lambda p: COVER[f["cover"][p]]), k(f["variants_other"]),
            each(f, lambda p: "%s (%s from %s; %s)" % (k(f["nearest_by_pool"][p]["figure"]), k(f["nearest_by_pool"][p]["distance"]),
                                                       k(f["nearest_by_pool"][p]["line"]), f["nearest_by_pool"][p]["variant"])),
            "; ".join("%s, %s" % (x["input"], five(f, x["plan"])) for x in f["perturbations"]),
            "%.2f" % f["rate_diag"]["count_rate_share"]["slope"]["K20"], "%.2f" % f["rate_diag"]["count_rate13"]["slope"]["K20"],
            "%.2f" % f["rate_diag"]["count_rate"]["slope"]["K20"], five(f, f["level4"]),
            _list("%s %s (%s)" % (pl[p], "%.3f" % f["pass3"]["own_falls"][p][0], "%.3f" % f["pass3"]["own_falls"][p][1])
                  for p in POOLS), "%.1f" % f["pass3"]["own_falls_zmax"], "%.3f" % f["pass3"]["one_fit_fall"],
            five(f, f["refused"]["the fall per container sold left free for each container type on its own"]),
            five(f, f["refused"]["the dray's last call as the line's own last docket, not the account's"]),
            "%.2f" % f["pass3"]["season_ratio"]["K50"][0], "%.2f" % f["pass3"]["season_ratio"]["K50"][1]),
    ]
    for i, s in enumerate(st):
        L.append("%d. %s" % (i + 1, s))
    lat = f["routes"]
    L += ["", "Each estimate is a step of its own, and leaving any out moves the call: without the rebuild of the checks "
          "%s; without the store under the 2027 plan (summer 2026's weeks of cover as step 7 defines them) %s; without the loss from the lots %s (each with the other two "
          "estimates kept and the other two components unmoved). Without two of them together the shortfalls are %s "
          "(checks and store), %s (checks and loss) and %s (store and loss), and without all three %s, in the order 50, "
          "30 and 20 litre kegs, firkins, kilderkins. No other conclusion survives the files: a whole delivery added to "
          "every check puts the trade's rise at %s and half a delivery at %s, where the dockets' own days give %s; the "
          "store regressed on deliveries carries 2026's runs into 2027; the register read as the fleet counts every "
          "container lost since 2011 as stock, and writing off everything it holds beyond the site and the cellars files "
          "%s." % (covers(f, "S1"), covers(f, "S2"), covers(f, "S3"), five(f, {p: lat["S1+S2"][p]["plan"] for p in POOLS}),
                   five(f, {p: lat["S1+S3"][p]["plan"] for p in POOLS}),
                   five(f, {p: lat["S2+S3"][p]["plan"] for p in POOLS}),
                   five(f, {p: lat["S1+S2+S3"][p]["plan"] for p in POOLS}), k(f["allowances"]["whole"]["C1"]),
                   k(f["allowances"]["half"]["C1"]), k(f["trade_rise"]), covers(f, "over S3"))]
    open(path, "w").write("\n".join(L) + "\n")
