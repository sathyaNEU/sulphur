# leak check, task10

**Verdict: REVIEW.** 11 files read, 7 golden figures and 11 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, guideline, golden, provider, design, delivery, record, baseline, neighbour, ashcombe, control, points, reduction, export, register, street, october, measured, carries, question, decisive, forecast, half-hours, graded, carried

## 3 answer figures in the pack (REVIEW 6)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 30.5 appears: ...40852 20 + 23 21.0 Fenwick Street PS41474 27 + 27 30.5 Hartwell Common PS41236 15 + 16 17.8 Kestwick Fie...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 22.5 appears: ...40617 20 + 20 23.0 Charlecote Way PS41108 20 + 20 22.5 Dunmore Street PS40852 20 + 23 21.0 Fenwick Stree...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 23.0 appears: ...Firm capacity (MW) Ashcombe Road PS40617 20 + 20 23.0 Charlecote Way PS41108 20 + 20 22.5 Dunmore Stree...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: golden figure 17.8 appears: ...1474 27 + 27 30.5 Hartwell Common PS41236 15 + 16 17.8 Kestwick Fields PS40508 17 + 17 19.5 Ravenhurst P...
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: carries 15 of 16 distinctive words of the committed call: 'Commit reinforcement at Ashcombe Road and Hartwell Common for winter 2027/28; Charlecote Way and Fenwick Street hold fir'
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: carries 13 of 16 distinctive words of the committed call: 'Commit reinforcement at Ashcombe Road and Hartwell Common for winter 2027/28; Charlecote Way and Fenwick Street hold fir'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: 11 of 25 stump-paragraph terms appear (guideline, provider, design, ashcombe, control, reduction); read whether the document names the move
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: 9 of 25 stump-paragraph terms appear (provider, baseline, ashcombe, reduction, register, street); read whether the document names the move

## 6 ranking artifacts (REVIEW 5)
- **REVIEW** `capacity_assessment_guideline_2026.pdf`: names 6 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_contract_awards_2027-28.pdf`: names 9 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `flexibility_events_2024-2026.csv`: names 9 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `primary_substation_register.xlsx`: names 6 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `primary_transformer_condition_2026.xlsx`: names 6 of 11 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 11 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 13 task metadata (REVIEW 1)
- **REVIEW** `metadata.json`: decision shares the design note's stump vocabulary (provider, design, delivery): say what the task decides, not how

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 9 dates after the setting (clean)

## 11 prompt gate (clean)


## Solver's-eye read

One isolated reader (general-purpose, sonnet, medium effort), 2026-11-08, on fresh copies of prompt.txt and target/
only; it read the pack for leaks and did not solve the task.

1. Decisive step: no sentence names it. Closest is guideline section 6 ("Flexibility contracted for the winter
   assessed is credited at the reduction in the primary's demand that its provider will deliver in the half-hours
   ending 17:30 and 18:00 on the design day, for each megawatt scheduled ..."), which fixes what is credited.
2. No file ranks or scores the candidates on the prompt's question (Appendix A gives firm capacity only; the award
   notice gives contracted MW only; nothing gives a design-day demand or a before or after figure).
3. capacity_assessment_guideline_2026.pdf "reads as a method sheet, but it is plausible as a governing document".
4. Nothing reads as the answer; the award notice's four zone rows and contracted MW are context.
5. Guideline 6 read literally: credit each primary with the delivered reduction per MW scheduled in the 17:30 and
   18:00 half-hours on the design day times the 2027/28 MW, and nothing else; guideline 7 commits where demand after
   the credit exceeds firm; guideline 3 and 4 fix the population. "s.6 fixes what to credit but not how to estimate
   the delivery per MW. Only the demand data and events can give that."
6. "The main answer is decided by an analytical choice: estimating delivery per scheduled MW from event history
   against a counterfactual", with a procedure-following component for the WHAT; no planted-defect sentence.

Sweep items: A harmless (contracted MW and zone names are the award notice's own content); B harmless, no ranking
(firm capacity, contracted MW, scheduled MW, ratings and health indices); C harmless (the prompt names outputs and
units, no method; "per megawatt scheduled" is the unit definition).

Realism tells reported, and their disposition: the nine primaries' names ran alphabetically with the world's keys;
feeder street names repeated across primaries; every zone's contract grew 0.5 MW a winter; growth references carried
a year after their acceptance (all four fixed in the generator, every graded figure unchanged in its bin); provider
names typed three ways and one letterhead on the three PDFs (kept: a control room's log and one organisation's
documents). Rulings in DESIGN_NOTE.md, Leak rulings.

### Re-read on the final cut (after the stage 4 fixes)

The same isolated reader brief, on fresh copies of the rebuilt prompt.txt and target/.

1. Points at guideline section 6 and the guideline's sections 2 to 7 as the stated pipeline ("hands over the method").
2. No file ranks the candidates; section 7 states the rule and computes nothing.
3. The guideline (a procedure document); the award notice's previous-winters table.
4. Nothing reads as a result.
5. Guideline 3, 4 and 6 read literally fix the before-demand, growth and credit; "The literal text does not say how
   delivery per MW is estimated from the events and demand data ... nor how the temperature correction is fitted. Those
   are left to the analyst."
6. "Mostly following a stated procedure in the guideline s2-s7. The open part is analytical (estimating delivery per
   scheduled MW from history, the temperature correction ...)."

Sweep items: A harmless on numbers (inputs, not results), the guideline flagged as method-heavy; B none ranks; C the
prompt's "per megawatt scheduled" mirrors guideline 6's filed definition, a mild cue.

Realism tells: 16:00 to 19:30 windows and few scheduled-MW values; contracted MW in 0.5 MW steps; codes PS40xxx, feeder
IDs, LCG references; "Plot 4, X Way" repeated in the growth register; health indices not linked to age in the condition
workbook. Rulings in DESIGN_NOTE.md, Leak rulings.

### Rubric repair read (2026-11-09, on target.zip 203d2bf4)
One isolated reader (general-purpose, sonnet, medium effort) on fresh copies of prompt.txt and target/ only, after the
asks were re-sited and the guideline's section 1 lead-time sentence restated; it read for leaks and did not solve.
1. Decisive step: none named. Nearest are guideline sections 3 and 6, which fix the before-demand's days and the
   credit's unit and window "but not how to estimate delivery" from the dispatch log and the half-hourly demand.
2. No file ranks or scores the candidates: Appendix A gives firm capacity only, the award notice contracted MW only.
3. capacity_assessment_guideline_2026.pdf (design condition, procedure, firm capacity), the register's DFES sheet and
   the award notice: the governing standard and its inputs, read as such.
4. None: Appendix A's firm capacities and the awards' megawatts are inputs; no demand, credit or exceedance appears.
5. Guideline sections 3, 4, 6 and 7 read literally give the golden's WHAT (the 2025/26 correction outside Christmas and
   the scheduled days, DFES compounded, the accepted connections in full, the delivered reduction per MW scheduled in
   the two credited half-hours on the 2027/28 MW, compared with Appendix A); "the delivery per scheduled MW is not
   given ... the method of estimating it is left open".
6. Mixed: the guideline's procedure for the WHAT, and "an analytical judgment on how much a provider really delivers
   per scheduled MW (estimated from past events against a counterfactual)"; the register, SCADA rename, weather
   versions and revised instructions read as texture.
Items: a harmless (the stated threshold); b harmless, the shared nouns are the subject, section 6's half-hours and
"per megawatt scheduled" are the WHAT, not the estimator; c no file ranks the candidates; d harmless (style).
Realism tells: the prompt's two colder temperatures beside a guideline that knows only minus 3.0 C read task-driven
(the ask now gives its reason, "should that winter bring days colder than the design day"); guideline issue 4's
document-control row ("Flexibility credit restated per megawatt scheduled"), the award notice's "on the same terms"
line, one weather station, PS4xxxx codes and the provider name variants were all read before and kept (rulings in
DESIGN_NOTE.md, Leak rulings). The prompt names no method, comparison, adjustment or step.
