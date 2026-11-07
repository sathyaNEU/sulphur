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
- `client/deep-reasoning.txt`: the standard in one line, the seven judgments that decide deep tasks, the one-fact
  test, the table of how runs fail (which failures count as evidence), the banned list with its quick tests, and
  the seven-item build checklist.
- `client/domains.txt`: the seven major domains and their 21 subdomains, each with example task types, what makes
  it deep and what domain fit means there.
- `client/prompt.txt`: the export of the Prompt page duplicated the Deep reasoning page; it carries the author's
  standing note at its end (the author rewrites every prompt for voice; the harness makes it correct and leak-free).
- `client/learning-modules/`: prompt writing, prompt reminders, input files, data messiness, two-layer task design,
  golden output, glossary, and the per-domain stumping strategies.
- `client/examples/`: the rebuilt example library (15 tasks that stumped the models for reasoning reasons) and its
  index.
- `client/quality-checks/quality.txt`: the reviewer-side quality checklist.
- `determinism_judge_system_prompt.md`: the determinism judge's system prompt with Gate H set to the Sulfur standard
  (H1 domain, H2 layers, H3 the decisive step's class, H4 the deep chain, H5 the one-fact test), handed verbatim to
  the `determinism-judge` agent.

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
