# task15: which Fjordkob store formats move their fresh ordering to Kornblomst's forecast for 2027, and why the pilot stores' fresh sales grew less and their fresh waste fell further than the other stores'

Architecture 2, drawn 2026-11-11. Architecture 1 (Banyena Grain Genetics' nominations to the High Rainfall Barley
Series) was READY and never run on the platform; the author re-rooted it for a much stronger stump with at least three
major analytical failure points in areas the earlier builds did not use, never task6's strategy (its line is under
`## Tried and rejected`). One architecture per world: this draw moves to another world (a Danish grocery chain),
another dataset (a simulated fresh-ordering field trial) and another shell. The careful but hurried column is
calibrated to the Sulfur run record: a run reads every file, reconciles every count, runs the field's textbook
method, models any pattern one plot shows and validates on held-out rows. So no result here is priced on a pattern
one table shows; each priced result is a correction the record in hand cannot flag (what the sales record does not
contain, which part of a loss another item recovered, whether the stores tried are the stores the answer is about),
estimated from a second file at another grain.

## Draw

Subdomain: General Statistics & Data Science
Analysis type: Comparative Analysis & Explanation
Answer shape: ranked causes with their contributions (the pilot stores' fresh sales growth gap and fresh waste gap
  against the other stores, each split into its causes and ranked by size), with the board's rollout option and each
  store format's expected yearly saving per store on top
Weight: synthesis: the call rests on many separately estimated pieces pulled into one ranked, reconciled account (the
  units lost to empty shelves, the paired item's recapture, the competitor openings, the formats' own growth, what the
  forecast's saving depends on in a store, each format's saving and its range), and two of them reach the same lost
  sales by different routes that must agree; the last two live builds lean on assembly (task16) and allocation
  (task9), and architecture 1 of this slot leaned on attribution
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
  population second (the pilot's stores are not the stores the rollout reaches); the decisive generator is G3
  record against operation (the sales record is not the demand); the decision is one of the board paper's four
  rollout options. After the rebase onto main the same day, task14's architecture 3 entered this card's window
  with decisive pattern G3 (`ban.pattern`), so the decisive generator moved to G6 composition shift, the honest first
  label for the call (the To Go format turns on the pilot's stores not being the format's stores), G3 second; re-checked
  on the registered card: WARN only. WARNs answered: `overuse.forum` (board_of_directors): a licence of this size is the board's to
  sign under the chain's delegation, and no other forum holds it; `repeat.deliverables` (pdf+xlsx against task1 v3,
  on the first check): a board paper and the workbook behind it is the genre of a rollout decision, and the shape,
  sheets and chart differ.
- **World:** Denmark, East Jutland. Fjordkob A/S, a regional grocery chain of 48 stores in three formats: 10 Fjordkob
  Super (large supermarkets), 20 Fjordkob neighbourhood stores and 18 Fjordkob To Go (small stores at railway
  stations, office districts and campuses), supplied every night from one fresh warehouse in Aarhus. Kornblomst
  Analytics, a forecasting vendor. Every organisation, store and product is invented; the towns are real. The
  setting is September 2026: the pilot ran from Monday 2 March to Sunday 30 August 2026, the dashboard's last week is
  week 35, and the board meets on Tuesday 6 October 2026 to sign or decline Kornblomst's 2027 licence, which the
  vendor needs by 1 November for a January start.
- **Forum, forcing event, organisation family:** board_of_directors, purchase_order_or_contract,
  retailer_or_ecommerce.
- **Deliverables:** a workbook and a short board paper with a chart (two files).

### The process behind the files

Written before any result was named (`stumping` 1.1). Fjordkob's fresh range is 36 items in five categories (bakery,
fruit and vegetables, dairy, meat and fish, ready meals), each subcategory holding two items a customer will take in
place of each other (two rye breads, two salad bags). Every evening each store's order for the next morning is
computed by the ERP's replenishment module, AutoOrdre: an order-up-to target of the next day's forecast plus a safety
stock, less the stock that will still be sellable, rounded up to the supplier's case pack. AutoOrdre's forecast
smooths each store and item's own sales with that store's own weekday pattern, and the category planners add the
uplift for each promotion week. Kornblomst's forecast, a chain-wide machine-learning model fed the weather, local
events and the promotion calendar, replaced AutoOrdre's forecast in 16 pilot stores for the 26 pilot weeks; the
regional managers chose the pilot stores (five Super, eight neighbourhood and three To Go), and they chose stores they
trusted to run a trial well. The tills time-stamp every sale; the daily store and item extract carries the units
sold, the sales value, the time of the last sale, the delivery, the waste scanned at close (some of it scanned the
next morning) and the closing stock the ERP calculates. Business intelligence keeps a weekly store and category
history for the older weeks, the weekly ambient (non-fresh) sales, and the hourly sales profiles by format, category
and weekday it measured on days the shelf did not run empty, which drive the store app's empty-shelf alert. Market
intelligence logs every competitor that opens within two kilometres of a store. The pilot dashboard reports, week by
week, waste as a share of fresh sales, availability as the share of store and item days with stock at close, and
forecast accuracy against sales, for the pilot stores and the rest. What nobody at Fjordkob sees directly: the demand
a shelf turned away after its last unit went, which the record holds only as a last-sale time and a zero; how much of
it customers bought as the other item of the pair, which depends on how much choice the store's shelf offers; that
Kornblomst's chain-wide model learned the week of a big store, so in a store whose trade falls away at the weekend it
orders too much for Saturday and Sunday and too little for the working days; that two discounters opened near pilot
stores during the pilot; and that the To Go stores the managers picked are high-street stores that trade like small
supermarkets, unlike the station and office stores that make up most of the format.

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
