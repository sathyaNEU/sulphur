## Tags

> **Domain:** Engineering and Physical Sciences, General Statistics & Data Science (exploratory data analysis and distribution assessment: the distribution of block averages).
> **Analytical objective:** Descriptive & Distribution Analysis.

## 1. Final Recommendation

**Commit Stage 5 to Tier B (125,000 oz).** Its 5 m by 5 m by 2.5 m mining blocks at 2.5 g/t or more hold about 150,000 oz, clear of Tier B and short of Tier C's 200,000 oz. Not Tier C: the declustered composites put 231 koz above the cut-off because a 2.5 m composite varies about twice as much as a block; and not Tier A: the kriged block model puts 96 koz there because its estimates vary less than the blocks do.

## 2. Supplementary Questions

### stage5_OPA_tier_board.pptx

1. Slide 1 states the commitment to Tier B and carries the chart: contained gold above each cut-off from 1.0 to 3.0 g/t for the mining blocks (heaviest line), the declustered composites and the kriged block model, with the three tier thresholds (75, 125 and 200 koz) as flat red lines; the mining-block line crosses 2.5 g/t between Tier B and Tier C.
2. Slide 2 sets out the declustering, the variogram and the block variance, and why the composites and the kriged model are rejected.

### stage5_high_grade_resource.xlsx

3. Sheet Grade-tonnage: one row per cut-off (1.0, 1.5, 2.0, 2.5 and 3.0 g/t) with the mining blocks' tonnes, grade and contained gold, then the gold above the agreement's 2.5 g/t cut-off and the tier it covers. The rows are the lognormal-shaped correction's; an affine correction to the same block variance moves a row's tonnes by up to 14 per cent, its grade by up to 6 per cent and its gold by up to 11 per cent, so the table is read within those bands and the graded figure is the next answer.
4. Gold above the agreement's cut-off, nearest 50,000 oz: 150,000 oz.
5. Sheets Declustering, Variogram and Comparison: the composites as drilled and declustered, the experimental and modelled variogram with the block average, and the same grade-tonnage curve for the declustered composites and the kriged block model.

## 3. Critical Components

1. The infill sits where the first grid ran high: Stage 5's composites average **1.38 g/t** as drilled and **1.18 g/t** declustered on the 25 m grid's cells.
2. The variogram has a **34 per cent** nugget and a short structure, so a 5 m by 5 m by 2.5 m block's grades vary only **0.54** times as much as a composite's.
3. The kriged block model cross-validates without bias (slope **1.00**) yet puts only **96 koz** above 2.5 g/t, against **231 koz** from the declustered composites.
4. At block support Stage 5 holds about **150,000 oz** above 2.5 g/t, between Tier B (**125,000**) and Tier C (**200,000**).

## 4. Step-by-Step

1. Put every collar in MC_drillhole_collars.csv on the mine grid (MGA94 less the shift in MC_2027_mine_plan_summary.pdf) and composited MC_drillhole_assays.csv to the 2.5 m flitches (values under detection at half the limit, the original assay where a screen fire re-assay follows).
2. Kept the 10837 composites inside MC_stage5_design_flitches.csv's outlines and declustered them on 25 m cells by flitch: 1.38 g/t as drilled, 1.18 g/t declustered.
3. Read the declustered composites above 2.5 g/t against Stage 5's 20.6 Mt (densities by weathering zone from MC_bulk_density.csv and MC_weathering_logs.csv): 231 koz, Tier C (the reasonable but insufficient read).
4. Kriged the 5 m by 5 m by 2.5 m blocks from the fitted variogram (24 composites, 45 m): unbiased in cross-validation (slope 1.00), 96 koz above 2.5 g/t, Tier A; its block estimates' coefficient of variation is 0.55, less than the blocks'.
5. Fitted the variogram downhole and across holes: nugget 34 per cent of the sill, structures of 12 m and 50 m; averaged within a block it is 0.46 of the sill, so the blocks' variance is 0.54 of the composites'.
6. Carried the declustered composite distribution to that variance (the indirect lognormal correction, which keeps the mean and narrows the spread): 147 koz above 2.5 g/t, about 150,000 oz, Tier B.

No other tier survives. The composites alone overstate the high-grade gold whether declustered (231 koz) or not (350 koz), and the kriged model understates it in every neighbourhood tried (95 to 108 koz). Every way of carrying the distribution to the block (affine or lognormal, declustering cells of 25 or 30 m, finer or coarser block discretisation, the nugget from the field duplicates) gives 136 to 162 koz, inside Tier B.
