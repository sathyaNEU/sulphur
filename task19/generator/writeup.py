"""task19 submission.md: the four answer blocks, every figure from figures.json."""
import analysis as AN

NAMES = AN.DNAME


def n0(x):
    return "{:,}".format(int(round(x)))


def ptxt(p):
    return "above 0.99" if p > 0.99 else ("below 0.01" if p < 0.01 else "%.2f" % p)


def write(F, path, workbook, note):
    dists = list(F["district_estimates"].keys())
    call = F["call"]
    q = [d for d in dists if d in call["qualifies"]]
    tc = [d for d in dists if d in call["too close to call"]]
    nq = [d for d in dists if d not in q and d not in tc]
    car = F["careful_call"]
    car_q_extra = [d for d in car["qualifies"] if d not in q]
    car_tc = [d for d in car["too close to call"]]
    lo, hi = F["national_interval"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Other, Survey Research & Official Statistics (nonresponse, calibration and measurement-error "
             "adjustment).  ")
    L.append("**Analytical objective:** Descriptive & Distribution Analysis.\n")
    L.append("## Final Recommendation\n")
    rec = ("**Certify %s as qualifying for the 2027/28 urban-services supplement, report %s as too close to call (chance "
           "of 25,000 or more %s, so half rate under circular 2026/14 paragraph 3.2), and %s as not qualifying**, on "
           "estimated usual residents of %s for Kilvarra (90 per cent interval %s to %s). "
           % (", ".join(NAMES[d] for d in q), " and ".join(NAMES[d] for d in tc),
              " and ".join(ptxt(F["p_line"][d]) for d in tc), ", ".join(NAMES[d] for d in nq),
              n0(F["national_estimate"]), n0(lo), n0(hi)))
    rec += ("Reject the register's counts, which put %s over the line; the %s that reading the matcher's links as the "
            "register's coverage and assuming independence gives, with %s qualifying on a national interval of plus or "
            "minus %.1f per cent; and the rolled-forward %s as a check on either, because it misses the same emigrants "
            "the register still lists."
            % (" and ".join(NAMES[d] for d in dists if F["register_counts"][d] >= 25000 and d not in q) or "no other district",
               n0(F["careful_national"]), " and ".join(NAMES[d] for d in car_q_extra) or "the same districts",
               F["careful_halfwidth_pct"], n0(F["official_2026"])))
    L.append(rec + "\n")
    L.append("## Supplementary Questions\n")
    L.append("### %s\n" % workbook)
    est = F["district_estimates"]
    L.append("1. An \"Estimates\" sheet with one row per district and a Kilvarra row: usual residents on 30 June 2026, each "
             "district within 1.0 per cent and Kilvarra within 0.6 per cent: " +
             "; ".join("%s %s" % (NAMES[d], n0(est[d])) for d in dists) + "; Kilvarra %s." % n0(F["national_estimate"]))
    L.append("2. Beside each estimate its 90 per cent interval; for Kilvarra %s to %s, a half-width of %.1f per cent "
             "(between 0.75 and 1.45 per cent). %s." % (
                 n0(lo), n0(hi), F["national_halfwidth_pct"],
                 "; ".join("%s %s to %s" % (NAMES[d], n0(F["district_intervals"][d][0]), n0(F["district_intervals"][d][1]))
                           for d in dists if d in tc or d in ("D05", "D06"))))
    L.append("3. The supplement column: %s qualify; %s too close to call, with a chance of 25,000 or more of %s (within "
             "0.16); %s do not qualify." % (", ".join(NAMES[d] for d in q), " and ".join(NAMES[d] for d in tc),
                                           " and ".join(ptxt(F["p_line"][d]) for d in tc),
                                           ", ".join(NAMES[d] for d in nq)))
    L.append("4. A \"Register to estimate\" sheet: for each district its register count, the entries that are not correct "
             "for the district (people who left Kilvarra or died, duplicate registrations and people living elsewhere in "
             "Kilvarra), the residents listed in another district and the residents on no list, adding to the estimate. "
             "Entries not correct for the district, each within 8 per cent: " +
             "; ".join("%s %s" % (NAMES[d], n0(F["register_not_correct"][d])) for d in dists) + ".")
    L.append("5. Residents listed in another district, each within 25 per cent (or 40 people): " +
             "; ".join("%s %s" % (NAMES[d], n0(F["listed_elsewhere"][d])) for d in dists) +
             ". Residents on no list, each within 25 per cent (or 40 people): " +
             "; ".join("%s %s" % (NAMES[d], n0(F["on_no_list"][d])) for d in dists) + ".")
    L.append("6. A \"National bridge\" sheet from the rolled-forward %s to the estimate: a gap of %s (within 0.6 per cent "
             "of the national figure), of which emigrants since mid-2021 never recorded in the accounts %s (within 15 per "
             "cent), arrivals on the border record missing from the accounts %s (exact), and a remainder of %s."
             % (n0(F["official_2026"]), n0(F["official_gap"]), n0(F["unrecorded_emigration"]),
                n0(F["immigration_not_in_accounts"]), n0(F["official_remainder"])))
    L.append("7. The share of the coverage survey's residents (serving personnel aside) on their own district's list, "
             "missed and false links counted: Kilvarran citizens %.1f per cent (within 0.6 point), others %.1f per cent "
             "(within 2.5 points)." % (F["coverage_pct"]["nationals"], F["coverage_pct"]["others"]))
    L.append("\n### %s\n" % note)
    L.append("8. One to two pages for the Commission: the call with each close district's chance, how the estimates were "
             "made, how sure they are, and why they differ from the register and from the rolled-forward estimate, with "
             "the same figures as the workbook.\n")
    L.append("## Critical Components\n")
    L.append("1. The matcher links %.1f per cent of the survey's Kilvarran citizens and %.1f per cent of others to their own "
             "district's list, but the clerical review shows it misses true links (recall %.1f and %.1f per cent): on the "
             "list are **%.1f** and **%.1f per cent**." % (
                 F["linked_pct"]["nationals"], F["linked_pct"]["others"], F["recall_pct"]["nationals"],
                 F["recall_pct"]["others"], F["coverage_pct"]["nationals"], F["coverage_pct"]["others"]))
    L.append("2. The register and the survey miss the same young men: births and survival put men per woman above the "
             "estimate's, so men aged 18 to 29 are raised by **%.3f** and 30 to 44 by **%.3f** (each within %.2f)." % (
                 F["raising_factor"]["18-29"], F["raising_factor"]["30-44"], F["constants"]["band_k"]))
    L.append("3. Kilvarra's 90 per cent interval is **%s to %s** (plus or minus %.1f per cent); resampling the survey "
             "blocks with the linkage correction and the raising factors held fixed gives plus or minus %.1f." % (
                 n0(lo), n0(hi), F["national_halfwidth_pct"], F["careful_halfwidth_pct"]))
    L.append("4. The rolled-forward estimate of %s is **%s** above the estimate; **%s** emigrants since mid-2021 are still "
             "listed and missing from the accounts, against %s arrivals the accounts left out." % (
                 n0(F["official_2026"]), n0(F["official_gap"]), n0(F["unrecorded_emigration"]),
                 n0(F["immigration_not_in_accounts"])))
    L.append("")
    L.append("## Step-by-Step\n")
    steps = [
        "Placed every register entry in the district its postcode belongs to through the postcode directory (codes "
        "retired in 2024 included, keying differences removed), and the survey's people and the follow-up's entries by "
        "their block.",
        "Linked the survey's people to the register on names, dates of birth, sex and postcodes, allowing other "
        "romanisations, nicknames and Irish forms, swapped day and month, defaulted dates of birth and name order "
        "swapped; one person per record. On the clerical review the matcher links %.1f per cent of Kilvarran citizens "
        "who are on their own district's list and %.1f per cent of others; the table of verified status against linked "
        "status, by citizenship and sex, gives each survey person their chance of being on their own district's list "
        "(%.1f and %.1f per cent overall)." % (F["recall_pct"]["nationals"], F["recall_pct"]["others"],
                                              F["coverage_pct"]["nationals"], F["coverage_pct"]["others"]),
        "Measured each district's correct entries from the follow-up: resident at the address, or moved within the "
        "district; movers with no district recorded at the share the district's known movers give; people the household "
        "could not place and vacant addresses at the district's placed outcomes; no-contact entries at the chance a "
        "logistic model fitted on the resolved ones gives (last attendance, registration date, dwelling type, age, sex, "
        "district). Entries not correct: " +
        ", ".join("%s %s" % (NAMES[d], n0(F["register_not_correct"][d])) for d in ("D05", "D06", "D07")) + ".",
        "Divided each district's correct entries, by age group and sex, by the share of the survey's people in that "
        "cell on the district's list; serving personnel came from the Defence Forces' return instead.",
        "Built men per woman for Kilvarrans aged 18 to 29 and 30 to 44 from births by sex and the life table's survival, "
        "and compared it with the estimate's (serving personnel added back on that side): raising factors %.3f and %.3f "
        "applied to every district's men of those ages. Independence leaves Kilvarra %s lower." % (
            F["raising_factor"]["18-29"], F["raising_factor"]["30-44"], n0(F["independence_gap"])),
        "Resampled the survey's blocks within districts and repeated every step, the clerical review's table and the "
        "raising factors included: Kilvarra %s (%s to %s); each district's chance of 25,000 or more from its estimate and "
        "spread, and the call under paragraph 3.2." % (n0(F["national_estimate"]), n0(lo), n0(hi)),
        "Bridged each register count to its estimate, the parts adding up, and the rolled-forward figure to the "
        "estimate: emigrants since mid-2021 still listed (the follow-up's people who left Kilvarra, dated by the year "
        "they left, those not known at the address shared out as the district's known outcomes are) less those whose "
        "departure the border system recorded: %s." % n0(F["unrecorded_emigration"]),
    ]
    for i, s in enumerate(steps, 1):
        L.append("%d. %s" % (i, s))
    L.append("")
    a1, b1 = F["linked_share_effect_pct"]
    a4, b4 = F["independence_effect_pct"]
    L.append("No other call survives. Reading the matcher's links as coverage lifts the districts by %.1f to %.1f per "
             "cent, and independence lowers them by %.1f to %.1f per cent; with both, and with the survey alone "
             "resampled (plus or minus %.1f per cent for Kilvarra against %.1f), %s reads as qualifying. Calibrating to the "
             "rolled-forward total, or reading the register's own counts, carries the emigrants both still hold, and puts "
             "%s over the line." % (a1, b1, -b4, -a4, F["careful_halfwidth_pct"], F["national_halfwidth_pct"],
                                    " and ".join(NAMES[d] for d in car_q_extra) or "the close district",
                                    " and ".join(NAMES[d] for d in dists if F["register_counts"][d] >= 25000 and d not in q) or "another district"))
    open(path, "w").write("\n".join(L) + "\n")
