# task24 determinism check (pass 2)

**Verdict:** DETERMINISTIC on the call and on the fork closed this pass; SOLUTION_WRONG suspected on the crowded-street (Vantorra) driver and cost figures, which I could not reproduce.
**Disposition:** FIX_NOW (answer blocks only; the author reconciles Vantorra's paid minutes against the generator, see Fix). Prompt and pack unchanged.

## Evidence (fresh unzip; independent simplified method: per-annotator multiplicative pace, first-pass and correction time fitted on 2026 task passes by size x occlusion, chain length from the blocks' reviews, paid/tool 1.18)

| Item | Blocks | Recomputed | Result |
|---|---|---|---|
| Shelfgrid paid minutes, contract-weighted (pricing policy s.3) | 38.8 (band 34.1-43.5) | 37.0-37.2 | reproduced |
| Shelfgrid, volume-weighted pace (old rival) | | 32.1-32.3 | outside band: the filed sentence closes it, contract weighting is the closer to the blocks |
| Vantorra paid minutes, contract-weighted | 54.4 (band 47.9-60.9) | 77.5 (stable across additive and multiplicative occlusion, 2.5x multiplier fitted) | NOT reproduced |
| Vantorra, volume-weighted | | 67.4 | NOT reproduced either |
| First-pass tool time on Vantorra's sample alone | | 43 min (about 51 paid) | exceeds the blocks' 54.4 total with corrections |
| 2026 calibration of the linear time model at 100+ objects per image | | observed 1,279 s against predicted 1,293 s (n=405) | model holds in 2026's densest bin, but Vantorra has 55% occluded boxes (28 small occluded per image) against 2026 projects' 5 to 40% |
| Vantorra cost if minutes are 77 (overhead 1.55 per paid hour) | 5.94 (5.58-6.30) | about 6.3 to 6.6 | likely outside the 6% band; call unchanged (decline, line 5.47) |
| Payroll total, three actuals, reviews 2.86 | reproduced last pass | unchanged | reproduced |

Rivals run this pass: contract- against volume-weighted pace (the 12% fork on minutes; the policy sentence "allotted a share ... in proportion to their contracted weekly hours" closes it, since contract weighting is what the blocks use and what lands Shelfgrid), equal weights (same as contract), additive against multiplicative occlusion (same). Calls: Vantorra and Brindle decline, others accept, under every variant I ran. The sentence closes the pace fork; every decisive fact (policy line, sample files, roster, size thresholds in QA-STD-03) is filed.

## Findings

1. Vantorra paid minutes 54.4 (and so its cost 5.94, its range, floor top-up 0.763, decline price 7.01) are not reproduced by the blocks' own Step 2 method on the shipped files: I get 67 to 77 minutes. A careful analyst following Step 2 would likely land outside the 12% minutes band and possibly the 6% cost band. The first-pass fit alone, on a sample with 55% occluded boxes, exceeds the blocks' total. Either the generator's Vantorra time uses a step the blocks do not state (a saturation at high density or a cap on the occlusion effect, which 2026's data at 27% occlusion do not show), or the figure is wrong.
2. Shelfgrid, Ardley-type and the other figures I checked are within the bands.

## Fix (solution, then pack only if the generator confirms a hidden step)

- Check Vantorra's minutes in the generator against a plain fit of first-pass and correction time on 2026 (size x occlusion, pace, contract weights). If the plain fit gives about 77 minutes, correct the paid minutes, cost, range, top-up and decline price for Vantorra (the call and the decline hold; the decline price rises to about 7.4 to 7.8). If the generator's 54.4 rests on a stated nonlinearity, state it in Step 2 and file the evidence in the pack (a 2026 project with occlusion above 50%); otherwise it is an unfiled fact (SEND_BACK).
