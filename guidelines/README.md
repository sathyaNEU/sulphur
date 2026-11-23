# Project Sulfur guidelines

The client's spec, as exported from the Sulfur handbook on 2026-11-07, sits under `client/` unchanged. The working
standard is the skills under `../.claude/skills/`, which apply this spec with Project Mark's measured record on top.
Where the client text is newer than a skill, the client text wins and the skill is brought up to it
(`../CLAUDE.md`, Standing rules).

## Files

- `client/guidelines-2026-11-20.md` (the guidelines page of 11/20, read 2026-11-21, the page a task is reviewed
  against): the bar (two rollouts, average under 60), the basics, what a stump must not be (with "only one decisive
  step" as a named send-back), what it should be (two or more decisive, independent steps; the one-fact, clean-data
  and effort tests), the critical components as the decisive steps' answers (the answer and never the method, each
  in a requested deliverable, independent), what else to keep in mind (no unstated conventions, the prompt must not
  point the other way, every decisive step reachable) and how to fill in `Valid Stump?`.
- `client/phase-2-announcement-2026-11-21.md`: the channel announcement that reopened the project: two rollouts,
  re-runs loosened without spamming, at least two independent and challenging steps, tasks already submitted
  reviewed against the same rules, and the examples not to be copied.
- `client/latest_update.txt`: what changed in the current version. The bar (two runs, average under 60, losing for an
  analytical reason), the generated rubric, the banned stumps, deep reasoning and the rebuilt example library.
- `client/overview.txt`: the welcome, program details, approval criteria, key requirements, the 18 answer shapes,
  the difficulty bar, how the rubric is built, banned stumps beside a deep version of each, and the 15 blocks of
  the task walkthrough.
- `client/deep-reasoning.md` (exported 2026-11-09, the current bar): difficulty throughout the analysis, the
  fourteen areas where analysis gets hard, a worked six-result illustration, the effort test and its three passes,
  where the weight can sit, the nine analysis types, the fourteen answer shapes, templating, the tools and where a
  hurried analyst stops, the shallow hidden factor and its three conditions with seven designs to judge, how runs
  lose points and which losses count, the banned list, surface against deep pairs, and the build checklist.
- `client/project-lead-review-2026-11-09.md`: the project lead's review of about 500 tasks, verbatim: the four prompt
  faults and the three-strike policy, "most tasks hinge on one thing", the shapes the client loves, task types now
  assigned.
- `client/domains.txt`: the seven major domains and their 21 subdomains, each with example task types, what makes
  it deep and what domain fit means there.
- `client/prompt.txt`: the export of the Prompt page duplicated the Deep reasoning page; it carries the author's
  standing note at its end (the author rewrites every prompt for voice; the harness makes it correct and leak-free).
- `client/learning-modules/`: prompt writing, prompt reminders, input files, data messiness, two-layer task design,
  golden output, glossary, and `stumping-strategies.md` (exported 2026-11-09): 77 investigation strategies across
  seven domain groups, each with its analysis type, answer shape, weight, chain of results, public data, scenario,
  hurried failures and pins, and each group's shallow versions with the client's verdicts;
  `overused-strategies-2026-11-21.md`: the closed strategies, 45 cards in six families as read on 2026-11-21 (34 on
  the first read of 2026-11-12), each with its trap, the fix already used and its accepted examples.
- `client/depth-scale-2026-11-09.md` with `depth-scale-2026-11-09-detail.md`: the client's reading of 17 submitted
  tasks on five depth levels, and each level 4 and 5 task in full.
- `client/approved-reviews-2026-11-14.md`: three review sheets of other fellows' approved tasks (the review reads
  its strongest run and audits forks blind).
- `client/examples/`: the rebuilt example library (17 tasks that stumped the models for reasoning reasons) and its
  index. `1.txt`, `16.txt` and `17.txt` are the three the author shared as the library's hardest on 2026-11-21 (runs
  averaging 0.26, 0.285 and 0.31): the difficulty to match, never a template.
- `client/quality-checks/quality.txt`: the reviewer-side quality checklist.
- `client/quality-checks/holistic-audit-v4-2026-11-22.md`: the platform's Holistic Audit v4, verbatim (pasted by the
  author on 2026-11-22): the QC the platform runs once a task's two responses are back, and that a fellow may run
  with any checking agent. It reproduces the four answer fields from the pack, runs the rivals in code (a rival that
  reproduces a run's figures with no quoted pin, or a more rigorous standard method that moves the call, is
  not_pinned), builds its own rubric and grades both runs on it against 0.65 (borderline from 0.60), and reads depth
  (level 4 or 5, a run failing at a decisive step on a valid label). The `determinism-judge` replays it:
  determinism mode (its Step 0, Part A and Part B) before the platform's runs, holistic mode (the whole audit) once
  both responses are saved; `../.claude/skills/determinism-check/holistic.py` fills its placeholders.
- `determinism_judge_system_prompt.md`: an earlier platform judge's system prompt with Gate H set to the bar of
  2026-11-09 (H1 domain, H2 layers, H3 not one thing with the shallow hidden factor test, H4 difficulty throughout
  with the effort test, H5 the one-fact test counted in results, and determinism per result with bands). Its Gates A
  to E are the `determinism-judge`'s house supplement in determinism mode; the Holistic Audit v4 decides where they
  differ.

## Where the working standard lives

- `../.claude/skills/stumping/` for the deep step, with Mark's measured record in `references/evidence.md`, the
  strategy families and their deaths in `references/strategies.md`, the Sulfur per-domain strategies annotated with
  Mark's flags in `references/sulfur-strategies.md`, and the Sulfur run record in `references/sulfur-record.md`
- `../.claude/skills/guide-to-prompt/` for the domain fit, the answer's shape and `prompt.txt`
- `../.claude/skills/supplemental-stumping/` for the asks and the rubric arithmetic
- `../.claude/skills/dataset-generation/` for the input pack
- `../.claude/skills/determinism-check/` for the gates and the judge
- `../.claude/skills/submission-writeup/` and `golden-realism/` for the answer blocks and the goldens
- `../.claude/skills/leak-check/` and `fingerprint/` for the ship gates
- `../.claude/skills/build-pipeline/` for the stage machine, the board and the run triage
