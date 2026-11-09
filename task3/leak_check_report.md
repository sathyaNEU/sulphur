# leak check, task3

**Verdict: REVIEW.** 17 files read, 15 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: temperature, record, hourly, station, transfer, basins, storms, carried, orographic, elevation, golden, stations, rain-snow, design, regional, bulletin, degrees, inside, family, decisive, pillows, airport, sentence, valley, regression

## 1 file names (REVIEW 7)
- **REVIEW** `usgs_12181650_annual_peaks.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `usgs_12183450_coyner_r_annual_peaks.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `usgs_12183450_coyner_r_peaks_above_base.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `usgs_12184900_annual_peaks.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `usgs_12186050_annual_peaks.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `usgs_12187200_annual_peaks.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data
- **REVIEW** `usgs_12189500_annual_peaks.txt`: a text file in the pack: confirm it is the organisation's own record (a thread, a log, a letter) and does not describe the data

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `pelton_county_road_standards_ch7_excerpt.pdf`: 7 of 25 stump-paragraph terms appear (record, station, carried, design, regional, bulletin); read whether the document names the move
- **REVIEW** `wsdot_region3_flood_frequency_excerpt.pdf`: 8 of 25 stump-paragraph terms appear (record, station, basins, design, regional, bulletin); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 17 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### Round 4 (the final cut, d36f2053)

Files read: prompt.txt; the three PDFs in full; all seven usgs_*.txt peak files (header, comment lines, samples, tails); the daily-discharge, GHCN-D, LCD and SNOTEL CSVs by header and first rows; region3_basin_characteristics.xlsx, all four sheets (none hidden).

1. Decisive step stated? No single sentence names the deciding analytical step. The documents hand over the frame, not the answer. Closest are the county standard's procedure sentences:
   - 7.4.3: "the design flood comes from stream gauge records, in this order: (a) the record of a gauge at the site ... otherwise (b) the record of the nearest gauged basin holding 25 years or more of annual peaks, carried to the site; (c) the state's regional flood equations only where no gauged basin within 15 miles of the site holds such a record, and only inside the ranges of the equations' explanatory variables."
   - 7.4.1: "on the climate of the gauged and station records. No allowance for a future climate is applied on County roads."
   - 7.4.4: "log-Pearson Type III ... expected moments algorithm, ... Multiple Grubbs-Beck test, and the station skew weighted with the regional skew".
   - prompt: "on the climate the records show" and "Durrow Creek has never been gauged".
   These name a transfer route, a fitting method and the climate basis. Read literally they name a route and a method, and the spreadsheet then makes the route a lookup (see Q5, Q6). Nothing says how to carry or adjust the record across basins whose elevation differs sharply.

2. Ranks or scores the spans on the question? No file ranks them against a 1 per cent flow. The Hess memo (hess_tm_durrow_creek_bridge_span_ratings.pdf) gives each span's rated flow: 140 ft = 20,500 cfs, 185 ft = 29,000 cfs, 240 ft = 40,000 cfs, plus stage tables. It makes no frequency estimate ("makes no estimate of flood frequency"). It is a rating, not a candidate ranking, but it is the only file that scores the spans, and it supplies the thresholds the answer is compared against.

3. Files that exist only to help the analyst: none is a readme, dictionary or purpose-built comparison aid. The nearest are:
   - region3_basin_characteristics.xlsx: the 'Elevation bands' sheet (area by 500 ft band for every gauged basin and Durrow Creek) is a purpose-built comparison aid. A real state flood study appendix does not normally publish hypsometry by band for the site.
   - the Hess memo's closing note: "We are glad to re-run the rating if the County's design discharge falls between the alternatives' rated flows". This is flavor.
   - the WSDOT excerpt's applicability line (4.2): "Estimates outside these ranges are not supported by the data and are not to be used for design." This is a warning that bars the regression route.

4. Figure or name reading as the answer: the three rated flows in the Hess Table 1 (20,500 / 29,000 / 40,000 cfs) are the thresholds, not the answer. No file states a design flow, a 1 per cent flow or the two largest flood years. The site fact that sets the climate problem is the xlsx row "Mean basin elevation (ft) 1870" for Durrow Creek against 6,030 to 6,540 ft for the five high-elevation gauges, and 1640 ft for Selby Creek. Selby is the only gauge of similar elevation, with a 14-year record and 59 in precipitation. The sheet's own distance column shows Selby at 14.6 mi inside the 15 mi limit but with a 14-year record. Coyner (6.2 mi, 1951-2025) is the first-named nearest 25+ year gauge. Neither name reads as the answer, but both are decision-relevant context.

5. Filed sentence fixing the main figure's computation or population: 7.4.3(b), quoted in Q1. Read literally with the xlsx:
   - No gauge at the site, so (a) fails.
   - The nearest gauged basin with 25+ years of annual peaks is Coyner River (86.4 sq mi, 6.2 mi, 1951-2025). Selby is closer-qualifying only by mileage rank (14.6 mi) but has 14 peaks, so it fails the 25-year test. So (b) gives Coyner, "carried to the site".
   - (c) is excluded because a gauged basin within 15 mi holds such a record. Separately, Durrow's 85.3 sq mi is inside 24.8 to 402 sq mi, and its precipitation is not given in the Durrow sheet, so range checking is not possible from the filed sheet alone.
   - 7.4.4 fixes the method as Bulletin 17C EMA with MGBT and weighted skew (regional skew -0.12, MSE 0.13, from the WSDOT excerpt).
   - 7.4.1 fixes the "1 per cent" as instantaneous peak on the records' climate, no future allowance.
   Literal result: a Bulletin 17C Coyner River fit (1951-2025 peaks, weighted skew), carried to Durrow by the drainage-area ratio (85.3 / 86.4), with the instantaneous peaks (not the daily file or the partial-duration file) as the series. I computed no figures. The literal text says nothing on how to carry the record when mean elevations and precipitation differ (6350 ft against 1870 ft).

6. What decides the main answer: a mix. Mostly the filed rule chain (7.4.3 order, 7.4.4 method, 7.4.2 shortest span at or above the design flood) plus a modeling judgment the files only hint at. The sentence "on the climate the records show" and the 7.4.1 phrase "on the climate of the gauged and station records" bind the answer to the observed record, not a projection. The unstated step is whether and how a flood series from a basin at 6350 ft mean elevation transfers to an 1870 ft basin (rain versus snow regime). That is what the elevation-bands sheet, the SNOTEL files, the Durrow Ridge and Tessel stations and the LCD hourly file (about 90 MB, the large messy one) are for. If the analyst follows 7.4.3(b) literally and carries Coyner by area ratio, the rule-following path ends in a defined answer. Whether that path is wrong depends on the author's intent. Risk for the author: a reader can tell the intended trap is "nearest long-record gauge is climatically unlike the site" only by noticing the xlsx elevation columns. That is data discovery, not a filed sentence, which is what the one-fact test wants. The weak point is the other direction: 7.4.3 is written as a precedence procedure. If the golden departs from 7.4.3(b), a literal judge could call the golden non-literal; if it follows 7.4.3(b), the stump may collapse to rule application.
   Also: the prompt asks for water years of the two largest floods "since 1951" and a 75-year estimated series. That is a reconstruction (regression of site on gauge or climate drivers), which no sentence in any file instructs. That part rests on analytical choice.

## Realism read
- usgs_*.txt peak files: the header block ("# peak_cd: 2 discharge is an estimate; ... # gage_ht in feet above the gage datum ...", "Retrieved 2026-10-14 09:46 PDT") is a paraphrase of the NWIS format, not verbatim. Real NWIS RDB peak files open with "# //" boilerplate lines and carry the 5s/15s/10d/6s/8s/27s/8s width row (present, correct). Real files also carry peak_cd flags (2, 5, 7, A) and gage_ht datum notes; these files have the peak_cd column empty on every row inspected, which is slightly unusual over 60 to 80 years. Retrieval stamps are spread over 09:43 to 09:51 by file, plausible for a manual pull. Blank gage_ht cells on large peaks (1965, 1959) are plausible. Pre-1962 rows have blank peak_tm in Coyner, plausible. Cross-station peak dates line up closely (the same storm dates with hour offsets, for example 1962-12-31, 1972-12-04) across all gauges. That is hydrologically plausible for neighbouring basins but very tidy. The Coyner partial-duration file headnote also says the gage datum "lowered 2.00 ft on 1 October 1985", a nice authentic touch, but not mentioned in the annual peak file.
- Gauge names ("Gorham Creek near Vesper", "Tarrow River near Brandt", "Quillen River at Ashby Falls", "Selby Creek near Hollis", "Pinnell Creek near Coe", "Coyner River near Tessel") are invented, with real-looking 8-digit 121xxxxx IDs near real USGS Skagit-basin ids. Station coordinates (48.3 N, -121.7 W) point to a real region, so the xlsx and the files mix real-looking geography with fictional names; check provenance in metadata.json.
- pelton_county_road_standards_ch7_excerpt.pdf and wsdot_region3_flood_frequency_excerpt.pdf: both are plain LibreOffice-style documents with a footer line. Content is plausible and unusually concise: the county standard is a single paragraph per section and reads as written to carry the task (7.4.3 and 7.4.4 are a tidy decision tree). The WSDOT "excerpt reproduced for project files" is a six-row table with fully consistent equations. A reviewer could say these read as authored for the task rather than excerpted from a real manual. The real WSDOT/USGS Region equations are not of this exact form or Region naming. Both name real-looking resolutions and dates (Resolution 2023-031, 2019 Update). The Hess memo is similarly tidy, with one table per span and a "TM 26-118" footer, dated 21 September 2026 (before the pull dates, fine).
- Spreadsheet: region3_basin_characteristics.xlsx sheet names have a trailing " visible" suffix in the printed state output only because I printed sheet_state; no hidden sheets. Titled as "state flood study 2019, appendix B/C", but it contains an extra 'Durrow Ck at Ransom Bar Rd' sheet made by "Pelton County Public Works, GIS" and an elevation-band sheet that a state appendix would not hold; the mix of sources in one workbook looks assembled.
- CSVs (GHCN-D, LCD, SNOTEL, USGS daily): headers match real exports. Durrow Ridge station elevation is 826.0 m in the GHCN-D file, but the xlsx lists 2710 ft for the same station; 826 m is about 2710 ft, so consistent. Tessel GHCN-D lists 359.7 m, while the xlsx says 1180 ft (359.7 m), consistent. No other realism flags.

### Main thread's rulings on round 4

- Question 1 quotes no sentence naming the decisive step; question 6 reads the donor, the fit and the span rule as the
  filed estimand and the carry between basins of unlike elevation as the unfiled analytical step: as designed (WHAT
  filed, HOW forced by the foothill gauge's own floods).
- The golden keeps 7.4.3(b): it carries the Coyner River's record; the foothill gauge only checks the construction.
- The elevation-band sheet and the assembled workbook: the state study's characteristics with the county's
  delineation and station list, a county working file; harmless.
- The NWIS header, few peak codes, the excerpt line, tidy cross-gauge dates (one storm record, physically synchronous):
  texture, none moves a cell; harmless.

### Round 3

Read: prompt.txt, all three PDFs in full, all six usgs_*.txt files (headers, samples, tails), the workbook (4 sheets, all visible), headers and samples of all CSVs. No figures computed.

1. Decisive step named? No single sentence names the deciding step. The closest procedural text is in pelton_county_road_standards_ch7_excerpt.pdf: 7.4.3 "(a) the record of a gauge at the site where it holds 25 years or more of annual peaks; otherwise (b) the record of the nearest gauged basin holding 25 years or more of annual peaks, carried to the site; (c) the state's regional flood equations only where no gauged basin within 15 miles of the site holds such a record, and only inside the ranges of the equations' explanatory variables." Also 7.4.4 ("log-Pearson Type III ... expected moments algorithm ... Multiple Grubbs-Beck ... station skew weighted with the regional skew") and 7.4.1 ("on the climate of the gauged and station records. No allowance for a future climate"). The prompt's own phrase "on the climate the records show" and "Durrow Creek has never been gauged" hint at the direction; the prompt asks for "the creek's estimated peak flow for each water year from 1951 to 2025" and "the water years of the creek's two largest floods since 1951", which implies transferring a record to the site. Nothing says how to transfer, which gauge, or what to adjust for (e.g. elevation/snow-rain difference in the elevation-band sheet is not commented on anywhere).

2. Ranks or scores the spans on the question? hess_tm_durrow_creek_bridge_span_ratings.pdf gives each span's rated flow (20,500 / 29,000 / 40,000 cfs) and water-surface tables, but no design flow or exceedance. It does not rank against the 1 per cent flow. No file gives a 1 per cent flow for Durrow Creek. The WSDOT regression table gives generic equations only.

3. Files that only help: pelton_county_road_standards_ch7_excerpt.pdf is a procedure/rules document (the 7.4.3 hierarchy and 7.4.4 method order are help, see Q5). wsdot_region3_flood_frequency_excerpt.pdf (regression coefficients, applicability ranges, regional skew -0.12 / MSE 0.13) is reference, and the stated applicability range (drainage area 24.8 to 402 sq mi, precipitation 65 to 112 in) is a purpose-built screen that tells the analyst when the equations do not apply. region3_basin_characteristics.xlsx sheet "Elevation bands" is a purpose-built comparison aid (area by 500 ft band for each gauge and Durrow). The workbook also carries "Distance from the Ransom Bar Rd crossing (mi)" for the five gauges, which directly fixes 7.4.3(b) nearest-gauge selection. No readme or dictionary exists.

4. Figure or name reading as the answer? No answer figure appears. Coyner River (12183450, 6.2 mi, 86.4 sq mi vs Durrow 85.3 sq mi) is plainly the intended donor by distance and area (the only gauge within 15 miles, and it alone has a daily-discharge file and a partial-duration file); this reads as context but effectively names the donor. The Hess memo's note "if the County's design discharge falls between the alternatives' rated flows" is context only.

5. Filed sentence fixing how the main figure is computed / population: 7.4.1 "design flood is the peak flow with a 1 per cent chance ... taken as the instantaneous peak discharge at the bridge, on the climate of the gauged and station records. No allowance for a future climate"; 7.4.3 as quoted above; 7.4.2 "The span selected is the shortest whose rated flow is at least the design flood." Literal result: Durrow (85.3 sq mi) has no gauge, so (a) fails; nearest gauged basin with 25+ years of annual peaks within the workbook is Coyner River (6.2 mi, record 1951-2025), carried to the site; regional equations (c) are out because a gauged basin within 15 miles holds such a record (and Durrow's mean precipitation is not given in the workbook, area 85.3 is in range). Fit LP3/EMA/MGBT with weighted regional skew (-0.12, MSE 0.13). The sentences give the donor and the method order; they do not give the transfer adjustment or the figure.

6. What decides the main answer: mixed. Superficially it is following a stated rule (7.4.3 gauge hierarchy, 7.4.4 Bulletin 17C method, 7.4.2 shortest-span rule). The part that could be analytical is how the Coyner record is carried to a basin whose elevation profile is far lower (Durrow mean elevation 1870 ft, max 4380 ft vs Coyner mean 6350 ft; elevation-band sheet and the SNOTEL/climate-station files point at rain versus snow contributing area), plus the Coyner stage datum change (lowered 2.00 ft on 1 Oct 1985, noted in the partial-duration header) and the historic/estimated peak codes. No file states which of these matters. Nothing in the pack states the transfer method. Risk to flag: the 7.4.3 hierarchy and the Bulletin 17C method sentence are executable procedure (banned kind "rule application") for the donor choice and curve fit; only the transfer judgment is not written down.

Per-file notes on the flagged files:
- usgs_*.txt (six files): contents consistent with real NWIS peak-file layout (comment header, tab header, "5s 15s 10d 6s 8s 27s 8s" format row, "Retrieved 2026-10-14" with different minute stamps 09:43 to 09:49 and 10:06). Site names (Gorham Creek, Coyner River near Tessel, Pinnell Creek near Coe, Tarrow River near Brandt, Quillen River at Ashby Falls) are fictional but the workbook and PDFs use the same names, so consistent. Real-looking mess: blank gage_ht rows, peak_cd 2 on two Coyner rows (1991-02-05, 2003-12-14), missing years, blank times pre-1962. Real NWIS site numbers 12181650 etc. with invented names is the one thing a real reader could catch. Realism concerns: all five gauges share the same storm dates (1965-02-10, 1972-12-04, 1982-11-11, 2023-02-17, 2025-01-02), as expected for a region; however the peaks across sites look strongly proportional (same events, scaled, with 1-3 hour lag per site in times, e.g. Gorham 20:00, Coyner 22:00 / next-day 00:00..., Tarrow 23:00...), which reads as synthetic-from-one-series rather than independent gauges. The peak_cd legend text lists codes 5 and 7 and A although only 2 appears in the rows sampled. The Coyner peaks file lacks 1951-WY header rows that other files have (header says "peak_cd" legend identical across all six, as in real files). The coyner "peaks_above_base" file has a custom header and a "water_year" column that a real USGS partial-duration download does not carry; reads as built. The note "(lowered 2.00 ft on 1 October 1985)" is an unusual sentence for a USGS comment block.
- pelton_county_road_standards_ch7_excerpt.pdf: LibreOffice 24.2 Writer, author "Pelton County Public Works", created 2026-04-07 (revision 6 adopted March 2023, fine). Single page, excerpt wording is crisp and ordered exactly as the task needs (7.4.1 to 7.4.5 maps onto the deliverable list); reads as built for the task rather than a real county code. Contains the method steps.
- wsdot_region3_flood_frequency_excerpt.pdf: LibreOffice-written, CreationDate 2024-05-14 for a 2019 WSDOT/USGS study (anachronism-free but a state report PDF from LibreOffice at 2024 is odd). Real WSDOT/USGS reports are not produced in Writer; "Excerpt reproduced for project files" is a built-sounding line. Table 3 coefficients and the 17-gauge basis are invented but internally consistent; "(precipitation )" header wraps oddly.
- hess_tm (not flagged but read): LibreOffice, 2026-09-21; fine, one page; date after the Retrieved 2026-10-14 pull of the gauge files (memo 21 Sep 2026 predates pulls, no conflict). The "Water surface at the rated flow" column equals low chord minus 2.0 ft exactly for all three spans, and the water-surface table "*" markings follow rated flow: tidy, built to shape.
- prompt.txt: about 800 characters, one paragraph, question first, no persona. States span choice rule ("shortest whose rated flow carries the creek's 1 per cent annual exceedance peak flow on the climate the records show"). It names no method, but "on the climate the records show" and "Durrow Creek has never been gauged" lean toward the transfer/stationarity direction; it also gives the exceedance bins that mirror the standard's 7.4.5 list. Rounding stated at the end.
- Workbook: authored by "Pelton County GIS", created 2026-03-17, modified 2026-03-19, but the first sheet is titled "state flood study 2019, appendix B" and sits in a county GIS workbook: a hybrid of sources in one file. Sheet "Climate stations" lists Ashby Pass SNOTEL 1241 with no matching file (a distractor-like omission) and the Durrow Ridge COOP at 2710 ft; GHCN file shows ELEVATION 826.0 (metres), consistent. Durrow's precipitation is not given in the workbook anywhere visible (Durrow sheet has no mean annual precipitation row).
- CSVs: GHCND, LCD (89 MB, 659k rows) and SNOTEL files are in the real export layouts. ghcnd_tessel has two stations merged (USC00458114 then 458117) which is real. Nothing else read.

### Round 2 (revision 2, the hourly record)

Read: prompt.txt, all three PDFs in full, all six usgs_*.txt peak files (headers plus samples; Coyner peaks and partial-duration file in full or near full), the workbook (4 sheets, all visible), headers/samples of the CSVs. No figures computed.

1. Decisive step stated?
No sentence names the decisive step as such. Nearest hand-overs are procedure sentences:
- Standards 7.4.1: "on the climate of the gauged and station records. No allowance for a future climate is applied on County roads." (settles the climate/stationarity WHAT).
- Standards 7.4.3: "(b) the record of the nearest gauged basin holding 25 years or more of annual peaks, carried to the site; (c) the state's regional flood equations only where no gauged basin within 15 miles of the site holds such a record, and only inside the ranges of the equations' explanatory variables."
- Standards 7.4.4: "Bulletin 17C ... log-Pearson Type III ... expected moments algorithm, ... Multiple Grubbs-Beck test, and the station skew weighted with the regional skew."
- Prompt: "on the climate the records show" and "the creek's estimated peak flow for each water year from 1951 to 2025" (the annual-series file implies transferring a gauge to the creek year by year).
These spell out the frequency method and the source-selection ladder. They do not say how to carry Coyner to Durrow (area, precipitation, orographic/elevation difference, which storms hit), nor that Durrow (mean elev 1870 ft vs Coyner 6350 ft, max 4380 ft vs 10380 ft) is a low, rain-dominated basin versus a snow/high-elevation gauge. The workbook sheet "Elevation bands visible" and the Climate stations sheet point strongly at this, but nothing announces it. Mild pointer only: prompt "on the climate the records show".

2. Does any file already rank or score the three spans on the question?
No. The Hess memo ranks nothing against a design flood; it gives rated flows (22,000 / 28,000 / 40,000 cfs) and says "makes no estimate of flood frequency". It does say "We are glad to re-run the rating if the County's design discharge falls between the alternatives' rated flows". No file gives an exceedance probability per span or a design flow. The regional equations (WSDOT) would give a candidate Q100 only via formula, not a ranking.

3. Files that exist only to help the analyst?
- hess_tm_durrow_creek_bridge_span_ratings.pdf: purpose-built input (rated flows), plausible as a real consultant memo; not a method aid.
- pelton_county_road_standards_ch7_excerpt.pdf: a procedure/method statement written for the task (see 5). Real-looking governing document but it is the main help file.
- wsdot_region3_flood_frequency_excerpt.pdf: regression coefficients and regional skew; supplies the inputs for the procedure.
- region3_basin_characteristics.xlsx: purpose-built comparison aid (basin attributes of the 5 gauges and Durrow side by side, with area-by-elevation bands in sq mi for gauges but acres for Durrow, and a distance column). Closest thing to a comparison aid; no answer in it. Sheet names end in "visible" ("Gauged basins visible" etc.), an oddity, see realism.
- usgs_12183450_coyner_r_peaks_above_base.txt (partial-duration series) and the Coyner daily discharge CSV: look like distractor/extra data, not helpers.
No readme, dictionary or notes file.

4. Figure or name reading as the answer rather than context?
None found. The prompt names the three spans and the thresholds only. Rated flows (22k/28k/40k cfs) are context. The "1 per cent" and "50 per cent" are the standard's. Nothing states a Q100, a chosen span, or the two largest-flood years. Note the 7.4.1/7.4.3 text makes (b), the nearest gauged basin (Coyner, 6.2 mi, 86.4 sq mi vs 85.3, 75-yr record), the evident source, and the 7.4.3(c) 15-mile / variable-range language makes the regional equations look excluded: Durrow's mean precipitation is not in the workbook, and Coyner (86.4 sq mi, precip 79) sits inside the equation ranges, so the equations are a decoy by rule. Gorham (18.9 mi), Tarrow, Quillen, Pinnell are beyond 15 mi.

5. Filed sentences that fix how the main figure is computed or over which population
- 7.4.3 (quoted above): literal result is rung (b): the nearest gauged basin with 25+ annual peaks, "carried to the site". Coyner River (6.2 mi, record 1951-2025, 75 peaks) is the nearest; 12181650 (18.9 mi) is the next. (a) does not apply, Durrow never gauged (prompt). (c) does not apply as a gauged basin within 15 miles holds such a record.
- 7.4.4: Bulletin 17C LP3 / EMA / MGBT, station skew weighted with regional skew (-0.12, MSE 0.13, Table 4 WSDOT). Literal result: LP3-EMA fit to Coyner annual peaks, with weighted skew.
- 7.4.1: design flood = 1 per cent AEP instantaneous peak, current climate, no future allowance.
- 7.4.2: shortest span whose rated flow is at least the design flood.
- Prompt: report flows to nearest 5,000 cfs.
The literal procedure leaves "carried to the site" undefined in method, which is the open piece the data must settle (the workbook's elevation bands, precipitation, and the climate and SNOTEL files bear on it). I give no figure.

6. What decides the main answer?
Mostly following a stated procedure (7.4.3 ladder, 7.4.4 method, rated-flow table from the Hess memo) plus an analytical choice in how a high, snow-influenced gauge (Coyner, mean elev 6350 ft) is transferred to a low-elevation rain-dominated creek (mean elev 1870 ft). The latter is not stated anywhere and is the only non-rule part; it is supported by the workbook's elevation bands and the climate/SNOTEL files. The ladder and method are spelled out, so a large share of the work is rule application. The 7.4.3 sentence ("carried to the site") and 7.4.1 ("climate of the gauged and station records") are the deciding sentences; the data that makes the decision analytical is the workbook sheet "Elevation bands visible" (band areas) and the two climate-station CSVs. Exceedance of each span's rated flow (the 25 / 100 / 500-year categories) follows from the fitted curve and a threshold in the prompt.
Planted-looking items for the sweep: the gage datum lowered 2.00 ft on 1 Oct 1985 (header of the partial-duration file; gage_ht fall in the annual peaks file after 1985, e.g. Coyner 1986 3250 cfs at 7.38 ft vs 3860 cfs at 9.82 ft in 1984), the missing water years in the annual list (1951 is in the partial-duration series but 1950-11-12 appears as the 1951 peak, 1956 and 1957 handled by the dates), peak_cd 2 on two Coyner rows (1991, 2003), the 2001 Gorham peak 8600 and others with blank gage_ht, the 2022 water year missing from all annual files (Coyner jumps 2021-12-21 to 2023-02-17 and a 2023-11-15 peak that is WY2024). None of these is announced by a filed sentence.

## Flagged files, read in full
- Six usgs_*.txt: formatting consistent with NWIS peak output (header lines, "5s 15s 10d 6s 8s 27s 8s" format row, tab separated). Gorham 12181650 and Pinnell have 63 and 58 peaks, Tarrow 70, Quillen 75, Coyner 75. peak_cd column used only twice (Coyner, code 2). No peak_cd 7 or A historic markers anywhere though the legend lists them. Retrieval stamps (2026-10-14 09:41 to 10:06 PDT) are 1 to 3 minutes apart per file, plausible for a person pulling six files, but all six files have the same shape (5s/15s/10d format row, identical header text) which a real download would also have. Coyner daily and partial-duration files (09:41, 10:06) fit. Gage-height column blank for several rows of Tarrow and Quillen, plausible. Peak-date coincidences across stations (same storm dates 1965-02-10, 1972-12-04, 1982-11-11, 2011-03-27 in all five gauges, with timing offsets of a few hours) are real-looking but very uniform. Coyner peak list has no 1988-04-09 as WY max issue... fine. One realism flag: Coyner peak times are blank before 1962 and the datum change in 1985 is documented only in the partial-duration file, not in the annual peaks file. The Coyner annual file lists 75 peaks for 1950-2025 (WY1951-2025 = 75 years), no gaps despite the partial-duration file's WY1956/1957/1960 mapping oddities: the annual file shows 1950-11-12 as WY1951 and 1952-02-24 as WY1952, consistent. Missing WY2022 in Coyner annual list is not a gap in the count only if 1991/94 etc. fill; counts alone I did not verify, and I did not recompute.
- pelton_county_road_standards_ch7_excerpt.pdf: reads like an authored task document. Section 7.4.3's ordered (a), (b), (c) ladder and "carried to the site" is written to exactly the shape this task needs; 7.4.4 names the full method. Metadata: Creator "Writer", Producer "LibreOffice 24.2", creation 7 Apr 2026, one page. A county standards manual normally comes from Word/InDesign. Its text pins method and source, which leaks the field's textbook procedure (the opponent's first move) rather than the deep step. Real county standards do cite Bulletin 17C, so the content is plausible, but the clause numbering and the specificity ("potentially influential low floods ... Multiple Grubbs-Beck") reads authored.
- wsdot_region3_flood_frequency_excerpt.pdf: realistic in content (QT = a A^b P^c, SEP, regional skew, equivalent record length). Table 3 coefficients are monotone smooth in a, b, c; the report is "WA-RD 891.2" with a "2019 Update" but CreationDate is 14 May 2024 and Producer LibreOffice 24.2 (an agency PDF would not come from LibreOffice 24.2 Writer; LibreOffice 24.2 was released Feb 2024, so date and version are consistent, but all three PDFs share the identical Creator/Producer, CreationDate times to the minute pattern "xx:00"). Explicit validity ranges (24.8 to 402 sq mi, 65 to 112 in) built to include or exclude the sites. Excerpt "reproduced for project files" is an authored caveat. Table 3 coefficient columns break across lines ("(precipitation )") because of narrow layout, a LibreOffice artefact.
- prompt.txt: one paragraph, about 800 characters, question first, no persona. It names the deliverables, the flood probabilities, the four exceedance-category bins, the year range 1951 to 2025 and rounding. It does not name the method. "on the climate the records show" is the only hint, echoing 7.4.1. It does say "Durrow Creek has never been gauged", which is written (b) route in effect. The sentence "the shortest whose rated flow carries the creek's 1 per cent annual exceedance peak flow" restates 7.4.2.

## Realism read
- PDFs: all three share Creator "Writer", Producer "LibreOffice 24.2", all stamped on-the-minute (22:47:00, 17:12:00, 16:00:00 UTC) and none carries a trailing real-document toolchain (no Word/InDesign/Acrobat). Hess memo is dated 21 Sep 2026 (before pull dates in Oct 2026, ok) but its creation time 22:47 UTC vs the memo's single-page layout is fine. All three are one-page with the same "Page 1" footer style and the same plain table layout. Reads as authored, not exported from the claimed agencies. WSDOT report "WA-RD 891.2" is a fabricated-looking report number; the county ch.7 and Hess memo are fictional entities, expected for a fictional county, but the WSDOT/USGS names are real organizations used in fabricated documents.
- Hess memo Table 1 ("Water surface at the rated flow" column) and Table 2 are mutually consistent and use clean 4,000 cfs steps with asterisks, a pack-built rating, uniform shapes. Table 2 values smooth; no free-text noise.
- region3_basin_characteristics.xlsx: Application "Microsoft Excel", creator "Pelton County GIS", created 2026-03-17, modified 2026-03-19; every internal zip entry stamped 2026-03-19 16:04 (consistent with openpyxl-style writing, no sheet-level history). Sheet names carry the suffix " visible" ("Gauged basins visible", "Durrow Ck at Ransom Bar Rd visible", "Elevation bands visible", "Climate stations visible"), an odd name for a GIS export and a possible reference to hidden-sheet handling; all four are visible. Durrow's band areas are in acres while gauges are sq mi, an inconsistency that reads as built to force a unit conversion. The title cell says "state flood study 2019, appendix B", yet the Climate sheet lists SNOTEL 1241 Ashby Pass (1985-) and Tessel 3 E, none matching a CSV supplied (no Ashby Pass or Brandt 4 W, Vesper 1 S, Tessel 3 E data), which makes those distractor rows. Durrow Ridge elevation is 826.0 (metres) in GHCN against 2710 ft in the workbook (consistent, 826 m = 2710 ft).
- CSVs: GHCND files carry real attribute strings (",,7,1700") and the Tessel file mixes DAPR/MDPR (accumulation) rows, authentic mess. The Durrow Ridge file is a different column set with no DAPR/MDPR (authentic since different stations). LCD hourly (89.8 MB, 659k rows) has regular :53 times and report type FM-15; a 1950 LCD with SOURCE 4 hourly airport reports is plausible but real hourly data in 1950 are sparser; uniform hour grid from 1950-10-01 looks regular. SNOTEL files carry the genuine NRCS warning header; Hatchet Meadow elevation 4160 ft there equals the workbook. Coyner daily CSV qualifiers column "A" on the first rows, fine.
- Retrieval stamps for six usgs files are 09:41 to 10:06 PDT on the same morning, plausible.
- Metadata scrub: nothing in the PDFs named a task, trap or build tool beyond "LibreOffice 24.2"/"Writer".

### Round 1 (the daily-temperature carry)

1. Decisive step named? No single sentence names it. The nearest procedural text is Pelton standards 7.4.3: "(b) the record of the nearest gauged basin holding 25 years or more of annual peaks, carried to the site", and 7.4.1: "on the climate of the gauged and station records". Nothing says how to carry a record, what to do about climate trend, or what to do with the SNOTEL, GHCN or daily-discharge files. The prompt's "on the climate the records show" is the only pointer toward a record-based adjustment, and it names no method.

2. Ranking or scoring of the three spans on the question: none. The Hess memo (hess_tm_durrow_creek_bridge_span_ratings.pdf) gives rated flows (22,500 / 33,500 / 46,000 cfs) and a stage table, but never compares them with a design flow; it says "makes no estimate of flood frequency". No file gives a design flow for Durrow Creek.

3. Files that only help the analyst: none is a readme/dictionary/manifest. Closest: region3_basin_characteristics.xlsx (sheet "Elevation bands", a Coyner-vs-Durrow area-by-elevation table, reads as a purpose-built comparison aid), and the three PDFs as governing/context documents (county standards, WSDOT regional equations excerpt, Hess rating memo).

4. Figure or name reading as the answer: the Hess memo's rated flows (22,500; 33,500; 46,000 cfs) and low chords are context for the final comparison, not an answer by themselves. The workbook's Durrow drainage area 85.3 sq mi next to Coyner 86.4 sq mi (nearest gauge, 6.2 mi) points strongly at Coyner as the donor; this is a near-answer to "which gauge", though arguably expected context. The elevation-band sheet showing Durrow's basin topping out at 4,380 ft against Coyner's 10,380 ft reads as a deliberately highlighted contrast. WSDOT 4.2 range "drainage area 24.8 to 402 square miles, mean annual precipitation 65 to 112 inches" together with the Durrow basin (85.3 sq mi) and no Durrow precipitation figure filed makes the regression route's applicability depend on a number the pack does not state.

5. Filed sentences fixing the computation/population:
- 7.4.3 (b): "the record of the nearest gauged basin holding 25 years or more of annual peaks, carried to the site". Literal result: use the nearest gauge with at least 25 annual peaks (workbook distance column: Coyner River, 6.2 mi), and transfer its flows to Durrow. The transfer method is not given.
- 7.4.3 (c): regional equations "only where no gauged basin within 15 miles of the site holds such a record, and only inside the ranges" . Literal result: with Coyner at 6.2 mi, equations are not used.
- 7.4.4: "log-Pearson Type III ... expected moments algorithm, potentially influential low floods identified by the Multiple Grubbs-Beck test, and the station skew weighted with the regional skew". Literal result: Bulletin 17C fit with EMA and MGBT, skew weighted with -0.12 (MSE 0.13) from the WSDOT excerpt.
- 7.4.1: "taken as the instantaneous peak discharge ... on the climate of the gauged and station records. No allowance for a future climate". Literal result: no climate projection; flows for the observed-record climate.
- 7.4.2: "The span selected is the shortest whose rated flow is at least the design flood." Literal result: compare 1 per cent flow with 22,500 / 33,500 / 46,000.

6. What decides the main answer: a mix. Choosing the donor and following 7.4.3/7.4.4 is rule application and is spelled out. Beyond that, the pack (Coyner peaks files with gage-datum note, two estimated peaks, a partial-duration file, daily flows, two SNOTEL sites, two GHCN stations, a Coyner-vs-Durrow elevation-band table, "on the climate the records show") invites an analytical judgment about how the donor's record relates to Durrow's contrasting elevation and the record's stationarity. No filed sentence states that judgment; the deciding text is the prompt phrase "on the climate the records show" plus the elevation-band sheet. Nothing reads as a planted-defect catch alone, though the dated datum note ("lowered 2.00 ft on 1 October 1985") and the estimated-peak codes are catchable details.

## Realism read
- PDFs: all three list Producer "LibreOffice 24.2" and Creator "Writer", a toolchain signature; the WSDOT report (2019) and county standards (2023) carry CreationDate 2019 and 2023 but the same LibreOffice 24.2 (released 2024) producer, which postdates both creation dates. Also the WSDOT and county PDFs look like short typeset excerpts, not scans of real publications.
- Hess memo is dated 21 September 2026 but PDF CreationDate is 18 Sep 2026 (minor); gauge files "Retrieved 2026-10-14" postdate it, which is fine.
- usgs_12183450_coyner_r_annual_peaks.txt: the comment says "water years 1991 and 2008: the gage house was damaged in the flood" but the codes sit on 1991-02-05 (4560) and 2008-01-29 (10500), with ordinary-sized flows; and real NWIS files wouldn't carry that free-text comment line.
- The five annual-peak files share synchronous storm dates (1965-02-10, 1972-12-04, 1982-11-11, etc.) with plausible hydrology but also blank or missing gage_ht in odd rows and 5-line identical headers; the header "Retrieved 2026-10-14 09:41 PDT" is identical across all seven USGS files (to the minute), unusual for separate real downloads.
- Pack site names (Durrow, Coyner, Tessel, Hatchet Meadow, Corbel Ridge) are fictional but station IDs are real-format; the xlsx creator is "Pelton County GIS" with no toolchain name.
- GHCN files: Tessel file has DAPR/MDPR columns and a different layout from Durrow Ridge, plausible real drift.

### Main thread's rulings on the round 2 read

- Question 1: no sentence names the decisive step; question 6: the transfer is the analytical piece and the filed text
  fixes the estimand around it, as designed (the WHAT filed, the HOW open and forced by the records).
- The workbook as a comparison aid: it is the state study's basin characteristics with the county's delineation and
  station list; it now carries every gauged basin's bands in one unit; harmless.
- Realism fixed in the generator: the PDF export stamps carry seconds; the creek's bands are in square miles like the
  county's own sheet; the workbook is rewritten in Excel's dialect (shared strings, 1980 entry stamps); each zip entry
  carries its file's own save; the hourly reports sit at 56 minutes past before the automated station and 53 after;
  the state report carries no report number from a real series.
- Stations in the workbook's list with no file in the pack (Brandt 4 W, Vesper 1 S, Ashby Pass): the state study's
  network is wider than the county's downloads; Tessel 3 E is in the valley file; harmless.
- The estimated peaks, the datum note and blank gage heights: texture that moves no graded cell (SF14); harmless.
