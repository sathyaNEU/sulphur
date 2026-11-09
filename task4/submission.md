## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (fleet electrification, a road haulier's battery-electric duty assignment).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order 6 battery-electric tractors, for V02, V05, V09, V14, V16, V18; V03, V07, V11, V21, V24, V27, V30, V33 stay on diesel.** The heavy duties V03, V07, V11 need 450 to 460 kWh on the January design day against a limit of **441 kWh** (85 per cent of the 519 kWh a 540 kWh battery keeps after its first year); the 8 or 9 tractors a careful but hurried forecast orders (declared payloads at 1.1 kWh per tonne per 100 km, one cold rate, the pilot batteries' age trend alone) send duties out that cannot finish a cold day inside the reserve.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx
1. Sheet Assessment, one row per shortlisted duty in duty order, with shipper, delivery, the three legs and round trip km, climb, planning load (0.1 t), design-day energy (nearest 10 kWh; any figure within 10 kWh of the one below is acceptable), share of the first-year usable battery and whether it goes electric; below the rows the usable battery after the first year (519 kWh), the limit (441 kWh), the tractors to order (6) and the duties.
   - V02: planning load 3.9 t, design day 410 kWh, electric
   - V03: planning load 29.3 t, design day 450 kWh, stays diesel
   - V05: planning load 7.6 t, design day 420 kWh, electric
   - V07: planning load 32.0 t, design day 460 kWh, stays diesel
   - V09: planning load 21.2 t, design day 400 kWh, electric
   - V11: planning load 26.5 t, design day 450 kWh, stays diesel
   - V14: planning load 4.6 t, design day 430 kWh, electric
   - V16: planning load 9.1 t, design day 410 kWh, electric
   - V18: planning load 5.4 t, design day 420 kWh, electric
   - V21: planning load 18.4 t, design day 470 kWh, stays diesel
   - V24: planning load 21.0 t, design day 470 kWh, stays diesel
   - V27: planning load 13.4 t, design day 470 kWh, stays diesel
   - V30: planning load 13.5 t, design day 460 kWh, stays diesel
   - V33: planning load 3.9 t, design day 480 kWh, stays diesel
2. Sheet Energy model: the coefficients, with one tonne of payload adding **2.0 kWh per 100 loaded km**, and the cold-form comparison on January and February 2026 held out (one rate below 16 C -6.6 per cent on the sub-zero days, a further rate below 0 C +0.5 per cent).
3. Sheet Payload calibration: each pilot shipper's weighed load against its declared weight on the Värnamo weighbridge, by note period (the drinks maker's notes carry its scale weight from August 2026), and the load each declaration is taken to.
4. Sheet Battery: the pilot batteries' first-year permanent loss, **3.8 per cent**, the usable battery after the first year 519 kWh and the limit 441 kWh.
5. Sheet Routes: each shortcut's payload figure, loss, limit and order beside the golden's.

### tractor_order_memo.pdf
6. One page to the management group: the order (6 tractors, V02, V05, V09, V14, V16, V18) first, the fourteen duties with planning load, design-day energy and verdict, the three estimates that move the order (payload 2.0 kWh per tonne per 100 km against 1.1 on the declarations, the two-rate cold form, the 3.8 per cent first-year loss) and what each shortcut would order instead.

## Critical Components

1. One tonne of payload adds **2.0 kWh per 100 loaded km** once each pilot day's declared weight is taken to the weighed load it stands for, shipper by shipper; fitted on the declarations it is **1.1**.
2. The pilot batteries lose **3.8 per cent** of their usable energy for good in their first year (temperature taken out of each day's energy per full charge), so the 2027 tractor keeps **519 kWh** and the limit is **441 kWh**.
3. On the January design day, with a further cold rate below 0 C, V03, V07, V11 need **450 to 460 kWh** and V14 needs **430 kWh**.

## Step-by-Step

1. Cleaned bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once, ambient dropouts filled from the Jönköping station plus the mean offset) and joined tms_consignments_jonkoping_2025-2026.csv on registration and date: 2334 pilot duty-days with declared weights read in kg or tonnes.
2. Planning loads from weighbridge_varnamo_2024-11_2026-10.csv per FES-2 4.2: the last weighing of each CMR, VMO-nn read as Vnn, gross less tare, November 2025 to October 2026 (V03 29.3 t, V14 4.6 t).
3. Fitted each duty-day's energy on km, climb, cold and payload times loaded km. On the declared weights the payload term is 1.1 kWh per tonne per 100 km and held-out days look fine, because they carry the same declarations.
4. Read the declarations against the Värnamo weighings shipper by shipper: the clerks' weighed load rises only 0.14 to 0.21 t per declared tonne, the dairy declares one weight whatever is loaded, and the drinks maker's notes match the bridge from August 2026. Each pilot day's declaration taken to its expected weighed load at its shipper and note period gives **2.0**; one pooled line over the bridge gives 1.2 and one over the pilot shippers 1.8, each mixing different declaration habits.
5. Chose the cold form out of sample: fitted without January and February 2026, one rate below 16 C under-forecasts those sub-zero days by 6.6 per cent; with a further rate below 0 C the error is +0.5 per cent. One rate puts every design-day energy about 12 kWh low and admits V03, V11.
6. Estimated the first-year loss from each day's energy per full charge (kWh used over the SOC it took) with a level per tractor, age in service and degrees below 20 C: **3.8 per cent**. Age alone gives 3.3 per cent, because the pilot began in March and ended in a mild October; the same months a year apart give 3.7. Usable battery 519 kWh, limit 441 kWh (FES-2 2.3, 4.3).
7. Forecast each duty at -5 C and its planning load from route_register_2026.xlsx: V02, V05, V09, V14, V16, V18 at 400 to 430 kWh; V03, V07, V11 at 450 to 460 kWh; the rest at 460 to 480 kWh.
8. Order 6 tractors. Declared payloads order 8 (V03, V07, V11 in, V14 out), one cold rate 8, no first-year loss 9, the three hurried steps together 9.

No other order survives: the declared weights are unbiased on average but scattered, so the slope fitted on them is diluted and only the weighbridge, read shipper by shipper, recovers it; the one-rate cold form fails its own holdout; and FES-2 2.3 charges the first year's loss, which the cold days hide unless temperature is taken out. Every route that takes all three steps (knots at 14, 18, -2 or 2 C, a quadratic, temperature bins, the station's temperature, either year alone, a within-duty fit, the calibration on the last twelve months, any of the temperature-controlled loss fits or the same months a year apart) orders the same 6, with every energy within 6 kWh of those above.
