# leak check, task16

**Verdict: REVIEW.** 13 files read, 39 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: mismatches, delivery, documented, missed, linkage, careful, agreement, engine, chance, different, counted, holding, groups, history, closed, overlays, community, decade, overlay, national, stands, discordant, reflex, population, confirming

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `one_chart_empi_conversion_plan.pdf`: carries 3 of 3 distinctive words of the committed call: 'Run Rule B at the One Chart conversion:'
- **REVIEW** `patient_identity_policy_him-14.pdf`: carries 3 of 3 distinctive words of the committed call: 'Run Rule B at the One Chart conversion:'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `halvard_match_6_specification.pdf`: 4 of 25 stump-paragraph terms appear (engine, chance, different, national); read whether the document names the move
- **REVIEW** `patient_identity_policy_him-14.pdf`: 4 of 25 stump-paragraph terms appear (different, history, overlays, overlay); read whether the document names the move

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

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

1. No sentence tells the analyst how to estimate the false merge rate, the hard step. Two sentences fix scope only. Conversion plan (`one_chart_empi_conversion_plan.pdf`) 7.2: "Each candidate rule is applied to every pair of active records in the two indexes, across and within each index, as the indexes stand at the conversion; the 2 November 2026 extracts are the planning baseline." That fixes population and comparison, not method. The matching specification (`halvard_match_6_specification.pdf`) section 1 is the clearest "how": "names are upper-cased with accents and punctuation removed and hyphens read as spaces; a last name is compared as a whole and token by token; street addresses are reduced to house number, street name and suffix in USPS abbreviations, with unit designators removed; phone numbers to ten digits; SSNs to nine digits, with all-zero and all-nine values treated as missing." The plan invokes this by reference ("Fields are compared as the matching engine standardizes them"), so it is a stated comparison convention, not a hint on estimating false merges. Policy (`patient_identity_policy_him-14.pdf`) section 3 states the organisation's own selection rule: "Automatic linking may be enabled at the conversion only under a rule whose expected false merges are no more than one per 2,000 automatic links... Where more than one rule meets this, the conversion uses the rule that joins the most pairs; where none does, every link is made after HIM review." Already paraphrased in the prompt, it says how to choose among estimated rates, not how to produce them, so it is not an estimation hint.

2. None. No file scores or ranks Rules A to D against each other. The matching specification scores pairs by its own weighted scheme (sections 2 to 3) for the engine's routine linking, a different mechanism, never applied to this question.

3. None. Every file reads as a real organisational artifact: a policy, a vendor spec, a program plan, a pilot review, a merge history, a duplicate report, registration counts, blood bank results, death notices, a delivery log, and the engine's own name equivalence table (named "Name Equivalence Table v6" inside the spec it serves, so it is the engine's reference file, not an analyst crib sheet).

4. None found. No figure or name states a rule's link count, false merge count, or distinct patient count anywhere, and no row is labelled as the recommended rule or as an overlay or duplicate patient.

5. Three sentences fix scope or convention literally. Conversion plan 7.2 (quoted above): literally, test every pair within Calder Bay, within Rosario, and across the two 2 November extracts; the files already carry only non-retired MRNs (no MRN retired in `calder_bay_merge_history_2006-2026.csv` reappears in `calder_bay_patient_index_2026-11-02.csv`), so every row already counts as active. Policy section 3 (quoted above): literally, a rule qualifies only if its own false merges per 2,000 links is at or under 1; among qualifying rules the one with the most automatic links is named; if none qualifies, every link goes to HIM review and no rule is recommended. Policy section 2: "A record that also holds the information of another patient is an overlay" and "A patient held under more than one active record is a duplicate." Literally, "records already holding two or more patients" means overlays, and "patients still sitting under more than one active record" means duplicates counted after the chosen rule's links are applied.

6. No single thing settles most of the ask. The main call turns on the policy's selection rule once rates are known, a rule application, but the rates are analysis: no file hands over a false merge count for any rule, and the one HIM-reviewed sample (`halvard_pilot_review_2026.xlsx`) covers only pairs that already fell in the engine's own 19 to 31 review band, narrower than each rule's own criteria, so using it is inference, not lookup. Part by part: "each rule's automatic links" turns on reading the rule definitions and the standardization paragraph correctly at scale, not estimation. "Estimated false merges" and "false merges per 2,000 links" turn on analysis. "Distinct patients the converted index will hold" and "how many both indexes already hold" turn on analysis (clustering linked pairs, and finding pre-existing cross-index identity, which no file gives in full). "Whether any Calder Bay records already hold two or more patients" turns on catching an anomaly across files, not one field: nothing is flagged as an overlay anywhere, while `blood_bank_type_screen_2016-2026.csv` (a few MRNs carry more than one ABO value) and `calder_bay_merge_history_2006-2026.csv` (some survivor and retired identities disagree on name or birth date) carry raw signal that must be cross-checked, not read off. "Patients still under more than one record" and "links touching an overlay record" turn on analysis built on the prior results, not a new filed fact.

**Flags**
one_chart_empi_conversion_plan.pdf: harmless. No "recommend," "preferred," "ranked" or "passing" anywhere in its text; its only hits are generic ("will decide," "under which"), and it never says which of Rule A to D passes.
patient_identity_policy_him-14.pdf: harmless. Its hits are "approve" (the policy's own approval line) and the section 3 selection sentence, the organisation's general rule for picking among rates once known, already paraphrased in the prompt, naming no specific rule.

Verdict: NO LEAK. No file ranks, scores or names a recommended rule, states a false merge figure, or computes any part of the estimate; the two flagged files carry only generic policy and procedural language already echoed in the prompt.

### Main thread's rulings (2026-11-13, architecture 4, cut 4c1045ec)

- REVIEW 3, answer figures: the plan and the policy carry the words of the rules and the conversion because they
  define them; the reader found no rule marked recommended, passing, preferred or ranked. Harmless.
- REVIEW 4, design-note vocabulary: the specification's engine, chance and national rates are its own account of
  the engine's scoring (the incumbent figure the golden supersedes on Rule A); the policy's different, history and
  overlay words are its definitions of a false merge, a duplicate and an overlay. Neither says how to estimate a
  rule's false merges. Harmless.
- Reader Q1 and Q5, the specification's standardization and the plan's section 7.2: the comparison convention and
  the population each rule's links are counted on (a reflex the golden and the blocks follow, R80); executed
  literally they give the golden's links. The policy's section 3 is the decision rule the prompt names; it chooses
  once the rates are estimated and produces none of them.
- Reader Q6, the blood bank's records with two ABO values and the merge history's names that disagree: the raw
  evidence the overlay count is built from, which no column flags; analysis, as the reader says.
- An earlier read of cut b787faf9 (the same pack with a steering committee deciding) also found no leak; it read the
  specification's national rate as the figure closest to an answer, the incumbent's claim, and Rule C's 0.92 against
  the specification's 0.88 as two thresholds for two uses, each landing on the golden.
