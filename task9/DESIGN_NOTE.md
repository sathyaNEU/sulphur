# task9 design note

Architecture 6, drawn 2026-11-08 after the platform returned architecture 5 on its determinism check and confirmed
the slot's domain as quantitative finance. Architecture 4, the slot's earlier quantitative finance build (the
market-impact capacity call), was FAILED_TO_STUMP on 2026-11-07 with both runs on the golden and all 24 ask figures,
and the author asked on 2026-11-08 for a draw at least three times harder, stumped on the asks as well as on the
call. One architecture per world: energy (EV packs), urban (regional GVA), actuarial (windstorm reinsurance),
quantitative finance's market impact and pharmacology (deprescribing) are spent in this slot, so the build moves to
structured credit with a new world, dataset, generator and prompt shell.

## Draw

1. Card: `.claude/skills/fingerprint/cards/task9.json`, architecture 6, registered 2026-11-08T06:21Z; architecture 5
   moved into the card's lineage with its fate (the four earlier architectures sit there as spent). Guard: PASS, with
   differentiation lines against mark135 (and its v1 lineage) and task7; nearest driver task7 at 0.08.
2. Pairing: Quantitative Finance, task type derivative pricing (the vocabulary's volatility-derivatives-pricing
   key: the price of a structured credit note is its loss distribution), objective Forecasting. The headline is a
   forward quantity, each senior note's chance of any loss of principal over 2027 to 2031, which decides the call.
3. World: Stichting Pensioenfonds Havenbedrijf en Logistiek (PHL), the Rotterdam port and logistics sector's
   pension fund, buys senior rated notes of private-credit funds for its matching portfolio through its fiduciary
   manager Kadeweg Fiduciair Beheer. Two direct-lending managers offer a senior note on a static portfolio of
   first-lien loans to European sponsor-backed mid-market companies: Kestrel Lane Credit Partners and Ostvale
   Capital. Kadeweg licenses Lenderbase (a loan-level performance database of European sponsor-backed loans, with its
   workout recoveries file) and Dealtrail (a buyout transactions database). People from `guard.py names --locale
   nl_NL --seed 906`: Ilse Lips (Kadeweg's head of credit, who puts the purchase to the fund's board of trustees through its
   investment committee), Damian Schenkel (chair of the board of trustees, who signs the rated-note standard), Liza Dekker (Kadeweg's
   credit analyst who receives the managers' data). They appear only in document control lines.
4. Candidates: Kestrel Lane's senior note, Ostvale's senior note, or neither.
5. Quantity: for each note, the probability that cumulative credit losses on its portfolio as held on 1 January
   2027 exceed the note's subordination before the end of 2031, the portfolio held static (a loan repaid early is
   replaced by an identical loan to the same borrower), default and recovery taken from the experience of comparable
   loans; the fund buys the note under 1.5 per cent, the lower if both are, and neither if none is (the standard's
   sections 2 and 3).
6. Shape: 02, a forecast across periods. Each note's chance of having taken a loss by the end of each year 2027 to
   2031 (10 figures), each note's five-year chance of loss, expected loss and the subordination it would need for a
   1.5 per cent chance (6), the call (1), and a chart of each portfolio's five-year loss exceedance with both notes'
   subordination marked: about 20 criteria, every one downstream of the dependence the deep step estimates.
7. Default path: rating and age default rates from the loan database, recoveries from the workout file, a one-factor
   Gaussian copula fitted to the database's yearly default rates, then the agencies' industry factor; it buys Kestrel
   Lane's note (`## Default path`).
8. Data-native sentence: a buyout fund decides from one pot of reserved equity, and one partnership's patience,
   whether to put more money into each of its companies when they breach, so companies held by the same fund at the
   same time fail in the same years; the loan record keeps each loan's own life and the deal record keeps each
   company's buyers, under the names each fund signed under, and no file joins a loan to the fund that held it.
9. Abstraction sentence, written against the nearest builds and found not to be the same: task7 values one
   borrower's rescue by the knock-on write-off it keeps off borrowers who draw their receipts from it (a directional
   contagion, an expectation); mark135 corrects an estimator of a variance for components struck at different times.
   Here no unit causes another's failure and no estimator of a series is corrected: a shared owner's year shock moves
   all its units at once, a variance component estimated from a record joined to a second record at another grain,
   and the call is a tail probability that an expectation never sees.
10. Furniture: forum trustees_or_governors (the fund's board of trustees decides the purchase on its investment
   committee's advice; committee_or_panel was redrawn after task3's architecture 4 registered it minutes before this card), forcing
   purchase_order_or_contract (both offers close on 12 March 2027), org financial_institution (a pension fund),
   role portfolio_manager (Kadeweg's head of credit runs the credit sleeve and asks). Stump strategy `other`: the
   decisive move is a dependence structure (a fund-year variance component in default), which no strategy key names;
   Gate G forecasting (statistical_rigor may not stand alone), pattern G17 decisive with G16 and G13 (the horizon is
   five years of a pool, the record is a year at a time of single loans).
11. As of 17 February 2027, the day after the Lenderbase and Dealtrail extracts were pulled (16 and 15 February,
   with the fourth quarter of 2026 filed); the investment committee meets on 25 February, the board of trustees on
   4 March, and both offers close on 12 March 2027.
12. Prompt shell: a what question (what note, if either, the fund would be right to buy), the second sentence opening
   on the committee note, the rounding sentence opening "Chances"; deliverables docx and csv. None repeats a shell in
   this slot's lineage (whether, how-much, which, what with pptx+xlsx, how-much with csv+pdf).

## Default path

The pipeline a competent credit quant builds from the prompt's words and the files' grain, the field's own method
for the deciding quantity in it (stumping 1.1b).

1. Conform the records: Lenderbase's latest submission of each loan-quarter, its pre-2019 and post-2019 status,
   purpose, rating and date codes on one vocabulary; the workout file's recoveries in one unit; both tapes in euros
   at the ECB rate of 31 December 2026, their ratings on one scale and their industries on Lenderbase's sectors
   through the crosswalk.
2. Company-years at risk 2008 to 2026 (a loan outstanding at the previous year end) and their defaults: 16,712 and
   578. One-year default chance by rating and years since the buyout (a probit, or a cohort table by rating and age).
3. Loss given default from the workout file: 38.0 per cent averaging every closed workout (39.9 per cent from the
   default years whose workouts have all closed).
4. Dependence, the field's method: a one-factor Gaussian copula with the asset correlation fitted to the record's
   yearly default rates (0.109), then the agencies' industry factor (0.059 more inside a sector). The solver's own
   back-test passes: the model's distribution of yearly default counts and of sector-year counts matches the
   record, because a sponsor house's year averages out over eighty houses.
5. Simulate five years for both portfolios at their 15.0 per cent subordination: Kestrel Lane 0.14 per cent,
   Ostvale 0.44 per cent; both pass MP-RN-2's 1 per cent test and the standard's 2.2 buys the lower.

Ends on: buy Kestrel Lane's note at a 0.14 per cent chance of loss against Ostvale's 0.44 per cent
Golden: buy Ostvale's note at a 0.54 per cent chance of loss; Kestrel Lane's fails the 1 per cent test at 1.33 per cent

## Stump sentence

The default path buys Kestrel Lane's note at a 0.14 per cent chance of loss against Ostvale's 0.44 per cent; the
step that lands it there is linking the borrowers' defaults only through the economy and their industries, when the
companies held by one sponsor house's funds default in the same years (a latent correlation of about 0.50 of what
the economy and the industry leave, 0.42 of the whole), and Kestrel Lane's 95 loans sit with five houses, so its
note's chance of loss is 1.33 per cent, over the bar, against Ostvale's 0.54 per cent.

## Deep reasoning

- Task type: derivative pricing in quantitative finance (the vocabulary's volatility-derivatives-pricing key): the
  loss distribution of a senior tranche of a static loan portfolio, serving Forecasting (a five-year forward chance).
- Domain test: the quantity that decides is each senior note's chance of any loss of principal over 2027 to 2031, a
  tail of the portfolio's credit loss distribution, and the field's estimator is a Gaussian factor copula (Vasicek,
  CreditMetrics) with default chances by rating and age and correlations fitted to the default record.
- Swap: "which of two hospital staffing contracts should the trust sign, judged on the chance a ward runs short"
  keeps a pick against a bar but loses the tranche, the attachment point, the sponsor that decides whether to rescue
  a borrower and the default correlation that prices the tail.
- Layer 1: Lenderbase re-submits corrected quarters (a late default filed over a watch), changed its status,
  purpose, rating and date codes in 2019 and carries LEIs only from 2012 (older loans join by name through the LEI
  extract); Dealtrail prints each buyer under the vehicle names a fund signed under (fund numerals, LP and SCSp,
  co-invest vehicles), sometimes the house alone, and carries withdrawn approaches and add-ons; the workout file
  holds recoveries in two units and open workouts with none; the tapes use two layouts, two rating scales and five
  currencies. Each is what the system does; none is placed to be caught.
- Layer 2: correlated defaults (the client's Banking strategy 07) carried into a structured-credit price: the
  dependence the copula must carry, estimated from the record as a variance component at the grain the
  concentration sits at.
- Decisive step: the companies whose funds belong to one sponsor house default together in the same year beyond
  what the economy and the industry explain, so the dependence needs a house-year component whose loading the
  record estimates, and Kestrel Lane's concentration in five houses is what that component bites on.
- Not semantics: with every field read and every record linked the field's copula still files Kestrel Lane,
  because no field records the house: it is a relation between rows (the stem shared by a house's fund vehicles on
  another database's buyout rows) and its effect is a co-movement in time that only an estimate shows.
- Not rule application: no filed rule names the dependence structure (MP-RN-2 4.2: correlated as far as the record
  shows); the enumerated family (one factor, industry, Basel's formula, a persistent fund effect, a fund-year
  effect, the house-year effect, each house as one obligor) spreads Kestrel Lane's chance from 0.12 to about 10 per
  cent and splits the call; the standing family, the structures the record supports, is the house-year effect alone
  (it beats the fund-year effect by 30 log-likelihood units and the persistent forms by 170; same-house pairs in
  different years default together at the independence rate, 0.114 per cent against 0.120), with Kestrel Lane at
  1.33 and Ostvale at 0.54; the ruling-out is loud.
- Analyst test: the easy route a strong analyst takes with every file conformed and every clause read is the
  field's copula fitted to the yearly and sector default rates, back-tested on them, which ends on buy Kestrel Lane's
  note at a 0.14 per cent chance of loss against Ostvale's 0.44 per cent.
- Estimand: MP-RN-2 (phl_rated_note_standard_2026.pdf) sections 2 to 4: the 1 per cent test over the five calendar
  years from the portfolio date, the lower chance when both pass, the portfolio as it stands with replacements, the
  loss per default at the average full-workout loss of comparable loans booked at default, subordination, the
  Lenderbase record, Gaussian credit standings correlated as the record shows.
- No decoy: nothing is planted; no rating letter, diversity score, manager memo or committee draft ranks the notes,
  the term sheets carry the same subordination and no expected loss, and no document mentions sponsors or houses.
- No certified replay: no figure in the pack is to be reproduced and the method is not recovered by matching one.
- Chain: (1) link every loan in the record and both tapes to the buyout that began the ownership it sits in and to
  the buyer's sponsor house, through Dealtrail's buyer names and dates; (2) see that defaults inside a house bunch
  in the same years beyond the year, the sector and the loans' ages, and separate that from a lasting house or fund
  quality (same-year pairs carry it, different-year pairs do not) and from the fund (it crosses a house's funds);
  (3) estimate the house-year component like for like, conditioned on the sector-year, as a latent correlation;
  (4) carry it with the economy and sector components into both portfolios as they stand, with default chances by
  rating and years since buyout and the loss per default from the default years whose workouts have closed, and
  simulate five years; (5) Kestrel Lane's note fails the 1 per cent test and Ostvale's passes.
- Judgment: the house-year variance component in default, a random effect fitted cluster by cluster on house-years
  given the sector-year, justified by the record: same-house same-sector-year pairs default together 3.4 times as
  often as other houses' pairs in the same sector-year, same-house pairs in different years at the independence
  rate, and the house-year clustering fits the record better than the fund-year or any lasting form.
- One-fact test: the likeliest hint is "companies owned by the same sponsor default together"; the run still has
  to find the house behind every loan through Dealtrail's buyer names and dates, locate the effect at the house and
  the year rather than the fund or a lasting quality, estimate it like for like rather than from raw co-default
  counts, take the loss per default from closed cohorts, and carry it through a five-year simulation: each step
  moves the graded figures, and the fund-level reading alone halves Kestrel Lane's chance.
- No replay: the call re-derives no published figure and no stated number is wrong; every input figure in the pack
  is right as it stands.
- Pinned: every rival run on the clean truth in checks.py (R1 to R8): the one-factor and industry copulas file
  Kestrel Lane, the persistent fund and fund-year forms file Ostvale with Kestrel Lane at 0.33 and 0.68, the
  closed-workout loss given default files Ostvale with Kestrel Lane at 0.98, the loan-age clock moves no figure by
  more than 0.07, the house-year estimators (cluster random effect, the pair-count moment estimator) land within
  0.05 of each other on the latent correlation; MP-RN-2 4.2 rules out an assumed correlation (Basel's) and a fat
  tailed copula.
- Run forecast: run 1 takes a method shortcut, the field's copula fitted to the yearly and sector default rates,
  back-tested and buying Kestrel Lane at about 0.1 per cent; run 2 an unfinished chain or dismissed own evidence,
  noting Kestrel Lane's sponsor concentration and keeping the copula's ranking, or modelling a lasting fund quality
  or a fund-level effect that lands Ostvale with every figure off.
- Strategy label: UNTESTED (Banking 07, correlated defaults, not independent ones), built in the live form: the
  excess dependence beyond the field's factors is estimated from the record at the grain a concentration sits at
  and carried into the tail of a concentrated portfolio, the field's copula at rungs 0 and 1.
- Lesson: a dependence a model leaves out passes the broad record's back-test when the broad record is diversified
  across it; the tail of a concentrated portfolio needs the dependence measured at the grain of the concentration,
  read through a second record no key joins; no build on file prices a tranche or measures dependence this way.

## Survivor anatomy

- Actor: the companies have rows (a loan's quarters, a company's buyouts); the property that decides is a relation
  between rows, which companies' funds belong to one house and that their defaults fall in the same years. No
  column in Lenderbase or either tape names a sponsor; Dealtrail names each buyout's buyer fund in vehicle names, and
  the house is the stem those names share.
- Link: loan to company (LEI where Lenderbase has one, the legal name through the LEI extract before 2012), company
  to its Dealtrail buyouts (LEI or trading name), loan to the buyout that began its ownership (dates), buyer to
  house (name stem); no key joins a loan to a house, no sentence invites it, and the comparison that shows the
  effect (same-house pairs in the same year against other houses' pairs in the same sector-year) is one the field's
  copula never asks for.
- Reflex: the field's own method, a one-factor Gaussian copula fitted to yearly default rates and the agencies'
  industry factor, sits at rungs 0 and 1 and files Kestrel Lane (0.12 and 0.14 against 0.32 and 0.44).
- Back-test: the textbook route validates: its predicted distribution of yearly default counts and of sector-year
  counts matches the record (checks.py B1), because the house component averages out over eighty houses.
- Second use: Dealtrail's buyout dates give the years since buyout that default chances run on, for every loan and
  every tape line (a refinanced loan's own date is later); the LEI extract joins pre-2012 loans by name; the
  workout file gives recoveries. Deleting the decisive step leaves every file in the pack.
- Shock: no year, house or fund stands out: Kestrel Lane's five houses have ordinary records (checks.py S1), the
  effect is spread over eighty houses and nineteen years and shows only as co-movement.
- Pins: MP-RN-2 files the WHAT (the test, the choice, the portfolio as it stands, loss per default, subordination,
  the record, Gaussian standings correlated as the record shows) and names no grouping, sponsor, house or fund;
  deleting 4.2 opens the copula's form (a fat tail moves both notes) but forces nothing about the house.

## Readability screen

Tests: 1 filed sentence, 2 schema, 3 reflex, 4 control bench, 5 hygiene, 6 linear, 7 dedicated organ.

| Rung | 1 | 2 | 3 | 4 | 5 | 6 | 7 | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 one-factor copula fitted to yearly rates | no | no | yes (the field's method) | no | no | no | no | readable |
| 1 industry factor added | no | sector column | yes (agency practice) | no | no | no | no | readable |
| 2 loss given default from closed cohorts | no | no | partly | no | no | no | no | readable |
| 3 house-year dependence (decisive) | no (4.2 names no grouping) | no (no sponsor column; buyer names on another database) | no (no copula practice groups by sponsor house) | no | no (the battery dedupes and links, it does not test co-movement) | no (an estimate inside a simulation) | no (Dealtrail serves the age clock) | silent |

## Semantic fork table

| SF | Term or convention | Readings | Ruled out by |
|---|---|---|---|
| SF1 | chance of any loss of principal over the five years | at any time in 2027 to 2031, or at the end of 2031 | same call: losses only accumulate, the two are one figure (checks.py) |
| SF2 | the portfolio | as it stands with replacements; run off as loans repay | MP-RN-2 3.2 |
| SF3 | loss on a default | average full-workout loss booked at default; each loan's own recovery drawn; recovery timing | MP-RN-2 3.4 |
| SF4 | form of the dependence | Gaussian standings; a fat-tailed copula; an assumed correlation | MP-RN-2 4.2 |
| SF5 | conditions over the five years | the record's; a macro view; the latest years only | MP-RN-2 4.1 |
| SF6 | currency | ECB rate of 31 December 2026; another day | MP-RN-2 3.2; checks.py shows a 30 December rate moves no figure |
| SF7 | what counts as a default | Lenderbase's defaults; payment default only | MP-RN-2 3.3 |
| SF8 | loss given default estimate | closed workouts only; default years whose workouts have all closed; a duration model | same call; the record forces the closed cohorts (recovery falls with workout length, the open workouts are the long ones) |
| SF9 | default chance clock | years since the buyout; years since the loan began | same call; the buyout clock fits better and moves no graded figure by more than 0.07 (checks.py) |
| SF10 | the grain of the dependence | house-year; fund-year; a lasting fund or house quality | same call for every sponsor form; the record ranks house-year first by likelihood and pair counts |
| SF11 | the lower-risk note when both qualify | chance of loss; expected loss | MP-RN-2 2.2 |
| SF12 | subordination needed for a chance | the five-year loss quantile | exact by MP-RN-2 3.5 |
| SF13 | weights inside a portfolio | euro par; loan count | MP-RN-2 3.2 and 3.4 (amounts) |
| SF14 | time steps | calendar years; quarters | MP-RN-2 4.2 (a one-year default chance) |
| SF15 | the term sheets' replenishment against the static portfolio | consistent: principal relent to the same borrower | the term sheets and MP-RN-2 3.2 |
| SF16 | whether borrowers and loans age over the five years | ages run on; ages held at the portfolio date | MP-RN-2 3.2 ("Borrowers and loans grow older as the years pass"), added after the stage 4 judge; the held reading keeps the call (checks.py SF16b) |
| SF17 | which defaults the average loss is taken over | every comparable default, open workouts included; closed workouts only | MP-RN-2 3.4 ("taken over every comparable default, those still in workout included"), added after the stage 4 judge; how the open ones end is left to the record |
| SF18 | a defaulted loan in the forward years | leaves the portfolio; replaced like a repaid loan and able to default again | MP-RN-2 3.4 ("A loan that has defaulted leaves the portfolio and is not replaced"), the pass 2 judge's optional pin; the re-default reading gives neither note (2.86 and 1.99 per cent) and is now ruled out |

## Ladder

| Rung | Construction | Kestrel Lane | Ostvale | Files | Dies to |
|---|---|---|---|---|---|
| 0 | one-factor Gaussian copula, correlation fitted to yearly default rates (0.109) | 0.12 | 0.32 | Kestrel Lane | the house-year co-movement the record shows |
| 1 | plus the industry factor (0.059 inside a sector) | 0.14 | 0.44 | Kestrel Lane | the same |
| 2 | plus a lasting fund quality (0.169 of the residual, fitted on funds across years) | 0.33 | 0.27 | Ostvale, figures off | same-fund pairs in different years default at the independence rate |
| 2b | a fund-year effect instead (0.505 within the fund) | 0.68 | 0.50 | Ostvale, figures off | cross-fund same-house pairs carry the same excess; house-year fits by 30 log-likelihood units |
| 3 (decisive) | house-year effect (0.503 of the residual, 0.418 of the whole) | 1.33 | 0.54 | Ostvale | nothing |

Margins: rung 1 files Kestrel Lane by 3.1 times; the golden files Ostvale by 2.5 times and puts Kestrel Lane 1.33
times over the bar and Ostvale 1.85 times under it. Every correction below the house component walks Kestrel Lane's
figure up and the decisive one reverses the ranking. Pricing sequence: the residue the WHAT leaves is the dependence
(a method, not a knob); the ceiling: each house as one obligor puts Kestrel Lane at about 10 per cent, so the move
needed (from 0.14 over 1.00) is inside it; the one-group-by route to the call is "Kestrel Lane is concentrated in
five sponsors", which lands the call and no figure; the standard error of the house component is about 0.04 on
the latent scale, which moves Kestrel Lane between about 1.1 and 1.5 and never under Ostvale (verify.py's moment estimator: 0.460, Kestrel Lane 1.18, Ostvale 0.58); the lever (a
correlation) and the ranked quantity (a tail chance) are not one variance because the portfolios differ in how
their loans group, not in their own noise; the reflex sweep is run as code (checks.py R1 to R8).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the loans in each tape as they stand | MP-RN-2 3.2 |
| 2 Unit of account | a loan, weighted by euro par | MP-RN-2 3.2, 3.4 |
| 3 Attribution window | the five calendar years from 31 December 2026 | MP-RN-2 2.1 |
| 4 As-of dating | the tapes' cut-off and the record to 2026 | MP-RN-2 3.1, 4.1 |
| 5 Version basis | Lenderbase's latest submission of each quarter | the data (re-submissions supersede); asserted |
| 6 Denominator | chance over all simulated five-year paths | MP-RN-2 2.1 |
| 7 Weighting | par in euros | MP-RN-2 3.2 |
| 8 Window length | 2008 to 2026 | MP-RN-2 4.1 |
| 9 Boundary inclusivity | a loss exceeding the subordination | MP-RN-2 3.5 ("exceeds") |
| 10 Rounding path | chances to two decimals, subordination to one, at the end | the prompt |
| 11 Tie-break | the lower chance | MP-RN-2 2.2; no tie |
| 12 Maturity and censoring | open workouts in the loss given default | the record forces the closed cohorts (SF8) |
| 13 Order of operations | defaults then losses year by year | MP-RN-2 3.4, 4.2 |
| 14 Row order | none | C1 |
| 15 Duplicate resolution | re-submitted quarters | latest submission; asserted |
| 16 Identity normalisation | LEI, else names through the LEI extract | the extract's legal and other names; asserted (no loan unlinked) |
| 17 Netting against gross | none | n/a |
| 18 Dimensional units | five currencies; recoveries in two units | ECB rate; values above one are per cent |
| 19 Code and status semantics | Lenderbase's two code sets | one vocabulary; asserted |
| 20 Integerisation | none | n/a |
| 21 Clause scope | MP-RN-2 applies to both offers | MP-RN-2 1 |
| 22 Forward window contents | the five years drawn from the record's conditions | MP-RN-2 4.1 |

## Literal reader

A judge executing MP-RN-2 word for word builds the portfolio as it stands, books the average full-workout loss at
each default, models Gaussian standings "correlated as far as the record of comparable loans shows them to be", and
so has to ask the record which loans' standings move together: the record answers with the economy's year, the
sector's year and the sponsor house's year (checks.py L1 runs the literal reading to the golden).

## Oracles

- The record's yearly and sector-year default counts confirm the textbook copula as well as the golden (both fit
  them): a control that ties on every basis, kept.
- No published figure, rating or score in the pack confirms either ranking. The term sheets' concentration limits
  (obligor and industry) are each manager's own and both portfolios meet them.

## Ask sheet

Every ask figure is computed from the deep step's output (the house-year component in the simulation).

| Ask | Figures | Second judgment | Shallow (industry copula) | Golden |
|---|---|---|---|---|
| A1 each note's five-year chance of loss | 2 | loss given default from the closed cohorts | 0.14, 0.44 | 1.33, 0.54 |
| A2 subordination for 1, 0.5 and 0.25 per cent | 6 | the same, and the tail's grain | 12.5, 13.4, 14.3; 13.8, 14.8, 15.7 | 15.6, 17.0, 18.3; 14.1, 15.1, 16.1 |
| A3 chance of a loss by each year end 2027 to 2031 | 10 | the age clock (years since buyout) and the timing of the house years | 0.00 0.00 0.02 0.06 0.14; 0.00 0.02 0.06 0.18 0.44 | 0.02 0.12 0.36 0.76 1.33; 0.00 0.02 0.08 0.24 0.54 |
| A4 the chart of five-year loss exceedance | 1 | the same simulation | thin tails, Kestrel Lane below Ostvale | Kestrel Lane above Ostvale beyond 10 per cent |

Mess on the ask paths: the same conforming every careful run applies (latest submission, codes, LEIs and names,
currencies, recovery units); none moves a graded figure between careful runs.

| Ask | Why the landed run misses or keeps it | Cracker (the landed run: house-year taken, every mess item cleaned, every rule read, the second judgments at their reflex) |
|---|---|---|
| A1 | the closed-workout loss given default puts Kestrel Lane at 0.98 and Ostvale at 0.33 | miss |
| A2 | the closed-workout loss given default moves each subordination by 0.6 to 0.8 | miss |
| A3 | the same reading moves every year from 2029 outside the bin; rating-only default chances move the profile | miss |
| A4 | the chart's ordering holds under either loss given default | keep |

Shallow keep: 15.8 per cent of ask weight (three of nineteen items fall inside the grading tolerance: Kestrel Lane's 2027 chance and Ostvale's 2027 and 2028 chances, all near zero)
Pair ceiling: 31.3 (ceiling.py: the cracker 47.0 against the shallow run 15.7; two shallow runs 15.7; the full includer, every second judgment taken, 57.8 against a shallow run)
Measured by: generator/ceiling.py

## Prompt contract

The author's voice rewrite may not drop or change: the decision (what note, if either, the fund would be right to
buy, Kestrel Lane's or Ostvale's); the threshold (a chance of any loss of principal between 2027 and 2031 below 1
per cent); the choice rule (the lower-risk one when both qualify) and the hold (neither); the deliverables
ic_note_senior_notes_2027.docx (the recommendation, each note's five-year chance, the subordination for chances of
1, 0.5 and 0.25 per cent, the exceedance chart up to 30 per cent of par with both notes' subordination marked) and
senior_note_loss_by_year.csv (each note's chance of a loss by the end of each year 2027 to 2031); the rounding
(chances per cent to two decimals, subordination per cent of par to one decimal).

## Stage 4

leak.py on target.zip 2e83c33f (--asof 2027-02-17): REVIEW, no LEAK. The main thread's rulings, one line each:

- Sweep 3, the term sheets carry 15.0: the subordination each manager offers, an input the call reads, not an output
  of the analysis; harmless.
- Sweep 4, stump-paragraph terms in the term sheets and MP-RN-2 (record, million, industry, default, effect,
  sponsor): "sponsor" appears only in "sponsor-backed", the asset class's own name in every direct-lending document;
  no sentence names a dependence, a grouping, a house or a fund; harmless.
- Sweep 9, dates after the setting: loan maturities in Lenderbase and both tapes, and the EURIBOR forward dates, are
  contractual future dates every such file carries; no submission, report or resolution date passes the pulls;
  harmless.
- Sweep 11, the prompt's deliverable set at 22 per cent of the corpus and one templating signal (both files named);
  voice warnings only; harmless.

Leak reader, read 1 (isolated, Sonnet at medium, prompt and pack only, on 2e83c33f with the stale prompt): question 1
none for the decisive step (the closest sentences it found, MP-RN-2 4.1 and 4.2, name the field's copula and the
record, rung 0's own method, and nothing about which loans move together); question 2 none; question 3 none (the
sector crosswalk and the standard read as vendor and client documents); question 4 none; question 5 every MP-RN-2
sentence quoted executes to the golden's construction (static portfolio, ECB rate of the cut-off, Lenderbase's
defaults, one average full-workout loss booked at default, Gaussian standings correlated as the record shows);
question 6 an analytical choice, the correlation estimate, with MP-RN-2 4.2 read as fixing the model's form only. It
took Dealtrail for a distractor. Its findings, fixed in one pass: the prompt still carried the drawing-board draft (a
1.5 per cent bar, one subordination target, whole-number rounding) against the standard's 1 per cent and the
goldens' three targets at one decimal, so prompt.txt now states the 1 per cent bar, the targets of 1, 0.5 and 0.25 per
cent and one decimal (the determinism judge's agent flagged the same mismatch while extracting the blocks); the two
term sheets read as one template, so Kestrel Lane's is now a summary of principal terms in a table and Ostvale's a
numbered term sheet in its own words; the note sizes print to one decimal with separators; the ECB file carries the
ECB's full set of thirty currencies. Its sweep rulings matched the main thread's (all harmless). guard.py surface on the rebuilt cut reads "Ireland
Collateral" as a persona: PDF text running "incorporated in Ireland" into the next row's "Collateral manager", not a
name. Not changed: the
workout file's two recovery units (each lender files in its own unit, values above one are per cent, and no graded
figure turns on it).

Leak reader, read 2 (isolated, Sonnet at medium, prompt and pack only, on 150c10c4): question 1 none (the nearest,
MP-RN-2 4.2, "names the structure, a Gaussian latent-factor default model with correlation estimated from
Lenderbase; that hands over the method family, though not how to estimate it"); questions 2 to 4 none (the shared
15.0 per cent subordination "does not discriminate"); question 5 each MP-RN-2 sentence executes to the golden's
construction; question 6 an analytical choice, "how to estimate the correlation and the default probabilities from
Lenderbase, and the files do not settle that" (the data do, which is the judge's question); prompt and standard agree
on the bar, the choice rule, the window and the hold. Sweep rulings all harmless (submission and report dates end
before the pulls; Lenderbase's later dates are maturities). Realism: the two notes' equal 15.0 per cent read as
"slightly constructed, but a plausible market convention".

Determinism judge, pass 1 (isolated thread, Sonnet at medium, on 2e83c33f with the corrected prompt patched into its
brief; determinism_check_report.md): DETERMINISTIC on the call, FIX_NOW. Gate G method_or_model_selection over
statistical_rigor, analytical_non_defect, surface_read_dependency no, sole_data_defect no; Gate H domain pass, layers
pass, decisive_step analytical, a chain of four, one fact not enough. It reproduced 578 defaults, 80 houses, five and
45 houses in the portfolios, the pair rates (0.83 and 0.247 per cent) and the 39.85 per cent loss, and found the
textbook copula buying Kestrel Lane (0.34 against 0.86 in its fit). Findings and the one-pass fix:
1. Ageing unpinned (MP-RN-2 3.2 silent on whether the five years age the borrowers; held ages move each chance by
   about 0.2): 3.2 now says "Borrowers and loans grow older as the years pass" (SF16; the held reading keeps the call,
   SF16b).
2. Loss given default read as every closed workout (37.96 per cent), the golden's restriction to closed cohorts filed
   nowhere: 3.4 now takes the average "over every comparable default, those still in workout included" (SF17), a
   population, with how the open workouts end left to the record (recovery falls with workout length).
3. Ostvale's margin thin in one variant (the judge's dependence estimate with held ages, 1.02): closed by 1; with ages
   running on, every estimator pairing measured keeps Ostvale at 0.79 or under and Kestrel Lane at 1.18 or over.
4. Two-decimal figures reproduce only within the estimators' spread: the generator now computes the band over two
   default-rate tables (probit, smoothed cohort) and two dependence estimators (cluster random effect, pair-count
   moments) and the critical components and the note state it (checks.py K13 asserts both edges keep the call).
5. 81 company-years apart: Step-by-Step 1 now names the at-risk rule.
Also from the judge's linking note: a join on LEI alone found seven and 48 houses because some recent buyouts carried
no LEI; every buyout from 2015 now carries it (K12), so the reconstruction no longer turns on a fallback join.

Leak reader, read 3 (isolated, Sonnet at medium, on 076bb4b7 after the one-pass fix): questions 1 to 4 none; question 5
every MP-RN-2 sentence executes to the golden's construction, 3.2's ageing and 3.4's population included; question 6
an analytical choice ("the estimation work, hazards, correlation, tail probabilities, is modelling judgment, not a
decoded field or planted defect"); asked directly, "the standard does not name sector, country, factor, vintage or any
correlation estimator". Its notes: the tapes still showed "Excel" as creator (the namespace attribute on dc:creator
slipped the scrub; fixed); the equal 15.0 per cent and dates on both term sheets read as set by the request for
proposals, which they now say. Its "mild concern" that 4.2 and 3.4 nearly specify the method is the standard's own
general method (a Gaussian standing correlated as the record shows; every default in the average), rung 0's frame,
with nothing about which borrowers move together.

Determinism judge, pass 2 (the FIX_NOW re-judge, isolated thread on 076bb4b7): DETERMINISTIC, APPROVE. Gate G
method_or_model_selection with the censored loss as a secondary judgment, analytical_non_defect,
surface_read_dependency no, sole_data_defect no; Gate H domain pass, layers pass, decisive_step analytical, a chain of
five. It reproduced every golden figure within 0.01 at 600,000 paths with the golden's parameters (Kestrel Lane 1.318,
Ostvale 0.538, the year ends, the subordination needs), found only the sector and the house carrying excess joint
defaults (country, lender, vintage, currency and rating pairs sit at 0.185 to 0.206 per cent against a 0.198 baseline),
and ran the rivals: its own dependence estimate 1.15 and 0.54; a house share from 0.30 to 0.50 keeps Ostvale between
0.51 and 0.57; a 38.0 per cent loss gives 0.95 and 0.34 (both pass, Ostvale lower); open workouts imputed from closed
durations give 39.3 per cent and 1.15 and 0.50; the economy factor's profile interval averaged out gives 1.43 and
0.80. Its one optional pin, applied: a defaulted loan leaves the portfolio and is not replaced (SF18; its re-default
reading gave 2.86 and 1.99, neither note). Residual, stated in the answer blocks: the two-decimal figures move 0.1 to
0.2 across sound estimators, the band the critical components carry.

Leak reader, read 4 (on the final cut 2e2598bc, after the pass 2 pin): no leak; question 1 none (4.2 "names a
latent-factor structure but not how to estimate the correlation"); question 6 an analytical choice; no grouping,
sector or country structure in any filed sentence; prompt and standard agree. The answers are appended to
leak_check_report.md under the Solver's-eye read.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the call turns on the house-year dependence (checks.py R3a,
  R3b, R6); every textbook copula files Kestrel Lane and back-tests on the record (B1, 17 of 19 years inside the
  band); no document, column or sentence names the house (R1, D1); the one-fact hint executed literally lands the
  call with every figure off (R5, Kestrel Lane 5.56 per cent); each link of the chain moves the call or a critical
  component (R4); the closed-workout loss given default and the fund grain move every figure outside its bin.
- Mess neutral: the conformed pack gives the truth's 16,712 company-years exactly (K1), no loan unlinked (K2), the
  houses partition the panel as the truth's do (K3), the 2008 to 2019 workouts all closed (K4).
- Determinism: fifteen forks closed and asserted (SF1 to SF15); the verifier's independent road (pandas, a cohort
  table, moment estimators) lands on the call with the house component at 0.460 against 0.503 and Kestrel Lane at
  1.18 against 1.33.
- The pack (final cut 2e2598bc): thirteen files in three categories (spreadsheet, text, code); the Lenderbase CSV
  73,066 rows, the Dealtrail CSV 8,858 rows; two distractors named only in metadata.json; every file's source, pull date and licence
  in metadata.json; producer metadata clean; two builds byte-identical over eighteen files.
- The goldens: exactly the two requested files; one set of numbers across the note, the CSV, the chart and the four
  blocks (figures_check.py, 75 of 75).

## Tried and rejected

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
