---
description: After the platform has generated the two runs, save both responses, set the build to RUNS, map where each run lost its points result by result and class every loss on the client's failure table, replay the platform's Holistic Audit v4 on the pair beside the triage (the determinism-judge in holistic mode; recorded and flagged, nothing fixed on it), mark each decisive step made or missed, write the answer to the form's stump question (How is each model stumped?) into submission.md directly after the Final Recommendation (mandatory, before the scores and whatever the route), record both scores and the average, and route the build (submit, fix determinism, fix the asks, rebuild a surface trigger as analysis, or redesign).
argument-hint: taskNN [the two scores, or nothing if runs/rubric.md carries them]
effort: medium
---

# /triage-runs

The build named in `$ARGUMENTS` is on the platform (`status` `READY` or `RUNS`) and its two runs are back.
Invoke `build-pipeline` (Stage 6) first.

1. **Collect the evidence into the task folder.** The author pastes each run's full response and the generated
   rubric (criteria, weights, and each run's pass or fail where the platform shows it). Save them verbatim as
   `taskNN/runs/run1.md`, `taskNN/runs/run2.md` and `taskNN/runs/rubric.md`; a pair already on file from an
   earlier cut is first archived under another name (`archN_pairK_response_1.md`) and moved to `runs.history`.
   Where the platform offers the files each run produced, save them under `runs/run1_files/` and
   `runs/run2_files/`: the holistic audit (step 3) grades a figure from them when a response points to a file, and
   grades from the response alone, saying so, when they are absent. If a response is missing, ask once for it and
   stop. If only the scores or the rubric are missing, ask for them
   once and carry on: the loss map and the stump answer are written from the responses alone, and the scores are
   recorded when they come. Never paraphrase a run.
2. **Record the pair, then the scores,** in `pipeline.json` `runs` (`files`, `recorded` with the ISO date, then
   `run1`, `run2` and `average` when the platform gives them) and set `status` `RUNS` the moment both responses
   are saved, scores or no scores (the `stump` gate binds from `RUNS`). The two runs are the two rollouts of the
   submission; the bar is their average under 60, and exactly 60 fails. A pair re-run on an unchanged submission is
   recorded in `runs.history` with its reason (a rollout that failed or stopped before the analysis), never run to
   draw a lower average.
3. **Spawn two agents in one message, in the background** (each definition sets its model and effort), each with
   the absolute task folder: one `run-triage` agent, which writes `runs/triage.md`, and one `determinism-judge` in
   holistic mode, which replays the platform's Holistic Audit v4 on the saved pair
   (`guidelines/client/quality-checks/holistic-audit-v4-2026-11-22.md`: correctness, determinism with the
   convention check, its own rubric grading both runs, depth) and writes `runs/holistic_check_v4.md`. This command
   licenses both. Check the audit's inputs first (`python3 .claude/skills/determinism-check/holistic.py taskNN
   --check` exits 0) so a missing block or pair stops before the pass is spent. The two
   threads read the same saved runs, neither waits on the other, and neither changes anything.
4. **Check its loss map against the design note yourself.** A run that lost the results the `## Effort test`
   priced as lost, in the classes the `## Results chain` names, is the design working; a run that earned a result
   priced as lost found a reflex the careful column missed (record it as evidence); a run that lost somewhere the
   chain does not predict is either a deep loss the design did not model or a surface trigger (fix it). Read its
   `## Decisive steps` table against the critical components: the runs between them missed two or more decisive
   steps, or the build is one decisive step by the runs' own evidence and is not submitted. Where you disagree
   with the agent, say so in one line each and keep both readings in the report.
4a. **Read the holistic audit beside the triage.** Append its verdict, score, rubric scores, determinism, depth
   level and must_fix list to `pipeline.json` `holistic` (`/holistic-check` step 4 gives the entry). Where the
   audit and the triage disagree (a first break classed on a valid label by one and a surface label by the other, a
   decisive step made in one reading and missed in the other, a fork one calls defensible), say so in one line
   each. The audit uses the platform's labels, so where the stump answer names a run's first break, it uses the
   label the audit gave (`run-triage`, the v4 vocabulary). A failed in-house audit does not change the route below
   and fixes nothing: it is named on top of the hand-over with its must_fix list and `Routes:` line, and the author
   decides before the paste goes in (fixes wait for the platform's audit or the author's word).
5. **Write the stump answer into `submission.md` now. It is mandatory, before the scores and whatever the
   route.** The form's question "How is each model stumped?" goes in as `## How is each model stumped?`, the very
   next block after `## Final Recommendation` and before `## Supplementary Questions`, from the triage's draft:
   where and how each response goes wrong, why the stump is fair, why it takes rigour (`submission-writeup`). It is
   emitted by the generator where the blocks are, every figure and quote in it asserted against the saved runs and
   `figures.json`, then rebuilt with the blocks-only pass (the pack and the goldens stay byte-identical).
   `python3 .claude/skills/submission-writeup/stump_block_check.py taskNN` (gates.py's `stump` gate) exits 0
   before anything is handed over. The paste handed to the author always carries the block in that place, whatever
   the verdict below. A step both runs made is never listed as missed; where the runs between them missed only one
   decisive step, or lost on a surface class, the block still says what the runs show, and the verdict says so.
6. **Route** on the verdict:
   - `SUBMIT`: hand the author the paste in order (Final Recommendation, the stump answer, Supplementary Questions,
     Critical Components, Step-by-Step) with the Reward block filled from `pipeline.json`; set `status` `SUBMITTED`
     once the author confirms submission, commit `SUBMITTED (taskNN): <call>, runs <x> and <y>, average <z>`.
   - `FIX_DETERMINISM`: `/fix-determinism taskNN <the run's method and why it is defensible>`.
   - `SURFACE_RISK`: the named trigger is rebuilt as analysis or becomes texture in the generator (unmissable, or no
     longer on any graded path), the free gates re-run, the pack is re-cut and the author regenerates the runs; the
     other results are not touched.
   - `FIX_ASKS`: `/fix-rubric taskNN` with the triage file.
   - `REDESIGN`: one line in `## Tried and rejected` (what both runs did), `status` `DESIGN`, `/build taskNN from 2`.
   - `RUBRIC_EDIT`: give the author the criterion and its corrected text; they edit it on the platform and re-run
     the evaluation, then this command runs again with the new scores.
7. **Record the lesson.** Append the spread, the classes, the scores and the route to `pipeline.json`
   `runs.history`, and one row to `stumping/references/sulfur-record.md` (the Sulfur run record: task, domain,
   analysis type, the weight and chain signature, both first-wrong-step classes, the spread, both scores, verdict).
   This record is what the next draw reads first.

Report: both scores and the average (or that they are owed), the counterfactual average, the loss map (which
results each run lost and why), each run's first wrong step quoted with its class, each decisive step made or
missed in each run, the in-house holistic audit's five-line summary with its score and must_fix list (and where it
disagrees with the triage), the stump answer as it now stands in `submission.md` with the `stump` gate's verdict,
the verdict and the route. No solver runs here: the platform's two runs are the only evidence, and the holistic
audit replays the platform's own check on them.
