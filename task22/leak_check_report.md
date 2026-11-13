# leak check, task22

**Verdict: REVIEW.** 22 files read, 33 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: lakeview, station, diversion, college, halvorsen, collapse, missed, correctors, airport, riverside, spread, nearest, stations, winter, downtown, golden, shortcut, modelling, result, january, evenly, booked, method, constructed, sendout

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `lauf_reduction_program_rules_2026.pdf`: golden figure 1.0 appears: ...twelve months ending September 30, 2026 exceeded 1.0 per cent of the gas delivered into it in the same...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `gas_temperature_study_memo_2025-06.pdf`: 8 of 25 stump-paragraph terms appear (lakeview, halvorsen, airport, riverside, winter, downtown); read whether the document names the move
- **REVIEW** `lauf_reduction_program_rules_2026.pdf`: 4 of 25 stump-paragraph terms appear (station, correctors, stations, downtown); read whether the document names the move
- **REVIEW** `lauf_study_fy2019_consultant_report.pdf`: 4 of 25 stump-paragraph terms appear (station, airport, result, january); read whether the document names the move

## 6 ranking artifacts (REVIEW 4)
- **REVIEW** `gas_temperature_study_memo_2025-06.pdf`: names 3 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `premise_meter_register_2026-11-02.xlsx`: names 6 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `third_party_damage_reports_2023-2026.xlsx`: names 6 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `utility_own_use_2023-2026.xlsx`: names 6 of 7 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'pptx+xlsx' at 24% of 21 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 22 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Architecture 1's two reads (the feeder pack) are in the READY commit 5592461's copy of this report.

### First read (isolated, medium effort, on the fresh cut of 2026-11-12, before the stage 4 fixes)

#### 1. Sentence/file that tells you how to do the analysis
`lauf_reduction_program_rules_2026.pdf` is the main one, in-universe as a Commission resolution: "Leak loss in a pressure district is the gas delivered into the district at its regulator stations, less the gas the district's customers took through their meters, the Utility's own use in the district, gas lost to third-party damage in the district and gas taken in the district without authorization" (the exact bridge the prompt's parenthetical lists); "Rule 1, main replacement. A pressure district enters the 2027-2029 main replacement program if its leak loss in the twelve months ending September 30, 2026 exceeded 1.0 per cent of the gas delivered into it in the same twelve months"; "Rule 2, meter changeout. ... exceeded the volume billed for them by more than 3.5 per cent of that billed volume, and where at least 100 such meters remain in service"; "Rule 3 ... Old Town and Downtown proceed as planned and are not re-decided under Rule 2." Also `gas_rate_schedules_2026.pdf`: "multiplied by the pressure factor 0.9663" and "The gas day is the 24 hours beginning at 9:00 a.m. Central Clock Time." Also `meter_changeout_plan_2027.xlsx` (sheet "Plan", last row, a footnote below the data): "The heating season begins November 1."

#### 2. File that ranks/scores the districts on the decision question
None. No column anywhere named rank/score/flag/exceed/qualify/priority; checked headers in all 22 files and full-text-searched all xlsx cell values for those words, no hits.

#### 3. File that exists only to help the analyst
None. No readme/data-dictionary/field-notes file. The closest is the "Meter models" lookup sheet inside `premise_meter_register_2026-11-02.xlsx` (Model/Type/TempComp/InService), but it reads as a real GIS/records code table embedded in the register, not a note addressed to whoever analyses the data. The few footnotes found (e.g. annual_lauf_report's "Sales: volume billed on bills issued...", utility_own_use's "Station heaters: rated input times heating hours...") explain how that file's own numbers were produced (provenance), not how to do the task.

#### 4. Figure/name that reads as the answer rather than context
None found naming a specific district. Closest candidate: `annual_lauf_report_fy2019-fy2026.xlsx` row "FY2026 ... LAUF % 2.42" covers Oct 2025-Sep 2026, the exact window Rule 1 names, but it is the whole utility, not any one pressure district; a hurried reader could mistake it for a ready-made answer instead of doing the per-district build.

#### 5. Filed sentence fixing a graded quantity/population, literally
`lauf_reduction_program_rules_2026.pdf`: "A pressure district enters the 2027-2029 main replacement program if its leak loss in the twelve months ending September 30, 2026 exceeded 1.0 per cent of the gas delivered into it in the same twelve months." Literal execution, in words: once each district's own leak loss and gas-in are built for that one fixed twelve-month window, the membership call becomes a single ratio-versus-cutoff test per district, applied the same way to every district with no further judgment.

#### 6. The one thing, and what it settles per ask
The rules PDF is that one thing: it fixes the balance's column definitions, both programs' numeric cutoffs, and the Old Town/Downtown carve-out. But it only fixes the *criteria*; it supplies none of the inputs. Per ask: (a) the monthly gas balance turns on real cross-file analysis (AMR reads + pressure factor, corrector dailies, temperature under-registration via a modeling choice between the 2019 Rankine-ratio study and the 2025 memo's regression, own use incl. an unattributed city-gate-line heater, damage, revenue-protection cases), genuine work; (b) leak loss as a share of gas-in is mechanical arithmetic once (a) is right; (c) main-replacement membership follows the stated Rule 1 threshold directly; (d) meter changeout follows Rule 2's threshold plus Rule 3's carve-out, but the "100 meters remaining" count needs reconciling the register against 2024-25 work orders (some "Carried to next program," "No access," "Customer refused"), a mix of rule-following and assembly; (e) "accounts that took gas without authorization" is mostly reading/joining `revenue_protection_cases_2021-2025.xlsx` (11 rows, PressureDistrict already given); (f) the heating-season count turns almost entirely on reading one filed definition, the plan's own PlannedDate values run only to late October 2027, ahead of the filed November 1 start, so this sub-ask is close to a triviality once that footnote is read.

#### Mechanical-sweep lines
- `lauf_reduction_program_rules_2026.pdf`: harmless. The 1.0%/3.5% figures are the program's own decision criteria, not any district's computed result; no district is named beside them. (It is nonetheless the single most load-bearing "how" document, see Q1/Q5/Q6.)
- `gas_temperature_study_memo_2025-06.pdf`: harmless. Districts are named only to describe logger placement; the Results table's numbers are aggregated across all outdoor/all indoor loggers, never broken out per named district.
- `premise_meter_register_2026-11-02.xlsx`: harmless. All 14 districts appear with raw IDs/pressures/cycles across its four sheets; no leak-loss figure, no flag column, no summary.
- `third_party_damage_reports_2023-2026.xlsx`: harmless. 159 flat incident rows across 14 districts, each with its own EstimatedGasLostMcf; no per-district rollup or comparison to any threshold.
- `utility_own_use_2023-2026.xlsx`: harmless. Flat monthly facility rows; no per-district total or ranking.
- `prompt.txt`: harmless. No company name, rule numbers, thresholds, file names or method; it names the balance's line items in plain language that happens to parallel the rules PDF's vocabulary ("leak loss," "own use," "gas taken without authorization"), but those are standard LAUF-accounting terms, not task-specific tells.

#### Realism
Checked PDF (`pdfinfo`) and xlsx (`docProps/core.xml`) metadata on all 11 documents: distinct creators per file (Utilities Finance, Gas Engineering, GIS and Records, Customer Service, Gas Operations, Measurement and Regulation), distinct creation/modified timestamps consistent with each file's own date range and content, varying LibreOffice versions appropriate to each document's era, no hidden sheets. No placeholder/LLM-sounding text found (grepped for lorem/test123/foo/TODO/placeholder etc., no hits). District names are spelled identically across every file (cross-checked premise register against revenue-protection, damage, own-use and work-order files, no mismatches). No defect spotted.

### Main thread rulings on the first read

- The REVIEW lines: harmless, as the reader ruled each (the rules' 1.0 per cent is the program's line; the memo, the
  register, the damage reports and the own-use file name districts beside raw records and rank nothing).
- The rules, the rate schedules and the plan's note (question 1): they file what is decided and the conventions (the
  balance's terms, the lines, the window, the pressure factor, the gas day, the season's start), never a method.
- The FY2026 utility-wide LAUF (question 4): the incumbent's billed-basis figure, no district; harmless.
- The accounts read off the revenue protection cases (question 6e): the cases were all found before the window; the
  prompt now asks for "the accounts that took gas without authorization in the program's twelve months".
- The scheduled changeouts as near trivial (question 6f): the plan's dates all precede November 1, so counting them
  all is the hurried shortcut; the prompt asks how many "will be done", and the 2024 and 2025 work orders carry the
  pace (SF14). Kept.
- Not raised by the reader but removed in the same pass: the gas rate schedules' meter-access clause (an inside meter
  takes an appointment), the mechanism R8's pace turns on. The billed volume pinned to "the gas its meters took that
  month".

### Second read (isolated, medium effort, on the cut after those fixes)

#### 1. Sentence/file that tells you how to do part of the analysis
`lauf_reduction_program_rules_2026.pdf` gives the literal test for both headline asks: "A pressure district enters the 2027-2029 main replacement program if its leak loss in the twelve months ending September 30, 2026 exceeded 1.0 per cent of the gas delivered into it in the same twelve months" (Rule 1); "The 2027 meter changeout replaces the meters that do not compensate for gas temperature in each pressure district where ... the gas those meters delivered at base conditions exceeded the volume billed for them by more than 3.5 per cent of that billed volume, and where at least 100 such meters remain in service" (Rule 2); "The changeouts the 2027 plan already schedules in Old Town and Downtown proceed as planned and are not re-decided under Rule 2" (Rule 3 pre-decides 2 of 14 districts by name). `meter_changeout_plan_2027.xlsx`'s trailing note fixes a date: "The heating season begins November 1."

#### 2. File that already ranks/scores the districts
None. Rule 3 plus the plan file's scope (it contains only Old Town and Downtown) pre-settles those two by rule, not by a computed score; no file ranks all 14 on leak-loss % or under-registration %.

#### 3. File that exists only to help the analyst
None. Every file is an operational business record. The "Meter models" tab inside `premise_meter_register_2026-11-02.xlsx` is a device catalog (Model/Type/TempComp/InService), a normal engineering lookup table, not a note written for whoever analyses the data.

#### 4. Figure/name that reads as the answer rather than context
The cutoffs (1.0 per cent, 3.5 per cent, 100 meters) and the two names in Rule 3 ("Old Town and Downtown"), plus "The heating season begins November 1," which fixes a date the prompt leaves open.

#### 5. Filed sentence that literally fixes a graded computation
`lauf_reduction_program_rules_2026.pdf`: "Every quantity is measured at base conditions, 14.73 psia and 60 degrees Fahrenheit," modifying "less the gas the district's customers took through their meters..." Literal execution in words: the "customers took" term in the leak-loss subtraction must be the temperature/pressure-corrected volume, not the billed volume; for a non-compensating meter that is billed volume plus that meter's own under-registration, so under-registration is carried out of leak loss rather than counted as loss. Same file: "The Utility's own use is the gas burned in the regulator station heaters." Literal execution: only the 16 "Regulator station heater ..." rows in `utility_own_use_2023-2026.xlsx` count; the 38 district-less "City gate line heater" rows are excluded from every district's own-use subtraction. `meter_changeout_plan_2027.xlsx`: "The heating season begins November 1." Literal execution: the cutoff for the last ask is 2027-11-01; every PlannedDate in the plan already falls between 2027-04-05 and 2027-10-29, so reading that ask against PlannedDate alone counts every scheduled changeout as "before the heating season."

#### 6. The "one thing" test
No single thing routine-izes most of the ask. The thresholds fix the pass/fail boundary for the two district sets but not the values compared to it. Those values still need: a choice of gas-temperature basis (the airport-air ratio method in `lauf_study_fy2019_consultant_report.pdf`, the logger regression in `gas_temperature_study_memo_2025-06.pdf`, the soil-network file, or the commercial correctors' own measured temperature, all of which disagree); reconciling billing lag/estimated AMR reads; prorating case- and incident-level losses into monthly district figures; and applying the base-conditions sentence above. Per part: the monthly balance turns on that analysis; the leak-loss share is arithmetic once the balance is right; the two district sets turn on a stated rule once inputs are right, except Old Town/Downtown's changeout status, which is pure rule-reading (Rule 3); the unauthorized-gas-accounts ask turns on reading a window correctly, since no filed case literally sits inside it; the changeout count turns on one filed date (Nov 1) plus genuine modeling of completion, since plan dates alone all clear it.

#### 7. Ambiguity by ask
"each district's leak loss as a share of its gas in" carries no window of its own (unlike the balance's explicit "October 2023 to September 2026"); could be the three-year total, an annual figure, or the Rule 1 window; no file closes it. "the accounts that took gas without authorization in the program's twelve months": `revenue_protection_cases_2021-2025.xlsx`'s 11 cases all have FoundDate on or before 2025-04-26 (file last touched 2026-01-21, before the Oct 2025-Sep 2026 window even opens); "took gas ... in the program's twelve months" could mean found in-window (literally none) or unauthorized-use period overlapping it. "how many ... will be done before the 2027-28 heating season": "done" vs. "scheduled" is open; the plan fixes November 1 but every PlannedDate already precedes it (max 2027-10-29), so a literal reading yields all of them, while `meter_changeout_work_orders_2024-2025.csv`'s own Completed/No access/Customer refused/Carried-to-next-program history is the only filed basis for a realistic lower count, and no file states which rate to carry forward. The two district sets are pinned, not open, by the base-conditions sentence in Q5.

#### Sweep lines
- `lauf_reduction_program_rules_2026.pdf`: harmless. 1.0 per cent is the Commission's adopted policy cutoff, not a district's result; no district or district-specific number appears.
- `gas_temperature_study_memo_2025-06.pdf`: harmless. Names North End, Riverside, Elm Grove, Halvorsen, Sundquist, Lakeview, Old Town, Downtown only as logger-site locations beside study-wide pooled monthly temperatures; no per-district number or ranking.
- `premise_meter_register_2026-11-02.xlsx`: harmless. All 14 districts appear beside premise counts, outlet pressures and metering-since dates; none compares districts on leak loss or under-registration.
- `third_party_damage_reports_2023-2026.xlsx`: harmless. All 14 districts appear beside per-incident EstimatedGasLostMcf in an unaggregated incident log; no running district total.
- `utility_own_use_2023-2026.xlsx`: harmless. All 14 districts' heaters appear beside monthly estimates, a seasonal fuel series with no comparison or threshold.
- `prompt.txt`: harmless. No attached file named, no method/comparison/threshold/rounding stated, no requester named beyond "our."

#### Realism defect
Every xlsx and pdf in the pack (all 11 checked) has a filesystem save time exactly one hour earlier, in UTC, than its own internal metadata's creation/modified time, e.g. `premise_meter_register_2026-11-02.xlsx`: filesystem 2026-11-02 13:41 UTC vs. internal modified 2026-11-02T14:41:00Z; `lauf_reduction_program_rules_2026.pdf`: filesystem 2026-06-16 23:40 UTC vs. internal CreationDate 2026-06-17T00:40:00Z. That direction is backwards and holds across every document regardless of season, pointing to a one-hour offset bug in the pack's stamping tool rather than anything in the business content. (An earlier read of PDF "EST/EDT" timezone labels looked like a Minnesota/Eastern mismatch but was a rendering artifact of this sandbox's own local clock, not a real file defect, once checked against the raw embedded UTC timestamps.) No other machine-made tells, hidden sheets, formulas, or trap-only files were found.

### Main thread rulings on the second read

- Rules 1 to 3 and the plan's note: they file what is decided (the lines, the window, the two districts the plan
  already covers), not how to compute; harmless.
- The accounts "found in the window" reading: the prompt says "took gas ... in", not "found in"; a run that books none
  also leaves the balance's column at zero, the priced no-diversion shortcut; harmless (the judge ruled the window
  closed).
- "Scheduled" against "done": SF14, ruled by the judge; the band covers the rival pace rates.
- The leak loss share had no window of its own: pinned ("for the program's twelve months, each district's leak loss
  as a share of its gas in and the accounts that took gas without authorization"; SF19).
- The file times an hour behind the internal stamps: the zip entries carry the sender's Central wall clock (08:41 for
  14:41Z) with no UTC field, and the reader's machine runs Eastern time; the container gate's intended form, harmless.

### Third read (isolated, medium effort, the re-pinned prompt only, read against the same cut)

1. No phrase names a method, a comparison, an adjustment, a step, an attached file, a count the data hold or a
   rounding instruction. "Also a short deck for the Utilities Commission" names the recipient Rule 4 of the program
   rules names for the Engineering Manager's filing; it hands over no figure or method.
2. The monthly balance's population, window and units are determinate (the register's districts, the prompt's
   October 2023 to September 2026, the rate schedules' pressure factor). "For the program's twelve months" resolves to
   one period, the rules' "twelve months ending September 30, 2026" (the annual LAUF report and the 2019 study key
   their fiscal years to the same date, with no rival period), and it governs both the share and the accounts. The
   revenue protection cases were all found before the window opens. The heating season resolves through the 2027
   plan's note ("The heating season begins November 1."). The two district sets are Rules 1 to 3's output.
3. Nothing reads as an answer.

### Main thread rulings on the third read

- The Commission as the deck's reader: the prompt names who reads a deliverable, not who asks; harmless.
- The cases found before the window: by design; the accounts are found in the reads, and the cases are the
  history whose pattern tells a bypass and a furnace tap from an absence; harmless.
- Verdict across the three reads: no leak, no helping file, no ranking file, no open fork left.
