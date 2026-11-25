## Tags

**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, energy efficiency and demand response evaluation (a one-way air-conditioner load control fleet's 2026 dispatch trial).
**Analytical objective:** Experiment & Causal Analysis.

## Final Recommendation

**Fund the Kettle Ridge VHF repeater, the Larkin find-and-fix round and the reconnection round within 14 km; do not fund the Halverson carrier fill-in site, the Medora Flats find-and-fix round or the outlying reconnection round.** Read as they stand, the cooperative's own records (a coverage map that covers every premise, a test log that passes 96 in 100 switches, work orders that find 9 in 100 unwired after a new unit) fund none of the six: they put the Kettle Ridge VHF repeater at 0 kW, the Larkin find-and-fix round at 58 and the reconnection round within 14 km at 260, against break-evens of 185, 280 and 509 kW.

## Supplementary Questions

### load_management_proposals_2027.csv
One row per proposal in the work plan's order, with the kW it adds at the 2027 coincident peak (and its band), its break-even kW, its annual cost and whether it is funded.
1. The peak kW each proposal adds in 2027, against its break-even:
   a. Kettle Ridge VHF repeater: 250 kW (band 231 to 262), break-even 185 kW, funded.
   b. Halverson carrier fill-in site: 185 kW (band 150 to 207), break-even 280 kW, not funded.
   c. Larkin find-and-fix round: 505 kW (band 385 to 640), break-even 280 kW, funded.
   d. Medora Flats find-and-fix round: 264 kW (band 200 to 350), break-even 401 kW, not funded.
   e. Reconnection round within 14 km: 1,402 kW (band 1,252 to 1,552), break-even 509 kW, funded.
   f. Outlying reconnection round: 224 kW (band 195 to 253), break-even 345 kW, not funded.

### load_management_trial_2026.xlsx
The call on the first sheet, then the step record, the fitted model, the bridge, the proposals in full, the routes each record gives taken as it stands, and the rebuilds.
2. How the kW the switches could take off at peak splits, at the coincident-peak index with every listed transmitter on the air (the 2027 footing):
   a. Lost to commands not received: 1,775 kW (band 1,480 to 2,210).
   b. Lost to switches that received the command and failed: 2,396 kW (band 1,750 to 3,300).
   c. Lost to working switches not connected to the air conditioner: 1,626 kW (band 1,451 to 1,787).
3. The funded plan: 2,157 kW added at the coincident peak (band 1,990 to 2,330), at USD 39.7 a kW-year (band 36.5 to 43.0).

### load_management_2027_board.pptx
Three slides: the call, the bridge as a waterfall, and each proposal's kW beside its break-even.

## Critical Components

1. Shed commands that get through at the fringe (switches more than 20 km from the nearest transmitter serving them), against switches within 8 km: **17 in 100** (band **10 to 22**).
2. Switches installed through 2015 that still work, at premises with no replaced unit: **67 in 100** (band **60 to 72**).
3. Switches still wired in where the air conditioner was replaced after the switch went in: **32 in 100** (band **27 to 41**).

## Step-by-Step

1. Assembled the trial: 11,923 active A/C switches on `lm_switch_register.csv`; 60 event days and 476 group shed commands in `paging_encoder_log_2026.csv` (local time, each group's first transmit, the encoder's repeats dropped); `scada_feeder_1min_2026.csv` read in UTC, mapped to feeders through `scada_point_list.csv` (two Pruett points renamed mid-July), duplicate rows dropped and held readings (three or more equal readings in a row) left out. Each feeder's step at each command is the mean of the five minutes from the transmit minute less the mean of the five before: 21,896 steps.
2. Set the footing: a working switch near a transmitter takes off 0.802 kW at index 1, the mean of the study homes that respond (a home responds when its mean response over its shed days is above 0.25 kW; 90 in 100 of the 380 do), each home's response read from `study_meters_hourly_2026.csv` against the same day's held-out homes in `study_event_assignments_2026.csv`; at the Appraisal's index of 1.15 the switches could take off 10,997 kW, and the steps hold 5,200 kW delivered.
3. Rejected the records read as they stand: they explain 799 kW of a 5,797 kW shortfall and fund nothing (the Kettle Ridge VHF repeater 0 kW, the Larkin find-and-fix round 58, the reconnection round within 14 km 260). Rejected the study homes carried to the fleet (0.728 kW an enrolled switch): it puts 9,981 kW on feeders whose steps hold 5,200, and funds nothing; the study homes are all within 8 km, installed in 2019 and 2020, with no unit replaced since.
4. Rebuilt each switch's reach on each event day: the distance to the nearest transmitter of its own paging system (the register's receiver field) that was on the air, from `paging_transmitters.xlsx` and `radio_shop_outage_log_2026.xlsx`; then apportioned the steps among the switches each command addressed by reach band, install batch, district and replaced unit together. Reception relative to the switches within 8 km is 0.93 at 8 to 14 km, 0.64 at 14 to 20 km and 0.17 beyond 20 km: 17 in 100 commands get through at the fringe. Reach to the nearest listed transmitter of either system instead puts the Kettle Ridge VHF repeater at 7 kW, because the western VHF fringe sits beside the carrier's Sandhill site, which those receivers do not hear.
5. Read the hardware off the batches: the paging groups are install batches, so each group's own steps net of reach and replaced units give its delivery against the study homes' working level: 67 in 100 of the switches installed through 2015 still work (the test log's bench signal passes 96 in 100).
6. Built the replaced-unit list: a rebate in `hvac_rebates_2012_2026.csv` (by premise number, pre-2021 numbers through the register's old-number field) or a permit in `county_mechanical_permits_2010_2026.csv` (by normalised address) for a replacement central air conditioner or heat pump, dated after the switch was installed: 4,506 switches. In the same fit 32 in 100 of them still deliver (the work orders' chance finding is 9 in 100 unwired).
7. Checked the fit against steps it was not built to match: on the steps where a transmitter change moved a switch's band, the four oldest batches and the quarter of feeders with most replaced units, the largest gap between predicted and recorded steps is 0.053; each record read as it stands leaves 0.386 to 0.760, the either-system reach 0.317 and the study homes carried to the fleet 1.873.
8. Carried the fit to 2027 on the Appraisal's footing (every listed transmitter on the air, index 1.15, each proposal alone): the premises in scope are 1,578 (Larkin round), 1,242 (Medora Flats round), 3,267 (within 14 km) and 1,239 (outlying); a find-and-fix round's new switch is credited with what a working switch near a transmitter takes off, and a reconnected one with its batch's level; each break-even is the annual cost over USD 88 a kW-year. The Kettle Ridge VHF repeater, the Larkin find-and-fix round and the reconnection round within 14 km clear theirs.
9. Totalled the plan: 2,157 kW for USD 85,675 a year, USD 39.7 a kW-year; the bridge closes on 5,200 kW delivered of 10,997.

No other set survives. The study homes hold none of the three conditions, and the records each measure something shallower than delivery on a peak afternoon. All 78 rebuilds of the fit's conventions (band edges, weighting, the district and batch terms, halves of the event days, the responder cut, trimmed steps, the step window from three to ten minutes either side, the index origin) file the same three. Each step left out alone moves a different proposal: without the reach rebuild the set is the Larkin find-and-fix round, the reconnection round within 14 km and the outlying reconnection round (the Kettle Ridge VHF repeater falls to 0 kW); without the batch reading it is the Kettle Ridge VHF repeater and the reconnection round within 14 km (the Larkin find-and-fix round falls to 58 kW); without the replaced-unit list it is the Kettle Ridge VHF repeater and the Larkin find-and-fix round (the reconnection round within 14 km falls to 187 kW). With the reach rebuild and the batch reading both left out the set is the reconnection round within 14 km and the outlying reconnection round; with the reach rebuild and the list, the Larkin find-and-fix round; with the batch reading and the list, the Kettle Ridge VHF repeater; with all three, none. Each share holds its value in every row where its own step is kept. The thinnest margin is the Medora Flats find-and-fix round: 350 kW at the top of its band against a break-even of 401.
