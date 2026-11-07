---
description: Repair a build whose main call held for at least one run but whose two-run average came back at 60 or more because the asks were collected. Re-couples the asks to the deep step so a run off it loses them for the same analytical reason, with the main recommendation frozen; proves the scope with freeze.py and hands back for new runs.
argument-hint: taskNN [nothing if runs/triage.md carries the result]
model: opus
effort: max
---

# /fix-rubric

The build named in `$ARGUMENTS` came back from `/triage-runs` with `FIX_ASKS`: at least one run missed the deep
step, and the average still reached 60 because that run collected points the deep step should have cost it. The job
is to make every graded figure downstream of the deep step, so a run that skips it loses them for the analytical
reason it already lost the call for. The main recommendation is what held: its sentence, its figures, its ladder and
the rows it reads are not touched.

Invoke `supplemental-stumping` (Parts 0, 1 and 6) and `build-pipeline` first. Read `runs/triage.md`,
`runs/rubric.md` and both runs; if they are missing, run `/triage-runs` first and stop.

**1. Freeze before any edit.** `python3 .claude/skills/build-pipeline/freeze.py snapshot taskNN`. Read the ask
sheet and `## Tried and rejected`.

**2. Read where the points went.** For the run off the call, list every criterion it passed and why it could: an
ask computed from rows the deep step never touches, a figure a filed sentence handed it, a critical component that
is a cleaning or counting result rather than the deep step's output, a formatting or instruction criterion. For
the run on the call, list what it lost; points it lost to a surface cause are a `SURFACE_RISK` finding, not a lever.

**3. Redesign the ask layer** (`supplemental-stumping` Part 6):
- **Re-site each collected ask downstream of the deep step**: the same stakeholder question asked of the quantity
  the deep step produces, across many units, periods or cells (the answer's shape), so the shallow analysis files a
  different value in every cell. An ask that cannot be made to depend on the deep step is dropped, never kept as a
  freebie.
- **Critical components carry the chain**: each of the 2 to 5 is a link of the deep chain (the comparison chosen,
  the estimate it gives, the adjustment's size, the decision quantity), never a row count or a cleaned total.
- **No ask is won or lost on a surface cause**: no ask turns on a field reading, a filed rule or a planted row. Mess
  stays texture on every ask path.
- Change the prompt's ask wording only when an ask must be re-sited, with unit and rounding kept and `leak.py` and
  `voice-check.py` green; the call sentence is frozen. The author re-voices the prompt afterwards.
- Never touch the main call's rows, the files it reads, the ladder, the deep step or the Final Recommendation.

**4. Assert, rebuild, prove the scope.** `checks.py` asserts that the shallow path (the default path's method)
misses every re-sited ask figure outside its rounding bin, and that every main-call figure recomputes unchanged.
Rebuild twice (byte-identical), redraft the Supplementary Questions and Critical Components blocks from
`figures.json` (`submission-writeup`), then the free gates: generator checks, `verify`, `figures_check.py`,
`precut.py`, `leak.py`, `voice-check.py`, `guard.py validate` and `heart`. Then:

```
python3 .claude/skills/build-pipeline/freeze.py check taskNN --mode rubric
```

Exit 1 means the main side moved: undo it. A PASS that reports no ask file moved changed nothing graded.

**5. Hand back.** Re-cut `target.zip` and the golden ZIP, append to `pipeline.json` `returned` (`repair:
"rubric"`), set `status` `READY`, one `## Tried and rejected` line per ask replaced (what the run did to the old
one), and commit `RESHIPPED (taskNN): asks re-coupled, <which>` with the zips and `golden/` force-added. The author
uploads the new pack and answer blocks, regenerates the runs and runs `/triage-runs` again.

**Report:** the paper pair estimate before and after (`supplemental-stumping` Part 0), the asks re-sited, the
critical components changed, the `freeze.py` verdict, the zip paths. No judge unless an ask's wording changed in
the prompt, no solver.
