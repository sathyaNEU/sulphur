# task4 architecture 9, platform run 1 (summary)

SUMMARY, not the run's own text. Written on 2026-11-10 from the author's account of the two architecture 9 runs
(the full texts were supplied in the parent conversation, not to the repo). Pack: architecture 9's target.zip
(commit af4ff11, 19b6bec945fc8f80).

## Method, as the author reported it

- Read every file and cleaned it: the twice-uploaded days, the re-weighed CMRs, the three weight formats, the
  station-filled ambient dropouts, the trailer tares reconciled to the registers, the legacy VMO-nn duty codes.
- Payload: per-shipper calibration of the declared weights on the Värnamo weighbridge, carried to each pilot duty's
  own declarations; filed 2.00 kWh per tonne per 100 loaded km (golden 1.9, band 1.7 to 2.4): earned.
- Battery loss: energy per full charge on age with tractor and temperature effects, a square-root-of-age form chosen
  over the straight line; filed 5.08 per cent (golden 4.6, band 4.2 to 5.6): earned.
- Winter speed: "a separate winter driving-time model translates routing-tool time into expected actual speed",
  fitted on the pilot's actual-to-planned ratio against temperature and read at -5 C: earned.
- The combination's tare from the trailer register on every leg, each multi-drop load unloaded by pallet share at
  its stops, 400 weekly block bootstraps for the bands.

## Call

- Order 8: V02, V03, V05, V09, V11, V14, V16, V18, the golden exactly.

## Class

None: landed. Each of the three estimates the design priced as a step the runs had named and not taken (the
calibration's transfer to the pilot's part loads, the early-life loss, the winter speed) was a mechanism one file's
plot or one join across files carried, and the run modelled each on sight.
