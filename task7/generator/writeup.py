"""task7 architecture 6: submission.md, the four answer blocks, drafted from figures.json so no figure is typed. Every
figure a block states is one an independent rebuild reproduces at the stated precision."""

LABEL = {"insulation": "insulation", "heating optimisation": "heating optimisation", "heating controls": "heating controls"}


def n(v):
    return format(int(v), ",")


def write(F, path):
    c, r, e, ev, ss, dp = F["call"], F["rates_pct"], F["eur_per_tonne"], F["evidence"], F["season_saving_2026"], F["default_path"]
    ba, be, ab = F["before_after_pct"], F["break_even_pct"], F["answered_by_day_2019_pct"]
    apps = F["applications_by_measure"]
    gm, tm = F["grant_by_measure_eur"], F["tonnes_by_measure"]
    riv = F["at_close_rivals"]
    pf = riv["pooled over the funded measures"]
    md = []
    md += ["## Tags", "",
           "**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, energy efficiency and demand "
           "response evaluation (verified savings of commercial retrofit measures).",
           "**Analytical objective:** Experiment & Causal Analysis.", ""]
    md += ["## Final Recommendation", "",
           "Fund **insulation and heating optimisation** in the 2026 round and **not heating controls**: set against the "
           "owners the 2019 draw passed over, each up to the season before its first service visit, the pilot's works saved %d%%, %d%% and "
           "%d%% of normal-weather gas, so this year's applications come to €%d, €%d and €%d of grant a tonne of CO2 "
           "against the €120 limit. The plain lottery comparison (%d%%, %d%% and below zero, insulation alone funded) is "
           "rejected because service visits reached most passed-over buildings from August 2019, each followed by normal-weather "
           "use about %s%% lower, and no works building had one."
           % (r["insulation"], r["heating optimisation"], r["heating controls"], e["insulation"], e["heating optimisation"],
              e["heating controls"], dp["rates_pct"]["insulation"], dp["rates_pct"]["heating optimisation"],
              ev["visit_step_pct"]), ""]
    md += ["## Supplementary Questions", "", "### committee_briefing_retrofit_round_2026.pptx", "",
           "1. The recommendation opens the deck: fund insulation and heating optimisation, not heating controls, with the "
           "funded round once the offer closes at about €%d million of grant and %s tonnes of CO2 over the measures' lives."
           % (c["at_close_grant_million"], n(c["at_close_tonnes"])),
           "2. Each measure's saving rate from the 2019 pilot, in whole per cent: insulation %d%%, heating optimisation "
           "%d%%, heating controls %d%%." % (r["insulation"], r["heating optimisation"], r["heating controls"]),
           "3. Each measure's grant per tonne on the 2026 applications, to the nearest €10, charted as bars against a line "
           "at the €120 limit: insulation €%d and heating optimisation €%d under it, heating controls €%d over it."
           % (e["insulation"], e["heating optimisation"], e["heating controls"]),
           "4. The CO2 the pilot's works saved in the 2025/26 season, each measure's saving rate on what its works "
           "buildings would have used that season without the works: about %s tonnes, to the nearest 500."
           % n(ss["tonnes"]),
           "", "### retrofit_round_2026.xlsx", "",
           "5. A sheet of measures, one row each with its saving rate, applications received by 12 June, grant to the "
           "nearest €10,000, lifetime tonnes to the nearest 10, grant per tonne and whether to fund it: insulation %d%%, "
           "%s applications, €%s, %s tonnes, €%d a tonne, fund; heating optimisation %d%%, %s applications, €%s, %s tonnes, "
           "€%d a tonne, fund; heating controls %d%%, %s applications, €%s, %s tonnes, €%d a tonne, do not fund."
           % (r["insulation"], n(apps["insulation"]), n(gm["insulation"]), n(tm["insulation"]), e["insulation"],
              r["heating optimisation"], n(apps["heating optimisation"]), n(gm["heating optimisation"]),
              n(tm["heating optimisation"]), e["heating optimisation"], r["heating controls"],
              n(apps["heating controls"]), n(gm["heating controls"]), n(tm["heating controls"]), e["heating controls"]),
           "6. A sheet of the %s funded applications received by 12 June (every insulation and heating optimisation "
           "application), one row each with its grant, its expected annual saving in whole MWh (the measure's saving rate "
           "times the application's reference consumption) and its lifetime tonnes to the nearest 10; together they "
           "carry €%s of grant."
           % (n(c["received_funded_applications"]), n(c["received_funded_grant_eur"])),
           "7. The funded round once the offer closes on 30 June: about €%d million of grant and %s lifetime tonnes, each "
           "funded measure's applications received by 12 June scaled up by the share of the 2019 responses for that measure "
           "in by the same day after the notice (insulation %d%%, heating optimisation %d%%)."
           % (c["at_close_grant_million"], n(c["at_close_tonnes"]), ab["insulation"], ab["heating optimisation"]), ""]
    md += ["## Critical Components", "",
           "1. The owners the 2019 draw passed over were not left alone: **%s of %s** had a service visit by April 2026, "
           "district by district from August 2019, each visit cutting the building's normal-weather use by about "
           "**%s%%** for good, and **none** of the %s works buildings had one."
           % (n(ev["passed_over_visited"]), n(ev["passed_over"]), ev["visit_step_pct"], n(ev["works"])),
           "2. Set against every passed-over owner, heating optimisation's saving appears to fade from **about %d points** "
           "in 2019/20 to **under %d** in 2025/26; against passed-over owners not yet visited it holds at **about %d points** "
           "every season, with no trend."
           % (ev["lottery_gap_2020_whole"], ev["lottery_gap_2026_under"], ev["clean_gap_whole"]),
           "3. The saving rates against owners not yet visited are **%d%%** for insulation, **%d%%** for heating "
           "optimisation and **%d%%** for heating controls, against %d%%, %d%% and below zero on the plain lottery "
           "comparison." % (r["insulation"], r["heating optimisation"], r["heating controls"], dp["rates_pct"]["insulation"],
                            dp["rates_pct"]["heating optimisation"]),
           "4. On the 2026 applications the grant per tonne is **€%d** for insulation, **€%d** for heating optimisation "
           "and **€%d** for heating controls, against €%d for heating optimisation on the lottery comparison."
           % (e["insulation"], e["heating optimisation"], e["heating controls"], dp["eur_per_tonne"]["heating optimisation"]),
           ""]
    md += ["## Step-by-Step", "",
           "1. Built each building's gas use per season (1 May to 30 April) from gas_meter_reads_2013_2026.csv: index "
           "differences between reads, carried across meter exchanges and counter rollovers, with corrections replacing "
           "estimates and typos, reads off 30 April shared out as benchmarking_method_2022.pdf sets out, cubic metres "
           "converted with each meter point's z-number and factor (meter_points_2026.csv) and the season's calorific value "
           "(calorific_values_2013_2026.csv), and a building's meter points summed.",
           "2. Normalised every season to long-term average weather as the notices do (VDI 3807, the use type's hot water "
           "share held, degree_days_haldenau.csv).",
           "3. Read the pilot from pilot_2019_responses_and_draw.xlsx: %s responses, %s drawn, %s with works done by 30 "
           "September 2019; the draw balances the two groups on the 2018/19 season (the works buildings' mean use within "
           "%s%% of the passed-over buildings', and each building is set against its own 2018/19 use) and on every season "
           "before it." % (n(ev["answers"]), n(ev["drawn"]), n(ev["works"]), ev["draw_balance_pct"]),
           "4. The insufficient route: the works buildings against every passed-over owner of the same measure, each "
           "against its own 2018/19 season, every season since, gives %d%%, %d%% and below zero; under the plan's "
           "appraisal heating optimisation then costs €%d a tonne and only insulation is funded, and the before and after "
           "on the works buildings alone (%d%%, %d%%, %d%%) funds all three."
           % (dp["rates_pct"]["insulation"], dp["rates_pct"]["heating optimisation"],
              dp["eur_per_tonne"]["heating optimisation"], ba["insulation"], ba["heating optimisation"],
              ba["heating controls"]),
           "5. Found why that comparison narrows season by season: the service-visit reads in the meter file put %s of the "
           "%s passed-over buildings under a visit by April 2026, district by district, each stepping down about %s%% "
           "against unvisited buildings from its visit, and no works building has one; the narrowing tracks the visits, "
           "not the works' age, which is the same for every works building."
           % (n(ev["passed_over_visited"]), n(ev["passed_over"]), ev["visit_step_pct"]),
           "6. Rebuilt the comparison season by season from the passed-over buildings not yet visited, each building "
           "dropped from its visit season, because a visit falls part way through that season: against unvisited "
           "buildings, use in the visit season sits %d%% to %d%% below the season before it (by visit season) and in the "
           "season after about %s%% below, so the visit season is only partly treated; the gap now holds flat (heating "
           "optimisation about %d "
           "points every season), and "
           "the saving rates as the plan's 4.2 sets them (each works building's use as a share of its 2018/19 use, against "
           "the comparison buildings' average share, every season, averaged, in whole per cent) are %d%%, %d%% and %d%%."
           % (ev["visit_season_step_lo"], ev["visit_season_step_hi"], ev["season_after_step_pct"], ev["clean_gap_whole"],
              r["insulation"],
              r["heating optimisation"], r["heating controls"]),
           "7. Applied climate_action_plan_2023_extract.pdf 4.4 to applications_2026.xlsx: rate times reference "
           "consumption times 0.201 t per MWh times 30, 15 or 10 years; grant per tonne €%d, €%d and €%d (break-even "
           "saving rates %s%%, %s%% and %s%%), so insulation and heating optimisation are funded and heating controls is "
           "not." % (e["insulation"], e["heating optimisation"], e["heating controls"], be["insulation"],
                     be["heating optimisation"], be["heating controls"]),
           "8. Projected the funded round to the offer's close on 30 June from the 2019 responses' dates: by the same day "
           "after the notice %d%% of the insulation responses and %d%% of the heating optimisation responses had come in (an "
           "insulation quote needs a survey), so each measure's received applications scale by their own share, giving "
           "about €%d million and %s lifetime tonnes; one pooled share for both measures would give €%d million and %s, "
           "because it scales the late-coming insulation applications too little."
           % (ab["insulation"], ab["heating optimisation"], c["at_close_grant_million"], n(c["at_close_tonnes"]),
              pf["grant_million"], n(pf["tonnes"])),
           "9. Took the pilot's 2025/26 saving at the council's rates on what each works building would have used that "
           "season without the works (its 2025/26 use divided by one less the rate): about %s tonnes of CO2; the rate on "
           "the buildings' 2018/19 use would give about %s, because what the works buildings would have used in 2025/26 "
           "without the works sits below their 2018/19 use."
           % (n(ss["tonnes"]), n(ss["static_2019_use_display"])),
           "",
           "No other conclusion survives. The before and after carries the season the notice flagged and the pandemic and "
           "price-shock years; the lottery and every comparison drawn from buildings outside the pilot's works keep "
           "buildings after their service visit, which no works building had, so they understate every measure "
           "alike; reading the narrowing as savings fading is refuted by the flat gap against unvisited buildings. Every "
           "comparison that drops visited buildings from their visit season, on any baseline, pooled or by measure, funds "
           "insulation and heating optimisation and leaves heating controls well over the limit."]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md) + "\n")
