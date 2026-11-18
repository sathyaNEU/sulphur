# task4 determinism check, pass r2 (Gates A to E)

Fresh unzip of `target.zip`; every figure below was rebuilt from the shipped files by the Step-by-Step's own rules.
Not opened: the design note, the generator, the goldens, any earlier report.

- **Verdict:** DETERMINISTIC, with SOLUTION_WRONG (the five covers are forced; the blocks carry one figure that does
  not rebuild and several rules that had to be guessed).
- **Disposition:** FIX_NOW. Answer-block edits only; the prompt and the pack stay as they are; no rerun.
- **Fix location:** solution.

## Why

Every reading the files leave open keeps the five covers (buy 30 litre kegs and firkins, hire 50 and 20 litre kegs,
nothing for kilderkins): about 90 rebuilds, singles, pairs and triples. The ten ask figures and the three components
rebuild to the unit. What fails is inside the blocks: the 20 litre figure of the rejected route in the Final
Recommendation (-383, "no cover") comes to +1,066 by the shortcut rules as written, and four rules of steps 5 and 7
read two ways or are silent.

## Figures rebuilt (Gate A)

| Figure | Blocks | Rebuilt | Band | |
|---|---|---|---|---|
| Planning case, K50 / K30 / K20 / FIR / KIL | 1,879 / 3,294 / 633 / 1,617 / -429 | same | in | exact |
| Hot case | 5,426 / 3,790 / 922 / 1,620 / -428 | same | in | exact |
| Component 1, rise at customers | 5,676 (3,079, 1,683, 566, 374, -26) | same | in | exact |
| Component 2, cold store | 10,195 (4,077, 2,177, 2,128, 1,558, 255) | same | in | exact |
| Component 3, year's loss, four types | 4,818 (2,399, 1,089, 1,104, 227) | 4,818 | in | exact |
| Off site at 30 Nov 2026 | 16,055 / 10,656 / 4,510 / 9,780 / 1,459 | same | | exact |
| Bends, deliveries at the count, F and t statistics | step 3 | same | | exact |
| Cellar relation (fixed stock, slopes, 0.878 to 0.852) | step 4 | same | | exact |
| Store cover 0.348 / 0.346 / 0.349 / 0.335 / 0.350; fitted fixed parts and errors | step 7 | same | | exact |
| Depots, wash and repair 0.545 to 0.637; condemned 198 / 111 / 26 / 57 / 14 | step 8 | same | | exact |
| Tag loss 106 of 35,448; read cover 102,424 of 105,549 | steps 5, 6 | same | | exact |
| Tags' rise 4,224 to 4,580, 356 (393 not traced in, 346 unscaled) | step 5 | same, under one of two readings (finding 3) | | guessed rule |
| Hurried: 5,764; 867 and 1,323; -658 and 5,858; 9,009; 13,997; 7,067 / 3,714 / -847 / -877 | steps 5 to 7, closing | same | | exact |
| Hurried: K20 of all three -383; in-step rise 9,956 | Final Recommendation, step 5, closing | +1,066; 11,356 | | **not reproduced** |

Every "not used" figure rebuilt: no trend 2,079 / 3,288 / 555 / 1,688 / -405; eight and thirteen weeks 3,964 and
4,451, 1,262 and 500; own dockets 0.36 / 0.68 / 0.78, 155 against 356, 1,420 / 3,149 / 532 / 1,702 / -423; two slopes
0.76 / 0.84 / 0.93 beside 1.02 / 1.01 / 1.00, 1,456 / 3,229 / 662 / 1,663 / -417; wash and repair held 1,267 / 3,108 /
554 / 1,638 / -426 (798 against 407, 499 against 235, 6,796 against 3,534); no condemnations 1,751 / 3,210 / 616 /
1,569 / -440; last 52 Mondays 1,848 / 3,525 / 701 / 1,607 / -339 with errors 84 / 146 / 61 / 186 / 24.

## Findings

1. **The rejected route's 20 litre figure does not rebuild (Final Recommendation, step 5, closing paragraph).** With
   the three shortcuts exactly as the blocks define them (customers in step on off site less the loss at the tag
   rate, the store at 2026's weeks of cover, the tag loss rate), four types come out to the unit (7,067, 3,714, -847,
   -877) and 20 litre kegs come to **+1,066** (weeks of 12 and 19 July 2027), a seasonal hire, not -383 and not "no
   cover". No season week gives -383 (the range is -247 to 1,066). In step alone gives 20 litre kegs 2,373 and a
   five-type rise of **11,356** at each type's own worst week (11,194 at the golden's weeks), not 9,956; the 50 litre
   figure of the same sentence (5,764) is exact. The -658 "no cover" is the store shortcut alone. Either a rule
   special to the tagged type is unstated or the two figures are wrong. Fix: correct or restate -383 and 9,956, and
   with them the Final Recommendation's "no cover for 20 litre kegs (-383)".
2. **Step 5 reads two ways on the hot case.** It gives the rise at today's accounts as "the fit at the week's normal
   temperature". The blocks' hot figures need the week's own temperature there. Read literally the hot case is
   3,868 / 3,592 / 805 / 1,619 / -429 (K50 below its band of 4,442). Fix: say the week's own temperature in the hot
   case, as the estate clause already does.
3. **The tag rule had to be guessed.** "A keg whose last delivery the recovery agent closed as not traced left out"
   read as the keg left out gives 4,208 to 4,580, a rise of **373**; the blocks' 4,224 and **356** need only the stay
   that follows that last delivery left out (16 such kegs were at a customer on an earlier delivery on 1 December
   2025). Fix: one sentence saying which. Carried to the 20 litre response, 373 gives 690 against 677, both in band.
4. **The estate's season had to be guessed.** With the trend inside "the type's fitted season": 1,872 / 3,295 / 635 /
   1,611 / -429, hot 5,418 / 3,791 / 924 / 1,615 / -428, components 5,672 and 10,194. The blocks' figures need the
   harmonics and temperature only. Both in band. Fix: say the trend is left out.
5. **"15 per cent as far" (closing paragraph) against 356 and 2,782 (step 5).** 356 over 2,782 is 12.8 per cent (13.1
   against the fitted weeks). Fix: one figure in both places.
6. **A fitted split on the whole record is neither admitted nor refused.** Step 7 fixes "the last 104 Mondays" with
   no ground; the racking runs and the range are unchanged over all three years. The mean method is indifferent (156
   Mondays: 1,890 / 3,304 / 640 / 1,627 / -430). The fitted split is not: on all 156 Mondays it gives 1,671 / 3,270 /
   645 / **1,313** / -465 and a store of 9,636, outside the firkin band (floor 1,478) and Component 2's (floor 9,962),
   same covers. Its firkin fixed part is 198 (standard error 92) against half runs of 342, 1.6 errors apart. Fix:
   refuse it in step 7 with those figures. A firmer ground than a distance in errors is on file: the direct split is
   steady by year (firkins 0.355, 0.324, 0.345) while the fitted firkin fixed part runs 330, 305, 198 on 52, 104 and
   156 Mondays.
7. **Two refusals are thin.** The last 52 Mondays' fit is refused on kilderkins' fixed part of 66 against 40 with an
   error of 24, 1.08 errors, and its -339 lies outside the kilderkin band. The same drift figures as in 6 would carry
   it. The week-beginning pairing is well refused, and for every type, not only 50 litre kegs: R squared 0.86 / 0.36 /
   0.19 / 0.16 / 0.20 falls to 0.55 / 0.24 / 0.13 / 0.06 / 0.08. The 637 (116) rebuilds on the 104 Mondays to 23
   November 2026; that window is not stated (dropping the one Monday with no week gives 644 (117) and 3,082 / 3,668 /
   685 / 2,021 / -354).
8. **"The register was cleaned at the first count" is in no file.** Only the hurried figures use it (9,009, 13,997,
   5,764, 7,067); the golden cancels the stock at customers. The files do support it by a figure: off site at the
   first count against the cellar relation's level is 9,086 and 9,128, 7,417 and 7,472, 4,122 and 4,104, 6,500 and
   6,517, 750 and 738. Fix: ground the sentence in that figure.
9. **Tag regressions on the whole record are not mentioned** (optional). The weekly tag count regressed on deliveries
   gives a 20 litre response of 0.87 to 0.97 on the last 104 or 52 weeks (659 to 690, in band) and 1.29 to 1.84 on all
   weeks (783 to 947, above the band top of 743, still a hire). The files rule the latter out: reads begin on 4
   December 2023, so the count stands at 506 on 11 December 2023 and 4,197 by 24 June 2024.

## Forks run (Gate C)

Planning case K50 / K30 / K20 / FIR / KIL; "same" means the five covers hold.

| Fork | Result | Call | Bands |
|---|---|---|---|
| Stock off site week by week from flows | Not buildable for the untagged types: no file holds returns, wash throughput or the packaging hall's empties between counts. At the counts only: loss over 2 and 3 years 1,859 / 3,282 / 633 / 1,597 / -417 and 1,846 / 3,274 / 633 / 1,599 / -422; the year's loss 4,764 and 4,727. K20 from the tags: finding 9 | same | in |
| Harmonics on a 52 week year; on 365.25 days | 1,882 / 3,298 / 632 / 1,618 / -427; 1,880 / 3,294 / 633 / 1,616 / -429 | same | in |
| Harmonics on the ISO week | 1,933 / 3,299 / 636 / 1,556 / -435 | same | in |
| First count from the week before the record | 1,881 / 3,305 / 638 / 1,628 / -428 | same | in |
| Store paired with the week beginning, mean method | 1,879 / 3,292 / 633 / 1,616 / -429 | same | in |
| The same pairing, fitted; slope beside half runs | 3,082 / 3,668 / 685 / 2,021 / -354; 1,464 / 3,047 / 603 / 1,426 / -449 | same | out; refused, ground reproduces (finding 7) |
| Two slopes: count's week; fitted week; four weeks | 1,456 / 3,229 / 662 / 1,663 / -417; 1,609 / 3,300 / 691 / 1,630 / -420; 1,743 / 3,299 / 707 / 1,612 / -419 | same | in |
| Own dockets: one, four, thirteen weeks | 710 / 3,035 / 469 / 1,760 / -414; 1,420 / 3,149 / 532 / 1,702 / -423; 1,664 / 3,241 / 587 / 1,658 / -429 | same | one and four out, refused, ground reproduces (155 against 356); thirteen in |
| K20 response from the tags' rise | 677 at 356; 690 at 373; 706 at 393; 669 at 346 | same | in |
| Other counting rules (305 to 432: day start or end, which Mondays) | 638 to 736, hot 929 to 1,073 | same | in, 7 and 4 under the tops |
| Wash and repair held at the count | 1,267 / 3,108 / 554 / 1,638 / -426 | same | in on planning; refused, ground reproduces |
| Trend not carried; with the fitted split; with the slope beside half runs | 1,965 / 3,290 / 601 / 1,667 / -417; 1,871 / 3,387 / 570 / 1,587 / -470; 1,998 / 3,228 / 619 / 1,705 / -403 | same | in |
| Estate out of the store; depots, wash and repair; float; loss; all four | 1,792 / 3,160; 1,743 / 3,079; 1,807 / 3,183; 1,842 / 3,232; 1,548 / 2,772 / 585 / 1,469 | same | K30 and FIR leave the bands; ruled out by FS-04 2.1 and 3.4 (a signed agreement's deliveries are deliveries) |
| Estate level through the year; season at the normal in the hot case | 1,724 / 3,208 / 617 / 1,626 / -429; hot 5,267 / 3,705 / 909 | same | in |
| Loss to the end of the week before; spread evenly over weeks | 1,809 / 3,265 / 630 / 1,594 / -433; 1,965 / 3,241 / 633 / 1,599 / -423 | same | in |
| Count's deliveries as one, two, four weeks before | 2,118 / 3,445 / 647 / 1,628; 1,661 / 3,360 / 620 / 1,579; 1,563 / 3,249 / 601 / 1,591 | same | in (Component 3 5,092 and 4,664) |
| One or three harmonics; bend a degree either way; quadratic; levels in place of logs; smearing; Christmas weeks | K50 1,850 to 2,208, hot 4,921 to 5,703 | same | in |
| Fitted split (104); slope beside half runs; median; last 52; mean of rackings | FIR 1,537 to 1,654, store 10,033 to 10,234 | same | in |
| Fitted split on all 156 Mondays, alone and crossed | 1,313 alone; 1,249 to 1,295 with one more convention; 1,227 with two; 1,190 only with four more stacked low | same up to three together | out (finding 6) |
| Summer counts only; fitted apart; share from the last year; last count alone for the depots | K50 1,717 to 1,865 | same | in |
| Sensitivities: line 20 per cent, cover 20 per cent, loss 20 per cent, season 5 per cent | K50 1,180 to 2,577; FIR 1,424 to 1,810; K20 520 to 746 | same | as stated in step 11 |
| Hurried routes | in step 5,764 / 4,175 / 2,373 / 791 / -497; tag loss 823 / 2,775 / 633 / 867 / -583; store 385 / 2,658 / -658 / 845 / -582; all three 7,067 / 3,714 / 1,066 / -847 / -877 | flip, as designed | K20 of all three: finding 1 |

Not run: the depots, wash backlog and repair bay week by week from their own records (two of step 11's forty).

**Strongest rival, run.** The tags are the one direct measurement of the response, so the rigorous rival calibrates
on them and carries the result. Carried as a slope (0.927 per container a week): 2,000 / 3,308 / 677 / 1,624 / -431,
in band. Scaling the reps' relation by the check (356 over 299): 2,290 / 3,356 / 677 / 1,582 / -433, in band. Carried
as a share of in step (12.8 or 15 per cent): **520 to 659** / 3,115 / 664 / 1,703 / -415, the same covers but below the
50 litre band and Component 1's (4,260 to 4,451). Refuted from `cellar_audits_2025_2026.csv` without the model:
counted stock at a 50 litre line is 26.6 per cent higher in June to August than in December to February on line
deliveries 86 per cent higher, a ratio of 0.31, where the tagged type shows 0.08 (relation: 0.34 and 0.11). The
blocks' "11 to 34 per cent" reproduces. Sufficient.

**Nearest to a line and to a band edge, readings the blocks admit.** Lines: firkins 1,499 against 1,200; 50 litre
1,308 against nil and 2,457 against 3,500; 20 litre 736 against 1,200; 30 litre 3,146 against 1,500; kilderkins -403
against nil. The only reading nearer is finding 6 (firkins 1,313). Band edges: 20 litre 736 under 743 and hot 1,073
under 1,077; Component 3 5,092 under 5,139; Component 2 10,033 over 9,962; firkins 1,499 over 1,478.

## Gates B, D, E

Pass. Purchase, seasonal hire, no cover and the minimum order run are FS-04 4.1's own words; the runs are in the
quotation; the season, both cases, the float and the requirement are FS-04 2 and 3; the estate, the brew plan, the
normals and ten summers are filed. The one unfiled sentence is finding 8, and no golden figure rests on it. The
prompt pins one figure a type a case, in containers, and one cover; the method is open. Careful answers split on
the data, not on a word.

## Fix (solution)

1. Correct or restate the 20 litre figure of the three-shortcut route (-383) and the in-step rise (9,956): Final
   Recommendation, step 5, closing paragraph.
2. Step 5: the week's own temperature for today's accounts in the hot case; the estate's season without the trend;
   which stay the not-traced rule leaves out.
3. Closing paragraph: 15 per cent against 356 over 2,782.
4. Step 7: refuse the whole-record fitted split with its figures; give the 52 Monday refusal a firmer ground; state
   the window of the week-beginning fit and its R squared for all five types.
5. Step 2: ground "cleaned at the first count" in the first count's figures. Optional: one sentence on the tag
   record's first months.

## Fixes taken (the build thread, 2026-11-17, one generator pass; the pack and the prompt unchanged)

Target digest c2dd65b140fc0d05 and `target.zip` md5 c5e45a78ecb27bfa3e9e46074d8fdcaa are the judged cut's; no stated figure and
no band moved, so no further pass was run. `checks.py` 151 of 151, `verify.py` 23 of 23, two byte-identical builds.

1. Finding 1: the rejected route moves the tagged kegs from their tags (the count at the close of the week 52 weeks earlier, times
   the week's deliveries over that earlier week's, less the tags' count at the count). The rule is now in step 5 and the closing
   passage, so -383 and 9,956 rebuild as stated.
2. Finding 2: step 5 gives the week's temperature in the case being run (its normal in the planning case, the summer's own in the
   hot case).
3. Finding 3: the tags' rule now says the stay after a keg's last delivery is left out where that delivery was closed as not
   traced, and the keg's earlier stays count.
4. Finding 4: the estate's season is the harmonics and the temperature terms of step 3's fit without its level or trend.
5. Finding 5: the tagged kegs' response is given both ways (13 per cent over step 5's rise, 356 against 2,782; 15 per cent by a
   least squares line through the last 104 weekly counts).
6. Findings 6 and 7: a fitted split is used where it stands within one standard error of the racking log's half runs for every
   type, which is the 104 Mondays only; on 52 and on all 156 it is refused in either form, by that rule and by the fixed part's
   drift with the window beside a cover that holds year by year, each with its planning figures (`checks.py` SF42). The mean
   split on all 156 Mondays joined the battery (41 conventions, 834 rebuilds; every band unchanged). The week-beginning fit's
   window and all five R squared are stated.
7. Finding 8: the first count's clear account is grounded in the figure the report gives (off site against the cellar
   relation's stock, every type; `checks.py` SF43).
8. Finding 9: the tags' filling months are stated and the count is read from the count of December 2024 (`checks.py` SF44).
