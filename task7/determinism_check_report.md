# Determinism check, task7 (2026-11-13 re-judge after the holistic check: Sequence replayed, Stagger sampled)

**Verdict:** DETERMINISTIC on the figures and the call, with one convention open (Sequence's queue, below).
**Disposition:** FIX_NOW: add the convention sentences listed under Findings 2 to 4. No prompt or pack change.

Correction to the first draft: my Stagger script applied the 0.95 divisor twice and clamped pre-July blocks onto quarter 0; the Stagger figure below is the corrected replay. The earlier 42.8 was my error, not the blocks'.

## Method
Fresh unzip. Enrolled = roster with exact duplicate rows dropped, status Active = 1,313 (reproduced). Transformer = GIS, with the 8 service transfers applied (4 GIS rows are stale, e.g. SB-9120 vs SB-3307). Nameplate = register with the change-outs applied (PH-8321, PH-5606, PH-6534 are stale in the register). MDM reads de-duplicated (120 re-sent rows); meters mapped to service points with the AMI exchanges (no overlap or gaps remain). Local = UTC-6: the only offset where the sessions line up with the MDM charging hours; no shipped text states it (weather file says "lst", UTC-7 gives Sequence 77). Base per transformer = homes' hourly kW minus the 1,313 enrolled chargers' recorded charging, x peaking factor per quarter-hour, plus option charging at constant energy/charge-time in its quarters, /0.95, against 1.2 x kVA, July-August max. Zero-energy sessions dropped.

## Evidence
| Figure | Block | Replay |
|---|---|---|
| Enrolled chargers | 1,313 | 1,313 |
| Transformers with metered 2026 loads over | 44 | 44 |
| Sequence over (literal queue, below) | 13 (12 to 14) | **13** |
| Stagger expected over | 29.7 (28.5 to 31.0) | **29.5** (100 draws, all 381 transformers with sessions, limit 1.2 x kVA, blocks at their true quarters, pre-July bins dropped; 11 transformers over on every draw, 27 above 50 per cent, 47 with chance strictly between 0 and 1) |

Replay used 381 transformers with sessions, blocks say 382 (one enrolled charger has no July-August session; immaterial to options).

## Forks run on Sequence (count over)
- Literal rule (queue waits for every charger before it, including a late charger started alongside; start on quarter-hour, rounded up): **13**. Closed by the proposal xlsx sentence "each starting when every charger before it in that order has finished".
- Late charger NOT waited for by the queue: **7**, outside the band. Only the proposal's wording closes it ("every charger before it"); a reasonable analyst reading "alongside whichever are charging" as outside the queue lands on 7. Add a stated convention to the blocks, and ideally the prompt/pack cannot add one (proposal is a shipped file), so this stays FIX_NOW as an explicit convention line in Step-by-Step.
- Start rounded nearest or not at all, queue cursor not rounded, late start not clipped to plug-in, drop the 30 June night: all **13**.
- Ready-by = unplug rounded to nearest: 12; rounded up: 13. Closed by EV-4 4.1 (round down).
- Ready-by = the member's recorded ready_by_local (present on Stagger sessions only): 10, outside the band. Closed by EV-4 4.1 ("unplug time rounded down"), not by the sessions file; keep that sentence in the blocks.
- Charge time = energy / peak_kw: 15, outside the band. Closed by EV-4 4.1 ("the time its charge took", the recorded start to end); say so.
- Charge time = energy / rated kW: 13.
- UTC-7 clock: 77. Closed by data only (sessions align with MDM at UTC-6); no sentence states the zone.

## Findings
1. Stagger 29.7 reproduces (29.5, inside 28.5 to 31.0) once my two script errors are fixed. No finding.
2. Sequence's queue reading: 13 vs 7 on whether a late-started charger holds up the ones behind it. Add to Step-by-Step 6 and Critical Component 2: "a charger started at its latest start still counts as ahead of every later charger in the queue".
3. Local clock (UTC-6) is nowhere stated; derivable from the data only. Low risk (UTC-7 is visibly broken), but one sentence in Step-by-Step 3 closes it.
4. Replacement cost for Sequence's 13 and the crossover were not recomputed here (cost table mount mapping not run); the count is the driver.

## Disposition carried out (main thread)

FIX_NOW applied in the answer blocks (generator/writeup.py, submission.md regenerated from figures.json): Step-by-Step 3 states the clock (local daylight time, six hours behind UTC, where the sessions line up with the charging in the hourly reads; fork row SF26, asserted from the data); Step-by-Step 6 states that each session draws its energy over its recorded charge time, that the ready-by is the unplug time rounded down to the quarter-hour, and that a charger started late at its latest start counts ahead of every later charger; Critical Component 2 says every later charger waits for it too. No prompt or pack change. Shipped without another judge, as /fix-determinism step 6 sets out.
