# leak check, task8

**Verdict: REVIEW.** 16 files read, 91 golden figures and 25 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, reader, golden, missed, reflex, sitting, sittings, students, carried, family, second, standard, graded, readers, population, policy, screened, measurement, points, evidence, landed, register, device, regression, beside

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `lexis_technical_summary.pdf`: golden figure 212 appears: ...isation Standard age scores were set in 2019 on 4,212 students in 168 maintained schools and academies...

## 4 design-note vocabulary (REVIEW 4)
- **REVIEW** `brightway_technical_summary.pdf`: 3 of 25 stump-paragraph terms appear (standard, measurement, points); read whether the document names the move
- **REVIEW** `lexis_technical_summary.pdf`: 5 of 25 stump-paragraph terms appear (sitting, students, standard, measurement, points); read whether the document names the move
- **REVIEW** `quill_technical_summary.pdf`: 3 of 25 stump-paragraph terms appear (students, standard, population); read whether the document names the move
- **REVIEW** `reading_forward_policy_2026.pdf`: 5 of 25 stump-paragraph terms appear (sitting, students, second, standard, policy); read whether the document names the move

## 6 ranking artifacts (REVIEW 3, INFO 5)
- **REVIEW** `brightway_results_2026.xlsx`: names 5 of 25 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `cognitive_profile_tests_2026.csv`: names 11 of 25 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `lexis_results_autumn2026.csv`: names 14 of 25 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `academies.csv`: names 21 of 25 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `attendance_y7_autumn2026.csv`: names 21 of 25 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `census_year7_2026-10-01.csv`: names 21 of 25 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `reading_forward_sessions_2025-26.csv`: names 21 of 25 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `y7_settling_in_survey_2026.csv`: names 21 of 25 answer-set candidates; confirm it does not rank them on the decision question

## 8 column names (REVIEW 1)
- **REVIEW** `quill_session_log_2026.csv`: columns a generator names and an organisation does not: correct

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'xlsx' at 22% of 18 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 16 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)


## Solver's-eye read (architecture 19, the cut pack of 2026-11-11, one isolated reader at medium effort)

Files read: prompt.txt; all 16 files under target/ (academies.csv, attendance_y7_autumn2026.csv,
brightway_results_2026.xlsx, brightway_technical_summary.pdf, census_year7_2026-10-01.csv,
cognitive_profile_tests_2026.csv, ks2_results_2026.csv, lexis_results_autumn2026.csv,
lexis_technical_summary.pdf, quill_results_2026.csv, quill_roster_map.csv, quill_session_log_2026.csv,
quill_technical_summary.pdf, reading_forward_policy_2026.pdf, reading_forward_sessions_2025-26.csv,
y7_settling_in_survey_2026.csv). All four PDFs read in full (pdftotext). All CSVs and the xlsx opened and
profiled with python3/openpyxl (headers, row counts, joins, hidden sheets/rows/cols/comments/defined names,
value-type scans).

### 1. Sentence/file that tells HOW vs one that fixes WHAT

Nothing in the pack tells the solver *how* to estimate anything statistically (no named method, formula,
weighting scheme, regression, or lookup table for converting one test's score to another). What the policy
(`reading_forward_policy_2026.pdf`) does is fix a series of **WHAT** facts: the population, the scale, the
selection rule and the threshold. For example:

- "**A student's entry reading is their reading at the start of Year 7, on the Lexis 2019 standardisation (the
  Lexis basis), as a whole standardised score.**" (2.1), fixes the target scale (WHAT), says nothing about how
  a Quill or Brightway score is translated onto it.
- "**It is taken from the student's first valid sitting of an entry reading test after the May 2026 KS2 tests. A
  sitting is valid when the test was completed; a Quill session is valid when the student answered at least 24
  questions.**" (2.2), fixes which sitting counts (a selection rule over existing records, not a method for
  deriving a new figure).
- "**A student on roll who has no valid sitting by the census is placed from their KS2 reading scaled score, at
  the whole Lexis score of equal reading at the start of Year 7.**" (2.4), fixes the fallback population and
  target scale, not the conversion method.
- "**A Year 7 student joins Reading Forward when their entry reading is below 85.**" (3), a literal threshold
  rule (WHAT), unambiguous as worded (strictly below 85; "85" itself does not join).
- "**Each academy is given 0.4 tutor hours a week for each Reading Forward student, for the 36 teaching weeks of
  the year.**" ... "**costed at the trust's reading tutor rate, £27.80 an hour for 2026-27 including on-costs.**"
  (4), a stated arithmetic rule for converting a headcount into hours and cost; this part genuinely *is*
  mechanical once the headcount is known, so the hard work is entirely upstream in getting the headcount right.
- "**Version 2 (September 2024) placed students on their own academy's test, on a standardised score below 85.**"
  (6), fixes the OLD comparison basis the prompt asks the solver to reconstruct and compare against; it still
  has to be recomputed from the raw per-student test files, not looked up.

No sentence anywhere names an equating method, a conversion formula, which file to join to which, or how to use
the standard error of measurement. The three test technical-summary PDFs (Brightway, Lexis, Quill) describe each
test's standardisation sample, scale and reliability (SEM / alpha) as **inputs** a solver would need to build a
measurement-uncertainty band, they do not tell the solver to build one, or how.

### 2. File that already ranks/scores the academies on the question

None. Every file is either individual-student-level (one row per student per test/attendance-week/survey
response) or trust-wide historical (the policy's "last October's 848 Reading Forward students... £339,500"
figure is a trust total, not broken out by academy, and is explicitly last year's). No file contains a
per-academy count of Reading Forward joiners, tutor hours, or cost for 2026-27; no file pre-sorts or scores the
21 academies against each other on this question. Aggregating by academy is work the solver has to do.

### 3. File that exists only to help the analyst

No file in the pack is a pure "dictionary/readme" with no substantive content of its own:

- `quill_roster_map.csv` looks like a helper crosswalk (quill_student_id -> site_code, sis_id, name, DOB) but it
  is load-bearing: `quill_results_2026.csv` carries no UPN, so this file is the only path from a Quill result to
  a census student (via `sis_id`, which matches `census.admission_no` for 1,346 of 1,363 rows, a genuine,
  slightly lossy join, not a clean handed-over key).
- The three technical-summary PDFs carry substantive psychometric facts (standardisation year/sample, scale
  range, reliability/SEM) that are real analytical inputs, not just background.
- `academies.csv` states which test each academy uses, necessary scope information restating the prompt's own
  premise ("our academies don't all test..."), not a solution aid.

Nothing is a step-by-step "how-to" note.

### 4. Figure or name that reads as the answer rather than context

The policy's "**last October's 848 Reading Forward students**" and the associated "**£339,500**" provisional
budget read the most like a ready-made answer, but the text explicitly scopes them to last year ("last October's
... students", "the provisional 2026-27 budget, approved with this policy on last October's 848... students") and
separately says the board approves the final budget "on the October census numbers", i.e. this year's number,
not yet computed. A hurried reader could mistake 848/£339,500 for this year's figures; they are stated as prior-
year context, and the arithmetic in the policy (0.4 hrs/wk × 36 wk × £27.80 ≈ £400.32/student × 848 ≈ £339,500)
is internally consistent, which could reinforce reusing it, but it is not this year's census count. No other
figure or name in the pack reads as a ready-made answer; results/roster/session files are all raw per-student or
per-session data.

### 5. Filed sentence fixing how a graded figure is computed/over which population

- "**It is taken from the student's first valid sitting of an entry reading test after the May 2026 KS2 tests. A
  sitting is valid when the test was completed; a Quill session is valid when the student answered at least 24
  questions.**" (2.2) Literal reading: among a student's test attempts, discard any that are not "Complete"
  (Lexis has a `status` field; 17 of 2,830 Lexis rows are "Incomplete") and, for Quill, discard any session where
  fewer than 24 items were logged, **regardless of the vendor's own status field**. I checked this: every one
  of the 1,437 rows in `quill_results_2026.csv` is marked "Completed", but counting rows per `session_id` in
  `quill_session_log_2026.csv` shows 45 of those 1,437 sessions logged fewer than 24 items (as few as 10).
  Trusting the roll-up file's "Completed" label instead of the item log would silently include invalid sittings.
  Then take whichever valid sitting is earliest by date. This matters: 62 Lexis-tested students have 2 or more
  Lexis rows (some Incomplete-then-Complete, some an earlier July sitting and a later September one), so "first
  valid" is a real per-student sort-and-filter, not a single lookup.
- "**A student on roll who has no valid sitting by the census is placed from their KS2 reading scaled score...**"
  (2.4) This sentence has two defensible literal readings that I believe give different answers for a small
  number of students: (a) "by the census" gates which sittings exist for this purpose, so a sitting dated after
  1 October 2026 does not count and such a student falls to the KS2 fallback even though a test score for them
  is physically present in the files; or (b) 2.2's "first valid sitting... after the May 2026 KS2 tests" has no
  upper bound, so any valid sitting, whenever dated, is used. I checked the dates: `lexis_results_autumn2026.csv`
  and the Brightway workbook both include sittings dated up to 2-5 October 2026 (after the 1 October census), and
  exactly 1 Lexis-tested student and 1 Brightway record have their only dated sitting after 1 October (0 for
  Quill). So the ambiguity is real but touches a negligible number of students in this cut, not a load-bearing
  fork.
- "**A Year 7 student joins Reading Forward when their entry reading is below 85.**" (3) is unambiguous (strict
  "<85"), in contrast to the in-year exit rule's different wording, "**leaves the programme at a re-assessment
  when their reading reaches 85**" (5), but the exit rule is about January/June review, outside what the prompt
  asks for, so it is context only, not a second reading of the October threshold.
- Sections 2.1/2.3 fix WHAT the output scale is (a whole Lexis-basis standardised score) but leave HOW a
  Quill or Brightway score becomes that figure completely open, that open method is the central judgment call
  the prompt's "whether they join" and the Quill/Brightway correspondence-table ask are built on.

### 6. Is there ONE thing that would make most of the prompt routine?

No single fact does this. The closest candidate is section 6 of the policy: "**Year 7 at the Brightway academies
also sit Lexis in September 2026, to put Brightway results on the Lexis basis.**" This is written down (not a
hidden/undocumented factor), and I confirmed it in the data: `lexis_results_autumn2026.csv` contains exactly the
9 Lexis-native URNs plus the 5 Brightway URNs (no Quill URNs at all), and most (not all) census students at each
Brightway academy have a matching Sept-2026 Lexis row, a genuine, slightly incomplete, within-student paired
sample (I checked whether the small unmatched tail at each Brightway academy is systematically higher- or
lower-scoring than the matched group; the averages move in different directions academy to academy on small
counts, i.e. it reads as ordinary absence noise, not a built-in selection effect). Noticing this only unlocks the
Brightway side of the Quill/Brightway-to-Lexis correspondence table (half the table, 5 of 21 academies), it says
nothing about Quill, which has no Lexis sitting anywhere in the pack and needs a different route (e.g. via the
universal KS2 test as a common anchor), and it settles none of: the valid-sitting/first-sitting logic, the
Quill-session item-count check, the no-sitting-and-no-KS2 exclusion (144 census students have no KS2 row at all),
the eligibility count, the tutor-hour/cost arithmetic, the cost range, or the v2-vs-v3 own-test comparison. So it
rescues at most one slice of one of the sub-asks, not "most" of the task.

Breaking down what each part of the prompt turns on:
- **Reading one field / applying a stated rule**: which students are in scope (on roll at the census); a
  Lexis-native academy's entry-reading figure once the valid sitting is picked (it already *is* the Lexis basis,
  no conversion); the <85 threshold; the tutor-hours and cost arithmetic once a headcount exists; the old (v2)
  comparison rule's definition.
- **Catching something that could be misapplied (a stated procedure, not a planted trap)**: the Quill
  "Completed"-but-under-24-items sessions; the duplicate/incomplete Lexis sittings requiring "first valid";
  the "by the census" vs "after May 2026 KS2" date-window reading in 2.4.
- **Genuine analysis**: building the Lexis-equivalent for Brightway students (from the real paired sample) and
  for Quill students (no paired sample exists for Quill at all); handling the no-sitting/no-KS2 exclusion
  population; turning the tests' stated SEM/reliability into a defensible cost range; and reconstructing the old
  v2 per-academy, own-test counts from the raw files to compare against the new v3 Lexis-basis counts.
I found no planted defect, decoy, copied block, or mislabelled column (one string value, `'Standardised score'`,
that an early automated scan of mine flagged in the Parkgate sheet turned out to be that sheet's own column
header, which sits one row lower than the other four Brightway sheets because Parkgate carries an extra note row
,  real layout drift, not a planted anomaly).

### Machine-generated / construction tells

Content reads as authentic throughout: varied real-looking DOB formats across the Brightway sheets (`28 Dec
2014`, `12.05.15`, `10/01/2015`...), an inconsistent preamble length in one Brightway sheet (Parkgate has an
extra note row the others lack, shifting its header down one row), `<70`/`abs` non-numeric cells in the
Brightway score column exactly matching that test's own stated reporting floor, partial/incomplete joins
everywhere (Quill roster-to-census match rate ~98.8%, Brightway name-match ~93-96%, 144 census students with no
KS2 row, 66 KS2 "A"(bsent)/1 "B" code rows), and a cognitive-ability file covering only 11 of the 21 academies.
No lorem-ipsum/placeholder/TODO text, no stray references to this being a task or to any AI tooling, no residual
formulas in the xlsx, no hidden sheets/rows/columns/comments/defined names. PDF metadata is internally consistent
and era-appropriate (LibreOffice Writer, creation dates matching each document's own stated history: Brightway
2017, Lexis 2023, Quill Nov 2024, the policy 9 July 2026). The xlsx's docProps show distinct human
creator/lastModifiedBy names and a genuine Microsoft Excel application tag with shared strings. One purely
forensic (not content-visible) tell: every internal zip member of `brightway_results_2026.xlsx` carries the
generic epoch timestamp 1980-01-01 00:00, which is what a scripted zip/xlsx writer leaves when it doesn't
override it; a native Excel save normally stamps real save times on those internal parts. This isn't visible to
a solver reading cell values and reveals nothing about the task's content or intended difficulty, but it is a
construction tell at the zip-metadata level worth a human look.

### Flagged-file verdicts

- **brightway_results_2026.xlsx, cognitive_profile_tests_2026.csv, lexis_results_autumn2026.csv**, harmless.
  All three are individual-student rows carrying an academy name only as a school label, not an academy-level
  ranking or score. None aggregates to an academy comparison on tutor hours, cost, or eligibility.
  `cognitive_profile_tests_2026.csv` is additionally off-topic (verbal/quantitative/non-verbal/spatial cognitive
  ability, not reading) and covers only 11 of 21 academies, reads as a plausible unlabelled distractor.
- **quill_session_log_2026.csv**, harmless. Header `session_id, item_seq, item_id, correct, seconds,
  answered_at` is a plausible real adaptive-test item log (sequence, item id, right/wrong, response time,
  timestamp); nothing in the names is overtly synthetic, and the file is substantively necessary (it's the only
  place the true per-session item count lives, since the roll-up file's status field doesn't reflect the
  policy's 24-question validity rule, see Q5).
- **reading_forward_policy_2026.pdf, lexis_technical_summary.pdf**, harmless; both hold stated inputs, not
  answers. The policy's only numbers are rates/durations (0.4 hrs/week, 36 weeks, £27.80/hour) and a historical,
  explicitly-dated prior-year total (848 students / £339,500), see Q4. Lexis's numbers (4,212 students, 168
  schools, 2019, mean 100/SD 15, range 69-141, alpha 0.93, SEM 4.0) are that test's own psychometric properties,
  inputs for a measurement-uncertainty band, not a figure for this year's population.
- **prompt.txt**, reads naturally. 768 characters, one plain first-person paragraph, states the question and
  the requested deliverables, names no method/comparison/step/file/author role, gives no rounding instruction.

### Main thread's rulings

- Question 5's fork on sittings after the census: same call; three of the four students with an October sitting have an earlier valid one, and the fourth is placed the same either way (KS2 at 101, the October Lexis at 97); SF12 records it.
- The workbook's zip members on 1980-01-01: the dialect Excel itself writes for an .xlsx's parts, which the house writer reproduces; audit_containers passes; harmless.
- Policy section 6, the closest candidate to one thing: it files which data link Brightway (the WHAT) and leaves the trial's order and its gain to be found; it touches the Brightway half of one table and nothing at the Quill or July academies.
- The prior year's 848 students and £339,500: stated inputs (metadata stated_inputs), the provisional budget the recommendation prices against.
