# leak check, task20

**Verdict: REVIEW.** 14 files read, 40 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: managers, record, careful, statements, channel, carried, investment, reflex, benchmark, audited, dropped, missed, method, evidence, engine, period, fitted, plateau, hurried, section, shortcut, market, forecasting, results, support

## 1 file names (REVIEW 2)
- **REVIEW** `corrigan_hart_pacing_plan_2027.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `peer_endowment_survey_2025.xlsx`: a sheet named 'About': confirm it is the organisation's own notes and does not describe the data's columns or files

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `wexmoor_endowment_liquidity_policy_2025.pdf`: 7 of 25 stump-paragraph terms appear (managers, record, investment, benchmark, evidence, section); read whether the document names the move
- **REVIEW** `wexmoor_investment_policy_statement_2024.pdf`: 4 of 25 stump-paragraph terms appear (managers, investment, period, support); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `corrigan_hart_pacing_plan_2027.xlsx`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 32% of 22 prompts (cap 30%); deliverable set 'docx+xlsx' at 23% of 22 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read (architecture 5, pass 1: the cut before the term-end release, minimum reserve USD 1,200 million)

Isolated Sonnet reader at medium effort, fresh copies of prompt.txt and target/ only, 2026-11-13.

### 1. Sentences or files that tell you how a step should be done

The reader quoted the liquidity policy's sections 2 to 9 (the eight quarters from 1 January of the budget year; net cash needs as spending plus calls less distributions, pending funds in full, the part not called at term end released; the reserve factors by class, holdings not revalued along the stress; the pass rule and the minimum; the stress path; the distribution rule with the late-statement fallback; section 8 leaving the calls open, "Capital calls are those the endowment's managers can be expected to make in the stress, judged on the evidence the Office of Investments holds", with no formula; section 9's program rule), the investment policy statement's spending formula and the capital plan's "No project draws on the endowment beyond the annual distribution the trustees approve."

### 2. A file that ranks or scores the candidates

None: the plan's Programs sheet lists the four programs' funds and totals only; no sheet carries a reserve, headroom, stress or pass figure beside a program.

### 3. A file that exists only to help the analyst

None: the plan's Notes sheet and the survey's About sheet are the organisations' own cover notes; neither explains columns or joins.

### 4. A figure or name that reads as the answer

None.

### 5. Filed sentences that fix a computation, read literally

Section 4 (the reserve at each class's factor on 31 December values); section 7 (each fund's 31 December value times its strategy's benchmark rate in the matching quarter); section 3 (pending funds' commitments in full; a fund stops counting as a need once its term ends: 11 register funds have term ends in 2027-28, and the statements show the pattern, e.g. WX-BO-107's final statement of 2025-09-30, "final statement; commitment not called released"); section 9 (the largest total that passes, or none); section 8 produces nothing numeric. The holdings report's "Policy liquidity class" column already sorts every holding into section 4's classes.

### 6. One thing, and what each part turns on

No single unlock: section 9 settles only the last step once each program's pass or fail is known. The program and the headroom turn on analysis (the stress build, with the calls left open by section 8); the distributions on section 7's stated procedure; the commitments not yet called on reading fields with hygiene. It read "the headroom above the minimum reserve over 2027 and 2028" as possibly asking for an interim checkpoint against the one cumulative threshold.

### Realism

Nothing machine-made in the PDFs or workbooks (metadata varied and plausible, no hidden content, no boilerplate); one tell: the activity file's portfolio companies named "<fund name> portfolio 01", "02" and so on.

### Rulings (main thread, 2026-11-13)

- Question 1: every quoted sentence is a governing clause the endowment would write (the policy's rules, the IPS's spending rule, the capital plan's statement of its own draws); section 8 keeps the calls' method open. Harmless.
- Question 5, section 3's release: the golden and the world's own 2027-28 kept calling funds after their terms ended; fixed in the generator (SF18): both now stop at the term's end, the policy's distributions unchanged. The headroom rose by USD 10.7 million and the minimum reserve moved to USD 1,150 million to keep the call centred.
- Question 5, the liquidity classes: the Office assigns them in the holdings report (section 4 says so); a filed convention earned by the careful pass. Harmless.
- Question 6, the headroom over 2027 and 2028: fixed in the prompt ("over the eight quarters of 2027 and 2028"), one cumulative figure as section 5 defines the test.
- Realism, the company names: fixed in the generator; the managers' reports now name each company, property, infrastructure asset or borrower (no figure moved).
- Mechanical sweep lines ruled by the main thread: the plan's Notes sheet and the survey's About sheet are the organisations' own notes; the Programs sheet lists the candidates without ranking them; the policy's and the investment policy statement's shared words are their own rules ("supports the university's teaching", the benchmark named for distributions only); the register's dates after March 2027 are its forward-looking period and term ends and expected closes; the minimum reserve is a stated input (metadata.json stated_inputs).

## Solver's-eye read (architecture 5, pass 2: the final cut, minimum reserve USD 1,150 million)

Isolated Sonnet reader at medium effort, fresh copies of prompt.txt and target/ only, 2026-11-13.

1. How-to sentences: the liquidity policy's sections 3 to 9 as filed (section 8 leaves the calls open: "Capital calls are those the endowment's managers can be expected to make in the stress, judged on the evidence the Office of Investments holds"); the holdings report's "Policy liquidity class" column, which section 4 says the Office assigns; the statements' "final statement; commitment not called released" notes on 19 liquidated funds' last rows.
2. Ranking: none; the Programs sheet lists the four nested programs with their funds and totals only.
3. Helper files: none; the plan's Notes sheet, the survey's About sheet and the holdings report's closing line ("Private funds at capital account value are reported separately (capital account statements).") are the organisations' own notes.
4. Answer-shaped figures or names: none.
5. Literal sentences: section 9 (the largest total that passes, or none), section 4 with the class column (the reserve at each assigned class's factor, not revalued along the stress), section 3 (pending funds in full).
6. One thing: none; the calls are left open by section 8 and need the benchmark, the register, the activity file and the audited borrowings. Two readings flagged: "the headroom above the minimum reserve over the eight quarters of 2027 and 2028" as one figure or a per-quarter path; the half-year calls and distributions with or without a strategy split.
Realism: clean (LibreOffice exports with distinct authors and dates, Excel workbooks with shared strings and their own creators, the Tilsworth rebrand and the restated 2024-06-30 pair read as plausible drift, no LLM phrasing).

### Rulings (main thread, 2026-11-13)

- Questions 1 to 5: governing clauses and the organisations' own notes; harmless (as pass 1).
- The headroom's two readings: closed in the prompt with "taken together" (section 5 defines one test over the eight quarters); voice-check and leak.py re-run on the change.
- The strategy split on the half-year asks: no fork on a graded figure (the asks grade the totals in each half; a split carries them); no change.
