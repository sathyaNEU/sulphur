# leak check, task4

**Verdict: REVIEW.** 14 files read, 73 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: asserted, record, heaters, careful, inside, carried, recharge, quotation, session, conditioning, temperature, architecture, bridge, graded, capacity, sessions, pooled, energies, register, station, winter, second, steady, verdicts, chargers

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `depot_electrification_standard_DES-1.pdf`: golden figure 4.3 appears: ...tay on diesel until the connection is reinforced. 4.3 The order put to the board is one bus for each bl...
- **REVIEW** `depot_electrification_standard_DES-1.pdf`: golden figure 4.1 appears: ...each block's electrification. 4. Assigning blocks 4.1 A weekday block qualifies for a battery-electric...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `depot_electrification_standard_DES-1.pdf`: 8 of 25 stump-paragraph terms appear (record, recharge, session, temperature, capacity, register); read whether the document names the move
- **REVIEW** `ebus_quotation_2027.pdf`: 3 of 25 stump-paragraph terms appear (heaters, quotation, capacity); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


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
- "2.2 A duty's energy is the energy the tractor draws from its battery for the round trip, depot out to depot in, in kWh, as the tractor's own battery system reports it.", Fixes the unit and boundary (depot-to-depot round trip) for the energy figure; fixes the source as the tractor's own battery system data (i.e., the BEV daily summary file), not a derived or modeled distance-based quantity.
- "2.3 The usable battery of a tractor model is the usable energy its manufacturer states for it, less the share of its usable energy a battery permanently loses in its first twelve months in service. That share is taken from the company's own battery-electric tractors.", Fixes the population for the "first-year loss share" figure as the company's own existing BEV tractors (the Jönköping pilot fleet), not the new model being quoted, and fixes the window as the first twelve months in service.
- "3.1 Energy figures for planning are estimated from the company's own operating records of its battery-electric tractors. Manufacturers' range and consumption figures are not used for planning.", Fixes the data source (own operating records) and explicitly excludes the manufacturer's spec sheet figures (the quotation's 630/540 kWh line) from use in the energy estimate.
- "4.1 The January design day is a working day with a mean ambient temperature of minus 5 degrees Celsius.", Fixes the temperature condition that defines the design-day window for the energy forecast.
- "4.2 A duty's planning load is the mean net payload of its departures in the twelve months to the end of the last full month before the assessment.", Fixes the population (a duty's own departures) and window (trailing twelve months to the last full month) for the payload figure used in the energy comparison.
- "4.3 A duty is assigned to a battery-electric tractor when its energy on the January design day, carrying its planning load, is no more than 85 per cent of the usable battery of the tractor model being ordered... Each duty assigned takes one tractor.", Fixes the comparison (energy vs. 85% of usable battery) and the unit-of-tractor-count rule (one tractor per assigned duty), i.e., what counts as "goes electric" and how duty count maps to tractor count.

These all fix the WHAT (population, window, unit, comparison) of a result, not the HOW (no formula, model or adjustment is specified for forecasting a duty's design-day energy from the pilot fleet's recorded energy).

**6. Is there one thing that, once noticed, would make most of what the prompt asks routine? For each ask: analysis, or reading a field/rule/planted thing?**

No single file, sentence, or column does this. The pieces needed are spread across files that must each be analyzed on their own terms:
- Forecasting each shortlisted duty's January design-day energy from the Jönköping pilot tractors' recorded daily energy (`bev_daily_summary_2025-03_2026-10.csv`) requires relating energy to distance, temperature (`daily_mean_temperature_2016-2026.csv`), payload, and route profile (climb, route register), this is genuine modeling, not a lookup.
- The payload-energy relationship (kWh per tonne per 100 loaded km) requires a regression/derivation across the pilot's own trips, not a stated figure.
- The first-year usable-battery loss share requires inferring degradation from the pilot fleet's own operating history over its time in service (no explicit "degradation %" column anywhere), this is analysis, not a reading.
- The "goes electric" call is a straightforward rule application (FES-2 4.3) once a duty's design-day energy figure is actually computed, but computing that figure is itself the hard analytical step, so the rule by itself settles nothing without the upstream work.
- Separately, the Värnamo duty-numbering change on 13 April 2026 (route register's "Duty (before 13 Apr 2026)" column, vs. `VMO-xx` codes still used in parts of `tms_consignments_varnamo...csv` and `weighbridge_varnamo...csv`) is a reconciliation step that must be done correctly to join trip/weighbridge records to the right shortlisted duties, but the mapping itself is given in the route register, so it is assembly work, not a hidden trap.

No single sentence or file collapses this into a lookup; nothing here reads as a shortcut that would make "most of" the asks routine.

**7. Realism checks.**

All four workbooks have distinct, plausible `docProps/core.xml` authorship and dates (Inger Norman, Georg Pålsson, Ekonomi; created 2020 to 2022, modified through late 2026), not a single uniform stamp. Both PDFs are produced by LibreOffice Writer with distinct creation timestamps, authors and page counts consistent with their content (fleet standard dated 22 Sep 2025; quotation dated 2 Oct 2026), nothing FPDF/ReportLab-flavoured.

Quotation `quotation_bev_tractors_2027.pdf` specification table: read line by line (Tractor, Battery, Charging, Drive, Unladen weight, Power take-off, Warranty, Price, Delivery), every line reads as an ordinary dealer quotation line (model configuration, capacity numbers, charging standard, warranty terms, price and delivery conditions). None of the lines is phrased as guidance to the analyst; nothing says "use this figure for planning" or similar. (Note, for cross-reference only, not as a leak: the "Power take-off: Electric PTO, 400 V AC, up to 40 kW, for body and trailer equipment" line is an ordinary spec item that happens to be thematically consistent with the "TRU SR-60e ePTO" reefer trailers seen in the fleet register's Trailers sheet, a real-world detail, not a planted pointer.)

Fleet register's Trailers sheet Equipment column: reads like a genuine fleet register. It mixes `None` (empty) with varied, semicolon-separated equipment strings ("Stanchions 12; Strap winches", "Tail lift 2,500 kg", "TRU SR-60e ePTO; ADR kit", "Coil well; Load bars; ADR kit; Truck-mounted forklift"), several distinct reefer unit model names (TRU SR-60e ePTO, TRU SR-60 D, TRU SR-60 D+SB, TRU AX-40 AGen), non-uniform tare weights, and irregular fleet-number spacing (T-104, 107, 111, 114, 116, 119, 121...). This does not read as templated or auto-generated; it has the irregularity of a real asset register.

**8. Distractors: which files look relevant but seem unused for the question?**

- `fuel_card_statement_varnamo_2025-2026.csv`, diesel fuel purchases (litres, SEK/l, station) keyed to diesel vehicle registrations only (checked: none of the six Jönköping BEV registrations appear in it). Looks like an operating-cost file but the prompt asks only about battery energy, electrification calls, payload-energy relationship and first-year battery loss, no cost figure is requested, so this file's diesel-cost data has no apparent role.
- `workshop_log_2025-2026.csv`, maintenance work orders across the whole fleet (tyres, tail-lift repairs, BEV "Service, battery-electric" jobs with labour hours and SEK cost). Contains no battery-capacity or degradation figures, just routine maintenance costs; looks like it could matter for a battery-health question but carries no capacity/energy data, only cost and labour time.
- `tms_consignments_jonkoping_2025-2026.csv`, Jönköping delivery consignments (not Värnamo), relevant to the Jönköping *pilot duties* in principle, but the prompt's shortlist and order question are entirely about Värnamo duties; its role (if any) is limited to characterizing the pilot's own payload pattern, and it may simply sit alongside the BEV daily summary as unused once the pilot's energy and payload relationship is drawn from the daily summary and weighbridge-style records instead.

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

## Solver's-eye read

Isolated reader (general-purpose, Sonnet, medium) on a fresh copy of prompt.txt and the pack, 2026-11-10, before the
outlet count and the quotation's range were moved (the only change since: 20 to 24 outlets, "four to twenty" to
"four to twenty-four"). It read every file and did not solve the task.

- Q1 (a sentence saying how to do the analysis): the standard's clauses 2.1 to 2.4, 3.1 to 3.3, 4.1 and 4.2 (the
  block's kilometres, the block's energy, the usable battery less the first winter's loss from the company's own
  buses, the design day, planning from own records, depot charging under the agreement, fuel per 100 scheduled km
  over twelve months, the 85 per cent test, the priority list cut at the first block the night cannot recharge), the
  agreement's 705 kW from 21:00 to 07:00, and the fleet plan's "weekday blocks as the 2026 autumn timetable". Ruling:
  every quoted sentence files the WHAT (population, outcome, window, unit, comparison, source) in the organisation's
  own genre; none names a bridge, a selection, a conversion, an age form or a schedule. Harmless.
- Q2 (a file ranking the candidates): the fleet plan's Priority column (1 to 48). Ruling: the city's zone order the
  standard's 4.2 walks, a filed fact, not a ranking on any energy, cost or decision basis (Gate G). Harmless.
- Q3 (a helper file): none found; every file has a standing use.
- Q4 (a figure reading as the answer): "20 further outlets, one per bus" and the quotation's "four to twenty buses"
  (the figure 20 twice). Ruling: fixed in the generator (24 outlets, four to twenty-four buses), off every route's
  count.
- Q5 (a literal sentence fixing a graded figure): 4.1 (the yes or no is the threshold check), 4.2 (the count and the
  set walk the priority list and stop at the first block the night cannot recharge), 3.3 (the diesel window, unit and
  population). Ruling: each literal reading is the golden's; the figures they operate on (the energies, the usable
  battery, the night's feasibility, the rates) are the analysis.
- Q6 (one thing): DES-1 section 4 with the priority list and the 705 kW window "settles the ordering method and the
  stopping rule... it does not settle the two input figures per block, the diesel figure, the first-year loss or the
  night energy, each of which still needs real work". The reader placed the diesel figures, the energies, the loss and
  the night on analysis, the verdict and the cut on the stated procedure once the inputs are right, and found nothing
  planted (hygiene items named: the 2025-08-11 recoding, the HVO rows on the electric buses' cards, the spare cards'
  typed vehicle). It saw the heating-system difference between the register and the quotation and predicted that a
  careful but hurried analyst "would most likely just fit energy or hvac_kwh vs ambient on the pilot fleet and evaluate
  at minus 15 without adjusting for the pilots' fuel-fired heat assist". It did not mention the pilot's selection on
  the fuel figures or the diesel bridge.
- Realism: no tell (three LibreOffice releases with their own stamps, two workbook creators, no hidden content, id
  sequences without a constant step); DES-1's numbered-clause style noted as the easiest kind to over-script, "not a
  tell on its own".
- Careful-pass estimate: "something under half", the losses on the design-day energy (the heaters), the first-year
  loss (the temperature confound or the warranty line), the night's cut (an energy budget in place of the windows) and
  the count that chains off them; in line with effort.py's 36.0.
- Unplaced: the two distractors (tyre and brake costs; the depot's electricity invoices).
- Flagged files: the standard "announces analytical moves" in 3.1, 4.1 and 4.2 (ruled above: the organisation's own
  rules, the WHAT); the agreement, the quotation and the fleet plan file facts only.

## Solver's-eye read, second pass (after the first judge pass and the rebuild)

Isolated reader (general-purpose, Sonnet, medium) on a fresh copy of the rebuilt prompt and pack, 2026-11-10. It read
every file and did not solve the task. Q1 and Q5: the standard's clauses, the agreement's capacity and the plan's
"weekday blocks as the 2026 autumn timetable" line, as before; it also quoted the quotation's "differ from your 2025
pilot buses in the heating system" as a fact that flags an adjustment without naming it (ruling: a fact of the world
the quotation would state anyway; the adjustment's size and route stay the analysis). Q2: the plan's priority column,
as before. Q3: the block register's Lines sheet and the plan's Timetable 2027 sheet read as a planner's reference
tabs (ruling: both are what such workbooks carry; neither describes the pack or a column). Q4: the outlet count and the
quotation's order range both at 24 (fixed in the generator: 26 outlets, four to thirty buses); the warranty's 70 per
cent at eight years as a loss-shaped figure a hurried reader could mistake for the first-year loss (ruling: a fact
of the quotation, ruled out by DES-1 2.3's own words, which the reader itself cites). Q6: no single fact; the
reader named the rotation of buses over blocks (the diesel attribution), the pilot heaters' HVO against the quoted
model's all-electric heating (a mechanism "the rows carry but no document states outright"), the first-year loss
and the night's cut as separate pieces of work, nothing planted. Realism: it found a charging session starting under
zero state of charge (fixed in the generator: the pilot's blocks and stand-ins now pass the planner's own range check,
no electric day ends under 15 per cent). Careful estimate: "something under half", the losses on the heaters, the
loss figure, the night's cut and the count. Unplaced: the two distractors and the workshop log.

## Solver's-eye read, third pass (the final cut, 4e8a8998)

Isolated reader (general-purpose, Sonnet, medium), 2026-11-10. Q1 and Q5 as before (the standard's clauses, the
agreement's capacity), plus a live reading of DES-1 2.4's "the town's weather station" against the two series in the
weather file (fixed in the generator: 2.4 now names the airport station; the town-centre series is asserted to land
the same order, SF28). Q2: the priority column, zone by zone (the city's order). Q3: the weather file as pure support
and the register's Lines sheet (ruling: an external series and a lookup tab, neither narrates the pack). Q4: the
outlets line "26 further outlets, one per bus and two spare" (reworded in the generator as the 2027 to 2029 rollout).
Q6: no single fact; the reader placed the diesel figures on assembly, the energies on modelling with the heating
difference "the rows carry but no document states outright", the loss on the telematics against the sessions' grid-
side energy, the cut on a real scheduling constraint; nothing planted. Realism: no tell beyond the zone-ordered
priority list (the city's order). Careful estimate: the mechanical half right, the heating difference, the loss's
source and the 36 never-run blocks where it goes wrong; no number given. Unplaced: the two distractors.

## Solver's-eye read, fourth pass (target.zip 67186f2dd19abb65, 2026-11-10)

An isolated Sonnet reader, cold, on a fresh unzip and the prompt only.
1. How to do the analysis: none beyond the standard's WHAT (DES-1 2.3 the loss's population, 2.4 the design day, 3.1 own records not the manufacturer's figures, 3.3 the diesel window and sources, 4.1 the 85 per cent test, 4.2 the priority order and the cut); "none of these supplies a number or a method".
2. Ranking: the fleet plan's Priority column, which DES-1 4.2 names as the assignment order; a zone queue, not a score on the question. Harmless (an input the decision takes).
3. Helper file: none.
4. Answer-like figure: the fleet plan's "26 further outlets, the 2027 to 2029 rollout" beside the quotation's "four to thirty buses". Ruled harmless: a multi-year infrastructure line, argued as no order and ranking nothing; a run that orders 26 has skipped the analysis the asks require.
5. Literal sentences: DES-1 2.3 (the loss from the company's own buses, their first twelve months) and 3.3 (the trailing twelve months, the fuel-card statements and the dispatch log): both execute to the golden's population and window.
6. One thing: none; the closest (the pilot buses run a fixed set of nine weekday blocks) settles only that those blocks have electric records. The reader noticed the pilot buses' fuel-fired heaters against the 2027 model's all-electric heating on a read, so R3's notice is a careful-pass move; its figure still needs the HVO fills tank to tank against hours and temperatures.
Sweep lines: the DES-1 clause numbers coinciding with figures, harmless (section numbering); the fleet plan's 2027 dates, harmless (the plan's own timetable).
Realism: nothing reads as generated; fills to two decimals, prices spread, no duplicate rows in 41,790 dispatch rows, charging starts shifting with summer time; the tyre and brake report reads as a genuine unused maintenance report.

## Solver's-eye read, architecture 10 loop 1 (read on target.zip 133243bf4849fb55, 2026-11-10)

# Leak read: task4 scratch pack (Niittylä depot battery-electric bus order)

Scope read in full: prompt.txt and all 14 files under target/ (block_register_2026.xlsx,
charging_connection_agreement_2025.pdf, depot_charging_sessions_2025-03_2026-10.csv,
depot_dispatch_log_2024-01_2026-10.csv, depot_electricity_invoices_2025-01_2026-10.csv,
depot_electrification_standard_DES-1.pdf, ebus_quotation_2027.pdf,
ebus_telematics_daily_2025-03_2026-10.csv, fleet_plan_2027.xlsx,
fuel_card_transactions_2024-01_2026-10.csv, tyre_and_brake_costs_2025.xlsx,
vehicle_register_2026.xlsx, weather_vehkasalo_daily_2016_2026.csv,
workshop_orders_2024-01_2026-10.csv). No figure computed, no score given.

## 1. Which sentence or file tells you how any part of the analysis should be done?

`depot_electrification_standard_DES-1.pdf` is the one document that states method/process
sentences (as opposed to pure data). Verbatim:

- "2.3 The usable battery of a bus model is the usable energy its manufacturer states for it
  when new, less the share of usable energy a traction battery permanently loses in its first
  twelve months in service. That share is taken from the company's own battery-electric buses."
- "2.4 The design day is a January working day with a daily mean air temperature of minus 15
  degrees Celsius at the town's airport weather station (Vehkasalo lentoasema). The design night
  is the night that follows it, at the same daily mean temperature."
- "3.1 Energy figures for planning are estimated from the company's own operating records.
  Manufacturers' range and consumption figures are not used for planning."
- "3.2 A battery-electric bus is charged at its depot only, on the charging lane's chargers,
  between its block's return and its next departure... The depot's chargers deliver up to 150 kW
  to a bus, and the charging installation draws no more than the capacity the distribution
  company's connection agreement gives it, in the periods the agreement gives it."
- "3.3 Fuel use is reported per block as litres of diesel per 100 scheduled kilometres over the
  twelve months to the end of the last full month before the assessment, from the fuel-card
  statements and the dispatch log, for the business case of each block's electrification."
- "4.1 A weekday block qualifies for a battery-electric bus when its energy on the design day is
  no more than 85 per cent of the usable battery of the bus model being ordered."
- "4.2 Qualifying blocks are assigned in the order of the fleet plan's priority list. The list is
  cut at the first block the depot cannot recharge, together with every block above it on the
  list, between the blocks' returns and their departures under 3.2."

These fix the WHAT (population, window, unit, comparison) for each figure; none of them supplies
the number itself.

## 2. Which file already ranks or scores the candidates on the prompt's question?

`fleet_plan_2027.xlsx`, sheet "Weekday blocks 2027", column "Priority": every one of the 48
Mon-Fri blocks (M101-M148) is given a rank from 1 to 48.

```
('Priority', 'Block', 'Lines', 'Scheduled km', 'Depot departure', 'Depot return', 'Zone', 'Note')
(1, 'M108', '9', 112.7, '05:31', '15:56', 1, 'centre lines, low-emission zone from 2027')
(2, 'M107', '9', 134.9, '05:48', '19:07', 1, None)
(3, 'M148', '3', 114.9, '07:01', '19:19', 1, None)
```

This is not incidental: DES-1 4.2 ("Qualifying blocks are assigned in the order of the fleet
plan's priority list") names this exact column as the ordering input for "which blocks."

## 3. Which file exists only to help the analyst?

None. All 14 files read as first-party business records (operating logs, registers, invoices, a
signed utility letter, a vendor quotation letter, an internal standard with its own version and
approval history), each tied to a named staff member consistent across files (Simo Virta appears
as DES-1's document author and as the addressee of the bus quotation; Eveliina Pajunen owns the
vehicle/tyre-brake registers and is addressed as "Ms Pajunen" in the connection-agreement letter).
No glossary, methodology note, or crib sheet is present.

## 4. Which figure or name reads as the answer rather than context?

No figure or name is presented as a finished result. The nearest thing is the "Priority" column
in fleet_plan_2027.xlsx (question 2) and, within it, block M108 at Priority 1, the only row
carrying a Note ("centre lines, low-emission zone from 2027"), which could read as a pointer to
"start here." But Priority ranks all 48 blocks, not a filtered qualifying set, and DES-1 4.1/4.2
still require the energy-vs-85%-threshold test and the recharge-feasibility cut before any block,
count, or MWh figure is settled. Nothing states the bus count, a block's qualification, the
degradation share, or the MWh draw outright.

## 5. Which filed sentence, read literally, fixes how any graded figure is computed or over which population?

Primary: DES-1 "4.1 A weekday block qualifies for a battery-electric bus when its energy on the
design day is no more than 85 per cent of the usable battery of the bus model being ordered."
Literal result in words: this fixes the yes/no figure as a single threshold comparison (qualify =
yes exactly when modelled design-day energy <= 85% of the 2027 model's usable battery net of
first-year loss, no otherwise). It fixes the comparison, not either input value.

Also fixing a population/window/source (not a number) for other graded figures:
- DES-1 2.3 fixes the first-year-loss figure's population to "the company's own battery-electric
  buses" (the six pilots) and its window to each one's own first twelve months in service, ruling
  out the quotation's unrelated warranty benchmark.
- DES-1 3.3 fixes the diesel-use figure's unit (L/100 scheduled km), window (trailing 12 months to
  the last full month before assessment) and sources (fuel-card statements, dispatch log).
- DES-1 4.2 fixes the ordering input (fleet_plan's Priority column) and the stopping rule (cut at
  the first non-rechargeable block) for "which blocks" / "how many buses."

## 6. Is there one thing that would make most of the prompt routine? Per-ask breakdown.

No single file, sentence, column or data pattern does this. The closest candidate is the DES-1
standard taken as a whole: it settles which comparison decides yes/no (4.1), which file's column
decides assignment order (4.2), and what "block," "block energy," "design day/night," and the
diesel window mean. What it does not settle, for any block: the design-day energy figure itself
(no document or telematics row is keyed to "design day," and the six pilot buses never ran a
numbered block at all per the dispatch log, so a consumption model has to be transferred from
their telematics to each block's own duty profile), the first-year loss share (must be measured
from the pilots' own history), the trailing-12-month diesel rate (must be assembled from four
fuel stations, two diesel spellings, time-bounded card reassignments, and HVO/AdBlue exclusions),
or the installation's MWh draw (must be modelled against the 690 kW night cap and the charger
rollout timing, complicated by the pilots relocating to another depot on 2027-01-11). So DES-1
fixes the rules, not the results.

Per ask:
- "How many battery-electric buses should we order", analysis (sums the per-block results),
  combined under a stated counting rule (4.3) once those results exist.
- "which weekday blocks should they take", analysis (the per-block qualification test) combined
  with a stated ordering/cut procedure (4.2) that names fleet_plan's priority list.
- "diesel use ... litres per 100 scheduled kilometres" per block, analysis: reconciling ~20,800
  fuel-card rows (two diesel spellings, one depot + three retail stations, re-keyed cards, HVO/
  AdBlue to exclude) to vehicles to blocks via the dispatch log.
- "battery energy in kWh ... on the standard's design day" per block, analysis: the pilots never
  ran these blocks (confirmed against the dispatch log), so a temperature/HVAC consumption model
  built from their telematics must be transferred to each block's own distance/duty profile, and
  the 2027 model's fully-electric heating (vs. the pilots' partly fuel-fired heating) has to be
  accounted for rather than copied.
- "a yes or no on whether it qualifies" per block, follows a stated rule (4.1) once the two
  figures above exist; the rule is given, the inputs are not.
- "share of usable battery ... lose for good in their first year", analysis: measured from the
  six pilots' own first-12-months charging/telematics history; the quotation's unrelated
  70%-at-8-years warranty figure is a plausible wrong number to reach for instead.
- "energy in MWh the charging installation would draw ... design night ... every qualifying block
  on charge", analysis: modelling simultaneous overnight demand against the connection
  agreement's stated 690 kW cap and the depot's charger count/timing.

No ask turns on catching one planted defect. The only "catch" items found (card reassignments,
two diesel spellings, HVO sitting only on the pilots' cards, AdBlue-only vehicle entry) are
ordinary fleet-data hygiene, not a single hidden fact that flips a result.

## A. depot_electrification_standard_DES-1.pdf, two number matches

Numeric tokens in the document, with counts: 1 (x5, from "1. Scope", "version 1", and the two
"DES-1"/"Page 1" header/footer occurrences), 2 (x3, "Version 2", "2. Terms", "2.4"'s "2"), 15
(x2, "85 per cent"'s complement and "minus 15 degrees"), 100, 150, 18, 85, 2024, 2026, plus the
section/subsection labels 2.1-2.4, 3.1-3.3, 4.1-4.4, 5.1. These are overwhelmingly (a) section/
subsection numbering, (b) the document's own version/approval dates, or (c) the standard's rule
constants (85 and 15 as the qualifying split, 150 as the per-charger kW cap, 100 as the diesel
rate's per-km basis). The document never states a bus count, a block's energy or diesel rate, a
degradation share, or an MWh figure anywhere, only rule text and administrative metadata.
Whichever two numbers the sweep matched, they are generic low-cardinality labels or constants
colliding by chance with unrelated computed figures; none of them reads, in context, as a stated
answer.

**Ruling: harmless.** No number in this document is presented as a result; the matches are
coincidental overlaps of section labels/rule constants with unrelated figures.

## B. fleet_plan_2027.xlsx, 4 ISO dates after 2026-11-06

All four are in sheet "Timetable 2027":
```
('Winter timetable 2027', '2027-01-11', 'weekday blocks as the 2026 autumn timetable')
('Summer timetable 2027', '2027-06-07', 'to be planned in spring')
('Line 8 to Satama hourly', '2027-01-11', 'within block kilometres as listed')
('Buses 1201 to 1206 to Kauppala depot', '2027-01-11', "regional and school lines; the city's 2027 terms exclude fuel-fired heaters")
```
Three cells read 2027-01-11 and one reads 2027-06-07, matching the sweep's count exactly.

**Ruling: harmless.** These are the planned future effective dates of timetable/depot changes,
exactly the forward content DES-1 4.4 says belongs in this annual planning cycle ("Blocks are
assessed each autumn for the following year's timetable, before any order is placed"). The
prompt itself is forward-facing (ordering buses for the 2027 timetable), so a fleet-planning
workbook carrying 2027 dates is in-world, not a generation artifact. None of the four dates is a
graded figure. The one substantive fact among them, the pilot buses' relocation to another depot
on 2027-01-11, is operational context relevant to the charging-capacity analysis, not an answer
hand-over.

## Realism tells

- One fuel-card row (ADBLUE, vehicle 1110) is timestamped 2026-11-01, one day past the filename's
  stated "...2026-10" span; a minor extraction-boundary artifact, not an error.
- Several vehicles' fuel cards were re-keyed mid-register (e.g. fleet nos. 1105, 1118, 1121, 1133,
  1134, 1136, 1144, 1150: an old card retired and a new one issued with adjoining validity dates).
  Authentic "latest version" hygiene, not a cross-file disagreement.
- The same diesel fuel is spelled two ways by station: "DIESEL" at the home depot pump (station
  9001) vs. "Diesel B7" at the three external retail stations (1123, 1187, 1409).
- `vehicle_entered` in the fuel-card file is populated only for ADBLUE rows (1,767 of 1,767) and
  never for DIESEL/Diesel B7/HVO (0 of ~19,000), a believable point-of-sale quirk.
- HVO purchases sit on exactly the six pilot e-buses' own fuel cards (confirmed by card number)
  and never on a diesel-fleet card, consistent with their fuel-fired cabin heater; this pattern is
  not written down anywhere and only shows via a cross-tab.
- The dispatch log (2024-01 to 2026-10, 41,790 rows) never once shows any of the six pilot e-bus
  plates against a numbered block, consistent with the fleet plan's own note that they currently
  run "regional and school lines," not the numbered blocks.
- Two workshop orders carry identical templated fault text for two different vehicles ("Fuel
  heater does not start, fault F12 (no flame). Glow pin and metering pump on order." for both 1202
  and 1205, and the matching repair note for both), plausible shared fault-code phrasing, but
  slightly too-clean.
- The quotation's 8-year/500,000 km, 70%-of-usable-capacity warranty line sits one paragraph from
  the battery spec and could be mistaken for the "first year" loss figure the prompt asks about;
  it is a different, later-life measure.

Main thread's rulings (2026-11-10): questions 1 to 6 find no process sentence for any graded result, no helper file, no answer figure and no one thing; the priority column is the city's zone order the standard's 4.2 walks (Gate G, filed as a fact); every literal reading quoted under question 5 executes to the golden. Lines A and B harmless as the reader rules. Realism lines fixed in the generator on target.zip 8a51114e25f18f18: the statement now closes at 31 October 23:59 (the one AdBlue row of 1 November 00:29 belongs to November's statement); the two heater-fault work orders are written up in two mechanics' words; the fleet plan's row reads "Buses 1201 to 1206 move to Kauppala depot" from 11 January 2027 (the reader took the earlier wording for the buses' present work; the dispatch log carries them by fleet number on the nine pilot blocks from March 2025). The other lines (re-keyed cards, two diesel spellings, the typed vehicle on the spare cards' AdBlue rows, HVO only on the electric buses' cards, the warranty line) are the process's own texture. No graded figure moved (the golden folder's digest is unchanged).
