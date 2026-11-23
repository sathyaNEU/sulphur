# task9 architecture 5, pair 3: triage (2026-11-23)

The trimmed prompt's first pair (RESHIPPED 8814ff8), both responses pasted by the author on 2026-11-23 with no
platform scores and no generated rubric. Read in the main thread (no /triage-runs, so no run-triage or judge agent).
Responses saved verbatim as runs/run1.md and runs/run2.md; pair 2 is archived as runs/arch5_pair2_*.

## Loss map against the answer blocks

| Graded item | Golden (band) | Response 1 | Response 2 |
|---|---|---|---|
| Call | escalate labels; plans for noise, releases, training data; monitor retunes | lost (noise escalated) | lost (noise escalated) |
| Label revisions | 9.98 (9.92 to 10.05) | 9.99, made | 9.9868, made |
| Optimisation noise (CC2) | 6.89 (6.05 to 7.40) | 9.10, lost | 12.8698, lost |
| Feature releases | 6.65 (6.34 to 6.84) | 6.41, made | 6.3016, under the floor by 0.04 (placement right) |
| Training data (CC1) | 6.62 (6.35 to 7.44) | 6.57, made | 6.7516, made |
| Retunes | 4.47 (4.41 to 4.52) | 4.47, made | 4.4728, made |
| Pinned-views share | 55.0 (53.2 to 60.0) | 61.17 (calendar 2027 Mondays), outside | 63.0495 (calendar) and 61.1264 (the four pairs' refreshes), outside |

Both responses also volunteered shares, merchants' own change and tier figures; the trimmed prompt no longer asks
for them and nothing grades them.

## Decisive steps

| Step | Response 1 | Response 2 | With pair 2 |
|---|---|---|---|
| S1 training data (CC1) | made, 6.57 | made, 6.7516 | made by 4 of 4 responses (6.61, 7.278, 6.57, 6.7516) |
| S2 optimisation noise (CC2) | missed, 9.10 (half a replicate pair a refit, summed over 13) | missed, 12.8698 (a whole pair a refit) | missed by 4 of 4, the same two full sums each time |
| S3 pinned views (supporting) | deciding part made (calendar refused, releases on a plan); share outside | deciding part made; share and releases figure outside | pair 2's Response 2 took the calendar (92.857) |

## First wrong step

- Response 1, method_shortcut: "A next refit carries one increment, so per-refit variance is half the pair MS; 13
  refits accumulate linearly", the assumption named and waved through ("Weekly increments and sources accumulate
  linearly in MS"). Its only alternative was the other full sum (12.87). Its check, a weekly OLS "with family fixed
  effects", gives each family a constant that absorbs the noise level, so it never tests the noise (a check of the
  wrong kind).
- Response 2, dismissed_own_evidence: "I examined panel time-series behavior but did not impose an unstated
  decaying-persistence model". Its validation is a self_confirming_check: the own-change residual takes up the
  noise model's difference one for one (its noise MS 165.6321 against Response 1's 82.8161, 82.82 apart; its own
  change 74.128653 against 159.1608, 85.03 apart), and a tier check sees only the sum.

## The pinned share rebuilt in core.py's own estimators

Scratch arithmetic on the generator's world (past_adoption, evaluate with each route's coverage), not in
figures.json and not in submission.md:

| Route | The four pairs' refreshes (28 Dec 2026 to 20 Dec 2027) | Calendar 2027's Mondays (4 Jan to 27 Dec 2027) | Feature releases |
|---|---|---|---|
| Response 1 (each family's three planned-to-first lags, empirical, no reverts) | 59.25 (431.33 of 728) | 61.17 (445.33), reproduces | 6.404 (its 6.41) |
| the same, reverts netted (4.4 per cent) | 56.64 | 58.48 | 6.621 |
| Response 2 (median planned-to-first lag a family, plug-in, no reverts) | 61.13 (445), reproduces | 63.05 (459), reproduces | 6.295 (its 6.3016) |
| the same, reverts netted | 58.44 | 60.28 | 6.520 |
| golden (log-linear take-up, integrated, reverts netted) | 55.01 | 56.82 | 6.647 |
| golden without reverts | 57.54 | 59.43 | |
| plug-in median, no reverts: log-linear / own / groups / pooled | 59.62 / 59.07 / 59.07 / 62.09 | 61.54 / 60.99 / 60.99 / 64.01 | 6.374 / 6.402 / 6.438 / 6.095 |

Reading. results.py `forks()` admits calendar 2027's Mondays and refuses taking no reverts "by the manifests'
reverted weeks", so on the house closure both share misses rest on the reverts. But the shipped Step-by-Step says
"every take-up form, log-linear or linear, by group, by family or pooled, integrated or as a plug-in median lag,
with or without reverts, puts it between 54.4 and 59.6 per cent", which the full cross does not bear out (pooled
plug-in without reverts 62.09, releases 6.095). An audit can reproduce Response 1's 61.17 from two conventions the
shipped text admits (calendar Mondays, no reverts): a not_pinned risk on the pinned share and on Response 2's
releases floor. Flagged for the author, not fixed (fixes wait for the platform's audit or the author's word).

## Score estimate (house model of the generated rubric: recommendation 18, components 20, asks 53, instruction 9)

- Graded strictly on the stated bands: Response 1 about 54 (the call, noise, CC2 and the pinned share lost),
  Response 2 about 45 (the releases figure as well), average about 50; the stronger run under 60.
- With the pinned share (and Response 2's releases) given back as a defensible alternative: each loses only the
  call, noise and CC2, about 63 (corelib's "S2 lost alone"), average about 63, over the bar.

## Verdict

Stumped on the call for an analytical reason both responses share, at one decisive step (S2). S1 was made by both,
and by four of four responses across two pairs, and S3's deciding part by both. build-pipeline's route table sends
"both runs made every decisive step but the same one whatever the average" to REDESIGN, not SUBMIT; the platform
average is likely under 60 on strict bands, but the margin rests on the pinned-share band edge. The author rules:
submit with both risks named, hold for the platform's scores and its holistic audit, or redesign.

The stump answer is in submission.md directly after the Final Recommendation (writeup.py `_stump_block`, every
quote and figure asserted against the saved responses and figures.json); it lists the noise step as the stump for
both, training data and the calendar's refusal as made by both, and each response's pinned share against the band
without classing it.
