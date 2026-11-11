# determinism-check report, task10, 2026-11-10 (pass 2)

Cut: target.zip sha256 `15f8ba39cfb270b72958f5d36eae445f5ff9d71ce836ecdb24135ae0256991c5` (confirmed by a
fresh unzip at `/tmp/determinism-check-task10-1794358265/target/`, matching the user-stated prefix). This is a new
cut, distinct from the prior `determinism_check_report.md` (sha `a40205c5...`), built after the platform returned
architecture 7 for a loosely pinned commit/hold split; this pass is on the levelled-up cut with the three new
decisions (R11 further-MW, R12 Ashcombe Road's schedule, R13 Hartwell Common's data hall) and guideline 7's
tightened share-of-design-days wording. One isolated thread (general-purpose, Sonnet, medium effort) read only
under that scratch directory and `graded_blocks.md` beside it, never `submission.md`, `DESIGN_NOTE.md`,
`metadata.json`, `pipeline.json`, or the prior report. It wrote `own_derivation.md` before opening
`graded_blocks.md` (order confirmed, "Order kept: derive-first, then opened graded_blocks.md").

## Verdict
**DETERMINISTIC** (no SOLUTION_WRONG)
**Disposition:** APPROVE (the thread's disposition, verbatim: "no in-house repair identified; see one caveat under
Evidence on the Hartwell-Common-plus-data-hall margin, which is close but not disqualifying, and is worth a human
eyeball before upload rather than a forced rework"). I agree: the Gate G/H reconciliation below finds nothing that
would change this.
**Stumping type:** mechanism: method_or_model_selection (with elements of binding_constraint on the marginal-flex
and Ashcombe-schedule asks, and decomposition_attribution on the rebound/peak-timing shift), stumping_family:
analytical_non_defect, surface_read_dependency: no, sole_data_defect: no

## Why
The thread's words: the prompt's population ("the Halverton constraint managed zone primaries") is independently
forced to exactly 5 of the 9 Appendix A primaries, confirmed from the award notice's section 2/4 and the flexibility
asset register's 29-zone roster (the other four primaries carry no 2027/28 CMZ at all), and the solution's asks use
exactly this population. Every committed figure traces to a named file and a stated, reproducible method, and the
thread independently reproduced the structural facts that gate the decision: firm capacities and contracted MW
(Appendix A / award notice, exact match), the fact that no 2027/28 flexibility-register row yet shows
`commissioning_test_passed` (so "MW in service by 15 Jan 2028" is necessarily a projection from `planned_commissioning`
via the historical class-level lag, not a lookup), the service-contaminated 2025/26 cold-day record (no working
weekday without a service in 2025/26 was colder than about 0.3C, so the design-day cold end must be modelled from
the service-free mornings, not read off a single raw day), and a real, non-obvious load-growth mechanism at
Charlecote Way (a cold-store customer energised just before the base-year assessment date, still mid-ramp).

## Recomputation ledger
The thread ran a medium-effort pass: it fully reproduced the structural/lookup figures bit-for-bit and verified the
modelled figures (R1 to R13) for methodological soundness and file traceability rather than re-running the
generator's >=100,000-day Monte Carlo from scratch. That is an explicit, stated limitation of this pass (not a
finding against the task).

| Figure | Claimed | Judge's check | Reproduced |
|---|---|---|---|
| Firm capacity (Appendix A), five primaries | 27.5 / 25.6 / 20.0 / 35.0 / 24.4 MW | Exact match, no computation needed | Yes |
| 2027/28 contracted MW | 21.0 / 8.5 / 6.0 / 13.0 / 4.0 | Exact match to award notice | Yes |
| CMZ population | Ashcombe Road, Charlecote Way, Dunmore Street, Fenwick Street, Hartwell Common (5 of 9 Appendix A primaries) | Independently derived from the award notice + asset register's 29-zone roster before opening the blocks; the other 4 primaries have no CMZ award | Yes |
| MW in service by 15 Jan 2028 requires a lag projection, not a lookup | Register snapshot shows 0 of 126 2027/28 rows with `commissioning_test_passed` | Confirmed: this is forced to be a forecast from `planned_commissioning`, stratified (solution: by asset class, 29 to 248 day medians) | Yes, method sound |
| Charlecote Way's 4.5 MW growth addition | A 3,100 kVA cold-store customer (Garside Business Park) energised 15/12/2025, still ramping | Traced to the named customer and its energisation date; a later 650 kVA "Accepted" customer (Elsdon Gardens, planned 05/07/2028) correctly excluded as past the 15 Jan 2028 cutoff | Yes |
| Cold-end design-day demand (R1) | Regression through service-free mornings, not a single raw day or straight-line fit | Confirmed the fork exists (no working weekday without a service in 2025/26 was colder than ~0.3C at Dunmore Street) and that the solution's kinked-regression closes it over the weaker straight-line rival (21.5 vs 22.2 MW), consistent with the design note's SF7/R1 row | Yes, fork closed correctly |
| Hartwell Common with data hall, nine-days-in-ten (R13) | 23.8 MW (band 23.5 to 24.3) against 24.4 firm | Not re-run through the Monte Carlo; checked that the solution's own named-and-rejected alternatives (2.4 MW at established share -> 25.9 MW; 3.8 MW at agreed capacity -> 27.3 MW) are both clearly over firm capacity and are correctly rejected by the same build-up evidence used at Charlecote Way | Method sound; **flagged, not failed** -- see below |
| Monte Carlo figures (R8 to R12, R14) | Expected peaks, nine-days-in-ten levels, shares of design days | Checked for internal consistency against Appendix A / the award notice, not re-derived from a from-scratch simulation (stated limitation of a medium-effort pass) | Not independently re-derived to the decimal |

## Competing answers that survived
None survived as a different committed answer. The thread itself raised four candidate forks before opening the
blocks and checked whether the solution closes each one:
1. Design-day selection (nearest single day near -3.0C vs a temperature regression) -- closed by the solution's
   regression method, which is the standard DNO approach and the only one usable given the service contamination.
2. Commissioning projection (literal `planned_commissioning` vs lag-adjusted) -- closed by the solution's
   class-stratified lag model, grounded in 1,045 already-commissioned rows.
3. Hartwell Common data-hall power-factor/ramp convention (full nameplate from day one vs a build-up curve) -- the
   thread initially flagged "the files give no ramp profile" for a hypothetical new customer, but on reading the
   blocks found the solution applies the same type-level build-up curve (derived from six real data halls in the
   settlement summary, 0.61 kW per kVA established, 15 per cent drawn at 5.5 months) used elsewhere in the chain for
   growth-register customers (guideline 4) -- a forced, non-arbitrary extension of a data-grounded convention, not
   an invented assumption. The thread's one remaining caveat is the resulting margin (see below), not the method.
4. Population scope (5 CMZ primaries vs all 9 Appendix A primaries) -- closed by the award notice and the asset
   register before the thread ever opened the blocks; the solution uses the same 5.

One item flagged as worth a human re-check rather than a determinism failure: **Hartwell Common with the data hall**
(R13) clears firm capacity by only 0.1 MW at the stated band's upper edge (23.5 to 24.3 against 24.4 firm). The
thread classifies this as a thin-but-clean margin (Gate C pass), not a thin-and-contested one, because the
solution explicitly names and rejects the two higher competing readings (established share, agreed capacity) with
grounded evidence rather than leaving them unaddressed. This matches the design note's own closure-table claim
(Axis 9: "no primary within 0.74 MW of firm capacity at the nine-days-in-ten level across the variants") only in
the aggregate; R13 specifically is the single tightest margin in the whole chain and is the one line a reviewer
should look at first before upload.

## Spec gates

| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 14 (2 PDF, 6 CSV, 5 XLSX; no system files, no `__MACOSX`, no empty placeholders) | Pass |
| File categories | 2 or more | 3 (PDF/text documents, CSV, spreadsheet/XLSX) | Pass |
| Large CSV (20,000+ rows) | 1 or more | `primary_demand_halfhourly_2023-2026.csv`, 196,241 lines | Pass |
| Messy CSV (10 to 20 printed pages or more) | 1 or more | `flexibility_asset_register_2026-11-04.csv`, 1,576 rows x 12 columns (well over 20 pages printed); `flexibility_events_2023-2026.csv` (361 rows x 11 cols) is a second candidate | Pass |
| Distractors named in metadata.json, unlabelled in the ZIP | 2 or more | 3: `customer_interruptions_2025-26.xlsx`, `primary_transformer_condition_2026.xlsx`, `duos_charging_statement_2027-28.pdf`; none named anywhere inside `target/` | Pass |
| Each distractor relevant-but-unused; one reproduces arithmetically and is ruled out by a shipped fact | Required | `primary_transformer_condition_2026.xlsx` (DGA/health-index data) looks like firm-capacity input but Appendix A already states firm capacity from "the 2025 thermal assessment" directly, ruling the transformer-condition route out by a named shipped fact; the other two (interruptions, DUoS charging) are plausible and unused | Pass |
| Deliverables, 1 to 3, all in the golden | Required | 2: `halverton_primary_assessment_2027-28.xlsx`, `capex_review_2027-28.pptx`; `golden.zip` holds exactly these 2 files | Pass |
| Asks multi-dimensional, unit stated, no rounding instruction in prompt | Required | Each ask spans 5 primaries x several computed MW/percent figures; `prompt.txt` names "MW" throughout and states no rounding (the answer blocks carry precision and bands) | Pass |
| Answer shape, one of the fourteen, 4+ checkable results | Required | 14 checkable results (R1 to R14 in `DESIGN_NOTE.md`'s results chain), a decision list of 5 primaries each with a reinforce/hold call, a nine-days-in-ten level, a share of design days over firm capacity and a flexibility alternative -- closest to a flagged set with its exceedance rate alongside a forecast path | Pass |
| Golden ZIP holds exactly the requested files/formats | Required | `golden.zip`: `halverton_primary_assessment_2027-28.xlsx` + `capex_review_2027-28.pptx`, matching the prompt's "a workbook and a few slides" | Pass |
| Nothing LLM-generated, golden reads as real work product | Required | Judge's hygiene check: PASS, no LLM tells, no README/provenance/benchmark leakage, no post-dated decisive facts | Pass |

## Gate G reconciliation
Thread's line: `mechanism: method_or_model_selection, stumping_family: analytical_non_defect, surface_read_dependency: no, sole_data_defect: no`. There is no stated/reported figure anywhere in the prompt or the shipped files for a solver to trust and then have to catch as wrong; every committed number must be built up from raw metered, event or register data. The clean-data test the thread ran (would this still stump on perfectly accurate data?) says yes, because the service-contaminated design day, the customer ramp-up curve, the commissioning lag and the rebound are all real properties of the simulated process, not an injected defect. This matches the design note's own "Not semantics" and "Not rule application" paragraphs and its Hidden factor record, where every listed factor's verdict is `keep` with `found by: modelling` (never "found by one look"), consistent with `sole_data_defect: no`.

## Gate H reconciliation
Design note's Gate H self-report: `domain: pass` (the field's own forecasting and capacity-assurance judgments, confirmed by the thread's own swap test -- a hospital/ward-staffing rewrite loses the design temperature, the service window, the build-up curve, the commissioning test and the rebound, so none of the 14 results survive the swap), `layers: pass` (Layer 1: SCADA point renames, mixed legacy/direct feeder keys, provider-name case drift, un-commissioned 2027/28 register snapshot, two-row switching transfers; Layer 2: design-day regression, customer build-up, commissioning-lag projection, rebound regression, Monte Carlo, marginal-flex and schedule optimisation), `results: 14 graded results across at least 7 of the 14 areas` (causal reasoning, missingness/measurement, forecasting, modeling, investigation loops, uncertainty, synthesis), `one_thing: none`, `effort: quick ~1.5 of 14, careful ~7 of 14, thorough 14 of 14`, `one_fact: the come-back sentence ("the load that comes back after the window is in proportion to what the window delivered, and the design day delivers several times what the record's events did") rescues 4 of 14 (R7, R11, R12, R14)`.

The thread's independent Gate H line (on the 9 graded asks it worked against): `domain: pass`, `layers: pass`, `results: 9 graded asks across >=5 areas`, `one_thing: none`, `effort: quick ~1-2 of 9, careful ~4-5 of 9, thorough 9 of 9`, `one_fact: "the flexibility service already ran on the cold 2025/26 days near -3C, so the raw metered design day is contaminated" rescues at most 1-2 of 9`.

Checking the two against each other and against the client's send-back triggers:
- **one_thing**: both say `none`; no single hidden or planted thing carries most of the graded results. The design note's Hidden factor record lists five constructed-but-real factors, each verdict `keep`, each found "by modelling" and explicitly stated to sit across every primary/customer type/asset class, never only in the deciding units (the house's stricter rule). No disagreement.
- **Effort levels**: the thread's quick pass (~11 to 22 per cent of 9) and the note's quick pass (~11 per cent of 14) agree; the thread's careful-but-hurried (~44 to 56 per cent of 9) and the note's (50 per cent of 14) agree closely. Neither pass leaves the quick solver above a third, and neither levels the careful pass with the thorough one. No reconciliation flag.
- **One-fact test**: the thread's best single sentence (1 to 2 of 9, roughly 11 to 22 per cent) rescues *fewer* results than the note's own declared "Largest single hint" (4 of 14, about 29 per cent, the come-back sentence, not the cold-end sentence the thread independently landed on). This is the safe direction -- the thread did not find a bigger single-sentence lever than the design note already disclosed and priced; it is not the "thread's best sentence rescues more than the note says" pattern that predicts a send-back.
- **Hidden factor carried only in deciding units**: none of the five recorded factors is confined to the deciding units per the note's own table (each is explicitly checked across every primary/customer type/class/provider); the thread's own-derivation did not find one either.
- **Declared distractor carrying a result**: the thread confirmed all three named distractors are unused by any committed figure, consistent with the note's "14 files, three of them never read by the assessment."
- **Band excluding a defensible rival, or a band too wide to separate hurried from thorough**: the thread ran four forks (design-day method, commissioning projection, data-hall ramp convention, population scope) and found the solution's reading inside the stated band or closed by named data in every case; the one band flagged as tight (R13, Hartwell Common with the data hall, 0.1 MW of headroom at the band's edge) is tight but not excluded -- the solution's own rejected alternatives (2.4 MW, 3.8 MW) sit clearly outside the band on the wrong side, which is the evidence a band is supposed to produce, not a sign it is too wide to grade.

No Gate G or Gate H finding here would move the disposition off APPROVE; the one item worth a human's attention before upload is the R13 margin, which is a review flag, not a send-back trigger.

## Stump power (Gate F)
The thread's assessment: strong. At least five genuinely different "hurried shortcut vs. correct method" pairs exist (design-day regression form, customer ramp-up vs. flat latest-reading, per-class commissioning lag vs. planned-date or single overall lag, provider rebound regression vs. raw event replay, and the resulting Monte Carlo), and the solution names the specific wrong numbers each shortcut produces and which primaries it would wrongly add or drop. A careful-but-hurried run plausibly gets the demand-growth and design-day pieces right but misses the commissioning-lag, rebound, and marginal-flex-doesn't-help pieces, landing on a wrong primary list or a wrong Ashcombe Road/Hartwell Common answer. This matches the design note's own run-forecast paragraph (both architecture 7 responses lost on the come-back and, for one response, the cold-end form) and its "9 independent judgments, depth level 5" claim.

## Findings, ranked
1. **Hartwell Common with the data hall (R13) is the tightest margin in the build** (23.8 MW claimed, band 23.5 to 24.3, against 24.4 firm capacity; 0.1 MW of headroom at the band's edge). Not disqualifying -- the solution explicitly names and rejects both higher competing readings with grounded evidence -- but it is the single line a human reviewer should re-check against the generator's own Monte Carlo output before upload.
2. The judge thread's medium-effort pass did not re-run the generator's own >=100,000-day Monte Carlo; the nine-days-in-ten and share-of-design-days figures (R8 to R12, R14) are judged on method soundness and file traceability, not bit-for-bit reproduction. This is a stated scope limit of the pass, not a finding against the task; the design note's own independent rebuild (`verify.py`, 18 of 18 figures inside band) and its 17-variant sweep are the stronger evidence on that front and were not contradicted by anything the thread found.
3. No fork, hidden factor, or distractor the thread checked survived as a disqualifying issue; every one closed inside the stated band or was ruled out by a named file.

## Next action for the author
Spot-check R13 (Hartwell Common with the 4,000 kVA data hall) against `generator/effort.json` / the Monte Carlo output one more time to confirm the 23.8 MW central estimate and its 23.5 to 24.3 band genuinely clear 24.4 MW firm capacity under the full `checks.py` variant sweep, since it is the thinnest margin in the chain; no other repair is needed, and the build can proceed to READY at this cut (sha `15f8ba39cfb270b7...`).
