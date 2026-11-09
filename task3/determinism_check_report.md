# Determinism check, task3 (architecture 6)

Each round ran one isolated judge thread (Sonnet, medium effort) that saw only prompt.txt, target/ and the graded blocks, wrote its derivation before opening the blocks, and filed the verdict below verbatim. The main thread's disposition follows each round.

## Round 4 (option 2, the foothill gauge, target.zip d36f2053): the final cut

Order kept: derivation.md was written before graded_blocks.md was opened (yes).

- **Verdict:** DETERMINISTIC
- **Disposition:** APPROVE (no rerun). Advisory only: the report's 1 per cent flow sits about 1,000 cfs above a rounding edge (see Evidence), so a rubric tolerance of one rounding step on supplementary 3 and on the CSV is prudent; no pack change needed.
- **Why:** The span is forced by the standard's own rule (7.4.3(b): Coyner R, 6.2 mi, 75 yr, is the nearest qualifying gauge; Selby Ck's 14 yr and the regional equations, with Durrow's mean annual precipitation of about 60 in outside the 65 to 112 in range, are barred) plus a transposition that the shipped stations and Selby's 14 peaks validate or refute. Every transposition that is unbiased against Selby (median error within about +-10 per cent) lands Q100 between roughly 21k and 27.5k, which is above 20,500 and below 29,000, so 185 ft; the area-ratio transfer (18.7k, 140 ft) is biased -26 per cent on Selby and the standard-atmosphere lapse (about 30k to 35k, 240 ft) is biased +29 to +47 per cent. The two largest floods (WY2008, WY2011) did not change in any variant I ran.

## Evidence (recomputed from target/)
| Item | Golden | Mine | Source |
|---|---|---|---|
| Coyner 75-peak B17C Q100 (weighted skew -0.159) | 18,900 | 18,860 (MoM) / 18,835 to 19,146 (EMA, censoring 2,000 to 3,000) | usgs_12183450 annual peaks, WSDOT excerpt Table 4 |
| Area-ratio carry | 18,700 | 18,700 | workbook areas 85.3 / 86.4 |
| Coyner rain share of area at the floods | median 50% | median 50.1% | hourly Tessel + elevation bands |
| Storm lapse rate | 5.36 C/km | 5.31 mean, 5.36 median (2,083 days >= 0.5 in at both) | two GHCND files |
| Precip rise with elevation | ~10% / 1,000 ft | Durrow Ridge / Tessel on warm storm days 1.15 over 1,550 ft | same |
| Selby out-of-sample, golden construction | +5% median | -0.4% median, median abs log error 0.107 | usgs_12186050 |
| Selby, rivals | -26 / +47 / +37 | std atm +29%, no rise +19%, tsnow 2 C +20% | my replication |
| Durrow Q50 / Q100 (flood-by-flood carry, EMA, WY1997 below threshold) | 10,000 / 25,000 | 8.8k / 23.5k (21k to 27.5k across validated parameter ranges) | rounds to 10,000 / 25,000 |
| Two largest WYs | 2008, 2011 | 2008, 2011 in all 8 variants | |
| Exceedance classes | 10-100 / 100-1,000 / >1,000 | 20,500 ~ Q50 (10-100); 29,000 near Q500 (100-1,000); 40,000 beyond Q1000 | |

Forks tested: (F1) "carried to the site" is unfiled; the area-ratio reading gives 140 ft but is refuted by Selby (named data) and by the elevation bands. (F2) MOVE.1 extension of Selby (18.3k, 140 ft) is excluded by the filed 25-year rule in 7.4.3; it is not the nearest qualifying basin. (F3) Storm window, dry-spell, EMA censoring threshold: Q100 moves 23.4k to 23.6k, no change of bin. (F4) Parameter choices inside the data-supported band (rise 0.05 to 0.15, lapse 5.36 to 5.7): Q100 20.6k to 24.5k, always 185 ft, but at rise 0.15 the rounded 1 per cent flow would read 20,000 (that variant is -8% to Selby's floods vs. -0.4% for the golden; separable by the named gauge). (F5) Regional equations: out of range by MAP, so 7.4.3(c) is closed. Data caveat: the Tessel hourly file has multi-day gaps (e.g. 1969-02-10); events inside gaps need the COOP files, and this did not alter the top-two ranking.

SOLUTION_WRONG: none found. Not exactly reproducible to 100 cfs for the CSV (unfiled flood-by-flood details), so that file should be graded with tolerance and on the two largest values and the 1997 "<" qualifier.

## Files/Hygiene
PASS. 17 files: CSV (5), TXT (6 USGS peak files), PDF (3), XLSX (1), formats span tabular, text, PDF, workbook. Real-looking NWIS, GHCN, LCD and SNOTEL layouts with gaps, partial duration series, datum change note, blank gage heights. Distractors present and unused (Gorham, Pinnell, Tarrow, Quillen peaks, SNOTEL pair for the lapse check is used). Constant exact 3.14 F per 1000 ft offsets between Tessel and both SNOTEL stations suggest the weather is derived rather than raw; I flag this as a possible provenance tell, not exclusion-level. No authoring disclosures seen in the PDFs. Temporal: retrieved dates 2026-10, memo 21 Sept 2026, consistent.

## Stump power
Good. The reflexive route, B17C on the named nearest gauge carried by drainage area (18.7k, 140 ft), is the textbook method the standard seems to ask for, and it is wrong by a physical reason (a high snow basin carried to a low rain basin). A run that notices the elevation mismatch still has to build the snow line from station data, calibrate lapse, rain-snow temperature and precipitation rise, and validate on a gauge the standard bars from design; a wrong lapse (6.5 C/km) or a missing precipitation rise sends it to 240 ft. Plausible partial failures are many, so both runs losing for analytical reasons is likely.

## Stumping type
`mechanism: method_or_model_selection` (transposition of a gauged record to an ungauged basin validated out of sample), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported inputs (Coyner peaks, rated flows) are all correct; the difficulty is which transfer is right, decided by the short gauge, not by catching a bad number.

## Deep reasoning
`domain: pass`, `layers: pass`, `decisive_step: analytical`, `chain: 5 inferences, judgment: transposition model chosen and validated out of sample against Selby (heterogeneity a pooled area-ratio transfer hides)`, `one_fact: none that makes it routine; the nearest sentence is "Coyner's floods are rain on snow, so carry them by the share of area below the snow line", which still leaves the lapse, rain-snow temperature, precipitation rise, event rain definition and validation to be built`.
Layer 1: gaps in the hourly airport file, PDS versus annual peak files, two COOP stations, datum change, provisional codes. Layer 2: hydrologic transposition by rain-contributing area and B17C on the carried series. Swap test: change the nouns to any non-hydrologic field and it stops making sense. Easy route: area-ratio carry, Q100 18.7k, 140 ft.

## Fix
none. Optional (solution/rubric): allow one-bin tolerance on the 1 per cent flow and on CSV values, since the unrounded Q100 (about 23.5k in my replication) is only about 1,000 cfs above the 22,500 rounding edge.

**Disposition (main thread):** DETERMINISTIC, shipped READY. The advisory (the 1 per cent cell about 1,000 cfs from its edge in the judge's replication, 2,300 in the golden's) is a rubric-tolerance note; the call and the bands carry the margin. The CSV's 100 cfs values are not graded one by one (the Supplementary answer describes its rows, columns, the censored year and its two largest values).

## Round 3 (revision 2, target.zip ac2f39bf)

# Verdict, task3 (Durrow Creek bridge span)

Order kept: derivation.md was written before graded_blocks.md was opened.

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK. The carry from the Coyner River to the creek has to be pinned or made recoverable by one method the data forces (or the spans' rated flows moved away from the sensitive range), then new runs are required.
- **Why:** 7.4.3(b) says only that the nearest gauged basin's record is "carried to the site"; no shipped text says how. The golden uses an unfiled stack: Tessel Field hourly rain-weighted temperature, a 36-hour/6-hour wet-spell definition, a storm lapse rate of 5.4 C/km from days with 0.5 in or more on both gauges, a rain-snow temperature of 0.9 C from SNOTEL, and a 10 per cent per 1,000 ft precipitation rise. The 1 per cent flow it lands on (about 25,000 cfs) sits between two rated flows (20,500 and 29,000) and moves across the 29,000 line under single reasonable changes to those choices. Affects the main recommendation, supplementary answers 3 to 7 and the CSV (answer 8). Gates C and E fail. Taxonomy: margin_or_boundary_fragility (decisive quantity has several valid estimation routes whose range straddles the deciding line), with underspecified_objective in the carry rule.
- **Evidence:**
  - Reproduced: Coyner 75 annual peaks (annual_peaks.txt) give an LP3 fit with weighted skew of about -0.16 and Q1% of about 18,860 cfs (golden 18,900); area transfer (85.3 / 86.4) gives about 18,700 (reproduces). Rated flows 20,500 / 29,000 / 40,000 trace to the Hess memo Table 1. Regional equations are barred by 7.4.3(c) because Coyner is 6.2 mi away (reproduces); Durrow Ridge annual rain of about 62 in is also under the equations' 65 in floor.
  - Minor: the golden says the creek's mean elevation is 1,860 ft; the workbook says 1,870 ft.
  - Not reproduced as forced: my own event-by-event carry using Tessel daily station temperatures (precipitation-weighted over the two days to the peak), the elevation bands, a 0.9 C snow line and the PDS list gave Q1% of about 30,000 (5.0 C/km, 10 per cent gradient) to 41,000 (5.4 C/km) and 55,000 (6.5 C/km, no gradient), and about 36,000 to 41,000 at 5.8 to 6.0 C/km. That is the 240 ft span for any defensible daily-temperature reading. The golden itself says the standard atmosphere's 6.5 C/km gives about 35,000 and counting rain without its rise with elevation gives about 30,000; both are above 29,000. The station pair's own lapse rate differs by method (3.0 F per 1,000 ft Tessel to Durrow Ridge, all days or winter, is 5.5 C/km; Durrow Ridge to Hatchet Meadow is 6.2 C/km; Hatchet to Corbel 5.7 C/km), so a run that takes the SNOTEL pair or a mean lapse rate crosses the 29,000 line.
  - Fork table: area transfer, 18,700, 140 ft; hourly rain-weighted snow line with storm lapse, 25,000, 185 ft; daily temperature or standard/pair lapse rate, 30,000 to 40,000+, 240 ft; precipitation-exponent transfer using Durrow Ridge rain, about 14,000, 140 ft. No shipped sentence selects among them; the hourly-record choice is argued only in the golden.
  - Two largest floods: golden says WY2008 and WY2011. Under my daily-temperature carry the top annual maxima were WY2008, 1973 and 1999 (2011 was not second); under area transfer they are WY1983 and 2001. The ranking and the 75 CSV values follow the carry choices, so CSV values to 100 cfs are not forced.
  - Exceedance bands: with Q1% near 25,000, the 140 ft (20,500) band "10 to 100 years" and 185 ft "100 to 1,000" follow the golden's curve only; they change with the fork.
- **Files/Hygiene:** PASS with caveats. 15 files; formats: CSV (6), TXT (6), PDF (3), XLSX (1); real-looking USGS NWIS, NOAA GHCN-D, LCD and SNOTEL exports with mess (duplicate Tessel rows from two co-located stations in 1988, 1950-78 precipitation gaps, ice and estimate codes). No authoring disclosure found. The Hess memo and county standards are in-fiction documents (dated September 2026 against files retrieved October 2026, a small temporal oddity: the memo predates the data pull). The workbook ships a Climate stations sheet that notes Tessel station moves, which is useful context. No exclusion-level finding.
- **Stump power:** The intended trap is real: the Coyner basin is high and snow-covered, and the creek is low and drains rain; a strong model that carries by area gets 140 ft. But the correct answer rides on an unfiled elaborate calibration, and models that go as far as the snow-line idea are likely to land on 240 ft (daily temperatures, standard lapse) or on 185 ft by luck, so failure is not cleanly analytical. Lever: file the carry (for example a filed rain-contributing-area rule with its snow-line temperature and lapse rate stated as the county's drainage-manual values) or move the rated flows so the answer is robust across the lapse-rate range.
- **Stumping type:** `mechanism: method_or_model_selection`, `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported Coyner numbers are fine; the difficulty is a transfer-model judgment on honest data, which is the wanted shape, but it is under-pinned.
- **Deep reasoning:** `domain: pass` (hydrology: flood frequency, regionalisation, rain-on-snow contributing area), `layers: pass`, `decisive_step: analytical`, `chain: 5 inferences, judgment: transfer of a high snow-dominated basin's flood record to a low rain-dominated basin by event-wise contributing area, with the snow-line temperature and lapse rate justified from station data`, `one_fact: none that fully rescues, though "use the storm snow line at the rain-weighted hourly temperature and the storm-day lapse rate" would make it routine`. The easy route is the drainage-area transfer of the Coyner LP3 curve (Q1% about 18,700, 140 ft); the golden's route gives about 25,000 and 185 ft.
- **Fix:** prompt and input_files. File the carry rule and its parameters in a shipped document, or restructure so the 1 per cent flow sits well inside one span's band under every defensible lapse rate, rain-snow temperature and precipitation gradient; then rebuild the CSV and top-two-flood answers from the pinned rule.

**Disposition (main thread):** repaired by option 2 (round 4). Three isolated judges each built the snow-line carry a different defensible way (daily temperatures, other lapse sets) and two of three filed spans other than the golden's; the carry is an open physical model whose result the files do not force at the span's margin. Paused for the author's decision between filing the carry, adding an observed low-basin record, or re-rooting.

## Round 2 (revision 2 as first cut, target.zip 4ff37442)

Order kept: derivation.md was written before graded_blocks.md was opened (yes). Scripts are under work/.

- **Verdict:** NOT_DETERMINISTIC (margin_or_boundary_fragility)
- **Disposition:** SEND_BACK. Pin the snow-line inputs (lapse-rate estimator and statistic, rain-snow temperature, storm/temperature definition) in the files or widen the margin between the creek's 1 per cent flow and the 22,000 cfs rating; this changes what solvers see, so a rerun is required.
- **Why:** The mechanism is real and found in the files (flood-time snow line, contributing area from the elevation-band sheet), and the golden's Coyner steps reproduce. But the span call (185, not 140) rests on a creek Q1 of about 22 to 26 thousand cfs set against a 22,000 cfs rating, and Q1 moves across that line under valid, data-supported estimators of the snow-line inputs that the files and prompt never pin. Affects the main recommendation, supplementary answers 3 to 6 (and the 25,000 rounding at the 5,000 step).

## Evidence (recomputed)
| Item | Result |
|---|---|
| Coyner B17C (75 peaks, skew -0.183, MSE 0.080, weighted -0.159) | Q1 18,860 (golden 18,900 ok), Q50 5,800 |
| Area-ratio carry | 18,650 -> 140 ft (the rejected route) ok |
| Median Coyner rain-share across floods (lapse 5.36, rain-snow 0.9 C, airport 353.6 m, 36 h wet run) | 50 per cent, reproduces golden |
| Lapse, Tessel 2 NE vs Durrow Ridge, days both >= 0.5 in, (tmax+tmin)/2: | median 5.36 (golden), mean 5.07 (n=2,089); tmax median 4.77, mean 5.08; tobs mean 5.03, median 4.77 |
| My replication, lapse 5.36, rs 0.9, 10%/1000 ft, b 0.856 | Q50 ~9,100; Q4% 18,600; Q1 23,750; Q0.2% 30,100; top two WY2008, 2011 (golden 10,000 / 25,000, same top two, so my pipeline sits ~5 per cent below the golden's) |
| Same, lapse 5.07 | Q1 21,860 (below the 22,000 rating: 140 ft would carry), Q0.2% 27,760 |
| Same, lapse 5.21/rs 0.89 (SNOTEL pair) | Q1 22,730; lapse 5.0 -> 21,400; rs 0.5 -> 22,300; rs 1.5 -> 26,300; lapse 5.8 -> 26,750 |
| Storm window 12-48 h, gap 3-12 h | Q1 ~23,750 (24-hr ... robust); 12 h window 24,800; hour-of-peak temperature instead of rain-weighted: 26,500 to 28,900 (straddles the 28,000 rating) |
| Standard 6.5 C/km | Q1 ~31,900 (240 ft); golden says ~35,000 (outside the data-measured lapse range, so properly ruled out) |

Competing answers: (a) 140 ft survives if the lapse is estimated as a mean (5.0 to 5.1) rather than the median 5.36 (Q1 21.4 to 21.9k vs 22,000). (b) 240 ft survives if temperature is taken at the peak hour (Q1 up to 28.9k) or lapse 5.8. Golden's 185 ft sits between, but with only about 8 per cent margin on the 22k side in my replication and the estimator choice is unpinned. Q1 reported to the nearest 5,000 is 20,000, 25,000 or 30,000 under these variants; the bins for the 140 and 185 ft spans (25-100 vs 100-500 vs >500 years) flip with them. Annual peaks series to 100 cfs cannot be unique across these estimators.
Robust: WY2008 and WY2011 as the two largest (about 1 per cent apart, both stay top two in most variants), Q50 = 10,000, the 240 ft span's >500 year bin, the rejection of the area transfer and of regression (barred by 7.4.3(c): Coyner within 15 mi).
Gate A: pass for Coyner values; the creek's Q1 reproduces only to about 5 per cent. Gate B: all inputs are in files (lapse from the two GHCN files, rain-snow temperature from SNOTEL, elevation bands). Gate E: prompt pins the question and the climate ("records show", 7.4.1) but not the carry method, which is allowed; the unpinned items above are estimation choices, not method.

## Files/Hygiene
PASS with notes. 16 files: csv x7 (incl. 89.8 MB hourly LCD, two 27k-row GHCN files), txt x6 (USGS peak files), pdf x3, xlsx x1. Real-source-looking USGS/NOAA/NRCS files with realistic mess (blank gage heights, estimate codes, quality flags, missing months at Durrow Ridge 1969/1984/2003, datum change 1985 noted). Distractors present (Gorham, Pinnell, Tarrow, Quillen peaks, daily discharge, climate-station sheet). The PDS file and elevation sheet carry the stump. No authoring disclosures seen. Place names are fictionalised variants of real data; no exclusion-level finding.

## Stump power
High and for a real reason: the area-ratio transfer (18.7k, 140 ft) and the state equation (~20k, 140 ft) are the reflex routes and both fail. The creek's flood-by-flood contributing-area carry is a genuine multi-step modelling task, so a strong model plausibly falls to 140 ft. The weakness is determinism of the margin, not stump power.

## Stumping type
mechanism: forecasting-free modelling transfer (method_or_model_selection, event-based regionalisation); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. No reported number is wrong; the difficulty is the correct transfer estimand and snow-line estimation. Passes Gate G.

## Deep reasoning
`domain: pass` (hydrology: regionalised flood frequency, rain-on-snow contributing area), `layers: pass` (L1: mixed gauges/stations/hourly 1950-2025, datum change, gaps; L2: event-level contributing-area transfer then B17C), `decisive_step: analytical`, `chain: 5 inferences, judgment: matching the transfer to the storm's rain-below-snow-line contributing area (estimating lapse, rain-snow temperature, precipitation gradient from the data)`, `one_fact: none` (told "the creek drains more of each storm", the solver still must estimate the snow line and rebuild the flood series). Easy route: area-ratio carry or regression gives ~18.7-20k and the 140 ft span.

## Fix
Location: input_files and prompt. Either (1) widen the margin so the call survives lapse 4.8 to 5.4 and rain-snow 0.5 to 1.5 C (for example move the 140 ft rated flow or the creek's Q1 so Q1 is >= ~10 per cent above 22,000 and >= 10 per cent below 28,000 under every data-supported estimator), or (2) file the estimator (mean vs median, which daily temperature variable, which storm day set) as a stated convention so a literal reader gets one lapse rate. Then rebuild the golden numbers and re-run. If the author's own pipeline shows Q1 at or above ~24,000 even with the mean lapse of 5.07 (mine reproduces the golden's 50 per cent rain share exactly but sits ~5 per cent low on Q1), the margin may hold and this reduces to a FIX_NOW pin of the lapse estimator.

**Disposition (main thread):** reproduced. The lapse spread is one reading of the Tessel record at a single elevation across the 1988 move (every statistic and temperature variable gives 5.32 to 5.39 with each station at its own elevation); the move is now 35 ft (SF12). The peak-hour temperature is not the rain's (SF22) and the Step-by-Step says so. Spans re-rated 20,500 / 29,000 / 40,000 cfs; bands at decades; regional gauges' unit floods aligned with the Coyner River's. Re-judged in round 3.

## Round 1 (the daily-temperature carry, target.zip 7e873e87)

Order kept: derivation.md was written to disk before graded_blocks.md was opened.

- **Verdict:** NOT_DETERMINISTIC
- **Disposition:** SEND_BACK. The golden's 185 ft call rests on a bespoke flood-by-flood snow-line transfer that no shipped file prescribes and that spans all three answers under reasonable parameter choices; the pack and prompt must pin the carry (or make the data force one parameterisation) and the runs must be redone.
- **Why:** The literal text (prompt, County 7.4.3(b), 7.4.4) gives: nearest gauged basin with 25+ years = Coyner (6.2 mi), Bulletin 17C curve, "carried to the site". The only transfer any file names is basin size (area 85.3 vs 86.4 sq mi; regression exponent 0.856), giving Q100 about 18,700 to 19,000 cfs and the 140 ft span (22,500 cfs). The golden instead builds a model (snow line from the Tessel temperature on the storm's wettest day, storm lapse rate, rain-snow temperature from SNOTEL, 10 per cent per 1,000 ft precipitation gradient, band-wise rain volumes, annual maximum of carried floods) to reach 27,000 cfs and 185 ft. Each of those inputs is a free analyst choice, the standard says nothing of the method, and reasonable alternatives land on every span. Gates C and E fail (main call and supplementary asks 2 to 7); taxonomy label: underspecified_objective (method of carry), with margin_or_boundary_fragility and answer_contradicts_files (literal 7.4.3(b) plus the only filed transfer gives 140 ft).

## Evidence

Recomputed and reproduced from the pack:
- Coyner 75 annual peaks (usgs_12183450_coyner_r_annual_peaks.txt, WY1951-2025, no gaps): log10 mean 3.7576, sd 0.2346, station skew -0.183; weighted with -0.12 (MSE 0.13): Q10 11.3k, Q4 14.3k, Q2 16.6k, Q1 18.9k, Q0.2 24.4k. Matches golden step 1 (18,900). Low-outlier censoring moves Q100 under 2 per cent. No trend in peaks or station precipitation (Kendall p 0.46, 0.20, 0.89).
- Area transfer: 18.7k to 19.0k, 140 ft span. Matches golden's "insufficient" figure (18,700).
- Regression (rejected by 7.4.3 order, and MAP about 58 to 62 is below the 65 in range): 14.1k to 20.3k for MAP 58 to 79, all below 22,500.
- Elevation bands (xlsx) sum to 86.41 sq mi (Coyner) and 85.30 (Durrow), means 6,351 and 1,865 ft: reproduces golden step 3.
- GHCN ELEVATION is in metres (Tessel 359.7, Durrow Ridge 826.0 while the workbook uses feet); the file does not state the unit. With metres, the paired-station difference on days both caught 0.5 in or more gives about 5.1 C/km (golden 5.36 on 2,161 days; I got 2,086 days, not an exact match, and with the elevations read as feet the lapse is 16.6 C/km).
- Rain-fraction medians: my replication of the golden's recipe gives Coyner rain share about 0.48 and carried ratio median 1.64 (golden 0.51 and 1.55): the direction reproduces. The golden's Q100 of 27,000 does NOT reproduce from the recipe as written in the blocks: my literal implementation (Gamma 5.4, rain-snow temperature 0.9 C, 10 per cent per 1,000 ft, wettest-day temperature, annual maximum of carried floods, EMA-free LP3 with weighted skew) gives Q100 about 56,000 cfs (240 ft). The details that separate 27k from 56k (how a flood is carried: ratio of depth-weighted rain volumes versus the ratio of areas, treatment of storms with a small rain share, storm window, which day's temperature) are not stated in the blocks or in any file.
- Sensitivity of my replication (Q100): rain-snow temperature 0 C: 32.7k (185 ft); 0.9 C: 56k (240 ft); 2 C: 40.7k (240 ft); standard-atmosphere lapse 6.5 C/km: 74k; no precipitation gradient: 65k. The golden itself concedes 18,700 (140 ft), 37,900 (240 ft), 33,700 and 29,600 as defensible-looking alternatives. A band running 18.7k to 37.9k straddles both rated-flow lines (22,500 and 33,500); the golden's 27,000 sits only 5,500 cfs above one line and 6,500 below the other, well inside that parameter noise.
- Competing answers that survive from the files: 140 ft (literal 7.4.3(b), area transfer, 18.7k to 19k), 185 ft (golden), 240 ft (steeper snow line or a depth-weighted carry). Supplementary asks 2 to 7 (17,000 / 21,000 / 24,000 / 27,000 / 34,000 cfs, rounded to 1,000) depend on the same unpinned carry and cannot be reproduced to the stated precision by a solver who follows the files; the "about 58 inches" MAP also depends on an unpinned station-to-basin interpolation.
- Fork table: carry by area (18.7k, 140 ft) / carry by rain-below-snow-line with golden parameters (27k, 185 ft) / same with alternate rain-snow temperature or lapse (33k to 75k, 185 or 240 ft).

## Files/Hygiene

PASS in count and mix: 15 files (6 CSV, 5 txt tab-delimited, 3 PDF, 1 xlsx); real-looking USGS, GHCN, SNOTEL formats with realistic mess (duplicated Tessel rows for 1988, 90-day gaps in Durrow Ridge, Tessel DAPR/MDPR accumulations, blank gage heights, estimated peaks). Distractors present and unused: Coyner daily-mean discharge (daily means are 0.4 to 0.9 of instantaneous peaks), the partial-duration series, the four other gauges. The workbook and PDFs read as authored for the task but not offensively so. Temporal coherence fine (retrieved 2026-10-14; memo 21 September 2026). No exclusion-level findings. Note for repair: GHCN station elevation units are not stated anywhere, which matters to the lapse-rate step.

## Stump power

Cannot be credited: a run that follows the filed text (area transfer, 140 ft) and a run that models the snow line differently from the golden both diverge for method-choice reasons, not a single forced analytical error. The mechanism that is supposed to do the work (rain-contributing area differs between a high and a foothill basin) is a real and plausible hydrologic insight, but the magnitude is not pinned by the shipped data to within the 17 per cent and 26 per cent margins around the golden.

## Stumping type

mechanism: method_or_model_selection (a transfer model chosen by the author); stumping_family: analytical_non_defect; surface_read_dependency: no; sole_data_defect: no. Not a banned surface-read flip; the failure is that the model selection is not validated against anything in the pack (no gauge in a low basin exists to calibrate the carry out of sample), so it is not forced.

## Deep reasoning

`domain: pass`, `layers: pass` (layer 1: unit and gauge-file mess; layer 2: transferring a flood record between basins of unlike elevation), `decisive_step: analytical` (as intended, but the transfer is unvalidated), `chain: 5 inferences (Coyner EMA curve, storm matching, snow line, rain-area ratio, refit), judgment: the choice of the transfer model and its parameters, which the data does not adjudicate`, `one_fact: "carry each flood by the ratio of rain-fed area below the storm's snow line"` (that sentence would make the rest arithmetic, so H5 is at risk; and the parameters still have to be pinned). The easy route (area transfer, 18.7k, 140 ft) is also the literal County rule, so the golden rejects the filed rule on grounds the files do not require.

## Fix

input_files and prompt, then rerun. Either (a) file the carry convention in the County standard or the TM (the transfer variable, snow-line temperature, lapse rate and precipitation gradient as filed numbers or as a rule that derives them from a named record) and state the units of the GHCN elevations; or (b) ship a low-elevation gauged record (or a calibration basin) that lets the transfer be validated out of sample so that the data, not the author, selects the parameters; and (c) widen the margin so the call survives the reasonable parameter range, then regenerate the blocks, and tie the CSV values to the pinned convention.

**Disposition (main thread):** reproduced (80 daily-record implementations, 27,055 to 92,536 cfs); revised to the airport's hourly record (revision 2).
