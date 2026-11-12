# Determinism check, task20 (architecture 2, second hardening)

Run 2026-11-12 on the second hardening's first cut, one isolated judge thread (medium effort) that saw only a fresh
unzip of target.zip, prompt.txt and the graded blocks; it wrote its own derivation before opening the blocks (order
kept, stated in its verdict). Its verdict and derivation follow verbatim, then the main thread's dispositions. The
re-judge after the FIX_NOW repairs is appended below when it lands.

## Verdict (pass 1)

# Verdict, task20 (Brindle & Moss Q4 FY25 nowcast)

Order kept: own_derivation.md was written before graded_blocks.md was opened and was not edited afterwards. Everything computed after opening is labelled "post-open" below.

- **Verdict:** DETERMINISTIC (thin on supplementary answer 3 and on the width of answer 1's band; no SOLUTION_WRONG found in the figures I could recompute).
- **Disposition:** FIX_NOW. Solution-block edits only, no model rerun: (a) state in answer 3 the order, the baseline and the unit the bridge is applied in, so a differently ordered bridge is graded fairly; (b) widen the estimate band at the top to about USD 1,484 million, because a defensible calibrated path lands at 1,476 to 1,481; (c) state the information set of the "three weeks before release" record. The pack and prompt do not change.
- **Why:** The call is forced by three data-visible effects, each of which I confirmed in the files after opening the blocks: KS-01 Midwest cards 61,377 to 72,596 (+18.28%) in the four weeks to 26 Oct 2025 as KS-06's fell and its feed ended (cards table, panel file); customer deposits recognised on delivery (8-K balance sheets; adding the deposit-change term cuts slope-1 RMSE against reported brand growth over 15 quarters from 1.31 to 0.76 points); and Q4 FY24 contract of USD 54.5 million against a run rate near 17.7. With all three the estimate is about 1,471 to 1,481 and the top of any reasonable range is 1,489 to 1,502, under the street's 1,518.0 (mean of 11; median 1,516.3). Weaknesses are in the asking, not the answer: the prompt never names the "steps" in answer 3 (Gate E, answer 3 only) and the record's information set is unfiled. Taxonomy label: none (with prompt_ambiguity noted on answer 3, fix location solution).

## Evidence
Recomputed from target/ (R = reproduced):

| Item | Blocks | Mine | R |
|---|---|---|---|
| Delivered panel, every issuer, YoY | -21.86% | -21.86% | yes, exact |
| KS-01 Midwest cards, 4 weeks to 26 Oct | +18.28% | +18.28% | yes, exact |
| Q4 FY24 contract / run rate | 54.5 / 17.7 | 54.545 / 17.7 (median of last 8 quarters) | yes |
| Custom share Dec-Jan, 2025/26 vs 2024/25 | 40.43 / 35.93 | 40.43 / 36.05 (Dec 36.05, Jan 36.04) | yes within 0.1 |
| Last-8-weeks share of payments, K1-5 | 57.00 / 56.09 | 57.00 / 56.18 | yes within 0.1 |
| Closing deposits 335.2 | 335.2 | 282.109 x 1.0391 x 1.0162 x 1.1252 = 335.2 | yes |
| Street | 1,518.0, median 1,516.3 | 1,517.99 / 1,516.3 | yes |
| Card-visible growth, regional mix, K1-5 | 7.18% | 7.41% | within 0.25 |
| Same, KS-01 out | 3.90% | 4.27% | within 0.4 (about 5 million) |
| Region growth, KS-01 kept / out (Midwest) | 9.51 / -2.09 | 9.2 / -1.9 | within 0.4 |
| Completion lag 0-2 (pooled first-delivered share) | used for +1.22 | 0.807 / 0.960 / 0.995 (stable by issuer) | step +1.66 vs 1.22 (band 0.91 to 1.99) |
| Licensee removal | -0.87 | -1.20 (band -1.52 to -0.56) | inside |
| Record 13 of 15, RMSE 1.24 | not reproduced to the row; a simplified rolling-origin version (regional-weighted, 80% t-interval, 9 quarters) gave 7 of 9 covered | | unverified |

Forks tried and what they give (post-open):
- Deposits: build forecast by trend (about 106 against the block's 114.5) is worth about -1.75 points against -2.19; inside the stated band (-3.40 to -1.54).
- KS-01: standardising by card-open year (KS-01 kept) gives 2.3% against 3.90%, more bearish, still short. Dropping KS-01 gives 4.27 on my cut. Both keep the call.
- Calibration: OLS of reported on (card growth minus deposit effect) has slope 0.85, intercept 0.6; applied to my 4.27 and a 2.2-point deposit effect it gives about 1,480.5 (slope 1, no intercept: 1,476.4). The block's estimate is 1,471.2 with band 1,462.3 to 1,480.2, so rivals reach the edge of the band. Top of range on that path is about 1,495 to 1,496, still 22 under the street.
- Contract carried at last year's level: about 1,509 estimate; the block marks it no position. Nothing filed says the Q4 FY24 delivery is non-recurring; the data do (spikes of 23.8, 23.2 and 54.5 fell in three different quarters and Q4 was 14 to 16 in FY21 to FY23), so it is forced by the data, not by a document. I class it as a defensible-looking but weaker rival, ruled out by named data.
- Street as mean or median: same call.
- Any single correction left out moves the range across the street (blocks' claim); consistent with my arithmetic (KS-01 alone is worth about 3.3 points, about 47 million).

Own derivation (written before opening the blocks, unchanged) against the stated bands:

| Result | Band in the blocks | My unchanged derivation | Inside |
|---|---|---|---|
| Net sales estimate | 1,462.3 to 1,480.2 | 1,539.2 (contract at run rate) or 1,575.5 (contract carried) | no |
| Lower end of range | 1,434.5 to 1,459.8 | about 1,513 or 1,550 | no |
| Upper end of range | 1,485.7 to 1,504.9 | about 1,566 or 1,600 | no |
| Growth after panel steps / at company mix | 9.22 / 7.18 | 9.53 / 7.41 | yes (rounded figures differ by 0.2 to 0.3) |
| Record RMSE (points) | 1.24 (0.92 to 1.61) | 1.24 (calibrated residual SE) | yes |
| Record coverage | 13 of 15 (9 to 13) | 7 of 9 (different quarter count) | not comparable |
| Completion step | +1.22 (0.91 to 1.99) | +1.66 | yes |
| Licensee step | -0.87 (-1.52 to -0.56) | -1.20 | yes |
| Regional mix step | -2.04 (-4.81 to -1.33) | about -2.1 | yes |
| KS-01 re-issued book | -3.28 (-3.58 to -0.35) | not found, 0 | no |
| Revenue on delivery (deposits) | -2.19 (-3.40 to -1.54) | not applied (flagged the lag, did not price it), 0 | no |
| Contract at run rate | -2.55 (-3.12 to -2.25) | -2.5 (fork A), 0 (fork B) | yes / no |
| Call | short | no position or long (A borderline, B long) | no |

Post-open refined path (not part of the unchanged derivation): about 1,476 to 1,481, range top about 1,495, short, i.e. at the edge of the blocks' estimate band and inside the call.

## Files/Hygiene
PASS. 27 files: 19 8-K exhibits (txt), 6 CSV (panel 163,620 rows, descriptor 3,276, delivery history 910, web visits 261, app 1,068, street 11), 1 PDF (10-K excerpt, one page), 1 xlsx (desk model). Four formats. Two large messy CSVs (panel; descriptor, many pages). Two unlabelled distractors (app downloads, web visits). Region labels (15 spellings of 4), merchant name variants, late-arriving weeks, an issuer that leaves, one that jumps: all produced by the feeds, not labelled. Temporal coherence holds (latest street estimate 3 Feb 2026, panel delivered 2 Feb, release 26 Feb). Boilerplate repeats across 8-Ks as real exhibits do. Minor: the panel and delivery file names say "delivery", which points at the late-data issue; the descriptor file's January 2026 is the complete month while the panel's is not (7.1 per cent higher), a second route to completion that the blocks do not use. No provenance, benchmark or authoring text seen. No exclusion-level finding. Company and brokers are fictional, so no public-data contamination.

## Stump power
Good spread. A ten-minute run files the desk model or the panel's like-for-like read (1,590 to 1,611, long) and loses the estimate, both range ends, the call and most of the bridge. A careful but hurried afternoon finds completion, licensee, regional mix and probably the contract spike (about 1,535 to 1,560, no position or long) and loses KS-01 (-3.3 points), deposits (-2.2) and so the call; two days of checking reach all of it. The record is the likeliest place for a clean run to lose small points (the information set). The most useful single sentence ("KS-01 took over KS-06's cards") rescues about 3 of about 14 graded results (CC1, the KS-01 step, the regions table) and does not rescue the call; the deposits sentence rescues about 3 and not the call either.

## Stumping type
mechanism: forecasting (nowcast) with decomposition_attribution; stumping_family: analytical_non_defect, borderline (the panel's like-for-like read is a surface read the answer rejects, and KS-01 is a constructed event, so route to live testing); surface_read_dependency: no (borderline); sole_data_defect: no (on clean data, without the KS-01 event, deposits, contract, regional mix, completion and licensee still put the hurried read about 80 to 100 million too high and the call is still lost).

## Deep reasoning
domain: pass (card-panel nowcast of retail net sales against the street, bridge from sample to reported revenue, back-test of the range; swap the nouns and it stops making sense); layers: pass (Layer 1: feed labels, late weeks, issuer exits and re-issue, descriptor mix, 8-K tables; Layer 2: panel-to-sales model, deposits timing, contract separation, interval and record); results: 14 graded across 7 areas (assembly, measurement, modeling, validation, decomposition, forecasting/uncertainty, synthesis); one_thing: none, with a shallow_hidden_factor note on KS-01 (constructed, present only in the deciding quarter and units, one filter after one sentence) which carries about a fifth of the results; effort: quick 2, careful 7, thorough 14 of 14; one_fact: "KS-01's Midwest cards are KS-06's re-issued accounts" rescues 3 of 14.
The weight of the work sits in assembly of the card-to-sales bridge and the timing step; a careful but hurried run is likeliest to lose the deposits step and files about 1,535 to 1,560 (growth about +3.5%).

## Fix
solution (no rerun): (1) answer 3: state the bridge order and the baseline, and give the step bands in a form that survives re-ordering (or grade the bridge in total plus each step's sign and a band); (2) answer 1: widen the estimate band to about 1,462 to 1,484 and the upper-end band accordingly, since calibrated and trend-deposit rivals reach 1,481; (3) answer 2: state which data are treated as known at each past release (vintage or final) and give the coverage band against the number of quarters tested; the prompt's "past quarter it could have been built for" leaves the minimum training length open; (4) note in the Step-by-Step why contract is run-rate (the earlier spikes in Q2 FY22 and Q3 FY23 did not recur in the next year's same quarter, and Q4 was 14 to 16 in FY21 to FY23) so the data, not assertion, rules out carrying 54.5. Prompt and files stay byte-identical.

## Own derivation (pass 1, written before the blocks were opened)

# Own derivation (written before opening graded_blocks.md)

Inputs used: kestrel panel weekly (163,620 rows, 2021-01-31 to 2026-01-25, 6 issuers, 3 merchant ids M0412 B&M, M0413 .com, M2290 Fernhollow), delivery history (27 deliveries, 6 weeks each), descriptor monthly detail, the 20 8-Ks (quarterly brand tables; Q4 by FY less 9M), the 10-K excerpt (regional net sales FY21-24, licensee statement, Fernhollow acquired 2 Jun 2024, 14-week Q4 FY23), Larkhill workbook (a prior model: per-card spend growth, slope 0.737, intercept 0.77, RMSE 1.3, Q3 FY25 miss: model 1333.7 vs reported 1306.9), street csv (11 brokers; mean of latest 1517.99, median 1516.3, prior mean 1523.9).

## Facts established
- Fiscal calendar reproduces the 8-K quarter ends (Q4 FY25 = weeks starting 2025-11-02 .. 2026-01-25, 13 weeks). Q4 FY23 was 14 weeks (not the target, but matters in the back-test: use per-week).
- Q4 FY24 base: 1483.678 (B&M 1320.081, Fernhollow 109.052, Contract 54.545). Contract Q4 FY24 is a spike (Q4 FY21/22/23: 16.4/14.3/14.5; Q1-Q3 FY25: 17.5/19.1/17.9).
- Panel messy: region labels 15 spellings -> 4; merchant name variants (use id); no duplicates.
- Late-arriving data: delivery history shows each issuer-week at age 1..6 weeks. Completion (delivered / final) pooled age1 0.807, age2 0.960, age3 0.9946, age4+ 1.0; stable by issuer (age1 0.747 KS-05 to 0.857 KS-02). The 2026-02-02 file therefore understates weeks 2026-01-25 (age 1), 01-18 (age 2), 01-11 (age 3). Effect on Q4 per-card growth: about +1.7 pp (as delivered 7.39 -> completed 9.05 on the licensee-excluded Larkhill-style measure). Descriptor file January 2026 is 1.071x the panel file January (descriptor is complete), consistent with this.
- Licensee descriptors inside M0412 (B&M AT HOLLISTERS shop-in-shops, BRINDLE CAFE) are not net sales (10-K). Share of M0412 rose 11.6 pct (Jan 2025) to 13.0 pct (Jan 2026); Q4 FY24 about 11.9 pct, Q4 FY25 about 13.4 pct. Removing them lowers Q4 per-card growth about 1.2 pp. Descriptor months = fiscal week_start months (reconciles to panel exactly).
- Panel composition: KS-06 leaves after 2025-10-26 (not in Q4 FY25); KS-04 enters 2022-06, KS-05 2023-12; KS-02 jumps 2023. Use issuers in both quarters (KS-01..05 for Q4).
- Panel is not representative by region: billing-region card share (NE 9-11 pct, MW 30-41 pct) vs 10-K sales share (NE 26-31 pct). Per-card growth by region very different (SE +14-24 pct, W +8-13 pct, MW 0-3 pct, NE -4 to +2 pct). Reweighting to 10-K prior-year regional sales shares improves fit to reported B&M growth (corr 0.50 -> 0.66; RMSE 1.32 -> 1.15 pp).
- Card-open vintage: newest cohorts spend 10-25 pct more per card than older (Q4 FY25: 2025 cohort 5.3 vs ~4.3 per card-week). Aggregate per-card growth is inflated by new cohorts (same-vintage growth about 3.6 pp lower). Standardising did not improve the back-test fit (corr 0.42-0.62), so it is a judgment; reported as a sensitivity.
- Lag (deposit to delivery): customer deposits fall 282 -> 221 over Q3->Q4 etc.; card spend leads sales. Lag scan of 0-8 weeks is noisy (best corr at lag 1 or 6, ~0.7); not pinned by the files; sensitivity only.

## Step values (Q4 FY25 YoY card growth measure, stable issuers KS-01..05, per card-week)
1. Larkhill-style raw (M0412+M0413+M2290 as delivered): +8.59 pct.
2. + licensee removed: 7.39 (-1.20 pp).
3. + late-data completion: 9.05 (+1.66 pp). (Fernhollow-excluded variant 9.42 / 9.53 Laspeyres issuer-weighted.)
4. + reweight to 10-K regional sales mix: 7.41 (-2.1 pp vs 9.53 Laspeyres issuer measure).
5. + (sensitivity) vintage standardisation: lowers by a further ~2-3.5 pp, but calibration intercept offsets it (predictions 5.3 to 7.1 pct).
6. Calibration to reported B&M per-week growth, 15 quarters FY22Q1-FY25Q3 (OLS): slope 0.64, intercept 1.96, residual SE 1.24 pp -> predicted B&M brand YoY +6.71 pct.
   Variants for the predicted B&M growth: no regional reweight 7.62; reg-weight lag 1 wk 6.92; lag 6 wk 5.89; vintage-standardised 5.3-7.1.

## Net sales build (USD m), primary method
- B&M brand: 1320.081 x 1.0671 = 1408.7; 80 pct (t, 13 df, incl. parameter uncertainty) +-1.8 pp -> [1385.0, 1432.5].
- Fernhollow: M2290 per-card growth (region-weighted 2.3, unweighted 4.4; Q3 FY25 reported +3.7 vs card 3.65/4.28) -> about +3 pct: 112.3 (111-114).
- Contract: no card signal. Fork A: reverts to run rate 18.2 (Q1-Q3 FY25 mean). Fork B: carry Q4 FY24 54.5 flat. Files do not pin which; lumps seen 23.8, 23.2, 54.5.
- Total: Fork A 1539.2, range about [1513, 1566]. Fork B 1575.5, range about [1550, 1600].
- Alternative methods for B&M growth (5.9 to 8.1 pct) move the total between 1522 and 1590.

## Back-test (rolling origin, min 6 training quarters, 80 pct t-interval, regional-weighted measure, B&M growth)
2023Q3..2025Q3 (9 quarters): covered 7 of 9 (78 pct); misses 2024Q4 (pred 7.38 vs 5.22) and 2025Q1 (4.13 vs 6.26). Minimum training length (6 vs 7 vs 8) is not filed: fork on the number of quarters tested (9, 8 or 7) and hence on the stated coverage (7/9, 6/8, 5/7...).

## Call
Street = 1517.99 (mean of 11 latest) or median 1516.3 (not filed which). Fork A: range lower end (about 1513) is a hair below the street -> "no position"; borderline. Fork B or any method with B&M growth above ~6.9 pct -> long. So the literal call depends on the contract assumption and on the B&M method: central estimate is above the street (1539 vs 1518, +1.4 pct), but the whole range clears only under the more bullish variants.

Options where the text is silent (literal readings): street = mean vs median; contract spike treatment; regional reweighting (10-K billing vs store region mismatch); vintage standardisation; lag; min training window for the back-test; range built on B&M growth vs total; completion factor by issuer vs pooled.

## Dispositions (main thread)

- FIX_NOW (a), Ask 3's baseline, order and unit: made. Ask 3 now states the baseline (the delivered panel's growth on the
  same quarter a year earlier: every issuer, raw spend, the panel's own regional weights), the unit (points of
  year-on-year growth, weekly averages), the order (the panel's three steps at the panel's weights with KS-01 kept,
  then the company's four at the company's) and that each band covers every order of the steps within its group.
- FIX_NOW (b), the estimate band: made. A retail-calibrated path (reported retail growth regressed on the chain's retail
  growth over the origins before, contract at its run rate) joins the golden family at USD 1,478.4 million (top
  1,505.8, short), and the estimate and range bands take a USD 5 million margin on the family.
- FIX_NOW (c), the record's information set: made. Ask 2 states it (the panel as delivered on 2 February 2026, the
  issuers less any with a re-issued book between the quarters, the prior fiscal year's regions, deposits and contract
  from the releases before each quarter's); fork row SF24.
- Fix 4, contract's run rate argued from the data: made in Step 6 (the fiscal 2022 Q2 and 2023 Q3 deliveries did not
  recur a year on; fourth quarters ran 14.3 to 16.4 in fiscal 2021 to 2023).
- The record's coverage (pass 1 found 7 of 9 on a rolling calibrated back-test): Ask 2 now states both readings with
  their bands (at the record's own error, and built only on the errors before each), fork row SF23, and grades each
  quarter's error in its own band, which is the prompt's ask ("how that range would have held in each past quarter").
- The Gate H note on KS-01 (constructed, the deciding quarter only): the process runs across the record. KS-02 took an
  outside book in May 2023 (Southeast cards up 35.44 per cent in four weeks), which pass 1 itself noted ("KS-02 jumps
  2023") and which moves the record's fiscal 2023 Q2 to fiscal 2024 Q2 errors; with the record graded quarter by
  quarter that book is now graded too.
- House rule: pass 1's own derivation landed R1, R3, R5 (contract at a run rate as one of two forks) and R8's mix and
  contract steps inside their bands, and missed R2, R4, R6 (quarter by quarter), R7 and R9: priced that way the careful
  column is 39.6, under 50.

## Verdict (pass 2, the re-judge after the FIX_NOW repairs)

# Verdict, task20 (Brindle & Moss Q4 FY25 nowcast)

Order kept: own_derivation.md was written before graded_blocks.md was opened. Only /tmp/determinism-check-task20-h3/ was read.

- **Verdict:** DETERMINISTIC (no SOLUTION_WRONG; every load-bearing figure I could rebuild reproduced, a few within rounding).
- **Disposition:** APPROVE. No rerun needed. Optional tidy-ups (not required): state in the answer blocks that the street figure is the mean of the 11 latest estimates (mean 1,518.0 and median 1,516.3 give the same call), and tighten the asymmetric "13 of 15 (7 to 13)" band on the in-range count.
- **Why:** The short call rests on three independent corrections the shipped files force: KS-01's Midwest card base jumps 61,377 to 72,596 in the four weeks to 26 Oct 2025 (cohort 2025 cards, 9.6k to 21.6k) while KS-06's Midwest cards fall and its feed ends, which the other issuers' Midwest cards do not show (without KS-01 the Midwest is -2.09% against 9.51%); customer deposits on every 8-K balance sheet track the last eight weeks of custom-order payments at a stable ratio (0.0269 to 0.0283 over 19 quarters) and the custom share of those weeks jumps to 40.4% (36.0% a year earlier), so revenue on delivery lags payments by about 2.2 points; and last year's Q4 Contract of USD 54.5 million (annual 100.4 less nine months 45.9) is a one-off against Q4s of 14.3 to 16.4 in FY21 to FY23. Left out singly, each puts the range across the street (golden says USD 1,502 to 1,510 estimates, no position), so the task is hard and forced at the same time, and the call survives every rival I ran.

## Evidence (recomputed from target/)

| Item | Golden | My recomputation | Status |
|---|---|---|---|
| Raw delivered panel growth, all issuers, total spend | -21.86 | -21.86 | reproduced |
| Completion of three late weeks (issuer medians over 27 vintages) | +1.22 (0.91 to 1.99) | +1.22 (pooled factors +1.48) | in band |
| Licensee shops and cafes out (monthly descriptor share) | -0.87 (-1.52 to -0.56) | -0.87 (my order -1.21) | in band |
| Regional growth with KS-01 / without (NE, SE, MW, W) | -2.57/-3.79, 13.77/13.29, 9.51/-2.09, 8.08/7.77 | identical to the hundredth | reproduced |
| Growth at company FY24 mix (23.87% MW) | 7.18 | 7.18 (weekly avg 7.177) | reproduced |
| Growth without KS-01 | 3.90 | 3.90 | reproduced |
| Matched-issuer per-card growth before mix | 9.22 | 9.06 | small gap (0.16), inside bridge band, not load-bearing for the call |
| Custom share of last 8 weeks / share of payments in them | 40.43 vs 35.93; 57.00 vs 56.09 | 40.43 vs 36.05; 56.95 vs 56.13 | reproduced to rounding |
| Closing deposits | 335.2 (326.8 to 340.2) | 333.5 (ratio chain), 334.7 (deposit/custom8 ratio) | in band |
| Retail net sales after deposits | 1,453.5 | 1,454.1 | in band |
| Contract run rate / last year Q4 contract | 17.7 (16.7 to 19.5) / 54.5 | 17.69 (median of last eight quarters) / 54.545 | reproduced |
| Estimate | 1,471.2 (1,460.3 to 1,483.4) | 1,471.8 | in band |
| 80% range | 1,447.7 (1,432.5 to 1,461.8) to 1,494.7 (1,483.7 to 1,510.8) | 1,448.3 to 1,495.3 on the golden's own error of 1.58 points | in band |
| Street | 1,518.0 mean, 1,516.3 median | 1,517.99 / 1,516.3 | reproduced |
| Hurried path (like-for-like growth to net sales) | 1,590.2 | 1,483.678 x 1.0718 = 1,590.2 | reproduced |
| Record errors, RMSE, in-range count | RMSE 1.24, 13 of 15 | from the golden's listed errors: RMSE 1.236, 13 of 15 inside +/-1.58 | arithmetic holds; I did not rebuild each quarter's as-built estimate to the second decimal |

Own derivation (written first, before the three corrections were found): B&M 1,402 to 1,415 (80% 1,380 to 1,437), plus Fernhollow 113.5, plus Contract 18 to 65, total 1,540 (1,518 to 1,563) at Contract 18.2, 1,577 at 54.5; call long or no position (knife edge at the street). It used completion, matched issuers, licensee out, region reweight and a 15-quarter regression; it explained the Midwest step-up as the new Columbus studio and missed deposits. That first-pass answer lies outside the bands for the estimate (1,460.3 to 1,483.4), the range ends and the call, which is the intended hurried failure; the pieces it did find (completion +1.48, licensee -1.21, regional reweight -1.9, contract level 18.2 and its -2.45 points, RMSE 1.15, street 1,518.0) fall inside their bands.

Extra rivals I ran on the corrected chain, all keep the top below the street: bias-corrected estimate 1,480.6 with the error standard deviation gives top 1,501.5; the error 10th percentile gives top 1,500.0; deposits from the deposit/custom-payments ratio gives 1,471.8; contract at the mean of FY25 Q1 to Q3 (18.2) moves the estimate +0.5. Deposit ratio checked quarter by quarter: 26.9 to 28.3 (scaled units), no break.

Forks examined, none flips the call on the corrected chain: street mean vs median vs latest-only (1,516 to 1,518, and the lowest broker 1,506.4 to highest 1,532.1 still leaves the top below the median); completion factors pooled vs by issuer vs medians; weights FY24 vs rolled; range from RMSE vs percentiles; window of 7 vs 9 weeks for deposits (golden lists it). The one judgement left in the chain is Contract: grown with retail or repeated, the range straddles the street (golden's own 1,509.0 rival), so the call depends on reading the Q4 FY24 Contract delivery as non-recurring. The files support that reading (Q4 FY21 to FY23 at 16.4, 14.3, 14.5; earlier spikes of 23.8 and 23.2 not followed by repeats; FY25 Q1 to Q3 run at 17.5, 19.1, 17.9), so I treat it as forced, with a margin of 12 to 23 million to the street.

## Files and hygiene: PASS
27 files: 6 CSV (panel 163,620 rows; descriptor 3,276 rows; delivery history; web visits; app daily; street), 19 txt 8-K exhibits, 1 xlsx (3 sheets, no formulas, plausible Excel properties), 1 PDF (LibreOffice export, one page). Four formats; two large messy CSVs; unused look-alikes (web visits, app daily) unlabelled. Mess is process-like (11 region spellings, 8 merchant-name spellings, descriptor drift in Aug 2024, KS-06 feed ending, incomplete latest weeks, one calendar-month tail in the descriptor file). No authoring or benchmark disclosure found, no README. Temporal: the street file carries one estimate dated 3 Feb 2026, a day after the 2 Feb panel delivery, and the file copy is dated 4 Feb; harmless to the call. The fact that deposits are recognised on delivery is not written in any file; it is the standard reading of a customer-deposit liability and is confirmed by the data (stable deposit-to-custom-payments ratio), so not a Gate B failure. No public-data contamination (fictional company). No exclusion-level finding.

## Stump power (Gate F)
Strong. The ladder from the delivered panel to net sales has 8 steps of 1 to 31 points; a run that stops at the like-for-like panel growth files 1,590 (a beat) with a record that looks clean (RMSE 1.45); the desk's model carried forward files 1,611. Leaving out any one of KS-01, deposits or Contract turns the short into no position, two out turns it long. A careful but hurried frontier run likely does completion, licensee, issuer matching and the regional reweight (it saw the Midwest bump) but is likeliest to lose the deposit-timing step (-2.19 points, deposits 335 against 220.7, a step it would have to infer from the balance sheet line plus custom descriptors) and to explain KS-01's book as a real Midwest studio effect, filing about 1,500 to 1,540 and a long or no-position call.

## Stumping type (Gate G)
`mechanism: decomposition_attribution` (with modeling and forecasting layers), `stumping_family: analytical_non_defect`, `surface_read_dependency: no`, `sole_data_defect: no`. The reported figures are fine; the difficulty is bridging a sampled payments panel to recognised net sales and a record of how that bridge held. Not a banned type. Caveat: part of the work does consist of catching that the panel's growth is inflated (KS-01 book, deposits), but three separate corrections, a bridge, a record and a range each need their own work and the clean-data test still leaves a hard forecasting task.

## Deep reasoning (Gate H)
`domain: pass` (card-panel nowcast of a retailer's quarter, panel-to-reported mapping, record of intervals, street comparison, which is what an equity research analyst estimates; swap-test fails when "net sales" and "street" are replaced), `layers: pass` (layer 1: region and name drift, licensee descriptors, incomplete latest weeks, departing issuer, 14-week quarter; layer 2: bridge, re-issued book, deposit timing, contract base, record), `results: 11 graded across 7 areas` (call, estimate and range, record, regions and KS-01, completion, licensee, deposits, contract, mix, bridge totals, note), `one_thing: none`, `effort: quick 3, careful 7, thorough 11 of 11`, `one_fact: "KS-01 took over KS-06's Midwest cards" rescues 2 of 11` (the KS-01 step and the regional table; the other two big corrections remain). The weight sits in the bridge and the as-built record; the result a careful but hurried run is likeliest to lose is the deposit step, filing retail growth about 3.9 points and net sales near 1,500 to 1,540 against 1,471.

H3 watch item (does not fail): three of the constructed effects sit mostly in the deciding quarter (KS-01 migration, the Dec to Jan custom-share jump to 40.4%, Q4 FY24 Contract is in the base). Each has an in-history analogue the data shows (KS-02's May 2023 book jump with the same signature, earlier Dec custom bulges of 32 to 36%, earlier one-off Contract quarters), and no single sentence rescues more than 2 of 11, so I count them as analysis, not a planted flip.

## Fix
none (solution, prompt and input files stand). If the author wants more margin against a reviewer who prefers a regression mapping: add one sentence to the Record block that the identity mapping has a mean error of -0.64 points and that a bias-corrected range still tops out at about 1,501 to 1,506 million, below the street.

## Own derivation (pass 2, written before the blocks were opened)

# Own derivation (written before opening graded_blocks.md)

Source: prompt.txt and target/ only. Scripts in work/ (load.py, fq.py, build.py, growth.py, reg.py, model.py).

## Files and what they hold
- panel weekly (163,620 rows, 2021-01-31 to 2026-01-25, 261 weeks, 6 issuers KS-01..06, 3 merchants M0412 stores, M0413 web, M2290 Fernhollow). Region labels in 11 spellings (NE, North East, MW, Mid-West, ...) fold to 4 regions; merchant_name in 8 spellings fold to 3 ids. No duplicate keys. panel_cards repeats identically over merchants for the same week-issuer-region-cohort cell.
- delivery history: 27 weekly vintages x 6 weeks x issuer. Newest week of a vintage is ~80 per cent complete (issuer range 0.75-0.88), next ~96 per cent, third ~99.5 per cent, then final. The panel file (delivered 2026-02-02) equals the lag-0 vintage, so weeks 2026-01-25, 01-18, 01-11 are incomplete.
- descriptor monthly: same panel by calendar month of week_start (matches panel totals to the cent except 2026-01 which is 1.0709x the panel, i.e. it is the completed month). Contains licensee descriptors inside M0412 (B&M AT HOLLISTERS x8, BRINDLE CAFE / SQ CAFE x3) = shop-in-shops and cafes whose sales are NOT net sales (10-K). Licensee share of M0412 spend rises from 6.9% (2021-02) to 13-14% (2025).
- 10-K excerpt: fiscal calendar (FY24 52 wks to 1 Feb 2025; FY23 53 wks with 14-week Q4), licensee exclusion, region table FY21-FY24 (annual B&M net sales by store/delivery region), Fernhollow acquired 2 Jun 2024.
- 19 8-Ks: quarterly total net sales and brand splits (Q4 brand = annual minus 9M). Q4 FY24: B&M 1320.1, Fernhollow 109.1, Contract 54.5, total 1483.7.
- Larkhill xlsx: Index of card growth vs reported "comparable" growth (comparable = ex-Fernhollow, 14-week Q4 FY23 scaled 13/14, Contract included), Fit (intercept 0.77, slope 0.737, RMSE 1.3), Q3 FY25 call (model 1333.7 vs reported 1306.9, miss -2.0%). I reproduced the fit from Index (a=0.757, b=0.738, resid sd 1.52 with n-2, 1.41 RMSE).
- street: 11 brokers, latest figures mean 1518.0, median 1516.3, range 1506.4-1532.1, prior figures mean about 1522.
- web visits, app daily: not used in my chain (looked relevant, no fit improvement tested beyond not needed).

## Findings that change the card measure (each a step)
1. Newest three weeks incomplete (factors by lag pooled 0.807/0.960/0.995; issuer-specific 0.75-0.86 for lag 0). Check: completed Jan-2026 M0412 spend 8.80M (pooled) / 8.85M (issuer-specific) vs descriptor file 8.87M.
2. Issuer KS-06 left after week 2025-10-26 (no Q4 FY25 rows). Issuers are regionally concentrated (KS-06 88% Midwest, KS-02 80% Southeast, KS-03 82% West, KS-01/KS-05 balanced) and grow at very different rates (KS-06 about 0-3%, others 5-15%). So the issuer set must be matched across years.
3. Licensee spend (Hollister shop-in-shops, cafes) inside M0412 to be removed; its share keeps rising, so including it overstates growth by about 1.2 points of card growth in Q4 FY25.
4. Panel is skewed to Southeast and West versus the 10-K net sales split (panel cards SE 39-41%, W 34-35%, NE 12%, MW 13%; B&M sales FY24 NE 26%, SE 26%, MW 24%, W 25%). Per-card growth by billing region in FY25 is SE +14-15, W +6-9, NE -3, MW -1 (till Q3) so unweighted per-card growth overstates national growth by about 2 points. Reweight regions to prior-year 10-K sales shares (FY24 for FY25).
5. Midwest per-card spend steps up about +10 points YoY from week 2025-10-19 (Columbus design studio first appears 2025-11; Tampa 2025-09, Phoenix 2025-10). Studios 8->11 in the Q3 8-K. Midwest now rests on the small Midwest cards of the other issuers since KS-06 left.
6. Contract (and Fernhollow) are separate: Contract is not on the cards at all. Contract by quarter: FY24 14.5, 13.3, 18.1, **54.5**; FY25 17.5, 19.1, 17.9, ?. Q4 of FY21-23 was 16.4, 14.3, 14.5. Q4 FY24 Contract is about 4x any earlier Q4, and it contaminates the Larkhill "comparable" growth for FY24 Q4 (8.41 reported incl. Contract vs B&M-only 5.22) and so its fitted line.
7. Fiscal calendar: Q4 FY23 had 14 weeks; Larkhill scales 13/14. Weeks align on Sunday starts; FY24 Q1+ compare against a quarter 53 weeks earlier by calendar but same fiscal week.

## Ladder for Q4 FY25 card growth (pooled per card-week, YoY; Nov 2 2025 - Jan 31 2026 vs Nov 3 2024 - Feb 1 2025)
- as delivered, all issuers, all merchants: +4.54 
- complete the three late weeks (pooled factors): 6.02 (+1.48)
- match issuers (drop KS-06 from base year): 10.11 (+4.09)
- remove licensee spend: 8.90 (-1.21)
- B&M scope only (store ex licensee + web): 9.27 ; Fernhollow card growth +4.15 (pooled) 
- reweight regions to company sales shares: 7.35 (-1.9 vs 9.27)
- map to reported B&M growth by regression of reported B&M growth (13-wk basis) on this measure, 15 quarters FY22Q1-FY25Q3: a=1.57, b=0.731, resid sd 1.15 (corr 0.71) -> B&M growth +6.9 (6.7 with five-issuer-only history)
Order of the steps is not pinned; points per step depend on order (listed in the order above).

## Estimate (primary chain: pooled completion, five matched issuers all quarters, ex licensee, region reweight, 15-quarter OLS, t-based 80% prediction interval)
- B&M Q4 FY25: 1408.7 (80%: 1386.4 - 1431.0) [variants over completion/issuers/weights/spend scope: point 1402-1415, interval half width 21-22].
- Fernhollow: 109.05 x (1.037 to 1.042) = 113.1-113.6 (card growth 4.15, Q3 reported growth 3.7). Small.
- Contract: no card information. Scenarios: recent run-rate 18.2 (FY25 Q1-Q3 mean); Q4 FY21-23 average 15; flat at 54.5 (Q4 FY24 repeat); 54.5 x YTD growth 18.7% = 64.7.
- Total: Contract 18.2 -> 1540.4 (80%: 1518.1 - 1562.7), growth +3.8%; Contract 54.5 -> 1576.7 (1554.4 - 1599.0), +6.3%; Contract 64.7 -> 1587 (1565-1609).
- Street: mean of latest 1518.0 (median 1516.3; with priors about 1522; Pell & Sutter estimate dated 2026-02-03 is after the 2026-02-02 delivery).
- Call: point is above street in every variant (1540 to 1587). Whole range above street only if Contract is placed at or above about 20 (low end 1518.1 vs 1518.0, i.e. a knife edge at Contract 18.2); with Contract 54.5 or 64.7 the range sits above by 36-50M (long). If Contract is given its own uncertainty (15 to 65) the range widens to about 1500-1610 and straddles the street (no position). Variants without the region reweight (B&M 1392-1398 / low 1370-1376) put the low end at 1505-1510, below street (no position).

## Record (how the 80% interval would have held)
Expanding-window OLS on B&M reported growth, t interval, B&M only, first 8 quarters as training: 7 quarters FY24Q1-FY25Q3, 5 of 7 inside (misses FY24Q4 5.22 vs [5.30, 8.25], FY25Q1 6.26 vs [2.30, 5.70]); with 6 training quarters 7/9; with 10 training quarters 3/5. Window choice moves the count; the quarters that miss are the same ones (FY24 Q4, FY25 Q1). Larkhill-style unadjusted index (no clean-up) in-sample residual sd 1.4-1.5 -> its interval is wider but misses Q3 FY25 by -2.0 per cent.

## Literal-reading forks recorded where the text is silent
- Street figure: mean vs median vs include Pell & Sutter/dated after panel; prior vs latest.
- Contract in Q4 FY25 (no data): 18 vs 54.5 vs 65 -> up to 47M difference, 3 points of growth; decides long vs no position.
- Whether region reweighting is applied (and weights prior-year vs current-year, FY25 weights not published).
- Completion factors pooled vs by issuer; whether descriptor Jan-2026 is used.
- Backtest minimum training length and whether history is rebuilt with vintage panels (only Aug 2025+ vintages exist) and whether Contract-contaminated FY24 Q4 is in the training target.
- Order of ladder steps (points per step).
- 80% band: t vs normal, prediction vs confidence interval, whole-sales vs B&M-only residual.

## Dispositions after pass 2 (main thread)

- APPROVE stands. The optional tidy-ups are made: the street figure stated as the mean of the eleven estimates (the
  median gives the same call); the in-range counts' bands taken from the routes whose record covers every quarter, one
  either side because a count moves by one when an error near the range's edge crosses it (13 of 15, band 12 to 14);
  the count built only on the errors before each stated from four errors (9 of 11, band 8 to 10) and from six (7 of 9,
  band 6 to 8); the record's mean error (-0.64 points) added back with the range from the errors' standard deviation
  tops out at USD 1,500.8 million, below the street, stated in Ask 2 and the closing.
- House rule on pass 2's own first pass: inside the bands it landed the panel steps, the regional mix and the contract
  run rate; it explained KS-01's Midwest step-up as the new Columbus studio, missed the deposits and filed USD 1,540
  million (long or no position). Priced that way the careful column is 39.6, under 50: READY.

