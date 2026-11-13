# task20 architecture 4: triage of the first platform round (2026-11-13)

Both runs were pasted by the author without their scores (runs/arch4_run1.md, runs/arch4_run2.md). Each run is read
against the golden and the bands of the answer blocks, result by result. The estimates below use effort.json's
weights; they are the main thread's reading, not the platform's measurement.

| Result | Golden (band) | Run 1 | Grade | Run 2 | Grade |
|---|---|---|---|---|---|
| R7 the largest 2027 total that passes (Recommendation) | USD 250m (175 to 350) | 250 (257.42 before the steps) | Right | none feasible (-6.76) | Missed |
| R6 headroom at USD 500m (Component 1) | -123.3 (-163 to -85) | -131.23 | Right | -275.72 | Missed |
| R2 calls, funds with a first close, by half (Component 2) | 517.0, 211.7, 222.0, 172.6 | 521.76, 224.92, 219.92, 156.88 (H2 2028 below 160) | Partly | 515.27, 224.87, 234.12, 173.43 | Right |
| R3 calls, funds yet to close, by half (Component 3) | 0.0, 0.0, 63.7, 85.2 | 0.00, 0.00, 65.00, 87.52 | Right | 0.00, 92.83, 92.26, 86.16 | Missed |
| R1 commitments not yet called, by strategy (Ask 1) | 1,918.2 ... 524.6 | every strategy within 0.1 | Right | every strategy within 0.1 | Right |
| R4 distributions, by half (Ask 2) | 402.8, 280.2, 169.5, 198.4 | 402.80, 280.18, 169.51, 198.36 | Right | the same | Right |
| R5 net cash needs at USD 500m (Ask 3) | 1,060.7 (1,022 to 1,100) | 1,068.64 | Right | 1,213.13 | Missed |
| Estimated score (effort weights) | | | 96.0 | | 51.7 |

Average on the estimate: 73.9, above the bar of 60.

## Where each run went

Run 1 made every deep step unprompted: it separated deployment, follow-ons, support investments, recycling, fees and
the borrowing-line settlements, called USD 239.40 million of line-financed investment in the first stress quarter,
moved the pending funds' calls into 2028 on market-conditioned delays, and back-tested its structural call model on a
held-out 2023-24 window against an age curve. Its only miss is R2's last half-year cell (156.88 against a band that
starts at 160). It named and waved through two assumptions: "Weakly identified recycling fractions are pooled" (the
golden family's pooled recycling lands inside the band) and "Support during the deepest stress extrapolates beyond the
historical range". First wrong step: none that moves a result beyond R2's last cell.

Run 2 made J1 (the USD 239.40 million line stock repaid in the first stress quarter) and J2 (delayed support on a
two-quarter lag, held-out R squared 0.98) and lost J3: the four pending funds call from the second half of 2027 on
their managers' dates, so the existing commitments' calls are USD 1,419.0 million against the golden's 1,272.2, the
needs at USD 500 million are 1,213.1 and no budget passes. First wrong step: the pending funds' first closes taken on
their expected dates (dismissed own evidence; the register's slipped closes left unused). Its losses are the
factorial's J3-dropped answer (USD 50 million on the golden's engine, none on its own).

## Classes

Run 1: no deep-class loss. Run 2: one, dismissed own evidence (J3), carried into R5, R6 and R7.

## Verdict and route

LANDED by run 1. The three stumps of architecture 4 are reflexes from this round (J1 and J2 made by both runs, J3 by
run 1), so the stump factorial has no stump left and the scaffold cannot be repaired by a re-pointed step (CLAUDE.md:
a landed scaffold is never re-pointed). Route: REDESIGN, a re-root to architecture 5 with new deciding lessons and a
new decision form. The runs' moves go to precedents.json as R63 to R66, the two waved-through assumptions as N34 and
N35, run 2's loss as L46.
