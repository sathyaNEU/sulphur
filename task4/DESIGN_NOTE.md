# task4: how many battery-electric buses to order for the Niittylä depot's weekday blocks in 2027, and which blocks they take

## Draw

Subdomain: Regression, classification & model diagnostics (General Statistics & Data Science; house domain Supply Chain & Logistics, a bus operator's depot electrification)
Analysis type: Forecasting & Predictive Modeling
Answer shape: A schedule under capacity (the weekday blocks a battery-electric bus can take, each with its design-day energy against the limit, scheduled under the depot's night charging capacity in the plan's priority order, with what each qualifying bus takes from the installation that night and the count that comes out)
Weight: a hard-to-measure quantity: each weekday block's battery energy on the design day for buses that have never run it, where the six pilot buses ran only the blocks the planner picked from the fuel figures, the pilot's battery record leaves out the heat its fuel-fired heaters supplied, and the block's difficulty survives only in the diesel fleet's fuel-card statement; beside it, what a bus on charge takes on a -15 C night, which the charging sessions carry only mixed with the recharge; task16 sits on investigation and task17 on modeling
Data-native sentence: the pilot's telematics carry one energy figure per bus-day for nine thrifty blocks, the fuel-card statement carries every block's diesel use only as litres between fills of buses that rotate over the blocks, and the charging system meters each session's energy as one figure in UTC, so the quantities the order turns on exist in no file and have to be built from three records joined over the dispatch log and the weather.
People: Simo Virta, the electrification programme manager, whose workbook and slides the golden are and who signs the standard; Eveliina Pajunen, the fleet manager, the connection agreement's addressee; Juhani Nousiainen, the dealer's key account manager, who signs the quotation; Kaarina Peltola, the distribution company's connection engineer (`guard.py names --geo Finland --seed 1004`). None appears in the prompt.

Architecture 10, 2026-11-10, a new world after architecture 9 (the Fryele tractor order, the fifth architecture in that
world) was landed by both platform runs (`runs/arch9/`): every estimate it priced was a per-unit mechanism one file's
plot or one join carried, and the record of six runs in that world says what beats them is evidence in a file they
dismiss on its face, a structure across files nothing names, a count over many units in which small sign-consistent
biases accumulate, and selection in which units reached the training record. Loop 1 (2026-11-10, the platform's
holistic audit): the order count was not forced (the workshop's two 22 kW outlets beside DES-1 3.2's "in the periods
the agreement gives it" let M124 in, 19 for 18) and three asks read two ways; the four forks are closed by WHAT pins,
and with the heater fix alone already landing the old count (18), a third independent judgment is built on the
charging side (the conditioning a bus on charge draws on a cold night), which moves the order to 17.

## Deep reasoning

Task type: Regression, classification & model diagnostics (General Statistics & Data Science), serving Forecasting & Predictive Modeling: each weekday block's 2027 battery energy on the January design day, forecast from a six-bus pilot that ran a selected ninth of the blocks, held against a limit that is itself an estimate (the usable battery after the first winter) and a night capacity shared by the blocks ordered, whose draw per bus on a -15 C night is itself estimated from the charging sessions.
Domain test: the results are a forecast carried from a sample selected on the outcome's own determinant (the planner put the pilot on the blocks with the lowest diesel use, so the pilot's covariates cannot identify the between-block effect and the old technology's consumption record is the measurement of it: a selection-on-observables problem whose observable sits in another file); a measurement gap in the pilot's own record (heat the pilot took from fuel that the new buses take from the battery) read from a second record; a degradation share from state-of-charge logs with its form chosen by fit; a metered total split into its two causes (the recharge over the charger's efficiency and a steady draw over the released hours that rises in the cold) and the cold part carried to a night colder than most of the record; and a capacity constraint over the forecasts that turns sign-consistent per-block shortfalls into buses. A careful statistician defends each as a statistical judgment; none is subject-matter arithmetic with a label.
Swap: "how many community nurses to hire for the clinic's rounds, from the pilot team's visit times" keeps a forecast from a pilot but loses the fuel-card statement that carries each round's difficulty, the fuel-fired heater whose share the new units take from the battery, the state-of-charge logs, the charger meters that mix the recharge with the battery's conditioning, and the night supply; the count stops making sense.
Where the weight sits: R4, the 48 design-day energies, which take the longest work: the diesel rate per block has to be rebuilt tank to tank over the dispatch log (R1), the pilot's own record split into a per-km rate by block and a per-hour cabin draw by temperature, the heaters' share read from the HVO fills against the register's rating and the quotation's heating spec (R3), and the bridge from the diesel rate to the pilot's per-km rate fitted over the 49 blocks an electric bus ran and carried to the 39 it never ran. Beside it R7: every session's metered energy put on local time, given its evening, its released hours (21:00 to 07:00) and its night's temperature, the battery's gain read from the bus's own day, and the meter's energy split into the recharge and a steady draw by a fit whose knot is chosen by fit. None of it is clever; all of it is long, and every piece ends in a figure that can be checked.
Layer 1: the fuel-card provider caps a transaction at 250 litres and the night shift swipes again for the rest; eight cards were reissued mid-period and three spare cards are used with the fleet number typed at the pump; odometers are typed with slips and blanks; the dispatch log changed its block codes with the planning system on 11 August 2025 and exported registrations instead of fleet numbers in its first two months; the telematics portal uploaded four May days twice and the buses' ambient sensor drops out; the airport station has a three-week gap in April 2023 the town station covers; the charging sessions are stamped in UTC across two summer-time changes a year and a session plugged in after midnight belongs to the evening before; the depot pump was out for a week in August 2025 and every fill went to a street station; six old buses were withdrawn in June 2025. Each is produced by its process, asserted neutral in `checks.py` (SF5 to SF10, SF31) and none decides a result.
Not one thing: three independent judgments each move the order and each is graded on its own figure. The bridge (the pilot's selection on the fuel figures) put right alone, with the heaters already read, gives every energy and every verdict and still orders 18 at the sessions' pooled ratio (effort.json hint 1); the conditioning put right alone orders 17 of a different set (M106, M111 and M132 in, M125, M129 and M135 out); leaving out only the heaters' share orders 19; the verdicts summed order 23; each result is graded on its own and the chain lands only when all of them do.
One-fact test: the most useful single sentence ("the pilot blocks were chosen for their low diesel use, and the diesel figures carry the difficulty the timetable's kilometres, climb and speed miss") rescues 3 of 9 results (R2, R4 and R6) on the careful pass, which then still orders 18; the conditioning's sentence rescues 1 (R7, the order still wrong on the careful energies); the heaters' and the night's sentences none (the careful pass, graded up, already reads both). Agrees with `effort.py`.
Not semantics: every field read right (the statement's litres and timestamps, the dispatch log's codes and kilometres, the telematics' energy and HVAC columns, the sessions' UTC stamps and metered energy, the register's heater line, the quotation's heating and battery thermal management rows) still leaves the pilot's fit carried on its covariates and the night charged at the sessions' pooled ratio; nothing filed says the pilot blocks were picked for their fuel figures, that the pilot's battery record leaves out the heaters' heat, how much a bus on charge draws beside its recharge on a cold night, or that the night cuts the list below the blocks that pass.
Not rule application: DES-1 files the WHAT (2.1 the block, 2.2 the block's energy, 2.3 the usable battery less the first winter's loss from the company's own buses, 2.4 the design day and the design night, 3.2 depot charging on the charging lane under the connection agreement, the installation's draw as its chargers take it session by session, 3.3 fuel per 100 scheduled km, 4.1 the 85 per cent rule, 4.2 the priority list cut at the first block the night cannot recharge, 4.3 one bus a block); the agreement files 690 kW from 21:00 to 07:00; the quotation files 480 kWh usable, all-electric heating with boosters below -10 C and the battery's thermal management from the charger as on the 2025 buses; the register files the heaters' 35 kW at 3.9 l/h; the fleet plan files the pilot buses' move to Kauppala. Nothing filed names a bridge, a selection, a deconvolution, an age form, a conversion of litres to heat, a split of the metered energy, a temperature knot or a schedule.
Estimand: DES-1 2.1 to 2.4, 3.2, 3.3 and 4.1 to 4.3 with the quotation's 480 kWh and the agreement's 690 kW: population the 48 weekday blocks of the 2027 fleet plan (all of them, none observed under the 2027 model), outcome each block's traction-battery energy depot out to depot in, window a January working day at a daily mean of -15 C at the airport station and the night after it at the same mean, unit kWh and buses, comparison each block against 85 per cent of 480 kWh less the share the company's own buses lose in their first twelve months, then the priority list cut at the first block the night period cannot recharge with those above it; the diesel figures over November 2025 to October 2026 per 100 scheduled km; the night draw at the connection point (what the chargers take) with every qualifying block's bus on charge.
No decoy: no memo, draft or stakeholder figure; the fleet plan ranks the blocks by the city's zone priority, not on any energy or decision basis; the quotation's warranty (70 per cent at eight years) is a floor, not a first-year figure; no file states a block's design-day energy, a per-km rate, a heating load, a loss, a charger efficiency, a conditioning draw or a count.
No replay: no result re-derives a published figure and no stated number in the pack is wrong.
Pinned: run on the cut pack and the clean truth (`checks.py`, 178 assertions; `verify.py` on its own code path): the diesel rates by least squares over fill intervals mapped by timestamp, by date, with and without the second swipes merged, 48 of 48 within 0.7 of each other; the per-km rate bridged on the diesel figure alone, with the hours per km, or for every block, every energy within 10 kWh and the same order; the station's temperature in place of the sensor's, within 8 kWh; the loss over curved, square-root, log and straight-line age forms 2.99 to 4.91 (band 2.7 to 5.0, every form inside and none moving a verdict); the heaters' heat from the fills at the register's rating (4.3 kW), the public lower heating value at 84 to 92 per cent (3.9 to 4.4), both inside 3.9 to 4.7; the conditioning at -15 C with the night's temperature as the mean of the evening's and the morning's (3.46), the evening's alone (3.32), the morning's alone (3.11), the bus's own sensor (3.36), the knot at 0, 5 or 10 C (3.23, 3.46, 3.08), all inside 2.8 to 4.2 and each landing the night inside its band and the same 17; a fit with no standing draw (2.86 kW at 0.934, worse fit) and a loss that scales with the recharge instead of the hours (0.868 at -15 C, residual 4.41 against 4.06) both land the night inside the band and the same 17; the battery's gain on the fitted fade curve with or without its cold term, or on 480 kWh less the first-winter loss, lands the conditioning inside its band and the same 17, the bare 480 kWh implying a charger efficiency over 0.98 (SF42); the night by the exact flow between the blocks' returns and departures, a least-slack schedule, the period's energy and 10 or 20 minute plug-in margins all cut at the 18th, the 17 holding with the night's draws 3 per cent higher and the 18th fitting only with them 2.5 per cent lower; the conditioning as a steady load or as flexible energy, the same 17; no block within 26 kWh of the limit in the truth and 18 in the golden.
Run forecast: R1 earned (the runs reconstruct the fuel figures for the business-case ask, a reconciliation they do by reflex); R2 lost to dismissed own evidence (the fuel-card file set aside for the forecast because litres do not measure battery energy, so the pilot blocks are never set against the rest); R3 earned on the careful column (graded up: a leak reader noticed the heaters on a read) and lost by any run that reads the pilot's own HVAC record at -15 C or fits the HVO fills on a textbook degree-day base; R4 lost to a method shortcut (the pilot's fit carried on kilometres, climb and hours per km, the hard blocks 33 kWh light on average); R5 earned (a curved age form is the runs' first move); R6 Partly (42 of 48 verdicts); R7 lost to a method shortcut (the sessions' pooled ratio, 0.920, read as the charging efficiency: a year of mostly mild nights averages the conditioning into one figure); R8 falls with R4 and R7 (29 blocks at the pooled ratio, 10.9 MWh); R9 Partly (18 against 17, the set sharing 15).
Strategy label: WORKS IN FORM (a forecast carried from a selected sample to the population through the old technology's own record, beside a measurement gap read from a second record, a metered total split into its causes with the cold part carried to the design night, and a capacity constraint over the forecasts).
Depth level: 5. Three independent judgments each move the count (the bridge: 18 without it at the pooled ratio, 17 of another set with only the conditioning right; the heaters' share: 19 without it; the conditioning: 18 without it), the night's capacity moves it from 23 to 17, and the first winter's loss sets the limit the verdicts are read against; the shortcuts land on nine distinct wrong answers over nine routes (effort.json routes), the careful pass orders 18 and the quick pass 33, and the honest family (three bridges, two temperatures, three age forms, six readings of the charging split, three schedulers) lands the 17 every time.
Lesson: a pilot whose units were chosen on the old technology's own record carries that record's information in its selection, so the forecast for the unselected units is identified by the old record and not by the covariates the pilot's data show; a load the pilot took from a second source is invisible in the pilot's own meter; a meter that mixes two loads with different causes has to be split by those causes before either is carried to a condition the record rarely saw; and a capacity shared across many forecasts turns shortfalls too small to see per unit into whole units. No build on file teaches the first three.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each weekday block's diesel use over November 2025 to October 2026, litres per 100 scheduled km (37.2 to 62.4; 48 cells) | assembly and reconciliation | DES-1 3.3; the fuel-card statement's fills tank to tank over the dispatch log's bus-days, by least squares over the intervals (the second swipe merged, the spare cards by the typed fleet number) | each within 0.7 of the golden (the timestamp, date and unmerged readings within 0.7 of each other) | method shortcut: each fill charged to the block run on the fill's day (30 or more blocks off by over 0.7), or every block given its commonest bus's yearly rate | - | Ask 1 |
| R2 | the pilot blocks' diesel use against the rest: 46.2 against 49.1 l/100 km, a gap of 2.9; the thriftiest half of the 33 blocks of 225 km or less on the 2024 timetable | causal reasoning | R1's rates over the nine blocks with 30 or more electric weekdays against the other 39 | gap within 1.0 | dismissed own evidence: the fuel-card file set aside for the forecast because litres do not measure battery energy, so the comparison is never made and the selection never stated | R1 | Component 1 |
| R3 | the heat the pilot buses' fuel-fired heaters supplied at -15 C: 4.3 kW (0.48 l/h of HVO at 35 kW for 3.9 l/h) | missingness and measurement | the electric buses' HVO fills on the statement tank to tank against the days' hours and temperatures (48 intervals), the register's heater rating, the quotation's all-electric heating below -10 C; the fault weeks in the workshop log, with the boosters capped, give 7.1 to 8.0 kWh a litre | 3.9 to 4.7 kW | narrow look at broad data: the pilot's own HVAC record read at -15 C (8.4 kW) and the fills never read as cabin heat, or the fills fitted on a textbook degree-day base (the careful column is graded up: Right) | - | Component 2 |
| R4 | the 48 design-day energies for the 2027 model, nearest 10 kWh (290 to 490) | forecasting | DES-1 2.2 and 2.4; the per-km rate outside HVAC by block, bridged from R1 over the 49 blocks an electric bus ran (slope 0.0309, residual 0.024 kWh per km), plus hours out times 12.4 kW (the pilot's 8.1 and R3's 4.3) | each within 10 kWh (the bridge with hours per km, the bridge for every block and the station's temperature all inside) | method shortcut: the pilot's fit carried on kilometres, climb and hours per km, the hard blocks 33 kWh light on average, 31 of 48 cells outside | R1, R3 | Ask 2 |
| R5 | the first-winter loss of usable battery, 4.3 per cent (usable 459.2 kWh for planning) | modeling | DES-1 2.3; each electric bus-day's energy over its state-of-charge drop on age with a cold term and a level per bus, a form with a fast early loss chosen by fit | 2.7 to 5.0 (every age form a fit could take, a straight line in age included at 2.99; no reading inside it moves a verdict) | self-confirming check: the quoted capacity taken as usable, no loss at all (the quick pass); the careful pass earns it | - | Ask 4 |
| R6 | each block's verdict against 390.3 kWh (23 qualify) | synthesis | DES-1 4.1 with the quotation's 480 kWh and R5 | exact per block (partial credit from four fifths of the blocks: an all-electric answer gets 23 of 48) | unfinished chain: 29 qualify on the careful pass's energies (42 of 48 verdicts right) | R4, R5 | Ask 3 |
| R7 | what a bus on charge takes through its charger beside the recharge on the design night: 3.5 kW for every hour on charge in the night period (0.45 kW plus 0.150 kW a degree below 5.0 C), with the recharge into the battery at 0.948 of the meter | modeling | DES-1 2.4 (the design night) and 3.2 (the installation's draw as its chargers take it, session by session); the quotation's battery thermal management from the charger as on the 2025 buses; 3,280 sessions with a rise of 30 points or more, on local time, against the battery's gain from the bus's own day, the released hours and the night's temperature, the knot chosen by fit | 2.8 to 4.2 kW (the six readings of the fit span 3.08 to 3.46) | method shortcut: the sessions' pooled ratio, 0.920, taken as the charging efficiency, no draw beside the recharge, so each qualifying bus's -15 C night is about 20 kWh light | - | Component 3 |
| R8 | the design night's draw at the connection point with every qualifying block's bus on charge: 9.1 MWh (8.4 the recharge, 0.7 the conditioning over 7.7 to 10.0 hours a bus), against 6.90 MWh the night period gives | synthesis | DES-1 2.4, 3.2 and the agreement's 690 kW from 21:00 to 07:00; R4, R6 and R7 | within 0.3 MWh (the readings of the charging split within 0.2) | unfinished chain: 29 blocks at the careful pass's energies over the pooled ratio, 10.9 MWh; the golden's own energies at the pooled ratio 8.7 MWh, outside the band | R4, R6, R7 | Ask 5 |
| R9 | the order: 17 buses for M101, M107, M108, M113, M116, M119, M122, M123, M125, M129, M134, M135, M137, M140, M142, M146 and M148 | synthesis | DES-1 4.2 and 4.3: the priority list cut at M145, the 18th, which the night cannot recharge with the 17 above it (the exact flow falls about 180 kWh short between the blocks' returns and departures with each bus's steady draw held over its window; the least-slack schedule recharges the 17) | exact (the honest family lands the 17 under three bridges, two temperatures, six readings of the charging split and three schedulers) | unfinished chain: 18 on the careful pass (29 without the night), 18 with the bridge alone at the pooled ratio, 17 of another set with the conditioning alone, 19 without the heaters' share, 23 with the verdicts summed, 19 on battery energy | R4, R5, R7 | Recommendation |

Carry-forward: R1, R3, R5 and R7 stand on their own inputs (the statement over the dispatch log; the HVO fills with the register and the quotation; the telematics' state of charge; the sessions with the weather and the bus's own day). R2 falls with R1 only if the rates are wrong by more than the gap, which no hurried read of R1 achieves on the pilot blocks alone. R4 falls with R1 or R3, R6 with R4 (and R5 only where a block sits between the two limits, which none does on this pack), R8 with R4, R6 or R7, and R9 with R4 or R7. No analytical result is the sole ancestor of more than half of the others (R4 of R6, R8 and R9; R7 of R8 and R9); a run that gets the energies right and the charging split wrong, or the reverse, still loses R8 and R9 by its own figures, which is the AND the chain is built on.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| the pilot's blocks were picked by the planner from the 2024 fuel figures among the short blocks, so the pilot's covariates (kilometres, climb, hours per km) miss the difficulty the chooser selected on (stops, dwell with the doors open, loads), which survives in every block's diesel use (the stand-in blocks are the next three on the planner's list) | constructed as the planner's process (a dispatch simulation over 48 weekday and 48 weekend blocks, every bus rotating) | no: the hurried fit is light on every hard block the pilot never ran, the ones far over the limit included (asserted: 5 or more blocks 40 kWh or more over the limit under-forecast by 15 kWh or more, where nothing turns), and the gap shows in the weekend blocks the decision never covers | a targeted comparison across two files (each block's diesel figure, itself rebuilt tank to tank over the dispatch log, against the pilot's), then modelling (a bridge from the diesel rate to the pilot's per-km rate over the 49 blocks an electric bus ran, carried to the 39 it never ran) | modelling (a bridge between two technologies' records, estimated, carried, and checked against the blocks with their own electric days) | keep: one of three, rescues 3 of 9 |
| the pilot buses' fuel-fired cabin heaters carried the heat above the small heat pump's capacity below about -3 C (the fit's enable point -2.5), so the pilot's battery record flattens in the cold while the 2027 model, all-electric with boosters below -10 C, takes that heat from the battery | constructed as the heating system's physics on every pilot bus-day (a capacity, a heat pump range, a fuel heater enabled below a set point) | no: the share sits on all 48 blocks (hours out times 4.3 kW, 35 kWh or more on each), on every winter day of the pilot, and in the 48 HVO fill intervals across both winters | modelling: the HVO fills on the statement tank to tank against the days' hours and temperatures, converted at the register's heater rating, read beside the quotation's heating spec; confirmed on the two buses whose heater the workshop log shows out | modelling (a load the pilot's own meter never saw, estimated from a second record and carried to the new units' physics) | keep: one of three (the careful column graded up, so its sentence rescues none) |
| a bus on charge takes a steady draw through its charger beside the recharge while the relay releases the chargers (the 24 V system, the BMS and the outlet's standby, and the battery held at its charging temperature below a 5 C night), so the charger's meter mixes two loads with different causes and the sessions' pooled ratio averages the cold one over a year of mostly mild nights | constructed as the battery's thermal management on every session (a standing draw, a slope below a set point, the released hours) | no: every one of the 3,291 sessions carries it, every cold night most, and the night's cut moves with it on every route's energies | modelling: each session on local time with its evening, released hours and night's temperature, the battery's gain from the bus's own day, the meter's energy split by a fit with the knot chosen by fit, then carried to each block's own window on a -15 C night | modelling (a metered total split into its causes and the cold part carried past most of the record) | keep: one of three, rescues 1 of 9 |
| the night supply shared over the buses ordered, so that per-block shortfalls too small to flip a verdict accumulate into buses (the verdicts summed give 23, the night 17) | filed (the connection agreement's 690 kW in the night period; DES-1 4.2) and the blocks' own returns and departures | no: every qualifying block is scheduled; the cut moves with every route's energies and charging split (routes land on 17 to 23 under it) | an exact schedule over the night (a maximum flow over the intervals with each bus's steady draw held, or a least-slack order), which three readings agree on and an earliest-departure heuristic misses by less than the 18th's shortfall | modelling (a feasibility computed over all the blocks taken together, never a per-block check) | keep: moves the count by six against the verdicts summed |
| the first winter's loss: fast in the first months, steady after | constructed as battery physics on all six buses, each with its own level | no: every bus's curve; the loss shows at every age | modelling (an age form chosen by fit on the state-of-charge logs, net of the reversible cold) | modelling | keep, earned by careful runs (sets the limit; on this pack no block sits between the limits with and without it) |
| the buses rotate daily over the blocks and fill every second or third night, so no block's fuel is ever observed directly | constructed as dispatch practice over every bus-day and every fill | no: all 48 weekday and 48 weekend blocks | a join and a deconvolution (least squares over the fill intervals against the blocks' kilometres between them) | modelling (a reconstruction, not a lookup) | keep, earned by careful runs (the assembly result R1) |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 diesel l/100 km per weekday block (48 cells) | Missed | Right | Right |
| R2 the pilot blocks' diesel gap to the rest, l/100 km | Missed | Missed | Right |
| R3 the fuel heaters' heat at -15 C, kW | Missed | Right | Right |
| R4 the 48 design-day energies | Missed | Missed | Right |
| R5 first-winter loss of usable battery, per cent | Missed | Right | Right |
| R6 each block's verdict | Missed | Partly | Right |
| R7 the conditioning draw on charge at -15 C, kW | Missed | Missed | Right |
| R8 the design night's draw with every qualifying block on charge, MWh | Partly | Missed | Right |
| R9 the order: the count and the blocks | Partly | Partly | Right |
| Roughly | 1 of 9 | 4 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (generator/effort_passes.py runs each pass end to end on the cut pack)
Largest single hint: the pilot blocks were chosen for their low diesel use, and the diesel figures carry the difficulty the timetable's kilometres, climb and speed miss; rescues 3 of 9 results (R2, R4 and R6; the order then still 18)
Pair estimate: 49.5

The careful column is graded up against the run record (`analysis.careful`): every file cleaned, crosswalked and
joined; the diesel rates tank to tank by least squares for the fuel ask (R1 right); the pilot's energy per km by
block and its HVAC draw per hour by temperature; the fuel heaters' heat read from the HVO fills once the register's
heater line and the quotation's heating row are set side by side (R3 right: a leak reader noticed the heaters on a
read, so the column assumes a careful run reaches the fills); the pilot's fit carried to the 39 blocks it never ran
on climb and hours per km; the first-winter loss on a curved age form (R5 right); the charging losses as the
sessions' pooled ratio (0.920); the night scheduled exactly on those figures. It orders 18 (M106, M111 and M132 in,
M125 and M135 out, so R9 Partly), passes 29 blocks (42 of 48 verdicts, R6 Partly), files 10.9 MWh for the night and
31 of 48 energies outside their bins. Under the column the earlier design used (the fills never read as heat), the
pair would be about 37; the 49.5 is the conservative figure, and the platform's grading of a count and a 48-cell
verdict list as wholes would put it lower. The quick pass (the pilot's mean energy per km on days at or below -5 C
times each block's kilometres against 85 per cent of 480 kWh, the night as battery energy) orders 33 and scores
19.5. Executed hints: the bridge put right on the careful pass rescues R2, R4 and R6 and orders 18 (the night still
at the pooled ratio); the conditioning put right rescues R7 and orders 17 of another set; the heaters' and the
night's sentences rescue nothing, the careful pass already applies both.

Pre-ship check (2026-11-10, loop 1, the final cut 8bb29ac7): the bar re-read against the built pack. The hidden factor record against the cut data: the pilot's selection shows on every hard block the pilot never ran (`checks.py` R5: five or more blocks 40 kWh over the limit under-forecast by 15 kWh or more, where nothing turns); the heaters' share sits on all 48 blocks and in 48 HVO intervals over two winters; the conditioning sits in every one of the 3,280 fitted sessions and every reading of the fit, every capacity basis for the gain but the bare 480 kWh, and every band edge land the same 17 (SF27, SF32 to SF36, SF42); the night's cut moves with every route's energies and charging split (17 to 23). The effort test against `effort.py`: quick 19.5, careful 49.5 (graded up on the heaters), thorough 100.0, the note's table and pair estimate the measured ones, the largest hint 3 of 9. The isolated reads: the loop 1 leak reader (no process sentence, no helper file, no one thing; three realism lines fixed in the generator) and the judge's passes 8 to 11 (pass 8 not counted, its order broken; pass 9 FIX_NOW on the loss band and ask 1, fixed; pass 10 APPROVE voided by the main thread's capacity-basis fork, fixed as SF42; pass 11 DETERMINISTIC APPROVE on 8bb29ac7, order kept), recorded in `determinism_check_report*.md` and `leak_check_report.md`. The free gates green on the final cut (`gates.py task4`: precut 84 of 84, effort, voice, leak REVIEW only, figures, containers, heart WARN, surface; checks 178 of 178, verify, two byte-identical builds).

## Data provenance

Source: generated by task4/generator from a simulated process (sim.py, pack.py, docs.py), seed 41007; Finnish naming and bus-industry vocabulary, every organisation, place, person, vehicle and record invented.
Behaves like the real thing: a 12 metre bus's energy per kilometre rises with climb and with the block's difficulty (stops, dwell with the doors open, loads) and its cabin heat demand with the cold; a diesel bus burns fuel by the same block physics with an idle draw per hour and a fuel-fired heater below the engine's waste heat; a battery-electric bus heats with a small heat pump whose coefficient falls to one at -10 C and a fuel-fired heater above its capacity, loses usable capacity fastest in its first months, shows less on cold days and gets it back; the dispatcher rotates buses over blocks with day-to-day persistence; the night shift fuels buses when under half a tank and swipes twice when the pump stops at 250 litres; the chargers put 94.5 per cent of what they take into the battery, and while the relay releases them each plugged-in bus draws a standing 0.35 kW and more as the night falls below 5 C to hold its battery at charging temperature.
Genuine patterns: (1) seasonal temperature with persistence at two stations and a bus-sensor offset; (2) energy per km rising with climb and difficulty, cabin draw rising with the cold then flattening on the pilot at its heat pump's capacity; (3) diesel use by block spanning 37 to 62 l/100 km with bus-level efficiency and a cold-engine penalty; (4) the pilot's blocks selected from the 2024 fuel figures among the short blocks, with three stand-in blocks and the weekend blocks beside them; (5) capacity fade fast then steady, bus by bus, with a reversible cold effect; (6) fills every second or third night at the depot and now and then at street stations; (7) heater fuel rising with the cold below about -3 C on the electric buses; (8) workshop visits at each bus's own rate, with two heater faults in the winter of 2025/26; (9) the sessions' metered energy per kWh into the battery rising on cold nights and with the hours a bus stays on charge.
Problems by process: a 250 litre cap and second swipes, reissued and spare fuel cards with the fleet number typed, odometer slips and blanks, block codes re-keyed at the planning system change, registrations in the dispatch log's first two months, telematics days uploaded twice, ambient dropouts, a station gap, UTC session stamps across summer time, a week of street fills while the depot pump was out, six buses withdrawn mid-period.
Breadth: 14 files; the fuel-card statement holds 20,803 transactions on 60 vehicles and 71 cards; the dispatch log 41,790 bus-days over 96 blocks; 3,315 electric bus-days and 3,291 charging sessions; 3,957 station days; 841 work orders; the block register's 96 blocks and 28 lines; two distractors (tyre and brake costs by vehicle, the depot's electricity invoices).

## Template check

Chain signature: assembly-reconciliation, causal-reasoning, missingness-measurement, forecasting, modeling, synthesis, modeling, synthesis, synthesis
Question form: how many (the order's size, with the blocks it takes), the fuel figures, the energies, the verdicts, the loss and the night's draw asked as their own quantities
Nearest build: task4 architectures 5 to 9 (the Fryele tractor order, the same assigned pairing): there a per-unit physical model carried through covariates and estimates a plot or a join showed; here the pilot's units were selected on the old technology's record, the correction is a bridge through a file the runs dismiss, the heaters' share is a structure across three files, the charger's meter mixes two loads that have to be split before the cold one is carried to the design night, and the count is capped by a shared night supply (a different answer shape, a different weight, no declared weight, no calibration line, no speed). Against other builds, task16 (a ranked list under a cap, investigation) and task10 (forecast bands, validation) differ in shape, weight and chain; the abstraction sentence against any build on file other than this slot's own lineage cannot be written. Guard WARNs answered: overuse.weight (hard-to-measure sat in task5 four builds ago; the quantity here exists in no file and is the honest label), repeat.gate_g (forecasting is the assigned analysis type), repeat.deliverables (a workbook and slides are what a board gets), repeat.question_form (a count asks how many).

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | the design day | -15 C daily mean at the airport station, or the coldest day on record | -15 C | DES-1 2.4 (asserted) |
| SF2 | the pilot blocks | the nine weekday blocks with 30 or more electric days, or every block an electric bus ran | the nine | the three stand-in blocks have 1 to 9 electric days; the gap is stated over the nine (asserted: the thriftiest half of the short blocks, none among the ten thriftiest or the hardest sixteen of the 48) |
| SF3 | the limit's arithmetic | 85 per cent of 480 less the loss share, or 85 per cent of 480 | less the loss | DES-1 2.3 and 4.1 (asserted) |
| SF4 | the diesel figure's kilometres | the dispatch log's scheduled km, or the odometer | scheduled | DES-1 3.3 (asserted) |
| SF5 | the old block codes | mapped to the register's current codes, or the old-coded months dropped | mapped | same call: the reference year and the pilot's weekdays run on the new codes; the old months dropped move no energy by more than 10 kWh (asserted) |
| SF6 | the telematics days uploaded twice | once, or twice | once | same call, no energy moves by more than 8 kWh (asserted) |
| SF7 | the night shift's spare cards (the AdBlue purchases, the vehicle typed at the pump) | to the vehicle by the typed fleet number, or dropped | to the vehicle | same call: they carry no diesel, so dropped they move no block's figure (asserted) |
| SF8 | a second swipe within minutes | merged into the fill, or a fill of its own | merged | same call, within 0.7 (asserted) |
| SF9 | a fill's bus-days | by the fill's timestamp against departures, or by date | timestamp | same call, within 0.7 (asserted) |
| SF10 | a bus-day's temperature | the bus's sensor filled from the airport station, or the station throughout | sensor | same call, within 8 kWh (asserted) |
| SF11 | the heaters' fuel | the HVO fills on the electric buses' cards, tank to tank | the fills | 48 intervals (asserted); no other record carries it |
| SF12 | litres to heat | the register's 35 kW at 3.9 l/h, the public lower heating value at a burner efficiency, or the fault weeks (8.0 and 7.1 kWh a litre, the boosters capped at 12 kW) | the register's rating | the rating and the public value inside 3.9 to 4.7 kW; the fault weeks a confirmation of the order of magnitude, not a figure (asserted) |
| SF13 | the battery's thermal management from the charger | block energy, or the installation's draw | the installation's draw, not block energy | DES-1 2.2 (mains energy at the depot is not block energy) and 3.2 (the draw is what the chargers take, session by session); the quotation (asserted) |
| SF14 | the careful pass's own count | its energies and the pooled ratio under the night give 18, not 17 | 18 | the hurried pass is graded on its own figures (asserted) |
| SF15 | the bridge's form | the diesel rate alone, or with the hours per km | either | same call, within 10 kWh, the same order (asserted) |
| SF16 | the bridge's reach | every block bridged, or the pilot blocks on their own electric days | own days | same call, within 10 kWh, the same order (asserted) |
| SF17 | the pilot blocks' verdicts | bridged or on their own days | either | no verdict changes (asserted) |
| SF18 | the loss's age form | curved (early loss plus a line), square root, log, or a straight line | curved | every form inside 2.7 to 5.0, the straight line at 2.99 too (it runs under the first months' fast loss); no form moves a verdict or the order (asserted) |
| SF19 | the loss's rounding | 4.3 to 0.1 | 4.3 | mid-band (asserted) |
| SF20 | the night draw | every qualifying block's recharge over the chargers' efficiency plus its steady draw over its window, at 0.1 MWh | 9.1 | stated at 0.1; the bridge variants and the station temperature within 0.3, the readings of the charging split within 0.2 (asserted) |
| SF21 | a block at the limit | none within 26 kWh in the truth, 18 in the golden (the 10 kWh grading tolerance and the rounding stay on one side) | clear | asserted |
| SF22 | "cannot recharge" | the exact flow over the night's intervals between the blocks' returns and departures with each bus's steady draw held (the standard's words), a least-slack schedule, the period's energy, an earliest-departure heuristic, or 10 or 20 minutes allowed at plug-in and departure | feasibility (the flow, exact windows) | the flow, the least-slack schedule and the period's energy all cut at the 18th, with 10 or 20 minute margins too; earliest-departure leaves the 17 short by under 1.5 per cent and the 18th by more than twice that (asserted) |
| SF23 | the cut's margin | the 17 hold with the night's draws 2 per cent higher (3 measured); the 18th fits only 2 per cent lower (2.5 measured) | as filed | asserted |
| SF24 | the usable battery | the quotation's 480 less the first winter's loss, or 480 | less the loss | DES-1 2.3; with 480 no block changes side on this pack (asserted), the loss is graded as its own ask |
| SF25 | the night's energy | at the connection point (the chargers' draw), or battery energy | connection point | the prompt and DES-1 3.2; battery energy alone orders 19 and the pooled ratio 18 (asserted) |
| SF26 | the order's size | the priority list cut by the night, or the verdicts summed | cut | DES-1 4.2; the verdicts summed give 23 (asserted) |
| SF27 | the graded bands' edges | the heaters' heat at 3.9 or 4.7 kW, the loss at 2.7 or 5.0 per cent, the conditioning at 2.8 or 4.2 kW | the golden mid-band | every edge lands the same 17, and the heat and loss edges the same verdicts (asserted) |
| SF28 | "the town's weather station" | the airport series (DES-1 2.4 names it) or the town-centre series, for the sensor dropouts and the heater fit | airport | DES-1 2.4; the centre series moves no energy by more than 8 kWh and lands the order, the centre series throughout within 10 kWh (asserted) |
| SF29 | "our own electric buses" | the six pooled, or one bus at a time | pooled | DES-1 2.3 (plural); each bus with a full year in service lands inside the band (asserted) |
| SF30 | the six pilot buses in 2027 | charged at Niittylä on the design night, or gone | gone | the fleet plan's Timetable 2027 sheet moves 1201 to 1206 to Kauppala from 11 January 2027 (the city's 2027 terms exclude fuel-fired heaters); DES-1 4.3 one bus for each block assigned (asserted) |
| SF31 | a session's evening and hours | the plug-in's local evening (UTC put on summer time, a plug-in after midnight on the evening before) and the hours on charge inside 21:00 to 07:00 | as stated | the agreement's relay holds the installation off outside the night period; 3,280 sessions carry a gain from the bus's own day (asserted) |
| SF32 | the night's temperature in the charging fit | the mean of the evening's and the morning's daily means, the evening's alone, the morning's alone, the bus's own sensor; the knot profiled, or at 0, 5 or 10 C | the mean, the knot profiled | every reading inside 2.8 to 4.2 kW, the night draw within 0.2 MWh and the same 17 (asserted) |
| SF33 | a standing draw | a base term beside the cold slope, or none | the base | the fit without it is worse; its night draw stays inside the band and lands the 17 (asserted) |
| SF34 | the cold's form on the meter | a steady draw over the hours on charge, or a loss that scales with the recharge | the hours | the scaling form fits worse (residual 4.42 against 4.07 kWh) and its cold-night residuals rise with the hours on charge; it still lands the night inside the band and the 17 (asserted) |
| SF35 | the hours the steady draw runs | the released hours (21:00 to 07:00), or every hour plugged in | released | the agreement's relay holds the chargers off outside the night period; the plugged-hours fit carried to the plugged hours still lands the night inside the band (asserted) |
| SF36 | the steady draw in the schedule | held over the whole window, or scheduled as flexible energy | held | same call, the same 17 (asserted) |
| SF37 | the workshop's two 22 kW outlets | service charging outside the night period or beside the chargers, or buses under repair | under repair | DES-1 3.2 (charged on the charging lane's chargers; the workshop's outlets are for buses under repair), the agreement (vehicles under repair) and the fleet plan (asserted) |
| SF38 | the design night | the night after the design day at the same mean, or another night | the night after, -15 C | DES-1 2.4 (asserted) |
| SF39 | the installation's draw | what the chargers take from the connection point, session by session, or the battery energy | the chargers' take | DES-1 3.2 (asserted) |
| SF40 | the yes or no | whether the block qualifies under DES-1 4.1, or whether it is assigned | qualifies | the prompt's "whether it qualifies under the standard" (asserted) |
| SF41 | the night's population | every qualifying block, or the blocks assigned | every qualifying block | the prompt's "the bus of every qualifying block on charge" (asserted) |
| SF42 | the battery's gain on charge | its state-of-charge points times the capacity its own day shows, the fitted fade curve with or without its cold term, the quoted 480 kWh less the first-winter loss, or the quoted 480 kWh | the day's own capacity | every reading but the bare 480 kWh lands the conditioning inside 2.8 to 4.2 kW, the night inside its band and the same 17; the bare 480 kWh implies a charger efficiency of 0.98 or more, fits the sessions worst and ignores the loss the company's own buses show (asserted) |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | the 48 weekday blocks of the 2027 fleet plan: filed, fleet_plan_2027.xlsx and DES-1 4.1; the night's population every qualifying block (the prompt) |
| 2 Unit of account | a block, one bus each: DES-1 4.3 |
| 3 Attribution window | a January working day at -15 C daily mean and the night after it at the same mean: DES-1 2.4; the diesel figures over November 2025 to October 2026: DES-1 3.3 |
| 4 As-of dating | extracts to 31 October 2026 pulled 2 to 4 November, the quotation of 6 October: the call reads no later record |
| 5 Version basis | DES-1 version 2 (August 2026), quotation 26-0931, connection agreement 2025-ND-117, the registers as saved in autumn 2026: filed |
| 6 Denominator | 480 kWh usable less the first winter's loss (SF3, SF24); scheduled kilometres for the diesel figures (SF4); the battery's gain over the meter's energy for the chargers' efficiency (SF31) |
| 7 Weighting | each fill interval once in the least squares; each electric bus-day once, blocks weighted by their days in the bridge; each session once in the charging fit; each qualifying block once in the night |
| 8 Window length | twelve months for the diesel figures (DES-1 3.3); twelve months in service for the loss (DES-1 2.3); the night period 21:00 to 07:00 (the agreement) |
| 9 Boundary inclusivity | no more than 85 per cent (DES-1 4.1); no block within 18 kWh of the limit in the golden (SF21); the 18th short by about 180 kWh under the exact flow (SF23, SF27) |
| 10 Rounding path | unrounded to the end; the answer blocks state each figure's precision (diesel 0.1, energies 10 kWh, the loss 0.1 per cent, the conditioning 0.1 kW, the night 0.1 MWh) and its band; the prompt states none |
| 11 Tie-break | none: no block at the limit; the priority list orders the blocks (DES-1 4.2) |
| 12 Maturity and censoring | none: the records are complete to their last day; every bus has served over twelve months by the as-of date except the June 2025 batch, whose first winter is in the record |
| 13 Order of operations | duplicates dropped, cards and codes mapped, fills merged, intervals built, rates fitted, the pilot split, the bridge fitted, energies, verdicts, the sessions split, the night: Step-by-Step |
| 14 Row order | fills by timestamp within a bus (SF9); sessions by plug-in; the priority list in the plan's order |
| 15 Duplicate resolution | a telematics day once (SF6); a second swipe merged (SF8) |
| 16 Identity normalisation | old codes to current (SF5); registrations to fleet numbers; cards to vehicles by validity, spare cards by the typed number (SF7) |
| 17 Netting against gross | the installation's draw is the recharge over the chargers' efficiency plus the steady draw over the window (SF13, SF20, SF39) |
| 18 Dimensional units | kWh, km, l/100 km, kW, MWh, hours; litres per transaction; SOC in whole per cent; UTC stamps on the sessions |
| 19 Code and status semantics | the register's day types; the plan's priority; the workshop's heater fault and repair lines (SF12); the plan's 2027 fleet change (SF30) |
| 20 Integerisation | buses are whole blocks: DES-1 4.3 |
| 21 Clause scope | DES-1 2.1 to 2.4 for the terms, 3.2 and 3.3 for charging and fuel, 4.1 to 4.3 for the call; the agreement for the capacity; the quotation for the model and its battery's thermal management |
| 22 Forward window contents | the 2027 model's usable battery after a year, its all-electric heating, its battery's thermal management as on the 2025 buses, the design day and night, the blocks' returns and departures, the night period, the pilot buses gone: filed or estimated (SF3, SF12, SF13, SF22, SF30) |

## Literal reader

DES-1 2.1 to 4.3 executed word for word: each weekday block's traction-battery energy depot out to depot in on a
January working day at -15 C, against 85 per cent of 480 kWh less the share the company's own buses lose in their
first twelve months (4.3 per cent: 390.3 kWh), 23 blocks; the plan's priority list cut at the first block the night
period's 690 kW cannot recharge with those above it, between each block's return and departure, at up to 150 kW a
bus, the installation's draw being what its chargers take, session by session, so each bus's steady draw beside its
recharge counts: M145, the 18th; 17 buses. The register's "Cabin heating" line is the equipment fitted, the
quotation's heating row the 2027 model's, its battery thermal management row the same system as on the 2025 buses,
the agreement's capacity the installation's draw at the connection point in the night period, the workshop's
outlets for buses under repair (DES-1 3.2, the agreement, the plan). The statement's litres are the fuel bought; the
dispatch log's planned km are the scheduled kilometres; the sessions' energy is the meter's. The prompt's "a bus of
the quoted 2027 model" names the model, not a method; "qualifies under the standard" is DES-1 4.1; "with the bus of
every qualifying block on charge" is the 23.

## Prompt contract

A voice rewrite keeps: the question (how many battery-electric buses to order for the Niittylä depot's 2027 weekday
blocks and which blocks they take, when most of those blocks have never been run by an electric bus: the forecast's
population includes the blocks no electric bus has run), every weekday block's ESTIMATED diesel use over the last
twelve months per 100 scheduled kilometres, a FORECAST from the company's own operating records of the battery energy
in kWh a 2027 bus would use on the standard's design day, whether that forecast qualifies under the standard (never
"goes electric" or "passes"), an ESTIMATE of the first-year loss as a share of usable battery on the company's own
electric buses, a FORECAST of the energy in MWh the charging installation would draw at the connection point on the
design night with the bus of every qualifying block on charge, a workbook and slides for the board. The words
estimate and forecast and "from our own operating records" stay (H20: without them the platform's Domains Fit review
read every ask as a lookup or a certified figure applied to a rule); they name what each result is and the data it
stands on, as DES-1 3.1 does, never the model. It never adds: a rounding instruction, a fuel heater, a bridge, a
selection, a pilot block, a covariate, a schedule, a regression, a tank, a fill, a temperature form, a holdout, state
of charge, battery conditioning, a charging efficiency, a file name, the standard by its code, the capacity figure, a
count of the blocks or the buses, or who is asking.

Leak sweeps answered (leak.py REVIEW lines, 2026-11-10; the third reader's lines: the standard's 2.4 now names the airport station, the outlets line reads as the 2027 to 2029 rollout, the prompt's loss ask is plural like DES-1 2.3, each asserted as SF28 and SF29): the agreement's 690 kW is the filed capacity the prompt's
standard runs on, named in `stated_inputs`; the standard's clause numbers 4.1 and 4.3 are section labels, not the
loss (4.3 per cent) or any figure; the stump-paragraph terms in the standard and the quotation (record, recharge,
temperature, session, register, station; heaters, quotation, capacity) are the organisation's own nouns (3.2's "as the
charging system records it session by session" defines the draw by the meters, the WHAT) and neither document names a
bridge, a selection, a share, a split of the metered energy, a temperature knot or a schedule; the fleet plan's
2027 timetable dates are the plan's own forward dates (a plan for the coming year carries them). The stage 4 reader's lines: the fleet plan's priority column is the city's zone order the standard's 4.2 walks, filed as a fact and not a ranking on any energy, cost or decision basis (Gate G); the plan's outlet count and the quotation's order range were moved off every route's count (32 bays and outlets, four to thirty buses) so no stated figure reads as the answer; the standard's 3.1, 4.1 and 4.2 are the organisation's own rules (the source, the threshold, the order and the cut), the WHAT, and leave every figure they operate on to the analysis.

## Tried and rejected

- 2026-11-10, architecture 10 stage 4, the first judge pass (FIX_NOW): a rank list in component 1 that depended on
  which blocks count as short (out of the blocks; the component states the means and the gap); the 19th block's kWh
  shortfall, whose magnitude depended on the plug-in margins assumed (out of the blocks; the windows are now the
  standard's words, each block's return to its departure inside the night period, the supply rescanned for
  balanced margins under them); M111 within the 10 kWh grading tolerance of the limit (every block now 26 kWh clear in
  the truth and 18 in the golden). The reader's figure 20 (outlets, the quotation's range) moved apart (26 outlets, four to thirty buses).
- 2026-11-10, architecture 10 stage 4, the second judge pass (DETERMINISTIC, one item owed): the heaters' band edges
  propagated to the cut, now asserted (SF27, both bands' edges land the same 18 and the same verdicts, the band half a
  kW either side of the golden); the re-read's realism line (a session starting under zero state of charge): the
  pilot's blocks, stand-ins and weekend blocks now pass the planner's own range check (the pilot buses' 480 kWh as the
  quoted model's), the boosters on a heater-out day capped at 12 kW, no electric day ends under 15 per cent; the
  stand-ins are the next three on the planner's list, so the pilot's record reaches no hard block; the heater fit
  leaves the heater-out days' hours out of its intervals.
- 2026-11-10, architecture 10 stage 3, the night's energy for the recommended buses as ask 5: every route capped by the
  night lands near the capacity's energy (the careful pass's 21 lighter buses sum to the golden's 18), so the figure
  graded nothing; replaced by the night demand of every qualifying block (8.7 MWh against 13.0 on the careful pass).
- 2026-11-10, architecture 10 stage 3, the telematics days uploaded twice in March 2026 (cold days): kept, they halve
  the heater fit's slope through the degree-days without litres and move every energy 7 to 11 kWh; the portal's outage
  moved to May, where the duplicates touch nothing (SF6 asserted within 8 kWh).
- 2026-11-10, architecture 10 stage 3, electric stand-ins on any short weekday block: 37 stand-in days spread over 30
  blocks gave almost every qualifying block its own electric days and the hurried fit nothing to miss; the dispatcher
  now keeps three approved stand-in blocks, so the bridge reaches the hard blocks through them and the weekend blocks
  while the pilot's covariate fit stays light on the 39 blocks it never ran.
- 2026-11-10, architecture 10 stage 3, the pilot's energy model with a per-hour auxiliary term beside block effects:
  kilometres and hours are collinear within a block, the term was unidentified (15.7 kW against 2.2) and every block
  effect biased; the per-km rate by block now carries the auxiliaries, and the diesel rate carries the idle draw the
  same way, so the bridge is one line.
- 2026-11-10, architecture 10 stage 3, charging allowed from the bus's return: the night's windows summed to 17 hours
  and no realistic supply bound the order; the connection agreement's night period (21:00 to 07:00, the load-control
  relay) is the operating arrangement, and the supply scanned at 5 kW steps for balanced margins (700 kW under the exact windows: the 18 hold
  3 per cent up, the 19th fits only 2 per cent down, 10 or 20 minute plug-in margins cut at the same 18, and the heaters'
  band edges leave the 18).
- 2026-11-10, architecture 10 stage 3, the pilot blocks as the thriftiest of all 48: the planner also needs the range,
  so the pick was from the blocks of 225 km or less, and the pilot sits at ranks 11 to 23 of the 48; the component
  states the gap and the ranks among the short blocks as computed.
- 2026-11-10, architecture 10 stage 2, the cold-day selection (the planner keeping the electric buses in on the
  coldest days) as the heating judgment: with fuel heaters the pilot has no range problem on cold days, and a handful
  of cold days the forecast missed would be outliers one residual plot shows; replaced by the heaters' share, which
  sits on every winter day and in a file the runs dismiss.
- 2026-11-10, architecture 10 stage 2, a 2027 timetable that re-cuts the blocks (line-level difficulty decomposed from
  the 2026 blocks): a second attribution the task did not need and a re-keying a solver would read as a trap; the 2027
  blocks are the 2026 autumn timetable's.
- 2026-11-10, architecture 9 (the calibration's transfer to the pilot's part loads, the early-life loss, the winter
  speed, in the Fryele world): both platform runs landed the golden exactly (`runs/arch9/`): run 1 by per-shipper
  calibration carried to each duty's own declarations, a square-root age form and a separate winter driving-time
  model; run 2 by the same with a declaration regime split found from the error itself. Each estimate the design
  priced as a step the runs had named and not taken was a mechanism one file's plot or one join carried. The world is
  left after five architectures; the lesson (what beats these runs is evidence in a file they dismiss, a structure
  across files nothing names, a count over many units, and selection into the training record) is this
  architecture's design.

- 2026-11-10, stage 4 re-judge, a stronger early-life loss so the straight-line loss flips a duty on its own (early
  loss 4.0 to 5.0 per cent over 0.18 to 0.30 years): the limit gap reached only 11.7 to 12.5 kWh against margins of
  10 or more, the curved forms spread 4.2 to 7.0 per cent, and the change would move graded figures after the one
  re-judge; not built. The -5 C speed ratio left the graded components instead (the re-judge thread put it within a
  careful run's reach), every figure unmoved.

- 2026-11-10, stage 4, the combination's tare and the drops as a graded component (R4 at first): the judge flagged it
  as earned by reflex and its isolated thread put a careful pass at 50 to 62 per cent on a grid that counted it
  twice; cut from the graded chain (kept in the model and the workbook), the verdicts' partial credit raised to
  three quarters of the duties; the careful pass 26.8 to 20.8, its design-day-speed variant 46.5 to 42.5.

- 2026-11-10, architecture 8 (three register joins beside the winter speed: the combination's tare by trailer, a
  multi-drop load taken off at its stops, ePTO fridge units drawing by the hour): both platform runs landed the golden
  exactly (order 7; payload 2.24 and 2.23, loss 3.78 and 3.79, every energy within about 3 kWh; `runs/arch8/`). Each
  join was to a register the runs already read, the new export, sheet and quotation line announced the steps, and the
  hourly fridge term made both runs time the design day, which is the winter speed. The judge's warning that the
  careful pass would earn 4 to 5 of 8 was recorded as a caveat instead of a blocker. Re-rooted as architecture 9: the
  fridge draw removed, the work moved into what the runs named and did not test.
- 2026-11-10, stage 2, the declaration practice differing by depot for the same shipper, read from an axle-load or
  gross-weight column in the daily summary: the summary carries no such column, and adding one would be a column that
  exists for the step; replaced by the pilot's part loads, which the pack already shows through each duty's own notes.
- 2026-11-10, stage 2, a battery-management or SOC-window update partway through, tractor by tractor: a timing break
  one residual plot per tractor shows and one indicator fixes (the client's shallow hidden factor, and this note's own
  earlier rejection of a drive-software update); replaced by the early-life loss, a form chosen by fit across every
  tractor.
- 2026-11-10, stage 2, the trailer body's air drag as the between-duty confounder of the payload slope (dense loads on
  low bodies): the tipper and the inloader have no pilot twin, so their drag would be a fork, and a flatbed's drag
  against a box is not physically one-signed; dropped.
- 2026-11-10, stage 2 pricing, the pilot duties at 80 to 93 per cent of the terminal's loads with drag 0.060: the
  careful pass's light-duty flips cleared its own limit by under 2 kWh; at 74 to 90 per cent, drag 0.066 and the
  winter fall 0.0125 a degree they clear it by 5 kWh or more.

- 2026-11-09, architecture 7 (the speed transfer as the deciding step beside the three reflex steps): both platform runs
  (`runs/arch7/run1.md`, `run2.md`, summaries) earned the payload term (1.98, 1.97), the loss (3.75), the cold curve and
  12 of 14 energies, fitted squared routing-tool speed (the year's ratio absorbed) and ordered 5, V14 out at 444.4 and
  443.0 kWh against the 442 kWh limit (golden 435.4). One duty, one judgment, 1 to 3 kWh: a thin level 3, and the
  graded 10 kWh band held both verdicts on V14; run 2 offered the golden's answer as a defensible alternative. Re-rooted
  as architecture 8: three more covariates the pilot's own rows do not show (the combination's tare by trailer, the
  tonne-km of a multi-drop load, the ePTO fridge units), each flipping two duties of its own, and no duty within 13 kWh.
- 2026-11-09, stage 2 pricing, the trailer pools one kind per pilot duty: the tare term (1.6) and the payload term (2.4)
  were confounded between duties and one shared coefficient gave 2.0, a 0.4 spread on R1; mixed pools (a mega on a box
  duty, a forklift on half the building-materials flatbeds) identify the tare within duty and bring the spread to 0.2.
- 2026-11-09, stage 2 pricing, the fridge unit at 3.4 kW: "every reefer draws" moved V33 13 kWh, no flip at a 13 kWh
  margin; at 4.4 kW it flips V30 and V33 clear of the limit.
- 2026-11-09, stage 2 pricing, V11 with two drops (0.56 at 44 per cent of the run): carried to the last drop it moved only
  9 kWh; three drops with a first stop at a fifth of the run move it 18.
- 2026-11-09, stage 2 pricing, the winter ratio at 0.0100 a degree and drag 0.046: the year's ratio moved every energy
  11 to 13 kWh and flipped nothing at a 13 kWh margin; at 0.0120 and 0.054 it moves 12 to 20 and flips V03, V11, V33.
- 2026-11-09, stage 2, a payload elevation term (the loaded leg's net descent): within-duty payload spread times a fixed
  elevation is under 1 kWh against 7 kWh of trip noise, so the term is set by physics constants (an efficiency and a
  regeneration share) the pack cannot pin: a fork, dropped.
- 2026-11-09, stage 2, a 2027 annual electricity figure over a normal year (the convexity of the cold curve): the gap
  between the year's energy at the mean temperature and over the ten-year distribution is about 2.5 per cent, inside the
  honest family's spread; dropped.

- 2026-11-09, architecture 6 (three estimates each moving the order: the payload term under declaration error, the
  sub-zero cold curve, the first-year battery loss net of the cold): the platform's run 1 landed the call and every
  graded figure (13 of 14 energies in their bin, 2.0 and 3.8 exact). It corrected the declarations by their measured
  error variance, kept a temperature quadratic on its fit, and regressed energy per full charge on age, temperature
  and tractor: each step a reflex for a frontier run once the asks named the quantity. Its own assumptions list named
  the gap it left untested: "Energy scales linearly with route distance ... the new round trips are 266-355 km,
  compared with 202-241 km for the pilot routes, so this remains a transfer assumption." Architecture 7 keeps the
  three steps in the chain and puts the deciding work in that transfer.
- 2026-11-09, stage 2, a second scenario (the order on a -10 C or -8 C day) as a further graded result: duties sit
  within 1 kWh of the limit across the honest rivals at both temperatures; dropped.
- 2026-11-09, stage 2, the drag coefficient at 0.032: leaving speed out moved every energy only 6 to 15 kWh, so half
  stayed within the graded 10 kWh and the careful pass priced at 58.5; at 0.046 (air drag about a sixth of the draw
  at 70 km/h) the shift is 9 to 21 kWh.
- 2026-11-09, stage 2, a drive-software update logged in the workshop file as the second judgment (the pilot's
  efficiency stepping down at each tractor's own update date): a timing break built into the data, found by one
  residual plot and fixed by one indicator, the client's shallow hidden factor; not built.

- 2026-11-09, stage 4, the dairy and the pallet maker writing one standard full-load weight on every note (13,500 kg
  on all 389 of the dairy's pilot notes): the determinism judge read a column with no spread at all as an authored
  device; both now declare the load plan's pallets at a standard weight each (540 and 360 kg), the pallet count on
  the note agreeing, and the per-shipper calibration carries them like any other.
- 2026-11-09, architecture 5 (one deep step: the declared payloads' dilution, with the cold form and every other step
  never moving a duty): returned by the portal, version 13, reward 68.5, not stumped. The review: the decision rests on
  one recognition, Tabergs Trävaror's exact declarations confirm the corrected term for free (2.19 against 2.20), and
  under calibration V03, V07 and V11 stay over the limit under every cold form. Rebuilt in the same world on the
  client's instruction as a results chain in which three estimates each move the order.
- 2026-11-09, stage 2 pricing, the drinks maker's scale from November 2025 or June 2026: its scale-weight pilot days
  alone (340 or 128) pinned the payload term at 2.03 with a standard error of 0.33, a second free check; from 17
  August 2026 they are about 60 and give 2.2 with a standard error of 0.52, a band from 1.2 to 3.2 that does not tell 2.0 from the declared fit's 1.2.
- 2026-11-09, stage 2 pricing, Forsheda Gummi in place of Tabergs: the pilot shippers' mean loads spanned only 10.8 to
  13.6 t, so the payload term was confounded with the duties' own route effects (2.5 to 2.7 on the true payloads
  against 2.15); the glassworks at 21 t widens the span and the route effect is halved.
- 2026-11-09, stage 2 pricing, the sub-zero curve at 0.0175 kWh per km per degree: one cold rate shifted every energy
  about 8.5 kWh, leaving no room between the one-rate route's margin and the golden's on V03; at 0.024 the shift is
  about 12.5 kWh.
- 2026-11-09, stage 2, a cold figure of its own (the design day's extra energy per 100 km over a mild day): one rate
  and the curved forms agree on it within the honest family's spread, because the one-rate fit lowers its base
  instead; the cold form is graded through the fourteen energies.
- 2026-11-09, stage 3, the pilot's 468 kWh usable battery: on cold days late in the pilot the logged state of charge
  went below zero (the architecture 5 pack had days ending at -13 per cent); the pilot battery is now 520 kWh usable
  and the longest duties are shorter, so no day ends below 5 per cent.
- 2026-11-09, stage 3, the quotation's warranty at 70 per cent after 8 years (3.75 per cent a year): inside the loss
  band, so the manufacturer's floor would have given the graded loss; at 75 per cent it gives 3.1, outside the band,
  and still orders the six.

- 2026-11-08, stage 5, the forum and context artifact as drawn (board_of_directors, register): `guard.py heart` on
  the final pull BLOCKed both (`ban.forum`, `ban.artifact`) against task2 v4, registered after this card; redrawn to
  executive_team (the management group approves the order) and operations_log (the weighbridge and telematics logs
  carry the evidence), the prompt, FES-2 1 and 4.4 and the memo reworded; no figure moved.

- 2026-11-08, stage 4, narrowing the pilot shippers' mean loads (11.7 to 12.9 t) so the pilot-shippers' pooled line
  (rung 2a) falls clear of the limit: the golden lost the between-shipper spread its estimate leans on (slope 1.95, the
  within-duty fit and the shipper-mean route left the golden's bins and the latter its six); reverted, the rung is
  ruled out by the per-shipper slopes and recorded as straddling the limit.

- 2026-11-08, architecture 4 (the Irish retailer's outlying districts handed to a courier, each set priced on the
  fitted van run): spent on the platform; the author reports not stumped, run texts not supplied to the repo. The van
  that drives through a district to reach the next one is a mechanism the stop sequences visibly carry (the run-days
  that skipped a district show it), modelled on sight like every earlier Sulfur landing. The world is left; the next
  deep step must sit in a property the rows in view cannot show, with its evidence in another file.
- 2026-11-08, stage 2 pricing, the pilot's telematics at trip grain (each leg's energy): the empty legs carry a payload
  of exactly zero, an error-free contrast with the loaded leg, so the declared fit's payload term came out at 2.0
  against 2.2 and the dilution vanished; the fleet portal's daily summary is the pilot's record.
- 2026-11-08, stage 2 pricing, clerks' error at 21 to 24 per cent: the declared slope fell to 0.6 kWh per tonne per
  100 km, below what rolling resistance alone costs, a figure a solver sanity-checks against physics; at 17 per cent
  it is 1.0, low but not absurd.
- 2026-11-08, stage 2, an ask on each going duty's spare load to the nearest tonne: the standing family spread it over
  a tonne on four of six duties (a fork on the asks); dropped.
- 2026-11-08, stage 2, the shortlist on mid-weight loads: duties near the pilot's mean load (12 t) give the same energy
  on any slope, so the shallow run kept 6 of 14 energies; the shortlist's shippers now sit far from the mean.

- 2026-10-31, architecture 2 (the agro-climatic network's 2028 drift-alert setting, the drifts cut short by the 3.0
  alerts' repairs): spent at the batch 1 repair; the determinism judge returned NOT_DETERMINISTIC, SEND_BACK: the 4.0
  call counted every repaired drift the re-run never reached as exactly one later alert, which no shipped file
  forces; a rate model built from the sensor history (onset at the previous clean check) puts slow drifts hundreds of
  days from the wider limits and gives 14 to 16 a year at 4.0, not 18; and the new contractor's visit day rested on
  an inference. Filing the counting rule would make the decisive step rule application, so the world is left after
  two architectures.
- 2026-10-31, the draw's first card (gap population, G3 decisive): `test.same_puzzle` and `test.same_driver` BLOCK
  against task270 v8, task464 and four older builds; the decisive gap is time (the route of record is standing and the
  routing changed night by night), the honest reading, which clears both.
- 2026-10-31, a bypass mechanism (depot-to-depot direct trailers skipping every hub): on the route of record each
  direct-loaded parcel is a miss at its plan's hub, a loud rate a solver investigates, and the lane-night correction
  that follows lands that hub's verdict; dropped before any data, the overflow alone carries the step.
- 2026-10-31, overflow nights on which Pruszkow's own scanning is unaffected: the overflow nights' excess of unscanned
  parcels at the Warsaw depots over Pruszkow's usual rate is then Strykow's unscanned overflow, a one-subtraction route
  to the call; Pruszkow's own misses now rise with its sorter's load on the same nights, so the excess route charges
  Strykow with Pruszkow's own misses and clears Pruszkow.
- 2026-10-31, a linehaul trip log in the pack: it is a second, timed route to each trailer and nothing else reads it,
  so its presence would announce the step (readability test 7); the unload bursts carry the trailer on their own.
- 2026-10-31, the first ask A (each hub's sort events its interface sent twice): a re-sent batch of sort events is the
  battery's near-exact duplicate and sits on the call's own file; the ask moved to the courier events per depot.
- 2026-10-31, one handheld model per depot (TC51 at the contract depots only): the battery's near-exact duplicate then
  lands every TC52 depot's re-sends exactly; every depot now runs both models.
- 2026-10-31, ask B matched against every courier event: with trailer collections as the only absence, any courier
  event is evidence of collection and that shortcut lands all 13 depots; couriers now record a failed pickup against the
  pre-advised number, which is no collection.
- 2026-10-31, marketplace order numbers drawn per seller for every marketplace: two sellers on one marketplace then
  share an order number and a pickup is counted against the wrong order; the marketplaces that number orders globally
  now do so.
- 2026-10-31, Strykow's own sorter at 0.61 per cent: the morning's sorted split left Strykow at 0.87, 1.148x from the
  line; at 0.56 per cent it sits at 0.77.
- 2026-10-31, the card as drawn at the heart screen (G3 decisive, the head of tracking data quality asking, a PDF note
  beside the workbook): `guard.py heart` BLOCKed ban.pattern and ban.role against task5's later re-draw, and warned
  the shell (whether, each, pdf and xlsx) repeated task245; the measured ladder puts the decisive step past the
  missing-at-random split (rung 1), so the decisive generator is G17 and G3 is the default path's; the requester is
  redrawn to the director of network operations and the chart goes to the board on a slide.
- 2026-10-31, the claims file opened claims up to five days after the extract (`leak.py`, dates after the setting): a
  claim not yet opened on 6 November is not in a 6 November extract, and a claim opened in its last five days is open.

Architecture 2 and earlier, carried from the agro-climatic note:


- The seed's own pitfall (a per-station two-sigma rule against a network budget): the multiplicity reflex; it is the
  default path, not a stump.
- Limits estimated from short baselines (the parameter-estimation effect on false alarms): an honest replay of the
  filed limit-setting over the record lands it, and executing the filed limit rule is close to rule application.
- A burn-in of new sensors in a 2028 replacement programme: a composition shift (composition_mix banned against
  task473) announced by the replacement plan.
- Closures clustered in one province: the continuing stations keep their near neighbours on their own side and the
  alerts barely move (prototype, 0 of 97 continuing stations' spread up by 5 per cent); the programme's stations are
  interspersed, as gap-filling stations are.
- validated_decoy true on the first card (the replay reproduces the alert log and only the closures break it):
  guard BLOCK; the April 2026 additions put the refutation inside the record.
- Seed 252: the per-setting figures at 3.0 and 3.5 sat 0.17 from their rounding edges (65.67, 26.67 a year) and a
  literal reading of the record's first fortnight moved 3.0; a scan of 1,000 seeds found one (1141) with all four
  three-year counts divisible by three and unchanged under the start, limit-rounding and strict-limit readings.
- A statistic defined on every day with 10 residuals: the export carries read days only, and a reader of the export
  moved 4.0 from 11 to 10; the statistic and its alerts are now on read days (section 5).
- The hold read per calendar year: lifting it each January moved 3.0 and 3.5 by a whole alert; section 8 now says a
  new year's configuration does not lift it.
- One out-of-sample year: a single fresh year on the 2028 network raised exactly 18 at 3.5; three fresh years are the
  section 7 horizon (24.7 at 3.5, 10.3 at 4.0).
- The asks with one campaign device drawn at random: the readings-first path kept 10 of 24 and the order-first path
  12; the campaign visits, the cancellations after the visit and the remote resets are now aimed at every district,
  and the standard's absence reaches the winter visits no campaign touches.
- Architecture 1 (the record re-run with the 34 closing programme stations out of the neighbour pool, as the decisive
  step on its own): spent 10-20 at stage 4. Reader 1 re-ran the quality control with the 2028 network and filed 4.0 at
  9 a year, every setting within one of the golden (63, 26, 9 and 3 against 61, 25, 9 and 3); reader 2 replayed the
  record and filed 3.5 at 9; judge DETERMINISTIC APPROVE. A stated change with an obvious mechanism is landed by a
  careful reader: the network re-run is now the first rung, and the decisive step is the drifts the record's own 3.0
  alerts cut short.
- One key, the censoring alone (no closures): a single unprompted insight decides it, and a reader who thinks of the
  repairs lands the call; two keys, each alone leaving 3.5 inside the visits, are needed.
- Drifts anywhere in the network: a drift left to grow carries a close neighbour's statistic over that neighbour's
  limit before its own alert (prototype, 5 to 12 stations per seed whose counterfactual count departed from the
  re-run plus the cut-short drifts); drifts now sit only where the weight a neighbour gives them times their spread
  stays under 0.7 of the neighbour's own, at stations that keep their usual neighbours.
- Censored drifts the spring round would have found first: a drift cut short in January or February at a setting of
  3.0 would at 4.5 have met the station's spring round before its alert (prototype, 1 to 2 a year); a drift whose
  station's next round falls before it could have crossed 4.5 is redrawn.
- An autumn calibration round in 2027 and 2028: 2028's rounds would then differ from 2025's and 2026's, and the
  record's drifts of June to August would have been found by a round rather than an alert, a forecasting fork on
  the window; every year now has the spring round only.
- The six stations added in April 2026: their 21 months against the record's three years opened an annualisation
  fork on each setting's count; the six infill stations now report from 2025.
- Old sensors with standing offsets up to 0.4 degrees: a false alert's visit at such a station adjusts a sensor
  that never drifted, and the history's drift-alert adjustments stop meaning drifts; standing offsets are now under
  0.12 degrees and no check without a drift passes the 0.2 adjustment threshold.
- The visit asks on orders and readings alone (round 2): drift orders cancelled after the visit with the readings under
  the cancelled order, orders the handover export lost, and a closed order with nothing under it counted a visit when
  the station had a reading under another order while it was open. The pass 3 judge sent it back (52 cancelled orders
  with readings against the dictionary's Visita, the lost orders' window unrecoverable; Gate C on asks 3 and 4), and
  with the visit filed reader D built the visits from the readings station by station and took 24 of 24. Filing a
  visit closes the fork and hands the ask to every reader; the devices that held were all readings a careful reader
  joins. The cancellations after a visit and the lost orders are gone; the device is now readings no visit made (a
  spare checked at the workshop under the station's order), found only against the range the station's logger
  recorded that day.
- The growth of a drift left to the reader (rounds 1 to 3): the pass 4 judge read section 7 literally as the record
  re-run and found nothing filed that a drift the 3.0 alert's check set right would have gone on growing; the as-found
  errors at repair (0.6 to 0.9 of the 4.0 limit) then read as the drifts' full size, and 3.5 stood as at least as
  defensible (SEND_BACK, Gates A to C on the main call). Section 9 now files the property of sensors the counterfactual
  rests on (a drift does not stop on its own and grows at the sensor's own rate until a check sets it right); the
  censoring remains the analyst's, and the cut-short drifts alone, without the network re-run, still file 3.5.
- An open interval on the rate (2026-11-07, the portal's Domains Fit return): a bootstrap over the month's mornings or
  unloadings puts Pruszkow's lower bound at 1.01 (90 per cent) and 0.97 (95), so its side of the tolerance moves with
  the method and the seed; the request files the interval's model (each parcel an independent chance of a miss), under
  which every standard binomial interval keeps each hub on one side, and grades only that side.
- 2026-11-08, architecture 3 (the Polish carrier's October missed sort scans by hub, the unscanned overflow parcels
  charged to the hub whose trailer they came off): spent on the platform; both runs reached the golden's call and every
  graded figure, so the platform returned not stumped before any rubric. Each read the overflow off the observed hub
  within each delivery-depot, door and night cohort by a plan-against-observed cross-check, a contradiction a cross-tab
  exposes and so a work order, and executed every texture device and the interval the request named. The world is left
  (one architecture per world); the next deep step has to move both runs' Final Recommendation, since a landed call
  never reaches the asks.
- 2026-11-08, stage 2 pricing, Killala as a through-road district: its approach from Ballina is too short for time in
  district to clear 1.15 of the line once removal keeps it (1.47 against 1.24); it left the offer and stays on the
  Ballina run.
- 2026-11-08, stage 2 pricing, the first set-by-set pricing: handing over a run's far end makes every through-road
  district before it the new end, so a corridor whose end goes takes its through-roads with it and the default and the
  golden agreed on them; the deep step bites only where the far end stays (Clifden, whose hotels and shops take
  several parcels a stop) or where removal is priced one district at a time (Mulranny, Bangor Erris).
- 2026-11-08, stage 2, the draft prompt's "the van-hours our runs would no longer drive" and "the van-hours each of our
  runs would shed": counterfactual words pointing at removal (the review's condition 1); cut to "the van-hours it
  saves" and "before and after the hand-over".
- 2026-11-08, stage 3, the golden's run hours without the driver's break: NPS-3 2.3 counts depot out to depot in, so
  the before and after figures were short by the break; the model now carries the break (never saved), found by the
  ceiling script against the run log.
- Stage 4 fix pass (2026-11-08): the judge's independent fit put Leenane and Letterfrack at 118 to 124 van-hours against the golden's 110 and R04's saved hours 30 above the golden on a 2026-only fit, and read the offer's "in any combination" beside NPS-3 4.1 as a search order. Dropped the combination wording (NPS-3 4.3 now names the selection as an outcome), moved saved hours to 100-hour bins with the Achill road slowed (R04 to about 710 saved, 1,610 before) and Owenduff's price raised to EUR 13.40 to hold the net saving mid-bin; component 1 is now 'about 110 van-hours' against the hours Owenduff's charge would pay for. The call, the stump, the ladder and the default path did not move.
- 2026-11-10, architecture 10 stage 4, pass 7 on target.zip 67186f2dd19abb65 (the 690 kW world): judge DETERMINISTIC APPROVE (17 needs a charging efficiency under 0.894, never observed; 19 needs 0.948 or more, one outlier session in 3,291; the heater band, 10 to 20 minute margins and both schedules land 18; careful but hurried about 2.5 of 8, ordering about 21; the diesel ask does not hand over the bridge). Its two findings: the six pilot buses after delivery, closed as SF30 (one bus a block assigned, the night on the assigned blocks); and the Step-by-Step's earliest-departure clause, which its thread could not reproduce because it took every block as in the depot the whole night (3 of the 18 are; the generator's least-slack schedule recharges the 18 and earliest-departure-first leaves 98 kWh short), so the clause is cut to the exact flow and the least-slack schedule. The fourth leak reader quoted no process sentence, found no helper file and no one thing, and noticed the fuel heaters on a read, so R3's notice is a careful-pass move and its price rests on the figure from the HVO fills. No graded figure and neither zip moved.
- 2026-11-10, architecture 10 loop 1, the platform's holistic audit (0 of 1 items addressed): the order count was not
  forced (the agreement's "except for the workshop's two outlets at 22 kW" beside DES-1 3.2's "in the periods the
  agreement gives it" and the quotation's 22 kW AC inlet put M124 in, 19 for 18), and "a yes or no on going electric"
  (23 or 18), "every block that passes" (8.7 or 6.7 MWh) and "deliver" (8.0 or 8.7 MWh) each read two ways. Closed by
  WHAT pins (DES-1 3.2: the charging lane's chargers, the workshop's outlets for buses under repair, the draw as the
  chargers take it; the agreement and the plan on the outlets; the prompt's "qualifies under the standard" and "the bus
  of every qualifying block on charge" at the connection point). With the heaters already read by a careful run (the
  leak reader noticed them), the heater fix alone landed the old count (18), so the chain was one judgment short: the
  charging sessions now carry what a bus on charge draws beside its recharge (the battery held at charging temperature
  on a cold night), a third independent judgment graded as component 3, which moves the order to 17; the six pilot
  buses move to Kauppala in the plan, closing SF30 by the data.
- 2026-11-10, architecture 10 loop 1, the least night-period capacity at which every qualifying block can be
  recharged, as a sixth ask (the reinforcement's size): the exact flow needs 921 kW against 913 kW for the night's draw
  over its ten hours, because almost every qualifying bus is in the depot from 21:00 and leaves after 05:00, so the
  averaging shortcut lands inside any honest band and the ask would grade nothing; not built.
- 2026-11-10, architecture 10 loop 1, a cabin preconditioning load before departure from the charger (the quotation's
  earlier row): the relay holds the chargers off from 07:00, so the blocks departing after 07:00 (and the afternoon
  blocks departing after 11:00) could not precondition from the charger and the draw's timing forked; replaced by the
  battery's thermal management over the released hours, which the relay bounds on every block.
- 2026-11-10, architecture 10 loop 1, the clean re-judge (FIX_NOW, order kept): the loss band of 3.8 to 5.0 excluded a
  straight line in age (2.96 on that pack, 2.80 on the judge's refit) with nothing shipped ruling it out; the loss moves no
  verdict and no bus, so the band is widened to 2.7 to 5.0 rather than a document naming the age form (a HOW pin). The
  same pass recomputed the 17 and M145 by its own max-flow and least-slack schedules across its own readings of the
  charging split and the workshop outlets, the night at 9.23 MWh and the conditioning at 2.98 to 3.46 kW, all inside
  their bands; its simplified diesel refit (19 blocks, no swipe merge) did not reproduce ask 1, which `verify.py`
  reproduces on all 48 within 0.7 on its own code path, so Step 2 now says the fit is joint over every block the
  intervals touch. The answer blocks dropped the context figures an earlier audit read as rival answers (the energy
  into the batteries, the draw for the assigned blocks, the fit's unbanded efficiency and parameters from component 3).
- 2026-11-10, architecture 10 loop 1, the main thread's check on the FIX_NOW re-judge (APPROVE, order kept), whose own
  conditioning fit came out at 2.23 kW: the battery's gain on charge read on the fitted fade curve without the
  reversible cold capacity put the draw at 2.27 kW, the efficiency at 0.958 and the order at 18 (M124 refused), and fitted
  the sessions better than the day's own record, a fork on the call. The reversible cold capacity was 0.16 per cent a
  degree below 10 C (4 per cent at -15 C), riding in the gain on exactly the cold nights the conditioning is read from;
  at 0.04 per cent a degree (1 per cent at -15 C, a pack its thermal management keeps warm) every capacity basis but the
  bare quoted 480 kWh lands 17 with M145 refused (SF42), and the loss, the verdicts, the energies and the order do not
  move (the limit 390.5 to 390.3 kWh). The APPROVE was scoped to the earlier pack, so the judge runs once more.
- 2026-11-10, architecture 10 loop 1, the platform's Domains Fit return on the READY prompt (979f04f): it read every ask as
  a lookup or a certified figure applied to a stated rule ("look up diesel use per 100 km, compare a quoted kWh figure
  against a design-day threshold, count qualifying blocks, and sum connection-point energy ... nothing needs to be
  estimated, modelled, forecast or validated"), the "quoted 2027 model" taken for a quoted energy. The prompt now leads
  with the forecast's population (most of the blocks never run by an electric bus) and names each result as what it is
  (an estimate of the diesel use, a forecast from the company's own operating records of the design-day energy, an
  estimate of the loss, a forecast of the night's draw), as this slot's architecture 5 did when the same review read it
  as route arithmetic; the answer blocks say the same. A 90 per cent interval on the loss, the review's own example, was
  measured and not built: the iid, by-bus clustered and per-bus intervals all read 4.2 to 4.5 on this pack, so it would
  grade nothing, and its bounds would inherit the age-form fork the band was widened for. No graded figure and neither
  zip moved.
