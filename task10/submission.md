## Tags

**Domain:** Energy Systems & Utilities (load, price & renewable forecasting: distribution network design-day peak demand).  
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Commit reinforcement at Ashcombe Road and Hartwell Common for winter 2027/28; Charlecote Way and Fenwick Street hold firm capacity with the flexibility contracted for that winter.** Credited at what Corvane Flex delivers on the design day, 0.4 per megawatt scheduled, the 2027/28 flexibility leaves Ashcombe Road at 26 MW against 23.0 MW firm and Hartwell Common at 20 MW against 17.8 MW; the 0.9 per megawatt their event records show counts the demand that rose at Tollbrook Lane and Kestwick Fields, across their 11 kV open points, in the same half-hours, and on that figure no primary would be reinforced.

## Supplementary Questions

### halverton_primary_capacity_2027-28.xlsx

1. A Zones sheet with one row per flexibility zone, in the order Ashcombe Road CMZ, Charlecote Way CMZ, Fenwick Street CMZ, Hartwell Common CMZ, giving the zone, its primary and asset code, the provider and the megawatts contracted for 2027/28, then the provider's delivery per megawatt scheduled on the design day: 0.4 at Ashcombe Road, 0.5 at Charlecote Way, 0.5 at Fenwick Street and 0.4 at Hartwell Common (Corvane Flex 0.4 at both its zones, Quillon Energy Services 0.5 at both of its).
2. The megawatts credited to each primary on its 2027/28 contract: 4 MW at Ashcombe Road, 4 at Charlecote Way, 7 at Fenwick Street and 3 at Hartwell Common.
3. Each primary's design-day demand after the credited flexibility against its firm capacity: Ashcombe Road 26 MW against 23.0 MW; Charlecote Way 21 MW against 22.5 MW; Fenwick Street 29 MW against 30.5 MW; Hartwell Common 20 MW against 17.8 MW, so Ashcombe Road and Hartwell Common exceed firm capacity and Charlecote Way and Fenwick Street do not.
4. A clustered column chart below the table: for each zone primary, its design-day demand before and after the credited flexibility beside its firm capacity, in MW, the after-flexibility column standing above firm capacity at Ashcombe Road and Hartwell Common and below it at Charlecote Way and Fenwick Street.
5. How far each primary to reinforce exceeds firm capacity on the design day: Ashcombe Road by 3 MW and Hartwell Common by 2 MW.
6. The primaries whose demand after their flexibility would exceed firm capacity on a working weekday of winter 2027/28 at a daily mean of minus 6.0 C: all four.

### capex_review_2027-28.pptx

7. Slides for the capital expenditure review that name Ashcombe Road and Hartwell Common as the primaries to reinforce for winter 2027/28, state that Charlecote Way and Fenwick Street hold firm capacity on the design day with their contracted flexibility, and carry the same chart of demand against firm capacity.

## Critical Components

1. On the flexibility events at Ashcombe Road, Fenwick Street and Hartwell Common, the primary across an 11 kV open point from each (Tollbrook Lane, Wexley Hill, Kestwick Fields) rose in the half-hours ending 17:30 and 18:00 by **1.4**, **1.4** and **0.8 MW** on average as the zone primary fell, which is not a reduction its provider delivers (section 6 of the guideline), so it is netted from the zone's fall; no neighbour of Charlecote Way rose.
2. Net of those rises the providers' own reduction falls as the day gets colder; at the design day's minus 3.0 C Corvane Flex delivers **0.4** and Quillon Energy Services **0.5** per MW scheduled, not the **0.9** per MW the event records show at Ashcombe Road, Fenwick Street and Hartwell Common.
3. On the 2027/28 contracts the flexibility credits **4**, **4**, **7** and **3 MW**, leaving Ashcombe Road at **26 MW** against 23.0 MW firm and Hartwell Common at **20 MW** against 17.8 MW.
4. Charlecote Way (**21 MW**, firm 22.5 MW) and Fenwick Street (**29 MW**, firm 30.5 MW) stay within firm capacity after their credited flexibility.

## Step-by-Step

1. Mapped both SCADA point names in primary_demand_halfhourly_2023-2026.csv to asset codes through primary_substation_register.xlsx, kept each quality G half-hour once and read its end in UK local time.
2. Kept the latest revision of each instruction in flexibility_events_2024-2026.csv, a cancelled one at 0.0 MW, and each hour of halverton_weather_hourly_2023-2026.csv at its checked reading, averaged over the GMT day.
3. Corrected each zone primary's 2025/26 daily peaks on working weekdays outside 24 December to 2 January and outside its scheduled days to the design condition (a level and one slope below 15.5 C) and grew the result by the DFES rates and the qualifying connections in load_growth_register_2026-27.xlsx (guideline sections 3 and 4).
4. Measured each event's fall at the zone primary in the half-hours ending 17:30 and 18:00 against a weather-adjusted baseline fitted on its other working weekdays: 0.9 per MW scheduled at Ashcombe Road, 0.9 at Fenwick Street, 0.9 at Hartwell Common and 0.6 at Charlecote Way; carried to the 2027/28 contracts, that keeps all four primaries within firm capacity and commits none (the shallow route).
5. Read the same half-hours at every primary each zone's open points reach in network_feeders_11kv.xlsx, on a baseline fitted without the zone's event days: Tollbrook Lane rose 1.4 MW on Ashcombe Road's events, Wexley Hill 1.4 MW on Fenwick Street's and Kestwick Fields 0.8 MW on Hartwell Common's, while no neighbour of Charlecote Way rose, so each of those zones' fall includes demand that rose across the open point, which section 6 of the guideline does not credit to the provider.
6. Netted each linked primary's rise from the zone's fall event by event and regressed the provider's reduction per MW scheduled on the event day's daily mean temperature: 0.4 per MW for Corvane Flex at Ashcombe Road, 0.4 at Hartwell Common, 0.5 for Quillon Energy Services at Charlecote Way and 0.5 at Fenwick Street at minus 3.0 C, inside the event days' own range of minus 5.8 to 6.2 C (0.6, 0.6, 0.6 and 0.6 on the average event day).
7. Credited those on the megawatts in flexibility_contract_awards_2027-28.pdf and compared with Appendix A of capacity_assessment_guideline_2026.pdf: Ashcombe Road at 26 MW against 23.0 exceeds firm capacity by 3 MW and Hartwell Common at 20 MW against 17.8 by 2 MW; Charlecote Way at 21 against 22.5 and Fenwick Street at 29 against 30.5 hold.
8. Checked the correction's straight-line form on winter 2023/24, which ran no flexibility: fitted on its working weekdays as mild as the 2025/26 days the correction uses, it meets that winter's sub-zero working weekdays within 0.2 MW on average at every zone primary, closer than a quadratic at each.
9. Read the same correction and the same provider regressions at a daily mean of minus 6.0 C: each provider delivers less per MW scheduled on the colder day while the demand rises, so all four exceed firm capacity; carrying the design day's credit to that day instead leaves Charlecote Way within it, and the zone's own fall leaves Fenwick Street within it.

No other conclusion survives the files. The zone primary's own fall, against a weather-adjusted baseline or the ten previous weekdays, counts the demand that rose at the neighbour, and the ten-day baseline also sits below the cold event days it is set against, so it files all four primaries. Read at minus 3.0 C, the same fall credits 0.7, 0.5, 0.8 and 0.7 per MW and files Ashcombe Road alone (0.4 MW over firm), because it counts as the providers' reduction the demand that rose across the open points, which is not a reduction its provider delivers: section 6 of the guideline credits only that, and the award notice measures what a provider delivers on its own metered assets. Taking the linked primary as the control adds that rise twice (1.0 per MW at Ashcombe Road) and files none. The zone and its linked primary taken together give the netting's provider reduction exactly (0.4 per MW at minus 3.0 C at Ashcombe Road). Crediting the providers at the average event day rather than at the design day keeps the same two primaries over firm capacity but credits 6, 5, 9 and 5 MW, which is not the reduction section 6 of the guideline credits, and at minus 6.0 C it leaves Charlecote Way and Fenwick Street within firm capacity; on the design day's credit, Ashcombe Road and Hartwell Common need reinforcement.
