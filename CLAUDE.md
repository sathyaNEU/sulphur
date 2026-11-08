# Project Sulfur task builds

Every `taskNN/` folder is one deterministic analytical task for Project Sulfur: `prompt.txt`, the input pack under
`target/` (shipped as `target.zip`), the golden deliverables under `golden/` (shipped as one golden ZIP), the answer
blocks in `submission.md`, and after the platform runs, `runs/`. The goal is one thing: tasks that clear the Sulfur
bar on the first submission because the two runs lose on a deep-reasoning judgment. Everything below serves that.

This harness is Project Mark's, refreshed for Sulfur. Mark's measured record (what landed on the portal and what
held) is kept in the skills as cautions, because Sulfur's client text recommends several moves Mark measured as
landable. Where the client's current Sulfur text and a Mark law disagree, the Sulfur text decides what is allowed
and the Mark law decides how it is built (`stumping` Part 1.0 lists every such conflict and how it is resolved).

## STOP: no solver, no scored reader, no probe

No in-house solver runs on any build under any name: no scored readers, no call-only or draw probes, no "cold"
reader that solves the prompt and hands back figures. Stump power is argued on paper (`precut.py`, the design
note's ladder and `## Deep reasoning`) and measured by the platform's two runs alone, which `/triage-runs` reads.
The leak reader reads the pack for leaks and never solves it; the determinism judge recomputes the golden and
never searches for the stump.

## The Sulfur standard comes first

The client's own text is in `guidelines/client/` (exported 2026-11-07): `latest_update.txt`, `overview.txt` and
`deep-reasoning.txt` are the bar; the learning modules, examples and quality checks sit beside them.

**The bar.** Two model runs are generated from the prompt and the pack, both graded against a rubric generated
from the prompt and the answer. The task passes when the **average of the two runs is under 60 per cent**
(exactly 60 fails; 72 and 40 passes at 56) **and both runs lose for a genuine analytical reason**: reviewers read
where each run first went wrong. Runs that lost on a formatting slip, a misread clause or a missed planted detail
fail the bar at any score. **Build to 50 on paper** (`supplemental-stumping` Part 0): the paper estimate is a
model and the platform is the measurement.

**Deep reasoning decides the answer.** The deciding step takes **three or more dependent inferences, at least one a
real statistical or modeling judgment the analyst has to justify from the data**, and the tempting wrong answer
comes from a reasonable analysis that does not go far enough. A competent analyst builds a clean answer that
passes its own checks and is wrong because the decision needs one or two more analytical moves. The judgments
that decide deep tasks: a comparison that is actually clean; heterogeneity that pooling hides; uncertainty that
matches the design; variance beyond sampling noise; separating two explanations for one pattern; outcomes that
have not finished happening; a forecast that has to earn its place out of sample.

**Banned as the deciding stump**, alone or several side by side, even when the task is deterministic and correct:
1. **Rule application**: the answer follows from a procedure, precedence or tie-break the files spell out.
2. **Data semantics**: the answer flips on reading one field, definition, clause, population or window one way.
3. **Planted defect or decoy**: the answer flips once one inserted problem is caught (a copied block, test rows, a
   shifted clock, a hidden extract, a mislabeled column, a wrong denominator).
4. **Replay or flip-the-wrong-number**: re-deriving a published figure, or a stated number that is simply wrong.
5. **Single-fact surface stump**: one sentence of help ("that file is a 10 per cent sample") makes it routine.
6. **Unpinned ambiguity**: two defensible readings or methods give different answers.

**The test, answered in writing for the main call:** suppose the solver cleans the data perfectly and reads every
instruction correctly; can it still reach the wrong answer by a reasonable but insufficient analysis? Yes is
analytical. No is a banned kind, and the build is redesigned. **The one-fact test** is answered beside it: name the
single sentence that would rescue a run; if one exists, the stump is surface.

**Mess is texture, never the stump.** Real files carry duplicates, inconsistent codes, gaps and layout drift, and
the solver must clean them; cleaning must never decide the answer (`dataset-generation`). **The domain is used, not
borrowed**: the deciding step needs the assigned field's own reasoning; swap the nouns for another field and the
task must stop making sense (`guide-to-prompt`).

## What Mark's feedback loop measured, and Sulfur keeps

These are the laws behind the skills, each paid for by a landed or returned build (`stumping/references/evidence.md`,
`strategies.md`, `shipped-ledger.md`). A Sulfur strategy that walks into one of them is redesigned, not shipped.
**`stumping/references/sulfur-strategies.md` is the author's union of the client's per-domain strategies and Mark's
families, minus every form Mark measured as not working**: each strategy is labelled WORKS, WORKS IN FORM (the dead
form named and banned), DOES NOT WORK (never the deep step, only rung 0 or 1) or UNTESTED. Read it before every draw;
`precut.py` refuses a design whose `Strategy label:` is DOES NOT WORK.

- **The field's named method is the opponent's first move.** Models execute the textbook method for the deciding
  quantity by reflex (analyse as randomised, the cluster-robust interval, the standard correction). A golden that
  IS that method is landed. The field's method sits at rung 0 or 1 of the ladder and the deep step is what this
  dataset needs beyond it (`stumping` 1.1b).
- **Anything written down is executed.** A filed sentence, helper document, release note, or pin that names the
  step, its clock, window, grouping or population hands it over (`stumping` Part 4). Documents describe fields,
  never process.
- **The WHAT screen.** A deep step that settles the population, outcome, window, unit or comparison is a fork or a
  rule, never a stump; no pin repairs it (`stumping` 1.2).
- **A grouping choice cannot carry the stump on its own** (pooled against stratified shows in the fit or forks the
  answer). Heterogeneity decides only through what the decision does with the groups, such as weighting them to
  the population the decision serves (`stumping` 1.1c).
- **A rung stacked on a solved step never held; hardening the asks after a landed call never rescued a build.** A
  landed call is redesigned at the deep step.
- **Devices whose discovery is their remedy are work orders**: the hygiene battery (duplicates, clocks, re-keyed
  records, latest-version rules) is run by reflex and decides nothing.

## Skill routing (binding)

Invoke the skill before the work, whatever the request's wording; if two apply, both, in pipeline order.

| Doing this | Invoke first |
|---|---|
| Starting or re-rooting a build, or asking whether a build repeats an earlier one | `fingerprint` |
| The domain fit, the answer's shape, the main recommendation, `prompt.txt` | `guide-to-prompt` |
| The deep step, the default path, the ladder, the banned-stump screen, re-rooting | `stumping` |
| The asks and the rubric arithmetic | `supplemental-stumping` |
| Forcing a unique answer while designing, or checking a build against the judge's gates | `determinism-check` |
| Building or repairing the pack under `target/` | `dataset-generation` |
| Writing or editing `submission.md` or any golden deliverable | `submission-writeup` |
| Making a golden read as a real work product (after its figures are asserted) | `golden-realism` |
| Declaring a pack ready, or recording a fix that came back from review | `reduce-house-fixes` |
| Checking a cut pack and prompt for anything that hands over the answer or the method | `leak-check` |
| Taking a task to the platform, resuming a build, reading the runs, repairing a returned one | `build-pipeline` |

## Commands and effort

| Command | What it does | Effort |
|---|---|---|
| `/build taskNN <domain> <objective>` | intake, draw, design, build, leak reader and judge, ready for the platform; resumes from `pipeline.json` | max |
| `/triage-runs taskNN` | records both run scores, classes each run's first wrong step, routes the build | medium |
| `/fix-determinism taskNN <finding>` | closes a fork (a run's defensible alternative or a judge finding); the call and the deep step stay frozen | max |
| `/fix-rubric taskNN` | the call held but the average is 60 or more: reworks the asks so they ride the deep step | max |
| `/approve taskNN` | the mechanical sign-off before upload (heart, surface, precut, leak verdict) | medium |
| `/leak-check taskNN` | `leak.py` plus one isolated reader | medium |

Every spawned agent (the leak reader, the determinism judge, the run triage) runs at medium effort, set in
`.claude/agents/` or on the `Agent` call. No isolated thread runs on the model's own initiative; the commands above
license the ones they name.

## The workflow

```
0 INTAKE   the assigned domain (one of the 21 subdomains) and objective; a starter data kit or own sourcing;
           status.py new for the number                                       pipeline.json DRAWING
1 DRAW     guard.py recent, coverage and mechanisms; the domain fit and shape; the card through guard.py
           check, then register                                               COMMIT "DRAWN (taskNN)"
2 DESIGN   the default path ending on a wrong answer, the deep chain (3+ inferences, the judgment named),
           the banned-stump screen, the ladder, fork and closure tables, the asks, prompt.txt
                                                                              gate: precut.py exit 0
3 BUILD    generator, pack, goldens, submission.md (the platform's four answer blocks)
           gate: generator checks, verify, two byte-identical builds, figures_check.py, the realism sweep,
           golden-realism, reduce-house-fixes, leak.py, guard.py surface and heart
4 CHECK    the leak reader and the determinism judge spawned together in the background; every finding fixed
           in the generator in one pass; a FIX_NOW re-judged once
5 READY    every gate re-run on the final cut; target.zip and the golden ZIP from the final rebuild; the author
           uploads the prompt and target.zip                                  COMMIT "READY (taskNN): <call>"
6 RUNS     the two runs come back: /triage-runs records both scores, classes each first wrong step and routes
           (submit, /fix-determinism, /fix-rubric, a surface trigger made texture, or redesign from 2)
7 SUBMIT   triage SUBMIT, the Reward block filled, submitted                 COMMIT "SUBMITTED (taskNN): ..."
           the review result later: APPROVED or RETURNED                      COMMIT "APPROVED" / "RETURNED"
```

One session runs the whole build in its main thread at max effort: design and build are the same hand, and a
repair is done where the context already is.

**The fingerprint guard is mandatory and free.** The card is registered the moment the draw is fixed. The 20 Project
Mark cards under `fingerprint/cards/` (filed as `markNN.json`, Mark's taskNN: 110, 111, 114, 115, 117, 119, 120, 124, 126, 128, 132, 135, 162, 169, 175, 179, 182, 196, 253 and 258) and
their shipped-ledger rows are the already-submitted baseline: a Sulfur build that repeats a Mark build's
driver, shell or data structure is a duplicate ("two tasks built on the same pattern with the same data structure are
treated as duplicates"). Personas come from `guard.py names`, never typed.

**Determinism is a construction, not an inspection**: invoke `determinism-check` while the ladder and the generator
are written. Its judge is spawned at stage 4, by `/fix-determinism`, or when the author asks.

## Git: one branch, commits at status changes only

The repository is `https://github.com/sathyaNEU/sulphur.git`, branch `main`. No other branch, no pull request.

- **Every status commit lands on `main`, whatever branch a session starts on.** A session that was handed a working
  branch (by its harness, a setup step or a default) still commits and pushes `DRAWN`, `READY`, `RESHIPPED`,
  `SUBMITTED`, `APPROVED`, `RETURNED`, `PAUSED`, `RETIRED` and `SKILLS:` commits to `main`: check out `main`, `git pull
  --rebase origin main`, commit there (or bring the work over with a rebase or cherry-pick), then `git push origin
  main`. Work left only on another branch is not shipped, and no pull request is opened for it.

- **Commit only at a status change**: `DRAWN (taskNN)`, `READY (taskNN): <call>`, `SUBMITTED (taskNN): <call>, runs
  <x> and <y>`, `APPROVED (taskNN)`, `RETURNED (taskNN): <why>`, `RESHIPPED (taskNN): <what moved>`, `PAUSED
  (taskNN)` with the resume step in `pipeline.json` (only when a session ends mid-stage), `RETIRED (taskNN)`. A
  skill change is its own commit, `SKILLS: <the rule>`.
- **Each commit carries every artifact that status touches**: the task folder, its card, and from READY on
  `target.zip`, the golden ZIP and `golden/` added with `git add -f`. Stage paths by name; never `git add -A`.
- **Before every push**: `git pull --rebase origin main`, then push. Never force-push or rewrite history; never
  commit `.cache/` or anything `.gitignore` names.
- Status lives in each build's `pipeline.json` (`DRAWING`, `DESIGN`, `BUILD`, `READY`, `RUNS`, `SUBMITTED`,
  `APPROVED`, `RETURNED`, `PAUSED`, `RETIRED`); `python3 .claude/skills/build-pipeline/status.py` prints the board.

## Task numbers

Sulfur builds are numbered from `task1` up (`status.py new`); the Mark baseline cards are filed as `markNN`
(`mark110` to `mark258`), so the two never collide. The platform's tier sets how many run at once (one at Tier 1, three at Tier 2, six at Tier 3).

## How a build is worked

1. **Deliver before bookkeeping.** Finish and hand over what was asked; only then skill lessons, house fixes or
   memory.
2. **One design note per build, with an append-only `## Tried and rejected` section** (that exact heading). When an
   approach dies, add one line: what was tried and why it died, written when it is abandoned.
3. **No backups, snapshots or versioned design docs** in a task folder. Allowed beside the note: `pipeline.json`,
   `metadata.json` (outside `target/`), `generator/figures.json`, the leak, determinism and triage reports, `runs/`.
   A build that cannot be rebuilt from its generator has a broken generator.

## Standing rules

- No em dashes anywhere in the repo. Use a comma, or parentheses for an aside.
- **Containers are scrubbed by construction, and checked before every ship.** Every shipped PDF is exported by a word
  processor (`reduce-house-fixes/scripts/writers/officepdf.py`), never FPDF, ReportLab or matplotlib and never
  relabelled; every workbook, document and deck passes through `writers/postprocess.py` (shared strings, the
  application's dialect, no library template, its own creator and stamps); no two files share a stamp and both zips
  carry each file's own save time. `audit_containers.py taskNN` exits 0 on the final cut before any READY,
  RESHIPPED or upload (`reduce-house-fixes` H1).
- **No dollar sign before a digit in a skill body.** The skill loader reads `$0` to `$9` as argument placeholders.
  Write the unit in words (`USD 38M`).
- Every figure in `submission.md` recomputes from `target/`, and a figure shared by two deliverables agrees in both
  to the same rounding.
- Skills state the current spec only: rules rewritten in place, no changelogs, no dated blocks. Build IDs and
  measured numbers stay where a rule stands on them. A Mark build ID cited in a skill is Mark's measured record.
- `guidelines/client/` is the client's export. Where it is newer than a skill, the client text wins and the skill
  is brought up to it in a `SKILLS:` commit.
- **Prompts are written the Mark way, then the author rewrites them for voice.** The draft is short and crisp (one
  plain paragraph under 1,000 characters, question first, no persona, rounding once at the end) and it is correct
  and leak-free: it pins the question, the decision, the deciding outcome or threshold and the deliverables, and
  never names the method, the comparison, the adjustment or a step, and never warns. The author's rewrite comes back
  through `voice-check.py --rewrite` (leaks fail, voice only warns) and `leak.py` (`guide-to-prompt`, `leak-check`).

## Current spec

**Determinism is literal.** The judge executes the shipped text word for word. The estimand (population, including
members not yet observed, outcome, window, unit, comparison) is filed so its literal execution is the golden; the
method stays open only where the design, a standard's general method or a filed selection criterion forces it,
with the data separating the candidates. Every term and convention has a row in the design note's fork table,
closed by a sentence or `same call`, asserted in `checks.py`; `precut.py` refuses an open one. The rival methods are
run, not argued: every defensible rival lands on the golden's call or is ruled out by named data.

**Every stump is bespoke.** The deep step comes from the dataset's own structure, and the design note says why in
one data-native sentence. The client's examples, example prompts and per-domain strategies are direction, never
templates: two tasks on the same pattern with the same data structure are duplicates.

**Inputs** (`dataset-generation`): 10 or more real, usable files (system files do not count), in 2 or more file
categories (spreadsheet, database, text, image, code; archives do not count but their contents do); at least 2
large, messy files, both CSV: one of 20,000 rows or more, and one that runs 10 to 20 printed pages or more (the Key
requirements page says a CSV; the Input files page also allows a long report or spreadsheet, so a CSV meets both),
each carrying realistic mess that must be cleaned and reconciled; at least 2 distractors that look relevant and
are unused, never labelled in a file name or anywhere inside the ZIP; cross-file reasoning required; every file
license-clean with source, pull date and license recorded in `metadata.json` (outside the ZIP); nothing LLM
generated, fabricated, padded or broken on purpose, and no file that reveals how the task was built or exists only
to carry a trap.

**Deliverables**: one deterministic main recommendation; one to three files in formats a real analyst would produce
for the decision (not `analysis_report.pdf` by default); a visual where it makes the call read at a glance.

**Asks**: no cap and no target count; each is hard and multi-dimensional (many rows, periods, segments or
calculations resolving to one gradable answer), unit and rounding inside the asking sentence. The answer's shape
(a ranked list under a cap, a bridge, a grid, a forecast across periods) supplies the rubric's criteria, and a run
that took the wrong analytical path gets them wrong (`supplemental-stumping`).

**Answer blocks** (`submission-writeup`): Final Recommendation (one or two sentences, first, naming what it rejects);
Supplementary Questions (a numbered list, one number per sub-ask, describing how each requested file should look);
Critical Components (2 to 5 load-bearing figures, the deep step among them); Step-by-Step (a short numbered path
from the raw files, showing the deep step and the reasonable but insufficient analysis it rejects), closing on why
no other conclusion survives. **The golden ZIP holds exactly the files the prompt requests**, one set of numbers
everywhere, nothing LLM-looking (`golden-realism`).

**Rubric**: generated from the prompt and the answer blocks; recommendation and critical components carry the most
weight, then the asks, then a small share for instruction-following. Edit a criterion only when it is clearly wrong
or missing, then re-run the evaluation.

**Domains**: the client's seven major domains and 21 subdomains (`guide-to-prompt/references/domains/`, client text
in `guidelines/client/domains.txt`). One subdomain, one task type, one objective. **Objectives**: Forecasting &
Predictive Modeling (especially welcome); Anomaly Detection & Diagnostics; Root-Cause Analysis; Experiment & Causal
Analysis; Descriptive & Distribution Analysis; Data Extraction & Conformation (ETL / Pipeline Build); plus the house
tags Opportunity Sizing & Decision Support and Data Quality Monitoring & Alerting, valid only where the prompt could
not be retagged without changing a word.

**Gate G**: no shipped artifact ranks the candidates on the decision question and gets it wrong. The difficulty
survives deleting every wrong number from the pack. **The call is forward facing by default**: a quantity about a
window not yet closed; a retrospective call is legal with its reason in the design note.
