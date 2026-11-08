# leak check, task7

**Verdict: REVIEW.** 17 files read, 16 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: buildings, comparison, building, season, heating, passed-over, lottery, golden, architecture, seasons, insulation, optimisation, second, decisive, record, service, notice, utility, visited, carried, points, default, feeder, patients, programme

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `climate_action_plan_2023_extract.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating optimisation'
- **REVIEW** `federal_funding_overview_2025.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating optimisation'
- **REVIEW** `pilot_2019_rules.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating optimisation'

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `benchmarking_method_2022.pdf`: 5 of 25 stump-paragraph terms appear (building, season, seasons, service, notice); read whether the document names the move
- **REVIEW** `climate_action_plan_2023_extract.pdf`: 13 of 25 stump-paragraph terms appear (buildings, comparison, building, season, heating, seasons); read whether the document names the move
- **REVIEW** `committee_request_2026-06-15.docx`: 6 of 25 stump-paragraph terms appear (buildings, building, season, service, notice, carried); read whether the document names the move
- **REVIEW** `federal_funding_overview_2025.pdf`: 7 of 25 stump-paragraph terms appear (buildings, building, heating, insulation, optimisation, points); read whether the document names the move
- **REVIEW** `municipal_heat_plan_2026_summary.pdf`: 3 of 25 stump-paragraph terms appear (buildings, building, heating); read whether the document names the move
- **REVIEW** `pilot_2019_rules.pdf`: 8 of 25 stump-paragraph terms appear (buildings, building, season, heating, insulation, optimisation); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'pptx+xlsx' at 30% of 10 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 17 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

Isolated reader (Sonnet, medium) on a fresh copy of prompt.txt and target/, 2026-11-08, before the plan's 4.2 rewording.

- Q1: none states the decisive step; the nearest are the pilot rules' draw by lot, the request's "on the gas its buildings would have used that season without the works" and the plan's 4.2 averaging sentence.
- Q2: none.
- Q3: none; the four documents (benchmarking method, plan extract, pilot rules, committee request) read as governing paperwork.
- Q4: none.
- Q5: the plan's 4.2 averaging sentence, read literally, could be taken as a works-only average; 4.4's pooled grant per tonne and all-or-nothing funding; 4.5's notice figure; the request's round once the offer has closed (an extrapolation to 30 June); the benchmarking method's conventions.
- Q6: an analytical choice, how each measure's saving rate is estimated from the pilot; the appraisal around it is the plan's rule.
- Flagged files: the plan extract harmless (the procedure for the appraisal, no figures); the federal overview harmless (a distractor); the pilot rules state the draw by lot (the design, not the decisive step).
- Realism: nothing machine-made; the request is precise about the quantities but plausible; the draw date in the pilot workbook's column name is odd but plausible.

Rulings (main thread): every REVIEW line harmless (the three files carry the measures' own names; the stump-vocabulary words in the documents are "Energy Services", "service life", "notice" and "carried", none naming a visit); the Q5 averaging sentence fixed in the generator: 4.2 now reads "the share the works saved in each building that had them, averaged over those buildings and given in whole per cent", so the saving it averages is each building's saving against what it would have used without the works.

Second isolated read after the 4.2 rewording (Sonnet, medium, 2026-11-08): no decisive step named (the nearest are
the plan's 4.2 per-building saving, the request's "would have used that season without the works" and the pilot
rules' draw by lot, the design, not the step); no ranking, helper or answer file; Q5 reads 4.2 as a per-building
saving against what the building would have used, averaged over the works buildings and rounded, with the request
making the counterfactual explicit; Q6 an analytical choice, how each measure's saving rate is estimated.

Third isolated read after the plan's 4.2 filed the saving rate's construction (Sonnet, medium, 2026-11-08): no decisive
step named; 4.2 "only says how the saving is computed once a comparison group exists ... nothing in it points toward a
particular choice"; no ranking, helper or answer file; Q6 an analytical choice, the comparison group for the saving
rate. Its one data question (drawn rows without a completion date) does not hold: the pilot workbook carries 1,218 drawn
rows with works completed, 38 drawn and withdrawn, 1,535 not drawn.
