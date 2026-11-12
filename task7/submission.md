## Tags

**Domain:** Energy Systems & Utilities, energy efficiency and demand response evaluation.
**Analytical objective:** Experiment & Causal Analysis.

## Final Recommendation

**Fund roof insulation alone in the 2026 round: €85.53 of grant per lifetime tonne of CO2 with its 90% range €79.67 to €94.17, within the €120 limit; neither heating optimisation (range up to €233.08) nor heating controls (up to €158.03) meets the committee's rule.** This rejects funding all three, which heating optimisation's seasons as measured (about €66 a tonne, range up to about €107) and ranges drawn building by building (controls up to about €109) give: the measured seasons carry the closed campaign's checks that the pilot's balanced works buildings held, and the pilot was drawn by owner.

## Supplementary Questions

### grant_round_2026_appraisal.xlsx

1. Sheet 'measures', each measure's saving rate over its life on the applications received by 12 June, as a share of their reference consumption: insulation 20.73% (within 1.2 points), heating optimisation 2.33% (within 0.4 points), heating controls 13.89% (within 1 point); sheet 'applications' carries every application received (a revised application replacing the earlier one) with its own rate and lifetime tonnes.
2. Sheets 'measures' and 'ranges', grant per lifetime tonne of CO2 with its 90% range, the range the estimate would have if the pilot's owners were drawn again: insulation €85.53 (€79.67 to €94.17), heating optimisation €100.92 (€65.25 to €233.08), heating controls €98.90 (€78.04 to €158.03). Graded: each grant per tonne (insulation's and controls' within 5 per cent, heating optimisation's within 15) and each range's upper end, the end the committee judges (insulation's within 10 per cent, controls' within 15, heating optimisation's within 30, its upper tail resting on few owners); the low ends are shown and not graded.
3. Sheet 'round at close', each measure's applications once the offer closes on 30 June and the grant they ask (each within 10 per cent): insulation 198 applications asking €5,813,088, heating optimisation 801 asking €1,208,872, heating controls 515 asking €3,091,923.
4. Sheet 'funded applications', every application received by 12 June for the funded measure, insulation, one row each in application order (application number, building, owner number, received, use, measure, grant, lifetime tonnes, each application's tonnes within 5 per cent), closed by the total: 69 applications asking €1,553,940 for 18,168 lifetime tonnes of CO2 in all (within 10 per cent).

### grant_round_2026_note.pdf

5. One page for the committee's paper: the answer first (fund insulation alone), a table of each measure's grant per tonne, 90% range, verdict and round at close, a chart of the three ranges against the €120 limit, and three short paragraphs: why not heating optimisation, why not heating controls, and the round.

## Critical Components

1. Heating optimisation's works alone keep **1.81%, 1.36% and 1.25%** of the gas in 2023/24, 2024/25 and 2025/26 (each works building's seasons before its own campaign check; each within 0.6 points), against 3.30%, 3.34% and 3.46% as measured.
2. Heating optimisation saves **2.33%** over its life on this year's applications, so its grant per tonne is **€100.92** with a 90% range up to **€233.08** (within 30 per cent), not about €66 from the seasons as measured.
3. Heating controls' 90% range, the pilot's owners drawn again, reaches **€158.03** at its upper end (within 15 per cent; point €98.90); drawn building by building it would stop at about €109.

## Step-by-Step

1. Rebuilt every building's normal-weather gas use season by season from `gas_meter_reads_2013_2026.csv` through `meter_points_2026.csv`, `calorific_values_2013_2026.csv` and the weather station, as the benchmarking method sets out (exchanges, rollovers, corrections and off-date reads handled).
2. Set each measure's works buildings against the owners the draw passed over (`pilot_2019_responses_and_draw.xlsx`, rules 3), each against its own 2018/19 season: heating optimisation 8.81% in 2019/20 levelling at about 3.37% from 2022/23; insulation 18.58% and controls 6.78% in 2025/26.
3. Tested what held heating optimisation level: the service reads in the meter file date each building's campaign check (September 2022 to March 2026, `municipal_heat_plan_2026_summary.pdf`), and a works building's saving steps up from its own check while a passed-over building's falls back within a winter; read off the seasons before each works building's check, the works alone keep 1.25% by 2025/26. The shallow reading carries the measured 3.37%, or reads the levelling as the 2022 price shock, which moved both arms alike.
4. Carried heating optimisation over its fifteen years against the gas the building would burn without the works, the campaign closed: the seasons as observed, then the level of the last three (1.60%), 2.33% on this year's applications, against 3.54% from the measured seasons, whose own back-test passes because every late season carried the campaign.
5. Carried controls along the share of the week each building stands empty, read off `electricity_load_profiles_2025.csv` with hotels and care homes lived in round the clock, and insulation along its roof per floor from `solar_cadastre_rooftops_2024.xlsx` over the register: this year's applications stand emptier and have more roof per floor than the pilot's works buildings, so controls save 13.89% and insulation 20.73% over their lives, not each use's pilot saving.
6. Priced every application on `applications_2026.xlsx` (a revised application replacing the earlier one) at its own building's saving and its reference consumption, as the climate action plan's appraisal sets it: €85.53, €100.92 and €98.90 a tonne.
7. Built each range as the committee asks, the pilot drawn again: owners resampled within each measure's drawn and passed-over owners with all their buildings, every step repeated (`buildings_register_2026.xlsx` gives each owner): insulation up to €94.17, heating optimisation up to €233.08, controls up to €158.03. Resampling buildings gives controls about €89 to €109, under the limit, because an owner's facility manager runs all its buildings alike.
8. Applied the committee's rule (`committee_request_2026-06-15.docx`): insulation alone has its range's upper end within €120.
9. Projected each measure's round to the 30 June close from the 2019 answers' timing and sizes (`pilot_2019_responses_and_draw.xlsx` against `applications_2026.xlsx`): insulation 198 applications asking €5,813,088, heating optimisation 801, heating controls 515.
10. Listed the funded measure's applications received so far: insulation's 69, asking €1,553,940 for 18,168 lifetime tonnes; the careful but hurried route, funding all three, would list every application received.

No other conclusion survives. Carrying heating optimisation's measured seasons funds it at about €66, but each works building's own check record shows the level came from a closed campaign; resampling buildings funds controls, but the pilot was drawn by owner (rules 3) and an owner's buildings move together; pricing by use or by the pilot's own mix ignores that this year's buildings stand emptier and have more roof per floor. Every reasonable reading of the seasons before each check and every owner-level range keeps optimisation and controls over €120 at the upper end and insulation under it.
