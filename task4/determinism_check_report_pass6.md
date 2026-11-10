# determinism-check report, task4, 2026-11-10

Pass on the rebuilt final cut (architecture 10): the pilot's blocks and stand-ins, the connection agreement's
capacity, the fleet plan's outlet count and the quotation's order range all changed since pass 5. One isolated
judge thread (general-purpose, sonnet, medium effort) ran against a fresh unzip of `target.zip` at
`/tmp/determinism-check-task4-1794292150/target/`, the prompt inlined, and the four graded blocks in a
scratch-only file it opened only after writing its own from-scratch derivation
(`/tmp/determinism-check-task4-1794292150/my_derivation.md`). It never saw `submission.md`, `DESIGN_NOTE.md`,
`generator/`, `pipeline.json`, `runs/`, any earlier report, or `guidelines/`. Full verdict:
`/tmp/determinism-check-task4-1794292150/verdict.md`.

## Verdict
DETERMINISTIC
**Disposition:** FIX_NOW (the thread's call), **but see the Gate C finding below, which this pass could not close**
**Stumping type:** mechanism: binding_constraint (primary), with method_or_model_selection (the battery-loss curve
shape) and an assembly/cross-reference layer (the diesel bridge, the heater derivation) riding alongside;
stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why
The thread independently rebuilt the chain from the raw files without reading the solution first, the 48 blocks'
design-day energies from `block_register_2026.xlsx`'s own scheduled km and hours-out plus the stated bridge
(a=-0.1328, b=0.03092) and heating rate (8.1 kW pilot HVAC + 4.3 kW replaced-heater draw = 12.4 kW/hour-out), the
23-block DES-1 4.1 qualifying set against 391 kWh, and an exact earliest-deadline-first feasibility solve of the
night's 700 kW/21:00-07:00 cap in the fleet plan's priority order, and landed on the golden's exact 18-block list,
cut at M125 as the 19th, and on asks 2, 3 and 5's figures to the stated rounding. That reproduction is why the
headline verdict is DETERMINISTIC, not SOLUTION_WRONG: every number in FINAL_RECOMMENDATION, SUPPLEMENTARY_ANSWERS
and CRITICAL_COMPONENTS traces to a named shipped file (`vehicle_register_2026.xlsx`'s cabin-heating column,
`ebus_quotation_2027.pdf`, `charging_connection_agreement_2025.pdf`, `fleet_plan_2027.xlsx`), and no competing
answer the thread could construct from the files (ordering on raw 480 kWh, or on the 23 qualifiers alone) survives
once DES-1 2.3, 3.2, 4.1 and 4.2 are read literally.

The one open item is the question this pass was specifically asked to close: whether the night cut is invariant
across Critical Component 2's own graded band (3.8 to 4.8 kW). The thread's sensitivity sweep says no, the literal
low edge, 3.8 kW, flips the order from 18 to 19 blocks with a different list (M125 now included, the cut moving to
M103). That is a direct conflict with the design note's own `checks.py` assertion SF27 ("every edge lands the same
verdicts and the same 18 (asserted)"), which this build's "2026-11-10, architecture 10 stage 4" log entry records
as having been fixed and asserted after the prior judge pass raised exactly this question. See "Competing answers"
below; this is reported, not resolved, because I did not re-derive the heater-edge chain myself (per the contract,
the generator is off-limits to me) and the thread's own sensitivity method was an isolate-the-heater-term
approximation, not a full re-run of the generator's own pipeline at heater = 3.8 kW.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ask 2, M108 design-day energy | 290 kWh | 293.3 -> 290 | Yes |
| Ask 2, M119 design-day energy | 360 kWh | 364.6 -> 360 | Yes |
| Ask 3, qualifying set | 23 blocks | 23, same set | Yes |
| Ask 5, connection-point energy, 23 qualifiers | 8.7 MWh | 8,000/0.92 = 8,695.65 -> 8.7 | Yes |
| Ask 5, connection-point energy, 18 ordered | 6.7 MWh | 6,200/0.92 = 6,739 -> 6.7 | Yes |
| Main recommendation, night cut (exact feasibility, priority order) | 18 blocks, the named list | identical 18, cut at M125 | Yes |
| Night cut under least-slack, simple period-energy, 10/20-min slack | 18 blocks | identical 18 in all variants | Yes |
| Night cut under earliest-departure-first *selection* (not DES-1 4.2's rule) | n/a | 17-18 blocks, different list | Not a defensible rival (DES-1 4.2 pins priority-order assignment) |
| Ask 1, diesel l/100 km (48 cells) | 37.2-62.4 | spot-checked 5 vehicle fuel-card totals for plausibility only, not all 48 cells to 0.1 | Partially (not independently re-derived cell by cell) |
| Ask 4, first-winter loss | 4.3% | not independently re-derivable without the SOC time series; curve-form comparison internally consistent, straight-line's exclusion a legitimate method call | Accepted on reasoning, not full re-derivation |
| Critical Component 2, heater kW at band edges | 4.3 kW, band 3.8-4.8 | band interior (3.9-4.8) holds the golden's 18; literal edge 3.8 kW flips to 19 | **Conflict, see below** |

## Competing answers that survived
- **The heater-band low edge (3.8 kW).** Critical Component 2 is graded within 3.8 to 4.8 kW. Every value the
  thread tested from 3.9 kW up to 4.8 kW reproduces the golden's 18-block main recommendation exactly; only the
  literal low edge, 3.8 kW (inclusive in the stated band), produces a different, defensible main-recommendation
  answer, 19 buses, with M103 cutting the list and M125 now included. The design note's `checks.py` assertion
  SF27 claims the opposite ("both bands' edges land the same 18 and the same verdicts") and records this exact
  question as closed after the prior judge pass. The two claims disagree. Because the thread approximated the edge
  test (holding the bridge and schedule fixed and varying only the isolated heater term against the golden's own
  published energies, rather than rerunning the generator's full pipeline at heater = 3.8 kW), and because I have
  no access to `generator/checks.py` under this contract, I cannot adjudicate which is right. This is the one
  genuinely open fork from this pass: **a value inside Critical Component 2's own graded tolerance band produces a
  different main recommendation than the golden**, which is a Gate C concern on the main recommendation if the
  thread's sensitivity holds up under a literal full-pipeline rerun.
- The loss-percentage band (3.8 to 5.0 per cent) was swept against the full heater band in combination and never
  moved the qualifying set or the night cut on its own; no block sits close enough to the 391 kWh limit for the loss
  parameter to matter. No fork here.
- No other competing answer survived for the main recommendation or any of the five supplementary answers; the
  thread's own construction of the strongest honest alternative in each case (raw 480 kWh ignoring first-year loss;
  ordering all 23 qualifiers ignoring the connection cap; earliest-departure-first selection instead of
  priority-order assignment) is ruled out by a named clause in DES-1 or the connection agreement.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 14 files: CSV x7, XLSX x4, PDF x3 (3 categories) | Yes |
| Large messy files | 1 CSV 20,000+ rows, 1 CSV 10-20 printed pages | `fuel_card_transactions...csv` 20,805 rows; `depot_dispatch_log...csv` 41,791 rows; `workshop_orders...csv` 841 rows / 7 cols incl. free-text description, consistent with 10-20 printed pages | Yes |
| metadata.json distractors | 2+ named, unlabeled in ZIP | `tyre_and_brake_costs_2025.xlsx`, `depot_electricity_invoices_2025-01_2026-10.csv`; neither named anywhere inside the ZIP | Yes |
| Distractors unused but relevant | each ruled out by a shipped fact | `tyre_and_brake_costs.xlsx` confirmed unused by the judge; `depot_electricity_invoices` plausible (relevant to a night-energy ask) and not referenced in any solution step | Yes |
| Deliverables | 1-3 requested, all present in golden, no format family forced | `niittyla_ebus_order_2027.xlsx` + `.pptx` requested in prompt.txt; `golden.zip` holds exactly those two files | Yes |
| Asks multi-dimensional, unit+rounding stated | yes | 5 supplementary asks, each 48 cells, unit and rounding given in the prompt's closing sentence | Yes |
| Answer shape, 4+ checkable results | one of 14 shapes | "a schedule under capacity" / ranked list under a cap; 8 graded results (main recommendation + 5 supplementary + 2 critical components) | Yes |
| Golden ZIP exact match | exactly requested files/formats | confirmed via `unzip -l golden.zip` | Yes |
| LLM-generated tells | none | judge's hygiene check: PASS, no LLM tells found | Yes |

## Gate G reconciliation
The thread's classification (`mechanism: binding_constraint` primary, `method_or_model_selection` and an
assembly/cross-reference layer riding with it; `surface_read_dependency: no`; `sole_data_defect: no`) matches the
design note's own framing: the "Not rule application" and "No decoy" sections name the same three independent
judgments (the diesel bridge, the heater cross-reference, the night's capacity feasibility) as the note's "Not one
thing" paragraph, and neither the note nor the thread finds any reported figure in the package that is itself wrong
and must be caught and flipped. No disagreement on Gate G; the task is correctly typed as a FINE-numbers
binding-constraint / method-selection shape, not surface-read-rejection.

## Gate H reconciliation
- **H3/one_thing:** thread says `none` of the client's banned shapes applies cleanly, consistent with the design
  note's hidden-factor record, which marks all four constructed factors (the pilot's selection-on-diesel, the
  fuel heater's hidden load, the night's shared capacity, the first-winter loss curve) `keep`, each requiring
  modelling to find or fix, not a one-step routine correction. No shallow_hidden_factor finding on either side.
- **Effort grades close but not identical.** Design note: quick 0.5/8 (6%), careful-but-hurried 2.5/8 (31%),
  thorough 8/8. Thread: quick ~1/8 (12%), careful-but-hurried ~2-3/8 (15-25% of rubric weight, which it states as
  "comfortably under... a third"), thorough 8/8. Both keep the careful-but-hurried pass at or under the third-of-
  results ceiling the client's bar requires; no finding here.
- **The one-fact test is where the two disagree, and this is the most important Gate H finding of the pass.** The
  design note's "Largest single hint" is "the pilot blocks were chosen for their low diesel use, and the diesel
  figures carry the difficulty the timetable's kilometres, climb and speed miss," which the note says rescues 1 of
  8 results (R2, and orders 20). The thread independently proposed a *different* candidate sentence, "the 2027
  bus's heat is 100 per cent electric where the pilot's fuel-fired heater hid part of its real cold-weather energy
  draw from the battery books", and estimated it would rescue up to 5 of 8 results if simply handed over
  (Critical Component 2, asks 2, 3 and 5 directly, plus a contribution to the main recommendation). 5 of 8 is well
  past the client's roughly-a-third ceiling for H5. The thread treated this as a caution rather than an outright H5
  fail, reasoning that the qualitative fact alone does not hand over the quantitative 4.3 kW (which still needs the
  HVO fuel-card regression) or the diesel bridge or the night schedule. That reasoning is defensible, but it is the
  author's own effort.py / design-note one-fact test that is supposed to catch exactly this, and it reports a
  smaller number (1 of 8) than an independent reviewer's first attempt at finding the single most useful sentence
  (5 of 8). This gap is worth the author's attention even though it does not, on the thread's own read, cross into
  an H5 failure.
- **Per-result determinism / Gate C on a graded band.** This is the same finding as the "Competing answers"
  section above, restated under Gate H's per-result rule: "a band that excludes a defensible rival is a Gate C
  failure on that result... a later result graded on the solver's own earlier figure is fine." Here the band does
  not exclude a rival; it *includes* one that flips the headline recommendation. Design note SF27 asserts the
  opposite. Unresolved by this pass; flagged for the author.
- No finding that the declared distractor carries a graded result (the thread confirmed `tyre_and_brake_costs.xlsx`
  unused).

## Stump power (Gate F)
Thread's estimate, reused here: a careful-but-hurried strong analyst plausibly lands inside the graded tolerance on
roughly 1-2 of the 8 results (Critical Component 1 at best, by cancellation in a difference-of-averages; partial
credit on scattered ask-1 cells), roughly 15-25% of the rubric weight these 8 results carry. Four independent,
well-separated failure modes were named: (1) skipping the heater cross-reference and under-building design-day
energy by 40-60 kWh/block (over-qualifying to as many as 41 blocks in the thread's own test); (2) mapping fuel-card
fills to blocks by "commonest bus" or "day of fill" instead of the tank-to-tank deconvolution, misassigning diesel
rates by several l/100 km; (3) a naive straight-line age-vs-loss fit landing at 2.96%, outside the 3.8-5.0 band;
(4) computing the 23 qualifiers and stopping there, never checking the 700 kW/10h connection cap, over-ordering by
5 buses. None of the four is a data-defect catch; each is "build an honest model correctly, respect a real
capacity limit." This matches the design note's own run forecast (R2-R4, R6-R8 lost; R1, R5 earned) closely enough
that no new stump-power finding is raised here beyond the open Gate C item above.

## Findings, ranked
1. **Open: a value inside Critical Component 2's own graded band (3.8 kW, the literal low edge) produces a
   different main recommendation (19 buses, not 18) by the judge's independent sensitivity sweep, directly
   contradicting the design note's `checks.py` assertion SF27.** This is the item this pass was asked to close and
   it did not close cleanly, it surfaced a conflict instead. Needs a literal full-pipeline rerun at heater =
   3.8 kW (not an isolated-term approximation) to settle which side is right.
2. The design note's one-fact test (1 of 8 rescued) understates what an independent reviewer's first try at the
   same test found (up to 5 of 8, if the heater-vs-register fact were simply handed over). Worth rechecking
   `effort.py`'s H5 sentence search, even though the thread itself did not call this an outright H5 failure.
3. Everything else the thread checked, the main recommendation, all five supplementary answers, Critical
   Component 1, the 23-block qualifying set, the 700 kW night-capacity math, the loss-curve method selection, and
   all hygiene items, reproduced cleanly and independently from the shipped files, with no competing defensible
   answer surviving.

## Next action for the author
Before shipping this cut, rerun the generator's own full pipeline (not an isolated approximation) at the heater
term pinned to exactly 3.8 kW, the literal low edge of Critical Component 2's graded band, and confirm directly
whether the night cut and the main recommendation's block list hold at 18 or move to 19. If it moves, either
narrow Critical Component 2's band to exclude the flipping edge (e.g. 3.9 to 4.8 kW) or widen the main
recommendation's own tolerance to accept both 18 and 19 at that edge; if it holds, record the specific values
(diesel bridge, 48 energies, qualifying set) that make SF27's assertion correct so a future judge pass can verify
it without re-deriving the whole chain.
