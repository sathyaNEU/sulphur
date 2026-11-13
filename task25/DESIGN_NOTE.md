# task25: which of Saukko Labs' H1 2027 pretraining runs will not finish inside the GPU windows reserved for them, and how much longer than the benchmark each run will take

## Draw

Subdomain: General Statistics & Data Science (Benchmarking and ablations)
Analysis type: Comparative Analysis & Explanation
Answer shape: bridge: for each H1 2027 run, the throughput benchmark's days bridged cause by cause to the expected
  days with an 80 per cent range, against the run's reserved window, with the late set and each late run's fix on
  top; the 2026 bridge from benchmark days to actual days is the record each cause is measured on
Weight: modeling: every cause has to be built at a condition no 2026 run reached (the slowest of up to a thousand
  data-parallel ranks on a long-document mix, best-fit packing on a long-form mix, hall B held past its contracted
  power for two months); the last three builds sat in modeling (task24), measurement (task20) and a hard-to-measure
  quantity (task7), so the weight repeats task24's (guard WARN): the answer shape (a bridge, not a forecast with
  drivers), the decision form and every lesson but one differ
Data-native sentence: every 2026 throughput figure is recorded at the grain of the system that produced it (a
  50-step interval of one run, one rank's share of a profiled step, the documents of one packed sequence, a
  five-minute reading of a hall's draw, one work order), and each H1 2027 run sits at a data-parallel width, document
  mix, packing rule or hall load no 2026 run reached, so its days can only be built at the grain where each cause is
  decided
People: Pia Kuosmanen (head of training infrastructure, whose workbook and note the golden are), Esa Airaksinen
  (chairs the compute committee that holds the H1 2027 reservations), Marja Laine (data team lead, owns the 2027
  mixes); drawn with `guard.py names --geo FI --seed 2511`. None appears in the prompt.

The world. Saukko Labs Oy, a fictional Espoo AI lab, trains its own Kide family of dense language models on two
leased GPU halls at Pohjoisvirta Datacenters' Kaivola campus: hall A (H100) and hall B (H200, larger, leased on a
contracted IT load below its full-load draw). The infrastructure team benchmarks every model configuration on a
64-node slice with a synthetic packed corpus before the compute committee reserves blocks and windows for the half
year; the 2027 reservations were sized on those benchmarks. The 2026 record holds about sixty runs' step logs,
profiled per-rank step timings and packing logs for a sample of runs, interruptions, node allocations, the provider's
five-minute hall draw and work orders, and the 2027 roadmap, configs, data mixes and works calendar.

## Stump screen

Written at the draw on 2026-11-13, before the card was registered and before any generator code; the numbers were
prototyped on scratch arrays (`scratchpad/proto/proto1.py` to `proto3.py`). Each candidate went through the nine tests
of `references/stump-screen.md` (1 off the closed page, 2 not a reflex, 3 nothing filed, 4 clean data, 5 two
records, 6 the waved-through assumption with its precedent, 7 a plausible shallower story, 8 across the data, 9 worth
the call). Three are kept; no one sentence rescues two of them (the first is the arithmetic of the slowest rank, the
second of a packing rule's padding, the third of a hall's power contract).

| Candidate trap | The assumption a run waves through (precedent) | The second record that refutes it | Tests failed | Kept |
|---|---|---|---|---|
| Documents are packed with document masking, so a sequence's attention cost grows with the square of its documents' lengths, and every step waits for the data-parallel rank whose sequences cost most; the 2027 long-context runs put long-document mixes on few sequences per rank and many ranks, while runs with many sequences per rank average the spread away | per-rank cost carried at the run's mean (the attention FLOPs of the mix), or attention at full context for every token (the textbook MFU formula), or the 2026 per-rank spread read as hardware jitter (N04, L22, L26, L36) | the profiled 2026 runs' per-rank timings joined step by step to the packing log's document lengths; the 2027 manifest's length mix and each run's data-parallel width and sequences per rank | none | kept (S1): the mean misses the few-sequence runs, the full-context formula overstates the many-sequence runs, so each formula is wrong on different runs |
| The 2027 long-context recipe keeps documents up to the context length whole and fills sequences best-fit from a shuffle buffer; a long-form mix with many documents between half and full context and few short ones to fill the gaps pads about a sixth of every step, and the token budget counts only real tokens | every sequence taken as full, 2026's fill carried (N04, L36) | the Q4 2026 extension runs' packing logs (fill per sequence under the same rule at lighter mixes) against the 2027 manifest's length histogram | none | kept (S18) |
| Hall B is leased on a contracted IT load below its full-load draw; when the hall's draw passes it, the provider's power manager lowers GPU power limits hall-wide and every job's step stretches with the excess; the 2027 reservations hold hall B full through February and March | a run's throughput taken as its own, the provider's hall telemetry set aside as facilities data (L38, L15, L01) | hall B's five-minute IT draw against the 2026 step logs' intervals (the days hall B passed its contracted load), and the 2027 reservation map | none (1: not the closed spillover card: no comparison is contaminated; the response is a capacity threshold measured where it was crossed) | kept (S3) |
| The provider's major works in 2025 and 2026 ran well past their planned hours; the 2027 calendar books a cooling upgrade in hall B and a network re-cabling in hall A inside reserved windows | works at their planned hours (N22, N03, L46) | the provider's 2025-26 work orders (planned against actual hours, by type) against the 2027 calendar | 9 (worth a day or two on the windows that hold them; one sentence leaves one routine step) | kept as a supporting result (each window's days lost to works), its route alone leaving the call standing |
| A cooling fault in hall A's row 6 from September 2026 slowed its nodes by about a fifth under sustained load (they passed the short burn-in), until the December repair | a passed burn-in taken to certify the node (N11) | per-rank timings, node allocations and the provider's incident log | 8 and the hidden-factor screen (a constructed factor one cross-tab shows; one sentence leaves one routine step) | dropped as a stump; kept as Layer 1 and a component of the 2026 bridge (repaired before 2027, so a pooled 2026 factor carries it wrongly into 2027) |
| A run spanning both of hall B's pods sends its gradient reduction over the spine and overruns the backward window that hid it inside one pod | the 2026 flat scaling to 512 nodes carried past the pod boundary (N04) | the network acceptance benchmark against the profiled backward windows | 2 (a filed benchmark the runs turn into a bandwidth calculation by reflex, R40), 9 (the size turns on the collective's design, a fork) | dropped |
| A reserved block's few hot spares run out when failed nodes wait for vendor repair, and the job stalls | spares always available because the 2026 shared pool never ran short | node failure and repair logs against the block's spare count | 9 (the stall is a Poisson tail whose fitted mean moves it by half: no forcing) | dropped |

## Deep reasoning

Task type: Benchmarking and ablations (controlled evaluation, isolating component effects): the infrastructure
  team's throughput benchmark is the controlled evaluation, and the work is isolating each component of the gap
  between it and production runs, measuring each on the record where it is decided and carrying it to runs at
  conditions the benchmark and the record never reached
Domain test: each result is the analysis type's own statistical object: an expected maximum over data-parallel
  ranks of a compound per-rank load (order statistics of a sum whose terms are quadratic in document length), the
  expected fill of an online best-fit packing process under a heavy-tailed length mix, a threshold response estimated
  on the intervals a hall crossed its contracted power (with the meter reading the cap, so the excess is rebuilt from
  the allocation record), interruption rates and their cost, an overrun distribution from comparable works, and a
  bridge whose items add to the gap
Swap: "the long-context runs need 15 per cent more days because each step waits for the rank whose sequences hold
  the long documents" read with warehouse nouns ("each wave waits for the picker whose orders hold the bulky items")
  keeps a max over parallel workers but loses the packing process that sets each worker's load, the benchmark it is
  bridged from, the cap read off a metered hall and the token budget a padded sequence does not count; the chain
  stops making sense outside a synchronous data-parallel trainer
Where the weight sits: modeling: R3 (the per-rank cost model fitted on two joined records and the expected maximum
  simulated at each 2027 run's own width, sequences per rank and mix), R4 (the loader's best-fit packing replayed on
  the 2027 length sample) and R5 (the throttle response measured on 2026's capped intervals once their excess is
  rebuilt, then replayed on hall B's 2027 load day by day) are each a model built and checked on its own record
Layer 1: the trainer's step counter restarts at zero after some resumes (a v2.3 logging fault) and the logger
  re-sends its last buffer after a restart, so step-log rows repeat; three runs were renamed at a resume (the
  registry carries both names); the provider's hall meter and work orders are in Helsinki local time while every
  Saukko log is UTC; the hall meter drops intervals during collector outages; checkpoint sizes are logged in GiB by
  the trainer and GB by the storage system; a cooling fault slowed hall A's row 6 under sustained load from 14
  September to its repair on 19 October 2026; none decides a result, each cleaned the same way by every careful run
Not one thing: the strongest single piece is R3; a run that nails it still has to measure the padding of best-fit
  packing on the scientific mix (R4), rebuild hall B's excess and its throttle (R5), cost the interruptions (R6) and
  the works (R7), and bridge 2026 (R2), and it still files the scientific run and the three hall B runs wrongly
One-fact test: the most useful single sentence is "each step waits for the data-parallel rank whose sequences hold
  the long documents"; it rescues R3 and the long-context runs' verdicts inside R8 and R9 for two of the nine
  results' weight, leaving R2, R4, R5 and R7 and four of the seven late runs to their own work
Not semantics: every field, unit and clause read correctly (the token budget counts real tokens, a window runs from
  00:00 UTC on its first day, the meter is the hall's IT load) still leaves the reflex route at every run fitting:
  the hurried figures come from carrying a mean, a fill and a run's own throughput to conditions that change them,
  not from a reading
Not rule application: no filed procedure computes a run's days; the reservation terms file what a window is, what
  counts as finishing and that freed nodes run backfill, and every remaining step (the per-rank cost model, the
  maximum over ranks, the packing fill, the excess and its response, the interruption cost) is estimated
Estimand: the reservation terms file each run's window (00:00 UTC on the first reserved day to 00:00 UTC on the day
  after the last), that a run finishes when the trainer has counted its token budget of training tokens (padding
  excluded), that the committee's test is whether the expected finish falls inside the window, and that a block's
  nodes stay busy to the window's end (backfill after an early finish); the data dictionary files a run's GPU-days
  held (allocated nodes times eight times the wall-clock hours from launch to final checkpoint, restarts and waits
  included) and the 2026 population (every run in the registry launched in 2026); the prompt asks for expected days,
  an 80 per cent range, the finish date, and the 2026 bridge from benchmark-implied GPU-days to GPU-days held
No decoy: nothing in the pack is written to carry a wrong answer; the benchmark file is the team's real measurement
  of each configuration on its own harness (synthetic corpus, 64-node slice, an idle hall), reproduces exactly by
  its stated method, and answers a shallower quantity; the asks price it on the golden's footing (each run's
  benchmark days and its bridge to expected days)
No replay: no result re-derives a published figure; the benchmark days are the bridge's starting point, not a figure
  to reproduce, and no stated number in the pack is wrong
Pinned: rivals run on the clean truth in `generator/rivals.py`: the per-rank cost model fitted per context or
  pooled, the maximum by simulation or by a normal approximation, lengths resampled from the 2027 sample or drawn
  from a fitted lognormal, the throttle as linear, quadratic or piecewise in the excess, interruptions per node-day
  by hall or pooled with a node-count term, the works overrun as the mean or median ratio by type; every run's
  verdict holds under each, every figure inside its band
Run forecast: R3 lost to a method shortcut (the mean rank, or the full-context FLOPs formula, or the 2026 per-rank
  spread read as hardware jitter: stopped at the first story); R4 lost to a method shortcut (2026's fill carried);
  R5 lost to dismissed own evidence (the provider's hall meter set aside as facilities data, or the flat top read as
  the hall's draw); R7 lost to a method shortcut (planned hours); R2 lost to stopped at the first story
  (interruptions plus hardware stragglers); R8 and R9 lost as an unfinished chain on every late run but the controls
Strategy label: UNTESTED (own: no client strategy bridges a throughput benchmark to production runs at conditions
  never run; the machine-learning strategies 1 to 4 are loss and evaluation curves)
Depth level: 5: three independent stumps (S1 the slowest rank, S18 best-fit padding, S3 hall B's throttle), each
  necessary alone and none sufficient; the shortcuts land on distinct wrong late sets (none late; four; six; three;
  one; five), the works overrun a supporting step that moves no verdict alone
Lesson: a benchmark measures throughput at the conditions it ran (a short synthetic mix, 64 ranks, an idle hall, a
  sequential packer), and production days come from the conditions a run meets: a model learns to bridge a
  controlled measurement to a deployment cause by cause, each cause measured where it is recorded, rather than
  carry one ratio; no build on file teaches the slowest-rank maximum, a packing process's fill or a capped meter's
  rebuilt excess

## Results chain

| ID | Result (checkable) | Area | Pinned by | Band | Hurried analyst | Depends on | Graded as |
|---|---|---|---|---|---|---|---|
| R1 | the 2026 ledger: GPU-days held by the 2026 runs (total and by hall), reconciled to the scheduler's allocation record | assembly-reconciliation | the data dictionary's GPU-days held and 2026 population; replayed and renamed rows resolved | exact to 0.5 per cent | narrow look at broad data: replayed rows counted or renamed runs split, 2 to 4 per cent off (made right by reflex, R01) | independent: allocation record | Ask 3 |
| R2 | the 2026 bridge from benchmark-implied GPU-days to GPU-days held, by cause (mix attention, slowest rank, padding, hall B throttle, row 6 cooling, interruptions and restarts, works, residual) | decomposition-attribution | the stated attribution order in the answer blocks; each cause measured on its own record | each item within 10 per cent of its own size or 300 GPU-days, the total exact | stopped at the first story: the gap filed as interruptions plus hardware stragglers, the throttle and the mix left in a residual | R1 | Component 4, Ask 3 |
| R3 | the per-rank cost model (the attention coefficient) and each 2027 long-context run's slowest-rank overhead over its mean rank | modeling | the profiled 2026 runs' per-rank timings joined to the packing log; each run's config (ranks, sequences per rank) and the 2027 length sample | overhead within 3 points | method shortcut: the mean rank (the mix's attention FLOPs) or the full-context formula; per-rank spread read as hardware jitter | independent: traces, packing log, 2027 sample | Component 1, Ask 2 |
| R4 | each best-fit 2027 run's packing fill (real tokens per sequence position) | modeling | the 2027 configs' packing rule and the 2027 length sample; the Q4 2026 packing logs | within 1.5 points | method shortcut: full sequences, 2026's 99.8 per cent carried | independent: 2027 sample and rule | Component 2, Ask 2 |
| R5 | hall B's throttle response (step-time inflation at each excess over contract) and each hall B run's mean inflation in 2027 | missingness-measurement | hall B's five-minute meter, the allocation record and the 2026 step logs; the 2027 reservation map and the pool's 2026 busy share | response within 2 points at the 2027 excess; each run's inflation within 2.5 points | dismissed own evidence: the hall meter set aside as facilities data, or its flat top read as the draw, so no excess is seen | independent: meter, allocations, step logs, reservation map | Component 3, Ask 2 |
| R6 | interruptions per 2027 run and the days they cost (lost work since the last checkpoint and restart time) | modeling | the 2026 interruption log by hall and node-days; the 2027 configs' checkpoint interval | within 15 per cent of the cost | method shortcut: one pooled rate per GPU-day with restarts at their median (made right by reflex, R07, R30) | independent: interruption log | Ask 2 |
| R7 | days lost to provider works in each 2027 window that holds them | forecasting | the 2025-26 work orders (planned against actual hours by type) and the 2027 calendar | within 0.35 days | dismissed own evidence: the notice's planned hours taken, the 2025-26 work orders' overruns set aside | independent: work orders, calendar | Ask 2 |
| R8 | each 2027 run's expected days from its window's start to its token budget, its 80 per cent range and finish date | forecasting | R3 to R7 on each run's config, budget and window | expected days within 3 per cent; range ends within 5 per cent | method shortcut: benchmark days at each run's mean rank with interruptions and planned works, so the long-context, scientific and hall B runs come out 10 to 45 per cent short | R3, R4, R5, R6, R7 | Ask 1, Ask 2 |
| R9 | the runs that will not finish inside their windows, with the days each is short | synthesis | the reservation terms' test (expected finish inside the window) | exact set; days short within 3 per cent of the window | method shortcut: every run filed as fitting | R8 | Recommendation, Ask 1 |

Carry-forward: R1 stands alone on the allocation record and R2 on 2026's own records, so a run that slips in 2027
loses neither; R3, R4, R5, R6 and R7 each stand on their own inputs and are graded run by run, so a slip on one
cause costs only that cause's cells and the verdicts it decides; R8 and R9 fall with the causes they rest on, and
only for the runs those causes reach (R3's errors reach the long-context runs, R4's the scientific run, R5's the
hall B runs), so no one slip costs more than four of the ten verdicts.

## Hidden factor record

| Factor | Real or constructed | Only in deciding units | Found by | Fix depth | Verdict |
|---|---|---|---|---|---|
| Attention cost quadratic in document length, with each step waiting for the slowest data-parallel rank | constructed by simulating the trainer's own cost and the synchronous step | no: every 2026 run carries it at its own size (overheads of 1 to 12 per cent in the profiled runs) | modelling: per-rank timings joined to the packing log, a cost model, then the maximum simulated at each 2027 run's own width and mix | modelling | keep |
| Best-fit packing pads a mix with few short documents | constructed by simulating the loader's packing rule | no: the Q4 2026 extension runs pack under the same rule at 96 to 99.8 per cent | modelling: the rule replayed on the 2027 length sample | modelling | keep |
| Hall B's contracted IT load below its full-load draw, with the provider throttling GPU power hall-wide past it | constructed by simulating the provider's power manager | no: every hall B job on 2026's 40 capped days carries it, at rebuilt excess up to 23 per cent | modelling: the excess rebuilt from the allocation record (the meter reads the cap), the response fitted, the 2027 load replayed | modelling | keep |
| Provider works run past their planned hours | constructed from the provider's work-order process | no: every 2025-26 major work order | a targeted comparison of planned against actual hours by type | routine once told | keep as a supporting step (moves no verdict alone) |
| Row 6 cooling fault, September to October 2026 | constructed | no: every hall A job on row 6 nodes in those weeks; repaired before 2027 | a targeted query of per-rank timings by node | routine once told | keep as Layer 1 and a 2026 bridge item; no 2027 effect |

## Effort test

| Result | Quick pass | Careful but hurried | Thorough |
|---|---|---|---|
| R1 2026 ledger | Missed | Right | Right |
| R2 2026 bridge | Missed | Partly | Right |
| R3 slowest-rank overhead | Missed | Missed | Right |
| R4 packing fill | Missed | Missed | Right |
| R5 hall B throttle | Missed | Missed | Right |
| R6 interruptions | Missed | Right | Right |
| R7 works | Missed | Partly | Right |
| R8 expected days | Missed | Missed | Right |
| R9 late runs | Missed | Missed | Right |
| Roughly | 0 of 9 | 3 of 9 | 9 of 9 |

Measured by: .claude/skills/stumping/effort.py on generator/effort.json
Largest single hint: "each step waits for the data-parallel rank whose sequences hold the long documents"; rescues 1 of 9 results (R3; the verdicts it touches inside R8 and R9 stay lost to the other causes)
Pair estimate: 44.4 (measured by effort.py on the cut pack, every careful loss cited; quick 7.0, thorough 100)

## Stump factorial

Reflex route: every reflex set right (the hygiene battery on the logs; each run's benchmark days reproduced; attention
  corrected for each run's own document mix at its mean; interruptions priced per node-day by hall with lost work and
  restart time; the works calendar's planned hours subtracted) and every stump hurried (each rank at its mean cost,
  every sequence full, each run's throughput independent of hall B's load); it files every 2027 run as fitting its
  window, against the golden's seven late runs (kide-13b-code-lc32, kide-34b-lc64, kide-8b-lc64, kide-34b-sci,
  kide-120b-v1, kide-34b-v3, kide-34b-16k)

| Judgment | Kind | Hurried choice | Evidence | Dropped alone from the golden | Fixed alone on the reflex route | One routine step once told |
|---|---|---|---|---|---|---|
| S1 each step waits for the slowest data-parallel rank, whose load is quadratic in its documents' lengths | stump | the mean rank (or the full-context FLOPs formula, which files kide-13b-lc32 late) | N04, L22, L26, L36 | four late (kide-120b-v1, kide-34b-16k, kide-34b-sci, kide-34b-v3): the three few-sequence long-context runs fit | three late (kide-13b-code-lc32, kide-34b-lc64, kide-8b-lc64); the scientific and hall B runs still fit; rescues 1 of 9 | no |
| S18 best-fit packing pads the scientific mix | stump | every sequence full | N04, L36 | six late: kide-34b-sci fits | one late (kide-34b-sci); rescues 1 of 9 | no |
| S3 hall B throttled past its contracted load from February to April | stump | each run's throughput its own; the meter set aside | L38, L15, L01 | four late (kide-13b-code-lc32, kide-34b-lc64, kide-34b-sci, kide-8b-lc64): the three hall B runs fit | three late (kide-120b-v1, kide-34b-16k, kide-34b-v3); rescues 1 of 9 | no |
| S4 works at the overrun record, not the plan | stump | the notice's planned hours | N22, N03, L46 | same call | no run late; rescues 1 of 9 | yes |
| J5 interruptions and restarts by node-days | reflex | (made unprompted) | R07, R30 | - | - | - |
| J6 each run's benchmark days and its own mix's mean attention | reflex | (made unprompted) | R18, R40 | - | - | - |

Level: 5: three necessary stumps (S1, S18, S3), none sufficient alone, their single drops on three distinct wrong late
  sets; S4 is a supporting step whose drop leaves the call standing

## Data provenance

Source: generated by `generator/` from a simulated process: Saukko Labs' scheduler and trainer, its data loader's
  packing, the cluster's failures and restarts, the colocation provider's power manager and works, and the 2027
  roadmap
Behaves like the real thing: the trainer's step is the slowest data-parallel rank plus an exposed remainder (the
  synchronous all-reduce of data-parallel training, the straggler pattern ByteDance's OSDI 2025 study measured from
  sequence-length imbalance); attention cost follows the square of each document's length under document masking;
  best-fit packing without truncation pads as the 2024 packing studies report; GPU throughput falls with the power
  limit the way hall-level power capping behaves (Facebook's Dynamo, power oversubscription); interruptions arrive
  at node-level hardware rates with restart costs like the Llama 3 report's; provider works overrun their plans
Genuine patterns: (1) throughput per GPU falls with model size and context length and rises with sequences per rank;
  (2) hall B's research pool follows a weekly cycle (busy weekdays, lighter weekends) and a summer lull; (3) node
  failure rates differ by hall and fall after the first months of a node's life; (4) every run shows a restart
  sawtooth of lost work since its last checkpoint; (5) loss falls along each run's own schedule (logged, unused by
  the call)
Problems by process: step counters reset at some resumes (a trainer logging fault in v2.3); the logger re-sends its
  last buffer after a restart (repeated rows); three runs renamed at a resume; provider files in Helsinki local time;
  meter intervals dropped during collector outages; GiB in the trainer and GB in storage; row 6's cooling fault
Breadth: fifty-three 2026 runs over two halls and 1,536 nodes, eleven 2027 runs, thirty-one files in five formats;
  choosing which of the step logs, traces, packing logs, meter readings, allocations and work orders carry each cause
  is itself the work

## Template check

Chain signature: assembly-reconciliation, decomposition-attribution, modeling, modeling, missingness-measurement,
  modeling, forecasting, forecasting, synthesis
Question form: which (which runs will not finish inside their windows), with how much (each run's days against the
  benchmark's)
Nearest build: (guard WARN on chains shared in shape or weight with task19, task2, task3, task4 and task9: none of
  them bridges a measurement to production at conditions never run, and the weight here is modeling against their
  assembly, measurement and synthesis) task24 (General Statistics, modeling weight, a set over a per-unit line on distinct wrong answers):
  its lessons are a QA any-miss product over objects, a pay floor's hinge and video track turnover in an
  annotation vendor's costs; here a maximum over parallel ranks, a packing process's fill and a capped meter's
  rebuilt excess bridge a benchmark to production; the answer shape (a bridge against a forecast with drivers), the
  decision form and every mechanism differ. Abstraction sentence against it: none writable without naming the
  mechanisms, which share nothing

## Frontier check

Precedents: R3 N04 (a model's transfer to a new range named and left untested), L22 (the published formula whose
  generating assumption the data contradict: the FLOPs-per-token formula assumes every sequence costs the same),
  L26 (a plausible shallower story passing its own checks: the per-rank spread as hardware jitter), L36 (a transfer
  fitted on the pilot's range carried to faster duties); R4 N04, L36; R5 L38 (a record carrying the effect's modifier
  set aside as unrelated), L15 (a response assumed instead of measured), L01 (the decisive quantity measured then set
  aside); R7 N22, N03, L46; R2 L26; R8 and R9 inherit their causes' ids
Shallow path checks: the reflex route back-tested on the 2026 runs reproduces their held GPU-days within 6 per cent
  run by run (2026 ran at narrower widths, lighter mixes, a sequential packer for nearly every run and 31 capped
  days in hall B), and the pooled benchmark-to-held ratio (1.066 over 2026) passes a leave-one-run-out check (L37); the checks of
  another kind: the per-rank timings joined step by step to the packing log (a rank's time follows the square of its
  documents' lengths, not its token count, which is identical across ranks), the Q4 2026 packing logs' padding
  against the 2027 length sample (another grain: documents, not runs), hall B's meter against the allocation record
  (the meter is flat at the contract on the days the allocation says the hall wanted more, and every hall B job's
  steps stretch with that excess)
Assumption made false: "throughput measured in 2026 carries to 2027 at each run's FLOPs" (N04): the 2027 long-context
  runs pair heavier mixes with fewer sequences per rank and more ranks, the scientific run's packer pads, and hall B
  is reserved past its contracted power for two months, each tested in its own record (traces with packing logs; the
  length sample; meter with allocations)
Forcing: the line is each run's window; the golden keeps every late run at 1.148 to 1.162 of its window and every
  fitting run at 0.833 to 0.841; eight rival constructions (the attention coefficient at the lowest and highest run's
  fit, lengths from a fitted lognormal, another packing seed, a normal approximation to the slowest rank, a
  straight-line throttle, the median works overrun, hardware stops pooled over halls) file the same seven; the
  shortcuts file none (the benchmark, the careful but hurried route, the pooled 2026 ratio) or a wrong six (the
  full-context formula); each fitted input moved by its defensible spread (the attention coefficient, the throttle
  response, interruption rates and the works ratio by 20 per cent each way, the pool's busy share by 0.1) leaves the
  late set unchanged, and the world's own replay files the same seven with every run's days within 4 per cent
  (asserted in `checks.py`)
Noun swap: nearest by `skeleton.py check` is task7 arch 11 (severity none): its decision form (one of a few options)
  and answer pattern (no single correction clears) differ, its lessons share non_additive_aggregation only through a
  seasonal coincidence of chargers, its mechanisms, detection and file roles do not carry; task24 (severity none)
  shares the lesson key and the common pattern, nothing else
Closed strategies: the call turns on S1 (non_additive_aggregation, off the page); the nearest closed card is "Units
  vary more than the stated error" and the fix differs: no alert bar is widened, the maximum over ranks is computed
  from a cost model and a packing process; S3 is not the spillover card (no treated-control comparison is
  contaminated: a capacity threshold is measured where it was crossed) and not the measurement-limit card (the meter
  is not censored: the hall really drew the contract, and the excess is rebuilt from the allocation record, not
  bounded); S18 is a packing process's fill, untouched by the page; no closed lesson is kept even as a supporting
  step (the row 6 fault and the works overrun are Layer 1 and a supporting step on open ground)

## Semantic fork table

| ID | Term or convention | Readings | Golden | Ruled out by |
|---|---|---|---|---|
| SF1 | a run's days | wall-clock from the window's start to the token budget; GPU-days; compute days without interruptions | wall-clock days from 00:00 UTC on the first reserved day | the reservation terms' definition of finishing and of a window; the prompt's "date it would finish" |
| SF2 | token budget | real tokens counted by the trainer; sequence positions including padding | real tokens | the reservation terms and the data dictionary (the trainer counts non-padding tokens) |
| SF3 | inside the window | expected finish on or before the window's end; finish with 80 per cent probability | the expected finish | the reservation terms' test |
| SF4 | benchmark days | tokens over the benchmark's tokens per GPU-second times the run's GPUs; with an interruption allowance | without any allowance | the benchmark file's own definition (a measured rate) and the bridge's starting point; same call |
| SF5 | GPU-days held (2026) | allocated nodes times eight times launch-to-final-checkpoint hours; GPU-hours the trainer was stepping | allocated, launch to final checkpoint | the data dictionary's definition |
| SF6 | 2026 runs | every run launched in 2026; only completed runs; only pretraining | every run launched in 2026 | the data dictionary's population; same call on the 2027 verdicts |
| SF7 | the 80 per cent range | the 10th to 90th percentile of the run's days; a confidence interval for the mean | the predictive 10th to 90th percentile | the prompt's "range" for days a run will take; graded on the expected days and the verdicts, the range ends banded |
| SF8 | hall B's load after a block's run finishes early | idle; backfill | backfill (busy to the window's end) | the reservation terms |
| SF9 | a run that would run past its window | stopped at the window's end; continued at the same conditions | continued under the planned hall load to the budget | the prompt asks the days each run will take; the reservation map gives the load after each window; same set |
| SF10 | the attribution order of the bridge | sequential in a stated order; log shares; Shapley over the causes | sequential in the order the answer blocks state | every alternative lands each item inside its band (asserted); same verdicts |

## Closure table

| Axis | Closure |
|---|---|
| 1 | Population: the 2027 runs are the roadmap's rows; the 2026 population is every run launched in 2026 (data dictionary); C1 for the verdicts |
| 2 | Unit of account: a run; days and GPU-days named in the asks; C4 (GPU-days against days differ by a run's node count) |
| 3 | Attribution window: a window runs 00:00 UTC on its first day to 00:00 UTC on the day after its last; no run starts off a day boundary |
| 4 | As-of dating: the record ends 31 October 2026, pulled 6 November; the 2027 roadmap and calendar as filed on 4 November |
| 5 | Version basis: the roadmap's v7 (the only version shipped); configs carry the same run IDs |
| 6 | Denominator: tokens counted by the trainer (real tokens) over days; filed in the terms |
| 7 | Weighting: the 2026 bridge sums GPU-days over runs (no weighting); the per-rank model fitted on rank-steps; C1 across fits per context and pooled |
| 8 | Window length: the throttle response fitted on all 2026 capped intervals; interruption rates on all of 2026 by hall; C3 across the first half against the whole year |
| 9 | Boundary inclusivity: inside the window means the expected finish at or before 00:00 UTC on the day after the last reserved day; no run sits within 12 per cent of it |
| 10 | Rounding path: days to 0.1, GPU-days to 10, shares to 0.1 point in the answer blocks; no figure within a cell's edge by construction |
| 11 | Tie-break: none needed; no two runs share a window or a verdict condition |
| 12 | Maturity and censoring: 2026 runs still live on 31 October are in the ledger to the pull date with their held GPU-days so far; same call on 2027 |
| 13 | Order of operations: the bridge's order is stated in the answer blocks; C3 across orders (SF10) |
| 14 | Row order: replayed log rows removed by (run, step, timestamp); asserted order-free |
| 15 | Duplicate resolution: replayed rows are exact repeats; collapse to one |
| 16 | Identity normalisation: renamed runs mapped by the registry's previous-ID column; node IDs consistent across files |
| 17 | Netting against gross: none; every bridge item is a non-negative cost except mix attention, which the order states |
| 18 | Dimensional units: GiB against GB for checkpoints (data dictionary); tokens throughout |
| 19 | Code and status semantics: interruption kinds and run statuses defined in the data dictionary; no code decides a result |
| 20 | Integerisation: none; days are continuous |
| 21 | Clause scope: the reservation terms apply to every 2027 block; the backfill clause to reserved blocks only |
| 22 | Forward window contents: the 2027 roadmap (runs, blocks, windows, budgets), configs, length sample, works calendar and the pool's 2026 load as the shipped drivers for 2027 |

## Literal reader

The prompt asks which 2027 runs will not reach their token budgets inside their reserved windows and how many days
each will take against the benchmark; the reservation terms define the window, finishing and the test; the data
dictionary defines GPU-days held and the 2026 population. Executed word for word, each run's days are the wall-clock
days to its budget under the conditions the files describe, and the late set is every run whose expected finish
falls after its window; no filed sentence states a cost model, a packing fill, a throttle or an overrun, so every
literal reading needs the same estimates and none files a different verdict.

## Prompt contract

May not drop or change: the question (which H1 2027 runs will not reach their token budgets inside the reserved
windows), each run's expected days against its benchmark days with an 80 per cent range and the finish date, the
bridge cause by cause, the 2026 bridge from benchmark-implied GPU-days to GPU-days held, the note on which runs need
more time or a change, the deliverables by type (a spreadsheet and a short note). Must never add: a method or cause
(ranks, stragglers, packing, padding, power, capping, maintenance), a count the data hold (the number of runs or
halls), a file name, a rounding instruction, a role or a reader, a warning.

## Pre-ship check

Read against the built pack on 2026-11-13. The hidden factor record holds on the cut data: the slowest-rank wait
shows in every 2026 long-context run (overheads of 18 to 23 per cent on four sequences per rank), best-fit padding in
both 2026 best-fit runs (fills above 0.99), the hall B cap on 39 days touching every hall B run then, the row 6 fault
on hall A's September and October jobs; none sits only in a deciding unit. The effort test agrees with `effort.py`
(quick 7.0, careful but hurried 44.4, thorough 100; the largest hint rescues one result). `checks.py` passes 117
assertions (the world's replay files the same seven late runs and every run's days within 4 per cent; eight rivals
and ten perturbations hold; the distractors deleted leave every figure unchanged), `verify.py` recomputes 17 figures
on its own code path, two builds are byte-identical, the containers audit clean, `leak.py` returns REVIEW only (2027
plan dates, a coincidental 18,900 inside a node name, generic words in the two PDFs).

## Tried and rejected

- 2026-11-13, at the draw, before this world: an object store's 2027 durability by pool (latent sector errors under a fill-stretched scrub cadence, rebuilds slowed by concurrent rebuilds, racks sharing a power feed): two of its three deciding steps sit on the client's closed common-shock card, data-loss rates are rare-event figures too wide to force a set, and the setting is the client's triage example and storage strategy; dropped.
- 2026-11-13: a nightly data-pipeline SLA forecast (merge bias at DAG joins, skewed joins, executor queueing): a careful run simulates the DAG by reflex and queueing at shared slots sits next to the closed shared-resource card; dropped.
- 2026-11-13: an LLM-judge evaluation with differential misclassification by checkpoint: the runs' own field, judge-bias corrections are a reflex there, and its other steps (contamination, transport to traffic) are a planted defect and a closed card; dropped.
- 2026-11-13: a scaling-law loss forecast for a larger run (schedule-matched endpoints, repeated data, a downstream sigmoid): every step is published method the runs apply by reflex, and the training-run setting is the client's worked illustration and its machine-learning strategies 1 to 4; dropped.
- 2026-11-13, at the draw: the run's analysis type as Forecasting (BLOCK, ban.pairing against task24's General Statistics x Forecasting); drawn as Comparative Analysis & Explanation, which the bridge from benchmark to production is.
- 2026-11-13, at the draw: cross-pod gradient reduction and hot-spare exhaustion as stumps (dropped, see the screen); the row 6 cooling fault and the works overrun kept only as supporting steps.
