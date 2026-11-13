# task20 architecture 3: platform review (pasted by the author, 2026-11-13)

Your package is impressive. Rebuilding the hedge book, the desk's selling rule, NEX's margin replay, the reservoir dispatch against the 700 GWh floor and the lagged affiliate tariff is real work, and the 2022 records peak (EUR 548.5m on 26 August 2022) reproduces exactly from the statements, day-ahead settlements and ledger.

The problem is annex (a) of the liquidity standard. "Moves on each business day by the percentage the forward ... moved on the corresponding day of 2022 (the same date, or the latest 2022 business day before it)" can be read two ways. One reading applies each mapped date's one-day 2022 return, so some moves repeat and others drop out. The other copies the cumulative level against the 30 December 2021 curve. By 27 August the first reading raises the January 2028 forward 2.22 times and the second 2.63 times. On your own model the first gives about EUR 208m and a EUR 250m facility, and the second gives your 328.8m and EUR 350m. The 2022 check cannot separate them, because both reproduce 2022 by construction.

To fix it, rewrite annex (a) so it reads one way. For example: "On each business day the stress forward for a delivery month equals its value on the last business day of the previous year times the ratio of the 2022 forward for the same calendar month on the corresponding date to its value on the last business day of 2021." Then add the daily-move reading to your variant sweep.

For what we are looking for, see https://project-sulfur.learn.joinhandshake.com/nov-09-updates.

Reasoning
Step 0: the golden is present and the inputs match the task (Hallingvass Kraft, NEX Clearing, the 2026 liquidity standard, the 2022 stress year). Eighteen files were checked.

PART A, correctness. I rebuilt the 2022 records peak from three sources: net_cash_to_nex in the NEX statements (with the superseded statement removed), the day-ahead net_amount_eur by settlement date, and paid_eur in the sales ledger by paid date. It comes to EUR 548.457m on 26 Aug 2022, which agrees with the author's 548.5. The model run reported the same 548.457 and the same 2022 replay date. The run also agrees with the author on several figures: hedge ratios 68.55/39.61/22.23, 2027 book after the peak 0.638 TWh, the peak date 27 Aug 2027, and the 2022 replay of about 548.4 on 26 Aug. On its own model the run reports EUR 328.747m under "cumulative price-level copying", which matches the author's 328.8. So the author's chain reproduces under the author's reading, and the remaining question is determinism.

PART B, determinism. The deciding step is how annex (a) of hk_liquidity_standard_2026.pdf builds the stress curve. The clause reads: "Every delivery month's forward price ... moves on each business day by the percentage the forward for the same calendar month moved on the corresponding day of 2022 (the same date in 2022, or the latest 2022 business day before it)". Read literally, each 2027 business day takes the one-day 2022 return of its mapped date. Under that reading Friday moves are repeated and other moves skipped (by the run's count, 51 repeated and 51 skipped over the year). The author's reading copies cumulative levels: each 2027 day takes the 2022 curve on the mapped date divided by the 30 Dec 2021 curve. Section 2's "prices ... repeat those of 2022" leans toward levels, but the annex wording leans toward daily moves. No file and no control figure separates the two, because both reproduce 2022 exactly when run on 2022.

I computed the price factors to 27 Aug 2027 from hk_risk_curve_daily (HK_SYS) under both readings:

| Delivery month | Level copy | Daily-move |
|---|---|---|
| Sep 2027 | 2.973 | 2.639 |
| Dec 2027 | 2.679 | 2.276 |
| Jan 2028 | 2.632 | 2.220 |
| 2029 | 2.52 | 2.09 |

These gaps are large. The run, on an otherwise matching model, gets EUR 208.4m (a EUR 250m facility) under the daily-move reading against 328.7m (EUR 350m) under level copying. The fork flips the recommendation. Determinism: not_pinned (taxonomy competing_defensible_answer / underspecified_objective).

PART C, depth. Outside this fork the task is broad. It rebuilds the hedge book, recovers the desk's selling rule, replays NEX's margin rates, models dispatch against the licence floor, and prices customers on a lagged tariff. Several of those steps are recovered by replaying past figures, but there are several connected judgments, so depth_level 4 (not concentrated in one step). The run's first break is defensible_alternative_rejected. It noticed the issue and quoted the author's figure: "Cumulative price-level copying: gives EUR 328.747 million ... not the standard's instruction to apply the corresponding daily percentage move". That is not valid evidence of difficulty. The miss traces wholly to the clause reading (loss concentration high, information only).

Verdict: the main recommendation flips on an unpinned reading of one clause, so the task fails.
