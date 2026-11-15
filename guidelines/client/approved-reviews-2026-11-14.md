# Review sheets of three approved tasks by other fellows, read 2026-11-14

Kept verbatim as the client's own review text, pasted by the author on 2026-11-14. None of the three is ours. They
sit beside `project-lead-review-2026-11-09.md` and `depth-scale-2026-11-09-detail.md`: the bar to beat and never a
skeleton to copy. The skeleton guard holds all three (`.claude/skills/fingerprint/corpus/client_skeletons.json`,
ids `review:2d1b99c1`, `review:52ab454f`, `review:d311cbf0`) and refuses a draw that reskins one. What the house
learned from them is `.claude/skills/stumping/SKILL.md` Part 1d.

What the sheets show about the review itself, in the reviewer's own terms:
- **Stumped** rests on a single usable GPT-6 Astra run read against the generated rubric (rewards 22, 17 and 35
  here; our returns of 2026-11-13 came back at 83, 78, 75 and 71).
- **Determinism (main)** is a blind fork audit (12 forks on one sheet), an independent replay of the golden with
  variants, and a ruling on every plausible rival by a figure computed from the shipped files.
- **Determinism (supp)** and **Solution (supp)** reproduce the committed figures inside their bands and check that
  one figure reads the same everywhere and that every rule the golden used is written in the Step-by-Step.

---

## Task 2d1b99c1-2bc7-4b21-8d9c-806d5ded9579

Fellow ID dcc9ec70-ac69-4e6f-af0d-076fcc754b47. Reward 22. Prelim verdict: Approved, Vincent will fix.

**Stumped.** passed (single usable GPT-6 Astra run scored 0.22 < 0.60 Sulfur bar; thin evidence, gate rests on one
run)

**Determinism (main).** passed with medium confidence: wave four goes ahead is the answer the data supports. Basis
is pinned by the prompt (September churn without the price change is the all-account headline rate, so annual movers
are counted in the base: the monthly-plan-only reading gives about +0.30 and is the known trap). Independent check
on the notified June 1 monthly cohorts in the 17 priced markets (python -I, run workbook cohort cells reconciled to
the KPI pack 68,803/2,885 and 62,877/3,482): the same-market Jun-Oct minus Feb-Jun change in 2026 against 2024 and
2025 gives September churn effect about +0.001 of cohort (golden -0.5 pts of cohort) and paying-at-1-Sep effect
about -0.078 (about -1,950 vs golden -1,737). The History shows the planted tenure-widening September swing (monthly
voluntary Sep/May ratio about 1.0 at 0-3 months to 1.9 at 24+ in 2025; 3.2 in 2024). The rival hold reading (Astra
run +0.625 via triple difference vs AU, NZ, ZA, IN, SG) rests on five small southern or tropical controls (about
3,200 accounts per cell) whose Jun-Oct 2026 churn fell about 1.2 pts for no shipped reason, has a placebo of its own
that does not validate seasonal comparability by tenure and climate, and reports its own 95% interval of -0.23 to
+1.48 straddling the 0.134 line. Blind fork audit landed 'probably waits' only through the monthly-only reading and
left basis and control forks open (not a full solve).

**Determinism (supp).** passed: headline rates, annual renewals (BTR25 440 of 859 left, 51%), Tillwave recovery
(about 25 to 27% vs 60 to 64%) and notified cohort counts reproduce; pieces 0.75 / 0.40 / 0.17 / -0.19 / 0.26 /
-0.04 inside bands

**Solution (main).** passed: golden call (go ahead, price about -0.04) is the answer the evidence supports

**Solution (supp).** passed with Vincent-fix: golden text says 1,580 in the steps and 1,577 in the memo; -0.035 vs
-0.04 rounding; state the convention; add the controls-unsuitable reason with a figure

**Duplicate.** passed

**Task type match.** passed: subscription churn attribution with a counterfactual price effect, bridge
decomposition and a launch decision, adjacent to causal-change and decomposition types

**Stumped type match.** passed: deciding step is building the right counterfactual (tenure-specific September swing
and following everyone notified whatever plan they moved to) and rejecting southern or tropical wave 4 markets as
controls; hidden in the data, not a rule application, field reading or replay

**Feedback.** Optional suggestion (not required; this task is approved as is): The package already makes the
notified-accounts counterfactual and the tenure-specific September swing hard to find, so no change is needed for
difficulty. If you want to harden it further without touching the answer, consider (1) adding a market-level climate
or hemisphere field only in the KPI pack notes, so the seasonal difference between the wave 4 markets and the
notified markets has to be discovered from the 2024 to 2025 history rather than assumed; (2) asking for the cost at
a second date such as 1 November, so the counterfactual stock has to be carried one more month through the 14-day
restoration window; and (3) adding a second unrelated seasonal driver to the older-base piece so the 0.26-point
monthly-plans line has to be split rather than left as the residual. These are general suggestions, not a
requirement.

---

## Task 52ab454f-1f72-414f-a35a-5d9de378d452

Fellow ID 988d2899-4583-460e-ac6b-d2e79761fd68. Reward 17. Prelim verdict: Approved, Vincent will fix.

**Stumped.** passed (single usable GPT-6 Astra run, 17 percent against the 23-criterion rubric, below the 0.60
Sulfur bar; thin evidence, gate rests on one run). The run saw the shipped 11-file bundle, identified that thumbed
conversations are mostly the bad ones (pilot 22.7 percent good among thumbed vs 75.9 percent among unthumbed), then
refused to estimate: all shares and lifts NA, keep for all four categories, so it missed the move calls on coding
and advice and every figure

**Determinism (main).** passed: the call is forced. Blind fork audit (12 forks): the decisive fork is how to value
the unthumbed 87 percent of traffic. Thumbed-only audit routes (moves all four) are pinned out by the pilot (54
percent of bad vs 10 percent of good conversations get a thumb; Enterprise has no thumbs at all). Pilot-transfer
routes (A pilot model applied to both arms) are the only plausible rival and move other (+2.1 to +4.7); they are
rebutted by shipped evidence: in the weighted audit bad conversations are copied 39 percent in B vs 23 percent in A
(21 percent in the pilot), so an A-trained model mis-reads B. My replay of the golden (per arm and category logistic
on the weighted audit, label-shift re-estimate of the unthumbed share) returns lifts +8.04 / +11.23 / -1.98 / -2.99
and variants (no reply length, pooled categories, two features only) keep all four calls: advice +8.0 to +8.3,
coding +11.0 to +12.0, other -1.96 to -2.04, writing -2.4 to -3.0

**Determinism (supp).** passed: shares reproduce inside the accept bands (A 59.9 / 67.6 / 63.8 / 56.3, B 71.1 / 64.6
/ 71.8 / 54.4 for coding / writing / advice / other); pilot checks reproduce (1,848 of 3,000 good = 61.6 percent;
54 vs 10 percent thumb propensity); 161,384 joined conversations and 20,540 thumbed reproduce

**Solution (main).** passed: golden call (move coding and advice, keep writing and other) is the answer the data
forces

**Solution (supp).** passed: every committed figure reproduces to 0.1 point (golden other 56.4 / lift -2.0 vs mine
56.3 / -1.98; writing 67.7 vs 67.6); no golden figure fix needed

**Duplicate.** passed

**Task type match.** passed: General Statistics and Data Science: experiment analysis with outcome measured on a
feedback-selected subsample, selection correction and label-shift estimation across arms, adjacent to missing-data
and bias-correction analysis types

**Stumped type match.** passed: the deciding step is estimating the share of good conversations for the unthumbed
majority separately for each arm (selection into thumbs depends on quality, arm thumb designs differ, signal links
differ), not a planted defect, decoy, replay, data-semantics reading or rule application; the cleaning rules are all
stated in data_notes. The single run saw the selection problem and declined the estimate instead of working it

**Feedback.** Optional suggestions (not required; this task is approved as is): The package is a good one. The
August pilot is a real calibration source, the thumbed-only audit with its per-cell draw caps is a genuine selection
trap, and the data notes pin every cleaning rule (re-export duplicates, classifier label rename, Android thumb
codes, double reviews, logging gap) without hinting at the estimator. If you want to raise the difficulty further,
consider adding a fifth category that exists only in the second half of the test, or letting the new classifier move
a share of conversations between categories at the Sept 22 cutover, so the per-category estimate also has to be
rebuilt on a changing population. A second lever is to ship a second feedback surface for one arm (for example, a
thumb card on a subset of treatment conversations only), so the thumb propensity has to be modeled in two forms. The
inputs are synthetic; if you can, name the generating assumptions for any figure a solver might want to check
against a public reference.

---

## Task d311cbf0-1bc8-4327-ad10-d0ce386dd25c

Fellow ID 68446619-ee58-454c-b207-fb3b5640c428. Reward 35. Prelim verdict: Approved, Vincent will fix.

**Stumped.** passed (single usable GPT-6 Astra run 0.35 < 0.60; thin evidence)

**Determinism (main).** passed: the data forces no alert fires. Raw no-to-yes (1.33%, 5.86%, 2.10%) is not a rate of
first diagnoses: 10.7% / 11.6% / 15.9% of 2019 yes answers reverse, and 54% of new diabetes reports carry a
diagnosis age before 2019. Netting (0.46%, 1.47%, 0.72%) is confirmed by diagnosis timing for diabetes and cancer
(0.47%, 0.68%; missed-in-2019 to reversal ratio 0.99, 1.03) and bounded for hypertension (alert needs 43% genuine
against 25% implied; design upper end 2.35% under 2.5%). Weight, age-check and gap variants stay inside the bands
(0.32 to 0.74, 1.15 to 2.16, 0.48 to 1.13); medicine confirmation fails its own test on diabetes (0.89% against
0.47%; 53% diagnosed before 2019)

**Determinism (supp).** passed: older diabetes (age at 2019 interview) timing rate 0.48% reproduces with boundary
rule 9 / 12 / 47 / 6; my cruder boundary (diagnosis age against 2019 age, 15 / 12 / 47) gives 0.63%, inside the
0.25% to 0.95% band, below 1.0%; netted 1.02% overstated (missed-earlier outnumber reversals 1.33 to 1); crosswalk
10,415, 146 age-failed pairs, household-id join 14,447 rows with 50.5% same sex all reproduce

**Solution (main).** passed: golden call (no alert fires, older outreach included) is the answer the evidence
supports

**Solution (supp).** passed with Vincent-fix: golden reproduces on every figure checked; the timing-class rule for
the boundary year is not written in the Step-by-Step

**Duplicate.** passed

**Task type match.** passed: survey follow-up certification with record linkage, measurement-error (reversal)
correction and annualised incidence against thresholds sits in the data-quality / monitoring and measurement-error
types

**Stumped type match.** passed: the deciding step is detecting from genuine NHIS answers that the lifetime 'ever
told' item misreports in both directions (yes-to-no reversals, diagnosis ages before baseline) and correcting it by
netting validated against diagnosis timing, with a separate timing basis for the 65 and over group. Real public
data, no planted pattern, no rule or field reading decides it, and telling a solver 'net the reversals' still leaves
linkage, weighting, annualisation, timing validation, the hypertension extension and the older-group break to do.
The run did not compute a netted rate and decline it; it never netted and committed the raw proxies

**Feedback.** Optional suggestion (not required; this task is approved as is): the golden's Step-by-Step does not
state how diagnosis timing is classed at the boundary year (the 9 / 12 / 47 / 6 split of 74 older adults rebuilds
only with: after = diagnosis age at or above the 2020 interview age, same year = at or above the 2019 age but below
the 2020 age, before = below the 2019 age, age 99 = missing); adding that one sentence to step 10 lets a reviewer
reproduce it. To raise the difficulty further, consider asking for the break-even genuine share per alert at the
design-based upper end, not only at the point estimate, or for a fourth condition whose age-at-diagnosis item is
thinner, so the netting check has to be rebuilt on sparser timing data.
