# leak check, task13

**Verdict: REVIEW.** 29 files read, 105 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: crew-day, missed, dismissed, evidence, clearance, exports, coupled, repeats, independent, physical, switching, reliability, single, washes, infeed, structures, contamination, underbuild, reflex, records, chronological, mutual, distinct, component, grow-in

## 3 answer figures in the pack (REVIEW 8)
- **REVIEW** `esdd_monitoring_2022-2026.xlsx`: golden figure 0.0343 appears: ...00:00 0.0406 0.0373 Crew 2 T2 2022-09-07 00:00:00 0.0343 0.181 Crew 2 T8 2022-09-07 00:00:00 0.001 0.747 C...
- **REVIEW** `esdd_monitoring_2022-2026.xlsx`: golden figure 0.0657 appears: ....0378 0.0898 Crew 5 T4 2026-10-06 00:00:00 0.0701 0.0657 Crew 5 T6 2026-10-07 00:00:00 0.0867 1.6439 Crew...
- **REVIEW** `esdd_monitoring_2022-2026.xlsx`: golden figure 0.0551 appears: ....0578 0.8251 Crew 4 T5 2025-07-21 00:00:00 0.0343 0.0551 Crew 2 T4 2025-08-05 00:00:00 0.0713 0.0515 Crew...
- **REVIEW** `esdd_monitoring_2022-2026.xlsx`: golden figure 0.0585 appears: ...0.0565 1.0947 Crew 5 T1 2022-05-14 00:00:00 0.029 0.0585 Crew 5 T3 2022-05-14 00:00:00 0.0801 1.0625 Crew...
- **REVIEW** `esdd_monitoring_2022-2026.xlsx`: golden figure 0.0571 appears: ...:00:00 0.0024 1.323 Crew 4 T3 2024-04-18 00:00:00 0.0571 1.4778 Crew 2 T5 2024-04-19 00:00:00 0.0423 0.085...
- **REVIEW** `esdd_monitoring_2022-2026.xlsx`: golden figure 0.0541 appears: ...00:00 0.0319 0.1899 Crew 2 T6 2022-08-12 00:00:00 0.0541 0.8198 Crew 4 T5 2022-08-15 00:00:00 0.0329 0.043...
- **REVIEW** `esdd_monitoring_2022-2026.xlsx`: golden figure 0.0509 appears: ...:00:00 0.001 0.2314 Crew 4 T2 2024-09-08 00:00:00 0.0509 0.2611 Crew 2 T4 2024-09-11 00:00:00 0.0704 0.051...
- **REVIEW** `reliability_reporting_procedure_rev5.docx`: carries 34 of 38 distinctive words of the committed call: 'Allocate all 36 winter and spring 69 kV crew-days under RP-04 Rev 5 to 9 due coastal washing sections (9 crew-days: Line'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `reliability_reporting_procedure_rev5.docx`: 8 of 25 stump-paragraph terms appear (crew-day, switching, reliability, single, structures, contamination); read whether the document names the move

## 8 column names (REVIEW 2)
- **REVIEW** `relay_records_gridvue_2022-2026.json`: columns a generator names and an organisation does not: generated, device, device, device, device, device, device, device
- **REVIEW** `substation_weather_stations_2023-2026.csv`: columns a generator names and an organisation does not: air_temp_c

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: deliverable formats: asks for a written document (memo.docx): the house set is a CSV, a workbook and at most a deck; keep one only where the decision's reader needs it, with the reason in the design note

## 12 describing content (REVIEW 1)
- **REVIEW** `reliability_reporting_procedure_rev5.docx`: names 16 column(s) of the data files verbatim (Breaker, Cause, Relay, cause, count, crew): confirm it is the organisation's own record and not a note written for the analyst

## 12 client quality check (INFO 2)
- **INFO** `-`: 29 usable files (10 or more required)
- **INFO** `-`: 4 file categories: database, document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 9 dates after the setting (clean)

## Solver's-eye read

Isolated Stage 4 Pass 2 read (`leak-reader-v4` on fresh scratch copy of `prompt.txt` and `target/` from locked build `target` digest `75ee2c97a47fa856`, `golden` digest `53db54223415c0c9`).

### Questions 1-6

1. **Method or step announcement:** None that announces an analytical method, adjustment, or solving step. Only governing reporting definitions, populations, windows, and the cooperative's Priority 1 scheduling policy appear in `reliability_reporting_procedure_rev5.docx` (Section 2, `Definitions`):
   - Fault population/grouping: `"One protection operation sequence on one 69 kV line: the trips, the reclosing and any lockout that follow one initiation within 60 seconds count as one fault. Breaker operations for switching, testing or maintenance are not faults. A fault on another line that a relay sees without tripping is not a fault on the relay's line."`
   - Reporting window: `"The calendar year. In a report made in November, the current year runs from 1 January to 31 October."`
   - Repeat-location grouping: `"A structure, a span, or a contiguous run of adjacent structures (no more than 400 m long, or up to 800 m along a single outside-right-of-way timber stand) at which three or more faults of one cause have occurred on one line since 1 January 2022; faults of the same cause falling within 400 m of another fault in the same run belong to that single repeat location. Salt contamination is dealt with by the washing program section by section and is not entered as a repeat location."`
   - Washing window/standing: `"A washing section is due when the contamination state on its porcelain insulators on 31 October is at or above the contamination level at which the cooperative's 69 kV porcelain line posts have flashed over in fog. The fog season runs from 1 December to 31 March."`
   - Priority 1 allocation rule: `"When open work exceeds the cooperative's fixed winter and spring 69 kV line-crew allowance (36 crew-days), all coastal washing sections due before 1 December are scheduled first (1 crew-day per section). The remaining crew-days are allocated to qualifying unfixed repeat locations in descending order of cumulative historical member-minutes since 1 January 2022 through the reporting cutoff per crew-day using standard crew allowances: avian guards 1 crew-day; insulator string replacement 2 crew-days; vegetation grow-in clearing 2 crew-days; outside-right-of-way hazard-tree removal 3 crew-days; equipment or hardware repair 3 crew-days. Any location whose crew allowance exceeds the remaining crew-days is skipped and deferred to the Priority 2 backlog; exact ties are broken by total fault count, then line and structure number."`
   - Neither `prompt.txt`, `protection_study_2022.pdf`, `protection_study_2025.pdf`, `relay_settings_69kv_2026.xlsx`, `esdd_monitoring_2022-2026.xlsx`, nor any operational log announces how to reconcile relay formats/units/clocks, adjust single-ended fault distances for mutual coupling or IPP infeed, diagnose unlabeled causes, model contamination buildup/wash-off/thresholds, or reconstruct transfer-scheme restoration times.

2. **Pre-ranked candidates (Gate G):** none. (`tower_and_pole_condition_survey_2025.xlsx` contains contractor wood-pole physical condition scores `"Overall rating (1 best to 5)"`, which do not rank lines, repeat locations, washing sections, or Priority 1/Priority 2 reliability candidates.)

3. **Helper-only artifact:** none. All 29 shipped files serve authentic electric-cooperative engineering, protection, SCADA, OMS, field-patrol, maintenance, vegetation, contamination-monitoring, avian-protection, land-ROW, or weather/lightning purposes.

4. **Answer leak:** none. No shipped file states fault counts, 2026 member interruptions/member-minutes, repeat-location rosters, flashover contamination thresholds, 31 October washing standings, or Priority 1/Priority 2 schedules.

5. **Literal-rule execution:** All literal grading rules are filed in `reliability_reporting_procedure_rev5.docx` (Section 2):
   - Fault sequence definition: fixes the fault population by collapsing multi-shot reclose/lockout sequences within 60 s into one fault and excluding switching/test triggers and non-tripping external-line pickups.
   - Fault location definition: fixes current-inventory structure numbering and single-structure vs two-structure span reporting.
   - Cause taxonomy: fixes the 9 allowed cause labels.
   - Member interruption definition: fixes the >5-minute sustained threshold, substation-restoration endpoint, and attribution to the energizing 69 kV line at fault time.
   - Reporting year: fixes calendar-year aggregation and the 2026 cutoff at 31 October 2026.
   - Repeat location definition: fixes the >=3 fault threshold since 1 Jan 2022, 400 m / 800 m chaining rules, and exclusion of salt contamination.
   - Work list definition: fixes open vs resolved status (unfixed since last fault) and remediation categories.
   - Washing standing definition: fixes the 31 October evaluation date, porcelain-insulator scope, and empirical historical fog-flashover standard.
   - Priority 1 winter and spring work program: fixes the 36 crew-day budget, washing-first scheduling, greedy ranking by cumulative member-minutes (1 Jan 2022 through 31 Oct 2026) per crew-day, crew allowances (1, 2, 2, 3, 3), skip-to-Priority-2 deferral, and tie-breakers.

6. **Single-thing / banned-stump check & realism tells:**
   - **No single-thing shortcut.** No single file, column, sentence, or planted trick settles most of the prompt. The task requires multiple independent analytical tracks: (a) consolidating heterogeneous relay/SCADA/electromechanical records and modeling physical fault-location distortions from double-circuit mutual coupling (Lines 10/11, with Inland bus Z0 changing after the March 2024 T1-to-T2 replacement) and grounded-wye IPP zero-sequence infeed (Lines 8/9), alongside current-inventory mapping; (b) multi-evidence root-cause attribution combining lightning strokes, airport and substation meteorology, hourly SCADA line loading, avian roost coordinates, and patrol logs where shift logs read `UNK` or `WIND`; (c) reconciling sustained (>5 min) member interruptions and member-minutes across `scada_soe_2022-2026.csv`, `oms_extract_2022-2026.sqlite`, and `members_by_feeder_monthly_2022-2026.csv`; (d) empirical contamination modeling on porcelain insulators (ESDD + NSDD, corridor surface, coastal distance, wash resets, rainfall) calibrated to actual historical fog flashovers to determine 31 October washing standings; and (e) repair-status verification across maintenance/vegetation work orders feeding the 36-crew-day Priority 1/Priority 2 allocation.
   - **Per-part assessment:** Every requested deliverable (fault CSV, annual line/cause counts, 2026 member interruptions and member-minutes, repeat locations and repair status, coastal washing standings, and ranked Priority 1/Priority 2 schedules) turns on genuine cross-source engineering and statistical modeling rather than catching a single planted code/unit/definition.

### Realism & Date Consistency

- **Cutoff and timezone consistency (as-of November 2026, data through 31 October 2026):** Consistent across all 29 files. `relay_records_gridvue_2022-2026.json` carries `"generated": "2026-11-03T09:06:41"` with records through `2026-10-01`. All local-time operational files end on or before `2026-10-31`, and UTC files end at `2026-11-01 04:53` UTC (`2026-10-31 23:53` CDT). Zero post-November-2026 dates or future-dated documents.
- **Minor non-leaky realism tells:** Two 2022 full-line patrol rows (`8007`, `8009`) show post-rebuild `To structure` counts alongside pre-rebuild pole findings; six added Line 8 structures (`L08-001` to `L08-006`) retain `insulator_installed = 1983`; reference `In service` and routine `Settings issued` dates fall on days 10 and 09 respectively. None leak answers or analytical steps.

### REVIEW Item Verdicts

- `reliability_reporting_procedure_rev5.docx` (sweeps 3, 4, 12): **harmless** - Authentic utility procedure (RP-04 Rev 5) filing operational WHAT definitions, reporting cutoffs, cause taxonomy, and the 36-crew-day Priority 1 allocation policy needed for determinism; standard domain terms and schema vocabulary appear solely as governing definitions without naming ESDD/NSDD variables, formulas, thresholds, or solving cues.
- `relay_records_gridvue_2022-2026.json` (sweep 8): **harmless** - Envelope key `"generated"` (`"2026-11-03T09:06:41"`) and record key `"device"` are authentic utility SCADA/relay export schema fields.
- `substation_weather_stations_2023-2026.csv` (sweep 8): **harmless** - Column header `air_temp_c` is standard meteorological nomenclature alongside `rh_pct`, `dewpoint_c`, `wind_ms`, `wind_dir_deg`, and `rain_mm`.
- `esdd_monitoring_2022-2026.xlsx` (sweep 3, 7 four-decimal matches: `0.0343`, `0.0657`, `0.0551`, `0.0585`, `0.0571`, `0.0541`, `0.0509`): **harmless** (main-thread check) - Coincidental collisions across 430+ raw 4-decimal coupon ESDD/NSDD readings (2022-2026) with derived 31 October 2026 projected effective-ESDD values and the empirical 10th-percentile threshold; none is labeled as a threshold or 31 October projection.
- `prompt.txt` (sweep 11, deliverable formats): **harmless** (main-thread check) - One-page Word memo for the Manager of Engineering is documented in `DESIGN_NOTE.md` as the standing sign-off artifact for the cooperative's winter and spring work list alongside the CSV and review workbook.

## Verdict

**CLEAN** - No answer leaks, method announcements, pre-ranked candidates, helper-only artifacts, or single-thing shortcuts appear in `prompt.txt` or any of the 29 shipped files. All REVIEW items are harmless operational, schema, or coincidental-precision artifacts, and date boundaries are consistent with a November 2026 report covering data through 31 October 2026.

