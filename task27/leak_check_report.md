# leak check, task27

**Verdict: REVIEW.** 17 files read, 68 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: conservation, handoff, physical, coldstore, reefer, reflex, drayage, stock-flow, pallet, rigorous, weighbridge, c-days, import, same-vessel, causes, containers, inland, unload, independent, golden, shared-train, direct, locked, chamber, wagons

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `weserfrucht_remediation_charter_rc2027.pdf`: carries 29 of 36 distinctive words of the committed call: 'Release 2027 Mandatory Remediation funding under Charter RC-2027 (>= 2,500 container-days) for five causes: vessel_berth'

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `weserfrucht_remediation_charter_rc2027.pdf`: 11 of 25 stump-paragraph terms appear (handoff, physical, coldstore, reefer, drayage, import); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `weserfrucht_remediation_charter_rc2027.pdf`: names 3 of 3 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 17 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

(Pass 2 cold isolated read of `/tmp/leak-task27/`, 2026-11-22)

### Questions 1-6

1. **Method or step announcement:** `prompt.txt`: none (states only the business question, the 2,500 container-day threshold reference, requested quantities, and deliverable types; names no attached files, rounding rules, or analytical steps). `weserfrucht_remediation_charter_rc2027.pdf` pins only corporate WHAT governance rules (Section 2.1 settled scope, revision supersession, UTC vs Europe/Berlin zones, entity crosswalk; Section 2.2 exhaustive 8-cause originating-bottleneck estimand without naming which stages hold misattributed dwell or how to untangle them; Section 3 2,500 cutoff on 2027 Annex C projections excluding 2026 documentary dispute settlements; Section 4.1 Schedule B EUR tariffs excluding bunker fuel and LKW-Maut; Section 4.2 calendar quarters and full-network BHV/HAM/Q3 scope; Annex C uniform cause-level 2027 projection formulas; Section 5 CSV schema). All other 16 files: none.
2. **Pre-ranked candidates (Gate G):** none. (`carrier_dispute_closeout_2026.xlsx` tabulates unprojected 2026 documentary TMS-stage commercial claims in unsorted lifecycle order; Charter RC-2027 lists tariffs and symbolic equations in lifecycle order without scoring causes.)
3. **Helper-only artifact:** none. Every shipped file serves an authentic operational, commercial, regulatory, or planning role.
4. **Answer leak:** none. No file contains attributed 2026 root-cause totals, projected 2027 container-days, 2027 EUR figures, or committed remediation designations.
5. **Literal-rule execution:** Every literal Charter RC-2027 clause (Section 2.1 `SETTLED` + max `extract_version` + excess hours / 24; Section 2.2 exhaustive 8-cause partition; Section 3 `>= 2,500.0` cutoff on 2027 Annex C; Section 4.1 Schedule B EUR tariffs; Section 4.2 non-leap quarters & full-network BHV/HAM/Q3; Annex C single uniform cause-level equation; Section 5 eight-row CSV schema) executes cleanly to the golden.
6. **Single-thing / banned-stump check & realism tells:** No single-thing shortcut. Attributing 2026 excess container-days turns on genuine multi-source operational diagnosis across independent systems (per-chamber WMS stock-flow vs aggregate DC occupancy and port yard dwell; consignment-level CHED BIP notices vs rail shuttle departures and weighbridges; unlinked empty-depot portal rejections vs physical gate logs and drayage turnaround).

### Realism & Date Consistency

- **Setting date boundary (`<= 2027-01-19`):** Clean across all 17 files; zero dates after `2027-01-19`, zero template leftovers, zero artificial answer-order sorting.
- **Chronology, DST & physical plausibility:** Exact Europe/Berlin `+01:00`/`+02:00` DST transitions reconciled to UTC; zero container chronology inversions; DC capacities and opening stocks tie to 0 pallets; reefer weights, pallet counts, multi-consist Vectron BR-193 rail blocks, Autobahn distances, and Maut tariffs are physically and commercially plausible. Minor cohort-boundary notes (Jan 5-14 empty tail in `depot_portal_requests_2026.csv`, planned-shuttle keying of `rail_shuttle_departures_2026.csv`) are benign simulation boundaries.

### REVIEW Item Verdicts

- **Sweep 3 (`weserfrucht_remediation_charter_rc2027.pdf`, decision vocabulary overlap):** `harmless` - Governance definitions (`REMEDIATE`, `MONITOR`, `2,500 container-days`, eight canonical `cause_id` tokens) only; zero answer leak.
- **Sweep 4 (`weserfrucht_remediation_charter_rc2027.pdf`, design-note vocabulary; ruled by main thread):** `harmless` - Appearing terms (`handoff`, `physical`, `coldstore`, `reefer`, `drayage`, `import`, `containers`, `inland`, `unload`, `direct`) are ordinary supply-chain operational nouns required by Charter stage definitions; Charter never mentions any stump mechanism (`chamber saturation`, `pull-back`, `same-vessel`, `24-hour lock`, `empty wagon`, `weighbridge`, `portal quota`, `retry multiplicity`).
- **Sweep 6 (`weserfrucht_remediation_charter_rc2027.pdf`, candidate causes beside numbers):** `harmless` - Numbers beside causes are strictly Schedule B tariffs, Table 1 free-time hours, and Annex C parameters in lifecycle order; zero ranking or scoring.
