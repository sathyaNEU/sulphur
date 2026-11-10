Response 1

Reviewed 65 resources
· 30m
Recommendation. Commit reinforcement at Ashcombe Road, Fenwick Street and Hartwell Common for winter 2027/28; do not commit capacity reinforcement at Charlecote Way.

Under the rule requiring commitment when demand exceeds firm capacity on more than 10% of design days, their nine-in-ten peaks are 26.7 MW against 23.0 MW, 31.3 MW against 30.5 MW, and 20.8 MW against 17.8 MW, respectively; Charlecote remains at 21.8 MW against 22.5 MW.

Final answers. The following results are in Halverton_Winter_2027-28_Capacity_Review.xlsx, principally the Review and Contract Bridge sheets, and in slides 2-3 of the capex deck.

All figures below are MW. Delivery refers to the half-hours ending 17:30 and 18:00, following the planning guideline.

Zone	Design demand before flex	Delivery 17:30 / 18:00	MW off daily peak	Expected daily peak	Nine-in-ten peak	Firm capacity	Action
Ashcombe Road	30.1	7.9 / 8.0	4.2	26.0	26.7	23.0	Commit
Charlecote Way	24.9	4.0 / 4.0	3.9	21.0	21.8	22.5	No commit
Fenwick Street	35.5	5.3 / 5.3	5.2	30.3	31.3	30.5	Commit
Hartwell Common	22.9	2.8 / 2.9	2.9	20.0	20.8	17.8	Commit
The contract-to-peak bridges are:

Ashcombe: 21.0 MW contracted → 8.0 MW mean central delivery → 4.2 MW off the daily peak. Rebound moves the modeled mean-profile peak to 20:00.
Charlecote: 7.5 MW contracted → 4.0 MW mean central delivery → 3.9 MW off the daily peak.
Fenwick: 10.0 MW contracted → 5.3 MW mean central delivery → 5.2 MW off the daily peak.
Hartwell: 7.5 MW contracted → 2.8 MW mean central delivery → 2.9 MW off the daily peak. Its ending-18:00 delivery is slightly higher than the two-interval average.
These bridges use fitted design-day availability of 37.9% for Corvane and 53.1% for Quillon, then apply the service ramp and rebound before finding the whole-day maximum. The calculations and profiles are in Contract Bridge, Models and Profiles.

The historical-only approach would have missed last winter's inferred central delivery by 0.19 MW on average, measured as event-weighted mean absolute error:

Zone	Held-out events	Average absolute miss
Ashcombe Road	65	0.21 MW
Charlecote Way	51	0.15 MW
Fenwick Street	59	0.24 MW
Hartwell Common	57	0.16 MW
All zones	232	0.19 MW
Training used winters 2023/24 and 2024/25 only; testing used 2025/26. The historical delivery-ratio comparator missed by 0.48 MW overall. These results, including event-level calculations, are in Backtest and slide 4.

The important qualification is that delivery is inferred from primary demand, not directly metered provider output. No provider delivery-meter series was supplied.

Step-by-step process.

Established the planning rules and inputs. Read all files in input-assets/10.1.zip. The capacity guideline defines the design weekday at -3.0 C, the growth treatment, firm capacities and the exceedance threshold. The contract award notice supplies current and historical contracted MW and the service window. The primary register supplies SCADA mappings and DFES growth; the feeder workbook maps connection records to primaries.

Cleaned the primary demand data. From primary_demand_halfhourly_2023-2026.csv, removed 441 exact duplicates from 196,213 rows, leaving 195,772. There were no conflicting MW duplicate groups or unmatched identifiers. Removed 54 intervals outside local November-March dates, leaving 195,718. Treated 896 S-quality and 31 B-quality readings as missing, retaining 194,791 good measurements. A further 356 expected records were absent. Demand was neither interpolated nor zero-filled. Midnight interval endings were assigned to the preceding demand day.

Prepared weather and calendar eligibility. In halverton_weather_hourly_2023-2026.csv, retained the latest version of each station-hour: 13,372 records became 13,062 unique readings. These form 547 GMT daily means: 488 days with 24 readings, 52 with 23, and 7 with 22. Used available-hour means and tested exclusion of incomplete days. Applied England working weekdays, bank holidays and the specified Christmas/New Year exclusion.

Resolved instructions and switching. The flexibility event file's 697 records became 643 final instructions after removing 54 superseded revisions: 606 Completed and 37 Cancelled. The switching log's 60 operations formed 30 transfer episodes, affecting 80 primary-days across the network. Excluded both sides of each transfer for every date touched. Removing 11 completed events on affected days left 595 usable events, comprising 363 training events and 232 held-out events.

Built clean demand baselines and connection growth. Across the four zones, 1,816 primary-days reduced to 1,192 calendar-eligible days, then 549 without instructions, 536 after switching exclusions, and 498 complete good-quality baseline days. The latest-winter forecast uses 25 Ashcombe, 41 Charlecote, 33 Fenwick and 35 Hartwell days. All 58 growth-register rows mapped to feeders. Excluded 13 inactive or superseded rows, 14 projects already energised before the growth window, and 3 after it. The resulting 28 eligible projects include 10 in the four zones.

Forecast design-day demand. Fitted temperature regressions separately by primary and winter for daily maxima and each half-hour. The 2025/26 design peaks are 26.7, 23.5, 33.3 and 20.9 MW, in the zone order used above. Compounded the specified DFES growth rates, then added qualifying connections of 2.3, 0.7, 0.9 and 1.2 MW. Every half-hour was scaled consistently with the resulting peak growth.

Estimated deliverable flexibility and whole-day peaks. Inferred historical delivery from clean-day counterfactual demand minus observed event demand. Fitted a provider-specific, temperature-dependent available-capacity model capped by the actual instruction. This avoids treating a successfully delivered small instruction as proof that the full registered portfolio is available. Applied the estimated service shape and post-window rebound, then found the maximum across all 48 half-hours.

Calculated uncertainty and checked the result. Used 250 joint bootstrap fits and 100,000 predictive design-day draws, retaining the dependence between uncertain demand baselines and inferred flexibility. The P90 is the predictive percentile of daily maxima, not a confidence limit for mean demand. Complete-weather, common-temperature-slope, cancelled-day and conservative shape-variability checks all retained the recommendation. P90s from the two halves of the simulation differed by less than 0.1 MW in every zone.

Excluded irrelevant evidence and verified the artifacts. Inspected the DUoS statement, customer-interruption workbook and transformer-condition workbook, but did not use tariffs, CI/CML or health indices to determine capacity compliance. The Method sheet records their exclusion rationale. Reopened both deliverables, reconciled workbook summaries and MAE against stored detail, checked for spreadsheet error cells and external dependencies, and visually inspected every slide.

Assumptions and judgment calls.

Counterfactual delivery: Primary demand differences are the available delivery proxy. Held-out 2025/26 clean-day fits construct evaluation outcomes only; they do not fit the delivery predictions.
Cold extrapolation: Latest-winter clean observations start at 5.0 C at Ashcombe and 4.7 C elsewhere, above the -3.0 C design condition. Historical-slope and cancelled-day sensitivities do not change the decisions, but model misspecification remains a risk.
Portfolio scaling: Availability and mean service shape are assumed to scale with contracted capacity and remain comparable in 2027/28. This matters particularly for Ashcombe's increase from 7.5 MW to 21.0 MW.
Shape uncertainty: The main forecast does not treat every observed shape residual as physical variability because those residuals also contain demand-inference noise. The separate conservative stress does so and still leaves Charlecote below firm capacity and the other zones above it.
Validation scope: The backtest uses observed daily temperature and tests central delivery means. It does not validate weather-forecast error or whole-day peak-tail coverage. The nine-in-ten levels are therefore model-dependent planning estimates, not measured compliance guarantees.
Capital scope: The modeled P90 gaps of 3.7 MW, 0.8 MW and 3.0 MW are screening requirements, not selected transformer ratings or project costs. Commitment is for December 2026, with energisation required by 31 October 2027.
Alternatives rejected.

Credit the contract's full nameplate MW. The inferred availability model supports only 37.9% or 53.1% at the design temperature, depending on provider. Instruction caps conceal availability on lightly called days.
Subtract central delivery directly from the original peak. Ashcombe's rebound shifts the constraint to 20:00, reducing its peak benefit to 4.2 MW despite 8.0 MW central delivery. Even the no-rebound sensitivity has a 24.4 MW P90, above its 23.0 MW firm capacity.
Defer Fenwick because its average peak fits. Its 30.3 MW expected peak is below 30.5 MW firm capacity, which is evidence in favour of deferral on a mean-only basis. The required tail test instead gives 31.3 MW, so commitment is necessary.
Use a simple historical delivery ratio. Its held-out average miss is 0.48 MW, compared with 0.19 MW for the capped, weather-aware model.
Commit Charlecote on capacity grounds. Its main P90 is 21.8 MW, and the conservative shape stress gives 22.0 MW, both below 22.5 MW firm capacity. Condition-led replacement remains a separate question.
Files produced.

Halverton_Winter_2027-28_Capacity_Review.xlsx: Decision dashboard, native Excel charts, contract bridges, profiles, historical backtest, sensitivity checks, source audit and supporting calculation data.
Halverton_Winter_2027-28_Capex_Review.pptx: Six capex-review slides covering the recommendation, zone results, peak-shift explanation, backtest, sensitivities and commitment actions.
Both files are saved under /home/agent/workspace. Temporary analysis files have been removed.

Packages installed. Installed in an isolated temporary environment because they were absent from the available interpreter: numpy, pandas, scipy, statsmodels, openpyxl, python-pptx, pymupdf, matplotlib, xlsxwriter and pillow, with their dependencies.
