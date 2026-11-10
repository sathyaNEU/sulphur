# leak check, task3

**Verdict: REVIEW.** 15 files read, 15 golden figures and 14 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, missed, design, sensor, waters, campaign, transfer, carried, guidelines, architecture, golden, planning, platform, elevation, inside, floods, result, residual, export, carries, storms, sentence, funded, northside, forecasting

## 1 file names (REVIEW 2)
- **REVIEW** `8673718_datums.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `usgs_02203560_brayle_r_hensley_daily.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `fy2028_tide_valve_round_guidelines.pdf`: carries 9 of 10 distinctive words of the committed call: 'Fund the valves at Wharf Street at Market Lane and Front Street at Ferry Lane.'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `fy2028_tide_valve_round_guidelines.pdf`: 6 of 25 stump-paragraph terms appear (record, sensor, carried, guidelines, planning, elevation); read whether the document names the move

## 6 ranking artifacts (REVIEW 2, INFO 1)
- **REVIEW** `311_service_requests_2023-2026.csv`: names 8 of 14 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `tidal_low_points_inventory_2026-10.xlsx`: names 9 of 14 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `fy2028_tide_valve_round_guidelines.pdf`: names 10 of 14 answer-set candidates; confirm it does not rank them on the decision question

## 8 column names (REVIEW 1)
- **REVIEW** `pt-front-01_2024-05-14_2026-10-31.csv`: columns a generator names and an organisation does not: device_id

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'docx+xlsx' at 27% of 15 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 15 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)


## Solver's-eye read

Isolated reader (Sonnet, medium effort) on fresh copies of prompt.txt and target/ (target.zip 5cc1927b843a50224a47f84691d032aa), 2026-11-10. Main thread's rulings follow the answers.

# Leak read (no solving)

1. Decisive steps. No file states a method outright. fy2028_tide_valve_round_guidelines.pdf (Section 4) fixes the estimand: "Expected tidal flood days. The average number of tidal flood days in the tide year over the weather and river flows of the tide years 1990-91 to 2025-26, on the published tide predictions of the Port Tolliver harbor gauge ... with the gauge's mean sea level for the tide year at the program's planning value." That implies: predictions + shifted MSL + weather-year resampling. Also "Where the lane has not been surveyed, it is the water level at which the utility's street sensor over the travel lane records water on the lane" (points to PT-FRONT-01 for LP-01). Inventory sheet "Tidal creeks" (marsh platform, channel invert) and "Logger campaigns" (sensor elevation, staff checks) hint at the datum/transfer work. Prompt itself names the "weather years" and the split into "sea level, tides and weather".

2. Ranking file: none. No file scores the five low points on expected 2027-28 days. Closest: inventory Low points sheet (lane elevations 4.88 to 5.10, inlet rims) ranks nothing but hands the flooding elevations for four points; 311 requests are context.

3. Help-only files: 8673718_datums.txt (datum table, NAVD88 3.42 vs MLLW; this is the conversion), tidal_low_points_inventory_2026-10.xlsx (inventory/dictionary-like, three sheets incl. logger metadata), fy2028_tide_valve_round_guidelines.pdf (definitions/governing document), slr_scenarios_8673718.csv (scenario reference). The USGS file header is a standard NWIS legend.

4. Answer-like figures: the PDF's "0.70 ft above its 1983-2001 mean sea level" and "8.6 ft above MLLW" are inputs, not results. The lane elevations (4.88, 4.96, 5.03, 5.10) are inputs. Nothing reads as a final count or ranking.

5. Filed sentence fixing computation/population: "The average number of tidal flood days in the tide year over the weather and river flows of the tide years 1990-91 to 2025-26" - literally: average over the 36 historical weather years of the 2027-28 count, run on the published 2027-28 predictions raised to the planning MSL. "A calendar day, in Eastern Standard Time ... to or above its flooding elevation. Rain alone does not make a tidal flood day" - literally: days defined on a fixed EST calendar (no DST), tide only. "The 90 per cent range is the range the tide year's count falls within in nine of every ten of those weather years" - literally the 5th to 95th percentile spread across those 36 years. Tide year = 1 May to 30 April.

6. What decides it: an analytical choice, mainly (how to build weather-year water levels over predictions, convert to NAVD88 using the datums, transfer harbor to the creek/river sites using the short loggers, derive LP-01's threshold from the sensor). Partly rule-following (the PDF's definitions: EST days, tide-year window, planning MSL) and reading units/datums (MLLW vs NAVD88; GMT-05 vs GMT-04 logger headers). Nothing looks planted except possibly the logger offset/clock mismatches below, which read as mess. The deciding sentence is the Section 4 "Expected tidal flood days" definition.

# Realism read

- Logger files contradict the inventory: inventory says HEN-RR-25 deployed 2025-03-01 12:00, retrieved 2025-06-16 09:00; the file runs 01/20/25 12:00 PM to 04/20/25 08:00 AM (4314 rows, 30-min steps) vs inventory "15 min" for all three. OYS (2025-08-25 10:00 to 10-30 14:00) and PEL (2024-09-15 11:00 to 11-21 09:30) match dates but also 30-min vs 15-min. File mtime of HEN is Apr 21 2025, consistent with the file, not the inventory. Either intentional discrepancy or generator slip; a reviewer will notice.
- Time-zone headers: PEL/OYS "GMT-04:00" (DST), HEN "GMT-05:00" in January (consistent with winter); fine, but Oct/Nov 2024 PEL stays GMT-04 across the 3 Nov DST end (header is one fixed offset), plausible for HOBO exports.
- Logger header format ("Plot Title", "LGR S/N", sequential serials 21187431/32/33) is HOBO-like and credible; consecutive serials are slightly neat.
- Inventory xlsx: creator "Port Tolliver Stormwater Utility", modified 2026-10-02; fine. Lane elevations to 2 decimals RTK all surveyed 2023-06-21/22/23 (neat). Marsh platform values given to 2 decimals "2019 LiDAR median" - plausible.
- Guidelines PDF: LibreOffice 24.2, created 16 Oct 2026 13:14 UTC; text issued 16 Oct 2026 and file mtime "Oct 16 09:14", consistent. Round numbers (0.70 ft, 8.6 ft) are policy values, acceptable.
- NOAA files modified in a tight sequence Nov 2 09:12-09:20 (hourly, high_low, predictions, monthly, datums): plausible for a scripted pull but all within 8 minutes. Datums.txt says MSL 3.17 / MHHW 6.79 yet GT also 6.79 (MHHW=GT, coincidence-looking); monthly_means MSL in 1955 is 2.37 vs epoch MSL 3.17, a 0.8 ft gap that is odd for a real series (real Georgia trend ~0.1 ft/30 yr), suggests simulated tides.
- Hourly file: "Predicted" columns do not equal high/low prediction values at 1955-01-01 (0.029 vs hourly 2000 differ by epoch, not checkable); hourly 2000-01-01 Predicted 4.104 vs Verified 3.719 an offset of ~0.39 on first rows, consistent across rows? (not checked).
- pt-front-01: 209,260 rows at exact 6-minute steps, depth 0.00 on first rows, battery 3.61 V jitter; ten-million-byte sensor file with a status column; plausible. Distractors (311 requests, GHCND, USGS discharge for non-low-point use) are unlabelled; USGS and GHCND data look real-format; the 311 file addresses vary in format (RIVER RD @ HENSLEY LANDING, 2200 Marsh Rd) realistically.
- No file names announce a trap.

Rulings: question 1 quotes no sentence naming a step; the guidelines' section 4 fixes the estimand and its literal execution is the golden's (question 5); the sensor sentence defines Front Street's flooding elevation (the WHAT). Question 3's files are the agency datums page, the asset register, the governing round guidelines and a distractor; none describes the data. Realism: the River Road campaign dates in the inventory and the loggers' 30-minute steps were real defects, fixed in the generator (the inventory now carries 2025-01-20 to 2025-04-20; the loggers write 15-minute readings); the 1955 monthly mean is January's seasonal low (the 1955 annual mean is 2.56 ft, a 3.9 mm/yr rise to the epoch, plausible for a subsiding coast); the NOAA products downloaded minutes apart is one session's download.
