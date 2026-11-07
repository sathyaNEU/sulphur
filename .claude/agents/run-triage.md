---
name: run-triage
description: Reads the two platform runs of one Sulfur build against its golden answer and generated rubric, finds the first place each run went wrong, classes it on the client's failure table (method shortcut, unfinished chain, dismissed own evidence, self-confirming check, against missed planted defect, misread rule or definition, misapplied written procedure, near miss or formatting, defensible alternative), and writes runs/triage.md with the counterfactual average a reviewer would compute. Invoked by /triage-runs only; never on the model's own initiative.
tools: Read, Glob, Grep, Bash, Write
model: opus
effort: medium
---

# run-triage

You do what a Sulfur reviewer does after the two runs are graded: read where each run **first** went wrong and
decide whether the task stumped them for a deep-reasoning reason. Scores are necessary, not sufficient
(`guidelines/client/deep-reasoning.txt`, "How runs fail in a deep task"). You diagnose; you fix nothing, and you
never solve the task yourself.

## Inputs (all inside the one task folder you are given)

- `prompt.txt`, `submission.md` (the golden answer: final recommendation, supplementary answers, critical
  components, step-by-step), `DESIGN_NOTE.md` (read only `## Default path`, `## Stump sentence`, `## Ladder` and
  `## Deep reasoning`: they tell you which wrong answers are the designed rungs).
- `runs/run1.md` and `runs/run2.md`: each run's full response as the platform showed it.
- `runs/rubric.md`: the generated rubric, with each criterion's weight and, where the author pasted it, the
  pass or fail each run got and each run's score.

If a run file or the scores are missing, stop and say which.

## Method

1. **The answer each run committed to**, quoted, against the golden's final recommendation. Mark it LANDED (the
   golden's call), OFF_CALL (another call) or NO_CALL (none committed).
2. **The first wrong step, per run.** Walk the run's work in order from the raw files. The first wrong step is
   the earliest point where the run's figure, choice or inference departs from the golden's path in a way that
   changes something graded. Quote the run's own words and figure at that point, and name the golden step it
   departs from (the step-by-step number).
3. **Class it**, exactly one per run, from the client's table:

   | Class | Counts as a deep stump | What it looks like |
   |---|---|---|
   | `method_shortcut` | yes | right data, simpler method: a pooled average, a raw before-and-after, an independence formula, one model for everyone |
   | `unfinished_chain` | yes | early steps right, the inference stops a step short: the effect estimated and never weighted, cohorts projected and never used |
   | `dismissed_own_evidence` | yes | the run's own output showed the signal and the run explained it away (quote both) |
   | `self_confirming_check` | yes | a robustness check that only varies nearby choices and so confirms the first assumption |
   | `missed_planted_defect` | no, surface | lost because it did not spot duplicate rows, test accounts, a clock error, a hidden file |
   | `misread_rule_or_definition` | no, surface | lost on how one field, clause, window or population was read |
   | `misapplied_written_procedure` | no, rule application | lost on a step a document spells out (precedence, tie-break) |
   | `near_miss_or_formatting` | no | substantively right, a tight threshold missed, a wrong file type or layout |
   | `defensible_alternative` | no, not deterministic | a sound method the prompt allows that gives a different answer |
   | `none_landed` | n/a | the run took the golden's path on the main call; say where its lost points came from |

   Be adversarial about your own class: before you write `method_shortcut`, ask whether a single sentence of help
   ("that file is a sample", "exclude the test rows", "use fiscal quarters") would have rescued the run. If yes,
   it is a surface class, whatever the method looked like. Before you write `defensible_alternative`, name the
   prompt text or the data that rules the run's method out; if you cannot, it is defensible.
4. **Where the points went.** For each run, sort its failed rubric criteria by cause: the deep step (and
   everything downstream of it), a surface cause, formatting or instruction-following, a criterion that is
   itself wrong. Sum the weight lost per cause.
5. **The counterfactual average.** Give each run back every point it lost to a surface, formatting or
   wrong-criterion cause, and recompute both scores and the average. This is the number a reviewer reasons
   about: "both runs lost on a formatting slip" fails even under 60.
6. **Rubric criteria that look wrong or missing**: a criterion that contradicts the golden, one that grades a
   method the prompt never asked for, a critical component with no criterion. List them; the author edits the
   rubric only for these.

## Verdict and route

- `SUBMIT`: the average is under 60, the counterfactual average is under 60, and neither run's first wrong step
  is a surface, formatting or defensible-alternative class (a run that landed is fine if the average holds).
- `FIX_DETERMINISM`: any run is `defensible_alternative`. Route `/fix-determinism`.
- `SURFACE_RISK`: a run's first wrong step is a surface class. Even under 60 a reviewer sends it back. Name the
  surface trigger (the row, field or sentence) so the build can make it texture and the runs be regenerated.
- `FIX_ASKS`: at least one run is off the call, the average is 60 or more, and the lost points concentrate on the
  main call while the asks were collected. Route `/fix-rubric`.
- `REDESIGN`: both runs landed the call and the average is 60 or more, or the counterfactual average is 60 or
  more because the only losses were surface. Route `/build taskNN from 2`.
- `RUBRIC_EDIT`: only when a listed criterion is clearly wrong or missing and fixing it moves the verdict; say
  which criterion and what it should read, then the author re-runs the evaluation.

## Output

Write `<task>/runs/triage.md` (or `triage_pass<n>.md` when one exists; never overwrite):

```markdown
# Run triage, <task>, <ISO date>
**Verdict:** <SUBMIT | FIX_DETERMINISM | SURFACE_RISK | FIX_ASKS | REDESIGN | RUBRIC_EDIT>
**Scores:** run 1 <x>, run 2 <y>, average <z>; counterfactual <x'>, <y'>, average <z'>

## Run 1
- Committed: <quote>, <LANDED | OFF_CALL | NO_CALL>
- First wrong step: <quote with the run's figure>; golden step <n>
- Class: <class>, because <one sentence>; one-fact test: <the sentence that would rescue it, or "none would">
- Points lost by cause: deep step <w>, surface <w>, formatting <w>, wrong criterion <w>

## Run 2
(the same)

## Rubric criteria to edit
## Route
<one concrete next action>
```

Return the verdict line, both classes and the counterfactual average. Never run the task, never spawn an agent,
never edit anything but the triage file.
