## Tags

**Domain:** Physical & Environmental Sciences, hydrology (flood frequency).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Build Alternative B, the triple 10 ft x 9 ft box (capacity 13,380 cfs): the design flow at Kinnard Road is about 10,570 cfs once the record's storms are run through today's watershed.**
Not Alternative A (7,460 cfs), which the gauge's 70 annual peaks fitted as they stand would choose at 5,090 cfs: they show no trend only because the paved watershed's faster floods and the lighter storms since 1990 cancel in them.

## Supplementary Questions

### kinnard_road_culvert_design_flow.docx

1. States the design flow, about 10,570 cfs (9,570 to 11,250 cfs on every sound pairing of the storms with their floods), and recommends Alternative B, triple 10 ft x 9 ft box, capacity 13,380 cfs; Alternative A (7,460 cfs) would overtop and Alternative C (18,720 cfs) passes at greater cost.
2. A chart of peak flow against return period: the frequency curve of the table the estimate rests on, the recorded peaks' curve beside it, both series' plotting positions, and the three capacities as lines.
3. Names water year 1968 as the largest flood in the table the estimate rests on (3,880 cfs recorded, about 7,810 cfs on today's watershed), not water year 1990, the largest as recorded (4,510 cfs).
4. The four largest in order: water years 1968, 1983, 1978 and 1962; as recorded the order would be 1990, 1983, 1968 and 1978.

### ollery_creek_design_peak_table.csv

1. 70 rows, one per water year 1956 to 2025; columns water_year, peak_date, recorded_peak_cfs and estimate_peak_cfs, the last the peak the estimate rests on: each recorded peak raised by the response's rise between that year's paved fraction and 2025's, to the nearest ten cfs; water year 1968's row reads about 7,810 cfs.

## Critical Components

1. The 70 recorded annual peaks show no trend (Kendall's tau **0.02**, p = **0.79**) and fitted as they stand give **5,090 cfs**, under Alternative A's 7,460.
2. Paired with the rain gauge's storm totals, the same storm makes about **2.0 times** the peak on today's watershed that it made in 1960: the log peak rises **2.96** per unit of paved fraction, which grew from **6** to **30 per cent**.
3. On today's watershed the design flow is about **10,570 cfs** (**9,570** to **11,250** on every sound pairing), above Alternative A's **7,460** and under Alternative B's **13,380**.
4. Water year **1968** is the largest flood on today's watershed, not **1990**, the largest as recorded.

## Step-by-Step

1. Read the Drainage Standard section 4: the design flow is the peak with a 1 per cent chance of being equalled or exceeded in any year of the crossing's first ten years of service (4.2), estimated from the gauge's record with the county's other records for the watershed (4.3); the least costly alternative whose capacity reaches it is recommended (4.5); capacities are in kinnard_road_culvert_alternatives.docx.
2. Fitted the 70 annual peaks in ollery_creek_annual_peak_flows.csv as they stand: Kendall's tau 0.02 (p = 0.79), no trend, and the log-Pearson III 1 per cent flow 5,090 cfs, which picks Alternative A; the peaks since 1995 alone, the peaks regressed on the paved fraction or detrended in time all stay at or under 5,870 cfs, the reasonable analysis that falls short.
3. Rebuilt each year's paved fraction from tamsett_stormwater_impervious_parcels.xlsx (the Ollery basin's impervious area by the year it was built, a split parcel under both numbers counted once, over the basin's 11.5 square miles): 6 per cent in 1956, 30 in 2025.
4. Paired the peaks in ollery_creek_peaks_above_base_1956-2025.csv (the 2009 and 2010 duplicate export counted once) with tamsett_rain_gauge_daily_1956-2025.csv's totals for the peak day and the two days before (the gauge in service, Monday accumulations spread): for the 312 storms of an inch or more, the log peak rises 2.96 per unit of paved fraction at a fixed storm, about 2.0 times the 1960 peak for the same storm; the storms since 1990 also ran lighter, which is why the annual peaks hide it.
5. Put each annual peak on today's watershed by that rise and refitted log-Pearson III: the 1 per cent flow is about 10,570 cfs, over Alternative A's 7,460 and under Alternative B's 13,380, so the county builds Alternative B.
6. Ranked the adjusted table: water year 1968 is the largest (3,880 cfs recorded, about 7,810 cfs today), then 1983, 1978 and 1962; as recorded the order is 1990, 1983, 1968 and 1978.

No other conclusion survives. Every sound pairing of the storms with their floods (windows of two to four days, storms of half an inch to three inches, the annual peaks against their own storms, decade effects, log-Pearson III or the generalized extreme value) puts the design flow between 9,570 and 11,250 cfs, between Alternative A's and Alternative B's capacities, and keeps water year 1968 first and the same four largest in the same order. Every route that fits the recorded peaks, however trimmed or detrended, stays at or under 5,870 cfs, because the lighter storms of the last three decades hide the faster floods in the annual maxima; only setting each flood against its storm separates the two.
