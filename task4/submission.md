## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (fleet electrification, a road haulier's battery-electric duty assignment).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order 8 battery-electric tractors, for V02, V03, V05, V09, V11, V14, V16, V18; V07, V21, V24, V27, V30, V33 stay on diesel.** The 8 need 410 to 430 kWh on the January design day against a limit of **438 kWh** (85 per cent of the 515 kWh a 540 kWh battery keeps after a first-year loss of 4.6 per cent), and the nearest diesel duty needs 450 kWh. This rejects the 5 (V03, V05, V09, V11, V16) that a pilot model built on the terminal's calibration line, a straight-line battery loss and the year's speed ratio would order: it prices V02, V14 and V18 at 450, 450 and 450 kWh against its own 445 kWh limit. It also rejects the 10 that the same model orders at the design-day speed, which lets in V07 and V21 on a payload term of 1.5.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx
1. Sheet Assessment, one row per shortlisted duty in duty order, with shipper, delivery, the three legs and round trip km, climb, planning load, design-day energy (nearest 10 kWh; any figure within 10 kWh of the one below is acceptable), share of the first-year usable battery and whether it goes electric; below the rows the usable battery after the first year (515 kWh), the limit (438 kWh), the tractors to order (8) and the duties.
   - V02: design day 430 kWh, electric
   - V03: design day 420 kWh, electric
   - V05: design day 420 kWh, electric
   - V07: design day 450 kWh, stays diesel
   - V09: design day 410 kWh, electric
   - V11: design day 420 kWh, electric
   - V14: design day 430 kWh, electric
   - V16: design day 420 kWh, electric
   - V18: design day 430 kWh, electric
   - V21: design day 450 kWh, stays diesel
   - V24: design day 460 kWh, stays diesel
   - V27: design day 470 kWh, stays diesel
   - V30: design day 460 kWh, stays diesel
   - V33: design day 460 kWh, stays diesel
2. Sheet Energy model: the coefficients, with one tonne of payload adding **1.9 kWh per 100 loaded km** (any figure from 1.7 to 2.4 is acceptable), a tonne of combination tare 2.0 kWh per 100 km on every leg, and the cold-form comparison on January and February 2026 held out.
3. Sheet Payloads: each pilot duty's mean declared weight against its shipper's at the terminal, the error each shipper's notes carry on the Värnamo weighbridge, and the load each duty's declarations are taken to; beside it the drinks maker's scale-weighed days.
4. Sheet Trailers and drops: each shortlisted duty's combination weight with the 2027 tractor, its stops and the share of the loaded run its load rides.
5. Sheet Battery: the pilot batteries' first-year permanent loss, **4.6 per cent** (any figure from 4.2 to 5.6 is acceptable), the usable battery after the first year 515 kWh, the limit 438 kWh, and the loss under each age form.
6. Sheet Speed: each duty's routing-tool speed and its speed on a -5 C day.
7. Sheet Routes: each shortcut's payload figure, loss, limit and order beside the assessment's.

### tractor_order_memo.pdf
8. One page to the management group: the order (8 tractors, V02, V03, V05, V09, V11, V14, V16, V18) first, the fourteen duties with design-day energy and verdict, the estimates that move the order (payload 1.9 kWh per tonne per 100 loaded km, the 4.6 per cent first-year loss and the 438 kWh limit, the duties' speed on a -5 C day) and what each shortcut would order instead.

## Critical Components

1. One tonne of payload adds **1.9 kWh per 100 loaded km** (1.7 to 2.4). The pilot's regional duties carry 75 to 89 per cent of the loads their shippers declare at the terminal, so the terminal's weighed-on-declared line, which pulls a clerk's estimate toward the terminal's loads, puts each pilot duty 0.5 to 4.4 t too heavy and the term at **1.5**; taking each duty's loads from its own declarations, with the error each shipper's notes carry on the weighbridge removed, gives 1.9, the within-duty fit 1.9 (the same fit on the terminal's line 2.3), and the drinks maker's own notes confirm it: from August 2026 its declarations equal the weighbridge's net load to the bridge's 20 kg, and on J07 and J08 they average 11.6 and 10.4 t, against 11.3 and 10.4 t from the duties' own earlier declarations and 13.2 and 13.1 t on the line.
2. The pilot batteries lose **4.6 per cent** of their usable energy for good in their first year: most of it in the first months, settling over about 4 months, then a steady loss. A straight line in age puts it at 3.1 per cent and the same months a year apart at 2.8, both blind to the early loss; every curved form lands from 4.3 to 5.5. The 2027 tractor keeps **515 kWh** and the limit is **438 kWh**, not 445.

## Step-by-Step

1. Cleaned bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once, ambient dropouts filled from the Jönköping station plus the mean offset) and joined tms_consignments_jonkoping_2025-2026.csv on registration and date, the day's notes summed: 2334 pilot duty-days, each with its speed, the trailer it pulled and its drops.
2. Planning loads from weighbridge_varnamo_2024-11_2026-10.csv per FES-2 4.2: the last weighing of each CMR, VMO-nn read as Vnn, gross less tare, November 2025 to October 2026.
3. Compared each pilot duty's declarations with its shipper's at the terminal: the pilot's regional duties run at 75 to 89 per cent of the terminal's loads. The clerks' estimates scatter widely around the weighed load, so the terminal's weighed-on-declared line pulls every declaration toward the terminal's loads and does not carry to the pilot. Read each shipper's declaration error on the weighbridge at each note period, removed it from the spread of each pilot duty's own declared weights, and took each declaration to its expected load on that duty. On the terminal's line the payload term is 1.5, on the raw declarations 1.2, on the duties' own loads **1.9** (with the error additive, 1.9; within duty, 1.9). The drinks maker's notes settle it: from August 2026 they carry the weighed load (they equal the weighbridge's net to its 20 kg), and on J07 and J08 they average 11.6 and 10.4 t, against 11.3 and 10.4 t from the same duties' earlier declarations and 13.2 and 13.1 t on the terminal's line.
4. Joined each day's trailer to fleet_register_2026.xlsx (sheet Trailers) and the tractor's own tare: the pilot's combinations run 17.6 to 22.7 t, and a tonne of tare costs 2.0 kWh per 100 km on every leg. Each shortlisted duty's combination is the quotation's 11.98 t tractor plus the mean tare of the trailers it pulled at Värnamo (V02 and V14's double decks 22.6 and 22.5 t, against the pilot's 20.3 t average); left out, the order is 6 (V03 out, V11 out).
5. Took each note's weight off at its stop's km on route_register_2026.xlsx (sheet Stops): the load rides 0.60 of V03's loaded km and 0.58 of V11's (tms_consignments_varnamo_2025-11_2026-10.csv). Carried to the last drop, the order is 6 (V03 out, V11 out).
6. Chose the cold form out of sample (one rate below 16 C under-forecasts January and February 2026's sub-zero days by 6.8 per cent; a further rate below 0 C +0.7).
7. Fitted each day's energy per full charge on a level per tractor, the day's degrees below 20 C and an age form with an early-life loss that settles over a time scale the fit chooses (about 4 months) and a steady loss: **4.6 per cent** in the first twelve months. A straight line in age fits far worse and gives 3.1; the same months a year apart compare ages a year on from the first months and give 2.8; every curved form gives 4.3 to 5.5. A straight-line loss alone orders 8 (no duty moves).
8. Added the square of the day's speed and set each duty's design-day speed from its routing-tool driving time times the pilot's actual-to-planned ratio at -5 C (0.76), so the Värnamo duties, planned at 74 to 83 km/h, run at 56 to 63 km/h. At the year's ratio (0.89) the order is 1 (V02 out, V03 out, V05 out, V11 out, V14 out, V16 out, V18 out); at the routing tool's speed 0; with no speed term 10 (V21 in, V30 in).
9. Forecast each duty at -5 C, its planning load, its design-day speed, its combination and its drops: V02, V03, V05, V09, V11, V14, V16, V18 at 410 to 430 kWh; V07, V21, V24, V27, V30, V33 at 450 to 470 kWh.
10. Order 8 tractors. The terminal's calibration line alone orders 9 (V07 in); with the straight-line loss and the year's ratio as well, 5 (V02 out, V14 out, V18 out); with that line and loss at the design-day speed, 10 (V07 in, V21 in). Declared payloads order 9 (V07 in), one cold rate 9 (V21 in), no first-year loss 13 (V07 in, V21 in, V24 in, V30 in, V33 in).

No other order survives: the terminal's line does not carry to the pilot's own loads, the batteries lose most of their first year's capacity early, a winter day runs slower than the routing tool's plan or the year's ratio, a combination's tare costs on every leg and a multi-drop load does not ride the whole run. Each of the three estimates alone, put right inside the careful model, still orders wrongly (2 with the duties' own loads, 3 with the curved loss, 10 at the design-day speed). Every route that takes all the steps (knots at 14, 18, -2 or 2 C, a quadratic, temperature bins, the station's temperature, either year alone, the declaration error additive or read on the last twelve months, each day at its duty's mean declaration, the within-duty fit, every curved loss form and cold term, speed as a straight line, every form of the speed ratio, one coefficient for tare and payload, the drops at equal shares) orders the same 8, with every energy within 8 kWh of those above.
