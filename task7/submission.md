## Tags

**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, energy efficiency and demand response evaluation (verified savings of commercial retrofit measures).
**Analytical objective:** Experiment & Causal Analysis.

## Final Recommendation

Fund **insulation and heating optimisation** in the 2026 round and **not heating controls**: set against the owners the 2019 draw passed over, each up to the season before its first service visit, the pilot's works saved 16%, 6% and 2% of normal-weather gas, so this year's applications come to €90, €90 and €220 of grant a tonne of CO2 against the €120 limit. The plain lottery comparison (13%, 2% and below zero, insulation alone funded) is rejected because service visits reached most passed-over buildings from August 2019, each followed by normal-weather use about 7% lower, and no works building had one.

## Supplementary Questions

### committee_briefing_retrofit_round_2026.pptx

1. The recommendation opens the deck: fund insulation and heating optimisation, not heating controls, with the funded round once the offer closes at about €8 million of grant and 90,000 tonnes of CO2 over the measures' lives.
2. Each measure's saving rate from the 2019 pilot, in whole per cent: insulation 16%, heating optimisation 6%, heating controls 2%.
3. Each measure's grant per tonne on the 2026 applications, to the nearest €10, charted as bars against a line at the €120 limit: insulation €90 and heating optimisation €90 under it, heating controls €220 over it.
4. The CO2 the pilot's works saved in the 2025/26 season, each measure's saving rate on what its works buildings would have used that season without the works: about 3,500 tonnes, to the nearest 500.

### retrofit_round_2026.xlsx

5. A sheet of measures, one row each with its saving rate, applications received by 12 June, grant to the nearest €10,000, lifetime tonnes to the nearest 10, grant per tonne and whether to fund it: insulation 16%, 156 applications, €2,500,000, 28,580 tonnes, €90 a tonne, fund; heating optimisation 6%, 230 applications, €750,000, 8,170 tonnes, €90 a tonne, fund; heating controls 2%, 484 applications, €850,000, 3,800 tonnes, €220 a tonne, do not fund.
6. A sheet of the 386 funded applications received by 12 June (every insulation and heating optimisation application), one row each with its grant, its expected annual saving in whole MWh (the measure's saving rate times the application's reference consumption) and its lifetime tonnes to the nearest 10; together they carry €3,250,000 of grant.
7. The funded round once the offer closes on 30 June: about €8 million of grant and 90,000 lifetime tonnes, each funded measure's applications received by 12 June scaled up by the share of the 2019 responses for that measure in by the same day after the notice (insulation 38%, heating optimisation 58%).

## Critical Components

1. The owners the 2019 draw passed over were not left alone: **1,056 of 1,535** had a service visit by April 2026, district by district from August 2019, each visit cutting the building's normal-weather use by about **7%** for good, and **none** of the 1,218 works buildings had one.
2. Set against every passed-over owner, heating optimisation's saving appears to fade from **about 4 points** in 2019/20 to **under 2** in 2025/26; against passed-over owners not yet visited it holds at **about 6 points** every season, with no trend.
3. The saving rates against owners not yet visited are **16%** for insulation, **6%** for heating optimisation and **2%** for heating controls, against 13%, 2% and below zero on the plain lottery comparison.
4. On the 2026 applications the grant per tonne is **€90** for insulation, **€90** for heating optimisation and **€220** for heating controls, against €280 for heating optimisation on the lottery comparison.

## Step-by-Step

1. Built each building's gas use per season (1 May to 30 April) from gas_meter_reads_2013_2026.csv: index differences between reads, carried across meter exchanges and counter rollovers, with corrections replacing estimates and typos, reads off 30 April shared out as benchmarking_method_2022.pdf sets out, cubic metres converted with each meter point's z-number and factor (meter_points_2026.csv) and the season's calorific value (calorific_values_2013_2026.csv), and a building's meter points summed.
2. Normalised every season to long-term average weather as the notices do (VDI 3807, the use type's hot water share held, degree_days_haldenau.csv).
3. Read the pilot from pilot_2019_responses_and_draw.xlsx: 2,791 responses, 1,256 drawn, 1,218 with works done by 30 September 2019; the draw balances the two groups on the 2018/19 season (the works buildings' mean use within 1.5% of the passed-over buildings', and each building is set against its own 2018/19 use) and on every season before it.
4. The insufficient route: the works buildings against every passed-over owner of the same measure, each against its own 2018/19 season, every season since, gives 13%, 2% and below zero; under the plan's appraisal heating optimisation then costs €280 a tonne and only insulation is funded, and the before and after on the works buildings alone (24%, 15%, 11%) funds all three.
5. Found why that comparison narrows season by season: the service-visit reads in the meter file put 1,056 of the 1,535 passed-over buildings under a visit by April 2026, district by district, each stepping down about 7% against unvisited buildings from its visit, and no works building has one; the narrowing tracks the visits, not the works' age, which is the same for every works building.
6. Rebuilt the comparison season by season from the passed-over buildings not yet visited, each building dropped from its visit season, because a visit falls part way through that season: against unvisited buildings, use in the visit season sits 3% to 6% below the season before it (by visit season) and in the season after about 7% below, so the visit season is only partly treated; the gap now holds flat (heating optimisation about 6 points every season), and the saving rates as the plan's 4.2 sets them (each works building's use as a share of its 2018/19 use, against the comparison buildings' average share, every season, averaged, in whole per cent) are 16%, 6% and 2%.
7. Applied climate_action_plan_2023_extract.pdf 4.4 to applications_2026.xlsx: rate times reference consumption times 0.201 t per MWh times 30, 15 or 10 years; grant per tonne €90, €90 and €220 (break-even saving rates 11.6%, 4.6% and 3.7%), so insulation and heating optimisation are funded and heating controls is not.
8. Projected the funded round to the offer's close on 30 June from the 2019 responses' dates: by the same day after the notice 38% of the insulation responses and 58% of the heating optimisation responses had come in (an insulation quote needs a survey), so each measure's received applications scale by their own share, giving about €8 million and 90,000 lifetime tonnes; one pooled share for both measures would give €7 million and 80,000, because it scales the late-coming insulation applications too little.
9. Took the pilot's 2025/26 saving at the council's rates on what each works building would have used that season without the works (its 2025/26 use divided by one less the rate): about 3,500 tonnes of CO2; the rate on the buildings' 2018/19 use would give about 4,000, because what the works buildings would have used in 2025/26 without the works sits below their 2018/19 use.

No other conclusion survives. The before and after carries the season the notice flagged and the pandemic and price-shock years; the lottery and every comparison drawn from buildings outside the pilot's works keep buildings after their service visit, which no works building had, so they understate every measure alike; reading the narrowing as savings fading is refuted by the flat gap against unvisited buildings. Every comparison that drops visited buildings from their visit season, on any baseline, pooled or by measure, funds insulation and heating optimisation and leaves heating controls well over the limit.
