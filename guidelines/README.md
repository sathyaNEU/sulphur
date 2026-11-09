# Project Sulfur guidelines

The client's spec, as exported from the Sulfur handbook on 2026-11-07, sits under `client/` unchanged. The working
standard is the skills under `../.claude/skills/`, which apply this spec with Project Mark's measured record on top.
Where the client text is newer than a skill, the client text wins and the skill is brought up to it
(`../CLAUDE.md`, Standing rules).

## Files

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
  hurried failures and pins, and each group's shallow versions with the client's verdicts.
- `client/examples/`: the rebuilt example library (15 tasks that stumped the models for reasoning reasons) and its
  index.
- `client/quality-checks/quality.txt`: the reviewer-side quality checklist.
- `determinism_judge_system_prompt.md`: the determinism judge's system prompt with Gate H set to the bar of
  2026-11-09 (H1 domain, H2 layers, H3 not one thing with the shallow hidden factor test, H4 difficulty throughout
  with the effort test, H5 the one-fact test counted in results, and determinism per result with bands), handed
  verbatim to the `determinism-judge` agent.

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
