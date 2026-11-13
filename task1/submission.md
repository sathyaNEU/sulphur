# task1: Kraanvogel Luisterboeken, the spring 2027 campaign's lead plan

## Tags

**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer lifetime value).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

Lead the spring 2027 campaign with Gezin: its trial starts bring EUR 22.0 each over their first 24 months after the publishers' EUR 0.40 per counted hour and the agency's fee, EUR 8.7 ahead of Flex (EUR 13.3). Not Onbeperkt, which the live listening log values at EUR 45.5 only because it misses the listening of downloaded titles and credits profiles to the accounts they sit on today; counted in full, Onbeperkt brings EUR -3.6.

## Supplementary Questions

### spring_campaign_2027_plans.xlsx

1. Sheet Lead plan has one row per plan (Flex, Standaard, Onbeperkt, Gezin) with the spring 2024 trial starts, the share paying after the trial, paying months, net revenue at 2027 prices, counted hours, remuneration at EUR 0.40 an hour, the agency's fee and the contribution per trial start, and the lead plan under the table.
2. Contribution per trial start over its first 24 months, after the agency's fee, in euros (band in brackets): Flex 13.3 (13.2 to 13.5); Standaard 12.4 (12.3 to 13.4); Onbeperkt -3.6 (-3.6 to -2.5); Gezin 22.0 (21.2 to 22.2); the campaign leads with Gezin.

### spring_campaign_2027.pptx

3. A short deck that opens on the lead plan (Gezin, EUR 22.0 per trial start) with the contribution of every plan in a column chart, then the base and its listening, then the spring 2024 trial starts.
4. Paying subscriptions at 31 October 2026, by plan (exact): Flex 376; Standaard 858; Onbeperkt 1,004; Gezin 731; 2,969 in all.
5. Counted hours per paying subscription-month, November 2025 to October 2026, by plan (band in brackets): Flex 5.34 (5.29 to 5.39); Standaard 10.49 (10.39 to 10.60); Onbeperkt 31.37 (31.06 to 31.72); Gezin 27.95 (27.67 to 28.41).
6. The spring 2024 campaign's trial starts on each plan over their first 24 months, at 2027 prices: Flex 337 trial starts, 54.3 per cent paying after the trial, 3.78 paying months and EUR 36.67 net revenue per trial start; Standaard 436 trial starts, 65.1 per cent paying after the trial, 6.51 paying months and EUR 89.33 net revenue per trial start; Onbeperkt 440 trial starts, 60.7 per cent paying after the trial, 7.14 paying months and EUR 122.95 net revenue per trial start; Gezin 309 trial starts, 56.6 per cent paying after the trial, 8.46 paying months and EUR 175.66 net revenue per trial start.
7. The 2027 remuneration on the subscriptions paying at 31 October 2026: about EUR 202,600 (EUR 191,900 to EUR 207,300).

## Critical Components

1. Contribution per trial start over 24 months (forecasting): **Gezin EUR 22.0**, Standaard **EUR 12.4**, Flex **EUR 13.3**, Onbeperkt **EUR -3.6**.
2. Counted hours per paying subscription-month (measurement): Onbeperkt **31.37** and Gezin **27.95** once the licence renewals' positions are merged with the live roll-up and each profile sits on the account its charge lists (the live roll-up on today's profiles gives 18.80 and 26.29).
3. Paying subscriptions at 31 October 2026 (assembly): **2,969**, Onbeperkt **1,004** and Gezin **731**.
4. The 2027 remuneration on the October 2026 base (forecasting): **EUR 202,600** (EUR 191,900 to 207,300).

## Step-by-Step

1. From payments_2024-01_2026-10.csv and accounts_export_2026-11-03.csv, keep consumer accounts and count each account's collected monthly charge once (a returned debit that is re-presented counts once, staff and test accounts out): 2,969 paying subscriptions at 31 October 2026 (guideline 3.1), reconciling to the KPI report's January to September months.
2. From listening_monthly_2024-01_2026-10.csv (a re-sent row counted once) and licence_server_renewals_2024-01_2026-10.csv, rebuild schedule B's count per profile and title: the rise in the furthest position any report shows, in the month reported, licensed titles only (catalogue_2026-10.csv). The live roll-up reproduces the 2026 statements' streamed seconds exactly, but those are the 2026 basis; on live positions alone Onbeperkt counts 20.51 hours a paying month, against 31.37 with the renewals' positions of downloaded titles.
3. Put each profile's hours on the account whose charge that month lists it (profiles_on_subscription in the payments, guideline 3.3): profiles_export_2026-11-03.csv shows each profile where it is now, and partners who folded their own subscription into a Gezin account carry their earlier listening with them, so today's export gives Gezin 31.52 counted hours a paying month where its paying months held 27.95.
4. Take the spring 2024 campaign's trial starts on each plan (signup source VJ24, guideline 3.4) over the trial month and 23 months after, re-rated at the 2027 list prices with VAT by country and the stores' fees: Gezin's 309 trial starts bring EUR 175.66 each over 8.46 paying months.
5. Charge each trial start's account EUR 0.40 per counted hour in those months and the agency's fee (the quote): Gezin EUR 22.0, Standaard EUR 12.4, Flex EUR 13.3, Onbeperkt EUR -3.6; the campaign leads with Gezin (guideline 3.7).
6. The careful route on the live roll-up and today's profiles leads with Onbeperkt (Onbeperkt EUR 45.5); merging the renewals alone leads with Standaard (Gezin EUR 10.4, its accounts charged for histories that came from other accounts); dating the profiles alone leads with Onbeperkt; the 2026 basis carried leads with Onbeperkt.
7. Forecast the October base's 2027 counted hours with survival by plan and paid-tenure band (November 2024 to October 2026) and counted hours per paying month by plan and calendar month, at EUR 0.40 an hour: about EUR 202,600 (EUR 191,900 to 207,300 over the survival and listening forms); on the live roll-up alone it would be EUR 149,900.

No other conclusion survives the records. Schedule B counts the furthest position a profile has reached from every position the app reports, and the licence renewals are such reports, so a count on the live roll-up alone understates Onbeperkt; guideline 3.3 puts a profile's hours on the account it belonged to, which the charges' profile lists date month by month, so today's export overstates Gezin; and the 2026 statements' revenue share is the agreement schedule B replaces. Every reading of the duplicate rows and every form of the base's forecast leads with Gezin, and only the two corrections together do.
