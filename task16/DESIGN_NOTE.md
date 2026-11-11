# task16: which enquiry types Quellstein Paket's assistant keeps taking first through the 2026 peak season

## Draw

Subdomain: General Statistics & Data Science
Analysis type: Data Extraction & Conformation (ETL / Pipeline Build)
Answer shape: A reconciled table plus findings (each reason family's resolution rate achieved and expected, tied back
  to a linked contact record that reconciles to the telephony and case totals, with the keep or hand-back call on top)
Weight: assembly: most of the work is building one contact record that can be trusted across four channel logs and
  estimating the follow-ups that record cannot see; the last two live builds lean on investigation (task18) and
  modeling (task1), and architecture 1 of this slot leaned on investigation
Data-native sentence: a customer who is not helped comes back through whichever channel is open, and each channel
  loses sight of the consignment in its own way (the telephone line stops asking for the tracking number when it is
  busy, a written case is counted against a conversation only once it is closed), while the season being planned draws
  its conversations from parcels in proportions set by how often an on-time, a late or a held parcel makes its
  recipient ask at all
People: Helena Neumann, Simon Pertl, Theresa Jovanovic, Alena Blümel (guard.py names --geo Austria --seed 1602)

Architecture 2, drawn 2026-11-11 after architecture 1 was spent on the platform (`runs/arch1_triage.md`). The careful
but hurried column is calibrated to that run: it reads every file, reconciles record counts, compares candidate
methods by held-out error, fits any pattern one table shows, validates on held-out groups and resamples clusters.
So no result here is priced on a pattern one table shows or a choice a hold-out settles. The chain's weight is on
estimates the data in hand cannot flag when they are left out: who is missing from a linked record, and who the
season's conversations will come from.

The world. Quellstein Paket is an Austrian parcel carrier with ten depots. Its contact division runs a chat
assistant, live chat, a telephone line with an IVR, and written cases (web forms and e-mail). The division's service
standard counts an assistant conversation as resolved when nobody makes a further contact about the same consignment,
through any channel, in the seven days after it ends, and makes a reason family assistant-first for a season when its
expected resolution rate, given the season plan, is at least 75 per cent. Version 3 of the assistant went live on
Monday 28 September 2026. The extract is cut on Monday 9 November 2026; the peak plan covers 16 November 2026 to
3 January 2027 and is fixed this week.

Guard WARNs answered. `overuse.gate_g` (method or model selection in six of the last twelve): the label is the
honest one, because each estimate has a shortcut and a sound form and the data in the pack say which (the keyed
calls for the capture, the backlog counts for the open cases, the pilot depots for the alerts); nothing here is a
forecast the past does not pin. `repeat.decision` (a designation set, as task1's last build): the standard's rule
makes the answer a set of families by construction; the shape differs (a reconciled table by family, no cap, no
ranking) and the question asks what rate to expect. `test.same_driver_older` is differentiated on the card against
mark196 and task6's second architecture.

## Deep reasoning

Task type: Data integration, record linkage & entity resolution
Domain test: every result is a record-linkage and missing-data quantity (a linked record reconciled to control
  totals, events the link cannot see restored by the inverse of a capture probability that moves with load, open
  cases completed from a count at another grain, a rate standardised to a population whose mix is exposure times a
  class-specific contact rate, an intervention's effect on that rate from a staggered roll-out, a range that carries
  day-level dependence)
Depth level: 5 on the client's depth scale, to be confirmed on the built pack: five independent judgments (the
  capture-weighted telephone follow-ups, the open written cases, the like-for-like version comparison, the season's
  conversation mix with the alerts' measured effect, the day-level range), each moving different families across
  the 75 per cent line, with the shortcuts landing on different sets

## Results chain

Sketch at the draw; pins, bands and the measured hurried figures are written at stage 2 from the built pack.

| ID | Result (checkable) | Area |
|---|---|---|
| R1 | the linked record: version 3 conversations with seven full days behind them and their follow-ups by channel, reconciled to the telephony and case totals | assembly and reconciliation |
| R2 | the telephone follow-ups, with those the tracking number never captured | missingness and measurement |
| R3 | the written follow-ups still open at the extract | missingness and measurement |
| R4 | each reason family's resolution rate achieved under version 3 | synthesis |
| R5 | what version 3 changed against version 2 on the conversations it handled | causal reasoning |
| R6 | the delay alerts' effect on conversations per late parcel | causal reasoning |
| R7 | the assistant conversations a week the season plan will generate, and the share from late or held parcels | forecasting |
| R8 | each family's expected resolution rate over the peak plan's weeks | forecasting |
| R9 | the 90 per cent range around it | uncertainty |
| R10 | the families to keep assistant-first and those to hand to advisers first | synthesis |

Carry-forward: R2, R3 and R6 each read an input of their own (the call log, the backlog counts, the pilot depots);
R4 and R5 fall with R2 or R3; R7 falls with R6; R8 and R10 need R2, R3 and R7 together; R9 is graded on the range's
width.

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
