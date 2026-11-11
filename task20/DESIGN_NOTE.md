# task20: whether Brindle & Moss's fourth-quarter fiscal 2025 net sales clear the street's figure, from the Kestrel card panel three weeks before the release

Architecture 2, drawn 2026-11-11 as a re-root of architecture 1 (spent; see the last lines of the tried-and-rejected
section), from the author's concept note (Concept 3, "Card panel to reported revenue"), hardened at stage 2 after the
judge's first pass. The answer is a quantity no record holds: the quarter's net sales, rebuilt from the relation between
a card panel (weekly, by issuer, region and card-open year, bank cards only, payments when customers order) and the
company's reported quarters (all tenders, recognised on delivery, with wholesale contracts no card carries), and
validated on the quarters both records share.

## Draw

Subdomain: Quantitative Finance (Quantitative Finance and Trading), task type Alpha research (finding and validating
  return-predictive signals), carded under `strategy-backtesting-evaluation`, the Quantitative Finance key that serves
  Forecasting
Analysis type: Forecasting & Predictive Modeling
Answer shape: a forecast with its band and drivers: the quarter's net sales, an 80 per cent range earned on past
  quarters, each step's worth from the card data to net sales, and whether the whole range clears the street's figure
Weight: validation: the estimate and its range are earned on rolling origins built as they would have been at each
  quarter, and the field's textbook pass (comparable panel, regional re-weight, tender coverage) passes its own record
  while missing what separates customer payments from this quarter's net sales; the last three live builds sat on etl
  conformance (task8), root-cause investigation (task9) and pricing (task21)
Data-native sentence: the panel sees what bank-card holders of six issuers paid when they ordered, while the company
  reports net sales of all tenders when merchandise is delivered, plus contract sales no card carries, so the quarter's
  net sales exist only as an estimate built across those differences and validated on the quarters both records share.
People: Audrey Hanson (consumer analyst, Larkhill Partners' research desk), Robert Campbell (portfolio manager, chairs
  the investment committee) (`guard.py names --geo us --seed 2611`). Neither appears in the prompt.

## Deep reasoning

Task type: strategy backtesting evaluation (`strategy-backtesting-evaluation`; the client's Alpha research, finding and
  validating return-predictive signals): an alternative-data nowcast of a listed retailer's quarterly net sales from a
  card panel, the signal validated on rolling origins and traded against the consensus
Domain test: the results are the quantities an alternative-data analyst at a long-short fund estimates before a print:
  the panel's like-for-like growth on a constant issuer set, its re-weighting to the company's footprint, the tender
  coverage (bank-card spend against all-tender sales), the conversion of what customers paid into what the company
  recognises (payments less the change in customer deposits for a retailer that books revenue on delivery), the part of
  net sales no card carries (wholesale contracts), the rolling-origin error of the nowcast, the 80 per cent range and the
  trade it supports against the consensus
Swap: rewritten as a hospital's admissions from an insurer's claims panel, the issuer set, card-open years, posting lags,
  the private-label tender, made-to-order deposits recognised on delivery, invoiced contract sales and the consensus line
  stop making sense; the re-weight to a footprint survives as an idea but none of its file roles do
Where the weight sits: R6 and R7, the record and the range: each of 15 past quarters rebuilt on what was known three
  weeks before its release (the issuers in both years then, the prior fiscal year's regional mix, the private-label share
  carried, last year's deposits scaled by that quarter's last eight weeks of payments and made-to-order share, wholesale
  at the median of the eight quarters before it), which is long work, not a trick
Layer 1: posting lags leave each issuer's latest three weeks short in every delivery (issuers post late transactions);
  the vendor's name match rolls the licensed Hollister's shop-in-shops and the Brindle Cafes into the brand's merchant id;
  issuers join (KS-04 in June 2022, KS-05 in December 2023) and leave (KS-06 after October 2025) as data agreements start
  and end; Fernhollow enters the consolidated results on 2 June 2024; fiscal 2023 has 53 weeks; the site's spend arrives
  under the site, its payment facilitator and its custom-order descriptor. Each is handled by a step the careful column
  earns (R1), and none decides the call alone
Not one thing: two independent deep steps carry the call, each alone leaving the range across the street. Revenue on
  delivery without wholesale gives USD 1,452.6 to 1,497.8 million; wholesale without revenue on delivery USD 1,513.4 to
  1,570.1 million; the textbook corrections (the regional mix and the bank-card share) are needed as well, and dropping
  either still leaves no position (USD 1,464.5 to 1,508.8 and 1,469.4 to 1,538.9 million)
One-fact test: "net sales are recognised on delivery, and the December made-to-order orders are still in customer
  deposits at the quarter's end" rescues R4 (1 of 9; R8 stays partly earned); "last year's fourth quarter carried a large
  wholesale contract the card panel cannot see" rescues R5 (1 of 9); each leaves R6, R7 and R9 missed, because the call
  needs both
Not semantics: every field, unit and clause read correctly (the panel's coverage, the descriptor detail, the revenue
  recognition paragraph, the wholesale line, the penetration table, the regional table) leaves the careful estimate at
  USD 1,581.4 million, because no reading says how this quarter's payments turn into its net sales or what the base
  quarter's contract means for the comparison; those are estimated
Not rule application: no filed procedure builds R4 to R9; once the bulletin's coverage and issuer changes and the
  filing's paragraphs are applied, what is left is to estimate the deposits at a quarter end no record holds yet, to set
  wholesale at a run rate, to build the record at each past quarter on what was known then, and to size the range
Estimand: the prompt fixes the quantity (net sales for the fourth quarter of fiscal 2025, the 13 weeks to 31 January
  2026, in USD million, as the company reports them), the range (80 per cent), the record (each past quarter the range
  could have been built for), the steps (each one's worth from the card data to net sales, in points of year-on-year
  growth) and the call rule (short if the whole range sits below the street's figure, long if above, otherwise no
  position); the vendor's bulletin fixes the panel's coverage (general-purpose cards, no private-label cards) and the
  issuer changes; the filing fixes the calendar, revenue on delivery with deposits, the licensed operations, the
  regions, wholesale, the tender split and the penetration and deposits by quarter
No decoy: the desk's third-quarter model (`larkhill_bmh_card_model_q3fy25.xlsx`) reproduces exactly by its own stated
  method from the shipped panel and results (spend per open card on the issuers in both quarters, the brand ids as
  delivered, reported growth regressed on it, intercept 1.62 points, slope 0.483, back-test 2.13 points) and answers a
  shallower quantity; it says nothing about the fourth quarter, its own third-quarter line shows USD 1,355.1 million
  against USD 1,314.9 million reported, and carried forward it files USD 1,562.6 million; Ask 2 and Ask 3 price it on the
  golden's footing
No replay: no result re-derives a published figure; the street's figure is the mean of eleven estimates and is the line,
  not a result; no stated number in the pack is wrong
Pinned: R1 by the delivery history, the descriptor detail and the bulletin's issuer changes (every order of the three
  panel steps inside each step's band); R2 by the filing's regional table (fiscal 2024, fiscal 2023 and fiscal 2024
  rolled forward inside 14.12 to 15.88); R3 by the penetration table and the coverage paragraph (four rules inside 16.60
  to 17.80; holding the third quarter flat ruled out by three successive, growing falls); R4 by the revenue recognition
  paragraph, the deposits by quarter and the descriptor detail (seven-, eight- and nine-week windows inside USD 307.8 to
  326.7 million; the whole quarter ruled out because deposits run near 2.25 weeks of retail payments, about eight weeks of
  a 30 per cent made-to-order share); R5 by the results' wholesale column (the median of eight or of four quarters inside
  USD 16.7 to 19.5 million; a mean that carries last year's one contract ruled out); R6 to R9 by the prompt's range, record
  and call rule with the eleven golden-family routes inside every band (run on the cut pack, `checks.py` R6a to R6f)
Run forecast: R4 dismissed own evidence (the revenue recognition paragraph and the deposits read and left aside, net
  sales taken as payments); R5 method shortcut (one growth rate applied to retail and wholesale together); R6
  self-confirming check (a record that looks sound because no past December held an event this large); R7 and R9
  self-confirming check (a beat, long); R8 unfinished chain (the bridge stopped at customer payments)
Strategy label: Quantitative Finance and Trading 4, "Slow-moving predictors, proven in real time" (validation-heavy): the
  signal proven on what was known at each origin, the textbook pass certified by a record that cannot see this quarter
Depth level: 5: many independent judgments (the entity, the immature weeks, the comparable panel, the regional mix, the
  tender coverage, revenue on delivery with the deposits at a quarter end no record holds, wholesale at its run rate, the
  record built as of each quarter), two of them deep and each necessary for the call; the shortcuts land on twelve
  distinct wrong answers (`effort.py`)
Lesson: what a card panel measures is customers' payments at order on the cards it holds; net sales are recognised on
  delivery, across all tenders and channels; a nowcast that validates on payments-shaped history passes its own record
  until a quarter's orders and deliveries part company. No build on file teaches the stock-and-flow between payments,
  deposits and recognised revenue or the normal-period correction of a contract-swollen base

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the panel's own steps: delivered growth -8.90, the latest weeks completed +1.21, the licensed shops and cafes out -0.57, issuers in both years and cards of the same age +27.74 points (like-for-like growth 19.48%) | assembly and reconciliation | the delivery history; the descriptor detail; the bulletin's issuer changes | delivered -9.20 to -8.60; completion 0.91 to 1.87; licensed -1.04 to -0.27; comparable 27.08 to 28.21 | Right in the careful column; quick: method shortcut, every issuer's delivered spend | independent: the panel, its delivery history and descriptor detail | Ask 3 (panel steps) |
| R2 | card-visible growth at the company's fiscal 2024 regional mix: 15.00% (the panel's own mix gives 19.48%) | modeling | the filing's net sales by region | 14.12 to 15.88 | Right in the careful column (the textbook re-weight); quick: method shortcut, the panel's own mix pooled | R1 | Component 1 |
| R3 | the private-label card's fourth-quarter share carried to 17.00% and net sales per bank-card dollar down 5.07% (customer payments +9.17%) | modeling | the penetration table and tender split; the bulletin's coverage | share 16.60 to 17.80; per bank-card dollar -5.64 to -3.96 | Right in the careful column (the textbook tender adjustment); quick: method shortcut, bank-card spend taken as all of sales | independent: the filing excerpts and the panel's coverage | Component 2 |
| R4 | customer deposits at the quarter's end near USD 318.9 million (USD 210.6 million in October; the made-to-order share of the last eight weeks 38.90% against 29.01%), revenue on delivery worth -7.33 points | missingness and measurement | the revenue recognition paragraph; deposits by quarter; the descriptor detail | deposits 307.8 to 326.7; points -9.75 to -6.45 | dismissed own evidence: reads the revenue recognition paragraph and the deposits column and files customer payments as net sales | R2, R3 | Component 3 |
| R5 | wholesale at its run rate, USD 17.7 million against last year's USD 52.5 million, separating it worth -2.47 points | framing | the results' wholesale column; the filing's wholesale paragraph | run rate 16.7 to 19.5; points -3.41 to -2.17 | method shortcut: one growth rate for retail and wholesale, so last year's contract carries into this quarter | independent: the quarterly results | Component 4 |
| R6 | the record: the chain rebuilt at each of 15 quarters from fiscal 2022 Q1 on what was known then, root mean square error 1.12 points, the third quarter's error +1.04 (13 of 15 inside) | validation | the prompt's record ask; the results; the panel's history | RMSE 0.89 to 1.59; Q3 error 0.38 to 1.69 | self-confirming check: a record of payments-shaped estimates (1.61 points) that looks sound because no past December held an event this large and no past base a contract this large | R4, R5 | Ask 2 |
| R7 | net sales USD 1,439.5 million (-0.63% on USD 1,448.6 million), 80% range USD 1,418.6 to 1,460.3 million | forecasting | the prompt's quantity and range; the record's error | estimate 1,430.4 to 1,455.2; low 1,406.3 to 1,430.1; high 1,453.8 to 1,481.9 | self-confirming check: USD 1,581.4 million with a range from its own record (USD 1,551.5 to 1,611.3 million); dismissed own evidence on the deposits | R4, R5, R6 | Ask 1 |
| R8 | the company steps: the regional mix -4.48, the bank-card share -5.83, revenue on delivery -7.33, wholesale at its run rate -2.47 points | decomposition and attribution | the bridge's order as applied; R2 to R5 | mix -5.36 to -2.96; bank-card share -6.36 to -4.17; delivery -9.75 to -6.45; wholesale -3.41 to -2.17 | unfinished chain: a bridge that stops at customer payments | R2, R3, R4, R5 | Ask 3 (company steps) |
| R9 | short: the top of the range (USD 1,460.3 million) sits USD 23.7 million below the street's USD 1,484.0 million | synthesis | the prompt's call rule; the street's eleven estimates | the call exact; the top 1,453.8 to 1,481.9 | self-confirming check: long, the range wholly above the street | R7 | Recommendation |

Carry-forward: R1, R3 and R5 are graded on inputs of their own (the panel's files, the filing, the results); R2 on the
panel's regional growth; R4 on the payments R2 and R3 give, so a slip at R2 or R3 moves R4's step but not its deposits
band much; R6 to R9 depend on R4 and R5 because the grader compares with the golden's figures, and the call is an AND by
design (either deep step alone leaves the range across the street), so a slip at R4 or R5 costs R6 to R9 and its own step
of R8, and nothing upstream.

## Hidden factor record

The licensed shops under the brand id and the posting lags are Layer 1 (filed processes: the vendor bulletin's matching
by trade name and restatement, the filing's licensed operations), handled at R1 and priced Right; they are not factors a
run has to find.

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| revenue on delivery with the December made-to-order event in deposits | constructed (simulated), the mechanism filed in the revenue recognition paragraph | no: a December to January event in every fiscal year (lifts of 10, 14, 0, 3 and 60 per cent on made-to-order orders) and deposits at every quarter end | the filing's paragraph and deposits column, then the descriptor detail's design-studio and custom-order lines, then modelling | modelling (the deposits at a quarter end no record holds, from last year's by the last eight weeks' payments and made-to-order share) | keep: alone it leaves the range across the street (USD 1,452.6 to 1,497.8 million) |
| wholesale contracts no card carries | constructed, filed in the results' wholesale column and the filing's paragraph | no: contracts in fiscal 2022 Q2, fiscal 2023 Q3 and fiscal 2024 Q4 (8, 10 and 36 above the run rate) | the results file's wholesale column against the panel's coverage | modelling (a run rate from the quarters before, retail and wholesale estimated apart) | keep: alone it leaves the range across the street (USD 1,513.4 to 1,570.1 million) |
| the panel's regional skew, sharpened by KS-06's exit | constructed, through the issuers' footprints; the exit filed in the bulletin | no: every quarter's panel weights; three issuer changes | a group-by of the panel by billing region against the filing's regional table | a re-weight (textbook) | keep: the careful column earns it |
| the private-label card's faster fall in fiscal 2025 | constructed, filed in the 10-Q | no: four quarters of the table | the table against the bulletin's coverage | the tender identity (textbook) | keep: the careful column earns it |
| softer in-stock demand in the holiday quarter | constructed outcome: part of the quantity measured, not a factor to remove | n/a | the panel itself, once deposits and wholesale are handled | none | keep: no step removes it |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the panel's own steps: delivered growth, the latest weeks completed, the licensed shops and cafes out, issuers in both years and cards of the same age | Missed | Right | Right |
| R2 card-visible growth at the company's regional mix | Missed | Right | Right |
| R3 the private-label card's fourth-quarter share and net sales per bank-card dollar | Missed | Right | Right |
| R4 customer deposits at the quarter's end and what revenue on delivery is worth | Missed | Missed | Right |
| R5 wholesale at its run rate and what separating it is worth | Missed | Missed | Right |
| R6 the range's record: rolling-origin error and the third quarter's miss | Missed | Partly | Right |
| R7 the quarter's net sales with its 80 per cent range | Missed | Missed | Right |
| R8 what the regional mix, the bank-card share, revenue on delivery and wholesale are worth | Missed | Partly | Right |
| R9 the call against the street | Partly | Missed | Right |
| Roughly | 0.5 of 9 | 4 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "net sales are recognised on delivery, and the December made-to-order orders are still in customer deposits at the quarter's end"; rescues 1 of 9 results (R4; R8 stays partly earned)
Pair estimate: 46.5 (the careful but hurried pass priced on the judge's own first pass of the previous version: the comparable panel, the regional re-weight and the tender coverage earned, payments filed as net sales and the growth applied to last year's total, USD 1,581.4 million, long); the quick pass scores 14.0

## Data provenance

Source: generated by the seeded generator in task20/generator from a simulated retailer and card panel: the company's
  weekly orders by region and channel (a category trend by fiscal year with softer in-stock demand in the holiday
  quarter, regional trends, the retail calendar's holidays, a rising web share), made-to-order orders (30 per cent of the
  store and site orders, lifted each December and January by a custom event) delivered after eight weeks and the rest
  delivered the week they are bought, customer deposits at each quarter end, wholesale contracts invoiced on delivery,
  Fernhollow consolidated from 2 June 2024, the shop-in-shops and cafes others run under the brand, the tender mix (bank
  cards, the private-label card, other tenders) with the private-label card's fall quickening in fiscal 2025; the panel's
  six issuers with their regional footprints, joins and an exit, card cohorts opened each quarter with back books at each
  issuer's first week, attrition, spend that settles with card age, posting lags and the weekly deliveries; the street's
  estimates; the desk's documents
Behaves like the real thing: the card panels funds buy from bank issuers (Kestrel stands for the type) and a
  home-furnishings retailer of the kind that books revenue on delivery and carries customer deposits for made-to-order
  goods, with the published behaviours of both: a panel skewed to its issuers' footprints, issuer churn, the latest weeks
  restated as late transactions post, merchant matching by descriptor that rolls licensees into the brand, bank-card
  coverage only, deposits that swell with made-to-order promotions, lumpy contract sales, and a 4-5-4 retail calendar
  with a 53rd week
Genuine patterns: (1) seasonality with the retail holidays (Presidents' Day, Memorial Day, the Fourth of July, Labor
  Day, Black Friday and Cyber Monday, the week after Christmas), (2) regional growth from -4% a year in the Northeast to
  13% in the Southeast, (3) the web share rising from 17 to 27 per cent, (4) new accounts spending more and settling over
  about a year, (5) deposits running near 2.2 to 2.3 weeks of retail payments with a seasonal dip at the fiscal year end,
  (6) licensees growing faster than the banner
Problems by process: posting lags (the latest three weeks provisional and restated in each delivery); issuer joins and
  an exit; the vendor's name match rolling the licensees into the brand id; the acquisition part-way through fiscal 2024;
  the 53-week fiscal 2023; the site's payment-facilitator descriptor
Breadth: 10 files (8 used, 2 distractors), 6 issuers, 4 regions, 10 card-open years, 3 merchant ids, 261 weeks, 110,040
  panel rows, 27 deliveries, 49 descriptors, 19 reported quarters, 11 brokers

## Template check

Chain signature: assembly and reconciliation, modeling, modeling, missingness and measurement, framing, validation,
  forecasting, decomposition and attribution, synthesis
Question form: which side of a line (will net sales come in above or below the street), with how much (the estimate and
  its range); the deliverables a spreadsheet and a short note
Nearest build: task18 by chain (assembly, measurement, modeling, decomposition) is a ranked-causes investigation of a
  system's unmetered loss; task5 v4 shares a nowcast of a period not yet complete on a county census; task12 v1 shares a
  re-weight to the target's mix in a banded call; none converts payments to recognised revenue or corrects a
  contract-swollen base

## Frontier check

Precedents: R4 N02, L07 (history assumed informative of the forward window; a measurement change flagged as a risk and
  never tested: the revenue recognition paragraph read, payments kept as sales); R5 L10, L11 (one pooled trend for a mix
  whose parts move in opposite directions; the split built for one step and dropped for the next: the wholesale column
  read, one growth rate applied); R6 L28 (certified the estimator with checks that cannot see the problem); R7 L28, N02;
  R8 L11, N02; R9 L28, N02.
Shallow path checks: the hurried route (the comparable panel at the company's mix with the bank-card share, filed as net
  sales) passes its own rolling record (1.61 points over fifteen quarters, the third quarter of fiscal 2025 within 1.22
  points) and a regression of reported growth on it (2.00 points); the checks of another kind are the deposits at each
  quarter end against the panel's payments (the 10-Q's quarterly column, at the company's grain, against the weekly
  panel) and the descriptor detail's made-to-order share in the quarter's last eight weeks (38.90% against 29.01%), and the
  results file's wholesale column against the panel's coverage (no card carries a contract).
Assumption made false: a run lists "net sales track what customers pay" and "the base quarter is a normal quarter" and
  moves on; the world's process makes both false this quarter (made-to-order orders are paid at order and recognised on
  delivery, and the December event left a third more of them undelivered at the quarter's end; last year's quarter held a
  USD 36 million hotel contract above the run rate), and the pack tests each (the revenue recognition paragraph and the
  deposits column; the wholesale column).
Forcing: the line is the street's USD 1,484.0 million (the mean of eleven estimates; the median 1,482.4 gives the same
  call); the golden family's range tops run USD 1,456.8 to 1,478.9 million, nearest 5.1 below the line; the shortcuts'
  range tops run USD 1,497.8 to 1,633.3 million, nearest 13.8 above; other tenders at 10 and 14 per cent, the last week's
  completeness 3 per cent either way, the licensed share a fifth either way and the range from the record's error
  percentiles keep the top between USD 1,458.5 and 1,464.3 million, all below the line.
Noun swap: the nearest by skeleton.py check is task5 v4 (severity none): its county counts completed by report become
  the panel's immature weeks, and only the nowcast of an incomplete period and the second source at another grain carry
  across; the decision form (act if the interval clears the line here, a set over a threshold there), the deciding
  lessons (stock and flow between payments, deposits and recognised revenue; the normal-period correction of the base),
  the moves and the answer pattern do not; task12 v1 shares the re-weight to the target's mix in a banded call, severity
  none.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | the street's figure | the mean of the eleven estimates / the median / the latest five | the mean, USD 1,484.0 million | same call (all clear every family range) |
| SF2 | net sales | as reported, Fernhollow and wholesale included / organic | as reported; Fernhollow is consolidated in both quarters | the prompt ("net sales ... when the company reports"); the filing's total net sales |
| SF3 | growth basis | weekly averages / quarter totals | weekly averages; both quarters have 13 weeks | same call (identical for the quarter); the filing's 53-week fiscal 2023 for the record |
| SF4 | the comparison quarter | the fourth quarter of fiscal 2024 / the third quarter of fiscal 2025 | the fourth quarter of fiscal 2024, the 13 weeks to 1 February 2025 | the prompt's "year-on-year growth" |
| SF5 | the licensed shops and cafes | kept in the brand id / taken out | taken out by month | the filing: their sales are not net sales |
| SF6 | Fernhollow in the panel before its acquisition | kept / from 2 June 2024 | from 2 June 2024 | the filing's acquisition paragraph; same call for the quarter |
| SF7 | completion factors | medians / means / the last thirteen deliveries | medians over the 27 deliveries | same call (all 1.33%) |
| SF8 | the regional weights | fiscal 2024 / fiscal 2023 / fiscal 2024 rolled forward | the prior fiscal year's retail net sales by region (fiscal 2024) | inside R2's band; same call |
| SF9 | the fourth quarter's private-label share | fiscal 2025's pace / the latest year-on-year change / a straight line / the third quarter's change / held flat / the quarter's own | the pace of fiscal 2025's first three quarters, 17.00% | four rules inside R3's band; held flat ruled out by three successive and growing falls (0.6, 1.0, 1.1 points); the quarter's own share is not known three weeks before the release |
| SF10 | other tenders | the 10-K's 12% held / moved | 12% held | same call at 10% and 14% |
| SF11 | the 80 per cent range | 1.2816 times the record's RMSE / the record's 10th and 90th percentile errors | 1.2816 times the RMSE | same call (top USD 1,464.3 million) |
| SF12 | the call | the prompt's rule | short only if the whole range sits below the street's figure | the prompt |
| SF13 | the record's first quarter | fiscal 2022 Q1 (the first with a year-earlier panel and a prior year's regional mix) / fiscal 2023 Q1 | fiscal 2022 Q1 | inside R6's band; same call |
| SF14 | calibration | the chain as built / reported growth regressed on the chain | as built | the regression lands inside R6 and R7's bands; same call (top USD 1,478.9 million) |
| SF15 | the panel's normalisation | cards of the same age / spend per card | cards of the same age | spend per card keeps the call; ruled out for R1 by its record (1.52 against 1.12 points) |
| SF16 | the issuers | every issuer / issuers in both quarters | issuers in both quarters, KS-01 to KS-05 | the bulletin's issuer changes |
| SF17 | the site's payment-facilitator descriptor | the site / not the site | the site (online orders are net sales) | same call |
| SF18 | the deposit window | eight weeks / seven / nine / the whole quarter | eight weeks (56 days) | seven and nine inside R4's band; the whole quarter ruled out: deposits average about 2.25 weeks of retail payments, eight weeks of a 30 per cent made-to-order share |
| SF19 | wholesale's run rate | the median of eight quarters / of four / the mean of four | the median of the eight quarters before | the median of four inside R5's band; the mean of four carries last year's one contract into the run rate (and still calls short) |
| SF20 | the quarter-end deposits | last year's scaled (golden) / moved as a year earlier / at the third quarter's weeks of payments / from a lead time carried | last year's, scaled by the last eight weeks' payments and made-to-order share | the descriptor detail's made-to-order share (38.90% against 29.01%) rules out the moves that ignore it |
| SF21 | wholesale in net sales | included / excluded | included (the filing's total net sales; the results' column is part of it) | the filing's regional table and totals |

## Closure table

| Axis | Closure |
|---|---|
| 1 | population: Brindle & Moss's net sales as reported, Fernhollow consolidated, wholesale included (SF2, SF21) |
| 2 | outcome: net sales in USD million for the fourth quarter of fiscal 2025 (the prompt) |
| 3 | window: the 13 weeks from 2 November 2025 to 31 January 2026 (the prompt; the results file) |
| 4 | unit: USD million for net sales, points of year-on-year growth for each step; in each asking sentence |
| 5 | comparison: the fourth quarter of fiscal 2024 (SF4), and the street's figure for the call (SF1) |
| 6 | as-of: the panel's delivery of 2 February 2026; the filing's 10-Q of 10 December 2025 |
| 7 | grain: week, issuer, billing region and card-open year in the panel; month and descriptor in the detail; quarter in the results and deposits; fiscal year in the regions |
| 8 | members not yet observed: the quarter's last week as first delivered, completed by each issuer's factor; the quarter-end deposits, estimated (R4) |
| 9 | which delivery: the latest restates the history; the history file gives the first-delivered values |
| 10 | prices: none |
| 11 | rounding: net sales and deposits to USD 0.1 million, growth and steps to 0.01 points, shares to 0.01 per cent; the answer blocks |
| 12 | threshold: the street's figure (SF1) and the call rule (SF12) |
| 13 | tie-break: none needed (the call's margin is USD 23.7 million) |
| 14 | expected value: none; the range is 80 per cent, two-sided |
| 15 | the regional weights: the prior fiscal year's (SF8) |
| 16 | the private-label rule: fiscal 2025's pace (SF9) |
| 17 | other tenders: 12% held (SF10) |
| 18 | the record: rolling origins from fiscal 2022 Q1, each built on what was known then (SF13) |
| 19 | the range: 1.2816 times the record's RMSE (SF11) |
| 20 | revenue on delivery: deposits at the quarter's end from last year's over an eight-week window (SF18, SF20) |
| 21 | wholesale: the median of the eight quarters before (SF19) |
| 22 | the entity and the issuers: the brand id less the licensed shops and cafes, the site, Fernhollow; issuers in both quarters (SF5, SF6, SF16, SF17) |

## Literal reader

The prompt asks for the quarter's net sales in USD million with an 80 per cent range, how that range would have held in
each past quarter it could have been built for, what each step from the card data to net sales is worth in points of
year-on-year growth, and the call by its stated rule; the vendor's bulletin fixes the panel's coverage, the
restatement of the latest weeks with the first-delivered history, the matching by trade name and the issuer changes;
the filing fixes the calendar, revenue on delivery with customer deposits, the licensed operations, the acquisition, the
regions, wholesale, the tender split and the penetration and deposits by quarter. Executed word for word with the
estimates the data force, they give the golden's estimate, range, record, steps and call; no reading of a filed sentence
gives another call.

## Prompt contract

A voice rewrite may not drop or change: the question (above or below the street's figure when the company reports on
26 February); the quarter (the fourth quarter of fiscal 2025, the 13 weeks to 31 January 2026); the opening reason (the
card panel is the only read before then and a sample of cardholders, not the company's books, so the answer is an
estimate); the four asks (net sales in USD million with an 80 per cent range; how the range would have held in each past
quarter it could have been built for; each step's worth from the card data to net sales in points of year-on-year
growth; the call by its rule, short if the whole range sits below the street's figure, long if above, otherwise no
position); the deliverables (a spreadsheet and a short note). It must never add: a rounding instruction, a method or
model, a warning, a file name, a role, the issuer that left, the regions, the private-label card, deposits, delivery,
wholesale, the custom event, the licensed shops, the posting lags, a count of issuers or estimates.

## Pre-ship check

- Stage 4 runs again on the hardened build: the leak reader (the filing, the descriptor detail and the prompt changed)
  and the determinism judge with its isolated first pass, priced against the careful column before READY.

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
- 2026-11-11, architecture 2 at stage 4 (the regional mix and the private-label card's faster fall as the two deep steps, the KS-06 exit, the demand turn in the holiday quarter): the determinism judge's isolated first pass, written before it opened the answer blocks, re-weighted the comparable panel to the 10-K's regions (step -4.1 points) and carried the private-label share (16.9) with the panel's coverage, landing the estimate inside its band (about USD 1,425 million); it lost only the record (a fitted regression, 1.15 to 1.5 points), the top of the range and a committed call. Priced on that pass the careful column reads about 72, so the chain went back to stage 2: in this field both corrections are the textbook moves a medium-effort run makes unprompted.
- 2026-11-11, hardening, lead times: a 2021 backlog and its 2022 unwind put misses of up to 11 points in every carried deposit rule's record (RMSE 4.1); a lengthening spread through fiscal 2025 showed in reported growth's slide from 3.9 to 1.5 per cent, so a trend extrapolation found the answer; a one-time lengthening early in fiscal 2025 left the quarter at +3.1 to +3.3 per cent, at the street; a backlog delivered in the base quarter put a 4.6-point unforeseeable miss in the record. Lead times now stay at eight weeks throughout.
- 2026-11-11, hardening, deposits alone (the December made-to-order event in deposits, everything else as before): one sentence about the deposits would have rescued R4 to R9 for a careful pass that already makes the textbook moves (one thing); wholesale contracts, invoiced and never on a card, were added as the second, independent deep step, so the call needs both.
