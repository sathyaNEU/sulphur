# determinism-check report, task4, 2026-11-10

Re-judge pass after the FIX_NOW from the first judge pass (architecture 10). Single isolated judge thread
(general-purpose, sonnet, medium effort) spawned against a fresh unzip of the rebuilt `target.zip` at
`/tmp/determinism-check-task4-18142/target/` plus the extracted graded blocks only; it wrote its own
independent derivation to disk (`scratch/my_derivation.md`) before opening the graded-blocks file. It never
saw `submission.md`, `DESIGN_NOTE.md`, `generator/`, `pipeline.json`, `runs/`, any prior report, or
`guidelines/` beyond the one inlined system prompt.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (own-office verification owed, no model rerun needed)
**Stumping type:** mechanism: method_or_model_selection (primary) with a binding_constraint layer;
stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why
The thread rebuilt the chain from the 14 shipped files before reading the solution and reproduced the
headline figures independently: the pilot-block diesel average (45.3 l/100 km, Critical Component 1) fell
out exactly from its own fleet-number/dispatch-log reconstruction; the 6.6/6.85/7.8/8.5 MWh figures in ask 5
reproduce exactly from the committed design-day energies, the 0.92 efficiency and 685 kW x 10 h; an exact
(non-greedy) interval-feasibility test over the connection agreement's 21:00-07:00 window confirms the
18-block set is schedulable and that M125 (19th on the priority list) is not. All three of the previously
found FIX_NOW defects are gone on this cut: Component 1 is now stated as means and a gap, not a rank list
dependent on which blocks count as "short"; the night's shortfall is computed over the standard's own
return-to-departure windows inside the night period, with the agreement's capacity rescanned to balance the
margins; every block now sits 26 kWh or more clear of the 390.4 kWh limit in the generator's own truth
(18 kWh-plus margin stated in the committed blocks), clear of the 10 kWh grading tolerance. The one soft
ambiguity the thread found on its own ("the town's weather station," where the file carries two stations)
closes the same way the solution closes it (SOLUTION_STEPS 1), so it is not an open fork. Gate B: every
decisive fact used (block returns/departures, 150 kW/685 kW/21:00-07:00, the usable-battery definition, the
priority-order cut rule) traces to a specific shipped file (`fleet_plan_2027.xlsx`,
`charging_connection_agreement_2025.pdf`, `depot_electrification_standard_DES-1.pdf`).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot blocks' diesel average (CC1) | 45.3 l/100 km | 45.3 (own block selection, own averaging) | Yes |
| Fuel heater heat at -15C (CC2) | 3.8 kW | mechanism confirmed in one groupby (HVAC-vs-temperature kink below -11 to -13C) + 57 HVO fills; within stated 3.4-4.7 band | Yes |
| First-winter battery loss (ask 4) | 4.3% (band 3.8-5.0) | own early/late comparison on 1201-1203 gives ~4.5%, inside band; rejected straight line (2.96%) correctly sits outside it | Yes |
| 18-block night energy, grid side | 6,608.7 kWh (<= 6,850 kWh cap) | reproduced exactly; FEASIBLE under exact interval test | Yes |
| 19-block (+M125) night energy | 7,000.0 kWh (> 6,850 kWh cap) | reproduced exactly; exactly one violated interval (the full night window) | Yes |
| Night demand, 23 qualifying blocks (ask 5) | 8.5 MWh at connection point | reproduces from committed energies / 0.92 | Yes |
| Order count and block set (recommendation) | 18 buses, cut at M125 | exact feasibility, least-slack schedule, earliest-departure schedule, and the period's total energy all agree on 18, cut at M125 | Yes |

## Competing answers that survived
None closed as open forks. One flagged-but-unresolved sensitivity: the thread could not fully rule out,
from the shipped files alone, whether reading Critical Component 2's own stated band (3.4-4.7 kW heater
heat) at its low end produces enough uniform drift across all 19 near-cutoff blocks' design-day energies to
flip the cutoff from 18 (M125 first excluded) to 17 (M135 first excluded). Its own stress test found the
cutoff flips under a uniform +3.5-4.0% shift applied identically to all 19 blocks' energies, and it judged
that magnitude "roughly the same order" as the spread already inside Component 2's stated tolerance. It
explicitly did not find that this flip occurs, only that it could not rule it out without the generator's
exact formula, which is out of its scope as a text-only reviewer against the shipped files.

My own reconciliation narrows this (see Gate G/H reconciliation below): the design note's own stated check
(SF23: "the 18 hold with energies 2 per cent higher ... the 19th fits only 1.5 per cent lower") already
tests a margin inside the 3.5-4.0% flip point the thread found, and a change in the heater component alone
(as opposed to a uniform scale of *total* block energy, which is what the thread actually tested) translates
to a materially smaller shift in total design-day energy, because the heating term is a minority share of
each block's total energy (12.0 kW x hours-out is the design note's own stated 30-60 kWh of a 290-490 kWh
total). The risk the thread flags is real in shape but likely overstated in magnitude by its own
worst-case proxy (a uniform scale of *everything*, not just the heater share); it is nonetheless a legitimate
loose end that the design note does not explicitly close with a heater-low-end-only sensitivity run, and I
cannot close it myself without running the generator, which is outside my own mandate as well.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10+ (excl. system files) | 14 files, no system/placeholder files | Pass |
| File categories | 2+ | xlsx (4), pdf (3), csv (7) -- spreadsheet, document/text, tabular data | Pass |
| Large messy CSV, 20k+ rows | 1+ | fuel_card_transactions_2024-01_2026-10.csv, 20,684 rows | Pass |
| Large messy CSV, 10-20 printed pages | 1+ | depot_dispatch_log_2024-01_2026-10.csv, 41,788 rows, ~1.9MB, spans a block-code remap and a vehicle-ID format change | Pass |
| metadata.json names 2+ distractors, none labelled in ZIP | required | tyre_and_brake_costs_2025.xlsx, depot_electricity_invoices_2025-01_2026-10.csv; neither named or flagged inside target.zip | Pass |
| Each distractor relevant-but-unused; one reproduces a graded quantity and is ruled out by a shipped fact | required | Both read as plausible, on-topic, uncited in SOLUTION_STEPS (judge's own check); neither was tested by the judge as "arithmetically reproduces a graded quantity then gets ruled out" -- this specific sub-requirement is not verified either way | Not verified |
| 1-3 deliverables, all present in golden, no forced format family | required | 2 deliverables (niittyla_ebus_order_2027.xlsx, niittyla_ebus_order_2027.pptx), both present in golden.zip, matching metadata.json | Pass |
| Asks multi-dimensional, unit + rounding stated | required | all 5 supplementary asks carry explicit unit and rounding (0.1 l/100km, 10 kWh, 0.1%, 0.1 MWh); each is a 48-cell or multi-block computation | Pass |
| Answer shape is one of the 14, 4+ checkable results | required | "a schedule under capacity"; 8 graded results per the results chain (R1-R8), each independently checkable | Pass |
| Golden ZIP holds exactly the requested files, requested formats | required | golden.zip: niittyla_ebus_order_2027.xlsx + niittyla_ebus_order_2027.pptx, matching the prompt's "a workbook... and a few slides" and metadata.json's deliverables list exactly | Pass |
| Nothing LLM-generated; golden reads as real work product | required | judge found no LLM tells, no provenance leakage in files it opened; provenance in metadata.json is a constructed-generator disclosure outside the ZIP (compliant) | Pass |

## Gate G reconciliation
Judge: `mechanism: method_or_model_selection` (primary) with a `binding_constraint` layer on top,
`stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.

Design note's strategy label: "WORKS IN FORM (a forecast carried from a selected sample to the population
through the old technology's own record, beside a measurement gap read from a second record and a capacity
constraint over the forecasts)." These describe the same shape from two independent angles: the judge names
the two FINE-numbers levers (model/method selection for the energy bridge and the fade-curve form; a binding
capacity constraint for the night), the design note names the mechanism (selection-on-observables, a
measurement gap, a shared capacity). Neither identifies a surface-read-rejection or a planted defect as the
primary stump. No reconciliation gap.

## Gate H reconciliation
Judge's Gate H line: `domain: pass`, `layers: pass`, `results: 8 graded across 5 areas`, `one_thing: none`,
`effort: quick ~1-2 of 8, careful-but-hurried ~2-3 of 8, thorough 8 of 8`, `one_fact: "the pilot ran the
easiest nine blocks and kept a fuel heater the ordered bus won't have" rescues about 3 of 8`.

Design note's own numbers (Results chain, 8 rows = R1-R8; Hidden factor record, 4 rows, all "keep"; Effort
test table): quick 0.5 of 8, careful-but-hurried 2.5 of 8, thorough 8 of 8; largest single hint rescues 1 of
8 (R2 alone, orders 20); the heaters' sentence separately rescues 1 of 8 (R3 alone, orders 19); the night's
sentence rescues 0.

Three points of reconciliation:
1. **Effort grades**: judge's quick (~1-2/8 ~ 12-25%) and careful-but-hurried (~2-3/8 ~ 25-37.5%) estimates
   sit within rounding of the design note's 0.5/8 (6%) and 2.5/8 (31%). No daylight here; both place the
   careful-but-hurried pass well under a third to just over a third, consistent with the client's effort test.
2. **One-fact test, a real discrepancy worth flagging**: the design note's own hint table treats the
   selection-on-observables fact and the fuel-heater fact as *two separate* sentences, each individually
   rescuing 1 of 8 (12.5%), well inside the "no more than about a third" bar. The judge's "one fact" instead
   conjoins both into a single compound sentence ("the pilot ran the easiest nine blocks *and* kept a fuel
   heater...") and credits that compound sentence with rescuing about 3 of 8 (37.5%), which is at or just
   over the H5 threshold. This is a bookkeeping difference, not a new finding: the design note's own
   discipline (one atomic fact per entry) is the correct test, and on that discipline no single sentence
   rescues more than 1 of 8. I flag it because the house's own reconciliation heuristic ("the thread's best
   single sentence rescues more results than the note's Largest single hint says") is literally triggered
   here, and the design note should make explicit, in one line, that its one-fact test is over atomic facts
   and that no compound sentence should be read as satisfying H5 on its own merged claim. This is a
   documentation precision item, not a basis to change the disposition.
3. **No one_thing finding**: both the judge and the design note agree no single hidden or planted factor
   carries most of the 8 results; the judge independently named four separately-checkable pieces of work
   (diesel bridge, heater decomposition, fade curve, night constraint), matching the design note's own four
   "keep" rows in the hidden factor record.

No finding here rises to the level the contract's send-back predictors describe (no single hidden/planted
thing carries most results; no hidden factor sits only in the deciding units per the hidden factor record's
own "no" column, confirmed independently by the judge's groupby read; effort grades track the note's table;
no band excludes a defensible rival the judge actually ran, except the one open margin question in Part B
above, which the judge itself treats as unresolved rather than as a Gate C failure).

## Stump power (Gate F)
Two stacked honest-data traps, matching the design note's "four independent judgments" framing: (1) a naive
energy model (scheduled km times a timetable-covariate fit, or the pilot's raw cold-weather draw applied
directly) is wrong in a way the data itself shows (the pilot ran an easier-than-average, selected subset of
blocks, and used a fuel heater the ordered model will not have); (2) even with the energy model right, a
solver who orders every block that individually clears the 85% threshold (23 blocks) misses the binding
night-charging constraint and over-orders by 5 buses. Judge's careful-but-hurried rubric-share estimate:
roughly 25-40%, comfortably under the 60% bar, with the recommendation itself (the final count and block
set) the single most likely total loss -- a careful-but-hurried run is likeliest to recommend 23 (or a
near relative, 19-21) rather than 18 with M125 named as the first cut.

## Findings, ranked
1. **Open but unresolved margin question (Part B)**: whether Critical Component 2's own stated band
   (3.4-4.7 kW), read at its low end and propagated honestly through the design-day-energy formula, could
   shift the night-charging cutoff from 18 (M125 first excluded) to 17 (M135 first excluded). The judge's own
   worst-case proxy (a uniform scale of total block energy) finds the flip point at +3.5-4.0%; my own
   reconciliation against the design note's SF23 (2% margin tested, holds) and the fact that the heater term
   is a minority share of total block energy (30-60 kWh of 290-490 kWh) suggests the actual sensitivity from
   Component 2's band alone is smaller than the judge's proxy, but this is not independently confirmed by
   running the generator. **This is the one item I recommend verifying before READY.**
2. **One-fact test bookkeeping**: the judge's compound "one fact" (two atomic facts conjoined) rescues ~3/8,
   at or above the one-third bar, while the design note's own atomic-fact table stays at 1/8 per fact. Not a
   send-back trigger on its own, but worth a one-line clarification in the design note's effort section.
3. All three defects named in the first judge pass (Component 1's rank-list dependency, the night shortfall's
   plug-in-margin dependency, the near-limit block) are confirmed closed on this cut; no new Gate A-E defect
   was found.

## Next action for the author
Before READY: run (or have the generator confirm via `effort.py`/`figures.json`) a sensitivity pass that
varies only Critical Component 2's heater-heat term across its own stated 3.4-4.7 kW band (holding every
other input at its committed value) and confirm the night-charging cutoff stays at 18 buses with M125 first
excluded across the whole band; record the result as one line in the design note's fork or closure table
(an SF entry alongside SF23). If it does flip within the band, narrow Component 2's graded band to the
sub-range that does not flip the recommendation, or state in the design note why the low end does not
propagate that far (e.g., a floor or damping elsewhere in the energy formula). No other fix is required; the
task is otherwise DETERMINISTIC, passes Gate G, and the Gate H standards (not one thing, difficulty
throughout, effort test, one-fact test on an atomic reading) are met.
