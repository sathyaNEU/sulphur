---
description: After the platform has generated and graded the two runs, record both scores and the average, map where each run lost its points result by result and class every loss on the client's failure table, and route the build (submit, fix determinism, fix the asks, rebuild a surface trigger as analysis, or redesign).
argument-hint: taskNN [the two scores, or nothing if runs/rubric.md carries them]
effort: medium
---

# /triage-runs

The build named in `$ARGUMENTS` is on the platform (`status` `READY` or `RUNS`) and its two runs are back.
Invoke `build-pipeline` (Stage 6) first.

1. **Collect the evidence into the task folder.** The author pastes each run's full response and the generated
   rubric (criteria, weights, and each run's pass or fail where the platform shows it). Save them verbatim as
   `taskNN/runs/run1.md`, `taskNN/runs/run2.md` and `taskNN/runs/rubric.md`. If anything is missing, ask once
   for it and stop. Never paraphrase a run.
2. **Record the scores** in `pipeline.json` `runs` (`run1`, `run2`, `average`, `recorded` with the ISO date) and
   set `status` `RUNS`. The bar is an average under 60; exactly 60 fails.
3. **Spawn one `run-triage` agent** (its definition sets model and effort) with the absolute task folder. This
   command licenses it. It writes `runs/triage.md`.
4. **Check its loss map against the design note yourself.** A run that lost the results the `## Effort test`
   priced as lost, in the classes the `## Results chain` names, is the design working; a run that earned a result
   priced as lost found a reflex the careful column missed (record it as evidence); a run that lost somewhere the
   chain does not predict is either a deep loss the design did not model or a surface trigger (fix it). Where you
   disagree with the agent, say so in one line each and keep both readings in the report.
5. **Route** on the verdict:
   - `SUBMIT`: set `status` `SUBMITTED` once the author confirms submission, fill the platform's Reward block from
     `pipeline.json`, commit `SUBMITTED (taskNN): <call>, runs <x> and <y>, average <z>`.
   - `FIX_DETERMINISM`: `/fix-determinism taskNN <the run's method and why it is defensible>`.
   - `SURFACE_RISK`: the named trigger is rebuilt as analysis or becomes texture in the generator (unmissable, or no
     longer on any graded path), the free gates re-run, the pack is re-cut and the author regenerates the runs; the
     other results are not touched.
   - `FIX_ASKS`: `/fix-rubric taskNN` with the triage file.
   - `REDESIGN`: one line in `## Tried and rejected` (what both runs did), `status` `DESIGN`, `/build taskNN from 2`.
   - `RUBRIC_EDIT`: give the author the criterion and its corrected text; they edit it on the platform and re-run
     the evaluation, then this command runs again with the new scores.
6. **Record the lesson.** Append the spread, the classes, the scores and the route to `pipeline.json`
   `runs.history`, and one row to `stumping/references/sulfur-record.md` (the Sulfur run record: task, domain,
   analysis type, the weight and chain signature, both first-wrong-step classes, the spread, both scores, verdict).
   This record is what the next draw reads first.

Report: both scores and the average, the counterfactual average, the loss map (which results each run lost and
why), each run's first wrong step quoted with its class, the verdict and the route. No solver runs here: the
platform's two runs are the only evidence.
