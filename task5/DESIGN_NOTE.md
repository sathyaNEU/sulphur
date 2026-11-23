# task5 design note: the consular officers each district needs for the 2027 posting cycle, and the citizens abroad behind them

Architecture 5, drawn on 2026-11-17 in a new world. Architecture 4 (the State of Franklin unemployment insurance files, READY on 2026-11-10 and never uploaded) was set aside before any platform round: its call turned on recent counts still filling in, which the client closed on 2026-11-12, it was cut before the core, open-members and rubric rules, and its prompt asked for a written memo. Read `## Tried and rejected` first. Every figure below is printed by `python3 task5/generator/core.py` (with `--detail` and `--forcing`) on the world's arrays, seed 5127, and the build's sections (`## Results chain`, `## Stump core`, `## Frontier check`, the pinning list) carry the cut pack's figures from `generator/figures.json`.

## Draw

Subdomain: Survey Research & Official Statistics (Other), census, register and administrative-data quality
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: an allocation with its sensitivity: the consular officers each of seven districts gets under the staffing order from the estimated number of citizens resident there on 1 January 2027, with the citizens who moved away since the 2021 census and how far each fitted input can move before a district's officers change
Weight: assembly: the work is conforming eight states' twice-reported migration tables, two census rounds, the hosts' vital events and the home register's event file into one population account for each host, and deciding which record stands for each term of that account (arrivals, exits, the years no partner covers); the builds before this one sit on modeling (task1) and a hard-to-measure quantity (task4), and the guard's window bans both
Data-native sentence: a citizen living abroad is counted where they live only at a census, and between censuses every move is written down twice (by the state they enter, at that state's habit of registering arrivals, and by the state they leave, at that state's habit of registering departures), with the partners' tables ending three years before the date and only the home register running on, so the head count on 1 January 2027 has to be assembled term by term from records that each see a different fraction of it.
People: Neja Bezjak (head of population statistics, Statistics Orlava, who supplies the estimate), Jani Debeljak (migration statistics analyst, the golden's author), Emil Bajc (secretary of the Posting Board, Ministry of Foreign Affairs), Kaja Kalan (population register, Statistics Orlava), Silvo Zver (liaison to the Common Movement Area Statistical Office), Klemen Kokalj (census methods) (`guard.py names --geo "Slovenia" --locale sl_SI --n 8 --seed 5127`)
As-of: 2027-02-22 (the home register's extract is of 19 February 2027 and holds every event dated to 31 December 2026; the Posting Board meets on 18 March 2027)

Card `.claude/skills/fingerprint/cards/task5.json`, architecture 5, registered 2026-11-17: WARN only. repeat.decision and repeat.question_form against task4 (a quantity figure asked as how many): the decision is a head count against a staffing order, so the form follows the decision, and the answer here is a whole number of officers per district where task4's is a cover per container pool. repeat.deliverables against task1 (a CSV and a workbook): the house set; the CSV here is a population account by host and year and the workbook's first sheet an establishment table. skeleton.house_lesson on conservation_residual_attribution (task22, task4) and validation_cannot_see_condition (mark258, task4): neither is this build's first lesson, each is one of three stumps on different axes, and the account here closes a population between two censuses on arrivals that are themselves estimated, which neither build does. NOTE test.same_puzzle_older against mark120, differentiated on the card. The guard's first pass blocked the forcing event (budget_or_appropriation) and the gap and pattern pair against task9 and task4's lineage; the event is the Posting Board's meeting (vote_or_meeting) and the decisive gap is the objective (what each table measures is not the moves), which is the honester label.

## Stump screen

Screened on paper and in `generator/core.py` before the card was registered (`references/stump-screen.md`, the seventeen tests).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A: every state's arrivals table holds that state's own share of the people who moved in (0.56 to 1.21 of them), the twice-reported matrix fixes the shares only up to one common factor, and one census table pins the factor | the receiving state's count is the flow, or the fuller of two reports is, or the fullest recorder is complete (L22, L51, N27) | Orlava's 2021 census table of foreign citizens by where they lived a year before, against its own register's arrivals of 2020; the partners' emigration tables against each host's arrivals of their citizens | none | kept (S1) |
| B: a host's departures table holds a fraction of the citizens who left (0.24 to 0.97), and no table holds the rest | the departures table is the exits (L48, L32, N10) | the host's two census counts with the arrivals and vital events between them | none | kept (S2) |
| C: the partners' tables end with 2023 and the moves of 2024 to 2026 changed (exits up 10 to 120 per cent by host, arrivals down in most), seen only by the home register at a fraction of its own | the latest three years carried to the date (N13, N28, L03) | the home register's deregistrations by destination and re-registrations by origin against the hosts' tables on the years both report | none | kept (S3) |
| D: the chance of leaving falls with years since arrival, so a host with many recent arrivals loses more than its average rate | a constant exit rate per resident | arrival cohorts by year in the hosts' tables | 2 and 12 (runs fit a duration profile wherever cohorts are tabled, R36; without cohort tables nothing forces it, and with them it is one fit) | dropped; C took its place |
| E: one state registers stays under a year as arrivals, so its table over-records | the fullest recorder is complete | the mirror matrix | 13 (it opens no member of its own: it is the reason the fullest recorder cannot set the level, part of A, and the same recording habit runs at some strength in every state) | not a stump: a mechanism of A |
| F: a partner whose reference year ran July to June until 2014 | every table is on calendar years | the release notes | 4 and 7 of the banned list (a reading of one field, and converting split years is an open fork) | dropped, and left out of the world |
| G: the censuses themselves miss some foreign citizens | the census is the truth | a coverage survey | 1 and 5 (dependent capture is closed and is task19's ground; no second record in this world) | dropped |
| H: batches of administrative deregistrations entered years after the move | the register's event date is the move | the entry date | 1 and 2 (near the closed reporting lag; one plot of entry against event date shows it) | dropped; late entries stay as Layer 1 with both dates on the row |
| I: citizens moving on between partner states | every arrival comes from the home state | arrivals by previous residence | 3 and 12 (filed by the tables' own definition, and one more column sums it) | dropped; the tables are by citizenship |

## Deep reasoning

Task type: census-register-administrative-data-quality in Survey Research & Official Statistics, which serves Data Extraction & Conformation: a population of citizens abroad conformed from eight states' register-based migration tables, two census rounds and the home register, with each term of the population account taken from the record that sees it.
Domain test: every result is a quantity official migration statistics estimates: a state's coverage of arrivals and of its own emigrants from the twice-reported flow matrix anchored on a census transition table, intercensal exits as the residual of the population account, the share of moves a home register catches, and a population of citizens abroad on a date no count covers. The field's analyst builds each from the record that sees it and says what the record cannot see.
Swap: "How many service engineers does each sales region need for the machines installed there on 1 January 2027?" keeps the count against a standard and nothing else: an installed machine is on a contract, a sale and a scrapping are each recorded once by one party, no second state reports the same move at its own habit, and no census fixes the stock every ten years. The task stops making sense.
Where the weight sits: R1 to R3 and R5. The account is long before it is clever: 56 state pairs, two reports each, thirteen years, three code schemes and superseded releases on one schema (R1); a share for every reporting state in both directions, with the one independent count that pins their level found and used (R2); an account per host between two censuses on arrivals that are themselves estimates (R3); and the same shares measured again for a register that sees the last three years alone (R5).
Layer 1: state and citizenship codes in three schemes (two letters, three letters, the area's numeric codes), because the hub, the national releases and the home register each keep their own; revised vintages of the same year republished under a later release, because states resend corrected tables; the home register's events keyed by municipal clerks (destinations and origins as free text beside the code, repeats after a re-sync of a municipality's queue, events entered up to six weeks after the move with both dates on the row); census tables by citizenship and by country of birth side by side in one workbook. None decides a result: every one resolves exactly, and `checks.py` asserts the cleaned files reproduce the world's recorded arrays to the unit.
Not one thing: the strongest single piece is the level of the recording shares. A run that nails it still files Skarholm an officer over, Brennia two over, Marovia three over, Tesmar three over, Fenmark an officer over and Almera two over (S1 fixed alone on the reflex route: 9, 12, 11, 10, 3, 6, 15 against 8, 10, 8, 7, 3, 5, 13; 23 on the rubric), because the exits and the last three years are untouched.
One-fact test: "each state's migration tables hold only that state's own share of the people who move in and of its own people who move out, a different share in each state" rescues R2 and nothing else (1 of 8 results), and only once the level is found: R3, R5 and every figure downstream still fall with S2 and S3.
Not semantics: every field, code, unit and clause read correctly leaves the reflex route where it is: an arrivals row is a registered arrival, a departures row a registered departure, a census count a count, the order's citizen, usual residence, date and rate are as written, and the route still staffs six districts wrong because of what share of the moves each register catches, not because of what a column means.
Not rule application: the staffing order files the population, the date and the rate; the area's regulation files what each table holds and when it is released. Neither performs R2 to R8. After every filed rule is applied the analyst still has to estimate what share of arrivals each host registers, how many citizens left each host, and what happened in the three years no partner reports.
Estimand: the Consular Establishment Order, clause 1.1 (a district is one partner state), 2.1 (one officer for every 5,000 Orlavan citizens or part of 5,000 usually resident in the district on 1 January of the cycle's first year), 2.2 (usual residence: living or intending to live there twelve months or more; a citizen is a person registered as an Orlavan citizen), 3.1 (the 2027 to 2029 cycle, the Board's meeting of 18 March 2027); the area's regulation on migration and population statistics, articles 2 (usual residence, immigration, emigration, citizenship as registered on arrival and kept while resident, the reference year as the calendar year of the move), 3 (the six tables), 4 (counts refer to 00:00 on 1 January) and 6 (transmission within 24 months, a later release replaces an earlier one); the prompt (citizens resident on 1 January 2027, the officers the order gives, citizens who moved away between the 2021 census and the end of 2026, by state). The method is filed nowhere.
No decoy: no memo, draft or column carries a wrong answer and no document argues for a route. The establishment in force (8, 6, 9, 8, 2, 5, 13) is the order applied to the 2021 census counts and reproduces exactly; it answers the 2021 question and is priced on the golden's footing by the ask for the 2027 citizens of every district.
No replay: no result re-derives a published figure and no filed number is wrong.
Pinned: 126 variants of the golden's conventions in `generator/core.py` (`FAMILY`) file the same officers in every district and set every band; each fitted input moved one measured spread up and down alone, and all four together, files the same officers (`--forcing`, exit 0); the rivals (the hosts' tables at face value, the larger report of each flow, shares scaled to the fullest recorder, arrivals as recorded with the account closed on departures) are each refused by a figure: Fenmark's count of 1 January 2016 (off 2,637, 2,905, 1,181 and 2,090 against the golden's 96) and the arrivals of 2021 to 2023 held out.
Run forecast: R2 lost to a method shortcut (the receiving state's count taken as the flow, or the field's reference-recorder scaling, which a state that over-records breaks); R3 lost to dismissed own evidence (the departures table taken as the exits though the host's own census pair is on file, or the account closed on raw arrivals, which reproduces the 2021 census exactly); R5 lost to dismissed own evidence (the home register seen to run to 2026 and set aside as incomplete, the last three years carried forward); R4 and R6 to R8 fall with them. The honest expectation is that the review's strongest run closes the account between the censuses (R3) or bridges the last three years on the home register (R5) but not both with the level of R2: a run that loses S1 alone earns 30.
Strategy label: other (each term of a population account assigned to the record that sees it: a census-anchored coverage chain for arrivals, the intercensal residual for exits, a second register for the uncovered years; no label in `references/sulfur-strategies.md` names the three together)
Depth level: 5: three independent judgments on different axes, each necessary and none sufficient, the three single drops on three different wrong establishments (8, 9, 8, 8, 3, 6, 13; 9, 12, 11, 9, 3, 7, 15; 8, 10, 8, 8, 3, 5, 13) and the lattice's seven shortcut routes on seven.
Lesson: two incomplete reports of the same flow fix each reporter's completeness only relative to the others, so the level has to come from a count that was not produced by registration; a stock counted twice pins the flow nobody recorded once the other flows are right; and a record that ends before the date is extended by the one record that runs on, at the fraction measured where both report. No build on file teaches a coverage level that the cross-reports cannot identify.

## Results chain

Every figure below is from the cut pack (`generator/figures.json`, seed 5127).

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | both reports of every flow among the eight states for 2011 to 2023 on one schema, Orlava's register events to 2026 by year and state, each host's census counts of 2011 and 2021 and its births and deaths of citizens: for Skarholm, Brennia, Marovia, Tesmar, Kestria, Fenmark and Almera the registered arrivals of citizens 2011 to 2023 are 29,914, 19,160, 39,714, 27,735, 13,644, 18,083 and 42,666 and the registered departures 10,737, 9,063, 9,709, 11,114, 4,997, 4,370 and 19,736 | assembly-reconciliation | the hub's releases, the home register, the census tables, the code table | exact on the cut pack | narrow look at broad data: the ten-minute pass opens the hosts' rows for Orlavan citizens alone and never conforms the other states' pairs; the careful pass builds all of it | - | Step-by-Step |
| R2 | the recording shares and the citizens who moved to each host: Orlava's register caught 72.0 per cent of foreign arrivals in 2020 and 36.3 per cent of its own emigrants 2011 to 2023; the hosts' arrival shares are 1.004, 0.558, 0.852, 0.707, 1.213, 0.668 and 0.890 | missingness-measurement | Orlava's 2021 census table against its register's arrivals of 2020; each partner's emigration table against Orlava's arrivals; the other partners' emigrants against each host's arrivals | the emigrants' share 35.3 to 36.8 per cent | method shortcut: the receiving state's count taken as the flow (44.9 per cent), or shares scaled to the fullest recorder (29.9 per cent) | R1 | Component 1 |
| R3 | each host's exits of citizens between its two censuses and the share its departures table caught: 0.473, 0.419, 0.242, 0.457, 0.967, 0.320 and 0.549 | decomposition-attribution | the census counts of 2011 and 2021, R2's arrivals, the vital events | Skarholm's share 44.9 to 48.2 per cent | dismissed own evidence: the departures table taken as the exits (100 per cent) though the host's own two censuses, on file, leave up to four times as many gone; or the account closed on arrivals as recorded, which reproduces the 2021 census exactly | R1, R2 | Component 2 |
| R4 | Fenmark's count of 1 January 2016 reproduced from its 2011 census (19,484 against the count's 19,580) and the arrivals of 2021 to 2023 held out against the home register scaled on 2011 to 2020 | validation | Fenmark's 2016 count; the hosts' arrivals of 2021 to 2023 | 19,410 to 19,620 citizens; the golden within 96 of the count, the five rival routes 1,181 to 2,905 away | self-confirming check: the route checked against the 2021 census it was closed on, the 2016 count left unread | R2, R3 | Step-by-Step |
| R5 | the share of moves to each host and of exits from it that Orlava's register catches (0.351 to 0.386 and 0.405 to 0.444) and the moves of 2024 to 2026 from it: Tesmar's exits ran 1.73 times those of 2021 to 2023 | modeling | Orlava's deregistrations by destination and re-registrations by origin against R2 and R3 on 2011 to 2023 | 1.70 to 1.77 | dismissed own evidence: the home register seen to run to 2026 and set aside as incomplete, 2021 to 2023 carried forward (1.01) | R2, R3 | Component 3 |
| R6 | citizens usually resident in each district on 1 January 2027: 36,469, 48,116, 36,684, 32,950, 12,227, 22,826, 62,662 | synthesis | the 2021 census counts; R2, R3, R5 | per district, the tables under `## Stump core` (from 36,130 to 36,650 for Skarholm) | dismissed own evidence: the reflex route files 44,061, 42,773, 51,395, 40,653, 13,246, 27,257, 71,324 | R2, R3, R5 | Asks 2 to 8 |
| R7 | citizens who moved away from each district from the 2021 census to the end of 2026: 13,755, 14,651, 23,410, 21,059, 3,453, 11,079, 22,057 | decomposition-attribution | the order 4.1; R3's exits to 2023, R5's after | per district, the tables under `## Stump core` | dismissed own evidence: the reflex route files 5,919, 4,898, 5,578, 7,288, 3,554, 3,292, 10,777 (the departures tables' own counts with 2021 to 2023 carried) | R3, R5 | Asks 9 to 15 |
| R8 | the officers the order gives each district: 8, 10, 8, 7, 3, 5, 13 (54 against 51 in force) | synthesis | the order 2.1 on R6 | exact | dismissed own evidence: the reflex route files 9, 9, 11, 9, 3, 6, 15 (62) | R6 | Recommendation |

Carry-forward: every graded figure sits downstream of a stump. R2's emigrant share falls with S1 alone and is S1's own figure; Skarholm's departure share in R3 falls with S2 alone (Skarholm registers every arrival, so S1 leaves it in its band) and is S2's own; Tesmar's ratio in R5 falls with S3 alone (the shares cancel in it) and is S3's own. Of the fourteen ask figures, S1 lost alone moves twelve outside their bands (Skarholm's two stay), S2 lost alone twelve (Kestria's two stay, where the departures table is nearly complete) and S3 lost alone eleven (Kestria's two and Fenmark's citizens stay: Kestria's exits hardly moved after 2023 and Fenmark's rose least among the larger districts). The reflex route lands one figure, Kestria's leavers. R6, R7 and R8 were one row at the draw; the build split them so that `effort.py` weighs the asks and the recommendation as the rubric does, and nothing in the core moved. precut's WARN that R2 sits upstream of R3 to R8 is answered by the factorial: with R2 right and nothing else, six districts are still wrong (S1 fixed alone, 23 on the rubric), because R3 needs its own account per host, R5 its own two shares per host on the overlap and R4 a count the route was not closed on.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a register counts registrations, not moves: each state catches its own share of arrivals (0.55 to 1.20, one state above one because stays under a year are registered) and its own share of its emigrants (0.36 to 0.80) | constructed, the documented behaviour of register-based migration statistics | no: all eight states, all 56 state pairs, every year | modelling: the two reports of each flow show the ratios in one look, the level only from the census transition table | modelling (a share per reporter in each direction, anchored, carried to the citizens' flows) | keep |
| citizens who leave a host seldom deregister there: the departures tables hold 0.24 to 0.92 of the exits | constructed, the same documented behaviour | no: every host, every year | modelling: the account between the two censuses on corrected arrivals | modelling (an account per host; it depends on the first factor) | keep |
| after 2023 exits rose in every host (by 10 to 120 per cent by 2026) and arrivals moved with each host's economy, in years no partner has reported | constructed, a turn in the hosts' labour markets | no: all seven hosts | a targeted query of the home register by state and year, then modelling its share on the overlap | modelling (two shares per host on the overlap, applied to three years) | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the conformed flows, censuses and vital events | Missed | Right | Right |
| R2 the recording shares and the citizens' arrivals | Missed | Missed | Right |
| R3 the exits between the censuses and the departures share | Missed | Missed | Right |
| R4 the 2016 count and the held-out years | Missed | Missed | Right |
| R5 the home register's shares and 2024 to 2026 | Missed | Missed | Right |
| R6 citizens on 1 January 2027 by district | Missed | Missed | Right |
| R7 citizens who moved away by district | Missed | Missed | Right |
| R8 the officers each district gets | Missed | Missed | Right |
| Roughly | 0 of 8 | 1 of 8 | 8 of 8 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the cut pack), and generator/core.py on corelib.py re-proved on the cut pack by generator/results.py (the rubric table of `## Stump core`)
Largest single hint: each state's migration tables hold only that state's own share of the people who move in and of its own people who move out, a different share in each state; rescues 1 of 8 results (R2, and only once the level is found; 23 rubric points with S1 fixed alone on the reflex route, six districts still wrong)
Pair estimate: 22.2 (effort.py on the cut pack: the careful but hurried pass earns the conformed tables and instruction-following; corelib's finer price of the same route is 13. A model, not a measurement: the platform's two runs are the measurement)

## Stump core

From `python3 task5/generator/results.py` (the core re-proved on the cut pack: seed 5127; eight states, sixteen years 2011 to 2026; the battery of 126 rebuilds), every figure as printed. Members are the seven districts; a member's line is the nearest multiple of 5,000 on each side.

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| Almera | 40000/45000/50000/55000/60000/65000/70000/75000/80000/85000 | 6.266e+04 | 317 | 7.132e+04 | 6.762e+04 | 5.975e+04 | forced |
| Brennia | 25000/30000/35000/40000/45000/50000/55000/60000/65000/70000 | 4.812e+04 | 505 | 4.277e+04 | 3.618e+04 | 5.133e+04 | S1 |
| Fenmark | 5000/10000/15000/20000/25000/30000/35000/40000/45000 | 2.283e+04 | 803 | 2.726e+04 | 2.571e+04 | 1.84e+04 | forced |
| Kestria | 5000/10000/15000/20000/25000/30000/35000 | 1.223e+04 | 248 | 1.325e+04 | 1.152e+04 | 1.17e+04 | forced |
| Marovia | 15000/20000/25000/30000/35000/40000/45000/50000/55000/60000 | 3.668e+04 | 434 | 5.14e+04 | 4.595e+04 | 3.41e+04 | S2 |
| Skarholm | 15000/20000/25000/30000/35000/40000/45000/50000/55000/60000 | 3.647e+04 | 251 | 4.406e+04 | 4.112e+04 | 3.45e+04 | forced |
| Tesmar | 10000/15000/20000/25000/30000/35000/40000/45000/50000/55000 | 3.295e+04 | 483 | 4.065e+04 | 3.829e+04 | 2.808e+04 | S3 |

| Figure | Block | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|
| C1 | components | 36.27 | 35.3 to 36.8 | moves | - | - | lost |
| C2 | components | 47.29 | 44.9 to 48.2 | - | moves | - | lost |
| C3 | components | 1.727 | 1.7 to 1.77 | - | - | moves | lost |
| N-Skarholm | asks | 3.647e+04 | 3.613e+04 to 3.665e+04 | - | flips | moves | lost |
| N-Brennia | asks | 4.812e+04 | 4.739e+04 to 4.871e+04 | flips | flips | moves | lost |
| N-Marovia | asks | 3.668e+04 | 3.605e+04 to 3.722e+04 | moves | flips | moves | lost |
| N-Tesmar | asks | 3.295e+04 | 3.228e+04 to 3.337e+04 | flips | flips | flips | lost |
| N-Kestria | asks | 1.223e+04 | 1.197e+04 to 1.258e+04 | moves | - | - | lost |
| N-Fenmark | asks | 2.283e+04 | 2.171e+04 to 2.356e+04 | flips | flips | - | lost |
| N-Almera | asks | 6.266e+04 | 6.221e+04 to 6.298e+04 | moves | flips | moves | lost |
| L-Skarholm | asks | 1.375e+04 | 1.344e+04 to 1.448e+04 | - | moves | moves | lost |
| L-Brennia | asks | 1.465e+04 | 1.408e+04 to 1.542e+04 | moves | moves | moves | lost |
| L-Marovia | asks | 2.341e+04 | 2.277e+04 to 2.441e+04 | moves | moves | moves | lost |
| L-Tesmar | asks | 2.106e+04 | 2.033e+04 to 2.222e+04 | moves | moves | moves | lost |
| L-Kestria | asks | 3453 | 3240 to 3790 | moves | - | - | earned |
| L-Fenmark | asks | 1.108e+04 | 1.034e+04 to 1.204e+04 | moves | moves | moves | lost |
| L-Almera | asks | 2.206e+04 | 2.137e+04 to 2.294e+04 | moves | moves | moves | lost |

| Route | Call | Earns on the rubric |
|---|---|---|
| golden | right | 100 |
| S1 lost alone | wrong | 30 |
| S2 lost alone | wrong | 30 |
| S3 lost alone | wrong | 34 |
| S1 fixed alone | wrong | 23 |
| S2 fixed alone | wrong | 16 |
| S3 fixed alone | wrong | 19 |
| reflex route (every stump lost) | wrong | 13 |
| rigorous standard route | wrong | 16 |

CORE PASS level 5  task5 architecture 5, cut pack

The lattice in citizens on 1 January 2027 (Skarholm, Brennia, Marovia, Tesmar, Kestria, Fenmark, Almera) and the officers each route files: the world 36,421, 48,083, 36,501, 32,637, 12,219, 22,273, 62,774 (8, 10, 8, 7, 3, 5, 13); golden 36,469, 48,116, 36,684, 32,950, 12,227, 22,826, 62,662 (8, 10, 8, 7, 3, 5, 13); S1 lost 36,432, 41,429, 38,476, 39,668, 11,698, 29,737, 64,169 (8, 9, 8, 8, 3, 6, 13); S2 lost 43,776, 56,703, 54,594, 44,463, 12,343, 30,435, 72,693 (9, 12, 11, 9, 3, 7, 15); S3 lost 37,866, 49,056, 38,161, 36,987, 11,997, 23,334, 64,899 (8, 10, 8, 8, 3, 5, 13); S1 and S2 lost 43,820, 42,397, 51,880, 39,391, 13,594, 27,477, 70,597 (9, 9, 11, 8, 3, 6, 15); S1 and S3 lost 37,840, 42,028, 39,482, 40,854, 11,448, 29,333, 65,939 (8, 9, 8, 9, 3, 6, 14); S2 and S3 lost 44,020, 55,989, 53,933, 45,063, 12,109, 29,896, 73,267 (9, 12, 11, 10, 3, 6, 15); all three lost 44,061, 42,773, 51,395, 40,653, 13,246, 27,257, 71,324 (9, 9, 11, 9, 3, 6, 15). The 2021 census counts (38,003, 29,251, 40,274, 35,735, 9,506, 24,085, 63,678) give the establishment in force 8, 6, 9, 8, 2, 5, 13, so the golden adds four officers in Brennia and one in Kestria and withdraws one each from Marovia and Tesmar.

Unobserved part: the Orlavan citizens usually resident in each partner state on 1 January 2027. No record holds it, in three parts: the citizens who arrived (each host registers its own share of them), the citizens who left (a host registers a fraction, and no table holds the rest), and everything after 31 December 2023 (no partner has reported it).
Instruments: each host's census counts every citizen on 1 January 2011 and 2021 and nothing between or after; its arrivals table sees 0.56 to 1.21 of the citizens arriving and its departures table 0.24 to 0.97 of those leaving, both to 2023 (read raw and rolled from the 2021 census to 1 January 2024 they file 41,120, 36,180, 45,954, 38,290, 11,516, 25,706, 67,622, the direct route); the hosts' vital events see every birth and death of a citizen to 2023; Orlava's register sees 0.36 of the citizens moving out and 0.41 to 0.45 of those leaving a host (the ones who come home and re-register), in every year to 2026, and 0.72 of the foreign citizens moving in; the partners' emigration tables see 0.38 to 0.80 of their own emigrants; Orlava's 2021 census table sees every foreign citizen who lived abroad a year before, for one year and for arrivals in Orlava only.
Referee: Fenmark counted its residents on 1 January 2016, between its two censuses; the count of Orlavan citizens is 19,580 and covers neither another host nor any date after 2021. The golden's account from the 2011 census files 19,484 (off 96); shares scaled to the fullest recorder 20,761 (off 1,181), shares scaled about their own average 18,386 (off 1,194), arrivals as recorded with the account closed on departures 17,490 (off 2,090), the host's tables at face value 16,943 (off 2,637), the larger report of each flow 16,675 (off 2,905). Read raw as a level for Fenmark's shares (its two half-decade accounts solved for one arrival share) it lands inside every band and is a member of the family; that reading is only as good as the draw of Fenmark's decade (across 45 draws it moves the level by 1 to 7 per cent), and the world carries a draw where it agrees with the census table to about 2 per cent (`core.py`, PLACED). Second check: the arrivals of 2021 to 2023 held out, the home register's deregistrations scaled on 2011 to 2020 against 2018 to 2020 carried forward (Brennia 15,265 actual, 15,482 scaled, 7,515 carried; Fenmark 4,057, 4,337, 5,420; Tesmar 7,816, 7,901, 9,095).
Strongest standard route: the field's reference-recorder scaling of the double-entry matrix (every state's shares estimated from the two reports of each flow and scaled so the fullest recorder is complete), with the exits and the last three years as the golden takes them: 34,497, 51,332, 34,101, 28,075, 11,698, 18,396, 59,751 (officers 7, 11, 7, 6, 3, 4, 12), wrong on every open member. It is refuted by Orlava's census table (the route puts Orlava's arrival share at 0.59 where the census against the register gives 0.72) and by Fenmark's 2016 count (off 1,181). Scaled about the shares' own average instead it files 38,164, 45,350, 38,904, 37,141, 12,681, 26,633, 65,165 (8, 10, 8, 8, 3, 6, 14): 4 districts right by the placement of this world, Tesmar, Fenmark and Almera wrong, and of the graded figures only Tesmar's ratio lands (about 16 on the rubric); it is disclosed here and is not one of the listed routes.
Said out loud: S1 "each state's migration tables hold only that state's own share of the people who move in and of its own people who move out, a different share in each state": four steps left (the level from Orlava's census table against its register; each partner's emigrant share from its flow to Orlava; each host's arrival share from the other partners' emigrants; the citizens' arrivals divided by it). S2 "a host's departures table holds only a fraction of the citizens who left, and the two censuses with the arrivals and vital events between them give the rest": four steps left (arrivals corrected first; the account per host; the recorded share; the exits of 2021 to 2023 from it). S3 "nothing is reported for 2024 to 2026 except what Orlava's own register caught, and it catches a different fraction of the moves to and from each host": three steps left (the two shares per host on the years both report; the three years' moves; natural change carried).
Worth: S1 is worth 6,690 citizens on Brennia, 13.2 times the family's spread of 505; S2 17,910 on Marovia, 41.3 times 434; S3 4,040 on Tesmar, 8.4 times 483 (the spread across the 126 rebuilds). Brennia's family runs 47,611 to 48,482 between lines at 45,000 and 50,000 and S1's drop lands at 41,429; Marovia's runs 36,250 to 37,025 between 35,000 and 40,000 and S2's drop lands at 54,594; Tesmar's runs 32,467 to 33,188 between 30,000 and 35,000 and S3's drop lands at 36,987.
Regimes: second stump on every member. S1's shares are checked on every pair of the matrix and on Fenmark's 2016 count and cannot be checked on any host's arrivals after 2023; it opens Brennia, which registers the smallest share of arrivals. S2's account is checked on the 2011 to 2021 decade of every host and at mid-decade in Fenmark and cannot be checked after the 2021 census; it opens Marovia, whose departures table holds the smallest share, and flips Skarholm, Fenmark and Almera as well. S3's shares are checked on thirteen years of overlap and on the held-out years and cannot be checked on 2024 to 2026; it opens Tesmar, where exits rose most. Kestria is forced: every route of the lattice files three officers.
Sharp: S1: its wrong route passes the 2021 census (the account closed on raw arrivals reproduces it exactly) and its rigorous form is the field's own method; its right route commits to one census table as the level of every share; the evidence is in Orlava's census table and in the other partners' pairs, neither of which mentions Orlavan citizens abroad; the correction runs from 0.56 to 1.21 across hosts; its own figure is C1. S2: its wrong route is the hosts' own published tables and passes every arithmetic check; its right route commits to exits no table holds; the evidence is the census pair; the correction runs from 0.24 to 0.97; its own figure is C2. S3: its wrong route passes a hold-out on 2021 to 2023 only if the hold-out is run on the hosts' tables alone, which cannot see the years after them; its right route commits to a register that catches about a third of the moves; the evidence is in the home register's rows after 2023; the correction is a ratio of 1.06 to 1.77 on exits by host; its own figure is C3.
Earns: a run that loses only S1 earns 30, only S2 30, only S3 34 (50 or under each); the reflex route earns 13 and the rigorous standard route 16 (30 and 50 or under); S1 fixed alone earns 23, S2 fixed alone 16, S3 fixed alone 20 (each more than the reflex route and a third at most). The reflex route still lands Kestria's leavers (3,554 against a band of 3,240 to 3,790: its departures table is nearly complete and its exits hardly moved), kept because the ask is by district and a figure cannot be withheld for one of seven. The battery of 126 widened the bands from the draw's 18, which lets S3 lost keep Kestria's two figures and Fenmark's citizens and raises it from 30 to 34.

Risks carried at the draw, for the build and the triage to read: (1) S3 sits in plain sight (the partners' tables stop at 2023 and the home register runs on); a run that bridges the home register on the overlap earns it, and what is left is S1 and S2, where a run that loses either alone still earns 30. (2) S2's right route is the field's residual method once arrivals are right, and the gap between the censuses is large (the raw account misses the 2021 census by thousands), so a run that checks the closure may take it; taken on raw arrivals it is the S1-lost route. (3) C3 is a cheap figure for a run that reads the home register's timing. (4) The share model is multiplicative with a 2 per cent pair wobble and may read as tidy; the build keeps the wobble and adds nothing. (5) The citizens' bands are 1 to 4 per cent wide on the battery of 126; the answer blocks state exactly the battery's bands, and S3 lost keeps Kestria's and Fenmark's citizens inside their bands. (6) Skarholm, Marovia and Tesmar sit 1,469 to 2,950 from the line the rigorous route crosses, and that route lands only 503 (Skarholm) and 899 (Marovia) beyond it. (7) The placement is specific to seed 5127 (other seeds fail the core) and to the placed draw of Fenmark's decade, so the generator imports the core's world.

Architect's acts at the build (this thread is the architect's; each was re-proved by `generator/results.py` on the cut pack, CORE PASS level 5): (1) the battery grew from 18 to 126 variants (every two single conventions that change different choices, and one home register share pooled over the seven hosts), because the review's audit crosses conventions; the call holds under all of them and the bands widened, which lifts S3 lost alone from 30 to 34 and S1 fixed alone from 19 to 23. (2) `main` takes the cut pack's arrays and returns the spec, so the build prices the shipped files and not the world's. (3) R6 of the draw was split into R6 (citizens), R7 (leavers) and R8 (officers) for `effort.py`; no figure moved. (4) The decade to the 2021 census was redrawn (`COURSE`, `_decade`): at the draw arrivals changed level in one step at the 2021 census in six hosts, Fenmark's exit rate fell fourfold at its 2016 count, and the seven 2011 census counts were multiples of 250, all of which read as generator settings in the golden's own year-by-year account. Each host now moves to its later level over its own years (Skarholm 2016 to 2019, Marovia and Tesmar 2018 to 2020, Almera 2016 to 2019, Brennia's boom 2019 to 2021, Fenmark fading through the whole decade with its leavers rising), the 2011 stock is the one that reaches the unchanged 2021 census count, and the years from 2021 are byte for byte the draw's (`_later`), so every post-census dial, hurried choice and route is the one proved at the draw. The reflex, direct and larger-report routes are unchanged to the person; the golden moved by 12 to 205 citizens a district and files the same officers. (5) Fenmark's decade carries a placed draw (`PLACED`): its 2016 count read as a level moves every share by 1 to 7 per cent across 45 draws of the decade's noise, the joint forcing row holds in 14 of them, and draw 44 is the one of the three that also keep the world's own counts inside every band which prices lowest (30, 30, 34). (6) Nothing else in the core changed: the seed, the recording dials, the three hurried choices, the routes and the referee's date are the draw's.

## Stump factorial

Reflex route: every file cleaned and brought to one coding; the latest release of every table; the register's repeats removed and its events dated by the move; each host's 2021 census count rolled forward on its own arrivals and departures tables and its births and deaths of citizens to 1 January 2024 (the closure of 2011 to 2021 looked at and put down to the registers' known weakness); the mean arrivals, the exit rate and the natural rate of 2021 to 2023 carried through 2024 to 2026; the order applied as written. It files 44,061, 42,773, 51,395, 40,653, 13,246, 27,257, 71,324 citizens and 9, 9, 11, 9, 3, 6, 15 officers, wrong in six districts, and is the careful but hurried pass.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 a host's arrivals table is that host's share of the citizens who arrived, and the level of every share comes from Orlava's census table | stump | the host's arrivals table taken as the arrivals | L22, L51, N27 | 8, 9, 8, 8, 3, 6, 13: Brennia an officer short, Tesmar and Fenmark one over | 9, 12, 11, 10, 3, 6, 15: six districts wrong; R2 rescued | no (four dependent steps) |
| S2 a host's exits are what its two censuses, the corrected arrivals and the vital events leave, and its departures table is a share of them | stump | the departures table taken as the exits | L48, L32, N10 | 9, 12, 11, 9, 3, 7, 15: six districts over | 8, 9, 8, 9, 3, 6, 14: four districts wrong; R3 rescued for Skarholm only | no (four dependent steps) |
| S3 the moves of 2024 to 2026 come from Orlava's register at the share of each host's moves it caught on the years both report | stump | 2021 to 2023 carried forward | N13, N28, L03 | 8, 10, 8, 8, 3, 5, 13: Tesmar an officer over | 9, 9, 11, 8, 3, 6, 15: five districts wrong; R5's ratio rescued | no (three dependent steps) |
| J4 the tables, the register and the censuses cleaned: three code schemes, superseded releases, repeats, late entries, free-text states | reflex | - | R01, R13 | same call | - | - |
| J5 every file read, the unused ones set aside | reflex | - | R02 | same call | - | - |
| J6 an at-date population rebuilt from a count and its events and checked against the next count | reflex | - | R57, R93 | same call | - | - |
| J7 the establishment in force reproduced from the 2021 census counts | reflex | - | R18 | same call | - | - |
| J8 several windows tried for a carried value, a hold-out on the latest years, a 20 per cent stress on a fitted rate | reflex | - | R31, R03, R16 | same call | - | - |

Level: 5: three necessary stumps, none sufficient alone, the three single drops on three distinct wrong establishments and the lattice's seven shortcut routes on seven.

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| Brennia | 48,116, ten officers (3,116 above 45,000, 1,884 under 50,000) | 505 | wrong: 42,773, nine | wrong: 36,180, eight | S1 |
| Marovia | 36,684, eight officers (1,684 above 35,000) | 434 | wrong: 51,395, eleven | wrong: 45,954, ten | S2 |
| Tesmar | 32,950, seven officers (2,050 under 35,000) | 483 | wrong: 40,653, nine | wrong: 38,290, eight | S3 |
| Skarholm | 36,469, eight officers (1,469 above 35,000) | 251 | wrong: 44,061, nine | wrong: 41,120, nine | S2 (its drop alone files nine) |
| Fenmark | 22,826, five officers (2,174 under 25,000) | 803 | wrong: 27,257, six | wrong: 25,706, six | S1 and S2 (either drop alone files six or seven) |
| Almera | 62,662, thirteen officers (2,662 above 60,000, 2,338 under 65,000) | 317 | wrong: 71,324, fifteen | wrong: 67,622, fourteen | S2 (its drop alone files fifteen) |
| Kestria | 12,227, three officers (2,227 above 10,000) | 248 | right: 13,246, three | right: 11,516, three | forced |

Direct route: the pack's most direct evidence read at face value is each host's own tables: its 2021 census count with its registered arrivals, registered departures and vital events of 2021 to 2023, the figure for 1 January 2024 taken as the latest there is (`direct` in `generator/core.py`). It files 41,120, 36,180, 45,954, 38,290, 11,516, 25,706, 67,622 (officers 9, 8, 10, 8, 3, 6, 14), wrong on all six open members: it misses the unregistered arrivals where they are many (Brennia), the unregistered exits everywhere, and three years. The second direct reading, the larger of the two reports of each flow (`mirror`), files 44,237, 42,933, 47,884, 40,845, 13,526, 26,399, 71,566 (9, 9, 10, 9, 3, 6, 15), wrong on the same six.

## Data provenance

Source: generated by `task5/generator` from a simulated process: eight states of a free-movement area whose citizens move among them year by year; each state's population register recording a move only when the mover registers or deregisters, at that state's habit; each state transmitting its tables to the area's statistical office two years after the reference year; a census in every state on 1 January 2011 and 2021 (and in Fenmark on 1 January 2016); Orlava's municipal clerks keying deregistrations and re-registrations into the central register.
Behaves like the real thing: register-based migration statistics disagree in exactly this way: the receiving state usually reports more than the sending state, departures are registered far less than arrivals, a state that registers short stays reports more arrivals than its partners report departures, and census counts of foreign citizens do not close with the registered flows between them. Flows follow each host's economy with noise and move from one level to another over several years, each host at its own time (no series changes level between one year and the next, `checks.py`); natural change is small and steady, and no state's share is a round constant across pairs (a 2 per cent pair wobble and binomial recording).
Genuine patterns: (1) arrivals that track each host's labour market, with a boom destination and a fading one; (2) exits that rise with the stock and turn up after 2023 by a different amount in each host; (3) the receiving state's report above the sending state's in most pairs and below it in some; (4) departures registered far less than arrivals in every state; (5) a fading destination, whose arrivals fall through the decade while its leavers rise, and a boom that takes off over 2019 to 2021; (6) births well above deaths in a young migrant population.
Problems by process: superseded releases (states resend corrected tables); three code schemes (the hub, the national releases and the register each keep their own); repeated register events (a municipality's queue re-synced); events entered weeks after the move (clerks key from paper); free-text states beside the code (older municipal software); census tables by citizenship and by country of birth side by side (the census regulation asks for both). Each comes from the system that writes the file, and none moves a result.
License: none needed (generated).
Used as is: not applicable (generated).
Breadth: 14 or more files: Orlava's register events 2011 to 2026 (several hundred thousand rows), the hub's migration tables by reporting state, table, partner, year, sex and age group across its releases (41,508 rows), the census tables of eight states in two rounds, the vital events of foreign citizens, Fenmark's 2016 count, Orlava's census transition table, the staffing order, the area's regulation, the establishment in force, the code table, the municipality list and two unused files; 56 state pairs with two reports each, so choosing which pairs carry information on a host's share is work.

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, decomposition-attribution, validation, modeling, synthesis
Question form: how-many (how many officers each district needs, on how many citizens)
Nearest build: task19 shares the subdomain and corrects one register's district counts with a field follow-up and a coverage survey linked without a key; nothing is linked here and no list is matched, the quantities are aggregate flows that two states each report, and the work is the level of each state's share and the years no partner covers. task8 counts reading groups to a standard from three tests of the same pupils and shares the decision form only. task4 closes a stock account for a loss; here the account's inflow is itself an estimate whose level the account cannot fix, and the account ends six years before the date. precut's nearest-chain WARN names task17 (a computing centre's GPU allocation cap from a scheduler log, a distribution cut with its weight on modeling): the two share four chain areas in another order and nothing else, neither the shape (an allocation against a head-count standard here) nor the weight (assembly here).

## Frontier check

Precedents: R2 careful Missed on L22 (the published formula whose generating assumption the data contradict: the reference-recorder scaling where one state over-records), L51 (the most rigorous standard design the pack affords built unprompted, its own check blind to the difference) and N27 (a second record at another grain set aside: the census transition table, which names no host); R3 Missed on L48 (a balance residual kept as noise rather than read as the unrecorded term), L32 (the residual the fitted account under-predicted left unattributed) and N10 (missing periods or flows assumed to run at the observed rate); R4 Missed on L28 (the estimator certified with checks that cannot see the problem: the route checked on the 2021 census it was closed on), L29 (small gaps taken as confirmation) and L03 (a second log at another grain set aside: the 2016 count); R5 Missed on N13 (the latest observed rate taken as the state at the decision date), N28 (inputs another process re-sets during the window held at their latest values) and L03; R6, R7 and R8 fall with R2, R3 and R5 (N27, L48, N13).
Shallow path checks: the hosts' tables at face value pass every arithmetic check on their own rows; the account closed on arrivals as recorded reproduces the 2021 census exactly, because the exits are defined by it; a hold-out of 2021 to 2023 on the hosts' tables passes for the carried route in the hosts whose flows were steady. What refutes them is of another kind: Fenmark's 2016 count at mid-decade (a file at another date), the other partners' emigration tables against a host's arrivals of their citizens (a file at another population), Orlava's census table against its own register (a file at another state) and the home register's rows after 2023 (a file at another window).
Assumption made false: the receiving state's count is the flow (false: a register counts registrations; tested by the partners' emigrants against a host's arrivals, where the sender often reports more); the fullest recorder is complete (false: one state registers stays under a year; tested by the census table, which puts Orlava's share at 0.72 where the scaling gives 0.59); registered departures are the exits (false: leavers seldom deregister; tested by the two censuses); the last reported years hold to the date (false: exits rose 10 to 120 per cent after 2023; tested by the home register's re-registrations by origin).
Forcing: the lines are the multiples of 5,000. Across the 126 rebuilds of the battery the nearest approach to a line is Skarholm at 36,218 (1,218 above 35,000), then Marovia at 36,250 and Brennia at 48,482 (1,518 under 50,000); every variant files the golden's officers, and the world's own counts sit in the same bands. The shortcuts land across the lines: S1 lost Brennia 41,429 (3,571 under 45,000), S2 lost Marovia 54,594 (14,594 over 40,000), S3 lost Tesmar 36,987 (1,987 over 35,000); the reflex, direct, larger-report and rigorous routes are wrong on every open member. Each fitted input (the host's arrival share, its departure share, the home register's share of moves and of exits) moved one measured spread up and down (the furthest any rebuild moves it: 1.6 to 2.6 per cent on a host's arrival share, 2.5 to 5.8 on its departure share, 2.6 to 7.4 and 2.5 to 8.9 on the register's shares), and all four together one spread each, files the same officers; the nearest row is Skarholm at 35,468 with all four down together. Two spreads on all four together to one side moves three districts down and one up, which the note records: the four are fitted on one another (the departure share and both register shares rest on the arrival share), so the joint row already overstates what can move together. The determinism judge's strongest rival (each host's two shares fitted on its own census accounts of seven citizenships, no second report and no census table) is on the golden's side of every line in all eight fits (nearest 633, Marovia at 35,633) and is refused as a source of figures by the six senders' reports (5 hosts outside), the 2021 counts and Fenmark's 2016 count (216 to 296 off against 96); read for the level alone it gives 70.8 to 72.2 per cent against the census table's 72.0, inside every band across 112 rebuilds.
Noun swap: nearest on file by `skeleton.py check`: severity none against every card, the client's corpus and the slot's lineage. task22 and task4 share one lesson (a conservation residual) and one detection; swapping either's nouns in (a gas district's unaccounted volume, a keg fleet's losses) carries the residual and nothing else: no second reporter of the same flow, no level the cross-reports cannot fix, no years outside every counterparty's record.
Closed strategies: the call turns on three lessons, none on the client's closed page: latent_structure_estimation (reporting shares identified from cross-reports up to a level, the level from an independent count), conservation_residual_attribution (exits as what the account between two censuses cannot otherwise hold) and observation_window_coverage with validation_cannot_see_condition (years outside the counterparties' record taken from a second record at a fraction measured on the overlap). Nearest closed cards and how each differs: "recent counts are still filling in (reporting lag)" has reports still arriving and is fixed by delay factors by route; here nothing for 2024 to 2026 will arrive before the decision, the 2023 tables are final, no delay factor exists, and the fix is another register at its measured share. "Two sources that are not independent (capture-recapture)" links two lists of the same individuals; here nothing is linked, the two reports are aggregates, and the unknown is each reporter's share. "The instrument changed" corrects a series across a break in its own instrument; here no series changes basis, one ends. Supporting steps from the closed page: none. A run that applied delay factors or a capture-recapture formula would have no rows to apply them to.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a citizen | a person registered as an Orlavan citizen in the state of residence; a person born in Orlava | registered as an Orlavan citizen | the order 2.2 and the regulation article 2 file citizenship as registered; the census workbook's country-of-birth sheets are a different population |
| SF2 | a change of citizenship | a resident who takes the host's citizenship leaves the population; stays in it | stays: citizenship is as registered on arrival and kept while resident | the regulation article 2 files it, and no table of acquisitions exists |
| SF3 | usually resident | living or intending to live in the state twelve months or more; registered at an address on the day | twelve months or more | the order 2.2 and the regulation article 2 |
| SF4 | 1 January 2027 | the population at the start of the day, the 2021 census count plus the moves and vital events of calendar years 2021 to 2026; at the end of the day | the start of the day | the regulation article 4 (a census and a population count refer to 00:00 on 1 January); same call |
| SF5 | one officer for every 5,000 citizens or part of 5,000 | the count divided by 5,000 and rounded up; rounded to nearest | rounded up | the order 2.1 ("or part of 5,000"); no variant comes within 1,200 of a multiple of 5,000, so an exact multiple does not arise |
| SF6 | a district | one partner state; a consulate's own catchment | one partner state | the order 1.1 and its schedule |
| SF7 | moved away from a state | ceased to be usually resident there, whatever the destination, deaths not counted; returned to Orlava only | whatever the destination, deaths not counted | the prompt's words ("moved away from that state"); the regulation article 2 defines emigration without regard to destination and tables deaths separately |
| SF8 | the window of the leavers | 1 January 2021 to 31 December 2026; to the last reported year | to 31 December 2026 | the prompt ("between the 2021 census and the end of 2026") |
| SF9 | the year of a move | the calendar year of the move; of its entry in the register | the move | the regulation article 2(e); the register carries both dates, and dated by entry every figure keeps its band (same call) |
| SF10 | which release of a table | the latest release holding the year; the first | the latest | the regulation article 6(3) (a later release replaces an earlier one); on the first release of every cell every figure keeps its band (same call) |
| SF11 | an arrival of a citizen | every registered arrival of an Orlavan citizen in the host, whatever the previous residence; arrivals from Orlava only | every registered arrival of an Orlavan citizen | the regulation article 3 files Table A by citizenship, with no split by previous residence; in Orlava's register, the one file that carries both, a foreign citizen's arrival is always from the state of citizenship, so the two readings are one count |
| SF12 | births and deaths of citizens after 2023 | carried at the 2021 to 2023 rate per citizen resident; carried as the 2021 to 2023 count; left out | the rate | same call: the count is a member of the family (at most 59 citizens' difference); left out is refused by the tables, where births exceed deaths in every host and year |
| SF13 | the years the shares are fitted on | 2011 to 2023; 2014 to 2023; 2016 to 2023; 2011 to 2020 | 2011 to 2023 | same call: each is a member of the family |
| SF14 | how the senders' ratios are pooled into a host's share | the ratio of sums; the mean or the median of the senders' ratios; the smallest sender dropped | the ratio of sums | same call: each is a member of the family |
| SF15 | the level of the shares | Orlava's 2021 census table against its register's arrivals of 2020, pooled or by partner; Fenmark's two half-decade accounts; the fullest recorder set to one; the shares' own average set to one | the census table, pooled | the census pooled, by partner mean and by partner median, and Fenmark's accounts are members of the family; the fullest recorder is refused by the census table (0.59 against 0.72) and by the 2016 count (off 1,181); the shares' own average is refused by the same two (0.88 and off 1,194) |
| SF16 | the home register's shares after 2023 | each host's own share on 2011 to 2023; on 2016, 2019 or 2021 to 2023; one pooled share for all hosts | each host's own on 2011 to 2023 | same call: the windows and the pooled share are members of the family |
| SF17 | the timing of exits within 2011 to 2023 | the departures table's years scaled to the decade's exits; the home register's re-registrations by year scaled the same way | the departures table's | same call: a member of the family |
| SF18 | the 2016 count | a check on the account; a third census that splits Fenmark's decade | a check | same call: split, it is the family's Fenmark variant |
| SF19 | stated precision | citizens and leavers to the whole person, shares to 0.1 per cent, the ratio to two decimals, each with its band | as listed | the answer blocks state each figure's band; the prompt dictates no rounding |
| SF20 | the moves of late 2026 | all entered by the file's last entry; the slowest entries of the last days still to come | entered, to about one event | same call: an entry follows its move by 42 days at most across sixteen years and the file's last entry is 40 days after 31 December 2026, so only entries slower than that for the 172 moves of the last 2 days can be outstanding (1.1 per cent of entries are: about 1 event); stated in step 1 |
| SF21 | the census table's other citizenships | left out of Orlava's arrival share (the seven partner citizenships); counted in | left out | same call: counted in, the share is 72.2 per cent against 72.0 and every citizens figure keeps its band |
| SF22 | a register event sent twice | counted once (the same event number); counted as rows | once | same call: with the repeats left in every graded figure keeps its band |
| SF23 | the level of the shares, read from the hosts' own censuses | Orlava's census table; one factor on every host's share fitted by least squares on the 49 census accounts of the hosts' foreign citizenships, the two reports' ratios between hosts kept (four weightings, the accounts pooled or each host's weighed equally) | the census table | same call: the 49 accounts put Orlava's arrival share at 70.8 to 72.2 per cent against 72.0, and every stated figure stays inside its band alone and with each other single choice of the battery (112 rebuilds, `results.closure`) |
| SF24 | a host's departure share | closed on the Orlavan citizens' own account; pooled over the host's seven foreign citizenships; fitted with the arrival share on those seven accounts | the Orlavan account | filed in step 4. Pooled, Skarholm's share is 48.5 per cent and carries its 2011 count to 38,414 against the 38,003 counted. Fitted on the seven accounts (the determinism judge's strongest rival) both shares file the golden's officers in all eight fits (nearest line 633, Marovia at 35,633) and are refused by named data: the share lies outside every sender's reading in 5 hosts, the 2011 counts are carried 273 over the 2021 count in Skarholm and 382 under in Brennia, and Fenmark's 2016 count is missed by 216 to 296 against 96 |
| SF25 | a share above 100 per cent | kept as measured; capped at 100 | kept | same call (Kestria files 3 officers either way); capped, its two figures leave their bands (11,698 citizens, 5,219 moved away), and the cap is refused by the six senders (117.5 to 124.8 per cent each) and by the home register's share of its citizens' moves there (31.8 per cent against 35.1 to 38.0 in the other hosts); stated in step 3 |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| the rate | one officer for every 5,000 citizens or part of 5,000 | the Consular Establishment Order (.pdf), 2.1 |
| the date | 1 January 2027 | the Consular Establishment Order (.pdf), 2.1 and 3.1; the prompt |
| the census dates | 1 January 2011 and 1 January 2021 | the hub's census workbook (.xlsx); the regulation, article 4 |
| Orlava's share of foreign arrivals | 0.720 | measured: Orlava's census table of foreign citizens by residence a year before (.xlsx) against its register's arrivals of 2020 (.csv); the family's pooled, mean and median readings span 0.720 to 0.723, and 0.722 with the table's other citizenships counted in |
| each partner's share of its own emigrants | 0.378 to 0.815 | measured: its Table B flow to Orlava against Orlava's Table A arrivals over the share above (the hub's releases, .csv) |
| each host's arrival share | 1.004, 0.558, 0.852, 0.707, 1.213, 0.668, 0.890 | measured: the other partners' Table B flows to the host, each over its sender's share, against the host's Table A; measured spread 1.6 to 2.6 per cent across the battery |
| each host's departure share | 0.473, 0.419, 0.242, 0.457, 0.967, 0.320, 0.549 | measured: its Table C against the exits its census pair leaves; measured spread 2.5 to 5.8 per cent |
| Orlava's share of moves to each host and of exits from it | 0.351 to 0.386 and 0.405 to 0.444 | measured: the register's deregistrations and re-registrations by state (.csv) against the two lines above on 2011 to 2023; measured spread 2.6 to 7.4 per cent on moves and 2.5 to 8.9 per cent on exits |
| births less deaths after 2023 | each host's 2021 to 2023 rate per citizen resident | measured from the hub's Table E (.csv) |
| the referee | 19,580 citizens in Fenmark on 1 January 2016 | Fenmark's 2016 count (.xlsx) |

Variant battery: 126 variants of the golden route in `generator/core.py` (`FAMILY`), run on the cut pack by `generator/results.py`: the golden; Orlava's share as the mean and as the median of the seven partners' ratios; a host's share as the mean and as the median of its senders' ratios; the smallest sender to each host dropped; the shares fitted on 2014 to 2023, on 2011 to 2020 and on 2016 to 2023; the home register's shares on 2016 to 2023, 2019 to 2023, 2021 to 2023 and 2011 to 2020; one home register share for all seven hosts; exits timed by the home register's re-registrations; births less deaths carried as a count; the level taken from Fenmark's two half-decade accounts; two combinations from the draw; and every two of the single conventions that change different choices. Every variant files the same call, 8, 10, 8, 7, 3, 5, 13, and every graded figure of every variant sits inside its stated band (`checks.py`, R7). The golden uses no constant only the core knows: the world's dials (the shares, the share of leavers who come home, the share of returners who re-register) never enter `chain`, and `generator/verify.py` rebuilds every stated figure from the shipped files without importing the core.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: persons registered as Orlavan citizens and usually resident in each of the seven partner states; children born to them in the host included from birth (Table E) |
| 2 | Unit of account: persons, whole; officers, whole |
| 3 | Attribution window: calendar years of the move; the leavers' window 1 January 2021 to 31 December 2026 |
| 4 | As-of dating: the population at 00:00 on 1 January 2027; the register extract of 19 February 2027 holds every event dated to 31 December 2026 |
| 5 | Version basis: the latest release of each hub table (the release of May 2026 holds 2023); the order as in force for the 2027 to 2029 cycle |
| 6 | Denominator: a share is recorded moves over estimated moves on the stated years, the ratio of sums |
| 7 | Weighting: senders weigh by their flows in a host's share; hosts weigh by their flows in Orlava's emigrant share |
| 8 | Window length: shares on 2011 to 2023; the account on 2011 to 2020; natural change after 2023 at the 2021 to 2023 rate |
| 9 | Boundary inclusivity: an exact multiple of 5,000 would take the lower number of officers; none arises |
| 10 | Rounding path: full precision to the end; citizens stated whole, each with its band |
| 11 | Tie-break: none needed; no variant comes within 1,200 of a line |
| 12 | Maturity and censoring: events entered late are in the extract (the latest entry lag is 42 days and the extract of 19 February 2027 holds entries to 9 February); the 2023 tables are final under article 6 |
| 13 | Order of operations: the conformed tables, Orlava's share, the partners' emigrant shares, the hosts' arrival shares, the citizens' arrivals, the account and the departure shares, the register's shares, 2021 to 2023, 2024 to 2026, the officers |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: a register event repeated after a re-sync (the same event number) counted once; a table cell in two releases taken from the later |
| 16 | Identity normalisation: one state code across the three schemes by the code table; free-text states resolved by the same table's names |
| 17 | Netting against gross: arrivals and exits are gross flows; nothing is netted before the account |
| 18 | Dimensional units: persons; persons a year; shares as fractions; the ratio of two three-year sums |
| 19 | Code and status semantics: the register's event types (deregistration abroad, registration from abroad), citizenship code, state of next or previous residence |
| 20 | Integerisation: nothing is rounded before the officers are read |
| 21 | Clause scope: the order's rate applies to each district separately; no minimum or maximum establishment is filed |
| 22 | Forward window contents: none forecast; 2024 to 2026 are estimated from the home register and the date is the day after the last event |

## Literal reader

The order's clause 2.1 executed word for word on the golden's seven counts files the golden: 36,469 citizens are seven full 5,000s and a part, eight officers; 48,116 ten; 36,684 eight; 32,950 seven; 12,227 three; 22,826 five; 62,662 thirteen. The regulation's articles executed word for word give the conformed tables of R1 (the latest release, the calendar year of the move, citizenship as registered) and nothing of R2 to R5. No shipped sentence, executed literally, produces a share, an exit or a 2027 count; the establishment in force executes to the 2021 census counts.

## Prompt contract

A rewrite keeps: the question in the how-many form (the officers each consular district needs for the 2027 posting cycle); the reason the answer rests on an estimate (the order counts citizens resident on 1 January 2027 and nobody has counted them since the 2021 censuses); the three figures for every state by their plain definitions and units (citizens resident on 1 January 2027; the officers the order then gives; citizens who moved away from that state between the 2021 census and the end of 2026); the deliverables by type (a spreadsheet with the estimates and a chart, a CSV of each state's population account by year from 2011). A rewrite never adds: that registers miss moves or which ones, the home register, the year the partners' tables end, a census question, a method, a comparison, a check, a file name, a count of districts or files, who is asking, a rounding rule or a warning.

## Build brief

World: Statistics Orlava (an invented central European republic of 3.9 million people) supplies the Ministry of Foreign Affairs' Posting Board with the number of Orlavan citizens usually resident in each of seven partner states of the Common Movement Area (Skarholm, Brennia, Marovia, Tesmar, Kestria, Fenmark, Almera) on 1 January 2027; the Consular Establishment Order staffs each district at one officer for every 5,000 citizens or part of 5,000. The engine is `generator/core.py`'s `simulate()` and `records()`: citizens of each state moving among the eight states year by year from 2011 to 2026 (`T`), each host's stock of Orlavan citizens from its 2011 census with arrivals, exits and births less deaths (`W`), each state's register catching its own share of arrivals (`a`, `A_HOME`) and of its own emigrants (`B_HOST`, `B_HOME`), a host's departures table catching `d` of the exits, half the leavers coming home and four fifths of those re-registering, the partners' tables ending with 2023 (`LAST`) and Orlava's register running to 2026. The build lays records over the core's yearly arrays and changes none of them: each yearly count becomes register events or table cells that sum back to it exactly (by sex, age group, municipality and date), which `checks.py` asserts for every array the golden reads.
Frozen: SEED 5127; the eight states, the years, every dial of `W` and the share constants; the census dates and Fenmark's 2016 count; the rate (5,000) and the date; each host's placement (`n0`); the golden's route (`chain`, `factors`), the three hurried choices (`HURRIED`), the direct, larger-report and rigorous routes, the battery (`FAMILY`) and the forcing (`spreads`, `--forcing`); the three components (Orlava's emigrant share, Skarholm's departure share, Tesmar's ratio) and the two asks (citizens on 1 January 2027, leavers from the 2021 census to the end of 2026); Orlava's census table covering foreign citizens only; no stock of citizens for any host between or after the censuses except Fenmark's 2016 count.
Files: (1) Orlava's population register migration events 2011 to 2026, one row per deregistration abroad or registration from abroad (event number, date of the move, date of entry, municipality, event type, citizenship, sex, year of birth, state of next or previous residence as a code and as the clerk's text), citizens and foreign citizens, area states and the rest of the world, with re-synced repeats and late entries: the 20,000-row file and the largest; cleaned, its counts by year and state equal the core's `recD[HOME]`, `ret` and `recA[:, HOME]` and Orlava's own cells in the hub's tables to 2023. (2) The hub's migration tables as released, one long file per release (reporting state, table A to D, partner state or citizenship, year, sex, age group, persons), later releases repeating earlier years with small corrections, to 2023: the long printed file. (3) The hub's Table E, births and deaths of foreign citizens by reporting state, citizenship and year to 2023. (4) The hub's census workbook: usual residents by citizenship and, on separate sheets, by country of birth, each state, 1 January 2011 and 2021. (5) Orlava's census table of foreign citizens by citizenship and place of usual residence one year before the census (same address, elsewhere in Orlava, abroad), 1 January 2021, with no row for Orlavan citizens. (6) Fenmark's population count of 1 January 2016 by citizenship. (7) The Consular Establishment Order (two to three pages, exported by the house PDF writer): districts, the rate, the population and date, the cycle and the Board's meeting. (8) The area's regulation on migration and population statistics (three to four pages): definitions, the six tables, the reference year, transmission and release. (9) The establishment in force by district, set in June 2023 on the 2021 census counts. (10) The code table for the three state code schemes with the state names. (11) Orlava's municipality list. (12) and (13) two unused files that look relevant: the hub's total usual residents of each state on 1 January of each year (all citizenships together), and passengers between Orlava and each partner state by quarter and mode (air, rail, coach), 2011 to 2026; neither is named as unused anywhere in the pack. (14) The Posting Board secretary's one-page request of 11 January 2027. Two or more file categories (spreadsheets and text), the pack at 30 MB or more.
Never filed: a sentence that a register misses moves or counts stays under a year; completeness, coverage, under-registration or over-registration of any state's tables; any state's registration rule or duration threshold; which state's tables are best; mirror statistics, double entry as a method, a reference country, an adjustment or correction factor; that the census table measures arrivals the register missed; error of closure, intercensal adjustment, residual; that leavers do not deregister; that the home register can stand in for the partners' missing years; a share, ratio or rate of any of these for any state; a stock of Orlavan citizens in any host between or after the censuses other than Fenmark's 2016 count; a survey estimate, consular registrations, voters abroad, passports issued abroad or any other count of citizens abroad; a file, sheet or column named for any of these; any document that describes the data files.
Goldens: `orlava_citizens_abroad_account_2011_2027.csv`: one row per host and year, the citizens resident on 1 January, the year's arrivals, exits and births less deaths as estimated, 2011 to 2027. `orlava_consular_staffing_estimate_2027.xlsx`: the first sheet states the officers for each district, the change on the establishment in force and what the estimate rejects, with one chart of the seven counts against the 5,000 lines; behind it the account by host, the recording shares, the 2016 check and the held-out years, the sensitivity of each district's officers to each fitted input, and a routes sheet showing what each shortcut files. Every figure from `figures.json`; both through the house writers.
Free: nouns beyond the people and the invented names; the document genre and wording inside the Never filed list; Layer 1 texture and its rates (every item resolving exactly); the split of each yearly count by sex, age group, municipality and date; the rest-of-world rows; the two unused files' contents; file names and formats; the number of releases.


## Leak rulings

`leak.py --asof 2027-02-22` on the cut pack: REVIEW, no LEAK. Each line:

- `consular_establishment_order_14_2025.pdf`, sixteen of the call's nineteen distinctive words: harmless. They are the
  seven district names of its Schedule and the words establishment, officers and cycle, which the order exists to
  define. It carries the rate (one officer for every 5,000 citizens or part of 5,000) and no number of citizens or
  officers for any district.
- `consular_establishment_order_14_2025.pdf`, six words of the stump paragraph (register, registered, orlava,
  skarholm, fenmark, reports): harmless. "Registered" is clause 2.2's definition of a citizen, "reports" is clause 4's
  duty to report, the rest are names. No clause says what a state's tables hold or miss, names a source for a term of
  the account, or orders a step.

The reader (one pass, Sonnet at medium, on fresh copies of the prompt and the pack): no sentence that hands over a
result's step, no ranking artifact, no helping file, no figure that reads as the answer; the sentences it quoted for
questions 1 and 5 are the Order's and the Regulation's definitions of what is counted, when and in which unit, and
executed literally they are the golden's estimand. One realism tell, fixed in the generator: the states' whole
populations were round numbers (each now has its own level and growth; only the own-citizens cell and the total of
each state moved, no cell any step reads). Its answers and the ruling on each are in `leak_check_report.md`.

## Pre-ship check

- The bar re-read against the cut: eight results across assembly, missingness and measurement, decomposition,
  validation, modeling and synthesis; three stumps on different axes (against what a host's arrivals table is
  measured, what a host's exits are, when the last three years are read), each moving its own district across a
  5,000 line and none reaching the establishment alone (corelib on the cut pack: level 5, no fail). The answer is a
  quantity no register holds; the prompt opens on why it has to be an estimate.
- The hidden factor record against the cut pack: each process runs across every unit it can reach (all eight states
  record their own share of arrivals and of their emigrants, on all 56 pairs and every year; every host's departures
  table holds 24.2 to 96.7 per cent of the exits; exits rose after 2023 in all seven hosts, by 6 to 77 per cent), and
  each shortcut misleads in districts where it decides nothing as well as in its own.
- The effort test against `effort.py`: quick 9.0, careful 22.2, thorough 100; the largest hint rescues 1 of 8;
  figure by figure a run that loses one stump earns 29.9, 29.9 or 33.7, the reflex route 12.8 and the rigorous
  standard route 15.7.
- Forcing on both sides: 126 rebuilds on the golden's officers (nearest line 1,218), every stated band holding them
  all; the level read from the hosts' 49 census accounts inside every band across 112 more; the three single
  shortcuts, the reflex, the direct, the larger-report and the reference-recorder routes across the lines; each
  fitted share moved by its host's own spread, singly and all four together, the same officers.
- Truth anchors from the world's own records: the pack's arrays equal the world's record of every table and register
  series; the fitted arrival shares sit within five per cent of the world's dials and the departure shares within
  eight; the world's own citizens and leavers sit inside every stated band and file the same officers (`checks.py`).
- No generator setting in sight: the golden's account by year was read after the build and the decade to 2021 was
  redrawn on smooth courses (Architect's acts at the build); no series changes level between two years, no host's
  largest move falls at a census, the 2011 counts and the states' whole populations are not round.
- Gates on the final cut: `gates.py task5 --full` 11 gates, 0 FAIL, 3 WARN (precut's two answered WARNs, leak REVIEW,
  heart's three repeats), `checks.py` and `verify.py` green, two byte-identical builds, `figures_check.py`,
  `audit_containers.py` on the pack, the golden and both zips, as recorded in `pipeline.json`.
- The determinism judge, once (Fable at high): DETERMINISTIC, FIX_NOW, answer blocks only. Every stated figure
  reproduced to the unit from the Step-by-Step alone, step 8 replayed as exactly 126 rebuilds, 26 forks run with no
  district's officers changing unless a filed count refutes the route. Its five findings were taken in one generator
  pass (the census-closure rival ruled by figures and the level it gives added as a check, the departure share's
  account stated, the cap on a share above 100 ruled, four wordings, item 16's row count dropped); no stated figure
  or band moved, so no second pass is owed. After the pass the pack changed only in the states' whole populations
  (the realism fix above), cells no step, fork or rival reads; that is recorded in the report and the pass was not
  repeated.
- The prompt grepped against the world after the last change: it states no count, no file, no method and no role,
  and every phrase (usually resident, the staffing order, the 2021 censuses, moved away) is the Order's or the
  Regulation's.

## Tried and rejected

- 2026-10-18, at the draw: the seed's own move, reading 2019 tail numbers through today's register, is identity
  resolution decided by reading the register right (data semantics); kept as Layer 1.
- 2026-10-18, at the draw: a 2027 projection of commercial aircraft NOx after the 50-seat jets retire, decided by a
  departure queue's relief at the hub's runway: the same lesson as task459 (a rate read at the decision's operating
  level, not the period average) in the same pairing, and a second hub ground-time task after task469.
- 2026-10-18, at the draw: the transition effect read against not-yet-transitioned airports (staggered adoption):
  already taught by task136 and task230.
- 2026-10-18, at the draw: operations at untowered fields from a rate per based aircraft learned at towered fields
  (selection on the outcome) as the decisive step alone: one live degree of freedom (every rung a different rate on
  the same based-aircraft list); kept as a lower rung beside the network route.
- 2026-10-18, at design: based broadcasting airplanes laid up for the year counted among the never-recorded: the small
  count fields' ratios split (L08 2 airplanes to 5) and the family of rate estimators spread 3 per cent; dropped.
- 2026-10-18, at design: an N-number changed late in 2026 at a count field read as never recorded by its current
  address and moved L08's ratio; changes kept to fields without a count and before September (SF12 asserted).
- 2026-10-18, at design: piston helicopters in the fleet: Table 1 is airplanes only and would need a rotorcraft factor;
  the valley's helicopters are turbine.
- 2026-10-18, at design: field targets on whole kilograms gave leads of exactly 22.00 and 3.00; offsets added so no lead
  sits within 0.02 kg of a whole kilogram and no tower's operations on a hundred.
- 2026-10-18, at stage 4: W33 under R4b (the never-recorded share of based airplanes as the unrecorded share, reader
  round 1's route) sat 0.1 per cent under the line, so that rung named no set; W33's recorded lead raised 0.38 kg, R4b
  now 5.2 per cent over, the golden W33 at 14.1 kg.
- 2026-10-18, at stage 4: today's register as the ask's primary device (the moved addresses' piston months priced as
  the turbines): reader round 2 resolved MASTER and DEREG by issue and cancel dates and hit all twelve figures, so the
  honest cracker scored 100 and the pair 66.6; the device became the Registry's dates leading the swap.
- 2026-10-18, at stage 4: the Registry's dates trailing the swap (the turbine flying under the number before its
  certificate): the turbines visit fields without a tower in that window, so the register's dates would price
  untowered operations as piston and move the call, and four towers' turbines fly too little to clear the bins.
- 2026-10-31, architecture 1 spent at the batch 1 repair: `guard.py heart` BLOCKed it against task242, registered ninety
  minutes earlier in another session, on strategy composition_mix, calibration gold_standard_subsample, forum
  council_or_assembly, forcing event budget_or_appropriation and organisation family local_government, and on pattern E
  against task197. It is the same core puzzle as task242 (a detector's capture calibrated on a gold-standard subsample,
  corrected by the composition of what it misses), so the slot re-roots into another world, dataset and shell. The
  repair's lessons (no file describing the data, no count the data hold in the prompt, the shell under its quotas,
  metadata prose that says what the task decides) carry into architecture 2.
- 2026-10-31, re-root screens on the item-response-theory-test-equating cell, each dead on file: item position effects
  in pre-equating (task482 v6, landed at stage 4); rapid guessing in a low-stakes sitting (task479 v4); drifted or
  released anchors and non-equivalent groups (task450, task471); rater severity on a shared subset (task471 v2).
- 2026-10-31, re-root screen: a computer-based mode effect read against students' prior paper scores with the prior's
  measurement error corrected. Rejected before code: the correction is a model of the measurement (the sampled case of
  `guide-to-prompt`'s ETL pincer, whose estimate spreads across reasonable settings), and with schools opting in, the
  school's mean prior score (measured almost without error) removes most of the bias, so the contextual model a strong
  analyst writes first lands the golden.
- 2026-10-31, re-root screens on the payment-claims and register cells: ACA grace-period cures (task482 v11, rule-heavy);
  high-cost regression to the mean, bundles against a comparison group, contract-order reconciliation and risk-adjusted
  ratios of totals (task487's screen); register over-coverage by signs of life (task478, task482); the seasonal
  adjustment cell's patterns (task453, task463, task467, task477, task481 spent).
- 2026-10-31, the world's first form, an Irish county council's vacancy programme: Ireland was drawn hours earlier by
  task268, and local_government is banned against task181, so the world moved to a Norwegian county pilot run by the
  national statistics office, where an empty dwelling is heated in November and the field's consumption floor fails for
  a reason of the country's own housing.
- 2026-10-31, at design: the weather service's hourly temperatures as a distractor: a temperature file beside an
  occupancy question points at heating, the decisive step's own premise; replaced by the power exchange's day-ahead
  prices.
- 2026-10-31, at design: holiday homes' and building sites' metering points in the hub's extract: a set of homes
  everyone knows stand empty, heated in November, would calibrate the empty profile for the solver; the extract covers
  the household points from each dwelling's day of use, as the data agreement would.
- 2026-10-31, at design: table B on organisation numbers, the KF and a one-step chain: a careful solver executing the
  ministry's definition kept all ten figures; rebuilt on the municipalities' own titles from before the business
  register (no number, the name of the day), namesake companies holding dwellings, and housing companies owned through
  the holding company and directly together.
- 2026-10-31, at design: the outages in three golden municipalities read as a pattern beside the answer; moved to
  Brekkevoll, Solmoen and Snøholt. Range-type household-day readings (a day's highest hour over its lowest) take an
  outage's zero hours as use in a vacant dwelling; with the outage log's hours left out they separate (SF12).
- 2026-10-31, at design: the Shock screen found the golden five were the five municipalities with the fewest flats;
  Hesteby's housing given more blocks and Snøholt's fewer, so no sort of a shipped statistic gives the set.
- 2026-10-31, at design: table A's renumbering in one or two blocks per municipality: a careful solver kept a cell where
  a small municipality's renumbered ground floors held nobody of one age band; blocks are now chosen until every band
  lives on the old ground floors on 1 November, a household taking in a child, a lodger or a parent where none does.
- 2026-10-31, at design: a register move dated before 1 November and registered after it opened two readings of "held
  as resident on 1 November" (the registration or the event date); the October moves are registered by 31 October
  (SF16).
- 2026-11-08, design repair after the portal's upload check (never run on the platform): the 2026-11-07 reword plus
  interval left the task reading as a regulation's threshold applied to counts and shares, with two tallies (persons
  by age, municipal holdings on the land register); both tallies dropped for the register's coverage errors against the
  estimate (SF26, SF27), and the ministry's letter no longer names Clopper-Pearson. The land, business and shareholder
  files stay in the pack, unread by any ask.
- 2026-11-08, at the repair: an interval from the occupancy reading's own error, measured on the dwellings whose
  residents moved inside the fortnight (373 dated events): the world draws a household's days at home independently of
  the register's move dates, so the meter does not follow them and the interval would not be forced; the basis is
  filed instead and only the wholly-above side graded (SF24).
- 2026-11-08, at the repair: grading which intervals take in or lie wholly below 5.0: Kvernhaug lies wholly below under
  the Wald interval and takes in the line under the exact, Wilson, Jeffreys and Agresti-Coull ones; only the
  wholly-above side, the same under all five, is graded.
- 2026-11-08, at the repair: net bias as the difference of the two rounded shares: Tverrvika and Hesteby move by 0.1;
  filed as one ratio of counts (SF27).
- 2026-11-08, at the repair: a re-root into a questionnaire module test (architecture 3, drawn and registered before the
  author's word) was withdrawn and the card and prompt restored: architecture 2 was never run on the platform, so its
  stump is untested and not spent.
- 2026-11-08, architecture 2 stump as filed: one-sentence rescue, judge H5 (determinism_check_report_arch2_pass1.md:
  DETERMINISTIC, SEND_BACK on Gate H, the household's rise cleanly bimodal so no statistical judgment was needed, H4
  weak, and no CSV of 20,000 rows); deepened in the same world with heating on daily timers (the rise now reads 70 vacant
  dwellings as lived in) and the household's departure from its own typical day as the decisive step, and the hub's
  daily values shipped as a CSV of over 100,000 rows.
- 2026-11-08, architecture 2 spent on its first platform round (target.zip 14f7ae29, runs saved under runs/): both runs
  read occupancy from each dwelling's departure from its own typical day (one subtracted the overnight baseline and the
  recurring local-hour pattern and cut the positive residual at 0.75 kWh, the other fitted day levels and clock-hour
  effects and cut the residual RMS at 0.20), filed the golden five and 396 vacant, and also rebuilt the 1 November
  register through the 20 renumbered blocks (359 people) and filed every coverage cell. The day-against-own-typical-day
  reading is a decomposition these runs make on sight; with the judge's earlier SEND_BACK the world is spent, and the
  re-root moves to another world, dataset and shell.
- 2026-11-08, re-root screen: a coverage survey whose non-contacts are mostly overcoverage, fixed by an admin auxiliary
  known for respondents and non-contacts alike: the same device as the signs-of-life screen task8 recorded (every
  activity window a threshold read as a fork), and once a run cross-tabs non-contact against the auxiliary the remedy is
  the textbook calibration; not drawn.
- 2026-11-08, re-root screen: a register-based estimate judged against a survey benchmark area by area, the observed
  discrepancy carrying the survey's design-based sampling noise: shrinkage ground (Survey 02 DOES NOT WORK), one
  correction concept, and task4 already carries a reliability correction; not drawn.
- 2026-11-08, re-root screen: a register count validated by its net agreement with the last census while gross over- and
  undercoverage scale with different migration flows: a projection whose deciding configuration (the components'
  divergence) is out of sample, the Gate C death of an open method; not drawn.
- 2026-11-08, at the draw: the decisive generator G12 (a missing report against a closed employer) repeats task8 v14 and
  v10, task6 v2 and mark196 on gap and Gate G under either gap order; G14 (the reporters' conditioned change) and G6 (the
  missing pool's mix) were banned against task7 v5 when it registered during the draw; G13 (the horizon
  on which a missing report's outcome lands) is the honest remaining label and carries no structural repeat.
- 2026-11-08, at the draw: the deliverable set csv+pdf crossed the corpus quota (three of nine prompts) when other builds took it during the draw; the certification moved to a workbook (csv+xlsx).
- 2026-11-08, prototype on the clean truth: with healthy employers late at the same rate at every size, the closed
  quarters' missing-alone pool was 63 per cent healthy by jobs (the healthy late filers are the larger employers), so
  its outcome (0.71 kept) did not transport to the shocked counties' pool (98 per cent distressed); the world now has
  large employers almost never late unless distressed, and the closed quarters start once four earlier quarters exist
  (habitual late filers misread as newly late in the first three), which put the pool at 95 per cent distressed and
  its outcome at about a quarter kept.
- 2026-11-08, prototype: a distressed agent client whose agent is also late cannot be told from its batch-mates, so a
  shock among clients of the late statewide bureaus is invisible to every reading; the shocked counties' exposed small
  employers file through local accountants (Garrow) or directly (Ostrom), and the year-end lateness sits with the
  statewide bureaus, as it does in practice.
- 2026-11-08, at build: new employers whose first report had not arrived (72, about 450 jobs) had no history to be
  estimated from, and nought, the median or the mean of the quarter's reporting new employers each moved twelve
  counties' changes by 0.1; the Division now posts a new employer's account from its first report, so no liable account
  without a report exists at the cut-off and the class is empty.
- 2026-11-08, at build (review): the missing-alone outcome taken separately for agent clients and direct filers read
  0.283 against 0.363 on the closed quarters and moved Garrow and Ostrom a bin each, because the direct filers' pool
  held healthy employers the agent clients' did not (habitual late filers in their second quarter after a birth or a
  succession, with one late report on file; local accountants' follow-up clients, whose small files formed no
  transmission; healthy one-off lateness weighted to larger employers). New and successor accounts now start on time,
  only the statewide bureaus send follow-up files, and healthy lateness runs at one multiple of the trouble hazard in
  every size class through both channels: 0.282 against 0.302, bootstrap s.e. of the difference 0.029, and the split is
  a standing member.
- 2026-11-08, at build: limiting follow-up files to the bureaus first drew their timing only for the bureaus, which
  shifted the timing stream and moved which agents ran late in every quarter (two late bureau files at the flash each
  had one switched client arrive, and the any-one-mate reading then designated Bray); the follow-up timing is drawn for
  the same agents as before and used only for the bureaus.
- 2026-11-08, at build: centring each county by its trend moved December 2025 as well as December 2026, and the
  rounding noise of the two levels was the size of the bin; a 2026-only nudge per county and the county size scale now
  centre each county's whole standing family inside one bin of change and one hundred of jobs.
- 2026-11-08, at build: the missing-alone outcome stated to three decimals (0.292) forked across the standing family
  (0.286 to 0.297 by window); it is stated as 0.29 in every block and the workbook.
- 2026-11-08, at stage 4 (judge, DETERMINISTIC and APPROVE, one open item): the judge's rebuild counted 27,652 liable
  and 4,275 outstanding against 27,651 and 4,274; the extra account was a new employer whose first-month closing
  notice was dated before its own liability date, so ordering the history by effective date left it active. Every
  closing and inactivation now takes effect after the account's own liability date, successors' register liability
  dates are their transfer dates, and checks.py asserts both orderings give one status.
- 2026-11-08, at stage 4 (reader): every closure took effect on the first of a month (3,842 of 3,842). An employer's
  notice of closing now names the day after its last payroll; the Division's inactivations keep the first of the
  month. Read literally, Schedule C then counted one outstanding employer at nought (its notice entered by the
  cut-off, its final report in its agent's late batch). Filing a closing employer's final report itself, with the
  notice, closed that and was rejected: a closing client's report arriving on time beside its agent's late batch made
  hundreds of late transmissions partly arrived, and the any-one-mate reading then designated no county. A notice of
  closing is now entered with the final report instead.
- 2026-11-08, at stage 5: the container ship gate (reduce-house-fixes H1, pulled from main during the session) fails
  a PDF written by ReportLab, and the house PDF writer needs LibreOffice, which this machine does not have; the Act,
  the data agreement and the rate notice now ship as Word documents written from the same stories by the house
  writer's Word stage and saved in Word's form (postprocess.normalize_docx), each with its own author and its drafting
  and last-save stamps, and both zips are cut by the house zip_folder with each file at its own save time. No
  sentence, cell or figure moved.
- 2026-11-10, architecture 3 returned at review (the author's account: one hidden trap decides it; the client's level 5
  wants three or four pieces of genuine analytical rigor, nothing planted, messy and ambiguous data with no rule to
  apply). Read against the bar of 2026-11-09 it is the returned shape: the fourth-quarter shock was built into the
  exposed employers of two counties only, their filing channels were set so the missing-alone reading would see them,
  and one sentence (a report missing from a transmission that arrived marks an employer in trouble) left a measurement
  on closed quarters. Re-rooted to architecture 4 as a results chain in the same world at the author's word.
- 2026-11-10, at the draw of architecture 4: a payroll bureau's change of reporting basis for the monthly counts (a mode
  change found from wages per job by transmission) as a tenth result: the Act's outcome is the report's month-three
  employment, so correcting a reported count is a reading of the outcome a literal judge could refuse; not drawn.
- 2026-11-10, at the draw: PEO client reporting, unposted successions and a claims file as further results: each is
  absorbed on average by the outcome measured on resolved quarters (a predecessor or a leased-out client ends at
  nought there), so it would grade nothing of its own; successions stay as texture.
- 2026-11-10, at the draw: uncertainty as its own result (a 90 per cent range per county, or the set of designations
  not settled at 90 per cent): the range's width spreads by a factor of two across honest methods and a set near the
  line asks for a thin margin; the replay on December 2025 carries how far the estimate can be out instead.
- 2026-11-10, at the draw: year-end lateness drawn afresh for every agent each year put between 5 and 14 per cent of
  jobs in late transmissions from one seed to the next and, at 14, moved small counties by 0.6 of a point on the
  choice of comparison cell alone; the same agents are swamped every January now (five bureaus, a fifth of the local
  accountants), which holds the share near 8 per cent in every fourth quarter.
- 2026-11-10, at design: with year-end lateness at 55 and 30 per cent of agents a quarter of all employers sat in late
  transmissions and the estimate's own noise (which of them had closed) reached 0.7 of a point in small counties;
  lateness now sits with the same swamped agents every January and the late transmissions hold about 7 per cent of jobs.
- 2026-11-10, at design: zero-wage placeholder reports that agents file to meet the due date and amend later, as a
  fifth judgment: a received report read as provisional is a reading of the outcome a literal judge could refuse, and
  a placeholder row reads as a planted defect; not built.
- 2026-11-10, at design: Bray kept out of the designated set only by the unregistered employers (the estimate without
  them at minus 2.1): the estimate's noise put the simulated truth on the other side of the line from the golden, so
  the flip was dropped; the unregistered employers move every county by 0.3 to 0.8 of a point and the state's sign.
- 2026-11-10, at design: county jobs to the nearest hundred let a crude estimate of the unregistered employers land
  inside most counties' ranges; they are graded to the nearest ten, the precision the family supports.
- 2026-11-10, at design: the worksite seasons sat at the lakes alone and the latest split misplaced jobs in three
  counties; lake summer trade, North Woods winter recreation and outdoor work and metro holiday retail now move five.
- 2026-11-10, stage 4, first cut: the seasonal lake resorts (55 late employers in Kittredge and Talcott on one fixed
  monthly profile, mostly clients of the statewide bureaus) and the step that carried them by their own December on
  September. The judge's rebuild put Kittredge at -2.4 to -2.0 against a -2.0 line and read the call as concentrated on
  that step; without it Kittredge read -1.7. A constructed subgroup in two counties, one of them deciding, found by one
  group-by and fixed by one routine step: the banned shape. Removed from the world and the method.
- 2026-11-10, stage 4, first cut: bands of 0.1 to 0.2 of a point from a 22-member family that varied only the golden's
  own settings. An independent rebuild sat outside Kittredge's band, outside the band on what employers outstanding on
  their own keep (0.25 against 0.27 to 0.32) and outside the unregistered employers' (540 and 2,150 against 560 to 620
  and 2,300 to 2,600). Bands now hold a 25-member family with those choices in it and a floor of a quarter of a point.
- 2026-11-10, stage 4, first cut: a careful pass granted the reading by cause and denied the development of the
  registrations. The judge's own derivation did the reverse, so the pass priced the wrong results (pair 47.5 on a
  route no careful run took). The careful pass is that derivation now (pair 40.5).
- 2026-11-10, second cut: a downturn that multiplied every housing employer's usual risk (9 to 18 times in the fourth
  quarter). To move Garrow by the point and a half the pooled reading needs, one micro firm in three had to be in
  trouble in a quarter; reshaped as a risk added alike to employers of every size under a hundred (11 points in the
  fourth quarter after 0.4, 1.2 and 3.5), which puts 7.9 per cent of construction jobs at employers outstanding on
  their own.
- 2026-11-10, second cut: Garrow's building tilt raised from 3.0 to 4.5 to deepen the downturn's bite there: half the
  county's jobs sat in the housing industries and the whole world reshuffled; left at 3.0.
- 2026-11-10, second cut: one world tuned by hand. County outcomes move by half a point from draw to draw (which
  employers are late, which have closed), so twelve seeds were scored on the same settings (the family's spread, the
  golden against the truth, what each hurried route does to Garrow and Kittredge, the replay); 50431 kept: the golden
  within 0.15 of a point of the truth in the three designated counties, the replay at 0.16 for the average county.
- 2026-11-10, second cut: the reporting employers' change by supersector statewide ruled out by a named fact (it
  differs by county within a supersector). It does not, by more than five points, in any supersector with enough
  reporters, and the variant lands in every band; it is a member of the family.
- 2026-11-10, second cut, after the re-judge: this quarter's share carried to the late batches graded as a critical
  component (about 590 jobs, construction employers at 0.79 against 0.84). A sound estimate without it stays in every
  band and the judge's rebuild left it out, so it fails the test for a component (a defensible method skips it and
  still reaches the answer); kept in the estimate as its own refinement, ungraded. The third result is now the look
  across quarters that says whether the closed quarters' evidence carries over, graded in the memo ask.
- 2026-11-10, second cut, after the re-judge: a floor of a quarter of a point on every band. The judge's second
  rebuild sat 0.3 to 0.45 away in Bray and Ostrom; the floor is half a point, and the careful pass still falls outside
  five counties by 0.7 or more.
- 2026-11-10, second cut, after the re-judge: every closed quarter with the unresolved left out (0.35) named as the
  hurried reading of what employers outstanding on their own keep. The judge read 0.33 on a sound definition; the
  reading is a member of the family and the range runs 0.24 to 0.37. The hurried figure there is the pooled 0.92.
- 2026-11-17, architecture 4 set aside before any platform round (READY 2026-11-10, never uploaded): its call turned on
  December reports still arriving, completed by cause and by batch, which is the client's closed reporting lag
  (2026-11-12); it had no proved core, no stump screen and no open-members table, its asks were totals every route
  rebuilds, and its prompt asked for a memo. The slot was redrawn in a new world with a new decision form.
- 2026-11-17, at the draw: a constant exit rate per resident as the third stump (the chance of leaving falls with years
  since arrival). Runs fit a duration profile wherever cohorts are tabled and nothing forces it where they are not;
  replaced by the three years no partner reports.
- 2026-11-17, at the draw: exits given a figure of their own on any host. The exits rest on the arrivals through the
  account, so every host's departure share fell with S1 as well; the figure is Skarholm's, which registers every
  arrival.
- 2026-11-17, at the draw: the rigorous route landing right on hosts whose flows balanced (shares scaled to the
  fullest recorder with the exits and the window as the golden takes them). Kestria made the forced member (its
  departures table nearly complete) and each host's 2011 stock placed by scan so the direct, larger-report and
  rigorous routes all land across a line.
- 2026-11-17, at the draw: the forcing row with all four fitted inputs moved two spreads to one side moved four
  districts. The four are fitted on one another, so the joint row is one spread each, which holds on both sides.
- 2026-11-17, at the draw: hosts' published annual stocks of foreign citizens, a survey estimate of citizens abroad,
  consular registrations and a July-to-June reference year. The first three would each size the districts on the
  question (Gate G, or a calibration set); the last is a reading of one field with an open conversion.
- 2026-11-17, at the build: in the register a foreign citizen's previous state differed from the state of citizenship on 8 per cent of
  arrivals. It opened a fork on which arrivals pair with a partner's Table B (by citizenship, or from that state only);
  an arrival of a foreign citizen is now always from the state of citizenship, as the world has it.
- 2026-11-17, at the build: a 2020 dip in the passenger traffic file. The world has no such year in its flows, so the file
  argued with the tables for no reason; removed.
- 2026-11-17, at the build: labour market indicators as the second unused file. They would read as drivers of the flows
  and invite a regression nobody needs; passenger traffic by partner state is as near and predicts nothing.
- 2026-11-17, at the build: the Order's 4.1 said citizens who have moved away, which left persons against moves open; it
  now counts emigrations under the regulation's article 2(c).
- 2026-11-17, at the build: the draw's world on level arrivals (one level to 2020, another from 2021, in six hosts), a
  fourfold fall in Fenmark's exit rate at its 2016 count and 2011 census counts that were multiples of 250. The golden's
  own account by year showed all three as steps at census dates; the decade was redrawn on smooth courses.
- 2026-11-17, at the build: Marovia's arrivals giving way over 2017 to 2019 from a start of 3,500 a year. The rigorous
  standard route then filed Marovia at 35,139, eight officers and right; the course starts at 3,700 with a steeper
  drift and the route files 34,101.
- 2026-11-17, at the build: Fenmark's decade on its first draw. Its 2016 count read as a level sat 3 to 4 per cent from
  the census table's, every measured spread grew by half and the joint forcing row crossed a line in two districts.
- 2026-11-17, stage 4: the judge's preferred repair, the census-closure fit (each host's two shares on its own seven
  census accounts) added to the battery with the bands redrawn. Skarholm's band would run to about 37,310 and the
  second component's to about 52.8, on a route whose own 95 per cent interval on Skarholm's share is 92.4 to 121.0
  per cent and whose shares contradict the six senders' reports in five hosts. Ruled out by those figures in the
  closing passage instead; what the 49 accounts can fix, the level, is run as a check and lands inside every band.
- 2026-11-17, stage 4: the states' whole populations as round levels growing 0.3 per cent a year (3,910,000 and
  4,027,300): the reader read the totals as generator rounding. Each state has its own level and growth.
