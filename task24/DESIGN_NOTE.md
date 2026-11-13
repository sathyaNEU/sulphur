# task24: which of the five Q1 2027 annotation requests Pellucid Annotation accepts at the clients' offered prices

## Draw

Subdomain: General Statistics & Data Science (Regression, classification & model diagnostics)
Analysis type: Forecasting & Predictive Modeling
Answer shape: a forecast path with bands and drivers (forecast-bands-drivers): each request's expected fully loaded cost per delivered image (or frame) with
  its 80 per cent range and its drivers (QA reviews, floor top-up, annotator paid minutes), with the accept set and the
  price each declined request would need on top
Weight: modeling: the cost of each request rests on two modelling builds the vendor's records hold only at other grains
  (QA's any-issue return and its correction chain over each image's objects, video frame time on track turnover) and a
  third the careful pass makes (each annotator-week's piece pay against the hourly floor); the last three builds sat in
  assembly (task13), a hard-to-measure quantity (task20) and synthesis (task23)
Data-native sentence: every 2026 cost the vendor paid is recorded at the grain of its own system (a task pass, a QA
  review, a worker-day punch, a worker-week pay line, an object or a track), so the cost of a request whose images are
  far denser, or whose video turns over more slowly, than any 2026 project can only be built from the grain where each
  cost is decided
People: Loice Mumo (finance lead, owns the pricing policy), Collins Mutuku (QA lead, owns the review standard), Mourine
  Kipngetich (people and payroll, owns the pay policy and the roster), Chege Ouma (payroll runs), Jeffrey Reyes (Iloilo
  centre manager); the clients' contacts Maria Osborn, Eleanor Wilson, Malte Mosemann, Wayne Carter and Jorge Berry; drawn
  with guard.py names (en_KE seeds 2411 and 2413, en_PH seed 2412, en_US seeds 2414 and 2415 for the clients)

## Stump screen

Written at the draw on 2026-11-13, before the card was registered and before any code. Each candidate went through
the nine tests of `references/stump-screen.md`; the three strongest independent ones were kept (no one sentence
rescues two of them: the first is the QA rule's arithmetic over objects and corrections, the second the pay rule's
arithmetic over annotators, the third the driver of video work). Stage 3 measured the second as a reflex (runs simulate
a rule's expected cost rather than apply it to the average unit, R53): it stays in the golden and prices nothing.

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| QA returns an image when any one object is missed, and each correction re-checks every object before another full review, so returns and re-returns both climb with the image's objects, steepest where they are small or occluded | 2026's re-return share of corrected tasks carried along the chain to images denser than any 2026 project (N04, L36, L40) | QA reviews of corrected tasks (found issues per re-review) against each image's objects, rising across every 2026 box project | none | kept |
| Annotators are paid per object with a guaranteed hourly floor settled per worker-week, so on slow work the slower annotators are topped up and the top-up per image is a hinge over the spread of speeds | 2026's top-up share of piece pay carried to slower work, or the floor applied to the average annotator (L40, N01) | payroll worker-week lines (paid hours, piece pay, top-up) against each annotator's passes in the task log | none at the draw; stage 3 measured it a reflex (R53) | kept as a reflex: in the golden, not a stump |
| Video is annotated by propagating boxes frame to frame, so frame time follows tracks entering and leaving, not objects on screen | frame time scaled by objects on screen at 2026's video rate, which fitted 2026's busy urban projects (L36, N05) | the 2026 video projects' archive (track ids per frame) against per-chunk times in the task log, with 2026's calm parking-lot project as the slice that separates the drivers | none | kept |
| The labelling tool stops its timer after 90 seconds without input, and annotators pause longer on crowded images, so tool time understates paid time most where images are dense | paid time per tool minute held at 2026's overall ratio | worker-day timesheet hours against the sum of tool time per worker-day | 1 (next to the closed card on values cut at a time limit) | dropped as a stump; kept as Layer 1 and a supporting step whose omission alone leaves the call standing |
| Each object takes longer when it overlaps others, and the crowded request overlaps far more | per-object time at 2026's average | object coordinates and per-object timestamps | 1 (the closed transport card: within-band rates carried to the target's mix), 2 (a pattern one group-by of one file shows, R14) | dropped |

## Deep reasoning

Task type: Regression, classification & model diagnostics (General Statistics & Data Science), serving Forecasting & Predictive Modeling
Domain test: each request's cost is a set of statistical objects the vendor's own records hold only at other grains: a Poisson intensity of found issues per object type aggregated into the chance an image comes back (any found issue returns it) and carried through a correction chain whose re-review intensity rises with the image's own, the expectation of a hinge (the weekly floor) over annotators' paces and weeks, and a regression of video time on the drivers the archive records (tracks starting and ending) chosen on the projects where the candidate drivers part; a careful statistician fits each at its own grain, extrapolates it by its structure past the record's support and checks it on the record's closed projects
Swap: replace the chain's structural re-review by 2026's re-return share and the turnover regressors by objects on screen and the task becomes arithmetic on 2026 averages; the results are the analysis type's own objects (an aggregated intensity carried through a chain, an expectation of a convex function, a regressor chosen out of sample), so a noun swap into another field leaves nothing to estimate
Where the weight sits: modeling, in R2 to R4: estimation builds over 390,000 task passes and as many reviews, 1,100 annotator-weeks and 250,000 archived tracks, each long rather than clever (fitting per-object rates, paces and care, the re-review multiplier, settling weeks, joining tracks to tasks)
Layer 1: duplicate punches (double taps on the clock) and shifts auto-closed at midnight with a supervisor edit the next day (the punch clock); corrections issued new pass ids with a parent link and sync retries that repeat rows (the labelling tool); the Iloilo QA desk's staff keys without a hyphen (the review system); two centres' local times, UTC+3 and UTC+8 (each centre's system); allowance and adjustment lines and one voided payroll re-run (payroll); two COCO dialects in the clients' samples (their previous vendors); projects still running at the pull carrying corrections not yet delivered (the register); none decides a result on its own
Not one thing: the strongest single piece is the QA chain (R2); a run that nails it still prices the video by objects on screen (R3), so its costing misses the parking-lot project (R5), declines Ardley and files Ardley's cost and range out of band (R6, R8, R7); a run that nails the video still carries 2026's re-return share and accepts Corvane (R2, R4, R6, R7, R9)
One-fact test: "A corrected image goes back to QA with every object re-checked, so the denser the image the likelier it comes back again" rescues R2 whole and the Corvane and Shelfgrid cells of R4, R6 and R8, 1 of 9 results whole
Not semantics: the hurried route reads every policy clause, field and unit correctly and still files wrong figures, because it carries 2026's re-return share and a per-object-on-screen rate to work they do not describe
Not rule application: the filed rules say what is counted (the cost lines, the floor per annotator per pay week, the return on any found issue, the re-review of every correction to the fourth); no filed procedure estimates per-object issue intensities, the re-review multiplier, annotator paces or the video drivers, and executing every rule on 2026's averages files the hurried answer
Estimand: the pricing policy (section 2 the expected cost per delivered image and its lines, section 3 the staffing basis, section 4 the acceptance line at 1.18 times that cost and the lowest acceptable price), the pay policy (piece rates, corrections unpaid, the floor settled per annotator per pay week), the QA review standard (an image returns on any found issue, every correction is reviewed again, at most four reviews), the requests for quotation (volume, unit, offered price)
No decoy: nothing in the pack argues an answer; the requests carry only each client's offered price, volume, unit and specification
No replay: no result re-derives a published figure; R1 rebuilds 2026's cost from the records and closes it on what payroll paid
Pinned: each result's rivals run on the cut pack (issue intensities with and without the annotators' care spread or with a lighter prior on care; the floor with and without week-to-week variation, clocked or contracted weeks; the video flow with and without track ends; reviewer time by centre or pooled), every one inside its band and filing the golden set
Run forecast: R2 method shortcut, R3 method shortcut (the video), R4 method shortcut (carried from the chain), R5 self-confirming check, R6 to R9 method shortcut; runs earn R1 and the floor's settlement by reflex
Strategy label: UNTESTED (no client strategy in references/sulfur-strategies.md carries this chain)
Depth level: 4: two independent judgments (the QA chain, the video driver), each necessary and neither sufficient; the floor is a third judgment the careful pass makes; the shortcuts land on six distinct wrong sets
Lesson: a cost defined on a joint condition across an item's parts, compounded through a chain that re-applies it, or driven by flows rather than stocks, is computed at the grain where each condition is decided and extrapolated by its structure where the target leaves the record's support; no build on file teaches either deciding lesson

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | April to October 2026 delivery cost as payroll settled it (piece pay, floor top-ups, reviewer pay, overhead) | assembly-reconciliation | the pay register's annotator-week and reviewer-week lines, the punch clock, the pricing policy's cost lines | USD 192,217 within 0.5 per cent | method shortcut is not made here: the careful run rebuilds it by reflex (Right) | - | Ask 4 |
| R2 | QA reviews per delivered image for each request | modeling | the QA review standard and the 2026 reviews against each image's objects | Corvane 2.86 (2.72 to 3.01), Shelfgrid 2.29 (2.18 to 2.40), Ardley 1.20 per task, Brindle 1.08, Kestrin 1.07, each within 5 per cent | method shortcut: a logistic first-pass return on the counts with 2026's re-return share (0.24) carried along the chain (Corvane 2.23, Shelfgrid 2.10) | independent: the request samples and the 2026 reviews | Ask 2, Component 2 |
| R3 | annotator paid minutes per delivered image (per frame for the video) | modeling | the tool's pass times, the punch clock, the archive's tracks | Corvane 54.4, Shelfgrid 38.8, Brindle 22.0, Kestrin 2.4 minutes; Ardley 0.341 a frame; each within 5 per cent | method shortcut: the video on frames and objects on screen (Ardley 0.608 a frame) and corrections at 2026's re-return share (Corvane 47.1) | independent: the request samples | Ask 2, Component 3 |
| R4 | floor top-up per delivered image for each request | modeling | the pay policy's floor per annotator per pay week and the pricing policy's staffing basis | Corvane 0.763, Shelfgrid 0.390, Brindle 0.421, Ardley 0.0005, Kestrin 0.006; within 20 per cent or USD 0.005 | method shortcut: the floor settled right but on the chain's too few corrections and the video's too many minutes (Corvane 0.516, Ardley 0.0081) | R3 | Ask 2 |
| R5 | each closed 2026 project's costing beside its actual cost per delivered image | validation | R1's actual costs and the costing applied to each project's own images and annotators | P26-0446 1.48, P26-0441 1.55, P26-0434 0.0186 a frame, each within 5 per cent; within 6 per cent on 23 of 24 closed projects | self-confirming check: the hurried costing holds within 6 per cent on 17 of 24 closed projects and misses the parking-lot video by 119 per cent (0.0416 a frame) | R1 | Ask 3, Component 4 |
| R6 | each request's expected cost per delivered image (per frame for the video) | forecasting | the pricing policy's cost definition | Corvane 5.94 (5.69 to 6.17), Shelfgrid 4.24, Ardley 0.0285 a frame, Brindle 1.65, Kestrin 0.31, each within 3 per cent | method shortcut: the hurried components (Corvane 4.95, Shelfgrid 3.99, Ardley 0.0430 a frame) | R2, R3, R4 | Ask 1, Component 1 |
| R7 | the requests to accept (offered price at least 1.18 times the expected cost) | synthesis | the pricing policy's acceptance line | accept Shelfgrid, Ardley and Kestrin; decline Corvane and Brindle | method shortcut: accepts Corvane and declines Ardley | R6 | Recommendation |
| R8 | each request's 80 per cent range on its expected cost | uncertainty | the request's sample resampled (images; the video's sequences whole) | each endpoint within 6 per cent: Corvane 5.78 to 6.11, Shelfgrid 4.13 to 4.34, Ardley 0.0275 to 0.0295, Brindle 1.61 to 1.69, Kestrin 0.30 to 0.32 | method shortcut: ranges drawn around the hurried costs (Corvane about 4.8 to 5.1) | R6 | Ask 1 |
| R9 | the lowest acceptable price for each request to decline (1.18 times its expected cost) | synthesis | the pricing policy's acceptance line | Corvane USD 7.01, Brindle USD 1.95, each within 3 per cent | method shortcut: no price for Corvane, which the hurried pass accepts, and one for Ardley it should not need | R6 | Ask 5 |

Carry-forward: R1, R2 and R3 stand alone on the requests' samples and the 2026 records; R4 uses R3's minutes (a run with the wrong minutes loses R4 only where they are wrong); R5 uses R1's actuals; R6 to R9 fall with the components, so each component is graded on its own

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| returns and re-returns rising with objects per image and their small and occluded share (any found issue returns an image; a correction re-checks every object) | constructed by the process: per-object slips by size and occlusion on every first pass and every correction of every 2026 project, the rule filed in the QA standard | no: every 2026 box project shows it (corrected tasks' re-return rises with objects per image across 21 projects, correlation 0.97); the requests go further than any of them | modelling: per-object issue intensities with each annotator's care fitted across 390,000 reviews, a re-review multiplier fitted on the corrections, both aggregated per image | modelling | keep |
| the floor binding on slow work (top-ups settled per annotator per pay week) | constructed by the process: every annotator's pace and week-to-week variation on every project, the rule filed in the pay policy | no: 2026 top-ups fall on weeks of every one of the 31 projects (8 per cent of piece pay overall) | modelling: paces from the task passes, weeks from the punch clock, settled per week; the careful pass does it (R53) | modelling | keep (a reflex) |
| video time following tracks starting and ending, not objects on screen | constructed by the process: the propagation tool's time on every task of every video project | no: all six 2026 video projects; the parking-lot project separates the drivers | modelling: archive tracks joined to tasks, regressors chosen across projects | modelling | keep |
| corrections still open at the pull on projects that run to the end of the extract | real by construction of the window: a project's cost so far includes images not yet delivered | no: every project running at the pull carries it | reading the register's end dates against the extract's end | none: R5 is graded on closed projects | benign |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 April to October 2026 delivery cost as payroll settled it | Missed | Right | Right |
| R2 QA reviews per delivered image | Missed | Partly | Right |
| R3 annotator paid minutes per delivered image (per frame for the video) | Missed | Partly | Right |
| R4 floor top-up per delivered image | Missed | Partly | Right |
| R5 each closed 2026 project's costing beside its actual cost per delivered image | Right | Partly | Right |
| R6 each request's expected cost per delivered image (per frame for the video) | Missed | Missed | Right |
| R7 the requests to accept (offered price at least 1.18 times the expected cost) | Missed | Missed | Right |
| R8 each request's 80 per cent range on its expected cost | Missed | Missed | Right |
| R9 the lowest acceptable price for each request to decline | Missed | Partly | Right |
| Roughly | 1 of 9 | 3.5 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "A corrected image goes back to QA with every object re-checked, so the denser the image the likelier it comes back again"; rescues 1 of 9 results
Pair estimate: 43.5

## Stump factorial

Reflex route: per-object time with each annotator's pace (R14, R26), paid time per tool second from the punch clock by centre (R01), reviewer time per object (R14), the 2026 cost rebuilt on payroll (R57) and the floor settled per annotator per pay week as an expected cost (R53) set right; the QA chain as a logistic first-pass return with 2026's re-return share along the chain and the video on frames and objects on screen set hurried; it accepts Corvane, Shelfgrid and Kestrin and declines Ardley and Brindle, which misses the call

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| J1 the QA chain: per-object issue intensities aggregated per image, each correction's re-review at an intensity in proportion to the image's own, to the fourth review | stump | a logistic first-pass return on the counts with 2026's re-return share (0.24) along the chain | L40, L36 | accepts Corvane, Shelfgrid, Ardley and Kestrin (Corvane 4.95 under its line of 5.47) | accepts Shelfgrid and Kestrin, declines Ardley; rescues R2 | no: the intensities, the care spread, the re-review multiplier and the chain are an estimation build, and the request's images leave the record's support |
| J2 the floor settled per annotator per pay week as an expected cost over paces and weeks | reflex | - | R53, R47 | same call | - | - |
| J3 video time on tracks starting and ending | stump | frame time on frames and objects on screen | L36, L42 | accepts Shelfgrid and Kestrin only (Ardley 0.0430 a frame over its line of 0.0331) | accepts Corvane, Shelfgrid, Ardley and Kestrin; rescues none whole | no: tracks joined to tasks and the regressors chosen across projects |
| J4 per-object time with each annotator's pace | reflex | - | R14, R26 | same call | - | - |
| J5 paid time per tool second by centre from the punch clock | reflex | - | R01, R57 | same call | - | - |

Level: 4: two necessary stumps, neither sufficient, the single drops on two distinct wrong sets; the shortcuts land on six

## Data provenance

Source: generated by task24/generator from a simulation of Pellucid Annotation's delivery process (weekly rota, the labelling tool's passes, QA reviews and correction chains, the punch clock, payroll settlement, the video delivery archive) and the clients' sample labels
Behaves like the real thing: pace and slips vary by annotator and week, slips rise with small and occluded objects and faster annotators slip more, a correction's re-check of every object brings new slips, projects differ in density and mix, holidays and part-time schedules shape the weeks, new hires are slower in their first weeks, video propagation makes time follow tracks entering and leaving, QA returns follow the any-issue rule, payroll settles the floor per annotator-week
Genuine patterns: (1) annotator pace and care heterogeneity with week-to-week variation and a pace and accuracy trade-off; (2) project-level object density, size and occlusion mixes across scene types; (3) each centre's public holidays, absences and part-time schedules; (4) new hires' learning in their first weeks; (5) video turnover differing by scene; (6) correction chains lengthening with density
Problems by process: duplicate punches from double taps and shifts auto-closed at midnight with a supervisor edit (the punch clock); corrections issued new pass ids with a parent link and sync retries repeating rows (the labelling tool); the Iloilo desk's unhyphenated staff keys (the review system); two local times (each centre's system); allowance and adjustment lines and a voided re-run (payroll); two COCO dialects (the clients' previous vendors); open correction chains on projects running at the pull (the register)
Breadth: about 390,000 task passes and as many reviews over 31 projects, 30 annotators and 10 reviewers over 30 weeks, six video projects with about 250,000 archived tracks, five requests with their samples; choosing which records answer which cost line is work

## Template check

Chain signature: assembly-reconciliation, modeling, modeling, modeling, validation, forecasting, synthesis, uncertainty, synthesis
Question form: which: which of the requests to accept under the pricing policy, the honest form for a set over a filed line (the shell quota's WARN is answered here)
Nearest build: task1 v5 (with task14 v3 and task20 v4 on the shape or the weight) shares the answer shape and the weight (a forecast with drivers, modeling) but prices a subscription rise through each plan's response; this one prices delivery cost through a QA chain over each image's objects and a video driver, with no response to price
House lesson: non_additive_aggregation also sits on mark114 v1 (demand taken only when parties share a site, so adding sites leaves it out) and task7 v11 (a season's peak of coincident units replayed night by night); here the joint condition is QA's any-issue return over one image's objects, compounded through a correction chain that re-applies it and extrapolated past the record's support, with no union of sites and no coincidence across units
House shell: a set over a filed line is the decision's own form (each request is accepted when its offered price clears 1.18 times its expected cost); the five live builds on the form differ in every deciding lesson
Abstraction sentence: none writable: no build on file turns on a joint condition across an item's parts compounded through a chain, or a flow driver chosen against a stock driver

## Frontier check

Precedents: R2 L40, L36; R3 L36, L42; R4 L40, L36; R5 L28, L37; R6 L40, L36; R7 L40, L36; R8 L40, L36; R9 L40, L36 (the same ids on each result in generator/effort.json)
Shallow path checks: R2's logistic first-pass return reproduces 2026's first-pass returns at every density and its constant re-return share reproduces 2026's re-returns overall; both are refuted only on corrected dense images (the re-reviews' found issues against each image's objects), and the request's images sit mostly beyond 2026's densest bin; a logistic of the re-return on the counts over-extrapolates (Corvane 3.45 reviews, Shelfgrid 2.86, declining Shelfgrid), and 2026's rates read from density bins and carried to the request's density mix land low (Corvane 2.36 reviews, cost 5.19, accepting Corvane); R3's frames-and-objects-on-screen model fits the busy urban and plaza video and is refuted only on the parking-lot project (the archive's tracks against the task times); R5's hurried costing holds on 17 of 24 closed projects and misses only the extremes
Assumption made false: that a corrected image comes back at 2026's average rate and that video time scales with objects on screen; false because the QA standard has the annotator re-check every object of a returned image (re-returns climb with objects) and propagation makes video time follow tracks entering and leaving; tested in the QA reviews of corrected tasks and the archive's tracks
Forcing: each request's line is its offered price over 1.18; the golden sits 8.4 per cent above Corvane's line, 8.1 per cent below Shelfgrid's, 13.9 per cent below Ardley's, 9.5 per cent above Brindle's and 11.6 per cent below Kestrin's; the six golden-family variants and the six perturbations (per-object time 5 per cent, issue intensities 10 per cent, paces 4 per cent, each way) file the golden set, and every shortcut files a wrong one (six distinct sets), all in generator/effort.json
Noun swap: skeleton.py check finds severity none against everything on file and the client's corpus (nearest task9 v3, task4 arch 12, task7 v11); what carries across is the common set over a line and the common shortcuts on distinct wrong answers
Closed strategies: neither deciding lesson is on the client's page; the nearest card is transport (a pooled rate carried to a target with a different mix, fixed by within-band rates reweighted to the target): that fix is a recorded shortcut here and lands wrong (2026's density-bin rates carried to Corvane's mix file it at 5.19 against its line of 5.47), because the request's images leave the record's support and only the structural chain extrapolates; the video fix changes the regressor, not a mix; the idle timer (next to the card on values cut at a time limit) is a supporting step whose route leaves every call standing

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | delivered image | every image of the request, each accepted by QA before hand-over | every image (all are delivered) | the pricing policy's definition; same call |
| SF2 | per frame for the video request | per frame or per 25-frame task | per frame, the request's own unit | the request for quotation prices per frame |
| SF3 | expected cost | mean, median or a percentile | the mean over the request's images and the annotators who would work it | the pricing policy names the expected cost |
| SF4 | floor top-up | per annotator per pay week, per day or per month | per annotator per pay week | the pay policy's settlement clause |
| SF5 | who works the request | both centres in proportion to contracted hours, or by headcount | contracted hours of the annotators on the roster at the costing date with the skill | the pricing policy's staffing basis |
| SF6 | QA reviews | first reviews only, or every review including re-reviews | every review | the QA review standard reviews every correction again |
| SF7 | overhead | per paid hour of annotators and reviewers, or per image | USD 1.55 per paid hour of both | the pricing policy's cost lines |
| SF8 | April to October 2026 | pay weeks 6 April to 1 November, or calendar months | the pay weeks in the register | the pay register's weeks; same call |
| SF9 | 80 per cent range | the expected cost's uncertainty from the sample, or the spread of single images, or the staffing drawn at random | the expected cost's uncertainty from the request's sample | the ask ranges the expected cost and the pricing policy names the staff; the call rests on the expected cost alone, same call |
| SF10 | corrections | paid as new pieces or unpaid | unpaid | the pay policy |
| SF11 | lowest price at which we could accept | 1.18 times the expected cost, or cost plus a margin | 1.18 times the expected cost | the pricing policy's acceptance line |
| SF12 | each 2026 project's actual cost per delivered image | cost so far over images delivered so far, or the cost of delivered images only | cost so far over delivered images, graded only on projects closed before the pull, where the two agree | the register's end dates; same figure on closed projects |
| SF13 | a reviewer's pay week | local Monday to Sunday at the reviewer's centre, or UTC | local, as the pay policy's week | the pay policy's week; the reviews carry UTC stamps and each centre's offset is in its punch clock and task-pass times; same call |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: each request's images or frames (the request's volume); 2026 projects from the register; C1 |
| 2 | Unit of account: per delivered image, per frame for the video (the requests' units); filed |
| 3 | Attribution window: pay weeks 6 April to 1 November 2026; passes and reviews dated in them; C1 |
| 4 | As-of dating: the roster at the 6 November pull for who works the requests; filed |
| 5 | Version basis: rates and floors as filed for 2026 apply to 2027 work (the pay policy has no 2027 change); filed |
| 6 | Denominator: delivered images of the request; filed |
| 7 | Weighting: annotators by contracted hours; filed |
| 8 | Window length: the whole extract; nothing graded moves with it |
| 9 | Boundary inclusivity: a pass belongs to the pay week of its submission; nothing decided at an edge |
| 10 | Rounding path: none filed; figures carried unrounded to the answer blocks' precision |
| 11 | Tie-break: none needed (no request sits on its line) |
| 12 | Maturity and censoring: corrections open at the pull sit on projects still running; R5 is graded on closed projects; C1 |
| 13 | Order of operations: cost lines summed per image then averaged; same as averaging each line; C1 |
| 14 | Row order: no result depends on file order; asserted |
| 15 | Duplicate resolution: sync-retry repeats of a pass drop; double-tap punches collapse to one; the tool's re-queued passes keep their parent link; C1 |
| 16 | Identity normalisation: staff ids carry the centre prefix in every system; the Iloilo desk's unhyphenated keys map to the roster's |
| 17 | Netting against gross: allowances and adjustments sit outside the cost lines (pricing policy); filed |
| 18 | Dimensional units: seconds in the tool, hours on the clock, USD in payroll; units in the headers |
| 19 | Code and status semantics: pass type, review decision and punch flags carry their own values; never the stump |
| 20 | Integerisation: none |
| 21 | Clause scope: the floor applies to every paid hour of the week; filed |
| 22 | Forward window contents: the requests' samples stand for their images (each request states its sample is drawn from the full set); filed |

## Literal reader

The pricing policy executed word for word gives each request's expected cost per delivered image as piece pay, the floor top-ups payroll would pay for the work (settled per annotator per pay week, as the pay policy files), reviewers' paid time at their rate, and overhead per paid hour; with the QA standard's any-issue return, its re-review of every correction to the fourth review, the requests' samples and the roster's contracted hours it produces the golden costs, and the acceptance line (offered price at least 1.18 times that cost) produces the golden set: accept Shelfgrid, Ardley and Kestrin, decline Corvane and Brindle

## Prompt contract

May not drop or change: the opening that no request has been worked so the answer rests on an estimate from the April to October 2026 records; the question (which requests to accept under the pricing policy); each request's expected cost per delivered image, per frame for the video request, with an 80 per cent range; the annotator paid minutes, QA reviews and floor top-up per delivered image behind it; each 2026 project's actual cost per delivered image beside the costing's figure; the April to October 2026 delivery cost as payroll settled it; the lowest acceptable price per image or frame for any request declined; a spreadsheet and a short note
Must never add: a rounding instruction, a method or its words (any missed object, re-check, re-return, per annotator-week, tracks, turnover, back-test, compare), a warning, an attached file's name, a role or who is asking, the number of requests

## Leak review

- leak.py answer figures, pricing_policy_FIN-POL-04.pdf (USD 1.55 per paid hour, 1.18 times the expected cost): harmless, the policy's own filed overhead rate and acceptance line, the WHAT the prompt's "under our pricing policy" points to; neither is an answer figure
- leak.py vocabulary, annotator_pay_policy_2026.pdf (object, record, annotators): harmless, the pay policy's own nouns (a piece rate per object, paid hours, annotators); it files the floor per pay week and names no estimation step
- leak.py vocabulary, pricing_policy_FIN-POL-04.pdf (projects, record, annotators): harmless, the staffing basis and the sharing of a week's pay across projects by tool time, filed so R1 and R5 have one allocation; no method
- leak.py vocabulary, qa_review_standard_QA-STD-03.pdf (objects, missed, object): harmless, the return on any missed object and the re-check of the whole returned task are the standard's filed rule (what a return and a correction are); the step the call turns on, fitting the re-review intensity and carrying the chain past the record's support, is not named
- reader, question 4, the pay register's period totals sheet: harmless, the workbook's own monthly summary, reconciled to the weekly sheets once the voided re-run nets out; its gross carries allowances and adjustments the pricing policy leaves out, and R1 also needs the overhead on paid hours
- leak.py prompt gate, the question form quota: the decision's own form (which requests to accept); the author rewrites the prompt for voice

## Tried and rejected

- 2026-11-13, at the draw: per-object time rising with overlap as a stump (dropped: it is the closed transport card's fix and a pattern one group-by shows); the tool's 90-second idle timer as a stump (dropped: next to the closed card on values cut at a time limit; kept as Layer 1 and a supporting step).
- 2026-11-13, stage 3, the QA stump as the any-issue aggregation alone, priced against 2026's return share by scene type: died on the honest careful column. A logistic of the first-pass return on the six object counts (a pattern one join and one group-by show, R14) reached Corvane and Shelfgrid within 5 to 7 per cent and the call. The stump moved to the correction chain (a correction re-checks every object, so the re-review climbs with the image's own intensity), with the corrections' re-check slips and effort set to what a whole-image re-check costs across every 2026 project.
- 2026-11-13, stage 3, the floor as a stump priced against 2026's top-up share: died. Settling the floor on the request's own paid time gets Brindle right, and runs simulate a rule's expected cost (R53). It stays in the golden as a reflex.
- 2026-11-13, stage 3, Corvane at 104 objects an image: the transport fix (2026's density-bin rates carried to the request's mix) reached the call by 0.7 per cent. Moved to dense junction and market scenes (about 125 objects, more occluded), most images beyond 2026's densest bin, where only the structural chain extrapolates.
- 2026-11-13, stage 3, the 80 per cent range with the staffing resampled: it put Corvane's range across its line. The pricing policy names the staff, so the range resamples the request's sample only (the video by whole sequence).
- 2026-11-13, stage 3, R5 graded on a project still running at the pull (P26-0458): its actual cost carries open correction chains and forks on whether undelivered work counts. Graded on three closed projects instead.
