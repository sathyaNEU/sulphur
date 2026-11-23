---
description: Build one Sulfur task end to end. The core is designed by the stump-architect agent on the strongest model (intake, draw, design gated by precut.py) unless /draw already did it; this thread then executes the architect's Build brief (the pack, the goldens, the answer blocks), runs the leak reader and the determinism judge together, and takes the build to READY. Takes a task number with the assigned domain and analysis type, or resumes a build from its pipeline.json.
argument-hint: taskNN <domain> <analysis type> [starter kit path] | new <domain> <analysis type> | resume taskNN | taskNN from <stage>
model: opus
effort: high
---

# /build

Run the pipeline for `$ARGUMENTS`. Invoke the `build-pipeline` skill first: the stages, gates, effort, commits,
`pipeline.json` and re-rooting are its business and are not restated here.

**Arguments.**

- `taskNN <domain> <analysis type>`: the number (`status.py new` gives the next free one, task1 up), the assigned
  Sulfur subdomain (one of the 21 in `guidelines/client/domains.txt`, mapped to its vocab key) and the assigned
  analysis type (one of the nine, the card's `objective`).
  A starter data kit path, when the author claimed one, becomes the pack's spine candidate.
- `new <domain> <analysis type>`: the same with the next free number.
- `resume taskNN`, `taskNN from <stage>`: continue from `pipeline.json`, re-checking that stage's gate first.

**The client's bar comes before anything else** (`CLAUDE.md`, first section; `stumping`). Read the project lead's
review (`guidelines/client/project-lead-review-2026-11-09.md`) and the strategies for the domain group before the
draw. A new draw is a results chain: four or more checkable results across three or more of the fourteen areas, each
pinned with a band and a hurried failure the runs make, no analytical result carrying most of the others, every
hidden factor through the client's three conditions, the effort test measured by `effort.py`, and the one-fact test
counted in results. A design that turns on one thing (a plant, a field reading, an executed procedure, a replayed
figure, a single fact, a shallow hidden factor or an open reading) is re-rooted, never resumed. A build cut under the
retired single-deep-step design is re-rooted to a results chain before any re-ship.

A build back from the platform is not a `/build`: `/triage-runs` reads the runs and routes it. A landed call comes
back here as `/build taskNN from 2` with the triage file's loss map in the design note.

**Two hands, one build** (`stumping` Part 1d; `build-pipeline`, Effort per role). The core is the architect's:
which judgments stump the review's strongest run, the world's dials, every margin, every estimator. This thread is
the build: it executes the note's `## Build brief` and moves nothing the brief lists under `Frozen:`. The
frontmatter's model and effort hold for the turn this command runs in; a later message in the same session is
answered by the session's own model, so a build is continued with `/build resume taskNN`, not with a bare reply.

**Run the stages in order**, invoking each stage's skills before its work and leaving a stage only when its gate
holds.

1. **Stages 0 to 2 belong to the architect.** If the task has no `DESIGN_NOTE.md` that passes `precut.py` with its
   `## Stump core`, `## Build brief` and `generator/core.py`, spawn one `stump-architect` agent (its definition sets
   Fable 5.2 at xhigh; this invocation licenses it) with the task number, the subdomain, the analysis type, any
   starter kit path and, for a re-root, the paths of `runs/` and the reviews. Do no design work while it runs. When
   it returns: run `precut.py taskNN` and `python3 taskNN/generator/core.py` yourself (both exit 0, or the architect
   is resumed with the output), show the draw in ten lines with the core table, commit `DRAWN (taskNN)`, and carry
   on. **Do not stop for the author.** A build `/draw` already designed starts at stage 3.
2. **The brief is executed, not improved.** Read `## Stump core` and `## Build brief` before anything else. The
   generator imports the world from `generator/core.py` (its process, switches, sizes and estimators) and adds the
   organisation's systems, the files, the Layer 1 mess and the documents around it. If the cut pack breaks a core
   assertion, a route lands on the wrong side of its line, a member turns forced, or closing a fork would need a
   sentence that names a result's work, stop the stage and resume the architect (`SendMessage` to the same agent,
   or a new `stump-architect` briefed with the note and the failing figure). Never widen a margin, narrow a rival,
   file a method or add an effect to get a gate through.
3. **Stage 3 is left only when the free gates are green**: `python3 .claude/skills/build-pipeline/gates.py taskNN
   --full` (generator checks with every fork and the bar block R1 to R7 asserted, `verify`, two byte-identical
   builds, `effort.py` agreeing with the note, `figures_check.py`, `leak.py`, `audit_containers.py`, `guard.py
   surface` and `heart`), plus the realism sweep.
4. **Stage 4 spawns two agents in one message, in the background:** the leak reader (as `/leak-check` step 4
   describes, `model: sonnet`, `effort: medium`) and the `determinism-judge` agent in determinism mode (its
   definition sets Opus 5.5 at high; the platform's Holistic Audit v4, Step 0, Part A and Part B: it lists the
   deciding figures from the answer blocks, derives each from the pack before it compares, runs a fork list of
   twelve or more in code and never prices difficulty). This invocation licenses both. While they run, bring the card current and write the pre-ship
   check. Fix every finding from both in one generator pass; re-judge once only when a fix moved a graded figure,
   the prompt or the pack (an answer-block edit is not re-judged); re-read only if a document or the prompt
   changed.
5. **Stage 5, READY.** Every gate re-runs on the final cut (`gates.py taskNN`: `precut.py`, `effort.py`,
   `voice-check.py`, `leak.py`, `guard.py heart` and `surface`, `figures_check.py`, `audit_containers.py`); nothing
   is handed over on a skipped gate. Cut `target.zip`
   and the golden ZIP (exactly the files the prompt requests, each entry at its file's own save time), then run
   `audit_containers.py taskNN` on them and stop on any FAIL (`reduce-house-fixes` H1), set `status` `READY`, commit `READY (taskNN):
   <call>` and push.
6. **Repairs of the pack, the goldens and the blocks run in this thread; repairs of the core go to the
   architect** (step 2). Spawn a fresh build agent only near the context limit, briefed with `pipeline.json`, the
   design note and the findings.

**Write `pipeline.json` at every stage boundary** (with `status` and `updated`), and commit only at the status
changes `build-pipeline` names. A blocker is removed in this session (redraw the axis, re-root into another task
type and dataset inside the assigned subdomain, fix the generator), never left as a pause.

**Report at READY**, in this order: the committed answer, the results chain (each result, its area and the hurried
figure against the golden), the effort test (quick, careful but hurried and thorough scores, the largest single hint
and what it rescues), the hidden factor record's verdicts, the leak line (`leak.py` verdict and the reader's question
1), the duplicate line (heart verdict, nearest build), the judge's determinism verdict and disposition, the pair
estimate, the paths of `prompt.txt`, `target.zip` and the golden ZIP, and the four answer blocks ready
to paste from `submission.md`. Then tell the author the next step: rewrite the prompt in their own words (re-gated
with `voice-check.py taskNN --rewrite`), upload, generate the two runs, and run `/triage-runs taskNN` with them.

Create no file in the task folder other than the ones the skills name.
