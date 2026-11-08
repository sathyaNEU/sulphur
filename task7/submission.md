## Tags

**Domain:** Banking, Credit & Financial Risk, expected credit loss provisioning (commercial property lending).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

Plan **€2 million** of 2027 credit loss on commercial property lending, not the €0.22 million (nil to the nearest €500,000) the CRE-LGD-3 model gives on the values the property register carries: those values are index roll-forwards of old inspections, and in the bank's own record a defaulting borrower's property was inspected at default below the value carried, by more the longer since its last inspection, while 26% of the year-end book was last inspected seven or more years ago.

## Supplementary Questions

### exco_cre_credit_loss_2027.pptx

1. The plan figure, on the opening slide: €2 million of expected credit loss in 2027 on the commercial property facilities performing at 31 December 2026, to the nearest €500,000, with the €0.22 million the model gives on the carried values named as the figure it replaces.
2. The split, on its own slide: investment lending €1.25 million and owner-occupied lending €0.75 million, to the nearest €250,000.
3. The five facilities expected to cost the bank most, on their own slide with each one's lending book, grade, exposure and expected loss: AB316705961, AB321158994, AB322222580, AB322344238, AB325355079. The deck lists them by expected loss, AB322222580 (investment) well ahead of the other four.

### cre_expected_loss_2027_by_loan.csv

4. One row for each of the 2,260 commercial property facilities performing at 31 December 2026, each with its facility number and its expected 2027 loss to the euro, largest first; the golden file also carries the customer, lending book, grade, chance of default, exposure, carried and expected security values and loss given default, a choice of layout rather than a requirement. The expected losses add up to the plan figure before rounding, and the first row is facility AB322222580.

## Critical Components

1. In the bank's record of defaults since 2012, the inspection at default against the value the register carried on the default date falls with the years since the inspection that value rests on: fitted, **93%** a year after it and **76%** at eight years for investment property, **89%** and **72%** for owner-occupied.
2. **26%** of the year-end book's exposure rests on an inspection seven or more years old, against fewer than one in ten of the properties in the record.
3. Priced at each facility's expected value at default (the carried value times the record's expected ratio for its years since inspection and lending book), the 2027 line is **€2 million**, against **€0.22 million** on the carried values.
4. At the same distance from the last inspection, owner-occupied security came in about **4** points lower at default than investment security, which puts **€0.75 million** on owner-occupied lending and **€1.25 million** on investment lending.

## Step-by-Step

1. plan_2027_credit_loss_request.pdf fixes the line: facilities performing at 31 December 2026, the master-scale chance of default at the year-end grade (ardcarn_credit_risk_policy_part4_2025.pdf, 4.1), the year-end balance, and the CRE-LGD-3 figure on the value the bank would expect its inspection to put on the security if the facility defaulted on 1 January 2027, prices held.
2. The 20261231 rows of dw_fact_loan_month_end_2022_2026.csv with default flag N give 2,260 facilities and €1.84 billion of exposure.
3. Each facility's security comes from the rows of dw_bridge_facility_security_2026-12.csv in force at the year end, a shared property split in proportion to exposure (policy 4.4); dw_dim_property_valuation_2004_2026.csv is cleaned of repeated rows and same-day corrections, FULL and IDX read as inspection and index roll-forward (policy 4.6), and the row in force on 31 December 2026 gives the carried value.
4. The default path: CRE-LGD-3, max(0, EAD - 0.78 x V) / EAD, on those carried values gives €0.22 million, nil to the nearest €500,000. The model's own back-test (cre_lgd_model_documentation_2025.pdf) passes in every year, but it feeds the model the inspection at default, not the value carried before it.
5. The carried value is the last inspection rolled forward by the Brackley Rowe series; walking each property's history back past the roll-forward rows to its last inspection shows 26% of the book's exposure last inspected seven or more years ago.
6. The record: for each property securing a default in default_register_2012_2026.csv (the first trigger per facility, legacy numbers through the facility register), the inspection the bank commissioned within three months of the default against the value carried on the default date. The ratio averages 87.1% (that average on every facility gives €1.2 million, so €1 million) and falls with the years since the inspection the carried value rests on, about 2.9% a year, more than 10 standard errors from nought in each lending book; inspections of performing properties in the 2012 to 2019 cycle fall by less, and on their own give €1.2 million, because nothing selected them.
7. The latest years are no better guide: over a third of the defaults since 2022 had their security inspected in the six months before they defaulted, so only about one in ten of them rested on an inspection seven or more years old, against 26% of the year-end book's exposure. The 2022 to 2026 average on every facility gives €1.3 million, so €1.5 million.
8. The log ratio fitted on years since inspection for each lending book, with the mean of the exponentiated residuals for the expected value, gives investment 93% at one year and 76% at eight, owner-occupied 89% and 72%; each facility takes its own years and book.
9. Expected loss per facility is PD x LGD x EAD on that expected value: €2 million in all to the nearest €500,000, investment €1.25 million and owner-occupied €0.75 million to the nearest €250,000, and the five facilities above.

No other figure survives the files. The carried values (€0.22 million) price the security at a value the bank's own defaults have never fetched; the cycle's inspections of performing properties (€1.2 million) miss what selects a borrower into default; one average shortfall (€1.2 million) or the latest years' average (€1.3 million) applies the record's fresher inspections to a staler book; linear, banded and median fits of the same ratio all file €2 million; pooling the two books lands the total but puts €1.5 million and €0.5 million on the split; and a default spread through 2027 (€2.3 million) is ruled out by the request's 1 January 2027.
