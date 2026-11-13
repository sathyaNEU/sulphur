# The design note, section by section

`precut.py` reads these headings and labels. The order below is the order the build writes them; a section is
written when its stage reaches it, and the gate runs at the end of stage 2 and again on the final cut. Write every
line in the build's own nouns. The angle-bracket text says what goes there and is never left in the note.

```
# taskNN: <the decision in the organisation's words>

## Draw

Subdomain: <the client's subdomain, exact wording>
Analysis type: <one of the nine: Descriptive & Distribution, Comparative Analysis & Explanation, Anomaly Detection
  & Diagnostics, Root-Cause, Experiment & Causal, Forecasting & Predictive Modeling, Opportunity Sizing & Decision
  Support, Data Extraction & Conformation, Data Quality, Monitoring & Alerting>
Answer shape: <one of the fourteen, e.g. a bridge that reconciles two totals; a flagged set with the evidence and
  the false-alarm rate>
Weight: <where most of the work sits: assembly, measurement, triage, investigation, modeling, validation,
  attribution, synthesis, allocation, a hard-to-measure quantity, metric or rule design; and why it differs from
  the last three builds>
Data-native sentence: <why this dataset's own structure makes the work hard, in one sentence>
People: <from guard.py names>

## Stump screen

Written at the draw, before the card is registered and before any code (`references/stump-screen.md`). Three to five
candidate traps, each through the eleven tests (1 off the closed page, 2 not a reflex, 3 nothing filed, 4 clean data,
5 two records, 6 the waved-through assumption with its precedent, 7 a plausible shallower story, 8 across the data,
9 worth the call against the variant battery, 10 the run's alternative ruled out by named data, 11 the golden can
measure it); the three strongest independent ones kept.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| <the world's process, one line> | <N02, L07, ...> | <file and grain> | none | kept |

## Deep reasoning

Task type: <the domain's task type from the taxonomy that serves the analysis type>
Domain test: <the field's own quantities the results are; what the field's analyst does with them>
Swap: <the call rewritten with another field's nouns, and what stops making sense>
Where the weight sits: <the heaviest result and why the work there is long, not clever>
Layer 1: <each piece of mess and the real process that produces it; none decides a result on its own>
Not one thing: <the strongest single piece of the task, and the results a run that nails it still has to earn>
One-fact test: <the most useful single sentence a reviewer could give a run, and the results it rescues (agrees
  with the Effort test's Largest single hint)>
Not semantics: <why every field, unit and clause read correctly still leaves each hurried result wrong>
Not rule application: <which results no filed procedure performs, and what is left to judge once every filed rule
  is applied>
Estimand: <the filed sentences fixing each result's population, outcome, window, unit and comparison, and where>
No decoy: <nothing written to carry a wrong answer: no memo or draft whose number is simply wrong, no document
  arguing the wrong answer, no copied block; an incumbent figure that reproduces exactly by its own stated method and
  answers a shallower quantity is named here with the ask that prices it on the golden's footing (stumping Part 1b)>
No replay: <no result re-derives a published figure; no stated number is simply wrong>
Pinned: <each result's rivals, run on the clean truth, landing inside its band or ruled out by named data>
Run forecast: <where each run is expected to lose points: the result ids and the class at each (method shortcut,
  unfinished chain, first story, narrow look, dismissed own evidence, self-confirming check)>
Strategy label: <the strategy's label in references/sulfur-strategies.md>
Depth level: <4 or 5 on the client's depth scale (guidelines/client/depth-scale-2026-11-09.md): the independent
  judgments counted, and the different wrong answers the shortcuts land on>
Lesson: <what a model learns by getting every result right, and why no build on file already teaches it>

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | <the result, a figure, set or table> | <one of the fourteen areas> | <the data or the stated convention> | <exact, or the range reasonable methods span> | <deep class: what a careful run in a hurry files instead> | - | <Component 1, Ask 3, Recommendation> |

Carry-forward: <how a later result is graded on the solver's own earlier figure, so one slip costs only the
results that depend on it>

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| <each pattern the runs have to find> | <real (public, as is) or constructed> | <yes or no, and where else it shows> | <one look, a targeted query, or modelling> | <routine, or modelling> | <keep, or rebuilt as ...> |

(or one line, `No hidden factor: <why nothing in the task has to be found>`)

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 <name> | Missed | Right | Right |
| Roughly | 1 of 6 | 3 of 6 | 6 of 6 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: <the sentence>; rescues N of M results
Pair estimate: <the careful but hurried pass's rubric score, 50 or under>

## Stump factorial

Reflex route: <every move a run makes unprompted or the files spell out set right, every stump hurried; the answer it
  files, which misses the call; this route is the careful but hurried pass>

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| J1 <the judgment> | stump | <what the run does instead> | <loss or named_assumption ids> | <the answer, which moves the call> | <the answer, still not the golden; results rescued> | <yes or no> |
| J4 <a move runs make> | reflex | <...> | <reflex ids or the filed document> | <same call, or the answer> | - | - |

Level: <4 at two necessary stumps none sufficient, 5 at three on two or more distinct wrong answers>

## Open members

One row per member of the call (a plan, a rule, a site, a list item, a package boundary): where the golden puts it
against its line, how far the honest family moves it, what the reflex route and the direct route file for it, and the
stump that brings it back (`../SKILL.md` Part 3.4). A member both routes file right is forced; write `forced` in its
last column. Two open members opened by different stumps is level 4, three is level 5.

| Member | Golden margin | Family spread | Reflex route | Direct route | Opened by |
|---|---|---|---|---|---|
| <member> | <its distance to its line> | <the honest family's widest move> | <what the reflex route files: wrong, and how> | <what the direct evidence read raw files: wrong, and how> | <the stump id, or forced> |

Direct route: <for each member, the pack's most direct evidence read at face value (the documented cases counted, the
confirming file raw, the reference cases' signature copied, the incumbent's transfer), the generator's route that runs
it, and why it lands wrong>

## Data provenance

Source: <generated by the generator from a simulated process, or public with its URL>
Behaves like the real thing: <the process simulated and the published behaviour it matches>
Genuine patterns: (1) <seasonality, trend, scale effects ...> (2) <...> (3) <...>
Problems by process: <each data problem and the real-world process step that produced it>
License: <public data only>
Used as is: <public data only: what was changed, if anything, and why it changes no result>
Breadth: <how many files, units, series or runs, and why choosing what to look at is work>

## Template check

Chain signature: <the areas of the results chain in order>
Question form: <how the prompt asks: what, which, how much, when, why ...>
Nearest build: <the build on file nearest in chain, shape and weight, and what differs>

## Frontier check

Precedents: <each result the careful but hurried pass loses, with the references/precedents.json ids (loss or
  named_assumption) behind it; the same ids sit on the result in generator/effort.json; a result with none is Right>
Shallow path checks: <for each priced result, the checks the hurried route passes (its back-test, placebo, nearby
  variants, the incumbent figure it reproduces) and the check of another kind that refutes it, with the second file
  at another grain that check needs>
Assumption made false: <the assumption a run lists and waves through (scaling, persistence, schedules, a pooled rate
  on a selected subset, a smooth response), why this world's process makes it false, and the file that tests it>
Forcing: <the line; the golden family's spread and its nearest distance to the line; the shortcuts' distances on the
  other side; each fitted input moved by its defensible spread (20 per cent when none is known) with the call holding>
Noun swap: <the nearest task on file or in the client's library by skeleton.py check, its nouns swapped into this
  one, and the elements that carry across unchanged (decision form, lessons, detection, moves, file roles, answer
  pattern); severity none>
Closed strategies: <the lesson the call turns on, the client's closed card nearest it (skeleton.py closed) and how its
  mechanism or fix differs; each closed lesson the chain keeps as a supporting step, the effort.json route that
  applies it alone and the answer that route files, the golden call standing>

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | ... | ... | ... | <a filed sentence, `same call`, or named data> |

## Pinning list

Every constant the golden's estimator uses that the world also holds (determinism-check §1): the golden may not know
what the generator knows.

| Constant | Golden value | Home |
|---|---|---|
| <a base temperature, threshold, exponent, share, draw per unit, time constant> | <value> | <the shipped file and where in it, or the estimator family and its measured spread> |

Variant battery: <how many variants of every modelled transport were run (each convention at the values the field
uses, each alternative source, each component in and out, pooled against per group) and that they file one answer>

## Closure table

| Axis | Closure |
|---|---|
| 1 | ... |   (22 rows, determinism-check)

## Literal reader

<the shipped sentences a reader executes word for word, and the result each produces>

## Prompt contract

<what a voice rewrite may not drop or change; what it must never add>

## Tried and rejected

- <one line per abandoned approach: what was tried and why it died>
```

## What the gate refuses

- Fewer than four results, or results drawn from fewer than three of the fourteen areas.
- A result with no band, no pin, no answer block, or a hurried failure that is not one of the six deep classes (a
  result lost to a plant, a reading or a procedure is a surface stump).
- A hidden factor that is constructed and sits only in the deciding units, or constructed, found in one look and
  fixed by one routine step.
- An effort test where the quick pass earns more than half of the results, where more care does not earn strictly
  more, where the thorough pass misses a result, where one sentence rescues more than half, or where the pair
  estimate is over 50. Once `generator/effort.json` exists the table must agree with `effort.py`.
- Generated data that does not say how it behaves like the real thing, or names fewer than three genuine patterns.
- The same chain of areas in the same order with the same answer shape as a build on file.
- For a card registered from `skeleton.RULE_FROM` on (a WARN before it): a missing `## Frontier check` label, a
  precedent id that is unknown or a reflex, or a skeleton BLOCK (severity 1 to 3 against a build on file, a client
  task or the slot's own lineage; the deciding lesson already taught twice; more than half the chain's lessons taught
  or closed; a decision form on four live builds). From `skeleton.CLOSED_FROM` on: a missing `Closed strategies:`
  line, a deciding lesson on the client's closed page, or a chain of closed lessons only.
- In `effort.py`: a careful-column loss with no precedent (graded Right), a cited pair estimate over 50, a forcing
  block missing, a golden-family variant across the line, a shortcut on the golden's side, or a perturbation that
  moves the call.
