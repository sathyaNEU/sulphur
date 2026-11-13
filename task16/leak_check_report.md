# leak check, task16

**Verdict: REVIEW.** 13 files read, 37 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: groups, architecture, agreement, chance, engine, overlays, missed, priced, result, nothing, checks, delivery, careful, golden, closed, configuration, results, population, linked, specification, weight, lesson, review, january, counts

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `one_chart_empi_conversion_plan.pdf`: carries 3 of 3 distinctive words of the committed call: 'Run Rule B at the One Chart conversion:'
- **REVIEW** `patient_identity_policy_him-14.pdf`: carries 3 of 3 distinctive words of the committed call: 'Run Rule B at the One Chart conversion:'

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `halvard_match_6_specification.pdf`: 6 of 25 stump-paragraph terms appear (chance, engine, linked, specification, weight, review); read whether the document names the move
- **REVIEW** `one_chart_empi_conversion_plan.pdf`: 3 of 25 stump-paragraph terms appear (engine, review, january); read whether the document names the move
- **REVIEW** `patient_identity_policy_him-14.pdf`: 4 of 25 stump-paragraph terms appear (overlays, result, results, review); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 13 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### 1. Sentences that dictate how a part of the analysis should be done
- HIM-14 section 3: "Automatic linking may be enabled at the conversion only under a rule whose expected false merges are no more than one per 2,000 automatic links, counting each pair of records the rule would join. Where more than one rule meets this, the conversion uses the rule that joins the most pairs; where none does, every link is made after HIM review." The eligibility test and the tie-break, once each rule's figures are known.
- Conversion plan 7.2: "Each candidate rule is applied to every pair of active records in the two indexes, across and within each index, as the indexes stand at the conversion; the 2 November 2026 extracts are the planning baseline." Fixes the comparison population (active records, within- and cross-index) and the snapshot date.
- Match 6 spec section 1 gives the standardization steps (case-fold names, USPS-reduce addresses, 10-digit phone, 9-digit SSN with all-zero/all-nine as missing) both indexes must pass through before any rule is applied.
- Match 6 spec section 3: "Candidate pairs are drawn by birth date, by SSN, by phone and by the first four letters of the last name with the birth year" describes the engine's own blocking keys.

### 2. File that ranks or scores the candidate rules
None. No file scores or ranks rules A-D against each other or names a recommended rule. `halvard_pilot_review_2026.xlsx` scores individual candidate *pairs* (SCORE 19.2-30.9, a human HIM_DECISION of Same patient/Different patients/Cannot determine) under the engine's separate weighted-score mechanism, not under rules A-D, and carries no rule-level tally.

### 3. File that exists only to help the analyst
None found; everything reads as a plausible business or system artifact (policy, conversion plan, vendor spec, merge log, pilot QA log, blood-bank and L&D operational logs). The two furthest from load-bearing are `registration_volumes_2024-2026.xlsx` and `rosario_duplicate_report_summary_2025-2026.xlsx`, both monthly aggregates with no patient-level key, so neither can be joined to a specific rule's output; they read as plausible distractor candidates rather than analyst crutches.

### 4. Figure or name that reads as the answer rather than context
The closest is the Match 6 spec's closing line: "At the national reference rates, two different people agree on first name, last name, birth date and sex with a chance of about one in 10 billion pairs." That sentence is reproduced from the weight table's own u-values (first/last/DOB/sex "Different"-complement rates), and the same table lets the same style of figure be built for rules B and D by one more multiplication. No rule name, memo line, or column is flagged "recommended," "answer," or similar.

### 5. Filed sentence whose literal execution fixes a figure or population
- HIM-14 section 3 (quoted above): literal execution, once the four rules' false-merge figures exist, mechanically picks the rule (highest-volume rule clearing the 1-per-2,000 bar, or "manual" if none clears it). It fixes the selection step, not the figures feeding it.
- The "about one in 10 billion" sentence: taken literally, it lets a solver report a national-reference collision chance as the false-merge estimate for rule A (and, by the same multiplication, B and D) without ever touching either patient index. In words, that would produce a reassuringly small, population-blind rate, not a figure grounded in this hospital's own name, address and birth-date overlap.
- Conversion plan 7.2's "every pair of active records": literal execution fixes the universe as active records only, which is not a column in either index and must be read off `calder_bay_merge_history` (a record retired into a survivor is no longer active).

### 6. Is there one thing that makes most of the task routine?
No. The HIM-14 tie-break only consumes already-computed rule-level false-merge figures; nothing states those figures for any rule. The "one in 10 billion" shortcut reaches only 3 of 4 rules (not rule C's OR/fuzzy logic), and describes national randoms rather than this population if taken at face value, so it is a plausible wrong turn, not an answer. Per ask: automatic-link counts under A-D turn on analysis (standardizing and comparing ~312,000 records at scale, including rule C's equivalence-table/Jaro-Winkler/OR logic), not a single field read. The false-merge estimate per rule turns on analysis; no filed figure exists for any rule against this population, and the national u-values are a tempting but non-local shortcut. Distinct patients in the converted index turns on analysis, sequenced behind the overlay split HIM-14 section 4 requires first. Patients already held by both indexes is its own cross-system question, stated nowhere. Calder Bay overlays turn on detection, since no column flags one; it must be built from inconsistencies across files, no single one labelled as the signal. Residual duplicates after the chosen rule's links turn on analysis, chained from the rule choice.

### Realism
All three PDFs show Producer "LibreOffice" / Creator "Writer" with distinct creation timestamps (Apr, Jun, Oct 2026), consistent with real exports. Facility names are varied and plausible (CB Bayside/Main/North; RMG Rosario/Children's), not flat placeholders. A spot check found no all-zero/all-nine SSNs in the Calder Bay index and no `LAST_ACTIVITY`/`LAST_ENC_DT` dates after the 2 Nov 2026 extract in either index. The pilot review file (986 rows, three decision categories including a small "Cannot determine" bucket, varied reviewer initials and dates) reads as genuine QA output. The merge history mixes MANUAL (HIM initials) and AUTO (REGSVC) merges across two decades, a realistic operational mix. One cross-document wrinkle: conversion-plan rule C's Jaro-Winkler cutoff (0.92) is stricter than the Match 6 spec's own "Similar" band (0.88 or more), so the spec's u-value for "Similar" is not a drop-in rate for rule C's narrower band. Both figures are stated plainly, so this reads as a real mismatch between a committee's chosen rule and a vendor's generic calibration, not a planted defect.

No leak found.

Read on the cut target.zip 7eeb799edc9c9775 (2026-11-12) by one isolated reader at medium effort, given only prompt.txt and a fresh unzip of target.zip.

### The main thread's rulings on the REVIEW lines

- Sweep 3, the plan and the policy carry the words of the call (Rule, B, One Chart conversion): the plan defines the four rules and the policy governs the conversion; neither ranks a rule. Harmless.
- Sweep 4, the specification (chance, engine, weight) and the policy (overlays, result, results, history): the engine's own weights document and the policy's definitions and record keeping; neither names a step. Harmless.
- Reader question 5, "active records": both index extracts hold active records only, so the plan's population executes as the files stand; the merge history adds evidence, not rows. Harmless.
