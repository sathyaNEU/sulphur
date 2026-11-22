# task9 determinism check (Gates A to E)

Pack: `task9/target/` copied fresh to `/tmp/determinism-task9-1795359697/target/` (29 files). No `target.zip` exists in the
folder yet, so this check is on the files the zip is to carry. Read: `prompt.txt` and the four answer blocks of
`submission.md`.

- **Verdict:** DETERMINISTIC. Every source's placement (escalation, three plans, monitor) holds on every route the files
  do not rule out.
- **Disposition:** FIX_NOW. This is answer-block work only: four bands widened, three missing convention sentences added,
  two figures corrected. Nothing solvers see changes and no rerun is needed. There is an optional SEND_BACK lever for
  fork F1, covered under Fix.

## Recomputed figures (the blocks' own method on the shipped files)

| Figure | Blocks (band) | Recomputed | Note |
|---|---|---|---|
| Assembly: merchants / ids / merchant-weeks / manifests | 29,580 / 34,148 / 3,360,865 / 2,473, 2,464, 1,764 / 644 pairs | same | exact |
| Retunes | 4.47 (4.41 to 4.52) | 4.47 | 6.156 x 13/4; log cadence is 4 weeks (425 of 425 gaps), projected 2027 pairs average 3.25 |
| Label revisions | 9.98 (9.92 to 10.05) | 9.99 | 7.672 x 13 |
| Bootstrap pairs, book weighted | 259.89 (247.16 net) | 260.12 (247.38 net) | 15.72 reproduced |
| Replicate pairs | 12.73 | 12.74 | 3.57 and 12.87 reproduced |
| Training data (CC1) | 6.62 (6.35 to 7.44) | 6.62 | exact (row-turnover formula, net of seed part, Sep-2026 book) |
| Optimisation noise (CC2) | 6.89 (6.23 to 7.33) | 6.31 to 6.89 (plain tied fit 6.63) | not reproduced exactly; persistence by family 0.66 to 0.98 against the blocks' 0.79 to 0.95 |
| Calendar planned / completed | 90.9 / 87.1 | 90.93 / 87.09 | reproduce only on the 52 refreshes from 28 Dec 2026 to 20 Dec 2027 |
| Rollout lags | 42; 3 to 31, median 14; 6.3 and 28.8; 4.4% reverted | same | the lag is counted from the completion week's Monday |
| Pinned views (CC3) | 55.0 (53.6 to 58.4) | 55.10 | integrated log-normal lag on components, mean slip, 4.4% reversion |
| Leave-one-out referee, recorded | 58.8, 56.6, 59.0 | same | only when the 39 weeks start at the completion week (unstated) |
| Feature releases | 6.65 (6.34 to 6.84) | 6.65 | 4.00 on planned weeks (4.46 on completed dates); 9.70 with 2026's 22 releases carried |
| Shares | 39.1 / 18.6 / 17.3 / 17.2 / 7.8 | 39.6 / 17.4 / 17.6 / 17.4 / 7.9 (with my 6.63) | in band |
| Record, 13-gap mean square | 509.15 | 509.15 | **only with a 26-week burn-in after each family's last rollout** (494.08 without) |
| Merchants' own share | 43.9 (41.8 to 46.0) | 44.1 | 49.2 from July 2024 reproduced |
| Weekly check | 42.34 | 42.65 | the ordering against 279.06 and 270.43 holds |
| Reflex own share / training data share | 14.2 / 62.5 | not reproduced / 62.5 | 14.2 not reached under four combinations (8.3, 22.3, 5.3, 7.0); not graded |
| Tier changes 2027 / removed | 14.0 (13.6 to 14.2) / 9.7 (9.4 to 10.0) | 13.93 / 9.73 | 2026 pairs 14.82 |

## Forks run

| # | Choice | Alternative | Result | Ruling |
|---|---|---|---|---|
| F1 | Standard 3.2, "the expected movement over the four snapshot pairs" | the mean of the four pairs' RMS, against the blocks' root of the mean mean-square | Feature releases go from 6.65 to **5.96** on the blocks' route. Neighbours: plug-in 5.84, linear 5.70, by-group 5.71. Pair mean squares are 106, 48, 15 and 7. Training data 6.59; the other sources are unchanged. Feature-release share about 14.4 | **Band fork** (a reading of a filed sentence). The call holds, 0.2 to 0.46 above the 5.5 line. The routes that cross the line are ruled out by filed facts: pooled lag 5.48 (lags run 4 weeks at zero components against 26 at five), no reversion 4.87 to 5.48 (manifests show 4.4% of the 26 weeks after first use reverted) |
| F2 | "Settled warm weeks": where they start | from each family's last rollout first use, with no burn-in | Record mean square 494.08. Own share **41.2 to 41.6**. Optimisation noise 6.81 to 6.95 | **Band fork plus a missing rule.** Not refuted: the 26 weeks after the last first use run *lower* than the later weeks (ratio 0.91 at gap 13 and 0.905 at gap 1, book weighted) |
| F3 | Same choice | 2026 weeks only | own share 44.8 to 46.2; optimisation noise 5.96 (20 gaps) to 6.47 (26 gaps) | 46.2 is above the 46.0 top. 5.96 is below the 6.23 floor and still a plan |
| F4 | "2027's weekly retrains" | calendar 2027 (4 Jan to 27 Dec), against the blocks' 28 Dec 2026 to 20 Dec 2027 | blocks' route 56.9; plug-in median lag 58.8; planned weeks 92.9 | **Band fork plus a missing sentence.** The referee does not rule out the plug-in route: its mean absolute error is 1.0 against the integrated route's 1.6 (57.6, 58.1, 58.7 and 56.1, 56.5, 57.1 against 58.8, 56.6, 59.0) |
| F5 | Lag model form | log-linear, linear, by group, by family; integrated or plug-in | pinned 55.1 to 58.6 on the pair window; feature releases 6.35 to 6.65 | in band. Pooled lag (57.5 to 59.4; 6.26 to 6.49) is ruled out by the component split |
| F6 | Slip from planned week to completion | mean, median, by family | pinned 55.1 to 55.5 | in band |
| F7 | Reversion | applied to all weeks, the first 26 weeks only, or none | pinned 55.1 / 55.6 / 57.6 to 58.0 | in band |
| F8 | Gap fit | 20, 26 or 30 gaps; unweighted, 1/y or 1/sqrt(k) weights; a quadratic term | 6.31 to 7.15 | in band and a plan. Fits with a free intercept give 6.12, below the floor. I rule them out because the score changes nothing at gap 0 |
| F9 | The persistence term free of the replicate pairs | free amplitude | 9.81 to 11.91; implied replicate 21.5 to 28.4 against 12.74 measured | ruled out by the replicate pairs (the blocks' own refutation reproduces) |
| F10 | Bootstrap seed part | gross, not net of the replicate pairs | 6.77 | in band |
| F11 | Turnover formula | the full three-term form, simple (out+in)/(N1 N2), or a per-pair noise level per row | 6.62 / 6.62 / 6.62 | in band |
| F12 | Book weights | the planned Dec-2027 book in place of Sep 2026 | 9.99 / 6.62 / 6.64 / 6.54 / 4.47 | in band |
| F13 | Retunes per pair | 3 per pair, read off the truncated 2026 log | 4.30 | ruled out: the 4-week cadence projects 3.25 a pair (42 pairs with 3, 14 with 4) |
| F14 | Releases dated on a snapshot Monday (FR-27-18, FR-27-24) | sent to the next pair, or FR-27-24 dropped | 6.63 / 6.63 | in band |
| F15 | Tier test, the strongest rival | per-merchant Gaussian tier-crossing on the panel's quarter-end scores | 2026: 14.56 to 14.86 (recorded 14.82); 2027: 13.70 to 13.99; removed 9.59 to 9.85 | in band |
| F16 | Tier aggregation | panel-merchant weights or book weights | 13.93 / 9.73 for both | in band |
| F17 | Strongest rivals on the call | bootstrap at face value (15.72), replicate at face value (3.57), calendar dates (4.00 / 4.46) | each refuted by a computed figure: the weekly check (the record 42.65 against 279.06 and 270.43, and 50.92 on the replicate route) and the referee | not forks |

Gate B passes. Every distinctive term of the recommendation is in a shipped file. The five sources and the band
names are in standard 1.2 and 4.1, the cap and the snapshot Mondays are in schedule C2 and C3, the pinned views are in
calendar PC-26-058, the components are in the registry, and the rollout dates come from the manifests' options. Gates D
and E pass apart from F1 and F4. Both are one-word or one-clause readings, and both are closed below by bands that
admit them.

## Fix (location: solution; nothing solvers see changes)

1. **F1 (feature releases).** Widen the points band from "6.34 to 6.84" to **5.70 to 6.84**. Widen the feature-release
   share band from "16.0 to 18.4" to **13.4 to 18.4**. Make both edits in Supplementary Questions 1 and wherever
   step 5 states them. The optional cleaner fix is a SEND_BACK, because it changes the pack and needs a rerun: add
   one clause to `gms_model_stability_standard_2026.pdf` 3.2 such as "the root of the mean of the four pairs'
   mean-square changes". That restores the margin to the 5.5 line on every reading.
2. **F2 and F3 (settled weeks).** Add a sentence to Step-by-Step 6 saying where each family's settled weeks start: 26
   weeks after the last of the three rollouts first reached it, or whatever rule the build uses. Widen the merchants'
   own share band from "41.8 to 46.0" to **41.0 to 46.5**. Lower the floor on Critical Component 2 and on
   Supplementary Questions 1 optimisation noise from "6.23" to **5.90**, which is still clear of the 5.5 line.
3. **F4 (pinned views).** Add to step 5: "2027's retrains are the 52 weekly refreshes of the four snapshot pairs
   closing in 2027, 28 December 2026 to 20 December 2027". Raise the top of the band on Critical Component 3 and
   Supplementary Questions 2 from "58.4" to **59.0**.
4. **Optimisation-noise fit spec (6.89).** Step 4 states only the persistence term. Add the companion terms, the gap
   range and the weighting that produce 6.89 and a persistence of 0.79 to 0.95. On a plain linear-plus-persistence fit
   I get 6.63, with persistence 0.66 to 0.98.
5. **Figures that do not reproduce.**
   - In step 7, 42.34 recomputes to **42.65**. Correct it or state how it was computed.
   - In step 6, the reflex route's 14.2 per cent merchants' own share does not reproduce. Restate how it is computed or
     correct it.
   - In step 5, the referee's "first 39 weeks" should say they count from each family's completion week.
   - In step 5, "4.00 on the calendar's dates" is the planned weeks. The completed dates give 4.46. Pick one wording
     and keep it the same in the Final Recommendation.
