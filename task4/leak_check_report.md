# leak check, task4

**Verdict: REVIEW.** 12 files read, 31 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: record, orders, drifts, station, declared, stations, reader, careful, golden, network, decisive, calibration, weight, shipper, nothing, method, shortcut, missed, readings, season, declarations, modelling, carries, re-run, overflow

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `quotation_bev_tractors_2027.pdf`: golden figure 540 appears: ...ttery Installed capacity 630 kWh; usable capacity 540 kWh Charging CCS2, up to 375 kW DC; on-board 43 k...
- **REVIEW** `fleet_electrification_standard_FES-2.pdf`: carries 4 of 6 distinctive words of the committed call: 'Order 6 battery-electric tractors, for V02, V05, V09, V14, V16, V18; V03, V07, V11, V21, V24, V27, V30, V33 stay on dies'
- **REVIEW** `quotation_bev_tractors_2027.pdf`: carries 4 of 6 distinctive words of the committed call: 'Order 6 battery-electric tractors, for V02, V05, V09, V14, V16, V18; V03, V07, V11, V21, V24, V27, V30, V33 stay on dies'

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'docx+xlsx' at 29% of 14 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 12 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 4 design-note vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Architecture 3, read 1 on target.zip 1b8dcbc7 and read 2 after the prompt's courier-event pin (isolated Sonnet
readers, a fresh copy of prompt.txt and target/ only each time).

1. Decisive step: no sentence names it; the nearest is TDS-4 2.1 (a month's parcels are those the delivery depots
   unloaded on its mornings, a hub's those it sorted the night before), which files the population, not which hub
   sorted a parcel with no sort event.
2. Ranking file: none; the sorter availability file carries downtime minutes only and the claims no hub verdict.
3. Helping file: none; the sort plan and the network register are the reference data a hub analyst works from, the
   request email a cover note.
4. Answer figure or name: none; the standard's 1.00 per cent tolerance only.
5. Population sentences: TDS-4 2.1 to 2.3 (unloaded parcels by sorting hub, a missed scan a parcel with no sort
   event, the alert above 1.00 per cent); 3.1 and 3.2 for the courier events; 4.1 to 4.4 for the pre-advices.
6. What decides: read 1, the analytical choice of the unit and its denominator, the population rebuilt across
   systems; read 2 put it nearest rule application with the sort plan's mapping. Ruled analytical: the sort plan is
   the easy route the record contradicts (Strykow sorted Pruszkow's overflow), and only the unloading each parcel
   came off at its depot places it; both judge passes read Gate H as analytical.

Sweep lines: the standard's 1.00 per cent is its own tolerance; the sort plan's December dates are its planned window
ends; both harmless. Read 2 found the phrase "the extract's courier events" a natural request (the email names the
October extract; "courier event" is TDS-4's own term).

Realism: nothing generated-looking; the register's uniform reader type and door pairs read as one vendor's estate.

## Solver's-eye read

Isolated Sonnet reader, medium effort, 2026-11-08, on target.zip f1a47765 (prompt and pack only).

Leak read (no solving). Files read: prompt, both PDFs, all five XLSX (every sheet, visible), heads of all CSVs.

1. Decisive step: no sentence names it. Closest are filed rules, not the step: FES-2 3.1 "Energy figures for planning are estimated from the company's own operating records of its battery-electric tractors. Manufacturers' range and consumption figures are not used for planning." and 4.3 (design day, 85 per cent of usable battery). These say the source and threshold, not how to model load, temperature and Jonkoping-to-Varnamo transfer. Verdict on whether that is too much help: see Q5.

2. No file ranks or scores the Varnamo candidates. fleet_plan_2027.xlsx is only the shortlist (14 duties, days/week, charger). The BEV summary gives Jonkoping per-day energy and consumption, which are raw records, not per-duty verdicts. Quotation gives capacity only, no consumption or range.

3. Helper-only files: none are readmes or dictionaries. route_register_2026.xlsx carries the "Duty (before 13 Apr 2026)" rename column, which is a join aid (weighbridge uses VMO-nn codes), natural in a register. shipper_register is a plain lookup. No notes file.

4. Answer-like names or figures: none. The only figures that read as hard numbers are standard and quote parameters (minus 5 C, 85 per cent, usable 540 kWh), which are inputs. No tractor count anywhere.

5. Filed sentences that fix the computation:
- FES-2 2.1/2.2: duty = depot-out to depot-in round trip per the route register; energy = battery draw, as the tractor's own battery system reports it (fixes the unit and the energy basis: battery-side, not diesel-equivalent or manufacturer).
- 4.1: design day = working day at a mean ambient of minus 5 C (fixes the temperature condition).
- 4.2: planning load = mean net payload of the duty's departures over the twelve months to the end of the last full month before assessment (fixes the load and window; the assessment date is not stated in the file, only "each autumn", so the window end is inferred from the Oct 2026 data/quote date; likely the fork table's job).
- 4.3: assigned when energy is no more than 85 per cent of usable battery of the model ordered; each duty takes one tractor (fixes the threshold, the battery denominator and the count rule).
- 2.3 + quotation: usable battery = manufacturer-stated usable energy, 540 kWh quoted; fleet_register states a different battery for the existing Jonkoping units (540 installed, 468 usable). The ordered model is the quoted one.
- 3.1: planning energy from the company's own BEV records, not manufacturer figures.
The ordering and arithmetic of the threshold is fully filed. The model for energy given load, temperature and distance is not.

6. What decides the main answer: an analytical choice. A solver must build a per-duty energy model from Jonkoping BEV records (energy vs distance, ambient, load via TMS payload), extrapolate to Varnamo duties (different distances, climb, tare differences, payload from weighbridge with declared vs measured), at minus 5 C, then apply the filed rule. The rule application itself is mechanical (4.3), but nothing in the files states how to get energy for a Varnamo duty; the BEV summary has no payload, no duty or route, so the load and route link must be reconstructed from TMS (declared_weight, mixed units like "9 350 kg") and fleet registers. Risk: much of the difficulty is cleaning (units, rename, tare), and the final step after the model is a filed threshold; if the model is simple, the decision may reduce to rule application plus cleaning. Not a leak, a design note for the author.

Flagged files:
- fleet_electrification_standard_FES-2.pdf: harmless. It files the estimand and the rule, which determinism requires; it does not name the energy model, the temperature or payload dependence, the Jonkoping-to-Varnamo extrapolation, or any hygiene step. "Manufacturers' range and consumption figures are not used" points at the data source but the quote carries none anyway.
- quotation_bev_tractors_2027.pdf: harmless. Capacity (630 installed, 540 usable), price, delivery; no range or consumption. The 540 vs fleet register 468 usable is a real difference between models, resolved by FES-2 2.3, not a trap sentence.
- prompt: harmless. It asks the count and assignment, pins the design day, FES-2, files and rounding (10 kWh). It names no method, comparison or step.

## Solver's-eye read

Reader 1, isolated Sonnet, medium effort, 2026-11-08, on target.zip f1a47765 (prompt and pack only):

Leak read (no solving). Files read: prompt, both PDFs, all five XLSX (every sheet, visible), heads of all CSVs.

1. Decisive step: no sentence names it. Closest are filed rules, not the step: FES-2 3.1 "Energy figures for planning are estimated from the company's own operating records of its battery-electric tractors. Manufacturers' range and consumption figures are not used for planning." and 4.3 (design day, 85 per cent of usable battery). These say the source and threshold, not how to model load, temperature and Jonkoping-to-Varnamo transfer. Verdict on whether that is too much help: see Q5.

2. No file ranks or scores the Varnamo candidates. fleet_plan_2027.xlsx is only the shortlist (14 duties, days/week, charger). The BEV summary gives Jonkoping per-day energy and consumption, which are raw records, not per-duty verdicts. Quotation gives capacity only, no consumption or range.

3. Helper-only files: none are readmes or dictionaries. route_register_2026.xlsx carries the "Duty (before 13 Apr 2026)" rename column, which is a join aid (weighbridge uses VMO-nn codes), natural in a register. shipper_register is a plain lookup. No notes file.

4. Answer-like names or figures: none. The only figures that read as hard numbers are standard and quote parameters (minus 5 C, 85 per cent, usable 540 kWh), which are inputs. No tractor count anywhere.

5. Filed sentences that fix the computation:
- FES-2 2.1/2.2: duty = depot-out to depot-in round trip per the route register; energy = battery draw, as the tractor's own battery system reports it (fixes the unit and the energy basis: battery-side, not diesel-equivalent or manufacturer).
- 4.1: design day = working day at a mean ambient of minus 5 C (fixes the temperature condition).
- 4.2: planning load = mean net payload of the duty's departures over the twelve months to the end of the last full month before assessment (fixes the load and window; the assessment date is not stated in the file, only "each autumn", so the window end is inferred from the Oct 2026 data/quote date; likely the fork table's job).
- 4.3: assigned when energy is no more than 85 per cent of usable battery of the model ordered; each duty takes one tractor (fixes the threshold, the battery denominator and the count rule).
- 2.3 + quotation: usable battery = manufacturer-stated usable energy, 540 kWh quoted; fleet_register states a different battery for the existing Jonkoping units (540 installed, 468 usable). The ordered model is the quoted one.
- 3.1: planning energy from the company's own BEV records, not manufacturer figures.
The ordering and arithmetic of the threshold is fully filed. The model for energy given load, temperature and distance is not.

6. What decides the main answer: an analytical choice. A solver must build a per-duty energy model from Jonkoping BEV records (energy vs distance, ambient, load via TMS payload), extrapolate to Varnamo duties (different distances, climb, tare differences, payload from weighbridge with declared vs measured), at minus 5 C, then apply the filed rule. The rule application itself is mechanical (4.3), but nothing in the files states how to get energy for a Varnamo duty; the BEV summary has no payload, no duty or route, so the load and route link must be reconstructed from TMS (declared_weight, mixed units like "9 350 kg") and fleet registers. Risk: much of the difficulty is cleaning (units, rename, tare), and the final step after the model is a filed threshold; if the model is simple, the decision may reduce to rule application plus cleaning. Not a leak, a design note for the author.

Flagged files:
- fleet_electrification_standard_FES-2.pdf: harmless. It files the estimand and the rule, which determinism requires; it does not name the energy model, the temperature or payload dependence, the Jonkoping-to-Varnamo extrapolation, or any hygiene step. "Manufacturers' range and consumption figures are not used" points at the data source but the quote carries none anyway.
- quotation_bev_tractors_2027.pdf: harmless. Capacity (630 installed, 540 usable), price, delivery; no range or consumption. The 540 vs fleet register 468 usable is a real difference between models, resolved by FES-2 2.3, not a trap sentence.
- prompt: harmless. It asks the count and assignment, pins the design day, FES-2, files and rounding (10 kWh). It names no method, comparison or step.

Reader 2, the same brief, 2026-11-08, on target.zip ce9fbb1b (after the forum noun changed in FES-2 and the prompt):

Leak read, reader6 (no solving done)

1. Decisive step: no sentence names it. Closest: FES-2 3.1 "Energy figures for planning are estimated from the company's own operating records of its battery-electric tractors. Manufacturers' range and consumption figures are not used for planning." This fixes the source of evidence, not how to model it (temperature, payload, distance, climb, Jonkoping-only fleet carried to Varnamo duties). Method is left open.

2. No file ranks or scores the duties. bev_daily_summary has per-day energy and consumption for Jonkoping BEVs only; the route register has km and climb; the quotation has battery size. None states a duty energy or a feasibility verdict.

3. Helper-only files: none in the sense of readme/dictionary/notes. fleet_plan_2027.xlsx is the shortlist (needed, not a hint). Shipper register and fleet register are plain reference data. Quotation and FES-2 are governing documents, not method guides.

4. Nothing reads as the answer. No duty count, no kWh per duty, no verdict anywhere. The only near-figures are 540 kWh usable (quotation), 85 per cent and minus 5 C (FES-2), all inputs.

5. Filed sentences that fix the computation (in words only):
- FES-2 2.2 "A duty's energy is the energy the tractor draws from its battery for the round trip, depot out to depot in ... as the tractor's own battery system reports it." Fixes the quantity as battery-reported round-trip energy.
- 4.1 "working day with a mean ambient temperature of minus 5 degrees Celsius." Fixes the design temperature.
- 4.2 "mean net payload of its departures in the twelve months to the end of the last full month before the assessment." Fixes the payload population and window (assessment date is autumn 2026, so the last full month is the pack's final one).
- 4.3 "no more than 85 per cent of the usable battery of the tractor model being ordered. Each duty assigned takes one tractor." Fixes the threshold and that tractor count equals assigned duties.
- 2.3 and the quotation "usable capacity 540 kWh" fix the ordered model's usable battery; the fleet register's "468 kWh usable" for the existing Jonkoping model is a different model (a contrast, not a leak).
- 3.2 no road charging, so each duty is a single depot-to-depot charge.
These are rule statements about the estimand; they do not say how to estimate energy for Varnamo duties from Jonkoping data.

6. What decides the answer: an analytical choice. Energy per duty must be modelled from the Jonkoping BEV log (temperature, load, distance/climb, and extrapolation to longer Varnamo duties and to a larger battery model), with payload per duty derived from weighbridge records (gross minus tare, declared weights as a distractor) and net of tare gaps. Rule-following (FES-2) is the frame but the cutoff sensitivity comes from the fit. Mild data-semantics risk: usable 468 vs 540, and old duty codes VMO-nn vs Vnn.

Flagged file verdicts:
- fleet_electrification_standard_FES-2.pdf: harmless. It files the estimand and thresholds; no figures or method.
- quotation_bev_tractors_2027.pdf: harmless. Supplies battery size and price; "usable 540" is a necessary input. Sentence "Your existing fleet portal account will show the new tractors' daily summaries as it does for the Jonkoping tractors" is texture. Its 24 Sept meeting reference is dated before the setting.
- prompt.txt: harmless. Pins question, deliverables and rounding; names no method. It does say "under FES-2", pointing to the governing standard, which is fine.

Architecture 6, 2026-11-09, isolated Sonnet reader on target.zip 9d65a333 (a fresh copy of prompt.txt and target/
only).
1. How to do it: FES-2 4.2 and 4.3 (the planning load's population and window, the 85 per cent test against the
   ordered model): filed conventions, the WHAT; the forecast and the loss estimate left open.
2. Ranking file: none; the shortlist carries no score, energy or verdict.
3. Helping file: none; every file is an operational register or governing document.
4. Answer figure or name: none; the 540 and 520 kWh capacities are inputs.
5. Literal sentences: FES-2 4.2 (each duty's own departures, the trailing twelve months, gross less tare), 4.3 (the
   ordered model's usable battery), 2.3 (the loss share from the company's own tractors), 4.1 (-5 C, inside the
   observed range): each fixes the population or the target, none a figure; executed, they give the golden's basis.
6. One thing: none; the planning load is assembly, the energy, the payload coefficient and the loss are each
   separate estimation, and only the final verdict is the filed rule applied to them.
Sweep rulings: the quotation's 540 kWh harmless (the ordered model's specification); the shared words of the call
harmless (the topic's ordinary nouns); the shell quota harmless (a style fingerprint, no disclosure).
