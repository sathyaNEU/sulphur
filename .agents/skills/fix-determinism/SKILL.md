---
name: fix-determinism
description: Repair a Sulfur build where a run took a defensible alternative (triage FIX_DETERMINISM), the determinism judge found a fork, or a reviewer returned it as not deterministic while the stump held. Closes the fork in the record so the literal reading is the golden without moving the main call or stumps, proves scope with freeze.py, re-judges once via determinism-judge, and re-ships.
---

# /fix-determinism

Repair an open reading on `taskNN`: a run took a sound method the prompt allows and landed elsewhere, or a judge/reviewer found two defensible answers. Make the shipped text, read literally, land on the golden already built without weakening the stumps.

**The core belongs to `stump-architect`.** If the fork-is-the-result test (step 3) shows the closing sentence would name what a result's work recognises, or the only closure is a filed method, invoke `stump-architect` (`.agents/agents/stump-architect.md`) with the finding so it adds a referee/falsification check or redesigns in `generator/core.py`, then rebuild. Never pin a stump into a rule here.

Read `.agents/skills/determinism-check/SKILL.md` and `.agents/skills/build-pipeline/SKILL.md` first. Read the finding from the user's message, `runs/triage.md`, or `pipeline.json`.

1. **Freeze before any edit:** `python3 .agents/skills/build-pipeline/freeze.py snapshot taskNN`. Read `## Semantic fork table`, `## Closure table`, `## Literal reader`, and `## Tried and rejected` in `DESIGN_NOTE.md`.
2. **Classify the finding** (`determinism-check` §6) and add a new fork-table row (`SFn`): term/convention, golden reading, alternative readings, and call/figure under each.
3. **Fork-is-the-result test & banned list:** Closing the HOW makes the result rule application (banned in `AGENTS.md`). Close the WHAT, never the HOW. If closing the fork in either direction puts the hurried pass inside the band, stop: log a line in `## Tried and rejected`, set `status` to `DESIGN`, and redesign via `/build taskNN from 2`.
4. **Close with the strongest valid move** (`determinism-check` §3):
   - **C1 converge** (align records so every reading selects the same rows/figure; preferred).
   - **C2 confirm / C3 corridor / C4 separate**.
   - **Pin at authority once** (one filed sentence in the governing document in `target/` fixing the WHAT, never the HOW).
   - If `solution_incorrect`, fix the generator so `figures.json`, goldens, and `submission.md` agree.
   - If `prompt_ambiguity` on an ask, tighten that ask's wording only (`voice-check.py` green, call sentence frozen).
5. **Assert, rebuild, prove scope:** Add `SFn` to `checks.py` and `verify.py`, rebuild twice (byte-identical), run `python3 .agents/skills/build-pipeline/gates.py taskNN --full`, then:
   ```
   python3 .agents/skills/build-pipeline/freeze.py check taskNN --mode determinism
   ```
   Use `--allow <figures.json key>` only when the golden itself had a `solution_incorrect` bug.
6. **Re-judge once:** Invoke `determinism-judge` (`.agents/agents/determinism-judge.md`) via `define_subagent` + `invoke_subagent` (`Model: inherit`, `Workspace: inherit`). On `APPROVE`, proceed; on `FIX_NOW` (answer-block edits only), edit and ship without another judge; on `SEND_BACK`, stop and report. Re-run `leak-reader` only if a document under `target/` or `prompt.txt` changed.
7. **Re-ship:** Re-cut `target.zip` and `golden.zip`, verify `audit_containers.py taskNN` exits 0, append to `pipeline.json` `returned` (`repair: "determinism"`), set `status` `READY`, add a `## Tried and rejected` line, commit `RESHIPPED (taskNN): determinism, <fork closed>` with `git add -f` on ZIPs and `golden/`, rebase onto `origin/main`, and push.

Report: the fork, the closure move, `freeze.py` verdict, judge verdict, and ZIP paths/MD5s.
