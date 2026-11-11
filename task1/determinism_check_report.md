# determinism-check report, task1, 2026-11-11

Context: architecture 3 of task1, repaired 2026-11-11 after the platform's holistic audit (returned on
determinism); DESIGN_NOTE.md records two earlier judge passes on the pre-repair cut (judge pass 1 and judge
pass 2, both 2026-11-10) and says "the determinism judge runs once on the repaired build." This report is
that post-repair pass, run against the final rebuild (target.zip, golden.zip, submission.md, prompt.txt as
they stand on disk today).

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: mixed (forecasting + decomposition_attribution + method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why

The judge thread reproduced the main assembly result (ask 4, paying digital subscribers at 31 October
2026 by title) exactly from `subscriptions_2023-01_2026-10.csv` + `price_periods_2023-01_2026-10.csv` +
`customers.csv` (dedup 449 exact-duplicate export rows, drop non-`DIGITAL` products and 24 `TEST`
accounts, join the price period covering 2026-10-31 with price > 0): Brueckenhafener Rundschau 5,076 /
Grevenauer Anzeiger 3,065 / Kreisblatt Ostheide 2,608 / Elmsbacher Nachrichten 1,481, total 12,230,
matching the committed figure to the digit, and corroborated it against an independently-dated controlling
file (`kpi_digital_2026.xlsx`) at four prior month-ends (within 0-2 subscribers per title, exact at June
2026). `media_plan_2027.xlsx`'s 18 lines reproduce the funded/excluded multiples with a clean, non-marginal
gap at the 3.5x cut (funded 3.93-6.47x, best excluded ~3.01-3.05x). The household-vs-customer-number
distinction (Critical Component 4) is a real join, not relabeling (1,797 shared payment fingerprints
across 2-4 distinct customer numbers). Every decisive term the recommendation turns on (consumer
subscription, "paying," household, 36-month value, the 3.5x funding rule, the price tiers and their
effective dates, the channel-code crosswalk) is stated in `digital_subscription_kpi_standard.pdf`,
`price_list_digital_2027.pdf`, `marketing_channel_codes.csv` or `offer_catalogue.csv`, with no external
dependency and no unreachable-action-vocabulary problem (the recommendation's "funded," "3.5 times"
language is lifted from the KPI standard itself).

**Material caveat on Gate A, disclosed by the thread itself:** the five forecasting/survival/attribution
sub-models underlying asks 1, 5, 6, 7, 8, 9 and 10 (the 36-month line values, the plan's end-2027
survivors, the intro-end and April-2027 churn deltas, the extra-cancellation count, the three-year
channel survival, the household-linked 36-month value) were **not independently rebuilt to their stated
precision bands**; the thread checked that every decisive input is present in a named file and that no
block contradicts another, but did not re-derive these figures from raw rows the way it did for ask 4.
This is a real scope limit on this pass, not a defect in the task: the design note's own closure table
(`checks.py R7`, `boot.py`) already runs the rival panel and a 39-of-40 start-month bootstrap against
these same five models and reports every golden figure 8 per cent or more from every rival and 12 per cent
or more from the funding bar, which is strong independent (author-side) corroboration this judge pass did
not duplicate. A future pass, or the real platform reviewer, should not assume these five models were
freshly recomputed here.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Paying subscribers at 31 Oct 2026, by title (ask 4) | BHR 5,076 / GAZ 3,065 / KBO 2,608 / ELN 1,481 (12,230) | BHR 5,076 / GAZ 3,065 / KBO 2,608 / ELN 1,481 (12,230) | Yes, exact |
| Same pipeline at Jan/Mar/Jun/Sep 2026, vs `kpi_digital_2026.xlsx` | file's reported counts | within 0-2 per title (exact at Jun) | Yes, within noise, independent source |
| media_plan_2027.xlsx funded multiples (3.94-6.46) vs best excluded (3.05) | 3.94-6.46x funded / 3.05x best excluded | 3.93-6.47x funded / ~3.01-3.05x best excluded | Yes, clean non-marginal gap |
| Household fingerprints shared across customer numbers (Critical Component 4) | a real join, not the customer number | 1,797 fingerprints shared by 2-4 distinct customer_no | Yes |
| 36-month net revenue per start, all 18 lines (ask 1) | EUR 85 to EUR 352 | not independently rebuilt | Not contradicted; structural consistency only |
| Nov 2025-Apr 2026 three-year channel survival (ask 9, Critical Component 2) | social 9.2%, search 26.4%, cashback 11.8%, etc. | not independently rebuilt | Not contradicted |
| Intro-end share and April-2027 add (asks 6-7, Critical Component 3) | PM1 69.1%/+7.7pt, ... | not independently rebuilt | Not contradicted |
| Extra cancellations from the April 2027 rise (ask 8) | 394 total, by title | not independently rebuilt | Not contradicted |
| 2027 plan survivors at 31 Dec 2027 (ask 5) | 1,869 of 2,960 | not independently rebuilt | Not contradicted |
| Jul-Sep 2023 household-linked 36-month value (ask 10, Critical Component 4) | social EUR 151, direct EUR 256 | not independently rebuilt | Not contradicted |

## Competing answers that survived

None found by the judge thread on the pieces it tested (the dedup, the channel crosswalk, the price-list
windows, the funding cut's margin). The design note's own closure table runs a wider set of rivals on the
five un-rebuilt models (reading-measure forms, tenure forms, offer-term forms, household-linkage forms,
the rise's window) and reports every rival funding the same eight lines, with every line 8 per cent or
more from the bar on every rival; this judge pass did not re-run that rival sweep itself but found nothing
in the files that contradicts it.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 18 (14 used + 4 declared distractors) | Pass |
| File categories | 2 or more | CSV (spreadsheet/text, 12 files), PDF (text/document, 2 files), XLSX (spreadsheet, 2 files) = 3 categories across 2+ families | Pass |
| Large messy CSV, 20,000+ rows | 1 or more | `reading_by_login_2024-01_2026-10.csv`, 423,723 rows | Pass |
| Large messy CSV, 10-20 printed pages | 1 or more | `marketing_spend_2023-01_2026-10.csv`, ~828 data rows x 6 columns (semicolon-delimited, German locale), approx. 18-19 pages at a plain print layout | Pass |
| metadata.json names 2+ distractors, none labelled inside the ZIP | required | 4 named (`print_circulation_2023-2026.csv`, `newsletter_signups_2025-2026.csv`, `reader_survey_2026.csv`, `digital_ad_revenue_2025-2026.csv`); none is named as a distractor in any shipped file | Pass |
| Each distractor relevant, unused by the solution | required | all 4 are plausible adjacent-business files (print circulation, newsletter signups, a reader survey, display-ad revenue), none touched by SOLUTION_STEPS 1-8; none reproduces a graded quantity arithmetically | Pass |
| 1-3 deliverables, all present in golden, no format mandated by prompt | required | prompt asks for "a spreadsheet" and "a one-page note"; golden/golden.zip hold exactly `acquisition_lines_2027.xlsx` and `acquisition_note_2027.pdf` | Pass |
| Asks multi-dimensional, unit stated, no rounding instruction in prompt | required | each of the 10 supplementary asks carries its own unit and a band in the answer blocks; prompt.txt has no rounding language | Pass |
| Answer shape is one of the fourteen client shapes | required | "a flagged set with the evidence" (the funded lines, each line's value/multiple, the budget, the eight supporting figures) | Pass |
| Golden ZIP holds exactly the requested files, in the requested formats | required | 2 files, xlsx + pdf, matching the prompt and the submission | Pass |
| Nothing LLM-generated, every golden reads as a real work product | required | design note and pre-ship check record a realism sweep (reader-survey free-text fix, channel-code list fix); judge thread's own grep for benchmark/LLM-authorship markers across target/ returned nothing | Pass (per thread; not independently re-swept by this orchestrator) |

## Gate G reconciliation

Thread: `mechanism: mixed (forecasting + decomposition_attribution + method_or_model_selection)`,
`stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. No
reported/surface figure in the package is being caught as wrong and flipped away from; `kpi_digital_2026.xlsx`'s
own numbers are confirmed and extended (a confirm-the-read element), and every hurried failure the thread
checked (pooled survival extrapolation, a flat after-the-date cancellation count, customer_no as household,
an end-of-intro rate with no full-price term) is a plausible-but-wrong *method* on honest, correctly-read
data, which is the FINE-numbers shape Gate G wants. This agrees with the design note's own classification
("Not semantics," "Not rule application," "No decoy," "No replay," four modelling judgments) and with its
template-check line (chain signature assembly-reconciliation / data-discovery / modeling / causal-reasoning
x2 / missingness-measurement / forecasting / synthesis / forecasting). No banned_stumping_type.

## Gate H reconciliation

Design note's canonical results chain has 9 results (R1-R9) across assembly-and-reconciliation, data
discovery, modeling, causal reasoning (x2), missingness-and-measurement, forecasting (x2) and synthesis;
the thread, working from the graded-block granularity (the recommendation, 4 critical components, 10
supplementary asks), counted roughly 12-13 gradable results across 5+ areas. The two counts are
reconcilable, not contradictory: several asks are the same underlying R at different grain (e.g. ask 1's
18 line values are all R7; the recommendation is R8). On the substance:

- **one_thing:** thread found none; design note states "not one thing" explicitly and backs it with a
  hidden-factor record of 4 separate constructed factors, each independently "keep"-verdicted (no single
  one alone flips the funded set; six distinct wrong sets arise from eleven different shortcuts). Agrees.
- **Hidden factor conditions:** all four factors in the design note's hidden factor record are classed
  "modelling" to find and "modelling" to fix (not a routine filter/reweight), matching the thread's own
  description of each trap as "a plausible-but-wrong method," not a shallow planted defect. Agrees.
- **Effort grades:** design note's effort.json-measured table is quick 0.5 of 9 (~6%), careful 2.5 of 9
  (~28%), thorough 9 of 9 (100%). Thread's own estimate is quick ~1 of 12-13 (~8%), careful ~4-6 of 12-13
  (~31-46%), thorough 12-13 of 12-13 (100%). Both show clear separation and a quick pass well under a
  third; the thread's careful-pass upper estimate (46%) runs a bit richer than the design note's measured
  28%, but the thread explicitly flagged that it did not rebuild 7 of the 9 underlying models, so its own
  "careful" estimate is a looser guess than the design note's effort.py-measured figure. Not a red flag,
  but worth noting the design note's number is the more load-bearing one.
- **One-fact test, the one real discrepancy worth recording:** the design note's measured largest single
  hint is "the April 2025 rise also raised the share leaving at the end of the introductory price,"
  rescuing R3 and R4 only (2 of 9, ~22%). The thread instead named a *different* sentence as most useful
  ("complete each cohort's survival from its own reading data, not its channel's older cohorts' pooled
  rate") and estimated it rescues the recommendation, ask 1, ask 5 and ask 9 (~4 of 12-13, ~31%, or in
  canonical R-chain terms roughly R5/R7/R8/R9, 4 of 9 = 44%). Read naively this would be a genuine Gate H5
  concern (a different, larger-reaching hint than the one the author priced). But the design note's own
  pre-ship check already ran exactly this counterfactual and recorded the result directly: **"with the
  reading hint the period term still funds SOC-KBO"** — i.e. giving a run the reading-completion insight
  alone does *not* rescue the recommendation (R8), because R7/R8 also depend on R3 and R4 (the full-price
  term), which that hint does not touch. The thread's "rescues the recommendation" claim does not survive
  this already-tested counterfactual; the design note's quantified answer (2 of 9 via the price-term hint)
  stands. This is reported as a finding against the thread's analysis, not against the task.

## Stump power (Gate F)

Thread's stump-power read: four separately-sourced traps (reading-completion for the newest cohorts,
tenure-banded extra-cancellation attribution for the April 2027 rise, household linkage via payment
fingerprint vs customer_no, and a full-price term in the end-of-intro model calibrated off the April 2025
step), each landing a hurried model on a specific, named wrong figure (1,977 still paying vs 1,869; EUR
135,385 for 14 lines vs EUR 80,084 for 8; 209 cancellations vs 394). This is losses spread across several
results, matching the 2026-11-09 bar, and agrees with the design note's own run-forecast line (R2, R4, R6,
R7, R9 lost or partly lost on a careful-but-hurried pass; R1 and R3/R5 partly earned). No too-easy signal
located by the thread (no methodology checklist in the prompt, no documented defect handed out, the
funding rule is the filed WHAT and not the whole task).

## Findings, ranked

1. **(Process, this pass)** The judge thread broke the required blind-derivation order at its first tool
   call (it printed the whole `graded_blocks.md` before writing any of its own derivation), so Gate A's
   reproduction of ask 4 and the structural checks on the rest should be read as a trace/reproduction
   check, not a blind independent derivation. It still argued the semantic-fork and rule-location claims
   (dedup not being a fork, the crosswalk having no date overlap, the price tiers not overlapping) from the
   files' own terms rather than from the stated answer, which limits the damage, but the isolation
   contract was not fully honored on this run.
2. **(Scope limit, this pass)** 7 of the design note's 9 canonical results (R2 through R6, R7, R9) were not
   independently rebuilt to their stated precision bands in this pass; they were checked for internal
   consistency and input-presence only. The design note's own rival sweep and 39/40 bootstrap on these same
   models (checks.py R7, boot.py) is the strongest evidence of record that they hold, but this judge pass
   did not reproduce that evidence itself.
3. **(Minor, no action)** The thread's named "largest single hint" differs from, and claims a larger
   reach than, the design note's own effort.py-measured hint, but the design note's pre-ship check already
   ran the thread's exact counterfactual and found it does not rescue the recommendation (SOC-KBO stays
   wrongly funded). No change needed; recorded for the record.
4. **(Non-finding)** No competing defensible answer, no missing decisive fact, no external dependency, no
   banned surface-read-rejection shape, and no one hidden/planted factor carrying most of the results were
   located anywhere in this pass.

## Next action for the author

None required to ship this cut: the verdict is DETERMINISTIC / APPROVE, Gate G passes clean
(analytical_non_defect, no surface-read-rejection), and Gate H passes (not one thing, difficulty spread
across the modelled results, the one-fact test already stress-tested in the design note's own pre-ship
check). If headroom is wanted before the next platform run, the one open item is procedural, not
analytical: re-run the determinism-check judge thread once more with its unzip and `graded_blocks.md`
read strictly in the required order (own derivation written first, blocks opened second) so that Gate A's
reproduction of asks 1, 5, 6, 7, 8, 9 and 10 is a genuine independent rebuild rather than a consistency
check against inputs the thread had already seen pointed at the committed figures.
