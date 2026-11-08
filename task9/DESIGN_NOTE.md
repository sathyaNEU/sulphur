# task9 design note

## Draw

1. Card: `.claude/skills/fingerprint/cards/task9.json`, architecture 7, registered 2026-11-08; architecture 6 moved into
   the card's lineage with its fate (landed on the platform: both runs rebuilt sponsor ownership, fitted a house factor
   and bought Ostvale). At the author's word ("make it more complex, multi layered") architecture 7 keeps architecture
   6's world and records and moves the deep step; the prompt's shell is redrawn (whether | the | csv+docx against what |
   in | csv+docx). Guard on the registered card: WARN only (objective and Gate G overuse; the slot's assigned objective
   is forecasting). Redrawn at the final heart screen: decisive generator G14 (BLOCK against task7 v6, registered after
   this card) to G2 (the recovery is read at the default's grain while what sets it lives at the house-year's).
2. Pairing: Quantitative Finance, task type derivative pricing (the vocabulary's volatility-derivatives-pricing key: the
   price of a structured credit note is its loss distribution), objective Forecasting. The headline is each senior
   note's chance of any loss of principal over 2027 to 2031, which decides the call.
3. World, people and furniture: as architecture 6 (Stichting Pensioenfonds Havenbedrijf en Logistiek through Kadeweg
   Fiduciair Beheer; Kestrel Lane Credit Partners and Ostvale Capital; Lenderbase with its workout file; Dealtrail; Ilse
   Lips, Damian Schenkel, Liza Dekker in document control lines only). The world's truth changes in three places:
   a sponsor house in a bad year stops putting money into its companies' restructurings, so its clustered defaults
   recover less and take longer to work out (world.py REC_H, DUR_H; the economy's year moves how many default, not what
   a default recovers); Kestrel Lane lends to seven houses' stronger credits (14 loans a house, most of each house's
   book, houses with ordinary records); Ostvale lends to weaker credits across many houses (2 loans a house) and
   offers 13.0 per cent subordination against the 15.0 its term sheet says Kadeweg's request set.
4. Candidates: Kestrel Lane's senior note, Ostvale's senior note, or neither.
5. Quantity: for each note, the probability that cumulative credit losses on its portfolio exceed its subordination
   (Kestrel Lane 15.0 per cent, Ostvale 13.0) before the end of 2031, the portfolio static (MP-RN-2 3.2), each
   default losing what is not recovered by the end of its workout (3.4), default and recovery taken from the record of
   comparable loans, standings correlated and recoveries with them as far as the record shows (4.1, 4.2); the fund buys
   the note under 1 per cent, the lower if both are, neither if none is (2.1, 2.2).
6. Shape: 02, a forecast across periods: each note's chance of a loss by the end of each year (10 figures, one
   decimal), each note's five-year chance (2), each portfolio's expected credit loss over the five years (2, one
   decimal), the subordination for 1 and 0.5 per cent (4, whole per cent rounded up), the call, and the
   loss-exceedance chart.
7. Data-native sentence: a buyout house decides from one partnership's view of its year whether to put more money into
   each of its companies when they breach, so the companies it holds fail in the same years, and in those years it lets
   them go rather than fund their restructurings, so the lenders sell or wind them up and recover less, slowly; the
   workout file keeps each default's own recovery and the deal file each company's buyers, no file joins a recovery to
   the house-year it happened in, and each manager's tape holds only its own slice of a house's book.
8. Abstraction sentence, written against the nearest builds and found not to be the same: architecture 6 (this slot)
   prices a shared owner's year into the default dependence only; task4 corrects a slope for a covariate's
   source-specific recording error; task7 values a rescue by the write-off it keeps off borrowers who draw on it. Here
   the severity of each loss is conditioned on the latent shared shock that also clusters the counts, a property of the
   owner-year across its whole book that a portfolio holding a slice of the book cannot observe in its own defaults, so
   it is inferred owner-year by owner-year from the record and carried as a shock; no build on file conditions a loss's
   severity on a latent shock measured at a grain the decision's portfolio does not share.
9. Shell: question form whether ("Should the fund buy ... or neither"), second sentence opening on the committee note,
   rounding sentence opening "Chances"; deliverables docx and csv; the asks coarsened to the precision the honest
   family shares (one decimal for chances, whole per cent for subordination).
10. Furniture: forum trustees_or_governors (the fund's board of trustees decides the purchase on its investment
   committee's advice), forcing purchase_order_or_contract (both offers close on 12 March 2027), org
   financial_institution (a pension fund), role portfolio_manager (Kadeweg's head of credit runs the credit sleeve and
   asks). Stump strategy `other`: the decisive move is a severity conditioned on a latent shared shock at the owner's
   grain, which no strategy key names; Gate G forecasting, pattern G2 decisive with G17 and G13 (the recovery is read
   at the default's grain while what sets it lives at the house-year's across its book; the horizon is five years of a
   pool, the record a year at a time of single loans).
11. As of 17 February 2027, the day after the Lenderbase and Dealtrail extracts were pulled (16 and 15 February,
   with the fourth quarter of 2026 filed); the investment committee meets on 25 February, the board of trustees on
   4 March, and both offers close on 12 March 2027.

## Default path

The pipeline a competent credit quant builds from the prompt's words and the files' grain, the field's own method for
the deciding quantity in it (stumping 1.1b).

1. Conform the records: Lenderbase's latest submission of each loan-quarter, its pre-2019 and post-2019 codes, the
   workout file's recoveries in one unit, both tapes in euros at the ECB rate of 31 December 2026 and on Lenderbase's
   sectors through the crosswalk.
2. Company-years at risk 2008 to 2026 and their defaults (16,712 and 578); one-year default chance by rating and
   years since the buyout.
3. Dependence, the field's method: a one-factor Gaussian copula fitted to the record's yearly default rates (0.109),
   then the agencies' industry factor (0.059).
4. Loss given default, the field's method: the average shortfall over the default years whose workouts have all
   closed, 42.7 per cent (the open workouts are the long ones; MP-RN-2 4.1 keeps them in).
5. Simulate five years for both portfolios at their subordination: Kestrel Lane 0.1 per cent, Ostvale 5.9 per
   cent; MP-RN-2 2.2 buys Kestrel Lane.

Ends on: buy Kestrel Lane's note at a 0.1 per cent chance of loss (Ostvale's fails at 5.9 per cent)
Golden: buy neither note: Kestrel Lane's chance is 3.9 per cent and Ostvale's 7.8 per cent, both over the test

## Stump sentence

A competent solver who conforms the records, fits the field's copula and averages the closed workouts' shortfall
buys Kestrel Lane's note at 0.1 per cent, and the arch 6 runs' route (the sponsor house's year added to the
dependence, one average loss) still buys it at 0.7; the step that lands it there is pricing every default at one
recovery, when the defaults that cluster in a sponsor house's bad year recover 74.9 per cent alone against 44.1
per cent with three or more others; a solver who sees that and carries the table to the notes by counting each
default's co-defaults among the note's own loans buys Ostvale at 0.1 per cent, because the table's counts run over
a house's whole book (a median of 13 companies) and Ostvale holds 2 of each house's; with each default's
recovery tied to its house-year's inferred shock Kestrel Lane's chance is 3.9 per cent and Ostvale's 7.8, both
over the test, and the fund buys neither.

## Deep reasoning

Task type: volatility-derivatives-pricing (Quantitative Finance, derivative pricing: a structured note's price is its loss distribution), a task type the taxonomy tags for Forecasting & Predictive Modeling; the forecast is each note's chance of losing principal over 2027 to 2031.
Domain test: the deciding quantity is a senior tranche's tail probability, the probability that a portfolio's credit loss passes its attachment, where loss is the sum of defaults times their loss given default; the field's object is the joint distribution of default and recovery, and the decisive judgment is that the severity is conditioned on the same latent sponsor shock that clusters the counts, a state of the sponsor's whole book; with patients and wards in place of loans and houses there is no tranche, no attachment and no owner whose bad year sets both how many fail and what each failure costs.
Swap: "should the hospital trust buy cover from insurer A or B for its 2027 malpractice claims" keeps a tail probability but loses the sponsor house that both clusters the defaults and walks away from their restructurings; nothing would tie a claim's size to a shared shock measured across a book that each policy holds only a slice of, and the call stops reading the same.
Layer 1: the systems produce it: Lenderbase resubmissions of a loan-quarter (latest kept), the 2019 change of status, purpose and rating codes, LEIs only from 2012 (older loans joined by name), recoveries reported in per cent by some lenders and as fractions by others, Dealtrail buyers named by fund or by house, withdrawn deals and add-ons, the managers' tapes in local currencies and on their own industry scales; each is neutral on the call (K1 to K3, SF21 asserted) and none is placed to be caught.
Layer 2: estimation_fit: the loss given default enters the tail through its dependence on the shocks that cluster the defaults; the methodological choice is what each default's recovery is taken to be: one average (closed workouts or mature cohorts), one tied to the economy's year, one read off the co-defaults the note itself would see, or one tied to its sponsor house's year inferred from that house-year's own defaults across the house's book.
Decisive step: each default's recovery is regressed on its house-year's shock, a latent quantity inferred as a posterior mean from the house-year's defaults across the house's whole book against the rates its companies' ratings, ages and sector-years expected, over the cohorts whose workouts have all closed, and the forward simulation draws each default's recovery from the same shocks that drew it, whatever share of the house's book the note holds.
Not semantics: every field read right (the 2019 code change, the per-cent and fraction recoveries, the open workouts, the buyers' names, the tapes' scales) still leaves a solver pricing every default at one recovery: no field links a recovery to a house-year, the deal file and the workout file share only the borrower, and the mean recovery reconciles to the closed workouts; and a solver who links them still has to decide what the recovery responds to, the co-defaults a note sees or the house's state.
Not rule application: MP-RN-2 files the WHAT (3.4 each default loses what its workout does not recover, 4.1 default and recovery from the record with its open workouts, 4.2 standings correlated and recoveries with them as far as the record shows) and nothing filed says which shock recovery moves with, at which grain, or how a latent shock is read. Enumerated family (one average over closed workouts or mature cohorts; a link to the economy's year; the record's co-default table carried to each note's own loans, as cells or a line; the same counts over each house's whole book; a link to the house-year's shock, inferred against the sector-year's or the year's rates, with or without the year's shock, under the cluster or the pair-moment dependence, fitted on the closed cohorts or on every closed workout): three calls (Kestrel Lane, Ostvale, neither); standing family (the house-state recoveries): 1.5 to 4.1 per cent for Kestrel Lane and 2.3 to 7.9 per cent for Ostvale, every one over the test, the call neither; the ruling-out is loud only to a solver who reads recovery against the house-year and asks what share of the house a note holds.
Analyst test: a strong analyst who conforms Lenderbase, rebuilds sponsor ownership from Dealtrail, fits a survival model and a market, sector and house copula, takes one censoring-corrected recovery and simulates both static portfolios buys Kestrel Lane's note at 0.7 per cent, the default path's Ends on (the field's copula without the house files it too, at 0.1); on the generator's clean truth the same route files the same call (checks.py R3d).
Estimand: MP-RN-2 2.1, 2.2, 3.2, 3.4, 4.1 and 4.2 (phl_rated_note_standard_2026.pdf): population each note's portfolio as on its tape, outcome the chance that cumulative loss passes the note's subordination by the end of 2031, window 2027 to 2031 drawn from the record's conditions, unit per cent, comparison each note against 1 per cent and the lower of two that pass.
No decoy: nothing is planted: the workout file is Lenderbase's own, the deal file Dealtrail's, the term sheets the managers'; no memo, rating report or stakeholder figure states a chance of loss or a recovery by house, and no file exists to carry the wrong answer.
No certified replay: the method is not recovered by reproducing a published figure; no file states a note's chance, a loss given default or a recovery link.
Chain: (1) defaults cluster by sponsor house and year (same house, sector and year pairs default together 0.84 per cent of the time against 0.25 across houses), so the house's year enters the dependence and the tail is a house-year event; (2) on the closed 2008 to 2019 cohorts the defaults that cluster in a house's year recover less (74.9 per cent alone against 44.1 with three or more others) while the economy's year does not lower recovery (-0.061 per unit of its shock), and the clustered defaults' long workouts are the open ones in the later cohorts; (3) those counts run over each house's whole book (a median of 13 companies in a defaulting house-year) while Ostvale holds 2 of a house's companies and Kestrel Lane 14, so the recovery belongs to the house-year's state, not to the co-defaults a note sees, and is carried by the house-year's latent shock; (4) each house-year's shock is inferred from its book's defaults against its companies' expected rates and recovery regressed on it over the mature cohorts (0.298 per unit, intercept 0.953); (5) the forward simulation draws each default's recovery from the shocks that drew it, and Kestrel Lane's chance is 3.9 per cent and Ostvale's 7.8: neither note is bought.
Judgment: the joint model of default and recovery under a latent shared shock measured at the sponsor's grain: the house-year shock is a property of the house's whole book, so a note holding two of its companies cannot read it from its own defaults; it is inferred by its posterior mean given the house-year's default experience under the fitted copula, which makes the regression of recovery on it a regression calibration, estimated on the cohorts whose workouts have closed so the long open workouts of clustered defaults do not bias it; the record shows each piece: the co-default table over whole books (V1), the books' size against the tapes' slices (V4), and the closed-workout link lifted (intercept 0.991 against 0.953, because the later cohorts' closed workouts are the quick ones).
Hidden by: the rows in view mimic the wrong structure three times: the economy's year shows recoveries no lower in bad years (-0.061 per unit; a bad economy brings defaults from houses having ordinary years), which confirms one average to a run that tests the textbook downturn link; the record's co-default table (lone 74.9 per cent against 44.1) displays the clustering effect, but over whole books, a sampling property the notes do not share, so a run that carries its regressor to a note's own loans prices Ostvale's defaults as lone ones; and the pooled recovery reconciles to the closed workouts, whose later cohorts hold only the quick cases.
After the notice: once a run has seen that clustered defaults recover less, three inferences remain: (1) the recovery follows the house's state across its whole book, not the co-defaults inside a note: counting co-defaults among a note's own loans, the obvious way into a portfolio simulation, buys Ostvale at 0.1 per cent (a line in the count, 0.8), so the state has to be carried by a latent shock inferred from the record's whole-book defaults (or the whole book simulated, which lands the same call); (2) the slope on that latent shock is a regression on its posterior mean fitted on the cohorts whose workouts have closed: a fit on every closed workout drops the open long workouts and lifts every recovery (Kestrel Lane 3.1 per cent against 3.9); (3) the same shocks draw default and recovery in the simulation, so the tail carries the clustered defaults at their low recoveries.
One-fact test: the likeliest hint ("recoveries are lower in bad years") invites the textbook downturn link to the economy's year, which the record shows flat or reversed (-0.061) and which leaves Kestrel Lane at 0.2 per cent and bought; the stronger hint ("the sponsor house's bad year cuts recoveries") still leaves the grain to judge (the co-defaults a note sees buy Ostvale at 0.1), the latent shock to infer house-year by house-year, the censoring to handle and the shocks to carry into the copula simulation.
No replay: the call does not re-derive any published figure, and no stated number in the pack is wrong.
Pinned: run on the cut pack (analysis.py, checks.py, verify.py): the house-year shock inferred against the sector-year's or the year's rates, with and without the year's shock, under the cluster or the pair-moment dependence, a cohort table or a probit for the default rates, the record's co-default counts over each house's whole book (cells or a line), and verify.py's independent Gauss-Hermite inference: every one files neither, Kestrel Lane between 1.5 and 4.1 per cent and Ostvale between 2.3 and 7.9; one average loss, the closed-workout average and the economy's-year link file Kestrel Lane; the co-default counts carried to each note's own loans file Ostvale (cells 0.1, line 0.8), ruled out by the record's grain (V4: the counts run over books of a median 13 companies, Ostvale holds 2 of each) and by the same default recovering differently according to which note holds it; a link fitted on every closed workout drops the open workouts MP-RN-2 4.1 keeps and moves every figure down (SF8).
Run forecast: method shortcut at rung 1 (one censoring-corrected recovery for every default, which the closed workouts confirm; a self-confirming check), the arch 6 runs' route; a run that suspects recovery moves with the cycle stops one inference short at rung 2 (the economy's year, flat), an unfinished chain; a run that finds the house-year table and carries it to each note's own loans buys Ostvale at 0.1 per cent at rung 2b, dismissing its own evidence that the table's counts are over whole books its tape holds two companies of.
Strategy label: WORKS IN FORM (Part A, variance beyond sampling noise and Banking 07 correlated defaults, live form: the component the standard model omits, here the recovery's loading on the shared owner's shock, estimated from the record at the owner's grain, never filed).
Lesson: in a portfolio's tail the severity of a loss can ride the same latent shock as the count, and that shock belongs to the shared owner's whole book, which a portfolio holding a slice of it cannot see in its own defaults; a severity averaged over the record prices the tail at the average state, one read off the portfolio's own co-defaults prices a thin slice as safe, and the shock has to be inferred owner-year by owner-year from the record's own counts; no build on file conditions severity on a latent shock measured at a grain the decision's portfolio does not share.

## Survivor anatomy

Actor: the deciding property, how a default's recovery moves with its sponsor house's year across the house's whole book, has no column in any file; it is a relation between a workout's recovery, the house that held the borrower (through Dealtrail) and the other defaults of that house's book in the same year.
Link: each recovery is tied to its house-year only through the borrower, a key the workout file and the deal file each carry for their own reasons, and the house's book only through the borrowers of the performance file; no sentence joins a recovery to a house, a book or a year's shock.
Reflex: the field's methods for the deciding quantity, a Gaussian copula with a censoring-corrected loss given default (rung 1, the arch 6 golden) and a downturn link to the economy's year (rung 2), file Kestrel Lane (Ends on).
Back-test: the one-average route reconciles to the closed workouts and its copula reproduces the record's yearly, sector-year and house-year default counts (B1); the downturn regression finds no slope, which confirms the average; the in-portfolio co-default route reproduces the record's own table cell by cell.
Second use: every file the step reads is in the pack for its own reason: the workout file is the loss given default's source (MP-RN-2 4.1), the deal file the house dependence's (arch 6's rung), the performance file the population and each house's book.
Shock: nothing moves visibly: the recovery averages agree with the closed workouts; sorted on rating, sector diversity, house count or pooled chance, Kestrel Lane is the safer note, and Ostvale's thin slices of each house make it look the diversified one; only the joint tail at the house's grain reverses both.
Pins: MP-RN-2 files the WHAT (each default's own loss, the record's conditions, standings and recoveries correlated as the record shows) in the fund's own standard; no filed sentence names a house, a sponsor, a year shock, a cluster, a book or a link (asserted: checks.py D1, L1).

## Readability screen

Seven tests per rung: 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a column, key or
marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or corpus scores
the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of a reported
figure; 7 a file the step alone reads.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 one-factor and industry copula, one average loss: Kestrel Lane | MP-RN-2 4.2 | yearly and sector rates | yes, the field's copula | the yearly counts back-test | no | a fit | none | readable |
| 1 the house's year in the dependence, one average loss: Kestrel Lane | 4.2 "as the record shows" | the deal file's buyers | yes, the arch 6 runs took it | the house-year counts | no | a cluster fit | the deal file | readable |
| 2 recovery tied to the economy's year: Kestrel Lane | 4.2 "and so is what lenders recover" | the default dates | yes, the downturn link | the slope reads flat | no | one regression | none | readable |
| 2b recovery read off the co-defaults among the note's own loans: Ostvale | 4.2 "and so is what lenders recover" | the deal file's buyers and the workout file | a group-by of recovery on co-defaults | the record's table reproduces | no | a table carried to the simulation | the workout file | readable |
| 3 (decisive) recovery tied to the house-year's inferred shock across its whole book, carried into the simulation | no sentence names a house, a book, a year shock or a cluster | no column joins a recovery to a house-year or a house's book | no: the reflexes are one average, the downturn link and the note's own co-defaults | nothing scores it; the average reconciles and the in-portfolio table reproduces | no | not linear: a posterior per house-year, a regression calibration and a joint simulation | the workout file is the loss given default's source | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | any loss in the five years | the loss at the end of 2031 | a loss in any one year | same figure | cumulative losses never fall (asserted) |
| SF2 | the portfolio | static, repaid loans replaced by identical ones | runoff | filed | MP-RN-2 3.2 (asserted) |
| SF3 | a default's loss | its own shortfall by the end of its workout, booked at default | one average | moves the call | MP-RN-2 3.4 and 4.2 (asserted) |
| SF4 | dependence | standings correlated as the record shows, recoveries with them | standings only | moves the call | MP-RN-2 4.2 (asserted) |
| SF5 | conditions | the record's | stressed | filed | MP-RN-2 4.1 (asserted) |
| SF6 | the FX date | 31 December 2026 | 30 December | same figures | asserted |
| SF7 | default | Lenderbase's | rating-agency default | filed | MP-RN-2 3.3 (asserted) |
| SF8 | the link's sample | the 2008 to 2019 cohorts, all closed | every closed workout | same call | asserted |
| SF9 | the age clock | years since the buyout | loan age | same call | asserted |
| SF10 | the sponsor grain | house-year | fund-year, lasting | fits worse | log-likelihood (asserted) |
| SF11 | choosing between two | the lower chance | the higher spread | filed | MP-RN-2 2.2 (asserted) |
| SF12 | subordination needed | the five-year loss quantile, rounded up | to nearest | same figures | the prompt; asserted |
| SF13 | weights | euro par | loan count | same call | asserted |
| SF14 | default chance | one-year | cumulative | filed | MP-RN-2 4.2 (asserted) |
| SF15 | relending | to the same borrower | new borrowers | filed | the term sheets (asserted) |
| SF16 | ageing | borrowers and loans grow older | frozen at the tape | same call | MP-RN-2 3.2; asserted |
| SF17 | open workouts | in the record | dropped | same call | MP-RN-2 4.1 (asserted) |
| SF18 | a defaulted loan | leaves, not replaced | replaced | filed | MP-RN-2 3.4 (asserted) |
| SF19 | the house shock's basis | against the sector-year's rates | against the year's rates | same call | asserted |
| SF20 | the year's shock in the link | in | out | same call | asserted |
| SF21 | recovery units | per cent and fractions as one share | mixed | same figures | asserted |
| SF22 | the co-defaults a recovery moves with | the house-year's across its whole book | the note's own loans | moves the call (Ostvale) | the record's counts run over whole books (V4) and one default recovers once whichever note holds it; asserted (R7, R8) |
| SF23 | expected credit loss | the mean five-year loss as a share of par, each default's own shortfall | a note's expected loss | filed | the prompt and MP-RN-2 3.4 and 3.5 (asserted) |

## Ladder

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | one-factor and industry copula, one average loss of 42.7 per cent | Kestrel Lane at 0.1 per cent | the record's same-year house pairs |
| 1 | the house's year in the dependence, one average loss | Kestrel Lane at 0.7 per cent (under the pair-moment dependence 0.67) | the clustered defaults' recoveries |
| 2 | recovery tied to the economy's year (-0.061 per unit) | Kestrel Lane at 0.2 per cent | the house-year's recoveries |
| 2b | the record's co-default table carried to each note's own loans (cells; a line in the count) | Ostvale at 0.1 per cent, Kestrel Lane 1.8 (line: 0.8 and 2.0) | the grain: the counts run over whole books of a median 13 companies and Ostvale holds 2 of each |
| 3 (golden) | recovery tied to the house-year's inferred shock (0.298 per unit) over the closed cohorts, the shocks carried into the simulation | neither: Kestrel Lane 3.9, Ostvale 7.8 | |

- **Margins.** The golden puts Kestrel Lane at 3.9 per cent and Ostvale at 7.8 (asserted at 1.5 times the bar);
  every sound house-state route keeps both over 1.5 per cent; every rung without a house-linked recovery
  keeps Kestrel Lane under 0.7 per cent; rung 2b keeps Ostvale under 0.8.
- **Position.** Three layers act jointly: the house's year in the dependence alone files Kestrel Lane, the recovery
  link needs it, and the link read at the note's grain files Ostvale; only the house-year's state, carried as a
  shock, files neither.
- **Worth.** The decisive step moves the call from Kestrel Lane (or Ostvale) to neither and Kestrel Lane's chance by
  about 6 times against the arch 6 route.

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | each note's tape | filed, MP-RN-2 3.1 and 3.2 |
| 2 Unit of account | a note | filed |
| 3 Attribution window | 2027 to 2031 | filed, MP-RN-2 2.1 |
| 4 As-of dating | the extracts of February 2027 | C1 |
| 5 Version basis | MP-RN-2 | filed |
| 6 Denominator | par | filed, 3.5 |
| 7 Weighting | euro par | filed (SF13) |
| 8 Window length | five years | filed |
| 9 Boundary inclusivity | below 1.0 per cent | filed, 2.1 |
| 10 Rounding path | one decimal for chances, whole per cent rounded up for subordination | the prompt (SF12) |
| 11 Tie-break | the lower chance | filed, 2.2 |
| 12 Maturity and censoring | open workouts in the record, the link on the closed cohorts | filed 4.1; C1 (SF8, SF17) |
| 13 Order of operations | conform, link, fit, simulate | C1 |
| 14 Row order | latest submission | C1 |
| 15 Duplicate resolution | latest submission of a loan-quarter | C1 |
| 16 Identity normalisation | LEI or name | C1 |
| 17 Netting against gross | loss net of recovery | filed, 3.4 |
| 18 Dimensional units | recoveries as shares | C1 (SF21) |
| 19 Code and status semantics | the 2019 codes | C1 |
| 20 Integerisation | none | n/a |
| 21 Clause scope | MP-RN-2 2 to 4 | filed |
| 22 Forward window contents | the record's conditions | filed (SF5) |

## Literal reader

Executed word for word, MP-RN-2 2.1 to 4.2 price each note's chance that its static portfolio's losses, each default
losing what its own workout does not recover, pass its subordination by the end of 2031, with default and recovery from
the record of comparable loans, its open workouts included, standings Gaussian and correlated, and recoveries with
them, as far as that record shows; the step the text leaves open is how the record shows recovery moving with the
standings, and every route that reads it against the house-year that clusters the defaults, at the grain the record
measures it, files neither, while one average and the economy's year price the clustered defaults at an ordinary
recovery and a note's own co-defaults price a thin slice of a house as lone defaults. SF1 to SF23 close every term.

## Oracles

None. No file states a note's chance, a loss given default by house or year, or a recovery link; the EURIBOR curve
and the matching portfolio's cash flows (distractors) rank nothing; the term sheets offer the subordination only.

## Ask sheet

Asks ride the joint tail and the recovery the house's state sets: each note's five-year chance (2), its portfolio's
expected credit loss (2), its chance by each year end (10) and its subordination for 1 and 0.5 per cent (4), eighteen
figures with the call. The expected loss carries the recovery link even where Ostvale's spread-out tail does not: one
average recovery files 5.0 and 7.7 per cent, the note's own co-defaults 5.0 and 4.9, the
golden 5.7 and 8.2. The second judgment on the asks is how each house-year's
shock is read (against the sector-year's rates, the golden, or the year's alone, which lands the call with every
figure lower) and how its slope is fitted (the closed cohorts, or every closed workout).

| Ask | Figures | Deep-step output it reads | Second judgment | Shallow run against the golden | Landed run's risk | Mess on its path |
|---|---|---|---|---|---|---|
| 1 the call | 1 | the joint tail | the grain | Kestrel Lane (or Ostvale at rung 2b) | none | the code change |
| 2 five-year chances | 2 | the joint tail | the shock's basis | both differ | both lower | the recoveries' units |
| 2b expected credit losses | 2 | each default's recovery at its house's state | the link's sample and basis | both differ | both lower | the recoveries' units |
| 3 chances by year end | 10 | the joint tail | the shock's basis | most differ | most lower | none |
| 4 subordination needed | 4 | the loss quantiles | the shock's basis | all differ | some lower | none |

| Ask figure | Golden | Shallow (one average loss) | Deeper (own co-defaults) | Cracker (house shocks against the year's rates) |
|---|---|---|---|---|
| the call | neither | miss | miss | keep |
| five-year chances, Kestrel Lane and Ostvale | 3.9 and 7.8 | miss | miss | miss |
| expected credit losses, both portfolios | 5.7 and 8.2 | miss | miss | miss |
| chances by year end, 2027 to 2031, both notes | ten figures | keep 1 of 10 | keep 1 of 10 | keep 4 of 10 |
| subordination for 1 and 0.5 per cent, both notes | four figures | keep 2 of 4 | miss | keep 3 of 4 |

- Shallow keep: 16.7 per cent of ask weight (the arch 6 route the platform's runs took; the default path, the
  field's copula without the house, keeps 22.2; the free cells are Ostvale's 2027 and 2028 chances and its two
  subordination figures, which every route shares because Ostvale's spread-out tail barely moves with the recovery
  link).
- Pair ceiling: 38.3 (the landed run C = 54.4, the shallow run S = 22.2; the deeper run D = 22.1, a
  landed and deeper pair 38.2).
- Measured by: generator/ceiling.py on the cut pack.

## Prompt contract

What the author's voice rewrite may not drop or change:
- The question: whether the fund should buy Kestrel Lane Credit Partners' senior note or Ostvale Capital's for its
  matching portfolio, or neither, under the 1 per cent test and the lower-risk rule.
- Deliverables: ic_note_senior_notes_2027.docx (the recommendation, each note's five-year chance, its portfolio's
  expected credit loss, the subordination for 1 and 0.5 per cent, the exceedance chart with both notes' subordination
  marked) and senior_note_loss_by_year.csv
  (each note's chance of a loss by each year end 2027 to 2031).
- Units and rounding: chances in per cent to one decimal; expected losses in per cent of par to one decimal;
  subordination in whole per cent of par rounded up.
- Never add: a sponsor, a house, a recovery, a correlation, a cycle, a downturn, a cluster, a book, a slice, or any
  method word.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the call turns on the recovery the house-year's state sets,
  carried at the house's grain (checks.py R3b, R4, R6, R7, R8); every route without a house-linked recovery files
  Kestrel Lane and its copula back-tests on the record (R3a, R3d, R3e, B1, 17 of 19 years inside the band); the
  record's co-default table carried to each note's own loans files Ostvale (R7), the same table over each house's
  whole book files neither (R8), and the grain that separates them is in the record (V4); no document, column or
  sentence names the house, the book or the link (R1, D1); the one-fact hint executed literally misses the call (R5);
  the closed-workout link, the shock's basis and the dependence estimator move every figure and keep the call (SF8,
  SF19, SF20, K13).
- Mess neutral: the conformed pack gives the truth's 16,712 company-years exactly (K1), no loan unlinked (K2), the
  houses partition the panel as the truth's do (K3), the 2008 to 2019 workouts all closed (K4), recoveries in per cent
  and fractions read as one share (SF21).
- Determinism: twenty-three forks closed and asserted (SF1 to SF23); the band refits the link under two default-rate
  tables, two dependence estimators and three shock bases (Kestrel Lane 1.5 to 4.0 per cent,
  Ostvale 2.3 to 7.8), every member over the test (K13); the verifier's independent road (pandas, a
  cohort table, pair moments, its own Gauss-Hermite shocks) lands on the call inside the band (Kestrel Lane
  1.60, Ostvale 2.40); the world's own process run forward over the record's years puts the two notes at 2.97 and
  4.51 per cent, inside the band and over the test (T1).
- The pack (final cut 3ec3c9ed): thirteen files in three categories (spreadsheet, text, code); the Lenderbase CSV
  73,066 rows, the Dealtrail CSV 8,858 rows; two distractors named only in metadata.json; every file's source, pull
  date and licence in metadata.json; two builds byte-identical over eighteen files; the container gate
  (audit_containers.py) 0 FAIL, 0 WARN over the pack, the golden and both zips.
- The goldens: exactly the two requested files; one set of numbers across the note, the CSV, the chart and the four
  blocks (figures_check.py).

## Stage 4

leak.py on target.zip bed0980b and again on the final cut 7c395ae0 (--asof 2027-02-17): REVIEW, no LEAK, the same
lines both times. The main thread's rulings, one line each:

- Sweep 3, golden figures in the documents: 15.0 and 13.0 are the subordination each manager offers, an input the
  call reads; 2.5 is Kestrel Lane's obligor limit; 1.0, 2.2 and 3.5 are MP-RN-2's test and section numbers; the
  standard shares the call's words because it states the test the call answers; harmless.
- Sweep 4, stump-paragraph terms in the term sheets and MP-RN-2 (recovery, default, record, workouts, sponsor,
  companies, million): "sponsor" appears only in "sponsor-backed", the asset class's own name; MP-RN-2 3.4, 4.1 and
  4.2 file the WHAT (each default's own loss over its workout, the record with its open workouts, standings and
  recoveries correlated as the record shows); no sentence names a house, a book, a grain, a shock or a link;
  harmless.
- Sweep 9, dates after the setting: Lenderbase's 19,066 are its maturity_date column alone (no submission, report or
  resolution date passes the pulls), the tapes' are maturities, the EURIBOR file's its forward dates; harmless.
- Sweep 11, the prompt's shell quota and its two files named up front: voice warnings only; harmless.

guard.py on the final cut 7c395ae0: heart WARN (objective and Gate G overuse; nearest driver this slot's own architecture 6 at
0.07), not BLOCK; surface exit 0 with one promoted pair, task9 against task67, adjudicated side by side: task67 is a
supply-chain duty-establishment forecast priced from a fixed-plus-variable cost structure on delivery extracts; it
meets this build only on the card labels (gap objective, pattern G2, Gate G forecasting), with another domain, data
structure and driver; not a duplicate. "Ireland Collateral" is PDF text ("incorporated in Ireland" running into the
next row), not a persona.

Leak reader, read 1 (isolated, Sonnet at medium, prompt and pack only, on bed0980b): question 1 none for the decisive step;
the nearest sentences it found, MP-RN-2 3.4, 4.1 and 4.2, "name the model family (Gaussian latent-factor default and
recovery, correlated, with open workouts included)", the filed WHAT the literal reading needs (without 4.2's
recovery clause the golden's link is a method nothing in the pack forces, the reason architecture 5 came back), and
nothing on which shock recovery moves with or at which grain; question 2 none; question 3 none (the sector crosswalk
a vendor's utility); question 4 none; question 5 every MP-RN-2 sentence it quoted executes to the golden's
construction (portfolio date, static pool with ageing, ECB rate of the cut-off, Lenderbase's defaults, each default's
own loss booked at default, the record with its open workouts, Gaussian standings correlated and recoveries with them);
question 6 an analytical choice (the default and recovery correlation estimated from the record, the open workouts),
with 4.2 read as writing down the model's form, ruled as above. It took Dealtrail and the LEI extract for decoys. Its
one finding, fixed: Ostvale's term sheet sized its Class A notes at 85 per cent of par against the 13.0 per cent
enhancement it states (EUR 1,575.0 million on 1,853 million of collateral); both term sheets now size the notes as par
less the stated enhancement, asserted (K19). Not changed: the standard's technical register (a fund's standard for
rated notes states its model), the Ostvale sentence on the thinner enhancement and wider margin (a term sheet answering
a request for proposals), the crosswalk.

Leak reader, read 2 (isolated, Sonnet at medium, prompt and pack only, on the final cut 7c395ae0): question 1 none (the
nearest, MP-RN-2 4.2, "hands over the model family (Gaussian-copula, correlated recovery) but not the estimation");
questions 2 to 4 none; question 5 every MP-RN-2 sentence executes to the golden's construction; question 6 an
analytical choice ("the standard states the model's form but not how to estimate it, so this is not rule
application"), the cleaning texture, not the stump; both term sheets internally consistent (Kestrel Lane EUR 1,597.5
million on about 1,879 million at 15.0 per cent, Ostvale 1,612.1 million on 1,853 million at 13.0); every sweep line
harmless; realism: "reads like a real sourcing exercise", the two tapes' schemas and scales different, the ECB file a
genuine download's thirty currencies.

Determinism judge, pass 1 (isolated thread, Sonnet at medium, spawned by the main session from the judge agent's brief,
on bed0980b; determinism_check_report_pass1.md): DETERMINISTIC on the call, FIX_NOW. Gate G method_or_model_selection
(the dependence structure and the recovery link, with censoring), analytical_non_defect, surface_read_dependency no,
sole_data_defect no; Gate H domain pass, layers pass, decisive_step analytical, a chain of five, the nearest one-fact
hint ("defaults and recoveries cluster by sponsor house-year") shortening the task without making it routine. It
reproduced the 578 defaults (345 "D" and 233 "Defaulted"; 500 workouts closed, 78 open), the 80 houses, both tapes
(98 loans with seven houses of 14, 100 with 66 houses of at most two), the same-house same-year pair count (665) and
the recovery gradient by co-defaults; it ruled every rival that buys Kestrel Lane or Ostvale out by named data (the
whole-book counts against Ostvale's two loans a house) and the closed-cohort fit a licensed choice. Findings and the
one-pass fix:
1. Ostvale's Class A notes at 85 per cent of par against its 13.0 per cent enhancement (the leak reader's finding):
   fixed as above (K19); the call, every figure and the asks unchanged, since the golden always read 13.0.
2. The one-decimal figures come from one estimator inside the stated band: judged against the band and the call they
   are deterministic; a sound run on another estimator can miss a decimal. Not changed: the band stands in critical
   component 4 and the note's Pinned line, every member over the test (K13), and the world's own process sits inside
   it (T1).
3. Its own reading of the co-default table (68.5 per cent alone against 43.4 with three or more, "unweighted") did not
   match 74.9 and 44.1; the golden's cells reproduce exactly with the co-defaults counted on the company-year panel or
   in the workout file over the 2008 to 2019 cohorts; critical component 2 now pins the reading (a default's sponsor
   house in the calendar year of its default).

Determinism judge, pass 2 (the re-judge; isolated thread, Sonnet at medium, on the final cut 7c395ae0;
determinism_check_report.md): DETERMINISTIC, APPROVE. Gate G method_or_model_selection, analytical_non_defect,
surface_read_dependency no; Gate H domain pass, decisive step analytical, a chain of five, no single hint making it
routine. Its own road reproduced the call and put every figure inside the stated band: recoveries in mixed units read
as one share (the 2008 to 2019 closed loss 43.0 per cent against 42.7), a lone default recovering 72.3 per cent and
one with three or more co-defaults 44.3 (against 74.9 and 44.1, its house reading finding 79 houses with defaults),
recovery no lower in crisis years, both term sheets reconciling to par less the enhancement, its simulation at 40,000
to 150,000 paths putting Kestrel Lane at 3.2 to 3.3 per cent and Ostvale at 6.7 to 6.8 (expected losses 5.6 and 7.9,
the year-end chances tracking the CSV), the one-average route buying Kestrel Lane (0.57 against 5.3) and the
own-loan co-default route buying Ostvale (0.17 against 1.4), "an analytical error the data separates out". Residual:
the one-decimal chances and whole-per-cent subordinations depend on the estimator (its Kestrel Lane subordination 19
and 21 against 20 and 22, Ostvale's 17 and 18 matching); none of its variants crossed the 1 per cent line. Not
changed: the asks stay at the golden's estimator with the band stated in critical component 4.

Container gate (reduce-house-fixes H1, audit_containers.py, filed as a ship gate after this build's first READY
commit): 36 FAIL on 7c395ae0 (openpyxl's dialect, inline strings and build-clock entries in the three workbooks,
python-docx's template parts in the golden note, one clock across each zip's entries). The generator now passes
every workbook and the note through the house container writer (postprocess.py: shared strings, Excel's and Word's
part order and dialect, each file's own creator, company and stamps) and cuts both zips at each file's own save time
in Kadeweg's clock, the exports at the pulls that wrote them; 0 FAIL, 0 WARN on the final cut 3ec3c9ed. Every cell,
sentence and figure is unchanged (each workbook's cells read identically before and after; figures.json
byte-identical), so the leak reads and the judge's passes stand on it.

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
