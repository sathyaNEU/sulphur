## Tags

**Domain:** Quantitative Finance and Trading, Quantitative Finance (derivative pricing: the loss distribution of a senior note on a static portfolio of loans).  
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Buy neither note: Kestrel Lane's chance of any loss of principal over 2027 to 2031 is 2.6 per cent and Ostvale's 1.8 per cent, both above MP-RN-2's 1 per cent test, once each default recovers as the record shows defaults in its sponsor house's year recover.** With one average loss for every default Kestrel Lane's note passes at 0.6 per cent and would be bought, and tying recovery to the economy's year leaves it at 0.2 per cent; but its loans sit with seven houses, the defaults that cluster in a house's bad year are the ones that recover least, and that is the tail a senior note is exposed to.

## Supplementary Questions

### ic_note_senior_notes_2027.docx

1. The recommendation: buy neither note; both fail MP-RN-2's 1 per cent test and the allocation stays in the cash and government bond sleeve (MP-RN-2 2.2).
2. Each note's chance of any loss of principal over 2027 to 2031: Kestrel Lane 2.6 per cent; Ostvale 1.8 per cent.
3. The subordination each note would need for chances of 1 and 0.5 per cent, in whole per cent of par rounded up: Kestrel Lane 18 and 20 per cent (it offers 15.0); Ostvale 16 and 17 per cent (it offers 15.0).
4. The chart: one log-scale panel, the five-year credit loss as a share of par from 0 to 30 per cent across, the chance it is exceeded up the side, one line per portfolio with Kestrel Lane's above Ostvale's in the tail, a vertical line at both notes' 15.0 per cent subordination where the lines read 2.6 and 1.8 per cent, and a horizontal line at the 1 per cent test.

### senior_note_loss_by_year.csv

5. Ten rows, one per note and year end, columns note, issuer, subordination_pct, year_end and chance_of_loss_pct: Kestrel Lane 0.1, 0.4, 0.9, 1.6 and 2.6 per cent at the ends of 2027 to 2031; Ostvale 0.0, 0.0, 0.2, 0.7 and 1.8 per cent.

## Critical Components

1. Companies held by one sponsor house default in the same years: pairs in the same house, sector and year defaulted together **0.84 per cent** of the time against **0.25 per cent** under different houses; the house's year carries **0.503** of the variance the economy (**0.109**) and the sector (**0.059**) leave.
2. On the 2008 to 2019 defaults, whose workouts have all closed, a default with no other default in its house that year recovered **71.1 per cent** and one with three or more others **48.7 per cent**; the economy's year alone barely moves recovery (**-0.048** per unit of the year's shock).
3. Recovery on the closed cohorts runs **0.860** plus **0.220** per unit of the house-year's shock (and **-0.003** per unit of the year's), each shock inferred from that house-year's or year's own defaults against the rates its loans' ratings, ages and sector-years expected.
4. Kestrel Lane's **98** loans sit with **7** houses and Ostvale's **100** with **66**; at 15.0 per cent subordination the five-year chance of loss is **2.6 per cent** for Kestrel Lane and **1.8 per cent** for Ostvale, both over the test.

## Step-by-Step

1. Conformed lenderbase_loan_performance_2008-2026.csv (latest submission of each loan-quarter, the 2019 change of codes, older loans joined by name through lei_reference_extract_2026-12-31.csv): 16,712 company-years at risk from 2008 to 2026 with 578 defaults; traced every loan through dealtrail_buyout_transactions_1997-2026.csv to the buyout that began its ownership and the buyer's sponsor house (80 houses).
2. Fitted one-year default chances by rating and full years since the buyout with a probit on the company-years.
3. The usual copula, one factor fitted to the yearly default rates (0.109) plus a sector factor (0.059), gives Kestrel Lane 0.1 per cent against Ostvale's 1.7 per cent and would buy Kestrel Lane.
4. Pairs in the same house and year default together far more often than across houses, so the house's year enters the copula (0.503 of the residual variance, log-likelihood -1,775.5 against -1,805.1 for fund-years); with one average loss of 41.9 per cent for every default (the 2008 to 2019 workouts, all closed) Kestrel Lane is at 0.6 per cent and Ostvale at 1.9 per cent: the reasonable but insufficient analysis, which buys Kestrel Lane.
5. Read the recoveries in lenderbase_workout_recoveries_2008-2026.csv against the economy's year: -0.048 per unit of the year's shock, so a downturn link leaves Kestrel Lane at 0.2 per cent and passing.
6. Read them against the house's year instead: on the closed 2008 to 2019 cohorts a lone default recovered 71.1 per cent and one with three or more others in its house that year 48.7 per cent; the clustered defaults also take longer, so 71 workouts are still open and the later cohorts' closed cases are the quick, good ones, which is why the link is estimated on the 2008 to 2019 cohorts.
7. Inferred each house-year's shock as its posterior mean given the house-year's defaults against its companies' sector-year rates, and each year's from its default rate, and regressed recovery on both: 0.860 plus 0.220 per unit of the house-year's shock and -0.003 per unit of the year's.
8. Read both tapes into euros at the ECB rate of 31 December 2026 and simulated 1,000,000 five-year paths under MP-RN-2, each default recovering on the year and house shocks that drew it: Kestrel Lane 2.6 per cent and Ostvale 1.8 per cent at 15.0 per cent subordination, with the year-end chances and the subordination needed above.

No other conclusion survives. Without the house's year in the dependence, with it but one average loss, or with a loss tied to the economy alone, the defaults that cluster in a house's bad year are priced at an ordinary recovery and Kestrel Lane is bought (at 0.1, 0.6 or 0.2 per cent); every estimate that ties recovery to the house's year keeps both notes over the test: the house-year's shock read against the year's rates (2.2 and 1.6 per cent), the house's shock alone (2.7 and 2.0 per cent), and a cohort table or pair counts for the default model (1.8 to 2.6 and 1.4 to 1.9 per cent); a link fitted on every closed workout drops the open ones MP-RN-2 4.1 keeps, the clustered defaults' long workouts, and puts Ostvale at 0.9 per cent. Ostvale's weaker credits fail the test on every route that keeps them.
