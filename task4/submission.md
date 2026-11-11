# task4: Saarnela's 2027 peak, the evening shifts and the agency booking

## Tags

**Domain:** General Statistics & Data Science, Regression, classification & model diagnostics (a third-party fulfilment centre's peak labour plan: forecasting each pick zone's picker hours once a second brand shares its zones).

**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

Agree the evening shift in weeks 47 to 50 in both small-parts zones, P1 and P2, and book 8,390 agency picker hours over the 2027 peak (760, 1,910, 1,930, 1,760, 2,030 in weeks 46 to 50); week 46 runs on day shifts alone. Not the draft plan's route (the client's budget as issued over its pooled overstatement, the 2025 peak's hours a line and the pilot's time a line), which opens the evening shift in week 48 in both zones only and books 5,320 hours: it plans 2027's day shifts at 2025's crowding though the limit puts 24 and 22 pickers on the floor, Huippu Sport at its polybag pilot, Kotikaari at an overstatement its modest 2027 plan does not carry, and Black Friday a week late.

## Supplementary Questions

### saarnela_peak_plan_2027.xlsx

The workbook has five sheets: Plan (one row per ISO week 46 to 50 and pick zone P1, P2, B1: the lines expected, the day-shift capacity at the zone's limit, the evening-shift verdict, the picker hours with their 80 per cent range, the own pickers' hours and the agency hours, then the agency hours by week), Volumes (each brand's and group's weekly lines, the budget as issued beside the lines expected), Forecast record (each budget's overstatement against its plan's growth), Time a line (the task-time model and the congestion curve) and Routes (each shorter route's evening-shift weeks and agency hours).

1. Picker hours each pick zone will need, paid hours to the nearest 10 with the range put at 80 per cent (sheet Plan; each figure graded within 6 per cent, each range end within 8 per cent): week 46 P1 780 (710 to 880), P2 690 (620 to 780), B1 490 (460 to 520); week 47 P1 1,300 (1,230 to 1,360), P2 1,200 (1,150 to 1,260), B1 610 (570 to 660); week 48 P1 1,320 (1,250 to 1,390), P2 1,220 (1,160 to 1,280), B1 590 (550 to 630); week 49 P1 1,140 (1,090 to 1,200), P2 1,060 (1,010 to 1,110), B1 520 (490 to 560); week 50 P1 1,360 (1,290 to 1,430), P2 1,250 (1,190 to 1,310), B1 610 (580 to 660).

2. Agency picker hours to book on top of the own pickers, to the nearest 10 (sheet Plan; each graded within 7 per cent): week 46 760; week 47 1,910; week 48 1,930; week 49 1,760; week 50 2,030; 8,390 over the peak.

3. Whether each small-parts zone needs the evening shift: P1 in weeks 47 to 50, P2 in weeks 47 to 50; neither in week 46, where the day shifts pick the week's lines below the limit (P1 at 0.85 and P2 at 0.87 of the day shifts' capacity at the limit).

4. The share by which Kotikaari's year-ahead forecasts of its peak weeks have overstated the order lines it placed in those weeks: 10.0 per cent (graded within 8.8 to 11.6), the October budgets' order lines over weeks 46 to 50 of 2022 to 2025 against the order lines the WMS's order import records for those weeks, both groups.

5. How much longer a Huippu Sport order line will take to pick than a Kotikaari one in the small-parts zones in the 2027 peak: 0.13 minutes of task time (graded within 0.09 to 0.16), 0.97 against 0.85.

### saarnela_peak_plan_2027.docx

6. One page for the management team: the recommendation (the evening-shift weeks by zone and the agency hours by week), a table of each week's picker hours by zone with the ranges, the verdicts and the agency hours, one chart of each small-parts zone's weekly lines against its day-shift capacity at the limit, and the drivers the plan rests on beside the draft's result.

## Critical Components

1. Aisle congestion, measured with the line mix held fixed: a line takes **0.46 minutes** longer at 1.8 pickers logged in an aisle than on an empty floor (graded within 0.40 to 0.51), on the WMS zone hours' task minutes regressed on lines by handling class, extra units, zone and a convex term in pickers per aisle (the aisles as the standard gives them before and after January 2024). The 2025 peak's day shifts put 1.15 pickers on the floor an aisle, against the two an aisle of 2027's day shifts at the limit, so its hours a line understate 2027's.

2. The 2027 budget's expected overstatement: **3.7 per cent** for Kotikaari small parts (graded within 2.6 to 6.1), against the pooled 10.0: the October budgets' overstatement over their whole year grows with the commercial plan's growth (2022 bulky 8.8; 2022 small parts 15.5; 2023 bulky 0.8; 2023 small parts 3.0; 2024 bulky 1.0; 2024 small parts 14.0; 2025 bulky 8.8; 2025 small parts 5.5), and the 2027 plan is 7 per cent; Huippu Sport's 26 per cent plan points to 14.1 per cent.

3. Black Friday's week: **21.4 per cent** of the 2027 peak's Kotikaari small-parts lines fall in week 47 (graded within 20.2 to 22.7), against the budget's 14.0: the budget phases 2027 by 2025's week numbers, 2026 has 53 ISO weeks, and Black Friday moves from week 48 in 2025 to week 47 in 2027 (26 November).

4. The 2025 peak's picker hours as the payroll records them: **3,384** in P1, **3,104** in P2 and **2,280** in B1 (weeks 46 to 50, worked hours, graded within 1 per cent), with 0.921 of each paid day-shift hour logged in to a zone.

## Step-by-Step

1. Conform the records: the old payroll export (semicolon, decimal commas, cost centres 4111 to 4150) onto the new one, its March 2024 correction run dropped, packing hours left out; the WMS zone hours exported twice on three dates de-duplicated; pickers logged per aisle with the standard's aisles (8 and 7 before 8 January 2024, 12 and 11 after); the 2025 peak's picker hours come to 3,384, 3,104 and 2,280 (component 4).

2. The forecast record (ask 4): the October budget rounds of the archive, the latest issue of each week, against the order lines Kotikaari placed in the same weeks (the order import): 10.0 per cent over the peak weeks of 2022 to 2025. The lines picked in those weeks run lower (the dense peaks' backlog spills into week 51), and the latest rolling forecasts land within a few per cent and say nothing about the year-ahead lead.

3. The budget's overstatement against its plan (component 2): over each year both groups' overstatement rises with the plan's growth (a log-log fit through the eight budget-years); the 2027 plan of 7 per cent for Kotikaari small parts gives 3.7 per cent, not the pooled 10.0, which would take out lines the modest plan never added.

4. The weekly profile (component 3): 2025's orders by day, moved 728 days onto the same weekday of 2027 (Black Friday 28 November 2025 onto 26 November 2027), released by the standard's rule on 2027's working days and scaled to the budget's growth over 2025 less the expected overstatement: week 47 carries 21.4 per cent of Kotikaari's small-parts peak, not the budget's 14.0; Huippu Sport's own daily orders re-keyed the same way.

5. The time a line (component 1, ask 5): the zone-hour regression gives each handling class's minutes, 0.108 a unit after the first and 0.062 for a Huippu Sport line, with congestion 0.46 minutes at 1.8 pickers an aisle; a fit without the density term returns impossible class rates, and a straight-line density term fits four times worse. Huippu Sport's peak mix comes from its article lines of November and December 2025 with the item master's classes and the slotting's zones: 0.97 minutes a line against Kotikaari's 0.85, +0.13; the pilot's own lines (0.73 against P2's 0.82, all polybag apparel) give -0.10.

6. The plan (asks 1 to 3): each zone-week's lines against what the day shifts at the limit can pick at the week's time a line with the congestion each hour's pickers give (the logged share by hour from the 2024 and 2025 peak days); P1 and P2 exceed it in weeks 47 to 50 by 1.17 to 1.30 times and week 46 stays at 0.85 and 0.87, so the evening shift opens in weeks 47 to 50 and the day shifts run at 24 and 22 pickers.

7. The ranges and the agency (asks 1 and 2): the range carries the budget's residual error at the year-ahead lead (0.021 on the log scale), the re-keyed profile's weekly error (0.047, 2024 onto 2025) and the model's (0.004), through the floor's own congestion; the agency books every hour above the own pickers' planned hours less the 2025 peak's sickness absence: 8,390 hours.

8. The draft's route, the budget as issued over the pooled 10.0 per cent with the 2025 hours a line and the pilot's time a line, opens the evening shift in week 48 in both zones only and books 5,320 hours; put right alone, the calendar opens it in no week in either zone (6,150 hours), the calibration in P1 week 48, P2 weeks 48 and 49 (5,850), the congestion in weeks 48 to 50 in both zones (6,100) and Huippu Sport's mix in P1 week 48, P2 weeks 48 and 49 (5,840).

Why no other conclusion survives: the draft's route and every route that puts one judgment right land a different set of evening-shift weeks, because the four move the weeks in different directions: the 2025 rate holds only below the density 2027's day shifts run at, the pilot measured polybag apparel, the pooled overstatement belongs to budgets that planned more growth, and a week-numbered phasing after a 53-week year puts Black Friday in week 48. Aligning 2025's days to 2027's by date instead of weekday puts Black Friday on a Sunday and is ruled out by its own record (each year's spike falls on the Friday after the fourth Thursday of November); a straight-line or cubic congestion term fits the zone hours far worse; every defensible variant (a quadratic term, a flat logged share, the 2024 and 2025 profiles averaged, a linear calibration, one through the origin or on the peak weeks) keeps weeks 47 to 50, and so does each fitted input moved 20 per cent.
