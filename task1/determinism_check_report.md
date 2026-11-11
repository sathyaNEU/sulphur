# determinism-check report, task1, 2026-11-10 (re-judge pass, architecture 3)

Re-judge pass after the two graded-figure changes: ask 5 now asks how many of the plan's 2027 starts on each
channel would still be paying at the end of 2027 if every line ran (previously: intro subscribers at 31 Oct
2026); ask 9 now asks the share of the November 2025 to April 2026 starts still paying three years after
starting (previously: two years). The reader-survey distractor also changed to carry a coded reason column.
Bundle `target.zip` md5 b7b3094e3c45a67f386bb3cef2258dc2.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG).
**Disposition:** APPROVE
**Stumping type:** mechanism: mixed (forecasting/missingness-completion for the newest-starts survival terms,
method/model selection for the household-linkage and full-price-inclusive end-of-intro terms, binding constraint
for the 3.5x funding rule); stumping_family: analytical_non_defect; surface_read_dependency: no;
sole_data_defect: no.

## Why
The isolated judge thread found every decisive mechanism behind the recommendation (the 3.5x funding rule, the
household definition, the net-revenue formula, the channel taxonomy) stated verbatim in
`digital_subscription_kpi_standard.pdf` and `price_list_digital_2027.pdf`, with the arithmetic chaining to the
committed figures reproducing exactly or inside the stated bands everywhere it was fully recomputed. I
independently re-verified the two headline sums myself, outside the thread's allowed path, directly against
`media_plan_2027.xlsx`'s own Spend 2027 column: the funded 8 lines sum to EUR 84,308.00 to the cent, and adding the
6-line shortcut set (PART-BHR, PART-KBO, SOC-BHR, SOC-ELN, SOC-GAZ, SOC-KBO) gives EUR 141,575.00 to the cent,
accounting for all 18 real plan lines (plus the sheet's Total row and footnote, correctly excluded). No committed
answer is contradicted by a literal reading of the files. The one open item is verification-budget, not a
demonstrated defect (see Competing answers / Evidence below): the thread could not fully re-derive the two
newly-changed figures (ask 5's plan-wide 31 Dec 2027 survival, ask 9's three-year survival) end to end within its
time budget.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Funded-8 budget | EUR 84,308 | EUR 84,308.00 (thread, and independently by me from media_plan_2027.xlsx Spend column) | Yes, exact |
| 14-line shortcut budget | EUR 141,575 | EUR 141,575.00 (thread, and independently by me) | Yes, exact |
| Ask 5/9 plan-starts denominators by channel | 735/687/466/685/387, total 2,960 | exact match summing media_plan's 12 monthly Starts columns by channel (thread) | Yes, exact |
| Household-linked 36-month value, Jul-Sep 2023 starts (ask 10 / component 4) | social 150, search 222, cashback 228, telemarketing 131, app 179, direct 265 (bands given) | social 151.8, search 222.3, cashback 225.1, telemarketing 121.8, app 175.8, direct 266.0 (independent pipeline: dedup, product/test filters, union-find household linkage, VAT/store-fee-net revenue) | 4 of 6 channels inside band; telemarketing (121.8 vs 123-131) and app-store (175.8 vs 177-180) land just outside, by <1.2 points / <0.7%, attributed by the thread to its own simplified billing-month heuristic rather than a golden defect |
| Customer-number-only variant (component 4 contrast figure) | social 128, direct 249 | social 128.1, direct 248.5 | Yes, essentially exact |
| Older-cohort full survival baseline (the contrast figure behind ask 9 / component 2) | social 12.0%, search 25.5%, cashback 15.6% | social 11.8%, search 25.6%, cashback 17.9% | social and search essentially exact; cashback the loosest match (17.9 vs 15.6) but still the right side of the comparison |
| Newest-cohort 3-year survival, reading-completed (ask 9 / component 2, the changed figure) | social 10.1 (9.9-10.2), search 27.3, cashback 13.5, telemarketing 8.9, app 12.3, direct 28.8 | not independently re-derived end to end (the hazard model itself); a raw unconditional spot-check at matched cohort ages did not clearly confirm the direction (young SOC cohort ran slightly above the old FB cohort through month 11 in a raw cut, and mean early reading was roughly equal between cohorts) | Open: not disproved, not independently confirmed. Thread explicitly flags this as a verification-budget gap, not a finding against the golden (a correctly specified hazard controlling for months-since-full-price and offer/channel, rather than an unconditional raw cut, can reasonably differ) |
| Plan-wide survival to 31 Dec 2027 (ask 5, the changed figure) | 403/735 social, 478/687 search, 370/466 cashback, 498/685 telemarketing, 255/387 app; total 2,004/2,960 | denominators exact; numerators depend on the same unreplicated hazard model as above, not independently confirmed to band | Open, same caveat as above |
| EUR 84,308 vs media_plan_2027.xlsx 18-line accounting | 8 funded + 6 shortcut-added + 4 never-funded = 18 | confirmed: funded8=84308, extra6=57267 (84308+57267=141575), remaining 4 lines (TEL-GAZ, APP-GAZ, APP-KBO, TEL-ELN) never funded under either scenario | Yes, exact, done by me directly against the bundle |

## Competing answers that survived
None found for the main recommendation or any of the fully-recomputed supplementary answers: the margin between
the lowest funded line's multiple (3.67x) and the highest unfunded line's (3.08-3.32x) is a real gap on a rule
pinned by KPI-standard section 4.1, not a knife-edge, and the thread found no reasonable alternative
household/channel/reading definition that moves a line across the 3.5x line.

For the two changed asks (5 and 9), no competing answer was shown to survive either — the thread's partial,
unconditional spot-check did not confirm the golden's direction, but it also did not establish a rival figure as
defensible; it is an unresolved verification gap, not a demonstrated fork. The design note's own fork and
closure tables (`DESIGN_NOTE.md` Semantic fork table SF11, SF10) pin the "three years after starting" and "every
line run as planned" readings used by these two asks, and the note records every rival reading-measure and tenure
form as landing in the stated band in `checks.py` R7 (not re-verified by me beyond trusting the author's own gate,
per the no-generator/no-design-note-before-return rule).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 17 files: CSV (13), XLSX (2), PDF (2) | Pass |
| Large messy files | a 20,000+ row CSV and a 10-20 printed page CSV | `reading_by_login_2024-01_2026-10.csv` (423,746 rows) and `subscriptions_2023-01_2026-10.csv` (32,473 rows) satisfy the row-count file; `marketing_spend_2023-01_2026-10.csv` (828 rows, ~16-20 printed pages) satisfies the page-count file | Pass |
| metadata.json distractors | 2+ named, none labelled inside the ZIP | 4 named (`print_circulation_2023-2026.csv`, `newsletter_signups_2025-2026.csv`, `reader_survey_2026.csv`, `digital_ad_revenue_2025-2026.csv`); none referenced in `submission.md` or `DESIGN_NOTE.md`, only in `generator/pack.py` (author-side, not shipped) | Pass |
| Distractors unused yet relevant | each weighs plausibly, none load-bearing | `print_circulation` (print, not digital, subscriber-shaped but out of scope by standard 2.1-2.2), `digital_ad_revenue`, `newsletter_signups` all plausible and unused; `reader_survey_2026.csv` (now with a coded `main_reason_code` column) checked explicitly by the judge thread and confirmed to carry no key joinable to any other shipped file and is referenced by no SOLUTION_STEPS | Pass |
| Deliverables | 1-3, all present in golden | 2 requested (`acquisition_lines_2027.xlsx`, `acquisition_note_2027.pdf`), both present in `golden.zip`, no others | Pass |
| Asks multi-dimensional, units stated, no rounding instruction | — | all 10 supplementary asks are per-channel/per-title/per-offer multi-row asks with units in the sentence; `prompt.txt` carries no rounding instruction, precision/bands are in `submission.md` | Pass |
| Answer shape | one of the 14 client shapes | an allocation (which lines to fund, the budget) with its sensitivity (the multiple-of-cost margin and rival bands) | Pass |
| Golden ZIP exact match | exactly the requested files, requested formats | `golden.zip` = `acquisition_lines_2027.xlsx` + `acquisition_note_2027.pdf`, nothing else | Pass |
| Not LLM-looking | — | judge thread found no LLM-authorship tells; governing documents read as real board-approved policy prose with version history | Pass |

Spec gates: all pass.

## Gate G reconciliation
Thread: `mechanism: mixed`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`,
`sole_data_defect: no`.

`DESIGN_NOTE.md`'s own Deep reasoning section states, verbatim: "Not semantics" (every field/code/clause read
correctly still leaves each hurried result wrong), "Not rule application" (the standard files the WHAT, not a
procedure), "No decoy" (no memo/draft/stakeholder figure ships), "No replay" (no result re-derives a published
figure). These line up exactly with the thread's `surface_read_dependency: no` and `sole_data_defect: no`: there
is no reported number anywhere in the shipped files that is itself wrong and must be caught; the difficulty is
building four transported models (full-price-inclusive end-of-intro, reading-completed survival, tenure-banded
cancellation excess, household linkage) from honest data. Gate G passes cleanly, no reconciliation gap.

## Gate H reconciliation
Thread: `domain: pass`, `layers: pass`, `results: ~15 graded across 6+ areas`, `one_thing: none`,
`effort: quick ~2-3 of 15, careful ~7-9 of 15, thorough 15 of 15`, `one_fact: "subscriptions sharing a payment
fingerprint or address are one household, link their revenue" rescues ~2 of 15`.

`DESIGN_NOTE.md`'s Results chain lists 9 underlying results (R1-R9) across assembly-reconciliation, data
discovery, modeling, causal reasoning (x2), missingness-measurement, forecasting (x2) and synthesis — 7 distinct
areas, consistent with the thread's "6+ areas." Its Hidden factor record lists four constructed-but-not-shallow
factors (newest-cohort reading differences, the full-price-inclusive end-of-intro exit, the rise's
notice-window/tenure response, household return-under-new-account), each verdict "keep," each requiring modelling
(not a one-step fix) and none confined to only the deciding units. The thread's own probing of the household
factor (the one it could fully recompute) found it real, file-derived, and matching the note's claimed magnitude
(+14.4%/+7.0% effect size recomputed vs the note's implied +17.2%/+6.4%) — consistent with "routine to link,
modelling to carry," not a shallow catch.

Its Effort test table gives quick 0/9, careful 2/9 (22%), thorough 9/9, with a Largest single hint ("the April
2025 rise also raised the share leaving at the end of the introductory price") rescuing 2 of 9 (R3, R4) and a
Pair estimate of 34.6. The thread's independently-derived numbers (quick ~2-3/15 = 13-20%, careful ~7-9/15 =
47-60%) are expressed over a finer unit (grading each supplementary ask and critical component separately rather
than the design's 9 consolidated results, several of which are graded via more than one block). Checking the two
tripwires named in this skill's reconciliation rule: the quick pass is comfortably under a third (13-20%, not
above), and the careful pass (47-60%) does not level with the thorough pass (100%) — both clear. The one real
divergence is in magnitude, not direction: the thread's careful-pass estimate (47-60%) runs noticeably higher
than the design's own pair estimate (34.6%), driven by its finer grading unit (an ask that reuses an R already
graded via a critical component is counted twice). This is a genuine difference worth the author's attention
before the next pair of platform runs, but it is not, on its own, one of the two reconciliation tripwires, and
the per-result pattern underneath it matches closely: the thread named the same results a careful-but-hurried run
is likeliest to lose (the household-linkage substitution on ask 10, and the pooled end-of-intro model on asks
6/7) as the design's own effort table (R2 Missed, R3 Partly/R4 Missed at the careful-but-hurried level). The
thread's best single sentence rescues about 2 of 15 (13%), under the design's 2 of 9 (22%) share — so the
one-fact test is, if anything, stated more conservatively by the independent thread than by the design note, not
less. The declared distractor (`reader_survey_2026.csv`) was explicitly checked and confirmed not load-bearing.
No reconciliation finding crosses the send-back threshold.

## Stump power (Gate F)
The thread assesses genuine, spread stump power: a careful-but-hurried run that applies the KPI standard's
stated rules literally but takes the first available shortcut at each of four junctures lands on a specific,
wrong figure at each (customer-only EUR 128/249 instead of household EUR 150/265 on ask 10; the older channel's
pooled 12.0%/25.5% instead of the reading-completed 10.1%/27.3% on ask 9 and component 2; a points-add of
materially less than 5.5-6.6 from a pooled historical fit instead of the full-price-term fit on component 3/asks
6-7; 229 pooled extra cancellations instead of 420 tenure-banded on ask 8). No single one of these, once named,
resolves the others. This matches the design note's own run forecast (R2, R4, R5, R6 each lost to a distinct
method shortcut) and its claim of six distinct wrong funded sets over eleven shortcuts.

## Findings, ranked
1. (Open, not a defect) The two changed figures — ask 5 (plan-wide survival to 31 Dec 2027) and ask 9 (three-year
   survival of the Nov 2025-Apr 2026 starts) — were not independently re-derived end to end by the judge thread
   within its time budget. The thread's unconditional spot-check did not clearly confirm the golden's claimed
   direction (that the newest cohorts read/convert worse than their channel's older starts), but it also did not
   establish that the golden is wrong; a correctly specified hazard model (controlling for months-since-full-price
   and offer/channel jointly, which the design note's Results chain and Hidden factor record both specify as the
   governing method) is not something an unconditional raw cut can rule out. Recorded as the primary residual
   uncertainty from this pass.
2. (Minor, not a defect) Two of six channels in the household-linked 36-month value (ask 10 / component 4) land
   just outside the stated band under the thread's own abbreviated pipeline (telemarketing and app-store, by
   under 1.2 points / 0.7%). The thread attributes this to its own simplifications (a heuristic payment-exception
   matching window, no explicit 14-day-withdrawal re-filter), consistent with the other four channels and the
   customer-number-only contrast figures landing essentially exact. Not escalated.
3. (Confirmed clean) Budget arithmetic, plan denominators, and the 18-line accounting all reproduce exactly from
   `media_plan_2027.xlsx`, independently of the judge thread.
4. (Confirmed clean) `reader_survey_2026.csv`'s new coded `main_reason_code` column does not make it load-bearing;
   it remains a genuine, unjoinable distractor.
5. (Confirmed clean) Gate G and Gate H reconciliation found no hidden/planted thing carrying most of the results,
   no surface-read-rejection, and an effort gradient (quick << careful << thorough) consistent with the design
   note's own table, net of a grading-unit-granularity difference in the magnitude of the careful-pass share
   (worth noting to the author, not a gate failure).

## Next action for the author
No fix required to ship. If closing the one open item (finding 1) before the next pair of platform runs is
wanted, the highest-value next step is a second, better-resourced recompute of the full-price-leaving hazard
specifically (joining `reading_by_login_2024-01_2026-10.csv`/`logins.csv` on months-since-full-price rather than
months-since-start, fit per offer and channel, exactly as `DESIGN_NOTE.md`'s Results chain for R5/R9 specifies) to
independently confirm the 10.1%/27.3%/13.5%/8.9%/12.3% figures and the 403/478/370/498/255 plan-wide numerators —
this is the only load-bearing claim this pass could not close to its own satisfaction.
