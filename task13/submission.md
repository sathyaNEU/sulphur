## Tags

**Domain:** Engineering and Physical Sciences, Energy Systems & Utilities, grid reliability and outage analysis (automatic fault location, isolation and service restoration on the automated distribution loops).
**Analytical objective:** Anomaly Detection & Diagnostics.

## Final Recommendation

**Replace the batteries in 16 recloser controls before December. Before June, move the receiving reclosers on the 16 transfer directions the ADMS does not switch to settings that carry a transfer, without waiting for the four reinforcements. Run as they stand, the loops should avoid about 24,679 sustained customer interruptions in 2027 (80 per cent range 17,912 to 31,580); from January to October 2026 they avoided 21,328 on the commission's definition.** The careful but hurried reading misses each of these:
- it re-batteries on last winter's tests (2 controls);
- it takes the reinforcements on their planned dates and the past summers as the coming one;
- it forecasts 28,729, because it prices each restoration at its own loop and misses the receiving reclosers' trips.

## Supplementary Questions

### flisr_review_2026.xlsx

1. Sheet "Restorations by year", one row per year: customers the automation restored within five minutes of the first loss of supply. The figures are 2022 32,875; 2023 25,796; 2024 28,781; 2025 22,561; 2026 (January to October) 25,056, each within 2 per cent. Beside each year the sheet gives the loop lockouts, the customers restored after five minutes and the lockouts the event archive does not hold.
2. Sheet "2026 avoided": 21,328 customer interruptions avoided from January to October 2026 on order paragraph 2's definition, within 2.5 per cent. It is reached from the 25,056 restored within five minutes:
   - less 2,407 restored customers that a receiving recloser's trip then put out again;
   - less 1,321 of the receiving feeders' own customers that those trips put out;
   - less 0 from closes onto a fault.
   A bar chart sits beside it, and sheet "Operations 2026" lists each 2026 lockout on an in-service loop with what the scheme did.
3. Sheet "Batteries", one row per recloser control. Each row gives the battery's installed date, its age at 28 February 2027, its load tests, its coldest test and the volts it would hold under the 30 A operation at -27 C. Replace: RCL-20149, RCL-20188, RCL-20205, RCL-20275, RCL-20355, RCL-20466, RCL-20536, RCL-20542, RCL-20547, RCL-20732, RCL-20977, RCL-21316, RCL-21357, RCL-21377, RCL-21643 and RCL-21710. RCL-20188 and RCL-21643 sit within 0.1 V below the 21.2 V line and RCL-21281 within 0.1 V above it, so a list holding the other 14 with or without any of those three is right.
4. Sheet "2027 forecast", one row per loop feeder: lockout rates, the customers each transfer restores, and which loop stands in supervised mode. The total: 24,679 customer interruptions avoided in 2027 if the loops run as they stand (23,712 to 25,405 across defensible replays), 80 per cent range 17,912 to 31,580.

### flisr_2026_memo.pdf

5. One page for the filing, leading with the two changes:
   - the 16 controls to re-battery before December, and why the line-powered functional tests pass them;
   - the receiving settings to change before June on all 16 unswitched directions. Left as they stand, transfers from June to September 2027 (the design basis's summer) would interrupt about 388 of the receiving feeders' own customers (318 to 455). Comparable completed projects ran a median 3.9 months late (4.5 for the reconductoring projects alone), so none of the four reinforcements has better than a 0.23 chance of being in service by 1 June;
   - then 2026 on the commission's definition with its working, and the 2027 forecast.

## Critical Components

1. **16** recloser controls' batteries (14 to 17 with the three at the 21.2 V line), led by RCL-21316, RCL-20466 and RCL-20542, would not carry a trip or close at -27 C by the end of February 2027, though every one passed its line-powered functional test.
2. The receiving reclosers on transfer directions the ADMS leaves in their normal settings tripped after transfers in 2026, with no fault found. That undid **2,407** restorations and put out **1,321** receiving customers, so 2026 avoided **21,328**.
3. Run as they stand, the loops avoid about **24,679** customer interruptions in 2027 (80 per cent range **17,912 to 31,580**). Without the transfer trips it would be 27,476.
4. The lockouts the event archive does not hold fell in its storm overflows, and none of them was restored within five minutes. The 2026 count within five minutes is **25,056**, where the archive with its gaps filled at its own rate gives 27,654.

## Step-by-Step

1. Rebuilt every lockout on an in-service loop from the device events in `scada_device_events_2022-2026.csv`, read on Central Standard Time: 405 lockouts from 2022 to 2026. Matched each lockout to the ADMS closes that followed it, timed from the lockout device's first trip, the five minutes of order paragraph 3.
2. Read `adms_flisr_event_archive_2022-2026.csv` in UTC under both message formats, through the register's tag crosswalk, and dropped the standby server's echoes. 35 of the lockouts are not in the archive. All fall inside the event-archive overflows the incident log records, and the device events show the front end closing those ties only after five minutes. Filling them at the archive's own success rate gives 27,654 for 2026; counting what the devices did gives 25,056 (row 1 for every year). The vendor dashboard counts completed sequences in the archive whatever their duration.
3. Found what the transfers did to the receiving feeders. The receiving reclosers that tripped while a transfer was in place, at little more than their group 1 pickup, are recorded in `oms_outage_events_2022-2026.csv` as no cause found. Every one is on a direction whose receiving controls the ADMS never moves to group 2 (CTL-4C in `da_device_register_2026.xlsx`). Operators switching the same transfers set group 2 first and never tripped one. Order paragraph 2 counts what customers had against what they would have had, so it nets 2,407 restorations undone and 1,321 receiving customers put out: 21,328.
4. Fitted each control's battery on its weekly load tests at 5 A against the airport temperature of the test hour (`kmkt_hourly_weather_2022-2026.csv`) and the battery's age. The batteries age at their own rates (0.13 to 0.44 a year in log resistance, each known to about 0.013), so one fleet fit or one per control type does not hold. Fitted to October 2025, such fits miss last winter's tests below -15 C by 0.52 to 0.64 V at 30 A, against 0.12 V for each battery's own fit, and they name 0 to 8 controls. Carried to -27 C at 28 February 2027 under the 30 A draw in `da_design_basis_rev3.pdf`: 16 fall below 21.2 V. Judging each battery at last winter's coldest test names 2; the maintenance book's failures, alarms and four-year cycle name 27; the age rule alone names 11. The functional tests pass every control because they run on line power.
5. Replayed each unswitched direction's transfers on the 2025 and 2026 hourly amps (`scada_hourly_amps_2025-2026.csv`) for June to September, the summer of `da_design_basis_rev3.pdf`. The replay starts at the months and hours the loops' lockouts struck and runs through the record's repair durations. It adds the approved 2.2 MW load from `large_load_requests_2026-2027.xlsx`. Transfers from June to September 2027 would put out about 388 receiving customers. The 2025-26 summers' average gives 582, and the plan's in-service dates give 237. The 40 comparable completed projects in `distribution_capital_works_2019-2027.xlsx` ran a median 3.9 months late.
6. Forecast 2027 at the record's average lockout rate since 1 January 2022 (order paragraph 5), using the scheme's own success rate with the storm losses restored. It keeps the loop now in supervised mode at its slow restorations, carries each control's chance of failing in the cold, and nets the transfer trips with the reinforcements at their likely dates: 24,679, 80 per cent range 17,912 to 31,580. The archive's rate with no netting and the plan's dates gives 28,729.

No other conclusion survives the files. A passed functional test cannot see cold cranking, and last winter's tests are not this winter's batteries. A reinforcement taken on its planned date ignores how this utility's projects actually finish. Pricing a restoration at its own loop leaves out the receiving feeder the order counts. A gap-filled archive assumes the lost sequences went like the kept ones, and the device record shows they did not.
