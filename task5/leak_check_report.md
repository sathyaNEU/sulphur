# leak check, task5

**Verdict: REVIEW.** 12 files read, 160 golden figures and 5 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: employers, report, quarter, worksite, outstanding, quarters, asserted, account, second, kittredge, closed, register, ostrom, careful, reading, earlier, garrow, design, family, accounts, records, replay, carried, cut-off, resolved

## 3 answer figures in the pack (REVIEW 3)
- **REVIEW** `ui_contribution_rate_notice_2027.docx`: golden figure -0.1 appears: ...4.00 -2.0 to -0.1 5.10 -4.0...
- **REVIEW** `ui_contribution_rate_notice_2027.docx`: golden figure 0.9 appears: ...3.20 0.0 to 0.9 4.00 -2.0...
- **REVIEW** `ui_contribution_rate_notice_2027.docx`: golden figure 3.0 appears: ...6.9 1.90 3.0 to 4.9 2.50...

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `community_transition_fund_act_2026.docx`: 9 of 25 stump-paragraph terms appear (employers, report, quarter, worksite, account, closed); read whether the document names the move
- **REVIEW** `ui_lmi_data_sharing_agreement_2025.docx`: 7 of 25 stump-paragraph terms appear (report, quarter, worksite, account, closed, earlier); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 33% of 15 prompts (cap 30%); deliverable set 'csv+docx' at 27% of 15 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 12 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Three isolated Sonnet readers at medium, 2026-11-10, each on a fresh copy of prompt.txt and target.zip, none shown the
design note, the generator, the answer blocks or this report's sweep lines. Each read for leaks and solved nothing.

### Read 3 (target.zip sha256 8f7854f965fb2bc7; the final cut, c238169b094ad50a, differs from it only by the two edits this read asked for)

1. How any part should be done. The reader was asked to separate what the files define from how anything not on file is
   worked out. What: the Act's 2(c) and 2(d) (the payroll period including the twelfth, the worksite's county, liability
   from the first day of covered employment "whether or not an account has been established"), 4 (minus 2.0 or lower,
   one decimal), 5(a) to 5(d) (the records "as they stand at the close of February 15", every employer "whether or not
   its contribution report ... has been received", the reported and estimated split, the published figure, the same
   estimate a year earlier, the employer list), and the agreement's Schedules A to D (report types, paper reports at
   00:00:00, held reports posted on establishment, "The contribution report is the record of an account's employment
   for the quarter", the worksite report "distributes the employment on the account's contribution report among its
   worksites"). How: "none. No sentence says how to estimate a missing report, impute, adjust, group, model or
   validate."
2. A file that ranks the counties: none. The published table gives December 2025 only.
3. A file that exists only to help: the county code list and the NAICS concordance (lookup tables); the agreement reads
   as a data dictionary in its schedules.
4. A figure or name that reads as the answer: none.
5. Filed sentences that fix a figure or a population: 5(a), 2(c) and 2(d), 5(b), 4, 5(c), Schedule A. Each executes to
   the golden's estimand.
6. One thing: the Act's whether-or-not clauses, which settle "that the estimation exists, but not the estimation itself,
   the as-of replay, the multi-worksite split or the reconciliation". "Nothing looks planted."

Review lines: the Act harmless (statutory wording, no step beyond the definitions); the agreement harmless (the worksite
sentence "borders on telling how to split"); the rate notice harmless (no figure coincides with an answer); the prompt
acceptable (one paragraph, question first, no file and no method).

Realism: names, public bodies, dates, metadata and the email (a note between two officials) read as real; no date
after 15 February 2027. Two edits asked for and made, neither moving a figure: an account named "State of Franklin"
with a 2019 liability date (the four state accounts now carry agency names), and the email's "the Act had thought of
that" (deleted; a deletion only, so no further read).

### Read 2, the second cut before the realism edits (sha256 eec3132c67fb5406)

No "do X" sentence, no ranking file, no answer figure. It listed the same clauses as rule application and data
semantics and read the frame (population, as-of, worksite allocation, the reconciliation's cause) as procedural and the
estimate for missing reports as open analysis; it asked for Schedule A's held-report sentence and Schedule D's
allocation sentence to be cut as process commentary. Realism: the email mirrored the deliverables and carried a
telephone number on a real area code; a state account read "University of Franklin Medical Center, Unit 2"; the
register's status date is written year first where its other dates are month first.

### Read 1, the first cut (sha256 5f5cda294e7b7b52)

No method sentence, no ranking file, no helping file, no answer figure, no one thing. Realism: the request read as
written for the analyst; sixteen government accounts in Calder shared one name; "Co. Co.".

### Rulings (main thread)

- The Act's clauses and Schedules A and D stay. Each files a WHAT the determinism spec requires filed (the population
  with its members not yet observed, the outcome, the as-of date, the base, the unit of account) and closes a fork
  (SF1, SF5, SF7, SF9); none says how a job not on file is estimated. Cut, Schedule A's sentence would leave a report
  received before its account existed readable two ways at every earlier cut-off, and Schedule D's would leave an
  employer's county jobs readable as the worksite report's own counts. Read 3, asked the what-or-how question
  directly, found no how.
- The reconciliation to the published table follows from the table's own footing and Schedule A, as read 2 says. It is
  R1, an assembly result the careful pass earns; nothing is priced on it.
- The agreement is the organisation's own governing document (who may use which records, for what); its schedules list
  the data elements the way such agreements do, in prose, and leak.py's describing-content sweep passes it.
- The register's year-first status date is the maintenance system's (the status history writes the same form) and
  Schedule B states no form for it: a benign oddity, kept.
- Fixed in the generator: the email (no deliverables, no section cited beyond 5, no telephone number), the state
  accounts' names, and from read 1 the public bodies' names and the doubled suffix.
