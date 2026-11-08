## Tags

**Domain:** Energy Systems & Utilities (load, price & renewable forecasting: distribution network design-day peak demand).  
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Commit reinforcement at Ashcombe Road and Hartwell Common for winter 2027/28; Charlecote Way and Fenwick Street hold firm capacity with the flexibility contracted for that winter.** Credited at what Corvane Flex delivers on the design day, 0.4 per megawatt scheduled, the 2027/28 flexibility leaves Ashcombe Road at 26 MW against 23.0 MW firm and Hartwell Common at 20 MW against 17.8 MW; the 0.9 per megawatt their event records show counts the demand that rose at Tollbrook Lane and Kestwick Fields, across their 11 kV open points, in the same half-hours, and on that figure no primary would be reinforced.

## Supplementary Questions

### halverton_primary_capacity_2027-28.xlsx

1. A Zones sheet with one row per flexibility zone, in the order Ashcombe Road CMZ, Charlecote Way CMZ, Fenwick Street CMZ, Hartwell Common CMZ, giving the zone, its primary and asset code, the provider, the megawatts contracted for 2027/28, the provider's delivery per megawatt scheduled on the design day (one decimal), the flexibility credited (whole MW), the primary's design-day demand before and after the credited flexibility (whole MW), its firm capacity and whether the demand after flexibility exceeds it.
2. Ashcombe Road CMZ: delivery 0.4 per MW scheduled; 4 MW credited on the 9.5 MW contracted; design-day demand after flexibility 26 MW against 23.0 MW firm; over firm capacity: Yes.
3. Charlecote Way CMZ: delivery 0.5 per MW scheduled; 4 MW credited on the 8.0 MW contracted; design-day demand after flexibility 21 MW against 22.5 MW firm; over firm capacity: No.
4. Fenwick Street CMZ: delivery 0.5 per MW scheduled; 7 MW credited on the 14.0 MW contracted; design-day demand after flexibility 29 MW against 30.5 MW firm; over firm capacity: No.
5. Hartwell Common CMZ: delivery 0.4 per MW scheduled; 3 MW credited on the 7.5 MW contracted; design-day demand after flexibility 20 MW against 17.8 MW firm; over firm capacity: Yes.
6. A clustered column chart below the table: for each zone primary, its design-day demand before and after the credited flexibility beside its firm capacity, in MW.

### capex_review_2027-28.pptx

7. Slides for the capital expenditure review that name Ashcombe Road and Hartwell Common as the primaries to reinforce for winter 2027/28, state that Charlecote Way and Fenwick Street hold firm capacity with their contracted flexibility, and carry the same chart of demand against firm capacity.

## Critical Components

1. On the flexibility events at Ashcombe Road, Fenwick Street and Hartwell Common, the primary across an 11 kV open point from each (Tollbrook Lane, Wexley Hill, Kestwick Fields) rose in the half-hours ending 17:30 and 18:00 by **1.4**, **1.4** and **0.8 MW** on average as the zone primary fell, which is not a reduction its provider delivers (section 6 of the guideline), so it is netted from the zone's fall; no neighbour of Charlecote Way rose.
2. Net of those rises the providers' own reduction falls as the day gets colder; at the design day's minus 3.0 C Corvane Flex delivers **0.4** and Quillon Energy Services **0.5** per MW scheduled, not the **0.9** per MW the event records show at Ashcombe Road, Fenwick Street and Hartwell Common.
3. On the 2027/28 contracts the flexibility credits **4**, **4**, **7** and **3 MW**, leaving Ashcombe Road at **26 MW** against 23.0 MW firm and Hartwell Common at **20 MW** against 17.8 MW.
4. Charlecote Way (**21 MW**, firm 22.5 MW) and Fenwick Street (**29 MW**, firm 30.5 MW) stay within firm capacity after their credited flexibility.

## Step-by-Step

1. Mapped both SCADA point names in primary_demand_halfhourly_2023-2026.csv to asset codes through primary_substation_register.xlsx, kept each quality G half-hour once and read its end in UK local time.
2. Kept the latest revision of each instruction in flexibility_events_2024-2026.csv: 90 completed events at Ashcombe Road, 58 at Charlecote Way, 82 at Fenwick Street and 91 at Hartwell Common.
3. Corrected each zone primary's daily peak on working weekdays outside 24 December to 2 January and outside its scheduled days to the design condition (winter levels and one slope below 15.5 C on the daily means of halverton_weather_hourly_2023-2026.csv, the station's checked reading for each hour) and grew it by the DFES rates and the qualifying connections in load_growth_register_2026-27.xlsx: design-day demand before flexibility 30, 25, 36 and 23 MW at Ashcombe Road, Charlecote Way, Fenwick Street and Hartwell Common.
4. Measured each event's fall at the zone primary in the half-hours ending 17:30 and 18:00 against a weather-adjusted baseline fitted on its other working weekdays: 0.9 per MW scheduled at Ashcombe Road, 0.9 at Fenwick Street, 0.9 at Hartwell Common and 0.6 at Charlecote Way; carried to the 2027/28 contracts, that keeps all four primaries within firm capacity and commits none (the shallow route).
5. Read the same half-hours at every primary each zone's open points reach in network_feeders_11kv.xlsx, on a baseline fitted without the zone's event days: Tollbrook Lane rose 1.4 MW on Ashcombe Road's events, Wexley Hill 1.4 MW on Fenwick Street's and Kestwick Fields 0.8 MW on Hartwell Common's, while no neighbour of Charlecote Way rose, so each of those zones' fall includes demand that rose across the open point, which section 6 of the guideline does not credit to the provider.
6. Netted each linked primary's rise from the zone's fall event by event and regressed the provider's reduction per MW scheduled on the event day's daily mean temperature: 0.4 per MW for Corvane Flex at Ashcombe Road, 0.4 at Hartwell Common, 0.5 for Quillon Energy Services at Charlecote Way and 0.5 at Fenwick Street at minus 3.0 C, inside the event days' own range of minus 5.8 to 6.2 C (0.6, 0.6, 0.6 and 0.6 on the average event day).
7. Credited those on the megawatts in flexibility_contract_awards_2027-28.pdf and compared with Appendix A of capacity_assessment_guideline_2026.pdf: Ashcombe Road 26 MW against 23.0 and Hartwell Common 20 MW against 17.8 exceed firm capacity; Charlecote Way 21 against 22.5 and Fenwick Street 29 against 30.5 do not.

No other conclusion survives the files. The zone primary's own fall, against a weather-adjusted baseline or the ten previous weekdays, counts the demand that rose at the neighbour, and the ten-day baseline also sits below the cold event days it is set against, so it files all four primaries; taking the linked primary as the control adds that rise twice (1.0 per MW at Ashcombe Road) and files none. The zone and its linked primary taken together give the netting's provider reduction exactly (0.4 per MW at minus 3.0 C at Ashcombe Road). Crediting the providers at the average event day rather than at the design day keeps the same two primaries over firm capacity but credits 6, 5, 9 and 5 MW, which is not the reduction section 6 of the guideline credits; on the design day's credit, Ashcombe Road and Hartwell Common need reinforcement.
