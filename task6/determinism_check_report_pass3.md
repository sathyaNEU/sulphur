# determinism-check report, task6, 2026-11-09 (pass 3)

Context: re-judge after (a) the generator's December trace spans changed (slowdowns now ramp in from uneven onset
times, two more incidents gained a caller whose own handling slows later but further than the fault's, three faults
were strengthened) and (b) `submission.md`'s four answer blocks were rewritten to new SLIs, intervals, shares and
root-cause components. `prompt.txt` and every filed document (PR-SLO-3, the service catalogue, the incident files)
are unchanged. Pass 2 (2026-11-09) approved the prior cut; this pass judges the current `submission.md`,
`prompt.txt`, `target.zip` and `golden.zip` as they stand, with its own fresh isolated thread (no reuse of pass 2's
figures, since the shipped numbers themselves moved).

## Verdict
**DETERMINISTIC**, append **SOLUTION_WRONG (minor)**. No NOT_DETERMINISTIC finding.
**Disposition:** FIX_NOW. The main recommendation, the full December SLI/budget/ran_over table, the service order,
the shares (36/31/16/3/3 = 89%) and the 280,000-request excess all independently reproduced from the raw files. Two
solution-block items did not independently reproduce to the isolated thread's own budget: the CSV's
`incident_minutes_h1`/`h2` for 6 of 10 services, and the main recommendation's narrative "own-weighted" contrast
figures (fares 0.4%, notifications 0.6%). Neither affects `ran_over`, the order, the shares or the excess figure; no
rerun required unless the author's own regeneration of those two items turns up a change to a graded value.
**Stumping type:** mechanism: `method_or_model_selection`; stumping_family: `analytical_non_defect`;
surface_read_dependency: `no`; sole_data_defect: `no`.

## Why
PR-SLO-3's thresholds table (section 4), SLI definition (section 2) and incident/root-cause rule (3.2/3.3), read
literally, force the budget column, the trace-root hourly-keep-share weighting (section 2.2's "any call... whether
or not the tracing store kept a span for it" only makes sense under a design-weighted estimator, since
fares-api/partner-gw/notify/payments are never trace roots and so their own LB RequestCount has no connection to how
heavily their spans were sampled), and the incident exclusion/root-cause rule. The isolated thread rebuilt the
weighting and the December SLI table for all 10 services from `trace_spans_2026-12.parquet` and
`lb_target_group_requests_2026-H2.csv` and reproduced every one of the golden's 10 SLIs to the stated rounding
(journey-search 0.54→0.5 ... notifications 1.32→1.3), which forces the five-service breach set, the order, the
shares and the excess independently of the solution text. The two contested root-cause calls (INC-1611 on fares, not
journey-search; INC-1619 on notifications, not accounts) were re-derived from span self-time binning, not read off
any filed column (`incidents_2026.csv`'s `root_cause_service` is blank/NaN for every December incident), confirming
R2's two hardest cases. The CSV's incident-minutes columns and one narrative contrast figure are the only items that
did not independently reproduce inside the thread's budget; they read as a solution-generation precision issue
(SOLUTION_WRONG-flavoured), not as evidence the graded figures are unforced.

## Recomputation ledger
| Figure | Claimed | Judge thread recomputed | Reproduced |
|---|---|---|---|
| December SLIs, all 10 services | journey-search 0.5 ... notifications 1.3 | 0.54→0.5 ... 1.32→1.3, matching all 10 | yes |
| Over-budget set and order | places, partner-gateway, fares, seat-map, notifications | same 5, same weighted-volume order | yes |
| Shares (36/31/16/3/3, sum 89%) | 36/31/16/3/3 = 89% | reproduced | yes |
| Excess requests | 280,000 | ≈284,854 weighted → rounds to 280,000 | yes |
| INC-1611 root cause | fares (not journey-search) | self-time jump 19:45 (fares) vs 20:15-20:45 (journey-search) | yes |
| INC-1619 root cause | notifications (not accounts) | self-time jump 17:30 (notify) vs 18:30 (accounts) | yes |
| 7 December customer-facing incidents | INC-1570/79/88/94/1611/19/27 | exactly the 7 with a status_page_history.json entry; INC-1560, INC-1602 excluded | yes |
| CSV `incident_minutes_h1`/`h2`, 10 services x 2 halves | full table | matched exactly for 4 of 10 cells (journey-search H1, tickets H1, partner-gateway H1, notifications H1); 16 cells differed by amounts the thread describes as clean multiples of 60 minutes (consistent with a DST-handling detail across the full year, which December alone does not exercise) | **partial — not fully independently verified this pass** |
| Narrative "own-weighted" contrast (fares 0.4%, PG 1.1%, notifications 0.6%) | stated in FINAL_RECOMMENDATION | PG reproduced (1.09-1.1%); fares ≈0.62-0.88% and notifications ≈0.67-0.76% in the thread's reconstruction, not 0.4%/0.6% | **partial — qualitative conclusion (fares/notifications stay under budget under this method) held in every variant; the precise decimal did not** |
| 90% CI (R4, partner-gateway 2.08-2.44 and the other over-budget intervals) | stated in Critical Component 3 | **not independently re-derived this pass** (thread's verdict does not report rebuilding the stratified linearisation) | not verified this pass |

## Competing answers that survived
None on the main call, on any supplementary answer, or on the five-service set, the order, the shares or the excess.
The only real fork (trace-root weighting vs. each service's own-hour reweighting) is run by the thread and resolved
the way the design note and the solution claim: own-hour weighting leaves fares/partner-gateway/notifications under
or near budget and gives a different, smaller breach set, which PR-SLO-3 2.2's literal text (a request counts
whether or not the store kept a span for it) rules out as the governing reading, not an equally licensed rival.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files, categories | 10+, 2+ | 15 files; csv (x6), xlsx (x2), docx, json (x2), md, parquet = 6 formats | yes |
| Large messy CSVs | one 20,000+ rows, one 10-20 printed pages | `lb_target_group_requests_2026-H2.csv` 44,160 rows; `cloud_billing_2026.csv` 7,858 rows x 9 cols (well over 10-20 printed pages) | yes |
| metadata distractors | 2+, none labelled in ZIP | 8 named in `metadata.json` (capacity_review, app_store_reviews, lb-H1, production_deployments, cluster_rollout_history, cloud_billing, cloud_invoices, cloud_resources); no in-ZIP labels found by the thread | yes |
| Distractors unused, relevant | yes | none traced by the thread as answering a graded quantity; plausible adjacent SRE/ops artifacts | yes |
| Deliverables | 1-3, all in golden | 2 (docx, csv); `golden.zip` holds exactly `reliability_review_2026.docx` and `service_sli_2026.csv`, matching the prompt's two deliverables | yes |
| Asks multi-dimensional, unit/rounding stated | yes | per-service grid, ranked list with shares and CIs, chart, 7 incident root causes, CSV grid; one rounding sentence at the prompt's end covers all units | yes |
| Answer shape, 4+ checkable results | yes | 6 results (R1-R6) across assembly/reconciliation, investigation loops, measurement, uncertainty, synthesis, decomposition/attribution | yes |
| Golden ZIP exact file set | yes | `golden.zip` namelist = [reliability_review_2026.docx, service_sli_2026.csv] | yes |
| Realism / no LLM tells | yes | thread found no README/benchmark/LLM-authorship tells; distinct file mtimes spanning a believable production timeline; `capacity_review_2026-Q4.md` reads as a real ops note, not boilerplate | yes |

## Gate G reconciliation
Judge thread: mechanism `method_or_model_selection`, family `analytical_non_defect`, surface_read_dependency `no`,
sole_data_defect `no`. No file states or asserts a pre-computed SLI, scorecard or conclusion that the solver must
catch is wrong; the SLI must be built from spans and LB counts from nothing, and the trap is choosing between two
defensible-looking aggregation/weighting methods under an unstated, non-uniform sampling design. This matches the
design note's own framing (Results chain R3: "method shortcut: each service's own spans reweighted on its own
hourly count"; no row in the Hidden factor record or the Semantic fork table describes a misleading stated figure
anywhere in the package). No mismatch between the thread's classification and the design note.

## Gate H reconciliation
Design note's **Results chain**: R1 (incident minutes/half, assembly), R2 (per-incident root cause, investigation
loops), R3 (every service's December SLI, measurement), R4 (90% CI, uncertainty), R5 (services over budget,
synthesis), R6 (start order/shares/excess, decomposition and attribution) — 6 results across 6 areas. The note's
carry-forward note states explicitly: "R3, R5 and R6 need both the weighting and R2: no single analytical result is
the only one behind them... the largest hint rescues one result," with a parenthetical added since pass 2 ("the
judge's pass 2 asked for this line, so no one-fact estimate credits either sentence with more than its own
results"). Design note's **Hidden factor record**: all five candidate factors (the edge sampler's near-fixed keep
rate, December's faults in one service's own handling, callers queueing behind a slow callee late in an incident,
the load curve itself, the exporter's re-sent batch) are marked "keep," each found by modelling or a routine query
and none isolated to the deciding units alone. Design note's **Effort test**: quick 0/6, careful 1.5/6 (25%),
thorough 6/6; pair estimate 31.3; largest single hint rescues 1 of 6.

The thread's `domain: pass`, `layers: pass` (both named: target-group renames across the H1/H2 boundary, tracing-
name/catalogue-name drift, re-sent span ids, DST-sensitive boundaries as Layer 1; design-weighted SLI estimation,
per-incident root-cause onset detection, stratified CI, full-year incident-minutes reconciliation as Layer 2),
`results: 6+ across 4+ areas`, and `one_thing: none` all agree with the note's structure.

Two deltas worth recording, one of them a real finding rather than a bookkeeping note:

- **The one-fact test, recurring overclaim.** The thread's `one_fact` line credits "weight each kept span by its
  trace root's hourly keep share" with rescuing "the main recommendation, the December table and the excess figure
  (3 of ~6 results, roughly half)." This repeats, in a sharper form, exactly the overclaim pass 2's finding 3 flagged
  and the design note added a line to pre-empt. The note's own mechanics show the weighting fact ALONE (without R2's
  dated exclusions) leaves fares and notifications at 0.9% each and only **three** services over budget (places,
  seat-map, partner-gateway), not the five the main recommendation names — so the weighting sentence by itself does
  not rescue the main recommendation, the shares, or the excess; it only gets a hurried run to the "reasonable route
  that falls short" (SOLUTION_STEPS step 3). Correcting the thread's estimate against the note's own stated mechanics
  puts the true one-fact rescue at 0 full results (R3 goes from Missed to Partly at best, R5/R6 stay wrong), well
  under the one-third ceiling, so **H5 still passes**, but the thread's stated number should not be taken at face
  value and the recurrence (same miscount shape as pass 2, despite the note's added line) means the "AND" dependency
  needs a second, more explicit line in the note's Effort test aimed at a reviewer reading only the one_fact line.
- **A hidden factor the thread found by one look rather than the note's "modelling."** The thread's Stump power
  section states the INC-1611/INC-1619 root-cause onset detection "is visible on a simple 15-minute group-by of
  self-time once a run thinks to isolate self-time from downstream-call time... this piece is earned by a careful
  run rather than a strong differentiator," explicitly invoking the house caution that "a mechanism the rows
  visibly carry is modelled on sight." The design note's Hidden factor record lists both relevant factors ("December
  faults in one service's own handling" and "callers' workers waiting on a slow call late in an incident") as found
  by "modelling: own handling time against a load curve, a changepoint per span name" / "modelling: onset order, not
  size," and the Effort test grades R2 only "Partly" at the careful-but-hurried level. If the thread is right that a
  plain group-by (not a fitted load-curve changepoint) already separates the two contested onsets, the careful
  column may deserve "Right" on R2 for INC-1611/INC-1619 specifically, which would move the careful score from
  1.5/6 toward 2/6 (33%) — still at, not over, the one-third ceiling, so this does not flip H4's verdict on its own,
  but it is the kind of finding the client's bar prices directly ("a mechanism the rows visibly carry is modelled on
  sight... the careful column earns it"), and it narrows R2's margin over R1 for the careful solver.

No Gate H failure: no single hidden or planted thing carries the task (the weighting insight alone does not reach
the main recommendation; the two root-cause calls, the CI and the incident-minutes reconciliation are each
independent pieces of work), the swap test holds (trace sampling, SLI design-weighting and incident root-cause
attribution are the SRE/distributed-tracing domain's own machinery, not borrowed nouns), and the effort test
separates quick from thorough cleanly (quick ≤33% either way, thorough 6/6) even after the one-fact correction above.

## Stump power (Gate F)
Two separable traps, matching the design note's Hidden factor record verdicts (all "keep") and `effort.json`'s pair
estimate of 31.3: (1) the trace-root-share weighting versus the more intuitive own-hourly reweighting, a genuine
survey-design judgment a hurried-but-careful run is likely to default away from, which alone flips 3 of the 5
breaching services and the whole staffing order; (2) the two contested root-cause calls (INC-1611 on fares, not
journey-search; INC-1619 on notifications, not accounts), each requiring the run to isolate a span's own handling
time from the calls it waited on before comparing it to an incident-free load curve. The thread flags (2) as weaker
than the note implies, being visible on a simple group-by once isolated, which matches the house caution on
mechanisms the rows visibly carry; it still estimates stump power as genuine because the two root-cause calls and
the full incident-minutes reconciliation remain independent of trap (1), spreading the losses across results rather
than concentrating them in one trap.

## Findings, ranked
1. MEDIUM, recurring one-fact overclaim: the thread's `one_fact` estimate ("rescues roughly half, 3 of 6") exceeds
   what the design note's own mechanics support (the weighting fact alone gives only 3 services over budget, not
   the five the recommendation names, so it does not by itself rescue the main recommendation, the shares or the
   excess). This is the same shape pass 2's finding 3 flagged; the note's added "AND" parenthetical did not stop a
   fresh isolated thread from making the same overclaim. Author action: add one explicit sentence to the Effort
   test ("the weighting fact alone still gives only three services over budget, not five; correct rescue count is
   0 of 6 full results") so a reviewer reading only the summary line does not need to re-derive this each pass.
2. LOW-MEDIUM, effort-grade precision on R2: the thread's own stump-power note suggests the INC-1611/INC-1619
   onset detection may be earned by a careful-but-hurried run via a plain self-time group-by, rather than needing
   the fitted-load-curve changepoint the design note's Hidden factor record implies. This would move R2 from
   "Partly" to "Right" for the careful column on those two incidents specifically, nudging the careful score from
   1.5/6 to roughly 2/6 (33%) — still within H4's ceiling, not disqualifying, but worth a note in the next design
   pass if the author revisits the effort grading.
3. LOW, verification gap (not a task defect): the isolated thread did not independently rebuild the 90% confidence
   intervals (R4) this pass, and only partially reconstructed the CSV's full-year `incident_minutes_h1`/`h2`
   columns (exact match on 4 of 10 services; 16 cells off by clean 60-minute multiples the thread attributes to its
   own ad-hoc DST handling, not a golden defect). Author action: re-verify the full-year incident-minutes
   reconciliation and the stratified-linearisation CI directly against the generator's own code before the next
   status change; nothing found this pass contradicts either.
4. LOW, SOLUTION_WRONG candidate, narrative-only: FINAL_RECOMMENDATION's "own-weighted" contrast figures (fares
   0.4%, notifications 0.6%) did not reproduce to the thread's precision (it got ≈0.6-0.9% under every variant
   tried), though the qualitative conclusion (both stay under budget under that method) held throughout. This
   sits in explanatory prose, not a graded value; regenerate the two decimals from the generator directly rather
   than by hand before the next ship.

## Next action for the author
Before the next status change: (1) regenerate the CSV's `incident_minutes_h1`/`h2` columns and the
FINAL_RECOMMENDATION's own-weighted contrast decimals (0.4%/1.1%/0.6%) directly from `generator/analysis.py`'s own
computation rather than by hand, and spot-check them against this pass's partial reconstruction; (2) add one
sentence to the design note's Effort test making explicit that the weighting fact alone still yields only three
services over budget (not five), so the one-fact rescue count is 0 of 6 full results, not "roughly half"; neither
item requires touching `prompt.txt` or any input file, and no model rerun is required unless the regeneration
changes `ran_over`, the order, the shares, or the excess figure (no evidence found this pass that it would).
