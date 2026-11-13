"""submission.md, the four answer blocks, drafted from figures.json so every figure is the generator's."""
import deliver as D

PL = ["Flex", "Standaard", "Onbeperkt", "Gezin"]
CAREFUL = "the careful route: the live roll-up's positions, today's profile export"
LIC = "the licence renewals merged, today's profile export"
MEM = "the live roll-up's positions, the profiles each charge lists"
SHARE = "the 2026 remuneration basis carried (52 per cent of net revenue)"


def eur(v, nd=1):
    return ("EUR %." + str(nd) + "f") % v


def write(path, f):
    c, R = f["contribution"], f["routes"]
    cr, lr, mr, sr = R[CAREFUL], R[LIC], R[MEM], R[SHARE]
    b5, b2 = f["bands"]["contribution"], f["bands"]["counted_per_month"]
    s24 = f["spring24"]
    lead = f["lead_plan"]
    L = []
    L += ["# task1: Kraanvogel Luisterboeken, the spring 2027 campaign's lead plan", "",
          "## Tags", "",
          "**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer "
          "lifetime value).",
          "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    L += ["## Final Recommendation", "",
          "Lead the spring 2027 campaign with %s: its trial starts bring %s each over their first 24 months after the "
          "publishers' EUR %.2f per counted hour and the agency's fee, %s ahead of %s (%s). Not Onbeperkt, which the "
          "live listening log values at %s only because it misses the listening of downloaded titles and credits "
          "profiles to the accounts they sit on today; counted in full, Onbeperkt brings %s." % (
              lead, eur(c[lead]), f["rate"], eur(f["lead_margin_eur"]), f["runner_up"], eur(c[f["runner_up"]]),
              eur(cr["contribution"]["Onbeperkt"]), eur(c["Onbeperkt"])), ""]
    L += ["## Supplementary Questions", "", "### %s" % D.FILES["wb"], ""]
    L.append("1. Sheet Lead plan has one row per plan (Flex, Standaard, Onbeperkt, Gezin) with the spring 2024 trial "
             "starts, the share paying after the trial, paying months, net revenue at 2027 prices, counted hours, "
             "remuneration at EUR %.2f an hour, the agency's fee and the contribution per trial start, and the lead "
             "plan under the table." % f["rate"])
    L.append("2. Contribution per trial start over its first 24 months, after the agency's fee, in euros (band in "
             "brackets): " + "; ".join("%s %.1f (%.1f to %.1f)" % (p, c[p], b5[p][0], b5[p][1])
                                        for p in PL) + "; the campaign leads with %s." % lead)
    L += ["", "### %s" % D.FILES["deck"], ""]
    L.append("3. A short deck that opens on the lead plan (%s, %s per trial start) with the contribution of every "
             "plan in a column chart, then the base and its listening, then the spring 2024 trial starts." % (
                 lead, eur(c[lead])))
    L.append("4. Paying subscriptions at 31 October 2026, by plan (exact): " + "; ".join(
        "%s %s" % (p, format(f["paying_oct"][p], ",")) for p in PL) + "; %s in all." % format(f["paying_oct_total"], ","))
    L.append("5. Counted hours per paying subscription-month, November 2025 to October 2026, by plan (band in "
             "brackets): " + "; ".join("%s %.2f (%.2f to %.2f)" % (p, f["counted_per_month"][p], b2[p][0], b2[p][1])
                                       for p in PL) + ".")
    L.append("6. The spring 2024 campaign's trial starts on each plan over their first 24 months, at 2027 prices: "
             + "; ".join("%s %s trial starts, %.1f per cent paying after the trial, %.2f paying months and EUR %.2f "
                         "net revenue per trial start" % (p, f["spring24_trial_starts"][p], s24["%s share paying" % p],
                                                          s24["%s paying months" % p], s24["%s net revenue" % p])
                         for p in PL) + ".")
    L.append("7. The 2027 remuneration on the subscriptions paying at 31 October 2026: about EUR %s (EUR %s to "
             "EUR %s)." % (format(f["remuneration_2027_base"], ","), format(f["remuneration_2027_band"][0], ","),
                           format(f["remuneration_2027_band"][1], ",")))
    L += ["", "## Critical Components", ""]
    L.append("1. Contribution per trial start over 24 months (forecasting): **%s %s**, Standaard **%s**, Flex "
             "**%s**, Onbeperkt **%s**." % (lead, eur(c[lead]), eur(c["Standaard"]), eur(c["Flex"]),
                                            eur(c["Onbeperkt"])))
    L.append("2. Counted hours per paying subscription-month (measurement): Onbeperkt **%.2f** and Gezin **%.2f** "
             "once the licence renewals' positions are merged with the live roll-up and each profile sits on the "
             "account its charge lists (the live roll-up on today's profiles gives %.2f and %.2f)." % (
                 f["counted_per_month"]["Onbeperkt"], f["counted_per_month"]["Gezin"],
                 cr["counted_per_month"]["Onbeperkt"], cr["counted_per_month"]["Gezin"]))
    L.append("3. Paying subscriptions at 31 October 2026 (assembly): **%s**, Onbeperkt **%s** and Gezin **%s**." % (
        format(f["paying_oct_total"], ","), format(f["paying_oct"]["Onbeperkt"], ","),
        format(f["paying_oct"]["Gezin"], ",")))
    L.append("4. The 2027 remuneration on the October 2026 base (forecasting): **EUR %s** (EUR %s to %s)." % (
        format(f["remuneration_2027_base"], ","), format(f["remuneration_2027_band"][0], ","),
        format(f["remuneration_2027_band"][1], ",")))
    L += ["", "## Step-by-Step", ""]
    steps = [
        "From payments_2024-01_2026-10.csv and accounts_export_2026-11-03.csv, keep consumer accounts and count each "
        "account's collected monthly charge once (a returned debit that is re-presented counts once, staff and test "
        "accounts out): %s paying subscriptions at 31 October 2026 (guideline 3.1), reconciling to the KPI report's "
        "January to September months." % format(f["paying_oct_total"], ","),
        "From listening_monthly_2024-01_2026-10.csv (a re-sent row counted once) and "
        "licence_server_renewals_2024-01_2026-10.csv, rebuild schedule B's count per profile and title: the rise in "
        "the furthest position any report shows, in the month reported, licensed titles only (catalogue_2026-10.csv). "
        "The live roll-up reproduces the 2026 statements' streamed seconds exactly, but those are the 2026 basis; "
        "on live positions alone Onbeperkt counts %.2f hours a paying month, against %.2f with the renewals' "
        "positions of downloaded titles." % (mr["counted_per_month"]["Onbeperkt"], f["counted_per_month"]["Onbeperkt"]),
        "Put each profile's hours on the account whose charge that month lists it (profiles_on_subscription in the "
        "payments, guideline 3.3): profiles_export_2026-11-03.csv shows each profile where it is now, and partners "
        "who folded their own subscription into a Gezin account carry their earlier listening with them, so today's "
        "export gives Gezin %.2f counted hours a paying month where its paying months held %.2f." % (
            lr["counted_per_month"]["Gezin"], f["counted_per_month"]["Gezin"]),
        "Take the spring 2024 campaign's trial starts on each plan (signup source VJ24, guideline 3.4) over the trial "
        "month and 23 months after, re-rated at the 2027 list prices with VAT by country and the stores' fees: "
        "%s's %s trial starts bring EUR %.2f each over %.2f paying months." % (
            lead, f["spring24_trial_starts"][lead], s24["%s net revenue" % lead], s24["%s paying months" % lead]),
        "Charge each trial start's account EUR %.2f per counted hour in those months and the agency's fee (the "
        "quote): %s %s, Standaard %s, Flex %s, Onbeperkt %s; the campaign leads with %s (guideline 3.7)." % (
            f["rate"], lead, eur(c[lead]), eur(c["Standaard"]), eur(c["Flex"]), eur(c["Onbeperkt"]), lead),
        "The careful route on the live roll-up and today's profiles leads with %s (Onbeperkt %s); merging the "
        "renewals alone leads with %s (Gezin %s, its accounts charged for histories that came from other accounts); "
        "dating the profiles alone leads with %s; the 2026 basis carried leads with %s." % (
            cr["lead"], eur(cr["contribution"]["Onbeperkt"]), lr["lead"], eur(lr["contribution"]["Gezin"]),
            mr["lead"], sr["lead"]),
        "Forecast the October base's 2027 counted hours with survival by plan and paid-tenure band (November 2024 to "
        "October 2026) and counted hours per paying month by plan and calendar month, at EUR %.2f an hour: about "
        "EUR %s (EUR %s to %s over the survival and listening forms); on the live roll-up alone it would be EUR %s." % (
            f["rate"], format(f["remuneration_2027_base"], ","), format(f["remuneration_2027_band"][0], ","),
            format(f["remuneration_2027_band"][1], ","), format(cr["remuneration_2027"], ",")),
    ]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s" % (i, s))
    L += ["", "No other conclusion survives the records. Schedule B counts the furthest position a profile has reached "
          "from every position the app reports, and the licence renewals are such reports, so a count on the live "
          "roll-up alone understates Onbeperkt; guideline 3.3 puts a profile's hours on the account it belonged to, "
          "which the charges' profile lists date month by month, so today's export overstates Gezin; and the 2026 "
          "statements' revenue share is the agreement schedule B replaces. Every reading of the duplicate rows and "
          "every form of the base's forecast leads with %s, and only the two corrections together do." % lead, ""]
    open(path, "w").write("\n".join(L))
