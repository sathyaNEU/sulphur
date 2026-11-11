# task13: the co-op's 2027 lightning protection refit and the referral rule behind it

## Draw

Subdomain: Energy Systems & Utilities, task type grid reliability and outage analysis (`grid-reliability-outage-analysis`, the only energy task type serving the assigned analysis type)
Analysis type: Anomaly Detection & Diagnostics
Answer shape: a monitoring rule with its expected alert count (the rule, the zones it refers now, its false referrals a season and its referrals after each season since 2022, checked against the cyclic inspections), with the refit on top
Weight: metric or rule design: most of the work is building the referral signal itself (lightning faults reconstructed on each device's own clock and memory, an expectation learned only from inspection-confirmed sound seasons, a threshold carried on their spread); the last three builds sat on assembly (task14), a hard-to-measure quantity (task3) and validation (task10)
Data-native sentence: a lightning fault exists only as a coincidence between two clocks (a recloser's own record of a trip and a lightning network's record of a stroke near the line), and the reclosers with no radio link keep their own drifting time and only their last 64 or 100 events between site visits, so the zones whose protection has failed, which trip most, are the zones whose records lose the most and line up the worst; what a sound zone should do is visible only in seasons a later cyclic inspection confirmed sound.
People: Lucas Ramirez (technical services manager, takes the refit to the management committee), Donna Rodriguez (reliability and protection engineer, the golden's author), Laurie Diaz (line inspection supervisor), Elizabeth Hernandez (general manager, issues the programme terms), John Fuentes (SCADA supervisor), Michelle Garcia (materials and warehouse); drawn with `guard.py names --geo Philippines` at seeds 1302, 1307 and 1311

**The decision.** Kalumpang Valley Electric Cooperative, a member-owned distribution co-op in Central Luzon, runs 13.2 kV
overhead lines from twelve substations, cut into protection zones by substation breakers and line reclosers. Lightning
is its largest cause of trips. Its 2017-2018 line arrester programme fitted arresters along the exposed lines; since
then ground leads have been stolen for their copper, a contract lot of line arresters has started failing and a batch
of porcelain pin insulators has been cracking. A cyclic line inspection reaches every zone once in five dry seasons. The
board's 2027 budget funds a dry-season refit (grounds, arresters and insulators restored) on the zones a referral rule
names before the 2027 lightning season, and the co-op will run the same rule after every season from now on.

**Card.** `.claude/skills/fingerprint/cards/task13.json`, architecture v2, registered 2026-11-11, guard verdict WARN.
Answered: `overuse.forum` (the management committee approves the dry-season work programme inside the board's budget,
the honest forum for a refit list); `repeat.gate_g` against task15 (there a growth gap split across drivers; here each
zone's faults assigned to lightning on its device's own clock and its excess to failed protection rather than to the
spread sound zones show); `repeat.question_form` (the decision is a rule, so the question asks what it is). Redrawn after
syncing with origin/main, when task14 v3, task15 v2 and task16 v2 entered the window: forum, decisive pattern (G7, the
operating window a recloser's record holds) and Gate G (card `notes`). The v1 card's identity moved into `lineage`.

## Tried and rejected

- A smart-meter outage-alert rollout recording small outages that customer calls missed, as the decisive layer:
  rejected at the draw, 2026-11-09. Which comparison is clean (recorded against experienced) is the estimand, so
  filing it spends the layer and leaving it open is a fork (`determinism-check` section 1).
- A random scratch world (feeder size and tree density drawn freely): the three-year count and the wind-normalised
  rate alone reproduced four to six of the golden six on five seeds, because size dominated; the world is built from
  groups (overdue northern feeders, dense plantation feeders trimmed recently, southern late-cycle feeders, overdue
  feeders with few trees) so each shortcut lands on a different wrong list.
- A one-year wind anomaly carried by the station's mean level: the decomposition fitted without the wind still landed
  four to five of the six, because one year is a small share of the outage record and a higher mean moves every gust
  alike; replaced by three years in which the storm track sat south (fewer strong-wind days in the north, about twice
  as many in the south, mean wind within 6 per cent) over an outage record from April 2022.
- Plantation feeders trimmed early in 2025 on a four-year cycle: their growth left them among the golden six; moved to
  a three-year cycle cut in the second half of 2025, which keeps them first on every recent count and on expected
  interruptions and last on the growth a catch-up removes.
- Major event days set by the 2.5-beta rule on the record: wind-storm days crossed the boundary and carried a fifth of
  the strong-wind hours, so the projection's treatment of those days moved the six's total by half; the filed
  boundary values now sit above every storm day, and the major event days are the five snow days.
- Hours of gusts of 60 km/h or more as the golden's exposure: 30 feeder-months with vegetation interruptions had no
  exposure at all, and the six's total moved 28 per cent across thresholds; the gust load, which fits the record best, is
  the golden, and the hour counts stay in the family (same six).
- Architecture 1 as a whole (Kotuku Networks' 2027 vegetation catch-up, READY 2026-11-09, never run on the platform):
  re-rooted 2026-11-11 at the author's word, for a stronger chain with at least three independent analytical failure
  points. Cut under the retired single-deep-step design: one Poisson fit carried every graded figure, the plantation
  feeders' dense corridor sat only in the deciding units with one filter as its fix, and the storm-track swing showed
  in one plot of gust hours by station.
- Architecture 2 at the prototype, a referral on the latest season alone: with about eight sound faults a zone-season
  the failed zones (2.2 to 3 times their sound rate) were referred at p near the threshold; the window became the
  seasons since the zone's last cyclic inspection, as the programme terms file it.
- Architecture 2 at the prototype, the sound expectation fitted on the season after each inspection only: 172
  zone-seasons of about eight faults could not show the sound zones' spread (the moment estimate of the negative
  binomial size ran to infinity) and the referral set swung from 0 to 10 zones with the dispersion; the expectation and
  its spread are fitted on every season a later cyclic inspection confirmed sound (410 zone-seasons, size near 25).
- Architecture 2 at the prototype, line arresters with no effect on direct strikes: losing them lifted a zone's
  lightning faults about 1.9 times, inside the scatter of sound zones around any design model; arresters every few
  spans now also drain part of a direct strike's current, so a zone that loses its ground leads or arresters runs 2.5
  to 4.5 times its sound rate, as the field's line arrester studies show.
