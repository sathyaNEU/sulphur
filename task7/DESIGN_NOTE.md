# task7: which of Cottonwood Draw Electric Cooperative's 2027 load-management proposals earn their cost at the wholesale peak

## Draw

Subdomain: Energy Systems & Utilities, Energy efficiency & demand response evaluation (`energy-systems-utilities`, `tariff-demand-response-evaluation`)
Analysis type: Experiment & Causal Analysis (assigned; the platform task 2d026b3c-65e4-403c-9a40-4bccaac5c1f0 keeps its type). The design is a randomised dispatch trial (which paging groups shed on which of 60 hot weekdays was drawn by lot) and the effects wanted are the trial's own: what a shed command causes at the feeder, and what each of six proposals would cause in 2027.
Answer shape: scenarios with the flip point (six proposals, each with the coincident-peak kW it adds and the break-even kW it has to clear, on top of the three shares the proposals rest on and the bridge from the kW the fleet could shed to the kW it does)
Weight: attribution, because every kW the fleet fails to deliver has to be assigned to one of three causes (the page never arrived, the switch is dead, the switch is no longer wired) from pooled feeder steps, and each proposal repairs only one cause; the last three builds leaned on a hard-to-measure quantity (task1), modeling (task9) and synthesis (task26)
Data-native sentence: the cooperative's switches are one-way and its members' meters are read once a month, so a shed command leaves no record at any premise; all that exists is the step each paging group's command makes in each feeder's SCADA load, and the three reasons a switch stays silent are tangled across the fleet (the oldest switches sit nearest the cooperative's own transmitters and at the premises that have since replaced their air conditioners).
People: Peter Mitchell (energy services manager, whose workbook and slides the golden are), Timothy Powell (operations superintendent, radio shop and SCADA), Caleb Mclean (member services, the switch register), Emily Maldonado (finance, the work plan's appraisal constants) (`guard.py names --geo "United States, Kansas" --seed 713`). None appears in the prompt.
Deliverables: a CSV (one row per proposal), a workbook (first sheet states the call) and a few slides. No written document.
Guard (card registered 2026-11-25T19:35Z, WARN only): forum board_of_directors (the cooperative's board adopts the work plan), forcing event vote_or_meeting, org family cooperative_or_member_body, role programme_officer, calibration pilot_log, artifact register, strategy causal_design, shape 13, answer shape scenarios-flip, weight attribution; the first generator was redrawn from G3 to G9 (the register counts what was installed, the delivery is what survives downstream), which is the honester label and cleared `ban.pattern` against task26. The house WARNs are answered in `## Frontier check`, `Noun swap:`.

Architecture 13, 2026-11-25, a new world on the author's word after the slot was un-retired. The reviewer's "How to fix it" of 2026-11-11 was read against the closed page before anything was drawn: design-clustered ranges (the clustered-interval card), controls carried through round-the-clock hotels (transport and range), the cadastre's attenuation (the noisy-regressor card), the 2022 price shock and burner checks in the passed-over arm (a co-occurring change), completion capacity as a forecast (the same hidden factor) are all closed cards or the returned factor, and architecture 9 already built two of them and was landed by reflex. None is used. What the review asked for underneath them is kept: the call rests on causal estimates, several judgments each move it, and no single fact makes the rest routine.

## Stump screen

Written on 2026-11-25 before the card and before `generator/core.py` (`references/stump-screen.md`). Test 0, the world: the estimand is the kW each proposal adds at the 2027 coincident peaks for the enrolled fleet as it stands; no shipped meter, monitor or account observes a switch's delivery (members' meters are monthly, the switches cannot report, the study homes hold none of the three conditions), the feeder SCADA observes only the pool, and the lever (which groups were paged) with the pooled outcome prices a group's total, never why its switches are silent or what a repair would restore. Eight candidates, each through the twenty tests.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| S1 a shed command sent is not a command received: a one-way switch hears its page less often the farther it sits from a transmitter of its own paging system that was on the air that day | "every enrolled premise is inside the coverage map" (N09 today's structure for all history, N27 a second record at another grain set aside, L38 a record carrying the modifier set aside, L70) | the transmitter register and the radio shop's hand-kept outage log against the feeder steps: feeders served by a transmitter that went off the air lose most of that group's step on those days and no others | none | kept |
| S2 a switch that passed its last test is not a switch that works now: the share still shedding falls with the install batch's age | "the annual test log shows 96 in 100 pass" (N11 a passed test taken to certify the unit, N46 delivery priced at full, N35 unit-level rates pooled) | the paging groups are install batches, each shed at its own minute, so each batch's own steps show what its switches deliver against what a working switch takes off in the study homes | none | kept |
| S3 the premise on the register is not the equipment the switch was wired to: where the air conditioner was replaced after the switch went in, most switches were left unwired | "the work orders found 9 in 100 unwired" (N14 a second record set aside, L56 a signal kept as a sensitivity, L58 two tangled conditions read one at a time, N36 rival explanations named and left untested) | the rebate register and the county's mechanical permits, dated against each switch's install date, against the steps of feeders with many and few such premises | none | kept |
| the fleet's level read off the 380 interval-metered study homes | "the metered homes stand for the fleet" | the feeder steps summed | 2 (a pooled total on the steps is one regression the runs make, R102), 14 (said out loud it is one step) | not kept: the level is reflex work and goes to the Step-by-Step |
| single against repeated pages, the reception level from the two arms together | "neither arm is unbiased" (N40) | the dispatch log's page counts | 9 and 13 (prototyped: every proposal's figure is a difference of delivered kW that needs no reception level, so the identity moves no member) | not kept |
| the working share by a mixture on unit-level responses | a threshold in place of a model (L57) | interval data per member | 0 (it needs interval meters at the members, which hand every correction to a unit-level regression), 11 (the mixture's spread across forms ran to the margin) | not kept |
| the snap-back landing in a coincident-peak hour after the window | "the event covers the peak" | the wholesale invoices' peak hours | 1 (the payback card) | not kept: a supporting line in the Step-by-Step only |
| switches on a feeder as of each event day after switching | today's feeder map for the whole summer (N09) | the switching log | 2 (R38: the runs replay a switching log unprompted), 4 (a re-key) | not kept: Layer 1 |

Kept: S1, S2 and S3, on three axes (what the stored command measures, when the stored test was true, who the registered premise is), three records (the transmitter files, the install batches, the rebate and permit files) and three members (a repeater, a find-and-fix round, a reconnection round), with three more proposals that only an over-correction funds. The three share one instrument, the feeder steps, and the note says so wherever it matters (`One-fact test:`, `Decisive steps:`).

## Deep reasoning

Task type: tariff demand response evaluation (`tariff-demand-response-evaluation`, the client's Energy efficiency & demand response evaluation, which serves Experiment & Causal Analysis): the impact evaluation of a direct load control programme from a randomised dispatch trial, with the proposals priced at the wholesale coincident peak.
Domain test: the results are the quantities a demand response evaluator estimates: the load reduction a dispatch causes at the feeder, the realisation rate of a one-way switch fleet split by cause (paging reception, switch failure, disconnection), and the coincident-peak kW a programme change adds against a wholesale demand charge; the evaluator reads them from load steps at command times because one-way load control leaves no acknowledgement.
Swap: "which marketing proposals are worth funding when coupons cannot report back" keeps the words and loses the analysis: there is no paging reach to a transmitter that was on the air, no feeder whose load steps at the minute a group is shed, no install batch that is also the address a command goes to, and no demand charge on the cooperative's load in the supplier's peak hour to price a repeater against.
Where the weight sits: R4 and R5, the attribution: 21,896 feeder steps have to be apportioned among switches by reach, batch and replaced unit in one fit, with the reach rebuilt per event day from two paging systems' transmitters and their off-air dates; it is long because every covariate is built from a different file at a different grain, not because any one idea is clever.
Layer 1: the SCADA historian freezes values through communication dropouts and two feeders were renamed after the Pruett substation rebuild; the paging encoder logs retried pages and local time while SCADA is UTC; the 2021 billing conversion re-keyed premise numbers in the switch register; the radio shop's outage log is typed by hand with site nicknames; rebates carry premise numbers and the county's permits only addresses; the monthly reads sit on billing cycles. Each is cleaned the same way by every careful run and none moves a graded figure outside its band.
Not one thing: the strongest single piece is the reach covariate (S1). A run that builds it perfectly and reads the other two records at face value still files the wrong set (it funds the repeater and neither round it should, corelib's `S1 fixed alone` earns 16 of 100), still misses R2, R3, the bridge and five of the six proposal figures.
One-fact test: "a one-way switch far from an on-air transmitter of its own paging system misses most of its pages" rescues R1 and the two repeater figures of R5, 2 of 7 results (agrees with the Effort test's Largest single hint). The sentence that names what the three stumps share, "apportion the feeder steps among the switches by reach, batch and replaced unit", names a method the data force and leaves every construction to do (the per-event reach from three files, the batch term against the study homes' working level, the replaced-unit flag from two registers); handed to the reflex route it rescues nothing until each covariate is built.
Not semantics: with every field, unit and clause read correctly (the proposals' scopes, the appraisal's value per kW, the index the plan appraises at) the reflex route still funds none of the six, because the three shares are estimates and no field holds them.
Not rule application: the work plan files what a proposal is, what it costs a year, the value of a kW and the conditions it is appraised at; nothing filed says how many pages arrive, how many switches work or how many are wired, and no procedure turns the steps into those shares.
Estimand: the 2027 work plan's appraisal page (`work_plan_2027_load_management.docx`, "Appraisal") files the population (the enrolled air-conditioner switches on the register at 30 September 2026), the outcome (kW of load reduction during a shed, at the supplier's cooling index of the four 2026 coincident-peak afternoons, 1.15), the window (the 2027 summer, every listed transmitter on the air), the unit (kW per proposal) and the comparison (each proposal against present practice, on its own); each proposal's scope is filed with it (the premises a visit round covers, the site a transmitter proposal adds).
No decoy: nothing is written to carry a wrong answer. The carrier's coverage map, the annual test log and the service work orders are honest records of shallower quantities (where a signal can be received outdoors on a test set, whether a switch clicked on the bench signal the day it was tested, what a technician happened to find on a visit made for another reason). Last year's load-management report multiplies the register by the programme's planning figure of 1.0 kW a switch; it reproduces exactly by its own stated method and Ask 2 prices it on the golden's footing (the kW the fleet could shed against the kW it does).
No replay: no result re-derives a published figure and no stated number is wrong.
Pinned: 15 rebuilds of the golden's conventions (reach bands, weighting, the district term, the batch term's form, halves of the event days, the study homes' responder cut, trimmed steps, the index origin) keep the funded set; each figure's band is what they span, with room (`generator/core.py`, the figure table). The rivals a strong run would take (the study homes carried to the fleet, the nearest listed transmitter of either system, threshold cuts) are each ruled out by the three-slice check in `Referee:`.
Run forecast: R1 lost by a method shortcut (the nearest listed transmitter, or the coverage map) and dismissed own evidence (the off-air days seen and left); R2 by a self-confirming check (the test log agrees with the study homes, which are all young switches); R3 by stopping at the first story (old switches are failing) and reading the two conditions one at a time; R4 and R5 by an unfinished chain (a level without its split); R6 and R7 follow.
Strategy label: own (a randomised dispatch whose receipt no record holds, apportioned from pooled feeder steps); UNTESTED in `references/sulfur-strategies.md`.
Depth level: 5 on the client's scale: three independent judgments, each estimated, each flipping a different proposal; the three single drops file three different wrong sets and the lattice seven; the set holds across 15 variants.
Lesson: when an intervention's receipt is never recorded, the effect of repairing it is identified only by apportioning the pooled outcome among the conditions that block receipt, each built from its own record; no build on file teaches noncompliance split by cause from a pool.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the share of shed commands lost at switches more than 20 km from an on-air transmitter of their own paging system, against switches within 8 km: 83 in 100 | causal reasoning | the feeder steps on the days a transmitter was off the air or not yet commissioned; the receiver and system fields | 78 to 87 in 100 | method shortcut: the nearest listed transmitter of either system, or the coverage map, gives no loss; dismissed own evidence where the off-air days are seen and left as noise | independent: the transmitter register, the outage log and the steps | Component 1 |
| R2 | the share of switches installed through 2015, at premises with no replaced unit, that no longer shed: 33 in 100 | modeling | each install batch's own steps against the working level of the study homes' responders | 30 to 36 in 100 | self-confirming check: the test log's 4 in 100 agrees with the study homes, whose switches are all six or seven years old | independent: the install batches, the study homes and the steps | Component 2 |
| R3 | the share of switches left unwired where the air conditioner was replaced after the switch went in: 68 in 100 | missingness and measurement | the rebate register and the permits dated against install dates, against feeders with many and few such premises | 65 to 70 in 100 | stopped at the first story: old switches fail, with the replaced units read as part of age or one condition at a time; the work orders' 9 in 100 kept as the figure | independent: the rebate and permit records and the steps | Component 3 |
| R4 | the bridge from the 10,998 kW the fleet could shed to the 5,200 kW it does: 1,775 lost to missed commands, 2,396 to failed switches, 1,627 to unwired switches | decomposition and attribution | the appraisal page's order (a switch counts against the first step that stops it: page, hardware, wiring) and R1 to R3 | 1,527 to 2,018; 2,056 to 2,824; 1,529 to 1,721 | unfinished chain: the delivered total found on the steps and the shortfall left unsplit or split by the three records at face value | R1, R2, R3 | Ask 2 |
| R5 | the coincident-peak kW each proposal adds in 2027: Kettle Ridge repeater 250, Halverson fill-in 185, Larkin find-and-fix 505, Medora Flats find-and-fix 264, reconnection within 14 km 1,402, outlying reconnection 224 | forecasting | the appraisal page (index 1.15, every listed transmitter on the air, each proposal alone) and R1 to R3 | 236 to 261; 151 to 202; 451 to 572; 208 to 324; 1,321 to 1,484; 195 to 253 | unfinished chain and dismissed own evidence: each proposal priced from the record that describes it (the map, the test log, the work orders) | R1, R2, R3 | Ask 1 |
| R6 | the funded plan: 2,158 kW added for USD 39.7 a kW-year | synthesis | the appraisal's value of USD 88 a kW-year and the filed annual costs | 2,094 to 2,227; 38.5 to 40.9 | unfinished chain: whatever set R5 gave | R5 | Ask 3 |
| R7 | the proposals funded: the Kettle Ridge repeater, the Larkin find-and-fix round and the reconnection round within 14 km; not the Halverson fill-in, the Medora Flats round or the outlying reconnection round | synthesis | each proposal's kW against its break-even (185, 280, 280, 401, 509 and 345 kW) | exact set | stopped at the first story: no proposal clears on the records at face value | R5, R6 | Recommendation |

Carry-forward: each stump owns one figure (S1 owns R1, S2 owns R2, S3 owns R3: the three critical components, each falling with its own stump alone). Every other graded figure sits downstream of two or three: the Kettle Ridge figure falls with S1, S2 and S3, the Halverson figure with S1 and S3, the Larkin figure with S2, the Medora Flats figure with S1 and S2, the reconnection figure within 14 km with S2 and S3, the outlying one with all three, the bridge with all three, the plan's kW with all three and its cost per kW with S2 and S3 (corelib's figure table). Counts every route reaches (11,923 switches, 21,896 steps, 380 study homes, the premises in each round) are stated only in the Step-by-Step.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| pages missed with distance to an on-air transmitter of the switch's own system | constructed (the generator simulates one-way paging reception) | no: it runs across all 11,923 switches and all 46 feeders, from nothing against the nearest band to 83 in 100 at the fringe, and it decides nothing in the Larkin district where every switch is near | modelling (no unit-level outcome exists; it shows only once the steps are regressed on a reach built per event day from three files) | modelling (a fitted reception curve carried to each proposal's premises) | keep |
| switches failed with the install batch's age | constructed (a hardware survival curve) | no: every batch from 2004 to 2025 carries it, including the batches no proposal touches | modelling (each batch's steps against the study homes' working level) | modelling | keep |
| switches unwired at replaced air conditioners | constructed (installers leave about seven in ten unwired) | no: 4,506 flagged premises across all four districts | modelling (a pooled fit with a flag built from two registers and dated against installs) | modelling | keep |
| the oldest switches sit nearest the cooperative's transmitters and at the premises with replaced units | constructed by the enrolment history (the programme began in town) | no | modelling | modelling (the joint fit) | keep |

No factor sits only in the deciding units, none shows in one cross-tab or plot of one file (no file holds a unit's delivery), and none is fixed by a filter, a split or one extra term on fields the pack names: each needs its covariate built and the pool apportioned.

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 share of commands lost at the fringe | Missed | Missed | Right |
| R2 share of pre-2016 switches that no longer shed | Missed | Missed | Right |
| R3 share of switches unwired at replaced units | Missed | Missed | Right |
| R4 the bridge from the kW the fleet could shed to the kW it does | Missed | Partly | Right |
| R5 the kW each proposal adds | Missed | Missed | Right |
| R6 the funded plan's kW and cost per kW | Missed | Missed | Right |
| R7 the proposals funded | Missed | Missed | Right |
| Roughly | 0 of 7 | 0.5 of 7 | 7 of 7 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the build writes it at stage 3; at design the table is the reflex route of `generator/core.py`, which earns 9 of 100)
Largest single hint: a one-way switch far from an on-air transmitter of its own paging system misses most of its pages; rescues 2 of 7 results
Pair estimate: 9 (the reflex route on corelib's rubric; a run that loses any one stump earns 28 to 40, the generous run route 21)

Clean-data test: with every file complete, de-duplicated, re-keyed and on one clock, the reflex route is a reasonable analysis: the randomised sheds measured on the interval-metered study homes with a placebo and a clustered interval (0.73 kW a switch), the fleet's delivered total found on the feeder steps, and each proposal priced from the record that describes it. It funds none of the six. What separates it from the golden is three estimates, never a repair or a reading.
Effort ladder: ten minutes multiplies the register by the planning figure and funds nothing or everything; an afternoon finds the delivered total on the steps and the shortfall, and still prices the proposals from the map, the test log and the work orders; two days builds the three covariates and apportions the steps.

## Stump core

Every figure below is printed by `generator/core.py` (seed 713), which ends on `corelib.run(spec)`: `CORE PASS level 5  task7 architecture 13`, 30 rows PASS, none WARN or FAIL.

| Member | Line | Golden | Family spread | Reflex route | Direct | Rigorous | Opened by |
|---|---|---|---|---|---|---|---|
| fix_t (Larkin find-and-fix round) | 279.736 | 504.8 | 47.1 | 58.22 | 58.22 | 134.5 | S2 |
| fix_w (Medora Flats find-and-fix round) | 400.827 | 264.4 | 40.5 | 45.82 | 45.82 | 105.8 | forced |
| recon_in (reconnection round within 14 km) | 508.612 | 1402 | 54.6 | 260.4 | 260.4 | 0 | S3 |
| recon_out (outlying reconnection round) | 344.949 | 224 | 19.5 | 98.74 | 98.74 | 0 | forced |
| rep_n (Halverson carrier fill-in) | 279.545 | 184.5 | 25.3 | 0 | 0 | 0 | forced |
| rep_w (Kettle Ridge VHF repeater) | 185.227 | 250.3 | 10.4 | 0 | 0 | 0 | S1 |

| Run route | Call | fix_t | fix_w | recon_in | recon_out | rep_n | rep_w |
|---|---|---|---|---|---|---|---|
| calibrated | wrong | 134.5 | 105.8 | 0 | 0 | 0 | 0 |
| cutoff | wrong | 867 | 570.9 | 2225 | 0 | 26.75 | 0 |
| generous | wrong | 590.9 | 555.6 | 1303 | 24.7 | 38.82 | 6.708 |
| hedge | wrong | 58.22 | 45.82 | 260.4 | 98.74 | 0 | 0 |

| Figure | Block | Golden | Band | S1 lost | S2 lost | S3 lost | Reflex route |
|---|---|---|---|---|---|---|---|
| C1 fringe commands lost | components | 0.8341 | 0.7833 to 0.8733 | moves | - | - | lost |
| C2 pre-2016 switches failed | components | 0.3296 | 0.3046 to 0.3599 | - | moves | - | lost |
| C3 switches unwired at replaced units | components | 0.6759 | 0.6502 to 0.7012 | - | - | moves | lost |
| A1 rep_w | asks | 250.3 | 235.7 to 261.1 | flips | moves | moves | lost |
| A1 rep_n | asks | 184.5 | 150.7 to 202.4 | moves | - | moves | lost |
| A1 fix_t | asks | 504.8 | 451.4 to 572 | - | flips | - | lost |
| A1 fix_w | asks | 264.4 | 207.5 to 324.3 | moves | moves | - | lost |
| A1 recon_in | asks | 1402 | 1321 to 1484 | - | moves | flips | lost |
| A1 recon_out | asks | 224 | 195.3 to 253.1 | flips | moves | moves | lost |
| A2 kW lost to missed commands | asks | 1775 | 1527 to 2018 | moves | - | - | lost |
| A2 kW lost to failed switches | asks | 2396 | 2056 to 2824 | - | moves | - | lost |
| A2 kW lost to unwired switches | asks | 1627 | 1529 to 1721 | moves | moves | moves | lost |
| A3 kW the funded plan adds | asks | 2158 | 2094 to 2227 | moves | moves | moves | lost |
| A3 funded plan cost per kW | asks | 39.71 | 38.45 to 40.9 | - | moves | moves | lost |

| Route | Call | Earns on the rubric |
|---|---|---|
| golden | right | 100 |
| S1 lost alone | wrong | 40 |
| S2 lost alone | wrong | 28 |
| S3 lost alone | wrong | 34 |
| S1 fixed alone | wrong | 16 |
| S2 fixed alone | wrong | 22 |
| S3 fixed alone | wrong | 16 |
| reflex route (every stump lost) | wrong | 9 |
| rigorous standard route | wrong | 9 |
| calibrated run route | wrong | 9 |
| cutoff run route | wrong | 9 |
| generous run route | wrong | 21 |
| hedge run route | wrong | 9 |

Unobserved part: the decision's quantity is the kW each proposal adds at the 2027 coincident peaks, which is the kW the switches it repairs would deliver less the kW they deliver now. No record holds a switch's delivery: the switches are one-way, members' meters are read monthly, and the dispatch log records commands sent. The part no record holds is, for every switch, whether its page arrived, whether its hardware acted and whether it is wired to a running air conditioner.
Instruments: (1) the feeder SCADA steps at each paging group's command (21,896 of them) see the sum of what a group's switches on a feeder deliver and nothing about which or why; read raw as a total they give the delivered 5,200 kW. (2) The 380 interval-metered study homes see unit-level delivery, in town, 1 to 8 km from a transmitter, with 2019-20 switches and no replaced unit: 0.728 kW per enrolled switch and 0.802 kW per responding switch; they are blind to all three conditions and read raw for the fleet they give 9,981 kW delivered. (3) The carrier's coverage map sees where a test set receives outdoors, and says every premise is covered. (4) The annual test log sees a bench signal on the day of the test: 96 in 100 pass. (5) The service work orders see what a technician found on a visit made for another reason: 9 in 100 unwired after a new unit. (6) The transmitter register and the outage log see which transmitters were on the air each day; the switch register sees each switch's receiver, batch and location; the rebate and permit files see replaced units.
Referee: a falsification check on the members' own records, with no file observing any share: predicted against recorded steps on three slices (steps where a transmitter change moved the group's reach band, the four oldest batches, the quarter of feeders with the most replaced units), the largest relative gap. Golden 0.053 (truth 0); S1 lost 0.760, S2 lost 0.608, S3 lost 0.386, pairs 1.11 to 1.34, all three 1.90, the generous route 0.317, the calibrated route 1.87. The study homes are a calibration set for one thing only, what a working switch near a transmitter takes off (0.802 kW); the calibrated route that carries them end to end funds nothing.
Strongest standard route: the randomised comparison on the interval-metered study homes, with a placebo on non-event days and an interval clustered by home, carried to the fleet by the register. It files rep_w 0, fix_t 134.5 and recon_in 0 against lines of 185.2, 279.7 and 508.6: wrong on all three open members. It is refuted by the feeder steps (its delivered total of 9,981 kW against the 5,200 the steps hold) and by the three-slice check (1.87). The strongest route on the steps themselves (the generous route: every named field and the distance to the nearest listed transmitter of either system, fitted jointly) files rep_w 6.7 and fix_w 555.6: wrong on the repeater, and wrong on the Medora Flats round because the reach it mis-assigns loads onto the batch term; it is refuted by the off-air slice (0.317 against 0.053).
Said out loud: S1, "a shed command sent is not a command received: how often a one-way switch hears its page falls with its distance to a transmitter of its own paging system that was on the air that day"; left to do: match each switch's receiver to a system, rebuild the on-air transmitter set for each of 60 event days from the register and the hand-kept log, compute each switch's reach per day, apportion the steps by reach band, and carry the curve to each proposal's premises under the 2027 transmitter set (5 steps). S2, "a switch that passed its last test is not a switch that works now: the share still shedding falls with the age of the install batch"; left: recognise the paging groups as install batches, fit each batch's delivery on its own steps net of reach and replaced units, set it against the study homes' responders, and carry the gap to each find-and-fix round's premises (4 steps). S3, "the premise on the register is not the equipment the switch was wired to: where the air conditioner was replaced after the switch went in, most switches were left unwired"; left: union the rebates and the permits by premise and address, date each against the switch's install, fit the flag in the pool with batch and reach held, and carry it to the reconnection round and out of the find-and-fix rounds (4 steps).
Worth: S1 is worth 250 kW on rep_w, 24.1 times the family's spread there (10.4); S2 447 kW on fix_t, 9.5 times (47.1); S3 1,220 kW on recon_in, 22.3 times (54.6). The bands are the 15 variants' range with a quarter of its width as room each side.
Regimes: second stump, three times: S1 opens the Kettle Ridge repeater, S2 the Larkin find-and-fix round, S3 the reconnection round within 14 km; the Halverson fill-in, the Medora Flats round and the outlying reconnection round are right under the reflex route and wrong only when a judgment is over-corrected (S1 pushed past its fit funds Halverson at 346.9, S2 pushed past funds Medora Flats at 488.7, S3 pushed past funds the outlying round at 399.5).
Sharp: S1: its wrong route passes its own check (every premise is inside the published coverage, and the nearest listed transmitter is near for the western fringe because the carrier's site stands there); the right route needs a commitment (reception as a function of reach to the switch's own system, stood behind by the off-air days); the evidence is in the transmitter register and the outage log; the correction runs from 0 near a transmitter to 83 in 100 at the fringe; its figure is Component 1. S2: the test log agrees with the study homes; the commitment is that a batch's steps net of reach and replaced units measure its working share against the responders' level; the evidence is in the dispatch log's group addresses and the register's install dates; the correction grows with each batch's age and is fitted batch by batch; its figure is Component 2. S3: the work orders agree with nothing being wrong; the commitment is the pooled flag effect with batch held; the evidence is in the rebate and permit files; the correction applies to the 3,267 and 1,239 flagged premises of the two reconnection rounds, spread unevenly over feeders, and is worth less where reach is poor; its figure is Component 3.
Earns: a run that loses S1 alone earns 40, S2 alone 28, S3 alone 34 (50 or under each); the reflex route 9; the rigorous standard route 9; the generous run route 21; S1 fixed alone 16, S2 fixed alone 22, S3 fixed alone 16. The reflex route lands no graded figure. The delivered total (5,200 kW), which the reflex route does reach, is not a stated figure of the asks and sits in the Step-by-Step.

## Stump factorial

Reflex route: every move a run makes unprompted or a file spells out is set right: the SCADA, dispatch and register hygiene (R01), the switching log replayed so each step counts the switches then on the feeder (R38), the step taken five minutes before against five minutes after each command, the study homes' randomised comparison with a placebo and an interval clustered by home (R55, R92), the delivered total found by regressing the steps on the switches dispatched (R102), the appraisal's constants applied as filed. Every stump is read at face value from the cooperative's record. It funds none of the six proposals (rep_w 0, fix_t 58.2, recon_in 260.4), which misses the call; this route is the careful but hurried pass.

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 reception by reach to an on-air transmitter of the switch's own system | stump | the coverage map: every premise covered, no loss | N09, N27, L38, L70 | moves the call: the Kettle Ridge repeater 0 kW against 185.2, not funded, and the outlying reconnection round 542.4 against 344.9, funded | still wrong: funds the repeater only (plan 475.5 kW); rescues R1 and two figures of R5 | no |
| S2 switches still working by install batch | stump | the annual test log: 96 in 100 pass | N11, N46, N35 | moves the call: the Larkin round 58.0 kW against 279.7, not funded | still wrong: funds the Larkin round only (plan 507 kW); rescues R2 and one figure of R5 | no |
| S3 switches still wired where the unit was replaced | stump | the work orders: 9 in 100 unwired | N14, L56, L58, N36 | moves the call: the reconnection round within 14 km 186.7 kW against 508.6, not funded | still wrong: funds both reconnection rounds and nothing else (plan 2,697 kW); rescues R3 | no |
| the delivered total on the steps | reflex | - | R102, R39 | same call | - | - |
| the study homes' randomised comparison, clustered | reflex | - | R55, R92 | same call | - | - |
| as-operated feeder membership from the switching log | reflex | - | R38 | same call | - | - |
| the appraisal constants (value, index, costs) | reflex | - | the work plan files them | same call | - | - |

Level: 5: three necessary stumps, none sufficient, the three single drops on three different wrong sets (seven distinct wrong calls across the lattice).

## Open members

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| Kettle Ridge VHF repeater (rep_w) | 250.3 kW against 185.2, 65 above | 10.4 | wrong: 0 kW, not funded | wrong: the coverage map covers every premise, 0 kW | S1 |
| Larkin find-and-fix round (fix_t) | 504.8 against 279.7, 225 above | 47.1 | wrong: 58.2 kW, not funded | wrong: the test log's 4 in 100, 58.2 kW | S2 |
| Reconnection round within 14 km (recon_in) | 1,402 against 508.6, 893 above | 54.6 | wrong: 260.4 kW, not funded | wrong: the work orders' 9 in 100, 260.4 kW | S3 |
| Halverson carrier fill-in (rep_n) | 184.5 against 279.5, 95 below | 25.3 | right: 0 kW, not funded | right | forced |
| Medora Flats find-and-fix round (fix_w) | 264.4 against 400.8, 136 below | 40.5 | right: 45.8 kW, not funded | right | forced |
| Outlying reconnection round (recon_out) | 224 against 344.9, 121 below | 19.5 | right: 98.7 kW, not funded | right | forced |

Direct route: for each member the pack's most direct evidence is read at face value by `hurried()` in `generator/core.py`: the carrier's coverage map for the two transmitter proposals (every premise covered, so a new site adds nothing), the annual test log for the two find-and-fix rounds (96 in 100 pass, so a round recovers 4 in 100), the service work orders for the two reconnection rounds (9 in 100 unwired). Each lands wrong on its open member because the record measures a shallower thing than delivery on a peak afternoon: outdoor reception on a test set, a bench click on the day of the test, a chance finding on another visit. The three forced members are below their lines on every hurried route and are crossed only by an over-correction, which is what keeps "fund everything" and "fund nothing" both wrong.

## Data provenance

Source: generated by the seeded generator in `task7/generator` around `core.py`, which simulates the cooperative's process: an enrolment history that began in town and moved outward, two one-way paging systems with their own transmitters, a summer dispatch trial drawn by lot, switches that fail with age, air conditioners replaced on their own clock, and a SCADA historian recording feeder load by the minute.
Behaves like the real thing: one-way direct load control fleets are evaluated from feeder or substation load steps at command times because the switches cannot acknowledge; published operability studies of such fleets find a third to a half of older switches not responding, for the three reasons simulated here (paging reception at the fringe of coverage, failed receivers and relays, and switches bypassed when the condensing unit is replaced); an air conditioner's reduction under cycling runs near 1 kW on a peak afternoon and scales with cooling load; a cooperative's wholesale demand charge is set by its load in the supplier's monthly peak hour.
Genuine patterns: (1) feeder load following the afternoon temperature with its own daily shape and a step at every shed and restore, (2) reception falling smoothly with distance to a transmitter, different for the two systems' sites, (3) the enrolment drive's geography (old switches in town, newer ones outward) and the housing stock's replacement of air conditioners by neighbourhood age, (4) hardware failing with age on a survival curve, (5) the study homes' unit-level responses with ordinary household noise, (6) the restore after each shed returning load above its pre-shed level.
Problems by process: the historian holds the last value through communication dropouts and two feeders carry their pre-rebuild names for part of the summer; the paging encoder logs local time with retried pages while SCADA is UTC; the 2021 billing conversion re-keyed premise numbers in part of the switch register; the radio shop's outage log is typed by hand with site nicknames and one overlapping entry; permits carry addresses in the county's own style; the switching log moves three feeder sections for parts of the summer.
License: not applicable (generated data)
Used as is: not applicable (generated data)
Breadth: about 16 files in four categories (CSV, workbook, PDF or Word, image); 11,923 switches on 46 feeders in four districts, 16 paging groups, 60 event days and 21,896 command steps inside about 1.2 million SCADA minutes, eight transmitters on two systems, 380 study homes with hourly intervals; deciding which of the many joins and windows to build, and which two files look relevant and are not, is work.

## Template check

Chain signature: causal-reasoning, modeling, missingness-measurement, decomposition-attribution, forecasting, synthesis, synthesis (seven results, six areas)
Question form: what (what is worth funding among the proposals), answered by a funded set with each proposal's kW against its break-even
Nearest build: by skeleton, task1 v8 (an unlabelled pool apportioned by a varying mix, on app installs and revenue, a go or hold on paid channels) and task9 arch 4 (spent); neither shares the decision form, the mechanisms or the file roles (`skeleton.py check`: severity none against every card, lineage entry and client task). By setting, task13 and task26 share the energy domain and nothing of the chain. The abstraction sentence a reviewer would have to write to call this a repeat ("a pooled outcome is apportioned among unit classes whose counts vary") is true of task1 v8's first stump only; here it carries three different conditions with three records and a causal question on a randomised dispatch.

## Frontier check

Precedents: R1 (N09, N27, L38, L70: today's structure assumed for all history, a second record at another grain set aside, a record carrying the modifier set aside, an aggregate record set aside for the detailed one), R2 (N11, N46, N35: a passed test taken to certify the unit, delivery priced at full, unit-level rates pooled when they look unstable), R3 (N14, L56, L58, N36: a second record set aside, a signal kept as a sensitivity, two tangled conditions read one at a time, rival explanations named and left untested), R4 and R5 (L63, L06: one step found and the other inputs left as they stood), R6 and R7 by dependence.
Shallow path checks: the reflex route passes every check it can run: the study homes' randomised comparison has a clean placebo and a tight clustered interval; the test log's pass rate agrees with the share of study switches that respond; the coverage map agrees with the register (every premise inside it); its delivered total reconciles to the steps. The check of another kind that refutes it is the three-slice comparison of predicted and recorded steps (off-air days, the oldest batches, the feeders with the most replaced units), which needs the transmitter files, the batches and the rebate and permit files beside the steps.
Assumption made false: "the fleet behaves like the metered study homes, and the cooperative's records say why not where it does not" (N11, N46, N27). False because the study homes were recruited in town among recent rebate takers with new switches, so they hold none of the three conditions, and each record measures a shallower thing than delivery. Tested by the steps against the three built covariates.
Forcing: each proposal's line is its filed annual cost over USD 88 a kW-year. The golden family (15 variants) keeps every proposal on its side: the nearest is the Medora Flats round, 324.3 at the band's high end against 400.8 (19 per cent clear), then the Kettle Ridge repeater, 235.7 at the low end against 185.2 (27 per cent), the outlying reconnection round (253.1 against 344.9) and the Halverson fill-in (202.4 against 279.5). Ten fresh draws of the step noise on the same world keep all six (rep_w 239 to 271, rep_n 162 to 239, fix_t 434 to 532, fix_w 214 to 292, recon_in 1,355 to 1,707, recon_out 199 to 264). The shortcuts sit across: 0, 58 and 260 kW against 185, 280 and 509. Each fitted input moved by 20 per cent (the far band's reception, the middle band's, the batch term, the flag term) and the working level moved by 10 per cent leaves the set unchanged (computed on the core's arrays: the tightest is the Larkin round at 316 against 279.7 with the batch term 20 per cent up); the build asserts each in `checks.py`.
Noun swap: nearest by `skeleton.py check` is task1 v8 (shared lesson `unlabelled_pool_apportioned_by_varying_mix`, shared move `source_rates_fitted_to_pool_totals`); swapping its nouns in (installs for switches, networks for batches) carries the pooled fit and nothing else: no randomised dispatch, no reach rebuilt per day, no replaced-unit flag, no repair proposals, a different decision form. Severity none. The three WARNs are answered here: `unlabelled_pool_apportioned_by_varying_mix` and `latent_structure_estimation` are each on two live builds of ours in other domains and other roles (this is the third use of each, which a reviewer could read as a house habit); `set_over_threshold` is the honest form for five proposals each against its own break-even and is on five live builds, so the answer shape (scenarios with the flip point) and the bridge carry the difference.
Closed strategies: the call turns on `instrument_noncompliance` (commands sent against commands received and acted on), which no accepted task teaches and no card holds. Read by its fix against the 45 cards: the nearest are "some groups are recorded far less completely" (fix: each group's completeness from an independent source, grossed up) and "the source reads high or low" (fix: a bias measured on checked cases). Neither is the fix here: no independent source or checked sample holds any share (the study homes hold none of the three conditions and the test log and work orders are the records being superseded), and nothing is grossed up; each share is identified only from how the pooled steps move as each class's dispatched count moves, with the reach rebuilt per event day. S1 beyond the nearest card: a reception curve in a covariate built from three files, proved on days a transmitter was off the air. S2: a working share by batch from each batch's own steps, set against a level the study homes supply for one cell. S3: a flag effect separated from the batch term it is tangled with. The transport card is not the fix either: the study homes are not reweighted to the fleet, because they have no far, old or replaced-unit cells to weight. No closed lesson decides. Closed lessons kept as supporting steps, each leaving the call standing when omitted alone: the interval on each proposal's kW clustered by event day (the clustered-interval card; omitted, the figures and the set are unchanged) and the restore's snap-back named beside the coincident-peak hours (the payback card; the appraisal page files that proposals are appraised on the shed hours, so it moves nothing).
Decisive steps: S1 owns "83 in 100 shed commands are lost at switches more than 20 km from an on-air transmitter of their own system" (17 get through), asked by "what share of shed commands get through at the edge of our paging coverage", in the workbook and the slides; its evidence sits in `paging_transmitters.xlsx` (system, coordinates, on-air dates), `radio_shop_outage_log_2026.xlsx` and the register's receiver field against the steps; once named, the per-day reach, the apportioning and the carry to the proposals are left. S2 owns "33 in 100 switches installed through 2015 no longer shed" (67 still work), asked by "what share of the switches installed through 2015 still work"; evidence in the dispatch log's group addresses, the register's install dates and the study homes; left: the batch fit net of reach and replaced units, against the responders' level. S3 owns "68 in 100 switches are unwired where the air conditioner was replaced since" (32 still wired), asked by "what share are still wired in where the member has replaced the air conditioner since"; evidence in `hvac_rebates_2012_2026.csv` and `county_mechanical_permits_2010_2026.csv` dated against installs; left: the union, the dating and the pooled flag fit. Independence, from the lattice: without S1 the funded set is Larkin and both reconnection rounds (the repeater 0 kW, the outlying round 542); without S2 it is the repeater and the reconnection round within 14 km (Larkin 58); without S3 it is the repeater and Larkin (the reconnection round 187); without S1 and S2 both reconnection rounds only; without S1 and S3 Larkin only; without S2 and S3 the repeater only; without all three none. Each component holds its golden value in every row where its own step is kept.
Run routes: all four are estimators in `core.py`'s `run_routes`. Generous (every named field and the distance to the nearest listed transmitter of either system, fitted jointly on the steps): funds Larkin, Medora Flats and the reconnection round within 14 km, misses the repeater below its line (6.7 kW) and puts Medora Flats above its line (555.6), earns 21. Calibrated (the study homes end to end): funds nothing, three members below, earns 9. Hedge (every signal noted, the three records central): funds nothing, earns 9. Cut-off (beyond 14 km lost, pre-2012 dead, flagged unwired; nine settings from 10 to 20 km and 2009 to 2015, every one wrong): funds Larkin, Medora Flats and the reconnection round within 14 km, the repeater below and Medora Flats above, earns 9. The misses fall on both sides of the lines, and each stump pushed past its fit files a wrong set too.
Validation handles: none. `scada_feeder_1min_2026.csv` holds only pooled steps: it identifies a group's total on a feeder and scores no share. `study_meters_hourly_2026.csv` holds unit-level delivery for homes with no fringe, no pre-2016 switch and no replaced unit: it scores none of the three shares and supplies the working level only; the calibrated route on it files none funded. `amr_monthly_reads_2024_2026.csv` cannot show a 3-hour shed on some afternoons in a month's total. `switch_test_log_2019_2026.csv` and `service_work_orders_2019_2026.csv` are the face-value records and score nothing. The wholesale invoices hold the cooperative's total in twelve peak hours a year, too few and too pooled to score a share. No file pairs a switch with a delivered kW, no slice observes a proposal's premises under a repair, and no total closes on any one cause.
Forward window: the figure is the kW each proposal adds in summer 2027 with every listed transmitter on the air and the supplier's cooling index at 1.15, not the 2026 trial's mean: the trial ran at indices from 0.65 to 1.25 with two transmitters off the air for part of it and one commissioned mid-summer, so the record's own mean delivered per switch misstates the 2027 footing; the history-mean route (each proposal credited with the trial-average shortfall of its premises, no cause split) files the repeater and the two rounds on the same shortfall and cannot tell which repair restores it.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | "worth funding" | adds at least its break-even kW; adds any kW; best cost per kW | kW added at USD 88 a kW-year covers the filed annual cost | the prompt's own sentence ("covers its yearly cost") and the appraisal page |
| SF2 | "peak kW it adds in 2027" | at the 2026 trial's mean conditions; at the coincident-peak index | at cooling index 1.15, the mean of the four 2026 coincident-peak afternoons | the appraisal page files the index and its value; same call at the trial mean (asserted) |
| SF3 | each proposal alone or stacked | against present practice; on top of the others | each on its own against present practice | the appraisal page ("each proposal is appraised on its own against present practice") |
| SF4 | transmitters on the air in 2027 | the set on the last trial day; every listed transmitter | every transmitter on the register with no off-air date | the appraisal page; the register's on-air dates |
| SF5 | "the edge of our paging coverage" | beyond 20 km from any listed transmitter; beyond 20 km from one the switch can hear | more than 20 km from the nearest on-air transmitter of the switch's own system | the Kettle Ridge proposal's scope files the fringe as "more than 20 km"; the receiver and system fields; the off-air days (a feeder beside the other system's site loses its steps when its own transmitter is off) |
| SF6 | "share of shed commands get through" | absolute; against switches near a transmitter | against switches within 8 km of their transmitter | named data: the steps identify delivery at the fringe only against the nearest band (the level of reception near a transmitter is not separable from the working level), and the answer states that basis |
| SF7 | "installed through 2015" | by install date; by receiver type | install date on or before 31 December 2015 | the prompt; the two coincide on the register (every pre-2016 switch is VHF) |
| SF8 | "still work" | among all pre-2016 switches; among those with no replaced unit | at premises with no replaced unit, so the two causes are not counted twice | the bridge order on the appraisal page; the all-premises reading is stated beside it in the workbook |
| SF9 | "replaced the air conditioner since" | any rebate or permit; one dated after the switch's install | a rebate or a mechanical permit for a condensing unit dated after the switch's install date | the reconnection proposals' scope files exactly that list |
| SF10 | the bridge's order | reach, then hardware, then wiring; another order | a switch counts against the first step that stops it: page, hardware, wiring | the appraisal page's bridge template (last year's report uses it) |
| SF11 | "the kW the fleet could shed" | the planning figure of 1.0 kW a switch; what a working, reached, wired switch takes off | the study homes' responding switches, 0.802 kW at index 1, times the register at index 1.15 | last year's report states its planning figure as such; the study homes measure it; the planning figure is priced beside it in Ask 2 |
| SF12 | the step at a command | five minutes before against five after; other windows | the mean of the five minutes after less the five before, at the encoder's transmit time | same call at 3 and 10 minutes (asserted); the group commands are ten minutes apart |
| SF13 | which switches a command addresses | the register's group; the encoder's address plan | the register's paging group, which is the encoder's address | the two agree on every switch (asserted) |
| SF14 | feeder of a switch on an event day | today's map; as operated | as operated, from the switching log | named data: three sections moved for parts of the summer; same call either way (asserted) |
| SF15 | reach bands | 8, 14 and 20 km; others | 8, 14 and 20 km | same call under four other sets of bands (the battery) |
| SF16 | weighting of the steps | by feeder load; unweighted | by the inverse of feeder load | same call unweighted (the battery) |
| SF17 | the batch term | free by group; a line in age | free by paging group | same call as a line in age (the battery) |
| SF18 | a study home that responds | mean response over 0.25 kW; 0.15; 0.35 | over 0.25 kW | same call at 0.15 and 0.35 (the battery) |
| SF19 | the cooling index's origin | zero; later onset | the supplier's published index as it stands | same call with the origin moved to 0.1 (the battery) |
| SF20 | the find-and-fix and reconnection rounds' premises | every pre-2016 switch in the district, or those with no replaced unit; every flagged premise, or split at 14 km | pre-2016 switches at premises not on the reconnection lists; flagged premises within, and beyond, 14 km of their own system's nearest transmitter | each proposal's filed scope |

## Pinning list

| Constant | Golden value | Home |
|---|---|---|
| value of a coincident-peak kW | USD 88 a kW-year | `work_plan_2027_load_management.docx`, "Appraisal" (four summer months at the supplier's demand rate, shown on the invoices) |
| each proposal's annual cost | USD 16,300 (Kettle Ridge), USD 24,600 (Halverson), USD 15.60, 28.40, 13.70 and 24.50 a premise visited (Larkin, Medora Flats, reconnection within 14 km, outlying reconnection) | `work_plan_2027_load_management.docx`, each proposal's cost line |
| the appraisal's cooling index | 1.15 | the work plan's "Appraisal"; the index itself is the supplier's daily series, `sunflower_basin_cooling_index_2026.csv` |
| the proposed sites | Kettle Ridge at grid (-31.0, 12.0) km, Halverson at (3.0, 25.0) km | `work_plan_2027_load_management.docx`, each transmitter proposal's site line |
| the fringe and the near band | more than 20 km, within 8 km | `work_plan_2027_load_management.docx`, the Appraisal page; the middle bands (8 to 14, 14 to 20) are the golden's and their measured spread across the battery's four other band sets is in every band |
| pre-2016 | install date to 31 December 2015 | the prompt and `work_plan_2027_load_management.docx`, the find-and-fix proposals' scope |
| a replaced unit | a rebate or permit dated after the switch's install | `work_plan_2027_load_management.docx`, the reconnection proposals' scope |
| the outlying premises | more than 14 km from the nearest transmitter serving the switch | `work_plan_2027_load_management.docx`, the outlying reconnection proposal's scope |
| what a working switch takes off | 0.802 kW at index 1 | measured from the study homes (responders over 0.25 kW); the cut's spread is in the bands |
| reception by band, the batch term, the flag term | 0.928, 0.637 and 0.166 against the near band; 16 batch levels; 0.324 | fitted from the steps; their spread across the battery is the bands |
| the step window | five minutes either side of the transmit time in `paging_encoder_log_2026.csv` | the golden's convention on `scada_feeder_1min_2026.csv`; the build measures its spread at 3 and 10 minutes and asserts the same call |

Variant battery: 15 variants file one answer, the same funded set, across every convention the golden uses (four other sets of reach bands, unweighted least squares, no district term, the batch term as a line in age, the first six and the last six event days dropped, even and odd event days alone, the study responders cut at 0.15 and 0.35 kW, steps beyond 2.5 standard deviations trimmed, the cooling index measured from 0.1); every band is their range with a quarter of its width as room. No constant in the golden is known only to `core.py`: the world's reception curve, survival curve and unwiring rate are never read by any estimator.

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the air-conditioner switches on the register at 30 September 2026 (the appraisal page); water-heater switches run a winter schedule and are outside the proposals |
| 2 | Unit of account: one switch at one premise; a proposal's figure is kW summed over the premises in its filed scope |
| 3 | Attribution window: the shed hours of an event afternoon, 16:00 to 19:00 local |
| 4 | As-of dating: the register, the transmitter list and the replaced-unit list as at 30 September 2026 |
| 5 | Version basis: feeder membership as operated on each event day (the switching log); the transmitter set as on the air on each event day for the fit and every listed transmitter for 2027 |
| 6 | Denominator: shares are against switches within 8 km of their transmitter (reach), against a working switch's level (hardware) and against premises with no replaced unit (wiring) |
| 7 | Weighting: steps weighted by the inverse of feeder load; same call unweighted |
| 8 | Window length: all 60 event days of the 2026 trial; halves of them give the same call |
| 9 | Boundary inclusivity: "more than 20 km", "through 2015", "dated after the install date"; no proposal sits within its band of a boundary |
| 10 | Rounding path: kW to whole numbers after summing; shares to whole per cent; cost per kW to one decimal; each stated with its band |
| 11 | Tie-break: none needed; no two proposals compete for a place |
| 12 | Maturity and censoring: the trial is closed; switches installed during the summer count from their install date |
| 13 | Order of operations: clean and align the records, build the steps, build the three covariates, fit, carry to each proposal, price |
| 14 | Row order: the CSV lists the proposals in the work plan's order |
| 15 | Duplicate resolution: retried pages collapse to the first transmit time; duplicated SCADA minutes keep the first; a premise with a rebate and a permit counts once |
| 16 | Identity normalisation: premise numbers re-keyed in 2021 map through the register's own old-number field; permits join by normalised address; the two renamed feeders map by the SCADA point list |
| 17 | Netting against gross: a proposal's figure is the kW after less the kW now for the same premises |
| 18 | Dimensional units: kW at the feeder breaker; km on the cooperative's planning grid; SCADA in UTC, the encoder in Central prevailing time |
| 19 | Code and status semantics: a test-log "pass", a work-order finding and the coverage map are records of the day they were made, never the delivered state |
| 20 | Integerisation: premises visited are counts by construction; kW are not rounded before pricing |
| 21 | Clause scope: each proposal's scope sentence in the work plan fixes its premises or site; the appraisal page fixes value, index, footing and the bridge's order |
| 22 | Forward window contents: summer 2027, the enrolled fleet as it stands, every listed transmitter on the air, no other proposal assumed |

## Literal reader

The prompt and the work plan executed word for word: "what is worth funding" is each proposal whose 2027 peak kW, times USD 88, covers its filed yearly cost; "the peak kW it adds" is the kW after less the kW now for the premises in its filed scope, at index 1.15, every listed transmitter on the air, on its own; "what share of shed commands get through at the edge" is delivery per enrolled switch more than 20 km from its transmitter against switches within 8 km; "installed through 2015" and "replaced the air conditioner since" are the register's install date and the dated rebate or permit; "how the kW the fleet could shed splits" is the appraisal page's bridge in its filed order. Read that way every sentence lands on the golden's quantity; the easy answers come from easier methods on the same quantities (the three records at face value), never from another reading.

## Prompt contract

A voice rewrite must keep: the question (what is worth funding among the 2027 load-management proposals); the reason the answer is an estimate (the switches cannot report back, the meters are read monthly, so it rests on last summer's dispatch trial); the test (the peak kW a proposal adds in 2027, at the plan's value per kW, covers its yearly cost); for each proposal the kW it adds and its break-even; the three decisive quantities, each asked in the decision's words and marked here as a decisive step's own: the share of shed commands that get through at the edge of paging coverage (S1), the share of switches installed through 2015 that still work (S2), the share still wired in where the air conditioner has been replaced since (S3); the split of the kW the fleet could shed at peak into delivered and lost to each; the three deliverables by type (a CSV with a row per proposal, a workbook showing how each figure comes from the data, a few slides). It must never add: a rounding instruction, a method, a comparison, a warning, the name of an attached file, who is asking or for whom, the number of proposals, switches, feeders or event days, the words transmitter outage, batch, rebate, permit or feeder step, or any distance.

## Build brief

For the build thread, which has none of the architect's context. Execute it; move nothing under `Frozen:`. A gate that cannot pass inside it goes back to the architect with the failing figure.

World: Cottonwood Draw Electric Cooperative (fictional, south-central Kansas; headquarters town Larkin; districts Larkin, Medora Flats, Halverson and Pruett; wholesale supplier Sunflower Basin Power; paging carrier TriCounty Paging). It serves about 36,000 meters on 46 feeders out of 12 substations and runs a summer air-conditioner load-management programme on 11,923 one-way paging switches, enrolled since 2004 (the drive began in Larkin and moved outward). Switches installed to 2015 listen to the cooperative's own VHF paging system (three transmitters: headquarters, the Medora Flats substation, the Halverson substation); later ones listen to TriCounty's 900 MHz system (five sites). The switches cannot report back. Members' meters are read monthly by drive-by; the only interval meters are on 380 "study homes" in Larkin, recruited in 2019 among members who had just taken the cooperative's high-efficiency air-conditioner rebate and fitted with new switches then. The 16 paging groups are install batches (group 1 the oldest). In summer 2026 energy services ran a dispatch trial: on each of 60 hot weekdays a random 4 to 12 of the 16 groups were shed 16:00 to 19:00, one group every ten minutes from 16:00 in a random order, each command a step in every feeder's load. During the trial the Halverson VHF transmitter was off the air on eight event days (lightning), the Medora Flats VHF transmitter on six (antenna work), TriCounty's north-east site on five, and TriCounty's Pruett site was commissioned before the 31st event day. The cooperative's load in Sunflower Basin's monthly peak hour sets its demand charge. The 2027 work plan carries six load-management proposals; the board adopts the plan in December 2026. `generator/core.py` builds exactly this world on arrays (`build()`), fixes every dial and proves the core; wrap it, never re-derive it: the generator imports `core.build()` and writes the files from its arrays, so the switch list, coordinates, install years, groups, states, event days, weather index, dispatch draws and step noise are the core's own. core.py's districts 0 to 3 are Larkin, Medora Flats, Halverson and Pruett; `rep_w` is the Kettle Ridge VHF repeater, `rep_n` the Halverson carrier fill-in, `fix_t` and `fix_w` the Larkin and Medora Flats find-and-fix rounds, `recon_in` and `recon_out` the two reconnection rounds.
Frozen: everything in `generator/core.py`: SEED 713; 60 event days; the feeder, switch, install-year, coordinate, group, load and dispatch draws; the two systems' transmitter coordinates and their off-air and commissioning windows; the reception, survival, replacement, unwiring (0.72) and flagging (0.93) processes; the step noise (0.4 per cent of feeder load on a ten-minute before-and-after difference; the SCADA minutes the build writes must reproduce core's `step` array to within rounding when the step is taken as the five minutes after the transmit time less the five before); the study homes (380, 1 to 8 km, six or seven year old switches, no replaced unit, 1.0 kW household noise per event); the appraisal constants (USD 88 a kW-year, index 1.15, annual costs USD 16,300 and 24,600, USD 15.60, 28.40, 13.70 and 24.50 a premise, the 20 km fringe, the 8 km near band, the 14 km outlying split, the 2015 install cut); the estimators `tensor`, `fit`, `study`, `figures`, `model`, `hurried`, the 15 variants, the run routes and the three-slice check; the members' lines and every golden figure, band and call. The face-value records are frozen at their values: the coverage map covers every enrolled premise, the test log passes 96 in 100, the work orders find 9 in 100 unwired after a new unit.
Files: (1) `scada_feeder_1min_2026.csv`, the historian's export: UTC time, SCADA point, kW; one row per feeder minute for 15:00 to 20:00 local on the 88 summer weekdays (about 1.2 million rows; the large file); weather-driven load with each shed and restore step from core; frozen values through dropouts and two renamed points are the mess; it must not carry any column that marks an event, a group or a step. (2) `paging_encoder_log_2026.csv`: one row per page transmitted (local time, system, group address, command, retry flag), about 2,200 rows. (3) `lm_switch_register.csv`: 11,923 rows (the second large file, well past ten printed pages): serial, premise number and old premise number, service address, feeder, grid x and y in km, install date, receiver (VHF 153 MHz or FLEX 929 MHz), paging group, device type, status. It must not carry any field of the switch's condition, last-heard date or signal level. (4) `paging_transmitters.xlsx`: site, system, grid x and y, on-air date, off-air date if any, owner. (5) `radio_shop_outage_log_2026.xlsx`: the hand-kept log of transmitter outages (site nickname, from, to, cause). (6) `switching_log_2026.csv`: feeder section transfers. (7) `hvac_rebates_2012_2026.csv` (premise number, unit type, install date) and (8) `county_mechanical_permits_2010_2026.csv` (address, permit date, work type); their union dated after the switch's install is the replaced-unit flag core calls `flag`, so the two files together must reproduce it exactly. (9) `study_meters_hourly_2026.csv` and `study_homes.csv`: the 380 homes' hourly kWh for the summer, with home, group and which event days each home's switch was held out (core's `s_tr`); responses must reproduce core's `study()` figures. (10) `sunflower_basin_cooling_index_2026.csv`: the supplier's daily cooling index (core's `w` on event days), and (11) `wholesale_invoices_2026.pdf`: monthly peak hour, billed demand, the demand rate (USD 22.00 a kW-month, four summer months making 88) and each peak afternoon's index (mean 1.15). (12) `work_plan_2027_load_management.docx`: the six proposals, each with its scope sentence (site and system for the two transmitter proposals; "switches installed through 2015 in the Larkin district at premises not on the reconnection lists" and the same for Medora Flats; "premises with a rebate or a mechanical permit for a new condensing unit dated after the switch was installed, within 14 km of the nearest transmitter serving the switch" and "... more than 14 km ...") and its annualised cost, and an "Appraisal" page: USD 88 a kW-year; proposals appraised on the shed hours at index 1.15, with every listed transmitter on the air, each on its own against present practice; the fringe as premises more than 20 km from the nearest transmitter serving them and the near band as within 8 km; and the bridge template in last year's order (commands not received, received but the switch failed, working but not connected, delivered). (13) `load_management_report_2025.pdf`: last year's report, the register times the planning figure of 1.0 kW a switch, labelled as a planning figure. (14) `tricounty_coverage_map_2026.png` (or PDF): the carrier's and the cooperative's published coverage, every enrolled premise inside. (15) `switch_test_log_2019_2026.csv`: the bench-signal test at install and at any service visit, 96 in 100 pass. (16) `service_work_orders_2019_2026.csv`: visits made for other reasons, with a "switch found unwired" finding on 9 in 100 visits to premises with a new unit. Distractors, never labelled: (17) `amr_monthly_reads_2024_2026.csv` (monthly drive-by reads per account) and (18) `water_heater_winter_schedule_2025_26.csv` (the winter programme's dispatches). Document every field, never a process: no document says how a step is taken, that reach should be computed per day, that groups are batches (the register and the encoder log show the group; the install dates show the batches), or what any share is.
Never filed: any sentence that a page can be missed, that reception falls with distance, or that a switch hears only its own system (the receiver and system fields carry it); the words "own system" beside "on the air that day"; any statement that paging groups follow install order; any switch-level or premise-level delivery, signal, last-heard or working field; any count or share of failed, unwired or unreached switches other than the three face-value records; any sentence joining the rebates or permits to the switches; the phrases "feeder step", "step change", "realisation rate", "operability", "noncompliance"; any note that the study homes are unrepresentative; any figure from `core.py`'s golden.
Goldens: three files, exactly what the prompt asks. `load_management_proposals_2027.csv`: one row per proposal in the work plan's order (proposal, premises or site, kW added in 2027, break-even kW, annual cost, cost per kW-year, funded yes or no). `load_management_trial_2026.xlsx`: first sheet the call and the six rows; then the step record's summary, the fitted model (reception by band, the 16 batch levels, the district terms, the replaced-unit term, the study homes' working level), the three shares (R1 to R3), the bridge (R4), the proposals (R5 and R6), a routes sheet (each record at face value alone and together, the study homes carried to the fleet, the nearest-listed-transmitter fit, with the figure and the set each files) and a variants sheet (the 15 variants). `load_management_2027_board.pptx`: a few slides, the first stating the call, one chart of the bridge, one of each proposal's kW against its break-even. Every figure from `figures.json`, written by the generator from core's functions. Answer blocks: the Final Recommendation names the three funded and the three rejected; Critical Components are R1, R2 and R3 as shares with bands and no method; Supplementary Questions carry Ask 1 (six proposal figures, one sentence each), Ask 2 (the bridge, one sentence) and Ask 3 (the plan's kW and cost per kW); the counts every route reaches sit only in the Step-by-Step, which closes on the leave-one-out and leave-two-out table from the lattice.
Free: the remaining nouns (feeder and substation names, site nicknames, staff beyond the four people), the weather and load shape between steps, Layer 1 texture inside the limits above, the two distractors' content, the documents' genre and layout, the chart styles, `effort.json`'s passes (the reflex route is `hurried()` with all three, the quick pass the planning figure), and `checks.py` (assert every SF row, the pinning list, the 20 per cent moves, the step-window variants and the three face-value records). The old architecture's generator files (`world.py`, `obs.py`, `pack.py`, `analysis.py`, `checks.py`, `effort.json`, `figures.json` and the rest) are replaced; `effort.json` and `checks.py` in particular are architecture 12's and must not survive into the build.

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
- 2026-11-08, architecture 5 draw, on paper: two effects offsetting inside the observed window (mix against rate under a flat total) as the deep step; task8 arch 18 already carries it, so another would read as a template.
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
- 2026-11-11, architecture 9 at build: the asks first carried each measure's saving season by season, the pilot's
  2025/26 CO2 and every application received; effort.py measured the careful but hurried pass at 61.7, the earned asks
  outweighing the two judgments, so the seasons and the 2025/26 CO2 left the asks (the seasons stay in the workbook as
  working) and the listing asks only for the funded measures' applications and their total, which a run that funds the
  wrong set gets wrong. The range's low ends were taken out of the grading: a symmetric range or a leave-one-owner-out
  spread puts them 20 to 70 per cent from the percentiles while every construction keeps the upper end, the end the
  committee judges, inside its band.
- 2026-11-11, stage 4: the judge read the feeder, hosting and heat-pump lines at the head of this section as another
  build's; they are this slot's own earlier draws (the co-op heat-pump architectures retired in October), kept under
  the append-only rule.
- 2026-11-12, architecture 9 at the platform: the run landed the call (insulation alone) and both deciding judgments by
  reflex: it clustered its bootstrap at the owner because the pilot rules filed the draw by owner, and separated the
  check campaign from the measure's ageing because the heat plan filed it (task7/runs/arch9/run1.md). It lost only
  insulation's transport (it set the solar cadastre aside as unrelated) and second-decimal figures. A judgment whose
  trigger a document files is executed; the world is spent, and architecture 10 moves to another world, dataset and
  shell.
- 2026-11-12, the READY prompt's framing: it restated the renewal bar, opened its second sentence on why the answer has
  to be an estimate (task457's approved opening) and pinned each kW to "the 4CP intervals of a summer like 2024 to 2026".
  Cut at the author's direction: Board Policy 412 files the bar, the intervals, the alerts as called and the devices
  counted, so the clauses were context the files hold, and "estimated from the last three summers" pointed at the data
  window. The prompt now asks the question, the two files and the asks only; no graded figure moved.
- 2026-11-12, architecture 10 (Cedar Brake co-op's thermostat providers at ERCOT's 4CP, READY at 03:15, never uploaded): the client's overused-strategies page, filed at 09:37 the same day, closes all three deciding carries (the 4CP days late in heat waves is
  'Repeated exposure behaves differently from a one-off', whose own example is smart-thermostat demand response fading over
  consecutive hot event days; the 2027 retail cohort and the fleet's homes are 'The pooled effect does not transfer to a target with
  a different mix'), so the call was a stack of closed lessons; the guard read it only as near because the card named another key.
  The world, its dataset and its shell go with it; architecture 11 decides on coincidence at a shared transformer, off the page.
- 2026-11-12, architecture 11 at calibration: half the chargers in the managed half made the 2026 meters alone call 'keep own
  schedules' (the metered summer's count fell below Sequence's), so a step near the closed 'outcome hidden by the intervention' card
  would have decided; the pilot manages one charger in four instead, and the route that reads own schedules off the meters now
  leaves the call standing (no_own in effort.json).
- 2026-11-12, architecture 11 at calibration: the managed half's own settings drawn from the own half's distribution or set to the
  commonest timer moved the own count by 13 (64 against 77); the roster now carries the usual charging each member gave at
  enrolment, as the rate schedule says it is asked, and the declared-only rival sits inside the band.
- 2026-11-12, architecture 11 at calibration: the monitored transformers' option-by-option peak lift as the golden put Stagger 6
  above the world's quarter-hour truth; the per-hour excess lands closest to the truth and is the golden, the peak lift a rival.
- 2026-11-13, architecture 11 after the holistic check: the Sequence count (11, USD 160,300) and the flip fee (USD 156) rested on three readings no file settled (whether the queue waits for a late charger: 7 if not; the ready-by for a session with none in the app: 14 or 16 at 15 or 30 minutes before the unplug; how hourly reads become quarter-hours: the golden's per-hour excess scaled by the square root of homes was filed nowhere). Closed by filing all three at their authority (the proposal's rule now says each charger waits for every one before it, the earlier plug-in first, both products on the quarter-hour; EV-4 4.1 the replay's frame and ready-by at the unplug time rounded down; DPS-7 revision 5's 2.2 and Table 2 peaking factors by nameplate, set from the 48 monitors and applied monitored or not, with Table 1's missing 50 kVA pole-mount row), not by keeping any open: the golden moved (own 53, Stagger 29.7, Sequence 13 and USD 196,700, flip USD 153) and the bands carry the rivals plus one marginal unit either side. The quarter-hour lift is no longer a judgment, so the depth line is level 4 on three judgments, not 5 on four. Re-judged once (Sequence replayed transformer by transformer to 13; Stagger sampled to 29.5 once the judge's own script stopped applying 0.95 twice and piling pre-July blocks onto 1 July): DETERMINISTIC, FIX_NOW, three answer-block sentences (the late charger counts ahead of every later one, energy over the recorded charge time, the clock six hours behind UTC), applied; the leak reader found no leak.
- 2026-11-13, architecture 11 (Hollins Creek's EV Overnight default) retired: the platform run landed every graded result (task7/runs/arch11/run1.md); its retrofits were each tried and refused on paper: per-device Stagger persistence (contradicts the proposal's wording; filing it hands it over), offline fallback on shared nights (a literal replay catches it, or nothing pins it), Sequence on the uncorrected GIS (plus or minus 2 transformers), charging taper (moves every figure, never the default, one sentence rescues four results).
- 2026-11-13, architecture 12 prototypes: per-feeder tap-event cells (too noisy alone: the commercial morning ramp and on-the-hour temperature steps contaminated them; the same-class peer control fixed the ramps, but heat pumps and resistive heat could not be told apart in the fit, so the compressor response was left to the trial's scale with every non-thermostatic load answering in proportion); an energy-weighted trial scale (one noisy trial feeder moved it 10 per cent; the median of the trial feeders' ratios holds it to 2.3 per cent).
- 2026-11-13, after the DRAWN commit (f1493be), the review before stage 4: J1 (the trial on its achieved dose) and J4 (the far end's volts) were stumps on paper but VO-1 3.1 and 2.3 spell both, so a careful run executes them; moved to the reflex side, the careful pass rose to 55, and seed 3077's three remaining stumps dropped onto two wrong sets only; the world was re-searched on the new reflex definition (1,200 seeds) and seed 4009 kept (three distinct single-drop sets, every rival and perturbation 4.8 percent or more from the line, the golden within 0.6 percent of the world's savings); two asks added that the stumps decide (each feeder's yearly response, the saving at the customer meters) and the program total; R2 graded on the trial feeders' average, since a linear-weather trial fit moved single trial feeders by up to 40 percent while the average moved 4 percent.
- 2026-11-13, the same review: the customer-meter export wrote MWh into a column headed kWh (each feeder's energy a thousand times small), fixed in the writer; the loss change was filed negative for a rise against the prompt's plain reading, now asked and filed as a rise; the annual report's customers and sales now come from the same load as the pack.
- 2026-11-13, stage 4 sweep: the year's exports ran to 31 December 2026 while their stamps and the memo sat in November (dates after the setting); the as-of moved to 14 January 2027, the year's exports to 4 to 7 January, the trial's records and the queue kept at their own dates.
- 2026-11-13, stage 4: the determinism judge (DETERMINISTIC, APPROVE) offered one optional fix, a VO-1 sentence that the loss current uses the feeder's own voltage; declined, because a filed sentence naming the step hands the losses stump (J5) to every run, and the nominal-kV reading is already ruled out by named data (SF17: the head-metered trial feeders' losses per load squared 7 to 9 percent higher on ON days).
- 2026-11-13, the platform's holistic audit of READY b75d025 (task7/runs/arch12/holistic_audit.md): the run did every priced stump by reflex (IV on the achieved dose, thermostatic transport from survey times load research, hourly far-end headroom, current squared at the lowered voltage, all within 2 percent), so J2, J3 and J5 are reflexes (R67 to R70) and the careful column's 47 was a design's guess; and the transport was unpinned (heating balance point, heating source, water-heating basis, pooled or per-class scale moved ELC-113 0.39 to 0.50 and GBR-113 0.36 to 0.49 against lines of 0.46 and 0.41), partly because the golden's 58 F and 68 F degree bases were the generator's own constants and no file holds them. Not uploaded; the deciding layer is redesigned on paper first.
- 2026-11-13, after the audit, the paper screen and prototypes: retrofit candidates availability from the AMI mesh (filing it hands it over, carrying it per feeder is the closed transport card), regulator tap steps (one value count of the log shows it) and cost overrun (a single-use file) died on paper; re-root worlds (a heat-pump lottery at the design-day peak, a randomized trimming trial, a wind-forecast vendor A/B) kept one trap each at most; the kept retrofit layer's T1 (compressor energy response from 2-hour tap events) died in prototype: 16,179 events give the compressor term -0.21 (0.22) against a true -0.30 and the base and thermostatic terms biased (0.36 for 0.80, 2.03 for 0.57), restricted to high-compressor hours -0.18 (0.17) against -0.10, too loose to pin a feeder. The auditor's variant spread measured on seed 4009: residential and rural feeders move 11 to 23 percent in yearly response across balance point, heating source, water heating and pooling, 11 distinct funded sets in 96 variants; with the degree bases pinned, per-class scaling still moves 13 percent and the heating source 7.
- 2026-11-13, retired: after the SKILLS commit abc0732 recorded the lessons, the author chose a new task number in the same domain with another analysis type; nine worlds screened in Energy x Experiment kept two stumps at most (a program-delivery world: the Q4 slip past the credit cliff, the claims-against-credits residual); the slot's lineage stays on the card.

- 2026-11-25, the re-root to architecture 13 after the author un-retired the slot: the reviewer's own suggestions of 2026-11-11 were screened against the closed page and not followed (design-clustered ranges are the clustered-interval card; controls carried through round-the-clock uses are transport and range; the cadastre's noisy addresses are the attenuation card; the 2022 price shock and burner checks in the passed-over arm are a co-occurring change; completion capacity as a forecast is the returned hidden factor), and architecture 9 had already built two of them and been landed by reflex. The Haldenau world stays spent.
- 2026-11-25, worlds screened on paper for architecture 13 and dropped before any code: every Energy x Experiment world whose outcome a member-level interval meter or a feeder SCADA point observes under a randomised lever died at test 0 (the rigorous comparison lands: a default time-of-use trial, a peak-time rebate against its settlement baseline, a home battery dispatch trial, a ripple-control window trial read at the zone substation, a district-heating peak-shaving trial read at building meters, a prepaid tariff trial read on vends); a gas thermostat setback trial kept one stump (runtime is not gas) and a physics chain; heat cost allocators in master-metered buildings died on the building meter; a district-heating supply-temperature switchback is the repeated-exposure card; an operator-called event series with a roster instrument died because the day-of load before the event carries the selection; a load-control fleet with interval meters at every member kept one stump (the working share) and handed the other corrections to a unit-level regression.
- 2026-11-25, architecture 13 prototypes that died before the kept core: (1) the three conditions fitted from each feeder's whole-window response against a counterfactual: a common day shock of 0.4 per cent of load swamped the install-batch dose, the batch levels came out at 0.38 to 0.87 in no order and a figure's spread across seeds ran to 40 per cent, and a day fixed effect removed the batch signal with the shock; replaced by the step each group's command makes at its own minute, which no day shock touches. (2) A Weibull hardware curve extrapolated to a new switch: the shape was not identified from the pool (k 1.0 to 2.6 across seeds), so the after-state of a repair is the study homes' responding switches instead. (3) Single against repeated pages as a third judgment: every proposal's figure is a difference of delivered kW and needs no reception level, so the identity moved no member. (4) The fleet's level from the study homes against the pool as a third judgment: a pooled total is one regression the runs make, kept as reflex work. (5) The carrier's western site at the town end of Medora Flats: the nearest listed transmitter of either system then tracked the own-system reach, and the route that fits every named field landed the call and earned 72; the carrier's site stands in the outer west in the kept world (as a carrier's would, beside the highway), so reach has to be built by system. (6) One reconnection round with the Larkin round's line at 350 kW: a 20 per cent rise in the batch term flipped the Larkin round and the over-corrected third judgment rested on a 5 per cent margin; the round is split at 14 km and the Larkin line set at 280.
- 2026-11-25, stated plainly for the next thread: the three kept judgments share one instrument (the feeder steps) and one fit; they are separate in their records, covariates, figures and members, and the sentence that names the fit leaves each construction to do, but a run that builds the whole fit with the reach done by system lands all three. The hardware and replaced-unit terms are named or one-join covariates once the fit exists, so the judgment that prices this build is whether a run commits a pooled apportioning at all when a clean unit-level sample and three official records sit beside it.
