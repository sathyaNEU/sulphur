# task9 triage, the reshipped pack's first pair (2026-11-22)

Read in the main thread from `runs/run1.md` and `runs/run2.md` against `submission.md`. The platform scores and the
generated rubric are not on file yet, so the averages are owed and the verdict is provisional.

## Loss map (golden, band, then each response)

| Figure | Golden (band) | Response 1 | Response 2 |
|---|---|---|---|
| Label revisions | 9.98 (9.92 to 10.05), escalation | 9.99 escalation, made | 9.987 escalation, made |
| Optimisation noise | 6.89 (6.05 to 7.40), plan | 9.10 escalation, lost | 12.870 escalation, lost |
| Feature releases | 6.65 (6.34 to 6.84), plan | 6.54 plan, made | 4.001 monitor, lost |
| Training data | 6.62 (6.35 to 7.44), plan | 6.61 plan, made | 7.278 plan, made |
| Retunes | 4.47 (4.41 to 4.52), monitor | 4.47 monitor, made | 4.472 monitor, made |
| Model-side shares | 39.1 / 18.6 / 17.3 / 17.2 / 7.8 | all five outside their bands | all five outside their bands |
| Merchants' own share | 43.9 (41.9 to 46.7) | 34.79, lost | 17.73, lost |
| Pinned views, actual use | 55.0 (53.2 to 60.0) | 58.97, made | 92.857, lost |
| Tier changes | 14.0 (13.7 to 14.6) | 13.56, lost | 13.365, lost |
| Tier changes, sources removed | 9.7 (9.4 to 10.3) | 8.52, lost | 6.626, lost |

## Decisive steps

| Step | Response 1 | Response 2 |
|---|---|---|
| CC1 training data (S1) | made (6.61) | made (7.278) |
| CC2 optimisation noise (S2) | missed: full carry, half a replicate pair per refit (unfinished chain; self-confirming check of the wrong source) | missed: full carry, a whole replicate pair per refit (dismissed own evidence: names the assumption and keeps it) |
| Pinned views, actual use (S3, supporting) | made (58.97) | missed: the calendar taken as use (method shortcut) |

First wrong step. Response 1: "warm-started sources were treated as permanent 13-week random-walk accumulations
rather than decaying effects" (unfinished chain). Response 2: "Warm-start treated as full carry/random-walk
accumulation, with no decay" (dismissed own evidence; it calls it "the assumption most capable of changing the
recommendation").

## Reading against the design

- S2 lost by both on the two routes the core priced (9.10 and 12.87): the design working.
- S1 made by both. The careful column priced it as lost; both responses scaled the bootstrap spread to each
  window's turnover unprompted. Recorded as evidence that the window-overlap step is a reflex for these runs.
- S3 lost by Response 2 exactly as priced (the calendar, releases 4.00 monitor), made by Response 1.
- So between them the responses missed two independent steps (S2 and S3), but only one of them (S2) is on the
  Critical Components, and the strongest-looking response (Response 1) missed only S2. Review risk: "only one
  decisive step" read off the CC block. Nothing is changed until the scores are in and the author rules.

## Verdict

Provisional SUBMIT on the analytical evidence (both calls wrong, every loss analytical, no surface trigger),
pending both platform scores under 60 and the strongest run under 60. Author's ruling owed on the CC block
(training data was made by both).

The stump answer below is in `submission.md` as `## How is each model stumped?`, directly after the Final
Recommendation, emitted by `generator/writeup.py` `_stump_block` with every response quote and figure asserted
against `runs/run1.md` and `runs/run2.md` and every golden figure from `figures.json` (`stump_block_check.py task9`
PASS; the response percentages are written there in per cent words). Status `RUNS`, scores owed.

## Stump draft (How is each model stumped?)

**Response 1.** Response 1 files optimisation noise in escalation at 9.10 points, where the answer is a remediation plan at 6.89 (band 6.05 to 7.40), and it is right on the other four sources. It read section 1.4 correctly, that a warm-started refit carries the randomness of the refits before it, but then assumed the carried noise never fades: "warm-started sources were treated as permanent 13-week random-walk accumulations rather than decaying effects". Taking half a replicate pair as each refit's fresh draw and adding thirteen of them gives its 9.10. It tested decay only by regressing later panel changes on release effects ("slopes near zero"), a check on another source; it never fitted how the score history's change grows with the gap between snapshots, which is where the decay shows. The overstated noise then runs downstream: merchants' own share comes out at 34.79 per cent against 43.9 (band 41.9 to 46.7), every model-side share sits outside its band (label revisions 34.52 against 39.1), and the tier counterfactual is 8.52 per cent against 9.7. It made the other two hard steps: training data at 6.61 (golden 6.62), by scaling the bootstrap spread to each window's rows, and actual use of pinned views at 58.97 per cent (band 53.2 to 60.0), measured from the three past platform changes, which keeps feature releases on a plan at 6.54.

**Response 2.** Response 2 files optimisation noise in escalation at 12.870 and feature releases on monitor at 4.001, where the answer is a plan for both (6.89 and 6.65). It took the same full-carry reading as Response 1 but counted a whole replicate pair per refit, and it named the choice itself: "Warm-start treated as full carry/random-walk accumulation, with no decay ... this is the assumption most capable of changing the recommendation, and I flag rather than hide it." Its only check on that choice was that the 2026 residual stayed flat across three quarters (75.610, 78.493, 75.005), which cannot tell full carry from decayed carry, since both hold the model side steady from quarter to quarter. It then took the platform calendar's rollout as the pinned views' actual use, "every family pinned by Monday 22 February 2027", for 92.857 per cent against 55.0, so releases drop to monitor; its own words show the risk was seen and set aside: "Pinned weeks taken on schedule ... the Monitor placement is conditional". Downstream, merchants' own share is 17.73 per cent against 43.9 and the tier counterfactual 6.63 against 9.7. It made the training-data step, 7.278 points inside the band 6.35 to 7.44, by a turnover estimator of its own.

**Why this is a fair stump.** Neither step turns on a planted defect or a buried sentence. Both responses cleaned the record to the golden's counts (3,360,865 scored merchant-weeks, 4,568 Tolka Pay identifiers mapped, 644 instrument pairs), so the losses came after the cleaning. The definitions are the standard's own and both responses quoted them: section 1.4 on carried noise, and the ask's "expected to actually run on pinned feature views". The evidence is not one line in one file but the shape of whole files. The decay is in the gap curve of the ten panel files, in every family: a straight line through gaps 8 to 26 meets gap 0 at 35.6 points squared, book weighted, and above zero in every family (14.3 or more), which a carry that never fades cannot produce. Actual use is in the scheduler manifests set against the calendar: 42 past family rollouts first trained 3 to 31 weeks after the calendar marked them complete. Response 1 reached the second step unprompted from the same files, so it is reachable.

**Why it takes rigour.** Each step has an obvious repair that still files the wrong band. For the noise, reading the replicate pairs at face value gives 3.57 points (monitor); adding each refit's draw in full gives 9.10 or 12.87 (escalation); fitting the gap curve free of the replicate pairs gives 8.77 but implies replicate pairs of 17.44 where 12.73 is measured. The answer needs the curve fitted family by family on the settled warm weeks, with its start tied to the measured replicate variance, which gives a persistence of 0.79 to 0.95 and 6.89 points. For pinned views, the calendar's planned weeks give 90.9 per cent and releases at 4.00, its completed dates 87.1 per cent and 4.46, monitor either way; the answer needs the take-up lag modelled from the past rollouts, with its spread and the reverted weeks, which gives 55.0 per cent and releases at 6.65. The steps are independent: missing only the noise step moves optimisation noise to escalation and nothing else, which is Response 1's call; missing both also drops feature releases to monitor, which is Response 2's.
