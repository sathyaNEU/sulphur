---
name: draw
description: Design the core of one Sulfur task in the current thread following the stump-architect contract (stages 0 to 2). Finds the independent judgments that stump the review's strongest run, proves them in generator/core.py, registers the fingerprint card, writes DESIGN_NOTE.md to precut.py exit 0 with Stump core and Build brief, drafts a natural practitioner prompt.txt, commits DRAWN, and stops for /build. Also re-draws or repairs the core of a returned build.
---

# /draw

Execute the stump architect's contract in the current thread. Read `.agents/agents/stump-architect.md` and follow it as written (`stumping` Part 1d is the governing rule). The only difference from the spawned subagent is that the main thread also commits and pushes `DRAWN (taskNN)` when `precut.py` exits 0.

## Modes

- `taskNN <domain> <analysis type>` or `new <domain> <analysis type>`: stages 0 to 2 for a new build.
- `taskNN from 1`: a re-root. Read `DESIGN_NOTE.md` `## Tried and rejected`, `runs/`, and every review pasted there first; increment `architecture`; never re-point a landed scaffold (`stumping` Part 8).
- `taskNN repair <finding>`: a returned build whose core must change (not difficult enough, a forced member, or an unforced figure whose fork is the result's own difficulty). Redesign and re-prove the core in `generator/core.py`.

## Exit & Handover

When `python3 .agents/skills/stumping/precut.py taskNN` and `python3 taskNN/generator/core.py` both exit 0 (and `python3 .agents/skills/guide-to-prompt/references/voice-check.py taskNN` passes with 0 FAIL and 0 WARN):

1. Present the draw in ten lines, the core table (member, golden and band, family spread, hurried/direct/rigorous routes, opened by), what each route earns on the rubric (each stump lost alone, reflex, rigorous, four run routes), the referee/physics scores, and any assertion holding with tight margin.
2. Commit `DRAWN (taskNN)` on `main` with the task folder and `.agents/skills/fingerprint/cards/taskNN.json`, `git pull --rebase origin main`, and push.
3. Name the next step: `/build taskNN from 3`.

Do not build the pack, goldens, or `submission.md` in `/draw`. A core that does not hold is dropped and redrawn here.
