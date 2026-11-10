Response 2
Reviewed 73 resources· 21m
Recommendation. Commit Ashcombe Road reinforcement in December 2026 for winter 2027/28; do not commit Charlecote Way, Fenwick Street or Hartwell Common on the design-day capacity criterion.
Ashcombe’s demand after flexibility is 23.77 MW against 23.00 MW firm, leaving a 0.77 MW shortfall at the specified -3 C daily-mean design condition.
Final answers. The zone-by-zone design-day results are:

* Ashcombe Road CMZ: credit 6.33 MW flexibility. Demand falls from 30.11 MW to 23.77 MW, against 23.00 MW firm. Reinforce for a 0.77 MW design-day shortfall.
* Charlecote Way CMZ: credit 3.94 MW. Demand falls from 25.02 MW to 21.08 MW, against 22.50 MW firm, leaving 1.42 MW headroom. No design-day commitment.
* Fenwick Street CMZ: credit 10.50 MW. Demand falls from 36.01 MW to 25.52 MW, against 30.50 MW firm, leaving 4.98 MW headroom. No design-day commitment.
* Hartwell Common CMZ: credit 5.45 MW. Demand falls from 22.91 MW to 17.47 MW, against 17.80 MW firm, leaving 0.33 MW headroom. No design-day commitment, but monitor this narrow margin.

These results are in `Halverton_Winter_2027-28_Capacity.xlsx`, sheet `Decision`, rows 11-14, and slide 1 of `Halverton_Winter_2027-28_Capex_Review.pptx`. Calculations use unrounded values, so subtracting displayed figures can differ slightly.
On a working weekday with a daily mean of -6 C, with flexibility recalculated for that temperature:

* Ashcombe Road exceeds firm: 5.28 MW flexibility credit; 26.65 MW net demand against 23.00 MW firm, an excess of 3.65 MW.
* Charlecote Way exceeds firm: 3.16 MW credit; 22.93 MW net demand against 22.50 MW firm, an excess of 0.43 MW.
* Fenwick Street remains below firm: 9.23 MW credit; 28.79 MW net demand against 30.50 MW firm, leaving 1.71 MW headroom.
* Hartwell Common exceeds firm: 4.61 MW credit; 19.89 MW net demand against 17.80 MW firm, an excess of 2.09 MW.

The stress results are in `Cold Stress`, rows 8-11, and slide 4. Charlecote’s stress breach is marginal: its 95% estimated-mean interval of 22.47-23.32 MW crosses its 22.50 MW firm threshold.
The spreadsheet contains an editable before-and-after chart against firm capacity on `Decision`; slide 2 presents the same comparison. The six-slide deck covers the commitment, flexibility credit, cold-stress exposure, validation and delivery actions.
Step-by-step process.

1. Established the governing rule and scope. Read `capacity_assessment_guideline_2026.pdf` and `flexibility_contract_awards_2027-28.pdf`. The guideline sets the commitment threshold at net design-day demand exceeding firm capacity at -3 C, and requires primary-side flexibility delivery in the half-hours ending 17:30 and 18:00. The award notice identifies the four CMZs and their future contracts. Firm capacity comes directly from Appendix A; no second power-factor adjustment was applied.
2. Resolved SCADA identifiers and quality. Read `primary_demand_halfhourly_2023-2026.csv` and `primary_substation_register.xlsx`. Mapped both historical and current SCADA identifiers to primary assets. From 196,201 demand rows, removed 441 exact duplicates, then excluded 931 S-quality and 31 B-quality readings, retaining 194,798 G-quality records. There were no unmapped identifiers or remaining asset/timestamp duplicates. Midnight interval ends were assigned to the preceding service day. The analytical data contain 4,086 November-March primary-days; 27 terminal April edge rows were excluded from model populations.
3. Prepared GMT daily temperatures. Read `halverton_weather_hourly_2023-2026.csv`. Selected the latest version at each station/timestamp, reducing 13,372 records to 13,062 hours. Of 547 dates, 488 had complete hourly coverage; 52 had 23 hours and 7 had 22 hours. The 59 incomplete days were excluded from the primary models without imputation. The coldest observed daily mean was -5.779 C.
4. Resolved dispatch revisions. Read `flexibility_events_2024-2026.csv`. Its 372 rows resolve to 336 final instructions after removing superseded revisions: 321 Completed and 15 Cancelled. Completed final scheduled MW supplies model exposure; final cancellations all carry zero MW. Primary/date joins avoid inconsistent provider-name spellings.
5. Constructed the baseline population. Used working weekdays from November through March, excluding weekends, 24 December-2 January, and applicable England/Wales bank holidays. There were 298 eligible calendar dates across the three winters before weather filtering and 260 afterward. The design-demand baseline uses only unscheduled 2025/26 days with complete weather and 48 good half-hours. Retained baseline samples were 41 Ashcombe, 55 Charlecote, 44 Fenwick and 42 Hartwell days. `Demand Build` records each exclusion stage.
6. Allocated eligible connection growth. Read `load_growth_register_2026-27.xlsx` and the 63 feeder records in `network_feeders_11kv.xlsx`, resolving five legacy circuit identifiers. Of 58 connection rows, included 28, totaling 10.170 MW across all primaries. Excluded 2 Superseded, 8 Withdrawn, 3 Quoted, 14 earlier-than-window and 3 later-than-window records. Used actual energisation where available, otherwise planned energisation, within 1 April 2026-31 October 2027 inclusive. The four CMZs contain 10 included connections totaling 5.130 MW: 2.300 MW Ashcombe, 0.710 MW Charlecote, 0.930 MW Fenwick and 1.190 MW Hartwell.
7. Forecast gross design demand. Fitted each primary’s daily maximum MW against daily mean temperature using its eligible baseline days. Compounded the two DFES annual growth rates, then added qualifying connections in full. Two-year growth factors were 1.044483, 1.030224, 1.036323 and 1.040399, respectively. This produces the gross design-day demands reported above. Baseline fit R-squared values were 0.99159, 0.96805, 0.99025 and 0.99292.
8. Estimated temperature-dependent flexibility. Fitted separate primary/half-hour regressions using temperature, winter effects, weekday effects, within-winter trend, scheduled MW and its temperature interaction. The model estimates primary-demand reduction per scheduled MW, rather than treating contracted MW as delivered relief. The four zones provide 1,040 potential observations per critical half-hour; missing or rejected interval readings leave 1,033 observations at 17:30 and 1,032 at 18:00. Applied the lower of the two expected delivery factors to each future award.
9. Challenged the result. Tested alternative weather specifications, untreated-primary controls, pre-service demand controls, cancellations, quality rules, half-hour averaging, removal of each winter and removal of a cold spell. All weather-aware alternatives preserve the Ashcombe-only commitment and the same three stress breaches. Five-fold blocked validation gives baseline errors of 0.142, 0.145, 0.162 and 0.098 MW; critical-interval errors range from 0.126-0.217 MW. All eight pre-service placebo confidence intervals include zero.
10. Quantified uncertainty and checked the artifacts. Used 1,000 joint calendar-week bootstrap draws, stratified by winter. Ashcombe’s design-day estimated-mean interval is 23.39-24.09 MW, entirely above firm. Hartwell’s is 17.22-17.76 MW, close to its firm limit. An independent audit reproduced the calculations and verified all 120 workbook formulas against cached results. Both Office files passed archive and reopening checks. The slide layout proof was inspected using a substitute font; native Excel/PowerPoint rendering was not available.

Also reviewed `primary_transformer_condition_2026.xlsx`, `customer_interruptions_2025-26.xlsx` and `duos_charging_statement_2027-28.pdf`. They contain transformer condition, feeder reliability and tariff information respectively, but do not determine the specified capacity decision. The network open-point records were reviewed without assuming unproven transfer relief. Every source’s role is documented in `Read Me`.
Assumptions and judgment calls.

* Two-half-hour credit: The guideline names both intervals without specifying a single aggregation rule. I used the lower expected reduction so credit supports both intervals. Averaging them does not change the recommendation.
* Observational estimation: Dispatch targets forecast demand above 95% of firm capacity, so events are not random. Weather/calendar controls, control-primary sensitivities and placebo tests support the estimate, but do not establish a guaranteed causal effect.
* Baseline extrapolation: The coldest eligible baseline temperatures are -0.083 C, 2.579 C, 2.746 C and 2.875 C, respectively. Even the design-day baseline therefore requires extrapolation. Alternative baseline specifications preserve the decision.
* Future portfolio scaling: Future awards are 1.46x, 1.78x, 2.15x and 2.50x historical maximum schedules. Applying historical delivery factors assumes enlarged portfolios retain comparable performance. This requires DSO confirmation, especially at Hartwell.
* Cold-weather evidence: Only seven distinct completed-event dates have daily means at or below -3 C. The -6 C case extrapolates beyond observed daily means. Its uncertainty is explicitly disclosed.
* Commitment versus stress readiness: The guideline’s point-estimate -3 C rule determines commitment. The -6 C result informs contingency planning, not an automatic additional capital commitment.
* Engineering scope: Ashcombe’s 0.77 MW is additional firm capability required by this assessment, not a transformer nameplate rating. No scheme costs or construction design were supplied, so none were invented.

Alternatives rejected.

* Credit the full contract awards: The measured design-hour response supports only 6.33 MW at Ashcombe against a 9.50 MW award. Headline contract capacity is not the stipulated credit measure.
* Use temperature-invariant delivery: That model would put Ashcombe at 21.62 MW and defer reinforcement. It is rejected because every critical-interval temperature interaction is significant at p < 0.001.
* Compare raw event and non-event averages: Dispatch selects higher-demand conditions. Those averages confound flexibility with weather and scheduling.
* Reinforce every stress-breach primary now: This substitutes the colder stress condition for the specified design criterion. Charlecote and Hartwell remain below firm at -3 C.
* Assume spare network-transfer capacity: The feeder and open-point registers do not establish deliverable firm transfer headroom.
* Treat the deferrals as risk-free: Hartwell retains only 0.33 MW design headroom, while Charlecote’s stress uncertainty interval crosses firm. These require monitoring and contingency measures, although they do not change the prescribed commitment decision.

Files produced.

* `Halverton_Winter_2027-28_Capacity.xlsx`: Fourteen-sheet workbook with formula-linked decisions, editable chart, stress results, source audits, model inputs, coefficients and validation.
* `Halverton_Winter_2027-28_Capex_Review.pptx`: Six-slide capex review with the recommendation, zone results, evidence, limitations and delivery actions.

Both files are saved under `/home/agent/workspace`. Temporary analysis scripts and previews were removed.
Packages installed. The advertised analytics packages were unavailable in the active runtime. Installed NumPy, SciPy, pandas, statsmodels, openpyxl, python-pptx, PyMuPDF, Matplotlib and Pillow, with dependencies, into the temporary runtime. XlsxWriter was also installed and used for the spreadsheet’s cached formulas and editable chart.
