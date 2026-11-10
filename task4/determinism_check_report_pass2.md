# determinism-check report, task4, 2026-11-09 (pass 2, architecture 8)

Note: `determinism_check_report.md` already exists in this folder from the prior pass on architecture 7's
submission (order 6: V02, V05, V09, V14, V16, V18). This pass is on a different, re-rooted build: architecture
8, re-registered 2026-11-09, `target.zip` sha256 prefix `19b6bec945fc8f80`, submission now committing order 7
(V03, V05, V09, V11, V16, V18, V33). The two passes are not comparable line by line; this file is the current one.

## Verdict
**DETERMINISTIC**

**Disposition:** APPROVE (one optional, low-materiality in-house note; no model rerun required)
**Stumping type:** mechanism: method_or_model_selection (secondary: binding_constraint, decomposition_attribution); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why

The isolated judge thread independently reproduced the decisive chain from the shipped files rather than from
the solution's say-so. FES-2 4.1 pins the design day to exactly -5 C; 4.2 pins the planning-load window to the
twelve months ending October 2026, matching `tms_consignments_varnamo_2025-11_2026-10.csv`'s own filename span;
4.3 pins the 85 per cent rule; the quotation PDF pins the 2027 tractor's tare (11,980 kg) and usable battery
(540 kWh). None of these is a free analyst choice. The thread recomputed, from the raw files and not the
solution blocks: the pilot duty-day dedup (2,374 raw rows, 40 duplicate-upload pairs dropped, 2,334 left), the
stop-by-stop ton-km share V03 and V11's loads ride (0.60 and 0.57), the per-shipper declared-to-weighed
calibration slope (0.14-0.21 for 5 of 6 shippers, with the dairy shipper BMJ a genuine 0.85 outlier that the
solution itself names rather than hides), the ePTO equipment-code logic from `fleet_register_2026.xlsx` (only
"TRU SR-60e ePTO" trailers draw from the tractor battery), and the 442 kWh limit arithmetic (540 x 0.962 x 0.85
= 441.7, rounds to 442). All reproduced. The main recommendation (order 7: V03, V05, V09, V11, V16, V18, V33)
and all eight committed answers are forced by files the thread could trace, with no decisive fact resting on
information outside the package.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot duty-days after dedup | 2,334 | 2,374 raw rows minus 40 duplicate-upload pairs = 2,334 | Yes, exact |
| V03 load rides share of loaded km | 0.60 | mean 0.605 / median 0.602 across 128 days, stop-by-stop ton-km | Yes |
| V11 load rides share of loaded km | 0.57 | mean 0.567 / median 0.574 across 128 days | Yes |
| Declared-to-weighed calibration slope | 0.14 to 0.2 t per declared tonne | TEN 0.206, HWP 0.198, GDR 0.168, LBY 0.171, VGL 0.137; BMJ 0.850 (dairy outlier, named by the solution itself) | Yes for 5 of 6 shippers; the sixth is the solution's own disclosed exception |
| ePTO-only draw on tractor battery | SR-60e ePTO draws; SR-60 D/D+SB and AX-40 AGen do not | Confirmed directly from `fleet_register_2026.xlsx` Equipment column | Yes |
| V02 / V14 combination weight | 22.7 / 22.5 t | 22.664 / 22.460 t under frequency-weighted mean tare (rounds to the claimed figures); a simple average of distinct trailers used gives 22.64/22.47 t (rounds 22.6/22.5) | Yes under the stated convention; a second, undocumented convention lands 0.1 t lower for V02 (see Competing answers) |
| Planning-load window | Nov 2025 to Oct 2026 | Matches `tms_consignments_varnamo_2025-11_2026-10.csv`'s own literal span and FES-2 4.2 | Yes, pinned not chosen |
| Design-day temperature | -5 C | FES-2 4.1 states it exactly | Yes, pinned not chosen |
| Winter speed ratio at -5 C | 0.77 | 0.765 to 0.790 across reasonable +/-1 to +/-2 C windows around -5 C; year ratio 0.894 matches claimed 0.89 | Yes, within a defensible band |
| Battery limit | 442 kWh | 540 x (1 - 0.038) = 519.5; x 0.85 = 441.7, rounds to 442 | Yes, exact |

## Competing answers that survived

One low-materiality fork the thread found and the design note's fork table does not close: the duty combination
weight (ask 4, "Sheet Trailers and drops") can be computed as the mean tare of a duty's trailers weighted by each
trailer's share of the duty's actual departures (the golden's apparent convention, giving V02 22.7 t) or as a
simple average of the distinct trailers a duty has pulled (giving V02 22.6 t). This is a real, defensible
alternative operationalization that is not named in the Semantic fork table (SF27 covers which trailer list to
use, SF33 covers the tare source, but neither covers the averaging rule across multiple trailers). It changes
only the descriptive tare figure by about 24 kg, well inside the energy model's 10 kWh rounding and inside the
tare coefficient's own precision; it does not move any duty's design-day energy by a graded amount and flips no
duty's electric/diesel verdict or the order of 7. Not disqualifying, but a genuine unclosed fork worth a one-line
pin.

No other competing answer survives. The five documented hurried shortcuts (declarations-only payload, carried-
to-last-drop, no tare term, no speed term / year's ratio, one cold rate / no first-year loss) each land on a
different, specific wrong order (8, 5, 9, 0/4/9, 9 tractors respectively), which is evidence the order of 7 is
not sitting on a knife-edge against ordinary alternative readings of the same files.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10+ (system files excluded) | 13 files in `target.zip`, all usable | Pass |
| File categories | 2+ | CSV x6, XLSX x4, PDF x2: 3 formats | Pass |
| Large messy CSV, 20,000+ rows | 1 | `weighbridge_varnamo_2024-11_2026-10.csv`, 21,417 data rows | Pass |
| Large messy CSV, 10-20 printed pages+ | 1 | `tms_consignments_varnamo_2025-11_2026-10.csv`, 18,074 rows, ~1.6 MB (several hundred printed-page equivalents), used directly in R5/R6 | Pass |
| metadata.json names 2+ distractors, none labelled inside the ZIP | 2+ | `fuel_card_statement_varnamo_2025-2026.csv`, `workshop_log_2025-2026.csv`, named only in `metadata.json`; no label inside `target.zip` | Pass |
| Each distractor relevant, unused, keyed so no accidental join | required | Both key on `vehicle_reg`/`fleet_no` (e.g. "XDX 934", "BEV-03"), not the shortlist's Vnn duty codes used by every graded file; plausible fleet operational artifacts (diesel fuel card, workshop job log) an analyst would open and set aside | Pass |
| 1-3 deliverables, all present in golden, no forced format family | required | `ev_duty_assessment_2027.xlsx` and `tractor_order_memo.pdf`, exactly the two requested, present in `golden/` and `golden.zip` | Pass |
| Asks multi-dimensional with unit/rounding stated | required | Prompt states "nearest 10 kWh," "0.1 kWh," "0.1 per cent"; 14-duty spreadsheet plus 7 sub-sheets, not a stacked lookup | Pass |
| Answer shape, one of the fourteen | required | Allocation (7 tractors to 14 duties) with its sensitivity (what each of 5 shortcuts would order instead) | Pass |
| Golden ZIP holds exactly the requested files, in the requested formats | required | `golden.zip`: exactly `ev_duty_assessment_2027.xlsx` and `tractor_order_memo.pdf` | Pass |
| Nothing LLM-shaped; goldens read as real work product | required | Judge grepped for synthetic/generated/benchmark/llm/claude/gpt across all files: zero hits; xlsx creator/modified metadata distinct per file and plausible | Pass |

## Gate G reconciliation

The judge's classification (`method_or_model_selection` + `binding_constraint` + `decomposition_attribution`,
`surface_read_dependency: no`, `sole_data_defect: no`) matches the design note's own strategy label, "WORKS IN
FORM (a forecast carried to a population the fit never saw, through covariates whose values for the new units
are themselves estimates from other registers)," and its explicit "Not rule application" / "No decoy" / "No
replay" lines. No reconciliation gap on Gate G: nothing in this build is a reported/surface figure the solver
must catch is wrong and reject; the difficulty is building the forward estimate honestly under a stated 85 per
cent constraint.

## Gate H reconciliation

Comparing the thread's findings against `DESIGN_NOTE.md`'s Results chain, Hidden factor record and Effort test:

- **`one_thing`: the thread said `none`, matching the note's "Not one thing" claim** that the strongest single
  piece (the winter speed ratio) rescues only 1 of 8 results. No gap here: the thread independently named the
  same five-way spread of hurried shortcuts the note documents (declarations-only, carried-to-last-drop, no
  tare term, no/wrong speed term, one cold rate), landing on five different wrong orders, and attributed its
  "strongest candidate stump" to the drop-allocation term, which the note's own Hidden factor record marks
  "modelling" fix depth and explicitly not confined to the deciding units (present across 4 pilot duties and 22
  Värnamo duties). Consistent.
- **Effort grades diverge from the note's calibration, a real finding.** The note's Effort test table, measured
  by `effort.py` on the cut pack, puts the careful-but-hurried pass at 2 of 8 results (quick ~0.5/8, thorough
  8/8). The thread's independent estimate puts careful-but-hurried at 4-5 of 8 (plausibly earning the ePTO term
  and the basic payload/tare split while still missing the drop allocation or the speed/temperature form). Both
  stay well short of the thorough pass's 8/8, so this does not trigger the "careful pass levels with the
  thorough one" send-back signal, but it is a genuine gap between the generator's measured calibration (based
  partly on architecture 7's two actual platform runs, before the tare/drops/ePTO judgments were added) and an
  independent reader's judgment of what a careful-but-hurried solver plausibly clears under architecture 8. Worth
  the author's attention: if the thread's read is closer to how the next two platform runs actually behave, the
  task may score a touch easier than the paper estimate (pair estimate 39.3) suggests, though still comfortably
  under the 60 per cent bar on either reading.
- **One-fact rescue count: the thread's best single sentence rescues more results than the note's own stated
  figure.** The note's "Largest single hint" line claims the duties-drive-slower sentence rescues 1 of 8 results.
  The thread's one-fact test names a different sentence ("a multi-drop load does not ride its full loaded run —
  allocate it stop by stop") and counts it rescuing about 2 of 8 results (the duty assessment energies and the
  trailers-and-drops sheet). This is the Gate H reconciliation signal that most reliably predicts a send-back
  under the contract (the thread's best single sentence rescuing more than the note's stated largest hint), so
  it is flagged explicitly here. In absolute terms 2 of 8 (25 per cent) is still comfortably under the roughly
  one-third ceiling H5 sets, so it does not on its own change the verdict or disposition, but the note's own
  "Largest single hint: ... rescues 1 of 8" line is understated relative to an independent reader's assessment
  and should be corrected to reflect the drop-allocation sentence as the actual largest lever.
- **No band excludes a defensible rival on a graded figure.** The one fork the thread found outside the note's
  fork table (the trailer-tare averaging convention for ask 4's combination-weight figure) sits in a
  non-graded-tolerance descriptive cell (24 kg against a tare term carried at kWh-level rounding) and does not
  reach any duty's design-day energy by a material amount; it is not a Gate C failure on a graded result.
  Recommend adding it to the Semantic fork table as a new row (alongside SF27 and SF33) closed "same call,
  within 0.1 t" so the convention is pinned rather than implicit.
- **No declared distractor was found to carry a result.** The thread confirmed both distractors key on
  identifiers (`vehicle_reg`, `fleet_no`) outside the shortlist's duty-code scheme and produced no hits when
  checked against the graded duties.

## Stump power (Gate F)

The thread assessed the task as not too easy: FES-2 and the quotation hand over the governing rule and the two
headline numbers (85 per cent, the 11.98 t tractor), but the actual design-day energy for each duty needs an
energy model built from four separate pieces of real analysis nothing in the files states outright (payload
calibration against the weighbridge, drop-by-drop load allocation, tare-on-every-leg accounting, ePTO
identification by equipment code, a holdout-validated cold-weather form, and a winter speed-slowdown term). The
five documented wrong-order shortcuts (8, 5, 9, 0/4/9, 9 tractors) show several independent, plausible,
textbook-adjacent ways a careful-but-hurried run drifts off the correct order of 7, spread across different parts
of the chain rather than concentrated in one trap.

## Findings, ranked

1. (Informational, not disqualifying) The note's "Largest single hint" line (1 of 8) undercounts the thread's
   independent one-fact rescue estimate (2 of 8, the drop-allocation sentence). Correct the note's line; no
   change to verdict or disposition since 2 of 8 is still under the one-third H5 ceiling.
2. (Informational, not disqualifying) The note's careful-but-hurried effort grade (2 of 8) is notably lower than
   the thread's independent estimate (4-5 of 8). Both clear the quick/thorough separation the client's H4 test
   wants; flagged for the author's awareness ahead of the next platform-run pair, not a send-back trigger.
3. (Minor, FIX_NOW-eligible) The trailer-tare averaging convention behind ask 4's V02/V14 combination-weight
   figures is a real fork (frequency-weighted mean vs simple mean of distinct trailers) that the Semantic fork
   table does not name. It is immaterial to every graded energy figure and verdict but should be pinned with a
   one-line fork-table row for completeness.
4. No Gate A-E failure, no Gate G banned-type finding, no Gate H send-back trigger.

## Next action for the author

Add one row to the Semantic fork table ("the duty's combination tare across multiple trailers: frequency-weighted
by departures, or a simple mean of distinct trailers; same call, within 0.1 t") and correct the Effort test's
"Largest single hint" line to credit the drop-allocation sentence with rescuing 2 of 8 results rather than 1. Both
are documentation-only; no change to the generator, the prompt, the pack or a rerun is required, and the build can
proceed to READY on this submission.
