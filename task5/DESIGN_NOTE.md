# task5 design note

Architecture 2 (re-rooted 2026-10-31). Read `## Tried and rejected` first.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task5.json`, architecture v2, registered 2026-10-31T17:41:05Z after a pull,
  so every card filed before it was in the check (the re-roots of task118, task181 and task306 included). `guard.py check`
  on the registered card: PASS. One older-build match on gap, pattern and Gate G (task477) is answered by a
  differentiation line on the card. Axes drawn clear of the window at registration: organisation family
  research_or_statistics_office (local_government is banned against task181, government_agency against task306,
  utility_or_infrastructure against task118), forum minister_or_cabinet, forcing event statutory_or_regulatory_filing,
  role statistical_office_head, strategy classification_error, calibration none, context artifact register, shape 01.
  Architecture 1's identity and fate are the card's lineage, its shell (how-many, "Put", csv and docx) in
  `lineage_shells`. Design repair of 2026-11-08 (no new architecture, the portal's Domains Fit callout): the card is
  re-registered with the forum redrawn from minister_or_cabinet (banned at re-registration against mark273 v5) to
  committee_or_panel, the honest label now that the office's own certified release, signed off by its quality board,
  is the decision and the ministry pays on it; the context artifact redrawn from register (banned against task4 v4) to
  planning_thread, the ministry's assignment that now carries the register-quality request; the differentiation line
  re-keyed from task477 to mark477, the same build under the baseline's name. `guard.py check` and `register` on
  2026-11-08: WARN only. Gate G stays method_or_model_selection (repeat.gate_g against task6 answered: the occupancy
  reading is a choice of measurement model, the label the decisive step earns); the decision stays designation_set
  (repeat.decision against task4 answered: Section 6 designates a set, the regulation's own shape); the deliverable set
  stays docx+xlsx (Section 7 files a letter and a dwelling list, the genre the office certifies in).
- **Pairing.** Survey Research & Official Statistics / `census-register-administrative-data-quality` / Data Extraction &
  Conformation. The task type serves ETL in the taxonomy. The work is the field's own: a register-based dwelling statistic
  built by conforming the cadastre, the population register, the electricity hub's meter point register and its hourly
  reads into one dwelling-level occupancy file under the scheme's data contract, and the call is the grant designation
  that file decides. Since the 2026-11-08 repair the deciding figure is stated as what it is in the field's terms: each
  municipality's vacancy share is an official estimate of true occupancy built from two error-prone administrative
  sources, the population register (which lists residents of empty dwellings and omits people who live where they are
  not registered) and the meter record, and the asks are the register's coverage errors measured against that estimate
  (overcoverage, undercoverage, net bias), the register-quality statistics an office publishes when it asks whether a
  register could carry a count, with each share's interval.
- **Niche.** A ministry's 2027 vacant dwelling activation grant, piloted in one fictional Norwegian county of ten
  municipalities, goes to every municipality where at least 5.0 per cent of the dwellings the regulation counts stood
  vacant in the reference fortnight of 9 to 22 November 2026. The regulation defines vacant by whether anyone lived in the
  dwelling, whatever the population register shows, and has the national statistics office certify each municipality's
  share by 15 January 2027 from the hub's hourly meter data, which the regulation makes the office's source.
- **The call.** Which municipalities qualify (a designation set), with each municipality's vacant dwellings, share and
  90 per cent interval, and the register's overcoverage, undercoverage and net bias beside them.
  Retrospective measurement, forward decision: the fortnight is closed, the grant is the 2027 programme's, and the
  regulation designates on that fortnight.
- **Shape.** 01, the candidates against a threshold: each municipality's vacant dwellings and share (two figures for each
  municipality), the designated set, the margin to the line, a chart of the shares against the threshold with named parts
  and the two files; with the asks, well over 25 criteria. Decision designation_set, answer set_of_items, question form
  whether (the call is where the grant should go).
- **Strategy.** classification_error. Gap objective first (the register's residents and the meter's level are correct
  records and are not what the regulation scores, which is whether anyone lived there), then population. Generators G3
  (record against operation: the meter's level records the heating, not the household) and G12 (absence of a registered
  resident against absence of residents). Gate G method_or_model_selection. Layer 2 family estimation_fit, pattern
  own:occupancy-from-the-household-daily-cycle-against-a-heating-load.
- **The ETL pincer, answered.** Of the five ETL moves this is the per-case input a second file pins: each dwelling's
  occupancy, pinned by its own hourly reads. The forcing file pins a condition (a household's daily cycle on some day of
  the fortnight). Reading the file correctly gives a level per hour and per day, and neither says whether anyone lived
  there; occupancy is the presence of the morning and evening rise over the dwelling's own night-time load, a model of a
  household's routine against a heating load that no field records, so a correct read is not sufficient. Nothing in the
  step is identity resolution, grain or time semantics.
- **Forum, event, organisation, role.** The ministry pays the grant on the office's certified figures (Section 8),
  so the certification goes to the scheme's funder (funder_or_donor; redrawn on 2026-11-08 from committee_or_panel,
  banned against task4 v4 at the deepening's re-registration); the regulation's delivery deadline forces it
  (budget_or_appropriation since the heart re-run of 2026-11-08: the ministry's 2027 allocation of the grant on the
  certified figures; statutory_or_regulatory_filing was banned against task3 v3, registered after this card); the national statistics office certifies it (research_or_statistics_office), its
  dwelling statistics section head the stakeholder (statistical_office_head).
- **People** (`guard.py names --geo Norway --seed 470`, locale no_NO): Martine Strøm, head of the office's dwelling
  statistics section; Eirik Haug, the ministry's adviser on the scheme. Neither appears in the prompt.
- **Data-native sentence.** An empty dwelling in a Norwegian November is heated (a lowered thermostat or frost protection
  keeps the electric heating on), so its hourly load runs with the outdoor temperature at levels many lived-in flats never
  reach, and where its owner left the heaters' or heat pump's daily timer running it also rises every morning and evening
  at its comfort hours, while the population register still lists residents who have moved to care or abroad and omits
  students and workers who never re-registered; only a household's day departing from what the dwelling repeats every
  day shows that someone lived there.
- **Stump deepened (2026-11-08, after the judge's SEND_BACK on Gate H).** As filed, the household's morning or evening
  rise separated the dwellings bimodally, so one sentence rescued a run (H5). The world now carries heating on daily
  timers (`sim._programs`, its own random stream, so every other draw is unchanged): 70 vacant dwellings left with their
  timer running, 30 per cent of the lived-in electric and heat-pump dwellings with one, and each household's odd jobs
  (a wash, a sauna, baking) on days of its own. The rise now reads the 70 as lived in and designates Tverrvika and
  Ørnevik alone, separating cleanly and agreeing with the register, so the strong run's own route passes its own
  checks; the decisive step is the household's departure from the dwelling's own typical day.
- **Abstraction sentence** (written against the nearest approved builds, not writable as the same): task182's "each
  bore's own lagged driver response" reads a unit's departure from its own response to a shared driver; here the step is
  the presence or absence of the users' daily rhythm in a unit's own record whose level a use-independent load carries,
  with no response to a driver estimated. Against task236 (a notified share read through a sentinel network's positivity)
  and task258 (each slow load rebuilt part by part), no second channel is used and nothing is rebuilt from components.
- **Sources.** The client's two-layer standard; register-based housing statistics (dwelling occupancy from the
  population register's registered residents, the official statistics convention this task's regulation sets aside);
  utility-data vacancy statistics (a dwelling counted vacant below a consumption floor over a period, the field's
  method at rung 1); smart-meter occupancy detection from load profiles (the household's daily activity cycle);
  Norway's centralised meter-data hub, its hourly reads and quality codes, and its meter point register;
  the Norwegian land register's public titles from before organisation numbers.

## Default path

The path a competent analyst takes after conforming every file correctly and reading both governing documents (figures
from the generator's checks on the built pack).

1. Read the regulation: the dwellings counted are the cadastre's Bolig units in use on or before 1 November 2026
   (Section 3); a dwelling is vacant when nobody lived in it on any day of 9 to 22 November 2026, whatever the register
   shows (Section 4); the office reads it from the hub's metered values with the cadastre (Section 5); 5.0 per cent or
   more of a municipality's counted dwellings qualifies it (Section 6).
2. Conform: 8,020 counted dwellings; each joined to its household metering points by the cadastre's unit ID, else by
   municipality and address for a single-unit house (Snøholt's points still under Fjordeid's old number 5809); the
   hourly values from UTC to Norwegian time, each hour once with the later delivery kept, a changed meter's two points
   added; the hub's daily values agree with the hourly ones summed.
3. Try the field's vacancy-from-meters rule, a consumption floor on the fortnight's average daily use: no municipality
   qualifies at any floor from 1 to 10 kWh a day, and the vacant dwellings use more than the lived-in (a median 22.8
   against 20.4 kWh a day). An empty dwelling in a Norwegian November is heated, so the analyst sets the level aside.
4. Read occupancy from the household's day instead: the morning (06 to 09) or evening (16 to 22) mean over the night
   (01 to 05) on any day, a dwelling lived in when some day rises. The rise is cleanly bimodal, nothing between 0.3 and
   0.8 kWh, and the dwellings it calls empty mostly have nobody registered on 1 November, so it validates.
5. Count: 326 vacant (70 vacant dwellings heated on a daily timer rise every morning and evening and read as lived in);
   share by municipality.

Ends on: Tverrvika and Ørnevik alone qualify (6.2 and 7.1 per cent), at every rise cut from 0.3 to 1.0 kWh.

Golden: five municipalities qualify (Tverrvika 7.3, Hesteby 6.4, Solmoen 6.5, Ørnevik 8.2 and Fjordeid 5.4 per cent).
Hesteby, Solmoen and Fjordeid fall under the line on the rise (4.6, 4.7 and 4.5 per cent) because their timer dwellings
read as lived in.

## Stump sentence

A competent solver conforms the cadastre and the hub's hourly values, sees that an empty dwelling in a Norwegian November
is heated so no consumption floor works, reads occupancy from the household's morning or evening rise over the
dwelling's own night-time use, sees it separate cleanly and agree with the register, and files that Tverrvika and Ørnevik alone qualify (6.2 and 7.1 per cent); 70 vacant dwellings were left heated on a daily timer that rises at the same hours by the same amount every day,
and only a household's departure from what the dwelling repeats every day, some hour more than 0.9 kWh above its own
typical day, shows that someone lived there, which designates five.

## Deep reasoning

- **Task type:** census-register-administrative-data-quality in Survey Research & Official Statistics, which serves
  Data Extraction & Conformation: a register-based dwelling statistic conformed from the cadastre, the meter data
  hub's metering points and hourly values and the population register into one dwelling-level file under the
  regulation's contract, the designation read from it.
- **Domain test:** the quantity that decides is each municipality's vacancy share, an official estimate of true
  occupancy built from two error-prone administrative sources, and beside it the register's coverage errors measured
  against that estimate; the field's two estimators for the share are the register-based count (dwellings with no
  registered resident, net bias zero by construction) and the utility-data vacancy statistic (a consumption floor on the
  metered electricity), and both sit at the bottom of the ladder here.
- **Swap:** put hospital wards for dwellings and admissions for residents and the call reads "which hospitals have
  5 per cent of their wards empty"; a ward's occupancy sits in the admissions system, no ward is heated empty because
  of the climate while its register lists the departed, and the household's own day against the building's heating has
  no meaning, so the task stops making sense.
- **Layer 1:** the hub's UTC hour stamps; days first delivered as estimates and replaced by a second delivery; hours
  missing after communication faults; meters changed in the fortnight under a new point; Snøholt's points still under
  Fjordeid's number because the grid company's records lag the 2024 split; addresses in capitals, unit numbers with a
  space or missing on single-unit houses, some points without the unit ID; communal points at block addresses; the
  register's events after 1 November; the land register's late registrations; the outage hours; every item as its
  system produces it, nothing placed to be caught.
- **Layer 2:** classification from a measured signal (estimation_fit): the choice of what in a dwelling's metered
  record shows that someone lived there, the variation of its days beyond what the building's own load repeats, rather
  than the level of use, the daily rise or the register.
- **Decisive step:** recognising that the daily rise has two explanations, a household's day and a heating timer's
  comfort hours, and separating them by what each does across the fortnight: a timer repeats the same hours by the same
  amount every day and a household departs from it, so occupancy is read from whether some hour of some day ran above
  the dwelling's own typical day by more than its repeated load and noise allow.
- **Not semantics:** every field read correctly (kWh per hour, UTC stamps, the E and M quality codes, the two
  deliveries, unit IDs, Snøholt's old number) gives a correct level for each dwelling and day, and the level is not
  occupancy; the floor route reads every field right and still files that no municipality qualifies.
- **Not rule application:** no filed rule says how occupancy shows in metered values (Section 5 names the source only),
  and executing every filed rule leaves the construction open: the enumerated family spreads from no municipality to
  all ten (the register all ten; floors of 0.5 to 10 kWh a day none, higher floors four to all ten; the daily rise at
  any cut from 0.3 to 1.0 kWh Tverrvika and Ørnevik; a timer read with its cut inside the lived-in dwellings seven or
  all ten); what rules the floors out is the data's own structure (vacant dwellings using a median 22.8 kWh a day
  against 20.4 for the lived-in), what rules the rise out is the timer dwellings' identical days, both silent, and the
  departure members then agree on the golden five across a gap of 0.6 to 1.3 kWh.
- **Analyst test:** a strong analyst who conforms every file and applies every filed rule rejects the consumption floor
  (empty dwellings are heated), reads occupancy from the household's daily rise, sees it separate bimodally and agree
  with the register, and files that Tverrvika and Ørnevik alone qualify (6.2 and 7.1 per cent); a weaker one stops at the floor
  and files none.
- **Estimand:** Sections 3, 4 and 6 of regulation_vacant_dwelling_grant_2027.pdf: the counted dwellings (the cadastre's
  Bolig units in use on or before 1 November 2026), each vacant when nobody lived in it on any day of 9 to 22 November
  2026 whatever the population register shows, a municipality's share of its counted dwellings rounded to one decimal,
  qualifying at 5.0 per cent or more; the ministry's assignment (ministry_assignment_2026-12-01.eml) files the
  interval's basis (the counted dwellings taken as so many chances of a dwelling standing empty) and overcoverage,
  undercoverage and net bias with their denominators.
- **No decoy:** nothing is planted: no memo, briefing, draft or stakeholder figure argues the floor or the register; the
  regulation and the ministry's letter file the WHAT; the hub's, the cadastre's and the registers' files are what those
  systems produce.
- **No certified replay:** no certified, published or prior-year figure ships; nothing is recovered by reproducing a
  published share or count.
- **Chain:** (1) the register-based count, the field's first estimator, designates all ten and the consumption floor,
  its second, designates none at every floor from 1 to 10 kWh a day; (2) the vacant dwellings use more energy than the
  lived-in (a median 22.8 against 20.4 kWh a day), so the level carries the heating, and the household's daily rise
  over the night is the next reading, which separates bimodally, agrees with the register and gives 326 vacant,
  Tverrvika and Ørnevik; (3) the rise has a second explanation: 70 of the dwellings it reads as lived in rise at the same
  hours by the same amount every day of the fortnight, a heating timer, so occupancy is the departure of a day from what
  the dwelling repeats, some hour more than 0.9 kWh over its own typical day (no vacant dwelling reaches 0.6, every
  lived-in one 1.3), which gives 396 vacant and the five; (4) with occupancy estimated, the register's coverage errors
  follow (118 overcoverage, 556 undercoverage, net bias 5.5 per cent), each needing step 3, and the shares' intervals
  put Tverrvika, Hesteby and Ørnevik wholly above 5.0.
- **Judgment:** a measurement-model judgment, separating two explanations for one pattern by its variation: the rise is
  a household or a timer, and the analyst has to justify from the data that the dwelling's own repeated day is the
  baseline against which a household shows (variance beyond what the building's load repeats) and place the cut in the
  gap that statistic's distribution shows (0.6 to 1.3 kWh); a timer read as days alike lands on the same five only with
  its cut in its own statistic's gap (a mean correlation of the days from 0.955 to 0.98), and cuts inside the lived-in
  dwellings are ruled out by those dwellings' own hours (SF28).
- **One-fact test:** the hint that empty dwellings are heated in November leads to the rise, which lands on two; the
  hint that some heating runs on timers names the confound but not the reading: the solver still has to build a
  baseline from each dwelling's own days, set each day at its night, choose a statistic and a cut the data justify (a
  timer read with an unjustified cut gives seven or all ten), keep the outage hours from reading as activity, roll the
  register back to 1 November through the renumbered blocks and set the register's errors against the estimate. No one
  sentence makes it routine.
- **No replay:** no published or certified figure ships and nothing is recovered by reproducing one; no stated number is
  wrong.
- **Pinned:** every rival is run on the clean truth: the register designates all ten (ruled out by Section 4), every
  floor from 1 to 10 kWh none and higher floors four to all ten (ruled out by the records, C4), the daily rise at any
  cut from 0.3 to 1.0 kWh Tverrvika and Ørnevik (ruled out by the timer dwellings' identical days, C4), a departure
  either way with outage hours read as use (ruled out by the grid's outage log), a timer cut inside the lived-in
  dwellings (ruled out by their own hours, SF28), and every departure reading in SF12 the golden five; the interval's
  side is the same under the exact, Wilson, Jeffreys, Wald and Agresti-Coull intervals for the three wholly above
  (SF24), and net bias is filed as one ratio of counts (SF27).
- **Run forecast:** unfinished chain at rung 2: a strong run rejects the floor, reads the daily rise, sees it validate
  and files Tverrvika and Ørnevik, its 20 main figures, interval sides and all 50 register cells wrong; a weaker run
  stops at the floor (none) or the register (all ten), 0 of 50.
- **Strategy label:** WORKS IN FORM (Part A, heterogeneity is not this; the family is classification from a measured
  signal, Survey 03's register-auxiliary form read the other way: the second source is the estimate's evidence and the
  register its object), the live form being a decisive feature no column records and the field's own two estimators at
  rungs 0 and 1.
- **Lesson:** metered energy shows that a home is lived in through what its days do that the building does not repeat,
  not through their level or their daily shape, wherever the building's own load runs with nobody there on a schedule
  (heating on a timer in a cold climate).

## Survivor anatomy

- **Actor:** the dwelling has rows (a cadastre unit, its metering points, their hours), and whether anybody lived in it
  has no column anywhere: the register's residents are another quantity the regulation sets aside, and no file holds
  a household, an occupancy flag or a vacancy code.
- **Link:** the signal is a relation between rows of one dwelling's own record, each hour of each day against the same
  hour of the dwelling's other days, each day set at its own night, a comparison no key offers and the field's vacancy
  statistic never makes.
- **Reflex:** the field's methods for the quantity sit at rungs 0 and 1 (the register's empty dwellings designate all
  ten, the utility-data consumption floor none at any floor from 1 to 10 kWh a day), and the smart-meter reading of a
  household's daily cycle, the strong analyst's first move past them, at rung 2 (Tverrvika and Ørnevik).
- **Back-test:** the rung-2 route validates: the rise is bimodal (nothing between 0.3 and 0.8 kWh), and of the
  dwellings it calls vacant most have nobody registered on 1 November, so it agrees with the register where the
  register is right; the 70 timer dwellings it reads as lived in sit in the lived-in mass of every rise statistic.
- **Second use:** every file the decisive step reads (the cadastre, the meter register, the hourly values) is the
  regulation's own evidence under Section 5 and is read by every route to the call; deleting the step drops no file.
- **Shock:** the golden five are the top or bottom five of none of 20 shipped statistics (the register-empty share, the
  mean and median use, the shares under and over floors from 1 to 30 kWh a day, the share of flats, the dwelling count,
  the holiday homes), asserted in checks.py.
- **Pins:** the WHAT is filed in the ministry's regulation (Sections 3, 4 and 6); no filed sentence names an hour of the
  day, a daily pattern, a consumption level, heating or a test (asserted on both governing documents), and the
  regulation's register sentence rules out rung 0 only.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| R0 the register's empty dwellings on 1 November | Section 4's register sentence | the register's rows | the official convention | none | none | a count | yes | readable |
| R1 a consumption floor on the fortnight's average daily use | none | the hourly or daily values | the utility-data vacancy statistic | the register agrees with it | none | a filter | yes | readable |
| R2 the household's daily rise over the night on any day | none | the hourly values | the smart-meter occupancy reading | bimodal, and the register agrees | none | a within-day comparison | yes | readable |
| R3 (decisive) a day departing from the dwelling's own typical day | no sentence names an hour, a pattern, heating or a timer | no column holds occupancy or a timer | the field's readings are the level and the daily shape | the rise and the register agree with each other, not with it | the battery cleans the hours and stops | a comparison across a dwelling's own days | the files are the call's own evidence | silent |

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | counted dwellings | Bolig units in use on or before 1 November 2026 | units with no date, units taken into use later, holiday homes | more dwellings, unmetered ones vacant | Section 3 (a date of taking into use on or before 1 November 2026) |
| SF2 | vacant | nobody lived in it on any day of the fortnight | no registered resident on 1 November | all ten | Section 4 (whether anyone was registered does not decide) |
| SF3 | the fortnight's clock | Norwegian time | the hub's UTC hours | same call | same call (asserted) |
| SF4 | an hour delivered twice | the later delivery | the first, or both added | same call | same call (asserted) |
| SF5 | a meter changed in the fortnight | both points added | the current point only | same call | same call (asserted) |
| SF6 | communal points | not a dwelling's | joined by address where one dwelling has it | same call | same call (asserted) |
| SF7 | Snøholt's points under 5809 | joined by unit ID | joined by address under 5809 | same call by ID | the meter register's unit IDs (asserted complete for Snøholt) |
| SF8 | the threshold | on the share rounded to one decimal | on the unrounded share | same call | same call (asserted, no share within 0.2 points of the line) |
| SF9 | the municipalities | the ten as they stood on 1 January 2026 | Fjordeid with Snøholt | same call | Section 2 |
| SF10 | missing hours | the day read on the hours present | a day with a gap left out | same call | same call (asserted) |
| SF11 | outage hours | read as recorded (zero) | left out | same call | same call (asserted) |
| SF12 | the household's day | some hour more than the cut above the dwelling's own typical day (the median of its days hour by hour, each day set at its night), on any day | nights 00 to 06 or 02 to 05, the typical day as the quartiles' mid-point, two-hour blocks, any cut from 0.7 to 1.2 kWh | same call | same call (asserted, every member separates with a gap of 0.6 to 1.3 kWh) |
| SF13 | on any day | a household on one day makes it lived in | the rise averaged over the fortnight | another set | Section 4 (nobody lived in it on any day) |
| SF28 | a heating timer | read off the departure from the dwelling's own typical day | the rise with days alike read as a timer (the days' mean correlation at 0.955 to 0.98), or the rise's spread under 0.10 kWh; or either with its cut inside the lived-in dwellings (correlation 0.90, spread 0.20) | the golden five in the gap; seven or all ten inside it | the records: each lived-in dwelling such a cut calls empty has an hour at least 1.3 kWh above its own typical day, a household on that day (Section 4); asserted |
| SF29 | a departure either way | above the typical day only | above or below, outage hours read as use | Solmoen and Snøholt gain households | the grid company's outage log: those hours had no supply (asserted with them left out) |
| SF30 | the hub's daily values | the hourly values decide; the daily values agree with them | the daily values for the level | the same floors, the same none | same call on every floor (the daily values are the hourly ones summed, estimated where hours are missing) |
| SF14 | a two-unit house | two dwellings | one | same call | Section 3 (dwelling units) |
| SF15 | holiday homes and care homes | not counted | counted | not in the extract | Section 3 |
| SF16 | table A, held on 1 November | the register's state that day | by event date against registration date | same persons | same call (asserted, no event straddles the day) |
| SF18 | table A, a block's renumbering | a change of unit number | a move | the old ground floors' residents lost | the records (every resident, one day, one floor up, old numbers absent from the cadastre) |
| SF24 | the share's 90 per cent interval | the exact binomial interval on the counted dwellings, filed in the assignment (the counted dwellings as so many chances of a dwelling standing empty), graded on which intervals lie wholly above 5.0 | the Wilson, Jeffreys, Wald or Agresti-Coull interval | the bounds move by up to 0.1; the three wholly above (5802, 5803, 5807) do not | the assignment files the exact binomial interval (asserted, and the golden's bounds are its bounds); only the wholly-above side is graded, the same under all five, every lower bound at least 0.05 points from 5.0 (asserted) |
| SF25 | what the designation rests on | the estimated share, as Section 6 sets it, the interval reported beside it | the whole interval above the threshold | three qualify (5802, 5803, 5807) | the prompt (judged on the estimated share, the interval beside it) and Section 6 (asserted) |
| SF26 | overcoverage and undercoverage rates | over the counted dwellings where the register held someone, and over those where it held nobody, on 1 November | over all counted dwellings, or registration on 5 January | every rate moves | the assignment's two denominators and its date (asserted) |
| SF27 | net bias | the dwellings where the register held nobody less the vacant ones, over all counted dwellings | the difference of the two rounded shares | Tverrvika and Hesteby move by 0.1 | the assignment files it as one ratio of counts (asserted) |

## Ladder

| Rung | Construction | Designates | Main figures kept |
|---|---|---|---|
| R0 | the register's empty dwellings on 1 November (the official convention) | all ten | 0 of 20 |
| R1 | a consumption floor of 1 to 10 kWh a day (the utility-data vacancy statistic) | none | 0 to 1 of 20 |
| R1b | floors of 10.5 to 15 kWh a day | four to all ten | 0 to 1 of 20 |
| R2 | the household's daily rise over the night on any day, any cut from 0.3 to 1.0 kWh | Tverrvika, Ørnevik | 0 of 20 |
| R2b | the register's empty dwellings with no daily rise | none | 0 of 20 |
| G | a day departing from the dwelling's own typical day | Tverrvika, Hesteby, Solmoen, Ørnevik, Fjordeid | 20 of 20 |

Margins: the golden shares sit at least 0.27 points from the rounding line (Snøholt 4.68, Fjordeid 5.36); the counts are
exact because the departure separates every dwelling (lived-in minimum 1.3 kWh, vacant maximum 0.6); on the rise the
three dropped municipalities sit at 4.6, 4.7 and 4.5, well under the line. No floor from 0.5 to 30 kWh a day and no rise
cut from 0.3 to 1.0 kWh designates the golden five.

## Closure table

| Axis | Reading in this build | Move |
|---|---|---|
| 1 Population | the counted dwellings: Bolig units in use on or before 1 November 2026 (Section 3); units with no date, taken into use later, holiday homes and care homes out | filed in Section 3; C1 on the data (SF1) |
| 2 Unit of account | the dwelling (a cadastre unit), a two-unit house two dwellings; the municipality for the share | filed (Sections 3 and 6); SF14 |
| 3 Attribution window | 9 to 22 November 2026, every hour of the fortnight read; the hourly values cover exactly that fortnight | filed in Section 4; C1, nothing at the edges moves a dwelling (SF3) |
| 4 As-of dating | the dwellings as at 1 November (in-use date); municipalities as at 1 January 2026; registration on 1 November for the coverage figures | filed in Sections 2 and 3 and in the ministry's letter; SF9, SF16, SF26 |
| 5 Version basis | the hub's later delivery where an estimated day was replaced | C1: first, latest and both give the same call (SF4) |
| 6 Denominator | the municipality's counted dwellings | filed in Section 6 |
| 7 Weighting | none: a count over a count | filed in Section 6 |
| 8 Window length | the whole fortnight, a dwelling lived in if any day shows a household | filed in Section 4 (on any day); SF13 records the averaged reading's other call |
| 9 Boundary inclusivity | 5.0 per cent or more qualifies | filed in Section 6; no share within 0.2 points of the rounding line (C1) |
| 10 Rounding path | each share rounded once to one decimal, the threshold read on the rounded share; the coverage rates and net bias each one ratio rounded once | filed in Section 6, the prompt and the assignment; C1, the unrounded reading gives the same call (SF8); SF24, SF27 |
| 11 Tie-break | none needed: the designation is a set, no ranking | C1 |
| 12 Maturity and censoring | none: the fortnight is closed and fully delivered; a few hours missing per meter | C1 (SF10) |
| 13 Order of operations | join, clock, deduplicate, classify, count | C1: each order prints the same call (SF3, SF4, SF5 asserted on every variant) |
| 14 Row order | none: every step is a set operation keyed by point and hour | C1 |
| 15 Duplicate resolution | an hour delivered twice (estimate then measurement): the later | C1 (SF4) |
| 16 Identity normalisation | point to dwelling by the cadastre's unit ID, else by municipality and address for a single-unit house; Snøholt's points under 5809 carry their IDs | the systems' own keys; C4 on the address-only join (SF6, SF7) |
| 17 Netting against gross | a dwelling's two points (a changed meter) added hour by hour | C1 (SF5) |
| 18 Dimensional units | kWh per hour throughout, one unit in the hub's file | units in the data |
| 19 Code and status semantics | kundekategori Husholdning against Fellesmåling; the quality codes E and M | the hub's own codes; C1 (SF4, SF6); never the stump |
| 20 Integerisation | whole dwellings and persons; nothing allocated | C1 by construction |
| 21 Clause scope | Section 4's register sentence decides vacancy only; the register is the object of the coverage figures | filed scope (Section 4, the ministry's letter) |
| 22 Forward window contents | the grant pays in March 2027 on the certified figures; nothing forecast | filed in Section 8; retrospective by the regulation's design |

## Literal reader

Executed word for word, the prompt and Sections 2 to 7 file the counted dwellings, the fortnight, the share, its rounding
and the threshold (SF1, SF8, SF9), and file vacant as nobody having lived in the dwelling on any day of the fortnight
whatever the register shows; Section 5 names the evidence and not how it shows occupancy, so the literal reader has to
decide what in a dwelling's metered values shows that someone lived there. Every reading that decides it from the
dwelling's own days, some hour of some day above its own typical day in any form SF12 lists, gives the golden five; the
register's reading is ruled out by Section 4's last sentence, the averaged reading by Section 4's "on any day", every
consumption floor by the records (C4: the vacant dwellings use a median 22.8 kWh a day against 20.4 for the lived-in),
and the daily rise by the records (C4: 70 dwellings rise at the same hours by the same amount on every one of the 14
days, a repetition no lived-in dwelling shows, and none of their hours ever leaves its typical day by 0.6 kWh). A timer
read as days alike gives the golden five with its cut in its statistic's gap and is ruled out inside the lived-in
dwellings by their own hours (SF28); a departure either way is ruled out by the outage log (SF29). Each convention the
call needs is closed in the fork table (SF3 to SF15 the same call, asserted), and each term of the register-quality
figures and the interval by the ministry's letter or the records (SF16, SF18, SF24 to SF27). Every step of the
write-up executes as written.

## Oracles

No shipped file ranks the municipalities on the call: no vacancy share, occupancy flag, household, timer or count of
empty dwellings is filed anywhere. The register is the one second source on occupancy and the regulation sets it aside;
it agrees with the floor and with the rise (the back-tests), not with the golden. The outage log documents zero hours in
three municipalities, which rule out a departure read either way (SF29) and nothing else; the municipality list
documents Snøholt's split (SF7). The hub's daily values are the hourly values summed by day, estimated where hours are
missing, and give every floor the same call (SF30). The registration behind the coverage figures has only the event log
as its referee (every resident of a renumbered block moving one floor up on one day, the cadastre holding only the new
numbers). The land, business and shareholder registers and the day-ahead prices are read by no ask and ship as
distractors. Nothing ties only under the golden.

## Ask sheet

**The register beside the vacancy figures: each municipality's overcoverage and undercoverage on 1 November 2026, each
as dwellings and a rate, and its net bias** (50 figures, the assignment's terms, SF26 and SF27). H18: the pilot asks
whether the register could carry the count in later years, which only the coverage errors against the estimate answer;
the call reads no register row. The asks ride the deep step: every figure is the register set against the occupancy
estimate, so a run on a consumption floor (0 to 2 of 50), the register (0 of 50) or the register's empty dwellings with
no household day (20 of 50) loses nearly all of them. Second judgment, carried from architecture 2's table A: the
registration on 1 November, the register of 5 January rolled back through the November block renumberings (device D2,
a label stored before a silent switch), which moves the coverage counts in the renumbered blocks. Stops: the register
as it stands 18 of 50; every event undone as written, the renumberings as moves (the cracker) 12 of 50; the dead and
the emigrated not added back 35 of 50. Path: the register of 5 January, the event log, the cadastre, the meter files
(the occupancy estimate). Realism: municipalities renumber flats to the national unit-number standard block by block,
and the register writes each change as a move.

**Each share's 90 per cent interval** (graded on its side only: the three wholly above 5.0, SF24). The basis is filed,
no method is; the bounds are shown and not graded.

Main population zero-counts: the call reads the cadastre's counted units, the meter register and the hourly values; no
register event is among them, and the call computed from those three files alone is the golden (asserted). The cadastre
and the meter register carry no old ground-floor number of a renumbered block (asserted), so the renumbering device's
rows sit only in the register's files.

| Hazard | Asks moved | Cells kept of 50 |
|---|---|---|
| a block's renumbering read as moves (D2) | register table | 12 |
| the snapshot as it stands (D2) | register table | 18 |
| the dead and the emigrated not added back (D4) | register table | 35 |

Referee: the event log for the renumberings.

| Ask row | The cracker (landed the call, hygiene battery, every filed rule executed) | Verdict |
|---|---|---|
| Register table, overcoverage and its rate | the register of 5 January rolled back by undoing every later event as the register writes it, the renumberings as moves | kept in six municipalities, missed in Hesteby, Kvernhaug, Fjordeid and Snøholt |
| Register table, undercoverage and its rate | the same | miss |
| Register table, net bias | the same | miss |
| The intervals wholly above 5.0 | the same three | kept |

Measured by: generator/ceiling.py on the cut pack: the cracker keeps 12 of the 50 register figures; the best mirror (a
consumption floor of 10.5 kWh a day) keeps 1.4 of the 38 recommendation points and 0 of 50, and the strong run's rung,
the daily rise at any cut from 0.3 to 1.0 kWh, keeps 0 of the 38 and 0 of 50.

Pair ceiling: 33.3 ((38 + 7 + 55 x 12/50) and (1.4 + 7 + 0), averaged); the main block's 38 is the call's 8, 1.35 for
each of the 20 municipality figures (vacant dwellings and share) and 3 for the intervals lying wholly above.

Shallow keep: 0.0 per cent of ask weight (the default path, a consumption floor anywhere from 1 to 10 kWh a day, keeps 0 of the 50 register figures and no interval side)

Mirror leakage: 0.0 per cent of ask weight (no mirror keeps a register cell: the daily rise reads the 70 timer dwellings as lived in, which moves overcoverage, undercoverage and net bias in every municipality)

## Prompt contract

The author's voice rewrite may not drop or change: the question (each municipality's share of counted dwellings vacant
in the fortnight of 9 to 22 November 2026, estimated from the register and meter data, and which municipalities it
qualifies for the 2027 vacant dwelling activation grant); the hold being grammatical ("any qualifying
municipalities"); vacancy_grant_certification_2027.docx with the qualifying names, each municipality's vacant
dwellings, share and 90 per cent interval, the chart of shares and intervals against the threshold, and each
municipality's overcoverage and undercoverage on 1 November 2026, each as dwellings and as a rate, and its net bias;
county_dwelling_occupancy_2026-11.xlsx with every counted dwelling, its municipality, the persons registered on 1
November 2026 and whether it stood vacant; shares, intervals, rates and net bias as per cents to one decimal. It may not
name an adjustment, a correction, the meter's daily shape or an interval method.

## Pre-ship check

1. Domain: the call stands on each dwelling's occupancy in the fortnight, read from its own hourly electricity record as
   a household's day against the building's heating; with wards for dwellings there is no heating left on in an empty
   home, no register that lags, and no household's day, and the task stops making sense.
2. Two layers: Layer 1 (the hub's clock, deliveries, gaps and meter changes, Snøholt's old number, the address and unit
   formats, the communal points, the outage hours) is cleaned by the battery and moves nothing (SF3 to SF11 asserted);
   Layer 2, what in a dwelling's record shows that someone lived there, decides the call.
3. No plant, semantics or rule application decides: the floor reads every field right and every filed rule applied and
   files none; no sentence names the household's day; the register and the floor are the field's own methods.
4. Determinism: the WHAT filed in Sections 3, 4 and 6 and the ministry's letter; the household-day family converges on
   the golden five across every member and cut (SF12); the tables' terms closed (SF16 to SF23).
5. Gates on the final cut (target.zip sha256 52fc465dedb924b1, after the shareholder register's realism pass, no figure
   moved): generator checks 84 of 84, the verifier on every
   graded figure, two byte-identical builds, figures_check.py 123 of 123, precut.py 61 of 61, voice-check.py PASS,
   leak.py REVIEW with no LEAK, guard.py surface clean and heart WARN only on the question form (a gate asks
   whether); the leak reader found no leak, and the determinism judge returned DETERMINISTIC, APPROVE (SF19 closes its
   one low note, the deed's date against the registration date).
6. leak.py REVIEW, sweep 3: the regulation's 5.0 is the threshold Section 6 files, shared by every reading,
   harmless.
7. leak.py REVIEW, sweep 4: the regulation's section, statistics, fortnight, points, office and cadastre are its
   own nouns, none names the decisive step, harmless (ruled here, not sent to the reader).
8. Domains Fit repair (portal, 2026-11-07: the prompt read as a regulation's threshold applied to counts and
   shares): the question now asks for the grant judged on the estimated share of each municipality's housing standing
   vacant, from the register and meter data, with that share's 90 per cent interval beside it, and the letter charts
   each share with its interval; the designation rests on the share (SF25, the judge's mild fork closed). The interval is a reporting statistic the ministry's letter files as the exact binomial interval on the
   counted dwellings (SF24); Wilson, Jeffreys and the normal approximation round differently somewhere, which is why
   the convention is filed, and the call does not move with any of them. The intervals of Kvernhaug, Solmoen,
   Ravnsund, Fjordeid and Snøholt take in the 5.0 line; the regulation designates on the share. The decisive step is
   unchanged: what in a dwelling's own hourly record shows that someone lived there.
9. Metadata repair (leak.py sweep 10): the regulation is exported by LibreOffice Writer (generator/officepdf.py), the
   ministry as Author and a real Subject; the hub's extract is written with no Arrow schema and no created_by
   (generator/parquetio.py), its timestamps read back in milliseconds, UTC, the same values.
10. Critical component 3 corrected at the judge's read (2026-11-07): a resident who left a renumbered block before
   its day from a flat nobody else held that day (Haugveien 6 H0302) is read one floor up like the rest of the block,
   as the world renumbers every flat; lived in with nobody registered is 556, not 557, and every counted dwelling's
   persons now equal the world's (asserted).

11. Domains Fit design repair (2026-11-08, no new architecture): the deciding figure is each municipality's vacancy
   share as an official estimate of true occupancy from two error-prone sources, and the asks are the register's
   coverage errors against it (overcoverage, undercoverage, net bias, SF26, SF27) with each share's interval graded on
   its wholly-above side (SF24); the call, the stump, the ladder and every Final Recommendation and Critical Components
   figure unchanged. Gates on target.zip 5cf39da4694631c8: checks 82 of 82, the verifier, two byte-identical builds,
   figures_check 128 of 128, precut 72 of 72, voice-check PASS, the input-files tell sweep clean, guard heart WARN
   only, surface exit 0 with one promoted pair (task4 v4) for the author; leak.py LEAK on sweep 10 only, the
   regulation PDF's Creator 'Writer' that LibreOffice writes, outside the sweep's tool list.

12. Stump deepened (2026-11-08, after the judge's SEND_BACK on Gate H): heating on daily timers in the world, the
   decisive step the departure of a day from the dwelling's own typical day (gap 0.6 to 1.3 kWh, cut 0.9), the rise now
   rung 2 (Tverrvika and Ørnevik at every cut from 0.3 to 1.0 kWh), the hub's daily values shipped as a CSV of 113,758
   rows; the call, every share and every register figure unchanged. Gates on target.zip 13a7d9af90ef518c: checks 95 of
   95, the verifier, two byte-identical builds, figures_check 134 of 134, precut 72 of 72, voice-check PASS, guard
   check WARN and heart WARN (forum and forcing event redrawn to funder_or_donor and budget_or_appropriation), surface
   exit 0, leak.py REVIEW with no LEAK (the daily file's "13,599" is one meter's day of 13.599 kWh, not the persons
   total, harmless), the pair ceiling 33.3, mirror leakage 0.0.

13. Stage 4 on 13a7d9af (2026-11-08): the leak reader found no leak (no file names the vacancy method, nothing names a
   timer, thermostat or schedule, no ranking file, no reserved domain or tell; "so many chances" read as a binomial
   basis, deliberate; the January extracts' 1 November rollback, intended). The judge: DETERMINISTIC, Gate H passes
   (analytical; the classifier choice is the statistical judgment; the rise rival lands on two and is unstable), one
   FIX_NOW: the interval's method unnamed, the exact, Wilson and Jeffreys bounds differing by up to 0.1. Fixed as a
   convention pin in the assignment, "the exact binomial interval, as in the office's register statistics" (SF24,
   asserted), never in the prompt; the interval is not the stump and no graded figure moved.

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
