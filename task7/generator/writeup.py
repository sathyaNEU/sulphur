"""task7 architecture 9: submission.md, the four answer blocks the author pastes into the platform, every figure taken
from figures.json at the precision the golden deliverables print it (percentages to two decimals, grant per tonne to
the cent, money to the euro, counts and totals whole)."""

IM, HM, CM = "insulation", "heating optimisation", "heating controls"
MEAS = [IM, HM, CM]
NAME = {IM: "Insulation", HM: "Heating optimisation", CM: "Heating controls"}


def n(v):
    return format(int(round(v)), ",")


def p(v):
    return "%.2f%%" % v


def e(v):
    return "€%s" % format(v, ",.2f")


def eu(v):
    return "€%s" % format(int(round(v)), ",")


def g(v):
    """a stated band, as the generator's parameter gives it"""
    return ("%g" % v)


def write(F, path):
    cv = F["conventions"]
    bp, bpt = cv["bands_pct"], cv["bands_points"]
    se = F["seasons"]
    rg, rb, et = F["range"], F["range_building"], F["eur_t"]
    own, meas = F["R2_own"], F["R1"][HM]
    last3_meas = F["measured_level_last3"]
    L = []
    L.append("## Tags")
    L.append("")
    L.append("**Domain:** Energy Systems & Utilities, energy efficiency and demand response evaluation.")
    L.append("**Analytical objective:** Experiment & Causal Analysis.")
    L.append("")
    L.append("## Final Recommendation")
    L.append("")
    L.append("**Fund roof insulation alone in the 2026 round: %s of grant per lifetime tonne of CO2 with its 90%% range "
             "%s to %s, within the €120 limit; neither heating optimisation (range up to %s) nor heating controls (up to "
             "%s) meets the committee's rule.** This rejects funding all three, which heating optimisation's seasons as "
             "measured (about %s a tonne, range up to about %s) and ranges drawn building by building (controls up to "
             "about %s) give: the measured seasons carry the closed campaign's checks that the pilot's balanced works "
             "buildings held, and the pilot was drawn by owner."
             % (e(et[IM]), e(rg[IM][0]), e(rg[IM][1]), e(rg[HM][1]), e(rg[CM][1]), eu(F["measured_opt_eur_t"]),
                eu(F["measured_opt_range"][1]), eu(rb[CM][1])))
    L.append("")
    L.append("## Supplementary Questions")
    L.append("")
    L.append("### grant_round_2026_appraisal.xlsx")
    L.append("")
    k = 1
    L.append("%d. Sheet 'measures', each measure's saving rate over its life on the applications received by 12 June, as a "
             "share of their reference consumption: insulation %s (within %s points), heating optimisation %s (within %s "
             "points), heating controls %s (within %s point); sheet 'applications' carries every application received "
             "(a revised application replacing the earlier one) with its own rate and lifetime tonnes."
             % (k, p(F["rates"][IM]), g(bpt["rate over the life"][IM]), p(F["rates"][HM]),
                g(bpt["rate over the life"][HM]), p(F["rates"][CM]), g(bpt["rate over the life"][CM])))
    k += 1
    L.append("%d. Sheets 'measures' and 'ranges', grant per lifetime tonne of CO2 with its 90%% range, the range the "
             "estimate would have if the pilot's owners were drawn again: insulation %s (%s to %s), heating optimisation "
             "%s (%s to %s), heating controls %s (%s to %s). Graded: each grant per tonne (insulation's and controls' "
             "within %s per cent, heating optimisation's within %s) and each range's upper end, the end the committee "
             "judges (insulation's within %s per cent, controls' within %s, heating optimisation's within %s, its upper "
             "tail resting on few owners); the low ends are shown and not graded."
             % (k, e(et[IM]), e(rg[IM][0]), e(rg[IM][1]), e(et[HM]), e(rg[HM][0]), e(rg[HM][1]), e(et[CM]),
                e(rg[CM][0]), e(rg[CM][1]), g(bp["grant per tonne"][IM]), g(bp["grant per tonne"][HM]),
                g(bp["range upper end"][IM]), g(bp["range upper end"][CM]), g(bp["range upper end"][HM])))
    k += 1
    L.append("%d. Sheet 'round at close', each measure's applications once the offer closes on 30 June and the grant they "
             "ask (each within %s per cent): insulation %s applications asking %s, heating optimisation %s asking %s, "
             "heating controls %s asking %s." % (k, g(bp["round at close"]), n(F["close"][IM]["n"]),
                                                 eu(F["close"][IM]["grant"]), n(F["close"][HM]["n"]),
                                                 eu(F["close"][HM]["grant"]), n(F["close"][CM]["n"]),
                                                 eu(F["close"][CM]["grant"])))
    k += 1
    L.append("%d. Sheet 'funded applications', every application received by 12 June for the funded measure, insulation, one "
             "row each in application order (application number, building, owner number, received, use, measure, grant, "
             "lifetime tonnes, each application's tonnes within %s per cent), closed by the total: %s applications asking "
             "%s for %s lifetime tonnes of CO2 in all (within %s per cent)."
             % (k, g(bp["an application's lifetime tonnes"]), n(F["n_apps"][IM]), eu(F["funded_grant"]),
                n(F["funded_tonnes"]), g(bp["the funded total"])))
    k += 1
    L.append("")
    L.append("### grant_round_2026_note.pdf")
    L.append("")
    L.append("%d. One page for the committee's paper: the answer first (fund insulation alone), a table of each measure's "
             "grant per tonne, 90%% range, verdict and round at close, a chart of the three ranges against the €120 "
             "limit, and three short paragraphs: why not heating optimisation, why not heating controls, and the round."
             % k)
    L.append("")
    L.append("## Critical Components")
    L.append("")
    L.append("1. Heating optimisation's works alone keep **%s, %s and %s** of the gas in %s, %s and %s (each works "
             "building's seasons before its own campaign check; each within %s points), against %s, %s and %s as "
             "measured." % (p(own[-3]), p(own[-2]), p(own[-1]), se[-3], se[-2], se[-1], g(bpt["own saving by season"]),
                            p(meas[-3]), p(meas[-2]), p(meas[-1])))
    L.append("2. Heating optimisation saves **%s** over its life on this year's applications, so its grant per tonne is "
             "**%s** with a 90%% range up to **%s** (within %s per cent), not about %s from the seasons as measured."
             % (p(F["R3_rate"]), e(et[HM]), e(rg[HM][1]), g(bp["range upper end"][HM]), eu(F["measured_opt_eur_t"])))
    L.append("3. Heating controls' 90%% range, the pilot's owners drawn again, reaches **%s** at its upper end (within %s "
             "per cent; point %s); drawn building by building it would stop at about %s."
             % (e(rg[CM][1]), g(bp["range upper end"][CM]), e(et[CM]), eu(rb[CM][1])))
    L.append("")
    L.append("## Step-by-Step")
    L.append("")
    s = 1
    L.append("%d. Rebuilt every building's normal-weather gas use season by season from `gas_meter_reads_2013_2026.csv` "
             "through `meter_points_2026.csv`, `calorific_values_2013_2026.csv` and the weather station, as the "
             "benchmarking method sets out (exchanges, rollovers, corrections and off-date reads handled)." % s)
    s += 1
    L.append("%d. Set each measure's works buildings against the owners the draw passed over (`pilot_2019_responses_and_draw.xlsx`, "
             "rules 3), each against its own 2018/19 season: heating optimisation %s in 2019/20 levelling at about %.2f%% "
             "from 2022/23; insulation %s and controls %s in 2025/26." % (s, p(meas[0]), last3_meas, p(F["R1"][IM][-1]),
                                                                       p(F["R1"][CM][-1])))
    s += 1
    L.append("%d. Tested what held heating optimisation level: the service reads in the meter file date each building's "
             "campaign check (September 2022 to March 2026, `municipal_heat_plan_2026_summary.pdf`), and a works "
             "building's saving steps up from its own check while a passed-over building's falls back within a winter; "
             "read off the seasons before each works building's check, the works alone keep %s by 2025/26. The shallow "
             "reading carries the measured %.2f%%, or reads the levelling as the 2022 price shock, which moved both arms "
             "alike." % (s, p(own[-1]), last3_meas))
    s += 1
    L.append("%d. Carried heating optimisation over its fifteen years against the gas the building would burn without the "
             "works, the campaign closed: the seasons as observed, then the level of the last three (%.2f%%), %s on this "
             "year's applications, against %s from the measured seasons, whose own back-test passes because every late "
             "season carried the campaign." % (s, F["R3_settled_level"], p(F["R3_rate"]), p(F["R3_measured_rate"])))
    s += 1
    L.append("%d. Carried controls along the share of the week each building stands empty, read off "
             "`electricity_load_profiles_2025.csv` with hotels and care homes lived in round the clock, and insulation "
             "along its roof per floor from `solar_cadastre_rooftops_2024.xlsx` over the register: this year's "
             "applications stand emptier and have more roof per floor than the pilot's works buildings, so controls save "
             "%s and insulation %s over their lives, not each use's pilot saving." % (s, p(F["rates"][CM]),
                                                                                   p(F["rates"][IM])))
    s += 1
    L.append("%d. Priced every application on `applications_2026.xlsx` (a revised application replacing the earlier one) at "
             "its own building's saving and its reference consumption, as the climate action plan's appraisal sets it: %s, %s and "
             "%s a tonne."
             % (s, e(et[IM]), e(et[HM]), e(et[CM])))
    s += 1
    L.append("%d. Built each range as the committee asks, the pilot drawn again: owners resampled within each measure's "
             "drawn and passed-over owners with all their buildings, every step repeated (`buildings_register_2026.xlsx` "
             "gives each owner): insulation up to %s, heating optimisation up to %s, controls up to %s. Resampling "
             "buildings gives controls about %s to %s, under the limit, because an owner's facility manager runs all its "
             "buildings alike." % (s, e(rg[IM][1]), e(rg[HM][1]), e(rg[CM][1]), eu(rb[CM][0]), eu(rb[CM][1])))
    s += 1
    L.append("%d. Applied the committee's rule (`committee_request_2026-06-15.docx`): insulation alone has its range's upper "
             "end within €120." % s)
    s += 1
    L.append("%d. Projected each measure's round to the 30 June close from the 2019 answers' timing and sizes "
             "(`pilot_2019_responses_and_draw.xlsx` against `applications_2026.xlsx`): insulation %s applications asking "
             "%s, heating optimisation %s, heating controls %s." % (s, n(F["close"][IM]["n"]), eu(F["close"][IM]["grant"]),
                                                                    n(F["close"][HM]["n"]), n(F["close"][CM]["n"])))
    s += 1
    L.append("%d. Listed the funded measure's applications received so far: insulation's %s, asking %s for %s lifetime "
             "tonnes; the careful but hurried route, funding all three, would list every application received."
             % (s, n(F["n_apps"][IM]), eu(F["funded_grant"]), n(F["funded_tonnes"])))
    L.append("")
    L.append("No other conclusion survives. Carrying heating optimisation's measured seasons funds it at about %s, but each "
             "works building's own check record shows the level came from a closed campaign; resampling buildings funds "
             "controls, but the pilot was drawn by owner (rules 3) and an owner's buildings move together; pricing by use "
             "or by the pilot's own mix ignores that this year's buildings stand emptier and have more roof per floor. "
             "Every reasonable reading of the seasons before each check and every owner-level range keeps optimisation "
             "and controls over €120 at the upper end and insulation under it." % eu(F["measured_opt_eur_t"]))
    open(path, "w", encoding="utf-8").write("\n".join(L) + "\n")
