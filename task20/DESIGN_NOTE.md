# task20: which of the Small and Mid Cap Facilitation desk's VaR exceptions in the 250 days to 30 June 2025 the model answers for, and the add-on to hold on the second-half book

Architecture 1, drawn 2026-11-11 from the author's concept note (Concept 1, "Why the desk breached VaR"), moved from a
fully generated credit book to an equity facilitation desk whose market layer is the published tape: the S&P 500 closes
from Cboe and the Nasdaq-100 closes from FRED, pulled 2026-11-11 and shipped as published up to 30 June 2025. The
desk's names, books, trades, P&L, risk engine and documents are simulated by the generator on that tape (seed 1114).
`generator/figures.json` carries every figure below at the precision the answer blocks state.

## Draw

Subdomain: Quantitative Finance (Quantitative Finance and Trading), task type Risk modeling (VaR/ES, stress testing,
  credit and counterparty risk), carded under the taxonomy key `factor-return-attribution`, the one Quantitative
  Finance task type that serves Root-Cause
Analysis type: Root-Cause
Answer shape: A timeline of what went wrong and when: every exception date of the year under one heading of the bank's
  backtesting standard, the engine's input failures dated, the headings adding back to the total, the count and zone a
  sound model shows, and the add-on the standard requires on the planned book month by month
Weight: investigation: most of the work is forming a cause for each exception, testing it by re-running the engine
  with that fault removed, and ruling it in or out; the last three live builds sat on validation (task9), metric or
  rule design (task13) and synthesis (task15)
Data-native sentence: the desk's P&L, its position systems' nightly extracts, the order blotter and the risk engine
  each hold the book on a different clock, so an exception only gets a cause once the book the forecast was about is
  rebuilt from the blotter's booking times against each extract's cut and the engine is re-run with each fault
  removed, on a real market tape whose volatility rose in bursts a two-year equally weighted window could not follow.
People: Nancy Ayala (head of Market Risk Control, files the classification), Christopher Reilly (desk head, Small and
  Mid Cap Facilitation) (`guard.py names --geo us --seed 1911`). Neither appears in the prompt.

- **Card:** `.claude/skills/fingerprint/cards/task20.json`, registered 2026-11-11 (filed first as task19 and moved when
  another session took that number). `guard.py check`: WARN only. Answered here: `skeleton.lesson_taught` and
  `skeleton.house_lesson` (heterogeneity carried to the decision): the planned book's segment split is a supporting
  step the careful pass earns; the call turns on the extracts' record as of their cut and on the engine's unmetered
  component (the proxied names' own moves), which nothing on file teaches.
- **World:** Tarrant Hale Securities LLC, the broker-dealer of a regional bank holding company in New York. Its Small
  and Mid Cap Facilitation desk makes markets in 190 Nasdaq-listed small and mid caps (every name invented), takes
  client closing-auction orders as principal and hedges with E-mini S&P 500 and E-mini Nasdaq-100 futures. The
  setting is 14 July 2025: the quarter's backtest put the desk in the red zone, and the supervisor's review asks for
  the classification by 31 July.
- **Forum, forcing event, organisation family:** regulator_or_inspector, audit_or_inspection, financial_institution.
- **Deliverables:** a workbook and a one-page PDF note (`exception_classification_2025Q2.xlsx`,
  `backtesting_note_2025Q2.pdf`).
- **Retrospective call, with its reason:** an exception classification is a review of a closed window by definition;
  the forward-facing part of the call is the add-on the desk holds on its planned book for each month of July to
  December 2025, which the standard requires before each month starts.

## Deep reasoning

Task type: Risk modeling (VaR/ES, stress testing, credit and counterparty risk), Quantitative Finance, carded as
  `factor-return-attribution` (serves Root-Cause): each result is a market-risk quantity the field estimates (the
  exceptions on two P&L measures, an engine's VaR on a given book, a full own-history VaR, a volatility-filtered VaR,
  an add-on for risks not in VaR) and the call is the supervisor's exception classification.
Domain test: a market-risk validator replicates the engine from its methodology, rebuilds the book the forecast was
  about, re-runs the engine with each fault removed (the book the desk held, every name on its own history, scenarios
  that follow volatility) and assigns each exception to the first fault that answers for it; the add-on is the gap
  between the own-history VaR and the engine's on the book the desk plans to run, month by month as the engine's
  mapping changes.
Swap: put a hospital's readmissions or a utility's outages in the call ("which of the ward's readmissions does the
  model answer for, and the add-on on the planned ward") and nothing survives: there is no quantile forecast, no
  static book revalued at closes, no scenario window to re-run, no proxy mapping, no supervisor's exception headings.
Where the weight sits: the engine's inputs (R3). ERE replicated from the methodology note on the extract each run read
  matches the run log to the dollar, so the engine looks sound and its input failures look like the 27 runs the log
  flags; but the book the forecast was about is in no file. Each EQX and FUTS extract is cut as the run starts, around
  18:30, and the middle office books the day's closing-auction allocations after it (a median USD 39.2 million gross a
  night); the close book is the extract plus the blotter's later bookings for that trade date or earlier, and only on
  that book do 4 exceptions turn out to be the inputs' and the 2 on reused extracts turn out not to be.
Layer 1: EQX's January 2025 migration (two extract schemas, new instrument ids through a crosswalk, the 17 January
  extract in both files); the vendor's two re-sent days (every row loaded twice) and one name's ticker change (its
  vendor id stable); the blotter's versions (fat-finger amendments and duplicate tickets cancelled before the evening
  extract, allocations moved between client accounts after it), client tickets booked the next morning under their
  trade date, and 25 lines the export repeats; product control's nine fee postings restated the next morning, mirrored
  by next-day general ledger postings under the original value date; four failed runs re-run on the extract their
  first attempt read; FUTS snapshots stamped in UTC. None decides a result: `checks.py` R2 asserts each one mishandled
  moves no heading, no exception and no add-on, or breaks the replication against the run log.
Not one thing: the strongest single piece is the closing allocations the extracts miss (R3), and a run that nails it
  still has to take both P&Ls (R1), find the reused extracts (R2), replicate ERE and re-run the own-history and
  volatility-scaled counterfactuals over the year (R4, R5), build the plan's book by segment (R7) and carry the
  store's graduations through the half (R8).
One-fact test: "ERE's position extracts are cut as each run starts, before the middle office books the day's
  closing-auction allocations" rescues R3, R4 and R6 (3 of 9); "the engine moves names onto their own history through
  the half as the store reaches 500 returns" rescues R8 alone; the call needs both, so no single sentence rescues it.
Not semantics: every field read right (both P&Ls, the run log's extract ids and cut times, the store rule, the plan's
  basis) still leaves R3, R4, R6 and R8 wrong: no field says what an extract was missing, and neither the plan nor the
  standard says how the engine's mapping moves through the half.
Not rule application: the standard files the headings, their order and what each counterfactual must cover, and the
  engine note files the store rule; no filed procedure rebuilds the close book from booking times, replicates the
  engine, scales scenarios to volatility, builds the planned book or projects the store over the half.
Estimand: MRS-4 3.1 to 3.4 (booked P&L, hypothetical P&L, an exception on either, the VaR reported for a date); 4(a)
  to 4(e) (the five headings, the first that accounts for it, (c) to (e) against the model); 5 (the corrected count
  over the period on the hypothetical P&L and the zone table); 6 (the add-on: the own-history VaR less ERE's on the
  same planned positions and window as ERE will report it for the month's first business day, floored at zero); the
  plan's months, segment targets, hedge and basis (the engine's 30 June run); the engine note's window, quantile,
  store rule and betas; the prompt pins the 250 trading days to 30 June 2025 and July to December 2025.
No decoy: nothing is written to carry a wrong answer. The official backtest (15 booked exceptions, red) is the
  incumbent figure, the right computation of a shallower quantity that every run reproduces (R18), priced on the
  golden's footing by R1. The run log's VaRs are exactly what ERE produced on what it read. No memo argues a cause.
No replay: no result re-derives a published figure and no shipped number is wrong: the official file, the run log,
  the extracts and product control's P&L are exact records of what the bank's systems produced.
Pinned: every rival run on the clean truth lands inside its band or is ruled out by named data (Semantic fork table):
  the volatility response at decay 0.94 to 0.97, scaled at the portfolio or name by name, keeps the sound count at 0
  to 2 (green) and the volatility heading at 2 to 3, with 14 February and 28 March 2025 moving between (d) and (e) and
  every other row holding; the interpolated quantile moves one inputs date and is ruled out by the note's fifth-largest
  loss; the add-on's mapping is pinned by MRS-4 3.4 and 6 and the note's store rule, and the rivals (the month's
  first run's mapping, a business day earlier, fractional shares and contracts) stay inside every month's band.
Run forecast: R3 lost to a stopped first story and a self-confirming check (the replication matches the run log; the
  reused extracts are the input failure the log flags; re-run on that day's extract, two exceptions are covered and
  filed under inputs); R4 and R6 lost through it; R8 lost to a stopped first story (the plan's ramp explains the
  monthly change) and an unfinished chain (the store rule used to replicate the backtest and dropped for the half);
  R9 through R3 and R8. R1, R2, R5 and R7 are earned by careful runs (reflexes R18, R14, R20).
Strategy label: WORKS IN FORM (the client's Quantitative Finance strategies 1 and 2 give the lesson: risk systems
  simplify, volatility clusters; neither's shape is used: no P&L explain metrics, no monitoring rule)
Depth level: 5: six independent judgments (the P&L the forecast was about; the book the engine read against the book
  held; the omitted own-name risk; the volatility response; the plan's book by segment; the store's schedule through
  the half), each moving a graded figure, and the shortcuts land on different wrong answers (15 booked, red; 2 inputs
  from the reused extracts with 16 against the model; 13 with the proxies kept, red; an add-on held at July's 0.32 or
  rising to 0.40 with the ramp; 0.40 falling with the graduations alone; 0.19 to 0.22 scaled in proportion).
Lesson: an exception is only the model's once the book it was asked about is rebuilt from the record's own clock, not
  taken from the extract the engine read, and an add-on follows both the book the desk will run and the dates the
  engine stops proxying; no build on file teaches a nightly extract's record as of its cut or a quantile engine's
  unmetered component.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | every exception of the period on either P&L: 19 (15 booked, 18 hypothetical; 4 on hypothetical only, 25 Sep 2024, 23 Oct 2024, 10 Feb 2025, 2 Apr 2025; 1 on booked only, 3 Apr 2025) | assembly and reconciliation | MRS-4 3.1 to 3.4; product control's P&L; the run log | exact | first story (quick pass): the official file's 15 booked exceptions taken as the population; the careful pass takes both P&Ls (reflex R18) | - | Component 1 |
| R2 | the runs that read an older extract: 27, dated, with the 2 exceptions on them (4 Nov 2024, 5 Feb 2025) | investigation | the run log's extract ids and messages against the extracts | exact | first story (quick pass): the run log never opened; the careful pass reads it (reflex R14) | - (the run log and the extracts) | Component 2 |
| R3 | the exceptions the engine's inputs caused: 4, every one by closing allocations booked after the extract (2 Aug 2024, 5 Aug 2024, 23 Oct 2024, 4 Mar 2025); the reused extracts caused none | investigation | MRS-4 4(b); the blotter's booking times against each extract's cut; the engine note | exact | stopped at the first story and a self-confirming check: the replication matches the run log, the reused extracts are re-run on that day's extract and the two exceptions on them filed under inputs (L26, L28) | R1 (the blotter, the extracts and the run log) | Ask 2 |
| R4 | the exceptions the model's omitted risks answer for: 11, dated | decomposition and attribution | MRS-4 4(c); the vendor's closes and the mapping | exact | stopped at the first story (through R3): 12 on the extract book, the four allocation nights among them and the two reused nights out (L26, L28) | R1, R3 | Component 3 |
| R5 | the volatility heading (2: 28 Mar 2025, 6 May 2025), the sound model's count over the year (2: 6 Sep 2024, 14 Feb 2025) and the zone (green) | modeling | MRS-4 4(d) and 5; decay 0.94 to 0.97, portfolio or series | volatility 2 to 3; count 0 to 2; zone exact | first story (quick pass): the official 15 and the red zone; the careful pass runs the filtered simulation (reflex R20) | R1 (the book and the own-history scenarios) | Ask 3 |
| R6 | every exception dated under one heading: 19 rows (other income 1, inputs 4, risks not in the model 11, volatility 2, model accuracy 1) | synthesis | MRS-4 4 | exact per row; 14 Feb and 28 Mar 2025 (d) or (e) | stopped at the first story (through R3): nine rows under another heading (L26, L28) | R1, R2, R3, R4, R5 | Ask 1 |
| R7 | the add-on for July 2025 on the planned book: USD 0.32 million (own-history VaR 2.24 million against ERE's 1.92 million) | forecasting | MRS-4 6; the plan's July targets, hedge and basis; the engine's 30 June run | 0.24 to 0.34 | method shortcut (quick pass): the 30 June add-on (0.18) carried over; the careful pass builds the plan's book (reflex R20) | - (the plan and the 30 June run) | Component 4 |
| R8 | the add-on for August to December 2025: 0.27, 0.11, 0.08, 0.03, 0.00 (USD million), as ERE's proxied names fall from 82 to 67 | forecasting | MRS-4 3.4 and 6; the engine note's store rule; the mapping's store start dates; the plan's months | each month's band (0.25 to 0.31, 0.09 to 0.13, 0.06 to 0.10, 0.01 to 0.05, 0.00 to 0.02) | stopped at the first story and an unfinished chain: the plan's ramp priced on the 30 June mapping, 0.28, 0.25, 0.30, 0.40, 0.40 (L26, L11, N06) | R7 | Ask 4 |
| R9 | the call: 14 of the 19 exceptions count against the model, 4 are the inputs' (the allocations; the reused extracts none), a sound model shows 2 (green); hold USD 0.32 million in July falling to nil by December | synthesis | R3, R4, R5, R8 | the figures in their bands | stopped at the first story (through R3 and R8): 16 against the model, the reused extracts blamed, the add-on rising to 0.40 (L26, N06) | R3, R4, R5, R8 | Recommendation |

Carry-forward: R2 and R3 each read inputs of their own (the run log with the extracts; the blotter's booking times
with the extracts' cut times), and R7 reads the plan and the 30 June run, so a run that slips on one still earns the
others. R4 needs R3 (the inputs heading comes first), R5's count runs over the whole year on the book held and is
graded on its own, R6 falls with any of R1 to R5, R8 with R7, and the call with R3, R4, R5 and R8. No analytical result
is the only analytical input of more than three of the other eight.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Closing-auction allocations booked after the extract is cut | constructed by the simulated middle office, every business day (median USD 39.2 million gross a night, more after big moves) | no: 249 of the 249 runs the blotter covers miss some; the gap moves the VaR both ways (too high on 129 runs) and decides 4 of the 19 exceptions | investigation: the blotter's booking times against each extract's cut time | modelling: the close book rebuilt and the engine re-run on it for every exception | keep |
| Extract reuse on feed failures | constructed by the simulated feed, 27 runs | no: 2 exceptions fall on reused runs and neither is caused by the reuse | one look at the run log, then modelling | modelling: the re-run on the book held shows the reuse decided none | keep |
| Proxied names' own moves (names with fewer than 500 store returns mapped to an index by beta) | constructed by the simulated desk's onboarding, every name every day (the proxied share of the book 31 to 40 per cent each quarter) | no: the engine runs short of the own-history VaR in every quarter, exception or not | modelling: an own-history VaR on the same book | modelling: the engine re-run with every name on its own history | keep |
| The volatility rise of 2024 to 2025 against a two-year equally weighted window | real: the S&P 500 and Nasdaq-100 tape as published, carried into every name | no: it shapes every name's moves through its index | modelling: a volatility-filtered VaR | modelling: the scenarios rescaled by EWMA volatility | keep |
| The store's graduations through the second half | constructed by the onboarding dates: 87 names proxied at 30 June, 67 by December | no: graduations run through every month of the half and through the backtest year | modelling: the store rule applied to each name's start date for each month's run | modelling: the engine re-priced on each month's mapping | keep |

No factor sits only in the units it decides: the cutoff misses allocations on every run, the reuse spans 27 runs of
which none decides an exception, the proxies run short every quarter and the store graduates names every month.
`checks.py` asserts each footprint, including the runs on which the missing allocations overstated the VaR.

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 every exception of the period on either P&L | Missed | Right | Right |
| R2 the runs that read an older extract | Missed | Right | Right |
| R3 the exceptions the engine's inputs caused, and those the reused extracts caused | Missed | Missed | Right |
| R4 the exceptions the model's omitted risks answer for | Missed | Missed | Right |
| R5 the volatility heading's count, the sound model's count and the zone | Missed | Right | Right |
| R6 every exception dated under one heading | Missed | Partly | Right |
| R7 the add-on for July 2025 on the planned book | Missed | Right | Right |
| R8 the add-on for each month from August to December 2025 | Missed | Missed | Right |
| R9 the call | Missed | Missed | Right |
| Roughly | 0 of 9 | 4.5 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "ERE's position extracts are cut as each run starts, before the middle office books the day's closing-auction allocations"; rescues 3 of 9 results (R3, R4 and R6)
Pair estimate: 45.6

The careful pass is graded up on purpose, to the Sulfur run record: it takes both P&Ls, replicates ERE from the note
on the extract each run read (matching the log to the dollar), re-runs the reused-extract nights on that day's extract,
re-runs the own-history and volatility-filtered counterfactuals in the standard's order and over the year, and builds
the plan's book by segment for each month. It takes the extracts as the book held, so the four allocation nights go to
the model and the two reused nights to the inputs, and it prices the plan's ramp on the 30 June mapping.

## Frontier check

Precedents: R3 L26 (a plausible shallower explanation that passes its own checks: the reused extracts, which the run
  log flags and a re-run on that day's extract confirms) and L28 (the estimator certified with a check that cannot see
  the problem: ERE replicated on the extracts matches the run log to the dollar); R4 and R6 L26 and L28 through R3;
  R8 L26 (the plan's ramp as the story of the monthly change), L11 (the split built for one step and dropped for the
  next: the store rule applied to replicate the backtest and not to the half) and N06 (long-run behaviour assumed
  unchanged over the horizon); R9 L26 and N06. The same ids sit on each result in `generator/effort.json`.
Shallow path checks: R3: the hurried route passes its own checks (the replication matches all 251 runs in the log; the
  27 reused runs stand out by their extract ids and messages; re-run on that day's extract, both exceptions on them
  are covered); the check of another kind is the blotter's booking times against each extract's cut time, at the
  trade grain against the run grain, then the engine re-run on the book held. R4 and R6: the hurried headings add back
  to 19; the refuting check is the same re-run. R8: the ramp-only path passes against July and August and against the
  plan's own growth; the refuting check is the mapping's store start dates against the note's 500-return rule, by
  which 20 of the 87 proxied names move to their own history between July and November.
Assumption made false: "the extract ERE read is the book the desk held at the close, except on the nights the feed
  failed" (the extracts are cut as the run starts and the middle office books the closing allocations after it, every
  night; the blotter's booking times test it); "ERE will proxy the same names through the half" (the store reaches 500
  returns for 20 of them by December; the mapping's store start dates and the note's rule test it).
Forcing: the line is the green zone's edge (a sound model's count of 4 or fewer). The golden family (decay 0.94,
  0.95, 0.96 and 0.97, scaled at the portfolio or name by name) gives 0 to 2, the nearest 2.5 below the line; the
  shortcuts land across it: the booked P&L on the reported VaR 15 (red) and the book held with the proxies kept 13
  (red), the nearest 8.5 above. Two routes land on the golden's side of the zone and are graded elsewhere: no
  volatility response gives 3 (green, the volatility heading then empty) and the extract book gives 2 (green, the
  inputs heading then the reused nights). Perturbations: the quantile interpolated (2), decay 0.99 (3), a 250-day
  window (1): the zone holds. The add-on's golden family (the month's first run's mapping, a business day earlier,
  fractional shares and contracts) stays inside every month's band against the ramp-only, graduation-only and
  proportional paths.
Noun swap: the nearest on file by `skeleton.py check` share only the supporting lesson (heterogeneity carried to the
  decision) with task12 v1, task16 v2, example 7 and depth 5a6e4e0c, at severity none; swapping a ward's readmissions
  or a fleet's failures into this task carries no decision form (a per-unit diagnosis of exception days), no deciding
  lesson (a quantile engine's unmetered component; a nightly extract's record as of its cut), no detection (booking
  times against extract cut times) and no file roles (a run log, a blotter, a mapping with store dates) across.

## Data provenance

Source: the market layer is published: S&P 500 daily closes from Cboe's index history download and the Nasdaq-100
  daily close from FRED (series NASDAQ100), pulled 2026-11-11, kept byte for byte in `generator/raw/` with their
  sha256 in `generator/raw/manifest.json` and shipped as published up to 30 June 2025 (the VIX closes drive the
  simulated names' volatility and are not shipped); everything else is generated by the generator from a simulated
  process on that tape (the names, the desk's flow and books, the middle office, product control, the ledger, the risk
  engine and its feeds, the documents).
Behaves like the real thing: each name's daily return is its beta to the published S&P 500 (and, for technology and
  communication names, to the Nasdaq-100's excess over it) plus a sector factor and a fat-tailed residual whose
  volatility follows the published VIX, with earnings gaps in the reporting seasons and rare news jumps; the desk's
  client flow leans against the day's move and swells with it, its client closing-auction orders swell after big
  moves and are taken as principal and hedged in futures at the close, its fees scale with flow, and its booked P&L
  carries same-day trading, commissions, fees, month-end reserves and funding (BCBS 1996; Berkowitz and O'Brien 2001).
Genuine patterns: (1) volatility clustering from the published tape, through every name; (2) earnings-season gaps four
  times a year per name and fat-tailed residuals; (3) client flow and closing orders that swell on big-move days, so
  income and allocations peak around loss days; (4) month-end reserve postings; (5) the desk's book drifting into newer
  small caps as names are onboarded, and the store graduating them 500 returns later.
Problems by process: the extracts are cut as the nightly run starts and miss the allocations the middle office books
  afterwards (the allocation step); the extract feed fails and the engine reuses the last extract it received (the
  feed); EQX's migration changes schema and ids and replays its cutover day (the migration); amendments, cancels, next
  morning bookings and repeated export lines in the blotter (middle office practice and the export); fee postings
  restated the next day (finance's close); failed runs re-run (the vendor's late file).
License: Cboe index history is published by Cboe for public download; FRED series are reproducible with attribution
  under FRED's terms (Nasdaq for NASDAQ100); values reproduced unaltered with source and pull date recorded; the
  generated files CC BY 4.0 (original work)
Used as is: the two published index series are shipped and used as published (cut at the quarter end, no value
  altered); the generator reads each close and computes returns.
Breadth: 20 files; 190 names over 773 trading days of vendor closes (147,250 rows with the re-sent days), 43,289
  extract rows over 251 nights in two schemas, 35,017 blotter lines, 1,271 ledger lines, 255 run-log rows, 950 mapping
  rows; deciding which records answer for an exception is the work.

## Template check

Chain signature: assembly-reconciliation, investigation-loops, investigation-loops, decomposition-attribution,
  modeling, synthesis, forecasting, forecasting, synthesis
Question form: why (with how many)
Nearest build: task18 (root-cause, investigation, ranked causes): a grid frequency event's losses split by cause along
  a time axis on a physical model; this build's answer is a dated per-exception diagnosis of a quantile engine with a
  forward add-on path, a different decision form, answer shape (timeline), lessons and file roles. Abstraction
  sentence against it: none writable (one reconstructs an unmetered physical loss at a boundary; the other rebuilds
  the book a nightly forecast read and re-runs the forecast with each fault removed).

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | which exceptions are in the population | booked only; hypothetical only; either | either (19) | MRS-4 3.3 |
| SF2 | the hypothetical P&L | product control's figure; a revaluation of the extract the engine read | product control's (the close book revalued; `checks.py` C5) | MRS-4 3.2 |
| SF3 | the VaR reported for a date | the run of that evening; the run of the previous evening | the previous evening's completed run | MRS-4 3.4; the official file's VaR column |
| SF4 | the quantile convention | fifth-largest loss of 500; interpolated between the fifth and sixth | fifth-largest | the engine note, section 3 |
| SF5 | the scenario window | 500 days; 250 days | 500 business days to the run date | the engine note, section 3 |
| SF6 | the order of headings when two account for an exception | the standard's order; any | 4(a) to 4(e) in order | MRS-4 4 |
| SF7 | the volatility response's form | decay and level of scaling | any decay in 0.94 to 0.97, portfolio or series | band (same call) |
| SF8 | the corrected count | the union's exceptions still uncovered; the sound model over all 250 days | the sound model over the period | MRS-4 5 |
| SF9 | which exceptions count against the model | (c) to (e); (e) only | (c) to (e) (14) | MRS-4 4, last sentence |
| SF10 | the planned book | each segment scaled to its target from the 30 June run's positions; the total scaled | segments scaled, the hedge re-sized at 86 per cent | the plan's Basis sheet |
| SF11 | the window and betas for the planned add-on | 30 June 2025; rolled forward | the engine's 30 June run | the plan's Basis sheet |
| SF12 | the mapping in each month of the plan | as at 30 June; as the store rule stands for the run that sets the month's first VaR | the store rule at that run | MRS-4 3.4 and 6; the engine note, section 4 |
| SF13 | the store's count | returns from the day after the start date to the run date; closes | returns (500) | the engine note, section 4 (the run log's daily mapping replicates only on it) |
| SF14 | a negative add-on | reported; floored | floored at zero | MRS-4 6 |
| SF15 | the reused extract's counterfactual | that day's extract; the book held | the book held | MRS-4 4(b) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: MRS-4 3.3 (either P&L), the prompt's 250 trading days to 30 June 2025 |
| 2 | Unit of account: a business date's exception; the add-on in USD on the desk's book |
| 3 | Attribution window: MRS-4 3.4 ties each date to the previous evening's run |
| 4 | As-of dating: each extract's own cut time; the plan's basis on the engine's 30 June run |
| 5 | Version basis: product control's latest version; the blotter's latest version of each ticket, cancels removed; asserted neutral |
| 6 | Denominator: none (counts and USD) |
| 7 | Weighting: equal-weight scenarios (the engine note); the volatility response's weights banded |
| 8 | Window length: 500 days (the engine note) |
| 9 | Boundary inclusivity: a loss larger than the VaR (MRS-4 3.3); the nearest exception margin is USD 4,821 on booked P&L |
| 10 | Rounding path: none before the end; the answer blocks state each figure's precision |
| 11 | Tie-break: MRS-4 4's order |
| 12 | Maturity and censoring: the window is closed; the plan's months use the store rule |
| 13 | Order of operations: MRS-4 4(a) to (e) |
| 14 | Row order: none (the blotter is read by ticket and version) |
| 15 | Duplicate resolution: the cutover extract in both schemas carries the same holdings; repeated blotter and vendor lines are exact |
| 16 | Identity normalisation: the EQX crosswalk maps old to new instrument ids one to one; the vendor's id is stable through the ticker change |
| 17 | Netting against gross: the add-on is on the net book with its futures |
| 18 | Dimensional units: USD throughout; futures notional from contracts, multiplier and settlement |
| 19 | Code and status semantics: blotter status codes (NEW, AMEND, CANCEL) and run statuses from their own files |
| 20 | Integerisation: shares and futures contracts whole in the files and in the plan's book |
| 21 | Clause scope: MRS-4 applies to desk-level backtesting; the plan to the second half of 2025 |
| 22 | Forward window contents: the plan's segment targets and the store rule drive July to December |

## Literal reader

MRS-4 3.3 read literally gives the 19 dates of R1; 4(b) read literally (ERE on the positions the desk held at the
previous close) gives R3 once the positions held are taken from the record (each extract plus the bookings made after
its cut for that trade date or earlier); 4(c) to 4(e) give R4 to R6; 5 gives the sound count over the 250 days (2) and
the zone (green); 6 with the plan's basis and MRS-4 3.4 gives R7, and with the engine note's store rule and the
mapping's store start dates gives R8.

## Prompt contract

A voice rewrite may not drop the window (250 trading days to 30 June 2025), the question of how many exceptions the
model itself answers for, every exception dated under one heading of the standard with the headings adding back, what
went wrong with the engine's inputs, the count and zone a sound model shows, the add-on on the book the desk plans for
the second half month by month from July to December, or the two deliverables (a workbook and a one-page PDF note). It
must never add a method (hypothetical P&L, re-run, proxy, own history, cutoff, extract, allocation, volatility filter,
segment, store), a file name, a warning or who is asking.

## Tried and rejected

- A fully generated credit relative-value book (the concept note's Concept 1 as written): set aside at the draw because its volatility regime would be a generator setting (a 1.45 multiplier for 50 days), and the client's Quantitative Finance strategies ask for the market records to be real.
- A desk on real NASDAQ single-stock closes (the skfolio research dataset, 1,455 names, 2018 to May 2023): prototyped on 2026-11-11 (official counts 6 to 23 by book, a proxy class of 5 to 9, a volatility class of 0 to 5 that moved with the decay chosen); set aside because the dataset carries no licence (Yahoo-derived, marked not for commercial use), and its 2022 bear market sat inside a two-year window that already held 2020 to 2021, so the volatility class came out thin.
- A credit desk priced off FRED Treasury and Moody's yields: set aside because every counterfactual engine would need a bond pricing convention (spread duration, convexity, carry), each one a fork on every result.
- Filed first as task19 on 2026-11-11; another session filed task19 (Kilvarra) minutes earlier, so this draw moved to task20 with the skeleton and Frontier rules of the same day applied (forcing event redrawn to the supervisor's review, the prompt opening on why).
- 2026-11-11, prototype: closing blocks booked late on 22 random days caused no breach in four worlds (a block meets a large move too rarely); rebuilt as the middle office's daily allocation step, which swells after big moves, and the fees as a share of flow.
- 2026-11-11, prototype: the engine's hedge recomputed from the snapshot's cash book (inconsistent with futures booked before the run); the engine now reads the futures position its snapshot holds, and the world was re-searched (400 seeds, seed 970 the only one passing every band with margin on every volatility variant).
- 2026-11-11, the ten names to move first (ranked by the VaR each name's move adds to the desk's book): dropped; on the 30 June book 68 of 89 proxied names have negative single-name marginals, the marginal and greedy top tens share one name, and a fifth-largest-loss VaR's name-level marginals follow which scenario sits fifth, not the names.
- 2026-11-11, the engine's shortfall split into the book's move into proxied names and the names getting riskier: dropped; the two orders of the two-step decomposition give composition 97 and 29 per cent of the rise.
- 2026-11-11, the breaches a year the planned book would show on the engine as it stands: dropped; the planned book's 17.5 sits next to the year's own 16 by coincidence, so the history shortcut would land inside any honest band.
- 2026-11-11, the seed search on the exact-accounting world (1,200 seeds): 985 set aside for a hypothetical knife-edge on 1 November 2024, 30, 621 and 785 for a zone variant at or over the line, 262 and 1190 for a variant sound count of 5 to 6; 1114 kept.
- 2026-11-11, an end-of-day position file holding the book at the close: dropped at the pack design, because a literal 4(b) re-run of the engine on that file hands over the inputs heading with no investigation (R3, R4 and R6 earned by the careful pass).
- 2026-11-11, the engine's extracts as the only daily positions with the hypothetical P&L computed from them: dropped, because the missing allocations (a median USD 39 million gross a night) then scramble the hypothetical P&L itself and the cutoff decides most results (one thing); product control's hypothetical P&L ships instead, as MRS-4 3.2 says product control produces it.
- 2026-11-11, the plan's book scaled from the true 30 June close book: dropped, because the cutoff then decides the add-on path as well (0.34 in July, 0.42 in August and 0.14 in December against 0.32, 0.27 and nil); the plan's basis is the engine's 30 June run.
- 2026-11-11, FUTS snapshots carrying the CME trade date (a day ahead in the evening): dropped, because a run dating the futures by it moves seven headings, a mess item that would decide results; the snapshot carries its New York position date.
- 2026-11-11, a flat second-half target from July: replaced by the plan's own ramp, because with nothing in a flat plan changing month to month the store's graduations are the only story the month-by-month ask can find; the ramp is the story a hurried run stops at.
- 2026-11-11, allocation amendments that changed quantities after the extract: changed to moves between client accounts, because taking first versions then moved a heading (mess not neutral).
