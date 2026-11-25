# task4 determinism check (Holistic Audit v4, determinism mode), 2026-11-25

Scope: prompt.txt 1fa45a2f98db0eb39ba3de57d665e867, target.zip e715f5861b0ccc4d768028d4922a8db4, submission.md
8683910acc4c7df5695316c1950deec0 (prompt not rewritten; 23 input files; fields: final recommendation, supplementary,
critical components, step-by-step). Workspace /tmp/holistic-task4-determinism-wvj3zuu5, scripts in its `work/`.

- **Verdict:** NOT_DETERMINISTIC (the firkin cover turns on a constant no file holds)
- **Disposition:** SEND_BACK (the cold store's run share needs a pin in the pack), plus FIX_NOW block edits listed below

## Step 0
The golden is present with computed values. The inputs belong to the task: Wrenfold, FS-04 issue 3, Lindqvist Q26-1187,
Maplestead schedules and the count of 30 Nov 2026 all appear in the files.

## Part A: correctness

I derived each figure first, then compared it. My pipeline: dedupe the dockets (2,562), fill blank codes from products,
map 253 renumbered accounts; fit log-weekly deliveries (trend, two harmonics, a hinge on Calder Vale temperature; my
bends came out 17/17/17/15/15 and the scatter 5.27 per cent); add Maplestead from listing at the Schedule B rate shaped by
the season; rebuild the checks with empties = line's weekly sales times days since the last dray call over 7; fit the
holding as a + S(b0 + b1 times the weeks between deliveries); estimate lot survival by weighted log-share on age; model the
store as half-run plus cover times deliveries; run the FS-04 weekly balance. The level at the count is the fit at week
23 Nov 2026 (recorded 10.7 C). That is the author's reading: the actual week is 5.0 per cent below it.

| Figure | Mine | Author | Band | Agree |
|---|---|---|---|---|
| Planning shortfall K50/K30/K20/FIR/KIL | 4,409 / 1,895 / 685 / 1,530 / -448 | 4,544 / 2,009 / 699 / 1,578 / -448 | all in | yes |
| Hot case (2nd of 10) | 8,463 / 2,365 / 1,030 / 1,540 / -448 | 8,590 / 2,486 / 1,043 / 1,586 / -448 | all in | yes |
| Covers | buy, buy, hire, buy, none | same | | yes |
| C1 trade rise | 4,614 / 2,134 / 784 / 372 / -27 = 7,877 | 4,644 / 2,140 / 785 / 385 / -27 = 7,927 | in | yes |
| C2 store at fullest | 4,266 / 2,382 / 2,177 / 1,582 / 254 = 10,662 | 4,299 / 2,383 / 2,181 / 1,581 / 254 = 10,698 | K50 band 4,271 and total band 10,668 missed by 5 and 6 | marginal |
| C3 loss | 2,486 / 1,086 / 220 / 1,054 / 237 = 5,083 | 2,486 / 1,085 / 220 / 1,054 / 237 = 5,083 | in | yes |
| Hazard, on-site share, alive | 11.0 per cent annual on K50; 0.59 / 0.45 / 0.44 / 0.31 / 0.60; 19,994 | 11.1; same; 19,990 | | yes |
| Holding a, b at weekly; raw b | 2.28 / 2.12 / 2.02 / 2.92 / 3.03; 0.95; 0.28 | 2.26 / 2.11 / 2.02 / 2.96 / 3.03; 0.95; 0.28 | | yes |
| Store cover c | 0.342 / 0.357 / 0.355 / 0.349 / 0.344 | 0.346 / 0.357 / 0.359 / 0.349 / 0.346 | | yes |
| Worst week K50 | 19 Jul (4,409; 26 Jul 4,385) | 26 Jul | | tie |
| Records as they stand (all three off) | -553 / -258 / -981 / **+14 (hire)** / -760 | -718 / -234 / -944 / -20 (no cover) / -754 | | FIR sign differs |

Mismatches:
1. Component 2's band (plus or minus 0.3 per cent) is tighter than the delivery fit's own noise. My K50 store and total
   land 5 and 6 below it with the author's convention.
2. The K50 worst week is a 24-container plateau over 19 and 26 July.
3. The Final Recommendation's naive firkin figure (-20, "no cover") sits on the zero line. I get +14, which is hire.
4. C3's displayed parts add to 5,082 against the stated 5,083. That is rounding only.
5. Step 4's fall check (0.88, SE 0.06): its specification is not stated. Mine gives -0.78 (not graded).

Decision_reproduces: yes, on the blocks' conventions. The single-stump-off claims hold on the calls: rebuild-off
2,573 / 1,142 / 412 / 1,589 / -431, store-off 3,244 / 1,364 / -491 / 827 / -585, loss-off 3,057 / 1,299 / 592 / 692 / -638.

## Part B: determinism

**Deciding steps:** these are the three estimates, and each is verified to move the call alone.

**Unpinned fork: the share of a racking run the cold store holds.** Step 7 takes "half of each beer's racking run" as
a fixed constant. No file states it, and the record cannot identify it, because the runs never change in the record
(the blocks rely on that for the stump). Each type's own regression of the Monday position on deliveries, with its
intercept read as theta times the run sum, gives:
- K50: 0.83 to 1.17
- K30: 0.63 to 0.79
- K20: 0.54 to 0.57
- FIR: 0.14 to 0.45, depending on the window (104 weeks: 0.27 plus or minus 0.18)
- KIL: 0.31 to 0.72

Carried to the 2027 plan, the type-own theta files **FIR 1,193, hire** (K50 5,343 buy, K30 2,135 buy, K20 819 hire,
KIL -385 none). That flips the firkin cover. In pairs with ordinary conventions it files FIR 1,142 to 1,199:
- count level at the actual week: 1,149
- no condemned since the count: 1,142
- quadratic survival: 1,157
- no temperature bend: 1,185
- flat Maplestead: 1,199

Sweeping one common theta, FIR flips below about 0.28 and K20 flips to buy above about 0.73.

The strongest design the pack affords (rule 2) reconstructs each beer's stock from the racking log in and the dockets
out (it correlates with the Monday store plus depots at 0.83 to 0.96). It measures theta at 0.31 to 0.39 on the K30,
K20, FIR and KIL beers. That files buy, buy, hire, buy, none, but the store totals 9,457 to 9,857, so Component 2 falls
out of its band for any theta not within about 0.004 of one half. No file refutes either rival. FIR's own intercept is
1.2 SE from one half, and K50's is 2.2 SE away on the other side. Pin: NO PIN FOUND. Both conditions for a rival that
counts hold: the call moves (FIR), and an analyst who regresses the store on deliveries and scales the run part is a
plausible adoption from the prompt.

Every other fork leaves the call standing. They are below with their dispositions.

**Data anomalies:**
- Check duplicates (24, 10 of them conflicting): keeping the last instead of the first moves nothing (4,410 / 1,894 / 683 / 1,531 / -448).
- Docket duplicates and blank codes: policy forced by the data.
- No docket falls on a check day, so the dray-day boundary is moot.

**Giveaways:** none. No file states a cover, a shortfall or a component.

## Evidence: the forks run
Planning shortfall K50 / K30 / K20 / FIR / KIL, on the author's count reading, each alone:

| Fork | Result | Disposition |
|---|---|---|
| Trend off | 4,548 / 1,877 / 625 / 1,613 / -437 | same call |
| One harmonic | 4,723 (out) / 1,901 / 716 / 1,559 / -450 | AIC prefers two on K50 |
| Three harmonics | 4,373 / 1,894 / 679 / 1,540 / -447 | same |
| No bend (linear temperature) | 4,529 / 1,898 / 694 / 1,524 / -449 | same; K50 AIC -900 vs -818 |
| Fit on last 104 weeks | 4,395 / 1,839 / 651 / 1,573 / -450 | same |
| Maplestead flat | 3,926 (out) / 1,687 (out) / 635 / 1,535 / -448 | same call; Schedule B files a twelve-month average |
| Count level: week of 30 Nov at normal | 4,634 / 1,996 / 731 / 1,543 / -447 | same; **C1 4,715 / 2,184 / 806 / 380 / -26 = 8,059, out of band** |
| Count level: actual week of 23 Nov | 4,750 (out) / 2,122 (out) / 774 (out) / 1,486 / -439 | same |
| Count level: 4-week mean | 4,052 (out) / 1,801 (out) / 642 / 1,540 / -439 | same |
| Holding with one slope | 3,970 / 1,757 | refuted: interaction 0.516, SE 0.041 on K50 |
| Empties at half / whole delivery | 3,882 / 1,674 and 5,348 / 2,274 | refuted: the dockets give each check's days |
| Survival linear in share | 5,120 / 2,080 / 735 / 1,790 / -377 | refuted: weighted SSE 5.82 vs 0.32 (K50), 0.56 vs 0.07 (FIR) |
| Survival quadratic in log share | 4,435 / 1,905 / 684 / 1,494 / -472 | same |
| Loss since count pro rata to deliveries | 4,381 / 1,962 / 686 / 1,544 / -453 | same |
| No condemnations since count | 4,267 / 1,816 / 664 / 1,480 / -457 | same |
| Float two fifths | 5,425 / 2,398 / 852 / 1,705 / -423 | pinned by FS-04 7.1 |
| Store at 2026 weeks of cover (stump) | 3,244 / 1,364 / -491 / 827 / -585 | refuted by the 2027 runs |
| **Store theta from each type's record** | 5,343 / 2,135 / 819 / **1,193 hire** / -385 | **NO PIN** |
| Store theta from stock flow (0.35 to 0.40) | 3,993 to 4,132 / 1,707 to 1,770 / 351 to 462 / 1,308 to 1,382 / about -480 | same call; C2 9,457 to 9,857 |
| Hot case highest instead of 2nd | 8,667 / 2,451 / 1,033 / 1,541 / -448 | pinned by FS-04 3.3 |

Every pair of the 13 non-stump conventions (78 pairs): no flip without theta. The extremes are K30 1,565 and FIR 1,142,
and both of those pairs contain theta.

## Fix
1. **Pack (SEND_BACK, through `/fix-determinism`):** file how the cold store holds a run, as a fact of operation and
   not the method. For example, a line in the brew plan or a cold-store instruction: "each beer is racked as one run
   when its stock in the cold store is down to its cover". Alternatively, give the record a measurable run change.
   The architect must weigh that it hands the weeks-of-cover stump a hold-out. Either way the run share must become
   derivable from the files.
2. **Blocks (FIX_NOW):**
   - Step 3: name the count's week (the week beginning 23 Nov 2026 at its recorded temperature, or 30 Nov at the normal).
   - Widen C1 to take both count-week readings (K50 to 4,715, K30 to 2,184, total to 8,059).
   - Widen C2 and the K50 store band to take the delivery fit's noise (at least 10,660 and 4,265).
   - Widen the planning bands for a 4-week count level (K50 to 4,052, K30 to 1,801) or refute it in Step 9.
   - Accept 19 or 26 July as the K50 (and K30, K20) worst week.
   - Reword the Final Recommendation's records-as-they-stand firkin figure ("about nil", not "no cover (-20)").
