# task22: where Delmont Power and Light's 2027 revenue protection sweep goes, and what its lines and transformers will lose in 2027

Architecture 1, drawn 2026-11-12, the first draw after the client's closed strategies page
(`guidelines/client/learning-modules/overused-strategies-2026-11-12.md`): every lesson in the chain is off it.

## Draw

Subdomain: Energy Systems & Utilities, distribution losses and the feeder energy balance (house task type
  distribution-losses-energy-balance; the client's nearest task types are load forecasting and grid reliability)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a bridge that reconciles two totals: each feeder's energy in, month by month from November 2023 to
  October 2026, carried to what its customers' meters recorded, the city's unmetered lights and own use, the lines'
  and transformers' losses and what is left (the non-technical loss), with the utility's line loss rise between the
  twelve months to October 2024 and the twelve months to October 2026 bridged to its causes; the four feeders the
  2027 sweep covers sit on top
Weight: assembly: one energy balance for fourteen feeders built from systems that count different things on
  different clocks (the wholesale delivery point meters by substation and hour, the feeder breakers' telemetry by
  feeder and hour with its gaps, customer reads on twenty billing cycles and at month ends, today's GIS against a
  switching log in two naming schemes, deemed lights, the transformer register), where the technical term is
  itself a network computation; the last two live builds weigh modeling (task7 v10) and validation (task20 v2)
Data-native sentence: nothing meters a feeder's theft or its own losses, so each is what is left of a balance whose
  terms come from systems that each see part of it: the breaker telemetry sees the feeder but goes dark in the
  storms when crews are moving customers between feeders, the delivery point meters see every hour but only by
  substation, the GIS knows where every load sits today but not who was on which feeder last winter, and the 2019
  loss study knows the network's losses at 2019's loads, before the licensed grows and the cold store connected at
  the far ends of the longest feeders.
People: drawn with `guard.py names --geo us --seed 2207`: Dustin Jones (the utility's engineering manager, who asks;
  not named in the prompt), Heidi Hester (the consulting engineer who wrote the 2019 loss evaluation study).
Decision: before the City of Delmont's 2027 utility budget closes, the engineering manager names the four of the
  fourteen feeders the revenue protection contractor sweeps in 2027 (the contract funds four), ranked by the
  non-technical loss each carried in the twelve months to October 2026 (the last month whose meter reads are all
  in), and the technical losses the 2027 power cost budget carries; forward-facing (the sweep and the losses are
  2027's).

Card: `.claude/skills/fingerprint/cards/task22.json`, architecture v1, registered 2026-11-12T14:48:55Z at WARN.
Redrawn at filing: the forum (board of directors, then executive team, to the line manager: the sweep is the
engineering manager's call inside the budget the council passes), the organisation family (a cooperative and a
utility both repeat task7 v10 and task13 v4 in the window; the city-owned utility is a local government department,
which is what public power is) and the question form (which, the last prompt's form, to where: the sweep is a place
on the network). The two WARNs are answered here: line_manager_or_team decides in seven builds, the honest forum for
an operational sweep; a spreadsheet and a Word memo repeat task20 and task7's deliverable set, and a memo to the
utility director is a Word document.

## Tried and rejected

- 2026-11-12, at filing: a rural electric cooperative as the organisation (Ketchum Prairie Electric Cooperative):
  both its honest organisation families repeat the last three builds (task7 v10 a cooperative, task13 v4 a utility),
  so the same balance moved to a city-owned utility, where theft, far-end grows and deemed lights are as common.
