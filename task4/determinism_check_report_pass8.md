# determinism-check report, task4, 2026-11-10

Pass on architecture 10, loop 1, rebuilt after the platform's holistic audit found the order count not forced
and three asks reading two ways (target.zip sha256 133243bf4849fb55...). One isolated judge thread
(general-purpose, sonnet, medium effort) ran against a fresh unzip of `target.zip` at
`/tmp/determinism-check-task4-1794356137-24998/target/` and the five graded blocks in a scratch-only
`graded_blocks.md` it was told to open only after writing its own from-scratch derivation
(`/tmp/determinism-check-task4-1794356137-24998/own_derivation.md`). It never saw `submission.md`,
`DESIGN_NOTE.md`, `generator/`, `pipeline.json`, `metadata.json`, `runs/`, `golden/`, `golden.zip`, any earlier
report, `leak_check_report.md`, or `guidelines/`. Full verdict: `verdict.md` in that scratch path.

**Order-of-work caveat, disclosed by the thread itself.** The thread reports that an early exploratory `cat
graded_blocks.md`, run to get its bearings before planning the review, showed it the full blocks (including
FINAL_RECOMMENDATION and the asks) before `own_derivation.md` was finished. It states no figure was copied into
the derivation and that every number there was re-derived from `target/` directly, and it flagged the breach
for the record rather than hiding it. This weakens, but does not void, the independence the contract requires:
the one load-bearing cross-check that matters most (filtering `fleet_plan_2027.xlsx`'s 1-48 priority order down
to the "yes" set and taking the first 17) is a mechanical, auditable operation that is hard to fake agreement
with by having peeked, and it reproduces the FINAL_RECOMMENDATION's 17-block set exactly, including M145 landing
18th. Recorded as a process finding, not a disposition-changing defect.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection + binding_constraint (mixed, both FINE-numbers shapes);
stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why
The main recommendation's 17-block order reproduces exactly and mechanically once the qualifying set (DES-1
4.1, 391 kWh threshold) and the fleet plan's priority order are fixed: taking the first 17 of the 23 "qualifies
= yes" blocks, in `fleet_plan_2027.xlsx`'s priority order, gives precisely M101, M107, M108, M113, M116, M119,
M122, M123, M125, M129, M134, M135, M137, M140, M142, M146, M148, with M145 the 18th qualifying block, matching
the recommendation's own claim about M145. The literal inputs the decision turns on (690 kW / 21:00-07:00 =
6.90 MWh from `charging_connection_agreement_2025.pdf`; 480 kWh usable-when-new from `ebus_quotation_2027.pdf`;
the 35 kW / 3.9 l/h fuel-fired heater from `vehicle_register_2026.xlsx`; the 85 per cent rule and the
priority-cut rule from DES-1 4.1/4.2) all trace to a specific shipped file with no external dependency. The
thread could not re-derive every pivotal number to stated precision in its time box (the fill-merge/interval
regression behind the 48 l/100 km figures, the diesel-to-energy bridge coefficients, the exact battery-loss
curve percentage, and the charger-efficiency/self-heating regression), but found no evidence against any of
them, and several adjacent figures (the 391 kWh threshold, the 6.90 MWh cap, the 17-block order itself)
reproduced exactly from literal file reads. No decisive fact lives outside the 14 shipped files.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Weekday block universe | 48 blocks, M101-M148 | `block_register_2026.xlsx` "Blocks" sheet, Day type Mon-Fri -> 48 rows | Yes |
| Pilot blocks (9) | M103, M118, M124, M125, M129, M135, M142, M145, M146 | Cross-tab of `depot_dispatch_log...csv` by fleet numbers 1201-1206 | Yes |
| Night cap | 6.90 MWh (690 kW x 10 h) | Literal read of `charging_connection_agreement_2025.pdf` | Yes |
| Usable-for-planning chain | 480 x (1-0.043) ~ 460; 0.85 x 460 = 391 kWh | Arithmetic over the quotation's 480 kWh and the company's own fitted loss | Yes (internally consistent) |
| Priority + qualify -> 17-block order | M101...M148 as listed | `fleet_plan_2027.xlsx` priority order filtered to the 23 "yes" blocks, first 17 | Yes, exact match, M145 18th |
| Whole-fleet diesel intensity (crude aggregate check) | 48-cell list, 37.2-62.4 | Total diesel litres / total non-electric planned km, Nov 2025-Oct 2026, ~44.9 l/100 km | Inside the plausible range, no contradiction |
| Per-block l/100 km (48 cells), bridge coefficients, loss-curve percentage, charger-efficiency regression, exact night schedule feasibility | as stated | Not independently re-derived to stated precision in the time box | Not checked to precision; no evidence against |

## Competing answers that survived
None found. The thread enumerated the obvious alternates (the pilot's own fit carried on timetable covariates,
the night at the sessions' pooled ratio, battery energy alone, the verdicts summed) and these are exactly the
rival routes the design note's own sensitivity table lists (18, 29, 33, 19, 21, 23) as wrong answers a hurried
or careful-but-hurried run lands on, not competing defensible readings of the prompt. No fork in the prompt or
files was found to admit two licensed operationalizations of the main decision or of any of the five
supplementary asks.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 14 files: 7 CSV, 3 xlsx, 4 PDF (3 categories) | Pass |
| Large messy files | 1 CSV 20,000+ rows, 1 CSV 10-20 printed pages | `depot_dispatch_log...csv` 41,790 rows; `fuel_card_transactions...csv` 20,804 rows (both clear the 20k floor); `workshop_orders...csv` 841 rows x 7 cols (~15-20 printed pages) | Pass |
| Distractors declared outside ZIP, unlabelled inside | 2+ named in metadata.json, no internal label, no build-reveal | `tyre_and_brake_costs_2025.xlsx`, `depot_electricity_invoices_2025-01_2026-10.csv` named in metadata.json; grep across target/ for distractor/generated/synthetic/benchmark/seed/generator returned no hits | Pass |
| Distractors relevant but unused | each used by neither golden nor asks, but plausible | Electricity invoices (whole-depot monthly billing, peak kW up to 376) tempts a solver toward a historical-peak capacity read instead of the connection agreement's filed 690 kW; tyre/brake costs tempts a maintenance-cost comparison; neither appears in any ask, critical component or step | Pass |
| 1-3 deliverables, all present in golden | xlsx + pptx requested and shipped | prompt: "A workbook with the block figures and a few slides for the board"; golden.zip contains exactly `niittyla_ebus_order_2027.xlsx` and `niittyla_ebus_order_2027.pptx` | Pass |
| Asks multi-dimensional, unit stated, no rounding instruction | per CLAUDE.md / memory | prompt.txt carries no rounding instruction; each ask in submission.md states its own precision/band; asks are 48-cell lists and MWh/percent figures, not single lookups | Pass |
| Answer shape (one of fourteen) | a checkable structured set with 4+ independently checkable results | An allocation (17 buses to blocks) with its binding-constraint sensitivity; 9 checkable results (R1-R9) in the design note, 8 graded in the answer blocks (5 asks + 3 critical components) | Pass |
| Golden ZIP exactly the requested files/formats | xlsx + pptx only | `unzip -l golden.zip` -> exactly those two files | Pass |
| Nothing LLM-looking, reads as real work product | per hygiene checks | Judge thread: no LLM-authorship tells, no README/benchmark/provenance leakage in target/; PDFs read as a connection-agreement letter, a sales quotation and an internal standard, dated and addressed consistently with the fiction | Pass |

## Gate G reconciliation
The thread's Gate G line (`mechanism: method_or_model_selection + binding_constraint`, `stumping_family:
analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`) matches the design note's own
framing cleanly. Nothing in DES-1, the connection agreement, the quotation, the fuel-card statement, the
telematics, the charging sessions, or the vehicle register is asserted and then overturned; every reported
figure is taken at face value and the difficulty is building honest models (a selection-aware bridge, a
heater/HVAC decomposition, a degradation curve, a temperature-dependent charger regression) and applying a
genuine binding capacity constraint over the results. The design note's own mechanism language ("a forecast
carried from a selected sample ... a measurement gap read from a second record ... a metered total split into
its causes ... a capacity constraint over the forecasts") is the same shape the thread independently named. No
disagreement to reconcile.

## Gate H reconciliation
The thread's Gate H line (`domain: pass`, `layers: pass`, `results: 5 asks + 3 critical components across >=5
areas`, `one_thing: none`, `effort: quick ~1-2 of 8, careful-but-hurried ~4-5 of 8, thorough 8 of 8`, `one_fact:
"the pilot ran the fleet's thriftiest blocks..." rescues 2-3 of 8`) tracks the design note's `## Results chain`,
`## Hidden factor record` and `## Effort test` closely:

- **one_thing.** The design note's "Not one thing" paragraph states three independent judgments each move the
  order on their own (the bridge: 18 without it at the pooled ratio; the conditioning: 17 of another set without
  it; the heaters' share: 19 without it), and the night's capacity moves the count from 23 to 17 on top of that.
  The thread reached the same conclusion independently, citing the same sensitivity numbers (18, 19, 21, 29, 33)
  and naming no single hidden or planted thing. No divergence.
- **Hidden factor record.** All four constructed factors in the design note (the pilot's selection on diesel
  figures, the fuel-fired heater's hidden load, the charger's mixed-cause meter, the night's shared capacity) are
  marked "no" for sitting only in the deciding units, and each is closed by a routine step called out as
  "modelling" (a bridge estimated and carried, a conversion from a second record, a split by causes with a fit
  knot chosen by fit, an exact flow/least-slack schedule), not a one-line fix. None reads as a shallow hidden
  factor under H3's three-condition test.
- **Effort.** Design note: quick 1 of 9, careful-but-hurried 4 of 9 (R1, R3, R5 Right, R6 Partly), thorough 9 of
  9, pair estimate 49.5. Thread: quick ~1-2 of 8, careful-but-hurried ~4-5 of 8, thorough 8 of 8. The two line up
  within normal estimation noise (both put the quick pass at roughly a ninth to an eighth, well under the
  one-third ceiling, and both put the careful-but-hurried pass at under half). One soft tension: the thread's
  prose suggests a careful-but-hurried run "plausibly gets [the pilot-selection trap] right... visible from one
  group-by," while the design note's own effort table marks R2 (the pilot-gap figure itself) Missed on the
  careful-but-hurried pass, because that pass dismisses the fuel-card file as not measuring battery energy and
  never states the comparison. This is a difference in framing (recognizing the mechanism qualitatively vs.
  landing the graded figure, R2, that depends on actually computing it) rather than a numeric disagreement; the
  thread's own effort numbers (4-5 of 8) do not force a different conclusion. Not a finding against the build.
- **One-fact test.** Design note's largest single hint rescues 3 of 9 (R2, R4, R6; the order still wrong at 18).
  The thread's best single sentence rescues 2-3 of 8. Both comfortably under the one-third bar. No divergence.
- **Bands.** The design note's "Pinned" section runs the honest family (three bridges, two temperatures, three
  age forms, six readings of the charging split, three schedulers) and reports every reading lands inside its
  stated band and the same 17-block order; the thread found no band that excludes a defensible rival and no band
  so wide it fails to separate the hurried figure from the golden. No Gate C finding on any result.
- **Declared distractors.** The thread named `tyre_and_brake_costs_2025.xlsx` and
  `depot_electricity_invoices_2025-01_2026-10.csv` as the two plausible unlabelled distractors and did not find
  either load-bearing in any result. Matches metadata.json's declared pair.

No reconciliation finding moves the disposition.

## Stump power (Gate F)
The thread finds stump power spread across several independent traps rather than concentrated in one: the
pilot's selection-biased sample (naive extrapolation over-qualifies 29-33 blocks), the heater/HVAC
decomposition (needed because the 2027 model heats electrically), the battery-loss curve-form choice (2.96 to
4.86 per cent spread at 12 months), the charger's pooled-vs-temperature-adjusted conditioning draw (pushing a
naive run to 18 buses), and the capacity-constrained, time-windowed night schedule. Its single likeliest loss
for a careful-but-hurried strong model is ask 5 / the night-energy figure, using the sessions' pooled 0.920
ratio instead of the temperature-adjusted one, landing an order of 18 buses (adding M145) and a total MWh figure
roughly 0.3 to 0.5 MWh above the golden's 9.1 MWh. This matches the design note's own run forecast (R7 lost to a
method shortcut, R8 and R9 falling with it) almost exactly.

## Findings, ranked
1. (Process, not disposition-changing) The judge thread's own order-of-work was breached: an early exploratory
   `cat graded_blocks.md` exposed the full graded blocks before `own_derivation.md` was finished. The thread
   disclosed this itself and reports no figure was copied; the strongest independent cross-check it performed
   (the priority-order filter reproducing the exact 17-block set) is mechanical enough that peeking does not
   explain the match away. Recorded for the record; no rebuild required.
2. (Minor, non-disqualifying) A soft tension between the thread's qualitative stump-power narrative (a
   careful-but-hurried run "plausibly" recognizes the pilot's selection bias) and the design note's own effort
   table, which scores R2 (the pilot-gap figure) Missed at that same pass. Both sources' aggregate effort numbers
   agree closely; this is a framing difference, not a numeric disagreement, and does not change the verdict.
3. No gate failure, no competing defensible answer, no banned stumping shape, no Gate H failure found.

## Next action for the author
None required for this pass; if a loop 2 is run for any other reason, re-run the judge thread with explicit
instructions not to `cat` the whole of `graded_blocks.md` in one shot during its initial orientation (page it,
or grep for section headers only) so the order-of-work guarantee holds without needing a post-hoc disclosure.
