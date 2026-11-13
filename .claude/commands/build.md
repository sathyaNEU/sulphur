---
description: Build one Sulfur task end to end (intake, draw, design gated by precut.py, build, leak reader and determinism judge together, ready for the platform) in this session's main thread. Takes a task number with the assigned domain and analysis type, or resumes a build from its pipeline.json.
argument-hint: taskNN <domain> <analysis type> [starter kit path] | new <domain> <analysis type> | resume taskNN | taskNN from <stage>
model: opus
effort: max
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

**Run the stages in order** in this thread, invoking each stage's skills before its work and leaving a stage only
when its gate holds.

1. **Do not stop for the author.** When the draw is filed, show it in ten lines (subdomain, task type and analysis
   type, the decision, where the weight sits, the answer shape, the results chain one line per result with its area
   and the hurried failure, the largest single hint and the results it rescues, the deliverables, the nearest build
   from `guard.py mechanisms` including the Mark cards, the guard verdict), commit `DRAWN (taskNN)`, and carry on. A
   failed gate is fixed and re-run without asking.
2. **Stage 2 is left only on `precut.py` exit 0.** A chain the careful but hurried pass mostly earns is redesigned,
   not argued; two failures on the results chain or the effort test re-root the draw before any data is cut. The
   rivals are run on the clean truth before the pack is cut: every defensible rival on every result lands inside its
   band or a named fact in the data rules it out.
3. **Stage 3 is left only when the free gates are green**: `python3 .claude/skills/build-pipeline/gates.py taskNN
   --full` (generator checks with every fork and the bar block R1 to R7 asserted, `verify`, two byte-identical
   builds, `effort.py` agreeing with the note, `figures_check.py`, `leak.py`, `audit_containers.py`, `guard.py
   surface` and `heart`), plus the realism sweep.
4. **Stage 4 spawns two agents in one message, in the background:** the leak reader (as `/leak-check` step 4
   describes, `model: sonnet`, `effort: medium`) and the `determinism-judge` agent (determinism only: it verifies
   the answer blocks against the prompt and the pack, never works the task on its own and never prices
   difficulty). This invocation licenses both. While they run, bring the card current and write the pre-ship
   check. Fix every finding from both in one generator pass; re-judge once only when a fix moved a graded figure,
   the prompt or the pack (an answer-block edit is not re-judged); re-read only if a document or the prompt
   changed.
5. **Stage 5, READY.** Every gate re-runs on the final cut (`gates.py taskNN`: `precut.py`, `effort.py`,
   `voice-check.py`, `leak.py`, `guard.py heart` and `surface`, `figures_check.py`, `audit_containers.py`); nothing
   is handed over on a skipped gate. Cut `target.zip`
   and the golden ZIP (exactly the files the prompt requests, each entry at its file's own save time), then run
   `audit_containers.py taskNN` on them and stop on any FAIL (`reduce-house-fixes` H1), set `status` `READY`, commit `READY (taskNN):
   <call>` and push.
6. **Repairs run in this thread.** Spawn a fresh agent only near the context limit, briefed with `pipeline.json`,
   the design note and the findings.

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
