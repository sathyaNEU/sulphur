# task13 design note: Kotuku Networks' 2027 vegetation catch-up

## Draw

**Card.** `.claude/skills/fingerprint/cards/task13.json`, architecture v1, registered 2026-11-09, guard verdict WARN
(no BLOCK). Domain Energy Systems & Utilities (`energy-systems-utilities`), task type grid reliability and outage
analysis (`grid-reliability-outage-analysis`), the one energy task type never drawn; objective Anomaly Detection &
Diagnostics, which that task type serves. Shape 01: a ranked list of feeders under a cap.

**The decision.** Kotuku Networks, a consumer-trust-owned lines company in the lower North Island, runs 48 11 kV
feeders off its zone substations across a northern coast, river plains and southern hill country with plantation
forest. Its 2027 vegetation catch-up trims six feeders' line corridors back to the condition straight after a cycle
trim, before the winter storms, and goes into the asset management plan it discloses before 1 April 2027. The
programme's terms file what it is judged on: the sustained customer interruptions it avoids in the 2027-28 regulatory
year (1 April 2027 to 31 March 2028) on days that are not major event days.

**Data-native sentence.** A tree contact on an overhead line happens when wind moves a branch onto a conductor, so a
feeder's tree-caused interruptions are its corridor's growth since the last trim times the gusts its weather station
saw; a year that was calm in one district and the windiest on record in another moves every feeder's count by its
district's wind before its corridor shows at all, and a corridor that was dense to start with keeps most of its
count after any trim.

**The two analytical judgments that decide the call** (each alone leaves the wrong six):
1. *Exposure: the 2026 counts carry the year's wind.* 2026 was calm on the northern coast and the windiest year in the
   record in the southern hill country, so each feeder's tree-caused interruptions have to be read per unit of the
   gust exposure at its own station (hours with gusts at or above the level that brings branches down), not per year.
2. *Decomposition: a catch-up removes only the growth since the last trim.* A feeder's rate per gust-hour is its
   corridor's base, which a just-trimmed corridor keeps, times the growth since its last cycle trim. The plantation
   feeders trimmed in 2024 and 2025 carry the highest rates per gust-hour and have little growth left to remove; the
   northern coastal feeders left longest untrimmed carry ordinary-looking counts and the most growth.

**Strategy label.** WORKS IN FORM (`stumping/references/sulfur-strategies.md`, Part A): separating two explanations
for one pattern (weather against condition) with a comparison that is actually clean (per unit of exposure), and
selection on a noisy outcome (the worst-looking feeders were picked on a windy year and on a base the remedy cannot
touch) in the live form where the decision's own effect, not the observed level, is what ranks.

**Guard WARN answered.** `repeat.gate_g` (decomposition_attribution, also task2's): the Gate G mechanism here is
honestly the assignment of a correctly recorded rise to its driver (wind against corridor growth); task2's is a
release's error rate against a clinician mix, a different world, shell and shape.

**People** (drawn with `guard.py names --geo "New Zealand" --seed 1301`): Tania Foley, network general manager;
Wayne Ward, vegetation manager (owner of the cycle log); Hoani Marshall, reliability engineer (the golden's author);
Kathryn Carter, regulatory manager (owner of the reliability reporting standard); Sean Chapman, the vegetation
contractor's supervisor; Maria Hodson, customer service lead.

**Sources** (all constructed by `generator/`; provenance in `metadata.json`): the outage management system's
interruption records 2022 to 2026; the met service's hourly station observations for four stations; the feeder
register; the vegetation cycle log; the reliability reporting standard (major event days); the 2027 catch-up's
programme terms (the WHAT); customer counts by feeder; and, unlabelled, two distractors.

## Tried and rejected

- A smart-meter outage-alert rollout recording small outages that customer calls missed, as the decisive layer:
  rejected at the draw, 2026-11-09. Which comparison is clean (recorded against experienced) is the estimand, so
  filing it spends the layer and leaving it open is a fork (`determinism-check` section 1).
- A random scratch world (feeder size and tree density drawn freely): the three-year count and the wind-normalised
  rate alone reproduced four to six of the golden six on five seeds, because size dominated; the world is built from
  groups (overdue northern feeders, dense plantation feeders trimmed recently, windy mid-cycle southern feeders,
  overdue feeders with few trees) so each shortcut lands on a different wrong list.
