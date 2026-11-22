---
name: build
description: Build one Sulfur task end to end. The core is designed by the stump-architect subagent (intake, draw, design gated by precut.py) unless /draw already did it; the parent thread then executes the architect's Build brief (pack, goldens, answer blocks), spawns leak-reader and determinism-judge together at stage 4, and takes the build to READY. Supports taskNN <domain> <analysis type>, new <domain> <analysis type>, resume taskNN, or taskNN from <stage>.
---

# /build

Run the Sulfur build pipeline for the requested task arguments. Read `.agents/skills/build-pipeline/SKILL.md` first: the stages, gates, commits, `pipeline.json`, and re-rooting are defined there and not restated here.

## Arguments

- `taskNN <domain> <analysis type>`: the task number (`python3 .agents/skills/build-pipeline/status.py new` gives the next free one, `task1` up), the assigned Sulfur subdomain (one of the 21 in `guidelines/client/domains.txt`, mapped to its vocab key), and the assigned analysis type (one of the nine, the card's `objective`). A starter data kit path, when claimed, becomes the pack's spine candidate.
- `new <domain> <analysis type>`: the same with the next free number.
- `resume taskNN` or `taskNN from <stage>`: continue from `pipeline.json`, re-checking that stage's gate first.

## The client's bar comes first

Follow `AGENTS.md` (first section) and `.agents/skills/stumping/SKILL.md`. Read `guidelines/client/project-lead-review-2026-11-09.md` and the strategies for the domain group before any draw. A new draw is a results chain with two or more decisive, independent steps (three targeted for level 5), each owning a critical component, each off the 45 closed strategies, with `effort.py` and `corelib.py` proving the margins before any pack exists.

A build back from the platform is not a `/build`: run `/triage-runs` first. A landed call comes back here as `/build taskNN from 2` with the triage loss map in the design note.

## Two hands, one build

The core belongs to `stump-architect` (`.agents/agents/stump-architect.md`): which judgments stump the review's strongest run, the world's dials, every margin, every estimator. The parent thread is the executor: it builds the pack, goldens, and answer blocks from `## Build brief` and moves nothing listed under `Frozen:`.

## Run the stages in order

Read each stage's skills under `.agents/skills/` before its work and leave a stage only when its gate passes:

1. **Stages 0 to 2 belong to `stump-architect`.** If the task has no `DESIGN_NOTE.md` passing `precut.py` with `## Stump core`, `## Build brief`, and `generator/core.py`, define and invoke `stump-architect` from `.agents/agents/stump-architect.md` via `define_subagent` (`enable_write_tools: true`) + `invoke_subagent` (`Model: inherit`, `Workspace: inherit`) with the task number, subdomain, analysis type, any starter kit path, and (for a re-root) `runs/` and review paths. Do no design work while it runs. When it returns: run `python3 .agents/skills/stumping/precut.py taskNN` and `python3 taskNN/generator/core.py` yourself (both exit 0, or resume the architect via `send_message` with the failing output), show the draw in ten lines with the core table, commit `DRAWN (taskNN)`, and carry on. **Do not stop for the author.** A build `/draw` already designed starts at stage 3.
2. **Execute the brief without drifting.** Read `## Stump core` and `## Build brief` first. The generator imports the world from `generator/core.py` and builds the organisation's systems, files, Layer 1 mess, and documents around it. If the cut pack breaks a core assertion, a route lands on the wrong side of its line, a member turns forced, or closing a fork would need a sentence naming a result's work, pause stage 3 and message `stump-architect` via `send_message` (or invoke a fresh one briefed with the note and failing figure). Never widen a margin, narrow a rival, file a method, or add an effect to clear a gate.
3. **Stage 3 leaves only when all free gates are green:** `python3 .agents/skills/build-pipeline/gates.py taskNN --full` (generator checks, `verify`, two byte-identical rebuilds, `effort.py`, `figures_check.py`, `voice-check.py`, `leak.py`, `audit_containers.py`, `guard.py surface` and `heart`), plus the realism sweep.
4. **Stage 4 invokes two isolated subagents in parallel in one `invoke_subagent` call:**
   - `leak-reader` (from `.agents/agents/leak-reader.md`, `enable_write_tools: false`, seeing ONLY a fresh scratch copy of `prompt.txt` and `target/`).
   - `determinism-judge` (from `.agents/agents/determinism-judge.md`, `enable_write_tools: true`, checking Gates A to E only).
   While they run, update the fingerprint card and pre-ship check. Fix every finding from both in one generator pass; re-judge once only when a fix moved a graded figure, the prompt, or the pack (answer-block-only edits are not re-judged); re-read only if a document or `prompt.txt` changed.
5. **Stage 5, READY.** Re-run `python3 .agents/skills/build-pipeline/gates.py taskNN --full` on the final cut. Cut `target.zip` and `golden.zip` (exactly the files the prompt requests, preserving file mtimes), run `python3 .agents/skills/reduce-house-fixes/scripts/audit_containers.py taskNN` and stop on any FAIL, set `status` to `READY`, commit `READY (taskNN): <call>` (with `git add -f taskNN/target.zip taskNN/golden/ taskNN/golden.zip`), rebase onto `origin/main`, and push.
6. **Keep responsibilities clean:** pack/golden/block repairs stay in this thread; core repairs go back to `stump-architect`.

Write `pipeline.json` at every stage boundary (`status` and `updated`), and commit at each status boundary named in `.agents/skills/build-pipeline/SKILL.md`.

## Report at READY

Report in order: the committed answer, the results chain, the effort test (quick/careful/thorough scores and largest single hint), the hidden factor record verdicts, the leak line (`leak.py` + reader Q1), the duplicate line (`heart` + nearest build), the judge's determinism verdict and disposition, the pair estimate, the paths and MD5s of `prompt.txt`, `target.zip`, and `golden.zip`, and the ready-to-paste answer blocks from `submission.md`.
