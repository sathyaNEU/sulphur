# task22: which of Brandvold Public Utilities' fourteen gas districts enter the 2027-2029 main replacement program, and where the 2027 meter changeouts go

Architecture 2, re-rooted 2026-11-12 (filed 2026-11-13 UTC) after architecture 1 (Delmont Power and Light's feeder
energy balance) was landed by both platform runs (`runs/arch1_triage.md`). New world, dataset and shell; the deciding
lessons are drawn from what those runs named and waved through, never from what they computed.

## Draw

Subdomain: Energy Systems & Utilities (gas distribution losses and the district gas balance; house task type
  distribution-losses-energy-balance; the client's nearest task types are load forecasting and grid reliability)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a reconciled table plus findings: each pressure district's monthly gas balance from October 2023 to
  September 2026, conformed from the systems that each see part of it (the regulator stations' correctors, the cycle
  reads, the meter register, the accounts, the damage reports, the utility's own use), with the findings on top: the
  districts whose leak loss crosses the main replacement program's line and the districts whose non-compensating
  meters the 2027 changeout replaces
Weight: measurement: the largest term of every district's balance (what its customers took at base conditions) is
  recorded by meters that register gas at its own temperature, over read periods that cut across the months, and for
  a few accounts not at all; the last two builds put their weight on attribution (task4 v13) and investigation
  (task9 v3)
Data-native sentence: nothing meters a district's leaks, so each district's leak loss is what is left after what its
  customers took, and that term is recorded by meters that register the gas at the temperature it has in the buried
  service, read on cycles that cut across the months, with a few accounts taking gas no meter records; the regulator
  stations see each district's gas day by day, the commercial correctors and the county soil station see the
  temperature the gas in the ground actually has, while the 2024-25 logger study and the 2019 consultant both tied
  that temperature to the airport's air in winters when air and soil moved together.
People: drawn with `guard.py names --geo us --seed 2208`: Marc Gilbert (the gas utility's engineering manager, who
  asks; not named in the prompt), Jocelyn Murray (the consultant who wrote the 2019 lost and unaccounted-for gas study).
Decision: before the Brandvold Utilities Commission adopts the 2027 capital budget in December 2026, the engineering
  manager files which of the fourteen pressure districts enter the 2027-2029 main replacement program (the program
  rules: a district enters when its leak loss in the twelve months ending September 30, 2026 exceeded 1.0 per cent of
  the gas delivered into it) and in which districts the 2027 changeout replaces the meters that do not correct for gas
  temperature (funded where they under-registered by more than 4.0 per cent of what they registered over the same
  twelve months), with what the changeouts already scheduled for 2027 will have replaced before the 2027-28 heating
  season; forward-facing (the programs and the season are 2027's).

Card: `.claude/skills/fingerprint/cards/task22.json`, architecture v2, checked at WARN against every card on file
(skeleton severity none against everything, the slot's lineage included). The WARNs, answered: the strategy risk
(grain_or_unit) is analysis, not a field read: every field read correctly still leaves the gas temperature to
estimate, the read periods to re-cut and the diversion to tell from absence; the chain-near WARN against task8 v19
(the same answer shape and weight) shares no lesson, mechanism or file role; the question form "which" is the
decision's own (which districts); record_algorithm_inversion on two live builds (task16 v3, task20 v3) is a supporting
lesson here (the cycle inverted on each district's daily sendout), not the one the call turns on; set_over_threshold
on four live builds is the honest form for a filed per-district line. Redrawn at filing: the organisation family (an
investor-owned gas company repeats task20 v3's utility in the window, so the utility is the city's own, as most
Minnesota gas towns' are), the forum (a committee repeats task9 and task20; the city's Utilities Commission is a
board), the stakeholder family and the memo (a Word memo repeats task9 and task20's set; the Commission gets a short
deck).

## Stump screen

Written at the draw, before the card was registered and before any code. Six candidates through the nine tests (1 off
the closed page, 2 not a reflex, 3 nothing filed, 4 clean data, 5 two records, 6 the waved-through assumption with
its precedent, 7 a plausible shallower story, 8 across the data, 9 worth the call). Magnitudes from the scratch
prototype (a Fargo-to-Alexandria climate, soil at 24 inches insulated by snow, residential use of 0.055 Mcf a day
plus 0.0105 per degree day below 60 F): the outdoor non-compensating meters under-registered 5.3 per cent of what
they registered in the twelve months to September 2026 on the soil, against 7.5 per cent on the airport's monthly
air temperature (in the snowless 2023-24 winter the two differ by 0.6); spreading each read evenly over its days
moved 0.3 to 0.8 per cent of a district's twelve-month use across the window's ends, degree-day weighting 0.0 to 0.2.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Non-compensating meters register gas at the temperature of the buried service, which follows the soil; in the deep-snow winter of 2025-26 the soil held near freezing while the air fell as far as in 2024-25, so the logger study's tie of gas temperature to the airport's air (validated on its own winter) and the 2019 consultant's monthly-mean method overstate the 2025-26 under-registration by about 2 points of the outdoor non-compensating volume, and indoor meters sit at basement temperature | gas temperature carried on the air as the study and the incumbent did (N04 a model's transfer named and left untested; L37 a check that cannot see the condition; L22 the incumbent's formula whose generating assumption the data contradict) | the commercial correctors' daily average gas temperatures through 2025-26 and the county soil station's 20 and 40 inch temperatures, daily, against the monthly reads | none | kept |
| Each read period's gas carried to calendar months on the district's own regulator-station daily sendout: spread evenly it moves gas across the September and October ends (heating starts in October) and across the winter months (student rentals empty over the break) | consumption between actual reads spread evenly by day (N20, both architecture 1 runs) | the regulator stations' daily corrector volumes against the cycle reads | 2 is partial in gas: degree-day weighting lands near the golden outside the college district | kept |
| The 2027 changeouts finish at the pace access allows (indoor meters need an appointment), about two thirds by the heating season in 2024 and 2025, not on the plan's October 31 date | planned works taken to happen in full on their dates (N22, architecture 1 run 1; N03) | the 2024-26 changeout work orders (planned and completed dates, by meter location) against the 2027 plan | none | kept |
| Accounts whose winter use collapsed are new snowbirds (absent November to April, normal summers) or bypassed meters (low in every month from the bypass on, the summer base load included) | every collapse read as diversion, or every one as absence (L26 a plausible shallower explanation that passes its own checks) | the summer months' reads and the same accounts' earlier winters, and the 2023-26 revenue protection cases | 5 is partial: the summer evidence is the same reads file at another season | kept as a fourth, supporting result |
| The regulator stations' corrector gaps and fixed-factor days rebuilt from the gate balance | R39 (both architecture 1 runs rebuilt a sub-meter's gaps from the upstream balance) | the city gate corrector | 2 | dropped as a trap; kept as an assembly result priced Right |
| Leak loss read from leak counts times the incumbent's emission factor per mile of main | none: the runs take the balance's residual by reflex (R40's kind) | the regulator stations against the reads | 2, 4 | dropped |

The three strongest are independent: no one sentence rescues two of them (the gas temperature, the daily shape and
the past pace each name their own record), and the fourth is graded on its own evidence.

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
- 2026-11-12, runs: architecture 1 (the feeder energy balance and the four-feeder sweep) landed on both platform runs:
  both replayed the switching log with pole-tag matching, rebuilt the breaker gaps from the delivery point, computed
  hourly I2R on the GIS at current loads, measured the new loads on interval analogs and recomputed the lights from the
  inventory, every one a judgment the effort test had priced lost (paper 20.8 against about the thorough column); each
  move's data were complete, labelled and the field's textbook input. Architecture spent with its world; re-rooted to
  architecture 2 on what both runs named and waved through (`runs/arch1_triage.md`).
