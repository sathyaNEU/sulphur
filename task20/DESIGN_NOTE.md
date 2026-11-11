# task20: whether Brindle & Moss's fourth-quarter fiscal 2025 net sales clear the street's figure, from the Kestrel card panel three weeks before the release

Architecture 2, drawn 2026-11-11 as a re-root of architecture 1 (spent: see the last lines of `## Pre-ship check

- Leak sweep rulings (main thread, stage 4): the design-note vocabulary line on the filing excerpts (private-label,
  quarters, filing, results, penetration, tender) is harmless: those are the company's own disclosure words for its tender
  mix and quarters, and no sentence says how the panel relates to them; the same line on the vendor's bulletin
  (private-label, coverage, issuer, issuers, bulletin, history) is harmless: the bulletin states what the panel holds and
  when issuers joined and left, which the estimand needs, and names no adjustment; the answer-figure line on the filing
  (the third quarter's private-label share) is the company's reported figure, an input, not a result.
- Stage 4 in progress: the leak reader and the judge's isolated thread are running.

## Tried and rejected`),
from the author's concept note (Concept 3, "Card panel to reported revenue"). The answer is a quantity no record holds:
the quarter's net sales, rebuilt from the relation between a card panel (weekly, by issuer, region and card-open year,
bank cards only) and the company's reported quarters (quarterly, all tenders, by region once a year), and validated on
the quarters both records share.

## Draw

Subdomain: Quantitative Finance (Quantitative Finance and Trading), task type Alpha research (finding and validating
  return-predictive signals), carded under `strategy-backtesting-evaluation`, the Quantitative Finance key that serves
  Forecasting
Analysis type: Forecasting & Predictive Modeling
Answer shape: a forecast with its band and drivers: the quarter's net sales, an 80 per cent range earned on past
  quarters, each adjustment's worth, and whether the whole range clears the street's figure
Weight: validation: the range and the growth index have to be earned on rolling origins built as they would have been
  at each quarter, and the textbook calibration (reported growth regressed on the panel) passes its own back-test while
  missing the two changes this quarter carries; the last three live builds sat on etl conformance (task8), root-cause
  investigation (task9) and pricing (task21)
Data-native sentence: the panel sees bank-card spend by the cardholders of six issuers whose footprints are not the
  company's, one of which left at the quarter's start, while the company reports all tenders by store region once a
  year, so the quarter's net sales exist only as an estimate built across the two records' grains and validated on the
  quarters they share.
People: Audrey Hanson (consumer analyst, Larkhill Partners' research desk), Robert Campbell (portfolio manager, chairs
  the investment committee) (`guard.py names --geo us --seed 2611`). Neither appears in the prompt.

## Deep reasoning

Task type: strategy backtesting evaluation (`strategy-backtesting-evaluation`; the client's Alpha research, finding and
  validating return-predictive signals): an alternative-data nowcast of a listed retailer's quarterly net sales from a
  card panel, the signal validated on rolling origins and traded against the consensus
Domain test: the results are the quantities an alternative-data analyst at a long-short fund estimates before a
  print: the panel's like-for-like growth on a constant issuer set, its re-weighting to the company's footprint, the
  tender coverage adjustment (bank-card spend against all-tender net sales), the rolling-origin error of the nowcast, the
  80 per cent range and the trade it supports against the consensus
Swap: rewritten as a hospital's admissions forecast from an insurer's claims panel, the issuer set, card-open years,
  posting lags restated weekly, the private-label tender and the consensus line stop making sense; the regional
  re-weight survives as an idea but its file roles (a 10-K regional table, a 10-Q penetration table, sell-side
  estimates) do not
Where the weight sits: R6 and R7, the record and the range: each of 15 past quarters rebuilt on what was known three
  weeks before its release (the issuers in both years at that time, the prior fiscal year's regional mix, the
  private-label share carried from the quarters reported before it), which is long work, not a trick
Layer 1: posting lags leave each issuer's latest three weeks short in every delivery (issuers post late transactions);
  the vendor's name match rolls the licensed Hollister's shop-in-shops and the Brindle Cafes into the brand's merchant id
  (descriptor matching by trade name); issuers join (KS-04 in June 2022, KS-05 in December 2023) and leave (KS-06 after
  October 2025) as data agreements start and end; Fernhollow enters the consolidated results on 2 June 2024; fiscal
  2023 has 53 weeks; the site's spend arrives under two descriptors (the site and its payment facilitator). Each is
  handled by a step the careful column earns (R1 to R3), and none decides the call alone
Not one thing: the strongest single piece is the private-label card's faster fall (R5); a run that carries it still
  files the panel's own regional mix (R4 missed), and its estimate regressed on past quarters is USD 1,449.4 million with
  a range of USD 1,433.3 to 1,465.5 million, across the street, so R6, R7, R8's regional step and R9 stay to be earned;
  the regional re-weight alone leaves USD 1,440.2 to 1,491.0 million, across the street as well
One-fact test: "the private-label card's share of net sales has fallen faster in fiscal 2025 than before, and the panel
  holds no private-label cards" rescues R5 (1 of 9); "the panel's cardholders sit in different regions from the
  company's sales" rescues R4 (1 of 9); each leaves R6, R7 and R9 missed and R8 partly earned
Not semantics: every field, unit and clause read correctly (the panel's coverage, the descriptor detail, the paragraph
  on the licensed operations, the penetration table, the regional table) leaves the hurried estimate at USD 1,481.6
  million, because the reading never says how the panel's mix or its tender coverage relate to this quarter's net
  sales; those are estimated
Not rule application: no filed procedure builds R4 to R9; once the bulletin's coverage and issuer changes and the
  filing's paragraphs are applied, what is left is to choose the regional weights, to forecast the fourth quarter's
  private-label share, to build the record at each past quarter on what was known then, and to size the range
Estimand: the prompt fixes the quantity (net sales for the fourth quarter of fiscal 2025, the 13 weeks to 31 January
  2026, in USD million, as the company reports them), the range (80 per cent), the record (each past quarter the range
  could have been built for), the adjustments (each one's worth in points of year-on-year growth) and the call rule
  (short if the whole range sits below the street's figure, long if above, otherwise no position); the vendor's bulletin
  fixes the panel's coverage (general-purpose cards, no private-label cards) and the issuer changes; the filing fixes the
  fiscal calendar, the licensed operations, the regions, the tender split and the penetration by quarter
No decoy: the desk's third-quarter model (`larkhill_bmh_card_model_q3fy25.xlsx`) reproduces exactly by its own stated
  method from the shipped panel and results (spend per open card on the issuers in both quarters, the brand ids as
  delivered, reported growth regressed on it, intercept 1.95 points, slope 0.407, back-test 1.53 points) and answers a
  shallower quantity (a per-card index fitted to past quarters); it says nothing about the fourth quarter, and its own
  third-quarter line shows a USD 1,342.9 million estimate against USD 1,310.3 million reported; Ask 2 (the record) and
  Ask 3 (the adjustments) price it on the golden's footing, and carried to the fourth quarter it files USD 1,473.9 million
No replay: no result re-derives a published figure; the street's figure is the mean of eleven estimates and is the line,
  not a result; no stated number in the pack is wrong
Pinned: R1 by the descriptor detail and the filing's licensed-operations paragraph (one reading, band 14.21 to 15.21);
  R2 by the delivery history (medians, means and the last thirteen deliveries all 1.27); R3 by the vendor bulletin's issuer
  changes and the panel's card-open years (spend per card lands inside the comparable step's band); R4 by the filing's
  regional table (fiscal 2024, fiscal 2023 and fiscal 2024 rolled forward inside 5.88 to 7.55); R5 by the penetration
  table and the coverage paragraph (four rules for the fourth quarter's share inside 16.60 to 17.80, holding the third
  quarter flat ruled out by three successive and growing falls); R6 to R9 by the prompt's range, record and call rule
  with the eight golden-family routes inside every band (run on the cut pack, `checks.py` R6a to R6e)
Run forecast: R4 unfinished chain (the regional split built to describe the panel and dropped for the estimate); R5
  dismissed own evidence (the private-label card named as outside the panel and left to the regression); R6
  self-confirming check (the regression's own back-test); R7 and R9 self-confirming check (the regression's estimate and
  range, a long call); R8 unfinished chain (the bridge stopped at the panel's like-for-like growth)
Strategy label: Quantitative Finance and Trading 4, "Slow-moving predictors, proven in real time" (validation-heavy): the signal proven on what was known at each origin, the textbook calibration passing its own back-test
Depth level: 4, with level 5's mark: two connected judgments decide the call (the regional mix and the tender coverage,
  an AND: either alone leaves the range across the street), the record built on what was known at each quarter is a
  third, and three more independent steps (the entity, the immature weeks, the comparable panel) carry their own
  results; the shortcuts land on eight distinct wrong answers (`effort.py`)
Lesson: a signal that tracks its target in back-test can stop tracking when the panel's composition and the target's
  coverage change in the forward window; the remedy is to model each relation structurally and validate the structural
  chain, not to re-fit the shortcut. The house builds that teach validation_cannot_see_condition (mark258 v1, task4
  v11) teach it on a sensor drift and a scheduling rule; none on a panel's coverage and composition

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the licensed shop-in-shops' and cafes' share of the brand id's spend in November to January: 14.71% | assembly and reconciliation | the descriptor detail; the filing's licensed-operations paragraph | 14.21 to 15.21 | Right in the careful column; quick: method shortcut, the brand id taken whole as net sales | independent: the descriptor detail and the filing | Component 1 |
| R2 | completing the quarter's latest weeks lifts its spend by 1.27% (each issuer's first-delivered share of its final week at lags 0 to 2, medians over 27 deliveries) | missingness and measurement | the delivery history; the vendor bulletin's restatement | 0.97 to 1.57 | Right in the careful column; quick: unfinished chain, the delivered latest weeks taken as final | independent: the delivery history | Component 2 |
| R3 | the panel's own steps: delivered growth -14.67, completion +1.09, licensed shops and cafes -1.32, issuers in both years and cards of the same age +25.74 points (like-for-like growth 10.84%) | missingness and measurement | the vendor bulletin's issuer changes; the panel's card-open years | delivered -14.97 to -14.37; completion 0.77 to 1.39; licensed -1.62 to -1.00; comparable 24.79 to 26.04 | Right in the careful column; quick: method shortcut, every issuer's delivered spend | R1, R2 | Ask 3 (panel steps) |
| R4 | card-visible growth at the company's fiscal 2024 regional mix: 6.71% (the panel's own mix gives 10.84%) | modeling | the filing's net sales by region; the panel's billing regions | 5.88 to 7.55 | unfinished chain: builds the regional split to describe the panel's skew, then pools at the panel's own mix and leaves the gap to the regression's intercept (method shortcut: one pooled rate for regions growing -1.45 to 16.98%) | R3 | Component 3 |
| R5 | the private-label card's fourth-quarter share carried to 17.00% (20.6% a year earlier, 17.9% in the third quarter) and net sales per dollar of bank-card spend down 5.07% (bank cards 71.0% of net sales against 67.4%) | modeling | the filing's penetration table and tender split; the vendor bulletin's coverage | share 16.60 to 17.80; per bank-card dollar -5.64 to -3.96 | dismissed own evidence: names the private-label card as outside the panel and assumes the regression's history covers its fall (1.0 point a year before fiscal 2025, 2.7 points in its first three quarters) | independent: the filing and the coverage paragraph | Component 4 |
| R6 | the record: the chain rebuilt at each of 15 quarters from fiscal 2022 Q1 on what was known then, root mean square error 0.70 points, third quarter's error +1.22 (11 of 15 inside) | validation | the prompt's record ask; the results file; the panel's history | RMSE 0.54 to 1.07; Q3 error 0.47 to 1.95 | self-confirming check: certifies the regression on the panel's own mix with its rolling back-test (1.50 points), whose quarters held no issuer exit and the slow private-label fall, and passes over its 3.31-point third-quarter miss | R4, R5 | Ask 2 |
| R7 | net sales USD 1,412.5 million (+1.30% on USD 1,394.4 million), 80% range USD 1,400.0 to 1,425.0 million | forecasting | the prompt's quantity and range; the record's error | estimate 1,402.5 to 1,427.6; low 1,387.9 to 1,412.4; high 1,417.1 to 1,442.7 | self-confirming check: the regression's USD 1,481.6 million with a range from its own record (USD 1,454.8 to 1,508.5 million); dismissed own evidence on the fiscal 2025 errors | R4, R5, R6 | Ask 1 |
| R8 | the company steps: the regional mix -4.13 and the bank-card share -5.41 points | decomposition and attribution | the bridge's order as applied; R4 and R5 | mix -4.96 to -3.29; bank-card share -6.02 to -4.22 | unfinished chain: a bridge that stops at the panel's like-for-like growth and books the rest to the regression | R4, R5 | Ask 3 (company steps) |
| R9 | short: the top of the range (USD 1,425.0 million) sits USD 25.0 million below the street's USD 1,450.0 million | synthesis | the prompt's call rule; the street's eleven estimates | the call exact; the top 1,417.1 to 1,442.7 | self-confirming check: long, the regression's range wholly above the street | R7 | Recommendation |

Carry-forward: R1, R2 and R5 are graded on inputs of their own (the descriptor detail, the delivery history, the
filing); R3 and R4 are graded on the panel's own figures, so a run that misses R1 or R2 loses R3's cells for those steps
only; R6 to R9 depend on R4 and R5 because the grader compares the run's figures with the golden's, and the chain is an
AND by design (either correction alone leaves the call across the line), so a slip at R4 or R5 costs R6 to R9 and the
matching step of R8, and nothing upstream.

## Hidden factor record

The licensed shops under the brand id and the posting lags are Layer 1 (filed processes: the vendor bulletin's matching by
trade name and restatement, the filing's licensed operations), handled at R1 and R2 and priced Right; they are not
factors a run has to find.

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| KS-06, the Midwest issuer, leaves after the week of 26 October 2025 | constructed (simulated), filed in the vendor's bulletin | no: three issuer changes across the panel (KS-04 2022, KS-05 2023, KS-06 2025); its effect is the regional mix the panel carries in every quarter | the vendor's bulletin, then modelling: its exit sharpens the panel's skew beyond anything the back-test's quarters held | modelling (constant issuers and the company's mix together) | keep: filed, not hidden; alone it decides nothing (constant issuers is R3, priced Right) |
| the panel's regional skew (issuers' footprints Southeast and West heavy against a Northeast and Midwest heavy company) | constructed, through the issuers' footprints | no: every quarter's panel weights and every year's regional table | a group-by of the panel by billing region against the filing's regional table | modelling: the re-weight is routine, but a regression on past quarters absorbs its average, so the decisive part is the change this quarter | keep: alone it leaves the range across the street (mix alone USD 1,440.2 to 1,491.0 million) |
| the private-label card's faster fall in fiscal 2025 (the partner tightened approvals) | constructed, filed in the 10-Q | no: four quarters of the penetration table and the record's fiscal 2025 errors | the penetration table read against the panel's coverage | modelling: a forecast of the fourth quarter's share and the tender identity | keep: alone it leaves the range across the street (USD 1,441.2 to 1,493.1 million, or 1,433.3 to 1,465.5 regressed) |
| the holiday quarter's demand turn (purchases per visit down from November) | constructed outcome: the quantity the panel measures, not a factor to remove | n/a: it is the target | the panel itself, once the two corrections are made | none | keep: no step removes it; the uncorrected panel hides it (like-for-like 10.84% against fiscal 2025's reported 4.2 to 5.5%) |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the reporting entity: the licensed shops' and cafes' share of the brand id's quarter | Missed | Right | Right |
| R2 the quarter's latest weeks completed from the delivery history | Missed | Right | Right |
| R3 the panel's own adjustments and its like-for-like growth | Missed | Right | Right |
| R4 card-visible growth at the company's regional mix | Missed | Missed | Right |
| R5 the private-label card's fourth-quarter share and the bank-card share's change | Missed | Missed | Right |
| R6 the range's record: rolling-origin error and the third quarter's miss | Missed | Missed | Right |
| R7 the quarter's net sales with its 80 per cent range | Missed | Missed | Right |
| R8 what the regional mix and the bank-card share are worth | Missed | Missed | Right |
| R9 the call against the street | Partly | Missed | Right |
| Roughly | 0.5 of 9 | 3 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "the private-label card's share of net sales has fallen faster in fiscal 2025 than before, and the panel holds no private-label cards"; rescues 1 of 9 results (R5; R8 to Partly)
Pair estimate: 32.8 (the careful but hurried pass: R1 to R3 earned, the regression on the panel's own mix filing USD 1,481.6 million and a long call); the quick pass scores 14.0 (the delivered panel's -14.67% calls short for the wrong reason)

## Data provenance

Source: generated by the seeded generator in task20/generator from a simulated retailer and card panel: the company's
  weekly sales by region and channel (a category trend by fiscal year with a demand turn in the holiday quarter,
  regional trends, the retail calendar's holidays, a rising web share), Fernhollow consolidated from 2 June 2024, the
  shop-in-shops and cafes others run under the brand, the tender mix (bank cards, the private-label card, other tenders) with the
  private-label card's fall quickening in fiscal 2025; the panel's six issuers with their regional footprints, joins and
  an exit, card cohorts opened each quarter with back books at each issuer's first week, attrition, spend that settles
  with card age, posting lags and the weekly deliveries; the street's estimates; the desk's documents
Behaves like the real thing: the card panels funds buy from bank issuers (Kestrel stands for the type), with the
  published behaviours of that data: a panel skewed to its issuers' footprints, issuer churn as data agreements start and
  end, the latest weeks restated as late transactions post, merchant matching by descriptor that rolls licensees into
  the brand, bank-card coverage only (no private-label or cash tender), and a 4-5-4 retail calendar with a 53rd week
Genuine patterns: (1) seasonality with the retail holidays (Presidents' Day, Memorial Day, the Fourth of July, Labor
  Day, Black Friday and Cyber Monday, the week after Christmas), (2) regional growth from -4% a year in the Northeast to
  13% in the Southeast, (3) the web share rising from 17 to 27 per cent, (4) new accounts spending more and settling over
  about a year, (5) attrition of about a fifth of cards a year against quarterly cohorts, (6) licensees growing faster
  than the banner
Problems by process: posting lags (the latest three weeks provisional and restated in each delivery); issuer joins and
  an exit; the vendor's name match rolling the licensees into the brand id; the acquisition part-way through fiscal 2024;
  the 53-week fiscal 2023; the site's payment-facilitator descriptor
Breadth: 10 files (8 used, 2 distractors), 6 issuers, 4 regions, 10 card-open years, 3 merchant ids, 261 weeks, 110,040
  panel rows, 27 deliveries, 45 descriptors, 19 reported quarters, 11 brokers

## Template check

Chain signature: assembly and reconciliation, missingness and measurement, missingness and measurement, modeling,
  modeling, validation, forecasting, decomposition and attribution, synthesis
Question form: which side of a line (will net sales come in above or below the street), with how much (the estimate and
  its range); the deliverables a spreadsheet and a short note
Nearest build: task18 by chain (assembly, measurement, modeling, decomposition) is a ranked-causes investigation of a
  system's unmetered loss; task5 v4 shares the reporting-lag nowcast lesson on a county census completed by report, with
  a set-over-threshold decision; task12 v1 shares stratify-and-reweight-to-target in a banded call; none has a panel's
  coverage, an issuer exit or a validation built at each origin

## Frontier check

Precedents: R4 L11, L25 (built the split for the first step and dropped it for the next; pooled the comparison areas
  instead of matching, reporting the trial's own mix); R5 N02, N06 (history assumed informative of the forward window;
  long-run behaviour assumed unchanged); R6 L28 (certified the estimator with checks that cannot see the problem); R7
  L28, N02; R8 L11, N06; R9 L28, N02.
Shallow path checks: the hurried route (issuers in both years, cards of the same age, reported growth regressed on the
  panel at its own mix) passes its own rolling back-test (1.50 points over nine quarters), a placebo of the same
  regression on fiscal 2024 alone, and the desk's third-quarter model it reproduces in kind; the check of another kind
  is the record of the structural chain against the regression in fiscal 2025 (third quarter 1.22 against 3.31 points),
  and the panel's weights by billing region in the target quarter against the filing's regional table (41.86% Southeast
  against 26.19%), which needs the 10-K's annual table at another grain from the weekly panel; and the penetration table,
  quarterly at the company's grain, against the vendor bulletin's coverage.
Assumption made false: a run lists "the relation between panel growth and reported growth is stable" and "the panel is
  representative after constant-issuer filtering" and moves on; the world's process makes both false this quarter (the
  partner's tighter approvals quicken the private-label card's fall, so bank cards pay for 71.0% of net sales against 67.4% and each dollar the panel sees stands for 5.07% less net sales; the Midwest
  issuer's exit leaves the comparable panel 79% Southeast and West), and the pack tests each (the 10-Q penetration table;
  the 10-K's regional table against the panel's billing regions).
Forcing: the line is the street's USD 1,450.0 million (the mean of eleven estimates; the median 1,448.4 and the latest
  five 1,448.6 give the same call); the golden family's range tops run USD 1,420.1 to 1,439.7 million, nearest 10.3
  below the line; the shortcuts' range tops (or point, for the trend) run USD 1,458.7 to 1,508.5 million, nearest 8.7
  above; other tenders at 10 and 14 per cent, the last week's completeness 3 per cent either way, the licensed share a
  fifth either way and the range from the record's error percentiles keep the top between USD 1,420.2 and 1,431.6
  million, all below the line.
Noun swap: the nearest by skeleton.py check is task5 v4 (severity none): its county counts completed by report become
  the panel's immature weeks, and only the reporting-lag nowcast and the second source at another grain carry across;
  the decision form (act if the interval clears the line here, a set over a threshold there), the deciding lessons (the
  panel's composition change and the tender coverage), the moves and the answer pattern do not; task12 v1 shares the
  re-weight to the target's mix in a banded call, severity none.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | the street's figure | the mean of the eleven estimates / the median / the latest five | the mean, USD 1,450.0 million | same call (median 1,448.4, latest five 1,448.6, all above every family range) |
| SF2 | net sales | as reported, Fernhollow included / organic | as reported; Fernhollow is consolidated in both quarters | the prompt ("net sales ... when the company reports"); the filing's acquisition paragraph |
| SF3 | growth basis | weekly averages / quarter totals | weekly averages; both quarters have 13 weeks | same call (identical for the quarter); the filing's 53-week fiscal 2023 for the record |
| SF4 | the comparison quarter | the fourth quarter of fiscal 2024 / the third quarter of fiscal 2025 | the fourth quarter of fiscal 2024, the 13 weeks to 1 February 2025 | the prompt's "year-on-year growth" |
| SF5 | the licensed shops and cafes | kept in the brand id / taken out | taken out by month (14.71% of the quarter) | the filing: their sales are not net sales |
| SF6 | Fernhollow in the panel before its acquisition | kept / from 2 June 2024 | from 2 June 2024 | the filing's acquisition paragraph; same call for the quarter |
| SF7 | completion factors | medians / means / the last thirteen deliveries | medians over the 27 deliveries | same call (all 1.27%) |
| SF8 | the regional weights | fiscal 2024 / fiscal 2023 / fiscal 2024 rolled forward | the prior fiscal year's net sales by region (fiscal 2024) | inside R4's band; same call |
| SF9 | the fourth quarter's private-label share | fiscal 2025's pace / the latest year-on-year change / a straight line / the third quarter's change / held flat / the quarter's own | the pace of fiscal 2025's first three quarters, 17.00% | four rules inside R5's band; held flat ruled out by three successive and growing falls (0.6, 1.0, 1.1 points); the quarter's own share is not known three weeks before the release |
| SF10 | other tenders | the 10-K's 12% held / moved | 12% held | same call at 10% and 14% |
| SF11 | the 80 per cent range | 1.2816 times the record's RMSE / the record's 10th and 90th percentile errors | 1.2816 times the RMSE | same call (top USD 1,424.8 million) |
| SF12 | the call | the prompt's rule | short only if the whole range sits below the street's figure | the prompt |
| SF13 | the record's first quarter | fiscal 2022 Q1 (the first with a year-earlier panel and a prior year's regional mix) / fiscal 2023 Q1 | fiscal 2022 Q1 | inside R6's band; same call |
| SF14 | calibration | the chain as built / reported growth regressed on the chain | as built | the regression lands inside R6 and R7's bands; same call |
| SF15 | the panel's normalisation | cards of the same age / spend per card | cards of the same age | spend per card lands inside R7's band with the same call; ruled out for R4 by its record (1.19 against 0.70 points) and the panel's spend per card falling with card age |
| SF16 | the issuers | every issuer / issuers in both quarters | issuers in both quarters, KS-01 to KS-05 | the vendor bulletin's issuer changes |
| SF17 | the site's payment-facilitator descriptor | the site / not the site | the site (online orders are net sales) | same call (in every month of both quarters) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | population: Brindle & Moss's net sales as reported, Fernhollow consolidated (SF2) |
| 2 | outcome: net sales in USD million for the fourth quarter of fiscal 2025 (the prompt) |
| 3 | window: the 13 weeks from 2 November 2025 to 31 January 2026 (the prompt; the results file) |
| 4 | unit: USD million for net sales, points of year-on-year growth for each adjustment; in each asking sentence |
| 5 | comparison: the fourth quarter of fiscal 2024 (SF4), and the street's figure for the call (SF1) |
| 6 | as-of: the panel's delivery of 2 February 2026; the filing's 10-Q of 10 December 2025 |
| 7 | grain: week, issuer, billing region and card-open year in the panel; quarter in the results; fiscal year in the regions |
| 8 | members not yet observed: the quarter's last week as first delivered, completed by each issuer's factor (R2) |
| 9 | which delivery: the latest restates the history; the history file gives the first-delivered values |
| 10 | prices: none |
| 11 | rounding: net sales to USD 0.1 million, growth and steps to 0.01 points, shares to 0.01 per cent; the answer blocks |
| 12 | threshold: the street's figure (SF1) and the call rule (SF12) |
| 13 | tie-break: none needed (the call's margin is USD 25.0 million) |
| 14 | expected value: none; the range is 80 per cent, two-sided |
| 15 | the regional weights: the prior fiscal year's (SF8) |
| 16 | the private-label rule: fiscal 2025's pace (SF9); four rules inside the band |
| 17 | other tenders: 12% held (SF10) |
| 18 | the record: rolling origins from fiscal 2022 Q1, each built on what was known then (SF13) |
| 19 | the range: 1.2816 times the record's RMSE (SF11) |
| 20 | the panel's normalisation: cards of the same age (SF15) |
| 21 | the entity: the brand id less the licensed shops and cafes, the site, Fernhollow (SF5, SF6, SF17) |
| 22 | the issuers: in both quarters (SF16) |

## Literal reader

The prompt asks for the quarter's net sales in USD million with an 80 per cent range, how that range would have held in
each past quarter it could have been built for, what each adjustment to the card data is worth in points of
year-on-year growth, and the call by its stated rule; the vendor's bulletin fixes the panel's coverage (general-purpose cards,
no private-label cards), the restatement of the latest weeks with the first-delivered history, the matching by trade
name and the issuer changes; the filing fixes the calendar, the licensed operations, the acquisition, the regions, the
tender split and the penetration by quarter. Executed word for word with the estimates the data force, they give the
golden's estimate, range, record, steps and call; no reading of a filed sentence gives another call.

## Prompt contract

A voice rewrite may not drop or change: the question (above or below the street's figure when the company reports on
26 February); the quarter (the fourth quarter of fiscal 2025, the 13 weeks to 31 January 2026); the opening reason (the
card panel is the only read before then and a sample of cardholders, not the company's books, so the answer is an
estimate); the four asks (net sales in USD million with an 80 per cent range; how the range would have held in each past
quarter it could have been built for; each adjustment's worth in points of year-on-year growth; the call by its rule,
short if the whole range sits below the street's figure, long if above, otherwise no position); the deliverables (a
spreadsheet and a short note). It must never add: a rounding instruction, a method or model, a warning, a file name, a
role, the issuer that left, the regions, the private-label card, the licensed shops, the posting lags, a count of
issuers or estimates.

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
- 2026-11-11, architecture 1 as built (the extracts' cutoff as the careful pass's loss at R3, R4 and R6, the store's graduations as its loss at R8): the determinism judge's isolated thread, at medium effort and before it opened the answer blocks, replicated ERE to the dollar, reconciled product control's hypothetical P&L against the extracts and found the closing allocations booked after the cut, classified every exception as the golden does ((a) 1, (b) 4 on the golden's dates, (c) 11) and computed the month-by-month add-on from MRS-4 6 read literally (0.324, 0.273, 0.114, 0.076, 0.035, 0); priced on that pass the careful column lands near 95, so the chain returns to stage 2. In this world the cutoff cannot be both hidden and not one thing: the allocations (a median USD 39 million gross a night) show in any reconciliation of a P&L that carries them, and kept out of every P&L they decide most results; and the add-on's month-by-month mapping is a filed rule once MRS-4 6 pins it. The judge's determinism findings carried to the redesign: the 4(d) EWMA timing (the then-current volatility through the scenario date gives a sound count of 3 at every decay, 28 March 2025 under (e)); the runs on which the reported VaR sat above ERE's on the book held (133 of 250, not 129 of 249); the add-on's base book pinned to the positions ERE read on 30 June; the plan approved after the 30 June run it cites; the crosswalk dated from the 17 January replay.
- 2026-11-11, re-root: architecture 1 (the SMCF desk's VaR exception classification on the S&P 500 and Nasdaq-100 tape) is spent on the judge's first pass above; architecture 2 moves to another world, dataset and shell, the author's Concept 3 (a card panel's nowcast of a retailer's quarterly revenue before the release), whose answer is an estimate no record holds.

- 2026-11-11, architecture 2 prototype: a cut in the panel's new accounts from fiscal 2024 (cohorts at 62 per cent) made total spend on the issuers in both years, regressed on past quarters, land inside the golden's band by coincidence (the shrinking card base cancelled the bank-card share's rise); the cut was dropped, and each issuer's card base now grows from its back book toward its steady state.
- 2026-11-11, architecture 2 prototype: a category cycle that put the quarter's true growth near the history's average let every weak-signal regression and fiscal 2025's reported trend land on the golden's side; rebuilt as reported growth of 3.5 to 8.4 per cent through the third quarter of fiscal 2025 (the street's +3.99% in line with it) and a demand turn in the holiday quarter (purchases per visit down) that only the corrected panel shows; the site-visits feed counts visits, so the turn does not show there.
- 2026-11-11, architecture 2: an ask for each region's growth dropped from the prompt (it hands R4's re-weight over); the regional figures are graded inside Ask 3's adjustments, and the 10-Q's sentence expecting penetration to keep falling in the fourth quarter was cut (a filed forecast of R5's input).
- 2026-11-11, architecture 2: the Midwest issuer at its first size (0.85 of the largest) left the drift-only regression's range below the street in some seeds; at 1.30 the comparable panel is 79 per cent Southeast and West after the exit, and the single-correction routes land across the line in seed 17 by USD 15.5 million or more.
