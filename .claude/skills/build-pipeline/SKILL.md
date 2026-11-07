---
name: build-pipeline
description: "The stage machine from an assigned Sulfur domain to a submitted task: intake, draw, design (precut.py), build, the leak reader and judge together, ready for the platform, the two runs triaged, submit. Owns pipeline.json, the stage gates, effort per role, the commit points, the run triage and its routes (/fix-determinism, /fix-rubric, a surface trigger made texture, redesign), freeze.py, status.py and re-rooting. Invoked by /build, /triage-runs, the two fix commands, and when resuming a build in flight."
---

# Build pipeline

Every gate is a script's exit status or a thread's verdict; no thread runs before the free gates pass. One session
carries a build end to end in its main thread at max effort. Spawned agents exist only where isolation is the point
(the leak reader and the judge must not have seen the design; the run triage must not be the designer arguing for
its own stump) and run at medium. There is no solver round: stump power is argued on paper (`precut.py`), checked by
the leak reader and the judge's Gate F, and measured by the platform's two runs.

## The stages

| # | Stage | Skills | Gate to leave the stage |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | the assigned subdomain and objective named; a starter data kit claimed or a real public spine found (`dataset-generation` §2); `taskNN` from `status.py new`; `pipeline.json` with `status` `DRAWING` |
| 1 | draw | `guide-to-prompt`, `stumping`, `fingerprint` (`mechanisms`, `check`, `register`, `names`) | card at PASS or answered WARN against every card, the Mark baseline included; **the Sulfur standard answered first** (`stump_class` analytical, the analyst test naming the easy route's wrong answer, the deep chain of three or more inferences with its judgment named, the one-fact test); both layers named; people drawn; the default path ending on a wrong answer; commit `DRAWN (taskNN)` |
| 2 | design | `stumping` (screen, fork table, 3 to 5 rungs), `determinism-check` (closure), `supplemental-stumping`, `guide-to-prompt` | **`precut.py taskNN` exit 0** (runs `voice-check.py`); every defensible rival method run on the clean truth and landing on the golden's call or ruled out by named data |
| 3 | build | `dataset-generation`, `determinism-check`, `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `leak-check`, `fingerprint` | generator green, every fork asserted, the Sulfur block (`dataset-generation` §7.1) green; `verify`; two byte-identical builds; the input gates; `metadata.json`; `figures_check.py` exit 0; realism sweep; house-fix register; `leak.py` not LEAK; `guard.py surface` clean and `heart` not BLOCK |
| 4 | check | `leak-check` (reader), `determinism-check` (judge) | both spawned in one message, in the background. Reader: no deep-step sentence, no helping file, quoted sentences execute to the golden, no main-call fork. Judge: APPROVE with Gate H passing H1 to H5. Every finding fixed in the generator in one pass, stage 3 gates re-run; FIX_NOW re-judged once; the reader re-runs only if a document or the prompt changed. SEND_BACK: re-root |
| 5 | ready | `fingerprint`, `reduce-house-fixes`, `submission-writeup` | the pre-ship check in the design note, the Sulfur standard re-read against the built pack; **every gate re-run on the final cut** (`precut.py`, `voice-check.py`, `leak.py`, `guard.py heart` and `surface`, `figures_check.py`); `target.zip` and the golden ZIP (exactly the requested files) from the final rebuild; card current; `status` `READY`; commit `READY (taskNN): <the call>` with both zips and `golden/` force-added; the author handed the prompt, the pack, the golden ZIP and the four answer blocks |
| 6 | runs | the author, `/triage-runs` (the `run-triage` agent) | both runs' full text and the generated rubric saved under `runs/`; both scores and the average recorded; each run's first wrong step classed; the route taken (below) |
| 7 | submit | the author | triage `SUBMIT`; the Reward block filled from `pipeline.json`; `status` `SUBMITTED`; commit `SUBMITTED (taskNN): <call>, runs <x> and <y>, average <z>`; later `APPROVED` or `RETURNED` from the review |

Back to design: a reader finding a deep-step sentence or a main-call fork; a FIX_NOW that moves the decisive path;
a triage `REDESIGN`; a review return that says the stump was surface or the domain a backdrop.

## Effort per role

| Role | Where | Effort |
|---|---|---|
| The build session (design, build, every repair) | `/build`, `/fix-determinism`, `/fix-rubric` | max, set in the command |
| Leak reader | stage 4, `/leak-check` | medium (`general-purpose`, `model: sonnet`, `effort: medium` on the call) |
| `determinism-judge` and its thread | stage 4, `/fix-determinism` | medium (agent definition) |
| `run-triage` | stage 6, `/triage-runs` | medium (agent definition) |
| `/approve` | author sign-off before upload | medium |

## Running the stages

- **One thread.** Design and build are one hand; a repair runs where the context already is. Spawn a fresh agent for
  a repair only when the session is near its context limit, briefed with `pipeline.json`, the design note and the
  finding.
- **Stage 4 spawns the reader and the judge together** (same pack, neither changes it). While they run, update the
  card and write the pre-ship check. Collect both reports, fix everything in one generator pass, rebuild, and relay
  nothing structural until both are in. Where they disagree on what a shipped sentence licenses, the judge
  recomputed and the reader did not, so the judge settles it. A reader finding is evidence of what a solver sees,
  which is Gate F, not Gate C.
- **The free gates come first, always:** nothing with a token cost runs on a pack the scripts have not passed.
- **No author checkpoints before READY.** The draw is shown in ten lines and the build carries on; the author can
  stop or redraw at any point, and `/approve` remains for a manual sign-off before upload.

## Stage 6: reading the runs

The platform generates two runs from the prompt and `target.zip` (it can take more than twenty minutes), generates the
rubric from the prompt and the answer blocks, and grades both. `/triage-runs` saves the runs and the rubric under
`runs/`, records the scores, and spawns `run-triage`, which classes the **first** place each run went wrong on the
client's table (`guidelines/client/deep-reasoning.txt`). The routes:

| Triage verdict | When | Route |
|---|---|---|
| `SUBMIT` | average under 60, the counterfactual average (surface and formatting losses given back) under 60, no run's first wrong step a surface class | fill the Reward block, submit, `SUBMITTED` |
| `FIX_DETERMINISM` | a run took a sound method the prompt allows to another answer | `/fix-determinism`; then new runs |
| `SURFACE_RISK` | a run's first wrong step is a missed planted detail, a misread field or clause, a misapplied written procedure, or a formatting slip | the trigger is made texture in the generator (unmissable, or off every graded path); the deep step is untouched; then new runs |
| `FIX_ASKS` | at least one run off the call, the average 60 or more from asks the off-call run still collected | `/fix-rubric`; then new runs |
| `REDESIGN` | both runs landed the call at 60 or more, or the only losses were surface | `## Tried and rejected` line, `status` `DESIGN`, `/build taskNN from 2` |
| `RUBRIC_EDIT` | a generated criterion is clearly wrong or missing and fixing it moves the verdict | the author edits that criterion on the platform and re-runs the evaluation |

**Reading a landed call** (back to stage 2 with this session as designer). Read each run against the default path and
the rungs; it left the ladder after the last rung it shows:
- walked the default path to the golden: redesign the deep step, never add a rung above it;
- never saw the rung, yet landed: discriminator dominance failed, fix the magnitudes;
- saw the rung and declined it: the evidence was not decisive enough in the data; strengthen what the data show,
  never file the method;
- executed the rung as a work order: it was announced; the leak sweeps and readability screen find where;
- missed only on a misread field or misapplied rule: a surface rung, not the stump; redesign.

Every run triaged adds a row to `stumping/references/sulfur-record.md`: the Sulfur run record is the evidence the
next draw reads first, beside Mark's measured record.

## Commits

Commit only at a status change: `DRAWN`, `READY`, `SUBMITTED`, `APPROVED`, `RETURNED`, `RESHIPPED`, `PAUSED`,
`RETIRED` (`CLAUDE.md`, Git). Each commit stages its paths by name: the task folder,
`.claude/skills/fingerprint/cards/taskNN.json`, the run record row, and from READY on `git add -f taskNN/target.zip
taskNN/golden/ taskNN/golden.zip`. Then `git pull --rebase origin main` and push. Nothing is committed between those
points; a session that stops mid-stage writes `pipeline.json` with a `resume` line and commits `PAUSED`. A blocker is
never a reason to stop: the session that meets it removes it (a redraw, a re-root into another task type and dataset,
a generator fix) and carries the build on.

## Returned tasks

**Every return re-ships on the regular checks only** (`CLAUDE.md`, the STOP block): the fix in the generator, the
free gates, the determinism judge, the leak check (`leak.py` and the one leak reader) and the duplicate check
(`guard.py heart` and `surface`), then new platform runs and `/triage-runs`. No solver, scored reader or probe is run.

Every repair keeps every free gate (generator checks, `verify`, byte-identical rebuilds, `leak.py`, `guard.py
validate` and `heart`, `voice-check.py` at `.claude/skills/guide-to-prompt/references/voice-check.py`,
`figures_check.py`, `precut.py`) and proves its scope with `freeze.py`. Each attempt gets a `## Tried and rejected`
line, re-cuts both zips, appends to `returned`, sets `status` `READY`, commits `RESHIPPED (taskNN)`, and counts as a
loop against the architecture.

**Before any determinism repair, the fork-is-the-stump test** (`/fix-determinism` step 3; `stumping` 1.2): if the
sentence that would close the fork names the thing the deep step recognises, the fork is the stump and the build goes
to stage 2, never to a pin. In Mark, pins that fixed population, window, unit or schedule and named no method turned
returns into approvals (169, 135, 151, 162); pins naming the clock, window or test the stump rides on landed the call
on the next round (141, 179 v3, 181 v2, 118 v2). No approved build was ever repaired by hardening the asks alone after
a landed call, and a rung stacked above the solved step never held.

**The Sulfur gate on every rework, before any resume.** The card carries `stump_class: analytical`, `analyst_test`,
`domain_test` and the deep chain, with no official or validated decoy flag; the note's `## Deep reasoning` passes
`precut.py`. A design whose deciding step is a plant, a field reading, an executed procedure, a replay, a single fact
or an open reading is re-rooted at stage 1, never resumed.

## `freeze.py` and `status.py`

- **Pick the mode whose contract matches the repair's scope, and if none matches, say so rather than manufacturing a
  pass.** `--mode determinism` appends any changed Supplementary Questions block to its findings unconditionally, on
  the premise that a determinism repair moves no graded figure, and `--allow` reaches only `figures.json` keys. So a
  determinism finding whose fix changes an asking sentence's unit or an ask's figures cannot be proved by that mode;
  the control there is `--mode rubric` plus a fresh `snapshot` at the repair's end. Editing `freeze.py` or retaking
  the snapshot to clear a mode the repair was always going to fail manufactures a pass on the author's own control:
  record both commands and both outputs instead, and let the author pick.
- `freeze.py snapshot taskNN` before the first edit of a fix; `freeze.py check taskNN --mode determinism` or `--mode
  rubric` after the rebuild. It freezes the Final Recommendation and Critical Components numbers, the figures.json
  keys carrying them, the stump sentence, the card's stump and driver, the design note's ladder and default path, and
  the prompt's call sentence; in determinism mode also every Supplementary Questions number.
- `status.py` prints every Sulfur build with its status and runs; `status.py next` the build to work next (returned,
  paused and in-runs builds first); `status.py new` the next free number (task601 up); `status.py taskNN` one build.

## `pipeline.json`

The one state file in a task folder: where the build is, never why.

```json
{"task": "task601", "status": "BUILD",
 "domain": "<vocab domain key>", "subdomain": "<the assigned Sulfur subdomain>", "objective": "forecasting",
 "stage": 3, "stage_name": "build", "updated": "2026-11-07",
 "call": "the committed recommendation in one line",
 "stump": "the stump sentence",
 "architecture": 1, "loops": 0,
 "precut": {"exit": 0, "date": ""},
 "leak": {"leak_py": "", "reader": ""},
 "duplicate_check": {"heart": "", "nearest": ""},
 "judge": {"verdict": "", "disposition": "", "gate_h": "", "report": ""},
 "paper_pair": null,
 "runs": {"run1": null, "run2": null, "average": null, "counterfactual_average": null,
          "first_wrong_step": {"run1": "", "run2": ""}, "triage": "", "recorded": "", "history": []},
 "returned": [{"date": "", "source": "triage | review", "repair": "determinism | rubric | surface | design", "commit": ""}],
 "resume": "", "approved": null, "submitted": null,
 "portal": {"status": "", "date": "", "note": ""}}
```

`status` is one of `DRAWING`, `DESIGN`, `BUILD`, `READY`, `RUNS`, `SUBMITTED`, `APPROVED`, `RETURNED`, `PAUSED` (the
session ended mid-stage; never a waiting state), `RETIRED`. `/approve` sets `approved`.

## Resuming

Read `pipeline.json` (`status`, `stage`, `resume`), then the design note's `## Tried and rejected`, then `runs/` if
it exists; re-check that stage's gate before new work. A `RETURNED`, `PAUSED` or `RUNS` build is taken before any new
number, and `status.py next` names it first.

## Re-root and retirement

An architecture is **spent** when the judge returns SEND_BACK, a FIX_NOW fails its second pass, two triage rounds
return `REDESIGN`, or `precut.py` fails twice on the default path (re-root before any data is cut). A hardening deepens
Layer 2 and never plants; if only a plant would hold, the architecture is spent.

**Re-root:** a new draw at stage 1 in the same subdomain and number, `architecture` incremented, `loops` reset, the
old card's lineage saying spent and why, one line in `## Tried and rejected`, committed `DRAWN`. **One architecture
per world:** once a world's deep step is spent the next draw moves to another world, another dataset and another
shell (Mark: 251, 249 and 269 each spent two architectures in one world where one would have; 118, 305 and 273 kept
one prompt shell across every re-root and `guard.py check` now blocks it). **No same-day serial re-roots without new
evidence**: a re-root needs the runs, the judge or the leak reader to have killed the version it replaces. A build is
**retired** only on the author's word: a `## Retired` section in the design note, `status` `RETIRED`, every card kept,
committed `RETIRED`.

## Throughput

The platform's tier sets how many tasks may be open at once (Tier 1 one, Tier 2 three, Tier 3 six, Tier 4 no
limit). While a build waits on its runs (stage 6), the next build may be drawn if the tier allows it. The moment a
build is submitted, the next draw starts on the author's word.
