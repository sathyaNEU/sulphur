# task1: Kraanvogel Luisterboeken, the January 2027 price rises

## Tags

**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer lifetime value).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

Let the January 2027 rises go ahead on Flex, Onbeperkt, Gezin and hold Standaard at its 2026 price: Standaard's rise passes the rival's comparable plan in both regions and changes the 2027 contribution of its October subscriptions by EUR -12.4 each, while the others gain (Flex EUR 3.3, Onbeperkt EUR 4.7, Gezin EUR 5.3). Not the careful reading that lets all four through on each plan's own past response (Standaard EUR 1.2), nor one that counts a downgrade as a lost subscription and so holds Onbeperkt.

## Supplementary Questions

### price_rises_2027.xlsx

1. Sheet Rises has one row per plan with its 2026 and 2027 price, the paying subscriptions at 31 October 2026, the change in their 2027 contribution if the rise goes ahead, in euros per subscription, and the decision; sheets Response and Past rises carry the figures below and Base the October subscriptions.
2. Change in the 2027 contribution of the subscriptions paying at 31 October 2026 if the plan's rise goes ahead, in euros per subscription (band in brackets): Flex 3.3 (3.0 to 4.6); Standaard -12.4 (-14.3 to -12.1); Onbeperkt 4.7 (3.0 to 5.1); Gezin 5.3 (5.0 to 7.0); the rises go ahead on Flex, Onbeperkt, Gezin and Standaard holds.

### price_rises_2027.pptx

3. A short deck that opens on the decision, then a column chart of each plan's change, the past rises' response table, and the base.
4. Paying subscriptions at 31 October 2026, by plan (exact): Flex 494; Standaard 1,218; Onbeperkt 1,434; Gezin 1,021; 4,167 in all.
5. Extra cancellations per 100 subscriptions at the first bill at the 2027 price (band in brackets): Flex Netherlands 4.1 (-0.3 to 4.4); Flex Flanders 4.1 (-0.3 to 4.4); Standaard Netherlands 25.2 (23.9 to 28.5); Standaard Flanders 25.2 (23.9 to 28.5); Onbeperkt Netherlands 15.9 (15.1 to 16.7); Onbeperkt Flanders 4.0 (3.1 to 4.3); Gezin Netherlands 28.2 (24.9 to 29.6); Gezin Flanders 0.0 (-0.3 to 0.3).
6. Extra downgrades per 100 subscriptions at that bill (band in brackets; Flex has no plan below it): Standaard Netherlands 16.5 (15.7 to 17.5); Standaard Flanders 16.5 (15.7 to 17.5); Onbeperkt Netherlands 24.7 (23.5 to 26.0); Onbeperkt Flanders 1.1 (0.5 to 1.4); Gezin Netherlands 3.4 (3.1 to 3.7); Gezin Flanders 0.0 (-0.3 to 0.3).

## Critical Components

1. The change in the October subscriptions' 2027 contribution (forecasting): Standaard **EUR -12.4**, Flex **EUR 3.3**, Onbeperkt **EUR 4.7**, Gezin **EUR 5.3** per subscription.
2. The response at the first bill (causal reasoning): Standaard loses **25.2** and moves down **16.5** in every 100 in both regions, Onbeperkt **15.9** and **24.7** in the Netherlands against **4.0** and **1.1** in Flanders.
3. The paying base at 31 October 2026 (assembly): **4,167** subscriptions, Standaard **1,218**.

## Step-by-Step

1. From payments_2024-01_2026-10.csv and accounts_export_2026-11-03.csv, count each consumer account's collected monthly charge once: 4,167 paying subscriptions at 31 October 2026 (guideline 3.1).
2. Rebuild schedule B's counted hours per profile and title from listening_monthly_2024-01_2026-10.csv and licence_server_renewals_2024-01_2026-10.csv, each profile on the account its charge lists that month: Onbeperkt 34.38 and Standaard 9.92 counted hours per paying month.
3. Find the 2025 and 2026 January rises in the charges by plan and region and read each one's extra cancellations and downgrades at the first bill against the same plan in the other region (guideline 3.10): the 3 that took the price past the rival's comparable plan (rival_price_scan_2024-01_2026-10.csv, the December scan, promotions left out) lost 15.9, 12.0, 28.2 per 100, the others 8.6, -1.6, 2.2, 4.0, 4.1.
4. Carry each 2027 rise at its own region's crossing: Standaard passes the rival in both regions (it never did before, so its own history says little), Onbeperkt and Gezin in the Netherlands only, Flex nowhere.
5. Value what is lost: those who leave at a crossing rise are the heavy listeners, whose counted hours at EUR 0.40 eat most of what they pay, and those who move down are light listeners still paying on the cheaper plan, valued on the past downgraders' own months (Onbeperkt EUR 69.7 each in 2027).
6. Net it per October subscription against the rise's gain: Flex 3.3, Standaard -12.4, Onbeperkt 4.7, Gezin 5.3 euros; the rises go ahead on Flex, Onbeperkt, Gezin (guideline 3.10).
7. The shortcuts land elsewhere: each plan's own past response lets all four through (Standaard 1.2); one response scaled by the rise lets all four through; counting a downgrade as an exit holds Onbeperkt; the 2026 revenue share holds Onbeperkt and Gezin; reading the response off the gap to the rival in a straight line holds all four.

No other conclusion survives the records. The past rises answered where they passed the rival and barely elsewhere, in each plan that had both kinds, so neither one response for every rise nor each plan's own history carries to 2027, where the crossings fall differently; a downgrade keeps the subscription paying; the leavers and the downgraders listen differently from their plan's average; and schedule B prices every counted hour. Every rival control, window and downgrader valuation lets the same three rises through.
