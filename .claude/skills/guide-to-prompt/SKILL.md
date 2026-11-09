---
name: guide-to-prompt
description: Decide what to ask, then write it. Fit the assigned Sulfur subdomain (one of 21) and a task type in it, one objective, a forward-facing committed call and the answer shape whose cells the generated rubric grades; then write prompt.txt so it pins only the question, the decision, the deciding outcome or threshold and the deliverables, and never names the method, the comparison, the adjustment or a step. written the Mark way (one plain paragraph under 1,000 characters, question first, no persona, rounding once at the end), gated by voice-check.py; the author then rewrites it for voice and the gate's rewrite mode checks the rewrite for leaks only. Mark's best prompts are in references/mark-prompts.md and the client's 15 accepted Sulfur tasks in references/examples.md. Use at the start of every build, before stumping designs the ladder, whenever a prompt is written or edited, and again on the author's rewrite.
---

# Choosing what to ask, and writing it

**The author rewrites every prompt for voice.** This skill's job on `prompt.txt` is that it is correct and leaks
nothing: the right question, the decision and its bar pinned, every deliverable and ask with its unit and rounding,
and no word that tells the solver how to get there. Voice is the author's; leaks and wrong content are ours. Every
rewrite comes back through the gate (section 4) before upload.

Read `references/mark-prompts.md` (Mark's best prompts, the model for how to write one) and `references/examples.md`
(the client's 15 accepted Sulfur tasks, the model for the depth a task needs, with where each run went wrong) before
drafting; open the two or three nearest the draw in full under `guidelines/client/examples/`.

## 1. The fit

**One subdomain, one task type.** The author is assigned one of the 21 subdomains (`guidelines/client/domains.txt`,
indexed in `references/domains/README.md`); pick one task type in it that serves the objective (the card's
`subdomain`; the guard and `precut.py` refuse one that does not). Each subdomain's client text carries two lines that
decide fit, quoted in `references/domains/README.md`: **what makes it deep** (the judgments that make that field's
tasks hard) and **domain fit** (what the deciding step must be). The deep step is drawn from the first and must
satisfy the second.

**Swap test:** put another field's nouns in the call sentence; if it reads the same, the domain is a backdrop. Write
the field's own deciding analysis, and why the swap breaks it, into the card's `domain_test` and the design note's
`## Deep reasoning` (`stumping` 1.1). A stated score, an eligibility check, a sort or a filter deciding the call is
a backdrop at any depth.

**One objective.** Forecasting & Predictive Modeling is especially welcome wherever the data supports a
deterministic answer.

| Objective | The decision turns on | Native shapes |
|---|---|---|
| **Forecasting & Predictive Modeling** (most wanted) | a future value the supplied history pins down, the model earning its place out of sample | 02, 13; 04, 06 over an open window |
| Root-Cause Analysis | the driver of a move, rivals ruled out on evidence | 12, 18; 09 for a fall |
| Anomaly Detection & Diagnostics | a real event separated from an artifact or from variance beyond noise | 17, 16, 01 |
| Experiment & Causal Analysis | a causal claim, designed or observational, with its uncertainty matched to the design | 11, 07, 08 |
| Descriptive & Distribution Analysis | how a population is composed or a metric distributed, not why it moved | 14, 05, 10 |
| Data Extraction & Conformation (ETL / Pipeline Build) | multi-source inputs conformed, then feeding an analytical judgment that decides | 03, 15 |
| Opportunity Sizing & Decision Support (house tag) | a sized opportunity, pool to realisable, driving the call | none; fails if retaggable unchanged |
| Data Quality Monitoring & Alerting (house tag) | the health of the data or pipeline, with a monitoring call | none; fails if retaggable unchanged |

**ETL is the most closed objective Mark measured, and the client now says conforming is never the stump.** Every ETL
driver Mark filed was one of five moves (complete a record the process could not make; re-grain or re-key onto the
decision's unit; re-time onto the decision's calendar; recover a per-case input a second file pins; split a total
between two causes), and a conformation call's decisive step reduces to a correction whose input is present (rule
application), absent (not determinate) or sampled (a measurement model). Sulfur's shape 15 says the same from the
other side: the conformed data must feed an analytical judgment that decides, such as an estimate whose uncertainty
depends on match quality. An ETL draw names that judgment before any world is drawn.

The committed call faces forward by default (a figure booked, ordered or staffed for a window not yet closed); a
retrospective call needs its reason in the design note. Write the fit into the design note's `## Draw`, then
`guard.py recent` and `coverage` before choosing and `guard.py check` on the card (`fingerprint`).

## 2. The shape, before the ladder

The rubric is generated from the prompt and the answer blocks, so the structure of the answer decides how many places
the runs can show whether they did the analysis. A concise prompt still asks for a rich answer: the work comes from a
few demanding asks over a repeated unit (candidates, periods, cells, reconciling items), never from a long list of
simple requirements. **Every cell of the shape must sit downstream of the deep step**, so a run that skipped it files a
different value in most cells. Pick from `references/shapes/README.md` (the client's 18 shapes, the same as Mark's,
each with its arithmetic and the seam where it turns hard rather than long) and write the cell count and why each cell
moves with the deep step into the design note.

| # | Shape: criteria from | # | Shape: criteria from |
|---|---|---|---|
| 01 | Ranked list under a cap: each candidate | 10 | Scorecard: each metric-threshold check |
| 02 | Forecast across periods: each period | 11 | Before and after with a control: each unit's effects |
| 03 | Bridge between totals: each reconciling item | 12 | Drill-down to one leaf: each level's piece |
| 04 | Setting one dial: each allowed setting | 13 | Scenarios and the flip point: each cell, the flip |
| 05 | Allocation to a fixed total: each bucket | 14 | Cuts of a distribution: each cut per segment |
| 06 | Schedule under capacity: each finish period | 15 | Fields to one schema: each field's source and transform |
| 07 | Grid of cells: each cell | 16 | Indicators into one score: each indicator |
| 08 | Rule replayed on history: each period's cells | 17 | Periods around a change point: each period |
| 09 | Funnel of stages: each stage's volume, rate, cost | 18 | Hypotheses versus evidence: each cell |

Shapes 08, 10 and 15 carry the client's own warning: a replay, a scorecard whose metrics and tests the folder spells
out, or a conformation are banned as the deciding stump and earn their place only through an independent analytical
step that flips the answer.

## 3. Writing prompt.txt

**Write it the Mark way.** The author's instruction is to learn prompt writing mostly from Mark, whose prompts came out
short, sweet and crisp: a person asking for help with a job they understand, the question first, the files wanted
back, each unit beside its figure, rounding once at the end, in one paragraph under 1,000 characters. It says nothing
a solver could use that the files do not also carry, and nothing about who is asking. Mark's best prompts, with where
each stump hides, are in `references/mark-prompts.md`; read them before drafting. The author then rewrites the draft
for a human voice, and the rewrite comes back through the gate in rewrite mode (section 4).

Write it last, against the golden. Context, question, files, rounding, in one paragraph. **The ten rules:**

1. **Lead with the question**, a direct question in the first two sentences.
2. **Cut who and why:** no names, titles, roles ("I'm getting the recommendation together"), sign-offs, meetings or
   readers of the file; go straight into the problem.
3. **Test every fact before cutting it:** a send date, extract date, cut-over or stop rule that bounds the answer stays.
4. **Keep every ask exactly:** what each deliverable holds, its periods, units and rounding, in meaning.
5. **Do not change meaning while smoothing:** "in cents" is not "dollars and cents"; "whether any, and if so how many"
   is not "how many".
6. **One continuous paragraph**, list items joined by commas and semicolons, no "Then" or "Last".
7. **Merge and shorten;** each rounding rule once, at the end, naming the figures it governs.
8. **Ask, do not specify:** "what is", "put it in", "also give me", never "X is the file, one row per".
9. **Drop claims made only to be rejected.** An opinion arguing the wrong answer is cut.
10. **Run the Sulfur check last:** does the answer turn on deep reasoning (three or more dependent inferences, one a
    statistical or modeling judgment), or on a stated procedure, a field read correctly, a planted row or one fact?
    If the latter, the build is not ready, whatever the prompt says.

**The prompt pins only four things** (Sulfur): the question, the decision, the deciding outcome or threshold, and the
deliverables. **May say:** the question, with the candidate set and the hold on the same footing ("or none this
cycle") where relevant; the forcing fact once (window, date, cut-over, stop rule); the threshold the call is held to;
each deliverable by its type, as a person asks for it ("a spreadsheet with a before-and-after chart", "a few slides
for the review"), with its content as a person states it; a file name only where the person would really give one;
the standard the call runs on only where the pack lacks it; a generic threat to validity ("participation was
voluntary").

**Never says:**
- **a method, comparison, model or adjustment** (Sulfur: never name the method, the trap, the comparison group, the
  confounder, the adjustment or the file that matters): no difference-in-differences, control group to use,
  shrinkage, clustering, back-test, out of sample, stratify, reweight, standardise, deduplicate, adjust or control
  for, seasonal adjustment, development curves, censoring, regression to the mean, mix or composition effects, and
  no hint such as "compare A against B";
- **a warning** (watch out, be careful, note that, make sure to account for, at face value, misleading);
- anything that fixes the basis, window, convention or population the deep step rides on (those are filed in the
  pack's governing document in the organisation's genre, `stumping` Part 4); the deciding metric, eligibility rule or
  fee schedule; an input file name; a standard by acronym; a trap word (clean, unduplicated, reconcile, attribution,
  mix, standardise, grain); two metrics named as valid; a warning that a view might mislead;
- **a count the data hold** (the candidate set's size, a population count, a derivable count: "which four of the
  eight", "each of our twelve zones", "we run 264 schools"); a decision parameter stays where it is not tied to such a
  count ("designate seven", never "seven of the sixteen");
- **a sentence that explains the data** (what a file is, how a field is coded, which system produced a column): the
  pack's own documents say that in the organisation's voice or nothing does;
- **a presupposition**, an ask that only parses if a subset is non-empty or a move happened ("how many and what they
  cost", "the sites where it fell"): make "none" a grammatical answer ("whether any and, if so, how many and what
  they cost") with every figure, unit and rounding kept, while a fact the requester knows before any analysis stays
  (`reduce-house-fixes` H23).

**What the client's reviewers return:** a prompt that spells out the method (anything the model should
work out itself, including an intermediate quantity asked only because the method needs it), that names the
attached files or lists the files wanted back, that describes more than the question needs, or that says who is
asking. Context the decision needs is buried in the files; the prompt is minimally sufficient: the question, the
outcomes wanted, the deliverables by type, the rounding. `voice-check.py` reads a deliverable named by type when
no file name is given.

Sulfur's prompt module sends a prompt back when it "names the method or the trap, warns the solver, rests on a written
procedure, allows a hedged answer, needs outside knowledge, pulls in a separate dataset or decision, or asks for more
than three files" (`guidelines/client/learning-modules/prompt.txt`). Its leaks to avoid, verbatim from the prompt
reminders: "Be careful: the nine schools were picked...", "Compare them with similar schools...", "Drop the duplicate
spring file...", "Cluster by school...". After drafting, reread the prompt as the solver and cut any sentence about
how to do the analysis, what to exclude, or what to watch for.

**Budget.** 1,000 characters is about 150 to 170 words. Compress per sentence, never by deleting a requirement: one
sentence with a list in it per file; cut every reason but one motive; rounding once; no role, meeting or pack
inventory; ask rather than specify. Never cut the repeated unit, the call, runner-up, gap or flip, a chart's named
parts, a unit, a derived figure's rounding, or the forcing fact. After each pass walk the figure list, recount the
cells and rerun the gate.

**Variety.** Two tasks on the same pattern with the same data structure are duplicates, and in Mark the one Duplicate
the portal returned named the prompt's shell (how many, a workbook with a count-once side table, one labelled stacked
bar, nearest N), not its nouns: 182 of 186 Mark prompts ran question, deliverable, side table, chart, rounding. So
the shell is drawn with the world: the question's form from the decision (a count asks how many, a pick which, a gate
whether, an amount how much, a date when); the second sentence led by the deliverable, the rule, the date or the use
rather than "Put ... in" every time; the rounding sentence opened on the figures it governs; the deliverable set and
the chart's species varied. `voice-check.py` holds corpus quotas (no question form over 30 per cent of prompts on
file, no second-sentence opener, rounding opener or deliverable set over 20 per cent) as a WARN.

**The client's templating checker.** The portal's pattern checker counts seven signals and marks a prompt
templated at three, borderline at two: files listed up front; steps ("First... Then... Finally"); three or
more stacked questions (two question-sentences in the opening already count); a closing one-sentence list of
documents; a dictated method ("according to the standard"); lists inside the prompt; UK spelling. Write one
question, name each deliverable file only in the sentence that gives its reason, never close on a list of
documents, and keep every ask's definition and rounding in flowing prose. Fold a second quantity into the one
question ("judged on the bed-days each hospital's share would free") rather than asking it; prefer neutral
wording to a UK-only spelling ("with every bar showing its value", not "labelled"). Mark's task127 scored four
of seven. `voice-check.py` counts the signals and fails at two.

**The call and the asks.** The call is one quotable sentence with its unit. Every ask is a component, qualifier (a
range, a sensitivity, the best alternative and whether it replaces the call) or audit trail of it, multi-dimensional
(many rows, periods, segments), and hard because the deep step feeds it; an ask a person could act on with the call
unmade is a second decision (`reduce-house-fixes` H18). An entity plus an aggregate names its grain. The asks are
designed in `supplemental-stumping`.

**The author's rewrite.** The design note's `## Prompt contract` lists, line by line, what a voice rewrite may not
drop or change: the decision sentence, the threshold, the hold option, every deliverable name and extension, every
ask with its unit and rounding, the as-of date. Hand it to the author with the draft. When the rewrite comes back, it
replaces `prompt.txt`, `pipeline.json` gets `"prompt_rewritten": true`, and the gate runs in rewrite mode: every leak
rule still fails it, the voice rules only warn. Then `leak.py` again, and the four answer blocks are re-read against
the rewritten wording.

## 4. The gate

```
python3 .claude/skills/guide-to-prompt/references/voice-check.py taskNN             # exit 1 on any FAIL
python3 .claude/skills/guide-to-prompt/references/voice-check.py --file <draft> --task taskNN
python3 .claude/skills/guide-to-prompt/references/voice-check.py taskNN --rewrite   # the author's rewrite
python3 .claude/skills/guide-to-prompt/references/voice-check.py                    # batch report
```

**Draft mode fails on** (Mark's rules): not `prompt.txt`; any backtick, hash, pipe, bracket, bullet, label-colon line,
or emphasis outside a file name; a line break; no question mark in the first two sentences; 1,000 characters or
more; an em or en dash; a persona from the card's `world.people`, a title, sign-off, board vote or reader; a sentence
opening Then, Next, First, Second, Last, Finally, After that; an LLM tell (leverage, robust, comprehensive, seamless,
delve, ensure, note that, in order to, furthermore, stakeholders); two attributed opinions; rounding outside the last
sentence; zero or more than three files; a count the data hold. **And on Sulfur's two leak rules:** a method,
comparison or adjustment named; a warning to the solver. It warns on a method hint word (cohort, holdout, matured,
pooled, weighted, seasonal, spillover, comparison or control group), a shell class over its corpus quota and a missing
rounding sentence.

**Rewrite mode** (`--rewrite`, or `"prompt_rewritten": true` in `pipeline.json`, which `precut.py` and `leak.py`
read too) keeps every leak rule as a FAIL (markdown, em dash, method named, warning to the solver, count the data
hold, deliverables) and turns the voice rules (one paragraph, question first, length, persona, sequencing, LLM tells,
roll call, rounding placement, shell quota) into WARNs. `leak.py` sweep 11 and `precut.py` run the same gate;
`leak.py` sweeps 4 and 5 add the design note's deep-step vocabulary and announcement sentences. A failing draft is not
done, and neither is a rewrite that fails.

## Checklist

- [ ] Subdomain, task type, objective and `domain_test` fixed against the client's "what makes it deep" and "domain fit"
- [ ] The shape picked, its cells counted, every cell downstream of the deep step
- [ ] The prompt pins the question, the decision, the threshold and the deliverables, and nothing about the method
- [ ] Every ask multi-dimensional with its unit and rounding; none presupposes what the data hold
- [ ] The draft is one paragraph under 1,000 characters, question first; `voice-check.py taskNN` exits 0
- [ ] `## Prompt contract` written and handed over; the author's rewrite passes `voice-check.py taskNN --rewrite`
