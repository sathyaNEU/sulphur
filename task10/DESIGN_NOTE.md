# task10: Wealdmoor Power Networks' winter 2027/28 reinforcement at the Halverton flexibility zones

Architecture 6, a results chain in the same world, re-rooted on 2026-11-10 at the platform reviewer's direction
(`runs/review_2026-11-10.md`): "document the transfer, for example as switching log entries, and make the call turn on
judgments that each move a figure". The world, the demand side and the pack's files are kept; the hidden transfer is
gone (the control room's ordinary switching is logged and filed in guideline 3), and the answer is eleven results:
seven asks, the three findings they stand on and the call.

## Draw

Subdomain: Energy Systems & Utilities
Analysis type: Forecasting & Predictive Modeling
Answer shape: a forecast with bands, plus its drivers (each zone primary's design-day peak for winter 2027/28 with its
  contract called in full, expected and at the nine-days-in-ten level, with what drives it: demand before flexibility,
  the megawatts delivered, the megawatts off the peak, the bridge from the megawatts contracted)
Weight: validation. Fitting any of three readings of the record takes an hour; the work is proving which one carries
  to a call of the whole of a contract far larger than any on record: megawatts scheduled varied at equal temperature
  and megawatts delivered did not, each provider's two zones agree on a share of the contract and not on a rate per
  megawatt scheduled, the share holds through three winters of stepped-up contracts, the weather correction's straight
  line is checked on cold hours the guideline's sample does not hold, and the held-out winter is shown to be a test the
  wrong reading also passes. No build on file has put its weight there; the last three sit elsewhere (task5, task15,
  task4).
Data-native sentence: three winters of calls sized to the day's need were mostly smaller than the contract and were
  met, so what a provider can deliver shows only on the cold days a call outran it, and the decision is about a call of
  the whole of a contract two to three times the size of any on record.
People: Marion Todd, Clifford Evans, Irene Carpenter (drawn at architecture 5 with guard.py names, the same world)

Guard: card re-registered 2026-11-10 after the stage 4 fix passes, WARN. driver.near 0.17 against this slot's own
architecture 5: the world and the decision are the same at the reviewer's direction, the chain is not (architecture 5 netted
one neighbour's rise; nothing here is netted, and the results are a forecast, a measured share, a backtest, a day profile,
a spread and a bridge). overuse.forum (executive_team): the December capital expenditure review is the world's own.
repeat.gate_g and overuse.gate_g (forecasting, task16): the analysis type assigned is forecasting; task16 forecasts a
benchmark loss from a pilot of training runs, this build reads a limit from the calls that outran it and rebuilds one
day. The forcing event is season_or_peak, the label first filed: the call is forced by the winter 2027/28 peak through
the December review at which a reinforcement has to be committed to be energised before it. The window moved twice on
2026-11-10 (task15 held season_or_peak, so the card carried budget_or_appropriation, an equally honest reading of the
same review; task16, registered earlier and pulled later, then held that one), and the first label is free again.

## Deep reasoning

Task type: Load, price & renewable forecasting (Energy Systems & Utilities, `load-forecasting`), which serves Forecasting & Predictive Modeling: each result is a forecast for a winter not yet begun, or the evidence it holds.
Domain test: a distribution planner forecasts a primary's design-day peak (a weather-corrected peak grown to the winter assessed), credits contracted flexibility at what it will deliver in the evening peak, checks the residual peak across the day's half-hours, and sets the level it stays under at a stated assurance against N-1 firm capacity; the field's own knowledge is that a demand-side provider's delivery is limited by what its enrolled assets have available on a cold evening (a de-rating of registered capacity), that curtailed heating and refrigeration load comes back after a service window, and that a design-day peak is a half-hourly quantity.
Swap: "where do we need to commit a new ward for winter 2027/28, counting the locum cover contracted for that winter" keeps a capacity call and loses megawatts scheduled against a registered contracted capacity, the load that comes back after a service window, the half-hourly day shape that moves a peak from the half-hour ending 18:00 to the one ending 20:00, and a design day set by temperature; none of the eleven results can be stated.
Where the weight sits: R2a and the proof around it. Three readings fit the record about equally well zone by zone (megawatts delivered per megawatt scheduled, a share of the megawatts contracted, the last contract's megawatts unchanged) and file 10.3, 8.1 and 2.9 MW at Ashcombe Road; choosing between them is long work on what the record can test: megawatts scheduled varied at equal temperature and megawatts delivered did not, the two zones of each provider agree on the share and not on the rate per megawatt scheduled, the share is the same winter by winter as the contracts stepped up, and the held-out winter (R3) passes both the right reading and the wrong one.
Layer 1: the SCADA historian's asset ID migration on 14 May 2024 (two point names), values held through comms outages flagged S, a CT fault's zeros flagged B at Ravenhurst Park, rows the outstation never sent, the December 2024 extract re-sent over 30 November; the dispatch log's re-issued and cancelled instructions with superseded rows kept, provider names typed five ways, UK local time beside the weather station's UTC; the weather station's raw readings beside their checked versions and its logger gaps; the control room's switching log, two rows a transfer (closed, then opened to normal), each at the minute it was made; the growth register's withdrawn, quoted and re-entered connections; feeders under their legacy circuit names. None decides a result: held values kept, weather versions averaged in and the first-issued megawatts move no figure out of its band (checks.py, L1 and SF14); the logged transfer days are filed in guideline 3 and, left in, change no call (SF2).
Not one thing: the strongest single piece is the share of the contract available on the design day (R2a); a run that nails it still has to rebuild the day half-hour by half-hour with the load that comes back (R4a, R4, R5: Ashcombe Road's peak is 25.9 MW in the half-hour to 20:00, not the 22.0 MW of the half-hour to 18:00, which is under firm), carry the day-to-day spread in proportion to the 2027/28 megawatts (R6a, R6: Fenwick Street's expected 30.1 MW is under firm, its nine-days-in-ten level 31.2 is over) and build the bridge (R8). Told the share, a pass that still takes the credit off the 17:30 to 18:00 peak with the record's megawatts of scatter reinforces Fenwick Street and Hartwell Common, not the three (checks.py, one-fact test).
One-fact test: "a provider can deliver no more than a share of its contracted megawatts on a cold evening, however many are scheduled" rescues 2 of 11 results (R2a and R2); the sentence about load coming back rescues R4a alone and the sentence about the spread R6a alone, because each later figure needs the others as well.
Not semantics: every field read right (both point names, quality G, the UK clock, the latest revision, the megawatts scheduled and contracted, the daily mean, the logged transfers) still leaves the careful pass on megawatts delivered per megawatt scheduled, the 18:00 half-hour and megawatts of scatter carried unchanged; no field holds what a provider had available, what came back or how much either varies.
Not rule application: the guideline files the WHAT of each result (the design day, the days behind the demand before flexibility, growth, the half-hours whose megawatts count as delivered, the contract scheduled in full, the day's highest half-hour, one design day in ten, firm capacity) and no document says how megawatts delivered relate to megawatts scheduled or contracted, that anything comes back, or how a day-to-day spread is measured or carried; with every filed rule applied, R2a, R2, R4a, R4, R5, R6a, R6 and R8 are still to be estimated (the stage 4 reader's own count: the guideline settles the demand side and the test, and the megawatts delivered, the megawatts off the peak, the nine-days-in-ten level and the backtest stay analysis). Enumerated family for R2 at Ashcombe Road: 21.0 (face value), 10.3 (per megawatt scheduled), 8.1 (share of the contract), 2.9 (the 2025/26 megawatts unchanged); standing family (22 variants of the share reading): 7.5 to 9.0.
Estimand: guideline WPN-NP-G-014 issue 4 sections 2 to 7 and Appendix A, and award notice WPN-DSO-FLX-2026-07: population the four zone primaries; outcome each primary's highest half-hourly demand on the winter 2027/28 design day with its contracted megawatts scheduled in full; megawatts delivered quoted as the delivery in the half-hours ending 17:30 and 18:00, the service delivered through its window; window a working weekday at a daily mean of minus 3.0 C; unit MW; comparison firm capacity, exceeded on more than one design day in ten. The backtest's population and error are in the prompt.
No decoy: nothing is written to carry a wrong answer: no memo, earlier assessment, provider claim or settlement figure states a delivery, a share, a peak or a ranking of the primaries.
No replay: no result re-derives a published figure and no stated number in the pack is wrong.
Pinned: each result's rivals run on the pack and the clean truth (checks.py, the family and SF2 to SF22): the cold days taken at or below 0, minus 1.5 or minus 2 C, a curved line, each zone on its own, the scatter as measured or as the share's own scatter times the award, a heating base of 14 or 17 C, an event's baseline with a slope each winter, with weekday levels or scaled to the day's own level before the window, a met call left out or taken as a floor (five forms), the megawatts fitted over every event (pooled or zone by zone), a cancelled instruction's day kept, the megawatts delivered carried to the award at the rate the three winters' record itself gives, the lower of the two credited half-hours, the first-issued megawatts, the logged days left in; every one reinforces the same three primaries and every figure sits inside its band, which is the range those 22 variants span. The readings outside the family are ruled out by named data: megawatts per megawatt scheduled by the equal-temperature test at Ashcombe Road (the delivered share moves 0.15, standard error 0.12, per unit of share called against the 0.53 it implies) and by the two zones of each provider; megawatts that do not grow with the contract by three winters of stepped-up contracts (megawatts delivered move 0.92 per cent, standard error 0.09, for each per cent contracted: SF22; carried at that rate instead of in proportion, every figure stays inside its band); a curved weather correction by the cold hours the scheduled days do carry (SF21).
Run forecast: R2a and R2, method shortcut (megawatts delivered per megawatt scheduled read at minus 3.0 C and applied to the contract, both architecture 5 rounds' own method); R4a, R4 and R5, unfinished chain (the credit taken off the 17:30 to 18:00 peak; round 2's run 1 named the come-back as "not a full simulation of rebound or a shifted residual daily peak" and went no further); R6a and R6, method shortcut (a range from the fit, or the megawatts of scatter its fit leaves carried unchanged to a contract two to three times the size; both round 2 runs reported a fit's interval); R7 and R8 fall with them; R1 and R3 are earned (R3 because the held-out winter passes megawatts per megawatt scheduled too). Different runs are expected to lose in different places: one that plots megawatts delivered against megawatts scheduled may earn R2a and still lose R4 to R6; one that carries the scatter in proportion earns R6a and Fenwick Street's level and still holds Ashcombe Road.
Strategy label: WORKS IN FORM (the client's Engineering strategy 6, a peak load forecast whose bands hold up, taken as direction only: the lesson that bands from a fit's residuals come out too narrow comes back; the structure does not: this is one winter, four primaries and a contracted intervention's effect on the peak).
Depth level: 5. Four independent judgments each move figures (what a call of the whole contract delivers; the day's peak once load comes back; the spread carried in proportion to one day in ten; the weather correction's line carried past its sample), with the demand forecast, the backtest and the bridge around them; seven shortcuts land on five different wrong sets and none on the golden's (none, Hartwell Common alone, Fenwick Street and Hartwell Common, Ashcombe Road and Hartwell Common, all four), Ashcombe Road needs two of the judgments together or the day rebuilt, and 22 variants of the golden's own choices keep the set.
Lesson: a contracted intervention's effect at a size never called has to be read from what limited it on the occasions it was fully stretched, proved on tests the wrong reading fails (a held-out period is not one of them here), and carried with its own day-to-day spread; no build on file forecasts a contract called in full from a record of part calls.

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | each zone primary's design-day demand before flexibility, winter 2027/28: 30.1, 24.9, 35.5 and 22.9 MW | forecasting | guideline 2 to 5 (the days, the correction to minus 3.0 C, DFES growth, the qualifying connections); the straight line by SF21 | 0.3 MW each side | method shortcut: the highest half-hour on record grown to 2027/28 (the quick pass, right at three primaries and 0.4 MW low at Fenwick Street); the careful pass earns it | - | Ask 1 |
| R2a | the share of its contracted megawatts each provider has available at minus 3.0 C: 0.39 (Corvane Flex) and 0.54 (Quillon Energy Services) | missingness and measurement | the cold days on which nearly every call outran what was available; the award notice's contracted megawatts by winter (registered capacity) | 0.36 to 0.45; 0.50 to 0.59 (22 variants) | method shortcut: megawatts delivered per megawatt scheduled regressed on temperature and read as what a megawatt of contract delivers, 0.46 and 0.61 of the contracts | independent: the events, the contracts and the SCADA record | Component 1 |
| R2 | megawatts each 2027/28 contract delivers at 17:30 to 18:00 on the design day: 8.1, 4.0, 5.4 and 2.9 MW | forecasting | guideline 6 (the half-hours, the contract scheduled in full); R2a carried to the award (SF22) | 7.3 to 9.5, 3.7 to 4.5, 4.9 to 5.9, 2.5 to 3.4 | method shortcut: 10.3 and 5.0 MW at Ashcombe Road and Charlecote Way, whose cold-day calls stopped short of the contract (0.8 and 0.5 MW outside the bands) | R2a | Ask 2 |
| R3 | winter 2025/26's completed events predicted from the winters before: out by 0.19 MW on average | validation | the prompt (last winter's events from the winters before it, the average miss) | 0.10 to 0.29 MW | self-confirming check: megawatts per megawatt scheduled passes the same held-out winter (0.24 MW) because last winter's calls sat as far below their contracts as the earlier ones; the careful pass earns the figure | R2a | Ask 7 |
| R4a | megawatts coming back in the half-hour after the window for each megawatt delivered: 0.32 (Corvane Flex) and 0.26 (Quillon Energy Services) | investigation loops | the half-hours after the window on every completed event | 0.21 to 0.39; 0.16 to 0.34 | unfinished chain: the measurement stops at the window's end and files nothing | independent: the half-hours after the window on the event days themselves | Component 2 |
| R4 | megawatts each contract takes off the day's peak: 4.2, 4.0, 5.4 and 2.9 MW, Ashcombe Road peaking in the half-hour to 20:00 | modeling | guideline 6 (the day's highest half-hour); guideline 4 (every half-hour in the peak's proportion); R4a | 3.9 to 4.6, 3.7 to 4.5, 4.9 to 5.9, 2.6 to 3.4 | unfinished chain: the megawatts delivered taken off the 17:30 to 18:00 peak (10.3 MW off at Ashcombe Road) | R1, R2, R4a | Ask 3 |
| R5 | each primary's expected design-day peak with flexibility: 25.9, 20.8, 30.1 and 20.0 MW | forecasting | guideline 3, 4 and 6; R1 and R4 | 0.3 to 0.6 MW each side | unfinished chain: 19.8 MW at Ashcombe Road and 19.9 at Charlecote Way on the per-megawatt credit off the 18:00 peak | R1, R4 | Ask 4 |
| R6a | each provider's day-to-day spread as a share of what it delivers: 16 per cent at both | uncertainty | the scatter of delivered over contracted about its line on the cold days, net of the baseline's own noise; the same share at a small contract and a large one | 12 to 24; 13 to 23 | method shortcut: the megawatts of scatter its own fit leaves, carried unchanged (7 and 6 per cent of what it delivers), or the fit's own interval | independent: the cold days' scatter about the share's line | Component 3 |
| R6 | the level each peak stays under on nine design days in ten: 26.5, 21.7, 31.2 and 20.6 MW | uncertainty | guideline 7 (one design day in ten); R6a carried in proportion with each primary's day-to-day spread, the day recomputed half-hour by half-hour | 26.1 to 27.0, 21.3 to 22.2, 30.7 to 31.8, 20.1 to 21.1 (the variants' range, and 0.3 MW above it for a rebuild on another baseline with the share's scatter as measured) | method shortcut: 20.5, 20.3, 30.4 and 20.5 MW (Fenwick Street 0.3 MW under its band and under firm) | R5, R6a | Ask 5 |
| R7 | the primaries to reinforce: Ashcombe Road, Fenwick Street and Hartwell Common (their nine-days-in-ten levels 3.5, 0.7 and 2.8 MW over firm); Charlecote Way 0.8 MW inside | synthesis | guideline 7 and Appendix A | the set exact | unfinished chain: Hartwell Common alone on the careful pass | R6 | Recommendation |
| R8 | each contract's megawatts bridged to the megawatts off the peak: of 46.0 MW contracted, 25.6 not available on the design day, 20.4 delivered, 3.9 lost as load comes back at Ashcombe Road, 16.5 off the peaks | decomposition and attribution | the prompt's order (contracted, down to off the peak); R2 and R4 | each bar inside the range the 22 variants span (0.2 to 1.1 MW each side) | unfinished chain: a bridge with no come-back bar and the per-megawatt credit (10.7 MW not available at Ashcombe Road against 12.9) | R2, R4 | Ask 6 |

Carry-forward: R1 stands on the demand side alone. R2a stands on the events and the contracts alone, and R2 and R3 fall with it. R4a has an input of its own (what comes back per megawatt delivered), so a run with R2a wrong can still show the come-back; R4 needs R1, R2 and R4a. R6a has an input of its own (the cold days' scatter); R6 needs R5 and R6a. R7 needs R6 and R8 needs R2 and R4. No analytical result is the only analytical input of more than two others (R2a: R2 and R3).

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| a provider delivers the megawatts scheduled until they outrun what its enrolled assets have available, a share of the megawatts contracted that falls as the evening gets colder | constructed as the provider's dispatch process, in every event | no: all four zones and all three winters (595 events measured; the share on the cold days sits within 0.05 of its provider's line in each of the 12 zone-winters, asserted). The form that misleads (megawatts per megawatt scheduled) misreads Ashcombe Road and Charlecote Way and decides Ashcombe Road alone; Charlecote Way holds either way (asserted) | modelling: megawatts delivered against megawatts scheduled and contracted by temperature, the cold days isolated, the contracts read from the award notice's table of winters | modelling: a share of the contract fitted where calls outran it, carried to a contract two to three times the size, proved by the equal-temperature test, the two zones and three winters of stepped-up contracts | keep: the heaviest result, one of four judgments |
| curtailed load comes back in the hour or two after the service window | constructed as physics (thermal and refrigeration payback), after every completed event | no: every zone (0.25 to 0.33 MW per megawatt delivered in the first half-hour at each, asserted); left out with the day still rebuilt it misreads Ashcombe Road's peak by 2.1 MW and changes no primary's call (asserted) | a targeted look at the half-hours after the window, once the day is rebuilt half-hour by half-hour | modelling: per megawatt delivered, carried to the larger delivery, the day's peak recomputed | keep |
| what a provider has available varies from evening to evening in proportion to its level | constructed as customer and asset behaviour, in every event | no: both providers, every zone (megawatts of scatter 0.38 at Ashcombe Road against 0.20 at Hartwell Common, asserted); the misreading (megawatts of scatter unchanged) misreads every level and, with megawatts per megawatt scheduled, leaves Fenwick Street under firm | modelling: the scatter about the cold-day line, net of the baseline's own noise | modelling: carried in proportion to the 2027/28 megawatts with the baseline's spread, the day recomputed | keep |
| calls sized to the day's need and capped at the contract | constructed as the DSO's scheduling process, filed in the award notice's service terms | no: every instruction | reading the award notice | none: it is why part calls and full calls both exist | keep, the process that makes R2a matter |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 design-day demand before flexibility, MW | Partly | Right | Right |
| R2a the share of its contracted megawatts each provider has available on the design day | Missed | Missed | Right |
| R2 megawatts each contract delivers at 17:30 to 18:00 on the design day | Missed | Partly | Right |
| R3 last winter predicted from the winters before: the average miss, MW | Missed | Right | Right |
| R4a megawatts coming back in the half-hour after the window, per megawatt delivered | Missed | Missed | Right |
| R4 megawatts each contract takes off the day's peak once the load that comes back is counted | Missed | Partly | Right |
| R5 expected design-day peak with flexibility, MW | Missed | Partly | Right |
| R6a each provider's day-to-day spread as a share of what it delivers, per cent | Missed | Missed | Right |
| R6 the level each peak stays under on nine design days in ten, MW | Missed | Missed | Right |
| R7 the primaries to reinforce | Missed | Missed | Right |
| R8 each contract's megawatts bridged to the megawatts off the peak | Missed | Partly | Right |
| Roughly | 0.5 of 11 | 4 of 11 | 11 of 11 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json (generator/effort_passes.py runs each pass end to end on the cut pack; no cell hand-graded)
Largest single hint: a provider can deliver no more than a share of its contracted megawatts on a cold evening, however many are scheduled; rescues 2 of 11 results
Pair estimate: 38.4

The careful column is the platform runs' own method on this world (both architecture 5 rounds: every file cleaned, a
weather-adjusted baseline, megawatts per megawatt scheduled with a temperature interaction, a backtest on the last
winter), graded up where the record leaves a doubt: its one-day-in-ten level uses the megawatts of scatter its own fit
leaves on the freezing days with the demand's day-to-day spread (not the fit's interval both round 2 runs reported),
and its backtest is earned. It earns R1, R3 and the cells of R2, R4, R5 and R8 at the two zones whose cold-day calls
took the whole contract. The seven asks are numbered as the prompt lists them and the three components are the findings
they stand on, so no result is priced twice. The paper is optimistic, and the price has a range: a run that carries
the scatter in proportion to what it delivers (still per megawatt scheduled, still off the 18:00 peak) earns half of
R6a and of the set (Fenwick Street and Hartwell Common) and prices at about 49; a run that plots megawatts delivered
against megawatts scheduled sees the plateau, and one plot of the evening after the window shows the come-back; each
still leaves the other results to earn.

## Data provenance

Source: generated by the generator from a simulated process (generator/world.py simulates the DSO, its providers and the control room; pack.py writes what their systems record).
Behaves like the real thing: the process simulated is a DSO's scheduled peak-reduction service: demand at nine primaries driven by the station's daily mean temperature with a day effect and a half-hourly shape by customer mix; a day-ahead forecast with its own error; calls sized to hold each primary at 92 per cent of firm capacity in half-megawatt steps and capped at the contract; a provider that delivers what is scheduled while its assets can and the available megawatts when they cannot, with the load coming back after the window; revisions and cancellations on the morning; ordinary 11 kV switching. It matches published behaviour of aggregated demand-side flexibility: delivery de-rated from registered capacity in cold weather, under-delivery concentrated on the largest calls, payback after thermal curtailment, day-to-day variability of a tenth to a fifth of the level.
Genuine patterns: (1) seasonal and cold-spell temperature with day-to-day persistence, and demand rising with heating degrees at a slope by primary; (2) a weekday and weekend half-hourly shape by customer mix, a Christmas dip and year-on-year growth by primary; (3) calls larger on colder days and on bigger forecasts, met when mild and short when cold; (4) the share available falling as it gets colder, by provider; (5) load coming back after every event, larger for the heat-pump portfolio; (6) scatter in delivered megawatts that grows with the contract; (7) forecast error common to the zones on a day.
Problems by process: point renames at the asset ID migration; held and bad values from comms outages and a CT fault; rows the outstation never sent; a monthly extract re-sent; superseded dispatch rows and provider names as typed; raw and checked weather readings; logger gaps; two-row transfers in the switching log; withdrawn and re-entered connections; legacy circuit names.
Breadth: 196,213 SCADA rows (nine primaries, three winters, half-hourly), 697 dispatch rows (606 completed instructions, 595 measured), 13,372 weather rows, 60 switching rows, 12 files; the events have to be sorted by temperature, by megawatts scheduled against contracted and by zone and winter before any reading of them can be tested.

## Template check

Chain signature: forecasting, missingness-measurement, forecasting, validation, investigation-loops, modeling, forecasting, uncertainty, uncertainty, synthesis, decomposition-attribution
Question form: where (where in the zones reinforcement has to be committed), then each result asked for zone by zone
Nearest build: task1 (forecast-bands-drivers, weight synthesis: a subscription book's ARR path built from five flows each with its own mechanism). What differs: the chain (task1 opens on a reconciliation and sums flows over months; this one measures a limit seen only when a call outruns it, proves it on tests the wrong reading fails, rebuilds one day half-hour by half-hour and carries a spread), the weight (validation), the unit (four primaries on one design day, not a monthly path) and the data (telemetry and a dispatch log against contract ledgers). The abstraction sentence that would make them the same ("a forward figure with a range and its components") is the answer shape itself, not the chain.

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | the design day | a working weekday at a daily mean of minus 3.0 C, the GMT day's hourly mean; a local-day mean | the GMT-day mean | guideline 2 |
| SF2 | the days behind the demand before flexibility | 2025/26 working weekdays outside Christmas, scheduled days and logged transfer days; the logged days left in | the logged days left out | guideline 3; left in, the same call (asserted) |
| SF3 | growth to 2027/28 | DFES rates compounded, qualifying connections in full, every half-hour in the peak's proportion | as filed | guideline 4 |
| SF4 | a contract's megawatts delivered | its delivery in the half-hours ending 17:30 and 18:00, as their mean; the lower of the two; the half-hour ending 18:00 alone (the prompt's 17:30 to 18:00 read as one half-hour) | the mean | guideline 6 (quoted as its delivery in those half-hours); the lower of the two and the half-hour ending 18:00 alone: same call, every figure inside its band (asserted) |
| SF5 | megawatts scheduled on the design day | the contract in full; the megawatts the day would need | the contract in full | guideline 6 |
| SF6 | demand with flexibility | the day's highest half-hour with the service delivered through its window; demand reduced in the half-hours ending 17:30 and 18:00 alone | the service through its window | guideline 6 as reworded after judge r2, whose own first pass took the earlier wording ("the megawatts delivered are those in the half-hours ending 17:30 and 18:00 ... no other measure is credited") as a credit in those two half-hours alone and reinforced all four: "with the service delivered through its window", the two half-hours being how a contract's megawatts are quoted (asserted on the PDF's text) |
| SF7 | one design day in ten | the 0.9 quantile of the day recomputed half-hour by half-hour; a normal reading at the peaking half-hour | the day recomputed | guideline 7; the normal reading within 0.25 MW (asserted) |
| SF8 | megawatts contracted in past winters | the award notice's table of three winters, registered capacity | as written | the award notice, sections 1 and 4 |
| SF9 | the cold days | at or below minus 1.0 C; 0, minus 1.5 or minus 2 C | minus 1.0 C | same call, every figure inside its band (asserted) |
| SF10 | the line through the share | straight in temperature; curved | straight | same call, inside the bands (asserted); the curve's held-out miss is 0.26 MW against 0.19 |
| SF11 | provider or zone | each provider's two zones together; each zone on its own | together | same call, inside the bands (asserted) |
| SF12 | the scatter | relative to the level, net of the baseline's own noise; as measured; the share's own scatter as measured times the award (pooled or zone by zone) | relative, net | same call, inside the bands (asserted) |
| SF13 | the heating base | 15.5 C; 14 or 17 C, carried through the events' baselines as well | 15.5 C | same call, inside the bands (asserted) |
| SF14 | an instruction's megawatts | its latest revision; the megawatts first issued | the latest revision | same call, inside the bands (asserted) |
| SF15 | the backtest | winter 2025/26's completed events from winters 2023/24 and 2024/25; the average miss | as the prompt says | the prompt; the miss runs 0.13 to 0.26 MW across the variants, inside the stated 0.10 to 0.29 (asserted) |
| SF16 | an event's temperature | the event day's daily mean at the station | the daily mean | guideline 2's measure |
| SF17 | the bridge's bars | contracted, not available, delivered, lost as load comes back, off the peak, in that order | that order | the prompt (from each contract's megawatts down to the megawatts off the peak); the bars add up (asserted) |
| SF18 | the baseline an event's megawatts are measured against | winter levels and one heating slope by half-hour; a slope each winter, weekday levels, or that baseline scaled to the day's own level in the half-hours before the window | winter levels and one slope | same call, inside the bands (asserted) |
| SF19 | a call that was met | kept among the cold days as measured; left out, taken as a floor (over the cold days, the days at or below 2 C or every day, on a straight or a curved line), or the megawatts fitted over every event as the lesser of the megawatts scheduled and the share (pooled or zone by zone) | kept as measured | same call, inside the bands (asserted) |
| SF20 | a cancelled instruction's day | a scheduled day, left out of the baselines; kept | left out | same call, inside the bands (asserted) |
| SF21 | the weather correction | straight in heating degrees; curved | straight | named data: the guideline's 2025/26 sample holds no day colder than plus 4.7 C, and in the hours before the service window, which the scheduled days carry, the line fitted on such days lands the days at or below 0 C within 1 per cent at every zone primary while a curve misses them by more; the curve's t on the daily peak is under 2 at all nine primaries (asserted) |
| SF22 | what is available against the megawatts contracted | in proportion (a share of registered capacity); at the rate the three winters' record itself gives (0.92 per cent for each per cent contracted); megawatts that do not grow | in proportion | the award notice (contracted megawatts are registered capacity); at the record's own rate: same call, inside the bands (asserted); megawatts that do not grow: named data, the rate's standard error is 0.09, so in proportion is inside two standard errors and none is ten away (asserted) |
| SF23 | the megawatts through the service window | the reduction each half-hour of the window shows on the events (a ramp in and out); the megawatts quoted taken flat through the window | as the events show | same call, every figure inside its band (asserted) |

## Closure table

| Axis | Closure |
|---|---|
| 1 Population | the four zone primaries of the award notice; filed (guideline 1, the awards) |
| 2 Unit of account | a primary substation, MW at its SCADA total; filed (guideline 3) |
| 3 Attribution window | megawatts delivered in the half-hours ending 17:30 and 18:00; the day's highest half-hour for the peak; filed (guideline 6; SF4, SF6) |
| 4 As-of dating | the exports of 1 to 3 November 2026, the awards of 21 October 2026; C1, no later record is read |
| 5 Version basis | guideline issue 4, awards WPN-DSO-FLX-2026-07; filed |
| 6 Denominator | megawatts contracted (registered capacity) by winter; filed in the award notice (SF8, SF22); megawatts scheduled is the rival ruled out by data |
| 7 Weighting | each completed event once; C1 (SF11, zone or provider) |
| 8 Window length | 2025/26 for the demand before flexibility (guideline 3); three winters of events; the backtest's split in the prompt (SF15) |
| 9 Boundary inclusivity | "exceed" strictly; no primary within 0.3 MW of firm at the one-in-ten level across the variants (margins, asserted) |
| 10 Rounding path | unrounded to the end, MW to one decimal and the average miss to two, as the prompt says |
| 11 Tie-break | none: no primary at its firm capacity |
| 12 Maturity and censoring | winter 2025/26 complete to 31 March 2026; a met call shows only a floor on what was available, handled by the cold days on which calls outran it; left out or taken as a floor it moves no figure out of its band (SF9, SF19) |
| 13 Order of operations | cleaned, corrected, grown, the day rebuilt, the spread carried; C1 |
| 14 Row order | the dispatch log by reference and revision; the switching log by time; C1 (SF14) |
| 15 Duplicate resolution | the re-sent SCADA overlap once; each weather hour at its checked version; C1 (L1) |
| 16 Identity normalisation | SCADA points under both names; feeders under both codes; providers as typed; C1 (L1) |
| 17 Netting against gross | none: nothing is netted; the logged transfer days are left out (guideline 3, SF2) |
| 18 Dimensional units | MW of real power, not Mvar; filed (guideline 3) |
| 19 Code and status semantics | quality G kept; status Completed; a cancelled instruction's day a scheduled day (SF20); Accepted and Energised connections; filed and C1 (L1) |
| 20 Integerisation | none: megawatts are continuous and no count is graded |
| 21 Clause scope | guideline 2 to 7 for the peaks and the call; the award notice's sections 1, 2 and 4 for the megawatts |
| 22 Forward window contents | winter 2027/28: its contracts scheduled in full, growth to 31 October 2027, the design day at minus 3.0 C; filed (guideline 4 and 6; SF5) |

## Literal reader

Guideline 2: the design day is a working weekday at a daily mean of minus 3.0 C (R1 to R7's condition). Guideline 3:
demand before flexibility from the 2025/26 working weekdays outside Christmas, scheduled days and logged transfer days,
corrected to that day (R1). Guideline 4: DFES rates compounded, the qualifying connections in full, every half-hour in
the peak's proportion (R1, and the day's half-hours for R4 and R5). Guideline 5 and Appendix A: firm capacity (R7).
Guideline 6: what the provider will deliver with the megawatts contracted scheduled in full for the service window; a
contract's megawatts delivered are quoted as its delivery in the half-hours ending 17:30 and 18:00 (R2); demand with
flexibility is the day's highest half-hour with the service delivered through its window (R4, R5).
Guideline 7: reinforce where that would exceed firm capacity on more than one design day in ten (R6, R7). The award
notice: megawatts contracted for 2027/28 and for the three winters past, registered capacity; calls sized to the
forecast above 92 per cent of firm capacity, in steps, up to the contract. The prompt: each result named with its unit;
what last winter's events delivered at 17:30 to 18:00 from the winters before it, as the average miss in MW (R3); from each contract's megawatts down to
the megawatts off the peak (R8); MW to one decimal and the average miss to two. Every sentence executes to the golden's
quantity; none says how megawatts delivered are to be estimated, that load comes back, or how a spread is measured.
Judge r1 executed the same sentences from the bundle alone and reproduced the demand side to two decimals and every
megawatt figure inside its band; the one figure it could not pin (a count of freezing-day events inside an 80 per cent
range) is no longer asked. Judge r2, deriving before it saw the blocks, reproduced every figure again and showed that
guideline 6's earlier wording could be executed as a credit in two half-hours alone (all four reinforced); the section
now says the service is delivered through its window and that the two half-hours are how a contract's megawatts are
quoted.

## Prompt contract

A voice rewrite may not drop or change: the question (where to commit reinforcement for winter 2027/28, Halverton
flexibility zones); for each zone the design-day demand before flexibility, the MW the 2027/28 contract delivers at
17:30 to 18:00 on the design day, the MW taken off the day's peak, the expected peak, the level it stays under on nine
design days in ten, against firm capacity; the walk from each contract's MW down to the MW off the peak; how far out on
average, in MW, the same approach would have been on what last winter's events delivered at 17:30 to 18:00, with only
the winters before it to go on; a
spreadsheet with a chart and a few slides for the capex review; MW to one decimal and the average miss to two. It must
never add: a file name, who is asking, how megawatts delivered are to be estimated, the words share, available, come
back, rebound or range from residuals, a temperature, a count of zones, winters or events.

## Leak rulings

leak.py on target.zip d84ca1b2: REVIEW, no LEAK. Ruled in the main thread:

- Answer figures in the pack (23.0, 22.5, 30.5, 17.8, and 21.0 and 19.5 for two primaries outside the zones; 21.0, 10.0,
  7.5; 3.5; 4.0 and 4.5): the firm capacities of guideline Appendix A, the megawatts contracted in the award notice, the
  service window's hours and past contracts. Each is an input every answer block quotes beside its results; none is a
  result.
- The committed call's words in the guideline and the award notice: the primaries' names, reinforcement, firm capacity
  and winter 2027/28 are those documents' own subject; neither names a primary to reinforce.
- Design-note vocabulary in the two documents (megawatts, scheduled, contracted, forecast, guideline, the primaries):
  the service's own terms. No document says what a call delivers against the megawatts scheduled or contracted, that
  load comes back after a window, or how a day-to-day spread is measured or carried (checks.py, documents name no
  step). The award notice's availability fee (GBP per MW per hour) is its payment term.
- Candidates beside numbers (the guideline, the award notice, the dispatch log, the register, the transformer
  condition file): ratings, contracted megawatts, scheduled megawatts and oil results; none sets a primary's demand
  with flexibility against its firm capacity (Gate G).
- Single-use test: every file the results read has a use of its own (the SCADA export is the demand side's source and
  the events' measure; the dispatch log is the DSO's instruction record; the switching log is filed in guideline 3; the
  award notice carries the megawatts and the service terms). No file exists to carry a result.

The stage 4 reader read the pack cold three times (after each fix pass that changed a document or the prompt; its
answers are in leak_check_report.md under Solver's-eye read). Ruled:

- Questions 1 and 5: the guideline files the design day, the sample, growth, the credited half-hours, the day's highest
  half-hour and the one-day-in-ten test, and the award notice the scheduling rule: the WHAT of each result, and each
  literal execution is the golden's quantity. On the final wording the reader executed guideline 6 as a reduction
  through the whole service window, the megawatts delivered being the contract's delivery in the two half-hours. The
  options the text leaves each keep the call and every figure inside its band: a cancelled instruction's day (SF20), the
  prompt's 17:30 to 18:00 read as one half-hour (SF4), the megawatts taken flat through the window (SF23), a
  transfer's days as the operation dates alone (inside SF2's extreme).
- Questions 2, 3 and 4: no file ranks the primaries on the question, none exists only to help the analyst and no figure
  reads as an answer.
- Question 6: the reader names the guideline as what makes the demand side and the test routine, and the megawatts
  delivered, the megawatts off the peak, the nine-days-in-ten level and the backtest as analysis. That is R1 and the
  criterion, one earned result of eleven, not most of the chain; the judge's measurement of the routes agrees.
- Question 7: workbook zip entries stamped 1980-01-01 are the application's own entry stamp (reduce-house-fixes H1);
  the workbooks created before their latest content are living registers, each last saved after its latest record
  (checked); the switching log was fixed in the generator on the readers' three findings (the minute of each operation,
  references in time order, ammeter readings at their own voltage and power factor, holiday transfers as fault
  restoration; no figure moved); the award notice's contract history in half-megawatt lots is the service's own step
  and the awards at multiples of the last contracts are the scenario's premise, which the reviewer's audit names as the
  judgment to test: left.

## Pre-ship check

Written 2026-11-10 on the final cut (target.zip d84ca1b2), the bar re-read against the built pack.

- The reviewer's direction, taken point by point. The transfer is documented: the control room's switching log is in
  the pack, guideline 3 leaves its days out, and nothing in the answer is netted for it. The call turns on judgments
  that each move a figure: the cold-weather decline of delivery (R2a: 0.39 and 0.54 of the megawatts contracted at
  minus 3.0 C, a straight line whose held-out miss is 0.19 MW against 0.26 for a curve); whether delivery scales to
  awards 1.9 to 2.8 times the 2025/26 contracts (R2 and SF22: 8.1 MW of 21.0 at Ashcombe Road, against 10.3 on
  megawatts scheduled and 2.9 if nothing grew); how the uncertainty is carried to the margin (R6a and R6: Fenwick
  Street 0.4 MW inside firm on the expected day and 0.7 over at the nine-days-in-ten level, and 0.1 inside if a small
  contract's megawatts of scatter are carried unchanged with megawatts per megawatt scheduled). A fourth, the day
  rebuilt with the load that comes back, moves Ashcombe Road's peak from 22.0 MW at 18:00 to 25.9 at 20:00.
- Not one thing, measured on the cut: seven shortcuts give five different wrong sets and none gives the golden's;
  Ashcombe Road needs the day rebuilt, or the share and the proportional spread together; Fenwick Street needs a
  day-to-day spread carried in proportion; told the single most useful sentence, the careful pass still reinforces
  Fenwick Street and Hartwell Common (2 of 11 results rescued).
- The hidden factor record against the cut data: the share within 0.05 of its provider's line in all 12 zone-winters;
  the come-back at every zone (0.25 to 0.33 MW per megawatt delivered); megawatts of scatter 0.38 at Ashcombe Road
  against 0.20 at Hartwell Common. No effect sits only where it decides: megawatts per megawatt scheduled also misreads
  Charlecote Way, where nothing turns on it, and the come-back runs at three zones whose peak it does not move.
- The effort test against effort.py: quick 10.9, careful 38.4, thorough 100, no cell hand-graded; the careful pass is
  graded up (its megawatts of scatter rather than the fit's interval, its backtest earned), and a run that carries the
  scatter in proportion prices at about 49.
- Determinism, three isolated passes on 2026-11-10. r1 (blocks inside its brief, so weaker on Gate C): every megawatt
  figure inside its band, FIX_NOW on a count of freezing-day events inside an 80 per cent range; the count is no
  longer asked. r2 (own derivation first): every graded figure inside its band, FIX_NOW on wording and on guideline
  6's two half-hours, which its first pass executed as the whole credit; the section is reworded in the pack, the
  megawatts' floor at Ashcombe Road follows its fits, and the prompt names what the backtest's miss is measured on.
  r3 (the one re-judge, own derivation first, on the final prompt and documents): DETERMINISTIC. Its own derivation,
  written before it opened the blocks, reinforces the same three primaries and lands every megawatt figure inside its
  band; FIX_NOW on the solution side only, applied as it prescribes (the nine-days-in-ten bands reach 0.3 MW above the
  variants, since its rebuild with the share's scatter as measured sits there; three clarifying sentences). No golden
  figure moved after r3. The pack it judged (1ee96fa6) differs from the final cut only in the switching log's
  references, ammeter readings and two reasons, which no figure reads (figures.json and submission.md byte-identical).
  Its Gate H line: no one thing; quick 2, careful 5, thorough 9 of 9 graded items; the share sentence rescues about 2
  to 3 of 9 (this note counts 2 of 11 whole results, with part cells of four more).
- Leak: three cold reads (the last on the final wording), no file that ranks the primaries, no helper file, no figure that reads as an answer; the
  guideline settles the demand side and the test (one earned result), the rest stays analysis by the reader's own
  account.
- Gates on the final cut: precut exit 0 with one WARN (R2a upstream of seven results; the largest hint measured at 2 of 11),
  effort PASS (pair 38.4, the note agreeing, no cell hand-graded), the prompt gate PASS (766 characters), figures PASS
  (187 figures), leak.py REVIEW with no LEAK, heart WARN, surface PASS, checks.py 62 of 62, the independent verifier
  PASS, two builds byte-identical, the container gate PASS on both zips.
- What stays uncertain: the careful column is calibrated on four architecture 5 runs made in another mechanism. A run
  that plots megawatts delivered against megawatts scheduled sees the plateau, and one that rebuilds the day sees the
  evening after the window; each of those earns its results and leaves the others. The platform's two runs are the
  measurement.

## Tried and rejected

- Architecture 6, nine-days-in-ten bands set by the variants with 0.1 MW either side: judge r3 (2026-11-10), from its
  own baseline and the share's scatter as measured, put Fenwick Street at 31.6 and Hartwell Common at 21.0, at and above
  the bands' tops. The share's own scatter joined the family (22 variants) and those bands reach 0.3 MW above it.
- Architecture 6, switching log references in generation order, ammeter readings an exact function of the megawatts,
  and planned jobs over New Year: the third cold reader named all three; references now run in time order, each reading
  has its own busbar voltage and power factor, and a transfer made over Christmas, New Year or a bank holiday is logged
  as fault restoration. No figure moved.
- Architecture 6, guideline 6 worded "The megawatts delivered are those in the half-hours ending 17:30 and 18:00 ... No
  other measure is credited": judge r2 (2026-11-10), deriving before it opened the blocks, credited the contract in
  those two half-hours alone, let the peak slide to 18:30 and reinforced all four primaries. A filed sentence whose
  literal execution gives another call is a fork whatever the events show, so the section now reads "A contract's
  megawatts delivered are quoted as its delivery in the half-hours ending 17:30 and 18:00 ... its highest half-hourly
  demand on that day with the service delivered through its window. No flexibility other than the contracted service
  is credited."
- Architecture 6, a floor of 7.8 MW on Ashcombe Road's megawatts delivered: judge r2's own fits (megawatts fitted over
  the whole record, zone level) gave 7.5 to 7.7. Megawatts fitted over every event and the three winters' own scaling
  joined the family (20 variants), the megawatts' band is never narrower than the share's band times the award, and the
  floor is 7.3.
- Architecture 6, the backtest's count of freezing-day events inside an 80 per cent range as a graded figure: judge r1
  (2026-11-10) reproduced every megawatt figure and found the count at 29 to 45 of 50 under its own cuts; across this
  generator's variants and six constructions of the range it runs 25 to 40. A figure reasonable methods spread that
  widely is unpinned, so the prompt asks the average miss alone and no count is graded.
- Architecture 6, bands set by nine variants of the golden's own choices: they left out the baseline an event's
  megawatts are measured against, the handling of a met call and a cancelled instruction's day, and the heating base
  was varied on the demand side only. A baseline scaled to the day's own level, a met call taken as a floor and a
  heating base of 14 C carried through the events each landed outside a stated band. The family is 17 variants and every
  band is the range they span.
- Architecture 6, Ashcombe Road at 16.0 MW contracted: megawatts per megawatt scheduled with the scatter carried in
  proportion reached the golden's three primaries with wrong megawatts (24.0 MW against firm 23.0), and the available
  share alone put its 18:00 half-hour over firm. At 21.0 MW the 18:00 half-hour is 22.0 MW, so Ashcombe Road needs the
  day rebuilt, or the share and the spread together, and none of seven shortcuts reaches the set.
- Architecture 6, the careful pass with the fit's own range and R3 priced as a result it loses: graded up to the
  megawatts of scatter its own fit leaves, carried unchanged, with its backtest earned (0.24 MW, inside the band: a
  held-out winter passes megawatts per megawatt scheduled too). With the asks numbered as the prompt lists them and
  the components as the findings they stand on, the pair estimate is 38.4 on eleven results (it was 42.5 on eight).
- Architecture 6, switching operations logged on the quarter-hour with durations in round hours: the stage 4 reader
  named the 15-minute steps; the log now carries the minute each operation was made, and no figure moved.
- Architecture 6, a deck and a chart title saying the three primaries are over firm "on nine design days in ten":
  Fenwick Street is over on about three; the titles now say "on more than one design day in ten" (guideline 7's words).
- Architecture 6, a two-winter event record with calls of the whole contract every time (architecture 5's dispatch):
  there was no megawatts-scheduled variation to test, and with calls sized to need over two winters Quillon's zones
  fell short on too few days (the variants of its share spanned 0.36 to 0.52). Three winters of events, calls sized to
  the forecast above 92 per cent of firm capacity, contracts sized so cold-day calls outrun what is available.
- Architecture 6, an S-shaped availability curve: a straight and a curved line through the cold days differed by 0.03
  at the design day and split Fenwick Street's megawatts by 0.4; the curve is now close to straight over the cold range.
- Architecture 6, a backtest by winter as the test between megawatts scheduled and megawatts contracted: it cannot
  tell them apart (0.24 against 0.20 MW), because the last winter's calls look like the earlier ones; the backtest
  separates growth with the contract from none, and the equal-temperature test and each provider's two zones separate
  scheduled from contracted.
- Architecture 6, the backtest's range counted on the days at or below minus 1.0 C: naming that cut in the prompt would
  have filed the golden's own choice of cold days; the prompt counts days below 0 C.
- Architecture 6, Fenwick Street at 10.5 or 12 MW contracted: its nine-days-in-ten level sat 0.15 to 0.45 MW over firm
  across the variants; at 10.0 MW it sits 0.3 to 1.0 over and its expected peak 0.1 to 0.8 under.
- Architecture 6, held (S) values: kept in, a held stretch inside an event evening tripled the scatter and moved every
  one-in-ten level; the outstations are polled on a second route through service windows, so no event evening is held.
- Architecture 5 (the provider's reduction net of the load a control room moved to the primary across an open point,
  read at minus 3.0 C; golden Ashcombe Road and Hartwell Common): spent on the platform's holistic audit of 2026-11-10.
  Both runs lost at the deciding step (rung 1b, Ashcombe Road alone, 0.67 to 0.75 per MW at the zone meter; a method
  shortcut and a self-confirming check) and the audit still read the step as a plant: the neighbours step up a flat
  1.4, 1.4 and 0.8 MW on event days whatever the megawatts scheduled, absent on cancelled days, so one sentence names
  it and one subtraction lands the call. A hidden concurrent action with a discrete signature is a planted factor
  however analytical the netting; the transfer is now documented texture and the deciding step moves to judgments
  the record has to settle (`runs/review_2026-11-10.md`).

- A mix shift by author tenure (new accounts' posts carry most review items, and AI took the newcomers): rejected at the
  draw, because the account-age column makes the segmentation a reflex the opponent runs on every visible attribute.
- Spam and flags scaling with page views rather than questions: rejected at the draw, because a per-queue trend of the
  flags already follows views, so the reflex lands, and the swap test reads it as generic demand forecasting.
- A volunteer pool with two retention types (veterans and casual reviewers) as a rung: dropped at the prototype, because
  the defensible retention estimators (tenure bands, pooled recent churn, a heterogeneity fit) split the per-site
  figures by up to 0.8 FTE; every site's pool now leaves at one steady rate since the pipeline dried up.
- Item and flag rates per question stepping up in 2023: dropped at the prototype, because a pooled ratio (over the
  step) and a reviewer trend over 2024 carry errors of opposite sign that cancel near the golden; both rates hold steady.
- Sizing the pool on the busiest 2027 month (shape 02): dropped at the prototype, because each late-2027 month's network
  hours carry about 300 hours of one-sigma spread, too wide for a monthly grid at any natural rounding.
- A volunteer pace with a wide spread across reviewers (KAPPA_SIG 0.60): the 2021 to 2023 and 2024 to 2026 saturated
  paces differed by 3.6 per cent, which moved Data & ML across its bin between eras; reviewers' own paces now spread at
  0.15.
- A Poisson trickle of new reviewers after the pipeline dried up: carried or dropped, it moved two sites by 0.4 FTE; the
  trickle is now a floor share (0.004) of the old inflow, and no construction moves a site.
- Pre-platform reviewers' grant dates drawn freely: they piled up at January 2013; tenure is now bounded by each site's
  launch on the register.
- Cover targets calibrated against random-walk inflows and exits: the calibration moved the wrong way; exits and inflow
  are now constructed (zero-sum swings within each quarter), and the January to September 2026 cover targets of
  Databases and Embedded & Hardware were set at 1.137 and 0.76 to centre their needs in their bins.
- Question moves drawn by source site: they ran the wrong way and reached 90,000 rows; moves are drawn into each
  destination at 0.55 of the first shares (49,530 rows).
- October to December 2026 on the chart with no question driver: a trend of each site's questions would be an open
  fork; the plan workbook carries the planning team's outlook sheet for those months, used only for the chart.
- WFM shifts of 7.5 paid hours: half the quarter totals ended on a half hour, a rounding fork at the nearest hour;
  shifts are now 8 paid hours, short days, overtime and corrections in whole hours.
- First actions on flags with an unbounded lognormal tail: some ran past the moderator tool's export run, dating rows
  after the as-of; a flag left past 90 hours is now escalated and taken within the next week of hours (no Ask A figure
  moves), and a review still open at the export keeps its first action as the handled time.
- The network first named Quernstone: a UK accounting firm carries that exact name (Companies House 04197485); the
  network is now Millrind (no company, network or software of that name found).
- Ask C's stop "each move applied in the month it moved": it files the golden's nine (no move straddles the window's
  edges enough to cross a rounding step), so it is recorded as a convergence, not a stop; Ask A's over-correction stop
  (reviewed flags dropped) misses 14 of 27, not 27.
- target.zip cut with a `target/` folder inside: the archive now carries the files at its root (house fix H4).
- Round 1, Ask C's device left silent (no file said how the old statistics job counted a moved question): the judge
  licensed three readings one decimal apart at every site (FIX_NOW). The warehouse notes now file the old job's counting
  and the comparison basis in the data team's voice; both other readings are asserted out. The device is no longer
  silent, so the cracker and the mirror both land Ask C (cracker sheet `hit`).
- Round 1, slide 2's series undefined (hours worked or need hours, flags in or out, which close standard, how October
  to December 2026 is counted): the operations notes now define paid review hours once, the prompt asks each year's
  actual hours totalled, and the three actual totals are graded and asserted (36,419, 36,233 and 29,626 hours); being
  construction figures, both top responses land them (cracker sheet `hit`). With Ask C, the pair ceiling moves from
  31.0 to about 41.0, over the 40 build target and under the 50 bar; precut fails its pair-ceiling and cracker rows on
  this alone, reported to the coordinator.
- Round 1, the roster missed the reviewers whose access lapsed in January or February 2024 without a platform review
  (its dictionary scope said every reviewer with access since 1 January 2024): a lapse rate read by lapse date then
  counted zero lapses in those months (1.92 per cent, 33). The 689 rows are now in the roster (first review blank), the
  dictionary's scope and lapse rule carry a worked example, and the lapse-date reading files the same nine.
- Round 1, the items no volunteer ever picks up drawn at one share for every item type: routed shares were identical
  across types in slack months, which read synthetic. Each type now has its own (close votes 0.91, low quality 0.72,
  edits 0.40, first posts 0.35 per cent); no graded figure moved. In saturated months the shares stay close across types
  because the 72-hour hand-off takes the oldest items first whatever their type; a per-type volunteer preference would
  change the routed mix that prices the frozen call, so it was not added.
- Round 1, the 24-hour share's denominator and the envelope's sign: the flag service standard now defines flag
  response as a share with the post-deleted closures out of both counts, the prompt names the measure (24-hour flag
  response), and the prompt asks how far above or below the envelope the request sits.
- Round 1, the question plan's 2026 actuals sheet stamped as pulled 8 October inside a workbook issued 18 September:
  the sheet now carries January to August 2026 as pulled on 14 September (no figure reads it).
- Round 2, Ask C held only less careful solvers once round 1 filed the old job's counting (the cracker landed it, precut
  failed): the 2022 sheet now carries the tag-sync undercount of May to August 2022 as first reported, with the
  statistics job's March 2023 restatement below its notes (sites down, months across); the careful-but-literal path
  misses all nine (nearest 0.27 points) and the golden's nine figures are unchanged.
- Round 2, the chart's three actual yearly totals (round 1): construction figures both top responses land; out of the
  prompt and the deliverable answers. The chart is graded on its content, its series filed in the operations notes and
  its months on the workbook's Monthly hours sheet. The pair ceiling is back to 31.4.
- Loop 3 (2026-10-27), the portal landed the call: both responses filed 35 FTE (the then golden) by building capacity
  against the inbox at the saturated pace and carrying each pool at its own lapse rate; the capacity framing was every
  strong solver's default, so it is now the default path and the decisive step moved to how the pool is carried.
- Two retention types with the pipeline drying in late 2024 or summer 2025: a trend of the network's lapse rate,
  extrapolated, landed the golden by coincidence (the closed pool's decline was already plain in the record); review
  access now closes on 1 September 2026, so the record shows only an open pool's flat rate.
- Grants following the question level squared (older pools at the sites AI hit hardest): the separations shrank and the
  trended-rate routes still tracked the golden; grants now follow the question level.
- Grants drying in January 2026 with the last twelve months' grants carried on: the two errors cancelled on the golden;
  with invitation-only access filed, no window of past grants is a reading of 2027.
- Invitations at 2 per cent of the old flow: carrying or dropping them moved a site by 0.44 FTE in all; invitations
  are now a handful a year and none fell in September.
- Covers calibrated by re-drawing the whole pool at each step: a site's need jumped by up to a whole FTE between
  iterations; each reviewer now draws from their own stream and each month's grants from a fixed quantile, so a cover
  change only adds or removes reviewers at the margin.
- The data dictionary, the file list, the operations notes and the warehouse notes (markdown): a file that describes the
  data is a leak (`dataset-generation` section 3); the conventions the asks and the chart need now sit in the operations
  handbook and the question count standard, and every export names its own columns.
- Annual netting at Databases and Infrastructure & DevOps 0.07 and 0.12 FTE from their bin edges, and the world's
  realised 2027 one bin lower at Data & ML (the 72-hour queue carries a short month's backlog into the next month's
  spare capacity): the three sites were re-centred slightly above their integers, and a day-by-day simulation of the
  hand-off on the forecast pool is asserted to file the same nine.
- Architecture 1 as a whole (2026-10-31, the batch 1 triage): the moderation pool's world, prompt and asks had been
  solved once on the portal and loop 3 kept them, so the slot is re-rooted in a new world with a new mechanism; the
  pool's leaving rate falling as fast leavers go first is spent for this slot.
- Re-root draw screens (2026-10-31), each rejected before any data was cut: a mixed-population flood frequency (spent
  in task273 and task130's notes); an event-driven trial's event count (task171 and task174 hold it); a dialysis
  cohort's eGFR slopes (a patient-level slope is the obvious route and the method forks); a vineyard's frost nights
  under inversions (dead in task170's notes); a health system's access change and a climate-extremes count (both
  measured dead in task174 and task170's notes); this slot's own frailty and tenure hazard (architecture 1).
- The first card probe for this draw carried `validated_decoy` true and Gap 1 first: BLOCKed on
  `two_layer.validated_decoy` (a closed record built to bless the wrong method) and on a structural signature spent in
  five builds. The design is drawn so the meter's own high-water-table storms and the overflow log refute one response
  per millimetre for anyone who checks them, and population (the meter's days are not the replay's) is the decisive gap.
- A June 2025 high river with storms in it (the spell centred in August): the meter logged three overflows in it that one
  response per millimetre misses, so the overflow log refuted the stop rung at the count level, a search signal; the spell
  now falls in a dry month of 2025 and the meter's logged overflows are dry-ground storms every rung reproduces.
- The spell's peak held below the replay's wettest days (12.6 km of sewer below the water table against 20): 812 replay
  days sat above anything the meter saw, so the deciding configuration was out of sample and the infiltration had to be
  extrapolated; the spell now reaches the replay's wettest days (one replay day above the meter's maximum).
- Pumps below the wet-winter base (92 to 100 L/s): the station spilled in dry weather on groundwater alone and the
  consent's 24-hour rule merged wet weeks into single long overflows, so more inflow could file fewer overflows and the
  count was not monotone in the flow; the pumps now sit above the wettest dry-weather peak and every overflow needs rain.
- Assumed unit hydrograph shapes and a crown or centreline reference for the submerged length: the replay spread 2.1 to
  5.0 a year, but only because those variants fit the meter two to three times worse; among fits within a few per cent of
  the best the figures agree inside the whole-number bin, so the figures are graded to whole overflows a year.
- Architecture 2 (the PS03 overflow replay with each day's own water table), returned FAILED_TO_STUMP on 2026-11-07:
  both responses landed the hold call. Response 1 replayed 2004 to 2023 and filed 48 overflows against the 40 the
  consent allows, then 2 after the upgrade; Response 2 filed the same hold. Any full-record replay with the subdivision
  already broke the consent, so the decisive step (each replay day's own water table) was never needed. Lesson: the easy
  route has to be the one strong solvers actually file, and it has to land on the wrong side; a count of rare
  exceedances spreads with every modelling choice, so the call now sits on a mean quantity whose naive family is tight.
- Judge round 1 (2026-11-07, FIX_NOW on the asks; the call forced, Gate G analytical_non_defect, Gate H pass). Ask A's
  window read literally dropped the platform councils' last run (a 2 July 2026 date in the period-end column): FP-04 now
  files the record's own convention (a pay period ends on a Sunday and is paid later that week; credited to the year it
  ends in), naming no platform and no weekday the advices carry. Ask B's unit was open (raw, per invitation and day, or
  per organiser, invitation and day): the asking sentence now files it (a visit two organisers made counts for both, a
  moved booking once as held). Both asks were scoped to the 30 councils the branch covers while the prompt read as the
  round: cut to the round's 24, the regional platform's twelve councils re-sited inside the round on the same pay
  cycles, so no in-round figure moved. Ask 1's turnout figures had no rounding and a refit evaluating members at the
  extract sat about 0.7 points under: the guide now files each member as they will stand when the ballot period closes
  and the tracker files that period (1 to 15 March 2027); whole-per-cent figures were not adopted because five councils
  sit within 0.05 of a half point (Corrigan Valley 62.53, Halston 59.53, Pellham 58.49, Rosedene 45.51, Underhill 40.54),
  so a worksite-effects refit (lift 1.027) can cross a rounding edge; the prompt asks only whether each council reaches
  half, the side being determinate under every refit. freeze.py: the main side unmoved; the twelve out-of-round ask
  figures and block 4's turnout percentages were dropped by the repair (allowed, this line).
- Hardening noted, not applied (the judge rated stump power moderate to good: a model that fits the delegate term lands
  the call): ship the 2026-28 term as the organising coordinator's separate July 2026 election return rather than a
  sheet of the delegate register, so the register a solver opens holds the terms the online votes cover and the new
  term sits in a file read for its own purpose; the call, the stump and every figure would stay frozen.
- Judge round 2 (2026-11-07): DETERMINISTIC, the call reproduced with 6 points either side and no respecification
  flipping a council, stump power moderate to high. Before ship: step 8 reworded (the golden keeps the later, last
  updated row of a moved booking); the xlsx inputs' creator and last-modified-by set to the branch, the body that
  issues them; the 2021 declarations given the Producer of the LibreOffice release current at their June 2021 export
  (7.1; the info dictionary is the last object, so startxref moves and every object offset is asserted unchanged), the
  other four PDFs dated after 24.2's February 2024 release; and the hardening above applied: the 2026-28 term now ships
  as `delegate_election_return_2026.xlsx`, the returning officer's return, and `delegate_register_2018-2026.xlsx` holds
  the terms to 2024-26. No graded figure moved (freeze.py); the input gates hold (17 files).
- Surface at ship promoted three pairs on card axes alone: task157 (back to back, the same domain and objective; a
  petition sample's pair defects, not a turnout forecast, differentiated on the card), task154 (the calibration form
  realised_outcome_roster repeated two builds apart: redrawn to counterparty_acknowledgement, the agent's declared
  results being a counterparty's record) and task265 (left truncation in a descriptive survival estimate,
  differentiated on the card); heart PASS; left for the author's adjudicated clone check.
- Architecture 3 (the union branch's protected action ballots, each member read with the delegate in post at the
  ballot): FAILED_TO_STUMP on the portal 2026-11-07, both responses on the golden 11 councils. Both put worksite
  delegate coverage in the turnout model from the start and evaluated it at the ballot close with the 2026-28
  delegates, so the decisive step was the forecaster's reflex (a recorded covariate's forward value), and the July
  2026 election return, read by nothing else, announced it. Re-rooted to architecture 4 in a new domain and world.
- Architecture 4 draw screens (2026-11-08), each rejected before any card or data: vacancy chains through a
  fixed-post hierarchy (dead in task174's and task137's notes, and a stock-and-flow check of posts finds it); a
  programme's lead-in audience (task115 and task174); one facility's overflow into a sibling removed by an expansion
  (task308's reader named railheading and the full car park's hidden demand, and the swap reads the same for wards
  or car parks); ward acquisitions per colonised patient-day (task181: infection prevention's own reflex); errors
  per interruption or per handover (task198 and task173); wear accrued only in hours inside a band after a duty
  change, and pump failures per start after a control change (task307's driver); admissions that rise with spare
  beds (a filed bed opening prompts the question, and the forecast needs a fixed point whose estimator forks);
  speculative double bookings (the hygiene battery's de-duplication reaches it and the identity match is Layer 1);
  bus headways under a denser timetable (task308's probe replayed the operation and carried every knock-on).
- First prototype of this draw (hangs on days since power-up, any site-wide power-down a reset): the parameters put
  every hub below 99 per cent; the legacy cabinet repairs now isolate the hub every few weeks, hangs start only after
  about 75 days, and the high-power units sit near 99.5 per cent on the record.
- Hang restarts isolating the whole hub: the units then restart one another and the programme hubs stay above 99 per
  cent; a hung unit is restarted at its own breaker, and only the legacy unit's cabinet repairs, planned visits and
  supply interruptions restart the whole hub.
- Three hubs whose legacy units rarely needed the cabinet opened, failing on both routes: the hubs' legacy repair
  counts then predict the high-power hangs across hubs, and a hub covariate (legacy units at the hub, or their
  repairs) would extrapolate to the golden, architecture 3's failure again; every hub now has exactly one legacy unit
  with cabinet repairs of 10 to 12.5 a year, and the hubs that fail on both routes are three coastal hubs whose
  high-power units suffer ordinary corrosion faults.
- The learner given the hub's legacy jobs in the last 60 days, the days since its last legacy job or the days since
  its last planned visit (prototype, clean truth): none reaches the golden; at the programme hubs they carry 0.7, a
  noisy 0 to 1.4 and 0.4 to 0.7 hangs a unit-year against about 3.3, so each files the default path's set.
- Prototype 7 (the RC50's cabinet repairs at random, 10 to 12.5 a year, every unit at a hub on one pillar): the
  hub-year count of the RC50's work orders predicts the HX150 hangs (z of minus 4.8), and the Poisson model carried at
  the programme's zero files the golden plus a rural spur hub; the count of pillar power-downs files the golden
  exactly. A covariate's forward value lands the call, architecture 3's failure again.
- Prototype 8 (motorway visits two-monthly only from April 2024, rural spurs at 4.5 interruptions a year): the
  full-covariate model filed the naive set with programme hubs 0.01 to 0.3 from 99, a coin flip per hub over redraws.
- Prototype 9 (the coastal hubs' HX150 units on their own pillar, the RC50's repairs still random): the model on the
  RC50's work orders alone still filed the golden exactly; the random repairs carry the signal however the pillars sit.
- Prototype 10, adopted: the RC50's cabinet service is monthly, so its work orders a year carry no hang signal (z of
  0.3) and the HX150 units on its pillar never run 75 days; the hubs whose HX150 units sit on a pillar of their own
  carry every hang on record. Two inland hubs share that arrangement with the three coastal ones, because a record in
  which only coastal units ever ran long could not tell the sea air from the uptime (the deciding configuration has to
  be on record off the coast).
- Ask screens refused: double counting on a meter shared by two connectors (a billing defect a real operator fixes, so
  planted); tariff re-rate copies with new session IDs (a near-duplicate the battery's de-duplication reaches); a hub
  code renumbering (the battery re-derives the code from the charge point); meter replacements to break a register
  shortcut for Ask B (each needs a work order in a main-call file, an ask organ there), so a solver who takes each
  unit's register advance over the window keeps Ask B.
- The first cut's register opened on its Charge points sheet: leak.py sweep 12 read the first two rows' cells (the
  units' IDs, makes and models, which the programme names) as column names and called the programme a dictionary
  (LEAK); the register now opens on its Hubs sheet, the order an asset team keeps it in, and no figure moved.
- The full-covariate model before the RC50's work rose with the coast (the RC50's repairs as random at every hub): it
  filed 11 of the 12 on the clean truth, because the hang hubs' RC50 jobs ran low by chance and the zero at the
  programme hubs extrapolated far below the record; the RC50s at the five own-pillar hubs now need about twice the
  repairs (the coastal units' corrosion, the inland pair's 2017 units), so its removal lowers that model's forecast.
- Stage 4 round 1 (2026-11-08, on 4bf9959c): the judge DETERMINISTIC (APPROVE), the leak reader clean on questions 1
  to 6 with one mild item (every HX150 freeze call-out on record at the five own-pillar hubs, read as placed). Worked
  in one generator pass, the lines below; the call, the stump and the twelve hubs unchanged.
- RC50 outages awaiting Tavrin parts in 2026, to give the shared-pillar units some long uptimes (a module on order for
  weeks, the RC50 out of service and its pillar live): the outage months carried a signal the full-covariate model
  read, and it filed 12 hubs with seven standard programme hubs among them; the outage path is empty, and the shared
  units' occasional long uptimes come from the RC50's inspection-only months (one in five, the cabinet not opened)
  and skipped services instead.
- RC50 cabinet repairs cut to 1.0 a year at the shared-pillar hubs (fewer isolations, more shared hangs on record):
  the shared units then hung often enough at a thirteenth hub to list it; the repairs stay at 3.5 a year there and
  6.8 at the five own-pillar hubs.
- The five own-pillar hubs' HX150 units commissioned in 2022 and 2023 like much of the fleet: the full-covariate model
  read the commissioning year (the hang hubs' units among the newest) and carried it to the programme's new units,
  filing standard programme hubs; their units are now commissioned in 2021.
- Callout attendance read from each Faulted spell's length: the RC50's long repair spells inflated it at the shared
  hubs and the verifier's own forecast sat 0.05 points from 99; attendance is read from the work orders (attended less
  logged) over every callout, in the golden and the verifier alike.
- The day-step members of the standing family counted a hang's first day whole and released it a day late (about a day
  of downtime too many a hang): they sat up to 0.7 points under the simulation (Annagh Cross 99.05 against 99.30), the
  verifier's copy too; both now count the part of each day a hang is down, from a hang at mid-day on average, and agree
  with the simulation within about 0.15.
- Ordinary faults at about 0.4 a unit-year everywhere, the standard hubs' callouts at 2.3 days, the rural spurs at 7.4
  and 7.9 interruptions a year and comms faults at 0.15 a unit-year: the hubs outside the list sat 0.22 to 0.4 points
  above 99 on the golden, two of 20 redraws filed another set, the rate route's back-tests drifted past half a point,
  and the standard hubs' 2026 faults at that attendance put four of them under 99 in the January to October 2026
  record, so carrying 2026 held four of the seven; faults now run about a quarter a unit-year outside the coast, the
  standard hubs' callouts about 2.05 days, the spurs about nine interruptions a year and comms faults a tenth a
  unit-year, every hub's true side at least 0.48 points from 99.
- The five own-pillar hubs at 3.4 to 4.1 charges a day (the quietest after the spurs): the full-covariate model leaned
  on charges a day and the hub's unit count (the standard hubs gain a unit in 2027) and filed 13 hubs, ten of the
  golden's; the five now take 4.8 to 5.6 charges a day, inside the standard hubs' range, and the model files 3.
- A rate-route back-test bound of 0.4 points: with comms repairs and faults at their real scatter a unit-year's own
  noise is about 0.4 points, so the bound is half a point with 85 per cent of units on their side, and the back-test
  prediction now carries the comms repairs' downtime as the rate route does.
- Load bank tests of about 55 kWh a connector with session drops of up to 18 minutes two and a half times a day: a
  column total (the gaps out, the tests in) cancelled to the golden figure at three hubs; tests now run about a
  quarter of an hour (30 to 40 kWh), drops three times a day for 6 to 15 minutes (inside the three missed heartbeats
  that write Offline), and the generator's clearance holds the gaps and the tests at least 0.16 MWh apart at every hub,
  the tests across a rounding step and no hub's charges on a round hundred.
- Work orders written from six to nine fixed sentences a job kind (one repeated 118 times) and planned jobs attended a
  whole number of days after logging: each write-up is now composed from the job's parts in its technician's habits
  (2,465 distinct over 3,546 jobs, none more than 9 times), planned jobs are logged at the planner's minute and
  attended at the technician's, and the parser's reading of every job's kind from its words is asserted against the
  truth.
- The plan's addressee typed rather than drawn (Bronagh Allis): now Ailis Fee from `guard.py names --geo ireland
  --seed 156`, the schedules signed by Darcy McGlinchey and Domhnall Linehan from the same draw.
- The prompt's question as "Which of our hubs will have..." (the which shell at 32 per cent of the prompts on file, and
  task482's form), then "Where will we have..." (the voice check and the heart read "will we" as whether): it now asks
  "Where in our network will a high-power charge point fall below...", read as where by both.
- "No forecast within 0.3 of 99" (the first hand-off's SF4 and closure line) was not what the build measured (0.21 to
  0.25 then): both now quote the measured margin, asserted at 0.2 or more.
- CRITICAL_COMPONENTS 1's hang count (84, which the judge read as 83 with a power-up before it on record and 90 in
  all): dropped, the onset day kept with its definition.
- The surface screen on the cached corpus (127 builds, 0 promoted at the first hand-off): the full re-extract screens
  314 and promotes 9 pairs on card axes or surface percentile, each differentiated on the card.
- The planned maintenance schedule writing 08:30 to 14:30 on every row while the world's visits ran in each
  contractor's own windows (the first fix pass varied the windows in the world, not in the schedule): the schedule now
  carries each hub's window for each year (motorway hubs early, rural spurs late, town centres before the shops open,
  moving with each year's plan), and Schedule 4's exclusions, the golden's and the verifier's, are read from it.
- Stage 4 round 2 (2026-11-08, on 3a6e329b): the leak reader clean, the judge DETERMINISTIC (APPROVE, no FIX_NOW). The
  ship pass worked the coordinator's fixes 1 to 7 in one generator pass; the call, the stump, the ladder and the default
  path unchanged. freeze.py's --allow, with its reasons: charges.Annagh Cross, energy_mwh.Annagh Cross,
  charges.Cloonfin Crossroads and energy_mwh.Cloonfin Crossroads (the spurs' interruption record raised by half, fix 5,
  which re-draws their 2026 sessions: 1738 to 1786 charges and 57.3 to 57.5 MWh, 2545 to 2507 and 81.9 to 81.0);
  pack.status_rows (the export cut at 31 October 24:00 and the spurs' extra power-downs), pack.dso_rows (the spurs'
  extra interruptions), pack.session_rows, pack.resent and pack.resent_hubs (the session numbering moves with the
  spurs' sessions, so the export's September re-sent page falls on other hubs; no other hub's records change),
  pack.wo_a and pack.wo_b (planned jobs raised by each contractor's own practice, the jobs open at the save, the spurs'
  callouts) and salt.NM125 (the clearance re-drew Annagh Cross's sessions once more).
- The status history ran past its stated coverage (rows to 8 November, from intervals that ended after 31 October) and
  the work orders held jobs attended and closed after the workbook's save: each export now ends at its own moment, a job
  raised before the save and not yet attended or closed stands open, and a spell still Offline when the record ends is
  censored rather than read as a hang (the golden and the verifier alike). The schedule's visits on 30 and 31 October
  stood Completed in a workbook saved on 29 October; a visit is Completed now only once its window closed before the save.
- Planned jobs raised 3 to 20 or 6 to 30 days ahead by both contractors (the same ceilings in two systems): Lissane's
  technician booked the next RC50 job on leaving the last one and its planner raised site visits in a batch the month
  before; Corran raises a site visit on the day the operator notifies the partnership and an RC50 job a fortnight ahead,
  about one in six then moved; the operator's notice runs from a fortnight to about six weeks. The jobs' write-ups are
  drawn in the order they always were, so every write-up outside the spurs' callouts stands as it did.
- The spurs at 7.3 and 9.4 interruptions a year: their lowest unit sat at 99.31 and 99.47 on the golden and 99.15 on the
  judge's own simulation, their expected lowest unit at 98.9 to 99.05 and their event probability at 0.41 to 0.48. The
  long rural overhead spurs now carry 42 and 54 interruptions on the record (about 11 and 14 a year): the extra faults
  are drawn on a stream of their own, so every other hub keeps its record, its sessions and its jobs (the spurs' old
  draws replayed where other hubs share a stream).
- The spurs' extra faults first drawn as a Poisson stream (4.6 and 4.9 a year): its draw moved the smoothed route to 9
  hubs (Cloonfin Crossroads in) and the rate route's back-tests to 0.42 and 0.43, figures the frozen ladder and default
  path state; the record now holds a stated count (14 and 18 beyond the base), and the stream is chosen, as the
  clearance chooses the asks' salts, so that the re-drawn spur record leaves every cheap route's set and the back-tests
  as they stand.
- The programme's document control table split across its page break (heading on page 1, rows on page 2): kept with its
  heading on page 2; no word changed.
- The PDFs' Creator (fix 4, optional): left as Writer. officepdf renders every document through LibreOffice Writer, so
  any other Creator would be contradicted by the file's own structure.
- The expected lowest unit, the event reading, each unit's own fault rate and a Weibull onset (the judge's optional
  items): asserted as SF17 to SF20, each on the same 12; the Weibull's fit is worse than the fitted onset's by 27.5 AIC.
- The RC50's 2027 isolations drawn as a Poisson stream at the hubs where it stays: they forecast 0.05 to 0.53 hangs a
  unit-year there against 0.00 to 0.39 on the record, which thins those hubs' expected-lowest-unit margins (Eskerbrook
  Shopping Centre at 99.07); drawn from the record's own calendar the member lists the same 12 at 99.23 and 0.32 at
  worst, measured and asserted, and the golden keeps the Poisson draw (no golden change).

- Architecture 4, the rapid-charging operator's 2027 availability plan (2026-11-08, platform round 1, target.zip
  5356713d): both runs landed the golden 12 hubs (the author reports not stumped; no rubric). Both read the hang ages
  off the first histogram (no hang before day 76 after a power-up), fitted a censored hazard on time since restart with
  the work orders' power cycles as the remedy, simulated the renewed network and back-tested on 2026: a mechanism the
  rows carry in one plot, with its remedy written in the work orders, was modelled on sight. Its asks fell (93,640 and
  94,297 charges against the golden's 90,612) but the platform rules a landed call before grading. World spent.
- Architecture 5 draw, a heat pump conversion programme's second phase forecast from homes that under-heated on gas and
  will heat fully on a heat pump (each home's uplift conditioned on its own pre-conversion balance point): rejected at
  the draw, because it is task3 architecture 1's driver in other nouns (the gain an upgrade adds conditioned on how much
  of each unit the old level already served), which one of that build's runs landed by regressing each earlier unit's
  gain on its own prior coverage; conditioning a carried gain on a covariate each unit's history prints is a reflex.
- Architecture 5 draw, a pilot of hybrid heat pumps whose gas backup flattened the cold-day electrical load carried to
  an all-electric second phase: rejected at the draw on the one-fact test (the pilot's units are hybrids), and the
  backup's discovery would be finding a population fact rather than analysing.
- Architecture 5 draw, stations whose winter peak responds in opposite directions to the gas-to-electricity price ratio
  (hybrids switching fuel, all-electric homes economising) carried to the 2027 energy tax shift: rejected at the draw,
  because a per-station forecast is the natural default, so each station's own slope is a reflex there (the grouping
  dichotomy), and the decision weights no population mix.
- Architecture 5 draw, measurement error in the heat pump count by substation (postcode allocation) attenuating the per
  heat pump coefficient: rejected at the draw, task4 architecture 5 carries an errors-in-variables driver in flight.
- Architecture 5 draw, phase imbalance (single-phase heat pumps landing on one phase, the transformer's per-phase limit
  binding first): rejected at the draw, because per-phase columns invite the per-phase reading and the installers'
  allocation is readable off the first phase's increments.
- Architecture 5 draw, latent excavation damage behind a spike in cable faults read as ageing: rejected at the draw, an
  activity elsewhere, linked by place and time, driving failures repeats architecture 4's family in this slot.
- Architecture 5 draw, export from PV-saturated feeders censored by inverter overvoltage trips: rejected at the draw, a
  trip is not a clean cap, and the capped-quantity family is crowded on this repository's cards (mark124, mark162,
  task4 architecture 2).
- Architecture 5 prototype, the partners' own design-day demand reconstructed by removing the moved sections as the
  deciding step: kept off the call, because removing a moved load from a series is cleaning; the partners' flags hold
  under every route by margin and the moved sections decide only their ask figures, while the call moves on what
  the credited flexibility is.
- Architecture 5 prototype, an unadjusted customer baseline (the mean of the ten previous non-event weekdays): measured
  0.33, minus 0.38 and 0.25 per megawatt scheduled at the three zones, its cold-day bias cancelling part of the moved
  section at one zone and turning another negative; it files a fourth primary (Charlecote Way) and misses, and its
  negative zone sends a run to the weather-adjusted baseline, which carries the whole moved section.
- Architecture 5 build, the pair estimate summing whatever half-hours either primary reported: a half-hour held or
  missing at one primary became a one-primary sum and dragged the pair's baseline (Hartwell Common 0.18 per MW against
  the netting's 0.39); the pair now sums only half-hours both primaries reported and reproduces the netting exactly.
- Architecture 5 build, the before-demand left to "assessed before any flexibility": excluding the event days and
  adding the measured fall back gave Ashcombe Road 26.0 and 26.7 MW after flexibility (two whole-MW cells), and keeping
  the event days dropped both committed primaries under firm; guideline 3 now names the days left out (SF3).
- Architecture 5 build, the growth register's "accepted offer" read without the energised: Fenwick Street moved from
  29 to 28 MW; guideline 4 now says the energised are included (SF5).
- Architecture 5 build, Fenwick Street's 14.0 MW contract: credited 6.75 and after 29.30 MW sat 0.25 and 0.20 from
  their whole-MW edges; the contract is 14.5 MW and both figures sit mid-bin.
- Architecture 5 build, an October to March SCADA export: October runs on British Summer Time, so a run reading the
  UTC stamps as local shifted October's half-hours and moved Fenwick Street's after figure; the export runs November to
  March (SF22).
- Architecture 5 build, the historian's first outage draw: two held stretches on Hartwell Common's 2024/25 evenings
  moved its delivery to 0.3 for a run that kept the S rows; the outage stream was redrawn (34) so every handling of the
  held values gives the golden's figures, and Ashcombe Road's first service starts on 27 November 2024 so no two zones
  or winters share an event count.
- Architecture 5 build, the dispatch log as the second large CSV: 379 rows, about seven printed pages; the weather file
  (13,372 rows, raw readings beside their checked versions, logger gaps) carries that gate.
- Architecture 5 build, nine primaries named in their keys' alphabetical order (Ashcombe, Brindle, Charlecote and on to
  Ingram), feeder streets repeated across primaries, every zone's contract up 0.5 MW a winter and growth references
  numbered after their acceptance: the stage 4 reader read each as templated; four primaries renamed (Tollbrook Lane,
  Ravenhurst Park, Wexley Hill, Kestwick Fields), one street per feeder, the winters' megawatts varied (Ashcombe Road
  5.0 then 6.5, Fenwick Street 5.5 then 6.5) and each reference numbered in its application year, every graded figure
  unchanged in its bin.
- Architecture 5 stage 4, the 2025/26 correction pooled over three winters with winter levels: the judge read guideline 3
  ("forecast from the primary's 2025/26 winter demand corrected to the design condition") literally and fitted 2025/26
  alone, which is the WHAT's literal execution; the golden now fits 2025/26 alone, and the pooled fit converges (SF4).
- Architecture 5 stage 4, Fenwick Street's 14.5 MW contract: a mean of the events within 1.5 or 2 C of minus 3.0 C
  (0.52 per MW) credited 8 MW and left 28; at 14.0 MW every one of 16 estimators lands on 7 and 29, and Ashcombe Road's
  contract moved to 9.5 MW with 0.25 MW more accepted growth (Fenwick Street 0.25 MW less) so every zone's estimator
  family sits inside one bin for delivery, credit and after (0.11 to 0.33 MW from the edges).
- Architecture 5 stage 4, a daily peak on a day the export cuts: under BST the last half-hours fall on 1 April local, and a
  one-reading "day" entered a 2025/26-only fit and moved Ashcombe Road by 1.5 MW; daily peaks and means now count only
  days with at least 44 half-hours and 20 hourly readings (SF1).
- Architecture 5 stage 4, the historian's export in UTC with events into the last days of March: the late-March weekdays
  are the mildest training days, so a run reading the UTC stamps as local moved every baseline by 0.1 MW and three zones'
  figures; the service now ends before British Summer Time, the export is on the UK clock as many historians write it,
  and Ashcombe Road's first and Hartwell Common's second service start later (28 November 2024, 10 November 2025) so no
  two zones or winters share an event count.
- Architecture 5 stage 4, "the control room moved a feeder section" in the answer blocks: no shipped file records a
  control-room action; the blocks now state the rise at the primary across the open point and cite guideline 6 for
  netting it (the judge's FIX_NOW).

- Architecture 5 platform round 1 (2026-11-08, triage FIX_ASKS; no rubric pasted, scores estimated at about 92 and 31,
  the author's estimate an average near 68): run 1 landed the golden with paired totals across the open points and
  the delivery read at minus 3.0 C, losing only the neighbour rises and the 0.9 contrast it never stated; run 2
  measured the neighbours' rise (1.271, 0.997 and 1.680 MW) and set it aside as not proving a transfer, filing
  Ashcombe Road alone on rung 1b (dismissed own evidence). Both read the design day, so the asks' designed second
  judgment (the design condition, the first cracker's rung 3) was spent by the guideline's and the prompt's own words.
- The per-zone answer items (Supplementary Questions 2 to 5, one per zone): run 2 collected Charlecote Way's whole row
  (0.5, 4, 21, No), because Charlecote Way has no transfer and every route that reads the design day agrees there, and
  the over-firm Yes at Ashcombe Road and No at Fenwick Street, which hold on both paths; replaced by one item per
  quantity across the four zones, the flags folded into the after item's set.
- The layout item (Supplementary Question 1) and the chart graded as present: format items both runs collect; the
  layout now rides inside the delivery item and the chart is graded on which after columns stand above firm.
- The step-by-step's upstream figures (each zone's completed events, the design-day demand before flexibility): both
  runs reproduced them (30, 25, 36 and 23 MW), so a criterion drawn from them is free; dropped from the blocks, the
  workbook still carries them.
- A colder-day ask at minus 4.5 C alone with each zone's demand after flexibility graded: Hartwell Common's figure sits
  0.07 MW from its edge across the estimator family, and a quadratic correction puts Fenwick Street and Charlecote Way
  on firm capacity there; the ask grades the sets at minus 4.5 and minus 6.0 C only, and winter 2023/24 rules the
  quadratic out (SF24).
- A threshold ask (the coldest daily mean each primary left on its flexibility can carry): Charlecote Way's sits
  0.03 C from its whole-degree edge under Theil-Sen; not asked.
- Asking each provider's delivery once, pooled across its zones, so that Charlecote Way's figures would ride Fenwick
  Street's: it sets one provider's two zones side by side, the contradiction run 2 never confronted (0.48 against
  0.74 per MW), and could hand the call to the run the stump held; the table stays per zone.
- The guideline's lead time (about eighteen months from a December 2026 commitment, which reaches June 2028)
  contradicted its own winter 2027/28; run 1 flagged it. Restated as energised by the end of the following October;
  no figure moved.
- The pair ceiling gated on the design's first cracker (the delivery averaged over the event days, 32.8 on the new
  asks): no platform run took that row, so it is not the worst honest landed run; the gated figure is now the landed
  run that reads the design day and misses the asks' own judgment (53.1), with the full includer's beside it.
- Stage 4 judge on the repaired asks (2026-11-09, pass 2, target.zip 203d2bf4; NOT_DETERMINISTIC, SEND_BACK, Gate G
  analytical_non_defect and Gate H pass, stump power strong; report determinism_check_report_pass2.md): the minus
  4.5 C set turned on Fenwick Street by 0.05 MW under the thread's own joint regression and fell 0.39 to 0.87 MW short
  under a quadratic correction or a delivery fitted on the 2025/26 events alone, so it is dropped and the colder-day
  ask keeps minus 6.0 C, which held under every variant the thread ran (Charlecote Way 0.35 to 0.70 MW over); the
  excess's rounding is now in the prompt's rounding sentence; three growth-register acceptances dated after the
  register's own save (late connections, outside the window, no figure moved) now fall before it.
- The same pass read guideline 6's "reduction in the primary's demand" as the primary's whole fall, the route read at
  minus 3.0 C that files Ashcombe Road alone (23.5 MW against 23.0), and found no filed sentence stating a transfer;
  two earlier passes and the run triage ruled that route out by "that its provider will deliver", "No other measure is
  credited" and the award notice's delivery measured on the provider's metered assets. The closing passage now names
  and rebuts that route; the judge's own closure ("load picked up elsewhere across open points is not credited")
  names the transfer the deep step finds and fails the fork-is-the-stump test, so the main call is left for the
  author's decision rather than pinned in a rubric repair.
