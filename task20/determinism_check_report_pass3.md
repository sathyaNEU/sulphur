# task20 determinism check (pass 3)

## Verdict: DETERMINISTIC with SOLUTION_WRONG

## Disposition: FIX_NOW (solution only) -- but verify the call before closing

One modeled figure in the refinancing-calls chain does not reproduce under the only ownership-share
method the shipped files support, and it sits close enough to the program-B qualifying line that the
author must re-check whether the call itself survives the correction, not just the one number.

## Evidence

| Figure | Blocks' value | My recompute | Status |
|---|---|---|---|
| Liquid reserve at policy factors | 2,778.7 | 2,778.7 | exact (liquid_holdings x policy sec. 4 classes, as filed) |
| Spending, 8 quarters | 791.0 | 791.0 | exact (FY2027 approved distribution 395.5 / 4 x 8; FY = 1 Jul-30 Jun per investment policy sec. 2, confirmed by partial FY2027 Q1/Q2 payments already posted) |
| Distributions in stress, H1/H2 2027, H1/H2 2028 | 685.6 / 466.2 / 273.9 / 291.3 | 685.6 / 466.2 / 273.9 / 291.3 | exact (fund values at 31 Dec x benchmark's pooled distribution-% rate, Q3 2008-Q2 2010 mapping, summed by strategy) |
| Commitments not yet called by strategy (6 strategies + total) | 1,601.8 / 421.4 / 223.7 / 581.2 / 1,172.7 / 474.0 / 4,474.8 | identical to the dollar | exact (register + capital-account unfunded_commitment_usd, superseded WX-GE-141 row dropped, 2 late statements rolled from Q3 + custodian Q4 activity, 4 pending funds counted in full) |
| Program re-up calls -> program totals (A/B/C/D) | 289.1 / 180.6 / 139.9 / 17.5 | same, from the blocks' own per-fund call figures | arithmetic ties out exactly to the pacing plan's program membership |
| Headroom before any 2027 commitment | 215.7 (182.3-235.3) | 215.6 from reserve - (spending+calls-distributions) - 1,520 minimum, using the blocks' own stated capital-calls total (1,969.1) | within rounding |
| **21 property/infra loans maturing 2027-2028, Wexmoor's share** | **USD 681.2 million** | **USD 909.5 million** | **does not reproduce** |

**The loan count and population are exact and unambiguous**: filtering manager_portfolio_activity's
"asset loan drawn"/"asset loan refinanced" records to Real estate + Infrastructure funds, taking the
latest loan record per (fund, portfolio company), dropping any company whose latest activity record of
any type is a "realization" (sold, no loan to refinance), and keeping maturities in 2027-01-01 to
2028-12-31 gives exactly 21 loans, independent of whether liquidated-fund exclusion is applied at all
(none of the 21 sit on a liquidated fund; all 21 are "asset loan drawn," none are post-mid-2022
refinances, consistent with the "12 refinancings since mid-2022" used only for fitting). No realization
record exists anywhere in any of the 21 companies' histories. I could not find a different 21-loan
population that reconciles to 681.2.

**The dollar conversion does not reproduce.** Applying each loan's face amount (amount_usd_m) at
Wexmoor's only available ownership measure -- Commitment (USD m) / Fund size (USD m) from the register,
confirmed to equal audited "Total commitments" exactly for every fund in the set -- gives USD 909.5
million, not 681.2 (a USD 228.3 million, 33% gap). Neither PDF (liquidity policy or investment policy
statement) states an alternative ownership-share convention; neither the register, the audited
financials, nor the activity file carries any other ownership or pro-rata field. 681.2/909.5 = 0.749,
which does not match any stated policy constant (the 0.700 LTV cap is a lender limit on value, not an
LP-share factor, and applying it would give 636.7, still off).

**Why this matters for the call, not just one line item.** The blocks' own stated band for the headroom
is 182.3 to 235.3, and program B's qualifying calls are 180.6 -- B clears even the band's lower edge by
only 1.7. If the corrected Wexmoor-share balance (909.5, 33% above the filed figure) carries through
proportionally into the stressed-refinancing gap and call (currently 157.2 of the 1,969.1 total calls),
the true headroom could fall below 180.6, which would flip the largest passing program from B to C. I did
not re-run the lenders'-limit regression itself (fitted on 12 historical refinancings and 597 quarterly
valuations, explicitly a modeled/banded piece), so I cannot certify whether the corrected balance still
leaves B passing; I can certify that the currently filed USD 681.2 million does not reproduce from the
shipped files by the only ownership method they support.

**Successor-close component (critical component 3, USD 49.4 million off calls):** directionally
consistent and not independently contradicted. Ewelme Real Estate V's and Corvane Ventures V's named
successors (Ewelme VI, Corvane VI) are exactly the pacing plan's Q1 2027 re-ups; Thornwick Capital
VI/Rudgely Equity VII/Brackley Growth VIII are exactly the register's three other "pending first close"
funds. The register's "Investment period ends" field does not reduce to a single clean formula (first
close + years, with any fixed rounding) for any manager, clause or not -- reproducing the exact 14-vs-10
manager split and the 61-succession count requires comparing many historical pairs, which is consistent
with this being a genuine investigation result rather than a one-line lookup. I did not find anything
that contradicts the five named funds or the 14/10 manager split within budget.

## Open-choice check (Gate C)

Ran the fiscal-year fork named in the Step-by-Step's own logic: using FY2026's approved distribution
(371.2) instead of FY2027's (395.5) for spending would raise headroom to roughly 264, still outside the
blocks' own band (182.3-235.3) in the other direction, and still leaves A failing -- but this alternative
is closed by a filed fact, not a judgment call: the investment policy statement section 2 pins the fiscal
year to 1 July-30 June, and spending_distributions_FY2014_FY2027.csv already shows FY2027 Q1 and Q2 paid
(consistent with a July-start year reaching Jan-Mar 2027 data pulls) and Q3/Q4 unpaid, so FY2027 is the
only reading the files support. No other forced choice found; the liquid-holdings file's "Policy
liquidity class" column already assigns each holding's factor (policy section 4 delegates this to the
Office of Investments), closing that fork too.

## Files/Hygiene

14 files, formats present: xlsx (5), csv (6), pdf (3). No missing-file or external-dependency issue found
for anything I checked; every figure I verified traces to a specific shipped file.

## Fix

**Where:** solution.

**What:** recompute the 21 property/infrastructure loans' Wexmoor-share balance from
manager_portfolio_activity_2013_2026.csv (asset loan drawn/refinanced, realized companies excluded) at
Commitment/Fund size from private_commitment_register_2026-12-31.xlsx; the figure should be USD 909.5
million unless the generator has a different, file-grounded ownership convention I could not locate, in
which case that convention needs to be stated somewhere in the shipped files (which would make the fix
input_files instead). Propagate the corrected balance through the stressed-refinancing gap and call, the
half-year capital-calls figures (Supplementary Q4), the headroom and its band (Supplementary Q3, Critical
Component 1), Critical Component 2's own numbers, and re-run the program test (Step 8) to confirm program
B still clears before re-shipping; if it does not, this becomes a SEND_BACK (the call and Final
Recommendation would change), not a cosmetic FIX_NOW.
