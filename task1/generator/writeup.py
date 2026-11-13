"""submission.md, the four answer blocks, drafted from figures.json so every figure is the generator's."""
import deliver as D

PL = ["Flex", "Standaard", "Onbeperkt", "Gezin"]
REG = ["Netherlands", "Flanders"]
CAREFUL = "the careful route: each plan's own past rise in its region, read at the first bill alone"
CROSS1 = "the crossing read, the first bill alone"


def write(path, f):
    c, b = f["change_2027"], f["bands"]
    cr = f["routes"][CAREFUL]
    up = ", ".join(p for p in PL if p in f["raise"])
    L = ["# task1: Kraanvogel Luisterboeken, the January 2027 price rises", "", "## Tags", "",
         "**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer "
         "lifetime value).", "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    hold = ", ".join(p for p in PL if p not in f["raise"])
    x1 = f["routes"][CROSS1]
    L += ["## Final Recommendation", "",
          "Let only Gezin's January 2027 rise go ahead (EUR %.1f per October 2026 subscription in 2027) and hold Flex, "
          "Standaard and Onbeperkt at their 2026 prices: Standaard's rise passes the rival's comparable plan in both "
          "regions (EUR %.1f); Flex's loses more to the light listeners who leave at the December bill after the price "
          "e-mail than it brings (EUR %.1f); Onbeperkt's is lost to those leavers and to the second profile the accounts "
          "that stay add, at EUR %.2f a counted hour (EUR %.1f). Not the careful reading that carries each plan's own "
          "past rise in its region at the first bill and lets %s through, nor one that sees where the rises pass the "
          "rival but stops at the first bill and lets %s through." % (
              c["Gezin"], c["Standaard"], c["Flex"], f["rate"], c["Onbeperkt"],
              " and ".join(cr["raise"]), ", ".join(x1["raise"][:-1]) + " and " + x1["raise"][-1]), ""]
    L += ["## Supplementary Questions", "", "### %s" % D.FILES["wb"], ""]
    L.append("1. Sheet Rises has one row per plan with its 2026 and 2027 price, the paying subscriptions at 31 October "
             "2026, the change in their 2027 contribution if the rise goes ahead, in euros per subscription, and the "
             "decision; sheets Response and Past rises carry the figures below and Base the October subscriptions.")
    L.append("2. Change in the 2027 contribution of the subscriptions paying at 31 October 2026 if the plan's rise "
             "goes ahead, in euros per subscription (band in brackets): " + "; ".join(
                 "%s %.1f (%.1f to %.1f)" % (p, c[p], b["R7"][p][0], b["R7"][p][1]) for p in PL) +
             "; the rise goes ahead on %s; %s hold." % (up, hold.replace(", Onbeperkt", " and Onbeperkt")))
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
    L.append("7. Of each plan's October 2026 subscriptions, still paying at 31 December 2027 if its rise goes ahead "
             "(band in brackets): " + "; ".join("%s %s (%s to %s)" % (p, format(f["paying_end27"][p], ","),
                                                                   format(b["R9"][p][0], ","), format(b["R9"][p][1], ","))
                                                for p in PL) + ".")
    L += ["", "## Critical Components", ""]
    L.append("1. The change in the October subscriptions' 2027 contribution (forecasting): Gezin **EUR %.1f**, Flex "
             "**EUR %.1f**, Standaard **EUR %.1f**, Onbeperkt **EUR %.1f** per subscription." % (
                 c["Gezin"], c["Flex"], c["Standaard"], c["Onbeperkt"]))
    L.append("2. The response around the bill (causal reasoning): at the first bill Standaard loses **%.1f** and moves "
             "down **%.1f** in every 100 in both regions; at the December bill after the e-mail Flex loses **%.1f**, "
             "Standaard **%.1f**, Onbeperkt **%.1f** and Gezin **%.1f** in every 100; Onbeperkt's stayers listen **%.1f** "
             "per cent more from the third month." % (
                 f["extra_cancel"]["Standaard Netherlands"], f["extra_down"]["Standaard Netherlands"],
                 f["announce_pct"]["Flex"], f["announce_pct"]["Standaard"], f["announce_pct"]["Onbeperkt"],
                 f["announce_pct"]["Gezin"], f["use_pct"]["Onbeperkt"]))
    L.append("3. The paying base at 31 October 2026 (assembly): **%s** subscriptions, Standaard **%s**." % (
        format(f["paying_oct_total"], ","), format(f["paying_oct"]["Standaard"], ",")))
    L.append("4. Still paying at 31 December 2027 if the rise goes ahead (forecasting): Gezin **%s** of %s, Onbeperkt "
             "**%s** of %s." % (format(f["paying_end27"]["Gezin"], ","), format(f["paying_oct"]["Gezin"], ","),
                                format(f["paying_end27"]["Onbeperkt"], ","), format(f["paying_oct"]["Onbeperkt"], ",")))
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
        "Carry each 2027 rise at its own region's crossing, on the rival's prices as last scanned (October 2026, "
        "guideline 3.8): Standaard passes the rival in both regions (it never did before, so its own history says "
        "little); Flex, Onbeperkt and Gezin pass it nowhere. Every 2027 rise is the plan's own past rise in euros (Flex "
        "EUR %.2f, the others EUR %.2f), so each past response carries at the size it was read." % (
            f["rise_eur"]["Flex"], f["rise_eur"]["Standaard"]),
        "Read what each past rise did outside its first bill, against the same plan in the other region over the same "
        "months, the mean of each plan's two rises: at the December bill after the price e-mail, of those paying in "
        "November, light listeners left (Flex %s, Standaard %s, Onbeperkt %s, Gezin %s per 100); from the third to the "
        "sixth month the accounts that stayed changed their counted hours by Flex %s, Standaard %s, Onbeperkt %s and Gezin "
        "%s per cent, Onbeperkt's single users having started to share the profile the plan pays for; every rate is "
        "carried to every 2027 rise in both regions (they are e-mailed on 1 December)." % (
            f["announce_pct"]["Flex"], f["announce_pct"]["Standaard"], f["announce_pct"]["Onbeperkt"],
            f["announce_pct"]["Gezin"], f["use_pct"]["Flex"], f["use_pct"]["Standaard"], f["use_pct"]["Onbeperkt"],
            f["use_pct"]["Gezin"]),
        "Value what is lost: those who leave at a crossing rise are the heavy listeners, whose counted hours at EUR "
        "%.2f eat most of what they pay; those who leave at the e-mail are light listeners, each worth what an October "
        "subscription on the plan brings in 2027 at the held price, on the plan's continuation by tenure and their own "
        "listening; the stayers' extra hours cost EUR 0.40 each from April 2027; "
        "those who move down keep paying on the cheaper plan, valued on the past downgraders' own months (Onbeperkt EUR "
        "%.1f each in 2027)." % (f["rate"], f["downgrader_value"]["Onbeperkt"]),
        "Net it per October subscription against the rise's gain: Flex %.1f, Standaard %.1f, Onbeperkt %.1f, Gezin "
        "%.1f euros; the rise goes ahead on %s only (guideline 3.10); %s of the %s October subscriptions are still paying "
        "at the end of 2027." % (c["Flex"], c["Standaard"], c["Onbeperkt"], c["Gezin"], up,
                                 format(f["paying_end27_total"], ","), format(f["paying_oct_total"], ",")),
        "The shortcuts land elsewhere: each plan's own past rise in its region at the first bill (the careful route) "
        "lets %s through; reading the crossing but stopping at the first bill lets %s through; leaving out the "
        "December leavers lets Flex through and leaving out the stayers' listening lets Onbeperkt through; the 2026 "
        "revenue share and one response for every rise land elsewhere again." % (
            " and ".join(cr["raise"]), ", ".join(x1["raise"])),
    ]
    for i, st in enumerate(steps, 1):
        L.append("%d. %s" % (i, st))
    L += ["", "No other conclusion survives the records. The past rises answered where they passed the rival and "
          "barely elsewhere, in each plan that had both kinds, so neither one response for every rise nor each plan's "
          "own history carries to 2027, where the crossings fall differently; a downgrade keeps the subscription "
          "paying; the leavers and the downgraders listen differently from their plan's average; and schedule B "
          "prices every counted hour; and a rise is answered at the December bill after its e-mail and in the hours of "
          "those who stay, not only at its first bill. Every rival control, window, downgrader valuation, dose form and "
          "perturbation lets the same one rise through.", ""]
    open(path, "w").write("\n".join(L))
