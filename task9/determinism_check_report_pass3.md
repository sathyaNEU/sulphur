# task9 determinism check (Gates A to E), pass 3: closing check on the final cut

Beside `determinism_check_report.md` (pass 1) and `determinism_check_report_pass2.md` (pass 2), both left as
written. Scope: the final `target.zip` (md5 0eca88a59d96b3aaeeac93189ef2f52f) against the cut judged in pass 2
(abc02f617fed2851bdf205acb11cb4eb), and the sentences of `submission.md` edited for N1 to N5 and R2. Only what
those touch was recomputed, on a fresh unzip, with the pipeline rebuilt from it (`scripts/p3/` in the session
scratchpad). Not opened, as before: `golden/`, `golden.zip`, `DESIGN_NOTE.md`, `generator/`, `metadata.json`.

## Verdict

**DETERMINISTIC. Disposition: APPROVE.** Fix location: none.

## The pack

- 23 files in both cuts, the same names; 22 byte-identical.
- `promo_calendar_2026.csv` is the one file that differs, in the `campaign` column only: 62 of 78 rows renamed,
  every `date_utc` and `market` pair identical and in the same order (13 names before, 12 now).
- `prompt.txt` is unchanged (684 characters).
- **No figure in the blocks reads the campaign name.** The calendar enters only the regression of the closing
  paragraph, as one promotion-day indicator by day and market, and both regressions reproduce to the digit on
  this cut (status shares 0.159, -0.054, 0.136, 0.013, 0.195, 0.162, 0.024, s.e. 0.003 to 0.091; replayed shares
  0.101, -0.079, 0.142, 0.033, 0.194, 0.139, 0.023, 0.55 together, trend 2.26 a session).
- **No graded figure, range or the list moved**: costs 0.1023, 0.0667, 0.1671, 0.0288, 0.0723, 0.0246, 0.0186;
  all groups 0.4805; listed 0.4084; months 0.4901, 0.6259, 0.3230; components 0.843, 1.393, 0.0347, 0.4052; list
  stock, promise, price, trend. The Final Recommendation, Supplementary Questions and Critical Components read
  as in pass 2, with every stated range kept.

## N1 to N5 and the April sentence, by the sentences as now written

| Item | Blocks | Recomputed | Status |
|---|---|---|---|
| N1 the arms (market and device, weekday and month effects; the arm's sessions; clustered by day) | held 1.94 (s.e. 0.76), expected 0.44, control 2.04 | 1.94 (0.76), 0.438, 2.04 | rebuilds |
| N2 day by day (a source's share of the day's hours; a request-time group's failed requests over the day's requests) | stock 0.1048, match 0.0212, inside every range, nearest 0.0166 | stock 0.1048, match 0.0212, promise 0.0667, price 0.1650, history 0.0289, trend 0.0720; nothing out of range | rebuilds |
| N3 second-quarter reading | seller 0.024 | 0.0244 (others 0.0963, 0.0622, 0.1534, 0.0250, 0.0642, 0.0137) | rebuilds |
| N4 the direct route | 0.162, 0.029, 0.046, 0.021, 0.018, 0.147, 0.008 | 0.162, 0.029, 0.046, 0.021, 0.018, 0.147, 0.008 | rebuilds |
| N5 first half from 11 January | ranges hold | component 2 at 1.384 (month weights) and 1.393 (quarter weights), inside 1.37 to 1.46; badge 0.0324, inside 0.031 to 0.036 | rebuilds |
| April sentence (R2) | quarter's tests 1.7 s.e. from the mart, all nine 0.4 | 0.4381 against 0.4115 (s.e. 0.0157): 1.70; 0.4052: 0.40 | rebuilds |

N4's inputs, for the record: shares stock 6.42, price 10.65, trend 8.11 per cent (14 chains, 5 price sources and
24 partitions counted once over the quarter's session hours), promise 5.58, history 1.61, seller 23.43, match
0.80 as the status record gives them; the September test pooled over markets and devices 2.526, 0.526, 0.428,
1.289, 0.217, 0.625, 0.978 points.

## Carried from pass 2, unchanged

- R2 stands as the author's choice: the quarter's own tests keep the list and leave four stated ranges (trend
  0.0614, price 0.1806, component 1 at 0.716, component 4 at 0.438); the blocks say so and refuse them on Q, the
  standard errors and now April. It is a precision argument, not a failed check.
- Step 9's count of 157 sets is not verified.

## Optional, no defect

The regression sentence says "promotion effects"; its figures are from one promotion-day indicator. With one
effect per campaign name on this cut the status regression gives seller 0.172 and history 0.011, the replayed
one seller 0.157 and promise -0.090, trend 0.192 to 0.194: the same conclusions, and no graded figure.
