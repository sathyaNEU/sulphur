# task15: which three Stage 3 lines Banyena nominates to the high-rainfall series for 2027, and why its past nominations fell short of its own trial figures

Architecture 1, drawn 2026-11-10 on the client's bar of 2026-11-09 (difficulty throughout, never one thing). The
author assigned the domain (General Statistics & Data Science); the analysis type was chosen at intake, Comparative
Analysis & Explanation, because no build on file carries it and the client names it among the three it most wants.
This note is completed at stage 2; the draw, the process behind the files and the chain's sketch stand below.

## Draw

Subdomain: General Statistics & Data Science (Machine learning research group)
Analysis type: Comparative Analysis & Explanation
Answer shape: a bridge that reconciles two totals (the mean advantage Banyena's own trials promised for its past nominees against the mean advantage they realised in the independent series, each reconciling item estimated, the unexplained part shown), with the 2027 nominations as the recommendation on top
Weight: attribution: the shortfall has three sources that move together in the record and each has to be estimated from a different part of it before the bridge closes; task5 sits on a hard-to-measure quantity, task7 on modeling, task4 on measurement
Data-native sentence: a staged breeding record observes every line a different number of times, in trials that are drier than the series the lines are nominated to and against a benchmark bred for that series, and it advances lines on the same noisy means it later quotes for them, so the figure quoted for a nominee and the figure it realises differ for reasons the record itself has to separate.
People: Meredith Cooke, head of breeding at Banyena Grain Genetics; Jesse Gibson, trials and data manager; Michaela Baxter, variety manager at Mount Rouse Seeds (the seed partner); John Morgan, coordinator of the High Rainfall Barley Series (`guard.py names --geo "Australia" --seed 15`). None appears in the prompt.

- **Card:** `.claude/skills/fingerprint/cards/task15.json`, architecture v1, registered 2026-11-10. `guard.py check` on
  the registered card: PASS, after two axes were redrawn when main moved under the draw (task5 architecture 4 entered
  the window at 01:59Z): prompt shape 03 to 01 (the repeated unit the rubric grades is each Stage 3 candidate's row,
  in or out of the three nominations, with the bridge beside it, which is the honest label and not only the passing
  one), and context artifact published_series to close_out_summary (the head of breeding works from the company's own
  season close-out and nomination dossiers; the series' published results are the realised outcomes, filed under the
  calibration form). Nearest drivers by text 0.05 (mark258), 0.04 (task8, task7): no structural match on gap, pattern
  and Gate G.
- **Task type:** multiple testing and selective inference (it serves Comparative Analysis & Explanation in the house
  mapping; never drawn before).
- **World:** Australia, western Victoria. Banyena Grain Genetics, a grower-owned barley breeding company in the
  Wimmera, bred for the dry Mallee and Wimmera; the High Rainfall Barley Series, an independent trial series of the
  Southern Cropping Trials Trust in the south-west; Mount Rouse Seeds, the seed partner whose uptake standard is a
  two-season mean of at least 103 per cent of the benchmark variety Byaduk in the series. Every organisation and
  variety is invented; the towns are real and the weather is simulated to their climate.
- **Forum, forcing event, organisation family:** customer_or_counterparty (the series takes the nominations and the
  seed partner takes up what meets its standard), season_or_peak (nominations and seed for the 2027 sowing),
  agriculture_or_food_producer.
- **Deliverables:** a workbook, a chart of the bridge and a short note (three files; the set repeats no recent build).

### The process behind the files

Written before any result was named (`stumping` 1.1). Each year Banyena sows about 300 new lines in Stage 1 at two
sites (two replicates), advances about a quarter to Stage 2 the next year at five sites, and about twenty of those to
Stage 3 at ten sites (three replicates), where the better half of a year's new Stage 3 lines are kept for a second
Stage 3 season. Every trial carries four check varieties, Byaduk among them. Lines are advanced at the end of each
season on that season's trial means as a percentage of Byaduk, with some breeder's taste, and a line gets a new code
when it reaches Stage 3. The trials manager's harvest system records every plot: its trial, replicate, block and
position, the weight off the plot and its moisture, a lodging score taken before harvest, and whether the plot was
harvested or abandoned (badly lodged plots are sometimes left). Seven of the ten sites are dryland Mallee and Wimmera
sites, two sit on the dry edge of the high-rainfall zone and one is irrigated; the season's water at a site (rain
from April to October, plus irrigation) is in the weather and irrigation records, not in the plot file. Each year the
head of breeding nominates three Stage 3 lines to the High Rainfall Barley Series on an index of her own: the line's
mean percentage of Byaduk at the three wetter sites over its Stage 3 seasons. The nomination dossier quotes that index
as the advantage to expect. The series then grows each nominee for two seasons at ten high-rainfall sites beside
Byaduk and other breeders' entries, harvests every plot, and publishes each entry's site means and lodging scores.
What nobody at Banyena sees directly: how much of a quoted index was the luck that got the line picked; that Byaduk,
a high-rainfall variety, gains more yield per millimetre of season water than Banyena's dryland-bred lines; and what
lodging costs a weak-strawed line at sites lusher than any of Banyena's own.

## Results chain

Sketch at the draw (pins, bands and the hurried figures are filled at stage 2 from the generator's own passes):

| ID | Result (checkable) | Area |
|---|---|---|
| R1 | the conformed trial record (trials, plots, lines followed across their codes) and the shortfall itself: the mean advantage promised and the mean advantage realised by the nominees with two completed series seasons | assembly and reconciliation |
| R2 | the part of the shortfall that is selection on noisy means, with lines seen for one Stage 3 season shrunk more than lines seen for two | causal reasoning (selection) |
| R3 | the part that is the benchmark's larger gain per millimetre of season water, carried from the programme's sites to the series' sites | modeling |
| R4 | the part that is lodging: the yield lost per score unit, estimated within line and trial with the abandoned plots allowed for, carried to the series' lodging pressure | missingness and measurement |
| R5 | the bridge closed: promised, less the three parts, against realised, with what stays unexplained and its range | decomposition and attribution |
| R6 | the corrected prediction's error on the past nominees (each predicted from the record as it stood when it was nominated) against the breeder's index | validation |
| R7 | every 2026 Stage 3 line's expected advantage over Byaduk in the 2027 and 2028 series, with an 80 per cent band | forecasting |
| R8 | each nominee's chance of meeting the 103 per cent two-season standard, and the chance that at least one of the three does | uncertainty |
| R9 | the three nominations in order, the first line left out, and the lines the breeder's index would have nominated instead | synthesis |

One-fact test at the draw: the most useful single sentence ("the benchmark gains more yield per millimetre of season
water than our lines") rescues R3 and moves R7 part of the way, 2 of 9; "lines are quoted on the means they were
picked on" rescues R2 alone; "weak-strawed lines lodge harder in the series" rescues R4 alone; no sentence about the
record gives R8, which needs the spread of realised two-season means with the benchmark and the weather shared. The
three nominations need all three parts at once: on the feasibility prototype the breeder's index, the index scaled
for selection alone, the water response without lodging and lodging without the water response each named a
different set of three.

Feasibility before the draw (a prototype of the process, eight seeds, in the session's scratch space, no pack cut):
over 24 completed nominees the shortfall ran 6 to 13 points of yield advantage, of which selection 1.4 to 5.0, the
water response and lodging together 2.9 to 7.7 and the unexplained remainder within about one and a half points; the
corrected prediction's error on the nominees was about a third of the index's; the abandoned plots moved the index by
under one point (so they are texture inside R4, not a result of their own).

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
