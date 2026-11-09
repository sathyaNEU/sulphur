# leak check, task7

**Verdict: REVIEW.** 18 files read, 46 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, carried, heating, record, golden, controls, pooled, feeder, patients, insulation, optimisation, nothing, comparison, missed, december, default, building, states, service, seasons, shipped, method, average, exactly, equipment

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `climate_action_plan_2023_extract.pdf`: golden figure 4.1 appears: ...that use most are one of the plan's instruments. 4.1 The programme The council grants 30 per cent of a...
- **REVIEW** `climate_action_plan_2023_extract.pdf`: golden figure 4.3 appears: ...ce of each measure's saving from the 2019 pilot. 4.3 Normal weather A season runs from 1 May to 30 Apr...
- **REVIEW** `climate_action_plan_2023_extract.pdf`: golden figure 4.6 appears: ...ted floor area in Stadtwerke Haldenau's register. 4.6 Monitoring The Climate Protection Office reports...
- **REVIEW** `climate_action_plan_2023_extract.pdf`: golden figure 4.4 appears: ...denau normalises it for its benchmarking notices. 4.4 Appraisal of a round An application's lifetime to...
- **REVIEW** `committee_request_2026-06-15.docx`: golden figure 4.6 appears: ...rks saved in the season to April 2026, as section 4.6 sets it out. With thanks and best wishes,...
- **REVIEW** `climate_action_plan_2023_extract.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating controls'
- **REVIEW** `grant_offer_2026_terms.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating controls'
- **REVIEW** `pilot_2019_rules.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating controls'

## 4 design-note vocabulary (REVIEW 5)
- **REVIEW** `benchmarking_method_2022.pdf`: 6 of 25 stump-paragraph terms appear (nothing, building, service, seasons, method, average); read whether the document names the move
- **REVIEW** `climate_action_plan_2023_extract.pdf`: 8 of 25 stump-paragraph terms appear (carried, heating, controls, insulation, optimisation, building); read whether the document names the move
- **REVIEW** `federal_funding_overview_2025.pdf`: 4 of 25 stump-paragraph terms appear (heating, insulation, optimisation, building); read whether the document names the move
- **REVIEW** `grant_offer_2026_terms.pdf`: 7 of 25 stump-paragraph terms appear (heating, record, controls, insulation, optimisation, nothing); read whether the document names the move
- **REVIEW** `pilot_2019_rules.pdf`: 6 of 25 stump-paragraph terms appear (heating, record, controls, insulation, optimisation, building); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 18 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Pack read in full as a solver would: all 18 files opened (6 PDFs via pdftotext/pypdf, 4 xlsx via openpyxl including a
sheet-state/defined-names/cell-comment sweep, 1 docx via python-docx including header/footer-part and
tracked-changes/comments checks, 7 CSVs via header + distribution + duplicate-row samples). No answer, figure or
score was computed; observations below are about structure and wording only.

### 1. Which sentence or file tells you how any part of the analysis should be done?

Nothing names a comparison, a model, or how to estimate the one quantity the whole chain turns on: each measure's
real saving percentage. No document says "compare drawn to not-drawn," "use the lottery as a natural experiment,"
"run a regression," "bootstrap," or anything like it; none of those words appear anywhere in the pack (checked by
grep across every extracted text and the docx).

What **is** spelled out, several places, is how the *derived arithmetic* on top of that saving percentage is
defined, and one data-hygiene rule. Quoting the clearest instances (full detail under Q5):

- `climate_action_plan_2023_extract.pdf`, 4.4: "The council funds a measure in a round when its grant per tonne is
  €120 or less, and then funds every application for that measure in the round." This is the decision rule, but it
  is **already in prompt.txt verbatim** ("under the council's limit of €120 of grant per lifetime tonne of CO2"),
  so the file adds no information the solver doesn't already have from the question itself.
- `grant_offer_2026_terms.pdf`, section 2: "An owner who revises the quote sends the application again; the later
  application replaces the earlier one." A dedup/latest-version rule (see Q7 for the 36 affected building_ids);
  this is the kind of reflex hygiene item the house record treats as pricing nothing, not an analytical step.

Everything else in the formulas (lifetime tonnes, saving rate on applications, grant per tonne, reference
consumption, the 4.6 monitoring definition) defines **what each term means**, not how to produce the one estimate
(the measure's saving) those terms are built on. See Q5 for the full list with literal readings.

### 2. Which file already ranks or scores the candidates (the measures)?

None. No file contains a saving percentage, a lifetime-tonnes figure, a grant-per-tonne figure, or any rank/score
column for insulation, heating optimisation or heating controls. I grepped every column header across all 18 files
(`select:`-style header dump) for anything like "saving", "rate", "tonnes", "rank", "score", "recommend" — the only
hits are the raw inputs (`quoted_cost_eur`, `grant_eur`, `reference_consumption_kwh`), never a computed measure-level
outcome.

### 3. Which file exists only to help the analyst?

None of the 18 is a bolt-on dictionary/readme/manifest/notes-sheet built just for a solver. Every file reads as a
document or extract a real office would hold: term sheets approved by a named committee on a named date, a utility's
versioned methodology note (`benchmarking_method_2022.pdf`, "Version 2, May 2022 (version 1, March 2019). Owner:
Torben Römer"), register/extract spreadsheets, a chair's internal memo. The closest thing to a "helper" document is
`benchmarking_method_2022.pdf`, but it is itself a real, dated, owned business artifact that the other documents
reference by name ("as Stadtwerke Haldenau normalises it for its benchmarking notices"), not a document manufactured
to carry the task's answer.

### 4. Which figure or name reads as the answer rather than context?

None found. No number anywhere in the pack matches what would be a final deliverable figure (no measure-level
saving %, no grant-per-tonne value, no named "recommended measure"), and no document states or implies which of the
three measures will clear €120/tonne.

### 5. Filed sentences that fix how a graded figure is computed (literal reading, no numbers)

From `climate_action_plan_2023_extract.pdf`:
- 4.2: "A measure's saving in a season is the gas its works save, as a share of the gas the buildings that had them
  would have used that season without them, both in a season of long-term average weather." → Defines "saving" as a
  counterfactual-vs-actual ratio, both sides weather-normalised; does not say how to build the counterfactual.
- 4.4: "An application's lifetime tonnes are the CO2 in the gas its measure's works would save in the building
  applied for over the measure's service life, each year's saving taken on the application's reference consumption,
  at 0.201 tonnes of CO2 per MWh of gas." → lifetime tonnes = service life (years, from the table: insulation 30,
  heating optimisation 15, heating controls 10) × (the measure's saving rate × the application's reference
  consumption in MWh) × 0.201.
- 4.4: "A measure's saving rate on a round's applications is their lifetime tonnes as a share of the tonnes their
  reference consumption carries over the same life." → saving rate on applications (per measure) = sum of that
  measure's applications' lifetime tonnes ÷ sum of (their reference consumption × service life × 0.201).
- 4.4: "A measure's grant per tonne in a round is the grant of the round's applications for it divided by their
  lifetime tonnes." → grant per tonne (per measure) = sum of granted applications' `grant_eur` ÷ sum of their
  lifetime tonnes.
- 4.4: "The council funds a measure in a round when its grant per tonne is €120 or less, and then funds every
  application for that measure in the round." → the funding decision rule (already in the prompt, see Q1).
- 4.5: "An application's reference consumption is the normalised use per square metre printed on the notice that
  carried the offer, times the building's heated floor area in Stadtwerke Haldenau's register." → reference
  consumption = `normalised_use_kwh_per_m2` (from that building's benchmarking notice) × `heated_floor_area_m2`
  (from the register). Note: for 2026 this value is already supplied as a column in `applications_2026.xlsx`; for
  the 2019 pilot it is not supplied and would need assembling from `benchmarking_notices_2019_2026.csv` and
  `buildings_register_2026.xlsx`.
- 4.6: "The Climate Protection Office reports each year to the committee on the CO2 the programme's works saved in
  the season just ended: the gas the buildings with works would have used that season without them, less what they
  used, both in normal weather, at the factor in 4.4." → CO2 saved in a season = (counterfactual normalised use
  without works − actual normalised use), summed over works buildings, × 0.201 t/MWh. This is the literal formula
  for the prompt's "CO2 the pilot's works saved in 2025/26" ask, but the counterfactual itself is not given.

From `benchmarking_method_2022.pdf`:
- Section 1: "Where a read is taken on another day, the use between two reads is shared over the days between them
  in proportion to each day's weight: the use type's hot water and process share spread evenly over the days of the
  year, and the rest in proportion to the day's degree figure…" → fixes the apportionment rule for meter reads that
  fall on a date other than 30 April (a measurement/assembly convention, not the causal estimate).
- Section 2: "The kWh billed are the cubic metres times the meter point's z-number times the season's billing
  calorific value for the network area." → fixes the m3→kWh conversion (using `factor`, `z_number` from
  `meter_points_2026.csv` and the season/network-area value from `calorific_values_2013_2026.csv`).
- Section 3: normalisation formula (hot-water/process share held flat, remainder scaled by G20/15 long-term degree
  days over the season's own) → fixes the weather-normalisation method, consistent with the degree-days file.

From `grant_offer_2026_terms.pdf`: the dedup rule quoted under Q1, and "except buildings that had works under the
2019 pilot" (section 1) → an eligibility filter on the 2026 offer population.

None of these hands over the measure's saving percentage itself; they only fix the arithmetic that sits on top of
it and a couple of housekeeping conventions.

### 6. Is there one thing that would make most of the prompt routine?

No. I did not find a file, sentence or column that states or implies the three measures' saving percentages, which
is the one quantity every downstream ask depends on (seasonal saving, saving rate on applications, lifetime tonnes,
grant per tonne, the 90% range, the flip rate, and the 2025/26 CO2 figure). It is not written anywhere; it can only
come from analysing the 2019 pilot's lottery (`pilot_2019_responses_and_draw.xlsx`: `drawn`/`not drawn`,
`withdrawn`, `works_completed`) against actual gas use (`gas_meter_reads_2013_2026.csv`, `meter_points_2026.csv`,
`calorific_values_2013_2026.csv`), weather-normalised (`weather_haldenau_daily_2013_2026.csv`,
`degree_days_haldenau.csv`, the method doc). Even having that one number would not make the whole prompt routine:
- Saving **by season since the works**: still requires per-season computation from meter reads (does it hold or
  decay over time) — turns on analysis.
- Saving **rate on applications received so far** / **lifetime tonnes** / **grant per tonne**: mechanical arithmetic
  once the saving rate and reference consumption exist — this piece *would* become close to routine if the saving
  rate were handed over, but it is not.
- **90% range and the flip rate**: no document names a method (no "confidence", "bootstrap", "interval", "range",
  "sensitivity", "threshold" anywhere in the pack) — turns on analysis.
- **How many applications it will have, granted and paid once the offer closes and withdrawals are in**: the
  applications file runs only to 2026-06-12 (matching the committee memo's "applications that came in by 12 June"),
  while the round stays open to 30 June and works/withdrawals run to 30 September — this is a forecast
  (arrival trend to close, then an attrition/withdrawal rate from the 2019 pilot's pattern) with no numeric answer
  or method given anywhere — turns on analysis.
- **Funded-application list with grant and lifetime tonnes**: mechanical once the funding decision and each
  application's lifetime tonnes exist, but still requires correctly applying the dedup rule (36 duplicate
  building_ids in `applications_2026.xlsx`) and the right population (funded measures only) — a reading/hygiene
  step, not a hidden trap.
- **2025/26 CO2 saved**: turns on analysis (needs the same counterfactual machinery as the seasonal saving figure,
  restricted to the single most recent season and the completed-works population).

So no single fact clears more than the mechanical/arithmetic layer; the core estimation, the uncertainty, and the
forecast each stand on their own.

### 7. Realism

Nothing read as generated or as the task describing its own data. Checked and clean:
- PDF metadata: each of the six PDFs has its own plausible Producer/LibreOffice version and creation date matching
  its content date (6.2 for 2019, 7.3 for 2022, 7.5 for 2023, 24.8 for Jan 2025, 25.2 for Apr 2026, 25.8 for Mar
  2026), distinct named authors/owners per document, no custom XMP, no annotations, no ReportLab/FPDF-style
  Producer.
- xlsx/docx metadata: distinct creators and companies per file ("Stadt Haldenau", "Stadtwerke Haldenau",
  "Landesanstalt für Umwelt Baden-Württemberg" on the solar cadastre, "Magda Peukert" on the memo), plausible
  created/modified timestamps (e.g. the memo shows revision 3, 41 minutes of edit time), no hidden sheets, no
  defined names, no cell comments, no tracked changes, no header/footer parts hiding extra text.
- Figures are not suspiciously round: quoted costs and grants are irregular (e.g. 1780 → grant 530, 33660 → grant
  10100), consistent with 30%-of-quote rounded to the nearest 10, not synthetic-looking round numbers.
- Mess looks like real mess, not a planted block: 1583 exact-duplicate rows in `gas_meter_reads_2013_2026.csv`,
  each appearing exactly twice and adjacent in the file (a realistic double-submitted-reading glitch, scattered
  across unrelated meter points, not a copied section); 36 duplicate `building_id`s in `applications_2026.xlsx`
  matching the stated "later application replaces the earlier one" rule; a `factor` of 10 (meters that count in
  tens of m3) on about 7% of meter points, matching the method doc's "some in tens of cubic metres"; the HN-3
  network area's billing calorific value jumps from ~10.0 to ~11.3 kWh/m3 exactly between 2016/17 and 2017/18,
  matching the method doc's stated L-gas-to-H-gas conversion date of 1 May 2017; a "1991-2020 mean" reference row
  appended to `degree_days_haldenau.csv` whose 12 monthly values sum to 3635, matching the figure quoted in the
  method doc. No "test", "dummy", "sample", "TBD" or similar strings anywhere in the CSVs.
- No ranking, score or recommendation text anywhere, no author/model fingerprints, nothing LLM-ish in the document
  prose (short, plain, bureaucratic, on-topic).

### The four flagged files (mechanical sweep: measure names / section numbers)

- `climate_action_plan_2023_extract.pdf`: Contains the formula definitions (lifetime tonnes, saving rate, grant per
  tonne, the €120 rule, reference consumption, the 4.6 monitoring definition) quoted under Q5. These are legitimate
  "what a term means" filings, not a leak of the actual saving percentage or of how to estimate it from the pilot.
  The €120 funding rule it states is not new information (verbatim already in prompt.txt). Harmless, with the
  caveat that it is where every downstream formula is defined, so it is required reading, not optional context.
- `committee_request_2026-06-15.docx`: An internal memo that mirrors the prompt's asks in plain-English, non-
  technical language ("your view of which measures to fund and how sure you are of each", "what the pilot showed
  season by season", "the workbook the office will use to issue the grants", "what the round will actually pay once
  the offer has closed"). It restates the same €120/tonne rule as the prompt and names who is asking and why, but
  never names a method, a statistic, a population or a comparison beyond what prompt.txt already says. Harmless
  context.
- `grant_offer_2026_terms.pdf`: Names the three measures, the application process, the 30%/€40,000 grant terms, and
  two conventions worth flagging as filed rules rather than leaks: the dedup rule ("the later application replaces
  the earlier one", confirmed operative on 36 rows) and an eligibility exclusion ("except buildings that had works
  under the 2019 pilot"). It points to climate-action-plan section 4 for the funding formula rather than repeating
  it. Harmless; the dedup rule is a hygiene convention, not an analytical shortcut.
- `pilot_2019_rules.pdf`: Describes the 2019 lottery mechanically (one measure per response, "the pilot's budget
  funds a little under half of the responses for each measure", drawn by lot "among the responses for each
  measure" i.e. randomised within each measure group, works due before the 2019/20 heating season, withdrawal loses
  the place). It explains why the `drawn`/`not drawn`/`withdrawn`/`works_completed` columns exist, but gives no
  exact split, no savings figure, and no instruction to use the draw as a natural experiment. Harmless, and
  arguably necessary for the solver to understand the pilot data's shape; it doesn't hand over the causal design.

### Files not otherwise discussed
`federal_funding_overview_2025.pdf` (federal BEG grant rates, gas boilers unfunded since 2024) and
`municipal_heat_plan_2026_summary.pdf` (future district-heating zones, earliest connection 2029-2032) are real-
looking municipal/agency documents that provide adjacent policy context; neither names a step, population or figure
for this task's computations. `electricity_customers_annual_2019_2025.csv` and `solar_cadastre_rooftops_2024.xlsx`
read as the pack's two distractors: both share a plausible join key with real task data (`customer_number` /
building address) but neither is referenced by any governing document and neither carries anything about gas,
measures, or CO2.

Main-thread rulings (2026-11-09, architecture 7, target.zip 00c9970f): every leak.py REVIEW line is harmless (the plan's own section numbers; the measures' names in the governing documents; the field's ordinary words); the reader's structural note on applications_2026.xlsx is the plan's own reference consumption (4.5) carried on the office's application record, harmless; questions 1 to 4 none, question 5 definitions only (none supplies a saving), question 6 analysis throughout, question 7 nothing generated-looking. No fix.

Prompt re-read after the R7 wording fix (Sonnet, medium, 2026-11-09, prompt and governing documents only): no method,
warning, file name, role or count the data hold; no single collapsing fact. One two-reading risk found and closed: "what
would be paid on them once withdrawals are in" named one of the 2026 terms' two causes of non-payment (withdrawal,
works not completed); the prompt now reads "once the works are done", the terms' own words, and the record converges
(every drawn 2019 owner either withdrew or completed, SF15, asserted). The pronoun in "how many applications it will
have" reads as the measure under the "For each measure" frame. No figure moved.
