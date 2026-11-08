# task4 design note

## Draw

Card `.claude/skills/fingerprint/cards/task4.json`, architecture 5, registered 2026-11-08 (a re-root: architecture 4,
the Irish retailer's courier hand-over priced set by set on the van runs, came back not stumped on the platform, the
author's report, run texts not supplied to the repo). One architecture per world: a new world (Småland, Sweden), a new
dataset (a battery-electric pilot's duty-day summaries and a terminal weighbridge log), a new organisation family (a
road haulier) and a new shell (how-many | for | pdf+xlsx against which | i'd | png+xlsx, how-many | in | png+xlsx and
whether | the | pptx+xlsx in the lineage).

**Why this draw, from the Sulfur record.** Every Sulfur landing so far (task2 arch 3, task3 arch 2 and 3, task4 arch 3
and 4) was a mechanism the rows visibly carry, modelled on sight and validated on held-out rows of the same stream
(`sulfur-record.md`, Lessons). The one partial stump (task6 arch 6, 73 and 83) was a sampling property the observed
values did not share with the decision unit. This draw takes the record's live ground literally: the decisive
property is one the rows in view cannot show (each declared payload's error structure), the textbook model passes the
only validation the stream allows (held-out pilot days carry the same declarations), the most natural check of the
covariate passes too (declarations unbiased on average), and the deciding evidence sits in a second file at another
grain (the weighbridge, one row per departure of another depot's fleet, the same shippers).

Guard on the registered card: WARN only, `repeat.gate_g` (forecasting after task9 v6): the objective is a forecast of
a duty's battery energy on a day not yet run, and the honest Gate G mechanism is forecasting. Redrawn at the check:
G3 decisive (BLOCK against task5, `ban.pattern`) to G1 (the covariate's value basis swaps between the fit, declared,
and the forecast, weighed), and docx+xlsx (WARN against task5) to pdf+xlsx. `test.same_puzzle_older` against mark140
answered with a differentiation line; mark262 (one classical noise variance carried from a selected subsample) and
mark249 (gains against partly agreeing references) differentiated on the card. Heart nearest 0.06 (mark170).

- **Pairing.** Supply Chain & Logistics (house domain) in its client domain General Statistics & Data Science, task type
  regression, classification and model diagnostics, which serves Forecasting & Predictive Modeling. The deciding
  quantity is each shortlisted duty's battery energy on the January design day of 2027, forecast from a model whose
  payload covariate was recorded by third parties.
- **Niche.** Fryele Åkeri AB, a regional haulier running regular full-load duties for Småland manufacturers from
  Jönköping and Värnamo. Six battery-electric tractors ran nine Jönköping duties from March 2025; the board orders
  battery-electric tractors for Värnamo duties from January 2027 under the haulier's own standard FES-2, at the
  dealer's 2027 model (540 kWh usable).
- **The call.** How many tractors and which shortlisted duties. FES-2 4.1 to 4.3 files the WHAT: a duty goes electric
  when its energy on a −5 °C working day, carrying its planning load (the mean net payload of its departures over the
  twelve months to October 2026), is at most 85 per cent of the ordered model's usable battery; one tractor a duty.
  Forward facing: an order for a year not yet run.
- **Shape.** other: the count and the duties (the call), each of the fourteen duties' design-day energy to the nearest
  10 kWh, a one-page memo. Decision quantity_figure, answer count, question form how-many.
- **Strategy.** other (errors-in-variables with a source-specific error structure). Gap objective (decisive: the fitted
  model predicts the declared stream correctly and is not what the forecast at weighed loads is scored on) then time
  (the design day is a forecast at conditions and loads the pilot's mean does not sit at); generators G1 (unit-of-value
  swap, decisive), G13 (horizon: the heavy and light duties sit far from the pilot's mean load), G16 (the cold form,
  chosen by back-test, the asks' judgment); Gate G forecasting; calibration gold_standard_subsample (the weighbridge);
  context artifact register; Layer 2 family estimation_fit, pattern own:declared-covariate-error-structure-by-source.
- **Forum, event, organisation.** board_of_directors (the December board approves the order), launch_or_rollout (the
  Värnamo charger bank and the first tractors in January 2027), logistics_or_3pl. Role procurement_lead (the fleet
  manager, who places the order).
- **People** (`guard.py names --geo Sweden --seed 505`, locale sv_SE): Georg Pålsson, fleet manager, who owns FES-2 and
  places the order; Inger Norman, transport planner, whose workbook and memo the golden are; Pierre Kjellberg, the
  dealer's key account manager, who signs the quotation. None appears in the prompt.
- **Deliverables.** ev_duty_assessment_2027.xlsx (the duties, energies, verdicts and the count) and
  tractor_order_memo.pdf (one page for the board): xlsx and pdf.
- **Data-native sentence.** A haulier's payload figures are the shippers' consignment-note declarations, and how a
  shipper declares is its own habit: clerks estimating from the order scatter around what the trailer carries, a dairy
  writes one standard weight on every note, a timber merchant prints its own weighbridge ticket; a pilot fitted on
  those declarations predicts its own days well and still halves the energy a tonne costs, which is the quantity the
  heavy steel and ballast duties and the light insulation duty turn on.
- **Abstraction sentence** (the one a reviewer holding this build beside its nearest approved build would say is the
  same, without domain nouns): none writable. Against mark262 (one slope de-attenuated by a single classical noise
  variance measured in a selected subsample and carried to the population) there is no selected subsample and no
  single variance: each source's error is a different structure (classical, Berkson, nil) and the one pooled
  correction is itself a wrong rung; against client example 11 (sampling noise of survey shares, one correction
  concept) the error is a recording practice read from a gold-standard record of the same sources, and the chain
  carries a forecast and a back-tested cold form after it.
- **Same-puzzle and library tests.** Gap objective, G1 and quantity_figure repeat no build in the last twelve
  (`check`); the golden is no named correction applied as a card states it (the textbook reliability correction is
  rung 2 and files the default's list).
- **Sources.** Battery-electric truck energy practice (energy per km rising with payload, cold and climb; manufacturers'
  ranges not used for planning); consignment-note weight declarations and terminal weighbridges; errors-in-variables
  (classical against Berkson error, regression calibration); the client's two-layer standard. All files constructed
  (`metadata.json`), real Swedish town names.

## Default path

1. Read FES-2 sections 2 to 4, the quotation (540 kWh usable, so 459 kWh is the limit), the shortlist and the route
   register (each duty's three legs and climb).
2. Clean the pilot: the daily summaries uploaded twice kept once, joined to the TMS consignments on registration and
   date (2,334 duty-days), declared weights parsed (kilograms, kilograms with a space, tonnes with a decimal comma),
   ambient dropouts filled from the Jönköping station day.
3. Fit the field's consumption model by least squares: battery energy on km, climb times km, the degrees below 16 °C
   and below 0 °C times km, and declared payload times loaded km (payload 1.0 kWh per tonne per 100 km); validate on
   January and February 2026 held out (2.4 per cent error).
4. Take each shortlisted duty's planning load from the weighbridge (last weighing per CMR, gross less tare, November
   2025 to October 2026), predict the design day at −5 °C, and check the weighbridge's declarations against its
   weighed loads: right on average (declared less weighed, −39 kg).
5. Assign the duties within 459 kWh.

Ends on: order 8 tractors, for V02, V03, V05, V07, V09, V11, V16 and V18 (the heavy V03, V07 and V11 at about 440 kWh;
the light V14 out at about 470).

Golden: order 6 tractors, for V02, V05, V09, V14, V16 and V18; V03, V07 and V11 need about 470 kWh and stay diesel.

## Stump sentence

A competent solver fits the pilot's duty-day battery energy on distance, climb, cold and the shippers' declared
payload, finds it predicts held-out January and February days within 2.4 per cent and the weighbridge's declarations
right on average, and orders 8 tractors, sending the heavy steel, ballast and metal duties V03, V07 and V11 (about 440
kWh on that model) and leaving out the light insulation duty V14 (about 470); the estimating shippers' declarations
scatter around the weighed load, so the fitted payload term (1.0 kWh per tonne per 100 km) is under half the loads'
effect (2.2), and only each declaration taken to the weighed load it stands for, shipper by shipper, with the dairy's
standard weight and the timber merchant's ticket left as what they are, orders 6: V02, V05, V09, V14, V16 and V18.

## Deep reasoning

Task type: regression, classification, model diagnostics (General Statistics & Data Science), the client domain the house domain supply-chain-logistics sits in, a task type the taxonomy tags for Forecasting & Predictive Modeling; the forecast is each duty's 2027 battery energy on the January design day.
Domain test: the quantity that decides is the energy a tonne of payload costs per loaded kilometre, a slope on a covariate the pilot holds only as third parties recorded it, so the field's question is the error structure of that covariate (classical, Berkson or nil) and the estimate that structure licenses; put patients and doses in place of tractors and loads and the shipper's declaration habit, the consignment note and the terminal's weighed departures have no counterpart, so the inference that decides has nothing to stand on.
Swap: "how many community nurses should we hire for the 2027 rota, and which rounds should they take, from the pilot's visit times" keeps a fitted time model but loses the third-party declaration whose error differs by who writes it and the weighbridge that weighs the same senders' loads; nothing is recorded by an outside party with its own error, and the call stops reading the same.
Layer 1: the haulier's systems produce it: the fleet portal uploading a day twice after a modem reconnect (same day, later upload stamp), ambient sensor dropouts (blank, the station file covers them), the TMS's declared weight typed three ways (12000, 12 000 kg, 12,00 t), the weighbridge's re-weigh after an axle limit (the CMR weighed twice, the later weighing final), the Värnamo duty codes re-keyed at the April 2026 TMS upgrade (VMO-07 to V07, with the crosswalk in the register), telematics in UTC and the weighbridge in local time, spare tractors on Värnamo duties (tare per weighing), blank declarations on 1.2 per cent of weighings; each is neutral on the call and every graded figure (SF5 to SF8 asserted) and none is placed to be caught.
Layer 2: estimation_fit: the energy model's payload term is estimated on declared weights, and the methodological choice is what each pilot day's payload is taken to be: the declaration, one pooled correction of it, an average consumption with no payload at all, or each declaration's expected weighed load given its shipper, read from the weighbridge.
Decisive step: each pilot day's declared payload is replaced by the weighed load it stands for under its shipper's own declaration practice (scattered estimates drawn toward the shipper's weighed mean, a standard weight taken at the shipper's weighed mean, a weighbridge ticket left as it is), so the energy a tonne costs is estimated on the loads the forecast is made at.
Not semantics: every field read right (the declared weight's three formats, the BMS energy, the re-weighs, the duty-code crosswalk, the planning load's window, the limit's 540 kWh) still leaves the declared payload in the fit: no field says how a shipper declares, the declared and weighed means agree within 4 per cent for every duty, and the model fitted on them validates on held-out days.
Not rule application: FES-2 files the WHAT (2.2 the energy, 2.3 the usable battery, 4.1 the design day, 4.2 the planning load, 4.3 the limit and one tractor a duty) and 3.1 says only that planning figures are estimated from the company's operating records; nothing filed says how the pilot's payload is taken. Enumerated family (declared, one pooled correction, average consumption, a line per shipper, each load at its shipper's mean, the exact shipper's days, a within-duty fit, the moments correction in verify.py): 9, 8, 8 and 6 tractors, payload 0 to 2.4 kWh per tonne per 100 km; standing family (the routes that take each shipper's declarations to the weighed load): 6 tractors on every one, payload 2.1 to 2.4, every energy in the same 10 kWh bin; the ruling-out is loud only to a solver who regresses the weighbridge's weighed loads on the declared ones shipper by shipper.
Analyst test: a strong analyst who cleans the summaries, the consignments and the weighbridge and reads FES-2 and the quotation correctly fits the consumption model on the declared payloads, validates it on held-out days, finds the declarations unbiased on the weighbridge and orders 8 tractors (V02, V03, V05, V07, V09, V11, V16, V18), the default path's Ends on; on the generator's clean truth (no mess) the same route orders the same 8 (checks.py, clean truth).
Estimand: FES-2 2.1 to 2.3 and 4.1 to 4.3 (fleet_electrification_standard_FES-2.pdf) with the quotation's usable capacity: population the shortlisted Värnamo duties (fleet_plan_2027.xlsx), outcome the battery energy of a round trip depot out to depot in, window a January working day at −5 °C mean ambient carrying the twelve-month planning load, unit kWh and tractors, comparison each duty against 85 per cent of 540 kWh.
No decoy: nothing is planted: the declarations are what consignment notes carry, the weighbridge is the terminal's compliance and billing record, the standard and quotation are ordinary documents; no memo, earlier assessment, manufacturer's range or stakeholder figure ranks the duties or states an energy, and no file exists to carry the wrong answer.
No certified replay: the method is not recovered by reproducing a published figure: no file states a duty's energy, a consumption rate per tonne or a shipper's declaration practice.
Chain: (1) the pilot's payload is the shippers' declaration, and the weighbridge shows declarations right on average but scattered around the weighed load, so a slope fitted on them is diluted even though the model validates on held-out pilot days; (2) the scatter is not one error: per shipper the weighed load regresses on the declared at 0.26 to 0.30 for the estimating clerks, the dairy declares one standard weight the weighed load scatters around, and the timber merchant's declaration is its weighbridge ticket (slope 1.00), so one pooled line (0.94, carrying the shippers' differences in load) corrects the slope only to 1.1; (3) each pilot day's declaration is taken to its expected weighed load given its shipper and the model refitted, 2.2 kWh per tonne per 100 km, which the timber merchant's own days confirm (2.2); (4) the cold form is chosen by back-test (one rate below 16 °C under-predicts held-out sub-zero days by 3.4 per cent, two rates by −0.4), and the refitted model at −5 °C and each duty's planning load orders 6 tractors.
Judgment: errors-in-variables: whether each shipper's declared payload carries classical, Berkson or no error is identified from the direction of the weighed-on-declared regression on the weighbridge, a record of the same shippers at another depot and grain; the calibrated payload term (2.2) is checked against the pilot days of the one shipper whose declarations are exact (2.2), and the moments correction in verify.py (the declared spread less the weighbridge's error variance) gives 2.1 and the same six duties.
One-fact test: the likeliest hint ("declared weights are noisy, so the payload slope is attenuated") invites one reliability ratio over the weighbridge, which carries the shippers' differences in load and the exact shippers and corrects the slope only to 1.1 (still 8 tractors), and a per-shipper variance ratio breaks on the dairy's constant declaration; the solver still has to read each shipper's error structure, take each pilot day's load to its weighed equivalent, refit and choose the cold form before the forecast. The other hint ("check the model on weighed loads") has nothing to check against: no pilot day was weighed.
No replay: the call does not re-derive any published figure, and no stated number in the pack is wrong.
Pinned: run on the cut pack and the clean truth (checks.py, verify.py): a line per shipper, each load at its shipper's mean, the exact shipper's slope, a within-duty fit, the 2025 and 2026 halves, the calibration on the last twelve months, the station temperature, hinges at 14, 16 and 18 °C with a second at −2, 0 or 2 °C, a quadratic and 8 °C bins, and the moments correction: every one 6 tractors (V02, V05, V09, V14, V16, V18) and every one of the fourteen energies in the golden's 10 kWh bin; the declared weights, one pooled correction, the average cold-day consumption and the declared fit with one cold rate order 8, 8, 9 and 10.
Run forecast: method shortcut at rung 1 (the consumption model on declared payloads, validated by its own held-out days and the weighbridge's unbiased mean: a self-confirming check); a run that suspects the declarations stops one inference short at rung 2 (one pooled correction, still 8 tractors), an unfinished chain; a run that lands the six with one cold rate below 16 °C misses all fourteen energies by a bin.
Strategy label: WORKS IN FORM (Education 02 and General Statistics, measurement error: the reliability estimated from the pack's own data, never a filed coefficient; here not one reliability but each source's error structure, with the pooled reliability as a wrong rung).
Lesson: a regression on a covariate recorded by third parties predicts its own stream and misstates the effect at true values; whether the error is classical, Berkson or nil is a property of each recorder, read from a record that measures the truth for the same recorders, and no build on file asks for the structure to be read source by source.

## Survivor anatomy

Actor: the deciding property, each shipper's declaration practice, has no column in any file; it is a relation between the declared and weighed weights of one shipper's departures (the direction and slope of their regression), on a file the pilot never touches.
Link: each pilot day's payload is tied to the Värnamo weighbridge only through the shipper code, a key both files carry for their own reasons (billing, compliance) and no sentence connects to the energy model; nothing joins a pilot day to a weighing.
Reflex: the field's consumption model (energy per km on payload, cold and climb, least squares on the operating records) sits at rung 1 and orders 8 tractors (Ends on); the field's average-consumption rule of thumb sits at rung 0 and orders 9.
Back-test: the declared-payload model predicts January and February 2026 held out within 2.4 per cent (the golden 2.3), and the weighbridge's declared and weighed means agree (−39 kg); both checks a solver runs on the easy route pass.
Second use: every file the step reads is in the pack for its own reason: the weighbridge is the planning load's source (FES-2 4.2) and the 20,000-row population file of the Värnamo duties, the TMS is the pilot's only payload and duty record, the shipper register names the shippers.
Shock: nothing moves visibly: the declarations are unbiased, the model fits; sorted on round-trip km, planning load, climb, the default model's energy or the declared mean, the golden six are not an interval (V09 at 21 t goes, V11 at 26 t does not; V14, the second-longest light duty, goes while V33, the lightest and longest, stays).
Pins: FES-2 files the WHAT (the energy, the design day, the planning load, the limit, one tractor a duty) in the haulier's own standard; no filed sentence names a declaration, a weighbridge, a calibration, an error or a shipper (asserted: checks.py searches FES-2 and the prompt).

## Readability screen

Seven tests per rung: 1 a filed sentence names the decisive quantity or sends the solver to it; 2 a column, key or
marker makes it a row predicate or a header-found join; 3 an opponent reflex reaches it; 4 a control or corpus scores
the rules or refutes the naive read; 5 the hygiene battery finds it; 6 one subtraction, ratio or half of a reported
figure; 7 a file the step alone reads.

| Rung | 1 Filed | 2 Schema | 3 Reflex | 4 Bench | 5 Hygiene | 6 Linear | 7 Second use | Verdict |
|---|---|---|---|---|---|---|---|---|
| 0 average consumption on cold days: 9 tractors | FES-2 4.1's design day | the summary's consumption column | yes, the rule of thumb | none | no | a mean | none | readable |
| 1 (default) consumption model on declared payloads: 8 tractors | FES-2 3.1, estimated from operating records | the TMS declared weight | yes, the field's model | the held-out days confirm it | no | a fit | none | readable |
| 2 one pooled correction from the weighbridge: 8 tractors | none | declared beside weighed on one row | yes, the textbook reliability ratio | none | no | one ratio | none | readable |
| 3 (decisive) each declaration taken to its weighed load by its shipper's practice, the model refitted | no sentence names a declaration, an error or a shipper's practice | no column holds a practice; the shipper code is a billing key | no: the reflexes are the declared fit and one reliability ratio | nothing scores it; the held-out check is blind to it | no: declarations are unbiased, no duplicate or clock is involved | not linear: a regression per shipper carried through a refit | the weighbridge is the planning load's file | silent |

**Condition 1 (Gate F risk), measured on the wording.** The prompt asks for "the battery energy its round trip needs on
the January design day"; FES-2 says "the energy the tractor draws from its battery". Nothing in the pack weighs a pilot
day, states a consumption per tonne or describes how a shipper declares. The held-out validation a careful solver runs
(January and February 2026) gives 2.4 per cent for the declared fit and 2.3 for the golden: the stream cannot tell them
apart, because the held-out days carry the same declarations. The evidence sits only in the weighbridge, read shipper
by shipper in the direction weighed-on-declared.

**Condition 2, the forecasting objective.** The design day is a forecast at a temperature (−5 °C) the pilot reached on
394 of 2,334 days below 0 °C and loads (3.9 to 31.9 t) far from the pilot's mean (12.3 t): the energy a tonne costs
decides the heavy and light duties, and the cold form is chosen by back-test (the asks' second judgment).

## Semantic fork table

| ID | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | the design day's temperature | the trucks' ambient mean, the station's day where it dropped out | the station's day throughout | same call and bins | same call (asserted) |
| SF2 | a duty's energy | energy_used_kwh, depot out to depot in | consumption times distance | the same column | FES-2 2.2; identical within 0.5 kWh (asserted) |
| SF3 | the planning load | mean weighed net payload | mean declared weight | same call and bins | FES-2 4.2; same call (asserted) |
| SF4 | the twelve months | November 2025 to October 2026 | calendar 2025, or every month on the bridge | same call | FES-2 4.2; same call (asserted) |
| SF5 | a re-weighed CMR | the later weighing | the first | same call | the remark "axle 2 over" and the later time; same call (asserted) |
| SF6 | a day uploaded twice | once | twice | same call | the same day and figures with a later upload stamp; same call (asserted) |
| SF7 | an ambient dropout | the station day plus the mean offset | the day dropped | same call and bins | same call (asserted) |
| SF8 | a declared weight in tonnes | parsed (decimal comma) | those days dropped | same call | same call (asserted) |
| SF9 | the usable battery | 540 kWh, the 2027 model ordered | the pilot's 468 kWh | moves the call | FES-2 4.3 "the tractor model being ordered" and 2.3; the quotation (asserted) |
| SF10 | the payload of a pilot day | the weighed load the declaration stands for, by shipper | the declaration | moves V03, V07, V11 and V14 | the weighbridge's per-shipper regression; the exact shipper's own days (asserted) |
| SF11 | the cold form | a rate below 16 °C and a further rate below 0 °C | one rate below 16 °C | same call, every energy a bin low | the January and February 2026 back-test: 3.4 per cent against −0.4 on sub-zero days (asserted) |
| SF12 | rounding | each energy to the nearest 10 kWh, every graded energy within 1 kWh of a bin centre | finer | same figures | the prompt; every rival in the golden's bin (asserted) |
| SF13 | tractors | one per duty assigned | a spare | same count | FES-2 4.3 (asserted) |
| SF14 | the fit's window | March 2025 to October 2026 | 2025 alone, 2026 alone | same call and bins | asserted |
| SF15 | the calibration's window | the two years on the bridge | the last twelve months | same call and bins | asserted |
| SF16 | the fit's structure | one level per km explained by climb | a level per duty, then climb | same call and bins | asserted |
| SF17 | the fit's km | the odometer distance | the route register's km | same call and bins | asserted |

## Ladder

| Rung | Construction | Answer | Dies to |
|---|---|---|---|
| 0 | average consumption on days of −8 to −2 °C (1.35 kWh per km) times each duty's km | 9 tractors (the golden less V14 plus V03, V07, V11 and V24) | FES-2 4.1 and 4.2: the energy carrying the duty's load; the pilot's consumption rises with load |
| 1 (default) | the consumption model on declared payloads (1.0 kWh per tonne per 100 km), both cold rates | 8 tractors (V03, V07 and V11 in at about 440 kWh, V14 out at about 470) | the weighbridge: the estimating shippers' weighed loads rise 0.26 to 0.30 t per declared tonne |
| 2 | one pooled correction from the weighbridge (0.94), 1.1 kWh per tonne per 100 km | the default's 8 | the per-shipper regressions: the pooled line carries the shippers' differences in load and the exact shippers |
| 2a | one line over the weighbridge departures of the pilot's own six shippers (0.49), 1.9 kWh per tonne per 100 km | 6 or 7 (V07 within 2 kWh of the limit; the judge's variant 458, this build's 460) | the per-shipper slopes: the line blends Tabergs' exact declarations (1.00) and the dairy's standard weight with the clerks' 0.26 to 0.30, so it estimates no shipper's error |
| 2b | the golden payload with one cold rate below 16 °C | the golden six, every energy a bin low | the January and February 2026 back-test (3.4 per cent under on sub-zero days) |
| 3 (golden) | each declaration taken to its weighed load by shipper, the model refitted (2.2), both cold rates | 6 tractors: V02, V05, V09, V14, V16, V18 | |

- **Margins.** Every duty's golden energy sits at least 9 kWh from the 459 kWh limit (the heavy V03, V07 and V11 at
  470, V14 at 450; asserted at 9.0); the default's heavy duties at least 8 kWh inside it and its V14 at least 5 outside
  (asserted). The standing family's spread on any duty is under 5 kWh; the 1h rung's shift is 7 to 8.
- **Position.** Three wrong lists (9, 8, 10 with the declared one-rate fit); the decisive move reverses rung 1's direction
  on the heavy duties and on V14 together, because the slope pivots about the pilot's mean load (12.3 t).
- **Pricing.** The residue the WHAT leaves is the payload term (a method, not a knob); the move the call needs is about
  30 kWh on the heavy duties against a ceiling of 1.2 kWh per tonne per 100 km times 16 t times 150 km (29 kWh), so the
  heavy duties were placed at 26 to 32 t; the one-group-by route (the declared fit) is affine in the declared column
  and lands 8; the standard error of the golden slope is about 0.05 kWh per tonne per 100 km (under 1.5 kWh on any
  duty); the lever (the slope) and the ranked quantity's noise are different variances.
- **Worth.** The decisive step moves four duties and the count from 8 to 6.

## Closure table

| Axis | Reading here | Move |
|---|---|---|
| 1 Population | the shortlisted Värnamo duties | filed, fleet_plan_2027.xlsx and FES-2 4.4 |
| 2 Unit of account | a duty, one tractor each | filed, FES-2 4.3 (SF13) |
| 3 Attribution window | a January working day at −5 °C | filed, FES-2 4.1 |
| 4 As-of dating | the extracts to 30 October 2026, the memo of 6 November | C1: the call reads no later record |
| 5 Version basis | FES-2 version 2, quotation Q-26-1187 | filed |
| 6 Denominator | the 540 kWh usable battery | filed, FES-2 4.3 and the quotation (SF9) |
| 7 Weighting | each departure weighs once in the planning load | filed, FES-2 4.2 |
| 8 Window length | twelve months for the load | filed, FES-2 4.2 (SF4) |
| 9 Boundary inclusivity | no more than 85 per cent | filed, FES-2 4.3; no duty within 9 kWh (asserted) |
| 10 Rounding path | energies unrounded to the end, to 10 kWh | the prompt; C1 (SF12) |
| 11 Tie-break | none | no duty at the limit (asserted) |
| 12 Maturity and censoring | none: the record is complete to its last day | n/a |
| 13 Order of operations | duplicates dropped, then joined, then fitted | C1 (SF6) |
| 14 Row order | weighings by time within a CMR | C1 (SF5) |
| 15 Duplicate resolution | a re-uploaded day once; a re-weighed CMR at its later weighing | C1 (SF5, SF6) |
| 16 Identity normalisation | Värnamo duty codes through the register's crosswalk | C1 |
| 17 Netting against gross | net payload as gross less tare | C1, the weighbridge's gross and tare columns |
| 18 Dimensional units | kWh, km, tonnes; declared weights in three formats | C1 (SF8) |
| 19 Code and status semantics | the remark on a first weighing | C1 (SF5) |
| 20 Integerisation | tractors are whole duties | filed, FES-2 4.3 |
| 21 Clause scope | FES-2 4.1 to 4.3 for the call, 2.1 to 2.3 for the terms | filed |
| 22 Forward window contents | the 2027 model's battery, the shortlist, the design day | filed (SF11 the cold form, chosen by back-test) |

## Literal reader

Executed word for word, FES-2 4.1 to 4.3 assign each shortlisted duty whose energy on a −5 °C working day, carrying the
mean net payload of its departures from November 2025 to October 2026, is at most 85 per cent of 540 kWh, one tractor
each; 3.1 sends the estimate to the company's operating records of its battery-electric tractors, and the one step the
text leaves open is how that estimate is built from records whose payloads are declarations; every route that takes
each declaration to the weighed load it stands for gives the golden six, while the declared fit, the pooled correction
and the average consumption are estimates of another payload. SF1 to SF17 close every term and convention.

## Oracles

None. No file states a duty's energy, a consumption per tonne, a shipper's practice or a range; the quotation gives
the usable capacity only; the fuel card statement and the workshop log (distractors) rank nothing on the decision
basis; the pilot's own consumption column is the energy over the distance, which the default path already reads.

## Ask sheet

Two asks, 15 figures, every one computed from the deep step's output: the order (1, the count and the duties, the call
itself) and each shortlisted duty's design-day energy (14). The energies' second judgment is the cold form (SF11): a
run that lands the six with one cold rate below 16 °C files every energy a bin low.

| Ask | Figures | Deep-step output it reads | Second judgment | Shallow run against the golden | Landed run's risk | Mess on its path |
|---|---|---|---|---|---|---|
| 1 the order | 1 | the payload term | none | 8 tractors | none | the duplicates, the formats |
| 2 the design-day energies | 14 | the payload term and the planning loads | the cold form | 12 of 14 differ | 14 of 14 a bin low | the re-weighs, the crosswalk, the dropouts |

| Ask figure | Golden | Shallow (the default path) | Cracker (lands the six, one cold rate) |
|---|---|---|---|
| 1 the order | 6, V02, V05, V09, V14, V16, V18 | miss | keep |
| 2 energies V02, V03, V05, V07, V09, V11, V14, V16, V18, V21, V24, V33 | 430, 470, 440, 470, 420, 470, 450, 430, 440, 490, 480, 490 | miss | miss |
| 2 energies V27 and V30 | 490, 480 | keep | miss |

- **Span:** the summaries, the consignments, the register, the weighbridge, the standard and the quotation; no ask
  reads a file the call does not.
- **Realism:** a duty-by-duty energy table against the battery is what a fleet planner takes to an order.
- Shallow keep: 13.3 per cent of ask weight (2 of 15 figures).
- Pair ceiling: 34.0 (the landed run C = 38 + 7 + 55 x 0.067 = 48.7, the shallow run S = 5 + 7 + 55 x 0.133 = 19.3).
- Measured by: generator/ceiling.py on the cut pack (pack digest printed with the sheet).

## Prompt contract

What the author's voice rewrite may not drop or change:
- The question: how many battery-electric tractors to order for the Värnamo duties on the 2027 shortlist, and which of
  those duties they take over under FES-2.
- The hold option is implicit in "how many" (none may qualify); never "which six" or any count.
- Deliverables: ev_duty_assessment_2027.xlsx (every shortlisted duty with its round trip's battery energy on the January
  design day and whether it goes electric, ending on the number of tractors) and tractor_order_memo.pdf (the order
  written up for the board on one page).
- Units and rounding: energies to the nearest 10 kWh.
- Never add: a declaration, a weighbridge, a payload, a weight, a shipper, a calibration, an error, cold, temperature
  forms, "check", "validate", or any method word.

## Leak rulings

- leak.py sweep 3, FES-2's "2.2": a section number, not the golden's payload figure; harmless.
- leak.py sweep 3, the quotation's 540 kWh: the WHAT (FES-2 4.3's usable battery), filed once at authority; harmless.
- leak.py sweep 3, FES-2 carries the call's words: the standard governs the call (battery-electric, duties, Värnamo is
  not named in it); it names no duty, energy or count; harmless.
- leak.py sweep 4, FES-2 shares payload, record, standard, planning, consumption with the stump paragraph: payload
  appears only in 4.2's planning load, consumption in 3.1's exclusion of manufacturers' figures; neither names a
  declaration, a weighbridge or an error; the reader quoted nothing for question 1; harmless.
- leak.py sweep 11, the prompt's shell quota and files up front: WARNs for the author's voice rewrite.
- Reader, question 5, FES-2 4.2's window end inferred from "the last full month before the assessment": the pack's
  latest records end 30 October 2026 and the quotation is dated 2 October, so the window is November 2025 to October
  2026; SF4 asserts the same call under calendar 2025 and under every month on the bridge; harmless.
- Reader, question 6, "the decision may reduce to cleaning plus the filed 4.3 rule if the model is simple": that is
  the default path (rung 1), which orders 8; the call turns on the payload term (SF10).

## Tried and rejected

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
