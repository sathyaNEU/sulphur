---
name: fix-rubric
description: Repair a Sulfur build whose runs lost points for analytical reasons but averaged 60 or higher because the runs earned results whose difficulty was a reflex or losses sat on too few results. Rebuilds or replaces earned results while freezing results that held, proves scope with freeze.py and effort.py, and re-ships for new runs.
---

# /fix-rubric

Repair a `FIX_ASKS` build from `/triage-runs`: analytical losses held, but the average or strongest run reached 60+ because the ask layer gave away points on figures untouched by the stumps or inside band under a lost stump. Keep the results that held frozen.

**The core belongs to `stump-architect`.** Invoke `stump-architect` (`.agents/agents/stump-architect.md`) with `runs/triage.md` (stronger run's earned map first) to rework `generator/core.py`, `## Stump core`, and `## Build brief`; then execute the brief and prove scope here.

Read `.agents/skills/supplemental-stumping/SKILL.md` (Parts 0, 1, 6), `.agents/skills/stumping/SKILL.md` (Parts 1 to 3), and `.agents/skills/build-pipeline/SKILL.md` first. Read `runs/triage.md`, `runs/rubric.md`, and both runs (if missing, run `/triage-runs` first and stop).

1. **Freeze before any edit:** `python3 .agents/skills/build-pipeline/freeze.py snapshot taskNN`. Read the results chain, effort test, and `## Tried and rejected`.
2. **Audit where points went:** Identify every result both runs earned (reflex, filed sentence, or restated fit) and every criterion passed without deep work. Surface losses are `SURFACE_RISK`, not a rubric lever.
3. **Rebuild earned results** (`supplemental-stumping` Part 6):
   - Rebuild a reflex result around the move beyond it, or replace it with a downstream consequence of a stump the runs lost. Cut figures untouched by any stump from the prompt and Supplementary Questions (keep their work in Step-by-Step).
   - Keep critical components independent (one per stump, stated as the answer with no method clause, inside a requested deliverable).
   - Keep one to four hard, multi-faceted asks; no surface causes.
   - Tighten `prompt.txt` only where needed, adhering strictly to the natural practitioner standard in `.agents/skills/guide-to-prompt/SKILL.md` (`voice-check.py` 0 FAIL / 0 WARN).
4. **Assert, rebuild, prove scope:** Update `checks.py` (R1 to R7), rewrite `effort.json`, confirm `effort.py` pair estimate is 50 or under, rebuild twice (byte-identical), redraft Supplementary Questions and Critical Components from `figures.json`, run `python3 .agents/skills/build-pipeline/gates.py taskNN --full`, and verify:
   ```
   python3 .agents/skills/build-pipeline/freeze.py check taskNN --mode rubric
   ```
   Exit 1 means a frozen result moved: undo it.
5. **Re-ship:** Re-cut `target.zip` and `golden.zip`, verify `audit_containers.py taskNN` exits 0, append to `pipeline.json` `returned` (`repair: "rubric"`), set `status` `READY`, record a `## Tried and rejected` line per rebuilt result, commit `RESHIPPED (taskNN): results rebuilt, <which>` with `git add -f` on ZIPs and `golden/`, rebase onto `origin/main`, and push.

Report: before/after `effort.py` pair estimate, results rebuilt/replaced, critical components changed, `freeze.py` verdict, and ZIP paths/MD5s.
