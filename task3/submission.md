## Tags

> **Domain:** Engineering and Physical Sciences, Physical & Environmental Sciences (inverse problems: physical-model calibration and uncertainty propagation, a groundwater withdrawal forecast).
> **Analytical objective:** Forecasting & Predictive Modeling.

## 1. Final Recommendation

**The district will permit the 1,000 gpm schedule.** Its greatest monthly drawdown at OW-S in 2046 is 8 ft against Rule WR-4's 9 ft limit, and the 1,250 gpm schedule reaches 10 ft. Not 1,250 gpm: calibrating the far field on the Mill Street record read against the nearest network well CV-07 or the wells' own pre-pumping levels credits the region's wet years to leakage and puts every schedule under 4 ft; and not none of them: the test's Theis fit, carried twenty years, puts even 450 gpm at 22 ft.

## 2. Supplementary Questions

### reidel_road_WR-4_demonstration.pdf

1. Page 1 states that the district will permit the 1,000 gpm schedule, with a table of the four schedules (450, 700, 1,000 and 1,250 gpm), each one's greatest monthly drawdown at OW-S in 2046 (4, 6, 8 and 10 ft) and whether it is within 9.0 ft (yes, yes, yes, no).
2. The chart under the table plots the drawdown at OW-S in every month from January 2027 to December 2046 for each schedule, one line per schedule with the 1,000 gpm line heaviest, against a dashed 9.0 ft limit line; every schedule's greatest month falls in 2046.
3. The text below gives the test fit (transmissivity 8,160 ft2/day, storativity 1.0e-03), the separation of the Mill Street record against CV-02 and CV-11, the leakage factor of 3,526 ft with the walls 5,000 ft apart, and the schedules and projection used.

### reidel_road_sentinel_forecast.xlsx

4. Sheet Demonstration: one row per schedule with the greatest monthly drawdown at OW-S in 2046 (to the hundredth and to the nearest foot: 4, 6, 8 and 10 ft), the greatest in the term and whether it meets 4.1; then the permitted schedule, 1,000 gpm.
5. Sheet Forecast OW-S: one row per month from 2027-01 to 2046-12 with the Mill Street projection (gpm), the drawdown from the Mill Street wells, and for each schedule its Reidel Road rate and the total drawdown at OW-S.
6. Sheets Aquifer test, Mill Street record and Calibration: the test fit, the monthly record from 2005 with each well's drawdown against the far wells and the model's, and the leakage factor with its residuals.

### Answers the district asked for

7. Greatest monthly drawdown at OW-S in 2046: 450 gpm 4 ft; 700 gpm 6 ft; 1,000 gpm 8 ft; 1,250 gpm 10 ft.
8. Drawdown the Mill Street wells caused at the Mill Street monitoring well, 2025 average: 5 ft.
9. Greatest monthly drawdown in 2046 at the registered domestic well nearest the Reidel Road field (DW-17), under the 1,000 gpm schedule: 7 ft.

## 3. Critical Components

1. The test's Theis fit (transmissivity **8,160 ft2/day**, storativity **1.0e-03**) matches the three observation wells to 0.08 ft, yet carried forward it puts the Mill Street wells' 2025 drawdown at MS-MW at **12 ft**: the test cannot see the far field.
2. CV-07 sits inside the Mill Street cone (its departure from CV-02 and CV-11 grew from **0.01 ft** in 2008 to **-1.67 ft** in 2025), so the natural level comes from CV-02 and CV-11, and against it the Mill Street wells drew MS-MW down **5 ft** in 2025.
3. The bounded leaky aquifer reproducing that drawdown has a leakage factor of **3,526 ft**; against CV-07 the record asks for about **1,900 ft**.
4. Greatest monthly drawdown at OW-S in 2046: **8 ft** at 1,000 gpm and **10 ft** at 1,250 gpm, against the **9 ft** limit.

## 4. Step-by-Step

1. From PW-1_constant_rate_2026-09_transducers.csv, barologger_BL-2231_2026-09.csv and the field readings' Loggers sheet: each logger on its own clock, pressure less the barologger, the OW-2 re-hang and OW-3's rewritten rows taken out, drawdown against each well's pre-test trend and barometric response.
2. Fitted Theis to OW-1, OW-2 and OW-3 at the totalizer's 1005 gpm: transmissivity 8,160 ft2/day, storativity 1.0e-03, residual 0.08 ft (the field's method); each well alone gives 8,320, 8,090 and 8,260 ft2/day, and every one of them keeps the call below.
3. Hindcast the Mill Street wells (monthly gpm from harlow_springs_MOR_well_production_2009-2026.csv, thousand gallons before July 2016) with that fit: 12 ft at MS-MW in 2025, more than twice the record, so the far field is calibrated on the record.
4. Read MS-MW (dropping readings taken with TW-1 running, the measuring point from cvwcd_well_register.xlsx) and the network wells: against its own 2005 to 2008 level or against CV-07 the record calibrates a leakage factor near 1,900 ft and every schedule under 4 ft at OW-S, filing 1,250 gpm (the reasonable but insufficient route).
5. CV-07's departure from CV-02 and CV-11 deepens with Mill Street pumping (correlation 0.91 with the monthly rate, against 0.15 for CV-02 less CV-11), and OW-S moved with CV-02 and CV-11 before 2009 (correlation 0.99): the natural level is CV-02 and CV-11's, and against it the Mill Street wells drew MS-MW down 5 ft in 2025.
6. With the walls at Plate 3's mapped edges (5,000 ft apart) and the test's T and S, the leakage factor that reproduces the drawdown at MS-MW, CV-07 and OW-S from March 2009 to September 2026 is 3,526 ft.
7. Superposed the Mill Street projection (reidel_road_WR-4_application_requested_schedules.pdf) and each Reidel Road schedule from April 2027 month by month at OW-S: greatest monthly drawdown in 2046 4, 6, 8 and 10 ft for 450, 700, 1,000 and 1,250 gpm, so Rule WR-4 4.2 permits 1,000 gpm.
8. Rule WR-4 4.4's domestic well is DW-17, nearest PW-1 and PW-2 in cvwcd_well_register.xlsx and about 200 ft inside the plate's west edge, where the wall's image matters: 7 ft in 2046 under 1,000 gpm, against 6 ft if the walls are left out (the record alone fits either way).

No other schedule survives. Theis from the test alone fails every schedule, but its own hindcast of the Mill Street record is more than twice the record. Every far-field calibration read against CV-07, the wells' own baselines or a fitted trend files 1,250 gpm, and CV-07's growing departure and the wet 2010s rule each of those out. Against CV-02, CV-11 or both, with the walls from 4,000 ft apart to absent and T from any observation well, the 1,000 gpm peak stays under 9 ft and the 1,250 gpm peak over it. Calibrated on OW-S alone, whose record carries half a foot of Mill Street drawdown, the leakage factor (3,065 ft) puts MS-MW's 2025 drawdown at 4.4 ft against the record's 4.9: it fits the sentinel's own small signal more closely only by missing the wells the Mill Street pumping draws down most. At DW-17 a model without the walls fits the record as well and reads 6 ft, but Plate 3 maps the edges of the saturated sand and gravel 5,000 ft apart, and the walls give 7 ft.
