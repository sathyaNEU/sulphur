---
name: holistic-check
description: Replay the platform's Holistic Audit v4 in-house on one build whose two platform responses are saved, through determinism-judge in holistic mode (the whole audit of guidelines/client/quality-checks/holistic-audit-v4-2026-11-22.md: correctness, determinism with the convention check, its own rubric grading both runs, and depth). Records the predicted verdict, score and must_fix list in pipeline.json and flags them to the author; fixes nothing. With "determinism" it runs the judge's pre-platform mode instead (Step 0, Part A and Part B) on a build with no runs yet.
---

# /holistic-check

The platform runs Holistic Audit v4 on a task once the two model responses are back, and a fail blocks submission. This workflow replays the exact client audit in-house on the same inputs: `prompt.txt`, `target.zip`, the four answer blocks in `submission.md`, and both saved platform responses (plus deliverable files if saved). The `determinism-judge` subagent follows the filled `audit_prompt.md` word for word in `holistic` mode.

1. **Check the inputs before spending a subagent pass:**
   - Ensure `taskNN/prompt.txt`, `taskNN/target.zip`, and `taskNN/submission.md` exist.
   - For `holistic` mode, ensure both saved responses sit under `taskNN/runs/` (`run1.md` + `run2.md`, or `response1.md` + `response2.md`, with optional `run1_files/` + `run2_files/`).
   - Run `python3 .agents/skills/determinism-check/holistic.py taskNN --check` (add `--mode determinism` for the pre-platform pass). A non-zero exit stops here.
2. **Invoke `determinism-judge`:**
   - Register `.agents/agents/determinism-judge.md` via `define_subagent` (`enable_write_tools: true`) if not already registered, then invoke via `invoke_subagent` (`Model: inherit`, `Workspace: inherit`).
   - Pass ONLY the absolute task folder and the mode (`holistic` or `determinism`). Never pass design notes, intent, or hints.
3. **Record the verdict:**
   - Read `<task>/runs/holistic_check_v4.md` (holistic mode) or `<task>/determinism_check_report.md` (determinism mode).
   - Append an entry to `pipeline.json` `holistic` (list): `date`, `mode`, `report`, `verdict`, `score`, `rubric` (`run1`, `run2`, `mean`, `stumped`), `correctness`, `determinism`, `depth_level`, `depth_flag`, `loss_concentration`, `must_fix`, and md5s of `prompt.txt`, `target.zip`, and `submission.md`.
   - If `runs/triage.md` exists, note every disagreement between `run-triage` and Holistic Audit v4 in one line each.
4. **Hard blocks before submission:**
   - Never treat a borderline pass (`0.60-0.65`) or `depth_flag: concentrated` with `loss_concentration >= 0.70` or any decisive step flagged as a `catch` / construction tell as safe to submit without explicit redesign or author override.
   - Do not modify `prompt.txt`, `target.zip`, or `submission.md` during `/holistic-check`; report the verdict, five-line summary, score, `must_fix` list, feedback paragraph, and `Routes:` line so the author decides.
5. **Commit and push** under the current `pipeline.json` status (`RUNS (taskNN): in-house Holistic Audit v4 <passed | failed>, score <n>`), staging only the report and `pipeline.json` explicitly.
