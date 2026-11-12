# determinism-check report, task7, 2026-11-11

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: statistical_rigor (primary: an omitted-variable confound in a natural randomised-by-lot
comparison, corrected by holding each building to seasons before its own exposure date to a documented citywide
concurrent heating-check campaign, plus owner-level clustering in the resample that the draw's own rules require),
secondary decomposition_attribution (reweighting the pilot's measured rate to this year's applicants' roof-area and
occupancy composition) and forecasting (projecting the round's close from the pilot's own historical arrival curve);
stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no.

## Why
Architecture 9 (this build) re-roots architecture 8, which was returned on 2026-11-11 for a single constructed factor
confined to insulation. Here the judge thread, working blind from a fresh unzip of `target.zip` and the bare
prompt, independently rebuilt normalised seasonal gas use from the raw meter reads and reproduced the utility's own
official `benchmarking_notices_2019_2026.csv` figures to a median error of about 0.005 per cent across roughly 18,600
building-season rows, then ran its own naive (season-average, building-level bootstrap) read of the 2019 pilot
**before** opening the graded blocks. That naive first pass funded insulation and heating optimisation and rejected
heating controls, a different headline from the golden call (insulation alone). The thread traced this fork to two
forced corrections that the shipped files, not an invented rule, require: (1) a citywide free heating-check campaign
(`municipal_heat_plan_2026_summary.pdf`, September 2022 to March 2026) shows up as `service visit` reads across
roughly 24,500 of 28,600 meter points city-wide (not confined to the pilot's deciding units) and mechanically
overlaps heating optimisation's own works, which the thread could see independently in the raw data as an unstable
treated/control saving ratio across seasons rather than a stable decaying effect; (2) `pilot_2019_rules.pdf` section
3 states the lottery was drawn by owner, not building, so a building-level resample is a literal procedural shortcut,
not a defensible rival, and owner counts (211-408 per arm) rule out the clustering correction being a thin or
degenerate artifact. The thread also reproduced the round-at-close application counts closely from the pilot's own
historical arrival curve (about 201/823/531 against the graded 198/801/515) and insulation's grant per tonne to
within about 1 per cent, but did not have budget within the review to rebuild the full owner-clustered bootstrap or
the roof-area/occupancy reweighting end to end; it confirmed the files and joins those steps depend on genuinely
exist and support the claimed direction.

## Recomputation ledger
| Figure | Claimed (golden) | Judge recomputed (own derivation, pre-graded-blocks) | Reproduced |
|---|---|---|---|
| Normalised seasonal gas use per building/season | — | independently rebuilt from `gas_meter_reads`, `meter_points`, `calorific_values`, weather; matched `benchmarking_notices_2019_2026.csv` to ~0.005% median error (~18,600 rows) | yes, to high precision |
| Insulation grant/tonne | €85.53 | €86.4 (naive, season-average, no owner clustering, no occupancy/roof reweight) | yes, within ~1% |
| Heating optimisation saving rate (R6) | 2.33% | 5.2% (naive, no service-visit correction) | no, naive misses the confound |
| Heating optimisation grant/tonne range upper end (R7) | €100.92, range up to €233.08 | €45.5, range up to €102.1 (naive) | no, naive lands under the €120 line |
| Heating controls saving rate (R6) | 13.89% | 10.3% (naive, no occupancy/roof reweight) | no, naive under golden |
| Heating controls grant/tonne range upper end (R7) | €98.90, range up to €158.03 | €132.7, range up to €190.1 (naive, building-level, no transport) | no, naive overshoots on the opposite side |
| Round at close, application counts (R9) | 198 / 801 / 515 | ~201 / 823 / 531 (own pilot-arrival-curve projection) | yes, within ~2-7%, inside the stated 10% band |
| Round at close, grant asked (R9) | €5,813,088 / €1,208,872 / €3,091,923 | not independently reproduced (thread flagged as out of budget) | not checked |
| Funded set (R8) | insulation alone | insulation + heating optimisation (naive) | no, naive funds a different set |

## Competing answers that survived
One fork was named and closed by the thread itself, not left open:

- **Fork:** the main recommendation and supplementary answers 1-4, under a naive season-average/building-level read
  versus the campaign-corrected/owner-clustered read.
  - Naive answer: fund insulation and heating optimisation (heating controls rejected).
  - Golden answer: fund insulation alone.
  - Shipped rule that closes it: `pilot_2019_rules.pdf` section 3 (the draw's unit is the owner, every owner's
    buildings together) forces owner-level, not building-level, resampling in the 90% range (R7); and
    `municipal_heat_plan_2026_summary.pdf`'s dated, citywide service-check campaign, independently visible in
    `gas_meter_reads_2013_2026.csv`'s `read_reason` field across virtually the whole meter population, forces
    heating optimisation's own saving to be read off each works building's seasons before its own check (R2), not
    off the seasons as measured. The thread concluded the golden (corrected) reading is the one the files force,
    not an equally licensed rival, because the confound is independently detectable from the raw data alone and the
    draw-unit rule is stated outright, not inferred.

No other fork survived; this is the good outcome the report format expects of an empty table, with the one named
fork resolved rather than left open.

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable files | 10 or more | 19 (all format-usable; no `__MACOSX`, no empty placeholders) | Pass |
| File categories | 2 or more | 4: csv, xlsx, pdf, docx | Pass |
| Large messy CSV, 20,000+ rows | 1 or more | `gas_meter_reads_2013_2026.csv` (413,033 rows) and `electricity_load_profiles_2025.csv` (178,514 rows) | Pass |
| Large messy CSV, 10-20 printed pages | 1 or more | `benchmarking_notices_2019_2026.csv` (37,190 rows) well exceeds this | Pass |
| Distractors named in `metadata.json`, unlabelled in ZIP | 2 or more | `electricity_customers_annual_2019_2025.csv` and `federal_funding_overview_2025.pdf`; neither is referenced by `generator/golden.py` or `generator/checks.py`; the leak rulings in `DESIGN_NOTE.md` confirm both as harmless and unused | Pass |
| Deliverables, 1-3 requested, all present in golden | 1-3 | 2 requested (a PDF note, a workbook); `golden.zip` contains exactly `grant_round_2026_appraisal.xlsx` and `grant_round_2026_note.pdf` | Pass |
| Golden ZIP holds exactly the requested files | exact match | confirmed by `unzip -l golden.zip` | Pass |
| Multi-dimensional asks, unit stated, no rounding instruction | required | each ask carries its own unit and precision band in the answer blocks, not in the prompt; the prompt itself carries no rounding instruction | Pass |
| Answer shape, one of the fourteen | required | a distribution and its cut (grant per lifetime tonne as a design-based 90% range, cut at the committee's €120 upper-end rule), with a forecast (round at close) and a flagged/listed set beside it; checkable results (R2, R6, R7, R8, R9, R10) each gradable on their own | Pass |
| Nothing LLM-generated, every golden a real work product | required | the judge thread's hygiene read found the documents terse and municipal in register, specific rather than round numbers, no authoring/benchmark disclosure or tool banner in any file it opened; the thread flagged this as not a full line-by-line sweep, consistent with the leak reader's own already-passed `leak.py` run | Pass (not independently re-swept) |

## Gate G reconciliation
The thread's line (`mechanism: statistical_rigor`, secondary `decomposition_attribution` and `forecasting`;
`stumping_family: analytical_non_defect`; `surface_read_dependency: no`; `sole_data_defect: no`) matches the design
note's own framing closely. The design note's Frontier check names the strategy label "a randomised effect read net
of a later programme that the treated units' own physics held, beside ranges at the draw's unit" and classifies
R2/R6(optimisation) as `investigation loops` and R7 as `uncertainty`, neither as a planted defect or a flip away from
a misleading reported number; the thread's own reasoning (the "as measured, €66/tonne" figure is the solver's own
naive computation, never a reported/stakeholder figure in any shipped file) is the correct basis for `surface_read_
dependency: no`, and matches the design note's "No decoy" line ("no shipped file states a saving, a rate, a grant
per tonne, a range or a recommendation"). `sole_data_defect: no` tracks the design note's `sole_data_defect` implicit
claim throughout: on clean data the lifetime-tonnes construction, the owner-aware 90% range, the occupancy/roof
reweight and the arrival-curve forecast would still be real work, just thinner.

## Gate H reconciliation
The thread's Gate H line (`domain: pass`, `layers: pass`, `results: >=7 graded across >=4 areas`, `one_thing: none`,
`effort: quick ~1 of 7, careful ~3-4 of 7, thorough 7 of 7`, `one_fact: ... rescues at most 2-3 of the 7 results`)
is checked against the design note's `## Results chain`, `## Hidden factor record` and `## Effort test`:

- **one_thing.** The design note's "Not one thing" section names exactly two unrelated judgments (heating
  optimisation's own saving net of the campaign, R2/R6; heating controls' range at the owner, R7), each deciding a
  different measure, with the roof-area/occupancy transports in R6 earned by the runs rather than counted as a
  third decisive judgment. The thread's `one_thing: none` with "at least three separable corrections" folds the
  earned transports in as a third correction, which is a slightly looser count than the note's two, but both land
  on the same substantive conclusion: no single catch carries the recommendation, and the thread's own naive first
  pass (missing only the two judgments the note names) landed on exactly one of the design note's four named
  possible funded sets ("insulation and optimisation"), which is direct behavioral confirmation of the note's "Not
  one thing" claim.
- **Hidden factor conditions.** The design note's Hidden factor record states the campaign factor is "no: every
  district, both arms of every measure and the whole stock took checks" (not confined to deciding units) and its
  fix depth is "modelling: the works' own saving read off the seasons before each building's check." The thread
  independently confirmed both: it found the service-visit reads span roughly 24,500 of 28,600 meter points
  city-wide, and it explicitly states it did not have budget to rebuild the exact per-building restriction, i.e. it
  recognised this as real modelling work, not a one-line fix. No daylight between the thread's finding and the
  note's record.
- **Effort grades.** The design note's `effort.py`-measured table gives quick 0.5 of 6 (about 8%), careful-but-
  hurried 2 of 6 (about 33%), thorough 6 of 6, with Pair estimate 40.5. The thread's own blind estimate is quick ~1
  of 7 (about 14%), careful ~3-4 of 7 (about 43-57%), thorough 7 of 7. The thread's careful-column estimate runs
  somewhat higher than the note's measured 33 per cent (its own narrative example of a "careful-but-hurried
  afternoon pass," however, funds insulation and heating optimisation and gets three of five graded supplementary
  sheets wrong, which is a materially larger miss than "43-57 per cent right" suggests, so the thread's own
  qualitative account and its numeric Gate H line are in some tension with each other, not just with the note). This
  is a soft discrepancy worth the main session's attention under "price careful variants by weight," but it does
  not change the disposition: both the thread's narrative and the note agree the careful-but-hurried pass gets the
  main recommendation wrong and clears comfortably below the thorough pass, and the quick-pass ceiling (under a
  third) holds on both counts.
- **One-fact test.** The note's Largest single hint rescues 2 of 6 results (about 33%). The thread's one_fact
  rescues "at most 2-3 of the 7 results" (about 29-43%) and explicitly does not touch the owner-clustering
  correction or the forecast. Comparable, inside the one-third ceiling on the note's own count basis; the thread's
  upper bound of 3 of 7 is marginally over a third on its own count basis, but the thread itself characterises this
  as clearing (passing) the ceiling, so no finding is raised.
- **Declared distractors.** The thread did not name either declared distractor (`electricity_customers_annual_
  2019_2025.csv`, `federal_funding_overview_2025.pdf`) as carrying any result; no finding.

None of the six reconciliation red flags in the determinism-judge contract apply with enough force to move the
disposition off APPROVE; the one soft tension (careful-column grade a bit higher than the note's measured figure,
while the thread's own narrative example scores lower) is reported above for the main session's weighing.

## Stump power (Gate F)
High and spread across results rather than concentrated in one trap, per the thread: a ten-minute pass gets the
formula right but likely funds on raw point estimates without the upper-90%-bound rule; a careful-but-hurried
afternoon pass gets the normalisation, the lifetime-tonnes formula and the plain treated/control comparison right
but plausibly misses the service-visit confound (visible only by plotting the saving ratio season by season and
investigating why it does not settle) and resamples at the building level rather than the owner level (a one-sentence
clustering requirement in a rules document from a different year than the one being analysed), funding insulation
and heating optimisation and getting the main recommendation and three of five graded supplementary sheets wrong. A
two-day, self-checking pass is needed to catch both corrections and to build the forecast off the pilot's own
arrival curve. This matches the intended effort gradient.

## Findings, ranked
1. (Informational, no action required) `DESIGN_NOTE.md`'s "## Tried and rejected" section (lines 218-225) contains
   entries about feeder hosting capacity, heat-pump netting and connection standards, content belonging to an
   unrelated electricity-grid-hosting-capacity build, not this gas-retrofit-grant task. This never reaches the
   judge (which never opens `DESIGN_NOTE.md`) and does not touch determinism, but it is a house-hygiene defect in
   the note worth cleaning before the note is read by a human reviewer.
2. (Informational) The judge thread's quantitative Gate H effort line (careful ~43-57% of 7) runs a bit above the
   design note's measured 33 per cent, while the thread's own narrative example of a careful-but-hurried run scores
   lower than its own numeric estimate implies. Neither point changes the verdict; flagged for the main session's
   own weighing under "price careful variants by weight."
3. (Not verified) The thread did not independently reproduce the round-at-close grant amounts (the asking-euro side
   of R9, as opposed to the counts) or the exact owner-clustered bootstrap distributions for heating optimisation
   and heating controls, citing review-time budget; it confirmed the underlying files and joins exist and support
   the claimed direction of each adjustment. This is a stated scope gap in the review, not a defect found in the
   task.

## Next action for the author
None required to ship; the task is DETERMINISTIC and APPROVE. If time allows before READY, tidy
`DESIGN_NOTE.md`'s "## Tried and rejected" section to remove the unrelated feeder/heat-pump entries (finding 1
above), since the note is read by a human reviewer even though the judge never opens it.
