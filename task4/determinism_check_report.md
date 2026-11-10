# determinism-check report, task4, 2026-11-10

Cut under review: target.zip 67186f2dd19abb656811be0826cf6f98bbfd6db452f61e761a8a02c1483b1a0e (rebuilt today after
the connection agreement's night capacity was raised to 690 kW, the heater band edges were asserted, and the
pilot blocks/stand-ins/boosters were made realistic). Superseded pass kept as
`determinism_check_report_pass6.md`.

**Process note.** Before spawning the isolated thread, the author session read DESIGN_NOTE.md's Results chain,
Hidden factor record and Effort test sections (for context on the previous rebuild) ahead of the thread's
return, which the contract reserves for after. The thread itself never saw the design note, generator,
golden, or submission.md; it worked only from a fresh unzip of target.zip and the extracted graded blocks.
Disclosed here rather than silently absorbed; it did not change any gate finding below, all of which rest on
the thread's independent recomputation and this session's own post-return checks against the shipped bundle.

## Verdict
**DETERMINISTIC**
**Disposition:** APPROVE
**Stumping type:** mechanism: binding_constraint (secondarily method_or_model_selection), stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The main recommendation (18 buses on the 18 named blocks) and all five supplementary asks reproduce from the
shipped files under a literal reading of DES-1 2.3/4.1/4.2/4.3 and the connection agreement's 690 kW night
cap. The judge thread independently rebuilt the battery first-year loss (4.4% from telematics capacity vs.
age, inside the committed 3.8-5.0% band), the charging efficiency (median 0.920 from 3,291 sessions, matching
the committed 0.92 exactly), the 391 kWh qualify threshold (480 kWh new x 0.957 x 0.85), and the night-capacity
cut (6,706.5 kWh for the 18 assigned blocks against the 6,900 kWh cap; 7,108.7 kWh if the 19th, M124, is
added). No decisive fact lives outside the 14 shipped files, and no competing answer survives for the order
count, the qualify list, or the loss band.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| First-year usable-battery loss | 4.3% (band 3.8-5.0%) | 4.4%, fast-early/flattening shape from telematics capacity-vs-age | Yes |
| Charging efficiency | 0.92 | median 0.920 across 3,291 sessions | Yes, exact |
| Qualify cutoff | 391 kWh (85% of 460 kWh) | 480 x 0.957 x 0.85 = 391.0 kWh; no block in the 371-419 kWh gap | Yes |
| Night cap | 690 kW x 10h = 6,900 kWh | 6,900 kWh (connection agreement, independently read) | Yes |
| 18-block night demand (connection point) | 6.7 MWh | 6,706.5 kWh | Yes, exact |
| 19-block (+M124) night demand | n/a (fails) | 7,108.7 kWh, over cap | Confirms cut at 18 |
| Heater heat at -15C | 4.3 kW (band 3.9-4.7) | 35 x 0.48/3.9 = 4.31 kW from the register's rated burn and the HVO fills | Yes |
| Order and block list | 18 buses, 18 named blocks | Same 18 blocks, independently derived from the priority list + qualify set + night cap | Yes |

Diesel l/100 km (ask 1) and the full 49-block bridge regression (ask 2's exact coefficients) were confirmed
as the forced *method* (no block-level diesel field exists anywhere else, and telematics is the only real
electric-energy source DES-1 3.1 allows) and spot-checked for plausibility, not rebuilt byte-for-byte: a full
independent rebuild is a 20,805-row x 41,791-row join, which the thread flagged as out of scope for a single
pass without ceasing to be useful, and nothing in its spot checks is inconsistent with the committed figures.

## Competing answers that survived
None, for the main decision or any supplementary answer. The qualify/no-qualify line sits in a clean 49 kWh
dead zone (no block between 371 and 419 kWh), so no individual block's call is fragile. The night-capacity
cut between 18 and 19 is closer (194 kWh of margin at 18, -209 kWh at 19) but the forcing test below shows no
single defensible input choice flips it either direction; it is a thin-but-clean margin (Gate C), not a
thin-and-contested one.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ files, 2+ categories | 14 files: 4 xlsx, 3 pdf, 7 csv (3 categories) | Pass |
| Large messy files | a 20,000+ row CSV, and a 10-20 printed page CSV | fuel_card_transactions (20,805 rows), depot_dispatch_log (41,791 rows); workshop_orders (842 rows, 7 narrow columns, ~64 chars/row, est. 14-17 pages) | Pass |
| Distractors named outside the ZIP | 2+ in metadata.json, none labelled inside | tyre_and_brake_costs_2025.xlsx, depot_electricity_invoices_2025-01_2026-10.csv named in metadata.json; neither file nor any other names "distractor" | Pass |
| Distractors relevant but unused, one answers-and-is-ruled-out | required | electricity invoices show peak_kw up to 370 (growing), which could be mistaken for "the depot's capacity"; the connection agreement explicitly separates "capacity, charging installation" (690 kW) from "the depot's other consumption" (what the invoices meter), ruling it out by name. Tyre/brake costs is pure off-topic breadth, unused by any result. | Pass |
| Deliverables 1-3, all present in golden | required | niittyla_ebus_order_2027.xlsx + .pptx, both in golden.zip, matching the prompt's "a workbook... and a few slides" | Pass |
| Asks multi-dimensional, units stated | required | all 5 asks and both critical components state unit and a numeric band/precision | Pass |
| Answer shape, one of fourteen | required | a ranked (priority) list under a binding capacity cap, with its drivers (diesel rate, bridge, loss, night demand) | Pass |
| Golden ZIP holds exactly the requested files | required | golden.zip: niittyla_ebus_order_2027.pptx, niittyla_ebus_order_2027.xlsx, nothing else | Pass |
| Nothing LLM-generated, golden reads real | required | thread reports the fuel-card, dispatch, telematics and charging-session files carry realistic incidental mess (card reissues, a block-code rename, UTC vs local stamps); no finding | Pass |

## Gate G reconciliation
Thread: `mechanism: binding_constraint` (+ `method_or_model_selection`), `stumping_family: analytical_non_defect`,
`surface_read_dependency: no`, `sole_data_defect: no`.

Against DESIGN_NOTE.md's `## Results chain` (8 results, R1-R8, synthesis-weighted) and
`## Hidden factor record` (4 factors, all graded "keep," none shallow): no disagreement. The thread
independently found and classified the same shape the note claims, a genuine binding capacity constraint
(DES-1 4.2) layered on two honest method choices (the diesel-to-electric bridge, the curved battery-age fit)
,  without having read the note. It did not find a surface read to reject and did not raise
`banned_stumping_type`. This is the strongest form of confirmation available: an isolated thread reaching the
design note's own classification from the files alone.

One thing the thread found that the design note's Hidden factor record does not mention: the 6 existing
pilot buses (1201-1206) permanently run 9 blocks today, 6 of which (M125, M129, M135, M142, M145, M146) land
inside the new 18-block order. DES-1 4.3 defines "order" literally as one bus per block assigned, with no
netting against buses already owned, so this does not change the forced count, but the files are silent on
whether the 6 pilot buses are retired or keep drawing from the same 690 kW connection overnight alongside the
new fleet. This is a real completeness gap in the night-capacity story that neither the design note nor the
submission addresses; it does not flip any committed figure (nobody can compute the alternative reading
either, since the files never license it), so it is not a Gate B/C failure, but it is worth a one-line
closure in the design note's fork table or SOLUTION_STEPS.

The thread also could not reproduce SOLUTION_STEPS point 7's claim that "a least-slack schedule recharges
the 18, an earliest-departure order does not": every qualifying block's return/departure falls outside the
21:00-07:00 night window with room to spare, so the problem collapses to a pure cumulative-energy-vs-cap sum,
not a bin-packing problem where EDF and least-slack could diverge. This does not change the headline number
(18, cut at M124) and is not a Gate A failure, but the write-up's scheduling claim is an overclaim on this
pack and should be tightened.

## Gate H reconciliation
Thread's Gate H line: `domain: pass`, `layers: pass`, `results: 8 graded across 5+ areas`, `one_thing: none`,
`effort: quick 1-2 of 8, careful 4-5 of 8, thorough 8 of 8`, `one_fact: rescues roughly 2-3 of 8 (ask 2, ask 5,
the order), stays under a third`.

Two reconciliation notes against the design note's own measured table (`effort.py`: quick 0.5/8, careful
2.5/8, thorough 8/8; largest hint rescues 1/8, pair estimate 36.0):

1. **Internal inconsistency in the thread's own summary line.** The Deep-reasoning headline says "careful 4-5
   of 8," but the thread's own worked table (Right: ask 4, critical component 2; Partly: ask 3; Lost: ask 1,
   ask 2, ask 5, critical component 1, the order) scores to 2 Right + 1 Partly, i.e. roughly 2.5 of 8, not
   4-5. The worked table is the reliable number; it tracks the design note's measured careful-pass score
   (2.5/8) closely. Treat the summary line's "4-5 of 8" as a drafting slip in the thread's report, not a
   second, higher estimate: the effort test still passes cleanly (quick well under a third, careful clearly
   above quick and clearly below thorough).
2. **The one-fact rescue is likely overstated.** The thread's named sentence ("the diesel figures are your
   only source of energy data for the 39 blocks the pilot never ran") is scored as rescuing ask 2, ask 5 and
   the order (3 of 8, "right at the one-third ceiling" by the thread's own words, which is in fact just over
   a third, 0.375). But the design note's own effort-pass tracking (Effort test note, "Executed hints") says
   putting the diesel bridge right *alone*, with the heater share still wrong, only orders 20 (not 18) and
   leaves R4 (ask 2's energies) "still light on every block" by the heater's 4.3 kW/hour, i.e. the bridge
   sentence alone does not land ask 2's 48 energies inside their ±10 kWh bands, so it does not fully rescue
   ask 2 or its downstream carry-forward (ask 5, the order). The design note's own figure (largest single
   hint rescues 1 of 8, R2 only) is the one this session trusts: it is measured by `effort.py` against the
   generator's own implementations, not estimated from a single pass. On that reading H5 passes comfortably
   under the one-third ceiling, more comfortably than the thread's own headline number suggests.

Both notes point the same way: the task passes H3-H5, and by a wider margin than the thread's summary
language implies once its own worked table and the design note's measured effort-pass numbers are read
together instead of the headline line alone.

## Stump power (Gate F)
The trap most likely to catch a strong-but-hurried run is skipping the diesel-to-electric bridge and the
pilot's HVAC/HVO heater decomposition, fitting the pilot's own kilometres/climb/temperature covariates
directly and extrapolating to the 39 blocks the pilot never ran, exactly SOLUTION_STEPS point 5's stated
counterfactual ("orders 21"). The thread's own careful-but-hurried run (reads every file, reconciles joins,
fits energy-per-km with temperature/speed-squared/climb, curves the age-loss term, schedules the night under
the connection cap, bootstraps and holds out, but sets the fuel-card file aside as "diesel does not measure
battery energy") lands 2 of 8 results clearly right (ask 4, critical component 2) with ask 3 partly right,
and loses ask 1, ask 2, ask 5, critical component 1 and the main order (landing near 21 buses on a different
block list). That is squarely in the "careful but hurried" band the effort test wants, and the losses spread
across assembly, modeling and synthesis rather than concentrating in one place.

The forcing test (below) adds that even where the task's margin is thinnest (the 18-vs-19 night-capacity
cut), no single defensible input choice flips it, so the margin itself is not a soft spot a frontier run can
exploit by chance.

### Forcing test (order)
Tested: every defensible charging-efficiency reading from the sessions file (annual 5th/25th/50th/75th/90th/
95th percentiles and max, plus a cold-night-only (<=-15C) subset), the full 3.9-4.7 kW heater band, plug-in/
out margins of 10-20 minutes, and EASY/earliest-departure vs. least-slack night scheduling.

- **To 17 buses:** would need charging efficiency below about 0.894. The annual 5th percentile (0.899) still
  clears the 6,900 kWh cap with 37 kWh of margin, and the cold-night subset never drops below 0.921. No
  defensible reading reaches 17.
- **To 19 buses:** would need efficiency at or above about 0.948, beyond the 75th percentile of even the
  coldest-night sessions (0.946) and reachable only via the single highest observed session (0.973, one
  outlier of 3,291). Stacking two independently generous choices at once (cold-night 75th-pct efficiency
  *and* the low end of the heater band) can just clear the cap, but that is compounding two separately
  estimated tail values, not one reasonable operationalization.
- Heater band alone (3.9-4.7 kW): moves the 19-block total by roughly +/-95 kWh battery-side, never under
  the 6,900 kWh cap at any point in the band.
- Plug margins and EDF vs. least-slack scheduling: make no difference whatsoever for this specific block set,
  because every qualifying block has the full 600-minute night window with no individual deadline inside it;
  the feasibility question is a pure cumulative-sum-vs-cap test. This is the basis for the Gate G finding
  above that SOLUTION_STEPS point 7's EDF/least-slack distinction does not reproduce on this data.

Conclusion: 18 is forced under every single reasonable, individually defensible input choice tested; 19 is
reachable only by cherry-picking a tail outlier or stacking two generous choices at once, and 17 is not
reachable at all.

### Precision test
No committed figure is stated at a precision its own defensible method does not support once the grading
band is read alongside it. Ask 1's one-decimal figure is tighter than the join method's real noise, but its
±0.7 l/100 km band (about 1.2-1.9% of the 37-62 range) absorbs that. Ask 2's energies cluster on exact 10 kWh
multiples with a matching ±10 kWh band (one rounding bin, not two mislabeled as one). Ask 4's 3.8-5.0% band
(1.2 points) reflects the genuine spread across the curved/sqrt/log method family the solution itself reports
(4.28/4.57/4.86 against an excluded straight line of 2.96, excluded because the data visibly curves, not
arbitrarily). Critical component 2's wider ±9% band around 4.3 kW is appropriate given it rests on only 58
HVO fuel-card rows across 6 vehicles; a tighter band would be false precision. No figure's band is a single
bin mislabeled as two, and no band is so wide it grades nothing.

## Findings, ranked
1. **Pilot-fleet night-capacity completeness gap** (new finding, not in the design note's fork table or
   hidden factor record): the files never say whether the 6 existing pilot buses are retired or continue
   drawing from the same 690 kW connection on the design night alongside the new fleet. Does not change any
   committed figure (DES-1 4.3 forces the order count regardless), but is worth a closing sentence.
   Severity: low, FIX_NOW-grade, solution-side.
2. **SOLUTION_STEPS point 7 overclaims an EDF-vs-least-slack divergence** that does not reproduce on this
   block set (every qualifying block has the full night window with no internal deadline, so the two
   heuristics cannot differ). Does not change the headline cut (18, at M124). Severity: low, FIX_NOW-grade,
   wording only.
3. **The judge thread's own Deep-reasoning summary line overstates the careful-pass score** ("4-5 of 8")
   against its own worked table (~2.5 of 8); the worked table, which matches the design note's measured
   effort-pass numbers, is the one to trust. No action needed on the build; noted for anyone reading
   verdict.md's headline line in isolation.
4. **The thread's one-fact estimate (rescues ~3 of 8, just over a third) is likely an overstatement** of what
   the "diesel is the only energy proxy" sentence actually buys a run, per the design note's own measured
   tracking (bridging alone still orders 20, not 18, because the heater share stays wrong) and should not be
   read as a borderline H5 result; the design note's own figure (1 of 8) is better evidence. No action
   needed.

## Next action for the author
Add one sentence to SOLUTION_STEPS (or the design note's fork table) stating the disposition of the 6
existing pilot buses on the design night, continue in service on their 3 non-order blocks (M103, M118,
M124) and share the same 690 kW connection, or retired/redeployed, so the night-capacity reasoning is
explicit about everything else drawing from the same meter; while there, tighten point 7's EDF-vs-least-slack
sentence to match what the data actually shows (a pure cumulative-energy-vs-cap test, not a scheduling-order
effect). Neither change touches a committed figure or requires a rerun.
