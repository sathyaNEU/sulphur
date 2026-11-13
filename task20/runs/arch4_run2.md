# task20 architecture 4, platform run 2 (pasted by the author, 2026-11-13; score not reported; the paste ends after the validation step)

Reviewed 55 resources
Recommendation. Reject the USD 500M plan and pause new 2027 commitments; no nonnegative budget passes the central policy test.

At USD 500M, the estimated ending reserve is USD 924.28M, below the USD 1,200.00M minimum by USD 275.72M. Even zero new commitments leaves a USD 3.68M shortfall. The rejection of USD 500M survives every reported sensitivity; whether a small budget could pass is model-sensitive.

Final answers. All amounts below are USD million. Totals are calculated before rounding.

Largest passing 2027 total: none feasible in the central estimate. Zero commitments is not a passing maximum: it leaves USD 1,196.32M against the USD 1,200.00M minimum. The negative algebraic ceiling, USD -6.76M, cannot be rounded into an approvable budget. This appears in Wexmoor_2027_Liquidity.xlsx, Decision and Budget_Grid, and on page 1 of Wexmoor_2027_Memo.pdf.
At USD 500M, 2027 net cash needs are USD 590.47M. The cumulative year-end reserve is USD 1,546.94M, leaving USD 346.94M above the minimum.
At USD 500M, 2028 incremental net cash needs are USD 622.66M. The cumulative ending reserve falls to USD 924.28M, leaving negative headroom of USD -275.72M.
Combined 2027-2028 net cash needs are USD 1,213.13M, comprising USD 573.00M spending plus USD 1,690.99M calls less USD 1,050.86M fund distributions. These results appear in Decision and Quarterly, and the memo's page 1 policy-test table.
For commitments made by 31 December 2026, the stressed half-year schedule is:

2027 H1: calls from funds that have held a first close 515.27; calls from funds yet to close 0.00; total calls 515.27; distributions 402.80.
2027 H2: first-close-held calls 224.87; yet-to-close calls 92.83; total calls 317.70; distributions 280.18.
2028 H1: first-close-held calls 234.12; yet-to-close calls 92.26; total calls 326.38; distributions 169.51.
2028 H2: first-close-held calls 173.43; yet-to-close calls 86.16; total calls 259.59; distributions 198.36.
Eight-quarter totals: first-close-held calls 1,147.69; yet-to-close calls 271.25; all existing-commitment calls 1,418.95; distributions 1,050.86.
These figures appear in the workbook's Half_Year sheet and the memo's page 1 existing-commitment table. Cohort classification is fixed at 31 December 2026.

Commitments not yet called at 31 December 2026 are:

Buyout: 1,918.16.
Growth equity: 433.39.
Venture capital: 186.04.
Real estate: 288.06.
Infrastructure: 840.79.
Private credit: 524.55.
Total: 4,191.00.
These appear in Unfunded, with fund-level reconciliation in Opening, and in the memo's page 1 strategy table.

Step-by-step process.

Established the governing rules. Inspected all 14 files in 20.1.zip. The liquidity-policy PDF governs the eight-quarter horizon, USD 25M budget increments, reserve factors and prescribed distributions. The investment-policy statement provides context but does not override fixed approved spending. The university capital plan explicitly requires no additional endowment draw. The peer survey was reviewed but not used to replace Wexmoor's policy or manager evidence.

Reconciled the commitment population. Used private_commitment_register_2026-12-31.xlsx, the capital-account statements and Q4 custodian cash activity. Retained all 98 registered funds. Removed one superseded statement from 2,303 rows, leaving 2,302; joined on fund ID and standardized the manager identity affecting 78 retained statement rows. Kept all 33 historical negative NAV observations rather than treating them as invalid cash-flow records.

Completed year-end balances. The opening population comprises 72 Q4 statements, two missing-Q4 repairs, 20 earlier-term expiries and four pending funds. For the two missing statements, applied September NAV plus custodian calls less distributions. Ardley V's repaired NAV/unfunded balances are USD 48.78M/USD 87.84M; Marrable V's are USD 9.72M/USD 193.34M. The four pending commitments count in full at USD 667.00M. Original commitments of USD 9,709.00M reconcile to cumulative calls of USD 5,128.69M, released commitments of USD 389.31M and unfunded commitments of USD 4,191.00M.

Prepared the manager evidence. Used 21,568 portfolio-activity records, 531 audited fund-year observations and 108 market quarters. Portfolio activity contains 1,124 initial investments, 2,047 follow-ons, 17,840 valuations and 557 realizations, with no duplicate transaction keys. The 3,171 missing cost-basis fields belong to investment transactions; exposure was taken from preceding valuations, not zero-filled. Converted statement dollars to millions and audited thousands to fund-level millions, applying LP ownership shares separately.

Calculated policy distributions. Used the industry benchmark's 69,675 rows covering 2,200 funds. The prescribed historical window contains 3,457 current fund-quarter observations and produces 48 strategy-quarter rates. Each rate is summed distributions divided by summed prior-quarter NAV. The 125 entering observations have zero distributions; the 19 departing observations have zero prior NAV. Independent and matched-panel denominator calculations agree. Applied the rates to fixed opening private NAV of USD 3,986.27M, producing USD 1,050.86M of policy distributions.

Calculated reserve and spending. Used the 18 classified liquid holdings, excluding the blank and footer rows. Eligible reserve is USD 2,137.41M: cash/Treasuries USD 499.70M, investment-grade bonds USD 345.15M, equities USD 966.49M and redeemable hedge funds USD 326.07M. Used approved FY2027 spending of USD 286.50M, divided by four and repeated for eight quarters. The five proposed 2027 funds determine commitment proportions; the pacing-plan total row and proposed 2028 commitments are not added to the tested programme.

Estimated calls from Wexmoor's own managers. Separated initial investment, scheduled follow-ons, delayed support, financing repayment, fees and expenses. Initial-deployment calibration uses 1,413 fund-quarter observations, including 597 zero-investment quarters, with manager estimates shrunk toward own-strategy estimates. The later deployment check uses 402 observations against 1,011 training observations and has RMSE of 1.234509 percentage points. Opening investment financing of USD 239.40M is repaid in the first stress quarter.

Validated the stress-sensitive components. Support estimation retains 6,332 observations after removing 7,195 younger-company exposures, 3,259 other-strategy exposures, 254 post-2026 observations and 800 observations with insufficient remaining commitment. The two-quarter-lag support model has later holdout R-squared 0.980620. Realization timing was selected using the earlier validation period, independently of the policy outcome; its later R-squared is 0.155152, indicating substantial remaining uncertainty. Registered terms and remaining commitments constrain every forecast.
