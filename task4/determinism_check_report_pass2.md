# task4 determinism check, pass 2 (Holistic Audit v4, determinism mode)

In-house replay of the platform's Holistic Audit v4 (Step 0, Part A, Part B), 2026-11-25. The cut: prompt.txt
1fa45a2f98db0eb39ba3de57d665e867, target.zip 9bbf8c214e05e61a6f930185c747976f, submission.md
0e4fdca438fca6cc5c79c0f49e881090 (manifest.json of the workspace, 23 input files, prompt not rewritten). I derived
every deciding figure from the pack before comparing it with the blocks. The earlier report was not opened.

- **Verdict:** DETERMINISTIC
- **Disposition:** FIX_NOW (answer-block edits only; nothing the solver sees changes)

## Step 0

The golden is present: all four fields carry computed values. The inputs belong to this task: Wrenfold, Calder Vale,
Maplestead, Lindqvist, Pennine, FS-04 and TQ-02 all appear in the pack, and every file the Step-by-Step names is
shipped.

## The audit's own lines

**correctness:** correct. Every cover reproduces, and so does every graded figure inside its band. The loss
reproduces exactly. My planning-case shortfalls sit 0 to 132 below the author's, with no rule in the blocks to
close the gap (see the fix list).

**figures_checked** (my value / the author's / agree):

| Figure | K50 | K30 | K20 | FIR | KIL | Agree |
|---|---|---|---|---|---|---|
| Lost in the trade, year to count | 2,486 / 2,486 | 1,085 / 1,085 | 220 / 220 | 1,054 / 1,054 | 237 / 237 | yes, 5,082 exact |
| Trade rise to summer peak | 4,611 / 4,644 | 2,143 / 2,140 | 785 / 785 | 384 / 385 | -27 / -27 | yes (7,896 / 7,927) |
| Cold store at fullest | 4,327 / 4,340 | 2,367 / 2,365 | 2,202 / 2,197 | 1,597 / 1,596 | 258 / 257 | yes (10,751 / 10,755) |
| Planning-case shortfall | 4,453 / 4,585 | 1,889 / 1,991 | 713 / 715 | 1,552 / 1,593 | -445 / -445 | yes, in band |
| Worst week | 19 Jul / 19 or 26 Jul | 26 Jul / 19 Jul to 9 Aug | 19 Jul / 12 to 26 Jul | 20 Sep / 20 Sep | 20 Sep / 20 Sep | yes |
| Hot case (2nd of 10 summers) | 8,522 / 8,635 | 2,359 / 2,467 | 1,057 / 1,057 | 1,561 / 1,600 | -445 / -445 | yes, in band |
| Cover (FS-04 4.1, Q26-1187 runs) | buy / buy | buy / buy | hire / hire | buy / buy | none / none | yes |

The intermediates also reproduce:
- dockets: 2,562 duplicate lines and 253 renumbered accounts;
- delivery fit: bends of 17, 17, 17, 15 and 15, a K50 scatter of 5.27%, and the count week 5.0% below the fit;
- cellar checks: 5,621 checks on 1,390 calls and days since the dray of 3.9 to 4.1;
- held per container sold a week on K50: 0.28 read raw and 0.953 rebuilt; per-line constants 2.26, 2.11, 2.02, 2.96
  and 3.03;
- the checks' fall: -0.880 (SE 0.059);
- loss rates of 11.1, 7.2, 2.8, 11.3 and 11.8%, on-site shares of 0.59, 0.45, 0.44, 0.31 and 0.60, and 19,991, 13,960,
  7,578, 8,245 and 1,777 alive;
- store: cover 0.3465 and share 0.509 (SE 0.0196);
- the raw-check rise: 4,857 (author 4,867).

The leave-out claims all reproduce their covers.

**mismatches:**
1. Step 7 says "the same fit on every Monday (0.505)". I get a share of 0.546 (cover 0.337). The covers are the same
   either way.
2. In the all-three-off route (the Final Recommendation's rejected order), firkins come out at +23 for me against
   -20 for the author. The route sits on the nil line, so "next to nothing (-20, about nil)" is a cover that reads
   either way.
3. Step 9 says every cover holds with each fitted input moved 20 per cent. On my rebuild K30 falls to 1,461 with the
   rise at -20% and to 1,416 with the store at -20%, both under 1,500. The claim holds only on the author's base, which
   is about 100 higher. These are stresses, not rival readings.
4. Step 9 says the nearest cover is 211 from its line. On my rebuild the nearest defensible pair is K30 at 1,582 (Level
   mean4 plus Maplestead flat, 82 above the line).

**decision_reproduces:** yes, all five covers.

**determinism:** pinned.

**unpinned_forks:** none that moves the call. One rival is closed only by an argument the blocks do not make (item A
below), and one fitted form moves graded figures out of their bands (item B).

**Giveaway files:** none. The only hits for the golden figures in the pack are serials, docket numbers and a
shared-string index.

## Part B

**Committed call:** purchase K50, K30 and FIR; hire K20; no cover for KIL. It rests on the three estimates (rise,
store, loss) feeding FS-04 2.1 to 2.3.

**Deciding step:** reading the checks as the whole holding, reading the store at 2026's runs, and carrying the fleet
with condemnations only. Each of these moves the call alone, both on my rebuild and on the author's. Leaving out all
three gives -556, -239, -978, +23 and -760 on my rebuild.

**Pins for the decision points that move the call:**
- **Maplestead left out** (K50 1,000 hire, K30 -513 none, FIR 874 hire). Pinned by FS-04 3.4: "the accounts supplied
  and those under a signed supply agreement". Schedule A is signed 23 October 2026.
- **Checks read raw** (2,474, 1,075, 406, 1,604 and -428). Pinned by TQ-02: "Full in cellar: unbroached ... On
  dispense: 1 where ... coupled", so the form has no empties. FS-04 5.1 keeps the empties waiting for the dray. The
  data check it: full plus on-dispense falls on sales times days since the dray at -0.88 (SE 0.059).
- **Store at 2026's runs or 2026's weeks of cover** (2,995, 1,273, -532, 819 and -586). Pinned by FS-04 3.4 ("the
  range and the brew plan as issued") and by the data. In racking_log each beer's median run is the same in every year
  from 2023 to 2026 (PIL 396 or 397, GLD 298), so no type's own series can see a run change. The cross-beer fit gives
  0.509 of a run (SE 0.020), and the 2027 plan moves PIL to 2,400 and GLD to 1,400.
- **No loss carried forward** (2,880, 1,194, 574, 704 and -635). Pinned by the data. The register has only ACTIVE and
  CONDEMNED. The lots' on-site share falls with age (K50 youngest lots 0.479, 0.433, 0.375; oldest 0.120, 0.104, 0.095).
- **Depots and wash held at the count's level** (K50 2,708 and K30 1,176, both hire). Pinned by the data: in
  depot_stock_weekly the full stock scales with deliveries. Summer over winter, stock against deliveries runs 1.67 vs
  1.70 (K50), 1.29 vs 1.31 (K30), 1.70 vs 1.69 (K20) and 0.79 vs 0.81 (FIR). Monday awaiting-wash runs 1.65 vs 1.72
  (K50) and 1.27 vs 1.31 (K30). The ratio of stock to deliveries is 0.248 in summer and 0.252 in winter.
- **Store "at its fullest" read as cover plus a whole run** (K20 2,480, which would be a buy). Ruled out by
  cold_store_monday_position. Over 104 Mondays the K20 total peaked at 983 and never reached cover plus runs, whose
  lowest value is 1,112. The type totals reached it on 0 to 8% of Mondays across the five types. Peaks of staggered
  beers do not add.
- **Float 2/5:** pinned by FS-04 2.1 and 7.1. The **season and planning weather** are pinned by 3.1 and 3.2. The **hot
  case** is pinned by 3.3 and does not change the cover (4.1).

**Strongest rival (house rule 2).** This is the absolute stock design: the requirement's trade term taken from the
checks model in level (a + b·s per line), and the fleet taken from the lots' survivors less losses and condemnations.
At the count the two instruments put the trade at:

| Type | Checks model | Lots (alive less site) | Gap |
|---|---|---|---|
| K50 | 9,194 | 8,224 | +970 |
| K30 | 7,386 | 7,650 | -264 |
| K20 | 4,207 | 4,229 | -22 |
| FIR | 6,435 | 5,660 | +775 |
| KIL | 739 | 721 | +18 |

The rival files 5,423 buy, 1,625 buy, 691 hire, 2,327 buy and -427 none. That is the same call, but it moves K50
above its band (high 5,064), K30 below its band (low 1,769) and FIR above its band (high 1,769).

Paired with Maplestead flat it gives K30 1,411 on my rebuild, which crosses to hire. On the author's base it would be
about 1,513. It is ruled out by FS-04 2.1 to 2.3: the containers at customers at the count are in both the
requirement and the fleet. Estimating that one stock twice with two instruments counts their disagreement as a
shortfall. The blocks never say this (item A).

**Fork list run in code.** The covers come out the same in every row except those marked as ruled out. Values are
K50 / K30 / K20 / FIR / KIL, on my rebuild.

| Fork | Shortfalls | Note |
|---|---|---|
| Level: count-week actual | 4,794 / 2,117 / 802 / 1,509 / -435 | |
| Level: mean of the last four weeks | 4,095 / 1,795 / 670 / 1,561 / -435 | |
| Level: 30 Nov at its normal | 4,678 / 1,990 / 759 / 1,564 / -444 | |
| Loss: OLS on logs | 4,453 / 1,895 / 713 / 1,550 / -445 | loss within band |
| Loss: binomial NLS | 4,451 / 1,887 / 714 / 1,554 / -445 | loss within band |
| Loss carried to the week's end | 4,497 / 1,908 / 717 / 1,570 / -441 | |
| Forward loss as a hazard on survivors | 4,309 / 1,846 / 710 / 1,464 / -465 | |
| Loss curve: linear survival form | 4,936 / 1,972 / 717 / 1,797 / -375 | item B |
| Maplestead flat through the season | 3,994 / 1,675 / 657 / 1,563 / -445 | |
| Bend +1 C | 4,493 / 1,892 / 715 / 1,570 / -444 | |
| Bend -1 C | 4,427 / 1,888 / 711 / 1,539 / -446 | |
| Bend +0.5 C | 4,475 / 1,890 / 714 / 1,561 / -444 | |
| Demand: seasonal naive (2024 to 2026 same weeks) | 6,368 / 2,209 / 741 / 1,654 / -418 | out of band; ruled out by 3.2 (normal weather) |
| Store fit on every Monday | 4,528 / 1,939 / 835 / 1,618 / -434 | |
| Store share at +2 SE | 4,601 / 1,976 / 853 / 1,637 / -431 | |
| Store share at -2 SE | 4,305 / 1,801 / 572 / 1,467 / -459 | |
| Depots and wash: ratio to the actual week | 4,641 / 2,007 / 761 / 1,536 / -442 | |
| Depots and wash: affine scaling | | same covers alone; refuted by the seasonal ratios above |
| Sales measure: own dockets, 13 weeks | 4,508 / 1,893 / 748 / 1,546 / -444 | |
| Sales measure: own dockets, 4 weeks | 4,511 / 1,905 / 759 / 1,544 / -445 | |
| Duplicate checks: keep first | 4,454 / 1,890 / 714 / 1,552 / -445 | |
| Days since the dray counted to the day inclusive | | identical |
| Rebuild at the fitted fall, 0.88 | 4,273 / 1,808 / 722 / 1,550 / -443 | |
| Half a delivery added to every check | 3,994 / 1,699 / 676 / 1,557 / -441 | the measured days refute it |
| Whole delivery added to every check | 5,454 / 2,300 / 896 / 1,518 / -453 | the measured days refute it |

Over every pair of the forks not ruled out (147 variants), the ranges are:

| Type | Min | Max | Line | Flips |
|---|---|---|---|---|
| K50 | 3,642 | 6,739 | 3,500 | none |
| K30 | 1,582 | 2,445 | 1,500 | none |
| K20 | 615 | 923 | 0 and 1,200 | none |
| FIR | 1,422 | 1,720 | 1,200 | none |
| KIL | -466 | -407 | 0 | none |

## Fix (solution only)

A. **Step 9, the cancellation and the K30 margin.** Add one sentence: "The trade's holding at the count is in both the
requirement and the fleet (FS-04 2.1, 2.2), so it is estimated once; taking it from the checks for the requirement
and from the lots for the fleet counts the two instruments' disagreement (+970, -264, -22, +775, +18 at the count) as
shortfall." Replace "the nearest 211 containers from a line" and the 20 per cent claim with the K30 margin as it
stands on the cut. Either widen the K50, K30 and FIR planning bands to take the absolute design (5,423, 1,625, 2,327
on my rebuild), or keep the bands and let the refutation sentence carry the case.

B. **Component 3 and the loss bands.** A linear survival form fitted to the same lots gives the following losses. The
lots' own binomial deviance favours the exponential by 146 (K50), 35 (FIR), 18 (KIL), 9 (K30) and 0.7 (K20).

| Type | Linear-form loss | Band |
|---|---|---|
| K50 | 3,251 | 2,469 to 2,518 |
| K30 | 1,213 | 1,033 to 1,108 |
| K20 | 226 | 179 to 239 |
| FIR | 1,359 | 1,033 to 1,067 |
| KIL | 324 | 227 to 240 |

Add to step 6: "a straight-line survival fits the lots worse (deviance +146 on K50) and is not used". Either widen
the K30 loss band (the gap there is only 9), or state the refutation.

C. **Step 8, the rules my rebuild had to guess** (house rule 5). The blocks should state:
- how losses and condemnations accrue from the count to each week: pro rata of the year-to-count loss, to the week's
  Monday or its end, and condemnations at which rate;
- which deliveries the depots' and wash's weeks of cover are read against;
- the base the Maplestead volume is "shaped by the season" against.

With my readings the planning case lands 132, 102, 2, 41 and 0 below the author's, and the hot case 113, 108, 0, 39
and 0 below. Everything stays inside the bands, but nothing written lets a reviewer place the gap.

D. **Final Recommendation, the rejected route's firkins.** "next to nothing for firkins (-20, about nil)" should read
"about nil for firkins (-20; the route sits on the nil line)". My rebuild of that route gives +23.

E. **Step 7.** The every-Monday share should read 0.546 (cover 0.337), or the window that gives 0.505 should be named.
