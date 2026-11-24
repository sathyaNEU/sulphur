# leak check, task28

**Verdict: REVIEW.** 15 files read, 117 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: physical, deconvolution, cutoff, misses, post-cip, permeate, two-path, reflex, overhaul, desalination, shortcut, mass-flux, continuous, shared-bay, variants, operating, scaling, static, re-growth, kinetic, process, diagnostics, protocol, swro-q, textbook

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 420 appears: ...g/L, 1-hour basis; 2nd-pass polishing) Clause 2.1 420 kWh/h Pretreatment-to-RO Scaling (RO header > 1.5...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 360 appears: ...(RO header > 1.50 & > 1.50; TMP drag) Clause 2.2 360 kWh/h Persistent Structural Membrane Fault (bypas...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 300 appears: ...reakthrough (> 450 mg/L, 1-hour basis) Clause 2.4 300 kWh/h Total 2027 excess desalination energy penal...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 540 appears: ...Membrane Fault (bypass recirculation) Clause 2.3 540 kWh/h Permeate Salinity / TDS Breakthrough (> 450...
- **REVIEW** `swro_integrity_standard_q27.pdf`: carries 32 of 39 distinctive words of the committed call: "Schedule five Barlavento SWRO trains for 2027 pressure-vessel overhaul under Engineering Protocol SWRO-Q27's 400-hour en"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `lims_qa_certificate_2026.pdf`: 3 of 25 stump-paragraph terms appear (permeate, continuous, process); read whether the document names the move
- **REVIEW** `swro_integrity_standard_q27.pdf`: 11 of 25 stump-paragraph terms appear (physical, permeate, overhaul, desalination, continuous, operating); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 15 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 13 task metadata (REVIEW 2)
- **REVIEW** `metadata.json`: files.operating_plan_2027.csv.covers shares the design note's stump vocabulary (operating, scaling, process): say what the task decides, not how
- **REVIEW** `metadata.json`: files.swro_integrity_standard_q27.pdf.covers shares the design note's stump vocabulary (physical, overhaul, desalination, diagnostics, protocol): say what the task decides, not how

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated grounded `leak-reader` Pass 7 read on fresh scratch copy (`/tmp/leak-task28-p7/`: `v3.2` `prompt.txt` [`4b10b0cc7528dc0c3b63afbc52d99eae`] and fresh unzip of `target.zip` [`436d94cd2e76581db4b8097808e9a735`] only; grounded verbatim on `prompt.txt` and `BDM-ENG-Q27-2026`; never solved):

- **Verdict:** **PASS** (zero leaks, zero method announcements, zero Clause 4.4 / raw-alarm discrepancy clauses, zero `post_cip_monitoring_cycle_hours` / `120 h` window hint in `scada_bay_config_2026.json`, zero negative or sub-LOQ boron composite readings, zero flat hydraulic flow clamping, accurate Lisbon wall-clock `shift_code` alignment across WET/WEST DST transitions, realistic `0.4-0.9 h` inline CIP flush durations, and SCADA historian supervisor separated from CIP technician rotation).
- **Q1 (method/step announcement):** `none`. Neither `prompt.txt`, `swro_integrity_standard_q27.pdf`, `lims_qa_certificate_2026.pdf`, nor `scada_bay_config_2026.json` announces or hints at any statistical or physical estimation method for any of the four 2026 failure modes.
- **Q2 (pre-ranked candidates, Gate G):** `none`.
- **Q3 (helper-only artifact):** `none`. Every file serves an authentic municipal desalination engineering, lab QA, SCADA/MES telemetry, or unlabelled regional utility context role (`mibel_iberian_power_spot_2026.csv`, `algarve_reservoir_levels_2026.xlsx`).
- **Q4 (answer leak):** `none`.
- **Q5 (literal-rule execution):** Clauses 1.2, 2.1 to 2.4, 3.1, 4.1 to 4.3, Annex A, and Annex B fix populations (`TR01..TR08` across North/South Bays), 2026 UTC calendar quarters, opening 32-interval burn-in, all four physical mode estimands, 400.0 h independent overhaul criterion, Clause 4.3 excess energy rates (`420 / 360 / 540 / 300 kWh/h`, reported in `MWh`), uniform Annex A 2027 projection equations, and Annex B 9-column historian CSV schema without ambiguity.
- **Q6 (single-thing / banned-stump check & realism):** `none`. All four failure modes require independent physical/statistical inference across disjoint multi-grain logs. Sampled boron composites are strictly above the `0.020 mg/L` LOQ (`min = 0.0453 mg/L` across all 15,024 clean rows, verified mechanically); hydraulic flows are smooth and non-clamped (`max_flow_repeat = 2`); `shift_code` matches Lisbon local hours across WET, WEST, and both 2026 DST transitions; CIP flushes span `0.4-0.9 h` with `Duarte Monteiro` separated from CIP logs; and `algarve_reservoir_levels_2026.xlsx` passed all mechanical leak and container audits cleanly.
- **REVIEW verdicts:**
  - Sweep 3 & 4 (`swro_integrity_standard_q27.pdf`, Clause 4.3 energy rates `420 / 360 / 540 / 300 kWh/h` and standard domain vocabulary): **harmless** (governing engineering standard defining WHAT is evaluated and reported; zero estimation methods or train answers leaked).
  - Sweep 4 (`lims_qa_certificate_2026.pdf`, domain words `permeate, continuous, process`): **harmless** (authentic ISO/IEC 17025 lab QA certificate documenting repeatability SDs, `0.020 mg/L` LOQ, and QA revision precedence; zero method announcements or answer leaks).
  - Sweep 13 (`metadata.json`, domain words `operating, scaling, process, physical, overhaul, desalination, diagnostics, protocol`, ruled in parent thread): **harmless** (internal task metadata describing scope only, never shipped to solvers, zero method hints).
