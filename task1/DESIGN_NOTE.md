# task1: what December 2027 ARR Tekenbord can commit to in the board's 2027 plan

## Draw

Subdomain: Cohort and LTV modeling (retention curves, customer lifetime value), Product Analytics (`retention-cohort-lifetime-value-modeling`)
Analysis type: Forecasting & Predictive Modeling
Answer shape: A forecast path with bands, plus its drivers (the monthly ARR path to December 2027 with an 80 per cent band, the figure with an 80 per cent chance of being met, and the drivers that bridge October 2026 to December 2027)
Weight: synthesis: five flows, each set by its own mechanism and estimated from its own file, have to be carried into one path whose pieces add back and whose band keeps the dependence between accounts; task4 sat on measurement, task7 on modeling, task6 on a hard-to-measure quantity
Data-native sentence: Tekenbord's ARR moves only through contracts, invoices and renewals, while the reasons it moves sit in other systems (the price book's effective dates, the product's workspace activity, the CRM's account tree and pipeline snapshots), so each flow has to be stitched from a different pair of files before the trailing totals mean anything.
People: Naomi Weijters (CFO, owns the ARR reporting policy and the board commitment), Jelte Helmerhorst (revenue operations analyst, whose workbook and note the golden are), Floortje Huisman (head of sales, owner of the pipeline export) (`guard.py names --geo NL --seed 1107`). None appears in the prompt.

Architecture 2, 2026-11-09, a new world. Architecture 1 (Corvane, tutor-linked member retention) was returned in
kind by the project lead's review of 2026-11-09: one constructed factor (the tutors' stopping hump) placed in the
forward cohort by an onboarding pause and a surge, with every graded figure coming out of one projection.
Guard: WARN (overuse.strategy decomposition_attribution 3 of 12, answered: the strategy is the honest label, the
forecast is built flow by flow; overuse.forcing_event vote_or_meeting, the board's plan meeting is what forces it;
repeat.gate_g forecasting, the assigned analysis type; repeat.decision quantity_figure and repeat.deliverables
docx and xlsx, the board's plan takes a figure and a workbook). Nearest driver task10 at 0.06; differentiated against
mark162's spent v1 (an uptake timed at each unit's restart, one flow, against five here).

## Tried and rejected

- Matching new members to the tutor with the most open slots (pricing simulator v1 to v2): every month's new members
  went mostly to new tutors, so history carried the same exposure as AUT26 and the curve landed on the truth
  (0.834 against 0.837 of receipts); the world needs the platform to match new members to established tutors and to
  run with spare established capacity, which it does.
- Twelve-month receipts per member as the decision quantity: the four observed months dilute the move to about
  3 per cent of the figure; the twelfth-charge retention carries it at about 18 per cent.
- Matching new members to the most established tutor with room, where "established" began at four teaching months
  (simulator v9): surge members landed on tutors inside the stopping hump, the spring 2025 campaign carried as much
  exposure as AUT26 and the curve missed it by 17 to 22 per cent on back-test, a search signal; established now means
  nine or more teaching months.
- A spring 2025 campaign of 680 members (simulator v7 to v10): either it carried most of the effect (the textbook
  route failed its own back-test) or it was too small to tell the models apart; SPR25 is now 264 members, too few to
  separate the routes on its own, the textbook route validates on it, and the discriminating evidence is member-level.
- Tutor capacity fixed at hire (generator v1 and v2): established tutors stayed full, so surge and growth overflow
  went to tutors inside the hump in ordinary months, history carried AUT26's exposure and the curve landed near the
  truth (0.301 against 0.303); established tutors now open more slots once past their first nine teaching months.
- A post-rematch uplift and calendar-month seasonality in the process (generator v3 to v6): neither decided anything,
  and between them they moved the graded cost per twelfth-month member by about 1.3 per cent across defensible
  variants, a fork at any useful rounding; both left the process.
- A 50 per cent first-month offer: the discounts were a quarter of the cost, so a deep run that misread the cost rule
  and left them out filed the re-run; the offer is now 10 per cent and leaving it out stays 5 per cent outside the bar.
- Tutor ids rewritten at a 2025 lesson-platform migration: left unnormalised they split tutors, flattened the stopping
  hump and flipped the call (1,274 twelfth-month members), so cleaning decided the answer; ids keep one format.
- A range on the twelfth-month members as an ask: tutor-clustered and member-independent ranges coincide at the
  nearest 50, so it graded no judgment; the cost ranges at the nearest 25 separate at every endpoint.
- Fuller new-tutor rosters to widen the clustered range (caps 26 to 36): one endpoint separated and the shallow routes
  moved to within 6 per cent of the bar; reverted.
- A 95 per cent range on the cost per twelfth-month member: its upper end sat on its rounding line at 4,000 draws
  and its lower end moved with the draw, so the figure was a coin at the nearest 25; the 90 per cent range keeps both
  ends inside their rounding (`checks.py` R7) and members drawn one at a time move both ends.
- An 80 per cent band on each month's total in the workbook: several of its 22 ends changed between seeds at 4,000
  draws at the nearest 50, and at the nearest 100 it no longer told tutor-by-tutor draws from member-by-member ones;
  the workbook carries the monthly expectations only.
- 2026-11-09, architecture 1 (Corvane, the autumn campaign's members carried through their tutors' stopping hump):
  returned in kind by the project lead's review (one hidden constructed factor; the forward cohort was the only one
  built to be exposed, the generator tuned until history stopped carrying the exposure, and every graded figure came
  from one projection). Re-rooted to a new world as a results chain.
