# leak check, task24

**Verdict: REVIEW.** 15 files read, 68 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: troubleshooting, labels, missed, volume, policy, golden, information, reviews, forecast, hurried, section, shortcut, bridge, result, method, judgments, reviewed, counted, ceiling, graded, record, agreement, constant, cheapest, vantorra

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `tallyfield_order_TF-PEN-2027-Q1.pdf`: golden figure 600 appears: ...s. Ticket type Comparisons Orders and delivery 47,600 Returns and refunds 35,600 Account and billing 30...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `launch_policy_DL-03.pdf`: 10 of 25 stump-paragraph terms appear (labels, volume, policy, reviews, forecast, section); read whether the document names the move
- **REVIEW** `tallyfield_order_TF-PEN-2027-Q1.pdf`: 3 of 25 stump-paragraph terms appear (troubleshooting, volume, section); read whether the document names the move
- **REVIEW** `tallyfield_quality_summary_2026.pdf`: 3 of 25 stump-paragraph terms appear (volume, judgments, record); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `reward_model_runs.xlsx`: columns a generator names and an organisation does not: tallyfield_device_troubleshooting, ardentdesk_device_troubleshooting

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'docx+xlsx' at 21% of 24 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 15 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## Solver's-eye read

**1. Sentences fixing a step, comparison, adjustment, grouping, population or window**

- `launch_policy_DL-03.pdf` sec. 2: "Every pair counts, whatever the split of the three choices." Fixes the accuracy metric's population (no pair dropped).
- sec. 3: "...expected to reach 81.0 per cent accuracy on the planned 2027 ticket mix: each ticket type's accuracy weighted by its share of the tickets the 2027 operating plan forecasts for the year." Fixes the weighting window: the full 2027 year, not Q1 alone.
- sec. 4: "A usable comparison is one in which the judge preferred one of the two replies ... is not used in training." Fixes which rows count.
- sec. 5: "the purchase is the cheapest one with which the Q1 2027 model's expected accuracy reaches the bar." Fixes the decision rule.
- `ardentdesk_quote_AD-Q-2611-07.pdf` sec. 1: "Pairwise reply comparisons on device troubleshooting tickets by Ardentdesk's device-support team..." Fixes the new purchase as device_troubleshooting only; the 2026 pilot spanned all five.
- `tallyfield_order_TF-PEN-2027-Q1.pdf` sec. 3: "Option comparisons are drawn ... in the same proportions by ticket type as section 1..." Fixes the option's split.
- `tallyfield_quality_summary_2026.pdf` sec. 3: "Batches TF26-022 to TF26-024 were exported again after the move; the second exports repeat the first." Names a duplicate-row mechanism.
- The prompt: "give each vendor's error rate against the standard by ticket type" fixes the comparison and grouping, pointing at `label_audit_2026.csv` unnamed.

**2. File that ranks or scores the candidates**

None scores the prompt's 2027 scenarios. `reward_model_runs.xlsx` carries three vendor-mix ablations (RM-11 "Ardentdesk only", RM-19 "Tallyfield only", RM-17 "Tallyfield cut to 30k"), each with an `is25_agreement_pct`, inviting a vendor ranking at face value, but on IS25 (single Tallyfield judgments, guideline v2), not the three-technician standard, and historically rather than forward.

**3. File that exists only to help the analyst**

None cleanly: closest is `draftline_eval_config.yaml`, which reads as the pipeline's own working config (owner, last-changed stamp, scorer version), not analyst scaffolding. Three of its lines, the label source, the no-preference requeue rule, the retry-new-job-id rule, are filed nowhere else, needed to read `eval_results_by_item.csv` correctly.

**4. Figure or name that reads as the answer rather than context**

Closest is `shadow_reviews`' `accuracy_vs_standard_pct` in `reward_model_runs.xlsx`, already in the graded unit. Not the answer: only seven runs (RM-02 to RM-16, never RM-22), overall not by type, from 2026 draft reviews, not a 2027 scenario. No cell, column or sentence names a recommended vendor or quantity.

**5. Filed sentences fixing a graded figure** (main list under 1; two more):
- `tallyfield_quality_summary_2026.pdf` sec. 1: "Comparisons completed include 'no preference' judgments." Fixes that Tallyfield's "completed" volume is a larger population than the "usable" count DL-03 sec. 4 defines for training.
- `launch_policy_DL-03.pdf` sec. 7.2: "A reward model that always preferred the better reply would reach, on a ticket type, the share of the type's pairs on which the standard's reply is the better one, plus half the share of pairs whose replies are as good as each other. Forecast accuracy against the standard is read on that basis." Fixes the graded figure as the curve read through that ceiling.

**6. One unlocking thing?**

I ran no cross-tabs or plots, only schema and row counts, so a distributional pattern could exist unseen. No single file, sentence or column collapses the ask. By part:

- Vendor error rate by ticket type: real analysis (`label_audit_2026.csv` is the only file where all three sources judge the same 2,000 pairs), plus decoding Ardentdesk's `chose`/`shown_left` into the A/B label the others use.
- Per-type expected accuracy and the 80 per cent range: real analysis, fitting 7.1's curve through 7.2's ceiling, T's measurement and the IS25-to-standard bridge both left open (below).
- The 2027 mix's blended accuracy: mechanical once per-type figures exist, per sec. 3's weighting rule.
- The cheapest purchase and its cost: mostly rule application on filed vendor terms (sec. 5), though weighing Tallyfield's locked proportions against Ardentdesk's single-type offer is a real comparison.

**Section 7 (Forecasting accuracy), specifically**

It does not say how to count T. It fixes T's grouping (per ticket type, not pooled) and the parameter structure ("K ... fitted for each ticket type and b ... fitted for all ticket types together"), but never T's units or vendor weighting; the yaml's "training_counts: usable comparisons by vendor and ticket type" is the closest filed candidate, with no sentence weighting it into T. Ties match the standard half the time, the curve's stated value, not a floor. Sec. 7.2 (quoted in 5) runs the curve through a ceiling from the standard's rate on the better reply, a filed step, not optional; left open is estimating each type's tied share from the votes.

Nor does it relate IS25 agreement to the standard: sec. 7.1 says only "Accuracy is forecast from the record of past training runs," without naming which record, though seven runs carry both `is25_agreement_pct` and `accuracy_vs_standard_pct` with no sentence mapping one to the other. The only filed facts on why they might diverge: the yaml's benchmark-label and no-preference-requeue lines, and the quality summary's note that guideline v3 replaced v2 from 5 January 2026.

It says nothing about replies' lengths anywhere in the pack; `reply_a_words`/`reply_b_words` appear only as columns in five CSVs.

Section 7 reads as a forecasting convention, a stated curve, a stated ceiling, a point forecast a range does not move, not instructions handing over the analysis: it fixes the curve and ceiling, never what feeds them.

### Rulings (2026-11-13, on the read after DL-03 section 7 was filed)

- Section 7: read as the organisation's forecasting convention (the curve, its ceiling, the point forecast); it fixes nothing that feeds the curve (the training signal's measure, the internal set's bridge to the standard, the pull to the longer reply), so J1 to J3 are untouched. Harmless.
- Q1 and Q5 (sections 2 to 5, the quote's and the order's terms, the quality summary's re-exports): the WHAT and the Layer 1 mess as filed before this fix. Harmless.
- Q2, the run register's vendor ablations with their internal-set agreement: historical, on the internal set's crowd labels and not the standard, and no 2027 option scored; unchanged by this fix and read by the earlier reader and judge. Harmless.
- Q3, the evaluation config: the pipeline's own working config, unchanged. Harmless.
- REVIEW lines (the order's 600, the policy's and the summaries' plain vocabulary, the register's per-type column names, the prompt's shell quota): read and harmless.
