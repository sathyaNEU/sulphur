# task20 determinism check, pass 2

## Verdict

DETERMINISTIC

## Disposition

APPROVE

## Evidence

### Mechanical recomputation (independent, from the shipped files)

| Figure | Block value (band) | My recomputation | Match |
|---|---|---|---|
| Liquid reserve at policy factors | 2,137.4 | 2,137.41 (cash/MMF/UST 499.7x1.0 + IG bonds 383.5x0.9 + public equities 1,380.7x0.7 + redeemable-within-24mo hedge funds 362.3x0.9 + non-redeemable hedge funds 412.8x0 + other 152x0) | Exact. Confirms the pass-2 fix: computed using plain 31 Dec values, no stress revaluation. |
| Spending (8 quarters) | 573.0 | 8 x (286.5/4) = 573.0, FY2027 approved distribution read from spending_distributions_FY2014_FY2027.csv | Exact |
| Commitments not yet called, by strategy | Buyout 1,918.2; Growth equity 433.4; VC 186.0; RE 288.1; Infra 840.8; PC 524.6; total 4,191.1 | Buyout 1,918.2; Growth equity 433.4; VC 186.0; RE 288.1; Infra 840.8; PC 524.6; total 4,191.0 | Exact per strategy, total within the stated 0.5 tolerance. Independently rebuilt from capital_account_statements (superseded row dropped), custodian Q4 activity for the 2 late funds (WX-BO-102, WX-BO-113), and the register's 4 pending-first-close funds at full commitment. No fund had both a lapsed term and a nonzero unfunded balance, so the "released at term end" rule binds nothing in this cut, consistent with the data. |
| Distributions in the stress, by half-year | H1'27 402.8 (402.3-403.3); H2'27 280.2 (279.7-280.7); H1'28 169.5 (169.0-170.0); H2'28 198.4 (197.9-198.9) | 402.80; 280.18; 169.51; 198.36 | All land at the center of the stated band. Rebuilt by summing, per quarter, each Wexmoor fund's 31-Dec-2026 value (late 2 funds adjusted by custodian Q4 net) times its strategy's rate = sum(benchmark distributions_pct_of_commitment that quarter) / sum(benchmark nav_pct_of_commitment at prior quarter-end), for the matching 2008Q3-2010Q2 quarter. |
| Net cash needs at USD 500m budget | 1,060.7 | 573.0 + 1,123.3 (first-close calls) + 148.9 (yet-to-close calls) + 266.5 (new-budget calls at 53.3/100m x 5) - 1,050.9 (distributions) = 1,060.8 | Within rounding (five inputs each rounded to 0.1) |
| Headroom at USD 500m | -123.3 | 2,137.4 - 1,060.7 - 1,200 = -123.3 | Exact |
| Headroom at USD 250m | +9.9 | 2,137.4 - 927.55 - 1,200 = 9.85 | Within rounding |
| Largest budget that passes (pre-step) | 268.6 | Solve 794.3 + 0.533X = 937.4 => X = 268.5 | Matches; confirms stepping DOWN (not nearest) to 250, since I separately verified 275 fails the test by about 3.5m headroom |
| First-close slip coefficient | 0.61 quarters per 10 points below 100 | Regressed slip (quarters) on index deficit/10 across all 90 historical first closes in the register (reference = exit index at the quarter before the originally expected close): slope through origin 0.621, OLS slope 0.614 (intercept ~0.02), R²=0.85 | Matches closely; a real, well-fit empirical relationship, not an arbitrary pick |
| First-close slip applied to the 4 pending funds | 2.5 and 3.8 quarters | My regression-based slip for the stress path: ~2.43-2.47 quarters (3 funds due Q3'27) and ~3.70-3.77 quarters (1 fund due Q4'27) | Close but not exact (within about 0.1-0.3 quarters); consistent with a well-determined fit, not a planted number |
| Subscription-line clean-down mechanism | "2022 and 2023 calls show each manager cleaning its lines down" | fund_audited_financials: total credit facility borrowings across all funds = 0 in FY2022, FY2023 and FY2024 (versus USD 2.9-5.6bn in 2019-2021), matching the elevated short-rate years | Mechanism confirmed present and visible in the data |
| Capital calls include fees and expenses | (used throughout Results 4/5) | unfunded_commitment_usd decreases, every period, by exactly contributions_investments + contributions_management_fees + contributions_fund_expenses (checked on WX-BO-102's last 4 statements) | Exact; closes the fork, the file's own arithmetic forces fees/expenses into "capital calls" |
| Defensive follow-on coefficient | 0.64 pct of cost per quarter per 10 points below 100, fit on 2020 and 2022-2024 | Reconstructed two readings of "share of those companies' cost": (a) follow-on $ / cost basis of the full held-2y+ population -> slope 0.41 (R²=0.99); (b) follow-on $ / cost basis of only the companies that received a follow-on that quarter -> slope 1.18. The stated 0.64 sits inside this bracket | Could not pin the exact denominator convention with certainty; qualitative relationship (rises as the lagged exit index falls below 100) is strong and real in both readings. See note below. |

### Gate C: the 10 named forks

1. **Half-year scenario** (H1/H2 2027, H1/H2 2028): pinned by the prompt itself. Closed.
2. **Which funds count as having held a first close**: pinned by the register's First close date (null only for the 4 "pending first close" status rows). Closed.
3. **Fees and expenses as capital calls**: closed by the capital account arithmetic above and by custodian_cash_activity, which records only one combined "capital call" movement type (a solver cannot split it even if they wanted to).
4. **Released commitments at term end**: pinned by liquidity policy section 3; checked and currently binds zero funds (no fund has both a lapsed term and a nonzero unfunded balance), so it cannot move the figure regardless of reading.
5. **The late-statement value**: pinned verbatim by policy section 7 (30 Sept value + Q4 calls - Q4 distributions per the custodian). Used directly; distributions reproduced almost exactly.
6. **The benchmark rate**: pinned verbatim by policy section 7 (quarter's distributions_pct_of_commitment over prior-quarter nav_pct_of_commitment, summed over the strategy's benchmark funds). Used directly; reproduced almost exactly.
7. **The stress path**: pinned by policy section 6 (exit index path from 2008Q3-2010Q2 scaled to the pre-test level; short rate +2.5pp; confirmed 31-Dec-2026 short rate 2.75% + 2.5 = 5.25%, matching Step 4's figure exactly).
8. **The budget's spread across the pacing plan**: closed by the fix. The "2027 proposed commitments" sheet (Oakhanger 150 / Wendlebury 100 / Corvane 45 / Ewelme 70 / Harpsden 135, by strategy) and the "Long-range pacing" sheet's 2027 row (150/100/45/70/0/135) now agree exactly, so there is no longer a choice between two different "proportions."
9. **The USD 25 million steps**: pinned by policy section 5. Verified the step is applied by rounding DOWN to the largest passing multiple (250, not 275, since 275 fails by about 3.5m), not by nearest rounding.
10. **Whether the reserve is revalued along the stress**: closed by the fix. Policy section 4 now states explicitly: "The factors stand for the stress in section 6, so the holdings are counted at their 31 December values and not revalued along its path." My from-scratch reserve computation using plain 31-Dec values and the liquidity-class factors alone reproduces 2,137.4 exactly, with no additional stress revaluation step; the alternative reading (apply the section 6 equity stress schedule to the reserve) is now explicitly ruled out by this sentence.

No surviving defensible alternative was found for any of the 10 named forks; each is closed by a specific named fact in the policy text, the register, the custodian file, or the capital account arithmetic itself.

### Gate B

Every decisive fact traces to a shipped file: the liquidity class factors and their meaning (policy section 4, matches liquid_holdings_2026-12-31.xlsx's own class labels verbatim, including "redeemable within 24 months" matching the policy's "within the eight quarters"); the USD 1,200m minimum and USD 25m steps (policy section 5); the stress definition (policy section 6, reproduced against market_series_quarterly); the distribution and capital-call conventions (policy sections 7-8); the FY2027 approved distribution of 286.5 (spending_distributions CSV, not the IPS's formula, which is background only and not needed); the pacing plan proportions (corrigan_hart_pacing_plan_2027.xlsx, both sheets now agreeing). No external dependency found. No vocabulary gap: "first close," "credit facility," "pacing," "unfunded commitment" etc. are literal column headers in the shipped files, directly observed.

### Gates D and E

The difficulty is analytical (reconciling late statements, superseded rows, and pending funds; correctly fitting rather than naively extrapolating the first-close-slip and follow-on relationships; applying the stress definition literally), not semantic. The prompt commits to one call ("the largest 2027 total that passes") and pins population/window/unit for each supplementary ask (by strategy, by half-year, by first-close status, "commitments made by the end of 2026" excluding the new budget). No bundling, no goal-vagueness found.

## Note (not a fix)

The defensive follow-on coefficient (0.64 pct per 10 points, feeding the USD 212.8m Critical Component 2 figure) is the one place I could not pin the exact "share of cost" denominator convention by independent reconstruction; my two natural readings bracket the stated value (0.41 and 1.18 against 0.64) rather than confirming it to the decimal. This does not reach the tightest-banded figure: the 2-quarter lag means the lagged exit index is still above 100 for all of H1 2027 (the quarters feeding the tightly-banded 517.0, band 505.0-532.0), so the follow-on effect lands entirely in H2 2027 and 2028, whose bands are proportionally wider (+-6.6% to +-9%). The policy itself leaves the capital-call method open ("judged from their record," section 8), so this is reported as a residual uncertainty, not a determinism defect.

## Fix

None.
