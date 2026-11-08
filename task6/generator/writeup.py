"""task6's submission.md, drafted from the figure set deliver.figures builds: every number is emitted, never
typed. The blocks run in the platform's order: Final Recommendation, Supplementary Questions, Critical Components,
Step-by-Step."""
import common as K
from deliver import names


def write(R, F):
    pg = "partner-gateway"
    over = F["over"]
    sli, bud, share = F["sli"], F["budget"], F["share_pct"]
    kept, wtd = F["pg_kept_mix_pct"], F["pg_weighted_mix_pct"]
    order = F["start_order"]
    n_over = "five" if len(over) == 5 else str(len(over))
    h1, h2 = F["incident_minutes_text"]
    L = ["## Tags", "",
         "**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).",
         "**Analytical objective:** Descriptive & Distribution Analysis.", "",
         "## Final Recommendation", "",
         "**Five internal services ran over their 2026 latency error budget and each gets a reliability engineer for "
         "the first half of 2027: %s.**" % names(over),
         "Partner-gateway's December SLI is %s%% against its %s%% budget once each kept span counts at its trace's "
         "edge keep share. Not partner-gateway at %s%%, its own spans reweighted hour by hour on its own count, because "
         "the store kept them with the traces journey-search, seat-map and booking started at very different shares. "
         "Not the kept spans' own share, which passes journey-search, places, seat-map and partner-gateway (%s%%, "
         "%s%%, %s%% and %s%%)." % (sli[pg], bud[pg], F["pg_service_hour"], F["kept_share"]["journey-search"],
                                    F["kept_share"]["places"], F["kept_share"]["seat-map"], F["kept_share"][pg]),
         "", "## Supplementary Questions", "",
         "### %s" % K.DOCX_OUT, "",
         "1. Names the services that ran over in the order their engineers start, the one with the most requests over "
         "its latency threshold in December first, each with its share of all our services' over-threshold December "
         "requests, whole per cent: %s." % names(["%s %s%%" % (s, share[s]) for s in order]),
         "2. A table of every service's December 2026 latency SLI beside its error budget, per cent to one decimal:"]
    for s in K.SVC:
        L.append("   - %s: SLI %s against a budget of %s, %s" % (s, sli[s], bud[s],
                                                               "over" if F["ran_over"][s] == "yes" else "within"))
    L += ["3. A bar chart after that table, each service's SLI against its own budget line, the services over budget "
          "in red.",
          "4. The %s served %s%% of all our services' over-threshold December requests together and %s more "
          "over-threshold requests than their budgets allow, to the nearest ten thousand." % (
              n_over, F["over_share_pct"], F["beyond_budget"]),
          "5. Customer-facing incidents named at least one of the %s for %s minutes in the first half of 2026 and %s "
          "minutes in the second, whole minutes." % (n_over, h1, h2),
          "", "### %s" % K.CSV_OUT, "",
          "1. A row per service, columns service, latency_sli_pct, error_budget_pct and ran_over; SLI and budget per "
          "cent to one decimal:"]
    for s in K.SVC:
        L.append("   - %s: SLI %s, budget %s, ran over %s" % (s, sli[s], bud[s], F["ran_over"][s]))
    L += ["", "## Critical Components", "",
          "1. Partner-gateway's December 2026 latency SLI is **%s%%** against a **%s%%** budget." % (sli[pg], bud[pg]),
          "2. Journey-search's traces carry **%s%%** of partner-gateway's December requests but only **%s%%** of its "
          "kept spans, seat-map's **%s%%** against **%s%%** and booking's **%s%%** against **%s%%**, so each kept span "
          "counts at its own trace's edge keep share." % (
              wtd.get("journey-search", "0"), kept.get("journey-search", "0"), wtd.get("seat-map", "0"),
              kept.get("seat-map", "0"), wtd.get("booking", "0"), kept.get("booking", "0")),
          "3. Partner-gateway served **%s%%** of all our services' over-threshold December requests, the most of any "
          "service, so its engineer starts first, then %s." % (
              share[pg], names(["%s (**%s%%**)" % (s, share[s]) for s in order[1:]])),
          "4. The %s served **%s%%** of all our services' over-threshold December requests between them, **%s** more "
          "than their budgets allow." % (n_over, F["over_share_pct"], F["beyond_budget"]),
          "", "## Step-by-Step", "",
          "1. Read PR-SLO-3: a service's latency SLI is the share of the requests it handled in December 2026, in "
          "Lisbon time (UTC all month), whose server span exceeded its section 4 threshold, whether or not the "
          "tracing store kept a span for it; a breach is an SLI over its budget.",
          "2. Kept the server spans in trace_spans_2026-12.parquet, dropping the GET /healthz probes and the rows "
          "re-sent under a repeated span_id, and linked each to its trace's root, the server span with a blank "
          "parent_span_id: every internal service's span sits in a whole trace an edge service started.",
          "3. The reasonable correction that falls short: reweighting each service's own kept spans hour by hour on its "
          "own RequestCount in lb_target_group_requests_2026-H2.csv (target groups through service_catalogue_2026.xlsx) "
          "rebuilds every hourly count and the balancer's 5xx counts, and puts partner-gateway at %s%% against its %s%% "
          "budget, four services." % (F["pg_service_hour"], bud[pg]),
          "4. The traces overturn it: each edge service keeps a flat few dozen root spans an hour whatever its "
          "traffic, and partner-gateway's kept spans are %s%% journey-search's traces, %s%% seat-map's and %s%% "
          "booking's, while journey-search's traces, kept most thinly and carrying the slow availability lookups, "
          "make %s%% of its requests." % (kept.get("journey-search", "0"), kept.get("seat-map", "0"),
                                          kept.get("booking", "0"), wtd.get("journey-search", "0")),
          "5. For each edge service and hour, divided its RequestCount by the root spans it kept, the weight of every "
          "span in the traces it started that hour, then divided each service's weighted spans over its threshold by "
          "its December RequestCount: partner-gateway %s%%, journey-search %s%%, places %s%%, seat-map %s%% and "
          "notifications %s%%, the other five under budget, so those %s get an engineer." % (
              sli[pg], sli["journey-search"], sli["places"], sli["seat-map"], sli["notifications"], n_over),
          "6. Each service's weighted spans over its threshold are its over-threshold December requests: of all ten "
          "services' total, %s, so the engineers start in that order; the %s served %s%% between them, and their "
          "over-threshold requests less each budget times its December RequestCount come to %s." % (
              names(["%s%s %s%%" % (s, " served" if i == 0 else "", share[s]) for i, s in enumerate(order)]),
              n_over, F["over_share_pct"],
              F["beyond_budget"]),
          "7. Read on step 3's correction, the same figures name four services that served %s%%, %s first, with "
          "partner-gateway at %s%% and outside the programme, and %s beyond budget." % (
              F["shallow_over_share_pct"], F["shallow_order"][0], F["shallow_pg_share_pct"],
              F["shallow_beyond_budget"]),
          "8. Incident minutes (PR-SLO-3 sections 5.2 and 5.4): each incident in incidents_2026.csv matched to its "
          "status page post by component and time, its end the last of its components back to operational, each "
          "service counted from the moment incident_timeline_2026.csv names it, every minute in which an incident "
          "named at least one of the %s counted once, the halves split at 1 July 00:00 Lisbon time: %s and %s "
          "minutes." % (n_over, h1, h2),
          "",
          "No other conclusion survives. Every weighting the whole traces leave standing (each span at its trace's "
          "edge keep share over the balancer's count or over the weighted kept count, the weights calibrated hour by "
          "hour, the root's hour or the span's own, spans whose trace began in November dropped or reweighted) gives "
          "the same one-decimal SLIs, the same start order, the same whole-per-cent shares, %s%% and %s. The kept "
          "spans' own share, a day or hour-of-day weighting and each service's own spans reweighted on its own hourly "
          "count all treat a span as kept at its own service's rate, which the store's whole-trace sampling at the "
          "edge rules out; each passes partner-gateway and leaves it out of the programme." % (
              F["over_share_pct"], F["beyond_budget"])]
    text = "\n".join(L) + "\n"
    F["sections"] = ["5.2", "5.4"]
    return text, F
