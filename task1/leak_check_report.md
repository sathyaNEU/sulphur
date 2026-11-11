# leak check, task1

**Verdict: REVIEW.** 18 files read, 140 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: million, trailing, golden, pooled, carries, reading, accounts, creation, chosen, priced, family, commitment, graded, carried, hurried, missed, uploaded, history, nearest, careful, social, account, growth, standard, inside

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `digital_subscription_kpi_standard.pdf`: golden figure 5.1 appears: ...d is not a line of the plan. 5. Monthly reporting 5.1 Controlling reports, for each title and month, th...
- **REVIEW** `digital_subscription_kpi_standard.pdf`: golden figure 3.5 appears: ...xpected 36-month value of its starts is at least 3.5 times its planned cost per start, the plan's spen...

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `digital_subscription_kpi_standard.pdf`: 4 of 25 stump-paragraph terms appear (carries, accounts, account, standard); read whether the document names the move

## 6 ranking artifacts (REVIEW 3, INFO 2)
- **REVIEW** `marketing_spend_2023-01_2026-10.csv`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `media_plan_2027.xlsx`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **REVIEW** `print_circulation_2023-2026.csv`: names 3 of 4 answer-set candidates beside numbers; confirm it does not rank them on the decision question
- **INFO** `digital_subscription_kpi_standard.pdf`: names 3 of 4 answer-set candidates; confirm it does not rank them on the decision question
- **INFO** `price_list_digital_2027.pdf`: names 3 of 4 answer-set candidates; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 5)
- **REVIEW** `logins.csv`: 173 ISO dates after 2026-11-04, e.g. 2026-11-05, 2026-11-06, 2026-11-07, 2026-11-08, 2026-11-09
- **REVIEW** `payment_exceptions_2023-01_2026-10.csv`: 16 ISO dates after 2026-11-04, e.g. 2026-11-05, 2026-11-06, 2026-11-08, 2026-11-09, 2026-11-11
- **REVIEW** `payment_methods.csv`: 148 ISO dates after 2026-11-04, e.g. 2026-11-05, 2026-11-06, 2026-11-07, 2026-11-08, 2026-11-09
- **REVIEW** `price_periods_2023-01_2026-10.csv`: 251 ISO dates after 2026-11-04, e.g. 2026-11-05, 2026-11-06, 2026-11-07, 2026-11-08, 2026-11-09
- **REVIEW** `subscriptions_2023-01_2026-10.csv`: 1794 ISO dates after 2026-11-04, e.g. 2026-11-05, 2026-11-06, 2026-11-07, 2026-11-08, 2026-11-09

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 33% of 15 prompts (cap 30%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 18 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Reader: one isolated Sonnet thread at medium effort, 2026-11-10, on fresh copies of prompt.txt and target/ (the repaired cut) only.

1. No process instruction. Quoted the policy's definitions and conventions (4.1 the six movement categories in their order; 2.1 and 2.4 what ARR is; 2.3 the plan rate; 5.2 the population a plan forecast's range runs over; 5.3 what a commitment is), "definitions of terms/population rather than a forecasting method or model".
2. No file ranks candidates or states the answer; the KPI export stops at September 2026 actuals.
3. No helper file: the policy, the price book and the KPI refresh each have a life outside the task.
4. None.
5. Literal sentences quoted (policy 2.4 the paid invoice's seats billed times the price times twelve, failed payments not paid; 2.3 the flat plan rate): each executes to the golden's convention (SF2, SF6, SF7).
6. No one thing: "at least four separately-sourced mechanisms" (the Business renewal, price and seat dynamics; the Team plan under the 2026 minimum; pipeline conversion against the CRM's flat stage constants; the policy's categories and the commitment rule), with the policy settling only what to report and how to select the step once a distribution exists. Per sub-ask: the commitment, the path, the bridge's magnitudes, the Team cohort's December ARR and the open deals' ARR turn on analysis; the opening book (R1) on reading the definitions and executing them across thousands of rows (the assembly result, graded as such); the bridge's categories and the step rule are stated procedures applied after the analysis.
Realism: none of the twelve files looks generated (prices drift around list, id steps irregular, each container its own author and stamps); one soft note, the policy's document history lines up neatly with the pieces the prompt needs though it reads as a plausible multi-year evolution. Answered in the generator: version 5 also sets the month-end reconciliation's deadline in 6.1, so the revision is not single-purpose.
Least relevant: nps_responses_2026-q3.csv and support_tickets_2026.csv (the two distractors).

Rulings on the REVIEW lines: sweep 4 (eight common policy words) harmless, the policy defines terms and names no method or step; sweep 9 (service ends and period ends after 3 November 2026) harmless, "forward-running terms, not events after the extract": no service start after 1 November 2026, the latest invoice date 2 November 2026, the period ends the billed month attached to it.
