"""task7 architecture 8: submission.md, the four answer blocks the author pastes into the platform, every figure taken
from figures.json at the precision the golden deliverables print it (percentages to two decimals, grant per tonne to
the cent, money to the euro, counts and totals whole)."""

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
    eu, r1, r2, r5 = F["R6_eur_per_tonne"], F["R1_saving_by_season_pct"], F["R2_life_saving_pct"], F["R5_rate_on_applications_pct"]
    rg, be = F["R7_range_eur"], F["R7_break_even_pct"]
    hur = F["hurried_eur_per_tonne"]
    byuse = hur["each use's saving, faded"]
    flat = hur["the pilot's seven-season average"]
    pooled = hur["the pilot's own mix, faded"]
    ba = hur["the works buildings' own before and after"]
    lin = hur["controls on a straight line through the lived-in band"]
    alone = hur["the empty week read off the load alone"]
    c3, ew = F["R3_controls_at_empty_pct"], F["R3_empty_week_pct"]
    h4, rf = F["R4_heating_at_roof_pct"], F["R4_roof_per_floor"]
    seasons = F["season_labels"]
    ac, gc, gp = F["R8_applications_at_close"], F["R8_grant_at_close_eur"], F["R8_grant_paid_eur"]
    L = []
    L.append("## Tags\n")
    L.append("**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, energy efficiency and demand "
             "response evaluation (verified gas savings of commercial retrofit measures, carried to a grant round).")
    L.append("**Analytical objective:** Experiment & Causal Analysis.\n")
    L.append("## Final Recommendation\n")
    L.append("Fund **insulation and heating controls** in the 2026 round and **not heating optimisation**: priced at the "
             "saving the 2019 lottery showed for each application's own building (controls at how much of the week it "
             "stands empty, read off its 2025 load profile; insulation at how much roof it has per square metre of floor, "
             "from the solar cadastre and the register) and carried over each measure's life, the applications received "
             "come to %s, %s and %s of grant per lifetime tonne of CO2 against the €%d limit (insulation, controls, "
             "heating optimisation). Pricing each application at its own use's saving (%s and %s) funds nothing and is "
             "rejected, because this year's controls applications stand empty %s of the week against %s for the pilot's "
             "controls buildings and this year's insulation applications have %.2f square metres of roof per square "
             "metre of floor against %.2f (applications weighted by reference consumption, the pilot's buildings by "
             "their 2018/19 gas), and each measure's saving rises with them."
             % (e(eu[ins]), e(eu[ct]), e(eu[ho]), F["limit_eur"], e(byuse[ins]), e(byuse[ct]), p(ew["2026"]),
                p(ew["pilot"]), rf["2026"], rf["pilot"]))
    L.append("")
    L.append("## Supplementary Questions\n")
    L.append("### grant_round_2026_note.docx\n")
    L.append("1. A two-page note for the committee's paper that opens with the call (fund insulation and heating "
             "controls, not heating optimisation, at %s, %s and %s a tonne against €%d), then why (controls' saving "
             "along the share of the week a building stands empty, insulation's along its roof per floor, this year's "
             "applications against the pilot's on each, heating optimisation's saving falling back), a table of the "
             "three measures (saving over the life, saving rate on the applications received, grant per tonne, 90%% "
             "range, the saving rate at which the call flips, fund or not), a chart of each grant per tonne with its "
             "range against a line at the limit beside controls' saving by empty week and insulation's by roof per "
             "floor, what the round will pay, the 2025/26 saving for the annual report, and a short table of how the "
             "quicker readings of the pilot land." % (e(eu[ins]), e(eu[ct]), e(eu[ho]), F["limit_eur"]))
    L.append("")
    L.append("### grant_round_2026_appraisal.xlsx\n")
    for k, m in enumerate(MEAS, 2):
        L.append("%d. Sheet \"savings by season\", %s saving against the owners the 2019 draw passed over, as a share "
                 "of the gas its works buildings would have used, normal weather, %s to %s: %s."
                 % (k, POSS[m], seasons[0], seasons[-1], ", ".join(p(v) for v in r1[m])))
    L.append("5. Sheet \"measures\", each measure's saving rate on the applications received by 12 June over its "
             "service life (lifetime tonnes as a share of the tonnes their reference consumption carries over the life): "
             "insulation %s, heating optimisation %s, heating controls %s; beside the pilot buildings' own saving over "
             "the life, %s, %s and %s." % (p(r5[ins]), p(r5[ho]), p(r5[ct]), p(r2[ins]), p(r2[ho]), p(r2[ct])))
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
                n(F["R8_funded_close_eur"]), n(F["R8_funded_paid_eur"])))
    L.append("8. Sheet \"applications\", one row for each of the %s applications received by 12 June (a revised "
             "application replacing the earlier one), with its use, measure, grant, reference consumption, saving rate "
             "over the life and lifetime tonnes, controls rows also showing the share of the week the building stands "
             "empty and insulation rows its roof per floor; together €%s of grant and %s lifetime tonnes (insulation "
             "%s, heating optimisation %s, heating controls %s)."
             % (n(F["R9_applications"]), n(F["R9_grant_eur"]), n(F["R9_tonnes"]), n(F["R9_tonnes_by_measure"][ins]),
                n(F["R9_tonnes_by_measure"][ho]), n(F["R9_tonnes_by_measure"][ct])))
    L.append("9. Sheet \"2025-26 saving\": the pilot's works saved %s tonnes of CO2 in the season to April 2026, the gas "
             "its works buildings would have used without the works less what they used, in normal weather."
             % n(F["R10_tonnes"]))
    L.append("")
    L.append("## Critical Components\n")
    L.append("1. Heating optimisation's saving falls from **%s** in its first winter to **%s** by the fourth and settles "
             "towards about %s, so over its %d-year life it saves **%s** of the pilot buildings' gas, not the seven "
             "seasons' average of %s." % (p(r1[ho][0]), p(r1[ho][3]), p(F["R2_ho_floor_pct"]), F["lives"][ho], p(r2[ho]),
                                         p(F["R2_seven_season_avg_pct"][ho])))
    L.append("2. Heating controls save nothing until about **%.1f%%** of the week is empty and then about %.2f points "
             "more for each further tenth: **%s** of the gas at half the week empty, **%s** at three fifths and **%s** "
             "at seven tenths, and %s in hotels and care homes lived in round the clock; this year's controls "
             "applications stand empty **%s** of the week (weighted by reference consumption), the pilot's controls "
             "buildings %s (weighted by their 2018/19 gas, those lived in round the clock at none)."
             % (F["R3_threshold_empty_pct"], F["R3_slope_points_per_tenth"], p(c3["50"]), p(c3["60"]), p(c3["70"]),
                p(F["R3_lived_in_pct"]), p(ew["2026"]), p(ew["pilot"])))
    L.append("3. Roof insulation saves **%s** of a building's heating where the roof is as large as the floor, **%s** "
             "at half and **%s** at a quarter; this year's insulation applications have **%.2f** square metres of roof "
             "per square metre of floor (weighted by reference consumption), the pilot's insulation buildings %.2f "
             "(weighted by their 2018/19 gas)."
             % (p(h4["1"]), p(h4["0.5"]), p(h4["0.25"]), rf["2026"], rf["pilot"]))
    L.append("4. Once the offer closes the funded round's applications ask for **€%s** and it pays **€%s** once the "
             "works are done, the late insulation applications larger (%s in 2019) and more often withdrawn."
             % (n(F["R8_funded_close_eur"]), n(F["R8_funded_paid_eur"]), p(F["R8_late_size_premium_pct"][ins])))
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
             "the service team's burner checks as savings and funds all three (%s, %s, %s)."
             % (n(F["answers_2019"]), n(F["drawn_2019"]), n(F["works_2019"]), p(r1[ins][-1]), p(r1[ho][0]), p(r1[ho][-1]),
                p(r1[ct][0]), p(r1[ct][-1]), e(ba[ins]), e(ba[ho]), e(ba[ct])))
    L.append("3. Carried each measure's seasons over its life (plan 4.4 lives %d, %d and %d years) by fitting the "
             "approach to the level the saving settles at: heating optimisation's life saving is %s, not the "
             "seven-season %s; carried flat, heating optimisation would be %s a tonne and wrongly funded."
             % (F["lives"][ins], F["lives"][ho], F["lives"][ct], p(r2[ho]), p(F["R2_seven_season_avg_pct"][ho]),
                e(flat[ho])))
    L.append("4. Read each building's week off electricity_load_profiles_2025.csv (its market locations summed under its "
             "customer number in buildings_register_2026.xlsx): the hours whose load is under half-way from the week's "
             "lowest hour to its highest are empty, none where the load never falls below three quarters of its "
             "highest hour (in use round the clock); every hotel and care home is lived in round the clock, its guests "
             "or residents there at night, so its night and midday dips are sleep and quiet, not an empty building (read "
             "off their load alone the pilot's hotels and care homes stand over half the week empty, yet they saved %s "
             "from controls). Banded the pilot's controls answers by it and set works against passed-over in each band: "
             "nothing until about %.1f%% empty, then a straight rise; a straight line through the lived-in band too "
             "prices controls at %s, and the hotels and care homes read off their load alone at %s."
             % (p(F["R3_lived_in_pct"]), F["R3_threshold_empty_pct"], e(lin[ct]), e(alone[ct])))
    L.append("5. Summed the roof faces of solar_cadastre_rooftops_2024.xlsx at each address (the cadastre writes str. "
             "for straße) over the register's heated floor area, banded the pilot's insulation answers by it and took "
             "each band's saving on the heating part (the use's hot-water share, which insulation leaves alone): a "
             "straight line in the logarithm of the roof per floor, from %s of the heating at a quarter to %s where the "
             "roof is as large as the floor." % (p(h4["0.25"]), p(h4["1"])))
    L.append("6. Priced every application in applications_2026.xlsx (a revised application replacing the earlier one) at "
             "its own building's saving (controls at its empty week, insulation at its roof per floor on its heating, "
             "heating optimisation at its own use's), faded over the life as its measure's saving fades, on its "
             "reference consumption at 0.201 t per MWh (plan 4.4 and 4.5): saving rates %s, %s and %s; grant per tonne "
             "%s, %s and %s. At each use's saving insulation comes to %s and controls to %s, and at the pilot's own mix "
             "%s and %s, so both fail; the pilot's seven-season saving carried flat funds heating optimisation alone."
             % (p(r5[ins]), p(r5[ho]), p(r5[ct]), e(eu[ins]), e(eu[ho]), e(eu[ct]), e(byuse[ins]), e(byuse[ct]),
                e(pooled[ins]), e(pooled[ct])))
    L.append("7. Drew the pilot's buildings again within each use and arm and repeated every step, the bands and their "
             "fits included: 90%% ranges %s to %s, %s to %s and %s to %s, each wholly on its call's side of €%d; the "
             "calls flip at saving rates of %s, %s and %s." % (e(rg[ins][0]), e(rg[ins][1]), e(rg[ho][0]), e(rg[ho][1]),
                                                              e(rg[ct][0]), e(rg[ct][1]), F["limit_eur"], p(be[ins]),
                                                              p(be[ho]), p(be[ct])))
    L.append("8. Projected the round to the offer's close from the 2019 answers measure by measure (pilot_2019_rules.pdf, "
             "grant_offer_2026_terms.pdf): %s, %s and %s were in by the same day; late insulation answers ran %s "
             "larger; drawn owners withdrew %s and %s of early and late insulation places. The funded round's "
             "applications ask for €%s and it pays €%s."
             % (p(F["R8_share_by_day_pct"][ins]), p(F["R8_share_by_day_pct"][ho]), p(F["R8_share_by_day_pct"][ct]),
                p(F["R8_late_size_premium_pct"][ins]), p(F["R8_withdrawn_pct"][ins][0]), p(F["R8_withdrawn_pct"][ins][1]),
                n(F["R8_funded_close_eur"]), n(F["R8_funded_paid_eur"])))
    L.append("9. Took the 2025/26 saving as plan 4.6 sets it, each works building's 2025/26 use grossed up by its "
             "measure's 2025/26 saving: %s tonnes; the seven-season average on the 2018/19 use gives %s."
             % (n(F["R10_tonnes"]), n(F["R10_hurried_tonnes"]["average on the 2018/19 use"])))
    L.append("")
    L.append("No other conclusion survives. The before and after funds all three on savings the comparison shows every "
             "building made; the pilot's seven seasons carried flat fund heating optimisation on winters it no longer "
             "saves; each use's saving, or the pilot's own mix, prices this year's controls and insulation applications "
             "at buildings that stand empty less and have less roof than theirs and funds nothing; carrying only one of "
             "the two drivers funds only that measure; and every defensible variant (four or eight bands, the bands as "
             "steps, the empty week read at 40 or 60 per cent of the load's range, every hotel and care home taken as "
             "lived in, insulation on its share of the gas, a two-season baseline, the last seasons carried) funds "
             "insulation and heating controls and leaves heating optimisation over the limit.")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")
