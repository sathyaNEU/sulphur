---
description: Repair a build whose runs lost their points for analytical reasons but whose two-run average came back at 60 or more, because the runs earned results whose only difficulty was a reflex or the losses sat on too few results. Rebuilds or replaces those results so the careful but hurried pass loses more of the chain, with the results that held frozen; proves the scope with freeze.py and effort.py and hands back for new runs.
argument-hint: taskNN [nothing if runs/triage.md carries the result]
model: opus
effort: high
---

# /fix-rubric

The build named in `$ARGUMENTS` came back from `/triage-runs` with `FIX_ASKS`: the runs' losses were analytical,
and the average still reached 60 because they earned results the design priced as lost, or their losses sat on one
or two results. The job is to make more of the chain need work beyond the runs' reflexes, so a careful run in a
hurry loses more results, in different areas, for analytical reasons. The results that held (the ones both runs
lost for the reason the chain names) are not touched.

**The core is the architect's.** Which results are rebuilt and what each now turns on is a design judgment:
spawn one `stump-architect` agent with `runs/triage.md` (the stronger run's earned results first) and let it rework
`generator/core.py`, the note's `## Stump core` and the `## Build brief`; this thread then executes the brief at
Opus 5.5 high and proves the scope.

Invoke `supplemental-stumping` (Parts 0, 1 and 6), `stumping` (Parts 1 to 3) and `build-pipeline` first. Read
`runs/triage.md`, `runs/rubric.md` and both runs; if they are missing, run `/triage-runs` first and stop.

**1. Freeze before any edit.** `python3 .claude/skills/build-pipeline/freeze.py snapshot taskNN`. Read the results
chain, the effort test and `## Tried and rejected`.

**2. Read where the points went.** From the loss map: every result both runs earned, and why they could (its only
difficulty was the textbook method, a pattern one plot shows, a holdout or a bootstrap; a filed sentence handed it
over; it restated another result's fit), and every criterion a run passed without the result's work (a formatting or
instruction criterion, a cleaned total). Points a run lost to a surface cause are a `SURFACE_RISK` finding, not a
lever.

**3. Rebuild the earned results** (`supplemental-stumping` Part 6):
- **Rebuild a reflex result around the move beyond it**: the same quantity asked where this world breaks a
  precondition of the textbook method, or where its output has to be carried somewhere the method does not go (into
  a weighted decision, a band that covers, a bridge that reconciles).
- **Or replace it with a consequence of a stump the runs lost** (`supplemental-stumping` Part 1 rule 3: the
  estimate for every member, carried one step further, the rejected option on the same footing, the distance to the
  line), so the figure falls with that stump. A figure with no stump on its path leaves the prompt and the blocks;
  its work stays in the Step-by-Step.
- **Read the triage's earned map first**: every criterion the higher-scoring run earned is either instruction-following,
  a figure no stump touches (cut), or a figure a lost stump moved by less than its band (replace).
- **Critical components are the decisive steps' answers** (the client's guidelines of 11/20): one per stump, each
  that stump's own figure stated as the answer with no method clause, sitting in a deliverable the prompt asks for,
  and independent, so a run that loses one stump still earns the others (`corelib.py`, the row `critical components
  independent`). A figure that falls with two stumps or more is an ask, never a component.
- **One to four asks, each hard and multi-faceted**: a rebuilt result joins an existing ask as one more facet (a
  row, a period, a member) before it becomes a new ask; a long list of easy asks is a send-back by name.
- **No result is won or lost on a surface cause**: no result turns on a field reading, a filed rule, a planted row or
  a built-in factor. Mess stays texture or an assembly result of its own.
- Change the prompt's wording only where a result must be asked differently, with its unit kept, no rounding instruction added, and
  `leak.py` and `voice-check.py` green; the author re-voices the prompt afterwards.
- Never touch the results that held, the files they read, or the Final Recommendation unless the call rests on a
  rebuilt result.

**4. Assert, rebuild, prove the scope.** `checks.py` asserts the bar block (R1 to R7) for every rebuilt result: the
hurried figure outside its band, the rivals inside it, no one thing. The generator rewrites `effort.json`; `effort.py`
shows the careful but hurried pass losing more of the chain and the pair estimate at 50 or under. Rebuild twice
(byte-identical), redraft the Supplementary Questions and Critical Components blocks from `figures.json`
(`submission-writeup`), then `python3 .claude/skills/build-pipeline/gates.py taskNN --full`. Then:

```
python3 .claude/skills/build-pipeline/freeze.py check taskNN --mode rubric
```

Exit 1 means a result that held moved: undo it. A PASS that reports no ask file moved changed nothing graded.

**5. Hand back.** Re-cut `target.zip` and the golden ZIP, append to `pipeline.json` `returned` (`repair:
"rubric"`), set `status` `READY`, one `## Tried and rejected` line per result rebuilt (what the runs did to the old
one), and commit `RESHIPPED (taskNN): results rebuilt, <which>` with the zips and `golden/` force-added. The author
uploads the new pack and answer blocks, regenerates the runs and runs `/triage-runs` again.

**Report:** the pair estimate before and after (`effort.py`), the results rebuilt or replaced and the area each now
sits in, the critical components changed, the `freeze.py` verdict, the zip paths. No judge unless a result's wording
changed in the prompt, no solver.
