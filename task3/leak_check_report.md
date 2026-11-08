# leak check, task3

**Verdict: REVIEW.** 13 files read, 3 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, leachate, network, matured, travel, clearing, recharge, county, conversions, wellhead, effect, decisive, fitted, sentence, survey, reading, weight, rounding, january, pooled, factor, recent, arrival, mixing, prompt

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `sallow_road_wellhead_protection_plan_2019.pdf`: 6 of 25 stump-paragraph terms appear (travel, recharge, county, wellhead, effect, weight); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: no method hint: carries weighted: keep only if it is the organisation's own word for a thing, not a pointer to the step

## 12 describing content (REVIEW 1)
- **REVIEW** `sallow_road_wellhead_protection_plan_2019.pdf`: names 9 column(s) of the data files verbatim (Well 3, acres, private, residential, site, source): confirm it is the organisation's own record and not a note written for the analyst

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, image or presentation, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)


## Solver's-eye read

Isolated reader (Sonnet, medium), 2026-11-08, on fresh copies of prompt.txt and target/.

1. Decisive step: none named. Rule WR-4 4.1 and 4.2 fix the question; the drawdown must come from the test, the
   well records and the Mill Street history, "but nothing says how".
2. No file ranks or scores the schedules; the application lists rates and monthly factors only.
3. No readme or dictionary; the register's Units, Datum and MP history sheets read as normal register content.
4. Nothing reads as the answer; the test rate (about 1,005 gpm) sits near the 1,000 gpm schedule ("mild, not a leak").
5. Literal sentences: Rule 2.2 (the Mill Street projection), 1.2 (term to 2046), the application's April 2027 start
   and equal split, 4.4 (the nearest domestic well), Table 1 (9.0 ft): each executes to the golden's estimand.
6. Decided by the hydrogeologic analysis (the model for extrapolating to 2046 left open); the clocks, barometer,
   re-hang and measuring points read as cleaning.

Main thread's rulings: Q4 harmless (the test was run near the field's design rate, as tests are). Realism: the
plate's "wells added October 2026" line read as machine-made and is removed in the generator; the rest harmless.

## Solver's-eye read

Isolated reader (Sonnet, medium) on prompt.txt and a fresh copy of target/, 2026-11-08:

# Solver's-eye read, task3 (no solving, no figures)

1. Decisive step quoted: prompt.txt: "requires it in service before the first year the annual flow-weighted mean nitrate at entry point EP-01 reaches 10 mg/L, and fixes the wells' pumping shares from 2027; hold each parcel's land cover as it stood in 2026." The supply plan says it too: "the utility's compliance and planning measure is the annual flow-weighted mean nitrate at EP-01" and the share table (Well 3 20 to 8 per cent). Together they hand over the structure (forecast per well, blend by planned shares, hold land cover). The prompt does not say how to forecast each well's nitrate.

2. Ranking / forecast / judgement on the question: none. No file ranks the options or forecasts nitrate. The WHPP gives zones, times of travel and recharge but no nitrate forecast. The supply plan gives the two in-service dates (1 Jan 2030 for the 2027 cycle, 1 Jan 2034 for the 2031 cycle) but no nitrate judgement.

3. Helper-only files: none that exist only to explain the folder. The closest is the "Land cover codes" sheet in ravell_county_groundwater_network_sites.xlsx (a code key, a normal lookup) and the "Recharge" sheet in sallow_road_WHPA_parcel_attributes_2019.xlsx (it repeats Table 1 of the WHPP). Both are ordinary reference tables, not a readme or manifest.

4. Figure or name that reads as the answer: none. The only candidate decision dates are the plan's two in-service dates (2030, 2034), which are given inputs, not the answer. The prompt's "2034 annual mean" and "first year ... reaches 10" ask for outputs and are not stated anywhere. Mild note: the prompt asks for the 2034 mean, which matches the 2031-cycle in-service year, so the 2034 hint tells the solver which year matters, though not the value.

5. Filed sentence fixing the main figure's computation / population:
 - corlinden_water_supply_plan_2025.pdf s.3: "the utility's compliance and planning measure is the annual flow-weighted mean nitrate at EP-01". Literal reading: the EP-01 annual mean is the pumping-weighted blend of the wells' nitrate, with well weights from pumped volume (the wells blend at a common header, samples at EP-01 also exist monthly).
 - Table 1 (plan): "The plan's shares of annual pumping are fixed for 2027 to 2040 and do not depend on demand": the 2027 to 2040 well weights are the plan's percentages, not history.
 - Prompt: "hold each parcel's land cover as it stood in 2026": the land-cover input to any forecast is frozen at 2026.
 - Plan s.4: in-service dates and "must be in service before the first calendar year in which the annual flow-weighted mean ... reaches 10", so the funding call compares that first year with 2030 and 2034.
 Method of forecasting each well's nitrate stays open (not filed).

6. What decides the main answer: mainly an analytical choice (how to project each well's nitrate to 2040 given the lag from land cover and travel time, and the pumping blend), with some rule-following (blend weights, 10 mg/L threshold, cycle dates are all filed). Deciding material: WHPP s.3 (recharge by land cover, flow-weighted travel time) and the parcel/land-cover/network files; the plan fixes the rules around it. Data semantics also bite (nitrate reported as NO3 in the files versus as N in the prompt; sample_point names; HR-W points; field duplicates; land-cover codes changing in 2008), but these read as cleaning texture, not the stump.

## Mechanical-sweep items
- prompt.txt "annual flow-weighted mean nitrate": harmless. It is the utility's own compliance measure as the supply plan s.3 states it, so the word names the quantity, not a step to take. (Slight caution: it does tell the solver the EP-01 mean is volume-weighted, but the plan's own text says so already.)
- sallow_road_wellhead_protection_plan_2019.pdf column values: harmless. It reads as the consultant's own 2019 plan deliverable (hydrogeologic setting, model, zones, inventory, recommendations) that cites the spreadsheet as its Appendix B; it is not addressed to an analyst and states no method for the task. Note it does supply a method-adjacent input (recharge by land cover, time-of-travel definition), but as the organisation's record of its model.
