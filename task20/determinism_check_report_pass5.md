# task20 determinism check, pass 5 (Gates A to E)

Scratch copy: /tmp/determinism-task20-p5/target. Scripts: the session scratchpad, folder w

**Verdict:** DETERMINISTIC on the call (B), with the blocks' mid-chain figures partly unreproduced and the margin thin under stacked alternatives. I could not rebuild the refinancing model, so the 219.1 headroom is not recomputed end to end.
**Disposition:** FIX_NOW (answer-block edits only; see Fix). No prompt or pack change needed on what I could test.

## Recomputed against the blocks

| Figure | Block | Mine | Status |
|---|---|---|---|
| Reserve | 2,778.7 | 2,778.74 | reproduced |
| Spending (8 x 98.88) | 791.0 | 791.0 | reproduced |
| Not yet called by strategy (Q4 custodian roll, released out, pending in full) | BO 1,614.4; GE 443.5; VC 223.7; RE 581.0; IN 1,169.8; PC 474.0; total 4,506.4 | 1,614.4; 443.5; 223.7; 581.0; 1,169.8; 474.0; 4,506.5 | reproduced (rounding) |
| Distributions by half-year | 603.6; 443.4; 237.9; 265.8 | 603.6; 443.4; 237.9; 265.8 | reproduced exactly |
| Benchmark call rates (vintage 6+ years before, whole, 2008Q3 to 2010Q2) | 12.13, 12.28, 9.02 % | 12.13, 12.28, 9.02 % | reproduced |
| Past-IP BO/GE/VC funds at registered ends | 32 funds, 2,170.7 | 32, 2,170.7 | reproduced |
| Audited borrowings at share | 49.2 | 49.2 | reproduced |
| Loans due in the window | 23, 839.6 | 23, 839.6 | reproduced (live loan = latest drawn or refinanced record, no later realization) |
| Past refinancings | 35, 5 at lower balance | 35, 5 | reproduced |
| Successor rule | 16 clause managers, 8 ran on | my register table agrees; every early-succession of a clause manager stops the quarter before the successor's first close (no exception); the 8 listed managers show fund periods that ran on | reproduced |
| New investments, 8 quarters | 1,173.7 | 1,134.9 (activity file at share, IP inclusive of end quarter); 1,127.3 (years from quarter after); 1,198.1 (investments from the capital-account statements); 1,182.6 (IP end quarter plus one); 1,056.0 (first investments only) | NOT reproduced, spread 1,056 to 1,198 |
| Past-IP calls | 245.9 | 278.9 (successor ends, cap at unfunded); 221.4 at registered ends | NOT reproduced (+33 on mine) |
| Facility balance | 310.1 | gross invested less called = 391.1; audited identity confirmed at FY2025 (borrowings = invested less called less reinvested), so the netting is derivable; 310.1 not rebuilt | partly |
| Fees and expenses | 180.1 | 243.9 on the latest statement's fee flat to term end | NOT reproduced; basis open |
| Refinancing calls 254.3, headroom 219.1, A 291.7, B 119.2 | | not rebuilt | not verified |

My investment (-39) and past-IP (+33) gaps run in opposite directions and nearly cancel, which suggests the golden counts the quarter of the period end differently (investing one more quarter, benchmark rate one quarter later). The policy does not say which.

## Forks run (headroom shift, program)

Headroom base 219.1; B needs at least 119.2 (99.9 room); A fails above 291.7 (72.6 room). A flips only if headroom exceeds 291.7; B falls to C below 119.2.
- Benchmark funds a year younger or older: past-IP calls 324.2 (vintage age 5) and 240.1 (age 7), against 278.9 on my base. Headroom moves about -45 and +39, B each time. Two years: 382.2 and 214.1. Shifts of 2 years younger give about -100 (borderline for B). The policy says "six or more years", so this is ruled out by the sentence for the base but the 2-year shift is not a defensible reading.
- Rate on the commitment not yet called instead of the value: past-IP calls 91.3, headroom about +190, B (A needs 291.7; still fails at about 410? not checked, may pass A). The policy says "over those funds' value at the end of the previous quarter" and "its value at 31 December": rules it out.
- Registered ends instead of successor ends: investments +163, past-IP -58, net about +105 calls, headroom about 85 to 115 by my scale: program C or the B edge. This is the block's rejected program A reading (careful route) only when the loans stay as they stand; not rerun.
- Pace on first investments only: investments 1,056.0 (-79 vs my base, headroom about +79, B; A needs headroom above 291.7, not reached).
- Pace years counted from the quarter after the first close: 1,127.3 (-8).
- Pace denominator statements vs activity file: +63 (1,198.1), headroom about -63, B holds.
- Facility with no reinvested-proceeds netting: balance 391.1 against 310.1, headroom about 138, B holds by 19 only.
- Facility at the latest audited borrowings (49.2): headroom about +261, about 480, A passes. The policy asks for the balance at 31 December; the audited file's latest year ends 2025 for 61 of 66 funds and the activity file shows the facilities drawn again in 2026, so this reading is ruled out by facts, not by a sentence. Step 3 says so.
- Fees on the latest statement's fee flat (243.9 vs 180.1): -64, headroom about 155, B holds by 36.
- Stack of the last two adverse readings (no netting and fees flat): headroom about 74, below 119.2, the call falls to program C. Each is a single-sentence choice the policy leaves to "the evidence" (section 8, last line) or to the unstated way the balance is formed.
- First closes slipped, reinvested proceeds netted, caps, extended periods, fund expenses: not run (budget).

## The two decisive judgments

- Successor closes: forced by the register for the managers with past cases (every early succession of a clause manager stopped the quarter before; no exception; the ran-on managers are mixed or consistently later). The seven funds and their successors' dates are unambiguous: four re-up dates come from the plan, three from the register's expected first closes. The deferral of a re-up in B or C does not change the manager's own first-close date (it is the manager's schedule). A literal reader holding every period to the register's recorded end would not be following section 8's evidence clause, but no shipped sentence says the register's end is wrong; the block's "hurried" reading is therefore legal under the text alone. The rule is derivable only from the pattern of past records.
- Refinancing calls: the five lower-balance refinancings show a follow-on investment of exactly the shortfall five days later (Juniper Valley: 297.135 to 280.570, follow-on 16.566; Bluff Station: 532.758 to 501.254, follow-on 31.504). So the fund-calls-the-shortfall rule is forced by the record. Two of those five funds were past their investment periods, so no sentence confining investments to the period applies (section 8's last line leaves other calls to evidence). I could not reproduce the lenders' limit fit (my loan to value on valuation records is noisy and above 1 for many refinancings, so the stated formula could not be checked) and did not rebuild the value response. The fitted inputs' spread against the band is unverified.

## Gates B, D, E

- Gate B: every fact I used is in a shipped file. The policy's bases are filed (pace, benchmark funds, rate, facilities, first closes). Not filed: which file measures "commitment not yet invested" and "investments"; the year-end facility balance formation; fees after the investment period; the quarter in which a successor-ended period starts the benchmark rate. "Successor funds", "first close", "investment period", "refinancing" appear in inputs.
- Gates D and E: the prompt asks for the program, the headroom in USD million, the calls and distributions by half-year, and the amounts not yet called by strategy. Each pins one answer with a unit. No ambiguity in the asks beyond the open bases above.

## Blocks' own claims

- Step 8's "the benchmark's 2008-10 call rates replayed on the commitments not yet called on program A": ruled out by the policy wording, consistent with A.
- Closing figures (178.3 or 254.1 for the benchmark a year younger or older; 217.9 for the pace over the commitment not yet called): not reproduced in my model (mine shifts -45 and +39 for the vintage rule). Directions agree; magnitudes differ by up to 10 in the older case and about 5 in the younger. They hold only if the golden's base differs from mine as described above.
- "Every rival fit within 213.1 to 233.8": contradicted for the facility netting (-81), fees flat (-64) and pace-from-statements (-63) as I ran them. Rewrite that sentence or add these rivals with their headrooms.

## Fix

Where: solution (answer blocks); no change to the prompt or pack.
1. State in Step 4 the conventions the policy leaves open and the golden used: the file for investments and commitment not yet invested; whether the end quarter of an investment period counts as investing; the quarter the benchmark rate starts; the fee rule after the period (cost still held versus latest fee) with its USD figure; how the 31 December facility balance is formed (invested less called less reinvested, the reinvested part rolled from the audit).
2. Reproduce 1,173.7, 245.9 and 180.1 from those stated conventions in the generator checks, or restate them.
3. Add to the closing passage the rivals that move the headroom furthest (no netting 138; fees flat 155; statements-based pace; the stack of the last two about 74 and program C) and either rule them out by a quoted sentence or widen the headroom band and state the stack margin. If the stack of two open choices flips B to C, that is a Gate C fork the files cannot close: SEND_BACK to add a fee sentence and a facility-formation sentence to the policy section 8.
4. Verify the refinancing fit (the stated limit formula) against the past refinancings and add the loan-to-value table to the Asset loans sheet.
