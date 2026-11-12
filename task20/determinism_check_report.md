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
