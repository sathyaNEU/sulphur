---
name: triage-runs
description: After the platform generates and grades the two model runs of a Sulfur build, save both responses and the rubric, record scores, spawn run-triage to map losses result by result and class every loss, mark each decisive step made or missed, draft the answer to the form's stump question (How is each model stumped?), and route the build (SUBMIT, FIX_DETERMINISM, SURFACE_RISK, FIX_ASKS, REDESIGN, or RUBRIC_EDIT).
---

# /triage-runs

Triage the two platform runs returned for `taskNN` (`status` `READY` or `RUNS`). Read `.agents/skills/build-pipeline/SKILL.md` (Stage 6) first.

1. **Collect evidence verbatim:** Save the user's pasted responses and generated rubric as `taskNN/runs/run1.md`, `taskNN/runs/run2.md`, and `taskNN/runs/rubric.md`. If anything is missing, ask once and stop. Never paraphrase a run.
2. **Record scores:** Update `pipeline.json` `runs` (`run1`, `run2`, `average`, `recorded` with today's ISO date) and set `status` `RUNS`. Bar is average under 60 (exactly 60 fails) AND strongest run under 60. Record any unchanged re-run reason in `runs.history`.
3. **Invoke `run-triage`:** Define and invoke `.agents/agents/run-triage.md` via `define_subagent` (`enable_write_tools: true`) + `invoke_subagent` (`Model: inherit`, `Workspace: inherit`) passing the absolute task folder. It writes `taskNN/runs/triage.md`.
4. **Cross-check its loss map against `DESIGN_NOTE.md`:** Compare losses against `## Effort test` and `## Results chain`. Record any unpredicted reflex in `.agents/skills/stumping/references/precedents.json`. Confirm `## Decisive steps` shows two or more decisive steps missed between the two runs. Note any disagreement beside the triage report.
5. **Route on verdict:**
   - `SUBMIT`: insert the verified stump draft into `submission.md` as `## How is each model stumped?` directly after `## Final Recommendation`, fill the Reward block from `pipeline.json`, and once confirmed commit `SUBMITTED (taskNN): <call>, runs <x> and <y>, average <z>`.
   - `FIX_DETERMINISM`: route to `/fix-determinism taskNN <finding>`.
   - `SURFACE_RISK`: rebuild the trigger as analysis or make it texture off every graded path, re-run gates, re-cut ZIPs, and regenerate runs.
   - `FIX_ASKS`: route to `/fix-rubric taskNN`.
   - `REDESIGN`: log a `## Tried and rejected` line, set `status` `DESIGN`, route to `/build taskNN from 2`.
   - `RUBRIC_EDIT`: give the user the exact criterion fix to apply on the platform.
6. **Record the lesson:** Append spread, classes, scores, and route to `pipeline.json` `runs.history`, and add one row to `.agents/skills/stumping/references/sulfur-record.md`.

Report: both scores, average, counterfactual average, loss map, each run's first wrong step + class, each decisive step made/missed, the `Valid Stump?` draft, verdict, and route. Never run an in-house solver.
