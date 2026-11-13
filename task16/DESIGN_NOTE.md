# task16: whether One Chart may link patient records automatically at Port Calder's April 2027 conversion, and under which rule

Architecture 3, drawn 2026-11-12, after architecture 2 was sent back at stage 4 (`## Tried and rejected`). Every lesson
in the chain is off the client's closed strategies page (`guidelines/client/learning-modules/overused-strategies-2026-11-12.md`).

## Draw

Subdomain: General Statistics & Data Science, data integration, record linkage and entity resolution (task type
  data-integration-record-linkage-entity-resolution)
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: a ranked list under a cap: the four candidate automatic linking rules ranked by the record pairs each
  joins at the conversion, each with its estimated false merges per 2,000 automatic links against the patient
  identity policy's cap of one, above the converted index reconciled to both legacy indexes (distinct patients,
  patients in both, records that hold two patients, duplicates left for review)
Weight: validation: most of the work is estimating, with no labelled set that covers them, the error rates of four
  record-linkage rules on two patient indexes, each rule failing for its own reason; the last two live builds weigh
  assembly (task22) and a hard-to-measure quantity (task1), and architecture 2 of this slot weighed assembly
Data-native sentence: a patient index holds what registrars typed at each visit and what an earlier merge rule did
  with it, so two records that agree on every field a rule compares may be two people (Port Calder's names are
  concentrated by community and by birth cohort, twins share a household, a family was registered under one
  subscriber's SSN), and two records of one patient may agree on little (a married name, a second surname dropped, a
  nickname, a new address); nothing in either index says which, and the only independent witnesses are the clinical
  events (blood groups, births, admissions) the rules never look at.
People: Brenda Hartman (director of health information management; signs the patient identity policy), Felicia Soto
  (the EMPI vendor's implementation consultant; the matching specification), Richard Wood (One Chart program
  director; the conversion plan), drawn with `guard.py names --geo us --seed 1603`; none is named in the prompt.
Decision: before the One Chart conversion on Monday 5 April 2027, the One Chart steering committee fixes whether the
  Halvard enterprise master patient index may join two patient records without HIM review, and under which of the
  conversion plan's four candidate rules: the patient identity policy caps automatic false merges at one per 2,000
  automatic links and takes the compliant rule that links the most; forward-facing (the conversion and its links are
  2027's).

The world. Port Calder is a fictional city on the Texas Gulf coast, about 60 per cent Hispanic, with a Vietnamese
community from the shrimping fleet. Calder Bay Health (three hospitals and clinics north of the ship channel) and
Rosario Medical Group (a hospital, a children's unit and clinics to the south) merged on 1 July 2025 as Calder Rosario
Health and convert to one electronic record, One Chart, on 5 April 2027. Each keeps its own patient index until then.
Calder Bay's registration software has merged a new registration into an existing record automatically whenever the
last name, birth date and sex match exactly since 4 March 2019; Rosario never merged automatically, and its HIM staff
merge what a monthly duplicate report shows. Until June 2021 Rosario's registration screen took the SSN from the
insurance card, which for a dependent is the subscriber's. Halvard Identity's engine scored a 2026 pilot of candidate
pairs; HIM reviewed the pairs in the engine's review band. Every extract is cut on Monday 2 November 2026; as-of date
for `leak.py`: 2026-11-04.

Card: `.claude/skills/fingerprint/cards/task16.json`, architecture v3, registered at WARN. Redrawn at filing: the
decisive generator (G16, method selection, first: the call picks a rule on its estimated error; G10 first put the
triple on task6 v5's lineage), the calibration organ (the clinical record the rules never use, physical verification;
the HIM pilot's reviewed pairs are the hurried route's check, and gold_standard_subsample is task7's in the window)
and the question form (whether, then which; task1 asked which). WARNs answered: identity_resolution
(strategy_risk) decides here on estimated error rates, never on one identifier read correctly; validation is the
honest weight (task20 v2 also carries it, outside the last two); executive_team (ten builds) is the honest forum for a
conversion steering committee of the system's executives; pick_one_of_n repeats task1 v4 because the conversion runs
one rule of four or none; inherited_attribute_from_other_unit (five live builds) and validation_cannot_see_condition
(three) are supporting steps beside a deciding lesson no task on file teaches.

## Tried and rejected

- A bridge between a projection and a disappointing large run (Comparative Analysis & Explanation, attribution): the
  honest strategy label is decomposition and attribution, which `ban.strategy` holds against task1 in the window; not
  relabelled, the draw moved to a forecast.
- Vendor labels as the only stump (the legacy-map route at 20 per cent error): on the real runs a pass that finds the
  expert-labelled development items and adds a per-route cost to a straight line still names the right configuration,
  so the pick turned on one thing (the yardstick).
- A contractor pool of 512,000 examples in the shortlist: the configuration on it wins by 0.07 under every sound
  forecast and under the straight line too, so nothing but the yardstick was priced.
- The dev split scored by route as separate logged scalars: a column would hand over the yardstick; the trainer logs
  one development loss and the per-item scores of each final checkpoint ship as the lab's error-analysis dump.
- A reference entry the proposal has to beat: the nearest configuration sat within 0.011 of any threshold that
  separated the shortlist, a margin the forecast cannot carry; the ranking is graded instead.
- A vendor label audit file (re-interpreted samples with agreement rates per route): with the routes' error rates on
  file a hurried pass avoids the map route by rule of thumb and wins the pick with no analysis; the routes' quality is
  left to what the runs show.
- The map route at 16 per cent error with a trial that mixed all three routes: the careful pass, calibrated to the run
  record (one scaling-law regression over every run, a floor or a quadratic chosen on held-back runs), named the right
  configuration and lost only the figures that hang on the bend, so the pick was earned by reflex and the pair priced
  near 70. Measured on the real runs at 10, 12, 14 and 16 per cent: at 12 the all-labels configuration truly scores
  0.660 against 0.6335, the pooled curve puts it first by 0.011, and every analysis that separates the level from the
  routes' costs names the right one by 0.012 to 0.039. The map route went to 12 per cent and the mixed trial out (the
  contractor's lot arrived in the pilot's last week).
- The pilot's largest runs left unfinished when the allocation ended, to be completed along the schedule: on a cosine
  schedule the logged loss at 70 to 90 per cent of a run is within 0.005 of its final value, so taking the last value
  as it stands is nearly right and the completion prices nothing.
- A compute cap that binds (a configuration that does not fit the slot): width buys under 0.006 a doubling at the
  expert pool, so no configuration that needs more hours is worth shortlisting; the hours stay texture (all four fit).
- A threshold on an extrapolated figure (lots 2 to 4 funded only if they lower the loss by a stated amount): the gap
  between the bent and the pooled forecast at one doubling past the pilot is 0.02 to 0.03, the size of the forecast's
  own error, so no line separates the right answer from the shortcut with margin.
- A separate result for what widening buys at 512,000 examples, and one for what the tuned learning rate buys there:
  each is one matched pair in the pack, a group-by the runs make unprompted, so each is earned and prices nothing.
- Nine asks on bands set by four members of one method family, with the held-back gap, the run counts and the widest
  configuration's learning rate graded (the first cut of this architecture, judged NOT_DETERMINISTIC on a narrow
  footing, FIX_NOW): the judge's own derivation (a level of its own at every total with the costs from contrasts
  between mixes, every run on the carried loss) named B and landed outside the bands on the contractor's cost
  (0.0023 against 0.0000 to 0.0020), the 512,000 level (0.599 against 0.600 to 0.613), A and the range, and the
  held-back gap proved a property of the solver's own curve (0.004 to 0.027 across sound ones), not a figure to
  grade. The bands were reset on a family of 49 run analyses that holds the judge's readings and the two bounds on
  what the examples past the largest trial return; the gap, the counts and the rate became working. With nine asks
  the careful pass then earned five and priced at 57 to 61, so the two reflex asks went and six results are graded.
- The width step priced through A (the pooled width term's 0.679 against a band topping at 0.672): a width curve on
  the carried loss gives 0.68 to 0.71 and the benchmark's own 512-wide scores less a step 0.663, with the truth at
  0.662, so A cannot be banded tighter than 0.650 to 0.720 and prices nothing.
- The level at or under the pool taken from the expert-label runs, the ladder put on the trials' rate, as the golden's
  own reading of the routes (contractor 0.0010 a tenth, B's range 0.609 to 0.638): the judge's second pass read the
  costs from mixes at one total (0.0018 to 0.0024) and the truth runs put them at 0.0017, so the same-total reading
  became the golden's (0.0020, range 0.604 to 0.645) and the first reading the other member the bands hold.
- The levels sentence priced at two results, with a least-squares floor fixed as the hinted pass's continuation:
  given a level at every total and left to choose its own form on the runs held back, the careful pass lands C and
  D as well, so the count is three of six and the note says so.
- Architecture 1 as shipped (the Norwegian group's scale-up forecast from a staged pilot sweep, six results, name
  configuration B at 0.625): spent on the platform on 2026-11-11. One run earned every graded result in 28 minutes
  (`runs/arch1_triage.md`): it compared two candidate calibrations by leave-one-out error, read the slowdown in
  matched cells (0.0471 then 0.0274 a doubling at one mix), fitted a response surface with a fitted breakpoint and
  validated it on held-out configurations, and resampled configurations and calibration pairs separately. The six
  results were one runs-by-settings table that one flexible fit absorbs, the asks named the intermediate quantities,
  and bands wide enough for every sound method (C from 0.648 to 0.689) graded nothing. No tighter honest band fails
  that run, so the world is spent: re-rooted to another world, dataset and shell as architecture 2.
- Architecture 2, a tenth result for what version 3 changed against version 2 on like conversations: on the built
  pack the linked comparison read 6.2 points, the restored one 7.1 and the like-for-like one 6.9, so no reading
  separated from another and the result priced nothing; cut, with version 2's weeks kept as the alerts' before period.
- Architecture 2, the backlog report in weekly age bands: a closed case raised early in the last week is both likelier
  closed and likelier to follow a conversation inside the seven-day-old window, so the weekly share overstated the
  open follow-ups by half (288 added against 182 true, Damaged parcel 4.7 points low). The report counts open cases
  by days open, as an ageing report does, and each closed case stands for the open ones of its own day and
  neighbours.
- Architecture 2, asks for the season's conversations a week and the adviser contacts they pass on: an ask for a
  volume built from the plan's parcels is the first half of the season mix, asked for, which is how architecture 1
  handed over its decomposition. The volume is a Critical Component and the prompt asks only for rates, ranges and
  the designation.
- Architecture 2, telephone follow-ups priced on the grain of the capture share (a pooled or weekly share against the
  quarter-hour's): on the built pack a pooled share moved no family by more than 2.0 points, inside the band a
  sound rebuild needs, so the grain prices nothing; the result is priced Right for the careful pass and the hurried
  failure there is leaving unkeyed calls out.
- Architecture 2, the telephone and case exports as silent partial extracts (calls with no tracking number absent,
  open cases absent, nothing filed): the determinism spec needs a source the golden completes to say it does not
  hold every member, and a silent partial extract is the planted defect the client names. KS-07 5.1 and 5.2 file
  both facts, the unkeyed calls are rows with a blank number, and both restorations are priced Right for the careful
  pass.
- Architecture 2, a common shock every twelve calls after a telephone contact (two or more calls per conversation in
  one in eight): a conversation with two calls and one keyed was overweighted and Track and trace's hidden
  follow-ups came out 24 per cent high; an adviser now settles most matters at the first call, as the summer weeks'
  record would show, and the weight is right to 3 per cent.
- Architecture 2, test rows and a repeated block as Layer 1 (the product team's tester sessions, a telephony test
  queue, ISO week 39 carried twice by overlapping weekly exports): the stage 4 leak reader read the test queue as
  possibly planted, and test rows and a copied block are the first two items on the client's list of planted
  defects. All three are out of the generator, with the sentence of KS-07 3.2 that excluded staff conversations; the
  backlog report now lists only the ages that have open cases (the reader read the zero-filled grid as generated),
  the depot list carries the hub and its date in two columns, and the plan's notification sheet has four short
  columns. No graded figure moved.
- Architecture 2 as built (nine results, pair 46.7 on paper): judged DETERMINISTIC and APPROVE at stage 4 on
  2026-11-11, and sent back to stage 2 by the same pass. The judge thread's own first derivation, at medium effort
  and before it saw the answers, found both measurement gaps from the files (the weekly flow against the extract,
  the advisers' tick on unkeyed calls), read resolution by delivery outcome from one group-by, weighted the plan's
  parcels by each outcome's contact rate at the alert depots, and landed all eleven rates and the set inside the
  bands in about four minutes; only the resampled range was left undone. Every estimate in the chain was a join and
  a ratio over ingredients a file labels (KS-07 5.1 and 5.2, the outcome class column, the plan's service-level and
  alert sheets), and five such estimates are still what a pass that reads every file wires together. The lesson for
  the next draw: a result is priced only where nothing in the pack labels its ingredients and no hold-out or
  reconciliation confirms it.
- Architecture 2 re-rooted on 2026-11-12 (the judge thread's first pass is the evidence: every estimate a join and a
  ratio over labelled ingredients, landed in four minutes). Architecture 3 moves to another world, dataset and shell (a
  merged Texas health system's patient index, a whether-question, a workbook and a Word memo) and to a weight the last
  two live builds do not carry (validation). Its priced results are error rates of record-linkage rules that no file
  labels and no hold-out covers: chance agreement read from the population's joint name, cohort and birth-date
  distribution, kin that share every field but one, an identifier stored for the wrong unit, an earlier merge rule's
  overlays; the only witnesses are clinical events the rules never use.

