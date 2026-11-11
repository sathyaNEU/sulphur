# task15: which Fjordkob store formats move their fresh ordering to Kornblomst's forecast for 2027, and why the pilot stores' fresh sales grew less and their fresh waste fell further than the other stores'

Architecture 2, drawn 2026-11-11. Architecture 1 (Banyena Grain Genetics' nominations to the High Rainfall Barley
Series) was READY and never run on the platform; the author re-rooted it for a much stronger stump with at least three
major analytical failure points in areas the earlier builds did not use, never task6's strategy (its line is under
`## Tried and rejected`). One architecture per world: this draw moves to another world (a Danish grocery chain),
another dataset (a simulated fresh-ordering field trial) and another shell. The careful but hurried column is
calibrated to the Sulfur run record: a run reads every file, reconciles every count, runs the field's textbook
method, models any pattern one plot shows and validates on held-out rows. So no result here is priced on a pattern
one table shows; each priced result is a correction the record in hand cannot flag on its own (what the sales record
does not contain, which form of an estimate survives a check where the answer is known, whether the stores tried are
the stores the answer is about), estimated from a second file or a second grain.

## Draw

Subdomain: General Statistics & Data Science (Machine Learning Research), task type benchmarking and ablations
Analysis type: Comparative Analysis & Explanation
Answer shape: ranked causes with their contributions (the pilot stores' fresh sales growth gap and fresh waste gap
  against the other stores, each split into its causes), with each store format's expected yearly saving per store,
  its 80 per cent range and the formats to switch on top
Weight: synthesis: the call rests on many separately estimated pieces pulled into one reconciled account (the units
  lost to empty shelves and the check that fixes their form, the discounter openings read off another record, the
  formats' own growth, what the forecast's saving depends on in a store, each format's saving and its range); the
  last two live builds lean on assembly (task16) and allocation (task9), and architecture 1 of this slot on
  attribution
Data-native sentence: a store's fresh sales are capped every day by the stock its own forecast ordered, so a forecast
  that orders leaner shows up in the record as less waste and a little less sold, never as the demand it turned away,
  while the stores a pilot runs in are picked by people for reasons that also decide how well a chain-wide forecast
  fits them.
People: Jakob Lauritsen (head of supply chain planning), Elna Johnsen (business intelligence analyst, the pilot
  dashboard), Dorthe Bruun (chief financial officer), Ludvig Bertelsen (Kornblomst Analytics' account manager)
  (`guard.py names --geo Denmark --seed 1502`). None appears in the prompt.

- **Card:** `.claude/skills/fingerprint/cards/task15.json`, architecture v2, registered 2026-11-11 with architecture 1
  in `lineage`. `guard.py check`: WARN only after two structural axes were redrawn on the draft. The first draft
  (gap population, decisive generator G6 composition shift, decision a designation set) BLOCKed `test.same_puzzle`
  against task7 v7 and `test.same_driver` against task3 v5, and a second (gap objective, G3, designation set) BLOCKed
  `test.same_puzzle` against task5 v2. The honest labels are the ones now filed: the decisive gap is objective (the
  dashboard's waste and at-close availability are correct and are not what the board's saving is scored on), with
  population second (the pilot's stores are not the stores the rollout reaches). After the rebase onto main the same
  day, task14's architecture 3 entered this card's window with decisive pattern G3 (`ban.pattern`), so the decisive
  generator moved to G6 composition shift, the honest first label for the call (the To Go format turns on the
  pilot's stores not being the format's stores), G3 second. WARNs answered: `overuse.forum` (board_of_directors): a
  licence of this size is the board's to sign under the chain's delegation, and no other forum holds it;
  `repeat.deliverables` (pptx+xlsx against task14 v3) and the prompt gate's shell quota (pptx+xlsx at 29 per cent of
  17 prompts): every two-file set with a workbook is over the cap in this corpus, a board decision's genre is a few
  slides beside the workbook behind them, and the deck's species (a dot-and-range chart against a licence tick, the
  splits and the routes as tables) is not task14's.
- **World:** Denmark, East Jutland. Fjordkob A/S, a regional grocery chain of 42 stores in three formats: 8 Super
  (large supermarkets), 18 Kvarter (neighbourhood stores, four of them by a station or in an office district) and 16
  To Go (small stores, twelve at railway stations, campuses, a hospital and office districts and four on pedestrian
  streets), supplied every night from one fresh warehouse in Aarhus. Kornblomst Analytics, a forecasting vendor.
  Every organisation, store and product is invented; the towns are real. The setting is September 2026: the pilot
  ran from Monday 2 March to Sunday 30 August 2026 (ISO weeks 10 to 35), the dashboard's last refresh is 7
  September, and the board meets on 6 October 2026 to sign or decline Kornblomst's 2027 licence, which the
  agreement needs by 1 November.
- **Forum, forcing event, organisation family:** board_of_directors, purchase_order_or_contract,
  retailer_or_ecommerce.
- **Deliverables:** a workbook and a few slides with a chart (two files: `fresh_forecast_rollout_2027.xlsx`,
  `fresh_forecast_board_2027.pptx`).

### The process behind the files

Written before any result was named (`stumping` 1.1). Fjordkob's fresh range is 32 items in five categories (bakery,
fruit and vegetables, dairy, meat, ready meals), two items to each subcategory; the To Go stores carry it without the
raw meat. Every evening each store's order for
the next morning is computed by the ERP's replenishment module, AutoOrdre: an order-up-to target of the next day's
forecast plus a safety stock (a service factor times the forecast's own recent misses against sales), less the stock
that will still be sellable, rounded up to the supplier's case pack (the warehouse breaks cases for To Go).
AutoOrdre's forecast smooths each store and item's own sales on that store's own weekday pattern, with the planners'
chain-wide promotion uplifts. Kornblomst's forecast, a chain-wide machine-learning model fed the weather, local events
and each format's promotion response, replaced AutoOrdre's forecast in 16 pilot stores for the 26 pilot weeks, with
Kornblomst's recommended service factor (0.75 against the ERP's 1.05). The regional managers chose the pilot stores:
their four biggest Super stores, nine busy Kvarter stores (three of them at a station or in an office district) and
their three busiest To Go stores, all three on pedestrian streets. Kornblomst also forecast every other store every
evening, and the ERP logged both forecasts. Customers arrive through each store's trading day and buy what is on the
shelf; when the shelf empties, the customers still to come leave without the item. The tills time-stamp every sale;
the daily store and item extract carries units sold, sales value excluding VAT, the time of the day's last sale, the
delivery, the units written off at close (some scanned the next morning and booked on the next day) and the closing
stock. Business intelligence keeps a weekly store and category history (with the ambient, non-fresh, trade beside
the fresh), the hourly sales profile by format, category and weekday it measured on days the shelf did not run empty
(it drives the store app's empty-shelf alert), and the pilot dashboard. Market intelligence logs competitor openings
near stores. What nobody at Fjordkob sees directly: the demand a shelf turned away after its last unit went, which
the record holds only as a last-sale time and a zero at close; that Kornblomst's chain-wide model learned the week of
the chain as a whole, which is the week of a big weekend-trading store, so in a store whose trade falls away at the
weekend it orders too much for Saturday and Sunday and too little for the working days; that two discounters opened
near pilot stores during the pilot; and that the To Go stores the managers picked are high-street stores that trade
like small supermarkets, unlike the station and office stores that make up most of the format.

## Deep reasoning

Task type: benchmarking and ablations (controlled evaluation, isolating component effects): a field trial of a new
  forecasting system against the incumbent in hand-picked stores, with the stores that kept the incumbent as the
  comparison, read for what each component of the gap is and what the system is worth where it would run
Domain test: every result is a statistician's object on a field trial with a capped outcome and a hand-picked sample:
  demand rebuilt from sales capped by stock through each stockout's last-sale time read as an order statistic
  against an in-stock intraday profile, the estimator's form validated where the answer is known, a concurrent
  shock separated with an outcome the trial cannot touch, a gap split into its parts against the formats' own
  trends, and a heterogeneous effect carried to the population it would be rolled out to through a moderator rebuilt
  from each store's own history, with a resampling range
Swap: put a hospital ward or a call centre in place of the store and there is no stock that caps the recorded
  outcome at a time of day, no in-stock day on which the estimator can be checked against a known count, no ambient
  trade the treatment cannot touch, and no weekly trading shape for a chain-wide model to misread; the call sentence
  stops making sense
Where the weight sits: the synthesis of R2, R4 and R7 into each format's saving (R8): the saving has a waste part
  and a margin part that ride on different scales, the margin part needs the turned-away units in their right form,
  each pilot store's expected level needs the openings taken out, and the whole has to be carried from sixteen
  hand-picked stores to forty-two by the property that governs it; each piece is long, none is clever
Layer 1: the daily extract changed layout at the ERP upgrade on 1 January 2026 (semicolons, decimal commas and
  Windows-1252 before, a dotted UTF-8 export after); the export job re-sent 840 store-item rows in 2025; two dairy
  items were renumbered when the supplier changed (the register carries the former numbers); some stores scan
  write-offs the next morning and book them on the next day; business intelligence renamed its category codes at the
  2026 range review; the last-sale time is blank on a day with no sale. Each is cleaned the same way by every careful
  run and moves no graded figure between careful runs (asserted)
Not one thing: the strongest single piece is the trading week (R7); a run that nails it still has to rebuild the
  turned-away units in a form that survives the in-stock check (R2, R3: the plain form puts Kvarter at 23,400,
  outside its band), read the openings off the ambient trade (R4), split both gaps (R5, R6) and range the savings
  (R9); a run that nails the estimator and reads by format switches all three formats
One-fact test: "the plain turned-away estimate overstates small counts, as the days the shelf did not run out show"
  rescues R2 and R3, 2 of 10; "the new forecast reads every store's week like a big weekend store's" rescues R7 and
  R10 and half of R9, 2.5 of 10 (R8 still misses Kvarter's band with every sale counted, 23,400 against 24,300 and
  up); the openings sentence rescues nothing the careful pass has not already earned
Not semantics: every field, unit and clause read correctly still leaves the turned-away units counted with every sale
  (125,000), each format read off its own pilot stores (To Go 23,800 a store) and the range resampled by format; no
  reading of the agreement, the dashboard or a column moves any of them
Not rule application: no filed procedure estimates demand past an empty shelf, separates an opening from the
  forecast, decides what a store's saving follows or carries it to stores the pilot did not run in; the agreement
  files what the saving is (4.2), what a year is and over which stores the average runs (4.3), and the rule on the
  average (4.1), and every one of those leaves the estimation open
Estimand: the prompt fixes the two gaps (the pilot stores' fresh sales in kroner and fresh waste at cost, over the
  pilot against the same weeks of 2025, against the other stores) and asks for each split in percentage points;
  the agreement fixes the saving (4.2: waste at cost avoided plus the margin on units gained less the margin on units
  no longer sold, against the same store on AutoOrdre), the year (4.3: twice the 26 weeks), the population (4.3:
  every store of the format in the register, pilot or not), the rule (4.1: switch when greater than the licence) and
  the licence (Annex 2); the 80 per cent range is the prompt's own
No decoy: nothing is written to carry a wrong answer: the dashboard answers its own question (waste and availability
  at close, pilot against the rest) correctly, the agreement states the decision's terms, and no memo, draft or
  stakeholder figure ranks the formats
No replay: no result re-derives a published figure; the dashboard's two headline changes are R1's inputs, not its
  graded content, and every graded figure is estimated
Pinned: R2's two forms (clipped at zero or not) and the simulation's truth inside its bands, the plain form outside;
  R4 under ramps of 2 to 6 weeks and both comparison sets; R5's residual reading (-1.0) and the truth (-0.85) inside;
  R7 under ratio and mean weighting; R8 under fourteen rivals (estimator form, grouping by trading week or by format
  within it, the margin part on sales, units or the 2025 turned-away margin, ratio or mean weights, a line in the
  weekend share, the recorded-margin route, the openings left in), all on the golden call, and the whole saving
  carried on fresh sales or on waste ruled out by the pilot's own record; R9 under three resampling variants;
  asserted in `checks.py` (115 assertions)
Run forecast: R2 (method shortcut: every sale counted, or no turned-away units at all), R3 (self-confirming check: the
  estimate never read back on in-stock days), R7 (narrow look: each format read off its own pilot stores), R8
  (method shortcut and narrow look together), R9 (unfinished chain: resampled by format, To Go's range above its
  licence) and R10 (unfinished chain: Super and To Go switched); R1, R4, R5 and R6 are earned by a careful run
Strategy label: WORKS IN FORM (heterogeneity that pooling hides, carried to the population the decision serves through
  a property rebuilt from each unit's own history; a capped outcome rebuilt from when each capped record stopped,
  its form checked where the answer is known; separating two explanations for one gap with a record the treatment
  cannot touch); the client's strategy 4 for this group (ranking fairly) is direction only
Depth level: 5: four independent judgments each needing estimation (the turned-away units' form, its check on
  in-stock days, the openings off the ambient trade, the trading-week transport with the saving's two parts on
  their own scales), two splits that need them, and eight shortcuts landing on three different wrong calls (Super and
  To Go; all three; Super alone)
Lesson: a pilot's measured effect is a property of the units it ran in: when the outcome is capped by the treatment's
  own choices, rebuild what the cap hid in a form you have checked where the answer is known, and carry the effect to
  the units the decision is about by what governs it in each unit, not by the label the decision is taken on; no
  build on file carries a capped outcome or a moderator rebuilt from each unit's history

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the pilot stores' two gaps: fresh sales -2.0 points (3.9 against 5.9 per cent), fresh waste at cost -17.5 points (-9.6 against +7.9) | assembly and reconciliation | the prompt (kroner, at cost, the same weeks of 2025); the dashboard ties to the deduplicated record to the cent | -2.1 to -1.9; -17.7 to -17.3 | method shortcut: counting the re-sent rows or leaving the renumbered items unjoined moves a gap by under 0.1, so every pass earns it | - | Ask 1 |
| R2 | units the pilot stores' empty shelves turned away: 94,100 in the pilot weeks, 81,300 in the same weeks of 2025 | missingness and measurement (censoring) | each sold-out day's last-sale time against the hourly profile, one sale fewer than made; within 1.2 per cent of the simulation's truth | 90,300 to 104,700; 78,000 to 91,100 (the estimate clipped at zero or not) | method shortcut: counts every sale (sales so far over the share of the day gone), 125,000 and 109,200 | independent: the daily record and the hourly profile | Component 1 |
| R3 | the estimate checked where demand is known: counting every sale overstates an in-stock day's sales by 9.7 per cent (40.9 on six sales or fewer); one sale fewer by 0.2 | self-verification | the 449,049 in-stock store-item days with two or more sales | 8.0 to 14.0 (days with one or more, two or more, three or more sales) | self-confirming check: the plain estimate is never read back on days whose demand is known | independent: the in-stock days | Component 2 |
| R4 | each discounter opening's effect on its store's trade: 2131 -7.0, 3031 -4.7, 3012 -1.6, 3114 -6.6, 4224 -4.3, 2146 -0.5 per cent | causal reasoning | the ambient weekly sales, 2026 against the same week of 2025 against the format's stores with no opening, the step across the opening date; each within 1.4 of the simulation's depth | each plus or minus 2.0 (ramps of 2 to 6 weeks; both comparison sets) | first story: the fresh record, where the forecast and the opening move together, read as the forecast's (the careful pass is graded Right here) | independent: the ambient weekly history | Component 4 |
| R5 | the sales gap split: forecast at its recommended setting -0.7, format mix -0.6, openings -0.4, not explained -0.3 | decomposition and attribution | the formats' own growth from their clean AutoOrdre stores; the turned-away sales against each pilot store's expected level; R4's shares; the residual reading (-1.0) and the simulation's -0.85 inside | forecast -1.05 to -0.55; mix -0.8 to -0.4; openings -0.6 to -0.2 | stopped at the first story: the whole gap is the forecast (-2.0) | R1, R4 | Ask 1 |
| R6 | the waste gap split: forecast at its recommended setting -15.7, format mix -1.2, openings -0.3, not explained -0.3 | decomposition and attribution | the formats' own waste change from their clean AutoOrdre stores; R4's shares on each store's waste; the residual reading (-16.0) inside | forecast -16.5 to -14.9; mix -1.6 to -0.8; openings -0.5 to -0.1 | stopped at the first story: the dashboard's whole gap is the forecast's saving (-17.5) | R1, R4 | Ask 2 |
| R7 | what the saving depends on: the trading week; weekend-trading pilot stores avoided 19.7 per cent of their 2025 waste, commuter-week pilot stores -1.3; the shadow forecasts' weekend ratio 2.42 against 0.91 | investigation | each store's 2025 weekend share of fresh units (no store between 0.205 and 0.253); the pilot stores' own savings; the shadow forecasts; the pilot stores' true rates (23.6 and -2.1) inside | 16.0 to 24.0; -4.5 to 2.0 | narrow look: each format's saving read off its own pilot stores (To Go 32.3 per cent of waste), never asking why the stores differ | independent: the stores' own weeks and the shadow forecasts | Component 3 |
| R8 | each format's expected saving per store and year: Super 40,200, Kvarter 28,000, To Go 2,400 DKK | modeling | agreement 4.2 and 4.3; the waste part on each store's 2025 waste and the margin part on its 2025 fresh sales at its trading week's rates; fourteen rivals inside every band; the whole saving on sales or on waste ruled out by the pilot's record | Super 28,300 to 47,000; Kvarter 24,300 to 31,900; To Go -6,300 to 6,400 | method shortcut and narrow look: by format with every sale counted, 33,100, 16,800 and 23,800 | R2, R4, R7 | Ask 3 |
| R9 | the 80 per cent range: Super 22,200 to 55,800; Kvarter 17,800 to 37,700; To Go -4,000 to 8,300 | uncertainty | 400 resamples of the stores (pilot stores within trading week, the others within format), every step redone; three variants inside | Super 17,200 to 27,500 and 50,100 to 60,800; Kvarter 12,800 to 22,800 and 32,700 to 42,700; To Go -9,000 to 1,000 and 3,300 to 13,300 | unfinished chain: resampled by format, To Go's range (19,700 to 27,700) sits wholly above its licence | R8 | Ask 3 |
| R10 | switch Super and Kvarter, keep To Go on AutoOrdre | synthesis | agreement 4.1 on R8; every rival on the golden's side of each licence by 3,500 or more | exact | unfinished chain: switches Super and To Go | R8 | Recommendation |

Carry-forward: R2, R3, R4 and R7 each read an input of their own (the daily record with the hourly profile, the
in-stock days, the ambient history, the stores' own weeks with the shadow forecasts), so a run that slips on one
still earns the others. R5 and R6 need R4's shares for their openings parts and nothing else upstream (the
forecast's band holds every form of the turned-away estimate). R8 needs R2 for its margin part, R4 for each pilot
store's expected level and R7 for the transport; R9 and R10 fall with R8. No analytical result carries more than
three of the other nine.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Demand turned away once a shelf empties (sales capped by stock) | constructed by the simulated trade, at every store, item and day the stock runs out | no: 22 to 30 per cent of store-item days in every format, group and year; it decides Kvarter's figure and moves every other | modelling: the last-sale time against the hourly profile, the estimator's form checked on in-stock days | modelling: an order-statistic estimate of each sold-out day's demand, validated | keep |
| The chain-wide model's weekly pattern (commuter-week stores over-ordered at the weekend) | constructed by the simulated forecast, in every store whose trade falls away at the weekend (16 stores in two formats, 3 in the pilot) | no: four Kvarter stores where it decides nothing (they lose money and Kvarter still switches) and twelve To Go stores where it decides | modelling: each pilot store's saving against its own weekend share, and the shadow forecasts' weekend ratio | modelling: the effect carried to every store by its own trading week, with the saving's two parts on their own scales | keep |
| Discounter openings near stores | constructed by the simulated market: six openings in the record, two in 2025 near other stores and four in 2026 (three pilot stores, one other) | no: three of the six are outside the pilot, and the call holds with every opening left in | modelling: a step in the ambient year-on-year series against same-format stores | modelling: each store's expected level carried by the share of trade its opening took | keep |

No factor sits only in the units it decides; each shows across the data the way its process puts it there, and for
each the fix is an estimate with a tempting shortcut, not a filter. `checks.py` asserts each footprint, a misreading
where it decides nothing (Kvarter's commuter stores) and the call with the openings left in.

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the pilot stores' two headline gaps against the other stores | Right | Right | Right |
| R2 the units the pilot stores' empty shelves turned away, pilot weeks and the same weeks of 2025 | Missed | Missed | Right |
| R3 the turned-away estimate checked on the days the shelf did not run out | Missed | Missed | Right |
| R4 each competitor opening's effect on its store's trade | Missed | Right | Right |
| R5 the sales growth gap split into its causes | Missed | Right | Right |
| R6 the waste gap split into its causes | Missed | Right | Right |
| R7 what the forecast's saving depends on in a store: its trading week | Missed | Missed | Right |
| R8 each format's expected yearly saving per store | Missed | Missed | Right |
| R9 the 80 per cent range on each format's saving | Missed | Missed | Right |
| R10 the formats to switch for 2027 | Missed | Missed | Right |
| Roughly | 1 of 10 | 4 of 10 | 10 of 10 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "the plain turned-away estimate overstates small counts, as the days the shelf did not run out show"; rescues 2 of 10 results (the trading-week sentence rescues 2 and half of R9)
Pair estimate: 46.0

The careful pass is graded up on purpose: it conforms both extracts, reads the openings off the ambient trade, splits
both gaps against the formats' own growth and puts a range on its savings, because the Sulfur run record has runs
doing each of those unprompted. It then counts every sale before the last-sale time, never checks that form on
in-stock days, and reads each format's saving off that format's own pilot stores. Were it also to find the trading
week (the second hint), it would earn R7 and the call, half of R9, and still miss R2, R3 and R8's Kvarter cell.

## Data provenance

Source: generated by `task15/generator` from a simulated process; nothing in the pack was downloaded
Behaves like the real thing: the generator simulates customers arriving through each store's trading day (an
  intraday shape mixing a weekend-trading store's and a commuter store's by the store's own commuter share) and
  buying what is on the shelf, overdispersed daily demand by store and item, the ERP's order-up-to rule with a
  safety stock from the forecast's own misses and case packs, first-in-first-out depletion and write-off at the end
  of shelf life, AutoOrdre's exponential smoothing on each store's weekday pattern and Kornblomst's chain-wide model
  with weather and promotion inputs, each store's last sale timed as the exact order statistic of the day's arrivals,
  the systems' exports with their recording conventions, and discounter openings that ramp in over weeks
Genuine patterns: (1) weekly shapes that differ by trading type and category, with stations and offices quiet at
  the weekend (2) seasons by category, an industrial-holiday dip in July in commuter stores and holiday peaks
  (3) format trends, To Go growing about 7 per cent a year and Super flat (4) promotion weeks with uplifts that
  differ by format (5) regional weather and event shocks with day-to-day persistence (6) overdispersed daily demand
  and store-level noise in waste of 5 per cent a year
Problems by process: the ERP's export layout change on 1 January 2026; store-days the export job re-sent in 2025; the
  next-morning write-off scans booked a day late (store practice); two items renumbered at a supplier change; the
  BI cube's category codes renamed at the range review; last-sale times blank on days with no sale
Breadth: 13 files; 389,960 and 309,760 daily store, item and day rows, 309,760 order proposals with both forecasts,
  19,656 weekly history rows; 42 stores in three formats, 32 items (28 in To Go); which stores, which record and which
  comparison carry the saving has to be worked out, and nothing in the pack says which

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, self-verification, causal-reasoning,
  decomposition-attribution, decomposition-attribution, investigation-loops, modeling, uncertainty, synthesis
Question form: why (a comparative explanation), then whether and which (the formats to switch)
Nearest build: task12 (heterogeneity that pooling hides, carried to a buyer base): there a price response by wave
  carried to a cohort mix; here a capped outcome is rebuilt first, a concurrent shock is separated with an untouched
  record, and the effect is carried by a property rebuilt from each unit's own week; the answer shape (ranked causes
  under a call), the weight (synthesis) and the shell differ, and nothing here is a cohort or a price

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "the same weeks of 2025" | ISO weeks 10 to 35 of 2025; the calendar dates 2 March to 30 August 2025 | ISO weeks (the dashboard's comparison) | same call: the calendar reading moves neither gap by 0.15 (asserted) |
| SF2 | "fresh sales in kroner" | sales value excluding VAT; units | value | the prompt (kroner); units give -2.02, inside the band (asserted), same call |
| SF3 | "fresh waste at cost" | units written off at that year's cost price, as booked; units; at sales price | at cost as booked | the prompt (at cost); BI and the dashboard book it so |
| SF4 | "the other stores" | every store not in the pilot; the same format's stores | every other store | the prompt; the dashboard's two groups |
| SF5 | "expected saving per store and year" | 4.2's change in fresh result (waste at cost avoided plus margin on units gained less margin on units lost, against the same store on AutoOrdre); waste alone; sales | 4.2 | agreement 4.2 |
| SF6 | gross margin | sales excluding VAT less the cost of the units; with VAT | excluding VAT | agreement 4.2; every price and sales column is labelled excluding VAT |
| SF7 | "the average over every store of that format" | all the register's stores of the format (8, 18, 16); the pilot stores only | all of them | agreement 4.3 (pilot stores and other stores alike); the pilot stores' own average puts To Go at 21,500 (asserted) |
| SF8 | a year | twice the 26 pilot weeks; a seasonal extrapolation | twice the 26 weeks | agreement 4.3 |
| SF9 | "greater than the format's licence price" | the expected saving against Annex 2's price per store and year | as written | agreement 4.1 and Annex 2; every rival 3,500 or more from a licence |
| SF10 | write-offs scanned the next morning | as booked; moved back a day | as booked | same call: they move the window totals by under 1 per cent at the edges (asserted) |
| SF11 | comparison stores for the savings | stores with an opening in the record left out; every store on the openings log left out | the former | same call: the latter stays inside every band (asserted) |
| SF12 | the trading-week cut | anywhere between the two groups' weekend shares | the widest gap (0.23) | same call: no store has a weekend share between 0.205 and 0.253 (asserted) |
| SF13 | "an 80% range" | the 10th and 90th percentiles of a resampling of the stores with every step redone | as stated | the prompt; three resampling variants inside every end's band (asserted) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the gaps run over the pilot stores and the other stores (the prompt); the saving's average over every store of the format in the register (4.3) |
| 2 | Unit of account: the store, item and day in the record; the store for the saving (4.2) |
| 3 | Attribution window: the pilot weeks, ISO 10 to 35 of 2026, against ISO 10 to 35 of 2025 (the prompt, the agreement's dates, the dashboard) |
| 4 | As-of dating: every export cut by 7 September 2026; the 2027 licence on Annex 2 as replaced on 1 September |
| 5 | Version basis: one ERP export per year (the layout changed with the year); one licence price list |
| 6 | Denominator: the pilot stores' own 2025 sales and waste for the splits; each store's 2025 waste and sales for its saving's parts |
| 7 | Weighting: the format's average over its stores, unweighted (4.3); the pilot rates as totals over totals, the mean of store rates inside every band (asserted) |
| 8 | Window length: 26 weeks, a year twice that (4.3) |
| 9 | Boundary inclusivity: whole ISO weeks; the late-booked write-offs at the edges move under 1 per cent (asserted) |
| 10 | Rounding path: savings stated to the nearest 100 DKK from unrounded values; every saving 3,500 or more from its licence under every rival |
| 11 | Tie-break: none needed; no format sits near its licence |
| 12 | Maturity and censoring: sales are capped by stock; the turned-away units are estimated (R2), their form checked (R3) |
| 13 | Order of operations: dedup and conform, then the units turned away, then each pilot store's saving, then the transport; the margin part read before or after the transport gives the same figure (linear) |
| 14 | Row order: no step depends on file order; the re-sent rows are exact copies |
| 15 | Duplicate resolution: exact duplicate store, item and day rows in the 2025 file counted once (840) |
| 16 | Identity normalisation: the two renumbered items joined by the register's former number; store numbers one form in every file |
| 17 | Netting against gross: the saving nets the margin given up against the waste avoided (4.2) |
| 18 | Dimensional units: DKK excluding VAT throughout; gaps in percentage points of the pilot stores' 2025 figure; units for the turned-away counts |
| 19 | Code and status semantics: the BI cube's old and new category codes map one to one; the order basis column names the forecast each store ordered on |
| 20 | Integerisation: none graded; unit counts are stated to the nearest 100 |
| 21 | Clause scope: 4.1 applies format by format and a format is taken whole; the per-store savings are workings, not decisions |
| 22 | Forward window contents: 2027 is twice the pilot's 26 weeks by 4.3; the Netto opening planned near store 3136 for November 2026 is on the log, and taking its likely share of that store's trade off would move Kvarter's average by under 300 DKK against an 8,000 margin (asserted) |

## Literal reader

The prompt executed word for word on the conformed record gives R1's two gaps. Agreement 4.2 executed word for word
asks for each store's change in fresh result against itself on AutoOrdre: the waste part is a comparison the record
supports (2025 against 2026, against the stores that kept AutoOrdre), and the margin part needs the units the store
sold in addition or no longer sold, which the sales record caps at the stock, so a literal reader must estimate the
units the empty shelves turned away; the in-stock days show which form of that estimate holds. 4.3 executed word for
word averages over every store of the format, so the pilot stores' own figures cannot stand for the format, and the
reader has to carry the pilot's saving to stores it did not run in by whatever governs it there. 4.1 then reads each
format's average against Annex 2. Every literal reading gives the golden's quantities; the hurried figures come from
easier methods on the same estimands (every sale counted, each format read off its own pilot stores, the range
resampled by format), never from another reading. No shipped sentence names a method, a comparison or a grouping.

## Prompt contract

A voice rewrite may not drop or change: the why question (the pilot stores' fresh sales in kroner grew less and their
fresh waste at cost fell further than the other stores', over the pilot against the same weeks of 2025); the
whether-and-which question (moving any store format's fresh ordering to Kornblomst's forecast for 2027, with none a
grammatical answer); each gap split into its causes in percentage points; each format's expected saving per store and
year from switching, in DKK, with an 80% range; the formats to switch; a spreadsheet and a few slides with a chart.
It must never add: a rounding instruction, a method or comparison (empty shelves, lost sales, demand, the trading
week, weekdays, competitors, store mix, resampling), a warning, an attached file's name, a role or reader, a count the
data hold (stores, formats, items, weeks), the licence prices or any other fact the files carry.

## Pre-ship check

Ruled in the main thread on `leak.py`'s REVIEW lines (2026-11-11, the stage 4 cut):
- The licence prices in the agreement's Annex 2 are stated inputs (`metadata.json` `stated_inputs`), the line the
  call is read against, not an answer.
- Clause numbers 4.2 and 4.3 and the agreement number FK-2026-014 are the governing document's own references.
- Two 2026 daily rows match range figures across a last-sale time and the next column (a time ending :33 or :50
  followed by 100 units received): artefacts of the comma-separated layout, not figures.
- The agreement carries the formats' and systems' names and the stump paragraph's ordinary words (result, margin,
  decision, licence, Kvarter, agreement) because it is the contract the decision is taken under; it names no method,
  grouping or comparison, and the reader's question 1 asks the same thing cold.
- The prompt gate's shell quota (pptx+xlsx at 29 per cent): answered under `## Draw`.

## Tried and rejected

- A population count from several overlapping lists with no common key (record linkage, then capture and recapture),
  screened at intake for the ETL cell: mark196's driver already recovers a count from the overlap of two capture
  channels with the second dependent on the first, and Mark's record has identity resolution holding nothing as a
  result's only difficulty.
- A labelling-operations bridge from gold-seeded accuracy to audited accuracy (targeted audits, imperfect reviewers,
  memorised gold items): it walks the client's own strategy 5 for this domain group (label errors in the yardstick,
  a biased screen combined with a random relabel) in its order with its deliverable.
- A training-sweep, eval-regression, run-forecast or checkpoint-ranking world: the client's worked illustration and
  its strategies 1 to 4 for this group; any chain there reads as a reskin of a page on the reviewers' desks.
- An optimiser benchmark from real runs (evaluations to target censored at budget, restarts, scaling with dimension,
  a customer workload mix): real algorithm behaviour cannot be set so that four independent judgments each move the
  pick by a clear margin, and its extrapolation step is the client's strategy 3.
- A comparison of two vintages under maturity (warranty claims with reporting delay, or loans): the client's own
  good example in the deep-reasoning page (the auto lender) and its level 5 general statistics example (SBA).
- A certified rate against a threshold from a targeted inspection sample with uncovered strata (fare evasion): the
  reweighting and the coverage imputation are the level 5 job-openings example's skeleton, trap for trap.
- Abandoned plots as a priced result of their own: on the prototype dropping them moved a nominee's index by under
  one point, because abandonment follows the lodging score and the loss is roughly linear in it; kept inside R4.
- A two-part bridge (own trials, series trials) with the remainder graded as its own result: the quick pass earned
  the remainder by calling the whole gap luck (nothing left), and the second part could be had by subtraction or by
  two wrongs cancelling (6.2 plus 4.9 against 10.7), so the series part is split and graded as two components.
- The three causes of the gap named in the prompt (the benchmark's gain, lodging): it names the factors a run has to
  find; the prompt splits the gap by where it arose and the split by cause sits in the critical components.
- A recalibration regression of returned on forecast and lodging as the careful pass's last step: on 24 nominations it
  took a negative slope on its own forecast and the wrong sign on lodging in this world, which no careful analyst
  would file; replaced by the mean miss and its lodging share, a wrong-signed share left out.
- The response to the trial's yield level kept as a rival inside the bands: it moves the benchmark's gain to 5.7 and
  lines by up to 6.6 points, so the bands would have held the careful pass; the data rule it out instead (season
  water t 4.4, yield level t -1.1 entered together) and `checks.py` asserts that.
- Lines modelled as unrelated to their sisters as the golden: the record shows about half the spread of level and
  response lying between crosses, so the cross level went into the golden and the simpler model stays as a rival.
- Seeds with a thin cut between the third and fourth line (220 at 0.95 points, most of 800 scanned under 1.0): two
  defensible fits named different thirds; world 730 was taken for a cut of 2.2 that every rival keeps.
- The gap split "by where it arose" (at our own trials, between our trials and the series' trials, what is left),
  the first cut's ask: the determinism judge's first pass returned it NOT_DETERMINISTIC (Gates G and H passed)
  because no document said what "arose at our own trials" is, and a literal reading (recording conventions, chiefly
  abandoned plots) gave 0.6 to 3.1 against 5.6. The option deed now files four heads for a review (schedule 2,
  clause 4.2), each an estimand in the deed's own words with no method, and the prompt points to them.
- The root mean square error of the solver's own figures on the past nominations "as each line was nominated", as a
  graded result (the first cut's R6): an own-method statistic no sound rival of the judge's reproduced (7.7 to 10.4
  against a band of 5.4 to 6.3), with an open training rule for the first sowing years. Dropped as an ask; the
  routes sheet of the workbook still shows each route's error.
- The three highest lines as the decision, on any world: across more than 1,000 worlds scanned the median cut between the third
  and fourth line was 0.8 points against a forecast spread near 5, and the judge's own unshrunk fit named a different
  three in world 730. The decision is now the lines to be expected at the deed's standard, at most three, on a world
  (3153) where two lines stand 2.5 or more above 107.0 and the next 3.6 below under every rival; the standard was set
  at a whole number inside that gap (106.5 centred it; 107.0 leaves the thinner side at 2.0 across rivals).
- The gap printed as the difference of the rounded means (15.1 where the unrounded means gave 15.2): the judge's
  SOLUTION_WRONG line; every figure now comes from unrounded values and each head is rounded on its own (SF14).
- The first leak reader's realism tells (the same number of lines entering and leaving every season, a series entry
  list of one size, no trial lost and no comment in twelve seasons, a handbook sentence requiring 12 kg of clean seed
  that read as an eligibility test against the seed store): the world now draws each year's sizes, the series loses a
  trial now and then and its coordinator comments on site seasons, and the seed sentence went; the seed store stays
  as an unused file.
- Each line fitted on its own trials alone, with no pooling, ruled out by its own remainder (2.4 points of the gap
  left on the 24 nominations, t 3.5): kept inside every band instead, because the first judge ran an unshrunk fit as
  a sound rival and it names the same two lines; the index head's band (1.4 to 4.3) and nine lines' tolerances are
  wider for it.
- The joint regression across Banyena's own trials (season water t 6.1, yield level t -2.1) as the fact that rules
  out a response to yield level: it rested on a yield level that held the lines' own yields, and with the other check
  varieties' mean as the level the two cannot be told apart there (r 0.92; t 2.5 and 1.5). The series' own trials
  (t 6.4 against -1.9 for Banyena's lines, 5.0 against -1.3 among the standards) and the remainder on the 24
  nominations (3.4, t 4.4) rule the route out instead, and the answer blocks say so.
- The chances taken as independent, or drawn from the spread of the estimates alone, as R7's own hurried failure: in
  this world the two nominees' chances multiply to 73% against 75% drawn together, and the estimates alone give 83%,
  inside the band of 64 to 85. R7 stands as a result that falls with R6 and R8 (the careful pass has no line to give
  a chance for), and the blocks reject neither figure.
- The lines to be expected at the deed's standard as the decision (107.0, with two lines 2.5 or more above it and
  the next 3.6 below under every rival run here): the second judge pass, deriving its own answer before it saw the
  blocks, put WI3559 at 106.2 (its level pulled toward the Stage 3 lines' own spread) and 107.7 (not pulled at all)
  against 109.5, so the second nomination turned on a pooling choice no file pins. NOT_DETERMINISTIC, Gates G and H
  passed (`determinism_check_report_pass2.md`). A line's expected yield is known to about 2.6 points, so no bar
  inside 5 points of a line can decide it. The decision is now the two lines to expect most from, which every fit
  of the judge's and every rival here names, the second never less than 5.2 clear of the next.
- The chances that the nominated lines meet the standard, as a graded result: the judge's rivals gave 39% and 53%
  for both against a band of 64 to 85. A chance near a bar moves with any pooling choice. Dropped from the asks; the
  80% range stays as a result of its own with room for the ways a season draw is modelled.
- A tolerance of 2.5 points on a line's expected relative yield: the judge's rivals fell outside it on 14 to 17 of
  the 28 rows, by up to 8 on the heaviest lodgers. The tolerance is now 5 (9 for the lines expected to lodge 45% or
  more, where the size of the lodging loss is read differently between sound fits) and a range end 3 more; the cost
  is that the careful pass keeps 11 of 28 expected yields and 37 of 56 range ends.
- The lodging head priced only as tonnes a hectare: the judge's reading of the loss as a share of yield gave 3.1 to
  3.3 against a band ending at 3.0. The generator now runs that reading (3.5% a tenth; a lodging head of 3.3 and a
  move of 4.4) and the bands of heads (b) and (c) hold it; lodging set against Byaduk's alone joined the rivals too.
- Three places, or any bar, as the decision on this world: the third and fourth lines stand 0.4 apart, and no bar
  sits 5 points clear of both a line above it and a line below it.
- The split of the heads by sowing year as a further ask (the 2017 nominations lost 11.9 points in the move, the
  2023 ones 0.9): its cells would turn on the form of the response where the judge's own forms agree only on the
  overall figure, and the careful pass would earn the lodging cells. Left in the workbook, not graded.
- A judge thread briefed with the graded blocks in its prompt, started before main's rule that the thread derives
  first and opens the blocks afterwards: stopped before it filed anything, and not a pass.
- The third judge pass (the thread again deriving first): DETERMINISTIC, FIX_NOW on the blocks alone, Gates G and H
  passed; every figure reproduced, the two lines held first and second under every sound variant it ran, and its own
  fits landed inside all four heads' bands. Its four repairs are in: "yield level" is now said to be the mean yield
  of the trial's entries on neither side of the comparison (with Byaduk's own yield as the level the comparison
  regresses a difference on one of its own terms), and the three comparisons use that one definition (t 6.3 and
  -2.7 for Banyena's lines in the series); the returned figure is said to be the series' ratio of means, with the
  mean of trial percentages (102.1, a gap of 10.9) named as not accepted; a line expected to lodge 65% or more has
  13 points of room (the judge's unshrunk fit put WI3585 12.4 from the golden); and a two-season line's index is said
  to run over all its Stage 3 trials at the three sites. The response is also said to be fitted on Banyena's record
  alone, and the spread of the lines' responses is given as a variance ratio against their standard errors (the
  judge's own count was 2.1 times, on another footing, against 5.5 here).
- The re-judge approved the final cut and offered one optional change: stop the handbook, the season review and the
  site list from saying that Kerang is watered, so that counting the waterings as season water is not handed over.
  Not taken: the irrigation log ships as a file whatever the documents say, a real handbook and site list would say
  it, and a change to a pack document after the approved cut would need the leak read and the judge again. The cost
  is that a careful run adds the waterings without having to think of it, which is why Kerang's waterings are a
  ruled-out route here and not a result.
- Architecture 1 itself (Banyena Grain Genetics, the High Rainfall Barley Series; READY 2026-11-10, never run): spent
  on 2026-11-11 at the author's word. The judge's Gate H read its stump power as moderate: a run that gives every line
  its own response to season water earns the nominations, which the note's own sensitivity put at 59.0 to 70.0 on the
  paper scale, so the call leaned on one modelling move. Re-rooted to another world, dataset and shell.
- A human-evaluation campaign world (an assistant's quality fell between two rating campaigns: rater severity linked
  through anchor items, refusals excluded by a rubric change, the prompt mix against production traffic), screened
  at this draw: all three priced corrections are measurement artifacts of the ratings, one area under three names,
  and the anchors announce the linking a run then performs.
- A ticket-routing model's accuracy across two halves (a bot that removes confident tickets before routing, final
  labels anchored on the model's own route, a new product's tickets): every priced piece is missingness and
  measurement, task6's area, and the audit sample a run would use reads as a two-phase design, task6's family.
- A retrieval test collection with judgments pooled from the incumbent (unjudged documents counted as irrelevant,
  two assessor pools, the query mix against the log): the pooling correction is a random-sample estimate of the
  relevance rate beyond the pool, design-based estimation in task6's family, and the pooling bias is known to runs.
- A robot grasping benchmark (operator scoring, faulted trials excluded, object wear, the sites' item mix): each
  correction is noticed and then fixed by one routine step (a re-scored subset, a fault count, a reweight), so each
  read as a one-fact stump.
- Interference through the central warehouse in this world (pilot stores ordering less freed rationed stock for the
  other stores): on the prototype it binds on few days, and in a full rollout every store gets the relief, so the
  rollout effect needs an allocation simulation no file pins; dropped from the chain.
- A slow-mover bias in the new forecast as the source of format differences: on the prototype cutting slow movers'
  orders saved more waste at cost than it lost in margin in every format, so it could not make a format lose; the
  format difference now comes from the weekly pattern the chain-wide model learned, which the record shows only
  through each store's own week.
- The paired item's recapture as a priced result (part of a turned-away sale bought as the other item of the pair,
  by format): on the prototype the estimator (the partner's sales above its like days on days the other ran out)
  ranged 0.18 to 0.81 against a true 0.31 with the day's own shocks in it, and no record in the pack separates
  substitution from a busy day; substitution was taken out of the world and the result out of the chain.
- The plain turned-away estimate (sales so far over the share of the day gone) as the golden: on the days the shelf
  did not run out it overstates the day's sales by 9.8 per cent, 41.4 on six sales or fewer, because the last sale
  closes the count; it became the careful but hurried reading and the in-stock check became a result (R3).
- Stockout times drawn from a normal approximation to the order statistic in the generator: it put too many last
  sales early in the day on small counts, so every estimator was biased against the simulation's own truth; the
  generator draws the exact beta quantile now, which moves only the recorded last-sale times.
- One saving rate per store as a share of its 2025 waste, by trading week, as the transport: carrying the margin
  part on waste put Super at 47,500 against a true 42,900, and carrying the whole saving on sales put Kvarter under
  its licence (16,600); the waste part now rides on each store's waste and the margin part on its sales, which lands
  within 3,200 of the truth in every format, and the single-scale routes are on the Routes sheet.
- A line in the weekend share as the golden transport: the pilot has only three commuter-week stores, and the line
  extrapolates to the To Go stations (weekend share 0.12 to 0.17) below anything the pilot measured (To Go -5,600);
  kept as a rival inside the bands.
- The Super licence at 30,000 or 33,000 DKK so that counting every sale would flip Super as well: the margin part
  read off the recorded gross margin lands within 400 of the plain estimate (Super 29,400 against 27,800), so any
  line that the plain estimate falls under also catches a route a judge could defend; the price list puts Super at
  27,000, every rival clears it by 2,400 or more, and the AND now sits in R8's figures rather than in the call.
- The waste gap split with the openings folded into the forecast's part (-16.3): the saving already took the
  openings' trade out of each pilot store's expected waste, so the split did the same (openings -0.3, forecast
  -15.7), and both readings sit inside the forecast's band.
- A Word note to the board as the second deliverable: every two-file set with a workbook is over the prompt corpus's
  shell quota, and a board decision's genre is a few slides, so the note became a four-slide deck.
- The full fresh range in every To Go store (the first stage 4 leak read's realism tell: a station kiosk selling raw
  minced beef): the To Go stores now carry the range without raw meat. Dropping the items from the world outright
  re-rolled every later random draw (a zero-mean demand draw consumes none), so the demand is drawn on the whole
  assortment and the unranged items zeroed, and the figures moved by under 300 DKK in every format.
- The whole saving carried on each store's waste by trading week, as a rival inside the bands: it widened Kvarter's
  band to the plain estimate's 23,400, so the trading-week sentence alone would have rescued R8 and half of R9 (3.5
  of 10). The pilot's own record rules it out instead: the weekend-trading Super pilot stores gave up 3.6 times the
  Kvarter ones' margin with 2.3 times their sales and 1.4 times their waste (asserted); it stays on the Routes sheet.
- The forecast's part of each gap labelled as the forecast alone (the first leak read): the recommended service
  factor changed with it in every pilot store and the record cannot part the two, so the part is labelled the
  forecast at its recommended setting, which is the package agreement 4.2 prices.
