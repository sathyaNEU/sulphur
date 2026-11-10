# leak check, task4

**Verdict: REVIEW.** 13 files read, 19 golden figures and 7 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: careful, record, orders, drifts, station, missed, design-day, stations, reader, within-duty, terminal, readings, architecture, network, decisive, calibration, declared, winter, carries, golden, straight, result, temperature, months, graded

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `fleet_electrification_standard_FES-2.pdf`: golden figure 4.2 appears: ...n ambient temperature of minus 5 degrees Celsius. 4.2 A duty's planning load is the mean net payload of...
- **REVIEW** `quotation_bev_tractors_2027.pdf`: golden figure 540 appears: ...ttery Installed capacity 630 kWh; usable capacity 540 kWh Charging CCS2, up to 375 kW DC; on-board 43 k...
- **REVIEW** `fleet_electrification_standard_FES-2.pdf`: carries 4 of 6 distinctive words of the committed call: 'Order 8 battery-electric tractors, for V02, V03, V05, V09, V11, V14, V16, V18; V07, V21, V24, V27, V30, V33 stay on dies'
- **REVIEW** `quotation_bev_tractors_2027.pdf`: carries 4 of 6 distinctive words of the committed call: 'Order 8 battery-electric tractors, for V02, V03, V05, V09, V11, V14, V16, V18; V07, V21, V24, V27, V30, V33 stay on dies'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `fleet_electrification_standard_FES-2.pdf`: 3 of 25 stump-paragraph terms appear (record, temperature, months); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 43% of 14 prompts (cap 30%); deliverable set 'docx+xlsx' at 21% of 14 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read (architecture 8, target.zip 19b6bec945fc8f80)

**1. Which sentence or file tells you how any part of the analysis should be done (a step, a comparison, an adjustment, a grouping, a population, a window, a model term)? Quote it. Say "none" if none.**

Nothing names a step, model term, comparison or adjustment. `fleet_electrification_standard_FES-2.pdf` fixes several *definitions* used to frame the question (see Q5), but it never says how to estimate anything (no regression, no grouping variable, no formula). No sentence anywhere says "adjust for temperature," "use a regression," "group by shipper," "exclude duty X," or similar. None found in any CSV/XLSX header, comment or cell either.

**2. Which file already ranks or scores the candidate duties on the prompt's question?**

None. `fleet_plan_2027.xlsx`, sheet "Shortlist 2027," lists the 14 candidate Värnamo duties (V02, V03, V05, V07, V09, V11, V14, V16, V18, V21, V24, V27, V30, V33) with only Duty, Shipper code/name, Delivery town, Days a week 2027, and Charging location text. No energy figure, no score, no flag for "goes electric," no order count anywhere in this or any other file.

**3. Which file or sheet exists only to help the analyst (a dictionary, notes, a manifest, commentary on what a column means)?**

`shipper_register_2026.xlsx` ("Shippers") is the closest thing to a pure reference table: code-to-name-to-site lookup with payment terms and service type, used only to resolve shipper codes (ANE, BMJ, KCY, etc.) that appear elsewhere. It carries no commentary on methodology, just entity lookup data. No file contains a literal "data dictionary" or "notes" tab explaining what a column means.

**4. Which figure or name reads as the answer rather than context?**

None found. No cell, filename, or sentence states a tractor count, an order size, a duty-by-duty "electric: yes/no" verdict, or a kWh figure presented as a final result. The quotation PDF states "valid for any number of tractors from one to twelve" (a vendor's capacity statement, not a recommendation), and nothing else resembles a pre-computed answer.

**5. Which filed sentence, read literally, fixes how any graded figure is computed or over which population? Quote it and state what it fixes literally (in words, no computation).**

From `fleet_electrification_standard_FES-2.pdf`:
- "2.2 A duty's energy is the energy the tractor draws from its battery for the round trip, depot out to depot in, in kWh, as the tractor's own battery system reports it." — Fixes the unit and boundary (depot-to-depot round trip) for the energy figure; fixes the source as the tractor's own battery system data (i.e., the BEV daily summary file), not a derived or modeled distance-based quantity.
- "2.3 The usable battery of a tractor model is the usable energy its manufacturer states for it, less the share of its usable energy a battery permanently loses in its first twelve months in service. That share is taken from the company's own battery-electric tractors." — Fixes the population for the "first-year loss share" figure as the company's own existing BEV tractors (the Jönköping pilot fleet), not the new model being quoted, and fixes the window as the first twelve months in service.
- "3.1 Energy figures for planning are estimated from the company's own operating records of its battery-electric tractors. Manufacturers' range and consumption figures are not used for planning." — Fixes the data source (own operating records) and explicitly excludes the manufacturer's spec sheet figures (the quotation's 630/540 kWh line) from use in the energy estimate.
- "4.1 The January design day is a working day with a mean ambient temperature of minus 5 degrees Celsius." — Fixes the temperature condition that defines the design-day window for the energy forecast.
- "4.2 A duty's planning load is the mean net payload of its departures in the twelve months to the end of the last full month before the assessment." — Fixes the population (a duty's own departures) and window (trailing twelve months to the last full month) for the payload figure used in the energy comparison.
- "4.3 A duty is assigned to a battery-electric tractor when its energy on the January design day, carrying its planning load, is no more than 85 per cent of the usable battery of the tractor model being ordered... Each duty assigned takes one tractor." — Fixes the comparison (energy vs. 85% of usable battery) and the unit-of-tractor-count rule (one tractor per assigned duty), i.e., what counts as "goes electric" and how duty count maps to tractor count.

These all fix the WHAT (population, window, unit, comparison) of a result, not the HOW (no formula, model or adjustment is specified for forecasting a duty's design-day energy from the pilot fleet's recorded energy).

**6. Is there one thing that, once noticed, would make most of what the prompt asks routine? For each ask: analysis, or reading a field/rule/planted thing?**

No single file, sentence, or column does this. The pieces needed are spread across files that must each be analyzed on their own terms:
- Forecasting each shortlisted duty's January design-day energy from the Jönköping pilot tractors' recorded daily energy (`bev_daily_summary_2025-03_2026-10.csv`) requires relating energy to distance, temperature (`daily_mean_temperature_2016-2026.csv`), payload, and route profile (climb, route register) — this is genuine modeling, not a lookup.
- The payload-energy relationship (kWh per tonne per 100 loaded km) requires a regression/derivation across the pilot's own trips, not a stated figure.
- The first-year usable-battery loss share requires inferring degradation from the pilot fleet's own operating history over its time in service (no explicit "degradation %" column anywhere) — this is analysis, not a reading.
- The "goes electric" call is a straightforward rule application (FES-2 4.3) once a duty's design-day energy figure is actually computed — but computing that figure is itself the hard analytical step, so the rule by itself settles nothing without the upstream work.
- Separately, the Värnamo duty-numbering change on 13 April 2026 (route register's "Duty (before 13 Apr 2026)" column, vs. `VMO-xx` codes still used in parts of `tms_consignments_varnamo...csv` and `weighbridge_varnamo...csv`) is a reconciliation step that must be done correctly to join trip/weighbridge records to the right shortlisted duties, but the mapping itself is given in the route register, so it is assembly work, not a hidden trap.

No single sentence or file collapses this into a lookup; nothing here reads as a shortcut that would make "most of" the asks routine.

**7. Realism checks.**

All four workbooks have distinct, plausible `docProps/core.xml` authorship and dates (Inger Norman, Georg Pålsson, Ekonomi; created 2020–2022, modified through late 2026), not a single uniform stamp. Both PDFs are produced by LibreOffice Writer with distinct creation timestamps, authors and page counts consistent with their content (fleet standard dated 22 Sep 2025; quotation dated 2 Oct 2026), nothing FPDF/ReportLab-flavoured.

Quotation `quotation_bev_tractors_2027.pdf` specification table: read line by line (Tractor, Battery, Charging, Drive, Unladen weight, Power take-off, Warranty, Price, Delivery) — every line reads as an ordinary dealer quotation line (model configuration, capacity numbers, charging standard, warranty terms, price and delivery conditions). None of the lines is phrased as guidance to the analyst; nothing says "use this figure for planning" or similar. (Note, for cross-reference only, not as a leak: the "Power take-off: Electric PTO, 400 V AC, up to 40 kW, for body and trailer equipment" line is an ordinary spec item that happens to be thematically consistent with the "TRU SR-60e ePTO" reefer trailers seen in the fleet register's Trailers sheet — a real-world detail, not a planted pointer.)

Fleet register's Trailers sheet Equipment column: reads like a genuine fleet register. It mixes `None` (empty) with varied, semicolon-separated equipment strings ("Stanchions 12; Strap winches", "Tail lift 2,500 kg", "TRU SR-60e ePTO; ADR kit", "Coil well; Load bars; ADR kit; Truck-mounted forklift"), several distinct reefer unit model names (TRU SR-60e ePTO, TRU SR-60 D, TRU SR-60 D+SB, TRU AX-40 AGen), non-uniform tare weights, and irregular fleet-number spacing (T-104, 107, 111, 114, 116, 119, 121...). This does not read as templated or auto-generated; it has the irregularity of a real asset register.

**8. Distractors: which files look relevant but seem unused for the question?**

- `fuel_card_statement_varnamo_2025-2026.csv` — diesel fuel purchases (litres, SEK/l, station) keyed to diesel vehicle registrations only (checked: none of the six Jönköping BEV registrations appear in it). Looks like an operating-cost file but the prompt asks only about battery energy, electrification calls, payload-energy relationship and first-year battery loss — no cost figure is requested, so this file's diesel-cost data has no apparent role.
- `workshop_log_2025-2026.csv` — maintenance work orders across the whole fleet (tyres, tail-lift repairs, BEV "Service, battery-electric" jobs with labour hours and SEK cost). Contains no battery-capacity or degradation figures, just routine maintenance costs; looks like it could matter for a battery-health question but carries no capacity/energy data, only cost and labour time.
- `tms_consignments_jonkoping_2025-2026.csv` — Jönköping delivery consignments (not Värnamo), relevant to the Jönköping *pilot duties* in principle, but the prompt's shortlist and order question are entirely about Värnamo duties; its role (if any) is limited to characterizing the pilot's own payload pattern, and it may simply sit alongside the BEV daily summary as unused once the pilot's energy and payload relationship is drawn from the daily summary and weighbridge-style records instead.

Main thread's ruling (2026-11-09): no question-1 quote, no ranking file, no helper file, no answer figure; every
question-5 sentence fixes a WHAT and executes to the golden's estimand (FES-2 3.1 bars the manufacturer's range and
consumption figures from the energy estimate, while 2.3 takes the usable battery from the manufacturer, as the golden
does). The reader's guess that the Jönköping notes may go unused is a solver's first impression, not a finding: they
carry the pilot's declarations, trailers and drops. Every REVIEW line harmless (design note, Literal reader).

## Solver's-eye read

2026-11-10, one isolated reader (Sonnet, medium) on fresh copies of prompt.txt and target/ (target.zip 494b463c).

1. No sentence or file says how any part of the analysis is done; the quotation is a price and specification sheet. FES-2 fixes definitions, windows and populations (see 5), none of them a method.
2. No file ranks or scores the shortlisted duties: fleet_plan_2027.xlsx lists the fourteen with shipper, delivery and charging, no energy, flag or count.
3. No helper file: the shipper register and the route register's Stops sheet are reference lookups the organisation keeps.
4. Nothing reads as the answer; 540 kWh (quotation) and 520 kWh (fleet register) read as specification inputs.
5. FES-2 2.2 (energy depot out to depot in), 2.3 (the loss from the company's own tractors), 4.1 (-5 C), 4.2 (mean net payload over the twelve months to the last full month), 4.3 (85 per cent, one tractor a duty): each fixes a WHAT; read literally each gives the golden's estimand (main thread: the golden executes every one as written).
6. No one thing: every requested figure needs an estimate from the operating data; the payload term, the loss and the energies are analysis; the order follows the filed 4.3 rule once the energies and limit exist.
7. A careful but hurried analyst would clean and join, compute planning loads, fit a linear energy model, apply 85 per cent: right on the broad pass and fail pattern, wrong or rough on the loss and the payload coefficient; the reader's estimate "roughly a third to 40 per cent of the graded detail", counting six pieces including the planning loads (not graded) and the order's direction. Main thread: result by result it agrees with effort.py (verdicts Partly, payload, loss and order missed); the gap is the denominator.
8. No generation tells seen (ids, plates, stamps, remarks, mixed weight formats, document prose).

Sweep REVIEW lines, ruled by the main thread: sweeps 3 and 4 on FES-2 and the quotation are clause numbers (4.2), the quoted 540 kWh input and ordinary words of an order and a specification (orders, terminal, weight, combination, record, temperature, months), naming no step; the reader found neither document names a method. Sweep 11's shell quota is a WARN for the author's rewrite.
