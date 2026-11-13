# leak check, task20

**Verdict: REVIEW.** 14 files read, 54 golden figures and 4 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: architecture, managers, follow-ons, inside, careful, quarter, dropped, prototype, record, statements, golden, budget, defensive, second, hurried, section, carried, reflex, missed, hardening, recycling, closes, fitted, prompt, market

## 1 file names (REVIEW 2)
- **REVIEW** `corrigan_hart_pacing_plan_2027.xlsx`: a sheet named 'Notes': confirm it is the organisation's own notes and does not describe the data's columns or files
- **REVIEW** `peer_endowment_survey_2025.xlsx`: a sheet named 'About': confirm it is the organisation's own notes and does not describe the data's columns or files

## 4 design-note vocabulary (REVIEW 1)
- **REVIEW** `wexmoor_endowment_liquidity_policy_2025.pdf`: 7 of 25 stump-paragraph terms appear (managers, quarter, record, budget, second, section); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 14 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 2 author vocabulary (clean)

## 3 answer figures in the pack (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)


## Solver's-eye read

### 1. Sentences or files that tell you how a step, comparison, adjustment, grouping, population or window should be done

The policy document, `wexmoor_endowment_liquidity_policy_2025.pdf`, is built to do exactly this for the parts of the test it governs (expected, since the prompt's question is literally whether a budget passes "its liquidity policy"). The load-bearing window/population/grouping sentences:

- Window: "The test covers the eight quarters from 1 January of the budget year." (Section 2)
- Population/grouping for net cash needs: "Net cash needs over the eight quarters are the spending distribution, plus the capital calls on every private commitment (those made by 31 December and the budget's new commitments), less the distributions from the private funds." (Section 3)
- Grouping for the liquid reserve: "each counted at the share of its value its liquidity class allows: cash, money market funds and US Treasuries 100 per cent; investment-grade bonds 90 per cent; public equities 70 per cent; hedge funds the endowment can redeem with the proceeds received within the eight quarters 90 per cent; all other holdings nothing." (Section 4)

Two things are worth flagging about what this document does *not* pin down, because they are where the real analysis still has to happen:
- Section 8, verbatim: "Capital calls are those the endowment's own managers can be expected to make in the stress, judged from their record in the endowment's funds." This names the population (the endowment's own managers/funds) but deliberately gives no method, formula or grouping, it is an open judgment.
- Nothing in any document (policy, IPS or capital plan) states a method for the prompt's other ask, the half-year base-case capital calls and distributions on existing commitments (not the stress). No file anywhere mentions a comparison, adjustment or grouping for that half-year pacing; it has to be built from `capital_account_statements_2013Q1_2026Q4.csv` and/or `industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv` with a method the analyst chooses.

### 2. File that already ranks or scores the candidates on the prompt's question

None. No file states a pass/fail verdict, a net cash needs total, a headroom total, or any candidate commitment amount other than the one already in the prompt text itself (Corrigan Hart's USD 500 million), which is an input, not an answer. `corrigan_hart_pacing_plan_2027.xlsx` proposes amounts (500 for 2027, rising to 585 by 2031 in "Long-range pacing") but never evaluates them against the liquidity policy. `peer_endowment_survey_2025.xlsx` gives other endowments' unfunded/value and liquidity ratios but never scores Wexmoor.

### 3. Files that exist only to help the analyst (not substantive data)

- The `Notes` sheet of `corrigan_hart_pacing_plan_2027.xlsx` (4 cells: drafting context, "no new managers are proposed for 2027," the advisor's own sizing rationale, and an attribution line). Pure background, not data.
- The `About` sheet of `peer_endowment_survey_2025.xlsx` (2 cells: "Survey of private university endowments of USD 2.5 billion to USD 14 billion, fiscal year 2025, anonymised." and "Compiled by Corrigan Hart LLC from responses received by 30 September 2025."). A provenance footnote.
- The trailing note row in `liquid_holdings_2026-12-31.xlsx`: "Private funds at capital account value are reported separately (capital account statements)." A pointer to another file, not data itself.

None of these three states a method, a figure, or a verdict; they only orient the reader.

### 4. Figure or name that reads as the answer rather than context

I did not find a figure planted as the answer. The two numbers that could be mistaken for the point of the exercise are both plainly inputs, not results: "USD 500 million" (the proposed 2027 total, already given in the prompt itself) and "USD 1,200 million" (the 2027 minimum reserve, stated in Section 5 of the policy as a trustee-set parameter, needed to run the test, not the result of it).

One thing that reads as more relevant than it is: the IPS asset-allocation table in `wexmoor_investment_policy_statement_2024.pdf` (Private equity and venture capital target 32%, range 25-40%) and the pacing plan's note that commitments are "sized to keep the private allocation near its 52 per cent policy target by 2031." Both look like they could bound or justify a commitment number, but the liquidity policy's test (Sections 3-5) never references an allocation percentage anywhere, it is a pure cash-flow test. A solver who anchors on the 32%/52% figures instead of the cash-flow test would be answering a different question.

### 5. Filed sentences that, read literally, fix how a figure is computed or over which population (quoted, with the literal result described in words, no numbers computed)

1. Section 3: "The spending distribution of each quarter is one quarter of the distribution the trustees approved for the fiscal year in which the test is run." Literally, this points at a single row of `spending_distributions_FY2014_FY2027.csv` (the FY2027 `approved_distribution_usd_m`, already tabulated there) and says to use one-quarter of that same fixed number for every one of the eight stress quarters, i.e. for both 2027 and 2028, rather than computing a fresh FY2028 figure from the IPS spending formula for the second year.
2. Section 3: "Commitments to funds that have not held a first close count in full." Literally, this tells the analyst that for any fund without a first close (four of them as of 31 December 2026, per the "First close" column of `private_commitment_register_2026-12-31.xlsx`), the whole committed amount, not a drawn-down or scheduled portion, is what goes into the capital-calls side of net cash needs.
3. Section 3: "A commitment's part not called when its fund's term ends is released and does not count." Literally, for a fund whose term ends inside or before the window, the gap between its commitment and what it actually called drops out of net cash needs entirely; this matches the 21 rows in `capital_account_statements_2013Q1_2026Q4.csv` whose `note` field reads "final statement; commitment not called released."
4. Section 4's liquidity-class sentence (quoted under Q1) literally says to take `liquid_holdings_2026-12-31.xlsx`'s own "Policy liquidity class" label on each of its 19 holdings rows and apply exactly the stated percentage to that row's market value, nothing else decides a holding's treatment.
5. Section 5: "Budgets are set in multiples of USD 25 million." Literally restricts "the largest 2027 total that passes" to a fixed grid of candidate amounts, nothing in between.
6. Section 7: "the benchmark funds' distributions in that quarter over their value at the end of the previous quarter, each summed over the strategy's funds." Literally, for a given stress quarter and strategy, this means pooling (summing), across every fund of that strategy in `industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv`, the quarter's distributions-as-percent-of-commitment and the prior quarter's NAV-as-percent-of-commitment, and dividing the two pooled sums, a dollar-weighted rate, not an average of each benchmark fund's own ratio. It also fixes the benchmark quarter by calendar offset from 2008 Q3 (not by matching vintage year, which the file also carries but this sentence never mentions).
7. Section 7's second sentence (the late-statement fallback, quoted under Q1's neighboring text) literally fixes a fund's 31 December value, when its Q4 statement has not arrived, to its 30 September capital-account NAV plus the Q4 capital calls and less the Q4 distributions exactly as `custodian_cash_activity_2026Q4.csv` recorded them for that fund. Three funds in the pack hit this condition (`WX-BO-102`, `WX-BO-113`, `WX-VC-161`).
8. Section 9: "A budget's new commitments are spread across the funds of the year's pacing plan in the plan's proportions." Literally points at `corrigan_hart_pacing_plan_2027.xlsx`, but the workbook gives two different proportion sets for 2027 that both sum to 500: the named-fund sheet ("2027 proposed commitments," e.g. Buyout 150, Private credit 135, no Infrastructure) and the strategy sheet ("Long-range pacing," e.g. Buyout 175, Private credit 65, Infrastructure 50). The sentence does not say which sheet "the plan's proportions" means.

### 6. The one thing, and a part-by-part read of the prompt

No single file, sentence or column collapses most of the prompt. The six things asked split into two largely independent clusters, and each keeps its own open step even once every filed convention above is applied:

- Cluster A (the budget test): the largest passing 2027 total, the net cash needs and headroom at USD 500 million. These share the liquid-reserve classification (a field read, see below) and the stress's capital-calls judgment (Section 8, deliberately left open, no file fills it).
- Cluster B (existing commitments): the half-year capital calls split by first-close status, the half-year distributions, and the unfunded balance by strategy at 31 December 2026. These share a base-case pacing method that no document states at all, plus a three-file reconciliation (register, capital account statements, custodian activity) carrying the restated/superseded duplicate for `WX-GE-141` and the three late Q4 statements.

Nothing in the pack bridges both clusters, so there is no single fact that rescues "most" of the prompt. Part by part:

- Largest 2027 total that passes: turns on analysis (the Section 8 capital-calls judgment drives the whole search); the "multiples of USD 25 million" grid and the pass/fail threshold are a stated procedure layered on top.
- Net cash needs at USD 500 million: turns on analysis (same capital-calls judgment, plus the benchmark distribution-rate computation) and on a rule to follow (Section 3's spending sentence, Section 9's allocation sentence, though which sheet Section 9 means is unpinned, see Q5 item 8).
- Headroom above the minimum reserve: once net cash needs and the liquid reserve exist, this is arithmetic; the liquid reserve side itself turns mostly on reading one field correctly (the holdings file's own "Policy liquidity class" column) rather than new analysis.
- Half-year capital calls split by first-close status: the split itself turns on reading one field correctly (the register's "First close" column, four funds are blank); the half-year calls amounts turn on analysis (no filed base-case method).
- Half-year distributions: turns on analysis (same gap, no filed base-case method).
- Unfunded commitments by strategy at 31 December 2026: turns mostly on correctly executing a stated rule and reconciliation (the late-statement fallback for three funds, the first-close-pending funds counting in full, the one restated/superseded duplicate, joined to the register's strategy field) rather than open analysis.

### Review verdicts

**(a) The `Notes` sheet in `corrigan_hart_pacing_plan_2027.xlsx`.** Harmless. Its four lines are drafting context (who it is for, when), a statement that no new managers are proposed, the advisor's own allocation-target rationale, and an attribution line. It names no step of the liquidity test, no figure, no verdict. The "52 per cent policy target by 2031" line is the one place a solver could be pulled toward the IPS allocation targets instead of the cash-flow test (see Q4), but that is a plausible real-world distraction, not an instruction.

**(b) The `About` sheet in `peer_endowment_survey_2025.xlsx`.** Harmless. Two lines of sourcing (population surveyed, who compiled it and when). No method, no figure relevant to Wexmoor's own test.

**(c) Whether `wexmoor_endowment_liquidity_policy_2025.pdf` names an analytical move versus rules the trustees set.** Harmless overall. The document is the rulebook the prompt explicitly asks the solver to satisfy, so stating the test's definitions (the window, the net cash needs components, the liquid reserve classes, the minimum reserve, the budget granularity) is the trustees' own rules, not a hint about how to analyze anything; and it visibly withholds a method exactly where the task wants analysis (Section 8's capital-calls judgment, and total silence on the half-year base-case pacing asked for separately). The one sentence worth a second look is Section 3's spending-distribution rule, which, read literally, turns what could have been a projection (apply the IPS's spending formula to a new FY2028 figure) into a single lookup repeated across both years; that is a filed convention fixing a population/window, consistent with how this project's own determinism rules say a result's inputs should be pinned, not an analytical shortcut being handed to the solver.

### Realism note

The pack reads as genuine institutional paperwork rather than generated filler. All three PDFs are LibreOffice Writer exports with distinct creation timestamps that match the dates named in each document's own text (policy amended 11 September 2025, created 11 Sept 2025; IPS approved 6 June 2024, created 6 June 2024; capital plan presented 18 September 2026, created 18 Sept 2026). The xlsx files carry distinct personas (Donna Turner for the custody/register/holdings files, Corrigan Hart LLC for the pacing plan and peer survey) with modified dates that lag their "as of" dates by a realistic number of days to weeks, not toolchain defaults. The underlying fund data carries ordinary mess spread broadly rather than narrowly: a subscription-credit-facility pattern touching 46 of 87 funds across every strategy, one restated/superseded capital account statement, three funds with a late Q4 statement patched by the custodian file, four funds pending first close, and 21 funds with a released unfunded balance at term end. `wexmoor_university_capital_plan_FY2027_FY2031.pdf` is a convincing distractor: a fully fleshed-out five-project capital plan with its own debt and gift figures that explicitly rules itself out of the endowment question in its own text ("No project draws on the endowment beyond the annual distribution the trustees approve"), rather than being silently unused. The one internal wrinkle worth a second look, not a trap, just worth the generator being able to justify, is that `corrigan_hart_pacing_plan_2027.xlsx`'s two sheets give different strategy splits of the same USD 500 million 2027 total (e.g. Buyout 150 vs 175, Private credit 135 vs 65, Infrastructure 0 vs 50), which is realistic drift between a long-range plan and the specific named deals but also means Section 9's "the plan's proportions" is not self-evidently pinned to one sheet. Nothing reads as LLM-written: the PDF prose is terse and numbers-first in the register of real IC memos, and no file name, sheet name or column name announces a trap or a method.

### Rulings (main thread, 2026-11-13)

- Q1 and Q5, the policy's sentences (window, net cash needs, reserve factors, spending, first close, release at term end, the benchmark rate, the late-statement value, the USD 25 million steps): harmless; each executes to the golden's reading, and section 8 leaves the calls' method open as designed.
- Q1 and Q6, the half-year calls and distributions read as a base case: fix; the prompt now asks for them in the policy's stress, and the answer blocks say so.
- Q5 item 8, two 2027 splits in the pacing plan: fix; the long-range sheet's 2027 row is now the year's named funds by strategy, and its notes say infrastructure resumes in 2028.
- Q5 item 7, a third late statement (WX-VC-161): harmless; that fund's term ended on 30 September 2026, its final statement released its commitment and it takes no part in any result.
- Q3, the plan's notes, the survey's provenance and the holdings report's pointer row: harmless (the organisations' own notes, no method or figure).
- Q4, the investment policy statement's allocation targets and the plan's 52 per cent: harmless; a distractor the liquidity test never references.
- REVIEW lines (a), (b) and (c): harmless, as the reader found.
- Realism: no fix.

### Solver's-eye read, pass 2 (the final cut: prompt names the stress on the half-year asks; policy section 4 pins the reserve; the plan's 2027 split made one)

### 1. Which sentence or file tells you how any part of the analysis should be done

`wexmoor_endowment_liquidity_policy_2025.pdf` is written to spell out the test's mechanics (population, window, comparison), which is expected for this kind of task since the WHAT must be filed for determinism. The clearest method sentences:

- "Net cash needs over the eight quarters are the spending distribution, plus the capital calls on every private commitment (those made by 31 December and the budget's new commitments), less the distributions from the private funds." (section 3, the governing formula and population)
- "The spending distribution of each quarter is one quarter of the distribution the trustees approved for the fiscal year in which the test is run." (section 3)
- "Commitments to funds that have not held a first close count in full." (section 3)
- "A commitment's part not called when its fund's term ends is released and does not count." (section 3)
- "Public equities stand at 85 per cent of their 31 December level in the first quarter and 70 per cent in the second, then recover five points a quarter to 100 per cent." (section 6)
- "each fund distributes its value at 31 December times the distribution rate of its strategy in the matching quarter from the third quarter of 2008 in the industry cash-flow benchmark: the benchmark funds' distributions in that quarter over their value at the end of the previous quarter, each summed over the strategy's funds." (section 7)
- "A budget's new commitments are spread across the funds of the year's pacing plan in the plan's proportions." (section 9)

The one place the policy explicitly declines to give a method is capital calls: "Capital calls in the stress are those the endowment's own managers can be expected to make in the stress, judged from their record in the endowment's funds." (section 8) That is the open HOW; everything else above is a filed WHAT.

### 2. Which file already ranks or scores the candidates on the prompt's question

None. No file states a pass/fail verdict for any budget size, and none proposes or implies a maximum committable figure beyond the USD 500 million already named in the prompt itself. `corrigan_hart_pacing_plan_2027.xlsx` only proposes a budget and its five-fund split; its "Notes" sheet gives rationale ("Commitments are sized to keep the private allocation near its 52 per cent policy target by 2031") but never runs or references the liquidity test. No file contains the words "pass," "fail," "headroom," or a computed reserve shortfall/surplus.

### 3. Which file exists only to help the analyst

- The "Notes" sheet inside `corrigan_hart_pacing_plan_2027.xlsx` (advisor commentary, dated for discussion, not data).
- The "About" sheet inside `peer_endowment_survey_2025.xlsx" ("Survey of private university endowments... Compiled by Corrigan Hart LLC from responses received by 30 September 2025"), and arguably the whole survey: it is anonymised peer context (Peer 01 to Peer 24) useful for a memo's framing but not required by any figure the prompt asks for.
- A single trailing line inside `liquid_holdings_2026-12-31.xlsx`: "Private funds at capital account value are reported separately (capital account statements)." This is a pointer, not data, telling the reader where NOT to look in this file.

### 4. Which figure or name reads as the answer rather than context

Nothing reads as a planted final answer. The two cleanest round numbers in the pack are the USD 500 million pacing-plan total (already disclosed in the prompt itself, so not a hidden leak) and the USD 1,200 million minimum reserve ("For the 2027 budget the minimum reserve is USD 1,200 million"), but the latter is explicitly framed as a policy threshold/parameter, not a result, and the rounding rule ("Budgets are set in multiples of USD 25 million") is a constraint on the answer's granularity, not the answer. No file contains a dollar figure labelled as a recommendation, cap, or verdict.

### 5. Filed sentences that literally fix a figure's computation or population, with two-way readings flagged

Fixed literally (stated in words, no numbers computed here):

- Net cash needs = spending distribution + capital calls on every commitment held at 31 December plus the new budget's commitments, minus distributions from the private funds, over the eight quarters. Population for capital calls is explicitly both the existing book and the new money, not one or the other.
- A fund with no first close yet has its full commitment, not a judged partial draw, treated as a capital-call need. Checked against `private_commitment_register_2026-12-31.xlsx`: exactly four existing funds carry status "pending first close" (Thornwick Capital VI, Kelstone Equity V, Rudgely Equity VII, Brackley Growth VIII), each with a "First close expected at commitment" date in Q3 or Q4 2027 and no fund size yet, consistent with the rule.
- The liquid reserve is the sum of each `liquid_holdings_2026-12-31.xlsx` holding's 31 December market value times its policy liquidity-class percentage (cash/MMF/Treasuries 100 per cent, investment-grade bonds 90 per cent, public equities 70 per cent, hedge funds redeemable within the eight quarters 90 per cent, everything else 0 per cent), with no revaluation along the stress path. The workbook's own "Policy liquidity class" column already carries this classification verbatim.
- The public-equity and short-rate stress path is a closed, self-contained eight-quarter schedule (85, 70, then +5 points a quarter to 100 per cent; rates +2.5 points flat) applied to the current 31 December dollar value, not derived from any historical index.
- The distribution rate used on each fund's 31 December value is a pooled ratio: sum of the matching strategy's benchmark funds' distributions-as-percent-of-commitment in the matching historical quarter, divided by the sum of the same funds' NAV-as-percent-of-commitment in the prior quarter (not an average of each fund's own ratio).
- Where a manager's Q4 2026 statement has not arrived, the 31 December value is the Q3 ending NAV plus Q4 calls minus Q4 distributions as the custodian recorded them. Checked: `capital_account_statements_2013Q1_2026Q4.csv` is missing a 2026-12-31 row for WX-BO-102 and WX-BO-113 (both "investing" status, so genuinely pending, not funds whose term already ended); `custodian_cash_activity_2026Q4.csv` carries a capital-call entry for each of them inside Q4 2026, so the reconstruction is fully executable.
- A tested budget's new money is split across the pacing plan's five named funds in its stated proportions (150/100/45/70/135 of the 500 total), whatever total is being tested, not reallocated to other strategies.

Flags (sentences or tables that could be read two ways, or where the prompt leaves something unpinned):

- "the distribution the trustees approved for the fiscal year in which the test is run" could be read as one fixed fiscal year's amount held flat for all eight quarters, or as a distribution that steps up each time a fiscal-year boundary is crossed inside the window (the window spans FY2027 through FY2029). `spending_distributions_FY2014_FY2027.csv` only carries figures through FY2027 (286.5, already quarterised as 71.62/71.62/blank/blank) and I found no Higher Education Price Index series anywhere in the pack, so the stepped reading cannot actually be executed from the filed data; only the flat reading is literally computable. A hurried reader who assumes stepping without checking for the missing HEPI input could still improvise a wrong escalation.
- "Commitments to funds that have not held a first close count in full" fixes the amount but not which half/quarter inside the eight-quarter window it lands in. The only data anchor is each fund's "First close expected at commitment" date; using it is a reasonable inference, not a stated rule, so this is a genuine open judgment rather than a literal instruction.
- Section 4's note that "the factors stand for the stress in section 6, so the holdings are counted at their 31 December values and not revalued along its path" is easy to misread as instructing you to apply BOTH the liquidity-class haircut and the section 6 equity/rate shock to the same holdings. Read literally it means the opposite: the liquidity factors substitute for revaluing along the stress path, so the section 6 equity and rate path is not applied to the liquid reserve at all.
- `market_series_quarterly_2000Q1_2026Q4.csv` carries the real 2008Q2 to 2010Q2 `public_equity_total_return_index` and `exit_activity_index_2015_100`. I checked the real index's path relative to its 2008Q2 level across the eight quarters (about 91, 83, 66, 70, 75, 84, 88, 95 per cent) against the policy's stated path (85, 70, 75, 80, 85, 90, 95, 100 per cent): they are materially different. Using the real historical index instead of the policy's literal percentages would change the equity stress figure. I could not find anywhere in the filed text that the "exit market... read on the exit activity index" sentence (section 6) connects to an operative formula for any figure the prompt asks about; sections 7 and 8 are each self-contained without reference to it, so it reads as scenario narrative rather than a required input, and the short-rate and 10-year yield columns likewise do not appear to feed any asked figure.
- `industry_fund_cashflow_benchmark_2000Q1_2026Q2.csv` carries a "contributions_pct_of_commitment" column that mirrors the "distributions_pct_of_commitment" column used for the distributions formula (section 7). Section 8 assigns capital calls to a different population (the endowment's own funds' record), so reusing the benchmark's contribution rate for calls by analogy with the distribution formula would be applying the right-looking formula to the wrong population.
- The prompt's own wording, "the policy's net cash needs over 2027 and 2028," does not say whether it wants one combined eight-quarter figure or something split by year; "the headroom left above the minimum reserve" is singular and the policy's test is run once, so one figure is the natural reading, but it is worth a reviewer's eye alongside the net cash needs phrasing.

### 6. One thing that would make most of the prompt routine, and what each part turns on

No single file, sentence, or column stands out as a one-fact unlock. The nearest candidate is a projection method for section 8's capital calls (the only place the policy leaves the HOW open), because it feeds the budget search, the net cash needs and headroom figure at USD 500 million, and half of the capital-calls-by-half grid. But naming a method would not hand over numbers: the endowment's own capital account and manager-activity history only starts in 2013, so there is no own-fund record of the actual 2008-2010 window to replay, and a real model has to be built from each fund's lifecycle stage (investing versus harvesting, per the register) across roughly 90 funds. I checked that all five of the pacing plan's 2027 managers (Oakhanger, Wendlebury, Corvane, Ewelme, Harpsden) are "Re-up" relationships with three to four prior funds already in the register, so even the brand-new 2027 commitments have a manager-level history to draw on once each passes first close, which is more construction work, not a shortcut. On balance, one sentence here would help two or three of the roughly five to six gradable result-grids at most, not most of the prompt.

Per part:

- Largest 2027 total that passes: analysis (building the full test and searching budget sizes in USD 25 million steps), built on top of several correctly-applied filed rules (first-close override, pacing-plan proportions, liquidity-class percentages).
- Net cash needs and headroom at USD 500 million: the same composite, plus correctly resolving the single-fiscal-year spending reading above.
- Capital calls by half, split by first-close status, for commitments made by end of 2026: the split itself is a direct field read (register status / first close date); the size and timing of the calls is analysis (section 8 has no formula).
- Distributions by half: almost entirely a stated procedure (section 7's formula against the industry benchmark) plus a reconciliation read (the two funds missing a Q4 2026 statement); the main risk is following a rule to the wrong population (the contributions-column look-alike above).
- Commitments not yet called at 31 December 2026 by strategy: mostly a direct read and aggregation (commitment minus called-to-date, or the filed unfunded_commitment_usd field, grouped by the register's strategy column), with the term-end-release rule and the two missing-statement funds as the main "catch this" steps rather than open analysis.

### Realism note

Everything reads as genuine working files rather than padding. The three PDFs are single-page, produced by LibreOffice Writer with distinct creation dates spanning 2024 to 2026, and read in a dry, procedural governance voice with no leak-sounding vocabulary. The five workbooks carry plausible, varied author names (Donna Turner for the university's own registers and holdings, Corrigan Hart for the advisor's pacing plan and survey), distinct creation and modification timestamps, no hidden sheets, and no library-template or toolchain signatures. The two large CSVs (manager_portfolio_activity at 21,568 rows, industry_fund_cashflow_benchmark at 69,675 rows) carry internally consistent structure rather than obvious filler. The messy, authentic touches are notable and look like real operations, not a dressed-up trap: one restated/superseded statement pair, two funds with a lagging Q4 2026 statement that the custodian file patches, 21 liquidated funds whose final statements explicitly release the uncalled balance, and audited financials that mix calendar and 30 June fiscal year ends. The peer survey is properly anonymised (Peer 01 to Peer 24) with a non-round, dispersed set of values. Nothing is named in a way that announces its own role (no "trap," "answer," or similar column or file name anywhere), and the capital plan PDF's explicit disclaimer that "no project draws on the endowment beyond the annual distribution the trustees approve" reads as a genuine, independently coherent document rather than a note written only to carry a decoy.

#### Rulings on pass 2 (main thread, 2026-11-13)

- Spending flat or stepped: harmless; section 3 sets each quarter at one quarter of the approved distribution for the fiscal year of the test, and only that reading is executable (no FY2028 figure, no price index ships).
- The pending funds' timing: harmless by design; the amount is filed and the timing is the slip judgment (J3), which no sentence hands over.
- Section 4's new sentence: harmless; read literally (as the reader reads it) the factors replace any revaluation along the stress path.
- The exit index path read as narrative: harmless; section 8 asks for the calls the managers make in the stress, so the path enters through their behaviour, which is the open method.
- The benchmark's contribution column: harmless; section 8 names the endowment's own managers' record as the basis, which rules the benchmark's calls out.
- One net cash needs figure or two: harmless; "both in USD million" with the policy's single eight-quarter test gives one figure each.
- No fix on pass 2.
