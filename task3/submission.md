## Tags

> **Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (physical-model calibration and data assimilation, spatiotemporal exposure: a well field's nitrate forecast from the land over it).
> **Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**Put Project NR-1 on the 2027 cycle.** The entry point's annual mean nitrate first reaches 10 mg/L as N in 2031 and is about 12 mg/L in 2034, so a plant funded in the 2031 cycle (in service 1 January 2034) comes too late. Not the 2031 cycle: the wells' falling record, a trend on it, and every model fitted to it with the wellhead model's groundwater travel time or one lag for every parcel set the Sallow Ridge clearing's effect to nothing, because the ridge's leachate is still in the 57 to 94 ft of sand above the water table.

## 2. Supplementary Questions

### corlinden_nitrate_plant_timing_memo.pdf

1. Opens with the call (the 2027 cycle), the first year EP-01's annual mean reaches 10 mg/L as N (2031) and the 2034 level (about 12), with a row of the forecast for 2027, 2029 to 2032, 2034 and 2040, then the chart.
2. Explains why the record looks safe (the wells fell from about 6.2 mg/L at EP-01 in 2012 to 5.3 in 2025 and show no rise where the travel time or the wells' own lag says the ridge should already show) and why the rise is coming (the unsaturated delay read from the county's matured conversions, carried to each ridge parcel's depth), with what the forecast rests on.

### corlinden_entry_point_nitrate_forecast.xlsx

3. Sheet Forecast: one row per year 2027 to 2040 with each well's forecast, the plan's shares (Well 3 8, Well 5 30, Well 6 32, Well 7 30 per cent) and EP-01's annual mean, flagged at or above 10 from 2031.
4. Sheets Unsaturated delay (the 14 matured conversions, each one's half-way arrival and delay, the fit a + b x depth with b = 0.13 years a foot), Leachate (each land cover's current level and the land-surface-year record), Protection area parcels (each parcel's delay and, for the ridge, its arrival at the well) and Wells record (observed against the model, 1990 to 2026).

### corlinden_entry_point_nitrate_2027-2040.png

5. EP-01's annual mean from 2012 to 2026 (record) and 2027 to 2040 (forecast) against a dashed 10 mg/L line, with the two cycles' in-service dates marked; the forecast steps from about 6 in 2030 to past 10 in 2031.

### Answers the Council asked for

6. First year EP-01's annual mean reaches 10 mg/L as N: 2031.
7. EP-01's 2034 annual mean: 12 mg/L as N.
8. Well with the highest 2034 annual mean: Well 7, at 16 mg/L as N.

## 3. Critical Components

1. The county's 14 network wells put under irrigation between 1990 and 2008 stepped up after a delay that grows with depth to water, **0.13 years a foot** (about 1 year at 11 ft to 10 at 82 ft), while their water-table ages are under half a year: the delay is in the unsaturated sand, and the wellhead model's travel time starts below it.
2. The Sallow Ridge parcels cleared for irrigated vegetables in 2017 to 2021 (1,099 acres, 57 to 94 ft to water, 1 to 3 years' groundwater travel from Wells 6 and 7) send their leachate to the wells **late in 2030**; with the travel time alone, or the one lag of about 4.5 years that fits the wells' record, it would already show, and fitting the record then sets the clearing's effect to nil.
3. Water under irrigated vegetables now carries about **21 mg/L as N** (the land-surface years since nutrient management; about 34 before it), mixed into each well by its parcels' recharge at the time the water left the water table.
4. EP-01 first reaches **10 mg/L in 2031** and is **12 mg/L in 2034**; Well 7 is highest, at **16 mg/L**.

## 4. Step-by-Step

1. Read corlinden_raw_water_nitrate_results_1988-2026.csv as nitrate-N (county laboratory results before 2004 reported as nitrate, divided by 4.427; field duplicates and re-runs averaged; the 2014 point names mapped): EP-01 fell from 6.2 mg/L in 2012 to 5.3 in 2025, Wells 6 and 7 from 7.0 and 5.5 in 2010 to 5.5 and 4.4 in 2026.
2. A trend on each well, blended by the plan's shares, puts EP-01 near 5 mg/L in 2034 and never at 10, so the 2031 cycle (the reasonable but insufficient reading of the record).
3. In ravell_county_parcel_land_cover_1986-2026.csv (local codes to 2007, cropland-layer codes after; split and re-numbered parcels joined through parent_parcel_id) and sallow_road_WHPA_parcel_attributes_2019.xlsx, the Sallow Ridge parcels in the zones of Wells 6 and 7 turn from forest to irrigated vegetables in 2017 to 2021. Taken at the wellhead model's groundwater travel time (1 to 3 years), or at the one lag of 4.5 years that best fits the wells' 1998 to 2018 record, the ridge would already have raised Well 6 by 10 mg/L in 2026; fitted to the 2019 to 2026 record the clearing's effect comes out at 0 per cent, and the forecast stays near 5 mg/L: the same 2031 cycle.
4. In ravell_county_groundwater_network_samples_1990-2026.csv with the sites workbook (two rebuilt wells' old numbers carried to the new), the 14 wells whose land went under irrigation in 1990 to 2008 each step up from their earlier level; the half-way arrival less the year irrigation began and the well's tritium-helium age (ravell_county_groundwater_age_survey_2019.xlsx) gives the delay to the water table, which fits a + b x depth with b = 0.132 years a foot (residual 0.3 years). Their average delay, 4.7 years, is the wrong number for the ridge: all but three of the matured conversions sit on 11 to 49 ft of sand, the ridge on 57 to 94.
5. The network's 3 wells under the 2017 to 2020 upland clearings (69 to 90 ft to water) show no rise yet, as the fit says: absence here is the leachate not yet arrived, not the land leaching nothing.
6. Each land cover's leachate by land-surface year from the network's wells on unchanged land (each sample dated back by its own age and delay): irrigated vegetables 20.9 and irrigated corn and soybean 13.2 mg/L in the latest five years, against about 34 for vegetables before nutrient management.
7. Each protection-area parcel reaches its well after its own delay and its groundwater travel time, mixed by acres times the recharge it had when the water left the water table (sallow_road_WHPA_parcel_attributes_2019.xlsx, Recharge), each well's model carried to its 2019-2026 level (residuals -0.31 to 0.01 mg/L), and the wells blended by corlinden_water_supply_plan_2025.pdf's shares with land cover held at 2026: the ridge reaches the wells late in 2030, EP-01 passes 10 in 2031 and is 12 mg/L in 2034, Well 7 at 16.

No other conclusion survives. The record, a trend on it and any fit to it read the ridge's absence as no effect, but every delay that would put the leachate at the wells by 2026 (the travel time alone, one lag for every parcel, the matured conversions' average) also predicts the rise at the county's three upland clearings, which the depth-specific delay alone explains; and under the delay that fits the matured conversions, the 2019 to 2026 record is silent on the clearing (its fit is the same at none of the effect and all of it). Read as a fitted step, through the origin, without the water-table age, or uncarried to the wells' level, the first year at 10 stays 2031 and the 2034 entry point 12 mg/L, well before 2034. Mixing by acres alone, or by the recharge at the time the nitrate left the root zone, puts Well 7 at 15, and taking vegetable leachate over all years (26 mg/L) overstates it; neither moves the cycle.
