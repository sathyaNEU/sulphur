# leak check, task28

**Verdict: REVIEW.** 14 files read, 105 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: physical, overhaul, scaling, two-path, composite, reflex, desalination, mixing, dual-recipe, hydraulic, variant, process, operating, membrane, protocol, swro-q, conductivity, support, bimodal, diagnostics, independent, excess, fickian, struct, hourly

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `mibel_iberian_power_spot_2026.csv`: golden figure 109.17 appears: ...IBEL,105.63,EUR/MWh 2026-03-22T20:00:00Z,PT_MIBEL,109.17,EUR/MWh 2026-03-22T21:00:00Z,PT_MIBEL,107.44,EUR/...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 540 appears: ...Membrane Fault (bypass recirculation) Clause 2.3 540 kWh/h Total 2027 excess desalination energy penal...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 420 appears: .../L, 1-hour basis; 2nd-pass polishing) Clause 2.1 420 kWh/h Pretreatment-to-RO Scaling (RO header > 1.5...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 360 appears: ...(RO header > 1.50 & > 1.50; TMP drag) Clause 2.2 360 kWh/h Persistent Structural Membrane Fault (bypas...
- **REVIEW** `swro_integrity_standard_q27.pdf`: carries 33 of 39 distinctive words of the committed call: "Schedule four Barlavento SWRO trains for 2027 pressure-vessel overhaul under Engineering Protocol SWRO-Q27's 400-hour en"

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `swro_integrity_standard_q27.pdf`: 17 of 25 stump-paragraph terms appear (physical, overhaul, scaling, composite, desalination, process); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 13 task metadata (REVIEW 2)
- **REVIEW** `metadata.json`: decision shares the design note's stump vocabulary (overhaul, membrane, protocol): say what the task decides, not how
- **REVIEW** `metadata.json`: files.swro_integrity_standard_q27.pdf.covers shares the design note's stump vocabulary (physical, overhaul, desalination, protocol, diagnostics): say what the task decides, not how

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated `leak-reader` Pass 4 read on fresh scratch copy (`/tmp/leak-task28-p4/`: `v2` `prompt.txt` and `target/` only; grounded on `BDM-ENG-Q27-2026`; never solved):

- **Verdict:** **PASS** (zero leaks, zero method announcements, zero Clause 4.4 / raw-alarm discrepancy clauses, zero legacy compliance/EUR/Schedule B leftovers across `prompt.txt`, `swro_integrity_standard_q27.pdf`, `lims_qa_certificate_2026.pdf`, `scada_bay_config_2026.json`, and all telemetry/lab/CIP CSVs; `algarve_reservoir_levels_2026.xlsx` verified mechanically clean with zero legacy/train terms).
- **Q1 (method/step announcement):** `none`. Neither `prompt.txt` nor any governing document states or hints at how to infer the three 2026 physical failure modes (no solute-flux coupling or composite support deconvolution, no two-path hydraulic mixing or conductivity lag method, no 4-state dual-recipe CIP latent-class separation).
- **Q2 (pre-ranked candidates, Gate G):** `none`.
- **Q3 (helper-only artifact):** `none`. Every file serves an authentic municipal desalination engineering or regional context role.
- **Q4 (answer leak):** `none`.
- **Q5 (literal-rule execution):** Clauses 1.2, 2.1 to 2.3, 3.1, 4.1 to 4.3, Annex A, and Annex B fix populations, 2026 UTC calendar quarters, opening 32-interval burn-in, mode estimands, 400.0 h independent overhaul criterion, Clause 4.3 excess energy rates (`420 / 360 / 540 kWh/h`, reported in `MWh`), uniform 2027 projection equations, and Annex B 8-column historian CSV schema without ambiguity.
- **Q6 (single-thing / banned-stump check & realism):** `none`. All three failure-mode forecasts require genuine independent physical/statistical inference; 2026 calendar, Thu-Mon 4h / Tue-Wed 8h autosampler schedule, `Europe/Lisbon` WET/WEST DST transitions, alternating `CIP_ALK_pH11` / `CIP_ACID_pH2` washes, technician shift rosters, sequential Annex A/B numbering, and physical sensor ranges are all coherent and plausible.
- **REVIEW verdicts:**
  - Sweep 3 (`mibel_iberian_power_spot_2026.csv`, row `2026-03-22T20:00:00Z`, `109.17 EUR/MWh`): **harmless** (ordinary evening-peak Iberian spot electricity price inside an 8,760-row regional market context table unused by Clause 4.3 MWh accounting).
  - Sweep 3 & 4 (`swro_integrity_standard_q27.pdf`, Clause 4.3 energy rates `420/360/540 kWh/h`, Annex A, Annex B, and general domain terms): **harmless** (governing engineering protocol defining WHAT is reported and validated energy rates; zero method announced, zero train figures leaked).
  - Sweep 13 (`metadata.json`, domain words `overhaul, membrane, protocol, physical, desalination, diagnostics`, ruled in parent thread): **harmless** (internal task metadata describing scope only, zero method hints).
