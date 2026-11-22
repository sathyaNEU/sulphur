# Finding a level 5 core in an hour

`../SKILL.md` Part 1d says what a core has to be and `stump-screen.md` says what kills a candidate. This file is the
other half: how the architect finds three sharp, independent stumps quickly, and proves them before anything is
built. The proof is `generator/core.py` ending on `corelib.run(spec)` (`../corelib.py`), which prints the core table
and `CORE PASS level 5`, `level 4` or `CORE FAIL`; `precut.py` runs it. Nothing here solves a task: it is arithmetic
on the architect's own world.

What it cannot do: tell whether a run will lose. Only the platform's runs and the review measure that. It makes the
design claims exact and checkable, and it removes the shapes that were returned.

## 1. What level 5 is: an exposure matrix

Read the client's five level 5 tasks (`guidelines/client/depth-scale-2026-11-09-detail.md`), the three approved
sheets and our four approvals side by side and one object explains all of them. Put the members of the call (or the
lines a figure is read against) down the side and the judgments across the top; each cell is how far that member's
figure moves when that judgment is made the hurried way.

- **Level 5**: three or more judgments, each with a cell large enough to flip a different member, so each shortcut
  files a different wrong answer and no one sentence repairs more than its own column. The client's words for it:
  "four different shortcuts each name a different territory"; "each shortcut gives a different wrong call: the
  pooled curve launches all sizes, payoff as censoring holds the product".
- **Level 4**: two such columns.
- **What we shipped and had returned**: a matrix with one live cell. Several stumps in one row (task1 v5), or rows
  that another route fills in for free (task16 v3's delivery log, task13 v5's confirmed signatures).

Where the matrix comes from is the whole method: **members differ in how they reached the record**. One arm has a
different feedback prompt, one condition has no dated item, one vintage is young, one territory's list is the
riskiest quarter of its shops, one group answers a follow-up that stands for the people who did not answer. Because
the observation process differs across members, an observation judgment bears on some members and not others, and
the matrix fills itself. A world whose members were all observed the same way cannot give level 5; change the world.

**A second matrix prices the rubric** (`supplemental-stumping` Parts 0 and 1). The first matrix is about the call
and is sparse: one flip per column, in different rows. The second has the graded figures down the side (each
member's own figure, each stump's own figure, the consequences the prompt asks for) and is dense: the process
behind a stump runs across the data, so it moves most members' figures outside their bands and flips only the
members near their lines. Each cell is one of three: *flips* (the effect is larger than the member's margin to its
line), *moves* (larger than the figure's band, smaller than the margin), *silent* (inside the band, a criterion that
route earns free). The level is counted on the first matrix; the score a run takes home is read off the second. A
core that is level 5 on the first and sparse on the second is what came back from review at 71 to 83: the run lost
one stump, and with it one member's figure and the recommendation, and kept the rest. `corelib` prints both and
prices every route: a run that loses any one stump earns 50 or under, the reflex route 30 or under (built for the
twenties), the rigorous standard route 50 or under, and each stump fixed alone earns something and a third at most.

## 2. The hour

**0 to 10 minutes: the decision and its members.**
- Four to eight members, each graded, read against a line the organisation would really hold (a policy threshold, a
  budget, a cap). A one-figure call has one member and is not drawn (`../SKILL.md` Part 3.4).
- The golden outcome is mixed: some members act and some do not, so no blanket call ("all", "none", "the biggest")
  is right, and the retreat's default is wrong on some member.
- Choose the member axis so that it lines up with a difference in how records are made (channel, arm, cohort,
  instrument, site system, reporting route). Write that difference down first; it is the source of every column.
- Leave one or two members far from their line under every route. They are texture, the runs earn them, and they
  stop the call from reading as "everything flips".

**10 to 25 minutes: the identity and the five questions.** Write each member's figure as an identity in the
organisation's own quantities (a level times a share times a rate, a stock plus flows, a difference of two
conditional means). For every factor of the identity ask:

| Axis | The question | The hurried route it invites |
|---|---|---|
| who | Which units are in the record for this factor, and does being in it depend on the factor itself? | the recorded units taken as all units |
| what | What does the stored value measure: the event, a report of it, a proxy, an algorithm's output? | the stored value taken as the event |
| when | When was it observed against the event's own clock, and has the unit finished? | the value at observation taken as the final value |
| against | What will a rigorous run compare or calibrate it against, and is that comparison exchangeable here? | the units, periods or sample the pack offers taken as the control |
| unit | At what unit or support is it recorded, against the unit the decision is made on? | the record's grain taken as the decision's |

Each honest "the record does not hold that" is a candidate. Write five or more. Then run
`python3 .agents/skills/fingerprint/skeleton.py closed` and `skeleton.py open`: a candidate whose mechanism and fix
are a closed card's is a supporting step at most, and the open list shows which lessons no accepted task teaches.
Keep candidates on different axes: two judgments on different axes cannot be rescued by one sentence, which is the
one-fact test passed by construction.

**25 to 35 minutes: four routes and a referee, on paper, per candidate.**
- the **hurried** route (what the factorial calls the hurried choice);
- the **direct** route: the pack's most direct evidence read raw;
- the **rigorous standard** route: what the strongest run builds, done properly, with the ingredients the pack
  really ships (never a strawman: task1 v5's careful route got two reflexes wrong and priced a one-trick build as
  level 5);
- the **golden**: an estimator constructed across two or more records in three or more dependent steps;
- the **referee**: the slice where the hidden quantity is known or bounded, which the target does not reach.

Kill on sight: the rigorous route equals the golden (a reflex); no referee exists without filing the method
(unforced, and the repair will turn it into a rule); the golden is a join, a filter or a re-key; the problem named
out loud leaves one step. Keep the three that sit on different axes and bear on different members.

**35 to 55 minutes: `generator/core.py`.** Standard library and numpy, seeded, a few hundred lines:
1. the world's process on arrays, with the observation process generating what each file will hold (so every
   estimator below reads only what ships);
2. the truth per member, the golden estimator, and one function per route;
3. the lattice: every member's figure with each subset of stumps made the hurried way (each alone, all together, all
   but one), which is also the routes sheet the golden workbook will carry;
4. the variant battery: twelve or more defensible rebuilds of the golden's conventions, returning every graded
   figure and not only the members' (each figure's band is what its variants span);
5. the referee: the golden's figure and each rival's on the slice;
6. the graded figures (`figures`): two to five critical components, one per stump and each that stump's own
   answer (it falls when that stump is lost alone and is earned when any other is: the client's page of 11/20,
   "a model that gets one step wrong should still be able to earn the others"), and the ask figures (every member's
   figure, and the consequences the prompt will ask for, which fall with two stumps or more), each on the same
   lattice keys and on the rigorous standard route; a figure that falls with two stumps is listed as an ask, never
   as a component; figures the blocks will state in one sentence share a `sentence` id, because the generated
   rubric makes one criterion of the sentence and it needs every figure on it;
7. `sys.exit(corelib.run(spec))`.

**55 to 60 minutes.** Copy the printed tables into the note's `## Stump core` (the rubric table under `Earns:`).
Write each stump's sentence said out loud and count the steps left. Read the figure matrix for silent cells: a
figure the reflex route still lands is cut from the asks or replaced by a consequence the stumps move further.

## 3. Dialling the numbers without cheating

The order matters; a core dialled in the wrong order passes the checker and fails the review.

1. **Sizes from the process, never from the line.** Set the observation process the way the real one behaves (a
   feedback propensity of 54 per cent on bad outcomes and 10 on good, a follow-up subsample of one in three, a
   reverse-answer rate of 11 to 16 per cent). The approved sheets' shortcuts sat two to four times away from the
   golden because the process was that strong, not because a line was moved to meet them.
2. **The battery before the margins.** Run the twelve variants first and read the family's spread per member. A
   spread too wide for the design is cured with more units or a longer history, never by removing variants.
3. **Then place the members, not the line.** The line is the organisation's and is the same for everyone; what the
   architect sets is each member's true level. For a member a stump opens: its distance to the line sits above the
   family's spread with room, and below the stump's worth less that spread. For a forced member: far outside every
   route.
4. **Keep the flips apart and the moves wide.** Every cell has three numbers: the stump's effect on the member's
   figure, the figure's band (its family's spread with room) and the member's margin to its line. On the member a
   stump opens, the effect is larger than the margin. On the other members it sits between the two: under the
   margin, so two stumps never flip one member and the level holds, and over the band by half again, so the figure
   is still lost and the rubric takes it. An effect inside the band is a free criterion; raise it through the
   process (a stronger propensity, a longer lag) or drop the figure from the asks, never by narrowing the band.
5. **Opposite directions.** Where the world allows it, let stumps push different members different ways (one
   shortcut over-acts, another under-acts). Then "apply every correction" is not a blanket instruction either, and
   the single drops land on distinct wrong calls.
6. **No constant the files do not hold.** Every number the golden uses is in the brief's `Files:` or measured from
   what ships. The checker cannot see this one; task7's balance points are why it is here.

`corelib` refuses: a golden that misses the truth's call; a battery under twelve or one that moves the call; a
reflex route that lands; a stump that does not move its own member, is worth under three times the family's spread,
or reaches the call when fixed alone; an open member the direct or the rigorous route files right; fewer than two
distinct wrong answers; no referee, a referee a rival also passes, or one that covers the target; a stump that is
one step from its figure once named, or that cites a reflex. And on the rubric: no graded figures listed, or fewer
than two critical components; a critical component that falls with two stumps or with none, or a stump with no
component of its own (`critical components independent`); a band that leaves one of its own variants outside; a
run that loses one stump still earning over 50; the reflex route earning over 30; the rigorous standard route
unpriced or earning over 50; a stump whose fix alone earns nothing (no figure of its own) or over a third.

## 4. What makes a stump sharp

A stump holds against the strongest run when all five are true. Write the five answers beside each kept stump.

1. **The wrong route is attractive.** It reproduces a figure someone already holds, or it passes its own check: a
   placebo, a hold-out from the same source, a reconciliation that closes. A wrong route that fails its own
   back-test is found by the run.
2. **The right route needs a commitment.** The estimator rests on an identifying assumption the run has to state
   and stand behind, with the referee as its evidence. Runs avoid that: they name the assumption and wave it
   through, or decline to estimate (L43, L44, L53). The prompt asks for a committed figure, so declining is wrong.
3. **The evidence is in another record at another grain.** No plot or group-by of one file shows it.
4. **The correction is not a constant.** Its size or its sign differs across members, or its own check breaks on one
   of them, so it cannot be applied once and carried.
5. **It has a graded figure of its own, and it moves most of the others.** A run that skips it loses that figure,
   the member, and every compound figure downstream of it.

And one test of the whole core: read the three said-out-loud sentences together. If a run handed all three still
has an afternoon of construction left, the core is deep; if the three sentences are the solution, it is three
things to notice.

## 5. Depth inside one stump

Level is not only the count of stumps. Each kept stump is itself a short chain, and the chain is where partial work
earns partial credit:

1. build the units the estimator needs (a link, a classification, an exposure) from records that do not share a key
   or a grain;
2. fit the piece the referee can score, and score it;
3. re-estimate on the part of the population the referee does not reach;
4. carry the result to each member through the member's own mix, state or schedule;
5. bound the member where step 2's check cannot be run.

Three of these five or more per stump, each leaving a figure in the workbook.

## 6. Never the same core twice

The method generates from this world's identity and its five answers; it never starts from a task on file.
- After `CORE PASS`, write the skeleton and run `skeleton.py check`; the three approved sheets, the client's
  examples, the depth-scale tasks and our own lineage are all in the comparison.
- The axes, the member geometry, the referee's kind and the arrangement of checked, bounded and broken members are
  each drawn fresh. Two builds of ours with the same three axes in the same roles, the same kind of referee and the
  same decision form are one skeleton, whatever the nouns.
- A lesson can come back. A structure cannot.
