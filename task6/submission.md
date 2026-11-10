## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## Final Recommendation

**Put reliability engineers on partner-gateway, places, fares, seat-map and notifications, in that order: the five ran over their 2026 latency error budgets.** Not journey-search, fares, places and seat-map, which each service's own spans reweighted on its own hourly count over the hours the trace export holds give: journey-search's 1.3% on those hours is 0.9% across December once the 11 days the store had already dropped are counted at the share their load gives, and partner-gateway and notifications run over only with each span at its trace root's keep share and each December incident on the service whose own handling slowed first.

## Supplementary Questions

### reliability_review_2026.docx

1. Names the services that ran over in the order their engineers start, the one whose SLI counts the most requests over its threshold first, each with its share of the over-threshold requests all our services' SLIs count (whole per cent) and a 90 per cent confidence interval on its SLI (per cent to two decimals): partner-gateway 33%, interval 2.20 to 2.42; places 29%, interval 1.24 to 1.52; fares 17%, interval 1.19 to 1.40; seat-map 3%, interval 1.82 to 2.14; notifications 3%, interval 1.08 to 1.31.
2. A table of every service's December 2026 latency SLI beside its error budget, per cent to one decimal:
   - journey-search: SLI 0.9 against a budget of 1.0, within
   - fares: SLI 1.3 against a budget of 1.0, over
   - places: SLI 1.4 against a budget of 1.0, over
   - seat-map: SLI 2.0 against a budget of 1.0, over
   - booking: SLI 0.3 against a budget of 0.5, within
   - payments: SLI 0.2 against a budget of 0.5, within
   - tickets: SLI 0.7 against a budget of 1.0, within
   - accounts: SLI 1.3 against a budget of 2.0, within
   - partner-gateway: SLI 2.3 against a budget of 2.0, over
   - notifications: SLI 1.2 against a budget of 1.0, over
3. A bar chart of each service's SLI against its own budget line, the services over budget in red.
4. The service that owned the root cause of each customer-facing incident in December:
   - INC-1570, declared 13 December 12:24, naming partner-gateway, seat-map: seat-map
   - INC-1579, declared 14 December 12:31, naming seat-map, partner-gateway: partner-gateway
   - INC-1588, declared 15 December 19:41, naming journey-search, partner-gateway, fares: partner-gateway
   - INC-1594, declared 17 December 20:49, naming booking, payments, notifications: payments
   - INC-1611, declared 21 December 19:46, naming journey-search, fares, booking: fares
   - INC-1619, declared 26 December 18:01, naming accounts, notifications, payments: notifications
   - INC-1627, declared 29 December 10:12, naming places: places
5. The five served 84% of the over-threshold requests all our services' SLIs count, and 200,000 more than their budgets allow, to the nearest ten thousand.

### service_sli_2026.csv

1. A row per service, columns service, latency_sli_pct, error_budget_pct, ran_over, incident_minutes_h1 and incident_minutes_h2; SLI and budget per cent to one decimal, minutes whole, each service counted from when the incident tool added it:
   - journey-search: SLI 0.9, budget 1.0, ran over no, incident minutes 149 and 584
   - fares: SLI 1.3, budget 1.0, ran over yes, incident minutes 266 and 534
   - places: SLI 1.4, budget 1.0, ran over yes, incident minutes 430 and 249
   - seat-map: SLI 2.0, budget 1.0, ran over yes, incident minutes 690 and 216
   - booking: SLI 0.3, budget 0.5, ran over no, incident minutes 421 and 483
   - payments: SLI 0.2, budget 0.5, ran over no, incident minutes 345 and 471
   - tickets: SLI 0.7, budget 1.0, ran over no, incident minutes 254 and 371
   - accounts: SLI 1.3, budget 2.0, ran over no, incident minutes 128 and 626
   - partner-gateway: SLI 2.3, budget 2.0, ran over yes, incident minutes 292 and 659
   - notifications: SLI 1.2, budget 1.0, ran over yes, incident minutes 99 and 680

## Critical Components

1. **INC-1611** was **fares'** own failure and **INC-1619** **notifications'**: fares' own handling and notifications' SMS verification rose above their load curves **first**, and journey-search's own handling and accounts' sign-in handling only after them, though those ran further over their curves across each incident.
2. With each kept span counted at its trace root's hourly keep share, partner-gateway's December SLI is **2.3%** against **2.0%**, fares' **1.3%** against **1.0%** and notifications' **1.2%** against **1.0%**; on each service's own hourly count, with the same incident time left out, they are 1.0%, 0.9% and 0.6%.
3. The trace export begins at **12 December 10:00**: December's first 11 days (33% of its edge requests) still count, each service's requests in each of those hours at the share over threshold its held, incident-free hours show at the same load, so journey-search's December SLI is **0.9%**, against **1.3%** on the export's hours alone.
4. Partner-gateway's 90 per cent interval runs **2.20% to 2.42%**, the traces taken as whole units within each root service's hour and the dropped hours' estimate carried with them.
5. The five served **84%** of the over-threshold requests the SLIs count, **200,000** more than their budgets allow.

## Step-by-Step

1. Kept the server spans in trace_spans_2026-12.parquet once each (a re-sent span id counted once) and linked each to its trace's root, the server span with no parent; counted the roots each edge service kept in each hour against its RequestCount in lb_target_group_requests_2026-H2.csv (target groups through service_catalogue_2026.xlsx).
2. Reconciled incidents_2026.csv, incident_timeline_2026.csv and status_page_history_2026.json: each customer-facing incident ends when the status page shows its last component operational, a service counts from when the timeline adds it, halves split at 1 July 00:00 Lisbon time; partner-gateway 292 and 659 minutes, notifications 99 and 680.
3. The reasonable route that falls short: each service's own spans reweighted on its own hourly count over the hours the export holds, with each incident's cause dated as in step 6, puts journey-search at 1.3%, fares at 1.2%, partner-gateway at 1.4% and notifications at 0.7%, so journey-search, fares, places and seat-map ran over.
4. The traces overturn it: the store kept a near-fixed number of whole traces an hour per edge service, so an internal service's kept spans carry its callers' keep shares; counted at its trace root's share (the root's RequestCount over the roots kept that hour), each internal service's slow operations, called from busy and thinly kept journey-search and accounts, weigh what they served.
5. The export overturns the period: its first span starts at 12 December 10:00, so December's first 11 days, 33% of its edge requests, are not in it, and they still count (PR-SLO-3 2.2, kept or not). Counted each service's requests in each of those hours, from lb_target_group_requests_2026-H2.csv, at the share over threshold its held, incident-free hours show in the same band of hourly load (ten bands): the early weeks were quieter, so journey-search falls from 1.3% on the export's hours to 0.9%, and every other SLI moves with it. Fitted on the export from 18 December, these bands predict its own 12 to 17 December at 0.81 of the over-threshold requests seen there, where matching the same weekday and hour predicts 1.96, so the match that ignores load, which leaves journey-search over, is ruled out.
6. Dated each December incident's cause: for every service it named, the own handling time of each span (less the calls it waited on) against a load curve fitted on the export's incident-free hours, a changepoint on the residuals; the earliest sustained rise owns the cause. Over the whole incident seat-map in INC-1579, journey-search in INC-1611 and accounts in INC-1619 ran furthest above their curves, but each rose only after the service it calls had, by twenty minutes or more: partner-gateway, fares and notifications own them.
7. Left each named service's requests out from when the timeline added it to the incident's end unless it owned the cause (PR-SLO-3's incident and root-cause clauses): fares, places, seat-map, partner-gateway and notifications ran over.
8. Took each over-budget SLI's 90 per cent interval by linearisation over strata of root service and hour with the kept traces as units, each trace also moving the band shares the dropped hours were counted at: partner-gateway 2.20% to 2.42%.
9. Each service's weighted spans over its threshold are the requests its SLI counts: the engineers start with partner-gateway (33%), the five served 84% together and 200,000 more than their budgets allow.

No other conclusion survives. Weighting each span by its own service's hourly count, or leaving the spans unweighted, keeps the slow operations of fares, partner-gateway and notifications at their callers' kept shares; reading December from the export's hours alone counts only the busy weeks and puts journey-search over; putting each December incident on the service the responders named first or last, on the one with the most slow requests, or on the one furthest over its load curve across the whole incident, charges journey-search and accounts with fares' and notifications' own failures on 21 and 26 December. Every weighting the whole traces leave standing (the balancer's count or the weighted kept count as the base, the root's hour or the span's own), every way of counting the dropped hours at their load that the held hours support (ten or twenty bands, a share that never falls as load rises, a curved logit, the called services' loads beside the service's own) and every reasonable reading of the onset gives the same five, the same order and the same rounded figures; a share linear in log load is ruled out by the held hours themselves, which bend at the busiest hours.
