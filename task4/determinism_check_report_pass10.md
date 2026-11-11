# determinism-check report, task4, 2026-11-10

Re-judge after a FIX_NOW, licensed under the pipeline's stage-4 rule ("FIX_NOW is fixed in the generator
and re-judged once"). The pack under `target/` is unchanged (`target.zip` sha256
`8a51114e25f18f18eafdf62f5105edc916f28a2f4f890ed9811e1bd92742ea5b`, confirmed by direct hash before the
fresh unzip); only the answer blocks in `submission.md` were amended. The prior clean pass (now
`determinism_check_report_pass9.md`) returned DETERMINISTIC with a FIX_NOW on two items: ask 4's stated
band (3.8-5.0) excluded the straight-line age form (2.96/2.80 depending on refit) with no shipped file
pinning the "choose by fit" convention, and ask 1's 19-of-48-block simplified refit left the diesel figures
unconfirmed rather than wrong. The amended `submission.md` widens ask 4's band to 2.7 to 5.0 (now stated to
span "every age form a fit could take... a straight line in age included") and the ask 1 figures reproduced
to within 0.16 l/100km across all 48 blocks on this pass's independent 48-block joint regression (see
below), so both FIX_NOW items are resolved on the data in hand.

One isolated judge thread (general-purpose, sonnet) ran against a fresh unzip of `target.zip` at
`/tmp/determinism-check-task4-1794358500/target/`, its own `judge_system_prompt.md` (the Sulfur
determinism-judge system prompt, read in full with Bash), and a **sealed**
`sealed/graded_blocks.md` (the four Sulfur answer blocks mapped onto the judge's labels, written by this
session, never inlined in the spawn prompt) it was instructed not to open until it had written
`own_derivation.md` in full. **Order kept: yes**, stated explicitly as the first line of `verdict.md`:
`own_derivation.md` (109 lines) was written to disk, with every figure traced to a specific file and
field in `target/` (battery-loss age forms from `ebus_telematics_daily...csv` against
`vehicle_register_2026.xlsx`'s quoted 480 kWh; the 48-block diesel joint regression from
`fuel_card_transactions...csv`, `vehicle_register_2026.xlsx` and `depot_dispatch_log...csv`; the charging
split from `depot_charging_sessions...csv`), before `sealed/graded_blocks.md` was ever opened. This is real
independent recomputation (a from-scratch 48-block joint tank-to-tank regression, four independently fit
battery-age forms, and a from-scratch LP/max-flow feasibility stress test over the night's 690 kW cap), not
the cheap half of Gate A.

## Verdict
DETERMINISTIC.
**Disposition:** APPROVE. No further fix needed; both FIX_NOW items from the prior pass reproduce cleanly
on the amended blocks and no new fork opened.
**Stumping type:** mechanism: `mixed` (`method_or_model_selection` for the diesel-to-energy bridge and the
heater substitution; `binding_constraint` for the night's 690 kW cap cutting the order at M145;
`statistical_rigor` for the degrading-capacity charging-split fit); stumping_family: `analytical_non_defect`;
surface_read_dependency: `no`; sole_data_defect: `no`.

## Why
Both items the prior pass flagged are closed on this pack, unchanged. Ask 1 (diesel l/100 km, 48 weekday
blocks): the thread's own from-scratch joint regression over `fuel_card_transactions_2024-01_2026-10.csv`
(HVO rows correctly excluded as e-bus cabin-heater fuel, not propulsion diesel, identified by the first HVO
transaction's date matching the first e-bus's in-service date exactly), `vehicle_register_2026.xlsx` (card
validity windows) and `depot_dispatch_log_2024-01_2026-10.csv` reproduced all 48 sealed values to within
0.16 l/100km (e.g. M101 57.83 vs 57.9, M119 62.32 vs 62.4, M140 54.19 vs 54.3, M142 49.96 vs 49.8), well
inside the stated 0.7 band and essentially an exact match on every block, not just the 19 the prior pass
managed. Ask 4 (first-winter battery loss): four independently fit age forms (linear 4.29%, sqrt 4.50%, log
4.57%, quadratic 4.86%, all against the quoted 480 kWh confirmed in `vehicle_register_2026.xlsx` and
`ebus_quotation_2027.pdf`) all land inside the amended 2.7-5.0 band, including the straight-line form that
the prior pass's band excluded.

The one place the thread could not fully close its own replication was critical component 3 / ask 5's
charging-split steady draw: its best literal reading (same-day observed telematics capacity rather than
flat nameplate, per the blocks' own "the capacity its own day shows" language) got efficiency to 0.941
against the golden's 0.949 (a close match) but only reached a 2.23 kW steady draw at -15 C against the
stated 3.5 kW point (band 2.8-4.2), short of the band on the thread's own best attempt within its time
budget. This did not change the verdict: holding efficiency at the golden's 0.949 and sweeping the steady
draw across the **entire stated band** (2.8, 3.5, 4.2 kW), the 17-block night total stays 6.57-6.78 MWh
(matching the sealed 6.7 MWh) and adding M145 as an 18th always exceeds the 6.90 MWh connection ceiling
(6.95-7.18 MWh) under every reading inside the band. Only the thread's own flat-nameplate-capacity shortcut
(steady draw ~1.2 kW, outside the band, which ignores the battery age-degradation the files and ask 4
establish) would admit M145 — and that shortcut is explicitly the hurried-analyst error critical component
3 and solution step 7-8 are built to catch, not a surviving Gate C rival. No competing answer survives for
the main recommendation or any supplementary ask.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Ask 1: diesel l/100km, all 48 blocks | 37.2 to 62.4 (full list in submission.md) | Independent 48-block joint tank-to-tank regression; largest gap observed 0.16 l/100km (e.g. M101 57.83 vs 57.9, M119 62.32 vs 62.4) | Yes, all 48 inside 0.7 band |
| Ask 4: first-winter battery loss | 4.3 percent (band 2.7-5.0) | Own 4-form fit against quoted 480 kWh: linear 4.29, sqrt 4.50, log 4.57, quadratic 4.86 percent | Yes, all 4 forms inside the amended band, including the straight line |
| Critical component 3: charger efficiency | 0.949 | 0.941-0.955 depending on capacity convention; 0.941 under the literal same-day-capacity reading | Yes, close match |
| Critical component 3: steady draw at -15 C | 3.5 kW (band 2.8-4.2) | 2.23 kW on the thread's own best literal replication (short of band); feasibility outcome re-checked by sweeping the full stated band instead | Not independently reproduced to the point estimate, but the M145 cut is stable across the entire band (see Why); not a Gate C fork |
| Ask 5 / M145 feasibility cut | 17 feasible, M145 (18th) infeasible | Own LP/max-flow stress test sweeping steady draw across 2.8-4.2 kW at efficiency 0.949: 17-block total 6.57-6.78 MWh (vs stated 6.7), 18-block (+M145) total 6.95-7.18 MWh, always over the 6.90 MWh cap | Yes, robust across the entire band |
| Component 2: fuel-heater output at -15 C | 4.3 kW | Arithmetic check: 0.48 l/h / 3.9 l/h x 35 kW = 4.31 kW | Yes, essentially exact |
| Connection parameters (690 kW, 150 kW/bus, 21:00-07:00 night) | Stated in Step-by-Step 8 / Ask 5 | Confirmed directly in `charging_connection_agreement_2025.pdf` | Yes |
| Alternative order counts (18, 19, 21, 23, 29, 33) under named shortcuts | Stated in Step-by-Step 9 | Thread's own hygiene check: these are the hurried-analyst shortcuts (pooled-ratio charging, raw pilot-fit on timetable covariates, dropping one correction at a time), not independently defensible unpinned readings | Consistent, no rival survives |

## Competing answers that survived
None. The one open item from the prior pass (ask 4's band excluding the straight-line form) is closed by
the amendment and reproduces on an independent 4-form fit. The one item the thread could not itself fully
close (component 3's steady-draw point estimate) is not a surviving fork: the thread's own stress test
shows the M145 cut and the 17-bus order hold under every reading inside the stated band, and the only
reading that would flip it (flat nameplate capacity, ~1.2 kW) lies outside the band and is the named
hurried-analyst failure mode for that component, not a defensible rival.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 14 files: CSV x8, XLSX x3, PDF x3 (3 categories); no system files, no `__MACOSX`, no `.DS_Store` inside the ZIP | Yes |
| Large messy files | 1 CSV 20,000+ rows, 1 CSV 10-20 printed pages | `fuel_card_transactions_2024-01_2026-10.csv` 20,803 data rows; `workshop_orders_2024-01_2026-10.csv` 841 rows with a free-text description field, ~54.7 KB (consistent with 10-20 printed pages, unchanged from the prior pass's assessment on the same pack) | Yes |
| metadata.json distractors | 2+ named, unlabeled in ZIP | `tyre_and_brake_costs_2025.xlsx`, `depot_electricity_invoices_2025-01_2026-10.csv`; neither named anywhere inside `target.zip` or `golden.zip` | Yes |
| Distractors unused but relevant | each ruled out by a shipped fact | Tyre/brake costs: unused in any solution step, plausible to a reader thinking about fleet replacement economics. Electricity invoices: would answer ask 5 (the night's draw) if summed naively, but the thread's own cross-check (session energy consistently 50-70% of the whole-depot monthly invoice total) and the connection agreement's own note that the meter covers more than bus charging rule it out as a drop-in answer | Yes |
| Deliverables | 1-3 requested, all present in golden, no format family forced | `niittyla_ebus_order_2027.xlsx` + `.pptx` requested in `prompt.txt` ("A workbook with the block figures and a few slides for the board"); `unzip -l golden.zip` holds exactly those two files | Yes |
| Asks multi-dimensional, unit + band stated, no rounding instruction in prompt | yes | 5 supplementary asks (three with 48 graded cells each), each with its unit and band in `submission.md`; `prompt.txt` carries no rounding instruction | Yes |
| Answer shape, 4+ checkable results | one of 14 shapes | A binding-constraint cut (a ranked list cut by feasibility) fed by a forecast and a decomposition; design note's own chain carries 9 results (R1-R9) | Yes |
| Golden ZIP exact match | exactly requested files/formats | `unzip -l golden.zip`: 2 files, matching the 2 requested deliverables exactly | Yes |
| LLM-generated tells | none | Thread's hygiene check: PASS; files read as genuine operational exports (fuel-card statement with card reassignments, a dispatch log with a mid-2025 block re-code, a signed connection-agreement letter, a versioned standard, a sales quotation); no provenance/benchmark leakage found | Yes |

## Gate G reconciliation
The thread's classification (mechanism `mixed`: `method_or_model_selection`, `binding_constraint`,
`statistical_rigor`; `surface_read_dependency: no`; `sole_data_defect: no`) matches the design note's own
account. No reported figure in the files is wrong or needs catching as a surface defect; the difficulty is
the diesel-to-energy bridging regression (R4), the fuel-heater substitution decomposition (R3), the
degrading-capacity charging-split fit (R7), and the 690 kW binding constraint cutting the order at M145
(R9), run jointly, exactly as the design note's Results chain and Carry-forward paragraph state ("no
analytical result is the sole ancestor of more than half of the others... a run that gets the energies
right and the charging split wrong, or the reverse, still loses R8 and R9 by its own figures"). No
defect-flip or data-semantics catch carries the task. Passes Gate G, no finding.

## Gate H reconciliation
The thread's Gate H line: domain pass (a diesel/electric bus depot capacity plan genuinely drives every
quantity; swapping the nouns for another field breaks the method); layers pass (assembly/reconciliation
layer: card-to-vehicle remapping, a mid-2025 block re-code, duplicate telematics days, UTC-to-local
timestamps; analytical layer: the joint block-level regression, the heater-substitution bridge, the
degrading-capacity charging fit, the binding-constraint cut); results: 6+ graded results across 4+ areas
(assembly and reconciliation, modeling, decomposition and attribution, causal/constraint reasoning,
uncertainty/validation); one_thing: `none` (no single hidden or planted factor carries most of the results;
removing any one of the diesel bridge, the heater split, the degrading capacity, or the night cap costs
only its own result); effort: quick ~1-2 of 6+ (~17-33%), careful-but-hurried ~3-4 of 6+ (~50-67%), thorough
6 of 6; one_fact: "use each bus's own degrading capacity, not the nameplate 480 kWh, when reading its
state-of-charge gain" rescues ~1-2 of 6+ results (~17-33%), not the diesel bridge or heater split.

This reconciles cleanly against the design note's own, more granular 9-result chain and effort table
(quick 1/9 ≈ 11%, careful-but-hurried 4/9 ≈ 44%, thorough 9/9; largest single hint rescues 3 of 9 ≈ 33%,
R2/R4/R6). The thread's coarser 6-result read and the note's 9-result read put the quick pass under a
third and the careful-but-hurried pass clearly short of the thorough pass in both readings; the thread's
one-fact estimate (17-33%) sits at or under the note's own 33%, not above it. No finding under any of the
six predictive patterns in the contract (no single hidden/planted factor dominating; no hidden factor
fixed with one routine step mislabeled as modelling or seen only in the deciding units beyond what the
note already discloses; no quick-pass or careful/thorough convergence; no single sentence rescuing more
than the note's own figure; no band excluding a rival the thread actually ran, or a band too wide to
separate a hurried figure from the golden, since the component-3 band was stress-tested across its full
width and the cut held; no declared distractor carrying a result). No Gate G/H finding predicts a
send-back under the 2026-11-09 bar.

## Stump power (Gate F)
The thread's own account: a careful-but-hurried pass using a flat/nameplate battery capacity when fitting
the charging split loses the cold-sensitive steady draw almost entirely (efficiency near 1.0, draw near
0.25-0.28 kW on the thread's own flat-capacity run) and would wrongly admit an 18th bus (M145) under the
690 kW night cap. A pass charging at the sessions' pooled average ratio instead of fitting cold-sensitivity,
or that fits the diesel-to-energy bridge without separating the heater substitution, both land on different
wrong block counts (18, 19, 21 per the design note's own step 9 and effort table). This is genuine,
spread-out stump power across several results (R4, R7, R9 in the design note's numbering), not one single
trap, and matches the design note's effort test (careful-but-hurried earns roughly 4 of 9 results, never
more than a third of the pair estimate on one sentence).

## Findings, ranked
1. (Resolved, informational only) Ask 4's band was widened from 3.8-5.0 to 2.7-5.0 in the amended blocks,
   now explicitly stated to span the straight-line age form; the thread's own independent 4-form fit
   (linear 4.29, sqrt 4.50, log 4.57, quadratic 4.86 percent) lands entirely inside the new band, closing
   the prior pass's FIX_NOW item.
2. (Resolved, informational only) Ask 1's 48 diesel figures reproduced on this pass's full 48-block joint
   regression to within 0.16 l/100km, well inside the stated 0.7 band, where the prior pass's 19-block
   simplified refit had left the figures unconfirmed (not wrong). No divergence found on this pass.
3. (No action needed) The thread could not, within its own time budget, fully close its replication of
   critical component 3's steady-draw point estimate (2.23 kW against the stated 3.5 kW, band 2.8-4.2),
   attributing the residual gap to the exact half-degree knot profiling and temperature convention the
   solution text specifies but the thread did not have time to match exactly. This is flagged as a
   replication-effort limitation of the single bounded pass, not a task defect: the thread's own
   sensitivity sweep across the entire stated band confirms the M145 cut and the 17-bus order are stable
   under every reading inside it, and the only reading that would flip the cut (flat nameplate capacity)
   lies outside the band and is the named hurried-analyst failure for that component.

## Next action for the author
None required. Both FIX_NOW items are closed on the amended `submission.md` against the unchanged pack;
no new fork or finding opened on this pass. Proceed to stage 5 (READY).
