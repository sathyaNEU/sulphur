# determinism-check report, task6, 2026-11-08

## Verdict
NOT_DETERMINISTIC as judged (ask 5 only; asks 1 to 4 and the CSV DETERMINISTIC). No SOLUTION_WRONG. The judged text was the prompt before the wording fix; the three findings are assessed below against prompt.txt as now shipped.
**Disposition:** judged SEND_BACK (narrow). After the prompt wording, final disposition APPROVE (all three findings closed on a literal reading; the new text was not re-judged by a thread, one pass only).
**Stumping type:** mechanism: method_or_model_selection (design-based weighting of a trace-sampled store), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
Every graded figure recomputes from the bundle. The own-hour rival (four services, places first, 62%, 160,000) is ruled out by named data (flat edge roots per hour, edge-weighted spans reconcile to LB hourly counts, partner-gateway kept spans correlate 0.12 with its RequestCount). Ask 5 held only under two unstated conventions (when an incident names a service; the unit of minutes), and the joint share did not name its base. The prompt now pins all three.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| SLIs (JS, fares, places, seat-map, booking, payments, tickets, accounts, PG, notifications) | 1.3, 0.6, 1.5, 1.5, 0.4, 0.3, 0.6, 0.7, 2.9, 1.6 | 1.323, 0.586, 1.496, 1.476, 0.368, 0.309, 0.589, 0.669, 2.898, 1.612 | yes |
| Shares, start order | PG 40, places 31, JS 16, seat-map 2, notif 1 | 40.33, 30.91, 15.74, 2.37, 0.78 | yes |
| Joint share | 90% | 90.12% | yes |
| Beyond budget | 300,000 | 300,831 | yes |
| Incident minutes H1 / H2 | 1,545 / 907 | 1,544.82 / 907.03 | yes, under the timeline-add reading |
| Own-hour rival | 1.4%, 62%, 160,000 | 1.44, 62.2%, 164,856 | yes |
| Caller mix, CC2 | 85/33, 12/33, 4/34 | 84.7, 11.6, 3.7 (kept 33/33/34) | yes |

## Competing answers that survived (judged text, then status against shipped prompt)
- Ask 5 naming moment: timeline "service added" 1,545/907 vs incidents_2026.csv services column (declaration) 1,571/1,067. CLOSED by "a service counting from when the incident tool added it" (timeline.csv event is literally "service added"; PR-SLO-3 5.2 "named it ... at the time"). Residual LOW: a service added after the status page cleared (INC-1494, places) contributes 0 minutes; this follows from 5.2's interval ending at the status page, not from a stated sentence.
- Ask 5 unit: summed duration 1,545/907 vs distinct clock minutes touched 1,553/911. CLOSED by "for how long" and "time in whole minutes ... rounded once at the end" (a duration, not a bucket count).
- Joint share base: 90% of all services' over-threshold requests vs 74% of all December requests. CLOSED by "what share of those requests", antecedent "all our services' over-threshold December requests". Residual LOW: "those" sits a clause after the antecedent but no other noun phrase competes.
- Start order, per-service shares, beyond-budget, SLIs: no defensible reading lands outside the bin. Five-only denominator (45/34/17/3/1) is contradicted by "all our services'". Dedupe or not: same rounded figures. Coarser weight grain (day, month): PG 1.78/1.68, excluded by PR-SLO-3 2.4 (hour) and the hourly LB file.
- GET /healthz kept: PG 2.76, beyond budget 250,466 (outside bin). Closed by PR-SLO-3 2.2 (health probes are not requests) plus span name. LOW, texture, inferred link.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files, categories | 10+, 2+ | 15; csv, xlsx, parquet, json, docx, md | yes |
| Large messy CSVs | 20,000+ rows; one 10 to 20 pages+ | lb H2 44,160 rows; incident_timeline 535 rows (about 11 pages), billing 7,858 | yes (timeline is the thin one, borderline) |
| metadata distractors | 2+, none labelled in ZIP | 8 named; no labels in zip | yes |
| Distractors unused, relevant | yes | H1 LB, billing, deployments etc.; judge found none answering a graded quantity | yes |
| Deliverables | 1 to 3, all in golden | 2 (docx, csv); golden.zip holds exactly those | yes |
| Asks multi-dimensional, unit and rounding stated | yes | per-service grid, table, chart, shares, minutes per half; rounding sentence covers all | yes |
| Answer shape | gradable cells downstream of deep step | per-service grid of 10 SLIs, shares, ranked list | yes |
| Realism / no LLM tells | yes | no authoring language in docx text; not read beyond that | yes (not exhaustively checked) |

## Gate G reconciliation
Judge: mechanism method_or_model_selection, family analytical_non_defect, no surface-read dependency, no sole data defect. Design note's data-native sentence (edge-level whole-trace sampler, keep share recorded nowhere, recovered from the edge service's hourly LB count) matches. The surface read the judge names carrying the easy route is the own-hour reweighting, not a declared distractor (the H1 LB file is declared but unused). No mismatch.

## Stump power (Gate F)
Gate H line: domain pass, layers pass, decisive_step analytical, chain 4 inferences (trace-level sample so own-hour correction biased; trace owner mix; edge hourly weights; reconciliation to LB counts as the check), one_fact borderline ("the store keeps a flat number of whole traces per edge service per hour" helps but the roots, weights and carry-through remain). Easy route (own-hour reweighting, 1.4%, four services) is plausible for a strong solver. The new asks ride the deep step: start order, shares, joint share and beyond-budget all flip under the rival (places first, 62%, 160,000). Ask 5 (incident minutes) is independent of the deep step, a rule/semantics ask, now pinned.

## Findings, ranked
1. MEDIUM, ask 5, underspecified_objective, naming moment: CLOSED by the prompt ("counting from when the incident tool added it"). Fork-table row and checks.py assertion still owed (author-side).
2. LOW to MEDIUM, ask 5, minute unit: CLOSED ("for how long", "time in whole minutes").
3. LOW to MEDIUM, joint share base: CLOSED ("share of those requests").
4. LOW, post-clear additions (INC-1494 places) contribute 0: follows from 5.2, add a fork-table line.
5. LOW, healthz texture: no change required.

## Next action for the author
Add fork-table rows (naming moment, post-clear addition, minute unit, joint-share base) with checks.py assertions, confirm the docx golden states ask 4 and ask 5 consistently with the new prompt wording, then proceed to READY. No pack change.
