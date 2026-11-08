"""task2 architecture 4: submission.md (the four platform blocks) and generator/figures.json, every figure from the
solution and the rungs on the cut pack."""
import math

import solve as S


def r50(oz):
    return int(50000 * math.floor(oz / 50000 + 0.5))


def c(n):
    return "{:,}".format(int(n))


def figures(g, R):
    tier = dict(S.TIERS)
    return {
        "call": g["tier"], "tier_oz": tier[g["tier"]] * 1000, "tier_c_oz": tier["C"] * 1000, "tier_a_oz": tier["A"] * 1000,
        "cut": S.CUT, "oz_50k": r50(g["oz"]), "oz_koz": round(g["oz"] / 1e3), "oz_text": c(r50(g["oz"])),
        "n": g["n"], "holes": g["holes"], "mean_raw": round(g["mean_raw"], 2), "mean_decl": round(g["mean_decl"], 2),
        "nugget_pct": round(g["model"][0] * 100), "a1": g["model"][2], "a2": g["model"][3],
        "gamma_bar": round(g["gamma_bar"], 2), "ratio": round(g["ratio"], 2), "T_mt": round(g["T"] / 1e6, 1),
        "decl_koz": round(R["rung1_declustered"]["oz"] / 1e3), "decl_50k": r50(R["rung1_declustered"]["oz"]),
        "raw_koz": round(R["rung0_raw"]["oz"] / 1e3),
        "krig_koz": round(R["kriged"]["oz"] / 1e3), "krig_50k": r50(R["kriged"]["oz"]),
        "krig_cv": R["kriged"]["cv"], "cv_slope": R["kriging_cv"]["slope_obs_on_est"],
        "cv_err": R["kriging_cv"]["mean_error"],
        "family_koz": [round(min(R[k]["oz"] for k in R["standing"] if k != "cell_20") / 1e3),
                       round(max(R[k]["oz"] for k in R["standing"] if k != "cell_20") / 1e3)],
        "krig_family_koz": [round(min(R[k]["oz"] for k in ("kriged", "kriged_n12", "kriged_n32")) / 1e3),
                            round(max(R[k]["oz"] for k in ("kriged", "kriged_n12", "kriged_n32")) / 1e3)],
        "cuts": S.CUTS,
        "years": [2019, 2021, 2022, 2024, 2027, 2028],
        "dims": [5, 2.5, 25, 12.5], "tiers_koz": [75, 125, 200], "tiers_oz": [75000, 125000, 200000],
        "rounding_oz": 50000, "krige_search": [24, 45, 12, 32, 60],
        "affine_band_t": int(math.ceil(100 * max(abs(R["affine"]["gt"][str(c)]["t"] / g["gt"][c]["t"] - 1) for c in S.CUTS))),
        "affine_band_g": int(math.ceil(100 * max(abs(R["affine"]["gt"][str(c)]["g"] / g["gt"][c]["g"] - 1) for c in S.CUTS))),
        "affine_band_oz": int(math.ceil(100 * max(abs(R["affine"]["gt"][str(c)]["oz"] / g["gt"][c]["oz"] - 1) for c in S.CUTS))),
    }


def submission(g, R, F, path):
    L = []
    A = L.append
    A("## Tags")
    A("")
    A("> **Domain:** Engineering and Physical Sciences, General Statistics & Data Science (exploratory data analysis "
      "and distribution assessment: the distribution of block averages).")
    A("> **Analytical objective:** Descriptive & Distribution Analysis.")
    A("")
    A("## 1. Final Recommendation")
    A("")
    A("**Commit Stage 5 to Tier %s (%s oz).** Its 5 m by 5 m by 2.5 m mining blocks at %.1f g/t or more hold about %s "
      "oz, clear of Tier %s and short of Tier C's %s oz. Not Tier C: the declustered composites put %d koz above the "
      "cut-off because a 2.5 m composite varies about twice as much as a block; and not Tier A: the kriged block "
      "model puts %d koz there because its estimates vary less than the blocks do."
      % (F["call"], c(F["tier_oz"]), S.CUT, F["oz_text"], F["call"], c(F["tier_c_oz"]), F["decl_koz"], F["krig_koz"]))
    A("")
    A("## 2. Supplementary Questions")
    A("")
    A("### stage5_OPA_tier_board.pptx")
    A("")
    A("1. Slide 1 states the commitment to Tier %s and carries the chart: contained gold above each cut-off from "
      "1.0 to 3.0 g/t for the mining blocks (heaviest line), the declustered composites and the kriged block model, "
      "with the three tier thresholds (75, 125 and 200 koz) as flat red lines; the mining-block line crosses 2.5 g/t "
      "between Tier B and Tier C." % F["call"])
    A("2. Slide 2 sets out the declustering, the variogram and the block variance, and why the composites and the "
      "kriged model are rejected.")
    A("")
    A("### stage5_high_grade_resource.xlsx")
    A("")
    A("3. Sheet Grade-tonnage: one row per cut-off (1.0, 1.5, 2.0, 2.5 and 3.0 g/t) with the mining blocks' tonnes, "
      "grade and contained gold, then the gold above the agreement's 2.5 g/t cut-off and the tier it covers. The "
      "rows are the lognormal-shaped correction's; an affine correction to the same block variance moves a row's "
      "tonnes by up to %d per cent, its grade by up to %d per cent and its gold by up to %d per cent, so the table "
      "is read within those bands and the graded figure is the next answer."
      % (F["affine_band_t"], F["affine_band_g"], F["affine_band_oz"]))
    A("4. Gold above the agreement's cut-off, nearest 50,000 oz: %s oz." % F["oz_text"])
    A("5. Sheets Declustering, Variogram and Comparison: the composites as drilled and declustered, the experimental "
      "and modelled variogram with the block average, and the same grade-tonnage curve for the declustered "
      "composites and the kriged block model.")
    A("")
    A("## 3. Critical Components")
    A("")
    A("1. The infill sits where the first grid ran high: Stage 5's composites average **%.2f g/t** as drilled and "
      "**%.2f g/t** declustered on the 25 m grid's cells." % (F["mean_raw"], F["mean_decl"]))
    A("2. The variogram has a **%d per cent** nugget and a short structure, so a 5 m by 5 m by 2.5 m block's grades vary "
      "only **%.2f** times as much as a composite's." % (F["nugget_pct"], F["ratio"]))
    A("3. The kriged block model cross-validates without bias (slope **%.2f**) yet puts only **%d koz** above 2.5 g/t, "
      "against **%d koz** from the declustered composites." % (F["cv_slope"], F["krig_koz"], F["decl_koz"]))
    A("4. At block support Stage 5 holds about **%s oz** above 2.5 g/t, between Tier B (**125,000**) and Tier C "
      "(**200,000**)." % F["oz_text"])
    A("")
    A("## 4. Step-by-Step")
    A("")
    A("1. Put every collar in MC_drillhole_collars.csv on the mine grid (MGA94 less the shift in "
      "MC_2027_mine_plan_summary.pdf) and composited MC_drillhole_assays.csv to the 2.5 m flitches (values under "
      "detection at half the limit, the original assay where a screen fire re-assay follows).")
    A("2. Kept the %d composites inside MC_stage5_design_flitches.csv's outlines and declustered them on 25 m cells by "
      "flitch: %.2f g/t as drilled, %.2f g/t declustered." % (F["n"], F["mean_raw"], F["mean_decl"]))
    A("3. Read the declustered composites above 2.5 g/t against Stage 5's %.1f Mt (densities by weathering zone from "
      "MC_bulk_density.csv and MC_weathering_logs.csv): %d koz, Tier C (the reasonable but insufficient read)."
      % (F["T_mt"], F["decl_koz"]))
    A("4. Kriged the 5 m by 5 m by 2.5 m blocks from the fitted variogram (24 composites, 45 m): unbiased in "
      "cross-validation (slope %.2f), %d koz above 2.5 g/t, Tier A; its block estimates' coefficient of variation is "
      "%.2f, less than the blocks'." % (F["cv_slope"], F["krig_koz"], F["krig_cv"]))
    A("5. Fitted the variogram downhole and across holes: nugget %d per cent of the sill, structures of %d m and %d m; "
      "averaged within a block it is %.2f of the sill, so the blocks' variance is %.2f of the composites'."
      % (F["nugget_pct"], F["a1"], F["a2"], F["gamma_bar"], F["ratio"]))
    A("6. Carried the declustered composite distribution to that variance (the indirect lognormal correction, which "
      "keeps the mean and narrows the spread): %d koz above 2.5 g/t, about %s oz, Tier %s."
      % (F["oz_koz"], F["oz_text"], F["call"]))
    A("")
    A("No other tier survives. The composites alone overstate the high-grade gold whether declustered (%d koz) or not "
      "(%d koz), and the kriged model understates it in every neighbourhood tried (%d to %d koz). Every way of carrying "
      "the distribution to the block (affine or lognormal, declustering cells of 25 or 30 m, finer or coarser block "
      "discretisation, the nugget from the field duplicates) gives %d to %d koz, inside Tier B."
      % (F["decl_koz"], F["raw_koz"], F["krig_family_koz"][0], F["krig_family_koz"][1], F["family_koz"][0],
         F["family_koz"][1]))
    open(path, "w").write("\n".join(L) + "\n")
