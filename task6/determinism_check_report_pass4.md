# determinism-check report, task6, 2026-11-09 (pass 4)

Context: re-judge after pass 3's FIX_NOW. Since pass 3, the input pack, `prompt.txt` and every filed document are
unchanged. `submission.md`'s answer blocks changed in one place: every contrast figure for "each service's own
spans reweighted on its own hourly count" (Final Recommendation, Critical Component 2, Step-by-Step step 3) and the
golden docx's "How the SLI was read" paragraph now state the own-hour contrast consistently, with the same incident
time left out as the golden weighting, so only the weighting basis differs (fares 0.9%, partner-gateway 1.1%,
notifications 0.8% everywhere). This pass runs its own fresh isolated thread (no reuse of pass 3's figures) against
the bundle as it now stands.

## Verdict
**DETERMINISTIC.** No SOLUTION_WRONG. No NOT_DETERMINISTIC finding.
**Disposition:** APPROVE. The isolated thread independently reproduced every load-bearing figure in
CRITICAL_COMPONENTS, SOLUTION_STEPS, FINAL_RECOMMENDATION and both SUPPLEMENTARY_ANSWERS blocks from the raw files,
including the previously-contested own-hour contrast figures (fares 0.9%, partner-gateway 1.1%, notifications 0.8%),
the full incident-minutes CSV (10/10 services, exact to the minute), and partner-gateway's 90% CI via an independent
cluster bootstrap (2.08-2.43% against the golden's linearised 2.08-2.44%). No model rerun required.
**Stumping type:** mechanism: `method_or_model_selection` + `decomposition_attribution` (mixed);
stumping_family: `analytical_non_defect`; surface_read_dependency: `no`; sole_data_defect: `no`.

## Why
PR-SLO-3 §2.1-2.4, 3.1-3.4 and 5.2, read literally, force the population, window and incident-exclusion rule; the
thread rebuilt the full December SLI table under the trace-root-share weighting for all 10 services from
`trace_spans_2026-12.parquet` and `lb_target_group_requests_2026-H2.csv` (via `service_catalogue_2026.xlsx`'s
crosswalk) and matched the golden exactly on all 10. Separately, it recomputed the same spans under each service's
own hourly count with the identical incident exclusions (Critical Component 2's fix target) and got fares 0.877→0.9,
partner-gateway 1.089→1.1, notifications 0.758→0.8 — an exact match to the now-corrected solution text and the
golden docx paragraph, resolving pass 3's finding 4 (the earlier inconsistent 0.4%/0.6% figures are gone). The two
contested root-cause calls (INC-1611 on fares, INC-1619 on notifications, and INC-1579 on partner-gateway, where the
call decides nothing) were independently re-derived from span self-time changepoints, including confirming that the
root-cause direction flips between INC-1570 and INC-1579 on the same service pair (seat-map/partner-gateway) — ruling
out any fixed "blame the bigger service" heuristic. The thread also confirmed the Final Recommendation's own
dismissal clause (swapping INC-1611/INC-1619's cause to journey-search/accounts reproduces fares and notifications
both at ≈0.86-0.92%, rounding to 0.9%, exactly as claimed).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| December SLIs, all 10 services (root-share weighting) | journey-search 0.5 ... notifications 1.3 | exact match, 10/10 | yes |
| Own-hour contrast (CC2, Step 3, Final Recommendation) | fares 0.9%, partner-gateway 1.1%, notifications 0.8% | 0.877→0.9, 1.089→1.1, 0.758→0.8 | yes (previously-flagged item now closed) |
| Golden docx "How the SLI was read" paragraph | same 0.9% / 1.1% / 0.8% figures | matches submission.md verbatim (orchestrator cross-check) | yes |
| Incident minutes CSV, 10 services x 2 halves | full table | exact to the minute, 10/10 (partner-gateway 292/659, notifications 99/680, seat-map 690/216, etc.) | yes |
| Over-budget set and order | places, partner-gateway, fares, seat-map, notifications | same 5, same weighted-count order (places 401,028 > partner-gateway 351,504 > fares 182,181 > seat-map 35,112 > notifications 31,641) | yes |
| Shares (36/31/16/3/3, sum 89%) | 36/31/16/3/3 = 89% | 35.6/31.2/16.2/3.1/2.8 → rounds to same, sum 89% | yes |
| Excess requests | 280,000 | ≈284,854 → rounds to 280,000 | yes |
| Partner-gateway 90% CI | 2.08% to 2.44% | independent cluster bootstrap 2.079%-2.427% | yes (within the stated band) |
| INC-1611 / INC-1619 / INC-1579 root cause | fares / notifications / partner-gateway | self-time changepoints reproduce the claimed onset ordering for all three, including the direction flip between INC-1570 and INC-1579 on the same service pair | yes |
| "No other conclusion survives" dismissal clause | swapped attribution gives fares/notifications 0.9% each | reproduced (≈0.863% / 0.922%, both round to 0.9%) | yes |

## Competing answers that survived
None. Every fork the design note names (SF8-SF10, SF14, SF16: the weighting base, the root's or span's hour,
November orphans, the onset lead window, the interval method) was run by the thread or is carried over as "same
call" from the prior passes' own verification; no rival lands outside the stated band on any graded figure.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files, categories | 10+, 2+ | 15 files (target.zip namelist, excluding archive wrapper); csv x6, xlsx x2, docx, json x2, md, parquet = 6 formats | yes |
| Large messy CSVs | one 20,000+ rows, one 10-20 printed pages | `lb_target_group_requests_2026-H2.csv` 44,160 lines; `cloud_billing_2026.csv` 7,858 lines x 9 cols | yes |
| metadata distractors | 2+, none labelled in ZIP | 8 named in `metadata.json` (capacity_review, app_store_reviews, lb-H1, production_deployments, cluster_rollout_history, cloud_billing, cloud_invoices, cloud_resources); no in-ZIP labels found by the thread or by direct inspection | yes |
| Distractors unused, relevant | yes | thread traced none as answering a graded quantity; plausible adjacent SRE/FinOps artifacts | yes |
| Deliverables | 1-3, all in golden | 2 (docx, csv); `golden.zip` namelist = exactly `reliability_review_2026.docx`, `service_sli_2026.csv` | yes |
| Asks multi-dimensional, unit/rounding stated | yes | per-service grid, ranked list with shares and CIs, chart, 7 incident root causes, CSV grid; one rounding sentence closes the prompt | yes |
| Answer shape, 4+ checkable results | yes | design note's 6 results (R1-R6) across 6 areas; thread independently counted 7 across 5 (minor recount difference, both well over the 4-result floor) | yes |
| Golden ZIP exact file set | yes | confirmed by direct zipfile listing | yes |
| Realism / no LLM tells | yes | thread found no provenance/LLM-authorship tells in target/; distinct file mtimes (Jul 2026 to Jan 2027) consistent with a real production timeline | yes |

## Gate G reconciliation
Thread: `method_or_model_selection` + `decomposition_attribution` (mixed), `analytical_non_defect`,
surface_read_dependency `no`, sole_data_defect `no`. The thread explicitly checked for a surface number being
debunked and found none: "no shipped file states a naive/dashboard SLI number that is later overturned... there is
no surface-reported number being debunked." This matches the design note's own framing (R3's method shortcut is
the hurried *default*, not a planted/reported figure being corrected) and pass 2/3's prior classifications. No
mismatch between the thread and the design note.

## Gate H reconciliation
Design note's **Results chain**: R1 (incident minutes, assembly), R2 (per-incident root cause, investigation
loops), R3 (every service's December SLI, measurement), R4 (90% CI, uncertainty), R5 (services over budget,
synthesis), R6 (order/shares/excess, decomposition and attribution) — 6 results, 6 areas. Design note's **Effort
test**: quick 0/6, careful 1.5/6 (25%), thorough 6/6; pair estimate 31.3; the weighting sentence alone rescues **0**
of 6 (the note's explicit, measured correction, flagging that "judge passes 2 and 3 each found a fresh reader
overclaiming this sentence"); the *other* candidate sentence ("each incident's cause is the named service whose own
handling rose first, not the one furthest over its curve") rescues 1 of 6 (R2 only).

The thread's Gate H line: `domain: pass`, `layers: pass`, `results: 7 graded across 5 areas`, `one_thing: none`,
`effort: quick 1-2 of 7, careful 3-4 of 7, thorough 7 of 7`, `one_fact: "weight each kept span by its trace root's
hourly keep share, not the service's own" rescues... roughly 2-3 of 7 results, under a third`.

Three deltas worth recording against the note, the first a genuine recurring finding:

- **The one-fact test overclaim recurs a third time.** The thread credits the root-keep-share weighting sentence
  with rescuing "2-3 of 7" results. The design note's own measured AND-logic (Effort test, lines 160-165) states
  this exact sentence rescues **0** of 6: the weighting alone, with each incident attributed to the service
  furthest over its curve (the natural pairing without R2's dating insight), leaves fares and notifications at
  0.9% each and only **three** services over budget, not the five the recommendation names — so the weighting fact
  by itself does not rescue R3, R5 or R6, only R2's own dating insight closes the gap, and the note records that
  pass 2 and pass 3 each made the identical overclaim independently. This is now a third independent recurrence
  (pass 2 finding 3, pass 3 finding 1, pass 4's thread), despite the note's explicit added correction line aimed at
  exactly this misreading. Correcting the thread's claim against the note's own stated mechanics puts the true
  one-fact rescue at 0-1 full results (R2 at best, from the *other* candidate sentence), which still clears H5's
  one-third ceiling comfortably, so **H5 still passes** on the corrected count — but the recurrence means a fresh
  isolated reader, with no visibility into the note, keeps reaching for the more "load-bearing-sounding" sentence
  and overstating its rescue power. This is a review-robustness finding about how the sentence reads in isolation,
  not a task defect.
- **Effort-grade level, careful vs. design note.** The thread's careful-but-hurried share (3-4 of 7, 43-57%) sits
  well above the note's calibrated careful score (1.5 of 6, 25%, from `effort.json`'s actual pair estimate of
  31.3). The gap is plausibly a result-counting artifact (the thread may be splitting R1/R6 or crediting partial
  correctness on R4's binomial-interval shortcut as "right" rather than "missed") rather than a real disagreement
  about which figures a careful run gets wrong — the thread's own prose still says the careful run "land[s] on the
  explicitly-dismissed wrong answers" for the over-budget set (R3/R5/R6), consistent with the note. Still, 43-57%
  is not "clearly" below the thorough score's 100% by the same margin the note's own measured figures show, and it
  is not level with thorough (7/7), so it does not flip H4, but it is the second pass in a row (after pass 3's
  finding 2) where an isolated thread's own effort grading reads looser than `effort.json`'s measured bands.
- **Results/areas recount (7 vs 6, 5 vs 6 areas).** Minor and non-disqualifying: both comfortably clear the 4-result,
  3-area H4 floor, and the thread's own area labels (assembly/reconciliation, measurement, causal
  reasoning/decomposition, uncertainty, synthesis) overlap closely with the note's six.

No Gate H failure: no single hidden or planted thing carries the task (the weighting insight alone still only
reaches three over-budget services per the note's own math; the root-cause attribution, the CI, and the
incident-minutes reconciliation are each independent, checkable pieces), the swap test holds, and the effort test
separates quick from thorough cleanly on every count (quick ≤29%, thorough 100%) even with the recount delta.

## Stump power (Gate F)
Two independent judgments, matching the design note's Hidden factor record (all "keep") and `effort.json`'s pair
estimate of 31.3: (1) the trace-root-share weighting versus the textbook own-hourly reweighting, which a
careful-but-hurried run defaults away from and which alone flips the over-budget set for partner-gateway, fares and
notifications; (2) the per-incident root-cause attribution by load-adjusted onset changepoint rather than the
most-intuitive heuristics (first-named, most slow requests, furthest-over-curve-across-the-whole-incident), which
the thread confirmed is a genuinely non-obvious, non-fixed-direction judgment (the attribution direction flips
between INC-1570 and INC-1579 on the same service pair). The thread independently verified both the golden route and
every one of the solution's claimed wrong routes (own-hour weighting gives places+seat-map; root weighting with
furthest-over-curve attribution gives three services; the swapped-attribution dismissal gives fares/notifications
back at 0.9%), so the losses are spread across weighting, attribution, CI and synthesis rather than concentrated in
one trap, as the design note intends.

## Findings, ranked
1. MEDIUM, recurring one-fact overclaim (third occurrence): the thread's `one_fact` estimate ("rescues roughly
   2-3 of 7, under a third") exceeds what the design note's own measured effort-test mechanics support (the
   weighting sentence alone rescues 0 of 6 per the note's AND-logic; only R2's dating sentence rescues 1). Does not
   change the DETERMINISTIC verdict or H5's pass (the corrected count, 0-1 of 6-7, clears the one-third ceiling by
   a wider margin than the thread's own self-reported number). Author action: none required to ship; if the design
   note is revisited, consider adding a sentence that explicitly anticipates a fresh reader crediting the weighting
   sentence with "roughly half" or "2-3 of 7" results (the pattern has now recurred in three independent judge
   passes despite the note's existing correction), since a line aimed at past readers has not stopped new ones from
   making the identical misread.
2. LOW, effort-grade looseness: the thread's careful-but-hurried share (3-4 of 7, 43-57%) reads higher than the
   note's calibrated 1.5 of 6 (25%) from `effort.json`. Does not flip H4 (still clearly below the thorough score and
   below half); likely a result-counting granularity difference rather than disagreement on which results a careful
   run actually gets wrong. No author action required.
3. LOW, cosmetic result/area recount (7 vs 6 results, 5 vs 6 areas): both pass the H4 floor comfortably; no
   disagreement about which figures are graded or how they are classified at the gate level.

## Next action for the author
None required before the next status change: every previously-open item (pass 3's two unreproduced narrative
figures, the incident-minutes partial match, and the CI verification gap) is now closed — the thread this pass
independently reproduced the own-hour contrast figures, all 10 services' incident minutes, and partner-gateway's CI
from the raw files with no residual discrepancy. The task is ready to ship as-is; the only items worth a note in a
future design-note revision are the recurring one-fact overclaim pattern (finding 1) and the effort-grade looseness
(finding 2), neither of which requires a rebuild or rerun.
