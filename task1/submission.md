# task1: Kraanvogel Luisterboeken, the January 2027 price rises

## Tags

**Domain:** Product Analytics, Product Analytics (Cohort and LTV modeling: retention curves, customer lifetime value).
**Analytical objective:** Forecasting & Predictive Modeling.

## Final Recommendation

Let Standaard's and Gezin's January 2027 rises go ahead (EUR 2.2 and EUR 5.4 per October 2026 subscription in 2027) and hold Flex (EUR -3.3, its rise passing the rival's Basis 10 uur) and Onbeperkt (EUR -4.8): many of those Standaard loses at the December and first bills take a plan up again within the year at the new price, and Onbeperkt's subscriptions that stay listen about 38 counted hours more each in 2027, every one of them paid at EUR 0.40. Not the careful reading that treats a stop as final and the stayers' listening as unchanged and lets Gezin and Onbeperkt through, nor one that adds the returns alone (Gezin, Onbeperkt and Standaard) or the stayers' listening alone (Gezin only).

## Supplementary Questions

### price_rises_2027.xlsx

1. Sheet Rises has one row per plan with its 2026 and 2027 price, the paying subscriptions at 31 October 2026, the change in their 2027 contribution with the rise, how many of them pay on any plan at 31 December 2027, the 2027 publisher remuneration on them and the decision; sheets First bill, Past rises, Stopped and back, Stayers' listening, Base and Other readings carry the figures below.
2. Change in the 2027 contribution of the subscriptions paying at 31 October 2026 if the plan's rise goes ahead, in euros per subscription (band in brackets): Flex -3.3 (-3.8 to -2.8); Standaard 2.2 (0.9 to 3.0); Onbeperkt -4.8 (-5.3 to -4.2); Gezin 5.4 (3.1 to 6.3); the rise goes ahead on Gezin and Standaard and holds on Flex and Onbeperkt.

### price_rises_2027.pptx

3. A short deck that opens on the decision, then a column chart of each plan's change, what a rise loses and what comes back, the stayers' listening, and the base with its 2027 publisher cost.
4. Paying subscriptions at 31 October 2026, by plan (exact): Flex 1,371; Standaard 2,146; Onbeperkt 2,136; Gezin 1,224; 6,877 in all.
5. Of each plan's October 2026 subscriptions, paying on any plan at 31 December 2027 if its rise goes ahead (band in brackets): Flex 591 (574 to 605); Standaard 1,039 (1,008 to 1,064); Onbeperkt 1,270 (1,237 to 1,299); Gezin 898 (871 to 921).
6. The 2027 publisher remuneration on them if the rise goes ahead, in euros per October subscription (band in brackets): Flex 12.1 (11.7 to 12.5); Standaard 27.8 (27.0 to 28.5); Onbeperkt 119.7 (113.4 to 122.3); Gezin 113.6 (110.6 to 116.2).
7. Extra cancellations per 100 subscriptions reaching the first bill at the 2027 price (band in brackets): Flex Netherlands 10.5 (9.4 to 11.7); Flex Flanders 10.5 (9.5 to 11.7); Standaard Netherlands 3.8 (2.7 to 5.4); Standaard Flanders 3.7 (2.6 to 5.4); Onbeperkt Netherlands 0.8 (-0.3 to 2.0); Onbeperkt Flanders 0.9 (-0.3 to 2.0); Gezin Netherlands 0.5 (-1.8 to 2.8); Gezin Flanders 0.6 (-1.8 to 2.8).
8. Extra downgrades per 100 at that bill (band in brackets; Flex has no plan below it): Standaard Netherlands 3.4 (3.1 to 4.0); Standaard Flanders 3.4 (3.1 to 4.0); Onbeperkt Netherlands 0.8 (0.5 to 3.3); Onbeperkt Flanders 0.9 (0.5 to 3.3); Gezin Netherlands 0.2 (-1.5 to 0.5); Gezin Flanders 0.2 (-1.5 to 0.5).

## Critical Components

1. The change in the October subscriptions' 2027 contribution with the rise (forecasting; bands as in question 2): Standaard **EUR 2.2**, Gezin **EUR 5.4**, Flex **EUR -3.3**, Onbeperkt **EUR -4.8** per subscription.
2. The stops that come back (modeling): of every 100 October subscriptions that stop by December 2027 with the rise, those paying again then (band in brackets): Flex **27** (25 to 29), Standaard **26** (24 to 28), Onbeperkt **23** (20 to 25), Gezin **23** (21 to 25); light listeners come back soonest (of 100 that stop in December, about 58 with under 3 counted hours a month pay again within a year, about 28 with 20 and more).
3. The stayers' listening (causal reasoning): the subscriptions that stay after a rise listen more, Onbeperkt's about 20 per cent more in the first month after the bill, fading over about 5 months; extra counted hours over 2027 for each subscription staying on the plan all year (band in brackets): Onbeperkt **37.9** (33.0 to 42.2), Gezin **7.4** (6.4 to 9.0), Standaard **6.2** (5.0 to 7.3), Flex **1.3** (-0.0 to 2.4).

## Step-by-Step

1. From payments_2024-01_2026-10.csv and accounts_export_2026-11-03.csv, count each consumer account's collected monthly charge once: 6,877 paying subscriptions at 31 October 2026 (guideline 3.1).
2. Rebuild schedule B's counted hours per profile and title from listening_monthly_2024-01_2026-10.csv and licence_server_renewals_2024-01_2026-10.csv, each profile on the account its charge lists that month: Onbeperkt 32.34 and Gezin 28.94 counted hours per paying month, Flex 4.63.
3. Read the eight past rises (price_list_2027.pdf dates them and their 1 December e-mails) against the same plan in the other region over the same months (guideline 3.10): the 4 whose new price passed the rival's comparable plan (rival_price_scan_2024-01_2026-10.csv, the December scan, promotions out) lost 10.8, 11.7, 9.9, 29.7 per 100 at the first bill, the others 7.8, -1.5, 4.0, 0.3; at the December bill after the e-mail Flex lost 9.4, Standaard 6.4, Onbeperkt 6.8 and Gezin 0.4 per 100 (each plan's two rises).
4. Carry the first bill to 2027 by listening band in proportion to each rise, the downgrades among subscriptions whose profiles fit the plan below, on the rival's prices as last scanned (October 2026, guideline 3.8; in July 2026 the rival raised its Basis 10 uur to EUR 10.29 and brought its Flemish Onbeperkt and Familie to its Dutch prices, so every plan sits below the rival in both regions before the rise): in both regions only Flex's 2027 price passes the rival, as both of Flex's past rises did, so Flex loses 10.5 per 100 and Standaard 3.8 (moving 3.4 down), Onbeperkt 0.8 and Gezin 0.5.
5. Follow every stop since 2024 in the payments and plan periods: a subscription that stops takes its plan up again on the same account at a monthly chance that falls with the months since, rises before the summer and is highest for light listeners (58 in 100 of the lightest December stops pay again within a year, 28 of the heaviest), paying the price then in force. A forecast that treats a stop as the end puts 300 of the 1,371 October subscriptions on Flex at the end of 2027 instead of 591 and holds Standaard (EUR -1.4).
6. Measure the stayers' listening within accounts: the accounts on the plan through each month after a past rise, against their own October to December hours, the rising region against the other (a plan's average would count the light leavers' absence as listening); Onbeperkt's stayers listened 19.7 per cent more in the first month, fading over about 5.1 months, Standaard's 11.0 and Gezin's 4.8. Carrying each account's recent hours passes a pooled holdout and misses it: Onbeperkt's rise then adds EUR 4.6.
7. Carry each October subscription month by month to December 2027 with the rise and with the 2026 price held, on its own paying months, listening, country and route: net revenue after VAT and the store's fee, less EUR 0.40 per counted hour (schedule B 2.1), the stayers' extra hours from January; downgraders on the past downgraders' own months.
8. Net it per October subscription: Flex -3.3, Standaard 2.2, Onbeperkt -4.8, Gezin 5.4 euros; the rise goes ahead on Gezin and Standaard (guideline 3.10). With the rises, 3,798 of the 6,877 October subscriptions pay on some plan at the end of 2027, and the 2027 remuneration on them is EUR 119.7 (Onbeperkt) to EUR 12.1 (Flex) each.
9. The shortcuts land elsewhere: the careful reading (no return after a stop, the stayers as before) lets Gezin and Onbeperkt through; with the returns alone Gezin, Onbeperkt and Standaard; with the stayers' listening alone Gezin only; reading each plan's two past rises together, without asking whether they passed the rival, Onbeperkt; one response for every rise, none.

No other conclusion survives the records. Standaard's rise pays only because a good share of the subscriptions it loses come back within the year at the higher price, which the payments of every past stop show; Onbeperkt's fails only because the accounts that stay listen more for months after the bill, which their own hours against the other region show, and each of those hours now costs EUR 0.40; Flex's 2027 price passes the rival as its 2025 Dutch rise did; Gezin's gain holds either way. Every rival control, window, dose form, continuation, downgrader valuation and fade, and each fitted response moved 20 per cent, lets the same two rises through.
