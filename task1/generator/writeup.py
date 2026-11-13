"""submission.md, the four answer blocks, drafted from figures.json so every figure is the generator's."""
import deliver as D

PL = ["Flex", "Standaard", "Onbeperkt", "Gezin"]
REG = ["Netherlands", "Flanders"]
CAREFUL = "the careful route: each plan's own past response, a downgrade counted as an exit, leavers at the plan's average"


def write(path, f):
    c, b = f["change_2027"], f["bands"]
    cr = f["routes"][CAREFUL]
    up = ", ".join(p for p in PL if p in f["raise"])
    L = ["# task1: Kraanvogel Luisterboeken, the January 2027 price rises", "", "## Tags", "",
         "**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer "
         "lifetime value).", "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## Final Recommendation", "",
          "Let the January 2027 rises go ahead on %s and hold Standaard at its 2026 price: Standaard's rise "
          "passes the rival's comparable plan in both regions and changes the 2027 contribution of its October "
          "subscriptions by EUR %.1f each, "
          "while the others gain (Flex EUR %.1f, Onbeperkt EUR %.1f, Gezin EUR %.1f). Not the careful reading that "
          "lets all four through on each plan's own past response (Standaard EUR %.1f), nor one that counts a "
          "downgrade as a lost subscription and so holds Onbeperkt." % (
              up, c["Standaard"], c["Flex"], c["Onbeperkt"],
              c["Gezin"], cr["change_2027"]["Standaard"]), ""]
    L += ["## Supplementary Questions", "", "### %s" % D.FILES["wb"], ""]
    L.append("1. Sheet Rises has one row per plan with its 2026 and 2027 price, the paying subscriptions at 31 October "
             "2026, the change in their 2027 contribution if the rise goes ahead, in euros per subscription, and the "
             "decision; sheets Response and Past rises carry the figures below and Base the October subscriptions.")
    L.append("2. Change in the 2027 contribution of the subscriptions paying at 31 October 2026 if the plan's rise "
             "goes ahead, in euros per subscription (band in brackets): " + "; ".join(
                 "%s %.1f (%.1f to %.1f)" % (p, c[p], b["R7"][p][0], b["R7"][p][1]) for p in PL) +
             "; the rises go ahead on %s and Standaard holds." % up)
    L += ["", "### %s" % D.FILES["deck"], ""]
    L.append("3. A short deck that opens on the decision, then a column chart of each plan's change, the past rises' "
             "response table, and the base.")
    L.append("4. Paying subscriptions at 31 October 2026, by plan (exact): " + "; ".join(
        "%s %s" % (p, format(f["paying_oct"][p], ",")) for p in PL) + "; %s in all." % format(f["paying_oct_total"], ","))
    L.append("5. Extra cancellations per 100 subscriptions at the first bill at the 2027 price (band in brackets): " +
             "; ".join("%s %s %.1f (%.1f to %.1f)" % (p, r, f["extra_cancel"]["%s %s" % (p, r)],
                                                      b["R3"]["%s %s" % (p, r)][0], b["R3"]["%s %s" % (p, r)][1])
                       for p in PL for r in REG) + ".")
    L.append("6. Extra downgrades per 100 subscriptions at that bill (band in brackets; Flex has no plan below it): " +
             "; ".join("%s %s %.1f (%.1f to %.1f)" % (p, r, f["extra_down"]["%s %s" % (p, r)],
                                                      b["R4"]["%s %s" % (p, r)][0], b["R4"]["%s %s" % (p, r)][1])
                       for p in PL[1:] for r in REG) + ".")
    L += ["", "## Critical Components", ""]
    L.append("1. The change in the October subscriptions' 2027 contribution (forecasting): Standaard **EUR %.1f**, Flex "
             "**EUR %.1f**, Onbeperkt **EUR %.1f**, Gezin **EUR %.1f** per subscription." % (
                 c["Standaard"], c["Flex"], c["Onbeperkt"], c["Gezin"]))
    L.append("2. The response at the first bill (causal reasoning): Standaard loses **%.1f** and moves down **%.1f** in "
             "every 100 in both regions, Onbeperkt **%.1f** and **%.1f** in the Netherlands against **%.1f** and **%.1f** "
             "in Flanders." % (f["extra_cancel"]["Standaard Netherlands"], f["extra_down"]["Standaard Netherlands"],
                               f["extra_cancel"]["Onbeperkt Netherlands"], f["extra_down"]["Onbeperkt Netherlands"],
                               f["extra_cancel"]["Onbeperkt Flanders"], f["extra_down"]["Onbeperkt Flanders"]))
    L.append("3. The paying base at 31 October 2026 (assembly): **%s** subscriptions, Standaard **%s**." % (
        format(f["paying_oct_total"], ","), format(f["paying_oct"]["Standaard"], ",")))
    L += ["", "## Step-by-Step", ""]
    ev = f["events"]
    cross = [e for e in ev if e["crossed"]]
    steps = [
        "From payments_2024-01_2026-10.csv and accounts_export_2026-11-03.csv, count each consumer account's "
        "collected monthly charge once: %s paying subscriptions at 31 October 2026 (guideline 3.1)." % format(
            f["paying_oct_total"], ","),
        "Rebuild schedule B's counted hours per profile and title from listening_monthly_2024-01_2026-10.csv and "
        "licence_server_renewals_2024-01_2026-10.csv, each profile on the account its charge lists that month: "
        "Onbeperkt %.2f and Standaard %.2f counted hours per paying month." % (
            f["counted_per_month"]["Onbeperkt"], f["counted_per_month"]["Standaard"]),
        "Find the 2025 and 2026 January rises in the charges by plan and region and read each one's extra "
        "cancellations and downgrades at the first bill against the same plan in the other region (guideline 3.10): "
        "the %d that took the price past the rival's comparable plan (rival_price_scan_2024-01_2026-10.csv, the "
        "December scan, promotions left out) lost %s per 100, the others %s." % (
            len(cross), ", ".join("%.1f" % e["extra_cancel"] for e in cross),
            ", ".join("%.1f" % e["extra_cancel"] for e in ev if not e["crossed"])),
        "Carry each 2027 rise at its own region's crossing: Standaard passes the rival in both regions (it never did "
        "before, so its own history says little), Onbeperkt and Gezin in the Netherlands only, Flex nowhere.",
        "Value what is lost: those who leave at a crossing rise are the heavy listeners, whose counted hours at EUR "
        "%.2f eat most of what they pay, and those who move down are light listeners still paying on the cheaper "
        "plan, valued on the past downgraders' own months (Onbeperkt EUR %.1f each in 2027)." % (
            f["rate"], f["downgrader_value"]["Onbeperkt"]),
        "Net it per October subscription against the rise's gain: Flex %.1f, Standaard %.1f, Onbeperkt %.1f, Gezin "
        "%.1f euros; the rises go ahead on %s (guideline 3.10)." % (c["Flex"], c["Standaard"], c["Onbeperkt"],
                                                                  c["Gezin"], up),
        "The shortcuts land elsewhere: each plan's own past response lets all four through (Standaard %.1f); one "
        "response scaled by the rise lets all four through; counting a downgrade as an exit holds Onbeperkt; the "
        "2026 revenue share holds Onbeperkt and Gezin; reading the response off the gap to the rival in a straight "
        "line holds all four." % cr["change_2027"]["Standaard"],
    ]
    for i, st in enumerate(steps, 1):
        L.append("%d. %s" % (i, st))
    L += ["", "No other conclusion survives the records. The past rises answered where they passed the rival and "
          "barely elsewhere, in each plan that had both kinds, so neither one response for every rise nor each plan's "
          "own history carries to 2027, where the crossings fall differently; a downgrade keeps the subscription "
          "paying; the leavers and the downgraders listen differently from their plan's average; and schedule B "
          "prices every counted hour. Every rival control, window and downgrader valuation lets the same three rises "
          "through.", ""]
    open(path, "w").write("\n".join(L))
