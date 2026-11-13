"""submission.md, the four answer blocks, drafted from figures.json so every figure is the generator's."""
import deliver as D

PL = ["Flex", "Standaard", "Onbeperkt", "Gezin"]
REG = ["Netherlands", "Flanders"]
CAREFUL = "the careful route: no return after a stop, the stayers listening as before"
RET1 = "returns after a stop, the stayers listening as before"
SAL1 = "the stayers' extra listening, no return after a stop"
TOGETHER = "the careful route with each plan's own rises read together"
POOLED = "the careful route with one response for every rise"


def _and(xs):
    xs = list(xs)
    if not xs:
        return "none"
    return xs[0] if len(xs) == 1 else ", ".join(xs[:-1]) + " and " + xs[-1]


def _band(v, b, nd=1):
    return "%.*f (%.*f to %.*f)" % (nd, v, nd, b[0], nd, b[1])


def write(path, f):
    c, b = f["change_2027"], f["bands"]
    R = f["routes"]
    up, hold = f["raise"], f["hold"]
    L = ["# task1: Kraanvogel Luisterboeken, the January 2027 price rises", "", "## Tags", "",
         "**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer "
         "lifetime value).", "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## Final Recommendation", "",
          "Let %s's and %s's January 2027 rises go ahead (EUR %.1f and EUR %.1f per October 2026 subscription in "
          "2027) and hold %s (EUR %.1f, its rise passing the rival's Basis 10 uur) and %s (EUR %.1f): many of those "
          "Standaard loses at the December and first bills take a plan up again within the year at the new price, "
          "and Onbeperkt's subscriptions that stay listen about %.0f counted hours more each in 2027, every one of them "
          "paid at EUR %.2f. Not the careful reading that treats a stop as final and the stayers' listening as unchanged and lets "
          "%s through, nor one that adds the returns alone (%s) or the stayers' listening alone (%s)." % (
              up[1], up[0], c[up[1]], c[up[0]], "Flex", c["Flex"], "Onbeperkt", c["Onbeperkt"],
              f["sal_hours"]["Onbeperkt"], f["rate"], _and(R[CAREFUL]["raise"]), _and(R[RET1]["raise"]),
              _and(R[SAL1]["raise"]) + " only"), ""]
    L += ["## Supplementary Questions", "", "### %s" % D.FILES["wb"], ""]
    L.append("1. Sheet Rises has one row per plan with its 2026 and 2027 price, the paying subscriptions at 31 October "
             "2026, the change in their 2027 contribution with the rise, how many of them pay on any plan at 31 "
             "December 2027, the 2027 publisher remuneration on them and the decision; sheets First bill, Past rises, "
             "Stopped and back, Stayers' listening, Base and Other readings carry the figures below.")
    L.append("2. Change in the 2027 contribution of the subscriptions paying at 31 October 2026 if the plan's rise "
             "goes ahead, in euros per subscription (band in brackets): " +
             "; ".join("%s %s" % (p, _band(c[p], b["R7"][p])) for p in PL) +
             "; the rise goes ahead on %s and holds on %s." % (_and(up), _and(hold)))
    L += ["", "### %s" % D.FILES["deck"], ""]
    L.append("3. A short deck that opens on the decision, then a column chart of each plan's change, what a rise "
             "loses and what comes back, the stayers' listening, and the base with its 2027 publisher cost.")
    L.append("4. Paying subscriptions at 31 October 2026, by plan (exact): " + "; ".join(
        "%s %s" % (p, format(f["paying_oct"][p], ",")) for p in PL) + "; %s in all." % format(f["paying_oct_total"], ","))
    L.append("5. Of each plan's October 2026 subscriptions, paying on any plan at 31 December 2027 if its rise goes "
             "ahead (band in brackets): " + "; ".join("%s %s (%s to %s)" % (
                 p, format(f["paying_end27"][p], ","), format(b["R9"][p][0], ","), format(b["R9"][p][1], ","))
                 for p in PL) + ".")
    L.append("6. The 2027 publisher remuneration on them if the rise goes ahead, in euros per October subscription "
             "(band in brackets): " + "; ".join("%s %s" % (p, _band(f["remun_2027"][p], b["R2"][p])) for p in PL) + ".")
    L.append("7. Extra cancellations per 100 subscriptions reaching the first bill at the 2027 price (band in "
             "brackets): " + "; ".join("%s %s %s" % (p, r, _band(f["extra_cancel"]["%s %s" % (p, r)],
                                                                 b["R3"]["%s %s" % (p, r)])) for p in PL for r in REG) + ".")
    L.append("8. Extra downgrades per 100 at that bill (band in brackets; Flex has no plan below it): " + "; ".join(
        "%s %s %s" % (p, r, _band(f["extra_down"]["%s %s" % (p, r)], b["R4"]["%s %s" % (p, r)]))
        for p in PL[1:] for r in REG) + ".")
    L += ["", "## Critical Components", ""]
    L.append("1. The change in the October subscriptions' 2027 contribution with the rise (forecasting; bands as in "
             "question 2): Standaard **EUR %.1f**, Gezin **EUR %.1f**, Flex **EUR %.1f**, Onbeperkt **EUR %.1f** per "
             "subscription." % (c["Standaard"], c["Gezin"], c["Flex"], c["Onbeperkt"]))
    bb, bs = b["R5"], b["R6"]
    L.append("2. The stops that come back (modeling): of every 100 October subscriptions that stop by December 2027 "
             "with the rise, those paying again then (band in brackets): Flex **%.0f** (%.0f to %.0f), Standaard "
             "**%.0f** (%.0f to %.0f), Onbeperkt **%.0f** (%.0f to %.0f), Gezin **%.0f** (%.0f to %.0f); light "
             "listeners come back soonest (of 100 that stop in December, about %.0f with under 3 counted hours a month "
             "pay again within a year, about %.0f with 20 and more)." % (
                 f["back_share"]["Flex"], bb["Flex"][0], bb["Flex"][1], f["back_share"]["Standaard"],
                 bb["Standaard"][0], bb["Standaard"][1], f["back_share"]["Onbeperkt"], bb["Onbeperkt"][0],
                 bb["Onbeperkt"][1], f["back_share"]["Gezin"], bb["Gezin"][0], bb["Gezin"][1],
                 f["back12_by_band"]["under 3"], f["back12_by_band"]["20 and more"]))
    L.append("3. The stayers' listening (causal reasoning): the subscriptions that stay after a rise listen more, "
             "Onbeperkt's about %.0f per cent more in the first month after the bill, fading over about %.0f months; "
             "extra counted hours over 2027 for each subscription staying on the plan all year (band in brackets): "
             "Onbeperkt **%.1f** (%.1f to %.1f), Gezin **%.1f** (%.1f to %.1f), Standaard **%.1f** (%.1f to %.1f), "
             "Flex **%.1f** (%.1f to %.1f)." % (
                 f["uplift_first_month"]["Onbeperkt"], f["fade_months"], f["sal_hours"]["Onbeperkt"],
                 bs["Onbeperkt"][0], bs["Onbeperkt"][1], f["sal_hours"]["Gezin"], bs["Gezin"][0], bs["Gezin"][1],
                 f["sal_hours"]["Standaard"], bs["Standaard"][0], bs["Standaard"][1], f["sal_hours"]["Flex"],
                 bs["Flex"][0], bs["Flex"][1]))
    L += ["", "## Step-by-Step", ""]
    ev = f["events"]
    cross = [e for e in ev if e["crossed"]]
    steps = [
        "From payments_2024-01_2026-10.csv and accounts_export_2026-11-03.csv, count each consumer account's "
        "collected monthly charge once: %s paying subscriptions at 31 October 2026 (guideline 3.1)." % format(
            f["paying_oct_total"], ","),
        "Rebuild schedule B's counted hours per profile and title from listening_monthly_2024-01_2026-10.csv and "
        "licence_server_renewals_2024-01_2026-10.csv, each profile on the account its charge lists that month: "
        "Onbeperkt %.2f and Gezin %.2f counted hours per paying month, Flex %.2f." % (
            f["counted_per_month"]["Onbeperkt"], f["counted_per_month"]["Gezin"], f["counted_per_month"]["Flex"]),
        "Read the eight past rises (price_list_2027.pdf dates them and their 1 December e-mails) against the same "
        "plan in the other region over the same months (guideline 3.10): the %d whose new price passed the rival's "
        "comparable plan (rival_price_scan_2024-01_2026-10.csv, the December scan, promotions out) lost %s per 100 "
        "at the first bill, the others %s; at the December bill after the e-mail Flex lost %.1f, Standaard %.1f, "
        "Onbeperkt %.1f and Gezin %.1f per 100 (each plan's two rises)." % (
            len(cross), ", ".join("%.1f" % e["extra_cancel"] for e in cross),
            ", ".join("%.1f" % e["extra_cancel"] for e in ev if not e["crossed"]), f["announce_pct"]["Flex"],
            f["announce_pct"]["Standaard"], f["announce_pct"]["Onbeperkt"], f["announce_pct"]["Gezin"]),
        "Carry the first bill to 2027 by listening band in proportion to each rise, the downgrades among "
        "subscriptions whose profiles fit the plan below, on the rival's prices as last scanned (October 2026, "
        "guideline 3.8; in July 2026 the rival raised its Basis 10 uur to EUR %.2f and brought its Flemish "
        "Onbeperkt and Familie to its Dutch prices, so every plan sits below the rival in both regions before the "
        "rise): in both regions only Flex's 2027 price passes the rival, as both of Flex's past rises did, so Flex "
        "loses %.1f per 100 and Standaard %.1f (moving %.1f down), Onbeperkt %.1f and Gezin %.1f." % (
            f["rival_2027"]["Flex Netherlands"], f["extra_cancel"]["Flex Netherlands"],
            f["extra_cancel"]["Standaard Netherlands"], f["extra_down"]["Standaard Netherlands"],
            f["extra_cancel"]["Onbeperkt Netherlands"], f["extra_cancel"]["Gezin Netherlands"]),
        "Follow every stop since 2024 in the payments and plan periods: a subscription that stops takes its plan up "
        "again on the same account at a monthly chance that falls with the months since, rises before the summer and "
        "is highest for light listeners (%.0f in 100 of the lightest December stops pay again within a year, %.0f of "
        "the heaviest), paying the price then in force. A forecast that treats a stop as the end puts %s of the "
        "%s October subscriptions on Flex at the end of 2027 instead of %s and holds Standaard (EUR %.1f)." % (
            f["back12_by_band"]["under 3"], f["back12_by_band"]["20 and more"],
            format(f["careful"]["paying_end27"]["Flex"], ","), format(f["paying_oct"]["Flex"], ","),
            format(f["paying_end27"]["Flex"], ","), R[SAL1]["change_2027"]["Standaard"]),
        "Measure the stayers' listening within accounts: the accounts on the plan through each month after a past "
        "rise, against their own October to December hours, the rising region against the other (a plan's average "
        "would count the light leavers' absence as listening); Onbeperkt's stayers listened %.1f per cent more in "
        "the first month, fading over about %.1f months, Standaard's %.1f and Gezin's %.1f. Carrying each account's "
        "recent hours passes a pooled holdout and misses it: Onbeperkt's rise then adds EUR %.1f." % (
            f["uplift_first_month"]["Onbeperkt"], f["fade_months"], f["uplift_first_month"]["Standaard"],
            f["uplift_first_month"]["Gezin"], R[RET1]["change_2027"]["Onbeperkt"]),
        "Carry each October subscription month by month to December 2027 with the rise and with the 2026 price held, "
        "on its own paying months, listening, country and route: net revenue after VAT and the store's fee, less "
        "EUR %.2f per counted hour (schedule B 2.1), the stayers' extra hours from January; downgraders on the past "
        "downgraders' own months." % f["rate"],
        "Net it per October subscription: Flex %.1f, Standaard %.1f, Onbeperkt %.1f, Gezin %.1f euros; the rise goes "
        "ahead on %s (guideline 3.10). With the rises, %s of the %s October subscriptions pay on some plan at the end "
        "of 2027, and the 2027 remuneration on them is EUR %.1f (Onbeperkt) to EUR %.1f (Flex) each." % (
            c["Flex"], c["Standaard"], c["Onbeperkt"], c["Gezin"], _and(up), format(f["paying_end27_total"], ","),
            format(f["paying_oct_total"], ","), f["remun_2027"]["Onbeperkt"], f["remun_2027"]["Flex"]),
        "The shortcuts land elsewhere: the careful reading (no return after a stop, the stayers as before) lets %s "
        "through; with the returns alone %s; with the stayers' listening alone %s only; reading each plan's two "
        "past rises together, without asking whether they passed the rival, %s; one response for every rise, %s." % (
            _and(R[CAREFUL]["raise"]), _and(R[RET1]["raise"]), _and(R[SAL1]["raise"]), _and(R[TOGETHER]["raise"]),
            _and(R[POOLED]["raise"])),
    ]
    for i, st in enumerate(steps, 1):
        L.append("%d. %s" % (i, st))
    L += ["", "No other conclusion survives the records. Standaard's rise pays only because a good share of the "
          "subscriptions it loses come back within the year at the higher price, which the payments of every past "
          "stop show; Onbeperkt's fails only because the accounts that stay listen more for months after the bill, "
          "which their own hours against the other region show, and each of those hours now costs EUR %.2f; Flex's "
          "2027 price passes the rival as its 2025 Dutch rise did; Gezin's gain holds either way. Every rival control, "
          "window, dose form, continuation, downgrader valuation and fade, and each fitted response moved 20 per "
          "cent, lets the same two rises through." % f["rate"], ""]
    open(path, "w").write("\n".join(L))
