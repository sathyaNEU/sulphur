# task1: Kraanvogel Luisterboeken, the January 2027 price rises

## Tags

**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer lifetime value).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

Let only Onbeperkt's January 2027 rise go ahead (EUR 4.7 per October 2026 subscription in 2027) and hold Flex, Standaard and Gezin at their 2026 prices: each of those rises takes the plan past the rival's comparable plan where most of its subscriptions are (Standaard and Flex in both regions, the rival having raised its Basis plan to EUR 10.29 in July 2026; Gezin in the Netherlands), and changes the 2027 contribution of its October subscriptions by EUR -1.4, EUR -13.2 and EUR -10.3 each. Not the careful reading that lets Gezin, Onbeperkt and Standaard through on each plan's own past response (Standaard EUR 1.2, Gezin EUR 1.0), nor one that sees where the rises pass the rival but counts a downgrade as a lost subscription and so holds Onbeperkt too.

## Supplementary Questions

### price_rises_2027.xlsx

1. Sheet Rises has one row per plan with its 2026 and 2027 price, the paying subscriptions at 31 October 2026, the change in their 2027 contribution if the rise goes ahead, in euros per subscription, and the decision; sheets Response and Past rises carry the figures below and Base the October subscriptions.
2. Change in the 2027 contribution of the subscriptions paying at 31 October 2026 if the plan's rise goes ahead, in euros per subscription (band in brackets): Flex -1.4 (-1.7 to -1.0); Standaard -13.2 (-15.1 to -11.6); Onbeperkt 4.7 (3.0 to 5.1); Gezin -10.3 (-10.6 to -8.8); the rise goes ahead on Onbeperkt and Flex, Standaard and Gezin hold.

### price_rises_2027.pptx

3. A short deck that opens on the decision, then a column chart of each plan's change, the past rises' response table, and the base.
4. Paying subscriptions at 31 October 2026, by plan (exact): Flex 494; Standaard 1,218; Onbeperkt 1,434; Gezin 1,021; 4,167 in all.
5. Extra cancellations per 100 subscriptions at the first bill at the 2027 price (band in brackets): Flex Netherlands 12.0 (10.8 to 12.6); Flex Flanders 12.0 (10.8 to 12.6); Standaard Netherlands 25.2 (22.2 to 28.5); Standaard Flanders 25.2 (22.2 to 28.5); Onbeperkt Netherlands 15.9 (14.3 to 16.7); Onbeperkt Flanders 4.0 (3.1 to 4.3); Gezin Netherlands 28.2 (24.9 to 29.6); Gezin Flanders 0.0 (-0.3 to 0.3).
6. Extra downgrades per 100 subscriptions at that bill (band in brackets; Flex has no plan below it): Standaard Netherlands 16.5 (14.6 to 17.5); Standaard Flanders 16.5 (14.6 to 17.5); Onbeperkt Netherlands 24.7 (22.2 to 26.0); Onbeperkt Flanders 1.1 (0.5 to 1.4); Gezin Netherlands 3.4 (3.0 to 3.7); Gezin Flanders 0.0 (-0.3 to 0.3).

## Critical Components

1. The change in the October subscriptions' 2027 contribution (forecasting): Onbeperkt **EUR 4.7**, Flex **EUR -1.4**, Standaard **EUR -13.2**, Gezin **EUR -10.3** per subscription.
2. The response at the first bill (causal reasoning): Standaard loses **25.2** and moves down **16.5** in every 100 in both regions, Gezin loses **28.2** in the Netherlands and **0.0** in Flanders, Onbeperkt **15.9** and **24.7** in the Netherlands against **4.0** and **1.1** in Flanders.
3. The paying base at 31 October 2026 (assembly): **4,167** subscriptions, Standaard **1,218**.

## Step-by-Step

1. From payments_2024-01_2026-10.csv and accounts_export_2026-11-03.csv, count each consumer account's collected monthly charge once: 4,167 paying subscriptions at 31 October 2026 (guideline 3.1).
2. Rebuild schedule B's counted hours per profile and title from listening_monthly_2024-01_2026-10.csv and licence_server_renewals_2024-01_2026-10.csv, each profile on the account its charge lists that month: Onbeperkt 34.38 and Standaard 9.92 counted hours per paying month.
3. Find the 2025 and 2026 January rises in the charges by plan and region and read each one's extra cancellations and downgrades at the first bill against the same plan in the other region (guideline 3.10): the 3 that took the price past the rival's comparable plan (rival_price_scan_2024-01_2026-10.csv, the December scan, promotions left out) lost 15.9, 12.0, 28.2 per 100, the others 8.6, -1.6, 2.2, 4.0, 4.1.
4. Carry each 2027 rise at its own region's crossing, on the rival's prices as last scanned (October 2026, guideline 3.8): Standaard passes the rival in both regions (it never did before, so its own history says little), Flex in both since the rival raised Basis 10 uur to EUR 10.29 in July 2026, Onbeperkt and Gezin in the Netherlands only. Every 2027 rise is the plan's own past rise in euros (Flex EUR 0.50, the others EUR 1.00) and lands no further past the rival than a past crossing did, so each past response carries at the size it was read; carried in proportion to the rise or on the log of the price ratio it moves no call.
5. Value what is lost: those who leave at a crossing rise are the heavy listeners, whose counted hours at EUR 0.40 eat most of what they pay, and those who move down are light listeners still paying on the cheaper plan, valued on the past downgraders' own months (Onbeperkt EUR 69.7 each in 2027).
6. Net it per October subscription against the rise's gain: Flex -1.4, Standaard -13.2, Onbeperkt 4.7, Gezin -10.3 euros; the rise goes ahead on Onbeperkt only (guideline 3.10).
7. The shortcuts land elsewhere: each plan's own past response, pooled or region by region, and one response for every rise let Gezin, Onbeperkt and Standaard through (Standaard 1.2, Gezin 1.0 on the careful route); seeing the crossings but counting a downgrade as an exit and leavers at the plan's average holds all four (Onbeperkt -4.2); the 2026 revenue share and a straight line in the gap to the rival hold all four too.

No other conclusion survives the records. The past rises answered where they passed the rival and barely elsewhere, in each plan that had both kinds, so neither one response for every rise nor each plan's own history carries to 2027, where the crossings fall differently; a downgrade keeps the subscription paying; the leavers and the downgraders listen differently from their plan's average; and schedule B prices every counted hour. Every rival control, window, downgrader valuation and dose form lets the same one rise through.
