---
name: submission-writeup
description: Draft or revise submission.md, the Sulfur answer blocks the author pastes into the platform, and every golden deliverable in the golden ZIP. Invoke whenever a submission.md is being written, rewritten, extended or reviewed for a task folder, including when the request just says "write the submission", "draft the answer", "do the golden for taskNN", or when a review says a block is thin. Carries the four platform blocks in order (Final Recommendation naming what it rejects, Supplementary Questions numbered one per sub-ask, Critical Components 2 to 5 drawn from different areas of the results chain, Step-by-Step walking every result and showing the hurried analysis it rejects, closing on why no other conclusion survives), the rule that every figure is emitted by the generator and recomputes, and the golden ZIP rules (exactly the files the prompt requests, one set of numbers).
---

# Writing the answer blocks

`submission.md` holds the four blocks the author pastes into the platform's Final Recommendation, Supplementary
Questions, Updated Critical Components and Updated Step-by-Step fields. The rubric is **generated** from them and
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
- **Reproducible, not low-level.** Steps name the file and the method that produce each result; they do not walk
  arithmetic, restate the files' conventions or narrate cleaning. A convention needing a paragraph belongs pinned in
  a shipped file.

**Order:** build, `determinism-check`, this skill, `golden-realism`; never before the analysis is done.

## The blocks, in order

| # | Block (platform field) | Length |
|---|---|---|
| 0 | `## Tags` (not pasted; for the card and the domain field) | 2 to 3 lines |
| 1 | `## Final Recommendation` | 1 or 2 sentences, the deciding figure, what it rejects |
| 2 | `## Supplementary Questions` | numbered, one number per sub-ask, grouped by file |
| 3 | `## Critical Components` | 2 to 5 one-liners |
| 4 | `## Step-by-Step` | about 6 to 10 numbered one-liners, then a short closing passage |

Nothing else goes in the file. **Not written:** a format rationale, a justification block, a golden listing, key
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

**2. Supplementary Questions.** One clearly labelled answer per sub-ask, numbered in the prompt's order, grouped by
file under `### <file.ext>` (the golden file's own name; the prompt asks for it by type), in the exact unit and
rounding asked. Where an ask is a requested file, the answer
**describes how that file should look**: its rows, columns, ordering, the figures in it and where the visual sits.
Each answer is graded at the main call's bar: it reproduces and is uniquely forced.

> ### district_excess.csv
> 1. Twelve rows, one per district, sorted by excess cases a week, highest first; columns district, raw weekly
>    cases, testing-adjusted excess (whole cases), 90 per cent interval (whole cases).
> 2. Harlow 41 (interval 33 to 49); Brenton 9 (interval 2 to 16); ...

- **Concise is not summarised.** An ask owing a row-set gets every row as its own point, every column value named,
  in the deliverable's order.
- **Never a markdown table** (pipes break, wide tables wrap, odd tables are an LLM tell).
- A figure in two places has the same rounding in both; compute it once in code and carry it.

**3. Critical Components.** 2 to 5 load-bearing results **every valid method must compute**, one line each, the
figure in bold at its rounding everywhere else, **drawn from different areas of the results chain** (an assembly
result with its gap to a control total, a model's estimate with its band, a backtest's error, an attribution's
shares, an onset date), never three restatements of one fit. These carry the most rubric weight, so most of them are
results the careful but hurried pass loses. Test: if a defensible method could skip it and still reach the answer,
cut it; if the hurried pass also gets it right, it grades nothing but its place in the chain.

> 1. Testing volume in Brenton rose **104 per cent** year on year against **11 per cent** in Harlow.
> 2. Harlow's testing-adjusted excess is **41 cases a week** (90 per cent interval **33 to 49**).

**4. Step-by-Step.** A short numbered path from the raw files through each result to the recommendation and the
supplementary answers, one sentence per step: the method, the shipped file it reads, and the figure it produces. At
each result the hurried pass loses, the step makes the judgment explicit (which comparison, which model, which
adjustment, which check, and why the data rule out the simpler route) and **shows the hurried analysis it rejects**:
the hurried method's figure from `figures.json`, then the data that overturn it.

> 3. Ranked districts on raw weekly cases from `case_line_list.csv`: Brenton leads at 63 a week (the shallow read).
> 4. Joined `lab_testing_volumes.xlsx`: Brenton's tests doubled while positivity stayed flat, so its rise is
>    ascertainment, not incidence.

Then **a short closing passage** (two to four sentences): why no other conclusion survives the prompt, the files and
standard domain knowledge, naming each rival method and the fact that rules it out.

- Cite where a convention is pinned ("per the surveillance protocol"), never restate it. A convention a competent
  analyst could reverse is an unpinned fork, fixed in a shipped file.
- Name only files the pack ships, by their pack names, or the grader finds missing input.
- Where a messy-data handling moves a graded figure, one step names the handling and the files it joins, so the
  grader can verify it; it never reads as the reason the call holds.
- End each step in a figure or finding, never an intention ("Analyzed the cohort data" is not a step).

## The golden ZIP

- **Exactly the files the prompt requests, in the requested formats, and nothing else.** If the prompt asks for a
  memo and a CSV, the ZIP holds those two files. A missing file, an extra file or a mismatched format blocks
  confirmation on the platform. Name it `golden.zip` in the task folder, built from `golden/` by the generator.
- **One set of numbers everywhere**: the recommendation, every answer, the critical components and every table and
  chart in the golden files agree exactly, same rounding. A grader diffs them against each other.
- **Business-realistic is a gate**: once figures are frozen, run every golden through `golden-realism`.
- **The recommendation is unmissable** in the files, never inferred from output.
- **A code deliverable prints the critical components' figures**, not only the answer.
- **Prefer code-produced artifacts** (a library chart, a script-written workbook, an emitted CSV); a chart in a text
  deliverable still comes from the script.
- **Nothing extra**: no answer to an ask the prompt did not make, no AI disclaimer, no placeholder.
- **Show the routes where the deliverable allows**: a short table in the golden of what each tempting shortcut gives
  beside the golden's figure (the client's reviewers praised "a routes sheet shows each shortcut's result, so the
  reasoning can be checked end to end"), so careful partial work earns visible credit; inside a requested file, never
  as an extra one.

## Rejection causes

LLM tells (em dashes, odd tables, white space, extra headers, filler such as *leverage, robust, seamless,
comprehensive*, hedging near the call); a figure that does not recompute; numbers that disagree between the blocks
and the golden files (the most common defect); padding; a component another valid method skips; an unpinned
convention; a conditional call; a golden ZIP whose file count differs from the prompt's.

## Checklist

- [ ] Exactly the four blocks plus tags; none of the banned blocks
- [ ] Final Recommendation first, one or two sentences, the deciding figure, what it rejects and why
- [ ] Supplementary Questions numbered one per sub-ask, grouped by file, each file's look described
- [ ] Critical Components 2 to 5 from different areas of the chain, most of them results the hurried pass loses
- [ ] Step-by-Step walks every result and shows the hurried analysis it rejects with its figure; closing passage
      names every rival
- [ ] No incidental figure; shared figures agree everywhere to the same rounding
- [ ] The golden ZIP holds exactly the requested files; code prints the components; `golden-realism` run after the
      figures froze
- [ ] `figures_check.py` exits 0; no em dashes
