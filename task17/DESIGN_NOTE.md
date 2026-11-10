# task17: how many node-hours the Landesrechenzentrum Ravensfeld commits to the 2027 GPU allocation round

## Draw

Subdomain: Resampling, simulation & Monte Carlo methods (General Statistics & Data Science, `resampling-simulation-monte-carlo-methods`)
Analysis type: Descriptive & Distribution Analysis
Answer shape: A distribution and where it is cut (the distribution of the GPU node-hours the gpu partition can deliver over the 2027 allocation year while meeting its service level, cut at the 80 per cent confidence the allocation policy sets, against the node-hours the 2027 round requests)
Weight: modeling: a discrete-event simulation of the partition under its filed scheduling policy is only as good as the four fitted inputs it runs on (a cluster arrival process, a censored duration model whose tail is chosen on a change in the limit, a repairable-fleet outage process with common-cause clusters and repair times, a rework fraction built from two of them), each a model with several parameters that take a sequence of steps to estimate; task16 sits on investigation, task10 on validation, task4 on measurement
Data-native sentence: the scheduler's accounting log records what the queue did (submit, eligible, start and end times per job segment, the state it ended in, the limit it ran under), the node event log records when each node was unavailable and the operator's reason, the rack layout says which nodes share a switch and a power feed, the allocations say what each project was granted and used and the configuration history says what limit each job was killed at, so every input the simulation of the allocation year needs (how granted hours turn into submissions and how those cluster, how long jobs would run under a limit never yet applied, how outages cluster and how long they last, how much work a failure throws away) has to be rebuilt from a different pair of files before the partition's deliverable total means anything.
People: Francesca Winkler (director of the centre, puts the round's cap to the centre's board), Mehdi Renner (HPC systems analyst, whose workbook and note the golden are), Carolin Hofig (chair of the allocation committee, signs the round's call) (`guard.py names --geo DE --seed 1610`). None appears in the prompt.

Architecture 1, drawn 2026-11-10. Guard: WARN only (overuse.objective forecasting 6 of 12, the assigned type; repeat.gate_g
method_or_model_selection against task7 v8; repeat.deliverables docx and xlsx, the board takes a workbook and a note).
Nearest drivers under 0.10; differentiated on the card against task10's spent v1 (one censored capacity) and mark132
(a wear-out spares forecast). `slots` on the mechanism nouns (queue, scheduler, walltime, checkpoint, preemption) and on
the setting nouns (simulation, Monte Carlo, censored durations, availability, repair) returns no earlier use.

The world. The Landesrechenzentrum Ravensfeld, a state research computing centre serving the state's universities, runs
a shared GPU partition (`gpu`) under a batch scheduler: 64 nodes, each allocated whole to one job, jobs requesting one
to eight nodes, two qualities of service (`normal`, limit 24 hours until 3 May 2026 and 48 hours since; `short`, 4
hours). Projects apply each December for node-hour grants for the coming year and draw on them as they submit; the
allocation policy (version 3, 2025) holds the partition to a 90th-percentile queue wait of at most four hours over the
allocation year's jobs and caps the round's grants at the total whose expected use, from the projects' own records,
meets that level with at least 80 per cent probability. The 2027 partition plan raises the `normal` limit to 96 hours
from 1 April 2027. The 2027 round's requests exceed any plausible cap, so the committee cuts them pro rata to the cap.
The board meets on 14 December 2026. The exports are cut at 15 November 2026.

## Deep reasoning

Task type: resampling-simulation-monte-carlo-methods (Resampling, simulation & Monte Carlo methods), serving Descriptive & Distribution Analysis: where the partition's deliverable total really sits once the duration tail under a raised limit, the outages that cluster, the work thrown away after failures and the queue's own variance are handled, read off a simulation whose inputs are four fitted stochastic models and reported as a distribution cut at a stated confidence.
Domain test: every result is a Monte Carlo object of this subdomain: a fitted cluster (session) arrival process with its burst structure; a censored duration model whose tail family is chosen by validating on a natural change in the censoring limit; a repairable-fleet outage process with common-cause clusters and class-specific repair times; a rework fraction built as a function of two of those models; a discrete-event simulation under a filed policy, validated on a held-out quarter; and a required-capacity distribution cut at 80 per cent.
Swap: "cap the 2027 grants at 318,000 node-hours so the 90th-percentile queue wait stays under four hours" with hospital nouns ("cap next year's elective bookings at 318,000 bed-days so the 90th-percentile admission wait stays under four hours") loses the scheduler's backfill on requested walltimes, a run-time limit the plan raises, the requeue of a job after a node failure with the work since its last checkpoint thrown away, and rack-level outages that take eight nodes down together; the call stops making sense.
Where the weight sits: modeling: four fitted inputs, each with several parameters reached through a sequence of steps (R2: the sessions' cluster structure, the pattern and the realised use of grants by project age and type; R3: the duration family under censoring, chosen by what each predicted for the 24 to 48 hour mass when fitted on jobs censored at 24 hours; R4: the outage process by rack and class with its repair times and the uptime hazard; R5: the rework fraction as a function of R3 and R4), plugged into one simulation under the filed policy, which then has to reproduce the third quarter of 2026 (R6) before the allocation year is read as a distribution cut at 80 per cent (R7).
Layer 1: job ids that roll over when the scheduler's counter wraps (the same id for two jobs two years apart; the submit time tells them apart); requeued jobs logged as several segments of one job, one row per start, with a restart count; submit and eligible times in UTC and start and end times in local time across the summer-time changes (the export's two systems); node lists as compressed ranges; time limits as day-hour strings; state codes with suffixes (`CANCELLED by 20311`); node event reasons typed freely by operators with variants of one cause; one month's accounting rows exported twice by a re-run job; node event intervals cut in two by scheduler restarts. Each is produced by the system that writes the file, handled alike by every careful run, and asserted neutral on every graded figure except R1, which grades the assembly.
Not one thing: seven results, four fitted inputs each from its own pair of files; the strongest single piece (the duration tail under the raised limit) moves R3 and about two nodes of R7, and a run that nails it still has to keep the sessions' bursts (R2), model the outages as clustered with repair times (R4), price the rework (R5), reproduce the 2026 quarter (R6) and carry the inputs' error into the cut (R7).
One-fact test: the most useful sentence is "the plan raises the limit to 96 hours, so the duration tail beyond 48 hours has to be extrapolated from the families that predicted the 24 to 48 hour mass"; it rescues R3 and moves R7 by about two nodes without landing it, 1 of 7 results.
Not semantics: every field read correctly (queue wait from eligible to start, the year by eligibility, the 90th percentile, nodes allocated whole, the limits by date, the plan's 96 hours, grants and their use) still leaves each hurried input wrong: nothing says how granted hours turn into submissions and how those cluster, which duration family extrapolates, that failures cluster by rack and take days to repair, or how much work a failure throws away.
Not rule application: the scheduler configuration files the policy the simulation runs (first come first served by eligible time, backfill on requested walltime, whole nodes) and the allocation policy files the WHAT (the wait, the percentile, the window, the 80 per cent rule, grants capped at the total whose expected use meets the level); no document names a process, a family, an outage model or a rework estimate; the plan's own capacity line ("the partition's node-hours must cover the expected use of the round's grants") is the quick pass's arithmetic and names no cap.
Estimand: allocation policy 2 and 3 (queue wait from a job's eligible time to its start; the 90th percentile over the gpu partition's jobs that became eligible in the window; the window the allocation year, 1 January to 31 December 2027; the round's grants capped at the total whose expected use, from the projects' records, meets the level with at least 80 per cent probability; requests above the cap cut pro rata); the scheduler configuration (the policy the queue runs under, the limits by date, the plan's 96 hours from 1 April 2027); the prompt (the cap in node-hours to the nearest 1,000, the cut as a share of the requests; the rounding).
No decoy: the capacity report states each week's utilisation, node-days lost and 50th and 90th-percentile waits correctly on the policy's definitions and ranks nothing; the plan's node-hours line is arithmetic on filed grants, not a cap; no memo argues a figure.
No replay: no result re-derives a published figure; the capacity report's Q3 2026 figures are the backtest's target (R6) and the assembly's control total (R1), graded against the solver's own rebuild.
Pinned: rivals run on the clean truth in `generator/passes.py`: sessions fitted as a cluster process or resampled by day within weekday and term; the tail as log-logistic, generalised gamma or a two-component lognormal mixture, each validated on the 24 to 48 hour window; outages as a marked cluster process by rack or as a compound process by class with the common-cause events drawn by rack; rework by project class or pooled with the no-checkpoint share; backfill as EASY or conservative; the cut read from 2,000 or 4,000 simulated futures with or without the inputs redrawn from their sampling error: each lands inside its result's band (the Results chain), and the hurried routes outside by the margins stated.
Run forecast: R1 earned; R2 Partly (method shortcut: Poisson submissions at the hourly mean, the node-hours right and the burst structure lost); R3 lost to a self-confirming check (families compared on their in-sample fit to jobs censored at 48 hours, or the tail cut at 48); R4 Partly (narrow look at broad data: the node-days lost right on average, the rack-level clusters and the repair times missed, availability carried as a constant); R5 lost to an unfinished chain (requeues seen in the log, the lost work never priced); R6 lost to dismissed own evidence (the backtest under-predicts the 2026 quarter and is explained away); R7 lost (the count at the cut too low by every shortcut, each by a different number of nodes).
Strategy label: WORKS IN FORM (Simulation checked out of sample: the system simulated and the model chosen by back-testing on a held-out quarter; Forecasts and regime breaks: the limit's change dated in the configuration history and the family that wins on it; Persistence: failures that cluster, counted as episodes).
Depth level: 5. Five independent judgments each move the cap (the realised use of grants with its burst structure, the duration tail, the clustered outages with repair times, the rework, the inputs' error in the cut); the shortcuts land on different caps (node-hours arithmetic about 450,000, every shortcut together about 380,000, no rework about 340,000, constant availability about 345,000, no tail about 350,000, Poisson about 355,000, against about 318,000), and the cap holds across the rivals' sweep.
Lesson: the capacity a queue can deliver at a service level is a simulation fed by several fitted processes, each on its own record and each with its own validation; the arithmetic of hours available, and every input that understates the queue's variance or its load, lands the deliverable total high in a different way.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the Q3 2026 job record rebuilt: jobs eligible in the quarter (about 14,800, nearest 10) and their node-hours used (about 118,000, nearest 1,000), reconciled to the capacity report | assembly and reconciliation | policy 2 (a job counted once, wait from eligible time, node-hours as nodes times elapsed); the capacity report's quarterly totals | exact at the rounding (a measured count) | method shortcut: segments counted as jobs and rolled-over ids merged (about 16,300 jobs), the duplicated month counted twice | - | Ask 5 |
| R2 | the realised use of 2024 to 2026 grants by project age (first-year projects about 52 per cent, continuing about 71 per cent, nearest per cent), the burst index of 2026's hourly submissions (variance to mean, about 6, nearest whole number), and the 2027 round's expected use at its requests (node-hours, nearest 10,000) | modeling | the allocations 2024 to 2027 and the job log's node-hours by project and month; the sessions by project, weekday and term | the use ratios within one point (measured); the burst index one of two adjacent integers; the expected use within one step of 10,000 | method shortcut: grants read as use (100 per cent) or one pooled ratio (about 65), Poisson submissions at the hourly mean (burst index 1) | - | Ask 3, Component 1 |
| R3 | the mean run time of a `normal` job under the plan's 96 hour limit (about 12 hours, nearest hour) and the share of `normal` work beyond 48 hours (about 10 per cent, nearest 5 per cent) | missingness and measurement | the configuration history (24 hours to 3 May 2026, 48 since, 96 from April 2027); the job log censored at each job's limit; the families' prediction of the 24 to 48 hour mass on the pre-May jobs | the families that pass the 24 to 48 hour validation land in one bin at each rounding (asserted) | self-confirming check: the families compared on how closely each matches the jobs below the 48 hour limit, which every family matches, so the thinnest tail is kept (Weibull, about 10.6 hours, 5 per cent), or the tail cut at 48 hours (10.4, 0); the move beyond is reading the May 2026 limit change as the test of each family's tail | - | Ask 4, Component 2 |
| R4 | the 2026 outage record: node-days lost per quarter (about 190, nearest 10), the share lost in events taking four or more nodes at once (about 45 per cent, nearest 5 per cent), and the median repair time by class (software reboot about 0.9 hours, nearest 0.1; hardware replacement about 4.6 days, nearest 0.5; rack events about 19 hours, nearest hour) | investigation loops | the node event log joined to the rack layout; the capacity report's weekly node-days lost | exact at the rounding (measured from the log once intervals cut by scheduler restarts are rejoined) | narrow look at broad data: availability carried as a constant 94 per cent, so no share and no repair times are produced; a run that reads the log earns the figures and still has to carry the clusters and repair times into the simulation (R6, R7) | - | Ask 6, Component 3 |
| R5 | the node-hours redone after node failures in 2026 as a share of node-hours used (about 6 per cent, nearest per cent), from requeued jobs' segments against like jobs that ran through, by each project's checkpointing | modeling | the requeued jobs' segments; the durations by class (R3); the failures (R4) | one bin (measured on the record; the methods agree within half a point) | unfinished chain: requeues seen in the log and the lost work never priced (0), or every restarted segment counted whole (about 11) | R3, R4 | Ask 7 |
| R6 | the backtest: the simulated 90th-percentile wait for July to September 2026 (about 3.1 hours, nearest hour) against the capacity report's 3.4 | validation | the capacity report; the scheduler configuration's policy; the inputs above fitted on data to June 2026 | the honest simulations land in one bin at the nearest hour (asserted; the world tuned so the family sits mid-bin) | dismissed own evidence: the hurried inputs give about 1.5 hours and the gap is explained away as the August rack outage | R2, R3, R4, R5 | Ask 2, Component 4 |
| R7 | the cap: the largest 10,000 node-hour step of 2027 grants whose expected use meets the service level in at least 80 per cent of outcomes (about 320,000), and the share of the round's requests cut (about 20 per cent, nearest per cent) | uncertainty | policy 3 (the level, the window, the 80 per cent rule, what the outcomes carry); the simulated futures with the inputs redrawn from their sampling error and a rack's nodes failing together; the round's requests | the cap within one step (asserted across the rivals); the share follows the cap | method shortcut: node-hours available over the pooled use ratio (about 450,000, no cut); every shortcut together (about 380,000, a 5 per cent cut); no tail (350,000); Poisson (355,000); constant availability (345,000); no rework (340,000) | R2, R3, R4, R5 | Recommendation, Ask 1 |
Carry-forward: R1, R2, R3 and R4 each stand on their own files and are graded on their own; R5 is measured on the record and graded on its own (its forward use is a function of R3 and R4); R6 and R7 fall with any input; no analytical result feeds more than R6 and R7 (two of six others).

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| submissions arriving in sessions (array sweeps, a user's run of resubmissions) with weekday and term pattern | constructed as how researchers submit | no: every project, every month; the hurried Poisson misreads every hour's variance | one look (the inter-submission times) | modelling (a cluster process, or resampling that keeps the sessions) | earned by careful runs; kept as a result because the forward growth has to be carried through it |
| the duration tail beyond the observed limit | constructed as the run-time distribution of research jobs | no: every `normal` job; the limit changed for every project on 3 May 2026 | modelling: the families' predictions on the 24 to 48 hour window | modelling (a validated family) | keep, one of five |
| failures clustering by rack (a switch or a power feed) and repairs by class | constructed as the fleet's physical layout and the operator's repair process | no: every rack, every year, 2024 to 2026; the worst weeks fall in different racks | modelling: co-occurrence by rack and day, repair times by reason class | modelling (a marked cluster process) | keep |
| the software failure hazard rising with time since a node's last reboot | constructed as how the nodes' driver state degrades | no: every node | modelling | modelling | thin alone, one of five |
| projects' checkpointing (none, hourly, six-hourly) | constructed as how research codes are written | no: every project with requeued jobs, across the whole record | modelling: requeued jobs' excess elapsed against like jobs | modelling (a mixture) | keep |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the Q3 2026 record rebuilt | Missed | Right | Right |
| R2 the use of grants, the bursts and the round's expected use | Missed | Partly | Right |
| R3 the duration tail at 96 hours | Missed | Missed | Right |
| R4 the 2026 outage record | Missed | Partly | Right |
| R5 the rework share | Missed | Missed | Right |
| R6 the backtest on Q3 2026 | Missed | Missed | Right |
| R7 the cap and the cut | Missed | Missed | Right |
| Roughly | 0 of 7 | 2 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: the plan raises the limit to 96 hours, so the duration tail beyond 48 hours has to be extrapolated from the families that predicted the 24 to 48 hour mass; rescues 1 of 7 results
Pair estimate: 34

The careful but hurried column is the union of what frontier runs do unprompted on a scheduler log: clean every id,
segment and clock; censor at the limit in force; fit a parametric duration family by in-sample fit; resample or draw
Poisson submissions; read availability as the mean share of nodes up; simulate first come first served with backfill;
backtest on 2026 and bootstrap the result. The quick pass is the plan's arithmetic: node-hours demanded over node-hours
available at the average availability.

## Data provenance

Source: generated by task17/generator from a simulated process (the scheduler, the nodes, the projects and the operators), seed 1610; German town and university names invented, user and project names from Faker de_DE, every figure invented.
Behaves like the real thing: researchers submit in sessions (sweeps of near-identical jobs, resubmissions after a failure or a parameter change) with hour-of-day, weekday and term pattern and a trend as projects are granted and ramp up; a job's run time follows a heavy-tailed distribution by job class and node count, cut at the quality of service's limit in force on its submit date; the scheduler starts jobs first come first served by eligible time with backfill on requested walltime over whole nodes; nodes fail from software causes (a hazard rising with uptime, reset by a reboot or a maintenance window), from hardware causes (replacement with a parts lead time), and together by rack when a switch or a power feed fails; a job running on a failed node is requeued and restarts from its last checkpoint, which depends on the project's code; planned maintenance windows drain the partition monthly.
Genuine patterns: (1) hour-of-day, weekday and term seasonality in submissions; (2) sessions of near-identical jobs; (3) growth of demand with projects' age and grant size; (4) a heavy-tailed run time by class and node count; (5) failures clustering by rack and in time, with repair times by class; (6) the queue's wait rising steeply with utilisation, visible in the capacity report's weeks; (7) the 2025 expansion's effect on waits.
Problems by process: id rollover; requeue segments; two clocks across summer time; range-compressed node lists; day-hour limit strings; state suffixes; free-text reasons; a re-run month in the accounting export; node intervals cut by scheduler restarts.
Breadth: 12 files; about 200,000 job segments on about 190,000 jobs from about 310 projects and 1,400 users; about 24,000 node events on 64 nodes in 8 racks; 150 weeks of the capacity report; four allocation rounds; two distractors (the storage quota report and the helpdesk ticket export).

## Template check

Chain signature: assembly-reconciliation, modeling, missingness-measurement, investigation-loops, modeling, validation, uncertainty
Question form: how-many (the nodes to add), with the chance at each count, the backtest wait, the monthly node-hours, the run time under the raised limit, the Q3 2026 record, the outage figures and the rework share asked as their own quantities
Nearest build: task4 (an allocation with its sensitivity, measurement weight, a fitted physical model carried to new units) and task10's spent v1 (one censored capacity): different shape, weight and chain; the client's ML strategies 3 (where a run will land, validation) and 8 (spares for failures never seen start, modeling then allocation) share single lessons (a backtest, a repairable fleet) and none chains four fitted processes into a queue simulation read as a distribution's cut. Abstraction sentence ("a forward service level is a simulation over four separately fitted inputs, each with its own shortcut landing on a different count") is not writable against a build on file.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | queue wait | start minus eligible time; or start minus submit | eligible to start | policy 2.1; the log carries both (asserted: the call holds under either) |
| SF2 | the quarter's jobs | jobs eligible in the window; or started, or submitted | eligible | policy 2.2 |
| SF3 | the 90th percentile | nearest rank or interpolated | either | same call (asserted) |
| SF4 | jobs that count | gpu partition jobs that started; cancelled before start excluded; both qualities of service | as filed | policy 2.2 |
| SF5 | a job | one accounting job id within one id epoch, its segments one job | as filed | policy 2.3 (a requeued job is one job); the submit times separate epochs (asserted) |
| SF6 | node-hours | nodes allocated times elapsed hours over every segment | as filed | policy 2.4 |
| SF7 | the duplicated month | once | once | same call (asserted) |
| SF8 | clocks | submit and eligible in UTC, start and end local | as the export's headers state | same call (asserted) |
| SF9 | the scheduling policy | first come first served by eligible time with backfill on requested walltime, whole nodes, EASY or conservative backfill | as the configuration states; either backfill | the configuration file; same count under both (asserted) |
| SF10 | the limit a job ran under | the `normal` limit on its submit date (24 to 3 May 2026, 48 after); `short` 4 | as filed | the configuration history |
| SF11 | the 2027 limit | 96 hours from 1 April 2027 | as filed | the partition plan 4 |
| SF12 | the service level window | 1 January to 31 December 2027, one percentile over the year | as filed | policy 3.2 |
| SF13 | met with 80 per cent probability | at least 0.80 | as filed | policy 3.3 |
| SF14 | the cap's step | the largest 10,000 node-hour step met in at least 80 per cent of outcomes | as filed | prompt; policy 3.3 |
| SF15 | the expected use of a grant | from the projects' own records (use by project age and type), not the grant itself | as filed | policy 3.3 ("expected use, from the projects' records") |
| SF16 | the round's requests and the cut | the requests on file; cut pro rata to the cap | as filed | the round's request list; policy 3.5 |
| SF17 | the duration family | any family that predicts the 24 to 48 hour mass within the band | any | inside the band (asserted); families that fail the window named |
| SF18 | the sessions | a fitted cluster process or resampled days within weekday and term | either | inside the band (asserted) |
| SF19 | the outage process | a marked cluster process by rack, or compound by class with rack events | either | inside the band (asserted) |
| SF20 | what the outcomes carry | the jobs, failures and repairs as they vary, and the uncertainty of every rate estimated from the records; no allowance beyond what the records show | as filed | policy 3.4 |
| SF21 | rounding | the cap in steps of 10,000; node-hours to 1,000 (R1) or 10,000 (R2); hours whole; days to 0.5; shares to 1 or 5 per cent as asked; the burst index whole | as filed | prompt |
| SF22 | maintenance windows | the filed 2027 calendar | as filed | the maintenance calendar |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | gpu partition jobs eligible in the window, including jobs not yet submitted: policy 2.2 and 3.2 |
| 2 Unit of account | the job; nodes allocated whole: policy 2.3, the configuration |
| 3 Attribution window | 1 January to 31 December 2027 by eligibility: policy 3.2 (SF2, SF12) |
| 4 As-of dating | exports cut 15 November 2026; the board on 14 December 2026 |
| 5 Version basis | configuration history by date; the plan's 2027 limits; the round's request list as filed |
| 6 Denominator | the year's jobs for the percentile; node-hours used for the rework share; the round's requests for the cut: policy 2, prompt |
| 7 Weighting | each job once; each simulated future once |
| 8 Window length | inputs fitted on the whole record; rivals on 2025 to 2026 inside the band (asserted) |
| 9 Boundary inclusivity | at most four hours; at least 0.80: policy 3.1, 3.3 |
| 10 Rounding path | unrounded to the end; prompt (SF21) |
| 11 Tie-break | none: the step below the cap is met in about 0.86 of outcomes and the step above in about 0.70, clear of 0.80 on both sides (asserted) |
| 12 Maturity and censoring | run times censored at each job's limit; the 96 hour tail extrapolated (SF10, SF11, SF17) |
| 13 Order of operations | inputs fitted, the simulation run, the percentile per future, the cut |
| 14 Row order | nothing depends on order |
| 15 Duplicate resolution | the re-run month once; segments one job (SF5, SF7) |
| 16 Identity normalisation | node names through the rack layout; job ids within an epoch (SF5) |
| 17 Netting against gross | none |
| 18 Dimensional units | hours, node-hours, node-days; limits as day-hour strings; local and UTC (SF8) |
| 19 Code and status semantics | states as the scheduler writes them; reasons through their class (R4) |
| 20 Integerisation | the cap a whole step of 10,000; the cut share to the nearest per cent |
| 21 Clause scope | policy 2 for the measure, 3 for the sizing; the configuration for the queue |
| 22 Forward window contents | the 2027 requests, the plan's limits, the maintenance calendar; policy 3.4 for what the outcomes carry |

## Literal reader

The allocation policy executed word for word gives the measure (the 90th percentile of eligible-to-start waits over
the gpu partition's jobs eligible in 2027), the bar (four hours), the rule (the cap is the largest 10,000 step of grants
whose expected use, from the projects' records, meets the level in at least 80 per cent of outcomes), what the
outcomes carry (3.4) and the pro rata cut (3.5); the scheduler configuration gives the policy the queue runs under and
the limits by date; the plan gives the 2027 limit; the round's request list gives the requests. Every forward figure
is an estimate the text leaves to the analyst, and every literal alternative in the fork table lands on the same graded
figures or is ruled out by the sentence named.

## Prompt contract

A voice rewrite keeps: the question (how many node-hours of grants the 2027 round can carry at the service level, as
the largest 10,000 node-hour step met in at least 80 per cent of outcomes, and what share of the requests that cuts);
the 90th-percentile wait the same forecast gives for July to September 2026; the use projects make of their grants in
their first year and after it; the round's expected use at its requests; the mean run time of a `normal` job under the
2027 limit and the share of its work beyond 48 hours; the Q3 2026 jobs and node-hours; node-days lost to outages per
quarter, the share in events taking four or more nodes and the usual repair time by kind of failure; the share of
2026's work redone after node failures; a workbook and a one-page note; the rounding as stated. It never adds: a method,
a simulation, a family, a backtest word, bursts, clustering, racks, checkpoints, a file name or who is asking.

## Tried and rejected

- (none yet at the draw)
