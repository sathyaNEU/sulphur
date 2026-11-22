# AGENTS.md: Antigravity Workspace Manual (Sulfur)

This repository holds the Sulfur task builds (`task1` up), the client's bar (`guidelines/client/`), and Antigravity's standalone skills and subagent definitions under `.agents/`. **Use `.agents/` exclusively in Antigravity sessions** (`.claude/` and `CLAUDE.md` belong to Claude Code and stay untouched).

> **STOP: NO IN-HOUSE SOLVER RUNS.** Never run a solver, scored reader, call-only probe, or "cold" agent that solves the prompt and returns figures. Difficulty is proven arithmetically in `generator/core.py` (`corelib.py`), argued in `DESIGN_NOTE.md` (`precut.py`), verified across generator passes (`effort.py`), and measured exclusively by the platform's two rollouts (`/triage-runs`). `leak-reader` reads for leaks only (never solves); `determinism-judge` verifies Gates A to E from `submission.md` (never derives its own answer or prices difficulty).

## The Client's Bar Comes First

Read `guidelines/client/guidelines-2026-11-20.md`, `guidelines/client/project-lead-review-2026-11-09.md`, `guidelines/client/learning-modules/overused-strategies-2026-11-21.md` (45 closed strategies), and `guidelines/client/examples/1.txt`, `16.txt`, `17.txt` before every draw.

- **Two or more decisive, independent steps** (three targeted for level 5): missing one must not sink the others, and no single sentence of help may rescue more than a third of the results.
- **No one-thing tasks, no planted defects, no closed strategies deciding the call:** rule application, data semantics, planted defects/decoys, shallow hidden factors, replays, single-fact surface stumps, unpinned ambiguities, and "only one decisive step" are banned. None of the 45 closed strategies may flip a new build's call.
- **Platform pass bar:** two-run average under 60% (exactly 60 fails), **higher-scoring run itself under 60%**, counterfactual average under 60%, all primary losses analytical (deep classes), and two or more decisive steps missed between the two runs. Build to **50 or under on paper** (`effort.py` and `corelib.py`: any single stump lost <= 50, reflex <= 30, rigorous <= 50, all 4 `run_routes` <= 50, two-sided `sides.over` and `sides.under`).
- **Natural practitioner prompts on the first pass:** draft straight to **NATURAL (0 of 9 signals)** and **FEW/NO SIGNS** on the AI-writing scan (55 to 120 words, one plain paragraph, insider domain vocabulary, zero `"how X drives Y"` methodology chains, zero data-gap/metering-gap explanations, zero parallel three-factor triplets, zero `"in the ZIP"` filler, zero rounding rules, zero attached file names). Pin exact formulas and filing column lists inside the organisation's governing document in `target/`.

## Skill Routing (`.agents/skills/`)

Read `.agents/skills/<name>/SKILL.md` before doing the work it governs; when two apply, follow both in pipeline order.

| Work | Workspace Skill |
|---|---|
| Starting/re-rooting a build, duplicate/skeleton/name checks | `.agents/skills/fingerprint/SKILL.md` |
| Domain fit, answer shape, natural `prompt.txt`, `voice-check.py` | `.agents/skills/guide-to-prompt/SKILL.md` |
| Results chain, stump screen, `corelib.py`, `precut.py`, `effort.py` | `.agents/skills/stumping/SKILL.md` |
| Asks, rubric arithmetic, critical component independence | `.agents/skills/supplemental-stumping/SKILL.md` |
| Bands, rivals, forks, forcing, Gates A to E, `figures_check.py` | `.agents/skills/determinism-check/SKILL.md` |
| Building/repairing the pack under `target/` and `metadata.json` | `.agents/skills/dataset-generation/SKILL.md` |
| Writing/updating `submission.md` and golden deliverables | `.agents/skills/submission-writeup/SKILL.md` |
| Making golden deliverables look like authentic work products | `.agents/skills/golden-realism/SKILL.md` |
| Container hygiene (`officepdf.py`, `postprocess.py`, `audit_containers.py`) | `.agents/skills/reduce-house-fixes/SKILL.md` |
| Mechanical leak sweeps (`leak.py`) and isolated `leak-reader` | `.agents/skills/leak-check/SKILL.md` |
| Stage machine, `gates.py`, `status.py`, `freeze.py`, `pipeline.json` | `.agents/skills/build-pipeline/SKILL.md` |

## Workflow Skills (Slash Commands)

Each workflow lives as a first-class Antigravity skill under `.agents/skills/<name>/SKILL.md`:

| Command | Skill Path | Purpose |
|---|---|---|
| `/draw` | `.agents/skills/draw/SKILL.md` | Stages 0 to 2 in main thread: `generator/core.py`, card, `DESIGN_NOTE.md`, `prompt.txt`, commit `DRAWN` |
| `/build` | `.agents/skills/build/SKILL.md` | End-to-end build: `stump-architect` (stages 0-2) -> pack/goldens/gates (stage 3) -> parallel `leak-reader` + `determinism-judge` (stage 4) -> `READY` (stage 5) |
| `/leak-check` | `.agents/skills/leak-check/SKILL.md` | Run `leak.py` mechanical sweeps + one isolated `leak-reader` subagent |
| `/approve` | `.agents/skills/approve/SKILL.md` | Pre-upload mechanical sign-off (`guard.py heart/surface`, `precut.py`, `leak.py`, `audit_containers.py`) |
| `/triage-runs` | `.agents/skills/triage-runs/SKILL.md` | Save platform runs + rubric, invoke `run-triage`, draft `How is each model stumped?`, route next action |
| `/fix-determinism` | `.agents/skills/fix-determinism/SKILL.md` | Close an open fork without weakening stumps, verify via `freeze.py --mode determinism`, re-judge once |
| `/fix-rubric` | `.agents/skills/fix-rubric/SKILL.md` | Rebuild earned reflex asks while freezing holding results, verify via `freeze.py --mode rubric` |

## Antigravity Subagents (`.agents/agents/`)

Register subagents from `.agents/agents/<name>.md` via `define_subagent` and launch via `invoke_subagent` using **`Model: inherit`** and **`Workspace: inherit`** (unless the user explicitly requests a different tier). Communicate with live subagents using `send_message`.

| Subagent | File | `enable_write_tools` | Scope & Isolation |
|---|---|---|---|
| `stump-architect` | `.agents/agents/stump-architect.md` | `true` | Stages 0-2 design & core repairs; writes only `DESIGN_NOTE.md`, `generator/core.py`, `prompt.txt`, `pipeline.json`, and card |
| `determinism-judge` | `.agents/agents/determinism-judge.md` | `true` | Stage 4 & `/fix-determinism`; Gates A-E only; NEVER reads `DESIGN_NOTE.md`, `generator/`, `figures.json`, `effort.json`, `pipeline.json`, `metadata.json`, or `golden/` |
| `leak-reader` | `.agents/agents/leak-reader.md` | `false` | Stage 4 & `/leak-check`; reads ONLY `/tmp/leak-<task>/` scratch copy of `prompt.txt` and `target/`; never solves |
| `run-triage` | `.agents/agents/run-triage.md` | `true` | Stage 6 `/triage-runs`; reads `runs/` + `submission.md` + note sections; writes `runs/triage.md` |

## One-Command Gate Runner

```bash
python3 .agents/skills/build-pipeline/gates.py taskNN --full
```

Runs `precut`, `effort`, `voice`, `leak`, `figures`, `containers`, `heart`, `surface`, `checks`, `verify`, and two byte-identical rebuilds in parallel using `.agents/skills/` exclusively.

## Standing Rules & Git

1. **One branch (`main`), always pushed:** Stage paths explicitly by name (never `git add -A`), force-add `taskNN/target.zip`, `taskNN/golden/`, and `taskNN/golden.zip` from `READY` onward, run `git pull --rebase origin main`, and push before handing back. Never force-push. Status commits: `DRAWN (taskNN)`, `READY (taskNN): <call>`, `RESHIPPED (taskNN): <what>`, `SUBMITTED (taskNN): ...`, `APPROVED (taskNN)`, `RETURNED (taskNN): ...`, `SKILLS: <change>`.
2. **Never touch `.claude/` or `CLAUDE.md`:** keep Claude Code's configuration strictly as-is.
3. **Zero em/en dashes** in `prompt.txt`, `submission.md`, `DESIGN_NOTE.md`, or reports.
4. **No dollar sign before a digit in any skill body** (write `USD 38M`).
5. **Containers scrubbed by construction:** every shipped PDF via `.agents/skills/reduce-house-fixes/scripts/writers/officepdf.py`, every Office deliverable through `postprocess.py`, distinct timestamps, verified with `audit_containers.py taskNN` exit 0 before every ship.
6. **Exact figures everywhere:** every figure in `submission.md`, CSV, and XLSX derives from `figures.json` and recomputes from `target.zip` (checked by `figures_check.py`, `verify.py`, and LibreOffice Calc formula evaluation).
