# determinism-check report, task4, 2026-11-10

Clean order-of-operations pass, run per the author's explicit instruction after the prior pass on this
loop (now `determinism_check_report_pass8.md`) broke the order (it opened `graded_blocks.md` before writing
its own derivation and recomputed none of the load-bearing figures), so that pass did not spend the one
re-judge available under `/fix-determinism` and this is the clean pass against `target.zip`
(sha256 `8a51114e25f18f18...`, the final cut after the leak reader's realism fixes).

One isolated judge thread (general-purpose, sonnet) ran against a fresh unzip of `target.zip` at
`/tmp/determinism-check-task4-1794357189/target/`, its own `judge_system_prompt.md` (the Sulfur
determinism-judge system prompt, inlined verbatim and read in full with Bash), and a **sealed**
`sealed/graded_blocks.md` it was instructed not to open until it had written `own_derivation.md`. The
thread confirmed in `verdict.md`'s first line ("Order kept: yes") that it derived Phase 1 (its own
recomputation from `target/` alone: timezone-aware charging-session splitting under six rival knot/
temperature specifications, a fixed-effects battery-loss fit under three age functional forms, a pooled
tank-to-tank diesel least-squares regression over 19 of 48 blocks, and an independent LP/max-flow
feasibility model of the night's charging schedule) **before** opening `sealed/graded_blocks.md` for
Phase 2. This is real recomputation, not the cheap half of Gate A (internal consistency of the blocks
against each other) that disqualified the prior pass.

## Verdict
DETERMINISTIC on the main recommendation and on supplementary answers 2, 3 and 5. Supplementary answer
4 (first-winter battery loss) carries a genuine, narrow Gate C borderline item (see Findings). Supplementary
answer 1 (diesel l/100 km) is **unconfirmed** by the thread's own simplified replication, not shown wrong.
**Disposition:** FIX_NOW, two narrow, author-side clarifications, no input-file or prompt change, no
model rerun.
**Stumping type:** mechanism: `binding_constraint` (primary), with `method_or_model_selection` and
`decomposition_attribution` as co-equal secondary mechanisms; stumping_family: `analytical_non_defect`;
surface_read_dependency: `no`; sole_data_defect: `no`.

## Why
The main recommendation (order 17 buses for M101/M107/M108/M113/M116/M119/M122/M123/M125/M129/M134/M135/
M137/M140/M142/M146/M148) is forced by a chain the thread reproduced independently end to end on the two
hardest numerical steps: (1) it re-derived from `fleet_plan_2027.xlsx`'s own "Weekday blocks 2027" table,
independently of the submission, that M145 lands exactly 18th once the priority list is filtered to the
23 qualifying blocks only (raw priority 29, 18th among qualifiers), not an assertion taken on faith; (2)
it then built its own LP time-discretised max-flow/feasibility model (21:00-07:00, 690 kW total, 150 kW
per bus, each bus's steady "keep-warm" draw held continuous over its charging window), fed with the
answer's own stated design-day energies, and the model independently confirms the first 17 blocks in
qualifying-priority order are feasible and adding M145 as an 18th is not, reproducing 6.74 MWh against
the stated 6.7 MWh for the 17, and 9.23 MWh against the stated 9.1 MWh for all 23 qualifiers (inside the
stated 0.3 MWh band). The charging-split parameters (component 3, ask 5's efficiency and steady draw)
reproduced tightly across six rival specifications (steady draw 2.98-3.46 kW against the stated 3.5 kW,
pooled ratio 0.9197 against the stated 0.920). The thread did **not** finish independently re-deriving
all 48 blocks' design-day energies (ask 2, the design's own largest piece of analytical work, the
heating-architecture bridge from the pilot's HVO-assisted telematics to the 2027 model's fully-electric
heating) to its own satisfaction within the time available, so the feasibility and night-draw checks above
were run on the golden's own stated energies as inputs, not on a fully independent re-derivation of R4
from raw files. That is a real, acknowledged limitation of this single bounded pass, not a defect found
in the task; the thread flagged it honestly rather than papering over it. Taxonomy: `none` on the main
recommendation and asks 2/3/5; a narrow `competing_defensible_answer` concern on ask 4 only (see Findings).

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Main order: bus count and block set | 17 buses, 17 named blocks, M145 excluded | Independent LP max-flow + least-slack schedule on the golden's stated energies: 17 feasible, M145 (18th among qualifiers) infeasible, confirmed under both methods and across the thread's own rival charging-split and workshop-outlet variants | Yes |
| Ask 5: night draw, 17 assigned | 6.7 MWh | 6.74 MWh (own LP) | Yes, inside 0.3 MWh band |
| Ask 5: night draw, 23 qualifying | 9.1 MWh | 9.23 MWh (own LP) | Yes, inside 0.3 MWh band |
| Component 3: steady draw at -15 C | 3.5 kW (band 2.8-4.2) | 2.98-3.46 kW across 6 rival specs (2 temperature definitions x 3 knots) | Yes |
| Component 3: charger efficiency | 0.949 | 0.926-0.950 across rival specs, 0.949-0.950 at knot 5-10 C | Yes |
| Component 3: pooled ratio | 0.920 | 0.9197 (own recompute) | Yes, essentially exact |
| Ask 4: first-winter loss | 4.3 percent (band 3.8-5.0) | Own 3-form fit: sqrt 4.54 percent (close to golden's curved/sqrt figures), log1p 3.45 percent (diverged, attributed to a differing log parameterisation), straight line 2.80 percent (outside the stated band) | Partial: the curved/sqrt forms are consistent; the straight-line rival the design itself names as the hurried method sits outside the band, as the design intends, but see Findings for whether that exclusion is adequately pinned |
| Ask 1: diesel l/100 km (19 of 48 blocks checked) | e.g. M118 37.9, M142 48.5, M125 42.1 (block register / dispatch-log tank-to-tank least squares, all 48 blocks jointly, 12-minute swipe merge) | Own simplified least-squares over 19 blocks jointly (no swipe merge, 6,035 of 18,248 intervals used): values differed by 1-5 l/100 km for 14 of 19 blocks, matched within band for 4 | Unconfirmed; the thread attributes the gap to its own simplification (no swipe merge, partial block set) rather than to a golden defect, and recommends the author re-verify with the exact stated preprocessing |
| Pilot buses draw nothing at Niittylä on the design night | Stated in Step-by-Step 8 | Confirmed directly: `fleet_plan_2027.xlsx` "Timetable 2027" moves buses 1201-1206 to Kauppala depot 2027-01-11 | Yes |
| Workshop's 22 kW outlets cannot charge in-service buses | Stated (component 3 / DES-1 3.2) | Confirmed by two independent, concordant sources: DES-1 3.2 ("the workshop's outlets are for buses under repair") and the connection agreement ("not on the load-control relay") | Yes |

## Competing answers that survived
- **Ask 4 (first-winter battery loss, 4.3 percent, band 3.8-5.0).** The straight-line age form, which
  the design note itself names as the hurried/self-confirming rival (submission's own Step-by-Step 6
  lists it: "a straight line in age 2.96"), reproduced by the judge's own fit at 2.80 percent, outside
  the stated band on both the golden's own number and the thread's independent refit. The design note's
  Results chain (R5) pins the selection by "a form with a fast early loss chosen by fit" (i.e., the
  better-fitting curved/sqrt/log family beats the straight line on R2 in the company's own telematics),
  which is a legitimate `method_or_model_selection` criterion (comparative goodness of fit on honest
  data), not an unpinned threshold, the straight line is "ruled out by named data" (its own inferior fit
  statistic) rather than equally defensible. But no shipped file in `target/` states this "choose by fit"
  convention explicitly; it lives only in the generator's own design note, which solvers never see. This
  is the one place in the chain where the shipped fit-selection convention is thinner than it should be:
  the band excludes a rival a rigorous solver could legitimately try first (straight-line degradation is
  the simplest reading of "lose for good in their first twelve months"), and nothing in `target/` tells
  that solver which functional-form family the standard intends. Recommend either widening the band to
  admit the straight-line rival, or adding one documented-convention line (in `DES-1` or the vehicle
  register) that pins sub-linear/curved calendar fade as the governing assumption for this fleet's
  battery chemistry.
- **Ask 1 (diesel l/100 km).** Not a competing-answer fork in the Gate C sense; the thread's own
  divergence is attributed to a deliberately simplified replication (no 12-minute swipe merge, 19 of 48
  blocks rather than the full joint fit), explicitly flagged as unconfirmed rather than wrong. No
  alternative answer is asserted to survive; the item is carried forward as an open re-verification task
  for the author, not a determinism finding against the golden.
- No other fork survived. The feasibility cut (17 vs 18), the charging-split parameters, and the
  pilot-fleet exclusion from the design night all closed cleanly under every rival the thread ran.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 14 files: CSV x7, XLSX x4, PDF x3 (3 categories); no system files, no `__MACOSX` | Yes |
| Large messy files | 1 CSV 20,000+ rows, 1 CSV 10-20 printed pages | `fuel_card_transactions...csv` 20,803 data rows; `depot_dispatch_log...csv` 41,790 data rows (both clear the 20,000-row bar); `workshop_orders...csv` 841 rows / 7 columns incl. a free-text description field, consistent with 10-20 printed pages | Yes |
| metadata.json distractors | 2+ named, unlabeled in ZIP | `tyre_and_brake_costs_2025.xlsx`, `depot_electricity_invoices_2025-01_2026-10.csv`; neither named anywhere inside `target.zip` or `golden.zip` | Yes |
| Distractors unused but relevant | each ruled out by a shipped fact | Neither file is referenced in any solution step or in the judge's own derivation; both are plausible to an untrained eye (tyre/brake cost by vehicle; a separate electricity-invoice feed) and unused in the actual night-draw or cost computation | Yes |
| Deliverables | 1-3 requested, all present in golden, no format family forced | `niittyla_ebus_order_2027.xlsx` + `.pptx` requested in `prompt.txt`; `unzip -l golden.zip` holds exactly those two files, nothing else | Yes |
| Asks multi-dimensional, unit + band stated, no rounding instruction in prompt | yes | 5 supplementary asks, each with 48 graded cells or a single banded figure; units and bands are in the answer blocks (submission.md), not the prompt; `prompt.txt` itself carries no rounding instruction | Yes |
| Answer shape, 4+ checkable results | one of 14 shapes | A binding-constraint schedule under capacity (a ranked list cut by a feasibility test) with a forecast and a decomposition feeding it; 9 results in the design note's own chain (R1-R9), well above the 4-result floor | Yes |
| Golden ZIP exact match | exactly requested files/formats | Confirmed via `unzip -l golden.zip`: 2 files, matching the 2 requested deliverables exactly | Yes |
| LLM-generated tells | none | Judge's hygiene check: PASS. Files read as genuine operational exports (a signed connection-agreement letter, a versioned internal standard, a sales quotation with a named account manager, messy fuel-card data with reissues and a pump cap, a mid-2025 block-code renumbering); no provenance/benchmark leakage found | Yes |

## Gate G reconciliation
The thread's classification (mechanism `binding_constraint` primary, with `method_or_model_selection`
and `decomposition_attribution` secondary; `surface_read_dependency: no`; `sole_data_defect: no`) matches
the design note's own account of where the weight sits: R4 (forecasting, the HVO-to-electric heating
bridge) and R7 (modeling, splitting the charger's metered energy into recharge and steady-draw) are
genuine decomposition/model-selection work on honest data, and R9 (the order itself) is a binding
constraint (the night's 690 kW) that overturns the naive per-block-threshold read, exactly as the design
note states ("the night supply shared over the buses ordered, so that per-block shortfalls too small to
flip a verdict accumulate into buses"). No defect-flip or data-semantics catch carries the task; this
reconciles cleanly, no Gate G finding.

## Stump power (Gate F)
The thread's own account of where a careful-but-hurried strong model is likeliest to lose matches the
design note's `Largest single hint` row closely: trusting the pilot buses' HVAC telematics as-is for the
2027 model's design-day energy (missing the HVO-heater architecture change), defaulting to a straight-line
battery-aging slope, or ranking blocks on raw design-day energy against the 85 percent threshold alone
without the night's 690 kW capacity constraint (the design note's own counterfactual: the pooled-ratio/
no-capacity read orders 18, the raw-energy-times-cold read orders 33). These are spread across at least
four of the design note's named areas (forecasting, modeling, decomposition, synthesis/binding
constraint), not concentrated in one catch, consistent with H4.

## Findings, ranked
1. **Ask 4's band excludes a named rival without a shipped pin (Gate C, narrow).** The straight-line
   age-form rival (2.80-2.96 percent depending on who fits it) sits outside the stated 3.8-5.0 percent
   band, and the "choose the better-fitting curved form" convention that rules it out lives only in the
   design note, not in any file a solver sees. FIX_NOW: either widen the band or add one line to a
   shipped file (or the prompt's governing standard) pinning the functional-form convention.
2. **Ask 1's diesel figures are unconfirmed, not shown wrong.** The thread's own simplified
   re-implementation (no 12-minute swipe merge, 19 of 48 blocks rather than the full joint fit) diverged
   from the golden by more than the stated 0.7 l/100 km band for most of the 19 blocks it checked, but it
   attributes this to its own simplifications and explicitly does not claim the golden is wrong. FIX_NOW:
   the author should re-verify a sample of the 48 block figures against the exact stated preprocessing
   (the merge rule and the full 48-block joint fit) to close this out with confidence; no finding is made
   against the golden on the evidence gathered in this pass.
3. **Ask 2's design-day energies (R4) were not independently re-derived from raw files in this pass.**
   The thread accepted the golden's own stated 48 design-day energies as inputs to its (independently
   built) feasibility model, rather than completing its own heating-architecture decomposition to
   sufficient confidence within the time available. This is the single largest piece of analytical work
   in the chain and the one this pass verifies least independently; it is a limitation of this bounded
   judge pass, not a finding against the task. No action needed unless a future pass has time to complete
   the full HVO-to-electric bridge independently.

## Next action for the author
Pin the age-curve selection convention for ask 4 (one line stating that the first-year loss share is
taken from the better-fitting of the candidate age-decay forms on the company's own telematics, or
widen the graded band to 2.8-5.0 to admit the straight-line rival), and separately re-run the exact
stated diesel tank-to-tank preprocessing (12-minute swipe merge, all 48 blocks fit jointly) on a sample
of blocks to confirm ask 1 against the 0.7 l/100 km band with full-method fidelity. Neither change
touches `prompt.txt`, `target.zip`, or the main recommendation; no model rerun is required.
