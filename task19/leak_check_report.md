# leak check, task19

**Verdict: REVIEW.** 16 files read, 85 golden figures and 6 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: missed, follow-up, careful, result, accounts, linkage, factor, interval, matcher, measured, linked, correct, independent, emigration, method, shortcut, independence, corrected, population, births, benchmark, review, errors, misses, person

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `LGGC_2026-14_grant_determination_population_basis.pdf`: golden figure 3.2 appears: ...of the pool in proportion to its usual residents. 3.2 Districts near the threshold. Where the Office's...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `LGGC_2026-14_grant_determination_population_basis.pdf`: 3 of 25 stump-paragraph terms appear (interval, population, person); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `CS26_persons.csv`: 1 ISO dates after 2026-12-03, e.g. 2026-12-18

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 16 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


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

## Solver's-eye read

Two isolated reads (general-purpose, sonnet, medium effort), each of prompt.txt and the cut pack in a scratch copy and nothing else: round 1 on the pack judged at stage 4, round 2 on the final cut after the prompt named the register bridge's three parts, gave the range a unit and asked for the note as a PDF.

Round 2, condensed with its quotations:

1. **Method-telling text:** none that fixes a method. The circular's 3.2 ("Where the Office's 90 per cent interval for a district lies wholly at or above 25,000, the district qualifies. Where the interval includes 25,000, ... unconfirmed and pays half") is "a decision rule on the interval and says nothing about how to estimate it"; 2.2 and 2.3 "define the estimand"; the accounts' footnote ("rolled forward from the 2021 Census") "shows what the rolled-forward figure is, not how to correct it".
2. **A file ranking the districts on the question:** none; "no district has a 2026 usual-resident figure anywhere".
3. **A file that exists only to help:** none; the clerical review, the follow-up and the link study "are inputs to response and coverage measurement and have no explanatory text".
4. **A figure that reads as the answer:** none; the accounts' 325,247 is the rolled-forward figure, "context and not the answer, since the prompt asks for a different quantity".
5. **Filed sentences fixing a graded figure:** circular 2.3 (districts by the postcode directory), 2.2 (students at the term-time address, personnel at their base, the twelve-month rule) and 3.2 (the interval rule), each the estimand or the decision rule executed literally.
6. **One thing that makes most of it routine:** "none found". "A solver who guessed 'dual-system / coverage estimation' would still have much to do"; the estimates, intervals, probabilities and both splits "turn on analysis", the qualify and too-close split on the circular's stated rule applied to those intervals.

**Review lines.** Answer-figure sweep: harmless (the circular's own paragraph number and threshold). Design-note vocabulary: harmless ("interval", "population" and "person" appear only where the circular defines what is estimated). The date after the setting: a date of birth of 2026-12-18 in the survey's persons file, "a keying error (probably year or day-month swap) a real survey file can carry", harmless.

**Realism notes and their disposition.** A few name pairings read as mixed (an Indian surname with a Turkish forename form); the workbooks' zip entries carry the 1980-01-01 stamp Excel itself writes; the single barracks in the Defence Forces' return and the smooth official tables fit their sources. None changed the pack.

Round 1 (the stage 4 pack) answered the six questions the same way: no method sentence, no ranking or helper file, no answer figure, "none is evident" as one thing; its notes (the life table's step at 17 and 35, names mixed against their citizenship, the survey's citizenship drawn apart from the border file's) were fixed in the generator before the final cut.

## Solver's-eye read

Three isolated reads (general-purpose, sonnet, medium effort), each of prompt.txt and the cut pack in a scratch copy and nothing else: round 1 on the stage 4 pack, round 2 on the rebuilt pack with the prompt naming the register gap's three parts, round 3 on the final prompt that also asks for the rolled-forward gap component by component.

Round 3, condensed with its quotations:

1. **Method-telling text:** the prompt names no method; its nearest sentences name "the three parts of the register gap", point the national gap "at the accounts' columns" and name the survey-to-register share asked for. The circular's 2.2 "states a population rule, not a method" and 2.3 "a stated convention".
2. **A file ranking the districts on the question:** none; "no file lists district figures against 25,000".
3. **A file that exists only to help:** none; the blocks' selection probabilities are "a design file that is needed for the analysis".
4. **A figure that reads as the answer:** none; the accounts' 325,247 "is the stated baseline the prompt asks to be compared against, not the answer".
5. **Filed sentences fixing a graded figure:** circular 2.2 (the usual-resident definition), 2.3 (districts by the postcode directory) and 3.2 (the interval rule), each read literally as the estimand or the decision rule.
6. **One thing that makes most of it routine:** "no single file or sentence looks like it settles most of the asks"; the follow-up's outcome codes "would speed up the register-gap split but not the estimates, intervals or national bridge".

**Review lines.** Answer-figure sweep: harmless (the threshold and the circular's own numbers). Design-note vocabulary: harmless (the words only define what is estimated). The date after the setting: a date of birth keyed wrongly, "normal, and it does not reveal how the pack was made". The prompt's new wording: the three parts "a definition of the estimand rather than a step"; "component by component" "gives away no step and does not say which component is wrong".

**Realism notes and their disposition.** Street words repeat across households, some name pairings read as mixed, and the Defence Forces' return's small female counts read neat; none changed the pack. Rounds 1 and 2 answered the six questions the same way (no method sentence, no ranking or helper file, no answer figure, no one thing); round 1's notes (the life table's step at 17 and 35, names mixed against their citizenship, the survey's citizenship drawn apart from the border file's) were fixed in the generator before the final cut.
