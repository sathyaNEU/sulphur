# leak check, task23

**Verdict: REVIEW.** 22 files read, 25 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: campaigns, oxidation, carried, pressure, record, golden, missed, flights, emission, chambers, collected, closed, efficiency, chamber, options, design, calibration, forecast, second, hurried, nearest, potential, spring, tickets, recirculation

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `council_agenda_lfg_capital_2027.pdf`: carries 14 of 17 distinctive words of the committed call: "Fund package D (USD 2.38 million): it is the cheapest package that keeps 2027 at or under the Council's 5,100-ton limit,"

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `council_agenda_lfg_capital_2027.pdf`: 7 of 25 stump-paragraph terms appear (campaigns, carried, record, emission, closed, options); read whether the document names the move
- **REVIEW** `ghg_annual_report_RY2025.pdf`: 5 of 25 stump-paragraph terms appear (oxidation, record, emission, collected, efficiency); read whether the document names the move
- **REVIEW** `tessaline_whole_site_methane_2025_2026.pdf`: 4 of 25 stump-paragraph terms appear (campaigns, carried, emission, second); read whether the document names the move

## 8 column names (REVIEW 7)
- **REVIEW** `auto_chamber_flux_hourly.csv`: columns a generator names and an organisation does not: soil_temp_c
- **REVIEW** `brightwater_plot_measurements_2019.csv`: columns a generator names and an organisation does not: soil_temp_c
- **REVIEW** `fernhallow_met_station_hourly.csv`: columns a generator names and an organisation does not: air_temp_c, soil_temp_10cm_c
- **REVIEW** `lfg_plant_hourly_2023-2026.csv`: columns a generator names and an organisation does not: flare_temp_f
- **REVIEW** `surface_emission_monitoring_quarterly.csv`: columns a generator names and an organisation does not: flag
- **REVIEW** `tessaline_campaign_results.csv`: columns a generator names and an organisation does not: air_temp_c
- **REVIEW** `wellfield_monitoring_2019-2026.csv`: columns a generator names and an organisation does not: temp_f

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'pptx+xlsx' at 27% of 22 prompts (cap 20%); reword at the role level, not the verb

## 12 describing content (REVIEW 1)
- **REVIEW** `council_agenda_lfg_capital_2027.pdf`: names 12 column(s) of the data files verbatim (basis, cell, completed, cover, date, installed): confirm it is the organisation's own record and not a note written for the analyst

## 12 client quality check (INFO 2)
- **INFO** `-`: 22 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)


## Solver's-eye read

Isolated reader (Sonnet, medium), 2026-11-13, on fresh copies of prompt.txt and target/ only.

1. No file says how any part of the analysis is done. What it quoted are the authors' descriptions of their own work:
   the report's collection-based equation (the prompt asks for the report's gap "in the order of its own equation", so
   the bridge's axes are filed by the prompt and the report), the study's isotope fraction (25 per mil), the survey's
   campaign eligibility rules, and the options paper's design basis (design capture 22 and 72 per cent, package C's
   pumps in every cell 4 well with liquid above its screen at the October 2026 survey, the cap at 86 per cent, the
   closed cells at 90 per cent), which it read as the packages' scope rather than method.
2. No file ranks or scores the packages; no file gives a package's 2027 emission.
3. No helper-only file; the tonnage workbook's basis column and Cells sheet read as the organisation's own records.
4. No figure reads as the answer: the report's and the survey's figures are in the prompt as the two figures to
   reconcile, the limit is context, and no file states the 2025 actual emission, cell 5's generation or oxidation
   share, or any package's 2027 emission.
5. Filed sentences fixing a computation: the resolution's definition of emissions and its least-cost, normal-weather
   rule, the cumulative packages, design capture as a share of cell 5's methane from each in-service date, the closed
   cells at 90 per cent, the report's collected-methane method (0.0192 kg per standard cubic foot, the engines'
   analyzer as fallback) and the survey's 8,760 hours.
6. No single planted item; noticing any one candidate leaves the others open. Per ask: the actual emission and its
   bridge, cell 4's change, cell 5's generation and oxidation share, and the packages need genuine analysis; cell 5's
   tonnage is assembly and field reading. It noted the options paper's package C condition as a rule to apply to the
   wellfield data.

### Sweep flags
- (a) column names: harmless, ordinary instrument and logger names with units in the producing systems' style.
- (b) the options paper's column words: the organisation's own council paper, not a note for the analyst.
- (c) the options paper carrying the call's words: harmless; it describes the packages and the resolution and
  recommends nothing.

### Realism notes
One pilot (the division's engineer) on every drone flight, plausible for a small county; campaign windows consistent
with the stated rules; drone take-offs bunched at 11:00 to 11:25; the 2025 monthly collected-methane table a little
too regular.

### Rulings (main thread)
- Questions 1 to 5: every sentence quoted executes to the golden's own convention (checks.py SF1 to SF18); nothing to
  fix.
- Question 6, package C's condition: it is the package's scope (which wells take pumps), a WHAT the options paper must
  file for R7 to be determinate; it names neither the faster decay nor that the flooding hides it. Harmless.
- Question 6, cell 5's tonnage as assembly: R1 is the chain's assembly result by design (the careful pass earns it).
- Realism: the drone take-offs now spread between 10:05 and 12:50, and the blower outages put zero-flow spells in the
  plant record and dips in the monthly table (generator, rebuilt); the single drone pilot stays.
