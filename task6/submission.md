## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## Final Recommendation

**Put reliability engineers on places, partner-gateway, fares, seat-map and notifications, in that order: the five ran over their 2026 latency error budgets.** Not places and seat-map alone, which each service's own spans reweighted on its own hourly count give even with every incident's cause dated right (fares 0.9%, partner-gateway 1.1%, notifications 0.8%), and not without fares and notifications, which fall to 0.9% each when INC-1611 and INC-1619 are put on journey-search and accounts, the services furthest over their load curves, rather than on fares and notifications, whose own handling slowed first.

## Supplementary Questions

### reliability_review_2026.docx

1. Names the services that ran over in the order their engineers start, the one whose SLI counts the most requests over its threshold first, each with its share of the over-threshold requests all our services' SLIs count (whole per cent) and a 90 per cent confidence interval on its SLI (per cent to two decimals): places 36%, interval 1.56 to 2.01; partner-gateway 31%, interval 2.08 to 2.44; fares 16%, interval 1.15 to 1.45; seat-map 3%, interval 1.77 to 2.26; notifications 3%, interval 1.14 to 1.49.
2. A table of every service's December 2026 latency SLI beside its error budget, per cent to one decimal:
   - journey-search: SLI 0.5 against a budget of 1.0, within
   - fares: SLI 1.3 against a budget of 1.0, over
   - places: SLI 1.8 against a budget of 1.0, over
   - seat-map: SLI 2.0 against a budget of 1.0, over
   - booking: SLI 0.3 against a budget of 0.5, within
   - payments: SLI 0.2 against a budget of 0.5, within
   - tickets: SLI 0.6 against a budget of 1.0, within
   - accounts: SLI 1.4 against a budget of 2.0, within
   - partner-gateway: SLI 2.3 against a budget of 2.0, over
   - notifications: SLI 1.3 against a budget of 1.0, over
3. A bar chart of each service's SLI against its own budget line, the services over budget in red.
4. The service that owned the root cause of each customer-facing incident in December:
   - INC-1570, declared 8 December 12:24, naming partner-gateway, seat-map: seat-map
   - INC-1579, declared 14 December 12:31, naming seat-map, partner-gateway: partner-gateway
   - INC-1588, declared 15 December 19:41, naming journey-search, partner-gateway, fares: partner-gateway
   - INC-1594, declared 17 December 20:49, naming booking, payments, notifications: payments
   - INC-1611, declared 21 December 19:46, naming journey-search, fares, booking: fares
   - INC-1619, declared 26 December 18:01, naming accounts, notifications, payments: notifications
   - INC-1627, declared 29 December 10:12, naming places: places
5. The five served 89% of the over-threshold requests all our services' SLIs count, and 280,000 more than their budgets allow, to the nearest ten thousand.

### service_sli_2026.csv

1. A row per service, columns service, latency_sli_pct, error_budget_pct, ran_over, incident_minutes_h1 and incident_minutes_h2; SLI and budget per cent to one decimal, minutes whole, each service counted from when the incident tool added it:
   - journey-search: SLI 0.5, budget 1.0, ran over no, incident minutes 149 and 584
   - fares: SLI 1.3, budget 1.0, ran over yes, incident minutes 266 and 534
   - places: SLI 1.8, budget 1.0, ran over yes, incident minutes 430 and 249
   - seat-map: SLI 2.0, budget 1.0, ran over yes, incident minutes 690 and 216
   - booking: SLI 0.3, budget 0.5, ran over no, incident minutes 421 and 483
   - payments: SLI 0.2, budget 0.5, ran over no, incident minutes 345 and 471
   - tickets: SLI 0.6, budget 1.0, ran over no, incident minutes 254 and 371
   - accounts: SLI 1.4, budget 2.0, ran over no, incident minutes 128 and 626
   - partner-gateway: SLI 2.3, budget 2.0, ran over yes, incident minutes 292 and 659
   - notifications: SLI 1.3, budget 1.0, ran over yes, incident minutes 99 and 680

## Critical Components

1. INC-1611 and INC-1619 were fares' and notifications' own failures: fares' own handling rose above its load curve from about **19:45** and journey-search's own handling only from about **20:25**; notifications' SMS verification rose above its load curve from about **17:00** and accounts' sign-in handling only from about **18:35**.
2. With each kept span counted at its trace root's hourly keep share, partner-gateway's December SLI is **2.3%** against **2.0%**, fares' **1.3%** against **1.0%** and notifications' **1.3%** against **1.0%**; on each service's own hourly count, with the same incident time left out, they are 1.1%, 0.9% and 0.8%.
3. Partner-gateway's 90 per cent interval runs **2.08% to 2.44%**, the traces taken as whole units within each root service's hour.
4. The five served **89%** of the over-threshold requests the SLIs count, **280,000** more than their budgets allow.

## Step-by-Step

1. Kept the server spans in trace_spans_2026-12.parquet once each (a re-sent span id counted once) and linked each to its trace's root, the server span with no parent; counted the roots each edge service kept in each hour against its RequestCount in lb_target_group_requests_2026-H2.csv (target groups through service_catalogue_2026.xlsx).
2. Reconciled incidents_2026.csv, incident_timeline_2026.csv and status_page_history_2026.json: each customer-facing incident ends when the status page shows its last component operational, a service counts from when the timeline adds it, halves split at 1 July 00:00 Lisbon time; partner-gateway 292 and 659 minutes, notifications 99 and 680.
3. The reasonable route that falls short: each service's own spans reweighted on its own hourly count, with each incident's cause dated as in step 5, puts fares at 0.9%, partner-gateway at 1.1% and notifications at 0.8%, so only places and seat-map ran over.
4. The traces overturn it: the store kept a near-fixed number of whole traces an hour per edge service, so an internal service's kept spans carry its callers' keep shares; counted at its trace root's share (the root's RequestCount over the roots kept that hour), each internal service's slow operations, called from busy and thinly kept journey-search and accounts, weigh what they served.
5. Dated each December incident's cause: for every service it named, the own handling time of each span (less the calls it waited on) against a load curve fitted on December's incident-free hours, a changepoint on the residuals; the earliest sustained rise owns the cause. Over the whole incident seat-map in INC-1579, journey-search in INC-1611 and accounts in INC-1619 ran furthest above their curves, but each rose only after the service it calls: partner-gateway from about 12:15 against 13:00; fares from about 19:45 against 20:25; notifications from about 17:00 against 18:35.
6. Left each named service's requests out from when the timeline added it to the incident's end unless it owned the cause (PR-SLO-3's incident and root-cause clauses): fares, places, seat-map, partner-gateway and notifications ran over.
7. Took each over-budget SLI's 90 per cent interval by linearisation over strata of root service and hour with the kept traces as units: partner-gateway 2.08% to 2.44%.
8. Each service's weighted spans over its threshold are the requests its SLI counts: the engineers start with places (36%), the five served 89% together and 280,000 more than their budgets allow.

No other conclusion survives. Weighting each span by its own service's hourly count, or leaving the spans unweighted, keeps the slow operations of fares, partner-gateway and notifications at their callers' kept shares; putting each December incident on the service the responders named first or last, on the one with the most slow requests, or on the one furthest over its load curve across the whole incident, charges journey-search and accounts with fares' and notifications' own failures on 21 and 26 December. Every weighting the whole traces leave standing (the balancer's count or the weighted kept count as the base, the root's hour or the span's own) and every reasonable reading of the onset gives the same five, the same order and the same rounded figures.
