## Tags

**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, grid reliability and outage analysis (the 69 kV fault record).
**Analytical objective:** Data Extraction & Conformation (ETL / Pipeline Build).

## Final Recommendation

**This winter, fit perch guards at 6 roost structures, replace 4 cracked strings (Line 9, structure 137 among them, 3.2 km past the solar tap), wash 9 coastal sections before 1 December and remove the hazard trees at 2 dead pine stands; before next summer, clear 4 grow-in spans.** Not the list the relays' own distances, the airport's fog and the past flashovers give, which replaces strings at the roost structures, clears spans where the relays put the tree contacts (1.9 to 9.6 km from the trees) and washes sections already cleaned in October.

## Supplementary Questions

### lpec_69kv_faults_2022-2026.csv

1. One row per 69 kV fault since 1 January 2022, 436 rows, in time order: date and time (Central), line and its terminals, distance from terminal A, the structure (and the span for a tree), fault type, cause in the procedure's categories, whether it cleared on reclose, members interrupted, member-minutes, momentary members, and the repeat location it belongs to. Faults by year: 2022 96, 2023 93, 2024 83, 2025 84, 2026 (January to October) 80, each within 1.

### lpec_69kv_fault_review_2026.xlsx

2. Faults by line and cause for each year. The 2026 faults by cause: lightning 9, bird or other animal 6, salt contamination 16, insulator failure 16, vegetation grown into the line 14, vegetation from outside the right of way 8, vehicle or other third party 5, equipment or hardware 2, other or unknown 4, each within 2.
3. The 2026 member interruptions and member-minutes by line: 57,024 member interruptions and 1,227,611 member-minutes in all, each within 2 per cent; by line (interruptions and member-minutes) Line 2 16,115 and 179,995; Line 5 11,171 and 172,224; Line 8 10,259 and 354,807; Line 9 1,168 and 27,196; Line 10 14,894 and 199,267; Line 13 3,417 and 294,124; no other line had a member out for more than five minutes.
4. Every repeat location with its cause, a structure within 2 of the one given (a span within 1): perch guards at Line 12, structure 104; Line 14, structure 117; Line 16, structure 23; Line 6, structure 79; Line 7, structure 31; Line 7, structure 52 (bird or other animal); replace the string at Line 15, structure 57; Line 2, structure 63; Line 5, structure 88; Line 9, structure 137 (insulator failure); clear the span at Line 10, structures 47-48; Line 10, structures 88-89; Line 14, structures 63-64; Line 6, structures 57-58 (vegetation grown into the line); remove the hazard trees at Line 11, structures 118-120; Line 13, structures 103-107 (vegetation from outside the right of way). Fixed after their last fault: Line 7 structure 38 (bird or other animal); Line 12 structure 96 (bird or other animal); Line 5 structure 101 (vegetation grown into the line); Line 14 structure 131 (vegetation grown into the line); Line 1 structure 48 (insulator failure); Line 3 structure 42 (insulator failure); Line 13 structure 72 (insulator failure).

### 69kv_work_list_winter_2026-27.docx

5. One page to the manager of engineering: this winter the perch guards, the four strings, the washing before 1 December (Line 2 sections 1 to 5 and 7; Line 3 sections 4, 5 and 7) and the hazard trees; before next summer the four spans; each with why the crew goes there.

## Critical Components

1. The trees: grow-in spans to clear at **Line 10, structures 47-48; Line 10, structures 88-89; Line 14, structures 63-64; Line 6, structures 57-58** and the hazard-tree stands at **Line 11, structures 118-120; Line 13, structures 103-107**, located by how each fault's residual current split between the two ends of its line, Line 10's 2022 and 2023 contacts read against the 2022 protection study; the relays' own distances put them **1.9 to 9.6 km** away.
2. The night faults at **6** roost structures are bird streamers (perch guards), not salt, and the **4** strings that flash over in light rain at any hour are failing porcelain.
3. The string on the solar tap line is at **Line 9, structure 137**, 3.2 km past the tap, not where Shell Ridge's relay reads it (Line 9, structure 148).
4. **9** washing sections are due before the fog season (Line 2 sections 1 to 5 and 7; Line 3 sections 4, 5 and 7): their deposit on 31 October is at or above the **0.032 mg/cm2** at which the porcelain has flashed over in fog (0.029 to 0.039 under the other defensible fits, every one of which files the same 9 sections).

## Step-by-Step

1. Built one fault per two-ended trip sequence in `scada_soe_2022-2026.csv` (both terminals' breakers out within a second; single-ended protection trips with no fault record are relay tests) and matched every relay record in `relay_events_eventrecall_export_2022-2026.csv` (UTC, miles) and `relay_records_gridvue_2022-2026.json` (local time, km, kA) on its own clock, set against SCADA: 436 faults, 80 of them in 2026.
2. Located each fault by how its residual current split between the two terminals, solved against the line-out zero-sequence sources in `protection_study_2022.pdf` for faults before Inland's new autotransformer (14 March 2024, `substation_register_2026.xlsx`) and `protection_study_2025.pdf` after. The relays' own distances assume no fault resistance and no infeed, and put the tree contacts 1.9 to 9.6 km from their spans; the 2025 study for every fault moves Line 10's 2022 and 2023 contacts off the span at structures 47-48, which then drops off the list.
3. On Line 9, past the tap, Ponder Creek keeps no record, so Shell Ridge's distance was corrected for the solar farm's ground current from its own export (`coyote_draw_solar_protection_events_2023-2026.csv`, Central Standard Time): its grounded-wye step-up feeds every fault beyond the tap, by night as well. The string is at Line 9, structure 137; the uncorrected distance reads Line 9, structure 148.
4. Caused each fault from what was there at the time: a stroke within a second along the line (`lightning_strokes_2022-2026.csv`), thunderstorms and fronts for trees from outside the right of way, the roost survey's structures (`waterbird_and_raptor_roost_survey_2021-2026.xlsx`) for pre-dawn faults in roost season, fog at the cooperative's own stations (`substation_weather_stations_2023-2026.csv`) for salt on the Gulf lines' porcelain, and the conductor's heat from `scada_line_loading_hourly_2022-2026.csv` for grow-ins. The airport's visibility misses the fog at the line and the survey left out leaves the roosts reading as failing strings: that route replaces strings at 11 places and fits no guards.
5. Grouped faults of one cause within 400 m (procedure RP-04) and took off what was fixed after the last fault (`line_maintenance_work_orders_2022-2026.csv`, `vegetation_work_orders_2022-2026.csv`, the numbers Lines 8 and 13 carried before their 2023 rebuilds mapped through `structure_inventory_69kv_2026.csv`): 6 perch guards, 4 strings, 4 spans, 2 stands. Counting every summer afternoon fault as a tree also lists the Line 13 pine stand as a span to clear.
6. Rebuilt the 2026 member impact from the SCADA trips, transfers and recloses and `members_by_feeder_monthly_2022-2026.csv`: 57,024 member interruptions and 1,227,611 member-minutes; the outage system's dispatcher-closed times overstate the minutes.
7. Carried each washing section's deposit from its last wash (`insulator_washing_log_2022-2026.xlsx`) or soaking rain at its own rate, the rate fitted on the never-washed test insulators in `esdd_monitoring_2022-2026.xlsx` against distance from the Gulf; the level is the lowest deposit carried to the day of a salt-contamination flashover in the fault table, 0.032 mg/cm2: 9 sections are at or above it. Washing every section that ever flashed over would wash 7, sections cleaned in October among them.

No other list survives the files. A relay's distance is a calculation that assumes a fault with no resistance and nothing feeding it from the side; the two ends' residual currents are not, and the patrols sent to the relays' distances after the tree contacts found nothing. The airport reports one point by the Gulf shore, and its codes miss fog that the cooperative's own stations record along the lines and report fog the lines did not have; the survey and the stations see what was at the structure. A section's past flashovers are not its salt today: nothing has soaked the coast since June and the October washes are clean.
