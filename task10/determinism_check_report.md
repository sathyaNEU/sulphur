# determinism-check report, task10, 2026-11-08

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: forecasting (design-day delivery projected from a temperature regression on event days) with statistical_rigor (spillover separation), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

**Pack provenance (recorded at the coordinator's request).** The judge read the pack with target.zip sha256 a3ba2ac0...b6b0 (judge unzip at /tmp/determinism-check-task10-1794165018/target/). After the verdict, two texture-only realism fixes were applied: growth-register site names carry varied plot numbers, and in the distractor primary_transformer_condition_2026.xlsx manufacture year is at or before commissioning and the health index tracks age. The shipped target.zip is now sha256 1350f12d94f40741f1601f73d9903de5df0ad7d06f9f66d03d3f2fbecbe88156. Per the coordinator, submission.md, figures.json and metadata.json are byte-identical to the judged state and checks.py (81/81), verify.py and figures_check.py pass on the rebuilt pack. I did not re-judge the rebuilt pack and did not diff it; the verdict is for the judged pack. The two changes touch neither the growth rates and connections' MW nor any file the solution uses (the transformer file is an unused distractor). generator/pack.py shows as modified in git (uncommitted).

## Why
One isolated judge thread executed the guideline literally and reproduced every committed figure from the raw files. Section 6 credits what the provider delivers per MW scheduled on the design day. The open-point topology plus the half-hourly demand at the linked primaries show part of the zone primary's fall reappearing across the open point (Tollbrook Lane +1.4, Wexley Hill +1.4, Kestwick Fields +0.8 MW; no neighbour of Charlecote Way). Netted and read at -3.0 C this gives 0.4/0.5/0.5/0.4 per MW, credits 4/4/7/3 MW, and reinforcement at Ashcombe Road and Hartwell Common. Every rival run either lands on the same call or is ruled out by named data.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Completed latest-revision events (Ash/Char/Fen/Hart) | 90/58/82/91 | 90/58/82/91 | Yes |
| Design-day demand before flexibility | 30/25/36/23 | 30.27/25.02/35.76/22.98 | Yes |
| Gross fall per MW (weather-adjusted baseline) | 0.9/0.6/0.9/0.9 | 0.86/0.61/0.89/0.91 | Yes |
| Neighbour rise on events | 1.4/1.4/0.8 | 1.37/1.42/0.83 (others about 0) | Yes |
| Netted delivery per MW at -3.0 C | 0.4/0.5/0.5/0.4 | 0.41/0.50/0.48/0.39 | Yes |
| Credit (whole MW) | 4/4/7/3 | 3.8/4.0/6.7/2.9 | Yes (Fenwick 7 via rounded 0.5, 6.7 unrounded also rounds to 7) |
| After flexibility vs firm | 26>23.0, 21<22.5, 29<30.5, 20>17.8 | same | Yes |
| Average-event-day credit (rejected route) | 6/5/9/5 | 5.9/4.9/9.0/4.5 | Yes |
| Ten-day baseline rival | files all four | all four exceed | Yes |

## Competing answers that survived
No fork survives with a different golden. One reading is worth the author's awareness: "reduction in the primary's demand" taken as the zone primary's gross fall at -3.0 C gives about 0.69/0.50/0.75/0.74 per MW, credits 7/4/10/6 MW, Ashcombe 23 against 23.0 (not exceeding in whole MW) and Hartwell 17 against 17.8, so none reinforced. It is closed by section 6 ("its provider will deliver", "no other measure") and by the data (the excess reappears at the linked primary in the same half-hours, only where an open point exists). The judge rates this deterministic but notes it is the one place a solver can be argued the other way on wording. Method variants (no winter level, 2025/26 only, start- vs end-dated half-hours, cancelled-event days, quality S rows, weather versions, superseded connections, hinge vs none) moved before-flex by about 1 MW at most and never changed the reinforce set; margins Ash +3, Hart +2.2, Fen -1.5, Char -1.5 MW.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files / categories | 10+ / 2+ | 11 / spreadsheet (5 xlsx), text (3 csv, 3 pdf) | Yes |
| Large messy CSVs | 20,000+ rows and a 10-20 page CSV | demand 196,201 rows; weather 13,372 rows (well over 20 pages printed); events 372 rows | Yes |
| Distractors in metadata.json | 2+, none labelled in ZIP | 3 (customer_interruptions, primary_transformer_condition, duos_charging); no label in ZIP, judge found no provenance leak | Yes |
| Distractor unused yet weighable | unused, ruled out by shipped fact | judge confirmed unused; I did not test that each reproduces a graded quantity arithmetically | Yes (not independently tested) |
| Deliverables | 1 to 3, all in golden | xlsx and pptx; golden.zip holds exactly those two | Yes |
| Asks multi-dimensional with unit and rounding | yes | 4 zones x 6 cells plus chart; whole MW and one decimal stated in prompt | Yes |
| Answer shape | many gradable cells downstream of deep step | scorecard, 16 cells plus call (design note: default path misses 14 of 16) | Yes |
| Realism | no LLM tells | judge: PASS, operator artifacts present; minor undocumented G/S/B flags and weather version_num, tested, move nothing. I did not open the golden files for a realism read. | Yes (judge-based) |

## Gate G reconciliation
Thread: decisive_step analytical, 5 inferences (baseline fit, neighbour rise, netting, temperature regression, credit vs firm), judgment separating provider reduction from load transferred to a neighbour and projecting to the design temperature; domain and layers pass; one_fact "part of the zone primary's fall is demand moved onto the primary across an 11 kV open point", which does not make the task routine; mechanism forecasting with statistical_rigor; stumping_family analytical_non_defect; surface_read_dependency no; sole_data_defect no.
Design note: Layer 2 estimand_identification, chain of the same five steps, judgment "separating two explanations for one pattern", Strategy label WORKS IN FORM (causal_design), default path 0.9/0.6/0.9/0.9 committing none. This matches the thread on chain, judgment, default path (0.9 gross; judge's rungs equal the note's rungs 1 to 3) and no-decoy. The declared distractors were not named as the surface read. Observation: the design note's one-fact test still quotes "the control room moved load", which the blocks no longer say after the FIX_NOW; the sentence is the author's private test, not a shipped artifact, and the thread's one_fact is the same fact in neutral words. Gate G: no shipped artifact ranks the candidates and gets it wrong (no file states a delivery, credit or ranking).
Gate H line: domain pass, layers pass, decisive_step analytical, chain 5, one_fact as above.

## Stump power (Gate F)
The thread did not class the decisive step analytical because the golden is a textbook route. It reached the golden only by adding spillover netting and the cold-day curve beyond the field's standard weather-adjusted baseline (measurement and verification), so the landable-call concern does not apply. Failure paths: the gross event fall (0.9 per MW, none reinforced), the linked primary as control (about 1.0, none), the average event day (6/5/9/5 MW, same two primaries but wrong figures), ten-day baseline (files all four). Plausibly stumps a strong model. The main thread weighs the call's survival: a run that nets and reads only the average day still lands the call and loses on every delivery and credit cell. The stump rests on data evidence and wording of section 6, not a spelled-out rule.

## Findings, ranked
1. Informational: the gross-fall reading (above) is the single argument a solver can make on wording; closed by section 6 and the data, no fix recommended (a sentence naming transfers would hand over the step).
2. Informational: G/S/B quality flags and weather version_num are undocumented; tested, no effect.
3. Process: the rebuilt pack (sha 1350f12d...) was not re-judged; relies on the coordinator's byte-identity statement for submission, figures and metadata.

## Next action for the author
Proceed to stage 5: re-run the gates on the final cut and record READY, noting that the judged target.zip hash (a3ba2ac0...) differs from the shipped one (1350f12d...) by the two texture-only fixes.
