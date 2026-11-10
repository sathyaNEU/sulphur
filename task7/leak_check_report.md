# leak check, task7

**Verdict: REVIEW.** 19 files read, 64 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: building, controls, insulation, heating, asserted, architecture, carried, record, golden, lottery, optimisation, nothing, lived-in, missed, comparison, sentence, points, inside, seasons, weekend, million, owners, register, author, driver

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `climate_action_plan_2023_extract.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating controls'
- **REVIEW** `grant_offer_2026_terms.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating controls'
- **REVIEW** `pilot_2019_rules.pdf`: carries 3 of 3 distinctive words of the committed call: 'insulation and heating controls'

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `benchmarking_method_2022.pdf`: 3 of 25 stump-paragraph terms appear (building, nothing, seasons); read whether the document names the move
- **REVIEW** `climate_action_plan_2023_extract.pdf`: 7 of 25 stump-paragraph terms appear (building, controls, insulation, heating, carried, optimisation); read whether the document names the move
- **REVIEW** `federal_funding_overview_2025.pdf`: 6 of 25 stump-paragraph terms appear (building, insulation, heating, optimisation, points, owners); read whether the document names the move
- **REVIEW** `grant_offer_2026_terms.pdf`: 7 of 25 stump-paragraph terms appear (building, controls, insulation, heating, record, optimisation); read whether the document names the move
- **REVIEW** `municipal_heat_plan_2026_summary.pdf`: 3 of 25 stump-paragraph terms appear (building, heating, owners); read whether the document names the move
- **REVIEW** `pilot_2019_rules.pdf`: 7 of 25 stump-paragraph terms appear (building, controls, insulation, heating, record, optimisation); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 2)
- **REVIEW** `prompt.txt`: rounding at the close: no rounding words anywhere; every derived figure needs one, stated once at the end
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 36% of 14 prompts (cap 30%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 19 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Architecture 8, 2026-11-09: one isolated reader (Sonnet, medium) on fresh copies of prompt.txt and the pack cut before the stage-4 repair. The repair afterwards was data-only (the electricity load profiles rebuilt with each building's day shape and the lived-in buildings' honest activity; no sentence added or reworded in any document or the prompt), so leak.py alone covers it. Main thread's rulings: question 1 quotes only the plan's and the method's definitions of WHAT (a saving, normal weather, lifetime tonnes, the limit, a revised application), which the house files deliberately; question 5's literal reading of plan 4.4 is the golden's (each application's own saving on its own reference consumption); the profiles' "handful of standard shapes" was fixed in the repair; the identical AppVersion and the 1980 entry stamps are what Excel itself writes; the missing rounding sentence is the author's call.

### Verdicts on the four flagged items

1. **climate_action_plan_2023_extract.pdf** — Not harmless on close reading, though the measure *names* alone are. Section 4.1 names the three measures, but the "applications" data (`applications_2026.xlsx`, `pilot_2019_responses_and_draw.xlsx`) discloses the same three measure strings in a `measure` column anyway, so naming them costs nothing. What the mechanical sweep didn't call out is that §4.2–4.6 of this same document file the literal **formulas** for five graded figures: the definition of "saving," the lifetime-tonnes/saving-rate/grant-per-tonne formulas, the CO2 factor (0.201 t/MWh), the service-life table (30/15/10 years), the binary fund-all-or-fund-none threshold rule at €120/tonne, and the CO2-monitoring formula reused in the prompt's last ask. This is the single densest concentration of "written down, therefore executed" method in the pack. It does not, however, hand over any of the formulas' *inputs* (see Q6).

2. **grant_offer_2026_terms.pdf** — Harmless. It names the measures (same reasoning as above) and restates the €120/tonne rule the prompt already states verbatim, so nothing new leaks there. It mainly files population/window facts (eligibility, the 30 June close, the revised-quote-replaces-earlier dedup rule, the pay-on-completion-only condition) — the WHAT, not a shortcut to any figure.

3. **pilot_2019_rules.pdf** — Harmless, and arguably useful framing rather than a leak: besides naming the measures, it discloses that 2019 places were allocated **by public lottery**, which is a legitimate hint toward a causal design (a randomized control group exists) but never prescribes using it that way, and it tells the solver that withdrawals and completion dates are tracked fields to look for, not what their values are.

4. **The prompt's missing rounding sentence** — Not a leak (it discloses no figure or method), but a real gap against the house prompt-writing rule ("rounding once at the end"). Confirmed: `prompt.txt` has no rounding instruction anywhere. This is a compliance/grading-consistency gap for the author to fix, not an information disclosure.

### 1. Sentence/file that tells you how a step, comparison, adjustment, grouping, population or window should be done (quoted)

Several, all from the governing PDFs:
- `climate_action_plan_2023_extract.pdf` §4.2: *"A measure's saving in a season is the gas its works save, as a share of the gas the buildings that had them would have used that season without them, both in a season of long-term average weather."*
- §4.3: *"A season runs from 1 May to 30 April. Gas use in a season of long-term average weather is the season's use normalised as Stadtwerke Haldenau normalises it for its benchmarking notices."*
- §4.4: *"An application's lifetime tonnes are the CO2 in the gas its measure's works would save in the building applied for over the measure's service life, each year's saving taken on the application's reference consumption, at 0.201 tonnes of CO2 per MWh of gas... The council funds a measure in a round when its grant per tonne is €120 or less, and then funds every application for that measure in the round."*
- §4.6: *"the gas the buildings with works would have used that season without them, less what they used, both in normal weather, at the factor in 4.4."*
- `benchmarking_method_2022.pdf` §3: *"the hot water and process share of the use type is held as it is, and the rest is scaled by the station's long-term degree days (G20/15, 1991 to 2020 mean, 3635) over the season's."* — this is the exact weather-normalisation recipe §4.3 points to.
- `grant_offer_2026_terms.pdf` §2: *"An owner who revises the quote sends the application again; the later application replaces the earlier one."* — fixes the population rule for "applications received so far" (dedupe to the latest per building+measure). Confirmed in the data: 29 `building_id`s in `applications_2026.xlsx` appear twice with a later `received` date and a different quote/grant.

### 2. File that already ranks or scores the three measures on the prompt's question

None. I checked every column header and grepped file contents for rank/score/recommend/flip/tonne-per-grant style terms; nothing pre-computes or orders the three measures' grant-per-tonne, saving rate, or fundability. No workbook has a "funded" flag or similar.

### 3. File that exists only to help the analyst (describes data / narrates how files fit together)

None of the 19 is a pure data dictionary or glossary. Every file is either raw operational/measurement data or a real-standing document (a city ordinance, a utility method note, grant terms, a committee memo). `committee_request_2026-06-15.docx` comes closest to a "helper" document, but it's framed as a stakeholder's request (who's asking, the meeting date, what's needed) rather than a description of the data; `benchmarking_method_2022.pdf` explains the utility's own metering/normalisation method (a genuine field-standard note the climate plan cites), not this dataset's structure.

### 4. Figure or name that reads as the answer rather than context

None found. The €120/tonne threshold appears in the climate plan and the committee memo, but it is already given verbatim in `prompt.txt` itself, so nothing new is disclosed. The service-life table (30/15/10 years) and the 0.201 t CO2/MWh factor are formula inputs, not outputs. No measure name, building, or number is singled out, bolded, or repeated in a way that signals it as "the" funded measure.

### 5. Filed sentence that, read literally, fixes how a graded figure is computed or over which population (quoted, with what its literal reading gives)

The clearest case is `climate_action_plan_2023_extract.pdf` §4.4 (quoted above). Literally read, it gives: for every individual application, lifetime tonnes = the measure's saving rate applied to that application's own reference consumption, converted to CO2 mass at a fixed 0.201 t/MWh factor and carried over a fixed, measure-specific service life (30/15/10 years); a measure's round-level "saving rate" is its applications' total lifetime tonnes divided by the tonnes their combined reference consumption would carry over that same life; a measure's "grant per tonne" is the round's total grant for that measure divided by that same lifetime-tonnes total; and the funding population rule is binary and all-or-nothing — a measure is funded only if that one ratio is €120 or under, and if so every application for it is granted, with no per-application cutoff, and if not, none is.

A second, equally literal one is §4.6: its population is "the buildings with works" (drawn, not withdrawn, completed) for the single season 2025/26, and its value is normal-weather counterfactual use minus actual use, at the §4.4 factor — i.e. the same before/after comparison as §4.2's "saving," just scoped to one season and expressed in tonnes rather than a percentage.

### 6. Is there one thing that would make most of the prompt routine? And which parts (if any) are rule-following rather than analysis?

No single file, sentence, column or built-in pattern does this. The nearest candidate is the climate-plan's §4.2–4.6 plus the benchmarking method's §3 normalisation formula, which together hand over the literal arithmetic for lifetime tonnes, saving rate, grant per tonne, the funding threshold, and the CO2-monitoring figure. But none of those formulas' inputs are handed over, and getting them right is most of the task:

- **"Saving" itself is not given.** It is the one number that drives lifetime tonnes, saving rate, grant per tonne and the fund/no-fund call for all three measures, and it has to be built from six-plus years of raw, messy meter data (389,106 `gas_meter_reads` rows, with `estimate`/`correction`/meter-swap rows, apportioned between uneven read dates by degree-day weighting, and the HN-3 network area's L-gas→H-gas calorific jump at 2017/18, which I confirmed in `calorific_values_2013_2026.csv`: ~10.0 kWh/m³ before, ~11.3+ after), scoped to exactly "the buildings that had" each measure (which itself requires combining the pilot workbook's draw/withdrawn/completed fields — nothing pre-flags "works buildings").
- **The one file that looks like a ready-made shortcut isn't one for the population that matters.** `benchmarking_notices_2019_2026.csv` already carries a `normalised_use_kwh_per_m2` column, but a building only gets a notice when its usage is in the top fifth of its use type — exactly the condition retrofitted buildings tend to drop out of after their works succeed. I checked this directly: several sampled 2019 pilot "works" buildings have a notice only in 2018/19 (before works) and never again, while others keep appearing every year. A run that read "saving" off this file alone, without noticing the coverage gap, would be quietly working from a shrinking, biased subset of the works buildings — a textbook "narrow look at broad data" failure, not a shortcut.
- **No document specifies the counterfactual method.** The pilot's lottery (drawn vs. not-drawn) is disclosed as a fact of how places were allocated, but nothing tells the solver to use the not-drawn group as a control, or how to project "what they would have used" six seasons out for the 2025/26 monitoring figure.
- **The 90% range, the flip-rate sensitivity, both forecasts (application count and paid-out amount), and the completion/withdrawal rate behind the second forecast have no formulas anywhere in the pack** and must be built from the pilot's own historical pattern and/or the applications' own arrival curve (data runs only to 12 June per the committee memo and `applications_2026.xlsx`'s own `received` column, while the offer runs to 30 June per the terms).
- **Cross-file reconciliation is genuinely messy, not routine:** `buildings_register_2026.xlsx` and `solar_cadastre_rooftops_2024.xlsx` match on (address, postcode) for only about 84% of the 24,000 buildings (20,159 of 24,000), implying address-format cleanup wherever that file is drawn on.

So: a few sub-steps genuinely are rule-following rather than analysis — the fund/no-fund cutoff itself once the ratio is known (a literal €120 threshold test), the revised-application dedup (a named hygiene rule), and plugging a given application's own reference consumption into the lifetime-tonnes formula once the measure's saving rate is established (arithmetic). But the figures that actually decide the recommendation — each measure's own saving (and therefore its saving rate, grant-per-tonne and flip point), the uncertainty band, both forecasts, and the 2025/26 monitoring figure — all turn on open analytical choices and real data assembly that no file makes for the solver.

### Generated-looking / padding check

- All 6 PDFs are single-page LibreOffice Writer exports with plausible, *different* LO versions tracking their stated dates (6.2 for the 2019 pilot rules, up to 25.8 for the 2026 heat-plan summary); no FPDF/ReportLab signatures, no identical boilerplate beyond a shared department letterhead style (expected, same city department). Prose reads as terse municipal/technical register, not LLM-flavored filler.
- `committee_request_2026-06-15.docx` has plausible core/app properties (revision 3, 41 minutes total editing time, created and modified the same morning), no tracked changes, no comments.
- All 4 xlsx files have correctly scrubbed metadata (real-looking per-source Creator/Company — Stadt Haldenau, Stadtwerke Haldenau, and "Landesanstalt für Umwelt Baden-Württemberg" for the solar cadastre — "Microsoft Excel" as Application, timestamps tracking the narrative dates, e.g. the pilot workbook created 2019-07-08 and modified 2019-10-07). No hidden sheets, no cell comments, no tracked changes, no stray chart/externalLink parts in any of the four. Minor tells only: all four share an identical `AppVersion` ("16.0300") despite three different source organisations, and every internal zip member across all four carries the generic 1980-01-01 DOS-epoch timestamp (a common openpyxl default) — faint library fingerprints worth a scrub pass, not an information leak.
- A whole-pack grep for toolchain/path signatures (sulfur, sulphur, task-number, golden, rubric, solver, openpyxl, generator, precut, claude, anthropic, fpdf, reportlab, /Users/) returned nothing.
- Nothing reads as pure unused padding on its own. `federal_funding_overview_2025.pdf` (a separate federal BEG grant scheme) and `municipal_heat_plan_2026_summary.pdf` (district-heating/heat-pump rollout dates) both look like plausible distractors: realistic and topic-adjacent, but neither is referenced by any data column and neither changes any formula the prompt's asks depend on. `solar_cadastre_rooftops_2024.xlsx` and the two electricity files (`electricity_customers_annual_2019_2025.csv`, `electricity_load_profiles_2025.csv`) aren't explicitly called for by the prompt's literal wording either, but they do join cleanly to `buildings_register_2026.xlsx` (load profiles cover all 24,000 customer numbers at what look like a handful of standard shapes, consistent with German standard-load-profile allocation; the annual-actuals file covers a smaller metered subset of 10,821), so they read as usable cross-file material rather than padding, just not strictly required by the question as worded.
