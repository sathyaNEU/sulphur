# leak check, task19

**Verdict: REVIEW.** 16 files read, 69 golden figures and 3 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: missed, residents, interval, follow-up, result, linkage, accounts, factor, births, independence, measured, listed, correct, independent, careful, method, shortcut, dual-system, population, linked, entries, matcher, raising, checks, dismissed

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `LGGC_2026-14_grant_determination_population_basis.pdf`: golden figure 3.2 appears: ...of the pool in proportion to its usual residents. 3.2 Districts near the threshold. Where the Office's...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `LGGC_2026-14_grant_determination_population_basis.pdf`: 3 of 25 stump-paragraph terms appear (residents, interval, population); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'docx+xlsx' at 33% of 18 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 16 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## Solver's-eye read

One isolated reader (general-purpose, sonnet, medium effort) read prompt.txt and the 16 files of the cut pack in a scratch copy and nothing else. Its answers, condensed with its quotations:

1. **Method-telling text:** none in the prompt. The circular (`LGGC_2026-14_grant_determination_population_basis.pdf`) files the estimand and the grant rule: the usual-resident definition ("lived in Kilvarra for at least twelve months, or had arrived intending to stay ... students in full-time education are counted at their term-time address, and serving members of the Defence Forces at the base where they are stationed"), the postcode-directory assignment of addresses to districts, and paragraph 3.2's interval rule. The reader: "These pin the target definition and the classification rule only. They do not name an estimator."
2. **A file ranking the districts on the question:** none. The register and list-size files give raw counts and nothing ranks them against 25,000; the accounts workbook gives only the national rolled-forward total.
3. **A file that exists only to help:** none. The practice and postcode lookups are ordinary reference tables; the blocks file's selection probabilities are design information a survey ships with.
4. **A figure that reads as the answer:** none. The nearest is the accounts' 325,624, which the prompt itself calls the rolled-forward estimate (context, not an answer); no district figure appears anywhere.
5. **Filed sentences fixing a graded figure:** the postcode-directory rule (districts by the directory as at 30 June 2026), the usual-resident definition (students at term-time addresses, personnel at their base), and paragraph 3.1 and 3.2 (qualifies at 25,000 or more; an interval straddling 25,000 is unconfirmed and paid at half rate). Each is the estimand's WHAT, executed literally by the golden.
6. **One thing that makes most of it routine:** "none is evident". The estimates and intervals rest on the survey, its design and the follow-up; the call on the intervals; the two bridges on the register, border, student and defence files; the coverage share on the survey-to-register match. Knowing that the register over-counts "would settle only part of this". Rule-following appears only in the circular's classification rule and the definition; "nothing here looks planted".

**Review lines.** Answer-figure sweep: harmless; the matched number in the circular is its own paragraph number and the filed threshold, which say nothing about any district's estimate. Design-note vocabulary (residents, interval, population): harmless; they are the estimand's own words in the circular's definition and rule, and the circular names no method. Shell quota (docx+xlsx at 33 per cent of recent prompts): open, decided at stage 5.

**Realism notes and their disposition.**
- The life table's male qx jumps at 17 (0.000253 to 0.000877) and falls at 35 (0.001924 to 0.001452): a real graduated table has neither. Fixed in the generator: a smooth Heligman-Pollard schedule (childhood decline, an accident hump peaking near 21, Gompertz).
- Names mix origins within a person and against their citizenship ("Klaus-Michael Olivier", citizenship ES): fixed in the generator, each person's names now come from their citizenship country's own names. While fixing it, the survey's citizenship was found drawn apart from the border file's nationality for the same person: the survey now records the person's own citizenship.
- The census age profile is smooth with similar band sizes under 20: judged plausible for a mature island population, unchanged.
- The register sorted by practice and registration date: the extract's real export order, unchanged.
- Uniform selection probability within a district's blocks: a stratified design, unchanged.
