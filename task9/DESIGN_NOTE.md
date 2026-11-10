# task9: how large a 3-month variance-swap ladder the Carrow Fields sleeve can add for 2027 (architecture 8)

## Draw

Subdomain: Quantitative Finance (Quantitative Finance and Trading)
Analysis type: Forecasting & Predictive Modeling (assigned), task type volatility-derivatives-pricing (the client's
  derivative pricing, market data and curve validation, and counterparty exposure types).
Answer shape: a schedule under capacity (the largest size of a new ladder that the two limits leave room for, and
  the 2027 plan at that size with its range).
Weight: allocation under constraints (the room two limits leave beside a standing ladder, taken off a record day
  by day); none of the last three builds on file sat there.
Data-native sentence: the policy measures both limits on the record since January 2007, the Cboe download of the
  3-month index begins on 18 September 2009, on the days that set the limits that index sits below the 30-day index
  it sits above in calm markets, and swaps sold a month apart share most of their days, so the ladder's 2008 has to
  be rebuilt from both neighbours and every average and range has to keep neighbouring sales together.
People: Stephanie Bowman (director of treasury), Edward Stewart (chief investment officer), Gloria Wilkins
  (investment operations), from guard.py names --geo US --seed 908.

1. World: the Carrow Fields Foundation's volatility-premium sleeve has sold one 12-month S&P 500 variance swap
   every month since July 2021 (USD 50,000 a point, two confirmations a month with three dealers) and wants to add
   a 3-month ladder from the January 2027 sale; the dealers' term sheet also quotes six months.
2. Data: public market records used as is (the Cboe index history downloads for the S&P 500, the 9-day, 30-day,
   3-month, 6-month and 1-year volatility indices, the VVIX and SKEW, pulled 2026-11-10 with closes to 2026-11-09).
   The sleeve's swaps, statements and policy are authored paperwork and carry no pattern of their own. The 3-month
   index's earlier closes (4 December 2007 on) are public on FRED and are held beside the generator as a
   cross-check, outside the pack.
3. Decision: one committed quantity, the largest vega per monthly 3-month sale that keeps the whole sleeve inside a
   settlement limit of 2.0 per cent of USD 1,487.6m (29.752m in a calendar year) and a collateral limit of 3.0 per
   cent (44.628m on any day) on the record, with the sleeve's 2027 cash plan at that size and its 80 per cent range.
   Forward facing: the ladder launches on 19 January 2027 and the size goes to the dealers first.
4. Results: eleven, across six areas (missingness and measurement, validation, modeling, synthesis, uncertainty,
   forecasting).
5. Where a hurried analysis goes: the missing strikes stood in for by a regression on the 30-day index, which fits
   the whole overlap (USD 124,500 a point), the ladder run only from its index's first date (136,600), each swap
   valued at its own index (144,400), the new ladder sized on its own (184,100), no cap in the valuation (38,900),
   the open swaps planned at their value (USD 1.883m against 2.494m), a forecast made in volatility and squared
   (3.015m), each average's range from settlements resampled one at a time (228,000 to 400,000 against 63,000 to
   552,000), and the standing ladder's two sales still to come left out of the plan.
6. Golden: USD 114,400 a point, bound by the collateral limit on 20 November 2008; a 6-month ladder instead would
   fit at 58,700; a 2027 plan of USD 5.728m (2.809m from the 12-month ladder, its November and December 2026 sales
   included, and 2.919m from nine 3-month settlements), four times in five between a net payment of 4.203m and
   receipts of 12.204m.
7. Card: shape 04, gap population then time, generators G12, G14, G13, Gate G forecasting, calibration form the
   dealers' statements, context artifact the month-end close-out, forum the treasury and investment office
   themselves (schedule D.8), forcing event the ladder's launch, organisation a foundation, role finance and
   treasury.
8. Guard: WARN only. repeat.deliverables (a memo, a workbook and a CSV, as task14): kept, because the third file is
   the sleeve's collateral for every day of the record, which is what a risk reviewer checks the size against, and
   the two-file set stood at 33 per cent of the prompts on file. repeat.gate_g (forecasting, as task10): the
   assigned analysis type is forecasting and the call is next year's ladder and plan, so the label is the honest
   one. test.same_puzzle_older against mark196 is differentiated on the card (a capture-recapture count; nothing
   here is counted or matched). The forum (committee, against task14), the forcing event (contract, against task3),
   the question form and one persona's first name were redrawn at the check.
9. Lineage: architectures 1 to 7 are spent (the card's lineage holds each fate); architecture 7's results chain died
   at stage 4 on Gate H with two built-in strands, which is why this draw constructs no market pattern at all.
10. Honest limit of the paper: the careful column prices three moves as lost (a one-index stand-in kept on a
    whole-overlap check, the value read as the expectation, settlements resampled one at a time). Each is a move a
    strong run makes some of the time, so the pair estimate below is a model and the platform's two runs are the
    measurement.

## Deep reasoning

Task type: volatility-derivatives-pricing, serving forecasting: variance swaps struck off an implied term structure,
  marked at accrued plus implied variance, their settlement forecast for the coming year.
Domain test: every result is a quantity the field prices or forecasts: a strike read off the implied term
  structure and rebuilt where the index is not published, realised variance accrued from closes, a seasoned swap's
  mark (accrued plus implied variance for its remaining term, under a cap), the exposure a dealer would call
  collateral on, the expected settlement of open swaps as distinct from their mark, and inference on overlapping
  settlements (the client's own depth line for this field: correcting inference for overlapping returns).
Swap: with hospital beds for swaps there is no strike, no accrued variance, no term structure that inverts in a
  crisis, no overlap between one month's sale and the next, and no difference between what a position is marked at
  and what it is expected to pay; the question stops making sense at the first result.
Where the weight sits: R4, the room on the binding day. It needs every 3-month swap sold from January 2007 struck
  (32 sale dates before its index file begins), both ladders' open swaps marked on each of 4,995 days at the
  variance implied for each swap's own remaining term under the cap, and the standing ladder's own use of the limit
  taken off day by day; the work is long, not clever.
Layer 1: eight index histories as Cboe publishes them (month/day/year dates, five files with open, high, low and
  close and three with a single column, each starting in a different year, index days with no S&P 500 close); a
  blotter with a confirmation first booked at ten times its size and a novation that leaves a superseded row, both
  on swaps that have since expired; one dealer quoting variance units and a variance strike; a valuation feed in
  three date formats with a re-sent day and three missing dealer days; statements struck ten days before the review
  date; an exchange holiday that moves a 2027 expiry. Each comes from how dealers, a custodian and an exchange keep
  records, and none decides a result.
Not one thing: the strongest single piece is rebuilding the 3-month strikes for 2007 to 2009 from both neighbours.
  A run that nails it still has to mark seasoned swaps at their remaining terms under the cap through two crises
  (R3, R5), take the standing ladder's use of each limit off day by day (R4), tell an expected settlement from a
  mark (R8), keep neighbouring sales together when it ranges an average (R6, R7), count the standing ladder's two
  sales still to come and the nine new settlements that fall in the year, and range all 21 settlements jointly
  (R10). The recommendation needs all three priced moves at once.
One-fact test: the most useful single sentence is "on the days that set the limit the 3-month index sits below the
  30-day index, so the missing strikes have to come from the maturities on both sides of three months"; it rescues
  R1, R2 and R4, 3 of 11. "An open swap's value is a price: expect what such swaps went on to pay on the record"
  rescues R8, 1 of 11. "Keep neighbouring sales together when the record is resampled and run the swaps not yet
  sold off the same start dates as the open ones" rescues R6, 1 of 11. Two moves at once (printed by checks.py as
  information): the rebuild and the expectation 4 of 11, the rebuild and dependence 5 of 11, the expectation and
  dependence 2 of 11; only all three rescue the plan and the recommendation (8 of 11). All are method choices on
  public data used as is; nothing is hidden or built in.
Not semantics: every field, unit and clause read correctly (vega against variance units, the cap, the sale and
  expiry rules, the year a settlement falls in, the sleeve-wide collateral measure, the record's sale dates) still
  leaves the 3-month ladder without strikes for 32 sale dates, leaves the mark where it is and leaves the
  settlements overlapping; no reading supplies a strike, an expectation or a range.
Not rule application: schedule D files what is measured (the record and its sale dates, the limits, the sleeve-wide
  collateral, the plan's basis, which ranges are reported) and the confirmation files the payoff; no document says
  how a strike is found where its index is not published, how a seasoned swap is valued, what an open swap is
  expected to pay or how a range is taken. After every filed rule is applied those four remain to judge.
Estimand: schedule D.2 and D.3 (sale date, expiry, strike index, cap, sizes in multiples of USD 100), D.4 (the two
  limits and Reference Assets), D.5 (the record from January 2007 to the review date, every ladder at its size on
  every sale date whether or not its index was yet published, settlement in the year of expiry, collateral the
  sleeve-wide negative value at the close on the dealers' valuation basis, no discounting), D.7 (the plan: every
  ladder's swaps that expire in the plan year, open swaps at the settlement amounts they are expected to pay as
  estimated at the review date, unsold swaps at their ladder's average settlement per sale over the swaps that
  would have expired by the review date, experience from the whole record, an average reported with the range the
  average itself lies in four times in five, the plan with the range of the year's settlements), D.8 (the review
  date); the master confirmation (realised volatility, the cap, the settlement amount); the credit support annex
  summary (exposure never more than the capped settlement).
No decoy: nothing in the pack argues for a size or a plan: the term sheet states the size the investment office
  asked the dealers to quote (USD 200,000) and no file tests it; the statements carry valuations and say so.
No replay: no result re-derives a published figure. The Cboe indices are inputs; the ladders, their marks and the
  sleeve's room exist nowhere outside this pack.
Pinned: analysis.py runs each result's rivals on the record. The 3-month ladder under six two-sided rebuilds
  (regression on both neighbours in levels and logs, on the 30-day and 1-year pair, total variance, linear, and the
  index's published earlier closes): 2.821 to 2.861 a sale and 156.5 to 163.9 for 2008. The 12-month peak under
  six readings of the term structure, 25.84m to 26.49m. The 3-month size under 26 rebuild-by-marks combinations,
  100,000 to 116,900, every one binding on the collateral limit on 20 November 2008; the 6-month size 54,100 to
  58,800. Each average's range under nine ways of keeping neighbouring sales together (four block lengths, three
  lag choices, calendar-year averages, a count of only the swaps that do not overlap). The expectation under ten estimators from the whole record, 2.394m to
  2.888m. The plan's range under seven joint replays. Every hurried figure sits outside its band by a margin
  checks.py asserts.
Run forecast: R1, R2 and R4 lost to a self-confirming check (a regression on the 30-day index validated on the
  whole overlap, where calm days outvote the stressed ones); R8 to a method shortcut (the value read as the
  expectation, or a forecast made in volatility and squared); R6 and R7 to a method shortcut (settlements resampled
  one at a time, dependence named as a caveat); R10 and R11 to an unfinished chain (all three, plus the standing
  ladder's two sales still to come); R3 and R5 at risk of a method shortcut (each swap valued at its own index, or
  the cap left out of the valuation). Calibration: each priced loss is a move a strong run makes some of the time.
Strategy label: WORKS IN FORM (a forecast that has to earn its place, its invariant rebuilt from a record; F7
  population in its legal form, a frame the published series leaves out rebuilt from histories and checked where it
  can be; inference corrected for overlapping observations; public market data used as is).
Depth level: 5 by structure, 4 by the careful column. Seven judgments each move a graded figure on their own (a
  rebuild that holds in stress, the remaining-term mark, the cap in the mark, the standing ladder's use of the
  limit, the expectation against the mark, dependence between neighbouring sales, the plan's population), and the
  shortcuts land on different sizes and plans (124,500 and 5.562m, 136,600 and 7.298m, 144,400 and 6.494m, 184,100
  and 7.507m, 114,400 and 5.117m, 114,400 and 6.249m); the careful column prices three of the seven as lost.
Lesson: a limit measured on a record is only as long as the shortest series behind it, and the relation used to
  lengthen that series has to be checked on the days that set the limit, where the average relation reverses; a
  mark is a price, which the record shows to sit at the one-in-five low of what such swaps go on to pay; and 226
  monthly settlements of 12-month swaps are closer to nineteen observations than to 226. No build on file rebuilds
  a traded index from its neighbours, separates a derivative's mark from its expected settlement or ranges an
  average of overlapping settlements.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the 3-month ladder's average settlement per sale on the record, USD 284,000 per USD 100,000 a point | missingness and measurement | schedule D.5(b): every monthly sale date from January 2007 counts whether or not the index was yet published; the 32 strikes before 18 September 2009 rebuilt from the 30-day and the 6-month or 1-year index | 282,000 to 287,000 | self-confirming check: stands the 30-day index in for the missing strikes by a regression that explains 0.94 of the 3-month index over the 4,312 days both are published (300,000) | independent: the index and price histories | Ask 2 |
| R2 | the 3-month ladder's worst calendar year on the record, 2008 at a net USD 16,154,000 paid per USD 100,000 a point | validation | the same strikes, checked on the 102 overlap days the 30-day index closed above 35 (fit off by 1.35 points there; the one-index stand-in 2.3 points high) | 15,650,000 to 16,390,000 | self-confirming check: the stand-in's strikes are too high where the limit is set, so 2008 comes out milder (14,125,000) | independent: the index and price histories | Component 4 (Ask 2) |
| R3 | the 12-month ladder's peak collateral on the record at its USD 50,000 a point, USD 25,876,000 (18 March 2020, with 20 November 2008 within 3 per cent) | modeling | schedule D.5(d): the open swaps valued together each day on the dealers' basis; the annex's cap on exposure | 25,800,000 to 26,500,000 | method shortcut: values each swap at the 1-year index (21,774,000), leaves the cap out of the valuation (30,067,000), or takes the worst calendar year of settlements (11,415,000) | independent: the index and price histories | Ask 4 |
| R4 | the largest 3-month size inside both limits, USD 114,400 a point, bound by the collateral limit on 20 November 2008 | synthesis | schedule D.4 and D.5 (every ladder at its size, both limits, sizes in multiples of USD 100) on R2's strikes and R3's valuation | 100,000 to 117,000 | unfinished chain: sizes the ladder on the stand-in's strikes (124,500), on the years its index file covers (136,600), on its own without the standing ladder (184,100), or at each swap's own index (144,400) | R2, R3 | Component 1 |
| R5 | the largest 6-month size instead, USD 58,700 a point, bound by the collateral limit on 20 November 2008 | modeling | the same schedule; the 6-month index is published from 2 January 2008 and the twelve strikes rebuilt before it move nothing | 54,000 to 59,000 | method shortcut: each swap valued at its own index (72,600) or the cap left out (28,200) | R3 | Ask 1 |
| R6 | the 80 per cent range of the 12-month ladder's average settlement per sale (USD 315,000 per USD 100,000 a point): 63,000 to 552,000 | uncertainty | schedule D.7(d): the range the average itself lies in; 226 settlements of swaps that share eleven of their twelve months with the next sale (correlation 0.93), resampled in blocks of consecutive sales | low end 14,000 to 82,000; high end 537,000 to 616,000 | method shortcut: resamples the settlements one at a time and names serial dependence as a caveat (228,000 to 400,000), or allows for five lags where neighbouring swaps share eleven months (123,000 to 507,000) | independent: the 12-month ladder's settlements, which need no rebuilt strike | Ask 3 (12-month) |
| R7 | the same range for the 3-month ladder's average: 143,000 to 413,000 | uncertainty | schedule D.7(d) on R1's settlements (correlation 0.64 between one sale and the next) | low end 131,000 to 159,000; high end 399,000 to 436,000 | method shortcut: resamples the settlements one at a time (194,000 to 370,000; 215,000 to 383,000 on the stand-in's strikes) | R1 | Ask 3 (3-month) |
| R8 | what the open swaps that expire in 2027 should be expected to settle at, USD 2,494,000 | forecasting | schedule D.7(a) and (c): expected settlement as estimated at the review date, experience from the whole record; realised variance against implied for each swap's remaining term from every start date since January 2007 | 2,390,000 to 2,890,000 | method shortcut: reads the expectation off the swaps' value (1,883,000), forecasts volatility and squares it (3,015,000), or takes the typical start date (3,545,000) | independent: the open swaps and the record's start dates | Component 2 (Ask 5) |
| R9 | the 80 per cent range of R8's total, USD 394,000 to 4,247,000 | uncertainty | the same start dates applied to all ten sale months at once | low end 200,000 to 420,000; high end 4,100,000 to 4,430,000 | method shortcut: draws the swaps independently (990,000 to 3,636,000); priced as earned, because strong runs replay fits jointly unprompted | independent: the start dates' replay, graded on its own ends | Ask 5 (range) |
| R10 | the 2027 plan at that size by ladder: the 12-month ladder USD 2,809,000 (the open swaps and its November and December 2026 sales, still to come, at the ladder's average), the 3-month ladder 2,919,000 (nine settlements), the sleeve 5,728,000, four times in five between minus 4,203,000 and 12,204,000 | forecasting | schedule D.7 (every ladder's swaps that expire in the plan year, open or not yet sold) and D.7(e); all 21 settlements replayed from the same 4,717 start dates | 12-month 2,705,000 to 3,205,000; 3-month 2,530,000 to 3,030,000; sleeve 5,235,000 to 6,235,000; low end minus 4,300,000 to minus 1,900,000; high end 11,200,000 to 12,400,000 | unfinished chain: plans the open swaps at their value and the new ladder on the stand-in's size and average (2,198,000 and 3,364,000), draws the swaps not yet sold one at a time (minus 447,000 to 11,027,000), or leaves the standing ladder's two coming sales out (2,494,000) | R1, R4, R8 | Component 3 (Ask 6) |
| R11 | the recommendation: add the 3-month ladder at no more than USD 114,400 a point, not the 200,000 quoted for, and carry USD 5,728,000 in the 2027 cash plan with its range of minus 4,203,000 to 12,204,000 | synthesis | R4 and R10 | the size in R4's band, the plan and its range in R10's | unfinished chain: a size from the stand-in's strikes and a plan from the marks (124,500 and 5,562,000, with a range that misses both ends) | R4, R10 | Recommendation |

Carry-forward: R1, R2, R3, R6, R8 and R9 stand on inputs of their own (the index histories, the 12-month ladder's
settlements, the open swaps). R4 falls with R2 or R3; R5 with R3 only (the 6-month index's late start moves
nothing, so a run that mishandles the 3-month strikes still earns R5); R7 with R1; R10 with R1, R4 or R8; R11 with
R4 or R10. A slip on the rebuild costs R1, R2, R4, R7, R10 and R11 and leaves R3, R5, R6, R8 and R9; a slip on the
expectation costs R8, R10 and R11; a slip on dependence costs R6, R7, R10 and R11.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| the Cboe download of the 3-month index begins on 18 September 2009 (the 6-month on 2 January 2008, the 9-day on 4 January 2011); the index's earlier closes from 4 December 2007 are public on FRED and are not in the foundation's folder | real (public data, used as is) | no: it shows on loading the file, and the 6-month and 9-day gaps sit beside it and decide nothing | one look at the file's first row | modelling: a strike series rebuilt from two neighbours and checked on the overlap; the public earlier closes land inside every band | keep |
| the 3-month index stands 12.5 per cent above the 30-day index on average and 7.9 per cent below it on the 102 overlap days the 30-day index closed above 35 | real (public data, used as is) | no: it runs through every stressed stretch of the overlap (2010, 2011, 2015, 2018, 2020 and later) | a targeted query on the overlap's stressed days | modelling: the rebuild has to use both neighbours | keep |
| realised variance has run below implied variance on the record (0.83 of it over one month, 0.67 over twelve), with a long left tail in what swaps pay | real (public data, used as is) | no: every start date since 2007 and every horizon | modelling: realised against implied by remaining term | modelling: an expectation and a joint range | keep |
| settlements of swaps sold a month apart are tied (correlation 0.93 between one 12-month sale and the next, 0.64 for 3-month sales) | real (a property of any monthly ladder on any record) | no: every pair of neighbouring sales in both ladders | a lag-one correlation of the settlements | modelling: an average's range and a plan's range that keep neighbouring sales together | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the 3-month ladder's average settlement per sale | Missed | Missed | Right |
| R2 the 3-month ladder's worst calendar year | Missed | Missed | Right |
| R3 the 12-month ladder's peak collateral | Missed | Right | Right |
| R4 the largest 3-month size | Missed | Missed | Right |
| R5 the largest 6-month size | Missed | Right | Right |
| R6 the range of the 12-month ladder's average | Missed | Missed | Right |
| R7 the range of the 3-month ladder's average | Missed | Missed | Right |
| R8 the open swaps' expected settlement | Missed | Missed | Right |
| R9 the open swaps' 80 per cent range | Missed | Right | Right |
| R10 the 2027 plan by ladder with its range | Missed | Missed | Right |
| R11 the recommendation | Missed | Missed | Right |
| Roughly | 0 of 11 | 3 of 11 | 11 of 11 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "on the days that set the limit the 3-month index sits below the 30-day index, so the missing strikes have to come from the maturities on both sides of three months"; rescues 3 of 11 results
Pair estimate: 34.5 (the careful but hurried pass: instruction-following 7 and Asks 1, 4 and the open swaps' range of six)

The careful column is priced up wherever strong runs make the move unprompted: every filed rule (the record's sale
dates, both limits with the standing ladder beside the new one, the cap, the year of expiry, the schedule's basis
for swaps not yet sold, the standing ladder's two coming sales), swaps valued on their remaining term, a stand-in
checked on the overlap, and the open swaps replayed jointly for their range. It is priced as lost on three moves
from the run record's list of what strong runs skip: a check that confirms itself (a one-index stand-in validated on
the whole overlap), a risk-neutral figure taken where a real-world one is asked, and observations resampled one at a
time with dependence left as a caveat. None is certain: a run that rebuilds from both neighbours earns R1, R2 and
R4 (about 56), one that also forecasts from realised against implied earns R8 (about 62), and the plan and the
recommendation need all three. Two moves at once rescue 4, 5 and 2 of 11 (checks.py prints them as information).

## Data provenance

Source: public, the Cboe Global Markets index history downloads (https://cdn.cboe.com/api/global/us_indices/daily_prices/
  SPX, VIX, VIX9D, VIX3M, VIX6M, VIX1Y, VVIX and SKEW _History.csv), pulled 2026-11-10 with closes to 2026-11-09;
  the exchange's holiday schedule for 2026 to 2028 as NYSE publishes it. The sleeve's swaps, the dealers'
  statements, the custodian's ledger and the foundation's policy are authored positions and paperwork.
Behaves like the real thing: every market value is the published close; the authored book is two confirmations a
  month struck at the published 1-year index, valued, collateralised and settled by the confirmation's own formula
  on those closes, so its history is what such a sleeve would have recorded.
Genuine patterns: (1) volatility clusters, with 2008 and 2020 the two episodes that set every limit; (2) the term
  structure slopes up in calm markets and inverts in stress; (3) implied variance exceeds realised variance on
  average, more at long horizons, with a long left tail in what a seller is paid; (4) each index file starts in its
  own year, and index days exist with no S&P 500 close; (5) a monthly ladder's settlements overlap, so they are
  serially tied.
Problems by process: the late-starting index files are Cboe's download history; the amended and novated
  confirmations, the variance-unit statement, the three date formats, the re-sent and missing valuation files and
  the month-end statement date are what a blotter, three dealers and a custodian produce; the moved expiry is the
  exchange's observed holiday.
License: Cboe index data are published by Cboe Global Markets for public download; the values are facts reproduced
  unaltered for this analytical task with the source and pull date recorded in metadata.json. The S&P 500 is a
  product of S&P Dow Jones Indices, whose closing levels Cboe republishes in the same download.
Used as is: the eight index files ship byte for byte as downloaded (raw/manifest.json holds each file's URL, pull
  date and sha256). Nothing is altered, filled, filtered or reordered.
Cross-check: FRED series VXVCLS (the same 3-month index, published from 4 December 2007; raw_check/ holds the pull
  and its sha256) equals the Cboe download on all 4,311 days both carry. It is not shipped and no golden figure
  reads it. analysis.py runs it as a rival: on the published earlier closes the 3-month ladder averages USD 286,000
  a sale with 2008 at 16,166,000 and sizes at 100,300 to 112,600, all inside the bands, and the golden's rebuilt
  strikes sit 0.53 points from the published closes on average over the 21 sale dates the two can be compared
  (20 October 2008: published 43.62, rebuilt 45.54, the one-index stand-in 50.25).
Breadth: 21 files; eight index histories of 4,000 to 13,000 rows; 4,995 record days on which up to fifteen open
  swaps are valued; 128 confirmations with 28,812 daily valuation rows; three candidate maturities; the binding day
  has to be found among two crises and the room taken off day by day; 21 settlements fall in the plan year.
Leak review: leak.py --asof 2026-11-10 returns REVIEW with no LEAK. (1) "ladder" in schedule D and the term sheet
  is the program's own word, defined in D.2(a) and declared as a field term. (2) The same two documents carry the
  words of the committed call (3-month, ladder, a point, monthly sale) because they are the program's vocabulary;
  neither carries a size but the 200,000 the dealers quoted for, a stated input. (3) Six ordinary words of this note
  (review, closed, published, November, schedule, carries) appear in schedule D; "published" sits in D.5's two
  population sentences, which file what the record is and say nothing of how a strike is found. (4) The blotter's
  and the exchange calendar's dates after the as-of date are the open swaps' expirations and the published holiday
  schedule, forward-looking records the plan year needs. Single-use test: D.5(b)'s second sentence, D.7's lead and
  D.7(d) and (e) each file a population or a quantity the decision cannot be read without (delete any one and a
  second literal answer opens); none names a method.

## Template check

Chain signature: missingness-measurement, validation, modeling, synthesis, modeling, uncertainty, uncertainty,
  forecasting, uncertainty, forecasting, synthesis
Question form: what (the largest size, with the limit and day that bind)
Nearest build: task4 (allocation-sensitivity, measurement) and task14 (bridge, assembly); neither sizes a position
  against limits measured on a record, rebuilds a published series from its neighbours, forecasts a derivative's
  settlement or ranges an average of overlapping observations, and no build on file shares this chain of areas or a
  schedule under capacity.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "sale" date of a month | the third Friday; the first business day after it | the first exchange business day after the third Friday | schedule D.2(b); every blotter trade date |
| SF2 | expiry | the third Friday; the business day before when the exchange is shut | the preceding exchange business day (17 June 2027 for the March sale) | schedule D.2(c) with the exchange's holiday file |
| SF3 | the strike | the index close on the sale date; the day before; another maturity's index | the closing level on the sale date of the Cboe index for the swap's maturity | schedule D.3; every blotter strike equals the 1-year index close of its trade date |
| SF4 | realised volatility | 252 over the days observed with no mean taken; a sample standard deviation; calendar days | the confirmation's formula: 100 times the root of 252 over N times the sum of squared log returns | the master confirmation, section 3; the 104 settled confirmations reproduce |
| SF5 | observation days | S&P 500 publishing days; days the volatility index files carry | days the S&P 500 publishes a close | the master confirmation, section 2; the index-only days carry no close to observe |
| SF6 | the cap | on settlement only; also on the valuation | realised volatility capped at 2.5 times the strike at settlement, and exposure never above the capped settlement | schedule D.3; the master confirmation, section 4; the annex summary, exposure |
| SF7 | the year a settlement falls in | the expiry's year; the payment date's; the sale's | the calendar year of expiry | schedule D.5(c) |
| SF8 | the record | from January 2007; from each index's first date; the sleeve's own years | sale dates from January 2007 through the review date, closes to 9 November 2026 | schedule D.5(a) and (b), D.8 |
| SF9 | the sleeve in the test | the new ladder alone; the new ladder with the 12-month ladder at USD 50,000 | every ladder of the sleeve at its size | schedule D.5(b); the blotter (two confirmations of 25,000 a month) |
| SF10 | collateral on a day | per dealer; per swap; the sleeve's open swaps together | the amount by which the open swaps together are valued against the sleeve | schedule D.5(d) |
| SF11 | the valuation basis | the swap's own maturity index; the 30-day index; implied variance for the remaining term | accrued variance plus implied variance for the remaining term, weighted by days | schedule D.5(d) (the dealers' basis); the valuation file's implied-to-expiry column, which differs swap by swap and reproduces every value to the dollar |
| SF12 | reading the term structure between published terms | total variance; linear in volatility; the nearest term; with or without the 9-day index | total variance between the two nearest published terms | same call: R3, R4 and R5 stay inside their bands under each (analysis.py rivals) |
| SF13 | a strike where the index is not published | rebuilt from both neighbours (regression, total variance, linear, logs); from the 30-day index alone | rebuilt from both neighbours | same call across the two-sided rebuilds; the one-sided stand-ins are 2.3 to 9.3 points high on the overlap's 102 stressed days (named data) and land outside the bands |
| SF14 | the terms used to value swaps before an index is published | the terms published that day; rebuilt terms added | the terms published that day | same call: rebuilt terms move R4 to 110,300 and R5 to 57,000, inside both bands |
| SF15 | the limits in dollars | 2.0 and 3.0 per cent of USD 1,487.6m; of another balance | 29,752,000 and 44,628,000 | schedule D.4(c); the audited statement of net assets at 30 June 2026 |
| SF16 | "largest size" | rounded to the nearest 100; the largest multiple of 100 inside the limits | the largest multiple of USD 100 | schedule D.2(a); 114,400 either way for the 3-month ladder, 58,700 against 58,800 for the 6-month, both in band |
| SF17 | average settlement per sale | over swaps expired by the review date; including open swaps at their marks | the swaps that would have expired by the review date (235) | schedule D.7(b) |
| SF18 | worst calendar year | full years only; part years counted | every calendar year of the record | same call: 2008 under either |
| SF19 | "expected to settle at" | the mark; an expectation on the record's experience | the expectation as estimated at the review date | schedule D.7(a) and (c); the mark sits below what the same swaps went on to pay from 80 per cent of the record's start dates (named data) |
| SF20 | the experience behind the expectation | the whole record; the sleeve's own years; years before the record | the whole record | schedule D.7(c) and D.5(a) |
| SF21 | "expected" | the mean; the median; a volatility forecast squared | the mean of the settlement | the word; the settlement amount is linear in variance (the confirmation, section 4), and the median (3,545,000) is the typical start date |
| SF22 | the open swaps that expire in 2027 | expiry dates in 2027; all open swaps | the ten sale months January to October 2026 | the blotter's expiry dates; schedule D.7 (the year of expiry) |
| SF23 | the new ladder's 2027 settlements | twelve; the nine whose expiry falls in 2027 | nine (sales 19 January to 20 September) | schedule D.7 (the year of expiry); the exchange calendar |
| SF24 | the open swaps' 80 per cent range | 10th to 90th percentile of the total; of each swap | the 10th and 90th percentiles of the ten sale months' total | the asking sentence; same call with each swap's own percentile added |
| SF25 | the review date | 30 October (the statements); 9 November | the 9 November close | schedule D.8 (the second Monday of November) |
| SF26 | size of the standing ladder | 25,000; 50,000; 250,000 | USD 50,000 a point per monthly sale | the blotter's live rows (two confirmations of 25,000 for each trade date) |
| SF27 | units on one dealer's lines | vega and volatility; variance units and variance | converted by the confirmation's definition (variance units are vega over twice the strike) | the master confirmation, section 1 |
| SF28 | discounting | none; at a money-market rate | none | schedule D.5(e) |
| SF29 | the dealers' own implied volatilities | used for the record; the published term structure | the published term structure (the dealers' figures exist only from July 2021) | schedule D.5(a) |
| SF30 | a sale date whose strike index was not yet published | left out of the record; kept | kept | schedule D.5(b), second sentence |
| SF31 | "80% range of the average" | the range single settlements fall in; the range the average itself lies in | the average's own range | schedule D.7(d) |
| SF32 | the swaps in the plan | the open swaps and the new ladder; every ladder's swaps that expire in the year, sold or not | every ladder's, so the standing ladder's November and December 2026 sales count | schedule D.7 (lead and (b)); the term sheet (the 12-month ladder continues) |
| SF33 | the plan's range | each ladder's range; the year's settlements together | the year's settlements together, receipts net of payments | schedule D.7(e) |
| SF34 | the unit of the averages and their ranges | per USD 100,000 a point; at each ladder's size | per USD 100,000 a point | the asking sentence |
| SF35 | the 3-month index's published earlier closes (public, not in the folder) | brought in; not brought in | either | same call: with them R1 is 286,000, R2 16,166,000 and R4 100,300 to 112,600, inside the bands |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | the record's sale dates from January 2007, published index or not (D.5(b), SF30); open swaps by expiry year (D.7); every ladder's unsold swaps by expiry year (D.7(b), SF32): filed, SF8, SF22, SF23 |
| 2 Unit of account | US dollars a volatility point per monthly sale (D.2(a)); record figures per USD 100,000 a point (SF34); one dealer's variance units converted by definition (SF27) |
| 3 Attribution window | a settlement falls in the calendar year of expiry (D.5(c)); no expiry sits on a year boundary |
| 4 As-of dating | closes through the review date, 9 November 2026 (D.8); statements are at 30 October and are not the value date (SF25) |
| 5 Version basis | the blotter's live rows (status column); the index files as pulled; the public earlier closes are a same-call rival (SF35) |
| 6 Denominator | per sale, over the swaps expired by the review date (D.7(b), SF17); realised variance over N observation days (SF4) |
| 7 Weighting | a ladder's swaps carry equal vega (D.2(a)); the mark weights accrued and implied variance by days (SF11) |
| 8 Window length | the whole record for limits and for experience (D.5, D.7(c)); no shorter window is licensed (SF8, SF20) |
| 9 Boundary inclusivity | observation days after the trade date to and including expiry (confirmation section 2); valuation days after the sale and before expiry |
| 10 Rounding path | figures computed unrounded and rounded once for print; the plan is the sum of its stated parts; sizes floored to multiples of USD 100 (D.2(a), SF16) |
| 11 Tie-break | none needed: one binding day (20 November 2008) under every sound valuation; R3's two episodes stated together and no day graded |
| 12 Maturity and censoring | swaps open at the review date are outside the per-sale average (D.7(b)); they are forecast in R8; swaps not yet sold are in the plan (SF32) |
| 13 Order of operations | the cap applies to realised volatility before the settlement amount (confirmation section 4) and bounds the valuation (annex) |
| 14 Row order | no result depends on file order; the valuation feed is keyed by date and reference |
| 15 Duplicate resolution | the re-sent valuation file repeats identical rows (C1); the superseded blotter row is marked and sits on an expired swap |
| 16 Identity normalisation | ticket to dealer reference through the blotter; the novated confirmation has expired |
| 17 Netting against gross | collateral is the sleeve's net negative value, swaps taken together (D.5(d), SF10); the plan's range is receipts net of payments (D.7(e), SF33) |
| 18 Dimensional units | volatility points and variance points never added: the confirmation's variance units convert them (SF27); the expectation is taken of variance (SF21) |
| 19 Code and status semantics | blotter statuses LIVE, SETTLED, SUPERSEDED and NOVATED read as written; never a result's difficulty |
| 20 Integerisation | sizes in multiples of USD 100, floored (SF16); dollars to the nearest thousand |
| 21 Clause scope | D.5 governs the limits, D.7 the plan; D.7(c) scopes experience to the whole record; D.7(d) scopes a range to the average, D.7(e) to the year |
| 22 Forward window contents | 2027 holds ten open 12-month sale months' expiries, the standing ladder's two sales still to come and nine new 3-month expiries; the exchange calendar ships the dates |

## Literal reader

A reader executing the shipped sentences word for word:
1. D.2 and D.3 with the blotter: the sleeve runs one ladder, 12 months at USD 50,000 a point per sale (two live
   confirmations of 25,000 for each trade date).
2. D.5(a) and (b): the 3-month ladder is sold on every sale date from January 2007, published index or not. The
   3-month index file starts on 18 September 2009, so 32 strikes are not in it. No sentence says how to find them:
   the reader has to rebuild them, and every rebuild from both neighbouring indices gives R1 and R2 inside their
   bands, as do the index's published earlier closes.
3. D.5(d) with the valuation file's implied-to-expiry column: a swap's value is its vega times strike squared less
   (accrued variance and the variance implied for its remaining term, weighted by days) over twice the strike,
   never worse than the capped settlement. On every day of the record the 12-month ladder's collateral peaks at
   USD 25.9m (R3); with a 3-month ladder beside it the collateral limit of USD 44.628m binds first, on 20 November
   2008, at USD 114,400 a point (R4); a 6-month ladder binds the same day at 58,700 (R5).
4. D.7(d): the range the average itself lies in four times in five. No sentence says how; the settlements show one
   sale tied to the next, and every way of keeping neighbouring sales together gives R6 and R7 inside their bands.
5. D.7(a) and (c): open swaps at the settlement amounts they are expected to pay, from the whole record's
   experience. Read as the value, the figure is USD 1,883,000; the record shows the same swaps paying more than
   their value from four start dates in five, so the value is not what they are expected to pay, and the
   expectation is USD 2,494,000 (R8) with its range (R9).
6. D.7 (lead), (b) and (e) with the exchange calendar: the plan carries every ladder's swaps that expire in 2027:
   the ten open sale months, the 12-month ladder's November and December 2026 sales at its average per sale, and
   nine 3-month swaps sold from 19 January at theirs: USD 5,728,000, with the range of the year's settlements
   taken together (R10).
Every literal reading gives the golden or breaks a quoted sentence, except two places where the sentence files the
quantity and the record decides the method: step 5's first reading, which the record's own outcomes rule out
(SF19), and step 4's resampling of single settlements, which the settlements' own correlation rules out. Those are
the places a judge may read a second answer, and they are reported.

## Prompt contract

A voice rewrite may not drop or change: the question (the largest size of a new 3-month ladder from the January
2027 sale that keeps the sleeve inside both policy limits, with the limit and the day that bind); the same for a
6-month ladder instead; on the policy's record and per USD 100,000 a point, the 3-month ladder's average settlement
per sale and worst calendar year and the 80 per cent range of that average and of the 12-month ladder's; the
12-month ladder's peak collateral; what the open swaps that expire in 2027 should be expected to settle at, with an
80 per cent range; the sleeve's 2027 cash plan by ladder at that size, with its 80 per cent range; the three
deliverables by type (a short memo, a spreadsheet, a CSV of the sleeve's collateral at that size for every day of
the record); the rounding (dollars to the nearest thousand, sizes in multiples of USD 100 a point). It must never
add: how a strike is found before its index is published; how a swap is valued; how a range is taken; the word
mark, risk-neutral, premium, interpolate, rebuild, backfill, overlap, block or bootstrap; the years 2008 or 2020;
the name of any attached file; who is asking; how many swaps are open or still to be sold.

## Tried and rejected

- 2026-11-08, architecture 7's first truth (recovery and workout length tied to both the economy's year and the
  house's): the textbook downturn link, recovery on the economy's year alone, then filed neither too (Kestrel Lane 3.2,
  Ostvale 2.4 per cent on the pack), so the one-fact hint landed the call; the economy's year now moves how many
  default, not what a default recovers.
- 2026-11-08, the world's recovery tied to the observable count of the house's other defaults in the year rather than
  to the house's state: the count depends on how much of the house's book a simulation draws, so a note holding a
  slice of a house had no single truth; the truth is the latent house-year shock, and the observable count carried to
  a note's own loans is the rival at rung 2b.
- 2026-11-08, architecture 6's portfolios under the house-linked recovery: Ostvale spreads 100 loans over 45 houses, so
  the link barely moved it (0.79 to 0.73 per cent) and the call stayed Ostvale; Kestrel Lane now lends to seven houses'
  stronger credits, which pass on one average loss and fail once the clustered defaults recover less, and Ostvale to
  weaker credits that fail on every route that prices its defaults at their houses' state.
- 2026-11-08, MP-RN-2 3.4 as architecture 6 shipped it ("the share lenders on comparable loans fail, on average, to
  recover ... taken over every comparable default"): read literally it files one pooled average, the route the step
  overturns; 3.4 now files each default's own loss over its workout, 4.1 the workout file with its open workouts, and
  4.2 standings correlated and recoveries with them as far as the record shows.
- 2026-11-08, a half-strength house effect as the attenuated rival with the intercept kept: the intercept carries the
  record's clustered defaults, so halving the slope alone lowers every loss and is no estimator a solver would fit;
  the attenuated rivals are the link fitted on every closed workout and the house shock inferred against the year's
  rates.
- 2026-11-08, a workout open nine years (a 2017 default with the house's longest stretch), then 2019 workouts still
  open at an eight-and-a-half-year cap: the mature cohorts were no longer all closed; workouts are capped at six and a
  half years.
- 2026-11-08, recoveries reported in per cent by some lenders and as fractions by others, with no floor: a per-cent
  lender's 0.8 (0.8 per cent) reads as 0.8 (80 per cent), and the stronger house link put enough recoveries under 1 per
  cent to move the loss given default by 0.002; a workout now always recovers at least 2 per cent, so every per-cent
  figure is 2.0 or more and no reading of the column is ambiguous (SF21).
- 2026-11-08, the house link at a recovery loading of 0.16: an independent estimator (moment dependence, its own
  Gauss-Hermite shocks, a cohort table) put Kestrel Lane at 1.0 per cent against the golden's 2.6, the tail being steep
  in the loading; the loading is now 0.26, so every sound estimator keeps Kestrel Lane over the bar while one average
  recovery keeps it under.
- 2026-11-08, Ostvale at 15.0 per cent subordination with weaker credits: the house link raised Ostvale's chance under
  the golden's estimator and lowered it under the verifier's (the link's intercept sits above the average recovery and
  Ostvale's defaults spread over many houses), so Ostvale's side of the bar moved with the estimator.
- 2026-11-08, Ostvale at 12.5 per cent: every sound route kept it far over the bar, but the record's co-default line
  carried to its own loans left it at 1.1 per cent, so rung 2b's call turned on the form a run fitted (cells Ostvale,
  line neither); Ostvale now offers 13.0 per cent, where every form of rung 2b files Ostvale and every sound route
  keeps it over 2 per cent.
- 2026-11-08, the estimators' band from two default-rate tables and two dependence estimators under the golden's
  link alone (Kestrel Lane 2.9 to 4.0): the verifier, refitting the link under its own pair-moment dependence, put
  Kestrel Lane at 1.6, outside it; the band now refits the link under each dependence and each shock basis, so it
  holds every sound estimator the build runs.

- 2026-11-08, architecture 6 (the sponsor house's year in the default dependence, Ostvale bought at 0.54 against
  Kestrel Lane's 1.33): landed on the platform (author's report, not stumped). Both runs rebuilt sponsor ownership from
  Dealtrail and fitted a house factor (run 1 Kestrel 1.47 and Ostvale 0.58; run 2 0.94 and 0.55), so the deep step was
  noticed and executed; both priced one censoring-corrected recovery for every default. Architecture 7 keeps the world
  at the author's word and moves the deep step to the recovery a default earns in its house's year.

- Pack 1 of the prototype (2026-10-24, seed 3061) hid each imported car's pack history before its Dutch registration (the log started at the Dutch registration), so a solver could not know an import's pack state and both probes repaired it differently (sonnet calibrated the imports down by 0.74, opus modelled the abroad replacements in expectation): a fork, not the stump. The log is now the OEMs' EU-wide record plus Voltwerk's own, and a car whose pack failed outside warranty abroad is scrapped there and never imported.
- The prototype's truth carried a scrappage and export rate that no file shows; the forecast now takes a car in use to stay in use through 2027, filed in the tooling plan.
- The first cut's imports arrived about six years old, inside the eight-year warranty, and moved the call by three per cent and one lot; the Mira city car is now the platform kept alive by old imports from abroad, as old cheap EVs are.
- A refurbished pack failing inside Voltwerk's two years was logged as an OEM warranty fit in the prototype (99 rows): fixed, a Voltwerk-warranty failure takes another refurbished pack under Voltwerk's cover.
- The first stage-2 world kept the Mira city car launched in 2014 with 520 imports a month and an eight-year warranty: its arrival stream still ramped through the replay windows, so the 6- and 24-month windows spread the Mira's forecast by 51 and the total straddled a hundred bin. The Mira is now launched in 2013 with a five-year warranty and a steeper wear-out, its stream flat over the last 36 months and its imports arriving as survivors on their original packs.
- An estimand counting only failures outside both warranties left out the packs Voltwerk itself replaces under its two-year warranty, which the line supplies too; the plan now counts every failure outside the OEM warranty.
- Grading each platform's forecast paid the wrong route: the register-only route files four of the five platforms' forecasts at the nearest hundred (only the Mira moves); the prompt grades the slots and the total.
- Ask B's re-keying first moved the naive share by under 0.1 point on the Volta hatch, the new ids passing at about the platform's own rate; the BMS is now replaced in seven reworks in ten and the line seed (31062, from 750 swept) keeps every platform's natural read and over-repair outside its bin on all three asks, worst golden edge 0.155 of a bin.
- The dealer rows of the replacement log first carried plates typed with dashes; a solver who joined without normalising them filed Mira 1,350 and Volta 1,000, so that mess could move the call (dataset-generation R2) and was cut: both sources now carry the register's own plate format.
- Ask C's first device, dock 2 setting its rejects aside without scanning them (absent from the intake export, present at the recycler without a core code), was landed 5 of 5 by the stage 4 reader: dock 2's zero rejects and the blank core codes sit on the path of anyone counting rejects, and the judge found the dock's practice stated in no file. Re-sited onto the grade's date (D2): the intake export carries each core's grade on 1 July 2026, so a core the line built on and scrapped reads AFGEKEURD, and only its work order in the MES shows it passed intake; every ask C figure is unchanged.
- The plan's "a car in use in the Netherlands is taken to stay in use through 2027" read to the stage 4 reader, and to the judge as its one soft spot, as freezing the register of 30 June 2026; the sentence now places the car in 2027 ("a car in use in the Netherlands in 2027 is taken to stay in use for the rest of the year"), the population the estimand already files, and names no import.
- The portal returned the build on determinism (both judges: Gates C, D and E, underspecified_objective, A, B and G passing): the plan as shipped named the register as its only source and its only dynamics clause was about exits, so both judges forecast the register of 30 June 2026 alone (3,448, 3,500 with a judge's renewals), and a judge also summed ask A's batch lines as written. Pinning the population to the register was refused (it makes the judges' answer the golden and spends the stump), and filing the projection (a twelfth a month at the trailing rate, mix and age) was refused (rule application, CLAUDE.md rule 3). Closed instead by the WHAT at authority: plan section 3 files the fleet of 2027 as the register and the cars first registered here from 1 July 2026 to the end of 2027 (SF25) and one pack per car (SF26), the projection left open and forced by C1 over 144 projections, and the line notes file the lot stock rule for ask A (SF27); no graded or stated figure moved (freeze.py). The cost: that the later registrations are in the fleet is now readable, so the decisive rung keeps only what no sentence says, which of them fall due; the default path's answer is now the easy route's on the literal estimand (the later registrations carried as new cars).
- 2026-10-31, architecture 1 spent at the batch 1 triage: shipped 10-24 and reshipped 10-26 after the portal's determinism block, its isolated cold reader reproduced the call cell for cell (Volta 900, Kestrel 250, Plover 350, Mira 1,450, Tern 50, 3,800) and named the decisive step a procedure, since the repair's population sentence and the plan's pack-age sentence read together as the method; the surviving risk the note recorded was that conditioning a survival curve on survival to the as-of date is reflex reachable. Re-rooted in a new world rather than hardened.
- 2026-10-31, re-root screen before this draw: an actuarial reinsurance-capital draw (a county mutual's 2027 windstorm programme, the vendor's year loss table loaded storm by storm for demand surge read off the market's index loss) cleared `guard.py check` and was set aside unregistered, because task309 (FORTIFIED roofs, one cut ratio across storms that varies with gust intensity, carried through a vendor event set) is the same insight in the same domain; regression to the mean in a health-services pilot and a healthy-adopter uptake were set aside as general statistical mechanisms readers name unprompted (task308's screen of six); stale-priced returns in a portfolio's risk budget were set aside as task135's cross-day covariance.
- 2026-10-31, architecture 2 (the development corporation's 2027 inward investment award between a logistics hub on the city region's boundary and an inland food plant, the induced round read where each project's staff live) drawn, registered and spent at stage 2 before any data was cut: the survivor anatomy's Actor test failed on paper, since where the hub's staff live is one join from a column (a roster postcode against the postcode directory's local authority), and every honest way to ship it (a roster, a travel plan's postcode survey, a commuting flow for the depot's zone) is a column or a sentence that sends a solver to it; the IO world offered no relation between rows that carries the induced round's leak.
- 2026-10-31, architecture 3 first cut (an occurrence cover against an annual aggregate cover): the two covers' releases separated by about 1.12 times under every loading of the storms, so no costing of the record moved the call; redesigned at stage 2 into the second-event cover, buy or not, on the occurrence cover's retained band.
- 2026-10-31, the second-event cover on the 50th worst year alone, an upper layer above the occurrence cover and a tall tower from 12 to 60 million were each priced: the single year was noisy enough to flip on the seed, the upper layer's release was small and noisy, and the tower closed the gap between the cheap routes and the golden; the capital policy's average of the 50 worst years and the 7.5 million xs 4 million band were kept.
- 2026-10-31, the first record draw (seed 498): the ratio of totals over the later storms of each season landed the call (worth plus 0.13 million) with the golden's release, and the mean of ratios over the later storms of each year landed it too; a stormier physics with more trains a season made the rank routes buy harder, and shifting a year's first train to clear the year end left nine gaps of exactly 70 days and one inside the window corridor. The record is now drawn with trains kept apart across the year end and searched over 7,500 seeds for one where every rank, year, season, size and pooled route under every estimator files the wrong call (seed 2703, worst route minus 0.06 million).
- 2026-10-31, an exposure ask on the home book (sums insured in force by county) was set aside: in-force by date, renewal terms under new numbers and lapses are rule application a careful solver executes, with no reconstruction left after noticing; the home extract ships as a distractor and the farm book carries the exposure ask.
- 2026-10-31, a reopened claim's further damage first came to some claims before they had been notified, which no claims system allows and which left the pairing of lines and instructions unrecoverable for those claims; further damage now comes only to a claim already open with its adjuster instructed.
- 2026-10-31, architecture 3 (Penwarden's second-event windstorm cover for the county mutual) spent at stage 4: the FIX_NOW failed its second pass. Pass 1 (DETERMINISTIC, FIX_NOW) found "worth" in two senses, cover B's one reinstatement missing from the working and the coinsurance share unpinned, all fixed; pass 2 (DETERMINISTIC, FIX_NOW) found the 2026 storms asks open, since 379 reopened /R1 claim lines with no instruction of their own took their original claim's instructed damage day in the golden, a rule filed nowhere, and the lines' own loss_date filed a recovery of 11,881,000 against 12,015,000. The main call (follow-on storms costing 1.62 times the model) held throughout. The lesson carried forward: a reopened, re-sent or amended record's date or owner is filed or unmistakable before any ask counts it. Reports kept as determinism_check_report_arch3.md and determinism_check_report_arch3_pass2.md.
- 2026-10-31, architecture 4 at its stage 4 judge (NOT_DETERMINISTIC, reconciled FIX_NOW): the call held in every variant, but the runner-up, the gap and the kept alpha moved with the curve's exponent (momentum 3.91 to 5.88 between 0.7 and 0.4), its weighting, a common intercept across the bands, the consolidation day left as a return and the ESG names dropped, because the desk's orders sat almost all under 3 per cent of a stock's day (1.2 per cent were event trades) and the data did not separate the forms (R2 0.4655 against 0.4630); the ESG list also took effect inside the log (15 January 2026) while 101 rebalance rows still traded listed names. Repaired in the generator, the call and the decisive step unchanged; the judge's verdict kept as determinism_check_report_arch4.md.
- 2026-10-31, the first repair raised liquid event trades to a tenth of the desk's orders (4 to 60 per cent of the day): the family converged, but those orders carried most of the desk's traded pounds, so the value-weighted band averages (57, 75 and 115 bps) converged on the curve and filed UK Mid Cap Value, and the default path no longer ended wrong. Rejected.
- 2026-10-31, kept: participation comes from thin names, as it does on a desk. Each lower band carries a tail of thinly traded names (52 in the FTSE 250, 100 in the SmallCap), where the books' ordinary orders, sized in pounds and scaled only mildly with liquidity, take a fifth to two thirds of the day; the desk's pounds stay in liquid names at about one per cent, so the band averages still file momentum (by 2.7 million) while about 1,550 small-cap orders above a tenth of the day pin the curve where momentum trades. The 12 least liquid small caps, which no book or candidate trades, carry the consolidations; the ESG list predates the log and no book or candidate trades a listed name; the books' orders begin on 1 April 2025 with 60 sessions of history; the Severnvale transition trades large and mid caps only, at five orders a day.
- 2026-10-31, a tail of 130 thin small caps was dropped: it left momentum's investable pool (5 million a day or more) too small to swap 18 names a month, and its kept alpha fell to under 1 million.
- 2026-10-31, a common intercept across the bands was not chased: the half-spread differs by band (3, 8.5 and 25 bps), so one intercept misprices each band's trades by 0.5 to 2.2 million, which no rounding bin absorbs; IC-07 now files the population a cost is estimated from (the desk's executions in the candidate's index band), the WHAT, and the golden fits band by band. A lower shortfall noise and a narrower or wider spread of order sizes were screened and left the family's width unchanged (it is form error, set by where the desk's orders sit), so the order sizes' spread was set at 0.6 for the wider stump margin.
- 2026-11-07, architecture 4 (Wealdmoor's GBP 400 million to one of three backtested UK strategies, the alpha each keeps once its rebalances are priced at that size) spent on its first portal round, FAILED_TO_STUMP: both responses filed the golden exactly (UK Mid Cap Value 8, UK Large Cap Quality 6, momentum 5, gap 2) by the field's own textbook, a per-band fit of shortfall on volatility times the square root of participation, validated on a July to November holdout where it beat the flat band costs (RMSE 13.6, 8.5 and 18.9 bps against 26.6, 12.7 and 40.2), so the data revealed the right method by fit; both also took all 24 ask figures, since the failover merge and the block allocation were filed in TCA standard section 1 and the allocation export. The participation-dependent cost carried to size is what a careful analyst executes by reflex; the market-impact world, the capacity driver and the which shell are spent.
- 2026-11-08, re-root screen before architecture 5 (paper only, no harness): a retention trial's spillover through referral or household ties (task127's reserved credit contagion is the same insight, and task131 v1 shipped household interference); an outpatient follow-up rollout netted of GP re-referrals and a DNA programme credited only with avoided rebookings (the first is a hidden overlap the author's lesson says both responses find, the second is one group-by once thought of); theatre overrun cancellations traced to a late start from the first patient's admission (task130, task111 and task137 screened the knock-on as a reflex); line infections split insertion against maintenance by days since insertion and an IV-to-oral switch netted of unswitchable courses (the options' own names announce the class, and the IVOS criteria are filed nationally); broadband full fibre's churn benefit by copper line length (the line's sync speed is one join from a column).
- 2026-11-08, architecture 5's first registered draft (a ward deterioration service, e-obs alerting with critical care outreach, validated at about a 43 per cent cut in arrest calls in two directorates and carried to an uncovered directorate whose arrests mostly had no e-obs escalation in the day before): rejected before registration on the abstraction sentence, because it is task258's insight in clinical nouns (a validated effect that works only through a per-unit precondition every past application met, carried to units that lack it, visible only by a join), and the guard put its structural signature on task127 v2 (the landed concurrent wait); the antecedent-arrest analysis is also the rapid-response literature's own (MERIT, NCEPOD), so a careful response would execute it.
- 2026-11-08, a shared-care rule filed in the federation's policy (practice pharmacists may not stop a specialist-started medicine without the specialist's agreement): rejected, because with the rule filed the decisive step becomes identifying a class from records under a filed rule, which is rule application; the provenance effect is left to the pilot's own outcomes.
- 2026-11-08, ask A first counted letters about each network's registered patients, the hospitals' stale practice
  field the device: the registration date (the letter's, the receipt's or the half's start) was unfiled, a fork, and
  filing it pinned the device; re-sited onto the letters each network's practices received, the asking sentence's own
  basis, with the devices in which records are one letter and which receipt is whose.
- 2026-11-08, the first GP Connect rows carried the letter's own date as the document date: the hygiene battery's
  re-key on patient, sender and date found every receipt and the cracker kept all five second-half letter figures.
  GP Connect messages carry their own send date, which the workflow log now holds.
- 2026-11-08, harms first graded to one decimal: a carry stratified by provenance and age band moved the antipsychotic
  review by 0.3 harms, so harms are whole numbers and patients the nearest 10, the precision the pilot carries; the
  specialist-started pilot patients who came off are the ones whose age band and sex leave the stratified carries
  inside those bins (checks.py M5), each review's rate unchanged (1 of 24, 1 of 24, 2 of 48).
- 2026-11-08, an initiation letter typed in the mental health trust's outage week went out in the 7 April batch, so a
  response that dropped the batch for ask A lost those patients' provenance on the call: such courses now carry the
  hospital trust's letter, and no initiation letter is held (checks.py K6).
- 2026-11-08, the first cut's gabapentinoid pool took 37 extra patients from texture opioid users overlapping texture
  gabapentinoid users, and palliative-care and epilepsy texture patients drawn from other reviews' pools left the
  protocol short of the truth by one or two: texture is now drawn outside every pool, and the protocol finds exactly
  the truth's patients (checks.py T1).
- 2026-11-08, read as a literal judge before stage 4: the close-out's take-up sentence (94 per cent of invitations)
  invited multiplying each chance by take-up, which moved review B to 11 harms and 270 patients; the sentence is gone
  and specification 3.2 files that the team reviews every patient in scope. Ask B's network read at the quarter's
  start moved 7 of 20 figures (newly registered patients drop out); specification 4.1 files the day of the
  consultation. "Hospital medicine letters" could be read without the mental health trust; specification 4.3 names
  both trusts. None names a device.
- 2026-11-08, stage 4 judge pass 1 on 0bacf975 (DETERMINISTIC, FIX_NOW): step 6 gave the GP Connect key as patient, sender and document date, which a literal reader took as the letter date (the message's own date is the day of receipt) and which filed the second-half letters 12.0 to 14.5 per 1,000 low; hub appointments written up on the next working day across a bank holiday left a weekend-only reading one figure off (Wrekinside North's second quarter, 11.7 against 11.6); and a 7 April copy's second receipt was left to the word letters. Step 6 now states the verifier's match, the pharmacists write up before a bank holiday, and specification 4.3 counts a letter once at its first receipt.
- 2026-11-08, architecture 5 (Marches Primary Care Collaborative's 2027 deprescribing review, the pilot's take-off carried by who started each medicine) returned on its first platform round (Project Sulfur) by the determinism check: the check executed specification 3.3 with each review's pilot rate, read the close-out's section 3 (no practice, age group or sex differed from the review's overall rate) as the licence to carry that one rate to every patient in scope, and filed review A at about 24 harms against B 12 and C 11, as both runs did; it ruled the golden's split by who started the medicine, read from the letters with a 60-day window, a method nothing in the pack forces, since the letters sit only in specification 4.3. The in-house judge had passed the split because the pilot separates on it (1 of 24 against 63 of 136); the platform's test is whether a governing document forces the method. A sentence that forces it files the method (rule application, the shared-care rule rejected above), a golden on review A leaves both runs on the call, and the slot's assigned domain is quantitative finance, so the architecture is spent and the build is carried on in Project Sulfur as task9.
- 2026-11-08, re-root screen before architecture 6 (quantitative finance, paper and a numpy prototype only): a
  point-in-time and search-discounted backtest (client strategy 01) was set aside because each step is a named
  correction a careful run executes (point-in-time constituents, delisting returns, the deflated Sharpe ratio); a
  VaR model's breach timing (client strategy 02) because the Christoffersen test and a volatility-scaled replacement
  are the field's own moves; an earnings-event variance decomposition for single-stock options because the earnings
  calendar would be a dedicated organ; momentum's conditional beta after a bear market because "momentum crashes" is
  named literature; private-equity NAV marks projected by each manager's exit uplift because desmoothing a reported
  mark is a spent family (mark slots on assessors' lagged marks).
- 2026-11-08, architecture 6's first prototype compared a portfolio concentrated in a few buyout funds against one
  concentrated in a few industries, at one attachment: with an industry factor near 0.07 to 0.12 and a fund-year
  factor near 0.25 to 0.35, the two concentrations offset (the five-year chance of loss within a factor of 1.1 to 2.3
  either way), so no estimate of either factor moved the call decisively. Re-shaped so the textbook advantage is the
  fund-concentrated note's own (more subordination, better ratings, more industries) and only the fund-year
  dependence takes it away; the industry-concentrated note's tail barely moves under either model.
- 2026-11-10, architecture 7 as it stood (one investigation, the sponsor house's year, carrying the call) read against
  the client's depth scale: a solid level 4, not 5, since three of its four shortcuts landed on the same wrong call
  (buy Kestrel Lane) and Ostvale failed on almost every route; rebuilt as a results chain with a second, independent
  strand (each sector's loading on the economy's year) so different shortcuts land on different wrong calls.
- 2026-11-10, the results chain's first cut kept Ostvale at 13.0 per cent subordination: with recovery tied to the
  posterior house-year shock, the link alone already put Ostvale over the test (2.0 per cent), so the sector strand
  decided nothing on its side; Ostvale now offers 17.0 per cent, where the link alone passes it (0.6) and only the
  sector loadings take it over.
- 2026-11-10, the house's share estimated by pair moments pooled over the whole record (0.29, then 0.31 sector by
  sector) sat well under the truth's 0.40 because a pooled loading mixes the swinging sectors with the rest; replaced
  as a band member by the moment estimator over every same-house pair on the fitted sector loadings (0.37).
- 2026-11-10, check V2 stated on co-default counts (the open workouts' defaults having more co-defaults than the
  closed ones) did not separate (0.42 against 0.41 a default); restated on what the censoring is about, the closed
  cohorts' workout durations by house-year shock (the worst third 4.2 years against 3.2 for the best) and the open
  workouts' shocks against the closed (-1.33 against -1.16).
- 2026-11-10, the first card kept architecture 7's forcing event (purchase order), context artifact (a filed
  standard) and prompt shape 02, and guard.py blocked each as repeating mark162 v2, task11 and task12; redrawn to the
  allocation round (budget_or_appropriation), the managers' collateral tapes (register) and shape 10.
- 2026-11-10, the memo plus a workbook of the year-end chances put the prompt's deliverable set (docx and xlsx) at 4
  of the 13 prompts on file against the 20 per cent cap; the year-end chances are asked as a table inside the memo,
  which is the one deliverable.
- 2026-11-10, the results chain at stage 4 with Ostvale at 17.0 per cent and the recovery sample left to the analysis:
  the determinism judge returned NOT_DETERMINISTIC (SEND_BACK on Gate C, G passing, H borderline). MP-RN-2 4.1 said
  only that the open workouts were in the record, so a link fitted on every closed workout, which bought Ostvale (0.77
  per cent), was a defensible reading. Separately, the weakest sound estimator's 1 per cent loss quantile for Ostvale
  (17.29 per cent of par) cleared its 17.0 by 0.29 points (1.15 per cent). 4.1 now reads recovery from the default
  years whose workouts have all closed, and Ostvale offers 16.5 per cent.
- 2026-11-10, architecture 7 as a results chain, after the stage-4 repair closed the judge's Gate C findings: the
  generator's bar then failed on Gate H. One sentence naming both strands (recovery on the sponsor house's year, each
  sector's loading on the economy's year) rescued 4 of 9 results (checks R5), and the weakest sound estimator cleared
  Ostvale's subordination by about one point of par (R7e). Both strands were structures built into a generated world,
  which is what the client's review returns. Spent before any upload; re-rooted as architecture 8 on public market
  records used as is.
- 2026-11-10, architecture 8's first exploration, a tail hedge sized in VIX futures from the 275 monthly contract
  files: a curve model that carries the hedge's gain back to the quarters before the futures traded reproduces the
  average event gain and misses single quarters by about 40 per cent (the fourth-month contract in the last quarter of
  2008: 15.1 modelled against 27.4 traded), as large as the frame effect it would measure (8.3 against 9.9), so the
  result is not determinate.
- 2026-11-10, a VIX futures hedge of the variance ladder, the contract month and the ratio chosen on the record:
  twenty annual observations set both (about 3.4 fourth-month contracts per USD 1,000 of vega lifts income over worst
  year from 0.26 to about 0.70), an in-sample fit with a fork at every roll convention; and each listed future's
  settlement forecast is a predictive regression with a holdout, the runs' reflex. The futures files are not shipped.
- 2026-11-10, the sleeve's mix across four maturities chosen by linear programme on the record (the most income
  inside both limits): the optimum moves between vertices across sound variants (1-month 201 with 6-month 91 thousand
  dollars a point under total-variance marks, 224 with 57 and 15 of 12-month under linear-volatility marks) and beats
  the best single ladder by 8.5 per cent, so the answer is the midpoint of different designs with a thin margin.
- 2026-11-10, the pick of one maturity at its largest size: the 1-month ladder wins under every route but one (its
  index covers the whole record and its collateral never binds, so its figure needs no judgment), and the only route
  that changes the pick is running the 3-month ladder from its index's first date, one fact. The question is set on
  the size of a 3-month ladder beside the standing 12-month one, where the binding day (20 November 2008) needs the
  rebuilt strikes, marks at the remaining term under the cap and the standing ladder's own use of the limit.
- 2026-11-10, two results tried as priced judgments and measured as earned: the standard error of a ladder's average
  yearly settlement (grouping by calendar year, the natural unit of the question, already gives the honest figure:
  22.6 for the 12-month ladder against 8.1 from the monthly settlements), and the 80 per cent range of the open
  swaps' settlement by adding each swap's own percentiles (7.9 to 84.9 joint against 6.3 to 85.8, because the
  remaining windows are nested). The first is dropped; the range stays as one result whose hurried failure is
  drawing the swaps independently (19.8 to 72.7).
- 2026-11-10, the rebuild of the missing 3-month strikes tried as the place where sound methods split: every rebuild
  that uses both neighbours lands within 3 per cent on the ladder's worst year (158.5 to 163.9 a point) and on the
  size (112.7 to 119.1 thousand), while one-sided proxies do not (the 30-day index scaled by its average ratio to the
  3-month index gives 117.0 and 139.3; a regression on the 30-day index alone 141.3 and 127.0), because the ratio is
  1.125 on average and 0.921 on the 102 overlap days the 30-day index closed above 35. The band is set by the
  two-sided rebuilds and the one-sided ones are the hurried route.
- 2026-11-10, the first card (a committee as the forum, the dealers' contract as the forcing event, a how-much
  question, a memo and a workbook): guard.py blocked the forum against task14 and the forcing event against task3,
  warned on the question form, and voice-check.py put the deliverable set at 33 per cent of the prompts on file.
  Redrawn to the treasury and investment office acting on it themselves, the ladder's January launch, a what
  question, and a third deliverable a risk reviewer uses, the sleeve's collateral for every day of the record.
- 2026-11-10, the truncation route priced in the careful column (the 3-month ladder run only from its index file's first date, USD 136,600): a literal reader of D.5(a) could defend leaving out sale dates with no published strike, so D.5(b) now files that a sale date counts whether or not its index was yet published; truncation is ruled out by a sentence and the careful column is priced on the one-index stand-in, which its own whole-overlap check confirms.
- 2026-11-10, the 3-month index treated as unpublished before September 2009: its closes from 4 December 2007 are public on FRED and equal the Cboe download on every day both carry. The pack stays as Cboe publishes it, the series is held as a cross-check beside the generator and outside the pack, and every band was widened to hold the answers on the published closes (the average's band top moved from 286,000 to 287,000).
- 2026-11-10, two mechanical asks (each open swap's realised volatility, the book's value at the review close): dropped as asks and kept in the workbook; with no assembly result graded, the blotter's amended and novated confirmations were moved to swaps that have expired, so neither can cost a graded result.
- 2026-11-10, the chain on two blocks (the frame and the expectation), where a run making either move scored about 70: a third, independent block added (the range of each ladder's average and the plan's range, which need neighbouring sales kept together), the plan made one joint result over all 21 settlements with the standing ladder's two coming sales in it, and the recommendation made to need all three.
- 2026-11-10, the compound sentence as a hard gate (the sentence naming every priced move rescuing a third of the results or fewer): it cannot hold with a pair estimate of 50 or under, because a sentence that names all a pass missed rescues all of it. Single sentences are gated at a third and two moves at once are printed as information (4, 5 and 2 of 11).
- 2026-11-10, average realised variance since 1990 as a sound estimator of the expectation: it draws on years before the record, which D.5(a) and D.7(c) leave out; moved to the ruled-out routes, which lets a volatility forecast squared (3,015,000) sit 4 per cent above the band.
- 2026-11-10, the careful pass granted the joint replay of the whole plan: with it the rebuild and the expectation together would have rescued the plan and the recommendation (6 of 11). It is priced instead on swaps not yet sold drawn one at a time from their ladder's record, the same reflex as its range of an average, while the open swaps' own joint replay stays granted.
- 2026-11-10, the bands on each average's range drawn from blocks and lags alone: counting only the swaps that do not overlap (the full-sample spread over the number of sales divided by the swap's months) is a common correction and landed outside them (14,000 to 616,000 for the 12-month ladder); it is taken into the rival set, and a standard error with fewer lags than the months neighbouring swaps share (123,000 to 507,000) is named as a route that stays too narrow.
