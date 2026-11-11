# Run triage, task16 (architecture 1), 2026-11-11
**Verdict:** REDESIGN (re-root: the world is spent on this run)
**Scores:** run 1 not supplied (estimated 93 to 100), run 2 not supplied; no rubric and no per-criterion grades
**Spread:** run 1 lost 0 results to 0 deep classes; the chain was earned end to end

Inputs: `runs/arch1_run1.md` (verbatim, pasted by the author with the note that the task "never stumped"). No second
run, no `runs/rubric.md` and no scores were supplied, and the run's workbook was not supplied. Every figure below is
the run's own stated figure checked against `submission.md`'s bands and the design note's `## Results chain`, so the
estimated score rests on that comparison. Written in the main thread from the one run; `/triage-runs` was not typed,
so no `run-triage` thread was spawned. A second run could not move the verdict: the design note priced this run's
path as losing 3.5 of 6 results and it lost none.

## Loss map

| ID | Golden (band) | Run 1 |
|---|---|---|
| R1 the trial's benchmark loss | 0.685 (0.680 to 0.690) | earned: "0.6848, using the mean of its three completed seeds" |
| R2 cost per tenth, contractor | 0.0020 (0.0005 to 0.0032) | earned: 0.0021 |
| R2 cost per tenth, map transfer | 0.0114 (0.0095 to 0.0125) | earned: 0.0115 |
| R3 the level at 512,000 expert labels | 0.600 (0.595 to 0.613) | earned at the band's edge: 0.5953 |
| R4 expected loss, A | 0.661 (0.650 to 0.720) | earned: 0.6751 |
| R4 expected loss, B | 0.625 (0.615 to 0.650) | earned: 0.6341 |
| R4 expected loss, C | 0.670 (0.648 to 0.689) | earned: 0.6533 |
| R4 expected loss, D | 0.680 (0.660 to 0.697) | earned: 0.6657 |
| R5 four-in-five range for the pick | 0.604 to 0.645, half-width 0.021 (low 0.580 to 0.640, high 0.625 to 0.690, half 0.010 to 0.040) | earned: 0.618 to 0.650, half-width 0.016 |
| R6 the configuration to name | B | earned: B, C the runner-up |

The one loss is instruction following: the prompt asks for a spreadsheet and a short note, and the run filed the
workbook alone. That is a surface loss, given back in any counterfactual.

## Moves the note priced as lost that the run made unprompted

The note's careful but hurried column had R3, R4 and R6 as Missed and R2 as Partly (2.5 of 6 earned, pair 46.5).

1. **R1, the yardstick** (priced Right for the careful column, and it was): "An affine calibration using expert-only
   development loss had leave-one-out RMSE 0.006108, compared with 0.020493 using mixed-source development loss."
   Two candidate calibrations, one cross-validated number each, the better one kept. A comparison of candidate
   methods by held-out error is this run's reflex.
2. **R3, the level past the expert pool** (priced Missed: one scaling curve through every run, its form chosen on
   held-back runs, carried on). The run saw the bend in matched cells: "at width 128 and 75% map-transfer labels,
   the improvement from 128,000 to 256,000 labels was 0.0471 expert-development loss units, but the next doubling
   improved loss by only 0.0274", fitted a response surface "allowing sample-size gains to slow after a fitted
   breakpoint", and checked it on held-out configurations ("held-out 512,000-label error was 0.008736, versus
   0.036258 for a straight log-size trend"). The trial design carried the same mix at three totals, so one group-by
   of one table showed the slowdown, and the hold-out the run always does confirmed it.
3. **R4 and R6, the forecasts and the pick** followed from 2: with the slowdown modelled, B leads C by 0.019. The
   run names the shortcut's answer itself: "Straight log-size extrapolation favors C".
4. **R5, the range** (priced Partly): configurations resampled whole, calibration pairs resampled separately,
   fresh-run and transfer error added, "Seed variation was not added twice". Inside every band.

## Why the design failed (the designer's reading, for the next draw)

- **Everything hard sat in one table that one flexible model absorbs.** Runs by (size, width, rate, route shares)
  is a regression table. A response surface with a breakpoint, validated on held-out configurations, earns the
  level, the costs, the forecasts and the pick at once. The six results were one fit read six ways.
- **The asks were the decomposition.** The prompt asked for the trial's benchmark loss, each route's cost per tenth
  and the 512,000 level by name, so the run was told which intermediate quantities to build.
- **The difficulty was a method preference, not a bias.** Sound methods differed by 0.01 to 0.03 on effects of the
  same size, so determinism forced bands wide enough to hold almost any careful analysis (C from 0.648 to 0.689,
  A from 0.650 to 0.720). A band that wide grades nothing.
- **The two risks named in the build were the two that landed**: the calibration comparison and the matched-share
  cells. The paper pair of 46.5 priced the careful column below what the run record already showed.

## What the next draw takes from it

Calibrate the careful but hurried column to this run: it reads every file, compares candidate methods by held-out
error, fits breakpoints and response surfaces, validates on held-out groups, resamples clusters and keeps variance
components apart, all unprompted, in under half an hour. A result survives only where that battery is run on the
wrong population or the wrong quantity and still comes back clean: who is in the data, what was measured, whether
the units in hand are the units the answer is about. Those are bias judgments with large, estimable corrections
(tight bands), they do not sit in one table, and same-sample validation cannot flag them.

## Route

REDESIGN, taken as a re-root (`build-pipeline`, Re-root): the run killed the version it replaces, the world's chain
is spent (no tighter honest band fails this run, since its figures sit as close to the author-side truth runs as the
golden's), so architecture 2 is drawn in another world, another dataset and another shell in the same subdomain
group and number.
