"""task6's submission.md, drafted from the figure set deliver.figures builds: every number is emitted, never
typed. The blocks run in the platform's order: Final Recommendation, Supplementary Questions, Critical Components,
Step-by-Step."""
import common as K
from deliver import names, handling


def poss(s):
    return s + ("'" if s.endswith("s") else "'s")


def write(R, F):
    over, order = F["over"], F["start_order"]
    sli, bud, share, ci, mins = F["sli"], F["budget"], F["share_pct"], F["ci"], F["minutes"]
    csl, rsl = F["owncount_sli"], F["rootcareful_sli"]
    n_over = "five" if len(over) == 5 else str(len(over))
    dec = [x for x in F["incidents"] if x["id"] in F["deciding"]]      # the misreadings that move a verdict
    mis = [x for x in F["incidents"] if x["id"] in F["misread"]]       # every incident the whole-window reading misreads
    pg, fa, no = "partner-gateway", "fares", "notifications"
    falls = [rsl[x["cause"]] for x in dec]
    fall = ("%s%% each" % falls[0]) if len(set(falls)) == 1 else names(["%s%%" % v for v in falls])
    days = names([x["declared"].split(" ")[0] for x in dec]) + " December"
    L = ["## Tags", "",
         "**Domain:** General Statistics & Data Science (missing data, censoring and measurement error).",
         "**Analytical objective:** Descriptive & Distribution Analysis.", "",
         "## Final Recommendation", "",
         "**Put reliability engineers on %s, in that order: the %s ran over their 2026 latency error budgets.** "
         "Not %s alone, which each service's own spans reweighted on its own hourly count give even with every "
         "incident's cause dated right (fares %s%%, "
         "partner-gateway %s%%, notifications %s%%), and not without %s, which fall to %s when %s are put on %s, the "
         "services furthest over their load curves, rather than on %s, whose own handling slowed first."
         % (names(order), n_over, names(F["owncount_over"]), csl[fa], csl[pg], csl[no], names([x["cause"] for x in dec]),
            fall, names([x["id"] for x in dec]), names([x["careful_cause"] for x in dec]),
            names([x["cause"] for x in dec])),
         "", "## Supplementary Questions", "",
         "### %s" % K.DOCX_OUT, "",
         "1. Names the services that ran over in the order their engineers start, the one whose SLI counts the most "
         "requests over its threshold first, each with its share of the over-threshold requests all our services' SLIs "
         "count (whole per cent) and a 90 per cent confidence interval on its SLI (per cent to two decimals): %s."
         % "; ".join("%s %s%%, interval %s to %s" % (s, share[s], ci[s][0], ci[s][1]) for s in order),
         "2. A table of every service's December 2026 latency SLI beside its error budget, per cent to one decimal:"]
    for s in K.SVC:
        L.append("   - %s: SLI %s against a budget of %s, %s" % (s, sli[s], bud[s],
                                                               "over" if F["ran_over"][s] == "yes" else "within"))
    L += ["3. A bar chart of each service's SLI against its own budget line, the services over budget in red.",
          "4. The service that owned the root cause of each customer-facing incident in December:"]
    for x in F["incidents"]:
        L.append("   - %s, declared %s, naming %s: %s" % (x["id"], x["declared"], ", ".join(x["named"]), x["cause"]))
    L += ["5. The %s served %s%% of the over-threshold requests all our services' SLIs count, and %s more than their "
          "budgets allow, to the nearest ten thousand." % (n_over, F["together_pct"], F["beyond_budget"]),
          "", "### %s" % K.CSV_OUT, "",
          "1. A row per service, columns service, latency_sli_pct, error_budget_pct, ran_over, incident_minutes_h1 and "
          "incident_minutes_h2; SLI and budget per cent to one decimal, minutes whole, each service counted from when "
          "the incident tool added it:"]
    for s in K.SVC:
        L.append("   - %s: SLI %s, budget %s, ran over %s, incident minutes %s and %s" % (
            s, sli[s], bud[s], F["ran_over"][s], mins[s][0], mins[s][1]))
    L += ["", "## Critical Components", "",
          "1. %s: %s rose above their load curves **first**, and %s only after them, though those ran further over "
          "their curves across each incident." % (
              names(["**%s** was **%s** own failure" % (dec[0]["id"], poss(dec[0]["cause"]))] +
                    ["**%s** **%s**" % (x["id"], poss(x["cause"])) for x in dec[1:]]),
              names([handling(x["cause"]) for x in dec]), names([handling(x["careful_cause"]) for x in dec])),
          "2. With each kept span counted at its trace root's hourly keep share, partner-gateway's December SLI is "
          "**%s%%** against **%s%%**, fares' **%s%%** against **%s%%** and notifications' **%s%%** against **%s%%**; "
          "on each service's own hourly count, with the same incident time left out, they are %s%%, %s%% and %s%%." % (
              sli[pg], bud[pg], sli[fa], bud[fa], sli[no], bud[no], csl[pg], csl[fa], csl[no]),
          "3. Partner-gateway's 90 per cent interval runs **%s%% to %s%%**, the traces taken as whole units within "
          "each root service's hour." % tuple(ci[pg]),
          "4. The %s served **%s%%** of the over-threshold requests the SLIs count, **%s** more than their budgets "
          "allow." % (n_over, F["together_pct"], F["beyond_budget"]),
          "", "## Step-by-Step", ""]
    steps = [
        "Kept the server spans in %s once each (a re-sent span id counted once) and linked each to its trace's root, "
        "the server span with no parent; counted the roots each edge "
        "service kept in each hour against its RequestCount in %s (target groups through %s)." % (
            K.FILES["spans"], K.FILES["lb_h2"], K.FILES["catalogue"]),
        "Reconciled %s, %s and %s: each customer-facing incident ends when the status page shows its last component "
        "operational, a service counts from when the timeline adds it, halves split at 1 July 00:00 Lisbon time; "
        "partner-gateway %s and %s minutes, notifications %s and %s." % (
            K.FILES["incidents"], K.FILES["timeline"], K.FILES["status"], mins[pg][0], mins[pg][1], mins[no][0],
            mins[no][1]),
        "The reasonable route that falls short: each service's own spans reweighted on its own hourly count, with "
        "each incident's cause dated as in step 5, puts fares at %s%%, partner-gateway at %s%% and notifications at "
        "%s%%, so only %s ran over." % (csl[fa], csl[pg], csl[no], names(F["owncount_over"])),
        "The traces overturn it: the store kept a near-fixed number of whole traces an hour per edge service, so an "
        "internal service's kept spans carry its callers' keep shares; counted at its trace root's share (the root's "
        "RequestCount over the roots kept that hour), each internal service's slow operations, called from busy and "
        "thinly kept journey-search and accounts, weigh what they served.",
        "Dated each December incident's cause: for every service it named, the own handling time of each span "
        "(less the calls it waited on) against a load curve fitted on December's incident-free hours, a changepoint "
        "on the residuals; the earliest sustained rise owns the cause. Over the whole incident %s ran furthest above "
        "their curves, but each rose only after the service it calls had, by twenty minutes or more: %s own them." % (
            names(["%s in %s" % (x["careful_cause"], x["id"]) for x in mis]), names([x["cause"] for x in mis])),
        "Left each named service's requests out from when the timeline added it to the incident's end unless it "
        "owned the cause (PR-SLO-3's incident and root-cause clauses): %s ran over." % names(over),
        "Took each over-budget SLI's 90 per cent interval by linearisation over strata of root service and hour with "
        "the kept traces as units: partner-gateway %s%% to %s%%." % tuple(ci[pg]),
        "Each service's weighted spans over its threshold are the requests its SLI counts: the engineers start with "
        "%s (%s%%), the %s served %s%% together and %s more than their budgets allow." % (
            order[0], share[order[0]], n_over, F["together_pct"], F["beyond_budget"]),
    ]
    L += ["%d. %s" % (i, s) for i, s in enumerate(steps, 1)]
    L += ["", "No other conclusion survives. Weighting each span by its own service's hourly count, or leaving the "
          "spans unweighted, keeps the slow operations of fares, partner-gateway and notifications at their callers' "
          "kept shares; putting each December incident on the service the responders named first or last, on the "
          "one with the most slow requests, or on the one furthest over its load curve across the whole incident, "
          "charges %s with %s own failures on %s. Every weighting the whole traces leave "
          "standing (the balancer's count or the weighted kept count as the base, the root's hour or the span's own) "
          "and every reasonable reading of the onset gives the same five, the same order and the same rounded "
          "figures." % (names([x["careful_cause"] for x in dec]), names([poss(x["cause"]) for x in dec]), days), ""]
    return "\n".join(L), F
