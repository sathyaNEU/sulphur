# task4: how many battery-electric tractors to order for the Värnamo duties in 2027, and which duties they take

## Draw

Subdomain: Regression, classification & model diagnostics (General Statistics & Data Science; house domain Supply Chain & Logistics, fleet electrification)
Analysis type: Forecasting & Predictive Modeling
Answer shape: An allocation plus its sensitivity (which shortlisted duties get the tractors, each duty's design-day energy against the limit, and the order each shortcut would place instead)
Weight: measurement: the order turns on three quantities the pilot records only indirectly and the runs' own checks do not test (the loads the pilot's duties carried, known only as shippers' declarations whose terminal calibration does not carry to the pilot's part loads; the battery's permanent loss, read through an energy-per-SOC proxy whose early-life fall a straight line and a year-apart check both miss; the speed on a winter day, known only as a planned figure); task1 sits on synthesis and task7 on modeling
Data-native sentence: the pilot's daily summaries carry one energy figure and two SOC readings per tractor-day, while the load each day carried exists only as a clerk's estimate on a note whose error the Värnamo weighbridge measures for loads of another size, so every quantity the order turns on is a measurement problem before it is a forecast.
People: Georg Pålsson, fleet manager, who places the order (FES-2's owner); Inger Norman, transport planner, whose workbook and memo the golden are; Pierre Kjellberg, the dealer's key account manager, who signs the quotation (`guard.py names --geo Sweden --seed 505`). None appears in the prompt.

Architecture 9, 2026-11-10, in the same world (the client's instruction to keep the data package; the author's
instruction to reship a level 5 task that is genuinely stumped). Architecture 8's two platform runs landed the
golden exactly (`runs/arch8/`): every step it added was one join to a register the runs already read, and its hourly
fridge term made both runs time the design day, which is the winter speed correction. This architecture removes the
fridge draw and puts the deciding work where the four recorded runs (architectures 7 and 8) said what they assumed
and did not test it, or computed the answer and set it aside: "Shipper calibration transfers between depots... no
measured Jönköping payload sample directly verifies it"; "the duty-fixed-effects specification estimates 2.80...
material model uncertainty" (dismissed for the pooled figure); year-over-year and first-year-only checks of a
straight-line battery loss; "Target routes are longer and faster in routing terms than the pilot routes, so the
forecasts involve extrapolation".

## Deep reasoning

Task type: regression, classification, model diagnostics (General Statistics & Data Science), serving Forecasting & Predictive Modeling: each shortlisted duty's 2027 battery energy on the January design day, forecast from a fitted energy model carried to duties the pilot never ran, against a limit that is itself an estimate of the ordered battery after a year in service.
Domain test: the results are a regression slope on a covariate observed through third-party reports with classical error, where the error model transports between two populations and the calibration line does not (the regression diagnostic the subdomain is about: the within-duty and between-duty estimates disagree on the line and agree on the transported model); a degradation curve whose form is chosen by fit and read inside the observed ages, net of a reversible seasonal effect; and an extrapolation in speed through a weather-dependent ratio.
Swap: "how many community nurses to hire and which rounds they take, from the pilot's visit times" keeps a fitted time model but loses the declared payload with its clerk's error, the battery's early-life fade read through state of charge, and air drag on a winter road's speed; the call stops making sense.
Where the weight sits: R1 and R2, two measurement problems the pilot's records support only after diagnostics: comparing each pilot duty's declarations with its shipper's at the terminal and carrying the error model rather than the line (then confirming on the drinks maker's scale days and the within-duty fit), and fitting the battery's age form against a straight line and seeing why the year-apart check agrees with the wrong one.
Layer 1: the dairy and the pallet maker declare their planned pallets at a standard weight each; the fleet portal uploads a day twice after a modem reconnect; the tractor's ambient sensor drops out (the station file covers it); the TMS types a declared weight three ways (12000, 12 000 kg, 12,00 t); the weighbridge re-weighs a CMR after an axle limit; the Värnamo duty codes were re-keyed at the April 2026 TMS upgrade; spare tractors change the stored tare; 1.2 per cent of weighings have no declaration; a multi-drop day's declared weight is split over several notes; SOC is logged in whole per cent. Each is asserted neutral (SF5 to SF8, SF27, SF33) and none decides a result.
Not one thing: three estimates each move the order, and each put right alone inside the careful model still orders wrongly (the duties' own loads alone: 2 tractors; the curved loss alone: 3; the design-day speed alone: 10; effort.json hints); the strongest single piece rescues 1 of 5 results.
One-fact test: the most useful single sentence ("the pilot's regional duties carry lighter loads than the same shippers' terminal runs, so the terminal's calibration line does not carry to them") rescues 1 of 5 results (R1) on the careful pass, which then orders 2; the loss sentence rescues 1 (R2, order 3), the winter speed sentence none (order 10). The re-judge thread's best sentence joined two of them ("control for ambient temperature and de-bias the declared payloads"), which is two hints.
Not semantics: every field read right (the declared weights, the weighbridge's declared and weighed columns, the SOC readings, the routing tool's driving time) still leaves the terminal's line on the pilot's loads, a straight line in age and the year's speed ratio; nothing filed says the pilot's loads differ from the terminal's, that the battery fades fast early, or that winter roads run slower than the plan.
Not rule application: FES-2 files the WHAT (2.1 the duty with its drops, 2.2 the energy the tractor draws, 2.3 the usable battery less the first year's permanent loss taken from the company's own tractors, 4.1 the design day, 4.2 the planning load, 4.3 the limit, one tractor a duty); nothing filed names a calibration, an error model, an age form, a speed, a ratio or a temperature form.
Estimand: FES-2 2.1 to 2.3 and 4.1 to 4.3 with the quotation's 540 kWh usable and 11,980 kg tractor: population the fourteen shortlisted Värnamo duties (fleet_plan_2027.xlsx), outcome the battery energy of a round trip depot out to depot in with its drops, window a January working day at -5 C departing with the mean net payload weighed November 2025 to October 2026, unit kWh and tractors, comparison each duty against 85 per cent of 540 kWh less the share a battery permanently loses in its first twelve months in service as the company's own tractors show it; the duty's speed and combination on that day are part of the forecast, not filed figures.
No decoy: no memo, draft or stakeholder figure; the quotation's warranty (75 per cent after 8 years) is a floor the dealer guarantees, not a first-year figure, and no file states a duty's design-day energy, a load factor, a consumption rate, a speed or a loss.
No replay: no result re-derives a published figure and no stated number in the pack is wrong.
Pinned: run on the cut pack and the clean truth (checks.py, 353 assertions; verify.py's per-duty moments correction and per-tractor log-of-age loss): the payload term over the error additive or multiplicative, read on the last twelve months, each day at its duty's mean declaration and the within-duty fit, 1.89 to 2.00 (band 1.7 to 2.4); the loss over every curved age form (square root, square root and line, log and line, piecewise line with knots at 3, 6 and 12 months, early-loss time scales of 0.20 and 0.45 years, the straight line on the first year's days) and cold term, 4.3 to 5.5 (band 4.2 to 5.6); the speed ratio over five forms, 0.758 to 0.783 (band 0.74 to 0.79); knots at 14, 18, -2 and 2 C, a quadratic, temperature bins, the station's temperature, either year alone, speed as a straight line, one coefficient for tare and payload, the drops at equal shares: every one orders the eight with every energy within 8 kWh and clear of its limit by 4 kWh or more.
Run forecast: R1 lost to dismissed own evidence and an unfinished chain (every recorded run took each declaration to the terminal's weighed-on-declared line by shipper and wrote that the transfer between depots was unverified; arch 8's runs computed the within-duty slope and set it aside; the careful pass files 1.5 and sets aside its own within-duty 2.3); R2 lost to a self-confirming check (every run fitted a straight line in age with tractor and cold terms and checked it against the same months a year apart, which agrees at 2.8 because it starts after the early loss; the first-year-only fit at 4.3 is computed and set aside); R3 lost to a method shortcut (both arch 7 runs fed the routing tool's speed at the year's ratio, energies 10 to 20 kWh high; arch 8's runs timed the design day only because of the hourly fridge term, now gone, and a run that times it is Partly here); R4 Partly; R5 lost (5 on the careful pass, 10 at the design-day speed).
Strategy label: WORKS IN FORM (a forecast carried to a population the fit never saw, through a covariate whose calibration does not transport, beside a degradation whose form the record chooses).
Depth level: 5. Three independent estimates each move the order and each alone leaves it wrong (2, 3 and 10 duties with one put right inside the careful model); the shortcuts land on 12 distinct wrong orders over 17 routes (effort.json); the careful pass orders 5 and its design-day variant 10, disagreeing with each other and with the eight.
Lesson: a calibration estimated on one population is a model of that population's true values as well as of the instrument; under classical error only the error model carries, and a check that varies a nearby choice inherits the blind spot it was meant to test.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | one tonne of payload adds 1.9 kWh per 100 loaded km | missingness and measurement | the weighbridge's declared and weighed loads per shipper and note period (the error model); each pilot duty's own declarations; the drinks maker's scale-weighed pilot days; the within-duty fit | 1.7 to 2.4 | dismissed own evidence: the terminal's weighed-on-declared line carried to the pilot, 1.5, its own within-duty 2.3 set aside | - | Component 1 |
| R2 | the batteries' first-year permanent loss, 4.6 per cent (usable 515 kWh, limit 438 kWh) | modeling | FES-2 2.3; energy per full charge on a level per tractor, an age form chosen by fit and degrees below 20 C | 4.2 to 5.6 | self-confirming check: a straight line in age, 3.1, confirmed by the same months a year apart (2.8) | - | Component 2 |
| R3 | the fourteen design-day energies, nearest 10 kWh (V02 430, V14 430, V18 430, V07 450, V21 450 ...) | forecasting | FES-2 4.1, 4.2; the model with every term (the combination's tare and the drops included, joins the recorded runs made), each duty at its design-day speed (the pilot's actual-to-planned ratio at -5 C, 0.76, band 0.74 to 0.79 over five forms) | each within 10 kWh | method shortcut: the routing tool's speed at the year's ratio (0.89, both arch 7 runs), 10 to 20 kWh high on most duties | R1 | Ask 1 |
| R4 | each duty's verdict against 438 kWh | synthesis | FES-2 4.3 | exact per duty (partial credit from three quarters of the duties: an all-electric answer gets 8 of 14) | unfinished chain: 11 of 14 on the careful pass | R2, R3 | Ask 2 |
| R5 | order 8: V02, V03, V05, V09, V11, V14, V16, V18 | synthesis | FES-2 4.3, one tractor a duty | exact | unfinished chain: 5 on the careful pass, 10 at the design-day speed, 2, 3 or 10 with one estimate put right | R2, R3 | Recommendation |

Carry-forward: R1 and R2 stand alone on their own inputs (the bridge and the pilot's notes; the pilot's SOC records); R3 falls with R1 or the design-day speed; R4 and R5 fall with R2 or R3. No analytical result carries more than half of the others: R1 sits upstream of R3 to R5, but put right alone it rescues none of them (the careful pass then orders 2; effort.json hints), because R2 and the winter speed carry the same three. Two pieces of work stay in the model and the workbook and are not graded on their own, because the stage 4 judge put them within a careful run's reach: the combination's tare and the drops (V02 and V14 22.6 and 22.5 t with the 2027 tractor; V03 and V11's loads riding 0.60 and 0.58 of their loaded km), and the -5 C speed ratio (0.76; Critical Components and the Supplementary Questions no longer state it as a graded figure, Step 8 shows it).

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| the pilot's regional duties carry part loads (75 to 89 per cent of the same shippers' terminal loads), so the terminal's weighed-on-declared line, which shrinks a clerk's estimate toward the terminal's loads, overstates every pilot duty | constructed as a dispatch process on all nine pilot duties, six shippers | no: every pilot duty is misread (0.5 to 4.4 t), the payload term moves, and the careful pass misreads energies by over 10 kWh on duties where nothing turns (asserted) | a targeted comparison across two files (each duty's declarations against its shipper's at the terminal), then modelling (an error model carried in place of the line), confirmed on the drinks maker's scale days and the within-duty fit | modelling (a measurement-error model transported between populations) | keep: one of three, rescues 1 of 5 |
| the battery's early-life loss: most of the first year's fade in the first months, then a steady loss | constructed as battery physics on all six tractors, each with its own rate | no: every tractor's curve beats its straight line (asserted); the year-apart check misses it by construction of the comparison, not by a planted event | modelling (an age form chosen by fit against the straight line, net of the reversible cold) | modelling | keep: thin alone (a form choice), one of three |
| energy per km rising with the square of speed, and the routing tool's optimism larger on winter roads | constructed as physics and a planning process across every day | no: all nine pilot duties and every day; the year's ratio misreads all fourteen energies | modelling: a speed term, then a ratio fitted against temperature read at -5 C | modelling | keep: one of three |
| the combination's tare on every leg; a multi-drop load taken off along the run | constructed as physics and a delivery process across every trailer and multi-drop duty | no | a join to the trailer register; the notes on the stops | modelling | keep in the model, not graded alone (earned by careful runs) |
| shipper-specific declaration error; the sub-zero cold curve and the cold's reversible capacity loss | constructed by simulating how each shipper writes a note, and as physics | no: 19 shippers, every day | modelling | modelling | keep: earned by careful runs |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 payload term, kWh per t per 100 loaded km | Missed | Missed | Right |
| R2 first-year battery loss, per cent | Missed | Missed | Right |
| R3 the 14 design-day energies | Missed | Missed | Right |
| R4 each duty's verdict | Missed | Partly | Right |
| R5 the order | Missed | Missed | Right |
| Roughly | 0 of 5 | 0.5 of 5 | 5 of 5 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (generator/effort_passes.py runs each pass end to end on the cut pack)
Largest single hint: the pilot's regional duties carry lighter loads than the same shippers' terminal runs, so the terminal's calibration line does not carry to them; rescues 1 of 5 results
Pair estimate: 20.8

The careful column is the union of the four recorded runs' methods, implemented in `analysis.routes` as "careful but
hurried": every file cleaned, the per-shipper weighed-on-declared calibration, the curved cold, the tare and the drops,
squared speed at the year's ratio, a straight-line loss with tractor and cold terms; its within-duty slope (2.3), the
year-apart loss (2.8) and the first-year-only loss (4.3) are computed and set aside (`effort.json` careful_dismissed).
Read strictly, the union also contains arch 8's timing of the design day (which arrived only through the hourly fridge
term, now removed): that variant (`careful_variant_design_day_speed`) is Partly on the energies and the verdicts and
misses the payload term, the loss and the order (10 against 8): 34.5.
Stage 4: the judge's first isolated thread put a careful pass at 50 to 62 per cent on an eight-result grid and
flagged the tare and drops as earned by reflex; its re-judge thread put it at about one result of six, the -5 C speed
ratio. Both pieces were taken out of the graded chain (they stay in the model and every energy), and the verdicts'
partial credit set at three quarters of the duties (an all-electric answer gets 8 of 14). Executed on the cut pack,
the careful pass scores 20.8; with one correction it scores 19.0 (the duties' own loads), 19.0 (the curved loss) or
34.5 (the design-day speed) and loses the order every time (`effort.json` careful_with_one_correction). The residual
risk, stated plainly: a run that both times the design day and carries the error model in place of the line lands
the order with only the loss wrong (the straight-line loss alone moves the limit 7 kWh and flips no duty). Making
the loss flip a duty alone needs a loss gap over 3 points, which widens the honest band of curved forms to about 4.2
to 6.6 per cent and leaves under 2 kWh of cushion (stage 4 sweep, Tried and rejected).

## Data provenance

Source: generated by task4/generator from a simulated process (sim.py, pack.py, docs.py), seed 5405; real Swedish town names, everything else invented.
Behaves like the real thing: a battery-electric 64-tonne combination's energy per km rises with climb, cold (bending below freezing), the square of speed and the whole combination's mass on every leg, with the payload's tonne-km on the loaded run as each drop comes off; trip noise 3 per cent and a route effect per duty; the routing tool plans each duty's driving time and the trucks fall short of it, more so on winter days; the consignment notes carry what the shipper writes, one per drop; the regional pilot duties carry the day's orders, lighter than the terminal's long full-load runs; the bridge weighs every departure with its trailer; the battery loses capacity fastest early in service and then steadily, and the cold depresses each day's energy per full charge and gives it back.
Genuine patterns: (1) seasonal temperature with persistence at two stations and a truck-against-station offset; (2) energy per km rising with climb, cold, speed and combination mass; (3) actual speed falling short of the plan, more in winter, with day-to-day noise; (4) declaration error by shipper practice, one practice changing in the window; (5) load size by lane: regional part loads against long-haul full loads for the same shippers; (6) capacity fade fast in the first months then steady, tractor by tractor, with a reversible cold effect; (7) trailer pools by goods with tare by build and equipment; (8) drop shares varying day to day around each customer's usual order.
Problems by process: re-uploads after modem reconnects, sensor dropouts, three weight formats typed into the TMS, re-weighs after axle limits, duty codes re-keyed at the TMS upgrade, spare tractors, blank declarations, a day's weight split over several notes, SOC in whole per cent.
Breadth: 13 files; the weighbridge holds about 21,400 weighings of 46 duties from 19 shippers; the Värnamo notes about 17,800 consignments; 2,334 pilot duty-days on six tractors; 145 trailers; the route register's 55 duties with their routing-tool times and stop lists; a ten-year temperature record at two stations; two distractors (the Värnamo fuel card statement and the workshop log).

## Template check

Chain signature: missingness-measurement, modeling, forecasting, synthesis, synthesis
Question form: which (the duties that go electric, with the order's size), with the payload figure and the loss asked as their own quantities
Nearest build: task4 architecture 8 (the same world, kept on the client's instruction; differentiation filed on the card: there three register joins the runs made on sight, here the calibration's transport, the loss's form and the winter speed, each a step the runs named and did not take); against other builds, task1 (an ARR path, synthesis) and task7 (scenarios, modeling) differ in shape, weight and areas; the abstraction sentence against a build on file other than this slot's own lineage cannot be written. Guard WARNs answered: repeat.gate_g (forecasting is the assigned analysis type), repeat.question_form (the decision is a pick of duties; "which" is its honest form).

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | the design day's temperature | the trucks' ambient (station-filled), or the station's throughout | trucks' ambient | same call, energies within 10 kWh (asserted) |
| SF2 | a duty's energy | energy_used_kwh, or consumption times distance | energy_used_kwh | FES-2 2.2; identical within 0.5 kWh (asserted) |
| SF3 | the planning load | mean weighed net payload, or mean declared | weighed | FES-2 4.2; same call (asserted) |
| SF4 | the twelve months | Nov 2025 to Oct 2026, calendar 2025, or every month on the bridge | Nov 2025 to Oct 2026 | FES-2 4.2; same call (asserted) |
| SF5 | a re-weighed CMR | the later weighing, or the first | later | same call (asserted) |
| SF6 | a day uploaded twice | once, or twice | once | same call (asserted) |
| SF7 | an ambient dropout | station day plus the mean offset, or the day dropped | filled | same call (asserted) |
| SF8 | a declared weight in tonnes | parsed, or those days dropped | parsed | same call (asserted) |
| SF9 | the battery the limit starts from | the quotation's 540 kWh, or the pilot's 520 | 540 | FES-2 2.3 and 4.3; the quotation (asserted) |
| SF10 | the payload of a pilot day | the expected load given its declaration on its own duty, or the declaration | expected load | R1's own result; the declarations order 9 |
| SF11 | the cold form | curved below freezing, or one rate below 16 C | curved | the January and February 2026 holdout (asserted) |
| SF12 | rounding | energies to the nearest 10 kWh, graded within 10 kWh | as filed | every rival within 8 kWh (asserted) |
| SF13 | tractors | one per duty assigned | one per duty | FES-2 4.3 (asserted) |
| SF14 | the fit's window | Mar 2025 to Oct 2026, or one year | both | same call (asserted) |
| SF15 | the error model's window | both years on the bridge, or the last twelve months | both | same call (asserted) |
| SF16 | the fit's structure | one level per km with climb and tare, or a level per duty | one level | same call; the within-duty slope 1.9 against 1.9 (asserted) |
| SF17 | the fit's km | odometer, or the route register's | either | same call (asserted) |
| SF18 | the drinks maker's notes | its scale period kept apart from its estimating period | apart | the scale months' declarations equal the weighed loads (asserted) |
| SF19 | the loss's cold term | degrees below 20 C, the day's temperature, degrees below 15 C | any | within 0.3 points, same call (asserted) |
| SF20 | the loss estimator | an age form fitted on every day, or the same months a year apart | fitted | the year-apart comparison starts a year after entry into service and misses the early loss (asserted 1.2 points or more below) |
| SF21 | "permanently loses in its first twelve months" | at like temperature from entry into service, or with the cold left in | like temperature | FES-2 2.3 "permanently"; the cold's loss returns each spring |
| SF22 | the limit's arithmetic | 85 per cent of 540 less the loss share | as filed | FES-2 2.3 and 4.3 (asserted) |
| SF23 | the usable battery after a year | 540 x (1 - loss) | as filed | asserted |
| SF24 | a duty's speed on the design day | the routing tool's speed times the pilot's ratio at -5 C, or the routing tool's speed, or the year's ratio | ratio at -5 C | FES-2 4.1 files the day; the pilot's ratio falls with temperature (asserted); the other readings order 0 and 1 |
| SF25 | the speed term's form | the square of speed, or a straight line | either | same call (asserted) |
| SF26 | the ratio's form | a slope below 8, 10 or 12 C, on the temperature, or days within 2.5 C | any | same call, all in 0.74 to 0.79 (asserted) |
| SF27 | the trailers a duty runs with | the bridge's trailer registrations, or the trailers on its notes | either | within 60 kg per duty (asserted) |
| SF28 | the pilot's loads | each duty's own, or the terminal's line | each duty's own | the scale-weighed J07 and J08 days match the duties' own loads within 0.8 t and sit over 1 t under the line (asserted) |
| SF29 | a multi-drop load's shares | each note's declared weight, or equal shares | either | same call, within 8 kWh (asserted) |
| SF30 | the tare term | its own coefficient, or the payload's | either | same call (asserted) |
| SF31 | the loss's age form | any curved form (early loss with a fitted time scale, square root, with a line, log and line, piecewise line) | the fitted time scale | same call, all in 4.2 to 5.6 (asserted); the straight line fits far worse (asserted) |
| SF32 | the 2027 tractor's own weight | the quotation's 11,980 kg, or the pilot tractors' | quotation | same call (asserted); the quotation states it |
| SF33 | a trailer's tare | the register's, or the bridge's stored tare less the diesel tractor's | either | identical for every trailer (asserted) |
| SF34 | a duty's combination tare over several trailers | each departure's trailer (weighted by use), or each distinct trailer once | weighted by use | same call, within 0.3 t and 3 kWh on every duty (asserted) |
| SF35 | the declaration error's form | multiplicative (a share of the load), or additive | either | same call, payload 1.9 both (asserted) |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | the fourteen shortlisted Värnamo duties: filed, fleet_plan_2027.xlsx and FES-2 4.4 |
| 2 Unit of account | a duty, one tractor each: FES-2 4.3 (SF13) |
| 3 Attribution window | a January working day at -5 C: FES-2 4.1; the duty's speed on that day estimated (SF24) |
| 4 As-of dating | extracts to 30 October 2026, the memo of 6 November: the call reads no later record |
| 5 Version basis | FES-2 version 3 (September 2025), quotation Q-26-1187, the registers as saved in autumn 2026: filed |
| 6 Denominator | 540 kWh less the first year's permanent loss: FES-2 2.3, 4.3 (SF9, SF22) |
| 7 Weighting | each departure once in the planning load and the duty's trailer tare; each pilot day once in the fits: FES-2 4.2, C1 |
| 8 Window length | twelve months for the load, the trailers and the notes (SF4); twelve months in service for the loss (FES-2 2.3) |
| 9 Boundary inclusivity | no more than 85 per cent: FES-2 4.3; no duty within 10 kWh (asserted) |
| 10 Rounding path | unrounded to the end; energies to 10 kWh, payload to 0.1, loss to 0.1 per cent: the prompt (SF12) |
| 11 Tie-break | none: no duty at the limit (asserted) |
| 12 Maturity and censoring | none: the records are complete to their last day |
| 13 Order of operations | duplicates dropped, notes summed per tractor-day, joined, fitted: C1 (SF6) |
| 14 Row order | weighings by time within a CMR: C1 (SF5) |
| 15 Duplicate resolution | a re-uploaded day once, a re-weighed CMR at its later weighing: C1 (SF5, SF6) |
| 16 Identity normalisation | duty codes VMO-nn to Vnn in the bridge log and the notes; trailers by registration: C1 |
| 17 Netting against gross | net payload as gross less stored tare: the bridge's columns (SF33) |
| 18 Dimensional units | kWh, km, tonnes, km/h, hours; three weight formats; SOC in per cent: C1 (SF8) |
| 19 Code and status semantics | the remark on a first weighing (SF5); the drinks maker's scale months (SF18) |
| 20 Integerisation | tractors are whole duties: FES-2 4.3 |
| 21 Clause scope | FES-2 2.1 to 2.3 for the terms, 4.1 to 4.3 for the call |
| 22 Forward window contents | the 2027 model's battery after a year and its weight, the shortlist, the design day, the duty's trailers, drops and speed on it: filed or estimated (SF11, SF21, SF24, SF27, SF32) |

## Literal reader

FES-2 2.1 to 4.3 executed word for word: each shortlisted duty's round trip, with its drops, on a January working day at
-5 C departing with the mean weighed net payload of November 2025 to October 2026, the energy the tractor draws from its
battery, against 85 per cent of 540 kWh less the share a battery permanently loses in its first twelve months in
service as the company's own tractors show it: 438 kWh, eight duties, eight tractors. The route register's "Driving
time h (routing tool)" is the planner's figure and says so; the daily summary's driving time is the tractor's. The
TMS notes' declared weight is the shipper's; the bridge's gross and tare are weighed. The prompt's "forecast from what
our Jönköping pilot tractors drew on their own duties" files the source, not a method.

## Prompt contract

A voice rewrite keeps: the question (which duties go electric, and the order's size), every shortlisted duty's
design-day energy forecast from the pilot and its yes or no, the payload figure per tonne per 100 loaded km, the
first-year permanent loss as a share of usable battery, a spreadsheet and a one-page PDF memo, and the rounding (10
kWh, 0.1 kWh, 0.1 per cent). It never adds: speed, driving time, the routing tool, a trailer, tare, a drop or stop, a
declaration, a weighbridge, a calibration, part or full loads, the terminal against the depot, an early loss or curve,
a cold or temperature form, a holdout, state of charge, a shipper, a file name, the standard by its code, or who is
asking. The first sentence keeps "which" (the shell is redrawn from architecture 8's "how many").

## Tried and rejected

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
