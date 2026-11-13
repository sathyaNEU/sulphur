# task23 architecture 1, READY cut 3bf7d67: the platform's holistic audit (pasted by the author, 2026-11-13)

Verbatim.

> Holistic Audit
>
> The data work in your answer is strong. The cell 5 tonnage (574,197 short tons) reproduces exactly, and the
> pressure-history correction of the campaigns (beta about 0.10 per hPa at a 16 hour constant, 2025 actual about
> 4,924 t) reproduces from the chamber and station files.
>
> The problem is that the Package C vs D call is not forced. C misses the limit by 449 t, about 8 percent. That margin
> is smaller than the spread your own method allows:
> - Your accepted band for cell 5's 2027 generation (3,302 to 4,202 t) straddles the level, about 3,644 t, at which C
>   passes.
> - Reasonable pressure-response specifications move the site level by about 5 percent (4,709 t at a 24 hour constant
>   against 4,926 t at 16 hours).
> - How much yield the new cell 4 pumps restore is unpinned (about 836 t vs about 970 t of benefit).
>
> A careful analysis that keeps every intermediate inside your tolerances can still put C at about 5,076 t, under the
> limit.
>
> To fix it, either widen the gap so C fails under every reasonable variant (for example, raise cell 5 receipts in the
> fill plan or tighten the limit), or state the forecast basis in a shipped document: pumped-well recovery and how cell
> 4's collection fractions are carried into 2027. Then confirm C stays above 5,100 across the variant sweep.
>
> For what we are looking for, see https://project-sulfur.learn.joinhandshake.com/nov-09-updates.
>
>
> Reasoning
> Step 0: the golden is present and the inputs match the task (Fernhallow, Kelloway County, Tessaline, Brightwater,
> Resolution 2025-41 with the 5,100 t limit, and packages A to E costed at 0.00/0.64/1.21/2.38/5.95).
>
> Part A, what I reproduced:
> - Cell 5 MSW tonnage: dropping VOIDs, keeping REISSUEs, mapping the MSW-* codes and filling blank disposal areas from
>   the daily log gives 574,196.58 short tons (574,195.8 from pounds). Author: 574,197. Agree.
> - Pressure response: a log-linear fit on AC-1 and AC-3 QC-OK hours, with the UTC clock shifted 8 h, chamber-month
>   effects, the soil-temperature departure and 6-hour rain, has least-squares SSE minimized at tau=16 among 4, 8, 12,
>   16, 24, 32 and 48 h. The coefficient is 0.0967 per hPa. Author: 0.100. Agree.
> - 2025 campaign factor and 2025 actual: the mean factor is 0.71 to 0.72. The 2025 actual comes out at 4,926 t with
>   beta 0.100 and 4,865 t with my fitted beta. Author: 4,924. Agree.
> - Pump scope: 17 unpumped cell 4 wells had liquid above the screen bottom in October 2026. EW-446 has no October
>   reading but has sat at about 34 ft against a 76 ft screen bottom all year, so the author's 18 is defensible. Its
>   flow is about 6 scfm, so it does not decide the call.
> - Not rebuilt: the 2027 package figures (A 6,942, B 6,385, C 5,549, D 4,495, E 4,095), cell 5 generation (3,752 t),
>   the cell 5 oxidation share (17.1%) and the bridges. Each sits at the end of a long chain of fitted parameters. I
>   could not independently reproduce them, so decision_reproduces is unclear.
>
> Part B, determinism:
> - The call is D over C, and C fails by 449 t, about 8% of its 5,549.
> - The run is careful. Every intermediate it reports falls inside the author's own tolerances: 2025 actual 4,691
>   (within 10%), tonnage exact, cell 4 change +85.1% exact, cell 5 generation 3,615 (within 12%), oxidation 16.2%
>   (within 4 points). Even so, it lands C at 5,076, which passes.
> - The run states that C flips once cell 5 generation is above 3,644 t. The author's accepted band for that figure is
>   3,302 to 4,202 t, so the band straddles the flip point.
> - Reasonable specifications of the pressure response move the 2025 level by about 5%: tau 24 gives 4,709 t against
>   4,926 t at tau 16. That level flows into the cell 4 generation used for 2027.
> - How much yield a pumped well recovers is unpinned: the author's C minus B is 836 t, the run's is about 967 to
>   977 t.
> - Together these swings exceed C's 8% margin. The run's package figures sit about 5% (A) to 11% (D) below the
>   author's, which points to differences in the 2027 forecast chain, not one mistake.
> - No document pins the forecast specification closely enough to force C over the limit. Determinism is not_pinned
>   (margin and boundary fragility).
>
> Part C, depth:
> - The task is genuinely deep: assembly with void and reissue handling, the pressure-sampling correction, separating
>   the cell 4 flooding effect from generation, kinetics, saturating oxidation and a package forecast. No one-thing
>   flip, rule-application or hidden-factor flag. Depth level 4.
> - The run did not fail at a hard sub-result. Its intermediates match, and it diverges only through accumulated
>   defensible forecasting choices near a thin margin (defensible_alternative_rejected / near_miss). That is not
>   valid evidence of difficulty.

## Checked against the build (2026-11-13)

- The margin: true. On the READY cut a 24-hour lag alone put C at 5,246 t (2.9 per cent over), a 32-hour lag at
  4,995 t (under), and a 24-hour lag with a pump gain 16 per cent larger at 5,115 t; with cell 5's calibration 4 per
  cent low as well it reached 4,998 t, the run's 5,076 t. The world's own replay of 2027 put C at 5,233 t, only 2.6
  per cent over.
- The pumps: true, and worse than stated. The options paper said the pumps "hold the liquid below the screen, as the
  June 2025 pilot pumps do", read literally as a cleared screen, while the golden held the pilot's 0.04 of the screen
  under liquid as a constant typed into the code rather than read off the pilot wells; and its scope ("at the October
  2026 liquid level survey") left out EW-446, last gauged in July.
- Cell 4's carry: inert. By zone, held flat, over twelve months or October alone, C moves under 1 per cent.
- Part C: the audit rates the build at depth 4, with no one-thing flip, rule application or hidden-factor flag. Its
  run made all three priced judgments (the pressure response, the recirculated decay read past the flooded wells,
  the saturating oxidation, its R2, R3, R4 and R5 inside their bands) and lost only the call, through the forcing. By
  the stump factorial (stumping Part 3.3) a judgment a run makes unprompted is a reflex; filed as reflexes, these three
  would leave the factorial without a stump and the careful column's losses on R2 to R5 uncited. The run's own text is
  not in the repo, so its lines are not yet in precedents.json: the author decides whether to file them from this
  summary, as task7 architecture 12's audit was, or to let the platform's two runs measure the repaired cut.
