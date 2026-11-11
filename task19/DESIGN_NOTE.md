# task19: Kilvarra's mid-2026 district populations for the 2027/28 grant determination

## Draw

Subdomain: Survey Research & Official Statistics, nonresponse, calibration and measurement-error adjustment
(coverage measurement of an administrative register)
Analysis type: Descriptive & Distribution Analysis (where each district's total really sits once the register's
erroneous entries and the people it misses are measured)
Answer shape: a reconciled table plus findings (twelve district estimates with intervals, the call against the line,
each register count bridged to its estimate, the national rolled-forward figure bridged to the estimate)
Weight: an estimate of a quantity that is hard to measure (usual residents where no census has run since 2021); the
last two live builds weighed validation (task9) and metric or rule design (task13)
Data-native sentence: the only list of residents is a health register that keeps people who have left, lists students
and movers where they used to live and never held some young men at all, and the coverage survey that measures it
shares no key with it and misses the same young men.
People: Grainne Grennan, Carla McCaffrey (guard.py names --geo Ireland --seed 19)

The chain, sketched at the draw (written in full at stage 2):

- R1 the share of usual residents held on their own district's list, by nationality, net of the linkage's missed and
  false links (assembly and reconciliation)
- R2 the register's erroneous entries by district from the follow-up, unresolved records imputed (missingness and
  measurement)
- R3 the residents each district's list misses because they are listed in another district (assembly and
  reconciliation)
- R4 the dependence factor for men aged 18 to 44 from the sex-ratio benchmark (modeling)
- R5 the twelve district estimates and the national total (modeling)
- R6 their 90 per cent intervals with the shared estimation errors carried (uncertainty)
- R7 the districts that qualify, the ones too close to call and each close one's probability (synthesis)
- R8 each district's register count bridged to its estimate (decomposition and attribution)
- R9 the national rolled-forward estimate bridged to the estimate, unrecorded emigration sized from the border and
  follow-up records (investigation)

One-fact test at the draw: the sex-ratio sentence rescues R4 alone (the missed links still lift every estimate); the
missed-links sentence R1 alone (the dependence still pulls the estimates down); the shared-errors sentence R6 alone;
the common-emigration sentence R9's emigration part alone. One of nine at most.

## Tried and rejected

- 2026-11-11, the concept note's district-level official estimates: a shipped series that puts Carnmoyle over the
  line ranks the candidates on the decision question (Gate G); only the national series and its components ship.
- 2026-11-11, the concept note's residency classifier trained on the 2021 census link as a graded result: with the
  follow-up's 2026 outcomes in hand the design-based rate needs no model, so the trap reached only runs that chose to
  model; the link ships as an unused file and its route is recorded, never graded.
- 2026-11-11, register over-coverage by a signs-of-life rule (the concept's crude activity filter): every activity
  window is a threshold a judge reads as a fork (task8's architecture 12 screen); over-coverage comes from the field
  follow-up's outcomes instead.
- 2026-11-11, the concept's NewTown two people under the line: a call that close is returned on forcing (task1 arch
  2 and 3, task4 arch 7 and 10); the near-line districts are set so the honest interval decides each one with margin.
