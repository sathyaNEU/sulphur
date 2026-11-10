# task7: which retrofit measures Haldenau's 2026 grant round funds, and what the round will pay (architecture 8)

Architecture 7 (each measure's lottery saving carried by building use and over its life to this year's applications)
passed its judge and was tested by the author on the platform on 2026-11-09: the run landed the call, every judgment
of the chain being one a frontier run makes unprompted (`runs/arch7/run1.md`). Its note, generator and goldens are in
git at commit d680af7. This architecture keeps the world, the lottery, the fade and the per-measure projection to the
offer's close, and moves the transport: this year's owners chose their measures knowing their buildings, and each
measure's saving follows a property of the building that no gas record carries, read from the meter operator's 2025
load profiles and the state's solar cadastre. Architectures 1 to 7 survive in the Tried and rejected record.

**Levelled up (2026-11-10, at the author's direction).** A run on the READY cut lost every point it lost to one
decision (it set the load profiles and the cadastre aside and carried each use's saving), and one sentence naming the
drivers, or the controls driver alone through its own at-close reading, would have given it the call: level 3. The
level-up adds a second judgment the call needs, from the same world's process and unrelated to the drivers: the council
has budgeted €8.2 million for what the round pays this year, a job not finished by 30 September is not paid, and under
half the roofers who did the 2019 roofs still quote while this year's roofs are larger. The committee's request now
files the basis of the €120 test (the applications received by 12 June) and the budget with its order. The READY cut is
backed up in ~/Documents/task7_arch8_backup_2026-11-09.zip.

## Draw

Subdomain: Energy Systems & Utilities, energy efficiency and demand response evaluation (`efficiency-savings-verification`)
Analysis type: Experiment & Causal Analysis (assigned on the platform task; what each measure's works did to a
  building's normal-weather gas use, against the comparison the 2019 lottery supports, carried to the 2026 round's own
  applicants)
Answer shape: scenarios with the flip point (each measure's grant per lifetime tonne on this year's applications against
  the €120 limit, with its range and the saving rate at which its call flips), with the round's settled grant beside it
Weight: modeling (each measure's saving along what it follows, fitted on the lottery's own buildings: a threshold and a
  rise in the share of the week a building stands empty, a line in the log of its roof per floor), with both properties
  measured from records the gas files do not carry, beside forecasting what the round pays once the works are done
  (each roofer's 2019 pace in square metres of roof against this year's larger roofs by 30 September), which the budget
  turns into part of the call; the last three builds sit on synthesis (task1), measurement (task4) and a hard-to-measure
  quantity (task6)
Data-native sentence: the pilot's places were drawn by lot, so the passed-over owners give each measure's saving, but
  this year's owners chose their measures knowing their buildings: the controls applicants' buildings stand empty far
  more of the week and the insulation applicants' have far more roof per floor than the pilot's buildings of the same
  use, both savings rise along those properties, and only the meter operator's typical weeks and the state's solar
  cadastre record them; and the roofers who must finish this year's larger roofs by 30 September are under half of
  those who did the 2019 roofs, whose completion dates show each firm's pace
People: Magda Peukert (chair, Committee for Climate and Environment) and Torben Römer (head of Energy Services,
  Stadtwerke Haldenau), from `guard.py names --geo Germany --seed 11`; neither is named in the prompt
Card: `.claude/skills/fingerprint/cards/task7.json`, v8, registered 2026-11-09 (stamp 2026-11-10T00:50:26Z UTC) at WARN;
  v7 moved into lineage with its fate. WARN answered: `repeat.deliverables` docx+xlsx against task1 (a committee note
  and the workbook the office issues grants from); at the final cut `repeat.gate_g` method_or_model_selection and `repeat.question_form`
  which against task6 v7, drawn since (the decision picks measures, so "which" is its form, and the transport along a measured
  driver is the method this build turns on). Differentiation on the card against task7 v7 (there the use on the
  notice, a property every gas record carries; here two properties measured from records at another grain), mark120 v1
  (a unit rebuilt by a two-hop join; here no unit is rebuilt) and mark253 v1. The decisive pattern is G2, grain
  mismatch: the properties live in a building's hourly typical week and the roof faces at its address, never in its
  season of gas. The shell: which, I, no rounding sentence, a note and a workbook.

## Deep reasoning

Task type: efficiency-savings-verification (energy efficiency and demand response evaluation), which serves Experiment & Causal Analysis
Domain test: every result is a measurement and verification quantity on weather-normalised metered gas: each measure's saving against the lottery's passed-over owners season by season, its persistence over the measure's service life, a setback saving that grows with the hours a building stands empty and is nil where people live round the clock, a roof insulation saving bounded by the roof's share of the building's heat loss and by the hot water it never touches, carried into grant per lifetime tonne of CO2 and into what a grant round will pay once its works are done by the deadline, a contractor's capacity read off its own completion record
Swap: "fund insulation and controls, because this year's controls applicants stand empty most of the week and this year's insulation applicants are low buildings with large roofs" read with a hospital's nouns keeps a skeleton and loses what decides: a setback that saves nothing until the empty spells outlast the reheating, a load profile whose night dip is sleep rather than absence, a roof's share of a building's heat loss, degree-day normalisation and lifetime tonnes of gas CO2
Where the weight sits: modeling and measurement, in R3 to R5: each building's empty week is read off its hourly typical week (its market locations summed, the hotels and care homes lived in round the clock told from their night dip), its roof per floor from the cadastre's roof faces over the register's floor area, each measure's saving fitted along them on the lottery's own bands, and every application priced on its own building; and forecasting, in R8c and R11: each roofer's 2019 pace in square metres of roof a working day, read off its pilot roofs and completion dates, fitted to this year's jobs in the order they were applied for from 13 July to 30 September, which the budget carries into the call
Layer 1: cumulative index reads at 30 April with late and early periodic reads, meter exchanges, five-digit counters that roll over, estimates replaced by corrections, customer typos corrected, rows imported twice, meters in tens of cubic metres, z-numbers and calorific values (the L-gas to H-gas change of 2017), second meter points, connections and disconnections, the service team's visit reads, extensions and empty floors, revised applications sent twice, a contractor typed without its legal form; in the electricity profiles, a building's annex or separately metered part as a second market location under the same customer number, a meter exchanged during 2025 leaving fewer measured days, public holidays averaged into their weekdays; in the cadastre, one row per roof face, "str." for "straße", a garage or shed beside the main roof at some addresses; each is the producing system's own and none decides a result (bar R2 and SF11 to SF14, SF20 in checks.py)
Not one thing: the call needs two unrelated judgments. Pricing each application on its own building (the empty week for controls, the roof per floor for insulation) is the only route on which both measures meet the limit; the works done by 30 September (each roofer's 2019 pace in square metres against this year's larger roofs) are the only reading on which the two fit the budget. A run told the drivers and paying every job as in 2019, or counting the roofers' work in jobs, funds controls alone; a run told about the roofers and pricing by use funds nothing; the roof alone passes insulation alone, which paid in full runs over the budget. Controls' figures also need the lived-in step (read off its load alone a hotel looks over half the week empty and controls come to 114 euro a tonne, the same pass on a figure outside its band); heating optimisation's fade, the round's count and grant at close and the 2025/26 saving are earned or lost on their own
One-fact test: the strongest single sentence still names both drivers ("this year's owners chose the measure that suits their building, so price controls along the share of the week each building stands empty, from its load profile, and roof insulation along its roof per floor, from the cadastre and the register") and rescues R3, R4, R5a, R5c and R7 (5 of 15, a third); it no longer rescues the call or the funded totals, which then fund controls alone on 2019's completion rate. The roofers' sentence rescues R8c and R11 (2 of 15); each driver's own sentence its two results; the lived-in sentence nothing for a pass that never opened the profiles (effort.json, measured)
Not semantics: every field read correctly (the read reasons, the draw, the measure, the notices' use and floor area, the reference consumption, the revised application, the profiles' weekdays and hours, the roof faces) and every Layer 1 item handled, the careful pass still files R3, R4, R5a, R5c, R6 and R8b wrong, because none of them is a reading: each is an estimate along a property the run has to think to measure
Not rule application: no filed procedure performs a result; the plan files what a saving is, what lifetime tonnes and a round's rate are and the limit, and the committee's request files the €120 test's basis, the budget and its order (from the lowest grant per tonne up, each where the budget covers what it pays); how the pilot's saving is estimated, along what it is carried to a building, how a building's week or roof is measured, how the saving carries over a life, how the round is projected and how much of its work the firms can do by 30 September are left to the analysis
Estimand: plan 4.2 (a saving as a share of the gas the buildings that had the works would have used, normal weather), 4.3, 4.4 (lifetime tonnes in the building applied for, over the measure's life, on the application's reference consumption; the round's saving rate; grant per tonne; the limit), 4.5 (reference consumption), 4.6 (the season saving); the 2026 terms (applications to 30 June, a revised application replacing the earlier one, payment on completion, nothing to an owner who withdraws or whose works are not completed by 30 September); the committee's request (the €120 test on the applications that came in by 12 June; €8.2 million for what the round pays this year, the measures taken from the lowest grant per tonne up, each where the budget still covers what its applications will be paid once the offer has closed and the works are done); the prompt (the applications received so far, a 90 per cent range, the flip rate, each measure's applications at close with the grant they ask for and what would be paid on them, the funded round's totals, every application received)
No decoy: no memo, draft, stakeholder figure or copied block; no shipped file states a saving, a rate, a grant per tonne or a recommendation; no shipped sentence links a load profile or a roof to a measure's saving; the committee request asks and states nothing
No replay: no result re-derives a published figure and no stated number is wrong
Pinned: every rival in the fork table run on the cut pack by checks.py lands inside its result's band (SF5, SF7 to SF10, SF16, SF17, SF19, SF20, SF23 to SF27) or is ruled out by a filed sentence (SF1 to SF3, SF11 to SF14, SF21, SF22, SF28) or named data (SF6, SF18, SF24's jobs, the lived-in band); each hurried route lands outside by an asserted margin; the funded pair pays 8 per cent or more under the budget on every rival of the works (14.7 on the golden) and 8 per cent or more over it paid in full or with the work counted in jobs
Run forecast: R3 and R4 narrow look at broad data (the saving split by the notice's use, the drivers left in two files the run reads as distractors, as architecture 7's run read the cadastre); R3 and R5c self-confirming check for a run that finds the empty week but fits every building off its load (the hotels and care homes sit under the curve and are fitted through, controls at 114.12); R5a and R5c unfinished chain (the pilot's use levels carried to applicants who chose on their buildings); R6 follows them to funding nothing; R7 self-confirming check (a range taken on the use-priced figure); R8c and R11 unfinished chain (every job paid at 2019's completion rate, the deadline in the terms never carried to the roofers) or self-confirming check (the roofers' work counted in jobs, which reads their 2019 pace as room for 80 per cent of this year's insulation grant); R6 then funds controls alone even with the drivers; R8b follows R6; R9 partly; a run that finds only one driver funds only its measure, or nothing
Strategy label: population selection on unrecorded properties (a randomised effect carried to units that chose their treatment on properties the trial's outcome records do not carry, each measured from a record at another grain), beside a persistence fit and a round projection whose payment rests on a capacity read off the firms' own completion record (sulfur-strategies.md, population_selection)
Depth level: 4 on the client's scale, with level 5's mark. Two unrelated judgments carry the call (each building's own saving along its driver, and the works the roofers can finish by 30 September), each needing estimation, either alone landing a different wrong set; around them the fade, the lived-in step, the round's timing with its sizes and withdrawals and the ranges each move a graded figure; the shortcuts land on four different wrong funded sets (nothing by each use's saving or the pilot's own mix; heating optimisation alone by the seven seasons carried flat; heating optimisation and controls by the before and after; controls alone with the drivers paid in full or counted in jobs, or with the empty week alone), and the golden holds across every defensible variant. Not 5: a strong run on file earned the lottery comparison, the fade and the round's count and grant, so two judgments, not four, decide the call for it
Lesson: a lottery's effect is exact for its own buildings; carrying it to a round whose owners chose their measure takes the property each measure's saving follows, which the outcome records do not carry and another record at another grain does, measured with what that record cannot show (an occupied building dipping at night), fitted on the lottery's own bands and carried building by building; and what a round pays is the work its contractors can finish by the deadline, measured in the unit the work takes (a roof's square metres, not the job), which the same owners' choice made larger this year; no build on file teaches either (task7 v7 carried by a recorded use; task2 weights a rate to a new mix in one step)

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each measure's saving in the pilot's works buildings in each season 2019/20 to 2025/26, against the owners the draw passed over | causal reasoning | the draw by lot within each measure (rules 3); plan 4.2 and 4.3 | a point a cell (two-season baseline, comparison by use, the draw's effect over completion) | method shortcut: the works buildings' own before and after, 3 to 4 points off every cell | - | Ask 2 |
| R2 | heating optimisation's saving over its 15-year life in the pilot's buildings: 2.15 per cent | forecasting | plan 4.4 lives; the seasons levelling off (data) | 0.25 points (the last season or the last three carried, a two-season baseline) | method shortcut: the seven seasons' average carried flat (3.78) | R1 | Component 1 |
| R3 | controls' saving along the share of the week a building stands empty: nothing until about 40 per cent, 2.92, 5.99 and 9.06 per cent at half, three fifths and seven tenths; this year's controls applications 68.15 per cent empty, the pilot's controls buildings 38.38 (every hotel and care home lived in round the clock) | missingness-measurement | the 2025 profiles and the lottery's bands (data) | 1.2 points at each reading (four or eight bands, the load read at 40 or 60 per cent of its range, hotels and care homes lived in only where their weekend days run 0 to 15 per cent above their nights or where every weekend day hour runs above every night hour, a line through the bands of buildings that close); 3 points on the empty week | narrow look at broad data: one saving per use (4.76 for every building); self-confirming check: the hotels and care homes read off their load alone (0.55, 4.22 and 7.90 per cent at the three readings; controls at 114.12 a tonne) | R1 | Component 2 |
| R4 | insulation's saving of the heating along the roof per square metre of floor: 24.05, 15.09 and 6.14 per cent at one, a half and a quarter; this year's insulation applications 1.13 square metres of roof per square metre of floor, the pilot's 0.79 | modeling | the cadastre over the register and the lottery's bands (data) | 3 points at each reading (four or eight bands, the bands as steps); 7 per cent on the roof per floor | narrow look at broad data: one saving per use (19.48 of the heating at any roof) | R1 | Component 3 |
| R5a | insulation's saving rate on the applications received, over its life: 22.46 per cent | causal reasoning | plan 4.4 (in the building applied for) | 0.8 points (every SF7 and SF19 rival) | unfinished chain: each use's pilot saving on this year's mix (18.49) | R4 | Ask 3 |
| R5b | heating optimisation's saving rate on the applications received: 1.98 per cent | causal reasoning | plan 4.4 | 0.25 points | method shortcut: the seven seasons carried flat (3.78) | R2 | Ask 3 |
| R5c | heating controls' saving rate on the applications received: 8.64 per cent | causal reasoning | plan 4.4 | 0.5 points (every SF7, SF16 and SF17 rival) | unfinished chain: each use's pilot saving on this year's mix (6.97) | R3 | Ask 3 |
| R8a | each measure's applications once the offer closes and the grant they ask for | forecasting | the 2026 terms; the 2019 answers' dates and quotes | 10 per cent (one withdrawal rate; a recipient-level response model) | method shortcut: one share for every measure, or late jobs priced like early ones | independent: the 2019 responses and the 2026 applications | Ask 5 |
| R8c | what each measure's applications would be paid once the works are done by 30 September: insulation 5,496,863 of 9,263,399, controls and heating optimisation in full | forecasting | the 2026 terms (nothing paid on works not completed by 30 September); the 2019 completions by firm; the 2026 quotes' firms | 10 per cent (the firms' work in one queue, the late applications shared by the firms' pace, each roof read off its quote, the late roofs larger by their grant, the works from 20 July) | unfinished chain: every job paid at 2019's completion rate; self-confirming check: the roofers' work counted in jobs (80.25 per cent of insulation's grant) | independent: the 2019 completions and the 2026 quotes' firms | Ask 5 |
| R11 | how many of each measure's applications at close would be paid: insulation about 172 of 275 | forecasting | as R8c | 10 per cent (as R8c) | unfinished chain: every application not withdrawn counted as paid (275); self-confirming check: the roofers' work counted in jobs | independent: the 2019 completions and the 2026 quotes' firms | Ask 5 |
| R6 | grant per tonne and the funded set: insulation 108.69 and controls 103.25 euro meet the limit and fit the budget, heating optimisation 193.18 does not | synthesis | plan 4.4, the limit and the committee's budget and order | 5 per cent (heating optimisation 10); the set exact | unfinished chain: each use's saving funds nothing (131.98, 127.98); with the drivers, every job paid as in 2019 or the work counted in jobs runs the pair over the budget and funds controls alone | R5a, R5b, R5c, R8c | Recommendation |
| R7 | each grant per tonne's 90 per cent range and the saving rate at which each call flips: 20.34, 3.18 and 7.44 per cent | uncertainty | the applications; the pilot's buildings drawn again within use and arm, the bands and fits repeated | flips exact to 0.05; range ends 5 per cent | self-confirming check: a range on the use-priced figure (insulation 125 to 143, controls 118 to 140) | R5a, R5b, R5c | Ask 4 |
| R8b | the funded round's totals against the budget: 11,451,661 euro asked, 6,992,958 paid, within the 8.2 million | synthesis | the funded set, R8a and R8c | 10 per cent | unfinished chain: nothing funded, nothing asked; or controls alone, every job paid | R6, R8a, R8c | Component 4 |
| R9 | every application received with its grant and lifetime tonnes (829 rows, 42,822 tonnes) | synthesis | plan 4.4 and 4.5 | 5 per cent a row | unfinished chain: the use levels on every controls and insulation row | R5a, R5b, R5c | Ask 6 |
| R10 | the CO2 the pilot's works saved in 2025/26: 3,216 tonnes | synthesis | plan 4.6 | 3 per cent (each use's own 2025/26 saving) | method shortcut: the seven-season average on the 2018/19 use (4,411) | R1 | Ask 7 |

Carry-forward: R8a, R8c and R11 are graded on inputs of their own (the 2019 responses with their contractors and completion dates, the 2026 applications with theirs) and stand whatever the rates; R10 needs only R1's last season; R2, R3 and R4 each fall only with R1, which the careful pass earns; each measure's rate R5 needs only its own driver's result, so a run that finds one driver keeps that measure's rate, range and rows and loses the other's; the call R6 and the funded totals R8b need both drivers and R8c.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| controls' saving growing with the share of the week a building stands empty (nothing until the empty spells outlast the reheating; nil where people live round the clock) | constructed (every building's week simulated from its use's archetypes, its own cut set by its empty week) | no: every building of every use has a week; within offices, shops and workshops the emptier half of the pilot's controls answers saves more (asserted); it moves no other measure | modelling: each building's week measured from the hourly profiles, the lived-in buildings told apart, banded on the lottery and fitted | measurement and modelling: the empty week from another file at another grain, a threshold and a rise | keep: a physical driver across the stock, one of two |
| roof insulation's saving growing with the roof per square metre of floor | constructed (storeys by use, each building's cut set by its roof per floor) | no: every building has a roof; within offices, shops and workshops the roofier half of the pilot's insulation answers saves more (asserted) | modelling: the cadastre's roof faces summed by address, over the register's floor area, banded and fitted on the heating part | assembly and modelling: an address join across two registers' spellings, a log line on the heating part | keep |
| this year's owners choosing their measure on those properties (strongly in 2026; in 2019 controls only slightly, insulation not at all) | constructed (each owner's choice leans on the building's empty week and roof, its use's shares kept) | no: every 2019 answer and every 2026 application is a choice; the 2019 answers sit within 0.05 of the offered buildings of their use on the empty week and within 12 per cent on the roof (asserted) | only by measuring the properties | none beyond R3 and R4 | keep: the process that makes the transport matter |
| hotels and care homes lived in round the clock, their electricity dipping at night and between meals | constructed (an activity curve per use: breakfast and dinner peaks in a hotel, meals in a care home) | no: every hotel and care home, in every round; conference houses and day-care centres among them close at weekends | the use on the register and domain knowledge (guests and residents there at night), borne out by the pilot's hotels and care homes sitting under the curve | measurement: every hotel and care home held lived in round the clock (its use on the register); read off the load alone a hotel looks over half the week empty and controls come to 114.12, the same call on a figure outside its band | keep: the measurement's own step, moving controls' figures, not the call |
| heating optimisation's saving falling back as heating curves are turned up | constructed | no: every heating optimisation works building | one plot of the seasons | modelling: the level it settles at | keep, earned by a careful run |
| the service team's burner checks | constructed | no: both arms alike (70.9 and 69.9 per cent) | a read reason in the meter file | none for the comparison | keep, texture |
| late insulation answers larger and more often withdrawn | constructed | no: every measure's answers carry a size and a withdrawal record | a targeted query on the 2019 responses | modelling: count, size and withdrawal projected measure by measure | keep |
| extensions and empty floors | constructed | no: across the stock, both arms | the floor area on the notices | none | keep, texture |
| fewer roofers taking council work in 2026 (12 of the 26 who did the 2019 roofs), each at its own pace | constructed (the firms, their paces, who still trades) | no: every firm of both trades has a pace and a 2019 record; the heating firms (27 of 30) fit this year's work in full | a query across two files (the quotes' contractors, 2019 and 2026) and modelling: each firm's pace off its completion dates, its jobs queued to 30 September | modelling: a capacity in the unit the work takes, a queue, the late applications shared | keep: one of two judgments the call needs |
| this year's insulation roofs larger (1,121 square metres on average against 802) | constructed (the same choice on the roof that drives R4) | no: every insulation application | the cadastre's roofs, or the quotes, against the 2019 works' | none beyond R8c | keep: what makes job counts mislead |
| a roofer's 2019 jobs taking it longer the larger the roof | constructed (a pace in square metres) | no: every 2019 roof (median correlation 0.85 within firms, rain days, late starts and each roof's own pace around it) | the completion dates against the roofs | none: it rules the jobs reading out | keep, evidence |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 each measure's saving by season | Missed | Right | Right |
| R2 heating optimisation's saving over its life | Missed | Right | Right |
| R3 controls along the empty week | Missed | Missed | Right |
| R4 insulation along the roof per floor | Missed | Missed | Right |
| R5a insulation's saving rate on this year's applications | Missed | Missed | Right |
| R5b heating optimisation's saving rate on this year's applications | Missed | Right | Right |
| R5c heating controls's saving rate on this year's applications | Missed | Missed | Right |
| R6 the funded set at the limit | Partly | Missed | Right |
| R7 each range and flip rate | Missed | Partly | Right |
| R8a each measure's round at close | Missed | Right | Right |
| R8c what each measure's round pays once the works are done | Missed | Partly | Right |
| R11 how many of each measure's applications are paid | Partly | Partly | Right |
| R8b the funded round's grant asked and paid | Missed | Missed | Right |
| R9 every application's lifetime tonnes | Missed | Partly | Right |
| R10 the pilot's 2025/26 CO2 | Missed | Right | Right |
| Roughly | 1 of 15 | 7 of 15 | 15 of 15 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (each pass computed end to end by checks.effort on the cut pack; the careful pass calibrated to the platform runs on architectures 7 and 8: the lottery, each use's saving, the fade and the round's count and grant at close right, every job paid at 2019's completion rate; two cells hand-graded with reasons)
Largest single hint: "this year's owners chose the measure that suits their building, so price controls along the share of the week each building stands empty, from its load profile, and roof insulation along its roof per floor, from the cadastre and the register"; rescues 5 of 15 results
Pair estimate: 46.0

## Data provenance

Source: generated by task7/generator (world.py simulates the utility's commercial customers, each building's week, storeys and electricity, the weather station, the benchmarking notices, the 2019 lottery, the service team's visits and the 2026 offer; pack.py writes each system's export, the meter operator's typical weeks and the state's solar cadastre among them; docs.py the council's and the utility's documents)
Behaves like the real thing: buildings carry their own level and envelope, a slow drift and season noise, weather through degree days on the type's hot-water share, the pandemic winters and the 2022 price shock by use, extensions and empty floors, burner checks of uneven effect, a week of their own whose electricity follows it (a base load that never stops, opening and closing hours lit in part, holidays on their weekdays, a night dip where people live), roofs set by storeys and pitch, quotes priced on the roof or the floor and answer dates driven by job size; owners choose their measure on their building's use and, once informed, on what suits it; each quote comes from a roofer or a heating firm, the larger firms quoting more often, and each firm works through its granted jobs in the order its owners answered, a roofer at its own pace in square metres of roof a working day, a heating firm with its own fitters (the 2019 roofs all done by 20 September, rain days and late starts among them; this year under half the roofers still quote)
Genuine patterns: (1) degree-day weather response with use-specific hot-water shares (2) a slow building drift and season noise (3) the pandemic winters and the price shock, different by use (4) each measure's saving varying building by building along its driver and fading for the operational measures (5) electricity load following each building's week, shaped through the day (lunch, a restaurant's afternoon lull, shift breaks), with part-staffed Saturdays, outdoor lighting at night, holidays, and night and midday dips where people live (6) answer timing and quote size scaling with the job (7) uneven burner-check effects (8) each firm's completions spaced by its jobs' size at its own pace, the larger firms quoting more
Problems by process: periodic reads taken days off 30 April, meter exchanges, counter rollovers, estimates later corrected, customer typos, re-imported rows, meters counting tens of cubic metres, the 2017 gas-quality change in one network area, second meter points, connections and disconnections, revised applications sent twice, a contractor typed without its legal form, second market locations per customer, a meter exchanged mid-2025, roof faces per address with outbuildings and an abbreviated street spelling
Breadth: 24,000 buildings and 25,900 gas meter points over thirteen seasons, 389,000 reads, 178,500 hourly typical-day rows for 25,500 market locations, 46,900 roof faces, 37,000 notices, 3,040 pilot answers across six uses and three measures, 829 applications, 56 contractors; choosing which comparison, which seasons, which property, which file and which buildings carry each result is the work

## Template check

Chain signature: causal reasoning, forecasting, missingness-measurement, modeling, causal reasoning, synthesis, uncertainty, forecasting, forecasting, forecasting, synthesis, synthesis, synthesis
Question form: which (a pick of measures under a limit and a budget), with what the round asks and pays beside it
Nearest build: task7 v7 (the same world, its transport by the notice's use, which a frontier run made unprompted; here two properties measured from records at another grain, the applicants having chosen on them); task2 (one transport step deciding a tier); task6 (a hard-to-measure quantity in another field); no build on file measures a unit's property from a second record at another grain to carry a randomised effect

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "saving" in a season | the share of the gas the works buildings would have used (aggregate); the average building's share | aggregate | plan 4.2 ("the gas its works save, as a share of the gas the buildings that had them would have used") |
| SF2 | the average of building shares | equal-weight against gas-weight | gas-weight | plan 4.2; over half a point apart on some measure, asserted |
| SF3 | "the buildings that had them" | the works buildings; the draw's effect scaled by the drawn owners' share with works; every drawn owner counted as treated | the works buildings | the scaled draw within a point of the golden every season (asserted); every drawn owner as treated is the offer's effect, which plan 4.2's "the buildings that had them" rules out (it dilutes every saving, asserted) |
| SF4 | a building's use | its 2019 notice; the 2026 register | the 2019 notice | same call, asserted |
| SF5 | the baseline and the comparison | the 2018/19 season, every passed-over owner of the measure; two seasons; the comparison taken use by use | 2018/19, the measure's passed-over owners | inside R1's band, asserted |
| SF6 | the saving after the seventh season | the fitted level; the last season or the last three carried; flat; the first season; an exponential fall to nothing; a line | the fitted level | the last seasons in the band; flat and the first season outside (asserted); the exponential and the line ruled out by the seasons' levelling (asserted) |
| SF7 | carrying each measure's saving to an application | the driver's bands fitted (six bands); four or eight bands; the bands as steps; a straight line through the bands of buildings that close; the last seasons carried; a two-season baseline | six bands fitted | inside R5 and R6's bands, same set, asserted |
| SF8 | the 90 per cent range | resampling buildings within use and arm, every step repeated, two seeds | the first seed | within 4 per cent at both ends, asserted |
| SF9 | withdrawals | early and late rates by measure; one rate by measure | early and late | inside R8a's band, asserted |
| SF10 | the 2025/26 saving | the measure's 2025/26 saving on each works building's use; each use's own | the measure's | inside R10's band, asserted |
| SF11 | reads off 30 April | shared by degree-day weight; counted whole to the nearer season | shared (method 1) | same call, insulation and controls within 5 per cent, asserted; heating optimisation's small late savings move most and it stays over the limit |
| SF12 | estimates without a correction | kept; dropped | kept (method 1) | same call, asserted |
| SF13 | normal weather | the method's normalisation; raw use | normalised (plan 4.3) | same call, asserted |
| SF14 | a revised application | the later replaces the earlier; both kept | the later (2026 terms 2) | same call, asserted |
| SF15 | "what would be paid once the works are done" | net of withdrawals; net of withdrawals and works not completed (terms 4) | both | converge: every drawn 2019 owner either withdrew or completed, asserted |
| SF16 | a building's empty hours | its load under half-way from the week's lowest hour to its highest, none where the load never falls below three quarters of its highest hour; at 40 or 60 per cent of the way | half-way | inside R3's band, same call, asserted |
| SF17 | who is lived in round the clock | every hotel and care home (its use on the register); a hotel or care home whose weekend days (8:00 to 20:00) run 0 to 15 per cent above its weekend nights (0:00 to 5:00); one whose every weekend day hour runs above every night hour; nobody (each read off its load) | every hotel and care home | the weekend test at every margin from 0 to 15 per cent and every weekend day hour above every night hour inside R3's, R5's and R6's bands, same call (asserted); nobody, the load alone, keeps controls under the limit at 113.59 and R3 outside its band, ruled out by the pilot's hotels and care homes, which read over half the week empty and saved 1.46 per cent where the curve gives them 4 or more (asserted) |
| SF18 | the form of controls' rise | a threshold and a straight rise; a straight line through the bands of buildings that close; a straight line through the lived-in band too | threshold and rise | the line through the closing bands inside the band (asserted); the line through the lived-in band fits the bands six times as badly (weighted squared error, asserted) and lands at 119.43, at the limit, so it is ruled out by its misfit rather than by its side of the line |
| SF19 | insulation's saving and the hot water | on the heating part, each application's use's hot-water share untouched; on its share of the gas | the heating part (plan 4.1: insulation of the roof or the top-floor ceiling; method 3's hot-water shares) | same call, inside the band, asserted |
| SF20 | a roof's area | every face at the address; a garage or shed beside a main roof left out | every face | same call, insulation within 5 per cent, asserted |
| SF21 | the applications the €120 test is taken on | the applications received by 12 June; the round's applications projected to 30 June | received by 12 June | the committee's request ("We set the round on the applications that came in by 12 June") |
| SF22 | the budget's order | from the lowest grant per tonne up, a measure where the budget still covers what its applications will be paid; anything else | that order | the committee's request |
| SF23 | when the 2026 works start | 13 July, the Monday after the 9 July meeting; 20 July | 13 July | R8c's band and the call (the pair under 80 per cent of the budget from 20 July, asserted) |
| SF24 | a roofer's pace | its pilot roofs' square metres (the cadastre) over the working days from 15 July 2019 to its last completion; each roof read off its quote; jobs a working day | the cadastre's square metres | the quote-read roofs inside R8c's band, same call (asserted); jobs ruled out by the 2019 record, in which a roof took a firm longer the larger it was (median correlation 0.85 within firms, asserted) |
| SF25 | the late applications' firms | each firm's share of the received ones; each firm's share of the firms' pace | the received share | the pace share inside R8c's band, same call (asserted) |
| SF26 | one queue or each firm's own | each firm's own; the firms' work summed into one queue | each firm's own | the one queue inside R8c's band, same call (asserted) |
| SF27 | the late roofs' size | the received roofs times the 2019 late answers' roof ratio; times their grant ratio | the roof ratio | the grant ratio inside R8c's band, same call (asserted) |
| SF28 | a contractor named with or without its legal form | the same firm; two firms | the same firm | the name with its legal form dropped is the only difference (pack, asserted by the verifier's match) |

## Closure table

| # | Axis | Reading | Move |
|---|---|---|---|
| 1 | Population | the pilot's works buildings and passed-over owners by measure; the applications received by 12 June for the €120 test; the round's applications to 30 June for what it pays | filed: rules 3, terms 1 to 3, the committee's request (SF21), the prompt |
| 2 | Unit of account | the building (an application is a building and a measure; its week and its roof are the building's) | filed: plan 4.4, terms 2 |
| 3 | Attribution window | the season, 1 May to 30 April; the week of 2025 for the electricity | filed: plan 4.3; the profiles' own year |
| 4 | As-of dating | the applications received by 12 June; the 2019 answers' own dates; the profiles of 2025 and the cadastre's 2023 flight | the request; C1 |
| 5 | Version basis | a revised application replaces the earlier one | filed: terms 2 (SF14) |
| 6 | Denominator | the gas the works buildings would have used | filed: plan 4.2 (SF1) |
| 7 | Weighting | the gas: buildings by their use, bands by their 2018/19 gas, applications by reference consumption | filed: plan 4.2 and 4.4 (SF2); C1 on the bands |
| 8 | Window length | seven seasons observed, the service lives filed | filed: plan 4.4; SF6 |
| 9 | Boundary inclusivity | €120 or less funds; a measure fits where the budget covers what it pays | filed: plan 4.4, the committee's request; no grant per tonne within 8 per cent of the limit, the funded pair 8 per cent or more under the budget |
| 10 | Rounding path | none in the prompt (the author's call, 2026-11-09): every figure stated at its natural precision, percentages to two decimals, grant per tonne to the cent, money to the euro, counts and totals whole, an application's tonnes to a tenth | C1: the bands are wider than any printing choice, asserted |
| 11 | Tie-break | none needed | C1 |
| 12 | Maturity and censoring | the 2026 round open to 30 June; seasons after the seventh unobserved | the prompt and R8a; SF6 |
| 13 | Order of operations | normalise, compare, measure the drivers, fit, carry, weight; the limit, then the budget from the lowest grant per tonne up (SF22) | C1; the committee's request |
| 14 | Row order | export order | C1 |
| 15 | Duplicate resolution | re-imported reads once; a revised application replaces the earlier | C1; SF14 |
| 16 | Identity normalisation | meter points to buildings through the meter list; market locations to buildings through the customer number; roof faces to buildings through the address and postcode, "str." read as "straße"; a contractor with or without its legal form (SF28) | the meter list, the register's customer number and address |
| 17 | Netting against gross | none | C1 |
| 18 | Dimensional units | cubic metres to kWh by z-number and calorific value; kW averaged by hour; square metres of roof over square metres of floor | method 2; the files' own columns |
| 19 | Code and status semantics | read reasons; drawn, withdrawn and completed; weekdays | the files' own columns |
| 20 | Integerisation | applications at close whole, as an estimate | C1 |
| 21 | Clause scope | plan 4.4 for each measure in the round | filed |
| 22 | Forward window contents | the applications still to come, from the 2019 answers' timing, sizes and withdrawals; the works to 30 September, from the 2019 completions by firm | R8a, R8c, the 2019 responses ship with contractors and completion dates |

## Literal reader

Executed word for word, plan 4.2 and 4.3 with the pilot rules give each season's saving as a share of the gas the works buildings would have used against the owners the draw passed over (R1); plan 4.4 asks for each application's saving in the building applied for over the measure's life and the round's saving rate as a share of the tonnes its reference consumption carries (R2 to R6, R9); 4.6 gives the 2025/26 saving (R10); the 2026 terms give the round at close and what is paid, nothing on works not completed by 30 September (R8a, R8c, R11, R8b); the committee's request gives the €120 test's basis (the applications that came in by 12 June) and the budget with its order (R6). The pilot's response file carries each answer's contractor and completion date, the 2026 applications each quote's contractor; no sentence says the firms are fewer, the roofs larger or that a firm's work is measured in square metres. No sentence names the comparison, the persistence, the drivers, the load profiles, the cadastre or the projection, and the readings a literal reader can take are the fork table's, each asserted. "In the building applied for" is the plan's own phrase from architecture 7, unchanged; it pins where the saving is taken, not how.

Leak rulings (leak.py, 2026-11-09, --asof 2026-06-24, REVIEW, no LEAK): the call's words (insulation and heating
controls) in the plan, the 2019 rules and the 2026 terms are the measures' names, which every governing document
must carry; the design-note vocabulary hits (building, insulation, controls, heating, carried, optimisation, record,
nothing, seasons, method, points, owners) are the field's ordinary words, and no sentence names a comparison, a fade,
a driver, a load profile, a roof or a projection; the prompt carries no rounding sentence at the author's word
(closure axis 10); no date after the setting. After the level-up (2026-11-10): the budget's €8.2 million in the
committee's request is a filed input the golden quotes, not an answer; the new stump terms in the governing documents
(square metres, September, owners, completion) are the field's ordinary words, and no sentence says the firms are
fewer, the roofs larger or that a firm's work is measured in square metres.

## Prompt contract

May not drop or change: the question (which measures, under €120 of grant per lifetime tonne of CO2 and the council's budget for the round); for each measure its saving in the pilot's works buildings in each season since the works, its saving rate on the applications received so far, their grant per tonne with a 90 per cent range and the saving rate at which the answer would flip, and how many applications it will have once the offer closes, the grant they ask for, and how many of them would be paid and for how much once the works are done, with the funded round's totals; every application received so far with its grant and lifetime tonnes; the pilot's 2025/26 CO2; a short note with the answer first and a workbook. The prompt carries no rounding sentence at the author's word; the answer blocks and the golden state every figure at its natural precision. Must never add: a method (a comparison, a fade, a driver, a load profile, a roof, a split by use, a projection, a contractor, a pace, a capacity, a deadline), a warning, an attached file's name, a role, the budget's figure or a count the data hold.

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
