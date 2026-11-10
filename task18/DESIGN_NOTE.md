# task18: how much fast frequency response Corvenna's transmission operator must hold in 2027's lowest-inertia hours, after the 14 June 2026 under-frequency event

## Draw

Subdomain: Energy Systems & Utilities, grid reliability and outage analysis (`grid-reliability-outage-analysis`)
Analysis type: Root-Cause (what took the island's frequency below the first under-frequency load-shedding stage on
  14 June 2026, how much of the fall each cause accounts for, which response providers fell short), with the forward
  call the root cause sets: the fast frequency response a recurrence in 2027's lowest-inertia hours would need
Answer shape: ranked causes (each cause's share of the fall below 50 Hz, in the order the causes came, adding to the
  observed nadir), beside the providers that fell short and the 2027 holding with its range
Weight: investigation (reconstructing what the frequency fell against from records that each see part of it: the
  infeeds the operator meters, the embedded solar no meter records, the inertia no record states, each provider's
  delivery against a baseline no record gives); the last three builds sit on modeling (task10), allocation (task9) and
  a hard-to-measure quantity (task2)
Data-native sentence: an island grid's frequency falls against everything that left it and everything that held it,
  but the operator meters only its own transmission connections, so the embedded solar its loss-of-mains protection
  tripped, the inertia of the demand's own motors and the response providers would have given anyway all have to be
  recovered from where they show (the grid supply points' flows, the first half-second of the fall at the system's
  centre of inertia, each provider's instructed trajectory), and a 2027 recurrence at lower inertia falls faster and
  trips a band of protection that held in 2026
People: Orlaith Ganley (director of system security, Corvenna Utilities Regulation Authority) and Kieran Rabbitte
  (head of system operability, Corvenna Transmission Operator), from `guard.py names --geo Ireland --seed 18`; neither
  is named in the prompt
Card: `.claude/skills/fingerprint/cards/task18.json`, registered 2026-11-10 at WARN. WARN answered:
  `repeat.question_form` how-much against task2 (the decision is a quantity of fast response, so "how much" is its
  form). Differentiated against mark126 and task8 on the structural tests (their drivers split record-linked units and
  carry parameters calibrated on another population; here an unmetered physical loss and the inertia are measured from
  the event itself and carried through a swing model). org_family government_agency and role compliance_or_audit
  because the investigation and the 2027 direction are the regulator's.

## Results chain (sketch at the draw; the full table at stage 2)

- R1 the reconciled sequence of losses (assembly and reconciliation): each recorder's clock set on the fault every
  recorder saw; the hurried pass is right here (a reflex the runs make).
- R2 the embedded solar lost, by mechanism, vector shift at the fault and rate of change of frequency in the fall
  (missingness and measurement): from each grid supply point's flow step net of load relief and the voltage-dependent
  dip; hurried: minute averages around the event (LFDD and load relief inside them) or the register's old-setting
  capacity at its output (every unit taken as tripped).
- R3 the inertia when the event began (modeling): the centre-of-inertia rate of change in the first half-second with
  the embedded loss in the step; hurried: the unit register's sum (the demand's motors left out), one PMU's rate, or
  the wind farm's megawatts alone as the step.
- R4 each response provider's delivery against its contract and the providers short (exploration and triage at
  breadth): against each provider's instructed trajectory and its contract's frequency curve; hurried: flat pre-event
  baselines and contracted megawatts at face value.
- R5 the fall below 50 Hz split by cause in the order the causes came (decomposition and attribution): a swing model
  calibrated on the event; hurried: megawatt shares of the losses.
- R6 the net and gross demand the first under-frequency stage removed against its design (missingness and
  measurement): feeders exporting solar at the moment they were shed; hurried: the feeders' recorded flows taken as the
  demand removed.
- R7 the 2027 fast-response holding for a recurrence at the lowest inertia (forecasting): the same sequence at 2027's
  lowest inertia, the embedded loss carried by protection band after the loss-of-mains programme's conversions (the
  steeper fall trips the 0.5 Hz/s band that held in 2026), providers at their measured delivery; hurried: the 2026
  shortfall scaled linearly.

## Tried and rejected

- A utility-scale solar fleet's 2026 shortfall bridged to its causes (sensor soiling masking module soiling, a drought
  year biasing the year-on-year degradation, tracker faults found by profile shape), set aside at the draw on
  2026-11-10: it follows the client's own strategies 4 and 5 for this domain group (the wind-farm bridge and the solar
  fleet diagnosis) step for step, and "a lesson can come back, a structure cannot".
- A wind farm's expected-to-actual bridge, set aside the same day: the depth scale's level-4 example is a wind farm's
  wake recovery, and the client's strategy 4 is this bridge.
- A distribution network's reliability bridge (customer minutes lost by cause, weather-normalised), set aside the same
  day: task13 holds the same subdomain with the same files (outage records, feeders, storm exposure).
- A distribution transformer fleet's failure rise (loading rebuilt from smart meters with the connectivity corrected
  by voltage correlation, reverse power flow from rooftop solar, thermal ageing, left-truncated failure records), kept
  for a later draw: the smart-meter volumes it needs would not fit a pack.
