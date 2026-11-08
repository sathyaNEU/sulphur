# task3 architecture 2, platform runs (reported by the author 2026-11-08)

Scores were not reported; the author's word: "they were not stumped, model found exact ground truth". Both runs
match the golden on the call and on every graded ask figure.

## Response 1 (130 resources, 45 min)

- Call: Alternative C, 38 MG with 45 MGD firm dewatering, 2.9 events a year, USD 128.5 million; A 9.7, B 6.8,
  D 1.3 (116, 82, 35, 16 events over 2014 to 2025).
- All 48 rainfall cells (RG-1 to RG-4, local Eastern months 2025) and the five Northside returns (261, 214, 300,
  302, 372 MG) identical to the golden.
- Method: the older meter's cfs to MGD, logger clocks to UTC, 693 overlapping zero rows dropped; continuous storage
  replay with withdrawal bounded by stored water, firm pump capacity and 140 MGD less concurrent Southside
  influent; 17 BAD plant hours interpolated; rain tips de-duplicated, calibration bursts removed, the July bucket
  changes applied; Northside returns from the 50-point stage-storage curve with the 0.45 ft remount offset.
- Rejected explicitly: ignoring plant headroom ("incorrectly gives B 2.8 events/year"), resetting storage at each
  pulse, uncorrected rainfall, nominal pump runtime for returns.

## Response 2 (102 resources, 48 min)

- Call, every alternative's events, all 48 rainfall cells and the five returns identical to Response 1 and the
  golden; the headroom constraint stated as the reason B fails.

## Diff against the golden

No cell differs. Both runs bounded the dewatering by the receiving plant's hour-by-hour headroom without being
asked: the plant historian sat in the pack and the constraint read as plain physics once the return point was
filed at the Southside headworks.
