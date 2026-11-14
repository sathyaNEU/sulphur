# task20 determinism check, pass 6 (Gates A to E)

Scratch: /tmp/determinism-task20-p6/target (fresh unzip). Scripts: .../scratchpad/w6 (full.py, fac.py, fees.py, refi.py, fit.py, loans.py, short.py, head.py, forks.py).

**Verdict:** DETERMINISTIC. Program B, headroom about 210, reproduced end to end by the policy's own sentences.
**Disposition:** APPROVE (two optional wording notes under Fix; neither moves a figure or the call).

## Recomputed against the blocks (USD million)

| Figure | Block | Mine | Status |
|---|---|---|---|
| Reserve / spending | 2,778.7 / 791.0 | 2,778.7 / 791.0 | reproduced |
| Not yet called, by strategy and total | 1,614.4 / 443.5 / 223.7 / 581.0 / 1,169.8 / 474.0 / 4,506.4 | same; total 4,506.5 | reproduced |
| Distributions by half-year | 603.6 / 443.4 / 237.9 / 265.8 | same (pass 5, rates re-run) | reproduced |
| Facility balances, total | 316.1 | 316.1 (fund by fund, 22 funds, matches the sheet); audited borrowings alone 49.2 | reproduced exactly |
| New investments, 8 quarters | 1,134.8 | 1,134.9 (activity file at share, IP end quarter inclusive, years from first-close quarter, notinv = commitment less cumulative share) | reproduced (pass 5's gap was the cap and period treatment) |
| BO/GE/VC past IP: count, value | 32, 2,170.7 | 32, 2,170.7 | reproduced |
| Their calls (benchmark rate x 31 Dec value, capped at unfunded) | 278.4 | 278.4 with the cap (278.9 without) | reproduced |
| Benchmark call rates | 12.13 / 12.28 / 9.02 % | same | reproduced |
| Fees and expenses | 174.4 | 180.8 (latest statement, medians 0.5/0.05, 0.625/0.05 etc. match the sheet exactly; per-quarter 22.6 in H1 2027 gives the block's 45.2) | not to 0.5: gap 6.4 after cap in my order; later halves drift lower in the golden (45.1, 43.2, 40.9 vs my 46.1, 45.2, 44.6). The golden's order of applying the joint commitment cap across components (fees and refinancing calls competing for the same unfunded) is not filed. Effect on halves 1 to 3, inside every band |
| Seven successor closes and rule | 7 funds, 16 and 8 managers | rebuilt from the register: every early succession of the 16 stops at the quarter before the successor's first close; the 8 ran on, no exception; Q dates agree | reproduced |
| Successor effect | 131.6 | registered-ends reading 79.6 vs 78.1 (all-in headroom) | within 1.5 |
| 23 loans, balance at share | 23, 839.6 | 23, 839.6 (last loan record per asset, not realized) | reproduced |
| Past refinancings | 35, 5 lower, 26 since mid-2022 | 35, 5, 26; LTV table on sheet Asset loans reproduced row by row (value = prior-quarter valuation + loan replaced; 0.621, 0.508, 0.493 ... 0.692) | reproduced |
| Lenders' limit at 5.25 percent | 0.496 (cap 0.690, kappa 3.720, spread 2.25) | min(cap, kappa/(r+s)) by least squares since 2022Q3: 0.692, 3.693, 2.189 giving 0.4965; since 2020: 0.4987; the 10 refinancings at 4.9 to 5.6 percent average 0.4965 | limit reproduced; the three parameters are fit-dependent but the limit is not |
| Shortfall on the 23 loans | 279.5 | 277.1 (golden's 0.70 and 0.035; the Q1 factor read from the sheet) | within 1 percent |
| Value response | 0.70 equity (a quarter late), 0.035 per point | my regression on all loan-bearing assets' valuation plus loan: 0.749 and 0.023 | not rebuilt to the stated pair (population and dependent variable are not filed); shortfall 267.6 on mine, about +10 headroom, inside the band |
| Called within commitments | 254.9 (46.7/137.2/38.1/32.9) | 247.0 in total (cap applied after the other calls) | within 8 (3 percent); half-year split not rebuilt |
| Calls by half-year | 749.1 / 564.5 / 475.6 / 369.5 | 749.1 / 565.5 / 477.6 / 372.8 | all inside bands (741.2-756.0; 555.5-573.0; 468.1-482.1; 361.2-389.5) |
| Headroom before 2027 | 209.7 (187.5 to 223.4) | 211.2 | inside band |
| Re-up calls A / B | 291.7 / 119.2 | not rebuilt (call magnitudes carried; pace and fee medians reproduce) | A fails and B passes under every fork below |

## Forks run (headroom, program; B needs at least about 119, A fails below about 292)

| Reading | Headroom | Program | Ruling |
|---|---|---|---|
| Benchmark funds a year younger / older | 168.6 / 250.1 (block 167.1 / 248.5) | B / B | ruled out by "six or more years"; B anyway |
| Every period at its registered end (successor rule dropped) | 79.6 (block 78.1) | C | the block's named rejected reading; ruled out by named data (the register's 61 successions) |
| Successors' first closes slipped 1 / 2 quarters | 180.5 / 154.7 | B / B | ruled out by "the quarter its manager has given" (pending) and the plan's schedule; B anyway |
| BO/GE/VC periods extended 4 / 8 quarters, successor ends kept | 217.3 / 219.0 | B / B | defensible under "judged on the evidence"; inside band (block's own 195.5) |
| Facility from first investment, audits ignored | 167.6 (block 166.0) | B | ruled out by the section 8 sentence on the balance |
| Facility at the latest audited borrowings only | 465.3 | A | ruled out by the same sentence, and by named data (facilities drawn again in 2026) |
| Proceeds reinvested netted | about 243 (block) | B | ruled out: "no allowance is made for proceeds reinvested" |
| Cap at commitment removed | about 130.5 (block) | B (by 11) | ruled out by section 3: "no fund is taken to call more than the part ... not yet called" |
| Rate net of ordinary calls | 276.4 (block) | B | ruled out: "taken whole" |
| Fund fees on top of the rate | 141.0 (block) | B | ruled out: fees "are within the rate" |
| Pace over commitment not yet called | 224.1 (block) | B | ruled out by the definition; 0.7 above the band top, hence not a graded rival |
| Limit fit since 2020; value response 0.65/0.75 equity, 0.025/0.045 rate; my own response fit | 204 to 221 | B | defensible, all inside the band |

Defensible rivals alone or stacked (extended periods, limit fit, value response, pace average of ratios +9, cost-based fee +3) land between about 195 and 230: B every time, A needs 292. Stack of sentence-contradicting readings (a year younger, cap off, fees on top: about 20 headroom, program D) is reported, not a fork.

## Band check

Headroom 187.5 to 223.4, the four call bands, the strategy and distribution tolerances hold against every defensible rival and my rebuild. The 224.1 pace rival and the 167.1 age rival sit outside the headroom band but are ruled out by quoted sentences.

## Gates B, D, E

- Gate B: every term the call turns on is in a shipped file now (investments, commitment not yet invested, facility formation, fees, minimum reserve 1,170, cap). Not filed and used by the golden: (1) the order in which the commitment cap is applied across call types in a quarter (moves fees and the half-year split by 1 to 4, headroom by about 1); (2) the population and variable of the value-response fit (0.70/0.035 vs my 0.75/0.023, about 10 of headroom); (3) the 31 December to first-quarter factor of an asset's value, which the sheet implies (-1.5 percent at the Q1 maturity) but a stated response does not give; (4) the quarter lag of the rate effect. None leaves a graded figure's band or the call.
- Gates D and E: the asks name the program, the headroom, calls and distributions by half-year and the unfunded by strategy, each with a unit. The program set (A to D) is in the pacing plan. No reading splits careful answers beyond the bands.

## Fix

None required. Optional (solution): in Step 4 or 6 say the cap is applied to the fund's total calls in the order facility, new investments, fees, past-period rate, refinancing; and in step 6 say the value response is fitted on the assets' valuation plus the loan, so a careful rebuild lands on 0.70 and 0.035 rather than on 0.75 and 0.02.

**DETERMINISTIC, APPROVE.**

## Addendum: final rebuild

Fresh scratch: /tmp/determinism-task20-p7/target; scripts in scratchpad/w7. Re-read prompt, policy section 8 as it now stands, and submission.md Steps 4 and 6.

**Disposition and verdict stand: DETERMINISTIC, APPROVE.** Headroom now rebuilds at 206.6 to 208.5 (block 209.7, band 187.5 to 223.4), program B.

### 1. Policy section 8 text
- The closing line is gone; the opener now reads "Capital calls are all those the endowment's managers can be expected to make in the stress, judged on the evidence the Office of Investments holds". A literal reader therefore counts (a) the funds' calls to meet a maturing loan's refinancing shortfall (they are expected calls, and the record shows the fund investing the difference in all 5 lower-balance refinancings), as the blocks do; the commitment cap in section 3 still limits them. The reading that leaves them out is the careful-route rival at 326.7 (A), already named and ruled out by the opener's "all" plus the activity file.
- (b) Investment period end: the policy is silent on successors; the opener sends the reader to the evidence, and the register rebuilds the same rule as in pass 6 (all 16 clause managers' early successions ended the quarter before; the 8 ran on). Ends held to the register: 79.6, program C, named-data ruling as before. Extension of periods in the stress: the text now says "no allowance for the exit market" in the investment paragraph, so the block's no-extension stands; if a reader extended them anyway the headroom is 217 to 219 (B, in band). No second reading reaches another program or leaves a band.

### 2. Custodian value dates, accrued liabilities
No figure moves. Unfunded by strategy 1,614.4 / 443.5 / 223.7 / 581.0 / 1,169.8 / 474.0 (4,506.5); facility balance 316.1 and audited borrowings 49.2, same funds; distributions 603.6 / 443.4 / 237.9 / 265.8 exactly. Accrued liabilities enter no section 7 or 8 figure.

### 3. Steps 4 and 6 as now stated (USD million, mine against the blocks')
| Figure | Block | Mine |
|---|---|---|
| Facility / new investments / rate on past-period funds | 316.1 / 1,134.8 / 278.4 | 316.1 / 1,134.9 / 278.4 |
| Fees and expenses | 174.4 (45.2, 45.1, 43.2, 40.9 by half) | 180.8 (45.2, 46.1, 45.2, 44.3): NOT reproduced, gap 6.4; term-end and pending-start variants give 177.1 to 179.9; unexplained. The stated order (facility, fees, rate, investments, refinancing last) leaves my sum unchanged since the cap binds only 0.5 |
| Value response, fitted as Step 6 states (assets past four years, loan unchanged in the quarter, valuation plus loan, one quarter late) | 0.70 and 0.035 on 743 | 0.704 and 0.032 on 834 (R2 0.995); lag 0 and lag 2 give R2 0.15 and 0.04; the stated pair rebuilt to rounding, count differs by the plan definition (not filed) |
| 31 Dec value moved from 30 Sep to the quarter before maturity: Q1 factor | 0.9847 (sheet) | 0.9849 |
| Shortfall on the 23 loans | 279.5 | 284.5 (block's 0.70, 0.035); 281.5 (my fit) |
| Called within commitments (refinancing last) | 254.9 | 251.6; 249.8 on my fit |
| Total calls on the commitments | 2,158.7 | 2,161.8 |
| Headroom | 209.7 | 206.6 (my fit 208.5) |

Alternative named in Step 4 (shortfall first): refinancing 276.3, others 1,885.5 (facility 303.8, fees 168.4), total 2,161.8, headroom 206.6: unchanged, as the block says.

Remaining open: the 6.4 fee difference (it makes my headroom lower, never higher than 213 if all of it were fees; B and band hold) and the plan definition behind 743. Neither moves a graded figure or the call. No fix required; optional: state which fund-quarters the golden's fee line omits (it lowers the later halves by 1 to 3.7 against a latest-statement reading) so a rebuild lands within 0.5.
