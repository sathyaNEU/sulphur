---
name: fingerprint
description: The anti-repeat system for task builds. Every build has a fingerprint card under cards/ (domain, subdomain, niche, objective, prompt shape, decision type, gap, pattern, generators, Gate G mechanism, calibration form, context artifact, stakeholder role, spine, world, deliverables, opening move, and a driver sentence with the domain nouns stripped), and guard.py checks a proposed draw against every card before the ladder is written, so the same kind of project is never drawn twice. Every card also carries the client's own skeleton (decision form, deciding lessons, detection, resolving moves, file roles, answer pattern), and skeleton.py compares it element by element with every card, every lineage entry and every task the client has shown us (corpus/client_skeletons.json: the Templated Task Examples pairs, the 17 depth-scale tasks, the 15 examples) at the client's three severities (near copy, templated, variant), counts how often each lesson is already taught, and refuses a reskin, a re-pointed scaffold or a lesson taught twice, never cleared by differentiation. Use at the start of every new build and every re-root (guard.py recent, coverage, suggest), when the draw is fixed and before any data is cut (guard.py check, then register), after the pack is cut (guard.py surface), and whenever the author asks whether a build repeats an earlier one. Mandatory, mechanical and free, it spawns nothing; a promoted pair is read side by side by the author. The 20 Project Mark cards kept (110, 111, 114, 115, 117, 119, 120, 124, 126, 128, 132, 135, 162, 169, 175, 179, 182, 196, 253 and 258), filed as markNN.json (Mark's taskNN), with their shipped-ledger rows, are the already-submitted baseline every Sulfur draw is checked against.
---

# Fingerprint

> The cheapest place to stop a repeat is before the first file exists.

## Part 0. What this is for

The ledger holds each build's status and portal result; a card, filed when the draw is fixed, holds identity
in one vocabulary, so the guard bans against builds in flight. **A card records identity, never outcome**
(status and outcomes go to `stumping/references/shipped-ledger.md`), except `lineage`, which keeps each dead
architecture's fate: a driver already solved is the worst redraw.

## Part 1. The card

`cards/taskNN.json`. Every enumerated field takes a key from `vocab.json`; `guard.py validate` refuses
anything else.

| Field | Records |
|---|---|
| `domain`, `subdomain`, `client_domain` | domain and subdomain; the client domain a house domain sits in |
| `niche` | the unusual sub-function, in the build's nouns (similarity) |
| `objective`, `shape` | the assigned analysis type (one of the nine in `vocab.json` objectives); prompt shape `01` to `18`, `single-figure`, `other` |
| `answer_shape`, `weight`, `chain_signature`, `results` | from 2026-11-09: one of the fourteen answer shapes; where the weight of the work sits (one of the eleven); the areas of the results chain in order (four or more, three or more distinct); the chain in one line |
| `decision_type`, `answer_unit`, `scoring_unit` | kind of call, its unit, the unit it is scored or paid on |
| `gap`, `pattern`, `generators` | decisive first |
| `gate_g` | the mechanism carrying the stump |
| `calibration_form`, `context_artifact` | calibration organ (`none` allowed); the stakeholder's file type |
| `stump_strategy` | the family of the decisive move, from the dataset's own analytic structure |
| `decisive_rule_filed`, `official_decoy` | booleans; `false` plus `true` is the withheld rule with an official decoy, whatever the strategy says |
| `validated_decoy` | the wrong method reproduces every certified figure and only a forward condition breaks it |
| `stump_class` | `analytical`, `planted`, `data_semantics` or `rule_application`; only `analytical` passes |
| `analyst_test` | what the careful but hurried pass files on the results it loses, and why (on retired cards: the easy route and its wrong answer) |
| `domain_test` | the field's own analysis that decides, and why a noun swap breaks the task |
| `layer2_family`, `layer2_pattern` | family from `vocab.json`; pattern `<domain>/<task-type>/<n>` from `layer2-rigor-patterns.md`, or `own:<name>` |
| `layer1` | the Layer 1 techniques the pack carries |
| `stakeholder_role`, `role_family` | the role as stated, its family |
| `spine` | file, rows, row meaning, grain, source dataset |
| `world` | geography, currency, org type, invented nouns, `people` |
| `forum`, `forcing_event`, `org_family` | who decides, what forces it now, the kind of organisation; always declared |
| `deliverables`, `opening_move`, `question_form` | the deliverables (the golden's file names; the prompt itself asks by type); `question-first`; how many, how much, which, whether, what, when, who, where |
| `driver` | **one sentence, the decisive move with every domain noun stripped** (similarity) |
| `driver_concrete`, `stump` | the move in the build's terms; the wrong committed answer and the step that lands it |
| `answer`, `answer_source` | the committed answer verbatim, its source |
| `lineage`, `differentiation` | earlier architectures with fate and driver; `{taskNN: one line}` against a flagged build |
| `architecture_spent` | `true` when this card's own draw is dead and the slot has moved past it: the card then holds no axis ban, while its driver, stump and lineage are still screened against |
| `shell`, `lineage_shells` | the prompt's shell as `guard.py register` reads it off `prompt.txt` (question form, second-sentence opener, deliverable set), and the shells of this slot's dead architectures; the portal reads the shell beside the driver (`stumping` Part 6) |

**The driver catches the reskin.** Strip industry, organisation, metric names and figures; keep what
quantity decides, where it comes from and what it does to the naive answer, so one insight in two
industries yields near-identical sentences.

```
weak    The analysis has to account for an important constraint in the data.
strong  The decisive quantity is a per-unit floor recovered from a closed corpus of past
        determinations, and applying it removes the largest naive candidates from the total.
```

## Part 1b. The skeleton: the client's own duplicate test

The client compares two tasks on their skeleton, not their setting (its Templated Task Examples page, read
2026-11-11): five send-backs, each a pair from one fellow, laid side by side element by element. "The reviewer reads
both tasks in full, swaps the nouns of one into the other (stores become suppliers, valves become shrubs), and counts
how many parts of the analysis carry across unchanged. A change of domain does not reset the count." And a second
question: "does the dataset already teach this lesson? If two accepted tasks already turn on the same deciding step,
a third copy teaches a model very little, even when it is built from scratch." Its three severities are all sent
back: **near copy** (the same trap, method and file roles), **templated** (the same deciding lesson inside the same
scaffold with one part re-pointed: new physics, a different estimator), **variant** (real new work, but the step that
decides the answer, or the decision skeleton around it, is already in the dataset).

So every card carries `skeleton`, in `skeleton_vocab.json` keys:

| Element | Holds |
|---|---|
| `decision_form` | what is chosen and how (rank and name one; the k largest over a screen with a runner-up; act only if an interval clears a line; a set over a filed line; a count to a standard ...) |
| `answer_pattern` | the result's shape (the winner climbs from far down; k of n pass with budget slack; the point says act and the interval says no ...); generic patterns identify nothing |
| `lessons` | the deciding lessons, **the one the call turns on first** (106 keys, 43 of them closed by the client's page of 2026-11-12, at the grain the client's pages use: "a naive interval that treats correlated units as independent", "the noise of the planned design, not the raw spread") |
| `mechanisms` | the build's own physics as free slugs, so a near copy that keeps the mechanism is told from a templated build that re-points it |
| `detection` | how the solver notices each |
| `moves` | the resolving moves |
| `file_roles` | which file plays which part |

Lineage entries carry theirs, so a re-root meets its own dead architectures. `skeleton.py` (imported by `guard.py
check`, so register, heart and `/approve` all run it) compares the draw with every card, every lineage entry and
everything the client has shown us (`corpus/client_skeletons.json`: the five pairs and their sent-back siblings, the
17 depth-scale tasks, the 15 examples), with no window and no differentiation:

- **severity 1** when every deciding lesson, its resolving move, the mechanism, half the specific file roles and a
  specific decision form or answer pattern carry across; **severity 2** when every deciding lesson and a resolving
  move carry into the same specific decision form or answer pattern; **severity 3** when the lesson the call turns on
  is decided inside the same specific decision form, or a shared lesson sits inside the same specific form and
  pattern, or the specific form and pattern, the resolving move and the file roles carry with new lessons. Common forms
  (go or hold on a figure, a forecast with its range, a set over a line, rank and name one, one of a few options, a
  dial) and common patterns (the naive figure across the bar, shortcuts on distinct wrong answers) identify nothing on
  their own; the client's pages name specific ones ("rank six, name one" with its minute, "twelve units, at most
  three, a runner-up", "act only if the whole interval clears"). Severity 1 and 2 BLOCK; severity 3 BLOCKs against a
  task that teaches when the chain has two lessons or fewer or the pair shares two; on the slot's own lineage
  severity 1 and 2 BLOCK.
- **The lesson count** counts the tasks that teach: the client's accepted and level 3 tasks and our approved builds
  (`corpus/approved.json`; a card records identity, never outcome). The deciding lesson taught by two or more BLOCKs a
  chain of one or two lessons; more than half the chain's lessons taught twice BLOCKs any chain; otherwise each taught
  lesson is a WARN (it may be one step among several, as task6 v7's design weights sit beside two judgments no task
  teaches). A lesson on two or more of our own live builds is a WARN (`skeleton.house_lesson`): once they are
  accepted, a third reads as a re-set.
- **The house shell:** a specific decision form with a specific answer pattern already on two live builds BLOCKs (the
  client's "a third task with the ... shell reads as a house template"); a form on four live builds WARNs.
- **The client's closed strategies** (`guidelines/client/learning-modules/overused-strategies-2026-11-12.md`, held as
  `closed_lessons` in `skeleton_vocab.json`, with twelve neighbours in `closed_near`): 34 lessons that already decide
  two or more accepted tasks. A card whose deciding lesson is closed BLOCKs (`skeleton.lesson_closed`: "same mechanism
  and the same kind of fix counts as the same lesson", so a new domain, new data or a new detection never clears it); a
  chain of closed lessons only BLOCKs (`skeleton.lesson_closed_stack`); a closed lesson counts as taught for the
  half-taught rule; a closed lesson as a supporting step WARNs (`skeleton.lesson_closed_support`: its route alone must
  leave the call standing); a deciding lesson next to a closed card WARNs (`skeleton.lesson_closed_near`, answered in
  the note's `Closed strategies:` line). A card registered before `skeleton.CLOSED_FROM` (2026-11-12) meets these as
  WARN.
- A card registered before `skeleton.RULE_FROM` meets every skeleton rule as WARN, so no build already past design
  flips; every later card and every unfiled draft meets it in full, and a card with no skeleton BLOCKs.

```
python3 .claude/skills/fingerprint/skeleton.py check <taskNN or scratch card>   # the element-by-element read
python3 .claude/skills/fingerprint/skeleton.py lessons --min 2                  # lessons already taught twice
python3 .claude/skills/fingerprint/skeleton.py closed [taskNN]                  # the client's closed page, cards against it
python3 .claude/skills/fingerprint/skeleton.py matrix                           # every pair on file at 1 to 3
python3 .claude/skills/fingerprint/skeleton.py selftest                         # the calibration below
```

**The calibration it is held to** (`selftest`): the client's five pairs come back at 1, 2, 2, 3 and 3, its own
reading; task4 architecture 7 against architecture 6 is flagged (one term added to the same chain); the two builds
the client approved (task6 v7, task457 shipped as task14 architecture 1, task2 v6 and task14 v3) stay apart pairwise
and each passes as a new draw on the pair and lesson rules (the closed rule left out, since the page was drawn from
accepted tasks), while the closed probes hold: a call on a closed lesson and a stack of them are refused, one closed
supporting step beside a new deciding lesson is not, and task2 v6, whose deciding lesson the page has since closed,
would be refused as a draw today; every accepted client task at level 4 or 5 and every example passes as a new draw against the rest, except the
overlaps the client's corpus itself holds (example 14 is the recipe app's interval-unit lesson in its k-of-n shell;
three or four accepted tasks already turn on interference, the interval unit and the split carried to the decision,
so a new draw on one of them is the third copy); and a plain forecast with untaught lessons passes. Change a rule
only with the selftest passing. **What the matrix showed on 2026-11-11:** no build of ours is one of the client's five
examples (both Mark copies and every Sulfur pack were screened for the page's proper nouns: two village names appear
only inside public registers and a place-name list). The exposure is our own: task4's lineage at severity 1
(architecture 7 against 6), 2 (9 against 6 and 7) and 3 (10 against all four before it); task10 architecture 5, the
returned planted-factor cut, refused as a new draw (its one lesson, interference, is taught by four accepted client
tasks); task12 at severity 3 against the client's patrols task; and house lessons on our live builds
(`extrapolation_beyond_observed_range` on four, `transport_effect_modifiers` on five).

**Label honestly.** A skeleton is written from the design note and the results chain, never to pass: when two keys
fit, take the one a reviewer holding both tasks would use, and add a vocabulary key only when none is honest (reason
in the card's `notes`).

## Part 2. The procedure

**1. Before choosing the pairing:**

```
python3 .claude/skills/fingerprint/guard.py recent      # last builds, one line each
python3 .claude/skills/fingerprint/guard.py coverage    # spent and never-drawn cells, axis use overall and last 12
python3 .claude/skills/fingerprint/guard.py suggest     # optional fresh draws, never breaking a ban
python3 .claude/skills/fingerprint/guard.py mechanisms --objective <o>   # every spent driver there, lineage included
```

`mechanisms` is the one read of the corpus a draw needs: one block per build on the objective (narrow it with
`--gate-g` or `--strategy`), so no card is opened by hand. Write one line on the insight each spends before
drawing. **Then run the candidate through `slots`**, because the card corpus holds only the mechanisms that
were registered:

```
python3 .claude/skills/fingerprint/guard.py slots --driver "<the candidate driver sentence>"
python3 .claude/skills/fingerprint/guard.py slots funnel overdispersion --min-terms 2
```

It searches every number's design note and `pipeline.json` for the candidate's own words and prints the
matching lines with the heading they sit under. A screen recorded in a slot note is as dead as one recorded
on a card, and `recent`, `mechanisms`, `nearest` and `heart` cannot see it: an overdispersion-adjusted funnel
was rejected with measurements in two slots (task183's note and task194's, which names it outright) while
every card screen passed it, and a pass was spent on it anyway. A hit is not a repeat; read the line.

**Run `slots` on the SETTING nouns as well as the mechanism nouns, and run it BEFORE the first harness.**
One pass that did both recovered six measured deaths living only in other slots' notes, and between them
they pre-empted most of two whole cells: of the five client rigor cards across those cells, four were
already shipped or spent in-cell and the fifth had been set aside at another build's draw. Two of the six
were a rung-2 construction spent at Gate F with both readers landing the call, on the pass's own cell, which
is the most expensive thing a draw can learn late. The arithmetic is simple: the read costs minutes, the
harness it saves costs hours, and the card screens will not fire because a draw that never registered left
no card to fire against.

**`slots` greps design notes, so also read the neighbouring slots' `pipeline.json`.** A slot's `resume`
line carries the measurements of a dead architecture, including architectures that were reassigned to
another slot's cell, and no `guard.py` subcommand surfaces it: `recent`, `coverage`, `mechanisms`, `nearest`
and `slots` all miss it. One draw found that a sibling slot's architecture had already screened its exact
allocated cell with three measured mechanism deaths and had left behind a three-clause filter on what could
survive there, which then organised its whole pass. That one JSON read beat its first hour of search. Read
the `resume` of every slot whose cell, objective or client domain touches yours.

**Run `slots` twice, once on the mechanism's nouns and once on the physical setting's**, because they are
different screens and the setting run is the cheaper kill. A draw whose mechanism words returned nothing had
its setting words (the pathogen, the notification route, the laboratory, the epidemic curve) return two
earlier builds on its own cell, one of them the candidate exactly once the nouns were stripped, while
`check` scored it at 0.06 with neither build among the five nearest drivers: the driver score is lexical, so
the same insight told in the setting's words is invisible to it. On any cell the lane has drawn on before,
the setting run comes before the first harness, not after it. Everything here is mechanical and free; the people index and the clone screen keep working caches
under `.cache/` (never committed), seeded from the tracked baselines in `corpus/` and `clone/baseline.json` (both cut to the same twenty Mark builds
as the cards; the clone baseline holds the ten of them fingerprinted on Mark's checkout)
(the clone fingerprinter, `clone/fingerprint.py`, lives here now; the adjudicated clone check was dropped).

**2. When the draw is fixed** (before the ladder; personas from `guard.py names --geo <geo> --seed <N>`):

```
python3 .claude/skills/fingerprint/guard.py new task98 > <scratch>/task98_card.json   # fill from ## Draw
python3 .claude/skills/fingerprint/guard.py check <scratch>/task98_card.json
python3 .claude/skills/fingerprint/guard.py register <scratch>/task98_card.json
```

The registered card is committed at once with `pipeline.json` and the design note (`DRAWN (taskNN)`), so every
other session's guard sees the draw. The draft's `skeleton` is filled before `check` (Part 1b); run
`skeleton.py check <scratch card>` first, because its element-by-element table names what to redraw.

Clear every BLOCK by redrawing its axis; answer each WARN in one design-note line. `register` refuses a
BLOCK; `--force` is the author's override, reason in `notes`.

**2b. The window moves under you, and your own registration moves it.** The axis bans (`ban.forum`,
`ban.forcing_event`, `ban.org_family`, `ban.strategy`, `ban.pairing`, `ban.subdomain`, `ban.pattern`,
`ban.role`, `ban.artifact`, `ban.spine`, `ban.shape`) run against the last three builds by filing time, and
`register` stamps that time afresh. So registering your own card pushes the slot's previous architecture
out of the window and pulls another build in, and a late re-registration anywhere reorders every live
build's window at once. A clear verdict therefore has a short shelf life. **Run `check` against the
registered card as the last act of stage 1**, not against the draft, and run it again before relying on a
clear verdict at stage 2. Three builds hit this in one day: one cleared `ban.forum` twice post-registration
before landing on a third value, and one cleared three axis BLOCKs at stage 2 that had not existed when its
draw was fixed. Redraw the axis rather than argue it, since differentiation never clears an axis ban, and
say in the note which values were redrawn and why the replacement is the honester label and not merely the
passing one.

**3. Re-root:** move the old identity into `lineage` with its fate, write the new draw, check and register.
The guard compares against the slot's own lineage too.

**4. After the pack is cut:** `guard.py surface task98` runs the clone fingerprinter's hard-tell screen on the build
and re-reads persona names from the pack; a promoted pair is renamed or regenerated.

**4b. Duplicate check (stage 3, and `/approve`):** `guard.py heart taskNN` compares `driver`,
`driver_concrete` and `stump` with every driver, lineage driver, stump and shipped-ledger row, then runs
the full check; exit 1 on BLOCK. An empty `stump` is filled from the design note first.

**5. When the submission is final**, update `answer`, `answer_source`, `spine.rows`, `deliverables`,
`opening_move` and `question_form`. Part of delivery, because the next draw checks against it.

**6. The ledger row** is rewritten at each status change (drawn, built, shipped, re-rooted, retired) and
takes the portal result with its date the day the author reports it (`build-pipeline`, The ledger row);
the card is untouched.

## Part 3. What the guard decides

BLOCK if any rule blocks, else WARN, else PASS; exit 1 on BLOCK.

| Rule | Level | Against |
|---|---|---|
| `legal.domain`, `legal.objective`, `legal.gate_g` | BLOCK | the taxonomy; surface-read rejection or `statistical_rigor` alone |
| `ban.pairing`, `ban.subdomain`, `ban.pattern`, `ban.calibration`, `ban.role`, `ban.artifact`, `ban.spine`, `ban.strategy` | BLOCK | last three builds |
| `ban.source` | BLOCK, else WARN | the same real source dataset in the last three, else anywhere |
| `ban.shape` | BLOCK | last two |
| `ban.forum`, `ban.forcing_event`, `ban.org_family` | BLOCK | last three; `overuse.*` WARN when spent across the corpus |
| `template.withheld_rule_decoy`, `template.cap` | BLOCK | in any of the last three, or already two in the last twelve; `template.flagged` WARN on every carrier |
| `template.validated_decoy`, `template.validated_cap` | BLOCK | in the last build, or already three in the last twelve |
| `overuse.strategy` | WARN | one strategy in three of the last twelve |
| `three_rules.class`, `.analyst_test`, `.domain_test` | BLOCK | a card from 2026-10-10 missing them or not `analytical` |
| `throughout.answer_shape`, `.weight`, `.chain` | BLOCK | a card from 2026-11-09 missing them, or a chain under four results or three areas |
| `template.chain` | BLOCK, never cleared by differentiation | the same chain signature in the same order and the same answer shape as any card on file ("A lesson can come back in a new task. A structure cannot.") |
| `template.chain_near` | WARN | the same chain signature, or the same answer shape and weight |
| `ban.weight`, `ban.answer_shape` | BLOCK | the weight of either of the last two live cards; the answer shape of the last one (`overuse.weight` WARN within five) |
| `three_rules.strategy_risk` | WARN | `time_semantics`, `grain_or_unit`, `identity_resolution`, `stated_rule_hard_construction`, `withheld_rule_corpus_fit` |
| `test.same_puzzle` | BLOCK | gap, pattern and decision type equal, last twelve, lineage included (older: unless differentiated) |
| `test.same_driver` | BLOCK | gap, pattern and Gate G equal, last twelve, lineage included (older: unless differentiated) |
| `test.own_lineage` | BLOCK unless differentiated | the slot's earlier architectures |
| `driver.text` / `driver.near` | BLOCK unless differentiated / WARN | driver similarity 0.30 and up / 0.12 to 0.30, every driver on file |
| `shell.template` | BLOCK, never cleared by differentiation | the prompt's shell (question form, second-sentence opener, deliverable set) and the structural driver (gap, pattern, Gate G) both repeat an approved or delivered build, anywhere on file: the combination the portal's Duplicate finding named (task179 v3 against task175) |
| `shell.repeat` | WARN | the prompt's shell alone repeats an approved or delivered build; reword at the role level, never the verb |
| `skeleton.near_copy`, `skeleton.templated` | BLOCK, never cleared by differentiation | severity 1 or 2 against any card, lineage entry or client task (Part 1b) |
| `skeleton.variant` | BLOCK, else WARN | severity 3 against a task that teaches, when the chain has two lessons or fewer or the pair shares two |
| `skeleton.own_lineage` | BLOCK at 1 and 2, WARN at 3 | the slot's own earlier architectures: a landed scaffold re-pointed |
| `skeleton.lesson_taught`, `skeleton.lesson_once` | BLOCK, else WARN | the deciding lesson taught twice on a thin chain, or more than half the chain taught; once is a WARN |
| `skeleton.house_shell` | BLOCK at four live builds, WARN at three | the decision form's use across live builds |
| `skeleton.lesson_closed`, `skeleton.lesson_closed_stack` | BLOCK (WARN before `skeleton.CLOSED_FROM`) | the deciding lesson is on the client's closed page, or every lesson is |
| `skeleton.lesson_closed_near`, `skeleton.lesson_closed_support`, `skeleton.lesson_closed_half` | WARN | the deciding lesson next to a closed card; closed lessons as supporting steps; a card filed before the page that the closed count would refuse |
| `skeleton.missing`, `skeleton.vocab` | BLOCK | no skeleton, or a key not in `skeleton_vocab.json` (WARN for a card registered before `skeleton.RULE_FROM`) |
| `shell.lineage` | BLOCK | a re-root keeps a dead architecture's shell (task118 kept one across four worlds) |
| `tell.names` | BLOCK | a shared multi-word invented name |
| `people.full`, `people.inside` | BLOCK | a full name reused anywhere; two personas in one build sharing a first name or surname |
| `people.first` / `people.last` | BLOCK, else WARN | first name in 3+ builds or the last twelve / surname in 2+ or the last twelve; else one older build |
| `overuse.*`, `repeat.*` | WARN | domain, objective, shape, Gate G, decision type, deliverable set, PDF share, opening move, question form, geography, niche |

- **Three and twelve:** the neighbours a reviewer holds, and one sitting. The axis bans run against the
  last three **live** cards: a card carrying `architecture_spent` is skipped, because those bans exist so a
  reviewer does not read two similar builds side by side and a dead architecture is read by nobody. The
  similarity rules and `slots` still see it, since a spent driver is the one most expensive to repeat.
- **Two structural tests:** the Template clone on record (task86 v1, task72 v2) differed only in decision
  type, so `test.same_puzzle` alone passed it.
- **Differentiation** clears only similarity rules, never axis bans, and never a BLOCK whose shell half
  matches an approved or delivered build: the portal holds every accepted task with no window, and the one
  build ruled past a heart BLOCK against an approved build ("window fixed at draw", task179 v3 against
  task175) came back as a Duplicate. A line that cannot be written is the finding.
- **The shell is read at register and at heart** from `prompt.txt`, so a card registered before the prompt
  is written carries no shell until `heart` or `/approve` re-reads it; `voice-check.py` holds the corpus
  quotas on the same classes (`guide-to-prompt` §3).
- **Drawn, never typed:** personas (one first name stood in 23 builds), furniture (committees and boards
  decided 49 prompts, regulators none), and pack file names in the organisation's idiom.

**Look up a strategy's ban window before spending design time on the direction.** `ban.strategy` is an
axis ban, so differentiation does not clear it and no argument will: a direction is either available or
it is not, and that is a fact to read off `coverage` and `recent` in the same breath as `mechanisms`,
before the design exists. task194 drew a sound architecture on `maturity_censoring` and could not
register it, because the immediately preceding build in the corpus carried the same label. Two costs
follow from checking late. The design waits for a window to lapse rather than being drawn into a free
cell, and the builder is put in front of a choice between relabelling the mechanism to pass the guard,
which is a lie in the card, and waiting. Neither is taken: the direction is redrawn at once, and when the
seed's world offers no honest unbanned direction the build moves to another client domain and dataset
(`CLAUDE.md`, A stuck build is unblocked, never parked); the better outcome is never to face it.

## Part 4. How this goes wrong

- **A PASS read as "not a clone"**: the design note still answers the similarity test.
- **The guard checks the vocabulary, not whether the design earns the label.** `guard.py check` PASSed a
  card whose `gate_g` was `binding_constraint` whose stump was in fact carried by the exposure population,
  and the draw that wrote it refused its own label rather than keep the PASS. A `gate_g` is honest only
  when the named mechanism carries the decisive step: `binding_constraint` needs the limit itself to change
  the naive pick, and on a ground where the binding quantity is not estimated it cannot. Read the vocab
  entry against the design, and when they disagree say so rather than banking the PASS.
- **A card written to pass**: if two keys fit, use the reviewer's. **A vague driver**: no quantity, no source.
- **A stale card** after a re-root: the similarity rules run against the dead architecture and pass, and its
  axes fence off ground no live build occupies. When an architecture is spent, set `architecture_spent` on
  its card the same day, and move the identity into `lineage` when the new draw is registered. Four spent
  cards in one lane had closed four domain-and-objective pairings on an objective the taxonomy serves with
  14 task types, and one of them BLOCKed a fresh draw that no driver could have cleared.
- **Vocabulary drift:** a new `vocab.json` value only when none is honest (reason in `notes`); `other`
  exists so no untrue key is forced.
- **A never-drawn SUBDOMAIN read as open ground, which is the same error as the never-built pairing and is
  made twice as often.** A subdomain with zero cards may be unbuilt because the taxonomy does not let it
  serve the objective at all: one measured instance BLOCKs on `three_rules.task_type` with "task type
  alarm-interface-evaluation serves experiment-causal, not anomaly-detection: the domain would be a
  backdrop", and it returns the same BLOCK on a sweep of four objectives. Of six task types in that domain
  exactly one served the objective, and it was already carded. **Run `guard.py check` on a probe card before
  briefing a cell as available, never infer availability from a zero count**, and never from the phrase
  "never drawn".
  **It errs in BOTH directions and a third slot measured both at once:** the pairing it expected to be barred
  was legal (no `three_rules.task_type` BLOCK at all), while the obvious natural home for its mechanism,
  a sensor-calibration subdomain, is tagged for Data Quality Monitoring ONLY and cannot serve anomaly
  detection, which is why the two builds sitting there carry that objective instead. Probe both the cell you
  doubt and the cell you assume. A whole candidate was screened to a measured refusal on an illegal cell this way; its
  arithmetic stands but the ground it cleared was never there.
- **An axis ban read as aged out without measuring it, and an unstamped card is not in the window.** A
  strategy was briefed as legal because a build carrying it had shipped, and it measured `BLOCK ban.strategy`
  against a card registered the same day. Two things make that reading wrong. The window is the last three
  LIVE cards in draw order, so a ship does not retire a ban, and a card with **no `registered` stamp at all
  is not in the window by filing time**, so the shipped build that seemed to license the strategy was not
  the card the ban was measured against. Read bans off `guard.py check` at the moment a card is drafted, not
  off a wave contract, a reservation, or a remembered verdict: three separate stale readings were measured in
  one day, and a slot's own `paper_screen` line had two labels recorded as blocked that measured free.
- **A family offered on its label:** a mechanism `coverage` shows as never drawn may have died in lineage
  (confirm_surface_read: zero main uses, four lineage architectures, all solved). Read the fates first.
- **A never-built pairing read as a menu.** Most of the pairings `coverage` prints as never built cannot be
  drawn at all: no task type in that domain serves that objective, so `guard.py check`'s legality rules and
  `precut.py`'s `Task type:` line refuse them (actuarial-science-insurance offers forecasting, opportunity
  sizing and descriptive task types only, so its anomaly-detection cell is empty by construction). Before a
  pairing is drawn, read the objective tags beside each of that domain's subdomains in
  `../guide-to-prompt/references/domains/README.md`. The taxonomy is narrow on several objectives: ETL is
  served by 6 subdomains, data-quality-monitoring by 8, root-cause by 13 and anomaly-detection by 14,
  against 45 for forecasting. A house domain inherits the task types of the client domains it maps to, so
  its cells are drawable wherever theirs are; `coverage` separates the never-built pairings a task type
  serves from the ones nothing serves.
- **A draw tested as if it had been drawn yesterday.** `check` on an unfiled card gives it a key that comes
  after everything filed that day, so the axis bans run against the window a reviewer will really hold.
  That key used to be withheld when a card already sat in the slot, which is exactly the re-root case: the
  filed card is the architecture the draw replaces, so a re-root was tested against a window three builds
  stale. task190's re-root passed `check` on a window ending at task196 and BLOCKed on `heart` against
  task244 the moment registration gave it a real stamp, with the pack already cut. Fixed in `guard.py`, and
  the lesson stands anyway: **an axis a draw cannot clear is cheapest to find before the generator is
  written, so probe with `check` at the draw and again the moment the card is filed.**
- **A draw left unfiled past its day.** The same key places an unfiled card after everything filed on its
  `drawn` date and before anything drawn later, so a draw parked unfiled past that day is tested forever
  against the builds drawn by then, and no later registration clears its bans. A draw is filed on the day
  it is registered: `drawn` is set to the filing day, `check` runs against that day's window, and the card
  registers when it clears. task169 and task173, drawn the same day and parked unfiled, stayed blocked by
  that day's last builds while the corpus moved on.
- **A mechanism that died before registration.** The card corpus is a record of draws, not of screens, so
  every mechanism killed at stage 1 or 2 is invisible to `recent`, `mechanisms`, `nearest` and `heart`. Those
  kills live in each number's `## Tried and rejected` and in `pipeline.json`, and they are the cheapest
  screen on file because they come with measurements. `guard.py slots` searches them; a draw that skips it
  re-screens ground this repo has already paid for.
- **A driver repeat the text screen cannot see.** `driver.text` works on the sentence, so one insight told in
  another field's nouns scores low: a load carried by a fitted transfer scored 0.07 against the architecture
  that is the same insight in the same domain, under the 0.12 WARN floor, and two task500 re-roots passed
  `check` at 0.05 and 0.08 while repeating their neighbours' drivers. The abstraction test and `slots` are
  the complements; the number is never the answer on its own.
- **A house domain's occupancy read off its own label.** `coverage` counts the pairing by the house label,
  while `guard.py`'s `three_rules.task_type` rule and `precut.py`'s `Task type:` line route the draw
  through the **client** task types the house domain inherits. Those are different populations, so a house
  pairing can print zero and be thoroughly occupied: measured, `business-operations-analytics` prints 0 on
  anomaly-detection and its five inherited AD task types carry six cards, `accounting-audit-forensic`
  prints 0 and its three carry four. Three other house domains inherit no AD task type at all and are
  simply undrawable there. **Allocate on the inherited task types, never on the pairing count.**

  **No `guard.py` subcommand prints the inherited count, and the structural tests return a false clear on
  it.** Filing a probe card per inherited task type and reading the BLOCKs does not work, measured: three
  such probes returned an identical verdict, the same single BLOCK, the same WARN and the same nearest
  drivers, with no `ban.subdomain`, no `ban.pairing` and no `test.own_lineage` on any of them. The reason is
  in the rules themselves. `ban.subdomain` runs on `recent`, the last three **live** cards by filing time,
  so a card outside that window is invisible to it however exactly it matches; and `test.same_puzzle`,
  `test.same_driver` and `test.own_lineage` key on gap, decisive pattern, decision type and Gate G, none of
  which is the subdomain. So the occupancy is read straight off the card corpus, by filtering `cards/*.json`
  on `objective` and on `subdomain` over the inherited task types, and nowhere else.
- **A spent cell read as a spent objective.** `ban.subdomain` reaches the last three builds, so a cell
  whose mechanism search came up empty is drawable again next sitting: what binds a redraw there is
  `driver.text`, `test.same_puzzle` and `test.same_driver`, all of which are about the mechanism. A lane
  whose objective holds few cells will keep returning to them, and the honest pause note says the driver
  search on that cell is spent, never that the ground is. Moving the number to another cell is one way to
  find a fresh driver and the slowest: the drivers a cell leaves open are listed by
  `guard.py mechanisms --objective <o>`, which is one screen.
- **`pattern: none` moves the structural test.** With `pattern` set to `none`, `guard.py check` reads
  `generators[0]` as the decisive pattern in `test.same_driver` and `test.same_driver_older`, so which
  triple the test fires on depends on the generator list rather than on the pattern field. Read the verdict
  rather than predicting it: a draw this corpus expected to raise a WARN returned a BLOCK on that path.
- **Not registering.** An unfiled card protects nobody.

## Part 5. Maintenance

`guard.py validate` after editing a card or `vocab.json`; cards are edited in place. `register` stamps
`registered` with the filing time, and builds drawn the same day order by it (cards filed before the stamp keep
task-number order and come first), so a draw's bans reach the builds actually filed before it. Driver thresholds:
cross-slot 99.9th percentile under 0.10, a byte-identical rebuild 0.88, AUC about 0.6 for mechanism (hence
the structural tests); recalibrate with `guard.py nearest`. Cards to task36 carry fitted labels; builds
with no design note or ledger row carry `mechanism_source: submission_only`.
