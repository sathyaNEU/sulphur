---
name: submission-writeup
description: Draft or revise submission.md, the Sulfur answer blocks the author pastes into the platform, and every golden deliverable in the golden ZIP. Invoke whenever a submission.md is being written, rewritten, extended or reviewed for a task folder, including when the request just says "write the submission", "draft the answer", "do the golden for taskNN", or when a review says a block is thin. Carries the four platform blocks in order (Final Recommendation naming what it rejects, Supplementary Questions as one numbered entry per ask, one to four, Critical Components as the decisive steps' answers, one per stump, each the answer and never the method, independent and in a requested deliverable, Step-by-Step walking every result and showing the hurried analysis it rejects, closing on why no other conclusion survives), the answer to the form's stump question, How is each model stumped (where and how each model goes wrong, why the stump is fair, why it takes rigour), written from the runs and kept first after the Final Recommendation, the rule that every figure is emitted by the generator and recomputes, and the golden ZIP rules (exactly the files the prompt requests, one set of numbers).
---

# Writing the answer blocks

`submission.md` holds the four blocks the author pastes into the platform's Final Recommendation, Supplementary
Questions, Updated Critical Components and Updated Step-by-Step fields, and once the runs are back the answer to
the form's stump question, directly after the Final Recommendation. The rubric is **generated** from the four blocks and
the prompt (`guidelines/client/overview.txt`, "How the rubric is built"): the recommendation and the critical
components carry the most weight, each supplementary answer becomes criteria, and instruction-following (files
present and named, rows and columns, length) takes a small share. So these blocks decide what the runs are graded
on: **the criteria are the results of the chain** (`stumping` 1.3), each one a result a run that skipped that
result's work gets wrong, and the results the runs lose sit in different blocks and different areas.

## Every figure recomputes, and is emitted, never typed

A determinism grader recomputes every figure in every block from the shipped files, and in Mark typed figures and
steps that read differently when followed literally were twelve of sixteen write-up findings in one window of judge
reports. Every extra figure is one more claim that can fail.

- The generator writes `<task>/generator/figures.json` (the call, each component, each step result, each
  supplementary answer, every result of the chain, and the careful but hurried pass's answer, as the blocks state
  them); the blocks are drafted from it,
  and this fails the build on any number absent from it:

```
python3 .claude/skills/determinism-check/figures_check.py taskNN
```

- **Cut incidental figures, never owed ones.** Every figure a component or an ask owes stays (each is a criterion).
  A figure that only shows working (a sub-count, a denominator) goes, except where the Step-by-Step needs it to show
  a result's hard move.
- **The Recommendation, the Supplementary Questions and the Critical Components state the core's graded figures and
  no others.** Each figure sentence there becomes a rubric criterion, and a criterion on a figure every route
  reaches (a joined count, a rebuilt total, a cleaned base, a reconciliation) is a point the run that missed the
  call still earns (`supplemental-stumping` Part 0). Those figures go in the Step-by-Step, where the reviewer
  reproduces them and no criterion is generated. For a build with a `generator/core.py`, the stated figures are
  its `figures` list.
- **Reproducible, not low-level.** Steps name the file and the method that produce each result; they do not walk
  arithmetic, restate the files' conventions or narrate cleaning. A convention needing a paragraph belongs pinned in
  a shipped file.
- **An estimate's clock time is never graded.** A changepoint, an onset or a peak moves by tens of minutes between
  sound methods (task6: the independent verifier's rolling median dated every December onset 15 to 55 minutes earlier
  than the golden's changepoint, with the same owner and the same order), and a run that names the right cause at
  another minute is then marked a near miss, a surface loss. So the answer blocks grade what the data force (the
  owner, the order of the rises, the side of a line) and state no clock time; a golden file may give an "about" time
  as the analyst's own dating. Run a second method's dating before any time goes near a block.

**Order:** build, `determinism-check`, this skill, `golden-realism`; never before the analysis is done.

## The blocks, in order

| # | Block (platform field) | Length |
|---|---|---|
| 0 | `## Tags` (not pasted; for the card and the domain field) | 2 to 3 lines |
| 1 | `## Final Recommendation` | 1 or 2 sentences, the deciding figure, what it rejects |
| after the runs | `## How is each model stumped?` (the form's stump question), directly after the Final Recommendation | a short paragraph per response, one on why the stump is fair, one on the rigour it takes |
| 2 | `## Supplementary Questions` | one numbered entry per ask (one to four), each entry its figure lines, grouped by file |
| 3 | `## Critical Components` | 2 to 5 one-liners, one per decisive step: its answer, no method |
| 4 | `## Step-by-Step` | about 6 to 10 numbered one-liners, then a short closing passage |

Nothing else goes in the file. The stump block is written from the runs, never before them, and it is the first
thing after the Final Recommendation, in the file and in the paste (below, "How is each model stumped?"). **Not written:** a format rationale, a justification block, a golden listing, key
assumptions, an AI disclaimer, a chat-style introduction, placeholders or TODOs.

**0. Tags.** The Sulfur major domain and subdomain in the client's exact wording (`guidelines/client/domains.txt`),
the task type, and the objective. No scenario recap.

> **Domain:** Biomedical and Health Sciences, Epidemiology & Public Health (disease surveillance).
> **Analytical objective:** Anomaly Detection & Diagnostics.

**1. Final Recommendation.** The call first, stated as a call, with no conditions and no "subject to"; a hold is a
call ("Fund none of the three programs this cycle"). Then the deciding figure and the margin, and **what it
rejects**: the answer the careful but hurried pass gives, named with its figure, and in a clause why it fails. Where
the answer is a set of results with no single call (a timeline, a bridge, a flagged set), the recommendation states
the headline result and the action it supports. This block answers the main recommendation only.

> **Send the winter outreach team to Harlow district, not Brenton.** Harlow's excess is 41 cases a week once the
> lab's testing growth is separated out; Brenton leads on the raw count (63) only because its testing doubled.

**2. Supplementary Questions.** One numbered entry per ask, in the prompt's order, and the prompt makes one to
four of them (the client's guidelines of 11/20: "1 to 4 hard, multi-faceted supplementary asks rather than a long
list of easy ones"). An entry opens on the ask in a few words and then gives its figures, one line per member,
period or option as `a.`, `b.`, `c.` under the number: each line is still one criterion, and the block no longer
reads as nineteen small questions. Entries are grouped by file under `### <file.ext>` (the golden file's own name;
the prompt asks for it by type), in the exact unit asked, at one precision with its band where reasonable methods
differ (the prompt dictates no rounding). Where an ask is a requested file, the answer
**describes how that file should look** in one line (its rows and the figures in it), then gives the figures. Every
described feature of a file or a chart (a column list, an ordering, a colour, where the visual sits) becomes a
one-point criterion every run earns, so the description is as short as the reader needs.
Each answer is graded at the main call's bar: it reproduces and is uniquely forced.

> ### district_excess.csv
> Twelve rows, one per district, sorted by excess cases a week, highest first; columns district, raw weekly
> cases, testing-adjusted excess (whole cases), 90 per cent interval (whole cases).
> 1. Excess cases a week in each district, with its 90 per cent interval:
>    a. Harlow 41 (interval 33 to 49).
>    b. Brenton 9 (interval 2 to 16).
>    c. ...

- **Concise is not summarised.** An ask owing a row-set gets every row as its own point, every column value named,
  in the deliverable's order.
- **Never a markdown table** (pipes break, wide tables wrap, odd tables are an LLM tell).
- A figure in two places has the same rounding in both; compute it once in code and carry it.

**3. Critical Components.** The decisive steps, and the correct answer to each (the client's guidelines of 11/20,
section 4: "list the two or more decisive, challenging steps and the correct answer to each. The rubric's heaviest
criteria are built from them"). 2 to 5 lines, **one per stump** (`generator/core.py`'s components), the figure in
bold at its rounding everywhere else. Four rules, each the page's own:

- **The answer, not the method.** "The restated 2023 baseline is USD 4.2M", not "restate the baseline". The line
  states the quantity in the deliverable's words, its figure, its unit and its band, and stops. No clause that says
  how it was reached or what it corrects ("once the lab's testing growth is separated out", "so the cold marks are
  the standard", "after the queue is taken out"): the method lives in the Step-by-Step, and a method clause in a
  component reads as the step and grades the wording.
- **Gradable.** The figure appears in a deliverable the prompt asks for, under a label that matches the line, and
  the prompt asks for that quantity (`supplemental-stumping` Part 1 rule 3). A component the prompt never asks for
  cannot be graded.
- **Independent.** "A model that gets one step wrong should still be able to earn the others." Each component is
  one stump's own figure: it falls when that stump is lost alone and is earned when any other is
  (`corelib.py`, `critical components independent`). A figure that falls with two stumps (a total, the call's own
  figure, a member's figure two corrections move) is an ask, never a component.
- **Lost by the hurried pass.** Never an assembly figure, a count or a base, never three restatements of one fit.
  If the hurried pass also gets it right, it is a free criterion and it goes to the Step-by-Step.

> 1. Brenton's testing-adjusted excess is **9 cases a week** (90 per cent interval **2 to 16**).
> 2. Harlow's cases with onset in the last three weeks, once every report is in, number **212** (band **198 to
>    226**).

**4. Step-by-Step.** A short numbered path from the raw files through each result to the recommendation and the
supplementary answers, one sentence per step: the method, the shipped file it reads, and the figure it produces. At
each result the hurried pass loses, the step makes the judgment explicit (which comparison, which model, which
adjustment, which check, and why the data rule out the simpler route) and **shows the hurried analysis it rejects**:
the hurried method's figure from `figures.json`, then the data that overturn it.

> 3. Ranked districts on raw weekly cases from `case_line_list.csv`: Brenton leads at 63 a week (the shallow read).
> 4. Joined `lab_testing_volumes.xlsx`: Brenton's tests doubled while positivity stayed flat, so its rise is
>    ascertainment, not incidence.

Then **a short closing passage** (two to four sentences): why no other conclusion survives the prompt, the files and
standard domain knowledge, naming each rival method and the fact that rules it out. **It carries the independence
of the decisive steps as figures**, from the core's lattice: the headline figure and the call with each step left
out alone, and where it matters in pairs ("with the testing correction and without the reporting completion the
call is Brenton at 63; with the completion and without the testing correction it is Carrow at 48"). The client's
hardest examples close this way, and it is what a reviewer checks "two or more decisive, independent steps"
against. Where one margin is thin, the passage says which and by how much.

- Cite where a convention is pinned ("per the surveillance protocol"), never restate it. A convention a competent
  analyst could reverse is an unpinned fork, fixed in a shipped file.
- Name only files the pack ships, by their pack names, or the grader finds missing input.
- Where a messy-data handling moves a graded figure, one step names the handling and the files it joins, so the
  grader can verify it; it never reads as the reason the call holds.
- End each step in a figure or finding, never an intention ("Analyzed the cohort data" is not a step).

## The golden ZIP

- **Exactly the files the prompt requests, in the requested formats, and nothing else.** If the prompt asks for a
  workbook and a CSV, the ZIP holds those two files. The files are a CSV, a workbook and at most a deck; a written
  document is the rare exception the prompt asks for with a reason (`guide-to-prompt` section 2), never added by the
  build. A missing file, an extra file or a mismatched format blocks
  confirmation on the platform. Name it `golden.zip` in the task folder, built from `golden/` by the generator.
- **One set of numbers everywhere**: the recommendation, every answer, the critical components and every table and
  chart in the golden files agree exactly, same rounding. A grader diffs them against each other.
- **Business-realistic is a gate**: once figures are frozen, run every golden through `golden-realism`.
- **The recommendation is unmissable** in the files, never inferred from output: one sentence on the workbook's
  first sheet or the deck's first slide, naming what it rejects.
- **A code deliverable prints the critical components' figures**, not only the answer.
- **Prefer code-produced artifacts** (a library chart, a script-written workbook, an emitted CSV); a chart in a text
  deliverable still comes from the script.
- **Nothing extra**: no answer to an ask the prompt did not make, no AI disclaimer, no placeholder.
- **Show the routes where the deliverable allows**: a short table in the golden of what each tempting shortcut gives
  beside the golden's figure (the client's reviewers praised "a routes sheet shows each shortcut's result, so the
  reasoning can be checked end to end"), so careful partial work earns visible credit; inside a requested file, never
  as an extra one.

## How is each model stumped?

The submission form asks it, and the answer is the first thing in the paste after the final answer
(`guidelines/client/stump-question-2026-11-21.md`, verbatim):

> How is each model stumped? Describe where and how the model goes wrong. Then explain why this is a fair stump and
> not an unfair one (for example, one that depends on a planted defect, one that depends on finding one sentence
> buried in the files, etc.). Show that getting it right takes deep reasoning or real analytical and methodological
> rigor.

It is the `Valid Stump?` field of the guidelines of 11/20 (section 6: where it fails, why it's fair, why it takes
reasoning), asked model by model. It is written after the runs, from their own text (both responses are saved under
`runs/` first; `run-triage` drafts it in `runs/triage.md`), and **kept in `submission.md` under
`## How is each model stumped?`, directly after `## Final Recommendation` and before `## Supplementary Questions`**.
Until the runs are back the file holds the tags and the four blocks. A build whose blocks are emitted by its
generator emits this one as well: the responses' figures and words are held in the generator exactly as the
responses write them, the golden's come from `figures.json`, and the generator's checks find every quoted figure
and phrase in the saved response, so a rebuild keeps the block and cannot leave it stale. It is not a graded block:
`figures_check.py`, `leak.py` and `freeze.py` read the four blocks by name and pass over it, and the determinism
judge does not read it.

Four short paragraphs, in the question's order (the bullets below are what goes into them):

- **Where and how each model goes wrong**, one paragraph per response, labelled as the platform labels them
  (`Response 1`, `Response 2`). Lead with what the response files against the golden (the band, the option, the
  figure), then take the decisive steps one by one: what the response did instead, in its own words where a short
  quote says it, with its own figure beside the golden's and the range, and which wrong member comes from which
  step. A step the response made is said to be made, with what it still missed (the fit made, the carry lost), and
  a member it files right on a wrong figure is given with both figures; a response that filed nothing is said to
  have filed nothing, with the working answer it reports and how far it got. **Quote the response where it names
  the choice itself**: a judgment call it flags, the right route kept as a sensitivity, counter-evidence it
  computed and set aside. That is the client's own picture of an analytical loss, in the model's words.
- **A route a response defends is ruled on, never waved off.** Where a response argues its route from a
  document's words, the block says what the document says, what the record shows against the route (a figure),
  and, where the other response read the same files the golden's way, quotes it. Before the block calls such a
  route a loss, the route is run in the golden's own estimators: if it moves a member across a line with the
  other steps right, it is a fork, and its figure and the fact that refuses it go on file (the fork table, a
  check, the closing passage) through `/fix-determinism` before the build is submitted.
- **Why it is fair**, answering the two unfair kinds the question names with figures from the pack, never with
  assurances. *Not a planted defect:* each step's problem is how the records come to be and runs through every
  unit, shown by its footprint outside the deciding members (the note's hidden factor record), and where the
  response's own cleaning counts match the golden's, say so with the counts: the loss came after the cleaning.
  *Not one sentence buried in the files:* say where the evidence sits (the two files whose comparison shows it,
  with the figure), that the definitions the steps rest on are the governing document's own and were read as
  written, and what each response found of the evidence unprompted (a step one response reached is reachable).
- **Why it takes deep reasoning or rigour**, as numbers and not as a claim: for each step, the obvious repair once
  the problem is seen, the wrong member and figure that repair still files, and the fact that refutes it (the
  closing passage's rivals and their refusals), then what the estimate takes instead (what has to be built, fitted
  or separated). Close on the independence: each step alone moves a different member, and which steps each
  response made and lost.

Written in plain words, every sentence carrying a figure or a quote, about 500 to 750 words for three steps and two
responses (the client's example for the older field ran four sentences on one step). It names no method the prompt
would have had to state, never claims a loss the responses' text does not show and never lists a step a response
made as missed. Every figure on the golden's side comes from `figures.json`, never typed: the blocks' own figures,
the closing passage's rivals, and the footprints and counts the fairness paragraph needs (the hidden factor
record's shares, the cleaning counts). A decisive step both responses landed is not listed as a stump; if that
leaves fewer than two missed between them, the build is not submitted on this block's strength (`build-pipeline`
stage 6).

## Rejection causes

LLM tells (em dashes, odd tables, white space, extra headers, filler such as *leverage, robust, seamless,
comprehensive*, hedging near the call); a figure that does not recompute; numbers that disagree between the blocks
and the golden files (the most common defect); padding; a component another valid method skips; an unpinned
convention; a conditional call; a golden ZIP whose file count differs from the prompt's; a critical component
that states a method, that the prompt never asks for, or that falls with another step's miss; a Supplementary
Questions block that reads as a long list of small asks; a stump answer that argues the design instead of quoting
the responses, or that counts a step a response made as missed.

## Checklist

- [ ] Exactly the four blocks plus tags, and once the runs are back the stump block; none of the banned blocks
- [ ] Final Recommendation first, one or two sentences, the deciding figure, what it rejects and why
- [ ] Supplementary Questions as one numbered entry per ask (one to four), each entry's figures one per line,
      grouped by file, each file's look described in one line
- [ ] Critical Components 2 to 5, one per stump: the answer with its unit and band and no method clause, in a
      requested deliverable and asked for by the prompt, each falling with its own stump alone
- [ ] The closing passage states the figure and the call with each decisive step left out alone (and in pairs
      where the call needs them together)
- [ ] After the runs: `## How is each model stumped?` directly after the Final Recommendation: where and how each
      response goes wrong, why the stump is fair (no planted defect, no buried sentence, shown by figures), why it
      takes rigour (each obvious repair's wrong figure and its refusal); every quote and figure in it found in
      the saved responses
- [ ] No figure every route reaches is stated in the Recommendation, the Supplementary Questions or the Critical
      Components (counts, rebuilt totals and bases sit in the Step-by-Step)
- [ ] Step-by-Step walks every result and shows the hurried analysis it rejects with its figure; closing passage
      names every rival
- [ ] No incidental figure; shared figures agree everywhere to the same rounding
- [ ] The golden ZIP holds exactly the requested files; code prints the components; `golden-realism` run after the
      figures froze
- [ ] `figures_check.py` exits 0; no em dashes
