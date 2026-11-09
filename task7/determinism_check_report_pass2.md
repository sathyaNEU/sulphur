# determinism-check report, task7, 2026-11-09

Pass 2 (stage 4, architecture 7: the Haldenau grant round rebuilt as a results chain after the 2026-11-09
platform review returned architecture 6 for turning on one thing). `determinism_check_report.md` (pass 1,
2026-11-08) is against the superseded architecture-6 pack and is kept as the prior pass; it is not
overwritten. Isolated judge thread's full verdict: `/tmp/determinism-check-task7-1794252635/verdict.md`
(scratch path, not retained after this session). target.zip sha256 prefix verified: 00c9970f9f34a9eb.

## Verdict
DETERMINISTIC
**Disposition:** APPROVE
**Stumping type:** mechanism: method_or_model_selection + decomposition_attribution + forecasting; stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no

## Why
The judge thread independently rebuilt the chain from the shipped files (before reading the submission's
claimed answers in detail) and reproduced every load-bearing figure to within rounding: the pilot's
3,055/1,375/1,338 counts, the 655 funded applications after deduping the 36 revised rows, grant-per-tonne
of roughly €88/€157-158/€99, the 11.7/3.0/5.8 per cent flip rates exactly, the 36/53/80 per cent same-day
response rates and the ~340/470/660 round-at-close counts, and the 40 per cent late-insulation size premium
with 4.2/8.9 per cent withdrawal rates. The main recommendation (fund insulation and controls, not heating
optimisation) and all nine supplementary figures are forced by formulas stated in
`climate_action_plan_2023_extract.pdf` sec 4.4, `grant_offer_2026_terms.pdf` and `pilot_2019_rules.pdf`,
applied to the shipped meter, pilot and application data; the two "obvious" naive readings (the pilot's own
building mix for controls, ~€162/t; heating optimisation's seven-season average carried flat, ~€108/t) are
both excluded by data the files themselves supply (this year's applicant use-mix vs. the pilot's, and the
visible plateau in the pilot's own seasonal series from season 4), not by an outside rule. Gates A-E pass
for the main call and for supplementary answers 2-9.

## Recomputation ledger
| Figure | Claimed | Judge recomputed | Reproduced |
|---|---|---|---|
| Pilot responses/drawn/completed | 3,055 / 1,375 / 1,338 | 3,055 / 1,375 / 1,338 | Yes |
| Funded applications (insulation + controls) | 655 | 123 + 532 = 655 (after keep-latest dedup of 36 revised rows) | Yes |
| Grant per tonne: insulation / optimisation / controls | €88 / €158 / €99 | €88.0 / €156.3 / €99.2 | Yes (within rounding; small gap from a uniform-vs-per-use-fade rate) |
| Funded grant total / lifetime tonnes (ask 8) | €3,050,000 / 33,030 t | €3,051,700 / 32,998 t | Yes (within rounding) |
| Flip rates (ask 6) | 11.7% / 3.0% / 5.8% | 11.66% / 3.03% / 5.78% | Yes, exact |
| Same-day response rate by measure (ask 7 basis) | 36% / 53% / 80% | 35.8% / 53.1% / 80.5% (23-day cutoff, 2026 notice date applied to 2019 pilot) | Yes |
| Round-at-close application counts (ask 7) | ~340 / ~470 / ~660 | ~344 / ~465 / ~661 | Yes |
| Late-insulation size premium / withdrawal rates (Critical Component 4) | 40% larger / 4.2% early, 8.9% late | 39.6% larger / 4.2% early, 8.9% late | Yes, exact |
| Season-by-season gas-use panel (ask 2-4 basis, 389,105-row meter file) | 14.8-16.8% / 11.8-1.2% / 5.2-4.0% | Not independently rebuilt from raw reads (scope); every downstream aggregate it feeds reproduced | Indirect pass only — flagged below |

## Competing answers that survived
None for the main call or any supplementary answer. The thread built the strongest case for both "obvious"
alternates and found each excluded by shipped data, not by an asserted rule: (1) heating controls at the
pilot's own building mix, ~4.3% saving / ~€162 per tonne (over the €120 cap) is excluded because this
year's controls applicants are overwhelmingly offices/shops/workshops while the pilot's controls arm was
30 per cent hotels and care homes (`buildings_register_2026.xlsx` / `applications_2026.xlsx` use codes
against `pilot_2019_responses_and_draw.xlsx`); (2) heating optimisation carried flat at the seven-season
average, ~3.3% / ~€108/t (under the cap, wrongly funded), is excluded by the visible plateau in the pilot's
own seasonal series from season 4 onward (plan 4.4's service-life framing plus the data's own levelling).
Both forks are closed by named data, matching the design note's semantic fork table (SF6, SF7).

## Spec gates
| Gate | Required | Actual | Pass |
|---|---|---|---|
| Usable file count | 10 or more | 18 (7 csv, 1 docx, 6 pdf, 4 xlsx; no system files, no `__MACOSX`) | Pass |
| File categories | 2 or more | spreadsheet (csv, xlsx) and text/document (pdf, docx) | Pass |
| Large CSV ≥20,000 rows | 1 or more | `gas_meter_reads_2013_2026.csv` 389,104 rows; also `electricity_customers_annual_2019_2025.csv` 75,040 and `benchmarking_notices_2019_2026.csv` 37,213 | Pass |
| CSV 10-20 printed pages or more | 1 or more | `meter_points_2026.csv` 28,564 rows (multi-column) comfortably clears this independent of the row-count gate | Pass |
| `metadata.json` names 2+ distractors, none labelled in the ZIP | required | 4 named (`electricity_customers_annual_2019_2025.csv`, `solar_cadastre_rooftops_2024.xlsx`, `municipal_heat_plan_2026_summary.pdf`, `federal_funding_overview_2025.pdf`); none labelled inside target.zip; no file reveals how the task was built | Pass |
| Each distractor unused yet relevant | required | all 4 read as genuine adjacent documents a utility/council would hold (electricity use, solar potential, district-heat plan, federal grant stacking rules) and none feeds a graded figure | Pass |
| One distractor reproduces a graded quantity arithmetically, ruled out by a shipped fact | required | **not met**: neither PDF distractor states a number that arithmetically coincides with a graded figure (federal_funding_overview gives a 15/30 per cent federal grant rate, not a per-tonne figure; municipal_heat_plan gives connection years, not a saving or CO2 figure); the design note records this as deliberate ("No decoy: ... no shipped file states a saving, a rate, a grant per tonne or a recommendation") | **Fail (minor)** — see note below |
| 1-3 deliverables, all present in golden, format open | required | 2 deliverables (`grant_round_2026_note.docx`, `grant_round_2026_appraisal.xlsx`), both in `golden.zip` and `golden/`, matching `metadata.json` | Pass |
| Asks multi-dimensional with unit/rounding stated | required | each ask carries unit and the prompt's closing rounding sentence covers every quantity (percent to 0.1, euro per tonne, counts to 10, grants to €10,000, totals to €0.1M, tonnes to 10/100) | Pass |
| Answer in one of the fourteen shapes | required | scenarios with the flip point (each measure's grant per tonne, range and flip rate against the €120 limit) plus the round's settled grant; matches design note's declared answer shape | Pass |
| Golden ZIP holds exactly the requested files/formats | required | `golden.zip` contains exactly `grant_round_2026_appraisal.xlsx` and `grant_round_2026_note.docx`, matching the prompt's two-deliverable request and `metadata.json` | Pass |
| Nothing LLM-generated; goldens read as real work product | required | judge's hygiene check: PASS, no boilerplate, no LLM tells, genuine operational-artifact feel (benchmarking notices, meter reads, pilot draw, grant terms); no separate finding | Pass |

Note on the one "Fail (minor)" row: the determinism judge's own system prompt (Gate F "WHAT ACTUALLY
STUMPS") and Gate G now steer builds away from "a reported figure is wrong, catch it" decoys; a distractor
that arithmetically reproduces a graded quantity and must be ruled out by a shipped fact is exactly that
shape in miniature. The design note's "No decoy" line is deliberate avoidance of Gate G risk, not an
oversight, and the judge thread independently classified the task's stumping as `analytical_non_defect`
with `surface_read_dependency: no`. This spec-gate line and Gate G pull in slightly different directions
by construction; given the client's 2026-11-09 bar explicitly bans the decoy-flip shape, the author's
choice to skip it is the correct one and this line should not be read as a defect to fix.

## Gate G reconciliation
Thread: `mechanism: method_or_model_selection + decomposition_attribution + forecasting`,
`stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`.
Design note's results chain (R1-R9) assigns areas causal reasoning (R1, R4), forecasting (R2, R7), modeling
(R3), uncertainty (R6), synthesis (R5, R8, R9) — five distinct areas, consistent with the thread's
multi-mechanism read and clearing H4's "three or more areas" bar on its own terms. The design note's
hidden-factor record marks every constructed pattern (optimisation's fade, the use-mix split, the burner
checks, the late/withdrawn insulation answers, extensions/empty floors) "keep" because each sits in every
unit (not only the deciding ones) and each fix is a genuine modelling step (a fitted level carried to a
15-year life, a saving estimated per use and faded, a count/size/withdrawal projection measure by measure).
This matches Gate H3's carve-out for a hidden factor that is fine because detecting or correcting it is
itself analysis, not a shallow_hidden_factor. No disagreement found between the thread and the note on
mechanism classification.

## Gate H reconciliation
Thread's Gate H line: `domain: pass`, `layers: pass`, `results: ~10+ graded across ≥4 areas`,
`one_thing: none`, `effort: quick ~1-2 of 10+, careful ~5-6 of 10+, thorough all`,
`one_fact: "heating optimisation's saving falls to about 1.2% by the fourth winter and stays there" rescues
~2-3 of 10+`.

Design note's Gate H record: Results chain names 9 graded results (R1-R9) across 5 areas; Effort test table
gives quick 0.5/9 (6%), careful 4/9 (44%), thorough 9/9; "Largest single hint" rescues 2/9 (22%). The
thread's independent estimates (quick ~10-20%, careful ~50-60%, one-fact ~20-30%) sit within the same band
as the note's own numbers — no material divergence on any of the findings this reconciliation step is built
to catch:
- **one_thing**: thread says `none`; note's H3 line explicitly states "the strongest single piece is the
  heating optimisation fade (R2); a run that nails it still has to estimate each use's saving (R3), price
  this year's applications at them (R4) ... and it still fails heating controls." Agreement.
- **Hidden factor record vs. thread's catches**: thread independently names the same two catches the note
  records as hidden-factor entries (the optimisation fade, the use-mix split) and classifies both as
  requiring a genuine modelling step to fix, matching the note's "modelling" fix-depth entries, not a
  one-sentence fix. Agreement.
- **Effort-grade spread**: thread's quick pass (~10-20%) is comfortably under a third, as the note's own
  table requires; thread's careful pass (~50-60%) sits above the note's own careful figure (44%) but both
  leave clear daylight to the thorough pass (100%), so neither reading triggers the "careful pass level
  with the thorough one" finding.
- **One-fact rescue**: thread's ~20-30% and the note's 22% both sit under a third. Agreement.
- **Declared distractor carrying a result**: none of the four named distractors appear anywhere in the
  thread's reproduced figures. No finding.
- **Band excluding a defensible rival / too-wide band**: thread ran both "obvious" rivals (pilot's own mix
  for controls, flat seven-season average for optimisation) and found both excluded by shipped data, inside
  the design note's own bands (SF6, SF7); the controls range (€90-€110) is narrow enough to separate the
  hurried €162/t figure from the golden €99/t. No finding.

No finding from this pass predicts a send-back under the 2026-11-09 bar.

## Stump power (Gate F)
Thread: a careful-but-hurried run is likeliest to lose on heating controls (filing the pilot's pooled-mix
rate, ~4.3%/€162 per tonne, and wrongly excluding controls from the funded set) and/or on heating
optimisation if it carries the seven-season average flat instead of fitting the plateau (~€108/t, wrongly
funding it). These are two independent, provable analytical misses, not a coin flip, and they are joined by
three further independent judgments (the round-at-close timing/withdrawal projection, the use-split by
occupancy, the 2025/26 CO2 base), consistent with the design note's depth-level-5 claim (five independent
judgments, three different wrong funded sets depending on which shortcut is taken).

## Findings, ranked
1. (Low severity, informational) The shipped distractors are genuinely unused and relevant but none is a
   decoy that arithmetically reproduces a graded quantity and must be ruled out by a shipped fact — the
   strict reading of one spec-gate bullet is not met. This is a deliberate, correct choice under the
   2026-11-09 Gate G standard (which bans exactly that shape as a primary stump) and should not be reworked.
2. (Informational, outside the judge's scope) `task7/DESIGN_NOTE.md`'s "Tried and rejected" section (lines
   roughly 176-213) contains a long run of entries that describe an unrelated task (a heat-pump/feeder
   hosting-capacity build with co-ops, crews and a hospital-discharge/actuarial-reserving architecture
   history) rather than this task's retrofit-grant world. This reads like cross-task content left in the
   file rather than genuine history for task7's own architectures 1-6; it does not touch the shipped bundle,
   the prompt, or the graded blocks, and the judge thread never saw it (it is outside the scratch
   allow-list), so it has no bearing on the DETERMINISTIC/APPROVE verdict above. Worth a cleanup pass before
   the note is relied on for future audits.
3. (No action needed) The thread did not independently rebuild the full season-by-season gas-use panel from
   the 389,105-row meter-read file (meter exchanges, rollovers, estimates, calorific conversion) given scope;
   every downstream aggregate it could cheaply cross-check from that pipeline's outputs reproduced almost
   exactly, which is strong indirect evidence the pipeline is sound, but it is not a from-scratch
   verification of asks 2-4's season-by-season percentages.

## Next action for the author
None required to ship. Optionally: clean the stray cross-task entries out of `DESIGN_NOTE.md`'s "Tried and
rejected" section (finding 2) before the next audit, since they make the note's history harder to trust at
a glance; this is bookkeeping, not a build defect, and does not affect this verdict.
