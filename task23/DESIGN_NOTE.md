# task23: the cheapest 2027 gas collection package that keeps Fernhallow Regional Landfill at or under Kelloway County Council's 2027 methane limit, and what the landfill actually emitted in 2025

## Draw

Subdomain: Physical & Environmental Sciences (emissions inventory)
Analysis type: Comparative Analysis & Explanation
Answer shape: a bridge that reconciles two totals: the division's 2025 greenhouse gas report figure (2,149 t) and the
  state's 2025 tracer survey figure (3,537 t), each carried to the site's actual 2025 emission (4,924 t) bar by bar,
  with the 2027 package call on top
Weight: synthesis: no instrument holds the landfill's emission, and the work is pulling seven partial ones (the
  reporting rule's method, the state's tracer campaigns, the division's drone flights, three automated chambers, the
  wellfield readings, the gas plant's flows and the 2019 oxidation study) into one 2025 figure and one 2027 forecast
  that add up; none of the last three builds (task9, task13, task20) put its weight there
Data-native sentence: no file holds what Fernhallow emits: the gas plant and the wells see the methane collected,
  the tracer campaigns and the drone flights see the whole site for a few hours of dry, steady weather, the chambers
  see a fraction of a square metre every hour, the 2019 plots see oxidation at 2019's fluxes, and the scale tickets see
  the waste that will make 2027's gas, so the annual figure and the forecast exist only as a reconciliation of
  instruments that each miss a different part
People: drawn with `guard.py names --geo us --seed 2323`: Nathan Wheeler (the division's landfill gas and compliance
  engineer, who files the greenhouse gas report, flies the drone surveys and keeps the well register; he asks and is
  not named in the prompt); Diane Martinez (Tessaline Environmental's project lead on the state's 2025 and 2026 tracer
  survey)
Decision: in January 2027 the Kelloway County Solid Waste Division brings to the County Council the least-cost package
  from its 2027 gas collection options (A, the plan of record with cell 5's collection at final grade in 2029; B,
  horizontal collectors in cell 5's completed lifts from May 1; C, B with pumps in cell 4's flooded wells from May 1;
  D, C with 18 vertical wells and pumps across cell 5's completed area from June 1; E, D with a geomembrane cap on cell
  4's slopes from October 1) expected to keep Fernhallow's 2027 methane emissions at or under the 5,100 t limit in
  Council Resolution 2025-41, in a year of normal weather; forward-facing (the year is 2027's), with the 2025
  reconciliation as the evidence the Council asked for once the state's survey and the division's report disagreed.

Card: `.claude/skills/fingerprint/cards/task23.json`, architecture v1, PASS against every card on file (skeleton
severity none against everything, the client corpus and the slot's lineage). Redrawn at filing: the gap and decisive
generator (objective with G2 repeated task7 v11's puzzle and a task8 lineage driver; the deciding step is the forward
window's cell 5 carried from a record that is not the operation, so time with G3); the deliverables (docx and xlsx
repeats task9, pdf and xlsx task20; a workbook and the Council deck). Relabelled at build (guard check PASS): the
context artifact is the division's 2025 greenhouse gas report (a period-end summary answering the rule's reported
figure correctly), generators G3, G14, G16. The voice gate's shell-quota WARN (deliverable set pptx and xlsx) is the
Council's own medium; the surface guard's one promoted pair (task22, the shared G3 label) is adjudicated in
pipeline.json: no shared step, data structure or answer shape.

## Stump screen

Written at the draw, before the card was registered and before any code. Six candidates through the nine tests (1 off
the closed page, 2 not a reflex, 3 nothing filed, 4 clean data, 5 two records at two grains, 6 the waved-through
assumption with its precedent, 7 a plausible shallower story, 8 across the data, 9 worth the call); the three strongest
independent ones kept. Magnitudes as measured on the cut pack: the 2025 campaigns' hours ran at 0.711 of the year's
mean emission (2026's at 0.792, the drone flights' at 0.736); cell 4's generation rose 85.1 per cent from 2022 while
its collected gas rose 28.7 per cent; cell 5's daily cover oxidized 39.3 per cent of the flux through the study's
plots on average and will oxidize 17.1 per cent of cell 5's methane in 2027.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Leachate recirculated into cell 4 since April 2023 sped its waste's decay and flooded the lower wells' screens, so cell 4's collected gas rose little while its generation rose; cell 5 takes recirculation from July 2026 | recirculation has not changed cell 4's gas because its collection barely moved, so cell 5 is carried at the dry decay rate (L02, L26, N04) | the monthly wellfield readings with liquid levels (the wells the leachate never reached and the wells given pumps in June 2025 rise, the flooded ones fall) against the recirculation log | none | kept |
| Gas stored in the waste leaves as barometric pressure falls and is held as it rises; the state's tracer campaigns and the division's drone flights both fly in dry, steady weather after fronts, on rising pressure | the campaign days stand for the year, and two independent programs agreeing confirms the level (N12, L28) | the automated chambers' hourly fluxes and the site barometer (hourly) against the campaign-level estimates | none (test 1 answered: near the closed fieldwork-timing card by family only; no seasons and no groups compared, and the fix is the gas's physical response to the pressure path carried hour by hour, conserving mass) | kept |
| Cover-soil methanotrophs oxidize a nearly fixed amount per square metre, so the share oxidized falls as the flux rises; cell 5's cover over fresh, wetted waste runs in 2027 at fluxes far above its spring 2026 flux and most of the 2019 daily-cover plots | the study's oxidation share for daily cover (or the reporting rule's default) carries to cell 5 (N04, L22) | the 2019 plot-level paired fluxes and isotope oxidation shares against cell 5's flux from its own generation | none | kept |
| Young waste in the uncollected cell 5 makes a growing share of 2027's gas, so 2025's site-wide collection efficiency overstates 2027's | the site-wide ratio carried forward (N01, N21) | scale tickets by cell and the well register | 1 (the closed transport card: a pooled rate carried to a target with a different mix) and 2 (the packages are defined cell by cell, so every run forecasts by cell, R25) | not kept: a reflex step in the chain |
| The engines' exhaust carries some methane unburned while the reporting method books destruction at 99 per cent | slip taken as the rule's 1 per cent (N21) | the engines' emission test reports against the plant's fuel flow | 9 (about 40 t a year, inside the golden family's spread) | not kept: Layer 1 |
| Construction debris, biosolids and cover soil weighed in with municipal waste | every ton counted at the municipal waste potential | the scale tickets' material codes | 2 and 4 (a material code read and a filter) | not kept: Layer 1 |

## Deep reasoning

Task type: emissions-inventory (the client's Physical & Environmental Sciences task types nearest it: physical-model
  calibration and data assimilation; sensor calibration and measurement uncertainty), which serves Comparative
  Analysis & Explanation
Domain test: every result is a quantity a landfill gas engineer or an emissions inventory analyst estimates: waste in
  place by cell and its methane potential, first-order decay at the rate each cell's moisture sets, collection
  efficiency by well and cover, the methane a cover soil oxidizes as a function of the flux through it, and an annual
  emission from short whole-site tracer measurements carried through the gas the waste holds and releases as barometric
  pressure moves; the call is the cheapest collection package under a methane limit
Swap: "the cheapest of five warehouse retrofit packages that keeps 2027 energy use under the board's limit, given that
  the meters agree and the audit disagrees" keeps the shape and loses every judgment: no gas is held and released with
  the barometer, no record barely moves because the same liquid both sped the source and blocked the collector, and no
  soil removes a smaller share as the flux through it rises
Where the weight sits: R7, the 2027 emission under each package: it needs the 2025 and 2026 measurements carried to
  every hour (R2's correction), cell 5's 2027 gas from its own spring 2026 level on the decay cell 4's dry and pumped
  wells show for recirculated waste (R3, R4), cell 4's uncollected gas from its 2026 balance with the pilot's pump gain,
  and the cover's oxidation at each cell's own 2027 flux (R5), month by month for five packages with their in-service
  dates; long because each input comes from a different instrument at a different grain, not because one step is clever
Layer 1: 1,136 voided tickets beside their reissues under the same ticket number (tare keying errors, some with
  negative nets), tickets with no disposal area (weekend and public loads before the September 2022 software change,
  and two scale-software outages in August 2025 and March 2026) and the material codes renamed on July 1, 2021; the
  historical tonnage by cell with 1991 and 1992 estimated; the gas plant's hourly export on the local wall clock (the
  fall-back hour repeated, the spring hour missing), analyzer calibration hours reading zero and engine outages; well
  readings with liquid levels quarterly (a depth or DRY) and oxygen intrusion readings; a well register with a blank
  cell on some wells; the station's barometer re-sited in June 2023 (a 0.6 hPa step) and its rain gauge clogged for
  nine days in November 2021; the chambers on UTC with QC-flagged hours and cell 5's chamber only from February 2026;
  the contractor's and the division's documents in their own units (kilograms an hour, short tons, metric tons,
  standard cubic feet a minute); none moves a graded figure outside its band once handled the way every careful run
  handles it (checks.py R2)
Not one thing: each stump fixed alone on the careful route leaves package A (the recirculated decay alone files A at
  4,574 t, the pressure response alone A at 4,986, the saturating oxidation alone A at 4,211); each dropped alone from
  the golden moves the call (to B, C and C); a run that nails any one still misses at least five of the eight results
One-fact test: the most useful single sentences rescue one result each or none: the recirculation sentence ("cell 4's
  collected gas is flat because the leachate that sped its decay also flooded its lower wells; the wells it did not
  flood show the faster decay") rescues R3, the pressure sentence R2, the oxidation sentence none, 1 of 8 at most;
  none rescues R4, R6, R7 or R8 (effort.json hints, computed)
Not semantics: every field, unit and clause read correctly (the tickets' materials and short tons, the plant's
  standard flows, the liquid levels, the campaign report's kilograms an hour, the study's isotope shares, the options
  paper's in-service dates) still leaves the campaigns' hours to carry to the year, the faster decay to read on the
  wells the leachate did not flood, and the oxidation to evaluate at a flux most of the study's plots never reached
Not rule application: the reporting rule's method gives the report's figure, and the Council's limit and the options
  paper's design capture fix the call's terms; no filed procedure corrects a measurement for the pressure path, reads a
  decay rate off unflooded wells or evaluates oxidation at a new flux, and what is left once every filed rule is
  applied is three estimations from three instruments
Estimand: the Council resolution files the limit (methane leaving the site to the atmosphere over calendar 2027, from
  every surface and from the flare and engines, in metric tons) and that the division brings the least-cost package
  expected to meet it in a year of normal weather; the options paper files each package's works, in-service dates,
  design capture and cost; the prompt files 2025 for the reconciliation and the report's bridge in the order of its own
  equation, cell 5's municipal waste through October 2026 in short tons, cell 4's generation change from 2022 to the 12
  months to October 2026, cell 5's 2027 generation and the cover's 2027 oxidized share if nothing changes
No decoy: no memo or draft argues a package; the 2025 greenhouse gas report's figure reproduces exactly by the
  reporting rule's own equation (8,354 t collected over the area-weighted collection efficiency 0.7844, the rule's 10
  per cent oxidation and 0.99 destruction) and answers a shallower quantity, priced on the golden's footing by the
  bridge (R6); the state survey's figure reproduces exactly as its 2025 campaigns' mean rate times 8,760 hours and is
  priced the same way
No replay: no result re-derives a published figure as the answer; the report's and the survey's figures are the
  bridge's starting points, each superseded by the reconciliation
Pinned: R2's rivals (the exponential pressure lag fixed at 12 or 20 hours, cell 4's chamber alone, all three
  chambers pooled, the campaigns weighted with the drone flights) land inside its 10 per cent band at 4,847 to 4,940 t,
  and the stage 4 judge's own reading (all three chambers, a 16-hour half-life not chosen by fit) at 4,693; the
  pressure's 12- and 24-hour changes are ruled out by the chamber record (unexplained variance 694 and 674 against 509
  for the fitted lag) and still land inside it; R3's zones read from the register's pumps or the work orders give the
  same wells; R4 and R7's rivals (cell 5 on cell 4's methane potential, the level from the closed cells' collected gas
  at their design collection, the faster decay ramped over three or six months, package C's gain as the pilot's mean
  flow ratio, cell 4's efficiency held at its autumn 2026 level) land inside their bands; R5's rivals (a logistic in
  the log of the flux, a capacity with its own half-saturation flux) land at 17.0 and 18.9 per cent against 17.1
Run forecast: R2 lost by a self-confirming check (the campaigns and the drone flights agree, so the level is taken),
  R3 by dismissed own evidence (the per-well readings show the rise, the cell total is filed), R4 by an unfinished chain
  (cell 5 carried at the dry decay), R5 by a method shortcut (the study's cover-type mean), R6 by the bars sized on the
  campaigns' level, R7 and R8 by the three together; R1 earned
Strategy label: OWN (no client strategy carries a landfill methane balance; the client's emissions-table ETL strategy
  is the nearest by task type and shares no step)
Depth level: 5: three independent judgments each necessary alone (the recirculated decay read past the flooded wells,
  the campaigns carried through the pressure response, the oxidation evaluated at cell 5's own flux), none sufficient
  alone on the reflex route, the single drops landing on B and C and the reflex route on A
Lesson: a record can barely move because one cause moved two of its terms the opposite way, so a source's response is
  read on the part of the instrument the second effect did not reach and carried to a unit that has no instrument yet;
  a measurement program's agreement with another program that samples the same weather validates nothing; a removal
  that saturates is evaluated at the flux it will meet, and a constant share cancels between a calibration and a
  forecast that a saturating one does not. No build on file teaches the first or the third, and the second sits on one
  live build as a supporting step

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the municipal waste placed in cell 5 from its opening through October 2026, in short tons (574,197) | assembly-reconciliation | the scale tickets (voids and reissues, the daily log's active cell for tickets without a disposal area), the material codes | within 1 per cent | narrow look (the quick read): every ticket summed as filed, voids, reissues and cover soil included (648,207); the careful but hurried pass earns it | - | Ask 3 |
| R2 | the site's actual methane emission in calendar 2025, in metric tons (4,924) | missingness-measurement | the 2025 campaigns and drone flights, the automated chambers' hourly fluxes, the site barometer; the resolution's definition | within 10 per cent of the golden | self-confirming check: the campaigns' mean rate times the year's hours (3,537), confirmed by the drone flights (3,832) | - | Component 1 |
| R3 | the per cent change in cell 4's methane generation from calendar 2022 to the 12 months to October 2026 (+85.1) | investigation-loops | the monthly wellfield readings with liquid levels, the well register's pumps and the work orders, the recirculation log | within 8 points of the golden | dismissed own evidence: cell 4's summed collected gas (+28.7 per cent), the flooded wells' fall read as cell 4's own | - | Component 2 |
| R4 | the methane cell 5 will generate in 2027, in metric tons (3,752) | forecasting | the scale tickets and the 2027 fill plan, the cell-resolved 2026 campaigns, the options paper's recirculation sentence, R3's decay | within 12 per cent of the golden | unfinished chain: cell 5's spring 2026 level from the uncorrected campaigns carried on the dry decay with the study's share (959) | R1, R3 | Ask 5 |
| R5 | the share of the methane reaching cell 5's cover in 2027 that the cover oxidizes if nothing changes, per cent (17.1) | modeling | the 2019 study's paired plot fluxes and isotope oxidation shares, R4's flux, the station's soil temperature normals | within 4 points of the golden | method shortcut: the study's daily-cover mean (39.3 per cent) | R4 | Ask 6 |
| R6 | the bridge from the 2025 report's figure (collection efficiency +3,280, then oxidation -467, then everything else -38) and from the 2025 survey's figure (the hours the campaigns did not sample, +1,387) to the actual 2025 emission, in metric tons | decomposition-attribution | the reporting rule's equation as the report files it, the survey's annualisation, R2; the prompt's order | collection within 15 per cent, oxidation within 250 t, the survey's gap within 490 t | method shortcut: the bars sized to the survey's level, so the survey has no gap and the report's collection bar is about a third short (2,274) | R2 | Ask 2 |
| R7 | the 2027 emission under each package A to E in a year of normal weather, in metric tons (6,942; 6,385; 5,549; 4,495; 4,095) | forecasting | the options paper's works, dates and design capture; R2's correction on the 2026 campaigns, R3's decay, R4, R5; the pilot wells | each within 7 per cent of the golden | unfinished chain: cell 5 on the dry decay, the campaigns' level and the study's oxidation, every package 40 per cent or more low (A 4,015) | R2, R4, R5 | Component 3 |
| R8 | the cheapest package that keeps 2027 at or under the Council's limit (package D) | synthesis | the resolution's limit (5,100 t) and least-cost rule; R7 | exact | method shortcut: package A on the three hurried judgments together (each alone gives B or C) | R7 | Recommendation |

Carry-forward: R1, R2 and R3 stand on inputs of their own (the tickets; the campaigns, flights, chambers and barometer;
the wellfield readings); R4 falls with R3 (and with R1's tonnage), R5 with R4's flux, R6 with R2, R7 with R2, R4 and
R5 together and R8 with R7. A run that misses the pressure response keeps R1, R3 and R5's method; one that misses the
offsetting record keeps R1, R2 and R6; one that misses the saturation keeps R1, R2 and R3.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| leachate recirculation speeding the decay of the waste it reaches while raising liquids over the lower wells' screens | constructed (the simulated landfill's moisture, decay and wells) | no: 26 of cell 4's 58 wells at their own liquid levels since 2023, the eight pilot pumps of June 2025, and cell 5 from July 2026 | modelling: per-well flows against liquid levels and pumps, a decay fitted on the wells the liquids did not reach | modelling | keep |
| gas held in the waste on rising pressure and released on falling pressure, with fair-weather measurement days | constructed (the simulated weather and gas transport) | no: every hour of the record, every chamber (cell 3's geomembrane cap breathes too), every campaign and flight at its own weather | modelling: chamber flux against the pressure path with a fitted lag, each campaign's hours placed on it | modelling | keep |
| cover oxidation saturating with flux | constructed (the simulated cover soils) | no: every plot of the 2019 study across three covers and four visits, every cell's emission | modelling: the oxidized share against flux across plots, a saturating form evaluated at a new flux | modelling | keep |
| the site's methane potential below the reporting default | constructed (the simulated waste stream) | no: every cell's waste since 1986 | calibration: the corrected campaigns or the closed cells' collected gas against the decay model | modelling | keep, a supporting step (an uncalibrated default files no package) |
| the 2027 gas shifting to the uncollected cell 5 | constructed (the filling sequence) | no: the shift runs through every year as each cell fills | a targeted query: tonnage by cell and the well register | routine | keep, a reflex step (the packages are defined cell by cell) |
| construction debris, biosolids and cover soil at the scale house | constructed (the simulated waste stream) | no: every day's tickets | a targeted query: the material codes | routine | keep, R1 only |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 the municipal waste placed in cell 5 through October 2026, in short tons | Missed | Right | Right |
| R2 the site's actual methane emission in 2025, metric tons | Missed | Missed | Right |
| R3 the per cent change in cell 4's methane generation from 2022 to the twelve months to October 2026 | Missed | Missed | Right |
| R4 the methane cell 5 will generate in 2027, metric tons | Missed | Missed | Right |
| R5 the share of the methane reaching cell 5's cover in 2027 that it oxidizes, per cent | Partly | Missed | Right |
| R6 the bridge from the 2025 report and the survey to the actual 2025 emission, metric tons | Missed | Missed | Right |
| R7 the 2027 emission under each package in a year of normal weather, metric tons | Missed | Missed | Right |
| R8 the cheapest package that keeps 2027 at or under the limit | Missed | Missed | Right |
| Roughly | 0.5 of 8 | 1 of 8 | 8 of 8 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (the passes are the generator's own routes on
  the cut pack: the quick pass the tickets summed as filed, the report's figure taken as the emission, cell 4's
  collected gas, cell 5 on the rule's default decay and the rule's 10 per cent; the careful pass every file conformed,
  the campaigns' level confirmed by the drone flights, one decay for every cell with the pilot pumps' gain and the
  cell-level forecast, the study's cover-type oxidation; the golden)
Largest single hint: "Waste holds gas while the barometer rises and lets it out as it falls, and the campaigns only
  fly on settled days after fronts"; rescues 1 of 8 results (R2); the recirculation sentence rescues R3 alone and the
  oxidation sentence none
Pair estimate: 20.8 (the careful pass earns R1 and the instruction-following share; every lost cell cites a
  precedent of its own class; quick 13.9, thorough 100)

## Stump factorial

Reflex route: every file conformed and every document read, the tickets' voids and missing disposal areas handled,
  the report's figure reproduced from its own equation, the pilot pumps' gain read from the pumped wells, the forecast
  built cell by cell as the packages are defined, a decay model calibrated on the measurements; with the campaigns'
  level taken as measured (confirmed by the drone flights), cell 4's collected gas read as its generation, and the
  study's cover-type oxidation; it files package A (A at 4,015 t, every package under the limit)

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| J1 the recirculated decay read on the wells the leachate did not flood, carried to cell 5 from July 2026 | stump | cell 4's collected gas read as no change in its decay; cell 5 on the dry decay | L02, L26, N04 | package B (B at 5,011 t, C at 4,114) | package A (A at 4,574 t; rescues R3, 1 of 8) | no: the faster decay has to be fitted on the unflooded and pumped wells and carried to a cell with no wells |
| J2 the campaigns and drone flights carried to every hour through the pressure response the chambers record | stump | the campaigns' mean rate times the year's hours, confirmed by the drone flights | N12, L28 | package C (B at 5,190 t, C at 4,370) | package A (A at 4,986 t; rescues R2, 1 of 8) | no: the response and its lag have to be fitted on the chamber record and each campaign's hours placed on it |
| J3 the cover's oxidation evaluated at each cell's own flux | stump | the 2019 study's mean share for each cover | N04, L22 | package C (B at 5,443 t, C at 4,735) | package A (A at 4,211 t; rescues none) | no: the share has to be fitted against flux across plots and evaluated at a flux most daily-cover plots never reached |
| J4 the forecast built cell by cell, each package acting on its own cell | reflex | a site-wide collection efficiency carried | R25 | same call | - | - |
| J5 the report's figure reproduced from its own equation | reflex | none | R18 | same call | - | - |
| J6 the pilot pumps' gain read from the pumped wells' flows | reflex | none | R14 | same call | - | - |
| J7 the tickets' voids, reissues and missing disposal areas | reflex | none | R01 | same call | - | - |

Level: 5 (three necessary stumps, none sufficient, the single drops on two distinct wrong answers, B and C, the
  reflex route on A; effort.py factorial PASS)

## Data provenance

Source: generated by task23/generator from a simulated regional landfill and its instruments: hourly weather on site
  since 2016 (frontal passages with the semidiurnal pressure tide, rain, wind, warm and cold spells, air and soil
  temperature), five cells filled from 1986 with their waste by material and month, first-order decay with a
  six-month methanogenic lag on each vintage, leachate recirculation in cell 4 from April 2023 and cell 5 from July
  2026 speeding the decay of the waste it reaches and raising liquids in the wells, a gas collection system of 114
  wells with an enclosed flare and two engines, cover soils that oxidize methane with a capacity set by cover and soil
  temperature, barometric pumping of the gas the waste holds, and the instruments that see it: scale tickets, the gas
  plant's hourly record, monthly wellfield readings, three automated chambers, the state contractor's tracer
  campaigns, the division's drone flights and the 2019 oxidation study
Behaves like the real thing: emissions fall on rising pressure and rise on falling pressure with a lag of hours, as
  chamber and eddy-covariance records at landfills show; recirculated cells generate faster and flood their wells, the
  bioreactor operators' commonest collection problem; the share of methane a cover oxidizes falls as the flux rises, as
  isotope studies of landfill covers find; a site's methane potential sits below the reporting default as modern waste
  carries less paper and food; tracer campaigns and drone mass-balance flights fly only in dry, steady wind
Genuine patterns: (1) the scale house's weekday, holiday and seasonal tonnage with a growth trend; (2) the synoptic
  pressure cycles and the semidiurnal pressure tide; (3) the gas plant's engine availability and the slow decline of
  the closed cells; (4) the oxidation's soil temperature seasonality, with warm and cold spells and years; (5)
  well-to-well heterogeneity in yield, oxygen intrusion and liquids; (6) the chambers' diurnal temperature cycle and
  rain response
Problems by process: voided and reissued tickets with tare errors and missing disposal areas (the scale-house
  operator and two software outages), the material code rename of 2021 (the software change), the plant's local wall
  clock and its analyzer calibration hours (the SCADA historian), quarterly liquid levels and oxygen intrusion readings
  (the wellfield technician), a re-sited barometer and a clogged rain gauge (the station), chamber QC hours and a
  chamber added in 2026, two estimated years in the historical tonnage
Breadth: 22 files; 212,294 scale tickets, 94,537 hours of weather, 33,600 hours of plant record, 10,223 readings on
  114 wells, three chambers (34,143 hours), eight campaigns, ten drone flights and 44 oxidation plots; deciding which
  instruments see which part of the emission is the work

## Template check

Chain signature: assembly-reconciliation, missingness-measurement, investigation-loops, forecasting, modeling,
  decomposition-attribution, forecasting, synthesis
Question form: what (the cheapest package under a limit), with what (the actual 2025 emission and its bridge)
Nearest build: task4 v13 (a bridge, weight attribution): no shared area order, weight or lesson; task20 v4 (a
  forecast with drivers, weight hard-to-measure): no shared lesson or file role; task22 v2 (a balance whose largest
  term is measured at its own physical state): it shares the field family of an instrument whose reading needs a
  physical correction, not the step (its temperature basis against this build's pressure path, offsetting record and
  saturating removal)
Abstraction sentence: the nearest build and this one would not be read as the same sentence: task22 converts one
  term with a proxy that decoupled in the target year; this build reconciles a facility's release from instruments that
  each miss a different part and forecasts it for a unit no instrument yet covers

## Frontier check

Precedents: R2 N12 and L28 (a rate learned in one condition carried to all hours; certified by a second program that
  shares the condition); R3 L02 and L26 (its own per-well output shows the rise, the cell total is filed; a
  plausible shallower story); R4 L11, L02 and N04 (the split built for cell 4 and dropped for cell 5; the decay
  carried to the new cell without the response measured); R5 N04 and L22 (a published constant oxidation share whose
  generating assumption the plots contradict); R6 N12 and L22; R7 L11, N12, N04 and L22; R8 N12, N04 and L22
Shallow path checks: R2's hurried level passes the drone flights' agreement (their 2025 mean, 3,832 t a year, sits
  within 9 per cent of the survey's 3,537); the check of another kind is the chamber record at hourly grain: the 2025
  campaigns' hours ran at 0.711 of the year's mean, the 2026 campaigns' at 0.792 and the drone flights' at 0.736. R3's
  hurried figure passes the plant's total and a single-decay back-test of the site's collected gas; the check of another
  kind is the per-well readings: the 32 wells the leachate never reached rose 26.3 per cent and the eight pumped wells
  149.1 per cent while the flooded wells fell. R4's passes the spring 2026 campaigns exactly (it is calibrated on
  them); the check of another kind is R3 carried to cell 5's own recirculation. R5's passes the study's own daily-cover
  interval; the check of another kind is the plot-level share against flux across all three covers. R7 and R8's pass
  every 2026 campaign; only the three checks above refute them
Assumption made false: that the campaigns' days stand for the year (false because the waste holds gas on rising
  pressure and the campaigns fly only after fronts; the chambers and the barometer test it); that recirculation left
  cell 4's gas unchanged (false because the same leachate flooded the lower wells; the per-well liquid levels and the
  pumped wells test it); that the cover oxidizes cell 5's 2027 gas at the study's daily-cover share (false because
  oxidation saturates; the plot data test it)
Forcing: the line is the Council's 5,100 t limit; on the cut pack the golden files D (C 5,549 t, 8.8 per cent over; D
  4,495 t, 11.9 per cent under) and all thirteen golden-family variants file D (the pressure lag fixed at 12 or 20
  hours, cell 4's chamber alone, all three chambers pooled, the campaigns weighted with the drone flights, oxidation as
  a logistic in the log of the flux or with its own half-saturation flux, cell 5 on cell 4's methane potential, the
  faster decay ramped over three or six months, package C's gain as the pilot's mean flow ratio, the level from the
  closed cells' collected gas, cell 4's efficiency held flat); each fitted input moved by its defensible
  spread (the campaigns' pressure factor by 0.03, the recirculated decay by 8 per cent, the dry decay by 10 per cent,
  the covers' oxidation capacity by 15 per cent, package C's pump gain by 20 per cent, cell 5's spring calibration by
  7 per cent) keeps D, the nearest being cell 5's calibration 7 per cent lower (C 5,337 t, 4.6 per cent over) and the
  pressure factor 0.03 lower (D 4,688 t, 8.1 per cent under); the twelve shortcuts file A, B, C or no package (the
  rule's default potential uncalibrated puts every package over the limit; the closed cells' level with the study's
  shares puts C at 4,977 t, 2.4 per cent under), none D (effort.json forcing)
Noun swap: the nearest task on file by skeleton.py check is task1 v5 (severity none); its nouns swapped in (audiobook
  plans become gas packages, a price rise's response becomes the methane forecast) carry across only the common decision
  form (one of a few options) and two common detections (a natural experiment in the record, a second source at
  another grain); its lessons, mechanisms, moves and answer pattern differ; against the client corpus the nearest is
  severity none
Closed strategies: the call turns on cancellation_of_offsetting_effects (one treatment moving two terms of a record in
  opposite directions); the nearest closed card is the co-occurring change tangled with the treatment, and the
  mechanism differs (no second change and no contrast: one cause sped the source and blocked the collector, and the
  fix reads the source on the part of the instrument the blocking did not reach and carries it to a unit with no
  instrument); the second stump, common_error_benchmark with a pressure response, is near the fieldwork-timing card by
  family only (no seasons and no groups compared; a physical response carried hour by hour, mass-conserving); the third,
  scaling_diminishing_returns, is on no card; the cell-by-cell forecast is the structure of the packages, not a pooled
  rate carried to a new mix, and no closed lesson is a step whose omission alone moves the call

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | methane emissions (the limit's quantity) | methane leaving the site to the atmosphere from every surface, the flare and the engines; surface emissions only | every source | the resolution's definition; same call: the flare and engines' unburned methane is 102 t of package D's 4,495 |
| SF2 | a year of normal weather | each month's soil temperature at its 2016 to 2025 mean with the pressure response averaging to one over the year; 2025's weather | normals | the resolution; same call: 2025's soil temperatures give C 5,520 t and D 4,472 t |
| SF3 | the cheapest package | the lowest capital cost in the options paper; the lowest cost per ton | the paper's cost | the resolution's least-cost rule and the paper's costs |
| SF4 | at or under the limit | expected emission not above the limit; with a margin | not above | the resolution's wording |
| SF5 | a package's works | cumulative (each package includes the one before); separate | cumulative | the options paper |
| SF6 | in-service dates | the paper's dates; slipped dates | the paper's dates | the options paper |
| SF7 | design capture | the share of all methane generated in cell 5 the collectors take from their date; a share of the area served | the share of cell 5's methane | the options paper's design-basis sentence |
| SF8 | the 2025 report's figure | as filed in March 2026; recomputed | as filed (it reproduces) | the report |
| SF9 | the survey's 2025 figure | the 2025 campaigns' mean rate times 8,760 hours as the survey states it; with the 2026 campaigns | 2025 campaigns only | the survey's own summary |
| SF10 | the bridge's order | collection efficiency first, then oxidation (the report's equation); oxidation first | collection then oxidation | the prompt ("the report's in the order of its own equation") and the report's equation |
| SF11 | municipal waste in cell 5 | the MSW material code with its old codes (MSW-COM, MSW-RES, MSW-TS); every material | MSW | the prompt's "municipal waste" and the tickets' material codes |
| SF12 | cell 4's methane generation | methane made in cell 4's waste; collected gas | made in the waste | the prompt's "generation" against the report's "collected" |
| SF13 | the 12 months to October 2026 | November 2025 to October 2026; January to October 2026 | November to October | the prompt |
| SF14 | the share the cover oxidizes | oxidized over the methane reaching the cover (the uncollected gas); over all gas made | reaching the cover | the prompt's wording |
| SF15 | if nothing changes in 2027 | package A (no new works in 2027); A with the 2029 works | A | the options paper |
| SF16 | methane in metric tons | metric tons of methane; short tons; CO2 equivalent | metric tons of methane | the prompt, the resolution and the report |
| SF17 | the weather of R5's year | normal weather as for the call; 2025's | normals | same band: 2025's soil temperatures give 17.5 per cent against 17.1 |
| SF18 | the waste in short tons | the tickets' net tons (short tons); metric tonnes | short tons | the prompt's "short tons" and the tickets' net_tons column |
| SF19 | cell 5's cover area in 2027 | its 24.2-acre footprint (the Cells sheet); the 2025 report's 14.6 acres filled | the footprint | the options paper ("across its whole footprint since July 13, 2026") and the lifts in the daily log and the fill plan; the 14.6 acres would give 12.8 per cent and the same call |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: every source on the Fernhallow site (five cells, the flare, the engines) |
| 2 | Unit of account: metric tons of methane over a calendar year (2025, 2027); cell 5's waste in short tons as weighed |
| 3 | Attribution window: calendar 2025 for the reconciliation; calendar 2027 for the forecast; November 2025 to October 2026 for R3 |
| 4 | As-of dating: the extracts pulled November 2 to 4, 2026; data to October 31, 2026 |
| 5 | Version basis: the report as filed in March 2026; the survey's final report of September 2026 |
| 6 | Denominator: R5 over the methane reaching cell 5's cover (SF14); R3 over 2022's generation |
| 7 | Weighting: none; each campaign corrected and averaged as the golden states |
| 8 | Window length: one calendar year for the emissions; the station's 2016 to 2025 record for the normals |
| 9 | Boundary inclusivity: a package's work counts from its in-service date's month |
| 10 | Rounding path: hourly and monthly values summed at full precision; tons shown whole |
| 11 | Tie-break: none needed; C sits 8.8 per cent over the limit and D 11.9 per cent under |
| 12 | Maturity and censoring: the 2027 forecast is a model; no record is censored |
| 13 | Order of operations: assemble waste, correct the campaigns, read the decay, calibrate cell 5, evaluate oxidation, forecast by package |
| 14 | Row order: no step depends on file order |
| 15 | Duplicate resolution: a voided ticket gives way to its reissue under the same ticket number |
| 16 | Identity normalisation: one id per well; the register maps each to its cell (a blank cell by the id's cell digit) |
| 17 | Netting against gross: emissions are gross of nothing; collected gas is destroyed at the flare and engines |
| 18 | Dimensional units: plant flows in standard cubic feet a minute (the column names); methane at 0.0192 kg per standard cubic foot (the report) |
| 19 | Code and status semantics: ticket material codes by the scale software's code list; well type and pumps by the register |
| 20 | Integerisation: none; tons are continuous |
| 21 | Clause scope: the limit applies to calendar 2027 only |
| 22 | Forward window contents: the 2027 fill plan, the options paper's works and dates, cell 5's recirculation since July 13, 2026 |

## Literal reader

Executing the shipped sentences word for word: the resolution's limit is the methane leaving the site in calendar 2027
in a year of normal weather; the options paper's packages are cumulative with their dates and design capture; the
cheapest package whose expected 2027 emission is not above the limit is the call. A reader who takes the campaigns'
mean as the year, reads cell 4's collected gas as its generation and applies the study's daily-cover oxidation to cell
5 files package A; none of those is another reading of a filed term, each is an easier method on the same filed
estimand.

## Prompt contract

A voice rewrite keeps: the question (what is the cheapest 2027 gas collection package that keeps 2027 at or under the
Council's limit in a normal-weather year); why it must be estimated (nothing measures what the site emits in a year,
and the report's 2,149 metric tons and the survey's 3,537 for 2025 disagree); the site's actual 2025 emissions in metric
tons and how much of each figure's gap from that comes from what, the report's in the order of its own equation; cell
5's municipal waste through October 2026 in short tons; the per cent change in cell 4's methane generation from 2022 to
the 12 months to October 2026; cell 5's 2027 methane generation in metric tons; the share of the methane reaching cell
5's cover in 2027 that the cover oxidizes if nothing changes; 2027 emissions in metric tons under every package; a
workbook and a short deck. It never adds a rounding instruction, a method (no barometric pressure, weather, campaign
days, recirculation, leachate, liquids, flooded wells, pumps as a cause, decay rate, saturation or flux), a warning, an
attached file's name, a role, or a count the data hold.

## Pre-ship check

- Bar re-read on the built pack: eight results across seven areas (assembly and reconciliation, missingness and
  measurement, investigation loops, forecasting, modeling, decomposition and attribution, synthesis), each pinned by a
  filed sentence (Resolution 2025-41's definition, limit and least-cost rule; the options paper's works, dates, design
  capture and cell 5's recirculation date; the report's equation) or the prompt (the units, the windows, the bridge's
  order) and the data, with the bands the answer blocks state; precut 0 FAIL; checks.py 113 of 113; verify.py 27 of 27
  on its own path; two rebuilds byte-identical; figures_check 123 of 123.
- Hidden factor record against the cut data: every chamber breathes with the barometer (cell 3's geomembrane cap
  too); the fair-weather rule lowers the 2026 campaigns (0.792) and the drone flights (0.736) as well as the 2025
  campaigns (0.711); 26 of cell 4's 58 wells flooded, 8 pumped; recirculation in both open cells; the share oxidized
  falls with the flux on all three covers of the study (checks.py R5).
- Effort test against effort.py: quick 13.9, careful 20.8 (1 of 8), thorough 100; the largest hint rescues 1 of 8;
  twelve shortcuts land on four distinct wrong answers (A, B, C and no package); level 5 from the factorial.
- Forcing: the golden C 5,549 t and D 4,495 t against 5,100; thirteen golden-family variants and twelve perturbations
  file D, the nearest C 5,337 t (cell 5's calibration 7 per cent lower) and D 4,688 t (the pressure factor 0.03 lower);
  the pressure's 12- and 24-hour changes ruled out by the chambers' fit and still on D; against the simulation the
  golden's 2025 figure is 4,924 t to its 4,903 and its 2027 package C 5,549 t to its 5,233 (both over the limit).
- Leak sweep REVIEW lines, ruled: the options paper carries the call's words because it defines the packages and the
  limit, and ranks none ("The Division will bring one of them to the Council"); the stump-vocabulary lines on the four
  PDFs are the field's own words (campaigns, oxidation, emission, collected, record), and no sentence relates pressure
  to emission, liquids to decay or flux to the oxidized share; the column names carry their units the way the
  producing systems export them (soil_temp_c, temp_f, flare_temp_f) and the surface emission file's flag column is its
  instrument's own; the options paper's column words (cell, cover, date, installed) are ordinary words of its genre;
  the prompt's deliverable quota is the Council's medium.
- Stage 4 leak reader (isolated, on the cut pack): no instruction, no ranking or helper file, no answer figure and no
  single item that makes the task routine; every filed sentence it quoted executes to the golden's convention; its
  package C point is the package's scope (harmless) and its realism notes were fixed in the generator (drone times,
  blower outages); leak_check_report.md carries the read and the rulings.
- Stage 4 determinism judge: pass 1 DETERMINISTIC on the call with two figures not pinned (its pressure fit pooled
  cell 3's chamber, then simulated at a third of the soil covers' response, with a half-life lag: 0.059 per hPa and
  2025 at 4,250 to 4,300 t; the oxidation form unstated) and the ticket step misworded, all fixed in the generator and
  the blocks; pass 2 DETERMINISTIC on the rebuilt cut (0.0997 per hPa, the campaigns' factor 0.711 and 2025 at 4,922 t
  reproduced by the stated specification; lags 8 to 24 hours and a standard-time campaign clock all inside the band;
  Q10 1.891 reproduced), with one solution-side finding, cell 5's cover area, closed in Step 6 and checks.py SF19.
- Gate WARNs answered: precut's R3 upstream of four results (R4, R5, R7 and R8 each need work of their own: the
  largest hint rescues R3 alone), its two routine factors (the shift to cell 5 and the scale-house materials, a reflex
  step and R1's assembly, neither the call) and nearest chains (Template check); the voice gate's deliverable quota
  (the Council's medium); the leak sweep's REVIEW lines (ruled above); heart's house lesson: task7 v12, drawn after
  this build (its DRAWN commit follows task23's), took cancellation_of_offsetting_effects as well, so the count rose
  after the draw; this build keeps its precedence by draw order.
- Containers: audit_containers exit 0 on the pack, the golden and both zips.

## Tried and rejected

- 2026-11-13, draw: a vapor intrusion world (which homes over a TCE plume get mitigation before winter): its strongest
  step, homes sampled in different seasons carried to the winter, is the client's closed fieldwork-timing card, and
  its second, the sewer pathway, is a house lesson on two live builds (position on a network).
- 2026-11-13, draw: an oil and gas basin's top-down against bottom-up methane: the aerial survey's wind-dependent
  detection limit is the closed censoring card, and towers, flights and plume imagery could not be simulated credibly
  enough to pin the bands.
- 2026-11-13, draw: an ozone attainment plan with a VOC-limited core: no task type in this subdomain serves the
  forecast it needs, and the photochemistry could not be simulated to an air-quality modeller's eye.
- 2026-11-13, draw: activated carbon breakthrough for PFAS with chromatographic overshoot: no task type in this
  subdomain serves it, and multicomponent adsorption could not be pinned to bands.
- 2026-11-13, draw: groundwater forensics with isotopes and capture zones: transport forecasts too sensitive to pin.
- 2026-11-13, draw: estuary salinity at a drinking water intake: a second tidal forecasting task in this subdomain
  after task3's tide valves.
- 2026-11-13, draw: the deliverables as a workbook and a Word memo (docx and xlsx repeats task9) or a PDF staff report
  (pdf and xlsx repeats task20); drawn as a workbook and the council briefing deck.
- 2026-11-13, draw: gap objective with G2 first (test.same_puzzle against task7 v11, test.same_driver against task8
  v16): the deciding step is the forward window's cell 5 carried from a record that is not the operation, so the gap
  is time and the decisive generator G3 (record versus operation).
- 2026-11-13, design: the 2026 reconciliation (the report and survey for 2026): 2026 has no filed report and its data
  stop in October; the bridge moved to calendar 2025, complete in every record.
- 2026-11-13, design: an uncertainty result (a 90 per cent range on the chosen package): its endpoints have no
  determinate band across the defensible error models; replaced by cell 5's 2027 generation (R4).
- 2026-11-13, design (prototype 4): cell 5 calibrated on its own spring 2026 campaigns lets the hurried oxidation share
  cancel backward and forward, leaving the oxidation stump worth 5 per cent; kept by giving cell 5's cover more capacity
  at low flux (its spring 2026 share near 40 per cent against under 10 in 2027), so the error survives the anchored
  route.
- 2026-11-13, design (prototype 6): the forecast carried cell 4 on its true collection efficiency, which understated
  the pressure stump; the analysis now takes cell 4's 2027 uncollected gas from its measured 2026 balance and adds the
  pilot's absolute pump gain.
- 2026-11-13, build: the site's methane potential at 96 cubic metres a tonne beside the reporting default of 100: a
  forecast from the default potential with no calibration, given the recirculated decay alone, landed package D (one
  stump sufficient on that route, with C at 6,218 t against the old 5,950 t limit); the potential moved to 84 (modern
  municipal waste) and the limit re-set to 5,100 t, so every uncalibrated route files no package or package A.
- 2026-11-13, build: the station's soil temperature had no year-to-year variation (each month within 0.04 C of its
  normal), a generator setting in sight; warm and cold spells and warm or cool years added on a separate random stream.
- 2026-11-13, build: R2's band at 8 per cent: the pressure's 12- and 24-hour changes (a worse fit to the chambers,
  unexplained variance 694 and 674 against 509) sat 7.8 and 6.6 per cent low, at the band's edge; the band widened to
  10 per cent, the survey's gap to 490 t with it.
- 2026-11-13, build: the card's decisive pattern relabelled G7 (blocked, task9 v3) and G13 (blocked, test.same_puzzle
  against task8 v17); G3 kept, the context artifact relabelled to the greenhouse gas report (close_out_summary); the
  surface guard's pair with task22 adjudicated as a shared label only.
- 2026-11-13, build: the prompt's "put it in a workbook and" construction, shared with task21 (surface guard); reworded.
- 2026-11-13, stage 4 (leak reader's realism notes): the report's monthly collected methane ran as a smooth curve and
  the drone flights all took off at 11:00 to 11:25; a monthly wellfield drift (2.4 per cent, then 1.1 per cent) moved
  the closed cells' decay estimate 5 to 7 per cent and the simulation's own package C to within 1 per cent of the
  limit, so the drift was dropped and the blower outages kept (each a zero-flow spell in the plant record and a dip in
  the month's collected methane); the flights now take off between 10:05 and 12:50.
- 2026-11-13, stage 4 (determinism judge): the chambers pooled across all three (cell 3's geomembrane chamber simulated
  at a third of the soil covers' response) with a half-life lag gave 0.059 per hPa and a 2025 figure 13 to 14 per cent
  low; cell 3's response set near the soil covers' (0.09 against 0.10), so pooling no longer moves R2, and the exact
  specification stated in the Step-by-Step; the oxidation's form and cell 5's area stated; the ticket step's wording
  corrected (voids dropped, reissues kept).
- 2026-11-13, stage 4: cell 4's 2027 collection held at its autumn 2026 efficiency over-forecast cell 4 against the
  simulation (the reached waste's share of its gas falls in 2027); the golden forecasts it by zone, the flat efficiency
  kept as a rival (same call); the faster decay now starts the month after the log's first injection, as the
  Step-by-Step states; the cover areas are read from the Cells sheet.
