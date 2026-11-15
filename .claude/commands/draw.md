---
description: Design the core of one Sulfur task in this thread on the strongest model (the stump architect's contract, stages 0 to 2). Finds the judgments that stump the review's strongest run, proves them in generator/core.py, registers the card, writes the design note to precut.py exit 0 with its Stump core and Build brief, drafts the prompt, and stops for /build. Also re-draws the core of a returned build.
argument-hint: taskNN <domain> <analysis type> [starter kit path] | new <domain> <analysis type> | taskNN from 1 | taskNN repair <the send-back or the triage finding>
model: fable
effort: xhigh
---

# /draw

Do the stump architect's work for `$ARGUMENTS` in this thread. Read `.claude/agents/stump-architect.md` and follow it
as written: it is the whole contract, and `stumping` Part 1d is the rule behind it. The only difference from the
spawned agent is that you are the main thread, so you also commit.

- `taskNN <domain> <analysis type>` or `new ...`: stages 0 to 2 for a new build.
- `taskNN from 1`: a re-root. Read the build's `## Tried and rejected`, its `runs/` and every review pasted there
  first; `architecture` goes up by one; a landed scaffold is never re-pointed (`stumping` Part 8).
- `taskNN repair <finding>`: a returned build whose core has to change (not difficult enough, a forced member, a
  figure the audit found unforced whose fork is the result's own difficulty). The world is kept only where the
  reviewer asked for it; the core is redesigned and re-proved in `generator/core.py`.

When `precut.py taskNN` exits 0: show the author the draw in ten lines, the core table (member, golden and band,
family spread, the hurried, direct and rigorous routes, opened by), the referee and its scores, and any assertion
that holds with little room. Commit `DRAWN (taskNN)` on `main` with the task folder and the card, push, and name the
next step: `/build taskNN from 3`.

Do not build the pack, the goldens or `submission.md` here. A core that will not hold is dropped and redrawn in this
thread, never handed on.
