---
description: Repair a build where a run took a defensible alternative (triage FIX_DETERMINISM), the determinism judge found a fork, or a reviewer returned it as not deterministic, while the stump held. Closes the judges' fork in the record so the literal reading is the golden, without moving the main call, the stump, the ladder or any graded figure, proves the scope with freeze.py, re-judges once, and re-ships.
argument-hint: taskNN <the finding: the run's alternative method, the judge's fork or the reviewer's note>
model: opus
effort: max
---

# /fix-determinism

The build named in `$ARGUMENTS` has an open reading: a run took a sound method the prompt allows and reached
another answer, or a judge or reviewer found two defensible answers. The job is
to make the shipped text, read literally, land on the golden it already has. The stump and the rubric are
what passed; they are not touched.

Invoke `determinism-check` and `build-pipeline` first. If the finding is not in `$ARGUMENTS`, read it from
`runs/triage.md` or `pipeline.json` (`portal`, `returned`) or ask once and stop.

**1. Freeze before any edit.**
`python3 .claude/skills/build-pipeline/freeze.py snapshot taskNN`. Read the design note's `## Semantic fork
table`, `## Closure table`, `## Literal reader` and `## Tried and rejected`.

**2. Classify the finding** against the gates (`determinism-check` §6) and write it as a new fork-table row
(`SFn`): the term or convention, the golden reading, each reading the judges took, and the call or figure
under each.

- `semantic_fork`, `underspecified_objective`, `competing_defensible_answer`: a reading the record leaves open.
- `prompt_ambiguity`: an ask or the decision worded two ways.
- `solution_incorrect`, `missing_input_data`, `answer_contradicts_files`: a figure that does not recompute
  from the shipped files, or a fact the golden uses that no file carries.

**3. The fork-is-the-result test and the banned list, before choosing a move.** A closure that files the method
makes that result rule application, which the client bans whatever the determinism verdict (`CLAUDE.md`, first
section). Close the WHAT, never the HOW. Then ask whether the fork *is* a result's difficulty: does the golden's
lead over the hurried figure at that result come from the reading rather than from the analysis? If closing the fork
in either direction puts the hurried pass inside the result's band, the difficulty lived in the fork (eight builds
died this way). **Stop**: write the line in `## Tried and rejected`, set `pipeline.json` `status` `DESIGN`, and
report that this result is redesigned (`/build taskNN from 2`), not pinned. A fork whose fix is a wider band is
closed by widening the band to what the honest family shares, then `effort.py` re-run: a band that now holds the
hurried figure grades nothing, and the result is redesigned. Never keep a fork open to keep a difficulty.

**4. Close it with the strongest move that holds** (`determinism-check` §3):
- **C1 converge:** align the records so every reading selects the same rows and the same figure; asserted on
  the figure and the counts. Preferred, because it adds no sentence.
- **C2 confirm / C3 corridor / C4 separate**, in that order, as the closure table defines them.
- **A pin at authority, once:** one filed sentence in the governing document (never the prompt, which
  carries the question and no convention) that fixes the WHAT (population, window, unit, inclusion,
  rounding), never the HOW. Read the exact wording as the runs would: a pin that names a result's quantity or
  step, or only makes the solver ask the question, hands that result over (`stumping` Part 5); reword it or use
  C1.
- A figure that does not recompute is fixed in the generator so `figures.json`, the golden and the write-up
  agree; the write-up is redrafted from `figures.json` (`submission-writeup`).
- `prompt_ambiguity` on an ask: tighten that ask's wording only, unit and rounding kept, `voice-check.py`
  green. The prompt's call sentence is frozen.

**5. Assert, rebuild, prove the scope.** Add the `SFn` row to `checks.py` and `verify.py`, rebuild twice
(byte-identical), then the free gates: generator checks, `verify`, `figures_check.py`, `precut.py`,
`leak.py`, `voice-check.py`, `guard.py validate` and `heart`. Then:

```
python3 .claude/skills/build-pipeline/freeze.py check taskNN --mode determinism
```

Exit 1 means a frozen item moved: undo that change and find a closure that does not move it. Only when the
golden itself was the non-literal figure (a `solution_incorrect` the author accepts) is a move allowed, with
`--allow <figures.json key>` and the reason in the fork-table row.

**6. Re-judge once.** Spawn the `determinism-judge` agent (medium effort in its definition) on the rebuilt
bundle; this command licenses that one pass. APPROVE: go on. FIX_NOW: repair in this thread, rerun step 5,
and ship without a third judge only if the finding is the same fork closed further. SEND_BACK: stop and
report; it is a redesign.

**7. Re-ship.** Re-cut `target.zip`, append to `pipeline.json` `returned` (`repair: "determinism"`), set
`status` `READY`, one `## Tried and rejected` line naming the fork and the move, and commit `RESHIPPED (taskNN): determinism, <the fork closed>` with the zip and `golden/` force-added
(`CLAUDE.md`, Git). The author uploads the new pack, regenerates the runs and runs `/triage-runs`.

**Report:** the fork in one line, the move used, the `freeze.py` verdict, the judge's verdict, the zip path.
No leak reader (unless a document's wording changed near the decisive step), no solver.
