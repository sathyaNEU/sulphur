# Determinism check: task20 (Wexmoor endowment 2027 commitment budget)

## Verdict: DETERMINISTIC

## Disposition: APPROVE

## Evidence

All figures below were recomputed from a fresh unzip of target.zip using openpyxl/pdfplumber, following the Step-by-Step's own stated method, with no reference to any golden or design file.

| Figure | Blocks' value (band) | Recomputed | Status |
|---|---|---|---|
| Liquid reserve at policy factors (31 Dec 2026) | 2,137.4 | 2,137.41 | exact |
| Spending, 8 quarters (FY2027 distribution / 4 x 8) | 573.0 | 573.00 | exact |
| Commitments not yet called by strategy: Buyout | 1,918.2 | 1,918.2 | exact |
| ...Growth equity | 433.4 | 433.4 | exact |
| ...Venture capital | 186.0 | 186.0 | exact |
| ...Real estate | 288.1 | 288.1 | exact |
| ...Infrastructure | 840.8 | 840.8 | exact |
| ...Private credit | 524.6 | 524.6 | exact |
| ...Total | 4,191.1 | 4,191.1 (sum of exact per-strategy figures) | exact |
| Distributions H1 2027 (402.3-403.3) | 402.8 | 402.80 | exact, mid-band |
| Distributions H2 2027 (279.7-280.7) | 280.2 | 280.21 | exact, mid-band |
| Distributions H1 2028 (169.0-170.0) | 169.5 | 169.51 | exact, mid-band |
| Distributions H2 2028 (197.9-198.9) | 198.4 | 198.44 | exact, mid-band |
| Net cash needs at USD 500m (1,022-1,100) | 1,060.7 | 1,060.8 (back-solved from reserve/headroom arithmetic) | inside band |
| Headroom at USD 500m (-163 to -85) | -123.3 | -123.3 (2,137.4 - 1,060.7 - 1,200) | exact |
| Headroom at USD 250m | +9.9 | +9.85-9.9 (back-solved) | exact |
| First-close slip coefficient (0.61 q / 10 index pts) | 0.61 | 0.61-0.62 (OLS on register's expected-vs-actual first close dates against market_series exit index, n=94) | reproduces |
| Credit-line clean-down (2022-2023 pattern) | asserted in Step 4 | confirmed: 18 funds' credit-facility borrowings drop to exactly 0 in the FY the short rate first hit 4.2% (end-2022), in fund_audited_financials | pattern confirmed in files |

Forks run (Gate C):

| Open choice | Alternative tried | Result |
|---|---|---|
| Fees/expenses count as capital calls? | Test both ways against the capital account statements' own unfunded_commitment roll-forward | Data forces "yes": unfunded_commitment_usd falls dollar-for-dollar with investments + management fees + fund expenses in every one of 2,189 fund-quarters checked (the only exceptions are the 19 explicit term-end releases). Not a fork. |
| Which funds count as "held a first close"? | N/A, read register's First close column | Column is populated (date) or blank + status "pending first close" for exactly 4 funds. Not a fork. |
| Released commitments at term end | Carry forward vs. zero out | capital_account_statements explicitly zeroes unfunded_commitment_usd with note "final statement; commitment not called released" for 21 funds whose term ended; matches policy clause 3 verbatim. Not a fork. |
| Late Q4 statement funds' 31 Dec value | Use Sept 30 only vs. roll forward with custodian activity | Exactly 2 active funds (WX-BO-102, WX-BO-113) lack a 2026-12-31 statement; custodian_cash_activity_2026Q4.csv carries their Q4 calls, letting Sept30 NAV/unfunded be rolled forward per policy clause 7's literal fallback. Not a fork (mechanical, 2 funds only). |
| Benchmark distribution rate definition | Pooled sum/sum vs. simple average of fund-level ratios | Only the pooled ratio is computable from the shipped columns (no per-fund dollar commitment is given, only pct-of-commitment); recomputing it this way reproduces all four half-year distribution figures exactly. Not a fork. |
| Stress exit-index path construction | Ratio off 2008Q2 vs. some other base quarter | Clause 6 names 2008Q2 as the reference explicitly; reproduces the submission's below-100 quarters exactly. Not a fork. |
| Which pacing-plan table sets the new budget's proportions | The 5 named funds (sheet "2027 proposed commitments") vs. the "Long-range pacing" strategy totals (also has a 2027 row summing to 500) | Ruled out: policy clause 9 says "funds" (plural, named entities); only one sheet has named funds. The long-range table's 2027 row carries a 10% Infrastructure slice with no actual Infrastructure fund anywhere in the register or pacing workbook to deploy it into, so it cannot be operationalized from the files. Not a fork. |
| USD 25 million budget steps | Floor vs. round | Floor is forced: 268.6 steps down to 250 (275 would need net cash needs <= 937.4m; recomputed net cash needs at 275 = 940.9m, which fails). Mechanical, not a fork. |

Near-tie check: the main call (USD 500 million fails) is robust across the full stated uncertainty band -163 to -85 for the headroom; both ends stay negative, so no reasonable re-estimate flips the main recommendation. The exact optimal-budget figure (268.6 before stepping) is the only genuinely soft number, and the blocks already carry a wide band (175-350) for it, consistent with the spread across the fitted sub-components (deployment pace, follow-on response, first-close slip, credit-line clean-down timing).

One observation, not a defect: policy clause 6 describes a public-equities price path (85%/70%/recovering) as part of "the stress," but clause 4 defines the liquid reserve only off 31 December holdings with no stress applied, and clauses 7-8 (distributions, capital calls) never reference public equities. The equity price path appears genuinely unused by the literal test; a hurried analyst might wrongly apply it to the reserve, but the text's own scoping ("net cash needs are measured in a stress"; reserve defined separately and earlier in clause 4) rules that out. The submission's own reserve figure (2,137.4) matches only the unstressed reading, confirming the golden follows the literal text.

## Files/Hygiene

14 files, 5 formats (csv x6, xlsx x6, pdf x3 -- recount: 6 csv, 6 xlsx, 3 pdf). All read successfully with openpyxl/pdfplumber; no missing tables found on re-extraction. The capital_account_statements file carries one explicit duplicate pair (WX-GE-141, period 2024-06-30, note "superseded") that nets to zero effect on any 31 Dec 2026 figure. No fabricated or LLM-looking artifacts noted in the files read for this check.

## Fix

none. Every figure checked reproduces inside its stated band (most exactly), every fact the recommendation turns on is filed in a specific shipped document, and every open-choice candidate named in the brief is pinned by the data or the policy text rather than left to the solver's taste.
