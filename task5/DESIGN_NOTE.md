# task5 design note

Architecture 3 (re-rooted 2026-11-08 after both platform runs landed architecture 2). Read `## Tried and rejected`
first. Figures marked as measured come from `generator/checks.py` on the built pack; the rest are design targets the
generator asserts.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task5.json`, architecture v3, registered 2026-11-08T16:49:19Z after a pull
  that brought in task3 v6, task7 v6, task9 v7 and task10. `guard.py check` on the registered card: WARN only,
  `repeat.gate_g` against task3 v6, answered here: the decisive step is a choice of nonresponse model pinned by the
  closed quarters' own outcomes, which is what method_or_model_selection means, and task3 v6's step (a transfer
  storm by storm) shares nothing else with it. Axes redrawn at registration because the window moved under the draft:
  the decisive generator from G12 (same puzzle and same driver against task8 v14 and v10, task6 v2 and mark196) and
  then G6 (banned against task3 v6) to G13, the horizon mismatch, which is the honest label (the outcome of a report
  that has not arrived lands as an inactivation months after the flash, so neither the flash nor the latest quarters
  can see it); the context artifact from published_series (task3 v6) and planning_thread (task7 v6) to register (the
  unemployment insurance employer account register is the frame the section works from); the forcing event from
  statutory_or_regulatory_filing (task3 v6) and budget_or_appropriation (task7 v6) to vote_or_meeting (the Fund
  Board designates at its 4 March 2027 meeting); the forum to committee_or_panel (the Board). Architecture 2's
  identity and fate are the card's lineage, its shell (which, name, docx+xlsx) in `lineage_shells`. The NOTE against
  mark253 v1 (a sample's respondents reweighted within a frame attribute) is answered by the card's differentiation
  line: no respondent stands in for a nonrespondent here and no frame attribute defines the class.
- **Pairing.** Survey Research & Official Statistics / `census-register-administrative-data-quality` / Data
  Extraction & Conformation. The work is the field's own: an official statistic (each county's covered employment for
  December 2026) conformed from an administrative census (the unemployment insurance quarterly contribution reports,
  their amendments, the multiple worksite reports, the employer account register and its status history) whose
  reports arrive late, certified on the reports in by a cut-off, with every liable employer counted whether or not
  its report has arrived. The ETL move is "complete a record the process could not make": the December jobs of the
  employers whose report has not arrived, and the conformation feeds the judgment that decides, which is a
  nonresponse model (`guide-to-prompt` section 1, the ETL pincer: the correction's input is absent for the current
  quarter and present, as outcomes, for the closed ones, so the step is a measurement model of the nonrespondents
  forced by the closed quarters).
- **Niche.** The State of Franklin (fictional) created a Community Transition Fund in 2026. For each fund year the
  Fund Board designates every county whose covered employment in the December before fell 2.0 per cent or more on the
  December a year earlier, on the Commissioner of Labor's certification filed by 1 March from the reports the
  Department has received by 15 February. 2027 is the fund's first year. The Labor Market Information section
  prepares the certification from the Unemployment Insurance Tax Division's extract.
- **The call.** Which counties qualify (a designation set, "none" grammatical), with each county's December 2026
  jobs, the part of them estimated for employers whose report had not arrived, and the change on December 2025.
  Retrospective measurement, forward decision: December 2026 is past but not fully reported at the cut-off, and the
  Act designates on the certified estimate for the 2027 fund year.
- **Shape.** 03, a bridge between two totals, county by county: the jobs the received reports show, plus the jobs
  estimated for the employers whose report had not arrived, gives the December 2026 estimate, against December 2025.
  Graded cells: per county the estimated part, the December total and the change (the reported part is in the
  deliverable and not asked, because every route files it the same way), and the designated set.
- **Strategy.** maturity_censoring (late arrival), gap time then population, generators G13 (horizon mismatch), G12
  (absence of record against record of absence), G3 (record against operation). Gate G method_or_model_selection.
  Layer 2 family estimand_identification, pattern own:a-missing-report-informative-only-when-its-usual-transmission-arrived.
- **Forum, event, organisation, role.** The Community Transition Fund Board designates at its 4 March 2027 meeting
  (committee_or_panel, vote_or_meeting) on the certification the Department of Labor's Labor Market Information
  section prepares (research_or_statistics_office); the section's director is the stakeholder (statistical_office_head).
- **People** (`guard.py names --geo "United States" --seed 501`, locale en_US): Danielle Fuller, director of the Labor
  Market Information section; Matthew Cox, the Department of Commerce's administrator for the Fund; and from
  `guard.py names --geo US --n 4 --seed 50327`, William Robertson, chief of the Unemployment Insurance Tax Division, who
  signs the data agreement for the Division and is copied on the Fund's request. None appears in the prompt.
- **World.** Fourteen counties: Calder (the metro county), Merritt, Linden, Whitcomb, Garrow, Pell, Hadley, Ostrom,
  Bray, Fenwick, Corliss, Talcott, Kittredge, Sayre; about 27,700 liable accounts and 480,000 covered jobs. Payroll
  agents file most small employers' reports, each agent sending its clients' reports in one transmission a quarter
  (some statewide bureaus send a main file and a follow-up); twelve statewide payroll bureaus serve clients across the
  state, the rest are local accountants. The Division posts a new employer's account from its first contribution
  report (liability established on that report, posted in the next few nights), so the register holds no liable
  account that has never reported. Q4 reports are due 31 January and at year end about half the statewide bureaus send their
  fourth-quarter transmissions after the 15 February cut-off, every year, while local accountants rarely run late.
- **Data-native sentence.** In an unemployment insurance report census the reports a payroll agent files arrive
  together, so a missing report usually means its agent's whole transmission is late and says nothing about the
  employer, while a report missing from a transmission that arrived means the employer stopped sending its payroll,
  which an employer that has shed jobs or closed does; a closed employer files nothing more and appears only when the
  Division inactivates its account two or three quarters later, so the closed quarters show what the missing alone
  were and the latest quarters do not yet.
- **Abstraction sentence** (against the nearest approved builds, not writable as the same): mark196 recovers a count
  from two dependent capture channels; mark182 corrects a duration distribution sampled by length; mark253 counts units
  below a line as a sum of probabilities under separated noise; mark179 links a second agency's records person by
  person. Here a unit-level total is completed for units that have not reported, where whether a unit's silence
  carries its outcome is read from whether the units it always reports with have reported, and the silent units'
  outcomes are read from earlier silent units on cohorts old enough for their closures to have been recorded. No
  sentence holding any of those builds beside this one is the same sentence.
- **Sources.** The client's two-layer standard and Survey strategy 03 (nonresponse bias weighting does not remove);
  the BLS Quarterly Census of Employment and Wages practice for delinquent reports (the previous month's employment
  carried by the reporting units' change in the same industry and area, the field's method at rung 1); state
  unemployment insurance bulk filing by payroll service providers and third-party administrators; UI account
  inactivation after consecutive quarters without a report; the multiple worksite report.

## Default path

The path a competent analyst takes after conforming every file correctly and reading the Act and the data agreement
(figures measured on the built pack by `checks.py`, rung R1x).

1. Read the Act: a county's December covered employment is the jobs for the pay period including 12 December at
   worksites in the county, summed over every employer liable for the fourth quarter, whether or not its report has
   been received; a county qualifies when its change on the December before, rounded to one decimal, is minus 2.0 per
   cent or lower; the certification counts the reports received by 15 February 2027.
2. Conform: the Q4 2026 reports received by 15 February 2027, the latest version of each (amendments over originals,
   resubmissions once); multiple worksite employers split by their worksite reports; the liable accounts from the
   register and its status history (inactivated accounts out from their effective quarter, successors in); the
   December 2025 base from the closed Q4 2025 reports.
3. Impute each liable employer whose Q4 2026 report has not arrived as the field does for a delinquent report: its
   September 2026 jobs moved by the change of the reporting employers in its county and supersector; an employer that
   has missed two quarters is treated as ceased.
4. Back-test the imputation on the closed quarters, rebuilt from the receipt times as the flash would have seen them:
   it overstates every county's final figure by 0.0 to 0.7 of a point on every closed quarter, a steady upward miss
   averaging 0.2 to 0.5, apart from the two lake counties' 2024 fourth quarter (1.3 and 2.2, their resorts' own
   December history a year short then), asserted in checks.py.
5. Sum by county and compare with December 2025.

Ends on: no county qualifies (the lowest Bray at minus 0.7, Ostrom minus 0.5, Garrow plus 0.3 per cent).

Golden: Garrow and Ostrom qualify (minus 3.0 and minus 3.1 per cent; Kittredge next at minus 1.2).

## Stump sentence

A competent solver conforms the reports, amendments and worksites, imputes each employer whose December report had not
arrived as the field does (its September jobs moved by its county's reporting employers' change), treats an employer
missing two quarters as ceased, sees that imputation back-test with a steady upward miss under 0.7 of a point on the
closed quarters and files that no county qualifies; a report missing from a transmission that arrived marks an employer
that has shed jobs or stopped trading, which keeps 0.29 of its September jobs on the quarters old enough for
inactivations to have landed, and that puts Garrow and Ostrom past the line.

## Deep reasoning

- **Task type:** census-register-administrative-data-quality in Survey Research & Official Statistics, which serves
  Data Extraction & Conformation: an official covered-employment statistic conformed from an administrative report
  census whose reports arrive late, with the nonreporting employers' December jobs estimated for the certification.
- **Domain test:** the quantity that decides is each county's December 2026 covered employment, an official estimate
  from an administrative census with late reports, worked as a statistics office works unit nonresponse: which missing
  reports are ignorable and which carry the outcome, and what the nonrespondents' jobs are; the field's estimator for
  a delinquent report (the employer's previous month carried by the reporting units' change in its cell) sits at rung 1.
- **Swap:** put hospitals and their monthly activity returns for employers and their reports and the call reads "which
  regions' December inpatient days fell 2 per cent on the returns in by mid-February"; no hospital stops filing because
  it has closed, no account is inactivated two quarters later to say so, and a hospital's missing return carries no
  outcome of its own, so the deciding inference has nothing to read and the task stops making sense.
- **Layer 1:** amended reports superseding originals and exact resubmissions seconds apart (the Division's filing
  system); multiple worksite reports splitting an employer's jobs across counties, with county names upper-cased and
  suffixed there and coded in the register (two systems); successor accounts after a transfer of business, the
  predecessor inactivated (the Division's account maintenance); seasonal employers reporting near-zero December jobs;
  NAICS 2017 codes on older accounts beside NAICS 2022 (the register's history); paper reports keyed by date with no
  time (the mail room); habitual late filers; employers missing two quarters not yet inactivated (the Division's
  quarterly run); every item as its system produces it, nothing placed to be caught.
- **Layer 2:** identification of a nonresponse mechanism and the nonrespondents' outcome (estimand_identification):
  a missing report is ignorable when its whole transmission is late and carries the employer's outcome when it is
  missing alone, and the outcome is read from earlier nonrespondents on quarters whose closures have been recorded.
- **Decisive step:** recognising that a missing report has two causes, an agent's late transmission or the employer's
  own failure to send its payroll, separating them by whether the employer's usual transmission-mates have reported, and
  estimating the missing-alone employers' December jobs from earlier missing-alone employers on quarters old enough for
  their inactivations to have landed.
- **Not semantics:** every field read correctly (the receipt time to the second, the report kind, the worksite split,
  the status history's codes and effective quarters, the Act's liable employers) gives a correct list of who has and
  has not reported, and the list does not say what a missing employer's December jobs are; the default path reads
  every field right and files that no county qualifies.
- **Not rule application:** no filed rule says how a nonreporting employer's jobs are estimated (the Act files the
  population, the outcome, the window, the comparison and the threshold; the data agreement describes fields), and the
  family a competent analyst would build spreads from none to every county: the reports as received designate all
  fourteen, the field's imputation and its two-quarter refinement none, the filer-type reading (every agent client's
  lateness ignorable) Ostrom alone, the newly-late reading every county with a late statewide bureau, the
  missing-alone reading with outcomes from the latest quarters none, with never-filers dropped none; the
  standing family (the missing-alone reading with the closed quarters' outcomes, under every clustering, window,
  threshold and split in SF12) files Garrow and Ostrom, and what rules the rest out is the closed quarters' own outcomes
  (C4), loud in the employers the rival misreads.
- **Analyst test:** a strong analyst who conforms every file and reads the Act and the agreement imputes each missing
  report as the field does, treats employers missing two quarters as ceased, back-tests with a steady upward miss under
  0.7 of a point and files that no county qualifies (the lowest Bray at minus 0.7, Ostrom minus 0.5, Garrow plus 0.3); one who notices the agents' transmissions and reads every agent client's lateness
  as the agent's files Ostrom alone.
- **Estimand:** sections 2, 4 and 5 of community_transition_fund_act_2026.docx: December covered employment for a county
  (the jobs for the pay period including 12 December at worksites in the county, summed over every employer liable to
  report for the quarter, whether or not its report has been received when the Commissioner certifies), the change on
  the December before as a per cent rounded to one decimal, minus 2.0 or lower designates, from the reports received
  by 15 February 2027; the data agreement (ui_lmi_data_sharing_agreement_2025.docx) defines every field.
- **No decoy:** nothing is planted: no memo, briefing, draft or stakeholder figure argues the field's imputation or any
  set; the Act and the agreement file the WHAT and the fields; every file is what its system produces.
- **No certified replay:** the published Q4 2025 county table confirms the December 2025 base on every route and says
  nothing about December 2026; no certified figure for December 2026 ships and nothing is recovered by reproducing one.
- **Chain:** (1) the field's imputation (September jobs moved by the cell's reporters) back-tests with a steady upward
  miss, traced on the closed quarters to missing reports from employers that had stopped; (2) a missing report has two
  causes, a payroll agent's late transmission or the employer's own failure, and only whether its usual
  transmission-mates have reported separates them, because the agents are named nowhere and their year-end lateness
  fills the missing pool; (3) the employers missing alone keep 0.29 of their September jobs, which only the quarters
  old enough for inactivations to have landed show, the latest quarters reading 0.72 because their closures have not
  been recorded; (4) carried into each county's December total, Garrow and Ostrom fall 2.0 per cent
  or more and no other county does.
- **Judgment:** a nonresponse-mechanism and outcome-model judgment, justified from the data: lateness within a late
  transmission is ignorable (the closed quarters show batch-late employers' December jobs moving with their cell's) and
  lateness alone carries the outcome (the closed quarters show the missing-alone keeping 0.29 of their September
  jobs, the same for agent clients and direct filers within sampling error, most of them never filing again and inactivated later), and the outcome must be measured on quarters
  whose closures have landed, because an immature quarter's unresolved employers are the closed ones.
- **Hidden by:** the field's imputation passes its own back-test, because informative lateness has been a small part of
  every past quarter's missing pool and its upward miss is 0.2 to 0.5 of a point; in December 2026 the missing pool's size and
  its mix by county, industry and size look like every year-end's, because the statewide bureaus' late transmissions
  dominate it, and the reporting employers in Garrow and Ostrom fall only slightly (the hardest hit are the ones that
  have not reported), so no group-by of the received reports shows the two counties.
- **After the notice:** once a run has seen that agents' transmissions arrive together, it still owes (1) the sibling
  reading, built from receipt times with no agent field, and the wrong turn there is the filer-type reading (every agent
  client's lateness taken as its agent's), which files Ostrom alone because Garrow's missing-alone employers are
  agent clients; (2) the outcome of missing alone, and the wrong turns there are the latest quarters (0.72 kept,
  none) and dropping the employers that never filed (0.70, none); (3) carrying both through every
  county's worksites and its December 2025 base.
- **One-fact test:** the likeliest hint, that an employer missing from a transmission that arrived is in trouble, still
  leaves the solver to rebuild the transmissions from receipt times with no agent field, to measure the trouble's
  outcome on quarters old enough for inactivations to have landed (the obvious quarters, the latest, read 0.72),
  and to carry it through every county; the hint that missing reports can mean closure leads to the newly-late reading,
  which designates every county with a late statewide bureau. No one sentence makes it routine.
- **No replay:** no published or certified figure for December 2026 ships and nothing is recovered by reproducing one;
  no stated number is wrong.
- **Pinned:** every rival is run on the clean truth (checks.py, the ladder): the reports as received designate all
  fourteen (ruled out by section 2: every liable employer counts whether or not its report has arrived); the field's
  imputation and its two-quarter refinement none, the filer-type reading Ostrom alone, the newly-late reading every
  county with a late statewide bureau, the latest-quarters and never-filers-dropped readings none and none (each
  ruled out by the closed quarters' outcomes for the employers it misreads, C4); every member of the standing family in
  SF12 files Garrow and Ostrom; the December 2025 base is one figure on every route (SF8).
- **Run forecast:** method shortcut at rung 1: a strong run conforms everything, applies the field's imputation, sees it
  back-test and files that no county qualifies; a run that notices the transmissions takes the filer-type reading
  (unfinished chain) and files Ostrom alone; a run that separates the two causes and reads the outcome from the latest
  quarters is a self-confirming check (its window agrees with its other recent windows) and files that no county
  qualifies.
- **Strategy label:** WORKS IN FORM (Part A, outcomes that have not finished happening): completion speed differs by a
  unit no pooled factor captures, here whether a missing report's transmission arrived, so the pooled or textbook
  completion (the field's imputation, a pooled late-report factor) files a named wrong answer; the dead form (the
  field's standard completion as the golden) is rung 1.
- **Lesson:** in an administrative census a missing record's meaning depends on how it would have arrived: a record
  missing with the batch it always comes in says nothing about its unit, one missing alone says what happened to it,
  and what happened is read only on cohorts old enough for the system to have recorded closures.

## Survivor anatomy

- **Actor:** the employer has rows (an account, its quarterly reports with receipt times, its worksites, its status
  changes), and whether its missing report carries its outcome has no column: no file holds a filing agent, a channel,
  a transmission number or a distress flag, and the data agreement's field list carries none.
- **Link:** the signal is a relation between rows of the reports file across quarters, an employer's report against
  the reports that arrived in the same second with it in earlier quarters and their arrival this quarter, a comparison
  no key offers and the field's imputation never makes; and the outcome is read across two files at two grains, the
  closed quarters' late reports and the status history's inactivations with their effective quarters.
- **Reflex:** the field's method for the deciding quantity (a delinquent report imputed from the previous month by the
  reporting units' change in its industry and area) sits at rung 1 and, with its two-quarter refinement, files that no
  county qualifies.
- **Back-test:** the textbook route validates: rebuilt from the receipt times on the closed quarters, the field's
  imputation overstates every county's final figure by 0.0 to 0.7 of a point, the small upward miss steady from quarter
  to quarter (the lake counties' 2024 fourth quarter apart, where the resorts' own history is a year short).
- **Second use:** every file the decisive step reads is read by every route: the receipt times define what the flash
  holds, the status history defines who is liable (inactivations, successors) and the December 2025 base, the closed
  quarters' reports are the history every back-test uses; deleting the step drops no file.
- **Shock:** Garrow and Ostrom are the top two of none of the shipped statistics a sort would read (the missing share,
  the share of usually-punctual employers missing, the reporting employers' change, the field's imputed change, the
  county's size, the share of agent clients, the share of small employers), asserted in checks.py.
- **Pins:** the WHAT is filed in the Act (the population with members not yet reported, the outcome, the pay period,
  the comparison, the rounding, the threshold, the cut-off); no filed sentence names an agent, a transmission, a
  filing channel, lateness, an imputation or an outcome of a missing report (asserted on both governing documents and
  the request).

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the reports as received | section 2's whether-or-not clause rules it out | the reports' rows | none | none | none | a sum | yes | readable |
| R1 the field's imputation for every missing report | none | the reports and the cells | the delinquent-report imputation | its own back-test passes | none | a ratio | yes | readable |
| R1x the same with two-quarter delinquents ceased | none | two missing quarters in the reports | the careful analyst's refinement | the back-test passes | the battery flags long delinquents | a filter | yes | readable |
| R2 the filer-type reading | none | co-arriving receipt times | a channel reading of lateness | none | none | a group-by of filers | yes | readable |
| R3 (decisive) missing from a transmission that arrived, outcomes on closed quarters | no sentence names an agent, a transmission, lateness or an outcome | no column holds an agent, a channel or a distress flag | the field's method imputes from the cell | the back-test passes the field's method | the battery cleans versions and worksites and stops | a comparison of each employer's report with its transmission-mates', across quarters | the files are every route's | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | liable employers for the fourth quarter | accounts liable on the register for any day of the quarter: liable by its last day and not closed, inactivated or transferred with effect by its first (a final report of zeros from an account closed before the quarter is no reporter) | accounts that filed a Q4 report; accounts active on 15 February; the history ordered by effective rather than processed date; an outstanding employer with a closure effective by 12 December read as nought (Schedule C) | all fourteen; the same; the same; the same | section 2 (whether or not its report has been received) and the history's effective dates (asserted); no account ends on or before its own liability date, so both orderings give one status, and no outstanding employer carries a closure entered by the cut-off, because a notice of closing is entered with the final report (both asserted) |
| SF2 | December covered employment | the month-three employment of the Q4 report (the pay period including 12 December) | the quarter's average; total wages | another figure | section 2 and the agreement's field definition (asserted) |
| SF3 | the reports received by 15 February | received at or before 23:59:59 on 15 February 2027, local time | the due date; the extract's full contents | same call | same call (asserted, nothing received on 15 February moves a county by 0.05) |
| SF4 | a report received twice or amended | the latest version received by the cut-off | the first; both | same call | same call (asserted) |
| SF5 | an employer with worksites in several counties | its jobs split by its worksite report; a missing one by its latest worksite report | the register's county | same call | same call (asserted, every county within 0.05) |
| SF6 | a successor account | the successor counts from its liability date, the predecessor out from its transfer quarter | both, or neither | same call | the status history (asserted) |
| SF7 | the December 2025 base | the closed Q4 2025 reports, latest versions, inactivated employers at zero | the published Q4 2025 table | same figures | the table equals the reports on every county (asserted) |
| SF8 | the change | Dec 2026 over Dec 2025, minus one, per cent, rounded once to one decimal; minus 2.0 or lower qualifies | unrounded; strict | same call | section 4 (asserted, no county within 0.15 of the line) |
| SF9 | paper reports keyed by date | received on that date | at midnight as a transmission | same call | same call (asserted) |
| SF10 | the cell for the field's imputation | county by supersector, falling back to the county | the county alone; the supersector statewide | same call | same call (asserted on every rung) |
| SF11 | an employer missing two quarters | carried at the closed quarters' outcome for two-quarter delinquents | ceased; imputed alive | same call | same call (asserted) |
| SF12 | the missing-alone reading | a missing employer whose last transmission's other reports have mostly arrived (and a direct filer newly late), carried at the closed quarters' outcome for missing alone, pooled | a transmission as three or more reports in one second or two or more; mates from the last quarter or the last four; half or three in ten arrived; outcomes pooled, by size class or by filing channel (agent clients 0.28, direct filers 0.30, bootstrap s.e. of the difference 0.03); closed quarters 2024Q1, 2024Q2 or 2023Q3 to 2025Q2 or 2025Q3 | same call | same call (asserted, every member files Garrow and Ostrom with every county's change, total and estimated part in the golden's bin) |
| SF13 | the filer-type reading | ruled out | every agent client's lateness taken as its agent's | Ostrom alone | the closed quarters: agent clients missing from a transmission that arrived kept 0.28 of their September jobs (asserted under one half) |
| SF14 | outcomes of missing employers | quarters whose missing-alone employers have all resolved (a late report or an inactivation) | the latest quarters; never-filers dropped | none; none | the status history: the latest quarters' unresolved employers are inactivated within the next two quarters on every closed quarter (asserted) |
| SF15 | seasonal employers missing in December | their own December-to-September pattern from the year before, moved by the cell | September moved by the cell | same call | the closed quarters (asserted, an ask's second judgment) |
| SF16 | a transmission that arrived | at least half of the employer's third-quarter transmission-mates have reported | any one of them has | same call, Garrow 0.3 and Ostrom 0.2 higher | the closed quarters: the two late transmissions in 2024Q1 and 2024Q2 with one or two of 48 mates in (clients that had moved to another agent) had their outstanding members arrive together, in one second, weeks later (asserted) |

## Ladder

| Rung | Construction | Designates | Changes kept (of 14) |
|---|---|---|---|
| R0 | the reports as received | all fourteen (Fenwick the nearest the line at minus 2.7) | 0 |
| R1 | the field's imputation for every missing report | none (Bray nearest at 0.0) | 0 |
| R1x | R1 with two-quarter delinquents ceased (default path) | none (Bray minus 0.7, Ostrom minus 0.5, Garrow plus 0.3) | 0 |
| R2 | the filer-type reading | Ostrom (minus 2.8; Garrow minus 0.2) | 3 |
| R2b | every newly-late employer at the missing-alone outcome | twelve counties, all but Fenwick and Sayre | 0 |
| R3a | missing alone, outcomes from the latest quarters (0.72 kept) | none (Ostrom minus 1.5) | 0 |
| R3b | missing alone, never-filers dropped (0.70 kept) | none (Ostrom minus 1.6) | 0 |
| Rs | the golden with the lake resorts at their cell's change | Garrow, Ostrom | 12 |
| G | missing alone, outcomes on the closed quarters | Garrow, Ostrom (minus 3.0 and minus 3.1; Kittredge next at minus 1.2) | 14 |

Margins (checks.py): on the golden Garrow and Ostrom sit 1.0 and 1.1 below the line and every other county at least
0.8 above it; R1, R1x, R3a and R3b keep both at least 0.4 above the line; R2 puts Ostrom at minus 2.8 and Garrow at
minus 0.2. Every rung but Rs names a set other than the golden's. Pricing: the shallow run (R1x) keeps nothing of the
call, the components or the asks; a run that notices the transmissions and stops at the filer-type reading (R2)
designates Ostrom alone and keeps three changes; a run that takes the deep step keeps the call and the components and
loses the lake counties' figures unless it also reads the resorts on their own pattern (Rs).

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | every employer liable for Q4 2026 on the register, reported or not | filed in section 2; SF1 |
| 2 Unit of account | the job (a worker on the payroll for the pay period including 12 December) at a worksite; the county | filed in section 2; SF2, SF5 |
| 3 Attribution window | December 2026 (month three of Q4) against December 2025 | filed in sections 2 and 4 |
| 4 As-of dating | reports received by 23:59:59 on 15 February 2027; the register and status history as at that day | filed in section 5; SF3 |
| 5 Version basis | the latest version of a report received by the cut-off | C1 (SF4) |
| 6 Denominator | the county's December 2025 covered employment | filed in section 4; SF7 |
| 7 Weighting | none: totals over totals | filed in section 4 |
| 8 Window length | one month (December) in each year | filed in section 2 |
| 9 Boundary inclusivity | minus 2.0 or lower qualifies | filed in section 4; SF8 |
| 10 Rounding path | the change rounded once to one decimal; jobs summed unrounded and stated whole | filed in section 4 and the prompt; SF8 |
| 11 Tie-break | none: a set, no ranking | C1 |
| 12 Maturity and censoring | December 2026 incomplete at the cut-off (the estimand counts every liable employer); the history's quarters mature as closures land | filed in section 2; the decisive step, SF12, SF14 |
| 13 Order of operations | versions, then liability, then worksites, then estimation, then sums | C1 (SF4, SF5 asserted on every order) |
| 14 Row order | none: set operations keyed by account and quarter | C1 |
| 15 Duplicate resolution | exact resubmissions once | C1 (SF4) |
| 16 Identity normalisation | the account number; county names to codes; NAICS 2017 to 2022 | the systems' own keys; C1 |
| 17 Netting against gross | a successor's jobs once | C1 (SF6) |
| 18 Dimensional units | jobs (head count) throughout | units in the data |
| 19 Code and status semantics | report kind O and A; status codes INACT, REACT, XFER, CLOSE | the agreement's schedules; C1 |
| 20 Integerisation | estimated jobs summed unrounded, stated whole | C1 |
| 21 Clause scope | section 2's whether-or-not clause governs the population only | filed scope |
| 22 Forward window contents | the Board designates on the certification for the 2027 fund year; nothing forecast past December 2026 | filed in sections 4 and 5 |

## Literal reader

Executed word for word, the prompt and sections 2 to 5 of the Act file the population (every liable employer, reported
or not), the outcome (month-three jobs at worksites in the county), the window, the comparison, the rounding and the
threshold, and say nothing of how a nonreporting employer's jobs are estimated, so the literal reader has to estimate
them. Every reading that estimates them from the closed quarters' own outcomes for employers missing alone, in any form
SF12 lists, gives Garrow and Ostrom; the reports-as-received reading is ruled out by section 2's whether-or-not clause;
the field's imputation, the filer-type reading, the newly-late reading and the latest-quarters and never-filers-dropped
readings are ruled out by the closed quarters' outcomes for the employers each misreads (C4, SF13, SF14), and the
any-one-mate reading of a transmission that arrived by the late transmissions whose members arrived together weeks
later (SF16). Each convention the call needs is closed in the fork table, asserted in checks.py.

## Oracles

No shipped file ranks the counties on the call: no December 2026 figure, flash, imputation, agent, transmission number
or distress flag ships. The published Q4 2025 county table ties to the reports on every route (SF7). The closed
quarters' reports and the status history are the referee for every reading of a missing report, and they refute every
rival on the employers it misreads; nothing ties only under the golden. The contribution rate notice and the county
population estimates are read by no route and ship as distractors.

Leak sweep (leak.py REVIEW, no LEAK, on the reader's cut and again on the final cut): the rate notice's 3.0, 0.0 and 0.1 are edges of
its reserve-ratio bands in the Division's 2027 contribution schedule, a distractor no route reads, and name no county
(harmless); the Act's "section", "account" and "design" are its own section numbering, the employer account and the
words designate and designation, and the agreement's "closed", "section", "account", "history", "agreement" and
"earlier" are its status codes, its schedules and the status-history extract's name, and neither document names an
agent, a transmission, lateness, an imputation or an outcome (asserted in checks.py; harmless).

## Ask sheet

The asks ride the deep step: per county the December 2026 jobs, the part estimated for employers whose report had not
arrived and the change, the designated set (sheet and chart) and the employer list with its classes. The landed row is
a run that takes the deep step and cleans every mess item but carries the lake resorts at their cell's change (the
asks' own second judgment); the shallow row is the default path, R1x.

| Ask (Supplementary item) | Shallow run (R1x) | Landed run's figures | Landed run, cracker verdict |
|---|---|---|---|
| 1 the sheet names the designated counties | misses (none) | Garrow and Ostrom | kept |
| 2 December 2026 jobs, fourteen counties and the state | misses | Kittredge and Talcott a hundred or more off | miss |
| 3 the jobs estimated for employers whose report had not arrived | misses | Kittredge and Talcott a hundred or more off | miss |
| 4 the change on December 2025, fourteen counties and the state | misses | Kittredge minus 0.2 and Talcott 1.1 against minus 1.2 and 0.3 | miss |
| 5 the chart against the line | misses | the same two columns below the line | kept |
| 6 the employer list and its classes | misses | every class count | kept |

Pair ceiling: 39.8 (the landed run 72.5, the shallow run 7.0). If the landed run also reads the resorts on their own
pattern it keeps every ask, 100.0, and the pair is 53.5, or 56.0 with five points of partial credit on the shallow run:
under 60, over the paper target of 50.

Shallow keep: 0.0 per cent of the ask weight (the landed run keeps 50.0).

Measured by: generator/ceiling.py

## Prompt contract

The author's voice rewrite may not drop or change: the question (where covered jobs in December 2026 fell 2.0 per cent
or more below December 2025, county by county, on the estimate the Department can certify from the quarterly reports
it had received by 15 February 2027); the hold being grammatical ("any counties that qualify"); the 2027 Community
Transition Fund; ctf_certification_december_2026.xlsx with every county's December 2026 jobs, how many of them are
estimated for employers whose report had not arrived, its change on December 2025, and the chart of the changes against
the line; ctf_employer_jobs_december_2026.csv with every liable employer, a row for each county it employs in, whether
its report had arrived and its December 2026 jobs there as reported or estimated; jobs whole numbers and changes per
cents to one decimal. It may not name an agent, a transmission, lateness, an imputation, a model, a back-test or a
closure.

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
