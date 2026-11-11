# leak check, task9

**Verdict: REVIEW.** 41 files read, 51 golden figures and 1 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: million, architecture, record, ostvale, ladder, average, sentence, golden, careful, carried, forecast, return, result, recovery, closed, missed, policy, estimator, review, inside, default, results, platform, carries, method

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `Capital_Review_Policy_2026.pdf`: carries 4 of 5 distinctive words of the committed call: 'Plan USD 665 million of net P&L for 2027 at the draft capital plan'

## 4 design-note vocabulary (REVIEW 2)
- **REVIEW** `Capital_Review_Policy_2026.pdf`: 7 of 25 stump-paragraph terms appear (million, record, result, closed, policy, review); read whether the document names the move
- **REVIEW** `Risk_Model_Methodology_2023.pdf`: 3 of 25 stump-paragraph terms appear (carried, return, method); read whether the document names the move

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 12 client quality check (INFO 2)
- **INFO** `-`: 41 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)

## 8 column names (clean)

## 11 prompt gate (clean)

## Solver's-eye read

One isolated reader (general-purpose, sonnet, medium) on fresh copies of prompt.txt and target/ (2026-11-11, cut 9a328d82):

1. Method-telling text. Capital_Review_Policy_2026.pdf (a governing document, field-level, not a solution) fixes: s5 "Each pod is charged funding on 20 per cent of its capital, at the 3-month Treasury bill rate plus 0.35 per cent a year, accrued on calendar days at the latest published bill rate"; s6 "A pod's PM team is paid 18 per cent of the pod's P&L for the calendar year after its funding charge, when that P&L is positive, and nothing when it is negative"; s4 drawdown halving at 5% / closure at 7.5% "measured on the capital the pod ran before any halving"; s7 alpha = P&L "beyond what a passive holding of the markets it trades would have earned ... on the published market series the platform keeps"; s8(a)-(e) "The plan budgets alpha only: it expects the markets themselves to earn nothing", whole year at planned capital under drawdown rules, net after funding "at the bill rate on the review date", payouts and platform costs, range = 10th to 90th percentile, capacity = "share of its alpha per dollar a pod gives up when its capital doubles, the same share at any size"; s9 hurdle "at least 1.5 per cent a year of net P&L, after the pod's PM payout and funding, on the capital it adds". Risk_Model_Methodology_2023.pdf: factor definitions (MKT, TECH, RATES, CURVE, CREDIT, VOL...), betas on last 252 days, "On a day a series is not published, its last published level is carried forward", plus the version history (CREDIT moved Aaa to Baa in July 2023). The prompt itself names no method.
2. No file ranks pods on the question. draft_allocation_plan_2027.xlsx lists draft capital and Increase/Decrease/No change/Onboarding but no verdict on the hurdle. allocation_plans_2018_2026.xlsx holds past plans with "Return on capital, record (%)" and "Expected P&L" per pod (a historical record-based expectation, not alpha or net of payouts). None.
3. Helper-only files: none obviously. book_code_map_20220401.csv (old pod code to new book id) exists to bridge the legacy and new risk files; the methodology PDF is the only explanatory doc. The ~30 FRED/Cboe series (DAAA, DEX*, IR3TIB01*, DTB3, DGS2...) read as raw inputs and distractors (FX, foreign interbank rates, DAAA are unlisted in the methodology).
4. Nothing reads as the answer. Closest: draft sheet "Change" column ("Increase") and "Total 19146.2 / 21510" capital; Platform costs sheet "Total 218.4". These are context.
5. Literal fixing sentences: (a) s8(a) "expects the markets themselves to earn nothing over the plan year" fixes the expected P&L to alpha only (market drift zero). (b) s9 fixes the hurdle test: incremental net P&L after payout and funding divided by the added capital, compared with 1.5% a year. (c) s8(c) "funding at the bill rate on the review date" fixes funding to a single rate (the 3-month bill as of the review, 20% of capital, plus 0.35%) rather than a forecast path. (d) s8(d) fixes the range as 10th-90th percentile of 2027 net P&L; the prompt's "80% range" is the same. (e) s8(b) fixes population: every pod in the draft plan, full year at planned capital, onboarding pods on their scheduled capital (the draft sheet's last column gives the dates), no departures/new pods, drawdown rules applied. (f) s6 fixes payout 18% of positive per-pod calendar-year P&L after funding, pod by pod (no netting). (g) s7 + s5 with s8(e) define alpha per year as % of capital and capacity as a constant proportional loss per doubling. s10 "The risk system's daily P&L and capital are the record ... month-end statements are the books of account" fixes which source is the record (risk system daily files, not the administrator statements). s2/s3 fix onboarding schedule 25/50/100% at 126/252 trading days.
6. Single thing: none dominates. The nearest candidates are (i) the old-to-new pod code bridge (book_code_map plus the two daily P&L files differing in units, date format and column names: USD vs USD 000, capital in USD vs USD mm) which settles assembly only; (ii) the policy s8(a) "alpha only", which settles the expectation's framing and the market-adjustment need, but not the factor-beta/alpha estimation, simulation, hurdle test or capacity estimation. The policy hands over a lot of the rules (payout, funding, drawdown, onboarding, hurdle), so those parts are rule-following once read; alpha-vs-factor estimation (which series in which regime, e.g. Aaa/Baa switch and carry-forward), the range via simulation, the per-group alpha-since-2017 and the capacity elasticity read as genuine analysis. Per part: expected 2027 net P&L and 80% range: mostly analysis plus following the stated plan rules; pods whose increases fail the 1.5% hurdle: analysis built on the stated rule (rule application for the test itself); strategy-group alpha since 2017: analysis, with the definitions in s7 stated (data semantics: units/code mapping/capital basis); capacity per doubling: analysis (cross-sectional/panel estimation), the "same share at any size" convention filed. Reading-field items (units, dates, code map, the 2022 relabelling, the statements vs risk record) are texture. Nothing visibly planted; the month-end statements file (net_pnl, incentive_accrual) is a possible decoy given s10 names risk system as the record.

