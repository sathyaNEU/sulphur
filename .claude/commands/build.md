---
description: Build one Sulfur task end to end (intake, draw, design gated by precut.py, build, leak reader and determinism judge together, ready for the platform) in this session's main thread. Takes a task number with the assigned domain and objective, or resumes a build from its pipeline.json.
argument-hint: taskNN <domain> <objective> [starter kit path] | new <domain> <objective> | resume taskNN | taskNN from <stage>
model: opus
effort: max
---

# /build

Run the pipeline for `$ARGUMENTS`. Invoke the `build-pipeline` skill first: the stages, gates, effort, commits,
`pipeline.json` and re-rooting are its business and are not restated here.

**Arguments.**

- `taskNN <domain> <objective>`: the number (`status.py new` gives the next free one, task1 up), the assigned
  Sulfur subdomain (one of the 21 in `guidelines/client/domains.txt`, mapped to its vocab key) and the objective.
  A starter data kit path, when the author claimed one, becomes the pack's spine candidate.
- `new <domain> <objective>`: the same with the next free number.
- `resume taskNN`, `taskNN from <stage>`: continue from `pipeline.json`, re-checking that stage's gate first.

**The Sulfur standard comes before anything else** (`CLAUDE.md`, first section). A new draw answers it in the card
and the design note's `## Deep reasoning` before the default path is written: the three or more dependent
inferences, the statistical or modeling judgment among them, the analyst test, the one-fact test, and one line per
banned stump showing it does not decide. A stump that is a plant, a field reading, an executed procedure, a replayed
figure, a single fact or an open reading is re-rooted, never resumed.

A build back from the platform is not a `/build`: `/triage-runs` reads the runs and routes it. A landed call comes
back here as `/build taskNN from 2` with the triage file in the design note.

**Run the stages in order** in this thread, invoking each stage's skills before its work and leaving a stage only
when its gate holds.

1. **Do not stop for the author.** When the draw is filed, show it in ten lines (subdomain and task type, the
   decision, the default path's answer against the golden, the deep chain in one line per inference, the shape,
   the deliverables, the nearest driver from `guard.py mechanisms` including the Mark cards, the guard verdict),
   commit `DRAWN (taskNN)`, and carry on. A failed gate is fixed and re-run without asking.
2. **Stage 2 is left only on `precut.py` exit 0.** A default path that ends on the golden is redesigned, not
   argued; two failures on the default path re-root the draw before any data is cut. The rivals are run on the
   clean truth before the pack is cut: every defensible rival method lands on the golden's call or a named fact
   in the data rules it out.
3. **Stage 3 is left only when the free gates are green**: generator checks with every fork asserted, `verify`,
   two byte-identical builds, `figures_check.py`, the realism sweep, `leak.py`, `guard.py surface` and `heart`.
4. **Stage 4 spawns two agents in one message, in the background:** the leak reader (as `/leak-check` step 4
   describes, `model: sonnet`, `effort: medium`) and the `determinism-judge` agent. This invocation licenses both.
   While they run, bring the card current and write the pre-ship check. Fix every finding from both in one
   generator pass; re-judge once on FIX_NOW; re-read only if a document or the prompt changed. Where the reader
   and the judge split on Gate H, recompute the easy routes on the clean truth and settle which kind of step
   decides before anything is handed over.
5. **Stage 5, READY.** Every gate re-runs on the final cut (`precut.py`, `voice-check.py`, `leak.py`,
   `guard.py heart` and `surface`, `figures_check.py`); nothing is handed over on a skipped gate. Cut `target.zip`
   and the golden ZIP (exactly the files the prompt requests, each entry at its file's own save time), then run
   `audit_containers.py taskNN` on them and stop on any FAIL (`reduce-house-fixes` H1), set `status` `READY`, commit `READY (taskNN):
   <call>` and push.
6. **Repairs run in this thread.** Spawn a fresh agent only near the context limit, briefed with `pipeline.json`,
   the design note and the findings.

**Write `pipeline.json` at every stage boundary** (with `status` and `updated`), and commit only at the status
changes `build-pipeline` names. A blocker is removed in this session (redraw the axis, re-root into another task
type and dataset inside the assigned subdomain, fix the generator), never left as a pause.

**Report at READY**, in this order: the committed answer, the default path's answer and the deep chain, the
`## Deep reasoning` lines for the analyst test and the one-fact test, the leak line (`leak.py` verdict and the
reader's question 1), the duplicate line (heart verdict, nearest build), the judge's verdict and Gate G line, the
paper pair estimate, the paths of `prompt.txt`, `target.zip` and the golden ZIP, and the four answer blocks ready
to paste from `submission.md`. Then tell the author the next step: upload, generate the two runs, and run
`/triage-runs taskNN` with them.

Create no file in the task folder other than the ones the skills name.
