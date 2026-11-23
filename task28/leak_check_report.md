# leak check, task28

**Verdict: REVIEW.** 14 files read, 104 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: physical, reflex, overhaul, engineering, process, scaling, composite, support, standard, measurement, triage, operating, structural, swro-q, cutoff, independent, anomalous, protocol, client, builds, lagrangian, alignment, cip-invariant, distinct, parcel

## 3 answer figures in the pack (REVIEW 5)
- **REVIEW** `mibel_iberian_power_spot_2026.csv`: golden figure 111.53 appears: ...IBEL,106.16,EUR/MWh 2026-11-11T21:00:00Z,PT_MIBEL,111.53,EUR/MWh 2026-11-11T22:00:00Z,PT_MIBEL,97.88,EUR/M...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 360 appears: ...ng (parcel > 1.50 & > 1.50; TMP drag) Clause 2.2 360 kWh/h Persistent Structural Membrane Fault (bypas...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 420 appears: .../L, 1-hour basis; 2nd-pass polishing) Clause 2.1 420 kWh/h Pretreatment-to-RO Scaling (parcel > 1.50 &...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 540 appears: ...Membrane Fault (bypass recirculation) Clause 2.3 540 kWh/h Total 2027 excess desalination energy burde...
- **REVIEW** `swro_integrity_standard_q27.pdf`: carries 37 of 43 distinctive words of the committed call: "Schedule four Barlavento SWRO trains for 2027 pressure-vessel overhaul under Engineering Protocol SWRO-Q27's 400-hour en"

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `lims_qa_certificate_2026.pdf`: 3 of 25 stump-paragraph terms appear (process, composite, standard); read whether the document names the move
- **REVIEW** `swro_integrity_standard_q27.pdf`: 16 of 25 stump-paragraph terms appear (physical, overhaul, engineering, process, scaling, composite); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 13 task metadata (REVIEW 2)
- **REVIEW** `metadata.json`: decision shares the design note's stump vocabulary (overhaul, engineering, protocol): say what the task decides, not how
- **REVIEW** `metadata.json`: files.swro_integrity_standard_q27.pdf.covers shares the design note's stump vocabulary (physical, overhaul, engineering, protocol): say what the task decides, not how

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Isolated `leak-reader` Pass 3 read on fresh scratch copy (`/tmp/leak-task28-p3/`: reframed `prompt.txt` and `target/` only; never solved):

- **Pass 3 reframing verification:** Confirmed zero leftover compliance, EUR penalty, audit, or Schedule B contradictions across `prompt.txt`, `swro_integrity_standard_q27.pdf` (`BDM-ENG-Q27-2026`), `operating_plan_2027.csv`, `lims_qa_certificate_2026.pdf`, and all other shipped files (`algarve_reservoir_levels_2026.xlsx` verified clean mechanically with zero legacy terms).
- **Q1 (method/step announcement):** `none` for any estimation method or analytical step (boron composite deconvolution, variable-flow Lagrangian parcel alignment, or 3-state CIP-invariant latent-class separation). Clause 4.4 pins the legacy baseline `H_inc_2026` required for the deterministic discrepancy metric; `scada_bay_config_2026.json` records `post_cip_monitoring_cycle_hours: 120`.
- **Q2 (pre-ranked candidates, Gate G):** `none`.
- **Q3 (helper-only artifact):** `none`.
- **Q4 (answer leak):** `none`.
- **Q5 (literal-rule execution):** Every graded population, UTC quarter boundary, mode estimand, 400.0-hour overhaul criterion, Clause 4.3 excess desalination energy penalty (`420 / 360 / 540 kWh/h`, reported in `MWh`), Clause 4.4 discrepancy formula, Annex B 2027 multipliers, and Annex C plant historian CSV schema (`energy_2027_mwh`) executes cleanly without ambiguity.
- **Q6 (single-thing / banned-stump check):** `none`; all three physical modes require independent multi-step physical/statistical inference with consistent 2026 calendar, weekday, and `Europe/Lisbon` DST transitions.
- **REVIEW verdicts:**
  - Sweep 3 & 4 (`swro_integrity_standard_q27.pdf`, Clause 4.3 energy rates `420/360/540 kWh/h` and domain terms): **harmless** (governing engineering protocol defining modes, criterion, energy penalty rates, and output schema; zero method announced, zero train figures leaked).
  - Sweep 4 (`lims_qa_certificate_2026.pdf`, routine terms `process, composite, standard`): **harmless** (accredited ISO/IEC 17025 lab QA certificate).
  - Sweep 3 (`mibel_iberian_power_spot_2026.csv`, row `2026-11-11T21:00:00Z`, `111.53 EUR/MWh`): **harmless** (incidental overlap inside an ordinary 8,760-row wholesale power price series).
  - Sweep 13 (`metadata.json`, domain words `overhaul, engineering, protocol, physical`): **harmless** (internal task metadata describing scope only, zero method hints).
