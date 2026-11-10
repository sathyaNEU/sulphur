# task4 architecture 8, platform run 2 (summary)

SUMMARY, not the run's own text. Written on 2026-11-10 from the author's account of the two architecture 8 runs in
the parent conversation (the full texts were supplied there, not to the repo). Pack: architecture 8's target.zip
(commit 50d36a3).

## Method, as the author reported it

The author's account gave the two runs' scores on the golden's figures separately and their methods and written
assumptions for the recorded runs together; the methods below are not attributed run by run beyond that account.


- The same cleaning battery as run 1 (uploads, reweighs, weight strings, station-filled temperatures, tares
  reconciled to the registers, legacy duty codes).
- Payload: per-shipper regression calibration on the weighbridge, 2.23 kWh per tonne per 100 loaded km (golden 2.2);
  the duty-fixed-effects slope computed and dismissed for the pooled one.
- Trailer tare on every leg, loads unloaded at the drops when the stop data existed, ePTO units read from the
  equipment column and their draw carried by elapsed time, so the design day's timing (the winter speed) entered the
  forecast.
- Battery capacity from energy over SOC with age, temperature and tractor effects, with year-over-year and
  first-year-only checks: 3.79 per cent (golden 3.8).
- Holdouts by duty, later period and month; block bootstraps by date or week ("Bootstrap intervals preserve
  within-day dependence but not serial dependence").

## Call

- Order 7, the golden's duties; every energy within about 3 kWh.

## Untested assumptions the run wrote down

The same list as run 1, with "the duty-fixed-effects specification estimates 2.80... material model uncertainty".

## Class

None: landed.
