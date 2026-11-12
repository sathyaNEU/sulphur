# leak check, task7

**Verdict: REVIEW.** 19 files read, 25 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: buildings, heating, insulation, architecture, controls, building, optimisation, campaign, owners, carried, funded, golden, measured, checks, record, comparison, season, million, lottery, spread, closed, sentence, second, feeder, balanced

## 4 design-note vocabulary (REVIEW 6)
- **REVIEW** `benchmarking_method_2022.pdf`: 3 of 25 stump-paragraph terms appear (building, season, spread); read whether the document names the move
- **REVIEW** `climate_action_plan_2023_extract.pdf`: 8 of 25 stump-paragraph terms appear (buildings, heating, insulation, controls, building, optimisation); read whether the document names the move
- **REVIEW** `federal_funding_overview_2025.pdf`: 7 of 25 stump-paragraph terms appear (buildings, heating, insulation, building, optimisation, owners); read whether the document names the move
- **REVIEW** `grant_offer_2026_terms.pdf`: 8 of 25 stump-paragraph terms appear (buildings, heating, insulation, controls, building, optimisation); read whether the document names the move
- **REVIEW** `municipal_heat_plan_2026_summary.pdf`: 7 of 25 stump-paragraph terms appear (buildings, heating, building, campaign, owners, checks); read whether the document names the move
- **REVIEW** `pilot_2019_rules.pdf`: 9 of 25 stump-paragraph terms appear (buildings, heating, insulation, controls, building, optimisation); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 19 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 9, 2026-11-11: one isolated reader (Sonnet, medium) on fresh copies of prompt.txt and the pack cut at
stage 4 (107 generator checks), briefed with the six questions only (every mechanical REVIEW line was a stump-vocabulary
match, ruled in the main thread and kept out of the brief). The earlier architectures' reads are in git history.
Main thread's rulings, one line each (also in the design note's Leak rulings):
- Q1, the committee's "the range your estimate would have if the pilot had been drawn again": the range's estimand
  (what source of uncertainty it carries), filed so the range is determinate; it names no unit, resampling or method,
  and the reader itself counts the unit as a separate catch. Kept.
- Q1, plan 4.2 to 4.5 and the benchmarking method: WHAT definitions at authority, as the reader says. Harmless.
- Q2 to Q4: none. Nothing to fix.
- Q5, plan 4.5 (reference consumption on the register's floor area): the applications file carries each
  application's reference consumption and every 2026 applicant's notice and register agree, as the reader found; no
  graded figure reads the pilot-era notices' floor areas (the pilot's savings come from the meter reads). Harmless.
- Q5, plan 4.4 (the round's own applications), terms 3 (every application of a funded measure granted, to 30 June),
  method 1 (a replaced estimate gives way): each literal reading is the golden's. Harmless.
- Q6: the closest single fact the reader names is the lottery, settling about two results; it lists the notices'
  survivorship, the owner unit, the round at close and the revised applications as separate catches, and does not
  name the campaign. No one thing settles most of the asks. Harmless.
- The 1980-01-01 entry stamps inside every Office file: what Excel and Word themselves write for every part; each
  file's own docProps stamps differ (H1, audit_containers exit 0). Harmless.
- The reader reads the cadastre and the electricity profiles as unconnected: they carry the transports' drivers by
  address and customer, a join the analysis has to find; the declared distractors are the annual electricity file and
  the federal overview, both of which it also reads as unneeded. Harmless.

### The reader's answers (verbatim, its dashes set as commas under the house rule)

**1. Which sentence or file tells you HOW any part of the analysis should be done (step, comparison, adjustment, grouping, population, window)? Distinguish WHAT a quantity is from HOW to estimate it.**

The one real HOW-leaning sentence is in `committee_request_2026-06-15.docx`: *"the committee will only fund one it can be confident about: where the upper end of its 90 per cent range, the range your estimate would have if the pilot had been drawn again, is €120 or less."* This mostly just restates what `prompt.txt` already says ("the committee's rule of judging each measure at the top of its 90% range"), so it adds nothing beyond the prompt except one clause: it names *what source of uncertainty* the range must reflect (re-running the 2019 lottery), not *how* to compute it (no mention of bootstrap, simulation, or a closed-form formula). The same paragraph pins a window, not a method: *"We set the round on the applications that came in by 12 June."*

Everything else that looks like a "how" is actually a filed WHAT, from `climate_action_plan_2023_extract.pdf` §4.2–4.5, the organisation's own definitions:
- §4.2: *"A measure's saving in a season is the gas its works save, as a share of the gas the buildings that had them would have used that season without them, both in a season of long-term average weather."*
- §4.4: *"An application's lifetime tonnes are the CO2 in the gas its measure's works would save in the building applied for over the measure's service life, against what the building would burn in each of those years without them, each year's saving taken on the application's reference consumption, at 0.201 tonnes of CO2 per MWh of gas."*
- §4.4: *"A measure's saving rate on a round's applications is their lifetime tonnes as a share of the tonnes their reference consumption carries over the same life."* / *"A measure's grant per tonne in a round is the grant of the round's applications for it divided by their lifetime tonnes."*
- §4.5: *"An application's reference consumption is the normalised use per square metre printed on the notice that carried the offer, times the building's heated floor area in Stadtwerke Haldenau's register."*

None of these say how to get the one number the whole chain rests on: the measured seasonal saving percentage per measure. §4.2's only pointer is *"The council takes the evidence of each measure's saving from the 2019 pilot"*; it doesn't say compare drawn vs. not-drawn, doesn't flag that treated buildings can disappear from the notices feed, doesn't say normalize from raw meter reads, doesn't say cluster by owner. `benchmarking_method_2022.pdf` does spell out a detailed HOW (seasons, degree-day weighting, calorific conversion), but it documents the utility's pre-existing method for a different artifact (the number printed on its own notices), not instructions for this question; a solver only needs it once they notice they must rebuild normalized use from raw data for buildings the notices feed drops (see Q6).

**2. Which file already ranks or scores the candidates (the retrofit measures) on the request's question?**

None. `applications_2026.xlsx`, `pilot_2019_responses_and_draw.xlsx`, and `benchmarking_notices_2019_2026.csv` are all row-level (per building/application), never rolled up to the three measures, and no document states a measure's saving rate, grant-per-tonne, or a funding recommendation.

**3. Which file exists only to help the analyst (a data dictionary, readme, or note on how the files fit together)?**

None. Every document is itself a dated, owned, real artifact of one office (a committee letter, pilot terms, a versioned benchmarking method note, a climate-action-plan extract, a federal information sheet, a heat-plan summary) rather than a key to the dataset. The closest candidate, `benchmarking_method_2022.pdf`, is explicitly owned ("Owner: Torben Römer, head of Energy Services") and versioned (v2, superseding v1 2019) as the utility's own internal method record, not a note written to orient the solver across the 19 files.

**4. Which figure or name reads as the answer rather than as context?**

None found. The two numbers that recur everywhere, €120 per tonne and the 90 per cent range, are the decision criteria stated in `prompt.txt` itself and repeated in `committee_request_2026-06-15.docx` and `climate_action_plan_2023_extract.pdf` §4.4; they are the test, not a result. No file states a computed saving rate, a grant-per-tonne value, or names which measure(s) should win.

**5. Which filed sentence, read literally, fixes how a requested figure is computed or over which population?**

- `climate_action_plan_2023_extract.pdf` §4.5: *"An application's reference consumption is the normalised use per square metre printed on the notice that carried the offer, times the building's heated floor area in Stadtwerke Haldenau's register."* Literal reading: multiply the notice's printed per-m² figure by the **current register's** floor area, not whatever floor-area figure is printed alongside it on that same notice. This is a real fork, not a hypothetical one: cross-checking `benchmarking_notices_2019_2026.csv` against `buildings_register_2026.xlsx`, 178 buildings carry a notice-era floor area that no longer matches the register (renovations/extensions over 7 years), and 89 of those 178 are inside the 2019 pilot's own response list, so it matters for whoever reconstructs the pilot-era reference consumption, even though it happens to make no difference for the 2026 applicant set itself (every 2026 applicant's latest notice and the register already agree).
- `climate_action_plan_2023_extract.pdf` §4.4: *"A measure's grant per tonne in a round is the grant of the round's applications for it divided by their lifetime tonnes."* Literal reading: population = that round's own logged applications for one measure, not the 2019 pilot's responses and not every building offered the round.
- `grant_offer_2026_terms.pdf` §3: *"For a funded measure every application received by 30 June 2026 is granted; for any other measure none is."* Literal reading: the funding call is all-or-nothing per measure, and the grant-window runs to 30 June, later than the 12 June cut the committee's decision is based on.
- `benchmarking_method_2022.pdf` §1: *"Where a read is estimated and later replaced, the replacement counts."* Literal reading: in `gas_meter_reads_2013_2026.csv`, where the same meter and date carry two rows (11,865 such pairs in the file), the "estimate" row is discarded in favour of the row that replaced it.

**6. Is there one thing that, once noticed, would make most of the request routine? What would it settle, and for each ask, does it turn on analysis, on reading a field/rule/definition, on a stated procedure, or on catching something planted?**

The closest single fact is the 2019 pilot's lottery, stated in `pilot_2019_rules.pdf` §3: *"Places are drawn by lot among the owners who responded for each measure... an owner who responded for several buildings taking part once with all of them... until each measure's places are filled. Owners not drawn may apply in a later round."* Noticing this tells you that, within a measure, "drawn" and "not drawn" owners are a randomized pair, which is also exactly the resampling frame the committee's letter names ("if the pilot had been drawn again"). That settles the identification strategy for at most two of the chain's results (how to estimate a measure's saving rate causally, and what the 90% range has to resample). It settles nothing else, and each of the following is a separate, unaided catch:
- It does not tell you that `benchmarking_notices_2019_2026.csv` only carries a building while that building sits in the top fifth of its use type (`benchmarking_method_2022.pdf` §4), so a retrofitted building can simply stop appearing. I checked this: only about 76% of treated buildings (1,027 of 1,352) have any post-2019 notice at all, against about 99% of the not-drawn control group (1,656 of 1,678); reading only the notices file for "before/after" would silently drop the buildings that saved the most.
- It does not tell you the draw's randomization unit is the owner, not the building. Building-level balance checks on use-type look significantly skewed by draw status for all three measures (chi-square p≈0.0, 0.002, 0.0001), which looks like a planted confound, but it is a clustering artifact: collapsing to one row per owner (as the rule above requires) makes the same check balanced (p≈0.43, 0.98, 0.94). A hurried, building-level treatment of the lottery misreads clean randomization as a confound, or understates the 90%-range's true width.
- It says nothing about forecasting the applications still to arrive by 30 June from the 21 May–12 June pattern already logged.
- It says nothing about the hygiene needed on `applications_2026.xlsx` itself: 25 buildings carry two rows (a revised quote; the terms say *"the later application replaces the earlier one"*), and the floor-area fork in Q5.

So it rescues roughly 2 of the chain's results, not most of them. Per ask:
- *Which measures the round can fund*: turns on analysis (the saving-rate estimate and its uncertainty); nothing hands this over.
- *Saving rate over its life, per measure*: the ratio itself is a filed definition to apply (§4.4, "A measure's saving rate on a round's applications is..."); the underlying seasonal rate it's built from is analysis (weather-normalized, survivorship-aware, owner-clustered).
- *Grant per tonne with its 90% range*: the point figure is arithmetic on a filed formula once lifetime tonnes are known; the range is analysis (resampling choice, plus the owner-clustering catch above).
- *How many applications once the offer closes, with the grant asked*: partly reading two different filed windows correctly (12 June committee cut vs. 30 June close), partly analysis (forecasting the gap).
- *The list of funded-measure applications, their grant/lifetime tonnes, and the total*: mostly following the filed §4.4 formula and reading fields correctly once the saving rate and funding call are set, plus the dedup hygiene catch (reading which of two rows for the same building is the current one; not a planted trap, the terms document it directly).
- *The one-page recommendation*: synthesis of the above, not a new computation.

**Two more observations, one line each:**

- Machine-generated tell: all five Office Open XML files (`applications_2026.xlsx`, `buildings_register_2026.xlsx`, `pilot_2019_responses_and_draw.xlsx`, `solar_cadastre_rooftops_2024.xlsx`, `committee_request_2026-06-15.docx`) share one identical internal zip timestamp, `1980-01-01 00:00`, on every inner part, despite `docProps` claiming four different organisations and dates spanning 2019–2026, a shared stamp a real sequence of saves from different offices over seven years would not produce; the PDFs and the per-file `docProps` metadata otherwise look individually plausible (distinct authors, realistic creation/modification minutes apart, genuine LibreOffice `/Producer` strings, no FPDF/ReportLab signature).
- File that looks relevant but isn't needed: `solar_cadastre_rooftops_2024.xlsx` (rooftop PV suitability/yield, keyed to the same building addresses) never connects to a gas-CO2 question about insulation/heating-optimisation/heating-controls grants; `federal_funding_overview_2025.pdf` (federal BEG stacking rules) and the two electricity files (`electricity_customers_annual_2019_2025.csv`, `electricity_load_profiles_2025.csv`, keyed by `customer_number`/`supply_address`, not `building_id`) read the same way: plausible, unconnected to any figure the prompt asks for.
