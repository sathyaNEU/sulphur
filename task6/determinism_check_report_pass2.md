# determinism-check report, task6, 2026-11-09 (pass 2)

Context: this is a re-judge of architecture 7, the re-rooted results-chain build made after the 2026-11-09 final-review
return ("the breach list turns on one thing... a shallow hidden factor"). Pass 1 (2026-11-08) judged an earlier
prompt/submission state (architecture 5/6) and is superseded; it is not overwritten per instruction. This pass judges
the current `submission.md`, `prompt.txt`, `target.zip` and `DESIGN_NOTE.md` as they stand on 2026-11-09.

## Verdict
**DETERMINISTIC.** No SOLUTION_WRONG.
**Disposition:** APPROVE. The isolated judge thread independently rebuilt the root's-hourly-keep-share reweighting
from raw telemetry (not from the solution text) and reproduced the committed SLI table, the five-service over-budget
set, the order, and the 260,000-request excess; the INC-1619 self-time-vs-wall-time root-cause call also reproduced
cleanly. No rerun required.
**Stumping type:** mechanism: method_or_model_selection (primary, the inverse-probability/root-share reweight for
biased trace sampling) with a secondary decomposition_attribution (self-time vs. wall-clock for root cause);
stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.

## Why
Every load-bearing figure recomputes from the shipped files. PR-SLO-3's document.xml states only the literal SLI
definition and the threshold/budget table; it never mentions trace sampling (the thread grepped all files for
"sampl" with zero hits), so the root-share reweighting is discovered, not written down. The main recommendation (the
five services, in order) and Supplementary Q1/Q2/Q5 of the docx, and the CSV's SLI/budget/ran_over columns, are all
forced once the reweighting and the PR-SLO-3 3.2 incident-window exclusion are applied; the "reasonable but
insufficient" own-hour-reweighted rival the solution names also reproduces and lands on the alternate (wrong) four-
service answer, confirming the fork is real and resolves the way claimed.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| December SLIs (fares, places, seat-map, PG, notifications) | 1.2, 1.8, 2.0, 2.2, 1.2 | 1.20, 1.79, 2.05, 2.22, 1.23 | yes |
| Own-hour rival SLIs | fares 0.8, PG 1.1, notif 0.6 | reproduced qualitatively (fares/PG/notif under budget) | yes |
| Over-budget set and order | fares, places, seat-map, PG, notifications | same 5, same weighted-volume order | yes |
| Excess requests | 260,000 | matched to nearest ten thousand | yes |
| INC-1619 onset times | notifications 17:10, accounts 18:34 | self-time jump at 17:00-17:10 bucket (notifications), flat until 18:30 bucket then 4-10x jump (accounts) | yes |
| 7 December customer-facing incidents | INC-1570/79/88/94, 1611/19/27 | exactly the 7 with a status_page_history_2026.json entry; INC-1560, INC-1602 correctly excluded | yes |
| root_cause_service leak check | — | NaN/open for all 7 in incidents_2026.csv, not leaked | yes |
| 90% CIs (R4), incident-minutes H1/H2 merge (R1) | PG 2.04-2.40, etc.; per-service minute pairs | **not independently re-derived** (thread flagged as time-bounded, no contradicting evidence found) | not verified this pass |

## Competing answers that survived
None on the main call or Q1/Q2/Q5. The own-hour reweighting fork (the "reasonable but insufficient" rival) is real
but is ruled out by the data itself (root-level trace sampling, confirmed by the mismatch between ~24-25 kept roots/
hour per edge service and the LB's much larger hourly RequestCount), matching the design note's closure-table row 7.
The one gap: the thread did not rebuild the stratified-linearization CIs (R4) or the full incident-minutes merge
(R1) end to end, so no rival was stress-tested there this pass; nothing found contradicts them.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files, categories | 10+, 2+ | 15 files; csv, xlsx, docx, json, parquet, md (6 formats) | yes |
| Large messy CSVs | one 20,000+ rows, one 10-20 printed pages | lb_target_group_requests_2026-H2.csv 44,160 rows; cloud_billing_2026.csv 7,858 rows x 9 cols (prints well over 10-20 pages) | yes |
| metadata distractors | 2+, none labelled in ZIP | 8 named in metadata.json (capacity_review, app_store_reviews, lb-H1, production_deployments, cluster_rollout_history, cloud_billing, cloud_invoices, cloud_resources); no labels found inside target.zip | yes |
| Distractors unused, relevant | yes | none of the 8 answers a graded quantity per the judge thread and the design note's chain; cloud/billing/deployment files are plausible adjacent artifacts | yes |
| Deliverables | 1-3, all in golden | 2 (docx, csv); golden.zip holds exactly those two files | yes |
| Asks multi-dimensional, unit/rounding stated | yes | per-service grid, ranked list with shares and CIs, chart, 7 incident root causes, CSV grid; one rounding sentence covers all units | yes |
| Answer shape, 4+ checkable results | yes | 6 results (R1-R6) across assembly/reconciliation, investigation loops, measurement, uncertainty, synthesis, decomposition/attribution | yes |
| Golden ZIP exact file set | yes | golden.zip namelist == [reliability_review_2026.docx, service_sli_2026.csv], matches prompt's two deliverables | yes |
| Realism / no LLM tells | yes | docx reads as a genuine internal memo (named author, ref number, dated); csv is a plain data export; thread grepped for generated/synthetic/benchmark/llm/fictional/placeholder, zero hits | yes |

## Gate G reconciliation
Judge thread: mechanism method_or_model_selection (primary) + decomposition_attribution (secondary), family
analytical_non_defect, surface_read_dependency no, sole_data_defect no. Design note's data-native sentence for the
deep step ("the store kept a near-fixed number of whole traces an hour per edge service, so an internal service's
kept spans carry its callers' keep shares") matches exactly what the thread independently rediscovered as the
root-share reweight. The thread separately verified the root-cause decomposition (self-time vs wall-clock) as its
own analytical piece, matching the design note's R2 (investigation loops). No mismatch: nothing in the shipped
files states or reports a number the solver must catch as wrong and reject; every figure is built from raw
telemetry, consistent with `sole_data_defect: no` and the design note's "no surface read" posture. No declared
distractor was named by the thread as carrying a graded result.

## Gate H reconciliation
Design note's Results chain: R1 (incident minutes/half, assembly), R2 (per-incident root cause, investigation
loops), R3 (every service's December SLI, measurement), R4 (90% CI, uncertainty), R5 (services over budget,
synthesis), R6 (start order/shares/excess, decomposition and attribution) — 6 results across 6 areas, with the
carry-forward note that R3 depends on BOTH the reweighting AND R2 (the incident-window exclusion), so "no single
analytical result is the only one behind" R3-R6.

The thread's `results`/`layers`/`domain` lines match this structure (6+ results, 4+ areas named explicitly, domain
pass on the swap test, both mess/analysis layers named). The thread's `one_thing: none` agrees with the design
note's Hidden factor record, which marks all five candidate hidden factors "keep" (none constructed-and-isolated-to-
the-deciding-units: each moves multiple services, is found by modelling rather than a one-sentence tip, or is inert
texture that decides nothing).

Two numeric deltas worth recording, neither disqualifying:
- **Effort grades.** Design note (`effort.py` on `generator/effort.json`): quick 0/6, careful 2/6 (33%), thorough
  6/6. Thread's independent estimate: quick ~1/6 (17%), careful 3-4/6 (50-67%), thorough 6/6. The thread's careful
  pass is higher than the design's own paper estimate, but it still sits clearly below thorough (never levels with
  it), and quick stays at or under a third either way, so neither of the Gate H reconciliation's disqualifying
  conditions (quick over a third; careful leveling with thorough) is triggered. Worth a note for the author that the
  design's paper effort grades may be a touch conservative relative to what a real careful-but-hurried pass earns.
- **One-fact test.** Design note's largest single hint ("the 26 December incident began in notifications' SMS
  verification, before accounts backed up") rescues 1 of 6 by the design's own count. The thread named a different
  single sentence (the root-share reweighting insight) and estimated it rescues roughly 1-2 of 6 (the main ranking
  and the SLI table). On inspection this is likely an overclaim in the safe direction: the main recommendation's
  text itself states that without the INC-1619 attribution (R2), notifications drops out at 0.9% and only four
  services would be named, so the reweighting fact alone, without R2, would not actually rescue the full main
  ranking. Either reading stays at or under the one-third ceiling (1/6 to 2/6 = 17-33%), so H5 passes either way, but
  the author should record in the design note that R3/R5/R6 need the reweighting AND R2 jointly, since the current
  carry-forward note already says this and the thread's slightly looser estimate did not pick up the joint
  dependency.

No Gate H failure: no single hidden or planted thing carries the task, the swap test holds (SRE latency SLOs, trace
sampling and root-cause attribution are the domain's own reasoning, not borrowed nouns), and the effort test
separates quick from thorough cleanly under either the design's or the thread's numbers.

## Stump power (Gate F)
The thread names two separable traps: (1) the root-share reweighting versus the own-hour reweighting (a genuine,
non-obvious statistical judgment a competent-but-hurried analyst would plausibly skip, landing on the "reasonable
but insufficient" 2-or-4-service answer), and (2) the INC-1619 self-time-vs-wall-time root-cause call (a caller
→callee queueing effect that makes accounts look like it failed first on raw duration, when notifications'
own handling actually rose first). Both are genuine analytical traps on honest data, not a surface-read rejection.
This matches the design note's Hidden factor record verdicts (all "keep") and `effort.json`'s pair estimate of 40.5.

## Findings, ranked
1. LOW, verification gap (not a task defect): the isolated thread did not independently rebuild R4's 90% confidence
   intervals or R1's full incident-minutes H1/H2 merge end to end (time-bounded); nothing it found contradicts
   either, and the design note's closure table (rows 7, 16) and fork table (SF16) already pin the method. Author
   action: none required to ship; if a future pass has budget, spot-check one CI and one minutes pair.
2. LOW, design-note bookkeeping: the design note's paper effort grades (careful 2/6) run a bit lower than this pass's
   independent estimate (careful 3-4/6); both stay well under thorough's 6/6 and over quick's ceiling, so this is
   not a Gate H problem, just a note that the paper model may be conservative. No fix required before shipping.
3. LOW, one-fact test precision: record explicitly in the design note (or `effort.json`'s comment) that the
   reweighting insight alone does not rescue the main ranking without R2's INC-1619 attribution, since a future
   reviewer's single-sentence estimate could otherwise overclaim rescue power on R3/R5/R6.

## Next action for the author
No pack, prompt or solution-block change needed; the task clears DETERMINISTIC/APPROVE on both Gate G and the
2026-11-09 Gate H standard. Optionally, before the next status change, add one line to the design note's Effort
test section noting R3/R5/R6's joint dependency on the reweighting AND R2 (closing finding 3 above), then proceed
to READY.
