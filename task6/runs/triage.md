# task6 architecture 6, platform round 1: triage

Recorded 2026-11-08 in the /fix-rubric session from the scores the author reported and the generated rubric
(runs/rubric.csv, 30 criteria, 100 points). The author named the route; no run-triage agent was spawned.

## Scores

| Run | Score | Call | Criteria lost | Points lost |
|---|---|---|---|---|
| run 1 (runs/run1.md) | 73 | off: four services, partner-gateway 1.4 against 2.0 | 1 recommendation (18), 2 partner-gateway SLI 2.8 to 3.0 (7), 21 the five flagged as over in the CSV (2) | 27 |
| run 2 (runs/run2.md) | 83 | on: five services, partner-gateway 2.9 | 5 to 9 incident minutes for partner-gateway, places, booking, notifications and fares (4, 4, 3, 3, 3) | 17 |

Average 78.0. Counterfactual average 86.5: run 2's incident loss is a misread of PR-SLO-3 5.2 ("named it at the
time"), a surface class, given back.

## First wrong step

- **Run 1: method shortcut.** It post-stratified each service's own kept server spans by hour on that service's
  load balancer count (its step 3), the default path's rung 3, and filed partner-gateway at 1.4 against 2.0. Every
  hygiene item was handled and every filed sentence read; its own checks (hourly counts rebuilt) passed. Analytical.
- **Run 2: lands the call.** It weighted each root-service hour and propagated the weight to the trace's spans,
  filing 2.9. Its one loss is on the incident ask: it read the export's final named-service lists from the
  declaration ("used final named-service lists retrospectively"), which section 5.2 rules out; every incident cell
  moved (places 794 and 222 against 755 and 109).

## Where the points went

Run 1, off the call, kept every ask: releases and rollbacks (rubric 10 to 13, 12 points), cloud cost by half (14 to
18, 19 points) and incident minutes (5 to 9, 17 points), plus the critical components that list the edge and
single-caller services' SLIs and budgets (3, 4, 19, 20, 16 points), which the default path reproduces exactly, and
the nine instruction rows. None of those figures reads the deep step.

## Route

**FIX_ASKS** (one run off the call, the average 60 or more from asks the off-call run collected): `/fix-rubric task6`,
done 2026-11-08. The asks were re-sited onto the SLI's own numerator (the engineers' start order, each named
service's share of all the services' over-threshold December requests, the share the five served together, the
requests beyond their budgets) and the incident minutes onto the union over the services the call names; releases,
rollbacks and cost were dropped; critical components 2 and 3 were replaced by links of the chain. Paper estimate on
the same 38, 7 and 55 split: 54.0 to 58.0 (generator/ceiling.py), against 78.0 measured on the old layer. The
DESIGN_NOTE's ask sheet and `## Tried and rejected` carry the detail. New platform runs, then `/triage-runs task6`.
