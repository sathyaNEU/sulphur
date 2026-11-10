# task5: the counties the Department can certify for the 2027 Community Transition Fund, and the estimate behind them

Architecture 4 (re-rooted 2026-11-10 as a results chain in the same State of Franklin world, at the author's word,
after architecture 3 was returned at review as turning on one thing). Read `## Tried and rejected` first. Every figure
below is measured by `generator/checks.py`, `generator/effort_passes.py` or `generator/golden.py` on the cut pack.

## Draw

Subdomain: Survey Research & Official Statistics (Other), census, register and administrative-data quality
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a reconciled table plus findings (each county's December 2026 covered jobs split into reported and estimated, its change on December 2025, reconciled to the published 2025 total and replayed on December 2025; the counties to designate on top)
Weight: a hard-to-measure quantity: the December jobs the files do not yet hold (employers whose report is out, employers with no account yet, worksite splits not yet in); task7 sits on modeling, task4 on measurement, task1 on synthesis; task6 (four cards back) also sits on a hard-to-measure quantity, a trace-sampled SLI, which shares nothing with a census caught early, so the guard's overuse WARN is answered here
Data-native sentence: forty-five days after the quarter the Division's files run behind the employment they record in four different ways at once (reports in agents' late batches, reports that will never come, accounts not yet set up, worksite reports trailing the contribution reports), each with its own evidence in the closed quarters, and the 2026 housing downturn makes this quarter unlike those closed quarters.
People: Danielle Fuller, director of the Labor Market Information section; Matthew Cox, the Department of Commerce's administrator for the Fund; William Robertson, chief of the Unemployment Insurance Tax Division (`guard.py names --geo "United States" --seed 501` and `--geo US --n 4 --seed 50327`, kept from architecture 3). None appears in the prompt.

Card `.claude/skills/fingerprint/cards/task5.json`, architecture v4, registered 2026-11-10: WARN only (overuse.weight
against task6 v7, answered above; repeat.gate_g and repeat.decision against task7 v8: that build picks measures under
a grant-per-tonne limit from a lottery, this one certifies a census caught early, and the two share no result). The
decisive generator was redrawn from G13 (banned against task1 v2) to G3, record against operation, which is the
honester label for a chain whose every result completes a record the operation has run ahead of. The forum was redrawn
from committee_or_panel (task7 v8 in the window) to minister_or_cabinet: the estimate is prepared for the Commissioner
of Labor's certification, due by statute on 1 March; the Board's designation follows it mechanically.

## Deep reasoning

Task type: census-register-administrative-data-quality in Survey Research & Official Statistics, which serves Data Extraction & Conformation: an official covered-employment statistic conformed from an administrative report census caught 45 days after the quarter, with the part not yet on file estimated component by component and the result reconciled to the published table and to the later records.
Domain test: every result is a quantity an official statistics office produces for an early estimate from an administrative census: the response status of the census at the cut-off, a nonresponse mechanism and the nonrespondents' outcome on resolved cohorts, a coverage adjustment for units not yet on the frame, an allocation of multi-establishment employers to areas, a revision analysis against the published figure and a replay against the later records; the field's delinquent-report imputation is the textbook and sits in the hurried column.
Swap: "which regions' December inpatient days fell 2.0 per cent, on the best estimate from the hospital returns on file on 15 February" keeps a threshold and late returns, but no hospital stops filing because it has closed, no account is set up weeks after a unit starts trading, no payroll agent files a batch, no worksite report distributes a total and nothing is inactivated two quarters later, so six of the nine results have nothing to estimate and the call stops making sense.
Where the weight sits: the jobs not yet on file (R2 to R5): 48,200 of the state's 456,300 December jobs are estimated, and each of the four parts needs its own reconstruction across files and quarters (transmissions rebuilt from receipt seconds and followed from quarter to quarter; outcomes read on cohorts old enough to have resolved; this quarter's trouble rate measured where it shows and carried to where it does not; registrations developed from this quarter's early count; each worksite carried by its own season). The work is long, not clever: none of the four is found by one look and each has a cruder version that validates on a normal year.
Layer 1: amended reports superseding originals, a few of them audit corrections months later, and exact resubmissions seconds apart (the Division's filing system); reports received on paper keyed by date with no time (the mail room); account numbers hyphenated with a check digit in the register and as digits in the worksite file, county codes in the register and upper-cased county names in the worksite file (two systems); NAICS 2017 codes on older accounts beside NAICS 2022 (the register's history); successor accounts after a transfer of business, the predecessor ended (account maintenance); seasonal lake resorts with near-empty Decembers; habitual late filers; worksite reports whose months do not add to an amended contribution report; reports held for accounts not yet established and posted later with their receipt time. Each is asserted neutral (R2 block, SF4, SF6) and none decides a result.
Not one thing: the strongest single piece (reading an employer missing from a transmission that arrived as in trouble) is granted to the careful pass, and a run that nails it still loses the late transmissions' jobs this quarter (R3), the employers with no account (R4), the worksite split (R5), eleven or more county figures (R6, R7) and Kittredge (R8). Three judgments each move the designated set on their own: without the cause-by-cause reading no county reaches the line, with the latest worksite reports' split Kittredge reads -1.9 and stays out, and with last year's unregistered jobs carried flat and the latest split Kittredge reads -0.9.
One-fact test: the most useful single sentence (employers missing alone hold several times their usual share of the housing chain's jobs this quarter, in the late transmissions as in the ones that arrived) rescues 1 of 9 results on the careful pass (R3); the sentence about accounts set up after the cut-off rescues 1 (R4) and the worksite sentence 1 (R5); none rescues the county figures, which need all three (effort.py, hints executed on the careful pass).
Not semantics: every field read right (receipt times to the second, report types, the two dates on each account, the status history's effective and entered dates, the worksite reports' dates received, the Act's population) gives a correct census of who has and has not reported and which accounts exist, and still leaves a careful run carrying the late transmissions at their reporting peers' change, the unregistered jobs at last year's level and the worksites at their latest split: nothing filed says what an outstanding report means, how many employers have no account yet or how a worksite's share moves with the season.
Not rule application: the Act files the population (every employer subject to the Law, reported or not, with an account or not), the outcome, the line, the cut-off, the base and the two reports it wants (the published figure reconciled, the replay), and the agreement describes fields; no filed sentence says how an outstanding report, an employer with no account or a missing worksite report is estimated, and once every filed rule is applied all 48,200 estimated jobs are still to be judged.
Estimand: sections 2(c), 2(d), 4 and 5(a) to 5(c) of community_transition_fund_act_2026.docx: population every employing unit with a worker in covered employment on any day of the fourth quarter of 2026, whether or not its report has been received and whether or not an account has been established; outcome workers on the payroll for the pay period including 12 December at worksites in the county; window December 2026 against December 2025; unit jobs by county; comparison December 2025 from the same records at the same date (not the published table); threshold minus 2.0 per cent or lower after rounding to one decimal; the records as they stand at the close of 15 February 2027; the replay from the records as they stood at the close of 15 February 2026. ui_lmi_data_sharing_agreement_2025.docx defines every field, says a report counts from its account's establishment and that the worksite report distributes the contribution report's employment.
No decoy: nothing is written to carry a wrong answer: no memo, draft, flash or stakeholder figure for December 2026 ships; the request quotes no figure; the published fourth-quarter 2025 table is correct on its own footing (reports posted through 31 May 2026) and reproduces from the records of that day (SF7).
No replay: no result re-derives a published figure: the reconciliation explains why the records now differ from the published table (three exact items, nothing unexplained) and no stated number is wrong.
Pinned: every rival is run on the cut pack (checks.py, 101 assertions; verify.py recomputes every graded figure on its own code path): 22 members of the standing family (a transmission as two, three or four reports in a second; arrived at a third, a half or two thirds; this quarter's trouble by housing chain, supersector or three-digit industry, with or without size; the resolved quarters with the earliest or latest left out; the missing-alone share by size, channel or chain; seasonal at 0.5, 0.6 or 0.7; the reporters' change in cells of five, ten or twenty) designate Garrow, Kittredge and Ostrom with every county's change within 0.3 of a point of the golden's and inside its band; four variants are ruled out by named facts and designate the same three anyway (unregistered employers pooled over every earlier cut-off: the fourth-quarter ratio is higher than any other quarter's in every year; shared out by each county's accounts: the quarter's registrations depart from the counties' account shares by a factor of 1.5 or more; the reporters' change by supersector statewide or by county alone: it differs by five points or more across supersectors); last December's worksite split lands inside every band (SF17).
Run forecast: R1, R2 and R9 earned (hygiene, a pattern the receipt seconds show, a replay on a normal year); R3 lost to a method shortcut (late transmissions at the reporting employers' change, the survivors' change); R4 lost to an unfinished chain (the Act's population read, last year's unregistered jobs carried as they were: 3,500 against 2,500) or dismissed as not estimable; R5 lost to a method shortcut (the latest worksite report's split); R6 and R7 lost in nine or more counties; R8 Partly (Garrow and Ostrom, Kittredge out). A run that catches one of R3 to R5 loses the other two in different counties.
Strategy label: WORKS IN FORM (outcomes that have not finished happening: completion differs by a unit no pooled factor captures, here the cause of each outstanding report, this quarter's trouble rate, this quarter's registrations and each worksite's season); the dead form, the field's delinquent-report imputation as the golden, is the textbook route and designates no county once the rest is right.
Depth level: 5. Six judgments each move a graded figure on their own (the cause of an outstanding report, the resolved quarters, this quarter's trouble carried to the late transmissions, the count and the size of the unregistered employers, the worksite carry, the replay's footing), three of them move the designated set, and effort.json records four distinct wrong sets over thirteen shortcuts (all fourteen counties, Ostrom alone, Garrow and Ostrom, none).
Lesson: an early estimate from an administrative census is completed component by component, each from the evidence of its own delay: a report's absence means what its usual companions' arrival says it means, a closed quarter tells what the missing kept only once its closures are recorded, this quarter's closure rate has to be read where it shows before the closed quarters' rate is lent to the units whose standing does not show, the units not yet registered are counted from this quarter's early registrations, and a total is split among places by each place's own season; a crude version of each validates on a normal year. No build on file teaches an estimate assembled from several delays at once.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the census at the cut-off (27,897 liable accounts, 20,777 reports received, 7,120 outstanding) and December 2025 now on file (455,880) against the published 455,161: 202 on late reports, 516 on accounts established since, 1 on amendments | assembly and reconciliation | the Act 2(d) and 5(a); the register's two dates, the status history's effective and entered dates, received_at; the published table's own footing (reports posted through 31 May 2026) | exact | earned by a careful run; the quick pass is a method shortcut (the register's active accounts, the published table taken as the base, the difference left as one lump) | - | Ask 6 |
| R2 | the outstanding reports by what their absence means: 4,844 in transmissions not yet received, 846 missing alone or late for the first time, 334 late every quarter, 999 two quarters out, 97 new accounts; the missing-alone kept 0.30 of September on the resolved quarters | missingness and measurement | received_at to the second across quarters; the resolved quarters' late reports, closures and inactivations | counts within 2 per cent (4,740 to 4,950; 820 to 870); 0.27 to 0.32 | earned by a careful run (the receipt seconds show the transmissions); the quick pass stops at the first story, every outstanding report read alike | R1 | Component 4 |
| R3 | this quarter's trouble carried to the late transmissions: about 530 fewer December jobs than the reporting employers' change gives; housing-chain employers at 0.86 of September | causal reasoning (transport) | this quarter's share of jobs at employers missing alone among employers whose standing shows (3.7 per cent in the housing chain against 0.4 to 0.6 at earlier fourth-quarter cut-offs), by chain and size | 250 to 600 jobs; 0.85 to 0.88 | method shortcut: the reporting employers' change, which is a survivors' change (0.89, nought fewer jobs) | R2 | Component 1 |
| R4 | the employers liable for the quarter with no account yet: about 590 employers, 2,500 December jobs | missingness and measurement (immature cohort) | the Act 2(d) and 5(b); the register's liability and establishment dates at this and earlier fourth-quarter cut-offs; late registrants' later reports | 560 to 620 employers; 2,300 to 2,600 jobs | unfinished chain: the population read and last year's unregistered jobs carried as they were (840 employers, 3,500 jobs), or left out as not estimable | independent: the register's liability and establishment dates | Component 2 |
| R5 | the county split of the 159 multi-county employers whose worksite report is out: about 100 fewer jobs in Kittredge, 190 fewer in Talcott and 160 fewer in Sayre than the latest reports' split | forecasting (each worksite's seasonal carry) | the worksite reports and their dates received; each worksite's own change between the same two quarters a year earlier; the reports that came in later at earlier cut-offs | 80 to 120; 170 to 210; 140 to 180 | method shortcut: the latest worksite report's split as it stands | independent: the worksite reports and their dates received | Component 3 |
| R6 | each county's December 2026 jobs and the part estimated (fourteen counties and the state: 456,300, of which 48,200 estimated) | decomposition and attribution (reported plus estimated reconciles to the total) | the Act 5(a) and 5(b); R2 to R5 carried through every employer and worksite | each county within its family range (20 to 190 jobs wide) | unfinished chain: eight or more counties outside their ranges on the careful pass | R2, R3, R4, R5 | Ask 2 |
| R7 | each county's change on December 2025 (Garrow -3.1, Ostrom -2.9, Kittredge -2.7, Bray -1.0 nearest; state +0.1) | synthesis | the Act 4 and 5(a): December 2025 from the same records at the same date | each county within 0.1 to 0.2 of a point | unfinished chain: nine or more counties outside their ranges (Kittredge -0.9, Talcott 2.8, Sayre 3.3 on the careful pass) | R6 | Ask 4 |
| R8 | designate Garrow, Kittredge and Ostrom | synthesis | the Act 4 | exact set | unfinished chain: Garrow and Ostrom on the careful pass; no county with every outstanding report at the reporters' change | R7 | Recommendation |
| R9 | the same estimate replayed on December 2025 from the records of 15 February 2026: -0.12 per cent from the state figure now on file, 0.37 per cent for the average county | validation | the Act 5(c); every date in the four extracts | -0.20 to 0.00; 0.30 to 0.45 | earned by a careful run on a normal year; the quick pass has no replay, and the estimate without the unregistered employers replays 0.9 per cent low (dismissed own evidence when that miss is seen and set aside) | R2, R4, R5 | Ask 7 |

R2 sits upstream of five results (precut's WARN), and it is the one judgment granted to the careful pass: each of the five needs work of its own beyond it (R3 this quarter's rate, R6 to R8 the unregistered employers and the worksite split as well, R9 the as-of footing), and the largest single hint rescues 1 of 9.

Carry-forward: R1 stands on the filed population and the dates; R4 and R5 stand on inputs of their own (the register's two dates; the worksite reports and their dates received) and are graded whatever a run did with the outstanding reports; R3 falls with R2; R6 falls with any of R2 to R5, county by county (a run that misses only the worksite split loses four counties, one that misses only the unregistered employers loses all fourteen by 0.3 to 0.8 of a point); R7 and R8 fall with R6; R9 falls with R2, R4 or R5 where the miss shows on a normal year (R4 does, R3 does not). No analytical result is the only analytical input of more than one other.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a report missing from a transmission that arrived marks an employer in trouble | constructed by simulating how payroll agents and employers file | no: 846 employers at this cut-off in every county (5 or more each), 250 to 350 at each of eleven earlier cut-offs; the misreading (carried at the reporters' change) moves all fourteen counties by 0.5 to 1.3 of a point and decides three | modelling: transmissions rebuilt from receipt seconds, followed from quarter to quarter, then outcomes on resolved quarters | modelling: an outcome measured on cohorts old enough for closures to be recorded | keep: granted to the careful pass |
| the 2026 housing downturn: trouble in the housing chain at several times its usual rate | constructed as an economic process ramping through 2026, with county-to-county noise | no: every county carries it by its industry mix (housing-chain employers missing alone in all fourteen, two thirds of them outside the designated counties), and it shows in the reported jobs too | a targeted query once the outstanding are read by cause (the missing-alone share by industry, this quarter against earlier fourth quarters) | modelling: this quarter's rate, measured where standing shows, carried to the late transmissions by chain and size | keep: one result (R3), moves no designation |
| accounts established weeks after liability begins | constructed by simulating the Division's registration (employers that register promptly, with their first report, or only when found) | no: every county (15 or more jobs each) and every earlier cut-off (150 or more accounts each); leaving them out misreads all fourteen counties by 0.3 to 0.8 of a point and flips none | a targeted query on the register's two dates, which the Act's population asks for | modelling: a development estimate (this quarter's registrations so far, earlier fourth quarters' delays, late registrants' size; last year's level and the registered employers' size each overstate by 40 per cent or more) | keep: one result (R4) |
| worksites with their own seasons, and worksite reports that trail the contribution reports | constructed by simulating multi-county employers (lake, North Woods and metro worksites; worksites opening and closing) | no: the latest split misplaces 60 jobs or more in five counties (Talcott and Sayre, where nothing turns, as well as Kittredge) and did so at the 2024 and 2025 fourth-quarter cut-offs | a targeted query (a worksite's months across quarters), or the split checked against the report that came later | modelling: a per-worksite seasonal carry normalised to the employer's December jobs; last December's split fails on worksites opened and closed since | keep: one result (R5), decides Kittredge only together with R2 and R4 |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the census at the cut-off and December 2025 against the published total | Missed | Right | Right |
| R2 the outstanding reports by cause, and what the missing-alone keep | Missed | Right | Right |
| R3 this quarter's trouble carried to the late transmissions (jobs) | Missed | Missed | Right |
| R4 the employers with no account yet | Missed | Missed | Right |
| R5 the worksite split against the latest reports' (jobs by county) | Missed | Missed | Right |
| R6 each county's December 2026 jobs | Missed | Missed | Right |
| R7 each county's change on December 2025 | Missed | Missed | Right |
| R8 the counties to designate | Missed | Partly | Right |
| R9 the replay on December 2025 | Missed | Right | Right |
| Roughly | 0 of 9 | 3.5 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (generator/effort_passes.py runs each pass end to end on the cut pack; no cell is hand-graded)
Largest single hint: employers missing alone hold several times their usual share of the housing chain's jobs this quarter, in the late transmissions as in the ones that arrived; rescues 1 of 9 results
Pair estimate: 47.5

The careful column is calibrated up: it is granted the transmissions and the resolved-quarter outcome (the receipt
seconds show the first and frontier runs handle unresolved cohorts), an exact reconciliation and a correct replay, and
it adds the unregistered employers crudely rather than leaving them out. What it does not do is the move beyond each
reflex: it carries the late transmissions at the survivors' change, last year's unregistered jobs as they were and the
latest worksite split. If it left the unregistered employers out altogether it would land the designated set by
offsetting errors (Kittredge 0.5 too low from the missing employers, 0.9 too high from the split) while every county
figure and the replay went wrong; `effort.json` carries that route as a shortcut. The paper is optimistic: a run that
also carries each worksite's season keeps Kittredge and the Lakes counties and scores near 60.

## Data provenance

Source: generated by task5/generator from a simulated process (sim.py, pack.py, docs.py), seed 50427; the NAICS code titles are the Census Bureau's own classification, everything else is invented.
Behaves like the real thing: the generator simulates how a state unemployment insurance tax division's files come to exist: about 40,000 employers with monthly jobs (trend, industry seasonality, noise), payroll agents that send their clients' reports in one transmission, the same agents swamped every January, employers in trouble that stop filing and are inactivated two quarters later, ordinary closures with a final report, new employers that register promptly, with their first report or only when found, examiners who set up accounts weeks later, worksite reports that trail the contribution reports, worksites with their own seasons that open and close, amendments, resubmissions, paper reports, successors, and a published table cut on its own date; this matches how QCEW source files behave (delinquent reports, late account set-up, multiple worksite reports).
Genuine patterns: (1) industry seasonality by supersector and summer-seasonal lake resorts; (2) county trends and month-to-month noise scaling with size; (3) year-end lateness concentrated in the same agents every fourth quarter; (4) a business cycle in the housing chain through 2026 (survivors shedding jobs, trouble several times its usual rate, fewer start-ups) with county-to-county noise; (5) hazard of trouble falling with employer size; (6) registration delay by how an employer registers, late registrants smaller; (7) worksite seasons by region and industry (lake summer trade, North Woods winter recreation and outdoor work, metro holiday retail) and worksite turnover higher in project industries; (8) births, ordinary closures and transfers every quarter.
Problems by process: amendments weeks or months after the original (corrections and audits), resubmissions seconds apart (the filing system), paper reports keyed by date (the mail room), two account-number formats and two county formats (two systems), NAICS 2017 codes on old accounts (the register's history), reports held until an account is established (registration), worksite reports that do not add to an amended report (two filings), accounts inactivated months after the employer stopped (the Division's quarterly run).
Breadth: 12 files; 429,471 report versions over 16 quarters from 39,227 accounts; 26,803 status changes; 17,944 worksite rows for 400 multi-county employers; 14 counties, 95 industries, about 260 payroll agents that no file names; eleven earlier cut-offs to measure on; two files the solution never reads (the 2027 contribution rate notice and the county population estimates).

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
| SF10 | the cell of the reporting employers' change | county by supersector in cells of five, ten or twenty, the county otherwise | ten | same call, every figure in band (asserted) |
| SF11 | an employer two quarters out | the resolved quarters' share (0.001); nought | the resolved quarters' share | same call (asserted) |
| SF12 | a transmission, and whether it arrived | two, three or four electronic reports in one second; a third, a half or two thirds of its other reports in | three; a half | same call, every figure in band (asserted) |
| SF13 | the resolved quarters | every quarter with 2 per cent or less of its outstanding jobs unresolved; the earliest or latest left out; 5 per cent | 2 per cent | same call (asserted) |
| SF14 | this quarter's trouble, and the missing-alone share | by housing chain and size; by supersector, three-digit industry or county with or without size; the share pooled or by size, channel or chain | chain and size; pooled | same call, every figure in band (asserted) |
| SF15 | a seasonal business | its own December under 0.5, 0.6 or 0.7 of its September in both earlier years | 0.6 | same call (asserted) |
| SF16 | the unregistered employers | from fourth-quarter cut-offs, county by county; pooled over every cut-off; shared out by each county's accounts | fourth quarters, by county | the fourth-quarter ratio is higher than any other quarter's every year, and the quarter's registrations depart from account shares by 1.5 times or more (both asserted); both variants designate the same counties |
| SF17 | the split of an employer whose worksite report is out | each worksite by its own change a year earlier; last December's split | own change | last December's split lands in every band and designates the same counties (asserted); the latest split as it stands is the hurried route, refuted by the reports that came later at the 2024 and 2025 cut-offs (asserted) |
| SF18 | a new account whose first report is out | the mean such accounts turned out to have; this quarter's reporting new employers' mean | the resolved mean | same call (asserted) |
| SF19 | jobs estimated | a county's total less its jobs on reports received (the outstanding and the unregistered together) | total less reported | the Act 5(b) (asserted) |
| SF20 | the replay's footing | every share and count as it stood on 15 February 2026; today's shares on that day's records | that day's | the Act 5(c); both land inside the replay's bands (asserted) |

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
| 12 Maturity and censoring | December 2026 incomplete at the cut-off; earlier quarters mature as closures and registrations land: the chain's R2 to R5, banded; SF11 to SF16 |
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
say nothing of how a job not yet on file is estimated, so the literal reader has to estimate four things: what each
outstanding report stands for, the employers with no account, and the split of employers whose worksite report is out.
Every reading in the fork table that estimates them from the files' own closed quarters gives Garrow, Kittredge and
Ostrom with each figure inside its stated range; the readings that stop short (every outstanding report at the
reporters' change, accounts on the register only, the latest worksite split) each fall outside a range and are refuted
by a named, asserted fact in the files (what the missing-alone kept once resolved; section 5(b); the worksite reports
that came later). The prompt names no file, method or role.

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
adjustment (no transmission, agent, late filer, imputation, registration, account set-up, season, worksite carry,
back-test), a warning, an attached file's name, who is asking, or a count the data hold (the number of counties,
employers or reports).

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
