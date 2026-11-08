# leak check, task7

**Verdict: REVIEW.** 16 files read, 6 golden figures and 0 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: million, record, carried, inspection, defaults, register, security, facility, inspections, architecture, december, shortfall, year-end, patients, feeder, staleness, decisive, exactly, average, latest, golden, market, facilities, roll-forward, cre-lgd-

## 2 author vocabulary (REVIEW 1)
- **REVIEW** `cre_lgd_model_documentation_2025.pdf`: \bthe model\b x3: ...elling. Independent validation: Model Risk, 14 October 2025. 1. Scope The model sets the loss given default of business facilities secured on commerc...

## 3 answer figures in the pack (REVIEW 2)
- **REVIEW** `ardcarn_credit_risk_policy_part4_2025.pdf`: golden figure 1.25 appears: ...probability of default 1 0.21% 2 0.42% 3 0.75% 4 1.25% 5 2.16% 6 3.74% 7 6.64% 8 13.28% 4.2 Default A f...
- **REVIEW** `ardcarn_credit_risk_policy_part4_2025.pdf`: golden figure 0.75 appears: ...ve-month probability of default 1 0.21% 2 0.42% 3 0.75% 4 1.25% 5 2.16% 6 3.74% 7 6.64% 8 13.28% 4.2 Def...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `ardcarn_credit_risk_policy_part4_2025.pdf`: 11 of 25 stump-paragraph terms appear (record, carried, inspection, defaults, register, security); read whether the document names the move
- **REVIEW** `cre_lgd_model_documentation_2025.pdf`: 7 of 25 stump-paragraph terms appear (inspection, defaults, security, facility, shortfall, facilities); read whether the document names the move
- **REVIEW** `plan_2027_credit_loss_request.pdf`: 7 of 25 stump-paragraph terms appear (inspection, security, facility, december, latest, facilities); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `dw_fact_loan_month_end_2022_2026.csv`: columns a generator names and an organisation does not: internal_grade, default_flag

## 9 dates after the setting (REVIEW 4)
- **REVIEW** `buildings_insurance_register_2026.xlsx`: 1468 ISO dates after 2027-01-15, e.g. 2027-02-01, 2027-03-01, 2027-04-01, 2027-05-01, 2027-06-01
- **REVIEW** `dw_fact_loan_month_end_2022_2026.csv`: 96958 ISO dates after 2027-01-15, e.g. 2027-01-16, 2027-01-18, 2027-01-19, 2027-01-21, 2027-01-22
- **REVIEW** `facility_register_2026-12.xlsx`: 3200 ISO dates after 2027-01-15, e.g. 2027-01-16, 2027-01-18, 2027-01-19, 2027-01-20, 2027-01-21
- **REVIEW** `rent_roll_2026-12.csv`: 2617 ISO dates after 2027-01-15, e.g. 2027-02-01, 2027-03-01, 2027-04-01, 2027-05-01, 2027-06-01

## 10 container metadata (INFO 1)
- **INFO** `-`: audit reported no writer signature (1 lines)

## 12 client quality check (INFO 2)
- **INFO** `-`: 16 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 11 prompt gate (clean)


## Solver's-eye read

Reader 1 (isolated, medium effort, cold copy of prompt.txt and target/, 2026-11-08), answers as returned, condensed:

1. Decisive step stated: "Largely yes, as a procedure": the memo's "Its loss given default follows the CRE-LGD-3 model,
   taking each default as if it fell on 1 January 2027 and the expected value of the security at that date, with property
   prices held at their latest published level through 2027" and the model document's definition of V as the inspection
   at default. No sentence names a statistical judgment.
2. Ranks or states the figure: none.
3. Helper-only files: none as a readme; the policy and the model document read as real governance papers.
4. Answer-like figure or name: none; the back-test's green rating "says the haircut is fine".
5. Literal execution: the memo, policy 4.4 and the model's formula, with V "taken as the latest value (index-rolled to the
   latest release, since prices are held flat)": the default path's construction.
6. What decides it: "mainly following a stated rule or procedure ... An analytical choice only enters if a solver
   questions the 22% haircut, the PDs or the held-flat prices."

REVIEW lines: all four ruled harmless (the model's own name; the policy and model numbers are inputs and history, not plan
figures; internal_grade and default_flag are ordinary bank names; the later dates are maturities, lease expiries, rent
reviews and renewals). Realism: customer names do not match their business codes; floor areas sit oddly against values;
the index releases run on a regular cadence; the documents are short and tidy; the two research and concentration files
read as distractors.

Main-thread ruling: question 5 is a main-call fork. "The expected value of the security at that date, with property
prices held" reads literally as the register's value, so the memo now files V as the value the bank would expect its
inspection to put on the security if the facility defaulted, and the loss as the CRE-LGD-3 figure on that expected value
(SF23). Question 6 is the reader's account of a route, not a measurement: the rule it names is the default path, and the
estimate of V is the analytical step it did not reach. The name and floor-area tells are fixed in the generator.

Reader 2 (isolated, medium effort, cold copy of the rebuilt pack, 2026-11-08), answers as returned, condensed:

1. Decisive step stated: "Partly": the memo names the quantity needed, "the value we would expect our inspection to put
   on the security if the facility defaulted", and "does not say how to estimate it"; nothing says the latest
   inspection is stale or what to do about it.
2. Ranks or states the figure: none.
3. Helper-only files: none; the policy, the model documentation and the memo read as bank governance documents.
4. Answer-like figure or name: none; the back-test's pass "mildly invites the solver to trust the model".
5. Literal execution: for each performing loan the grade, balance, master-scale PD and property share, and "an
   estimated inspection value as at 1 Jan 2027", run through CRE-LGD-3: the golden's estimand, its estimator left open.
6. What decides it: "Largely an analytical/modelling choice: estimating the inspection value at default from the
   property history, given that index roll-forwards are not inspections", with rule-following and hygiene beside it.

REVIEW lines: all four harmless. Realism: customer names match their business codes; floor areas plausible by type;
remaining tells were evenly spaced customer numbers (fixed: customer, legacy facility and property numbers now carry
irregular gaps, order kept), a geometric master scale (a master scale is built that way) and a tidy back-test (computed
from the record).

Main-thread ruling: no leak; question 5 now executes to the golden's estimand; question 6 names an analytical choice.
