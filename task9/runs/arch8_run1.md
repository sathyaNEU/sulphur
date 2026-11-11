# task9 architecture 8, platform run 1 (the text the author pasted on 2026-11-11, kept as given)

Reviewed 49 resources

Recommendation. Use USD 111,500 per point per monthly sale for the new 3-month ladder from January 19, 2027, as the modeled policy maximum; retain the 12-month ladder at USD 50,000 per point.
The mutually exclusive 6-month alternative is USD 57,500 per point. Both bind on daily collateral on November 20, 2008, against the USD 44,628,000 limit. These maxima depend on the disclosed reconstruction of missing index history and estimated dealer valuation basis.

Final answers. Dollar amounts below are rounded to the nearest USD 1,000; ladder sizes are exact USD 100 multiples. Positive settlement amounts are receipts.
The memo is `Volatility_Ladder_Memo.pdf`; the workbook is `Volatility_Ladder_Analysis.xlsx`.

* 3-month maximum: USD 111,500 per point per monthly sale. Peak combined-sleeve collateral is USD 44,614,000, leaving USD 14,000 headroom. Increasing the size to USD 111,600 produces USD 44,631,000 collateral and fails. Its worst combined settlement year is 2008: −USD 22,453,000, within the USD 29,752,000 annual payment limit. Location: memo page 1; workbook `Decision`, `Sizing` and `Annual Limits`.
* 6-month alternative: USD 57,500 per point per monthly sale. Peak combined-sleeve collateral is USD 44,600,000, leaving USD 28,000 headroom. Increasing the size to USD 57,600 produces USD 44,633,000 collateral and fails. Its worst combined settlement year is 2020: −USD 20,390,000. Location: the same sections.
* 3-month historical economics, per USD 100,000 per point: Average settlement per sale is USD 281,000, with an 80% range of USD 146,000 to USD 409,000 for the average. The worst calendar year is 2008: −USD 16,336,000. The average uses 235 matured sales. Location: memo page 1; workbook `Decision`, `Mean Ranges` and `Annual Limits`.
* 6-month historical economics, on the same basis: Average settlement is USD 288,000, with an 80% range of USD 73,000 to USD 483,000 for the average. The worst calendar year is 2020: −USD 18,416,000. The average uses 232 matured sales. Location: the same sections.
* 12-month historical average, per USD 100,000 per point: USD 315,000, with an 80% range of USD 73,000 to USD 539,000, using 226 matured sales. Location: memo page 1; workbook `Decision` and `Mean Ranges`.
* 12-month peak collateral: USD 51,754,000 per USD 100,000 per point, on March 18, 2020. At the continuing USD 50,000 size, that is USD 25,877,000. Standalone ladder peaks are not added when testing the sleeve. Location: memo page 1; workbook `Decision` and `Daily Collateral`.

The open swaps expiring in 2027 are expected to settle at USD 2,618,000 in aggregate, with an 80% predictive range of USD 738,000 to USD 4,249,000. These are 20 dealer tickets representing 10 monthly cohorts, each totaling USD 50,000 per point.
Their cohort estimates are below. Location: memo page 2; workbook `Open Forecast`, with individual dealer tickets in `Open Tickets`.

* January 15, 2027: USD 347,000; range USD 306,000 to USD 396,000.
* February 19, 2027: USD 365,000; range USD 295,000 to USD 437,000.
* March 19, 2027: USD 413,000; range USD 316,000 to USD 501,000.
* April 16, 2027: USD 318,000; range USD 182,000 to USD 438,000.
* May 21, 2027: USD 283,000; range USD 123,000 to USD 432,000.
* June 17, 2027: USD 264,000; range USD 87,000 to USD 439,000.
* July 16, 2027: USD 244,000; range USD 45,000 to USD 444,000.
* August 20, 2027: USD 176,000; range −USD 85,000 to USD 420,000.
* September 17, 2027: USD 110,000; range −USD 220,000 to USD 392,000.
* October 15, 2027: USD 100,000; range −USD 264,000 to USD 404,000.

Aggregate expectations are calculated before rounding. Aggregate range endpoints are calculated jointly, not by adding individual endpoints.
The 2027 cash plan at the proposed sizes is as follows. Location: memo page 2; workbook `Cash Plan`, `Future Sales` and `Cash Scenarios`.

* Continuing 12-month ladder: Expected receipts USD 2,933,000; 80% predictive range USD 121,000 to USD 5,094,000.
* New 3-month ladder: Expected receipts USD 2,824,000; range −USD 982,000 to USD 6,419,000.
* Sleeve with the 3-month ladder: Expected receipts USD 5,757,000; range USD 153,000 to USD 10,976,000.
* Alternative 6-month ladder: Expected receipts USD 992,000; range −USD 841,000 to USD 2,788,000.
* Sleeve with the 6-month ladder: Expected receipts USD 3,925,000; range −USD 405,000 to USD 7,520,000.

The continuing ladder includes USD 315,000 expected from the two not-yet-sold November/December 2026 trades expiring in 2027. The new 3-month ladder contributes 9 expiries, April-December; the 6-month alternative contributes 6 expiries, July-December. Both begin selling on January 19, 2027, with first expiries on April 16 and July 16, respectively.
`Volatility_Ladder_Daily_Collateral.csv` contains all 4,995 published SPX closing dates, including zero-collateral days, for both mutually exclusive sleeve alternatives. Dollar columns are rounded to USD 1,000; sizes and the policy limit are identified explicitly. The workbook's `Daily Collateral` sheet retains unrounded calculations.

Step-by-step process.

1. Read all 21 archive members. The policy, master confirmation, CSA summary, audited assets, indicative terms and three dealer statements established the governing rules and controls. The blotter and settlements established positions and economics. Dealer valuations and the collateral ledger established marking and custody conventions. The eight market histories supplied prices and diagnostic variables; the NYSE holiday file supplied future closures. The workbook's `Sources` sheet records each filename and its role.
2. Establish policy capacity and dates. Audited Reference Assets are USD 1,487,600,000, producing the USD 29,752,000 settlement limit and USD 44,628,000 collateral limit. The review close is November 9, 2026. Historical business days follow published SPX closes; future business days exclude supplied full closures but retain early closes.
3. Resolve actual positions. Removed one superseded ticket containing the USD 250,000 notional error and retained its USD 25,000 correction. Counted the novation once economically. This leaves 129 lifecycle references, 128 economic tickets and 64 monthly cohorts, each totaling USD 50,000 per point. Of 24 live tickets, 20 expire in 2027 and four in 2026.
4. Prepare the policy market record. Retained 4,995 policy-period SPX rows from 13,073 supplied rows. Reconstructed 683 VIX3M, 251 VIX6M and 1,009 VIX9D missing closes using contemporaneous log-ratio term-structure models. Filled six isolated VIX1Y gaps by interpolating its log spread to VIX. No SPX observations were imputed and no crisis returns were trimmed. This retained 32 reconstructed 3-month sale strikes and 12 reconstructed 6-month sale strikes rather than deleting those sales.
5. Identify and validate valuation arithmetic. Removed eight exact duplicate dealer rows, leaving 28,804. Every remaining mark reconciles to the dollar using reported quote precision and full-precision variance units. All 104 actual settlements reconcile to cents. The market-to-quote model uses calendar-day total-variance interpolation; later-date holdout error is 0.129015 volatility points and USD 1,880.08 per position. Missing WXB transaction detail on three dates was not treated as zero exposure.
6. Simulate the entire policy program. Generated 238 monthly sales for each tenor and 102,201 open-swap daily valuation rows. Applied the realized-volatility cap to each transaction, then netted all open sleeve marks before taking collateral's adverse amount. Annual settlements were attributed to expiry year. Solved every daily and annual marginal size ceiling, applied the dealer quote ceiling, and rounded the tightest result down to USD 100. The next increment fails for both alternatives.
7. Estimate uncertainty in historical averages. Used 50,000 circular moving-block bootstrap samples, with 12-month blocks to preserve overlapping-trade dependence. Tested 6- and 24-month blocks. These ranges concern the average settlement, not an individual sale or a future calendar year.
8. Build coherent cash forecasts. Used 4,717 historical forward paths, preserving known accrued variance on open swaps. A common positive volatility scale applies to every future SPX return and future strike within each path. Positive, minimum-relative-entropy probabilities match all 17 unsold-sale policy means without shifting payoffs beyond contractual bounds. Expectations and predictive percentiles use the same joint scenarios.
9. Validate and reconcile outputs. Checked zero cap violations and zero negative future variance increments, and matched the policy means within USD 0.01. Tested chronological forecast diagnostics and sparser historical-start samples. Independently reconciled the memo, workbook and CSV. The final PDF has three pages; the workbook has 25 sheets, no error cells and no external workbook links; all 4,995 CSV rows reconcile.

Assumptions and judgment calls.

* Historical reconstruction is unavoidable. The policy requires sales before several indices were published. The resulting maximum is conditional on the stated reconstruction, not an exact recovery of unavailable published quotes.
* Dealer marking uses an equal-panel estimated basis. Actual allocation and quote variation can change the maximum by more than one USD 100 increment.
* No execution buffer is deducted. The request was for maximum modeled capacity. A 10% upward shock to missing early indices reduces capacity to USD 107,600 for 3-month and USD 55,200 for 6-month. A 0.25-point dealer quote overlay reduces it to USD 110,500 and USD 57,000. Both checks retain the same binding limit and date.
* Future paths use six-month volatility as their common conditioning level. This preserves coherent shared returns but assumes a persistent volatility scale. The forecast is not a dealer mark or a guarantee of future receipts.
* Ranges exclude some model uncertainty. Parameter, reconstruction and future-regime uncertainty are not included. Overlapping historical paths are not independent years.
* The positive 3-month lower endpoint is not robust assurance. Using every 21st historical start changes it from USD 153,000 to −USD 170,000, as disclosed in the memo and `Predictive Sensitivity`.
* Cash plan means settlement cash only. Collateral movements and collateral interest are excluded. Later sales expiring in 2028 do not contribute to 2027 settlements.

Alternatives rejected.

* Using only the sleeve's live history or dropping unpublished-index years: This conflicts with the full-record requirement and omits the November 20, 2008 binding event.
* Using the USD 200,000 quoted size: Both modeled policy maxima are lower; even the next USD 100 increment above each maximum breaches collateral.
* Treating annual settlement payments as binding: The 3-month and 6-month cases retain USD 7,299,000 and USD 9,362,000 of annual payment capacity, respectively.
* Using summed dealer postings: That is not global policy netting. On March 11, 2025, dealer postings total USD 150,000 while policy net collateral is zero.
* Interpolating volatility directly: Its holdout quote error is 0.274628 volatility points, versus 0.129015 for calendar total-variance interpolation.
* Using dealer marks as expected settlements, or adding marginal interval endpoints: Those approaches confuse replacement value with physical settlement expectations or ignore shared SPX exposure.
* Treating the 6-month ladder as an additional position: It is a valid substitute, not a second new ladder. The indicative terms provide for one new ladder.

Files produced. All are saved under `/home/agent/workspace`.

* `Volatility_Ladder_Memo.pdf`: Three-page decision memo covering capacity, historical economics, open settlements, cash plans and material model risks.
* `Volatility_Ladder_Analysis.xlsx`: Auditable calculations, full daily valuation trail, source inventory, forecasts, calibration and sensitivity checks.
* `Volatility_Ladder_Daily_Collateral.csv`: Daily collateral for both sleeve alternatives across the complete published-close record.

Packages installed. Installed in a `uv`-managed environment: NumPy, pandas, SciPy, openpyxl, XlsxWriter, ReportLab and PyMuPDF, with dependencies.
