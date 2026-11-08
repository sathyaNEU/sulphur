## Tags

**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).
**Analytical objective:** Descriptive & Distribution Analysis.

## Final Recommendation

**Five internal services ran over their 2026 latency error budget and each gets a reliability engineer for the first half of 2027: journey-search, places, seat-map, partner-gateway and notifications.**
Partner-gateway's December SLI is 2.9% against its 2.0% budget once each kept span counts at its trace's edge keep share. Not partner-gateway at 1.4%, its own spans reweighted hour by hour on its own count, because the store kept them with the traces journey-search, seat-map and booking started at very different shares. Not the kept spans' own share, which passes journey-search, places, seat-map and partner-gateway (0.7%, 0.7%, 0.7% and 0.8%).

## Supplementary Questions

### reliability_review_2026.docx

1. Names the services that ran over in the order their engineers start, the one with the most requests over its latency threshold in December first, each with its share of all our services' over-threshold December requests, whole per cent: partner-gateway 40%, places 31%, journey-search 16%, seat-map 2% and notifications 1%.
2. A table of every service's December 2026 latency SLI beside its error budget, per cent to one decimal:
   - journey-search: SLI 1.3 against a budget of 1.0, over
   - fares: SLI 0.6 against a budget of 1.0, within
   - places: SLI 1.5 against a budget of 1.0, over
   - seat-map: SLI 1.5 against a budget of 1.0, over
   - booking: SLI 0.4 against a budget of 0.5, within
   - payments: SLI 0.3 against a budget of 0.5, within
   - tickets: SLI 0.6 against a budget of 1.0, within
   - accounts: SLI 0.7 against a budget of 1.0, within
   - partner-gateway: SLI 2.9 against a budget of 2.0, over
   - notifications: SLI 1.6 against a budget of 1.0, over
3. A bar chart after that table, each service's SLI against its own budget line, the services over budget in red.
4. The five served 90% of all our services' over-threshold December requests together and 300,000 more over-threshold requests than their budgets allow, to the nearest ten thousand.
5. Customer-facing incidents named at least one of the five for 1,545 minutes in the first half of 2026 and 907 minutes in the second, each service counting from when the incident tool added it, whole minutes.

### service_sli_2026.csv

1. A row per service, columns service, latency_sli_pct, error_budget_pct and ran_over; SLI and budget per cent to one decimal:
   - journey-search: SLI 1.3, budget 1.0, ran over yes
   - fares: SLI 0.6, budget 1.0, ran over no
   - places: SLI 1.5, budget 1.0, ran over yes
   - seat-map: SLI 1.5, budget 1.0, ran over yes
   - booking: SLI 0.4, budget 0.5, ran over no
   - payments: SLI 0.3, budget 0.5, ran over no
   - tickets: SLI 0.6, budget 1.0, ran over no
   - accounts: SLI 0.7, budget 1.0, ran over no
   - partner-gateway: SLI 2.9, budget 2.0, ran over yes
   - notifications: SLI 1.6, budget 1.0, ran over yes

## Critical Components

1. Partner-gateway's December 2026 latency SLI is **2.9%** against a **2.0%** budget.
2. Journey-search's traces carry **85%** of partner-gateway's December requests but only **33%** of its kept spans, seat-map's **12%** against **33%** and booking's **4%** against **34%**, so each kept span counts at its own trace's edge keep share.
3. Partner-gateway served **40%** of all our services' over-threshold December requests, the most of any service, so its engineer starts first, then places (**31%**), journey-search (**16%**), seat-map (**2%**) and notifications (**1%**).
4. The five served **90%** of all our services' over-threshold December requests between them, **300,000** more than their budgets allow.

## Step-by-Step

1. Read PR-SLO-3: a service's latency SLI is the share of the requests it handled in December 2026, in Lisbon time (UTC all month), whose server span exceeded its section 4 threshold, whether or not the tracing store kept a span for it; a breach is an SLI over its budget.
2. Kept the server spans in trace_spans_2026-12.parquet, dropping the GET /healthz probes and the rows re-sent under a repeated span_id, and linked each to its trace's root, the server span with a blank parent_span_id: every internal service's span sits in a whole trace an edge service started.
3. The reasonable correction that falls short: reweighting each service's own kept spans hour by hour on its own RequestCount in lb_target_group_requests_2026-H2.csv (target groups through service_catalogue_2026.xlsx) rebuilds every hourly count and the balancer's 5xx counts, and puts partner-gateway at 1.4% against its 2.0% budget, four services.
4. The traces overturn it: each edge service keeps a flat few dozen root spans an hour whatever its traffic, and partner-gateway's kept spans are 33% journey-search's traces, 33% seat-map's and 34% booking's, while journey-search's traces, kept most thinly and carrying the slow availability lookups, make 85% of its requests.
5. For each edge service and hour, divided its RequestCount by the root spans it kept, the weight of every span in the traces it started that hour, then divided each service's weighted spans over its threshold by its December RequestCount: partner-gateway 2.9%, journey-search 1.3%, places 1.5%, seat-map 1.5% and notifications 1.6%, the other five under budget, so those five get an engineer.
6. Each service's weighted spans over its threshold are its over-threshold December requests: of all ten services' total, partner-gateway served 40%, places 31%, journey-search 16%, seat-map 2% and notifications 1%, so the engineers start in that order; the five served 90% between them, and their over-threshold requests less each budget times its December RequestCount come to 300,000.
7. Read on step 3's correction, the same figures name four services that served 62%, places first, with partner-gateway at 25% and outside the programme, and 160,000 beyond budget.
8. Incident minutes (PR-SLO-3 sections 5.2 and 5.4): each incident in incidents_2026.csv matched to its status page post by component and time, its end the last of its components back to operational, each service counted from the moment incident_timeline_2026.csv names it, every minute in which an incident named at least one of the five counted once, the halves split at 1 July 00:00 Lisbon time: 1,545 and 907 minutes.

No other conclusion survives. Every weighting the whole traces leave standing (each span at its trace's edge keep share over the balancer's count or over the weighted kept count, the weights calibrated hour by hour, the root's hour or the span's own, spans whose trace began in November dropped or reweighted) gives the same one-decimal SLIs, the same start order, the same whole-per-cent shares, 90% and 300,000. The kept spans' own share, a day or hour-of-day weighting and each service's own spans reweighted on its own hourly count all treat a span as kept at its own service's rate, which the store's whole-trace sampling at the edge rules out; each passes partner-gateway and leaves it out of the programme.
