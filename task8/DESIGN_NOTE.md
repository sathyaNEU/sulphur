# task8 design note: which joining boards' banked portfolio marks Carrow Awards converts before the June 2027 awards, and by how many marks

Architecture 20, drawn on 2026-11-18 in a new world. Architecture 19 (Hollinbrook Academies Trust's Year 7 entry reading on one basis, READY on 2026-11-11 and never uploaded) was set aside before any platform round: it was cut before the core, open-members and rubric rules, two of its chain's lessons were closed by the client on 2026-11-12 and its asks sat on counts the careful pass rebuilds (`## Architecture 19 record`). Read `## Tried and rejected` first. Every figure below is printed by `python3 task8/generator/core.py` (with `--detail` and `--forcing`) on the world's arrays, seed 8134; the build replaces them with the cut pack's figures from `generator/figures.json`.

## Draw

Subdomain: Education & Learning Sciences, item response theory and test equating (linking marking standards)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a reconciled table plus findings: every joining board's banked portfolio marks placed on Carrow's marking standard (by board and series, and by centre in the CSV), with the boards the merger protocol converts, the direction and the conversion on top
Weight: measurement: the work is finding out what a board's moderation record measures (how much of a marking difference a moderator records, at which point of a centre's cycle, and against whose standard) and conforming seven boards' records to one standard with it; the three builds before this one sit on modeling (task3), a hard-to-measure quantity (task4) and assembly (task5). The guard's WARN that task1 also sits on measurement is answered here: task1 measures a recording algorithm's cut on one ledger, and nothing in this build is a recording rule
Data-native sentence: a centre's portfolio marks are checked only by a moderator who works from the centre's own marked record, only in the centre's rota year and only against that board's own principal, so the one record of how far marks stand from a standard holds a fraction of the difference, at one point of a cycle, on seven different standards, and the banked marks have to be placed on Carrow's from the three other records that each see one of those gaps.
People: Tamara McPherson (director of standards, Carrow Awards, who files the conversion), Arran Cullinane (assessment research analyst, the golden's author), Christina Flahive (principal moderator for the workshop portfolio, Carrow Awards), Kate Montague (head of data services, Carrow Awards), Dominic McHale (comparability, Office of the Examinations Regulator), Owen Hastings (secretary of the merger transition group) (`guard.py names --geo "Ireland" --locale en_IE --n 8 --seed 8134`)
As-of: 2027-02-08 (every board's 2026 series is closed and moderated; Carrow files the conversion with the regulator by 31 March 2027 and makes its first awards for the joining boards' candidates in June 2027)

Card `.claude/skills/fingerprint/cards/task8.json`, architecture 20, registered 2026-11-18: WARN only, skeleton severity none against every card, the client's corpus and the slot's lineage. overuse.weight (measurement, task1) is answered under Weight. overuse.objective (four of the last twelve are ETL) is the client's assignment. repeat.gate_g against task5 (etl_conformance): the honest label for a conformed record judged against a filed protocol; the fine numbers here are marks on a standard, there head counts in an account. repeat.deliverables against task3 and task5 (a CSV and a workbook): the house set; the CSV here is one row per centre and series and the workbook's first sheet a conversion table. The guard's first pass blocked the pattern (G3 against task3) and the organisation family (government_agency against task3): the largest mover of the call is the standard each board marks to (a unit-of-value swap, G1, which flips four boards), and Carrow is a not-for-profit awards body, as awarding bodies commonly are.

## Stump screen

Screened on paper and in `generator/core.py` before the card was registered (`references/stump-screen.md`, the seventeen tests).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A: a moderator works from the centre's marked record, so the difference a sample records is 36 to 71 per cent of the difference a marker working cold finds, a different share in every board | the moderator's mark is a second reading of the portfolio, so the recorded difference is the difference (L22, L28) | the standardisation trial: the year before's sampled portfolios marked cold by the whole team, joined to the mark the moderator gave the same portfolio live | none | kept (S1) |
| B: a centre is sampled once in a two or three year rota, tightens after the moderator's report and drifts until the next sample, so the marks it banks between samples sit 0.4 to 3.2 marks under its sampled year | a centre's last sample stands for the years it was not sampled; the sampled centres stand for the rest (N13, L37) | the centre's own mark sheets, every candidate every year: the level by years since the last sample, within centre and net of the board's year | none | kept (S2) |
| C: each board's moderators are standardised to their own principal, and the boards' standards stand 6.5 marks below to 1.8 above Carrow's; no portfolio was marked by two boards | a board's moderation measures its centres against the standard (N27, L06) | the people who moderate for two boards: their cold trial marks against each team's consensus, and each board's agreed marks against its consensus | none | kept (S3) |
| D: each centre's portfolio marks moderated statistically against its candidates' written paper | the paper is a common yardstick | paper marks by candidate | 1 and 12 (the fit is decided by regression to the mean and a flattened slope, both closed; and the boards set their own papers, so it links nothing) | dropped, and no paper marks ship |
| E: a difference inside tolerance is recorded as nil | the record holds every difference | the sample marks behind the record | 1 and the measured-dead table (a value at a limit is a bound, closed; a deadband is found and undone on sight) | dropped; the record carries every difference to the mark |
| F: the sample over-draws the top and bottom of a centre's rank order | the sample mean is the centre mean | the sampling rule | 1 and 2 (design weights are saturated and a reflex once the rule is filed) | dropped; samples are drawn across the range and the direction of the difference does not vary with rank |
| G: boards sample the centres whose last difference was largest | the rota is fixed | the moderation history | 1 (units picked at an extreme fall back, closed) | dropped; the rota is fixed by the centre's rota group |
| H: a principal's cold check of a slice of live samples as the instrument for the share | the labelled slice is fitted and carried | the slice itself | 2 and 12 (the strongest run fits a labelled sample and carries it unprompted, and what is left is carrying an effect to another mix, closed) | dropped; A took the trial, which is kept for another purpose and has to be joined back |
| I: centres that changed board, re-moderated by the new board, as the link between standards | a centre carries its marking across | transfer records | 7 of the banned list (how fast a centre takes up the new board's standard is an open fork) | dropped; centre numbers are board-specific and no centre changes board in the record |
| J: a joint alignment exercise in which every board marked the same scripts | none | the exercise | 2 (a fully crossed design is the field's textbook link and a reflex once it ships) | dropped; C took the people who moderate for two boards |

## Deep reasoning

Task type: item-response-theory-test-equating in Education & Learning Sciences, which serves Data Extraction & Conformation: seven boards' moderation and mark records conformed to one schema and one marking standard, with a single-group link between standards through the markers two boards share.
Domain test: every result is a quantity educational measurement estimates when marking standards are linked: the share of a marking difference a second marker records when the first mark is in sight, the level of centre marking through a moderation cycle, a board's marking standard placed against a reference through common raters, and marks expressed on another board's standard. The field's analyst asks of every moderation figure who marked, having seen what, when in the cycle and to whose standard.
Swap: "Which suppliers' declared weights does the depot re-base before the contract merges, and by how many kilos?" keeps a per-source conversion against a tolerance and nothing else: a weighbridge does not read lower because it was shown the declared weight, a supplier does not weigh more carefully after a check and drift, and no weighbridge is calibrated to its own foreman. The task stops making sense.
Where the weight sits: R2 to R4. Each is a measurement of the instrument, not of the centres: 480 trial scripts a board joined back to the live moderation of the same portfolio (R2); fifteen years of mark sheets for 170 to 260 centres a board, rota years rebuilt from the moderation record, a within-centre fit net of the board's year (R3); the registration numbers that recur in two boards' trials, each person's cold marks against each team's consensus, each board's agreed marks against its consensus, ten links over seven boards (R4).
Layer 1: seven boards' systems with their own layouts (one row per portfolio in some, one row per sample with the marks in a delimited field in others; centre numbers in board prefixes and in the national scheme), because each board bought or built its own; candidate numbers reissued on re-entry and withdrawn or absent entries left on the sheets with no mark; moderation records resent after an appeal, the later replacing the earlier; trial marks keyed by the moderators themselves, with blanks where a script was not reached and the unit's older 80-mark scheme in the earliest years. None decides a result: every one resolves exactly, and `checks.py` asserts the cleaned files reproduce the core's arrays.
Not one thing: the strongest single piece is the standards link, which flips four boards on its own. A run that nails it and nothing else still leaves Ardkeel alone when it stands 3 marks high (S3 fixed alone on the reflex route: 0.98, -0.38, 4.15, -0.76, 0.68, -4.05; 21 on the rubric), and every graded figure is still outside its band.
One-fact test: "each board's moderators mark to their own principal's standard, and the boards' standards differ by several marks" rescues R4 and nothing else (1 of 7 results), and only once the link is found and built in four steps: R2, R3 and every figure downstream still fall with S1 and S2.
Not semantics: every field, code, unit and clause read correctly leaves the reflex route where it is: a moderator mark is a moderator's mark, a sample difference a sample's difference, an adjustment an adjustment, the protocol's banked mark, series, standard and tolerance are as written, and the route still places five boards on the wrong side of the tolerance because of what a moderation difference measures, not because of what a column means.
Not rule application: the merger protocol files the population, the outcome, the standard, the tolerance and the conversion; the code of practice files sample sizes, tolerances, rota lengths and how an adjustment is applied. Neither performs R2 to R7. After every filed rule is applied the analyst still has to estimate what share of a difference a moderator records, where a centre's marking sits between samples and how far each board's standard stands from Carrow's.
Estimand: the merger protocol, section 2 (banked marks: the workshop portfolio marks awarded by a joining board in the 2025 and 2026 series, as awarded after moderation), section 3 (Carrow's standard: the standard of its principal moderator's agreed marks, as applied in its 2026 moderation), section 4 (a board's distance: the mean over its candidates with banked marks, the two series together, of the banked mark less the mark the portfolio merits at Carrow's standard, in marks; converted where the distance is 2.0 marks or more either way, by the distance), section 5 (the joining boards as a whole: the same mean over every candidate with a banked mark at any joining board), section 6 (filed with the regulator by 31 March 2027); the prompt (each joining board's distance for the two series together and for each series, the joining boards together, the boards converted and the direction). The method is filed nowhere.
No decoy: no memo, draft or column carries a wrong answer and no document argues for a route. Each board's moderation outcomes reproduce exactly from its sample marks by the code of practice; they answer a shallower question (was the centre within the board's tolerance of its moderator) and are priced on the golden's footing by the ask for every board's distance from Carrow's standard.
No replay: no result re-derives a published figure and no filed number is wrong.
Pinned: 98 variants of the golden's conventions in `generator/core.py` (`VARIANTS`: every single convention and every two that change different choices) file the same call and set every band; each fitted input moved one measured spread up and down alone, and all three together in every combination, files the same call (`--forcing`, exit 0); the rivals (the record raw, each board's own severity added, the last sample carried, each board's own principal as the standard) are each refused by a figure: the regulator's 2023 review of Dunmoyle on the centres not sampled that year (5.54 marks; the golden 5.70; the rivals 3.13, 6.74, 3.95 and 2.16).
Run forecast: R2 lost to a self-confirming check (the trial read as proof that moderators mark accurately, an additive severity taken from it, the live record never compared with it); R3 lost to dismissed own evidence (the rota seen, the unsampled centres carried at their last sample or left to the sampled ones, the mark sheets used for weights only); R4 lost to a method shortcut (each board's own principal taken as the standard, the boards compared on their own records); R5 to R7 fall with them. The honest expectation is that the review's strongest run finds one of the three (most likely the standards, which the question itself points at) and loses the other two: a run that loses one stump alone earns 22.
Strategy label: other (the moderation record's three blind spots each assigned to the record that sees it: a share from scripts marked twice for another purpose, a cycle from the centres' own marks, a standard from the markers two boards share; no label in `references/sulfur-strategies.md` names the three together)
Depth level: 5: three independent judgments on different axes, each necessary and none sufficient, the three single drops on three different wrong calls and the lattice's seven shortcut routes on five.
Lesson: a check made in sight of what it checks measures a fraction of the truth, and the fraction has to be measured where the same things were also judged cold; a unit checked once in a cycle is seen at the point the check itself creates; and local standards with no item in common are linked through the people who hold two of them. No build on file teaches any of the three.

## Results chain

Every figure below is from `generator/core.py` at the draw (seed 8134); the build replaces them from `generator/figures.json`.

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the seven boards' moderation samples, outcomes and adjustments, rota years and mark sheets for 2012 to 2026 on one schema: per board and series the centres sampled, the portfolios re-marked, the mean recorded difference and the adjustments applied (2021 to 2026: 1.47, 3.44, 2.60, 3.08, 5.26, 3.38 marks for the six joining boards, 4 to 33 per cent of sampled centres adjusted) | assembly-reconciliation | each board's sample marks, outcome records and mark sheets; the code of practice | exact on the cut pack | narrow look at broad data: the ten-minute pass reads the outcome records alone and never opens the sample marks, the trials or the mark sheets; the careful pass builds all of it | - | Step-by-Step |
| R2 | the share of a cold difference each board's moderators record: 36.4, 65.0, 48.6, 58.3, 70.9 and 64.0 per cent (Ardkeel, Brannock, Dunmoyle, Eskerry, Fennor, Gortavale) | missingness-measurement | each trial script's centre mark and cold consensus against the live moderator's mark of the same portfolio | Ardkeel 35.7 to 37.5 per cent | self-confirming check: the trial read as showing the moderators accurate, their severity added, the share left at 100 per cent | R1 | Component 1 |
| R3 | the level of a centre's marks by years since its last sample: Fennor's centres mark 3.19 marks lower one year after a sample and 1.59 lower two years after than in the sampled year (0.44 to 2.05 in the other boards) | modeling | the mark sheets by centre and year against the rota years, within centre and net of the board's year | Fennor, one year after: -3.23 to -2.98 marks | dismissed own evidence: the rota seen and the centre's last sample carried flat (0.0), or the year's sampled centres left to stand for the rest | R1 | Component 2 |
| R4 | each board's live standard against Carrow's: -0.39, -3.44, 1.75, -3.35, -3.91 and -6.52 marks | data-discovery | the moderators registered with two boards: their cold trial marks against each team's consensus; each board's agreed marks against its consensus; ten links adjusted to Carrow | Gortavale -6.58 to -6.50 marks | method shortcut: each board's own principal taken as the standard (0.0) | R1 | Component 3 |
| R5 | the regulator's 2023 review of Dunmoyle reproduced on the centres not sampled that year: 5.70 marks against the review's 5.54 | validation | the review's cold marks at Carrow's standard | the golden within 0.16 of the review; the four rival routes 1.20 to 3.38 away | self-confirming check: the route checked on the stability of each centre's successive samples, which are always at the same point of the cycle, the review left unread or read as Dunmoyle's own business | R2, R3, R4 | Step-by-Step |
| R6 | each board's banked marks against Carrow's standard by series: 2025: 3.03, 0.50, 6.09, 0.57, 1.32, -2.99; 2026: 2.93, 0.43, 6.36, 0.88, 1.07, -2.69; the two series together 2.98, 0.46, 6.22, 0.72, 1.20, -2.84 marks | synthesis | the protocol sections 2 to 4; R2, R3, R4 | per figure, the tables under `## Stump core` (Ardkeel together 2.80 to 3.13) | dismissed own evidence: the reflex route files 1.37, 3.05, 2.40, 2.59, 4.59, 2.47 together | R2, R3, R4 | Asks 1 to 18 |
| R7 | the boards the protocol converts and the conversion: Ardkeel down 3.0, Dunmoyle down 6.2, Gortavale up 2.8, the other three carried as banked; the joining boards together stand 1.66 marks above Carrow's standard | synthesis | the protocol section 4 on R6 | the call exact; together 1.54 to 1.81 marks | dismissed own evidence: the reflex route converts Brannock, Dunmoyle, Eskerry, Fennor and Gortavale down and leaves Ardkeel (2.80 together) | R6 | Recommendation, Ask 19 |

Carry-forward: every graded figure sits downstream of a stump, and all nineteen ask figures sit downstream of all three. Ardkeel's share in R2 falls with S1 alone and is S1's own figure; Fennor's level a year after a sample in R3 falls with S2 alone (it is read from the mark sheets and never touches the share or the standards) and is S2's own; Gortavale's standard in R4 falls with S3 alone and is S3's own. S1 lost alone, S2 lost alone and S3 lost alone each move all nineteen ask figures outside their bands; the reflex route lands none. The counts and bases every route reaches (centres, portfolios, candidates, the recorded differences and adjustments of R1) are stated in the Step-by-Step only.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a moderator's mark is drawn to the centre's: the recorded difference is 36 to 71 per cent of a cold one | constructed, the documented behaviour of second marking with sight of the first mark | no: all seven boards, every year, every moderator at their own strength | modelling: the trial scripts joined back to the live moderation of the same portfolio | modelling (a share per board, then every recorded difference divided by it before anything is carried) | keep |
| a centre tightens after a moderator's report and drifts until its next sample | constructed, the documented behaviour of centres between moderation visits | no: every centre of the six boards on a two or three year rota, at its own drift; absent only at Carrow, which samples every year | modelling: the mark sheets by years since the last sample, within centre and net of year | modelling (a level per board and year of the cycle, added to each centre's last sample) | keep |
| each board's team is standardised to its own principal and the standards differ | constructed, what separate boards with no shared standardisation do | no: all seven boards | a targeted query (registration numbers that recur in two boards), then modelling | modelling (person-level cold marks against two teams, each board's agreed marks, ten links adjusted over the network) | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the conformed moderation records and mark sheets | Missed | Right | Right |
| R2 the share of a cold difference recorded | Missed | Missed | Right |
| R3 the level by years since the last sample | Missed | Missed | Right |
| R4 each board's standard against Carrow's | Missed | Missed | Right |
| R5 the 2023 review reproduced | Missed | Missed | Right |
| R6 banked marks against Carrow's standard by board and series | Missed | Missed | Right |
| R7 the boards converted and the conversion | Missed | Missed | Right |
| Roughly | 0 of 7 | 1 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (written at the build); at the draw, generator/core.py on corelib.py (the rubric table of `## Stump core`)
Largest single hint: each board's moderators mark to their own principal's standard, and the boards' standards differ by several marks; rescues 1 of 7 results (R4, and only once the link is built; 21 rubric points with S3 fixed alone on the reflex route, Ardkeel still wrong and no ask figure inside its band)
Pair estimate: 9 (corelib's price of the reflex route, which is the careful but hurried pass: instruction-following and nothing else. A model, not a measurement: the platform's two runs are the measurement)

## Stump core

From `python3 task8/generator/core.py` (seed 8134; seven boards, fifteen series 2012 to 2026; the battery of 98 rebuilds), every figure as printed. Members are the six joining boards; a member's lines are 2 marks below and 2 marks above Carrow's standard.

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| Ardkeel | -2/2 | 2.981 | 0.127 | 1.374 | 1.462 | 1.103 | S1 |
| Brannock | -2/2 | 0.4644 | 0.433 | 3.054 | 3.495 | 2.538 | forced |
| Dunmoyle | -2/2 | 6.22 | 0.286 | 2.4 | 2.785 | 2.019 | forced |
| Eskerry | -2/2 | 0.7205 | 0.297 | 2.588 | 3.072 | 3.1 | forced |
| Fennor | -2/2 | 1.196 | 0.275 | 4.589 | 5.154 | 4.835 | S2 |
| Gortavale | -2/2 | -2.839 | 0.31 | 2.466 | 3.491 | 2.163 | S3 |

corelib writes `forced` for a member no stump names as its own; Brannock and Eskerry are open on the reflex route and are flipped by S3 alone (`## Open members`), and only Dunmoyle is forced.

| Figure | Block | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|
| C1 share recorded, Ardkeel | components | 36.37 | 35.67 to 37.46 | moves | - | - | lost |
| C2 year after a sample, Fennor | components | -3.186 | -3.228 to -2.977 | - | moves | - | lost |
| C3 standard against Carrow, Gortavale | components | -6.517 | -6.58 to -6.498 | - | - | moves | lost |
| A1 Ardkeel | asks | 2.981 | 2.8 to 3.125 | flips | moves | moves | lost |
| A1 Brannock | asks | 0.4644 | 0.2715 to 1.022 | moves | moves | flips | lost |
| A1 Dunmoyle | asks | 6.22 | 5.864 to 6.634 | moves | moves | moves | lost |
| A1 Eskerry | asks | 0.7205 | 0.3086 to 0.996 | moves | moves | flips | lost |
| A1 Fennor | asks | 1.196 | 0.8175 to 1.44 | moves | flips | flips | lost |
| A1 Gortavale | asks | -2.839 | -3.103 to -2.414 | moves | moves | flips | lost |
| A2 Ardkeel 2025 | asks | 3.033 | 2.84 to 3.158 | moves | moves | moves | lost |
| A2 Brannock 2025 | asks | 0.5012 | 0.2742 to 1.103 | moves | moves | moves | lost |
| A2 Dunmoyle 2025 | asks | 6.085 | 5.777 to 6.496 | moves | moves | moves | lost |
| A2 Eskerry 2025 | asks | 0.567 | 0.1801 to 0.8411 | moves | moves | moves | lost |
| A2 Fennor 2025 | asks | 1.324 | 0.9155 to 1.543 | moves | moves | moves | lost |
| A2 Gortavale 2025 | asks | -2.987 | -3.258 to -2.528 | moves | moves | moves | lost |
| A2 Ardkeel 2026 | asks | 2.928 | 2.74 to 3.111 | moves | moves | moves | lost |
| A2 Brannock 2026 | asks | 0.4269 | 0.2319 to 0.9824 | moves | moves | moves | lost |
| A2 Dunmoyle 2026 | asks | 6.355 | 5.9 to 6.783 | moves | moves | moves | lost |
| A2 Eskerry 2026 | asks | 0.8764 | 0.4274 to 1.156 | moves | moves | moves | lost |
| A2 Fennor 2026 | asks | 1.068 | 0.7072 to 1.395 | moves | moves | moves | lost |
| A2 Gortavale 2026 | asks | -2.692 | -2.952 to -2.29 | moves | moves | moves | lost |
| A3 six boards | asks | 1.661 | 1.537 to 1.808 | moves | moves | moves | lost |

| Route | Call | Earns on the rubric |
|---|---|---|
| golden | right | 100 |
| S1 lost alone | wrong | 22 |
| S2 lost alone | wrong | 22 |
| S3 lost alone | wrong | 22 |
| S1 fixed alone | wrong | 16 |
| S2 fixed alone | wrong | 18 |
| S3 fixed alone | wrong | 21 |
| reflex route (every stump lost) | wrong | 9 |
| rigorous standard route | wrong | 9 |

CORE PASS level 5  task8 architecture 20

The lattice in marks above Carrow's standard, the two series together (Ardkeel, Brannock, Dunmoyle, Eskerry, Fennor, Gortavale), and the call each route files (down, as banked, up): the world 3.09, 0.53, 5.81, 0.58, 1.03, -3.17 (down, as banked, down, as banked, as banked, up); golden 2.98, 0.46, 6.22, 0.72, 1.20, -2.84 (the same call); S1 lost 0.49, -1.40, 3.39, -1.48, -1.00, -4.74 (Ardkeel left as banked); S2 lost 3.47, 1.48, 6.98, 1.44, 2.87, -2.15 (Fennor converted down); S3 lost 3.38, 3.90, 4.47, 4.07, 5.11, 3.68 (all six down); S1 and S2 lost 0.98, -0.38, 4.15, -0.76, 0.68, -4.05 (Ardkeel left); S1 and S3 lost 0.88, 2.04, 1.64, 1.87, 2.91, 1.78 (Brannock and Fennor down, the other four left); S2 and S3 lost 3.87, 4.92, 5.23, 4.79, 6.78, 4.36 (all six down); all three lost 1.37, 3.05, 2.40, 2.59, 4.59, 2.47 (five down, Ardkeel left). The direct route files 1.46, 3.50, 2.79, 3.07, 5.15, 3.49 and the rigorous standard route 1.10, 2.54, 2.02, 3.10, 4.83, 2.16, each converting the same five boards down. The fitted inputs: share recorded 0.364, 0.650, 0.486, 0.583, 0.709, 0.640; standards -0.39, -3.44, 1.75, -3.35, -3.91, -6.52; cycle levels (years after a sample) Ardkeel -1.05, -0.44; Brannock -2.05, -1.14; Dunmoyle -1.54, -0.70; Eskerry -1.45; Fennor -3.19, -1.59; Gortavale -1.36. Sampled centres adjusted 2021 to 2026: 4, 16, 12, 24, 33 and 33 per cent, and 4 per cent at Carrow.

Unobserved part: how far each joining board's banked 2025 and 2026 portfolio marks stand from the standard in force at Carrow. No record holds it, in three parts: what a marker working cold would find in a centre a moderator sampled (the moderator records a fraction of it), where a centre's marking stands in the years it is not sampled (the moderation record holds nothing for them), and how far the board's own standard stands from Carrow's (no portfolio was marked by both).
Instruments: each board's moderation record sees every sampled centre in its rota year, as a moderator working from the centre's marked record recorded it, against that board's principal (read raw it files 1.46, 3.50, 2.79, 3.07, 5.15, 3.49, the direct route); the outcome records see which centres were adjusted and by how much; the mark sheets see every candidate's centre mark and awarded mark in every year and nothing about any standard; the standardisation trial sees 40 of the year before's sampled portfolios a year marked cold by the whole team and by the principal, and carries the reference that joins each back to its live moderation; the moderator register sees who marks for which board, 68 people for two; the regulator's 2023 review sees Dunmoyle's centres at Carrow's standard, cold, for one series.
Referee: the regulator's 2023 review of Dunmoyle, in which Carrow's senior moderators marked eight portfolios from every Dunmoyle centre cold at Carrow's standard. It covers neither another board nor the 2025 and 2026 series. Read on the centres Dunmoyle did not sample that year it gives 5.54 marks; the golden files 5.70 (off 0.16); S1 lost 3.13 (off 2.41), S2 lost 6.74 (off 1.20), S3 lost 3.95 (off 1.59), the rigorous standard route 2.16 (off 3.38). Read raw on every centre it gives 5.92 for Dunmoyle in 2023, which lies inside the band of each of Dunmoyle's three figures: a run that carries the review forward as Dunmoyle's answer lands them (about 8 rubric points). Dunmoyle is the forced member and the review is its own measurement three years earlier; the figures stay, because an ask for every board but one would name the referee. Read as a calibration set for the other boards (the share, the cycle and the standard measured on Dunmoyle and carried) it files a share of 0.49 where the boards run 0.36 to 0.71 and a standard of 1.75 where they run -6.52 to -0.39, and is wrong on every open member.
Strongest standard route: per open member, the most rigorous standard design the pack affords: each board's moderator severity taken from its own standardisation trial (the team's cold consensus against the agreed marks) and added to the recorded differences, candidate weights, the applied adjustments netted, the centres not sampled in the year carried at their own last sample shrunk to the board's mean. It files 1.10 (Ardkeel, left as banked), 2.54 (Brannock, down), 3.10 (Eskerry, down), 4.83 (Fennor, down), 2.16 (Gortavale, down), wrong on all five. It is refuted by the trial scripts joined to their live moderation (Ardkeel's moderators recorded 36 per cent of the cold difference on the same portfolios), by the mark sheets (Fennor's centres mark 3.2 lower the year after a sample) and by the review (2.16 against 5.54).
Said out loud: S1 "a moderator works from the centre's marked record, so the difference a sample records is only part of the difference a marker working cold would find": four steps left (find that the trial scripts are the year before's sampled portfolios; join each to its live moderation; fit the share board by board; divide every recorded difference before it is carried or netted). S2 "a centre is sampled once in its rota cycle, and the marks it banks in the other years are not given at the level its sampled year shows": four steps left (rebuild each centre's rota years; the level of its own marks by years since the sample, within centre; net of the board's year; add it to the centre's last sample at the corrected share). S3 "each board's moderators are standardised to their own principal, so a board's moderation measures its centres against its own standard and not Carrow's": four steps left (find the people registered with two boards; their cold trial marks against each team's consensus; each board's agreed marks against its consensus; the ten links adjusted over the network to Carrow).
Worth: S1 is worth 2.50 marks on Ardkeel, 19.7 times the family's spread of 0.127; S2 1.68 on Fennor, 6.1 times 0.275; S3 6.52 on Gortavale, 21.1 times 0.31 (the spread across the 98 rebuilds). Ardkeel's family runs 2.85 to 3.08 above the line at 2 and S1's drop lands at 0.49; Fennor's runs 0.92 to 1.37 under the line at 2 and S2's drop lands at 2.87; Gortavale's runs -3.03 to -2.53 below the line at -2 and S3's drop lands at 3.68.
Regimes: second stump on every member. S1's share is checked on twelve years of trial scripts in every board and on the review, and cannot be checked on the 2025 and 2026 samples themselves; it opens Ardkeel, whose moderators record the smallest share. S2's levels are checked on fifteen years of mark sheets and on the review's unsampled centres, and cannot be checked on a 2026 centre's standing against any standard; it opens Fennor, whose centres move most through the cycle. S3's standards are checked on ten links that close around the network and on the review, and cannot be checked on any portfolio; it opens Gortavale, whose standard stands furthest from Carrow's, and flips Brannock, Eskerry and Fennor as well. Dunmoyle is forced: every single drop keeps it converted down.
Sharp: S1: its wrong route passes the trial itself (the team's cold marks agree with the principal's to within a mark, so the moderators look accurate) and every arithmetic check on the samples; its right route commits to dividing a board's whole record by a share measured on 480 scripts; the evidence is in the trial file, which exists to standardise moderators and says nothing about centres; the correction runs from 0.36 to 0.71 across boards; its own figure is C1. S2: its wrong route passes a stability check on each centre's successive samples, which are always taken at the same point of the cycle; its right route commits to a level the moderation record never holds; the evidence is in the mark sheets, which a run reads for weights; the correction runs from 0.4 to 3.2 marks; its own figure is C2. S3: its wrong route passes every within-board check, because nothing inside a board's record can show its own standard; its right route commits to a link carried by 68 people; the evidence is in the register and the trial marks; the correction runs from -6.5 to 1.8 marks and changes sign across boards; its own figure is C3.
Earns: a run that loses only S1 earns 22, only S2 22, only S3 22 (50 or under each); the reflex route earns 9 and the rigorous standard route 9 (30 and 50 or under); S1 fixed alone earns 16, S2 fixed alone 18, S3 fixed alone 21 (each more than the reflex route and a third at most). The reflex route lands no graded figure. With the review carried forward as Dunmoyle's answer each of those routes earns about 8 more (30 with one stump lost, 17 on the reflex route).

Risks carried at the draw, for the build and the triage to read: (1) S3 is the judgment the question itself points at (a board's marks against another board's standard), so the strongest run will look for a link; what it has to find is that the link is people, in a register and a trial file, and that it runs through each board's agreed marks. A run that builds it and nothing else earns 21. (2) S1's instrument is a join of two files kept for different purposes; a run that joins everything joinable and plots the live mark against the cold consensus sees the share, and the build must not make that join the obvious one (the trial register carries the source portfolio's reference, not a column named for the moderation). (3) S2 is a response of the centres that the mark sheets carry; a group-by of mean mark on years since the last sample shows it once the rota years are rebuilt, so its difficulty is in thinking to ask, not in the fit. (4) The golden's own sampling error is about 0.3 marks a board (the world against the golden: 0.11, 0.07, 0.41, 0.14, 0.17, 0.33), wider than some bands; the bands are the battery's, the call holds in 13 of 16 seeds scanned at these dials (the other three fail on the referee's margin only), and the forcing rows hold at one spread in every combination with the nearest line 0.40 away. (5) C3's band is narrow (0.08 marks): the links are precise; the build widens the battery with the link's own conventions before the blocks are written. (6) Three of nineteen ask figures (Dunmoyle's) are open to the review read raw.

## Stump factorial

Reflex route: every board's files conformed to one schema; the later moderation record kept where one was resent; withdrawn and absent entries dropped; the applied adjustments netted; every centre weighted by its candidates with banked marks; each board's moderator severity (the team's cold consensus against the agreed marks, from the standardisation trial) added; a centre not sampled in the year carried at its own last recorded difference; the protocol applied as written. It files 1.37, 3.05, 2.40, 2.59, 4.59, 2.47 marks, converts Brannock, Dunmoyle, Eskerry, Fennor and Gortavale down and leaves Ardkeel, wrong on five of six boards, and is the careful but hurried pass.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 a moderator's recorded difference is a share of the cold difference, measured board by board on the trial scripts joined to their live moderation | stump | the recorded difference taken as the difference | L22, L28 | Ardkeel left as banked (0.49) where it is converted down; every ask figure outside its band | all six converted down (3.87, 4.92, 5.23, 4.79, 6.78, 4.36): four boards wrong; R2 rescued | no (four dependent steps) |
| S2 a centre's marks in the years between samples sit at the level its own mark sheets show for that year of the cycle | stump | the last sample carried flat | N13, L37 | Fennor converted down (2.87) where it is carried as banked; every ask figure outside its band | Brannock and Fennor down, Ardkeel, Dunmoyle and Gortavale left (0.88, 2.04, 1.64, 1.87, 2.91, 1.78): five boards wrong; R3 rescued | no (four dependent steps) |
| S3 each board's standard is placed against Carrow's through the moderators two boards share, each side taken to its own agreed marks | stump | each board's own principal taken as the standard | N27, L06 | all six converted down (3.38, 3.90, 4.47, 4.07, 5.11, 3.68): Gortavale down where it goes up, Brannock, Eskerry and Fennor down where they are carried | Ardkeel left as banked (0.98): one board wrong and every ask figure outside its band; R4 rescued | no (four dependent steps) |
| J4 seven layouts conformed, resent records, reissued candidate numbers, blank and absent entries, the older mark scheme | reflex | - | R01, R13 | same call | - | - |
| J5 every file read, the unused ones set aside | reflex | - | R02 | same call | - | - |
| J6 the applied adjustments netted and centres weighted by candidates | reflex | - | R18 | same call | - | - |
| J7 a severity for each board's moderators from its own trial, shrinkage of small samples, a stability check on successive samples | reflex | - | R31, R03, R16 | same call | - | - |

Level: 5: three necessary stumps, none sufficient alone, the three single drops on three distinct wrong calls and the lattice's seven shortcut routes on five.

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| Ardkeel | 2.98, converted down (0.98 above the line at 2) | 0.127 | wrong: 1.37, left as banked | wrong: 1.46, left as banked | S1 |
| Fennor | 1.20, carried as banked (0.80 under the line at 2) | 0.275 | wrong: 4.59, converted down | wrong: 5.15, converted down | S2 |
| Gortavale | -2.84, converted up (0.84 below the line at -2) | 0.31 | wrong: 2.47, converted down | wrong: 3.49, converted down | S3 |
| Brannock | 0.46, carried as banked (1.54 under the line at 2) | 0.433 | wrong: 3.05, converted down | wrong: 3.50, converted down | S3 (its drop alone files 3.90) |
| Eskerry | 0.72, carried as banked (1.28 under the line at 2) | 0.297 | wrong: 2.59, converted down | wrong: 3.07, converted down | S3 (its drop alone files 4.07) |
| Dunmoyle | 6.22, converted down (4.22 above the line at 2) | 0.286 | right: 2.40, converted down, at less than half the conversion | right: 2.79, converted down | forced |

Direct route: the pack's most direct evidence read at face value is each board's own moderation record: the mean recorded difference of the portfolios its moderators re-marked in the 2025 and 2026 series (`direct` in `generator/core.py`). It files 1.46, 3.50, 2.79, 3.07, 5.15, 3.49 and converts Brannock, Dunmoyle, Eskerry, Fennor and Gortavale down, wrong on all five open members: it is a fraction of the cold difference where the fraction is small (Ardkeel), it is taken at the top of the cycle where the cycle is large (Fennor), and it is against the board's own standard everywhere (Gortavale, Brannock, Eskerry).

## Data provenance

Source: generated by `task8/generator` from a simulated process: seven examining boards, each with 170 to 260 centres whose instructors mark every candidate's workshop portfolio out of 100; each board sampling a centre once in its rota (every year at Carrow, every two or three years elsewhere), a moderator re-marking 10 to 20 portfolios from the centre's marked record, the board confirming the centre's marks or moving them by the sample's mean difference where it passes the board's tolerance, and the moderator's report going back to the centre; each board's team standardised every year on 40 of the year before's sampled portfolios, marked cold before the meeting and settled by the principal's agreed marks; some moderators working for two boards.
Behaves like the real thing: moderation of centre-assessed work behaves in exactly this way: second marks given with sight of the first sit close to it, centres' marking drifts upward between visits and tightens after a critical report, and separate boards that never standardise together hold different standards. Every effect varies by unit (each moderator's own draw to the centre's mark, each centre's own drift and take-back, each person's own standard each season), nothing is a constant across rows and nothing changes level at a date.
Genuine patterns: (1) centres lenient on average, with a long tail of lenient centres and a few severe ones; (2) a sawtooth in each centre's marks over its rota cycle, larger where the board's moderators record more of the difference; (3) boards whose moderators record less of the difference adjusting fewer centres (4 per cent at Ardkeel against 33 at Fennor); (4) cohort size varying tenfold across centres, with small centres' means noisy; (5) a slow rise in every board's marks over the years, common to its centres; (6) moderators' cold marks scattered about their team's consensus by about two marks, each with a lean of their own.
Problems by process: seven layouts (each board's own system); resent moderation records (an appeal reopens the record); reissued candidate numbers (re-entry); blank trial marks (a script not reached before the meeting); the older 80-mark scheme in the earliest trial years (the scheme changed before the window any result reads); withdrawn and absent entries on the mark sheets. Each comes from the system that writes the file, and none moves a result.
License: none needed (generated).
Used as is: not applicable (generated).
Breadth: 30 or more files: seven boards' mark sheets (about a million candidate rows together), seven sample-mark files, seven outcome files, seven trial-mark files with their script registers, the moderator register, the centre registers, the regulator's 2023 review, the merger protocol, the code of practice, and unused files; 1,490 centres, 1,350 moderator appointments and fifteen series, so deciding which records bear on a board's distance from another board's standard is work.

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, modeling, data-discovery, validation, synthesis
Question form: which (which joining boards' banked marks are converted, in which direction and by how many marks)
Nearest build: the slot's own architecture 19 shares the subdomain, the analysis type and the answer shape (a reconciled table) and nothing else: it put three reading tests with different reference populations on one basis for a head count to a standard, and its chain ran assembly, measurement, measurement, measurement, a seasonal correction, synthesis; here one mark scheme runs throughout, no instrument changes, and the chain is the share a moderator records, the cycle, the standards link and a referee. task5 (the last ETL build) assembles a population account from twice-reported flows; nothing here is reported twice and no account closes. task19 shares the reconciled table and corrects a register with dependent capture channels; nothing here is captured or matched. precut's nearest chains (task13, task19, task22) share the reconciled table and neither the weight nor the chain: task13 sits on attribution (a fault record across relay exports), task19 on a hard-to-measure quantity, task22 on triage (a gas balance on one basis); none has a share, a cycle or a link between standards, and ETL's native answer is a conformed table.

## Frontier check

Precedents: R2 careful Missed on L22 (a published formula whose generating assumption the data contradict: the code's own definition of a sample difference, which assumes an independent second mark) and L28 (the estimator certified with checks that cannot see the problem: the trial's agreement between team and principal); R3 Missed on N13 (the latest observed rate taken as the state at the decision date: the last sample carried) and L37 (a pooled factor certified by a held-out error that cannot see the condition: successive samples always at the same point of the cycle); R4 Missed on N27 (a second record at another grain set aside because it lacks the unit's identities: the trial marks, which name no centre) and L06 (one correction made and the second declined: the board's own severity added, the board's standard left alone); R5, R6 and R7 fall with R2, R3 and R4 (L28, N13, N27).
Shallow path checks: the recorded differences reproduce every outcome record exactly by the code of practice; the trial shows each team within a mark of its principal; each centre's successive samples agree with one another (they sit at the same point of the cycle); a shrunken carry of the last sample back-tests well on the next sample for the same reason. What refutes them is of another kind: the trial scripts joined to the live moderation of the same portfolio (a file at another grain, script against sample), the mark sheets by years since the sample (a file at another window, every year against the rota year), the two-board moderators' cold marks (a file at another population, people against centres) and the regulator's review (a file at another standard).
Assumption made false: the moderator's mark is an independent second reading (false: the moderator works from the centre's marked record; tested by the trial scripts, where the same portfolios were also marked cold); a centre's marking holds between samples (false: it tightens after a report and drifts; tested by its own mark sheets); the boards share a standard, or each board's principal is the standard (false: separate teams, separate principals; tested by the people who mark for two boards and by the review).
Forcing: the lines are 2 marks below and above Carrow's standard. Across the 98 rebuilds of the battery the nearest approach to a line is Gortavale at -2.53 (0.53 from -2), then Fennor at 1.37 and Ardkeel at 2.85; every variant files the golden's call, and the world's own values sit on the same sides. The shortcuts land across the lines: S1 lost Ardkeel 0.49 (1.51 under 2), S2 lost Fennor 2.87 (0.87 over 2), S3 lost Gortavale 3.68 (5.68 above -2); the reflex, direct and rigorous routes are wrong on every open member. Each fitted input (the share recorded, the cycle levels, the standards) moved one measured spread up and down for every board at once (the furthest any rebuild moves it: 2.0 to 6.5 per cent on the share, 0.08 to 0.21 marks on a cycle level, 0.04 to 0.14 marks on a standard), and all three together in each of the eight combinations, files the same call; the nearest row is Gortavale at 0.40 from its line with the share down and the other two up.
Noun swap: nearest on file by `skeleton.py check`: severity none against every card, the client's corpus and the slot's lineage. task19 shares one detection and one move (a second source at another grain, a recorded figure divided by a measured rate) and task20 the three detections; swapping either's nouns in (a register's district counts, an endowment's fund programs) carries no lesson, no mechanism and no decision form across.
Closed strategies: the call turns on three lessons, none on the client's closed page: anchored_second_reading, state_reset_at_inspection and local_standards_linked_by_shared_raters. Nearest closed cards and how each differs. "Two sources that are not independent (capture-recapture)" has one list feeding another so that an overlap is inflated, fixed by removing the dependent records; here nothing is counted or matched, the second mark is a measurement drawn to the first, the quantity is a difference shrunk by a share, and the fix is to measure the share on scripts also marked cold and divide. "Outcomes are hidden by the intervention itself" has flagged units rescued so that their outcome is the intervention's, fixed from units the intervention could not reach; here every centre is on the rota and none is unreached, the adjusted marks are netted as the protocol files them (a reflex), and what is estimated is a centre's own level in its other years from its own marks. "Seasons fall in different places (fieldwork timing)" has groups observed in different seasons of a profile that exists apart from the survey, fixed by a month profile within fixed units from the same record; here the profile is made by the moderation itself, the moderation record holds one point of it for every centre and so cannot give it, and it comes from a second record. "The instrument changed (drift or step change)" corrects one series across a break in time; here nothing changes in time, seven standards run side by side with no item in common, and the fix is a network link through common raters. "A noisy explanatory variable flattens the slope" is kept as a supporting step only: the share fitted with the consensus' own error allowed for is a member of the family (`pull_how` deming), moves no figure outside its band and leaves the call standing. Supporting steps from the closed page that a route applies alone: shrinkage of small samples, inside the rigorous standard route, which files the wrong call.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a banked mark | the mark as awarded by the board after moderation (the centre's mark less any adjustment); the centre's own mark | as awarded | the protocol section 2 |
| SF2 | the banked series | every portfolio mark awarded in the 2025 and 2026 series; only those of candidates still on roll | every mark of the two series | the protocol section 2 (a three-year course: no 2025 or 2026 portfolio mark has yet been used in an award) |
| SF3 | Carrow's standard | its principal moderator's agreed marks as applied in its 2026 moderation; its team's cold consensus; its centres' own marks | the agreed marks | the protocol section 3 |
| SF4 | a board's distance | the mean over candidates; the mean over centres | over candidates | the protocol section 4 |
| SF5 | the test | on the two series together; on each series | together | the protocol section 4; each series alone files the same side for every board (same call) |
| SF6 | 2.0 marks or more | the unrounded distance against 2.0; the distance rounded to a whole mark | unrounded | the protocol section 4; no variant comes within 0.5 of a line (same call) |
| SF7 | the conversion | the distance itself, to one decimal; a whole number of marks | the distance | the protocol section 4; the blocks state each distance with its band |
| SF8 | a sample's difference | the centre's mark less the moderator's, the mean over the sampled portfolios; the moderator's less the centre's | centre less moderator | the code of practice, the outcome record's own sign |
| SF9 | an adjustment | applied to every candidate of the centre in the series, in whole marks; to the sampled candidates only | every candidate | the code of practice; the mark sheets show it |
| SF10 | which moderation record | the later where a record was resent after an appeal; the first | the later | the code of practice (a resent record replaces the earlier) |
| SF11 | the years the share is fitted on | every trial year on file; the last five; year by year and averaged | every year | same call: each is a member of the family |
| SF12 | the form of the share | a slope with an intercept; through the origin; with the consensus' own error allowed for | with an intercept | same call: each is a member of the family |
| SF13 | the cycle level | the board's mean level by years since the sample; each centre's own change in mean mark since its sample, net of the year; the two averaged | the board's mean level | same call: each is a member of the family |
| SF14 | the years the cycle is fitted on | the last nine series; six; twelve; weighted by candidates or not | nine, unweighted | same call: each is a member of the family |
| SF15 | the last sample | the centre's latest sample; its last two averaged | the latest | same call: a member of the family |
| SF16 | how the links are pooled | the mean of each pair's differences, weighted by its people; the median; trimmed; unweighted; the six shortest paths only | the weighted mean over all ten | same call: each is a member of the family |
| SF17 | a board's agreed marks against its consensus | the mean over its trial scripts; the median | the mean | same call: a member of the family |
| SF18 | the review | a check on the estimate, read on the centres not sampled that year; Dunmoyle's own answer; a calibration set for every board | a check | the review covers one board and the 2023 series; as Dunmoyle's answer it lands inside Dunmoyle's bands (stated under Referee); as a calibration set it is refused by every other board's own share and standard |
| SF20 | the joining boards as a whole | the mean over every candidate with a banked mark at any joining board; the mean of the six boards' distances | over candidates | the protocol section 5 |
| SF19 | stated precision | distances to 0.1 mark, shares to 0.1 per cent, each with its band | as listed | the answer blocks state each figure's band; the prompt dictates no rounding |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| the tolerance of the protocol | 2.0 marks either way | the merger protocol (.pdf), section 4 |
| the banked series | 2025 and 2026 | the merger protocol (.pdf), section 2; the prompt |
| each board's rota length and tolerance | one to three years; 3 to 6 marks | the code of practice (.pdf), schedule; the rota years themselves are in the moderation record |
| the share of a cold difference recorded | 0.364, 0.650, 0.486, 0.583, 0.709, 0.640 | measured: the trial scripts' centre mark and cold consensus against the live moderator's mark of the same portfolio; measured spread 2.0 to 6.5 per cent across the battery |
| the cycle levels | -0.44 to -3.19 marks | measured: the mark sheets by years since the centre's last sample, within centre, net of the board's year; measured spread 0.08 to 0.21 marks |
| each board's standard against Carrow's | -0.39, -3.44, 1.75, -3.35, -3.91, -6.52 marks | measured: the two-board moderators' cold trial marks against each team's consensus and each board's agreed marks against its consensus; measured spread 0.04 to 0.14 marks |
| the consensus' own error (one variant only) | the spread of a team's cold marks over the number marking | measured from the trial marks; the core's stand-in is its dial for a moderator's error, which the build replaces with the measured spread |
| the referee | 5.54 marks, Dunmoyle 2023, centres not sampled that year | the regulator's review marks (.csv) |

Variant battery: 98 variants of the golden route in `generator/core.py` (`VARIANTS`): the share through the origin, on the last five trial years, with the consensus' own error allowed for, fitted year by year; cycle levels weighted by candidates, on six and on twelve series, each centre's own change, the two averaged; the last two samples averaged; links trimmed, at the median, unweighted, along the six shortest paths; agreed marks at the median; and every two of these that change different choices. Every variant files the same call and every graded figure of every variant sits inside its stated band. The golden uses no constant only the core knows: the world's dials (each board's draw, drift, take-back and standard) never enter `estimate`, `pulls`, `phase_effects` or `offsets`, which read the recorded arrays alone.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: every workshop portfolio mark awarded by a joining board in the 2025 and 2026 series; withdrawn and absent entries carry no mark and are out |
| 2 | Unit of account: marks out of 100, the mean over candidates |
| 3 | Attribution window: a mark belongs to the series it was awarded in |
| 4 | As-of dating: the records as extracted on 8 February 2027, every 2026 series closed |
| 5 | Version basis: the later moderation record where one was resent; the protocol and the code of practice as in force for the 2027 awards |
| 6 | Denominator: candidates with a banked mark in the board and series |
| 7 | Weighting: centres weigh by their candidates with banked marks; the two series weigh by their candidates |
| 8 | Window length: the share on every trial year on file; cycle levels on the last nine series; links on every year the two-board moderators marked both trials |
| 9 | Boundary inclusivity: a distance of exactly 2.0 marks is converted; none arises |
| 10 | Rounding path: full precision to the end; distances stated to 0.1 mark, each with its band |
| 11 | Tie-break: none needed; no variant comes within 0.5 of a line |
| 12 | Maturity and censoring: every series in the record is closed and moderated; appeals on the 2026 series closed in November 2026 |
| 13 | Order of operations: the conformed records, the share, the cycle levels, the standards, the review, each centre's distance, each board's by series and together, the call |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: a resent moderation record replaces the earlier; a reissued candidate number is one candidate per series |
| 16 | Identity normalisation: centre numbers in one scheme by the centre registers; moderators by their national registration number |
| 17 | Netting against gross: an applied adjustment is netted from the centre's marks before the distance is read |
| 18 | Dimensional units: marks; shares as fractions of a difference; marks on the older 80-mark scheme rescaled by the code's schedule, in years no result reads |
| 19 | Code and status semantics: outcome codes (confirmed, adjusted), entry status (marked, withdrawn, absent), appointment type |
| 20 | Integerisation: adjustments are whole marks as recorded; nothing else is rounded before the call |
| 21 | Clause scope: the tolerance applies to each board separately, the two series together |
| 22 | Forward window contents: none forecast; the banked marks are fixed and the standard is the one in force in 2026 |

## Literal reader

The protocol's section 4 executed word for word on the golden's six distances files the golden: 2.98 is 2.0 or more above, converted down; 0.46 carried as banked; 6.22 converted down; 0.72 and 1.20 carried; -2.84 is 2.0 or more below, converted up. The code of practice executed word for word reproduces every outcome record from its sample marks (the sample's mean difference, the board's tolerance, a whole-mark adjustment for every candidate) and nothing of R2 to R7. No shipped sentence, executed literally, produces a share, a cycle level, a standard or a distance from Carrow's standard.

## Prompt contract

A rewrite keeps: the question in the which form (which joining boards' banked portfolio marks are converted before the June 2027 awards, which way and how far); the reason the answer rests on an estimate (nobody has marked the banked portfolios to the standard in force at Carrow); the figures for every joining board by their plain definition and unit (how far its banked marks from the 2025 and 2026 series stand above or below that standard, in marks, for the 2025 and 2026 series taken together and for each series) and for the joining boards as a whole; the deliverables by type (a spreadsheet with the estimates, the boards converted and a chart; a CSV with one row per centre and series). A rewrite never adds: how moderators mark or what they see, the rota, the trial, people who work for two boards, the regulator's review, a method, a comparison, a correction, a check, a file name, a count of boards, centres or files, who is asking, a rounding rule or a warning.

## Build brief

World: Carrow Awards, a not-for-profit awards body in Ireland, takes over six regional examining boards (Ardkeel, Brannock, Dunmoyle, Eskerry, Fennor, Gortavale) from the June 2027 awards of the three-year Senior Trades Certificate, whose first-year workshop portfolio is marked out of 100 by the centre's instructors and banked until the award. The engine is `generator/core.py`'s `simulate()`: for each board its centres (`nc`), rota group (`grp`), each centre's leniency against its board's live standard year by year (`lam`), the sample's recorded mean difference (`G`), sample size (`ns`), adjustment (`adj`), candidates (`ncand`) and mean centre mark (`mbar`); the trial scripts (`ex_x`, `ex_y`, `ex_gap`, `ex_year`); the two-board moderators' cold marks against each team (`D`); the regulator's review (`review`). The build lays records over those arrays and changes none of them: each centre-year becomes candidate rows whose mean is `mbar` and sample rows whose mean difference is `G` to the precision the golden reads, each trial script becomes a row per moderator whose consensus, agreed mark and live moderation mark reproduce `ex_x`, `ex_y` and `ex_gap`, each two-board moderator's marks reproduce `ra` and `rb`, which `checks.py` asserts for every array the golden reads.
Frozen: SEED 8134; the seven boards and every dial of `BOARDS`; `DUAL`, `DUAL_YEARS`, the error dials, `NEX`, `EX_YEARS`; the series 2012 to 2026 and the banked series; the line (2.0); the referee (Dunmoyle, 2023, eight portfolios a centre, read on the centres not sampled); the golden's route (`estimate`, `pulls`, `phase_effects`, `offsets`), the three hurried choices (`LOST`), the direct and rigorous routes, the battery (`VARIANTS`) and the forcing (`spreads`, `--forcing`); the three components (Ardkeel's share recorded, Fennor's level a year after a sample, Gortavale's standard against Carrow's) and the asks (each board's distance for the two series together and for each series, the joining boards together); no portfolio marked by two boards except the review's; no centre that changes board.
Files: (1) each board's portfolio mark sheets 2012 to 2026, one row per candidate and series in the board's own layout (centre number, candidate number, series, entry status, centre mark, awarded mark), seven files, the largest of 150,000 rows or more: the 20,000-row CSV and the long printed one are among them. (2) Each board's moderation sample marks, one row per sampled portfolio (series, centre, candidate, centre mark, moderator mark, moderator registration number), two boards holding a sample's marks in a delimited field. (3) Each board's moderation outcomes, one row per centre and series sampled (portfolios sampled, mean difference, outcome, adjustment applied, date of the report), with resent records. (4) Each board's standardisation trial marks, one row per script and moderator (series, script, registration number, mark given before the meeting), with blanks and the older scheme in the earliest years. (5) Each board's trial script register (script, the series and reference of the portfolio it is a copy of, the principal's agreed mark). (6) The national moderator register (registration number, name, board, series of appointment), one row per appointment, a person with two boards on two rows. (7) The centre registers (centre number in the board's and the national scheme, name, county, year approved). (8) The regulator's 2023 review of Dunmoyle: one row per portfolio (centre, candidate, centre mark, review mark) and a one-page scope letter (which centres, how many portfolios, who marked, to which standard), no findings. (9) The merger protocol (two to three pages, the house PDF writer): sections 1 to 6 as under Estimand, section 5 giving the joining boards as a whole over every candidate with a banked mark. (10) The code of practice for centre-assessed work (three to four pages): sample sizes by entry, each board's rota length and tolerance, the form of an adjustment, the moderator's report, standardisation (trial scripts are clean copies of the previous series' sampled portfolios, marked before the meeting; the principal's agreed marks settle the standard). (11) to (13) three unused files that look relevant, never named as unused: enquiries about results by board and series (requests for re-moderation and their outcome, all closed with no change after the appeal records already in the outcome files), centre approval visits (workshop facilities and safety, nothing on marking), candidate entries by trade and age band. Two or more file categories (spreadsheets, text), the pack at 30 MB or more.
Never filed: a sentence that a moderator's mark is influenced by, drawn to, anchored on or close to the centre's mark, or that seeing the centre's marks matters; that moderation differences are understated, compressed or conservative; any ratio, share or slope between a moderated and a cold mark; that the trial measures anything about live moderation; that centres mark more leniently or severely at any point of the rota, or drift, or respond to a report; a comparison of sampled and unsampled centres or years; that the boards' standards differ, any board's standard against another's, cross-board comparability findings, the review's results or conclusion; that two-board moderators link anything; a column, sheet or file named for any of these (no `blind`, `seen`, `anchor`, `cycle`, `phase`, `years_since`, `dual`, `link`, `offset`); any document that describes the data files.
Goldens: `carrow_banked_marks_by_centre_2025_2026.csv`: one row per centre and series, the board, the candidates with banked marks, whether the centre was sampled that series, and its estimated distance from Carrow's standard in marks. `carrow_banked_marks_conversion_2027.xlsx`: the first sheet states the boards converted, the direction and the conversion, the boards carried as banked and what the estimate rejects, with one chart of the six distances against the two lines; behind it the distances by board and series, the share recorded by board, the cycle levels, the standards link (the ten pairs and the adjusted standards), the 2023 review check, the sensitivity of each board's side to each fitted input, and a routes sheet showing what each shortcut files. Every figure from `figures.json`; both through the house writers.
Free: nouns beyond the people and the invented names; the document genre and wording inside the Never filed list; Layer 1 texture and its rates (every item resolving exactly); the split of each centre-year into candidate rows and of each sample into portfolio rows; each board's layout; the unused files' contents; file names and formats; trades, counties and centre names.

## Architecture 19 record (spent 2026-11-18)

Hollinbrook Academies Trust's Year 7 entry reading on one basis (South Yorkshire and the East Midlands;
education-learning-sciences, item-response-theory-test-equating, ETL, etl_conformance): 21 academies on three entry
reading tests (Lexis, Quill restandardised on a 2024 sample, Brightway on paper), a fixed-order trial at the
Brightway academies and July transition-day sittings at four Lexis academies, conformed to the Lexis basis to count
the students below 85 and set Reading Forward's tutor time; the golden funded 874 places (GBP 349,880) against a
provisional GBP 339,500. Built to READY on 2026-11-11 (seed 818025), the judge DETERMINISTIC and the reader clean,
never uploaded. Spent on 2026-11-18 without runs: it turned on two judgments (the trial's order and the July
sittings), so one judgment found earned 37 to 51 and both earned everything; it was cut before the core, the open
members and the rubric rules (no generator/core.py, no Stump factorial, no Pinning list); its chain's lessons sit on
or beside the client's closed page of 2026-11-12 (the instrument changed, a co-occurring change, seasons fall in
different places); its graded figures were head counts the careful pass rebuilds; and its heart blocked on the
calibration form and the forum against later builds.


## Architecture 18 record (spent 2026-11-11)

The Prairie Adult Credentials Board's 2027 Level 1 Numeracy pass mark (Winnipeg; education-learning-sciences,
item-response-theory-test-equating, ETL, decomposition_attribution): the 2027 paper borrowed twelve long mathematical
Level 2 items, and the bank's concurrent calibration put the expected mark at the standard at 21.57 (a pass mark of
22); a model of each borrowed item's shift for Level 1 candidates with both causes the bank records (an everyday
advantage and a reading cost with stem length) and the scale constant fitted together filed 19. Built to READY on
2026-11-08 (seed 818025), two cold leak reads clean, never uploaded. Spent on 2026-11-11 without runs: one pass mark
carried by one decomposition is the single-deep-step design the 2026-11-09 review returned in kind, and the author
asked for a build that meets the new bar.

## Architecture 17 record (spent 2026-11-08)

The Corlinn Schools Assessment Trust's choice among three draft Year 10 science papers for the November 2027 sitting
(education-learning-sciences, item-response-theory-test-equating, composition_mix): the bank's Term 3 items had been
calibrated at the August 2026 sitting, when about nine in ten of their responses came before the candidate's own school
had finished the unit, and recalibrated on the taught responses they put Paper C nearest 25 at the Achieved standard
(A 25.89, B 23.02, C 24.80) against the bank's Paper A (24.78, 20.64, 21.58). The asks were each region's entries,
sittings, make-up sittings and mean make-up mark. Shipped 2026-11-08 (judge DETERMINISTIC, APPROVE on round 2, target.zip
02c4e9b7). On the platform's first round both runs filed Paper C and every regional figure: run 1 fitted a joint
conditional Rasch model with a coverage contrast for each Term 3 unit, run 2 kept the Term 3 responses after each school
finished the unit; the prompt's August-against-November gap announced the mechanism, the course outline and Appendix
B's per-school sequences handed over the join, taught-content adjustment is a textbook IRT reflex, and each ask device
was a hygiene item both runs caught. The full record is in `pipeline.json` (`lineage_v17`) and `runs/triage.md`; its
stage-4 reports are kept as `determinism_check_report_arch17.md` and `leak_check_report_arch17.md`.

## Architecture 16 record (spent 2026-11-07)

Brackwell Alloys' 2026 product-family direct emissions for Velden's 2027 low-carbon premium (physical-environmental-
sciences, emissions-inventory, decomposition_attribution): the homogenizing furnace's gas allocated by its loads' firing
hours, not their tonnes, put 6082 billet at 0.263 over SCR-2's 0.235 and the premium at EUR 342,000 against the
per-tonne route's EUR 456,000. Shipped 2026-10-31 (judge DETERMINISTIC, APPROVE; target.zip 433ff500), reshipped
twice on 2026-11-07 for PDF provenance, and returned FAILED_TO_STUMP the same day: both portal responses filed EUR
342,000 on the firing-hours allocation, the method a careful analyst reaches for, which the hourly gas fitted at
R-squared 0.9985; the portal also flagged Domains Fit. The full record is in `pipeline.json` (`lineage_v16`).

## Architecture 15 record (spent 2026-10-31)

Architecture 15 priced Pembrook Castings' 2027 employee dental maximum under its Finance Policy F-17: each maximum's
cost per covered person month on the 2025 plan year at the 2027 fees, against Board Resolution 2026-31's 1.90 dollars.
The golden added back the predetermined work members at the 1,500 dollar maximum put off to the January reset, which
put 3,000 dollars over the limit and filed 2,000. The stage 4 judge returned NOT_DETERMINISTIC with SEND_BACK and the
reconciliation confirmed a withheld rule: F-17 executed word for word on the 2025 claims gives 0.83 and 1.23 dollars
and files 3,000, and no shipped text adds the put-off work; the asks left the put-off column's total, the deductible on
34 lines, "still in treatment" and an orphan case open. Its world (a manufacturer's self-insured dental plan) is left
with it, and its report is kept as `determinism_check_report_arch15.md`.

## Architecture 14 record (spent 2026-10-31)

Architecture 14 elected the Larrowbrook Physician Network's 2027 two-sided track practices: each practice's 2026
network measure carried from the October interim run by its own 2025 run-out at the same cut, plus the members in
hospital stays still running on 31 August, which the hospitals bill at discharge and the feeds show only as the
physicians' daily charges, each past the 250,000 dollar member cap (Mallowcrest Pediatrics' neonatal triplets,
Garrowdale Family Practice's trauma family). It shipped 2026-10-25 (zip 2c0f8d35, judged APPROVE on 04486b1a) with
eight practices entering. The repair's judge pass 2 returned FIX_NOW: two graded thresholds a cent off, the 2025
measures within a third of a cent of a rounding edge. The re-judge found the write-up's claim that all seven stay
members were past the cap by 31 August false under a pooled per-day reading (4,535.53 dollars a day against the
per-kind 6,380), the call's margins thin and the stay amount unfiled: a FIX_NOW that failed its second pass, which
spends the architecture. Its world (a clinically integrated network's risk track) is left with it.

## Architecture 13 record (spent 2026-10-25)

Architecture 13 elected the Larrowbrook Physician Network's 2027 two-sided track practices: each practice's 2026
network measure on the payers' final 2026 attribution, projected from the October interim run by the practice's own
2025 run-out at the same cut, against the default path that takes the interim measure as the 2026 figure (Ostrelwood,
Thornelfield and Jesselford alone, against the golden nine). At stage 4 round 1 (zip ab79a5f44c18f637) both scored
readers landed the call (exit 1): each read the prompt's "projected to the payers' final 2026 attribution" beside the
standard's attribution rules as a population the October run cannot hold, re-ran the October 2025 interim run on the
2025 claims with the standard's own rules and the Appendix C factors, and carried each practice's interim measure by
its own 2025 final-to-interim ratio. Reader A kept all 78 ask figures (Kesselcrest's reviewed 99215 visits at the
99214 rate out of level 5, Merrinlake's halved modifier-25 visits counted by their code, Pemberglen's coverage month
from its payment reference, Kesselcrest's Medicare Advantage lines at 6.50 out); reader B kept every benchmark,
threshold and ask B figure and no ask A figure. The judge thread was stopped at the spend. Asked to project an interim
figure to a final one, a careful reader takes last year's interim-to-final ratio, the field's completion reflex, and a
standard whose rules can be re-run on last year's claims hands it that ratio in one pass.

## Architecture 12 record (spent 2026-10-24)

Architecture 12 certified the Quillmere Lake basin's 2027 Seasonal Communities Aid: each city's average population
present in its busiest month of the measurement year read from its plant's influent BOD load divided by the load per
person its own January to April 2026 fix, against the default path that counts residents plus the paid stays the fee
returns and both platforms record (Sorrelton and Esker Narrows alone, USD 1,200,000 each, against the golden's five
cities at USD 480,000 each). At stage 4 round 1 (zip be45d7b75ea5cc24) both scored readers landed the call (exit 1):
each read the Act's "every other person staying in or visiting the city" as a population no record holds, went to the
one file that measures everyone (the plants' influent), divided the load by 0.17 lb a person a day (the population
equivalent the world had been tuned to agree with), checked it against the residents in winter and filed the five
cities; both also counted Kettle & Pine's nights back from the departure in its reference (reader A all 32 of ask A,
reader B 26 of 32 on half-dollar rounding) and missed only the pond systems' flow basis in ask B. The judge thread was
stopped at the spend. A statute that defines the population as everyone present, beside records that plainly hold
only the paid stays, sends a careful reader looking for a measure of everyone, and a pack whose influent rows have
no other use hands it one.

## Architecture 11 record (spent 2026-10-24)

Architecture 11 settled Lumenfold Learning's 2025-26 outcomes guarantee district by district, each partner district's
share of eligible students at or above Proficient on a matrix-sampled spring science assessment re-estimated from its
students' own two-module answers with the district in the population model, against the default path that averages
the contractor's five plausible values by district (19 districts owed USD 32,045.00 against the golden's 16 owed
USD 25,493.75). At stage 4 round 1 both scored readers missed the call, reader A kept all of ask A through the
catalog's hours per session, and the judge's pass 1 returned FIX_NOW on a cent tie in the credits (seat prices moved to
whole half dollars). In round 2 reader C refitted the 2PL latent regression from the item responses with district in
the conditioning model, validated it on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75 and
kept every ask figure: a conditioning model that leaves out the grouping variable is a reflex for a reader who knows
plausible values, so the architecture was spent.

## Architecture 10 record (spent 2026-10-24)

Architecture 10 accrued each Medicare hospice provider number's FY2026 aggregate cap repayment at the December 2026
close, each beneficiary counted under the proportional method on the days to come from their state at the close (an
open stay by its length so far, a live discharge by its time out, returns read at every hospice from the benefit
periods extract), against the default path that runs the open stays on and takes the live discharges as finished
(Fallowmere USD 0.3 million against nothing). At stage 4 all four isolated readers across two rounds missed the call
and the round 1 judge returned DETERMINISTIC, APPROVE; the round 2 judge returned NOT_DETERMINISTIC, SEND_BACK
(margin_or_boundary_fragility and competing_defensible_answer): the printed 0.3 needed Fallowmere's count inside a
window of 2.9 beneficiaries while independent builds of the projection scattered about a beneficiary either way, and
the pool start, the number of later elections and the Kaplan-Meier tail were left unfiled (0.248 to 0.447 on the
judge's variants); ask A's routine-paid days read as an unstated rule. A designation set would have held (every variant
put Fallowmere above its cap); a figure printed to USD 0.1 million on a three-beneficiary window did not.

## Architecture 9 record (spent 2026-10-23)

Architecture 9 read each station's Schedule C availability from the bikes in working order docked, each bike's spells
rebuilt from the trips and fleet moves and a bike counted out of working order from the end of the ride that left it
when renters passed it over and a van then took it to the depot for a day or more, against the status feed's available
count (W-02, W-12, W-16 and W-19 against W-16 alone). At stage 4 (zip 14ceb178) both scored readers missed the call:
reader A subtracted the reported bikes and the bikes mechanics took in without a report, inside the inspection windows
(W-16 and W-19); reader B subtracted the reported bikes only (W-16). Both kept nearly every ask figure (65 and 64 of 74,
exit 1): the sales export's present-location column undone through the work orders' terminal replacements, and the
alarms ended at restarts once the clear pairing ran to hundreds of hours with sales inside them. The isolated judge
thread returned NOT_DETERMINISTIC, SEND_BACK, competing_defensible_answer (Gates B, C and E): no shipped file says that
unreported broken bikes exist or how to find them, so the records read literally (the feed, or the rebuild with the
reported bikes out) file W-16 alone, and the depot-stay cut and the pass test sit only in the solution's steps (at 36
and 48 hours W-17 and W-19 move by a point); Gate G `planted_defect_flip`, `surface_read_rejection`,
`surface_read_dependency: yes`, `sole_data_defect: yes`; Gate H `decisive_step: planted`.

## Architecture 8 record (spent 2026-10-23)

Architecture 8 carried each store's data logger record through the vaccine's thermal lag, a first-order response
fitted per logger make on the two weeks each pilot store's old logger kept recording beside its new in-carton sensor
(42.2, 42.2 and 41.9 minutes), against the loggers' readings taken as the vaccine's temperature (six stores against
ten). At stage 4 (zip ad958ec9) reader B set the pilot stores' loggers beside their in-carton sensors over the overlap
unprompted, fitted the lag as a first-order filter (0.21 of the gap closed per ten minutes, about 42 minutes) and
landed the six stores and every store's whole hours, answering question 6 "an analytical choice" on standard 7.2; it
kept every ask figure too (122 of 122 graded figures, exit 1): the counts' own closing times, the credits found when
per-item balances went negative, the vial write-offs by cost over the per-dose cost, the tax switch by the
maintenance-only invoices at Schedule B's prices, and the two-store routes split by Schedule B. Reader A and the judge
thread were stopped at the spend.

## Architecture 7 record (spent 2026-10-23)

Architecture 7 read each production day's oxidizer outlet from the relation the ten oxidizers' tests trace (a floor of
about 45 ppmv as carbon, 1.8 per cent of the inlet above about 2,500) at the inlet the day's captured VOC and airflow
imply, against each plant's latest test efficiency (Ashcombe 21 and Kelvedon 20 against 29 and 28). At stage 4 (zip
5ab18e48) reader A read the floor straight off the test tables (Ashcombe's 2018 two-press test holds the same 45 ppmv
at half the inlet), rebuilt each hour's outlet as the greater of the floor and 1.8 per cent of the inlet and landed the
five and all 14 whole tons, Part 2 question 1 "none" and question 6 "an analytical choice"; reader B carried each
fixed-fan unit's test outlet to the year through the register's fan-drive column (R4, six plants). Both readers kept
all 28 ask figures: the revision log read, the payment lines parsed, Haldane matched on description. The judge thread
was stopped at the spend.

## Architecture 6 record (spent 2026-10-22)

Architecture 6 set Form 27A's placement scores from the bank difficulties carried from the old platform's field-test
section (positions 61 to 70) to the positions 21 to 70 the unique items take on Northgate Assess, by the position term
the 2026 attempts measure, against the default path's difficulties as filed (29 and 18 against 30 and 19). At stage 4
reader A rebuilt every response at its delivered position, fitted the Rasch model with the anchor block fixed, found
items harder later in the test on both platforms and landed 30 and 19 exactly (29.48 and 18.50), Part 2 question 1
"none" and question 6 "an analytical choice"; it kept 13 of 62 ask figures (the system totals and some twice counts).
Reader B and the judge thread were stopped at the spend.

## Architecture 5 record (spent 2026-10-22)

Architecture 5 designated rapid price growth areas on each dwelling type's own year effect weighted by the census
stock's value, with a pooled hedonic year term as the default path. At stage 4 both readers and the judge's own
derivation took the type-by-stock aggregation by reflex (type medians or type year effects weighted by the census
stock) and missed the call only on the location control (electoral division), which the judge read as unfiled; filing
it hands all three the call, so the decisive step as designed does not stump and the one that held is a fork.


## Tried and rejected
- Architecture 6, item position effects in pre-equating (2026-10-22, spent at stage 4): reader A fitted a Rasch model
  with a position term to the rebuilt attempts and carried the field-test difficulties to Form 27A's positions,
  unprompted by any sentence. The calibration context has to be recoverable for the truth to be fair (the report's
  delivery section and both exports' positions), and once it is, an analyst who knows the field checks the effect the
  context invites; a context effect measured by an obvious model term is a reflex for the field's own analysts.
- Architecture 6 draw (2026-10-22): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened
  before it and dead: a CEMS gap fill on load (guard BLOCK on pattern G12 and strategy population_selection against
  task273, same-puzzle and same-driver spent in five to seven builds, the statutory filing against task249);
  multiplicative against additive seasonality (task146, task147); a moving holiday (task162, task467, task135);
  Denton benchmarking (this slot, below); retroactive eligibility as a denominator still developing (the completion
  driver of task451 and task479 v5); Fellegi-Sunter frequency weights (set aside at task486's draw against task468's
  linker error); the oldest old by extinct generations (task228); non-detects under several limits (task189).
- Architecture 5, the stock's price change as each dwelling type's own year effect weighted by the census stock's
  value (2026-10-22, spent at stage 4): both readers and the judge's first derivation weighted dwelling types by the
  census stock by reflex (the note's "dwellings the 2022 census counts" and the census workbook by type invite it) and
  missed only on the electoral-division control, which the judge read as unfiled (r5a); filing it hands them the call.
  A stock aggregation over a tabulated type mix is a reflex once the stock is the filed population.
- Architecture 5 draw (2026-10-22): re-rooted on the author's standing rule (no retirement); the world and pack of architecture 4 kept, the decisive step moved from the constant-quality regression its reader 9 found to the aggregation that regression skips (each type's own year effect over the stock's value), with the pooled regression now the default path. At registration the v4 identity BLOCKed on own_lineage, gap population on same-puzzle and same-driver (task251 v5), shape 10 and the statutory filing (task249 v6) and filed_standard (task478 v4); redrawn as recorded in the Draw, the circular changed to settle the 2027 fund allocations.
- Ask B's reissued student ids as a 7-digit id equal to the old one plus a campus constant, linked by birth date, sex and ZIP (2026-10-21, stage 4 round 1): both readers resolved it on the person columns and kept all six headcounts (score_reader 50 per cent); re-sited so the new ids share the old form with no arithmetic tie, birth date, sex and ZIP are shared by different students, and the movers' majors are recoded, so only the four-field key resolves it.
- Architecture 1, a coordinating board's instructional grant with four parents' consolidated returns apportioned by a cost model (2026-10-21, spent at stage 4): round 1's two readers split by FTE or total credit hours and missed; both round 2 readers fitted instruction expense on credit hours by level across the standalone campuses, split each parent's return by the modelled cost and landed the call (exit 1). Pricing activity by level from the units that report alone is a strong reader's reflex once the activity file by level ships beside the combined return.
- Architecture 2, regional register error rates from an audit drawn unequally by a risk screen (2026-10-21, spent at stage 4): both readers checked the audit's composition against the register (35 per cent referred against 8), weighted each stratum to the 30 April register and landed the call; both also read the UTC times into local time and dropped the restored companies (asks 28 of 28). A sample whose composition differs from its frame on a shipped flag is reweighted by a strong reader; a stated clock and a restoration notice are seen devices.
- Architecture 3, registration offices put on a timeliness plan from a quarter's median working days with part of the quarter still open at the extract (2026-10-21, spent at stage 4): both readers censored the open applications at their age, took the Kaplan-Meier median and landed the call, and dated payments by the batch terminal day (asks 28 of 28). An open caseload shipped beside a duration cohort, with a paper saying the open ones count, is read as right-censored by a strong reader; a settlement batch file carrying the terminal day is a seen device.
- Architecture 4, areas' house price change for the rapid price growth designation read from a shifting sample of the stock (2026-10-21, spent at stage 4): reader 9 fitted log price on type, floor area, age, newness and the address point file's electoral division with a year term and landed the call; reader 10 left location out and missed; the block purchases' one consideration on every line held both readers (0 ask totals of 32). A constant-quality index is a strong reader's reflex once the note cites the handbook and the attributes ship; location one join away is not a hidden dimension.
- A district's register error rise tested with the spread of the audit's sampled blocks (2026-10-21, screened at the draw): the guard put it beside task261 (subgroup statistics from one clustered sample, their difference's error from the clusters), the same driver.
- Regional quarterly output benchmarked to annual totals by Denton against pro-rata (2026-10-21, screened): Denton's extrapolation holds the end-of-year ratio, which sits within a few tenths of a point of pro-rata's annual ratio, while a trending ratio puts the truth far from both; the separation is too small and the truth not recoverable without forecasting the ratio.
- Architecture 7 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: gross labour-force flows corrected for reinterview misclassification (task244's
  driver); speededness on a timed form (task249's screen); a winner's curse in form assembly (task471's shrinkage
  coin flip); generic price erosion by entrant count (task484 v1's ramp, screened at task478's draw); percent-of-charges
  hospital contracts carried to each hospital's current chargemaster (the swap test reads it as any list-price
  contract); laboratory results harmonised by proficiency-test bias (the reported result is the measurement, so the
  correction is a fork); a cancer registry's completeness by the flow method (task249's screen); common-stack
  apportionment from single-unit hours (task263's unmixing); a concentration-discharge load (task452 v1, task135);
  change of support for block grades (task270, task254, task273 screens); linkage on an address the outcome changes
  (task468's linker error); calculator-type DIF and released-item drift on the item bank (architecture 6's lesson: a
  context an obvious model term measures).
- v7 stage 3, 2026-10-23: the first tuning let each oxidizer's test outlet carried to the year (its concentration on
  each day's air, or its rate over the year's hours) file the golden five, because a fixed-fan plant at the floor emits
  the same rate every day; Larkmoor Graphics was made a concentrated-test, mostly-dilute plant under 25 tons so those
  routes file six (R4, R4m, R4b).
- v7 stage 3, 2026-10-23: press VOC to one decimal: the standing family spreads up to 0.37 tons on a plant, so the
  figure is graded in whole tons, every member 0.19 tons or more from a half (G4); the CSV's used and captured
  columns went with it (free to both top responses), the CSV now the press VOC and coverage.
- v7 stage 3, 2026-10-23: the tuned plants landed on whole tons (29.00, 37.00); moved to ordinary offsets (G5). Days
  below the tests' lowest inlet at three plants opened an extrapolation fork (interpolated efficiency against the
  floor); the low days were raised inside the tested range.
- Architecture 7, 2026-10-23: spent at stage 4. The decisive relation was visible inside one oxidizer's own tests (the
  same outlet at two inlets) and in the register's fan-drive column, and a regenerative oxidizer's outlet floor is
  field knowledge both readers carried; the asks' devices each sat one file away from a careful reader's path (the
  master's revision log in the same workbook, the washer gallons in readable payment text, descriptions beside the
  renumbered items). Next architecture: a decisive step no table displays as a pattern and no column labels.
- Architecture 8 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world, aimed
  at architecture 7's lesson (no table displays the decisive relation, no column labels it). Screened before it and
  dead: vessel propulsion from AIS speed over ground carried to speed through the water by an estuary's tidal streams
  (a port world beside task472 and task474, and a tidal stream table has no other use in an emissions pack, so its
  presence announces the correction); container ships' at-berth auxiliary load by the reefers on board, calibrated on
  shore power meters (a port world, and a reader calibrating on the meters sees the per-call spread with reefers its
  first explanation); a tanker's boiler load at berth by its own steam cargo pumps on discharge (the at-berth tanker
  rules' own reasoning, a reflex once the transfer log is joined); dairy lagoon methane through the lagoon's
  temperature lag behind the air (the rate model is a filed procedure, and four inspection readings a year cannot fix
  the lag deterministically); switcher locomotives' idling through the start-stop system's restart temperature (a
  rate carried across a weather covariate, task478 v7's driver); crematory mercury by the decedents' dental cohort (a
  composition mix one survey table hands over); breaker SF6 leak rates from temperature-uncompensated pressures (the
  gas temperature at each reading is not recoverable). A cold-chain prototype (thirty-six refrigerators, probe 6 minutes,
  carton 48) put the logger's own hours at two to ten times the vaccine's, the default qualifying 29 against 12, with
  a 45-minute lag fitted on ten fourteen-day overlaps at 0.04 degrees C reproducing the carton's set exactly, while 30
  and 60 minute duration filters (17 and 6) and a 45-minute moving average (20) fell elsewhere and a 90-minute moving
  average missed by one refrigerator: the stage 2 world keeps the default's count plausible and every store clear of the
  line under the standing family.
- v8 stage 3, 2026-10-23: standard 7.1 first read "the records of each store's device of record are its vaccine
  temperature records", which a literal reader takes as the logger's readings being the vaccine's temperature (an
  official decoy for the default path); it became a records-custody clause.
- v8 stage 3, 2026-10-23: under the interval-mean reading of a record's vaccine temperature five stores' whole hours
  moved by one while the call held; 7.3 now files the counting (a record counts its ten minutes by the vaccine's
  temperature at its time stamp), WHAT and not HOW (SF17).
- v8 stage 3, 2026-10-23: return credits from both manufacturers put the cracker's balance below zero at eleven
  stores, a loud failure that points at the double count; only Halvorsen's standard-dose products are returnable, the
  leftovers leaner and the unrecorded losses scaled to each store's volume (cracker 15 doses or more, A6).
- v8 stage 3, 2026-10-23: maintenance-only invoices at one price per unit type tied ten stores' service figures (a
  constant response would have kept them); per-model prices and add-on parts at some visits, every store's figure now
  distinct (B5). With the tax switch as ask B's only silent device a reader who found it kept 23 to 30 of 30; the
  pre-move two-store maintenance routes on one invoice were added, so the tax switch alone keeps 10.
- v8 stage 3, 2026-10-23: the first names sat on real organisations, products or places in or near the field (H21):
  Coldline (a refrigeration manufacturer), Polarwatch (an ocean-data programme), Vaxtor, Homeline, Arctis, Glacier
  Medical, and the acquired chains Rookwood Drug and Saltash Apothecary; renamed Tellvane, Brumal, Stellane, Keswell,
  Brannon, Pendry Medical, Vollmer Drug and Lindqvist Apothecary before any reader saw the pack.
- Architecture 8, 2026-10-23: spent at stage 4. Two instruments recording one unit side by side are compared by a
  strong reader on reflex: the pilot stores' logger and in-carton series parted at every restock and defrost swing, so
  reader B fitted a first-order lag on the overlap with no sentence asking for it. Every ask device had one natural
  check that exposed it (per-item balances, cost per unit, a list price met exactly, one invoice on two sites).
  Next architecture: a decisive step whose evidence no single side-by-side comparison shows, and ask devices that no
  per-item reconciliation or unit-price check reveals.
- Architecture 9 draw (2026-10-23): re-rooted on the author's standing rule (no retirement) with a fresh world. Screened before it and set aside: phantom shelf inventory under a vendor-managed availability guarantee (on-shelf availability is an industry term that names its own correction); a plan directory's ghost providers read from claims (the directory and the claims sit side by side, architecture 8's reflex); a starting dose as the mark of a true initiator in an outcomes contract (population_selection, in the window against task275); rectifying inspection's over-weighted rejected lots (population_selection again); left truncation of a fleet's lifetimes (task133's delayed entry for a taken-over book); GPS chord distance by terrain for fuel-tax jurisdiction miles (the call would sit on a few per cent of one state's miles); meter error read off a system balance (the instrument-bias family task478 v5 and task480 v1 lost to readers); charger uptime from failed sessions (the failure is written in the session record itself). The bike-share draw keeps the listed count correct for what the operator knew and puts the difference in renters' choices, which no record states.
- v9 stage 2, 2026-10-23: the fleet's clock ran four hours off Eastern time after the move to absolute instants (its
  local minute of the day counted from midnight UTC), so the pack showed the morning rush at noon; the window's start was
  re-anchored to 20:00 on 23 September so the fleet's own clock is Eastern time, the trajectory byte for byte the same
  (46,883 trips), the station move and the dock expansions read at 23:00, and Schedule C's minutes taken from Eastern
  time itself; the designations held (W-16 alone against W-02, W-12, W-16, W-19).
- v9 stage 2, 2026-10-23: each station's three months to one decimal put nine of 72 cells within two minutes of a
  printed edge and W-12's lowest month (87.652) within a minute; graded at each station's lowest month in whole per cent
  instead (the tightest ten minutes clear, M1), the margin to one decimal (0.684, eleven minutes), the monthly figures
  kept in the workbook as context.
- v9 stage 2, 2026-10-23: ask B's hours to one decimal put W-18 within a second of an edge; graded in whole hours, each
  pay station's alarm stream chosen so its figure sits 0.08 hours or more inside its bin (M3).
- v9 stage 2, 2026-10-23: the union of overlapping alarms as ask B's device: at whole hours the summed and merged
  spans print alike at every station; kept as texture (B3), the restarts carrying the device.
- v9 stage 2, 2026-10-23: with only the alarms and restarts in the log, ending an open alarm at the pay station's next
  event of any kind kept 15 of 24 hours figures (the restart was nearly always the next event), an honest pair of 45.7;
  the cabinet heater's events on cold days and the service door at reader repairs added, the shortcut keeps 4 (33.1).
- v9 stage 2, 2026-10-23: invented names screened by web search (Wellhaven, Northlane Mobility, Corlund Kiosk
  Systems): no organisation, product or place on any of them in or near the field; Welland, Ontario is three edits away.
- Architecture 9, 2026-10-23: spent at stage 4 on the judge's SEND_BACK. A count the operator's system publishes as
  available, read against a state no record holds (a bike's working order inferred from what renters and the vans did
  with it), is a surface read rejected however the evidence is gathered: on clean data the feed would be right, so the
  judge files Gate G surface_read_rejection and Gate H planted, and with nothing filed saying unreported faults exist
  the records read literally give the feed's answer (competing_defensible_answer). The readers missed the call for the
  same reason the judge refused it. Both ask devices were found: a column filled from a present-day register is undone
  by a work-order log that lists every swap, and a pairing that runs alarms to hundreds of hours with sales inside them
  announces its own repair. Next architecture: a quantity every file visibly lacks (so no surface read stands in for it),
  estimated by a method the data forces, and ask devices whose wrong reading is plausible rather than absurd and whose
  evidence no log lists outright.
- Architecture 10 draw (2026-10-23), no card filed. The guard's window closes survey research for ETL (ban.pairing and
  ban.subdomain against task483, so census-register and seasonal adjustment are both out) and the strategies grain_or_unit,
  population_selection and composition_mix (task483, task275, task179); payment claims, emissions, IRT equating and data
  integration clear it. Screened on those four and dead on file or on measurement: competing exits against censoring
  (task169, task266; the competing exit is a reflex, task133); pooled-test infection rates (task188); age-length keys
  (post-stratification, a reflex once the aged subsample's design ships); a pooled tail share from parts' means and spreads
  (task483's lesson); a population's share past a cut from short matrix-sampled booklets (task464's shrinkage lesson);
  direct against indirect adjustment of a net series (task453 v2's fork); time-series consistency by splicing (task123's
  screen); chance agreement on name and birth date in a voter roll (task468's common-identifier lesson); credibility for
  site emission factors (the regulatory standard takes the site's own tests, a fork); tracer flux ratios (the integrated
  ratio is the method's own definition, so the default is the golden); flows traced through intermediaries to end markets
  (task451 v1's swap failure); uncompensated gas meters (a unit read, data semantics); correlated systematic errors in an
  activity-data uncertainty (the call is a monitoring decision, Data Quality); cohort waits from cumulative counts under
  first-in-first-out (generic queueing, the swap reads the same); a pick log matched to put-aways by each lane's access
  order (drive-in lanes are last-in-first-out, field knowledge a strong reader carries, architecture 7's death).
- Architecture 10 draw (2026-10-24): drawn on the hospice cap after a second screen of the four open ETL task types (survey research still closed by task483). Screened and dead: TRI range codes valued at the exact filings inside each range (the midpoint is the programme's own convention, a competing defensible answer, and the exact filings are one group-by away); charge compression in cost-plus repricing (the implant invoices put the cost-to-charge ratio against the charge in plain view, and the functional form forks); a stopped turbine's nacelle anemometer read through the running transfer function (readers impute from neighbours by habit, and Gate G reads an instrument bias as planted); unconstrained demand on sell-out days (the product-limit estimator is a reflex and converges with the intraday route); time-of-observation bias in daily maxima (the calendar-day maximum is not recoverable from a 5 p.m. reset and the nearest hourly station); trend uncertainty with shared emission factors (propagating through the difference carries the shared factor by construction, so the easy route is right); items dropped from scoring rescored through the test characteristic curve (the published conversion table replays the method); best-of-k seed reports deflated by each recipe's seed spread (the client's GSDS Layer 1 list names best seed against mean as harmonisation); inverter clipping, demand ratchets and dead-time counting losses (each leaves a flat top or a ceiling in the records that announces its correction); unit value against a fixed-basket price index for provider unit cost (composition_mix, banned against task179 for this registration); DIF purification, testing-window instruction time and single-group order effects in equating (field reflexes, or no bias in the equating); register status nowcast by a Markov chain (forecasting, and architecture 9's surface-read refusal); interpolation along a process curve between sparse readings (task478 v6's and task480's degradation and life-cycle families). The first card draft BLOCKed on test.same_puzzle against task171 v4 with G13 decisive; G12 is the honest decisive generator for the step that decides.
- v10 stage 2, 2026-10-24: a lifetime projection with Brackwater, Lindmoor and Wexmoor owing beside Fallowmere: the
  standing family (Aalen-Johansen or empirical return chances, three valuations of a return, the open stays' later
  returns overall or from their time so far) moves each core program's cap by USD 30,000 to 70,000 against cells of
  USD 100,000, and the overall-rate route kept three of the four amounts; the core programs were placed under the cap
  and Fallowmere carries the call alone (nothing accrued on the default path, USD 0.3 million on the golden).
- v10 stage 2, 2026-10-24: pooled models across provider numbers and a split by discharge reason each moved
  Fallowmere's count by up to 1.3 per cent on cells of small programs; the policy files the reference class (the same
  provider number and diagnosis group), and Fallowmere's seller's system records no revocation against discharge
  reason, so the reason split is not available for its history.
- v10 stage 2, 2026-10-24: with return stays as long as first stays the overall rate times the census average landed
  the golden's cell (0.325 against 0.300); re-elections run shorter (the beneficiary comes back in decline) and seldom
  end alive again, so that route files 0.53 and the census-average valuation by time out 0.19.
- v10 stage 2, 2026-10-24: the outside share of Fallowmere's returns was raised from a third to four in five, so the
  route that reads returns from Elderglen's own records files nothing (cap ratio 0.971) instead of landing beside the
  golden.
- v10 stage 3, 2026-10-24: the organisation and program names Elderglen, Brackwater, Corrinbrook, Dunsmere, Lindmoor,
  Pennacott, Sallowfield and Wexmoor sat within two edits of real places in the GeoNames register (Eden Glen,
  Blackwater, Swallowfield and Fallowfield, Dunmore and Dinsmore, Wyndmoor, Dixmoor) or carried a place word (Penna,
  and Cornbrook in Manchester two edits from Corrinbrook); renamed Wendleglen, Brindlemoor, Corvelfield, Darrelbrook,
  Marrellford, Rennickdale, Varrowmere and Farrinridge in the generator, every figure unchanged. The lines above keep the
  names they were written with.
- v10 stage 4 round 1, 2026-10-24: both scored readers missed the call (each ran the open stays on and took the
  live discharges as finished, nothing accrued) and the judge returned DETERMINISTIC, APPROVE (Gate G analytical, Gate H
  pass); reader A joined the claim lines to the remittance register and kept all 24 ask A figures (exit 1), so the
  device that the latest version is not the paid one sat off the careful path. Re-sited: the contractor's prepayment
  review pays some held inpatient days at the routine rate, visible only by repricing the paid version, with the
  returned replacements kept as a hazard and moved more than 118 days before the close (reader B had priced them as
  pending, cutting payments); the census report's length-of-stay table, blank on a group key mismatch, now prints.
- v10 stage 4 round 2, 2026-10-24, architecture spent: both fresh scored readers again missed the call (open stays
  run on, live discharges finished, nothing accrued) and kept 0 of 24 ask figures, but the judge thread returned
  NOT_DETERMINISTIC, SEND_BACK (margin_or_boundary_fragility, competing_defensible_answer): Fallowmere's printed 0.3
  needs its count inside 177.6 to 180.5, a window of 2.9 beneficiaries (USD 0.1 million at the cap amount and 98 per
  cent), while independent builds of the same projection scatter about a beneficiary either way (0.248 to 0.311 on the
  judge's variants, 0.279 to 0.314 on the standing family), and it named four choices the policy leaves open (the
  Kaplan-Meier tail, one later election or several, stays begun before 1 October 2016, the last provider number when the
  open stay is at another hospice); it also read ask A's routine-paid days as an unstated counting rule. Lesson: a cap
  repayment printed to USD 0.1 million moves a cell every 2.9 beneficiaries of count, so a projection whose honest
  spread is a beneficiary cannot print one cell; the next architecture's call has to be a quantity whose cell is wider
  than its estimator family's spread, measured on independent builds rather than on the author's own family.
- 2026-10-24, architecture 11 draw, screened on paper before any code against v10's lesson (a call whose cell is wider
  than its estimators' measured spread): Medicare Advantage post-payment recoupments or denial overturns for a
  hospital's 2027 contract notices carry v10's latent structure (a terminal-looking state that is not final) and
  task451's (amounts still to arrive).
- Architecture 11 draw: Medicaid procedural reinstatements and COBRA retroactive elections: retroactive eligibility was
  screened at task451 and task479 v5, and COBRA's selection is population_selection, banned against task275.
- Architecture 11 draw: ACA risk adjustment transfers estimated from competitors' public prior-year transfers: carrying
  a competitor's risk forward is a fork; ACA grace-period cures: rule-heavy, with the cure rate carried across the 2026
  subsidy expiry.
- Architecture 11 draw: censored transplant costs by inverse probability of censoring weights: mature cohorts are
  unbiased without a trend, and a trend makes the stump a dated step; authorization- or ADT-based claims reserves: the
  completion family, and a leading indicator is a reflex.
- Architecture 11 draw: price-standardised total cost of care tiers: the standardisation is a WHAT (filed is rule
  application, unfiled a fork); deductible leveraging is task479 v3's driver; prescription abandonment by out-of-pocket
  cost: the lever is too small; stop-loss and high-cost claimant pooling: non-linear aggregation at claimant level and
  level-dependent counts are closed.
- Architecture 11 draw: hospital coding intensity after an EHR conversion, separated by the same patients' successive
  admissions: adjacent to task453 (a measurement change read from a within-design contrast that nets a drift), the event
  study is the reflex and the WHAT signposts the method.
- Architecture 11 draw: low-voltage anode effect PFCs at aluminium potlines: task459's driver (a ratio with a fixed
  component carried across activity levels), and the IPCC slope method files it; wastewater digester relief-valve
  venting: v9's Gate G risk (an unmetered event inferred from indirect evidence); idle and shut-in wells: a setting clone
  of task462 and task450 v1; stack test-day tune-ups: population_selection and a surface read.
- Architecture 11 draw: a landfill's pre-record waste read from the volume survey: the gas collection record calibrates
  the decay model and absorbs the missing waste; refinery turnaround cycles: a schedule in a file is read; fuel switched
  during gas curtailments: a degree-day normalisation is the reflex.
- Architecture 11 draw: Fellegi-Sunter term-frequency weights: adjacent to task468 (false links on common
  identifiers); address agreement decaying with the gap between records: adjacent to task468 v1.
- Architecture 11 draw: majority-drifted or released anchors (v6, task450); rater severity drift on a shared
  constructed-response subset (task471 v2's driver); rapid guessing in a low-stakes sitting (task479 v4, sent back as
  cleaning contaminated data); speededness and not-reached items (an anchor-drift screen catches them).
- Architecture 11 draw: queue position for open appeals or a coding backlog against timely filing limits: the waiting
  time is a generic queue quantity, so the swap test fails and the domain is a backdrop; censored demand behind
  capacity is task18, task108 and task168; capture-recapture is task199, task243, task248 and task448.
- Architecture 11 draw: newborns and deliveries predicted from current pregnancies in an employer group's renewal: the
  base projection's credibility and trend choices fork, in a large group last year's deliveries already carry the
  component, and the honest strategy (who is in the 2027 population) is population_selection, banned against task275.
- Architecture 11 draw: race and ethnicity imputed from surname and geography for group counts: summing the
  probabilities is the reflex for counts, and the weighting-against-regression choice for rates needs a gold-standard
  subsample, banned against task275.
- Architecture 11 draw: the payroll survey's birth-death model against the lagged QCEW census is reserved for task484
  v2, and drawing it here through a house domain would game the survey x ETL ban against task483.
- Architecture 11 draw, first world: plausible values aggregated by school for a county school system's coaching list
  reskins task450's world and call (a district's own assessment naming the campuses below a share for coaching), so the
  mechanism moved to a company's guarantee settlement with its partner districts.
- Architecture 11 placement, benchmarks by prior tercile (12 to 20 for the lowest, up to 30 for the highest): no
  district the plausible values pull down could cross a benchmark it met, since the strong-implementation districts
  with weak backgrounds sit in the lowest tercile, so benchmarks became whole numbers from 12 to 35 per order form.
- Architecture 11 placement, a 5.5-point margin to the family's envelope with 2.5 points of crossing for every route:
  no maximum likelihood or curve-inversion count crossed anywhere, the routes' upward bias peaking near 9 points; the
  shipped margin is 4 points to the whole family's envelope with 1.5 to 3 points of crossing by route.
- Architecture 11 asks, a series' total on each row with series of up to 12 hours: the hours column summed put most
  districts at two to three times their contract, which reads as wrong at a glance; the series were cut to 3 and 4
  hours and the summer institute booked by day.
- Architecture 11 ask A, the offering's catalog hours on every session row (a series' total on each of its sessions):
  round 1's reader A set the series rows beside the catalog's hours per session and replaced them, keeping all 58 hours
  and 18 credits (exit 1); the catalog every reader opens for the live and recorded formats holds the tell one lookup
  away. Re-sited onto the session times the scheduler holds as hours and minutes after the point, every offering
  scheduled in whole hours so only the sessions that ran short or long carry minutes.
- Architecture 11, credits on quarter-dollar seat prices: a 15 per cent credit on a fee of 11,537.50 is 1,730.625, so the
  cent had a tie that no file breaks (judge pass 1, FIX_NOW); seat prices moved to whole half dollars, every credit a
  whole cent, the call's set unchanged.
Architecture 11 (the contractor's plausible values drawn from a conditioning model with no district term, each district re-estimated with the district in the model), spent at stage 4 round 2 on zip ce5456c3: reader C refitted the 2PL latent regression from the item responses with district in the conditioning model, validated its fit on the contractor's Table 6, filed the golden 16 districts and USD 25,493.75, and kept every ask figure (58 of 58 hours, 20 of 20 shortfall credits, 36 of 36 memo rows) by reading the hours field as hours and minutes from its fractions. A conditioning model that omits the grouping variable is a reflex for a reader who knows plausible values, so the round-3 PD re-site (series credit hours stacked on h.mm) is moot and the slot re-roots.
- 2026-10-24, architecture 12 draw: a Lunar New Year factory shutdown reaching a US East Coast port's container imports
  a Pacific or Cape crossing later, for its calendar-adjusted series: the decisive step is a lag and a window, the
  enumerable single choice the client's measured coin flips share, the effect is famous in trade data, and a port world
  would be this lane's third (task472, task474). Not drawn.
- 2026-10-24, architecture 12 draw: a state's payroll survey estimates early-benchmarked to the lagged unemployment
  insurance census where the birth-death model ran ahead in a slowdown: the two series count the same jobs side by side
  (architecture 8's reflex), the step is a choice between two files, and rejecting the published estimate for the census
  reads as a surface-read rejection at Gate G. Not drawn.
- 2026-10-24, architecture 12 draw: revisions measured from real-time vintages, or rebuilt pseudo-real-time by
  re-adjusting truncated spans: the client's pin makes the triangle rule application once the vintages ship, and the
  truncated re-adjustment forks between X-11 and STL end filters. A seasonal break from a school calendar moved to
  August: the post-break span is a window and the regime regressors are a reflex. Not drawn.
- 2026-10-24, architecture 12 draw: chain drift in a scanner-data price index (economics x ETL is undrawable, and the
  formula is one enumerable switch); suppressed county-industry cells rebuilt from their margins (identification is the
  step, so one linear solve is the easy route landing); custom-area margins of error from replicate tables against the
  approximation (the handbook licenses both, a fork at Gate C); register over-coverage by signs of life (every activity
  window is a threshold read as a fork). Not drawn.
- 2026-10-24, architecture 12 draw: the lake towns' population present also read from their transfer stations' scale
  tickets or their water meters: solid waste is collected on schedules that lag the stays, and summer water use carries
  the irrigation of empty cottages, so neither measures the people present as the sewer does; kept out of the pack.
- 2026-10-24, architecture 12 stage 4: the population present read through the plants' influent load per person,
  calibrated on the winter months; both round 1 readers landed the call at the 0.17 lb population equivalent (exit 1),
  because the Act's definition made the paid-stay records visibly incomplete and the influent rows had no other use in
  the pack. Spent.
- Architecture 13 draw (2026-10-24): re-rooted on the author's standing rule (no retirement) with a fresh world.
  Screened before it and dead: Medicaid exposure developed through retroactive enrollment (task474 v4's capitation
  world, task451 and task479 v5's completion, and the recent months' dip shows on any monthly tabulation); linkage
  sensitivity by identifier stratum for linked mortality (a pooled clerical correction lands the stratified set on
  paper, and stratifying by the identifier is a reflex); three measurement systems combined by triple collocation
  (task228, landed); regression against equating in a score crosswalk (task464); payday counts by weekday schedule
  (task477); data fusion through a small joint source (task465); a prospective capitation priced on experience chosen
  the same way a period earlier (task130's lineage); business deaths confirmed after two years without reactivation
  (the standard's definition makes the adjustment a reflex); out-of-state births to residents arriving through the
  vital records exchange (a completion the place-of-occurrence field shows).
- 2026-10-24, architecture 13 stage 2: the October run's short counts read as members still to come who cost nothing
  (the interim measure scaled by the run's members over the 2025 final run's, or by the member months) filed the golden
  set with the practices as first placed, so a reader who saw the counts and assumed the rest landed the call without
  the 2025 re-run. Birrelhaven, the paediatric clinic whose late members cost nearly what its others cost (run-out
  0.944 on a 22 per cent short count), was placed 5.5 per cent over its threshold, where the zero-cost reading takes it
  12.8 per cent under.
- 2026-10-24, architecture 13 stage 2: asks with one device each (the code on the claim for ask A, Pemberglen's
  posting period for ask B) handed a whole ask to any response that found its device; each ask now carries a second,
  independent silent device (Merrinlake's halved modifier-25 visits; Kesselcrest's Medicare Advantage lines on the same
  remittances), and the best single-device handling keeps 6 of 52 figures.
- 2026-10-24, architecture 13 stage 2: the projected 2026 figure graded to the cent was dropped from the prompt's
  columns: the licensed constructions agree on every election but not on the cents (per payer against per practice
  moves a projection by up to 0.6 per cent), so the workbook carries the projection as context and the rubric grades
  the benchmarks, thresholds and elections.
- 2026-10-25, architecture 13 (each practice's interim measure carried to the payers' final attribution by its own
  2025 run-out at the same cut), spent at stage 4: both scored readers re-ran the October 2025 interim run from the
  2025 claims and landed the call, reader A with all 78 ask figures; a projection from an interim run to a final one
  whose prior-year ratio the standard's own rules rebuild is the completion reflex, and the second ask devices (the
  halved modifier-25 visits, the Medicare Advantage lines at another rate) fell to a reader who checked only the payer
  whose rates looked wrong and the one fee that did not match the standard.
- 2026-10-25, architecture 14 draw: the member cap read as what the run-out truncates (a member whose year to date
  already sits at the cap carries fixed dollars while the year's months grow): in architecture 13's world no member
  reaches USD 250,000 by August and 25 reach USD 100,000 (2.9 per cent of the capped January to August amounts), and a
  practice's capped share moves from one year to the next by noise (about 1.5 per cent of a projection), so no flip
  holds.
- 2026-10-25, architecture 14 draw: competing exits read as censoring (a cumulative incidence against one minus
  Kaplan-Meier) is spent by task134, task254, task257, task264 and task266; a share above a cut counted from scores
  measured with error is task253's driver; random-groups equating with make-up sessions on one form fails on the
  group-equivalence check, which is the field's own quality control and lands by reflex.
- 2026-10-25, architecture 14 stage 2: the run-out (v13's golden) on the default path left Birrelhaven's 2025 twins,
  in a neonatal unit from 24 June to October 2025, running at the 2025 cut, and the same-cut figure read as the network
  would have reported it at 30 September 2025 then left their facility claims out of the run-out's denominator and kept
  them in its numerator: 32 of the 128 constructions entered seven, Birrelhaven out. Their stay now runs from 3 March to
  June 2025 and is paid by August, so no long stay runs at the 2025 cut and the run-out's precondition holds in 2025.
- 2026-10-25, architecture 14 stage 2: the asks' architecture 13 devices (Kesselcrest's reviewed 99215 visits at its
  99214 rate, Merrinlake's halved modifier 25 visits at no rate on the schedule, Pemberglen's coverage month in its
  payment reference, Kesselcrest's Medicare Advantage lines at another fee) all fell to one reader who matched every
  line to the schedule and every fee to the standard. The halved visit now passes that match (Merrinlake's 2026 level 5
  is twice its level 3, so a halved 99215 is a full 99213), Merrinlake's retro lines from its July run now carry a
  cohort's member months under its first month of coverage (every line its member count times the fee), and the
  Medicare Advantage lines are gone.
- 2026-10-25, architecture 14 stage 2: the benchmarks and thresholds as graded columns (26 figures every reader keeps,
  a third of the scored ask figures in architecture 13) were dropped from the prompt; the workbook carries them as the
  elections' context and the write-up names the two practices the stays move.
- 2026-10-25, architecture 14 stage 4 round 1 (target.zip cc4a6fbd821d4dfd): both scored readers filed the default ten
  and missed the call, and the judge returned DETERMINISTIC with FIX_NOW (Callowglen's share 0.002 points from its
  rounding boundary under 23 same-day duplicate visits, the chart graded on sign). Reader A rebuilt every payer's runs
  from the claims, read Kesselcrest's reviewed 99215 lines at their 99214 rate, took Merrinlake's halving as a payment
  reduction and spread Merrinlake's retro lines over the rebuilt members' months, keeping all 52 ask figures (score
  FAIL). Kesselcrest's review moved off the line onto a claim adjustment line (every line now matches its code), the
  world bills one visit a member a day, and the fees narrowed to each payer's July to September total, because a
  run-rebuilding reader reconciles any allocation of fees to the months they cover.
- 2026-10-25, architecture 14 fix pass: the narrowed fee ask (each payer's July to September coverage fees, 3 figures)
  withdrawn before any reader saw it: ceiling.py's cracker kept all three (Merrinlake's retro lines spread by their
  member counts, Pemberglen's from its payment reference), so precut's cracker row read "keeps 3", and a fee ask in
  these remittances has no device a run-rebuilding reader cannot reconcile. The remittances ship as distractors; ask A
  is the one device ask.
- Architecture 14, the network's stays still open at the cut carried at the member cap (2026-10-31, spent at stage 4):
  the repair's judge pass 2 found two graded thresholds a cent off with the 2025 measures within a third of a cent of
  a rounding edge, and the re-judge found the write-up's "all seven past the cap by 31 August" false under a pooled
  per-day reading (4,535.53 a day against the per-kind 6,380), thin margins and the stay amount unfiled. A FIX_NOW that
  fails twice is spent; the world goes with it. Lessons carried into architecture 15: every graded figure at least a
  quarter of its rounding unit from an edge under every defensible conformance, asserted; every factual write-up
  sentence true under every defensible reading of an unfiled amount; call margins no defensible variant comes within a
  few per cent of flipping.
- Architecture 15 draw screens (2026-10-31), each dead before a harness: fisheries observer-coverage discards (task275
  approved on it); a sum of probabilities against a count of shrunken predictions for a threshold count (task253
  approved on it); TNC deadhead at an airport curb (task467's airport ground-transport world); APU minutes from gate
  power draw (a reflex for the field's own analysts once the meter log is in the pack); crop insurance optional against
  enterprise units on prorated production histories (the prorated years print identical unit yields, which the hygiene
  battery flags); a funnel-flow grain bin's discharge order (physics no judge reproduces without a free regime
  parameter, and one of two traceability reflexes lands it); coincidental exact-key matches growing with the comparison
  file (task468's false links on common identifiers told in other words); a vendor's clustered coding audit (a filed
  confidence level plus a batch column points at the variance, readability test 1); queue time from backlog over
  intake (no ETL task type carries it); mine-to-mill change of support (a free choice of support correction, Gate C);
  record-linkage and seasonal-adjustment cells set aside on the directive's batch reading (task250 and task470 hold
  those client domains), the census-register cell on task470 itself.
- Architecture 15 stage 2 (2026-10-31), a limit of 3.0 per cent of the plan's cost on a menu of 2,000, 2,500 and 3,000
  dollars: the 2,500 option sat between the routes with margins under 1.2 on both sides; the resolution now allows
  2,000 or 3,000 dollars at no more than 1.90 dollars per covered person month.
- Architecture 15 stage 2, an ask on the persons at the maximum by relationship: a count the accumulators state
  outright; replaced by the orthodontic balances, whose units cross the migration.
- Architecture 15 stage 2, ask A as shares to one decimal: five of the seven quarters sat within a quarter unit of a
  rounding edge; asked as counts, which have none.
- Architecture 15 stage 3, a simulation that began on 1 January 2024 with nothing carried in: January 2024 held no work
  put off from 2023, so 2025 rose 11 per cent on 2024 and the October 2024 projection missed by 5 per cent, a search
  signal the back-test was meant not to give; a 2023 plan year now runs first and is not extracted.
- Architecture 15 stage 3, members putting work off before meeting the deductible, and new needs on a tooth whose work
  was put off: each opened a fork on the graded figures (the put-off work's deductible; a later claim on the same tooth
  matched by procedure family); a member now weighs a cut estimate only once the deductible is met, and work put off
  stands in for the next year's need on the same tooth and procedure family.
- Architecture 15 stage 3, a sentence in F-17 filing the deductible convention: it would have told a literal reader to
  charge the 2026 claim's deductible on the put-off work; the records carry the convention instead (SF6, SF14).
- Architecture 15 stage 3, a request stamped on the stroke of 5:00 p.m.: "after 5:00 p.m." and the golden's reading
  disagreed on it; no request is now stamped on the cutoff minute.
- Architecture 15 stage 3, the bound routes (every person at the maximum taking the whole rise; a year annualised from
  the day the maximum was met) reach 2,000 dollars without the decisive step, and no menu or limit moves them while
  the golden's correction raises the cost; they stay recorded in the ladder as the build's open exposure, each refuted
  by the records and each missing every graded cost figure.
- Architecture 15 (Pembrook Castings' dental maximum under F-17): the stage 4 judge returned NOT_DETERMINISTIC with
  SEND_BACK and the reconciliation confirmed a withheld rule: F-17 executed word for word on the 2025 claims gives
  increases of 0.83 (2,000) and 1.23 (3,000) and files 3,000, while the golden's 2,000 needed the work members put off
  to the January reset added back, which no shipped text states; the asks also left the put-off column's total, the
  deductible on 34 lines, "still in treatment" and an orphan case open. The slot's lesson: the filed standard's
  word-for-word execution must be the golden, and the difficulty is computing that filed quantity from the data's
  structure, never a correction the standard does not ask for.
- Architecture 16 design (2026-10-31): a third ask on the aluminium Midland recovered from each quarter's dross, read
  from its settlement statements, dropped before data was cut: with the lift date on each settlement line the figure
  is executed by any careful reader, and without it the figure rides the processor's booking lag, which no sentence
  can file without handing it over.
- Architecture 16 design (2026-10-31): the family intensities graded to two decimals, dropped on the measured spread:
  the defensible fits put 6082 billet between 0.260 and 0.268 and the castings between 0.45 and 0.52, so the call is
  graded on the premium and the families earning it, and the prompt pins no rounding on the intensities.
- Architecture 16, the homogenizing furnace's gas allocated by its loads' firing hours (2026-11-07, spent on its first
  portal round): both responses landed the golden premium of EUR 342,000 on the firing-hours allocation, the method a
  careful analyst reaches for, which the hourly gas fitted at R-squared 0.9985, so the fit handed over the route; the
  portal also flagged Domains Fit. The emissions-inventory world and the furnace-allocation driver are spent.
- Architecture 17 draw screens (2026-11-07), each set aside before a card: a linkage precision carried from a
  validation run onto a run with rarer true matches (task446's invariant, error rates carry and the yield moves, already
  screened at task174); claims completion by each nursing facility's own monthly billing day against the extract (the
  trap is per-reporter completion, 181's route, 445's reporters, task451's sender delay); IBNR from each member's
  infusion rhythm across the medical and pharmacy benefits (v14's skeleton: a per-member amount incurred and unbilled,
  read from a second stream, past a per-member threshold); same-event double capture across two lists, an ED-initiated
  treatment start recorded in both (task196's approved driver); chain-linked volume non-additivity (a named correction
  in the accounts manuals, the library test); construction value put in place spread by each project's own endpoints
  (the progress reports back-test the duration scaling, so the fit points at the golden); Medicaid encounter
  completeness by subcapitated vendor (encounter data validation is the actuary's own step); a regional series'
  seasonality rebuilt from its units' histories (one join and a per-cell mean); a year-end processing pattern absorbed
  as seasonality (the change is dated and visible).
- Architecture 17 draw, the due-contact family (2026-11-07, five prototypes): register children counted resident only
  where activity shows, and absence of activity is evidence of departure only where a well-child contact fell due under
  the child's own centre's schedule. District schedules put inactivity at 6 per cent against 36 (the pack's largest
  anomaly); masking it with district emigration biased the golden by +5.4 per cent; centre catchments left the pooled
  route within the golden's own noise (pooled minus golden sd 1.6, golden sd 1.1); a previous cohort's complete outcome
  made the golden exact (sd 0.8) but per-centre calibration landed within 1.4; a recall rule keyed to each child's own
  history removed the anomaly and the district by age-year calibration landed at +0.1 per cent. Its world also sat
  beside task471 v4's register-adjusted municipal population, and its honest label, composition_mix, was banned when
  the family was screened.
- Architecture 17, first prototype of the drawn mechanism (2026-11-07): with schools whose Term 3 unit ended before
  their first sitting day, recalibrating on whole schools that had finished the unit landed the golden in 20 of 20; the
  world gives every Term 3 unit at least five weeks against a sitting in weeks 3 to 5, so no school has finished one
  before it sits and taught responses exist only inside schools, after each school's own last lesson.
- Architecture 17 stage 2 (2026-11-07): both Term 3 units ending inside the sitting window (the prototype's world) is
  not how a ten-week term runs; the generator teaches the units in sequence, the first ending in week 4 or 5 of each
  school's own term and the second at its term end, which first left about 5 per cent of the Term 3 responses taught
  (about 60 per item, the golden 0.24 logits off the truth on the shipped seed) and was widened to a sitting of 6 to 9
  days with the first unit ending 1 to 7 school days after it (about 11 per cent, 150 per item).
- Architecture 17 stage 2 (2026-11-07): drafts composed on the shipped seed's golden estimates put the golden at B on
  redraws whose Term 3 estimates fell the other way; the drafts are composed on the items' taught difficulties and the
  shipped seed chosen from a scan (482025) where every graded figure sits a quarter mark inside its bin, the bank
  picks A, every golden variant keeps the whole marks and every rival route misses C.
- Architecture 17 stage 2 (2026-11-07): golden targets A 27, B 26, C 25 left the bank's pick split between A (8 of 20)
  and B (12 of 20); retargeted to A 26, B 23, C 25 so the bank lands on A in 20 of 20. A Term 3 taught mean of 0.15
  logits put the banked Term 3 items at the hard end of the bank (half a logit above the rest, two of them the bank's
  worst outfit); a mean of -0.85 with the untaught effect held to 0.6 to 1.3 logits puts them 0.20 above, inside the
  spread.
- Architecture 17 asks (2026-11-07): a licence-fee ask (one publisher's stimulus fee repeated on every item line, the
  other's fees in Australian dollars) needed either the agreement's per-stimulus clause or the publisher's invoice to
  find the repetition, the first a filed rule adjudicating the device and the second an oracle tying only under the
  golden; an item-exposure ask could move the call through a disqualified draft; both dropped for the make-up mean.
- Architecture 17 asks, parent review (2026-11-07): with the make-up count unasked and walk-ins absent, the full
  includer (roster join, entries on first name, surname and birth date) kept 6 of 12 ask figures, over two fifths;
  unbooked absentees who sat at a host and reach only the keyed file (D4, their home school through the entry number
  keyed and the register) put a second reconstruction on the sat block, the make-up count joined ask B by shape, and
  the full includer keeps 4 of 16.
- Architecture 17 stage 4 round 1 (2026-11-08): the judge returned FIX_NOW on ask B alone: the batch of 13 scripts
  keyed on one day, all even and seven over 50, could be halved whole, in part, dropped or kept, because no shipped
  file stated the make-up paper's maximum or the keying unit; the roster's header now files both in the office's
  voice with the batch rule, the keyed file numbers each session's batch, and the golden memo states only what the
  files show. The reader came back clean; its one note (every early register row on one entry date) is answered by
  each school's upload carrying its own day.
- 2026-11-08, platform round 1 on architecture 17: both runs filed Paper C and every regional figure. Run 1 fitted coverage penalties for U5 and U6 (about 1 logit each) and zeroed them for November; run 2 kept U5 and U6 responses only after each school finished the unit. The August-against-November gap in the prompt, the course outline and Appendix B's per-school sequences handed over the join, and taught-content adjustment is a reflex; spent (runs/triage.md).
- Architecture 18 draw screens (2026-11-08), each set aside before the card: a guessing floor at a low Level 1
  standard on Level 2-calibrated multiple-choice items (a prototype put the bank eight marks off the truth and spread
  the floor-only and full routes over three marks around it: Rasch misfit at the low end makes every estimator's
  answer depend on its form, and a three-parameter fit is the reflex for multiple-choice data); the same floor offset by
  a reading cost on the bridging items (the same fragility, replaced by two clean shifts under a true Rasch model);
  teacher-judgment standard setting with class-referenced judging (the literal standard executes to the pooled
  contrasting-groups cut, so the correction is a withheld artefact rule, and a moderators-only route is unbiased);
  standard maintenance through prior attainment with the prior's unreliability (task5's screen: a measurement model
  whose estimate spreads, and the school-level route lands); common-centre standard maintenance with centres leaving
  after a bad year (about a tenth of a logit of regression at realistic selection, and multi-year averaging, the
  reflex, removes most of it); item clones whose features shift difficulty (one pass mark for every version is
  unbiased on average, so the call does not move); a concordance from dual test-takers who took the second test after
  a low first score (mark474's driver, selection on falling short in a common-person link); a pretest-to-operational
  shift, repeaters' familiarity with reused items and mid-life item revisions (each removed by a reflex: a pretest
  adjustment, excluding repeaters, a latest-version rule).
- 2026-11-08, architecture 18, stage 2: the regional ask as a count of expected passes (the first prompt draft) was replaced by a mean mark, because a count at whole candidates moves with every estimator choice near the pass mark; the mean mark at one decimal was graded in whole marks instead, because the ability estimator and scale family (Warm or maximum likelihood abilities, the joint likelihood's stretch undone in part or in full) spreads each region's mean by up to 0.26 of a mark; and each patterns item's chance is graded as its band verdict and the group's range, because the forms of the split move single chances by up to 0.048. Seeds 818018 to 818043 were screened (the call's bin, the band edges, the rivals' distance, the regional whole marks over the family); 818025 is the one kept.
- 2026-11-11, architecture 18 spent before upload: cut under the retired single-deep-step design (one pass mark carried by one decomposition of the borrowed items' shift); re-rooted on the author's word to a results chain for the 2026-11-09 bar.
- 2026-11-11, architecture 19 draw screens, each set aside before the card: an exam board's paper-to-screen mode move linked through embedded anchors (the slot's own lineage of banks, papers and pass marks, and a dial again); three interim vendors linked through a state test with a test-date growth term (the vendors' week-of-instruction norms already absorb the date, so the term decides nothing); a single NEAT link of one test to Lexis through KS2 alone (the anchor's four-month gap and lower reliability bias any observed-score link across groups as different as the Brightway and Lexis academies by about two standardised points, so a lone anchor link cannot be both the golden and true, and the decision would hang on one link); a January exit forecast with test-specific regression to the mean (no history pairs a September result on one test with a January result on another, so the forecast's form would be an open fork).
- 2026-11-11, architecture 19, stage 3: every rival placing the same students in every academy (the first check) was dropped for whole-score-group bands: in 60 worlds scanned (seeds 8340 to 8399) the rivals differed by 10 to 28 students in total, because a converted score near the whole-score cut moves a whole score group of 15 to 25 students; seed 8342 is kept (only no presmoothing differs, by 16 at the Brightway academies, and the trust total sits 1.7 per cent from the simulator's expectation).
- 2026-11-11, architecture 19, stage 3: Brightway linked through KS2 was left open as a rival and dropped: it lands 838 to 874 students as the presmoothing changes (four moments 838), which would have put the hurried totals inside the total's band; the policy now files the trial as the trust's Brightway link (section 6), and the KS2 route sits in the ruled-out routes with its numbers.
- 2026-11-11, architecture 19, stage 3: the coded careful pass first fitted KS2 to Lexis on the September sittings alone while taking the July sittings as entry reading, a pass that knew the July timing in one step and not the next; it now pools every Lexis sitting into the reference, as a run that has not seen the July timing does, and R4 moved from Right to Missed in the careful column (pair 34.5 to 16.2).
- 2026-11-11, architecture 19, stage 3: two literal readings of the policy were closed before stage 4: "since the end of Year 6" excluded the 1 to 3 July transition-day sittings (Year 6 runs to late July), now "after the May 2026 KS2 tests"; "the Lexis score equal to their KS2 reading scaled score" read as numeric equality, now "from their KS2 reading scaled score, at the whole Lexis score of equal reading at the start of Year 7".
- 2026-11-18, architecture 19 set aside before any upload (the record above): a build that turns on two judgments of which one is a closed lesson cannot be levelled up in place, because its graded figures are head counts every route rebuilds and its world carries no third instrument; re-rooted as architecture 20.
- 2026-11-18, architecture 20, the draw: each centre's portfolio marks moderated statistically against its candidates' written paper was dropped at the screen: the fit is decided by regression to the mean and a flattened slope (both closed), and the boards set their own papers, so the paper links nothing across boards. No paper marks ship.
- 2026-11-18, architecture 20, the draw: a principal's cold check of a slice of live samples as the instrument for the share was dropped: a labelled slice under a wide instrument is a calibration set the strongest run fits and carries unprompted (memory of task3's referee), and what is left is carrying an effect to another mix (closed). The share is read instead from the standardisation trial, which is kept for another purpose and has to be joined back to the live moderation.
- 2026-11-18, architecture 20, the draw: centres that changed board, re-moderated by their new board, as the link between standards was dropped: how fast a centre takes up its new board's standard is an open fork no file can close. The link is the people who moderate for two boards, read on their cold trial marks; no centre changes board in the record.
- 2026-11-18, architecture 20, the draw: a top-three call (the three boards furthest from the standard) was dropped: the cycle stump never changed the set. The call is the protocol's tolerance of 2 marks either way on every board, which each stump flips on its own member.
- 2026-11-18, architecture 20, the draw: conversion amounts in whole marks inside the call was dropped: a board at 2.98 converts by 3 and at 6.22 by 6, and a rival at 6.5 by 7, a rounding fork on the recommendation. The conversion is the estimated distance itself, stated with its band.
- 2026-11-18, architecture 20, the draw: a uniform tolerance of 3 marks across the boards was dropped: at the first dials one board adjusted 87 per cent of its sampled centres and another 58, which no board does. Tolerances are the boards' own (3 to 6 marks) and the drift slower; 4 to 33 per cent of sampled centres are adjusted, fewest where the moderators record least.
- 2026-11-18, architecture 20, the draw: a review restricted to the centres a board did not sample was dropped as a file that exists only for the check; the regulator's review covers every Dunmoyle centre, as a real review would, and is read on the unsampled ones. Its cost is stated under Referee: read raw it gives Dunmoyle's own level, about 8 rubric points on any route.
- 2026-11-18, architecture 20, the draw: the first dials (seed 8120, a moderator's error of 2.4 marks, 30 trial scripts a year) failed the core on the battery: Fennor's golden landed at 1.96 against a world value of 1.48 and one variant crossed the line. The cause was sampling error on the centres not sampled in the year, not a bias (the fitted and the world's cycle levels agree). Fixed in the world, not in the estimator: 40 trial scripts a year, a moderator's error of 2.0, Fennor placed lower with a stronger cycle, Gortavale and Eskerry likewise; 13 of 16 seeds then pass and the other three fail on the referee's margin only. Seed 8134 is kept (one stump lost 22, 22, 22).
- 2026-11-18, architecture 20, the draw: the rigorous standard route first filed Ardkeel right (2.10), because that board's own-trial severity lifted it over the line; a board whose cold consensus sits below its principal's agreed marks has a negative own-trial severity, which is as natural, and the route now files 1.10.
- 2026-11-18, architecture 20, the draw: the guard blocked the first card on the pattern (G3 against task3) and the organisation family (government_agency against task3). The largest mover of the call is the standard each board marks to, a unit-of-value swap (G1), and an awards body is commonly a not-for-profit: both changed on the card, nothing in the core moved.
