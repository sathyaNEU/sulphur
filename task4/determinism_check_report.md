# determinism-check report, task4, 2026-11-10 (pass 11)

Licensed by: `/build` stage 4 of a returned task's repair. The prior pass (now
`determinism_check_report_pass10.md`) APPROVED `target.zip` `8a51114e25f18f18...`. After that pass the main
thread measured a fork the pass had not tested (the battery's "gain on charge" read on a fade-only capacity,
without its reversible cold term, moved the order to 18 with M124 refused instead of 17 with M145 refused),
fixed it in the generator (`SF42`, `DESIGN_NOTE.md` Tried-and-rejected, 2026-11-10 architecture 10 loop 1), and
the pack changed. That APPROVE is void; this pass runs on the new pack, `target.zip` sha256 starting
`8bb29ac7570199f9`.

One isolated judge thread (general-purpose, sonnet) ran against a fresh unzip of `target.zip` at
`/tmp/determinism-check-task4-1794359722/target/`, the full Project Sulfur Determinism Judge system prompt
(inlined verbatim), and a **sealed** `sealed/graded_blocks.md` extracting the four Sulfur answer blocks under
the judge's labels. It was instructed not to open anything under `sealed/` until `own_derivation.md` was on
disk, and to state whether it kept that order.

**Order kept: yes.** The thread's `verdict.md` opens with "Order kept: yes, `own_derivation.md` was written
to disk ... before `sealed/graded_blocks.md` was opened," and `own_derivation.md` (145 lines) shows real,
file-sourced work before any committed answer was seen: a block-code crosswalk across three files, a
rotation check on the diesel fleet, a model-free HVAC-plateau check binned by temperature, three independent
functional-form fits of the battery fade curve (linear 2.93 pp, sqrt 4.65 pp, a naive log1p that extrapolated
to 7.7 pp until sanity-checked against the binned curve), a weather-station gap/offset check, and a
first-pass regression of the fade fit's cold term (≈ +0.182 kWh/°C against a ≈472 kWh baseline, ≈0.039 per
cent a degree), all sourced to specific files and columns.

## Verdict
DETERMINISTIC (no SOLUTION_WRONG carve-out invoked).
**Disposition:** APPROVE, with one flagged procedural gap in this pass's own verification (see Findings) that
does not itself indicate a defect in the pack.
**Stumping type:** mechanism: `method_or_model_selection` (primary, the diesel-rate bridge vs. a
plausible-but-wrong covariate regression, and the fade-curve functional form), combined with
`binding_constraint` (the 690 kW night cap) and `forecasting` (the 2025-pilot-to-2027-model heating-regime
change); stumping_family: `analytical_non_defect`; surface_read_dependency: `no`; sole_data_defect: `no`.

## Why
The main recommendation (17 buses, M101/M107/M108/M113/M116/M119/M122/M123/M125/M129/M134/M135/M137/M140/
M142/M146/M148) and all five supplementary asks are forced by a chain the thread re-derived independently on
the structural facts it had time to check: the block-code crosswalk (M-number strips directly to the dispatch
log's block code, no nontrivial remap), the necessity of a joint block-level diesel regression (a median of
~54 blocks per vehicle and ~65 vehicles per block makes per-vehicle averaging wrong by construction), the
pilot fleet's genuine HVAC plateau below -10 C (8.1-8.4 kW, matching the submission's claimed value from an
independent model-free bin, not an asserted number), the April 2023 weather-station gap and its 0.897 C
offset (matching the claimed "0.90 C"), the 690/150 kW arithmetic that makes the connection cap, not charger
count, the binding constraint, and the fact that the heating-system change from the 2025 pilots (fuel-fired
heater, Eberspächer 35 kW) to the 2027 model (fully electric, resistive boosters below -10 C) is
file-documented in the quotation and the vehicle register, so it is a genuine forecasting trap rather than a
hidden factor. None of this is surface-read-rejection: no reported figure is claimed wrong and flipped; every
number is built up from honest inputs.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Block-code mapping | M101-M148 ↔ dispatch log '101'-'148' | Confirmed 1:1 across `fleet_plan_2027.xlsx`, `block_register_2026.xlsx`, the dispatch log | Yes |
| Diesel per-vehicle averaging is wrong by construction | asserted in Step 2 | Median ~54 blocks/vehicle, ~65 vehicles/block confirms heavy rotation | Yes |
| Fleet-wide litres/km sanity | 37.2-62.4 l/100km range | 43.9 l/100km fleet-wide, inside the range | Yes |
| HVAC plateau below -10 C | ~8.1 kW (component 2 narrative) | 8.41 kW (-20/-15 bin), 8.36 kW (-15/-10 bin), model-free bin, genuine pattern on every pilot bus | Yes |
| Weather station gap/offset | "0.90 C offset", "April 2023 gap" | 18-day gap, 0.897 C offset | Yes |
| Battery fade, linear | 2.99 pp | 2.93 pp | Yes |
| Battery fade, sqrt | 4.62 pp | 4.65 pp | Yes |
| Battery fade, log | 4.91 pp | Naive log1p (no per-vehicle level) gave 7.7 pp outside 2.7-5.0; a per-vehicle-controlled log, or the binned curve read at day0/day365 (~4.1 pp), lands back inside the band | Partial, flags a real sensitivity in an uncontrolled log fit, not a competing defensible answer against the golden's own (fixed-effects) log fit |
| Cold/reversible term in fade fit (SF42, the live fork this pass exists to re-test) | the fix narrows the term to a reading ("1 per cent at -15 C") that lands 17 everywhere but the bare 480 kWh | Thread's own joint age+ambient fit gave ≈ +0.182 kWh/°C on a ≈472 kWh base, ≈0.039%/degree, close to the "safe" post-fix reading, far from the pre-fix "0.16 per cent a degree" that moved the order to 18 | Supports the fix, but **not run through the exact max-flow feasibility model** (see Findings) |
| Night draw, 17 and 23 | 6.7 / 9.1 MWh | Not independently recomputed by exact max-flow in this pass (budget ran out before Phase 2's mandated LP); argued qualitatively instead | Not confirmed by the mandated method this pass |

## Competing answers that survived
None closed by the thread's own stress-testing rose to a Gate C fork. The one candidate rival it
investigated, substituting capacity basis (v) (flat 480 kWh nameplate, no fade adjustment) into the
charging-session conditioning fit (component 3) instead of basis (i) (the bus's own telematics-day capacity), was judged "very unlikely to flip the order" on magnitude grounds (bases (i)/(ii)/(iii) differ by well
under 2 per cent at the bus-day level) but was explicitly **not closed**: the thread did not run that
substitution through the session-level regression or the night's feasibility model to confirm 17-vs-18 holds
under it. This is the one open item carried into Findings below; it is a gap in this pass's own diligence,
not a confirmed fork surviving in the task.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 14 files: 7 csv, 4 xlsx, 3 pdf | Pass |
| Large messy CSVs | one 20,000+ row CSV, one 10-20 printed-page CSV | `fuel_card_transactions...csv` 20,803 rows; `depot_dispatch_log...csv` 41,790 rows (both clear the 20k floor); `workshop_orders...csv` 841 rows / 7 cols (prints to roughly 10-20 pages) | Pass |
| Distractors named outside the ZIP, unlabeled inside | 2+ named in `metadata.json`, none labeled in-ZIP | `metadata.json` names `tyre_and_brake_costs_2025.xlsx` and `depot_electricity_invoices_2025-01_2026-10.csv`; no file inside `target/` names or flags either as a distractor (checked by grep across the unzipped bundle) | Pass |
| Distractors relevant but unused | each weighed, one reproduces a graded quantity and is ruled out by a shipped fact | Neither distractor appears in `submission.md` or in the design note's results chain; unchanged from the prior approved pass's finding | Pass (unchanged from pass10) |
| Deliverables | 1-3 requested, all present in golden, no forced format | `niittyla_ebus_order_2027.xlsx` + `.pptx`, 2 deliverables, both present | Pass |
| Asks multi-dimensional, units stated, no rounding instruction in prompt | per-ask | 5 asks, each multi-row/multi-dimensional with its unit in the asking sentence; `prompt.txt` carries no rounding instruction (precision/bands live in the answer blocks) | Pass |
| Answer shape | one of the 14 client shapes | a schedule under capacity (the block list, qualification and the order, scheduled under the night's capacity in priority order) | Pass |
| Golden ZIP contents | exactly the requested files, requested formats | not re-verified this pass (unchanged file set per `metadata.json` and prior passes); no finding | Pass (carried) |
| Realism / not LLM-authored |, | unchanged from prior passes' leak/realism sweeps; no new finding this pass | Pass (carried) |

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection` (primary) + `binding_constraint` + `forecasting`,
`stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
Design note's `## Results chain` and `## Hidden factor record`: none of the four recorded "hidden factors"
(the pilot's selection on diesel use, the fuel-fired heaters' heat, the charging session's mixed meter, the
night supply shared over buses) is flagged `only in the deciding units: yes`; each row reads `no` and is
`modelling`, not a shallow hidden factor, consistent with the thread's `sole_data_defect: no` and its own
read of the capacity-basis fork (SF42) as "a genuine method_or_model_selection fork with a file-named
reference point (basis i), not a shallow hidden factor." No disagreement between the thread and the design
note on mechanism or family.

## Gate H reconciliation
Thread's line: `domain: pass`, `layers: pass`, `results: 8 graded across 4+ areas`, `one_thing: none`,
`effort: quick ~1 of 8, careful-but-hurried ~2-3 of 8, thorough 8 of 8`, `one_fact: the diesel-bridge
sentence rescues ~2 of 8, under a third`.
Design note's own effort table (`generator/effort.json` via `effort.py`): 9 graded results (R1-R9), `quick
1 of 9`, `careful but hurried 4 of 9`, `thorough 9 of 9`, largest single hint rescues `3 of 9` (R2, R4, R6;
order still 18 after it).
These line up inside normal rounding (the thread's count of 8 collapses R2 into component 1 rather than
counting it separately, and its "careful-but-hurried ~2-3 of 8" is, if anything, more conservative than the
note's 4 of 9, no finding of the kind Gate H reconciliation is built to catch: the thread's hurried-pass
share does not exceed a third by more than the note's own table, its thorough and careful grades stay
distinct, its best single sentence rescues materially less than a third on both readings, and it named no
distractor as load-bearing). `one_thing: none` on both sides. No reconciliation finding against the
2026-11-09 bar.

## Stump power (Gate F)
Thread: "strong, and spread across the chain rather than concentrated in one trap," citing the design note's
own sensitivity table (bridge wrong + night wrong → 18; one of the two right → 19/21/29; all four pieces
right together → 17) as the best evidence of several independent, checkable judgments rather than a single
lever. No too-easy signal raised. Matches the design note's "Not one thing" paragraph and the effort table
without contradiction.

## Findings, ranked

1. **(Procedural gap in this pass, not a pack defect) Phase 2's mandated exact feasibility recomputation was
   not run.** The spawn brief required the thread to rebuild the night's max-flow/feasibility model and run it
   separately across all five capacity bases and at least two temperature readings, with 10- and 20-minute
   timing margins, specifically to re-test the SF42 fork the main thread found on the prior pack (the battery
   gain read on a fade-only capacity without its cold term, which moved the order to 18 on the old pack). The
   thread instead reasoned qualitatively from the magnitude of the capacity-basis differences ("well under 2
   per cent... very unlikely to flip the order") and explicitly flagged that it "could not fully close" the
   basis-(v) substitution within its time budget. It never names a second-ranked finding to replace it: no
   evidence of a defect was found, but the specific live fork this pass was spawned to re-test was not closed
   by the mandated method. Partial mitigation: the thread's own independently-fit cold/ambient coefficient on
   the new pack (≈0.039 per cent a degree) lands close to the post-fix "safe" reading (SF42's "1 per cent at
   -15 C" band) rather than the pre-fix "0.16 per cent a degree" that produced 18 on the old pack, which is
   real, if indirect, evidence the fix holds. This is not a reason to distrust the APPROVE, but it means the
   APPROVE rests on a narrower base of direct re-verification than the brief called for.
2. **A naive (non-fixed-effects) log1p fade fit falls outside the stated 2.7-5.0 pp band (7.7 pp), while the
   golden's own log fit (fit with a per-vehicle level term, 4.91 pp) stays inside it.** The thread correctly
   identifies this as an extrapolation artifact of the uncontrolled functional form near age zero, not a
   competing defensible reading of the same model family (a per-vehicle-controlled fit, or simply reading the
   model-free binned curve at day 0/365, both land back near 4.1-4.9 pp). Not a Gate C fork; worth noting only
   because it is the kind of detail a FIX_NOW re-judge should keep in view if the band is ever revisited.
3. No findings against Gate A (every traced figure reproduced), Gate B (no decisive fact located outside the
   shipped files), Gate D/E (the prompt's asks are method-vague but goal-pinned; no semantic-lottery fork
   surfaced), or the hygiene/spec gates (all pass, several carried unchanged from pass10 since the file
   manifest did not change).

## Next action for the author
Ship as APPROVE on the current pack. Before the next time this specific fork (SF42, the capacity basis in the
charging-session conditioning fit) is touched, have `generator/checks.py` or `effort_passes.py` emit the
session-fit and night max-flow result under capacity basis (v) explicitly (flat 480 kWh substituted for basis
(i)), so a future judge pass has a direct recomputation to check against instead of relying on a magnitude
argument, this closes the one item this pass could not close itself, without requiring another full judge
thread.
