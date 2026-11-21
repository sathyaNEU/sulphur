# Project Sulfur task builds

Every `taskNN/` folder is one deterministic analytical task for Project Sulfur: `prompt.txt`, the input pack under
`target/` (shipped as `target.zip`), the golden deliverables under `golden/` (shipped as one golden ZIP), the answer
blocks in `submission.md`, and after the platform runs, `runs/`. The goal is one thing: tasks that clear the Sulfur
bar on the first submission and survive the project lead's review, because the difficulty runs through the whole
analysis and the runs lose their points in several places for analytical reasons. Everything below serves that.

This harness is Project Mark's, refreshed for Sulfur and rebuilt on 2026-11-09 for the client's new bar. Mark's
measured record (what models execute, what landed and what held) is kept in the skills as cautions on each result.
Where the client's current text and a Mark law disagree, the client text decides what is allowed and the Mark law
decides how a result is built.

## STOP: no solver, no scored reader, no probe

No in-house solver runs on any build under any name: no scored readers, no call-only or draw probes, no "cold"
reader that solves the prompt and hands back figures. Difficulty is argued on paper (`precut.py`, the design note's
`## Results chain` and `## Effort test`) and computed by `effort.py` from the generator's own implementations of the
golden and the hurried methods on the cut pack, which is arithmetic, not a solver: nothing reads the prompt. It is
measured by the platform's two runs alone, which `/triage-runs` reads. The leak reader reads the pack for leaks and
never solves it. The determinism judge checks determinism only (Gates A to E): it starts from the answer blocks,
recomputes them by their own stated method on the shipped files, runs the alternatives the prompt or the files leave
open, and never derives an answer of its own, prices difficulty or reports on the stump.

## The client's bar comes first

The client's own text is in `guidelines/client/`: `guidelines-2026-11-20.md` (the guidelines page of 11/20, read
2026-11-21 with the phase 2 announcement beside it in `phase-2-announcement-2026-11-21.md`), `deep-reasoning.md`
(2026-11-09) and `learning-modules/stumping-strategies.md` (2026-11-09) are the bar, with the project lead's review
of 2026-11-09 verbatim in `project-lead-review-2026-11-09.md` and the closed strategies, 45 as read on 2026-11-21, in
`learning-modules/overused-strategies-2026-11-21.md`; `latest_update.txt`, `overview.txt`, the learning modules, the
examples (17; `1.txt`, `16.txt` and `17.txt` are the hardest three, as shared on 2026-11-21) and the quality checks sit beside them. Read the page of 11/20,
the review and the closed page before every draw.

**Why the bar moved.** The project lead reviewed about 500 tasks and returned the pattern this harness used to
build: "most tasks hinge on one thing. Usually it's a hidden factor built into the data: a subgroup, an event that
hits the control group, a confounder that only shows up in the units that decide the call. Sometimes it's one clever
method choice. Either way, once someone's told that one thing, the rest is routine." And: "a factor you planted in
the data is really just a planted defect in a stats costume, so we will send those back." Tasks that passed every
check here (two runs under 60, analytical first wrong steps, a clean judge) were returned on this. **Going forward
the client rejects tasks that rely on just one thing, and so do we: no build ships that does.**

**The bar.** Two model runs are generated from the prompt and the pack and graded against a rubric generated from
the prompt and the answer blocks. The task passes when the **average of the two runs is under 60 per cent** (exactly
60 fails) **and the runs lose for analytical reasons**, and the reviewers read the design as well as the runs.
**Build to 50 on paper**: `effort.py`'s pair estimate is a model and the platform is the measurement. The two runs
are two rollouts of one submission; re-runs are cheap and allowed in moderation, never spammed, and a task already
submitted is reviewed against the same rules (the announcement of 2026-11-21).

**Two or more decisive, independent steps** (the page of 11/20). "Only one decisive step" is a send-back by name:
"even when the deciding step is real analysis, if it is the only challenging part of the task, catching it gives the
whole answer and missing it gives none." A task carries "two or more decisive, independent steps that each need real
reasoning", "missing one should not sink the others", and a run fails "by doing a reasonable analysis that does not
go far enough, not by missing one hidden detail". What that fixes in every build:
- **The Critical Components block is the decisive steps**: two or more, each with its correct answer and never its
  method ("The restated 2023 baseline is USD 4.2M", not "restate the baseline"); each answer sits in a deliverable
  the prompt asks for; and they are independent ("a model that gets one step wrong should still be able to earn the
  others"). So each component is one stump's own figure, asked for by the prompt as a quantity of the decision, and
  a figure that falls with two stumps is an ask (`corelib.py`, the row `critical components independent`).
- **One to four hard, multi-faceted supplementary asks**, never a long list of easy ones.
- **Three tests on every stump**: the one-fact test; the clean-data test ("a solver that cleans the data perfectly
  and reads every instruction correctly should still be able to reach the wrong answer through a reasonable but
  insufficient analysis"); the effort test (ten minutes, an afternoon and two days "should each score clearly higher
  than the last").
- **Every decisive step is reachable** from the prompt, the data and the documents ("no rule nobody wrote down and
  no source nothing points to"); **no unstated conventions** (the business definition is pinned in the prompt or a
  document, never the method); **the prompt must not point the other way** (a run that follows the prompt's own
  words is never marked wrong).
- **The `Valid Stump?` field** at submission answers three things for each decisive step the runs missed: where it
  fails, why it is fair, why it takes reasoning (`run-triage` drafts it from the runs; `build-pipeline` stage 7).

**What the client's hardest examples show** (`guidelines/client/examples/1.txt`, `16.txt` and `17.txt`, runs averaging
0.26 to 0.31; a difficulty profile and never a template, and by the announcement "likely already overused stumps"): each
decisive step needs its own fitted model or estimator; the runs saw the signal and kept it as a sensitivity check,
cut at a threshold instead of fitting, picked one arm instead of fitting both, or computed the counter-evidence and
set it aside; one effect stayed hidden behind a tangled neighbour until both were fitted together; today's level was
taken as normal where the option changes what produced it; a stream was extrapolated from its own history where its
generating cohorts had to be followed; and the independence is shown as a table (each step left out alone, then in
pairs, with the figure and the call each time).

**The review reads its strongest run, not the average** (`guidelines/client/approved-reviews-2026-11-14.md`, three
review sheets of other fellows' approved tasks). The Stumped gate rested on a single GPT-6 Astra run on each (rewards
22, 17 and 35; our builds that cleared the platform's average came back at 71 to 83), determinism on a blind fork
audit with the golden replayed across variants and every rival ruled on by a figure computed from the shipped files.
So the opponent every core is designed against is that run, a pair is submitted only when its higher-scoring run is
itself under 60, and the judge audits forks the way that review does (`stumping` Part 1d, `run-triage`,
`determinism-judge`).

**The rubric is priced for the run that loses one stump** (`supplemental-stumping` Parts 0 and 1). The generated
rubric gives 18 to the recommendation, about 20 to the critical components, about 53 to the asks and 9 to
instruction-following, one criterion per figure sentence of the blocks, and a run earns every figure its route
lands. Asks sited away from the stumps were collected in full by runs that missed the call (task6 architecture 6 at
73, task11 at 54 with no call), and the client's rubric page says "a wrong analytical path should get them wrong".
So every figure the prompt asks for and the blocks state sits downstream of a stump, most of them downstream of two
or more (each stump's process runs across the members, moving their figures outside the bands while flipping only
its own member's call), each stump keeps one figure of its own, and reflex work (counts, rebuilt totals, bases) is
done and never stated as a graded figure. `corelib.py` at design and `effort.py` on the cut pack refuse a build
where a run that loses any one stump still earns over 50 or the reflex route over 30; the design aims at the
twenties.

**Difficulty throughout.** The client's standard in one line: "A deep task asks for several pieces of genuine
analysis spread across the work, each ending in a result that can be checked, and more careful work keeps earning
more. It is never won or lost on one hidden or planted thing that, once caught, flips the whole answer." So every
build is a **results chain**:
- **four or more checkable results** (the worked illustration has six), drawn from **three or more of the fourteen
  areas** (framing; data discovery; assembly and reconciliation; missingness and measurement; exploration and triage
  at breadth; investigation loops; modeling; validation; causal reasoning; forecasting; decomposition and
  attribution; uncertainty; synthesis; self-verification), each pinned by the data or a stated convention, with a
  band where reasonable methods differ, each graded in an answer block;
- each result with the **hurried analyst's failure** a careful run actually makes there, one of the six deep
  classes: method shortcut, unfinished chain, stopped at the first story, narrow look at broad data, dismissed own
  evidence, self-confirming check;
- the **effort test** passed: a ten-minute pass earns a third of the results or fewer, a careful but hurried
  afternoon earns more, two days of self-checking work earns all of them, and no single sentence of help rescues
  more than a third (`stumping`, `effort.py`).

The careful but hurried column is calibrated to the run record, not to the design: frontier runs clean every file,
read every document, run the field's textbook method, model any pattern one plot shows, hold out, back-test and
bootstrap unprompted. A result whose only difficulty is one of those moves is earned by the runs.

**Banned, alone or several side by side** (one family: one hidden or planted thing that, once caught, flips the
answer):
1. **Rule application**: a procedure, precedence or tie-break the files spell out produces the answer.
2. **Data semantics**: the answer flips on reading one field, definition, clause, population or window one way.
3. **Planted defect or decoy**: a copied block, test rows, a shifted clock, a hidden extract, a mislabeled column,
   a wrong denominator, a memo written to carry the wrong answer.
4. **Shallow hidden factor**: a confounder, subgroup, contaminating event, timing break or measurement change built
   into the data that no document mentions, when it was constructed, one sentence about it leaves one routine step
   (a stratification, an extra term, a filter, a reweight), and it sits only in the deciding units or shows in one
   cross-tab or plot. The house rule is stricter: a constructed factor that sits only in the units that decide the
   answer is refused whatever its fix, because a real process would put it across the data.
5. **Replay**: re-deriving a published figure, or a stated number that is simply wrong.
6. **Single-fact surface stump**: one sentence of help makes the task routine.
7. **Unpinned ambiguity**: two defensible readings or methods give different answers on any result.
8. **Only one decisive step**: the deciding step is real analysis but it is the only hard part, so the answer is
   all or nothing on it. Two or more decisive steps, each independently hard, each with its own checkable figure.

**The closed strategies** (`guidelines/client/learning-modules/overused-strategies-2026-11-21.md`): 45 analytical
lessons that already decide two or more accepted tasks are closed, in six families. The 34 of the first read
(2026-11-12): regression to the mean, survivorship, outcomes hidden by the intervention, self-selection, occurrence
sampling, shrinkage, clustered intervals, overdispersion, attenuation, placebo baselines, censoring, competing risks,
late entry, the settled level, reporting lag, repeated exposure, limits as bounds, young cohorts, payback, used-up
easy cases, transport to a new mix, spillover, displacement, assignment odds, composition, closure diversion,
fixed-count rescaling, instrument change, survey change, fieldwork seasons, billing location, dependent capture, a
co-occurring change, hindsight. The 11 added by the read of 2026-11-21: adverse selection into an option, the
treatment changing who is left to measure, the outcome running on a different clock, a source that reads high or
low calibrated on checked cases, groups recorded less completely than others (gross up by completeness), old
figures restated to the target basis, a projection that holds fixed what the change will move, a straight line or
an average mispricing the margin, credit only for what would not have happened anyway, extrapolation past the
observed range, and scoring on the data used to choose. **None may be the step that flips a new build's answer**,
whatever the domain, data or detection ("same mechanism and the same kind of fix counts as the same lesson"); each
may be a supporting step whose omission alone leaves the call standing; two of them stacked with nothing new is a
repeat. `skeleton.py closed` lists them as the guard holds them, the guard blocks a card that turns on one or stacks
them (a card registered before a lesson closed meets it as WARN, a return risk at review), and the note's Frontier
check carries a `Closed strategies:` line (`stumping` Part 1c; the open ground is
`stumping/references/open-ground.md`).

**The depth scale** (`guidelines/client/depth-scale-2026-11-09.md`, the client's reading of 17 real submitted tasks):
levels 1 and 2 are sent back, level 3 (one real method step) is a judgment call kept about half the time, levels 4
(two or three connected judgments) and 5 (many independent judgments, different shortcuts landing on different wrong
answers) are the target. Every build names its level in the note and aims at 4 or 5. Learn from the examples, never
template them. Each level 4 and 5 task's prompt, inputs, reference solution and review notes are in
`guidelines/client/depth-scale-2026-11-09-detail.md`: the bar to beat, never a skeleton to copy.

**Thinner, not banned.** A legitimate method choice that carries most of the score, with nothing planted, is a
valid task but a thin one; the client asks for the results around that step. We build the results around it.

**The stump factorial** (`stumping` Part 3.3), on paper at design and computed on the cut pack: every judgment the
call can turn on is a reflex (runs make it unprompted, or a file spells it out) or a stump (a run has been seen to lose
it); the careful pass is the reflex route, never a route that also gets a reflex wrong; two or more stumps must each
move the call when dropped alone, and none may reach the call when fixed alone on the reflex route. Two is level 4,
three is level 5, one is a one-trick build and dies on paper. `precut.py` and `effort.py` refuse it.

**The one-fact test**, answered in writing for every build: name the single most useful sentence a reviewer could
give a run and count the results it rescues. It rescues a third of them or fewer, or the build is redesigned.

**Mess is texture and can be one result.** Real files carry duplicates, inconsistent codes, gaps and layout drift,
and the solver must clean and reconcile them; assembly can be a checkable result of its own, but cleaning never
decides the task. **The domain is used, not borrowed**: the results are quantities the assigned field estimates,
models or tests; swap the nouns for another field's and the task must stop making sense (`guide-to-prompt`).

**Vary where the hardness sits.** "Difficulty throughout is not a template." Each build names its analysis type (the
client assigns one of nine), its answer shape (one of fourteen) and where the weight of the work sits (assembly,
measurement, triage, investigation, modeling, validation, attribution, synthesis, allocation, a hard-to-measure
quantity, metric or rule design), and picks a weight not leaned on in the last builds. "A lesson can come back in a
new task. A structure cannot": the same chain of steps in the same order, the same question template or the same
answer shape is a template even on new data, and `guard.py` blocks it.

## What Mark measured, kept as cautions on every result

Each was paid for by a landed or returned build (`stumping/references/evidence.md`, `strategies.md`,
`shipped-ledger.md`). They now price results, not a single stump:

- **The field's named method is the runs' first move.** A result whose golden is the textbook method is earned by
  the runs; it can sit in the chain, but it counts as Right in the careful column, and the results that price the
  task need a move beyond it.
- **Anything written down is executed.** A filed sentence, helper document, release note or pin that names a
  result's step, clock, window, grouping or population hands that result over. Documents describe fields, never
  process.
- **The WHAT is filed, the HOW stays open.** Each result's population, outcome, window, unit and comparison are
  filed so their literal execution is the golden; a step that settles one of them is a fork or a rule, never a
  difficulty.
- **A mechanism the rows visibly carry is modelled on sight** (the Sulfur run record, five rounds): one plot or one
  group-by of one file shows it, so the careful column earns it.
- **Devices whose discovery is their remedy are work orders**: the hygiene battery (duplicates, clocks, re-keyed
  records, latest-version rules) is run by reflex and prices nothing.

## What Sulfur measured, binding on every draw

Thirty platform rounds to 2026-11-11 (`stumping/references/sulfur-record.md`):

- **Most rounds came back landed, and the paper pair estimates were 40 to 60 points high** (38.4 measured about 97;
  46.5 about 95). So a careful-column loss counts only where a frontier run has been seen to lose that kind of move
  (`stumping/references/precedents.json`, from our runs and the client's pages); `effort.py` grades every uncited cell
  Right and holds the cited pair estimate to 50. The exceptions are the approved builds: task2 v6 (26.0 on paper) and
  task14 v3 (49.5) passed, though the cited rule would have priced both at 100, because they lost where no run had
  yet been recorded losing (which partial source answers which part of the estimand); their runs' own lines are added
  to `precedents.json` once pasted.
- **The runs lose in six places** (`stumping` Part 1b): the split they see and then drop before the decision; the
  assumption they name and wave through, made false by the world's process and testable from another file; units
  selected by the outcome's own history; a response they assume instead of measuring, and the marginal unit; the
  system's net against the unit's own; a shallow path that passes its own checks. The first, third and fifth were
  closed as deciding lessons by the client's page of 2026-11-12 and the fourth by its read of 2026-11-21 (a straight
  line or an average mispricing the margin), which also narrows the second (proportional scaling, a form carried
  past its range and a projection that holds an intermediate fixed are now cards) and the sixth (a check run on the
  data used to choose is a card). So the deciding lesson comes from an assumption no card names, from a check of
  another kind, and from the open dimensions (conservation, changing structure, non-additive quantities, position on
  a network, hidden state, a recording algorithm whose inversion is not a gross-up; `stumping` Part 1c).
- **Seven approvals on file decide on the observation process, and our send-backs for difficulty decided on
  mechanisms of the world** (`stumping` Part 1d): our four below and the three approved sheets of 2026-11-14 all turn
  on how the record came to hold what it holds, while task1 v5, task13 v5, task22 v2 and task25's first cut turned on
  a response, a signature, a loss term or a penalty that the rows either carried (modelled on sight) or did not
  (unforced at audit, then filed into a rule). An open member is opened by an observation-process judgment; the
  problem may sit in plain sight, because the work is the estimator (one approved run named the selection and filed
  nothing); the most rigorous standard design the pack affords lands across the line; a referee slice the target
  does not reach rules between estimators, which is what forces the call while the method stays open; each stump is
  worth three times the honest family's spread; the estimated quantities carry the rubric's weight. The three sheets
  are on file as skeletons (`review:*`) and are never reskinned. The read of 2026-11-21 closes the commonest
  observation-process corrections as deciding lessons (a completeness gross-up from an independent source, a bias
  calibrated on checked cases, a basis restated, the treatment changing who is recorded), so an observation-process
  stump is open only where its estimator is more than one of those: several recording effects tangled with each
  other and with who the units are, a recording algorithm to invert, a state the record never held, sources assigned
  part by part with no checked sample that hands over the factor.
- **The four approved builds** (task6 v7; task457, shipped as task14 architecture 1; task2 v6; task14 v3) share an
  anatomy, never a skeleton: the answer is a quantity the primary record does not hold; several partial instruments
  see it, each with its own blind spot, and the work is assigning each part of the estimand to the one that sees it
  (the runs took the closest-looking or most complete one); the target reaches units or periods no instrument covers;
  every factor across the data, the shortcuts on different wrong answers, the margin held against every variant;
  task457 was approved once its prompt opened on why the answer has to be an estimate. No chain of theirs is copied.
  Two of the four decide on lessons the page has since closed (task2 v6's transport; task14 v3's rises a register
  sees only by choice, which the read of 2026-11-21 lists among its accepted examples): approved before the cards,
  refused as a draw today.
- **A landed scaffold is never re-pointed** (task4 architectures 6 to 10, task10 architectures 4 to 7, all landed): a
  re-root changes the deciding lessons and the decision form, and the skeleton guard checks the slot's lineage.
- **The field's whole textbook chain is one reflex when the pack ships its ingredients** (task22 arch 1, task7 arch 12):
  a step priced as a stump on another build's loss is earned once the pack carries the inputs of the field's standard
  method (a survey, a published draw per unit, a trial, a GIS), however many steps the method has; and a golden that
  uses a constant only the generator knows (task7's 58 F) is a fork the platform's auditor finds
  (`stumping/references/stump-screen.md` tests 2, 10 and 11, its measured-dead table, `determinism-check` §1).
- **Forcing has two sides** (six returns on determinism or forcing): every defensible rival on the golden's side, the
  shortcuts across the line, and the call holding when each fitted input moves by its spread (`effort.json` forcing).
- **The opponent is the runs' recorded routes, never our hurried one** (task3 arch 8, 2026-11-21: both runs filed all
  seven classes against a paper pair of 26.7, on routes no lattice key held). The runs fit any correction a shipped
  file lets them check (a storage account closing a bucket loss, radar pixel pairs reading a ratio off, a slice of
  gauges scoring the whole chain), apply every correction at full strength with the uncertainty integrated, and
  calibrate end to end on any slice that observes the target; they lose where nothing checks the correction and they
  keep the signal as a sensitivity, cut at a threshold or decline (the approved sheets, examples 16 and 17). So
  `core.py` implements four run routes (generous, calibrated, hedge, cut-off), each filing a wrong call and priced at
  50 or under; the misses fall on both sides of a line; no stump has a validation handle; a referee is a calibration
  set first, so the call is forced by a falsification check on the members' own records unless the calibrated route
  on the referee files wrong; and the estimand is a forward window, never the record's own mean (`corelib.py`
  `run_routes`, `precut.py` `Run routes:`, `Validation handles:` and `Forward window:`, `stump-screen.md` tests 16
  and 18 to 20). The stump the runs lose is a parameter they must set, whose default (a pooled value, today's level,
  a literature constant, the same as another group, independence, a pro-rata split, the face value) the world makes
  false across every unit, identified only through a covariate built from another file or an internal check.

## Skill routing (binding)

Invoke the skill before the work, whatever the request's wording; if two apply, both, in pipeline order.

| Doing this | Invoke first |
|---|---|
| Starting or re-rooting a build, or asking whether a build repeats an earlier one | `fingerprint` |
| The domain fit, the answer's shape, the main recommendation, `prompt.txt` | `guide-to-prompt` |
| The results chain, the one-thing screen, the effort test, the hidden factor record, re-rooting | `stumping` |
| The asks, the rubric arithmetic, how results become graded criteria | `supplemental-stumping` |
| Pinning each result (bands, rivals, forks), or checking a build against the judge's gates | `determinism-check` |
| Building or repairing the pack under `target/` | `dataset-generation` |
| Writing or editing `submission.md` or any golden deliverable | `submission-writeup` |
| Making a golden read as a real work product (after its figures are asserted) | `golden-realism` |
| Declaring a pack ready, or recording a fix that came back from review | `reduce-house-fixes` |
| Checking a cut pack and prompt for anything that hands over a result or a method | `leak-check` |
| Taking a task to the platform, resuming a build, reading the runs, repairing a returned one | `build-pipeline` |

## Commands and effort

| Command | What it does | Effort |
|---|---|---|
| `/draw taskNN <domain> <analysis type>` | the brain alone, in the main thread: the core proved in `generator/core.py`, the card, the note to `precut.py` exit 0 with its Build brief; also re-draws a returned build's core | Fable 5.2, xhigh |
| `/build taskNN <domain> <analysis type>` | spawns the `stump-architect` for the core unless `/draw` did it, then executes the brief: build, leak reader and judge, ready for the platform; resumes from `pipeline.json` | Opus 5.5, high |
| `/triage-runs taskNN` | records both run scores, maps each run's losses result by result, routes the build, drafts the `Valid Stump?` field | medium |
| `/fix-determinism taskNN <finding>` | closes a fork on a result (a run's defensible alternative or a judge finding) | Opus 5.5, high |
| `/fix-rubric taskNN` | the losses were analytical but the average is 60 or more: reworks the asks so more results are graded | Opus 5.5, high |
| `/approve taskNN` | the mechanical sign-off before upload (heart, surface, precut, effort, leak verdict) | medium |
| `/leak-check taskNN` | `leak.py` plus one isolated reader | medium |

**The brain and the body are different models** (`build-pipeline`, Effort per role). The `stump-architect` (Fable
5.2 at xhigh) designs the core: the three or four independent judgments that stump the review's strongest run,
proved in `generator/core.py` and handed over as the note's `## Stump core` and `## Build brief`. It works by
`stumping/references/core-method.md` (level 5 as an exposure matrix of members against judgments, five questions
asked of every factor of each member's figure, three stumps kept on different axes) and its core.py ends on
`stumping/corelib.py`, which grades the core level 5, level 4 or fail, prices every route on the rubric, and which
`precut.py` runs. The build (Opus
5.5 at high) executes that brief and moves nothing in it; whatever touches the core goes back to the architect. The
`determinism-judge` runs on Opus 5.5 at high (it stands in for the review's audit), the leak reader on Sonnet at
medium, the run triage on Opus at medium, each set in `.claude/agents/` or on the `Agent` call. Fable 5.2 is the
design's model and no other role's: no judge, reader or triage thread is spawned on it. No isolated thread runs on
the model's own initiative; the commands above license the ones they name.

## The workflow

```
0 INTAKE   the assigned domain (one of the 21 subdomains) and analysis type (one of the nine); status.py new for
           the number                                                         pipeline.json DRAWING, doctrine throughout
1 DRAW     guard.py recent, coverage and mechanisms; the strategy atlas; the weight and answer shape not leaned on
           recently; the stump screen on paper (five or more candidate traps through its twenty tests, the three
           strongest that open different members kept, stumping/references/stump-screen.md) and the core proved
           in generator/core.py (stumping Part 1d); the card (answer_shape, weight,
           chain_signature) through guard.py check, then register             COMMIT "DRAWN (taskNN)"
2 DESIGN   the Stump core and the Build brief, the results chain, the hidden factor record, the effort test on
           paper, the data provenance, the template check, fork and closure tables, the asks, prompt.txt
           gate: precut.py exit 0 and core.py exit 0         (stages 0 to 2: the stump-architect, Fable 5.2 xhigh)
3 BUILD    generator around core.py (simulating the real process), pack, goldens, effort.json, submission.md
           (stages 3 to 5: the build thread, Opus 5.5 high, executing the Build brief)
           gate: generator checks, verify, two byte-identical builds, effort.py, figures_check.py, the realism
           sweep, golden-realism, reduce-house-fixes, leak.py, guard.py surface and heart (or python3 gates.py taskNN)
4 CHECK    the leak reader and the determinism judge (determinism only) spawned together in the background;
           every finding fixed in the generator in one pass; re-judged once only when a fix moved a graded figure,
           the prompt or the pack
5 READY    every gate re-run on the final cut; target.zip and the golden ZIP from the final rebuild; the author
           rewrites the prompt for voice, uploads it and target.zip           COMMIT "READY (taskNN): <call>"
6 RUNS     /triage-runs records both scores, maps the losses result by result and routes (submit,
           /fix-determinism, /fix-rubric, a surface trigger rebuilt as analysis, or redesign from 2)
7 SUBMIT   triage SUBMIT, the Reward block and the Valid Stump? field filled (where each missed decisive step
           fails, why it is fair, why it takes reasoning), submitted          COMMIT "SUBMITTED (taskNN): ..."
           the review result later: APPROVED or RETURNED                      COMMIT "APPROVED" / "RETURNED"
```

A build has two hands. The architect designs the core and proves it in numbers before any pack exists; the build
thread executes the brief, and a repair of the pack is done where the context already is, while a repair of the
core goes back to the architect. `python3 .claude/skills/build-pipeline/gates.py taskNN` runs every free
gate in one pass and prints one summary; run it instead of the scripts one by one.

**Speed comes from killing weak ideas on paper** (`build-pipeline`, Speed): the stump screen before the card, the
core proved in `generator/core.py` before the generator is written, one review pass by the reader and the judge
together, and no gate or agent re-run that a fix did not touch.

**The fingerprint guard is mandatory and free.** The card is registered the moment the draw is fixed. The 20 Project
Mark cards under `fingerprint/cards/` (filed as `markNN.json`, Mark's taskNN: 110, 111, 114, 115, 117, 119, 120, 124,
126, 128, 132, 135, 162, 169, 175, 179, 182, 196, 253 and 258) and their shipped-ledger rows are the
already-submitted baseline: a Sulfur build that repeats a Mark build's driver, shell or data structure is a duplicate.
Personas come from `guard.py names`, never typed. **Every card carries the client's skeleton** (decision form,
deciding lessons, detection, resolving moves, file roles, answer pattern): `fingerprint/skeleton.py`, run inside
`guard.py check`, refuses a near copy, a templated build or a variant of anything on file, of the slot's own lineage
or of any task the client has shown us (`fingerprint/corpus/client_skeletons.json`: the templating page's pairs, the
17 depth-scale tasks, the 17 examples, the three approved review sheets of 2026-11-14), and a deciding lesson the
dataset already teaches twice; the client swaps the nouns and counts, so a new setting never clears it.

**Determinism is a construction, not an inspection**: invoke `determinism-check` while the results chain and the
generator are written. Its judge is spawned at stage 4, by `/fix-determinism`, or when the author asks.

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
(`mark110` to `mark258`), so the two never collide. The platform's tier sets how many run at once (one at Tier 1,
three at Tier 2, six at Tier 3).

## How a build is worked

1. **Deliver before bookkeeping.** Finish and hand over what was asked; only then skill lessons, house fixes or
   memory.
2. **One design note per build, with an append-only `## Tried and rejected` section** (that exact heading). When an
   approach dies, add one line: what was tried and why it died, written when it is abandoned. The note's shape is
   `stumping/references/design-note-template.md`.
3. **No backups, snapshots or versioned design docs** in a task folder. Allowed beside the note: `pipeline.json`,
   `metadata.json` (outside `target/`), `generator/figures.json`, `generator/effort.json`, the leak, determinism and
   triage reports, `runs/`. A build that cannot be rebuilt from its generator has a broken generator.
4. **Builds cut under the retired single-deep-step design** (task1 to task14) are not re-shipped as they stand:
   `precut.py` marks them, and each is re-rooted to a results chain before any upload or re-ship.

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
- **The prompt: write it correctly, the author rewrites it for voice.** The project lead returns prompts that spell
  out the method, name the attached files, carry context the files already hold, or say who is asking, and runs a
  three-strike policy on LLM-sounding prompts (warning, then one task a week, then offboarding). So the draft is
  short and direct (one plain paragraph under 1,000 characters, question first, no rounding instruction), and it is
  correct and leak-free: it pins the question, what each result is (population, outcome, window, unit), the
  deliverables by type ("a spreadsheet and a few slides"), never dictates rounding (each graded figure's precision
  and band are stated in the answer blocks), and never names the method, the
  comparison, the adjustment or a step, never warns, never names an attached file ("see the attached ZIP" or
  nothing) and never says who is asking. The author always rewrites it in their own words; the rewrite comes back
  through `voice-check.py --rewrite` (leaks fail, voice only warns) and `leak.py` (`guide-to-prompt`, `leak-check`).

## Current spec

**Determinism is literal and per result.** The judge executes the shipped text word for word. Every constant the
golden shares with the world is filed or measured (the note's `## Pinning list`), and every modelled transport is
rebuilt across a variant battery of twelve or more that files one answer, before anything is priced. Each result's
estimand (population, including members not yet observed, outcome, window, unit, comparison) is filed so its literal
execution is the golden; the method stays open. Every result is pinned by the data or a stated convention, with a
band where reasonable methods differ: the rivals are run, not argued, and every defensible rival lands inside the
band or is ruled out by named data. Every term and convention has a row in the design note's fork table, closed by
a sentence or `same call`, asserted in `checks.py`; `precut.py` refuses an open one. The grader compares every
figure to the golden, so a later result built on a wrong earlier figure is wrong unless the result names an input
of its own; the chain is designed so a hygiene slip costs nothing and a lost stump costs every figure downstream
of it, which is most of them (`supplemental-stumping` Part 1).

**The next-level contract** (every card registered from `skeleton.RULE_FROM`, 2026-11-11; a WARN for builds filed
before it): the card's skeleton clears `skeleton.py check`; the design note carries `## Frontier check` (`Precedents:`,
`Shallow path checks:`, `Assumption made false:`, `Forcing:`, `Noun swap:`); `effort.json` cites a precedent for every
careful-column loss and records `forcing` on both sides; `precut.py` and `effort.py` refuse any of them missing.

**Every chain is bespoke.** The results come from the dataset's own structure, and the design note says why in one
data-native sentence. The client's examples, strategies and worked illustration are direction, never templates:
copying their steps onto a new topic is a reskin.

**Data** (`dataset-generation`): generated data is the house route and is fine when it is business-realistic and
behaves like the real thing throughout: the generator simulates the real process (the organisation's systems, the
physics, the people), so the files carry many genuine patterns and noise, several genuine problems of different
kinds produced by the process, and benign oddities that decide nothing; no effect is added only where it decides a
result. Public data used as is is welcome where it fits, with its source and license. Either way: 10 or more real,
usable files (system files do not count), in 2 or more file categories (spreadsheet, database, text, image, code;
archives do not count but their contents do); real breadth where it is natural (many units, series, runs or files,
so deciding what to look at is work); at least 2 large, messy files, both CSV: one of 20,000 rows or more, and one
that runs 10 to 20 printed pages or more; at least 2 distractors that look relevant and are unused, never labelled
in a file name or anywhere inside the ZIP; cross-file reasoning required; source, pull date and license recorded in
`metadata.json` (outside the ZIP); nothing LLM generated or padded, and no file that reveals how the task was built
or exists only to carry a trap.

**Deliverables**: a structured set of results in one of the fourteen answer shapes, with a recommendation on top
where the decision needs one; one to three files in formats a real analyst would produce for the reader who will use
them (not `analysis_report.pdf` by default); a visual where it makes the results read at a glance. **The house set
is a CSV, a workbook and at most a deck.** A written document (a memo, a note or a report, as Word, PDF or
Markdown) is the rare exception, asked for only where the decision's reader could not use a workbook or a deck,
with the reason in the note; the call sits on the workbook's first sheet or the deck's first slide
(`guide-to-prompt` section 2; `voice-check.py` and `guard.py check` warn on one).

**Asks**: the results, asked for, as **one to four hard, multi-faceted supplementary asks** (the page of 11/20:
"rather than a long list of easy ones"); each resolves to several gradable answers (many rows, periods, segments or
calculations), its unit inside the asking sentence and no rounding instruction (the answer blocks state each
figure's precision, with its band where reasonable methods differ). The prompt asks for what the estimates are used
for (the figure for every member, carried a step further, the rejected option on the same footing) and for each
decisive step's own quantity in the decision's words (the hours a case will take under the new agreement, never
the adjustment that gives them), so every critical component is gradable in a requested deliverable; it never asks
for a count, a total or a table every run rebuilds, so a run that lost a stump gets every ask downstream of it
wrong (`supplemental-stumping`).

**Answer blocks** (`submission-writeup`): Final Recommendation (one or two sentences, first, naming what it
rejects); Supplementary Questions (one numbered entry per ask, one to four, each entry carrying its figures, and
each requested file's look in one line); Critical Components (the decisive steps, two to five, one per stump: each
line is that step's answer as a figure with its unit and band and no method clause, the figure sits in a requested
deliverable, and each falls with its own stump alone); Step-by-Step (a short numbered path from the raw files
through each result, showing where the hurried analysis goes wrong, and the only block that carries the counts and
bases every route reaches), closing on why no other conclusion survives. **The golden ZIP holds exactly the files
the prompt requests**, one set of numbers everywhere, nothing LLM-looking (`golden-realism`).

**Rubric**: generated from the prompt and the answer blocks; recommendation and critical components carry the most
weight, then the asks, then a small share for instruction-following. Edit a criterion only when it is clearly wrong
or missing, then re-run the evaluation.

**Domains and analysis types**: the client's seven major domains and 21 subdomains
(`guide-to-prompt/references/domains/`, client text in `guidelines/client/domains.txt`); one subdomain, one
analysis type, one decision. **The nine analysis types**, assigned by the client: Descriptive & Distribution
Analysis; Comparative Analysis & Explanation; Anomaly Detection & Diagnostics; Root-Cause Analysis; Experiment &
Causal Analysis (over-represented across the program, so give the others a turn); Forecasting & Predictive Modeling;
Opportunity Sizing & Decision Support; Data Extraction & Conformation (ETL / Pipeline Build); Data Quality,
Monitoring & Alerting. The client's most wanted: root cause and debugging of complex systems (training runs,
services, pipelines, fleets), forecasting and prediction, and comparing things and explaining the difference. Which
task types serve Comparative Analysis & Explanation is a house mapping in `vocab.json`, not client taxonomy.

**Gate G**: no shipped artifact ranks the candidates on the decision question and gets it wrong. The difficulty
survives deleting every wrong number from the pack. **The call is forward facing by default**: a quantity about a
window not yet closed; a retrospective call is legal with its reason in the design note.
