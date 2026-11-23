# leak check, task28

**Verdict: REVIEW.** 14 files read, 104 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: reflex, physical, composite, triage, membrane, support, process, measurement, cutoff, diagnostics, independent, client, builds, lagrangian, alignment, cip-invariant, distinct, parcel, inversion, monitor, rigorous, seawater, hydraulic, deconvolution, variable-flow

## 3 answer figures in the pack (REVIEW 4)
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 360 appears: ...Scaling (parcel > 1.50 & > 1.50 index) Clause 2.2 360 EUR/h Persistent Structural Membrane Fault Clause...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 540 appears: ...h Persistent Structural Membrane Fault Clause 2.3 540 EUR/h Total 2027 Schedule B exposure sums across...
- **REVIEW** `swro_integrity_standard_q27.pdf`: golden figure 420 appears: ...eate Boron (> 0.50 mg/L, 1-hour basis) Clause 2.1 420 EUR/h Pretreatment-to-RO Scaling (parcel > 1.50 &...
- **REVIEW** `swro_integrity_standard_q27.pdf`: carries 24 of 35 distinctive words of the committed call: "Pull four Barlavento SWRO trains for mandatory 2027 vessel overhaul under Standard SWRO-Q27's 400-hour threshold: TR07 ("

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `swro_integrity_standard_q27.pdf`: 11 of 25 stump-paragraph terms appear (physical, composite, triage, membrane, support, process); read whether the document names the move

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)

## Solver's-eye read

Isolated `leak-reader` Pass 2 read on fresh scratch copy (`/tmp/leak-task28-p2/`: `prompt.txt` and `target/` only; never solved):

- **Pass 1 realism fixes verified resolved (7/7):** `operating_plan_2027.csv` calendar hours and dispatch duty ratio (`calendar_hours_2026`, `baseline_output_2026_km3`, `scheduled_output_2027_km3`, `dispatch_duty_ratio_2027`, aligned with Annex B `R_duty`); `intake_tep_z_index` standardized algal-TEP precursor index (`> 1.50` relative to 2020-2025 coastal baseline); smooth opening burn-in rows on `ro_feed_header_15m_2026.csv`; `post_cip_monitoring_cycle_hours: 120` in `scada_bay_config_2026.json`; chronological `CIP-2026-0001..0178` wash IDs; `LIMS-26W52` weekly batch cap matching `lims_qa_certificate_2026.pdf`; clean single-period `"E.M."` in both PDFs.
- **Q1 (method/step announcement):** None for any of the three underlying physical reconstructions (composite boron deconvolution, variable-flow hydraulic transit alignment, or separating persistent structural faults from reversible bio-fouling). Literal Clause 4.4 pins the 2026 legacy screening baseline `H_inc_2026` required for the deterministic discrepancy metric; Clause 2.2 pins the 32-interval burn-in exclusion; `scada_bay_config_2026.json` holds `post_cip_monitoring_cycle_hours: 120`.
- **Q2 (pre-ranked candidates, Gate G):** `none`.
- **Q3 (helper-only artifact):** `none`.
- **Q4 (answer leak):** `none`.
- **Q5 (literal-rule execution):** All operational scope, calendar quarters, mode estimands, 400.0-hour threshold, QA precedence, Schedule B tariffs, discrepancy rate formula, Annex B projection equations, and Annex C CSV columns execute cleanly without ambiguity.
- **Q6 (single-thing / banned-stump check):** No single file, column, sentence, or planted trick makes the task routine; all three modes require independent, genuine physical analysis with clean date consistency across all 14 files.
- **REVIEW verdicts:**
  - Sweep 3 (`swro_integrity_standard_q27.pdf`, Schedule B tariffs `420/360/540` EUR/h and standard vocabulary): **harmless** (contractual unit tariffs and standard engineering context; zero train results or calls disclosed).
  - Sweep 4 (`swro_integrity_standard_q27.pdf`, 11 domain words): **harmless** (routine desalination engineering definitions and filing schema; zero estimation method named).
