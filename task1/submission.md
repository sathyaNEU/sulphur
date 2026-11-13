# task1: Kraanvogel Luisterboeken, the January 2027 price rises

## Tags

**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer lifetime value).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

Let only Gezin's January 2027 rise go ahead (EUR 6.1 per October 2026 subscription in 2027) and hold Flex, Standaard and Onbeperkt at their 2026 prices: Standaard's rise passes the rival's comparable plan in both regions (EUR -14.8); Flex's loses more to the light listeners who leave at the December bill after the price e-mail than it brings (EUR -4.4); Onbeperkt's is lost to those leavers and to the second profile the accounts that stay add, at EUR 0.40 a counted hour (EUR -4.6). Not the careful reading that carries each plan's own past rise in its region at the first bill and lets Onbeperkt and Standaard through, nor one that sees where the rises pass the rival but stops at the first bill and lets Flex, Gezin and Onbeperkt through.

## Supplementary Questions

### price_rises_2027.xlsx

1. Sheet Rises has one row per plan with its 2026 and 2027 price, the paying subscriptions at 31 October 2026, the change in their 2027 contribution if the rise goes ahead, in euros per subscription, and the decision; sheets Response and Past rises carry the figures below and Base the October subscriptions.
2. Change in the 2027 contribution of the subscriptions paying at 31 October 2026 if the plan's rise goes ahead, in euros per subscription (band in brackets): Flex -4.4 (-4.8 to -2.6); Standaard -14.8 (-15.8 to -13.3); Onbeperkt -4.6 (-5.0 to -3.9); Gezin 6.1 (1.8 to 6.4); the rise goes ahead on Gezin; Flex, Standaard and Onbeperkt hold.

### price_rises_2027.pptx

3. A short deck that opens on the decision, then a column chart of each plan's change, the past rises' response table, and the base.
4. Paying subscriptions at 31 October 2026, by plan (exact): Flex 689; Standaard 1,226; Onbeperkt 1,453; Gezin 1,014; 4,382 in all.
5. Extra cancellations per 100 subscriptions at the first bill at the 2027 price (band in brackets): Flex Netherlands 4.5 (-0.3 to 4.8); Flex Flanders 4.5 (-0.3 to 4.8); Standaard Netherlands 21.2 (17.8 to 22.2); Standaard Flanders 21.2 (17.8 to 22.2); Onbeperkt Netherlands 2.9 (1.3 to 3.2); Onbeperkt Flanders 2.9 (1.3 to 3.2); Gezin Netherlands 0.0 (-0.3 to 3.5); Gezin Flanders 0.0 (-0.3 to 3.5).
6. Extra downgrades per 100 subscriptions at that bill (band in brackets; Flex has no plan below it): Standaard Netherlands 15.6 (13.8 to 18.2); Standaard Flanders 15.6 (13.8 to 18.2); Onbeperkt Netherlands 1.0 (0.5 to 3.0); Onbeperkt Flanders 1.0 (0.5 to 3.0); Gezin Netherlands 0.0 (-0.3 to 0.3); Gezin Flanders 0.0 (-0.3 to 0.3).
7. Of each plan's October 2026 subscriptions, still paying at 31 December 2027 if its rise goes ahead (band in brackets): Flex 141 (135 to 153); Standaard 283 (277 to 297); Onbeperkt 677 (663 to 698); Gezin 664 (628 to 677).

## Critical Components

1. The change in the October subscriptions' 2027 contribution (forecasting): Gezin **EUR 6.1**, Flex **EUR -4.4**, Standaard **EUR -14.8**, Onbeperkt **EUR -4.6** per subscription.
2. The response around the bill (causal reasoning): at the first bill Standaard loses **21.2** and moves down **15.6** in every 100 in both regions; at the December bill after the e-mail Flex loses **13.3** and Onbeperkt **7.2** in every 100; Onbeperkt's stayers listen **8.0** per cent more from the third month.
3. The paying base at 31 October 2026 (assembly): **4,382** subscriptions, Standaard **1,226**.
4. Still paying at 31 December 2027 if the rise goes ahead (forecasting): Gezin **664** of 1,014, Onbeperkt **677** of 1,453.

## Step-by-Step

1. From payments_2024-01_2026-10.csv and accounts_export_2026-11-03.csv, count each consumer account's collected monthly charge once: 4,382 paying subscriptions at 31 October 2026 (guideline 3.1).
2. Rebuild schedule B's counted hours per profile and title from listening_monthly_2024-01_2026-10.csv and licence_server_renewals_2024-01_2026-10.csv, each profile on the account its charge lists that month: Onbeperkt 35.41 and Standaard 9.93 counted hours per paying month.
3. Find the 2025 and 2026 January rises in the charges by plan and region and read each one's extra cancellations and downgrades at the first bill against the same plan in the other region (guideline 3.10): the 3 that took the price past the rival's comparable plan (rival_price_scan_2024-01_2026-10.csv, the December scan, promotions left out) lost 14.4, 10.9, 28.9 per 100, the others 5.3, -0.8, 1.7, 2.9, 4.5.
4. Carry each 2027 rise at its own region's crossing, on the rival's prices as last scanned (October 2026, guideline 3.8): Standaard passes the rival in both regions (it never did before, so its own history says little); Flex, Onbeperkt and Gezin pass it nowhere. Every 2027 rise is the plan's own past rise in euros (Flex EUR 0.50, the others EUR 1.00), so each past response carries at the size it was read.
5. Read what each past rise did outside its first bill, against the other region over the same months: at the December bill after the price e-mail the light listeners left (13.3 per 100 on Flex, 7.2 on Onbeperkt), and on Onbeperkt the accounts that stayed listened 8.0 per cent more from the third month, as single-profile accounts added the second profile the plan pays for; 2027's rises are e-mailed on 1 December.
6. Value what is lost: those who leave at a crossing rise are the heavy listeners, whose counted hours at EUR 0.40 eat most of what they pay; those who leave at the e-mail are light listeners worth the whole of 2027; those who move down keep paying on the cheaper plan, valued on the past downgraders' own months (Onbeperkt EUR 65.1 each in 2027).
7. Net it per October subscription against the rise's gain: Flex -4.4, Standaard -14.8, Onbeperkt -4.6, Gezin 6.1 euros; the rise goes ahead on Gezin only (guideline 3.10); 1,765 of the 4,382 October subscriptions are still paying at the end of 2027.
8. The shortcuts land elsewhere: each plan's own past rise in its region at the first bill (the careful route) lets Onbeperkt and Standaard through; reading the crossing but stopping at the first bill lets Flex, Gezin, Onbeperkt through; leaving out the December leavers lets Flex through and leaving out the stayers' listening lets Onbeperkt through; the 2026 revenue share and one response for every rise land elsewhere again.

No other conclusion survives the records. The past rises answered where they passed the rival and barely elsewhere, in each plan that had both kinds, so neither one response for every rise nor each plan's own history carries to 2027, where the crossings fall differently; a downgrade keeps the subscription paying; the leavers and the downgraders listen differently from their plan's average; and schedule B prices every counted hour; and a rise is answered at the December bill after its e-mail and in the hours of those who stay, not only at its first bill. Every rival control, window, downgrader valuation, dose form and perturbation lets the same one rise through.
