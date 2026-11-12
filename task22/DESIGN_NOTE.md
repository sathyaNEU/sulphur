# task22: where Delmont Power and Light's 2027 revenue protection sweep goes, and what its lines and transformers will lose in 2027

Architecture 1, drawn 2026-11-12, the first draw after the client's closed strategies page
(`guidelines/client/learning-modules/overused-strategies-2026-11-12.md`): every lesson in the chain is off it.

## Draw

Subdomain: Energy Systems & Utilities, distribution losses and the feeder energy balance (house task type
  distribution-losses-energy-balance; the client's nearest task types are load forecasting and grid reliability)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a bridge that reconciles two totals: each feeder's energy in, month by month from October 2023 to
  September 2026, carried to what its customers' meters recorded, the city's unmetered lights and own use, the lines'
  and transformers' losses and what is left (the non-technical loss), with the utility's line loss rise between the
  twelve months to September 2024 and the twelve months to September 2026 bridged to its causes; the four feeders the
  2027 sweep covers sit on top
Weight: assembly: one energy balance for fourteen feeders built from systems that count different things on
  different clocks (the wholesale delivery point meters by substation and hour, the feeder breakers' telemetry by
  feeder and hour with its gaps, customer reads on twenty billing cycles and at month ends, today's GIS against a
  switching log in two naming schemes, deemed lights, the transformer register), where the technical term is
  itself a network computation; the last two live builds put theirs on a fitted model (task7 v10) and on its checks
  (task20 v2)
Data-native sentence: nothing meters a feeder's theft or its own losses, so each is what is left of a balance whose
  terms come from systems that each see part of it: the breaker telemetry sees the feeder but goes dark in the
  storms when crews are moving customers between feeders, the delivery point meters see every hour but only by
  substation, the GIS knows where every load sits today but not who was on which feeder last winter, and the 2019
  loss study knows the network's losses at 2019's loads, before the licensed grows and the cold store connected at
  the far ends of the longest feeders.
People: drawn with `guard.py names --geo us --seed 2207`: Dustin Jones (the utility's engineering manager, who asks;
  not named in the prompt), Heidi Hester (the consulting engineer who wrote the 2019 loss evaluation study).
Decision: before the City of Delmont's 2027 utility budget closes, the engineering manager names the four of the
  fourteen feeders the revenue protection contractor sweeps in 2027 (the contract funds four), ranked by the
  non-technical loss each carried in the twelve months to September 2026 (the last month whose meter reads were
  all in when the extracts were pulled on November 2 to 5), and the technical losses the 2027 power cost budget carries; forward-facing (the sweep and the losses are
  2027's).

Card: `.claude/skills/fingerprint/cards/task22.json`, architecture v1, registered 2026-11-12T14:48:55Z at WARN.
Redrawn at filing: the forum (board of directors, then executive team, to the line manager: the sweep is the
engineering manager's call inside the budget the council passes), the organisation family (a cooperative and a
utility both repeat task7 v10 and task13 v4 in the window; the city-owned utility is a local government department,
which is what public power is) and the question form (which, the last prompt's form, to where: the sweep is a place
on the network). The two WARNs are answered here: line_manager_or_team decides in seven builds, the honest forum for
an operational sweep; a spreadsheet and a PDF memo repeat task13 v4's deliverable set (a Word memo would repeat
task20 and task7's, the set at 24 per cent of recent prompts), and a one-page memo the utility director forwards to
the council's budget file goes as a PDF.

## Deep reasoning

Task type: distribution-losses-energy-balance (Energy Systems & Utilities, house task type serving ETL; the client's
  nearest task types are load forecasting and grid reliability): a feeder energy balance conformed from the systems
  that each see part of it, whose residual is the quantity wanted.
Domain test: every result is a quantity a distribution utility's loss and revenue-protection engineers compute: each
  feeder's energy in at the breaker closed against the wholesale delivery point, the customers each feeder served
  month by month, the unmetered lights' real use, technical losses as the square of each segment's current at its
  loads' positions plus transformer core and copper losses, the non-technical residual, the line loss bridge, new
  connections' demand and next year's technical losses.
Swap: "rank the water zones by non-revenue water" keeps the balance's skeleton (input, metered, unbilled authorised,
  apparent and real losses), but real losses follow pressure, not the square of the flow through each shared main,
  so the deciding judgment (a loss that is a convex function of where the load sits on the path) has no counterpart,
  and a demand factor of grows against their applied lighting load stops meaning anything.
Where the weight sits: R4 and R1 to R2: the technical term is a network computation on loads placed at the nodes of
  the tree that served them each month, and the balance it closes needs the breaker energy rebuilt for the hours the
  telemetry missed and every customer on the feeder that served it; each piece is long because the record each
  needs is a second system at another grain (the delivery point meters by substation, the switching log by device,
  the GIS by segment, the reads by cycle).
Layer 1: the historian's hour-beginning local clock against the delivery point's hour-ending standard time (the
  November hour twice, the March hour skipped); communication failures blanking hours on every feeder, a North RTU
  outage on all four North feeders for an afternoon, and APT-2's transducer stuck for 52 hours in August 2025 with
  good quality; AMR reads on twenty business-day cycles with estimated reads trued up later, AMI meters read at
  midnight on the first, meter exchanges with a final and an initial read, register rollovers and CT multipliers,
  vacant premises billed to the owner's account; the CIS extract pulled in two runs overlapping by a day; the OMS's
  pole-tag device names before its July 2024 upgrade and a crosswalk keyed by hand that missed about one switch in
  eight (each recoverable from the GIS pole tags); LED conversions billed at the old lamp's deemed kWh; net-metered
  customers with delivered and received registers. None decides a result on its own: R1 and R2 grade the assembly.
Not one thing: three corrections each move the four, and the four needs all of them: placing load where it sits on
  the network (R4), the switching log replayed (R2) and the storm gap rebuilt from the delivery point (R1); every
  single correction and every pair of them on the careful pass files a wrong four (forcing routes, computed), and
  the bridge (R6), the new connections' demand (R7) and 2027's losses (R8) each need their own work beyond them.
One-fact test: the most useful single sentence is "the GIS shows today's network; the switching log moved customers
  between feeders"; it rescues R2 alone (1 of 9), because the four still needs the gap and the positions; each of the
  other three hints (the delivery point covers every hour the breakers missed; technical losses follow the square of
  each segment's current where the loads sit now; new connections draw what comparable members draw) rescues one
  result (computed: effort.json hints, each run as the careful pass with that one correction).
Not semantics: every field, code and clause read correctly (the clocks, the read types, the multipliers, the lamp
  codes, the scope's definition) still leaves the breakers' missing hours to carry, today's GIS to read for the
  history and the study's percentages to apply, each filing a different four.
Not rule application: the scope of work files what a non-technical loss is and that the four with the largest are
  swept; the budget instructions file the base year and what 2027 adds; no filed procedure fills a breaker gap,
  places a load on the network, replays a switching log or estimates a connection's demand.
Estimand: the RFP scope A.2 and A.3 (non-technical loss on a feeder: the energy that entered it at the breaker and
  from customers' generation, neither recorded by a customer's meter, used by the City's unmetered lights, nor lost
  in its conductors, transformers and secondary and service conductors; the four with the largest in the twelve
  months ending September 30, 2026); the budget instructions 1 and 2 (the base year's months standing for 2027's, only
  approved connections from their service dates and approved works from their in-service dates, no weather
  adjustment); the prompt (the monthly balance's columns and window, customers served at month end, the bridge
  between the two twelve-month windows on the utility's own line loss, the peak hourly demand each approved 2027
  connection adds, each feeder's 2027 technical losses).
No decoy: nothing is written to carry a wrong answer: the 2019 loss study is the consultant's correct computation of
  2019's losses at 2019's loads by its own stated method (an incumbent figure, reproduced exactly by R18's reflex and
  superseded by the network computation at 2026's loads); the line loss report states the utility's own basis
  truthfully and R6 reproduces it; no memo ranks feeders.
No replay: no result re-derives a published figure; R6's two line loss percentages tie to the utility's report as a
  check, and the split is computed.
Pinned: every rival a careful analyst could defend is run on the cut pack and files the golden four (forcing,
  computed): load placed by each node's twelve-month rather than monthly energy, each read period spread evenly over
  its days rather than by the substation's daily energy; and the four holds under conductor resistance at 25 C, plus
  5 per cent, transformer losses 10 per cent either way, burning hours 5 per cent lower and substation transformer
  losses 20 per cent higher. Load placed by transformer rating (the study's load-flow convention for unmetered
  loads) files APT-3 for CHL-3 and is ruled out by named data: every transformer's customers are metered, and their
  meters put the nodes' average load between 0.08 and 0.32 kW per kVA of transformer rating (10th to 90th
  percentile, asserted), so a rating says little about where the load sits.
Run forecast: a strong run loses R1 by dismissed own evidence (the breakers' gaps carried at the feeder's own average
  while the delivery point shows the substation's full energy for those hours), R2 by dismissed own evidence (today's
  GIS for the whole history, the switching log set aside when its old device names fail to join), R4 by a method
  shortcut (the 2019 study's percentages or its equivalent resistance at 2026's current), R5 and R9 by an unfinished
  chain (the residual on those three), R6 by stopping at the first story (the rise read as theft), R7 by a method
  shortcut (the applied load as the demand) and R8 by dismissed own evidence (the base year's loss rate carried to
  2027); R3 is earned.
Strategy label: OWN (no client strategy carries a feeder energy balance; the client's emissions-table ETL strategy is
  the nearest by analysis type and shares no step).
Depth level: 5 on the client's scale: four independent judgments each move a graded figure (the breaker gaps from the
  delivery point, the switching log replayed, technical losses at the loads' positions, the new connections'
  measured demand), the call needs the first three together, and fourteen shortcut routes land on five different
  wrong fours.
Lesson: a residual that the physics must close is only as good as every term subtracted before it, and the largest
  term here is a convex function of where the load sits on a changing network: carried at an old study's percentage
  or equivalent resistance it misreads the network's own losses as theft wherever load has grown at the far end, and
  the residual also needs each hour's energy in rebuilt where the feeder's own meter was dark and each customer on
  the feeder that served them; no build on file closes a physical balance whose biggest term must be recomputed on
  the network.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each feeder's energy in at the breaker with the telemetry's missing hours rebuilt: CHL-3 1,340.5 MWh in January 2026 and 12,232.6 for the twelve months to September 2026, the fourteen feeders 248,001.4 | assembly-reconciliation | the delivery point meters and the substations' transformer and station service sheets; the scope's energy in at the breaker | CHL-3 January within 3 per cent, twelve months within 0.6 per cent; fourteen feeders within 0.12 per cent | dismissed own evidence: the gaps carried at the feeder's own average for the hour (CHL-3 January 1,033.6, twelve months 11,866.2) while the delivery point shows the substation's full energy for those hours | - | Component 3 |
| R2 | who each feeder served month by month and what their meters recorded: NTH-4 374 customers at the end of March 2026 and 441 at the end of May; NTH-4's meters 9,377.7 MWh and NTH-3's 6,707.5 in the twelve months | assembly-reconciliation | the OMS switching orders, the device crosswalk and the pole tags, the GIS network; the prompt's customers served at month end | counts within 3; metered use within 1.5 per cent | dismissed own evidence: today's GIS feeder for every month (NTH-4 440 in March, 9,871.9 MWh), the switching log set aside when its old device names do not join | - | Component 2 |
| R3 | the city's unmetered lights' real use in the twelve months to September 2026: 874.1 MWh, against 1,145.7 billed at deemed kWh | missingness-measurement | the lighting inventory's lamps and conversion dates, the engineering tables' input watts and burning hours, the lighting bills; the scope's lights | real use within 4 per cent | method shortcut: the deemed kWh on the lighting bills as their use (1,145.7) | - | Ask 3 |
| R4 | each feeder's technical losses at its loads' 2026 positions: APT-3 1,786.6 MWh, APT-4 1,189.0, the fourteen feeders 13,002.6 (5.24 per cent of their energy in) | modeling | the GIS segments and conductors, the 2019 study's conventions (resistance at 50 C, single-phase taps, secondary at 0.7 per cent), the transformer register and loss tables | APT-3 and APT-4 within 7 per cent; fourteen feeders within 4 per cent | method shortcut: the 2019 study's percentage of each feeder's 2026 energy (APT-3 832.9) or its equivalent resistance at 2026's current, the load still placed where it stood in 2019 | R1 | Component 1 |
| R5 | each feeder's non-technical loss in the twelve months to September 2026: CHL-2 1,310.4 MWh, APT-4 1,121.9, NTH-4 700.3, CHL-3 698.9, NTH-3 502.7, APT-3 456.6 | decomposition-attribution | the scope A.3; R1 to R4 | each within 75 MWh or 9 per cent, whichever is wider | unfinished chain: the residual on today's GIS, the gap at the average and the study's percentages (APT-4 1,573.9, APT-3 1,402.8, CHL-2 1,335.3, NTH-3 977.3) | R1, R2, R3, R4 | Ask 1 |
| R6 | the rise in line loss on the utility's own basis from 7.74 per cent (twelve months to September 2024) to 8.24 (to September 2026): technical losses +0.44 points, non-technical +0.30, everything else -0.24 | decomposition-attribution | the prompt's two windows; purchases at the delivery points and sales on bills issued in each window | each line loss within 0.05; each part within 0.10 points | stopped at the first story: the rise read as theft, technical losses held at the study's percentage (technical +0.02, non-technical +0.56) | R1, R4 | Component 4 |
| R7 | the peak hourly demand each approved 2027 connection adds: LL-2026-433 521.6 kW, LL-2026-722 931.4, LL-2026-964 541.2 | modeling | the large power interval meters and the applications (the connected grows' peak hourly demand over their applied load, 0.745; the cold store's own, 0.660) | each within 5 per cent | method shortcut: the applied load as the demand (700, 1,250 and 820 kW) | - | Ask 4 |
| R8 | each feeder's 2027 technical losses: APT-4 1,720.9 MWh, APT-3 1,694.1, the fourteen feeders 13,455.3 | forecasting | the budget instructions 1 and 2; today's network, the CWP reconductor from March 15, 2027, R7's demand at the connected grows' hourly shape | APT-4 and APT-3 within 7 per cent; fourteen feeders within 3 per cent | dismissed own evidence: the base year's technical loss rate carried to 2027's energy with the applied loads (APT-4 889.5, APT-3 960.3, fourteen 11,105.3) | R4, R7 | Ask 5 |
| R9 | the four feeders the 2027 sweep covers: CHL-2, APT-4, NTH-4 and CHL-3 (NTH-3 next at 502.7 MWh, 196.2 below CHL-3) | synthesis | the scope A.2 | exact set | unfinished chain: the careful residual's four, APT-4, CHL-2, APT-3 and NTH-3 | R5 | Recommendation |

Carry-forward: R1, R2, R3 and R7 stand on inputs of their own (the delivery point and the breakers; the switching log
and the GIS; the lights' inventory and bills; the interval meters and the applications); R4 needs R1's breaker energy
for its current; R5 falls with any of R1 to R4, R9 with R5, R6 with R1 and R4, R8 with R4 and R7. A run that slips on
the topology keeps R1, R3, R4 and R7; one that slips on the gap keeps R2, R3 and R7; one that keeps the study's
percentages keeps R1, R2, R3 and R7.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| load grown at the far end of long feeders (licensed grows since 2019, a cold store in 2025) | constructed (the simulated connections, each with its application) | no: new large loads on six feeders at positions from 0.3 to 0.95 of the main, two deciding (APT-3 in, CHL-3 out under the study's percentages), the rest moving nothing | modelling: each month's metered load placed on the GIS network and the equivalent resistance recomputed | modelling | keep |
| switching that moved customers between feeders (two permanent transfers, two construction ties, the storm tie, planned maintenance) | constructed (the simulated switching orders) | no: every substation; the March 2024 NTH-2 transfer, the IND and APT construction ties and the storm move numbers without moving the four, the April 2026 lateral moves it | a targeted query and a replay: the OMS log linked to the GIS through the crosswalk and the pole tags, the network traced hour by hour | modelling (a network replay) | keep |
| the breakers' telemetry missing in storms and comm failures | constructed (the simulated historian) | no: random gaps on every feeder, a four-feeder North outage, a stuck transducer on APT-2; only CHL-3's storm gap moves the four | a targeted query: the breakers' sum against each delivery point, hour by hour | modelling: the substation balance with its transformer losses and station service | keep |
| LED conversions billed at the old lamp's deemed kWh | constructed (the simulated lighting programme) | no: every feeder with street or area lights; it moves no feeder in or out | a targeted query: the inventory's conversion dates against the bills' lamp codes | routine | keep, R3 only |
| illegal grows on rural feeders | constructed (the estimand itself) | no: sites on every feeder, most on the rural ones | it is the residual | modelling | keep |

precut's WARN on the LED row is answered by its verdict: routine by construction and kept to R3; with the lights at
their deemed kWh the four stands, 200.8 MWh clear of the fifth (asserted in checks.py).

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 each feeder's energy in, the breaker metering's missing hours rebuilt | Missed | Missed | Right |
| R2 who each feeder served, month by month, and what their meters recorded | Missed | Missed | Right |
| R3 the unmetered lights' real use against their deemed kWh | Partly | Right | Right |
| R4 each feeder's technical losses at its loads' positions | Missed | Missed | Right |
| R5 each feeder's non-technical loss, twelve months to September 2026 | Missed | Missed | Right |
| R6 the rise in line loss bridged to its causes | Missed | Missed | Right |
| R7 the peak hourly demand each approved 2027 connection adds | Missed | Missed | Right |
| R8 each feeder's technical losses in 2027 | Missed | Missed | Right |
| R9 the four feeders the 2027 sweep covers | Missed | Missed | Right |
| Roughly | 0.5 of 9 | 1 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the passes are the generator's own routes on
  the cut pack: the quick pass the breakers as they come with no technical losses on today's GIS; the careful pass
  every file conformed with today's GIS, the gaps at the feeder's average, the 2019 study's percentages and the
  applied loads; the golden)
Largest single hint: "The GIS shows today's network; the switching log moved customers between feeders."; rescues 1 of 9
  results
Pair estimate: 20.8 (the careful pass earns R3 and the instruction-following share; every lost cell cites a
  precedent of its own class)

## Data provenance

Source: generated by task22/generator from a simulated municipal distribution system (seed 22061): hourly weather,
  fourteen radial 12.47 kV feeders from four substations with their segments, switches and ties, 9,000 customers on
  their transformers with class load shapes, solar, AMR and AMI meters, large power loads, permitted and illegal grows,
  street and area lights, the switching orders and outages, the flows and losses of every segment hour by hour, and
  each recording system's export.
Behaves like the real thing: the energy balance closes exactly in the truth (breaker energy against every load and
  loss, asserted); losses on each segment are its resistance times the square of its current, so long rural feeders
  run at 4.9 to 10.3 per cent technical losses (the longest with load at their ends highest) and town feeders at 3.5
  to 4.3, system 5.2 per cent,
  as distribution utilities report; transformers lose their core losses every hour in service; AMR meters run
  slightly slow until exchanged; illegal grows light at night; billing cycles follow business days.
Genuine patterns: (1) temperature-driven load with winter heating on electric-heat feeders and summer cooling (2) load
  growth from licensed grows and a cold store on rural feeders, and solar on town feeders (3) a January ice storm and
  summer heat waves (4) customer turnover with vacant premises (5) the AMI rollout feeder by feeder (6) the LED
  programme district by district (7) planned maintenance outages and unplanned outages by cause
Problems by process: the historian's local clock and the delivery point's standard time; communication failures,
  including a four-feeder RTU outage and the storm; a stuck transducer; estimated reads on drive-by routes; meter
  exchanges; register rollovers and CT multipliers; the CIS extract run twice over a day; the OMS's device names
  changing at its upgrade with an incomplete crosswalk; lights billed at codes the conversions never updated.
Breadth: 22 files (four large CSVs of 111,072 to 388,752 rows, ten workbooks and PDFs, three distractors: the outage
  record, the wholesale rate schedule and the airport's daily weather), fourteen feeders, 1,056 primary segments,
  9,022 service points and 3,137 transformers, so deciding which records close each feeder's balance is work.

## Template check

Chain signature: assembly-reconciliation, assembly-reconciliation, missingness-measurement, modeling,
  decomposition-attribution, decomposition-attribution, modeling, forecasting, synthesis
Question form: where (where the 2027 sweep goes)
Nearest build: task13 v4 (Energy, grid reliability: automated restoration's avoided interruptions, feeders and
  transfers in its setting) and task14 v3 (ETL, a register completed from a panel): task13 prices what an automatic
  action changed across the network against its own log; this build closes an energy balance whose largest term is
  recomputed on the network; task14 completes optional change records from a survey; neither recomputes a physical
  loss on a changing network or fills a meter's gap from the conservation of energy. Abstraction sentence: none
  writable against either.

## Frontier check

Precedents: R1 N10 (missing periods carried at the observed rate); R2 N09 (today's topology for all history), N14 (a
  second record set aside once its linkage failed); R4 L22 (the published formula whose generating assumption the
  data contradict), L36 (a transfer fitted on the old range carried to a new one); R5 L11, L32; R6 L26, L27; R7 L15
  (a response assumed, not measured); R8 N13 (the latest rate as the state at the decision date), N01 (an enlarged
  load assumed to scale in proportion); R9 L11.
Shallow path checks: R1: the careful fill reconciles every feeder's twelve months to within a fraction of a per cent
  of its average and shows no blank hours; only the substation balance hour by hour (the delivery point file, another
  grain) exposes the storm's missing energy. R2: today's GIS keeps every substation's total right and every month's
  residual positive on NTH-3 and NTH-4; only the switching log replayed on the network (another grain: device
  operations) moves the lateral. R4: the study's percentages reproduce the study's own 2019 figures exactly and give
  a plausible 4.3 per cent system loss; only the segments' currents at 2026's node loads (the GIS and the reads)
  show APT-3's losses doubling. R6: the theft story matches the sweep's motivation; only R4's losses for both windows
  split it. R7: the applications' connected loads are filed figures; only the interval meters of the connected grows
  show the demand. R8: the base year's rate is the latest; only the network with the new loads and the reconductor
  gives 2027's.
Assumption made false: that technical losses scale with energy (N01, and the runs' "losses taken as a fixed share"):
  false here because the new load sat at the far end of the longest feeders, where losses grow with the square of a
  current carried furthest; the pack tests it through the GIS segments, the applications' locations and the reads by
  transformer. And that today's network held for the whole history (N09): false because the switching log moved a
  lateral in April 2026 and the storm tie moved CHL-2's customers in January; tested by the OMS log against the GIS.
Forcing: the line is the fourth feeder's non-technical loss (CHL-3, 698.9 MWh) against the fifth (NTH-3, 502.7), a
  margin of 196.2; the golden family (three variants) files the golden four; all fourteen shortcut routes file another
  four (five distinct); conductor resistance at 25 C and plus 5 per cent, transformer losses 10 per cent either way,
  burning hours 5 per cent lower and substation losses 20 per cent higher all leave the four standing.
Noun swap: the nearest skeletons on file (skeleton.py check: task14 v3, task19 v1, task15 v2, task4 arch 10) share no
  lesson, mechanism, decision form or answer pattern; swapped into task13 v4 (feeders, transfers) the deciding move
  (a loss recomputed on the network at the loads' positions) has no place, and its lessons (a downstream offset, a
  validation that cannot see the condition) none here; severity none.
Closed strategies: the call turns on nonlinear_functional_of_path (losses with the square of the current at the
  loads' positions), off the client's closed page; the nearest card, "The pooled effect does not transfer to a target
  with a different mix", differs in mechanism and fix: the loss is not an effect estimated on one population and
  reweighted to another's mix, it is a physical quantity recomputed segment by segment on the network, non-separable
  across loads (a load's loss depends on every other load sharing its path). The chain keeps no closed lesson as a
  supporting step (skeleton.py closed task22: 0 of 5 closed); the time-varying membership, the conservation fill and
  the measured demand are open too.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | non-technical loss on a feeder | energy in at the breaker plus customers' generation less what meters recorded, the city's lights and technical losses; the breaker energy less billed sales | the scope's definition | RFP scope A.3 |
| SF2 | the twelve months | October 1, 2025 to September 30, 2026; the bills issued in that period | the calendar window | RFP scope A.2 ("in the twelve months ending September 30, 2026") and the prompt |
| SF3 | what customers' meters recorded | the meters' delivered kWh spread over the days they cover; the kWh on bills issued in the month | the days they cover | the prompt's monthly balance (energy and use in the same month); same call on the twelve months |
| SF4 | customers' generation | the received register on net-metered services; nothing | the received register | RFP scope A.3 ("from customers' own generation") |
| SF5 | the city's lights | their real use at their lamps' input watts and burning hours; the deemed kWh billed | real use | RFP scope A.3 ("used by the City's unmetered street and area lights") |
| SF6 | technical losses | conductors, transformers and secondary and service conductors; conductors only | all three | RFP scope A.3 |
| SF7 | the conductor resistance | at 50 C; at 25 C | at 50 C | the 2019 study's convention; same call (forcing: 25 C keeps the four) |
| SF8 | a single-phase tap's loss | six times the three-phase expression; the phase conductor alone | six times | the 2019 study's convention (phase and neutral) |
| SF9 | secondary and service losses | 0.7 per cent of energy delivered to services; computed | 0.7 per cent | the 2019 study's convention |
| SF10 | where a node's load sits in a month | the tree that served it that month; today's | the tree that served it | the scope's "entered the feeder"; the switching log |
| SF11 | customers served at month end | service points connected on the last day whose node the feeder served at midnight; accounts billed | connected service points | the prompt's "customers served" |
| SF12 | the line loss | purchases less sales on bills issued in the window, over purchases; the balance's losses | the utility's basis | the line loss report's stated basis and the prompt's "line loss" |
| SF13 | the rise's parts | substations, technical, non-technical, lights, billing, the last three as "everything else"; a shift-share | the parts as shares of purchases, which add to the line loss in each window | the prompt's "came from": parts that add to the rise (asserted) |
| SF14 | a connection's peak hourly demand | its applied load at the share of applied load comparable connected customers draw at their own peak hour; its applied load | the measured share | the prompt's "will add" (what the connection draws, not what it applied for); the interval meters |
| SF15 | the cold store expansion's comparable | the cold store's own share; the grows' | its own | same call within 5 per cent; the only comparable cold store is itself |
| SF16 | 2027's technical losses | the base year's months standing for 2027's on today's network with approved connections and works; a trend | the budget instructions' basis | budget instructions 1 and 2 |
| SF17 | a connection's start | its scheduled service date; the application date | the service date | budget instructions 2 |
| SF18 | the reconductor | from its in-service date; all year | from March 15, 2027 | budget instructions 2 and the CWP |
| SF19 | the four | the four largest non-technical losses; the largest per mile or per customer | the four largest | RFP scope A.2 |
| SF20 | a breaker hour two feeders missed together | the substation's residual split by their shares in the same hour of adjacent days; dropped | split | same call: the North RTU's afternoon (June 11, 2025) lies outside both twelve-month windows and carries under a quarter of one per cent of any North feeder's year (asserted), so it moves no graded figure |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the fourteen feeders; every service point, large power account and light the network served |
| 2 | Unit of account: the feeder, by the hour for energy in and by the day for metered use |
| 3 | Attribution window: a load counts on the feeder whose breaker served its node that hour (SF10) |
| 4 | As-of dating: the extracts of October 27 to November 5, 2026; the twelve months end September 30, 2026 |
| 5 | Version basis: one extract per system; the CIS's overlapping day kept once |
| 6 | Denominator: line loss over purchases (SF12); technical per cent over energy in |
| 7 | Weighting: none; energies summed |
| 8 | Window length: twelve calendar months (SF2) |
| 9 | Boundary inclusivity: a month runs from midnight on the first, local time |
| 10 | Rounding path: hourly kWh summed at full precision, MWh shown to 0.1, points to 0.01 |
| 11 | Tie-break: none needed; the fourth and fifth are 196.2 MWh apart |
| 12 | Maturity and censoring: every read covering September 2026 is in the extract (the last AMR cycle reads on October 28, the AMI reads on October 1) |
| 13 | Order of operations: conform the clocks, fill the breaker gaps, replay the network, place the loads, then subtract |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: the CIS rows repeated by the overlapping pull are exact copies, kept once |
| 16 | Identity normalisation: OMS devices to GIS switches by the crosswalk, else by the pole tag; service points to transformers to nodes by the GIS |
| 17 | Netting against gross: customers' received energy adds to energy in; nothing is floored |
| 18 | Dimensional units: MWh for energy, kW for demand, per cent and points for line loss |
| 19 | Code and status semantics: read types, lamp codes and rate codes as each system writes them |
| 20 | Integerisation: customer counts whole |
| 21 | Clause scope: the scope's definition applies to every feeder alike; the budget instructions to every feeder's 2027 |
| 22 | Forward window contents: 2027 adds the three approved connections, the subdivision's first lots on NTH-1 near its substation and the APT-3 reconductor; nothing else |

## Literal reader

Executing the scope A.2 and A.3 and the budget instructions word for word: each feeder's non-technical loss is its
breaker energy and its customers' generation less what its customers' meters recorded, the city's lights and its
technical losses, over the twelve months ending September 30, 2026, and the four largest are swept; 2027's technical
losses are the base year's on today's network with the approved connections and the reconductor. A reader who takes
the breakers' readings as they come, today's GIS and the study's percentages files APT-4, CHL-2, APT-3 and NTH-3,
against A.3's "lost in the feeder's own conductors" and "entered the feeder"; none of those is another reading: each is
an easier method on the same filed estimand.

## Prompt contract

A voice rewrite keeps: the question (where the 2027 sweep goes, four feeders, ranked by the energy each lost to theft,
tampering and other unmetered use in the twelve months to September 2026); why it must be estimated (nothing meters
theft or the lines' own losses); the utility's line loss figures (7.7 and 8.2 per cent); the monthly balance from
October 2023 to September 2026 with its columns; the bridge between the two twelve-month windows into technical,
non-technical and everything else; the peak hourly demand each approved 2027 large connection will add; each feeder's
2027 technical losses; a spreadsheet and a one-page PDF memo. It never adds a rounding instruction, a method (no delivery
point, gap, interpolation, switching log, GIS, topology, transfer, position, square, resistance, study, demand factor,
interval data or reconductor), a warning, an attached file's name, a role, or a count the data hold.

## Pre-ship check

- Bar re-read on the built pack: nine results across six areas (assembly and reconciliation, missingness and
  measurement, modeling, decomposition and attribution, forecasting, synthesis), each pinned by a filed sentence (RFP
  2026-14 A.2 and A.3, the budget instructions 1 and 2, the 2019 study's conventions) and the data, with the bands the
  answer blocks state; precut 93 checks, 0 FAIL, 1 WARN (answered in the Hidden factor record); checks.py 106 of 106;
  verify.py PASS on its own path; two rebuilds byte-identical.
- Hidden factor record against the cut data: load added since 2019 sits on six feeders at 0.3 to 0.95 of the main
  (APT-3 loses 1,786.6 MWh where the study's percentage gives 832.9); switching in every substation, the April 21
  lateral carrying 494.2 MWh of NTH-3's metered use; breaker gaps on all fourteen feeders (each more than 20 hours),
  CHL-3's storm gap 306.9 MWh in January (1,340.5 against 1,033.6 at the average); unbilled LED conversions on ten or
  more feeders, the four standing with the lights at deemed kWh (200.8 clear); illegal grows on every feeder.
- Effort test against effort.py: quick 0.5 of 9 (13.9), careful 1 of 9 (20.8), thorough 9 of 9; the largest hint
  rescues 1 of 9; fourteen shortcuts land on five different wrong fours. Caution on the paper estimate: the judge's
  thread, which read the graded blocks before deriving, reproduced R7's two demand ratios (0.745 and 0.660) exactly;
  priced Right in the careful column on that showing, the pair estimate reads 34.6, still under 50.
- Forcing: the line is CHL-3's 698.9 MWh against NTH-3's 502.7, a margin of 196.2 (their bands, 623.9 to 773.9 and
  427.7 to 577.7, do not meet); the golden family's three variants and six perturbations keep the four.
- Determinism judge (one pass, on the cut before the stage 4 fixes): DETERMINISTIC, APPROVE; Gate G
  method_or_model_selection, analytical_non_defect, no surface-read dependency; Gate H passes (one thing none, the best
  hint one correction of three). Its thread opened the graded blocks before deriving, so its first pass is not a cold
  read and prices the careful column no further than R7 above; it reproduced the line loss levels, the study's APT-3
  percentage, both demand ratios, the storm gap to the hour, APT-2's 52 stuck hours and the April transfer, and left
  R2, R4 and R5 to the author: verify.py rebuilds them on its own path on the final cut (NTH-4 374 and 441, APT-3's
  technical losses within 0.1 per cent, the six feeders' non-technical losses within 2 per cent, the same four). The
  stage 4 fixes moved no method and no estimand, and every stage 3 gate re-ran on the final cut.
- Leak: leak.py REVIEW only (--asof 2026-11-05: the CWP's 0.6 miles, the field's own words in the study, RFP and
  budget, the OMS's Device column and the approved connections' 2027 service dates, each ruled harmless in the
  report). Two isolated reads at medium effort: the first found the meters left on AMR naming three of the four (fixed:
  CHL-3 moved into the May 2026 phase, IND-3 left for the third) and the applications' numbering changing pattern in
  2026 (fixed); the second, on the final cut after a document and the prompt changed, found no leak and no realism
  defect, and its three points are closed forks (SF5, SF19) or the fixed split.
- Gate WARNs answered: precut's LED row (Hidden factor record); heart's overuse.forum and repeat.deliverables (Draw).
- Containers: audit_containers exit 0 on the pack and the golden, re-run on both zips as the last command before the
  commit.

## Tried and rejected

- 2026-11-12, at filing: a rural electric cooperative as the organisation (Ketchum Prairie Electric Cooperative):
  both its honest organisation families repeat the last three builds (task7 v10 a cooperative, task13 v4 a utility),
  so the same balance moved to a city-owned utility, where theft, far-end grows and deemed lights are as common.
- 2026-11-12, stage 3: the window to October 2026 with the extracts pulled on December 2: the pack's files ran past
  the day it ships (breaker data to November 30, the GIS export dated November 25), a dated tell; the world moved back a
  month to the twelve months to September 2026 with the extracts of November 2 to 5, the simulation and the hourly
  files from September 2023 and the reads from August 2023, so every bill in the first window carries simulated use
  (a cut with the reads starting in September had written late cycles' first bills as register-only reads, dropping a
  month of their sales from the first window and turning the rise into a fall), the weather on a stream of its own,
  and NTH-3's theft target lowered from 566 to 480 MWh to hold the fourth-to-fifth margin (197.6).
- 2026-11-12, stage 4: the leak reader found the three feeders without AMI (APT-4, CHL-2 and CHL-3) were three of the
  golden four, with the CWP naming the same three for AMI's third phase: one group-by and one PDF line gave a prior on
  three names. The rollout moved CHL-3 into the May 2026 phase with NTH-4 and APT-3 and left IND-3 for the third, so
  the meters left on AMR are APT-4 and CHL-2 (in every route's four) and IND-3 (seventh), and the pattern says nothing
  about the contested places; the AMI dates draw from a stream of their own, CHL-3's theft target rose from 577 to
  610 MWh to hold the margin (196.2), and the large load applications are numbered in each year's order received
  (the approved 2026 three had read LL-2026-01 to 03 against three-digit numbers everywhere else).
