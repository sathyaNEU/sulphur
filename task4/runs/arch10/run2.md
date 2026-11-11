# task4 architecture 10, platform run 2 (target.zip from commit 0c3b7fc, pasted by the author 2026-11-11)

Reviewed 87 resources, about 29 min.

Recommendation. Order 17 battery-electric buses for Niittyla's 2027 weekday blocks, assigned to the first 17
battery-qualified blocks in fleet-plan priority order. Those buses require 6.619 MWh on the design night and a managed
peak of 662.80 kW, below the 690 kW connection limit; adding the next qualifying block requires 7.003 MWh, exceeding the
night's 6.900 MWh maximum.

Order and assignments: M108, M107, M148, M101, M146, M119, M113, M140, M122, M137, M142, M116, M134, M123, M129, M125,
M135. First charging-constrained block M145 (priority 29); M124, M103, M139, M105 and M118 also stay on diesel; 25
blocks fail the battery test. Purchase price EUR 9.316 million; "This is not an 11-bus net order: the six existing pilot
buses transfer to Kauppala on 11 January 2027."

Forecasting blocks without electric history: "36 of the 48 weekday blocks have no electric operating history. Their
forecasts use a transferable model fitted to 3,291 distinct electric bus-days across 49 blocks, combining
diesel-service intensity and scheduled kilometres for non-HVAC energy, then adding temperature- and duration-dependent
electric heating. Holding entire blocks out of training gives 8.52 kWh traction-energy RMSE."

Every block: both a diesel-service denominator and a mixed-fleet denominator reported; diesel-service L/100 km within
0.2 of the golden on every block; design-day kWh 292.88 to 496.34, the same 23 qualifying (table in the run's
Block Decisions sheet: M108 51.51, 292.88; M107 51.94, 362.85; M148 59.28, 346.73; M101 58.05, 362.08; M146 50.45,
334.41; M119 62.65, 364.06; ... M117 44.09, 446.74).

Permanent first-year battery loss: 4.39%, conditional 95% interval 4.31% to 4.47%; 458.93 kWh usable; 390.09 kWh limit.

All-qualifying design-night connection demand: 9.069 MWh, "including conversion losses and charger-fed thermal
demand"; battery energy 7.982 MWh.

Step-by-step (condensed):
- Governing rules and registers read; distractors reviewed and excluded.
- "Fitted interval litres using the scheduled kilometres of constituent block-days, with block, vehicle and temperature
  effects. The fit used 5,961 complete intervals and achieved 6.57 L per interval RMSE."
- "Fitted non-HVAC energy using distance and diesel-service intensity without block-specific electric effects. Traction
  fit RMSE is 8.44 kWh; whole-block-held-out RMSE is 8.52 kWh."
- "Workshop failures identify 26 bus-days for vehicle 1202 ... and 22 bus-days for vehicle 1205 ... The fitted design-day
  electric HVAC demand is 12.37 kW ... Excluding either outage episode gives 12.42 kW and 12.36 kW."
- "Fitted a weighted age curve anchored at the known new usable capacity, with a separate reversible temperature term.
  This gives 4.39% permanent first-year loss. An alternative quadratic age model gives 4.54%."
- "Converted charging timestamps from UTC to Europe/Helsinki ... The charging model includes learned conversion losses
  and 22.63 kWh of design-night thermal demand per bus. Fit RMSE is 4.46 kWh per session; the forward test gives 3.76
  kWh."
- "The scheduling model conservatively caps each bus at 150 kW connection-side draw including auxiliaries ... The
  selected 17 buses fit at 662.80 kW; adding M145 requires 701.48 kW."
- "A +5% energy stress permits only 16 buses; -5% permits 18."

Assumptions and judgment calls (verbatim):
- Diesel denominator: Diesel-operated scheduled kilometres are the primary business-case denominator. The workbook also
  reports the literal mixed-fleet denominator.
- Fuel inventory: Depot refills outside active service are assumed to restore comparable tank levels.
- Heating transfer: Pilot heater failures are an operating-record proxy for the new bus's fully electric heating.
  Comparable cabin comfort and heating duty are assumed; the new hardware is not proven identical.
- Battery inference: The loss estimate comes from energy/SOC records, not direct workshop SOH measurements. Its
  confidence interval is conditional on the selected model.
- Charging control: The schedule assumes managed, adjustable charging.
- Decision basis: DES-1 uses the central forecasts and the mandatory priority sequence.
- Delivery timing: The quoted buses arrive in August-September, not at the January timetable change.

Alternatives rejected (condensed): all 23; 18 in priority order (7.003 MWh and 701.48 kW); skipping M145; an 11-bus net
order; distance alone for electric demand (20.40 kWh RMSE); pilot winter consumption without the heating correction;
winter capacity reduction as permanent fade; "depot invoices, transformer capacity, workshop outlets or daytime charging
to enlarge the order".
