---
name: supplemental-stumping
description: Turn the results chain into asks and price the rubric so a run scores as low as the analysis allows (the Stumped gate reads the review's strongest run against 60; a run that loses any one stump stays at 50 or under and the reflex route in the twenties). Every figure the answer blocks state sits downstream of a stump, the weight is spread across the stumps so none carries it alone, each stump keeps one figure of its own and that figure is its critical component (the client's guidelines of 11/20: the decisive steps' answers, independent, each in a requested deliverable), the asks number one to four and each is multi-faceted, reflex work is done and never stated as a graded figure, and every band comes from the variant battery; corelib.py prices every route at design and effort.py on the cut pack. Mark's measured record of what models execute (anything written down, the hygiene battery, a device whose discovery is its remedy) still binds every ask. Use after stumping fixes the core and the results chain and before data is cut, and in /fix-rubric. references/evidence.md and proven-in-production.md hold Mark's measured record.
---

# The Ask Layer

The asks are the results chain, asked for. The rubric is generated from the prompt and the answer blocks, so what
the prompt asks and what the blocks state is the rubric: every figure sentence becomes a criterion, and a run earns
each criterion its own figure lands. The ask layer cannot make a run lose a judgment (that is the core's work,
`../stumping/SKILL.md` Part 1d). It decides how many points each lost judgment costs, and how many points cost a
run nothing. Mark's record (`references/evidence.md`, cited as `evidence.md` with its part; the shipped devices with
their portal tier in `references/proven-in-production.md`) says what models execute; it is kept as the list of
things an ask must never rest on.

## Part 0. The arithmetic: what a run earns

**The split, measured.** The two generated rubrics on file (task6 architecture 6, 30 criteria; task11, 18 criteria)
both came to 100 points the same way: the recommendation one criterion of 18; the critical components 18 to 23; the
asks 50 to 55; instruction-following 9, one point per requested file, per described feature of a file or chart and
per format rule. Each figure sentence of the Critical Components and the Supplementary Questions became one
criterion (a sentence naming two members' figures became one criterion that needs both), and no criterion came from
the Step-by-Step. `../stumping/corelib.py` prices on 18, 20, 53 and 9, the figures of one sentence as one criterion
(each figure of the core carries its `sentence`); `effort.py` keeps 38, 55 and 7 so builds stay comparable with the
ones already priced.

**A run's score is what its route lands.** Every run earns the 9, so 9 is the floor. Above it a run earns the
recommendation when its call is right, and each figure whose value sits inside the band the blocks state. A frontier
run does all the reflex work right (`../stumping/references/precedents.json`), so **every figure with no stump on
its path is a free criterion**, and so is a figure a stump moves by less than its band.

**The review reads its strongest run, and that run loses fewer stumps than the platform's two.** Builds of ours that
scored 28 to 49 on the platform came back from review at 71 to 83. So the ask layer is priced on two lines, computed
at design by `generator/core.py` (corelib's rubric table, from the same lattice that proves the core) and again on
the cut pack by `effort.py`:

- **One stump lost: 50 or under, for every stump.** A run that makes every judgment but one still fails the bar
  with ten points of room. The recommendation is 18, so each stump on its own takes about 32 of the 73 figure
  points, which three stumps can only do when their figure sets overlap: most graded figures sit downstream of two
  stumps or more.
- **The reflex route: 30 or under, built for the twenties.** A run that loses every stump, or names the problem and
  declines to estimate, keeps the 9 and a handful of points.

Two more keep the client's standard ("more careful work keeps earning more"; no single sentence of help rescuing
more than a third): a stump fixed alone on the reflex route earns something (it has a figure of its own), and adds a
third of the rubric at most.

**The critical components are the decisive steps, and they are independent** (the client's guidelines of 11/20,
`guidelines/client/guidelines-2026-11-20.md` section 4). "List the two or more decisive, challenging steps and the
correct answer to each. The rubric's heaviest criteria are built from them." "Give the answer, not the method."
"Each step's answer must appear in one of the deliverables the prompt asks for." "A model that gets one step wrong
should still be able to earn the others." So on the rubric the two heaviest blocks behave differently, by design:

| Block | Points | What a run that loses one stump of three keeps |
|---|---|---|
| Recommendation | 18 | nothing where the call needs every stump; all of it where the call needs the corrections together and one alone leaves it standing (both forms are accepted, and the lattice says which) |
| Critical components | 20 | the other stumps' components, about two thirds: each component is one stump's own figure, so it falls with that stump and no other |
| Asks | 53 | the few figures the lost stump leaves inside their bands: most ask figures sit downstream of two stumps or more |
| Instruction-following | 9 | all of it |

`corelib.py` holds both properties at once: `critical components independent` (every component falls with exactly
one stump, and every stump has one) and one stump lost at 50 or under. The second is carried by the asks and the
call, never by tying the components together: a component that falls with two stumps is moved to the asks, and
where one stump lost comes out over 50 the fix is an ask figure with more stumps on its path, or a silent ask
figure cut.

**Where the points went, on the record.**

| Build | What the asks were | What the run kept |
|---|---|---|
| task6 architecture 6 | sited away from the call (releases, rollbacks, cloud cost, incident minutes) | the run off the call scored 73: the 48 points of those asks and 16 of the components; the releases and the cost were dropped ("no figure reads the SLI"), every ask was re-sited onto the stumped SLI, service by service, and the build was approved as architecture 7 |
| task11 | "deliberately separate from the call" (station loads, carbon fed), 55 points | both runs kept every gradable one; the run that declined the call still scored 54 |
| task8 | four devices whose discovery is their remedy | both runs found all four |
| task22 architecture 2, task13 architecture 5, task16 architecture 3, task1 architecture 5 | rebuilt totals, counts and bases stated in the blocks beside the estimates | 71 to 83 at review: "both rebuilt gas in close to your 1,844,373 Mcf", "the same 436 faults by year", "the link counts themselves are mechanical", "the same October 2026 base on every plan" |
| task20 architecture 4, run 2 | three stumps, each with its own results | one stump lost: an estimated 51.7 on the effort weights |
| the three approved sheets (`guidelines/client/approved-reviews-2026-11-14.md`) | the estimate, member by member (eight shares and four lifts; three netted rates; six bridge pieces) | 17, 22 and 35: the runs kept the joined counts and headline rates and nothing else; the run that named the selection and declined filed "all shares and lifts NA" |

The client's own lines agree. The rubric page: "Supplementary questions and asks: each hard ask you wrote. A wrong
analytical path should get them wrong" (`guidelines/client/overview.txt`). And the reviewers' weak mark on a level 5
task: "much of the work sits away from the deciding step" (b9efebd1).

**The paper is optimistic.** Mark measured paper ceilings of 35.1 and 39.4 that came back at 83.5, and every Sulfur
paper estimate without a run behind it came back 40 to 60 points high, because a judgment priced as lost was a
reflex. The rubric table cannot see that: it says what a lost stump costs, never whether the stump is lost. The
platform's two runs are the only measurement (`/triage-runs`).

## Part 0b. Real Holistic Audit v4 rubric math (why scores stuck at 55-65 and how to hit 30s-40s)

Holistic Audit v3/v4 revealed two massive gaps between the legacy house pricing (18/20/53/9) and real platform rubrics:
1. **Error Carried Forward (ECF) on arithmetic rollups:** On `task27` (18 pts: `avoidable EUR`, `network total`, `EUR total`, `BHV`, `HAM`, `Q3`) and `task9 arch 5` (30 pts: shares, own share, tier figures), the platform rubric gave FULL credit for derived totals/shares/currency rollups computed cleanly from a run's own wrong upstream attribution. Legacy `corelib.py` assumed 0 ECF and predicted 37 when reality was 65!
2. **One check per figure (no multi-figure sentence bundling):** v4 C1 rule 7 splits every entity and figure into its own independent criterion, with `recommend + decisive figures` at 45-55% and `IF` at 5-10%. On a disjoint 8-member scorecard where each stump moves only 2 members, solving 2 of 3 stumps leaves 75% of entities right plus IF + ECF + texture = 65+.

**The v4-hardened rules enforced in `corelib.py` (`v4_hardened: True`) to land platform scores cleanly in the 30s-40s:**
- **Zero un-stumped texture or cleaned-base figures** in Supplementary Questions or Critical Components (every single graded figure must miss its band on the reflex route: 0 silent figures).
- **Drop pure arithmetic rollups or mark them `"ecf": True`** so `corelib.py` credits them as EARNED on partial-stump routes (`v4-ECF one stump lost <= 50`, `v4-ECF two stumps lost <= 35`, `v4-ECF reflex <= 25`).
- **Build a coupled figure matrix (`>= 50%` of non-ECF ask figures downstream of 2+ independent stumps):** Instead of 1 disjoint stump per member, let 2-3 independent modeling judgments compose across every graded entity (for example, joint attribution x dose-response/partial-pooling x stratified projection or budget-constrained ranking under a cap), while each stump still keeps its own single-stump Critical Component.

## Part 1. The ask doctrine

1. **Every stated figure is downstream of a stump.** A figure the prompt asks for and the blocks state is a
   criterion; it earns its place only when the reflex route files it outside its band. An ask sited on quantities no
   stump touches (a second family of files, an input of its own, a reconstruction) is collected by the run that
   missed the call, which is the run the review reads.
2. **Spread across the stumps, never hung on one.** A core has two matrices, and they are shaped differently. The
   **call matrix** (members against stumps, the cells that flip a member across its line) is sparse: each stump
   flips a different member, which is the level (`../stumping/references/core-method.md`). The **figure matrix**
   (graded figures against stumps) is dense: a real process runs across the data, so each stump moves most members'
   figures outside their bands while flipping only the members near their lines. Every cell is one of three:
   *flips* (the effect is larger than the member's margin to its line), *moves* (larger than the figure's band,
   smaller than the margin), *silent* (inside the band: a free criterion on that route). The approved sheets are
   this shape: the raw rates were wrong on all three conditions, the pilot transfer on every share of one arm, the
   wrong counterfactual on all six bridge pieces. A figure downstream of exactly one stump is that judgment
   restated: each stump gets one of its own (Part 0's ladder), which is its critical component, and the rest are
   compound and sit in the asks. A chain where one stump
   is the only analytical input of most figures is one thing under another name (`precut.py` counts it), so the
   overlap is between independent stumps, never one stump read at many cells.
3. **Ask for what the estimate is used for.** The client's level 5 tasks ask follow-ups only the corrected
   intermediate answers (b9efebd1: the expected charge-offs among the loans still open, the older vintages on the
   same footing, the plan by funding month; 279e74f2: "Corinne's mid-October plan needs the same figure"), and
   every review of ours asked for the same thing. The kinds, each drawn from this world's own decision and never
   from a list: the estimate for every member (the whole column, never spot cells); the estimate carried one step
   further (a second date, the next period, the stock a month on, the money); the rejected or the incumbent option
   priced on the golden's footing; each member's distance to its line or its break-even; the size of what the
   record does not hold. Never name the intermediate the correction produces: an ask that names it hands over the
   decomposition (`../stumping/references/sulfur-record.md`).
   **Each stump's own figure is asked for too, in the decision's words.** A critical component has to be gradable
   in a requested deliverable, so the prompt asks for the quantity that stump settles as something the decision
   uses and every route would have to produce: "the hours a case of each kind will take from start to finish under
   the new agreement", "how many in-scope referrals we'll get each year" (example 16 asks for both of its decisive
   steps' answers this way and names neither method). The test for the wording: a hurried analyst reads the
   sentence and answers it with the hurried figure, without learning that anything needs correcting. "The hours
   corrected for the queue", "the recording share by days to the deadline" and "the restated baseline" fail it; so
   does a quantity that exists only on the golden's route. Where no neutral wording exists, the stump's own figure
   is the member-level estimate that stump alone moves (a named member's figure, a named period's), asked for
   inside the ask that covers every member.
4. **Reflex work is done, never stated as a graded figure.** Counts, joined totals, rebuilt series, cleaned bases
   and reconciliations are needed by every route and reached by every frontier run. The prompt does not ask for
   them, and the Supplementary Questions and the Critical Components do not state them; the Step-by-Step carries
   them so the reviewer can reproduce the path. The prompt asks for the estimates, never for the table they are
   built from (a 504-row balance asked for by name is 504 cells a run rebuilds). An assembly result is asked only
   where the assembly is itself a judgment a run has been seen to lose, cited like any other stump.
5. **Bands come from the battery and sit inside the stump.** Each stated figure carries the band its twelve or more
   variants span, with room, and it is stated only where every stump claimed on it moves it outside that band
   stretched by half again (a narrower miss is a near miss, which the review gives back). A band wide enough to
   hold the reflex route's figure grades nothing (task16 architecture 1: bands of 0.648 to 0.689 held every careful
   analysis). A figure whose honest band swallows the stump is cut from the blocks, never narrowed: a band that
   leaves a defensible variant outside is a fork (`determinism-check`).
6. **A committed figure for every member.** The prompt asks for the figure on every member, so a run that names the
   problem and declines to estimate is wrong on every row and not only on the call.
7. **Sentences are criteria.** One figure sentence is one criterion, all or nothing. Each sentence of the blocks is
   the deliverable's own row or line, and no sentence holds only figures the reflex route lands. In `generator/core.py`
   the figures a line states together share one `sentence` id, so `corelib.py` prices the line and never its
   figures one by one, and a component's figure restated on an ask line is listed there as well. Each file's look
   is described in one line: every described feature (a column list, a chart element, an ordering) is a point every
   run earns.
8. **No ask is won or lost on a surface cause.** A run that loses an ask to a field reading, a filed rule, a planted
   row or a formatting choice is evidence of a surface stump, and the reviewer reads where each run lost its points.
   Mess sits on the paths as texture that every careful run cleans the same way (Part 4), so a hygiene slip moves no
   graded figure outside its band.
9. **One to four asks, each hard and multi-faceted** (the guidelines of 11/20: "1 to 4 hard, multi-faceted
   supplementary asks rather than a long list of easy ones"). An ask is one asking sentence of the prompt that
   resolves to many gradable figures (a figure per member, per period, per option), every one separately gradable
   and determinate; five asks or more, or an ask that is one lookup, is a redraw of the ask layer. The
   Supplementary Questions block carries one numbered entry per ask and each entry's figure sentences are the
   criteria (rule 7), so the criterion count is unchanged: what changes is that nothing in the list is a small ask
   standing on its own.

## Part 2. What Mark measured, which still binds

Eleven Mark portal rubric figures sorted cleanly (`evidence.md`): **every ask layer at or over 70 was reachable by
executing something written down**, and every layer that held rode a reconstruction across two systems or grains
that no sentence states. Under Sulfur the asks are the results of the chain instead of data devices, but the first finding
binds every ask: nothing written down may carry an ask's difficulty. These rules are applied before an ask is
drafted:

1. **Run the pin test first.** Write every asking sentence with the pins a determinism judge will force (basis,
   grain, unit, source, window) and with the WHAT every governing document files, then ask whether each device
   still bites. If the pin names the device's dimension (196), a filed sentence states its handling (236, 114,
   187), or the frozen main-call files fix the figure (151), the device is dead at design however silent its
   rows. Devices live only in the dimensions the pins leave open: how many rows carry the quantity, which rows
   reached the file, which records are one event, which key is the true one.
2. **Demand work after the notice, and price the full includer.** The responses at 72 (151, 464) did the full
   handling the paper cracker said nobody would. Model the response that notices every problem and handles it
   the standard way, and require that it still files figures outside their bands. On Sulfur that response is the
   rigorous standard route, which corelib holds to 50 or under (Part 0), and it holds because each ask sits
   downstream of a second stump the first one's handling does not reach (Part 1 rule 2). Mark's form of it was a
   second device from another family on the same ask (151's deferred-salary reconciliation beside the catch-up
   halves; 236's two per ask). A device whose discovery and whose remedy are the same act is a work order (1.0
   below).
3. **An ask-only file does not keep an ask.** 151's injured-list asks read files the call never opened and were
   still pinned by the batting lines. Mark's remedy (site every ask on quantities the main-call files cannot
   compute) is superseded by Part 1 rule 1; the finding stands as the reason an ask sited away from the stumps is
   never safe.
4. **Give each device mass and breadth.** Every figure of its ask moves by several bins; no block that is one
   number repeated (187's ten curtailment criteria were one farm-wide number); no median that moves only when a
   mishandled row crosses a mark (118 at 87); 114 needed a 15-hour floor after a 57.
5. **Pair every pin with the device beneath it and file the WHAT in the organisation's own form before shipping.**
   The repair that closed each held layer's determinism finding without spending its device was one sentence in
   the record's own voice stating the WHAT (151's register header, 281's home timekeeper headers, 275's basis
   shown never to move the call). A device that cannot survive its convention being filed was the ambiguity
   (182 architecture 2, 39.1 claimed against 75.2 measured once the terms were defined), and shipping it buys a
   determinism return and an ask layer at once.

**1.0 A device whose discovery and whose remedy are the same act is not a device.** Noticing that eight
references each serve two stations IS noticing that the join must go through the address; the hygiene battery
performs the discovery, and cutting the narration that described it moved nothing (165, 21 of 21). Mark's
remedy was a reconstruction (a state rebuilt over time from an event log, a deduplication under a key that has to
be worked out); on Sulfur the runs do those by reflex, and the work left after noticing is an **estimator built
across records and ruled on by a referee slice** (`../stumping/SKILL.md` Part 1d), which neither shows in one fit
nor forks. The test at design time is unchanged: after the solver has noticed the problem, is there still work to
do, and can that work be done wrong?

**1.1b The blind-response test, at the draw.** For the widest graded component, score the response that applies
one obvious rate to one obvious size column, the constant response and the all-nil response, before any file
exists (190's eight-segment table was 7 of 8 reproducible from a flat rate). More than about a quarter of the
cells recoverable that way means the component measures the data's shape, and the ask's shape changes.

**1.1c The hygiene battery a careful solver runs unprompted.** A device resting on any of these is seen, never
silent, and keeps nothing (measured in-house and confirmed on the portal: 251 at 95, 118's corrections block,
464 at 72):
- exact or near-exact duplicate rows, re-sent batches, a repeated total on every line of a bulk receipt;
- a second series repeating the first one interval early (a check meter), dropped as a duplicate;
- a clock in UTC or standard time, found from a missing DST gap or an hour profile, and converted;
- carried-over or re-keyed records matched across two systems, and rows after a system's close;
- consecutive spells merged across a one-day gap; an estimate row dropped where its actual exists;
- a rescinded or reversed row removed by its rescind or credit; a withdrawn correction applied;
- a code or phase field contradicted by a parcel, plat or schedule, re-derived from the finer key;
- a visible rate code or half-price line read as the discount; a comment column read for what it says;
- **pairing a payment's halves, or a header amount to its item rows** (151 at 72, 118 architecture 4);
- **walking a dose, a rate or a state back through a change log** (464 at 72);
- **applying a per-section latest-release or latest-version rule** (118's readers block, 165, 121);
- **reconciling a remittance, a roster or a register to its filed rate or schedule** (474 v4, 176, 187).
The devices that held shared one property: the repair needed a judgment the battery does not make, about which
records are one event or which key is the true one, taken from a cardinality or an identity in the data, with
no field, comment or code announcing it.

**1.1d Three tells that hand an ask over**, screened before the pack is cut: a release note or helper line that
tells the solver a later extract stands above the published column (law 3); arithmetic exact enough to find by
inspection (five values at about fourteen times a month, rollup rows each summing to exactly three members); a
device whose two handlings both tie. A device a solver meets announced or finds by inspection is re-sited
(another file, another grain, another join in the resolution chain), never re-worded or widened.

**A fork is not a device.** A device is found only by an internal inconsistency; a fork is resolved by reading a
sentence, so closing it hands the ask to every response that reads the sentence and leaving it open is a
determinism finding (one build went 28.5 to 38.3 to 67.8 as its forks were pinned; another's whole layer was the
call's own construction and measured 65.5). **Test every ask against the pin the call needs:** if filing what
the call must file resolves the ask, the ask is that sentence read back and grades nothing. Replace it with a
consequence of the estimate that the sentence does not settle (Part 1 rule 3), still downstream of the stumps;
never move it onto quantities no stump touches (Part 1 rule 1).

**Three bans, kept.** 1 **No filed rule adjudicates a device on the ask's path, and nothing narrates one**: only an
internal inconsistency finds it (a wrong cardinality, an impossible row, a rollup above its parts). 2 **No
marker**: no batch id, source value, load stamp, flag or single column isolates device rows; blend benign rows
into every batch touched, give each classifier column a benign twin. 3 **No oracle**: no control tying only
under the golden or only on the wrong read; no identity, total, name agreement, confirming round number or
column the answer inverts from; one byte-clean referee arbitrates a designed disagreement without handing over a
level, all else ties under every handling.

## Part 3. Mark rules that Sulfur supersedes, and why

- **"No ask keyed to the call or its construction"** (Mark ban 4; 110 at 84, 464 v2), **"decoupled in
  computation"** (Mark 1.3) and **"each ask graded on an input of its own"**: in Mark a coupled ask was collected by
  every response that landed the call, so a separate device took points from it. On Sulfur a run that lands every
  stump is a returned task whatever the asks do, and the run the review reads has missed the call: what it collects
  is every ask sited away from the stumps (Part 0, task6 architecture 6 and task11). So the asks sit downstream of
  the stumps. Two halves of the old rule survive. With one stump, coupled asks are that one judgment read at other
  cells, which is the banned one-thing design, so the coupling is to two or three independent stumps (Part 1 rule
  2). And no ask hands over a construction: no "for the option you recommend" that a wrong pick can still answer on
  its own terms, no asking sentence that names the steps.
- **"An ask's device may turn on data semantics or rule application"** (Mark 2.1): Sulfur reviewers read where each run
  first went wrong, so an ask lost on a reading or a rule marks the task as a surface stump. Every ask's difficulty is
  analytical.
- **The separation line** (zero device rows in the main population): it existed to keep devices off the call. With
  devices demoted to texture there is nothing to separate; the realism rules still bind every row.

## Part 4. Mess on the ask paths: Mark's device book as texture

Mark's device families are now the Layer 1 vocabulary: realistic things systems do to records, which every careful run
cleans the same way, so they move no graded figure between careful runs. They keep their value as the record of what
models execute by reflex (so they never carry an ask) and of what reads as sabotage (so they never ship).

**The nine laws.** 1 **Unflagged** (ban 1). 2 **Split evidence**: a column the wrong path never reads plus a
corroborating file, neither enough alone. 3 **Silent** (2.3). 4 **Aimed**: each mishandling and mis-repair lands
on a stated value outside the bin. 5 **Interior**: ship the genuine population blanket exclusion destroys. 6
**Fair**: one handling reproduces truth exactly, asserted; unrecoverable truth is cut; a grader who checks
consistency knowing the golden can find and confirm the inconsistency, and the golden's handling is named in a
block 3 step only the grader reads (`submission-writeup`). 7 **No marker** (ban 2). 8 **No oracle** (ban 3). 9
**Shared real causes**: one cause may feed several devices; the pack never reads as sabotage.

Families: D1 duplication, D2 version, D3 units and meaning, D4 absence, D5 scope, D6 grain, D7 keys, D8 clocks,
D9 self-validation. The client's rigor cards (`../stumping/references/client/layer2-rigor-patterns.md`) that turn
on the data's own structure (vintages and reporting lags, point-in-time universes, censored young cohorts,
exposure denominators, incomplete recent periods, event-level quantities on every line) are device seeds in D2,
D5, D6 and D8; the seed is the structure, never the card's pin.

**Held on Mark's portal or never leaked** (now texture; listed so a build knows which ones a careful run does not see, and keeps them off every graded path unless the handling is forced and standard) (the primaries to draw from, `evidence.md` and `proven-in-production.md`
for each build):
- **Analytical rigor, a reconstruction left after noticing:** a catch-up half settled in a later period's line
  (151); terminal moves read from a prior-id chain with no dates (275); transfers dated from the arrival and
  identities left unresolved (119); orders replayed in sequence across a go-live (169); a specimen under two
  gateway keys and an infant under its mother's key (236); dwellings per supply point (162); a receipt number
  plus payer as the identity (175); a cable fault's reports on every pole of its circuit (281).
- **D8** a settlement, upload or recorded date for the event date (135, 303, 253, 304).
- **D1** the same records under two sources or key schemes where the copy is not exact (275, 447, 196, 179, 309).
- **D2** a label stored before a silent switch with a false-clean as-of join (126, 128, 253, 258, 268, 309).
- **D4** absence evidenced in a file no habitual join reaches (124, 258, 196, 464); a channel drained in stages.
- **D5** a silently partial extract; out-of-scope rows known only by structure (196, 120).
- **D6** an event's quantity on every line it covers, one grain below a total the ask asks for and allocated
  with other files (135, 124, 120); a ledger at another grain than its name.
- **D7** the true key elsewhere (another field, a reference string, a prior-id chain); codes reissued to other
  entities; an as-of join hiding the far edge; records billed to another holder after a transfer.
- **D3** units or scale set per source, date or pack; a missing currency read as the house's (303, 128, 117).
- **D9** totals invariant under the device; a control true only in its scope; name agreement lying both ways.

**Seen, reflex repair wrong**, a primary only with its over-cleaning half: keys recycled across entities so a
global dedup deletes real records; repeated keys with opposite meanings; a withdrawn correction a diligent
response applies (at most one per build); blanks missing not at random; a repair right for one population only;
a log read as a roster; dirty keys with one collision punishing global normalisation.

**Seen, repaired right** (hazards or texture): exact duplicates, re-sent batches, reprints; roll-ups inside
detail; displaced fields and drifted layouts; key formats, padding, case, invisible characters; join fan-out.

**Repetition.** Devices may repeat across builds, re-skinned by the world's own records: the label stored before
a silent switch has held in six worlds under six switch mechanisms, and the two-system cutover and the
UTC-against-local clock are the corpus's commonest organs. Only the main call's driver must be unique
(`../stumping` Part 6); an ask device is an organ. Two things still read as one author and are varied: the ask
grid (about twenty cells with a device in every cell at one build in six per lane, dimensions and ask count
drawn with the world, at least one ask not fed to the chart), and the sheet's own prose (a pair ceiling printed
without a script behind it is the author's exposure, not the solver's).



## Part 5. Each result's stops, determinism and the audit

Each result has three to five stops, complete competent pipelines at distinct values outside its band: the quick
read, the careful but hurried read (the deep class named in the results chain), the over-corrected read, the right
method on the wrong population, the answer. These are the passes `effort.py` scores. The golden sits mid-bin; a miss inside the bin needs more device mass. The ladder file comes from the
golden's code and never ships. Every figure is separately gradable, a quantity, never a treatment or device word.

**The span floor:** eight or more files and ten to fifteen columns on the golden's causal path, each file moving
the ask when misread. Split the quantity across sources, route through the resolution chain (fact, correction,
register, crosswalk, standard), separate the antidotes: hub and spoke, fixed before the spine is cut. No two asks
hang on the same single stump: each stump owns one figure, and every other ask sits downstream of two stumps or
more (Part 1 rule 2).


**Price the determinism closure before the ask is designed: on the ask side determinism and difficulty trade one
for one.** A device that is a reconstruction the records support two ways is a Gate C fork, and the closure
(naming the record, the set and the boundary in the asking sentence) files the reconstruction as a rule (157:
three closures moved the cracker's keep from 0.040 to 0.240 and the pair from 36.2 to 45.7 with no figure
moving). So the device rides rows the sentence can name without naming their handling, or the whole ask is paid
when a judge finds the fork.

**The reconciliation ask is where determinism dies.** A bridge between two totals has as many licensed readings
as there are bases that could define either total (196's settlement month against advice month moved 486,513
between quarters; 199's pack supported three bridges). The asking sentence carries the basis and the grain, the
reconciliation sits at the grain of the table it reconciles, and `checks.py` asserts the closure at that grain.
Enumerate the bases before writing the ask; one is the only acceptable number.

**A pin is paid for.** Every pin added to close a fork is paired with a silent primary underneath it (rule 5),
and the pair is **measured** on the cut pack afterwards. A pin's scope has two halves: the figures it governs and
the neighbouring figures it must leave alone, both asserted; a filed sentence's scope is stated before it is
written and its wording approved before it ships (three pins in one session each leaked something different).
Pins and devices are not substitutes: a pinned convention with a silent device under it is the shape that holds.

**Measure the forcing as a number, before the pack is cut.** For each device, compute the figure that makes the
wrong reading wrong (193's chain log ties in 148 of 148 chain-months under one reading and fails 144 under the
other) and assert it; where no such figure exists, replace the ask. An inconsistency makes a device findable, the
asking sentence's words make the figure forced, and a device needs both: a term that admits a figure reached
without the inconsistency is a fork however good the inconsistency is (182's "the quarter hours the historian did
not record"). Take the lazy answer's handhold away (rename channels after what the instrument measures, not after
the ask's words) and word the quantity so the device's rows are inside it by construction.

**The effort script** (`effort.py` on `generator/effort.json`, named on the `Measured by:` line): three passes, every
result contributing a scored figure to each, computed end to end by the generator's own code on the cut pack and
priced on 38, 7 and 55 so builds are comparable; the worst honest number in the gated field
(182 wrote 39.1 for a response that skipped the filed rules while the cracker measured 75.2). The script is read,
not just run: scoring the same stops on two passes, hardcoding a result to Missed, or a hand grade that ignores the
chain have each passed a gate that only read the sheet. Re-run it after every change, not once at the end. Cutting a figure no device reaches is
a correctness check as well as a ceiling lever (190's plain quarterly count was hiding a quarter-basis defect).

Every ask answer recomputes from the bundle, forced by the records; assert every stop and delta, recompute every
ask in the verifier, and sweep: lazy, necessity matrix, pair simulation on the cut pack, over-cleaner, oracle,
wrong-path battery, and a grep for each device's words and any organ stated twice. Repair one
device at a time, organ and records together; never delete an organ.

## Part 6. The returned-task revision

**The losses were analytical but the average reached 60** (`/fix-rubric`, from `/triage-runs`' `FIX_ASKS`, proved by
`freeze.py check --mode rubric`): read which criteria the higher-scoring run earned and why. A figure with no stump on its path
leaves the prompt and the blocks (its work stays in the Step-by-Step); a figure a lost stump moved by less than its
band is replaced by a consequence that stump moves further (Part 1 rule 3); a critical component the run got right
though it lost that component's stump is a reflex priced as a stump (a core repair), and one it got right because
it made that judgment stays (the components are independent, Part 0). A result earned because its difficulty was a reflex (the textbook method,
a plot, a holdout) is a core repair and goes to the architect. **The runs lost most of their points on one result**: the task is thin, so the fix adds
results that need their own work rather than hardening that one. Never harden by planting.

**A stopping rule checks its fallback is shippable**: "cut the layer back to what the records force" is not a
fallback where pinning the open quantities kills the results' judgments and the pair sits near the bar (Mark 182).

## Part 7. The effort sheet

The design note's `## Results chain` and `## Effort test` are the ledger `dataset-generation` builds against and
`precut.py` reads (`../stumping/references/design-note-template.md`): per result, its asking sentence's block, its
band, the hurried pass's value against the golden, and the mess on its path with the handling every careful run
applies; then the three-pass table, `Measured by:` naming `effort.py` on `generator/effort.json`, `Largest single
hint:` and `Pair estimate:` (50 or under). Builds cut under the retired design carry `## Ask sheet` with `Shallow
keep:`, `Pair ceiling:` and a cracker table, and `precut.py` reads them there.
