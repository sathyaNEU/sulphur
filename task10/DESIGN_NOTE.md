# task10: Wealdmoor Power Networks' winter 2027/28 reinforcement at the Halverton zone primaries

Architecture 7, drawn on 2026-11-10 in the same world after both platform runs landed architecture 6
(`runs/arch6_triage.md`, REDESIGN: 0 of 11 results lost). The organisation, the nine primaries and the files' genres are
kept. The chain is built on what the two runs did and did not do. What they did by reflex (hygiene, the switching days,
the share capped at the instruction, the come-back replayed over the day, a predictive nine-days-in-ten level) is kept as
results a careful run earns. The weight sits on three structural judgments the runs named as assumptions and never
tested (the cold end of demand where the service always ran, what the register's customers still have to add, what an
enlarged contract's sites will have commissioned), each of which runs across the whole record and decides a different
primary: five zones, five calls, each turning on a different piece of the work. The fiction's dates sit before the day
the build ships (exports of 1 to 4 November 2026, the award notice of 21 October 2026).

## Draw

Subdomain: Energy Systems & Utilities
Analysis type: Forecasting & Predictive Modeling
Answer shape: a distribution and where it is cut (each zone primary's design-day peak for winter 2027/28 with its
  flexibility contract instructed in full, as the expected peak, the level it stays under on nine design days in ten
  and the share of design days over firm capacity, cut at firm capacity under the guideline's one-day-in-ten rule,
  with the primaries to reinforce on top)
Weight: modeling. Three specifications carry the result and each has to be chosen against what the record is, not
  fitted to what it shows: the form of demand at the cold end, where every evening without a service is a mild one;
  how a connected customer's draw builds up by its type, read from customers at every age; and how late a signed site
  commissions by its class, read across the licence area's register and not from the zone's own past. The last two
  live cards sit on assembly (task14) and a hard-to-measure quantity (task3); architecture 6 sat on validation.
Data-native sentence: the service is instructed on the days the control room's forecast runs high, so the record holds
  an evening without it only on mild, low-running days; a connected customer takes two to three years to reach a share
  of its agreed capacity that depends on what it is; and a provider's sites commission months after the date planned
  by an amount that depends on the kind of asset, while the 2027/28 awards are made of different kinds than each
  zone's own record.
People: Marion Todd, Clifford Evans, Irene Carpenter (drawn at architecture 5 with guard.py names, the same world)

Lineage: architecture 6 (the available share read from the calls that outran it, the come-back, the spread carried in
proportion, a held-out winter) landed on both platform runs with every headline figure; its identity and fate are in
the card's lineage. The prompt shell is redrawn with the chain (which; the second sentence led by the design day; a
workbook and a few slides), and a fifth constraint managed zone, Dunmore Street, joins the four.

Guard: card registered 2026-11-10T07:44:07Z, WARN, no BLOCK. template.chain_near and overuse.weight (task17, a
distribution and where it is cut with the weight on modeling): task17 cuts a resampled distribution of one statistic
and its modeling is the resampling design; here the distribution is each primary's design-day peak, built from three
structural models of a physical process, and the cut is the guideline's firm capacity rule; the chain signatures share
no run of three areas. driver.near 0.21 and 0.13 against this slot's own architectures 6 and 5: the world and the
decision are the same, the chain is not (architecture 6 read a contract's limit from part calls and validated it;
architecture 5 netted a neighbour's rise; here the three deciding quantities are the cold end of demand, the
connections' build-up and commissioning by class). overuse.forum (executive_team): the December capital expenditure
review is the world's own. repeat.decision (designation_set, task14): the review commits a list of primaries, and
task14 designates departments for verification from a coverage bridge. repeat.question_form (which, task3): a pick
asks which. The decisive gap is filed as time and the decisive generator as composition shift: the measurement is three
winters back and the call two winters forward, and what differs between them is composition (the design day against
the days measured without a service, the awards' asset classes against the record's, the customers' ages against
today's).

Surface screen on the final cut (guard.py surface, read against origin/main on 2026-11-10): one pair promoted, task10 against task14
(surface 0.100, the same decision type on the cards). Read side by side: task14 is an academic medical centre's coverage statement for
its conflict-of-interest registry (survey research and official statistics, a bridge, the weight on assembly); the domain, the
files, the chain and the answer differ, and the one shared trait is that each designates a set.

## Deep reasoning

Task type: Load, price & renewable forecasting (Energy Systems & Utilities, `load-forecasting`), which serves Forecasting & Predictive Modeling: every result is a forecast for a winter not yet begun, or a quantity that forecast is built from.
Domain test: a distribution planner forecasts a primary's design-day peak (a weather-corrected peak for the latest winter, grown at the DFES rate, plus the diversified demand new connections add), credits contracted flexibility at what it will deliver in the evening peak, and sets the residual peak at a stated assurance against N-1 firm capacity. The field's own knowledge decides each judgment: demand-side response is dispatched on the cold days, so a weather correction can only read the cold end where the service never reaches; a connection draws a share of its agreed supply capacity that depends on what it is and builds up over years; a provider can only deliver from sites that have passed their commissioning test; curtailed heat comes back after the window and can move the peak.
Swap: "which wards do we need to commit to opening for winter 2027/28, counting the agency cover contracted for it" keeps a capacity call and loses a design temperature, a service window that removes the cold evenings from the record, an agreed supply capacity a customer grows into, a commissioning test, megawatts that come back after a window and a half-hourly day shape that moves a peak from the half-hour ending 18:00 to the one ending 20:00; none of the eleven results could be stated.
Where the weight sits: modeling, in three places that each need a model chosen against how the record came to be, not fitted to what it shows. R1: the evening's cold end is built from the mornings of 285 working weekdays and each evening's relation to its morning, because the evenings without a service stop near 0.3 C at Dunmore Street. R2: 13,715 customer-months turned into a build-up by customer type, then each customer carried from its own level. R4: 1,536 sites across the licence area turned into commissioning by asset class with the sites still to come and the sites withdrawn counted, then applied to awards made of other classes than each zone's past. Each is long work on a large file and none is a trick: the method in each is ordinary once the question is asked.
Layer 1: the SCADA historian's asset ID migration (two point names per primary), values held through comms outages flagged S, bad values flagged B, rows the outstation never sent and a monthly extract re-sent over the day before (441 rows); the dispatch log's revised and cancelled instructions with superseded revisions kept and provider names as typed; UK local time in the SCADA and dispatch exports beside the weather station's GMT, with raw and checked versions of an hour; the switching log's two-row transfers; the growth register's withdrawn, superseded and quoted offers and legacy feeder codes; the asset register's superseded entries (39), class names as typed and five providers under fifteen spellings; the settlement summary's part months. Read the careless way one at a time, each leaves the list unchanged and every figure inside its band (checks.py BAR R2); none decides a result.
Not one thing: the strongest single piece is what will be in service (R4). A run that nails it has the megawatts delivered (R6) and still commits Hartwell Common, drops Dunmore Street and Charlecote Way and files the peaks and levels wrong at three primaries. The cold end (R1) decides Dunmore Street alone, the customers (R2) Charlecote Way one way and Hartwell Common the other, the sites (R4) Fenwick Street, the day replayed (R7, R8) Ashcombe Road. 18 shortcut routes give 7 different wrong lists.
One-fact test: the most useful single sentence ("a provider's availability follows the megawatts in service, and the sites still to come commission as late as their class has across the register, not on the planned dates") rescues 2 of 11 results (R4 and R6); the cold-end sentence rescues R1 alone and the build-up sentence R2 alone; any two of the three together rescue 3 of 11, and none of the six brings the careful pass to the list (effort.json hints; checks.py BAR R5 and R6).
Not semantics: every field read right (both point names, quality G, the UK clock, the latest revision, megawatts scheduled, the GMT daily mean, the transfers paired, accepted offers, the register's dates, each site's status and test date) leaves the careful pass exactly where it is: no field holds what the evening would have been on a cold day without the service, what a customer will draw in January 2028, or when a site still to come will pass its test.
Not rule application: the guideline files the WHAT of each result (the design day and that every such day counts, the latest winter, growth, which customers and between which dates, in service and on which date, the credited half-hours, the day's highest half-hour, one design day in ten over day-to-day variation, firm capacity) and no document says how demand at the cold end is to be read, how a customer's draw relates to its agreed capacity or its age, how late sites commission, that anything comes back after a window, or how a spread is measured; with every filed rule applied, R1, R2, R4, R5, R7 and R9 are still to be estimated.
Estimand: guideline WPN-NP-G-014 issue 5 sections 2 to 7 and Appendix A, and award notice WPN-DSO-FLX-2026-07; population the five zone primaries of the award notice and every design day, whether or not a service would be instructed on it; outcome each primary's highest half-hourly demand on the winter 2027/28 design day with its contracted megawatts instructed in full for the whole service window, a contract's megawatts delivered quoted as the mean of the half-hours ending 17:30 and 18:00; window a working weekday at a GMT-day mean of minus 3.0 C at Halverton, assessed as at 15 January 2028; unit MW by primary and whole per cent of design days; comparison firm capacity (Appendix A), exceeded on more than one design day in ten, taken over the variation from one design day to another.
No decoy: nothing is written to carry a wrong answer: no memo, earlier assessment, provider claim, settlement figure or forecast states a demand, a delivery, a share, a peak or a ranking of the primaries; the register's planned dates are what the providers gave at signing, a real field and not an assessment.
No replay: no result re-derives a published figure and no stated number in the pack is wrong (firm capacities, ratings, contracted megawatts and DFES rates are inputs and agree across the files).
Pinned: 17 variants of the golden's own choices run on the pack and on the clean truth (the form of the mornings' temperature response, the hours taken as the morning, the winters, how an evening is tied to its morning, a customer's own level and the build-up's shape, the record a site still to come is read on, the share's line and the calls that were met): every one commits the same list (Ashcombe Road +1.88; Charlecote Way +1.11; Dunmore Street +0.93; Fenwick Street +1.07; Hartwell Common -0.74 MW against firm capacity at the weakest) and every figure of every variant sits inside the stated bands (checks.py BAR R7). The rivals outside the bands are ruled out by named data: a straight line through the mornings reads the 32 mornings at or below minus 1 C at Dunmore Street 0.56 MW low (t 5.2); no working weekday without a service was colder than 0.3 C there in 2025/26; established draw runs from 0.22 to 0.59 of agreed capacity across 10 customer types; 3.3 per cent of 1172 sites were in service by their planned date; Fenwick Street had its whole contract in service in mid January 2025 and 2026 on refrigeration and HVAC (1.04 and 1.09 of it), and its sites still to come are process load; 30 of 143 process load sites past their planned date were still to come at the extract and 9 withdrawn. An independent rebuild by other methods (verify.py) lands every figure inside its band.
Run forecast: R1 and R3 with it, method shortcut: both architecture 6 runs fitted each half-hour on the days without a service and carried the line to the design temperature, naming it an assumption; here that loses Dunmore Street. R2, first story and narrow look: both runs took the register's connections in full; here the customers already energised still owe most of their rise (Charlecote Way) and those due late have barely begun (Hartwell Common). R4 and R6, self-confirming check or method shortcut: both runs took availability to scale with the megawatts contracted; here the sites still to come commission by class (Fenwick Street), and a run that groups the register by class and reads the commissioned sites alone keeps the list and misses the megawatts at two primaries. R8 to R11, unfinished chain: the replay, the predictive level and the cut are done by reflex around the wrong centres. R5 and R7 are expected to be earned by both runs.
Strategy label: DIRECTION ONLY (the client's energy strategy on peak load forecasts whose bands hold up, and the depth scale's list of what stumps a careful run: a rate from the average applied to units selected for being extreme, pooling where composition differs, a risk named and never sized); the chain is the Halverton record's own.
Depth level: 5. Four independent judgments each decide a different primary and none helps with another (the cold end of demand, Dunmore Street; the customers' build-up, Charlecote Way one way and Hartwell Common the other; commissioning by class, Fenwick Street; the day replayed with the load that comes back, Ashcombe Road), with the share, the nine-days-in-ten level and the cut around them; 18 shortcut routes land on 7 different wrong lists, and the only one that keeps the list (each class read from the commissioned sites alone) misses the megawatts at two primaries.
Lesson: a forecast for a design condition has to be built from the part of the record the intervention never touched, a register's addition from what its members still have to grow, and a contract's worth from what will be in service by its kind; each is a selection or composition question that a fit to the visible record answers wrongly without failing any hold-out. No build on file forecasts a constrained unit where the intervention has removed the design condition from the untreated record.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | Design-day demand in winter 2025/26: the day's highest half-hour at minus 3.0 C, every working weekday with or without a service, MW by primary (Dunmore Street 22.2, Ashcombe Road 30.2) | causal reasoning | guideline 2 and 3 (the design day, every such day, no service delivered, normal running arrangement, the latest complete winter) and the SCADA record: the half-hours ending 07:00 to 15:30 are never inside a service window, 285 working weekdays, 39 at or below 0 C | 21.9 to 22.6 at Dunmore Street, 29.9 to 30.8 at Ashcombe Road; each primary's band in the answer blocks (SF7 to SF10) | method shortcut: each evening half-hour on a straight line through the days no service ran, carried to minus 3.0 C: 20.2 at Dunmore Street and 29.0 at Ashcombe Road. Both architecture 6 runs fitted this and named the carry as an assumption | - | Component 1 |
| R2 | Megawatts the load growth register's customers add to each primary's demand between 15 January 2026 and 15 January 2028 (Charlecote Way 4.5, Hartwell Common 0.7) | missingness and measurement | guideline 4 (the register as it stands, the two assessment dates, a customer's mean demand 17:00 to 18:00 on working days) and 13,715 customer-months in the settlement summary: customers of 10 types at every age | 4.0 to 4.7 at Charlecote Way, 0.5 to 1.1 at Hartwell Common (SF12) | first story at Charlecote Way: its three large customers were energised before the latest winter's assessment date, so they are taken as already in the measured demand (0.0 MW); narrow look at Hartwell Common: the customers due after the latest winter counted at their type's established share (2.7 MW), their age on the assessment date never examined | - | Component 2 |
| R3 | Design-day demand before flexibility in winter 2027/28, MW by primary (Charlecote Way 30.3, Dunmore Street 23.0) | forecasting | guideline 4: R1 at the DFES rates of the substation register compounded for two years, plus R2, every half-hour in the peak's proportion | 29.8 to 30.7 at Charlecote Way, 22.7 to 23.4 at Dunmore Street | unfinished chain: the growth arithmetic done right on R1's line and R2's count: 25.5 at Charlecote Way, 21.0 at Dunmore Street, 26.2 at Hartwell Common against 24.3 | R1, R2 | Ask 1 |
| R4 | Megawatts each provider can be expected to have in service on 15 January 2028 (Fenwick Street 7.6 of 13.0 contracted, Ashcombe Road 17.8 of 21.0) | modeling | guideline 6 (in service from the commissioning test until withdrawn; the sites in service on the assessment date) and the asset register's 1,536 sites in 29 zones: the share in service by days since the planned date, by asset class, the sites still to come and the sites withdrawn counted | 7.3 to 7.8 at Fenwick Street, 17.2 to 18.2 at Ashcombe Road (SF15) | self-confirming check: the sites still to come taken on their planned dates (14.3 MW at Fenwick Street, 23.2 at Ashcombe Road), which each zone's own past winters seem to confirm (Fenwick Street had its whole contract in service by mid January, on refrigeration and HVAC). One step on, a method shortcut: each class's lateness read from the sites commissioned alone (8.4 and 18.9) | - | Component 3 |
| R5 | Share of its megawatts in service each provider has available on the design day (Corvane Flex 0.42, Quillon Energy Services 0.51) | missingness and measurement | guideline 6 and the completed events: megawatts delivered against megawatts in service that day; an event that met its instruction shows only a floor | 0.40 to 0.46 and 0.49 to 0.55 (SF17) | method shortcut on the quick pass only: megawatts delivered over megawatts contracted with the met calls taken as the share (0.37 and 0.54); a careful run caps the share at the instruction, as both architecture 6 runs did, and earns it | - | Component 4 |
| R6 | Megawatts each contract can be expected to deliver between 17:00 and 18:00 on the design day (Fenwick Street 3.9, Ashcombe Road 7.6) | forecasting | guideline 6 (instructed in full; quoted as the mean of the half-hours ending 17:30 and 18:00): R4 times R5 | 3.7 to 4.2 at Fenwick Street, 7.2 to 8.0 at Ashcombe Road (SF16, SF25) | unfinished chain: the share is right and is applied to megawatts that will not be in service: 7.4 at Fenwick Street, 9.9 at Ashcombe Road | R4, R5 | Ask 2 |
| R7 | Megawatts that come back in the four half-hours after the window per megawatt delivered (Corvane Flex 0.67, Quillon Energy Services 0.31) | investigation loops | the event days' own half-hours after 19:30 against the day's evening without a service | 0.60 to 0.71 and 0.26 to 0.36 | unfinished chain on the quick pass only: the evening after the window never examined; a careful run replays it, as both architecture 6 runs did, and earns it | - | Component 5 |
| R8 | The design day's expected peak with the service instructed in full, MW by primary (Ashcombe Road 28.5 in the half-hour ending 20:00, Fenwick Street 35.0) | forecasting | guideline 6 (the highest half-hour with the service delivered through its window, whichever half-hour that falls in): the day replayed half-hour by half-hour with R3, R6 and R7 | 28.2 to 29.0 at Ashcombe Road, 34.7 to 35.4 at Fenwick Street | unfinished chain: the replay is done and earned, on a demand and a delivery that are each off: 21.4 at Charlecote Way against 25.9, 31.6 at Fenwick Street, 24.6 at Hartwell Common against 22.8 | R3, R6, R7 | Ask 3 |
| R9 | The level each peak stays under on nine design days in ten, MW by primary, against firm capacity (Dunmore Street 21.1 against 20.0, Hartwell Common 23.4 against 24.4) | uncertainty | guideline 7 (over the variation from one design day to another as the record shows it): design days drawn from the day-to-day spread of demand and of what each provider had available, each day's highest half-hour taken (SF20, SF23) | 20.8 to 21.5 at Dunmore Street, 23.1 to 23.8 at Hartwell Common; the weakest variant 0.74 MW from firm capacity | unfinished chain: a predictive level is drawn, as both runs did, around the wrong centre: 18.9 at Dunmore Street, 22.1 at Charlecote Way against 27.0, 32.9 at Fenwick Street against 36.2, 25.3 at Hartwell Common | R3, R6, R7 | Ask 4 |
| R10 | Share of design days on which the peak would exceed firm capacity, whole per cent by primary (Charlecote Way 62, Fenwick Street 50, Hartwell Common 0) | uncertainty | guideline 7 and Appendix A: the same drawn days set against firm capacity | 45 to 72 at Charlecote Way and 41 to 65 at Fenwick Street, wide because each peak sits near firm capacity; 0 to 4 at Hartwell Common | unfinished chain: the same days around the wrong centre: 0, 0 and 0 per cent at Charlecote Way, Dunmore Street and Fenwick Street, 62 at Hartwell Common | R3, R6, R7 | Ask 5 |
| R11 | The primaries to commit for reinforcement: Ashcombe Road, Charlecote Way, Dunmore Street and Fenwick Street; Hartwell Common held | synthesis | guideline 7: commit where the peak would exceed firm capacity on more than one design day in ten; every variant gives the same list | exact: the list of four | dismissed own evidence: the careful pass commits Ashcombe Road and Hartwell Common on three assumptions a run writes into its own caveats (the line carried past its data, the customers' diversity, the planned dates) and does not size | R9 | Recommendation |

Carry-forward: none is offered, since the platform grades every figure against the golden. R1, R2, R4, R5 and R7 are each measured from files of their own and are the five Critical Components, so a slip in one costs only what hangs on it: R3 falls with R1 or R2, R6 with R4 or R5, and R8 to R11 with R3, R6 or R7, in each case at the primary concerned alone, because every result is a table by primary (a wrong cold end at Dunmore Street leaves the other four primaries' cells right).

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Heating demand steepens below freezing, and the service is instructed on the days forecast high, so the evenings without it are the mild and low-running ones | constructed (the simulated process) | no: the steepening is in 7 of nine primaries' records, the four with no flexibility zone among them, and the instruction rule runs at all five zones; the line reads Ashcombe Road and Fenwick Street low as well, where the list does not change | modelling: the mornings of every working weekday against temperature, and each evening's relation to its morning on the days no service ran; no evening without a service shows it | modelling: a two-stage model of the day, the cold end taken from hours the service never reaches | keep (R1) |
| A connected customer grows into a share of its agreed capacity over two to three years, by type | constructed (the simulated process) | no: 10 of 10 customer types and all nine primaries; at the four primaries with no flexibility zone the short reading is off by 0.05, 0.00, 0.49, 0.33 MW and decides nothing | a targeted query across the register and the settlement summary on the meter point, then modelling: each type's draw by months since energisation | modelling: a build-up by type scaled to each customer's own level, carried to the assessment date | keep (R2) |
| Sites pass their commissioning test late by an amount that depends on the asset class, and some are withdrawn | constructed (the simulated process) | no: six classes across 29 zones and five providers; the planned dates read the megawatts in service long at Ashcombe Road and Charlecote Way too, where the list does not change | the class medians show in one group-by of the register; the megawatts need modelling of the share in service by days since the planned date, with the sites still to come and the sites withdrawn counted | modelling: commissioning by class with the sites still to come and the sites withdrawn in the record, given how long each site is already overdue | keep (R4); a run that stops at the group-by keeps the list and loses the megawatts at two primaries (Effort test, sensitivity) |
| Curtailed load comes back in the four half-hours after the window | constructed (the simulated process) | no: every event at all five zones and both providers; it moves the peak at Ashcombe Road alone and runs at four primaries where it changes no call | a targeted query: the event days' half-hours after the window against the day's evening without a service; both architecture 6 runs made it unprompted | modelling: the day replayed half-hour by half-hour | keep, as a result a careful run earns (R7, Right in the careful column) |
| What a provider has available falls as the day gets colder and is capped by the megawatts in service | constructed (the simulated process) | no: both providers, all five zones, three winters | modelling: a met call shows only a floor, so the share is fitted with the met calls as floors; both architecture 6 runs capped it unprompted | modelling: a censored fit against temperature | keep, as a result a careful run earns (R5, Right in the careful column) |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 design-day demand in winter 2025/26, MW | Partly | Missed | Right |
| R2 megawatts the register's customers add by 15 January 2028 | Missed | Partly | Right |
| R3 design-day demand before flexibility in winter 2027/28, MW | Missed | Missed | Right |
| R4 megawatts each provider will have in service on the assessment date | Missed | Missed | Right |
| R5 the share of its megawatts in service each provider has available on the design day | Partly | Right | Right |
| R6 megawatts each contract delivers between 17:00 and 18:00 | Partly | Partly | Right |
| R7 megawatts that come back after the window per megawatt delivered | Missed | Right | Right |
| R8 the day's expected peak with the service instructed in full, MW | Missed | Missed | Right |
| R9 the level the peak stays under on nine design days in ten, MW | Missed | Missed | Right |
| R10 the share of design days over firm capacity, per cent | Missed | Missed | Right |
| R11 the primaries to reinforce | Missed | Missed | Right |
| Roughly | 1.5 of 11 | 3 of 11 | 11 of 11 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (generator/effort_passes.py computes each pass end to end on the cut pack; no cell is hand-graded)
Largest single hint: "a provider's availability follows the megawatts in service, and the sites still to come commission as late as their class has across the register, not on the planned dates"; rescues 2 of 11 results (R4 and R6). The cold-end sentence rescues 1 and the build-up sentence 1; the strongest compound sentence (any two of the three together) rescues 3 of 11.
Pair estimate: 24.5 (quick 17.3, thorough 100.0)

The careful column is calibrated to the two architecture 6 runs, graded up wherever they made the move unprompted:
hygiene, the switching days, an event's megawatts against the day's own counterfactual, the share capped at the
instruction (R5 Right), the come-back replayed over the whole day (R7 Right), a predictive nine-days-in-ten level by
drawing days. Where a result needs a move beyond those, the pass takes the reading both runs gave: a straight line
through the days without a service carried to the design temperature (both runs fitted it and named the carry as an
assumption), the customers due after the latest winter at their type's established share (the runs took them in full,
which is the quick pass), and the sites still to come on their planned dates (the runs took availability to scale with
the megawatts contracted). A held-out winter and a chronological choice of model do not move it: every held-out evening
without a service is a mild one, and each zone's own past winters confirm the planned dates on classes the new awards
are not made of. It commits Ashcombe Road and Hartwell Common; the quick pass commits Hartwell Common.

What each sentence of help does to the careful pass (effort.json hints):

- "the days without a service stop near 2 C and are the low-running ones, and the heating load steepens below freezing: read the cold end from the hours before the window, which every day carries": rescues 1 of 11 (R1); the careful pass told it commits Ashcombe Road, Dunmore Street, Hartwell Common
- "a customer draws a share of its agreed capacity that depends on its type and takes two to three years to reach it: count every register customer's rise between the two assessment dates": rescues 1 of 11 (R2); the careful pass told it commits Ashcombe Road, Charlecote Way
- "a provider's availability follows the megawatts in service, and the sites still to come commission as late as their class has across the register, not on the planned dates": rescues 2 of 11 (R4, R6); the careful pass told it commits Ashcombe Road, Fenwick Street, Hartwell Common
- "both of the first two sentences (the cold end and the customers' build-up)": rescues 3 of 11 (R1, R2, R3); the careful pass told it commits Ashcombe Road, Charlecote Way, Dunmore Street
- "both the cold end and the commissioning sentences": rescues 3 of 11 (R1, R4, R6); the careful pass told it commits Ashcombe Road, Dunmore Street, Fenwick Street, Hartwell Common
- "both the build-up and the commissioning sentences": rescues 3 of 11 (R2, R4, R6); the careful pass told it commits Ashcombe Road, Charlecote Way, Fenwick Street

Sensitivity, recorded and not the gate: if a run also groups the asset register by class and reads each class's
lateness from the sites commissioned alone (one group-by of one file, the most reachable of the three judgments), the
pass earns 3.5 of 11 results, scores 26.9 and commits Ashcombe Road, Fenwick Street, Hartwell Common. Single sentences then rescue at most
2 result(s), but only two judgments are left, so the two sentences naming both (the cold end and the build-up)
rescue 5 of 11 (R1, R2, R3, R9, R11); that composite sits 0.40 MW over firm capacity at Fenwick Street and 0.89 at
Hartwell Common. The bar's compound test holds on the measured calibration (3 of 11) and not on this one.

The list each route files (effort.json routes; 7 different wrong lists over 18 shortcuts):

- Ashcombe Road, Charlecote Way, Dunmore Street, Fenwick Street: every result of the chain; each class's record read from the sites commissioned alone
- Ashcombe Road, Charlecote Way, Fenwick Street: each evening half-hour on a straight line through the days no service ran, three winters; the same line through the latest winter's days alone; every working weekday with the megawatts scheduled as a regressor
- Ashcombe Road, Dunmore Street, Fenwick Street, Hartwell Common: customers due after the latest winter, agreed capacity in full; the same customers at the average share today's customers draw; the same customers at their type's established share; every customer at what the latest months show, no further build-up
- Ashcombe Road, Dunmore Street, Fenwick Street: the same customers on their type's build-up
- Ashcombe Road, Charlecote Way, Dunmore Street: the megawatts contracted, at the share the events delivered of their contract; the megawatts contracted, at the share of megawatts in service; the sites still to come on their planned dates; the zone's own past share of its contract in service in mid January; the sites still to come on the provider's record across its classes; the sites still to come on the register's record across every class
- Charlecote Way, Dunmore Street, Fenwick Street: the delivery taken off the 17:00 to 18:00 peak
- Ashcombe Road, Hartwell Common: careful but hurried: the line, the type's established share, the planned dates
- Hartwell Common: quick: the latest winter's line, agreed capacity in full, the contract at face value, the expected day

## Data provenance

Source: generated by the generator from a simulated process (generator/world.py simulates the DSO, its customers, its providers and the control room; pack.py writes what their systems record).
Behaves like the real thing: the process simulated is a DSO's constraint managed zones over three winters: demand at nine primaries driven by the station's daily mean temperature, with heating that steepens below freezing by an amount that depends on the primary, a day effect common to the zone and one of each primary's own, and a half-hourly shape by customer mix; a day-ahead forecast with its own error; instructions sized to hold each primary at 92 per cent of firm capacity in half-megawatt steps, capped at the contract, revised or cancelled on the morning; providers that deliver what is scheduled while their sites in service can and a share of them that falls with the cold when they cannot, with the load coming back after the window; customers that connect on a register and grow into a share of their agreed capacity over two to three years by type, each at its own level and pace; providers across 29 zones signing sites of six classes that pass their commissioning test a little early, on time, months late or never, by class and a little by provider; ordinary 11 kV switching. No effect is placed where it decides: each runs across every primary, customer type, class and provider, with a place where reading it wrongly decides nothing (checks.py BAR R5).
Genuine patterns: (1) seasonal and cold-spell temperature with day-to-day persistence, and demand rising with heating degrees at a slope by primary that steepens below freezing at 7 of nine primaries; (2) a weekday and weekend half-hourly shape by customer mix, a Christmas dip and year-on-year growth by primary; (3) instructions larger on colder days and on bigger forecasts, met when mild and short when cold, the available share falling as it gets colder by provider; (4) load coming back after every event, more for the heat-pump portfolio; (5) customers building up over two to three years to a share of agreed capacity that runs from 0.22 to 0.59 by type, with their own levels and paces; (6) commissioning lateness skewed by class (medians from 29 to 248 days), with sites withdrawn and 3.3 per cent passing on or before the planned date; (7) day-to-day scatter common to the zone and specific to each primary.
Problems by process: point renames at the historian's asset ID migration; held and bad values from comms outages and a CT fault; rows the outstation never sent; a monthly extract re-sent; superseded instruction revisions and provider names as typed; raw and checked weather readings; two-row transfers in the switching log; withdrawn, superseded and quoted offers and legacy feeder codes in the growth register; superseded entries and class names as typed in the asset register; part months in the settlement summary.
Breadth: 196,240 SCADA rows (nine primaries, three winters, half-hourly), 360 dispatch rows, 13,319 weather rows, 60 switching rows, 13,715 customer-months for 234 customers, 1,575 asset register rows for 1,536 sites in 29 zones under five providers, 136 growth register rows; 14 files, three of them never read by the assessment. Which hours, which customers and which sites carry each quantity has to be worked out before anything is fitted.

## Template check

Chain signature: causal-reasoning, missingness-measurement, forecasting, modeling, missingness-measurement, forecasting, investigation-loops, forecasting, uncertainty, uncertainty, synthesis
Question form: which (which of the zone primaries to commit to reinforcing), then each figure asked for by primary
Nearest build: task17 (a distribution and where it is cut, with the weight on modeling: a resampled distribution of one statistic, its modeling the resampling design). What differs: the chain (this one builds each primary's peak from three structural models of a physical process, replays a day and cuts at a firm capacity rule; the two signatures share no run of three areas), the unit (five primaries on one design day), the data (telemetry, a dispatch log, a connections register, a site register) and the answer (a list of primaries with each one's level). Architecture 6 of this slot shares the world and not the chain, the weight (validation) or the answer shape.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | the design day | a working weekday at a GMT-day mean of minus 3.0 C; a local-day mean; any day of the week; Christmas week | a Monday to Friday that is not a bank holiday and not 24 December to 2 January, at a mean of the station's hourly readings for the GMT day of minus 3.0 C | guideline 2: "The design day is a working weekday on which the daily mean air temperature at Halverton weather station is minus 3.0 degrees Celsius. The daily mean is the mean of the station's hourly readings for the GMT day." |
| SF2 | the assessment date | 15 January of the winter; the winter's start; its coldest day | 15 January 2026 for the latest winter and 15 January 2028 for the winter assessed | guideline 2: "A winter's design day is assessed as at 15 January of that winter, the assessment date." |
| SF3 | which design days | every design day; only the days a service would be instructed; only the days it would not | every design day | guideline 2: "The assessment concerns every such day, whether or not a flexibility service would be instructed on it." |
| SF4 | the normal running arrangement | days with a logged transfer left out, for the demand and for what a service delivered; left in | left out at both primaries of the transfer | guideline 3 ("no load transferred to or from the primary across a normally open point") and guideline 6 ("What a service delivered is taken only from days on which the primary was in its normal running arrangement."); left in, the list is the same |
| SF5 | growth | the DFES rates compounded for each year between the winters; one year; simple | two years compounded, every half-hour in the peak's proportion | guideline 4: "for each year between the two winters, compounded" and "Every half-hour of the design day is taken to grow in the proportion its highest half-hour grows." |
| SF6 | the customers counted | every accepted or energised customer on the register, for what it adds between the two assessment dates; only customers energised between the dates; quoted offers too | every customer on the register as saved, accepted offers on the date the register holds, withdrawn, superseded and quoted offers left out | guideline 4: "the demand that the customers on the load growth register will have added to the primary's demand between the two assessment dates", "an offer counts once it is accepted", "offers withdrawn, superseded or only quoted are not counted" |
| SF7 | the form of the mornings' temperature response | a curve with fixed knots; two lines meeting at a fitted knee; a curve below a fitted knee; the cold days' own line | a curve through the mornings of every working weekday | same call: three variants give the same list and every figure inside its band |
| SF8 | the hours taken as the morning | the half-hours ending 07:00 to 15:30; those ending 09:00 to 15:00 | 07:00 to 15:30, none inside a service window | same call |
| SF9 | the winters behind the latest winter's demand | three winters with a level each; the two latest; the latest alone; a drift read at 15 January | three winters, the latest winter's level | same call: three variants give the same list inside the bands |
| SF10 | how an evening is tied to its morning | each half-hour as a ratio to the day's morning, on the days no service ran; regressed on the day's own morning | the ratio | same call |
| SF11 | a customer's demand | mean demand 17:00 to 18:00 on working days; maximum demand; consumption | the summary's mean_kw_1700_1800_working_days | guideline 4: "the settlement team's monthly summary gives each half-hourly metered customer's mean demand between 17:00 and 18:00 on working days" |
| SF12 | a customer's own level and the build-up's shape | its latest three months; its latest six; its type's level; a build-up with or without a slow start | its own latest three months carried up its type's build-up | same call: three variants give the same list inside the bands |
| SF13 | the sites counted | the sites on the register as extracted; sites a provider might still add | the register's live entries as at 4 November 2026 | the award notice: "No site may be added to a 2027/28 schedule after 16 October 2026"; no site on the register was signed later |
| SF14 | in service | from the commissioning test until withdrawn or left; from the planned date; from signing | from the day a site passes its test until it is withdrawn or leaves the service, on the assessment date | guideline 6: "a site is in service from the day it passes that test until it is withdrawn or leaves the service" and "sites in service on the assessment date" |
| SF15 | the record a site still to come is read on | its class across the register; its class with its own provider; a fitted distribution by class; the sites withdrawn left as still to come | its class across the register, the sites withdrawn counted as never commissioned | same call: three variants give the same list inside the bands; the sites commissioned alone are ruled out by the 30 of 143 process load sites still to come and 9 withdrawn, and keep the list |
| SF16 | megawatts delivered | the mean of the half-hours ending 17:30 and 18:00; the whole window's mean; the largest half-hour | the mean of the two half-hours | guideline 6: "A contract's megawatts delivered are quoted as its mean delivery in the half-hours ending 17:30 and 18:00." |
| SF17 | the share's line and the calls that were met | a line in temperature with the met calls as floors; a curve; flat above 2 C; the calls that fell short alone | a line on the log of the share, the met calls as floors | same call: three variants give the same list inside the bands |
| SF18 | instructed in full | the megawatts contracted for 2027/28, for the whole window; the megawatts a forecast would call | the megawatts contracted in the award notice, scheduled for the whole service window | guideline 6: "instructed in full: the megawatts contracted for that winter in the contract award notice, scheduled for the whole of the service window" |
| SF19 | the peak with flexibility | the day's highest half-hour, whichever it is; the highest half-hour inside the window; the 17:00 to 18:00 demand less the delivery | the highest of the 48 half-hours with the service delivered through its window | guideline 6: "its highest half-hourly demand on the design day with the service delivered through its window, whichever half-hour that falls in" |
| SF20 | one design day in ten | over the variation from one design day to another; over the estimates' own uncertainty | day-to-day variation of demand and of what a provider has available | guideline 7: "taken over the variation from one design day to another as the record shows it, not over the uncertainty of the assessment's own estimates" |
| SF21 | firm capacity | Appendix A; recomputed from the register's ratings | Appendix A | guideline 5 and Appendix A; the register's ratings recompute to the same figures (same call) |
| SF22 | megawatts contracted | the award notice's 2027/28 table; the previous winter's | the 2027/28 awards | the award notice, section 2 |
| SF23 | the nine days in ten | the 90th percentile of drawn days' highest half-hours; a normal reading at the peaking half-hour | the drawn days | same call: the normal reading is within 0.3 MW at the primaries that peak inside the window |
| SF24 | a cancelled instruction's day | a day without a service; left out | a day without a service | same call: with the 27 cancelled instructions' days left out, the same list and every figure inside its band |
| SF25 | delivered between 17:00 and 18:00 | the mean of the half-hours ending 17:30 and 18:00; either half-hour on its own | the mean of the two | guideline 6 (SF16); either half-hour alone is within 0.05 MW at every primary (same call) |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | the five zone primaries of the award notice, and every design day whether or not a service would be instructed; filed (guideline 1 and 2, the awards; SF3) |
| 2 Unit of account | a primary substation, MW at its SCADA total (guideline 3); a customer's mean kW from 17:00 to 18:00 on working days (guideline 4, SF11); a site's registered kW (guideline 6) |
| 3 Attribution window | megawatts delivered as the mean of the half-hours ending 17:30 and 18:00 (guideline 6; SF16, SF25); the day's highest half-hour for the peak (SF19) |
| 4 As-of dating | the exports of 1 to 4 November 2026, the growth register saved 30 October 2026, the awards of 21 October 2026, the asset register as at 4 November 2026; the assessment dates 15 January 2026 and 15 January 2028 (SF2); C1, no later record is read |
| 5 Version basis | guideline issue 5, awards WPN-DSO-FLX-2026-07; the latest revision of each instruction, the checked version of each weather hour, the register's live entries; filed and C1 (BAR R2) |
| 6 Denominator | megawatts in service on the day for the share (guideline 6: what the provider's sites in service can be expected to deliver); agreed capacity for a customer's draw; megawatts contracted and megawatts scheduled are rivals ruled out by data |
| 7 Weighting | each completed event once; each site by its registered kW; each customer by its own demand; C1 |
| 8 Window length | the latest complete winter for the demand (guideline 3), read with three winters of days (SF9); three winters of events; the register's whole history |
| 9 Boundary inclusivity | "exceed its firm capacity on more than one design day in ten" strictly; no primary within 0.74 MW of firm capacity at the nine-days-in-ten level across the variants (margins, asserted) |
| 10 Rounding path | unrounded to the end; MW to one decimal place and the share of days to the nearest whole per cent, as the prompt says |
| 11 Tie-break | none: no primary at its firm capacity, and the answer is a list, not a ranking |
| 12 Maturity and censoring | winter 2025/26 complete; a met call shows only a floor on the share (SF17); a site still to come is counted for as long as it has been watched and a withdrawn site as never commissioned (SF15); a customer's build-up is read from customers at every age (SF12) |
| 13 Order of operations | cleaned, the latest winter's demand, growth, the customers, the sites, the share, the day replayed, the days drawn; C1 |
| 14 Row order | the dispatch log by reference and revision; the switching log by time; the asset register by site reference and status date; C1 |
| 15 Duplicate resolution | the re-sent SCADA overlap once; each weather hour at its checked version; superseded register entries left out; C1 (BAR R2) |
| 16 Identity normalisation | SCADA points under both names; feeders under both codes; providers and classes as typed; customers by MPAN core; C1 (the L1 checks) |
| 17 Netting against gross | nothing is netted; the logged transfer days are left out (guideline 3 and 6, SF4) |
| 18 Dimensional units | MW of real power, not Mvar; kVA of agreed capacity against kW of demand; kW registered against MW contracted; each in its file's own column name |
| 19 Code and status semantics | quality G kept; status Completed for an instruction's latest revision, a cancelled instruction's day (SF24); Accepted and Energised customers (SF6); Commissioned, In delivery, Withdrawn and Left service sites (SF14); filed and C1 |
| 20 Integerisation | the share of design days to a whole per cent; megawatts continuous; no count is graded |
| 21 Clause scope | guideline 2 to 7 and Appendix A for the peaks and the call; the award notice's sections 1, 2 and 4 for the megawatts and the schedules of sites |
| 22 Forward window contents | winter 2027/28 as at 15 January 2028: its contracts instructed in full, two years of growth, the customers the register holds on their dates, the sites the register holds (none added after 16 October 2026, SF13); filed |

## Literal reader

Guideline 2: the design day is a working weekday at a GMT-day mean of minus 3.0 C, every such day counts whether or not
a service would be instructed, and a winter is assessed as at 15 January (R1 to R11's condition). Guideline 3: design-day
demand is the primary's half-hourly demand on that day with no service delivered and no load transferred, for the latest
complete winter (R1). Guideline 4: the DFES rates compounded, plus what the customers on the register as saved will have
added between the two assessment dates, a customer's demand being its mean from 17:00 to 18:00 on working days, every
half-hour in the peak's proportion (R2, R3). Guideline 5 and Appendix A: firm capacity (R9 to R11). Guideline 6: the
contract instructed in full for the whole window and credited with what the provider's sites in service on the
assessment date can be expected to deliver; a site is in service from its commissioning test until withdrawn; megawatts
delivered quoted as the mean of the half-hours ending 17:30 and 18:00; what a service delivered taken only from normal
running days; the peak is the day's highest half-hour whichever it is (R4 to R8). Guideline 7: commit where the peak
would exceed firm capacity on more than one design day in ten, over the variation from one design day to another, and
report the share of design days (R9 to R11). The award notice: megawatts contracted for 2027/28 and the four winters
before it, the service's terms, and that no site may be added to a 2027/28 schedule after 16 October 2026 (R4). The
prompt: which primaries to commit, and for each one its demand before flexibility, the megawatts its contract can be
expected to deliver between 17:00 and 18:00, the day's expected peak with the service instructed in full, the level that
peak stays under on nine design days in ten and the share of design days over firm capacity; MW to one decimal place and
the share to the nearest whole per cent. Every sentence executes to the golden's quantity. None says how demand at the
cold end is to be read, how a customer's demand relates to its agreed capacity or its age, how late a site commissions,
that load comes back after a window, or how a spread is measured.

## Prompt contract

A voice rewrite may not drop or change: the question (which of the Halverton zone primaries to commit to reinforcing for
winter 2027/28); the design day; for each primary its demand before flexibility, the MW its flexibility contract can be
expected to deliver between 17:00 and 18:00, the day's expected peak with the service instructed in full, the level that
peak stays under on nine design days in ten and the share of design days it would be over firm capacity, each set
against firm capacity; a workbook with the figures and a few slides for the capex review; MW to one decimal place and the
share to the nearest whole per cent. It must never add: a file name, who is asking, how any figure is to be estimated,
the words morning, build-up, asset class, commissioning, come back, rebound or censored, a temperature, a count of
zones, winters, customers or sites, or a warning of any kind.

## Leak rulings

leak.py --asof 2026-11-04 on target.zip a40205c5: REVIEW, no LEAK (sweeps 1, 2, 5, 7 to 12 clean). Ruled in the main
thread; the stage 4 reader has not read this cut.

- Answer figures in the pack (27.5, 25.6, 20.0, 35.0 and 24.4, and 27.0 for a primary with no zone): the firm
  capacities of guideline Appendix A, which every answer block quotes beside its levels. Each is an input; none is a
  result. 27.0 is also Charlecote Way's nine-days-in-ten level, a coincidence of one decimal place with Wexley Hill's
  firm capacity.
- The committed call's words in the guideline and the award notice: the primaries' names, reinforcement, firm capacity
  and winter 2027/28 are those documents' own subject; neither names a primary to reinforce.
- Design-note vocabulary in the two documents (megawatts, register, record, the primaries' names, guideline, window,
  half-hour, planned, customers, provider): the service's own terms. No document says how demand at the cold end is to
  be read, how a customer's demand relates to its agreed capacity or its age, how late a site commissions, that load
  comes back after a window, or how a spread is measured (checks.py, documents name no step).
- Candidates beside numbers (the guideline's Appendix A, the award notice, the asset register, the dispatch log, the
  substation register, the transformer condition file): ratings, contracted megawatts, registered kW, megawatts
  scheduled and oil results. None sets a primary's demand with flexibility against its firm capacity (Gate G).
- metadata.json, the monthly summary's coverage line ("January 2021 to October 2026", "customers"): the months the
  file covers and whose demand it holds; it names no method. metadata.json sits outside the ZIP.
- Dates after the setting: none flagged. The asset register's planned commissioning dates in 2027, the growth
  register's planned energisation dates and the award notice's contract period are forward-looking records each of
  those files exists to hold (reduce-house-fixes H16); no extract carries a recorded event after its own date
  (checks.py, documents: dates in order).
- Single-use test: every file the results read has a use of its own. The SCADA export is the demand side's source and
  the events' measure; the dispatch log is the DSO's instruction record; the switching log is the control room's;
  the settlement summary covers every half-hourly metered customer in the zone, most of them not on the growth
  register; the asset register is the DSO's licence-wide register of every provider's sites, across 29 zones; the
  award notice carries the megawatts, the service's terms and the schedules' closing date. No file exists to carry a
  result, and none describes the data.
- The one sentence this architecture added to close a fork (guideline 6, "What a service delivered is taken only from
  days on which the primary was in its normal running arrangement") files which days count, a convention both
  architecture 6 runs applied unprompted; deleted, the list is unchanged and five figures leave their bands (SF4). It
  names none of the three judgments.

## Tried and rejected

- Architecture 6, nine-days-in-ten bands set by the variants with 0.1 MW either side: judge r3 (2026-11-10), from its
  own baseline and the share's scatter as measured, put Fenwick Street at 31.6 and Hartwell Common at 21.0, at and above
  the bands' tops. The share's own scatter joined the family (22 variants) and those bands reach 0.3 MW above it.
- Architecture 6, switching log references in generation order, ammeter readings an exact function of the megawatts,
  and planned jobs over New Year: the third cold reader named all three; references now run in time order, each reading
  has its own busbar voltage and power factor, and a transfer made over Christmas, New Year or a bank holiday is logged
  as fault restoration. No figure moved.
- Architecture 6, guideline 6 worded "The megawatts delivered are those in the half-hours ending 17:30 and 18:00 ... No
  other measure is credited": judge r2 (2026-11-10), deriving before it opened the blocks, credited the contract in
  those two half-hours alone, let the peak slide to 18:30 and reinforced all four primaries. A filed sentence whose
  literal execution gives another call is a fork whatever the events show, so the section now reads "A contract's
  megawatts delivered are quoted as its delivery in the half-hours ending 17:30 and 18:00 ... its highest half-hourly
  demand on that day with the service delivered through its window. No flexibility other than the contracted service
  is credited."
- Architecture 6, a floor of 7.8 MW on Ashcombe Road's megawatts delivered: judge r2's own fits (megawatts fitted over
  the whole record, zone level) gave 7.5 to 7.7. Megawatts fitted over every event and the three winters' own scaling
  joined the family (20 variants), the megawatts' band is never narrower than the share's band times the award, and the
  floor is 7.3.
- Architecture 6, the backtest's count of freezing-day events inside an 80 per cent range as a graded figure: judge r1
  (2026-11-10) reproduced every megawatt figure and found the count at 29 to 45 of 50 under its own cuts; across this
  generator's variants and six constructions of the range it runs 25 to 40. A figure reasonable methods spread that
  widely is unpinned, so the prompt asks the average miss alone and no count is graded.
- Architecture 6, bands set by nine variants of the golden's own choices: they left out the baseline an event's
  megawatts are measured against, the handling of a met call and a cancelled instruction's day, and the heating base
  was varied on the demand side only. A baseline scaled to the day's own level, a met call taken as a floor and a
  heating base of 14 C carried through the events each landed outside a stated band. The family is 17 variants and every
  band is the range they span.
- Architecture 6, Ashcombe Road at 16.0 MW contracted: megawatts per megawatt scheduled with the scatter carried in
  proportion reached the golden's three primaries with wrong megawatts (24.0 MW against firm 23.0), and the available
  share alone put its 18:00 half-hour over firm. At 21.0 MW the 18:00 half-hour is 22.0 MW, so Ashcombe Road needs the
  day rebuilt, or the share and the spread together, and none of seven shortcuts reaches the set.
- Architecture 6, the careful pass with the fit's own range and R3 priced as a result it loses: graded up to the
  megawatts of scatter its own fit leaves, carried unchanged, with its backtest earned (0.24 MW, inside the band: a
  held-out winter passes megawatts per megawatt scheduled too). With the asks numbered as the prompt lists them and
  the components as the findings they stand on, the pair estimate is 38.4 on eleven results (it was 42.5 on eight).
- Architecture 6, switching operations logged on the quarter-hour with durations in round hours: the stage 4 reader
  named the 15-minute steps; the log now carries the minute each operation was made, and no figure moved.
- Architecture 6, a deck and a chart title saying the three primaries are over firm "on nine design days in ten":
  Fenwick Street is over on about three; the titles now say "on more than one design day in ten" (guideline 7's words).
- Architecture 6, a two-winter event record with calls of the whole contract every time (architecture 5's dispatch):
  there was no megawatts-scheduled variation to test, and with calls sized to need over two winters Quillon's zones
  fell short on too few days (the variants of its share spanned 0.36 to 0.52). Three winters of events, calls sized to
  the forecast above 92 per cent of firm capacity, contracts sized so cold-day calls outrun what is available.
- Architecture 6, an S-shaped availability curve: a straight and a curved line through the cold days differed by 0.03
  at the design day and split Fenwick Street's megawatts by 0.4; the curve is now close to straight over the cold range.
- Architecture 6, a backtest by winter as the test between megawatts scheduled and megawatts contracted: it cannot
  tell them apart (0.24 against 0.20 MW), because the last winter's calls look like the earlier ones; the backtest
  separates growth with the contract from none, and the equal-temperature test and each provider's two zones separate
  scheduled from contracted.
- Architecture 6, the backtest's range counted on the days at or below minus 1.0 C: naming that cut in the prompt would
  have filed the golden's own choice of cold days; the prompt counts days below 0 C.
- Architecture 6, Fenwick Street at 10.5 or 12 MW contracted: its nine-days-in-ten level sat 0.15 to 0.45 MW over firm
  across the variants; at 10.0 MW it sits 0.3 to 1.0 over and its expected peak 0.1 to 0.8 under.
- Architecture 6, held (S) values: kept in, a held stretch inside an event evening tripled the scatter and moved every
  one-in-ten level; the outstations are polled on a second route through service windows, so no event evening is held.
- Architecture 5 (the provider's reduction net of the load a control room moved to the primary across an open point,
  read at minus 3.0 C; golden Ashcombe Road and Hartwell Common): spent on the platform's holistic audit of 2026-11-10.
  Both runs lost at the deciding step (rung 1b, Ashcombe Road alone, 0.67 to 0.75 per MW at the zone meter; a method
  shortcut and a self-confirming check) and the audit still read the step as a plant: the neighbours step up a flat
  1.4, 1.4 and 0.8 MW on event days whatever the megawatts scheduled, absent on cancelled days, so one sentence names
  it and one subtraction lands the call. A hidden concurrent action with a discrete signature is a planted factor
  however analytical the netting; the transfer is now documented texture and the deciding step moves to judgments
  the record has to settle (`runs/review_2026-11-10.md`).

- A mix shift by author tenure (new accounts' posts carry most review items, and AI took the newcomers): rejected at the
  draw, because the account-age column makes the segmentation a reflex the opponent runs on every visible attribute.
- Spam and flags scaling with page views rather than questions: rejected at the draw, because a per-queue trend of the
  flags already follows views, so the reflex lands, and the swap test reads it as generic demand forecasting.
- A volunteer pool with two retention types (veterans and casual reviewers) as a rung: dropped at the prototype, because
  the defensible retention estimators (tenure bands, pooled recent churn, a heterogeneity fit) split the per-site
  figures by up to 0.8 FTE; every site's pool now leaves at one steady rate since the pipeline dried up.
- Item and flag rates per question stepping up in 2023: dropped at the prototype, because a pooled ratio (over the
  step) and a reviewer trend over 2024 carry errors of opposite sign that cancel near the golden; both rates hold steady.
- Sizing the pool on the busiest 2027 month (shape 02): dropped at the prototype, because each late-2027 month's network
  hours carry about 300 hours of one-sigma spread, too wide for a monthly grid at any natural rounding.
- A volunteer pace with a wide spread across reviewers (KAPPA_SIG 0.60): the 2021 to 2023 and 2024 to 2026 saturated
  paces differed by 3.6 per cent, which moved Data & ML across its bin between eras; reviewers' own paces now spread at
  0.15.
- A Poisson trickle of new reviewers after the pipeline dried up: carried or dropped, it moved two sites by 0.4 FTE; the
  trickle is now a floor share (0.004) of the old inflow, and no construction moves a site.
- Pre-platform reviewers' grant dates drawn freely: they piled up at January 2013; tenure is now bounded by each site's
  launch on the register.
- Cover targets calibrated against random-walk inflows and exits: the calibration moved the wrong way; exits and inflow
  are now constructed (zero-sum swings within each quarter), and the January to September 2026 cover targets of
  Databases and Embedded & Hardware were set at 1.137 and 0.76 to centre their needs in their bins.
- Question moves drawn by source site: they ran the wrong way and reached 90,000 rows; moves are drawn into each
  destination at 0.55 of the first shares (49,530 rows).
- October to December 2026 on the chart with no question driver: a trend of each site's questions would be an open
  fork; the plan workbook carries the planning team's outlook sheet for those months, used only for the chart.
- WFM shifts of 7.5 paid hours: half the quarter totals ended on a half hour, a rounding fork at the nearest hour;
  shifts are now 8 paid hours, short days, overtime and corrections in whole hours.
- First actions on flags with an unbounded lognormal tail: some ran past the moderator tool's export run, dating rows
  after the as-of; a flag left past 90 hours is now escalated and taken within the next week of hours (no Ask A figure
  moves), and a review still open at the export keeps its first action as the handled time.
- The network first named Quernstone: a UK accounting firm carries that exact name (Companies House 04197485); the
  network is now Millrind (no company, network or software of that name found).
- Ask C's stop "each move applied in the month it moved": it files the golden's nine (no move straddles the window's
  edges enough to cross a rounding step), so it is recorded as a convergence, not a stop; Ask A's over-correction stop
  (reviewed flags dropped) misses 14 of 27, not 27.
- target.zip cut with a `target/` folder inside: the archive now carries the files at its root (house fix H4).
- Round 1, Ask C's device left silent (no file said how the old statistics job counted a moved question): the judge
  licensed three readings one decimal apart at every site (FIX_NOW). The warehouse notes now file the old job's counting
  and the comparison basis in the data team's voice; both other readings are asserted out. The device is no longer
  silent, so the cracker and the mirror both land Ask C (cracker sheet `hit`).
- Round 1, slide 2's series undefined (hours worked or need hours, flags in or out, which close standard, how October
  to December 2026 is counted): the operations notes now define paid review hours once, the prompt asks each year's
  actual hours totalled, and the three actual totals are graded and asserted (36,419, 36,233 and 29,626 hours); being
  construction figures, both top responses land them (cracker sheet `hit`). With Ask C, the pair ceiling moves from
  31.0 to about 41.0, over the 40 build target and under the 50 bar; precut fails its pair-ceiling and cracker rows on
  this alone, reported to the coordinator.
- Round 1, the roster missed the reviewers whose access lapsed in January or February 2024 without a platform review
  (its dictionary scope said every reviewer with access since 1 January 2024): a lapse rate read by lapse date then
  counted zero lapses in those months (1.92 per cent, 33). The 689 rows are now in the roster (first review blank), the
  dictionary's scope and lapse rule carry a worked example, and the lapse-date reading files the same nine.
- Round 1, the items no volunteer ever picks up drawn at one share for every item type: routed shares were identical
  across types in slack months, which read synthetic. Each type now has its own (close votes 0.91, low quality 0.72,
  edits 0.40, first posts 0.35 per cent); no graded figure moved. In saturated months the shares stay close across types
  because the 72-hour hand-off takes the oldest items first whatever their type; a per-type volunteer preference would
  change the routed mix that prices the frozen call, so it was not added.
- Round 1, the 24-hour share's denominator and the envelope's sign: the flag service standard now defines flag
  response as a share with the post-deleted closures out of both counts, the prompt names the measure (24-hour flag
  response), and the prompt asks how far above or below the envelope the request sits.
- Round 1, the question plan's 2026 actuals sheet stamped as pulled 8 October inside a workbook issued 18 September:
  the sheet now carries January to August 2026 as pulled on 14 September (no figure reads it).
- Round 2, Ask C held only less careful solvers once round 1 filed the old job's counting (the cracker landed it, precut
  failed): the 2022 sheet now carries the tag-sync undercount of May to August 2022 as first reported, with the
  statistics job's March 2023 restatement below its notes (sites down, months across); the careful-but-literal path
  misses all nine (nearest 0.27 points) and the golden's nine figures are unchanged.
- Round 2, the chart's three actual yearly totals (round 1): construction figures both top responses land; out of the
  prompt and the deliverable answers. The chart is graded on its content, its series filed in the operations notes and
  its months on the workbook's Monthly hours sheet. The pair ceiling is back to 31.4.
- Loop 3 (2026-10-27), the portal landed the call: both responses filed 35 FTE (the then golden) by building capacity
  against the inbox at the saturated pace and carrying each pool at its own lapse rate; the capacity framing was every
  strong solver's default, so it is now the default path and the decisive step moved to how the pool is carried.
- Two retention types with the pipeline drying in late 2024 or summer 2025: a trend of the network's lapse rate,
  extrapolated, landed the golden by coincidence (the closed pool's decline was already plain in the record); review
  access now closes on 1 September 2026, so the record shows only an open pool's flat rate.
- Grants following the question level squared (older pools at the sites AI hit hardest): the separations shrank and the
  trended-rate routes still tracked the golden; grants now follow the question level.
- Grants drying in January 2026 with the last twelve months' grants carried on: the two errors cancelled on the golden;
  with invitation-only access filed, no window of past grants is a reading of 2027.
- Invitations at 2 per cent of the old flow: carrying or dropping them moved a site by 0.44 FTE in all; invitations
  are now a handful a year and none fell in September.
- Covers calibrated by re-drawing the whole pool at each step: a site's need jumped by up to a whole FTE between
  iterations; each reviewer now draws from their own stream and each month's grants from a fixed quantile, so a cover
  change only adds or removes reviewers at the margin.
- The data dictionary, the file list, the operations notes and the warehouse notes (markdown): a file that describes the
  data is a leak (`dataset-generation` section 3); the conventions the asks and the chart need now sit in the operations
  handbook and the question count standard, and every export names its own columns.
- Annual netting at Databases and Infrastructure & DevOps 0.07 and 0.12 FTE from their bin edges, and the world's
  realised 2027 one bin lower at Data & ML (the 72-hour queue carries a short month's backlog into the next month's
  spare capacity): the three sites were re-centred slightly above their integers, and a day-by-day simulation of the
  hand-off on the forecast pool is asserted to file the same nine.
- Architecture 1 as a whole (2026-10-31, the batch 1 triage): the moderation pool's world, prompt and asks had been
  solved once on the portal and loop 3 kept them, so the slot is re-rooted in a new world with a new mechanism; the
  pool's leaving rate falling as fast leavers go first is spent for this slot.
- Re-root draw screens (2026-10-31), each rejected before any data was cut: a mixed-population flood frequency (spent
  in task273 and task130's notes); an event-driven trial's event count (task171 and task174 hold it); a dialysis
  cohort's eGFR slopes (a patient-level slope is the obvious route and the method forks); a vineyard's frost nights
  under inversions (dead in task170's notes); a health system's access change and a climate-extremes count (both
  measured dead in task174 and task170's notes); this slot's own frailty and tenure hazard (architecture 1).
- The first card probe for this draw carried `validated_decoy` true and Gap 1 first: BLOCKed on
  `two_layer.validated_decoy` (a closed record built to bless the wrong method) and on a structural signature spent in
  five builds. The design is drawn so the meter's own high-water-table storms and the overflow log refute one response
  per millimetre for anyone who checks them, and population (the meter's days are not the replay's) is the decisive gap.
- A June 2025 high river with storms in it (the spell centred in August): the meter logged three overflows in it that one
  response per millimetre misses, so the overflow log refuted the stop rung at the count level, a search signal; the spell
  now falls in a dry month of 2025 and the meter's logged overflows are dry-ground storms every rung reproduces.
- The spell's peak held below the replay's wettest days (12.6 km of sewer below the water table against 20): 812 replay
  days sat above anything the meter saw, so the deciding configuration was out of sample and the infiltration had to be
  extrapolated; the spell now reaches the replay's wettest days (one replay day above the meter's maximum).
- Pumps below the wet-winter base (92 to 100 L/s): the station spilled in dry weather on groundwater alone and the
  consent's 24-hour rule merged wet weeks into single long overflows, so more inflow could file fewer overflows and the
  count was not monotone in the flow; the pumps now sit above the wettest dry-weather peak and every overflow needs rain.
- Assumed unit hydrograph shapes and a crown or centreline reference for the submerged length: the replay spread 2.1 to
  5.0 a year, but only because those variants fit the meter two to three times worse; among fits within a few per cent of
  the best the figures agree inside the whole-number bin, so the figures are graded to whole overflows a year.
- Architecture 2 (the PS03 overflow replay with each day's own water table), returned FAILED_TO_STUMP on 2026-11-07:
  both responses landed the hold call. Response 1 replayed 2004 to 2023 and filed 48 overflows against the 40 the
  consent allows, then 2 after the upgrade; Response 2 filed the same hold. Any full-record replay with the subdivision
  already broke the consent, so the decisive step (each replay day's own water table) was never needed. Lesson: the easy
  route has to be the one strong solvers actually file, and it has to land on the wrong side; a count of rare
  exceedances spreads with every modelling choice, so the call now sits on a mean quantity whose naive family is tight.
- Judge round 1 (2026-11-07, FIX_NOW on the asks; the call forced, Gate G analytical_non_defect, Gate H pass). Ask A's
  window read literally dropped the platform councils' last run (a 2 July 2026 date in the period-end column): FP-04 now
  files the record's own convention (a pay period ends on a Sunday and is paid later that week; credited to the year it
  ends in), naming no platform and no weekday the advices carry. Ask B's unit was open (raw, per invitation and day, or
  per organiser, invitation and day): the asking sentence now files it (a visit two organisers made counts for both, a
  moved booking once as held). Both asks were scoped to the 30 councils the branch covers while the prompt read as the
  round: cut to the round's 24, the regional platform's twelve councils re-sited inside the round on the same pay
  cycles, so no in-round figure moved. Ask 1's turnout figures had no rounding and a refit evaluating members at the
  extract sat about 0.7 points under: the guide now files each member as they will stand when the ballot period closes
  and the tracker files that period (1 to 15 March 2027); whole-per-cent figures were not adopted because five councils
  sit within 0.05 of a half point (Corrigan Valley 62.53, Halston 59.53, Pellham 58.49, Rosedene 45.51, Underhill 40.54),
  so a worksite-effects refit (lift 1.027) can cross a rounding edge; the prompt asks only whether each council reaches
  half, the side being determinate under every refit. freeze.py: the main side unmoved; the twelve out-of-round ask
  figures and block 4's turnout percentages were dropped by the repair (allowed, this line).
- Hardening noted, not applied (the judge rated stump power moderate to good: a model that fits the delegate term lands
  the call): ship the 2026-28 term as the organising coordinator's separate July 2026 election return rather than a
  sheet of the delegate register, so the register a solver opens holds the terms the online votes cover and the new
  term sits in a file read for its own purpose; the call, the stump and every figure would stay frozen.
- Judge round 2 (2026-11-07): DETERMINISTIC, the call reproduced with 6 points either side and no respecification
  flipping a council, stump power moderate to high. Before ship: step 8 reworded (the golden keeps the later, last
  updated row of a moved booking); the xlsx inputs' creator and last-modified-by set to the branch, the body that
  issues them; the 2021 declarations given the Producer of the LibreOffice release current at their June 2021 export
  (7.1; the info dictionary is the last object, so startxref moves and every object offset is asserted unchanged), the
  other four PDFs dated after 24.2's February 2024 release; and the hardening above applied: the 2026-28 term now ships
  as `delegate_election_return_2026.xlsx`, the returning officer's return, and `delegate_register_2018-2026.xlsx` holds
  the terms to 2024-26. No graded figure moved (freeze.py); the input gates hold (17 files).
- Surface at ship promoted three pairs on card axes alone: task157 (back to back, the same domain and objective; a
  petition sample's pair defects, not a turnout forecast, differentiated on the card), task154 (the calibration form
  realised_outcome_roster repeated two builds apart: redrawn to counterparty_acknowledgement, the agent's declared
  results being a counterparty's record) and task265 (left truncation in a descriptive survival estimate,
  differentiated on the card); heart PASS; left for the author's adjudicated clone check.
- Architecture 3 (the union branch's protected action ballots, each member read with the delegate in post at the
  ballot): FAILED_TO_STUMP on the portal 2026-11-07, both responses on the golden 11 councils. Both put worksite
  delegate coverage in the turnout model from the start and evaluated it at the ballot close with the 2026-28
  delegates, so the decisive step was the forecaster's reflex (a recorded covariate's forward value), and the July
  2026 election return, read by nothing else, announced it. Re-rooted to architecture 4 in a new domain and world.
- Architecture 4 draw screens (2026-11-08), each rejected before any card or data: vacancy chains through a
  fixed-post hierarchy (dead in task174's and task137's notes, and a stock-and-flow check of posts finds it); a
  programme's lead-in audience (task115 and task174); one facility's overflow into a sibling removed by an expansion
  (task308's reader named railheading and the full car park's hidden demand, and the swap reads the same for wards
  or car parks); ward acquisitions per colonised patient-day (task181: infection prevention's own reflex); errors
  per interruption or per handover (task198 and task173); wear accrued only in hours inside a band after a duty
  change, and pump failures per start after a control change (task307's driver); admissions that rise with spare
  beds (a filed bed opening prompts the question, and the forecast needs a fixed point whose estimator forks);
  speculative double bookings (the hygiene battery's de-duplication reaches it and the identity match is Layer 1);
  bus headways under a denser timetable (task308's probe replayed the operation and carried every knock-on).
- First prototype of this draw (hangs on days since power-up, any site-wide power-down a reset): the parameters put
  every hub below 99 per cent; the legacy cabinet repairs now isolate the hub every few weeks, hangs start only after
  about 75 days, and the high-power units sit near 99.5 per cent on the record.
- Hang restarts isolating the whole hub: the units then restart one another and the programme hubs stay above 99 per
  cent; a hung unit is restarted at its own breaker, and only the legacy unit's cabinet repairs, planned visits and
  supply interruptions restart the whole hub.
- Three hubs whose legacy units rarely needed the cabinet opened, failing on both routes: the hubs' legacy repair
  counts then predict the high-power hangs across hubs, and a hub covariate (legacy units at the hub, or their
  repairs) would extrapolate to the golden, architecture 3's failure again; every hub now has exactly one legacy unit
  with cabinet repairs of 10 to 12.5 a year, and the hubs that fail on both routes are three coastal hubs whose
  high-power units suffer ordinary corrosion faults.
- The learner given the hub's legacy jobs in the last 60 days, the days since its last legacy job or the days since
  its last planned visit (prototype, clean truth): none reaches the golden; at the programme hubs they carry 0.7, a
  noisy 0 to 1.4 and 0.4 to 0.7 hangs a unit-year against about 3.3, so each files the default path's set.
- Prototype 7 (the RC50's cabinet repairs at random, 10 to 12.5 a year, every unit at a hub on one pillar): the
  hub-year count of the RC50's work orders predicts the HX150 hangs (z of minus 4.8), and the Poisson model carried at
  the programme's zero files the golden plus a rural spur hub; the count of pillar power-downs files the golden
  exactly. A covariate's forward value lands the call, architecture 3's failure again.
- Prototype 8 (motorway visits two-monthly only from April 2024, rural spurs at 4.5 interruptions a year): the
  full-covariate model filed the naive set with programme hubs 0.01 to 0.3 from 99, a coin flip per hub over redraws.
- Prototype 9 (the coastal hubs' HX150 units on their own pillar, the RC50's repairs still random): the model on the
  RC50's work orders alone still filed the golden exactly; the random repairs carry the signal however the pillars sit.
- Prototype 10, adopted: the RC50's cabinet service is monthly, so its work orders a year carry no hang signal (z of
  0.3) and the HX150 units on its pillar never run 75 days; the hubs whose HX150 units sit on a pillar of their own
  carry every hang on record. Two inland hubs share that arrangement with the three coastal ones, because a record in
  which only coastal units ever ran long could not tell the sea air from the uptime (the deciding configuration has to
  be on record off the coast).
- Ask screens refused: double counting on a meter shared by two connectors (a billing defect a real operator fixes, so
  planted); tariff re-rate copies with new session IDs (a near-duplicate the battery's de-duplication reaches); a hub
  code renumbering (the battery re-derives the code from the charge point); meter replacements to break a register
  shortcut for Ask B (each needs a work order in a main-call file, an ask organ there), so a solver who takes each
  unit's register advance over the window keeps Ask B.
- The first cut's register opened on its Charge points sheet: leak.py sweep 12 read the first two rows' cells (the
  units' IDs, makes and models, which the programme names) as column names and called the programme a dictionary
  (LEAK); the register now opens on its Hubs sheet, the order an asset team keeps it in, and no figure moved.
- The full-covariate model before the RC50's work rose with the coast (the RC50's repairs as random at every hub): it
  filed 11 of the 12 on the clean truth, because the hang hubs' RC50 jobs ran low by chance and the zero at the
  programme hubs extrapolated far below the record; the RC50s at the five own-pillar hubs now need about twice the
  repairs (the coastal units' corrosion, the inland pair's 2017 units), so its removal lowers that model's forecast.
- Stage 4 round 1 (2026-11-08, on 4bf9959c): the judge DETERMINISTIC (APPROVE), the leak reader clean on questions 1
  to 6 with one mild item (every HX150 freeze call-out on record at the five own-pillar hubs, read as placed). Worked
  in one generator pass, the lines below; the call, the stump and the twelve hubs unchanged.
- RC50 outages awaiting Tavrin parts in 2026, to give the shared-pillar units some long uptimes (a module on order for
  weeks, the RC50 out of service and its pillar live): the outage months carried a signal the full-covariate model
  read, and it filed 12 hubs with seven standard programme hubs among them; the outage path is empty, and the shared
  units' occasional long uptimes come from the RC50's inspection-only months (one in five, the cabinet not opened)
  and skipped services instead.
- RC50 cabinet repairs cut to 1.0 a year at the shared-pillar hubs (fewer isolations, more shared hangs on record):
  the shared units then hung often enough at a thirteenth hub to list it; the repairs stay at 3.5 a year there and
  6.8 at the five own-pillar hubs.
- The five own-pillar hubs' HX150 units commissioned in 2022 and 2023 like much of the fleet: the full-covariate model
  read the commissioning year (the hang hubs' units among the newest) and carried it to the programme's new units,
  filing standard programme hubs; their units are now commissioned in 2021.
- Callout attendance read from each Faulted spell's length: the RC50's long repair spells inflated it at the shared
  hubs and the verifier's own forecast sat 0.05 points from 99; attendance is read from the work orders (attended less
  logged) over every callout, in the golden and the verifier alike.
- The day-step members of the standing family counted a hang's first day whole and released it a day late (about a day
  of downtime too many a hang): they sat up to 0.7 points under the simulation (Annagh Cross 99.05 against 99.30), the
  verifier's copy too; both now count the part of each day a hang is down, from a hang at mid-day on average, and agree
  with the simulation within about 0.15.
- Ordinary faults at about 0.4 a unit-year everywhere, the standard hubs' callouts at 2.3 days, the rural spurs at 7.4
  and 7.9 interruptions a year and comms faults at 0.15 a unit-year: the hubs outside the list sat 0.22 to 0.4 points
  above 99 on the golden, two of 20 redraws filed another set, the rate route's back-tests drifted past half a point,
  and the standard hubs' 2026 faults at that attendance put four of them under 99 in the January to October 2026
  record, so carrying 2026 held four of the seven; faults now run about a quarter a unit-year outside the coast, the
  standard hubs' callouts about 2.05 days, the spurs about nine interruptions a year and comms faults a tenth a
  unit-year, every hub's true side at least 0.48 points from 99.
- The five own-pillar hubs at 3.4 to 4.1 charges a day (the quietest after the spurs): the full-covariate model leaned
  on charges a day and the hub's unit count (the standard hubs gain a unit in 2027) and filed 13 hubs, ten of the
  golden's; the five now take 4.8 to 5.6 charges a day, inside the standard hubs' range, and the model files 3.
- A rate-route back-test bound of 0.4 points: with comms repairs and faults at their real scatter a unit-year's own
  noise is about 0.4 points, so the bound is half a point with 85 per cent of units on their side, and the back-test
  prediction now carries the comms repairs' downtime as the rate route does.
- Load bank tests of about 55 kWh a connector with session drops of up to 18 minutes two and a half times a day: a
  column total (the gaps out, the tests in) cancelled to the golden figure at three hubs; tests now run about a
  quarter of an hour (30 to 40 kWh), drops three times a day for 6 to 15 minutes (inside the three missed heartbeats
  that write Offline), and the generator's clearance holds the gaps and the tests at least 0.16 MWh apart at every hub,
  the tests across a rounding step and no hub's charges on a round hundred.
- Work orders written from six to nine fixed sentences a job kind (one repeated 118 times) and planned jobs attended a
  whole number of days after logging: each write-up is now composed from the job's parts in its technician's habits
  (2,465 distinct over 3,546 jobs, none more than 9 times), planned jobs are logged at the planner's minute and
  attended at the technician's, and the parser's reading of every job's kind from its words is asserted against the
  truth.
- The plan's addressee typed rather than drawn (Bronagh Allis): now Ailis Fee from `guard.py names --geo ireland
  --seed 156`, the schedules signed by Darcy McGlinchey and Domhnall Linehan from the same draw.
- The prompt's question as "Which of our hubs will have..." (the which shell at 32 per cent of the prompts on file, and
  task482's form), then "Where will we have..." (the voice check and the heart read "will we" as whether): it now asks
  "Where in our network will a high-power charge point fall below...", read as where by both.
- "No forecast within 0.3 of 99" (the first hand-off's SF4 and closure line) was not what the build measured (0.21 to
  0.25 then): both now quote the measured margin, asserted at 0.2 or more.
- CRITICAL_COMPONENTS 1's hang count (84, which the judge read as 83 with a power-up before it on record and 90 in
  all): dropped, the onset day kept with its definition.
- The surface screen on the cached corpus (127 builds, 0 promoted at the first hand-off): the full re-extract screens
  314 and promotes 9 pairs on card axes or surface percentile, each differentiated on the card.
- The planned maintenance schedule writing 08:30 to 14:30 on every row while the world's visits ran in each
  contractor's own windows (the first fix pass varied the windows in the world, not in the schedule): the schedule now
  carries each hub's window for each year (motorway hubs early, rural spurs late, town centres before the shops open,
  moving with each year's plan), and Schedule 4's exclusions, the golden's and the verifier's, are read from it.
- Stage 4 round 2 (2026-11-08, on 3a6e329b): the leak reader clean, the judge DETERMINISTIC (APPROVE, no FIX_NOW). The
  ship pass worked the coordinator's fixes 1 to 7 in one generator pass; the call, the stump, the ladder and the default
  path unchanged. freeze.py's --allow, with its reasons: charges.Annagh Cross, energy_mwh.Annagh Cross,
  charges.Cloonfin Crossroads and energy_mwh.Cloonfin Crossroads (the spurs' interruption record raised by half, fix 5,
  which re-draws their 2026 sessions: 1738 to 1786 charges and 57.3 to 57.5 MWh, 2545 to 2507 and 81.9 to 81.0);
  pack.status_rows (the export cut at 31 October 24:00 and the spurs' extra power-downs), pack.dso_rows (the spurs'
  extra interruptions), pack.session_rows, pack.resent and pack.resent_hubs (the session numbering moves with the
  spurs' sessions, so the export's September re-sent page falls on other hubs; no other hub's records change),
  pack.wo_a and pack.wo_b (planned jobs raised by each contractor's own practice, the jobs open at the save, the spurs'
  callouts) and salt.NM125 (the clearance re-drew Annagh Cross's sessions once more).
- The status history ran past its stated coverage (rows to 8 November, from intervals that ended after 31 October) and
  the work orders held jobs attended and closed after the workbook's save: each export now ends at its own moment, a job
  raised before the save and not yet attended or closed stands open, and a spell still Offline when the record ends is
  censored rather than read as a hang (the golden and the verifier alike). The schedule's visits on 30 and 31 October
  stood Completed in a workbook saved on 29 October; a visit is Completed now only once its window closed before the save.
- Planned jobs raised 3 to 20 or 6 to 30 days ahead by both contractors (the same ceilings in two systems): Lissane's
  technician booked the next RC50 job on leaving the last one and its planner raised site visits in a batch the month
  before; Corran raises a site visit on the day the operator notifies the partnership and an RC50 job a fortnight ahead,
  about one in six then moved; the operator's notice runs from a fortnight to about six weeks. The jobs' write-ups are
  drawn in the order they always were, so every write-up outside the spurs' callouts stands as it did.
- The spurs at 7.3 and 9.4 interruptions a year: their lowest unit sat at 99.31 and 99.47 on the golden and 99.15 on the
  judge's own simulation, their expected lowest unit at 98.9 to 99.05 and their event probability at 0.41 to 0.48. The
  long rural overhead spurs now carry 42 and 54 interruptions on the record (about 11 and 14 a year): the extra faults
  are drawn on a stream of their own, so every other hub keeps its record, its sessions and its jobs (the spurs' old
  draws replayed where other hubs share a stream).
- The spurs' extra faults first drawn as a Poisson stream (4.6 and 4.9 a year): its draw moved the smoothed route to 9
  hubs (Cloonfin Crossroads in) and the rate route's back-tests to 0.42 and 0.43, figures the frozen ladder and default
  path state; the record now holds a stated count (14 and 18 beyond the base), and the stream is chosen, as the
  clearance chooses the asks' salts, so that the re-drawn spur record leaves every cheap route's set and the back-tests
  as they stand.
- The programme's document control table split across its page break (heading on page 1, rows on page 2): kept with its
  heading on page 2; no word changed.
- The PDFs' Creator (fix 4, optional): left as Writer. officepdf renders every document through LibreOffice Writer, so
  any other Creator would be contradicted by the file's own structure.
- The expected lowest unit, the event reading, each unit's own fault rate and a Weibull onset (the judge's optional
  items): asserted as SF17 to SF20, each on the same 12; the Weibull's fit is worse than the fitted onset's by 27.5 AIC.
- The RC50's 2027 isolations drawn as a Poisson stream at the hubs where it stays: they forecast 0.05 to 0.53 hangs a
  unit-year there against 0.00 to 0.39 on the record, which thins those hubs' expected-lowest-unit margins (Eskerbrook
  Shopping Centre at 99.07); drawn from the record's own calendar the member lists the same 12 at 99.23 and 0.32 at
  worst, measured and asserted, and the golden keeps the Poisson draw (no golden change).

- Architecture 4, the rapid-charging operator's 2027 availability plan (2026-11-08, platform round 1, target.zip
  5356713d): both runs landed the golden 12 hubs (the author reports not stumped; no rubric). Both read the hang ages
  off the first histogram (no hang before day 76 after a power-up), fitted a censored hazard on time since restart with
  the work orders' power cycles as the remedy, simulated the renewed network and back-tested on 2026: a mechanism the
  rows carry in one plot, with its remedy written in the work orders, was modelled on sight. Its asks fell (93,640 and
  94,297 charges against the golden's 90,612) but the platform rules a landed call before grading. World spent.
- Architecture 5 draw, a heat pump conversion programme's second phase forecast from homes that under-heated on gas and
  will heat fully on a heat pump (each home's uplift conditioned on its own pre-conversion balance point): rejected at
  the draw, because it is task3 architecture 1's driver in other nouns (the gain an upgrade adds conditioned on how much
  of each unit the old level already served), which one of that build's runs landed by regressing each earlier unit's
  gain on its own prior coverage; conditioning a carried gain on a covariate each unit's history prints is a reflex.
- Architecture 5 draw, a pilot of hybrid heat pumps whose gas backup flattened the cold-day electrical load carried to
  an all-electric second phase: rejected at the draw on the one-fact test (the pilot's units are hybrids), and the
  backup's discovery would be finding a population fact rather than analysing.
- Architecture 5 draw, stations whose winter peak responds in opposite directions to the gas-to-electricity price ratio
  (hybrids switching fuel, all-electric homes economising) carried to the 2027 energy tax shift: rejected at the draw,
  because a per-station forecast is the natural default, so each station's own slope is a reflex there (the grouping
  dichotomy), and the decision weights no population mix.
- Architecture 5 draw, measurement error in the heat pump count by substation (postcode allocation) attenuating the per
  heat pump coefficient: rejected at the draw, task4 architecture 5 carries an errors-in-variables driver in flight.
- Architecture 5 draw, phase imbalance (single-phase heat pumps landing on one phase, the transformer's per-phase limit
  binding first): rejected at the draw, because per-phase columns invite the per-phase reading and the installers'
  allocation is readable off the first phase's increments.
- Architecture 5 draw, latent excavation damage behind a spike in cable faults read as ageing: rejected at the draw, an
  activity elsewhere, linked by place and time, driving failures repeats architecture 4's family in this slot.
- Architecture 5 draw, export from PV-saturated feeders censored by inverter overvoltage trips: rejected at the draw, a
  trip is not a clean cap, and the capped-quantity family is crowded on this repository's cards (mark124, mark162,
  task4 architecture 2).
- Architecture 5 prototype, the partners' own design-day demand reconstructed by removing the moved sections as the
  deciding step: kept off the call, because removing a moved load from a series is cleaning; the partners' flags hold
  under every route by margin and the moved sections decide only their ask figures, while the call moves on what
  the credited flexibility is.
- Architecture 5 prototype, an unadjusted customer baseline (the mean of the ten previous non-event weekdays): measured
  0.33, minus 0.38 and 0.25 per megawatt scheduled at the three zones, its cold-day bias cancelling part of the moved
  section at one zone and turning another negative; it files a fourth primary (Charlecote Way) and misses, and its
  negative zone sends a run to the weather-adjusted baseline, which carries the whole moved section.
- Architecture 5 build, the pair estimate summing whatever half-hours either primary reported: a half-hour held or
  missing at one primary became a one-primary sum and dragged the pair's baseline (Hartwell Common 0.18 per MW against
  the netting's 0.39); the pair now sums only half-hours both primaries reported and reproduces the netting exactly.
- Architecture 5 build, the before-demand left to "assessed before any flexibility": excluding the event days and
  adding the measured fall back gave Ashcombe Road 26.0 and 26.7 MW after flexibility (two whole-MW cells), and keeping
  the event days dropped both committed primaries under firm; guideline 3 now names the days left out (SF3).
- Architecture 5 build, the growth register's "accepted offer" read without the energised: Fenwick Street moved from
  29 to 28 MW; guideline 4 now says the energised are included (SF5).
- Architecture 5 build, Fenwick Street's 14.0 MW contract: credited 6.75 and after 29.30 MW sat 0.25 and 0.20 from
  their whole-MW edges; the contract is 14.5 MW and both figures sit mid-bin.
- Architecture 5 build, an October to March SCADA export: October runs on British Summer Time, so a run reading the
  UTC stamps as local shifted October's half-hours and moved Fenwick Street's after figure; the export runs November to
  March (SF22).
- Architecture 5 build, the historian's first outage draw: two held stretches on Hartwell Common's 2024/25 evenings
  moved its delivery to 0.3 for a run that kept the S rows; the outage stream was redrawn (34) so every handling of the
  held values gives the golden's figures, and Ashcombe Road's first service starts on 27 November 2024 so no two zones
  or winters share an event count.
- Architecture 5 build, the dispatch log as the second large CSV: 379 rows, about seven printed pages; the weather file
  (13,372 rows, raw readings beside their checked versions, logger gaps) carries that gate.
- Architecture 5 build, nine primaries named in their keys' alphabetical order (Ashcombe, Brindle, Charlecote and on to
  Ingram), feeder streets repeated across primaries, every zone's contract up 0.5 MW a winter and growth references
  numbered after their acceptance: the stage 4 reader read each as templated; four primaries renamed (Tollbrook Lane,
  Ravenhurst Park, Wexley Hill, Kestwick Fields), one street per feeder, the winters' megawatts varied (Ashcombe Road
  5.0 then 6.5, Fenwick Street 5.5 then 6.5) and each reference numbered in its application year, every graded figure
  unchanged in its bin.
- Architecture 5 stage 4, the 2025/26 correction pooled over three winters with winter levels: the judge read guideline 3
  ("forecast from the primary's 2025/26 winter demand corrected to the design condition") literally and fitted 2025/26
  alone, which is the WHAT's literal execution; the golden now fits 2025/26 alone, and the pooled fit converges (SF4).
- Architecture 5 stage 4, Fenwick Street's 14.5 MW contract: a mean of the events within 1.5 or 2 C of minus 3.0 C
  (0.52 per MW) credited 8 MW and left 28; at 14.0 MW every one of 16 estimators lands on 7 and 29, and Ashcombe Road's
  contract moved to 9.5 MW with 0.25 MW more accepted growth (Fenwick Street 0.25 MW less) so every zone's estimator
  family sits inside one bin for delivery, credit and after (0.11 to 0.33 MW from the edges).
- Architecture 5 stage 4, a daily peak on a day the export cuts: under BST the last half-hours fall on 1 April local, and a
  one-reading "day" entered a 2025/26-only fit and moved Ashcombe Road by 1.5 MW; daily peaks and means now count only
  days with at least 44 half-hours and 20 hourly readings (SF1).
- Architecture 5 stage 4, the historian's export in UTC with events into the last days of March: the late-March weekdays
  are the mildest training days, so a run reading the UTC stamps as local moved every baseline by 0.1 MW and three zones'
  figures; the service now ends before British Summer Time, the export is on the UK clock as many historians write it,
  and Ashcombe Road's first and Hartwell Common's second service start later (28 November 2024, 10 November 2025) so no
  two zones or winters share an event count.
- Architecture 5 stage 4, "the control room moved a feeder section" in the answer blocks: no shipped file records a
  control-room action; the blocks now state the rise at the primary across the open point and cite guideline 6 for
  netting it (the judge's FIX_NOW).

- Architecture 5 platform round 1 (2026-11-08, triage FIX_ASKS; no rubric pasted, scores estimated at about 92 and 31,
  the author's estimate an average near 68): run 1 landed the golden with paired totals across the open points and
  the delivery read at minus 3.0 C, losing only the neighbour rises and the 0.9 contrast it never stated; run 2
  measured the neighbours' rise (1.271, 0.997 and 1.680 MW) and set it aside as not proving a transfer, filing
  Ashcombe Road alone on rung 1b (dismissed own evidence). Both read the design day, so the asks' designed second
  judgment (the design condition, the first cracker's rung 3) was spent by the guideline's and the prompt's own words.
- The per-zone answer items (Supplementary Questions 2 to 5, one per zone): run 2 collected Charlecote Way's whole row
  (0.5, 4, 21, No), because Charlecote Way has no transfer and every route that reads the design day agrees there, and
  the over-firm Yes at Ashcombe Road and No at Fenwick Street, which hold on both paths; replaced by one item per
  quantity across the four zones, the flags folded into the after item's set.
- The layout item (Supplementary Question 1) and the chart graded as present: format items both runs collect; the
  layout now rides inside the delivery item and the chart is graded on which after columns stand above firm.
- The step-by-step's upstream figures (each zone's completed events, the design-day demand before flexibility): both
  runs reproduced them (30, 25, 36 and 23 MW), so a criterion drawn from them is free; dropped from the blocks, the
  workbook still carries them.
- A colder-day ask at minus 4.5 C alone with each zone's demand after flexibility graded: Hartwell Common's figure sits
  0.07 MW from its edge across the estimator family, and a quadratic correction puts Fenwick Street and Charlecote Way
  on firm capacity there; the ask grades the sets at minus 4.5 and minus 6.0 C only, and winter 2023/24 rules the
  quadratic out (SF24).
- A threshold ask (the coldest daily mean each primary left on its flexibility can carry): Charlecote Way's sits
  0.03 C from its whole-degree edge under Theil-Sen; not asked.
- Asking each provider's delivery once, pooled across its zones, so that Charlecote Way's figures would ride Fenwick
  Street's: it sets one provider's two zones side by side, the contradiction run 2 never confronted (0.48 against
  0.74 per MW), and could hand the call to the run the stump held; the table stays per zone.
- The guideline's lead time (about eighteen months from a December 2026 commitment, which reaches June 2028)
  contradicted its own winter 2027/28; run 1 flagged it. Restated as energised by the end of the following October;
  no figure moved.
- The pair ceiling gated on the design's first cracker (the delivery averaged over the event days, 32.8 on the new
  asks): no platform run took that row, so it is not the worst honest landed run; the gated figure is now the landed
  run that reads the design day and misses the asks' own judgment (53.1), with the full includer's beside it.
- Stage 4 judge on the repaired asks (2026-11-09, pass 2, target.zip 203d2bf4; NOT_DETERMINISTIC, SEND_BACK, Gate G
  analytical_non_defect and Gate H pass, stump power strong; report determinism_check_report_pass2.md): the minus
  4.5 C set turned on Fenwick Street by 0.05 MW under the thread's own joint regression and fell 0.39 to 0.87 MW short
  under a quadratic correction or a delivery fitted on the 2025/26 events alone, so it is dropped and the colder-day
  ask keeps minus 6.0 C, which held under every variant the thread ran (Charlecote Way 0.35 to 0.70 MW over); the
  excess's rounding is now in the prompt's rounding sentence; three growth-register acceptances dated after the
  register's own save (late connections, outside the window, no figure moved) now fall before it.
- The same pass read guideline 6's "reduction in the primary's demand" as the primary's whole fall, the route read at
  minus 3.0 C that files Ashcombe Road alone (23.5 MW against 23.0), and found no filed sentence stating a transfer;
  two earlier passes and the run triage ruled that route out by "that its provider will deliver", "No other measure is
  credited" and the award notice's delivery measured on the provider's metered assets. The closing passage now names
  and rebuts that route; the judge's own closure ("load picked up elsewhere across open points is not credited")
  names the transfer the deep step finds and fails the fork-is-the-stump test, so the main call is left for the
  author's decision rather than pinned in a rubric repair.
- 2026-11-10, architecture 6 (the results chain of eleven: a share of the contract available on the cold days, the come-back after
  the window, a spread in proportion, the bridge) landed on the platform: both runs committed the golden's three primaries with
  every stated figure inside its band (0 of 11 results lost against a paper pair of 38.4). Each run fitted an availability
  ceiling capped by the instruction, rebuilt the day half-hour by half-hour with the come-back, drew a predictive
  nine-in-ten level and back-tested on the held-out winter, unprompted. All three mechanisms showed in the rows, and the
  three things the runs named as untested assumptions (the contract scaling in proportion, the straight line carried eight
  degrees below the clean days, no serial dependence) were true in the world, so assuming them cost nothing.
- Architecture 7, each evening half-hour regressed on the day's own morning by least squares: the day effect sits in the regressor, so the slope is pulled down and the cold end read low; the evening is now divided by the day's morning factor and regressed on the morning the temperature gives, and the regression is kept as a variant (SF10).
- Architecture 7, commissioning by class read from the five zones' own sites: eight process load sites in three winters could not hold a class record; the asset register now covers the licence area's 29 zones and five providers.
- Architecture 7, instructions cancelled at random: cold evenings without a service appeared in the record and the line through such days found the cold end; a cancellation now follows the morning's revised forecast on marginal, low-running days, which is how a control room cancels.
- Architecture 7, Fenwick Street at 35.2 MW of firm capacity with a 12.5 MW award: the route that regresses every working weekday on megawatts scheduled sat 0.46 MW over firm capacity and the register's pooled record 0.58 under; firm capacity is 35.0 and the award 13.0 MW, and both sit 0.7 MW either side.
- Architecture 7, Hartwell Common at 24.5 MW of firm capacity with a 3,200 kVA commercial unit due in September 2027: the careful pass sat 0.53 MW over firm capacity; firm capacity is 24.4 and the unit 4,000 kVA.
- Architecture 7, a share that printed 0.40 for Corvane Flex and lateness that was never negative (no site of 1,172 in service by its planned date): both read as settings; the share's floor moved and a site's work now starts about a fortnight before its planned date, so a few of the quick classes pass on or before it.
- Architecture 7, the asset register extracted on 27 November and the awards dated 24 November 2026, with goldens saved in December: every stamp sat after the day the build ships; the register is now the extract of 4 November, the award notice 21 October with its schedules closed on 16 October, and the goldens are saved by 9 November.
- Architecture 7, the prompt's "between 17:30 and 18:00" beside guideline 6's half-hours ending 17:30 and 18:00: read literally the prompt named one half-hour and the guideline two; the prompt and every label now say 17:00 to 18:00, and either half-hour alone is within 0.05 MW of the mean of the two (SF25).
- Architecture 7, restructuring the register so that a class read from its commissioned sites alone drops Fenwick Street (most process load sites in recent, unfinished cohorts): it needs a gap of about 1.5 MW at the nine-days-in-ten level between that reading and the golden, and the scheduled-megawatts route already sits 0.5 MW under the golden on the commit side, so no firm capacity holds 0.6 MW on both sides; the reading stays a route that keeps the list and loses megawatts, and its effect on the effort test is recorded as a sensitivity.
