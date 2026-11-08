## Tags

**Domain:** Quantitative Finance and Trading, Quantitative Finance (derivative pricing: the loss distribution of a senior note on a static portfolio of loans).  
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

**Buy Ostvale's Class A note: its chance of any loss of principal over 2027 to 2031 is 0.54 per cent, inside MP-RN-2's 1 per cent test, while Kestrel Lane's is 1.33 per cent and fails it.** The usual copula that links defaults only through the economy and the sector gives Kestrel Lane 0.14 per cent against Ostvale's 0.44 per cent and would buy Kestrel Lane, but it leaves out the years in which a sponsor house's companies fail together, which Kestrel Lane's concentration in five houses turns into the fatter tail.

## Supplementary Questions

### ic_note_senior_notes_2027.docx

1. The recommendation: buy Ostvale's Class A note; Kestrel Lane's note fails MP-RN-2's 1 per cent test and is not bought.
2. Each note's chance of any loss of principal over 2027 to 2031: Kestrel Lane 1.33 per cent; Ostvale 0.54 per cent.
3. The subordination each note would need for chances of 1, 0.5 and 0.25 per cent: Kestrel Lane 15.6, 17.0 and 18.3 per cent of par (it offers 15.0); Ostvale 14.1, 15.1 and 16.1 per cent of par (it offers 15.0).
4. The chart: one log-scale panel, the five-year credit loss as a share of par from 0 to 30 per cent across, the chance it is exceeded up the side, one line per portfolio with Kestrel Lane's above Ostvale's in the tail, a vertical line at both notes' 15.0 per cent subordination where the lines read 1.33 and 0.54 per cent, and a horizontal line at the 1 per cent test.

### senior_note_loss_by_year.csv

5. Ten rows, one per note and year end, columns note, issuer, subordination_pct, year_end and chance_of_loss_pct: Kestrel Lane 0.02, 0.12, 0.36, 0.76 and 1.33 per cent at the ends of 2027 to 2031; Ostvale 0.00, 0.02, 0.08, 0.24 and 0.54 per cent.

## Critical Components

1. Companies held by one sponsor house default in the same years: pairs in the same house, sector and year defaulted together **0.84 per cent** of the time against **0.25 per cent** for pairs in the same sector and year under other houses, while pairs in the same house but different years sit at the independence rate (**0.114** against **0.120 per cent**).
2. The house's year carries **0.503** of the variance of a borrower's credit standing that the economy (**0.109**) and the sector (**0.059**) leave, and it fits the record better than a fund-year or a lasting house or fund effect.
3. Kestrel Lane's **95** loans sit with **5** houses; Ostvale's **100** loans with **45**.
4. Each default loses **39.9 per cent**, the average shortfall on the 2008 to 2019 defaults whose workouts have all closed.
5. At 15.0 per cent subordination the five-year chance of loss is **1.33 per cent** for Kestrel Lane, which fails the test, and **0.54 per cent** for Ostvale, which passes; across sound estimates of the record (a probit or a cohort table for the default rates, a random effect or pair counts for the dependence) Kestrel Lane stays between 1.2 and 1.4 per cent and Ostvale between 0.5 and 0.7 per cent.

## Step-by-Step

1. Conformed lenderbase_loan_performance_2008-2026.csv (latest submission of each loan-quarter, the 2019 change of codes, LEIs only from 2012 with older loans joined by name through lei_reference_extract_2026-12-31.csv): 16,712 company-years at risk from 2008 to 2026 (each loan reported performing or on watch at the previous year end, or outstanding at the start of the record in 2008) with 578 defaults.
2. Traced every loan through dealtrail_buyout_transactions_1997-2026.csv to the completed buyout that began the ownership it sits in and to the buyer's sponsor house (the name its funds share): 80 houses, no loan unlinked.
3. Fitted one-year default chances by rating and full years since that buyout with a probit on the company-years.
4. The usual copula, one factor fitted to the yearly default rates (0.109) plus a sector factor (0.059), matches the record's yearly and sector-year default counts and gives Kestrel Lane 0.14 per cent against Ostvale's 0.44 per cent: the reasonable but insufficient analysis, which would buy Kestrel Lane.
5. Counted joint defaults among pairs at risk in the same year: 0.84 per cent for the same house, sector and year against 0.25 per cent across houses, and 0.114 per cent for the same house in different years, the independence rate, so the dependence is a house's shared bad year, not a weak house.
6. Estimated the house-year component as a random effect on house-year clusters given the sector-year: 0.503, with a log-likelihood of -1,775.5 against -1,805.1 for fund-years and -1,947.6 for a lasting fund effect.
7. Took the loss on default from the 364 closed workouts on 2008 to 2019 defaults, 39.9 per cent; the average over every closed workout (38.0 per cent) leaves out the 51 open workouts, which are the long ones that recover less.
8. Read both tapes into euros at the ECB rate of 31 December 2026, gave each borrower its house and years since buyout, and simulated 1,000,000 five-year paths under MP-RN-2: Kestrel Lane 1.33 per cent and Ostvale 0.54 per cent at 15.0 per cent subordination, with the year-end chances and subordination needs above.

No other conclusion survives. Every model without the house's year buys Kestrel Lane and is contradicted by the same-year house pairs; reading the dependence at the fund, or as a lasting fund effect, also buys Ostvale but fits the record worse and leaves Kestrel Lane at 0.68 or 0.33 per cent; the closed-workout loss on default keeps the call (0.98 against 0.33 per cent) but understates loss because the open workouts are the long ones; and MP-RN-2 4.2 rules out an assumed correlation or a fat-tailed copula.
