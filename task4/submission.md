## Tags

**Domain:** Mathematics, Statistics and Computer Science, General Statistics & Data Science (regression, classification & model diagnostics), house domain Supply Chain & Logistics.
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Order 6 battery-electric tractors, for Värnamo duties V02, V05, V09, V14, V16, V18; V03, V07, V11, V21, V24, V27, V30, V33 stay on diesel.** Each of the six needs at most **450 kWh** on the January design day against FES-2's **459 kWh** (85 per cent of 540 kWh usable) once each pilot day's declared payload is taken to the weighed load it stands for, which puts a tonne at **2.2 kWh per 100 km loaded**; the model fitted on the declared weights (1.0 kWh) orders 8, sending the heavy duties V03, V07, V11 (440 kWh on the declared weights, 470 kWh in fact) and dropping V14.

## Supplementary Questions

### ev_duty_assessment_2027.xlsx

1. One row per shortlisted duty (fourteen), with its shipper, delivery, the three legs and round-trip km, climb, planning load (mean weighed net payload, November 2025 to October 2026), the January design-day energy to the nearest 10 kWh, its share of the 540 kWh usable battery and whether it goes battery-electric; beneath, the number of tractors and the duties going. Sheets for the energy model and the payload calibration sit behind it.
2. V02: 430 kWh, goes battery-electric.
3. V03: 470 kWh, stays diesel.
4. V05: 440 kWh, goes battery-electric.
5. V07: 470 kWh, stays diesel.
6. V09: 420 kWh, goes battery-electric.
7. V11: 470 kWh, stays diesel.
8. V14: 450 kWh, goes battery-electric.
9. V16: 430 kWh, goes battery-electric.
10. V18: 440 kWh, goes battery-electric.
11. V21: 490 kWh, stays diesel.
12. V24: 480 kWh, stays diesel.
13. V27: 490 kWh, stays diesel.
14. V30: 480 kWh, stays diesel.
15. V33: 490 kWh, stays diesel.
16. Tractors to order: 6 (V02, V05, V09, V14, V16, V18).

### tractor_order_memo.pdf

17. One page to the board: the order of 6 tractors and the duties first, the fourteen duties' design-day energies in a table, then how the energy was estimated (the declared payloads calibrated on the Värnamo weighbridge, 2.2 against 1.0 kWh per tonne per 100 km) and what the declared-weight model would have ordered (8 tractors).

## Critical Components

1. On the Värnamo weighbridge the declarations are right on average (declared less weighed, **-39 kg**) but for the estimating pilot shippers the weighed load rises only **0.26 to 0.30** tonnes per declared tonne; the dairy declares one standard weight (**13,500 kg**) and Tabergs Trävaror its own weighbridge figure (slope **1.00**).
2. A tonne of payload costs **2.2 kWh per 100 km loaded** with each pilot day's payload taken to its expected weighed load shipper by shipper (the Tabergs days alone give 2.2), against **1.0** fitted on the declared weights.
3. The heavy duties V03, V07, V11 need **470 kWh** on the January design day and V14 **450 kWh**, against the 459 kWh limit.
4. **6** tractors: V02, V05, V09, V14, V16, V18.

## Step-by-Step

1. Joined bev_daily_summary_2025-03_2026-10.csv (a day uploaded twice kept once) to tms_consignments_jonkoping_2025-2026.csv on registration and date, giving 2334 duty-days with the declared weight (kilograms or tonnes with a decimal comma) and the duty's legs and climb from route_register_2026.xlsx; ambient dropouts took the Jönköping station day from daily_mean_temperature_2016-2026.csv.
2. Fitted each duty-day's battery energy by least squares on km, climb times km, the degrees below 16 C and below 0 C times km, and payload times loaded km; on the declared weights the payload term is 1.0 kWh per tonne per 100 km, and the model predicts January and February 2026 held out within 2.4 per cent.
3. Applied at −5 C and each duty's planning load from weighbridge_varnamo_2024-11_2026-10.csv, that model orders 8 tractors (V02, V03, V05, V07, V09, V11, V16, V18), the reasonable but insufficient answer: the heavy duties come out at 440 kWh and V14 at 470 kWh.
4. Read the weighbridge (the last weighing of each CMR, net as gross less tare) against the declared weights shipper by shipper: right on average, but for Tenhult Möbler, Huskvarna Wellpapp, Gränna Dryckes, Lekeryds Byggvaror the weighed load regresses on the declared at 0.26 to 0.30, the dairy's notes carry one standard weight and Tabergs' carry its weighbridge ticket, so a slope fitted on the declarations is diluted wherever the declarations scatter around the load, and one pooled line over the weighbridge (0.94) carries the shippers' differences in load, not the clerks' error, and corrects it only to 1.1.
5. Replaced each pilot day's declaration by its expected weighed load given the shipper and the declaration (the shipper's weighed mean for the dairy, the declaration itself for Tabergs) and refitted: 2.2 kWh per tonne per 100 km; Tabergs' own days, whose declarations are exact, give 2.2 on their own.
6. Kept the second cold rate below 0 C: with one rate below 16 C the model fitted without January and February 2026 under-predicts their sub-zero days by 3.4 per cent, with both rates by -0.4.
7. Predicted each shortlisted duty on the January design day at its planning load and kept those within 459 kWh (FES-2 4.1 to 4.3): V02, V05, V09, V14, V16, V18, 6 tractors.

No other order survives: the model's held-out check cannot see the dilution because the held-out days carry the same declarations, so only the weighbridge, which weighs the same shippers' loads, measures it; every route that takes each shipper's declarations to the weighed load (a line per shipper, the shipper's mean, the exact shipper's days, a within-duty fit, either year, any cold form with a rate below 0 C) gives the same six duties, while the declared weights, one pooled correction and an average consumption on cold days order 8, 8 and 9.
