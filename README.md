# Project Sulfur task builds

Each `taskNN/` folder (task1 up) is one deterministic analytical task built for Project Sulfur: a prompt, an input
pack, the golden deliverables, the four answer blocks for the platform, and after the platform's two runs, their
triage. The aim: tasks whose two runs average under 60 per cent because both lose on a deep-reasoning judgment, never
on a misread field, a written rule or a planted row. `CLAUDE.md` is the working contract and every session loads it.

This harness is Project Mark's (`sathyaNEU/real-world-data-extraction-conformation-etl-build-problems`), refreshed for
Sulfur: Mark's measured record of what stumped and what the models solved is kept as cautions, the client's Sulfur
spec sits in `guidelines/client/`, and `.claude/skills/stumping/references/sulfur-strategies.md` is the union of
Sulfur's and Mark's strategies minus every form Mark measured as not working.

## Start a session

```
/build task1 <domain> <objective>      # intake to READY: draw, design, build, leak reader and judge
/build resume task1                    # a paused build, from its pipeline.json
/triage-runs task1                     # after the platform's two runs: scores, first wrong steps, the route
/fix-determinism task1 <finding>       # a run took a defensible alternative, or a judge found a fork
/fix-rubric task1                      # the call held but the average reached 60
/approve task1                         # mechanical sign-off before upload
/leak-check task1                      # leak.py plus one isolated reader
python3 .claude/skills/build-pipeline/status.py      # the board
```

`/build`, `/fix-determinism` and `/fix-rubric` run at max effort; `/triage-runs`, `/approve`, `/leak-check` and every
spawned agent at medium. No in-house solver runs: the platform's two runs are the only stump evidence.

## Layout

| Path | What it holds |
|---|---|
| `CLAUDE.md` | the contract: the Sulfur standard, Mark's measured laws, routing, commands, workflow, git, the current spec |
| `.claude/skills/` | eleven skills, one per stage, scripts beside the skill that owns them |
| `.claude/commands/`, `.claude/agents/` | six commands; the determinism judge and the run triage agents |
| `.claude/skills/fingerprint/cards/` | 302 Project Mark cards filed as `markNN.json` (Mark's taskNN), the already-submitted duplicate baseline, plus each Sulfur card (`taskNN.json`) |
| `guidelines/` | the client's Sulfur export (`client/`) and the determinism judge's system prompt |
| `taskNN/` | the builds |

## Git

One branch, `main`. Commit only at a status change (`DRAWN`, `READY`, `SUBMITTED`, `APPROVED`, `RETURNED`,
`RESHIPPED`, `PAUSED`, `RETIRED`), staging paths by name, then `git pull --rebase origin main` and push. Packs and
goldens are rebuilt by each generator; a build tracks only `target.zip`, `golden.zip` and `golden/` from READY on.
