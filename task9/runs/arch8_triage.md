# task9 architecture 8: where the two platform runs lost (main-thread loss map, 2026-11-11)

No scores and no rubric were supplied with the two runs, so this is the loss map against the golden's bands, read
from the run texts (`arch8_run1.md`, `arch8_run2.md`) and the platform's holistic audit (`arch8_holistic_audit.md`).
It is not a `/triage-runs` report.

| Result | Golden | Band | Run 1 | Run 2 |
|---|---|---|---|---|
| R1 3-month average per sale, per USD 100,000 a point | 284,000 | 282,000 to 287,000 | 281,000, out by 1,000 (a log-ratio rebuild; the audit calls it defensible) | 282,000, in |
| R2 3-month worst calendar year | 2008, 16,154,000 | 15,650,000 to 16,390,000 | 2008, 16,336,000, in | 2008, 16,389,000, in |
| R3 12-month peak collateral at USD 50,000 | 25,876,000 | 25,800,000 to 26,500,000 | 25,877,000, in | 25,876,000, in |
| R4 3-month size, limit and day | 114,400, collateral, 20 Nov 2008 | 100,000 to 117,000 | 111,500, collateral, 20 Nov 2008, in | 111,000, collateral, 20 Nov 2008, in |
| R5 6-month size | 58,700 | 54,000 to 59,000 | 57,500, in | 57,300, in |
| R6 12-month average's 80% range | 63,000 to 552,000 | low 14,000 to 82,000, high 537,000 to 616,000 | 73,000 to 539,000, in | 69,000 to 539,000, in |
| R7 3-month average's 80% range | 143,000 to 413,000 | low 131,000 to 159,000, high 399,000 to 436,000 | 146,000 to 409,000, in | 147,000 to 410,000, in |
| R8 open swaps' expected 2027 settlement | 2,494,000 | 2,390,000 to 2,890,000 | 2,618,000, in | 2,487,000, in |
| R9 its 80% range | 394,000 to 4,247,000 | low 200,000 to 420,000, high 4,100,000 to 4,430,000 | low 738,000 out, high 4,249,000 in | low 92,000 out, high 4,237,000 in |
| R10 2027 plan by ladder | 12-month 2,809,000; 3-month 2,919,000; sleeve 5,728,000 | 2,705,000 to 3,205,000; 2,530,000 to 3,030,000; 5,235,000 to 6,235,000 | 2,933,000; 2,824,000; 5,757,000, all in | 2,802,000; 2,818,000; 5,620,000, all in |
| R10 the plan's 80% range | -4,203,000 to 12,204,000 | low -4,300,000 to -1,900,000, high 11,200,000 to 12,400,000 | +153,000 to 10,976,000, both out | -3,412,000 to 12,064,000, both in |
| R11 recommendation | 114,400 a point, plan 5,728,000 | R4 and R10 bands | in | in |

**First wrong step.** Neither run took an analytical wrong step. Every loss is a defensible alternative on a
result the golden left loosely pinned: run 1's log-ratio rebuild of the early 3-month strikes (R1), and both runs'
forecast bases for the predictive ranges (run 1 a vol-scaled joint replay with entropy-tilted probabilities, run 2 a
ratio replay on 225 monthly origins), which the audit also names. Class on the client's table: defensible
alternative (not deterministic) on R1, R9 and R10's range; nothing else lost.

**What the runs did unprompted.** Two-sided log-ratio rebuilds of the missing 3-month, 6-month and 9-day histories,
validated on held-out overlap days; total-variance interpolation chosen by fit to the dealers' marks; the cap applied
before sleeve-wide netting; every daily and annual ceiling solved; circular block bootstraps at three block lengths;
expected settlement from realised against implied variance on the whole record; joint replays for every range;
purged chronological validation and coverage checks (run 2 measured 74.7 to 78.7 per cent coverage). Run 2 inspected
the skew and vol-of-vol files and set them aside as non-contractual; run 1 tested a constant 0.25-point dealer
overlay as a sensitivity.

**Verdict.** REDESIGN, re-rooted at the author's word (2026-11-11). The platform's audit found that a careful,
competent build reaches the headline answers. Measured in the main thread on the real series before the re-root: the
one judgment the world still offers, a stressed dealer basis tied to the skew index (the jump term a variance swap
prices and the 30-day index omits), moves the 3-month size from 114,400 to about 104,000 with the binding day
unchanged, and a plain proportional markup fitted on the dealer window lands at 104,500 by the coincidence of the
skew index's secular rise and the crisis volatility levels; the cap fixes the binding-day collateral of every
3-month swap open on 20 November 2008 at 2.625 times its strike. The world is spent: architecture 9 moves to another
world, another dataset and another shell.
