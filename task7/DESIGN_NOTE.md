# task7: which retrofit measures Haldenau's 2026 grant round can fund at the committee's confidence (architecture 9)

Architecture 8 (each measure's lottery saving carried along the empty week and the roof per floor, the call on the
roofers' capacity in square metres) was returned at review on 2026-11-11: the deciding step was one constructed factor
that bit only in insulation, and the runs reproduced every other step (`runs/review_2026-11-11.md`; agreed, no rebuttal).
Its note, generator and goldens are in git at commit b355e5c. This architecture keeps the world, the pilot, the meter
work and both transports (now earned steps the runs make), takes the roofers out of the decision, and moves the call
onto two judgments the runs have been seen to lose: heating optimisation's saving without the state campaign's heating
checks that held it up in the pilot's late seasons, the campaign having closed, and each measure's 90 per cent range at
the unit the pilot was drawn by, the owner, whose facility manager runs every one of its buildings the same way.

## Draw

Subdomain: Energy Systems & Utilities, energy efficiency and demand response evaluation (`efficiency-savings-verification`)
Analysis type: Experiment & Causal Analysis (assigned on the platform task: what each measure's works did to a
  building's normal-weather gas use, against the comparison the 2019 lottery supports, carried over the 2026 works' life
  and to the 2026 applicants, with the range the lottery's own design gives)
Answer shape: a distribution and where it is cut (each measure's grant per lifetime tonne on this year's applications
  as the spread a fresh draw of the pilot's owners would give, cut at €120 at its upper end, the committee's rule), with
  the round at close and the pilot's 2025/26 CO2 beside it
Weight: investigation (what held heating optimisation's measured saving level from 2022/23 on, when its works alone were
  still letting it fall: its own persistence, the state campaign's checks that balanced systems held, the 2022 price
  shock that moved every building alike; the three told apart by the campaign's district-by-district timing), beside
  uncertainty at the draw's unit; the last builds sit on validation (task20), measurement (task8), attribution (task9)
  and modeling (task21)
Data-native sentence: the pilot's places were drawn by lot among the owners who answered, an owner's buildings together,
  and an owner's facility manager runs every one of its buildings' heating the same way, so the pilot's evidence is as
  many owners as it holds, not buildings; and from September 2022 to March 2026 the state campaign's checks set every
  taker's heating curve back down district by district, which a balanced system holds and an unbalanced one soon loses,
  so heating optimisation's works buildings saved more after their check than their works alone keep, and the campaign
  has closed for the 2026 works' life
People: Magda Peukert (chair, Committee for Climate and Environment) and Torben Römer (head of Energy Services,
  Stadtwerke Haldenau), from `guard.py names --geo Germany --seed 11`; neither is named in the prompt
Card: `.claude/skills/fingerprint/cards/task7.json`, v9, registered 2026-11-11 (stamp 2026-11-11T22:54:30Z) at WARN; v8
  moved into lineage with its fate. Redrawn axes against the last three live cards: the forum to council_or_assembly
  (the climate committee prepares, the council votes the round), the role to policy_adviser (the request is the
  committee chair's), the decisive generator to G13 horizon mismatch (the pilot's late seasons carried a campaign the
  2026 works' life lacks), the calibration form to `other` (the deciding calibration is the campaign's
  district-staggered check record inside the meter reads; the lottery is the earned comparison, and pilot_log and
  physical_verification are both on the last three cards). WARN answered: `skeleton.lesson_taught` on
  uncertainty_at_shared_unit (four tasks teach it; here it decides controls only and sits beside a deciding lesson no
  task on file teaches, forward_window_structure_change) and concurrent_change_in_comparison (two); `skeleton.house_lesson`
  on forward_window_structure_change, validation_cannot_see_condition, concurrent_change_in_comparison and
  transport_effect_modifiers (each one step of six); `repeat.deliverables` pdf+xlsx against task8 (a committee's
  one-page note and the workbook grants are issued from); `driver.near` against this slot's v7 and v6 (0.20, 0.12;
  their deciding steps were each use's saving and the visits in the comparison arm, neither of which decides here).
  The shell: which, the, xlsx (v8's was which, i, xlsx).

## Deep reasoning

Task type: efficiency-savings-verification (energy efficiency and demand response evaluation), which serves Experiment & Causal Analysis
Domain test: every result is a measurement and verification quantity on weather-normalised metered gas: each measure's saving against the lottery's passed-over owners season by season; an operational measure's persistence against the counterfactual its life will actually face; the interaction of a heating check with hydraulic balancing (a lowered heating curve sticks only in a balanced system); a setback saving that grows with the hours a building stands empty and is nil where people live round the clock; a roof insulation saving bounded by the roof's share of the heat loss and untouched by the hot water; lifetime tonnes of gas CO2 per euro of grant, and an evidence standard a grant committee can hold a measure to
Swap: "fund insulation alone, because optimisation's saving levelled only while the campaign's checks lasted and controls' evidence rests on a few owners" read with a hospital's nouns keeps a skeleton and loses what decides: a heating curve a check resets and a balanced system holds, a campaign's district-by-district rollout as the record that separates it from the measure's own fade and from the price shock, a setback that saves nothing until empty spells outlast the reheating, degree-day normalisation and lifetime tonnes of gas CO2
Where the weight sits: investigation, in R2 and R3: heating optimisation's measured saving levels at about 4.4 per cent from 2022/23 on, and a run that fits its fade to the seasons as measured carries that level over fifteen years; the works' own saving is read off each works building's seasons before its campaign check (and the owners who declined it) against the passed-over owners outside the season of their own check, and keeps falling to about 1.5 per cent, while the price shock moved works and passed-over buildings alike and so explains none of it; and uncertainty, in R7: the pilot's evidence for controls rests on a handful of owners whose facility managers kept or overrode their timers across all their buildings, so its range at the owner runs past €140 where a building-level range stops near €107
Layer 1: cumulative index reads at 30 April with late and early periodic reads, meter exchanges, five-digit counters that roll over, estimates replaced by corrections, customer typos corrected, rows imported twice, meters in tens of cubic metres, z-numbers and calorific values (the L-gas to H-gas change of 2017), second meter points, connections and disconnections, the service team's reads at a check (both rounds), extensions and empty floors, revised applications sent twice, a contractor typed without its legal form; in the electricity profiles, a second market location per customer, a meter exchanged during 2025, public holidays averaged into their weekdays; in the cadastre, one row per roof face, "str." for "straße", a garage or shed beside the main roof; each is the producing system's own and none decides a result
Not one thing: the call needs two unrelated judgments, each deciding a different measure: heating optimisation's saving without the closed campaign's held lift (golden about €117 a tonne, upper end over €140; the measured seasons carried give about €77, upper end €104, and fund it) and controls' range at the owner the pilot was drawn by (upper end over €140; a building-level range stops near €107 and funds it); insulation passes on every route. A run that makes neither funds all three, one that makes only the first funds insulation and controls, one that makes only the second funds insulation and optimisation; the transports along the empty week and the roof per floor, the lottery season by season, the round at close and the 2025/26 CO2 are earned or lost on their own
One-fact test: the strongest single sentence ("the state campaign's checks from September 2022 set heating curves back down, the pilot's balanced works buildings held it, and the campaign has closed") rescues R2, R3 and R10's optimisation rows (3 of 11, under a third of the results); it leaves controls' range, and so the call, wrong; the owner sentence ("the pilot was drawn by owner and an owner's buildings move together") rescues R7 and nothing upstream (effort.json, measured)
Not semantics: every field read correctly (the read reasons, the draw by owner, the measure, the notices' use and floor area, the reference consumption, the revised application, the profiles' weekdays and hours, the roof faces) and every Layer 1 item handled, the careful pass still files R2, R3, R7 and the call wrong, because none of them is a reading: one is an investigation of what held a saving up, the other the spread a design gives
Not rule application: no filed procedure performs a result; the plan files what a saving is, what lifetime tonnes and a round's rate are and the limit, and the committee's request files the €120 test's basis (the applications received by 12 June) and its rule (each measure judged at the upper end of its 90 per cent range); how the pilot's saving is estimated, what held it up, how it carries over the life and to a building, and how the range is built are left to the analysis
Estimand: plan 4.2 (a saving as a share of the gas the buildings that had the works would have used, normal weather), 4.3, 4.4 (lifetime tonnes in the building applied for, over the measure's life, against the gas it would use without the works, on the application's reference consumption; the round's saving rate; grant per tonne; the limit), 4.5 (reference consumption), 4.6 (the season saving: what the works buildings would have used that season without the works, less what they used); the 2026 terms (applications to 30 June, a revised application replacing the earlier one); the committee's request (the €120 test on the applications that came in by 12 June, each measure funded only where the upper end of its 90 per cent range, the range a fresh draw of the pilot would give, is within it); the heat plan summary (the campaign's checks, September 2022 to March 2026, closed); the pilot rules (the draw among the owners who answered, an owner's buildings together); the prompt
No decoy: no memo, draft, stakeholder figure or copied block; no shipped file states a saving, a rate, a grant per tonne, a range or a recommendation; no shipped sentence links the campaign to a measure's saving or a facility manager to a range; the committee request asks and states nothing
No replay: no result re-derives a published figure and no stated number is wrong
Pinned: every rival in the fork table run on the cut pack by checks.py lands inside its result's band or is ruled out by a filed sentence or named data; each hurried route lands outside by an asserted margin; every measure's call holds by 8 per cent or more of the limit under every rival and falls on the other side under its shortcut
Run forecast: R2 and R3 stopped at the first story and self-confirming check (the fade fitted to the seasons as measured, its back-test on the later seasons passing because every one of them carried the campaign, or the levelling read as the price shock's); R7 method shortcut (buildings resampled, as the architecture 7 run did); the call follows; R10's optimisation rows follow R3; R9's funded tonnes follow the call; R1, R4, R5, R6, R9's counts and R11 earned
Strategy label: a randomised effect read net of a later programme that the treated units' own physics held (a forward window without it), beside ranges at the draw's unit (sulfur-strategies.md, causal_design)
Depth level: 4 on the client's scale, with level 5's mark: two independent judgments each decide a different measure, every combination of shortcuts lands on a different funded set (all three; insulation and controls; insulation and optimisation; the golden insulation alone), and around them the lottery season by season, both transports, the lived-in buildings, the round at close and the 2025/26 CO2 each move a graded figure. Not 5: a strong run on file earns the lottery, both transports and the round at close, so two judgments, not four, decide the call for it
Lesson: an operational measure's measured persistence is only the persistence it had under the conditions of the trial's seasons; when a later programme re-applied part of the treatment and the treated units' own physics held it, the trial's late seasons overstate what the measure keeps in a forward window without that programme, and the programme's staggered timing is what separates the two; and a trial drawn by group carries the evidence of its groups, so its range is built at the group

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each measure's saving in the pilot's works buildings in each season 2019/20 to 2025/26, against the owners the draw passed over | causal reasoning | the draw by lot among owners within each measure (rules 3); plan 4.2 and 4.3 | 1.5 points a cell (the comparison taken use by use, the draw's effect scaled by completion) | method shortcut: the works buildings' own before and after | - | Ask 1 |
| R2 | heating optimisation's saving each season as its works alone keep it (falling to about 1.5 per cent by 2025/26), against the measured (levelling at about 4.4) | investigation loops | the campaign's dates (heat plan summary); each building's check read (meter file); plan 4.2 | 1 point in the last three seasons (works rows before their check or none, with or without the passed-over owners' check season) | stopped at the first story: the measured seasons read as the measure's own fade, or the levelling read as the price shock's | R1 | Component 1 |
| R3 | heating optimisation's saving rate over its life on this year's applications: about 2.9 per cent | forecasting | plan 4.4 (against the gas the building would use without the works over the life) | 0.4 points (the level from the last two or three seasons, a fitted approach to a level, each season's own weights) | self-confirming check: the measured seasons' fade fitted and back-tested on the same campaign-held seasons (about 4.5) | R2 | Ask 2 |
| R4 | controls' saving along the share of the week a building stands empty, the hotels and care homes lived in round the clock; this year's controls applications about 0.70 empty | missingness-measurement | the 2025 profiles and the lottery's bands (data) | as architecture 8 | narrow look at broad data: one saving per use | R1 | Component 3 |
| R5 | insulation's saving of the heating along the roof per floor; this year's insulation applications about 1.1 square metres of roof per square metre of floor | modeling | the cadastre over the register and the lottery's bands (data) | as architecture 8 | narrow look at broad data: one saving per use | R1 | Component 3 |
| R6 | insulation's and controls' saving rates over their lives on this year's applications | causal reasoning | plan 4.4 | 0.8 and 0.6 points | unfinished chain: each use's pilot saving on this year's mix | R4, R5 | Ask 2 |
| R7 | each measure's grant per lifetime tonne with its 90 per cent range as a fresh draw of the pilot's owners would give it, every step repeated | uncertainty | the draw among owners (rules 3); the committee's rule | points 5 per cent (optimisation 15); range ends 8 per cent | method shortcut: buildings resampled within use and arm (controls' upper end about €107) | R3, R6 | Ask 3, Component 2 |
| R8 | the funded set: insulation alone (optimisation's and controls' upper ends over €140) | synthesis | the committee's rule | the set exact | unfinished chain: all three funded (the measured seasons carried, buildings resampled) | R7 | Recommendation |
| R9 | each measure's applications once the offer closes and the grant they ask, and the lifetime tonnes the funded round buys | forecasting | the 2026 terms; the 2019 answers' dates, sizes and withdrawals | counts and grant 10 per cent; tonnes 10 per cent | method shortcut: one share for every measure; the funded tonnes follow the funded set | independent: the 2019 responses (counts); R8 (tonnes) | Ask 4 |
| R10 | every application received with its grant and lifetime tonnes | synthesis | plan 4.4 and 4.5 | 5 per cent a row | unfinished chain: optimisation's rows at the measured seasons | R3, R6 | Ask 5 |
| R11 | the CO2 the pilot's works saved in 2025/26: what the works buildings would have used that season without the works, less what they used | synthesis | plan 4.6 | 3 per cent | method shortcut: the seven-season average on the 2018/19 use; dismissed own evidence: the campaign's held lift taken out of a season in which it was the works' own saving | R1 | Ask 6 |

Carry-forward: R9's counts and grant are graded on inputs of their own (the 2019 responses, the 2026 applications) and stand whatever the rates; R11 needs only R1's last season; R2 and R3 fall with R1's optimisation column only; R4, R5 and R6 fall with R1; R7's ranges are graded on their own construction at each measure's own point; the call R8 needs R3 and R7; R9's funded tonnes need R8; R10's optimisation rows need R3, the rest R6.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| the state campaign's heating checks (September 2022 to March 2026) set heating curves back down; a balanced system holds it, an unbalanced one soon loses it | constructed (every taker's curve reset; the hold set by each building's balancing) | no: every district, both arms of every measure and the whole stock took checks; they move insulation's and controls' arms alike and every non-pilot building; only in heating optimisation's works buildings, balanced by their works, does the check stick | investigation: the levelling against the works' own fade, the campaign's district-by-district dates in the meter file's check reads, the works buildings before and after their own check, the price shock ruled out because it moved both arms alike | modelling: the works' own saving read off the seasons before each building's check, its settled level over the life, and the forward window without the campaign | keep: one of two judgments the call needs |
| an owner's facility manager runs all its buildings' heating one way (controls' timers kept or overridden; how far a curve creeps) and a portfolio's buildings drift together | constructed (an owner effect on every portfolio) | no: every owner of every use and both arms; the draw itself was by owner (rules 3) | the pilot rules and the data (an owner's buildings move together) | method: the range at the owner, every step repeated | keep: one of two judgments the call needs |
| controls' saving growing with the share of the week a building stands empty, nil where people live round the clock | constructed | no: every building has a week | modelling: the profiles at another grain | measurement and modelling | keep, earned by the runs on architecture 8 |
| roof insulation's saving growing with the roof per floor | constructed | no: every building has a roof | modelling: the cadastre over the register | assembly and modelling | keep, earned by the runs on architecture 8 |
| this year's owners choosing their measure on those properties, and owners checked in the campaign's last two winters asking for optimisation more often | constructed | no: every 2019 answer and 2026 application is a choice | only by measuring the properties | none beyond R4 and R5 | keep |
| heating optimisation's own saving falling back as heating curves are turned up | constructed | no: every heating optimisation works building | the seasons before each building's check | modelling: the level it settles at | keep |
| the 2022 price shock | constructed | no: every building, both arms alike | the arms' own seasons | none: a rival explanation the data rule out | keep, texture |
| the first round's burner checks (August 2019 to March 2022) | constructed | no: every district, both arms alike | a read reason in the meter file | none | keep, texture |
| late insulation answers larger and more often withdrawn | constructed | no | a query on the 2019 responses | modelling: count, size and withdrawal projected measure by measure | keep |
| extensions and empty floors | constructed | no: across the stock | the floor area on the notices | none | keep, texture |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 each measure's saving by season | Missed | Right | Right |
| R2 optimisation's saving as its works alone keep it | Missed | Missed | Right |
| R3 optimisation's saving over its life | Missed | Missed | Right |
| R4 controls along the empty week | Missed | Right | Right |
| R5 insulation along the roof per floor | Missed | Right | Right |
| R6 insulation's and controls' rates on this year's applications | Missed | Right | Right |
| R7 each grant per tonne and its range | Missed | Partly | Right |
| R8 the funded set | Missed | Missed | Right |
| R9 the round at close and the funded tonnes | Partly | Partly | Right |
| R10 every application's grant and tonnes | Missed | Partly | Right |
| R11 the pilot's 2025/26 CO2 | Missed | Right | Right |
| Roughly | 0 of 11 | 6 of 11 | 11 of 11 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (provisional until the pack is cut)
Largest single hint: "the state campaign's checks from September 2022 set heating curves back down, the pilot's balanced works buildings held it, and the campaign has closed"; rescues 3 of 11 results
Pair estimate: provisional

## Frontier check

Precedents: R2 and R3 lost: N08 (the architecture 7 run on this world: "Age and calendar effects cannot be separated completely ... The uncertainty ranges do not cover this structural assumption"), L26 (a plausible shallower explanation that passes its own checks), L28 (the estimator certified by checks that cannot see the problem), L31 (a recent fall read as permanent); R7 lost: L19 (default intervals although the allocation unit was read), L35 (an independence model where units share shocks), and the architecture 7 run's own building bootstrap ("2,000 building-bootstrap replicates per measure"); R4, R5 and R6 earned: R23 (the architecture 8 runs reproduced both transports, `runs/review_2026-11-11.md`)
Shallow path checks: R2/R3: the fade fitted to the measured seasons fits them closely and a back-test on the last three seasons passes, because every one of those seasons carried the campaign (validation_cannot_see_condition); the price shock story fits the calendar; the check of another kind is the works buildings' seasons before and after their own campaign check, district by district in the meter file's check reads, which shows the saving stepping up at each building's check and the price shock moving both arms alike. R7: a building-level bootstrap is stable across seeds and B; the check of another kind is the draw itself (rules 3: owners drawn, an owner's buildings together) and the owners' own buildings moving together in the gas file
Assumption made false: "the pilot's seasonal pattern recurs for new works" (named and waved through by the architecture 7 run); false here because the pilot's late seasons carried a campaign that the 2026 works' life will not, tested from the meter file's check reads by district and the heat plan summary's campaign dates; and "buildings are independent" (the arch 7 run's bootstrap), false because the draw and the facility management are by owner, tested from the register's owners and the pilot rules
Forcing: provisional on the clean truth (seed 70706): optimisation's golden €117 (upper end €148 at the building, €200 at the owner) against the measured route's €77 (upper end €104 at the owner, €86 at the building) and the seven seasons flat €69; controls' upper end €143 at the owner against €107 at the building; insulation's upper end €100; each measure's rivals and shortcuts asserted in checks.py once the pack is cut
Noun swap: nearest on file html:nursing-home-citations and html:county-pairs-network (act only if the interval clears, the interval at the shared unit): swapped in, the interval at the owner carries across and decides controls here, but the deciding lesson (a measured persistence held up by a closed campaign, separated by its staggered timing) and the decision's other two measures do not; nearest in this slot, v8 (the transports and a capacity replay) and v6 (visits in the comparison arm only, one exclusion): the transports carry across as earned steps, the capacity and the comparison-only visits do not

## Data provenance

Source: generated by task7/generator (world.py simulates the utility's commercial customers, their owners and portfolios, each building's week, storeys, electricity and heating curve, the weather station, the benchmarking notices, the 2019 lottery drawn by owner, the service team's two rounds of checks and the 2026 offer; pack.py writes each system's export; docs.py the council's, the state's and the utility's documents)
Behaves like the real thing: buildings carry their own level and envelope, a slow drift (shared within a portfolio) and season noise, weather through degree days on the type's hot-water share, the pandemic winters and the 2022 price shock by use, extensions and empty floors, a heating curve that sits above need and creeps back after any reset, faster where the system was never balanced, burner checks, a week of their own whose electricity follows it, roofs set by storeys and pitch, quotes priced on the roof or the floor and answer dates driven by job size; owners answer for all their buildings with one measure and their facility managers run them alike
Genuine patterns: (1) degree-day weather response with use-specific hot-water shares (2) a slow drift, shared within a portfolio, and season noise (3) the pandemic winters and the price shock, different by use (4) each measure's saving varying building by building along its driver and by owner (5) a heating curve's creep back after a reset, held by balancing (6) electricity load following each building's week, shaped through the day (7) answer timing and quote size scaling with the job (8) checks rolled out district by district in two rounds
Problems by process: periodic reads taken days off 30 April, meter exchanges, counter rollovers, estimates later corrected, customer typos, re-imported rows, meters counting tens of cubic metres, the 2017 gas-quality change in one network area, second meter points, connections and disconnections, revised applications sent twice, a contractor typed without its legal form, second market locations per customer, a meter exchanged mid-2025, roof faces per address with outbuildings and an abbreviated street spelling
Breadth: 24,000 buildings in about 13,900 owners and 25,900 gas meter points over thirteen seasons, about 400,000 reads, the 2025 typical weeks of 25,500 market locations, 46,900 roof faces, 37,000 notices, 3,150 pilot answers across six uses and three measures, about 870 applications; choosing which comparison, which seasons, which buildings, which property and which unit carries each result is the work

## Template check

Chain signature: causal reasoning, investigation loops, forecasting, missingness-measurement, modeling, causal reasoning, uncertainty, synthesis, forecasting, synthesis, synthesis
Question form: which (the measures that clear the committee's rule), with the round at close and the pilot's 2025/26 CO2 beside it
Nearest build: task7 v8 (the same world, the call on capacity); task15 (a field trial with a concurrent change in the comparison and a transport); the client's nursing-home-citations and county-pairs-network (the interval at the shared unit); no build on file reads a randomised effect's persistence net of a later programme that the treated units' physics held

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "saving" in a season | the share of the gas the works buildings would have used (aggregate); the average building's share | aggregate | plan 4.2 |
| SF2 | heating optimisation's saving over its life | against the gas the building would use without the works over the life (no campaign: it closed); against the seasons as measured | without the works, campaign closed | plan 4.4 and the heat plan summary (the campaign closed in March 2026) |
| SF3 | the 2025/26 saving | what the works buildings would have used in 2025/26 without the works, the campaign's checks as they came; the same with the campaign's lift taken out | as the season came | plan 4.6 (the season's own saving) |
| SF4 | the 90 per cent range | the spread a fresh draw of the pilot would give (owners redrawn, every step repeated); buildings redrawn | owners | the committee's request and rules 3 (the draw among owners) |
| SF5 | the committee's rule | a measure funded where the range's upper end is within €120; where the point is | the upper end | the committee's request |
| SF6 | the applications the test is taken on | received by 12 June; projected to 30 June | received by 12 June | the committee's request |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the pilot's works buildings and passed-over owners by measure; the applications received by 12 June for the test; the round's applications to 30 June for the round at close | filed: rules 3, terms 1 to 3, the committee's request, the prompt |
| 2 | Unit of account | the building for a saving and an application; the owner for the draw | filed: plan 4.4, terms 2, rules 3 |
| 3 | Attribution window | the season, 1 May to 30 April; the week of 2025 for the electricity | filed: plan 4.3 |
| 4 | As-of dating | the applications received by 12 June; the campaign's dates | the request; the heat plan summary |
| 5 | Version basis | a revised application replaces the earlier one | filed: terms 2 |
| 6 | Denominator | the gas the works buildings would have used | filed: plan 4.2 |
| 7 | Weighting | the gas | filed: plan 4.2 and 4.4 |
| 8 | Window length | seven seasons observed, the service lives filed | filed: plan 4.4 |
| 9 | Boundary inclusivity | €120 or less at the upper end funds | filed: the committee's request |
| 10 | Rounding path | none in the prompt; figures at their natural precision | the answer blocks |
| 11 | Tie-break | none needed | - |
| 12 | Maturity and censoring | the round open to 30 June; seasons after the seventh unobserved | the prompt; plan 4.4 |
| 13 | Order of operations | normalise, compare, carry, weight; the range around the whole chain | plan; the committee's request |
| 14 | Row order | export order | - |
| 15 | Duplicate resolution | re-imported reads once; a revised application replaces the earlier | terms 2 |
| 16 | Identity normalisation | meter points to buildings; market locations to buildings; roof faces to buildings by address; owners by the register's owner number | the files' keys |
| 17 | Netting against gross | none | - |
| 18 | Dimensional units | cubic metres to kWh by z-number and calorific value | method 2 |
| 19 | Code and status semantics | read reasons (a check read in either round); drawn, withdrawn and completed | the files' own columns |
| 20 | Integerisation | applications at close whole, as an estimate | - |
| 21 | Clause scope | plan 4.4 for each measure in the round | filed |
| 22 | Forward window contents | the 2026 works' life without the campaign (closed March 2026); the applications still to come | the heat plan summary; the 2019 responses |

## Literal reader

Executed word for word, plan 4.2 and 4.3 with the pilot rules give each season's saving against the passed-over owners
(R1); plan 4.4 asks for each application's saving in the building applied for over the measure's life against the gas
it would use without the works, which the heat plan summary's closed campaign sets without further checks (R3, R6, R10);
the committee's request funds a measure only where the upper end of its 90 per cent range, the range a fresh draw of
the pilot would give, is within €120, and rules 3 says the draw was among owners (R7, R8); 4.6 gives the 2025/26
saving as the season came (R11). No sentence names the campaign's effect on a measure, a balanced system, a facility
manager, a resampling unit, a persistence model or a comparison.

## Prompt contract

May not drop or change: the question (which of the pilot's measures the 2026 round can fund, under €120 of grant per lifetime tonne of CO2 and the committee's rule of judging each at the top of its 90 per cent range); that the figures are estimates because the works run past the seasons the pilot has seen; a one-page note with the answer and a workbook; for each measure its saving in the pilot's works buildings in each season since the works, its saving rate over its life on the applications received so far, their grant per lifetime tonne with its 90 per cent range, and how many applications it will have once the offer closes with the grant they ask; the lifetime tonnes the funded round buys; every application received so far with its grant and lifetime tonnes; the pilot's 2025/26 CO2. Must never add: a method (a comparison, a fade, a campaign, a check, a balanced system, an owner or facility manager, a resampling unit, a driver, a load profile, a roof, a projection), a warning, an attached file's name, a role, a rounding instruction or a count the data hold.

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
- 2026-11-09, architecture 7 at design: the reviewer's suggestion of buildings that changed floor area as a lever
  (an insulation works arm whose owners converted their attics after the roof works): every reading that sets the
  converted buildings aside or censors them at the change is unbiased when converters save like the rest, so the fix is
  one filter, and when they save more it needs the new space's gas estimated from conversions that themselves include
  roof insulation; kept only as texture (extensions and empty floors across the stock, balanced by the draw).
- 2026-11-09, the visits kept as a modelled factor (deferred in the works arm, uneven, logged from 2021): a constant
  visit term in the comparison corrects the bias once the visits are known, which is the one extra term the client
  names; the visits now reach both arms by district and decide nothing.
- 2026-11-09, the saving as the average building's share (mean of logs): controls 1.3 points and insulation 0.8 points
  over the gas-weighted share and the 2025/26 saving 11 per cent apart by use; plan 4.2 now files the share of the gas.
- 2026-11-09, heating optimisation keeping 20 to 40 per cent of its first season: the flat route and the golden
  family sat within the 90 per cent range of each other; it now keeps about 5 per cent, levelling by the fourth season.
- 2026-11-09, the prompt's rounding sentence (savings to one decimal, grant per tonne to the euro, counts to 10, grants
  to EUR 10,000, round totals to EUR 0.1 million, tonnes to 10, the 2025/26 CO2 to 100): dropped at the author's word;
  the golden and the answer blocks now state each figure at its natural precision, every value unchanged (the widest
  printed shift under the old rounding was 94 application rows under 10 tonnes printed as 0 or 10).
- 2026-11-09, architecture 7 on the platform (the author's test run, `runs/arch7/run1.md`, no score pasted): the run read
  the lottery as drawn (instrumented on completion), priced each use's saving to this year's applications, carried
  heating optimisation's fade on its last three seasons and projected the round measure by measure, landing the call at
  87, 95 and 139 euro a tonne; it lost only the round's insulation count (312 against 343) and heating optimisation's
  figure. Every judgment of the chain was one a frontier run makes unprompted, so the chain priced nothing; re-rooted as
  architecture 8 at the author's choice, the transport moved onto each measure's driver read from another record.
- 2026-11-09, architecture 8 at design: the service team's burner checks setting the boiler's clock to the building's
  hours as the controls driver (a check that finds the clock unset sets it): controls saved about 7 per cent against
  unchecked buildings and 2 per cent against checked ones, but the use-priced route landed within 2 per cent of the
  golden (4.06 against 4.21 per cent), no separation, and a check is an event in both arms the reviewer names.
- 2026-11-09, a size-aware projection of the round (late answers reweighted by size and use): 343 to 348 insulation
  applications against the world's 395, no closer than the golden's; R8a's band widened to 10 per cent instead, so a
  recipient-level response model like architecture 7's run (312) lands inside it.
- 2026-11-09, heating optimisation's fade by occupancy class as the second lever (hotels and care homes turning the
  curve back up at night): each use's seven-season level already carries most of it, so the pooled fade on use levels
  and the class fade sat 4 to 7 per cent apart; the second lever moved to the roof.
- 2026-11-09, the round at close as the funding population (late insulation applications larger and capped): received
  and late applications' grant per tonne differed by 1 to 6 per cent in the world; no lever.
- 2026-11-09, the lived-in rule on a weekend maximum over minimum of 1.10: the base load's 3 per cent hour-to-hour noise
  put every closed conference house and day-care centre over it; the rule now sets weekend days against weekend nights
  at 1.08, agreeing with the world on 99.98 per cent of buildings.
- 2026-11-09, the 2019 owners choosing on the drivers at a third of the 2026 strength: it halved both levers (controls
  125 by use against 119 by the empty week); 2019 owners now lean only slightly towards controls in an emptier
  building and not at all towards insulation on the roof.
- 2026-11-09, profiles and roofs only for buildings still on gas: 3 per cent of the pilot's answers (buildings that left
  the network) lost both; every building standing in 2025 now has a profile, every building standing at the 2023
  flight a roof.
- 2026-11-09, every drawn owner counted as treated (the offer's effect): with the roof driving insulation it now
  dilutes insulation past the limit, so SF3 is closed by plan 4.2's "the buildings that had them" rather than by
  convergence; the draw's effect scaled by completion stays within a point of the golden every season.
- 2026-11-09, a straight line through every band of controls' saving, the lived-in band included: 115.83 euro a tonne,
  funding controls on a line that fits the bands twice as badly as the threshold and rise; a hurried route outside the
  band, not a rival (SF18).
- 2026-11-09, stage 4, first judge pass (DETERMINISTIC, APPROVE, `determinism_check_report_pass1.md`): a single
  sentence naming both drivers rescued about half the chain, because a hotel's load then read about 60 per cent empty
  and fitting every building off its load still funded controls (112 euro a tonne); the lived-in buildings now carry
  their honest activity (a hotel's breakfast and evening peaks over a long low day and night, a care home's meals), so
  read off the load alone they look two thirds empty, the pilot's lived-in bands sit under the curve, and controls
  fail at 156.47; the both-drivers sentence rescues R4 and R5a only.
- 2026-11-09, stage 4, the reader: the profiles read as "a handful of standard shapes" (plateaus with sharp edges); a
  working day's shape (lunch, the afternoon tail, a restaurant's lull, shift breaks), part-staffed Saturdays, outdoor
  lighting at night and a day-to-day spread were added, and a continuous-operation rule (a load that never falls below
  three quarters of its peak has no empty hours) keeps a control room or a three-shift line from reading its night
  dip as an empty building.
- 2026-11-09, stage 4, second judge pass (NOT_DETERMINISTIC, SEND_BACK, `determinism_check_report.md`): the lived-in
  test written as "a hotel or care home whose weekend days run above its weekend nights" carried no margin; read as
  strict hour-by-hour dominance it held 2 per cent of the pilot's hotels and care homes lived in and put controls near
  the load-alone figure, over the limit. Repaired by a construction with no margin (every hotel and care home lived in
  round the clock, by its use on the register, which the lottery's own hotels and care homes bear out: two thirds
  empty off their load, under 1.5 per cent saved), the weekend test kept as a rival family that lands inside the band
  at every margin to 15 per cent once the lived-in buildings carry an honest base load (6 and 5 W a square metre for
  hotels and care homes, against 14 and 12 in use), and strict dominance inside R3's band with the same call.
- 2026-11-09, stage 4, third judge pass (NOT_DETERMINISTIC, SEND_BACK, `determinism_check_report.md`): with the lived-in
  step decisive for controls, no filed sentence made hotels and care homes lived in, so reading them off their load
  (159.57) survived as a rival, and a line through the lived-in band sat at 120.02. The step can be decisive only if
  it is filed, and filed it is a definition read; at the author's choice the lived-in buildings went back to their
  milder activity (a hotel reads over half the week empty off its load, not two thirds), so the step moves controls'
  figures, not the call (114.12), the use rule and the honest base loads kept, and the both-drivers hint recorded at
  6 of 13 as the build's level-4 risk.
- 2026-11-09, every hotel and care home made lived in by overriding the conference houses and day-care centres after
  the draw: it changed a few 2019 choices, redrew the lottery and shrank both levers (controls 115.4 against 132.5 by
  use), so it was reverted; the line through the lived-in band stays at 120.02, ruled out by its misfit.
- 2026-11-10, a run on the READY cut (pasted by the author, the audit in this session's record): it set the load
  profiles and the cadastre aside in one sentence, carried each use's saving and lost every point it lost there; the
  both-drivers sentence would have taken it from about 47 to 73 to 86 on the house split, and the controls driver alone
  would have landed the call through its own reading of the round at close. Level 3 in practice; levelled up rather
  than re-rooted, the backup in ~/Documents.
- 2026-11-10, buildings leaving gas as the heat plan's networks arrive (each measure's tonnes counted only while the
  building burns gas, the take-up read off an existing network's history), set aside at its scratch gate: with 8 per
  cent margins on both sides it decides the call only if about 83 per cent of insulation's reference consumption sits in
  the priority areas (21 per cent today), a concentration that would sit where it decides; with real shares the
  survival curve a careful run fits on the visible removals lands the golden's side. Controls sits near the line (128 by
  use, 103 on its own building), so a second judgment on the call has to leave controls almost untouched.
- 2026-11-10, the round at close as the basis of the €120 test (as plan 4.4 and terms 3 would read), with taller
  buildings answering later, set aside: this year's owners chose insulation on the roof, so few tall buildings are among
  the early applications and the late mix would rest on a handful of them, and the run's own forecast already hung a
  quarter of insulation's tonnes on two applications; the committee's request now files the basis instead (SF21).
- 2026-11-10, 16 of the 26 roofers still trading, rejected at calibration: the works then pay about three quarters of
  insulation's grant, and the funded pair lands within 8 per cent of every budget that also keeps insulation alone,
  paid in full, clearly over it; with 12 the pair pays 85 per cent of €8.2 million, every rival under 88, while paid in
  full (131) or counted in jobs (109) it runs over.
- 2026-11-10, after judge pass 5 (which approved the cut it read): the 2019 roofing record made less tidy (one working
  day in seven lost to rain, the same days for every firm; some firms starting a few days late; each roof faster or
  slower than its area alone says), the pace retuned so every 2019 roof still finished by 20 September, and the heating
  firms given more fitters so the two heating measures together would fit (the busiest firm at 81 per cent of its
  room); a data-only change, re-checked by the generator's assertions and leak.py, every graded figure moving by under a
  per cent bar the round's payment (6.99 million, inside the published bands).
- 2026-11-11, platform review of architecture 8 (returned; the holistic audit on the same version had passed it at
  level 5, pinned): the deciding step was one constructed hidden factor, the roofers' capacity on this year's larger
  roofs, which bit only in insulation (the heating firms had room) and left one routine step once named (pace times
  working days per firm; every reading within a tenth). The test responses reproduced the pilot seasons, both
  per-building transports (the empty week from the load profiles with the lived-in buildings, the roof per floor from
  the cadastre), the fade, the round at close and every carbon call, so the effort test's careful column, which priced
  both transports as lost, was 40 to 60 points optimistic as the run record warns. Agreed with the return, no
  rebuttal (`runs/review_2026-11-11.md`); re-rooted at stage 1 as architecture 9 in the same world at the reviewer's
  direction, the call moved onto analysis and the capacity out of the decision.
- 2026-11-11, architecture 9 at design: the service visits kept from architecture 8 in both arms as a decomposition (the
  reviewer's third suggestion) with a check resetting the curve in every building: in a world where a reset creeps back
  faster in a balanced building than an unbalanced one the visits nearly cancel between the arms (1.3 points early, 0.2
  late, about 7 per cent of the life), and with visits in the comparison arm only it is architecture 6 again; built
  instead as a campaign whose check a balanced system holds (the physics of balancing), with the first round's checks
  tuning burners only.
- 2026-11-11, architecture 9 at design: the decomposition's first estimator, an event study of the checks by arm with
  season effects, under-removed the works buildings' held lift (the lift collinear with the works' own seasons in a
  four-cohort rollout) and landed near the measured seasons; the golden reads the works buildings' seasons before
  their own check instead, and the level the works settle at is the last three such seasons weighted by the gas each
  rests on (a fitted approach to a level on the thin late seasons swung from €53 to €600 across seeds).
- 2026-11-11, architecture 9 at design: controls' range at the owner, with the owners' facility-management spread on the
  saving alone, came out only 1.10 times the building-level range at its upper end (seed 70707), too thin to force;
  the world now gives a portfolio's buildings a shared slow drift and controls a wider facility-management spread with
  less building-level noise, and seeds 70701 to 70715 were scanned for the scale-free margins; seed 70706 holds every
  call by 12 per cent or more under the golden and lands every shortcut on the other side.
