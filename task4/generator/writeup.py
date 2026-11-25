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
        if abs(x) < 0.05 * f["min_run"][p]:
            out.append("next to nothing for %s (%s, about nil)" % (f["plural"][p], k(x)))
        else:
            out.append("%s for %s (%s)" % ({"buy": "a purchase", "hire": "a seasonal hire", "nothing": "no cover"}[r[p]["cover"]],
                                            f["plural"][p], k(x)))
    return _list(out)


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
        "register less the condemned as the fleet), which orders %s." % (
            deliver.headline(f), each(f, lambda p: k(f["plan"][p])), _list(k(f["min_run"][p]) for p in POOLS),
            reflex_words(f)))
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
        "its normal is in the battery), as a single week's dockets scatter %s per cent about the fit on 50 litre kegs; the 2027 weeks run at the normal (planning case) or a summer's recorded "
        "weeks (hot case), the Maplestead outlets added from their listing dates in `%s` at the schedule's average weekly "
        "volume over the twelve months to September 2026, shaped by the season." % (
            F["weather"], five(f, {p: P[p]["bend_c"] for p in POOLS}, "%.1f"), day(f["level_fit_week"]),
            "%.1f" % f["level_fit_temp"], "%.1f" % (100 * f["level_diag"]["K50"]["scatter"]), F["schedule"]),
        "Rebuilt what each checked line held (`%s`, %s line checks on %s calls, a line entered twice taken once): the "
        "TQ-02 form (`%s`) records the full containers and the one on dispense on the account's order day, and the empties "
        "wait for the dray (FS-04 5.1), so each check gets back the line's weekly sales (its share of its type's deliveries over the "
        "record times the type's deliveries that week) times the days since the dray last called at the account over seven (on average %s days and %s containers a "
        "check for 50 litre kegs). Read as they stand the checks give 50 litre kegs %s containers per container sold a "
        "week on a weekly delivery; rebuilt, %s. The checks' own fall is the check: one least-squares fit over all %s "
        "checks of the five types (a line entered twice taken once), each check's full containers and the one on "
        "dispense on, for each type, a constant, the line's weekly sales (the share measure) and those sales times the "
        "weeks between its deliveries, and one common term, the line's weekly sales times the days since the dray last "
        "called over seven: its coefficient is -%s (standard error %s), where a count of the whole holding would not "
        "fall at all." % (
            F["checks"], k(c["checks"]), k(c["check_calls"]), F["form"], P["K50"]["mean_days"],
            P["K50"]["mean_added_back"], P["K50"]["face_per_sale_weekly"], P["K50"]["per_sale_weekly"], k(fs["checks"]),
            "%.2f" % fs["fall"], fs["se"]),
        "Fitted what a line holds by type on the rebuilt checks: a number per line whatever it sells (%s) and a number "
        "per container sold a week that grows with the weeks between deliveries (`%s`); carried to every line supplied "
        "and to the Maplestead lines, the trade's rise from the count to its summer peak is %s, **%s** (Component 1). "
        "Read as they stand the checks give %s." % (
            five(f, {p: P[p]["fixed_per_line"] for p in POOLS}, "%.2f"), F["routes"],
            five(f, f["trade_rise_by_pool"]), k(f["trade_rise"]), k(rc["S1"]["C1"])),
        "Read the loss from the lots (`%s` tally against `%s` by lot and purchase date): the share of each lot found on "
        "site, weighted by the containers found, falls with the lot's age at %s per cent of the fleet a year by type, "
        "with %s of the fleet on site. Each lot on the register times its survival gives %s alive at the count, and the "
        "trade lost %s over the year to the count, **%s** (Component 3); the fleet carried forward with the "
        "condemnations only loses none." % (
            F["count"], F["register"], five(f, {p: A[p]["leaving_pct"] for p in POOLS}, "%.1f"),
            ", ".join("%.2f" % A[p]["share_on_site"] for p in POOLS), five(f, {p: A[p]["alive"] for p in POOLS}),
            five(f, f["year_loss_by_pool"]), k(f["year_loss"])),
        "Measured the cold store from its Monday position by product (`%s`, the last 104 Mondays) against each "
        "product's deliveries and its racking run (`%s`, the median filled): a beer's stock saws between its cover and "
        "its cover and a run, and a heavy week of deliveries is itself what draws it down, so the beers' means are "
        "fitted, not the weeks inside a beer: each beer's mean stock on its mean weekly deliveries and its run, across "
        "the %s beers, ordinary least squares with no intercept, gives a cover of %s weeks of deliveries and a share of "
        "%s of a run (standard error %s). The beer-weeks with a cover for each type read %s, because a heavy week draws a "
        "beer down (the 20 litre cover comes out at %s against %s to %s for the other types); that and the beer-weeks "
        "with one cover (%s), the same fit on every Monday (%s) and a run as the mean of its rackings are in the battery. "
        "Each type's own regression of its Monday total on deliveries with the intercept read as the share is not used: "
        "it runs from %s to %s by type and window, its runs never having changed in the record. Under the 2027 plan's "
        "runs, range and on-sale dates (`%s`, a new beer at the share of its planned run) the store at its fullest in the "
        "season is %s, **%s** (Component 2). Summer 2026's weeks of cover carried to 2027 give %s, and pass a hold-out of "
        "2026 because the runs did not change in the record; each beer's own weeks of cover carried to its 2027 deliveries "
        "give %s." % (
            F["store"], F["racking"], f["store_fit"]["between"]["n"], "%.3f" % f["store_fit"]["between"]["cover"]["K50"],
            "%.3f" % f["store_fit"]["between"]["share"], "%.3f" % f["store_fit"]["between"]["se"],
            "%.3f" % f["store_fit"]["panel"]["share"], "%.3f" % f["store_fit"]["panel"]["cover"]["K20"],
            "%.3f" % min(v for q, v in f["store_fit"]["panel"]["cover"].items() if q != "K20"),
            "%.3f" % max(v for q, v in f["store_fit"]["panel"]["cover"].items() if q != "K20"),
            "%.3f" % f["store_fit"]["one_cover"]["share"], "%.3f" % f["store_fit"]["between_all"]["share"],
            "%.2f" % f["typeown_range"][0], "%.2f" % f["typeown_range"][1], F["plan"],
            five(f, f["store_2027_by_pool"]), k(f["store_2027"]), k(rc["S2"]["C2"]), k(f["beer_cover_C2"])),
        "Ran each week from the count to the week beginning %s (FS-04 2.1 to 2.3): the trade's rise, the store, the "
        "depots, wash and repair at the count's weeks of deliveries, and a float of two sevenths, less the containers on "
        "site at the count, plus the containers lost and condemned since. The planning case's largest week (3.1, 3.2) is "
        "%s; the hot case, the second highest of the ten summers %s to %s run week by week (3.3), is %s." % (
            day(f["season"][1]), five(f, f["plan"]), min(f["summers"]["K50"]), max(f["summers"]["K50"]), five(f, f["hot"])),
        "Read the cover on the planning case (4.1) against the minimum runs of `%s`: %s. Rebuilt on %s other "
        "conventions, each alone and every two together (the bands), every cover holds, the nearest %s containers from "
        "a line, and so it does with each fitted input moved 20 per cent (deliveries 5) or all four by two measured "
        "spreads. Not used: a line's own dockets over thirteen or four weeks for its sales (the fitted holding per "
        "container sold on 20 litre kegs rises from %s on the share to %s and %s, as a line's whole containers lump its "
        "own dockets), the count's own recorded week for its level (%s per cent off the fit, a week's scatter) and the mean of its last "
        "four weeks (it files %s, the same covers), the fall per "
        "container sold left free (its slope's standard error %s against the rebuild's %s on 50 litre kegs) and the "
        "Maplestead volumes flat through the season (Schedule B files each as the average weekly volume over the "
        "twelve months to September 2026); each files the "
        "same covers." % (
            F["quotation"], each(f, lambda p: COVER[f["cover"][p]]), k(f["variants"] - 1), k(f["nearest_variant"]["distance"]),
            "%.2f" % f["rate_diag"]["count_rate_share"]["slope"]["K20"], "%.2f" % f["rate_diag"]["count_rate13"]["slope"]["K20"],
            "%.2f" % f["rate_diag"]["count_rate"]["slope"]["K20"], "%.1f" % (100 * f["level_diag"]["K50"]["count_week"]), five(f, f["level4"]),
            "%.3f" % f["slope_se"]["K50"]["joint"], "%.3f" % f["slope_se"]["K50"]["rebuild"]),
    ]
    for i, s in enumerate(st):
        L.append("%d. %s" % (i + 1, s))
    lat = f["routes"]
    L += ["", "Each estimate is a step of its own, and leaving any out moves the call: without the rebuild of the checks "
          "%s; without the store under the 2027 plan %s; without the loss from the lots %s (each with the other two "
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
