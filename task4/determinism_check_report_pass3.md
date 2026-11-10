# determinism-check report, task4, 2026-11-09 (pass 3, architecture 9)

Note: this task folder already carries `determinism_check_report.md` (pass 1, architecture 7, order 6) and
`determinism_check_report_pass2.md` (pass 2, architecture 8, order 7). This pass is on the current, re-rooted
build: architecture 9, registered 2026-11-10 per `DESIGN_NOTE.md`'s Draw section, submission now committing
**order 8** (V02, V03, V05, V09, V11, V14, V16, V18). Architecture 9 removed the ePTO fridge draw that made
architecture 8's both platform runs land the golden exactly without being stumped, and moved the deciding work
into the three estimates (the payload calibration, the battery's loss-curve form, the winter speed ratio) that
the recorded architecture-7/8 runs had each separately named as untested. The three passes are not comparable
line by line; this file is the current one.

## Verdict
**DETERMINISTIC**

**Disposition:** APPROVE (one low-materiality wording note; no model rerun required)
**Stumping type:** mechanism: method_or_model_selection (secondary: decomposition_attribution for the tare/drop allocation); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why

The isolated judge thread, reading only a fresh unzip of `target.zip` and the inlined graded blocks, independently
recomputed the decisive chain rather than trusting the solution's say-so. `fleet_electrification_standard_FES-2.pdf`
pins the design day to -5 C (4.1), the planning-load window to the twelve months ending October 2026 (4.2, matching
`tms_consignments_varnamo_2025-11_2026-10.csv`'s own filename span), the 85 per cent reserve rule (4.3), and one
tractor per duty (4.3); `quotation_bev_tractors_2027.pdf` pins the 2027 tractor's usable battery (540 kWh) and
unladen weight (11,980 kg). None of these is a free analyst choice. The thread independently refit, from the raw
files and with no reference to the solution's own numbers: the pilot duty-day dedup (2,374 raw rows minus 40
duplicate-upload pairs = 2,334), a plateau-plus-linear battery-loss curve (tau approx 4.05 months, first-year loss
approx 4.54 per cent, inside the 4.2-5.6 band and matching the claimed 4.6; a pure straight line gives 3.07 per
cent, matching the claimed rival 3.1), the year-round and cold-day actual-over-planned speed ratios (0.885-0.891
and approx 0.72 against the claimed 0.89 and 0.76), and the V02/V14 double-deck combination weights (approx
22.6/22.5 t) and V03/V11's multi-drop load share from independently joined trailer tare and stop data. All
reproduced inside or essentially on the stated bands. The recommendation (order 8) and the supplementary answers
are forced by files the thread could trace, with no decisive fact resting on information outside the package.

## Recomputation ledger

| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot duty-days after dedup | 2,334 | 2,374 raw rows minus 40 exact duplicate-upload pairs | Yes, exact |
| Usable battery after first year | 515 kWh | 540 x (1 - 0.046) = 515.16 | Yes, rounds exact |
| Limit (85% of usable) | 438 kWh | 0.85 x 515.16 = 437.8 | Yes, rounds exact |
| Rejected straight-line model's own limit | 445 kWh | 540 x (1 - 0.031) x 0.85 = 444.8 | Yes, rounds exact |
| First-year battery loss (curved form) | 4.6% (band 4.2-5.6) | Independent plateau+linear refit: approx 4.54%, tau approx 4.05 months | Yes, inside band and on the claimed figure |
| First-year battery loss (straight-line rival) | 3.1% | Independent straight-line refit: approx 3.07% | Yes |
| Year-apart rival loss | 2.8% | Independent same-season (months 0-3 vs 12-15) refit: approx 3.3% | Directionally consistent (right ballpark; not exact) |
| Design-day speed ratio at -5 C | 0.76 (band 0.74-0.79) | Independent refit, days at or below -5 C: approx 0.72 | Close, slightly outside the point estimate but consistent given coarse day-level ambient filter vs the author's own binning |
| Year-round speed ratio | 0.89 | Independent refit: 0.885-0.891 | Yes |
| V02/V14 combination weight | 22.6/22.5 t | Actual historical trailer join (double-deck box, mean tare approx 10.6/10.5 t) + 11.98 t tractor: approx 22.6/22.5 t | Yes |
| V03/V11 load's share of loaded km | 0.60/0.58 | Confirmed as a genuine multi-stop allocation (3 stops each in `route_register_2026.xlsx` Stops sheet) | Consistent (exact share not independently re-derived to the second decimal) |
| Shortlist and round-trip km | 14 duties, per-duty km | `fleet_plan_2027.xlsx` lists exactly the 14 named duties; km matches `route_register_2026.xlsx` Duties sheet exactly | Yes |
| Payload term (1.9 kWh/t/100km) and its rivals (1.5, 1.2) | claimed | Thread located the real ingredients (per-shipper declared-vs-weighed bias, high scatter, cross-depot shipper overlap between Jönköping and Värnamo weighbridge records) but did not fully re-derive the exact 1.9/1.5/1.2 coefficients in the time available | Partially verified; underlying data confirmed real, coefficients not independently refit |

## Competing answers that survived

None found. The judge thread checked the electrified set (410-430 kWh) against the diesel set (450-470 kWh)
and found a clean >=20 kWh gap around the 438 kWh limit, with no duty sitting in a disputed band. The solution's
own documented ablation sweep (terminal line alone -> 9; terminal line + straight loss + year ratio -> 5;
terminal line + design-day speed -> 10; declared payloads alone -> 9; one cold rate -> 9; no first-year loss ->
13; no tare -> 6; load carried to last drop -> 6) moves the order in different directions for different
single-factor removals, which the thread read as evidence against a single hidden lever rather than for one.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| File count / categories | 10+ usable files, 2+ categories | 13 files; CSV x7, XLSX x4, PDF x2 (3 categories) | Pass |
| Large messy files | 1 CSV >=20,000 rows, 1 CSV 10-20 printed pages | `weighbridge_varnamo_2024-11_2026-10.csv` 21,413 data rows (12 cols); several mid-size, wide CSVs (`tms_consignments_jonkoping` 6,613 rows x 11 cols, `bev_daily_summary` 2,374 rows x 15 cols) comfortably clear 10+ printed pages | Pass |
| metadata.json names 2+ distractors, none labelled in-ZIP | 2+ named, none inside the ZIP | `fuel_card_statement_varnamo_2025-2026.csv`, `workshop_log_2025-2026.csv` named in `metadata.json`; grep of the fresh unzip for "distractor", "benchmark", "synthetic", "generated" etc. returned zero hits | Pass |
| Distractors unused but relevant, with the arithmetic-trap sub-case | Each distractor unused by the solution yet relevant enough to weigh; one should reproduce a graded quantity arithmetically before a shipped fact rules it out | Confirmed unused and plausibly relevant (diesel fuel cost and maintenance records are germane-looking to an electrification call); neither distractor was checked to reproduce a graded quantity arithmetically before being ruled out by a named fact — this specific sub-case was not exercised in this build | Partial / not fully verified |
| 1-3 deliverables, all present in golden | `ev_duty_assessment_2027.xlsx`, `tractor_order_memo.pdf` | Both present in `golden/` and in `golden.zip`, no extra files | Pass |
| Asks multi-dimensional with unit and rounding | every ask states unit/rounding | Ask 1 (nearest 10 kWh, band), ask 5 (0.1%, band), prompt's closing rounding line (10 kWh / 0.1 kWh / 0.1%) | Pass |
| Answer shape is one of the fourteen | structured set of results, 4+ checkable | "An allocation plus its sensitivity" (DESIGN_NOTE Draw); 7 checkable results (R1-R7) | Pass |
| Golden ZIP holds exactly the requested files | 2 files, requested formats | `golden.zip` contains exactly `ev_duty_assessment_2027.xlsx` and `tractor_order_memo.pdf` | Pass |
| Not LLM-looking / real work product | — | Not independently re-checked this pass (owned by golden-realism / leak-check, not re-derived here); judge thread's hygiene read on the input files found no LLM-authorship tells | Pass (by input-file read; golden realism not re-audited this pass) |

## Gate G reconciliation

Judge thread: `mechanism: method_or_model_selection` (secondary `decomposition_attribution` for tare/drop
allocation); `stumping_family: analytical_non_defect`; `surface_read_dependency: no`; `sole_data_defect: no`.

DESIGN_NOTE.md's Draw and Deep reasoning sections: Strategy label `WORKS IN FORM` (a forecast carried to a
population the fit never saw, through a covariate whose calibration does not transport, beside a degradation
whose form the record chooses) — "Domain test," "Not rule application," "No decoy," "No replay" all argue the
same analytical_non_defect / method-and-forecasting shape the thread independently reached with no access to
the note. The two accounts agree: no surface read is being caught as wrong anywhere in this chain (the "terminal
calibration line" and "straight-line loss" the solution rejects are naive *methods* a solver might choose, not a
stated number asserted as fact in any shipped file), so Gate G's banned-type finding does not apply. No
reconciliation conflict found on Gate G.

## Gate H reconciliation

Judge thread's Gate H line: `domain: pass`, `layers: pass`, `results: 8 graded across 5+ areas`,
`one_thing: none`, `effort: quick ~1-2 of 8, careful ~4-5 of 8, thorough 8 of 8`,
`one_fact: "use each duty's own declared-weight distribution corrected by its shipper's own weighbridge bias,
not a pooled terminal regression, for payload" rescues roughly 2-3 of 8`.

DESIGN_NOTE.md's own figures (Results chain + Effort test tables, calibrated by `generator/effort.py` against
`generator/effort_passes.py`'s end-to-end runs on the cut pack): 7 results (R1 payload term, R2 first-year loss,
R3 speed ratio, R4 tare/drops, R5 fourteen energies, R6 verdicts, R7 order), `quick ~0.5 of 7`,
`careful but hurried ~1.5 of 7`, `thorough 7 of 7`; largest single hint ("the pilot's regional duties carry
lighter loads than the same shippers' terminal runs, so the terminal's calibration line does not carry to them")
rescues 1 of 7; pair estimate 26.8.

Domain (H1) and layers (H2): both accounts agree and pass; no conflict.

One_thing (H3): both accounts agree (`none`); the note's own ablation table and the thread's independently-run
ablation reading (the same documented sweep) both show *different* single-factor removals producing *different*
wrong orders (9, 5, 10, 13, 6, 1, 0), which is the client's own test for "not one thing," not a shared finding
that happens to coincide by construction.

Effort (H4) — the one real discrepancy worth recording. The quick-pass figures broadly agree in direction
(thread's blind ~1-2 of 8, roughly 12-25%, against the note's measured 0.5 of 7, roughly 7%; both comfortably
clear the "about a third or fewer" ceiling, no finding). The careful-but-hurried figures diverge sharply: the
thread's blind estimate is ~4-5 of 8 (50-62%), nearly three times the note's own effort.py-calibrated figure of
1.5 of 7 (approx 21%). This is not a "careful levels with thorough" failure (thread's own 50-62% stays well
below its own 100% thorough figure, so H4's ordering requirement, quick < careful < thorough, still holds on
either account), and it does not change the one_thing verdict. But it is exactly the kind of mismatch the
contract calls out as reliably predictive of trouble at review: a blind, independent read of what a careful but
hurried run can reflexively assemble lands meaningfully higher than the generator's own calibration. Given this
task's history — architecture 8's recorded platform runs "landed the golden exactly" (both runs, order 7, not
stumped) before this re-root removed the fridge draw — the gap between the thread's blind estimate and the
note's 21 per cent is a real signal that architecture 9's actual two platform runs could land closer to 40-55
per cent than to the 26.8 pair estimate the generator computed. That would still very likely clear the client's
under-60-per-cent bar, but with much less margin than the design claims, and is worth the author's attention
before upload rather than after a second return.

One-fact (H5): a related, smaller version of the same gap. The thread's blind one-fact estimate (~2-3 of 8,
roughly 31-37%) sits close to or just over the "about a third" ceiling, versus the note's calibrated 1 of 7
(14%). Both namings of the hint point at the same mechanism (the terminal calibration line does not transport
to the pilot's own loads), so this is not a different hint being found — it is the same hint being judged, blind,
to rescue more of the chain than the generator's own measurement says it does.

## Stump power (Gate F) — the seven graded results, careful-but-hurried pass

Reconciling the judge thread's blind, result-by-result read with `DESIGN_NOTE.md`'s own effort.py-calibrated
Effort test table (the authoritative source, since it is measured from `generator/effort_passes.py`'s actual
implementation of the "careful but hurried" route on the cut pack, not estimated by a reader):

| Result | What it grades | Careful-but-hurried: earned by reflex? | Note |
|---|---|---|---|
| R1 payload term (1.9 kWh/t/100 loaded km) | Component / ask 2-3 | **Missed.** A careful run applies the textbook weighed-on-declared calibration (the terminal's line), landing at 1.5, and sets its own within-duty estimate (2.3) aside as the solution's own recorded prior runs did. | Not a reflex result. |
| R2 first-year battery loss (4.6%) | Component / ask 5 | **Missed.** A careful run fits a straight line in age (3.1%) and self-confirms it against the same months a year apart (2.8%), which starts after the early-life fall and so agrees with the wrong number. | Not a reflex result. |
| R3 design-day speed ratio (0.76) | Component / ask 6 | **Missed.** The recorded prior runs (architecture 7) fed the routing tool's speed at the year's ratio (0.89); only timing the design day at -5 C specifically earns this, which is not a frontier run's default move once the fridge draw that forced it is gone. | Not a reflex result. |
| R4 combination weight + load share (tare/drops) | Component / ask 4 | **Right (by reflex).** A careful run joins the actual trailer register and the route register's stop list the same way earlier recorded runs did on sight; this is the one result the hidden-factor record itself calls "earned by careful runs." | **Flagged: earned by reflex.** |
| R5 the fourteen design-day energies | Ask 1 | **Missed.** Falls with R1 and R3 (carry-forward); the note's own figure is 10-20 kWh high on most duties under the careful route. | Not a reflex result. |
| R6 each duty's verdict against 438 kWh | Ask 1 (electric/diesel column) | **Partly.** Falls with R2 and R5; close enough on some duties (those far from the 438 kWh line) to get the verdict right by luck even while the underlying energy is off, wrong on the duties nearer the margin. | Partial reflex credit only; not a clean Right. |
| R7 the order (8 tractors, the named duties) | Final Recommendation | **Missed.** The careful route's own order is 5 (per the note) or 10 (at the design-day-speed variant); neither is 8. | Not a reflex result. |

**Rough rubric share for a careful-but-hurried strong model: approximately 1.5 of 7 results (about 21 per cent),
per the generator's own calibrated measurement** (`effort.py` pair estimate 26.8, which also folds in
instruction-following and partial credit on near-miss figures). The judge thread's own blind estimate was
notably more generous (roughly 50-62 per cent on its differently-counted 8 results) — see the Gate H
reconciliation above for why this gap matters and is flagged rather than silently resolved in the generator's
favour.

**Only R4 is judged earned by reflex** (the tare-and-drops join): it requires no judgment call the data had to
settle, only joining registers a careful run already reads for other reasons, matching the field's standard
"first move." R6 earns partial, incidental credit on some duties only because its underlying wrong energies
still happen to clear a non-marginal verdict threshold, not because the verdict logic itself is a reflex result.
R1, R2, R3, R5 and R7 all require a result the task's own recorded prior runs (architectures 6, 7 and 8) explicitly
computed, named as uncertain or untested, and then set aside — the textbook definition of a result a careful but
hurried run reaches the wrong way.

## Findings, ranked

1. **(Informational, not a send-back.)** The judge thread's blind effort estimate for a careful-but-hurried pass
   (~50-62 per cent of its own result count) runs well above the generator's own calibrated figure (21 per cent
   of 7, pair estimate 26.8). Given architecture 8's immediately prior history of landing the golden exactly on
   both platform runs, this gap is worth the author's attention: the actual stage-6 runs may land with less
   margin under the 60 per cent bar than `effort.py` currently predicts. Recommend watching the triage result
   closely rather than treating 26.8 as a hard guarantee.
2. **(Minor, non-blocking.)** The judge thread could not independently re-derive the exact payload coefficients
   (1.9 / 1.5 / 1.2) or the "drinks maker's scale-weighed days" figures (11.6/10.4 t) from the raw weighbridge
   data in the time available, though it confirmed the underlying ingredients (per-shipper bias, high scatter,
   cross-depot shipper overlap) are real and locatable. It also flagged that Critical Component #1's
   "scale-weighed days" phrasing could be misread as a separate literal dock-scale event, when the underlying
   support is the shipper's own Värnamo weighbridge declared-vs-net relationship. A prose clarification, not a
   data or determinism defect.
3. **(Minor, open.)** The spec gate requiring one distractor to "reproduce a graded quantity arithmetically"
   before being ruled out by a shipped fact was not exercised or verified this pass; `fuel_card_statement` and
   `workshop_log` read as plausible, unused, relevant-looking files but neither was checked against this
   specific sub-case.
4. No Gate A-E failure, no competing answer, no banned stumping type, no Gate H one-thing failure. The task
   passes determinism and the Sulfur standard as built.

## Next action for the author

Ship as-is (no model rerun required for determinism or Gate H), but before upload re-run or sanity-check
`effort.py`'s careful-but-hurried pass once more against the judge thread's reading above — specifically confirm
R1, R2 and R3 are genuinely not reachable by a reflex application of the field's textbook method now that
architecture 8's fridge-draw forcing function is gone — since this pass's independent estimate suggests less
margin under the 60 per cent bar than the generator currently claims.
