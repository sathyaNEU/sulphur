# Project lead review, 2026-11-09 (Vincent, Handshake AI, posted to the Sulfur channel)

Kept verbatim as the client's own review text. It sits beside `deep-reasoning.md` and
`learning-modules/stumping-strategies.md` (both exported the same day) and governs where it is newer than a skill.

---

**7:09 PM.** @channel Hi, we're again seeing a bunch of LLM-generated prompts with these main issues.

Spelling out the methodology in the prompt. Why are we helping the model on what they should do? You should not be
telling the model anything it should have to figure out itself. In fact, this will help you stump the model if you
give it less information. Most necessary context should be buried in the files rather than stated in a long prompt.

Naming the files that are attached. When you're talking with ChatGPT, do you normally name out every single file that
is attached? You can just say "see attached ZIP" or nothing at all since the files are obviously attached.

Being overly descriptive and adding unnecessary context. Most people do not spell out their life story to ChatGPT,
they are direct and straight to the point. Prompts should be minimally sufficient to answer the question.

Stating who you are. Most people don't start a question to ChatGPT by saying "I'm a product manager at Google and have
worked here for 20 years". They just go right into the problem.

We will continue the three strike policy from Mark. Two strikes if it's very severe. Expect DMs shortly.

First offense: warning by DM with clear explanations of why. You will have to fix your prompt and re-run all the model
responses. This wastes everyone's time and prevents you from doing other tasks, so please take the time to make sure
your prompt is not LLM-generated. Second offense: throttled to one task per week. Third offense: offboarded, no
exceptions since there's already been two prior warnings.

We encourage LLM assistance, but it takes ~5 minutes to rewrite the prompt in your own words. We also have this
assistant for you: https://project-sulfur.learn.joinhandshake.com/prompt-writing-test

**8:04 PM.** @channel More tasks will be released later tonight. Assessing the quality of tasks right now.

**2:03 AM.** Hey all, quick note on where we want Sulfur tasks to go, and the pattern we keep seeing.

The pattern right now: most tasks hinge on one thing. Usually it's a hidden factor built into the data: a subgroup, an
event that hits the control group, a confounder that only shows up in the units that decide the call. Sometimes it's
one clever method choice. Either way, once someone's told that one thing, the rest is routine.

Why that's a problem: it tests whether you spotted the one thing, not whether you can do real analysis. Thinking
harder doesn't help much; you either see it or you don't. And a factor you planted in the data is really just a
planted defect in a stats costume, so we will send those back.

What we want instead: tasks where the difficulty runs through the whole analysis, the way it does in real work. A
strong task makes the solver:
- figure out which of many files, metrics or logs actually matter
- stitch messy sources together (bad join keys, changing schemas, numbers that don't reconcile)
- investigate: form a hypothesis, test it, rule things out, follow the next lead
- build and check a model or forecast on data it hasn't seen
- split a change into its causes and make the pieces add up
- say how sure it is, and pull it all into a clear conclusion
- among other things, these are just examples

Each of those steps should be genuinely hard and produce something we can check. The more careful the work, the more
of it comes out right.

Examples of the shape we love:
- Not "Spot the one subgroup I made respond differently" but "Here are the logs from 40 training runs. Which ones went
  wrong, when, why, and how much did each change contribute?"
- Not "Notice the control metros got faster delivery" but "Our checkout conversion fell 8% this quarter. Bridge it to
  the causes using these event logs, release notes and traffic data, and rank what to fix."
- Not "Read section 4 the right way" but "Forecast next year's demand for each of 300 products with honest ranges, and
  tell us which forecasts we shouldn't trust and why."

Areas we especially want: root cause and debugging of complex systems (training runs, services, pipelines, fleets),
forecasting and prediction, and comparing things and explaining the difference. Answers can be a ranked list of
causes, a timeline, a forecast with bands, a breakdown that adds up to the total, or a set of flagged issues. They
don't have to be a yes or no.

We will be following up with changes: the quality checks and review process will be updated to address this;
Lovable instructions and examples will be updated with what we believe are the best current examples; new tasks will
now be assigned a task type (forecasting, root cause analysis, etc.) in addition to a domain.

Overall, I will say that people have been doing a good job, and it's natural to find one thing that works and keep
pumping them out. However, our clients want a set of diverse, varied tasks with each task teaching them something very
different, so we will be cracking down on this.

**5:04 AM.** @channel Compared to Project Mark, I think everyone has taken great efforts to make their deeper and less
reliant on a planted defect or rule application. So, I'm very proud of you all for that.

That said, after reviewing ~500 tasks, we're still seeing a lot that rely on "one fact" to trip up the model: one
thing flips the decision, and the whole task comes down to whether you find it. Usually that one thing isn't part of
the real data. It's been planted, and it doesn't look like anything a real dataset would contain.

Common versions: a duplicate or test row that changes the total, an event or subgroup built into only the units that
decide the answer, or a clause that has to be read one particular way.

We're also pushing toward deeper tasks that need real end-to-end investigation, where the difficulty runs through the
whole analysis. We don't expect every task to get there yet, but going forward we'll be rejecting tasks that rely on
just "one thing."

Examples of the tasks wanted: https://project-sulfur.learn.joinhandshake.com/examples. Prompt examples:
https://project-sulfur.learn.joinhandshake.com/taxonomy. Deep reasoning tactics:
https://project-sulfur.learn.joinhandshake.com/deep-reasoning.

Lastly, tasks will be released shortly and will be assigned a task-type now. You can pick one the same way you pick a
domain. This is to encourage more diversity since 80% of tasks followed a very similar format.
