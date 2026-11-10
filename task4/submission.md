## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (fleet electrification, a road haulier's battery-electric duty assignment).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order 7 battery-electric tractors, for V03, V05, V09, V11, V16, V18, V33; V02, V07, V14, V21, V24, V27, V30 stay on diesel.** The 7 need 410 to 430 kWh on the January design day against a limit of **442 kWh** (85 per cent of the 519 kWh a 540 kWh battery keeps after its first year), and the nearest diesel duty needs 460 kWh; this rejects the 5 that a pilot model carried per km and per departing tonne, at the year's speed ratio and with the trailers never read, would order: it prices V03 and V11 at 500 and 500 kWh because it carries their loads to the last drop on a payload term of 2.9, when their loads come off along the run.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx
1. Sheet Assessment, one row per shortlisted duty in duty order, with shipper, delivery, the three legs and round trip km, climb, planning load, design-day energy (nearest 10 kWh; any figure within 10 kWh of the one below is acceptable), share of the first-year usable battery and whether it goes electric; below the rows the usable battery after the first year (519 kWh), the limit (442 kWh), the tractors to order (7) and the duties.
   - V02: design day 460 kWh, stays diesel
   - V03: design day 430 kWh, electric
   - V05: design day 420 kWh, electric
   - V07: design day 460 kWh, stays diesel
   - V09: design day 410 kWh, electric
   - V11: design day 430 kWh, electric
   - V14: design day 460 kWh, stays diesel
   - V16: design day 410 kWh, electric
   - V18: design day 420 kWh, electric
   - V21: design day 470 kWh, stays diesel
   - V24: design day 460 kWh, stays diesel
   - V27: design day 470 kWh, stays diesel
   - V30: design day 460 kWh, stays diesel
   - V33: design day 430 kWh, electric
2. Sheet Energy model: the coefficients, with one tonne of payload adding **2.2 kWh per 100 loaded km** (any figure from 2.0 to 2.4 is acceptable), a tonne of combination tare 1.8 kWh per 100 km on every leg, the ePTO fridge unit 4.4 kW, and the cold-form comparison on January and February 2026 held out.
3. Sheet Payload calibration: each pilot shipper's weighed load against its declared weight on the Värnamo weighbridge, by note period, and the load each declaration is taken to.
4. Sheet Trailers and drops: each shortlisted duty's combination weight with the 2027 tractor, its trailers' refrigeration unit, its stops and the share of the loaded run its load rides.
5. Sheet Battery: the pilot batteries' first-year permanent loss, **3.8 per cent** (3.6 to 4.0 acceptable), the usable battery after the first year 519 kWh and the limit 442 kWh.
6. Sheet Speed: each duty's routing-tool speed and its speed on a -5 C day (0.77 of it).
7. Sheet Routes: each shortcut's payload figure, loss, limit and order beside the assessment's.

### tractor_order_memo.pdf
8. One page to the management group: the order (7 tractors, V03, V05, V09, V11, V16, V18, V33) first, the fourteen duties with design-day energy and verdict, the estimates that move the order (payload 2.2 kWh per tonne per 100 km, the combination's weight on every leg, the drops, the ePTO fridge units, the 3.8 per cent first-year loss, the duties' speed on a -5 C day) and what each shortcut would order instead.

## Critical Components

1. One tonne of payload adds **2.2 kWh per 100 loaded km** (2.0 to 2.4) once each pilot day's declared weight is taken to the weighed load it stands for, the load is taken off at each drop and the combination's tare is carried on every km (**1.3** on the declarations, 1.9 with every load carried to the last drop, 3.1 with the trailer left out).
2. The pilot batteries lose **3.8 per cent** of their usable energy for good in their first year, so the 2027 tractor keeps **519 kWh** and the limit is **442 kWh**.
3. Only the ePTO fridge units run from the tractor's battery, about **4.4 kW** from depot out to depot in: V24 and V30 pull them and need about 32 kWh each for it on the design day; V33's diesel units draw nothing.
4. On a -5 C day the pilot drove at **0.77** of the routing tool's speed (**0.89** over the year), so the Värnamo duties, planned at 74 to 83 km/h, run at 57 to 64 km/h.
5. With the 2027 tractor V02 and V14 haul double-deck combinations of **22.7** and **22.5 t** against the pilot's **20.3 t** average, and V03's and V11's loads ride **0.60** and **0.57** of their loaded km.

## Step-by-Step

1. Cleaned bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once, ambient dropouts filled from the Jönköping station plus the mean offset) and joined tms_consignments_jonkoping_2025-2026.csv on registration and date, the day's notes summed: 2334 pilot duty-days, each with its speed, the trailer it pulled, its drops and its hours from first departure to last arrival.
2. Planning loads from weighbridge_varnamo_2024-11_2026-10.csv per FES-2 4.2: the last weighing of each CMR, VMO-nn read as Vnn, gross less tare, November 2025 to October 2026.
3. Took each pilot day's declared weight to its expected weighed load at its shipper and note period, read from the Värnamo weighings (the clerks' weighed load rises 0.14 to 0.2 t per declared tonne); on the declarations a tonne costs 1.3.
4. Joined each day's trailer to fleet_register_2026.xlsx (sheet Trailers) and the tractor's own tare: the pilot's combinations run 17.6 to 22.7 t, and a tonne of tare costs 1.8 kWh per 100 km on every leg against the payload's 2.2 on the loaded run. Each shortlisted duty's combination is the quotation's 11.98 t tractor plus the mean tare of the trailers it pulled at Värnamo; left out, the pilot's average combination stands in for every duty and the order is 9 (V02 in, V14 in).
5. Took each note's weight off at its stop's km on route_register_2026.xlsx (sheet Stops), from the day's notes: the load rides 0.60 of V03's loaded km and 0.57 of V11's (tms_consignments_varnamo_2025-11_2026-10.csv). Carried to the last drop the payload term falls to 1.9 and the order is 5 (V03 out, V11 out).
6. Read the trailers' Equipment codes: only the SR-60e ePTO unit runs from the tractor (AX-40 AGen has its own axle generator, SR-60 D and D+SB their own diesel). On the pilot's dairy duty the ePTO days draw **4.4 kW** more for as long as the duty is out; V24 and V30 pull ePTO units, V33 diesel ones. Without the fridge term the order is 9 (V24 in, V30 in); with every reefer drawing it is 7 (V30 in, V33 out).
7. Chose the cold form out of sample (one rate below 16 C under-forecasts January and February 2026's sub-zero days by 6.2 per cent; a further rate below 0 C +0.5) and took the battery loss net of the cold: **3.8 per cent** (3.2 by age alone).
8. Added the square of the day's speed and set each duty's design-day speed from its routing-tool driving time times the pilot's actual-to-planned ratio at -5 C (0.77). At the routing tool's speed the order is 0; at the year's ratio (0.89) 4 (V03 out, V11 out, V33 out); with no speed term 9 (V14 in, V30 in).
9. Forecast each duty at -5 C, its planning load, its design-day speed, its combination, its drops and its fridge unit: V03, V05, V09, V11, V16, V18, V33 at 410 to 430 kWh; V02, V07, V14, V21, V24, V27, V30 at 460 to 470 kWh.
10. Order 7 tractors. Declared payloads order 8 (V07 in), one cold rate 9 (V14 in, V30 in), no first-year loss 9 (V14 in, V30 in).

No other order survives: the declarations dilute the payload term, a combination's tare costs on every leg, a multi-drop load does not ride the whole loaded run, only the ePTO units draw on the battery, the one-rate cold form fails its own holdout, FES-2 2.3 charges the first year's loss, and a winter day runs slower than the routing tool's plan or the year's ratio. Every route that takes all the steps (knots at 14, 18, -2 or 2 C, a quadratic, temperature bins, the station's temperature, either year alone, the calibration on the last twelve months, each temperature-controlled loss fit, speed as a straight line, every form of the speed ratio, one coefficient for tare and payload, the fridge unit by driving hours or by km, the drops at equal shares) orders the same 7, with every energy within 9 kWh of those above; a within-duty fit also orders the same 7, but its payload slope (2.8, standard error 0.19 against 0.04) rests on the dairy duty alone.
