# task20 architecture 4, platform run 1 (pasted by the author, 2026-11-13; score not reported)

Reviewed 44 resources
Recommendation. Reject the USD 500M plan and cap 2027 new private-fund commitments at USD 250M under the policy stress.

USD 250M leaves USD 4.02M above the USD 1,200.00M minimum reserve. The USD 500M plan leaves a USD 131.23M shortfall. The passing ceiling is conditional on the fitted capital-call estimates, not a guarantee against forecast error.

Final answers. All amounts below are USD million.

Largest passing 2027 commitment: 250.00. The continuous mathematical ceiling is 257.42, rounded down to the policy's USD 25M increments. At 250.00, net cash needs are 933.39, reserve remaining is 1,204.02, and headroom is 4.02. The next increment, 275.00, fails with headroom of -9.51. These results appear in Wexmoor_2027_Liquidity.xlsx, Decision, and the memo's first-page approval table.
At the USD 500M plan: 2027 net cash needs are 502.58, leaving year-end headroom of 434.83. Additional 2028 net cash needs are 566.06. Combined 2027-2028 needs are 1,068.64, leaving reserve of 1,068.77 and final headroom of -131.23. Headroom is cumulative from January 2027, not reset annually. See workbook Cash Flow and memo page 1, USD 500M Plan: Policy Cash Needs.
For commitments made by the end of 2026, stressed capital calls are:

2027 H1: first close held 521.76; first close pending 0.00; total 521.76.
2027 H2: first close held 224.92; first close pending 0.00; total 224.92.
2028 H1: first close held 219.92; first close pending 65.00; total 284.92.
2028 H2: first close held 156.88; first close pending 87.52; total 244.40.
Eight-quarter totals: first close held 1,123.49; first close pending 152.51; total 1,276.00.
These appear in workbook Cash Flow, with fund-level detail in Existing Calls, and memo page 2, Stressed Capital Calls and Distributions. Group membership is fixed at 31 December 2026.

Distributions on those existing commitments under the same policy stress are:

2027 H1: 402.80
2027 H2: 280.18
2028 H1: 169.51
2028 H2: 198.36
Total: 1,050.86
See workbook Cash Flow, Distribution Rates, and Fund Distributions, and the same memo page 2 table.

Commitments not yet called at 31 December 2026, by strategy, are:

Buyout: 1,918.16
Growth equity: 433.39
Venture capital: 186.04
Real estate: 288.06
Infrastructure: 840.79
Private credit: 524.55
Total: 4,191.00
See workbook Commitments, including the complete fund-level reconciliation, and memo page 2, Uncalled at 31 December 2026.

Displayed components can differ from displayed totals because calculations retain full precision.

Step-by-step process.

Established the controlling rules. Read wexmoor_endowment_liquidity_policy_2025.pdf, wexmoor_investment_policy_statement_2024.pdf, and wexmoor_university_capital_plan_FY2027_FY2031.pdf. Applied the eight-quarter liquidity test, specified market stress, reserve classifications, minimum reserve, and commitment increments. The capital plan requires no additional endowment draw; the university's separate operating liquidity is excluded.

Reconciled the commitment population. Read private_commitment_register_2026-12-31.xlsx, capital_account_statements_2013Q1_2026Q4.csv, and custodian_cash_activity_2026Q4.csv. The register contains 98 commitments: 73 active closed funds, 4 pending funds, and 21 expired funds. Removed one superseded Tilsworth VI statement, reducing 2,303 statement rows to 2,302. Canonicalized manager names by fund ID, correcting aliases on 78 retained rows across 5 funds. Reviewed all 107 custodian movements, using them only where statements were missing.

Reconstructed missing year-end balances. Ardley V and Marrable V lacked fourth-quarter statements. Their September NAVs plus custodian calls less distributions produce December NAVs of 48.78 and 9.72, respectively; their uncalled balances are 87.84 and 193.34. Total fixed opening private NAV is 3,986.27. Original commitments of 9,709.00 reconcile to cumulative calls of 5,128.69, term-end releases of 389.31, and remaining uncalled commitments of 4,191.00.

Applied consistent units and data controls. Converted statement and custodian USD amounts to millions and audited USD-thousand amounts to millions. Used calendar-quarter keys and retained actual audit fiscal dates. There were no missing numeric statement cash-flow, NAV, or uncalled fields, no exact duplicate portfolio records, and no duplicate custodian rows. Retained 33 negative historical statement NAVs and 808 negative benchmark NAVs rather than clipping source values. All cutoff fund NAVs are nonnegative, and all distribution-rate denominators are positive. Missing pending-fund sizes and contractual dates were handled with normalized forecasts rather than invented fund sizes.

Estimated manager capital calls. Read manager_portfolio_activity_2013_2026.csv, fund_audited_financials_FY2013_FY2026.xlsx, and market_series_quarterly_2000Q1_2026Q4.csv: 21,568 portfolio records, 531 audited fund-years, and 108 market quarters. Separated deployment, follow-ons, support investments, recycling, fees, expenses, and borrowing-line settlements. The stressed short rate is 5.25%, which causes 239.40 of opening LP-equivalent borrowing to enter first-quarter calls. Calls respect remaining commitment limits; unused commitments are released at term end.

Calculated prescribed distributions separately. Read all 69,675 rows of industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv. The policy window contains 3,831 rows from 2008Q2 through 2010Q2, supporting 48 strategy-quarter rates. Each rate is summed distributions divided by summed prior-quarter NAV, multiplied by fixed Wexmoor opening NAV. Modeled portfolio-sale proceeds were used only for recycling, not substituted for policy distributions.

Calculated liquid resources and spending. Read liquid_holdings_2026-12-31.xlsx and spending_distributions_FY2014_FY2027.csv. Retained 18 holdings, excluding only a blank row and a reporting note. Eligible reserve is 2,137.41: cash/Treasuries 499.70, investment-grade bonds 345.15, public equities 966.49, and redeemable hedge funds 326.07. Locked hedge funds and other holdings contribute zero. From the spending file's 14 fiscal years, used approved FY2027 spending of 286.50 annually, or 71.625 quarterly, throughout the test.

Scaled the proposed programme and solved the boundary. Read corrigan_hart_pacing_plan_2027.xlsx; allocated the tested budget across Oakhanger, Wendlebury, Corvane, Ewelme, and Harpsden in proportions of 30%, 20%, 9%, 14%, and 27%. The resulting eight-quarter new-call coefficient is 0.541002 per dollar committed. Existing-book net needs before new commitments are 798.14, versus permissible net needs of 937.41. Solving that relationship and rounding down produces the 250.00 ceiling. Reviewed the 24 peers in peer_endowment_survey_2025.xlsx, but did not use peer ratios to override Wexmoor's policy.

Validated the forecast and tested alternatives. Calibrated through 2022Q4 and forecast 2023-2024 for 70 commitments, covering 560 fund-quarter comparisons, without feeding future portfolio activity into predictions. Actual calls were 896.24, versus 884.91 predicted. Aggregate-quarter weighted absolute percentage error was 6.54%, compared with 8.21% for an internally fitted fixed age curve; aggregate bias was -1.26%. Separately, conditional accounting reconstruction had USD 8.15 call mean absolute error and USD 50.66 fund-level borrowing mean absolute error. These reconciliation results are not forecast precision.

Verified the artifacts. Checked fund-level rollforwards, call-component identities, pacing weights, the passing/failing budget boundary, and all spreadsheet formulas against independently evaluated results. Reproduced the forecasts from the workbook's embedded engine. Confirmed that both files open, the PDF contains all requested answers, and its three-page layout has no text outside page bounds. Removed the temporary build script.

Assumptions and judgment calls.

Expected calls determine the formal ceiling. The policy specifies estimated calls, not a statistical confidence threshold. I therefore used the fitted expected-call forecast without silently adding a discretionary buffer.
First-close timing is estimated, not assumed certain. The four pending commitments total 667.00 and remain included in full. Market-conditioned delays move their expected calls into 2028. Adjacent-quarter timing preserves estimated mean delays but does not represent every possible closing outcome.
Some recycling and exit parameters are uncertain. Weakly identified recycling fractions are pooled, and the model projects expected company cohorts rather than complete joint simulation paths. Support during the deepest stress extrapolates beyond the historical range.
Benchmark percentages are used consistently. Benchmark fund sizes are unavailable, so the calculation uses the supplied normalized commitment units rather than inventing dollar weights.
Only the 2027 budget is tested. The separate 2028 commitment programme is excluded, and approved FY2027 spending is held fixed as required.
The ceiling is model-sensitive. Across 13 one-at-a-time cases, passing budgets range from 25.00 to 400.00. USD 500M fails every case, but USD 250M is not robust to every higher-call alternative. These cases are sensitivities, not confidence intervals.
Alternatives rejected.

Approve USD 500M: rejected because its final reserve is 1,068.77, below the 1,200.00 minimum by 131.23.
Round the ceiling up to USD 275M: rejected because that budget fails by 9.51.
Use a fixed age call curve: rejected as the main estimate because its aggregate-quarter error is 8.21%, versus 6.54% for the structural model, and it misses borrowing-line and closing-timing effects.
Assume every pending fund closes on schedule: retained as a sensitivity, not the central forecast. It reduces the passing budget to 25.00.
Use modeled asset sales as policy distributions: rejected because the policy explicitly prescribes benchmark rates applied to fixed opening NAV.
Treat USD 250M as a guaranteed safe budget: rejected. Its 4.02 cushion is narrow, and higher-call sensitivity cases fail at that amount. This is the principal evidence against treating the central estimate as robust.
Files produced. Saved under /home/agent/workspace:

Wexmoor_2027_Liquidity.xlsx: formula-driven policy test, detailed forecasts and reconciliations, validation, sensitivities, source data, and embedded runnable capital-call model.
Wexmoor_2027_Liquidity_Memo.pdf: three-page Investment Committee memo containing the recommendation and every requested numerical result.
Packages installed. The advertised analytics packages were absent from the runtime. Installed NumPy, pandas, SciPy, statsmodels, scikit-learn, openpyxl, XlsxWriter, PyMuPDF, ReportLab, and Matplotlib, with their dependencies, in a temporary virtual environment.
