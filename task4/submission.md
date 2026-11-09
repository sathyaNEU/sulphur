## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (fleet electrification, a road haulier's battery-electric duty assignment).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order 6 battery-electric tractors, for V02, V05, V09, V14, V16, V18; V03, V07, V11, V21, V24, V27, V30, V33 stay on diesel.** V03, V11, V30 need 450 to 460 kWh on the January design day against a limit of **442 kWh** (85 per cent of the 520 kWh a 540 kWh battery keeps after its first year); the 9 tractors a forecast in proportion to distance orders, even with the payloads, the cold and the battery loss right, prices the Värnamo duties at the pilot's slower speeds, 9 to 21 kWh too low.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx
1. Sheet Assessment, one row per shortlisted duty in duty order, with shipper, delivery, the three legs and round trip km, climb, planning load, design-day energy (nearest 10 kWh; any figure within 10 kWh of the one below is acceptable), share of the first-year usable battery and whether it goes electric; below the rows the usable battery after the first year (520 kWh), the limit (442 kWh), the tractors to order (6) and the duties.
   - V02: design day 410 kWh, electric
   - V03: design day 450 kWh, stays diesel
   - V05: design day 420 kWh, electric
   - V07: design day 460 kWh, stays diesel
   - V09: design day 400 kWh, electric
   - V11: design day 450 kWh, stays diesel
   - V14: design day 440 kWh, electric
   - V16: design day 410 kWh, electric
   - V18: design day 420 kWh, electric
   - V21: design day 470 kWh, stays diesel
   - V24: design day 470 kWh, stays diesel
   - V27: design day 470 kWh, stays diesel
   - V30: design day 460 kWh, stays diesel
   - V33: design day 480 kWh, stays diesel
2. Sheet Energy model: the coefficients, with one tonne of payload adding **2.1 kWh per 100 loaded km** (any figure from 1.9 to 2.1 is acceptable), and the cold-form comparison on January and February 2026 held out.
3. Sheet Payload calibration: each pilot shipper's weighed load against its declared weight on the Värnamo weighbridge, by note period, and the load each declaration is taken to.
4. Sheet Battery: the pilot batteries' first-year permanent loss, **3.8 per cent** (3.6 to 4.0 acceptable), the usable battery after the first year 520 kWh and the limit 442 kWh.
5. Sheet Speed: each duty's routing-tool speed and its speed on a -5 C day (0.82 of it).
6. Sheet Routes: each shortcut's payload figure, loss, limit and order beside the assessment's.

### tractor_order_memo.pdf
7. One page to the management group: the order (6 tractors, V02, V05, V09, V14, V16, V18) first, the fourteen duties with design-day energy and verdict, the four estimates that move the order (payload 2.1 kWh per tonne per 100 km, the two-rate cold form, the 3.8 per cent first-year loss, the duties' speed on a -5 C day) and what each shortcut would order instead.

## Critical Components

1. The Värnamo duties run at 74 to 83 km/h on the routing tool against at most 73 km/h on any pilot day; at the pilot's actual-to-planned ratio on a -5 C day (0.82, against 0.91 over the year) they drive at 61 to 68 km/h, and each 10 km/h there costs about **6.2 kWh per 100 km**.
2. One tonne of payload adds **2.1 kWh per 100 loaded km** (1.9 to 2.1) once each pilot day's declared weight is taken to the weighed load it stands for, shipper by shipper (**1.2** on the declarations).
3. The pilot batteries lose **3.8 per cent** of their usable energy for good in their first year, so the 2027 tractor keeps **520 kWh** and the limit is **442 kWh**.
4. On the January design day V03, V11, V30 need **450 to 460 kWh** and V14 needs **440 kWh**.

## Step-by-Step

1. Cleaned bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once, ambient dropouts filled from the Jönköping station plus the mean offset) and joined tms_consignments_jonkoping_2025-2026.csv on registration and date: 2334 pilot duty-days, each with its average speed (distance over driving time).
2. Planning loads from weighbridge_varnamo_2024-11_2026-10.csv per FES-2 4.2: the last weighing of each CMR, VMO-nn read as Vnn, gross less tare, November 2025 to October 2026.
3. Took each pilot day's declared weight to its expected weighed load at its shipper and note period, read from the Värnamo weighings (the clerks' weighed load rises 0.13 to 0.2 t per declared tonne): **2.1** kWh per tonne per 100 km against 1.2 on the declarations.
4. Chose the cold form out of sample (one rate below 16 C under-forecasts January and February 2026's sub-zero days by 6.4 per cent; a further rate below 0 C +0.8) and took the battery loss net of the cold: **3.8 per cent** (3.2 by age alone).
5. Added the day's average speed to the energy model (air drag, on the square of speed): the pilot fit improves only from 2.88 to 2.51 per cent, and a model without it validates on held-out pilot days, because the pilot never drives as fast as the Värnamo duties.
6. Set each Värnamo duty's design-day speed from route_register_2026.xlsx's routing-tool driving time times the pilot's actual-to-planned speed ratio at -5 C (0.82; 0.91 over the year). Without a speed term the order is 9 (V03, V11, V30 in); at the routing tool's speed 3 (V05, V14, V18 out); at the year's ratio 5 (V14 out).
7. Forecast each duty at -5 C, its planning load and its design-day speed: V02, V05, V09, V14, V16, V18 at 400 to 440 kWh; V03, V11, V30 at 450 to 460 kWh; the rest at 460 to 480 kWh.
8. Order 6 tractors. Declared payloads order 8 (V03, V07, V11 in, V14 out), one cold rate 9, no first-year loss 10 (V03, V07, V11, V30 in).

No other order survives: the declared weights dilute the payload term, the one-rate cold form fails its own holdout, FES-2 2.3 charges the first year's loss, and the Värnamo duties drive faster than any pilot day but slower than the routing tool promises on a winter day, so a forecast at the pilot's speeds, at the routing tool's or at the year's average ratio each orders another number. Every route that takes all four steps (knots at 14, 18, -2 or 2 C, a quadratic, temperature bins, the station's temperature, either year alone, a within-duty fit, the calibration on the last twelve months, each temperature-controlled loss fit, speed as a straight line, and the ratio's slope below 8 or 12 C, on the temperature or over days within 2.5 C of -5) orders the same 6, with every energy within 7 kWh of those above.
