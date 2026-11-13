# task22 architecture 1: the two platform runs read against the golden (2026-11-12)

Read in the build session's main thread against `submission.md` and the design note's results chain and effort test.
The author pasted both runs in full and reported that both landed the ground truth; the platform's scores and the
generated rubric were not pasted, so no score is recorded and the run-triage agent was not spawned.

## The call

Both runs: **LANDED**. Run 1: "Select CHL-2, APT-4, NTH-4, and CHL-3 ... fourth-ranked CHL-3 exceeds fifth-ranked APT-3
by 46.5 MWh." Run 2: "Prioritize CHL-2, APT-4, NTH-4 and CHL-3 ... CHL-3 leads APT-3 by 152.3 MWh." The golden sweeps the
same four (NTH-3 fifth at 502.7).

## Loss map, result by result (figures against the answer blocks' bands)

| Result | Golden (band) | Run 1 | Run 2 | Design's careful column |
|---|---|---|---|---|
| R1 energy in, gaps rebuilt | 14 feeders 248,001.4 (247,703.8 to 248,299.0); CHL-3 rebuilt from the delivery point | 248,001.8, gaps "using wholesale reconciliation"; earned | CHL-3's 249-hour gap rebuilt from the upstream balance (714.5 MWh); earned | Missed (N10) |
| R2 membership, switching replayed | NTH-4 374 and 441; metered use 9,377.7 and 6,707.5 | 124 switch operations replayed, pole tags matched beyond the crosswalk; earned | minute-level switching, two permanent and three temporary transfers; earned | Missed (N09, N14) |
| R3 lights' real use | 874.1 (839.1 to 909.1) | 874.4; earned | inventory, input watts and conversions; earned | Right |
| R4 technical losses | APT-3 1,786.6, APT-4 1,189.0 (7 per cent); 14 feeders 13,002.6 (4 per cent) | 14 feeders 12,717.7 earned; APT-3 about 1,588 (implied by its 655.6 residual), outside | APT-3 about 1,715 (implied), inside | Missed (L22, L36) |
| R5 non-technical loss | six feeders, bands of 75 MWh or 9 per cent | five inside; APT-3 655.6 against 381.6 to 531.6, outside | all six inside (APT-3 528.6) | Missed |
| R6 the rise bridged | technical +0.44, non-technical +0.30, else -0.24 (each 0.10) | +0.296, +0.470, -0.269: two parts outside | +0.342, +0.408, -0.250: the non-technical part 0.008 outside | Missed (L26, L27) |
| R7 new connections' peak | 521.6, 931.4, 541.2 (5 per cent) | 526.9, 940.9, 542.9; earned | 520.3, 931.2, 541.2; earned | Missed (L15) |
| R8 2027 technical losses | APT-4 1,720.9, APT-3 1,694.1 (7 per cent); 14 feeders 13,455.3 (3 per cent) | APT-3 1,489.5 outside; APT-4 and total inside | APT-4 1,941.6 outside; APT-3 and total (13,856.8) inside | Missed (N13, N01) |
| R9 the four | CHL-2, APT-4, NTH-4, CHL-3 | earned | earned | Missed |

First place each run departs from the golden on a graded figure: run 1 at R4, APT-3's technical losses (its other
demand placed "by monthly service-load shares"), a model detail inside a sound method (near miss); run 2 at R6, the
non-technical share of the rise 0.008 outside its band (near miss). Neither first wrong step is a deep class.

## What the runs did that the design priced as lost

Every judgment the effort test priced as a careful-column loss was made unprompted by both runs: the switching log
replayed on the network with the old device names matched by pole tag (R38), the breaker gaps rebuilt from the
delivery point balance (R39), technical losses computed hour by hour on the GIS at current loads with the 2019
study's percentage rejected (R40), the new loads' demand measured on the energized analogs with a site hold-out
(R41), the lights recomputed from the inventory (R42). The careful column priced at 20.8 (34.6 with R7 re-priced)
came back at about the thorough column. The cited precedents (N09, N10, N14, L15, L22, L36, N01, N13) came from packs
where the right move's data were absent or unlabelled; here each move's data were complete, labelled and the field's
textbook input, so each was a reflex.

What both runs named as an assumption and waved through, true in this world and so free: consumption calendarized
uniformly by day between reads (N20), unmetered load placed in proportion to metered load (N21), connections starting
on their scheduled dates (N22, run 1), nominal voltage and balanced phases (run 2).

## Verdict

**REDESIGN, architecture spent.** The average is not known but both runs landed the call and all but one or two
figures each; the losses that exist are near misses on model detail, not analytical. Every deciding step was a
field reflex, so no hardening inside this chain holds (a landed scaffold is never re-pointed), and the world goes with
it (one architecture per world). Re-root at stage 1 in a new world, with deciding lessons drawn from what these runs
waved through rather than from what they computed.
