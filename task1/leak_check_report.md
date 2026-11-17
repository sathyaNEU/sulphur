# leak check, task1

**Verdict: REVIEW.** 14 files read, 77 golden figures and 2 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: android, google, budget, applovin, stores, missed, export, accounts, twelve-month, charges, reports, networks, reflex, generator, record, auction, recorded, result, priced, account, graded, attribution, tracking, channels, charge

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `growth_policy_paid_channels_v3_2026-09.pdf`: 9 of 25 stump-paragraph terms appear (google, budget, stores, charges, record, account); read whether the document names the move

## 9 dates after the setting (REVIEW 1)
- **REVIEW** `media_plan_2027.xlsx`: 156 ISO dates after 2026-11-09, e.g. 2027-01-04, 2027-01-11, 2027-01-18, 2027-01-25, 2027-02-01

## 10 container metadata (REVIEW 1)
- **REVIEW** `target`: one author 'Rafa Naranjo' on 2 of 3 documents: files from different teams or bodies carry their own authors

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 3 file categories: document, spreadsheet, structured (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and the 14 files of the pack, 2026-11-16, on the
cut the judge read. It solved nothing and saw no design note, generator, answer block or report.

1. **A sentence or file that tells how the analysis is done:** none. The policy "fixes definitions, not a method": it
   quoted sections 2.1, 2.2, 2.6 and 4.1 and found that they "name no estimator, comparison or adjustment"; 2.2's "whether
   or not the attribution partner can name it" is "a population statement".
2. **A file that ranks or scores the candidates:** none. The policy gives the bands' lines only; no file carries a
   channel's return.
3. **A file that exists only to help the analyst:** none. The conversion-value file is "a bit-layout config that an app
   team would keep"; the budget workbook's change log is one a finance team would keep.
4. **A figure or name that reads as the answer:** none.
5. **Filed sentences that fix a computation or a population:** 1.2 (the plan's growth-sheet channels, Apple Search Ads
   outside), 2.1 (12-month net revenue per euro, the plan's 52 weeks at the plan's weekly spend as billed), 2.2 (first
   install of a new consumer account, one channel per install whether named or not), 2.3 (365 days from the install,
   store and web charges at the time of the transaction, refunds out), 2.4 (VAT by storefront, the stores' 15 per cent,
   the checkout's 3 per cent), 2.5 (the two prices, unchanged in 2027), 2.6 (one more euro, every week raised in
   proportion), 3.1 (the lines, on the return at the plan's spend), 3.2 (the four figures per channel), 4.1 (records to
   the start of November). **Main thread:** each is the estimand as the golden executes it, asserted sentence by
   sentence in `checks.py` (SF1 to SF22) and by the independent verifier; none names a step.
6. **One thing that makes most of it routine:** none. "The nearest candidate is the policy's definitions (2.2 to 2.4).
   They define the revenue per install, but not how to attribute, extrapolate or respond to spend." Part by part: the
   returns, the revenue per install and the next euro turn on analysis; the band is a filed rule applied to the
   figures; the staff, test, sandbox and reinstall rows are definition reading. **Main thread:** those rows are the
   hygiene set, measured neutral (each left unhandled moves no call and no graded figure out of its band).

Sweep lines, the reader's call: the 2027 dates in the media plan are the plan's own week starts (harmless); one author
on both workbooks is the person who keeps both budget sheets, and the policy has its own author (harmless).

Realism notes and what was done with each:
- The policy PDF was stamped 16 September and says it was approved on the 21st: fixed in the generator, the PDF is
  exported on the approval day (17:42 on 21 September 2026).
- The change log's notes came from eighteen phrases, with one closing phrase on every return to base: rewritten in the
  generator in the team's own hand (the quarter, the month and the weeks in the note, about one row in three left
  empty, five ways of closing a move); the moves themselves are unchanged.
- The stretch sheet is the plan times each channel's uplift and the plan runs in flights of several weeks: left, a
  stretch case is a percentage on the plan and a media plan is flighted by period; the sheet says it is the draft for
  the insertion orders.
- The policy's 4.2 (what version 3 added): left, a revision line of its genre; it settles nothing (deleting it moves
  no figure).
- Billing event ids, campaign names, the conversion-value file and the container stamps: read as genuine.

### Second read, on the rebuilt cut (the change log's notes rewritten, the policy PDF re-dated)

One isolated reader (Sonnet, medium) on fresh copies of `prompt.txt` and the 14 files, 2026-11-16, after the stage 4
repairs. It solved nothing.

1. **A sentence or file that tells how the analysis is done:** none. Of the change log: "Every note is a budget-change
   reason ... None explains why a recorded quantity differs from another or says which record to trust."
2. **A file that ranks or scores the candidates:** none.
3. **A file that exists only to help the analyst:** it named `skadnetwork_conversion_values.json` ("describes the
   conversion-value bit layout"). **Main thread: harmless.** It is the app's own conversion-value mapping, the
   configuration the backend computes the value from (which event sets which bit, the measurement window, when the
   postback is sent); the first reader called it "a bit-layout config that an app team would keep". The golden prices
   each value as its own cell and does not read the bit layout; the file is the home of the postback window (SF16).
4. **A figure or name that reads as the answer:** none.
5. **Filed sentences that fix a computation or a population:** the same list as the first read (1.2, 2.1 to 2.6, 3.1,
   4.1). "Together these fix the estimand fully ... They give no method for the forward estimate." It called 2.2's
   "whether or not the attribution partner can name it" a mild hint; **main thread:** it is the population of an
   install's channel, without which the named installs and all installs are two readings of every figure (SF2).
6. **One thing that makes most of it routine:** none. The change log "helps only the marginal-return and
   spend-response asks ... a documented mechanism and not a constructed single decider"; every ask turns on analysis,
   the band being the policy's rule applied to the analysed returns.

Sweep lines: the plan's 2027 dates and the shared author are both cleared, as in the first read.

Realism notes and what was done with each:
- The PDF's creation time shown as 11:42 EDT: the reader's viewer converting the stored 15:42 UTC (17:42 in Madrid on
  the approval day); the house writer stores UTC. Left.
- The change log: "the blank and non-blank mixes read as human", with short notes that repeat ("As planned", "End of
  the hold-back") and percentages in round steps. Left: 96 of 144 rows carry a note, 49 distinct; a team does move a
  budget in round percentages for a few weeks, and the moves themselves are the core's frozen schedule.
- The plan's blocks change in the same weeks on every channel and the stretch sheet is a fixed ratio on the plan:
  left, as in the first read (a plan flighted by month; the sheet says it is the draft for the insertion orders).
- The policy's 4.2 again: left, a revision line of its genre that settles nothing.
