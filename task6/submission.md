## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## Final Recommendation

**Put reliability engineers on partner-gateway, places, fares, seat-map and notifications, in that order: the five ran over their 2026 latency error budgets.** Not the six the trace export's own hours give (journey-search reads 1.1% there against its 1.0%, and 0.8% across December once the 274 hours before the export are counted from the tracing store's span metrics), not places and seat-map alone, which each service's own hourly count gives (partner-gateway 1.0%, fares 0.9%, notifications 0.7%), and not a list with journey-search in place of fares and notifications, which putting each December incident on the service furthest over its load curve gives.

## Supplementary Questions

### reliability_review_2026.docx

A short review: the call and the start order on the first page, then every service against its budget with the chart, December's incidents, and how the SLI was read.

1. The services that ran over, in the order their engineers start, each with its share of the over-threshold requests all the services' SLIs count (whole per cent, 1 point either way accepted) and a 90 per cent confidence interval on its SLI (per cent, each end within 0.03):
   a. partner-gateway: 33% of the over-threshold requests, interval 2.17 to 2.41.
   b. places: 29% of the over-threshold requests, interval 1.27 to 1.55.
   c. fares: 17% of the over-threshold requests, interval 1.20 to 1.40.
   d. seat-map: 3% of the over-threshold requests, interval 1.80 to 2.07.
   e. notifications: 3% of the over-threshold requests, interval 1.19 to 1.42.
   f. Between them the five served 200,000 more over-threshold requests than their budgets allow (190,000 to 220,000 accepted).
2. Every service's December 2026 latency SLI beside its error budget (per cent; where a range follows the SLI, any figure in it is accepted), with a bar chart of each SLI against its own budget line:
   a. journey-search: SLI 0.8 (0.76 to 0.86) against a budget of 1.0, within.
   b. fares: SLI 1.3 (1.27 to 1.34) against a budget of 1.0, over.
   c. places: SLI 1.4 (1.37 to 1.45) against a budget of 1.0, over.
   d. seat-map: SLI 1.9 against a budget of 1.0, over.
   e. booking: SLI 0.3 against a budget of 0.5, within.
   f. payments: SLI 0.2 against a budget of 0.5, within.
   g. tickets: SLI 0.7 against a budget of 1.0, within.
   h. accounts: SLI 1.2 (1.20 to 1.26) against a budget of 2.0, within.
   i. partner-gateway: SLI 2.3 against a budget of 2.0, over.
   j. notifications: SLI 1.3 (1.27 to 1.32) against a budget of 1.0, over.
3. The service that owned the root cause of each customer-facing incident in December:
   a. INC-1570, declared 13 December 12:24, naming partner-gateway and seat-map: seat-map.
   b. INC-1579, declared 14 December 12:31, naming seat-map and partner-gateway: partner-gateway.
   c. INC-1588, declared 15 December 19:41, naming journey-search, partner-gateway and fares: partner-gateway.
   d. INC-1594, declared 17 December 20:49, naming booking, payments and notifications: payments.
   e. INC-1611, declared 21 December 19:46, naming journey-search, fares and booking: fares.
   f. INC-1619, declared 26 December 18:01, naming accounts, notifications and payments: notifications.
   g. INC-1627, declared 29 December 10:12, naming places: places.

### service_sli_2026.csv

Ten rows, one per service; columns service, latency_sli_pct, error_budget_pct, ran_over, incident_minutes_h1 and incident_minutes_h2.

4. Each service's SLI, budget, whether it ran over and its customer-facing incident minutes in each half of 2026 (whole minutes, counted from when the incident tool added the service):
   a. journey-search: SLI 0.8, budget 1.0, ran over no, incident minutes 149 and 584.
   b. fares: SLI 1.3, budget 1.0, ran over yes, incident minutes 266 and 534.
   c. places: SLI 1.4, budget 1.0, ran over yes, incident minutes 430 and 249.
   d. seat-map: SLI 1.9, budget 1.0, ran over yes, incident minutes 690 and 216.
   e. booking: SLI 0.3, budget 0.5, ran over no, incident minutes 421 and 483.
   f. payments: SLI 0.2, budget 0.5, ran over no, incident minutes 345 and 471.
   g. tickets: SLI 0.7, budget 1.0, ran over no, incident minutes 254 and 371.
   h. accounts: SLI 1.2, budget 2.0, ran over no, incident minutes 128 and 626.
   i. partner-gateway: SLI 2.3, budget 2.0, ran over yes, incident minutes 292 and 659.
   j. notifications: SLI 1.3, budget 1.0, ran over yes, incident minutes 99 and 680.

## Critical Components

1. The service whose SLI counts the most over-threshold requests, and so starts first, is **partner-gateway**; payments' December SLI is **0.2%**, within its 0.5%.
2. **INC-1579** was **partner-gateway's** own failure, **INC-1611** **fares'** and **INC-1619** **notifications'**.
3. Places' December SLI is **1.4%** (1.37 to 1.45 accepted) and booking's **0.3%**.

## Step-by-Step

1. Kept the server spans in trace_spans_2026-12.parquet once each (a re-sent span id counted once) and linked each to its trace's root, the server span with no parent; mapped tracing names and target groups through service_catalogue_2026.xlsx; read thresholds and budgets from section 4 of PR-SLO-3_service_level_objectives_2026.docx.
2. Reconciled incidents_2026.csv, incident_timeline_2026.csv and status_page_history_2026.json: a customer-facing incident ends when the status page shows its last component operational, a service counts from when the timeline adds it, and the halves split at 1 July 00:00 Lisbon time; that gives the incident minutes of the CSV and the windows the standard's incident clause leaves out.
3. The reasonable route that falls short: each service's own spans reweighted on its own hourly RequestCount from lb_target_group_requests_2026-H2.csv over the hours the export holds, with each December incident put on the named service furthest over its load curve across the incident, gives journey-search, places and seat-map as the services over budget (partner-gateway 1.3%, journey-search 1.7%).
4. The traces overturn the weighting: the store kept a near-fixed number of whole traces an hour per edge service, so an internal service's kept spans carry its callers' keep shares. Counted each kept span at its trace root's hourly keep share (the root's RequestCount over the roots kept that hour): partner-gateway's slow calls come in through busy, thinly kept journey-search and weigh far more than its own count gives them, while payments' slow calls come through quiet, thickly kept booking and weigh less (0.5% on its own count, 0.2% at the roots' shares).
5. The export overturns the period: its first span starts at 12 December 10:00, so the first 274 hours of December, 33% of the month's edge requests, have no spans, and the standard counts a request whether or not a span was kept. tracing_span_metrics_2026-12.csv holds those hours: the hourly duration histogram of every span the store ingested, by service and span name, the same spans as the export wherever the two overlap. For each server series in those hours, counted the spans over the service's threshold and weighted them like the spans themselves (an internal operation by the keep shares of the edge services whose client spans called it that hour). For seat-map, booking, payments, tickets and partner-gateway the threshold is a histogram boundary and nothing is estimated.
6. For journey-search, fares, places, accounts and notifications the threshold sits inside a bucket, and the bucket was split at the share of its spans over the threshold that the service's held, incident-free spans show in the same band of hourly load (five bands). Straight-line interpolation inside the bucket is the shortcut that fails: on the hours the export holds it rebuilds 3.0 times the over-threshold requests the spans themselves show for places and 1.9 times for journey-search, and would put places at 2.0% and fares at 1.6%. With the hours counted, journey-search falls from 1.1% on the export's hours to 0.8% and places from 1.7% to 1.4%.
7. Dated each December incident's cause: for every service it named, the own handling time of each span (less the calls it waited on) against a load curve fitted on the export's incident-free hours, a changepoint on the residuals; the earliest sustained rise owns the cause. Over the whole incident seat-map in INC-1579, journey-search in INC-1611 and accounts in INC-1619 ran furthest above their curves, but each rose only after the service it calls had: partner-gateway, fares and notifications own them.
8. Left each named service's requests out from when the timeline added it to the incident's end unless it owned the cause, and compared each SLI with its budget: fares, places, seat-map, partner-gateway and notifications ran over.
9. Took each over-budget SLI's 90 per cent interval by linearisation over strata of root service and hour with the kept traces as units, the hours read from the span metrics adding their own sampling error and the error of each bucket's split; a trace bootstrap with the splits refitted agrees within 0.03.
10. Each service's weighted spans over its threshold are the requests its SLI counts: the engineers start with partner-gateway (33%), and the five served 200,000 more than their budgets allow.

No other conclusion survives, and the three judgments are independent. Leave out the trace roots' weights alone and the list is places and seat-map (partner-gateway 1.0%, fares 0.9%, notifications 0.7%). Leave out the dated causes alone and it is journey-search, places, seat-map and partner-gateway (fares 0.8%, notifications 0.9%, journey-search 1.2%). Leave out the hours before the export alone and it is the five with journey-search (1.1%). Leave out the weights and the dated causes and it is journey-search, places and seat-map; the weights and the early hours, journey-search, fares, places and seat-map; the dated causes and the early hours, journey-search, places, seat-map and partner-gateway. Every split of a threshold's bucket the held spans support (one pooled share, two to thirty load bands, a logit in load, the hour of day) gives the same five, the same order and SLIs inside the ranges above; so do interpolation inside the bucket and the bucket's two bounds for the list, though not for the figures. A fill that reads no span metrics and gives the early hours the export's own share puts partner-gateway at 2.9%, where the span metrics, whose 1,000 ms boundary is its threshold, count 2.3% with nothing estimated. The thinnest margin is in the start order: seat-map counts 8 per cent more over-threshold requests than notifications, and holds that place under every split.
