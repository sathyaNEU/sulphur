# Run triage, task11, 2026-11-08
**Verdict:** FIX_ASKS (after a required RUBRIC_EDIT plus golden fix on criterion 4, which raises both scores and so does not move the verdict toward SUBMIT)
**Scores:** run 1 78, run 2 54, average 66; counterfactual 88, 64, average 76

Golden call: Fennick Creek, 47 of 47 days above the trigger, every other sub-watershed 0 (submission.md section 1).
Default path / rung 1 (DESIGN_NOTE `## Default path`, `## Ladder`): Tessel River by load share (39 days). Neither
run took the default path: both rejected Tessel and whole-lake mixing on the buoy profiles.

## Verified fact: criterion 4 (Dunmore Creek monthly atrazine) is a golden defect

- `generator/golden.py` `rated_flow` (line 198) returns `float(np.interp(h, hh, qq))` for any stage above the
  rating's first point. `np.interp` holds the end value beyond the table's last stage, so **the golden clips**:
  above the top stage, discharge is held flat at the table's last discharge (rating 1: 6.00 ft, 702.47 cfs; rating
  2: 5.99 ft, 696.77 cfs). `verify.py` line 242 has the same clamp, so the independent check repeats the defect
  rather than catching it.
- Recomputed from `target/` with golden.py's own functions: 190 DC-04 15-minute intervals in the April to July
  window sit above the table's top (from 28 April to 24 July). Stage reaches **2.82 ft above the table's top**
  (about 8.8 ft against 6.0), and the golden still holds the flow at about 700 cfs.
- Dunmore monthly kg (April, May, June, July): golden clip 4.2, 64.3, 71.1, 13.7 (that is 4, 64, 71, 14).
  Linear extension of the last segment gives 4.3, 70.1, 82.8, 14.0 (4, 70, 83, 14). A power law fitted to the top
  of the table gives 4.3, 70.5, 84.1, 14.0 (4, 70, 84, 14). Both runs fitted a power law and reported
  4, 70, 84, 14. Run 2 also reported that terminal-linear extension moves June to 83.
- No file, prompt sentence or fork-table row (DESIGN_NOTE SF1 to SF13, closure table) pins what to do above the
  rating. The determinism report (line 83) reproduced 4, 64, 71, 14 only because it copied the same clamp.
  Holding discharge flat while stage rises nearly 3 ft is not a hydrographic practice anyone could defend.
  Extending the rating (and flagging it) is the standard move, and it is what both runs did, independently.
- Classification: **wrong criterion (golden defect)**, not an analytical loss and not a run-side defensible
  alternative. The golden's value is the indefensible one. Note also that even after the golden is corrected,
  extrapolation is itself a fork (June 83 linear against 84 power law). So the fix belongs in the pack, not just
  in the golden (see Route).

## Run 1
- Committed: "Place Brennick Water's 2027 atrazine cost-share program in Fennick Creek ... Fennick 45 estimated
  source-removal days, versus 0 for each other sub-watershed", **LANDED**
- First wrong step: the earliest graded departure is step 5's Dunmore flow ("extrapolated 189 high-stage Dunmore
  intervals using power laws fitted to the rating tables", reporting Dunmore May 70 and June 84 against the
  golden's 64 and 71). That is the golden defect above, not a run error. The first genuine departure is at
  golden step 3. The run built a fitted source-tagged transport model ("41 layers and 1,699 three-hour steps"), and
  "Fennick receives every exceedance except May 29-30, producing 45 days. The May pulse remains unresolved"
  (observed 6.78 and 6.40 ug/L against predicted 2.721 and 2.224). It counted Fennick only where Fennick's
  *modelled* contribution cleared the margin, and it left the residual unattributed ("Model residuals ... were not
  redistributed among watersheds"). The golden does the presence test: the lake was stratified from 27 April and
  Fennick's water alone entered the intake's layer, so without Fennick only the spring residue (at most 0.21 ug/L)
  remains. On that test, 29 and 30 May count too.
- Class: `none_landed`, because the run made the decisive stratified-routing judgment (rung 3) and named Fennick
  with every rival at 0. Its 12 lost points on the count come from stopping one inference short on the May pulse:
  the run's own routing put no other tributary's water in the intake's layer, so the unexplained residual could
  only be Fennick's. That is a deep-chain shortfall, not a defensible alternative: the 4.5 m entry-depth separation
  of every other tributary (DESIGN_NOTE `## Ladder`) rules out another source. One-fact test: none would rescue it
  short of handing over the presence logic itself.
- Points lost by cause: deep step 12 (criterion 2, 45 against 47), surface 0, formatting 0, wrong criterion 10
  (criterion 4)

## Run 2
- Committed: "Do not award the 2027 cost-share program on these records alone ... Fennick Creek is the leading
  intake-pathway hypothesis, not a demonstrated winner", with every count "Not identifiable", **NO_CALL**
- First wrong step: golden step 3. Every earlier graded step matched the golden: 47 exceedance days, the
  confirmation-first rule, Tessel/Fennick/Oxley loads, carbon 3,243 / 25,024 / 23,776 / 3,693. Dunmore 70/84 is
  the golden defect again. The run built the buoy profiles and intake depth and found the signal: "Corrected
  intake-depth temperature matches plant temperature with 0.2288 C RMSE, compared with 5.7343 C for whole-lake
  temperature", and Fennick's "June-August match to raw-water temperature is strong, at 0.2675 C RMSE". It then
  explained that signal away: "This supports selective intake geometry, but does not identify chemical source
  fractions or transport histories", and "Award Fennick from temperature similarity alone ... does not establish its
  atrazine contribution on each trigger day". It never placed each tributary at its entry depth or ran plan 5.1's
  counterfactual.
- Class: `dismissed_own_evidence`, because its own output showed the intake drawing one layer and Fennick's water
  matching it, and it declined to carry that into the routing and count (an unfinished chain as well, but the
  quoted pair is the defining failure). Not `defensible_alternative`: the prompt and plan 5.1 demand a count per
  sub-watershed, and the data separate the candidates (Fennick's entry within 0.63 m of the intake on every
  trigger day, every other tributary at least 4.5 m away). Declaring the counts unidentifiable is not a method that
  gives another answer. One-fact test: no single fact about the data rescues it. The rescuing sentence ("route each
  tributary to the depth of matching temperature") is the deep step itself.
- Points lost by cause: deep step 36 (criteria 1, 2, 3: 18 + 12 + 6), surface 0, formatting 0, wrong criterion 10
  (criterion 4)

## Rubric criteria to edit
- **Criterion 4 (weight 10), wrong.** It grades the golden's clamped-rating figures (4, 64, 71, 14), which no
  defensible method reproduces. Do not just swap in 4, 70, 84, 14: linear against power-law extrapolation still
  forks June (83 against 84). Fix it in the generator so that DC-04 stages stay inside the rating. Either extend
  both ratings' tables past the season's peak stage (about 8.8 ft) in `DC-04_LB-05_ratings_and_field_visits.xlsx`,
  or keep the generated stages under 6.0 ft. Then rebuild the golden, rerun `verify.py` (which shares the clamp at
  line 242 and should be made to fail on an above-table stage), and let the criterion regenerate.
- **Weight structure (not a wrong criterion, but the root of the score).** The call plus critical components carry
  36 points (criteria 1 to 3). The asks carry 55 (criteria 4 to 9) and read only the station loads and carbon,
  which DESIGN_NOTE `## Ask sheet` deliberately separates from the call ("the call reads none of them"). Both runs
  collected every ask except the defective one.
- Missing: critical component 2 (stratified 27 April to 6 October; Fennick alone in the intake's layer on every
  trigger day) has no criterion.
- Watch item for determinism, not an edit: run 1's fitted-model counterfactual gives 45 against the golden's
  presence-test 47. The data rule the residual out (see Run 1), but `/fix-rubric` should keep the count criterion's
  exactness or add a criterion grading why the days are Fennick's.

## Route
`/fix-rubric task11`. Run 2 is off the call and its 36 lost points sit entirely on the main call, while both runs
collected the asks. Fixing criterion 4 alone moves the average from 66 to 76, away from the bar, so the verdict is
not RUBRIC_EDIT. First fix the DC-04 rating coverage in the generator (criterion 4 above), then rework the asks so
they ride the stratified-routing step instead of the load and carbon arithmetic: for example, the stratification
dates, each tributary's entry depth against the intake by month, or the days above the trigger by month per
sub-watershed. Shift the weight off station loads accordingly. Caution from Mark's record: run 1 landed the deep
step cleanly at a counterfactual 88, so getting the average under 60 needs about 25 or more points off a landed
run. If the reworked asks cannot take that from a run that routed correctly, the honest route is REDESIGN from 2
(`/build task11 from 2`), not further hardening.
