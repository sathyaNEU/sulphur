# leak check, task1

**Verdict: REVIEW.** 18 files read, 49 golden figures and 9 candidate names taken from submission.md, 25 stump terms taken from the design note.

LEAK stops the ship. REVIEW is a reader's call and the /leak-check command's solver's-eye pass reads every REVIEW line. INFO is a sweep that ran and found nothing or was skipped.

Stump terms swept: million, golden, trailing, carries, family, pooled, december, months, onbeperkt, accounts, creation, chosen, platform, hurried, priced, inside, uploaded, nearest, commitment, growth, graded, history, account, missed, measured

## 3 answer figures in the pack (REVIEW 1)
- **REVIEW** `SUL_licence_agreement_2027-2029_schedule_B.pdf`: golden figure 0.40 appears: ...For each month Kraanvogel pays each publisher EUR 0.40 for every counted hour of the publisher's titles...

## 4 design-note vocabulary (REVIEW 3)
- **REVIEW** `growth_planning_guideline_2026-10.pdf`: 4 of 25 stump-paragraph terms appear (months, accounts, growth, account); read whether the document names the move
- **REVIEW** `price_list_2027.pdf`: 3 of 25 stump-paragraph terms appear (december, onbeperkt, nearest); read whether the document names the move
- **REVIEW** `spring_campaign_2027_quote_Bureau_Grauwe_Gans.pdf`: 3 of 25 stump-paragraph terms appear (onbeperkt, growth, account); read whether the document names the move

## 8 column names (REVIEW 1)
- **REVIEW** `licence_server_renewals_2024-01_2026-10.csv`: columns a generator names and an organisation does not: device_id

## 9 dates after the setting (INFO 1)
- **INFO** `-`: no --asof given, sweep skipped (pass the fiction's as-of date)

## 10 container metadata (INFO 1)
- **INFO** `-`: container gate PASS (PASS: 0 FAIL, 0 WARN)

## 11 prompt gate (REVIEW 1)
- **REVIEW** `prompt.txt`: shell quota: deliverable set 'pptx+xlsx' at 24% of 21 prompts (cap 20%); reword at the role level, not the verb

## 12 client quality check (INFO 2)
- **INFO** `-`: 18 usable files (10 or more required)
- **INFO** `-`: 2 file categories: document, spreadsheet (2 or more required)

## 1 file names (clean)

## 2 author vocabulary (clean)

## 5 announcements (clean)

## 6 ranking artifacts (clean)

## 7 hidden content (clean)


## Solver's-eye read

### 1. Which sentence or file tells you how any part of the analysis should be done?

`growth_planning_guideline_2026-10.pdf` is the governing document and it pins several steps literally, not just facts:

- "A paying subscription is a consumer account whose monthly charge for the billing month covering the date was
  collected. Staff and test accounts are not consumer accounts. A charge returned and not re-presented, or refunded,
  is not collected. The paying subscriptions on a plan at a month end are the accounts paying on the month's last
  day, on the plan charged." (3.1) — fixes the population and the month-end test for every headcount the prompt
  asks for (end-of-October 2026 base, end-of-2027 retained base).
- "A subscription's contribution in a period is its net revenue in the period less the remuneration on its
  account's counted hours in the period at the licence agreement's rate." (3.9) — fixes what "contribution" means
  and that remuneration is subtracted at the licence rate in force.
- "A January price rise goes ahead on a plan when it raises the 2027 contribution of the subscriptions paying on
  that plan at 31 October 2026, followed through 2027, against holding the plan's 2026 price." (3.10) — this is the
  literal decision rule: compute 2027 contribution of the Oct-2026 cohort under the new price vs. under the held
  2026 price, and the rise goes ahead only if the new-price figure is higher. It also fixes the comparison
  population (the 31 Oct 2026 cohort, not new signups) and the window (through all of 2027).
- "A rise's extra cancellations and extra downgrades are those at a subscription's first bill at the new price
  beyond what the same months would have brought without the rise, counted among the subscriptions that reach that
  bill." (3.10, second sentence) — fixes the definition of "lost at first bill" and "moved down a plan" as an
  incremental (vs. counterfactual baseline) quantity, not a raw churn rate.
- "Forecasts use the licence agreement in force in the forecast months, the current price list including the
  changes it announces, and the rivals' prices as last scanned, and assume no other change of terms or prices."
  (3.8) — fixes that the forecast must use the 2027 licence schedule and no other assumption.
- 3.3 and 3.5 fix "counted hours" and "net revenue" (VAT, store fee schedule by tenure, refunds) literally.

None of this hands over a number; it hands over the comparison, the population and the window. That is squarely the
kind of filed WHAT the house doctrine expects to be literal (it is a stated convention, not a planted shortcut), but
a solver who reads 3.9–3.10 closely gets the entire decision test for free and only has to supply the arithmetic.

`SUL_licence_agreement_2027-2029_schedule_B.pdf` fixes the remuneration method itself: "For each month Kraanvogel
pays each publisher EUR 0.40 for every counted hour of the publisher's titles in the month" (B2.1) and the counted-
hours definition in B2.2 (first-time-reached position only, re-listening adds nothing). This is the "new per-hour
remuneration" the prompt says "none has been weighed against" — it is the single new input the whole task hinges
the cost side on.

### 2. Which file already ranks or scores the candidates (the plans' rises) on the prompt's question?

None. No file contains a 2027 contribution figure, a go/no-go flag per plan, a churn or downgrade rate, or anything
that already orders the four plans. `kpi_monthly_report_2026-09.xlsx` gives only 2026-to-date paying counts and
aggregate net revenue/remuneration (not split by plan), which is historical context, not a score on the rise
decision. The rivals' price scan and the price list give prices, not a verdict.

### 3. Which file exists only to help the analyst?

`kpi_monthly_report_2026-09.xlsx` — a monthly KPI summary (paying counts per plan, trial starts, net revenue,
aggregate remuneration) through September 2026, with a footnote defining "paying" by cross-reference to the
guideline. It is a sanity-check/orientation file: nothing in it is needed to compute any asked figure (the raw
payments/plan_periods/accounts files carry the same information at full granularity), but it lets a solver
sanity-check its own aggregates against a published series. It is not a distractor (it is clearly relevant) and
not load-bearing either.

### 4. Which figure or name reads as the answer rather than context?

Nothing reads as a precomputed answer. The closest candidate is growth_planning_guideline 3.10's rule itself ("a
rise goes ahead when...") — it names the test but supplies no number, so it is the method, not the answer. No file
states "Flex rise should/should not go ahead" or similar. EUR 0.40/hour (B2.1) and the four 2027 list prices
(price_list_2027.pdf) are themselves just filed inputs, not a figure to be used as output, so I don't read either as
an answer dressed as context.

### 5. Which filed sentence, read literally, fixes how any figure the prompt asks for is computed or over which population?

- 3.1 (paying subscription / month-end test) fixes literally how "the paying subscriptions on each plan at the end
  of october 2026" and the parallel end-2027 figure must be counted: consumer accounts only, charge actually
  collected (not merely billed), on the plan charged at that month's last day.
- 3.9 fixes literally how "the change each rise makes to what that plan's subscriptions... bring in 2027, in euros
  per subscription" must be computed: net revenue minus remuneration at the licence rate, i.e. contribution, not
  gross billings.
- 3.10 fixes literally the population for every per-plan recommendation (the cohort paying at 31 October 2026,
  followed through all of 2027, not new sign-ups) and the comparison (new 2027 price vs. 2026 price held flat).
- 3.10's second sentence fixes literally that "how many of every 100 subscriptions the rise would lose at their
  first bill" and "move down a plan" are incremental effects of the rise (actual minus a no-rise counterfactual for
  the same cohort/months), not simple churn or downgrade rates read off the data.
- B2.2 fixes literally how "counted hours" (the input to remuneration, and hence to contribution) are measured:
  only forward progress past a profile's prior furthest position in a title counts; re-listening counts nothing.
- 3.5 fixes literally what is subtracted to get net revenue (VAT, tenure-dependent Apple/Google store fee, refunds).

### 6. Is there one thing that would make most of the prompt routine? Does each part turn on analysis or on reading a rule?

No single file, sentence, column or visible pattern collapses the whole task. The growth_planning_guideline comes
closest to a "master key" in that 3.9/3.10 fix the contribution formula and the go/no-go test, but applying it still
requires, for each of four plans: reconstructing the Oct-2026 cohort, counted hours per account/profile from a
458k-row renewals file plus listening data, net revenue with store-fee and VAT treatment, projecting 2027 collected
months (needs plan_periods/payments to establish who's still on the plan and when they'd be billed), and then the
incremental cancellation/downgrade rate versus a counterfactual baseline derived from the same plan's own pre-rise
history — split further by NL and BE ("Flanders") for the per-100 figures. That is several independent pieces of
work (cohort construction, remuneration recomputation under the new per-hour schedule, counterfactual churn/
downgrade estimation, country split, aggregation to a 2027 contribution-per-subscription figure), not one lookup.

Breaking the asks down:
- The per-plan "change in 2027 revenue per subscription" and the go/no-go call turn on analysis (contribution
  modelling, applying the new remuneration rate to counted hours, projecting through 2027) — the rule in 3.9/3.10
  fixes *what* to compute, not the number, and counted-hours/contribution still have to be built from raw usage and
  payments data.
- "Paying subscriptions on each plan at end of October 2026" turns mostly on reading 3.1's definition correctly
  (which accounts count, which status) applied to accounts_export/plan_periods/payments — a correct-population
  exercise more than an analytical one, though reconciling plan_periods vs. payments to find the plan actually
  charged still takes real reconciliation work.
- "How many would still be paying at end of 2027 if the rise goes ahead" is a forecasting/retention estimate: it
  requires modelling retention net of the rise's incremental loss (3.10), so it is analysis built on top of the
  defined population.
- The NL/Flanders per-100 lost-at-first-bill and downgrade figures are a genuine estimation task (no historical
  rise at these exact prices exists in the data to read off directly): this turns on analysis (building a
  counterfactual from the base rates and any comparable prior pattern in the data, e.g., price elasticity implied
  by payments/cancellation history), not on reading a single field.

So the task is not a single-fact stump: the guideline supplies the method's definition (as the house doctrine
expects for a filed WHAT), but each number still demands separate construction from several large files, and the
hardest asks (incremental churn/downgrade, 2027 retention) have no rule that computes them outright.

### Flagged files

- **SUL_licence_agreement_2027-2029_schedule_B.pdf** — not a leak of the answer, but it is load-bearing: it is the
  "publisher's new per-hour remuneration" the prompt refers to, and B2.1–B2.2 literally fix the remuneration rate
  and the counted-hours method that every contribution figure depends on. Legitimate governing document, not a
  decoy.
- **growth_planning_guideline_2026-10.pdf** — the most leak-adjacent file in the pack: 3.9 and 3.10 state the exact
  contribution formula and the exact go/no-go comparison. This is a filed convention (consistent with "the WHAT is
  filed, the HOW stays open"), not a solved number, but a careless solver who skips straight to 3.10 gets the whole
  decision test handed to them; the work is still in building the four plans' figures from raw data.
- **price_list_2027.pdf** — harmless; it is simply the source of the 2027 prices (and the 2026 prices for
  comparison) that the prompt requires and that no other file states. Also carries the operationally relevant
  details that the rise "may still be withdrawn for a plan until 30 November 2026" and that subscribers are told by
  e-mail on 1 December 2026, neither of which leaks a method, just context for why the forecast is forward-looking.
- **spring_campaign_2027_quote_Bureau_Grauwe_Gans.pdf** — harmless with respect to the price-rise question; it
  prices a 2027 acquisition campaign (fee per trial start by lead plan) that is not part of what the prompt asks
  (the prompt is about existing Oct-2026 subscribers and the rise's effect on them, not new trial economics). It
  reads as a plausible distractor: relevant-looking (same plans, same year) but not used by any of the four asked
  quantities. Not labelled as a distractor anywhere in the file or its name.
- **licence_server_renewals_2024-01_2026-10.csv, column `position_s`** — harmless; it is simply the furthest
  position (in seconds) reached by a profile in a title at that renewal timestamp, which is exactly the raw signal
  B2.2 needs ("the furthest position... as reported by the app"). It is a plain data column, not a leak; computing
  counted hours from successive `position_s` values per profile/title is real reconciliation work (458,597 rows,
  no pre-aggregation).

### Realism

- All four flagged PDFs carry `Producer: LibreOffice 26.8.2.2 (AARCH64)` / `Creator: Writer`, consistent across the
  pack and consistent with the house rule that shipped PDFs are word-processor exports, not FPDF/ReportLab. No stray
  library template or matplotlib signature seen.
- The KPI workbook's document properties show a human creator/last-modified-by ("Hugo Brouwer") and a plausible
  creation/modification date trail (Jan 2026 to Oct 2026), not an LLM or library default.
- All document dates sit between March 2025 and 9 November 2026, i.e. before today (13 November 2026) and before
  the setting's own forward horizon; nothing postdates the task's present.
- The growth_planning_guideline skips section numbers (2, 4 and others never appear, jumping 1 to 3 to a changelog)
  — reads as a real document with sections removed/renumbered over versions, a benign realism tell, not a leak.
- No file name or visible content announces itself as a "trap," "decoy," or names the stump; the campaign quote and
  the KPI workbook are unlabelled and look like ordinary business documents.

### Verdict

NO LEAK (growth_planning_guideline_2026-10.pdf §3.9/3.10 states the contribution formula and the go/no-go
comparison as a filed convention, which is expected and still leaves the per-plan cohort construction, remuneration
recomputation, 2027 projection and NL/Flanders incremental churn-and-downgrade estimation as real analytical work;
no file ranks, scores or pre-answers the four plans' rise decisions).

Main thread's rulings (2026-11-13): question 1 and 5 quote guideline 3.1, 3.8, 3.9, 3.10 and schedule B 2.1 to 2.2, which file each result's population, comparison, window and unit (the WHAT, house doctrine) and never a method; harmless. Question 3 names the KPI workbook, a reconciliation source the raw files reproduce; harmless. Every flagged REVIEW line harmless. Verdict: no leak.
