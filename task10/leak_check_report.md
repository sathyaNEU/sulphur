# leak check, task10

**Verdict: REVIEW.** 14 files read, 68 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: street, architecture, record, fenwick, ashcombe, register, golden, megawatts, charlecote, hartwell, common, dunmore, guideline, primary, half-hour, planned, window, customers, carried, missed, october, forecast, inside, january, months

## 3 answer figures in the pack (REVIEW 7)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 25.6 appears: ...40617 24 + 24 27.5 Charlecote Way PS41108 22 + 22 25.6 Dunmore Street PS40852 20 + 23 20.0 Fenwick Stree...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 27.5 appears: ...Firm capacity (MW) Ashcombe Road PS40617 24 + 24 27.5 Charlecote Way PS41108 22 + 22 25.6 Dunmore Stree...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 20.0 appears: ...41108 22 + 22 25.6 Dunmore Street PS40852 20 + 23 20.0 Fenwick Street PS41474 30 + 30 35.0 Hartwell Comm...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 27.0 appears: ...PS40233 23 + 23 26.0 Wexley Hill PS40975 24 + 24 27.0 Transformer ratings from the primary substation r...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 24.4 appears: ...1474 30 + 30 35.0 Hartwell Common PS41236 21 + 21 24.4 Kestwick Fields PS40508 17 + 17 19.5 Ravenhurst P...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 35.0 appears: ...40852 20 + 23 20.0 Fenwick Street PS41474 30 + 30 35.0 Hartwell Common PS41236 21 + 21 24.4 Kestwick Fie...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: carries 21 of 26 distinctive words of the committed call: 'Commit reinforcement at Ashcombe Road, Charlecote Way, Dunmore Street and Fenwick Street for winter 2027/28 and hold Har'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: 17 of 25 stump-paragraph terms appear (street, record, fenwick, ashcombe, register, megawatts); read whether the document names the move
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: 14 of 25 stump-paragraph terms appear (street, fenwick, ashcombe, register, megawatts, charlecote); read whether the document names the move

## 6 ranking artifacts (REVIEW 6)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_asset_register_2026-11-04.csv`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_events_2023-2026.csv`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `primary_substation_register.xlsx`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `primary_transformer_condition_2026.xlsx`: names 5 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 13 task metadata (REVIEW 1)
- **REVIEW** `metadata.json`: files[7].covers shares the design note's stump vocabulary (customers, october, january): say what the task decides, not how

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Stage 4 reader, 2026-11-10, on cut a40205c5 (target.zip sha256), one isolated thread that saw only prompt.txt and the
unzipped pack and solved nothing. Its answers, as returned:

1. Sentences that say how the analysis is done. The prompt pins only the quantities and the rounding.
   capacity_assessment_guideline_2026.pdf "describes the method almost end to end": section 2 (the design day and the
   GMT daily mean), section 3 ("with no flexibility service delivered and with the network in its normal running
   arrangement ... established for the latest complete winter, 2025/26"), section 4 ("increased at the primary's
   underlying peak growth rates ... compounded, plus the demand that the customers on the load growth register will
   have added", "an offer counts once it is accepted ... offers withdrawn, superseded or only quoted are not counted",
   the monthly summary's mean demand between 17:00 and 18:00, "Every half-hour of the design day is taken to grow in
   the proportion its highest half-hour grows"), section 6 ("credited with what the provider's sites in service on the
   assessment date can be expected to deliver", "mean delivery in the half-hours ending 17:30 and 18:00", "taken only
   from days on which the primary was in its normal running arrangement", "whichever half-hour that falls in"),
   section 7 ("more than one design day in ten", "taken over the variation from one design day to another as the
   record shows it, not over the uncertainty of the assessment's own estimates"). The awards notice adds "a site counts
   toward delivery once it has passed its commissioning test" and "No site may be added to a 2027/28 schedule after 16
   October 2026".
2. Files that rank or score the candidates on the prompt's question: none. The nearest are the awards notice
   (contracted MW by primary) and the guideline's Appendix A (firm capacity); neither ranks or scores.
3. Files that exist only to help the analyst: the guideline "works as a method sheet"; Appendix A is an input table;
   no other file is a helper.
4. Figures or names that read as the answer: none. The awards notice lists five primaries, so it narrows the
   candidates to the five with a 2027/28 contract; it does not say which to reinforce.
5. Sentences that fix a graded figure literally: section 2 (every working Monday to Friday outside bank holidays and
   24 December to 2 January at a GMT-day mean of minus 3.0 C, assessed as at 15 January); section 3 (half-hourly SCADA
   total demand, UK local end time, the day's peak its highest half-hour, no flexibility delivery, no transferred
   load, from the 2025/26 record); section 4 (the 2025/26 figure grown at the two DFES rates compounded plus the
   register customers' added demand between the two assessment dates, accepted offers counted on the register's date,
   withdrawn, superseded and quoted offers not counted, a customer's demand from the monthly summary); section 5
   (Appendix A); section 6 (the contracted megawatts scheduled for the whole window, credited at what the sites in
   service on the assessment date can be expected to deliver, in service from the commissioning test until withdrawn,
   delivery as the mean of the half-hours ending 17:30 and 18:00, from normal-running days); section 7 (the share of
   design days over firm capacity, the spread from day-to-day variation in the record); the awards notice (contracted
   megawatts, the service window 16:00 to 19:30).
6. One thing: "capacity_assessment_guideline_2026.pdf. It is a complete recipe for demand, growth, register uplift,
   flexibility credit, peak and exceedance share. Once it is read literally, what remains is execution of a filed
   procedure." Part by part: firm capacity is read from a table; demand before flexibility "follows a stated rule
   (s3 and s4). The only judgement is how demand at -3 C is modelled"; expected delivery "follows a stated rule ...
   The data work is real, in the asset register statuses and dates, the events and the switching log"; the expected
   peak, the nine-days-in-ten level and the share each follow a stated rule, the level needing a modelled day-to-day
   spread. "None of it turns on catching something planted. The one real piece of analysis is the distributional
   model of design-day demand and of provider availability."
7. Realism: the growth register's references follow one pattern and its 2019 and 2020 rows are energised "a regular 9
   to 15 months after offer acceptance"; superseded rows repeat the accepted row's reference; transformer ratings and
   firm capacities are round; the SCADA point names change on one date (plausible); class and provider names vary as
   typed (real messiness); a site commissioned a day before its planned date (plausible); the switching log is short
   and tidy. "Nothing else reads as obviously machine-made."
8. Sweep lines: all harmless. Appendix A is an input; neither document names which primaries to reinforce or states a
   demand, a delivery, a peak or a ranking; none of the six files ranks or scores the primaries (the transformer
   condition file scores asset health, not this question).

Findings the reader listed to fix: the guideline's sections 2 to 7 as a near-complete method statement ("If the
method should stay open, trim it"); section 4's proportional growth of every half-hour; section 6's two half-hours and
normal-running days; the awards notice naming exactly five primaries and closing the schedules on 16 October 2026.

Main thread's rulings (2026-11-10):
- Questions 1, 3, 5 and 6 (the guideline as a recipe): every sentence the reader quotes files what a result is (the
  design day and that every such day counts, the latest winter, growth, which customers and between which dates, a
  customer's demand, in service and on which date, the credited half-hours, the day's highest half-hour, one design
  day in ten over day-to-day variation). None says how demand at the cold end is read, how a customer's demand
  relates to its agreed capacity or its age, or how late a site commissions. The reader's account is of a route it
  did not run; the generator's measurement of that route (effort_passes.py, the careful pass: every filed sentence
  executed with the methods both architecture 6 runs used) commits Ashcombe Road and Hartwell Common and earns 3 of
  11 results. The sentences stay: each closes a fork (SF3, SF4, SF5, SF6, SF11, SF13, SF14, SF16, SF18 to SF20), and
  section 2's "whether or not a flexibility service would be instructed on it" is what stops the days without a
  service being read as the population.
- Question 4 and the awards notice's five primaries: the prompt asks about the zone primaries, and the notice is
  where a zone and its contract are defined; it carries no call.
- Question 7: the flat 6 to 14 months from acceptance to energisation is fixed in the generator (acceptance dates now
  run from about three months to over two years before energisation, large supplies longer), and with it one row
  the mechanical sweeps could not see: an offer shown as accepted on 20/01/2027 in a register saved on 30 October
  2026 (dd/mm/yyyy, outside sweep 9). The date is printed only, no result reads it, and checks.py now asserts no
  acceptance or energisation after the register's last save. The other notes describe how such records look.
