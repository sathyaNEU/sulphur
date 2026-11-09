# task7 design note (architecture 6)

Architectures 1 to 5 survive only in the Tried and rejected record at the end of this note and in git; architecture 5's
pack, generator and goldens were removed at the re-root on 2026-11-08 (READY commit c404109 holds them), and its one
platform run is kept as evidence in `runs/arch5/run1.md`. Architecture 6's first mechanism (take-up of a once-only offer
driven by a rise in use) was priced and redrawn at design the same day, before any pack existed; its line is in Tried and
rejected.

## Draw

- **Card:** `.claude/skills/fingerprint/cards/task7.json`, architecture v6, lineage v1 to v5, registered 2026-11-08 and
  re-registered the same day when the mechanism was redrawn (the first mechanism's driver is kept in the card's notes),
  at WARN only, and re-checked on the registered card. The redraw moved the decisive gap from population to time and the
  generators to G5, G16 and G17, because the first gap, pattern and decision type repeated task8's lineage (BLOCK
  `test.same_puzzle`); time is the honester key, since the decisive step dates each comparison building's visit and
  uses it only for the seasons before it.
- **WARNs answered:** `repeat.gate_g` (decomposition_attribution, against task3 v5): task3 separates a storm driver from
  a catchment response inside flood maxima; here a narrowing gap between the works buildings and the comparison is split
  between the works, which hold, and a second programme that treated the comparison buildings, a different mechanism on
  a different record. `repeat.question_form` (which, against task3 v5): the decision designates measures, so a "which"
  question is the decision's own form.
- **Pairing:** Energy Systems & Utilities, task type `efficiency-savings-verification` (energy efficiency and demand
  response evaluation), which serves Experiment & Causal Analysis: the effect of each retrofit measure on a commercial
  building's gas use in a season of long-term average weather. The call faces forward: which measures the council funds
  in its 2026 grant round, a round whose works and savings have not happened.
- **Shape:** 07, a grid of cells: the three measures, each with its saving rate, its grant per tonne on the 2026
  applications and its verdict against the council's limit; every funded application received with its expected saving
  and lifetime tonnes; the funded round's grant and lifetime tonnes once the offer closes; and the pilot's 2025/26
  saving.
- **Strategy:** `causal_design` (a comparison that is actually clean), Gate G `decomposition_attribution`, generators G5
  (provision elsewhere: the comparison buildings received the service team's tuning), G16 (method selection) and G17.
- **Strategy label (`sulfur-strategies.md`):** WORKS IN FORM, a comparison that is actually clean, in its live form: the
  contamination is visible only through a relation in the data (each passed-over building's service-visit read against
  its later seasons, and no such read among the works buildings), never a column, schema or filed sentence; the
  comparison is never filed in the estimand; and after the clean comparison is taken the chain still carries the
  appraisal of the 2026 round, the round carried to the offer's close from the 2019 responses' timing measure by measure,
  and the pilot's 2025/26 saving on what its buildings would have used that season. The family's nearest
  client case is Example 4 (a second resource reaching the waiting units after the rollout began).
- **Data-native sentence:** Haldenau's 2019 retrofit pilot drew its places by lot among the owners who answered the
  benchmarking notice's offer, but from August 2019 the utility's service team tuned the burners of its commercial
  customers district by district, free of charge, and passed over every building with pilot works, so the passed-over
  owners' gas use stepped down one district at a time and the lottery's comparison narrows season after season as if
  the works' savings were fading.
- **Abstraction sentence:** the card's driver: the effect of a treatment assigned by lottery, where the units the lottery
  passed over were reached one area at a time by a second programme that skipped the winners and moved the same outcome
  for good, so the randomised comparison narrows period by period as if the effect faded; only passed-over units the
  second programme had not yet reached give the counterfactual. Against the nearest builds on file it is none of theirs:
  task9 keeps a second-round effect inside an area, mark128 reads a contact's effect only where the queue outran the
  team, task8 v5 regresses value on traded units, task4 v3 apportions unrecorded passage between nodes.
- **World:** Stadtwerke Haldenau, the fictional municipal utility of Haldenau (Baden-Wuerttemberg, about 450,000
  inhabitants), supplies gas to about 24,000 commercial buildings. Each May its benchmarking notice goes to the buildings
  whose normalised use per square metre is in the top fifth of their type. The council's 2019 pilot offered a grant in
  that May's notice (insulation, heating optimisation, heating controls; 30 per cent of the quoted cost, at most
  €40,000), each answer with a contractor's quote by 30 June; 2,791 owners answered, 1,256 places were drawn by lot on 8
  July 2019 and 1,218 buildings had their works by 30 September 2019. The 2026 round offers the grant again in the
  notices of 20 May 2026, open to 30 June; 870 applications came in by 12 June 2026, and the committee's paper goes out
  on 26 June, before the offer closes. The climate committee (chair Magda Peukert) sets the round on 9 July 2026; the analysis comes from the utility's
  energy services (Torben Römer, head). People drawn with `guard.py names --geo Germany --seed 11`. Currency EUR.
- **Sources (all constructed for this task, seeded and deterministic; nothing real is described):** the gas meter reads
  (meter point by read date, May 2013 to April 2026: periodic reads at 30 April, interim and service-visit reads, meter
  exchanges, estimates and corrections, the large messy CSV); the meter points (building, z-number, meter factor,
  network area); the billing calorific values by network area and season; the building register (address, district,
  type, floor area); the benchmarking notices 2019 to 2026 (the long CSV); the pilot's responses and draw; the 2026
  applications; the Haldenau station's daily temperatures and its monthly degree days with the 1991 to 2020 means; the
  council's climate action plan extract (the saving rate, normal weather, the appraisal, the limit); the pilot's rules;
  the utility's benchmarking method; the committee chair's request; distractors a planner would weigh (the utility's
  electricity customers' annual use, the solar cadastre's rooftop potential, the municipal heat plan summary, the
  federal funding overview).

## Default path

1. Build each building's gas use per season (1 May to 30 April) from `gas_meter_reads_2013_2026.csv`: index differences
   between the periodic reads of 30 April, carried across meter exchanges, counter rollovers, interim and service-visit
   reads, corrections and estimates, converted from cubic metres to kWh with each meter's z-number and factor
   (`meter_points_2026.csv`) and the season's calorific value for its network area (`calorific_values_2013_2026.csv`),
   summed over a building's meter points (`buildings_register_2026.xlsx`).
2. Normalise every season as the utility's benchmarking method does (VDI 3807: the type's hot-water share held, the rest
   scaled by the long-term G20/15 over the season's, `degree_days_haldenau.csv`).
3. Read the pilot as the randomised trial its draw made (`pilot_2019_responses_and_draw.xlsx`): for each measure, the
   drawn buildings that had the works against the answering owners the draw passed over, each against its own 2019
   notice season, in every season since the works (the field's comparison-group billing analysis, a difference in
   differences).
4. Saving rates, in whole per cent as the plan takes them: insulation 13, heating optimisation 2, heating controls below
   zero.
5. The plan's appraisal on `applications_2026.xlsx`: insulation €110 a tonne, heating optimisation €280, heating
   controls no saving at all.

- **Ends on:** fund insulation alone in the 2026 round; heating optimisation fails the limit at €280 a tonne and heating
  controls saves nothing.
- **Golden:** fund insulation and heating optimisation at €90 a tonne each, heating controls failing at €220; saving
  rates 16, 6 and 2 per cent; the funded round about €8 million of grant and 90,000 lifetime tonnes once the offer
  closes (386 funded applications for €3.25 million received by 12 June); the pilot's works saved about 3,500 tonnes of
  CO2 in 2025/26.

## Stump sentence

The default path reads the pilot as the randomised trial it was drawn as, sets the works buildings against every owner
the draw passed over, finds insulation 13, heating optimisation 2 and heating controls below zero, and funds insulation
alone (heating optimisation at €280 a tonne against the €120 limit); the step that lands it there is trusting a
comparison the utility's service team was treating one district at a time, for from August 2019 it tuned the burners of
most passed-over buildings and skipped every works building, and against passed-over buildings not yet tuned heating
optimisation saves 6 per cent at €90 a tonne and is funded.

## Deep reasoning

- **Task type:** efficiency-savings-verification (energy efficiency and demand response evaluation), which serves
  Experiment & Causal Analysis.
- **Domain test:** the deciding quantity is each measure's saving rate on weather-normalised gas use, the measurement and
  verification question of what the works saved against what the building would have used, worked the way the field
  works it (metered use, the utility's VDI 3807 degree-day normalisation, a comparison group of untreated buildings);
  the call turns it into grant per tonne of CO2 over each measure's service life.
- **Swap:** "fund insulation and heating optimisation but not heating controls, because set against passed-over
  buildings whose burners were not yet tuned heating optimisation saves 6 per cent of normal-weather gas", read with a
  hospital's nouns ("fund ward programmes A and B but not C, because set against wards the second programme had not yet
  reached B saves 6 per cent"), keeps its skeleton and loses what decides: the season's degree days the use is
  normalised by, a burner whose tuning cuts the same metered gas the works cut, the read a technician takes at the visit
  that dates it, and the service lives and the gas CO2 factor that turn a saving rate into grant per tonne.
- **Layer 1:** cumulative meter index reads at the 30 April reading date, with meter exchanges (a removal read and a
  fitting read), five-digit counter rollovers, periodic reads taken late in May or June, interim and service-visit
  reads, customer reads corrected later, estimates replaced by actual reads, duplicate rows from a re-import, meters
  with a factor of ten, the z-number per meter and the billing calorific value per network area and season, a second
  meter point on some buildings, buildings connected or disconnected mid-series; every item is a billing system's own
  product and none decides (asserted in `checks.py`).
- **Layer 2:** estimand_identification, `causal_design`: the comparison that is actually clean when the randomised
  comparison group was treated after the draw by a second programme that skipped the treated units.
- **Decisive step:** recognising that the owners the draw passed over were not left alone: the service-visit reads in
  the meter file date the visit at which the utility's service team tuned a building's burner, district by district from
  August 2019; every passed-over building's normalised use steps down from its visit and no works building has a
  visit, so a passed-over building compares only for the seasons before its visit.
- **Not semantics:** every field read correctly (the read reason, the draw result, the measure asked for, the notice's
  normalised use, the reference consumption) and every Layer 1 item handled, the lottery comparison still files
  insulation 13, heating optimisation 2 and heating controls below zero, and the works buildings' own before and after
  files 24, 15 and 11.
- **Not rule application:** no filed rule says how the saving is estimated or which buildings compare: the plan files
  the saving rate as the share of a building's normal-weather use its measure's works save, taken from the pilot, and the
  appraisal formula. The enumerated family (the works buildings' own before and after; the lottery against every
  passed-over building on one, two or every season before, on the first season only, the seasons to 2022 or the last two;
  the offered owners who did not answer; everyone outside the pilot; read as drawn without a baseline; each with and without
  the visited buildings) spans heating optimisation from 1.6 to 14.8 per cent; the standing family (every comparison that
  drops a building from its visit season, averaged over the works buildings as the plan files it) spans 5.7 to 6.1, one
  whole per cent; the ruling-out is loud: visited passed-over buildings step down about 7 per cent at
  their visit against unvisited ones, and against unvisited buildings the gap holds flat from 2020 to 2026.
- **Analyst test:** the strong analyst cleans every read, normalises as the utility does, reads the pilot as a randomised
  trial and files the lottery comparison, insulation 13, heating optimisation 2 and heating controls below zero, so it
  ends on funding insulation alone; seeing the gap narrow from 4.1 points in 2020 to 1.6 in 2026, it reads the narrowing
  as savings fading and, carried over each measure's life, funds no more.
- **Estimand:** `climate_action_plan_2023_extract.pdf` section 4: the saving rate of a measure is the share of a
  building's gas use in a season of long-term average weather that the measure's works save, taken from the 2019 pilot
  as each works building's use as a share of its 2018/19 use set against the comparison buildings' average share (one
  less the first over the second), averaged over the buildings and seasons, in whole per cent;
  normal weather is the utility's benchmarking normalisation; an application's lifetime tonnes are the rate times its
  reference consumption times 0.201 tonnes per MWh times the measure's service life, and a measure is funded when the
  grant of the round's applications for it per lifetime tonne is €120 or less.
- **No decoy:** nothing is planted: no memo, report, briefing or figure in the pack states a saving rate, a before and
  after, a grant per tonne, the service team's work or a recommendation; the service-visit reads are the meter readings
  a technician takes, in the same file and format as every other read, one reason among seven.
- **No certified replay:** the pack certifies no saving and publishes no figure to reproduce; the method is not
  recovered from a published number.
- **Chain:** (1) the draw makes the passed-over owners the comparison, and against them the works' gap narrows every
  season (heating optimisation 4.1 points in 2020, 1.6 in 2026); (2) the narrowing is not the works fading: it follows
  the passed-over buildings' service-visit reads district by district, each building stepping down about 7 per cent from
  its visit, and no works building has a visit; (3) so each season's comparison is the passed-over buildings not yet
  visited, against which the gap holds flat (5.6, 6.1, 5.7, 5.5, 5.5, 6.1 and 6.5 points); (4) the saving rates are
  16, 6 and 2 per cent; (5) under the plan's appraisal the 2026 applications cost €90 a tonne for insulation and for
  heating optimisation, both funded, and €220 for heating controls, not funded.
- **Judgment:** separating two explanations for one narrowing gap, the works' savings fading against the comparison
  buildings being treated: the timing decides it (the narrowing tracks the passed-over buildings' visit seasons, while
  every works building's works are the same age), with the unvisited buildings' flat gap and the visited buildings'
  step at their visit; the modelling choice that follows is to censor each comparison building from its visit season,
  rather than model decay or defer to the randomisation.
- **Hidden by:** the narrowing reads as savings persistence fading, a pattern measurement and verification expects; the
  gas price shock of 2022 cut every building's use in the same seasons, so the passed-over buildings' falls read as the
  crisis; the draw balances the two groups on the notice season and on every season before it, a placebo on the
  pre-pilot seasons shows no gap, and a panel against buildings outside the pilot agrees with the lottery, because every
  building outside the pilot was tuned alike.
- **After the notice:** once a run sees the passed-over buildings' use stepping down, (1) it must decide that the step is
  a treatment of the comparison and not part of the counterfactual: a run that keeps the lottery's full comparison as the
  pilot's net effect (the randomisation's own answer) files the contaminated rates, while the plan's rate is what a
  measure's works save, which the 2026 applicants (most of them already visited, the visits over by April 2026) will
  get; (2) it must date each comparison building's visit from the reads and drop it from that season on, on the same
  baseline as the works buildings, rather than dropping the crisis seasons (heating optimisation 3 per cent) or reading
  the last seasons as the faded saving (2); (3) it carries the rates through the plan's appraisal; and two asks carry a
  judgment of their own after that: the funded round once the offer closes, where insulation responses come late (in
  2019 38 per cent of them were in by the same day after the notice, against 58 per cent for heating optimisation), so
  each measure scales by its own share (about €8 million and 90,000 tonnes; one pooled share €7 million and 80,000;
  the applications received €3 million and 40,000); and the 2025/26 saving, taken on what the works buildings would have
  used that season (3,500 tonnes), not on their 2018/19 use (4,000), which the gas price shock and the pull back from a
  flagged season have left behind.
- **One-fact test:** the likeliest hint is "the service team tuned the passed-over buildings' burners"; with it a run
  still has to find the visits among seven read reasons, see that the works buildings were skipped, censor each
  comparison building from its visit season, keep the comparison balanced on the notice season and carry the rates
  through the appraisal, the round at close and the 2025/26 saving; and without it the narrowing has two ready
  explanations, fading savings and the crisis, that every check confirms.
- **No replay:** the call re-derives no published figure, and no stated number in the pack is wrong.
- **Pinned:** every rival run on the cut pack (`checks.py`): the works buildings' before and after 23.6/14.8/11.2
  (ruled out: the 2019 notice season ran high, and the pandemic and the gas price shock moved every building); the
  lottery against every passed-over building, one-season base 12.9/2.4/-1.9, panel base 12.5/2.4/-2.2, first season
  only 13.4/4.1/0.5, seasons to 2022 13.9/3.4/-0.3, last two seasons 11.7/1.6/-3.4, read as drawn 12.1/2.7/-0.9 (per
  square metre 12.4/3.5/-2.8); the offered owners who did not answer 12.6/2.5/-1.7; everyone outside the pilot
  12.7/2.7/-1.6 (each ruled out by the service visits: visited buildings step down about 7 per cent at the visit, and no
  works building was visited); the golden family (passed-over buildings not yet visited on a one-season, two-season or
  every-season base, by measure or pooled, a mean of logs or by building; offered owners not yet visited) 15.6 to 16.0,
  5.7 to 6.1 and 1.7 to 2.0, every member 16, 6 and 2 in whole per cent under the plan's filed construction; the
  comparison's share as a ratio of totals (16.0, 5.3, 1.7) or an absolute difference over the 2018/19 use (14.6, 5.3,
  1.8), which the plan's 4.2 rules out, land the same call.
- **Run forecast:** one run reads the pilot as the randomised trial and stops at the lottery comparison (method
  shortcut), funding insulation alone; a run that sees the narrowing reads it as fading savings and carries the decline
  over each measure's life (self-confirming check: a declining saving fits every season); a run that notices the
  passed-over buildings' falls puts them down to the gas price shock and drops those seasons (dismissed own evidence),
  still funding insulation alone.
- **Strategy label:** WORKS IN FORM, a comparison that is actually clean, live form: the contamination read only through
  a relation in the data, the comparison not filed, two more inferences after it.
- **Lesson:** a randomised comparison stays clean only while nothing treats one arm after the draw; when a second
  programme reaches the comparison group one area at a time, the effect appears to fade, and the cure is to censor each
  comparison unit at its own treatment rather than model decay or defer to the randomisation; no build on file teaches
  it (task7 arch 4 priced spillover between customers; this slot's first architecture 6 mechanism, a selected rise).

## Survivor anatomy

- **Actor:** the deciding property (a passed-over building was tuned, and in which season) has no column: the draw file
  records drawn or not drawn, the register records districts, and the tuning shows only as a read a technician took at
  the visit, one read reason among seven in the meter file, read against the building's later seasons.
- **Link:** the signal is read through the relation between a building's service-visit read and its later normalised
  use, and the absence of any such read among the works buildings, across the meter file (by meter point), the meter
  points (to buildings) and the draw file; no key or sentence ties a visit to the comparison, and the field's comparison
  method never asks what happened to the comparison buildings after the draw.
- **Reflex:** the field's methods sit at rungs 0 and 1 and file wrong calls: the works buildings' before and after (IPMVP
  Option C) funds all three measures, and the comparison-group billing analysis on the lottery funds insulation alone.
- **Back-test:** the textbook route validates: the draw balances the groups on the 2019 notice season and on every
  season before it, a placebo on the pre-pilot seasons shows no gap, and a panel against buildings outside the pilot
  agrees with the lottery (every building outside the pilot was tuned alike), so the comparison passes the checks a
  careful run makes.
- **Second use:** every file the decisive step reads is in the pack for its own reason: the meter reads are the base of
  every saving (a service-visit read must be carried across like any interim read), the meter points map reads to
  buildings, and the draw file says which buildings had works.
- **Shock:** the movement the step recovers (the passed-over buildings' step down at their visits) reads as ordinary
  explained movement, the gas price shock having cut every building's use in 2022 and 2023 and a fading saving being an
  expected pattern; the funded set is not an interval of any shipped statistic's sort (the 2026 applications' grant per
  reference MWh-year puts heating controls cheapest, and the before and after puts all three under the limit).
- **Pins:** the WHAT is filed in the climate action plan, the council's own genre (the saving rate as the share of
  normal-weather use a measure's works save, taken from the pilot; normal weather as the utility normalises; the
  appraisal formula, the lives, the factor and the €120 limit); no filed sentence names the comparison, the passed-over
  owners, the service team, the visits or decay.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | 8 Framing | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| 0 works buildings' before and after | the plan's normal weather | no | yes, IPMVP Option C | no | no | yes | no | no | readable |
| 1 lottery against every passed-over building | the pilot rules' draw | the draw result | yes, the randomised comparison | no | no | no | no | no | readable |
| 2 decay read from the narrowing gap | no | no | yes, an event study | no | no | no | no | no | readable |
| 3 (decisive) passed-over buildings dropped from their service visit | no | a read reason among seven, no flag on the building | no, no field method asks what treated the comparison after the draw | no | no, the battery sums across interim reads | no | no, the reads are the base of every saving | no, the prompt and documents name no visit, tuning or fading | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | "the share ... that the measure's works save" | the works' own saving, against comparison buildings not yet tuned | the lottery's net comparison, tuning included | insulation alone | the plan's "that the measure's works save" (the tuning is not the works), and the 2026 applicants get no further visits (the last visits were in March 2026) |
| SF2 | "taken from the 2019 pilot" | the drawn buildings that had their works | every drawn owner, withdrawals included | same call | asserted: the 38 withdrawn owners move no rate across a whole per cent |
| SF3 | "normal weather" | the utility's benchmarking normalisation | raw use, or a degree-day regression | same call | asserted: the comparison is concurrent, every variant on the call |
| SF4 | the baseline | the 2019 notice season | two seasons, or every season to 2019 | same call, same whole per cent | asserted |
| SF5 | a visited building's last comparison season | the season before its visit season | the visit season kept | same call | asserted |
| SF6 | the comparison pool | answering owners passed over, same measure | every measure pooled; offered owners who did not answer | same call, same whole per cent | asserted |
| SF7 | the share a works building saved | its use as a share of its 2018/19 use against the comparison buildings' average share, one less the ratio, averaged over works buildings and seasons | the comparison's share as a ratio of totals (5.3 on heating optimisation), a geometric mean (5.7) or a median (6.0); an absolute difference over the 2018/19 use (5.3) | same call under each; the whole per cent moves only under the ratio of totals and the absolute difference | the plan's 4.2 files the construction (the average of the comparison buildings' shares, one less the first over the second); asserted |
| SF8 | "reference consumption" | as stated on the 2026 application | recomputed from the 2026 notice | same call | asserted: the application states the notice's figure |
| SF9 | "the grant" | the application's grant | the quoted cost | none funded at three times the grant | the plan's appraisal names the grant |
| SF10 | "€120 or less" | inclusive | strict | same call | C1: no measure within 20 per cent of the limit |
| SF11 | service lives and the factor | 30, 15 and 10 years; 0.201 t per MWh | other published lives or factors | none: filed | the plan's section 4 |
| SF12 | the round's applications for the grant per tonne | the applications received by 12 June | the round projected to its close | same grant per tonne to €10 | asserted: the projection scales a measure's grant and tonnes by one share |
| SF13 | "the funded round once the offer closes" | each funded measure's received applications scaled by the share of the 2019 responses for that measure in by the same day after the notice | one pooled share; the days elapsed; the applications received | €8 million and 90,000 tonnes against €7 million and 80,000, €6 million and 70,000, €3 million and 40,000 | the 2019 responses' dates by measure (insulation 38 per cent in by the day, heating optimisation 58); asserted over weeks, calendar dates and use types |
| SF14 | a building's meter points | summed | the main meter only | same call | asserted: the register maps every meter point |
| SF15 | late and estimated reads | carried by each read's own date, estimates replaced by the later actual read | estimates kept; reads off 30 April counted whole | same call, same 2025/26 saving to 500 tonnes | asserted |
| SF16 | rounding path | the council's rates in whole per cent into the appraisal (plan 4.2) | the rates unrounded | same call | the plan's 4.2; asserted |
| SF17 | "what the pilot's works saved in the season to April 2026" | each measure's rate on its works buildings' 2025/26 use divided by one less the rate | the gas without the works read off the comparison; the buildings had they been visited like their passed-over neighbours; the rates unrounded | 3,500 tonnes under each | the committee's request: the rate on the gas the buildings would have used that season; the 2018/19 use (4,000) and the use with the works (3,000) miss |

## Ladder

The pricing sequence, run on the cut pack (`generator/checks.py`, every rung):

1. **The residue the filed WHAT leaves** is a method question, which buildings and seasons compare, not a knob: the plan
   files what a saving rate is, where it is taken from and how it is averaged, and nothing on how the comparison is
   built.
2. **The move against the ceiling:** heating optimisation must move from the lottery's 2 per cent to its break-even 4.6
   to change the call; the largest move the tuning can make is its own effect on the comparison, about 7 per cent of the
   passed-over buildings' use, two thirds of them visited. The move needed is inside it.
3. **The one-group-by route** is the lottery's difference in differences (rung 1), which files 12.9, 2.4 and -1.9; the
   golden needs each comparison building's visit season, read off one read reason in the meter file and carried to the
   building through the meter points, and a comparison rebuilt season by season.
4. **Standard error of the step:** the golden family spans 5.7 to 6.1 per cent on heating optimisation, every member 6
   in whole per cent, against a break-even of 4.6; insulation 15.6 to 16.0 against 11.6; heating controls 1.7 to 2.0
   against 3.7.
5. **The lever and the ranked quantity** are not the same variance: the verdict is per measure against a fixed limit.
6. **The unit's own history:** each comparison building's visit is a step in its own series; the series' season to
   season spread (about 3 per cent) is under half the step, so the step is readable for a run that looks at a visited
   building, and a run must still decide what the step means for the comparison.
7. **A subset that hands the quantity over:** the passed-over buildings still unvisited in 2026 are the owners who
   declined the visit; they are part of the comparison the golden uses, and nothing marks them but the absence of a
   visit read.
8. **The reflex sweep:** every other way the pack measures the saving is enumerated below, each route's rates taken in
   whole per cent as the plan takes them.

| Rung | Route | Insulation, heating optimisation, controls (per cent) | Grant per tonne (euro) | Funded | Dies to |
|---|---|---|---|---|---|
| 0 | the works buildings' before and after (IPMVP Option C) | 23.6, 14.8, 11.2 | 58, 37, 41 | all three | the 2019 notice season ran high, and the pandemic and the gas price shock moved every building (the lottery shows it) |
| 1 | the lottery against every passed-over building, on the notice season | 12.9, 2.4, -1.9 | 110, 280, none | insulation | the service visits (visited buildings step down about 7 per cent; no works building was visited) |
| 1b | the same on every season to 2019, offered owners who did not answer, everyone outside the pilot, or read as drawn (in kWh or per square metre) | 12.1 to 12.9, 2.4 to 3.5, -2.8 to -0.9 | 107 to 116, 140 to 280, none | insulation | the service visits |
| 2 | decay read from the narrowing gap (the last two seasons as the saving) | 11.7, 1.6, -3.4 | 116, 280, none | insulation | the untuned buildings' gap holds flat |
| 2b | the crisis seasons dropped (seasons to 2022) | 13.9, 3.4, -0.3 | 100, 180, none | insulation | the visits began in August 2019, before any crisis season |
| 2c | the first season only | 13.4, 4.1, 0.5 | 110, 140, 450 | insulation | the first autumn's visits (16 districts) |
| 3 | passed-over buildings dropped from their visit season (golden) | 16.0, 5.8, 2.0 | 90, 90, 220 | insulation and heating optimisation | none |

- **Winners:** rung 0 funds all three measures, rungs 1 to 2c fund insulation alone, rung 3 funds insulation and heating
  optimisation (386 funded applications received for €3.25 million; about €8 million and 90,000 lifetime tonnes once the
  offer closes).
- **Margins:** on the golden heating optimisation runs at 0.77 of the limit, insulation at 0.73 and heating controls at
  1.86 times it; rung 1 puts heating optimisation at 2.3 times the limit and rung 2c at 1.15; rung 0 puts heating
  controls at 0.34.
- **Position and dominance:** the golden is the extreme comparison: every route that keeps a visited building as a
  comparison files a lower rate for every measure, so no half-applied correction lands on it from below, and the only
  route above it is the before and after, which ignores the comparison altogether. No route that keeps the visited
  buildings lands the funded set (Gate F, asserted).
- **Grid:** two independent choices (whether the visited buildings stay in the comparison; the baseline and pool) give
  every cell listed above; the cells that keep visited buildings fund insulation alone or less, and every cell that
  drops them funds insulation and heating optimisation.
- **Worth:** the decisive rung moves the graded verdict on heating optimisation and every graded figure (rates, grant
  per tonne, the funded applications, the round at close, the 2025/26 saving).

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | the pilot's works buildings for the rate; the 2026 applications received for the appraisal; the round at close for its totals | filed (plan 4.2, 4.4; the request); C1 on the 38 withdrawals (SF2) |
| 2 Unit of account | the building, its meter points summed | the register maps meter points to buildings; asserted (SF14) |
| 3 Attribution window | a season is 1 May to 30 April | the periodic reads fall on 30 April; late reads carried by date (SF15) |
| 4 As-of dating | data to the reads of 30 April 2026, applications received by 12 June 2026, the offer open to 30 June | filed in the request and the applications file |
| 5 Version basis | estimates and corrections replaced by the later actual read | C1: asserted (SF15) |
| 6 Denominator | the rate's denominator is the building's normal-weather use without the works | filed (plan 4.2); the aggregation is the plan's average over the works buildings (SF7) |
| 7 Weighting | every works building and season since the works, each building alike | filed (plan 4.2), C1 across the licensed averages (SF7) |
| 8 Window length | every season since the works, 2020 to 2026 | C1: the golden family on every baseline and window (SF4) |
| 9 Boundary inclusivity | €120 or less | C1: no measure within 20 per cent of the limit (SF10) |
| 10 Rounding path | the council's rates in whole per cent into the appraisal, each reported figure rounded once | filed (plan 4.2), asserted (SF16) |
| 11 Tie-break | none needed | no two measures compete for a limit |
| 12 Maturity and censoring | a passed-over building compares only before its visit season; the round's applications still to come | the decisive step (SF5); the projection by measure (SF13) |
| 13 Order of operations | normalise, then compare, then appraise | the plan's order; asserted |
| 14 Row order | none | C1: no figure depends on file order |
| 15 Duplicate resolution | exact re-imported rows dropped | C1: every duplicate is exact |
| 16 Identity normalisation | meter points to buildings through the meter points file; meter numbers across exchanges | the systems' own keys |
| 17 Netting against gross | none | no saving nets against another |
| 18 Dimensional units | cubic metres to kWh by z-number, factor and calorific value | the meter points and calorific values files; asserted |
| 19 Code and status semantics | read reasons; draw results; application dates | each file's own values, plain words; never the stump |
| 20 Integerisation | none | no whole-unit allocation |
| 21 Clause scope | the appraisal applies to a round's applications for a measure | filed (plan 4.4) |
| 22 Forward window contents | the 2026 applications received and the round still open to 30 June | shipped (`applications_2026.xlsx`, the request); the closed round projected from the 2019 responses (SF13) |

## Literal reader

Executed word for word, the plan's section 4 and the committee's request give the golden: the saving rate is the share
of normal-weather use the measure's works save, averaged over the works buildings and taken in whole per cent, so a
comparison building is one the works did not touch and nothing else moved; the lottery's full comparison measures the
works against buildings the service team was tuning (SF1, ruled out by the plan's own words and by the 2026 applicants,
who get no further visits); the round once the offer closes is what the applications received will come to (SF13);
the 2025/26 saving is each rate on what the works buildings would have used that season (SF17); every convention the
computation needs has a fork row closed by a filed sentence or asserted as the same call or the same rounded figure,
and the call under every licensed reading of the estimand is insulation and heating optimisation funded, heating
controls not.

## Oracles

- **The notices' normalised use** (`benchmarking_notices_2019_2026.csv`) ties to the cleaned reads for every flagged
  building and season under every licensed handling of the reads: it confirms the Layer 1 build, on every route alike,
  and says nothing of a saving.
- **The draw's balance** (the drawn and passed-over buildings alike on the 2019 notice season and on every season
  before) confirms the randomisation on every route; it is the textbook check the lottery comparison passes.
- No control, published figure or reconciliation in the pack states a saving, a grant per tonne or a verdict.

## Ask sheet

- **Ask 1, the deck's opening (the call and the round once the offer closes):** golden: fund insulation and heating
  optimisation, not heating controls; about €8 million and 90,000 tonnes.
- **Ask 2, each measure's saving rate (3 cells, whole per cent):** golden 16, 6 and 2; the lottery 13, 2 and -2; the
  before and after 24, 15 and 11.
- **Ask 3, each measure's grant per tonne charted against the limit (3 cells, nearest €10):** golden €90, €90 and €220;
  the lottery €110, €280 and no saving.
- **Ask 4, the pilot's 2025/26 saving (nearest 500 tonnes), its own second judgment:** each rate on what the works
  buildings would have used that season: golden 3,500; a landed run that applies the rate to the 2018/19 use 4,000; the
  rate on the use with the works 3,000; the lottery's rates 1,500.
- **Ask 5, the measures sheet (18 cells):** rate, applications received, grant, lifetime tonnes, grant per tonne and the
  verdict per measure; the applications and grants are read off the applications file by every route, the rest moves
  with the decisive step.
- **Ask 6, the funded applications (386 rows):** grant, expected annual saving in whole MWh, lifetime tonnes to the
  nearest 10; the row set is the golden's funded set, every figure moves with the rate.
- **Ask 7, the funded round once the offer closes (€1 million, 10,000 tonnes), its own second judgment:** each funded
  measure's applications received scaled by the share of the 2019 responses for that measure in by the same day after the
  notice: golden €8 million and 90,000; one pooled share for the two measures €7 million and 80,000; the days elapsed €6
  million and 70,000; the applications received €3 million and 40,000; the lottery's funded set €7 million and 60,000.
- **Pair ceiling:** 45.8 (`ceiling.py` on the cut pack: the recommendation 20, four components 4.5 each,
  instruction-following 7, the asks 55 spread over the seven supplementary answers, each kept in proportion to its
  figures a route gets right; the landed run that sums the applications received and applies the rate to the 2018/19
  use scores 79.0, the default path 12.5). With one of the two second judgments taken the pair is 52.3, with both 56.2.
- **Shallow keep:** 9.9 per cent of the ask weight (the default path keeps the applications and grants read off the
  file, the insulation and heating controls verdicts and the chart's bars and limit line).
- **Measured by:** task7/generator/ceiling.py on the cut pack.

| Ask figure | Golden | Landed run (visits found, received applications summed, the rate on the 2018/19 use) | Shallow run (the lottery comparison) | Cracker verdict on the landed run |
|---|---|---|---|---|
| saving rates | 16, 6, 2 | 16, 6, 2 | 13, 2, -2 | keeps |
| grant per tonne and verdicts | €90, €90, €220; funded, funded, not | the same | €110, €280, none; funded, not, not | keeps |
| the funded applications | 386 rows, the golden's figures | the same | the insulation rows only, the lottery's figures | keeps |
| the round once the offer closes | €8 million, 90,000 tonnes | €3 million, 40,000 tonnes | €7 million, 60,000 tonnes | misses |
| the pilot's 2025/26 saving | 3,500 tonnes | 4,000 tonnes | 1,500 tonnes | misses |

## Leak rulings

- `leak.py` (2026-11-08, as-of 15 June 2026): REVIEW, no LEAK. The answer-figure sweep's three files carry the measures'
  own names (the plan's programme, the pilot's terms, the federal overview's eligible measures): harmless. The
  stump-vocabulary sweep's six documents carry "Energy Services", "service life", "notice", "season" and "carried":
  harmless, none names a visit, a tuning, the passed-over owners or a comparison.
- The isolated reader found no decisive step, ranking file, helper file or answer figure; its one finding, the plan's
  4.2 averaging sentence read as a works-only average, was fixed in the generator (each building's saving, averaged).

- The duplicate gate (`guard.py heart`, 2026-11-08 after the pull): BLOCK on `ban.strategy` (causal_design) and
  `ban.org_family` (utility_or_infrastructure) against task10 v5. The dates: this architecture's card was registered
  with both axes at 2026-11-08T16:17:59Z (DRAWN commit 0a705d3); task10 v5 drew the same two axes at 17:16:44Z; this
  card's mechanism redraw re-registered it at 17:38:55Z on a corpus that did not yet hold task10's card, which moved its
  stamp after task10's. The honest labels are these two (the comparison choice is causal design; the analysis is the
  municipal utility's), and the only unbanned pair the guard leaves (a government agency, population selection) would be
  a relabel, so neither axis is redrawn; the collision and its dates go to the author at sign-off (reduce-house-fixes
  H27 and H31).

## Prompt contract

A voice rewrite may not drop or change: the question (which of the pilot's retrofit measures Haldenau's 2026 grant round
should fund); the threshold (the council's limit of €120 of grant per tonne of CO2); committee_briefing_retrofit_round_2026.pptx
with the recommendation first, each measure's saving rate from the 2019 pilot and its grant per tonne on the 2026
applications charted against the limit, and the CO2 the pilot's works saved in 2025/26; retrofit_round_2026.xlsx with a
row per measure (saving rate, applications, grant, lifetime tonnes, grant per tonne, fund or not), a row per funded
application (grant, expected annual saving, lifetime tonnes), and the funded round's grant and lifetime tonnes once the
offer closes on 30 June; saving rates in whole per cent, grant per tonne to the nearest €10, grants to the nearest
€10,000 and the closed round's to €1 million, annual savings in whole MWh, lifetime tonnes to the nearest 10 and the
closed round's to 10,000, the 2025/26 saving to the nearest 500 tonnes. It may never add the lottery, the draw, the
passed-over owners, the comparison, a control group, the service team, visits, tuning, burners, fading or persistence,
the crisis, the pandemic, weather normalisation by name, the responses' timing, a projection or a completion share, a
count of measures, buildings or applications, or any hint that the comparison buildings changed.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the call rests on the comparison that is actually clean (each
  passed-over building dropped from the season of its service visit, read off one read reason in the meter file
  against the building's later seasons), with the lottery comparison at rung 1 and the works buildings' before and
  after at rung 0; no route that keeps the visited buildings lands the funded set (Gate F, asserted); the two asks
  with judgments of their own (the round once the offer closes, the 2025/26 saving) ride the deep step.
- Free gates on the final cut: generator checks 79 of 79, figures_check 100 of 100, precut 75 of 75 (voice-check's
  shell quota WARN: the pptx and xlsx deliverable set at 30 per cent of prompts on file), leak.py REVIEW with no LEAK,
  the container gate clean, two byte-identical builds, `guard.py surface` clean; `guard.py heart` BLOCK against task10
  v5, which drew this architecture's two axes an hour after this card did (Leak rulings above).
- Stage 4: three isolated leak reads found no decisive step, ranking, helper or answer file, the last reading the
  filed 4.2 as saying how a saving is computed and never which buildings compare; the judge's first pass found the
  saving rates unforced (the estimator, the seasons), fixed by filing the construction in 4.2; its re-judge returned
  DETERMINISTIC with a FIX_NOW on the answer text alone (the visits described as the files show them, service-visit
  reads followed by lower use, rather than as burner tuning; the draw-balance figure; the reason the visit season is
  dropped, which closes the 16, 5 and 1 reading), and the one targeted re-judge of that fix returned DETERMINISTIC with
  three refinements applied (the balance stated as within 1.5 per cent, the visit season's step as 3 to 6 per cent by
  visit season against about 7 the season after, step 9's reason stated from the data). The pack and the prompt did
  not move (`determinism_check_report.md`).
- Pair ceiling 45.8 (`ceiling.py`), shallow keep 9.9 per cent.

## Tried and rejected

- The note's decisive rung, per feeder the smaller of expected buyers and hosting slots: a stated connection standard, a per-feeder hosting map and a neighbourhood-to-feeder join whose keys line up hand it to any solver who reads them, its driver sits nearest task106's, and as labelled it BLOCKs on ban.pattern C (task119), ban.calibration pilot_log (task122) and test.same_driver_older (a signature spent in nine builds); kept as rung 2.
- Resistance-to-heat-pump netting (each resistance conversion frees feeder headroom for oil or propane conversions): the connection standard either states a per-heat-pump assessment, which contradicts the netting and is a counter-pin, or states a net-change rule, which hands it over; a corpus of past approvals would refute the stop rung, which L1 forbids.
- Heat pumps per home (large ducted homes taking two outdoor units, so two feeder draws per slot): visible at heat-pump grain in any connection or rebate record, and found by any solver who counts rebates per buyer; moves only the saturated feeders, too little to change a leader.
- Survey staleness (homes converted since fieldwork leave the pool): a dated register keyed on neighbourhood is a schema-visible pool deduction a careful solver makes unprompted.
- Competing claims on feeder headroom (the utility's deferred queue, committed loads, a state income-qualified programme): each needs a first-come-first-served clause the solver executes, and the effect sits only on saturated feeders.
- Seasonal against winter hosting capacity on summer-peaking feeders: needs a filed "winter" assessment that sends the solver straight to the feeder load history.
- A feeder map naming each neighbourhood's primary feeder while boundary streets sit on the next one: reads as a coarse instrument (sole_data_defect yes under the instrument repair), and a solver who reads "primary" looks for the street-level join.
- The expected minimum against the minimum of the expectation at feeders where buyers and slots balance: under 10 per cent on any feeder and inside the nearest ten on co-op totals.
- The year-end lapse on Year 1's lag alone (late autumn purchases missing 31 December): a stated deadline the solver replays at the finest grain on offer; kept as the check that passes at rung 2.
- A utility service-upgrade queue for old 100 A homes as the decisive rung: the upgrade requirement has to be stated for determinism, which sends the solver to upgrade lead times, and old homes sit mostly on saturated feeders, where the feeder cap already binds.
- Relabelling the note's pilot log as realised_outcome_roster to clear ban.calibration: a relabel that does not name the decisive move, so the organ itself was redrawn as Year 1's install book.
- A Nova Scotia setting with a fictional utility (oil and electric heat): the province's distribution is one large utility, so a co-op that sets its own heat-pump rate meters reads as invented; moved to Minnesota co-op territory.
- A field operations voice saying the 2025 meter-exchange backlog is behind us: true, but it names the backlog and sends a reader to the weeks the crews ran at their ceiling; dropped.
- A filed field-procedure line on the order of work (standing orders first, then orders in date order): read beside the programme's volume it gives a solver a reason to ask whether the crews keep up; the order is to be pinned by the 2025 record instead, and the line stays out unless the determinism check needs it.
- Keeping one co-op as the requester at registration, relabelled cooperative_or_member_body to clear ban.org_family: the key is honest for a member-owned co-op, but two United States power-company allocation builds would then sit side by side with task124, the calibration and artifact bans would still need redrawing, and the business-operations-analytics x opportunity-sizing-decision pairing would still block task128; the requester moved to the fund instead.
- The draw's per-co-op ask figures (meters still unset on 31 December, qualifying buyers the feeders turn away) and its chart parts (the stacked series, the year-end queue annotated): each names rung 3 or rung 4 in the prompt, which outranks every file, so a solver is told the queue and the feeder cap exist before opening anything; replaced by two device-carried pilot audits and a 2027-against-2026 chart.
- Spare capacity of about six sets a week at Lakes: the autumn queue bites harder, but each crew's annual spare (about 300) then falls below Lakes' 420 placeable meters, so a crude annual check hands Riverbend the lead without the queue; spare set back to about ten (annual about 500).
- Lakes and Uplands crews on a Monday-to-Friday week: the 2027 Friday holidays (Christmas observed 24 December, New Year observed 31 December) and Thanksgiving Friday open a holiday-handling fork worth up to a full ten on Lakes' slots; moved both crews to four ten-hour days, Monday to Thursday, with the 2026 record showing they worked the Thursdays before Friday holidays.
- Grading the year's rebated installs as the unrounded co-op sets rounded once to the nearest ten: the two binding co-ops' convention spreads (about 5 and 3.5 sets) add across a ten on the total; the graded total is the sum of the co-ops' slots, with the unallocated figure its complement.
- A spring queue left to run continuously into the autumn at the binding crews: year-end sets then depend on the spring start week and every holiday from Memorial Day on, a spread of more than ten; spring volumes sized so both crews clear by August.
- Pilot spring shares that differ by neighbourhood: per-co-op and pooled readings of the forward calendar then differ by 4.2 sets a point at Lakes; set to exactly 25 per cent in every pilot neighbourhood.
- A 2027 slot-release rule (a quarter of each co-op's slots in the spring window): it makes arrivals depend on the allocation itself and its fixed point (Lakes about 183) disagrees with the one-pass queue (about 240), a fork created by a filed sentence; no release rule, so both readings give 240.
- A per-co-op ask on the pilot's days from claim to payment: a staffing decision that the split never reads, so it fails H18; re-cut to the rebate dollars paid in 2026 and the installs they cover, the audit trail of the pilot the rates are built on.
- A pilot close-out stating the total rebates paid: an oracle that verifies ask B's handling for free; the pack states no paid, cost or cleared total.
- Field-order volumes at the draw's 70,000 rows: six crews' standing work over 104 weeks is about 31,000 orders at realistic crew sizes, and padding the file to 70,000 would need order types nothing reads; 31,000 clears the gate.
- Ask B's clock device on the 31 December 2026 evening payment run: the pack's as-of date is 11 December and the trustees meet on 17 December, so no December run exists to cross the year; the cutoff moved to the fund's November month end (the 30 November run clears on 1 December UTC) and the prompt asks for rebate dollars paid through the end of November.
- Anthony Bentley as the outreach director: the name is not in the seed-127 draw (`guard.py names --geo "United States, Minnesota" --seed 127 --n 200`); Anne Garcia from the draw then took BLOCK people.first against task125; Sara Duncan from the same draw is clear.
- The outreach director's belief that Uplands has more propane and electric homes than any other co-op: Table H1 puts Valley first on propane and electricity, so the belief would be a stakeholder read the pack refutes; reworded to more qualifying homes, which the survey's joint counts make true (rung 1's leader).
- The rung 3 twins with each neighbourhood's buyers split across two feeders: the map puts each neighbourhood on exactly one feeder, so Elm Park and Birch Hollow are identical on the survey and sit on a full and a roomy feeder respectively.
- A Lakes ceiling cycle averaging 10.45 a day over twenty days: the plateau's 50 days start mid-cycle and recover 10.57, which moves Lakes across a ten; the ceiling is a four-day 11, 10, 11, 10 pattern (42 a week) and standing work a twenty-day block averaging 8.05, so spare is 2.44 a day in any window.
- Pilot install rates with neighbourhood-level noise: rates by system and income band, or each co-op's own pilot rates, would each give a different forward figure (H14); every pilot neighbourhood is built from unit blocks (38 ducted-propane households to 3 installs, 32 electric to 1, 95 hydronic to 1), so every finer grain returns the system rates exactly.
- Pilot purchase dates spread evenly with a random installer lead time: autumn installs clustered to six orders a week at Uplands (0.86 of its spare); installs are spread evenly over each season's install span instead, peak four a week at Lakes and three at Uplands.
- The rebate amount as a pilot-log column: it would let a per-rebate reconciliation of the ledger find every returned payment for free; the amounts live in Schedule B of the participation terms instead (still a reconciliation route, recorded as HZ2's leakage).
- The rules file named `clean_heat_programme_rules_2027.pdf` after the fund: leak.py's file-name sweep reads `clean_` as the author's cleaned-data noun (LEAK); renamed `heat_pump_programme_rules_2027.pdf` in the generator.
- A "Decision sought" closing section and totals for expected installs, feeder room and meter sets in the note's line-by-line table: the section restated the split on an orphaned page, and a meter-set total of 1,174 beside 1,170 placed is a second statement of the year's installs by another rounding path (H3); both cut.
- 2026-10-10: the crew meter-set queue as decisive rung under a hosting-slot cap; the determinism judge returned SEND_BACK and the build was retired, not submitted.
- 2026-10-12, re-root (architecture 2): the author re-queued the number in wave 1 as "re-root, Opportunity Sizing". Candidates weighed at the draw and rejected: a charged-off card portfolio's sale against keeping it (the warehouse's payers are a visible attribute every solver conditions on, and the composition-mix strategy is banned against task501); a diabetic eye screening van placed by first-round against repeat-round yield (the prevalence-round effect is textbook to a strong solver); acoustic leak-detection crews placed by main material (material is a GIS column the reflex stratifies on, and a conditioned yield transferred across mixes is composition mix); a health plan's navigations split by procedure group where members follow their surgeon (the payment-claims task type serves ETL and Anomaly Detection, not Opportunity Sizing); an overdraft fee cap's revenue at risk sequenced after the banks' own changes (lending sits outside Economics in the client taxonomy, and no banking task type serving Opportunity Sizing fits a rule's revenue impact).
- 2026-10-12, architecture 2 at stage 2: a brokerage "package available from" date beside the start date (care ready before the patient left): it shows the care wait apart from the delay for every patient held by equipment, so a solver reconciling the two sees a third of Ashby Vale's patients leaving days after their care was ready and goes looking; the brokerage records care starting on the day the patient went home, and the restart patients carry the counterfactual instead.
- Restart patients needing discharge equipment at the same rate as new-package patients: subtracting their average nights (the control reflex) filed the golden split exactly; restart patients mostly have their equipment at home already (0.15 of the rate), and the control now files Ashby Vale first.
- Wendlebury's equipment need at 0.27 of covered patients: counting equipment patients at nought (R2) then filed the golden split; at 0.62, with the North depot's quick deliveries, R2 fills Cleeve Park and leaves Wendlebury short while the golden barely moves.
- The national weekly return by site: its nights per discharge rank the hospitals on the delay, an artifact on rung 0; it ships by trust, a distractor.
- A boundary change moving two wards from Ashby to Marchford district in April 2026 as an Ask B device: the ask's "district" would read two ways (as then or as now); the districts are stable and the county-line postcode district carries the district hazard.
- The winter's delayed bed-days total in the chart's title: within-trust moves leave the five-hospital total unchanged, so the cracker banks it; the title states what the chart shows, and the ask adds each hospital's delayed patients.
- Re-brokered and re-sent referrals as Ask B devices: whether a re-sent referral is a second referral the brokerage took reads two ways; cut.
- The part-filled hospital's bed-days at 967.45: rounding the value to two places first gives 968; the clearance brings one Cleeve Park delivery forward a day, so 968.23 rounds to 968 on every path.
- 2026-10-14, second-layer attempt after shipping (built to stage 4, not shipped): the patients the wait for home care itself sent to a rehabilitation bed or a care home (re-assessed while waiting, so the warehouse records them on pathway 2 or 3 and the default cohort conditions on the wait's own outcome), found from the brokerage's withdrawn hospital referrals, with the note's section 3 moved to "medically optimised for discharge home on pathway 1". Every free gate was green (27,838 checks, the verifier, a byte-identical rebuild, precut, leak.py), but the judge returned NOT_DETERMINISTIC and SEND_BACK on that pack (determinism_check_report_loop1.md, which covers the rejected prototype and not the shipped pack): no shipped sentence says a withdrawn hospital referral marks a patient optimised for home, and that reading alone moves Ashby Vale from 10 packages to none. Filing the population as "whatever pathway they left on" would hand over the post-treatment insight and leave only a record linkage a solver executes once told, so the call would turn on a filed rule; the leak reader also opened a fork on the package's "up to four weeks" (the re-assessed patients waited 23 to 26 nights on average). Reverted to the shipped pack, which the generator rebuilds byte-identical (27,095 checks); the shipped build's longest saving is 14 nights, so the four-week fork does not reach it.
- 2026-10-14, architecture 3 (a full refresh at the author's request, built to stage 4, not shipped): actuarial reserving for a motor bodily injury book (Ninebark Mutual, year end 2026, Forecasting), the paid history restated at the latest diagonal's closed shares of claimant features (Berquist-Sherman) after a claims platform slowed settlement, $400 million carried against the paid chain ladder's $325 million. Stage 3 green, the leak reader clean and the adjudicated clone check on Sonnet CLEAN, but the judge returned NOT_DETERMINISTIC, SEND_BACK: the reserving basis leaves the method to the actuary, and frequency-severity on paid per closed feature carries $350 million with nothing shipped selecting between them, while filing the method would make the decisive step rule application. The author restored this architecture; architecture 3's note, generator and judge report are in git at 6edd337.
- 2026-10-16, loop 1: filing the dependency as a discharge rule ("the ward discharges the patient once the delivery is made") in the equipment notes: it states the timing that a package's counterfactual turns on, so the decisive step would read as executing a filed rule; the route's definition files only what the equipment is for. The judge's optional pin (required_by is the discharge ready date) stays out for the same reason.
- 2026-10-16, loop 1: practices closed by merger on covered patients' spells (67, carried by the patient for every later admission): dropping the closed codes moved four hospitals' caps, a field reading that could decide figures on the main call; the registration is now taken at admission, so the closed codes sit only on spells admitted before each merger.
- 2026-10-16, loop 1: waits drawn flat between two bounds (home care 4 to 10 nights in Marchford, 6 to 14 in Ashby; South deliveries 5 to 13): the stage 4 reader read the covered patients' nights after the ready date, 3 to 14 with a hard floor, as too clean for delay data; every wait is now right-skewed by its quantile at the same uniform draw, so no other draw in the stream moved.
- 2026-10-16, loop 1: a weekend event moved to the Monday (and sometimes the Tuesday) by a fixed chance: every Saturday and Sunday the services turned down piled onto Monday, so Monday carried 1.8 times a midweek day's discharges and 2.3 times its deliveries, a new tell; a turned-down weekend day now redraws the wait from the service's own spread, which spreads the weekend's load across the working week.
- 2026-10-31, reship under the learning loop's rules: the acute, equipment and council extract notes and the data
  request log withdrawn (shipped files may not describe the data, and the log narrated a device); the two reporting
  conventions the notes carried that a figure turns on (delayed nights dated to their evening, a patient delayed in a
  month with one such night; the brokerage's wait in calendar days from receipt to start) moved into the fund note's
  monitoring section, and every other field reads from its own column. The prompt dropped its counts of hospitals,
  districts and months and opens on where the packages go.
- 2026-11-07, portal FAILED_TO_STUMP on architecture 2: both responses filed the golden split exactly (Royal Marchford 508, Wendlebury 350, Holmford 120, Cleeve Park 222, Ashby Vale none, 6,816 bed-days). The equipment wait running alongside the care wait is an overlap a careful response finds by joining the depot's deliveries to the covered patients, so the stump was a hidden overlap rather than a method the field's full practice gets wrong; the discharge world is spent and the slot re-roots in another domain.
- 2026-11-07, architecture 4 draw, candidates screened on paper before this card: the marginal travel a visit
  adds to a crew's day (a shared cost a removal does not save is architecture 2's logic, and routing reads the same
  for any field); a pooled fleet assessed by round rather than by vehicle (task153's fleet duty-cycle world, and the
  estimand has to name the rounds); arrivals seeing busier units than the time-average busy fraction (the optimization
  card's MEXCLP is the careful route and a replay of the calls lands the golden); failures per running hour or start
  (task170 and task176 screens); vacancy chains (task174, task137); turbine wakes (task187); demand-response snapback
  (task118); a lower screening threshold read from interval cancers in excess of the undetectable band (excess over a
  reference band is epidemiology's attributable-risk reflex, and the follow-up contradicts any extrapolation, so a
  back-test picks the golden); a written-off portfolio's hold value by payment arrangement (architecture 2's draw
  rejected the card portfolio sale, and a paying segment is a visible attribute); a setting active only above a
  threshold (task162), threshold counts from point predictions (task253, task151), staggered adoption (task136,
  task137), immortal time (task122), a post-treatment control (the careful textbook's own remedy). Chosen: the
  write-off a support package keeps off borrowers that depend on the supported firm's payments.
- Contagion defaults on the first payees of each payer (stage 3, 2026-11-08): the record's payee default rate then rose
  with receipt share (bands at 0.30, 0.43 and 0.57), so a logistic fit on share or three share bands moved Matai's
  figure and the total a NZ$50,000 bin. Reassigned within each payer so the rate is flat in share, every count and date
  kept; a two-band cut at 0.65 still moves a bin (SF11), as no assignment of 31 outcomes holds every cut.
- Matai Valley Foods in Manufacturing (stage 3, 2026-11-08): a rate by the defaulting payer's division (3 of 8 in
  Manufacturing) put Matai at NZ$1,650,000. Moved to Agriculture as a grower-packer supplying supermarkets, a division
  in which no payer defaulted.
- Fernmark Bank and Harcourt Packhouse (stage 3, 2026-11-08, H21): FernMark is New Zealand's national brand mark and
  Harcourts a national real-estate brand one letter away. Renamed Ruahine Bank and Marlowe Packhouse.
- The wholesale borrower's 2025 re-default (stage 3, 2026-11-08): put wholesale's share at exactly 6.25 per cent, a
  rounding tie. Dropping it changed the number of defaults and shifted every later draw (asks A and C moved); the third
  re-default moved to retail instead, same draws.
- Round watch-list PDs and balances, and a validation table marked Pass on every grade (stage 4 leak reader,
  2026-11-08): two-digit PDs, term loans drawn exactly to their limits and balances in whole thousands read as built,
  and an honest one-sided test fails grades 5 to 7. PDs now carry four decimals, balances cents, term loans amortise,
  and the table carries the bank's traffic light, amber in grades 5 to 7 and monitored.
- 2026-11-08, platform round 1 (run 1 98 on the call; run 2 58 off it, Kinloch and Ridgeway, after computing the eight dependants and the record's 13 of 31 and declining to price them): both runs filed every security value, total commitment and 2025 sector share exactly. The case-file asks were rule application (terms 4.1 and 4.2 file the indexation and the guarantee basis; the validation report files the default definition), and the hygiene battery (migration dates, discharges, former names, releases, loan-keyed register rows) was run by reflex, as Mark measured; dropped as asks, their files ship as context.
- The ranked list of the eight package values as an ask: six of the eight have no dependants, so the default path files six of eight cells; kept in the golden workbook as the table behind the choice, not asked.
- The write-off each package keeps off other borrowers, a list of the dependants with their own figures, or the intake's write-off split by sector as asks: each names or hints at the dependence in the prompt (the deep step handed over), and the sector split also sits NZ$6,300 under a bin edge at Transport.
- Envelopes of NZ$4.0, 7.0 and 8.0 million: the standing family spreads each across two NZ$50,000 bins; the grid runs from NZ$4.5 to NZ$6.5 million.
- The less dependent payees' count (6 of 61) as a graded figure: one of the six defaulted exactly 365 days after its payer, so a follow-up convention moves it to 5 of 61; it stays out of every answer block and the note.
- A second judgment the clean landed run would miss, to bring the paper pair under 50: none survives the freeze. An interval on the rise forks across methods, a timing split of 2027 against 2028 write-off reopens the call, and every leak-free handle on the dependence is a function of the package values the clean landed run computes; the pair stays at 56.0.
- Critical component 1 as a count ("8 from Matai Valley Foods"): the off-call run counted the eight and denied the protection, and kept the criterion; reworded, numbers frozen, so the component states that the package keeps them out of default.
- figures.json keys `commitment.Northgate Print` (1,750,000) and `sector_counts.I.1` (5) left with the case-file and sector asks; freeze.py read them as main-call figures only because their values coincide with Matai's NZ$1,750,000 and the 5 of 211 control count, which stay in figures.json under their own keys (`--allow` on both).
- 2026-11-08, platform round 2 on architecture 4 (the re-sited asks: fall-back intakes and the envelope curve): both runs landed Kinloch Engineering and Matai Valley Foods (the author's word; texts not pasted). The payer dependence was a mechanism the transactions and the default register visibly carried, and both runs priced it once they had measured it. Architecture 4 is spent, and its world (Ruahine Bank, its borrowers, its payments) with it.
- 2026-11-08, cleanup at the author's word: every file of architectures 1 to 4 (generators, packs, goldens, reports, runs) removed from the folder; this record, the run record and the card's lineage keep what each died of.
- 2026-11-08, architecture 5 draw, on paper: the excess default risk of a borrower in the year after a downgrade (rating momentum), with 2027 following a 2026 downgrade wave and the grade-only transition matrix validating on the pooled history. Stripped of nouns it is mark179's driver (a chance that rises for a period after an event, the forecast year following a surge of such events), and a path property the state omits is the same abstraction as task1's provider tenure; dropped before a card was written.
- 2026-11-08, architecture 5 draw, on paper: two effects offsetting inside the observed window (mix against rate under a flat total) as the deep step; task3 arch 3 and task8 arch 18 both carry it, so a third would read as a template.
- 2026-11-08, architecture 5 at stage 2, the recent-experience route (seed 129): the record's latest years averaged flat,
  pooled or by book, landed the plan cell and both book cells, because the record's recent defaults were as stale as the
  year-end book a year later; the world now has the workout unit re-inspect facilities of €1 million or more at
  referral from 2022, so a third of the recent defaults rest on fresh inspections and recent experience files €0.8 to
  €1.4 million.
- Watch-list re-inspections at a downgrade to grade 7 or 8 from 2023 (stage 2): they reached 21 of 354 recent defaults
  and moved nothing; re-inspecting every stage 2 facility at its annual review from 2022 freshened the riskiest part of
  the year-end book, pulled the golden to €2.36 million beside the record's average (€2.24 million), and was reverted.
- No go-live roll-forward (stage 2): defaults from January to April 2012 were set against un-indexed 2004 to 2007
  inspections (ratios 0.2 to 0.35), which bent every functional form apart; the warehouse's go-live now rolls every
  value forward to 2011 Q3 on 3 January 2012.
- The 2013 to 2019 recovery at full strength (stage 2): the index rose 3 to 5 per cent between the carried quarter and
  the inspection at default, so the raw and index-adjusted ratios split the plan figure by 7 per cent; every index move
  after the 2012 trough is halved and SF21 asserts the two land together.
- A year-end book facility with no valuation row in force (stage 2): a December 2026 origination whose inspection loaded
  on 10 January 2027; inspections dated in the year now load by 31 December, and the register writes no roll-forward
  over a newer inspection already on file.
- Seeds 129 to 152 scanned with the master scale as the one free scale (stage 2): seed 141 at 0.82 of the earlier
  published scale is the only world where every standing rival files the three graded cells with €48,000 or more inside
  the book cells and €127,000 inside the plan cell, the five facilities hold under every split member, the pooled run
  misses both book cells and every shallow route misses the plan cell by €375,000 or more.
- The memo's "the expected value of the security at that date" (stage 4, leak reader 1): read literally as the register's
  latest value with prices held, which is the default path, and it left room for the unconditional market value and for
  the loss averaged over the values an inspection might return (€2.48 million, so €2.5 million); the memo now files V as
  the value the bank would expect its inspection to put on the security if the facility defaulted, and the loss as
  CRE-LGD-3 applied to it (SF23), naming no record, staleness or shortfall.
- Customer names drawn by lending book alone and floor areas drawn flat in a range (stage 4, leak reader 1): a
  "Hospitality Ltd" carried a nursing-care code and a 4,459 m2 medical centre sat on a small value; names now follow
  the property's business and areas the first inspection's value at a regional rate per square metre, both on streams
  of their own so no graded draw moved.
- Customer, legacy facility and property numbers in steps of 13, 37 and 11 (stage 4, leak reader 2): sorted, each ran
  as an arithmetic progression; the numbers now carry irregular gaps from a stream of their own, increasing in the same
  order, so no sort and no graded figure moved.
- Secondary figures stated at a precision no other construction reproduces (stage 4, determinism judge, FIX_NOW): the
  record's 844 (a count of properties, written as defaults; the judge counted 833 to 883 by its own rules), the cohort
  since 2022 as 112 of 319 and 10 per cent (122 of 322 and 8.7), the band means 75 and 9 per cent (73.7 and 8.5), the
  CSV's euro total and the unrounded plan figure (the judge's base €2.06 million), "€0.2 million" beside a €500,000
  grid, and the order of the third and fourth facilities. The blocks now state the graded cells at the prompt's
  rounding, the fitted ratios (reproduced to the whole per cent), the model figure as €0.22 million, the working counts
  in words with each bound asserted in checks.py, and the five as a set with the clear leader named.
- The Step-by-Step's "more than 20 standard errors" and a column list read as required (stage 4, re-judge, optional
  notes): 20 held for the pooled slope (23) and not for each book's (15 and 19), now "more than 10 in each lending
  book", asserted per book; the prompt names no CSV columns, so the answer now requires each facility's number and
  its expected loss and calls the golden file's other columns a choice of layout.
- 2026-11-08, platform round 1 on architecture 5: not stumped; the model filed the €2.0 million plan figure (the author's word; run
  texts not pasted). The stage 4 re-judge had named the risk: filing V as the value the bank would expect its
  inspection to put on the security if the facility defaulted sends a solver to the record of inspections at default,
  and once that record is built the shortfall's slope on years since inspection is the visible covariate a strong
  model fits; architecture 5 is spent.
- 2026-11-08, re-root to architecture 6: architecture 5's files removed from the folder (in git at c404109); its run
  kept as `runs/arch5/run1.md`.
- 2026-11-08, architecture 6's first mechanism (take-up of a once-only grant offer driven by the rise in use into the
  notice season; the counterfactual conditioned on the seasons before the notice): priced on the clean truth at design,
  before any pack. Selection on a rise brackets the truth, a twelve-month baseline over (heating optimisation 8.3 against
  6.2) and a long one under (4.5); the eligible comparison on a panel landed within a point and a half, a two-season
  baseline within one, and the golden family's own spread (5.0 to 6.3 per cent across pools, baselines and the ratio of
  totals, with the never-in-the-programme pool at 7.5) crossed every decision bar the long-baseline routes could be
  separated by; a comparison bracketing the truth always has a lucky baseline. Redrawn the same day as the lottery
  comparison that a second programme treated (one-sided: every route that keeps a treated comparison building files
  low).
- 2026-11-08, the offer-once rule across seven rounds (2019 to 2025): later offers went only to buildings newly flagged,
  which had risen into the top fifth, so later rounds were rise-selected even with take-up at random and the long
  baselines understated again; the pilot became one round drawn by lot.
- 2026-11-08, a tuning campaign spread evenly over seven winters: the first season after the works carried little
  contamination, so the first season alone landed every figure; the campaign front-loaded (twelve districts in its
  first autumn); the first season alone now misses every rate and lands only the funded set.
- 2026-11-08, the comparison read as drawn, with no baseline (the post-period means of drawn and passed-over buildings):
  in kWh it carries the buildings' size spread (several points of standard error), so it is noise, not a member of the
  golden family; every licensed route takes a baseline.
- 2026-11-08, the ask layer measured at a pair of 53.3 on the cut pack (the saving to April 2026 the only second
  judgment, and its shortcut within 4 per cent of the golden at the nearest 5,000 tonnes): the asks re-sited onto two
  judgments of their own, the funded round once the offer closes (the 2019 responses' timing by measure) and the pilot's
  2025/26 saving at the council's rates; the saving to April 2026 dropped, because "without the works" could also be
  read as with the service visits those buildings would then have had, which a single season at the council's rates
  makes converge.
- 2026-11-08, the application rows: every application with its verdict let the lottery keep the heating controls and
  insulation rows; the sheet now lists the funded applications, the office's own grant list.
- 2026-11-08, the first autumn's visits in twelve districts from September: the first season alone still funded
  heating optimisation (at 0.96 of the limit); sixteen districts from August put it at 1.15 times the limit.
- 2026-11-08, the draw as first realised: the heating optimisation works buildings ran 3 per cent under their
  passed-over owners on the 2018/19 season by chance, and the lottery read as drawn, with no baseline, landed the funded
  set; the draw redrawn to one balanced within each measure (under 1.2 per cent), where every reading of the lottery
  files insulation alone.
- 2026-11-08, the ratio of totals in the golden family: it put heating controls at 2.6 per cent (3 in whole per cent)
  against 2.1 for the mean of the buildings' gaps; the plan now files the rate as the average over the works buildings.
- 2026-11-08, an insulation cost of €72 a square metre to push the lottery to fund nothing: it left two shallow routes
  at 0.98 and 0.99 of the limit and a default answer of no measure at all, which a run would question; kept at €54.5.
- 2026-11-08, stage 4 judge: the saving rates unforced (heating optimisation 5, 6 or 7 per cent as the comparison's
  share was pooled, averaged or differenced and the seasons chosen), the call forced under every estimator; the plan's
  4.2 now files the construction (each works building's use as a share of its 2018/19 use against the comparison
  buildings' average share, one less the ratio, averaged over buildings and seasons), never which buildings compare;
  critical component 2 restated at whole points and the 2018/19 rival at 500 tonnes.
- 2026-11-09, platform review of architecture 6 (version 17; stumped, determinism, solution and type checks passed;
  prelim verdict sent back for fixes): the funding answer turns on one thing, the service visits in the meter file
  (about 7 per cent off most passed-over buildings and none of the works buildings, `TUNE_EFFECT = 0.070` on `~w.works`
  only), constructed, only in the comparison arm, fixed by one exclusion; past it the plan's 4.2 and 4.4 formulas carried
  every figure. The reviewer kept the lottery and the per-measure projection to the offer's close. Re-rooted at stage 1
  as architecture 7 in the same world at the reviewer's direction (client text decides what is allowed).
