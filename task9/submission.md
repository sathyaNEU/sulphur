## Tags

**Domain:** Quantitative Finance and Trading, Quantitative Finance (derivative pricing: the loss distribution of a senior note on a static portfolio of loans).  
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Buy neither note: Kestrel Lane's chance of any loss of principal over 2027 to 2031 is 3.9 per cent and Ostvale's 7.8 per cent, both above MP-RN-2's 1 per cent test, once each default recovers as the record shows defaults in its sponsor house's bad year recover.** This rejects Kestrel Lane's note, which passes at 0.7 per cent only if every default loses one average share, and Ostvale's, which passes at 0.1 per cent only if each default's recovery is read off the other defaults among the note's own loans, when Ostvale holds two of each house's companies and recovery follows the house's whole year.

## Supplementary Questions

### ic_note_senior_notes_2027.docx

1. The recommendation: buy neither note; both fail MP-RN-2's 1 per cent test and the allocation stays in the cash and government bond sleeve (MP-RN-2 2.2).
2. Each note's chance of any loss of principal over 2027 to 2031: Kestrel Lane 3.9 per cent; Ostvale 7.8 per cent.
3. Each portfolio's expected credit loss over 2027 to 2031, as a share of its par: Kestrel Lane 5.7 per cent; Ostvale 8.2 per cent.
4. The subordination each note would need for chances of 1 and 0.5 per cent, in whole per cent of par rounded up: Kestrel Lane 20 and 22 per cent (it offers 15.0); Ostvale 17 and 18 per cent (it offers 13.0).
5. The chart: one log-scale panel, the five-year credit loss as a share of par from 0 to 30 per cent across, the chance it is exceeded up the side, one line per portfolio with Kestrel Lane's above Ostvale's in the tail, a vertical line at each note's subordination (Kestrel Lane 15.0, Ostvale 13.0 per cent) where its line reads 3.9 and 7.8 per cent, and a horizontal line at the 1 per cent test.

### senior_note_loss_by_year.csv

6. Ten rows, one per note and year end, columns note, issuer, subordination_pct, year_end and chance_of_loss_pct: Kestrel Lane 0.2, 0.6, 1.4, 2.5 and 3.9 per cent at the ends of 2027 to 2031; Ostvale 0.0, 0.2, 1.0, 3.5 and 7.8 per cent.

## Critical Components

1. Companies held by one sponsor house default in the same years: pairs in the same house, sector and year defaulted together **0.84 per cent** of the time against **0.25 per cent** under different houses; the house's year carries **0.503** of the variance the economy (**0.109**) and the sector (**0.059**) leave.
2. On the 2008 to 2019 defaults, whose workouts have all closed, a default with no other default in its sponsor house in the calendar year of its default recovered **74.9 per cent** and one with three or more others **44.1 per cent**; the economy's year does not lower recovery (**-0.061** per unit of the year's shock).
3. Those counts run over each house's whole book (a median of **13** of the house's companies at risk in a defaulting house-year), while Ostvale's tape holds **2** companies of each house and Kestrel Lane's **14**; so recovery is tied to the house-year's own shock, inferred from that house-year's defaults against the rates its companies' ratings, ages and sector-years expected: **0.953** plus **0.298** per unit of the shock on the closed cohorts (and **0.000** per unit of the year's).
4. Kestrel Lane's **98** loans sit with **7** houses and Ostvale's **100** with **66**; the five-year chance of loss is **3.9 per cent** for Kestrel Lane's note at 15.0 per cent subordination and **7.8 per cent** for Ostvale's at 13.0, both over the test (the sound estimators span 1.5 to 4.0 and 2.3 to 7.8 per cent).

## Step-by-Step

1. Conformed lenderbase_loan_performance_2008-2026.csv (latest submission of each loan-quarter, the 2019 change of codes, older loans joined by name through lei_reference_extract_2026-12-31.csv): 16,712 company-years at risk from 2008 to 2026 with 578 defaults; traced every loan through dealtrail_buyout_transactions_1997-2026.csv to the buyout that began its ownership and the buyer's sponsor house (80 houses).
2. Fitted one-year default chances by rating and full years since the buyout with a probit on the company-years.
3. The usual copula, one factor fitted to the yearly default rates (0.109) plus a sector factor (0.059), gives Kestrel Lane 0.1 per cent against Ostvale's 5.9 per cent and would buy Kestrel Lane.
4. Pairs in the same house and year default together far more often than across houses, so the house's year enters the copula (0.503 of the residual variance, log-likelihood -1,775.5 against -1,805.1 for fund-years); with one average loss of 42.7 per cent for every default (the 2008 to 2019 workouts, all closed) Kestrel Lane is at 0.7 per cent and Ostvale at 6.2 per cent: the reasonable but insufficient analysis, which buys Kestrel Lane.
5. Read the recoveries in lenderbase_workout_recoveries_2008-2026.csv against the economy's year: -0.061 per unit of the year's shock, no lower in bad years, so a downturn link leaves Kestrel Lane at 0.2 per cent and passing.
6. Read them against the house's year instead: on the closed 2008 to 2019 cohorts a lone default recovered 74.9 per cent and one with three or more others in its house that year 44.1 per cent; the clustered defaults also take longer, so 78 workouts are still open and the later cohorts' closed cases are the quick, good ones, which is why the link is estimated on the 2008 to 2019 cohorts.
7. Carrying that table to the notes by counting each default's co-defaults among the note's own loans puts Kestrel Lane at 1.8 per cent and Ostvale at 0.1 per cent and buys Ostvale (a straight line in the count gives 2.0 and 0.8): the second reasonable but insufficient analysis. A default in the record shares its house-year with a median of 13 of the house's companies, and Ostvale holds 2 of each house's, so its defaults read as lone ones whatever year their house is having; the same default cannot recover more because the note holds fewer of its house's loans.
8. Inferred each house-year's shock as its posterior mean given the house-year's defaults against its companies' sector-year rates, and each year's from its default rate, and regressed recovery on both: 0.953 plus 0.298 per unit of the house-year's shock and 0.000 per unit of the year's.
9. Read both tapes into euros at the ECB rate of 31 December 2026 and simulated 1,000,000 five-year paths under MP-RN-2, each default recovering on the year and house shocks that drew it: Kestrel Lane 3.9 per cent at 15.0 per cent subordination and Ostvale 7.8 per cent at 13.0, expected credit losses of 5.7 and 8.2 per cent of par, and the year-end chances and the subordination needed above.

No other conclusion survives. Without the house's year in the dependence, with it but one average loss, or with a loss tied to the economy alone, the defaults that cluster in a house's bad year are priced at an ordinary recovery and Kestrel Lane is bought (at 0.1, 0.7 or 0.2 per cent); reading recovery off the co-defaults among each note's own loans prices Ostvale's defaults as lone ones and buys Ostvale (0.1 or 0.8 per cent). Every estimate that ties recovery to the house's year keeps both notes over the test: the same co-default counts taken over each house's whole book in the record (2.2 and 5.7 per cent, 4.1 and 5.0 with a straight line), the house-year's shock read against the year's rates (3.5 and 6.7), the house's shock alone (4.0 and 7.8), a cohort table or pair counts for the default model and the dependence with each house-year's shock read three ways (1.5 to 4.0 and 2.3 to 7.8 per cent), and a link fitted on every closed workout, which drops the open ones MP-RN-2 4.1 keeps (3.1 and 4.8).
