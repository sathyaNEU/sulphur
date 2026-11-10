# task4 architecture 7, platform run 1 (summary)

SUMMARY, not the run's own text. Written on 2026-11-09 from the author's account of the run in the parent
conversation (the full text was supplied there, not to the repo). Pack: target.zip 76adf383c1395b39.

## Method, as the run filed it

- Cleaned every file: the twice-uploaded days, the ambient dropouts (station-filled), the three declared-weight
  formats, the re-weighed CMRs, the VMO-nn duty codes.
- Payload: took each pilot declaration to its weighed equivalent from the Värnamo weighbridge, shipper by shipper
  (regression calibration). Filed 1.98 kWh per tonne per 100 loaded km (golden 2.1, band 1.9 to 2.1): earned.
- First-year battery loss from energy per full charge on age, temperature and tractor: 3.75 per cent (golden 3.8,
  band 3.6 to 4.0): earned. Limit about 442 kWh.
- Cold: a curved sub-zero form on the pilot: earned.
- Speed: added the square of speed to the energy model and fed each Värnamo duty the routing tool's planned speed
  (round-trip km over the register's driving time), fitted against the pilot's own routing-tool speeds, which
  absorbs the year's average actual-to-planned ratio (the design note's "year's ratio" shortcut), not the ratio on
  a -5 C day.
- Design-day energies: 12 of 14 inside the 10 kWh band; V05 and V18 about 15 kWh high.

## Call and loss

- Ordered 5 (V02, V05, V09, V16, V18), V14 excluded at 444.4 kWh against a limit near 442 kWh (golden V14 435.4).
- The whole loss sat on one duty by 1.2 to 2.6 kWh, through the winter actual-to-planned speed ratio.
- Offered a cubic-temperature model as a defensible alternative under which V14 would qualify.

## Class

Method shortcut on the speed transfer (the year's ratio), one legitimate step; both runs lost in the same place.
