"""task8: figures.json and submission.md, both written from the golden's own objects (every figure in the four
answer blocks is printed from here, at its stated precision, with its band where reasonable methods differ)."""
import json

import params as P
import results as R

TEST_WORD = {"Lexis": "Lexis", "Quill": "Quill", "Brightway": "Brightway"}


def r1(x):
    return round(float(x), 1)


def band(b, nd=1):
    lo, hi = b
    if nd == 0:
        return [int(round(lo + 0.5)), int(round(hi - 0.5))]
    return [round(lo + 0.05, nd), round(hi - 0.05, nd)]


def figures(G):
    g, B = G["golden"], G["bands"]
    D = G["D"]
    acad = sorted(D["academies"])
    pl = g["placements"]
    F = {"threshold": int(P.THRESHOLD), "hours_per_student": P.HOURS_PER_STUDENT, "weeks": P.WEEKS, "rate": P.RATE,
         "provisional_budget": int(P.PROVISIONAL_BUDGET), "last_october": P.LAST_OCTOBER}
    F["on_roll"] = len(pl)
    F["on_roll_by_academy"] = {a: sum(1 for p in pl if p["s"]["academy"] == a) for a in acad}
    F["valid_by_academy"] = {a: int(g["R1"][a]) for a in acad}
    F["valid_total"] = int(sum(g["R1"].values()))
    F["ks2_placed"] = sum(1 for p in pl if p["basis"] == "ks2")
    F["no_result"] = sum(1 for p in pl if p["basis"] == "none")
    F["second_sitting_gain"] = r1(g["R2"])
    F["july_level"] = r1(g["R5"])
    F["brightway_lexis"] = {str(x): r1(v) for x, v in g["R3"].items()}
    F["quill_lexis"] = {str(x): r1(v) for x, v in g["R4"].items()}
    F["programme"] = {a: int(g["R6"][a]) for a in acad}
    F["programme_total"] = int(g["R6_total"])
    F["own"] = {a: int(g["own"][a]) for a in acad}
    F["own_total"] = int(g["own_total"])
    F["change"] = {a: int(g["R7"][a]) for a in acad}
    F["change_by_test"] = {k: int(v) for k, v in g["R7_test"].items()}
    F["change_total"] = F["programme_total"] - F["own_total"]
    F["hours"] = {a: r1(g["R9"][a]) for a in acad}
    F["hours_total"] = r1(g["R8_hours"])
    F["cost_total"] = int(round(g["R8_cost"]))
    F["extra_over_budget"] = F["cost_total"] - F["provisional_budget"]
    if "boot" in G:
        lo, hi = G["boot"]["lo"], G["boot"]["hi"]
        F["range_students"] = [lo, hi]
        F["range_hours"] = [r1(lo * P.HOURS_PER_STUDENT), r1(hi * P.HOURS_PER_STUDENT)]
        F["range_cost"] = [int(round(lo * P.HOURS_PER_STUDENT * P.WEEKS * P.RATE)),
                           int(round(hi * P.HOURS_PER_STUDENT * P.WEEKS * P.RATE))]
        F["boot_reps"] = G["boot"]["reps"]
    F["bands"] = {
        "R2": band(B["R2"]), "R5": band(B["R5"]),
        "R3": {str(k): band(v) for k, v in B["R3"].items()}, "R4": {str(k): band(v) for k, v in B["R4"].items()},
        "R6": {k: band(v, 0) for k, v in B["R6"].items()}, "R6_total": band(B["R6_total"], 0),
        "R7_test": {k: band(v, 0) for k, v in B["R7_test"].items()},
        "R9": {k: band(v) for k, v in B["R9"].items()}, "R8_hours": band(B["R8_hours"]),
    }
    car = G["routes"]["careful"]
    F["careful"] = {"programme_total": int(car["R6_total"]), "hours_total": r1(car["R8_hours"]),
                    "cost_total": int(round(car["R8_cost"])), "second_sitting_gain": r1(car["R2"]),
                    "july_level": r1(car["R5"]), "brightway_lexis": {str(x): r1(v) for x, v in car["R3"].items()}}
    F["routes_total"] = {nm: int(r["R6_total"]) for nm, r in G["routes"].items()}
    F["routes_cost"] = {nm: int(round(r["R8_cost"])) for nm, r in G["routes"].items()}
    F["ruled_out_total"] = {nm: int(r["R6_total"]) for nm, r in G["ruled_out"].items()}
    ev = G["evidence"]
    F["evidence"] = {"gap_lexis_second": r1(ev["gap_lexis_second"]), "gap_lexis_first": r1(ev["gap_lexis_first"]),
                     "gap_lexis_first_below": r1(-ev["gap_lexis_first"]),
                     "n_lexis_second": ev["n_lexis_second"], "n_lexis_first": ev["n_lexis_first"],
                     "switch_lexis_first_obs": r1(ev["switch_lexis_first_obs"]),
                     "switch_lexis_first_ks2_pred": r1(ev["switch_lexis_first_ks2_pred"]),
                     "ks2_mean": {k: r1(v) for k, v in ev["ks2_mean"].items()},
                     "sas_mean": {k: r1(v) for k, v in ev["sas_mean"].items()}}
    F["rivals_total"] = {nm: int(r["R6_total"]) for nm, r in G["rivals"].items()}
    tots = list(F["rivals_total"].values()) + [F["programme_total"]]
    F["family_range"] = [min(tots), max(tots)]
    share = {}
    for p in pl:
        share.setdefault(p["s"]["academy"], []).append(p["basis"] == "july")
    F["n_july_academies"] = sum(1 for v in share.values() if sum(v) > 0.5 * len(v))
    F["n_switch_academies"] = len(P.SWITCH_ACADEMIES)
    return F


def money(x):
    return "£{:,.0f}".format(x)


def btxt(b, nd=1):
    if nd == 0:
        return "exact" if b[0] == b[1] else "%s to %s" % (b[0], b[1])
    return "%.1f to %.1f" % (b[0], b[1])


def submission(F, path, D):
    acad = sorted(D["academies"], key=lambda a: (D["academies"][a]["entry_reading_test"], a))
    tests = {a: D["academies"][a]["entry_reading_test"] for a in acad}
    L = ["# task8: Hollinbrook Academies Trust, Reading Forward 2026-27 tutor time\n", "## Tags\n",
         "**Domain:** Education & Learning Sciences, Psychometrics (scale validation, item response theory, test "
         "equating).", "**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).\n"]
    L.append("## Final Recommendation\n")
    L.append("Budget Reading Forward for %d students and %.1f tutor hours a week this year, %s (range %s to %s), "
             "%s more than the provisional %s, with the hours by academy below; not the %s for %d students that "
             "converting Brightway through the trial's pairs as they stand and taking the July transition-day "
             "sittings as entry reading gives, which would leave the provisional budget looking sufficient." % (
                 F["programme_total"], F["hours_total"], money(F["cost_total"]), money(F["range_cost"][0]),
                 money(F["range_cost"][1]), money(F["extra_over_budget"]), money(F["provisional_budget"]),
                 money(F["careful"]["cost_total"]), F["careful"]["programme_total"]))
    L.append("\n## Supplementary Questions\n")
    L.append("### reading_forward_entry_2026.xlsx\n")
    L.append("1. Sheet Students has one row per Year 7 student on roll at the 1 October 2026 census, %s rows, with the "
             "UPN, academy, the academy's entry test, the sitting used and its date, the result as recorded, the entry "
             "reading as a whole score on the Lexis basis, how the student was placed and whether they join Reading "
             "Forward. Students with a valid entry sitting by the census, by academy (exact): " % f"{F['on_roll']:,}" +
             "; ".join("%s %d" % (a, F["valid_by_academy"][a]) for a in acad) +
             "; %s in all, with %d more placed on their KS2 reading and %d with no result." % (
                 f"{F['valid_total']:,}", F["ks2_placed"], F["no_result"]))
    L.append("2. Sheet Academies gives each academy's Reading Forward students and tutor hours a week (0.4 hours per "
             "student), in that order with the band in brackets: " + "; ".join(
                 "%s %d (%s), %.1f hours" % (a, F["programme"][a], btxt(F["bands"]["R6"][a], 0), F["hours"][a])
                 for a in acad) + "; %d students and %.1f hours in all." % (F["programme_total"], F["hours_total"]))
    L.append("\n### reading_forward_tutor_time_2026.pdf\n")
    L.append("3. One page to the director of education. The trust's tutor time is %.1f hours a week (%s), costing %s "
             "for the 36 weeks at £27.80 an hour (range %s to %s, %d to %d students, from re-estimating the "
             "conversions), against the provisional %s." % (
                 F["hours_total"], btxt(F["bands"]["R8_hours"]), money(F["cost_total"]), money(F["range_cost"][0]),
                 money(F["range_cost"][1]), F["range_students"][0], F["range_students"][1],
                 money(F["provisional_budget"])))
    L.append("4. The Lexis score of equal reading at the start of Year 7 for a Quill result of 70, 75, 80, 85, 90 and 95: "
             + "; ".join("%s %.1f (%s)" % (x, F["quill_lexis"][str(x)], btxt(F["bands"]["R4"][str(x)])) for x in R.POINTS)
             + "; for the same Brightway results: " + "; ".join(
                 "%s %.1f (%s)" % (x, F["brightway_lexis"][str(x)], btxt(F["bands"]["R3"][str(x)])) for x in R.POINTS)
             + ".")
    L.append("5. Against each academy's own test (its own standardised score below 85, the KS2 rule for students without "
             "one), by academy (the own-test count exact, the change carrying the academy's band from item 2): " +
             "; ".join("%s %d on its own test, %+d" % (a, F["own"][a], F["change"][a]) for a in acad) +
             "; by test, Lexis academies %+d (%s, all at the July academies), Quill academies %+d (%s), Brightway "
             "academies %+d (%s); %d on the academies' own tests in all, %+d." % (
                 F["change_by_test"]["Lexis"], btxt(F["bands"]["R7_test"]["Lexis"], 0), F["change_by_test"]["Quill"],
                 btxt(F["bands"]["R7_test"]["Quill"], 0), F["change_by_test"]["Brightway"],
                 btxt(F["bands"]["R7_test"]["Brightway"], 0), F["own_total"], F["change_total"]))
    L.append("\n## Critical Components\n")
    ev = F["evidence"]
    L.append("1. The Brightway academies' Lexis trial was a second sitting for most students, and a second sitting ran "
             "**%.1f points** (%s) above a first: at the %d academies where half the tutor groups sat Lexis first, "
             "Lexis ran %.1f points above Brightway when it came second and %.1f below when it came first." % (
                 F["second_sitting_gain"], btxt(F["bands"]["R2"]), F["n_switch_academies"], ev["gap_lexis_second"],
                 -ev["gap_lexis_first"]))
    L.append("2. A Lexis sitting at the July transition day stands **%.1f points** (%s) above the start of Year 7, read "
             "against KS2 through the September Lexis academies." % (F["july_level"], btxt(F["bands"]["R5"])))
    L.append("3. Quill's standardised scores rest on a softer 2024 sample: a Quill 85 is a Lexis **%.1f** and a "
             "Brightway 85 a Lexis **%.1f**." % (F["quill_lexis"]["85"], F["brightway_lexis"]["85"]))
    L.append("4. The programme needs **%d** students' tutor time, **%s**, against the provisional %s." % (
        F["programme_total"], money(F["cost_total"]), money(F["provisional_budget"])))
    L.append("\n## Step-by-Step\n")
    for i, s_ in enumerate(steps(F), 1):
        L.append("%d. %s" % (i, s_))
    L.append("")
    L.append("No other conclusion survives the records. Reading every test's standardised score as a Lexis score is "
             "ruled out by KS2, on which the Quill academies' intake reads %.1f against %.1f for the students who sat "
             "Lexis in September, while their own scores run %.1f against %.1f; a prediction of Lexis from KS2 by regression pulls "
             "every converted score toward the middle and places %d students; converting Brightway through KS2 instead "
             "of the trial is not the trust's link for Brightway (policy section 6), and it reads those academies a "
             "little high (the students who sat Lexis first there have KS2 results that give %.1f against the %.1f "
             "they scored); and every reasonable version of the conversions (the presmoothing, frequency "
             "estimation for Quill, the gain from median gaps or the fixed-order academies alone, the July level by "
             "median or regression) places %d to %d students, differing only by whole score groups at the cut." % (
                 ev["ks2_mean"]["Quill"], ev["ks2_mean"]["Lexis"], ev["sas_mean"]["Quill"], ev["sas_mean"]["Lexis"],
                 F["routes_total"]["Quill predicted from KS2 by regression"], ev["switch_lexis_first_ks2_pred"],
                 ev["switch_lexis_first_obs"], F["family_range"][0], F["family_range"][1]))
    open(path, "w").write("\n".join(L) + "\n")


def steps(F):
    return [
        "From census_year7_2026-10-01.csv, take the %s Year 7 students on roll at the census; attach each student's "
        "sittings from lexis_results_autumn2026.csv (by UPN, or name and date of birth where the UPN is blank), "
        "quill_results_2026.csv (through quill_roster_map.csv's admission numbers, or by name inside the site's academy) "
        "and brightway_results_2026.xlsx (by name and date of birth inside each sheet's academy), dropping the "
        "repeated export rows; the first valid sitting by the census is a completed Lexis or Brightway test or a Quill "
        "session of 24 questions or more in quill_session_log_2026.csv (the policy): %s students have one." % (
            f"{F['on_roll']:,}", f"{F['valid_total']:,}"),
        "Read a September Lexis sitting on the Lexis 2019 basis directly, and build the KS2 to Lexis conversion on the "
        "KS2 reading (ks2_results_2026.csv) and first Lexis sittings of the students who sat Lexis in September, by "
        "equipercentile linking with presmoothing (the July sittings kept out of it).",
        "Convert Quill through KS2 (Quill to KS2 inside the Quill academies, then KS2 to Lexis): a Quill 85 is a Lexis "
        "%.1f, where reading the Quill score as a Lexis score keeps it at 85." % F["quill_lexis"]["85"],
        "Pair each Brightway academy student's Brightway result with their Lexis trial result and read the order from "
        "the two sittings' dates: at the %d academies where half the tutor groups sat Lexis first, the gap between the "
        "orders gives a second-sitting gain of %.1f points; take it off whichever sitting came second and link "
        "Brightway to Lexis on the pairs: a Brightway 85 is a Lexis %.1f, not the %.1f the pairs as they stand give." % (
            F["n_switch_academies"], F["second_sitting_gain"], F["brightway_lexis"]["85"],
            F["careful"]["brightway_lexis"]["85"]),
        "For the four academies that sat Lexis at the July transition day, compare their results with what their KS2 "
        "results give through the September academies: they stand %.1f points higher, and each July result is "
        "brought down by it." % F["july_level"],
        "Place every student at the whole Lexis score of equal reading at the start of Year 7 from their first valid "
        "sitting, converted, or from "
        "their KS2 reading if they have no sitting, and count those below 85: %d students, %.1f tutor hours a week, %s "
        "for the year; drawing the linking samples again gives %d to %d students." % (
            F["programme_total"], F["hours_total"], money(F["cost_total"]), F["range_students"][0],
            F["range_students"][1]),
        "Compare with each academy's own test: %d students in all, the Quill academies %d short and the Brightway "
        "academies %d over; the shortcuts above together give %d students and %s, inside the provisional %s." % (
            F["own_total"], F["change_by_test"]["Quill"], -F["change_by_test"]["Brightway"],
            F["careful"]["programme_total"], money(F["careful"]["cost_total"]), money(F["provisional_budget"])),
    ]


def write(G, fig_path, sub_path):
    F = figures(G)
    json.dump(F, open(fig_path, "w"), indent=1, sort_keys=True, ensure_ascii=False)
    submission(F, sub_path, G["D"])
    return F
