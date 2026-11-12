# task1: which plan Kraanvogel Luisterboeken's spring 2027 campaign leads with, on each sign-up's first 24 months under the publishers' 2027 per-hour agreement

## Draw

Subdomain: Cohort and LTV modeling: retention curves, customer lifetime value (Product Analytics, retention-cohort-lifetime-value-modeling)
Analysis type: Forecasting & Predictive Modeling
Answer shape: A forecast path with bands, plus its drivers (each plan's 24-month contribution per spring 2027 sign-up with its band, built from the plan's counted listening, paying months and net revenue, and the lead plan on top)
Weight: hard-to-measure: counted hours by plan are a quantity no record holds (the publishers' remuneration engine counts the furthest position each profile first reaches in each title from two reporting channels, the live sessions and the positions downloaded titles report at licence renewal, and reports totals by publisher only); task22 sat on assembly and task7 on modeling, the last two builds; the overuse.weight WARN against task13 (hard-to-measure five builds back) is answered by the different quantity (sustained interruptions avoided by automated loops there, a royalty base by plan here)
Data-native sentence: Kraanvogel's subscriptions, payments and family profiles live in its billing system, its listening reaches the analytics warehouse only from live playback, and the downloaded titles it plays offline surface only when the device next renews the title's licence, while the publishers are paid on the engine's count of both, by publisher and month; so what each plan's listening costs under the 2027 per-hour agreement is in none of the files until the count is rebuilt per profile, per title and per account as it stood on the day.
People: Romy Korsman (head of growth, owner of the spring 2027 campaign), Hugo Brouwer (finance controller, owner of the publisher remuneration and the growth planning guideline), Tara Martens (growth analyst, whose workbook and deck the golden are) (`guard.py names --geo NL --seed 1112`). None appears in the prompt.

Architecture 4, 2026-11-12, a new world. Architecture 3 (Medienhaus Brückenhafen's 2027 acquisition lines) was returned twice on forcing and determinism (`runs/arch3/review_2026-11-12.md`) and its deciding lessons (vintage_or_cohort_drift, completion_of_young_cohorts) are on the client's closed page of 2026-11-12; architecture 2 (Tekenbord's ARR commitment) was spent on the single-total risk. One architecture per world: a new country, a new product, a new decision form (one of four plans, not a set over a bar), a new shell (a workbook and a deck), and the deciding lesson off the closed page.

## Deep reasoning

Task type: Cohort and LTV modeling (retention curves, customer lifetime value), which serves Forecasting
Domain test: every result is a subscription cohort quantity: paying subscriptions by plan, counted listening per paying subscription-month by plan under the publishers' counting rule, the share of it reported only at licence renewal, each plan's sign-ups' conversion, paying months and net revenue over 24 months, each plan's 24-month contribution per sign-up and the 2027 remuneration of the base; the growth analyst's job is exactly this unit economics per plan.
Swap: "lead the spring campaign with Standaard because Onbeperkt's listeners play half their hours offline, which the session log never sees, and Gezin's re-listening and removed profiles" makes no sense with a hospital's or a factory's nouns: there is no counted hour, licence renewal, family profile or per-hour royalty to rebuild.
Where the weight sits: R2, counted hours per paying subscription-month by plan, rebuilt from roughly half a million profile-title-month rows of live listening and a quarter of a million licence renewals, merged per profile and title into the engine's running furthest position, counted in the month each position reaches the engine, and attributed to the account and plan each profile belonged to on that date.
Lesson: the stored count a contract pays on is an algorithm's output over two channels, and the activity log that looks complete is one of them; no build on file teaches it (record_algorithm_inversion has no carrier).

## Results chain (sketch at the draw; completed at stage 2)

| ID | Result (checkable) | Area |
|---|---|---|
| R1 | paying subscriptions by plan at 31 October 2026 | assembly and reconciliation |
| R2 | counted hours per paying subscription-month by plan, November 2025 to October 2026 | missingness and measurement |
| R3 | each plan's share of counted hours that reach the engine only at licence renewal, same months | data discovery |
| R4 | each plan's spring 2024 campaign sign-ups over their first 24 months: share paying after the trial, paying months and net revenue per sign-up at 2027 prices | modeling |
| R5 | each plan's 24-month contribution per spring 2027 sign-up (net revenue less EUR 0.40 per counted hour and the agency's fee) | forecasting |
| R6 | the 2027 remuneration owed on the subscriptions paying at 31 October 2026 | forecasting |
| R7 | the plan the campaign leads with | synthesis |

One-fact test (at the draw, on paper): "the licence renewals carry the listening of downloaded titles" moves the careful route from Onbeperkt to Gezin, not to the golden Standaard, and rescues R3 alone; "family profiles were added and removed, so read them from the dated events" moves it nowhere (Onbeperkt still); each correction alone files a different wrong plan, both together file Standaard (paper margin 44 per cent, every route's pick at least 44 per cent ahead of Standaard in its own arithmetic).

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
- 2026-11-09, stage 3: seat additions from the book's mean growth in users by account age (no account's own drift):
  EUR 0.10 million against the process's EUR 0.49 million, because need growth differs by account and seats only
  ever true up; replaced by each account's own drift, shrunk to the book (24 months), with 12 and 18 months, each
  account's trailing true-up rate and the book's trailing rate kept as rivals.
- Each account's trailing true-up rate as the golden's seat additions (the stage-2 prototype): EUR 0.56 million,
  above every drift form; kept as a rival, inside every band.
- A slower April decay (PAD_DECAY 3.0, PAD_SHOCK 0.10) to push the careful pass's last-three-months Team rate out of
  R3's band: the excess series is too noisy month by month for the golden to tell the forms apart either, and the gap
  stayed about EUR 15,000; parameters reverted, R3 priced Partly for the careful pass.
- The commitment graded at one 0.1 million bin: the honest family's P20 spans EUR 9.79 to 9.92 million (the exit
  model's utilisation form and the seat-addition form move it), so the commitment's band is 9.8 to 9.9 and the draft
  moved from EUR 10.4 to 10.2 million so that the careful pass (10.23) still clears it wrongly.
- The draft at EUR 10.4 million: the careful but hurried pass's commitment (EUR 10.2 million) sat under it, so the
  pass gave the right verdict for the wrong reason; the draft is EUR 10.2 million.
- Credit notes and re-issues on renewals after 1 March 2026: kept beside the re-issues they moved the price line to
  EUR 310,000 and the commitment to 10.0, so cleaning decided R2; the billing errors now sit on 2024 to February 2026
  renewals, where kept they break the renewal pairing visibly and decide nothing.
- The workspace links' end-and-restart dates listed as Layer 1 mess: read without dates they move R3 (1.43), R5
  (1.12) and the commitment (9.7), because the dates are how an upgrade is told from a cancellation; they are
  evidence for R3, R4 and R5, not mess.
- The ask "how much of October's Team ARR is still billed on the Team plan in December 2027": read two ways (the
  October ARR of the accounts still on Team, or their December 2027 ARR, about EUR 0.07 million apart); the prompt
  now asks for the Team ARR in December 2027 from accounts on the plan at the end of October 2026.
- New Business accounts held at their signing ARR to December 2027 (their ramp true-ups and the first renewals of
  November and December 2026 signings ignored): policy 4.2 counts a first term at its service start, every route
  shares the convention, and it is recorded rather than modelled.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, the uploaded cut (price rise 1 March 2026, Team minimum 1 April 2026, deal creation falling from 37 to 27
  a month after March 2026, the commitment "to the nearest EUR 0.1 million"): the platform's holistic audit failed it
  on determinism (runs/arch2/holistic_audit.md). The P20 of 9.89 rounded to 9.9, a step met in under 80 per cent of
  outcomes, and rounded down to 9.8; the band with and without the estimation uncertainty was pinned by no file;
  the Team and open-deal figures were stated as ranges at 10,000; and the run's "recent creation" reading of the
  post-March fall made a naive pipeline view fail the draft on its own. Repaired in the generator: the commitment
  defined as the largest 0.1 million step met in at least 80 per cent of outcomes (prompt, policy 5.3); policy 5.2
  files what the range carries; the two note figures asked at the precision the defensible methods pin; the creation fall removed (flat since 2024);
  the price rise and the minimum moved to 1 January 2026 so the trailing year carries the whole step and the padded
  seats; the world re-seeded so every graded figure sits mid-bin at its rounding.
- 2026-11-10, a world with the price rise at 1 March 2026 and the creation fall removed (seed 1107, scratch v1 and
  v2): every trailing extrapolation cleared the golden by 0.08 to 0.5 million only, because the trailing year's new
  Business, expansion and churn ran below the forward's while only the price line ran above; with the rise and the
  minimum at 1 January and the creation trend ended in 2024 (v3) the trailing views clear by 1.2 million.
- 2026-11-10, the exit model without a utilisation term priced as a hurried route: in the March-calendar world it moved
  accounts lost by 60,000, in the chosen world by under 2,000 (the term carries the seat cuts, not the exits), so it is
  a rival inside the bin (SF24), and the pooled route and independent draws carry R4's loss.
- 2026-11-10, the book's trailing true-up rate at accounts near their seats as a rival for seat additions: 60,000 under
  the drift forms in every world measured (it ignores each account's own growth and the ramp of young accounts); priced
  as a hurried route; the drift windows 12, 18, 24 and each account's own trailing rate stay the family, which with
  need growth less dispersed (NEED_GROWTH_SD 0.03) lands in one step.
- 2026-11-10, the pooled renewal route's seat-reduction gap as a structural result: in the uploaded cut pooled rates
  gave 310,000 against 200,000, in the first re-seeded worlds the two coincided; the gap was the cut's mix against
  the history's, not the process. The process now carries it: utilisation at signing drifts down year by year, so
  the forward book's renewals cut and leave more than the pooled history says; the direction still varies by world
  and the chosen seed's gap is asserted.
- 2026-11-10, the common factor of 0.25 the platform run assumed, as a defensible rival: nothing in the records supports
  it and policy 5.2 rules it out; in the chosen world it widens the 80 per cent range by about a third and moves the 20th
  percentile down by under 20,000, inside the step, so it is priced as a route the sentence settles rather than one the
  step separates (SF21).
- 2026-11-10, Team seasonality in the hurried "last three months" route: in the uploaded cut the last three months
  sat one 10,000 bin under the golden because the April shock had decayed to its floor by August; with the plan's
  cancellations running with the calendar (an autumn peak in every year of the history) a three-month window
  carries a season and lands 60,000 to 160,000 under the golden in every world measured.
- 2026-11-10, the two note figures at the nearest EUR 50,000: the win odds by stage and deal age put the open deals' part
  20,000 above the stage-and-staleness golden, so at 50,000 the defensible family straddled a bin edge in the chosen world;
  asked at the nearest EUR 0.1 million the family lands in one bin with margin, the CRM's odds stay far outside, and
  stage alone, which that rounding no longer separates, is priced as a route the CRM's odds carry rather than its own.
- 2026-11-10, seeds 1101 to 1124 scanned for a world whose graded figures sit mid-bin at the new roundings with the
  band's step the same with and without the estimation uncertainty and the pooled, trailing-twelve and stage-alone
  routes outside; 1109 failed only on seat reductions 4,000 from a 50,000 edge, 1115 only on the Team figure 4,000
  from an edge; seed 1126 chosen on the full family.
- 2026-11-10, architecture 2 after the holistic-audit repair (seed 1126; commitment the largest EUR 0.1 million step met in 80 per cent of outcomes, 10.0, met in 83 per cent, 10.1 in 69; draft 10.3, met in 36; every naive extrapolation 10.72 to 11.49 clears it; judge DETERMINISTIC APPROVE): measured against the uploaded platform run's own methods (price by size, renewals on utilisation and first renewal, pipeline by stage and time in stage, the Team plan's last three months, recent deal creation), the run lands the commitment and earns R1, R2 and R5, scoring 66.5 of the 93 graded weight (R3 and R7 missed, R4 partly); its two blind spots cancel (lost accounts about 130,000 low without the group term, Team about 76,000 low on the autumn peak). Two world moves were measured and rejected: the Team cancellation peak moved to late winter shifted the golden as far as the route (commitment 10.2, the draft met in 78 per cent); the seat-growth spread restored to the uploaded world's (0.08 a year, monthly noise 0.008) brought back the run's seat-addition miss (routes on pooled rates at 9.8 and 9.9) but spread the honest family over two steps (10.0 and 10.1). The routes table shows why: the five designed judgments each move the 80 per cent figure of a 10 million book by 0.0 to 0.15 million, inside the honest family's own spread, and only the CRM's odds (10.73), independent draws (10.39) and pooled renewals (10.29) separate, all three moves the uploaded run did not make. The determinism the audit requires (the band's contents filed, no added allowance) removes the stacked pessimism that made the uploaded run miss by 0.7 million. The world is spent: a commitment on one total aggregates every judgment below the methods' disagreement. Re-root to a new world in which each judgment flips units of a set or count.
- 2026-11-10, architecture 3 at the draw, a ranked list under a budget cap (best value per euro first until the next line would not fit): over two million cost and budget configurations searched against every rival, the robust cuts (a 7 to 12 per cent gap, leftover budget fitting no unfunded line) turned on one or two lines (the social Kreisblatt and telemarketing Kreisblatt pair) and a careful run that used the reading log landed the golden list, because the full-price and returns shortcuts cancel on the deep-intro lines; replaced by the standard's line-by-line bar (3.5 times the planned cost per start), on which ten lines sit 3 to 14 per cent from the bar, every rival funds the same eight and the shortcuts fund six distinct wrong sets.
- 2026-11-10, the base's December 2027 count as R9: the October 2026 base is mostly long-tenured, so the careful pass's errors cancel (the rise read late adds 3 to 4 per cent, customer-number returns take 2.5 off) and it lands within half a per cent; replaced by the intro subscribers at the cut carried to the full price in December 2027, which the careful pass misses by 6 to 9 per cent.
- 2026-11-10, a first debit able to fail in the engine: a subscription could end before it began, colliding with the withdrawal code for January 2023; failures now start at the second billing, and the pack reproduces the simulator's panel field for field.
- 2026-11-10, stage 4, R9 as the October 2026 intro subscribers paying full price in December 2027: priced on the rubric split, a careful run that read the April 2025 rise in full earned R6 and R9 together (both asks, both carried by the rise's first-year response) and scored 62.1; R9 is now the plan's 2027 starts still paying on 31 December 2027 by channel, carried by the full price at the end of intro and the newest starts' survival, and that variant scores 48.4.
- 2026-11-11, the platform's holistic audit of the uploaded build (returned on determinism): R9 counted the telemarketing free quarter as paying (498 against about 454 on 31 December 2027; standard 2.2), nine lines sat 5 to 7 per cent from the 3.5 bar and J12 had never run on telemarketing or cashback, so a 20 per cent shift in exit rates moved the call from 7 to 15 lines. Repaired: R9 counts no free month; TEL-BHR ran J12 from May 2024 to February 2025 and PART-GAZ from January to September 2024, so both 2027 J12 lines carry an offer their channel ran; the plan's costs per start re-placed so every line sits 12 per cent or more from the bar.
- 2026-11-11, wider margins on the uploaded world (habit drift 0.65 and 0.50, a full-price coefficient of 2.2): with every line 10 per cent or more from the bar the careful pass's social lines needed two shortcuts together (the reading and the period term, each 9 to 18 per cent), so the reading hint and the full-price hint each rescued the funded set and completion alone flipped nothing; the call would have hung on whichever of the two a run made. The process now carries both more strongly (the newest social starts' habit 0.9 lower, cashback 0.7, a full-price coefficient of 3.0), so each single judgment moves lines past the margin: completion alone funds SOC-KBO, the period term SOC-KBO and APP-KBO, and no hint rescues the set.
- 2026-11-11, a calibration of each line on its own newest starts (observed over expected full-price cancellations, shrunk by a pseudo-count) as a rival: it moves SOC-KBO 24 per cent up and swings 8 to 37 per cent with its own pseudo-count and window, because each line's starts of the twelve months to October 2026 have had 3 to 18 full-price cancellations (139 in all, against 146 the reading model and 138 the channel model expect); the count cannot separate the models, so the rival is ruled out on its data rather than banded, and the closing passage and the Checks sheet name it.
- 2026-11-11, a household bootstrap as the forcing evidence: drawing households ignores the line-month campaigns that move a month's starts together and gave line spreads of 3 to 5 per cent; whole start months are now drawn within each line (boot.py, each copy keeping its own customer numbers, fingerprints and addresses so the links rebuild inside it), spreads 2 to 7 per cent, and 39 of 40 draws fund the same eight lines.
- 2026-11-11, a back-test of the leaving model fitted on the 2024 starts and scored on the 2025 starts as forcing evidence: both models over-predict the later starts' exits (the reading model by 10 per cent, the channel model by 25), so it is not shipped; the reading coefficient (minus 0.69, standard error 0.03, on 2,336 cancellations) and the newest starts' measured reading carry the forcing.
- 2026-11-11, the offer and the price stepped up to as terms in the leaving model: neither improves the fit (AIC 20,339.7 and 20,334.3 against the golden's 20,335.0) and each moves line values 2 to 6 per cent; both are rivals inside the bands.
- 2026-11-12, architecture 3 as reshipped (every line 12 per cent from the bar, the clean truth and 39 of 40 redraws on the golden set): returned on determinism by the platform's review (runs/arch3/review_2026-11-12.md); the household-return projection and the young starts' completion were open modelling choices, and the return hazard fitted without early reading alone funds 9 lines (SOC-KBO 3.52), with channel completion 13 (EUR 127,830); the forcing family had tested each choice only inside the hurried route, never alone; both deciding lessons are on the client's closed page of 2026-11-12; architecture spent, re-rooted to a new world.
- 2026-11-12, architecture 4 drawn on a greater-of remuneration (the larger of 52 per cent of revenue and a per-hour floor, monthly on the service's totals): on paper the floor bound in two to four months within 5 to 9 per cent of the kink, so the regime calendar was an open fork, and the with-and-without increment it priced is a reflex (the architecture 3 run computed paired forecasts unprompted); replaced by a flat 2027 rate per counted hour, the 2026 revenue share kept as the shortcut a run carrying the latest cost files.
