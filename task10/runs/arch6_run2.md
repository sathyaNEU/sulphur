Response 2

Reviewed 88 resources
· 34m
Recommendation. Commit reinforcement at Ashcombe Road, Fenwick Street and Hartwell Common for winter 2027/28; do not commit Charlecote Way on capacity grounds.

Their post-flexibility P90 peaks are 27.1, 31.3 and 20.6 MW, above firm capacities of 23.0, 30.5 and 17.8 MW respectively. Charlecote's P90 is 21.8 MW, below 22.5 MW firm. The planning rule requires commitment where demand exceeds firm capacity on more than one design day in ten.

Final answers. All demand and delivery figures below are MW. "P90" is the predicted whole-day peak level met or stayed below on nine design days in ten, not a confidence bound on the mean.

Zone	Before flexibility	Mean delivery at the two reference half-hours	Off the day's peak	Expected peak	P90 peak	Firm capacity	Decision
Ashcombe Road	30.3	8.0	4.3	25.9	27.1	23.0	Commit
Charlecote Way	24.9	3.8	3.7	21.2	21.8	22.5	Do not commit
Fenwick Street	35.6	5.4	5.3	30.3	31.3	30.5	Commit
Hartwell Common	23.0	2.9	2.9	20.1	20.6	17.8	Commit
These results are in Halverton_Winter_2027-28.xlsx, sheet Decision, and slides 1-2 of Halverton_Capex_Review.pptx. Figures round independently; calculations retain full precision.

The contract-to-peak bridge is:

Zone	Contract MW	Design-day availability	Delivered at 17:30	Delivered at 18:00	Mean delivered MW	Off peak MW
Ashcombe Road	21.0	38.3%	8.0	8.1	8.0	4.3
Charlecote Way	7.5	50.9%	3.8	3.8	3.8	3.7
Fenwick Street	10.0	54.0%	5.4	5.4	5.4	5.3
Hartwell Common	7.5	38.2%	2.8	2.9	2.9	2.9
The times are interval-ending labels. The bridge is documented in Contract Bridge, Profiles and slide 2.

Ashcombe explains why delivery cannot simply be deducted from the original peak. Its mean profile falls to 22.2 MW at 18:00, but is already 23.9 MW at 16:00 before service, and rebounds to 25.9 MW at 20:00 after service. That leaves only 4.3 MW of whole-day peak relief from 8.0 MW of reference delivery. The profile chart and explanation are in Profiles and slide 3.

The prior-winters-only backtest gives:

Zone	Scored 2025/26 events	Mean absolute miss
Ashcombe Road	65	0.15 MW
Charlecote Way	51	0.11 MW
Fenwick Street	59	0.17 MW
Hartwell Common	57	0.11 MW
All zones, event weighted	232	0.13 MW
Both the delivery model and its counterfactual baseline were fitted using 2023/24 and 2024/25 only. The score measures the absolute miss in each event's average delivery across the two reference half-hours. Results and individual events are in Backtest, Event Detail and slide 4.

Important qualification: the pack contains no independently metered provider-delivery series. Historical delivery is inferred from primary SCADA against a fitted no-flexibility counterfactual. The backtest is therefore an inference backtest, not settlement-meter accuracy.

Step-by-step process.

Read all 12 files inside input-assets/10.1.zip. capacity_assessment_guideline_2026.pdf established the design condition, growth treatment, firm capacities and decision rule. flexibility_contract_awards_2027-28.pdf supplied current and historical contracts and the service window. primary_substation_register.xlsx supplied SCADA mappings and DFES growth rates.

Read primary_demand_halfhourly_2023-2026.csv, halverton_weather_hourly_2023-2026.csv, flexibility_events_2023-2026.csv and control_room_switching_log_2023-2026.csv for demand, weather, dispatch and network-state observations. Joined load_growth_register_2026-27.xlsx to network_feeders_11kv.xlsx using both modern and legacy feeder identifiers.

Inspected but did not use three contextual files in the capacity model. customer_interruptions_2025-26.xlsx measures historical reliability, not design-day thermal loading. primary_transformer_condition_2026.xlsx informs asset-health renewal, but supplies no mandated capacity derating. duos_charging_statement_2027-28.pdf describes tariffs; its red band does not replace the contracted service window.

Cleaned 196,213 SCADA rows, removing 441 exact duplicates. Of the 195,772 unique records, 896 S-quality and 31 B-quality values were excluded from fitting; no demand was imputed. All SCADA labels mapped successfully. Excluded 54 readings outside the November-March assessment season. Weather reconciliation removed 310 older versions, leaving 13,062 hourly observations. Daily means used the available 22-24 readings, without imputation.

Resolved 697 instruction rows to 643 final instructions, removing 54 superseded revisions. Final outcomes were 606 completed schedules and 37 cancellations. Paired 60 switching operations into 30 transfer spans, excluding both endpoint primaries throughout each span. Event modelling retained 593 events after removing 11 switching-affected events and 2 events lacking required good-quality observations.

Built each design-demand baseline from winter 2025/26, at a daily mean temperature of -3.0 C. Each zone began with 151 calendar days, reduced to 99 working, non-blackout days. In Ashcombe, Charlecote, Fenwick and Hartwell order, event exclusions were 67, 52, 59 and 57 days; additional switching exclusions were 1, 1, 0 and 0; incomplete/non-G exclusions were 2, 1, 4 and 3. This left 29, 45, 36 and 39 complete baseline days. Half-hourly temperature regressions produced baseline design peaks of 26.8, 23.5, 33.5 and 20.9 MW.

Applied compounded DFES growth, then qualifying connections in full. The growth register contained 58 rows: excluded 2 superseded, 8 withdrawn and 3 quoted records, then 14 records before the eligibility window and 3 after it. Retained 28 connections across all primaries, including 10 in the flexibility zones. CMZ additions were 2.3, 0.7, 0.9 and 1.2 MW respectively. Eligibility used actual energisation dates where available, otherwise planned dates, between 1 April 2026 and 31 October 2027. Every half-hour was scaled in proportion to the forecast peak, as required.

Estimated event delivery against a counterfactual using temperature and the primary's pre-service demand level. Fitted a temperature-dependent available-capacity ceiling, capped by scheduled MW, rather than assuming a constant delivered percentage. Model-family selection used chronological 2024/25 validation, before the final holdout: the chosen model's pooled miss was 0.13 MW, against 0.15 MW for a schedule-fraction model, 0.17 MW for a temperature-dependent efficiency model and 0.43 MW for a constant factor.

Applied estimated service delivery across the seven half-hours ending 16:30-19:30, and added the observed-pattern rebound through 21:30. Generated 10,000 predictive profiles per zone, resampling model fits and whole-day residual patterns, then took each profile's maximum. This preserves peak displacement and produces predictive P90s rather than confidence intervals for average demand.

Checked the method against directly observed held-out daily net peaks: 222 complete event days, 0.16 MW mean absolute error, and P90 coverage of 210/222 days, or 94.6%. For cold, capacity-binding events, coverage was 39/42, or 92.9%. Complete-weather-only, cancelled-day exclusion and earlier-winter temperature-slope sensitivities preserved the recommendation. Workbook formulas reconciled to the saved simulations and profiles; both files passed archive checks, and slide geometry/text-fit checks found no overflow.

Assumptions and judgment calls.

Final cancellations were treated as untreated baseline candidates. Excluding them instead does not change the recommendation.
Daily weather means retain days with missing hourly readings when 22-24 readings remain. Restricting the analysis to complete weather days does not change the recommendation.
Temperature response is extrapolated beyond the clean 2025/26 temperature range in Ashcombe, Fenwick and Hartwell. Using earlier-winter temperature slopes preserves the decisions.
Enlarged fleets are assumed to retain historical cold-weather availability and proportional delivery variability. This is material: at 75% fleet performance, Charlecote's P90 rises to 22.6 MW against 22.5 MW firm, with 16.0% exceedance. That scenario would reverse its deferral.
Predictive tails rely on 31, 30, 36 and 36 cold, capacity-binding historical events, not on the number of simulation draws. Structural fleet changes and all sources of serial dependence are not captured by the bootstrap. Ashcombe's cold held-out coverage was only 10/12, or 83.3%; this limitation strengthens caution but does not reverse its commitment decision.
These assumptions and sensitivities are in Method, Validation, Sensitivities and slide 5.

Alternatives rejected.

Deducting the entire contract: enrolled MW is not guaranteed delivered MW. Historical cold-event performance supports the lower delivery estimates shown above.
Using a constant historical delivery factor: its held-out miss was 0.46 MW, versus 0.13 MW for the selected approach.
Approving Fenwick on expected demand alone: its 30.3 MW expected peak is below 30.5 MW firm, but its 31.3 MW P90 fails the specified risk standard.
Ignoring peak displacement and rebound: Ashcombe's evening reference delivery does not remove its whole-day constraint. Even without rebound, its P90 remains 24.2 MW, above 23.0 MW firm.
Treating reliability or transformer condition as the deciding capacity evidence: these can justify separate investment, but do not replace the supplied thermal-capacity rule.
Files produced.

Halverton_Winter_2027-28.xlsx: decision dashboard, two native charts, contract-to-peak bridge, half-hourly profiles, backtest, sensitivities, source reconciliation, predictive draws and embedded analytical code.
Halverton_Capex_Review.pptx: five-slide capex review covering the recommendation, delivery bridge, Ashcombe peak displacement, validation and delivery-assurance risks.
Temporary analysis files and previews were removed. Existing workspace configuration was left untouched.

Packages installed. Installed numpy, pandas, scipy, statsmodels, openpyxl, XlsxWriter, python-pptx, PyMuPDF and matplotlib, with their dependencies, in an isolated Python environment because the active interpreter lacked the advertised analytics packages.
