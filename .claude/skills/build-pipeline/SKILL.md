---
name: build-pipeline
description: "The stage machine from an assigned Sulfur domain and analysis type to a submitted task: intake, draw, design (precut.py on the results chain), build (effort.py on the generator's passes), the leak reader and judge together, ready for the platform, the two runs triaged result by result with the platform's Holistic Audit v4 replayed beside them, submit. Owns pipeline.json, the stage gates, gates.py (every free gate in one pass), effort per role, the commit points, the run triage and its routes (/fix-determinism, /fix-rubric, a surface trigger rebuilt as analysis, redesign), freeze.py, status.py and re-rooting. Invoked by /build, /triage-runs, /holistic-check, the two fix commands, and when resuming a build in flight."
---

# Build pipeline

Every gate is a script's exit status or a thread's verdict; no thread runs before the free gates pass. A build has
two hands: the **stump architect** designs the core on the strongest model at its highest effort (stages 0 to 2,
`stumping` Part 1d), and the **build** executes the architect's brief in the session's main thread on Opus 5.5 at high
(stages 3 to 5). The other spawned agents exist where isolation is the point (the leak reader and the judge must not
have seen the design; the run triage must not be the designer arguing for its own design). There is no solver round: difficulty is screened on paper before any code (the
stump screen), argued in the note (`precut.py`), computed from the generator's own passes (`effort.py`) and measured
by the platform's two runs; the judge replays the platform's Holistic Audit v4 (determinism only before the runs,
the whole audit on them) and the leak reader checks leaks only. **`python3 .claude/skills/build-pipeline/gates.py taskNN`** runs every free gate in one
pass (precut, effort, voice-check, leak, figures, containers, guard heart and surface) and prints one summary.

## The stages

| # | Stage | Skills | Gate to leave the stage |
|---|---|---|---|
| 0 | intake | `fingerprint` (`recent`, `coverage`) | the assigned subdomain and analysis type named; the data route chosen (a simulated process or a public source, `dataset-generation` §2); `taskNN` from `status.py new`; `pipeline.json` with `status` `DRAWING` and `"doctrine": "throughout"` |
| 1 | draw (the architect) | `guide-to-prompt`, `stumping`, `fingerprint` (`mechanisms`, `slots`, `check`, `register`, `names`; `skeleton.py closed`) | the observation process written and the unobserved part of the decision's quantity named (`stumping` Part 1d); the client's guidelines of 11/20 and its closed strategies read (`guidelines/client/guidelines-2026-11-20.md`; `guidelines/client/learning-modules/overused-strategies-2026-11-21.md`, 45 cards, `stumping` Part 1c) and the two or three decisive steps chosen off them, none a closed card's fix; **the stump screen passed on paper** (`stumping/references/stump-screen.md`: five or more candidate traps written, each through the twenty tests, the three strongest that open different members kept, the four run routes implemented and landing wrong on both sides of a line) and **proved in `generator/core.py`** (the truth, the golden, the hurried, direct and most rigorous standard routes, the lattice of shortcuts, the referee's scores and the variant battery, ending on `stumping/corelib.py`'s `CORE PASS level 4` or `5`; found by `stumping/references/core-method.md`) before the card is registered; the client's strategies for the domain group read (`stumping/references/sulfur-strategies.md`); the weight and answer shape not leaned on recently; card at PASS or answered WARN against every card, the Mark baseline included, carrying `answer_shape`, `weight` and `chain_signature`; the results chain sketched (four or more results, three or more areas) with the one-fact test answered; people drawn; commit `DRAWN (taskNN)` |
| 2 | design (the architect) | `stumping` (the results chain, the hidden factor record, the effort test, **the stump factorial, Part 3.3**, **the core, Part 1d**), `determinism-check` (bands, closure), `supplemental-stumping`, `guide-to-prompt` | **`precut.py taskNN` exit 0** (runs `voice-check.py`) with `## Stump core` and `## Build brief` written and `python3 taskNN/generator/core.py` exit 0; its `## Stump factorial` read off core.py: two or more stumps each necessary, none sufficient alone on the reflex route, or the draw dies on paper; **the rubric priced by core.py** (`supplemental-stumping` Part 0: a run that loses any one stump earns 50 or under, the reflex route 30 or under, the rigorous standard route 50 or under), with the prompt asking only for figures downstream of the stumps; every defensible rival on every result run on the clean truth and landing inside its band or ruled out by named data |
| 3 | build (this thread, executing `## Build brief`) | `dataset-generation`, `determinism-check`, `submission-writeup`, `golden-realism`, `reduce-house-fixes`, `leak-check`, `fingerprint` | generator green, every fork asserted, the bar block (`dataset-generation` §7.1, R1 to R7) green; **`effort.py taskNN` exit 0** with the note agreeing; `verify`; two byte-identical builds; the input gates; `metadata.json`; `figures_check.py` exit 0; realism sweep; house-fix register; **`audit_containers.py taskNN` exit 0** (`reduce-house-fixes` H1: every container from the house writers, distinct stamps); `leak.py` not LEAK; `guard.py surface` clean and `heart` not BLOCK |
| 4 | check | `leak-check` (reader), `determinism-check` (judge) | both spawned in one message, in the background. Reader: no sentence that hands over a result's step, no helping file, quoted sentences execute to the golden, no fork on any result. Judge (determinism mode: the platform's Holistic Audit v4, Step 0, Part A and Part B, through `determinism-check/holistic.py`; each deciding figure derived from the pack before it is compared with the blocks, a fork list of twelve or more run in code, the strongest standard rival computed and refuted by a shipped figure or reported, a pin quoted from the prompt or the data for every decision point that could move the call or NO PIN FOUND, the blocks rebuilt from the Step-by-Step alone; it never prices difficulty): DETERMINISTIC. Every finding fixed in the generator in one pass, stage 3 gates re-run; a FIX_NOW whose fixes only edit the answer blocks (a band, a stated convention, a wording) is not re-judged; re-judge once only when a fix moved a graded figure, the prompt or the pack; the reader re-runs only if a document or the prompt changed. SEND_BACK: the fork closed in the prompt or the pack (`/fix-determinism`) |
| 5 | ready | `fingerprint`, `reduce-house-fixes`, `submission-writeup` | the pre-ship check in the design note, the bar re-read against the built pack (the hidden factor record against the cut data, the effort test against `effort.py`); **every gate re-run on the final cut** (`gates.py taskNN`: `precut.py`, `effort.py`, `voice-check.py`, `leak.py`, `guard.py heart` and `surface`, `figures_check.py`); `target.zip` and the golden ZIP (exactly the requested files) from the final rebuild, cut with each file's own save time; **`audit_containers.py taskNN` exit 0 on those zips**, the last command before the commit; card current; `status` `READY`; commit `READY (taskNN): <the call>` with both zips and `golden/` force-added; the author handed the prompt, the pack, the golden ZIP and the four answer blocks |
| 6 | runs | the author, `/triage-runs` (the `run-triage` agent) | both runs' full text (the two rollouts of the submission) and the generated rubric saved under `runs/`, and `status` `RUNS` the moment both responses are saved; each run's losses mapped result by result and classed, the first wrong step named; each decisive step marked made or missed in each run; **the platform's Holistic Audit v4 replayed on the pair beside the triage** (the `determinism-judge` in holistic mode, `runs/holistic_check_v4.md`), its verdict, score and must_fix recorded in `pipeline.json` `holistic` and flagged to the author, nothing fixed on it unless the author says so; **the stump question's answer (How is each model stumped?) written into `submission.md` directly after the Final Recommendation, mandatory, before the scores and whatever the route**, emitted by the generator and checked against the saved runs (`stump_block_check.py taskNN` exit 0, gates.py's `stump` gate); both scores and the average recorded when the platform gives them; the route taken (below) |
| 7 | submit | the author | triage `SUBMIT`; the Reward block filled from `pipeline.json`; the paste in order (Final Recommendation, How is each model stumped? as stage 6 wrote it, Supplementary Questions, Critical Components, Step-by-Step), the `stump` gate green; `status` `SUBMITTED`; commit `SUBMITTED (taskNN): <call>, runs <x> and <y>, average <z>`; later `APPROVED` or `RETURNED` from the review |

Back to design: a reader finding a sentence that hands over a result or a fork on one; a FIX_NOW that moves a
result's path; a reader or triage finding one thing carrying most of the results; a triage `REDESIGN`; a review
return that says the task hinges on one thing, a factor was planted, or the domain is a backdrop.

## Effort per role

| Role | Where | Model and effort | Why |
|---|---|---|---|
| `stump-architect` (the brain: the core, the card, the note, the brief) | stages 0 to 2 of `/build`; `/draw` in the main thread; design judgments in `/fix-rubric` and `/fix-determinism` | Fable 5.2, xhigh (agent definition; `/draw` frontmatter) | the three or four judgments that stump the review's strongest run decide whether a build is approved; everything after them is execution |
| The build (the body: generator around `core.py`, pack, goldens, blocks, pack repairs) | `/build` from stage 3, `/fix-determinism`, `/fix-rubric` | Opus 5.5, high (command frontmatter) | it executes an exact brief; it never moves a frozen dial |
| `determinism-judge` (one thread; the platform's Holistic Audit v4: determinism mode about 60 tool calls, holistic mode about 90) | determinism mode at stage 4 and in `/fix-determinism`; holistic mode in `/triage-runs` and `/holistic-check` | Opus 5.5, high (agent definition) | it replays the platform's own QC, whose forks cost a return each (task1, task7, task9, task13, task20, task24, task25); a thread of its own in a workspace that holds only what the audit gets, never the generator, the note, the figures file or the golden; one or two passes a build before the runs, one per saved pair |
| Leak reader | stage 4, `/leak-check` | Sonnet 5.5, medium (`general-purpose`, on the call) | it reads and answers, it does not reason about method; no leak return on record since it was set |
| `run-triage` | stage 6, `/triage-runs` | Opus 5.5, medium (agent definition) | reading two runs against a rubric |
| `/approve` | author sign-off before upload | medium | mechanical |

**Fable 5.2 is the design's model and no other role's.** Only the `stump-architect` and `/draw` run on it; the
judge, the leak reader and the triage are never spawned on it, by their definition or by a `model` on the `Agent`
call, and a judge resumed for a second pass is resumed on the model its definition names.

A command's `model` and `effort` hold for the turn it runs in; the session's own model answers the next message. An
agent's definition holds wherever it is spawned. So the brain's model is pinned by its agent definition, and a build
is continued with `/build resume taskNN`.

## Speed: where a build's time goes, and the rules that keep it short

The platform's two runs are the only measure of difficulty; nothing in-house solves the task. A build's time goes on
the idea, the generator and the gates, in that order of value, so:

- **Kill weak ideas on paper.** The stump screen (`stumping/references/stump-screen.md`) takes fifteen minutes and
  runs before the card is registered; an idea that fails a test is dropped there, not after a generator, a pack and a
  review. Most of a returned build's cost was spent building an idea a reflex or a filed sentence already gave away.
- **Prove the core before the generator.** `generator/core.py` on the world's arrays (the truth, the golden route,
  each trap's worth, the hurried, direct and most rigorous standard routes against the line, the referee's scores)
  settles the parameters in minutes and is kept: the generator imports it, so the pack and the goldens are written
  once, after the margins hold, and the build cannot drift from them. The same script prices the rubric before any
  ask is written (what a run that loses one stump still earns), so a build that would come back from review at 70
  dies there and not after two platform rounds.
- **One review pass.** The leak reader and the determinism judge run together, once. The judge in determinism mode
  checks determinism only and never prices difficulty; difficulty is the build's (`precut.py`, `effort.py`, the
  skeleton guard) and the platform's, whose holistic QC the judge replays on the platform's own runs once they are
  saved. A fix that only edits the answer blocks is made and shipped without a second judge.
- **No commit while agents or background jobs are still writing, and nothing left unpushed at hand-back.** A status
  change takes its status commit; work between two statuses is committed under the status `pipeline.json` holds and
  pushed before the session reports to the author (`CLAUDE.md`, Git); `PAUSED` only when the session itself ends
  mid-stage.

## Running the stages

- **Two hands.** The architect returns the note at `precut.py` exit 0 with `## Stump core`, `## Build brief` and
  `generator/core.py`; the build thread re-runs `precut.py` and `core.py` itself before it starts, executes the
  brief and repairs the pack where its context is. Anything that touches the core (a broken assertion on the cut
  pack, a member turned forced, a fork whose closure would name a result's work, a finding that the task is not
  difficult enough) goes back to the architect: resumed with `SendMessage` while it is alive, spawned again with the
  note and the finding otherwise. The build never widens a margin, files a method or adds an effect to pass a gate.
  Spawn a fresh build agent only when the session is near its context limit, briefed with `pipeline.json`, the
  design note and the finding.
- **Stage 4 spawns the reader and the judge together** (same pack, neither changes it). While they run, update the
  card and write the pre-ship check. Collect both reports, fix everything in one generator pass, rebuild, and relay
  nothing structural until both are in. Where they disagree on what a shipped sentence licenses, the judge
  recomputed and the reader did not, so the judge settles it. In determinism mode the judge's report never
  reprices the effort test and never sends a build back for difficulty.
- **The free gates come first, always:** nothing with a token cost runs on a pack the scripts have not passed.
- **No author checkpoints before READY.** The draw is shown in ten lines and the build carries on; the author can
  stop or redraw at any point, and `/approve` remains for a manual sign-off before upload.

## Stage 6: reading the runs

The platform generates two runs from the prompt and `target.zip` (two rollouts of one submission; it can take more
than twenty minutes), generates the rubric from the prompt and the answer blocks, and grades both. The bar is the
average of the two under 60, with the losses analytical. Rollouts are cheap and the client has loosened its limit on
them (the announcement of 2026-11-21: "you should still NOT be spamming"), so a pair is re-run on an unchanged
submission only for a reason written into `pipeline.json` `runs.history` (a rollout that failed, stopped before the
analysis or was cut short), never to draw a lower average; after any change to the prompt, the pack or the blocks
the new pair is the measurement and the old one is history. `/triage-runs` saves the runs and the rubric under
`runs/`, records the scores, and spawns `run-triage`, which maps where each run lost its points result by result and
names the **first** place each run went wrong, classed on the client's table (`guidelines/client/deep-reasoning.md`, "Reading the runs").
Beside it, the `determinism-judge` replays the platform's Holistic Audit v4 on the same saved pair (holistic mode;
`/holistic-check` runs it alone). That audit is the QC the platform runs once the two responses are back, and its
fail blocks a submission: it builds its own rubric from its reproduction (recommend at least 30 per cent, ideally
about half), grades both runs on it against 0.65 (borderline from 0.60), runs the convention check wherever both
runs reached the same alternative, and passes depth only at level 4 or 5 with a run failing at a decisive step on a
valid label. Its verdict is recorded and flagged, and never changes the route below on its own: fixes wait for the
platform's audit or the author's word. The routes:

| Triage verdict | When | Route |
|---|---|---|
| `SUBMIT` | average under 60, the counterfactual average (surface and formatting losses given back) under 60, the higher-scoring run itself under 60 (the review's gate rests on its single strongest run), no run's first wrong step a surface class, and **the two runs between them missed two or more decisive steps** for analytical reasons (the client's "only one decisive step" is read off the runs: a step both runs made is a reflex by their own evidence) | fill the Reward block, submit, `SUBMITTED` |
| `FIX_DETERMINISM` | a run took a sound method the prompt allows to another answer | `/fix-determinism`; then new runs |
| `SURFACE_RISK` | a run's first wrong step is a missed planted detail, a misread field or clause, a misapplied written procedure, or a formatting slip | the trigger is made texture in the generator (unmissable, or off every graded path); the deep step is untouched; then new runs |
| `FIX_ASKS` | the losses were analytical, and the average or the higher-scoring run is 60 or more because the triage's earned map shows points on figures no stump touches or on figures a lost stump moved inside their bands | `/fix-rubric` (those figures leave the prompt and the blocks, or are replaced by consequences of the lost stumps); then new runs |
| `REDESIGN` | the average 60 or more with the losses on one or two results, or the only losses were surface, or both runs made every decisive step but the same one whatever the average (one decisive step left: the landed steps go to `precedents.json` as reflexes and the architect redraws them) | `## Tried and rejected` line, `status` `DESIGN`, `/build taskNN from 2` |
| `RUBRIC_EDIT` | a generated criterion is clearly wrong or missing and fixing it moves the verdict | the author edits that criterion on the platform and re-runs the evaluation |

**Reading the loss map** (back to stage 2 with this session as designer). Read where each run lost its points, result
by result, against the design note's results chain and effort test:
- losses spread across several results, the two runs losing in different places: the design held; submit;
- each decisive step, made or missed in each run (the triage's table): two or more missed between the runs is the
  client's "two or more decisive, independent steps" shown on the runs, and the stump answer has an entry for
  each; one missed by both and the rest made is one decisive step, whatever the average; a step is read on its own
  figure on the run's own inputs (the run's route rebuilt in `core.py` to its filed figures, the run's other lost
  steps then completed on it), never on a band, because two lost steps offset into a right band (task1 arch 7,
  where both responses lost two steps each and the review read one);
- both runs earned a result the note priced as lost: its difficulty was a reflex the careful column should have
  scored Right; rebuild that result around a move beyond it, or replace it with a result from another area;
- most of both runs' lost weight on one result: thinner; add results that need their own work rather than hardening
  that one;
- a result lost to a missed plant, a built-in factor, a misread field or a written procedure: a surface stump on
  that result; rebuild it on real analysis or make its trigger texture off every graded path.

Every run triaged adds a row to `stumping/references/sulfur-record.md`: the Sulfur run record is the evidence the
next draw reads first, beside Mark's measured record.

## Commits

Every status change takes its commit: `DRAWN`, `READY`, `SUBMITTED`, `APPROVED`, `RETURNED`, `RESHIPPED`, `PAUSED`,
`RETIRED` (`CLAUDE.md`, Git). Whatever a session did between two statuses is committed as well, under the status
`pipeline.json` holds with what moved (`RUNS (taskNN): <what moved>`), and pushed before the session hands back: the
author reads the work on GitHub, so nothing is left only in the working tree. Each commit stages its paths by name
(never another session's uncommitted files): the task folder,
`.claude/skills/fingerprint/cards/taskNN.json`, the run record row, and from READY on `git add -f taskNN/target.zip
taskNN/golden/ taskNN/golden.zip`. Then `git pull --rebase origin main` and push. A session that stops mid-stage
writes `pipeline.json` with a `resume` line and commits `PAUSED`. A blocker is
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

**Before any determinism repair, the fork-is-the-result test** (`/fix-determinism` step 3; `stumping` Part 5): if
the sentence that would close the fork names what a result's work recognises, the fork is that result's difficulty,
and the result is redesigned at stage 2, never pinned. In Mark, pins that fixed population, window, unit or schedule
and named no method turned returns into approvals (169, 135, 151, 162); pins naming the clock, window or test the
difficulty rode on landed the call on the next round (141, 179 v3, 181 v2, 118 v2). No approved build was ever
repaired by hardening the asks alone, and a rung stacked above a solved step never held.

**The bar on every rework, before any resume.** The card carries `stump_class: analytical`, `answer_shape`, `weight`
and `chain_signature`, with no official or validated decoy flag; the note passes `precut.py` on the results-chain
contract. A design whose answer turns on one thing (a plant, a field reading, an executed procedure, a replay, a single
fact, a shallow hidden factor or an open reading) is re-rooted at stage 1, never resumed. **A build cut under the
retired single-deep-step design is re-rooted to a results chain before any re-ship**, whatever its runs scored.

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
  keys carrying them, the card's stump and driver, the design note's results chain and hidden factor record (the
  ladder and default path on retired builds), and
  the prompt's call sentence; in determinism mode also every Supplementary Questions number.
- `status.py` prints every Sulfur build with its status and runs; `status.py next` the build to work next (returned,
  paused and in-runs builds first); `status.py new` the next free number (task1 up); `status.py taskNN` one build.

## `pipeline.json`

The one state file in a task folder: where the build is, never why.

```json
{"task": "task1", "status": "BUILD",
 "domain": "<vocab domain key>", "subdomain": "<the assigned Sulfur subdomain>", "objective": "forecasting",
 "stage": 3, "stage_name": "build", "updated": "2026-11-07",
 "doctrine": "throughout",
 "call": "the committed recommendation in one line",
 "chain": "the results in one line: R1 ..., R2 ..., each a checkable result",
 "architecture": 1, "loops": 0,
 "precut": {"exit": 0, "date": ""},
 "leak": {"leak_py": "", "reader": ""},
 "duplicate_check": {"heart": "", "nearest": ""},
 "judge": {"verdict": "", "disposition": "", "report": ""},
 "holistic": [{"date": "", "mode": "holistic", "report": "runs/holistic_check_v4.md", "verdict": "", "score": null,
               "rubric": {"run1": null, "run2": null, "mean": null, "stumped": ""}, "correctness": "",
               "determinism": "", "depth_level": null, "must_fix": [], "md5": {}}],
 "paper_pair": null, "effort": {"quick": null, "careful": null, "thorough": null, "largest_hint": ""},
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

An architecture is **spent** when a determinism fork can only be closed by naming what a result's work recognises
(the fork-is-the-result test), two triage rounds return `REDESIGN`, or `precut.py` fails twice on the results chain
or the effort test (re-root before any data is cut). A hardening deepens
Layer 2 and never plants; if only a plant would hold, the architecture is spent.

**Re-root:** a new draw at stage 1 in the same client domain and number (the card's `subdomain` is a house task type under that domain, not its boundary: a re-root may take any of the domain's task types, organisations, instruments and data, adding files or withholding them), `architecture` incremented, `loops` reset, the
old card's lineage saying spent and why, one line in `## Tried and rejected`, committed `DRAWN`. **One architecture
per world:** once a world's chain is spent the next draw moves to another world, another dataset and another
shell (Mark: 251, 249 and 269 each spent two architectures in one world where one would have; 118, 305 and 273 kept
one prompt shell across every re-root and `guard.py check` now blocks it). **A landed scaffold is never
re-pointed:** a re-root, or a level-up a reviewer asks for in the same world, changes the deciding lessons and the
decision form, never one more correction in the same chain. task4 ran ten architectures and task10 seven, most adding
one correction to the same order or commit chain, and both runs landed every one that ran; the client's templating
page sends that pattern back at severity 2. The new card's `skeleton` is screened against the slot's own lineage
(`fingerprint` Part 1b), and a severity 1 or 2 match there BLOCKs. **No same-day serial re-roots without new
evidence**: a re-root needs the runs, the judge or the leak reader to have killed the version it replaces. A build is
**retired** only on the author's word: a `## Retired` section in the design note, `status` `RETIRED`, every card kept,
committed `RETIRED`. A session never proposes retirement because a design space ran dry: it widens the draw (another
task type in the client domain, another organisation and decision, other instruments, files added or withheld,
public data) and keeps drawing, and no screen brief carries a stop short of a passing core (task3 was recommended
for retirement after ten architectures inside one house task type, and the author ruled it out).

## Throughput

The platform's tier sets how many tasks may be open at once (Tier 1 one, Tier 2 three, Tier 3 six, Tier 4 no
limit). While a build waits on its runs (stage 6), the next build may be drawn if the tier allows it. The moment a
build is submitted, the next draw starts on the author's word.
