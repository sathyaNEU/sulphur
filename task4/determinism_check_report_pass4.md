# determinism-check report, task4, 2026-11-10 (pass 4, architecture 10)

Note: this task folder already carries `determinism_check_report.md` (pass 1, architecture 7, order 6),
`determinism_check_report_pass2.md` (pass 2, architecture 8, order 7, not present in the folder listing at review
time but referenced by pass 3) and `determinism_check_report_pass3.md` (pass 3, architecture 9, the Fryele tractor
order). This pass is on the current, re-rooted build: architecture 10, registered 2026-11-10 per `DESIGN_NOTE.md`'s
Draw section, a Finnish municipal bus operator's 2027 battery-electric bus order for its Niittylä depot. The task
is at pipeline stage BUILD (`pipeline.json`); this run is the author-requested rehearsal ahead of stage 4.

One isolated judge thread (`general-purpose`, `model: sonnet`) was spawned against a fresh unzip of `target.zip` at
`/tmp/determinism-check-task4-1794288734/target/`, the literal `prompt.txt`, and the four graded blocks of
`submission.md` inlined in its brief, with `guidelines/determinism_judge_system_prompt.md` quoted in full. It never
opened `submission.md`, `DESIGN_NOTE.md`, `generator/`, `pipeline.json`, `runs/`, any earlier report, or
`guidelines/`. It had Bash and Read only (no Agent, no server tools). It wrote `verdict.md` in the scratch path,
which is reproduced in substance below.

## Verdict

**DETERMINISTIC**, with SOLUTION_WRONG (two write-up defects that do not touch the committed numbers a run is
graded against) and one live Gate C margin-robustness risk on block M111 that is not yet closed.

**Disposition:** **FIX_NOW**, every finding below is repairable by regenerating solution text or (for M111)
either regenerating that block's energy chain or adding an explicit tie-break convention in `DES-1`; none requires
changing what a solver would have seen if a run were already in flight, and no run has happened yet (stage BUILD).

**Stumping type:** mechanism: a mix of `method_or_model_selection` (diesel-to-kWh/km bridge vs. a naive
timetable-covariate fit; the battery-degradation curve form) and `binding_constraint` (the 705 kW / 150 kW night
feasibility check), with a data-discovery component (the electric buses' own fuel-fired heater, found in a column
of the vehicle register, not flagged); `stumping_family: analytical_non_defect`; `surface_read_dependency: no`;
`sole_data_defect: no`.

## Why

The main call (order 18 buses, the named 18 blocks, cut the priority list before M125) independently reproduces:
the judge thread rebuilt the priority-ordered qualifying set from `fleet_plan_2027.xlsx` plus the committed ask-3
yes/no list and landed on exactly the 18 named blocks, and ran its own exact interval-feasibility (LP) model of the
night window from `block_register_2026.xlsx`'s return/departure times and the connection agreement's 150 kW/bus and
705 kW/site caps, confirming the 18-block set is feasible and that adding M125 is not, under four independent
scheduling methods. That is Gate A/B/C holding on the main decision and on ask 5.

Two SOLUTION_WRONG defects, neither load-bearing against a graded figure:

1. Critical Component 1's rank list ("1, 2, 3, 4, 5, 6, 7, 8, 10") is off by one against the thread's own
   recomputation from `block_register_2026.xlsx` and the committed ask-1 figures: the correct sequence is
   "1, 2, 3, 4, 5, 6, 7, 9, 10" (M120, not a pilot block, is rank 8; M126, a pilot block, is rank 9). The 44.8 /
   49.3 / 4.5 l/100 km figures in the same component do reproduce exactly.
2. The recommendation's "about 170 kWh" shortfall for M125 does not match the thread's own exact-LP recomputation
   (about 82 kWh at the connection point under the schedule-optimal allocation that still fully serves the 18). The
   thread found "~170 kWh" reproduces only under a non-optimal earliest-deadline-first heuristic, and even there the
   shortfall splits between M125 (~157 kWh) and M140 (~15 kWh), not M125 alone.

Neither defect changes the committed decision (18 buses, that block set), so the carve-out for SOLUTION_WRONG
applies rather than NOT_DETERMINISTIC.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot diesel gap (Component 1) | 44.8 vs 49.3, gap 4.5 | 44.79 vs 49.33, gap 4.54 | Yes |
| Pilot blocks' rank among 35 short blocks | 1,2,3,4,5,6,7,**8**,10 | 1,2,3,4,5,6,7,**9**,10 | No (off by one; SOLUTION_WRONG) |
| Usable battery / limit (asks 3, 4) | 460 kWh usable, 391 kWh limit, loss 4.3% | 480 kWh quoted x (1-4.3%) = 459.4 to 460; limit 391 | Yes |
| First-winter loss band | 4.3%, band 3.8-5.0 | charging-session-derived loss 4.4-4.9% at 8-20+ months, inside the band; a naive linear fit (2.95%) falls outside | Yes |
| Night demand, 23 qualifying blocks (ask 5) | 8.7 MWh connection point, 8.0 MWh battery-side | 8,673.9 kWh / 0.92-adjusted = 8.7 MWh; battery-side 7,980 kWh = 8.0 MWh | Yes |
| Night demand, recommended 18 blocks | 6.7 MWh (inside Final Recommendation) | 6,717.4 kWh = 6.7 MWh | Yes |
| All 48 ask-2-to-ask-3 threshold mappings | 48 yes/no verdicts against 391 kWh | 0 mismatches across all 48 against the literal DES-1 4.1 rule | Yes |
| M125 shortfall under "any schedule" | "about 170 kWh" | exact-LP: ~82 kWh at the connection point; EDF heuristic: ~172.6 kWh split M125/M140; FIFO heuristic: spread across 5 blocks; aggregate check: ~70 kWh over cap | Partially (qualitative cut holds; the quoted magnitude and attribution do not) |
| 18-vs-19 feasibility cut | 18 feasible, 19 (+M125) infeasible | confirmed under all four scheduling methods tried (exact LP, least-slack/EDF, earliest-departure FIFO, aggregate total-energy) | Yes |

## Competing answers that survived

One open fork, not yet closed by a stated convention:

- **M111's margin against the 391 kWh threshold.** M111's committed design-day energy is 400 kWh, 9 kWh over the
  391 kWh qualification limit, which is inside the ±10 kWh grading tolerance stated for ask 2. The design note's
  own closure table (axis 9, SF21) asserts "no block within 7 kWh" of the limit in the golden, which is consistent
  with (barely clears) the 9 kWh the judge thread found by direct recomputation, but asserting the margin exists is
  not the same as closing the fork it creates. M111 sits at priority rank 3 in `fleet_plan_2027.xlsx`, ahead of all
  but two of the recommended 18, so it is high-impact: a run graded "correct" on M111's ask-2 energy anywhere in the
  388-390 kWh sub-band of the stated ±10 kWh tolerance would correctly read DES-1 4.1 literally and call M111 "yes,"
  contradicting the golden's "no," and would very likely change the composition (and possibly the count) of the
  final 18. This is the one place in the pack where the stated grading tolerance (±10 kWh) is wider than the
  distance between the golden figure and a decision boundary that figure feeds (9 kWh). Two defensible answers: (a)
  M111 "no," 18 buses, the named set (the golden); (b) M111 "yes" under a run graded within tolerance on ask 2, which
  shifts the qualifying set and very plausibly the final count. Not yet ruled out by any stated convention; the
  design note's SF21/axis 9 entries record the margin but do not add a tie-break rule for a block that lands inside
  the ask-2 tolerance band around 391 kWh.

No other fork survived: the semantic fork table's other 25 entries (SF1-SF26) are each closed by an asserted,
checked claim (within a stated numeric band), and the judge thread's own stress-testing of the main decision, the
diesel bridge, the degradation-curve choice and the night schedule did not surface a second live fork.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 14 (system files/placeholders: none) | Pass |
| File categories | 2 or more | 3: spreadsheet (xlsx x4), text/document (PDF x3), tabular text (CSV x7) | Pass |
| Large messy CSV, 20,000+ rows | 1 or more | 2: `depot_dispatch_log` (41,791 rows), `fuel_card_transactions` (20,721 rows) | Pass |
| Messy CSV, 10-20 printed pages | 1 or more | `workshop_orders_2024-01_2026-10.csv`, 832 rows, approx. 15.1 pages at approx. 55 lines/page | Pass |
| metadata.json names 2+ distractors, none labelled in the ZIP | required | `tyre_and_brake_costs_2025.xlsx`, `depot_electricity_invoices_2025-01_2026-10.csv` named in `metadata.json`; `grep -il distractor` across every shipped file returns nothing | Pass |
| Distractors relevant but unused, one reproduces arithmetically and a shipped fact rules it out | required | not independently re-verified by the judge thread (out of its scope); design note's "No decoy" line names the fleet plan's zone-priority column and the quotation's warranty figure as the candidates it defends against, not these two distractor files specifically. Carry-forward item, not a finding | Not independently confirmed |
| 1-3 deliverables requested, all present in the golden | required | prompt asks for "a workbook... and a few slides"; golden.zip holds exactly `niittyla_ebus_order_2027.xlsx` and `niittyla_ebus_order_2027.pptx`, 2 files | Pass |
| Asks multi-dimensional, unit + rounding stated | required | all 5 asks are 48-cell or depot-wide grids; prompt states "Diesel to 0.1 l/100 km, energies to the nearest 10 kWh, the loss to 0.1 per cent and the night's energy to 0.1 MWh" | Pass |
| Answer shape is one of the fourteen client shapes | required | "a schedule under capacity" (design note's Draw line): a priority list cut by a capacity constraint, with per-block results each checkable | Pass |
| Golden ZIP holds exactly the requested files in requested formats | required | 2 files, xlsx + pptx, matching the prompt's "a workbook... and slides" | Pass |
| Nothing reads LLM-generated; every golden reads as a real work product | required | judge thread found no README, no authoring/benchmark language, no uniform-tidy tells; dates and provenance internally consistent with the fiction | Pass |

## Gate G reconciliation

The judge thread's classification (mechanism: mixed `method_or_model_selection` + `binding_constraint` with a
data-discovery component; `surface_read_dependency: no`; `sole_data_defect: no`) matches the design note's own
account closely. The design note's Draw/Deep-reasoning section names the same four independent judgments as the
thread independently found: the diesel bridge (a selection-on-observables correction, `method_or_model_selection`),
the fuel heaters' share (data discovery: a load the pilot's own meter never saw, read from a second record), the
degradation-curve form (`method_or_model_selection`/validation), and the night's capacity (`binding_constraint`).
Neither the design note nor the thread found a planted defect, a rule-application shortcut, or a single hidden
factor; both independently reached `sole_data_defect: no` by reasoning that the clean-data test would still leave
a bridge-regression choice, a curve-form choice and a scheduling-feasibility problem in place. No daylight between
the two on Gate G.

## Gate H reconciliation

- **H1 (domain).** The thread passed the swap test on its own initiative, calling the domain load-bearing (kWh,
  150/705 kW caps, battery degradation, diesel l/100 km). Matches the design note's own swap sentence (the clinic/
  nurses substitution, which the note says "loses the fuel-card statement... the count stops making sense").
- **H3 (not one thing).** The design note's `one_thing` posture is `none`: the Not-one-thing paragraph states a run
  that nails the bridge alone still orders 20, a run that nails the heaters alone orders 19, verdicts summed without
  the night order 23, and only all of them together land 18. The thread's independent read agrees: its own
  careful-but-hurried table shows a run missing different subsets of {the bridge, the heater heat, the degradation
  curve, the charging efficiency / scheduling} landing on distinct wrong totals, not a single flip. No finding here.
- **H4, effort grades.** The design note's effort table: quick pass 0.5 of 8, careful-but-hurried 2.5 of 8, thorough
  8 of 8 (`effort.py` pair estimate 36.0). The thread's own independent per-result table (not shown the design note)
  put the careful-but-hurried pass at roughly 25-35% of the rubric (recommendation + components ~38 pts at 20-30%
  credit; the five asks ~55 pts at 25-35% credit; instruction-following ~7 pts earned in full), which translates to
  something close to 2-3 of 8 results earned outright plus partial credit on 2 more (R1, R2 partly-to-right; R4
  partly), consistent with, and if anything slightly more generous than, the design note's 2.5 of 8. Both are
  comfortably under the one-third ceiling and both show clear separation between a quick pass and a careful-hurried
  one; H4 holds on both readings.
- **H5, the one-fact test.** The design note names its largest single hint as the pilot-selection sentence
  ("the pilot blocks were chosen for their low diesel use, and the diesel figures carry the difficulty the
  timetable's kilometres, climb and speed miss"), claiming it rescues exactly 1 of 8 results (R2, moving the order
  to 20). The thread, working blind to this, independently proposed a *different* candidate sentence (the heaters'
  one: "the 2027 model has no fuel heater, so design-day energy must add back the heat the pilot buses' own fuel
  heaters supplied") and estimated it rescues "at most 2-3 of the 8 graded results." Both land under the
  one-third ceiling (2.67 of 8), so neither breaks H5 on its own terms, but the thread's estimate is real, measured
  evidence that the true one-fact ceiling for this pack may sit nearer 2-3 of 8 than the design note's claimed 1 of
  8, worth re-checking with `effort.py` on the heaters' hint specifically rather than taking either figure as
  settled, since it is the margin the client's bar is built around.
- **No Gate H failure.** Domain passes, both layers are named and real, no one-thing flip, effort separates cleanly,
  one-fact stays under the ceiling by both measures.

## Stump power (Gate F)

Independently estimated by the judge thread at roughly 25-35% of the rubric for a careful-but-hurried strong model,
comfortably under the 60% bar, with losses concentrated on: (c) missing the electric buses' own fuel-fired cabin
heater (a quiet vehicle-register column, not flagged anywhere as relevant), likely MISSED; (e) the first-winter
battery loss, a hurried run's textbook first move (a straight line in age) sits at 2.95%, outside the stated
3.8-5.0% band, likely MISSED; (g) the night demand, likely MISSED if the 0.92 charging efficiency is dropped or
the qualifying set from (f) carries forward wrong; (h) the final count and block set, likely MISSED, requiring (c),
(e) and the efficiency factor all correct plus an interval-feasibility (not aggregate) check. (a) the 48 diesel
rates and (b) the pilot's diesel gap are the two results a careful-but-hurried run is most likely to get right or
partly right. This spread (not one trap) is the evidence the design note's "Not one thing" and "Run forecast" rows
already predict (R1 and R5 earned on the careful pass; R2, R3, R4, R6, R7 lost; R8 Partly), the judge's blind
estimate and the design note's own effort table converge on the same shape without having seen each other.

## Findings, ranked

1. **(FIX_NOW, write-up)** Critical Component 1's rank sequence is off by one; the correct sequence is
   "1, 2, 3, 4, 5, 6, 7, 9, 10," not "...8, 10." Fix: regenerate the sentence from the generator's own rank
   computation.
2. **(FIX_NOW, write-up, needs author verification first)** The Final Recommendation's "about 170 kWh" shortfall for
   M125 does not match the judge thread's independent exact-LP recomputation (~82 kWh). Before rewording, the author
   should re-run `checks.py`'s own feasibility assertion (SF22/SF23, the "exact flow" cut) against the thread's LP
   model to determine which figure is right: either the generator's exact-flow check has a bug (e.g. a sequencing or
   per-bus-window constraint the thread's independent LP did not reproduce), or the recommendation text is quoting a
   heuristic (EDF) figure under the "exact flow" label by mistake. The qualitative cut (18 feasible, 19 not) is not
   in question; only the magnitude and the single-block attribution are.
3. **(SEND_BACK-adjacent but not yet triggered, open Gate C fork)** M111's design-day energy (400 kWh) sits 9 kWh
   from the 391 kWh threshold, inside the stated ±10 kWh ask-2 tolerance, and M111 is priority rank 3 (high-impact
   on the final set). No stated convention closes this; it should be closed before the pack goes to the platform,
   either by regenerating M111's underlying diesel/energy chain so it clears the threshold by a safer margin, or by
   adding an explicit DES-1 or fork-table convention for a block whose ask-2 energy lands inside its own grading
   tolerance band around 391 kWh.
4. **(informational)** The design note's claimed one-fact ceiling (1 of 8, the pilot-selection sentence) and the
   judge thread's independently estimated ceiling (2-3 of 8, the heaters' sentence) do not fully agree. Neither
   breaks H5, but the gap is worth closing with `effort.py` run specifically on the heaters' hint before relying on
   the design note's 1-of-8 figure as settled.
5. **(carry-forward, not independently checked this pass)** The "each distractor reproduces arithmetically and a
   shipped fact rules it out" sub-requirement for `tyre_and_brake_costs_2025.xlsx` and
   `depot_electricity_invoices_2025-01_2026-10.csv` was outside the judge thread's scope (it was not asked to probe
   the distractors) and was not separately re-derived by this reviewer; it is a carry-forward item for a future pass
   or the leak reader, not a finding against this pass.

## Next action for the author

Fix, in the generator, (1) the Critical Component 1 rank sequence, (2) the M125 shortfall figure (after resolving
whether `checks.py`'s exact-flow assertion or the recommendation text is the one with the error), and (3) add an
explicit tie-break/closure sentence for M111's margin against the 391 kWh threshold (or regenerate its energy chain
with a safer margin) before this pack is taken to stage 4 for the leak reader and a re-judge; none of these three
requires changing `target.zip` in a way that would invalidate a prior run, since no platform run exists yet for
this architecture.
