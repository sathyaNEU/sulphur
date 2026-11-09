# task13 design note: Kotuku Networks' 2027 vegetation catch-up

## Draw

**Card.** `.claude/skills/fingerprint/cards/task13.json`, architecture v1, registered 2026-11-09, guard verdict WARN
(no BLOCK). Domain Energy Systems & Utilities (`energy-systems-utilities`), task type grid reliability and outage
analysis (`grid-reliability-outage-analysis`), the one energy task type never drawn; objective Anomaly Detection &
Diagnostics, which that task type serves. Shape 01: a ranked list of feeders under a cap.

**The decision.** Kotuku Networks, a consumer-trust-owned lines company in the lower North Island, runs 48 11 kV
feeders off ten zone substations across a northern coast, river plains and southern hill country with plantation
forest, watched by four automatic weather stations. Its 2027 vegetation catch-up trims six feeders' line corridors
back to the clearance a cycle trim leaves, finished by 31 March 2027, and goes into the asset management plan it
discloses before 1 April 2027. The programme terms file what it is judged on: the sustained vegetation customer
interruptions it avoids in the 2027-28 regulatory year (1 April 2027 to 31 March 2028) on days that are not major
event days, against each feeder's corridor left as it stands, with no cycle trim anywhere until April 2028.

**Data-native sentence.** A tree contact on an overhead line happens when wind moves a branch onto a conductor, so a
feeder's vegetation interruptions are its corridor's density, multiplied by the growth since its last cycle trim and
by the gusts its weather station saw; three years with a third of the usual damaging gusts on the northern coast and
more than twice them in the southern hills move every feeder's count by its district's wind before its corridor
shows at all, and a corridor that is dense straight after a trim keeps most of its count after any trim.

**The two analytical judgments that decide the call** (each alone leaves the wrong six):
1. *Exposure: the recent counts carry the recent wind.* From November 2023 the storm track sat south: Paua Bay
   recorded 38 hours a year of gusts of 60 km/h or more against its 2007-2023 normal of 106, Titi Saddle 312 against
   133, while the mean wind at every station moved under 6 per cent. Each feeder's vegetation interruptions have to be
   read per unit of its own station's gust exposure, and 2027-28 projected at the station record's long-run exposure.
2. *Decomposition: a catch-up removes only the growth since the last trim.* A feeder's rate per unit of exposure is
   its corridor's rate straight after a cycle trim times the growth since that trim (15.5 per cent a year across the
   network). The plantation feeders, on a three-year cycle and cut in the second half of 2025, carry the highest
   expected interruptions and little growth to remove; the six northern coastal feeders cut between October 2019 and
   May 2020 carry ordinary-looking counts and the most growth.

**Strategy label.** WORKS IN FORM (`stumping/references/sulfur-strategies.md`, Part A): separating two explanations
for one pattern (weather against corridor condition) with a comparison that is actually clean (per unit of the
exposure that drives the events), and selection on a noisy outcome in the live form where the decision's own effect,
the part of the rate the remedy changes, ranks the units rather than their observed level.

**Guard WARN answered.** `repeat.gate_g` (decomposition_attribution, also task2's): the Gate G mechanism here is the
assignment of a correctly recorded rise to its drivers (wind against corridor growth against corridor density);
task2's is a release's error rate against a clinician mix, a different world, shell and shape.

**People** (drawn with `guard.py names --geo "New Zealand" --seed 1301`): Tania Foley, general manager network;
Wayne Ward, vegetation manager (owner of the cycle log); Hoani Marshall, reliability engineer (the golden's author);
Kathryn Carter, regulatory manager (owner of the reliability reporting standard); Sean Chapman, the vegetation
contractor's supervisor; Maria Hodson, customer service lead (no document).

**Sources** (all constructed by `generator/`; provenance in `metadata.json`): the outage management system's
interruption export, April 2022 to October 2026 (10,917 rows); the weather service's hourly records for four
stations, 2006 to October 2026 (182,616 rows each) and its station register; the feeder register (with the zone
substations' coordinates); the protection device register; the ICP registry's month-end counts; the vegetation cycle
log from 2014; the reliability reporting standard; the 2027 catch-up's programme terms (the WHAT); and, unlabelled,
the tree notices register and the contractor's 2027 schedule of rates.

## Default path

The competent reliability engineer's route, every field read and every filed rule applied:

1. Clean the outage export by the reliability reporting standard: drop the 479 call-centre records of operations
   SCADA or the field crew logged, keep unplanned interruptions of 1 minute or longer, take vegetation as VEG and
   TREE across the October 2023 recode, map Rangiora Street's former feeder codes.
2. Mark the major event days by the standard's SAIDI and SAIFI boundary values (daily indices over the regulatory
   year's mean month-end ICPs) and leave them out: five days, all snow on the southern hills.
3. Rank the feeders on vegetation customer interruptions over the three years to October 2026, the field's
   worst-performing-feeder list, with the cycle log's dates beside them, and fund the six at the top.

Ends on: TOT-02, TIT-04, MKR-01, KWH-01, TIT-01 and TIT-03 (31,591 to 9,009 customer interruptions in three years),
the five plantation feeders and one southern late-cycle feeder; on the golden's own projection those six avoid
5,770 customer interruptions in 2027-28.

Golden: PBY-10, HRK-03, HRK-05, WTK-02, PBY-11 and PBY-03, the six northern coastal feeders left longest since a
cycle trim, avoiding 12,984 customer interruptions (0.33 of network SAIFI on 39,943 ICPs).

## Stump sentence

A competent analyst who removes the major event days and ranks the feeders on vegetation customer interruptions since
November 2023 funds TOT-02, TIT-04, MKR-01, KWH-01, TIT-01 and TIT-03, the plantation feeders and a southern
late-cycle feeder, and their catch-up avoids 5,770 customer interruptions; normalising for wind still funds the
plantation feeders, whose expected interruptions are a dense corridor a catch-up leaves in place, and splitting the
rate into corridor and growth without the wind funds the southern late-cycle feeders, whose growth the stormy years
inflated; the saving is on PBY-10, HRK-03, HRK-05, WTK-02, PBY-11 and PBY-03, 12,984.

## Deep reasoning

Task type: grid-reliability-outage-analysis (Energy Systems & Utilities), serving Anomaly Detection & Diagnostics: the
anomaly is the recent vegetation record itself, a southern rise and a northern fall that are the weather and not the
corridors, diagnosed before the programme is targeted.
Domain test: the deciding quantity is the sustained vegetation customer interruptions a corridor trim avoids on each
11 kV feeder in 2027-28, which the field reads from the outage record as vegetation SAIFI by feeder outside major event
days, and models from tree-contact rates against storm exposure and the vegetation management cycle.
Swap: "fund the six feeders where a vegetation catch-up avoids the most customer interruptions" rewritten as "fund the
six schools where a repaint avoids the most absences": gust exposure at a weather station, trim cycles, corridor
regrowth, protective devices and major event days stop making sense.
Layer 1: the outage system's call-centre records beside SCADA and field-crew records of one operation, planned work
and momentary interruptions in the same export, the October 2023 cause recode, local times with no offset, Rangiora
Street's feeders renamed at its 2023 rebuild, Titi Saddle's gusts in knots before July 2013, logger gaps and suspect
spikes in the station records, cycle jobs closed weeks after the crew finished; every careful run cleans them alike.
Layer 2: estimand_identification, own pattern: the feeders that look worst were selected on a stormy district and on a
corridor density the remedy cannot touch; the choice that flips the call is reading the record per unit of station
gust exposure and splitting the rate into the corridor's own rate and the growth since its trim.
Decisive step: each feeder's monthly vegetation interruptions fitted as Poisson counts on its nearest station's gust
load, as a corridor rate times a network growth per year since the last cycle trim, and 2027-28 projected at the
station record's 2006-2025 gust load with the growth left running and with it restarted on 31 March 2027.
Not semantics: every field, code, unit and definition read correctly leaves the recent counts true counts: the
plantation feeders really had the most vegetation interruptions, and nothing in any file marks a year as unusual or a
corridor as dense; the weather and the corridor's own rate exist only in the station records and the fit.
Not rule application: no filed rule normalises for wind or splits the rate; the standard defines the counting and the
terms the comparison. Enumerated family (18 routes on the cut pack): 0 to 3 of the six; standing family (26
constructions the data leave defensible: gust measures 45 to 70 km/h and gust excess 35 to 45, base years, lags and
bins, the cleaning choices, the clocks, the stations): 6 of 6 every time. The ruling-out is loud: the station
record's damaging-gust hours run 0.36 and 2.35 of normal, and the cycle log's trims show each feeder's rate stepping
down at its trim.
Analyst test: the strong analyst removes the major event days and ranks on three-year vegetation customer
interruptions with years since trim beside them, and files TOT-02, TIT-04, MKR-01, KWH-01, TIT-01 and TIT-03, which
avoid 5,770 against the golden six's 12,984.
Estimand: the programme terms (vegetation_catchup_2027_programme_terms.docx, sections 2(d) and 3): sustained,
unplanned vegetation customer interruptions in 1 April 2027 to 31 March 2028 on days that are not major event days,
expected with the corridor left as it stands against the corridor as the catch-up leaves it, no cycle trim before
April 2028; SAIFI on the ICPs at the latest month-end (section 5).
No decoy: nothing is planted to be caught; the plantation feeders' counts are the true record of a stormy south and a
dense corridor, and no memo, draft or stakeholder figure argues for them.
No certified replay: no published figure is reproduced to recover the method; the pack carries no prior ranking,
benefit estimate or reliability forecast.
Chain: (1) the recent record's north-south swing is the wind, seen in damaging-gust hours and not in mean wind, so
counts are read per unit of each station's gust exposure; (2) on that scale each feeder's rate is its corridor's rate
after a trim times a growth since the trim, fitted across feeders and months; (3) 2027-28 is projected at the station
record's long-run exposure, not the recent years' or the outage record's own; (4) the saving is the growth the
catch-up removes, in customer interruptions at each feeder's own customers per interruption; (5) the six largest.
Judgment: two modelling judgments justified from the data: the exposure measure (the gust load fits the record best,
hour counts from 50 km/h leave months with vegetation interruptions and no exposure) and the split of the rate into
corridor and growth (the rate steps down at every trim in the window and climbs with years since, 15.5 per cent a
year); the asks add the design-matched range across the station record's weather years.
Hidden by: two effects offsetting inside the observed window: the northern feeders' growing corridors were held down
by three calm years and the southern feeders were lifted by three stormy ones, while the annual mean gust moved under
6 per cent at every station, so a plot of mean wind or the field's major-event-day treatment (the major event days
were snow days) shows nothing; the plantation feeders lead on every recent count and on wind-normalised expected
interruptions.
After the notice: (1) once the southern storms are seen, the exposure must be the damaging gusts and the projection
the long-run record: a run that projects at the recent years (persistence) or the outage record's own weather funds
the southern feeders again (R8, R9); (2) the normalised rate must be split into corridor and growth: a run that counts
every expected interruption as removable funds the plantation feeders (R3, R3b), and a run that reads growth only from
years since trim funds the most overdue small feeders (R2, R2b); (3) customers per interruption from each feeder's own
record, and the range from the weather years, not the fit's standard errors.
One-fact test: the likeliest hint, "normalise the tree interruptions for wind", leaves the run funding the plantation
feeders on wind-normalised expected interruptions (1 of 6); "the catch-up removes only the growth since the last
trim", without the wind, leaves it funding the southern late-cycle feeders (0 to 1 of 6); no single sentence carries
both, and either hint still leaves the projection weather to choose.
No replay: the call re-derives no published figure and no stated number is wrong; the standard's boundary values and
the registers are correct as filed.
Pinned: every rival a careful analyst would run was run on the cut pack (`generator/rivals.py`): gust measures from 45
to 70 km/h, gust excess over 35 and 45, straight or squared, base years 2006-2024, 2006-2026, 2011-2025 and 2016-2025,
lags of half a year and a year, whole-year bins, a negative binomial fit, two stations blended, the job-closed trim
date, UTC months, a December or February catch-up finish, customers per interruption since November 2023 or at
October 2026 ICPs, and every cleaning choice all land the golden six; the routes that skip a step miss it (ladder).
Run forecast: one run takes the field's worst-feeder ranking (method shortcut at rung 0) or checks the mean wind,
sees nothing and keeps it (dismissed own evidence); the other normalises for wind and stops at expected interruptions
or decomposes on counts alone (unfinished chain at rung 2 or 3), filing the plantation or the southern feeders.
Strategy label: WORKS IN FORM, separating weather from corridor condition on a clean per-exposure comparison, with the
remedy's own effect (the growth the trim removes) as the ranking quantity rather than the observed level.
Lesson: a remedy's saving is the part of the rate the remedy changes, read per unit of the exposure that drives the
events and projected at the exposure the decision year will see; no build on file teaches the three together in grid
reliability, and the skill transfers to any maintenance cycle run against weather.

## Survivor anatomy

Actor: the feeder's corridor is the actor, and the deciding property, the growth since its last trim per unit of gust
exposure, has no column anywhere: the outage export prints interruptions, the cycle log prints job dates, the station
records print hourly gusts, and the property exists only as their join through a fit.
Link: the signal is read through a link no key offers: each feeder to its nearest station by the zone substation's
coordinates in the feeder register and the station register, each month's gust load from the hourly record on the
local clock, and each month's years since trim from the cycle log; no file carries a station column or a trim age.
Reflex: the field's worst-performing-feeder list on vegetation customer interruptions outside major event days sits at
rung 0 and files the plantation feeders; the field's weather treatment, the major event day, removes the five snow
days and none of the storms.
Back-test: the easy route validates on its own terms: the plantation feeders lead the vegetation count in each of the
three years and in the whole record, and the southern rise lines up with the record's worst storms, so a run checking
its ranking against the history finds it confirmed.
Second use: every file the decisive step reads ships for its own reason: the outage export for any reliability
figure, the standard for the counting and the major event days, the feeder register and the station records for
storm reporting and network planning, the cycle log for the vegetation programme itself; delete the decisive step and
the pack is unchanged.
Shock: the movement the step recovers reads as ordinary: the northern feeders' vegetation interruptions fell (it looks
like an improvement), the southern rose (it looks like deterioration on plantation lines); sorted on any shipped
statistic (recent count, years since trim, cycle overdue, customers), the golden six are not an interval of the sort.
Pins: the WHAT is filed once in the programme terms (the regulatory year, vegetation interruptions counted as the
standard counts them, the corridor left as it stands against the catch-up, no cycle trim before April 2028, SAIFI on
the latest month-end ICPs), in the network's own programme genre, and no sentence anywhere names wind, gusts,
stations, growth, exposure or a method.

## Readability screen

| Rung | 1 Filed sentence | 2 Schema | 3 Reflex | 4 Control bench | 5 Hygiene | 6 Linear | 7 Dedicated organ | 8 Framing | Verdict |
|---|---|---|---|---|---|---|---|---|---|
| R0 worst-feeder ranking on recent vegetation customer interruptions | the terms ask for customer interruptions avoided | interruptions and causes are rows | the field's method | none | yes | a sum | no | the terms frame no axis | readable |
| R2 most years since trim, or most overdue on the cycle | none | the cycle log's dates | a maintenance reflex | none | no | one subtraction | no | none | readable |
| R3 wind-normalised expected interruptions, all removable | none | station records are files | a normalisation reflex once the wind is seen | none | no | a ratio | no | none | readable |
| R6 corridor and growth fitted on counts alone | the terms compare corridor states | trim dates are in the log | a regrowth reflex | none | no | a fit | no | none | readable |
| R7 (decisive) corridor and growth fitted per unit of each station's gust load, projected at the long-run record | no sentence names wind, gusts, stations, exposure or growth | no station column, no trim age, no exposure field; the link is coordinates | not the field's method, which ranks recent counts outside major event days | none | no | no | every file read has its own use | the terms state no difference on the weather or corridor axis | silent |

## Semantic fork table

| Id | Term or convention | Golden reading | Alternative | Call under it | Ruled out by |
|---|---|---|---|---|---|
| SF1 | vegetation interruptions | cause VEG to 30 September 2023, TREE after | adverse weather counted as vegetation | same call (asserted) | standard section 4; same call asserted |
| SF2 | sustained | 1 minute or longer | momentary interruptions counted | same call (asserted) | standard 2(b) |
| SF3 | one interruption per operation | the 479 call-centre records of operations SCADA or the field crew logged dropped | kept | same call (asserted) | standard 3(b) |
| SF4 | major event days | daily unplanned SAIDI or SAIFI above the path's boundary value: the five snow days | none excluded; SAIDI alone | same call (asserted); no major event day carried a strong-wind hour | standard section 5; terms 3(b) |
| SF5 | the window and the comparison | 1 April 2027 to 31 March 2028; the corridor as it stands against the catch-up; no cycle trim before April 2028 | a cycle trim on overdue feeders in 2027-28 | a different quantity | terms 2(d) and 3(c) |
| SF6 | the catch-up's finish | 31 March 2027 for every span | mid-December 2026, 1 February 2027 | same call (asserted) | terms 2(b); same call asserted |
| SF7 | customers per interruption | each feeder's mean over its vegetation interruptions since April 2022 | since November 2023; scaled to October 2026 ICPs | same call (asserted) | same call asserted |
| SF8 | the exposure measure | the monthly gust load, each hour's gust above 40 km/h squared | hours of gusts of 45 to 70 km/h; gust excess over 35 or 45, straight or squared | same call (asserted); totals 12,247 to 15,757 | the gust load fits the record best (log-likelihood -2,756; the nearest, the straight excess over 45 km/h, -2,777; hours of 45 km/h -3,022), asserted; same call asserted |
| SF9 | the long-run exposure | each calendar month's mean over 2006 to 2025 | 2006-2024, 2006-2026, 2011-2025, 2016-2025 | same call (asserted) | same call asserted |
| SF10 | the growth's form | log-linear in years since trim | a half-year or one-year lag; whole-year bins | same call (asserted) | same call asserted |
| SF11 | the station of a feeder | the station nearest the zone substation | the two nearest blended by inverse distance | same call (asserted) | same call asserted |
| SF12 | the trim date | the crew-finished date | the job-closed date | same call (asserted) | the log's own heading: a job closes once the audit is signed off |
| SF13 | the clock | months in New Zealand local time | the station record's UTC months | same call (asserted) | standard 2(e) |
| SF14 | Rangiora Street's feeders | former RGS codes mapped through the feeder register | history before the rename dropped | same call (asserted) | the register's former-code column |
| SF15 | the SAIFI denominator | ICPs at the latest month-end, 39,943 | the 2025-26 mean | same call (0.33 either way, asserted) | terms section 5 |
| SF16 | the count model | Poisson with a rate per feeder | negative binomial | same call (asserted) | same call asserted |
| SF17 | Titi Saddle's units | knots converted before July 2013 | left unconverted | same call (asserted) | the station register's note and the unit column |
| SF18 | suspect and missing hours | dropped | suspect hours kept | same call (asserted); no gap falls inside the outage record | the station record's quality flag |
| SF19 | the 90 per cent range | the 5th to 95th percentile of the six's saving across the weather of every complete regulatory year of the station record, the 20 from 2006-07 to 2025-26: 6,000 to 19,000 | the 19 years to 2024-25; nearest-rank percentiles; the fit's own standard errors | the 19 years give 10,000 to 19,000 (recorded); nearest rank within one step of each end; the fit's own errors give 11,000 to 16,000 | every complete year is the record's own spread of weather, and 2025-26 is complete; the decision year is one year of weather, so the fit's errors alone understate it (asserted) |

## Ladder

Priced on the cut pack (`generator/rivals.py`, `generator/checks.py`; world seed 1312). The world's own truth (30
synthetic weather years at the world's rates) has the same six.

| Rung | Construction | Six | Of the golden's six | Dies to |
|---|---|---|---|---|
| R0 | vegetation customer interruptions, last twelve months | TIT-04 TOT-02 MKR-01 TIT-01 KWH-01 TIT-02 | 0 | the stormy south and the plantation corridors |
| R1 | the same, three years to October 2026 (default path) | TOT-02 TIT-04 MKR-01 KWH-01 TIT-01 TIT-03 | 0 | the same; their catch-up avoids 5,770 |
| R1b | the same, the whole record | TOT-02 TIT-04 KWH-01 MKR-01 TIT-01 TIT-02 | 0 | the same |
| R2 | most years since the last cycle trim | PBY-02 RNG-01 PBY-09 PBY-01 RNG-03 PBY-08 | 0 | the open plains feeders on an eight-year cycle have few trees |
| R2b | most overdue against the feeder's cycle | PBY-08 PBY-10 PBY-11 HRK-06 WTK-02 PBY-06 | 3 | small overdue feeders with few trees |
| R5 | three-year customer interruptions times years since trim | TIT-03 MKR-09 TOT-02 TIT-02 TIT-04 MKR-06 | 0 | the recent counts carry the southern storms |
| R5b | the same times cycles overdue | MKR-09 TIT-03 MKR-06 PBY-10 MKR-07 MKR-05 | 1 | the same |
| R3 | wind-normalised three-year rate at the long-run exposure, all removable | TOT-02 TIT-04 KWH-01 MKR-01 TIT-01 PBY-10 | 1 | the plantation corridor's own rate stays after a trim |
| R3b | the golden fit, every expected interruption removable | TOT-02 TIT-04 PBY-10 KWH-01 TIT-01 MKR-01 | 1 | the same: TOT-02 keeps 4,951 of 6,220 |
| R6 | corridor and growth fitted on counts, no station record | MKR-09 TOT-02 TIT-03 TIT-02 TIT-04 PBY-10 | 1 | the growth read through three calm and three stormy years |
| R6y | the same with year effects | TOT-02 MKR-09 TIT-03 TIT-02 TIT-04 PBY-10 | 1 | year effects are network-wide; the swing is by district |
| R6m | the same with calendar-month effects | TOT-02 MKR-09 TIT-03 TIT-02 TIT-04 PBY-10 | 1 | the same |
| R6b | the same, growth by whole years | TOT-02 TIT-04 TIT-01 MKR-01 KWH-01 TIT-02 | 0 | the same |
| R6w | the fit on the mean gust | TOT-02 MKR-09 TIT-03 TIT-02 PBY-10 TIT-04 | 1 | the mean gust moved under 6 per cent |
| R7 | corridor and growth with district-by-year effects, projected at their average | TOT-02 MKR-09 PBY-10 TIT-03 TIT-02 HRK-03 | 2 | the average carries the three stormy years |
| R8 | the golden fit projected at the three years to October 2026 | TOT-02 MKR-09 TIT-03 TIT-02 TIT-04 MKR-07 | 0 | persistence: the 2009-11 swing the other way ran its course |
| R9 | the golden fit projected at the outage record's own exposure | TOT-02 MKR-09 TIT-03 TIT-02 PBY-10 TIT-04 | 1 | the record is 36 of its 55 months in the swing |
| R10 (decisive) | corridor and growth per unit of each station's gust load, 2027-28 at the 2006-2025 record, customers per interruption from each feeder | PBY-10 HRK-03 HRK-05 WTK-02 PBY-11 PBY-03 | 6 | |

Golden family on the cut pack (26 constructions, `rivals.family`): the same six every time; the six's total moves
from 12,247 (gust load over 35 km/h) to 15,757 (hours of 55 km/h or more), the golden 12,984. Margin: the sixth
(PBY-03, 1,821) leads the seventh (TOT-02, 1,268) by 1.44 times. No route that skips a step reaches four of the six;
the nearest is the overdue ranking at three.

## Closure table

| Axis | Reading | Closure |
|---|---|---|
| 1 Population | every 11 kV feeder the network operates, 48 | terms section 4 |
| 2 Unit of account | the feeder, in or out as a whole | terms section 4 |
| 3 Attribution window | 1 April 2027 to 31 March 2028 | terms 3(a); SF5 |
| 4 As-of dating | the corridor as it stands, last trims to October 2026, no cycle trim until April 2028 | terms 2(d); SF5 |
| 5 Version basis | the standard's version 4 and its DPP3 and DPP4 boundary values | standard section 5 |
| 6 Denominator | customer interruptions in count; SAIFI on the latest month-end ICPs | terms section 5; SF15 |
| 7 Weighting | each interruption weighted by the customers the device interrupted | standard 2(d); SF7 |
| 8 Window length | the fit on April 2022 to October 2026; the long-run exposure 2006 to 2025 | SF9 (every base year asserted) |
| 9 Boundary inclusivity | a major event day exceeds the boundary value; sustained is 1 minute or longer | standard 2(b) and 5(a); SF2, SF4 |
| 10 Rounding path | once, at the end; the quarters rounded to add to the year | prompt; checks |
| 11 Tie-break | none needed | the sixth leads the seventh by 1.44 times |
| 12 Maturity and censoring | the corridors keep growing through 2027-28 left as they stand; the catch-up's regrowth from 31 March 2027 | terms 2(b), 3(c); SF6 |
| 13 Order of operations | clean, mark major event days, fit, project, weight by customers, rank | checks (asserted end to end) |
| 14 Row order | the export sorted by start time; nothing depends on order | checks |
| 15 Duplicate resolution | the call-centre record of a logged operation is not a second interruption | standard 3(b); SF3 |
| 16 Identity normalisation | Rangiora Street's former codes; device codes with the feeder prefix | the feeder register; SF14 |
| 17 Netting against gross | planned interruptions out; momentary out | standard 2(b), 2(c); SF2 |
| 18 Dimensional units | gusts in km/h, Titi Saddle's knots converted | SF17 |
| 19 Code and status semantics | the cause codes across the recode; the station quality flags | standard section 4; SF1, SF18 |
| 20 Integerisation | interruptions to one decimal, customer interruptions whole, range to 1,000 | prompt |
| 21 Clause scope | the terms judge only vegetation interruptions, on non-major-event days | terms 3(a), 3(b) |
| 22 Forward window contents | 2027-28 holds no cycle trim and the catch-up finished by 31 March 2027 | terms 2(b), 2(d) |

## Literal reader

A judge executing the terms word for word computes, for each feeder, the vegetation customer interruptions it can be
expected to have in 2027-28 with its corridor left as it stands and with the corridor a cycle trim leaves on 31
March 2027, counted by the standard; "expected" is the forecast for a year of the record's weather, so the literal
reading needs the corridor rate, its growth since trim and the exposure the year will see, which is the golden's
construction. Nothing in the terms names how; the judge who ranks the recent counts has executed a different
quantity (the past three years), which the terms do not ask for.

## Oracles

- The world's truth: each feeder's expected 2027-28 avoided interruptions over 30 synthetic weather years at the
  world's own rates (`world.truth`); its six are the golden six (asserted in `checks.py`).
- The independent verifier (`verify.py`): its own readers, cleaning, major event days, numpy Poisson fit and
  projection reproduce every row, the total, the SAIFI and the growth exactly.
- The family (`rivals.family`): 26 constructions, each returning the golden six.
- The rungs (`rivals.rungs`): 18 routes that skip a step, none reaching four of the six.

## Ask sheet

- **A1 the feeder table** (48 rows ranked by customer interruptions avoided): expected vegetation interruptions in
  2027-28 left as is, customer interruptions left as is and after the catch-up, and the difference. Rides the deep
  step in every cell: the shallow run's left-as-is figures are its recent averages and its after-catch-up figures a
  guess; second judgment on the after-catch-up column: the corridor regrows through 2027-28 from 31 March.
- **A2 the six's total and network SAIFI** (critical): 12,984 and 0.33 on 39,943 ICPs; shallow 5,770 on the wrong six.
- **A3 the split across the regulatory year's quarters**: 2,753, 5,466, 3,102 and 1,663; second judgment: the storms
  are seasonal (the record's winter carries most of the gust load) and both corridors grow through the year, so an
  even split or a year-grain projection misses.
- **A4 the 90 per cent range**: 6,000 to 19,000; second judgment: the decision year is one year of weather, so the
  range is the spread across the station record's complete years (more than twice the width of the fit's own uncertainty, 11,000 to 16,000).
- **A5 the chart** of the avoided interruptions on every feeder.
- **Mess on the paths:** every Layer 1 item is handled alike by careful runs (`checks.py` SF1 to SF4, SF12 to SF18).

| Ask | Weight | Shallow run | R3b all removable | R6 no station record | Cracker (landed run) |
|---|---|---|---|---|---|
| A1a tree interruptions left as is | 9 | miss | keep | miss | keep |
| A1b customer interruptions left as is | 9 | miss | keep | miss | keep |
| A1c customer interruptions after the catch-up | 9 | miss | miss | miss | miss |
| A1d interruptions avoided and the ranking | 9 | miss | miss | miss | miss |
| A2 the six's total and SAIFI | 7 | miss | miss | keep | keep |
| A3 the quarters | 6 | miss | miss | miss | miss |
| A4 the 90 per cent range | 6 | miss | miss | miss | miss |

The cracker takes the deep step on strong-wind hours of 60 km/h (a measure that fits the record less well than the
gust load), works at the year's grain and gives the fit's own uncertainty as its range (70.0). The shallow run is the
default path (7.0). The wind-normalised run that counts everything as removable is off the call (31.0; with the
cracker 50.5); the decomposition on counts alone 20.0 (with the cracker 45.0).

Shallow keep: 0.0
Pair ceiling: 38.5
Measured by: generator/ceiling.py (on the cut pack)

## Prompt contract

A voice rewrite may not drop or change: the question (which six 11 kV feeders the 2027 vegetation catch-up goes to,
to avoid the most sustained customer interruptions in the 2027-28 regulatory year); `vegetation_catchup_2027_feeders.csv`
with a row for every feeder ranked by the interruptions avoided, giving the expected tree-caused sustained
interruptions left as is, the expected tree-caused customer interruptions left as is and after the catch-up, and the
difference; `vegetation_catchup_2027_board_note.docx` naming the six with their total, its network SAIFI, its split
across the year's four quarters, a 90 per cent range and a chart of every feeder's avoided interruptions; the
rounding (interruptions one decimal, customer interruptions whole, the range to 1,000, SAIFI two decimals). The
rewrite keeps one question, names no input file, says nothing about who is asking, and never says how the
interruptions are to be estimated (no wind, weather, stations, growth, exposure, trim age or model).

## Leak sweep rulings

- Sweep 3 (the programme terms carry the call's distinctive words): harmless; the words are the decision's own
  (six 11 kV feeders, catch-up, cycle trim), and the terms name no feeder, district, station or method.
- Sweep 4 (stump-paragraph terms in the standard and the terms: record, counts, weather, outage, interruption,
  programme, leaves): harmless; "weather" is the standard's adverse-weather cause category and "leaves" is the
  clearance a trim leaves; neither document names wind exposure, growth or a method (asserted in `checks.py`).
- Sweep 9 (dates after 2026-11-03 in the tree notices register): harmless; they are the works-due dates of notices
  issued in October 2026, forward-looking by construction, and no notice is closed after 21 October 2026.
- Sweep 11 (deliverable set csv+docx at 23 per cent of recent prompts): a quota WARN; the table and the board note
  are the decision's natural pair, and the question form moved from "which" to "where" to clear its quota.

## Pre-ship check

- The Sulfur standard re-read against the built pack: the deciding step is the exposure-normalised split of each
  corridor's rate into its own rate and the growth since trim, projected at the long-run record (two modelling
  judgments, five dependent inferences); no banned stump decides (no field reading, rule, plant, replay, single fact
  or open reading flips the six; `checks.py` asserts 26 conventions and 18 rungs).
- The pack: 14 files in three categories (CSV exports, workbooks, documents); the outage export (11,396 rows) and the
  four station records (182,616 rows each) are the large messy CSVs; two distractors (the tree notices register and
  the schedule of rates) read by no golden step; provenance and licence in `metadata.json`.
- The golden ZIP holds exactly the two requested files; every figure in the answer blocks is in `figures.json`
  (`figures_check.py` exit 0) and the independent verifier reproduces all 48 rows.

## Stage 4

- Leak reader (isolated, Sonnet, medium): clean. Questions 1 to 4 none; question 5 quotes the programme terms 3(c)
  with 3(b), 2(a) and 2(d), whose literal reading is the golden's quantity; question 6 an analytical choice; the
  three sweep lines it was given ruled harmless (`leak_check_report.md`, `## Solver's-eye read`).
- Determinism judge: DETERMINISTIC, APPROVE (`determinism_check_report.md`); Gate H passes (analytical decisive step,
  six or more inferences, no one-fact rescue). Its findings, fixed in one generator pass: `metadata.json` now names
  the two distractors; the feeder register's ICP column is written from the registry's October 2026 counts, so it
  totals 39,943 like the ICP file (it had read 39,933; SAIFI 0.33 either way). Its Gate G label (forecasting with a
  model-selection layer) differs from the card's decomposition_attribution; both are analytical, non-defect
  classifications that agree on every fact, and the card keeps the label that names the mechanism.
- After the pass, the clone screen promoted task12 against task13 at a surface score of 0.10, all of it from both
  packs being flat folders of the same three formats (every wording, name and schema axis at zero); the weather
  service's four hourly records now ship in their delivery folder `pou_aws_hourly/`, and no pair is promoted. The
  exports' saved times are now written as New Zealand time (they had been read in the build machine's zone).
- After the first READY commit: the 90 per cent range had run over the 19 regulatory years to 2024-25 although the
  station record also completes 2025-26; it now runs over every complete regulatory year, the 20 from 2006-07 to
  2025-26 (6,000 to 19,000; the 19 years give 10,000 to 19,000, recorded in SF19 and asserted). The quarters are
  rounded by largest remainder so they add to the year (2,753, 5,466, 3,102, 1,663), and the independent verifier now
  recomputes the quarters and the range as well. The judge traced the range rather than recomputing it; the six, the
  total, the SAIFI and every feeder row are unchanged.

## Tried and rejected

- A smart-meter outage-alert rollout recording small outages that customer calls missed, as the decisive layer:
  rejected at the draw, 2026-11-09. Which comparison is clean (recorded against experienced) is the estimand, so
  filing it spends the layer and leaving it open is a fork (`determinism-check` section 1).
- A random scratch world (feeder size and tree density drawn freely): the three-year count and the wind-normalised
  rate alone reproduced four to six of the golden six on five seeds, because size dominated; the world is built from
  groups (overdue northern feeders, dense plantation feeders trimmed recently, southern late-cycle feeders, overdue
  feeders with few trees) so each shortcut lands on a different wrong list.
- A one-year wind anomaly carried by the station's mean level: the decomposition fitted without the wind still landed
  four to five of the six, because one year is a small share of the outage record and a higher mean moves every gust
  alike; replaced by three years in which the storm track sat south (fewer strong-wind days in the north, about twice
  as many in the south, mean wind within 6 per cent) over an outage record from April 2022.
- Plantation feeders trimmed early in 2025 on a four-year cycle: their growth left them among the golden six; moved to
  a three-year cycle cut in the second half of 2025, which keeps them first on every recent count and on expected
  interruptions and last on the growth a catch-up removes.
- Major event days set by the 2.5-beta rule on the record: wind-storm days crossed the boundary and carried a fifth of
  the strong-wind hours, so the projection's treatment of those days moved the six's total by half; the filed
  boundary values now sit above every storm day, and the major event days are the five snow days.
- Hours of gusts of 60 km/h or more as the golden's exposure: 30 feeder-months with vegetation interruptions had no
  exposure at all, and the six's total moved 28 per cent across thresholds; the gust load, which fits the record best, is
  the golden, and the hour counts stay in the family (same six).
