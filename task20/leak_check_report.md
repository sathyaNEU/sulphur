# leak check, task20

**Verdict: REVIEW.** 14 files read, 33 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, managers, prototype, investment, golden, record, careful, section, quarter, inside, dropped, reflex, period, fitted, statements, register, carried, successor, second, market, manager, hurried, determinism, follow-ons, window

## 1 file names (REVIEW 2)
- **REVIEW** `corrigan_hart_pacing_plan_2027.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `peer_endowment_survey_2025.xlsx`: a sheet named 'About': confirm it is the organisation's own notes and does not describe the data's columns or files

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `wexmoor_endowment_liquidity_policy_2025.pdf`: 10 of 25 stump-paragraph terms appear (managers, investment, record, section, quarter, period); read whether the document names the move
- **REVIEW** `wexmoor_investment_policy_statement_2024.pdf`: 4 of 25 stump-paragraph terms appear (managers, investment, period, manager); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `corrigan_hart_pacing_plan_2027.xlsx`: names 7 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `manager_portfolio_activity_2013_2026.csv`: 142 ISO dates after 2027-03-12, e.g. 2027-03-31, 2027-06-30, 2027-09-30, 2027-12-31, 2028-03-31
- **REVIEW** `private_commitment_register_2026-12-31.xlsx`: 104 ISO dates after 2027-03-12, e.g. 2027-03-31, 2027-06-30, 2027-09-30, 2027-12-31, 2028-03-31

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 33% of 24 prompts (cap 30%); deliverable set 'docx+xlsx' at 21% of 24 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Architecture 6's cut (2026-11-13): one isolated reader (general-purpose, Sonnet, medium) on fresh copies of prompt.txt and target/ only.

1. **Method/step/window/population sentences.** No file tells the analyst what comparison, model or adjustment to run; the one document that fixes procedure is the policy the prompt itself asks about. `wexmoor_endowment_liquidity_policy_2025.pdf` §2: "The test covers the eight quarters from 1 January of the budget year." §3: "Net cash needs over the eight quarters are the spending distribution, plus the capital calls on every private commitment..., less the distributions from the private funds." §9: "Where the plan sets out alternative programs, the Investment Committee adopts the program with the largest total of new commitments that passes." These are the policy's own rules (what the prompt's "liquidity policy" means), not an outside hint.

2. **Ranking file.** None. `corrigan_hart_pacing_plan_2027.xlsx`'s "Programs" sheet lists A/B/C/D with only a description and a "Total (USD m)" column (540 / 365 / 280 / 40); no pass/fail mark, no liquidity reference, no order by headroom.

3. **Helper-only file.** None found. The two short sheets that could look like dictionaries are organisational text, not column dictionaries: "Notes" ("Draft for discussion with the Office of Investments, 7 December 2026, for the Investment Committee's March 2027 meeting... Corrigan Hart LLC, Private Markets Advisory.") is the consultant's own cover memo; "About" ("Survey of private university endowments of USD 2.5 billion to USD 14 billion, fiscal year 2025, anonymised. Compiled by Corrigan Hart LLC from responses received by 30 September 2025.") describes the survey's population, not the workbook's fields.

4. **Figure/name reading as the answer.** None. The nearest candidates are inputs, not outputs: the USD 1,520 million minimum reserve (policy §5, a stated constant) and the four programs' totals. No headroom, pass/fail or recommended-program figure appears anywhere in target/.

5. **Sentence fixing a figure's computation or population.** Policy §7: "each fund distributes its value at 31 December times the distribution rate of its strategy in the matching quarter from the third quarter of 2008 in the industry cash-flow benchmark: the benchmark funds' distributions in that quarter over their value at the end of the previous quarter, each summed over the strategy's funds." Executed literally this fixes the distributions-in-stress figure to one formula and one population: group the benchmark by strategy, read its distribution rate in the quarter mapped from 2008Q3, multiply by each Wexmoor fund's own 31-Dec-2026 NAV. §8: "the calls managers make on the companies their funds already hold are judged on the industry benchmark's funds that were past their investment periods from 2008 to 2010," which fixes the benchmark sub-population (post-investment-period funds only) used for the capital-calls estimate, and rules out a slowdown assumption ("No allowance is made for managers finding fewer new companies to invest in...").

6. **One unlocking thing?** No. The policy defines the test, but executing it still needs: assembling the liquid reserve across 20 holdings in 5 liquidity classes (§4's haircuts), clearing one restated/one "superseded" row in the capital-account statements, selecting the right benchmark rows by strategy and vintage for both calls and distributions, estimating FY2028 spending (only FY2027's is given in `spending_distributions_FY2014_FY2027.csv`; FY2028 needs the IPS's 70/30 formula applied forward with no HEPI figure supplied), and reconciling unfunded commitments by strategy across the register, audited financials and Q4 custodian activity. Most parts turn on analysis (cross-file assembly and stress estimation); a few sub-steps turn on reading a stated definition correctly (the §4 haircuts, §3's rule that a fund without a first close counts in full) but still need correct application across files, not a single lookup. Nothing hinges on a planted decoy; the capital-plan PDF is a disclosed, undisguised non-leak distractor ("No project draws on the endowment beyond the annual distribution the trustees approve").

**Flags**
- `corrigan_hart_pacing_plan_2027.xlsx` "Notes": the consultant's own meeting cover note (audience, scope, program philosophy), not a column or file dictionary. Harmless.
- `peer_endowment_survey_2025.xlsx` "About": describes the survey's population and compiler, not the sheet's columns. Harmless.
- Both PDFs state only their own institution's rules (the test's parameters; the IPS's allocation and spending rules); neither names a file, a step, or "what to look for" beyond its own policy text. Harmless.
- `corrigan_hart_pacing_plan_2027.xlsx` "Programs" sheet: description and USD totals only, no liquidity pass/fail mark or rank. Harmless.

Verdict: NO LEAK. No file ranks or scores the four programs, no figure reads as the final answer, and the one document that fixes procedure (the liquidity policy) is the institution's own governing rule that the prompt explicitly names as the test, not a solver hint; the asked-for figures still require cross-file assembly, benchmark-based stress estimation and minor hygiene cleanup to produce.

**Main thread's rulings (2026-11-13):** every REVIEW line harmless. The plan's Notes sheet and the survey's About sheet are the organisations' own notes; the two policy PDFs state their institutions' rules (the liquidity policy is the test the prompt names, its section 8 fixing the basis of the calls past the endowment's record, the line balances where reports stop and the pace of new investment, none of which names the successor funds' closes or the real-asset loans); the plan's Programs sheet carries descriptions and totals only. The reader's question-6 remark that FY2028 spending needs the investment policy statement's formula misses policy section 3 ("one quarter of the distribution the trustees approved for the fiscal year in which the test is run"), which the golden applies (SF4) and the platform's audit recomputed exactly; no fix. Question 1 quotes only the policy's own test; question 5's sentences execute to the golden (sections 7 and 8, SF7, SF21). Nothing settles most of the asks; no fix.
