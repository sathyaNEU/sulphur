# The client's 15 accepted Sulfur tasks

The client rebuilt its example library from tasks that stumped the models for reasoning reasons
(`guidelines/client/examples/1.txt` to `15.txt`, index in `examples.txt`). In each one the runs cleaned the data and
read the instructions correctly, often noticed the key issue, and then lost on judgment. Read two or three in or near
the draw's domain before designing, **for the depth, never the template**: two tasks on the same pattern with the same
data structure are duplicates. How to write the prompt itself is learned from `mark-prompts.md`.

Scores are the frontier-model average (eight runs where marked /8, else the two graded runs). The label column is the
strategy's label in `../../stumping/references/sulfur-strategies.md`.

| # | Subdomain, objective | Score | The deep step | How the runs failed | Label |
|---|---|---|---|---|---|
| 1 | Product Analytics, root cause | 0.26/8 | composition against behavior: margin by each customer's use count, open returns projected to maturity first | explained it by basket shape, held the mix flat despite its own trend, sized the recovery at a third | WORKS |
| 2 | Marketing, incrementality | 0.46 | a push outage on the same app build contaminates the cohort contrast; the ratio calibrated only on members the offer never reached | raw contrast, contaminated calibration, the wrong functional form | WORKS IN FORM |
| 3 | Marketing, media mix | 0.45 | search spend follows demand; an unlabeled off-week test read as a difference against the other weeks | trusted the agency's curves, refit on the same confounded variation, dismissed the test | WORKS IN FORM |
| 4 | Banking, causal | 0.24/8 | states waiting for rollout got the freed collector time, so excluding them doubles the lift | applied the standard's form literally, named the spillover then deferred to the standard, treated the gaps as confirmation | WORKS |
| 5 | General Statistics, forecasting | 0.45/8 | customer-specific, opposite-direction market responses validated by a chronological back-test | a shared market term, dropped a pooled term as harmful, stress tests inside the pooled structure | WORKS IN FORM |
| 6 | Healthcare Delivery, program evaluation | 0.57/8 | areas were started worst-first, so only concurrent controls matched by size band and month, weighted to the service's mix, work | each area's own baseline, pooled controls, computed the right figure then discarded it | WORKS IN FORM |
| 7 | Economics, causal identification | 0.55/8 | a rider-weighted long-run instrumented elasticity by system size | a pooled same-month estimate, computed the weighted figure and left it unused, a sensitivity grid on one number | WORKS IN FORM |
| 8 | Economics, spillover | 0.40 | unlabeled leader-follower pricing pairs; a control group that excludes the followers | ranked by own volume, looked for spillover by geography, used a contaminated control | WORKS IN FORM |
| 9 | Psychology, latent structure | 0.36 | a board distribution fitted by EM and validated on unselected full boards | the textbook formula, validated on selected rounds | UNTESTED |
| 10 | Psychology, censoring | 0.43 | quick-round timeouts treated as right-censored per-child slopes | dropped the timeouts, censored the unrelated practice timeouts too, set the evidence floor by caution | WORKS IN FORM |
| 11 | Political Science, measurement error | 0.28 | each slope disattenuated by the reliability of its district shares | raw slopes, robustness checks that cannot catch it | WORKS IN FORM (ships 5 files, below the 10-file minimum, by the client's own note) |
| 12 | Economics, sample selection | 0.45 | the offer changed who has a wage, so bounds | wages compared among workers only, covariate adjustment, unsupported selection-model assumptions | DOES NOT WORK as the golden (the client calls the chain short) |
| 13 | Urban, policy impact | 0.44/8 | the cities were diverging before the rule, so a listing-cohort comparison | scaled the aggregate, re-ran on a log scale, found the cohort result then set it aside | WORKS IN FORM |
| 14 | Education, program evaluation | 0.59/8 | standard errors clustered on the 84 allocated schools | default and robust errors | DOES NOT WORK (the client calls it "closer to a single-insight task"; 0.59 is one point under the bar) |
| 15 | Education, variance components | 0.50/8 | a cohort-to-cohort variance term beyond sampling noise | read the bad cohorts as data bugs, kept one variance model throughout, accepted 15 schools as credibly below | WORKS |

**What the library shows, across all 15.** The first wrong step is always a method shortcut, an unfinished chain,
dismissed evidence or a self-confirming check; in examples 6, 7 and 13 a run computed the right figure and set it
aside. Planted-looking defects sit in examples 1, 4, 13 and 14 and decided nothing, because no run got far enough for
them to matter. The two weakest by the client's own notes (12 and 14) are the two whose deep step is one named method,
which is Mark's law 1.1b seen from the client's side.
