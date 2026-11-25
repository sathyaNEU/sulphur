"""task6's submission.md, drafted from the figure set deliver.figures builds: every number is emitted, never
typed. The blocks run in the platform's order: Final Recommendation, Supplementary Questions, Critical Components,
Step-by-Step."""
import common as K
from deliver import names, handling


def poss(s):
    return s + ("'" if s.endswith("s") else "'s")


def letters():
    for c in "abcdefghijklmnopqrstuvwxyz":
        yield c


def write(R, F):
    over, order = F["over"], F["start_order"]
    sli, bud, share, ci, mins = F["sli"], F["budget"], F["share_pct"], F["ci"], F["minutes"]
    own, win, exp = F["own_sli"], F["window_sli"], F["export_sli"]
    js, pg, fa, no, pl, bk, pay = ("journey-search", "partner-gateway", "fares", "notifications", "places", "booking",
                                   "payments")
    n_over = "five" if len(over) == 5 else str(len(over))
    dec = [x for x in F["incidents"] if x["id"] in F["deciding"]]      # the misreadings that move a verdict
    mis = [x for x in F["incidents"] if x["id"] in F["misread"]]       # every incident the whole-window reading misreads
    band = F["sli_band"]

    def sli_txt(s):
        return "%s (%s to %s)" % (sli[s], band[s][0], band[s][1]) if s in band else sli[s]

    L = ["## Tags", "",
         "**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).",
         "**Analytical objective:** Descriptive & Distribution Analysis.", "",
         "## Final Recommendation", "",
         "**Put reliability engineers on %s, in that order: the %s ran over their 2026 latency error budgets.** "
         "Not the six the trace export's own hours give (journey-search reads %s%% there against its %s%%, and %s%% "
         "across December once the %s hours before the export are counted from the tracing store's span metrics), "
         "not %s alone, which each service's own hourly count gives (partner-gateway %s%%, fares %s%%, notifications "
         "%s%%), and not a list with journey-search in place of fares and notifications, which putting each December "
         "incident on the service furthest over its load curve gives."
         % (names(order), n_over, exp[js], bud[js], sli[js], F["gone_hours"], names(F["own_over"]), own[pg], own[fa],
            own[no]),
         "", "## Supplementary Questions", "",
         "### %s" % K.DOCX_OUT, "",
         "A short review: the call and the start order on the first page, then every service against its budget with "
         "the chart, December's incidents, and how the SLI was read.", "",
         "1. The services that ran over, in the order their engineers start, each with its share of the "
         "over-threshold requests all the services' SLIs count (whole per cent, %s point either way accepted) and a "
         "%s per cent confidence interval on its SLI (per cent, each end within %s):" % (
             F["share_room_pts"], F["interval_level_pct"], F["ci_room"])]
    it = letters()
    for s in order:
        L.append("   %s. %s: %s%% of the over-threshold requests, interval %s to %s." % (
            next(it), s, share[s], ci[s][0], ci[s][1]))
    L.append("   %s. Between them the %s served %s more over-threshold requests than their budgets allow (%s to %s "
             "accepted)." % (next(it), n_over, F["beyond_budget"], F["beyond_band"][0], F["beyond_band"][1]))
    L.append("2. Every service's December 2026 latency SLI beside its error budget (per cent; where a range follows "
             "the SLI, any figure in it is accepted), with a bar chart of each SLI against its own budget line:")
    it = letters()
    for s in K.SVC:
        L.append("   %s. %s: SLI %s against a budget of %s, %s." % (
            next(it), s, sli_txt(s), bud[s], "over" if F["ran_over"][s] == "yes" else "within"))
    L.append("3. The service that owned the root cause of each customer-facing incident in December:")
    it = letters()
    for x in F["incidents"]:
        L.append("   %s. %s, declared %s, naming %s: %s." % (next(it), x["id"], x["declared"], names(x["named"]),
                                                             x["cause"]))
    L += ["", "### %s" % K.CSV_OUT, "",
          "Ten rows, one per service; columns service, latency_sli_pct, error_budget_pct, ran_over, "
          "incident_minutes_h1 and incident_minutes_h2.", "",
          "4. Each service's SLI, budget, whether it ran over and its customer-facing incident minutes in each half "
          "of 2026 (whole minutes, counted from when the incident tool added the service):"]
    it = letters()
    for s in K.SVC:
        L.append("   %s. %s: SLI %s, budget %s, ran over %s, incident minutes %s and %s." % (
            next(it), s, sli[s], bud[s], F["ran_over"][s], mins[s][0], mins[s][1]))
    L += ["", "## Critical Components", "",
          "1. The service whose SLI counts the most over-threshold requests, and so starts first, is "
          "**%s**; payments' December SLI is **%s%%**, within its %s%%." % (order[0], sli[pay], bud[pay]),
          "2. %s." % names(["**%s** was **%s** own failure" % (mis[0]["id"], poss(mis[0]["cause"]))] +
                           ["**%s** **%s**" % (x["id"], poss(x["cause"])) for x in mis[1:]]),
          "3. Places' December SLI is **%s%%** (%s to %s accepted) and booking's **%s%%**." % (
              sli[pl], band[pl][0], band[pl][1], sli[bk]),
          "", "## Step-by-Step", ""]
    steps = [
        "Kept the server spans in %s once each (a re-sent span id counted once) and linked each to its trace's root, "
        "the server span with no parent; mapped tracing names and target groups through %s; read thresholds and "
        "budgets from section 4 of %s." % (K.FILES["spans"], K.FILES["catalogue"], K.FILES["slo"]),
        "Reconciled %s, %s and %s: a customer-facing incident ends when the status page shows its last component "
        "operational, a service counts from when the timeline adds it, and the halves split at 1 July 00:00 Lisbon "
        "time; that gives the incident minutes of the CSV and the windows the standard's incident clause leaves "
        "out." % (K.FILES["incidents"], K.FILES["timeline"], K.FILES["status"]),
        "The reasonable route that falls short: each service's own spans reweighted on its own hourly RequestCount "
        "from %s over the hours the export holds, with each December incident put on the named service furthest over "
        "its load curve across the incident, gives %s as the services over budget (partner-gateway %s%%, "
        "journey-search %s%%)." % (K.FILES["lb_h2"], names(F["careful_over"]), F["careful_sli"][pg],
                                   F["careful_sli"][js]),
        "The traces overturn the weighting: the store kept a near-fixed number of whole traces an hour per edge "
        "service, so an internal service's kept spans carry its callers' keep shares. Counted each kept span at its "
        "trace root's hourly keep share (the root's RequestCount over the roots kept that hour): partner-gateway's "
        "slow calls come in through busy, thinly kept journey-search and weigh far more than its own count gives "
        "them, while payments' slow calls come through quiet, thickly kept booking and weigh less (%s%% on its own "
        "count, %s%% at the roots' shares)." % (own[pay], sli[pay]),
        "The export overturns the period: its first span starts at %s, so the first %s hours of December, %s%% of "
        "the month's edge requests, have no spans, and the standard counts a request whether or not a span was kept. "
        "%s holds those hours: the hourly duration histogram of every span the store ingested, by service and span "
        "name, the same spans as the export wherever the two overlap. For each server series in those hours, "
        "counted the spans over the service's threshold and weighted them like the spans themselves (an internal "
        "operation by the keep shares of the edge services whose client spans called it that hour). For %s the "
        "threshold is a histogram boundary and nothing is estimated." % (
            F["held_from"], F["gone_hours"], F["gone_pct"], K.FILES["spanmetrics"], names(F["exact"])),
        "For %s the threshold sits inside a bucket, and the bucket was split at the share of its spans over the "
        "threshold that the service's held, incident-free spans show in the same band of hourly load (five bands). "
        "Straight-line interpolation inside the bucket is the shortcut that fails: on the hours the export holds it "
        "rebuilds %s times the over-threshold requests the spans themselves show for places and %s times for "
        "journey-search, and would put places at %s%% and fares at %s%%. With the hours counted, journey-search falls "
        "from %s%% on the export's hours to %s%% and places from %s%% to %s%%." % (
            names(F["bridged"]), F["linear_check"][pl], F["linear_check"][js], F["linear_sli"][pl],
            F["linear_sli"][fa], exp[js], sli[js], exp[pl], sli[pl]),
        "Dated each December incident's cause: for every service it named, the own handling time of each span (less "
        "the calls it waited on) against a load curve fitted on the export's incident-free hours, a changepoint on "
        "the residuals; the earliest sustained rise owns the cause. Over the whole incident %s ran furthest above "
        "their curves, but each rose only after the service it calls had: %s own them." % (
            names(["%s in %s" % (x["careful_cause"], x["id"]) for x in mis]), names([x["cause"] for x in mis])),
        "Left each named service's requests out from when the timeline added it to the incident's end unless it "
        "owned the cause, and compared each SLI with its budget: %s ran over." % names(over),
        "Took each over-budget SLI's %s per cent interval by linearisation over strata of root service and hour with "
        "the kept traces as units, the hours read from the span metrics adding their own sampling error and the "
        "error of each bucket's split; a trace bootstrap with the splits refitted agrees within %s." % (
            F["interval_level_pct"], F["ci_room"]),
        "Each service's weighted spans over its threshold are the requests its SLI counts: the engineers start with "
        "%s (%s%%), and the %s served %s more than their budgets allow." % (
            order[0], share[order[0]], n_over, F["beyond_budget"]),
    ]
    L += ["%d. %s" % (i, s) for i, s in enumerate(steps, 1)]
    L += ["", "No other conclusion survives, and the three judgments are independent. Leave out the trace roots' "
          "weights alone and the list is %s (partner-gateway %s%%, fares %s%%, notifications %s%%). Leave out the "
          "dated causes alone and it is %s (fares %s%%, notifications %s%%, journey-search %s%%). Leave out the hours "
          "before the export alone and it is the %s with journey-search (%s%%). Leave out the weights and the dated "
          "causes and it is %s; the weights and the early hours, %s; the dated causes and the early hours, %s. Every "
          "split of a threshold's bucket the held spans support (one pooled share, two to thirty load bands, a logit "
          "in load, the hour of day) gives the same %s, the same order and SLIs inside the ranges above; so do "
          "interpolation inside the bucket and the bucket's two bounds for the list, though not for the figures. A "
          "fill that reads no span metrics and gives the early hours the export's own share puts partner-gateway at "
          "%s%%, where the span metrics, whose %s ms boundary is its threshold, count %s%% with nothing estimated. The "
          "thinnest margin is in the start order: %s counts %s per cent more over-threshold requests than %s, and "
          "holds that place under every split." % (
              names(F["own_over"]), own[pg], own[fa], own[no],
              names(F["window_over"]), win[fa], win[no], win[js],
              n_over, exp[js],
              names(F["own_window_over"]), names(F["own_export_over"]), names(F["window_export_over"]),
              n_over, F["flat_sli"][pg], F["span_metrics_bounds"], sli[pg],
              F["order_last_two"][0], F["order_last_gap_pct"], F["order_last_two"][1]), ""]
    return "\n".join(L), F
