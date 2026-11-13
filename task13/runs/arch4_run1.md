# task13 architecture 4, platform run 1 (pasted by the author on 2026-11-12)

The author pasted the platform's single run on architecture 4 (Blue Earth Valley Power's automated loops, uploaded as
13.1.zip) together with the holistic audit that returned the build. The score was not pasted. This file records the
run's committed figures against the golden and its own words where it named an assumption or set a record aside; it
is a reading of the run, not a `/triage-runs` report.

## The audit (returned on determinism)

Two graded answers were not forced: the battery list (a temperature fit on non-summer tests puts RCL-20378 at
21.197 V, below the 21.2 V line, and pulls RCL-21490 and RCL-21236 under it too; nothing pinned the fitting window)
and the 2027 figure (the order's "as they stand" left the four 2027 reconductors, cold battery failures, the L05 load
and the 80 per cent range open; the build's own variants 24,394 and 29,666 fell outside its 24,784 to 26,551 band).
The reviewer offered pins (a fitting basis in the design basis; a paste-ready forecast basis in the prompt). The
author chose a re-root over pins.

## The run against the golden

| Result | Golden | Run | Reading |
|---|---|---|---|
| R1 restored within five minutes, 2022 to 2026 | 32,875; 25,796; 28,781; 22,561; 25,508 | the same five figures | landed |
| R2 2026 avoided on the commission's definition | 21,780 (less 2,407 undone, less 1,321 receiving) | 21,780 (the same walk, 2,407 and 1,321) | landed |
| R3 controls to re-battery | 16 (14 to 17 with RCL-20188, RCL-21643, RCL-21281 at the line) | 17: the golden's 16 plus RCL-20378 | landed but for one control the audit found unforced |
| R4 receiving harm June to September 2027 | 381 (311 to 445) | not computed as asked (a thermal screen of 47 of 88 transfer scenarios) | missed |
| R5 2027 avoided as the loops stand | 25,741 (80 per cent 18,889 to 32,894) | 23,683 (80 per cent 16,352 to 31,361) | missed, and the audit found the band unforced |

Every result that priced the build on paper (the storm overflows read from the device record, the receiving trips
netted, each battery carried to -27 C) was made unprompted: the run rebuilt the lockouts from SCADA, removed 1,092
archive replays, linked 11 load-related repeat trips and fitted each battery installation's ageing with a temperature
term. The world was spent; architecture 5 moved to a new world, dataset and shell (`DESIGN_NOTE.md`, Tried and rejected).

## The run's own words (added to precedents.json)

- Reflex: "Converted ADMS UTC timestamps to fixed CST and reconciled OMS civil times to SCADA. All 588 lockouts
  matched OMS records ... Delayed storm entries and the fall-back-hour ambiguity were resolved using physical SCADA
  evidence rather than trusting the OMS start minute."
- Named assumption: "Airport ambient proxies cabinet temperature, and resistance measured at 5 A is extrapolated to
  30 A. These assumptions justify proof testing, especially near the cutoff."
- Named assumption (a second record set aside): "Read the AMI daily aggregates but excluded them from interruption
  attribution because they lack customer-level identities and minute-level event timing."
