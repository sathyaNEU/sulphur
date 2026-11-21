# Project Sulfur guidelines (11/20), read 2026-11-21

Kept verbatim as the client's own page ("Project Sulfur guidelines (11/20)"), pasted by the author on 2026-11-21 with
the phase 2 announcement (`phase-2-announcement-2026-11-21.md`). It governs where it is newer than a skill. What it
adds to the bar of 2026-11-09 (`deep-reasoning.md`, re-read the same day and unchanged): "only one decisive step" as
a named send-back, two or more decisive and independent steps, the Critical Components block as those steps with
each one's answer, 1 to 4 hard supplementary asks, the clean-data test beside the one-fact and effort tests, and the
"Valid Stump?" field.

---

Guidelines

The main thing we are looking for is real analytical, deep-reasoning stumps.

**The bar.** Two model runs are generated from your prompt and graded against the rubric. Their average must be below
60% (exactly 60% does not pass), and the runs must lose for a genuine analytical reason, not formatting, trivia or
one hidden detail.

## 1. The basics every task needs

**A realistic request in your domain.** A real stakeholder asking for a set of results, usually with one decision on
top, written in natural prose the way you would type to a colleague. Tailored to your assigned domain, not a generic
prompt. LLM-generated prompts are rejected.

**One deterministic recommendation.** It does not have to be binary, but the final conclusion must be the only one
the prompt and data support.

**1 to 3 deliverables.** The files a real analyst would produce, with 1 to 4 hard, multi-faceted supplementary asks
rather than a long list of easy ones.

**Real, messy input files.** At least 10 usable files in at least 2 file categories, including at least 2 large,
messy files and at least 2 distractors. Build on data where the difficulty already exists. No LLM-generated files
and no file that reveals how the task was built. See Input files.

**Method left open.** The prompt pins the question, the decision, the deciding outcome or threshold and the
deliverables. It never names the method, the trap or the adjustment.

**A real golden solution.** A ZIP with the same number of files the prompt requests, business-realistic and not
LLM-looking.

**Original.** Don't template examples or your own earlier tasks. Examples show the qualities we want, not a
scaffold, prompt wording or trap to reuse.

## 2. What the stumps shouldn't be

**A planted defect or decoy.** Something wrong was put into the data (or a misleading file was added) and the whole
answer depends on noticing it. Once the model suspects it, one query finds it and one obvious correction fixes it.

Example: A clinic network asks which site has the longest wait times. One site's export contains every appointment
twice because the file was re-sent. Remove the duplicates and that site drops from first to fourth; leave them in
and it "wins".

Why it's sent back: the difficulty is noticing, not solving. Tell the solver "one file is duplicated" and the rest
is routine.

**Rule application.** A document already contains the procedure or definition that decides the answer, so the work
is finding the right sentence and following it. Finding a sentence is not reasoning.

Example: A foundation asks which of five grant applicants to fund. A "scoring standard" in the inputs lists the
scoring steps, the weights and a tie-break rule. Apply the steps as written and the winner falls out; there is no
method choice left to make.

Why it's sent back: a careful reader gets it right and a hurried one gets it wrong, but no analysis separates them.

**The shallow hidden factor.** The author builds one hidden cause into the data (a confounder, a special subgroup, a
one-off event) that sits only in the units that decide the answer, or shows up in a single table. One sentence gives
it away and one routine step (a filter, a split, one extra term) fixes it.

Example: A lender asks whether loans from 2024 default more than loans from 2022. The author edits the file so one
dealer group, present only in the 2024 loans, defaults at three times the normal rate. Told "one dealer group is
driving it", the solver filters it out and the gap disappears.

Why it's sent back: it looks like analysis, but it is a planted defect with a story attached. Real hidden factors
run through the whole dataset and need modelling to measure, not one filter.

**Data semantics.** The answer flips on reading one field, definition or time window a particular way. There is no
analysis to do once the reading is settled.

Example: A subscription app asks whether churn rose last quarter. "Active" in the data dictionary means a payment in
the last 30 days, not a login. Count logins and churn looks flat; count payments and it rose. Everything else is the
same simple count.

Why it's sent back: the task tests reading, not reasoning, and if the field is ambiguous it is not deterministic
either.

**Replay.** The task asks the solver to reproduce a number someone has already produced, by working backwards to
their unwritten method and reapplying it. Once the method is recovered, the answer is arithmetic. A close cousin:
the only twist is that a figure quoted in the brief is wrong, and spotting the mismatch decides the call.

Example: A city publishes a "neighbourhood need score" every year but never prints the formula. The task gives the
2019 to 2023 scores and asks for the 2024 ranking. The solver recovers the weights by fitting past scores, applies
them to 2024, and is done. (Cousin: a memo says the default rate is 4.1%, the files give 3.6%, and catching the gap
is the whole task.)

Why it's sent back: recovering someone else's formula, or spotting a wrong number, is a single step. There is no new
analysis that could make a careful answer better than a lucky one.

**Only one decisive step.** Even when the deciding step is real analysis, if it is the only challenging part of the
task, catching it gives the whole answer and missing it gives none. Tasks need two or more decisive steps, each
independently hard.

Example: A hospital asks whether to keep an overflow staffing agency. The one insight is that busy weeks cluster
together rather than arriving independently. Once that is modelled, the answer is a direct count of past quarters
with five or more overflow weeks; nothing else in the task is hard.

Why it's sent back: the answer is all or nothing on one step. Add a second independently hard judgment that also
moves the answer, with its own checkable figure.

## 3. What the stumps should be

One decisive step is not enough. The only challenging part of the whole task: if the model gets it, it gets
everything; if it misses it, it misses everything.

Two or more decisive, independent steps that each need real reasoning. There should be several challenging,
realistic ways for the model to go wrong, and missing one should not sink the others. The model should fail by doing
a reasonable analysis that does not go far enough, not by missing one hidden detail.

Specific lessons that have already decided many accepted tasks are closed. Check Overused stumping strategies before
you pick one.

**The tests for any stump.** One-fact test: if telling the solver one fact makes the rest routine, the stump is a
planted thing. Clean-data test: a solver that cleans the data perfectly and reads every instruction correctly should
still be able to reach the wrong answer through a reasonable but insufficient analysis. Effort test: a solver with
ten minutes, one with an afternoon and one with two days should each score clearly higher than the last.

## 4. Critical components: your decisive steps

**List two or more.** In the Critical Components block, list the two or more decisive, challenging steps and the
correct answer to each. The rubric's heaviest criteria are built from them.

**Give the answer, not the method.** "The restated 2023 baseline is $4.2M", not "restate the baseline".

**Make each answer gradable.** Each step's answer must appear in one of the deliverables the prompt asks for.

**Keep them independent.** A model that gets one step wrong should still be able to earn the others.

## 5. Also keep in mind

**Realistic mess is not the stump.** Messy data is required for realism, but cleaning it or reading it correctly
must never decide the answer. Keep most of the rubric's points on the reasoning steps.

**No unstated conventions.** If a graded figure depends on a choice the prompt and files do not settle (what
"engagement" or "active" means, which denominator, which window, how missing values are filled), pin the business
definition in the prompt or an input document, never the method.

**The prompt must not point the other way.** Read your prompt against your answer before you submit. A model that
follows your prompt's own words must not be marked wrong.

**Every decisive step is reachable.** A careful analyst should reach the right answer from the prompt, the data and
the docs, with no rule nobody wrote down and no source nothing points to.

**Vary your tasks.** Spread your tasks across the nine analysis types and vary where the hardness sits, the answer
shape and the kind of data. A reused chain of steps, question template or answer shape is templating, whatever the
topic. See Deep reasoning.

## 6. Filling in "Valid Stump?"

Answer three things for each decisive step the runs missed:

- **Where it fails:** which step the run got wrong, and what it did instead.
- **Why it's fair:** where the evidence sits in the data or docs, and why a careful analyst would find it.
- **Why it takes reasoning:** the analysis needed to get it right, and why it stays hard even once you know what to
  look for.

Example: Both runs costed the relief scheme from survey answers at face value. The evidence is in the fieldwork
data: households interviewed close to the deadline and in long interviews report fewer bills in arrears, and the
banded questions anchor on the random starting amount. Getting it right means separating the interview-length effect
from the deadline effect in one model, correcting the banded amounts for anchoring, and showing the corrected cost
against the budget. Knowing that misreporting exists doesn't give the answer; each correction has to be estimated
and shown to change the total.
