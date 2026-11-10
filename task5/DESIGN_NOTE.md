# task5: the counties the Department can certify for the 2027 Community Transition Fund, and the estimate behind them

Architecture 4 (re-rooted 2026-11-10 as a results chain in the same State of Franklin world, at the author's word,
after architecture 3 was returned at review as turning on one thing), second cut: the stage 4 judge found the first
cut deterministic but thin at Kittredge and narrow in its bands, so the world was redrawn on seed 50431 with the
seasonal lake resorts removed, the downturn reshaped and every band given a floor; its second pass found the list
forced and asked for wider ranges and stated conventions in the answer blocks, which are in (see `## Stage 4`). Read
`## Tried and rejected` first. Every figure below is measured by `generator/checks.py`, `generator/effort_passes.py`
or `generator/golden.py` on the cut pack.

## Draw

Subdomain: Survey Research & Official Statistics (Other), census, register and administrative-data quality
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a reconciled table plus findings (each county's December 2026 covered jobs split into reported and estimated, its change on December 2025, reconciled to the published 2025 total and replayed on December 2025; the counties to designate on top)
Weight: a hard-to-measure quantity: the December jobs the files do not yet hold (employers whose report is out, employers with no account yet, worksite splits not yet in); task7 sits on modeling, task4 on measurement, task1 on synthesis; task6 (four cards back) also sits on a hard-to-measure quantity, a trace-sampled SLI, which shares nothing with a census caught early, so the guard's overuse WARN is answered here
Data-native sentence: forty-five days after the quarter the Division's files run behind the employment they record in four different ways at once (reports in agents' late batches, reports that will never come, accounts not yet set up, worksite reports trailing the contribution reports), each with its own evidence in the closed quarters, and the 2026 housing downturn makes this quarter unlike those closed quarters.
People: Danielle Fuller, director of the Labor Market Information section; Matthew Cox, the Department of Commerce's administrator for the Fund; William Robertson, chief of the Unemployment Insurance Tax Division (`guard.py names --geo "United States" --seed 501` and `--geo US --n 4 --seed 50327`, kept from architecture 3). None appears in the prompt.

Card `.claude/skills/fingerprint/cards/task5.json`, architecture v4, registered 2026-11-10 at 01:59:25Z (the draw; the
card's figures were refreshed at the second cut without a new draw): WARN only (overuse.weight against task6 v7,
answered above, and against task9 v7, re-rooted later the same day on a lender's recoveries and sector loadings, which
shares no result with a census caught early; repeat.gate_g and repeat.decision against task7 v8: that build picks
measures under a grant-per-tonne limit from a lottery, this one certifies a census caught early, and the two share no
result). task17, drawn at 03:33:57Z, shares this build's strategy and organisation family and is the later draw. The
decisive generator was redrawn from G13 (banned against task1 v2) to G3, record against operation, which is the
honester label for a chain whose every result completes a record the operation has run ahead of. The forum was redrawn
from committee_or_panel (task7 v8 in the window) to minister_or_cabinet: the estimate is prepared for the Commissioner
of Labor's certification, due by statute on 1 March; the Board's designation follows it mechanically.

## Deep reasoning

Task type: census-register-administrative-data-quality in Survey Research & Official Statistics, which serves Data Extraction & Conformation: an official covered-employment statistic conformed from an administrative report census caught 45 days after the quarter, with the part not yet on file estimated component by component and the result reconciled to the published table and to the later records.
Domain test: every result is a quantity an official statistics office produces for an early estimate from an administrative census: the response status of the census at the cut-off, a nonresponse mechanism and the nonrespondents' outcome on resolved cohorts, a coverage adjustment for units not yet on the frame, an allocation of multi-establishment employers to areas, a revision analysis against the published figure and a replay against the later records; the field's delinquent-report imputation is the textbook and sits in the hurried column.
Swap: "which regions' December inpatient days fell 2.0 per cent, on the best estimate from the hospital returns on file on 15 February" keeps a threshold and late returns, but no hospital stops filing because it has closed, no account is set up weeks after a unit starts trading, no payroll agent files a batch, no worksite report distributes a total and nothing is inactivated two quarters later, so six of the nine results have nothing to estimate and the call stops making sense.
Where the weight sits: the jobs not yet on file (R2 to R5): 39,900 of the state's 473,500 December jobs are estimated, and each part needs its own reconstruction across files and quarters (agents' batches rebuilt from receipt seconds and followed from quarter to quarter; outcomes read on cohorts old enough to have resolved; this quarter's share of jobs at employers outstanding on their own measured where standing shows and carried to where it does not; registrations developed from this quarter's early count; each worksite carried by its own season). The work is long, not clever: none of the parts is found by one look and each has a cruder version that validates on a normal year.
Layer 1: amended reports superseding originals, a few of them audit corrections months later, and exact resubmissions seconds apart (the Division's filing system); reports received on paper keyed by date with no time (the mail room); account numbers hyphenated with a check digit in the register and as digits in the worksite file, county codes in the register and upper-cased county names in the worksite file (two systems); NAICS 2017 codes on older accounts beside NAICS 2022 (the register's history); successor accounts after a transfer of business, the predecessor ended (account maintenance); habitual late filers; worksite reports whose months do not add to an amended contribution report; reports held for accounts not yet established and posted later with their receipt time. Each is asserted neutral (R2 block, SF4, SF6) and none decides a result.
Not one thing: no single piece carries the answer, and the call needs two different judgments in two different counties. Without the reading by cause Garrow stays above the line under every way of carrying the outstanding reports alike (-1.9 to -1.2); with the latest worksite reports' split Kittredge reads -1.2; Ostrom is designated under most hurried routes. A run that nails the reading by cause still loses the worksite split (R5), the Lakes counties' figures (R6, R7), Kittredge (R8) and the replay (R9); a run that nails the worksite split still loses R2, R3, Garrow and its neighbours' figures. The stage 4 judge, on both cuts, counted three separate pieces of work each flipping a different county.
One-fact test: the most useful single sentence (a report that is out with its payroll agent's whole batch says nothing about the employer, one that is out on its own usually means trouble, and such employers kept about three tenths of their jobs at earlier cut-offs) rescues 1 of 9 results on the careful pass (R2); the worksite sentence rescues 1 (R5); the sentence about this quarter's share in construction rescues none without the reading by cause, and the sentence about accounts set up after the cut-off none (the careful pass already develops them). None rescues the call, which needs the reading by cause and the worksite split together (effort.py, hints executed on the careful pass). The stage 4 judge's own count for the cause sentence was about 4 of 13 graded items on the second cut (under a third), down from about 4 of 9 on the first, where the call turned on Kittredge alone.
Not semantics: every field read right (receipt times to the second, report types, the two dates on each account, the status history's effective and entered dates, the worksite reports' dates received, the Act's population) gives a correct census of who has and has not reported and which accounts exist, and still leaves a careful run carrying every outstanding report at its reporting peers' change with one survival share and the worksites at their latest split: nothing filed says what an outstanding report means, how many employers have no account yet or how a worksite's share moves with the season.
Not rule application: the Act files the population (every employer subject to the Law, reported or not, with an account or not), the outcome, the line, the cut-off, the base and the two reports it wants (the published figure reconciled, the replay), and the agreement describes fields; no filed sentence says how an outstanding report, an employer with no account or a missing worksite report is estimated, and once every filed rule is applied all 39,900 estimated jobs are still to be judged.
Estimand: sections 2(c), 2(d), 4 and 5(a) to 5(c) of community_transition_fund_act_2026.docx: population every employing unit with a worker in covered employment on any day of the fourth quarter of 2026, whether or not its report has been received and whether or not an account has been established; outcome workers on the payroll for the pay period including 12 December at worksites in the county; window December 2026 against December 2025; unit jobs by county; comparison December 2025 from the same records at the same date (not the published table); threshold minus 2.0 per cent or lower after rounding to one decimal; the records as they stand at the close of 15 February 2027; the replay from the records as they stood at the close of 15 February 2026. ui_lmi_data_sharing_agreement_2025.docx defines every field, says a report counts from its account's establishment and that the worksite report distributes the contribution report's employment.
No decoy: nothing is written to carry a wrong answer: no memo, draft, flash or stakeholder figure for December 2026 ships; the request quotes no figure; the published fourth-quarter 2025 table is correct on its own footing (reports posted through 31 May 2026) and reproduces from the records of that day (SF7).
No replay: no result re-derives a published figure: the reconciliation explains why the records now differ from the published table (three exact items, nothing unexplained) and no stated number is wrong.
Pinned: every rival is run on the cut pack (checks.py, 119 assertions; verify.py recomputes every graded figure on its own code path): the 30 members of the standing family (a batch as two, three or four reports in a second; arrived at a third, a half or two thirds; this quarter's share carried to the late batches or not, by supersector, three-digit industry or a hand-picked group of housing industries, with or without size; the resolved quarters with the earliest or the latest left out, or every closed quarter with the unresolved left out or at nought; the share kept by size, channel or industry group; late every quarter as all or three of the last four reports, the habitually late carried with the late batches or at the reporters' change; a late employer by its cell or by its own change a year earlier; the reporters' change in cells of five, ten or twenty or by supersector statewide; unregistered employers developed on fourth-quarter cut-offs or on every cut-off; a worksite by its own change a year earlier or by last December's split; the employers still silent for December 2025 at nought or at their last report) designate Garrow, Kittredge and Ostrom, each 0.6 of a point or more below the line and every other county 0.6 or more above it, with every county's change within half a point of the golden's. Each band holds the family and never comes nearer the figure than half a point (half a per cent of a county's jobs), the room an independent rebuild of the same estimate needs: the stage 4 judge's two rebuilds sat within 0.1 of a point in five named counties on the first cut and up to 0.45 away in Bray and Ostrom on the second. No band reaches within 0.4 of a point of the line. Two variants are ruled out by named facts and designate the same three anyway (unregistered employers shared out by each county's accounts: the quarter's registrations depart from account shares by 1.5 times or more; the reporters' change by county alone: it differs by five points or more across supersectors).
Run forecast: R1 and R4 earned (hygiene; developing this quarter's registrations is the field's textbook, and the stage 4 judge's own derivation ran it unprompted on both cuts); R2 lost to stopping at the first story (every outstanding report read alike, one survival share from a back-test: 0.92 against 0.29 and 0.96 by cause); R3 lost with it to a self-confirming check (a pooled rate back-tested on the closed quarters passes there, and this quarter is never set against them); R5 lost to a method shortcut (the latest worksite report's split); R6 and R7 earned in part (nine of fourteen counties inside their bands, the other five 0.7 of a point or more out); R8 lost (Ostrom alone on the careful pass; Kittredge and Ostrom, Kittredge, or Garrow and Ostrom on a run that does one of R2 and R5); R9 lost to a self-confirming check (the pass's own replay is 0.4 per cent low for the state and half a point out for the average county, a point or more in the Lakes, and is read as close enough).
Strategy label: WORKS IN FORM (outcomes that have not finished happening: completion differs by a unit no pooled factor captures, here the cause of each outstanding report, this quarter's share of employers in trouble, this quarter's registrations and each worksite's season); the dead form, the field's delinquent-report imputation as the golden, is the textbook route and designates Ostrom alone, or Kittredge and Ostrom once the worksites are carried.
Depth level: 5. Six judgments each move a graded figure on their own (the cause of an outstanding report, the resolved quarters, this quarter set against the closed ones, the count and the size of the unregistered employers, the worksite carry, the replay's footing), two of them move the designated set in two different counties, and effort.json records five distinct wrong sets over eleven shortcuts (all fourteen counties; Ostrom; Kittredge and Ostrom; Kittredge; Garrow and Ostrom).
Lesson: an early estimate from an administrative census is completed component by component, each from the evidence of its own delay: a report's absence means what its usual companions' arrival says it means, a closed quarter tells what the missing kept only once its closures are recorded, this quarter's closure rate has to be read where it shows before the closed quarters' rate is lent to the units whose standing does not show, the units not yet registered are counted from this quarter's early registrations, and a total is split among places by each place's own season; a crude version of each validates on a normal year. No build on file teaches an estimate assembled from several delays at once.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the census at the cut-off (27,796 liable accounts, 21,743 reports received, 6,053 outstanding) and December 2025 now on file (472,867) against the published 472,199: 173 on late reports, 502 on accounts established since, -7 on amendments | assembly and reconciliation | the Act 2(d) and 5(a); the register's two dates, the status history's effective and entered dates, received_at; the published table's own footing (reports posted through 31 May 2026) | exact | earned by a careful run; the quick pass is a method shortcut (the register's active accounts, the published table taken as the base, the difference left as one lump) | - | Ask 6 |
| R2 | the outstanding reports by what their absence means: 3,992 in agents' batches not yet received, 815 outstanding on their own, 355 late every quarter, 812 two quarters out, 79 new accounts; those outstanding on their own kept 0.29 of September on the resolved quarters, those in late batches 0.96 | missingness and measurement | received_at to the second across quarters (a batch is three or more reports in one second); the resolved quarters' late reports, closures and inactivations | 3,900 to 4,080; 1,140 to 1,200 for the next two together (750 to 880 and 300 to 420 apart); 0.24 to 0.37 | stopped at the first story: every outstanding report read alike and carried at one survival share from a back-test (0.92), which is what the stage 4 judge's own derivation did on both cuts | R1 | Component 1 |
| R3 | this quarter set against the closed ones: employers outstanding on their own hold 7.9 per cent of construction employers' September jobs against 0.8 a year earlier and under one per cent at every earlier fourth-quarter cut-off (815 employers against 309), so the closed quarters' pooled experience does not describe this quarter's outstanding reports | causal reasoning (does the closed quarters' evidence carry over) | the share among employers whose standing shows, by supersector, at this and every earlier cut-off (0.9, 1.1 and 2.7 at the first three cut-offs of 2026) | 7.4 to 8.4; a year earlier 0.3 to 1.2 | self-confirming check: a pooled share or survival rate is back-tested on the closed quarters, passes there, and is carried into a quarter it does not describe | R2 | Ask 9 |
| R4 | the employers liable for the quarter with no account yet: about 590 employers, 2,400 December jobs | missingness and measurement (immature cohort) | the Act 2(d) and 5(b); the register's liability and establishment dates at this and earlier cut-offs; late registrants' later reports | 500 to 630 employers; 2,000 to 2,600 jobs | earned by a careful run that develops this quarter's registrations (540 employers and 2,200 jobs on every earlier cut-off; the judge's two derivations gave about 2,100); the unfinished chain carries last year's unregistered jobs as they were (3,400) or leaves them out as not estimable | independent: the register's liability and establishment dates | Component 3 |
| R5 | the county split of the 185 multi-county employers whose worksite report is out: about 260 fewer jobs in Kittredge, 150 fewer in Talcott and 80 fewer in Sayre than the latest reports' split, 120 more in Calder, 110 more in Linden and 90 more in Ostrom | forecasting (each worksite's seasonal carry) | the worksite reports and their dates received; each worksite's own change between the same two quarters a year earlier; the lake worksites' fall in every earlier December | 190 to 330; 100 to 190; 40 to 110; the other three within 40 jobs | method shortcut: the latest worksite report's split as it stands | independent: the worksite reports and their dates received | Component 2 |
| R6 | each county's December 2026 jobs and the part estimated (fourteen counties and the state: 473,500, of which 39,900 estimated) | decomposition and attribution (reported plus estimated reconciles to the total) | the Act 5(a) and 5(b); R2, R4 and R5 carried through every employer and worksite | each county within its family range and never nearer than half a per cent of its jobs (100 to 1,040 jobs wide) | unfinished chain: five counties outside their ranges on the careful pass | R2, R4, R5 | Ask 2 |
| R7 | each county's change on December 2025 (Ostrom -3.1, Garrow -3.0, Kittredge -3.0, Bray -1.1 nearest; state +0.1) | synthesis | the Act 4 and 5(a): December 2025 from the same records at the same date | each county within 0.5 to 0.6 of a point, no band within 0.4 of the line | unfinished chain: five counties outside their ranges, each by 0.7 of a point or more (Garrow -1.9, Kittredge -0.9, Bray -0.3, Talcott 2.4, Sayre 2.2 on the careful pass) | R6 | Ask 4 |
| R8 | designate Garrow, Kittredge and Ostrom | synthesis | the Act 4 | exact set | unfinished chain: Ostrom alone on the careful pass; Kittredge and Ostrom, or Kittredge alone, with every outstanding report carried alike and the rest right; Garrow and Ostrom with the latest worksite split and the rest right | R7 | Recommendation |
| R9 | the same estimate replayed on December 2025 from the records of 15 February 2026: -0.01 per cent from the state figure now on file, 0.16 per cent for the average county | validation | the Act 5(c); every date in the four extracts | -0.30 to 0.20; up to 0.35 | self-confirming check: the careful pass's own replay is 0.41 per cent low and 0.47 out for the average county (a point or more in the Lakes) and is read as close enough; the quick pass has no replay | R2, R4, R5 | Ask 7 |

R2 sits upstream of five results (precut's WARN). Each of the five needs work of its own beyond it (R3 the look across quarters, R6 to R8 the worksite split as well, R9 the as-of footing), the largest single hint rescues 1 of 9, and the cause sentence leaves the call wrong in Kittredge.

The estimate also carries this quarter's share to the employers in late batches (about 590 fewer jobs than the reporting employers' change; construction employers at 0.79 of September against 0.84). That refinement is not graded: a sound estimate without it stays inside every band, the judge's second rebuild left it out and still designated the three, and nothing on file at the cut-off can test it. It is described in the workbook and the steps as the estimate's own.

Carry-forward: R1 stands on the filed population and the dates; R4 and R5 stand on inputs of their own (the register's two dates; the worksite reports and their dates received) and are graded whatever a run did with the outstanding reports; R3 falls with R2; R6 falls with R2 or R5 county by county (a run that misses only the worksite split loses three counties, one that misses only the reading by cause the housing-heavy ones, one that leaves the unregistered employers out six by half a point or more); R7 and R8 fall with R6; R9 falls with R2 or R5 where the miss shows on a normal year (R5 does). No analytical result is the only analytical input of more than one other.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a report outstanding on its own (its usual batch arrived without it, or the employer files singly) marks an employer in trouble | constructed by simulating how payroll agents and employers file | no: 815 employers at this cut-off in every county (5 or more each), 280 to 560 at each of eleven earlier cut-offs; carrying every outstanding report alike misreads Bray, Talcott and Whitcomb, where nothing turns, by half a point or more, as well as Garrow | modelling: batches rebuilt from receipt seconds, followed from quarter to quarter, then outcomes on resolved quarters | modelling: an outcome measured on cohorts old enough for closures to be recorded | keep: R2; with R3 it decides Garrow |
| the 2026 housing downturn: employers in trouble in construction and the industries that supply it at several times the usual rate | constructed as an economic process deepening through 2026 (construction's share of jobs at employers outstanding on their own 0.9, 1.1 and 2.7 per cent at the first three cut-offs of the year, 7.9 at the fourth), with county-to-county noise | no: every county carries it by its industry mix (construction employers outstanding on their own in all fourteen, most of them outside the designated counties), and it shows in the reported jobs too | a targeted query once the outstanding are read by cause (the share by industry, this quarter against earlier cut-offs) | modelling: the share measured where standing shows at this and every earlier cut-off, which decides whether the closed quarters' evidence carries over | keep: R3 grades the comparison (this quarter against the closed ones); the carry to the late batches is the estimate's own refinement and ungraded |
| accounts established weeks after liability begins | constructed by simulating the Division's registration (employers that register promptly, with their first report, or only when found) | no: every county (15 or more jobs each) and every earlier cut-off (150 or more accounts each); leaving them out misreads all fourteen counties by 0.3 to 0.8 of a point and flips none | a targeted query on the register's two dates, which the Act's population asks for | modelling: a development estimate (this quarter's registrations so far, earlier cut-offs' delays, late registrants' size; last year's level and the registered employers' size each overstate by 40 per cent or more) | keep: one result (R4), earned by a run that develops the registrations |
| worksites with their own seasons, and worksite reports that trail the contribution reports | constructed by simulating multi-county employers (lake, North Woods and metro worksites; worksites opening and closing) | no: the latest split misplaces 60 jobs or more in six counties (Talcott and Sayre, where nothing turns, Calder, Linden and Ostrom, as well as Kittredge), and the lake worksites held fewer jobs in December than in September in every earlier year | a targeted query (a worksite's months across quarters), or the split checked against the report that came later | modelling: a per-worksite seasonal carry normalised to the employer's December jobs; last December's split lands in every band | keep: one result (R5); it decides Kittredge |

The seasonal lake resorts of the first cut (a subgroup of single-county employers in Kittredge and Talcott on one fixed monthly profile, carried by their own December on September) are gone from the world: constructed, in two counties one of which decided, found by one group-by and fixed by one routine step, they were the banned shape. Regional seasons now sit only where the worksite reports carry them, across seven counties.

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the census at the cut-off and December 2025 against the published total | Missed | Right | Right |
| R2 the outstanding reports by cause, and what those outstanding on their own keep | Missed | Missed | Right |
| R3 this quarter set against the closed ones (construction's share at employers outstanding on their own) | Missed | Missed | Right |
| R4 the employers with no account yet | Missed | Right | Right |
| R5 the worksite split against the latest reports' (jobs by county) | Missed | Missed | Right |
| R6 each county's December 2026 jobs | Missed | Partly | Right |
| R7 each county's change on December 2025 | Missed | Partly | Right |
| R8 the counties to designate | Missed | Missed | Right |
| R9 the replay on December 2025 | Missed | Missed | Right |
| Roughly | 0 of 9 | 3 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (generator/effort_passes.py runs each pass end to end on the cut pack; no cell is hand-graded)
Largest single hint: an employer's worksites keep their own seasons, so the latest worksite report on file does not give December's split; rescues 1 of 9 results (the cause sentence also rescues 1, the other two none)
Pair estimate: 37.0

The careful column is calibrated to the run record, not to the design: it is the derivation the stage 4 judge wrote
from the pack alone before opening the answer blocks (a careful run at medium effort). It conformed the census and the
reconciliation, back-tested the outstanding reports as one pool (a survival share and the reporting employers' change
by supersector), counted two quarters out as nought, developed the unregistered employers with a chain ladder on the
register's two dates, split multi-county employers by the latest worksite report and read its replay at the state
total. It designated Garrow and Ostrom on the first cut and missed Kittredge. On this cut the same route designates
Ostrom alone (Garrow -1.9, Kittredge -0.9), earns R1 and R4 and nine of fourteen county figures, and loses the reading
by cause, the look across quarters, the worksite split, the call and the replay. The paper is honest about two things: a
run that also carries each worksite's season keeps the Lakes counties and Kittredge and lands Kittredge and Ostrom
(Garrow -1.9, a tenth of a point above the line under one of the three pooled routes, so a pooled run can also fall
on the right side of it by chance); and the platform's two runs are the only measurement. The judge's own estimate on the
second cut was higher than this table (careful 7 of 13 graded items against 3 of 9 results here), which is the reason
the paper figure is not the claim: both sit under the bar, and the runs decide.

## Data provenance

Source: generated by task5/generator from a simulated process (sim.py, pack.py, docs.py), seed 50431; the NAICS code titles are the Census Bureau's own classification, everything else is invented.
Behaves like the real thing: the generator simulates how a state unemployment insurance tax division's files come to exist: about 40,000 employers with monthly jobs (trend, industry seasonality, noise), payroll agents that send their clients' reports in one transmission, the same agents swamped every January, employers in trouble that stop filing and are inactivated two quarters later, ordinary closures with a final report, new employers that register promptly, with their first report or only when found, examiners who set up accounts weeks later, worksite reports that trail the contribution reports, worksites with their own seasons that open and close, amendments, resubmissions, paper reports, successors, and a published table cut on its own date; this matches how QCEW source files behave (delinquent reports, late account set-up, multiple worksite reports).
Genuine patterns: (1) industry seasonality by supersector; (2) county trends and month-to-month noise scaling with size; (3) year-end lateness concentrated in the same agents every fourth quarter; (4) a business cycle in construction and the industries that supply it through 2026 (survivors shedding jobs, employers of every size under a hundred in trouble at a rate that deepens quarter by quarter, fewer start-ups) with county-to-county noise; (5) hazard of trouble falling with employer size; (6) registration delay by how an employer registers, late registrants smaller; (7) worksite seasons by region and industry (lake summer trade, North Woods winter recreation and outdoor work, metro holiday retail) and worksite turnover higher in project industries; (8) births, ordinary closures and transfers every quarter.
Problems by process: amendments weeks or months after the original (corrections and audits), resubmissions seconds apart (the filing system), paper reports keyed by date (the mail room), two account-number formats and two county formats (two systems), NAICS 2017 codes on old accounts (the register's history), reports held until an account is established (registration), worksite reports that do not add to an amended report (two filings), accounts inactivated months after the employer stopped (the Division's quarterly run).
Breadth: 12 files; 427,262 report versions over 16 quarters from 38,999 accounts; 26,451 status changes; 19,789 worksite rows for about 440 multi-county employers; 14 counties, 95 industries, about 260 payroll agents that no file names; eleven earlier cut-offs to measure on; two files the solution never reads (the 2027 contribution rate notice and the county population estimates).

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, causal-reasoning, missingness-measurement, forecasting, decomposition-attribution, synthesis, synthesis, validation
Question form: what (the best estimate of each county's jobs), with which counties it puts below the line folded into the one question
Nearest build: task5 architecture 3 (this slot's own lineage, differentiated on the card: one step there, nine results here, the two-county shock replaced by a statewide downturn); against other builds, task6 v7 (a flagged set from trace-sampled SLIs) and task1 v2 (an ARR path with drivers) differ in shape, weight and areas, and the abstraction sentence (a period total caught early, completed from four delays each with its own evidence) cannot be written against any build on file.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | an employer subject to the Law for the quarter | liable by the quarter's last day and not ended with effect by its first, on the history by effective or by entered order; accounts that filed; accounts active on the extract date | liable by its last day, not ended by its first | the Act 2(d) and 5(b); no account ends on or before its own liability date, so both orders give one status (asserted) |
| SF2 | December covered employment | month three of the fourth-quarter report; the quarter's average | month three | the Act 2(c) (the payroll period including the twelfth); the published December column reproduces from month three (asserted) |
| SF3 | the records at the close of 15 February | received at or before 23:59:59 that day; the due date | at or before 23:59:59 | the Act 5(a); fewer than 400 reports arrive on 15 or 16 February (asserted, same call) |
| SF4 | a report received twice or amended | the latest version on file; the first | the latest | same call, every county's change in band under the first (asserted) |
| SF5 | an employer with worksites in several counties | its December jobs from the contribution report, split by the worksite report; the worksite report's own counts | split by the worksite report's shares | the agreement, Schedule D (the worksite report distributes the contribution report's employment); the two add up on 99.9 per cent of original reports (asserted) |
| SF6 | a successor account | the successor counts from its transfer, the predecessor ends; both | successor from transfer | the status history (asserted) |
| SF7 | December 2025 | from the same records at the same date; the published table | the same records | the Act 5(a); the published table is the records of 31 May 2026 and reproduces exactly (asserted) |
| SF8 | the change and the line | rounded once to one decimal, minus 2.0 or lower designates; unrounded | rounded once | the Act 4; no county within 0.25 of a point of the line (asserted) |
| SF9 | a report received before its account was established | on file from the account's establishment; from its receipt | from establishment | the agreement, Schedule A (held and posted once the account is established); matters only at earlier cut-offs (asserted) |
| SF10 | the cell of the reporting employers' change | county by supersector in cells of five, ten or twenty (the county otherwise); the supersector statewide; the county alone | ten | the first four are the same call with every figure in band (asserted); the county alone is ruled out by the reporters' change differing by five points or more across supersectors, and designates the same counties (asserted) |
| SF11 | an employer two quarters out | the resolved quarters' share (0.001); nought | the resolved quarters' share | same call (asserted) |
| SF12 | a batch, and whether it arrived | two, three or four reports received in one second; a third, a half or two thirds of its other employers reported | three; a half | same call, every figure in band (asserted) |
| SF13 | the resolved quarters | every quarter with 2 per cent or less of its outstanding jobs unresolved; the earliest or latest left out; 5 per cent | 2 per cent | same call (asserted) |
| SF14 | this quarter's share at employers outstanding on their own, and the share they keep | by supersector and size; by supersector, three-digit industry, county or a hand-picked group of housing industries, with or without size; the share kept pooled or by size, channel or industry group | supersector and size; pooled | same call, every figure in band (asserted) |
| SF15 | a late employer's change | the reporting employers' December on September in its county and supersector; its own December on September a year earlier | the cell | same call, every figure in band (asserted) |
| SF16 | the unregistered employers | developed on fourth-quarter cut-offs or on every cut-off, county by county; shared out by each county's accounts | fourth quarters, by county | the first two are the same call with every figure in band (asserted); sharing out is ruled out by the quarter's registrations departing from account shares by 1.5 times or more, and designates the same counties (asserted) |
| SF17 | the split of an employer whose worksite report is out | each worksite by its own change a year earlier; last December's split | own change | same call, every figure in band (asserted); the latest split as it stands is the hurried route, refuted by the lake worksites' fall in every earlier December and by the reports that came later at the 2024 and 2025 cut-offs (asserted) |
| SF18 | a new account whose first report is out | the mean such accounts turned out to have; this quarter's reporting new employers' mean | the resolved mean | same call (asserted) |
| SF19 | jobs estimated | a county's total less its jobs on reports received (the outstanding and the unregistered together) | total less reported | the Act 5(b) (asserted) |
| SF20 | the replay's footing | every share and count as it stood on 15 February 2026; today's shares on that day's records | that day's | the Act 5(c); both land inside the replay's bands (asserted) |
| SF21 | an employer late every quarter | every report on file for the last four quarters received after its cut-off (two at least); three of the last four | every report | same call (asserted); the two counts are graded together (1,140 to 1,200) and the split banded 15 per cent of the habitual |
| SF22 | what employers outstanding on their own kept | on the resolved quarters, the unresolved left out; on every closed quarter with the unresolved left out, or taken at nought | the resolved quarters | 0.29, 0.35 and 0.27: same call, every figure in band (asserted); the band on the share (0.24 to 0.37) takes in all three and the judge's 0.30 and 0.33 |
| SF23 | the employers in late batches | the reporting employers' change with this quarter's share of employers outstanding on their own carried to them; the reporting employers' change alone | with the share carried | same call, every figure in band (asserted); the carry is the estimate's refinement and is not graded |
| SF24 | the habitually late | carried as the late batches are; at the reporting employers' change | as the late batches | same call, every figure in band (asserted) |
| SF25 | an employer liable for the fourth quarter of 2025 whose report has still not come | nought (36 employers, silent five quarters; two quarters out keep 0.001); its last report carried (about 230 jobs) | nought | same call, every county's change in band under the carry (asserted); the answer blocks state the convention |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | every employing unit with a worker in covered employment on any day of 2026 Q4, reported or not, with an account or not: filed in the Act 2(c), 2(d), 5(b); SF1 |
| 2 Unit of account | the job at a worksite; the county: filed in 2(c); SF2, SF5 |
| 3 Attribution window | December 2026 against December 2025: filed in 4 and 5(a) |
| 4 As-of dating | the records at the close of 15 February 2027 (15 February 2026 for the replay, 31 May 2026 for the published table): filed in 5(a), 5(c) and on the table; SF3, SF9, SF20 |
| 5 Version basis | the latest version on file at the moment: C1 (SF4) |
| 6 Denominator | the county's December 2025 jobs from the same records: filed in 5(a); SF7 |
| 7 Weighting | none: totals over totals; shares within an employer for worksites (SF5) |
| 8 Window length | one month in each year: filed in 2(c) |
| 9 Boundary inclusivity | minus 2.0 or lower designates: filed in 4; SF8 |
| 10 Rounding path | the change rounded once to one decimal; county jobs to the nearest ten, state to the nearest hundred, an employer's to one decimal: filed in 4 and the prompt; SF8 |
| 11 Tie-break | none: a set, no ranking |
| 12 Maturity and censoring | December 2026 incomplete at the cut-off; earlier quarters mature as closures and registrations land: the chain's R2 to R5, banded; SF11 to SF16, SF21 to SF25 |
| 13 Order of operations | versions, then liability, then kinds, then estimates, then worksites, then sums: C1 (asserted on the family) |
| 14 Row order | none: set operations keyed by account and quarter |
| 15 Duplicate resolution | a resubmission once: C1 (SF4) |
| 16 Identity normalisation | the account number without its hyphen; county names to codes; NAICS 2017 and 2022 to supersector: the systems' own keys |
| 17 Netting against gross | a successor's jobs once (SF6); the reconciliation's three items add to the difference exactly |
| 18 Dimensional units | jobs (head count) throughout |
| 19 Code and status semantics | report types ORIGINAL and AMENDED; changes LIABLE, CLOSED, INACTIVATED, TRANSFERRED: the agreement's schedules |
| 20 Integerisation | estimates summed unrounded, stated at the asked rounding; every band at that rounding |
| 21 Clause scope | 5(b)'s whether-or-not clauses govern the population; 5(c) governs the two reports |
| 22 Forward window contents | the certification serves the 2027 fund year; nothing is forecast past December 2026 |

## Literal reader

Executed word for word, the prompt and sections 2, 4 and 5 of the Act file the population (reported or not, with an
account or not), the outcome (the payroll period including the twelfth, at worksites in the county), the line, the
cut-off, December 2025 from the same records, the reconciliation to the published figure and the replay's footing, and
say nothing of how a job not yet on file is estimated, so the literal reader has to estimate three things: what each
outstanding report stands for, the employers with no account, and the split of employers whose worksite report is out.
Every reading in the fork table that estimates them from the files' own closed quarters gives Garrow, Kittredge and
Ostrom with each figure inside its stated range; the readings that stop short (every outstanding report carried alike,
accounts on the register only, the latest worksite split) each fall outside a range and are refuted by a named,
asserted fact in the files (what employers outstanding on their own kept once resolved, against those in late batches;
section 5(b); the lake worksites' fall in every earlier December). The prompt names no file, method or role.

## Prompt contract

The author's voice rewrite may not drop or change: the question (the best estimate the Department can certify of each
county's covered jobs in December 2026 from what was on file on 15 February 2027, and which counties it puts 2.0 per
cent or more below December 2025, for the 2027 Community Transition Fund); "none" staying grammatical for the counties;
the workbook with every county's December 2026 jobs split into those on reports received and those estimated, its
change on December 2025 and the chart of the changes against the line; why the December 2025 state total now on file
differs from the published one; what the same estimate would have given for December 2025 from the files as they stood
on 15 February 2026; the CSV of every liable employer by county with its December 2026 jobs, reported or estimated;
the one-page memo naming the counties and what the estimates rest on; county jobs to the nearest ten, state totals to
the nearest hundred, an employer's to one decimal, changes to one decimal. It may not add: a method, a comparison or an
adjustment (no batch, agent, late filer, imputation, registration, account set-up, season, worksite carry,
back-test), a warning, an attached file's name, who is asking, or a count the data hold (the number of counties,
employers or reports).

## Stage 4

First cut (target.zip sha256 5f5cda294e7b7b52), 2026-11-10. The leak reader found no method sentence, no ranking
file, no helper file and no answer figure, and asked for three realism fixes: the request read as written for the
analyst ("the two things 5(c) asks for", "what you would have told us a year ago"); sixteen government accounts in
Calder shared the name "Calder County"; a private name doubled its suffix ("Co. Co."). All three are fixed in the
generator (the request now says two Board members asked how firm a December figure can be in mid-February; public
bodies take distinct names by county and kind; banks, credit unions, churches and schools carry no corporate suffix).

The determinism judge wrote its own derivation before opening the answer blocks and returned DETERMINISTIC, FIX_NOW,
with four defects in the blocks and a borderline one-fact line. What it found, and what was done:

- Kittredge reproduced the call but not the figure (its best rebuild -2.4 against -2.7, 92 of 96 variants designated,
  0.0 to 0.7 of a point clear of the line), and the call concentrated on carrying seasonal firms by their own
  December on September. The seasonal lake resorts are removed from the world and the step from the method; every
  designated county now sits 0.9 of a point or more below the line across the family, and each band ends 0.7 below it.
- What employers outstanding on their own kept reproduced at 0.25 under the judge's definition (0.27 to 0.32
  accepted). The band took in that definition (every closed quarter, the unresolved at nought: 0.27 here) and ran
  0.25 to 0.32 on the second cut; it is 0.24 to 0.37 after the second pass.
- The developed count of unregistered employers reproduced at 540 employers and 2,150 jobs on every earlier cut-off
  (560 to 620 and 2,300 to 2,600 accepted). That development is a member of the family now and the bands run 500 to
  630 and 2,000 to 2,600; last year's level (3,400) stays outside.
- "The reporting employers' change applied to every outstanding report designates no county" did not reproduce (the
  judge's rebuild with a survival share designated Garrow and Ostrom). Every statement about a rival is now emitted
  from a route the generator runs: three ways of carrying the outstanding reports alike, each with its set.
- "Housing chain", "transmission" and "missing alone" are in no shipped file. The blocks now say construction (the
  concordance's supersector), a batch (three or more reports received in the same second) and outstanding on its own.
- One-fact test borderline (the cause sentence at about 4 of 9). The call now needs the reading by cause in Garrow and
  the worksite split in Kittredge; the cause sentence rescues 1 of 9 on the careful pass, measured.
- The judge's own derivation is the careful pass now (it pooled the outstanding reports and developed the
  registrations, the reverse of what the first cut's careful pass was granted).

Second cut (target.zip sha256 eec3132c67fb5406), 2026-11-10, the one re-judge. The judge's own derivation, written
before it opened the answer blocks, pooled the outstanding reports at one share by supersector and developed the
unregistered employers: it put Ostrom on the line (-2.0), Garrow at -1.4 and Kittredge at -0.6, which is the careful
pass priced here. With the blocks open it returned DETERMINISTIC, FIX_NOW, answer blocks only: the list is forced under
every estimator it built that reads the outstanding reports by cause (Garrow -2.7 to -3.2, Kittredge -2.8 to -3.1,
Ostrom -2.6 to -3.45, Bray nearest at -0.7 to -1.3); stump power strong, three separate pieces of work each flipping
a different county; no change to the pack or the prompt. Reproduced exactly: the published total, the 668 and its
three items, the census, the 3,992, the 1,170, the 219 of 404, the row count, the 7.9 per cent. What it asked for, and
what was done:

- Ranges on county jobs and changes narrower than its rebuild (Bray, Garrow and Ostrom 0.1 to 0.2 of a point and about
  100 jobs outside; the state 200 to 400 jobs above). The floor on every band is half a point now (half a per cent of a
  county's jobs, a fifth of a per cent of the state's), and the family has its choices in it: the late batches without
  this quarter's share carried to them, the habitually late at the reporters' change, the share kept on every closed
  quarter. No band comes within 0.4 of a point of the line.
- The replay outside both ranges (-0.20 to -0.22 and 0.25 to 0.28, its unregistered count running short a year
  earlier). The ranges are -0.30 to 0.20 and up to 0.35; the careful pass's replay (-0.41, 0.47) stays outside.
- What employers outstanding on their own kept: 0.30 pooled and 0.33 on its reading. The range is 0.24 to 0.37.
- Two graded items rested on the author's conventions (the cause counts in the employer list, the construction share
  and the jobs carried to the late batches in a component). The employer list's counts are stated as the file's own
  basis column under conventions it names, with ranges; the carry to the late batches is no longer graded (a sound
  estimate without it stays in every band); the components are the three results every sound estimate has to compute
  (the reading by cause with what each kept, the worksite carry, the unregistered employers); the construction share is
  graded where the prompt asks what the estimates rest on.
- December 2025 as now on file: 36 employers liable for that quarter have still filed no report. The blocks say they
  are counted at nought, and carried at their last report (about 230 jobs) every county's change stays in band (SF25).

The judged cut and the shipped cut differ in the pack by the request email and four legal names (below), and in the
answer blocks by the changes above. The fixes were not judged again: the pipeline's one re-judge is spent, and the
judge asked for no rerun of the pack. The report file for this pass is not in the folder: the agent that writes it
from the thread's verdict stopped on a model safeguard flag (a false positive on its request, by its own message) and
the main thread did not write the report in its place; the verdict it would have filed is the paragraph above, and
the agent can be run again to write `determinism_check_report.md`.

## Pre-ship check

Final cut: target.zip sha256 c238169b094ad50a, golden.zip sha256 d811df74a18cd37c, 2026-11-10.

- Generator: 119 assertions, the independent verifier 14 of 14 on its own code path, two byte-identical builds.
- gates.py: 0 FAIL, 4 WARN, each answered: precut (R2 upstream of five results: see the paragraph under the results
  chain); voice (the shell quota across the last fourteen prompts: the author rewrites the prompt in their own words
  and re-gates it); leak (REVIEW lines below); heart (overuse.weight against task6 v7 and task9 v7, repeat.gate_g
  and repeat.decision against task7 v8: answered in `## Draw`).
- effort.py: quick 7.0, careful but hurried 37.0, thorough 100; the largest hint rescues 1 of 9; five distinct wrong
  sets over eleven shortcuts.
- figures_check.py and audit_containers.py: exit 0 (every number in the answer blocks is in figures.json; every
  container written by the house writers, no two files on one stamp, both zips on each file's own save time).
- leak.py --asof 2027-02-15: REVIEW, no LEAK. Rulings: the rate notice's reserve-ratio band edges (0.0 to 0.9, 1.0 to
  2.9, 3.0 to 4.9, -2.0 to -0.1) coincide with one-decimal changes by chance and state nothing about employment:
  harmless. The Act and the agreement share field nouns with the note (report, quarter, worksite, account): both are
  asserted to name no step of the estimate (checks.py, pins) with positive controls, and three readers found no
  sentence that says how anything not on file is worked out: harmless. The prompt's shell quota: noted, the author
  rewrites it.
- Leak reader: three reads (leak_check_report.md). The last, on the cut before two edits it asked for, found no how
  sentence, no ranking file, no answer figure and nothing planted. The Act's clauses and Schedules A and D stay as the
  filed WHAT (SF1, SF5, SF7, SF9); the agreement's schedules list data elements in prose and pass the describing-content
  sweep; the register's year-first status date is the maintenance system's form, kept as a benign oddity.
- Determinism judge: two passes, both DETERMINISTIC, FIX_NOW (see `## Stage 4`); the second pass's fixes are in the
  answer blocks and were not judged again. No report file for the second pass (see `## Stage 4`).
- Judged cut against shipped cut: the pack differs in two files only: the request email (the deliverables, the section
  5(c) citation, the telephone number and "the Act had thought of that" removed) and four legal names in the account
  register (the state accounts). No graded figure, no governing document and no report, status or worksite row moved
  (generator/figures.json was byte-identical before and after those edits), so the verdict on the pack carries.

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
  missing pool's mix) were banned against task7 v5 and task3 v6 when those registered during the draw; G13 (the horizon
  on which a missing report's outcome lands) is the honest remaining label and carries no structural repeat.
- 2026-11-08, at the draw: the deliverable set csv+pdf crossed the corpus quota (three of nine prompts) when task3 v6 and
  another build took it during the draw; the certification moved to a workbook (csv+xlsx).
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
