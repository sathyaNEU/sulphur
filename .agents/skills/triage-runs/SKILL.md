---
name: triage-runs
description: After the platform generates and grades the two model runs of a Sulfur build, save both responses and optional deliverable files/rubric, record scores, invoke BOTH run-triage AND determinism-judge (holistic mode, running Holistic Audit v4 verbatim) in parallel, check stump_block_check.py, cross-check disagreements, and route the build (SUBMIT, FIX_DETERMINISM, SURFACE_RISK, FIX_ASKS, REDESIGN, or RUBRIC_EDIT).
---

# /triage-runs

Triage the two platform runs returned for `taskNN` (`status` `READY` or `RUNS`). Read `.agents/skills/build-pipeline/SKILL.md` (Stage 6) first. **NEVER let the parent build thread self-triage or approve its own task without BOTH isolated subagents (`run-triage` + `determinism-judge` in holistic mode).**

1. **Collect evidence verbatim:**
   - Save the user's pasted responses verbatim as `taskNN/runs/run1.md` and `taskNN/runs/run2.md` (archive any older cut's pair as `archN_pairK_run1.md` first). Save deliverable files under `runs/run1_files/` and `runs/run2_files/` if supplied, and any platform rubric/scores as `runs/rubric.md`.
   - Update `pipeline.json` `runs` (`files`, `run1`, `run2`, `average`, `recorded` with ISO date) and immediately set `status` to `RUNS`.
2. **Pre-check Holistic Audit v4 inputs:**
   - Run `python3 .agents/skills/determinism-check/holistic.py taskNN --check`. Fix any missing file/block issue before invoking subagents.
3. **Invoke BOTH isolated subagents in parallel in ONE `invoke_subagent` call** (define each first via `define_subagent` with `enable_write_tools: true` if not registered; launch with `Model: inherit`, `Workspace: inherit`):
   - `run-triage` (`.agents/agents/run-triage.md`): reads `runs/` + `DESIGN_NOTE.md` + `generator/core.py`, writes `taskNN/runs/triage.md`.
   - `determinism-judge` (`.agents/agents/determinism-judge.md`) in **`holistic` mode**: runs the FULL client Holistic Audit v4 (`guidelines/client/quality-checks/holistic-audit-v4-2026-11-22.md`) from scratch via `.agents/skills/determinism-check/holistic.py taskNN --mode holistic`, writes `taskNN/runs/holistic_check_v4.md`. Pass ONLY the task folder and `mode: holistic`.
4. **Reconcile both reports strictly (most conservative verdict wins):**
   - Record Holistic Audit v4's output in `pipeline.json` `holistic` (list).
   - Compare `runs/triage.md` against `runs/holistic_check_v4.md`. Explicitly list every disagreement (e.g., if v4 flags a catch, construction tell, `depth_level < 4`, `depth_flag: concentrated`, or `stumped: borderline/failed`).
   - **Hard-block `SUBMIT`:** Do NOT route `SUBMIT` if ANY of the following hold in EITHER report:
     - Platform OR v4 average `>= 0.60`, OR **higher-scoring run `>= 0.60`**;
     - Holistic Audit v4 verdict is `failed`, or `depth_level < 4`, or `one_thing_flip != none`, or any deciding step is flagged as a `catch` or construction tell;
     - Stronger run has `loss_concentration >= 0.70` concentrated on one sub-result/catch;
     - Fewer than 2 **non-catch** decisive steps were missed across the two runs for valid v4 difficulty reasons.
   - Record every unpredicted reflex in `.agents/skills/stumping/references/precedents.json`.
5. **Emit and verify `## How is each model stumped?`:**
   - Write the verified stump answer directly after `## Final Recommendation` in `submission.md` (via generator blocks-only rebuild so `target.zip` and `golden.zip` stay byte-identical), and run `python3 .agents/skills/submission-writeup/stump_block_check.py taskNN` to exit 0.
6. **Route and log:**
   - `SUBMIT` (only when all hard blocks pass): hand over the paste in order + Reward block; after user confirms submission, commit `SUBMITTED (taskNN): ...`.
   - `FIX_DETERMINISM`: `/fix-determinism taskNN <finding>`.
   - `SURFACE_RISK`: remove/disclose the catch or construction tell and rebuild on real modeling.
   - `FIX_ASKS`: `/fix-rubric taskNN` (strip ECF rollups and un-stumped texture asks; tighten coupled asks).
   - `REDESIGN`: log `## Tried and rejected`, set `status` `DESIGN`, route `/build taskNN from 2`.
   - Append a measurement row to `.agents/skills/stumping/references/sulfur-record.md` and `pipeline.json` `runs.history`, then commit and push.
