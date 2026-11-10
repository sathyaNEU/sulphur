# Run triage, task10 (architecture 6), 2026-11-10
**Verdict:** REDESIGN
**Scores:** run 1 not supplied (estimated 95 to 100), run 2 not supplied (estimated 93 to 100), average about 97; counterfactual about 100, 100, average about 100
**Spread:** run 1 lost 0 results to 0 deep classes, run 2 lost 0 to 0; no deep loss anywhere, so neither spread nor concentrated: the chain was earned end to end by both runs

Inputs: `runs/arch6_run1.md` and `runs/arch6_run2.md` (verbatim). No `runs/rubric.md`, no per-criterion grades and no
scores were supplied; the author reports both runs landed with nothing lost. Every figure below is checked against
`submission.md`'s bands and the design note's `## Results chain`, so the estimated scores rest on that comparison and
not on a rubric. Neither the missing rubric nor the scores could move the verdict: the runs sit inside the golden's
bands on every graded figure but one, and that one misses by 0.1 MW.

## Loss map

Weights are not known (no rubric). The grade is what each run's stated figures earn against the golden's bands.

| ID | Golden (band) | Run 1 | Run 2 |
|---|---|---|---|
| R1 demand before flex | 30.1, 24.9, 35.5, 22.9 (0.3 each side) | earned: 30.1, 24.9, 35.5, 22.9 | earned: 30.3, 24.9, 35.6, 23.0 |
| R2a share of contract available at -3.0 C | 0.39 Corvane (0.36 to 0.45), 0.54 Quillon (0.50 to 0.59) | earned: "37.9% for Corvane and 53.1% for Quillon" | earned: zone by zone 38.3% and 38.2% (Corvane zones), 50.9% and 54.0% (Quillon zones), all inside |
| R2 MW delivered 17:30 to 18:00 | 8.1, 4.0, 5.4, 2.9 | earned: 8.0, 4.0, 5.3, 2.8 (two-interval means) | earned: 8.0, 3.8, 5.4, 2.9 |
| R3 backtest average miss | 0.19 (0.10 to 0.29) | earned: 0.19 | earned: 0.13 |
| R4a come-back per MW delivered | 0.32, 0.26 (Component 2) | earned in effect, coefficient not stated: "Applied the estimated service shape and post-window rebound"; Ashcombe moves to 20:00 | earned in effect, coefficient not stated: "added the observed-pattern rebound through 21:30"; 22.2 MW at 18:00 against 25.9 at 20:00 |
| R4 MW off the day's peak | 4.2, 4.0, 5.4, 2.9 | earned: 4.2, 3.9, 5.2, 2.9 | earned: 4.3, 3.7, 5.3, 2.9 |
| R5 expected peak | 25.9, 20.8, 30.1, 20.0 | earned: 26.0, 21.0, 30.3, 20.0 | earned: 25.9, 21.2, 30.3, 20.1 |
| R6a spread as share of delivery | 16 per cent (Component 3) | earned in effect, share not stated: bootstrap plus predictive draws; Fenwick P90 31.3 | earned in effect, share not stated: "proportional delivery variability" carried to the enlarged fleets; Fenwick P90 31.3 |
| R6 nine-days-in-ten level | 26.5 (26.1 to 27.0), 21.7, 31.2, 20.6 | earned: 26.7, 21.8, 31.3, 20.8 | earned at three, near miss at one: 27.1 at Ashcombe Road, 0.1 over the printed band but inside the note's own extension ("0.3 MW above it for a rebuild on another baseline"); 21.8, 31.3, 20.6 |
| R7 the set | Ashcombe Road, Fenwick Street, Hartwell Common | earned | earned |
| R8 bridge | per zone contracted, not available, delivered, come-back, off peak; totals 46.0, 25.6, 20.4, 16.5 | earned in substance, partly as reported: contracted to delivered to off peak per zone with the availability share and the come-back named in words; no four-zone totals, no labelled come-back bar in the response text | the same: contract, availability, delivered, off peak per zone; no totals or labelled come-back bar in the text |

The workbooks were not supplied, so R8's bars, the R4a coefficient and the R6a share may well be on the runs'
Contract Bridge, Profiles and Models sheets. The prompt never asks for either coefficient. Wherever these three show
as partial, the cause is reporting, not analysis.

## Moves the note priced as lost that both runs made unprompted

The note's careful-but-hurried column has R2a, R4a, R6a, R6 and R7 as Missed and R2, R4, R5 and R8 as Partly, and
forecasts about 4 of 11. Both runs earned all 11 in substance.

1. **R2a, the capped availability ceiling** (forecast as a method shortcut: per MW scheduled, regressed on
   temperature). Run 1: "Fitted a provider-specific, temperature-dependent available-capacity model capped by the
   actual instruction. This avoids treating a successfully delivered small instruction as proof that the full
   registered portfolio is available", and "Instruction caps conceal availability on lightly called days". Run 2:
   "Fitted a temperature-dependent available-capacity ceiling, capped by scheduled MW, rather than assuming a constant
   delivered percentage". Run 2 also chose its model family against the note's own hurried reading: "the chosen
   model's pooled miss was 0.13 MW, against 0.15 MW for a schedule-fraction model, 0.17 MW for a
   temperature-dependent efficiency model". The note's proof chain (equal-temperature test, two zones per provider,
   three winters of stepped-up contracts) was never needed. A min(scheduled, ceiling) model was the first move, once
   the award notice's service terms said calls are sized to need and capped at the contract (hidden factor record,
   row 4).
2. **R2 carried as a share of the contract to the 2027/28 award.** Both runs: Ashcombe 8.0 MW, not the forecast
   10.3.
3. **R3, the backtest with a comparator.** Run 1 reports a "historical delivery-ratio comparator" at 0.48 MW. Run 2
   reports a constant factor at 0.46 and the two rival families above. The note forecast that the held-out winter
   "cannot tell the two readings apart". Run 2 used a chronological validation winter to separate them anyway.
4. **R4a and R4, the come-back and the day rebuilt half-hour by half-hour** (forecast as an unfinished chain: the
   credit taken off the 17:30 to 18:00 peak). Run 1: "Applied the estimated service shape and post-window rebound,
   then found the maximum across all 48 half-hours", and "Rebound moves the modeled mean-profile peak to 20:00". Run
   2: "Applied estimated service delivery across the seven half-hours ending 16:30-19:30, and added the
   observed-pattern rebound through 21:30", and "rebounds to 25.9 MW at 20:00". Both rejected the shortcut by name:
   "Subtract central delivery directly from the original peak" (run 1), "Ignoring peak displacement and rebound" (run
   2).
5. **R6a and R6, a predictive tail carried in proportion** (forecast as a method shortcut: the fit's interval, or MW
   of scatter carried unchanged). Run 1: "The P90 is the predictive percentile of daily maxima, not a confidence limit
   for mean demand", from 250 joint bootstrap fits and 100,000 draws. Run 2: "predictive P90s rather than confidence
   intervals for average demand" and "Enlarged fleets are assumed to retain historical cold-weather availability and
   proportional delivery variability". Run 2 also checked tail coverage on held-out days: "210/222 days, or 94.6%".
6. **R7, Fenwick on the tail and not the mean.** Run 1: "Defer Fenwick because its average peak fits ... The required
   tail test instead gives 31.3 MW". Run 2: "Approving Fenwick on expected demand alone: its 30.3 MW expected peak is
   below 30.5 MW firm, but its 31.3 MW P90 fails".
7. **R8, a bridge with a come-back step.** Both runs bridge contract to delivery to off-peak and attribute Ashcombe's
   gap to the rebound. The note's hurried bridge had "no come-back bar and the per-megawatt credit".

Layer 1 was cleaned by reflex in both runs, and the distractors were inspected and set aside with reasons: the DUoS
statement, the customer interruptions and the transformer condition.

## Run 1
- Committed: "Commit reinforcement at Ashcombe Road, Fenwick Street and Hartwell Common for winter 2027/28; do not
  commit capacity reinforcement at Charlecote Way." LANDED.
- First wrong step: none. Every stated figure sits inside the golden's band. Class: none.
- One-fact test: not applicable, because no sentence was needed. Read the other way, the note's largest hint (the
  share sentence) rescued nothing, because the run supplied it itself.
- Points lost by cause: deep 0, one legitimate step 0, surface 0, formatting up to a few (R8 totals and the come-back
  bar, R4a and R6a coefficients unstated in the text, if the rubric grades them), wrong criterion 0.

## Run 2
- Committed: "Commit reinforcement at Ashcombe Road, Fenwick Street and Hartwell Common for winter 2027/28; do not
  commit Charlecote Way on capacity grounds." LANDED.
- First wrong step: none analytical. The only figure outside a printed band is "27.1" at Ashcombe Road's
  nine-days-in-ten level (golden 26.5, 26.1 to 27.0). Its baseline uses "temperature and the primary's pre-service
  demand level", which is the note's "scaled to the day's own level before the window" variant, and the note's R6
  band admits 0.3 MW above the range for such a rebuild. Class: `near_miss_or_formatting`. It does not move the call:
  27.1 and 26.5 are both far over 23.0 firm.
- One-fact test: not applicable, the same as run 1.
- Points lost by cause: deep 0, one legitimate step 0, surface 0, formatting up to a few (the R6 Ashcombe 0.1, R8
  totals, R4a and R6a coefficients unstated), wrong criterion 0.

## Counterfactual reading

No run lost points to an analytical cause, so the counterfactual (every surface, formatting and wrong-criterion point
returned) is about 100 for both runs, average about 100. The actual average is unknown but cannot sit near 60. The
note's pair estimate of 38.4, and the 49 for the "carries the scatter in proportion" variant, were wrong by roughly
60 points.

The diagnosis is a calibration error in the careful column, not a fork or a plant:
- All three constructed mechanisms (the availability ceiling, the come-back and the proportional spread) are carried
  visibly by the rows, and both runs modelled each one on sight. That is the house caution: "A mechanism the rows
  visibly carry is modelled on sight".
- The careful column was calibrated to the architecture 5 runs, which faced a different pack and prompt. It assumed
  those runs' estimator would recur. It did not: with a contract cap filed in the award notice and three asks that
  separate delivery from peak relief, a frontier run's default is a capped ceiling, a whole-day profile and a
  predictive P90.
- The prompt's ask structure points at the chain. It asks for "the MW its 2027/28 contract will deliver at 17:30 to
  18:00" and, separately, "the MW that takes off the day's peak". It asks for "the level it stays under on nine design
  days in ten" (a predictive quantity), and to "walk me from each contract's MW down to the MW off the peak" (which
  tells the run there are losses in between). None of these is a leak of method. Together they still name R2, R4, R6
  and R8 as distinct quantities, and both runs answered each one with the method its wording implies.
- The depth level 5 claim did not hold up: "seven shortcuts land on five different wrong sets" priced nothing,
  because neither run took any of the seven.

## Rubric criteria to edit

No rubric was supplied, so none can be listed against weights. Three points matter if one is generated:
- `submission.md` Supplementary Question 5 prints Ashcombe Road's band as 26.1 to 27.0, while the note's R6 band runs
  0.3 MW above that for a rebuild on another baseline. A criterion built from the printed band fails run 2's 27.1 on
  a variant the golden itself admits. The two documents should agree (the author's edit, not this triage's).
- Critical Components 2 and 3 carry coefficients the prompt never asks for (0.32 and 0.26 MW per MW delivered; 16
  per cent). A criterion that requires those exact figures grades a quantity outside the prompt. The figures the
  prompt does ask for (the 20:00 peak and Fenwick's 31.3) are what both runs reported.
- None of these moves the verdict. Fixing all three only raises the runs' scores.

## Precedence note

Taken literally, a counterfactual average of 60 or more triggers `SURFACE_RISK`. But no loss here has a surface
cause, and there is no row, factor, field or sentence to name as the trigger. The runs lost nothing, and they lost
nothing because they did the deep work. `FIX_DETERMINISM` does not apply: no run took a defensible alternative that
changes a result, and both landed the golden. `FIX_ASKS` does not apply: no run lost the call or the components to a
deep class. `REDESIGN` is the clause that fits: the counterfactual average is 60 or more and the only losses were
surface and formatting.

## Route

`/build task10 from 2`. Add a `## Tried and rejected` line for architecture 6: the capped availability ceiling, the
rebound with a whole-day peak and the proportional predictive P90 were all modelled unprompted by both platform
runs, average about 97. Recalibrate the careful column to these two runs, not to architecture 5. Two things are
worth keeping, as in the architecture 5 audit: the demand side and the world. A re-rooted chain needs results whose
difficulty survives a run that fits a capped, temperature-dependent ceiling, rebuilds the 48 half-hours and draws a
predictive tail, because that is now the measured default. Results whose only difficulty is one of those three moves
count as Right in the careful column.
