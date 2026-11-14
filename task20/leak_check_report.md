# leak check, task20

**Verdict: REVIEW.** 14 files read, 33 golden figures and 8 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: section, period, closes, careful, investment, successor, inside, manager, statements, reflex, periods, register, records, evidence, carried, missed, benchmark, dropped, architecture, property, hurried, engine, forecasting, quarter, refinancing

## 1 file names (REVIEW 2)
- **REVIEW** `corrigan_hart_pacing_plan_2027.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `peer_endowment_survey_2025.xlsx`: a sheet named 'About': confirm it is the organisation's own notes and does not describe the data's columns or files

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `wexmoor_endowment_liquidity_policy_2025.pdf`: 9 of 25 stump-paragraph terms appear (section, period, closes, investment, manager, periods); read whether the document names the move
- **REVIEW** `wexmoor_investment_policy_statement_2024.pdf`: 4 of 25 stump-paragraph terms appear (period, investment, manager, periods); read whether the document names the move

## 6 ranking artifacts (REVIEW 1)
- **REVIEW** `corrigan_hart_pacing_plan_2027.xlsx`: names 7 of 8 answer-set candidates beside numbers; confirm it does not rank them on the decision question

## 9 dates after the setting (REVIEW 2)
- **REVIEW** `manager_portfolio_activity_2013_2026.csv`: 142 ISO dates after 2027-03-12, e.g. 2027-03-31, 2027-06-30, 2027-09-30, 2027-12-31, 2028-03-31
- **REVIEW** `private_commitment_register_2026-12-31.xlsx`: 103 ISO dates after 2027-03-12, e.g. 2027-06-30, 2027-09-30, 2027-12-31, 2028-03-31, 2028-06-30

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: question form 'which' at 30% of 23 prompts (cap 30%); deliverable set 'docx+xlsx' at 22% of 23 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 7 hidden content (clean)

## 8 column names (clean)


## Solver's-eye read

Architecture 6 after the holistic audit's repair, the rebuilt cut of 2026-11-13 (stage 4, pass 2). One isolated reader (Sonnet at medium) saw fresh copies of prompt.txt and target/ only, was told which files the sweep flagged and never which words or numbers, and solved nothing. Its answers, with the main thread's ruling on each.

1. Sentences that say how the analysis is done: the liquidity policy, sections 3 to 9 (net cash needs, the reserve's factors, the test and the minimum, the stress path, the distribution rates, and in section 8 the pace of new investments, first closes on the managers' dates, the benchmark rate for buyout, growth and venture funds past their periods, how the facility balance is formed, the fees and expenses, and the program rule of section 9). Ruling: harmless by design. These are the reflex components the holistic audit asked to be stated (runs/arch6_holistic_audit.md); each executes to the golden (question 5), and executed alone they file the careful route's answer, program A, not the golden's B. Nothing quoted touches either deciding judgment: the policy says nothing of what ends an investment period or of the assets' loans (checks.py asserts it).
2. A file that ranks or scores the candidates: none. The plan's Programs sheet lists programs A to D with their funds and totals and scores nothing. Ruling: clean.
3. Files that exist only to help the analyst: no dictionary, readme or notes file. It read the peer survey and the capital plan as distractors (they are, and are unlabelled), and gave the custodian's file and the market series one use each. Ruling: harmless. The custodian's fourth-quarter cash is what a custodian sends whether or not a statement is late, and the market series carries the exit index, equities and the short rate the policy's stress and the assets' values and loans all run on.
4. A figure that reads as the answer: none. The nearest are the plan's program totals, the minimum reserve and the approved distribution, all inputs. Ruling: clean.
5. Filed sentences that fix a graded figure literally: section 3 (pending funds in full, release at the term's end, the cap at the commitment), section 7 (distributions and the late-statement value), section 8 (the rate taken whole, no allowance for the exit market or reinvested proceeds, the facility balance's sum, the custodian's calls taken as called for investments). Ruling: each executes to the golden; checks.py reads every one back from the shipped PDF and verify.py recomputes the facility balance and the pace from them independently.
6. One thing that makes most of it routine: "the liquidity policy PDF itself", which settles the distributions, the commitments not yet called and the filed parts of the calls. Ruling: not a one-fact unlock. Those are the results priced Right for the careful pass (R1, R4 and the reflexes J1 to J6); the policy alone files a headroom of USD 326.7 million and program A, and the two results that decide the program (R2 the successor closes, R3 the refinancing calls) and the three downstream of them are not in it. The reader did not name the successor closes anywhere. It did name the loans: with the fees now filed, section 8's last line (any other call a fund can be expected to make is judged on the evidence) stood alone, and the reader called it "the one open clause" and pointed from it at the activity file's loan records. Ruling: FIXED. The line is deleted and its content folded into the section's opening sentence (all the calls the managers can be expected to make, for whatever purpose, judged on the evidence), so every call still counts and the list no longer closes on a signpost. The loan records themselves stay: they are the activity file's own rows, and reading them is the work of R3.

Realism. Fixed in pack.py, no figure moved (figures.json and effort.json identical before and after): the custodian's fourth-quarter cash fell on two dates (now each fund's own business day, 43 dates); each fund's accrued liabilities repeated year after year in the audited accounts (now a varying share of the quarter's fee). From pass 1, fixed in the same cut: each fund's audited cash was one amount every year; commitment dates fell on four calendar days. Left as they are, with the reason: every agreement's investment period is five years (the usual term); a first-year fund's borrowings equal its investments at cost (it invests through its facility before its first calls for investments); early fees are a round share of commitment (the contractual rate on a round commitment).

The sweep's REVIEW lines. The plan's Notes sheet: the adviser's cover notes, harmless. The survey's About sheet: the survey's provenance, harmless. The two policies' stump-vocabulary counts: the field's own nouns, neither names a deciding judgment, harmless. The plan's Programs sheet: a list, no ranking, harmless. Dates after 12 March 2027 in the activity file and the register: loan maturities, scheduled period and term ends, expected first closes, harmless. The prompt's shell quota: a batch count; the prompt is unchanged.

Final read (stage 4, isolated, the cut with section 8's closing line gone; prompt.txt and target/ only, nothing solved). No ranking, no answer figure and no helper file; the liquidity policy is the method document, by design. What the pack pointed it to first for the capital calls, and what it would check next, were section 8's filed bases; neither named the successor closes or the loans. It quoted two phrases of section 8's opening sentence as pointing past the list of bases: "for whatever purpose" and "judged on the evidence the Office of Investments holds". Rulings. The first: fixed. The three words were added in this repair when the closing line was folded into the opening sentence, and they do no work "all those" does not do; they are deleted in docs.py, and checks.py and verify.py read the sentence back from the shipped PDF ("Capital calls are all those the endowment's managers can be expected to make in the stress, judged on the evidence the Office of Investments holds."). The second: kept. It is the policy's standard for what counts as a call, the clause that makes the end of an investment period a matter of evidence and not of the register's recorded date (the determinism judge's pass 5 note on the literal reader), it would stand in the policy whatever the files held, and it names no call, file or step. Its further realism remarks are left as they are, with the reason: a first-year fund's borrowings equal its investments at cost (a fund invests through its facility before its first calls for investments); fees and expenses are flat shares of round commitments (the agreements' terms); every agreement gives a five-year investment period (the usual term); the audited accounts' total commitments are the fund's size, not the endowment's share (they are the fund's accounts).

Verdict of the read: no LEAK. Two announcements were found across the passes and removed in the generator (the stand-alone closing line of section 8, then the three words "for whatever purpose" in its opening sentence). The reader was not run again after the second removal, which deletes the words it quoted and adds none; leak.py was re-run on the final cut (REVIEW, the lines ruled above).
