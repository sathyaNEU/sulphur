"""task7 architecture 7: submission.md, the four answer blocks the author pastes into the platform, every figure taken
from figures.json at the precision the golden deliverables print it (percentages to two decimals, grant per tonne to
the cent, money to the euro, counts and totals whole)."""

LABEL = {"insulation": "insulation", "heating optimisation": "heating optimisation", "heating controls": "heating controls"}
MEAS = ["insulation", "heating optimisation", "heating controls"]
POSS = {"insulation": "insulation's", "heating optimisation": "heating optimisation's", "heating controls": "heating controls'"}


def n(v):
    return format(int(v), ",")


def p(v):
    return "%.2f%%" % v


def e(v):
    return "€%.2f" % v


def write(F, path):
    ins, ho, ct = MEAS
    eu, r1, r2, r4 = F["R5_eur_per_tonne"], F["R1_saving_by_season_pct"], F["R2_life_saving_pct"], F["R4_rate_on_applications_pct"]
    rg, be = F["R6_range_eur"], F["R6_break_even_pct"]
    flat = F["hurried_eur_per_tonne"]["the pilot's seven-season average"]
    pooled = F["hurried_eur_per_tonne"]["the pilot's own mix, faded"]
    typeflat = F["hurried_eur_per_tonne"]["each type's seven-season average"]
    ba = F["hurried_eur_per_tonne"]["the works buildings' own before and after"]
    t3 = F["R3_by_type_pct"]
    rc = F["controls_round_clock_share_pct"]
    seasons = F["season_labels"]
    ac, gc, gp = F["R7_applications_at_close"], F["R7_grant_at_close_eur"], F["R7_grant_paid_eur"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, energy efficiency and demand "
             "response evaluation (verified gas savings of commercial retrofit measures, carried to a grant round).")
    L.append("**Analytical objective:** Experiment & Causal Analysis.\n")
    L.append("## Final Recommendation\n")
    L.append("Fund **insulation and heating controls** in the 2026 round and **not heating optimisation**: priced at the "
             "saving the 2019 lottery showed for each application's own building use, carried over each measure's "
             "service life, the applications received come to %s, %s and %s of grant per lifetime tonne of CO2 "
             "against the €%d limit (insulation, controls, heating optimisation). The pilot's seven-season saving "
             "carried flat at the pilot's own mix (%s, %s and %s, funding insulation and heating optimisation and "
             "not controls) is rejected, because heating optimisation's saving falls from %s in its first winter to "
             "%s by the fourth and stays there, and %s of the pilot's controls answers came from hotels and care homes, "
             "where controls save next to nothing, against %s of this year's controls applicants."
             % (e(eu[ins]), e(eu[ct]), e(eu[ho]), F["limit_eur"], e(flat[ins]), e(flat[ct]), e(flat[ho]),
                p(r1[ho][0]), p(r1[ho][3]), p(rc["2019"]), p(rc["2026"])))
    L.append("")
    L.append("## Supplementary Questions\n")
    L.append("### grant_round_2026_note.docx\n")
    L.append("1. A two-page note for the committee's paper that opens with the call (fund insulation and heating "
             "controls, not heating optimisation, at %s, %s and %s a tonne against €%d), then a table of the three "
             "measures (saving over the life, saving rate on the applications received, grant per tonne, 90%% range, "
             "the saving rate at which the call flips, fund or not), a chart of each measure's grant per tonne with its "
             "range against a line at the limit beside the pilot's savings by season, what the round will pay, the "
             "2025/26 saving for the annual report, and a short table of how the quicker readings of the pilot land."
             % (e(eu[ins]), e(eu[ct]), e(eu[ho]), F["limit_eur"]))
    L.append("")
    L.append("### grant_round_2026_appraisal.xlsx\n")
    for k, m in enumerate(MEAS, 2):
        L.append("%d. Sheet \"savings by season\", %s saving against the owners the 2019 draw passed over, as a share "
                 "of the gas its works buildings would have used, normal weather, %s to %s: %s."
                 % (k, POSS[m], seasons[0], seasons[-1], ", ".join(p(v) for v in r1[m])))
    L.append("5. Sheet \"measures\", each measure's saving rate on the applications received by 12 June over its "
             "service life (lifetime tonnes as a share of the tonnes their reference consumption carries over the life): "
             "insulation %s, heating optimisation %s, heating controls %s; beside the pilot buildings' own saving over "
             "the life, %s, %s and %s." % (p(r4[ins]), p(r4[ho]), p(r4[ct]), p(r2[ins]), p(r2[ho]), p(r2[ct])))
    L.append("6. Sheet \"measures\", each measure's grant per tonne on those applications with its 90%% range and the "
             "saving rate at which its call would flip: insulation %s (%s to %s), flipping at %s; heating "
             "optimisation %s (%s to %s), flipping at %s; heating controls %s (%s to %s), flipping at %s. "
             "Insulation and controls are funded, heating optimisation is not."
             % (e(eu[ins]), e(rg[ins][0]), e(rg[ins][1]), p(be[ins]), e(eu[ho]), e(rg[ho][0]), e(rg[ho][1]), p(be[ho]),
                e(eu[ct]), e(rg[ct][0]), e(rg[ct][1]), p(be[ct])))
    L.append("7. Sheet \"round at close\", one row per measure once the offer closes on 30 June, with the grant its "
             "applications ask for and what would be paid on them once the works are done: insulation about %s "
             "applications asking €%s, €%s paid; heating optimisation about %s asking €%s, €%s if it were funded; "
             "heating controls about %s asking €%s, €%s paid. The funded round's totals: €%s asked and €%s paid."
             % (n(ac[ins]), n(gc[ins]), n(gp[ins]), n(ac[ho]), n(gc[ho]), n(gp[ho]), n(ac[ct]), n(gc[ct]), n(gp[ct]),
                n(F["R7_funded_close_eur"]), n(F["R7_funded_paid_eur"])))
    L.append("8. Sheet \"funded applications\", one row for each of the %s insulation and heating controls "
             "applications received by 12 June (a revised application replacing the earlier one), with its use, grant "
             "and lifetime tonnes, each priced at its own use's saving over the measure's life; together €%s of grant "
             "and %s lifetime tonnes." % (n(F["R9_funded_applications"]), n(F["R9_funded_grant_eur"]),
                                         n(F["R9_funded_tonnes"])))
    L.append("9. Sheet \"2025-26 saving\": the pilot's works saved %s tonnes of CO2 in the season to April 2026, the gas "
             "its works buildings would have used without the works less what they used, in normal weather."
             % n(F["R8_tonnes"]))
    L.append("")
    L.append("## Critical Components\n")
    L.append("1. Heating optimisation's saving falls from **%s** in its first winter to **%s** by the fourth and levels "
             "off, so over its %d-year life it saves **%s** of the pilot buildings' gas, not the seven seasons' "
             "average of %s." % (p(r1[ho][0]), p(r1[ho][3]), F["lives"][ho], p(r2[ho]), p(F["R2_seven_season_avg_pct"][ho])))
    L.append("2. Heating controls save **%s** in offices, **%s** in shops and **%s** in workshops, and **%s** in hotels "
             "and **%s** in care homes, which are heated round the clock."
             % (p(t3[ct]["office"]), p(t3[ct]["retail"]), p(t3[ct]["workshop"]), p(t3[ct]["hotel"]), p(t3[ct]["care home"])))
    L.append("3. On this year's applications heating controls save **%s** over their life, against **%s** at the "
             "pilot's own mix of buildings, because hotels and care homes made up %s of the pilot's controls answers "
             "and %s of this year's applicants." % (p(r4[ct]), p(F["R4_pooled_life_pct"][ct]), p(rc["2019"]), p(rc["2026"])))
    L.append("4. Only **%s** of the 2019 insulation answers were in by the same day after the notice, the late ones "
             "ran **%s** larger and **%s** of the late insulation places were withdrawn, so the funded round pays "
             "**€%s**, not the €%s received by 12 June scaled up."
             % (p(F["R7_share_by_day_pct"][ins]), p(F["R7_late_size_premium_pct"][ins]), p(F["R7_withdrawn_pct"][ins][1]),
                n(F["R7_funded_paid_eur"]), n(F["grant_received_funded_eur"])))
    L.append("")
    L.append("## Step-by-Step\n")
    L.append("1. Built each building's gas use per season (1 May to 30 April) from gas_meter_reads_2013_2026.csv, "
             "carrying index differences across meter exchanges, counter rollovers, estimates and corrections, sharing "
             "reads off 30 April as benchmarking_method_2022.pdf sets out, converting cubic metres with "
             "meter_points_2026.csv and calorific_values_2013_2026.csv, and normalising each season to long-term "
             "weather with degree_days_haldenau.csv as the same method sets out (the use type's hot-water share held).")
    L.append("2. Read the pilot from pilot_2019_responses_and_draw.xlsx (%s answers, %s drawn by lot within each "
             "measure, %s with works) and set each measure's works buildings against the owners the draw passed over, "
             "each against its own 2018/19 season, as a share of the gas the works buildings would have used (plan "
             "4.2): insulation holds near %s, heating optimisation falls from %s to %s, controls ease from %s to %s. "
             "The works buildings' own before and after (no comparison) books the pandemic, the 2022 price shock and "
             "the service team's burner checks as savings and funds all three (%s, %s, %s); the checks reached "
             "%s of works and %s of passed-over buildings, so the lottery balances them."
             % (n(F["answers_2019"]), n(F["drawn_2019"]), n(F["works_2019"]), p(r1[ins][-1]), p(r1[ho][0]), p(r1[ho][-1]),
                p(r1[ct][0]), p(r1[ct][-1]), e(ba[ins]), e(ba[ho]), e(ba[ct]), p(F["visited_share_pct"]["works"]),
                p(F["visited_share_pct"]["passed over"])))
    L.append("3. Carried each measure's seasons over its life (plan 4.4 lives %d, %d and %d years) by fitting the "
             "approach to the level the saving settles at: heating optimisation levels off at about %s from the fourth "
             "season, so its life saving is %s, not the seven-season %s; an exponential fall to nothing misses the last "
             "seasons and a straight line runs out before year fifteen. Carried flat, heating optimisation is %s and "
             "is wrongly funded." % (F["lives"][ins], F["lives"][ho], F["lives"][ct], p(F["R2_ho_floor_pct"]), p(r2[ho]),
                                     p(F["R2_seven_season_avg_pct"][ho]), e(flat[ho])))
    L.append("4. Split the pilot by the use on each building's 2019 notice: insulation saves least where hot water takes "
             "the most gas (hotels %s, care homes %s, restaurants %s, against offices %s), and controls save almost "
             "nothing in buildings heated round the clock (hotels %s, care homes %s)."
             % (p(t3[ins]["hotel"]), p(t3[ins]["care home"]), p(t3[ins]["restaurant"]), p(t3[ins]["office"]),
                p(t3[ct]["hotel"]), p(t3[ct]["care home"])))
    L.append("5. Priced every application in applications_2026.xlsx (a revised application replacing the earlier one) "
             "at its own use's saving, faded over the life as its measure's saving fades, on its reference "
             "consumption at 0.201 t per MWh (plan 4.4 and 4.5): saving rates %s, %s and %s; grant per tonne %s, %s "
             "and %s. At the pilot's own mix controls would save %s and cost %s a tonne; each use's saving carried flat "
             "funds all three (heating optimisation %s)."
             % (p(r4[ins]), p(r4[ho]), p(r4[ct]), e(eu[ins]), e(eu[ho]), e(eu[ct]), p(F["R4_pooled_life_pct"][ct]),
                e(pooled[ct]), e(typeflat[ho])))
    L.append("6. Drew the pilot's buildings again within each use and arm and repeated every step: 90%% ranges %s to "
             "%s, %s to %s and %s to %s, each wholly on its call's side of €%d; the calls flip at saving rates of "
             "%s, %s and %s." % (e(rg[ins][0]), e(rg[ins][1]), e(rg[ho][0]), e(rg[ho][1]), e(rg[ct][0]), e(rg[ct][1]),
                                 F["limit_eur"], p(be[ins]), p(be[ho]), p(be[ct])))
    L.append("7. Projected the round to the offer's close from the 2019 answers measure by measure (pilot_2019_rules.pdf, "
             "grant_offer_2026_terms.pdf): %s, %s and %s were in by the same day; late insulation answers ran %s "
             "larger; drawn owners withdrew %s and %s of early and late insulation places. The funded round's "
             "applications ask for €%s and it pays €%s; one share for every measure, late jobs priced like early ones "
             "or no withdrawals would each misstate it."
             % (p(F["R7_share_by_day_pct"][ins]), p(F["R7_share_by_day_pct"][ho]), p(F["R7_share_by_day_pct"][ct]),
                p(F["R7_late_size_premium_pct"][ins]), p(F["R7_withdrawn_pct"][ins][0]), p(F["R7_withdrawn_pct"][ins][1]),
                n(F["R7_funded_close_eur"]), n(F["R7_funded_paid_eur"])))
    L.append("8. Took the 2025/26 saving as plan 4.6 sets it, each works building's 2025/26 use grossed up by its "
             "measure's 2025/26 saving: %s tonnes; the seven-season average on the 2018/19 use gives %s and the "
             "2025/26 saving on the 2018/19 use %s, because the price shock, the burner checks and the 2018/19 "
             "season's own high reading left that use behind."
             % (n(F["R8_tonnes"]), n(F["R8_hurried_tonnes"]["average on the 2018/19 use"]),
                n(F["R8_hurried_tonnes"]["2025/26 rate on the 2018/19 use"])))
    L.append("")
    L.append("No other conclusion survives. The before and after funds all three on savings the comparison shows "
             "every building made; carrying the pilot's seven seasons flat funds heating optimisation on winters it no "
             "longer saves; the pilot's own mix fails controls on hotels and care homes few of this year's applicants "
             "are; and every defensible variant (a two-season baseline, each use's comparison, the last seasons "
             "carried, two occupancy classes) funds insulation and heating controls and leaves heating optimisation "
             "over the limit.")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
