# task1: which band each of Zancada's paid acquisition channels sits in for 2027

## Draw

Subdomain: Cohort and LTV modeling: retention curves, customer lifetime value (Product Analytics, retention-cohort-lifetime-value-modeling)
Analysis type: Forecasting & Predictive Modeling
Answer shape: a flagged set (each of the seven paid channels placed in the growth policy's scale, hold or cut band on its forecast 12-month net revenue per euro at the 2027 media plan's weekly spend, with the figure, its band and the results behind it)
Weight: measurement: most of the work is measuring a quantity no record holds (what a euro of each channel's 2027 spend returns in twelve months) from instruments that each see part of it; task22 sat on assembly, task7 on modeling and task23 on modeling, and this slot's architecture 5 on modeling
Data-native sentence: a store charge reaches Zancada's own records only when the subscriber next opens the app, the attribution partner's export holds an iOS install only when its user allowed tracking, and the 2027 plan buys Google Android at weekly spends the 2026 record reached only in two pushes, so each channel's twelve-month return has to be assembled from the stores' sales reports, the ad networks' conversion postbacks and the weeks of heavier spend, each part from the instrument that sees it.
People: Bernardo Pombo (head of financial planning, who signs the 2027 insertion orders), Magdalena Requena (head of growth, owner of the growth policy), Ester Rey (growth analyst, whose workbook and note the golden are), Rafa Naranjo (paid acquisition manager) (`guard.py names --geo spain --seed 61113`). None appears in the prompt.

Architecture 6, 2026-11-13, a new world on the author's word after architecture 5 (Kraanvogel's January 2027 price rises) was sent back at review with one open member (runs/review_2026-11-13.md). Prototyped before the card on the source-assignment anatomy and the open-members rule (`stumping` Part 3.4): in a scratch world every one of the eleven shortcut routes files at least one channel wrong, on nine to eleven distinct wrong calls; three distinct stumps open their own channels (the charges the app never records open AppLovin and Meta Android, tracking consent opens Meta iOS and TikTok iOS, the spend response opens Google Android); each open member's margin sits between the honest family's spread and the stump's worth.

## Stump screen

Screened on paper and in the scratch prototype before the card (`references/stump-screen.md`, the thirteen tests).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| A: subscribers who stop opening the app keep paying for months, and their charges never reach the app's records | the app's payment records are complete, or the stores' excess is spread in proportion to what was recorded (N21, L44) | the stores' daily sales reports by product and country against the app's charges and each account's last open | none | kept |
| C: iOS users who allow tracking are the more engaged, and the attribution export holds only them | the export's iOS users stand for the channel's installs (N27: the postbacks set aside for want of user identities) | the ad networks' install postbacks with each install's conversion value, against the app's own record of every account's first two days | test 2 weak (some runs know tracking consent) | kept |
| B: the auction charges more and returns weaker users as a channel's weekly spend rises | the 2026 revenue per euro holds at the plan's spend (N01: an enlarged commitment assumed to scale in proportion) | the 2026 weekly spend against each install week's installs and value, the 2026 pushes above all | test 2 weak (media-mix saturation is known) | kept |
| the 2026 cohorts not yet twelve months old completed from the older cohorts' later months | young cohorts read at their observed months (closed card: completion of young cohorts) | the 2025 cohorts' full twelve months | 1 (closed) | supporting only |
| SKAN conversion values withheld on small campaign-days read as no conversion | a withheld value is a zero (data semantics) | the postback's own null and the campaign-day counts | 3 and 8 (a field read; banned alone) | texture |

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
- 2026-11-12, at build: an AND built from the live log over-counting Gezin's re-listening: the counting rule takes a title's live position at most once, so a live-only first reach can only under-count (Gezin came out low, not high); the second correction moved to profile membership, partners folding their own subscriptions into family accounts with their history, which today's profile export credits to the family account.
- 2026-11-12, at build: the 2026 revenue share carried forward landed on the golden's plan (Gezin) while Gezin's counted hours per euro of revenue sat near Onbeperkt's; child profiles' listening moved toward re-listening and Onbeperkt's adults listen more, so taking hours out of the cost now favours Onbeperkt, and the agency fees were set from the pack's own pre-fee values over a plausible band (EUR 10 to 55) for the widest narrowest margin (24 per cent on paper, EUR 8.7 measured).
- 2026-11-12, at build: a filed fee perturbation of 10 per cent on Gezin left it EUR 3 ahead and a 10 per cent move in the 2027 rate would flip it to Flex; the rate is filed in schedule B and not fitted, so the forcing block moves the fees 10 per cent and each plan's measured counted hours 5 per cent, and the note records that R5's level is sensitive to the count's level, which the reconstruction pins exactly.
- 2026-11-12, stage 4, architecture 4 as built (Gezin EUR 22.0 per trial start, careful route Onbeperkt, pair 43.7 on paper): the determinism judge kept the order and its own first pass rebuilt R1 exactly and R2 inside the band on all four plans before it opened the blocks, merging the licence renewals and dating profiles by the charges' profile lists by reflex; disposition SEND_BACK on Gate G (planted_defect_flip: a coverage gap and a stale roster, two record corrections whose discovery is their remedy) and H3 and H5 (the compound hint naming both rescues the call); architecture spent. The lesson for the next draw: a second record the pack carries beside a reconciliation target is merged by reflex, so the deciding judgment must be an estimate whose reflexive method lands wrong, not a record to be found or re-keyed.
- 2026-11-12, architecture 5 at design: the cap response graded as a result: its estimate from counted hours (1.6) cannot recover the world's multiplier on listening time (2.3), because the cap binds on time listened, which the files do not hold; kept in the world, reaching the golden through the past downgraders' own months, and no longer asked.
- 2026-11-12, architecture 5 at design: asks for what a downgrader brings and for the leavers' listening against their plan named the two valuations' intermediates and would have handed them over; both left inside R7.
- 2026-11-12, architecture 5's first cut (Flex 9.99 to 11.49, Gezin 22.99 to 26.49): returned by the holistic audit because the 2027 Gezin and Flex rises lay outside every past rise's size and overshoot, so whether the response grows with the rise was open and a dose-scaled reading withdrew Gezin (the platform run withdrew Flex and Gezin on log-dose scaling); the audit also showed the single-run truth check too noisy to test the golden (Flex's sign at EUR 0.50 a coin flip under replays). Repaired with each rise at its own past size, the rival's July 2026 rise and a replayed truth; Flex at 10.49 with the rival unmoved (truth EUR 0.04, se 0.3) was tried and rejected as a coin flip.
- 2026-11-13, the repaired cut (Flex 10.49, Gezin 23.99, the rival's July 2026 move, Onbeperkt alone going ahead): one trick by the author's audit and the new stump factorial; against the platform run's own route (downgraders kept, own listening) the crossing alone rescued four of five results. Re-designed with three stumps; persistence after a crossing rise (light listeners leaving from the third bill to the sixth) was tried as the second and dropped: it reached only Standaard, which the crossing already holds, so it never moved the call alone.
- 2026-11-13, stage 4 pass 1 on the factorial cut: the judge sent it back because the blocks did not say Gezin's December leaving was in the golden (it always was: +8.8 without it, +6.1 with it); the blocks now give every plan's December and listening rates and the leavers' valuation, and two readings joined the golden family (the plain mean of past crossings for a plan with none of its own; responses not floored at none), widening Standaard's and Gezin's first-bill bands. Pass 2 DETERMINISTIC, APPROVE.
- 2026-11-13, the reshipped cut (9ecc8c8, Gezin alone): returned by the platform's holistic audit (runs/arch5_audit_2026-11-13.md) on two counts, both true. Standaard's 2027 crossing had no past crossing of its own and the golden's carry was wrong against the world itself (21.2 and 16.1 per 100 against a replayed 4.5 to 7.4 and 41.5 to 43.9: the other plans' crossing downgrades were held down by profile limits that never bind on Standaard, and checks.py never set R3 and R4 against the replayed truth); and Onbeperkt's call turned on one constructed second-profile uplift that one table shows. The run pasted with it (runs/arch5_run2.md) made the crossing with the profile limit and the December leavers unprompted (R61, R62), so the factorial stood on the uplift alone. Re-designed in the same world at the audit's request: no 2027 configuration the record never ran, the uplift removed, the past e-mails dated, two processes the runs named and waved through (a stop followed by paying again, N33; the stayers' consumption response, N23) run on every plan; every graded figure now checked against the replayed world.
- 2026-11-13, a backtest of the 2026 rises predicted from 2025 alone as an ask (the audit's first example): Flex's and Onbeperkt's 2025 rises passed the rival and their 2026 rises did not, and Gezin's ran the other way, so a forecast from 2025 alone needs the cross-plan carry of a never-seen kind the audit refused for Standaard (the downgrades above all); its second example, a December effect under stated e-mail dates, is taken: the price list dates every past e-mail.
- 2026-11-13, Standaard's own past crossing (the rival's Plus 30 uur at EUR 14.49 in Flanders in 2025) to pin a 2027 crossing: pinned, but Standaard then held whatever the other judgments did; the rival's Plus 30 uur at EUR 16.99 keeps every Standaard rise below it, and Flex carries the crossing instead (its own 2025 Dutch rise, the rival's July 2026 rise to EUR 10.29).
- 2026-11-13, at design: the stayers' extra listening as one flat uplift on the whole account: it cost Flex and Standaard as much per hour as Onbeperkt and put every plan below zero; it falls on the account holder and grows with their listening, so it decides Onbeperkt and moves the others little.
- 2026-11-13, at design: Standaard's EUR 1.00 rise with the returns reached only EUR +0.1 in the replayed world, too thin to force; its past and 2027 rises are EUR 1.50, the 2027 rise still its own past rise in euros.
- 2026-11-13, at build: the stayers measured as accounts paying in December and in the month read (not in every month between) counted subscriptions that left and paid again by the summer; the stayers are those on the plan in every month to the one read.
- 2026-11-13, at build: the fade fitted across the plans puts Onbeperkt's 2027 extra hours at 37.8 against the replayed world's 26; the pack's own first-quarter months (18.9, 16.4, 17.8 per cent) support the fit, the plan-by-plan fade and the observed months sit inside the band, and no reading moves Onbeperkt off hold.
- 2026-11-13, stage 4 judge pass 3 on the first repaired cut: NOT_DETERMINISTIC, SEND_BACK. "Passes the rival" read two ways: crossing from at or below the rival's price (the golden) or a new price above it, and Onbeperkt and Gezin in Flanders had sat above the rival since their own 2025 and 2026 rises, so under the second reading their Flanders 2027 cells came from crossing events (10.8 to 29.7 per 100 against the golden's 0.9 and 0.6); only one past rise (Flex's Flemish 2026, already above) told the readings apart. Closed by construction, not by a sentence: the rival's Flemish Basis 10 uur at EUR 9.79 like the Dutch one (so Flex's Flemish 2026 rise crossed from below, as its Dutch 2025 rise did), and in July 2026 the rival's Basis raised to EUR 10.29 and its Flemish Onbeperkt and Familie brought to its Dutch prices, so no plan sits above the rival before any rise and both readings classify every case alike (SF20, asserted in checks.py and verify.py). The call holds (Standaard and Gezin).
- 2026-11-13, stage 4 judge pass 4 on the fixed cut: DETERMINISTIC, APPROVE (the rival comparison rebuilt region by region for every past rise and every 2027 cell, the October base reproduced; the returns and the stayers' listening components not rebuilt by the judge, carried by checks.py against eight replays of the world's 2027). Leak reader (run on the cut before the rival alignment, a data-only change): NO LEAK.
- 2026-11-13, re-root to architecture 6, stump screen on paper (stumping Part 3.4 and the full reflex list R01 to R83):
  in architecture 5's world only the stayers' listening is a stump runs lose (returns R76, the rival-conditioned
  transfer R77, the Flex one-region crossing R77, route migration one group-by and the listening's second channel, the
  catalogue addition the closed co-occurring-change card), so the world hosts one open member and is spent. A new
  B2B subscription world (the three segments with the lowest 2027 net revenue retention under a save-team cap) was
  screened and dropped before any code: expansion ramps slipping against contracted dates is a reflex (R65, R73),
  monthly overage on commits reset at renewal is a convexity runs simulate (R53), and renewals reset toward active
  seats is one join and one regression of the usage log against the contracts; its domain fit read as revenue
  operations. The open class with no reflex on file is source assignment (L03, N14, N27, L44, L08: a second
  instrument at another grain set aside), the approved builds' anatomy.
- 2026-11-13, architecture 6 screen, a second world prototyped and dropped (scratch, no task files): a mobile
  subscription app's 2027 acquisition in six channel and platform cells, each cell's 12-month net revenue per install
  against its quoted cost per install. Four of the six cells were forced, because each cell's value was read from one
  complete instrument (Apple Search Ads by Apple's own attribution, the three Android cells by the attribution export),
  so every route filed them alike. The two iOS ad-network cells were both opened by the one consent stump, one open
  member. And the golden failed on identifiability: the value-by-conversion-value map pooled over iOS users carried
  Apple Search Ads' engagement within each value, putting TikTok iOS at 5.27 against the truth's 4.53, while the
  shortcut that reads withheld values as zero landed at 4.24 (off 0.74 against 0.29).
