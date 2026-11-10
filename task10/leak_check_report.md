# leak check, task10

**Verdict: REVIEW.** 12 files read, 66 golden figures and 10 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: megawatts, architecture, golden, record, ashcombe, carried, scheduled, guideline, street, fenwick, inside, window, contracted, megawatt, missed, measured, provider, half-hour, scatter, prompt, forecast, spread, primaries, carries, half-hours

## 3 answer figures in the pack (REVIEW 16)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 27.0 appears: ...| Page 1 of 2 Wexley Hill PS40975 24 + 24 27.0 Transformer ratings from the primary substation r...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 17.8 appears: ...1474 27 + 27 30.5 Hartwell Common PS41236 15 + 16 17.8 Kestwick Fields PS40508 17 + 17 19.5 Ravenhurst P...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 19.5 appears: ...1236 15 + 16 17.8 Kestwick Fields PS40508 17 + 17 19.5 Ravenhurst Park PS40391 15 + 15 17.5 Tollbrook La...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 23.0 appears: ...Firm capacity (MW) Ashcombe Road PS40617 20 + 20 23.0 Charlecote Way PS41108 20 + 20 22.5 Dunmore Stree...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 30.5 appears: ...40852 20 + 23 21.0 Fenwick Street PS41474 27 + 27 30.5 Hartwell Common PS41236 15 + 16 17.8 Kestwick Fie...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 21.0 appears: ...41108 20 + 20 22.5 Dunmore Street PS40852 20 + 23 21.0 Fenwick Street PS41474 27 + 27 30.5 Hartwell Comm...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 22.5 appears: ...40617 20 + 20 23.0 Charlecote Way PS41108 20 + 20 22.5 Dunmore Street PS40852 20 + 23 21.0 Fenwick Stree...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 10.0 appears: ...t CMZ Fenwick Street Quillon Energy Services Ltd 10.0 5.70 289 Hartwell Common CMZ Hartwell Common Cor...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 21.0 appears: ...Ashcombe Road CMZ Ashcombe Road Corvane Flex Ltd 21.0 6.40 312 Charlecote Way CMZ Charlecote Way Quillo...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 7.5 appears: ...y CMZ Charlecote Way Quillon Energy Services Ltd 7.5 5.85 296 Fenwick Street CMZ Fenwick Street Quillo...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 2.5 appears: ....5 Charlecote Way CMZ Quillon Energy Services Ltd 2.5 3.0 4.0 Fenwick Street CMZ Quillon Energy Service...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 3.5 appears: ...ntract period on the contracted megawatts for the 3.5 hours of the service window. Utilisation is paid...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 4.5 appears: ...ck Street CMZ Quillon Energy Services Ltd 2.5 3.5 4.5 Hartwell Common CMZ Corvane Flex Ltd 2.0 2.5 3.0...
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: golden figure 4.0 appears: ...ecote Way CMZ Quillon Energy Services Ltd 2.5 3.0 4.0 Fenwick Street CMZ Quillon Energy Services Ltd 2....
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: carries 14 of 17 distinctive words of the committed call: 'Commit reinforcement at Ashcombe Road, Fenwick Street and Hartwell Common for winter 2027/28; Charlecote Way stays withi'
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: carries 11 of 17 distinctive words of the committed call: 'Commit reinforcement at Ashcombe Road, Fenwick Street and Hartwell Common for winter 2027/28; Charlecote Way stays withi'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: 14 of 25 stump-paragraph terms appear (megawatts, ashcombe, scheduled, guideline, street, fenwick); read whether the document names the move
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: 11 of 25 stump-paragraph terms appear (megawatts, ashcombe, scheduled, street, fenwick, window); read whether the document names the move

## 6 ranking artifacts (REVIEW 5)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: names 4 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: names 8 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_events_2023-2026.csv`: names 8 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `primary_substation_register.xlsx`: names 4 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `primary_transformer_condition_2026.xlsx`: names 4 of 10 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 12 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Architecture 6. One isolated reader each time (general-purpose, sonnet, medium effort) on fresh copies of prompt.txt
and target/ only; it read the pack for leaks and did not solve the task. Two reads on 2026-11-10: the first on the
stage 3 cut (target.zip a934f8e7), the second after the stage 4 fix pass changed the award notice and the prompt
(target.zip 9ba1c5b9; the final cut 7ce57054 differs from it only in the minute of each switching-log entry, which no
figure reads). The second read's answers, in its own words where quoted:

1. Method-telling text: "the capacity assessment guideline ... states most of the method, and the prompt itself names
   none." It quotes guideline 2 (the design day and the GMT-day mean), 3 (the 2025/26 working weekdays outside
   Christmas, the scheduled days and the logged transfer days), 4 (growth, the qualifying connections, every half-hour
   in the peak's proportion), 5 (firm capacity), 6 ("what its provider will deliver on the design day with the megawatts
   contracted ... scheduled in full", "the half-hours ending 17:30 and 18:00") and 7 ("more than one design day in
   ten"), and the award notice's scheduling rule. "The open parts are how to turn contracted MW into delivered MW, the
   spread behind 'nine design days in ten', and the back-test." "The prompt itself is clean."
2. "No file ranks or scores the candidates on the question."
3. "No file is made only for the analyst." The guideline and the award notice are in-world governing documents; the
   charging statement, the interruptions workbook and the condition workbook read as plausible distractors.
4. "Nothing reads as the answer." The award notice's contracted megawatts and Appendix A's firm capacities are inputs;
   21.0 MW at Ashcombe Road against 7.5 in 2025/26 "is a striking jump. It is a contract fact and not a design-day
   number."
5. Filed sentences read literally: guideline 6 fixes the credited half-hours and the day's highest half-hour and "does
   not say how the delivered MW relates to contracted MW"; guideline 3 fixes the SCADA total and the exclusions, where
   "a scheduled day could be read as including Cancelled and Superseded rows ... a possible fork"; guideline 4 fixes
   the register filter and the dates; guideline 2 the GMT day; the award notice the half-megawatt steps.
6. "The pattern that makes most of it routine is the guideline's s3 to s7 ... What stays analytical is the
   contracted-MW-to-delivered-MW conversion and the back-test." Ask by ask: the demand before flexibility "is largely
   prescribed by s3, so it is a rule procedure with data cleaning"; the megawatts delivered "is the unspecified part
   ... It turns on analysis and is the most open step"; the megawatts off the peak "partly rule following (s4
   scaling), partly analysis"; the expected peak and the nine-days-in-ten level "Analysis"; the backtest "Analysis
   with no filed method".
7. Realism: every workbook's zip entries are stamped 1980-01-01; the PDFs are Writer and LibreOffice 7.6 with dates
   that match; the switching log "is very regular: all Closed/Opened pairs, 15-minute steps"; the award notice's
   contract history "is monotone in every zone ... a mild too-clean pattern"; no em dashes, no placeholder strings, file
   names describe data.

The first read answered the same way on questions 1 to 6 and added, on question 7, that five workbooks were created
before their latest content.

A third read followed the second fix pass (guideline 6 reworded, the prompt naming what the backtest's miss is measured
on; target.zip 1ee96fa6, from which the final cut d84ca1b2 differs only in the switching log's references, ammeter
readings and two reasons, which no figure reads). On question 5 it executed section 6 word for word: "A word-for-word
reader subtracts the delivered MW from the design-day half-hour profile across the whole service window, the 7
half-hours ending 16:30 through 19:30 ... Then the primary's with-flexibility demand is the max of that reduced
profile", and the megawatts delivered "refers to the contract's delivery in those half-hours". The credit in two
half-hours alone, which the second judge's first pass took from the earlier wording, is gone. The options it still
lists: the prompt's "17:30 to 18:00" read as one half-hour; a cancelled instruction's day; a transfer's days as the
operation dates alone or every day from close to restore; the GMT day's hour labels. On question 6: "The only open
piece is the delivery rate per contract ... Nothing in the pack is a planted trap that flips everything", with the
megawatts delivered, the nine-days-in-ten level and the backtest read as analysis. On question 7: the switching log's
references out of time order, its ammeter readings an exact function of the megawatts, and planned jobs over New
Year; the contract history in half-megawatt lots with awards 2 to 2.8 times the last contract "reads as built"; the
guideline of 15 September 2026 cites a notice dated 21 October.

Verdict on each line (the design note's Leak rulings carry the reasons):

- Questions 1 and 5: harmless, the WHAT of each result filed as designed; the cancelled-day option is SF20 (same call,
  every figure inside its band, asserted).
- Questions 2, 3 and 4: clean.
- Question 6: one earned result (the demand before flexibility) and the criterion, not most of the chain; the megawatts
  delivered, the megawatts off the peak, the nine-days-in-ten level and the backtest stay analysis by the reader's own
  account.
- Question 7: the 1980 entry stamps are the application's own (reduce-house-fixes H1); workbooks created before their
  content are living registers, each last saved after its latest record (checked); the switching log's quarter-hours
  FIXED in the generator (the minute as logged, figures.json and submission.md byte-identical before and after); the
  contract history's half-megawatt lots left as the tender's own.
- The third read's options: the half-hour ending 18:00 alone for the two half-hours' mean (SF4) and the megawatts
  taken flat through the window (SF23) each keep the call and every figure inside its band (asserted); a cancelled
  day is SF20; a transfer's days read as the operation dates alone sit between the golden and SF2's extreme (the
  logged days left in altogether, same call); the hour labels move the daily mean by under 0.07 C (judge r2).
- The third read's realism lines: the switching log FIXED in the generator (references in time order, each ammeter
  reading at its own busbar voltage and power factor, transfers made over Christmas, New Year or a bank holiday logged
  as fault restoration; figures.json and submission.md byte-identical before and after). The half-megawatt lots are
  the service's own step, and awards at multiples of the last contracts are the scenario's premise (the reviewer's
  audit names them as the judgment to test): left. The guideline's "the contract award notice" is a standing reference
  to each winter's notice: left.
- Every REVIEW line of sweeps 3, 4 and 6: inputs and the service's own terms, ruled in the design note.
