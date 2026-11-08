"""task7: submission.md, the four answer blocks, drafted from figures.json so no figure is typed. Every figure a block
states is one an independent rebuild reproduces at the stated precision: the graded cells at the prompt's rounding, the
fitted ratios to the whole per cent, and the working counts in words."""


def write(F, path):
    c, a, k, r = F["call"], F["asks"], F["components"], F["rungs"]
    five = ", ".join(a["five_facilities"])
    first = a["five_by_loss"][0]
    md = []
    md += ["## Tags", "",
           "**Domain:** Banking, Credit & Financial Risk, expected credit loss provisioning (commercial property lending).",
           "**Analytical objective:** Forecasting & Predictive Modeling.", ""]
    md += ["## Final Recommendation", "",
           "Plan **%s** of 2027 credit loss on commercial property lending, not the %s (nil to the nearest €500,000) the "
           "CRE-LGD-3 model gives on the values the property register carries: those values are index roll-forwards of old "
           "inspections, and in the bank's own record a defaulting borrower's property was inspected at default below the "
           "value carried, by more the longer since its last inspection, while %s%% of the year-end book was last inspected "
           "seven or more years ago." % (c["plan_figure_display"], r["carried_display"], k["book_stale_share_pct"]), ""]
    md += ["## Supplementary Questions", "", "### exco_cre_credit_loss_2027.pptx", "",
           "1. The plan figure, on the opening slide: %s of expected credit loss in 2027 on the commercial property "
           "facilities performing at 31 December 2026, to the nearest €500,000, with the %s the model gives on the carried "
           "values named as the figure it replaces." % (c["plan_figure_display"], r["carried_display"]),
           "2. The split, on its own slide: investment lending %s and owner-occupied lending %s, to the nearest "
           "€250,000." % (a["investment_display"], a["owner_occupied_display"]),
           "3. The five facilities expected to cost the bank most, on their own slide with each one's lending book, "
           "grade, exposure and expected loss: %s. The deck lists them by expected loss, %s (%s) well ahead of the other "
           "four." % (five, first["facility"], first["book"].lower()),
           "", "### cre_expected_loss_2027_by_loan.csv", "",
           "4. One row for each of the %s commercial property facilities performing at 31 December 2026, each with its "
           "facility number and its expected 2027 loss to the euro, largest first; the golden file also carries the "
           "customer, lending book, grade, chance of default, exposure, carried and expected security values and loss "
           "given default, a choice of layout rather than a requirement. The expected losses add up to the plan figure "
           "before rounding, and the first row is facility %s." % (format(a["csv_rows"], ","), a["csv_top_facility"]), ""]
    md += ["## Critical Components", "",
           "1. In the bank's record of defaults since 2012, the inspection at default against the value the register "
           "carried on the default date falls with the years since the inspection that value rests on: fitted, **%s%%** "
           "a year after it and **%s%%** at eight years for investment property, **%s%%** and **%s%%** for owner-occupied."
           % (k["inv_fitted_1y_pct"], k["inv_fitted_8y_pct"], k["occ_fitted_1y_pct"], k["occ_fitted_8y_pct"]),
           "2. **%s%%** of the year-end book's exposure rests on an inspection seven or more years old, against fewer "
           "than one in ten of the properties in the record." % k["book_stale_share_pct"],
           "3. Priced at each facility's expected value at default (the carried value times the record's expected ratio "
           "for its years since inspection and lending book), the 2027 line is **%s**, against **%s** on the carried "
           "values." % (c["plan_figure_display"], r["carried_display"]),
           "4. At the same distance from the last inspection, owner-occupied security came in about **%s** points lower "
           "at default than investment security, which puts **%s** on owner-occupied lending and **%s** on investment "
           "lending." % (k["occ_level_gap_points"], a["owner_occupied_display"], a["investment_display"]), ""]
    md += ["## Step-by-Step", "",
           "1. plan_2027_credit_loss_request.pdf fixes the line: facilities performing at 31 December 2026, the master-scale "
           "chance of default at the year-end grade (ardcarn_credit_risk_policy_part4_2025.pdf, 4.1), the year-end "
           "balance, and the CRE-LGD-3 figure on the value the bank would expect its inspection to put on the security "
           "if the facility defaulted on 1 January 2027, prices held.",
           "2. The 20261231 rows of dw_fact_loan_month_end_2022_2026.csv with default flag N give %s facilities and "
           "%s of exposure." % (format(k["book_facilities"], ","), k["book_exposure_display"]),
           "3. Each facility's security comes from the rows of dw_bridge_facility_security_2026-12.csv in force at the "
           "year end, a shared property split in proportion to exposure (policy 4.4); dw_dim_property_valuation_2004_2026.csv "
           "is cleaned of repeated rows and same-day corrections, FULL and IDX read as inspection and index roll-forward "
           "(policy 4.6), and the row in force on 31 December 2026 gives the carried value.",
           "4. The default path: CRE-LGD-3, max(0, EAD - 0.78 x V) / EAD, on those carried values gives %s, nil to the "
           "nearest €500,000. The model's own back-test (cre_lgd_model_documentation_2025.pdf) passes in every year, but "
           "it feeds the model the inspection at default, not the value carried before it." % r["carried_display"],
           "5. The carried value is the last inspection rolled forward by the Brackley Rowe series; walking each property's "
           "history back past the roll-forward rows to its last inspection shows %s%% of the book's exposure last "
           "inspected seven or more years ago." % k["book_stale_share_pct"],
           "6. The record: for each property securing a default in default_register_2012_2026.csv (the first trigger per "
           "facility, legacy numbers through the facility register), the inspection the bank commissioned within three "
           "months of the default against the value carried on the default date. The ratio averages %s%% (that average "
           "on every facility gives %s, so %s) and falls with the years since the inspection the carried value rests on, "
           "about %s%% a year, more than %s standard errors from nought in each lending book; inspections of performing "
           "properties in the 2012 to 2019 cycle fall by less, and on their own give %s, because nothing selected them."
           % (k["record_mean_ratio_1dp"], r["record_mean_display"], r["record_mean_rounded_display"],
              k["fall_per_year_pct"], k["slope_t_book_floor"], r["cycle_drift_display"]),
           "7. The latest years are no better guide: over a third of the defaults since %s had their security inspected "
           "in the six months before they defaulted, so only about one in ten of them rested on an inspection seven or "
           "more years old, against %s%% of the year-end book's exposure. The %s to 2026 average on every facility gives "
           "%s, so %s."
           % (r["recent_from"], k["book_stale_share_pct"], r["recent_from"], r["recent_display"], r["recent_rounded_display"]),
           "8. The log ratio fitted on years since inspection for each lending book, with the mean of the exponentiated "
           "residuals for the expected value, gives investment %s%% at one year and %s%% at eight, owner-occupied %s%% and "
           "%s%%; each facility takes its own years and book." % (k["inv_fitted_1y_pct"], k["inv_fitted_8y_pct"],
                                                                 k["occ_fitted_1y_pct"], k["occ_fitted_8y_pct"]),
           "9. Expected loss per facility is PD x LGD x EAD on that expected value: %s in all to the nearest €500,000, "
           "investment %s and owner-occupied %s to the nearest €250,000, and the five facilities above."
           % (c["plan_figure_display"], a["investment_display"], a["owner_occupied_display"]),
           "",
           "No other figure survives the files. The carried values (%s) price the security at a value the bank's own "
           "defaults have never fetched; the cycle's inspections of performing properties (%s) miss what selects a "
           "borrower into default; one average shortfall (%s) or the latest years' average (%s) applies the record's "
           "fresher inspections to a staler book; linear, banded and median fits of the same ratio all file %s; pooling "
           "the two books lands the total but puts %s and %s on the split; and a default spread through 2027 (%s) is "
           "ruled out by the request's 1 January 2027."
           % (r["carried_display"], r["cycle_drift_display"], r["record_mean_display"], r["recent_display"],
              c["plan_figure_display"], r["pooled_investment_display"], r["pooled_owner_occupied_display"],
              r["midyear_display"]), ""]
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(md))
