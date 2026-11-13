# leak check, task23

**Verdict: REVIEW.** 22 files read, 25 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: campaigns, oxidation, pressure, carried, golden, record, nearest, missed, design, chambers, flights, inside, closed, emission, collected, options, sentence, calibration, efficiency, tickets, chamber, checks, method, forecast, second

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `council_agenda_lfg_capital_2027.pdf`: carries 14 of 17 distinctive words of the committed call: "Fund package D (USD 2.38 million): it is the cheapest package that keeps 2027 at or under the Council's 5,500-ton limit,"

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `brightwater_cover_oxidation_2019.pdf`: 3 of 25 stump-paragraph terms appear (oxidation, chamber, method); read whether the document names the move
- **REVIEW** `council_agenda_lfg_capital_2027.pdf`: 7 of 25 stump-paragraph terms appear (campaigns, carried, record, design, closed, emission); read whether the document names the move
- **REVIEW** `ghg_annual_report_RY2025.pdf`: 6 of 25 stump-paragraph terms appear (oxidation, record, emission, collected, efficiency, method); read whether the document names the move
- **REVIEW** `tessaline_whole_site_methane_2025_2026.pdf`: 5 of 25 stump-paragraph terms appear (campaigns, carried, emission, method, second); read whether the document names the move

## 8 column names (REVIEW 7)
- **REVIEW** `auto_chamber_flux_hourly.csv`: columns a generator names and an organisation does not: soil_temp_c
- **REVIEW** `brightwater_plot_measurements_2019.csv`: columns a generator names and an organisation does not: soil_temp_c
- **REVIEW** `fernhallow_met_station_hourly.csv`: columns a generator names and an organisation does not: air_temp_c, soil_temp_10cm_c
- **REVIEW** `lfg_plant_hourly_2023-2026.csv`: columns a generator names and an organisation does not: flare_temp_f
- **REVIEW** `surface_emission_monitoring_quarterly.csv`: columns a generator names and an organisation does not: flag
- **REVIEW** `tessaline_campaign_results.csv`: columns a generator names and an organisation does not: air_temp_c
- **REVIEW** `wellfield_monitoring_2019-2026.csv`: columns a generator names and an organisation does not: temp_f

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'pptx+xlsx' at 25% of 24 prompts (cap 20%); reword at the role level, not the verb

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

## 9 dates after the setting (clean)


## Solver's-eye read

Isolated reader (Sonnet, medium), 2026-11-13, on fresh copies of prompt.txt and target/ only, on the repaired cut (the
transfer contract on the tickets, the options paper's new design basis). The read of the READY cut 3bf7d67 is in git.

1. No file says how any part of the analysis is done. It quoted the options paper's design basis (design capture 15 and
   78 per cent; package C's pumps in every cell 4 well whose liquid stood above its screen bottom when last gauged in
   2026, holding the liquid where the June 2025 pilot pumps hold it; the cap at 86 per cent; the closed cells at 92 per
   cent), the report's equation and constants and the study's isotope fraction: the packages' scope, the report's own
   method and the study's own method.
2. No file ranks the packages on emissions; the options paper lists them by cost and states the resolution's rule,
   never its result.
3. The options paper is the one file that is not a measurement or a record; it defines the packages, their costs and
   the limit. No helper-only file.
4. No figure reads as the answer: no file states the 2025 actual emission, cell 5's 2027 generation or oxidation share,
   or any package's 2027 emission.
5. Filed sentences fixing a computation, with their literal results: design capture 15 per cent from May 1, 2027 for B
   and C, 78 per cent once the wells are in for D and E, none before; package C's pumps in the cell 4 wells whose latest
   2026 depth to liquid sits above the screen bottom; cells 1 to 3 at 92 per cent of their methane through 2027; the
   report's equation fixing the bridge's order.
6. Nothing collapses more than one ask; the pilot pumps' work orders bear only on cell 4's collection. Per ask: the
   packages, the 2025 actual and its bridge, cell 4's change (the plant record starts in 2023 and mixes cells 1 to 4),
   cell 5's generation (no decay constants are filed) and its oxidation share (the study never measured cell 5) turn
   on analysis; cell 5's tonnage on reading the tickets' fields and codes.

### Sweep flags
- (a) the column names: harmless, the producing systems' unit-bearing names.
- (b) the options paper's column words and the call's words: the organisation's own council paper; it defines the
  packages and the resolution and recommends nothing.

### Realism notes
- The 2019 study's text said seven runs failed where its table and its plot file show ten.
- Cross-file consistency confirmed: the pilot pumps' work orders match the register's pump dates, the recirculation log
  the options paper's dates, cell 5's first tickets the Cells sheet.
- One drone pilot on every flight: plausible for a small program.

### Rulings (main thread)
- Questions 1 and 5: every quoted sentence executes to the golden's own convention (checks.py SF1 to SF22); the design
  basis is the packages' WHAT, the pumps' level and scope included (SF20, SF21); nothing to fix.
- Question 3: the options paper is the decision's own document and must file the packages for R7 to be determinate.
  Harmless.
- Question 6: R1 is the chain's assembly result by design (the careful pass earns it).
- Realism: the study's failed-run count now follows its plot file (generator, checks.py R4); the single drone pilot
  stays.

### Follow-up: the gas model sentence (same reader, after the options paper gained one sentence)
- Question 1: the sentence fixes one convention, when a month's waste starts producing methane; the decay's form, its
  rates and the waste's yield stay unfiled. Question 5, literally: a month's waste adds nothing to a cell's generation
  until six months after its placement month, whichever file carries the tonnage. Question 6: it settles none of the
  asks; it bears mainly on cell 5's 2027 generation, one of several modelling choices there, and barely on cell 4's
  (its waste is years past the onset). The 2019 study now counts ten failed runs, matching its table and plot file.
- Ruling: harmless, the convention the golden uses for every cell (SF23). Whether it reaches cell 4 is inert: R3 is
  read off the wells' own flows, and cell 4's last waste went in in January 2025.
