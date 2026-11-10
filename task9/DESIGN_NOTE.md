# task9: Kestrel Lane's senior note, Ostvale's, or neither, for the matching portfolio

## Draw

Subdomain: Quantitative Finance (task type volatility and derivatives pricing: the price of a structured credit note
  is its loss distribution)
Analysis type: Forecasting & Predictive Modeling (each note's chance of any loss of principal over 2027 to 2031)
Answer shape: A distribution and where it is cut: each portfolio's five-year credit-loss distribution, where each
  note's subordination cuts it (the chance of loss, overall and by year end), where it would have to be cut for
  chances of 1 and 0.5 per cent, and each portfolio's expected credit loss, with the recommendation on top
Weight: a hard-to-measure quantity: a senior tranche's tail chance needs the joint law of defaults and recoveries at
  two grains the record never prints (each sector's swing with the economy's year, and the sponsor house's year that
  sets both how many of its companies fail and what they recover); the last builds' weights sit in synthesis (task1),
  modeling (task7) and measurement (task4)
Data-native sentence: a buyout house decides from one partnership's view of its year whether to fund each of its
  companies' breaches, so its companies default in the same years and in those years are sold or wound up for less,
  while the economy's year weighs on the capital-goods, building, freight, chemicals and car-parts chain far more
  than on services and staples and costs those defaults nothing extra because their houses are having ordinary years;
  the workout file keeps each recovery, the deal file each company's buyers, the performance file each sector's
  years, and each manager's tape concentrates one of the two shocks, Kestrel Lane's on seven houses, Ostvale's on the
  five sectors that follow the cycle
People: Ilse Lips (head of credit, Kadeweg Fiduciair Beheer), Damian Schenkel (chair of the trustees), Liza Dekker
  (document control), from `guard.py names` at the original draw

1. Card: `.claude/skills/fingerprint/cards/task9.json`, architecture 7 rebuilt as a results chain, re-registered
   2026-11-10: WARN only (objective and Gate G overuse; nearest drivers this slot's own lineage). Redrawn to
   clear bans, each to the honester label: prompt shape 10 (a scorecard against a threshold; 02 repeated task12, 14
   task2), forcing event budget_or_appropriation (the matching portfolio's senior-note allocation round, MP-RN-2 2.2;
   purchase_order_or_contract repeated mark162 v2, vote_or_meeting task12), context artifact register (the two
   collateral tapes the call is priced on; filed_standard repeated task11), the year-end chances asked as a table
   inside the memo (one deliverable, clear of the single-step form's csv and docx shell and of the corpus cap on a
   docx and xlsx set) and the prompt's second sentence reopened.
2. Why this rebuild: the single-step form of architecture 7 reads as level 4 on the client's depth scale (one
   investigation, the sponsor house's year, carried the call; three of its four shortcuts landed on one wrong call;
   Ostvale failed on almost every route) and was cut under the retired single-deep-step design; the author asked
   for a level 5 task. The world, records, people and documents are architecture 7's; the truth adds a loading per
   sector on the economy's year (world.py AM_S: 0.23 to 0.30 for the five cyclical sectors, 0.01 to 0.05 elsewhere),
   Kestrel Lane's seven houses are drawn from the twelve whose books lean least on those sectors, Ostvale lends only
   in them, and Ostvale offers 16.5 per cent subordination (above the 15.0 per cent the
   request for proposals set, for its weaker credits).
3. As of 17 February 2027 (Lenderbase and Dealtrail pulled 16 and 15 February); the investment committee meets on 25
   February, the trustees on 4 March, and both offers close on 12 March 2027.

## Deep reasoning

Task type: volatility-derivatives-pricing (Quantitative Finance; the price of a senior note is its loss distribution),
  a task type the taxonomy tags for Forecasting & Predictive Modeling; the forecast is each note's chance of losing
  principal over 2027 to 2031.
Domain test: the deciding quantities are a senior tranche's tail chances, the chance a portfolio's credit loss passes
  its attachment, with loss the sum of defaults times their loss given default; the field estimates them with a
  factor copula whose dependence and severity it calibrates on the default and workout record, and here both have to
  be estimated at grains the record does not print: each sector's loading on the economy's year, and the sponsor
  house's year, which also sets what a default recovers.
Swap: "should the hospital trust buy cover from insurer A or B for its 2027 malpractice claims" keeps a tail
  probability but loses the tranche and its attachment, the sponsor whose bad year sets both how many fail and what
  each failure costs, and the sector chain that orders less in a downturn; the results stop reading the same.
Where the weight sits: R4 and R5, each note's five-year chance: four estimated layers (default rates by rating and
  years since the buyout; each sector's loading on the year; the house-year's share; recovery on the house-year's
  latent shock read across the house's whole book on the closed cohorts) carried jointly through one simulation; it
  is long because each layer is estimated from a record whose grain differs from the tapes'.
Layer 1: Lenderbase resubmits loan-quarters (the latest kept), changed its status, purpose and rating codes and its
  date format in 2019, and carries LEIs only from mid-2012 (older loans joined by name through the LEI extract); the
  workout file reports recoveries in per cent for most lenders and as fractions for nine, and leaves open workouts
  blank; Dealtrail names buyers by fund, by house or with a co-invest vehicle and carries withdrawn approaches and
  add-ons; the tapes use their own layouts, rating scales and industry names in five currencies; each is neutral on
  every result once conformed (checks.py K1 to K3, R2a, R2b).
Not one thing: the strongest single piece is recovery's link to the sponsor house's year (R3); a run that nails it
  buys Ostvale at 0.83 per cent unless it also estimates each sector's loading (R2),
  and a run that nails R2 instead buys Kestrel Lane at 0.36 per cent; the call, the
  subordination needed and the chances by year end need both, and R1 sits under both.
One-fact test: the house's sentence, "a sponsor house in a bad year lets its defaulted companies go for less, across the whole of its book", rescues R3 and R4 (2 of
  9); the sectors' sentence rescues R2 and R5; neither rescues the call or the joint asks. A
  sentence naming both strands, "defaults and recoveries cluster in a sponsor house's year, and five sectors load on the economy" (the stage-4 judge's), measured on the route a run builds from
  it (recovery read off each house-year's co-defaults across the house's whole book, with the sector loadings and the house's year in the copula), rescues R2, R4, R6, R9 (4 of 9, effort.py's WARN band): it
  leaves R3, R5, R7, R8 to the latent house-year shock, which a co-default count does not measure, and a run that
  counts the co-defaults among the note's own loans from the same sentence still buys
  Ostvale (1.93 against 0.28 per cent).
Not semantics: every field, unit and clause read right (the 2019 codes, the per cent and fraction recoveries, the open
  workouts, the buyers' names, the tapes' scales) still leaves a run with one recovery for every default and one
  loading for every sector: no field carries a house, a loading or a link, and the pooled figures reconcile to the
  record (the closed cohorts' average recovery, the yearly default counts inside the copula's band).
Not rule application: MP-RN-2 files the WHAT (3.4 each default's own loss over its workout; 4.1 the record with its open
  workouts; 4.2 standings correlated, and recoveries with them, as far as the record shows) and nothing filed says
  which shocks move defaults or recoveries, at which grain, or how a latent shock is read. The enumerated family
  (one average recovery; a downturn link; the co-default table at the note's grain or the book's; the house-year's
  shock on three bases, with or without the year's term, on the default years MP-RN-2 4.1 reads recovery from; one pooled
  loading, larger independent sector factors, or a loading per sector by likelihood, pair moments or two groups)
  spans three calls; the standing family (both strands carried, 20 members) spans 2.3 to 4.0 per
  cent for Kestrel Lane and 1.5 to 3.0 for Ostvale, every member over the test; the ruling-out is loud
  only to a run that reads recovery against the house-year and the sectors against the year.
Estimand: MP-RN-2 2.1, 2.2, 3.2, 3.4, 3.5, 4.1 and 4.2 (phl_rated_note_standard_2026.pdf) and the prompt: population
  each note's portfolio as on its tape; outcomes the chance that cumulative loss passes the note's subordination by
  the end of 2031 and by each year end, the portfolio's mean five-year loss as a share of its par, and the five-year
  loss quantiles at 1 and 0.5 per cent; window 2027 to 2031 drawn from the record's conditions; unit per cent;
  comparison each note against 1 per cent and the lower of two that pass; subordination as each term sheet states it.
No decoy: nothing planted: the workout file is Lenderbase's own, the deal file Dealtrail's, the term sheets the
  managers'; no memo, rating report or stakeholder figure states a chance, a recovery by house or a sector's loading.
No replay: no result re-derives a published figure, and no stated number in the pack is wrong.
Pinned: each result's rivals run on the clean truth (analysis.py rivals and band, checks.py SF and R rows, verify.py's
  own road): R1 by likelihood (0.395), on the pooled scale (0.403) or by pair
  moments; R2 by likelihood, pair moments or two groups; R3 on three shock bases, with or without the year's term;
  R4 to R9 across the 20 combinations; ruled out by named data: one recovery (V1), the economy's year (V3), the
  note's own co-defaults (V4), independent sector factors (V5); by the text, the link on every closed workout (SF8:
  MP-RN-2 4.1 reads recovery from the default years whose workouts have all closed, 2008 to 2019).
Run forecast: R2 method shortcut (one pooled loading) or narrow look (the swing given to each sector as its own
  factor); R3 first story (the economy's year tested, found flat, one recovery kept) or dismissed own evidence (the
  co-default table seen, one recovery kept) or an unfinished chain (the table carried to each note's own loans);
  R4 to R9 fall with the strand a run missed; R1 is earned.
Strategy label: WORKS IN FORM (Part A variance beyond sampling noise, live form: the recovery's loading on the shared
  owner's shock at the owner's grain; Part A heterogeneity that pooling hides, live form: the sector loadings weighted
  to the portfolio the decision serves)
Depth level: 5: seven judgments that each move a result (the house's share; each sector's loading and the five
  sectors' moving together; recovery's link to the house's year rather than the economy's; its whole-book grain; the
  closed-cohort sample; the joint carry), two independent strands both needed for the call, and the shortcuts land on
  two different wrong calls: Kestrel Lane (the agencies' copula, one average loss; the sector loadings, one average loss; larger sector factors of their own, one average loss) and Ostvale
  (the house's year in the copula, one average loss; recovery tied to the economy's year; recovery on the house-year's shock, one pooled loading; recovery on the house-year's shock, larger sector factors of their own; recovery read off the co-defaults among each note's own loans); the golden holds across 20 estimator variants.
Lesson: a senior tranche's tail can run through two different shared shocks at once, an owner's year that also sets
  severity and an economy's year that weighs by sector and does not, and each note's concentration decides which one
  bites; one average severity hides the first, one pooled loading the second, and the defaults the economy drives
  come from owners having ordinary years, so a loading carried with one severity overstates the second note.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the house-year's share of each company's credit standing, 0.395 | modeling | the record's same-house pairs (0.61 against 0.23 per cent) and the random-effect likelihood on house-years given sector-years | 0.34 to 0.43 | method shortcut: the agencies' copula with no house at all (the runs of architecture 6 earned it) | - | Component 1 |
| R2 | Ostvale's portfolio's loading on the economy's year, 0.251 (industrial machinery, building products and services, transport and logistics, chemicals and materials and automotive parts at 0.14 to 0.36, the rest at most 0.05) | exploration and triage | the sixteen sectors' yearly defaults and the marginal likelihood over the year and sector-year factors (one loading for all fits 54.5 points of 2 log-likelihood worse on 15) | 0.21 to 0.3 | method shortcut: one pooled loading (0.065); or a narrow look: each swinging sector given a larger factor of its own, so its bad years arrive one sector at a time | - | Component 2 |
| R3 | recovery per unit of the house-year's shock, 0.313 (intercept 0.982) | investigation loops | the closed 2008 to 2019 cohorts: a lone default 74.7 per cent, three or more others 38.3; the economy's year alone -0.047; the shock as a posterior mean across the house's whole book | 0.26 to 0.34 | first story: the economy's year tested, found flat, one recovery kept; or dismissed own evidence: the co-default table seen and set aside | R1 | Component 3 |
| R4 | Kestrel Lane's five-year chance of loss, 3.7 per cent at 15.0 | forecasting | MP-RN-2 2.1, 3.2 to 4.2; R1 and R3 carried into the simulation | 2.3 to 4.0 | unfinished chain: the house's year in the copula with one recovery, 0.39 | R1, R3 | Ask 2 |
| R5 | Ostvale's five-year chance of loss, 2.8 per cent at 16.5 | forecasting | as R4, with R2 | 1.5 to 3.0 | method shortcut: recovery on the house's year with one pooled loading, 0.83 | R1, R2, R3 | Ask 2 |
| R6 | the recommendation: neither | synthesis | MP-RN-2 2.1 and 2.2 | exact | unfinished chain: one strand carried, the other note bought | R4, R5 | Recommendation |
| R7 | the subordination for 1 and 0.5 per cent: Kestrel Lane 20 and 22, Ostvale 19 and 21 | uncertainty | the five-year loss quantiles, whole per cent rounded up | each cell within its members' range | unfinished chain: quantiles of a loss law with one strand | R1, R2, R3 | Ask 4 |
| R8 | the chance by each year end, 2027 to 2031, both notes | forecasting | the cumulative loss by year end against each subordination | each cell within its members' range | unfinished chain: one strand carried | R1, R2, R3 | Ask 5 |
| R9 | each portfolio's expected credit loss, Kestrel Lane 5.9 and Ostvale 7.6 per cent of par | forecasting | MP-RN-2 3.4 and 3.5, each default's own shortfall | each cell within its members' range | method shortcut: one average recovery (41.0 per cent loss) for every default | R1, R3 | Ask 3 |

Carry-forward: R1 and R2 stand on the record alone and R3 on R1; Kestrel Lane's figures (R4, its cells of R7 to R9)
fall with R1 or R3 and not with R2, Ostvale's (R5, its cells) with R2 as well; the call falls with either strand. No
analytical result is the only analytical input of more than one other (R1 behind R3).

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| defaults clustering by sponsor house-year | constructed, simulated from each house's yearly decision | no: across all 80 houses and every year; Ostvale's 63 houses and Kestrel Lane's 7 alike | a targeted query (same house-year pairs, after rebuilding ownership from the deal file) | modelling (a random-effect layer in the copula) | keep: R1, earned by careful runs |
| recovery falling in the house's bad year | constructed, simulated from the same decision | no: every house's defaults in both halves of the closed cohorts | modelling (each house-year's latent shock inferred across its whole book; the co-default table shows a gradient only at the book's grain) | modelling (a regression calibration on the closed cohorts, carried into the simulation) | keep: R3, one of several results |
| five sectors' loading on the economy's year | constructed, simulated from each industry's tie to the cycle | no: every company of those sectors across 19 years and 80 houses (Kestrel Lane holds some too) | a targeted query (sixteen sectors read against the year) then modelling | modelling (a loading per sector by marginal likelihood, net of the sector-years, carried with the house-state recovery; larger independent sector factors miss the joint swing) | keep: R2, one of several results |
| the clustered defaults' long, still-open workouts | constructed, simulated from the same decision | no: every house's recent defaults | modelling (the open workouts read against their house-years) | modelling (the link fitted on the closed cohorts, MP-RN-2 4.1 keeping the open ones) | keep: inside R3 |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the house-year's share of each standing | Missed | Right | Right |
| R2 Ostvale's loading on the economy's year | Missed | Partly | Right |
| R3 recovery per unit of the house-year's shock | Missed | Missed | Right |
| R4 Kestrel Lane's five-year chance of loss | Missed | Missed | Right |
| R5 Ostvale's five-year chance of loss | Missed | Missed | Right |
| R6 the recommendation | Missed | Missed | Right |
| R7 the subordination for 1 and 0.5 per cent | Missed | Missed | Right |
| R8 the chance by each year end | Missed | Missed | Right |
| R9 each portfolio's expected credit loss | Partly | Partly | Right |
| Roughly | 0.5 of 9 | 2 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "defaults and recoveries cluster in a sponsor house's year, and five sectors load on the economy"; rescues 4 of 9 results
Pair estimate: 24.5

## Data provenance

Source: generated by task9/generator from a simulated process (world.py, pack.py): sponsor houses raising funds,
  funds buying and selling companies, each company's loans and their quarterly reports to a lender consortium, the
  defaults and their workouts, and two managers drawing their tapes from the companies alive at the end of 2026.
Behaves like the real thing: default rates graded by rating and peaking three to four years after a buyout; yearly
  default rates spiking in the economy's bad years (2009, 2020, 2012, 2023) and the capital-goods and freight chain
  spiking hardest; a sponsor's companies failing together; recoveries falling and workouts lengthening in the
  sponsor's bad years, with the latest workouts still open; resubmitted quarters, a 2019 change of codes, LEIs only
  from 2012; each matches the published behaviour of European sponsor-backed mid-market loans.
Genuine patterns: (1) default rates by rating and by years since the buyout (a seasoning hump); (2) the economy's
  year, weighing by sector; (3) sponsor house-year clustering of defaults; (4) recovery falling with the house's year
  and workouts lengthening; (5) secondary buyouts, refinancings and exits resetting ownership; (6) currencies and
  margins by rating.
Problems by process: resubmitted loan-quarters (lenders correcting drawn amounts or filing defaults late); the 2019
  vocabulary change; LEIs missing before mid-2012 and for some lenders; recoveries in per cent or fractions by lender;
  open workouts with no recovery yet; buyers named by fund, house or co-invest vehicle; withdrawn deals and add-ons in
  the deal file; tapes in five currencies on two rating scales and two industry schemes.
Breadth: 16,967 company-years over 19 years, 16 sectors and 80 houses
  (493 funds); 74,356 loan-quarter rows; 537 workouts; 9,179 deals; two tapes of 98 and 100 loans;
  thirteen files, two of them distractors; deciding which sectors, houses and years carry the tail is work.

## Template check

Chain signature: modeling, exploration-triage, investigation-loops, forecasting, forecasting, synthesis, uncertainty,
  forecasting, forecasting
Question form: whether (buy one of two notes or neither), the deliverable by type (a memo)
Nearest build: task4 (allocation-sensitivity, measurement: a pilot model carried to duties under a battery limit) and
  task7 (scenarios-flip, modeling); neither prices a tail through two shared shocks at different grains, and no
  build on file has this chain with a distribution cut. Abstraction sentence tried against the nearest Mark build
  (mark135, a variance of a weighted sum from asynchronously struck components): not writable, the deciding
  quantities here are tail chances set by two dependence structures and a state-dependent severity.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | any loss in the five years | the loss at the end of 2031; a loss in any one year | the end of 2031 | same call: cumulative losses never fall (asserted) |
| SF2 | the portfolio | static with repaid loans replaced; runoff | static | MP-RN-2 3.2 |
| SF3 | a default's loss | its own shortfall by the end of its workout; one average | its own | MP-RN-2 3.4 and 4.2 |
| SF4 | dependence | standings correlated as the record shows, recoveries with them; standings only | both | MP-RN-2 4.2 |
| SF5 | conditions | the record's; stressed | the record's | MP-RN-2 4.1 |
| SF6 | the FX date | 31 December; 30 December | 31 December | same call (asserted) |
| SF7 | default | Lenderbase's; an agency's | Lenderbase's | MP-RN-2 3.3 |
| SF8 | the link's sample | the default years whose workouts have all closed (2008 to 2019); every closed workout | the fully closed default years | MP-RN-2 4.1 ("what lenders recover is read from the default years whose workouts have all closed", asserted against the workout file); the open workouts are the clustered defaults' long ones (V2), so every closed workout would lighten every loss |
| SF9 | the age clock | years since the buyout; loan age | years since the buyout | same call; the buyout clock fits better (asserted) |
| SF10 | the sponsor grain | house-year; fund-year; lasting | house-year | the log-likelihood (asserted) |
| SF11 | choosing between two | the lower chance; the wider margin | the lower chance | MP-RN-2 2.2 |
| SF12 | subordination needed | the five-year loss quantile rounded up; to nearest | rounded up | the prompt |
| SF13 | weights | euro par; loan count | euro par | same call (asserted) |
| SF14 | default chance | one-year; cumulative | one-year | MP-RN-2 4.2 |
| SF15 | relending | to the same borrower; to new borrowers | the same borrower | the term sheets |
| SF16 | ageing | borrowers and loans grow older; frozen at the tape | they age | MP-RN-2 3.2; same call either way (SF16b) |
| SF17 | open workouts | in the record as defaults; dropped | in the record as defaults | MP-RN-2 4.1 ("a default whose workout is still open counts as a default") |
| SF18 | a defaulted loan | leaves, not replaced; replaced | leaves | MP-RN-2 3.4 |
| SF19 | the house shock's basis | the sector-year's rates; the year's rates; each sector's rate moved by its loading on the year's shock | the sector-year's | same call (every member of the band) |
| SF20 | the year's shock in the link | in; out | in | same call (asserted) |
| SF21 | recovery units | per cent and fractions read as one share | one share | the values (a 0 to 1 share in every row) |
| SF22 | the co-defaults a recovery moves with | the house-year's across its whole book; the note's own loans | the whole book | the grain (V4): the counts run over books of a median 12 companies and Ostvale holds 2 of each house's |
| SF23 | expected credit loss | the portfolio's mean five-year loss over par; the note's expected loss | the portfolio's | the prompt and MP-RN-2 3.4 and 3.5 |
| SF24 | each sector's loading | by likelihood; by pair moments; in two groups | by likelihood | same call (every member of the band) |
| SF25 | the house's share | latent scale; pooled scale; pair moments | latent scale | same call (every member of the band) |
| SF26 | the sectors' swing | a loading on the shared year; larger independent sector factors | a loading on the shared year | the five sectors' yearly rates move together (0.63 against 0.09 for the rest, V5), which independent factors cannot produce; they buy Ostvale |
| SF27 | the two-group threshold | a loading above 0.10; any cut between the five and the rest | above 0.10 | same call; the per-sector fit needs none |
| SF28 | each note's subordination | as its term sheet states (15.0 and 16.5); the request's 15.0 for both | as stated | the term sheets (Class A par less the stated enhancement, asserted) |
| SF29 | the tapes' rating basis | at origination; current at the cut-off | at origination | both tapes' headers name it, and every tape loan the record holds carries the same rating as Lenderbase's rating_at_origination (asserted) |

## Closure table

| Axis | Closure |
|---|---|
| 1 | population: each note's tape, MP-RN-2 3.1 and 3.2 |
| 2 | unit of account: a note |
| 3 | attribution window: 2027 to 2031, MP-RN-2 2.1 |
| 4 | as-of dating: the extracts of February 2027 (C1) |
| 5 | version basis: MP-RN-2 |
| 6 | denominator: par, MP-RN-2 3.5 |
| 7 | weighting: euro par (SF13) |
| 8 | window length: five years |
| 9 | boundary inclusivity: below 1.0 per cent, MP-RN-2 2.1 |
| 10 | rounding path: one decimal for chances and losses, whole per cent rounded up for subordination (the prompt; SF12) |
| 11 | tie-break: the lower chance, MP-RN-2 2.2 |
| 12 | maturity and censoring: open workouts in the record as defaults, recovery read from the default years whose workouts have all closed (MP-RN-2 4.1; SF8, SF17) |
| 13 | order of operations: conform, link to houses, fit, simulate (C1) |
| 14 | row order: the latest submission (C1) |
| 15 | duplicate resolution: the latest submission of a loan-quarter (C1) |
| 16 | identity normalisation: LEI, else the name through the LEI extract (C1) |
| 17 | netting against gross: loss net of recovery, MP-RN-2 3.4 |
| 18 | dimensional units: recoveries as shares (SF21) |
| 19 | code and status semantics: the 2019 codes (C1) |
| 20 | integerisation: none |
| 21 | clause scope: MP-RN-2 2 to 4 |
| 22 | forward window contents: the record's conditions (SF5) |

## Literal reader

Executed word for word, MP-RN-2 2.1 to 4.2 price each note's chance that its static portfolio's losses, each default
losing what its own workout does not recover, pass its subordination by the end of 2031, with default and recovery
from the record of comparable loans, its open workouts included, standings Gaussian and correlated and recoveries with
them as far as that record shows. What the text leaves open is how the record shows them correlated; every route that
reads the standings against each sector's swing with the year and the house's year, and recovery against the house's
year at the grain the record measures it, files neither; one average recovery, a downturn link, one pooled loading,
larger independent sector factors and a note's own co-defaults each file one of the notes. SF1 to SF29 close every
term; the prompt pins every result's unit and rounding.

## Prompt contract

The voice rewrite may not drop or change: the question (Kestrel Lane Credit Partners' senior note, Ostvale Capital's,
or neither, for the matching portfolio, under the 1 per cent test with the lower-risk one when both qualify); the
memo for the investment committee with the recommendation, each note's chance of any loss over 2027 to 2031, its
portfolio's expected credit loss over them, the subordination for chances of 1 and 0.5 per cent, a table of each
note's chance by each year end from 2027 to 2031 and the exceedance chart to 30 per cent of par with both
subordinations marked; the rounding (chances and expected losses to one decimal in per cent, subordination in whole per cent
of par rounded up). It must never add a sponsor, a house, a sector, the economy, a cycle, a recovery, a correlation,
a loading, a workout, a file name or anything about who is asking.
## Stage 4

- Leak reader (isolated, Sonnet, medium, on target.zip 29757c9b with a fresh prompt.txt): no LEAK. Questions 2 to 4
  none (the term sheets give the offered terms only; the sector crosswalk reads as the vendor's utility for the two
  tapes; 15.0, 17.0 and the 1.0 per cent test read as terms). Questions 1 and 6 name MP-RN-2 4.2 as the one sentence
  that names the model family, leaving open "the estimation of PD, correlation and LGD": it names no shock, grain,
  sector loading or owner, so it closes forks SF4 and SF14 and decides no result; kept, as the two reads of the
  single-step form ruled it. Question 5's sentences (2.1, 2.2, 3.1 to 3.5, 4.1, 4.2) each execute to the golden's
  construction. The reader took the deal file for a distractor, so nothing announces the sponsor-house strand. Its
  one realism note (the standard is unusually well specified) is answered by the fork 4.2 closes. Every sweep line is
  ruled harmless in `leak_check_report.md` (`## Solver's-eye read`): the offered subordination, the request for
  proposals' floor, a section number, the test's own words, and the standard's definitions of default, loss and the
  record.
- The prompt's deliverable set (a memo and a workbook) sat at 4 of 13 prompts on file against the 20 per cent cap;
  the year-end chances are now a table inside the memo, the one deliverable, and the prompt gate passes clean (904
  characters).
- Determinism judge, pass 1 (on target.zip 29757c9b; `determinism_check_report.md`, the thread spawned from the
  judge's brief by the main session): NOT_DETERMINISTIC, SEND_BACK, margin_or_boundary_fragility on Ostvale's side;
  Gate G passes (method_or_model_selection, analytical_non_defect, no surface read, no sole data defect), Gate H
  borderline. Read against the gate table, the failing gate is C (`underspecified_objective`), which spends no
  architecture; every finding repaired in one generator pass:
  - the recovery sample: MP-RN-2 4.1 said only that the open workouts were in the record, so a link fitted on every
    closed workout (Ostvale 0.77 per cent at 17.0, buying Ostvale) was a defensible reading. 4.1 now reads "a default
    whose workout is still open counts as a default, and what lenders recover is read from the default years whose
    workouts have all closed", which executes to 2008 to 2019 on the workout file (every later year has open
    workouts; SF8 asserts it). The quick pass and its route lose that window's average (41.0 per cent), not every
    closed workout's (37.0).
  - the margin: the weakest sound estimator's 1 per cent loss quantile for Ostvale was 17.29 per cent of par, 0.29
    points over its 17.0 (1.15 per cent). Ostvale now offers 16.5 per cent: every sound estimator fails it by 0.79
    points or more (band 1.5 to 3.0 per cent), and the routes that buy Ostvale still do (one pooled loading, quantile
    16.20; larger independent sector factors, 16.00).
  - the rating basis: both tapes now name their rating as at origination, as Lenderbase's is, and every tape loan the
    record holds (71 of Kestrel Lane's, 60 of Ostvale's) carries the same rating in both (SF29).
  - the bands: the five-year chances, the expected credit losses, the subordination needed and the year-end chances
    carry the sound estimators' range in the Supplementary Questions (figures.json `ask_bands`).
  - Gate H: the judge's best sentence names both strands. Measured on the route a run builds from it (recovery read off
    each house-year's co-defaults across the house's whole book), it rescues R2, R4, R6 and R9, 4 of 9, in effort.py's
    WARN band. It leaves R3, R5, R7 and R8 to the latent house-year shock, and the same sentence read at the note's own
    loans still buys Ostvale. Both factors run across the record: the five sectors' yearly rates move together over 19
    years and 80 houses (the judge's own 0.62 against 0.09), and same-house pairs co-default in every sector. Each
    note's concentration is its own offer. The sector strand moves Kestrel Lane too (4.38 per cent on one pooled
    loading against 3.7).
  - The judge's own road was in its words cruder than the golden's (independent per-loan recovery noise, loadings and
    default rates not fitted by likelihood). It put both notes near 1.6 per cent at its own slope (0.22 against 0.313),
    counted 20,933 loan-years against the golden's 16,967 company-years, and ran expected losses above the golden's.
- The repair's cut (target.zip 4a97e7b6, two builds byte-identical) clears what Gate C found. Ostvale's band is 1.5 to
  3.0 per cent at 16.5 with the golden at 2.8; the recovery sample is filed, the rating basis named and the asks
  banded (figures_check 0 absent; the verifier not reached). It fails two of the generator's own bar checks:
  - R5: the judge's sentence naming both strands rescues R2, R4, R6 and R9, 4 of 9 against the house's third, at any
    subordination. Once both strands are told in one sentence, Gate H's one-fact test fails.
  - R7e: at 16.5, the route with recovery on the house-year's shock and one pooled loading sits at 0.90 per cent on the
    clean truth (0.83 on the pack). That is inside the 0.8 margin the check keeps so that the sector strand is needed
    on Ostvale's side. The two margins share about one point of par (the pooled route's 1 per cent quantile is 16.20,
    the weakest sound estimator's 17.29), so Gate C's margin and the level-5 route structure cannot both hold with room.
- Read against the gate table, R5 is a Gate H failure, and a Gate H failure spends the architecture (`build-pipeline`:
  re-root in another world, with another dataset and another shell). Paused for the author's ruling: re-root as
  architecture 8 in a new world, or retire the slot. The leak reader did not re-read the repaired documents (4.1, the
  Ostvale term sheet, the tape headers), because the build stops here.

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
