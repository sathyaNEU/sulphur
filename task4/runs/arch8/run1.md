# task4 architecture 8, platform run 1 (summary)

SUMMARY, not the run's own text. Written on 2026-11-10 from the author's account of the two architecture 8 runs in
the parent conversation (the full texts were supplied there, not to the repo). Pack: architecture 8's target.zip
(commit 50d36a3).

## Method, as the author reported it

The author's account gave the two runs' scores on the golden's figures separately and their methods and written
assumptions for the recorded runs together; the methods below are not attributed run by run beyond that account.


- Read every file and cleaned it: the twice-uploaded days, the re-weighed CMRs, the kg and tonne strings, the
  ambient dropouts filled from the station, the trailer tares reconciled to the registers, the legacy VMO-nn codes.
- Payload: per-shipper regression calibration of the declared weights on the Värnamo weighbridge. Filed 2.24 kWh
  per tonne per 100 loaded km (golden 2.2). Computed a duty-fixed-effects payload slope (2.80) and set it aside in
  favour of the pooled figure, naming it "material model uncertainty".
- Joined each day's trailer to the fleet register for the combination's tare, unloaded each multi-drop load at its
  stops, and told the ePTO fridge units from the other reefers by the equipment column.
- Because the ePTO unit draws by the hour, modelled each duty's elapsed time on the design day ("predicting timing
  as well"), which carried the winter actual-to-planned speed into the forecast.
- Nonlinear temperature; squared speed; battery capacity from energy over SOC depletion with age, temperature and
  tractor effects, checked year over year and on the first year only: 3.78 per cent (golden 3.8).
- Validation: leave-one-duty-out, later-period and month holdouts; a date or week block bootstrap.

## Call

- Order 7: V03, V05, V09, V11, V16, V18, V33, the golden exactly; every energy within about 3 kWh of the golden's.

## Untested assumptions the run wrote down

"Target routes are longer and faster in routing terms than the pilot routes, so the forecasts involve
extrapolation"; "Shipper calibration transfers between depots... no measured Jönköping payload sample directly
verifies it"; "Actual drop shares follow declared shares; individual drop weights are not measured"; "Elapsed time
proxies ePTO runtime"; "assumes no unrecorded battery replacement, SOC-buffer or metering change".

## Class

None: landed. Every architecture 8 step was one join to a register the run already read.
