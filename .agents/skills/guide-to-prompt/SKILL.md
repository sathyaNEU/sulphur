---
name: guide-to-prompt
description: Decide what to ask, then write it. Fit the assigned Sulfur subdomain (one of 21) and a task type in it, the assigned analysis type (one of nine), and an answer that is a structured set of results in one of the client's fourteen answer shapes, with a forward-facing recommendation on top where the decision needs one; then write prompt.txt so it pins only the question, what each result is (as one to four hard, multi-faceted asks, with each decisive step's own quantity asked for in the decision's words), the deliverables by type, and never dictates rounding, names the method, the comparison, the adjustment, a step or an attached file, never warns and never says who is asking. Written short and crisp (one plain paragraph under 1,000 characters, question first, no rounding instruction), gated by voice-check.py; the author then rewrites it in their own words (the project lead runs a three-strike policy on LLM-sounding prompts) and the rewrite is re-gated.
---

# Choosing what to ask, and writing it

**The author rewrites every prompt for voice.** This skill's job on `prompt.txt` is that it is correct and leaks
nothing: the right question, the decision and its bar pinned, every deliverable and ask with its unit (never a rounding),
and no word that tells the solver how to get there. Voice is the author's; leaks and wrong content are ours. Every
rewrite comes back through the gate (section 4) before upload.

Read `references/mark-prompts.md` (Mark's best prompts, the model for how to write one) and `references/examples.md`
(the client's accepted Sulfur tasks, the model for the depth a task needs, with where each run went wrong) before
drafting; open the two or three nearest the draw in full under `guidelines/client/examples/`, and the prompts of
`1.txt`, `16.txt` and `17.txt` (the three shared as the library's hardest) for how a prompt asks for each decisive step's answer
without naming a method. The client's guidelines of 11/20 (`guidelines/client/guidelines-2026-11-20.md`) are the
page a prompt is reviewed against.

## 1. The fit

**One subdomain, one task type.** The author is assigned one of the 21 subdomains (`guidelines/client/domains.txt`,
indexed in `references/domains/README.md`); pick one task type in it that serves the assigned analysis type (the card's
`subdomain`; the guard and `precut.py` refuse one that does not). Each subdomain's client text carries two lines that
decide fit, quoted in `references/domains/README.md`: **what makes it deep** (the judgments that make that field's
tasks hard) and **domain fit** (what the deciding step must be). The results are drawn from the first and must
satisfy the second.

**Swap test:** put another field's nouns in the call sentence; if it reads the same, the domain is a backdrop. Write
the field's own deciding analysis, and why the swap breaks it, into the card's `domain_test` and the design note's
`## Deep reasoning` (`stumping` Part 4). A stated score, an eligibility check, a sort or a filter deciding the call is
a backdrop at any depth.

**One analysis type, assigned.** The client now assigns the analysis type as it assigns the domain, to spread the
work: "80% of tasks followed a very similar format." Each type, in the client's words, with the shapes it most often
takes (any of the fourteen can fit):

| Analysis type | What it answers (client) | Native answer shapes |
|---|---|---|
| Descriptive & Distribution Analysis | where a total really sits, once immature periods or design weights are handled | a distribution and where it is cut; a reconciled table |
| Comparative Analysis & Explanation (client most wanted) | why two groups or two periods differ, with the gap decomposed | a bridge; ranked causes with contributions |
| Anomaly Detection & Diagnostics | which units are genuinely unusual once real variance beyond noise is modelled, with a stated rule and false-alarm rate | a flagged set with its false-alarm rate; a timeline |
| Root-Cause Analysis (client most wanted) | the chain from a symptom back to its cause, with rival explanations ruled out by the data | ranked causes with contributions; a timeline |
| Experiment & Causal Analysis (over-represented) | what a change did, against a comparison the design supports | scenarios with the flip point; a bridge |
| Forecasting & Predictive Modeling (client most wanted) | a path with a band, chosen because it wins out of sample | a forecast path with bands and drivers |
| Opportunity Sizing & Decision Support | how large an opportunity is and where a dial should be set | an allocation with its sensitivity; a ranked list under a cap; a schedule under capacity |
| Data Extraction & Conformation (ETL / Pipeline Build) | messy sources linked and conformed to one schema, with a computed, checkable result | a reconciled table plus findings |
| Data Quality, Monitoring & Alerting | a monitoring rule tuned on history, with the alert load it will produce | a monitoring rule with its expected alert count; a defined metric |

**ETL is the analysis type Mark found most closed, and conforming never decides a task on its own.** Every ETL
driver Mark filed was one of five moves (complete a record the process could not make; re-grain or re-key onto the
decision's unit; re-time onto the decision's calendar; recover a per-case input a second file pins; split a total
between two causes), and a conformation call's decisive step reduces to a correction whose input is present (rule
application), absent (not determinate) or sampled (a measurement model). Sulfur's shape 15 says the same from the
other side: the conformed data must feed an analytical judgment that decides, such as an estimate whose uncertainty
depends on match quality. An ETL draw names the results after the conformation (the matching rule with its
estimated error rate, the gap to a published total, the analysis on top) before any world is drawn.

The committed call faces forward by default (a figure booked, ordered or staffed for a window not yet closed); a
retrospective call needs its reason in the design note. Write the fit into the design note's `## Draw`, then
`guard.py recent` and `coverage` before choosing and `guard.py check` on the card (`fingerprint`).

## 2. The answer shape, before the results

The client's answer is "a set of results, not one call. A recommendation can sit on top of it." Pick one of the
fourteen answer shapes (`vocab.json` answer_shapes: ranked causes with their contributions; a timeline; a forecast
path with bands and drivers; a bridge that reconciles two totals; a flagged set with the evidence and the false-alarm
rate; a reconciled table plus findings; an allocation with its sensitivity; a ranked list under a cap; a schedule
under capacity; a monitoring rule with its expected alert count; scenarios with the flip point; a distribution and
where it is cut; a composite score; a defined metric with its properties), not the last build's (`guard.py` blocks a
repeat). The shape's cells are where the rubric grades, so the results of the chain sit in its cells and the results
the runs lose sit in different cells. The card also keeps the prompt shape it uses (`shape`, the client's 18 prompt
shapes below, each with its arithmetic in `references/shapes/README.md`):

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
out, or a conformation never decide a task on their own; they earn their place as results beside results that need
their own analysis.

**The deliverable formats.** One to three files, and the house set is a CSV, a workbook and at most a deck. The
workbook holds the results a reader works in, and its first sheet states the call; a CSV holds a table another
person or system will load (one row per member, period or cell); a few slides are asked for only where the reader
is a meeting, and the first slide states the call. A written document (a memo, a note, a report or a one-pager, as
Word, PDF or Markdown) is the rare exception: asked for only where the decision's reader could not use a workbook
or a deck (a filing, a signed determination, a notice that leaves the organisation), with the reason in the note's
`## Draw`. What a note would have said goes on the workbook's first sheet or the deck's first slide. A call that
needs a recommendation never ships as a CSV alone. `voice-check.py` (the `deliverable formats` row) and `guard.py
check` (`prefer.formats`) warn on a written document. A repair that keeps the prompt keeps its files; a new draw
and a re-root choose them by this rule.

## 3. Writing prompt.txt

**Write it the Mark way.** The author's instruction is to learn prompt writing mostly from Mark, whose prompts came out
short, sweet and crisp: a person asking for help with a job they understand, the question first, the files wanted
back, each unit beside its figure, in one paragraph under 1,000 characters. **It carries no rounding instruction**
(the author's rule since this harness's Sulfur prompts: a prompt that dictates rounding grades a run on a rounding
convention rather than on the analysis, and runs report their own precision anyway); each graded figure's precision,
with its band where reasonable methods differ, is stated in the answer blocks instead (`submission-writeup`). It says nothing
a solver could use that the files do not also carry, and nothing about who is asking. Mark's best prompts, with where
each one's difficulty hides, are in `references/mark-prompts.md`; read them before drafting. The author then rewrites the draft
for a human voice, and the rewrite comes back through the gate in rewrite mode (section 4).

Write it last, against the golden. Context, question, files, in one paragraph. **The ten rules:**

1. **Lead with the question**, a direct question in the first two sentences.
2. **Cut who and why:** no names, titles, roles ("I'm getting the recommendation together"), sign-offs, meetings or
   readers of the file; go straight into the problem.
3. **Test every fact before cutting it:** a send date, extract date, cut-over or stop rule that bounds the answer stays.
4. **Keep every ask exactly:** what each deliverable holds, its periods and units, in meaning.
5. **Do not change meaning while smoothing:** "in cents" is not "dollars and cents"; "whether any, and if so how many"
   is not "how many".
6. **One continuous paragraph**, list items joined by commas and semicolons, no "Then" or "Last".
7. **Merge and shorten;** no rounding rule anywhere; precision belongs to the answer blocks.
8. **Ask, do not specify:** "what is", "put it in", "also give me", never "X is the file, one row per".
9. **Drop claims made only to be rejected.** An opinion arguing the wrong answer, or a memo whose number is simply
   wrong, is cut. An incumbent figure that is the right computation of a shallower quantity (the contractor's rate,
   the draft's fall, the manager's plan) may stay as the stakeholder's position when an ask prices it on the same
   footing as the golden (`stumping` Part 1b).
10. **Run the bar check last:** does the answer ask for several results that each need their own analysis, or does
    it turn on a stated procedure, a field read correctly, a planted row, a built-in factor, one fact or one
    decisive step? If the latter, the build is not ready, whatever the prompt says.
11. **Read the prompt against the answer** (the guidelines of 11/20: "the prompt must not point the other way. A
    model that follows your prompt's own words must not be marked wrong"). Take each sentence literally and follow
    it to a figure: a window, a population, a unit, an "as of", a "for each", a stakeholder's stated belief. If the
    literal reading lands anywhere but the golden, the sentence is rewritten or the convention is filed in a
    document, and the judge's Gate A is run on the final wording (`determinism-check`).

**The prompt pins only three things**: the question (with the decision and its threshold where there is one), what
each result is (its population, outcome, window and unit, in plain words) and the deliverables by type, and no
rounding. **May say:** the question, with the candidate set and the hold on the same footing ("or none this
cycle") where relevant; the forcing fact once (window, date, cut-over, stop rule); the threshold the call is held to;
each deliverable by its type, as a person asks for it ("a spreadsheet with a before-and-after chart", "a few slides
for the review", "a CSV of every feeder"), with its content as a person states it; a file name only where the
person would really give one;
the standard the call runs on only where the pack lacks it; a generic threat to validity ("participation was
voluntary").

**Draft straight to NATURAL (0 of 9 signals, FEW/NO SIGNS on the AI-writing scan) on the first pass.** Do not ship a
mechanical brief expecting back-and-forth edits later. Every draft obeys four practitioner rules proven directly
against the platform's 9-signal templating and AI-writing checker (and mechanically gated by
`.agents/skills/guide-to-prompt/references/voice-check.py`):

1. **Never explain *why* the data need estimation (no data-gap pre-diagnosis).** Pre-identifying a metering gap,
   missing telemetry, uncounted stock, or partial coverage (`"substations lack direct metering for the peak load
   figure"`, `"nobody counts..."`, `"nothing on record shows..."`) triggers both *Excessively wordy / over-contextualized*
   and *AI-writing scan D (analysis done in the brief)*. If estimation framing is needed for domain fit, keep it to one
   bare sentence (`"Timing and sizing have to be estimated from the 2026 records."`) and let the solver discover the
   observation gap in the files. State a calendar cutoff only when it defines the forward window itself, never as an
   explanation of an instrument gap.
2. **Never spell out a methodology chain (`"how X drives Y"`).** Clauses like `"so we can see how each site's A, B,
   and C drive its D and E"` tell the solver which factors to chain together and in what logical order. Drop the
   `"how X drives Y"` framing completely: ask for `"site-level backup to justify the schedule and sizing"` (or the
   domain's natural equivalent) and let the solver choose what to show.
3. **Never enumerate a uniform parallel factor triplet (AI-writing scan C/D).** Symmetric three-item lists of
   intermediate model inputs (`"peak active demand, reactive demand, and heaviest-phase share"`) read as a
   model-generated inventory and duplicate what belongs in the organisation's governing document. File exact formulas,
   definitions, and required filing columns inside the governing standard in `target/` (e.g. a planning standard or
   appropriation filing spec), and reference them in `prompt.txt` by their practitioner name (`"each site's 2026
   appropriation filing figures and assigned phase"`).
4. **Never add `"in the ZIP"` or `"See the attached ZIP."` filler.** Refer naturally to the records (`"from the 2026
   records"`) or omit attachment mentions entirely.
5. **Never recite a column-by-column register spec or stack sub-metric cuts of the same quantity.** A sentence like
   `"Rank every operational cause by projected 2027 excess container-days alongside its 2026 total, total 2027 network
   and remediation container-days, 2027 cost in euros overall and for designated causes, plus ..."` triggers BOTH
   *Spells out the methodology* and *Excessively wordy / over-contextualized*. State the core business decision in the
   opening question, pin the exact column schema and formulas in the organisation's governing charter/standard in
   `target/`, and name only the two or three headline commercial outputs Controlling or leadership actually needs.
6. **Never stack two or three deliverables in the closing sentence.** Ending on `"Put A in a CSV, build B in a
   spreadsheet, and summarize C in a short slide deck"` triggers *Closes on a list of documents*. Give each deliverable
   its own short sentence anchored to why its specific audience uses it (e.g., deck for the close-out review,
   spreadsheet for Controlling, CSV to load into the tracker), with at most one deliverable type in the final sentence.

**Measured contrast (task26, platform LLM prompt test):**
- *BORDERLINE (2 of 9 signals, AI-writing scan: SOME SIGNS):* `"The relief-pool substations lack direct metering for
  the peak load figure used in capital planning, so both the timing and the sizing have to be estimated from the 2026
  records in the ZIP. Put the 2027-2029 relief schedule and a loading chart up front in a spreadsheet so we can see
  how each site's peak active demand, reactive demand, and heaviest-phase share drive its firm N-1 loading and relief
  sizing, plus the pool summary."`
- *NATURAL (0 of 9 signals, AI-writing scan: FEW/NO SIGNS, Formatting: PASS):* `"When should each Vesterdal Nett
  substation in the relief pool get firm-capacity relief in the 2027-2029 capital cycle, and how much relief capacity
  in MVA is needed overall? Timing and sizing have to be estimated from the 2026 records. Put the relief schedule and
  a loading chart up front in a spreadsheet, with the pool summary and site-level backup to justify the schedule and
  sizing. We'll also load each site's 2026 appropriation filing figures and assigned phase into our network register,
  so include a substation-level CSV as well."` (88 words, 537 chars; compact, insider domain vocabulary, zero
  methodology chaining, zero data-gap explanation, zero triplet inventory; every formula and filing column pinned
  inside `vesterdal_planning_standard_ns2026.pdf`).

**Never says:**
- **a method, comparison, model or adjustment** (Sulfur: never name the method, the trap, the comparison group, the
  confounder, the adjustment or the file that matters): no difference-in-differences, control group to use,
  shrinkage, clustering, back-test, out of sample, stratify, reweight, standardise, deduplicate, adjust or control
  for, seasonal adjustment, development curves, censoring, regression to the mean, mix or composition effects, and
  no hint such as "compare A against B";
- **a methodology chain or factor triplet** (`"so we can see how A, B, and C drive D"`);
- **a data-gap or metering-gap explanation** (`"lack direct metering"`, `"can't be metered"`, `"nobody counts..."`);
- **a warning** (watch out, be careful, note that, make sure to account for, at face value, misleading);
- anything that fixes the basis, window, convention or population a result's work rides on (those are filed in the
  pack's governing document in the organisation's genre, `stumping` Part 5); the deciding metric, eligibility rule or
  fee schedule; an input file name; a standard by acronym; a trap word (clean, unduplicated, reconcile, attribution,
  mix, standardise, grain); two metrics named as valid; a warning that a view might mislead;
- **a count the data hold** (the candidate set's size, a population count, a derivable count: "which four of the
  eight", "each of our twelve zones", "we run 264 schools"); a decision parameter stays where it is not tied to such a
  count ("designate seven", never "seven of the sixteen");
- **a sentence that explains the data** (what a file is, how a field is coded, which system produced a column) or
  `"in the ZIP"` / `"See the attached ZIP"` filler;
- **a presupposition**, an ask that only parses if a subset is non-empty or a move happened ("how many and what they
  cost", "the sites where it fell"): make "none" a grammatical answer ("whether any and, if so, how many and what
  they cost") with every figure and unit kept, while a fact the requester knows before any analysis stays
  (`reduce-house-fixes` H23).

**What the client's reviewers return** (the project lead, 2026-11-09, verbatim in
`guidelines/client/project-lead-review-2026-11-09.md`): "Spelling out the methodology in the prompt. Why are we
helping the model on what they should do?"; "Naming the files that are attached... You can just say nothing at all";
"Being overly descriptive and adding unnecessary context... Prompts should be minimally sufficient to answer the
question"; "Stating who you are... They just go right into the problem." Most necessary context lives in the files,
never stated in the prompt. **The three-strike policy** runs on LLM-generated prompts: a warning and a rerun of every
model response, then one task a week, then offboarding. Draft clean, compact practitioner prose first so the author's
light voice pass (if any) starts from 0 of 9 signals rather than needing rewrites. `voice-check.py` fails a prompt
that names a file in the pack, spells out a methodology chain, or pre-diagnoses a data gap, and warns on an output
file named where a type would do or a parallel factor triplet.

Sulfur's prompt module sends a prompt back when it "names the method or the trap, warns the solver, rests on a written
procedure, allows a hedged answer, needs outside knowledge, pulls in a separate dataset or decision, or asks for more
than three files" (`guidelines/client/learning-modules/prompt.txt`). Its leaks to avoid, verbatim from the prompt
reminders: "Be careful: the nine schools were picked...", "Compare them with similar schools...", "Drop the duplicate
spring file...", "Cluster by school...". After drafting, reread the prompt as the solver and cut any sentence about
how to do the analysis, why the data are incomplete, what to exclude, or what to watch for.

**Budget.** Aim for **55 to 120 words (350 to 700 characters)**; hard ceiling is 1,000 characters. Compress per
sentence, never by deleting a requirement: one clean ask per deliverable with natural insider domain terms; cut every
explanation of data gaps or factor chains; no rounding; no role, meeting, ZIP filler, or pack inventory; ask rather
than specify. Never cut the repeated unit, the call, runner-up, gap or flip, a chart's named parts, a unit, or a
calendar boundary that defines the forward window. After each pass walk the figure list, recount the cells and rerun
`voice-check.py`.

**Variety.** Two tasks on the same pattern with the same data structure are duplicates, and in Mark the one Duplicate
the portal returned named the prompt's shell (how many, a workbook with a count-once side table, one labelled stacked
bar, nearest N), not its nouns: 182 of 186 Mark prompts ran question, deliverable, side table, chart, rounding. So
the shell is drawn with the world: the question's form from the decision (a count asks how many, a pick which, a gate
whether, an amount how much, a date when); the second sentence led by the deliverable, the rule, the date or the use
rather than "Put ... in" every time; what each file holds and
the chart's species varied (the format set is small by design, see "The deliverable formats" in section 2, so it is
never varied by adding a written document). `voice-check.py` holds corpus quotas (no question form over 30 per cent
of prompts on file, no second-sentence opener over 20, no deliverable set over 35) as a WARN.

**The client's templating checker.** The portal's pattern checker counts seven signals and marks a prompt
templated at three, borderline at two: files listed up front; steps ("First... Then... Finally"); three or
more stacked questions (two question-sentences in the opening already count); a closing one-sentence list of
documents; a dictated method ("according to the standard"); lists inside the prompt; UK spelling. Write one
question, ask for each deliverable only in the sentence that gives its reason, never close on a list of
documents, and keep every ask's definition in flowing prose. Fold a second quantity into the one
question ("judged on the bed-days each hospital's share would free") rather than asking it; prefer neutral
wording to a UK-only spelling ("with every bar showing its value", not "labelled"). Mark's task127 scored four
of seven. `voice-check.py` counts the signals and fails at two.

**The results and the asks.** The prompt makes **one to four asks, each hard and multi-faceted** (the guidelines of
11/20: "1 to 4 hard, multi-faceted supplementary asks rather than a long list of easy ones"): one sentence or one
clause per ask, in the deliverable's terms, its unit beside it and no rounding, each resolving to many figures (a
figure per member, per period, per option). A recommendation, where the decision needs one, is one quotable
sentence with its unit and rests on several results. An entity plus an aggregate names its grain. An ask a person
could act on with no result of the chain behind it is a second decision (`reduce-house-fixes` H18). The asks are
designed in `supplemental-stumping`.

**Each decisive step's answer is asked for, in the decision's words.** The critical components are the decisive
steps' answers, and "each step's answer must appear in one of the deliverables the prompt asks for" (the guidelines,
section 4), so a component the prompt never asks for cannot be graded. Ask for the quantity each stump settles as
something the decision uses: the client's hardest forecast prompt asks "how many in-scope housing and insolvency
referrals we'll get each year, and the hours a case of each kind will take from start to finish under the new
agreement", which are its two decisive steps' answers, and names neither the cohorts nor the queue. The wording
test: a hurried analyst reads the sentence and answers it with the hurried figure, learning nothing about what
needs correcting. A quantity that exists only on the golden's route (a recording share, a pull, an adjustment
factor, a restated base) is never asked for by name; where a step's own figure has no neutral name, it is a named
member's or a named period's estimate inside the ask that covers every member. A person may also ask to see the
working, once and plainly ("show how you got from the data to each figure so someone can follow every step", the
client's hardest survey prompt): it names no method and makes the path part of the deliverable.

**Every decisive step is reachable, and no convention is left unstated** (the guidelines, section 5). "A careful
analyst should reach the right answer from the prompt, the data and the docs, with no rule nobody wrote down and no
source nothing points to": each stump's evidence sits in a shipped file a careful analyst opens for the question
asked, and the note's `Decisive steps:` line says where. "If a graded figure depends on a choice the prompt and
files do not settle (what 'engagement' or 'active' means, which denominator, which window, how missing values are
filled), pin the business definition in the prompt or an input document, never the method": the definition is
filed in the organisation's own document where it can be, and stated in the prompt only where no document would
carry it.

**The author's rewrite.** The design note's `## Prompt contract` lists, line by line, what a voice rewrite may not
drop or change: the question, the threshold and hold option where there is one, every result asked for with its
unit (each decisive step's own quantity among them, marked as such, since a rewrite that drops one leaves a
critical component ungradable), every deliverable by type, the as-of date; and what it must never add (a rounding instruction, a method, a warning, an
attached file's name, a role, a count the data hold). Hand it to the author with the draft. When the rewrite comes back, it
replaces `prompt.txt`, `pipeline.json` gets `"prompt_rewritten": true`, and the gate runs in rewrite mode: every leak
rule still fails it, the voice rules only warn. Then `leak.py` again, and the four answer blocks are re-read against
the rewritten wording.

## 4. The gate

```
python3 .agents/skills/guide-to-prompt/references/voice-check.py taskNN             # exit 1 on any FAIL
python3 .agents/skills/guide-to-prompt/references/voice-check.py --file <draft> --task taskNN
python3 .agents/skills/guide-to-prompt/references/voice-check.py taskNN --rewrite   # the author's rewrite
python3 .agents/skills/guide-to-prompt/references/voice-check.py                    # batch report
```

**Draft mode fails on** (Mark's rules + platform 9-signal & AI-writing checks): not `prompt.txt`; any backtick, hash,
pipe, bracket, bullet, label-colon line, or emphasis outside a file name; a line break; no question mark in the first
two sentences; 1,000 characters or more; an em or en dash; a persona from the card's `world.people`, a title, sign-off,
board vote or reader; a sentence opening Then, Next, First, Second, Last, Finally, After that; an LLM tell (leverage,
robust, comprehensive, seamless, delve, ensure, note that, in order to, furthermore, stakeholders); two attributed
opinions; any rounding instruction (to the nearest, decimal places, whole numbers); zero or more than three
deliverables (by file name or by type); a prompt that opens by saying who is asking; a count the data hold; a file in
the pack named (by its name or its stem read as words); **a methodology chain (`"how X drives Y"`)**; **a data-gap or
metering-gap pre-diagnosis (`"lack direct metering"`, `"can't be metered"`, `"nobody counts..."`)**; **ZIP attachment
filler (`"in the ZIP"`, `"see the attached ZIP"`)**. **And on Sulfur's two leak rules:** a method, comparison or
adjustment named; a warning to the solver. It warns on a method hint word (cohort, holdout, matured, pooled, weighted,
seasonal, spillover, comparison or control group), a **parallel 3-factor inventory triplet** (AI-writing scan C/D), and
a shell class over its corpus quota.

**Rewrite mode** (`--rewrite`, or `"prompt_rewritten": true` in `pipeline.json`, which `precut.py` and `leak.py`
read too) keeps every leak rule as a FAIL (markdown, em dash, method named, methodology chain, warning to the solver,
count the data hold, deliverables, an attached file named, a stated role) and turns the voice rules (one paragraph,
question first, length, persona, sequencing, LLM tells, roll call, a rounding instruction, data-gap pre-diagnosis, zip
filler, shell quota) into WARNs. `leak.py` sweep 11 and `precut.py` run the same gate; `leak.py` sweeps 4 and 5 add the
design note's vocabulary and announcement sentences. A failing draft is not done, and neither is a rewrite that fails.

## Checklist

- [ ] Subdomain, task type, the assigned analysis type and `domain_test` fixed against the client's "what makes it
      deep" and "domain fit"
- [ ] The answer shape picked (not the last build's), the results placed in its cells, the lost ones in different cells
- [ ] The prompt pins the question, what each result is and the deliverables by type, with no rounding instruction, no
      method named, no `"how X drives Y"` methodology chain, no parallel 3-factor triplet, no data-gap/metering
      explanation, no `"in the ZIP"` filler, no attached file named, no role, and no warning
- [ ] Exact formulas and filing columns live in the organisation's governing document inside `target/`, referenced in
      `prompt.txt` by natural business name
- [ ] One to four asks, every one multi-faceted with its unit; none presupposes what the data hold
- [ ] Each decisive step's own quantity asked for in the decision's words (a hurried analyst answers it with the
      hurried figure); no quantity that exists only on the golden's route named
- [ ] The prompt read against the answer sentence by sentence (its literal reading lands on the golden); every
      decisive step reachable from the prompt, the data and the documents; every business definition a graded
      figure needs pinned in a document or the prompt, never the method
- [ ] The draft is one compact paragraph (target 55-120 words, hard max < 1,000 chars), question first;
      `voice-check.py taskNN` exits 0 with 0 FAIL and 0 WARN on the new checks
- [ ] `## Prompt contract` written and handed over; any author voice pass re-verified with `voice-check.py taskNN --rewrite`
