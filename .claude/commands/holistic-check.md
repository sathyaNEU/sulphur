---
description: Replay the platform's Holistic Audit v4 in-house on one build whose two platform responses are saved, through the determinism-judge in holistic mode (the whole audit of guidelines/client/quality-checks/holistic-audit-v4-2026-11-22.md: correctness, determinism with the convention check, its own rubric grading both runs, and depth). Records the predicted verdict, score and must_fix list in pipeline.json and flags them to the author; fixes nothing. With "determinism" it runs the judge's pre-platform mode instead (the audit's Step 0, Part A and Part B) on a build with no runs yet.
argument-hint: taskNN [determinism]
effort: medium
---

# /holistic-check

The platform runs its Holistic Audit v4 on a task once the two model responses are back, and a fail blocks the
submission. This command runs the same audit here first, on the same inputs: the prompt, the pack, the four answer
fields and both responses with the files each run produced. The audit is the client's text, and the
`determinism-judge` follows it word for word in holistic mode. This command licenses that one pass.

1. **The inputs.** The build named in `$ARGUMENTS` has `prompt.txt`, `target.zip` and the four answer blocks in
   `submission.md`. Holistic mode also needs both saved responses: `runs/run1.md` and `runs/run2.md`, or the pair
   `pipeline.json` `runs.files` names (`response1.md` and `response2.md` are found too). Where the author has the
   files each run produced, they go under `runs/run1_files/` and `runs/run2_files/` (named after the response
   file: `runs/response1_files/` beside `response1.md`). Without them the audit grades each run from its response
   alone and says so. If a response is missing, ask once for it and stop. With `determinism` in the arguments, no
   runs are needed: this is the pre-platform pass.
2. **Check the inputs before spending the pass.** `python3 .claude/skills/determinism-check/holistic.py taskNN
   --check` (add `--mode determinism` for the pre-platform pass). A non-zero exit stops here with its line: a missing
   answer block would fail the audit's Step 0, and a missing pair means the runs are not saved yet. The judge builds
   its own workspace.
3. **Spawn one `determinism-judge`** (its definition sets Opus 5.5 at high) with the absolute task folder and the
   mode, `holistic` or `determinism`. Nothing else is in the brief: the judge reads only what `holistic.py` hands
   it.
4. **Record it.** When the judge returns, read its report: `runs/holistic_check_v4.md` (holistic mode) or
   `determinism_check_report.md` (determinism mode), each `_pass<n>` beside an earlier one. Append to
   `pipeline.json` `holistic` (a list) one entry: `date`, `mode`, `report`, `verdict`, `score`, `rubric` (`run1`,
   `run2`, `mean`, `stumped`), `correctness`, `determinism`, `depth_level`, `must_fix` (one line each) and the md5s
   of `prompt.txt`, `target.zip` and `submission.md` from the report's opening line. Where `runs/triage.md` exists,
   read its verdict beside the audit's and say in one line each where the two disagree (a failure class read
   differently, a decisive step marked made by one and missed by the other).
5. **Nothing is fixed on it.** An in-house verdict records and flags: fixes wait for the platform's audit or the
   author's word, and the four graded blocks stay byte-identical. A failed audit is told to the author on top of
   the hand-over, with its must_fix list and the `Routes:` line, so they decide before the paste goes in.
6. **Commit and push** under the status `pipeline.json` holds, with the report and `pipeline.json` staged by name:
   `RUNS (taskNN): in-house Holistic Audit v4 <passed | failed>, score <n>` (or the build's own status word), then
   `git pull --rebase origin main` and `git push origin main` (`CLAUDE.md`, Git).

**Report:** the five-line summary as the audit writes it (correctness, determinism, the rubric scores and the
stumped gate, depth, the verdict), the score, the must_fix list, the feedback paragraph, the `Routes:` line and
where the audit and the triage disagree. No solver runs here: the audit replays the platform's own check on the
platform's own two runs.
