# task9 architecture 8, platform run 2 (the text the author pasted on 2026-11-11, kept as given)

Reviewed 47 resources

Recommendation. Size the new 3-month ladder at USD 111,000 per point per monthly sale from January 19, 2027, retaining the USD 50,000-per-point 12-month ladder. Under the documented historical reconstruction, collateral determines the maximum on November 20, 2008: $44,624,000 against the $44,628,000 limit; the next USD 100 increment breaches it.

Final answers. Dollar amounts below are rounded to the nearest thousand. Positive settlements are receipts; negative settlements are payments. The maxima are conditional on the documented reconstruction of unpublished early volatility indices.

* 3-month maximum: USD 111,000 per point per monthly sale. Collateral binds on November 20, 2008, with $4,000 displayed headroom. At USD 111,100 per point, peak collateral becomes $44,641,000, exceeding the limit. The sleeve's worst annual net settlement is -$22,430,000 in 2008, within the $29,752,000 annual payment limit. These results appear on memo page 1 and the spreadsheet's `Sizing` sheet.
* 6-month alternative: USD 57,300 per point per monthly sale, replacing rather than accompanying the new 3-month ladder. Collateral also binds on November 20, 2008, at $44,604,000, leaving $24,000 displayed headroom. At USD 57,400 per point, peak collateral becomes $44,637,000, exceeding the limit. Its sleeve's worst annual net settlement is -$20,353,000 in 2020. See memo page 1 and `Sizing`.
* Historical 3-month economics, per USD 100,000 per point: average settlement $282,000 per sale; 80% range of that average $147,000 to $410,000; worst calendar year 2008, with -$16,389,000 net settlements. The average uses 235 expired sales. See memo page 1 and `Historical Summary`.
* Historical 6-month economics on the same basis: average settlement $286,000 per sale; 80% range $75,000 to $484,000; worst calendar year 2020, with -$18,416,000 net settlements. The average uses 232 expired sales. See the same locations.
* Historical 12-month average on the same basis: $315,000 per sale, with an 80% range of $69,000 to $539,000, using 226 expired sales. These are ranges for the average, not for an individual settlement. See memo page 1 and `Historical Summary`.
* 12-month peak collateral: $51,752,000 per USD 100,000 per point, on March 18, 2020. At the retained USD 50,000-per-point size, the peak is $25,876,000. See memo page 1 and `Decision`.

The open swaps expiring in 2027 are expected to settle for $2,487,000 in aggregate, with an 80% predictive range of $92,000 to $4,237,000. The following figures combine each pair of dealer tickets into its actual USD 50,000-per-point monthly cohort:

* January 15, 2027: $343,000; range $309,000 to $393,000.
* February 19, 2027: $359,000; range $284,000 to $435,000.
* March 19, 2027: $404,000; range $300,000 to $500,000.
* April 16, 2027: $306,000; range $157,000 to $434,000.
* May 21, 2027: $268,000; range $97,000 to $427,000.
* June 17, 2027: $249,000; range $65,000 to $436,000.
* July 16, 2027: $228,000; range $4,000 to $442,000.
* August 20, 2027: $158,000; range -$158,000 to $418,000.
* September 17, 2027: $90,000; range -$343,000 to $390,000.
* October 15, 2027: $80,000; range -$467,000 to $401,000.

These appear on memo page 2 and `Open 2027`. That sheet also provides each forecast normalized to USD 100,000 per point. At that normalization, the aggregate is $4,974,000, with range $183,000 to $8,474,000. Aggregate ranges are calculated jointly, not by adding individual endpoints.
The 2027 cash plan at the selected sizes is:

* Already-open 12-month swaps: $2,487,000; range $92,000 to $4,237,000.
* Not-yet-sold 12-month swaps expiring in 2027: $315,000; range -$1,081,000 to $1,116,000.
* Continuing 12-month ladder total: $2,802,000; range -$463,000 to $5,223,000.
* New 3-month ladder: $2,818,000; range -$1,367,000 to $8,046,000.
* Whole sleeve with the 3-month addition: $5,620,000; range -$3,412,000 to $12,064,000.
* New 6-month alternative: $982,000; range -$845,000 to $3,502,000.
* Whole sleeve with the 6-month alternative: $3,785,000; range -$2,823,000 to $8,291,000.

The cash plan is on memo page 2 and `2027 Cash Plan`; individual expiries and actual settlement dates are in `2027 Cash Schedule`. It includes nine new 3-month settlements or six new 6-month settlements. Collateral transfers and collateral interest are excluded.
Daily collateral: `daily_collateral.csv` contains 4,995 exchange-session rows, from January 3, 2007 through November 9, 2026, covering the retained ladder and both mutually exclusive sleeve alternatives. Collateral and headroom columns contain integer USD rounded to the nearest thousand. The spreadsheet's `Daily Collateral` sheet retains full precision behind its rounded display.

Step-by-step process.

1. Established the governing rules. Read the IPS Schedule D, master confirmation, CSA summary, indicative 2027 terms, and audited FY2026 net-assets statement from `input-assets/9.1.zip`. Audited assets of $1,487,600,000 establish the $29,752,000 settlement-payment limit and $44,628,000 collateral limit. The indicative terms allow only one additional ladder.
2. Reconstructed the existing book. Read `CFF_VolPremium_Blotter.xlsx`, the settlement CSV, all three dealer statements, daily dealer valuations, and the collateral ledger. From 130 blotter tickets, excluded one superseded erroneous ticket and one novated-out duplicate, retaining 128 economic tickets. The 64 actual monthly sales each total USD 50,000 per point. Of 24 live tickets, 20 tickets forming ten cohorts expire in 2027. The spreadsheet documents the retained positions and reconciliation results.
3. Prepared the market record. Read all eight market histories and the NYSE holiday file. Restricted the 13,073 SPX observations to the policy's 4,995-session record and aligned the volatility indices to those dates. No stress observations were removed or winsorized. SKEW and VVIX were inspected but not used: neither is a contractual input, and adding them to the selected models would introduce unnecessary fitting complexity.
4. Handled missing tenor histories explicitly. Reconstructed 683 early 3-month observations, affecting 32 sale dates, and 251 early 6-month observations, affecting 12 sales. The models regress the logarithm of the missing tenor on log VIX and an observed longer tenor. Observed quotes always take precedence. Filled six isolated one-year-index gaps using only the preceding session. Before VIX9D publication, used VIX as the short endpoint rather than inventing a VIX9D history. Coefficients, flags, and validation scores are in `Reconstruction` and `Market Inputs`.
5. Applied the contract calendar and settlement formula. Sales occur on the first exchange session after the third Friday; expiry occurs on the specified third Friday or preceding session. Historical observation dates come from SPX. Future dates use the supplied holiday calendar, retaining early-close sessions. Calculated annualized variance from squared daily log returns, used actual observation counts, and capped realized volatility at 2.5 times strike. Settlements are attributed to expiry year, even though cash moves two exchange business days later.
6. Validated the valuation basis. Removed eight exact duplicate daily valuation rows, leaving 28,804 unique marks. Normalized volatility and variance quotations and used exact blotter notionals rather than rounded statement units. Quoted inputs reproduce every unique dollar-rounded mark; all 104 actual settlements reconcile to cents. Three WXB dealer/day records are absent from the daily file despite ledger exposures; all other ledger exposures reconcile. Those missing dealer records were not used to manufacture historical collateral.
7. Built and sized the hypothetical ladders. Generated 238 monthly sales per tenor across the complete record. Daily marks blend accrued variance with remaining implied variance, with the contractual exposure cap applied before whole-sleeve netting. Tested every daily collateral observation and every calendar-year net settlement against the limits, retained the existing ladder, and rounded feasible sizes down to USD 100 increments. An exhaustive permitted-size grid confirmed both maxima and the failure of the next increment.
8. Estimated uncertainty in historical averages. Used 20,000 circular block-bootstrap resamples, with 12-month blocks and seed 20261109, to preserve dependence among overlapping monthly swaps. A 24-month-block sensitivity gives a 3-month mean range of $158,000 to $397,000 and a 12-month mean range of $61,000 to $555,000. These checks are stored separately from annual cash prediction ranges.
9. Built the joint 2027 cash forecast. Used 225 monthly historical origins, January 2007 through September 2025, with complete subsequent paths. For open swaps, combined actual accrued variance with remaining variance estimated from historical realized-to-implied ratios. For future sales, used the policy-required historical average. Reused each historical path across positions and ladders, then summed cash before calculating percentiles, preserving dependence.
10. Checked forecasting and deliverables. Forecast validation holds out an origin year and purges training outcomes overlapping its forward windows. Calibration improves variance-forecast RMSE at all ten horizons, but marginal predictive-band coverage is 74.7% to 78.7%, below the nominal 80%. Aggregate annual coverage is not independently established. Verified that the PDF opens as three pages, workbook formula caches agree with the CSV, dates and rounding reconcile, and the recommendation is identical across all three deliverables. Removed temporary analysis files.

Assumptions and judgment calls.

* Historical reconstruction affects the exact maximum. Early 3-month and 6-month quotes do not exist in the supplied published record. The reported sizes therefore depend on the calibrated reconstruction, which is clearly flagged rather than presented as observed data.
* No additional safety buffer is included. These answer the maximum-size question. The 3-month choice leaves only $4,000 of displayed collateral headroom.
* The inferred curve is a valuation convention, not a fully identified dealer model. Calendar-day total-variance interpolation best fits the supplied marks. The contractual cap is enforced, but near-cap option-value adjustments cannot be identified from the dealer sample.
* Forecast bands are conditional historical estimates. They assume historical normalized variance experience remains relevant. They do not establish guaranteed 80% future coverage or include uncertainty from every modeling choice.
* Policy collateral differs from operational postings. Whole-sleeve netting follows Schedule D; dealer-level flooring, transfer rounding, and collateral interest are not substituted for that measure.

Alternatives rejected.

* Omitting pre-publication sales: prohibited by policy. For the 3-month ladder, this shortcut would increase apparent capacity to USD 136,600 per point and move the apparent binding day to March 18, 2020.
* Uncalibrated tenor interpolation: would permit USD 112,300 per point for 3 months and USD 58,700 for 6 months. The calibrated main 3-month reconstruction has held-out RMSE of 0.552974 volatility points, versus 1.163326 for the uncalibrated bridge, supporting the selected lower capacities.
* Linear interpolation of annualized variance or volatility: dealer-quote RMSE is 0.316782 and 0.331101 volatility points, respectively, versus 0.146327 for total-variance interpolation.
* Treating mean uncertainty as annual cash risk: rejected because the cash plan concerns an actual year's settlements, not uncertainty in an average. The deliverables calculate and label these separately.
* Adding marginal forecast endpoints: rejected because open swaps and ladder settlements share market paths. Aggregate bands use joint scenario totals.
* Treating the 6-month alternative as invalid: it remains feasible at the stated size. It is an alternative implementation, not a second ladder to add alongside the 3-month recommendation.

Files produced. All files are under `/home/agent/workspace`.

* `ladder_decision_memo.pdf`: Three-page decision memo covering sizes, binding limits, historical economics, open settlements, cash plans, and material qualifications.
* `variance_ladder_analysis.xlsx`: Detailed calculations, historical trades, daily and annual limits, forecasts, scenarios, bootstrap results, source inventory, and reconciliation evidence.
* `daily_collateral.csv`: Rounded daily collateral and headroom for all 4,995 record sessions under both alternatives.

Packages installed. Installed `pypdf`, `reportlab`, and `xlsxwriter`. Because the runtime did not expose the advertised analytics packages, also installed `numpy`, `pandas`, `scipy`, `openpyxl`, `python-docx`, and `matplotlib` in an isolated temporary environment.
