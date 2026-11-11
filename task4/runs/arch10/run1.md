# task4 architecture 10, platform run 1 (target.zip from commit 0c3b7fc, pasted by the author 2026-11-11)

Reviewed 122 resources, about 1 h.

Recommendation. Order 17 battery-electric buses for Niittyla's 2027 weekday blocks.

Of the 48 blocks, 23 qualify against the 390.18 kWh battery-energy ceiling, but only the first 17 qualifying blocks can
be recharged in fleet-plan priority order. Their design-night connection demand is 6.516 MWh; charging all 23
qualifying buses would require 8.923 MWh, exceeding the 6.900 MWh overnight ceiling.

Final answers. Niittyla_2027_Block_Assessment.xlsx and Niittyla_2027_Board_Briefing.pptx.

Order and assignment: the 17 buses, in priority order, to M108, M107, M148, M101, M146, M119, M113, M140, M122, M137,
M142, M116, M134, M123, M129, M125 and M135.

Estimating blocks without electric history: only 12 weekday blocks have electric observations; 36 do not. "I used
reconstructed diesel demand, scheduled kilometres and full block hours to predict non-HVAC battery energy, then
replaced the pilot buses' fuel-assisted heating with an internally observed electric-heating estimate.
Leave-one-block-out prediction RMSE is 8.09 kWh, versus 21.05 kWh for a kilometres-only model."

Every block (diesel L/100 km; design-day kWh; verdict), in priority order: M108 51.65, 289.2, qualifies, assigned;
M107 51.96, 358.0, assigned; M148 59.32, 340.9, assigned; M101 58.03, 354.1, assigned; M146 50.48, 329.9, assigned;
M119 62.60, 357.3, assigned; M113 52.35, 336.8, assigned; M140 53.58, 313.1, assigned; M122 62.21, 354.7, assigned;
M137 52.57, 351.1, assigned; M111 58.63, 416.8, no; M142 50.23, 307.3, assigned; M116 58.63, 350.9, assigned; M106
60.72, 411.1, no; M134 50.96, 309.8, assigned; M132 59.37, 408.8, no; M123 52.96, 315.4, assigned; M141 55.86, 430.7,
no; M129 46.88, 361.4, assigned; M112 51.31, 430.6, no; M120 46.39, 425.3, no; M131 52.07, 427.5, no; M125 45.44,
358.7, assigned; M115 50.59, 415.1, no; M127 51.82, 479.1, no; M144 48.85, 414.1, no; M135 42.91, 336.8, assigned; M114
46.21, 413.8, no; M145 43.83, 333.1, qualifies, deferred by charging constraint; M128 49.45, 412.3, no; M124 48.46,
359.4, deferred; M103 44.91, 356.2, deferred; M139 51.14, 355.7, deferred; M126 45.97, 418.8, no; M104 42.69, 421.6,
no; M130 41.24, 447.1, no; M109 38.48, 489.2, no; M102 38.81, 431.0, no; M121 40.94, 431.1, no; M136 43.92, 477.1, no;
M147 38.73, 422.1, no; M138 40.49, 423.3, no; M105 39.39, 357.9, deferred; M110 37.38, 455.6, no; M133 40.06, 469.1,
no; M118 42.17, 359.4, deferred; M143 39.11, 476.7, no; M117 44.09, 438.0, no.

Permanent first-year battery loss: 4.37%, 95% interval 4.29% to 4.44%; 459.03 kWh usable, 390.18 kWh ceiling.

Design-night connection demand with every qualifying block on charge: 8.923 MWh, "including charging losses and
session thermal/auxiliary demand"; battery replenishment 7.847 MWh.

Step-by-step (condensed, the run's own words where quoted):
- Read all 14 files; governing documents DES-1, the agreement, the quotation, the fleet plan.
- Distractors inspected and excluded (whole-depot invoices "whose baseload cannot be treated as charging-installation
  demand"; tyre and brake costs).
- Identities normalised (2,460 registration aliases, 23,684 old block codes); zero duplicates or mismatches.
- "Reconstruct diesel consumption between refills ... Combined 191 split depot refills ... Intermediate external
  purchases were pooled through the next depot refill."
- "Fitted nonnegative block rates using 5,987 completed refill intervals touching the reporting year, covering all 96
  block types ... Held-out-quarter RMSE was 9.140933 litres, versus 12.928615 litres for distance-only allocation."
- Telemetry de-duplicated (24 rows), 93 missing temperatures filled from the airport.
- "Separate ageing from reversible cold effects ... The selected front-loaded-plus-continuing decline model had 5.44 kWh
  RMSE on the May-onward holdout, versus 9.53 kWh for constant linear decline. A 500-replicate whole-week bootstrap."
- "Workshop records identified 46 clean heater-outage bus-days; 13 observations on 11 dates were at airport
  temperatures at or below -10 C. These yielded 11.84 kW electric HVAC demand at the design temperature ... versus 8.14
  kW during normal fuel-assisted pilot operation."
- "Corrected charging sessions for actual SOC gain using smoothed capacity, then fitted mains energy against battery
  replenishment and cold-weather overhead. Leave-quarter-out RMSE was 3.90 kWh, versus 7.66 kWh for a constant-efficiency
  model."
- "Tested successive qualifying prefixes using exact return/departure intervals, the 21:00-07:00 relay window, 150 kW DC
  per bus and 690 kW at the connection. The 17-bus schedule reconciles fully. Adding M145 requires 6,895.54 kWh,
  exceeding its departure-limited charging opportunity of 6,893.81 kWh by 1.73 kWh."

Assumptions and judgment calls (verbatim):
- Refill inventories: Depot refill endpoints are assumed to have comparable tank stocks; the receipts do not explicitly
  confirm full tanks. Paired-interval, capped-endpoint and replacement-interval sensitivity checks are included.
- Heating transfer: Heater failures are the best internal evidence for no-fuel-heater operation, but comparable
  passenger comfort and 2027 equipment performance are assumptions. Cabin-temperature evidence is unavailable.
- Battery transfer: The pilots' temperature-adjusted first-year loss is applied to the quoted 2027 usable capacity.
- Charging behaviour: The feasibility model assumes controllable charging up to the specified power limit; no taper
  curve was supplied. Spreading auxiliary demand uniformly across charging availability still gives 17 feasible and 18
  infeasible.
- Extrapolation: Predictor-support warnings are shown block by block. Five assigned blocks exceed the observed
  diesel-proxy range.
- Uncertainty at the cutoff: The 18th-bus deficit is smaller than modelling uncertainty. Heating 10% lower permits 18
  buses; heating 10% higher, total block energy 5% higher, and battery-loss stresses of 4.0%-5.0% retain 17.

Alternatives rejected (condensed): all 23 (8.923 MWh over 6.900); 18 by total energy (deadline-limited opportunity);
pilot winter consumption unchanged ("would classify 38 blocks as qualifying and produce a misleading 19-bus order");
a fleet-average kWh/km; fill-day attribution; charger energy for capacity or depot bills for charging.
