# task3 submission: Port Tolliver's FY2028 tide valves

## Tags

**Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (extreme-value and environmental-hazard analysis: tidal high-water exceedance carried from a tide gauge to low points with short records).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Fund the valves at Wharf Street at Market Lane and Front Street at Ferry Lane.** They expect about 32.3 and 25.0 tidal flood days in the 2027-28 tide year against 17.1 or fewer at each of the other three, and they come out on top under every defensible variant of the method; this rejects the pair that straight-line campaign transfers fund (River Road at Hensley Landing and Marsh Road at Pellam Creek, 37.3 and 33.6 days), because Pellam Creek's high water bends below the line once the tide tops the marsh and River Road's only campaign sat in a wet late winter whose river lift the autumn king tides do not get.

## Supplementary Questions

### fy2028_tide_valve_ranking.xlsx

1. A Ranking sheet with one row per low point, the funded two first, columns low point, LP ID, flooding elevation (ft NAVD88), 2025-26 tidal flood days, expected tidal flood days 2027-28 (one decimal), the 90 per cent range, funded (yes for Wharf Street at Market Lane and Front Street at Ferry Lane) and the basis; a Harbor gauge sheet; a Weather years sheet (each of the 36 weather years' counts at every low point and that year's top two); a Variants sheet (the funded pair and each low point's expected days under each of the 72 defensible variants); and a Routes sheet (the pair under each shortcut).
2. Expected tidal flood days in the 2027-28 tide year (the band each spans across the defensible variants): Front Street at Ferry Lane 25.0 (23.9 to 25.5); Marsh Road at Pellam Creek 14.3 (11.7 to 18.3); River Road at Hensley Landing 17.1 (11.7 to 18.7); Wharf Street at Market Lane 32.3 (31.3 to 32.8); Oyster Creek Road 1.2 (0.4 to 1.9).
3. Tidal flood days in the 2025-26 tide year: Front Street at Ferry Lane 20 (19 to 21); Marsh Road at Pellam Creek 17 (16 to 20); River Road at Hensley Landing 10 (8 to 12); Wharf Street at Market Lane 26 (25 to 27); Oyster Creek Road 8 (7 to 11).
4. Wharf Street at Market Lane and Front Street at Ferry Lane are the top two in 28 of the 36 weather years (27 to 33 across the variants); in the others River Road takes Front Street's place.
5. The harbor gauge expects about 27.0 days at its 8.6 ft minor flood threshold in 2027-28 (25.9 to 27.5 across the variants), with a 90 per cent range of 22 to 31 days (low end 19.5 to 23.5, high end 30.0 to 35.0).
6. From 21 days in 2025-26 to about 27.0 in 2027-28 (a change of about +6.0), sea level adds about +5.8 days (+4.1 to +7.0 whichever order the three changes are applied in); the tides and the weather share the rest, and their shares turn on the order: the tides between -3.0 and +1.7 and the weather between -0.7 and +2.3 (-0.7 and +1.0 averaged over the six orders), the three parts adding to the change in every order.

### fy2028_tide_valve_memo.pdf

7. A one-page memo to the Stormwater Advisory Board that opens with the funded pair and its expected days, gives the five-row table and a bar chart of expected days with each low point's range (the funded two highlighted), then the harbor gauge's figures and change, and a paragraph each on how Front Street, Marsh and Oyster Creek Roads, and River Road were carried from the harbor.

## Critical Components

1. Marsh Road floods at a harbor high water of about **8.75 ft** (8.70 to 8.76 across the bending forms), not the 8.54 ft one straight line through its 2024 campaign gives, so it flooded on about **17** days in 2025-26 (not 26) and expects about **14.3** in 2027-28 (not 33.6).
2. River Road's high waters stand about **0.47 ft** higher at 25,000 cfs than at 5,000 cfs, and its campaign ran at 24,900 cfs on average, so carried day by day on the Brayle's flows it flooded on about **10** days in 2025-26 (8 to 12 across the flow forms the campaign fits; the campaign's single offset gives 26) and expects **11.7 to 18.7** days in 2027-28 (17.1 by the best-fitting form), far below the single offset's 37.3.
3. Front Street's lane sits at **5.20 ft NAVD88**, the lowest water level its street sensor records on the lane; it flooded on **20** days in 2025-26, 15 of them recorded by the sensor and 5 in its outage.
4. Wharf Street at Market Lane (**32.3**) and Front Street at Ferry Lane (**25.0**) lead the other three by at least **1.35 times** under every one of the 72 defensible variants, and the pair holds in about **28 of 36** weather years.

## Step-by-Step

1. Put the harbor's verified high waters, predictions and monthly means (8673718 files) on the 1983-2001 MLLW datum and the inventory and loggers on NAVD88 with the datums page's 3.42 ft; the 2025-26 tide year's mean sea level stood 0.63 ft above the epoch's.
2. Took each past high water's departure from its prediction less its tide year's mean sea level (an hourly residual swings through the tide, and the raw departure carries the sea level twice: 38.9 days); replayed on 2025-26 it gives the observed 21 days.
3. Ran the 2027-28 predicted high waters at the planning sea level (0.70 ft) under each of the 36 weather years: the harbor expects about 27.0 days, 22 to 31 in nine years of ten; the count trend files 10.8 and a Poisson range 19 to 36.
4. Split the harbor's change from 21 to 27.0 over the six orders of applying sea level, tides and weather: about +5.8, -0.7 and +1.0; taken one at a time from 2025-26 the three do not add to the change.
5. Read Front Street's lane from the street sensor (pt-front-01): the lowest water level it records on the lane in readings that persist is 5.20 ft NAVD88 (vehicles are single readings, rain ponds at lower tides); the drain rim in the inventory files 44 days for 2025-26, and the sensor alone misses its outage's 5.
6. Paired the 2024 Marsh Road campaign's (PEL-MR-24) high waters with the harbor's: one straight line fits the bulk but runs above all 13 high waters where the harbor reached 8.3 ft or more (by 0.18 ft on average), its residuals 0.10 ft against 0.03 for a transfer that bends near the marsh platform (4.29 ft NAVD88); the bending transfer floods the road at 8.75 ft; Oyster Creek (OYS-CR-25) bends the same way and floods only at 9.11 ft.
7. Paired River Road's campaign (HEN-RR-25) with the harbor and the USGS daily flows: the offset falls as the river falls (the staff checks rule out drift), and the linear, power and curved flow forms fit alike (the square-root and logarithmic forms fit worse), so the transfer carries the flow: 2025-26 gives about 10 days and the single campaign offset 26.
8. Ran every low point through the same weather years, each with its own transfer and that year's river flows: Wharf Street at Market Lane 32.3; Front Street at Ferry Lane 25.0; River Road at Hensley Landing 17.1; Marsh Road at Pellam Creek 14.3; Oyster Creek Road 1.2; the funded pair is the same under all 72 variants, and holds in about 28 of the 36 weather years.

No other pair survives. Straight-line transfers fund River Road and Marsh Road (37.3 and 33.6 days), but Marsh Road's own high waters above the marsh and River Road's own offset against the river's flow refute both; the drain rim and the untransferred harbor fund Front Street and River Road; the count trend and a Poisson range ignore the planning sea level and the clustering of tidal days. Every alignment of the weather years, every flow form the campaign fits and every bending form of the marsh transfer keep Wharf Street and Front Street on top.
