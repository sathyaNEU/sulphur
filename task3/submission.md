# task3 submission: Durrow Creek bridge span

## Tags

**Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (extreme-value and environmental-hazard return-period analysis: flood frequency at an ungauged site).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Build the 185 ft span.** Durrow Creek's 1 per cent annual exceedance flood at Ransom Bar Road is about **25,000 cfs** once the Coyner River's record is carried to the creek flood by flood, at the rain each storm put on each basin below its snow line, which is above the 140 ft span's rated 20,500 cfs and inside the 185 ft span's 29,000 cfs; this rejects the 140 ft span that the drainage-area transfer of the river's curve (about 18,700 cfs) would choose, because the river's floods drained rain over only about half of its high basin while the foothill creek drains whole, and the 240 ft span that a snow line placed with the standard atmosphere's 6.5 degrees C per kilometre (about 35,000 cfs) would choose.

## Supplementary Questions

### durrow_creek_bridge_hydrology_report.pdf

1. The report recommends the 185 ft span: its rated flow (29,000 cfs) carries the creek's 1 per cent flood and the 140 ft span's (20,500 cfs) does not; it gives the basin (85.3 square miles), the record carried (the Coyner River near Tessel, USGS 12183450), how each flood was carried, the flows as a table with a chart of the creek's frequency curve against the three spans' rated flows, the span table and the creek's largest floods.
2. The creek's 50 per cent annual exceedance flow: 10,000 cfs.
3. The creek's 1 per cent annual exceedance flow: 25,000 cfs.
4. The 140 ft span (rated 20,500 cfs): its rated flow would be exceeded once in 10 to 100 years.
5. The 185 ft span (rated 29,000 cfs): its rated flow would be exceeded once in 100 to 1,000 years.
6. The 240 ft span (rated 40,000 cfs): its rated flow would be exceeded less often than once in 1,000 years.
7. The creek's two largest floods since 1951 came in water years 2008 and 2011.

### durrow_creek_estimated_annual_peaks.csv

8. Seventy-five rows, one per water year from 1951 to 2025 in order, columns water_year, estimated_peak_flow_cfs (to the nearest 100 cfs), qualifier, coyner_river_peak_date and coyner_river_peak_cfs (the date and peak of the Coyner River flood carried); water year 1997 holds no flood fed by rain and is given as less than the low-flood threshold (qualifier "<"); the two largest values are water years 2008 and 2011, the same floods the report names.

## Critical Components

1. Durrow Creek's 1 per cent flood is about **25,000 cfs**, against rated flows of **20,500**, **29,000** and **40,000 cfs** for the 140, 185 and 240 ft spans, so the 185 ft span is the shortest that carries it.
2. In the Coyner River's floods only about **half** of its basin drained rain (a median **50 per cent**; the rest lay above the storm's snow line) against **all** of Durrow Creek's, so the creek's 1 per cent flood is about a third larger than the river's own **18,900 cfs**, not the same size.
3. Each flood's snow line comes from the airport's hourly temperature while its rain fell, with the storm lapse rate the station pair shows on storm days (about **5.4 degrees C per kilometre**, well below the standard atmosphere's 6.5) and the SNOTEL pillows' rain-snow temperature (about **0.9 degrees C**).
4. The creek's two largest floods since 1951 came in water years **2008** and **2011**, not in the Coyner River's record years (1983 and 2001).

## Step-by-Step

1. Fitted Bulletin 17C to the Coyner River's 75 annual peaks in usgs_12183450_coyner_r_annual_peaks.txt (expected moments, station skew weighted with the regional skew of -0.12 in wsdot_region3_flood_frequency_excerpt.pdf): the river's 1 per cent flood is 18,900 cfs.
2. The reasonable but insufficient route: carried that curve to the creek by drainage area (region3_basin_characteristics.xlsx, 85.3 against 86.4 square miles) and got about 18,700 cfs, the 140 ft span, with the river's record years as the creek's largest floods; the same transfer reproduces the region's other gauged basins because all of them are high basins like the river's.
3. Read the elevation bands in the workbook: the river's area has a mean of 6,350 ft and reaches 10,380 ft, the creek's a mean of 1,860 ft and a top of 4,380 ft, so in a winter storm the two basins drain different shares of their area as rain.
4. Measured the snow line's inputs: the storm lapse rate from ghcnd_tessel_daily_1950-2025.csv and ghcnd_durrow_ridge_daily_1950-2025.csv on days both caught 0.5 in or more (5.36 degrees C per kilometre, 2,158 days; the SNOTEL pair gives 5.21), the rain-snow temperature from the two SNOTEL files (0.89 degrees C) and the rise of precipitation from the warm storms' ridge and valley totals (10 per cent per 1,000 ft).
5. For each flood in the annual and above-base peak files, took the run of wet hours before its peak in lcd_tessel_field_hourly_1950-2025.csv (routine FM-15 reports; rain from the last wet hour within 36 hours of the peak, dry spells of 6 hours or less) and its rain-weighted temperature, the temperature the rain fell at (the reading at the river's peak hour is not: no rain fell in that hour in 48 per cent of the floods, and it ran a median 0.7 degrees C colder): 183 floods were fed by rain, the river drained rain over a median 50 per cent of its basin and the creek over 100 per cent, and the river's own peaks follow that rain at a correlation of 0.76 against 0.55 for the storm's whole-basin rain.
6. Carried each flood to the creek at the ratio of the two basins' rain below its snow line with the state equation's drainage-area exponent, took the largest carried flood in each water year, and entered water year 1997, with no flood fed by rain, as below the low-flood threshold.
7. Fitted Bulletin 17C to the carried series: the creek's 50 per cent flow is about 10,000 cfs and its 1 per cent flow about 25,000 cfs, and the two largest carried floods are water years 2008 and 2011.
8. Compared the rated flows in hess_tm_durrow_creek_bridge_span_ratings.pdf with the curve: the 140 ft span's 20,500 cfs would be exceeded once in 10 to 100 years, the 185 ft span's 29,000 cfs once in 100 to 1,000 years, so the county builds the 185 ft span.

No other conclusion survives. The drainage-area transfer, the region's mean unit flood (18,700 cfs) and the state equation (14,200 cfs, barred by section 7.4.3(c)) all assume the creek drains the same share of each storm as the high gauges, which the stations and the elevation bands refute. A snow line placed with the standard atmosphere's lapse rate (about 35,000 cfs) or rain counted without its rise with elevation (about 30,000 cfs) contradicts what the stations measure in storms and points to the 240 ft span; the valley's daily mean temperature and the airport's reading at the river's peak hour both read air the rain did not fall in, which the rain-weighted hourly record separates, and every storm definition and rain weighting the hourly record allows keeps the 1 per cent flood at about 25,000 cfs and the 185 ft span.
