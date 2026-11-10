# leak check, task3

**Verdict: REVIEW.** 15 files read, 33 golden figures and 14 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, sensor, missed, design, campaign, waters, architecture, transfer, carried, guidelines, golden, planning, inside, platform, elevation, carries, sentence, funded, floods, result, residual, export, storms, transfers, different

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

### Round 2 read (target.zip 521db5d2edd3226b5e4ae4fde406d10f)

# Leak read (no solving)

1. Decisive steps. fy2028_tide_valve_round_guidelines.pdf section 4 carries most of the method: "The average number of tidal flood days in the tide year over the weather and river flows of the tide years 1990-91 to 2025-26, on the published tide predictions of the Port Tolliver harbor gauge ... with the gauge's mean sea level for the tide year at the program's planning value", "the planning mean sea level standing 0.70 ft above its 1983-2001 mean sea level", and "The 90 per cent range is the range the tide year's count falls within in nine of every ten of those weather years." Also "Flooding elevation. The elevation of the travel lane's low point ... Where the lane has not been surveyed, it is the water level at which the utility's street sensor over the travel lane records water on the lane." Together these hand over the structure: predictions plus weather-year resampling plus a MSL shift, and the flooding elevation per low point. The prompt itself ("expected tidal flood days", "weather years", "split ... into sea level, tides and weather") names the three-way decomposition.

2. No file ranks the five low points. Nothing scores expected days. The inventory xlsx gives only elevations (rim, lane), which are inputs.

3. Helper-only files: fy2028_tide_valve_round_guidelines.pdf (definitions and rules), tidal_low_points_inventory_2026-10.xlsx (inventory, creeks, logger campaigns sheets: a descriptive register), 8673718_datums.txt (a description of datums). The xlsx sheet names carry the word "visible" ("Low points visible", "Tidal creeks visible", "Logger campaigns visible"), which is an odd label suggesting hidden sheets existed; the file has only three sheets, so the name reads as a build artifact.

4. Reads-as-answer: nothing states a final figure. Closest: the guidelines give planning MSL 0.70 ft and harbor threshold 8.6 ft MLLW; these are inputs. The xlsx lists the LP-01 lane as blank ("Lane not surveyed; sensor over the travel lane at the sag") and gives lane elevations 4.95 to 5.13 for the others, so the flooding elevations are given directly, not derived.

5. Filed sentence fixing a main figure: "Expected tidal flood days. The average number of tidal flood days in the tide year over the weather and river flows of the tide years 1990-91 to 2025-26, on the published tide predictions ... of the tide year, with the gauge's mean sea level for the tide year at the program's planning value." Literal result in words: for each low point, the mean over 36 weather years of the count of EST calendar days in 1 May 2027 to 30 April 2028 on which predicted tide, shifted to planning MSL and combined with each weather year's surge and river effect, reaches the lane-low-point elevation. Population/window/unit are all fixed. "Planning mean sea level" literal: 0.70 ft above the 1983-2001 MSL. "Flooding elevation" for LP-02..05 is the "Travel lane low point" column; for LP-01 the sensor's water-on-lane level.

6. What decides it: following a stated procedure plus a modest amount of reading definitions (the guideline's text above; NAVD88 vs MLLW conversion using 8673718_datums.txt, NAVD88 = 3.42 ft above MLLW; the "Rim" vs "Travel lane" columns, the "EST calendar day" clause, the unsurveyed LP-01 rule). The estimand is spelled out in the PDF; the remaining work looks like the method steps the PDF describes. Risk: the PDF largely tells the analyst what to do, and the xlsx column "Lowest inlet rim" vs "Travel lane low point" is a decoy-type choice resolved by one definition sentence.

# Realism read
- 8673718_datums.txt: epoch MSL 3.17 ft MLLW, but monthly means file 2026 MSL values (e.g. 2026-09 MSL 4.254, MLLW 1.135 in the monthly series' own datum) and 1955 MSL 2.370: the monthly file is in a rising local datum while datums.txt is fixed epoch; the two use different zero references, easy to confuse but consistent with real NOAA products. The 2026 monthly "Highest 8.687" and gauge threshold 8.6 fit.
- Hourly file: Date/Time (LST) columns with Predicted, Preliminary, Verified: realistic. High_low observed ends 2026-09-30 while hourly runs to 2026-10-31 and monthly to 2026-09: different pull ends, plausible but mismatched.
- Loggers: PEL-MR-24 header "GMT-04:00" runs through 21 Nov 2024 (after DST ended 3 Nov), so a fixed offset; HEN-RR-25 header "GMT-05:00" in Jan-Apr 2025 (EST, then DST began 9 Mar), also fixed offset. Plausible HOBO behaviour, but internally the two loggers differ, and the xlsx times are local; a time-zone trap for the analyst. Logger deployment/retrieval times in the xlsx (2024-09-15 11:00; 2024-11-21 10:00) match the first/last rows' time of day neatly, retrieval 10:00 vs last row 09:45 (fine). Elevations in xlsx given as "-1.35" while logger sensor "dry at low water": consistent.
- All three loggers deployed at exact top-of-hour times (11:00, 12:00, 10:00) and the staff checks are 0.00 to 0.02 ft: very clean.
- File mtimes: scratch files all from 2 Nov 2026 within minutes (09:12 to 09:31) for NOAA/USGS downloads: sequential pulls, plausible as one session. PEL-MR-24.csv has mtime Nov 22 2024 and OYS-CR-25 Oct 31 2025, HEN-RR-25 Apr 21 2025, matching their retrieval dates: nice but slightly too tidy.
- xlsx internal zip dates all 1980-01-01 (writer-built, not a spreadsheet application save); core.xml created 2026-09-29, modified 2026-10-02 while file mtime is Oct 2: ok. The sheet names ending "visible" are the main oddity.
- pt-front-01 sensor: 6-minute, distance_mm with empty water_level_ft_navd88 column in the first rows; filename covers 2024-05-14 to 2026-10-31 but the last row is 2026-11-01T04:54Z (UTC vs local, fine). 
- 311_service_requests: addresses inconsistent in style (MARSH RD, RIVER RD @ HENSLEY LANDING, 300 Wharf St), good texture. USGS gauge 02203560 file begins 1985-10-01 though weather years start 1990-91: fine.
- Possible planted-looking items: the "Failed"/"Missing" flap gate column, the logger campaigns at three low points with different seasons, and the unsurveyed LP-01 lane tied to a sensor: each exists for one use in the task (a calibration or lane-elevation path per site), mild structure-with-one-use tell.

Rulings: question 5's literal result used the harbor's predicted tide at each low point's lane, which is the no-transfer route; the guidelines' flood day already said "the water at a low point", and the definitions now say "the water at the low point itself, at its outfall" and "a low point's average number of tidal flood days ... with the tide year's astronomical tide taken from the published predictions" (target.zip 09853342), so their literal execution needs each low point's own water and no step is named; question 6's "stated procedure" rests on that reading. The sheet names carry no "visible" suffix (the workbook XML names them Low points, Tidal creeks and Logger campaigns); the zip entries' 1980-01-01 dates are what the spreadsheet application writes; fixed logger offsets are the logger's own behaviour; deployments on the hour and small staff checks are field practice; the three campaigns are what a stormwater utility runs to learn each low point's tide, the use they serve in the world.

### Round 3 read (target.zip 09853342cd300629a1c3fdddc108e23b, the guidelines' definitions pinned at the low point)

# Leak read (no solving)

1. Decisive steps. fy2028_tide_valve_round_guidelines.pdf section 4 states the whole procedure: "Expected tidal flood days. A low point's average number of tidal flood days in the tide year over the weather and river flows of the tide years 1990-91 to 2025-26, with the tide year's astronomical tide taken from the published predictions of the Port Tolliver harbor gauge (NOAA station 8673718) and the gauge's mean sea level for the tide year at the program's planning value." Also "Planning mean sea level ... 0.70 ft above its 1983-2001 mean sea level" and "Where the lane has not been surveyed, it is the water level at which the utility's street sensor over the travel lane records water on the lane." Section 3: "The two with the most receive valves." The inventory xlsx (Tidal creeks, Logger campaigns sheets) names the data to bridge: creek marsh platforms, channel inverts, logger sensor elevations, "Sensor in creek channel 40 ft below outfall; dry at low water". The method (water-level transfer, simulate weather years, SLR/tide/weather split) is not named as such; the guideline defines the estimand.

2. No file ranks or scores the five low points on expected days. The inventory lists rims and lane elevations (4.68 to 5.13 ft NAVD88; LP-01 blank) but no counts. The 311 file has "Flooding - Street" requests per address, which is rain-flavored context, not a ranking.

3. Helper-only files: tidal_low_points_inventory_2026-10.xlsx (describes the low points, creeks, logger campaigns) and 8673718_datums.txt (datum table). fy2028_tide_valve_round_guidelines.pdf is a governing document that also doubles as the definition sheet. The logger CSV headers, the usgs header and the datums file are native source headers.

4. Reads as answer rather than context: none in the pack. Nearest: the PDF's "0.70 ft" planning MSL and "8.6 ft above MLLW" minor flood threshold are inputs, and the xlsx lane elevations (5, 4.95, 5.13, 5.03) are inputs. Nothing states a count or winner.

5. Literal sentences. "Tidal flood day. A calendar day, in Eastern Standard Time, on which the tide brings the water at the low point itself, at its outfall, to or above its flooding elevation. Rain alone does not make a tidal flood day." Literal result: a day counts if the water level at the low point's own outfall (the receiving water at that outfall, i.e. creek for LP-02 and LP-05, Brayle River for LP-03, harbor for LP-01 and LP-04), not the harbor gauge's level, reaches the flooding elevation (travel lane low point in ft NAVD88; for LP-01 the sensor-derived level where the lane records water). Days are EST calendar days (not local daylight time). Also: "Tide year. 1 May to 30 April." and "Expected ... average ... over the weather and river flows of the tide years 1990-91 to 2025-26". The harbor gauge's own count uses "8.6 ft above MLLW".

6. What decides the main answer: an analytical choice chain, not a single read. Per low point the solver must build an outfall-level water model from the gauge, creek/river loggers and river flow (usgs_02203560...), handle datums (MLLW vs NAVD88, 3.42 offset in datums.txt), time zones (logger headers GMT-05:00 / GMT-04:00, sensor in UTC, gauge LST), the sensor's blank water level outside a window (derive from distance_mm), and run weather years. Rule-following is partly involved (the PDF's definitions fix population, window, EST day), but no sentence names the decisive step. The inventory's logger sheet and the "Sensor in creek channel 40 ft below outfall; dry at low water" note are the nearest pointers.

# Realism read
- Gauge files are NOAA-format (datums, high_low, hourly, monthly means); consistent. Odd: monthly_means MSL 2.37 (1955) vs datums MSL 3.17 on the MLLW 1983-2001 epoch, and monthly MLLW column -0.87 in 1955 while datums say 0.00; plausible as a monthly series reported on a fixed datum but the MLLW column varying is unusual, worth a check against NOAA's real format.
- high_low_predictions runs to 2028-04-30 and 1955 start; real predictions are normally not shipped with a 1955-2028 span in one file; fine as a pull.
- pt-front-01: 209,260 rows at exactly 6-minute steps, status 'OK' on every row, battery 3.48 to 3.63 smooth; water_level_ft_navd88 filled for only 13,824 rows (blank elsewhere, starting blank in the first rows); a uniformly perfect status column is slightly too clean. File mtime Nov 3 2026 matches the end-date 2026-10-31.
- Logger CSVs: HEN-RR-25 labelled GMT-05:00 though deployed 01/20 to 04/20/25 (spans the March DST change, so a fixed offset is a header claim that may disagree with local time); OYS and PEL use GMT-04:00 for Aug-Oct and Sep-Nov (EDT, correct; PEL retrieved 11/21/24, after Nov 3 DST end, so GMT-04:00 label vs inventory's local times is similarly doubtful). Row counts match campaigns (8,630 rows ~ 90 days at 15 min).
- Inventory xlsx dated 2026-10 with file mtime Oct 2; guidelines PDF "issued 16 October 2026", mtime Oct 16; consistent. HEN-RR-25 mtime Apr 21 2025, OYS Oct 31 2025, PEL Nov 22 2024: consistent with retrieval dates.
- 311 file: 848 rows with messy address variants; 61 flood requests mention rain; plausible texture, no impossible coincidences.
- usgs file: real NWIS format, A/P codes, data to 2026-10-31 provisional; plausible.
- No identical timestamps across separate downloads; no file with one use besides the inventory/guidelines.

Rulings: question 1 quotes the estimand (the WHAT) and names no method; question 5 now executes to the golden (each low point's own outfall water against its lane, not the harbor gauge's level); question 6 reads an analytical chain. Realism: the monthly MLLW column falls below the epoch's 0.00 in early years because each month's lower low waters sat lower before the sea rose (as in NOAA's own tables); the sensor's status column now carries the battery's sag before each outage, the restarts and weak echoes (target.zip 464e528c); fixed logger offsets are the logger's behaviour.
